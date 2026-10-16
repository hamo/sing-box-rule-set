"""Verify dispatch and matching through both native format converters."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_build import ROOT, builder, adguard

COMPILER = ROOT / ".tools/sing-box"


@unittest.skipUnless(COMPILER.is_file(), "Run scripts/install-sing-box.py first")
class SRSTests(unittest.TestCase):
    def test_new_provider_builds_mixed_formats_and_preserves_originals(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            configs = directory / "configs"
            configs.mkdir()
            output = directory / "build"
            sources = [
                {"name": "adguard", "url": "https://fixture.example/adguard", "format": "adguard"},
                {"name": "adblock", "url": "https://fixture.example/adblock", "format": "adblock"},
                {"name": "source", "url": "https://fixture.example/source", "format": "sing-box"},
            ]
            (configs / "arbitrary_provider.json").write_text(json.dumps({"sources": sources}))
            texts = {
                "adguard": ("[Adblock Plus]\n||ads.example.com^\n"
                            "@@||allowed.ads.example.com^\n||track*.example.net^\n"),
                "source": json.dumps({"version": 3, "rules": [{
                    "domain": ["exact.example.org"], "domain_suffix": ["source.example.com"],
                    "domain_keyword": ["ad-keyword"],
                }]}),
            }
            texts["adblock"] = texts["adguard"]
            with patch.object(builder, "download", side_effect=lambda url, path:
                              path.write_text(texts[url.rsplit("/", 1)[1]])):
                builder.build(configs, output, str(COMPILER))
            for name, domain, expected in (
                ("adguard", "ads.example.com", True), ("adguard", "child.ads.example.com", True),
                ("adguard", "tracker.example.net", True), ("adguard", "allowed.ads.example.com", False),
                ("adguard", "child.allowed.ads.example.com", False), ("adguard", "example.com", False),
                ("adguard", "notads.example.com", False), ("adguard", "ads.example.com.evil", False),
                ("source", "source.example.com", True), ("source", "child.source.example.com", True),
                ("source", "exact.example.org", True), ("source", "child.exact.example.org", False),
                ("source", "prefix-ad-keyword.example.net", True),
                ("source", "example.com", False),
            ):
                with self.subTest(name=name, domain=domain):
                    result = subprocess.check_output([
                        str(COMPILER), "rule-set", "match", "--format", "binary",
                        str(output / f"{name}.srs"), domain,
                    ], text=True, stderr=subprocess.STDOUT)
                    self.assertEqual("match rules." in result, expected)
            self.assertEqual((output / "sources/adguard.txt").read_text(), texts["adguard"])
            self.assertEqual((output / "sources/adblock.txt").read_text(), texts["adblock"])
            self.assertEqual((output / "adblock.srs").read_bytes(), (output / "adguard.srs").read_bytes())
            self.assertEqual((output / "sources/source.json").read_text(), texts["source"])
            records = json.loads((output / "metadata.json").read_text())["sources"]
            self.assertEqual([r["format"] for r in records], ["adguard", "adblock", "sing-box"])
            self.assertTrue(all(r["provider"] == "arbitrary_provider" for r in records))
            # The compiler downgrades v3 JSON to SRS v2 when no v3-only fields are used.
            self.assertEqual([r["srs_version"] for r in records], [2, 2, 2])
            self.assertEqual(records[2]["upstream"]["version"], 3)

    def test_unsupported_modifier_fails_even_when_native_converter_exits_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("||example.com^\n||other.example^$dnstype=A\n")
            with self.assertRaisesRegex(ValueError, "skipped unsupported"):
                adguard.convert(source, Path(temp) / "output.srs", str(COMPILER), {})

    def test_badfilter_cancels_blocking_and_exception_rules_before_compilation(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("||disabled.example.com^\n||active.example.com^\n"
                              "@@||allowed.active.example.com^$important\n"
                              "||disabled.example.com^$badfilter\n"
                              "@@||allowed.active.example.com^$badfilter,important\n"
                              "||absent.example.com^$badfilter\n")
            output = Path(temp) / "output.srs"
            record = adguard.convert(source, output, str(COMPILER), {})
            self.assertEqual(record["rule_count"], 6)
            self.assertEqual(record["conversion"]["compiled_rule_count"], 1)
            self.assertEqual(len(record["conversion"]["disabled_rules"]), 2)
            self.assertEqual(len(record["conversion"]["badfilter_rules"]), 3)
            for domain, expected in (("disabled.example.com", False), ("active.example.com", True),
                                     ("allowed.active.example.com", True), ("absent.example.com", False)):
                with self.subTest(domain=domain):
                    result = subprocess.check_output([
                        str(COMPILER), "rule-set", "match", "--format", "binary", str(output), domain,
                    ], text=True, stderr=subprocess.STDOUT)
                    self.assertEqual("match rules." in result, expected)

    def test_explicit_report_policy_tracks_unsupported_rules_and_enforces_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_text("||ads.example.com^\n||192.0.2.1^\n||other.example^$dnstype=A\n")
            options = {"name": "fixture", "unsupported_policy": "report", "max_skipped_rules": 2}
            record = adguard.convert(source, Path(temp) / "output.srs", str(COMPILER), options)
            self.assertEqual(record["conversion"]["compiled_rule_count"], 1)
            self.assertEqual(record["conversion"]["skipped_rule_count"], 2)
            self.assertTrue(any("192.0.2.1" in rule for rule in record["conversion"]["skipped_rules"]))
            with self.assertRaisesRegex(ValueError, "exceeds max_skipped_rules"):
                adguard.convert(source, Path(temp) / "output.srs", str(COMPILER),
                                {**options, "max_skipped_rules": 1})
            with self.assertRaisesRegex(ValueError, "Too few compiled rules"):
                adguard.convert(source, Path(temp) / "output.srs", str(COMPILER),
                                {**options, "min_rules": 2})
            # The native raw-domain fast path can omit totals after skipping.
            # Refuse ambiguous accounting even in explicitly enabled report mode.
            source.write_text("ads.example.com\n||192.0.2.1^\n")
            with self.assertRaisesRegex(ValueError, "Cannot account"):
                adguard.convert(source, Path(temp) / "output.srs", str(COMPILER), options)

    def test_all_ten_domain_fragments_compile_and_preserve_hostname_matching(self):
        fragments = ["||countly-", "-ad123-", "-iklan-gif-", "-iklan789-", "-1080x140-",
                     "-1080x180-", "-1300-x-200-", "-720x90-", "-728-x-90-", "-970x90-"]
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            output = Path(temp) / "output.srs"
            source.write_text("\n".join(fragments) + "\n")
            record = adguard.convert(source, output, str(COMPILER), {})
            self.assertEqual(record["conversion"]["compiled_rule_count"], 10)
            self.assertEqual(record["conversion"]["skipped_rule_count"], 0)
            self.assertEqual([r["original"] for r in record["conversion"]["rewritten_rules"]], fragments)
            cases = [("countly-analytics.example.com", True), ("x.countly-analytics.example.com", True),
                     ("COUNTLY-ANALYTICS.EXAMPLE.COM", True), ("notcountly-analytics.example.com", False),
                     ("countly.example.com", False), ("ordinary.example.com", False)]
            for fragment in fragments[1:]:
                cases.extend([("x" + fragment + "y.example.com", True),
                              ("X" + fragment.upper() + "Y.EXAMPLE.COM", True),
                              ("x" + fragment.replace("-", "") + "y.example.com", False)])
            for domain, expected in cases:
                with self.subTest(domain=domain):
                    result = subprocess.check_output([
                        str(COMPILER), "rule-set", "match", "--format", "binary", str(output), domain,
                    ], text=True, stderr=subprocess.STDOUT)
                    self.assertEqual("match rules." in result, expected)

    def test_fragment_exceptions_and_badfilter_keep_their_effect_after_rewrite(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            output = Path(temp) / "output.srs"
            source.write_text("||countly-\n@@||countly-safe-\n-ad123-\n@@-safe-ad123-\n"
                              "-iklan-gif-\n-iklan-gif-$badfilter\n")
            record = adguard.convert(source, output, str(COMPILER), {})
            self.assertEqual(record["conversion"]["compiled_rule_count"], 4)
            self.assertEqual(len(record["conversion"]["rewritten_rules"]), 4)
            self.assertEqual(record["conversion"]["disabled_rules"], ["-iklan-gif-"])
            for domain, expected in (("countly-ads.example.com", True), ("countly-safe-ads.example.com", False),
                                     ("x.countly-safe-ads.example.com", False), ("x-ad123-y.example.com", True),
                                     ("x-safe-ad123-y.example.com", False), ("x-iklan-gif-y.example.com", False)):
                with self.subTest(domain=domain):
                    result = subprocess.check_output([
                        str(COMPILER), "rule-set", "match", "--format", "binary", str(output), domain,
                    ], text=True, stderr=subprocess.STDOUT)
                    self.assertEqual("match rules." in result, expected)


if __name__ == "__main__":
    unittest.main()

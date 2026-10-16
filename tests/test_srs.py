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


if __name__ == "__main__":
    unittest.main()

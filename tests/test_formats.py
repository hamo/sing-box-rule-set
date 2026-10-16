import json
import tempfile
import unittest
from pathlib import Path

from test_build import ROOT, adguard
from formats import sing_box


class AdGuardTests(unittest.TestCase):
    def test_optional_headers_metadata_counts_and_wildcards(self):
        source = {"validation": {"headers": ["[Adblock Plus]"], "count_field": "Entries"}}
        text = ("\ufeff[Adblock Plus]\r\n! Entries: 3\r\n! Version: 123\r\n\r\n"
                "||ads.example.com^\r\n@@||allowed.ads.example.com^\r\n*-ad.example.net*\r\n")
        normalized, count, metadata = adguard.inspect_list(text, source)
        self.assertEqual(count, 3)
        self.assertEqual(metadata["version"], "123")
        self.assertEqual(normalized.splitlines()[-3:], [
            "||ads.example.com^", "@@||allowed.ads.example.com^", "*-ad.example.net*",
        ])
        self.assertNotIn("[Adblock Plus]", normalized)
        self.assertEqual(adguard.inspect_list("||example.com^\n", {})[1], 1)

    def test_upstream_requirements_are_configuration_only(self):
        source = {"validation": {"title_prefix": "Example List", "count_field": "total lines"}}
        text = "!Title: Example List\n!Total lines: 1\n||example.com^\n"
        self.assertEqual(adguard.inspect_list(text, source)[1], 1)
        for invalid in (text.replace("lines: 1", "lines: 2"),
                        text.replace("Example List", "Other list"),
                        text.replace("!Total lines: 1\n", ""), "<html>error</html>"):
            with self.subTest(text=invalid), self.assertRaises(ValueError):
                adguard.inspect_list(invalid, source)

    def test_empty_or_below_minimum_lists_fail(self):
        for text, source in (("", {}), ("!comments only", {}),
                             ("||example.com^", {"min_rules": 2})):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "minimum"):
                adguard.inspect_list(text, source)

    def test_embedded_list_metadata_does_not_override_subscription_header(self):
        source = {"validation": {"title_prefix": "AdGuard DNS filter", "count_field": "entries"}}
        text = ("! Title: AdGuard DNS filter\n! Entries: 2\n! Version: subscription\n"
                "||ads.example.com^\n! Title: Embedded list\n! Entries: 1\n"
                "! Version: embedded\n||tracking.example.com^\n")
        normalized, count, metadata = adguard.inspect_list(text, source)
        self.assertEqual(count, 2)
        self.assertEqual(metadata["title"], "AdGuard DNS filter")
        self.assertEqual(metadata["version"], "subscription")
        self.assertIn("! Title: Embedded list", normalized)

    def test_report_policy_requires_explicit_skip_limit(self):
        for source in ({"unsupported_policy": "ignore"}, {"unsupported_policy": "report"},
                       {"unsupported_policy": "report", "max_skipped_rules": True},
                       {"max_skipped_rules": 1}):
            with self.subTest(source=source), self.assertRaises(ValueError):
                adguard.validate(source)
        adguard.validate({"unsupported_policy": "report", "max_skipped_rules": 200})

    def test_badfilter_keeps_comments_and_regex_anchors_and_rejects_partial_cancellation(self):
        normalized = "! ||example.com^$badfilter\n/ads[0-9]+\\.example\\.com$/\n"
        self.assertEqual(adguard.apply_badfilter(normalized), (normalized, [], []))
        for rule in ("||example.com^$badfilter,domain=other.example",
                     "0.0.0.0 example.com$badfilter"):
            with self.subTest(rule=rule), self.assertRaisesRegex(ValueError, "Unsupported badfilter"):
                adguard.apply_badfilter(rule + "\n")

    def test_fragment_rewrite_leaves_ip_regex_comments_and_modifiers_unchanged(self):
        lines = ["! -ad123-", "# ||countly-", "||192.0.2.1^", "||192.0.2.1",
                 r"/^192\.0\.2\.[1234]$/", "||ordinary.example^", "-ad123-$important",
                 "-ad123-$dnstype=A", "||countly-*", "||countly-^", "/-ad123-/"]
        text = "\n".join(lines) + "\n"
        self.assertEqual(adguard.rewrite_domain_fragments(text), (text, []))


class SingBoxTests(unittest.TestCase):
    def test_invalid_or_empty_json_fails_before_compilation(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.json"
            for config in ([], {}, {"version": 2, "rules": []},
                           {"version": 2, "rules": "invalid"}):
                source.write_text(json.dumps(config))
                with self.subTest(config=config), self.assertRaises(ValueError):
                    sing_box.convert(source, Path(temp) / "output.srs", "missing-compiler", {})


if __name__ == "__main__":
    unittest.main()

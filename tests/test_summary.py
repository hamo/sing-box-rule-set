"""Check the Actions summary with real mixed-format conversions."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_build import ROOT, builder

COMPILER = ROOT / ".tools/sing-box"
spec = importlib.util.spec_from_file_location("summary_verify", ROOT / "scripts/verify-build.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


@unittest.skipUnless(COMPILER.is_file(), "Run scripts/install-sing-box.py first")
class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        configs, output = root / "configs", root / "build"
        configs.mkdir()
        sources = [
            {"name": name, "format": name, "url": f"https://fixture.example/{name}",
             "unsupported_policy": "report", "max_skipped_rules": 1}
            for name in ("adguard", "adblock")
        ] + [
            {"name": name, "format": "sing-box", "url": f"https://fixture.example/{name}"}
            for name in ("json-group", "json-nested")
        ]
        (configs / "fixture.json").write_text(json.dumps({"sources": sources}))
        text_list = ("[Adblock Plus]\n! Title: Fixture\n\n"
                     "||active.example.com^\n@@||allowed.active.example.com^\n"
                     "||disabled.example.com^\n||disabled.example.com^$badfilter\n"
                     "||absent.example.com^$badfilter\n||192.0.2.1^\n")
        texts = {
            "adguard": text_list, "adblock": text_list,
            "json-group": '// Source: https://fixture.example/\n' + json.dumps({
                "version": 2, "rules": [{
                    "domain": ["exact.example.org", "other.example.org"],
                    "domain_suffix": "source.example.com", "domain_keyword": "ad-keyword",
                    "domain_regex": ["^ads"], "ip_cidr": [], "invert": True,
                }],
            }),
            "json-nested": json.dumps({"version": 2, "rules": [
                {"domain": ["a.example"]},
                {"type": "logical", "mode": "or", "rules": [
                    {"domain_suffix": ["b.example", "c.example"]},
                    {"type": "logical", "mode": "and", "rules": [
                        {"network": "tcp", "domain": "d.example", "port": 443},
                        {"ip_cidr": ["192.0.2.0/24", "2001:db8::/32"], "invert": True},
                    ]},
                ]},
            ]}),
        }
        with patch.object(builder, "download", side_effect=lambda url, path:
                          path.write_text(texts[url.rsplit("/", 1)[1]])):
            builder.build(configs, output, str(COMPILER))
        self.configs, self.output = configs, output

    def test_metadata_counts_match_console_and_actions_summary(self):
        root = Path(self.temp.name)
        configs, output = self.configs, self.output
        summary_file = root / "step-summary.md"
        console = subprocess.check_output([
            sys.executable, str(ROOT / "scripts/verify-build.py"), str(output),
            "--sources-dir", str(configs), "--summary", str(summary_file),
        ], text=True)
        summary = summary_file.read_text()
        self.assertEqual(console.rstrip(), summary.rstrip())
        self.assertIn("| Source rule lines | Rule objects | Match entries | Skipped |", summary)
        self.assertNotIn("Upstream objects/lines", summary)
        self.assertNotIn("| Compiled |", summary)
        expected = {
            "adguard": ["adguard", "6", "—", "2", "1"],
            "adblock": ["adblock", "6", "—", "2", "1"],
            "json-group": ["sing-box", "—", "1", "5", "0"],
            "json-nested": ["sing-box", "—", "6", "8", "0"],
        }
        rows = {}
        for line in summary.splitlines():
            if line.startswith("|"):
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                rows[cells[0]] = cells[1:]
        for name, columns in expected.items():
            with self.subTest(name=name):
                self.assertEqual(rows[name][:5], columns)
                self.assertEqual(int(rows[name][5].replace(",", "")),
                                 (output / f"{name}.srs").stat().st_size)
                self.assertEqual(rows[name][6], "2")
        self.assertIn("including nested logical containers", summary)
        self.assertIn("not unique domains or matched hosts", summary)
        self.assertIn("resolved 2 badfilter directives, disabled 1 rules, skipped 1", summary)
        # Preserve the existing metadata/min_rules contract while improving display.
        records = {r["name"]: r for r in json.loads((output / "metadata.json").read_text())["sources"]}
        self.assertEqual(records["json-nested"]["rule_count"], 2)
        self.assertEqual(records["adblock"]["rule_count"], 6)
        for name, columns in expected.items():
            with self.subTest(metadata=name):
                record = records[name]
                objects = record["rule_object_count"]
                if columns[2] == "—":
                    self.assertIsNone(objects)
                else:
                    self.assertIs(type(objects), int)
                    self.assertEqual(objects, int(columns[2]))
                self.assertIs(type(record["match_entry_count"]), int)
                self.assertEqual(record["match_entry_count"], int(columns[3]))

    def test_missing_invalid_or_inconsistent_metadata_counts_require_rebuild(self):
        metadata_path = self.output / "metadata.json"
        original = metadata_path.read_text()
        for index, record in enumerate(json.loads(original)["sources"]):
            for field in ("rule_object_count", "match_entry_count"):
                invalid_values = ("missing", -1, 0, True, False, "1", 1.0, {})
                if type(record[field]) is int:
                    invalid_values += (float(record[field]), str(record[field]), None)
                for invalid in invalid_values:
                    with self.subTest(name=record["name"], field=field, invalid=invalid):
                        metadata = json.loads(original)
                        changed = metadata["sources"][index]
                        if invalid == "missing":
                            del changed[field]
                        else:
                            changed[field] = invalid
                        metadata_path.write_text(json.dumps(metadata))
                        with self.assertRaisesRegex(ValueError, "metadata rule counts.*rebuild required"):
                            verifier.verify(self.output, self.configs)
        metadata_path.write_text(original)
        verifier.verify(self.output, self.configs)


if __name__ == "__main__":
    unittest.main()

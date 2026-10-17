"""Compile repository-owned rules without fetching any upstream list."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_build import ROOT, builder

COMPILER = ROOT / ".tools/sing-box"
spec = importlib.util.spec_from_file_location("custom_verify", ROOT / "scripts/verify-build.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


@unittest.skipUnless(COMPILER.is_file(), "Run scripts/install-sing-box.py first")
class CustomTests(unittest.TestCase):
    def test_local_build_preserves_source_and_rejects_stale_or_invalid_updates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sources").mkdir()
            (root / "rules").mkdir()
            (root / "docs").mkdir()
            (root / "docs/rule-set-README.md").write_text("custom rules\n")
            (root / "LICENSE").write_text("fixture license\n")
            raw = root / "rules/example.json"
            raw.write_text(json.dumps({"version": 2, "rules": [{"domain_suffix": ["example.com"]}]}))
            config = {"name": "example", "path": "rules/example.json", "format": "sing-box"}
            (root / "sources/custom.json").write_text(json.dumps({"sources": [config]}))
            output = root / "output"
            with patch.object(builder, "ROOT", root), patch.object(builder, "download") as download:
                builder.build(root / "sources", output, str(COMPILER))
                download.assert_not_called()
                self.assertEqual((output / "sources/example.json").read_bytes(), raw.read_bytes())
                record = json.loads((output / "metadata.json").read_text())["sources"][0]
                self.assertEqual(record["source_type"], "local")
                self.assertEqual(record["path"], config["path"])
                self.assertNotIn("download_url", record)
                verifier.verify(output, root / "sources")
                original = (output / "example.srs").read_bytes()
                raw.write_text(json.dumps({"version": 2, "rules": [{"domain_suffix": ["example.net"]}]}))
                with self.assertRaisesRegex(ValueError, "rebuild required"):
                    verifier.verify(output, root / "sources")
                builder.build(root / "sources", output, str(COMPILER))
                self.assertNotEqual((output / "example.srs").read_bytes(), original)
                verifier.verify(output, root / "sources")
                previous = (output / "example.srs").read_bytes()
                raw.write_text("invalid JSON")
                with self.assertRaises(ValueError):
                    builder.build(root / "sources", output, str(COMPILER))
                self.assertEqual((output / "example.srs").read_bytes(), previous)

    def test_finance_domains_and_subdomains_match_with_strict_suffix_boundaries(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "build"
            with patch.object(builder, "download") as download:
                builder.build(ROOT / "sources", output, str(COMPILER), ["custom"])
                download.assert_not_called()
            verifier.verify(output, ROOT / "sources", ["custom"])
            config = json.loads((ROOT / "rules/geosite-finance-us.json").read_text())
            domains = [domain for rule in config["rules"] for domain in rule["domain_suffix"]]
            self.assertEqual(len(domains), len(set(domains)))
            for domain in domains:
                for candidate, expected in ((domain, True), ("login." + domain, True),
                                            ("not" + domain, False), (domain + ".example.org", False)):
                    with self.subTest(domain=candidate):
                        result = subprocess.check_output([
                            str(COMPILER), "rule-set", "match", "--format", "binary",
                            str(output / "geosite-finance-us.srs"), candidate,
                        ], text=True, stderr=subprocess.STDOUT)
                        self.assertEqual("match rules." in result, expected)


if __name__ == "__main__":
    unittest.main()

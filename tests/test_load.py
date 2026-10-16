"""Require native startup to load both converter outputs and reject corruption."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from test_build import ROOT, adguard
from formats import sing_box

spec = importlib.util.spec_from_file_location("check_srs_load", ROOT / "scripts/check-srs-load.py")
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)
COMPILER = ROOT / ".tools/sing-box"


@unittest.skipUnless(COMPILER.is_file(), "Run scripts/install-sing-box.py first")
class LoadTests(unittest.TestCase):
    def test_native_startup_loads_mixed_srs_and_rejects_corrupt_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            raw = directory / "filter.txt"
            raw.write_text("||ads.example.com^\n||countly-\n-ad123-\n")
            adguard.convert(raw, directory / "adguard.srs", str(COMPILER), {})
            raw = directory / "source.json"
            raw.write_text(json.dumps({"version": 3, "rules": [{"domain_suffix": ["example.org"]}]}))
            sing_box.convert(raw, directory / "source.srs", str(COMPILER), {})
            self.assertEqual(loader.check_load(directory, COMPILER), 2)
            # A valid magic/version header alone must not pass the native load.
            (directory / "adguard.srs").write_bytes(b"SRS\x02broken payload")
            with self.assertRaisesRegex(ValueError, "failed to load SRS"):
                loader.check_load(directory, COMPILER)

    def test_empty_build_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "No SRS"):
                loader.check_load(Path(temp), COMPILER)


if __name__ == "__main__":
    unittest.main()

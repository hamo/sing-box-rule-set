import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build as builder
from formats import adguard


class DiscoveryTests(unittest.TestCase):
    def test_local_sources_reject_ambiguous_missing_and_escaping_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            configs = root / "sources"
            configs.mkdir()
            (root / "rules").mkdir()
            (root / "rules/example.json").write_text('{"version":2,"rules":[{}]}')
            (root / "rules/escape.json").symlink_to(ROOT / "README.md")
            source = {"name": "fixture", "format": "sing-box", "path": "rules/example.json"}
            for changes, remove_path, message in (
                ({"url": "https://example.org/list.json"}, False, "exactly one"),
                ({}, True, "exactly one"),
                ({"path": "../outside.json"}, False, "inside the repository"),
                ({"path": str(root / "rules/example.json")}, False, "inside the repository"),
                ({"path": "rules/missing.json"}, False, "existing file"),
                ({"path": ".git/config"}, False, "under rules/"),
                ({"path": "rules/escape.json"}, False, "existing file"),
                ({"path": ""}, False, "nonempty"),
                ({"path": "rules"}, False, "existing file"),
                ({"fallback_urls": []}, False, "do not support"),
            ):
                with self.subTest(changes=changes, remove_path=remove_path):
                    configured = {**source, **changes}
                    if remove_path:
                        configured.pop("path")
                    (configs / "custom.json").write_text(json.dumps({"sources": [configured]}))
                    with patch.object(builder, "ROOT", root), self.assertRaisesRegex(ValueError, message):
                        builder.load_sources(configs)

    def test_new_upstream_only_requires_url_and_format_config(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = {"name": "new-list", "url": "https://example.org/list.txt", "format": "adguard"}
            (directory / "new-provider.json").write_text(json.dumps({"sources": [source]}))
            self.assertEqual(builder.load_sources(directory), [("new-provider", adguard, source)])

    def test_invalid_format_duplicate_name_and_validation_fail_before_download(self):
        with self.assertRaisesRegex(ValueError, "Unknown upstreams"):
            builder.load_sources(ROOT / "sources", ["unknown"])
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = {"name": "fixture", "url": "https://example.org/", "format": "adguard"}
            for changes, duplicate, message in (
                ({"format": "unknown"}, False, "Unsupported source format"),
                ({}, True, "duplicate"),
                ({"validation": {"typo": True}}, False, "validation options"),
                ({"url": "http://example.org/"}, False, "HTTPS"),
                ({"min_rules": 0}, False, "positive integer"),
            ):
                with self.subTest(changes=changes, duplicate=duplicate):
                    configured = {**source, **changes}
                    (directory / "example.json").write_text(json.dumps({
                        "sources": [configured, configured] if duplicate else [configured],
                    }))
                    with self.assertRaisesRegex(ValueError, message):
                        builder.load_sources(directory)


class BuildTests(unittest.TestCase):
    def test_failed_primary_uses_configured_fallback(self):
        source = {"name": "fixture", "url": "https://primary.example/",
                  "fallback_urls": ["https://mirror.example/"]}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "source.txt"

            def download(url, destination):
                if url == source["url"]:
                    destination.write_text("partial download")
                    raise subprocess.CalledProcessError(28, "curl")
                destination.write_text("complete mirror data")

            with patch.object(builder, "download", side_effect=download):
                used = builder.download_source(source, path)
            self.assertEqual(used, source["fallback_urls"][0])
            self.assertEqual(path.read_text(), "complete mirror data")

    def test_second_source_failure_preserves_previous_complete_build(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            output = directory / "build"
            output.mkdir()
            (output / "previous.srs").write_bytes(b"previous good build")
            configs = directory / "configs"
            configs.mkdir()
            (configs / "example.json").write_text(json.dumps({"sources": [
                {"name": name, "format": "adguard", "url": f"https://{name}.example/",
                 "validation": {"headers": ["[Adblock Plus]"], "count_field": "entries"}}
                for name in ("first", "second")
            ]}))

            def download(url, path):
                path.write_text("[Adblock Plus]\n! Entries: 1\n||example.com^\n" if "first" in url
                                else "<html>upstream failed</html>")

            def run(command, **kwargs):
                Path(command[command.index("--output") + 1]).write_bytes(b"SRS\x02fake")
                return type("Result", (), {"returncode": 0, "stdout": "parsed rules: 1/1\n"})()

            with patch.object(builder.subprocess, "check_output", return_value="sing-box test\n"), \
                    patch.object(builder, "download", side_effect=download), \
                    patch.object(adguard.subprocess, "run", side_effect=run), \
                    self.assertRaisesRegex(ValueError, "Missing"):
                builder.build(configs, output, "sing-box")
            self.assertEqual(list(output.iterdir()), [output / "previous.srs"])
            self.assertEqual((output / "previous.srs").read_bytes(), b"previous good build")


if __name__ == "__main__":
    unittest.main()

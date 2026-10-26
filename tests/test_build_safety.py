"""Protect maintained files and recover the previous build on replacement errors."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_build import ROOT, builder
from formats import sing_box


class BuildSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.configs, self.output = self.root / "sources", self.root / "build"
        for name in ("sources", "rules", "docs", ".tools", "build"):
            (self.root / name).mkdir()
        (self.root / "LICENSE").write_text("fixture license")
        (self.root / "docs/rule-set-README.md").write_text("fixture docs")
        (self.root / "rules/local.json").write_text("hand maintained source")
        (self.output / "previous.srs").write_bytes(b"previous complete build")
        (self.output / "nested").mkdir()
        (self.output / "nested/source.txt").write_text("old source")
        (self.configs / "fixture.json").write_text(json.dumps({"sources": [
            {"name": "fixture", "url": "https://fixture.example/list", "format": "sing-box"},
        ]}))

    @staticmethod
    def tree(path):
        return {p.relative_to(path).as_posix(): p.read_bytes() for p in path.rglob("*") if p.is_file()}

    def build(self):
        def compile_rule(command, **kwargs):
            Path(command[command.index("--output") + 1]).write_bytes(b"SRS\x02fixture")

        with patch.object(builder, "ROOT", self.root), \
                patch.object(builder, "download", side_effect=lambda u, p:
                             p.write_text('{"version":2,"rules":[{"domain":["example.org"]}]}')), \
                patch.object(builder.subprocess, "check_output", return_value="sing-box fixture\n"), \
                patch.object(sing_box.subprocess, "run", side_effect=compile_rule):
            builder.build(self.configs, self.output, str(self.root / ".tools/sing-box"))

    def test_maintained_directories_and_external_inputs_are_rejected_before_build(self):
        (self.root / "alias").symlink_to(self.root / "rules", target_is_directory=True)
        protected = [self.root / name for name in
                     ("rules", "sources", "scripts", "tests", "docs", "tools", ".tools", ".github", ".git")]
        protected += [self.root, self.root.parent, self.root / "alias", self.root / "rules/nested"]
        protected += [self.root / "LICENSE", self.root / "custom-bin", self.root / "custom-bin/sing-box"]
        (self.root / "other-repo/.git").mkdir(parents=True)
        protected.append(self.root / "other-repo")
        external_configs = self.root / "custom-configs"
        external_configs.mkdir()
        before = self.tree(self.root)
        for output in protected + [external_configs, external_configs / "nested"]:
            with self.subTest(output=output), patch.object(builder, "ROOT", self.root), \
                    patch.object(builder.subprocess, "check_output") as compiler, \
                    self.assertRaisesRegex(ValueError, "dedicated build directory"):
                builder.build(external_configs, output, str(self.root / "custom-bin/sing-box"))
            compiler.assert_not_called()
            self.assertEqual(before, self.tree(self.root))

    def test_cli_rejects_rules_output_in_an_isolated_repository(self):
        shutil.copytree(ROOT / "scripts", self.root / "scripts")
        result = subprocess.run([
            sys.executable, str(self.root / "scripts/build.py"), "--output", str(self.root / "rules"),
        ], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dedicated build directory", result.stderr)
        self.assertEqual((self.root / "rules/local.json").read_text(), "hand maintained source")

    def test_failed_replacement_or_interrupt_restores_old_build(self):
        original = self.tree(self.output)
        rename = Path.rename
        for error in (OSError("write failed"), KeyboardInterrupt()):
            def fail_install(path, target):
                if path.name.startswith(".rule-set-") and not path.name.startswith(".rule-set-backup-"):
                    raise error
                return rename(path, target)

            with self.subTest(error=type(error).__name__), \
                    patch.object(Path, "rename", autospec=True, side_effect=fail_install), \
                    self.assertRaises(type(error)):
                self.build()
            self.assertEqual(original, self.tree(self.output))
            self.assertEqual([], list(self.root.glob(".rule-set-*")))
        self.build()
        self.assertNotIn("previous.srs", self.tree(self.output))
        self.assertTrue((self.output / "fixture.srs").is_file())
        self.assertEqual([], list(self.root.glob(".rule-set-*")))

    def test_failed_restore_keeps_backup_outside_temporary_cleanup(self):
        original = self.tree(self.output)
        rename = Path.rename

        def fail_install_and_restore(path, target):
            if path != self.output:
                raise OSError("replacement and rollback failed")
            return rename(path, target)

        with patch.object(Path, "rename", autospec=True, side_effect=fail_install_and_restore), \
                self.assertRaises(OSError):
            self.build()
        backups = list(self.root.glob(".rule-set-backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(original, self.tree(backups[0]))


if __name__ == "__main__":
    unittest.main()

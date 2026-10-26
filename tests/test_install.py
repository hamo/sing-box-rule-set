"""Keep the working compiler until the downloaded executable has been checked."""

import hashlib
import importlib.util
import io
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_build import ROOT

spec = importlib.util.spec_from_file_location("install_compiler", ROOT / "scripts/install-sing-box.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "tools").mkdir()
        (self.root / ".tools").mkdir()
        self.destination = self.root / ".tools/sing-box"
        self.previous = b"previous working compiler"
        self.destination.write_bytes(self.previous)

    def install(self, executable, checksum_ok=True):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w:gz") as archive:
            entry = tarfile.TarInfo("sing-box-0.0.0-linux-amd64/sing-box")
            entry.size = len(executable)
            archive.addfile(entry, io.BytesIO(executable))
        data = stream.getvalue()
        digest = hashlib.sha256(data).hexdigest() if checksum_ok else "0" * 64
        (self.root / "tools/sing-box.json").write_text(json.dumps({
            "version": "0.0.0", "sha256": {"linux-amd64": digest},
        }))
        real_run = subprocess.run

        def download_or_check(command, **kwargs):
            if command[0] == "curl":
                Path(command[command.index("--output") + 1]).write_bytes(data)
                return subprocess.CompletedProcess(command, 0)
            self.assertEqual(self.destination.read_bytes(), self.previous)
            self.assertNotEqual(Path(command[0]), self.destination)
            return real_run(command, **kwargs)

        with patch.object(installer, "ROOT", self.root), \
                patch.object(installer.platform, "system", return_value="Linux"), \
                patch.object(installer.platform, "machine", return_value="x86_64"), \
                patch.object(installer.subprocess, "run", side_effect=download_or_check):
            installer.main()
        self.assertEqual([], list((self.root / ".tools").glob(".install-*")))

    def test_valid_executable_replaces_previous_only_after_version_check(self):
        executable = b"#!/bin/sh\nexit 0\n"
        self.install(executable)
        self.assertEqual(self.destination.read_bytes(), executable)
        self.assertTrue(self.destination.stat().st_mode & 0o111)

    def test_bad_checksum_or_failed_executable_preserves_previous(self):
        for executable, checksum_ok, error in (
            (b"#!/bin/sh\nexit 0\n", False, SystemExit),
            (b"#!/bin/sh\nexit 23\n", True, subprocess.CalledProcessError),
            (b"not an executable", True, OSError),
        ):
            with self.subTest(executable=executable), self.assertRaises(error):
                self.install(executable, checksum_ok)
            self.assertEqual(self.destination.read_bytes(), self.previous)
            self.assertEqual([], list((self.root / ".tools").glob(".install-*")))

    def test_failed_replace_preserves_previous(self):
        with patch.object(Path, "replace", side_effect=PermissionError("replacement failed")), \
                self.assertRaises(PermissionError):
            self.install(b"#!/bin/sh\nexit 0\n")
        self.assertEqual(self.destination.read_bytes(), self.previous)
        self.assertEqual([], list((self.root / ".tools").glob(".install-*")))


if __name__ == "__main__":
    unittest.main()

"""Exercise publication against a local bare Git remote; no network required."""

import os
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/publish.sh"
ROOT = SCRIPT.parents[1]


class PublishTests(unittest.TestCase):
    def test_first_publish_noop_and_fast_forward(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "repo"
            remote = root / "remote.git"
            output = root / "build"
            source.mkdir()
            output.mkdir()
            env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}

            def git(*args, cwd=source):
                return subprocess.check_output(["git", *args], cwd=cwd, env=env,
                                               stderr=subprocess.STDOUT, text=True).strip()

            git("init", "--bare", str(remote))
            git("init", "-b", "main")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.com")
            (source / "source-code.py").write_text("# main branch\n")
            git("add", ".")
            git("commit", "-m", "Initial code")
            main = git("rev-parse", "HEAD")
            git("remote", "add", "origin", str(remote))
            (output / "sources").mkdir()
            for name in ("README.md", "LICENSE"):
                (output / name).write_text("first version\n")
            records = []
            for config in sorted((ROOT / "sources").glob("*.json")):
                for item in json.loads(config.read_text())["sources"]:
                    name = item["name"]
                    extension = ".txt" if item["format"] == "adguard" else ".json"
                    binary = output / f"{name}.srs"
                    raw = output / "sources" / f"{name}{extension}"
                    binary.write_bytes(b"SRS\x02fixture")
                    raw.write_text("original source fixture\n")
                    records.append({
                        **item, "provider": config.stem, "srs_version": 2, "rule_count": 1,
                        "sha256": {path.relative_to(output).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                                   for path in (raw, binary)},
                    })

            def save_metadata():
                (output / "metadata.json").write_text(json.dumps({"compiler": "fixture", "sources": records}))

            save_metadata()

            def publish():
                return subprocess.check_output(["bash", str(SCRIPT), str(output)], cwd=source,
                                               env=env, stderr=subprocess.STDOUT, text=True)

            publish()
            first = git("rev-parse", "refs/heads/rule-set", cwd=remote)
            files = git("ls-tree", "-r", "--name-only", first, cwd=remote).splitlines()
            self.assertEqual(set(files), {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()})
            self.assertIn("unchanged", publish())
            self.assertEqual(first, git("rev-parse", "refs/heads/rule-set", cwd=remote))
            updated = records[0]
            binary = output / f"{updated['name']}.srs"
            binary.write_bytes(b"SRS\x02updated rules")
            updated["sha256"][binary.name] = hashlib.sha256(binary.read_bytes()).hexdigest()
            save_metadata()
            publish()
            second = git("rev-parse", "refs/heads/rule-set", cwd=remote)
            self.assertNotEqual(first, second)
            self.assertEqual(first, git("rev-parse", f"{second}^", cwd=remote))
            # Corrupt output must be rejected before the publication branch changes.
            binary.write_bytes(b"corrupted")
            with self.assertRaises(subprocess.CalledProcessError):
                publish()
            self.assertEqual(second, git("rev-parse", "refs/heads/rule-set", cwd=remote))
            self.assertEqual(main, git("rev-parse", "HEAD"))
            self.assertEqual("main", git("branch", "--show-current"))
            self.assertEqual("# main branch\n", (source / "source-code.py").read_text())


if __name__ == "__main__":
    unittest.main()

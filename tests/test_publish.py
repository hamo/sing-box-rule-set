"""Exercise publication against a local bare Git remote; no network required."""

import os
import hashlib
import json
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_build import builder

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/publish.sh"
ROOT = SCRIPT.parents[1]


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
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
                extension = builder.get_converter(item["format"]).EXTENSION
                binary = output / f"{name}.srs"
                raw = output / "sources" / f"{name}{extension}"
                binary.write_bytes(b"SRS\x02fixture")
                if "path" in item:
                    raw.write_bytes(builder.local_source_path(item).read_bytes())
                elif item["format"] == "sing-box":
                    raw.write_text(json.dumps({"version": 2, "rules": [{"domain": ["example.com"]}]}))
                else:
                    raw.write_text("original source fixture\n")
                count = (len(builder.get_converter("sing-box").load_config(raw.read_text())["rules"])
                         if item["format"] == "sing-box" else 1)
                records.append({
                    **item, "provider": config.stem, "srs_version": 2, "rule_count": count,
                    "source_type": "local" if "path" in item else "remote",
                    "sha256": {path.relative_to(output).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in (raw, binary)},
                })
                if item.get("unsupported_policy") == "report":
                    records[-1]["conversion"] = {
                        "compiled_rule_count": 1, "skipped_rule_count": 0,
                        "badfilter_rules": [], "disabled_rules": [], "skipped_rules": [],
                    }

        def save_metadata():
            (output / "metadata.json").write_text(json.dumps({"compiler": "fixture", "sources": records}))

        save_metadata()

        def publish():
            return subprocess.check_output(["bash", str(SCRIPT), str(output)], cwd=source,
                                           env=env, stderr=subprocess.STDOUT, text=True)

        self.source, self.remote, self.output = source, remote, output
        self.env, self.records, self.main = env, records, main
        self.git, self.save_metadata, self.publish = git, save_metadata, publish

    def test_first_publish_noop_and_fast_forward(self):
        git, publish, save_metadata = self.git, self.publish, self.save_metadata
        source, remote, output = self.source, self.remote, self.output
        records, main = self.records, self.main
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
        attempts, waits = self.reject_pushes(99)
        self.assertIn("unchanged", publish())
        self.assertFalse(attempts.exists())
        self.assertFalse(waits.exists())
        # A report must account for every input line before publication.
        reported = next(record for record in records if record.get("conversion"))
        reported["conversion"]["skipped_rule_count"] = 1
        save_metadata()
        with self.assertRaises(subprocess.CalledProcessError):
            publish()
        self.assertEqual(second, git("rev-parse", "refs/heads/rule-set", cwd=remote))
        reported["conversion"]["skipped_rule_count"] = 0
        save_metadata()
        # Corrupt output must be rejected before the publication branch changes.
        binary.write_bytes(b"corrupted")
        with self.assertRaises(subprocess.CalledProcessError):
            publish()
        self.assertEqual(second, git("rev-parse", "refs/heads/rule-set", cwd=remote))
        self.assertEqual(main, git("rev-parse", "HEAD"))
        self.assertEqual("main", git("branch", "--show-current"))
        self.assertEqual("# main branch\n", (source / "source-code.py").read_text())

    def reject_pushes(self, failures):
        """Use a real Git server hook to fail pushes; record sleeps without waiting."""
        root = Path(self.temp.name)
        attempts, waits = root / "push-attempts", root / "retry-waits"
        hook = self.remote / "hooks/pre-receive"
        hook.write_text(
            "#!/bin/sh\nset -eu\n"
            f"attempts={shlex.quote(str(attempts))}\n"
            "read old new ref\n"
            "printf '%s\\n' \"$new\" >> \"$attempts\"\n"
            "count=$(wc -l < \"$attempts\")\n"
            f'if [ "$count" -le {failures} ]; then\n'
            "  echo 'fatal error in commit_refs' >&2\n"
            "  exit 1\nfi\n"
        )
        hook.chmod(0o755)
        bin_dir = root / "bin"
        bin_dir.mkdir()
        sleep = bin_dir / "sleep"
        sleep.write_text("#!/bin/sh\n" +
                         f"printf '%s\\n' \"$1\" >> {shlex.quote(str(waits))}\n")
        sleep.chmod(0o755)
        self.env["PATH"] = str(bin_dir) + os.pathsep + self.env["PATH"]
        return attempts, waits

    def assert_checkout_intact(self):
        self.assertEqual(self.main, self.git("rev-parse", "HEAD"))
        self.assertEqual("main", self.git("branch", "--show-current"))
        self.assertEqual("", self.git("status", "--porcelain"))
        worktrees = self.git("worktree", "list", "--porcelain")
        self.assertEqual(1, sum(line.startswith("worktree ") for line in worktrees.splitlines()))

    def test_transient_push_failures_recover_on_last_attempt(self):
        attempts, waits = self.reject_pushes(2)
        previous = None
        for content in ("first version\n", "updated version\n"):
            with self.subTest(content=content):
                (self.output / "README.md").write_text(content)
                attempts.unlink(missing_ok=True)
                waits.unlink(missing_ok=True)
                log = self.publish()
                self.assertIn("fatal error in commit_refs", log)
                proposed = attempts.read_text().splitlines()
                self.assertEqual(3, len(proposed))
                self.assertEqual(1, len(set(proposed)))
                self.assertEqual(["5", "10"], waits.read_text().splitlines())
                published = self.git("rev-parse", "refs/heads/rule-set", cwd=self.remote)
                self.assertEqual(proposed[0], published)
                self.assertEqual(content.strip(), self.git("show", f"{published}:README.md", cwd=self.remote))
                if previous:
                    self.assertEqual(previous, self.git("rev-parse", f"{published}^", cwd=self.remote))
                else:
                    self.assertEqual("1", self.git("rev-list", "--count", published, cwd=self.remote))
                previous = published
                self.assert_checkout_intact()

    def test_push_retry_exhaustion_preserves_published_branch(self):
        self.publish()
        previous = self.git("rev-parse", "refs/heads/rule-set", cwd=self.remote)
        (self.output / "README.md").write_text("unpublished update\n")
        attempts, waits = self.reject_pushes(99)
        with self.assertRaises(subprocess.CalledProcessError) as raised:
            self.publish()
        self.assertEqual(1, raised.exception.returncode)
        self.assertIn("Publication failed after 3 push attempts.", raised.exception.output)
        proposed = attempts.read_text().splitlines()
        self.assertEqual(3, len(proposed))
        self.assertEqual(1, len(set(proposed)))
        self.assertEqual(["5", "10"], waits.read_text().splitlines())
        self.assertEqual(previous, self.git("rev-parse", "refs/heads/rule-set", cwd=self.remote))
        self.assert_checkout_intact()


if __name__ == "__main__":
    unittest.main()

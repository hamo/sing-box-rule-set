#!/usr/bin/env python3
"""Start sing-box with every built SRS and require successful initialization."""

import argparse
import json
import subprocess
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_load(output, compiler, timeout=30):
    binaries = sorted(output.resolve().glob("*.srs"))
    if not binaries:
        raise ValueError("No SRS files to load")
    config = {
        "log": {"level": "info"},
        "route": {"rule_set": [
            {"type": "local", "tag": path.stem, "format": "binary", "path": str(path)}
            for path in binaries
        ]},
        "outbounds": [{"type": "direct", "tag": "direct"}],
    }
    with tempfile.TemporaryDirectory(prefix="srs-load-") as temp:
        path = Path(temp) / "config.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        process = subprocess.Popen([
            str(compiler), "--disable-color", "run", "--config", str(path),
        ], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = []
        started = threading.Event()

        def read_logs():
            for line in process.stdout:
                lines.append(line)
                if "sing-box started (" in line:
                    started.set()

        reader = threading.Thread(target=read_logs, daemon=True)
        reader.start()
        deadline = time.monotonic() + timeout
        try:
            while not started.wait(0.1):
                if process.poll() is not None:
                    reader.join(timeout=5)
                    raise ValueError("sing-box failed to load SRS files:\n" + "".join(lines))
                if time.monotonic() >= deadline:
                    raise ValueError("Timed out waiting for sing-box startup:\n" + "".join(lines))
            if process.poll() is not None:
                raise ValueError("sing-box exited immediately after startup:\n" + "".join(lines))
        finally:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            reader.join(timeout=5)
            process.stdout.close()
        if process.returncode:
            raise ValueError("sing-box did not shut down cleanly:\n" + "".join(lines))
    return len(binaries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, nargs="?", default=ROOT / "build")
    parser.add_argument("--sing-box", type=Path, default=ROOT / ".tools/sing-box")
    args = parser.parse_args()
    count = check_load(args.output, args.sing_box.resolve())
    print(f"sing-box successfully loaded all {count} SRS files, started and shut down cleanly.")


if __name__ == "__main__":
    main()

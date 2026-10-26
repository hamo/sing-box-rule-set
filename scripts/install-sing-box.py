#!/usr/bin/env python3
"""Install the pinned official compiler after verifying the archive hash."""

import hashlib
import json
import platform
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = json.loads((ROOT / "tools/sing-box.json").read_text())
    arch = {"x86_64": "amd64", "aarch64": "arm64", "arm64": "arm64"}.get(
        platform.machine().lower(), platform.machine().lower()
    )
    target = f"{platform.system().lower()}-{arch}"
    expected = config["sha256"].get(target)
    if not expected:
        raise SystemExit(f"Unsupported platform: {target}; install sing-box manually")
    version = config["version"]
    package = f"sing-box-{version}-{target}"
    url = f"https://github.com/SagerNet/sing-box/releases/download/v{version}/{package}.tar.gz"
    destination = ROOT / ".tools/sing-box"
    destination.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".install-", dir=destination.parent) as temp:
        archive = Path(temp) / "sing-box.tar.gz"
        subprocess.run([
            "curl", "--fail", "--silent", "--show-error", "--location",
            "--retry", "3", "--connect-timeout", "15", "--max-time", "180",
            "--output", str(archive), url,
        ], check=True)
        if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
            raise SystemExit("sing-box archive SHA-256 mismatch")
        with tarfile.open(archive) as tar:
            binary = tar.extractfile(f"{package}/sing-box")
            if binary is None:
                raise SystemExit("sing-box binary missing from archive")
            staged = Path(temp) / "sing-box"
            with binary, staged.open("wb") as output:
                shutil.copyfileobj(binary, output)
            staged.chmod(0o755)
            subprocess.run([str(staged), "version"], check=True)
            staged.replace(destination)


if __name__ == "__main__":
    main()

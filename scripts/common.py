"""Shared download and artifact metadata helpers."""

import hashlib
import json
import subprocess


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(url, destination):
    if not url.startswith("https://"):
        raise ValueError("Source URLs must use HTTPS")
    subprocess.run([
        "curl", "--fail", "--silent", "--show-error", "--location",
        "--proto", "=https", "--proto-redir", "=https",
        "--retry", "2", "--retry-max-time", "180", "--connect-timeout", "15", "--max-time", "120",
        "--speed-limit", "1024", "--speed-time", "30",
        "--max-filesize", "104857600", "--output", str(destination), url,
    ], check=True)


def srs_version(path):
    with path.open("rb") as stream:
        header = stream.read(4)
        payload = stream.read(1)
    if len(header) != 4 or header[:3] != b"SRS" or not payload:
        raise ValueError(f"Invalid or empty SRS output: {path.name}")
    return header[3]

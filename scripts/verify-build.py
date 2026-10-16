#!/usr/bin/env python3
"""Verify complete build contents and checksums before publishing."""

import argparse
import json
from pathlib import Path

from build import ROOT, load_sources
from common import sha256, srs_version


def verify(output, config_dir):
    expected = {source["name"]: (provider, converter, source)
                for provider, converter, source in load_sources(config_dir)}
    metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
    records = metadata["sources"]
    names = [record["name"] for record in records]
    if len(set(names)) != len(names) or set(names) != set(expected):
        raise ValueError("Build does not contain exactly the configured rule sets")
    binaries = {path.stem for path in output.glob("*.srs")}
    if binaries != set(expected):
        raise ValueError("Missing or unexpected SRS files")
    allowed = {"metadata.json", "README.md", "LICENSE"}
    rows = []
    for record in records:
        name = record["name"]
        provider, converter, source = expected[name]
        if record["provider"] != provider or any(record.get(key) != value for key, value in source.items()):
            raise ValueError(f"{name}: metadata does not match source configuration")
        files = {f"{name}.srs", f"sources/{name}{converter.EXTENSION}"}
        if set(record["sha256"]) != files:
            raise ValueError(f"{name}: missing or unexpected checksums")
        for filename in files:
            path = output / filename
            if not path.is_file() or path.stat().st_size == 0 or sha256(path) != record["sha256"][filename]:
                raise ValueError(f"{name}: missing, empty or corrupt file: {filename}")
        if srs_version(output / f"{name}.srs") != record["srs_version"]:
            raise ValueError(f"{name}: SRS version mismatch")
        allowed.update(files)
        rows.append(f"| {name} | {record['format']} | {record['rule_count']:,} | "
                    f"{(output / (name + '.srs')).stat().st_size:,} | {record['srs_version']} |")
    actual = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
    if actual != allowed:
        raise ValueError(f"Unexpected or missing build files: {sorted(actual ^ allowed)}")
    for filename in ("README.md", "LICENSE"):
        if not (output / filename).stat().st_size:
            raise ValueError(f"Empty {filename}")
    return (f"Verified {len(records)} rule sets; all files and SHA-256 checksums match.\n\n"
            "| Rule set | Format | Rule objects/lines | SRS bytes | SRS version |\n"
            "| --- | --- | ---: | ---: | ---: |\n" + "\n".join(rows) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sources-dir", type=Path, default=ROOT / "sources")
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    summary = verify(args.output.resolve(), args.sources_dir.resolve())
    print(summary)
    if args.summary:
        with args.summary.open("a", encoding="utf-8") as stream:
            stream.write(summary)


if __name__ == "__main__":
    main()

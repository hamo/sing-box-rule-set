#!/usr/bin/env python3
"""Verify complete build contents and checksums before publishing."""

import argparse
import json
from pathlib import Path

from build import ROOT, load_sources, local_source_path
from common import sha256, srs_version
from formats import sing_box


def verify(output, config_dir, selected=None):
    expected = {source["name"]: (provider, converter, source)
                for provider, converter, source in load_sources(config_dir, selected)}
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
    notes = []
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
        if "path" in source:
            original = output / "sources" / f"{name}{converter.EXTENSION}"
            if (record.get("source_type") != "local" or "download_url" in record
                    or sha256(original) != sha256(local_source_path(source))):
                raise ValueError(f"{name}: local source changed or provenance is incorrect; rebuild required")
        if srs_version(output / f"{name}.srs") != record["srs_version"]:
            raise ValueError(f"{name}: SRS version mismatch")
        conversion = record.get("conversion", {})
        compiled = conversion.get("compiled_rule_count", record["rule_count"])
        skipped = conversion.get("skipped_rule_count", 0)
        if source.get("unsupported_policy") == "report" and not conversion:
            raise ValueError(f"{name}: missing conversion report")
        if conversion:
            skipped_rules = conversion["skipped_rules"]
            badfilters = conversion["badfilter_rules"]
            disabled = conversion["disabled_rules"]
            rewritten = conversion.get("rewritten_rules", [])
            if (skipped != len(skipped_rules)
                    or compiled + skipped + len(badfilters) + len(disabled) != record["rule_count"]
                    or skipped > source.get("max_skipped_rules", 0)):
                raise ValueError(f"{name}: invalid conversion counts")
            if skipped or badfilters:
                notes.append(f"\n{name}: resolved {len(badfilters)} badfilter directives, "
                             f"disabled {len(disabled)} rules, skipped {skipped} unsupported rules.\n")
            if rewritten:
                notes.append(f"\n{name}: rewrote {len(rewritten)} domain-fragment rules "
                             "as equivalent hostname regex rules (included in compiled count).\n")
                mappings = [f"{rule['original']} -> {rule['converted']}" for rule in rewritten]
                notes.append(f"\n<details><summary>{name}: rewritten domain fragments</summary>\n\n"
                             "```text\n" + "\n".join(mappings) + "\n```\n\n</details>\n")
            if skipped:
                notes.append(f"\n<details><summary>{name}: unsupported rules and reasons</summary>\n\n"
                             "```text\n" + "\n".join(skipped_rules) + "\n```\n\n</details>\n")
        allowed.update(files)
        if record["format"] == "sing-box":
            raw = output / "sources" / f"{name}{converter.EXTENSION}"
            config = sing_box.load_config(raw.read_text(encoding="utf-8"))
            objects, entries = sing_box.rule_counts(config["rules"])
            source_lines, object_count = "—", f"{objects:,}"
        else:
            source_lines, object_count, entries = f"{record['rule_count']:,}", "—", compiled
        rows.append(f"| {name} | {record['format']} | {source_lines} | {object_count} | "
                    f"{entries:,} | {skipped:,} | {(output / (name + '.srs')).stat().st_size:,} | "
                    f"{record['srs_version']} |")
    actual = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
    if actual != allowed:
        raise ValueError(f"Unexpected or missing build files: {sorted(actual ^ allowed)}")
    for filename in ("README.md", "LICENSE"):
        if not (output / filename).stat().st_size:
            raise ValueError(f"Empty {filename}")
    return (f"Verified {len(records)} rule sets; all files and SHA-256 checksums match.\n\n"
            "| Rule set | Format | Source rule lines | Rule objects | Match entries | Skipped | SRS bytes | SRS version |\n"
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |\n" + "\n".join(rows) + "\n\n"
            "Source rule lines exclude comments, blank lines and subscription headers; — means not applicable.\n"
            "Rule objects count all JSON rules, including nested logical containers. Match entries count "
            "JSON matcher values (excluding structural fields) or successfully converted text rules "
            "(including exceptions, excluding badfilter directives, disabled and skipped rules).\n"
            "Counts are before compiler deduplication/optimization, not unique domains or matched hosts.\n"
            + "".join(notes))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sources-dir", type=Path, default=ROOT / "sources")
    parser.add_argument("--source", "--upstream", dest="selected", action="append",
                        help="Verify only this source group; repeatable")
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    summary = verify(args.output.resolve(), args.sources_dir.resolve(), args.selected)
    print(summary)
    if args.summary:
        with args.summary.open("a", encoding="utf-8") as stream:
            stream.write(summary)


if __name__ == "__main__":
    main()

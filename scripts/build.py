#!/usr/bin/env python3
"""Build remote and repository-maintained rules using format-based converters."""

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from common import download, sha256, srs_version, write_json
from formats import get_converter

ROOT = Path(__file__).resolve().parents[1]


def local_source_path(source):
    value = source.get("path")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Local source path must be a nonempty repository-relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Local source path must stay inside the repository")
    if not path.parts or path.parts[0] != "rules":
        raise ValueError("Local sources must be maintained under rules/")
    resolved = (ROOT / path).resolve()
    if (not resolved.is_relative_to(ROOT.resolve())
            or not resolved.is_relative_to((ROOT / "rules").resolve()) or not resolved.is_file()):
        raise ValueError(f"Local source must be an existing file inside the repository: {value}")
    return resolved


def load_sources(directory, selected=None):
    configs = {path.stem: path for path in sorted(directory.glob("*.json"))}
    if selected:
        unknown = set(selected) - configs.keys()
        if unknown:
            raise ValueError(f"Unknown upstreams: {', '.join(sorted(unknown))}")
        configs = {name: path for name, path in configs.items() if name in selected}
    loaded = []
    names = set()
    for provider, path in configs.items():
        if not re.fullmatch(r"[a-z0-9]+(?:[-_][a-z0-9]+)*", provider):
            raise ValueError(f"Invalid upstream configuration name: {provider}")
        sources = json.loads(path.read_text(encoding="utf-8"))["sources"]
        if not sources:
            raise ValueError(f"No sources configured for {provider}")
        for source in sources:
            name = source["name"]
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in names:
                raise ValueError(f"Invalid or duplicate source name: {name}")
            if ("url" in source) == ("path" in source):
                raise ValueError("Source must specify exactly one of url or path")
            if "path" in source:
                local_source_path(source)
                if "fallback_urls" in source:
                    raise ValueError("Local sources do not support fallback_urls")
            elif not isinstance(source["url"], str) or not source["url"].startswith("https://"):
                raise ValueError("Source URLs must use HTTPS")
            fallbacks = source.get("fallback_urls", [])
            if not isinstance(fallbacks, list) or any(
                not isinstance(url, str) or not url.startswith("https://") for url in fallbacks
            ):
                raise ValueError("fallback_urls must be an array of HTTPS URLs")
            minimum = source.get("min_rules", 1)
            if type(minimum) is not int or minimum < 1:
                raise ValueError("min_rules must be a positive integer")
            converter = get_converter(source["format"])
            converter.validate(source)
            names.add(name)
            loaded.append((provider, converter, source))
    if not loaded:
        raise ValueError(f"No upstream configurations found in {directory}")
    return loaded


def download_source(source, destination):
    urls = [source["url"], *source.get("fallback_urls", [])]
    for index, url in enumerate(urls):
        try:
            download(url, destination)
            return url
        except subprocess.CalledProcessError:
            if index == len(urls) - 1:
                raise
            print(f"{source['name']}: download failed; trying fallback {index + 1}", flush=True)


def build(config_dir, output, compiler, selected=None):
    sources = load_sources(config_dir, selected)
    version = subprocess.check_output([compiler, "version"], text=True).splitlines()[0]
    output.parent.mkdir(parents=True, exist_ok=True)
    # No existing output is changed if any upstream fails.
    with tempfile.TemporaryDirectory(prefix=".rule-set-", dir=output.parent) as temp:
        staged = Path(temp)
        records = []
        (staged / "sources").mkdir()
        for provider, converter, source in sources:
            raw = staged / "sources" / f"{source['name']}{converter.EXTENSION}"
            if "path" in source:
                shutil.copyfile(local_source_path(source), raw)
                origin = {"source_type": "local"}
            else:
                used_url = download_source(source, raw)
                origin = {"source_type": "remote", "download_url": used_url}
            binary = staged / f"{source['name']}.srs"
            record = converter.convert(raw, binary, compiler, source)
            actual_version = srs_version(binary)
            records.append({
                **source, **record, "provider": provider, "srs_version": actual_version,
                **origin,
                "sha256": {path.relative_to(staged).as_posix(): sha256(path) for path in (raw, binary)},
            })
            print(f"{source['name']}: {binary.stat().st_size:,} bytes (SRS v{actual_version})",
                  flush=True)
        write_json(staged / "metadata.json", {"compiler": version, "sources": records})
        shutil.copy2(ROOT / "LICENSE", staged / "LICENSE")
        shutil.copy2(ROOT / "docs/rule-set-README.md", staged / "README.md")
        output.mkdir(exist_ok=True)
        for path in output.iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        for path in staged.iterdir():
            shutil.move(str(path), output / path.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources-dir", type=Path, default=ROOT / "sources")
    parser.add_argument("--source", "--upstream", dest="upstream", action="append",
                        help="Build only this source group (including custom); repeatable")
    parser.add_argument("--output", type=Path, default=ROOT / "build")
    parser.add_argument("--sing-box", default=str(ROOT / ".tools/sing-box"))
    args = parser.parse_args()
    output = args.output.resolve()
    git_dir = ROOT / ".git"
    if (output == ROOT or ROOT.is_relative_to(output) or (output / ".git").exists()
            or output == git_dir or git_dir in output.parents):
        parser.error("Output must be a dedicated build directory, not a repository or its parent")
    build(args.sources_dir.resolve(), output, args.sing_box, args.upstream)


if __name__ == "__main__":
    main()

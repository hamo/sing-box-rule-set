"""Convert AdGuard-compatible lists using sing-box's native converter."""

import re
import subprocess
import tempfile
from pathlib import Path

EXTENSION = ".txt"
SUBSCRIPTION_HEADERS = ("[Adblock Plus]", "[AdGuard]")


def validate(source):
    validation = source.get("validation", {})
    if not isinstance(validation, dict):
        raise ValueError("validation must be an object")
    unknown = validation.keys() - {"headers", "title_prefix", "count_field"}
    if unknown:
        raise ValueError(f"Unsupported AdGuard validation options: {', '.join(sorted(unknown))}")
    if "headers" in validation:
        headers = validation["headers"]
        if not isinstance(headers, list) or not headers or any(h not in SUBSCRIPTION_HEADERS for h in headers):
            raise ValueError(f"headers must be a nonempty list of {SUBSCRIPTION_HEADERS}")
    for key in ("title_prefix", "count_field"):
        if key in validation and (not isinstance(validation[key], str) or not validation[key].strip()):
            raise ValueError(f"{key} must be a nonempty string")


def inspect_list(text, source):
    """Normalize subscription metadata; rule interpretation belongs to sing-box."""
    lines = text.lstrip("\ufeff").splitlines()
    validation = source.get("validation", {})
    first = lines[0].strip() if lines else ""
    if validation.get("headers") and first not in validation["headers"]:
        raise ValueError("Missing configured filter-list header")
    if first in SUBSCRIPTION_HEADERS:
        lines = lines[1:]
    metadata = {}
    count = 0
    normalized = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        normalized.append(line)
        if line.startswith(("!", "#")):
            key, separator, value = line[1:].partition(":")
            if separator:
                metadata[key.strip().lower()] = value.strip()
        else:
            count += 1
    prefix = validation.get("title_prefix")
    if prefix and not metadata.get("title", "").startswith(prefix):
        raise ValueError(f"Filter-list title must start with {prefix!r}")
    field = validation.get("count_field")
    if field:
        declared = metadata.get(field.strip().lower(), "")
        if not declared.isdigit() or int(declared) != count:
            raise ValueError(f"Entry count mismatch: {field}={declared!r}, actual={count}")
    minimum = source.get("min_rules", 1)
    if count < minimum:
        raise ValueError(f"Only {count} rules; minimum {minimum}")
    return "\n".join(normalized) + "\n", count, metadata


def convert(raw, output, compiler, source):
    normalized, count, metadata = inspect_list(raw.read_text(encoding="utf-8-sig"), source)
    with tempfile.TemporaryDirectory(prefix="adguard-") as temp:
        converter_input = Path(temp) / "input.txt"
        converter_input.write_text(normalized, encoding="utf-8")
        result = subprocess.run([
            compiler, "--disable-color", "rule-set", "convert", "--type", "adguard",
            "--output", str(output), str(converter_input),
        ], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise ValueError(f"AdGuard conversion failed:\n{result.stdout}")
    # Native conversion can exit successfully while skipping unsupported rules.
    counts = re.search(r"parsed rules: (\d+)/(\d+)", result.stdout)
    if "ignored unsupported" in result.stdout or (counts and int(counts[1]) != int(counts[2])):
        raise ValueError(f"AdGuard conversion skipped unsupported rules:\n{result.stdout}")
    return {"rule_count": count, "upstream": metadata}

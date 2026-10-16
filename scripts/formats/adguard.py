"""Convert AdGuard-compatible lists using sing-box's native converter."""

import re
import subprocess
import tempfile
from pathlib import Path

EXTENSION = ".txt"
SUBSCRIPTION_HEADERS = ("[Adblock Plus]", "[AdGuard]")


def validate(source):
    policy = source.get("unsupported_policy", "error")
    if policy not in ("error", "report"):
        raise ValueError("unsupported_policy must be error or report")
    limit = source.get("max_skipped_rules", 0)
    if type(limit) is not int or limit < 0 or (policy == "report" and limit == 0):
        raise ValueError("max_skipped_rules must be a positive integer for report policy")
    if policy == "error" and limit:
        raise ValueError("max_skipped_rules requires report policy")
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
                # Embedded source lists can repeat fields such as Title.
                # Keep the subscription's own metadata from the file header.
                metadata.setdefault(key.strip().lower(), value.strip())
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


def apply_badfilter(normalized):
    """Resolve DNS badfilter directives before invoking the native converter."""
    lines = normalized.splitlines()
    directives = set()
    targets = set()
    for line in lines:
        if line.startswith(("!", "#")):
            continue
        pattern, separator, modifiers = line.rpartition("$")
        options = modifiers.split(",") if separator else []
        if "badfilter" not in options:
            continue
        remaining = [option for option in options if option != "badfilter"]
        # Broader browser syntax can partially disable rules. Only implement
        # whole-rule cancellation in the DNS syntax we can preserve exactly.
        if any(option != "important" for option in remaining) or any(c.isspace() for c in pattern):
            raise ValueError(f"Unsupported badfilter syntax: {line}")
        targets.add(pattern + ("$" + ",".join(remaining) if remaining else ""))
        directives.add(line)
    disabled = [line for line in lines if line in targets]
    badfilters = [line for line in lines if line in directives]
    filtered = [line for line in lines if line not in targets and line not in directives]
    return "\n".join(filtered) + "\n", badfilters, disabled


def convert(raw, output, compiler, source):
    normalized, count, metadata = inspect_list(raw.read_text(encoding="utf-8-sig"), source)
    normalized, badfilters, disabled = apply_badfilter(normalized)
    effective_count = count - len(badfilters) - len(disabled)
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
    skipped = re.findall(r"^.*?ignored unsupported (.+)$", result.stdout, re.MULTILINE)
    # The pinned converter emits counts only when it skips rules. Fully
    # supported inputs succeed silently; any skip without counts must fail.
    compiled_count = int(counts[1]) if counts else effective_count
    if ((counts and int(counts[2]) != effective_count)
            or compiled_count + len(skipped) != effective_count
            or ("ignored unsupported" in result.stdout and not counts)):
        raise ValueError(f"Cannot account for every converted rule:\n{result.stdout}")
    if skipped and source.get("unsupported_policy", "error") == "error":
        raise ValueError(f"AdGuard conversion skipped unsupported rules:\n{result.stdout}")
    if len(skipped) > source.get("max_skipped_rules", 0):
        raise ValueError(f"Skipped {len(skipped)} rules; exceeds max_skipped_rules")
    if compiled_count < source.get("min_rules", 1):
        raise ValueError("Too few compiled rules after badfilter and unsupported-rule handling")
    if skipped:
        print(f"{source['name']}: WARNING: {len(skipped)} unsupported rules; "
              "details recorded in metadata.json", flush=True)
    return {
        "rule_count": count, "upstream": metadata,
        "conversion": {
            "compiled_rule_count": compiled_count,
            "badfilter_rules": badfilters, "disabled_rules": disabled,
            "skipped_rule_count": len(skipped), "skipped_rules": skipped,
        },
    }

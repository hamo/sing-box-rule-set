"""Compile sing-box source-format JSON with the official compiler."""

import json
import re
import subprocess

EXTENSION = ".json"
JSON_TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|//[^\r\n]*|/\*.*?\*/', re.DOTALL)


def load_config(text):
    """Read JSON with comments without changing strings, URLs or line numbers."""
    def remove_comment(match):
        token = match.group()
        if token.startswith('"'):
            return token
        return re.sub(r"[^\r\n]", " ", token)

    return json.loads(JSON_TOKENS.sub(remove_comment, text))


def rule_counts(rules):
    """Count JSON objects and matcher values before compiler optimization."""
    def values_count(value):
        if isinstance(value, dict):
            return sum(values_count(items) for items in value.values())
        if isinstance(value, list):
            return len(value)
        if isinstance(value, bool):
            return int(value)
        return int(value is not None and value != "")

    objects, entries = len(rules), 0
    for rule in rules:
        children, child_entries = rule_counts(rule.get("rules", []))
        objects += children
        entries += child_entries + sum(
            values_count(value) for key, value in rule.items()
            if key not in {"type", "mode", "rules", "invert"}
        )
    return objects, entries


def validate(source):
    if source.get("validation"):
        raise ValueError("sing-box JSON does not support AdGuard header validation")


def convert(raw, output, compiler, source):
    config = load_config(raw.read_text(encoding="utf-8"))
    if (not isinstance(config, dict) or type(config.get("version")) is not int
            or not isinstance(config.get("rules"), list)):
        raise ValueError("sing-box source must contain integer version and rules array")
    count = len(config["rules"])
    minimum = source.get("min_rules", 1)
    if count < minimum:
        raise ValueError(f"Only {count} rules; minimum {minimum}")
    subprocess.run([
        compiler, "rule-set", "compile", "--output", str(output), str(raw),
    ], check=True)
    objects, entries = rule_counts(config["rules"])
    return {
        "rule_count": count, "rule_object_count": objects, "match_entry_count": entries,
        "upstream": {"version": config["version"]},
    }

"""Compile sing-box source-format JSON with the official compiler."""

import json
import subprocess

EXTENSION = ".json"


def validate(source):
    if source.get("validation"):
        raise ValueError("sing-box JSON does not support AdGuard header validation")


def convert(raw, output, compiler, source):
    config = json.loads(raw.read_text(encoding="utf-8"))
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
    return {"rule_count": count, "upstream": {"version": config["version"]}}

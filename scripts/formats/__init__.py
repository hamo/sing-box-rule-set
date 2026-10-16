"""Format-based conversion tools, independent of upstream identity."""

from . import adguard, sing_box

CONVERTERS = {"adguard": adguard, "sing-box": sing_box}


def get_converter(format_name):
    if not isinstance(format_name, str) or format_name not in CONVERTERS:
        raise ValueError(f"Unsupported source format: {format_name}")
    return CONVERTERS[format_name]

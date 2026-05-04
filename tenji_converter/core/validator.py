from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import re

WAIT_RE = re.compile(r"^\s*\d+(?:\.\d+)?\s*(ms|us|ns|s)\s*$", re.IGNORECASE)
HEX_RE = re.compile(r"^0x[0-9a-fA-F]+$")


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


REQUIRED_TOP_LEVEL = {"action", "items"}
ALLOWED_ACTIONS = {"generate", "append"}


def _is_wait_command(command: dict[str, Any]) -> bool:
    return str(command.get("cmd", "")).lower() == "wait"


def _is_hex_command(command: dict[str, Any]) -> bool:
    return str(command.get("cmd", "")).lower() in {"write", "read", "mask_write"}


def validate_spec(spec: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    missing = [k for k in REQUIRED_TOP_LEVEL if k not in spec]
    if missing:
        errors.append(f"Missing required top-level keys: {', '.join(missing)}")
        return ValidationResult(ok=False, errors=errors, warnings=warnings)

    action = spec.get("action")
    if action not in ALLOWED_ACTIONS:
        errors.append(f"action must be one of {sorted(ALLOWED_ACTIONS)}, got: {action}")

    items = spec.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
        return ValidationResult(ok=False, errors=errors, warnings=warnings)

    seen_symbols: set[str] = set()

    for idx, item in enumerate(items, start=1):
        symbol = str(item.get("symbol", "")).strip()
        if not symbol:
            errors.append(f"items[{idx}] missing symbol")
        elif symbol in seen_symbols:
            errors.append(f"items[{idx}] duplicated symbol: {symbol}")
        else:
            seen_symbols.add(symbol)

        commands = item.get("commands", [])
        if not isinstance(commands, list):
            errors.append(f"items[{idx}].commands must be list")
            continue

        for cidx, command in enumerate(commands, start=1):
            if not isinstance(command, dict):
                errors.append(f"items[{idx}].commands[{cidx}] must be object")
                continue

            if _is_wait_command(command):
                value = str(command.get("value", "")).strip()
                if not WAIT_RE.match(value):
                    errors.append(
                        f"items[{idx}].commands[{cidx}] Wait value format invalid: {value}"
                    )

            if _is_hex_command(command):
                value = str(command.get("value", "")).strip()
                if value and not HEX_RE.match(value):
                    errors.append(
                        f"items[{idx}].commands[{cidx}] hex value invalid: {value}"
                    )

            if str(command.get("cmd", "")).upper().endswith("_TMU") and not symbol.endswith("_TMU"):
                warnings.append(
                    f"items[{idx}] uses TMU command but symbol does not end with _TMU: {symbol}"
                )

    return ValidationResult(ok=not errors, errors=errors, warnings=warnings)

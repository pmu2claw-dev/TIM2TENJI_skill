from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import re

from .memory_rules import apply_memory_rules
from .normalizer import normalize_spec

WAIT_RE = re.compile(r"^\s*\d+(?:\.\d+)?\s*(ms|us|ns|s)\s*$", re.IGNORECASE)
HEX_RE = re.compile(r"^0x[0-9a-fA-F]+$")


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    memory_warnings: list[str] = field(default_factory=list)
    memory_rules_applied: list[dict[str, Any]] = field(default_factory=list)
    memory_context_preview: str = ""


ALLOWED_ACTIONS = {"generate", "append"}


def _is_wait_command(command: dict[str, Any]) -> bool:
    return str(command.get("cmd", "")).lower() == "wait"


def _is_hex_command(command: dict[str, Any]) -> bool:
    return str(command.get("cmd", "")).lower() in {"write", "read", "mask_write"}


def validate_spec(spec: dict[str, Any], memory_root: Path | None = None) -> ValidationResult:
    normalized = normalize_spec(spec)
    errors: list[str] = []
    warnings: list[str] = []

    action = normalized.get("action")
    if action not in ALLOWED_ACTIONS:
        errors.append(f"action must be one of {sorted(ALLOWED_ACTIONS)}, got: {action}")

    items = normalized.get("test_items")
    if not isinstance(items, list) or not items:
        errors.append("test_items must be a non-empty list")
        return ValidationResult(ok=False, errors=errors, warnings=warnings)

    seen_symbols: set[str] = set()
    for idx, item in enumerate(items, start=1):
        symbol = str(item.get("symbol", "")).strip()
        if not symbol:
            errors.append(f"test_items[{idx}] missing symbol")
        elif symbol in seen_symbols:
            errors.append(f"test_items[{idx}] duplicated symbol: {symbol}")
        else:
            seen_symbols.add(symbol)

        commands = item.get("commands", [])
        if not isinstance(commands, list):
            errors.append(f"test_items[{idx}].commands must be list")
            continue

        for cidx, command in enumerate(commands, start=1):
            if not isinstance(command, dict):
                errors.append(f"test_items[{idx}].commands[{cidx}] must be object")
                continue

            value = str(command.get("params") or command.get("value") or "").strip()
            if _is_wait_command(command) and not WAIT_RE.match(value):
                errors.append(f"test_items[{idx}].commands[{cidx}] Wait value format invalid: {value}")

            if _is_hex_command(command) and value and not HEX_RE.match(value):
                errors.append(f"test_items[{idx}].commands[{cidx}] hex value invalid: {value}")

            if str(command.get("cmd", "")).upper().endswith("_TMU") and not symbol.endswith("_TMU"):
                warnings.append(
                    f"test_items[{idx}] uses TMU command but symbol does not end with _TMU: {symbol}"
                )

    memory_result = apply_memory_rules(normalized, memory_root=memory_root)
    errors.extend(memory_result.get("errors", []))
    warnings.extend(memory_result.get("warnings", []))

    return ValidationResult(
        ok=not errors,
        errors=errors,
        warnings=warnings,
        memory_warnings=memory_result.get("memory_warnings", []),
        memory_rules_applied=memory_result.get("memory_rules_applied", []),
        memory_context_preview=str(memory_result.get("memory_context_preview", "")),
    )

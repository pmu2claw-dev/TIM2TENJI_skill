from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .excel_writer import write_spec_to_excel
from .gates import evaluate_gates
from .normalizer import normalize_spec
from .repair import repair_spec
from .validator import validate_spec
from .visual_verify import verify_visual_integrity


@dataclass
class CompileResult:
    ok: bool
    output_excel: str | None
    normalized_spec_json: str
    summary_json: str


def load_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_user_request_as_spec(request: str) -> dict[str, Any]:
    try:
        payload = json.loads(request)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass

    return {
        "action": "generate",
        "_parser_meta": {"fallback_used": True},
        "items": [
            {
                "category": "NL Request",
                "scenario": "from free text",
                "symbol": "AUTO_SYMBOL",
                "commands": [{"cmd": "NOTE", "value": request}],
                "judge": "INFO",
                "comment": "Generated from natural language fallback",
            }
        ],
    }


def _merge_parser_meta(target: dict[str, Any], source: dict[str, Any]) -> None:
    src = source.get("_parser_meta", {}) if isinstance(source.get("_parser_meta"), dict) else {}
    dst = target.get("_parser_meta", {}) if isinstance(target.get("_parser_meta"), dict) else {}
    merged = dict(dst)
    merged.update(src)
    target["_parser_meta"] = merged


def compile_tenji(
    request: str | None,
    request_file: Path | None,
    spec_file: Path | None,
    output: Path,
    existing_excel: Path | None,
    template: Path | None,
    verify_visual: bool,
    memory_root: Path | None = None,
    auto_repair: bool = False,
    gate_strict: bool = False,
) -> CompileResult:
    if spec_file:
        raw_spec = load_json_file(spec_file)
    elif request_file:
        raw_spec = parse_user_request_as_spec(request_file.read_text(encoding="utf-8"))
    elif request:
        raw_spec = parse_user_request_as_spec(request)
    else:
        raise ValueError("One of --spec / --request-file / --request is required")

    normalized_spec = normalize_spec(
        raw_spec,
        existing_excel=str(existing_excel) if existing_excel else None,
    )
    validation = validate_spec(normalized_spec, memory_root=memory_root)

    parser_meta = normalized_spec.get("_parser_meta", {}) if isinstance(normalized_spec.get("_parser_meta"), dict) else {}
    parser_meta["memory_context_preview"] = validation.memory_context_preview
    parser_meta["memory_rules_applied"] = validation.memory_rules_applied
    parser_meta["memory_warnings"] = validation.memory_warnings
    normalized_spec["_parser_meta"] = parser_meta

    repaired_used = False
    if auto_repair and validation.errors:
        repaired_spec = repair_spec(normalized_spec)
        repaired_validation = validate_spec(repaired_spec, memory_root=memory_root)
        if len(repaired_validation.errors) < len(validation.errors):
            normalized_spec = repaired_spec
            validation = repaired_validation
            repaired_used = True

    gates = evaluate_gates(
        spec=normalized_spec,
        validation_errors=validation.errors,
        validation_warnings=validation.warnings,
        strict=gate_strict,
    )

    summary: dict[str, Any] = {
        "ok": validation.ok and gates.ok,
        "errors": validation.errors,
        "warnings": validation.warnings,
        "memory_warnings": validation.memory_warnings,
        "memory_context_preview": validation.memory_context_preview,
        "memory_rules_applied": validation.memory_rules_applied,
        "auto_repair": {"enabled": auto_repair, "applied": repaired_used},
        "gates": {
            "ok": gates.ok,
            "hard_failures": gates.hard_failures,
            "soft_warnings": gates.soft_warnings,
            "fidelity_score": gates.fidelity_score,
            "lineage": gates.lineage,
        },
        "visual_verify": None,
        "output": None,
    }

    _merge_parser_meta(normalized_spec, {"_parser_meta": {"lineage": gates.lineage}})
    normalized_spec_json = json.dumps(normalized_spec, ensure_ascii=False, indent=2)

    if not summary["ok"]:
        return CompileResult(
            ok=False,
            output_excel=None,
            normalized_spec_json=normalized_spec_json,
            summary_json=json.dumps(summary, ensure_ascii=False, indent=2),
        )

    output_excel = write_spec_to_excel(
        normalized_spec,
        output_path=output,
        template=template,
        existing_excel=existing_excel,
    )
    summary["output"] = str(output_excel)

    if verify_visual:
        visual_ok, visual_msg = verify_visual_integrity(output_excel, output.parent)
        summary["visual_verify"] = {"ok": visual_ok, "message": visual_msg}

    return CompileResult(
        ok=True,
        output_excel=str(output_excel),
        normalized_spec_json=normalized_spec_json,
        summary_json=json.dumps(summary, ensure_ascii=False, indent=2),
    )

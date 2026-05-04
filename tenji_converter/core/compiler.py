from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .excel_writer import write_spec_to_excel
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
    # MVP: expect request is already JSON string of spec; fallback to single-item template
    try:
        payload = json.loads(request)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass

    return {
        "action": "generate",
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


def compile_tenji(
    request: str | None,
    request_file: Path | None,
    spec_file: Path | None,
    output: Path,
    existing_excel: Path | None,
    template: Path | None,
    verify_visual: bool,
) -> CompileResult:
    if spec_file:
        raw_spec = load_json_file(spec_file)
    elif request_file:
        raw_spec = parse_user_request_as_spec(request_file.read_text(encoding="utf-8"))
    elif request:
        raw_spec = parse_user_request_as_spec(request)
    else:
        raise ValueError("One of --spec / --request-file / --request is required")

    validation = validate_spec(raw_spec)
    summary: dict[str, Any] = {
        "ok": validation.ok,
        "errors": validation.errors,
        "warnings": validation.warnings,
        "visual_verify": None,
        "output": None,
    }

    normalized_spec_json = json.dumps(raw_spec, ensure_ascii=False, indent=2)

    if not validation.ok:
        return CompileResult(
            ok=False,
            output_excel=None,
            normalized_spec_json=normalized_spec_json,
            summary_json=json.dumps(summary, ensure_ascii=False, indent=2),
        )

    output_excel = write_spec_to_excel(
        raw_spec,
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

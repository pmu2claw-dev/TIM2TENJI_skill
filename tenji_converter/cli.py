from __future__ import annotations

import argparse
from pathlib import Path

from tenji_converter.core.compiler import compile_tenji


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tenji-convert",
        description="TIM2TENJI skill package: convert request/spec into TENJI Excel",
    )
    parser.add_argument("--request", type=str, help="Natural language request or JSON string")
    parser.add_argument("--request-file", type=Path, help="Path to request text file")
    parser.add_argument("--spec", type=Path, help="Path to normalized spec JSON")
    parser.add_argument("--output", type=Path, required=True, help="Output .xlsx/.xlsm path")
    parser.add_argument("--existing-excel", type=Path, help="Existing workbook path for append mode")
    parser.add_argument("--template", type=Path, help="Template workbook path")
    parser.add_argument("--normalized-spec-output", type=Path, default=Path("normalized_spec.json"))
    parser.add_argument("--summary-output", type=Path, default=Path("summary.json"))
    parser.add_argument("--verify-visual", action="store_true", help="Run LibreOffice-based PDF verification")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = compile_tenji(
        request=args.request,
        request_file=args.request_file,
        spec_file=args.spec,
        output=args.output,
        existing_excel=args.existing_excel,
        template=args.template,
        verify_visual=args.verify_visual,
    )

    args.normalized_spec_output.write_text(result.normalized_spec_json, encoding="utf-8")
    args.summary_output.write_text(result.summary_json, encoding="utf-8")

    if result.ok:
        print(f"[OK] TENJI compile finished: {result.output_excel}")
        print(f"[INFO] normalized spec: {args.normalized_spec_output}")
        print(f"[INFO] summary: {args.summary_output}")
        return 0

    print("[ERROR] TENJI compile failed, see summary output")
    print(f"[INFO] summary: {args.summary_output}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

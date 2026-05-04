# TIM2TENJI_skill

將 OpenClaw 的 TENJI Excel 產線能力（spec 驗證 + workbook 輸出）與 Hermes 的知識化治理概念（rule/gate/lineage）包裝成可在其他電腦安裝執行的工具套件。

## 目標

- 讓其他使用者可透過 **自然語言或 spec JSON** 產生/追加 TENJI Excel。
- 提供可版本化、可追蹤的輸出流程（normalized spec + summary）。
- 以 MVP 形式先落地 Core Engine，後續逐步擴充 Hermes hard-gate 與 lineage。

## 目前功能（v0.1.0）

- CLI 指令：`tenji-convert`
- 支援輸入：
  - `--spec`：標準化 spec JSON
  - `--request` / `--request-file`：自然語言（MVP fallback）
- 支援輸出：
  - 產生新 Excel (`action=generate`)
  - 追加既有 Excel (`action=append` + `--existing-excel`)
- 驗證：
  - action/items 結構檢查
  - symbol 唯一性
  - Wait 時間格式（ms/us/ns/s）
  - hex 值格式（0x...）
  - TMU 命令命名警示
- 可選視覺驗證：`--verify-visual`（需 LibreOffice/soffice）

## 安裝

```bash
cd TIM2TENJI_skill
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## 快速使用

```bash
tenji-convert \
  --spec examples/spec.sample.json \
  --output output/TENJI_output.xlsm \
  --normalized-spec-output output/normalized_spec.json \
  --summary-output output/summary.json
```

詳見：
- `docs/USAGE.md`
- `docs/PACKAGING.md`
- `CHANGELOG.md`

## 專案結構

```text
TIM2TENJI_skill/
  tenji_converter/
    cli.py
    core/
      compiler.py
      validator.py
      excel_writer.py
      visual_verify.py
  docs/
    PACKAGING.md
    USAGE.md
  pyproject.toml
  CHANGELOG.md
```

## 路線圖（摘要）

- v0.2：導入 OpenClaw 原生 normalize/validator 模組化接軌。
- v0.3：加入 Hermes lineage / golden gate / fail->repair 工作流。
- v0.4：提供 API server + Docker runtime。

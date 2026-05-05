# TIM2TENJI_skill

將 OpenClaw 的 TENJI Excel 產線能力（spec 驗證 + workbook 輸出）與 Hermes 的知識化治理概念（rule/gate/lineage）包裝成可在其他電腦安裝執行的工具套件。

## 目標

- 讓其他使用者可透過 **自然語言或 spec JSON** 產生/追加 TENJI Excel。
- 提供可版本化、可追蹤的輸出流程（normalized spec + summary）。
- 導入 OpenClaw 對齊的 normalize / memory rules，並加入 Hermes gate 與 fail->repair 工作流。

## 目前功能（v0.2.0）

- CLI 指令：`tenji-convert`
- 支援輸入：
  - `--spec`：標準化 spec JSON
  - `--request` / `--request-file`：自然語言（MVP fallback）
- 記憶體/修復/閘門參數：
  - `--memory-root`：指定 durable memory 規則來源根目錄
  - `--auto-repair`：驗證失敗時啟用自動修補再重驗
  - `--gate-strict`：Hermes 嚴格模式（warning 視為 failure）
- 支援輸出：
  - 產生新 Excel (`action=generate`)
  - 追加既有 Excel (`action=append` + `--existing-excel`)
- 規格正規化與驗證：
  - normalize（兼容 `items` / `test_items`）
  - action/items 結構檢查
  - symbol 唯一性
  - Wait 時間格式（ms/us/ns/s）
  - hex 值格式（0x...）
  - TMU 命令命名警示
- Memory rules（OpenClaw 對齊）：
  - protocol trigger/judge 組合檢查
  - OS 空格式、UR mapping、QC/HVDCP 與 BC1.2 等規則
- Hermes gate：
  - hard failures / soft warnings
  - fidelity score
  - lineage 摘要
- Fail -> Repair：
  - wait 單位補齊、hex 正規化、常見 attach/ForceV 線索修補
- 可選視覺驗證：`--verify-visual`（需 LibreOffice/soffice）

## 安裝

```bash
cd TIM2TENJI_skill
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

> 發佈狀態註記（2026-05-05）：目前已確認 **source install ready**（可 `pip install -e .`），但 **wheel/sdist artifact 尚未進行正式 build 驗證**（刻意略過以避免流程卡住）。

## 快速使用

```bash
tenji-convert \
  --spec examples/spec.sample.json \
  --output output/TENJI_output.xlsm \
  --memory-root ./memory \
  --auto-repair \
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
      normalizer.py
      memory_loader.py
      memory_rules.py
      repair.py
      gates.py
      excel_writer.py
      visual_verify.py
  docs/
    PACKAGING.md
    USAGE.md
  pyproject.toml
  CHANGELOG.md
```

## 路線圖（摘要）

- v0.3：擴充更完整 Hermes lineage / golden gate 策略。
- v0.4：提供 API server + Docker runtime。

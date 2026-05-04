# 使用說明

## 1) CLI 指令

```bash
tenji-convert [options]
```

## 2) 主要參數

- `--request <text>`：自然語言或 JSON 字串
- `--request-file <path>`：自然語言文字檔
- `--spec <path>`：spec JSON（建議正式使用）
- `--output <path>`：輸出 Excel 路徑（必要）
- `--existing-excel <path>`：append 模式要追加的既有 Excel
- `--template <path>`：模板路徑（可選）
- `--memory-root <path>`：durable memory 根目錄（可選）
- `--auto-repair`：驗證錯誤時嘗試自動修補後再驗證
- `--gate-strict`：啟用嚴格 gate（warnings 視為失敗）
- `--normalized-spec-output <path>`：normalized spec 輸出，預設 `normalized_spec.json`
- `--summary-output <path>`：summary 輸出，預設 `summary.json`
- `--verify-visual`：啟用 LibreOffice PDF 驗證

## 3) 範例：用 spec 生成新檔

```bash
tenji-convert \
  --spec spec.sample.json \
  --output output/TENJI_new.xlsm \
  --memory-root ./memory \
  --auto-repair \
  --normalized-spec-output output/normalized_spec.json \
  --summary-output output/summary.json
```

## 4) 範例：append 到既有檔

```bash
tenji-convert \
  --spec spec.append.json \
  --output output/ignored_for_append.xlsm \
  --existing-excel existing/TENJI_master.xlsm \
  --gate-strict \
  --summary-output output/append_summary.json
```

> 註：append 時會直接儲存回 `--existing-excel` 路徑。

## 5) spec JSON 最小格式

```json
{
  "action": "generate",
  "items": [
    {
      "category": "PMIC",
      "scenario": "Enable sequence",
      "symbol": "BUCK1_EN",
      "commands": [
        { "cmd": "WRITE", "value": "0x1A" },
        { "cmd": "WAIT", "value": "5ms" }
      ],
      "expected": "Pass",
      "judge": "PASS"
    }
  ]
}
```

## 6) 輸出檔說明

- Excel：TENJI 結果檔
- `normalized_spec.json`：實際使用的規格內容（含 normalize 結果與 lineage meta）
- `summary.json`：執行摘要（errors/warnings/memory/gates/fidelity/output/visual verify）

## 7) 常見問題

### Q1: `--verify-visual` 失敗？
A: 檢查系統是否安裝 LibreOffice，且 `soffice` 在 PATH 中。

### Q2: 自然語言轉換準確率如何？
A: 目前仍建議正式流程使用 `--spec`；自然語言路徑為 fallback，會持續迭代。

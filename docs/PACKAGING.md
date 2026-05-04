# Packaging 說明

## 1) 打包定位

`TIM2TENJI_skill` 是一個可安裝的 Python package，目標是在他人電腦上重現「TENJI Excel 轉換」流程。

- **Core Engine（已實作 MVP）**
  - request/spec ingestion
  - spec validator
  - excel writer（含 append）
  - visual verify（LibreOffice PDF）
- **Knowledge/Gate（目前為骨架）**
  - 規則檔與驗證點可持續擴充
  - 後續可接 Hermes lineage/golden answer gate

## 2) 打包內容

- `pyproject.toml`：套件建置與依賴設定
- `tenji_converter/cli.py`：命令列介面 (`tenji-convert`)
- `tenji_converter/core/compiler.py`：轉換協調器（parse/validate/write/verify）
- `tenji_converter/core/validator.py`：規則驗證器
- `tenji_converter/core/excel_writer.py`：Excel 生成/追加
- `tenji_converter/core/visual_verify.py`：PDF 視覺檢查
- `README.md`：專案簡介
- `docs/USAGE.md`：詳細使用說明
- `CHANGELOG.md`：版本紀錄

## 3) 安裝型態

### 本地開發安裝

```bash
pip install -e .
```

### Wheel 發佈（可選）

```bash
python -m pip install build
python -m build
# 產出 dist/*.whl
```

## 4) 跨機部署建議

- 目標機需 Python 3.10+
- 若要啟用 `--verify-visual`：安裝 LibreOffice 並確保 `soffice` 可用
- 建議用 virtualenv/venv 隔離依賴

## 5) 品質閘（MVP）

- 結構合法性（top-level keys、action、items）
- command-level 檢查（wait/hex/tmu）
- 輸出 sidecar artifacts：
  - normalized spec JSON
  - summary JSON（errors/warnings/output/visual status）

## 6) 後續擴充方向

1. 接軌 OpenClaw 現有 normalize/validate 邏輯
2. 導入 Hermes skill memory rules 作 hard gate
3. 新增 lineage 紀錄（request -> spec -> workbook hash）
4. 加入 fail->repair 重試策略與 golden workbook 比對

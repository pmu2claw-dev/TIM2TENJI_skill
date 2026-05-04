# Packaging 說明

## 1) 打包定位

`TIM2TENJI_skill` 是一個可安裝的 Python package，目標是在他人電腦上重現「TENJI Excel 轉換」流程。

- **Core Engine（已實作）**
  - request/spec ingestion
  - normalize + validator + memory rules
  - auto repair（可選）
  - gates（hard/soft + fidelity + lineage）
  - excel writer（含 append）
  - visual verify（LibreOffice PDF，可選）

## 2) 打包內容

- `pyproject.toml`：套件建置與依賴設定
- `tenji_converter/cli.py`：命令列介面 (`tenji-convert`)
- `tenji_converter/core/compiler.py`：轉換協調器
- `tenji_converter/core/normalizer.py`：規格正規化
- `tenji_converter/core/validator.py`：核心驗證
- `tenji_converter/core/memory_loader.py`：memory 載入與相關性選取
- `tenji_converter/core/memory_rules.py`：memory-driven domain 規則
- `tenji_converter/core/repair.py`：自動修補策略
- `tenji_converter/core/gates.py`：Hermes gate/fidelity/lineage
- `tenji_converter/core/excel_writer.py`：Excel 生成/追加
- `tenji_converter/core/visual_verify.py`：PDF 視覺檢查
- `README.md`、`docs/USAGE.md`、`CHANGELOG.md`

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

## 5) 品質閘（v0.2）

- normalize（`items`/`test_items` 對齊）
- 結構合法性（action/symbol/commands）
- command-level 檢查（wait/hex/tmu）
- memory rules（protocol/OS/UR/QC-HVDCP 等）
- gates（hard failures + soft warnings + fidelity score + lineage）
- 輸出 sidecar artifacts：
  - normalized spec JSON
  - summary JSON

## 6) 後續擴充方向

1. 導入更完整 Hermes golden answer gate
2. 強化 lineage（request -> spec -> workbook hash）
3. 擴充 fail->repair 策略與規則覆蓋率
4. 提供 API server + Docker runtime

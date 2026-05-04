# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-05-04

### Added
- 初始化 `TIM2TENJI_skill` 專案與 Python package 結構
- 新增 CLI：`tenji-convert`
- 新增 Core 模組：
  - `compiler.py`：整合 parse/validate/write/verify 工作流
  - `validator.py`：MVP 規則驗證（action/items/wait/hex/tmu）
  - `excel_writer.py`：TENJI Test_Note/Revision 寫入與 append 支援
  - `visual_verify.py`：LibreOffice PDF 驗證
- 新增文件：
  - `README.md`
  - `docs/PACKAGING.md`
  - `docs/USAGE.md`
  - `CHANGELOG.md`

### Notes
- v0.1.0 聚焦可安裝、可執行、可追蹤的 MVP。
- Hermes lineage/golden hard gate 將於後續版本逐步導入。

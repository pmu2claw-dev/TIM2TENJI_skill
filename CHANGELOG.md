# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-05-04

### Added
- 新增 OpenClaw 對齊模組：
  - `normalizer.py`
  - `memory_loader.py`
  - `memory_rules.py`
  - `repair.py`
- 新增 Hermes gate 模組：
  - `gates.py`（hard/soft gate、fidelity score、lineage）
- CLI 新增參數：
  - `--memory-root`
  - `--auto-repair`
  - `--gate-strict`

### Changed
- `compiler.py` 升級流程：
  - normalize -> validate(+memory) -> auto-repair(可選) -> gates -> excel -> visual verify
- `validator.py` 升級為整合 normalize 與 memory rules 的驗證入口
- `summary.json` 擴充：memory context、memory rules、gates、fidelity、lineage
- 文件更新：README / USAGE / PACKAGING
- 發佈狀態：source install ready；wheel/sdist artifact build 驗證暫未執行（避免驗證流程阻塞）

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

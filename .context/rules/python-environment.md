# Python Environment Standards

> UV-only Python environment. NEVER use system Python.

<!-- L2-REINJECT: rank=3, content="UV ONLY. Use uv run for all Python. NEVER use python/pip/pip3 directly. Use uv add for deps." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | UV-only constraints H-05, H-06 |
| [Command Reference](#command-reference) | Correct UV commands |
| [Large File Handling](#large-file-handling) | Transcript file size limits |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-05 | MUST use `uv run` for all Python execution. NEVER use `python`, `pip`, or `pip3` directly. | Command fails. Environment corruption. |
| H-06 | MUST use `uv add` for dependency management. NEVER use `pip install`. | Build breaks. |

---

## Command Reference

| Task | Correct | FORBIDDEN |
|------|---------|-----------|
| Run CLI | `uv run jerry <cmd>` | `python -m src...` |
| Run tests | `uv run pytest tests/` | `pytest tests/` |
| Run script | `uv run python script.py` | `python script.py` |
| Add dep | `uv add <package>` | `pip install <package>` |
| Add dev dep | `uv add --dev <package>` | `pip3 install <package>` |
| Sync deps | `uv sync` | -- |

---

## Large File Handling

| File | Action | Reason |
|------|--------|--------|
| `index.json` (~8KB) | Read | Metadata, speaker list, chunk refs |
| `chunks/chunk-*.json` (~130KB) | Read | Transcript data in manageable pieces |
| `extraction-report.json` (~35KB) | Read | Entity extraction results |
| `canonical-transcript.json` (~930KB) | **NEVER read** | Too large for context window |

# Python Environment Standards

> **CRITICAL:** This project uses UV for Python dependency management.
> **NEVER** use system-managed Python (python, python3, pip, pip3).

---

## UV Usage (MANDATORY)

### Running the Jerry CLI

```bash
# CORRECT - Use the jerry CLI entry point
uv run jerry transcript parse <file.vtt> --output-dir <dir>
uv run jerry session start
uv run jerry items list

# WRONG - Don't use verbose module paths
uv run python -m src.interface.cli.main <args>  # ❌ VERBOSE, use jerry instead
```

### Running Other Python Commands

```bash
# CORRECT - Always use UV
uv run pytest tests/
uv run python script.py

# WRONG - NEVER use system Python
python script.py                            # ❌ FORBIDDEN
python3 script.py                           # ❌ FORBIDDEN
pip install package                         # ❌ FORBIDDEN
pip3 install package                        # ❌ FORBIDDEN
```

### Adding Dependencies

```bash
# CORRECT - Use UV to add dependencies
uv add package-name
uv add --dev pytest mypy ruff

# WRONG - Never use pip directly
pip install package-name                    # ❌ FORBIDDEN
pip3 install package-name                   # ❌ FORBIDDEN
```

### Running Tests

```bash
# CORRECT
uv run pytest tests/
uv run pytest tests/unit/ -v
uv run pytest --cov=src

# WRONG
pytest tests/                               # ❌ FORBIDDEN
python -m pytest tests/                     # ❌ FORBIDDEN
```

---

## Why UV?

1. **Reproducible environments** - Lock file ensures consistent dependencies
2. **Isolation** - Project dependencies don't pollute system Python
3. **Speed** - UV is significantly faster than pip
4. **No conflicts** - Avoids system Python version mismatches

---

## Common Commands Reference

| Task | Command |
|------|---------|
| Run CLI | `uv run python -m src.interface.cli.main <args>` |
| Run tests | `uv run pytest tests/` |
| Add dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |
| Sync dependencies | `uv sync` |
| Show installed | `uv pip list` |

---

## Large File Handling (Transcript Skill)

### Files Agents Should Read

| File | Size | Use For |
|------|------|---------|
| `index.json` | ~8KB | Metadata, speaker list, chunk references |
| `chunks/chunk-*.json` | ~130KB each | Actual transcript data in manageable pieces |
| `extraction-report.json` | ~35KB | Entity extraction results |

### Files Agents Should NEVER Read

| File | Size | Why Forbidden |
|------|------|---------------|
| `canonical-transcript.json` | ~930KB | **TOO LARGE** - will overwhelm context window |

**The canonical-transcript.json is for:**
- Reference/archive purposes
- Programmatic access by Python code
- NOT for LLM agent consumption

**Agents work from chunks because:**
- Each chunk is < 150KB (fits in context)
- Chunking was specifically designed to solve this problem (DISC-009)
- Python parser creates chunks; agents consume chunks

---

## Enforcement

This rule is **HARD** - violations will break the build and cause environment issues.

If you catch yourself typing `python`, `python3`, `pip`, or `pip3` - STOP and use `uv run` or `uv add` instead.

---

*Created: 2026-01-30*
*Reason: Repeated violations of UV-managed environment requirement*
*Updated: 2026-01-30 - Added large file handling rules*

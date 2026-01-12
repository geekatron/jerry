# PROJ-004-e-001: JSON5 Python Support Investigation

**PS ID:** PROJ-004
**Entry ID:** e-001
**Type:** Research Artifact
**Date:** 2026-01-12
**Author:** ps-researcher agent (v2.0.0)
**Status:** Complete

---

## L0: Executive Summary (ELI5)

Python has no built-in JSON5 support, but two solid third-party libraries exist: `json5` (pure Python, zero dependencies, slow) and `pyjson5` (Cython-based, fast, requires compilation). For configuration files with comments, Python's built-in `tomllib` (stdlib since 3.11) offers a better alternative with native comment support, datetime types, and zero external dependencies - making TOML the recommended choice for Jerry's configuration needs.

---

## L1: Technical Findings (Software Engineer)

### 1. JSON5 Libraries in Python

#### 1.1 `json5` Package (dpranke/pyjson5)

**PyPI:** [json5](https://pypi.org/project/json5/)
**GitHub:** [dpranke/pyjson5](https://github.com/dpranke/pyjson5)
**Latest Version:** 0.13.0 (2026-01-01)
**License:** Apache Software License

**Characteristics:**
- Pure Python implementation
- Zero runtime dependencies
- Mirrors stdlib `json` API
- Python 3.8 - 3.14 support

**Installation:**
```bash
pip install json5
```

**Usage Example:**
```python
import json5

# Read JSON5 with comments
config = json5.loads("""
{
    // Database configuration
    "host": "localhost",
    "port": 5432,  // PostgreSQL default
    /*
     * Credentials should be overridden
     * by environment variables in production
     */
    "user": "dev_user",
}
""")

# Write JSON5
output = json5.dumps(config, indent=2)
```

**Key Features:**
- Single-line (`//`) and multi-line (`/* */`) comments
- Trailing commas allowed
- Unquoted object keys (if valid identifiers)
- Single-quoted strings
- Multi-line strings
- `allow_duplicate_keys=False` option for strict parsing
- `quote_style` parameter for output control

**Performance Warning:**
> "It can be 1000-6000x slower than the C-optimized JSON module, and is 200x slower (or more) than the pure Python JSON module."

This performance is acceptable for configuration file parsing (done once at startup) but unsuitable for high-throughput data processing.

#### 1.2 `pyjson5` Package (Kijewski/pyjson5)

**PyPI:** [pyjson5](https://pypi.org/project/pyjson5/)
**GitHub:** [Kijewski/pyjson5](https://github.com/Kijewski/pyjson5)
**Latest Version:** 2.0.0 (2025-10-02)
**License:** Apache/MIT Dual License

**Characteristics:**
- Cython-based implementation
- Performance comparable to stdlib `json`
- Requires compilation (pre-built wheels available)
- Python 3.8 - 3.14 support

**Installation:**
```bash
pip install pyjson5
```

**Usage Example:**
```python
import pyjson5

# Preferred API
config = pyjson5.decode("""
{
    // Configuration with comments
    host: "localhost",  // unquoted keys work
    port: 5432,
}
""")

# Also supports load/loads for drop-in replacement
config = pyjson5.loads(json5_string)

# Encoding (produces HTML-safe ASCII output)
output = pyjson5.encode(config)
```

**Key Features:**
- Full JSON5 1.0.0 specification support
- HTML-safe output (escapes `<`, `>`, `&`, `'`)
- `encode_*()` and `decode_*()` preferred over `load(s)`/`dump(s)`
- High performance (comparable to stdlib json)

**Trade-off:**
Requires Cython compilation or pre-built wheel availability.

### 2. Stdlib Support Assessment

#### 2.1 JSON5 in Python Stdlib

**Status:** No stdlib support exists. No PEP has been proposed.

The Python standard library's `json` module only supports strict JSON (RFC 8259). There is no indication of plans to add JSON5 support.

#### 2.2 `tomllib` (Python 3.11+ stdlib)

**Documentation:** [tomllib](https://docs.python.org/3/library/tomllib.html)
**Added:** Python 3.11 via [PEP 680](https://peps.python.org/pep-0680/)

**Characteristics:**
- Read-only TOML 1.0.0 parser
- Zero external dependencies
- Part of Python stdlib
- Pure Python (based on tomli)

**API:**
```python
import tomllib

# Load from file (MUST be binary mode)
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# Load from string
config = tomllib.loads("""
# Database configuration
[database]
host = "localhost"
port = 5432  # PostgreSQL default

# Credentials
[database.auth]
user = "dev_user"
""")
```

**Type Mapping:**

| TOML Type | Python Type |
|-----------|-------------|
| string | `str` |
| integer | `int` |
| float | `float` |
| boolean | `bool` |
| offset date-time | `datetime.datetime` (with tzinfo) |
| local date-time | `datetime.datetime` (tzinfo=None) |
| local date | `datetime.date` |
| local time | `datetime.time` |
| array | `list` |
| table | `dict` |

**Limitations:**
- Read-only (no `dump`/`dumps`)
- For writing, use `tomli-w` or `tomlkit`
- Does not preserve comments in parsed output

### 3. Read/Write Capabilities Comparison

| Library | Read | Write | Preserve Comments | Performance |
|---------|------|-------|-------------------|-------------|
| `json5` | Yes | Yes | No | Very Slow |
| `pyjson5` | Yes | Yes | No | Fast |
| `tomllib` | Yes | **No** | No | Medium |
| `tomli-w` | No | Yes | No | Medium |
| `tomlkit` | Yes | Yes | **Yes** | Slow |

### 4. Zero-Dependency Pure Python Options

| Library | Pure Python | Zero Deps | Stdlib |
|---------|-------------|-----------|--------|
| `json5` | Yes | Yes | No |
| `pyjson5` | No (Cython) | No | No |
| `tomllib` | Yes | Yes | **Yes** (3.11+) |
| `tomli` | Yes | Yes | No (backport) |

**Winner for Zero-Dependency:** `tomllib` (stdlib) or `json5` (if JSON5 format required)

### 5. Code Examples

#### 5.1 JSON5 Configuration Pattern
```python
# config.json5
"""
{
    // Jerry Framework Configuration
    "version": "1.0.0",

    // Project settings
    "project": {
        "default_dir": "projects",
        "auto_create": true,
    },

    // Logging configuration
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    },
}
"""

import json5

def load_config(path: str) -> dict:
    with open(path) as f:
        return json5.load(f)
```

#### 5.2 TOML Configuration Pattern
```python
# config.toml
"""
# Jerry Framework Configuration
version = "1.0.0"

# Project settings
[project]
default_dir = "projects"
auto_create = true

# Logging configuration
[logging]
level = "INFO"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
"""

import tomllib

def load_config(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)
```

---

## L2: Strategic Recommendation (Principal Architect)

### Decision Framework

| Criterion | JSON5 | TOML | Weight |
|-----------|-------|------|--------|
| Stdlib support | No | Yes (3.11+) | High |
| Zero dependencies | Yes (`json5`) | Yes (`tomllib`) | High |
| Python ecosystem adoption | Low | High | Medium |
| Write support | Yes | Requires `tomli-w` | Medium |
| Date/time native types | No | Yes | Low |
| Familiar syntax | Yes (JSON-like) | No (INI-like) | Low |
| Performance | Poor | Good | Low |

### Recommendation for Jerry

**Primary Choice: TOML with `tomllib`**

**Rationale:**

1. **Zero External Dependencies (P-002 Compliance)**
   - `tomllib` is in Python stdlib since 3.11
   - Jerry already requires Python 3.11+
   - No additional packages needed for reading config

2. **Python Ecosystem Alignment**
   - `pyproject.toml` is the standard for Python projects
   - Familiar to Python developers
   - Used by Poetry, PDM, setuptools

3. **Configuration-First Design**
   - TOML was designed specifically for configuration
   - Native date/time support useful for scheduling/expiration
   - Section headers (`[section]`) provide clear organization

4. **Comment Support**
   - Full `#` comment support in source files
   - Comments ignored during parsing (expected behavior)

**For Write Requirements:**

If Jerry needs to write configuration files:
```python
# Option 1: tomli-w (simple, no comment preservation)
pip install tomli-w

# Option 2: tomlkit (comment preservation, slower)
pip install tomlkit
```

### When to Use JSON5 Instead

Consider `json5` only if:
1. Configuration must be valid JavaScript (e.g., shared with Node.js tools)
2. Existing JSON configs need comment support without migration
3. Nested structures are deeply complex (TOML tables can be verbose)

### Migration Path

If Jerry has existing JSON config files:

```python
# Temporary: Read JSON5 during migration
import json5

def load_legacy_config(path: str) -> dict:
    """Load legacy JSON5 config (deprecated)."""
    with open(path) as f:
        return json5.load(f)

# Target: TOML for new configs
import tomllib

def load_config(path: str) -> dict:
    """Load TOML configuration."""
    with open(path, "rb") as f:
        return tomllib.load(f)
```

### Final Verdict

| Aspect | Recommendation |
|--------|----------------|
| **Format** | TOML |
| **Read Library** | `tomllib` (stdlib) |
| **Write Library** | `tomli-w` (if needed) |
| **Fallback** | `json5` for legacy JSON migration |

---

## Sources

### Primary Documentation
- [json5 PyPI](https://pypi.org/project/json5/)
- [pyjson5 PyPI](https://pypi.org/project/pyjson5/)
- [Python tomllib Documentation](https://docs.python.org/3/library/tomllib.html)
- [PEP 680 - tomllib](https://peps.python.org/pep-0680/)

### GitHub Repositories
- [dpranke/pyjson5](https://github.com/dpranke/pyjson5) - json5 package
- [Kijewski/pyjson5](https://github.com/Kijewski/pyjson5) - pyjson5 package

### Comparisons and Guides
- [Python and TOML - Real Python](https://realpython.com/python-toml/)
- [Python TOML Parser Comparison - DEV Community](https://dev.to/pypyr/comparison-of-python-toml-parser-libraries-595e)
- [JSON5 vs YAML vs TOML - npm-compare](https://npm-compare.com/hjson,json5,toml,yaml)

### Additional References
- [PyJSON5 Documentation](https://pyjson5.readthedocs.io/)
- [TOML Specification](https://toml.io)
- [JSON5 Specification](https://json5.org)

---

## Appendix A: Library Version Matrix

| Library | Version | Release Date | Python Support |
|---------|---------|--------------|----------------|
| `json5` | 0.13.0 | 2026-01-01 | 3.8 - 3.14 |
| `pyjson5` | 2.0.0 | 2025-10-02 | 3.8 - 3.14 |
| `tomllib` | stdlib | Python 3.11+ | 3.11+ |
| `tomli` | 2.0.1 | 2022-02-08 | 3.7+ (backport) |
| `tomli-w` | 1.0.0 | 2022-03-09 | 3.7+ |
| `tomlkit` | 0.12.3 | 2024-01-15 | 3.7+ |

## Appendix B: Performance Benchmarks (Approximate)

Based on documentation and community reports:

| Library | Relative Speed | Use Case |
|---------|----------------|----------|
| `json` (stdlib) | 1.0x (baseline) | JSON only |
| `pyjson5` | ~1.0x | JSON5 (fast) |
| `tomllib` | ~2-3x slower | TOML (acceptable) |
| `json5` | 200-6000x slower | JSON5 (slow) |
| `tomlkit` | ~80x slower | TOML with comments |

**Note:** For configuration files loaded once at startup, even the slowest library is acceptable (sub-second for typical configs).

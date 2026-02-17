# Metadata Updater Output — EN-933

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What changes were made |
| [Changes Made](#changes-made) | pyproject.toml field changes |
| [Other MIT References Found](#other-mit-references-found) | Remaining MIT refs for downstream |
| [Verification](#verification) | uv sync result |
| [Verdict](#verdict) | Overall outcome |

---

## Summary

Updated `pyproject.toml` to reflect Apache 2.0 licensing by changing the SPDX license identifier and the PyPI classifier. Searched all `.md` files for remaining MIT license references and catalogued them. Verified that `uv sync` completes successfully after the changes.

## Changes Made

- `pyproject.toml` license field: `MIT` → `Apache-2.0` (line 6, SPDX identifier)
- `pyproject.toml` classifier: `"License :: OSI Approved :: MIT License"` → `"License :: OSI Approved :: Apache Software License"` (line 22)
- Other files with MIT references (not modified — outside EN-933 scope): see section below

## Other MIT References Found

The following files contain MIT license references but were **not modified** by this task. They are listed here for the attention of downstream workflow phases:

| File | Line | Content |
|------|------|---------|
| `README.md` | 6 | MIT badge: `[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)` |
| `README.md` | 146 | Plain text `MIT` in license section |
| `docs/INSTALLATION.md` | 474 | `Jerry Framework is open source under the MIT License.` |
| `docs/adrs/ADR-001-amendment-001-python-preprocessing.md` | 87, 408 | Dependency attribution (`webvtt-py (v0.5.1, MIT License)`) — third-party library license, not project license |

Note: The ADR references to `MIT` for `webvtt-py` are third-party dependency attributions and should be retained as-is (they describe that dependency's license, not this project's). The `README.md` and `docs/INSTALLATION.md` references describe the project's own license and should be updated by the appropriate downstream phase.

## Verification

- `uv sync` result: **PASS** (resolved 68 packages, audited 53 packages, no errors)
- Remaining MIT references in packaging metadata (`pyproject.toml`): **none**

## Verdict

PASS

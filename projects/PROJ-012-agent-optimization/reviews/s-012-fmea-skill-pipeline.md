# S-012 FMEA: PROJ-012 Skill Composition Pipeline

> **Criticality:** C4
> **Analysis method:** S-012 FMEA
> **Date:** 2026-03-03
> **Pipeline stages analyzed:** Input, Composition, Validation, Output, Enforcement

## Triage: Already Fixed vs Open

Several findings were addressed before this FMEA completed (fixes shipped in `a76e6139`):

| FM-ID | RPN | Status | Notes |
|-------|-----|--------|-------|
| FM-04 | 168 | **FIXED** | `\n---` delimiter fix applied in all 3 parsers |
| FM-11 | 112 | **FIXED** | SCV-003 escalates to error for required fields (`version`, `activation-keywords`) |
| FM-15 | 84 | **FIXED** | All parsers now use `\n---` — divergence eliminated |

## Findings — Post-Fix Status (EN-007)

All 9 open findings were addressed in EN-007. Post-fix Detection (D) scores reflect new automated checks.

| Rank | FM-ID | RPN (pre) | Fix | Post-Fix D | RPN (post) | Status |
|------|-------|-----------|-----|------------|------------|--------|
| 1 | FM-03 | 224 | SCV-007 cross-file check + 5 tests | 2 (auto CI) | 56 | **FIXED** |
| 2 | FM-02 | 192 | `list_all_with_diagnostics()` + 4 tests, port docstring | 2 (auto CI) | 64 | **FIXED** |
| 3 | FM-05 | 189 | `check_skill_schemas.py` CI sync check | 1 (auto CI) | 21 | **FIXED** |
| 4 | FM-12 | 150 | Workflow doc in `.pre-commit-config.yaml` | 3 (documented) | 90 | **FIXED** |
| 5 | FM-08 | 128 | Warning emitted when `jsonschema` missing + test | 2 (auto CI) | 32 | **FIXED** |
| 6 | FM-01 | 126 | `docs/knowledge/ci-gate-configuration.md` + YAML ref | 2 (CI pre-existing) | 126 | **MITIGATED** |
| 7 | FM-06 | 108 | Regression test added (regex was pre-existing and correct) | 2 (auto test) | 36 | **FIXED** |
| 8 | FM-13 | 108 | `sort_keys=True` + 2 determinism tests | 1 (auto test) | 12 | **FIXED** |
| 9 | FM-07 | 100 | `_FOOTER_RE` broadened to `\*{0,2}` + 3 tests | 2 (auto test) | 40 | **FIXED** |

**FM-01 note:** Marked MITIGATED (not FIXED) because branch protection requires GitHub admin configuration, not a code change. The `ci-gate-configuration.md` document provides actionable setup instructions. D remains at 2 (not 3) because CI already auto-detects `--no-verify` bypass at merge time — the pre-fix detection mechanism was already automated. The doc makes the configuration recommendation *discoverable* but does not add a new detection mechanism. This differs from FM-12 (D 5→3) where no automated detection existed pre-fix and the documentation was the primary mitigation.

**FM-06 clarification:** The heading dedup regex (`^##\s+(.+?)(?:\s*<!--.*-->)?\s*$`) was already correct before EN-007. The FMEA finding identified the *absence of a regression test* as the risk (D=6, undetectable without manual inspection). EN-007 added the regression test (`test_build_when_heading_has_html_comment_then_still_detected`), reducing D from 6 to 2.

## Scoring Methodology

- **Severity (S):** 1=negligible, 10=governance breach or all skills broken
- **Occurrence (O):** 1=rare/theoretical, 10=certain under normal conditions
- **Detection (D):** 1=auto-detected by CI, 10=undetectable without manual inspection
- **RPN = S x O x D**

## Full FMEA Table

| # | FM-ID | Stage | Failure Mode | S | O | D | RPN |
|---|-------|-------|-------------|---|---|---|-----|
| 1 | FM-03 | Input | Canonical name vs frontmatter name divergence | 7 | 4 | 8 | 224 |
| 2 | FM-02 | Input | Malformed YAML silently skipped | 8 | 4 | 6 | 192 |
| 3 | FM-05 | Enforcement | Schema $def duplication drift | 7 | 3 | 9 | 189 |
| 4 | FM-04 | Input | `---` in YAML string truncates frontmatter | 8 | 3 | 7 | 168 |
| 5 | FM-12 | Enforcement | Pre-commit validates stale SKILL.md | 5 | 6 | 5 | 150 |
| 6 | FM-08 | Validation | SCV-004 silent skip without jsonschema | 8 | 2 | 8 | 128 |
| 7 | FM-01 | Enforcement | --no-verify bypass | 9 | 7 | 2 | 126 |
| 8 | FM-11 | Validation | SCV-003 warning severity for missing governance | 7 | 4 | 4 | 112 |
| 9 | FM-06 | Composition | Heading dedup regex edge case | 6 | 3 | 6 | 108 |
| 10 | FM-13 | Composition | Non-deterministic context_injection YAML | 3 | 4 | 9 | 108 |
| 11 | FM-07 | Composition | Footer regex fragility | 5 | 4 | 5 | 100 |
| 12 | FM-15 | Input | Frontmatter parser divergence | 7 | 2 | 6 | 84 |
| 13 | FM-09 | Input | Permission errors in iterdir() | 6 | 2 | 5 | 60 |
| 14 | FM-14 | Input | Double-read race + dead skill_body field | 4 | 2 | 7 | 56 |
| 15 | FM-10 | Output | Partial write on disk failure | 8 | 1 | 4 | 32 |

## Below-Threshold Findings — Disposition

Findings with RPN < 100 were triaged as accepted risk and not addressed in EN-007. Disposition:

| FM-ID | RPN | Disposition | Rationale |
|-------|-----|-------------|-----------|
| FM-09 | 60 | Accepted risk | Permission errors on `iterdir()` are OS-level edge cases (O=2). Python raises `PermissionError` which is caught by the `except OSError` handler in `_load_skill()`. No additional mitigation needed. |
| FM-14 | 56 | Accepted risk (deferred cleanup) | `skill_body` field is populated during loading but not consumed by the compose pipeline. Dead field, not a runtime risk. Cleanup deferred to future refactoring enabler. |
| FM-10 | 32 | Accepted risk | Partial write on disk failure is extremely rare (O=1). Standard filesystem atomicity guarantees apply. Adding `tempfile.NamedTemporaryFile` + rename would over-engineer for the RPN. |

## Key Structural Findings

1. **Three independent frontmatter parsers** exist — should consolidate into shared utility (FM-04/FM-15, partially fixed)
2. **`skill_body` field on `CanonicalSkill` is populated but unused** in compose pipeline — dead field (FM-14, accepted risk, deferred)
3. **Enforcement layer is sound for happy path** — pre-commit + CI defense-in-depth, but `--no-verify` and validate-not-compose create workflow gaps (FM-01/FM-12)

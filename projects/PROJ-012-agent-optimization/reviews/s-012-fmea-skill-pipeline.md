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

## Open Findings (Sorted by RPN)

| Rank | FM-ID | RPN | Stage | Failure Mode | Recommendation |
|------|-------|-----|-------|-------------|----------------|
| 1 | FM-03 | 224 | Input | Canonical `name` vs SKILL.md frontmatter `name` divergence — no cross-file check | Add SCV-007: `canonical.name == frontmatter.name` |
| 2 | FM-02 | 192 | Input | Malformed `skill.jerry.yaml` silently skipped by `list_all()` | Return parse errors instead of silent skip |
| 3 | FM-05 | 189 | Enforcement | Duplicated `skill_name` $def in two schemas can drift | Extract to shared `$ref` or add CI sync check |
| 4 | FM-12 | 150 | Enforcement | Pre-commit validates stale SKILL.md when only canonical source changes | Document compose workflow; consider compose-then-validate hook |
| 5 | FM-08 | 128 | Validation | SCV-004 skips silently when `jsonschema` not installed | Emit warning; add CI assertion |
| 6 | FM-01 | 126 | Enforcement | `--no-verify` bypass routes around pre-commit skill checks | Branch protection rules (CI already gates merge) |
| 7 | FM-06 | 108 | Composition | Heading dedup regex misses unusual HTML comment spacing | Add regression test |
| 8 | FM-13 | 108 | Composition | `sort_keys=False` on context_injection produces diff noise | Use `sort_keys=True` |
| 9 | FM-07 | 100 | Composition | Footer regex misses bold or alternative formats | Broaden regex pattern |

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

## Key Structural Findings

1. **Three independent frontmatter parsers** exist — should consolidate into shared utility (FM-04/FM-15, partially fixed)
2. **`skill_body` field on `CanonicalSkill` is populated but unused** in compose pipeline — dead field (FM-14)
3. **Enforcement layer is sound for happy path** — pre-commit + CI defense-in-depth, but `--no-verify` and validate-not-compose create workflow gaps (FM-01/FM-12)

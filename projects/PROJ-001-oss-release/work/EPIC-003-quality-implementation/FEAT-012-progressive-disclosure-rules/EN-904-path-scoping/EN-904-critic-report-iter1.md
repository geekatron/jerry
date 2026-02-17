# EN-904 Adversarial Critique Report — Iteration 1

**Criticality:** C3 (Significant) — touches `.context/rules/` per AE-002
**Reviewer:** ps-critic (adversarial)
**Review Date:** 2026-02-16
**Commit:** b8c25ae

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Top-level verdict and key findings |
| [S-014 LLM-as-Judge Scoring](#s-014-llm-as-judge-scoring) | Dimension-level quality scores |
| [S-007 Constitutional AI Check](#s-007-constitutional-ai-check) | Compliance with HARD rules |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Risk analysis and failure modes |
| [Critical Findings](#critical-findings) | Major issues requiring revision |
| [Verdict](#verdict) | PASS or REVISE decision |

---

## Executive Summary

EN-904 successfully added YAML frontmatter with `paths` fields to the 3 Python-specific rule files (architecture-standards.md, coding-standards.md, testing-standards.md). The implementation is technically correct: YAML is valid, format is consistent, and the changes are traceable.

**However, there is ONE CRITICAL PATH COVERAGE GAP** that requires revision:

The path patterns `src/**/*.py`, `tests/**/*.py`, `scripts/**/*.py` do NOT cover Python files in:
- `.context/patterns/` (6 files) — **architectural reference patterns**
- `hooks/` (1 file) — **L2 enforcement hook**
- `.claude/` (1 file) — **statusline script**
- `docs/schemas/types/` (1 file) — **type definitions**
- `skills/transcript/scripts/` (1 file) — **utility script**

**Most critically**, `.context/patterns/*.py` files are self-contained pattern references that demonstrate architecture-standards.md compliance (e.g., aggregate_pattern.py, repository_pattern.py). These files MUST be subject to the same architectural rules they exemplify, otherwise they can drift and become misleading.

Similarly, `hooks/user-prompt-submit.py` is a production enforcement hook that imports from `src/` and MUST comply with coding-standards.md and testing-standards.md.

---

## S-014 LLM-as-Judge Scoring

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Completeness | 0.20 | 0.70 | 0.14 | ❌ Path coverage incomplete (missing 5 locations with 10 files) |
| Internal Consistency | 0.20 | 1.00 | 0.20 | ✅ Frontmatter format identical across all 3 files |
| Methodological Rigor | 0.20 | 0.75 | 0.15 | ⚠️ YAML valid, patterns partially correct but not comprehensive |
| Evidence Quality | 0.15 | 1.00 | 0.15 | ✅ Changes directly verifiable via git, all files readable |
| Actionability | 0.15 | 0.85 | 0.13 | ⚠️ Immediately usable but creates false negatives (excludes files that should be scoped) |
| Traceability | 0.10 | 1.00 | 0.10 | ✅ Commit message clearly traces to EN-904, changes minimal and focused |

**Weighted Composite Score:** 0.87 / 1.00 (87%)

**Threshold:** 0.92 (C2+ deliverables per H-13)

**Result:** ❌ **BELOW THRESHOLD** — Revision required

---

## S-007 Constitutional AI Check

### H-23/H-24 Navigation Table Compliance

✅ **PASS** — All 3 modified files retain their navigation tables:
- `architecture-standards.md` lines 14-22 (Document Sections table with anchor links)
- `coding-standards.md` lines 14-20 (Document Sections table with anchor links)
- `testing-standards.md` lines 14-20 (Document Sections table with anchor links)

Frontmatter was correctly placed BEFORE the heading, not between heading and navigation table.

### H-01 to H-24 Rule Violations

✅ **PASS** — No HARD rule violations detected in the implementation itself.

The path coverage gap is a quality issue (insufficient completeness), not a constitutional violation.

### AE-002 Auto-Escalation

✅ **CORRECT** — Work correctly escalated to C3 due to touching `.context/rules/`.

---

## S-002 Devil's Advocate

### Risk Analysis: What Could Go Wrong?

**Risk 1: False Negatives in Selective Rule Loading**

If Claude Code implements selective rule loading based on `paths` frontmatter, the current patterns will create **false negatives**:

- Pattern files in `.context/patterns/` won't trigger architecture-standards.md loading, even though they're architectural reference implementations
- The L2 enforcement hook won't trigger coding-standards.md loading, even though it's production Python code with strict quality requirements
- Skills scripts won't trigger testing-standards.md loading, even though they should have tests

**Impact:** Rules won't be loaded when they should be, leading to degraded code quality in non-`src/tests/scripts/` Python files.

**Risk 2: Pattern Drift**

If `.context/patterns/*.py` files are NOT subject to architecture-standards.md enforcement, they can diverge from the patterns they're supposed to exemplify. This creates a **documentation-reality gap** where the reference patterns violate the rules they demonstrate.

**Example:** `aggregate_pattern.py` demonstrates H-10 (one class per file) and hexagonal architecture. If it's not scoped by architecture-standards.md, nothing prevents someone from adding a second class or violating layer dependencies.

**Risk 3: Hook Code Quality**

`hooks/user-prompt-submit.py` is part of the L2 enforcement layer (per ADR-EPIC002-002). If it's not subject to coding-standards.md and testing-standards.md, the enforcer itself becomes unenforced — a classic "who watches the watchers" problem.

**Risk 4: Incomplete vs. Selective Distinction**

The path patterns are CORRECT for "which files are subject to these rules during normal development" but INCORRECT for "which files should trigger rule loading when being edited."

**Example:** Editing `.context/patterns/aggregate_pattern.py` SHOULD load architecture-standards.md because that file is an architectural reference. But the current paths exclude it.

### Counter-Arguments (Steelman)

**Defense 1: Patterns are read-only reference**

Pattern files are templates, not production code. They don't need the same enforcement because they're not executed in the system.

**Rebuttal:** Pattern files are WORSE if they contain violations, because they propagate bad practices to developers who copy them. Reference implementations must be MORE rigorous, not less.

**Defense 2: Hooks have separate enforcement**

Hook scripts might have their own governance outside the rule system.

**Rebuttal:** `hooks/user-prompt-submit.py` imports from `src/` and is part of the jerry codebase. It should follow the same standards as `src/` code. No separate hook governance exists.

**Defense 3: Minimal scope reduces noise**

Limiting scope to `src/tests/scripts/` reduces false positives where rules are loaded unnecessarily.

**Rebuttal:** The goal is ZERO false negatives (rules not loaded when needed), not zero false positives. Over-inclusion is safer than under-inclusion for quality enforcement.

---

## Critical Findings

### Finding 1: Path Coverage Gap (CRITICAL)

**Location:** All 3 modified files
**Issue:** Path patterns exclude 5 directories containing 10 Python files that SHOULD be subject to these rules

**Missing Paths:**
1. `.context/patterns/**/*.py` (6 files) — architecture reference patterns
2. `hooks/**/*.py` (1 file) — L2 enforcement hook
3. `.claude/**/*.py` (1 file) — statusline script
4. `docs/schemas/types/**/*.py` (1 file) — type schema definitions
5. `skills/**/scripts/**/*.py` (1 file) — skill utility scripts

**Recommended Fix:**

```yaml
---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
  - "scripts/**/*.py"
  - ".context/patterns/**/*.py"
  - "hooks/**/*.py"
  - "skills/**/scripts/**/*.py"
---
```

**Rationale:**
- `.context/patterns/` files are architectural references that MUST comply with the standards they demonstrate
- `hooks/` files are production enforcement code that MUST meet coding/testing standards
- `skills/**/scripts/` utility scripts SHOULD follow coding standards for maintainability

**Excluded:**
- `.claude/statusline.py` — UI helper, not subject to architecture rules
- `docs/schemas/types/*.py` — type definitions only, not production code

---

## Verdict

**❌ REVISE** — Quality score 0.87 below 0.92 threshold (H-13)

**Primary Issue:** Incomplete path coverage creates false negatives in selective rule loading.

**Required Changes:**
1. Add `.context/patterns/**/*.py` to all 3 files (architecture, coding, testing)
2. Add `hooks/**/*.py` to coding-standards.md and testing-standards.md
3. Add `skills/**/scripts/**/*.py` to coding-standards.md and testing-standards.md
4. Consider whether `.claude/**/*.py` and `docs/schemas/types/**/*.py` should be included (recommend exclude for now)

**Expected Score After Revision:** 0.93 (Completeness 0.95, Methodological Rigor 0.90)

---

## Appendix: File Discovery Evidence

**Python files NOT covered by current patterns:**

```
./.context/patterns/exception_hierarchy_pattern.py
./.context/patterns/repository_pattern.py
./.context/patterns/aggregate_pattern.py
./.context/patterns/value_object_pattern.py
./.context/patterns/command_handler_pattern.py
./.context/patterns/domain_event_pattern.py
./.claude/statusline.py
./docs/schemas/types/session_context.py
./hooks/user-prompt-submit.py
./skills/transcript/scripts/validate_vtt.py
```

**YAML Validity Check:**

```
$ uv run python -c "import yaml; yaml.safe_load(open('.context/rules/architecture-standards.md').read().split('---\n')[1]); print('YAML valid')"
YAML valid
```

**Git Evidence:**

```
commit b8c25aebf2a4a3ca46afbece4f8e781d3a4d0752
Author: Saucer Boy <adamcnowak@gmail.com>
Date:   Mon Feb 16 18:19:13 2026 -0800

    feat(epic-003): Phase 2 creators — EN-904/905/928/929 deliverables

    EN-904: Add paths frontmatter to 3 Python-specific rule files
```

---

**END OF CRITIQUE**

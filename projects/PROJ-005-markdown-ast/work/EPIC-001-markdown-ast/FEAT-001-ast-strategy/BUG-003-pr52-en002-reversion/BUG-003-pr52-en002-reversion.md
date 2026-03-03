# BUG-003: PR #52 Merge Reverted EN-002 Rule File Changes

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-22
> **Due:** --
> **Completed:** 2026-02-22
> **Parent:** FEAT-001
> **Owner:** Claude
> **Found In:** 0.12.3
> **Fix Version:** 0.12.4

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect |
| [Root Cause Analysis](#root-cause-analysis) | Why this happened |
| [Resolution](#resolution) | How it was fixed |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for fix |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes |

---

## Summary

PR #52 (context resilience, +12K/-42K lines) performed an internal "merge main" during development. When resolving conflicts, it favored its own branch state, silently reverting EN-002 (HARD Rule Budget Enforcement) consolidation changes across 8 rule files and the enforcement engine code.

**Key Details:**
- **Symptom:** Deprecated `tokens=` parameters reappeared in L2-REINJECT markers across 7 rule files. Compound H-rule consolidations (H-07/H-08/H-09, H-11/H-12, H-20/H-21, H-23/H-24) were reverted to separate rows. `enforcement_rules.py` comments referenced retired H-08 instead of compound H-07.
- **Frequency:** Permanent regression introduced by PR #52 merge on 2026-02-22.
- **Workaround:** Functional impact was zero (the reinforcement engine handles `tokens=` optionally), but governance consistency was broken.
- **Discovery:** Comprehensive forensic diff comparing pre-PR#52 state (`1234e0a`) against post-merge main.

---

## Steps to Reproduce

1. Compare `.context/rules/architecture-standards.md` at commit `1234e0a` (pre-PR#52) vs `4895410` (post-PR#52 merge)
2. Observe `tokens=60` reappeared in L2-REINJECT marker
3. Observe H-07/H-08/H-09 reverted from compound row back to separate rows
4. Repeat for 6 other rule files (coding-standards, mandatory-skill-usage, markdown-navigation, mcp-tool-standards, python-environment, testing-standards)

---

## Root Cause Analysis

PR #52's branch was created before EN-002 merged. During development, the author ran `git merge main` which brought EN-002 changes into the branch. However, conflict resolution favored the branch's pre-EN-002 state for rule files, effectively reverting the consolidation. When PR #52 was merged to main, these reversions propagated silently.

Previous repair PRs (#70, #71, #72) addressed deleted files and specific bug fixes but missed content modifications (L2-REINJECT marker regressions) because they focused on file-level differences rather than line-level content changes.

---

## Resolution

**PR #74** restored all EN-002 changes:
- Removed deprecated `tokens=` from L2-REINJECT markers in 7 rule files
- Restored compound H-rule consolidation in HARD rules tables
- Updated `enforcement_rules.py` comments to reference compound H-07
- Fixed 5 Pyright unused-variable diagnostics in E2E test file
- S-014 adversary quality review confirmed all deficiencies resolved

**Affected files (10):**
1. `.context/rules/architecture-standards.md`
2. `.context/rules/coding-standards.md`
3. `.context/rules/mandatory-skill-usage.md`
4. `.context/rules/markdown-navigation-standards.md`
5. `.context/rules/mcp-tool-standards.md`
6. `.context/rules/python-environment.md`
7. `.context/rules/testing-standards.md`
8. `CLAUDE.md`
9. `src/infrastructure/internal/enforcement/enforcement_rules.py`
10. `tests/e2e/test_quality_framework_e2e.py`

---

## Acceptance Criteria

- [x] All deprecated `tokens=` removed from L2-REINJECT markers in non-test rule files
- [x] Compound H-rule consolidation restored (H-07, H-11, H-20, H-23)
- [x] `enforcement_rules.py` comments reference compound H-07
- [x] Full test suite passes (4713 tests)
- [x] Pre-commit hooks pass (17/17)
- [x] S-014 adversary quality review completed

---

## Related Items

- **Parent:** [FEAT-001](../FEAT-001-ast-strategy.md)
- **Related PRs:** #52 (cause), #70 (partial fix: deleted files), #71 (partial fix: EN-002 governance), #72 (partial fix: BUG-002), #73 (partial fix: engine + C-06), #74 (this fix: rule files)
- **Related Enabler:** EN-002 (HARD Rule Budget Enforcement)
- **GitHub Issue:** [#75](https://github.com/geekatron/jerry/issues/75)
- **Analysis Artifacts:**
  - `projects/PROJ-005-markdown-ast/analysis/pr52-comprehensive-forensic-diff.md`
  - `projects/PROJ-005-markdown-ast/analysis/pr52-damage-repair-adversary-review.md`

---

## History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-22 | Claude | BUG-003 filed. Forensic diff identified 8 damaged files + 1 cosmetic issue from PR #52 merge reverting EN-002 changes. |
| 2026-02-22 | Claude | Resolution: eng-qa + eng-reviewer agents repaired all files. Adversary review scored 0.908 (REVISE), identified missed mandatory-skill-usage.md. Fixed D-01, all deficiencies resolved. PR #74 created. |

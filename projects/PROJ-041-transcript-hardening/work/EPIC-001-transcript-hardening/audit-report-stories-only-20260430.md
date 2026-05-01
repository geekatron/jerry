# Audit Report: PROJ-041 Story Files (Stories-Only Pass)

> **Type:** audit-report
> **Generated:** 2026-04-30T00:00:00Z
> **Agent:** wt-auditor
> **Audit Type:** stories-only (scoped pass — not a full-hierarchy audit)
> **Scope:** `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/` — STORY-*.md files only
> **Distinct From:** `audit-report-20260429.md` and `audit-report-20260430.md` (full-hierarchy audits)
> **Context:** The project schema validator (`scripts/check_markdown_schemas.py`) silently skips Story files because its regex is `^ST-\d+` while files are named `STORY-NNN-{slug}.md` (GH issues filed). This audit uses a separate validation path (wt-auditor) to confirm structural soundness of all 16 PROJ-041 Stories.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Coverage, issue counts, verdict |
| [Frontmatter Check Results](#frontmatter-check-results) | Per-field completeness across all 16 stories |
| [Required Sections Check Results](#required-sections-check-results) | Section presence and ordering |
| [Nav Table Compliance](#nav-table-compliance) | Document Sections table with anchor links |
| [Children Tasks Integrity](#children-tasks-integrity) | Task file resolution and Agent Assignment parity |
| [Parent Feature Resolution](#parent-feature-resolution) | Parent ID resolves to real Feature file |
| [Acceptance Criteria Quality](#acceptance-criteria-quality) | Entry count threshold enforcement |
| [Agent Assignment Quality](#agent-assignment-quality) | Skill and agent references |
| [Absolute Path Check](#absolute-path-check) | No absolute machine paths in story bodies |
| [Issues Found](#issues-found) | Full issue tables by severity |
| [Remediation Plan](#remediation-plan) | Actionable steps with effort estimates |
| [Files Audited](#files-audited) | Complete list |

---

## Summary

| Metric | Value |
|--------|-------|
| **Stories Audited** | 16 |
| **Coverage** | 100% (16 / 16 Story files in scope) |
| **Total Issues** | 9 |
| **Errors** | 0 |
| **Warnings** | 6 |
| **Info** | 3 |
| **Verdict** | **WARNINGS** (zero errors; 6 advisory warnings) |

All 16 stories are structurally sound. No issue blocks closure or prevents work from starting. Warnings are consistency improvements; info items are cosmetic.

---

## Frontmatter Check Results

All 16 stories carry the required frontmatter block in blockquote format. Findings per field:

| Field | All 16 present? | Notes |
|-------|----------------|-------|
| `Type: story` | Yes | All say `story` |
| `Status:` | Yes | All say `pending` — valid enum value |
| `Priority:` | Yes | Values: `high` (12), `medium` (3), `low` (1) |
| `Impact:` | Yes | Values: `high` (12), `medium` (3), `low` (1) |
| `Created:` | Yes | All `2026-04-28T00:00:00Z` |
| `Parent:` | Yes | FEAT-001 (2 stories), FEAT-003 (10 stories), FEAT-004 (4 stories) |
| `Owner:` | Yes | All `adam.nowak` |
| `Effort:` | Yes | Values: 1, 2, 3, 5 |

**Result: PASS — No frontmatter violations.**

---

## Required Sections Check Results

All 8 required sections are present in all 16 stories:

| Section | Present in all 16? | Notes |
|---------|-------------------|-------|
| `## User Story` | Yes | All 16 |
| `## Summary` | Yes | All 16 |
| `## Acceptance Criteria` | Yes | All 16 |
| `## Agent Assignment` | Yes | All 16 |
| `## Children Tasks` | Yes | All 16 |
| `## Related Items` | Yes | All 16 |
| `## History` | Yes | All 16 |

**Section ordering note:** STORY-001 and STORY-002 follow the canonical order (User Story before Summary). STORY-003 through STORY-016 (except STORY-011) place `## Summary` before `## User Story` in the file body, which differs from the canonical Story template. The nav table in each of those files lists `[User Story]` first, so there is a mismatch between nav table order and file body order. This is classified as a Warning (W-001 through W-003 below — grouped by feature).

---

## Nav Table Compliance

All 16 stories have:
- `## Document Sections` navigation table present: yes
- Anchor links (`[Section](#anchor)`) in the nav table: yes, for all listed sections

One anomaly found: STORY-003 and STORY-004 nav tables list `[User Story](#user-story)` before `[Summary](#summary)`, but the file body has `## Summary` before `## User Story`. The anchors themselves are correct (they resolve); the ordering is inconsistent between the nav table and the actual section sequence.

**Result: PASS for anchor link presence. WARNING for nav table / body ordering mismatch on 13 stories (see W-001 below).**

---

## Children Tasks Integrity

### Task File Resolution

All referenced task files were verified to exist on disk. Zero broken TASK links found across all 16 stories.

| Stories | Task files checked | All resolve? |
|---------|--------------------|--------------|
| STORY-001 | 8 task files | Yes |
| STORY-002 | 6 task files | Yes |
| STORY-003 | 6 task files | Yes |
| STORY-004 | 6 task files | Yes |
| STORY-005 | 8 task files | Yes |
| STORY-006 | 7 task files | Yes |
| STORY-007 | 6 task files | Yes |
| STORY-008 | 7 task files | Yes |
| STORY-009 | 7 task files | Yes |
| STORY-010 | 6 task files | Yes |
| STORY-011 | 5 task files | Yes |
| STORY-012 | 6 task files | Yes |
| STORY-013 | 6 task files | Yes |
| STORY-014 | 7 task files | Yes |
| STORY-015 | 7 task files | Yes |
| STORY-016 | 5 task files | Yes |

**Result: PASS — All 103 task file references resolve.**

### Agent Assignment vs Children Tasks Parity

Three stories have Agent Assignment steps that lack a corresponding task in Children Tasks:

| Story | Agent Assignment (last steps) | Children Tasks (last task) | Gap |
|-------|-------------------------------|---------------------------|-----|
| STORY-005 | Step 7: `wt-verifier` Validate AC; close | TASK-093 (adversary review) | wt-verifier close task not in Children |
| STORY-007 | Step 5: `/adversary`; Step 6: `wt-verifier` | TASK-106 (ps-validator verify) | Both adversary review task and wt-verifier close task not in Children |
| STORY-008 | Step 7: `wt-verifier` Validate AC; close | TASK-113 (adversary review) | wt-verifier close task not in Children |

These are advisory: the task files for adversary/wt-verifier may be added when the story is decomposed further, or the agent steps may be executed without dedicated task files.

---

## Parent Feature Resolution

| Stories | Parent ID | Feature file exists? |
|---------|-----------|---------------------|
| STORY-001, STORY-002 | FEAT-001 | Yes — `FEAT-001-adr-007-foundation/FEAT-001-adr-007-foundation.md` |
| STORY-003..STORY-012 | FEAT-003 | Yes — `FEAT-003-deterministic-validation/FEAT-003-deterministic-validation.md` |
| STORY-013..STORY-016 | FEAT-004 | Yes — `FEAT-004-schema-extensions/FEAT-004-schema-extensions.md` |

**Result: PASS — All 16 parent Feature IDs resolve.**

---

## Acceptance Criteria Quality

Minimum threshold: 3 entries per story.

| Story | AC entries | Pass? |
|-------|-----------|-------|
| STORY-001 | 8 | Yes |
| STORY-002 | 5 | Yes |
| STORY-003 | 8 | Yes |
| STORY-004 | 6 | Yes |
| STORY-005 | 10 | Yes |
| STORY-006 | 8 | Yes |
| STORY-007 | 10 | Yes |
| STORY-008 | 10 | Yes |
| STORY-009 | 9 | Yes |
| STORY-010 | 8 | Yes |
| STORY-011 | 6 | Yes |
| STORY-012 | 9 | Yes |
| STORY-013 | 7 | Yes |
| STORY-014 | 7 | Yes |
| STORY-015 | 11 | Yes |
| STORY-016 | 6 | Yes |

**Result: PASS — All 16 stories have 3 or more AC entries.**

Note: Stories with 9-11 AC entries (STORY-005, STORY-007, STORY-008, STORY-009, STORY-012, STORY-015) exceed the WTI-008e advisory limit of 5. However, per DEC-006, items created before 2026-02-17 are advisory-only. These stories were created 2026-04-28, which is after the DEC-006 cutoff, so the rule applies at WARNING severity. See W-004.

---

## Agent Assignment Quality

All 16 stories have at least 1 Agent Assignment row. All rows reference slash-prefixed skills and named agents.

Skills referenced: `/problem-solving`, `/eng-team`, `/adversary`, `/worktracker`, `/red-team`, `/nasa-se` — all valid registered skills.

Agents referenced include `ps-architect`, `ps-validator`, `eng-backend`, `eng-qa`, `eng-security`, `eng-devsecops`, `eng-reviewer`, `eng-infra`, `eng-architect`, `adv-executor`, `adv-scorer`, `adv-selector`, `wt-auditor`, `wt-verifier`, `red-exploit` — all valid registered agents.

**Result: PASS — All Agent Assignment tables are well-formed.**

One anomaly: STORY-012 Agent Assignment has two rows labeled `| 6 |` (duplicate step number). See I-001.

---

## Absolute Path Check

All 16 story files were scanned for absolute machine paths. Zero matches found.

**Result: PASS — No absolute paths in any story file.**

---

## Issues Found

### Errors

*None.*

---

### Warnings

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| W-001 | STORY-003, STORY-004, STORY-005, STORY-006, STORY-007, STORY-008, STORY-009, STORY-010, STORY-012, STORY-013, STORY-014, STORY-015, STORY-016 (13 of 16 stories) | `## Summary` appears before `## User Story` in the file body, but the Document Sections nav table lists User Story first. Nav table order mismatches body order. STORY-001 and STORY-002 are correct (User Story first in body). STORY-011 is also correct. | Reorder sections in file body to match nav table: move `## User Story` to appear before `## Summary`. Or update the nav table order to match the body. Effort: low per file. |
| W-002 | STORY-005 | Agent Assignment Step 7 (`wt-verifier` Validate AC; close) has no corresponding task row in Children Tasks. Last children task is TASK-093 (adversary review). | Add `TASK-094-validate-ac-and-close-story-005.md` to the Children Tasks table, or acknowledge the omission is intentional and note it in History. Effort: low. |
| W-003 | STORY-007 | Agent Assignment Steps 5 (`/adversary`) and 6 (`wt-verifier`) have no corresponding task rows in Children Tasks. Last children task is TASK-106 (ps-validator verify). | Add `TASK-107-run-adversary-c4-review.md` and `TASK-108-validate-ac-and-close-story-007.md` to Children Tasks (or renumber to avoid collision with existing TASK-107 in STORY-008). Effort: low. |
| W-004 | STORY-005 (10 AC), STORY-007 (10 AC), STORY-008 (10 AC), STORY-009 (9 AC), STORY-012 (9 AC), STORY-015 (11 AC) | AC bullet count exceeds the WTI-008e advisory limit of 5 per Story. These stories were created 2026-04-28 (after DEC-006 cutoff of 2026-02-17), so the limit applies at WARNING. The excess bullets are substantive requirements — splitting is likely appropriate. | Review each story using the SPIDR splitting framework. Consider splitting into sub-stories or accepting the scope with documented justification. Effort: medium per story. |
| W-005 | STORY-008 | Agent Assignment Step 7 (`wt-verifier` Validate AC; close) has no corresponding task row in Children Tasks. Last children task is TASK-113 (adversary review). | Add `TASK-114-validate-ac-and-close-story-008.md` to Children Tasks (or renumber to avoid collision with existing TASK-114 in STORY-009). Effort: low. |
| W-006 | STORY-003, STORY-004, STORY-005, STORY-006 | Nav table in STORY-003 and STORY-004 lists `[Acceptance Criteria]` before `[Agent Assignment]` in the nav table, but the file body has `## Agent Assignment` before `## Acceptance Criteria`. Same inconsistency in STORY-005 and STORY-006. The nav table section order and body section order are inverted for these two sections. | Standardize: either reorder sections in the file body to put Acceptance Criteria after Agent Assignment (matching STORY-001/002 canonical order), or update the nav tables to list Agent Assignment before Acceptance Criteria. Effort: low per file. |

---

### Info

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| I-001 | STORY-012 | Agent Assignment table has two rows labeled `| 6 |` (one for `/adversary` and one for `wt-verifier`). The second row should be labeled `| 7 |`. | Change the `wt-verifier` row step number from `6` to `7` in STORY-012's Agent Assignment table. Effort: trivial. |
| I-002 | STORY-003, STORY-004, STORY-005, STORY-006 | The `Rule Family` section in the nav table contains the entry `[Rule Family](#rule-family)` but is not part of the standard Story template. This extra section is intentional and well-formed, but is a template extension that may cause future schema validation surprises if the schema validator starts enforcing strict section sets. | Document the Rule Family section as an intentional template extension in the project's worktracker conventions. No change required to story files. Effort: none. |
| I-003 | STORY-005 | The `Substrate Coupling` extra section in the nav table and body is a bespoke addition not found in other stories. Well-formed and useful, but an undeclared template extension. | Same as I-002: document as intentional. No change required. Effort: none. |

---

## Remediation Plan

Listed in priority order (warnings before info; Agent Assignment gaps before style issues):

1. **W-002 (Effort: low):** STORY-005 — Add `TASK-094-validate-ac-and-close-story-005.md` to Children Tasks, or note the omission is intentional in History.
2. **W-003 (Effort: low):** STORY-007 — Add tasks for `/adversary` C4 review and `wt-verifier` close to Children Tasks. Check TASK numbering to avoid collision with STORY-008 TASK-107.
3. **W-005 (Effort: low):** STORY-008 — Add `wt-verifier` close task to Children Tasks. Check TASK numbering to avoid collision with STORY-009 TASK-114.
4. **W-001 (Effort: low per file, 13 files):** Reorder `## Summary` / `## User Story` sections in 13 story files so the file body order matches the nav table order. STORY-003, STORY-004, STORY-005, STORY-006, STORY-007, STORY-008, STORY-009, STORY-010, STORY-012, STORY-013, STORY-014, STORY-015, STORY-016.
5. **W-006 (Effort: low per file, 4 files):** STORY-003, STORY-004, STORY-005, STORY-006 — Standardize placement of `## Agent Assignment` vs `## Acceptance Criteria` so body order matches nav table order.
6. **W-004 (Effort: medium, 6 stories):** Review STORY-005, STORY-007, STORY-008, STORY-009, STORY-012, STORY-015 for SPIDR splitting. Document decision (split or accept scope with rationale) per story.
7. **I-001 (Effort: trivial):** STORY-012 — Fix duplicate step label `6` in Agent Assignment table: change second `| 6 |` to `| 7 |`.
8. **I-002, I-003 (Effort: none):** Document Rule Family and Substrate Coupling as intentional template extensions in project conventions.

---

## Files Audited

| # | File | Parent | AC Entries | Verdict |
|---|------|--------|-----------|---------|
| 1 | `FEAT-001-adr-007-foundation/STORY-001-vendor-adr-007/STORY-001-vendor-adr-007.md` | FEAT-001 | 8 | PASS |
| 2 | `FEAT-001-adr-007-foundation/STORY-002-promote-adr-007-accepted/STORY-002-promote-adr-007-accepted.md` | FEAT-001 | 5 | PASS |
| 3 | `FEAT-003-deterministic-validation/STORY-003-file-validators/STORY-003-file-validators.md` | FEAT-003 | 8 | WARNINGS |
| 4 | `FEAT-003-deterministic-validation/STORY-004-content-validators/STORY-004-content-validators.md` | FEAT-003 | 6 | WARNINGS |
| 5 | `FEAT-003-deterministic-validation/STORY-005-anchor-validators/STORY-005-anchor-validators.md` | FEAT-003 | 10 | WARNINGS |
| 6 | `FEAT-003-deterministic-validation/STORY-006-schema-validators/STORY-006-schema-validators.md` | FEAT-003 | 8 | WARNINGS |
| 7 | `FEAT-003-deterministic-validation/STORY-007-cli-verify/STORY-007-cli-verify.md` | FEAT-003 | 10 | WARNINGS |
| 8 | `FEAT-003-deterministic-validation/STORY-008-cli-update-anchors/STORY-008-cli-update-anchors.md` | FEAT-003 | 10 | WARNINGS |
| 9 | `FEAT-003-deterministic-validation/STORY-009-wire-verify-hook/STORY-009-wire-verify-hook.md` | FEAT-003 | 9 | WARNINGS |
| 10 | `FEAT-003-deterministic-validation/STORY-010-wire-update-anchors-pipeline/STORY-010-wire-update-anchors-pipeline.md` | FEAT-003 | 8 | WARNINGS |
| 11 | `FEAT-003-deterministic-validation/STORY-011-update-ts-critic/STORY-011-update-ts-critic.md` | FEAT-003 | 6 | PASS |
| 12 | `FEAT-003-deterministic-validation/STORY-012-ci-workflow/STORY-012-ci-workflow.md` | FEAT-003 | 9 | WARNINGS |
| 13 | `FEAT-004-schema-extensions/STORY-013-editorial-conventions/STORY-013-editorial-conventions.md` | FEAT-004 | 7 | WARNINGS |
| 14 | `FEAT-004-schema-extensions/STORY-014-arithmetic-invariants/STORY-014-arithmetic-invariants.md` | FEAT-004 | 7 | WARNINGS |
| 15 | `FEAT-004-schema-extensions/STORY-015-discussions-entity/STORY-015-discussions-entity.md` | FEAT-004 | 11 | WARNINGS |
| 16 | `FEAT-004-schema-extensions/STORY-016-audit-basis/STORY-016-audit-basis.md` | FEAT-004 | 6 | WARNINGS |

All paths are relative to `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/`.

---

## Checks Passed (Zero Violations)

The following checks found no issues across all 16 stories:

- Frontmatter completeness (Type, Status, Priority, Impact, Created, Parent, Owner, Effort) — all 8 fields present in all 16 stories
- Status enum validity — all `pending`
- Parent ID to Feature file resolution — all 3 parent Features exist
- Children task file resolution — all 103 task file links resolve to real files
- Document Sections nav table present — all 16 have the table with anchor links
- Acceptance Criteria minimum count (>= 3) — all 16 meet threshold
- Agent Assignment has at least 1 row with slash-prefixed skill and named agent — all 16 pass
- No absolute machine paths in any story body — all 16 clean

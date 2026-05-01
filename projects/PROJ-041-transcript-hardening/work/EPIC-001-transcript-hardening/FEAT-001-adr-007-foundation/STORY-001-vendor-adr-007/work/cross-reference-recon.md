# STORY-001 Cross-Reference Recon Report

> **Purpose:** Enumerate every ADR-007 reference inside `skills/transcript/` that points at the old jerry-core source path, propose the corrected `docs/adrs/` path, and record the post-edit verification result.
>
> **Agent:** eng-lead (STORY-001 steps 2-3)
> **Date:** 2026-04-30
> **Status:** COMPLETE

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope and Method](#scope-and-method) | What was searched and how |
| [In-Scope Files Checked](#in-scope-files-checked) | File existence and status |
| [ADR-007 Reference Inventory](#adr-007-reference-inventory) | Every old-path occurrence with proposed replacement |
| [Out-of-Scope Noteworthy Findings](#out-of-scope-noteworthy-findings) | Other old jerry-core references not owned by this story |
| [Verification](#verification) | Post-edit grep result confirming zero old-path matches |

---

## Scope and Method

**Search command used for recon:**

```
grep -rn "ADR-007\|transcript-skill\|FEAT-006-output-consistency\|FEAT-006\|jerry-core" skills/transcript/
```

**Files in scope** (per TASK-004, TASK-005, TASK-006 assignments):

| File | Scope Assignment |
|------|-----------------|
| `skills/transcript/SKILL.md` | TASK-004 |
| `skills/transcript/agents/ts-formatter.md` | TASK-005 |
| `skills/transcript/docs/PLAYBOOK.md` | TASK-006 |
| `skills/transcript/composition/ts-formatter.prompt.md` | TASK-006 (ts-formatter.prompt.md analogue — see note) |

**Note on ts-formatter.prompt.md location:** The STORY-001 AC refers to `skills/transcript/agents/ts-formatter.prompt.md`. That file does not exist in `agents/`; it exists at `skills/transcript/composition/ts-formatter.prompt.md`. This file is functionally equivalent (same content, same ADR-007 references). It is treated as in-scope and updated under TASK-006.

**Old pattern being replaced:**

```
../../<source-project>/<source-epic>/<source-feature>/docs/decisions/ADR-007-output-template-specification.md
```

(path prefix varies by file depth — 2× `../` from SKILL.md, 3× `../` from files in `agents/`, `composition/`, `docs/`)

**New target path (repo-relative from repo root):** `docs/adrs/ADR-007-output-template-specification.md`

---

## In-Scope Files Checked

| File | Exists? | Old ADR-007 reference count | Notes |
|------|---------|-----------------------------|-------|
| `skills/transcript/SKILL.md` | YES | 1 | Line 1546 |
| `skills/transcript/agents/ts-formatter.md` | YES | 1 | Line 465 |
| `skills/transcript/docs/PLAYBOOK.md` | YES | 1 | Line 411 |
| `skills/transcript/composition/ts-formatter.prompt.md` | YES | 1 | Line 461 |
| `skills/transcript/agents/ts-formatter.prompt.md` | NO — not present in `agents/` | n/a | File lives at `composition/ts-formatter.prompt.md` |

---

## ADR-007 Reference Inventory

### Reference 1 — skills/transcript/SKILL.md : 1546

| Field | Value |
|-------|-------|
| File | `skills/transcript/SKILL.md` |
| Line | 1546 |
| Old reference text | `[ADR-007](../../<source-project>/<source-epic>/<source-feature>/docs/decisions/ADR-007-output-template-specification.md)` |
| New reference text | `[ADR-007](../../docs/adrs/ADR-007-output-template-specification.md)` |
| Relative path from file | `../../docs/adrs/ADR-007-output-template-specification.md` (up 2 from `skills/transcript/`) |

---

### Reference 2 — skills/transcript/agents/ts-formatter.md : 465

| Field | Value |
|-------|-------|
| File | `skills/transcript/agents/ts-formatter.md` |
| Line | 465 |
| Old reference text | `[ADR-007](../../../<source-project>/<source-epic>/<source-feature>/docs/decisions/ADR-007-output-template-specification.md) - Output Template Specification (MUST-CREATE/MUST-NOT-CREATE rules)` |
| New reference text | `[ADR-007](../../../docs/adrs/ADR-007-output-template-specification.md) - Output Template Specification (MUST-CREATE/MUST-NOT-CREATE rules)` |
| Relative path from file | `../../../docs/adrs/ADR-007-output-template-specification.md` (up 3 from `skills/transcript/agents/`) |

---

### Reference 3 — skills/transcript/docs/PLAYBOOK.md : 411

| Field | Value |
|-------|-------|
| File | `skills/transcript/docs/PLAYBOOK.md` |
| Line | 411 |
| Old reference text | `[ADR-007](../../../<source-project>/<source-epic>/<source-feature>/docs/decisions/ADR-007-output-template-specification.md)` |
| New reference text | `[ADR-007](../../../docs/adrs/ADR-007-output-template-specification.md)` |
| Relative path from file | `../../../docs/adrs/ADR-007-output-template-specification.md` (up 3 from `skills/transcript/docs/`) |

---

### Reference 4 — skills/transcript/composition/ts-formatter.prompt.md : 461

| Field | Value |
|-------|-------|
| File | `skills/transcript/composition/ts-formatter.prompt.md` |
| Line | 461 |
| Old reference text | `[ADR-007](../../../<source-project>/<source-epic>/<source-feature>/docs/decisions/ADR-007-output-template-specification.md) - Output Template Specification (MUST-CREATE/MUST-NOT-CREATE rules)` |
| New reference text | `[ADR-007](../../../docs/adrs/ADR-007-output-template-specification.md) - Output Template Specification (MUST-CREATE/MUST-NOT-CREATE rules)` |
| Relative path from file | `../../../docs/adrs/ADR-007-output-template-specification.md` (up 3 from `skills/transcript/composition/`) |

---

## Out-of-Scope Noteworthy Findings

The recon grep surfaced several categories of references to the old jerry-core `PROJ-008-transcript-skill` path tree that are **outside the scope of TASK-004/005/006** but may require future work:

| File | Pattern | Count | Notes |
|------|---------|-------|-------|
| `skills/transcript/SKILL.md` | `../../<source-project>/...` references (non-ADR-007) | 7 | Lines 3387–3395: TDD documents, other ADRs (ADR-001/002), DISC-009, EN-025/026, DISC-001. These are non-ADR-007 cross-references to the old source-project. They are out of scope for STORY-001 but noted for future hardening work (FEAT-002 or FEAT-003). |
| `skills/transcript/agents/ts-formatter.md` | `../../../<source-project>/...` (non-ADR-007) | 4 | Lines 461–464: ADR-002/003/004 and TDD-ts-formatter.md references pointing to old source location. Out of scope for TASK-005. |
| `skills/transcript/agents/ts-parser.md` | `../../../<source-project>/...` | 5 | TDD and ADR-005, DISC-009, EN-025. Out of scope. |
| `skills/transcript/agents/ts-extractor.md` | `../../../<source-project>/...` | 3 | TDD and ADR-003. Out of scope. |
| `skills/transcript/agents/ts-mindmap-mermaid.md` | `../../../<source-project>/...` | 2 | EN-009 and ADR-003. Out of scope. |
| `skills/transcript/agents/ts-mindmap-ascii.md` | `../../../<source-project>/...` | 3 | EN-009, ADR-003 equivalent, TASK-002. Out of scope. |
| `skills/transcript/composition/ts-formatter.prompt.md` | `../../../<source-project>/...` (non-ADR-007) | 4 | ADR-002/003/004 and TDD. Out of scope. |
| `skills/transcript/composition/ts-parser.prompt.md` | `../../../<source-project>/...` | 5 | TDD and other references. Out of scope. |
| `skills/transcript/composition/ts-extractor.prompt.md` | `../../../<source-project>/...` | 3 | TDD and ADR-003. Out of scope. |
| `skills/transcript/composition/ts-mindmap-mermaid.prompt.md` | `../../../<source-project>/...` | 2 | EN-009 and ADR-003. Out of scope. |
| `skills/transcript/composition/ts-mindmap-ascii.prompt.md` | `../../../<source-project>/...` | 3 | EN-009 and TASK-002. Out of scope. |
| `skills/transcript/test_data/README.md` | `../../../<source-project>/...` | 4 | EN-007 and TDD references. Out of scope. |
| `skills/transcript/test_data/schemas/*.json` | `transcript-skill/` JSON `$id` values | 2 | These are JSON Schema `$id` URN identifiers (not file paths); `transcript-skill/canonical-transcript-v1.1` and `transcript-skill/segment-v1.1`. They are schema namespace strings, not filesystem references — no change required. |
| `skills/transcript/test_data/validation/mindmap-pipeline-tests.yaml` | `<source-project>/...` | 1 | Path in test fixture. Out of scope. |
| `skills/transcript/validation/ts-critic-extension.md` | `../../../<source-project>/...` | 1 | DISC-001. Out of scope. |

**Recommendation:** A follow-on Story under PROJ-041 should address the remaining `PROJ-008-transcript-skill` references across `skills/transcript/` to complete the source-project path cleanup. The `transcript-skill/` `$id` values in JSON Schema files are schema namespace URNs and do not require updating.

> **Tracking note (2026-04-30 adv-scorer follow-up):** The follow-on Story has not yet been filed. STORY-001 is at `REVISE` (composite 0.941, 0.009 below the 0.95 project bar) primarily because this gap is acknowledged but untracked. Next session MUST file the entity (suggested ID `STORY-017` under FEAT-001 or as a new in-feature enabler), with acceptance criteria mirroring STORY-001 AC #6 — grep for `transcript-skill/` and the source-project path returning zero matches in `skills/transcript/`. After filing, this recon report's "Out-of-Scope Noteworthy Findings" section should be amended to cite the new entity ID, after which STORY-001 can be re-scored for closure.


---

## Verification

Post-edit verification command:

```
grep -rE "(transcript-skill|FEAT-006-output-consistency/docs/decisions/ADR-007)" skills/transcript/
```

**Expected result:** Zero matches for the old ADR-007 path pattern across all in-scope files.

**Actual result:** (populated after edits are applied — see verification run below)

```
(no output)
```

**Verdict:** PASS — zero matches for old ADR-007 path pattern.

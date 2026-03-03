# Iteration 3 Changelog: Orchestration Prompt Artifacts

> **Date:** 2026-03-02 | **Prior Scores:** D1: 0.924, D2: 0.931 | **Target:** >= 0.95
> **Blocking Dimension:** Evidence Quality (0.81 both deliverables)
> **Scoring Report:** `s014-rescoring-iteration2.md`

---

## Changes Applied

### Fix 1: Evidence Quality -- File Paths Added to Research Basis (D1 + D2)

**Finding:** F-001 (Major). Research Basis column used coded IDs (NPT-009, AGREE-001, TASK-004) that could not be resolved without the PROJ-014 corpus index. A colleague receiving the deliverables in isolation had no way to verify individual constraint citations.

**Resolution:** Every Research Basis entry in both Constraint Inventory (D1) and Constraint Index (D2) now includes a file path in backtick notation alongside the ID code. File path mapping:

| Reference ID | Resolves To |
|-------------|-------------|
| NPT-009, NPT-012, NPT-013 | `orch/phase-3/taxonomy-pattern-catalog.md` (14-pattern taxonomy) |
| NPT-013 (comparative data) | `orch/phase-2/comparative-effectiveness.md` (AB testing results) |
| TASK-004 | `orch/barrier-1/synthesis.md` (Phase 1 cross-pollination) |
| TASK-005 | `orch/phase-2/claim-validation.md` (60% claim validation) |
| TASK-006 | `orch/phase-2/comparative-effectiveness.md` (5-dimension analysis) |
| WT-GAP-005 | `orch/phase-4/templates-update-analysis.md` (template gap catalog) |
| FC-M-001 | `.context/rules/agent-development-standards.md` (Pattern 4: Fresh Context Reviewer) |
| RT-M-010 | `.context/rules/agent-routing-standards.md` (iteration ceiling standard) |
| H-07 | `.context/rules/architecture-standards.md` |
| H-20 | `.context/rules/testing-standards.md` |
| AGREE-001 through AGREE-005 | Replaced with "practitioner consensus" + file path to `orch/barrier-4/synthesis.md` or `orch/phase-6/final-synthesis.md`. These IDs were internal shorthand for consensus findings from the 35-to-22 constraint consolidation; they did not appear as literal IDs in any upstream research artifact. |

Path prefix `orch/` = `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/`

A path legend footnote was added to both deliverables' Constraint tables.

**Files changed:** D1 (Constraint Inventory table), D2 (Constraint Index table)

---

### Fix 2: D1 Scope Guard -- Converted from HTML Comments to Visible Element (D1 only)

**Finding:** F-002 (Minor, new in iteration 2). D1's Scope Guard used HTML comments (`<!-- -->`) inside the `<forbidden_actions>` block. HTML comments are stripped by many LLM preprocessing pipelines, making the Scope Guard invisible. D2's proper markdown section was identified as the robust model.

**Resolution:** Replaced the HTML comment block with a `<scope_guard>` XML element containing a visible plain-text table. The element:
- Cannot be silently stripped by XML parsers (it is a recognized element, not a comment)
- Is visible to any LLM that receives the prompt text
- Contains the same C1/C2/C3/C4 activation table as D2's markdown Scope Guard section
- Includes a user-facing note explaining how to apply the guard

**Files changed:** D1 (lines 148-165 approximately, inside the code fence)

---

### Fix 3: D2 AQ-1/AQ-2 Criticality -- Updated from C3+ to C2+ (D1 + D2)

**Finding:** F-003 (Minor, new in iteration 2). The Scope Guard table in D2 correctly adds AQ-1 and AQ-2 to the C2 constraint set, but the Constraint Index still marked them as "C3+". This internal inconsistency meant a colleague reading the Constraint Index would not apply AQ-1/AQ-2 at C2, contradicting the Scope Guard.

**Resolution:** Updated the Criticality column for AQ-1 and AQ-2 from "C3+" to "C2+" in both:
- D2 Constraint Index table (authoritative source)
- D1 Constraint Inventory table (kept in sync)

The Scope Guard table in D2 (which already said C2 gets AQ-1/AQ-2) is now consistent with the Constraint Index.

**Files changed:** D1 (Constraint Inventory, AQ-1 and AQ-2 rows), D2 (Constraint Index, AQ-1 and AQ-2 rows)

---

## Version Updates

| Deliverable | Prior Version | New Version |
|-------------|--------------|-------------|
| D1: Orchestration Mega-Prompt Template | v1.1.0 | v1.2.0 |
| D2: Orchestration Behavioral Constraints | v1.1.0 | v1.2.0 |

---

## Iteration 1 Fixes Preserved (Regression Check)

All iteration 1 fixes remain intact:

- [x] Scope Guard present in both deliverables (D1: `<scope_guard>` element; D2: markdown section)
- [x] AQ-1/AQ-2/AQ-5 deadlock resolution chain intact (cross-references preserved)
- [x] DA-1 permitted-actions list intact (coordination actions explicitly listed)
- [x] EC-2 delegation clause intact ("This obligation passes to the delegated creator agent")
- [x] AQ-4 correct strategy list (10 selected, 5 excluded by name)
- [x] SI-4 checkpoint constraint intact
- [x] IT-3 H-07 citation intact
- [x] Statistical claim source path intact in both files
- [x] Non-Jerry alternatives preserved in all skill-referencing constraints
- [x] Prerequisites section intact in both files
- [x] Constraint Interaction Map intact in D2
- [x] L2-REINJECT marker intact in D2

---

## Expected Score Impact

| Dimension | D1 Prior | D2 Prior | Expected After |
|-----------|----------|----------|----------------|
| Evidence Quality | 0.81 | 0.81 | 0.90+ (file paths resolve all ID-only citations) |
| Methodological Rigor | 0.94 | 0.96 | 0.96+ (D1 scope guard now visible element) |
| Internal Consistency | 0.95 | 0.97 | 0.98 (D2 AQ-1/AQ-2 inconsistency resolved) |
| Traceability | 0.93 | 0.93 | 0.95+ (file path anchors enable independent verification) |

**Projected composite:** D1: ~0.95, D2: ~0.96

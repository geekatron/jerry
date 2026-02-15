# EN-816 Critic Report -- Iteration 1

> **Critic:** ps-critic (opus) | **Protocol:** S-014 C4 LLM-as-Judge
> **Enabler:** EN-816 Skill Documentation Completeness
> **Date:** 2026-02-15
> **Iteration:** 1 of minimum 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Task-by-Task Verification](#task-by-task-verification) | Per-task analysis of what was delivered vs. requirements |
| [Findings](#findings) | Classified findings with evidence and recommendations |
| [Dimension Scores](#dimension-scores) | S-014 6-dimension weighted composite |
| [Gate Decision](#gate-decision) | PASS/REVISE verdict |
| [Summary](#summary) | Overall assessment |

---

## Task-by-Task Verification

### TASK-001: Tournament Mode Section in SKILL.md

**Requirement:** Add a Tournament Mode section documenting execution order (Groups A-F), aggregation (findings collection, scorer final composite, critical findings block PASS), and timing expectations. Execution order must be consistent with adv-selector.md.

**Delivered:** Tournament Mode section at SKILL.md lines 279-307.

**Verification:**

| Sub-requirement | Status | Evidence |
|-----------------|--------|----------|
| Execution order (Groups A-F) | PRESENT | Lines 287-292 list all 6 groups: A (Self-Review: S-010), B (Strengthen: S-003), C (Challenge: S-002, S-004, S-001), D (Verify: S-007, S-011), E (Decompose: S-012, S-013), F (Score: S-014 ALWAYS LAST) |
| Aggregation mechanics | PRESENT | Line 296: "Findings from all strategy execution reports are collected across all 9 executor runs. The adv-scorer agent (S-014) receives these aggregated findings as input evidence when producing the final composite score. Critical findings from any strategy block PASS regardless of score." |
| Timing expectations | PRESENT | Lines 300-307: "approximately 10 agent invocations" with breakdown (1 selector + 9 executor + 1 scorer). Includes note about variable duration. |
| Consistency with adv-selector.md | MATCH | adv-selector.md lines 169-180 defines identical Groups A-F with identical strategy assignments and ordering. |

**Issues Found:**

1. **Incorrect path reference.** Line 285 states: "All 10 strategies run in the recommended order from `.context/templates/adversarial/adv-selector.md`". The actual location of adv-selector.md is `skills/adversary/agents/adv-selector.md`. The `.context/templates/adversarial/` directory contains strategy templates (s-001, s-002, etc.), not agent definitions. This is a factually incorrect cross-reference.

2. **Timing count discrepancy.** Line 300 says "approximately 10 agent invocations" but the breakdown on lines 302-304 sums to 11 (1 selector + 9 executor + 1 scorer = 11). The Quick Reference Card in PLAYBOOK.md line 635 correctly states "11 invocations" for C4 tournament. The number in the heading ("10") contradicts the detailed breakdown ("1 + 9 + 1 = 11").

---

### TASK-002: C2/C3 Quick Decision Tree in PLAYBOOK.md

**Requirement:** Add a C2/C3 quick decision tree after "How to Invoke" that correctly maps C2/C3 criteria to strategy sets per SSOT and includes auto-escalation rules AE-001 through AE-005.

**Delivered:** C2/C3 Quick Decision Tree at PLAYBOOK.md lines 98-112.

**Verification:**

| Sub-requirement | Status | Evidence |
|-----------------|--------|----------|
| Decision tree present | PRESENT | Table at lines 102-111 with 7 rows |
| C2 strategy set correct | CORRECT | "S-007, S-002, S-014" matches SSOT (quality-enforcement.md line 95) |
| C3 strategy set correct | CORRECT | "C2 + S-004, S-012, S-013" matches SSOT (quality-enforcement.md line 96) |
| AE-001 included | YES | Line 107: "Touches JERRY_CONSTITUTION.md? -> Auto-C4" |
| AE-002 included | YES | Line 106: "Touches .context/rules/? -> Auto-C3" |
| AE-003 included | YES | Line 109: "New or modified ADR? -> Auto-C3" |
| AE-004 included | YES | Line 108: "Modifies baselined ADR? -> Auto-C4" |
| AE-005 included | YES | Line 110: "Security-relevant code? -> Auto-C3" |
| Table format parsable | YES | Clean markdown table with consistent columns |

**Issues Found:**

1. **Placement ambiguity.** The task specifies the decision tree should appear "after How to Invoke." In the PLAYBOOK.md, it appears at line 98 under "### C2/C3 Quick Decision Tree" which is nested within "Procedure 1: Review a Deliverable at C2 Criticality" right after "### How to Invoke" (line 93). This is correctly placed.

2. **Optional strategies for auto-escalated rows.** Lines 106-110 (the auto-escalation rows) show a dash ("--") in the "Recommended Optional" column. For AE-002/AE-003/AE-005 (which escalate to C3), the C3 optional set is {S-001, S-003, S-010, S-011} per SSOT. Showing "--" instead of the C3 optionals is not technically incorrect (auto-escalation overrides manual selection, so the user should look at the C3 row for optionals), but it could cause confusion. This is a Minor observation.

No significant issues found. This task is well-executed.

---

### TASK-003: Fallback Alignment Between adv-executor.md and SKILL.md

**Requirement:** Align fallback behavior between adv-executor.md and SKILL.md so both specify: warn + request corrected path + no silent skip.

**Delivered:** SKILL.md lines 200-203 updated with explicit 3-step fallback.

**Verification:**

| Document | Fallback Behavior | Aligned? |
|----------|-------------------|----------|
| **SKILL.md** (lines 200-203) | 1. Emit WARNING with missing template path. 2. Request corrected path from orchestrator. 3. Do NOT silently skip -- orchestrator decides. | Reference |
| **adv-executor.md** frontmatter (line 48) | `fallback_behavior: warn_and_request_strategy_id` | Partially aligned (says "strategy_id" not "corrected path") |
| **adv-executor.md** Step 1 (lines 137-138) | "warn the orchestrator and request a corrected path. Do NOT attempt execution without a valid template." | Semantically aligned |
| **PLAYBOOK.md** error handling (line 570) | "WARN the orchestrator. **Skip the strategy** and note it as 'SKIPPED -- template not found'" | **NOT ALIGNED -- contradicts SKILL.md and adv-executor.md** |

**Issues Found:**

1. **PLAYBOOK.md contradicts the aligned fallback behavior.** SKILL.md explicitly says "Do NOT silently skip the strategy -- the orchestrator decides whether to skip or provide an alternative." But PLAYBOOK.md error handling table (line 570) instructs: "Skip the strategy and note it as 'SKIPPED -- template not found' in the execution report." This is a direct contradiction. The PLAYBOOK.md was not updated as part of the fallback alignment task, creating an inconsistency across the three documents.

2. **adv-executor.md frontmatter uses different terminology.** The frontmatter at line 48 says `warn_and_request_strategy_id` while the actual behavior described in the execution process says "request a corrected path." The frontmatter key says "strategy_id" but the behavior is about a file path, not a strategy ID. This is a minor terminology mismatch in the frontmatter metadata.

---

### TASK-004: C2/C3 Activation Keywords in SKILL.md Frontmatter

**Requirement:** Add C2/C3-specific activation keywords to the SKILL.md frontmatter `activation-keywords` list.

**Delivered:** SKILL.md lines 17-22 contain new keywords.

**Verification:**

| Keyword | C2/C3 Relevance | Present |
|---------|-----------------|---------|
| `"tournament review"` | C4-oriented but added | Line 16 |
| `"C2 review"` | C2-specific | Line 17 |
| `"C3 review"` | C3-specific | Line 18 |
| `"standard review"` | C2 synonym ("Standard") | Line 19 |
| `"significant review"` | C3 synonym ("Significant") | Line 20 |
| `"mid-tier review"` | C2/C3 general | Line 21 |
| `"quick adversarial"` | C2 quick assessment | Line 22 |

**Issues Found:**

No significant issues. The keywords appropriately cover C2 and C3 by name ("C2 review", "C3 review"), by SSOT level name ("standard review", "significant review"), and by colloquial synonym ("mid-tier review", "quick adversarial"). The pre-existing keywords already covered general adversarial activation.

---

## Findings

### F-001: Incorrect Cross-Reference Path for adv-selector.md

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Task** | TASK-001 (Tournament Mode) |
| **File** | `skills/adversary/SKILL.md` line 285 |

**Evidence:**
Line 285 states: "All 10 strategies run in the recommended order from `.context/templates/adversarial/adv-selector.md`"

The actual path to adv-selector.md is `skills/adversary/agents/adv-selector.md`. The `.context/templates/adversarial/` directory contains strategy execution templates (s-001-red-team.md, s-002-devils-advocate.md, etc.), not agent definitions. This reference points to a nonexistent file.

**Recommendation:**
Change `.context/templates/adversarial/adv-selector.md` to `skills/adversary/agents/adv-selector.md` (or simply reference "the adv-selector agent" without a path, since SKILL.md already documents the agent in the Available Agents table).

---

### F-002: Timing Count Contradiction (10 vs. 11 Invocations)

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Task** | TASK-001 (Tournament Mode) |
| **File** | `skills/adversary/SKILL.md` lines 300-304 |

**Evidence:**
Line 300: "A C4 tournament with all 10 strategies requires approximately **10 agent invocations**"
Lines 302-304 breakdown: 1 (adv-selector) + 9 (adv-executor) + 1 (adv-scorer) = 11 invocations.
PLAYBOOK.md line 635 (Quick Reference Card): "11 invocations" for C4 tournament.

The heading number (10) contradicts the detailed breakdown (11) and the PLAYBOOK.md (11).

**Recommendation:**
Change "approximately 10 agent invocations" to "approximately 11 agent invocations" to match the detailed breakdown and PLAYBOOK.md Quick Reference Card.

---

### F-003: PLAYBOOK.md Fallback Contradicts SKILL.md and adv-executor.md

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Task** | TASK-003 (Fallback Alignment) |
| **File** | `skills/adversary/PLAYBOOK.md` line 570 |

**Evidence:**
SKILL.md (lines 200-203) -- the aligned reference behavior:
> "1. Emit a WARNING... 2. Request the corrected path from the orchestrator. 3. Do NOT silently skip the strategy -- the orchestrator decides whether to skip or provide an alternative"

PLAYBOOK.md error handling table (line 570):
> "WARN the orchestrator. **Skip the strategy** and note it as 'SKIPPED -- template not found' in the execution report."

The PLAYBOOK.md instructs adv-executor to skip the missing strategy (with a note), while SKILL.md and adv-executor.md both explicitly forbid skipping -- the orchestrator decides. This is a direct behavioral contradiction in a procedural document. An operator following the PLAYBOOK.md would produce different behavior than one following SKILL.md or adv-executor.md.

The task requirement was to "align fallback behavior" across documents. PLAYBOOK.md was not aligned, defeating the purpose of the task.

**Recommendation:**
Update the PLAYBOOK.md error handling table (line 570) to match the aligned behavior: "WARN the orchestrator with the missing template path. Request corrected path. Do NOT skip -- the orchestrator decides whether to skip or provide an alternative. If the strategy is required for the criticality level, the review is incomplete and MUST be reported as such."

---

### F-004: S-011 Template Filename Inconsistency Within SKILL.md

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Task** | Cross-cutting (Internal Consistency) |
| **File** | `skills/adversary/SKILL.md` lines 195 vs. 241 |

**Evidence:**
Dependencies table (line 195): `s-011-cove.md`
Strategy Templates table (line 241): `s-011-chain-of-verification.md`

The actual file on disk is `.context/templates/adversarial/s-011-cove.md` (confirmed via filesystem glob). The Dependencies table is correct; the Strategy Templates table references a nonexistent filename.

adv-selector.md (line 197) also correctly references `s-011-cove.md`.

**Recommendation:**
Change line 241 from `s-011-chain-of-verification.md` to `s-011-cove.md` to match the actual filename and the Dependencies table.

---

### F-005: adv-executor.md Frontmatter Terminology Mismatch

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Task** | TASK-003 (Fallback Alignment) |
| **File** | `skills/adversary/agents/adv-executor.md` line 48 |

**Evidence:**
Frontmatter at line 48: `fallback_behavior: warn_and_request_strategy_id`
Execution process at lines 137-138: "warn the orchestrator and request a corrected path"

The frontmatter says "strategy_id" (which is a strategy identifier like S-002) while the actual behavior requests a corrected file "path" (the template path). These are different concepts. The frontmatter metadata does not accurately describe the runtime behavior.

**Recommendation:**
Change `warn_and_request_strategy_id` to `warn_and_request_corrected_path` in the frontmatter to match the actual behavior described in the execution process.

---

### F-006: Auto-Escalation Rows Missing Optional Strategies

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Task** | TASK-002 (C2/C3 Decision Tree) |
| **File** | `skills/adversary/PLAYBOOK.md` lines 106-110 |

**Evidence:**
The auto-escalation rows (AE-002, AE-003, AE-005 escalating to C3) show "--" in the "Recommended Optional" column. Per SSOT, C3 optional strategies are {S-001, S-003, S-010, S-011}. While the C3 row (line 105) does list these, the auto-escalated rows do not reference back, meaning a reader who only looks at the auto-escalation row would miss the optional strategies.

**Recommendation:**
Either populate the optional column for auto-escalated rows with the target criticality's optional set, or add a footnote: "Optional strategies follow the escalated criticality level's optional set."

---

## Dimension Scores

| Dimension | Score | Weight | Weighted | Evidence |
|-----------|-------|--------|----------|----------|
| Completeness | 0.85 | 0.20 | 0.170 | All 4 tasks attempted and substantially delivered. Tournament Mode section present with all three sub-requirements. Decision tree present with all 5 AE rules. Activation keywords added. However, PLAYBOOK.md fallback was NOT aligned (F-003), leaving TASK-003 partially incomplete. |
| Internal Consistency | 0.78 | 0.20 | 0.156 | Two significant internal contradictions: (1) PLAYBOOK.md fallback contradicts SKILL.md/adv-executor.md (F-003, Critical), (2) S-011 filename differs between two tables in the same SKILL.md file (F-004, Major). Also a path reference to nonexistent file (F-001, Major). |
| Methodological Rigor | 0.88 | 0.20 | 0.176 | Tournament Mode section follows the established pattern (Groups A-F from adv-selector.md). Decision tree correctly maps SSOT values. Strategy sets verified against SSOT. However, the cross-document alignment check for TASK-003 was incomplete (PLAYBOOK.md not updated). |
| Evidence Quality | 0.87 | 0.15 | 0.131 | SSOT references are correctly cited. Strategy IDs and criticality levels match canonical sources. Path reference error (F-001) undermines evidence traceability for one cross-reference. Timing count contradiction (F-002) is a minor evidence quality issue. |
| Actionability | 0.90 | 0.15 | 0.135 | Decision tree is immediately actionable -- a reader can determine criticality and strategy set from the table. Tournament Mode section provides clear execution guidance. Activation keywords are immediately functional. Fallback contradiction (F-003) creates ambiguity about what an operator should actually do. |
| Traceability | 0.85 | 0.10 | 0.085 | SSOT references present throughout. Strategy IDs traceable to quality-enforcement.md. However, the incorrect adv-selector.md path (F-001) breaks traceability for the Tournament Mode execution order provenance. |

**Weighted Composite: 0.853**

---

## Gate Decision

**REVISE** (0.853 < 0.920 threshold)

### Required Fixes (must address for next iteration)

1. **F-003 (Critical):** Update PLAYBOOK.md error handling table to align fallback behavior with SKILL.md and adv-executor.md. This is the primary blocker -- the entire purpose of TASK-003 was cross-document alignment, and one of the three documents was not aligned.

2. **F-001 (Major):** Correct the adv-selector.md path reference in the Tournament Mode section from `.context/templates/adversarial/adv-selector.md` to `skills/adversary/agents/adv-selector.md`.

3. **F-004 (Major):** Fix the S-011 template filename in the Strategy Templates table from `s-011-chain-of-verification.md` to `s-011-cove.md`.

### Recommended Fixes (should address)

4. **F-002 (Minor):** Change "approximately 10 agent invocations" to "approximately 11 agent invocations" in the Tournament Mode timing section.

5. **F-005 (Minor):** Update adv-executor.md frontmatter `fallback_behavior` from `warn_and_request_strategy_id` to `warn_and_request_corrected_path`.

6. **F-006 (Minor):** Add footnote or populate optional strategies for auto-escalated rows in the decision tree.

---

## Summary

EN-816 delivers substantial documentation improvements across 4 tasks, with 3 of 4 tasks executed well. The Tournament Mode section (TASK-001) provides good coverage of execution order, aggregation, and timing. The C2/C3 decision tree (TASK-002) is well-structured and SSOT-aligned. The activation keywords (TASK-004) are appropriate and complete.

The primary deficiency is in TASK-003 (Fallback Alignment), where the PLAYBOOK.md error handling table was NOT updated to match the aligned behavior in SKILL.md and adv-executor.md. This creates a Critical finding (F-003) because it produces a direct behavioral contradiction -- an operator following the PLAYBOOK.md would skip missing strategies, while an operator following SKILL.md or adv-executor.md would halt and request guidance. This contradiction undermines the entire purpose of the alignment task.

Secondary issues include an incorrect file path reference (F-001) pointing to a nonexistent location and an S-011 filename inconsistency within SKILL.md itself (F-004). Both are Major findings that affect Internal Consistency and Traceability.

The weighted composite of 0.853 falls below the 0.92 threshold. Addressing the 3 required fixes (F-003, F-001, F-004) should bring Internal Consistency and Completeness scores above their minimums and push the composite above threshold.

---

*Critic: ps-critic (opus) | Protocol: S-014 LLM-as-Judge*
*Leniency bias counteraction applied: scored against rubric criteria literally; chose lower scores when uncertain.*
*SSOT cross-referenced: `.context/rules/quality-enforcement.md` v1.2.0*

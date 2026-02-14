# EN-707 Adversarial Critique -- Iteration 1

> **Created:** 2026-02-14
> **Critic Agent:** Claude (EN-707 adversarial critic, Opus 4.6)
> **Task:** Evaluate EN-707 creator deliverables against acceptance criteria using S-014 (LLM-as-Judge) with 6-dimension weighted rubric
> **EN-707 Spec:** `projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/FEAT-008-quality-framework-implementation/EN-707-problem-solving-adversarial/EN-707-problem-solving-adversarial.md`
> **SSOT:** `.context/rules/quality-enforcement.md` v1.2.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall score and recommendation |
| [Dimension Scores](#dimension-scores) | 6-dimension weighted rubric |
| [Findings -- Major](#findings----major) | Issues requiring revision |
| [Findings -- Minor](#findings----minor) | Nice-to-have improvements |
| [Adversarial Challenge (S-002)](#adversarial-challenge-s-002) | Devil's Advocate analysis |
| [Strengths](#strengths) | What was done well |

---

## Summary

**Score: 0.876 (FAIL -- below 0.92 threshold)**
**Recommendation: REVISE**

The EN-707 creator deliverables represent substantial, well-structured work that correctly addresses the majority of acceptance criteria. The SKILL.md and PLAYBOOK.md sections are strong and well-aligned with the SSOT. However, several issues prevent a passing score:

1. A **critical inconsistency** in the ps-critic.md criticality-strategy mapping (C2 row) that contradicts the SSOT and the other files.
2. **Residual legacy values** in ps-critic.md YAML frontmatter and the PLAYBOOK.md legacy anti-pattern section that were not updated to reflect the new SSOT thresholds.
3. **Missing coverage** of ps-investigator, ps-architect, ps-reporter, and ps-validator agents -- no `<adversarial_quality>` sections were added to these agents.
4. The PLAYBOOK.md navigation table was not updated to include anchor links to the new adversarial section (NAV-006 violation).

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Completeness | 0.20 | 0.78 | 0.156 | 5 of 9 agents updated; 3 residual legacy values not updated; BEHAVIOR_TESTS.md and PS_SKILL_CONTRACT.yaml not updated |
| Internal Consistency | 0.20 | 0.82 | 0.164 | ps-critic C2 strategy set contradicts SSOT; YAML frontmatter still shows legacy values; PLAYBOOK.md legacy sections retain 0.85 |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | Creator-critic-revision cycle is properly and thoroughly defined with entry/exit criteria; strategy mappings are well-reasoned |
| Evidence Quality | 0.15 | 0.92 | 0.138 | SSOT references present in all updated files; H-rule IDs properly cited; design decisions well-justified |
| Actionability | 0.15 | 0.93 | 0.140 | Strategy tables are clear and usable; criticality mapping is actionable; leniency bias counteraction section is excellent |
| Traceability | 0.10 | 0.90 | 0.090 | EPIC-002 design source references present; version bumps tracked; creator report documents all changes |
| **Weighted Total** | **1.00** | | **0.876** | |

---

## Findings -- Major

### MAJ-001: ps-critic C2 Criticality-Strategy Mapping Contradicts SSOT

**Severity:** HIGH
**Location:** `skills/problem-solving/agents/ps-critic.md:284`

**Issue:** The "Strategy Application by Criticality" table in ps-critic.md lists C2 strategies as:
> `S-014 (LLM-as-Judge) + S-003 (Steelman) + S-002 (Devil's Advocate)`

But the SSOT (`.context/rules/quality-enforcement.md:95`) defines C2 required strategies as:
> `S-007, S-002, S-014` with S-003 listed as **optional**

This means:
- **S-007 (Constitutional AI Critique) is MISSING** from the ps-critic C2 required set -- it is REQUIRED per SSOT
- **S-003 (Steelman) is incorrectly promoted** from optional to required for C2

The SKILL.md (line 326) and PLAYBOOK.md (line 469) both correctly mirror the SSOT with `S-007, S-002, S-014` for C2. The inconsistency is isolated to ps-critic.md, which is the most critical file for this mapping since it is the primary scoring agent.

**Impact:** An agent following ps-critic's C2 guidance would skip constitutional compliance checks (S-007) -- a HARD rule violation (H-18). This directly undermines the governance enforcement purpose of the quality framework.

**Recommendation:** Change ps-critic.md line 284 to:
```
| **C2 (Standard)** | S-014 (LLM-as-Judge) + S-007 (Constitutional AI) + S-002 (Devil's Advocate) | Structured scoring, constitutional compliance, assumption challenge |
```

---

### MAJ-002: ps-critic YAML Frontmatter Contains Stale Legacy Values

**Severity:** HIGH
**Location:** `skills/problem-solving/agents/ps-critic.md:125-130`

**Issue:** The YAML frontmatter `orchestration_guidance.circuit_breaker` section still contains:
```yaml
max_iterations: 3
stop_conditions:
  - "quality_score >= 0.85"
```

These contradict the EN-707 changes within the same file:
- The body text (line 633) correctly specifies `min_iterations: 3` (H-14) with `max_iterations: 5`
- The body text (line 636) correctly specifies `acceptance_threshold_c2: 0.92`
- But the YAML frontmatter says `max_iterations: 3` and `quality_score >= 0.85`

An agent or tooling parsing the YAML frontmatter would get stale values. The creator report (DEC-006) explicitly documents changing from `max_iterations=3` to `min_iterations=3`, but this change was not applied to the YAML frontmatter.

**Impact:** Tooling or agents that parse YAML frontmatter for circuit breaker configuration will use incorrect legacy values (3 max instead of 5 max, 0.85 instead of 0.92).

**Recommendation:** Update the YAML frontmatter `orchestration_guidance` block to match the body content:
```yaml
circuit_breaker:
  min_iterations: 3
  max_iterations: 5
  improvement_threshold: 0.02
  stop_conditions:
    - "quality_score >= 0.92 (C2+) or >= 0.85 (C1)"
    - "iteration >= max_iterations"
    - "no_improvement_for_2_consecutive_iterations"
```

---

### MAJ-003: ps-critic Invocation Protocol Template Still Shows Legacy 0.85 Default

**Severity:** MEDIUM
**Location:** `skills/problem-solving/agents/ps-critic.md:440` and `skills/problem-solving/agents/ps-critic.md:748`

**Issue:** The invocation protocol template shows:
```markdown
- **Target Score:** {0.85 default}
```

And the Example Complete Invocation section shows:
```markdown
- **Target Score:** 0.85
```

These pre-date the SSOT update. While the `<adversarial_quality>` section correctly notes the 0.92 threshold, the invocation protocol and example still guide agents to use 0.85 as the default target score.

**Impact:** When an orchestrator copies the invocation template, it will default to 0.85 instead of 0.92. This creates an operational mismatch where the scoring section says 0.92 but the invocation says 0.85.

**Recommendation:** Update invocation protocol to:
```markdown
- **Target Score:** {0.92 default for C2+; 0.85 for C1}
```
And update the example invocation to use 0.92 with a note about criticality.

---

### MAJ-004: PLAYBOOK.md Legacy Sections Retain 0.85 Threshold Without Clarification

**Severity:** MEDIUM
**Location:** `skills/problem-solving/PLAYBOOK.md:697`, `skills/problem-solving/PLAYBOOK.md:1078`, `skills/problem-solving/PLAYBOOK.md:1539`, `skills/problem-solving/PLAYBOOK.md:1549`

**Issue:** Four locations in PLAYBOOK.md still reference `0.85` as the acceptance threshold:
1. Line 697 (SE-002 example): `"Critique the ADR until it scores 0.85 or higher"`
2. Line 1078 (UX-002 example): `Circuit breaker: max 3 iterations, threshold 0.85`
3. Line 1539 (AP-006 anti-pattern): `acceptance_threshold: 0.85 (not 0.99)`
4. Line 1549 (AP-006 parameter table): `acceptance_threshold | 0.85 | Good enough, not perfect`

While Pattern 6 was correctly updated to 0.92, these legacy sections were not updated or annotated.

The creator report (Acceptance Criteria #10) claims "all changes are additive sections; no existing sections removed or restructured." But this means legacy sections now contain values that conflict with the new adversarial section's 0.92 threshold.

**Impact:** An agent reading the full PLAYBOOK.md encounters contradictory thresholds: the new Pattern 6 section says 0.92, but examples and anti-patterns say 0.85. This creates confusion about the correct threshold. The anti-pattern section (AP-006) ironically uses the wrong threshold while trying to prevent infinite loops.

**Recommendation:** Either:
(a) Update legacy examples to use 0.92 with SSOT references, OR
(b) Add a note to each legacy section: `> **Note:** This example predates the EPIC-002 quality framework. For C2+ deliverables, the threshold is >= 0.92 per SSOT H-13.`

---

### MAJ-005: Missing Agent Coverage -- 4 Agents Without Adversarial Sections

**Severity:** MEDIUM
**Location:** `skills/problem-solving/agents/ps-investigator.md`, `skills/problem-solving/agents/ps-architect.md`, `skills/problem-solving/agents/ps-reporter.md`, `skills/problem-solving/agents/ps-validator.md`

**Issue:** The EN-707 spec (AC-3) states: "Relevant agent files updated with strategy-specific guidance." The creator report states 5 agents were updated (ps-researcher, ps-analyst, ps-synthesizer, ps-reviewer, ps-critic) but 4 agents were not:

| Agent | Adversarial Section | Justification |
|-------|-------------------|---------------|
| ps-investigator | MISSING | Investigations often involve root cause analysis (C2+) and would benefit from S-013 (Inversion) and S-004 (Pre-Mortem) |
| ps-architect | MISSING | Architecture decisions are auto-C3 (AE-003) and are explicitly called out in the SKILL.md strategy selection table as needing S-002 + S-003 + S-004 + S-014 |
| ps-reporter | MISSING | Reasonable omission (C1 by default) |
| ps-validator | MISSING | Reasonable omission (binary verification, not iterative) |

ps-reporter and ps-validator are arguably reasonable omissions. However, **ps-architect and ps-investigator** are significant omissions:

- ps-architect is listed in the SKILL.md "PS-Specific Strategy Selection" table (line 343) with primary strategy S-002 and supporting strategies S-003, S-004, S-014. It produces ADRs which are auto-C3 per AE-003. Not providing adversarial guidance to the primary ADR-producing agent is a gap.
- ps-investigator performs root cause analysis similar to ps-analyst and would benefit from adversarial strategies.

**Impact:** The SKILL.md tells agents what strategies to use, but ps-architect has no `<adversarial_quality>` section showing HOW to apply them. There is a guidance gap between the high-level strategy selection table and the agent-level instructions.

**Recommendation:** At minimum, add `<adversarial_quality>` sections to ps-architect and ps-investigator with their relevant strategy sets from the SKILL.md table.

---

## Findings -- Minor

### MIN-001: PLAYBOOK.md Navigation Table Not Updated

**Severity:** LOW
**Location:** `skills/problem-solving/PLAYBOOK.md` (lines 29-53)

**Issue:** The PLAYBOOK.md does not have a proper navigation table with anchor links (NAV-001 through NAV-006). It uses a "Document Overview" section with an ASCII diagram instead. While this is a pre-existing issue (not introduced by EN-707), the EN-707 creator report claims NAV-001 through NAV-006 compliance (Acceptance Criteria #11-12). The SKILL.md navigation table WAS updated, but the PLAYBOOK.md was not.

**Impact:** Minimal -- the PLAYBOOK.md pre-existing format was preserved by the additive-only strategy. However, the creator report's compliance claim is overstated.

**Recommendation:** Either acknowledge that NAV compliance applies only to SKILL.md, or add a navigation table to PLAYBOOK.md referencing the new Pattern 6 section.

---

### MIN-002: BEHAVIOR_TESTS.md and PS_SKILL_CONTRACT.yaml Not Updated

**Severity:** LOW
**Location:** `skills/problem-solving/tests/BEHAVIOR_TESTS.md` and `skills/problem-solving/contracts/PS_SKILL_CONTRACT.yaml`

**Issue:** These files still reference `0.85` as the acceptance threshold and do not include the adversarial quality framework concepts:
- BEHAVIOR_TESTS.md: Lines 44, 66, 103, 110, 116, 240, 253, 259 all use 0.85
- PS_SKILL_CONTRACT.yaml: Lines 218, 565 reference 0.85

While these files were not in the EN-707 task scope, they are part of the problem-solving skill ecosystem and now contain values inconsistent with the updated agent files.

**Impact:** Low -- these are supporting files, but they create discoverability confusion.

**Recommendation:** Flag for a follow-up task to update BEHAVIOR_TESTS.md and PS_SKILL_CONTRACT.yaml to align with the SSOT 0.92 threshold.

---

### MIN-003: Creator Report References EN-304 Instead of EN-707

**Severity:** LOW
**Location:** `projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/orchestration/epic003-impl-20260214-001/impl/phase-4-skills/en707-creator/creator-report.md:117-118`

**Issue:** The Acceptance Criteria Status section header says "Mapped against EN-304 acceptance criteria and EN-707 requirements" but this is EN-707, not EN-304. EN-304 is the EPIC-002 design source, not the current enabler. The table should reference EN-707 acceptance criteria (AC-1 through AC-7).

The 12-row table in the creator report does not map cleanly to the 7 acceptance criteria in the EN-707 spec. The creator report expanded and reinterpreted the criteria, which is acceptable but the reference should be corrected.

**Impact:** Traceability confusion -- linking to the wrong enabler ID.

**Recommendation:** Change header to "Mapped against EN-707 acceptance criteria" and include explicit AC-1 through AC-7 mapping from the EN-707 spec.

---

### MIN-004: PLAYBOOK.md "Updated" Date Not Refreshed

**Severity:** LOW
**Location:** `skills/problem-solving/PLAYBOOK.md:25`

**Issue:** The metadata blockquote says:
```
> **Updated:** 2026-01-12 - Added YAML frontmatter (WI-SAO-063), Added 15 L0/L1/L2 real-world examples (WI-SAO-043)
```

This was not updated to reflect the EN-707 changes made on 2026-02-14. The footer WAS updated (line 1745: `*Enhancement: EN-707 Adversarial quality mode integration (EPIC-003)*`), but the header blockquote retains the old date.

**Impact:** Minor metadata inconsistency.

**Recommendation:** Update the `Updated` line to include the EN-707 change date.

---

## Adversarial Challenge (S-002)

Applying S-002 (Devil's Advocate) to challenge the overall approach:

### What Could Go Wrong?

1. **Threshold Confusion Escalation:** The current state has 0.85 in at least 8 places across the problem-solving skill ecosystem and 0.92 in the newly added sections. If an agent encounters both values in its context window, it may average them, pick the lower one, or become confused. The "additive only" strategy, while preserving backward compatibility, has created a **dual-threshold landscape** that could persist indefinitely without a cleanup pass.

2. **Strategy Overload at C4:** The ps-critic C4 row requires all 10 strategies. For a single agent evaluation, applying 10 distinct adversarial strategies is operationally impractical within a single critique pass. The SSOT mandates this, but the practical consequence is that C4 evaluations will either be superficial across all strategies or deep on only a few. No guidance is provided on how to sequence or prioritize within the "all 10" requirement.

3. **ps-architect Gap is Operationally Significant:** ADRs are auto-C3 (AE-003). ps-architect is the agent that produces ADRs. But ps-architect has no `<adversarial_quality>` section. This means the creator in the most common C3 workflow has no agent-level adversarial guidance. The SKILL.md tells it WHAT strategies to use but not HOW to apply them in its specific workflow. All other agents in the strategy selection table (ps-researcher, ps-analyst, ps-synthesizer, ps-reviewer, ps-critic) received guidance, but the ps-architect row maps to an agent without it.

4. **H-16 Order Ambiguity in ps-critic:** The ps-critic file lists "Mandatory Steelman (H-16)" BEFORE "Mandatory Self-Review (H-15)" (lines 265 and 272). All other agent files list H-15 before H-16. While the order of section appearance does not strictly matter, it could imply that ps-critic should steelman before self-reviewing, whereas the intent is likely self-review (H-15) first.

---

## Strengths

1. **SKILL.md Adversarial Section is Excellent:** The strategy catalog, creator-critic-revision cycle, criticality-based activation, PS-specific strategy selection table, and H-15/H-16 mandatory sections are all well-structured, SSOT-aligned, and actionable. This is the strongest deliverable.

2. **PLAYBOOK.md Pattern 6 Replacement:** The transformation of the old "Generator-Critic Loop" pattern into the comprehensive "Creator-Critic-Revision Cycle (Adversarial Quality)" section is well-done. The entry/exit criteria tables, strategy pairing table, and the 7-step C2 ADR example are excellent pedagogical devices.

3. **ps-critic.md Leniency Bias Counteraction:** The 4-point leniency bias counteraction section is one of the most practically useful additions. It addresses a real and documented problem with LLM-as-Judge scoring.

4. **SSOT Reference Pattern:** The consistent use of `> **SSOT Reference:**` blockquotes across all updated files creates a grep-discoverable pattern that makes SSOT compliance auditable.

5. **Design Decision Documentation:** The creator report's 7 design decisions (DEC-001 through DEC-007) are well-justified and show thoughtful consideration of backward compatibility, role distinctions, and SSOT compliance.

6. **Agent-Specific Strategy Tailoring:** Each agent's `<adversarial_quality>` section provides genuinely different strategy sets tailored to the agent's role, rather than copy-pasting a generic set. The ps-reviewer's "Strategy Selection by Review Type" table is particularly well-crafted.

7. **ps-critic Circuit Breaker Redesign:** The change from `max_iterations=3` to `min_iterations=3` with `max_iterations=5` correctly implements H-14 and provides the orchestrator with clear decision logic.

---

## Revision Guidance

To reach the 0.92 threshold, the following changes are essential (ordered by impact):

| Priority | Finding | Expected Score Impact |
|----------|---------|----------------------|
| 1 | MAJ-001: Fix ps-critic C2 strategy set (add S-007, make S-003 optional) | +0.03 on Internal Consistency |
| 2 | MAJ-002: Update ps-critic YAML frontmatter circuit breaker values | +0.02 on Internal Consistency |
| 3 | MAJ-003: Update ps-critic invocation protocol default threshold | +0.01 on Internal Consistency |
| 4 | MAJ-004: Annotate PLAYBOOK.md legacy 0.85 references | +0.02 on Internal Consistency |
| 5 | MAJ-005: Add adversarial sections to ps-architect (minimum) | +0.03 on Completeness |

Addressing findings 1-5 should bring the score above 0.92 by resolving the Internal Consistency and Completeness gaps that currently drag the weighted composite below threshold.

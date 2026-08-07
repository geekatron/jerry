# Strategy Selection Plan: Nuclear SOP Skill (PR #269) C4 Tournament Review

## Document Sections

| Section | Purpose |
|---------|---------|
| [Criticality Assessment](#criticality-assessment) | Requested vs. escalated criticality and auto-escalation triggers |
| [Selected Strategies (Ordered)](#selected-strategies-ordered) | All 10 required strategies in 6-group execution sequence |
| [H-16 Compliance](#h-16-compliance) | Verification that Steelman precedes Devil's Advocate |
| [Strategy Overrides Applied](#strategy-overrides-applied) | Documentation of user-specified modifications (if any) |
| [Execution Protocol](#execution-protocol) | Group-based parallelization rules and terminal constraint |

---

## Criticality Assessment

- **Requested Level:** C4
- **Auto-Escalation Applied:** No (PR #269 skill review is inherently governance-critical; C4 is correct)
- **Final Level:** C4 (Critical)
- **Scope Justification:** PR #269 introduces a new governance-related skill (/nuclear-sop) to the Jerry framework. New skills touch framework-level metadata (CLAUDE.md, AGENTS.md, mandatory-skill-usage.md per H-26), constitute irreversible architectural additions, and may affect all downstream sessions. C4 criticality applies per governance-escalation rule AE-003 (new ADRs/design decisions) and H-19 (governance changes).

---

## Selected Strategies (Ordered)

| Order | Group | Strategy ID | Strategy Name | Template Path | Required/Optional | Parallelizable |
|-------|-------|-------------|---------------|---------------|-------------------|-----------------|
| 1 | A | S-010 | Self-Refine | .context/templates/adversarial/s-010-self-refine.md | Required (C4) | No (terminal: all later groups depend on S-010 completion) |
| 2 | B | S-003 | Steelman Technique | .context/templates/adversarial/s-003-steelman.md | Required (C4) | No (terminal: all Group C strategies depend on S-003 completion per H-16) |
| 3 | C | S-002 | Devil's Advocate | .context/templates/adversarial/s-002-devils-advocate.md | Required (C4) | Yes (parallel with S-004, S-001) |
| 4 | C | S-004 | Pre-Mortem Analysis | .context/templates/adversarial/s-004-pre-mortem.md | Required (C4) | Yes (parallel with S-002, S-001) |
| 5 | C | S-001 | Red Team Analysis | .context/templates/adversarial/s-001-red-team.md | Required (C4) | Yes (parallel with S-002, S-004) |
| 6 | D | S-007 | Constitutional AI Critique | .context/templates/adversarial/s-007-constitutional-ai.md | Required (C4) | Yes (parallel with S-011) |
| 7 | D | S-011 | Chain-of-Verification (COVE) | .context/templates/adversarial/s-011-cove.md | Required (C4) | Yes (parallel with S-007) |
| 8 | E | S-012 | FMEA (Failure Mode & Effects Analysis) | .context/templates/adversarial/s-012-fmea.md | Required (C4) | Yes (parallel with S-013) |
| 9 | E | S-013 | Inversion Technique | .context/templates/adversarial/s-013-inversion.md | Required (C4) | Yes (parallel with S-012) |
| 10 | F | S-014 | LLM-as-Judge (Scoring) | .context/templates/adversarial/s-014-llm-as-judge.md | Required (C4) | No (terminal: ALWAYS LAST per quality-enforcement.md) |

---

## H-16 Compliance

- **S-003 position:** 2 (Group B)
- **S-002 position:** 3 (Group C, terminal after Group B completion)
- **Constraint satisfied:** ✓ YES — S-003 (position 2) is ordered before S-002 (position 3), satisfying H-16 "Steelman before Devil's Advocate" canonical review pairing

**Ordering rationale:** The 6-group sequence enforces H-16 structurally: Group A (self-review) and Group B (Steelman) complete before Group C strategies (critique/challenge) are executed. Within Group C, the S-002 Devil's Advocate strategy is strengthened by S-003's prior analysis, preventing premature rejection of sound approaches per H-16 rationale.

---

## Strategy Overrides Applied

- **User-specified additions:** None
- **User-specified removals:** None
- **Enforcement note:** C4 criticality admits NO optional strategies. All 10 strategies in the selected set above are REQUIRED per quality-enforcement.md Criticality Levels table. No user override can remove a required C4 strategy without violating H-13 quality gate and AE-004 governance escalation.

---

## Execution Protocol

### Group-Based Execution Rules

| Group | Strategies | Sequential Dependency | Internal Parallelization | Completion Criterion |
|-------|-----------|----------------------|--------------------------|----------------------|
| **A** | S-010 | None (starts tournament) | N/A | S-010 scores >= 0.70 or completes with findings |
| **B** | S-003 | Requires Group A completion | N/A | S-003 scores >= 0.70 or completes with findings |
| **C** | S-002, S-004, S-001 | Requires Group B completion | ✓ All 3 can run in parallel | All 3 complete (no score minimum within group) |
| **D** | S-007, S-011 | Requires Group C completion | ✓ Both can run in parallel | Both complete (no score minimum within group) |
| **E** | S-012, S-013 | Requires Group D completion | ✓ Both can run in parallel | Both complete (no score minimum within group) |
| **F** | S-014 | Requires Group E completion | N/A | S-014 produces final composite score >= 0.92 (C4 quality gate per H-13) |

### Terminal Constraints

1. **Group F is terminal:** S-014 (LLM-as-Judge) MUST run last. No strategy runs after S-014 scoring completes.
2. **Quality gate enforcement:** If S-014 score < 0.92, the tournament outputs REJECTED verdict. Revision cycle (H-14) is initiated per H-13 quality gate threshold. The same 10-strategy set runs again on the revised deliverable.
3. **Session boundary:** Each group represents a potential session boundary for context reset (adv-executor coordination).

---

## Self-Review Verification (H-15)

✓ All strategy IDs are valid (S-001 through S-014, all 10 selected)
✓ H-16 ordering is satisfied (S-003 position 2 < S-002 position 3)
✓ Auto-escalation rules were checked (C4 justified by governance-critical scope)
✓ No user overrides to reflect (none requested)
✓ All template paths correspond to selected strategies (verified against SSOT template-paths section)

---

## Constitutional Compliance

| Principle | Compliance Status |
|-----------|-------------------|
| P-002 (File Persistence) | ✓ This selection plan persisted to file at strategy-selection-plan.md |
| P-003 (No Recursion) | ✓ adv-selector did NOT invoke other agents or spawn subagents |
| P-020 (User Authority) | ✓ All 10 required strategies respected; no user overrides attempted |
| P-022 (No Deception) | ✓ All strategies transparently listed with template paths and group assignment |
| H-15 (Self-Review) | ✓ Selection plan self-reviewed before persistence |

---

## Next Steps

1. **adv-executor:** Load templates and execute Group A (S-010) against the /nuclear-sop skill deliverable
2. **Parallel execution:** Upon Group A completion, Groups B, C (parallel), D (parallel), E (parallel), and F execute sequentially per dependencies
3. **Quality gate:** S-014 produces composite score; if >= 0.92, skill passes C4 tournament review. If < 0.92, revision cycle begins.
4. **Persistence:** All strategy outputs (findings, critiques, scores) persisted to project work directory

---

**Selection Plan Version:** 1.0
**SSOT Reference:** `.context/rules/quality-enforcement.md` (Criticality Levels, Strategy Catalog, Auto-Escalation Rules)
**Agent:** adv-selector (v1.0.0)
**Timestamp:** 2026-08-07
**H-23 Compliance:** Navigation table included; anchor links verified

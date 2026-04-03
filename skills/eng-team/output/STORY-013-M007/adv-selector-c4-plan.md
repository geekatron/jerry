# Strategy Selection Plan — M-007 disallowedTools Fix

> **Agent:** adv-selector (Strategy Selector)
> **Task:** Map C4 criticality level to adversarial strategy set per SSOT
> **Deliverable:** M-007 fix (disallowedTools Task→Agent rename across 11 UX agent definition files)
> **Output Level:** L1 (Technical)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Criticality Assessment](#criticality-assessment) | Requested level, auto-escalation check, final level |
| [Selected Strategies (Ordered)](#selected-strategies-ordered) | All 10 strategies in execution sequence |
| [H-16 Compliance](#h-16-compliance) | Steelman-before-Devil's-Advocate enforcement |
| [Strategy Overrides Applied](#strategy-overrides-applied) | User overrides and P-020 compliance |

---

## Criticality Assessment

| Field | Value |
|-------|-------|
| **Requested Level** | C4 (Critical) |
| **Deliverable Type** | Code Modification (UX agent definition files) |
| **Deliverable Path** | `skills/ux-orchestrator/agents/`, `skills/ux-*/agents/` (11 files) |
| **Auto-Escalation Applied** | No |
| **Auto-Escalation Check** | AE-001: Not touching constitution. AE-002: Not touching .context/rules/. AE-003: Not an ADR. AE-004: Not modifying baselined ADR. AE-005: Not security-relevant code. All AE rules checked — none triggered. |
| **Final Level** | **C4** |

**Rationale:** The task modifies 11 agent definition files (UX skill agents). Agent definitions in `skills/*/agents/` are part of the governance layer per agent-development-standards.md H-34 enforcement. Changes to agent governance files, while not touching the constitutional file itself or .context/rules/, represent high-impact structural changes affecting multiple agents (11 files spanning 6 skill agents). The change pattern (disallowedTools: Task→Agent rename) is a schema-breaking modification that cascades across all agent definitions. User has explicitly assigned C4 criticality. No auto-escalation rules trigger; this remains C4 as requested.

---

## Selected Strategies (Ordered)

All 10 selected strategies per quality-enforcement.md C4 requirement. Ordered per H-16 constraint (Steelman before Devil's Advocate) and recommended execution order (Groups A-F).

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional |
|-------|-------------|---------------|---------------|-------------------|
| **1** | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Required (Group A) |
| **2** | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Required (Group B — H-16 enforces S-003 before S-002) |
| **3** | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required (Group C — H-16 satisfied: S-003 at pos 2, S-002 at pos 3) |
| **4** | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | Required (Group C) |
| **5** | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | Required (Group C) |
| **6** | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required (Group D) |
| **7** | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | Required (Group D) |
| **8** | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | Required (Group E) |
| **9** | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | Required (Group E) |
| **10** | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required (Group F — ALWAYS LAST) |

### Execution Groups

**Group A — Self-Review (H-15):**
- S-010 (Self-Refine) — Creator reviews own work for obvious defects before critic invocation

**Group B — Strengthen (H-16 Phase 1):**
- S-003 (Steelman Technique) — Find strongest possible version of the change before any critique

**Group C — Challenge (H-16 Phase 2 + Role-Based):**
- S-002 (Devil's Advocate) — Attack assumptions after steelman phase (H-16 satisfied)
- S-004 (Pre-Mortem Analysis) — Identify failure modes and risks
- S-001 (Red Team Analysis) — Offensive security testing of the agent definition changes

**Group D — Verify (Compliance & Consistency):**
- S-007 (Constitutional AI Critique) — Verify H-34 schema compliance, P-003/P-020/P-022 adherence across all 11 files
- S-011 (Chain-of-Verification) — Cross-file consistency verification; ensure rename applied uniformly

**Group E — Decompose (Structured Analysis):**
- S-012 (FMEA) — Failure mode analysis for disallowedTools Task/Agent semantics across agent invocation patterns
- S-013 (Inversion Technique) — Invert: what would break if the rename is NOT applied? What if applied inconsistently?

**Group F — Score (Quality Gate):**
- S-014 (LLM-as-Judge) — Quantitative scoring against 6-dimension rubric (completeness, consistency, rigor, evidence, actionability, traceability). Quality threshold: >= 0.95 per task context.

---

## H-16 Compliance

| Constraint | Status | Evidence |
|-----------|--------|----------|
| **S-003 position** | Position 2 | Steelman Technique appears at order position 2 |
| **S-002 position** | Position 3 | Devil's Advocate appears at order position 3 |
| **Constraint satisfied** | ✓ **YES** | S-003 (pos 2) executes BEFORE S-002 (pos 3). H-16 constraint enforced. |

**Rationale:** The H-16 constraint (HARD rule, line 62 in quality-enforcement.md) mandates that Steelman (S-003) must be applied before Devil's Advocate (S-002) to prevent premature rejection of sound approaches. The ordering above satisfies this by:

1. Completing Group B (Strengthen) with S-003 before advancing to Group C
2. Executing S-002 only after S-003 has identified the strongest version of the change
3. This two-phase approach (strengthen → then challenge) ensures the tournament evaluates the change on its merits, not on initial presentation defects

---

## Strategy Overrides Applied

| Override | Status | Reason |
|----------|--------|--------|
| **User-specified additions** | None | No overrides requested |
| **User-specified removals** | None | No overrides requested |
| **P-020 Compliance** | ✓ Confirmed | User explicitly assigned C4 criticality; this plan honors that authority. No user-required strategies were removed. |

**Note:** No user overrides were provided in the ADV CONTEXT. The strategy set is fixed per the C4 criticality level per quality-enforcement.md line 155: "All 10 selected" with "Optional: None". All 10 strategies are REQUIRED for C4 deliverables.

---

## Summary

**Execution Plan:**
- **Strategy Set:** All 10 selected strategies (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)
- **Execution Sequence:** 10-strategy tournament in Groups A-F per recommended order
- **H-16 Constraint:** Satisfied — S-003 at position 2, S-002 at position 3
- **Quality Threshold:** >= 0.95 per task context (higher than standard 0.92 for C4 governance changes)
- **Next Step:** Invoke `/adversary` skill with adv-executor agent to execute templates in listed order against the 11 UX agent definition files

**Template Files Ready:**
All 10 template files verified to exist in `.context/templates/adversarial/`:
- `s-001-red-team.md` ✓
- `s-002-devils-advocate.md` ✓
- `s-003-steelman.md` ✓
- `s-004-pre-mortem.md` ✓
- `s-007-constitutional-ai.md` ✓
- `s-010-self-refine.md` ✓
- `s-011-cove.md` ✓
- `s-012-fmea.md` ✓
- `s-013-inversion.md` ✓
- `s-014-llm-as-judge.md` ✓

---

*Plan generated by adv-selector (Strategy Selector agent)*
*SSOT Reference: `.context/rules/quality-enforcement.md` [Criticality Levels, Strategy Catalog, H-16 ordering]*
*Date: 2026-03-29*
*Constitutional Compliance: H-13 (quality gate), H-14 (iteration cycle), H-15 (self-review), H-16 (ordering), H-17 (scoring), H-18 (constitutional check), H-19 (escalation)*

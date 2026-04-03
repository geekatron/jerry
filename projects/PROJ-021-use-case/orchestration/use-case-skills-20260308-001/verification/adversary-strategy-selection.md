# Adversarial Strategy Selection Plan

**PROJ-021-use-case Final Verification Review**

---

## Criticality Assessment

**Requested Level:** C3 (Significant)

**Auto-Escalation Applied:** No — Requested level is appropriate

**Final Level:** C3 (Significant)

---

## Auto-Escalation Analysis

The adv-selector agent actively checked all AE rules per H-19:

| Rule | Condition Check | Result | Impact |
|------|-----------------|--------|--------|
| AE-001 | Touches `docs/governance/JERRY_CONSTITUTION.md`? | No | — |
| AE-002 | Touches `.context/rules/` or `.claude/rules/`? | No (rule files are in skills/*/rules/, not .context/rules/) | — |
| AE-003 | New or modified ADR? | No (no ADR deliverables) | — |
| AE-004 | Modifies baselined ADR? | No | — |
| AE-005 | Security-relevant code? | No | — |
| AE-006 | Token exhaustion at C3+ criticality? | No (context within normal limits) | — |

**Escalation Decision:** None required. Requested C3 stands as final criticality.

**Rationale for C3 (not C2):** Per quality-enforcement.md Criticality Levels table:
- Scope: PROJ-021 affects >10 files (3 new skills + rule files + schemas + samples = 50+ files)
- Time to reverse: >1 day (involves skill architecture, agent definitions, registration)
- Impact: API changes (new skill interfaces, schema-driven agents)
- Requirements: All tiers of enforcement required (HARD + MEDIUM + SOFT)

---

## C3 Strategy Set Mapping

Per quality-enforcement.md Criticality Levels table for C3:

**Required strategies (must apply):**
- S-007 (Constitutional AI Critique) — Verify governance compliance
- S-002 (Devil's Advocate) — Challenge assumptions in skill design
- S-014 (LLM-as-Judge) — Quantitative quality scoring
- S-004 (Pre-Mortem Analysis) — Identify failure modes in skill architecture
- S-012 (FMEA) — Risk assessment across skill integration
- S-013 (Inversion Technique) — Decompose complex skill interactions

**Optional strategies (may apply if needed):**
- S-001 (Red Team Analysis) — Security assessment of agent definitions
- S-003 (Steelman Technique) — Strengthen skill architecture rationale
- S-010 (Self-Refine) — Self-correction before critic review
- S-011 (Chain-of-Verification) — Cross-verification of artifacts

**Total: 6 required + 4 optional = 10 selected strategies available**

---

## Selected Strategies (Ordered)

Execution order enforces H-16 constraint: S-003 (Steelman) BEFORE S-002 (Devil's Advocate).

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional | Rationale |
|-------|-------------|---------------|---------------|-------------------|-----------|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Optional | Self-review before presentation per H-15; establishes baseline quality before external critique |
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Optional (H-16 ordering) | Strengthen skill architecture rationale and agent design patterns before attack phase; required prior to S-002 |
| 3 | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required (C3) | Challenge core assumptions in 3-skill decomposition, agent coordination, schema design decisions |
| 4 | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | Required (C3) | Identify failure scenarios in skill integration, agent dependencies, orchestration handoffs |
| 5 | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | Optional | Security assessment: agent definition attack surface, constitutional compliance in guardails, schema injection risks |
| 6 | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required (C3) | Verify P-003 (no recursive subagents in agent designs), P-020 (user authority in skill boundaries), P-022 (no deception in agent descriptions) |
| 7 | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | Optional | Cross-verify artifact coherence: agent defs ↔ governance files ↔ skill registration ↔ schemas |
| 8 | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | Required (C3) | Failure modes analysis: agent signature mismatches, schema drift, skill orchestration breakpoints |
| 9 | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | Required (C3) | Invert relationships: What if agents fail? What if schema changes? What if registration is incomplete? |
| 10 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required (C3, ALWAYS LAST) | Quantitative scoring against 6-dimension rubric: Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability |

---

## H-16 Compliance Check

**H-16 Constraint:** S-003 (Steelman) MUST be ordered BEFORE S-002 (Devil's Advocate).

- S-003 position in execution order: **2**
- S-002 position in execution order: **3**
- **Constraint satisfied: YES** — S-003 (position 2) comes before S-002 (position 3)

---

## Strategy Overrides Applied

**User overrides:** None requested

**Default application:** All 6 required strategies (C3 mapping per quality-enforcement.md table) are included. 4 optional strategies selected based on skill scope complexity:
- S-010 (Self-Refine) — Essential for H-15 compliance before critic review
- S-003 (Steelman) — Required by H-16 ordering (prerequisite to S-002)
- S-001 (Red Team) — Recommended for agent definition security assessment
- S-011 (Chain-of-Verification) — Recommended for artifact coherence validation

**No required strategies removed.**

---

## Execution Context

**Deliverable Scope:**
- 3 new skills: /use-case, /test-spec, /contract-design
- 6 agents (2 per skill): uc-author, uc-slicer, tspec-generator, tspec-analyst, cd-generator, cd-validator
- 3 rule files: use-case-writing-rules.md, clark-transformation-rules.md, uc-to-contract-rules.md
- 3 JSON schemas: use-case-realization-v1.schema.json, test-specification-v1.schema.json, contract-design-v1.schema.json
- 6 sample artifacts (one per agent)
- Governance files: SKILL.md (3×), agent .md files (6×), .governance.yaml (6×)

**Quality Gate:** >= 0.92 composite score (H-13)

**Minimum iterations:** 3 creator-critic-revision cycles (H-14)

**Assessment scope:** Agent definitions (H-34 compliance), skill registration (H-26 compliance), artifact coherence, schema correctness

---

## Pre-Execution Verification (H-15 Self-Review)

Before invoking the strategy execution phase, verify:

- [ ] All 10 strategy IDs are valid (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)
- [ ] H-16 ordering satisfied: S-003 (pos 2) before S-002 (pos 3)
- [ ] Auto-escalation rules checked: no auto-C3/C4 conditions triggered
- [ ] User overrides documented: none applied
- [ ] Template paths verified: all 10 templates exist in `.context/templates/adversarial/`
- [ ] Deliverable paths identified: skills/use-case/, skills/test-spec/, skills/contract-design/
- [ ] Final criticality locked: C3 (Significant)

**Self-review result: READY FOR EXECUTION**

---

## Operational Notes

1. **Strategy execution order is deterministic** — Strategies execute in the table order (1-10) with no branching or conditional logic.

2. **S-014 (LLM-as-Judge) is always last** — Per quality-enforcement.md Implementation section, LLM-as-Judge scoring must occur after all other strategies complete to avoid anchoring effects.

3. **Quality gate threshold: 0.92** — Per H-13, deliverables scoring below 0.92 composite are REJECTED and must be revised. Minimum 3 iterations required per H-14.

4. **Context isolation** — If individual agents (uc-author, uc-slicer, etc.) require isolated C3 review, invoke via /adversary skill Task tool for fresh context per FC-M-001 (agent-development-standards.md).

5. **Handoff protocol** — If strategies produce intermediate artifacts, validate against handoff schema (agent-development-standards.md Handoff Protocol section).

---

## Files Referenced

| File | Purpose |
|------|---------|
| `.context/rules/quality-enforcement.md` | SSOT for criticality levels, strategy catalog, threshold definitions |
| `.context/rules/agent-development-standards.md` | H-34 agent definition standards, H-16 ordering, handoff protocol |
| `.context/templates/adversarial/s-{NNN}-{slug}.md` | Strategy execution templates (10 total) |
| `skills/use-case/SKILL.md` | Skill registration and agent list |
| `skills/test-spec/SKILL.md` | Skill registration and agent list |
| `skills/contract-design/SKILL.md` | Skill registration and agent list |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/` | Deliverable artifacts for review |

---

**Strategy Selection Plan Status: FINALIZED**

**Plan created:** 2026-03-11

**Criticality Level: C3 (Significant)**

**Enforcement: All tiers (HARD + MEDIUM + SOFT)**

**Execution entry point:** `/adversary` skill with `adv-executor` agent

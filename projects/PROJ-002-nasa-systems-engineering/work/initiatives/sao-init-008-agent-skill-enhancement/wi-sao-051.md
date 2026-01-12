---
id: wi-sao-051
title: "Compliance Check: NASA/Anthropic Standards"
status: OPEN
parent: "_index.md"
initiative: sao-init-008
children: []
depends_on:
  - wi-sao-050
blocks:
  - wi-sao-052
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "3-4h"
entry_id: sao-051
token_estimate: 500
---

# WI-SAO-051: Compliance Check - NASA/Anthropic Standards

> **Status:** 📋 OPEN
> **Priority:** P1 (Phase 2 Analysis)
> **Pipeline Pattern:** Pattern 2 (Sequential) - Analysis Step 2

---

## Description

Verify that current agent definitions comply with relevant standards: Anthropic best practices, NASA SE standards (for nse-* agents), and Jerry Constitution principles. Document compliance status and required fixes.

---

## Acceptance Criteria

1. [ ] Anthropic compliance verified for all agents
2. [ ] NASA SE compliance verified for nse-* agents
3. [ ] Jerry Constitution compliance verified for all agents
4. [ ] Compliance reports created with fix recommendations

---

## Tasks

### T-051.1: Anthropic Compliance

- [ ] **T-051.1.1:** Verify agent prompts follow Claude best practices
- [ ] **T-051.1.2:** Verify XML/structured prompting used appropriately
- [ ] **T-051.1.3:** Verify guardrails section exists and is adequate
- [ ] **T-051.1.4:** Verify tool descriptions are well-formed
- [ ] **T-051.1.5:** Document compliance in `analysis/sao-051-anthropic.md`

### T-051.2: NASA SE Compliance (nse-* only)

- [ ] **T-051.2.1:** Verify nse-* agents align with NPR 7123.1
- [ ] **T-051.2.2:** Verify technical review types are accurate and complete
- [ ] **T-051.2.3:** Verify terminology matches NASA standards
- [ ] **T-051.2.4:** Verify SE process references are current
- [ ] **T-051.2.5:** Document compliance in `analysis/sao-051-nasa.md`

### T-051.3: Jerry Constitution Compliance

- [ ] **T-051.3.1:** Verify all agents comply with P-003 (no recursive subagents)
- [ ] **T-051.3.2:** Verify agents support P-002 (file persistence)
- [ ] **T-051.3.3:** Verify agents don't violate P-022 (no deception)
- [ ] **T-051.3.4:** Document compliance in `analysis/sao-051-constitution.md`

---

## Compliance Standards

### Anthropic Standards

| Standard | Description | Verification Method |
|----------|-------------|---------------------|
| XML Structure | Use XML tags for prompt organization | Check for `<identity>`, `<instructions>`, etc. |
| Guardrails | Non-negotiable rules section | Check for guardrails/constraints section |
| Tool Design | Self-contained, robust, clear intent | Review tool descriptions |
| Examples | Concrete demonstrations | Check for examples section |

### NASA SE Standards (nse-* only)

| Standard | Description | Verification Method |
|----------|-------------|---------------------|
| NPR 7123.1 | SE procedural requirements | Verify process references |
| Review Gates | SRR, PDR, CDR, etc. | Verify gate definitions |
| Terminology | NASA standard terms | Cross-reference with handbook |

### Jerry Constitution Principles

| Principle | Description | Verification Method |
|-----------|-------------|---------------------|
| P-002 | File Persistence | Check for file output patterns |
| P-003 | No Recursive Subagents | No Task() calls within agents |
| P-022 | No Deception | No misleading outputs |

---

## Expected Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Anthropic compliance | `analysis/sao-051-anthropic.md` | Claude best practices check |
| NASA SE compliance | `analysis/sao-051-nasa.md` | NPR 7123.1 alignment |
| Constitution compliance | `analysis/sao-051-constitution.md` | Jerry principles check |

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-051-001 | Check | Anthropic compliance verified | ⏳ Pending |
| E-051-002 | Check | NASA SE compliance verified | ⏳ Pending |
| E-051-003 | Check | Constitution compliance verified | ⏳ Pending |
| E-051-004 | Artifact | Compliance reports created | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
*Created: 2026-01-12*

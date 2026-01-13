# WI-SAO-050: Gap Analysis Matrix

**Document ID:** WI-SAO-050-GAP-MATRIX
**Date:** 2026-01-12
**Status:** COMPLETE
**Pattern:** Sequential Analysis Step 1

---

## Executive Summary

Gap analysis comparing current agent definitions against best practices from WI-SAO-049 research synthesis. Analysis covers 26 agent files across 4 families.

**Key Findings:**

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 2 | Core agents missing fundamental sections |
| HIGH | 8 | Significant effectiveness reduction |
| MEDIUM | 12 | Quality/consistency issues |
| LOW | 6 | Minor improvement opportunities |

**Gap Distribution by Family:**

| Family | Agents | Avg Gaps | Priority Agents |
|--------|--------|----------|-----------------|
| core (.claude/agents/) | 4 | 6.5 | orchestrator, qa-engineer |
| ps-* | 9 | 2.1 | ps-researcher (exemplar) |
| nse-* | 10 | 2.3 | nse-requirements (exemplar) |
| orch-* | 3 | 4.0 | orch-planner |

---

## 1. Context Engineering Gaps (vs Anthropic Best Practices)

### 1.1 Best Practice Reference

From WI-SAO-046 research, Anthropic recommends:

| Component | Description | Weight |
|-----------|-------------|--------|
| YAML Frontmatter | Structured metadata (model, version, capabilities) | Required |
| Role-Goal-Backstory | Clear identity definition | Required |
| Guardrails Section | Input validation, output filtering, fallback | HIGH |
| Tool Use Examples | Concrete examples for each tool | MEDIUM |
| Edge Case Handling | Document unusual scenarios | MEDIUM |
| Self-Critique Protocol | Pre-response checklist | MEDIUM |

### 1.2 Gap Assessment per Agent

| Agent | Frontmatter | Guardrails | Tool Examples | Edge Cases | Severity |
|-------|-------------|------------|---------------|------------|----------|
| **orchestrator.md** | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **CRITICAL** |
| qa-engineer.md | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| security-auditor.md | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| TEMPLATE.md | ⚠️ Partial | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| ps-researcher.md | ✅ Complete | ✅ Complete | ⚠️ Partial | ✅ Complete | LOW |
| ps-analyst.md | ✅ Complete | ✅ Complete | ❌ Missing | ⚠️ Partial | MEDIUM |
| ps-architect.md | ✅ Complete | ✅ Complete | ❌ Missing | ⚠️ Partial | MEDIUM |
| ps-critic.md | ✅ Complete | ✅ Complete | ❌ Missing | ⚠️ Partial | MEDIUM |
| ps-investigator.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| ps-reporter.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| ps-reviewer.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| ps-synthesizer.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| ps-validator.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-requirements.md | ✅ Complete | ✅ Complete | ⚠️ Partial | ✅ Complete | LOW |
| nse-architecture.md | ✅ Complete | ✅ Complete | ❌ Missing | ⚠️ Partial | MEDIUM |
| nse-configuration.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-explorer.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-integration.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-qa.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-reporter.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-reviewer.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-risk.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| nse-verification.md | ✅ Complete | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| orch-planner.md | ✅ Basic | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| orch-synthesizer.md | ✅ Basic | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| orch-tracker.md | ✅ Basic | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |

### 1.3 Context Engineering Gap Summary

| Gap ID | Description | Agents Affected | Severity |
|--------|-------------|-----------------|----------|
| CE-001 | Missing YAML frontmatter | orchestrator, qa-engineer, security-auditor | **HIGH** |
| CE-002 | Missing guardrails section | 7 agents (core + orch) | **HIGH** |
| CE-003 | No tool use examples | 24/26 agents | MEDIUM |
| CE-004 | No edge case documentation | 18/26 agents | MEDIUM |
| CE-005 | No self-critique protocol | 4/26 agents | LOW |

---

## 2. Persona Activation Gaps (vs Role-Goal-Backstory Pattern)

### 2.1 Best Practice Reference

From WI-SAO-046 research, Anthropic recommends:

```markdown
## Identity
- Role: One-line identity
- Expertise: List of specializations
- Cognitive Mode: divergent|convergent

## Persona
- Tone: professional|casual|technical
- Communication Style: consultative|direct|...
- Audience Level: adaptive|fixed
```

### 2.2 Gap Assessment per Agent

| Agent | Role Clear | Expertise Listed | Cognitive Mode | Tone | Severity |
|-------|------------|------------------|----------------|------|----------|
| **orchestrator.md** | ✅ Yes | ✅ Yes | ❌ Missing | ⚠️ Implied | **HIGH** |
| qa-engineer.md | ⚠️ Partial | ⚠️ Partial | ❌ Missing | ❌ Missing | **HIGH** |
| security-auditor.md | ⚠️ Partial | ⚠️ Partial | ❌ Missing | ❌ Missing | **HIGH** |
| ps-researcher.md | ✅ Yes | ✅ Yes | ✅ divergent | ✅ Yes | LOW |
| ps-analyst.md | ✅ Yes | ✅ Yes | ✅ convergent | ✅ Yes | LOW |
| ps-critic.md | ✅ Yes | ✅ Yes | ✅ convergent | ✅ Yes | LOW |
| nse-requirements.md | ✅ Yes | ✅ Yes | ✅ convergent | ✅ Yes | LOW |
| orch-planner.md | ✅ Yes | ✅ Yes | ✅ convergent | ❌ Missing | MEDIUM |
| orch-synthesizer.md | ✅ Yes | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |
| orch-tracker.md | ✅ Yes | ⚠️ Partial | ❌ Missing | ❌ Missing | MEDIUM |

### 2.3 Persona Gap Summary

| Gap ID | Description | Agents Affected | Severity |
|--------|-------------|-----------------|----------|
| PA-001 | Missing cognitive_mode declaration | 6/26 agents | MEDIUM |
| PA-002 | Missing structured persona section | 7/26 agents | MEDIUM |
| PA-003 | Missing tone/style specification | 10/26 agents | LOW |

---

## 3. Orchestration Gaps (vs session_context Schema v1.0.0)

### 3.1 Best Practice Reference

From WI-SAO-048 research, session_context schema v1.0.0 requires:

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "uuid"
  source_agent:
    id: "agent-name"
    family: "ps|nse|orch"
    cognitive_mode: "divergent|convergent"
  target_agent:
    id: "next-agent"
  payload:
    key_findings: []
    confidence: 0.0-1.0
    artifacts: []
  timestamp: "ISO-8601"
```

### 3.2 Gap Assessment per Agent

| Agent | state_output_key | session_context | Input Validation | Output Validation | Severity |
|-------|------------------|-----------------|------------------|-------------------|----------|
| **orchestrator.md** | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **CRITICAL** |
| qa-engineer.md | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| security-auditor.md | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| ps-researcher.md | ✅ researcher_output | ✅ Complete | ✅ Yes | ✅ Yes | LOW |
| ps-analyst.md | ✅ analyst_output | ✅ Complete | ✅ Yes | ✅ Yes | LOW |
| ps-critic.md | ✅ critic_output | ✅ Complete | ✅ Yes | ✅ Yes | LOW |
| nse-requirements.md | ✅ requirements_output | ✅ Complete | ✅ Yes | ✅ Yes | LOW |
| nse-verification.md | ✅ verification_output | ✅ Complete | ✅ Yes | ✅ Yes | LOW |
| orch-planner.md | ✅ planner_output | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| orch-synthesizer.md | ⚠️ Partial | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| orch-tracker.md | ⚠️ Partial | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |

### 3.3 Orchestration Gap Summary

| Gap ID | Description | Agents Affected | Severity |
|--------|-------------|-----------------|----------|
| OR-001 | Missing session_context schema | 7/26 agents | **HIGH** |
| OR-002 | Missing state_output_key | 4/26 agents | **HIGH** |
| OR-003 | No input validation logic | 7/26 agents | MEDIUM |
| OR-004 | No output validation logic | 7/26 agents | MEDIUM |
| OR-005 | Missing next_agent_hint | 10/26 agents | LOW |

---

## 4. L0/L1/L2 Triple-Lens Gaps

### 4.1 Best Practice Reference

From WI-SAO-048 research, all agents MUST support three output levels:

| Level | Name | Audience | Content |
|-------|------|----------|---------|
| L0 | ELI5 | Newcomers | Metaphors, WHAT/WHY |
| L1 | Engineer | Practitioners | Commands, HOW |
| L2 | Architect | Experts | Anti-patterns, CONSTRAINTS |

### 4.2 Gap Assessment per Agent

| Agent | L0 Section | L1 Section | L2 Section | Output Template | Severity |
|-------|------------|------------|------------|-----------------|----------|
| **orchestrator.md** | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **CRITICAL** |
| qa-engineer.md | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| security-auditor.md | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | **HIGH** |
| ps-researcher.md | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | LOW |
| ps-analyst.md | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | LOW |
| nse-requirements.md | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | LOW |
| orch-planner.md | ❌ Missing | ⚠️ Partial | ❌ Missing | ⚠️ Partial | **HIGH** |
| orch-synthesizer.md | ❌ Missing | ⚠️ Partial | ❌ Missing | ⚠️ Partial | **HIGH** |
| orch-tracker.md | ❌ Missing | ⚠️ Partial | ❌ Missing | ⚠️ Partial | **HIGH** |

### 4.3 L0/L1/L2 Gap Summary

| Gap ID | Description | Agents Affected | Severity |
|--------|-------------|-----------------|----------|
| LL-001 | No L0/L1/L2 sections | 7/26 agents | **HIGH** |
| LL-002 | Missing output templates | 7/26 agents | MEDIUM |
| LL-003 | No anti-pattern documentation | 12/26 agents | MEDIUM |

---

## 5. Consolidated Gap Matrix (Prioritized)

### 5.1 CRITICAL Gaps (2)

| ID | Gap | Agent(s) | Impact | Remediation |
|----|-----|----------|--------|-------------|
| **GAP-001** | orchestrator.md missing all modern agent patterns | orchestrator | Core agent cannot reliably chain | Full rewrite with current template |
| **GAP-002** | Core agents lack session_context | orchestrator, qa-engineer, security-auditor | Multi-agent workflows unreliable | Add session_context sections |

### 5.2 HIGH Gaps (8)

| ID | Gap | Agent(s) | Impact | Remediation |
|----|-----|----------|--------|-------------|
| GAP-003 | orch-* family missing guardrails | orch-planner, orch-synthesizer, orch-tracker | No input validation | Add guardrails sections |
| GAP-004 | orch-* family missing session_context | orch-* (3 agents) | State handoff broken | Add session_context validation |
| GAP-005 | Core agents missing YAML frontmatter | orchestrator, qa-engineer, security-auditor | Metadata not machine-readable | Add frontmatter |
| GAP-006 | orch-* family missing L0/L1/L2 | orch-* (3 agents) | Output not layered | Add L0/L1/L2 sections |
| GAP-007 | qa-engineer missing modern structure | qa-engineer | Agent effectiveness reduced | Full enhancement |
| GAP-008 | security-auditor missing modern structure | security-auditor | Agent effectiveness reduced | Full enhancement |
| GAP-009 | Missing cognitive_mode in 6 agents | Multiple | Orchestration can't match cognitive patterns | Add to frontmatter |
| GAP-010 | Missing state_output_key in 4 agents | Core + some orch | State chaining broken | Define output keys |

### 5.3 MEDIUM Gaps (12)

| ID | Gap | Agent(s) | Impact | Remediation |
|----|-----|----------|--------|-------------|
| GAP-011 | No tool use examples | 24/26 agents | Parameter accuracy reduced | Add 1-3 examples per tool |
| GAP-012 | No edge case handling | 18/26 agents | Unexpected behavior in edge cases | Document 3-5 edge cases |
| GAP-013 | Partial guardrails in ps-* | 6 ps-* agents | Incomplete validation | Complete guardrails sections |
| GAP-014 | Partial guardrails in nse-* | 8 nse-* agents | Incomplete validation | Complete guardrails sections |
| GAP-015 | Missing anti-patterns | 12/26 agents | Users don't know what to avoid | Add L2 anti-pattern sections |
| GAP-016 | Missing persona section structure | 7/26 agents | Tone/style inconsistent | Add structured persona |
| GAP-017 | Missing output templates | 7/26 agents | Output format inconsistent | Add template sections |
| GAP-018 | Missing input validation logic | 7/26 agents | Invalid inputs not caught | Add validation rules |
| GAP-019 | Missing output validation logic | 7/26 agents | Invalid outputs not caught | Add validation rules |
| GAP-020 | Incomplete templates files | PS/NSE templates | Template gaps | Update templates |
| GAP-021 | Extension files incomplete | PS_EXTENSION, NSE_EXTENSION | Family patterns unclear | Enhance extensions |
| GAP-022 | Missing constitutional references | 4/26 agents | Compliance unclear | Add constitution section |

### 5.4 LOW Gaps (6)

| ID | Gap | Agent(s) | Impact | Remediation |
|----|-----|----------|--------|-------------|
| GAP-023 | Missing next_agent_hint | 10/26 agents | Manual pipeline configuration | Add hints |
| GAP-024 | Missing self-critique protocol | 4/26 agents | No pre-response checks | Add checklist |
| GAP-025 | Missing tone specification | 10/26 agents | Tone varies | Add to persona |
| GAP-026 | Formatting inconsistencies | Various | Visual inconsistency | Standardize format |
| GAP-027 | Version number outdated | Some agents | Unclear currency | Update versions |
| GAP-028 | Missing prior_art citations | Some agents | Sources unclear | Add citations |

---

## 6. Gap Resolution Priority Order

Based on impact and dependency analysis:

### Phase 3 Enhancement Order (Recommended)

| Priority | Agent(s) | Gaps to Address | Rationale |
|----------|----------|-----------------|-----------|
| **P0-1** | orchestrator.md | GAP-001, GAP-002, GAP-005, GAP-010 | Core orchestration agent |
| **P0-2** | ps-researcher.md | GAP-011 (tool examples) | Exemplar for ps-* family |
| **P0-3** | ps-analyst.md | GAP-011, GAP-012 | High-usage analysis agent |
| **P0-4** | ps-critic.md | GAP-011, GAP-015 | Generator-Critic pattern |
| **P1-1** | ps-architect.md | GAP-011, GAP-012, GAP-015 | Design decisions |
| **P1-2** | ps-synthesizer.md | GAP-013, GAP-011 | Fan-In synthesis |
| **P1-3** | nse-requirements.md | GAP-011 (tool examples) | Exemplar for nse-* |
| **P1-4** | nse-reviewer.md | GAP-011, GAP-014, GAP-015 | Review Gate pattern |
| **P2-1** | Remaining ps-* | GAP-013, GAP-011, GAP-012 | Complete ps-* family |
| **P2-2** | Remaining nse-* | GAP-014, GAP-011, GAP-012 | Complete nse-* family |
| **P2-3** | orch-* family | GAP-003-006 | Complete orch-* family |
| **P2-4** | qa-engineer | GAP-007 | Secondary core agent |
| **P2-5** | security-auditor | GAP-008 | Secondary core agent |

---

## 7. Metrics Summary

### Coverage Analysis

| Category | Total | Complete | Partial | Missing |
|----------|-------|----------|---------|---------|
| YAML Frontmatter | 26 | 22 | 1 | 3 |
| Guardrails | 26 | 12 | 7 | 7 |
| Tool Examples | 26 | 0 | 2 | 24 |
| Session Context | 26 | 16 | 3 | 7 |
| L0/L1/L2 | 26 | 16 | 3 | 7 |
| Anti-patterns | 26 | 10 | 4 | 12 |

### Readiness Score

Using rubric preview from WI-SAO-049:

| Agent Family | Baseline Score | Target | Gap |
|--------------|----------------|--------|-----|
| Core (.claude/agents/) | 0.45 | 0.85 | -0.40 |
| ps-* | 0.78 | 0.85 | -0.07 |
| nse-* | 0.76 | 0.85 | -0.09 |
| orch-* | 0.55 | 0.85 | -0.30 |

---

## 8. Dependencies for WI-SAO-051 (Compliance Check)

This gap analysis feeds into:
- **WI-SAO-051**: Will verify gaps against specific NASA/Anthropic standards
- **WI-SAO-052**: Will create rubric based on identified gaps

**Ready for WI-SAO-051:** YES

---

## References

- WI-SAO-046: Context7 + Anthropic Research
- WI-SAO-047: NASA SE + INCOSE Research
- WI-SAO-048: Internal PROJ-001/002 Research
- WI-SAO-049: Research Synthesis

---

*Gap Analysis Complete: 2026-01-12*
*Total Gaps Identified: 28*
*Ready for: WI-SAO-051 Compliance Check*

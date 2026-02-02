# EN-202:BUG-005: Mandatory Skill Usage Section Lost (108 Lines)

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-02 (Gap Analysis GAP-002)
PURPOSE: Document critical gap - Mandatory skill usage behavioral content completely lost
-->

> **Type:** bug
> **Status:** pending
> **Resolution:** -
> **Priority:** critical
> **Impact:** critical
> **Severity:** critical
> **Created:** 2026-02-02T05:00:00Z
> **Due:** 2026-02-03T00:00:00Z
> **Completed:** -
> **Parent:** EN-202
> **Owner:** Claude
> **Found In:** CLAUDE.md (rewritten)
> **Fix Version:** EN-202

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Reproduction Steps](#reproduction-steps) | How to identify the gap |
| [Environment](#environment) | System configuration |
| [Evidence](#evidence) | Gap analysis documentation |
| [Root Cause Analysis](#root-cause-analysis) | Cause identification |
| [Fix Description](#fix-description) | Required remediation |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Change log |
| [System Mapping](#system-mapping) | External system mappings |

---

## Summary

The "Mandatory Skill Usage (PROACTIVE)" section (lines 667-774, **108 lines**) was **COMPLETELY LOST** during the CLAUDE.md rewrite. This critical behavioral content instructs Claude to proactively invoke skills without waiting for user prompts. It includes trigger phrases, skill usage behavior rules, and concrete examples.

**Key Details:**
- **Symptom:** Claude will NOT proactively invoke `/problem-solving`, `/nasa-se`, or `/orchestration` skills
- **Frequency:** Every session - proactive skill invocation behavior is missing
- **Workaround:** None - users must explicitly invoke skills

---

## Reproduction Steps

### Prerequisites

Access to gap analysis traceability matrix and both CLAUDE.md versions.

### Steps to Reproduce

1. Open new CLAUDE.md (80 lines)
2. Search for "PROACTIVE" - no results
3. Search for "USE AUTOMATICALLY WHEN" - no results
4. Search for "Trigger Phrases" - no results
5. Check `.claude/rules/` for mandatory-skill-usage - does not exist
6. Compare with CLAUDE.md.backup lines 667-774 - content completely missing

### Expected Result

Mandatory skill usage behavioral guidance should be preserved either:
- In CLAUDE.md (condensed)
- In a dedicated `.claude/rules/mandatory-skill-usage.md` file
- In each skill's SKILL.md with proactive invocation section

### Actual Result

Content is completely missing. No migration target was created. Skills Quick Reference table exists but lacks proactive invocation instructions.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Any |
| **Browser/Runtime** | N/A (documentation file) |
| **Application Version** | CLAUDE.md (rewritten) |
| **Configuration** | Default |
| **Deployment** | Repository root |

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| Gap Analysis traceability-matrix.md | Report | GAP-002 identified (CRITICAL) | 2026-02-02 |
| CLAUDE.md.backup lines 667-774 | Source | Original 108 lines | 2026-02-02 |
| New CLAUDE.md | Verification | Content absent | 2026-02-02 |

### Lost Content (108 lines)

```markdown
## Mandatory Skill Usage (PROACTIVE)

> **CRITICAL:** You MUST use the following skills PROACTIVELY without waiting for the user to prompt you.
> These skills are designed to ensure quality, rigor, and traceability in all work.

### /problem-solving (MANDATORY for Research/Analysis)

**USE AUTOMATICALLY WHEN:**
- Starting ANY research or analysis task
- Investigating bugs, issues, or problems
- Performing root cause analysis
- Synthesizing findings from multiple sources
- Creating architecture decisions (ADRs)

**Provides:**
- 8 specialized agents: researcher, analyst, synthesizer, architect, reviewer, investigator, validator, reporter
- Structured frameworks: 5W2H, Ishikawa, Pareto, FMEA, 8D
- Evidence-based decision making with citations
- Persistent artifact generation

**Trigger Phrases (use skill automatically):**
- "research", "analyze", "investigate", "explore"
- "root cause", "why", "understand"
- "synthesize", "consolidate", "summarize findings"
- "review", "validate", "critique"

### @nasa-se (MANDATORY for Requirements/Design)

**USE AUTOMATICALLY WHEN:**
- Defining or analyzing requirements
- Creating design specifications
- Performing verification & validation
- Conducting technical reviews
- Managing system integration
- Risk management activities

**Provides:**
- NPR 7123.1D process implementation
- 10 specialized agents for systems engineering
- Requirements engineering rigor
- Verification/validation frameworks
- Technical review protocols
- Mission-grade quality practices

**Trigger Phrases (use skill automatically):**
- "requirements", "specification", "shall statements"
- "verification", "validation", "V&V"
- "technical review", "design review"
- "risk management", "FMEA"
- "system integration", "interface"

### @orchestration (MANDATORY for Multi-Step Workflows)

**USE AUTOMATICALLY WHEN:**
- Work involves multiple phases or stages
- Multiple agents need coordination
- Tasks have dependencies requiring sync barriers
- State must be checkpointed for recovery
- Cross-pollinated pipelines are needed

**Provides:**
- ORCHESTRATION_PLAN.md - Strategic workflow context
- ORCHESTRATION_WORKTRACKER.md - Tactical execution tracking
- ORCHESTRATION.yaml - Machine-readable state (SSOT)
- Sync barriers for parallel work coordination
- State checkpointing for resilience

**Trigger Phrases (use skill automatically):**
- "orchestration", "pipeline", "workflow"
- "multi-agent", "parallel", "coordinate"
- "sync barrier", "checkpoint"
- "phases", "stages", "gates"

### Skill Usage Behavior Rules

1. **DO NOT WAIT** for user to invoke skills - use them proactively when triggers apply
2. **COMBINE SKILLS** when appropriate (e.g., /orchestration + /problem-solving + /nasa-se for complex analysis)
3. **INVOKE EARLY** - Use skills at the start of work, not after struggling without them
4. **PERSIST ARTIFACTS** - All skill outputs must be persisted to the repository
5. **REFERENCE IN TODO** - Track skill invocations and outputs in your TODO list

### Example: Starting a New Feature

```
User: "Let's work on EN-004 Architecture Decisions"

Claude's Internal Process:
1. ✅ Invoke /orchestration - This has multiple ADRs requiring coordination
2. ✅ Invoke /problem-solving - Research and analysis needed for each ADR
3. ✅ Invoke /nasa-se - Architecture decisions require SE rigor
4. ✅ Create/update TODO with skill tracking
5. ✅ Proceed with coordinated execution
```
```

---

## Root Cause Analysis

### Root Cause

The "Mandatory Skill Usage (PROACTIVE)" section was not identified for extraction during the CLAUDE.md rewrite planning. It was neither:
1. Kept inline in the new CLAUDE.md
2. Extracted to a skill
3. Extracted to `.claude/rules/`

The section was simply omitted, resulting in complete data loss.

### Contributing Factors

- Focus on extracting worktracker content overshadowed other sections
- No comprehensive content inventory performed before rewrite
- EN-202 task list did not include "preserve mandatory skill usage" as a task
- Quick Reference skills table was created but lacks behavioral instructions

---

## Fix Description

### Solution Approach

Create `.claude/rules/mandatory-skill-usage.md` containing the proactive skill invocation rules. This file will be auto-loaded by Claude Code's `.claude/rules/` mechanism.

### Required Changes

1. Create `.claude/rules/mandatory-skill-usage.md` with full content
2. Include trigger phrase tables for each skill
3. Include the 5 behavior rules
4. Include the example workflow

### Target File

`.claude/rules/mandatory-skill-usage.md`

---

## Acceptance Criteria

### Fix Verification

- [ ] All proactive skill invocation rules preserved
- [ ] `/problem-solving` trigger phrases and USE AUTOMATICALLY WHEN preserved
- [ ] `/nasa-se` trigger phrases and USE AUTOMATICALLY WHEN preserved
- [ ] `/orchestration` trigger phrases and USE AUTOMATICALLY WHEN preserved
- [ ] All 5 Skill Usage Behavior Rules preserved
- [ ] Example workflow preserved
- [ ] File placed in `.claude/rules/` for auto-loading

### Quality Checklist

- [ ] Content matches original CLAUDE.md.backup lines 667-774
- [ ] Rules file follows `.claude/rules/` formatting conventions
- [ ] No behavioral requirements lost
- [ ] File is auto-loaded by Claude Code

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)

### Related Items

- **Gap Analysis:** [traceability-matrix.md](./gap-analysis/traceability-matrix.md) (GAP-002)
- **Original Source:** CLAUDE.md.backup lines 667-774
- **Skills Quick Reference:** CLAUDE.md lines 73-80 (incomplete without behavior rules)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T05:00:00Z | Claude | pending | Initial report from gap analysis (GAP-002) |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |

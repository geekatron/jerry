# INV-004: Cross-Artifact Consistency Validation

> **Investigation ID:** INV-004
> **Phase:** Artifact Integrity Phase 2
> **Date:** 2026-01-12
> **Investigator:** ps-investigator agent
> **Status:** COMPLETE

---

## L0: Summary

**Tests Run:** 4 consistency checks
**Passed:** 2
**Issues Found:** 2
**Critical Issues:** 0

Two consistency discrepancies identified: agent count mismatch between TOOL_REGISTRY and actual files, and incomplete AGENTS.md documentation.

---

## L1: Validation Results

### Check 1: Agent Count Consistency

| Source | Claimed Count | Actual Count | Status |
|--------|---------------|--------------|--------|
| TOOL_REGISTRY.yaml (total_agents) | 25 | 30 | MISMATCH |
| Core agents | 3 | 4 | MISMATCH |
| PS agents | 9 | 10 | MISMATCH |
| NSE agents | 10 | 12 | MISMATCH |
| Orch agents | 3 | 3 | MATCH |

**Root Cause:** File counts include TEMPLATE.md and EXTENSION.md files that are not "functional agents" but template/documentation files.

**Actual File Breakdown:**
- Core: orchestrator.md, qa-engineer.md, security-auditor.md, TEMPLATE.md (4 files)
- PS: 9 functional agents + PS_AGENT_TEMPLATE.md + PS_EXTENSION.md (11 files)
- NSE: 10 functional agents + NSE_AGENT_TEMPLATE.md + NSE_EXTENSION.md (12 files)
- Orch: 3 functional agents (3 files)

### Check 2: AGENTS.md Coverage

| Expected | Actual | Status |
|----------|--------|--------|
| All 25+ agents documented | 3 core agents only | MISMATCH |

**Finding:** AGENTS.md only documents core agents (Orchestrator, QA Engineer, Security Auditor). Missing 22+ skill agents from PS, NSE, and Orch families.

### Check 3: Version Consistency

| Schema | Location | Claimed Version | Verified |
|--------|----------|-----------------|----------|
| TOOL_REGISTRY.yaml | Line 14 | 1.0.0 | ✓ |
| PS_SKILL_CONTRACT.yaml | Line 4 | 1.0.0 | ✓ |
| NSE_SKILL_CONTRACT.yaml | Line 4 | 1.0.0 | ✓ |
| CROSS_SKILL_HANDOFF.yaml | Line 4 | 1.0.0 | ✓ |

**Status: PASS** - All versions consistent

### Check 4: Tool Count Consistency

| Source | Claimed | Actual | Status |
|--------|---------|--------|--------|
| TOOL_REGISTRY.yaml (total_tools) | 14 | 14 | MATCH |

**Status: PASS** - Tool count accurate

---

## L2: Detailed Findings

### F-001: Agent Count Includes Non-Functional Files

**Category:** documentation_debt
**Severity:** LOW
**Impact:** Metrics in TOOL_REGISTRY are unclear about scope

**Evidence:**
- TOOL_REGISTRY.yaml line 742-751 declares metrics
- total_agents: 25 excludes TEMPLATE and EXTENSION files
- Actual file count: 30 (includes templates/extensions)

**Recommendation:**
1. Clarify in TOOL_REGISTRY what counts as an "agent"
2. Add separate metrics: `agents_functional`, `agents_templates`, `agents_extensions`

### F-002: AGENTS.md Incomplete

**Category:** documentation_debt
**Severity:** MEDIUM
**Impact:** Users cannot discover skill-specific agents from central registry

**Evidence:**
- AGENTS.md documents only 3 core agents
- Missing: ps-researcher, ps-analyst, ps-architect, ps-critic, ps-validator, ps-synthesizer, ps-reviewer, ps-investigator, ps-reporter
- Missing: nse-requirements, nse-verification, nse-risk, nse-reviewer, nse-integration, nse-configuration, nse-architecture, nse-explorer, nse-qa, nse-reporter
- Missing: orch-planner, orch-tracker, orch-synthesizer

**Recommendation:**
1. Update AGENTS.md to document all agents
2. Organize by skill family with links to skill contracts
3. Or: Keep AGENTS.md for core agents only, reference skill contracts as SSOT

---

## Conclusion

**Result:** PARTIAL PASS

Cross-artifact consistency is **mostly good**:
- Version numbers are consistent across all schemas
- Tool counts are accurate
- Skill contract agent lists match actual files

**Documentation gaps exist**:
- Agent count metrics are ambiguous
- AGENTS.md is incomplete

**Recommended Action:** Create work item to update AGENTS.md and clarify TOOL_REGISTRY metrics.

---

## CORRECTION ADDENDUM (2026-01-12)

> **Status: F-002 FINDING WITHDRAWN**
> **Reviewer:** Human + Claude Opus 4.5
> **Date:** 2026-01-12

### F-002 Correction: AGENTS.md is NOT Incomplete

The original finding F-002 was **INCORRECT**. Upon manual review:

**Actual Architecture (By Design):**

| Agent Location | Count | Documentation Location |
|----------------|-------|------------------------|
| `.claude/agents/` | 3 (orchestrator, qa-engineer, security-auditor) | `AGENTS.md` ✓ |
| `skills/problem-solving/agents/` | 9 (ps-*) | `skills/problem-solving/SKILL.md` ✓ |
| `skills/nasa-se/agents/` | 10 (nse-*) | `skills/nasa-se/SKILL.md` ✓ |

**All 22 agents are fully documented** - just in their appropriate locations:
- Core framework agents → root `AGENTS.md`
- Skill-specific agents → skill's `SKILL.md`

This is **proper separation of concerns**, not a documentation gap.

**Evidence:**
- `skills/problem-solving/SKILL.md` lines 76-88: Full table of all 9 PS agents
- `skills/nasa-se/SKILL.md` lines 108-121: Full table of all 10 NSE agents
- `AGENTS.md` lines 39-70: Full documentation of 3 core agents

**Recommended Action:** NONE - WI-SAO-068 is **WITHDRAWN**

---

*Report Date: 2026-01-12*
*Investigation: INV-004*
*Agent: ps-investigator v2.1.0*
*Correction Added: 2026-01-12 by Claude Opus 4.5*

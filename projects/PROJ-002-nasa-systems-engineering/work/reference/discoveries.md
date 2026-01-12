---
id: ref-discoveries
title: "Project Discoveries"
type: reference
parent: "../WORKTRACKER.md"
related_work_items:
  - wi-sao-005  # DISCOVERY-001 caused cancellation
  - wi-sao-006  # DISCOVERY-001 caused cancellation
  - wi-sao-030  # DISCOVERY-004, DISCOVERY-005 observed
  - wi-sao-031  # DISCOVERY-005, DISCOVERY-006, DISCOVERY-007 observed
created: "2026-01-11"
last_updated: "2026-01-11"
token_estimate: 2800
---

# Discoveries

This document captures significant discoveries made during project execution that impacted planning, architecture, or work item status.

---

## DISCOVERY-001: nse-orchestrator/ps-orchestrator Architectural Misalignment

- **Discovered:** 2026-01-11
- **Severity:** CRITICAL (blocks WI-SAO-005, WI-SAO-006)
- **Discovery Context:** During pre-implementation analysis of WI-SAO-005
- **Finding:**

The originally planned `nse-orchestrator` and `ps-orchestrator` agents are architecturally incompatible with the Claude Code execution model and P-003 constraint.

**Key Insights:**

1. **P-003 Constraint (Hard):** Agents cannot spawn other agents. Maximum one level of nesting (orchestrator → worker).

2. **Claude Code Architecture:** The MAIN CONTEXT (Claude Code session itself) IS the orchestrator. From `skills/orchestration/SKILL.md` lines 87-101:
   ```
   MAIN CONTEXT (Claude) ← Orchestrator
       │
       ├──► orch-planner      (creates plan)
       ├──► ps-d-001          (Phase work)
       ├──► nse-f-001         (Phase work)
       ├──► orch-tracker      (updates state)
       └──► orch-synthesizer  (final synthesis)

   Each is a WORKER. None spawn other agents.
   ```

3. **Existing Solution:** The `orchestration` skill already provides the coordination mechanism via:
   - `orch-planner` - Creates execution plans
   - `orch-tracker` - Updates state checkpoints
   - `orch-synthesizer` - Final synthesis

4. **Original Intent Mismatch:** WI-SAO-005/006 attempted to create "orchestrator agents" that would coordinate other agents. This violates P-003 because:
   - An agent cannot delegate to or spawn other agents
   - Only the MAIN CONTEXT can invoke agents via the Task tool
   - "Delegation manifests" created by an agent would have no executor

**Research Sources:**
- skills/orchestration/SKILL.md (P-003 Compliance section)
- docs/governance/JERRY_CONSTITUTION.md (P-003 definition)
- ORCH-SKILL-003 (5W1H Analysis) - Established MAIN CONTEXT as sole orchestrator

**Resolution:** WI-SAO-005 and WI-SAO-006 CANCELLED. The orchestration skill already provides this capability correctly.

**Impact:**
- WI-SAO-005 → CANCELLED → moved to `wontdo/`
- WI-SAO-006 → CANCELLED → moved to `wontdo/`

---

## DISCOVERY-002: "Mixed" Cognitive Mode Not Academically Canonical

- **Discovered:** 2026-01-11
- **Severity:** MEDIUM (terminology issue)
- **Discovery Context:** User challenge during WI-SAO-005 planning
- **Finding:**

The cognitive mode "mixed" used in WI-SAO-005/006 acceptance criteria is NOT a formally recognized cognitive mode in academic literature.

**Canonical Cognitive Modes (Research):**

| Mode | Origin | Year | Description |
|------|--------|------|-------------|
| **Divergent** | J.P. Guilford | 1956 | Generating multiple creative solutions |
| **Convergent** | J.P. Guilford | 1956 | Finding the single best solution |
| **Lateral** | Edward de Bono | 1967 | Indirect, creative approach; restructuring |

**Academic Sources:**
- Guilford, J.P. (1956). "The structure of intellect" - Psychological Bulletin, 53(4), 267-293
- de Bono, E. (1967). "New Think: The Use of Lateral Thinking" - Basic Books

**"Mixed" Analysis:**
- Not formally defined in cognitive psychology literature
- May refer to iterative alternation between divergent and convergent modes
- The Diamond model (diverge → converge) is the standard pattern, but phases are discrete
- Calling something "mixed" is imprecise and loses the benefit of mode-specific behaviors

**Resolution:** Future agents should use one of the canonical modes (divergent, convergent, lateral) or explicitly document iterative alternation between modes. The term "mixed" should not be used.

**Impact:**
- Agent design guidelines updated
- No work items directly affected beyond WI-SAO-005/006 (already cancelled)

---

## DISCOVERY-003: WORKTRACKER_SOP.md Did Not Follow Claude Code Best Practices

- **Discovered:** 2026-01-11
- **Severity:** MEDIUM (technical debt)
- **Discovery Context:** User-requested research into Claude Code best practices for SOP

**Finding:**

The original WORKTRACKER_SOP.md v1.0.0 was created without evidence-based design. Gap analysis against authoritative sources identified 12 missing elements.

**Research Methodology:**
1. Context7 query: `/anthropics/claude-code` and `/nikiforovall/claude-code-rules`
2. Web search: Claude Code best practices, LangGraph memory management, AWS Strands SOPs
3. Gap analysis against 15 authoritative sources

**Key Gaps Identified:**

| Gap ID | Missing Element | Best Practice Source | Severity |
|--------|-----------------|----------------------|----------|
| GAP-SOP-001 | Expert persona definition | Claude Code 6-step process | MEDIUM |
| GAP-SOP-002 | Proactive behavior triggers | Claude Code Handbook | HIGH |
| GAP-SOP-003 | Worked examples | Claude Code best practices | HIGH |
| GAP-SOP-004 | Decision-making framework | Claude Code optimization | MEDIUM |
| GAP-SOP-005 | Self-verification questions | Claude Code quality control | MEDIUM |
| GAP-SOP-006 | Escalation protocol | Claude Code escalation | MEDIUM |
| GAP-SOP-007 | Session vs persistent memory | LangGraph memory types | LOW |
| GAP-SOP-008 | Rollback procedures | Industry crisis management | MEDIUM |
| GAP-SOP-009 | Anti-patterns section | Best practice completeness | LOW |
| GAP-SOP-010 | Version changelog | Industry auditability | LOW |
| GAP-SOP-011 | IF/WHEN/THEN logic | AWS Strands SOP | LOW |
| GAP-SOP-012 | Session start/resume guidance | LangGraph thread management | MEDIUM |

**Research Sources (Authoritative):**
- [Anthropic Claude Code Agent Creation System Prompt](https://github.com/anthropics/claude-code) - HIGH authority
- [Claude Code Handbook](https://github.com/nikiforovall/claude-code-rules) - HIGH authority
- [AWS Strands Agent SOPs](https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/) - HIGH authority
- [LangGraph State Management](https://sparkco.ai/blog/mastering-langgraph-state-management-in-2025) - HIGH authority
- [CLAUDE.md Optimization (Arize)](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/) - HIGH authority

**Resolution:**
- Updated WORKTRACKER_SOP.md from v1.0.0 → v2.0.0
- Added 8 new sections addressing HIGH and MEDIUM gaps
- Persisted research to `research/worktracker-sop-best-practices-analysis.md`

**Impact:**
- WORKTRACKER_SOP.md now evidence-based and aligned with industry best practices
- Research artifact available for future reference
- Changelog added for auditability

---

## DISCOVERY-004: Agent Path Confusion in Multi-Test Sessions

- **Discovered:** 2026-01-11
- **Severity:** MEDIUM (causes incorrect test artifact locations)
- **Discovery Context:** During PS-ORCH-005 Fan-Out test execution (WI-SAO-030)
- **Finding:**

When invoking multiple agents across different tests in the same session, agents occasionally wrote output to incorrect directories (previous test directories instead of current test directories).

**Observed Behavior:**
- ps-analyst and ps-researcher agents invoked for PS-ORCH-005 test
- Output files appeared in `PS-ORCH-002/` directory instead of `PS-ORCH-005/`
- Root cause: Agents may cache or confuse paths from prior context

**Evidence:**
- Source: WI-SAO-030 (DISCOVERY-030-001)
- Execution Report: `tests/ps-orchestration-results/PS-ORCH-005/EXECUTION-REPORT.md`

**Resolution:**
- Re-invoked agents with explicit absolute paths
- **Recommendation:** Always use absolute paths in agent prompts, not relative references

**Impact:**
- PS-ORCH-005 test required agent re-invocation
- No data loss (files recoverable)
- Process improvement identified for future test execution

---

## DISCOVERY-005: API Connection Errors During Agent Invocation (Transient)

- **Discovered:** 2026-01-11
- **Severity:** LOW (transient, recoverable with retry)
- **Discovery Context:** Multiple occurrences during SAO-INIT-006 verification testing
- **Finding:**

API connection errors occurred sporadically during agent invocations. All were transient and recovered with retry.

**Occurrences:**
| Instance | Agent | Test | Resolution |
|----------|-------|------|------------|
| 1 | ps-reporter | PS-ORCH-006 | Retry succeeded |
| 2 | nse-requirements | CROSS-ORCH-001 | Retry succeeded (2 attempts) |
| 3 | ps-analyst | CROSS-ORCH-002 | First attempt succeeded |

**Evidence:**
- WI-SAO-030: DISCOVERY-030-002
- WI-SAO-031: DISCOVERY-031-001
- Execution Reports in `tests/ps-orchestration-results/*/EXECUTION-REPORT.md`

**Resolution:**
- Retry agent invocation on connection error
- No architectural changes required

**Impact:**
- Minor execution delays (< 1 minute per retry)
- No test failures attributable to connection errors
- All tests completed successfully after retries

---

## DISCOVERY-006: Cross-Family Agent Interoperability Validated

- **Discovered:** 2026-01-11
- **Severity:** INFO (positive validation finding)
- **Discovery Context:** CROSS-ORCH-001 and CROSS-ORCH-002 test execution (WI-SAO-031)
- **Finding:**

**POSITIVE VALIDATION:** ps-* and nse-* agent families successfully interoperate using shared session_context schema v1.0.0.

**Validated Patterns:**
| Pattern | Test | Agents | Result |
|---------|------|--------|--------|
| Sequential Cross-Family | CROSS-ORCH-001 | ps-researcher → nse-requirements | PASS |
| Mixed Fan-In | CROSS-ORCH-002 | ps-analyst + nse-risk → ps-reporter | PASS |

**Key Evidence:**
- session_context schema_version "1.0.0" transfers between families
- Key findings consumed and traced across family boundaries
- 10 findings → 22 requirements (CROSS-ORCH-001)
- 10 findings → 5 unified findings (CROSS-ORCH-002)
- Convergence score: 0.92 (strong alignment)

**Evidence Artifacts:**
- `tests/ps-orchestration-results/CROSS-ORCH-001/` (2 files, 42,272 bytes)
- `tests/ps-orchestration-results/CROSS-ORCH-002/` (3 files, 51,081 bytes)
- Full execution reports with traceability matrices

**Impact:**
- Cross-family orchestration patterns ready for production use
- Validates session_context schema design
- Enables mixed ps-*/nse-* workflows for NASA SE domain

---

## DISCOVERY-007: Parallel Agent Execution Timing Variance

- **Discovered:** 2026-01-11
- **Severity:** INFO (informational, not a defect)
- **Discovery Context:** CROSS-ORCH-002 parallel phase execution (WI-SAO-031)
- **Finding:**

When invoking agents in parallel, execution times vary significantly based on agent model selection and output complexity.

**Observed:**
- nse-risk: ~1 minute (produced 20,286 bytes)
- ps-analyst: ~5 minutes (produced 13,585 bytes)

**Analysis:**
- Model selection (haiku vs sonnet) affects inference time
- Output structure complexity varies by agent role
- Larger output size does not correlate directly with longer execution time

**Evidence:**
- Source: WI-SAO-031 (DISCOVERY-031-002)
- Execution Report: `tests/ps-orchestration-results/CROSS-ORCH-002/EXECUTION-REPORT.md`

**Resolution:**
- No action required - this is expected behavior
- For time-critical workflows, consider model selection impact

**Impact:**
- Informational for workflow planning
- Does not affect test validity

---

*Last Updated: 2026-01-11*
*Source: Extracted from WORKTRACKER.md lines 2387-2464, extended with DISCOVERY-003 through DISCOVERY-007*

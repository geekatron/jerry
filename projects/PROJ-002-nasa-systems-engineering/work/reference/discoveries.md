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

## DISCOVERY-008: 8 Orchestration Patterns Identified (Expanded from 4)

- **Discovered:** 2026-01-12
- **Severity:** INFO (positive expansion of documented patterns)
- **Discovery Context:** Deep research for SAO-INIT-007 Triple-Lens Playbook Refactoring
- **Finding:**

Deep analysis of agent files and orchestration patterns revealed 8 distinct orchestration patterns, expanding from the 4 previously documented.

**Original 4 Patterns:**
1. Sequential Chain
2. Fan-Out (Parallel)
3. Fan-In (Aggregation)
4. Generator-Critic Loop

**Newly Identified Patterns:**
5. Single Agent - Direct invocation without orchestration overhead
6. Cross-Pollinated Pipeline - Bidirectional barriers for multi-track workflows
7. Divergent-Convergent (Diamond) - Explore options then converge
8. Review Gate - Quality checkpoint with pass/fail and feedback loop

**Key Technical Details:**

| Pattern | Use Case | Cognitive Mode |
|---------|----------|----------------|
| Single Agent | Direct specialty match | Agent-dependent |
| Sequential Chain | Order-dependent workflow | Convergent |
| Fan-Out | Independent parallel tasks | Divergent |
| Fan-In | Output consolidation | Convergent |
| Cross-Pollinated | Multi-skill collaboration | Mixed (barrier-separated) |
| Diamond | Solution exploration | Divergent → Convergent |
| Review Gate | Quality gates (SRR, PDR, CDR) | Convergent |
| Generator-Critic | Iterative refinement | Alternating |

**Circuit Breaker Parameters (Pattern 8):**
- `max_iterations`: 3 (hard limit)
- `quality_threshold`: 0.85 (exit condition)
- `escalation`: After 3 fails → human review required

**Evidence:**
- Source: SAO-INIT-007 initiative deep research
- Agent files analyzed: 22 agents across ps-*, nse-*, orch-* families
- Location: `initiatives/sao-init-007-triple-lens-playbooks/_index.md`

**Impact:**
- Comprehensive pattern catalog available for playbook refactoring
- Pattern selection decision tree documented
- Workflow scenario compositions defined

---

## DISCOVERY-009: Session Context Schema v1.0.0 Formalized

- **Discovered:** 2026-01-12
- **Severity:** INFO (formalization of existing practice)
- **Discovery Context:** Deep research for SAO-INIT-007 Triple-Lens Playbook Refactoring
- **Finding:**

Formal session context schema v1.0.0 has been documented for agent handoffs. This schema enables:
- Validated agent-to-agent state transfer
- Cognitive mode declarations
- State output key mapping
- Next agent hints

**Schema Structure:**
```yaml
session_context:
  version: "1.0.0"
  session_id: "uuid-v4"
  source_agent: "agent-name"
  target_agent: "agent-name"
  handoff_timestamp: "ISO-8601"
  state_output_key: "key_name"
  cognitive_mode: "convergent|divergent"
  payload:
    findings: [ ... ]
    confidence: 0.0-1.0
    next_hint: "suggested_next_agent"
```

**State Output Key Mapping (19 agents):**

| Agent | State Key | Next Hint |
|-------|-----------|-----------|
| ps-researcher | research_output | ps-analyst |
| ps-analyst | analysis_output | ps-architect |
| ps-architect | architecture_output | ps-validator |
| ps-validator | validation_output | ps-synthesizer |
| ps-critic | critique_output | (generator) |
| ps-investigator | investigation_output | ps-analyst |
| ps-reporter | report_output | (terminal) |
| ps-reviewer | review_output | (conditional) |
| ps-synthesizer | synthesis_output | ps-reporter |
| nse-requirements | requirements_output | nse-verification |
| nse-verification | verification_output | nse-reviewer |
| nse-reviewer | review_output | (conditional) |
| nse-reporter | report_output | (terminal) |
| nse-risk | risk_output | nse-reviewer |
| nse-architecture | architecture_output | nse-integration |
| nse-integration | integration_output | nse-verification |
| nse-configuration | configuration_output | nse-qa |
| nse-qa | qa_output | nse-reporter |
| nse-explorer | exploration_output | (context-dependent) |

**Cross-Skill Handoff Support:**
- ps-architect → nse-architecture
- ps-analyst → nse-risk
- ps-validator → nse-verification
- nse-requirements → ps-architect
- nse-verification → ps-investigator
- nse-reviewer → ps-analyst

**Evidence:**
- Source: SAO-INIT-007 initiative deep research
- Prior validation: CROSS-ORCH-001, CROSS-ORCH-002 (DISCOVERY-006)
- Location: `initiatives/sao-init-007-triple-lens-playbooks/_index.md`

**Impact:**
- Standardized handoff protocol for all orchestration patterns
- Enables automated validation of agent chains
- Supports cross-skill workflows

---

## DISCOVERY-010: work-XXX Naming Convention is Valid Pattern

- **Discovered:** 2026-01-12
- **Severity:** LOW (false positive in test harness)
- **Discovery Context:** WI-SAO-037 playbook validation test harness development
- **Finding:**

The playbook validation test harness initially flagged `work-XXX-topic.md` patterns as placeholders, but this is actually a valid naming convention for work item references.

**Valid Patterns Identified:**
- `work-XXX-topic.md` - Work item file naming convention
- `XXX-\d+` - ID patterns (e.g., XXX-001)
- `XXX-e-` - Evidence ID patterns

**Resolution:**
- Updated test harness exclude patterns to recognize these as valid
- Test harness now passes all three playbooks

**Impact:**
- Test harness accuracy improved
- No documentation changes needed

---

## DISCOVERY-011: nse-architecture Missing State Management Section

- **Discovered:** 2026-01-12
- **Severity:** LOW (documentation gap)
- **Discovery Context:** WI-SAO-040 session context schema validation
- **Finding:**

The `nse-architecture.md` agent file is missing the explicit State Management section that defines the Output Key. All other 18 agents have this section.

**Evidence:**
```
skills/nasa-se/agents/nse-architecture.md
- Has session_context in frontmatter
- Missing: State Management section with Output Key
- Other agents have: `**Output Key:** `{type}_output``
```

**Resolution:**
- Flagged as technical debt
- Low priority as schema_version is correctly implemented

**Impact:**
- Minor documentation inconsistency
- No functional impact (agent works correctly)

---

## DISCOVERY-012: Critical Documentation Gaps in Problem-Solving Playbook

- **Discovered:** 2026-01-12
- **Severity:** CRITICAL (user-reported gaps)
- **Discovery Context:** User review of SAO-INIT-007 "complete" status
- **Finding:**

The problem-solving PLAYBOOK.md was marked complete but has critical gaps:

**Gap Analysis:**

| Gap ID | Severity | Description | Impact |
|--------|----------|-------------|--------|
| GAP-012-001 | **CRITICAL** | Generator-Critic loop not documented | Users can't use ps-critic effectively |
| GAP-012-002 | **CRITICAL** | ps-critic agent usage not explained | Agent exists but undocumented |
| GAP-012-003 | **HIGH** | No concrete L0/L1/L2 examples | Users lack real-world reference |
| GAP-012-004 | **MEDIUM** | @ symbol invocation not documented | Users don't know invocation syntax |
| GAP-012-005 | **HIGH** | nse-* Generator-Critic applicability unknown | NASA SE feedback loops unclear |

**Root Cause:**
Initial playbook refactoring focused on structural compliance (L0/L1/L2 lens) but missed functional completeness (all agent interactions, concrete examples, invocation methods).

**Resolution:**
- SAO-INIT-007 reopened (9/13 → 9/13 complete with 4 new work items)
- WI-SAO-042: Research & document Generator-Critic patterns (P1)
- WI-SAO-043: Add L0/L1/L2 concrete examples (P1)
- WI-SAO-044: Document @ symbol agent invocation (P2)
- WI-SAO-045: Verify nse-* Generator-Critic applicability (P1)

**Impact:**
- Initiative completion delayed
- Additional ~13h estimated effort
- Playbook quality will improve significantly

---

*Last Updated: 2026-01-12*
*Source: Extended with DISCOVERY-010, DISCOVERY-011, DISCOVERY-012 from SAO-INIT-007 validation*

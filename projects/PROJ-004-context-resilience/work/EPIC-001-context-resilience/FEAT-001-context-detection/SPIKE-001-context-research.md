# SPIKE-001: Research Context Measurement, Detection Thresholds & Resumption Protocols

<!--
TEMPLATE: Spike
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

> **Type:** spike
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research question, hypothesis, scope |
| [Findings](#findings) | Summary and detailed findings (populated after research) |
| [Recommendation](#recommendation) | Decision and recommended actions (populated after research) |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes |

---

## Content

### Research Question

**Question:** How can we reliably detect context exhaustion during multi-orchestration runs, what are the optimal detection thresholds, and what resumption protocol enables Claude to self-orient from ORCHESTRATION.yaml + WORKTRACKER.md in a new session?

### Hypothesis

We hypothesize that:
1. Context fill can be estimated through token counting heuristics or Claude Code session APIs
2. A two-tier threshold (warning ~70%, critical ~85%) provides sufficient lead time for graceful checkpoint
3. The existing ORCHESTRATION.yaml `resumption` section, combined with WORKTRACKER.md status, contains sufficient state for full context reconstruction
4. A structured resumption prompt template can reliably re-orient Claude without operator guidance

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox Duration | 8 hours |
| Start Date | TBD |
| Target End Date | TBD |

**Warning:** Do not exceed the timebox. If more research is needed, create a follow-up spike.

### Scope

**In Scope:**
- How Claude Code exposes context usage (APIs, hooks, heuristics, system messages)
- How context compaction (automatic compression) works and when it triggers
- What token counting methods are available (tiktoken, API response metadata, etc.)
- Current ORCHESTRATION.yaml `resumption` section completeness and gaps
- Current manual resumption pain points and failure modes
- Optimal threshold values based on real orchestration run data
- Resumption prompt template design
- Integration points with existing /orchestration skill and AE-006 rule

**Out of Scope:**
- Implementation of detection mechanism (that's FEAT-001 work)
- Automatic session rotation (future scope)
- Context optimization/compression strategies
- Cross-provider context management (Anthropic-specific only)

### Research Approach

1. **Inventory existing mechanisms:** Audit Claude Code session APIs, hook system, and system-reminder messages for context fill indicators. Review AE-006 (token exhaustion escalation) for existing handling.
2. **Analyze real orchestration runs:** Examine PROJ-001 orchestration runs (FEAT-015 license migration, EPIC-001 docs workflow) for context exhaustion patterns — when did they hit limits, what state was lost, how was resumption handled.
3. **Evaluate detection methods:** Compare (a) token counting heuristics, (b) Claude Code context compaction detection, (c) hook-based monitoring, (d) response quality degradation signals. Score by reliability, overhead, and implementation complexity.
4. **Assess resumption completeness:** Review existing ORCHESTRATION.yaml `resumption` sections from real workflows. Identify gaps — what information is missing for reliable self-orientation? What does an operator currently have to supply manually?
5. **Design resumption prompt:** Draft a structured prompt template that reads ORCHESTRATION.yaml + WORKTRACKER.md and outputs a resumption plan. Test mentally against real workflow snapshots.
6. **Propose thresholds:** Based on real data, propose warning and critical thresholds. Consider: how much token budget is needed for a graceful checkpoint? How much degradation occurs at various fill levels?
7. **Synthesize findings:** Document findings, recommendation, and follow-up work items.

---

## Findings

### Summary

_To be populated after research._

### Detailed Findings

_To be populated after research._

### Evidence/References

_To be populated after research._

---

## Recommendation

### Decision

_To be populated after research._

### Recommended Actions

_To be populated after research._

### Follow-up Work Items

| Type | Title | Priority |
|------|-------|----------|
| _TBD_ | _To be defined based on findings_ | _TBD_ |

### Risks/Considerations

- Context measurement APIs may not exist or may be unreliable
- Threshold values may vary significantly by orchestration pattern and criticality level
- Resumption fidelity depends on ORCHESTRATION.yaml completeness — if the yaml is stale, resumption fails
- Quality gate enforcement across session boundaries is untested

---

## Related Items

- Parent: [FEAT-001: Context Exhaustion Detection & Graceful Session Handoff](./FEAT-001-context-detection.md)
- Related: [quality-enforcement.md AE-006](../../../../.context/rules/quality-enforcement.md) — Existing token exhaustion escalation rule
- Related: [/orchestration skill](../../../../skills/orchestration/SKILL.md) — Orchestration state management
- Related: PROJ-001 ORCHESTRATION.yaml — Real workflow state examples

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-19 | pending | Spike defined. 7-step research approach covering detection methods, threshold analysis, and resumption protocol design. |

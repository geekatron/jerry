# SPIKE-001: Research Context Measurement, Detection Thresholds & Resumption Protocols

<!--
TEMPLATE: Spike
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

> **Type:** spike
> **Status:** done
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

- **Context exhaustion is a real, quantifiable problem.** PROJ-001 FEAT-015 analysis projects 350-400K tokens for a single C2 orchestration (4 phases, 8 agents, 9 QG iterations) against a 200K context window, predicting 2 compaction events. Quality gate iterations are the dominant cost driver at 29K-45K tokens each.
- **Detection is feasible with existing Claude Code mechanisms.** A Hybrid A+B architecture (transcript-based token heuristic + PreCompact hook compaction detection) provides both proactive early warning and deterministic compaction awareness, consuming ~2% of context budget for monitoring overhead.
- **The original two-tier threshold hypothesis (70%/85%) is insufficient.** A five-tier graduated model (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY + COMPACTION) calibrated from empirical PROJ-001 data provides the operational granularity needed for graduated orchestrator responses. C1/C3/C4 thresholds are PROVISIONAL.
- **The existing resumption protocol is critically incomplete.** The current 5-field resumption section captures location but not intelligence (defect history, decisions, quality trajectory). An enhanced schema v2.0 with 7 sub-sections and 23 fields addresses 6 identified gaps (2 CRITICAL, 2 HIGH, 2 MEDIUM).
- **Structured resumption prompt templates enable self-orientation.** Two prompt templates (resumption at ~760 tokens for new sessions, compaction alert at ~280 tokens for same-session re-orientation) achieve productive work within 2-3 prompts in mental testing against PROJ-001 scenarios.

### Detailed Findings

**Hypothesis 1 (Context fill estimation): CONFIRMED with caveats.** 17 mechanisms were inventoried across 5 areas (API, hooks, system-reminder, AE-006, status line). The most accurate data sources (Token Counting API, Usage Objects) are client-side only. The transcript-based heuristic (Method A) uses `$TRANSCRIPT_PATH` usage data as a proxy for context fill. The injection pathway via `UserPromptSubmit` -> `additionalContext` is proven and operational. Key caveat: the `input_tokens` ~ context fill approximation is unvalidated (OQ-9). See synthesis Section L1, Hypothesis 1 for full evidence.

**Hypothesis 2 (Two-tier threshold): PARTIALLY CONFIRMED -- revised to five-tier.** Phase 2 showed that a single QG iteration can consume 14.5% of the 200K window, meaning the gap between "comfortable" and "compaction imminent" can be crossed in one operation. The five-tier model provides graduated responses calibrated to operational capacity: WARNING at 70% (2 QG iterations fit), CRITICAL at 80% (1 fits), EMERGENCY at 88% (none fit). Validation against PROJ-001 shows thresholds would have provided 5 detection signals across 17 steps. See synthesis Section L1, Hypothesis 2 for full evidence.

**Hypothesis 3 (Resumption sufficiency): REFUTED.** Six resumption gaps identified (RG-1 through RG-6). The root cause (RG-6) is that the resumption section is static -- updated only at workflow completion. Enhanced schema v2.0 with 23 fields and an explicit update protocol addresses all gaps. Companion checkpoint file format provides emergency state snapshots for unplanned compaction. See synthesis Section L1, Hypothesis 3 for full evidence.

**Hypothesis 4 (Resumption prompt): CONFIRMED with operational constraints.** Two prompt templates designed and mentally tested. Template 1 achieves productive work by prompt 3 at both PROJ-001 compaction points. Template 2 achieves same-session re-orientation with 6-22% of post-compaction context. Constraints: Template 1 requires manual operator injection (no SessionStart automation), and the system depends on the resumption update protocol being followed. See synthesis Section L1, Hypothesis 4 for full evidence.

### Evidence/References

| # | Phase | Artifact | Key Content |
|---|-------|----------|-------------|
| 1 | Phase 1 | `res/phase-1-inventory/research-inventory/mechanism-inventory.md` | 17 mechanisms (M-001 through M-017), 6 gaps (GAP-001 through GAP-006), capability matrix |
| 2 | Phase 2 | `res/phase-2-analysis/run-analyzer/run-analysis.md` | PROJ-001 workflow profile, token budgets, 17-step fill projection, resumption gaps (RG-1 through RG-6), risk points |
| 3 | Phase 3 | `res/phase-3-detection/detection-evaluator/detection-evaluation.md` | Hybrid A+B recommendation, method scoring, architecture, open questions (OQ-1 through OQ-9) |
| 4 | Phase 4 | `res/phase-4-resumption/resumption-assessor/resumption-assessment.md` | Enhanced resumption schema v2.0, checkpoint file format, WORKTRACKER assessment |
| 5 | Phase 5 | `res/phase-5-prompt/prompt-designer/resumption-prompt-design.md` | Template 1 (~760 tokens), Template 2 (~280 tokens), OQ resolutions, PROJ-001 mental tests |
| 6 | Phase 6 | `res/phase-6-thresholds/threshold-analyst/threshold-proposal.md` | Five-tier model, operation cost catalog, AE-006 integration, PROJ-001 validation, calibration protocol |
| 7 | QG-1 | `res/quality-gates/qg-1/gate-result.md` | Detection evaluation: 0.91 -> 0.93 PASS (2 iterations) |
| 8 | QG-2 | `res/quality-gates/qg-2/gate-result.md` | Threshold proposal: 0.90 -> 0.92 PASS (2 iterations) |

All artifact paths are relative to `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/`. Full synthesis document: `res/phase-7-synthesis/spike-synthesizer/spike-synthesis.md`.

---

## Recommendation

### Decision

**GO for FEAT-001 implementation.** The research demonstrates that context exhaustion is a real, quantifiable problem with a feasible technical solution using existing Claude Code mechanisms. The detection architecture (Hybrid A+B), threshold model (five-tier graduated), resumption schema (v2.0 with 23 fields), and prompt templates (2 templates) are designed with sufficient detail for direct implementation. The research was conducted across 7 phases with 2 quality gates (QG-1: 0.93 PASS, QG-2: 0.92 PASS), providing high confidence in the design quality.

### Recommended Actions

1. **Implement the minimum viable context resilience system (P1 items 1-5).** This includes the UserPromptSubmit context monitor hook (Method A), PreCompact checkpoint hook (Method B), compaction alert injection, enhanced ORCHESTRATION.yaml template, and orchestrator resumption update protocol. Estimated effort: 12-19 hours.
2. **Update AE-006 in quality-enforcement.md (P2 item 6).** Replace the single rule with graduated sub-rules (AE-006a through AE-006e). Note: this touches `.context/rules/` and triggers AE-002 (auto-C3 minimum).
3. **Validate key assumptions (P2 items 8-9).** Run two timeboxed spikes: (a) validate that `input_tokens` accurately approximates context fill (OQ-9), and (b) investigate whether the ECW status line can share data with hooks for Method C upgrade (OQ-1).
4. **Validate thresholds against a second workflow (P3 item 13).** Run a monitored session with the detection system active against a non-FEAT-015 workflow to stress-test the single-workflow calibration.

### Follow-up Work Items

| Type | Title | Priority |
|------|-------|----------|
| Enabler | Implement UserPromptSubmit context monitor hook (Method A) | P1 - Critical |
| Enabler | Implement PreCompact hook for checkpoint file creation (Method B) | P1 - Critical |
| Enabler | Implement compaction alert injection in UserPromptSubmit hook | P1 - Critical |
| Story | Update ORCHESTRATION.yaml template with enhanced resumption schema v2.0 | P1 - Critical |
| Story | Update orchestrator prompt to maintain resumption section (update protocol) | P1 - Critical |
| Story | Update AE-006 in quality-enforcement.md with graduated sub-rules | P2 - High |
| Story | Implement threshold configuration file | P2 - High |
| Spike | Validate OQ-9: Does `input_tokens` accurately approximate context fill? | P2 - High |
| Spike | Investigate Method C feasibility (OQ-1): status line data sharing | P2 - High |
| Story | Add `.jerry/checkpoints/` to project workspace layout | P3 - Medium |
| Story | Create resumption prompt automation (Template 1 populator) | P3 - Medium |
| Enabler | Implement PostToolUse hook for resumption staleness validation | P3 - Medium |
| Story | Validate thresholds against a second workflow type | P3 - Medium |
| Story | Document calibration protocol and recalibration triggers | P4 - Low |

### Risks/Considerations

- **Single-workflow calibration.** All quantitative findings derive from PROJ-001 FEAT-015. Thresholds may not generalize to workflows with different token consumption patterns (e.g., deep research spikes, multi-file refactors). Mitigation: Calibration Protocol with 2 validation workflows and 4 recalibration triggers defined.
- **Triggering vs. effectiveness gap.** Detection signals fire at the right time (validated), but orchestrator compliance at 80%+ fill is unvalidated. L1 enforcement degrades to 40-60% at high fill, creating circularity where L2 mitigation is vulnerable to the problem it mitigates. Mitigation: L3 deterministic gating (blocking tool calls at EMERGENCY) identified as future enhancement.
- **L2-only enforcement.** No L3 or L5 enforcement layers for context resilience exist. All enforcement relies on the LLM voluntarily following injected instructions. Mitigation: Design is extensible to L3/L5; dual enforcement (L2 reinject + hook-based staleness detection) reduces single-point-of-failure risk.
- **Cumulative estimation uncertainty.** Token estimates have 10-20% error per operation, potentially compounding across many operations. Threshold boundaries are approximate (+/- 5%). Mitigation: EMERGENCY threshold at 88% provides 12% safety margin accounting for cumulative drift.
- **Quality gate enforcement across session boundaries is untested.** The enhanced resumption schema preserves quality gate state, but no actual multi-session QG flow has been executed. Mitigation: FEAT-001 implementation should include a controlled multi-session QG test.
- **Template 1 requires manual injection.** No SessionStart hook automation for cross-session resumption. Operator must manually paste the resumption prompt. Mitigation: Template 1 populator (P3 work item) and future SessionStart hook integration.

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
| 2026-02-19 | done | SPIKE-001 research complete. 7 phases, 2 quality gates (QG-1: 0.93 PASS, QG-2: 0.92 PASS). Recommend proceeding with FEAT-001 implementation. |

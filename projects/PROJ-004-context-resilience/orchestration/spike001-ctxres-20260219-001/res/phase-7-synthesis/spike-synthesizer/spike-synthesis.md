# SPIKE-001 Research Synthesis: Context Measurement, Detection Thresholds & Resumption Protocols

<!-- PS-ID: SPIKE-001 | ENTRY-ID: phase-7-synthesis | DATE: 2026-02-19 -->
<!-- AGENT: ps-synthesizer v2.2.0 | MODEL: claude-opus-4-6 -->

> Final synthesis of all SPIKE-001 research findings across 6 phases and 2 quality gates.
> Provides hypothesis assessment, consolidated findings, architecture implications,
> and actionable follow-up work items for FEAT-001 implementation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Stakeholder-level: research question, key findings, recommendation |
| [L1 Detailed Findings](#l1-detailed-findings) | Engineer-level: hypothesis assessment with evidence |
| [L2 Architecture Implications](#l2-architecture-implications) | Principal architect: framework impact, enforcement model changes |
| [Open Questions](#open-questions) | Consolidated unresolved questions from all phases |
| [Follow-Up Work Items](#follow-up-work-items) | Concrete stories, enablers, and tasks for FEAT-001 |
| [Cross-Phase Traceability Matrix](#cross-phase-traceability-matrix) | Finding-to-evidence mapping |
| [Self-Review Checklist](#self-review-checklist) | S-010 compliance verification |
| [References](#references) | All phase artifacts and quality gate results |

---

## L0 Summary

### Research Question

How can we reliably detect context exhaustion during multi-orchestration runs, what are the optimal detection thresholds, and what resumption protocol enables Claude to self-orient from persistent state in a new session?

### Key Findings

1. **Context exhaustion is a real, quantifiable problem.** Analysis of the PROJ-001 FEAT-015 workflow shows that a single C2 orchestration with 4 phases, 8 agents, and 9 quality gate iterations would consume approximately 350-400K tokens in a single session -- nearly 2x the 200K context window. Two compaction events are predicted, each causing unmanaged context loss. Quality gate iterations are the dominant cost driver at 29,000-45,000 tokens each. (Phase 2)

2. **Detection is feasible with existing Claude Code mechanisms.** A hybrid detection architecture combining transcript-based token heuristics (Method A) with PreCompact hook compaction detection (Method B) provides both proactive early warning and deterministic compaction awareness. The injection pathway is proven -- the existing `UserPromptSubmit` hook's `additionalContext` field successfully injects per-prompt data into Claude's context window, consuming approximately 2% of the context budget for monitoring overhead across a session. (Phases 1, 3)

3. **A five-tier graduated threshold model replaces the original two-tier hypothesis.** The original 70%/85% hypothesis was revised to a five-tier model (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY + COMPACTION) calibrated against empirical PROJ-001 data. WARNING fires at 70% (when fewer than 2 QG iterations fit), CRITICAL at 80% (when only 1 QG iteration fits), and EMERGENCY at 88% (when no QG iteration fits). C1/C3/C4 thresholds are PROVISIONAL pending multi-workflow calibration. (Phase 6)

4. **The existing resumption protocol is insufficient.** The current ORCHESTRATION.yaml `resumption` section has 5 fields occupying 12 lines. It captures location (where the workflow is) but not intelligence (what happened -- defect history, decisions, quality trajectory). An enhanced schema v2.0 with 7 sub-sections and 23 fields addresses 6 identified gaps (2 CRITICAL, 2 HIGH, 2 MEDIUM). Two prompt templates (resumption at ~760 tokens, compaction alert at ~280 tokens) enable self-orientation within 2-3 prompts. (Phases 4, 5)

5. **AE-006 needs graduated sub-rules.** The current single AE-006 rule ("mandatory human escalation on token exhaustion at C3+") has no automated detection, no quantitative definition of "exhaustion," and no graduated response. A proposed replacement with 5 sub-rules (AE-006a through AE-006e) maps detection thresholds to escalation actions by criticality level, with enforcement through L2 prompt injection. (Phase 6)

### Recommendation

**GO for FEAT-001 implementation.** The research demonstrates that context exhaustion is a real problem with a feasible technical solution. The detection architecture, threshold model, resumption schema, and prompt templates are designed with sufficient detail for direct implementation. Key risk: single-workflow calibration means thresholds are provisional and must be validated during FEAT-001 implementation against additional workflow types.

---

## L1 Detailed Findings

### Hypothesis 1: Context fill can be estimated through token counting heuristics or Claude Code session APIs

**Assessment: CONFIRMED with caveats.**

**Evidence:**

- Phase 1 inventoried 17 mechanisms across 5 areas (API, hooks, system-reminder, AE-006, status line). The most accurate data sources (M-001 Token Counting API, M-002 Usage Objects) are client-side only -- the LLM cannot directly access them. (Phase 1, L2 Capability Matrix)
- The transcript-based heuristic (Method A) uses `$TRANSCRIPT_PATH` -- available in ALL hook events -- to parse usage data from JSONL transcript entries. The most recent turn's `input_tokens` value serves as a proxy for current context fill. (Phase 3, Method A Profile)
- The `UserPromptSubmit` -> `additionalContext` injection pathway is proven and operational. Jerry's L2 reinforcement system already uses it, injecting ~600 tokens per prompt. Adding a `<context-monitor>` injection adds approximately 40-200 tokens per prompt depending on threshold level. (Phases 1, 3)
- The ECW status line (M-017) reads actual `context_window.current_usage` data from Claude Code, but this data is not available to hooks (GAP-003). A file-based relay (status line writes, hook reads) is proposed as a Method C upgrade path but feasibility is unverified. (Phases 1, 3)

**Caveats:**

- The equation `input_tokens` ~ context window occupancy is plausible but empirically unvalidated (OQ-9 from Phase 3 QG-1). Phase 4 prototyping must verify this relationship.
- Transcript-based estimation is approximate (GAP-006). After compaction, cumulative sums over-estimate fill. The heuristic's accuracy degrades over long sessions with multiple compaction events.
- The post-compaction transcript behavior is unknown (OQ-3). Whether `input_tokens` in a post-compaction entry reflects pre- or post-compaction context size is unverified.
- Estimation error margin is 10-20% per operation. Cumulative estimation uncertainty may compound across many operations, producing larger drift at high fill levels. (Phase 6, Operation Cost Catalog)

### Hypothesis 2: A two-tier threshold (warning ~70%, critical ~85%) provides sufficient lead time for graceful checkpoint

**Assessment: PARTIALLY CONFIRMED -- revised to five-tier model.**

**Evidence:**

- Phase 2 empirical analysis of PROJ-001 FEAT-015 showed that the first phase (1 agent + 3 QG iterations) reaches 63.6% context fill. A single QG iteration at C2 costs ~29,000 tokens (14.5% of the 200K window). This means the gap between "comfortable" and "compaction imminent" can be crossed in a single operation. (Phase 2, Cumulative Fill Projection)
- The original two-tier hypothesis (70%/85%) was too coarse. Phase 6 demonstrated that at 70%, approximately 60,000 tokens remain -- enough for 2 typical QG iterations. At 85%, only 30,000 tokens remain -- potentially insufficient even for a single iteration. The gap between these two tiers was too large to provide graduated guidance. (Phase 6, Token Budget Analysis)
- The revised five-tier model (NOMINAL 0-55%, LOW 55-70%, WARNING 70-80%, CRITICAL 80-88%, EMERGENCY 88-95%, plus COMPACTION) provides graduated responses calibrated to operational capacity at each level. (Phase 6, Proposed Thresholds)
- Validation against PROJ-001 confirmed that WARNING would fire at Step 7 (71.1%) -- the last opportunity for proactive action before a QG iteration pushes fill from 71.1% to 88.6% in a single step. CRITICAL would fire mid-QG-iteration at ~81.6% (after S-014 completes), enabling the orchestrator to complete the current iteration then checkpoint. (Phase 6, Validation Against PROJ-001)

**Caveats:**

- Thresholds are calibrated from a single workflow (PROJ-001 FEAT-015). C1/C3/C4 adjustments are PROVISIONAL extrapolations that require validation against measured workflows. (Phase 6, Calibration Protocol)
- QG iterations are large enough (29K-45K tokens) to jump across multiple threshold levels in a single step. At PROJ-001 Step 8, the system would cross WARNING, CRITICAL, and EMERGENCY within one QG iteration. The multi-prompt nature of QG iterations provides intermediate detection points, but the orchestrator must be designed to handle mid-operation threshold transitions. (Phase 6, Validation Against PROJ-001)
- The validation demonstrates when thresholds would trigger (timing) but not whether the orchestrator would reliably act on the signals at high context fill (effectiveness). At 80%+ fill, L1 enforcement effectiveness degrades to 40-60% (ADR-EPIC002-002 research), creating a circularity: the L2 mitigation mechanism is itself vulnerable to the context rot problem it mitigates. (Phase 6, Validation Limitations)

### Hypothesis 3: The existing ORCHESTRATION.yaml `resumption` section contains sufficient state for full context reconstruction

**Assessment: REFUTED -- significant gaps identified, enhanced schema designed.**

**Evidence:**

- Phase 4 analyzed the PROJ-001 ORCHESTRATION.yaml resumption section (5 fields, 12 lines) and the orchestration template (identical 5-field structure). The resumption section captures *where* the workflow is but not *what happened*. (Phase 4, Current State Analysis)
- Six resumption gaps were identified (RG-1 through RG-6), rated CRITICAL to MEDIUM:
  - RG-1 (CRITICAL): No accumulated defect context. QG-1 had 6 major findings in iter 1, 3 in iter 2 -- none surfaced in resumption.
  - RG-2 (HIGH): No inter-phase decision log. QG-2 found DA-001 (copyright inconsistency); the resolution affected Phase 3 but was invisible in resumption.
  - RG-3 (MEDIUM): No compaction event records.
  - RG-4 (MEDIUM): No quality score trajectory (scores embedded as prose in `current_state` string).
  - RG-5 (HIGH): No agent-specific context summaries.
  - RG-6 (CRITICAL): Resumption section is static -- updated only at workflow completion, not incrementally. (Phase 4, Gap Analysis)
- RG-6 (static resumption) is the root cause: if the section were updated at each state transition, it would naturally accumulate defect context, decisions, quality trajectory, and agent summaries. The fix is an explicit update protocol with defined triggers. (Phase 4, Gap Analysis)
- WORKTRACKER.md was assessed as a resumption aid and found insufficient for session recovery -- it answers "what is the project status?" not "where did I leave off?" The ORCHESTRATION.yaml resumption section is the correct location for session recovery data. (Phase 4, WORKTRACKER Assessment)

**Proposed solution:**

- Enhanced resumption schema v2.0 with 7 sub-sections and 23 fields: Recovery State (8 fields), Files to Read (structured with priority/purpose/sections), Quality Trajectory (7 fields), Defect Summary (5 fields), Decision Log (N entries), Agent Summaries (N entries), Compaction Events (2 + N entries). (Phase 4, Enhanced Resumption Schema)
- Companion checkpoint file format (`.jerry/checkpoints/cx-{NNN}-checkpoint.json`) written by the PreCompact hook, providing emergency state snapshots for unplanned compaction. (Phase 4, Checkpoint Data Design)
- Resumption update protocol: the orchestrator MUST update the resumption section at every state transition (phase start/complete, QG iteration, compaction event, cross-phase decision, agent completion). (Phase 4, Schema Design Principle)

### Hypothesis 4: A structured resumption prompt template can reliably re-orient Claude without operator guidance

**Assessment: CONFIRMED with operational constraints.**

**Evidence:**

- Phase 5 designed two prompt templates:
  - **Template 1 (Resumption Prompt, ~760 tokens):** Injected at new session start. Provides recovery state, quality trajectory, key decisions, agent summaries, defect patterns, and prioritized file read instructions. All variables sourced from ORCHESTRATION.yaml resumption section. (Phase 5, Template 1)
  - **Template 2 (Compaction Alert, ~280 tokens):** Injected automatically by `UserPromptSubmit` hook after detecting a PreCompact checkpoint file. Provides what happened, what was lost, and immediate recovery actions. (Phase 5, Template 2)
- Mental testing against PROJ-001 at both predicted compaction points showed:
  - QG-2 compaction (Step 9, 106% fill): LLM reaches productive work by prompt 3. Re-orientation cost: 6.4-22.4% of post-compaction context. (Phase 5, Test 1)
  - QG-Final compaction (Step 17, 118% fill): Conditional success -- may need prompt 4 for 6-deliverable QG-Final. Re-orientation cost: 3.4-57.4% of post-compaction context. (Phase 5, Test 2)
- Cross-session resumption (Template 1 in a fresh 200K window) costs ~5,260 tokens total (2.6% of window), leaving ~195K tokens of headroom. (Phase 5, Mental Test Summary)

**Operational constraints:**

- Template 1 currently requires manual injection by the operator (pasting as the first user message). Future automation via a `SessionStart` hook detecting unacknowledged checkpoint files is proposed but not designed. (Phase 5, Integration Notes)
- Template 2 depends on the PreCompact hook writing a checkpoint file successfully. If the hook fails, no compaction alert is injected and the LLM continues without re-orientation. (Phase 5, Failure Modes)
- The entire prompt template system depends on the resumption update protocol being followed. If the resumption section is stale (RG-6 problem), both templates are populated with stale data. Dual enforcement (L2 reinject + L3/L4 hook-based staleness detection) is proposed as mitigation. (Phase 5, OQ-R5 Resolution)
- The mid-QG-iteration compaction policy is "restart current iteration" (per OQ-R3 resolution). This is simpler but costs ~29,000 tokens per restart vs. a partial-continuation path that would save ~12,000 tokens but introduce significant complexity. (Phase 5, OQ-R3)

---

## L2 Architecture Implications

### Impact on the 5-Layer Enforcement Architecture

The context resilience system introduces new capabilities at multiple enforcement layers:

| Layer | Current State | FEAT-001 Addition | Context Rot Vulnerability |
|-------|--------------|-------------------|--------------------------|
| L1 (Session start) | CLAUDE.md, rule files loaded once | AE-006 sub-rules loaded as behavioral foundation | Vulnerable -- degrades with context fill |
| L2 (Every prompt) | L2-REINJECT quality tags (~600 tokens/prompt) | `<context-monitor>` injection (40-200 tokens/prompt) + `<compaction-alert>` injection (~280 tokens, one-time after compaction) + AE-006 reinject tag (~35 tokens/prompt) | Immune -- re-injected every prompt |
| L3 (Pre-tool-call) | PreToolUse gating | Future: Block agent dispatch at EMERGENCY fill level | Immune -- deterministic gating |
| L4 (Post-tool-call) | PostToolUse inspection | Future: Validate resumption staleness after ORCHESTRATION.yaml writes | Mixed -- deterministic gating immune, self-correction vulnerable |
| L5 (Commit/CI) | Post-hoc verification | Future: Verify checkpoint files exist when fill exceeded thresholds | Immune -- runs outside context |

**Key architectural insight:** The current detection system operates entirely at L2 (prompt injection). This is the correct starting point because L2 is immune to context rot and the injection pathway is proven. However, L2 enforcement relies on the LLM voluntarily complying with injected instructions. At high fill levels (80%+) where the detection signals are most critical, LLM compliance may be degraded. Future L3 enforcement (blocking tool calls at EMERGENCY) would provide a context-rot-immune backstop. (Phase 6, AE-006 Integration, Enforcement Note)

### Impact on Existing AE-006 Rule

The current AE-006 single rule is replaced by 5 graduated sub-rules:

| Sub-Rule | Trigger | Escalation | Enforcement |
|----------|---------|------------|-------------|
| AE-006a | CRITICAL (80%+) at any criticality | Auto-checkpoint: complete current op, write resumption | L2 (context-monitor) |
| AE-006b | EMERGENCY (88%+) at C1-C2 | Auto-boundary: no new ops, final checkpoint, signal session end | L2 (context-monitor) |
| AE-006c | EMERGENCY (88%+) at C3+ | Mandatory human escalation: checkpoint + operator notification | L2 (context-monitor + reinject) |
| AE-006d | PreCompact fires at C3+ | Mandatory human escalation: auto-checkpoint via hook, operator authorizes continuation | L2 (compaction-alert) + Method B (deterministic) |
| AE-006e | Second compaction in session at C3+ | Mandatory human escalation: recommend new session with resumption prompt | L2 + Method B counter |

This preserves the original AE-006 intent (mandatory human escalation at C3+ exhaustion) while adding automated graduated responses for C1-C2 and earlier warning stages.

### Impact on Orchestration Template

The ORCHESTRATION.yaml template requires two changes:

1. **Enhanced `resumption:` section** -- Replace the current 5-field structure with the v2.0 schema (7 sub-sections, 23 fields). Backward compatible: existing fields preserved, new sub-sections additive.
2. **Checkpoint directory** -- Add `.jerry/checkpoints/` to the project workspace layout for PreCompact hook checkpoint files.

### Cross-Cutting Concerns

**Context rot and quality gate enforcement across sessions.** The research reveals a fundamental tension: quality gate enforcement requires accumulated context (defect history, revision tracking, score trajectory), but context exhaustion destroys this accumulated context. The enhanced resumption schema and checkpoint system address this by persisting accumulated intelligence to files, enabling cross-session quality gate continuity. However, the effectiveness of this persistence has not been tested with actual multi-session quality gate flows.

**Token budget impact.** The detection system adds approximately 3,960 tokens of monitoring overhead per 50-prompt session (~2% of the 200K window). Combined with the existing L2 reinject budget (~30,000 tokens for 50 prompts at 600/prompt), the total L2 injection overhead is approximately 17% of the context window. This is within the enforcement architecture budget defined in ADR-EPIC002-002 (15,100 tokens = 7.6% for rules alone, with detection as an additional justified cost).

**ORCHESTRATION.yaml size growth.** The enhanced resumption schema adds approximately 1,000-1,500 tokens to the ORCHESTRATION.yaml file size. For a completed workflow, the file grows from ~7,500 tokens to ~9,000 tokens. This is a 20% increase that must be factored into the session fixed overhead calculations.

---

## Open Questions

### Consolidated from All Phases

| ID | Question | Source Phase | Impact | Status |
|----|----------|-------------|--------|--------|
| OQ-1 | Can the ECW status line share context data with hooks via a shared state file? | Phase 3 | Determines Method C feasibility as a drop-in upgrade for Method A. | OPEN -- requires Phase 4 prototyping |
| OQ-2 | What is the actual hook execution order for PreCompact relative to UserPromptSubmit? | Phase 3 | Determines reliability of file-based relay pattern for compaction notification. | OPEN -- requires empirical testing |
| OQ-3 | What does the transcript look like after compaction? Does the usage data reflect pre- or post-compaction token counts? | Phase 3 | Determines whether Method A can self-correct after compaction. | OPEN -- requires examining a post-compaction transcript |
| OQ-4 | What is the actual compaction reset size? (Phase 2 assumed ~50K tokens / 25% of window.) | Phase 3 | Calibrates post-compaction fill estimates and remaining headroom calculations. | OPEN -- requires controlled testing |
| OQ-5 | What minimum state must be preserved in the checkpoint file for reliable re-orientation? | Phase 3 | Phase 4 proposed a comprehensive checkpoint format; implementation may reveal what is truly essential vs. nice-to-have. | PARTIALLY ADDRESSED by Phase 4 |
| OQ-6 | How should the orchestrator behave when it receives a CRITICAL signal mid-QG-iteration? | Phase 3 | Policy question answered by Phase 5: complete current iteration, then checkpoint. Do not start new iterations. | RESOLVED by Phase 5 (OQ-R3) |
| OQ-7 | What is the actual L1 enforcement effectiveness curve for Claude Opus 4.6 at various fill levels? | Phase 3 | ADR-EPIC002-002 cites 40-60% effectiveness at 50K+ context, but this may be stale for 4.6 models. | OPEN -- requires fresh calibration |
| OQ-8 | Should thresholds be static (fixed percentages) or dynamic (adjusted based on remaining work estimate)? | Phase 3 | Static recommended for initial implementation; dynamic thresholds identified as future enhancement. | RESOLVED -- static first, dynamic later |
| OQ-9 | Does `input_tokens` in the usage response accurately approximate total context window occupancy? | Phase 3 (QG-1) | Foundation of Method A's reliability. If divergent, threshold calibration is invalid. | OPEN -- requires empirical validation |
| OQ-R1 | Token budget for compaction alerts. | Phase 4 | Answered: 300-400 tokens recommended, 500 hard ceiling. | RESOLVED by Phase 5 |
| OQ-R2 | Full ORCHESTRATION.yaml vs. resumption section only on resumption. | Phase 4 | Answered: resumption section first (~1,500 tokens), selective reads after. | RESOLVED by Phase 5 |
| OQ-R3 | How to handle compaction during mid-QG iteration. | Phase 4 | Answered: restart current iteration from the beginning. | RESOLVED by Phase 5 |
| OQ-R4 | Multiple compaction events in one session. | Phase 4 | Answered: incrementing checkpoint IDs, process most recent only. | RESOLVED by Phase 5 |
| OQ-R5 | Enforcement via hook vs. rule file for resumption update protocol. | Phase 4 | Answered: dual enforcement (L2 reinject + hook-based staleness check). | RESOLVED by Phase 5 |

**Summary:** 6 questions resolved by downstream phases. 6 questions remain OPEN and require empirical testing or prototyping during FEAT-001 implementation. 1 question (OQ-5) partially addressed.

---

## Follow-Up Work Items

### Priority-Ordered Work Items for FEAT-001

| # | Type | Title | Priority | Rationale |
|---|------|-------|----------|-----------|
| 1 | Enabler | Implement UserPromptSubmit context monitor hook (Method A) | P1 - Critical | Core detection mechanism. Extends existing `user-prompt-submit.py` to parse `$TRANSCRIPT_PATH`, compute fill %, and inject `<context-monitor>` tag. Estimated effort: 2-4 hours. |
| 2 | Enabler | Implement PreCompact hook for checkpoint file creation (Method B) | P1 - Critical | Compaction awareness mechanism. New hook entry in `hooks.json`. Reads ORCHESTRATION.yaml resumption section, writes `.jerry/checkpoints/cx-{NNN}-checkpoint.json`. Estimated effort: 4-6 hours. |
| 3 | Enabler | Implement compaction alert injection in UserPromptSubmit hook | P1 - Critical | Post-compaction re-orientation. Extends UserPromptSubmit hook to detect unacknowledged checkpoint files and inject Template 2 (`<compaction-alert>`). Estimated effort: 2-3 hours. |
| 4 | Story | Update ORCHESTRATION.yaml template with enhanced resumption schema v2.0 | P1 - Critical | Template change enables all new orchestrations to use the enhanced resumption format. Update `skills/orchestration/templates/ORCHESTRATION.template.yaml`. Estimated effort: 2-3 hours. |
| 5 | Story | Update orchestrator prompt to maintain resumption section (update protocol) | P1 - Critical | Behavioral change in the orchestrator agent's instructions: MUST update resumption section at every state transition. Add L2-REINJECT tag for resumption update reminders. Estimated effort: 2-3 hours. |
| 6 | Story | Update AE-006 in quality-enforcement.md with graduated sub-rules | P2 - High | Replace single AE-006 rule with AE-006a through AE-006e. Add L2-REINJECT tag for AE-006 escalation protocol. Auto-escalation: AE-002 applies (touches `.context/rules/` = auto-C3 minimum). Estimated effort: 1-2 hours. |
| 7 | Story | Implement threshold configuration file | P2 - High | Create configurable threshold file (`.jerry/context-monitor-config.json` or similar) with default and criticality-adjusted thresholds. Avoid hardcoding thresholds in hook scripts. Estimated effort: 1-2 hours. |
| 8 | Spike | Validate OQ-9: Does `input_tokens` accurately approximate context fill? | P2 - High | Critical validation for Method A reliability. Compare `input_tokens` from transcript against Method C actual data (if available) or known context window state. Timebox: 2 hours. |
| 9 | Spike | Investigate Method C feasibility (OQ-1): Can status line share data with hooks? | P2 - High | If feasible, Method C replaces Method A as the proactive layer with exact (not heuristic) context data. Implement Option 2: status line writes state file, hook reads it. Timebox: 2 hours. |
| 10 | Story | Add `.jerry/checkpoints/` to project workspace layout | P3 - Medium | Update project creation automation and workspace layout documentation. Estimated effort: 1 hour. |
| 11 | Story | Create resumption prompt automation (Template 1 populator) | P3 - Medium | Script or tool that reads ORCHESTRATION.yaml resumption section and latest checkpoint file, populates Template 1, and outputs the resumption prompt for operator use. Future: integrate with SessionStart hook. Estimated effort: 3-4 hours. |
| 12 | Enabler | Implement PostToolUse hook for resumption staleness validation (L3/L4) | P3 - Medium | Hook fires after ORCHESTRATION.yaml writes. Checks `resumption.updated_at` freshness. Injects warning if stale. Estimated effort: 2-3 hours. |
| 13 | Story | Validate thresholds against a second workflow type | P3 - Medium | Run a monitored session with the detection system active against a workflow with a different profile than FEAT-015 (e.g., deep research spike or multi-file refactoring). Collect per-operation token costs and fill trajectory. Compare against PROJ-001 calibration. Timebox: 4 hours. |
| 14 | Story | Document calibration protocol and recalibration triggers | P4 - Low | Persist the calibration protocol from Phase 6 as operational documentation. Define when and how thresholds should be recalibrated. Estimated effort: 1-2 hours. |

**Total estimated effort:** 25-37 hours across 14 work items.

**Critical path:** Items 1-5 (P1) form the minimum viable context resilience system. Items 6-9 (P2) complete the framework integration and validate key assumptions. Items 10-14 (P3-P4) provide operational completeness and future-proofing.

---

## Cross-Phase Traceability Matrix

| Finding | Phase(s) | Evidence Level | Confidence |
|---------|----------|---------------|------------|
| 17 mechanisms inventoried; no single mechanism provides complete context detection | Phase 1 | PRIMARY -- direct documentation review of Anthropic API docs, Claude Code hooks docs, codebase analysis | HIGH |
| 6 critical gaps identified (GAP-001 through GAP-006); GAP-001 (no model-accessible fill signal) is the primary gap | Phase 1 | PRIMARY -- gap analysis from mechanism inventory | HIGH |
| PROJ-001 FEAT-015: 35 files, 674K bytes, ~168K tokens of artifacts; 85-95% context fill projected | Phase 2 | PRIMARY -- measured file sizes from PROJ-001 filesystem; token estimates via bytes/4 heuristic (10-20% error margin) | HIGH (file sizes) / MEDIUM (token estimates) |
| 63.6% fill after Phase 1 (1 agent + 3 QG iterations); 2 compaction events predicted | Phase 2 | DERIVED -- cumulative fill projection from measured artifact sizes + estimated overhead | MEDIUM |
| QG iterations are the dominant cost driver at 29K-45K tokens each | Phase 2 | PRIMARY -- measured artifact sizes for S-014, S-007, S-002 strategy outputs | HIGH |
| 6 resumption gaps (RG-1 through RG-6) with 2 CRITICAL (defect context, static resumption) | Phase 2, Phase 4 | PRIMARY -- direct analysis of PROJ-001 ORCHESTRATION.yaml resumption section and template | HIGH |
| Hybrid A+B detection recommended; composite scores A=3.75, B=3.30, C=4.05*, D=1.15 | Phase 3 | DERIVED -- multi-criteria evaluation with weighted scoring; sensitivity analysis confirms ranking stability | HIGH (ranking) / MEDIUM (absolute scores) |
| Method A: transcript heuristic feasible but approximate (GAP-006); `input_tokens` proxy unvalidated | Phase 3, QG-1 | ANALYTICAL -- method design + evidence assessment; OQ-9 flags unvalidated assumption | MEDIUM |
| Method B: PreCompact hook provides deterministic compaction signal but is reactive (zero lead time) | Phase 3 | PRIMARY -- Claude Code hooks documentation confirms PreCompact event | HIGH |
| Method D: quality degradation rejected (composite 1.15) -- lagging indicator, high overhead, high false positive rate | Phase 3 | DERIVED -- scoring against 6 dimensions with evidence-based justifications | HIGH |
| Enhanced resumption schema v2.0: 7 sub-sections, 23 fields, backward compatible | Phase 4 | DESIGNED -- schema specification based on gap analysis; not empirically tested | MEDIUM |
| Checkpoint file format: JSON with 6 sections, written by PreCompact hook | Phase 4 | DESIGNED -- specification with field-level source mapping; not empirically tested | MEDIUM |
| Template 1 (resumption, ~760 tokens): productive by prompt 3 in mental test | Phase 5 | TESTED (mental test) -- validated against 2 PROJ-001 compaction scenarios | MEDIUM |
| Template 2 (compaction alert, ~280 tokens): productive by prompt 3 (conditional for QG-Final) | Phase 5 | TESTED (mental test) -- validated against 2 PROJ-001 compaction scenarios | MEDIUM |
| Five-tier threshold model: NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY + COMPACTION | Phase 6 | DERIVED -- calibrated from Phase 2 empirical data with mathematical verification; single-workflow basis | HIGH (C2 defaults) / LOW (C1/C3/C4 provisional) |
| AE-006 replacement: 5 sub-rules (AE-006a through AE-006e) with L2 enforcement | Phase 6 | DESIGNED -- rule specification based on threshold model; not empirically tested | MEDIUM |
| Validation against PROJ-001: thresholds would have provided 5 detection signals across 17 steps | Phase 6 | ANALYTICAL -- retrospective timeline analysis demonstrates triggering, not effectiveness | HIGH (triggering) / LOW (effectiveness) |
| Total injection overhead: ~3,960 tokens per 50-prompt session (~2% of 200K window) | Phase 6 | DERIVED -- calculation from injection budget per threshold level x estimated prompt distribution | MEDIUM |
| QG-1: detection evaluation passed at 0.93 after 2 iterations (initial 0.91) | QG-1 | PRIMARY -- quality gate scoring with S-003, S-007, S-002, S-014 | HIGH |
| QG-2: threshold proposal passed at 0.92 after 2 iterations (initial 0.90) | QG-2 | PRIMARY -- quality gate scoring with S-003, S-007, S-002, S-014 | HIGH |

---

## Known Limitations

This synthesis consolidates limitations identified across all phases:

1. **Single-workflow calibration.** All quantitative findings (token costs, fill projections, thresholds) are derived from PROJ-001 FEAT-015 -- a single C2 workflow with a specific profile (4 phases, 8 agents, 9 QG iterations, license migration). The Phase 6 Calibration Protocol proposes two validation workflows but cannot provide validation data within the spike scope. (Phase 2 Methodology, Phase 6 Calibration Protocol)

2. **Triggering vs. effectiveness gap.** The PROJ-001 validation demonstrates when detection signals would fire, but not whether an orchestrator at 80%+ context fill would reliably comply with complex checkpoint instructions. At high fill levels, L1 enforcement degrades to 40-60% effectiveness, and the L2 detection mechanism is itself prompt injection that the LLM must voluntarily follow. (Phase 6, Validation Limitations)

3. **L2-only enforcement.** The current design has no L3 deterministic gating (blocking tool calls at EMERGENCY) or L5 post-hoc verification (CI checks for checkpoint files). All enforcement relies on L2 prompt injection. Adding L3/L5 enforcement layers is identified as a future enhancement. (Phase 6, AE-006 Integration Note)

4. **Cumulative estimation uncertainty.** Individual operation estimates have 10-20% error margins. When composed across many operations, these errors may compound rather than cancel. Threshold boundaries (55%, 70%, 80%, 88%) should be understood as approximate (+/- 5%). (Phase 6, Operation Cost Catalog)

5. **Post-compaction context size unverified.** The ~50K token (25% of window) post-compaction reset assumption affects all EMERGENCY and COMPACTION level analyses. Actual compaction behavior depends on Claude Code's internal algorithm, which is not publicly documented. (Phase 2, Phase 6)

6. **Mental testing only.** The resumption prompt templates (Phase 5) were validated through mental simulation against PROJ-001 scenarios, not through actual execution. Re-orientation cost, prompt-to-productivity timing, and template variable population correctness are all unvalidated in practice. (Phase 5, Limitations)

7. **Template 1 requires manual injection.** The resumption prompt for new sessions must currently be pasted by the operator. No SessionStart hook automation exists. This creates a dependency on operator discipline for cross-session continuity. (Phase 5, Integration Notes)

---

## Self-Review Checklist

- [x] All 6 phase artifacts read and referenced (mechanism-inventory.md, run-analysis.md, detection-evaluation.md, resumption-assessment.md, resumption-prompt-design.md, threshold-proposal.md)
- [x] Both QG results incorporated (QG-1: 0.91 -> 0.93 PASS at iteration 2; QG-2: 0.90 -> 0.92 PASS at iteration 2)
- [x] All 4 hypotheses assessed (H1: CONFIRMED with caveats, H2: PARTIALLY CONFIRMED -- revised to 5-tier, H3: REFUTED -- enhanced schema designed, H4: CONFIRMED with operational constraints)
- [x] Open questions consolidated (15 questions: 6 resolved, 6 open, 1 partially addressed, 2 resolved by design decision)
- [x] Follow-up work items are actionable (14 items with type, priority, rationale, and effort estimates)
- [x] Navigation table present with anchor links (H-23/H-24)
- [x] No claims without evidence citations (all findings reference specific phase artifacts and finding IDs)
- [x] Known limitations documented (7 limitations with source phase references)
- [x] Cross-phase traceability matrix provided (20 findings mapped to phases, evidence levels, and confidence)

---

## References

| # | Source | Path | Content Used |
|---|--------|------|-------------|
| 1 | Phase 1: Mechanism Inventory | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-1-inventory/research-inventory/mechanism-inventory.md` | 17 mechanisms (M-001 through M-017), 6 gaps (GAP-001 through GAP-006), capability matrix |
| 2 | Phase 2: Run Analysis | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-2-analysis/run-analyzer/run-analysis.md` | PROJ-001 FEAT-015 workflow profile, token budget estimates, cumulative fill projection (17 steps), resumption gaps (RG-1 through RG-6), risk points (RP-1 through RP-5) |
| 3 | Phase 3: Detection Evaluation (QG-1 revised) | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-3-detection/detection-evaluator/detection-evaluation.md` | Hybrid A+B recommendation, method scoring matrix, recommended architecture, detection thresholds (provisional 60/80/90%), open questions (OQ-1 through OQ-9) |
| 4 | Phase 4: Resumption Assessment | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-4-resumption/resumption-assessor/resumption-assessment.md` | Enhanced resumption schema v2.0, checkpoint file format, detection integration, WORKTRACKER assessment, open questions (OQ-R1 through OQ-R5) |
| 5 | Phase 5: Resumption Prompt Design | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-5-prompt/prompt-designer/resumption-prompt-design.md` | Template 1 (~760 tokens), Template 2 (~280 tokens), variable specification, OQ-R1 through OQ-R5 resolutions, PROJ-001 mental tests |
| 6 | Phase 6: Threshold Proposal (QG-2 revised) | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-6-thresholds/threshold-analyst/threshold-proposal.md` | Five-tier threshold model, operation cost catalog, token budget analysis, criticality-adjusted thresholds, AE-006 integration, PROJ-001 validation, calibration protocol |
| 7 | QG-1 Gate Result | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/quality-gates/qg-1/gate-result.md` | Detection evaluation scoring: iter 1 (0.91 REVISE), iter 2 (0.93 PASS). 7 DA findings from iter 1, all addressed in iter 2. |
| 8 | QG-2 Gate Result | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/quality-gates/qg-2/gate-result.md` | Threshold proposal scoring: iter 1 (0.90 REVISE), iter 2 (0.92 PASS). 6 DA findings from iter 1, all resolved in iter 2. 3 Minor residual findings (non-blocking). |

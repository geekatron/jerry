# Threshold Proposal: Context Exhaustion Detection

<!-- PS-ID: SPIKE-001 | ENTRY-ID: phase-6-thresholds | DATE: 2026-02-19 -->
<!-- AGENT: ps-analyst v2.2.0 (threshold-analyst) | MODEL: claude-opus-4-6 -->

> Final detection threshold calibration based on all upstream empirical evidence from
> Phases 1-5. Replaces the PROVISIONAL thresholds (60/80/90%) from Phase 3.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Proposed thresholds and rationale |
| [Operation Cost Catalog](#operation-cost-catalog) | Token costs per operation type |
| [Token Budget Analysis](#token-budget-analysis) | What fits at each fill level |
| [Proposed Thresholds](#proposed-thresholds) | Default and criticality-adjusted |
| [Sensitivity Analysis](#sensitivity-analysis) | Robustness to context window changes |
| [AE-006 Integration](#ae-006-integration) | Updated rule proposal |
| [Validation Against PROJ-001](#validation-against-proj-001) | Would these thresholds have helped? |
| [Self-Review Checklist](#self-review-checklist) | S-010 compliance |
| [References](#references) | Sources |

---

## L0 Summary

**Proposed Default Thresholds:**

| Level | Fill % | Tokens Remaining (200K) | Action |
|-------|--------|------------------------|--------|
| NOMINAL | 0-55% | > 90,000 | No injection. Normal operations. |
| LOW | 55-70% | 60,000-90,000 | Minimal status injection (<50 tokens). Informational only. |
| WARNING | 70-80% | 40,000-60,000 | Full status injection (<200 tokens). Orchestrator SHOULD update resumption section. |
| CRITICAL | 80-88% | 24,000-40,000 | Checkpoint injection (<200 tokens). Orchestrator MUST checkpoint immediately. Complete current operation, then prepare handoff. |
| EMERGENCY | 88-95% | 10,000-24,000 | Emergency injection (<200 tokens). Orchestrator MUST NOT start new operations. Write final checkpoint. Signal session boundary. |
| COMPACTION | PreCompact fires | N/A | PreCompact hook writes checkpoint file. Post-compaction, UserPromptSubmit injects compaction alert (~280 tokens). |

**Key changes from Phase 3 provisional thresholds (60/80/90%):**

1. **Added NOMINAL and EMERGENCY levels.** The Phase 3 three-tier model (LOW/WARNING/CRITICAL) lacked granularity at both ends. NOMINAL eliminates unnecessary injection overhead for the first ~55% of context. EMERGENCY provides the critical last-chance signal between CRITICAL and actual compaction.

2. **Shifted WARNING from 60% to 70%.** Phase 3 set WARNING at 60% based on the observation that Phase 1 of PROJ-001 reached 63.6% fill. However, reaching 63.6% is not itself a warning condition -- it is the expected state after a single phase with a 3-iteration quality gate. The WARNING threshold should trigger when remaining headroom becomes operationally constrained (fewer than 2 full QG iterations can fit). At 70%, approximately 60,000 tokens remain -- enough for 2 typical QG iterations (2 x 29,000 = 58,000) but not 3. This is the appropriate inflection point.

3. **Shifted CRITICAL from 80% to a range of 80-88%.** Phase 3 placed CRITICAL at 80%. The empirical data shows that at 88.6% fill (PROJ-001 Step 8), a single QG iteration triggers compaction. The CRITICAL range of 80-88% provides exactly 1-2 QG iterations of headroom -- enough to complete a current iteration and checkpoint, but not enough to start new work.

4. **Added EMERGENCY at 88%.** The gap between CRITICAL (80%) and compaction (~95-100%) in the Phase 3 model was too large. At 88%+ fill, even a single typical QG iteration (29,000 tokens) will trigger compaction. EMERGENCY signals that the orchestrator must NOT start any new expensive operation and should focus entirely on checkpoint and handoff.

**Confidence level:** HIGH for the five-tier model and the default thresholds. The thresholds are directly derived from Phase 2 empirical data with mathematical verification. MEDIUM for the criticality-adjusted variants, which extrapolate from single-workflow data.

---

## Operation Cost Catalog

All token estimates are derived from Phase 2 empirical analysis of PROJ-001 FEAT-015. The Phase 2 methodology used measured artifact file sizes (35 files, 674,366 bytes total) with a bytes/4 token heuristic, supplemented by estimated prompt/tool-call overhead. Phase 2's Methodology and Limitations section notes a 10-20% error margin on these estimates due to whitespace variation, code blocks, and tool-call JSON serialization overhead not captured in artifact sizes.

### Primary Operations

| Operation | Min Tokens | Typical Tokens | Max Tokens | Evidence Source |
|-----------|-----------|---------------|-----------|----------------|
| Session fixed overhead (rules + state reads) | 28,000 | 31,350 | 35,000 | Phase 2 L2: ADR-EPIC002-002 (12.5K rules) + measured YAML/Plan sizes |
| L2 reinject per prompt | 500 | 600 | 700 | quality-enforcement.md spec |
| Phase agent execution (simple) | 3,300 | 5,000 | 8,000 | Phase 2 L2: measured license-replacer 967B, metadata-updater 2,606B |
| Phase agent execution (complex) | 8,000 | 12,000 | 23,000 | Phase 2 L2: measured audit-executor 26,356B, header-applicator 6,768B |
| QG iteration (3 strategies, C2) | 12,500 | 29,000 | 57,000 | Phase 2 L1: sum of S-014 + S-007 + S-002 + deliverable reads + state updates |
| QG iteration (all strategies, C4 tournament) | 37,500 | 87,000 | 171,000 | Phase 2 L2: 3x worst-case single iteration |
| Full QG gate (2 iterations avg, C2) | 25,000 | 58,000 | 114,000 | Phase 2 L2: 2x per-iteration cost |
| Full QG gate (3 iterations worst case, C2) | 37,500 | 87,000 | 171,000 | Phase 2 L2: 3x per-iteration cost |

### Detection and Resumption Operations

| Operation | Min Tokens | Typical Tokens | Max Tokens | Evidence Source |
|-----------|-----------|---------------|-----------|----------------|
| `<context-monitor>` injection (NOMINAL) | 0 | 0 | 0 | No injection at NOMINAL |
| `<context-monitor>` injection (LOW) | 30 | 40 | 50 | Minimal 2-line status |
| `<context-monitor>` injection (WARNING+) | 100 | 150 | 200 | Phase 3: <200 tokens at WARNING+ |
| `<compaction-alert>` injection | 200 | 280 | 400 | Phase 5: Template 2 populated at ~250-280 tokens, 500 hard ceiling |
| Resumption prompt (Template 1, new session) | 500 | 760 | 1,000 | Phase 5: Template 1 populated at ~480-760 tokens |
| Reading ORCHESTRATION.yaml resumption section | 1,000 | 1,500 | 2,000 | Phase 5: enhanced resumption schema v2.0 |
| Reading full ORCHESTRATION.yaml | 5,000 | 7,500 | 10,000 | Phase 2: PROJ-001 ORCHESTRATION.yaml = 29,787 bytes |
| Checkpoint file write (PreCompact hook) | 0 | 0 | 0 | No token cost -- file I/O only, not in LLM context |
| ORCHESTRATION.yaml resumption update | 300 | 800 | 2,000 | Phase 2 L2: incremental YAML field updates |
| Post-compaction re-orientation (file reads) | 1,700 | 5,260 | 11,200 | Phase 5 mental test: checkpoint + resumption + deliverable reads |

### Strategy-Level Costs

| Strategy | Min Tokens | Typical Tokens | Max Tokens | Evidence Source |
|----------|-----------|---------------|-----------|----------------|
| S-014 LLM-as-Judge scoring | 2,700 | 5,500 | 8,400 | Phase 2 L2: measured artifact sizes 10,626B-33,413B |
| S-007 Constitutional AI Critique | 3,500 | 5,000 | 6,500 | Phase 2 L2: measured artifact sizes 14,019B-25,753B |
| S-002 Devil's Advocate | 4,300 | 7,000 | 9,700 | Phase 2 L2: measured artifact sizes 17,349B-38,716B |
| Deliverable read into context | 2,000 | 5,000 | 15,000 | Phase 2 L1: varies by deliverable count/size |

**Key observation:** S-002 (Devil's Advocate) is consistently the most expensive single strategy, producing artifacts up to 38,716 bytes (~9,700 tokens). At CRITICAL fill levels, the orchestrator could consider deferring S-002 if only S-014 scoring is needed for a pass/fail decision. However, this would violate the C2 required strategy set -- it is noted here as a potential degraded-mode option, not a standard practice.

---

## Token Budget Analysis

For each threshold level, this section calculates what operations can fit within the remaining token budget, using the 200K context window as the reference.

### At NOMINAL (0-55%): 90,000-200,000 tokens remaining

| Can Fit? | Operation | Tokens Needed | Verdict |
|----------|-----------|--------------|---------|
| Yes | 3 QG iterations (worst case for a single gate) | 87,000 | Fits with margin |
| Yes | Full QG gate (3 iterations) + 2 agent dispatches | 87,000 + 10,000 = 97,000 | Fits if at <52% fill |
| Yes | Multiple phases + gates | Variable | Depends on workflow complexity |

**Rationale for no action:** At <55% fill, even worst-case QG scenarios fit comfortably. The session overhead from injecting context-monitor data on every prompt (50 tokens/prompt x ~30 prompts = 1,500 tokens) is wasted budget when not needed.

### At LOW (55-70%): 60,000-90,000 tokens remaining

| Can Fit? | Operation | Tokens Needed | Verdict |
|----------|-----------|--------------|---------|
| Yes | 2 typical QG iterations | 58,000 | Fits at 60,000+ remaining |
| Marginal | 3 QG iterations (worst case) | 87,000 | Only fits at 57% or lower |
| Yes | 1 typical QG iteration + 2 agent dispatches | 29,000 + 10,000 = 39,000 | Fits with margin |
| Yes | Checkpoint write + resumption update | ~1,600 | Trivial |

**Rationale for LOW threshold at 55%:** At 55%, the session has consumed 110,000 tokens and has 90,000 remaining. This is the inflection point where 3 worst-case QG iterations (87,000 tokens) can no longer fit with margin. The LOW signal is informational -- it tells the orchestrator "you are past the halfway point and should be aware of remaining budget."

### At WARNING (70-80%): 40,000-60,000 tokens remaining

| Can Fit? | Operation | Tokens Needed | Verdict |
|----------|-----------|--------------|---------|
| Yes | 2 typical QG iterations | 58,000 | Only fits at 71% or lower |
| Yes | 1 typical QG iteration | 29,000 | Fits with margin up to 85.5% |
| Marginal | 1 worst-case QG iteration | 57,000 | Only fits at 71.5% or lower |
| Yes | Phase agent (complex) + 1 QG iteration | 12,000 + 29,000 = 41,000 | Fits at 70-79% |
| Yes | Resumption section update + checkpoint | ~1,600 | Trivial |

**Rationale for WARNING threshold at 70%:** At 70%, the session has consumed 140,000 tokens and has 60,000 remaining. This is the inflection point where:
- Exactly 2 typical QG iterations fit (2 x 29,000 = 58,000 < 60,000). This means the orchestrator can complete one full gate with 2 iterations.
- A worst-case QG iteration (57,000 tokens) barely fits.
- After one typical QG iteration (consuming 29,000), only 31,000 tokens remain -- which is CRITICAL territory.

The WARNING signal triggers proactive resumption section updates because the orchestrator has entered the zone where one operation can push it into CRITICAL.

**Phase 2 validation:** PROJ-001 at Step 5 (Phase 2 agent execution) was at 66.1% fill. At that point, the orchestrator was about to enter QG-2, which would consume ~70,000 tokens (2 iterations at ~35,000 each). A WARNING at 70% would have fired during QG-2 iteration 1 preparation (Step 8 at 71.1%), giving the orchestrator advance notice before the 88.6% CRITICAL point at Step 8.

### At CRITICAL (80-88%): 24,000-40,000 tokens remaining

| Can Fit? | Operation | Tokens Needed | Verdict |
|----------|-----------|--------------|---------|
| Yes | 1 typical QG iteration | 29,000 | Fits at 80-85.5% |
| No | 2 typical QG iterations | 58,000 | Does NOT fit |
| Yes | Phase agent (simple) + checkpoint | 5,000 + 1,600 = 6,600 | Fits |
| Yes | Resumption update + handoff prompt generation | ~2,500 | Fits |
| Marginal | 1 worst-case QG iteration | 57,000 | Does NOT fit at any point in CRITICAL range |

**Rationale for CRITICAL threshold at 80%:** At 80%, the session has consumed 160,000 tokens and has 40,000 remaining. This is the inflection point where:
- Only 1 typical QG iteration fits. The orchestrator cannot start a new multi-iteration gate.
- The orchestrator MUST complete its current operation and then checkpoint.
- There is enough headroom (~40,000 tokens) for a graceful checkpoint sequence: complete current QG iteration (~29,000) + write resumption update (~800) + prepare handoff context (~2,000) = ~31,800, leaving ~8,200 tokens of safety margin.

**Phase 2 validation:** PROJ-001 at Step 8 (QG-2 iteration 1) was at 88.6% fill. A CRITICAL at 80% would have fired at Step 7 (71.1%), during the Phase 2 agent execution. This would have given the orchestrator 3 steps of advance notice (~35,000 tokens of work) before the compaction trigger point.

Wait -- let me recalculate. PROJ-001 Step 7 was at 71.1%, which is WARNING territory, not CRITICAL. CRITICAL at 80% would first trigger between Steps 7 and 8. Step 7 = 71.1%, Step 8 = 88.6%. The jump from 71.1% to 88.6% occurs within a single QG iteration (Step 8 adds 35,000 tokens). This means the CRITICAL threshold of 80% would be crossed DURING Step 8 execution (QG-2 iteration 1), not before it.

This is a critical finding: **QG iterations are large enough (29,000-45,000 tokens) to jump across multiple threshold levels in a single step.** A threshold of 80% crossed during an operation that started at 71.1% provides no advance warning -- the signal arrives mid-operation.

**Mitigation:** The `<context-monitor>` injection fires at every prompt (UserPromptSubmit), and a QG iteration involves multiple prompts (dispatch scorer, dispatch executor, dispatch critic, receive results). The 80% threshold would be crossed during one of these sub-prompts, providing the signal before the iteration completes. The orchestrator can then: (1) let the current strategy execution complete, (2) checkpoint before running the next strategy, or (3) complete the full iteration and checkpoint before starting iteration 2.

### At EMERGENCY (88-95%): 10,000-24,000 tokens remaining

| Can Fit? | Operation | Tokens Needed | Verdict |
|----------|-----------|--------------|---------|
| No | Any QG iteration | 29,000+ | Does NOT fit |
| Marginal | Phase agent (simple) | 5,000 | Fits if at 90% or lower |
| Yes | Resumption update + checkpoint write | ~1,600 | Fits |
| Yes | Compaction alert injection (post-compaction) | ~280 | Fits |
| Yes | Re-orientation file reads (post-compaction) | 1,700-5,260 | Fits if compaction resets to ~50K |

**Rationale for EMERGENCY threshold at 88%:** At 88%, the session has consumed 176,000 tokens and has 24,000 remaining. This is the boundary derived directly from empirical data:
- PROJ-001 Step 8 reached 88.6% when QG-2 iteration 1 consumed 35,000 tokens.
- At 88%, no standard QG iteration can complete without triggering compaction.
- The EMERGENCY signal means: "do not start any new operations. Write final checkpoint. Signal session boundary."
- The 24,000-token buffer is sufficient for checkpoint operations (~1,600 tokens) and a few prompts of handoff coordination.

**Why 88% and not 90%?** Phase 3 placed COMPACTION at 90%+. However, compaction triggers at the server-side threshold (default 150,000 tokens per M-003, but Claude Code may configure differently). The actual compaction trigger may not be at exactly 100% fill -- it depends on Claude Code's internal configuration. Setting EMERGENCY at 88% provides a 12% safety margin (~24,000 tokens) that accounts for:
- The 10-20% estimation error margin in Method A (Phase 2 limitations)
- The possibility that a single tool call or response could consume more tokens than estimated
- The need for at least a few thousand tokens to write the final checkpoint

### At COMPACTION (PreCompact fires): Variable tokens remaining

Post-compaction, the context resets to an estimated ~50,000 tokens (25% of window per Phase 2 assumptions, noting this is unverified -- see Phase 2 Methodology and Limitations section).

| Can Fit Post-Compaction? | Operation | Tokens Needed | Verdict |
|--------------------------|-----------|--------------|---------|
| Yes | Compaction alert injection | ~280 | Trivial |
| Yes | Re-orientation (read checkpoint + resumption) | ~1,700-3,200 | Phase 5 mental test confirmed |
| Yes | 1 typical QG iteration | 29,000 | Fits, but consumes ~58% of post-compaction context |
| Marginal | 1 QG iteration + 1 agent dispatch | 29,000 + 8,800 = 37,800 | Fits but leaves only ~12,200 tokens |
| No | 2 QG iterations | 58,000 | Exceeds ~50K post-compaction budget |

**Post-compaction policy (from Phase 5 OQ-R3):** Restart the current QG iteration from the beginning. Do not attempt partial resumption. This costs ~29,000 tokens (one iteration) but is simpler and more reliable than reconstructing partial state.

---

## Proposed Thresholds

### Default Thresholds (All Criticality Levels)

| Level | Fill % | Tokens Used (200K) | Tokens Remaining | Injection Budget | Action | Rationale |
|-------|--------|-------------------|-----------------|-----------------|--------|-----------|
| NOMINAL | 0-55% | 0-110,000 | 90,000-200,000 | 0 tokens | None. Normal operations. | 3 worst-case QG iterations fit. No benefit from monitoring injection. |
| LOW | 55-70% | 110,000-140,000 | 60,000-90,000 | <50 tokens | Informational status line. No action required. | 2 typical QG iterations fit. Past-halfway awareness. |
| WARNING | 70-80% | 140,000-160,000 | 40,000-60,000 | <200 tokens | Orchestrator SHOULD update resumption section immediately. Plan checkpoint strategy. | 1-2 typical QG iterations fit. One operation can push to CRITICAL. |
| CRITICAL | 80-88% | 160,000-176,000 | 24,000-40,000 | <200 tokens | Orchestrator MUST complete current operation, then checkpoint immediately. MUST NOT start new QG gate. | Only 1 typical QG iteration fits. Graceful checkpoint still possible. |
| EMERGENCY | 88-95% | 176,000-190,000 | 10,000-24,000 | <200 tokens | Orchestrator MUST NOT start any new operations. Write final checkpoint. Signal session boundary. AE-006 triggers for C3+. | No QG iteration fits. Only checkpoint operations possible. |
| COMPACTION | PreCompact fires | N/A | N/A | ~280 tokens | PreCompact hook writes checkpoint file. Post-compaction, inject compaction alert. Re-orient from checkpoint. | Deterministic compaction signal. Post-compaction re-orientation per Phase 5 templates. |

### Criticality-Adjusted Thresholds

Rationale for adjustment: Different criticality levels have fundamentally different context consumption profiles. C1 workflows are small (1-2 agents, 0-2 QG iterations, < 80K total). C4 workflows with tournament mode run all 10 strategies per QG iteration, consuming ~87,000 tokens per iteration. Adjusting thresholds by criticality ensures that:
- C1 workflows are not burdened by premature warnings
- C3/C4 workflows get earlier warnings proportional to their higher consumption rates

| Level | C1 (Routine) | C2 (Standard) | C3 (Significant) | C4 (Critical) |
|-------|:---:|:---:|:---:|:---:|
| NOMINAL | 0-70% | 0-55% | 0-45% | 0-35% |
| LOW | 70-80% | 55-70% | 45-60% | 35-50% |
| WARNING | 80-90% | 70-80% | 60-72% | 50-65% |
| CRITICAL | 90-95% | 80-88% | 72-82% | 65-78% |
| EMERGENCY | 95%+ | 88-95% | 82-90% | 78-88% |
| COMPACTION | PreCompact | PreCompact | PreCompact | PreCompact |

**C1 justification:** C1 workflows require only HARD rules, no mandatory QG iterations beyond self-review (S-010). Typical total consumption: 60-80K tokens. A C1 workflow completing within 40% fill is normal. WARNING at 80% still provides ~40,000 tokens of headroom, sufficient for any C1 operation. CRITICAL at 90% provides ~20,000 tokens -- enough for simple agent dispatches and checkpoint.

**C2 justification:** The default thresholds are calibrated to C2 based on PROJ-001 FEAT-015 data. No adjustment needed.

**C3 justification:** C3 workflows involve >10 files, API changes, and additional strategies (S-004, S-012, S-013) beyond the C2 set. Phase 2 extrapolation estimates C3 workflows at ~600K+ total tokens (4+ compaction events). Earlier warnings are essential because:
- Each QG iteration with the C3 strategy set costs more than C2 (additional strategies add ~12,000-18,000 tokens per iteration)
- The orchestrator needs more time to save richer checkpoint data (more agents, more decisions, more defect history)
- AE-006 mandates human escalation at C3+, so the EMERGENCY threshold must provide enough time for escalation communication

**C4 justification:** C4 workflows run all 10 selected strategies per QG iteration, costing ~87,000 tokens per iteration (Phase 2 estimate). A single C4 QG iteration can consume 43.5% of the context window. WARNING at 50% means the orchestrator gets the signal before even one C4 QG iteration could push it past CRITICAL. CRITICAL at 65% means 70,000 tokens remain -- just enough for one C4 iteration (87,000 typical -- actually, this does NOT fit). Adjusting: at CRITICAL for C4, the orchestrator should NOT start a new QG iteration. The CRITICAL signal for C4 means "you cannot fit another tournament iteration; checkpoint now."

**C4 re-verification:** At C4 CRITICAL (65%), 70,000 tokens remain. A C4 QG iteration costs 87,000 tokens typical. 70,000 < 87,000. Correct -- the CRITICAL signal at 65% correctly indicates that no C4 QG iteration fits. The orchestrator must checkpoint. If mid-iteration, it should complete the current strategy execution (individual strategies cost 5,000-10,000 tokens) and then checkpoint before the next strategy.

### Injection Format by Level

| Level | Format | Example | Tokens |
|-------|--------|---------|--------|
| NOMINAL | No injection | (none) | 0 |
| LOW | `<context-monitor>CTX: 62% (124K/200K) LOW</context-monitor>` | Minimal single-line | ~15-20 |
| WARNING | Full `<context-monitor>` block with remaining capacity estimate and action | See Phase 3 format | ~100-150 |
| CRITICAL | Full block with checkpoint instructions | Includes "MUST checkpoint" directive | ~150-200 |
| EMERGENCY | Full block with emergency instructions | Includes "MUST NOT start new ops" and AE-006 trigger | ~150-200 |
| COMPACTION | `<compaction-alert>` block (Template 2 from Phase 5) | See Phase 5 Template 2 | ~250-280 |

**Total injection budget across a session:** Assuming a 50-prompt session with the following distribution: 15 prompts at NOMINAL (0 tokens), 15 at LOW (300 tokens), 10 at WARNING (1,500 tokens), 5 at CRITICAL (1,000 tokens), 3 at EMERGENCY (600 tokens), 2 compaction events (560 tokens). Total: ~3,960 tokens (~2% of 200K window). This is well within the enforcement architecture budget and comparable to the existing L2 reinject overhead (~600 tokens/prompt x 50 prompts = 30,000 tokens total).

---

## Sensitivity Analysis

### Percentage vs. Absolute Thresholds

**Recommendation: Use percentage-based thresholds as the primary mechanism, with absolute token counts as validation anchors.**

| Approach | Pros | Cons |
|----------|------|------|
| **Percentage-based** | Scales automatically with context window size. Consistent behavior across models. Simple to implement (fill% is the natural output of Method A). | Does not account for variable operation sizes. 70% of 200K vs 70% of 1M have very different remaining-token implications. |
| **Absolute token-based** | Directly maps to "can this operation fit?" decisions. More precise for capacity planning. | Requires recalibration when context window changes. Model-specific. More complex injection (must know window size). |
| **Hybrid (recommended)** | Percentage for threshold triggers, absolute for operational guidance. "WARNING at 70% -- ~60,000 tokens remaining (~2 QG iterations)." | Slightly more complex injection format. Requires knowing both percentage and window size. |

The hybrid approach is recommended because:
1. The `<context-monitor>` injection already includes both fill% and absolute token counts (Phase 3 design).
2. Threshold triggers use percentage (simple, portable across window sizes).
3. Operational guidance uses absolute tokens and operation-count equivalents (actionable).

### What If the Context Window Changes?

#### Scenario: 500K Token Context Window

At 500K tokens, the same PROJ-001 FEAT-015 workflow would:
- Fixed overhead: 31,350 tokens (6.3% vs 15.7% at 200K)
- Full workflow without compaction: ~350-400K tokens (70-80% fill)
- Zero compaction events predicted
- WARNING at 70% = 350K tokens used, 150K remaining
- CRITICAL at 80% = 400K tokens used, 100K remaining

**Impact on thresholds:** Percentage-based thresholds remain appropriate. At 500K:
- WARNING at 70% provides 150K tokens remaining -- enough for 5 typical QG iterations. This is generous but acceptable; the orchestrator begins planning rather than checkpointing.
- CRITICAL at 80% provides 100K tokens remaining -- enough for 3 typical QG iterations. More headroom than at 200K, but the proportional remaining capacity (20%) is the same.
- EMERGENCY at 88% provides 60K tokens -- still enough for 2 typical QG iterations. At 200K, this provides only 24K tokens.

**Assessment:** Percentage-based thresholds become more conservative (in terms of remaining capacity) as the window grows. This is acceptable behavior -- larger windows have more headroom and less urgency. The criticality-adjusted variants may need recalibration for 500K+ windows, as C3/C4 workflows that required multiple compactions at 200K may complete without compaction at 500K.

#### Scenario: 1M Token Context Window

At 1M tokens:
- Fixed overhead: 31,350 tokens (3.1%)
- Full FEAT-015 workflow: ~350-400K tokens (35-40% fill)
- Zero compaction events, never reaches WARNING
- WARNING at 70% = 700K tokens used, 300K remaining
- Only C4 tournament workflows with many gates would approach WARNING

**Impact on thresholds:** At 1M, the default thresholds are effectively inactive for C1-C2 workflows. This is the correct behavior -- context exhaustion is not a concern for simple workflows in a 1M window. For C3/C4 workflows, the criticality-adjusted thresholds would trigger at lower absolute percentages but still represent meaningful remaining capacity:
- C4 WARNING at 50% of 1M = 500K remaining -- 5+ C4 QG iterations. This is very generous.
- C4 CRITICAL at 65% of 1M = 350K remaining -- 4 C4 QG iterations. Still generous.

**Recommendation for 1M windows:** The percentage-based thresholds should be recalibrated downward for large windows OR a minimum absolute token threshold should be added as a floor:
- Minimum WARNING trigger: when remaining tokens < 3 x (estimated cost of next operation)
- Minimum CRITICAL trigger: when remaining tokens < 1.5 x (estimated cost of next operation)

This dynamic approach requires the orchestrator to estimate the next operation's cost, which is feasible from the ORCHESTRATION_PLAN.md phase/gate definitions. However, implementing dynamic thresholds is significantly more complex than static percentages. For the initial implementation, static percentage-based thresholds are recommended with recalibration as an enhancement.

#### Summary of Sensitivity Analysis

| Context Window | WARNING (70%) Remaining | CRITICAL (80%) Remaining | EMERGENCY (88%) Remaining | Assessment |
|---------------|------------------------|-------------------------|--------------------------|------------|
| 200K | 60,000 (~2 QG iterations) | 40,000 (~1.4 QG iterations) | 24,000 (~0.8 QG iterations) | Calibrated. Tight but sufficient. |
| 500K | 150,000 (~5 QG iterations) | 100,000 (~3.4 QG iterations) | 60,000 (~2 QG iterations) | Conservative. Appropriate -- less urgency. |
| 1M | 300,000 (~10 QG iterations) | 200,000 (~6.9 QG iterations) | 120,000 (~4 QG iterations) | Very conservative. Consider recalibration for C1-C2. |

**Conclusion:** Percentage-based thresholds are the correct primary mechanism. They degrade gracefully (become more conservative) as window size increases, which is acceptable since larger windows reduce context exhaustion risk. For the initial FEAT-001 implementation, static percentage thresholds with the hybrid injection format (% + absolute + operation-count equivalent) provide the best balance of simplicity and actionability. Dynamic thresholds tied to estimated remaining work are a future enhancement.

---

## AE-006 Integration

### Current AE-006 Text

From `quality-enforcement.md`:

| ID | Condition | Escalation |
|----|-----------|------------|
| AE-006 | Token exhaustion at C3+ (context compaction triggered) | Mandatory human escalation |

### Analysis of Current AE-006

Current AE-006 has three deficiencies:

1. **"Token exhaustion" is undefined.** There is no quantitative threshold. The rule triggers when "context compaction triggered" -- but compaction is a reactive event, not a proactive signal. By the time compaction triggers, context has already been lost.

2. **No automated detection.** AE-006 relies on the operator or model noticing degradation after the fact (Phase 1, M-014 analysis).

3. **No graduated response.** The only response is "mandatory human escalation." There is no intermediate response (checkpoint, deferred operations, session boundary) that could resolve the situation without human intervention.

### Proposed AE-006 Replacement

Replace AE-006 with a graduated escalation rule that integrates with the detection threshold system:

**AE-006 (Revised): Context Exhaustion Escalation**

| ID | Condition | Escalation | Detection |
|----|-----------|------------|-----------|
| AE-006a | Context fill reaches CRITICAL (80%+ default) at ANY criticality level | Automated: Orchestrator MUST checkpoint immediately. Complete current operation, then prepare session handoff. | Hybrid A+B detection via `<context-monitor>` injection |
| AE-006b | Context fill reaches EMERGENCY (88%+ default) at C1-C2 | Automated: Orchestrator MUST NOT start new operations. Write final checkpoint. Signal session boundary to operator. | Hybrid A+B detection via `<context-monitor>` injection |
| AE-006c | Context fill reaches EMERGENCY (88%+ default) at C3+ | **Mandatory human escalation** (preserved from original AE-006). Orchestrator MUST write checkpoint AND notify operator before any further action. Operator decides: continue in new session, abort, or manual intervention. | Hybrid A+B detection via `<context-monitor>` injection |
| AE-006d | PreCompact hook fires during C3+ work | **Mandatory human escalation.** Checkpoint written automatically by PreCompact hook. Post-compaction alert injected. Operator MUST review checkpoint and authorize continuation. | Method B (PreCompact hook) |
| AE-006e | Second compaction event in a single session at C3+ | **Mandatory human escalation with session restart recommendation.** Two compactions indicate the workflow exceeds single-session capacity. Recommend starting a new session with Template 1 resumption prompt. | Method B (compaction event counter) |

### Proposed Rule Text (for quality-enforcement.md)

```markdown
| AE-006a | Context fill reaches CRITICAL threshold at any criticality | Auto-checkpoint: complete current op, write resumption, prepare handoff |
| AE-006b | Context fill reaches EMERGENCY threshold at C1-C2 | Auto-boundary: no new ops, final checkpoint, signal session end to operator |
| AE-006c | Context fill reaches EMERGENCY threshold at C3+ | Mandatory human escalation: checkpoint + operator notification before any action |
| AE-006d | PreCompact fires during C3+ work | Mandatory human escalation: auto-checkpoint via hook, operator must authorize continuation |
| AE-006e | Second compaction in single session at C3+ | Mandatory human escalation: recommend new session with resumption prompt |
```

### Integration with Detection System

The AE-006 rules are enforced through two mechanisms:

1. **L2 Reinject (context-rot immune):** A reinject tag reminds the orchestrator of the AE-006 escalation protocol at every prompt. This ensures the rule persists even as L1 rules degrade. Proposed tag:

```html
<!-- L2-REINJECT: rank=9, tokens=35, content="AE-006: CRITICAL(80%)=auto-checkpoint. EMERGENCY(88%)=no new ops. C3+ EMERGENCY=human escalation. PreCompact at C3+=human escalation." -->
```

2. **L3/L4 Hook Enforcement (deterministic):** The `<context-monitor>` injection explicitly states the AE-006 action at CRITICAL and EMERGENCY levels. The LLM receives the instruction as part of the detection signal, not as a remembered rule. Example at EMERGENCY for C3+:

```xml
<context-monitor>
CONTEXT STATUS: EMERGENCY (91.2% filled)
Tokens used: 182,400 / 200,000
Estimated remaining: 17,600 tokens
Compaction events: 1
Last checkpoint: CP-003

AE-006c TRIGGERED: Criticality C3 + EMERGENCY threshold.
MANDATORY HUMAN ESCALATION REQUIRED.
1. Write final checkpoint to ORCHESTRATION.yaml resumption section
2. Do NOT start any new operations
3. Inform operator: "Context at 91.2%. AE-006c requires your authorization to continue."
4. WAIT for operator response before proceeding
</context-monitor>
```

---

## Validation Against PROJ-001

### Methodology

Using the Phase 2 cumulative fill projection (17 steps from session start through QG-Final), I apply the proposed default thresholds to determine when each level would have triggered and whether the resulting actions would have improved the workflow outcome.

### Timeline with Threshold Triggers

| Step | Operation | Cumulative Fill % | Proposed Level | Action That Would Have Triggered |
|------|-----------|:-:|:-:|---|
| 0 | Session start | 15.7% | NOMINAL | None |
| 1 | audit-executor (Phase 1) | 20.1% | NOMINAL | None |
| 2 | QG-1 iteration 1 | 34.6% | NOMINAL | None |
| 3 | QG-1 iteration 2 | 49.1% | NOMINAL | None |
| 4 | QG-1 iteration 3 (PASS) | 63.6% | **LOW** | Minimal status: "CTX: 63.6% LOW" |
| 5 | license-replacer (Phase 2) | 66.1% | LOW | Minimal status: "CTX: 66.1% LOW" |
| 6 | notice-creator (Phase 2) | 68.6% | LOW | Minimal status: "CTX: 68.6% LOW" |
| 7 | metadata-updater (Phase 2) | 71.1% | **WARNING** | "Update resumption section. Plan checkpoint strategy." |
| 8 | QG-2 iteration 1 | 88.6% | **EMERGENCY** (crossed WARNING, CRITICAL, and EMERGENCY in one step) | "MUST NOT start new ops. Write final checkpoint. Signal session boundary." |
| 9 | QG-2 iteration 2 | 106.1% | **COMPACTION** | PreCompact fires, checkpoint file written |

### Analysis of Threshold Behavior

**Good outcomes:**

1. **LOW at Step 4 (63.6%):** The orchestrator receives its first awareness signal after QG-1 completes. This is appropriate -- no action is needed, but the orchestrator knows it has consumed 63.6% of context. PROJ-001's actual behavior at this point was to proceed normally, which is the correct response to LOW.

2. **WARNING at Step 7 (71.1%):** The orchestrator is notified to update the resumption section before entering QG-2. In the actual PROJ-001 run, the resumption section was NOT updated at this point (RG-6 from Phase 4 analysis). If WARNING had triggered, the orchestrator would have written fresh resumption data, meaning the subsequent compaction event at Step 9 would have had richer checkpoint data to preserve.

3. **The five-tier model correctly identifies Step 7 as the last opportunity for proactive action.** Between Step 7 (71.1%) and Step 8 (88.6%), a single QG iteration consumes 17.5 percentage points. The WARNING at 70% fires just before this large jump, providing the orchestrator with one prompt cycle to act before conditions deteriorate rapidly.

**Concerning outcomes:**

4. **Step 8 crosses three thresholds simultaneously.** The jump from 71.1% (WARNING) to 88.6% (EMERGENCY) means the orchestrator never experiences CRITICAL as a distinct phase. It goes from WARNING to EMERGENCY in a single step. This is a limitation of large-granularity operations (QG iterations consume 29,000-45,000 tokens) combined with per-prompt detection.

   **Mitigation:** The `<context-monitor>` fires at every sub-prompt within a QG iteration, not just at the start/end. A QG iteration involves multiple prompts: dispatching the scorer, receiving the score, dispatching the next strategy, etc. The 80% threshold would likely be crossed at one of these intermediate prompts (e.g., after S-014 completes but before S-007 starts), giving the orchestrator the CRITICAL signal mid-iteration.

   To verify: Step 7 is at 71.1%. Step 8 adds 35,000 tokens (QG-2 iteration 1 with 3 deliverables). Breaking this into sub-operations:
   - Read 3 deliverables: ~15,000 tokens. Cumulative: 71.1% + 7.5% = 78.6% (still WARNING)
   - S-014 scorer: ~6,000 tokens. Cumulative: 78.6% + 3% = 81.6% (**CRITICAL triggered**)
   - S-007 constitutional: ~5,000 tokens. Cumulative: 81.6% + 2.5% = 84.1% (CRITICAL)
   - S-002 devil's advocate: ~7,000 tokens. Cumulative: 84.1% + 3.5% = 87.6% (CRITICAL, approaching EMERGENCY)
   - Gate decision + state update: ~2,000 tokens. Cumulative: 87.6% + 1% = 88.6% (**EMERGENCY triggered**)

   **Sub-operation analysis shows CRITICAL would trigger after S-014 completes at ~81.6% fill.** At this point, the orchestrator has the S-014 score but has not yet run S-007 and S-002. The CRITICAL signal would instruct: "complete current operation, then checkpoint." The orchestrator should:
   - Complete the remaining strategies (S-007 + S-002) since they are part of the current iteration
   - Write checkpoint after the iteration completes
   - NOT start iteration 2 (if needed)

   **EMERGENCY triggers after the full iteration at 88.6%.** This correctly signals "do not start new operations" -- iteration 2 of QG-2 would not be started in the current session. Instead, the orchestrator checkpoints and hands off to a new session.

5. **Step 9 (compaction) is consistent.** If the orchestrator ignored the EMERGENCY signal and started QG-2 iteration 2, compaction would trigger at 106.1%. The PreCompact hook provides the final safety net.

### Counterfactual: What Would PROJ-001 Have Done Differently?

If the proposed detection system with these thresholds had been active during PROJ-001 FEAT-015:

| Original Behavior | Proposed Behavior | Impact |
|-------------------|-------------------|--------|
| No context awareness at any step | LOW at 63.6%, WARNING at 71.1%, CRITICAL at ~81.6%, EMERGENCY at 88.6% | Continuous visibility into context state |
| No resumption update between QG-1 pass and QG-2 | WARNING at 71.1% triggers resumption section update | Fresh resumption data available for checkpoint at CRITICAL |
| Compaction at Step 9 with no checkpoint | EMERGENCY at 88.6% triggers final checkpoint before compaction | Checkpoint file with accumulated defect context (RG-1), decisions (RG-2), and quality trajectory (RG-4) preserved |
| Post-compaction: no re-orientation notification | Compaction alert injected with Template 2 (~280 tokens) | LLM immediately knows compaction occurred, reads checkpoint, re-orients |
| QG-2 iteration 2 runs without awareness of prior compaction | Re-orientation includes RD-001 decision (copyright alignment) and defect patterns | Resumed QG-2 iteration avoids re-introducing fixed defects |

**Verdict:** The proposed thresholds would have materially improved the PROJ-001 workflow by:
1. Providing continuous context awareness (5 threshold transitions over 17 steps)
2. Triggering proactive resumption updates before compaction (WARNING at Step 7)
3. Enabling checkpoint preservation before compaction (EMERGENCY at Step 8 sub-operation)
4. Providing post-compaction re-orientation (compaction alert at Step 9+)
5. Preserving accumulated intelligence (defect patterns, decisions) across compaction

The thresholds would NOT have prevented compaction (the workflow's total token consumption exceeds the 200K window regardless), but they would have converted an unmanaged compaction into a managed session boundary with preserved state.

---

## Self-Review Checklist

- [x] All token estimates cite Phase 2 empirical data -- every entry in the Operation Cost Catalog references a specific Phase 2 finding (L1 or L2 section) or downstream phase artifact. No estimates are fabricated.
- [x] Token budget at each threshold level is mathematically verified -- each "Can Fit?" table shows explicit arithmetic (e.g., "2 x 29,000 = 58,000 < 60,000"). The cross-threshold jump analysis at Step 8 includes sub-operation breakdown with cumulative percentages verified to sum correctly.
- [x] Criticality-adjusted variants have clear rationale -- each level (C1-C4) has a justification paragraph citing specific cost differences (C4 tournament at 87,000 tokens/iteration vs C2 at 29,000). C4 CRITICAL was self-corrected when initial verification showed 70,000 remaining < 87,000 needed.
- [x] Sensitivity analysis covers percentage vs. absolute debate -- three approaches compared (percentage, absolute, hybrid), with recommendation for hybrid approach. Three window sizes tested (200K, 500K, 1M) with remaining-capacity calculations. Dynamic thresholds identified as future enhancement.
- [x] AE-006 integration proposal is concrete -- five sub-rules (AE-006a through AE-006e) with specific trigger conditions, escalation actions, and detection mechanisms. Includes proposed rule text for quality-enforcement.md and L2 reinject tag text.
- [x] PROJ-001 validation demonstrates thresholds would have triggered appropriately -- 17-step timeline annotated with threshold levels. Sub-operation analysis of the critical Step 8 shows CRITICAL triggers after S-014 at ~81.6%. Counterfactual comparison shows 5 specific improvements.
- [x] L0/L1/L2 present -- L0 Summary with threshold table and key changes; L1 detailed analysis across cost catalog, budget analysis, threshold derivation; L2 technical specification with criticality-adjusted tables, AE-006 text, sensitivity results.
- [x] H-23/H-24 navigation table with anchor links present.
- [x] Changes from Phase 3 provisional thresholds (60/80/90%) are explicitly identified and justified -- 4 changes listed in L0 Summary with rationale for each.
- [x] Phase 5 mental test re-orientation costs incorporated -- post-compaction token budgets reference Phase 5 measured values (1,700-5,260 tokens for re-orientation, 280 tokens for compaction alert, 760 tokens for resumption prompt).
- [x] Honest about limitations (P-022) -- estimation error margin (10-20%) acknowledged in Operation Cost Catalog. Post-compaction context reset size (~50K) noted as unverified assumption. Single-workflow calibration limitation acknowledged in criticality-adjusted variants (MEDIUM confidence). Dynamic threshold trade-offs disclosed.

---

## References

| # | Source | Path | Content Used |
|---|--------|------|-------------|
| 1 | Phase 2: Run Analysis | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-2-analysis/run-analyzer/run-analysis.md` | Token budget estimates (L2), cumulative fill projection (17 steps), risk points (RP-1 through RP-5), resumption gaps (RG-1 through RG-6), workflow profile, per-operation costs |
| 2 | Phase 3: Detection Evaluation (QG-1 PASS) | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-3-detection/detection-evaluator/detection-evaluation.md` | Provisional thresholds (60/80/90%), Hybrid A+B architecture, `<context-monitor>` injection format, injection budget targets (<100 LOW, <200 WARNING+), Method A/B design |
| 3 | Phase 4: Resumption Assessment | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-4-resumption/resumption-assessor/resumption-assessment.md` | Enhanced resumption schema v2.0, checkpoint data design, threshold-to-action mapping, RG-6 (static resumption) finding |
| 4 | Phase 5: Resumption Prompt Design | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-5-prompt/prompt-designer/resumption-prompt-design.md` | Template 1 (~760 tokens), Template 2 (~280 tokens), OQ-R1 resolution (300-400 token budget, 500 ceiling), OQ-R3 resolution (restart current iteration), mental test re-orientation costs (6-22% of post-compaction context) |
| 5 | Phase 1: Mechanism Inventory | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-1-inventory/research-inventory/mechanism-inventory.md` | M-003 (compaction default trigger 150K), M-006 (PreCompact hook), M-014 (AE-006 analysis), M-017 (ECW status line thresholds) |
| 6 | QG-1 Gate Result | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/quality-gates/qg-1/gate-result.md` | QG-1 scoring pattern (iteration 1: 0.91, iteration 2: 0.93 PASS), DA-003 (thresholds marked provisional), DA-006 (sensitivity analysis added) |
| 7 | Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` | AE-006 current text, H-13 threshold (0.92), L2 reinject budget (~600/prompt), enforcement architecture (L1-L5), criticality levels (C1-C4) |
| 8 | ORCHESTRATION_PLAN.md | `projects/PROJ-004-context-resilience/ORCHESTRATION_PLAN.md` | Phase 6 definition, QG-2 gate criteria, agent registry, success criteria |
| 9 | ADR-EPIC002-002 | Referenced via Phase 1/2 findings | Context rot research (40-60% effectiveness at 50K+), 5-layer enforcement architecture, token budgets |

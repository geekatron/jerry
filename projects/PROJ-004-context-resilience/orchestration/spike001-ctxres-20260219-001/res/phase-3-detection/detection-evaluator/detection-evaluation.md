# Detection Method Evaluation: Context Exhaustion Detection

<!-- PS-ID: SPIKE-001 | ENTRY-ID: phase-3-detection | DATE: 2026-02-19 -->
<!-- AGENT: ps-analyst v2.2.0 (detection-evaluator) | MODEL: claude-opus-4-6 -->

> Comparative evaluation of four detection methods for context exhaustion in Claude Code
> orchestration workflows. Produces a scored recommendation with implementation architecture.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Executive recommendation and key trade-offs |
| [Method Profiles](#method-profiles) | Detailed analysis of each detection method |
| [Scoring Matrix](#scoring-matrix) | Comparative scoring across 6 dimensions |
| [Weighted Composite Scores](#weighted-composite-scores) | Weighted ranking and recommendation |
| [Recommended Architecture](#recommended-architecture) | Design of the hybrid approach |
| [Risk Assessment](#risk-assessment) | What could fail with the recommendation |
| [Open Questions](#open-questions) | For Phases 4-6 to resolve |
| [Self-Review Checklist](#self-review-checklist) | S-010 compliance verification |
| [References](#references) | Source traceability |

---

## L0 Summary

**Recommendation: Hybrid of Method A (Token Counting Heuristic) + Method B (Compaction Detection), with Method C (ECW Status Line) as a stretch goal pending feasibility verification.**

The evaluation finds that no single detection method provides both proactive early warning and deterministic compaction awareness. Method A (transcript-based token heuristic) scores highest overall due to its proactive nature, low overhead, and proven implementation pathway via the existing `UserPromptSubmit` hook. Method B (PreCompact hook detection) is essential as a complementary reactive layer because it provides the only deterministic compaction signal. Method D (quality degradation) is rejected as a primary detection mechanism due to its lagging nature and high false-positive rate.

Method C (ECW Status Line data) would be the ideal solution -- it provides actual `context_window.current_usage` data from Claude Code -- but its feasibility depends on whether hook scripts can access the same JSON feed that the status line script receives. This is an unresolved question (GAP-003 from Phase 1). If Method C proves feasible, it supersedes Method A as the primary proactive layer.

**Key trade-off:** Method A is implementable today with known mechanisms but provides approximate data (GAP-006). Method C provides exact data but requires investigation into data accessibility. The hybrid architecture is designed so that Method C can replace Method A as a drop-in upgrade without changing the overall detection flow.

**Confidence level:** HIGH for the hybrid A+B recommendation. MEDIUM for Method C feasibility (requires Phase 4 prototyping to verify).

---

## Method Profiles

### Method A: Token Counting Heuristic (Transcript-Based)

**How it works:**
1. A `UserPromptSubmit` command hook script parses the `$TRANSCRIPT_PATH` JSONL file
2. The script sums token usage data from the `usage` objects in each transcript entry (`input_tokens` + `output_tokens` per turn)
3. The most recent turn's `input_tokens` value is used as the best available proxy for current context fill (since `input_tokens` in each API response reflects the total input sent for that turn, which approximates context window occupancy). Note: The equation `input_tokens` ≈ context window occupancy is a plausible interpretation but has not been empirically validated. Phase 4 prototyping should include a verification step comparing `input_tokens` with actual context fill (e.g., via Method C data if available).
4. The fill percentage is computed against the known 200K context window size
5. The result is injected as `additionalContext` via the hook output, making it visible to the LLM

**Evidence for (from upstream findings):**
- **M-007** confirms `$TRANSCRIPT_PATH` is available in ALL hook events and contains usage objects per turn
- **M-009/M-010/M-012** confirm the `UserPromptSubmit` -> `additionalContext` injection pathway is proven and operational (Jerry's L2 reinforcement already uses it)
- The existing `user-prompt-submit.py` hook demonstrates the pattern: read data, compute result, inject via `additionalContext`
- The ECW `statusline.py` already implements `_estimate_tokens()` using the chars/4 heuristic (line 374-380), proving the approach is viable for rough estimation
- Phase 2 used the bytes/4 heuristic to produce fill projections that aligned with expected compaction trigger points (106.1% at Step 9, 118.2% at Step 17)

**Evidence against (from upstream findings):**
- **GAP-006** explicitly flags that transcript-based estimation is approximate: summing `input_tokens` across turns does not account for compaction reducing effective context, context editing clearing content, or prompt caching behavior
- The transcript records what was *sent*, not what is *currently in* the context window after compaction -- after a compaction event, the heuristic would over-estimate fill unless it detects and adjusts for compaction
- **M-013** confirms no post-compaction notification exists, so the heuristic script would need independent compaction detection (which is where Method B complements)
- Accuracy degrades over long sessions with multiple compactions

**Implementation approach:**
- Extend the existing `user-prompt-submit.py` or add a second `UserPromptSubmit` hook
- Parse last entry in `$TRANSCRIPT_PATH` for `usage.input_tokens` as primary signal
- Fall back to cumulative sum with chars/4 estimation if usage data is unavailable
- Inject result as `<context-monitor>` tag in `additionalContext`

**Score justifications:**

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Reliability | 3 | Approximate by nature (GAP-006). The most recent turn's `input_tokens` is a reasonable proxy but not exact. Degrades after compaction events unless compensated. Phase 2 analysis showed the heuristic aligned with predicted compaction points, suggesting it is "good enough" for threshold detection even if not exact. |
| Overhead | 5 | Zero API calls. File I/O only (reading JSONL). The `$TRANSCRIPT_PATH` file is local. ECW already parses it for tool tracking. Estimated <50ms per invocation based on ECW's 5-second cache TTL being considered acceptable. |
| Implementation Complexity | 4 | The injection pathway is proven (M-010). Transcript parsing is straightforward JSONL. The main complexity is handling the compaction edge case (adjusting estimates after compaction). A working prototype could be built in <2 hours. |
| Granularity | 3 | Provides estimated token count and fill percentage (not binary). However, the estimate has a 10-20% error margin (Phase 2 methodology limitations). Cannot distinguish between fresh tokens, cached tokens, and compacted tokens. |
| Proactiveness | 5 | Fires on every user prompt via `UserPromptSubmit`. Provides continuous monitoring with configurable warning (70%) and critical (85%) thresholds. The LLM receives the signal BEFORE it begins processing the next turn, giving maximum lead time. |
| Compaction Awareness | 2 | Does NOT inherently handle compaction. After compaction, the cumulative sum approach over-estimates fill. The most recent turn's `input_tokens` approach may be more resilient IF the transcript records post-compaction token counts (see OQ-3 -- this is unverified), but requires the transcript to contain a post-compaction entry. Needs Method B to compensate. |

---

### Method B: Claude Code Context Compaction Detection

**How it works:**
1. The `PreCompact` hook fires when Claude Code is about to compact the conversation
2. A command hook on `PreCompact` writes a checkpoint file (e.g., `.jerry/compaction-checkpoint.json`) containing timestamp, estimated pre-compaction fill, and current orchestration state
3. A `UserPromptSubmit` hook checks for the existence of the checkpoint file on every prompt
4. If a checkpoint file exists and is recent (created since last prompt), it injects a "compaction occurred" notification into `additionalContext`, informing the LLM that context was compacted and it should re-orient
5. The checkpoint file is then marked as "acknowledged" to prevent repeated notifications

**Evidence for (from upstream findings):**
- **M-006** confirms `PreCompact` is a real hook event that fires before compaction with `trigger` (manual/auto) and `custom_instructions` in its input
- PreCompact is the ONLY deterministic signal that compaction is about to occur -- all other methods are heuristic
- **GAP-004** (no post-compaction LLM notification) is directly addressed by this file-based notification relay: PreCompact writes checkpoint -> UserPromptSubmit reads checkpoint -> LLM receives notification
- Phase 2 identified two predicted compaction events in the FEAT-015 workflow (Steps 9 and 17), confirming that compaction WILL occur in real orchestration runs

**Evidence against (from upstream findings):**
- **M-006** also notes that PreCompact has "no decision control and no ability to inject context -- it can only run side-effect scripts"
- The signal is REACTIVE, not proactive: it fires when compaction is already imminent, leaving zero time for graceful checkpoint if one hasn't already been created
- The file-based relay introduces a timing dependency: the `UserPromptSubmit` hook must fire AFTER the compaction completes and BEFORE the LLM processes the next turn -- this should be guaranteed by hook ordering, but needs verification
- There is no mechanism to know how much context was lost during compaction (the summary content is opaque to the hook)

**Implementation approach:**
- Add a `PreCompact` hook entry to `hooks.json`
- The hook script writes a JSON checkpoint file with `{timestamp, trigger, pre_compaction_estimate}`
- Extend the `UserPromptSubmit` hook to check for recent checkpoint files
- If found, inject `<compaction-alert>` tag with re-orientation instructions
- Optionally: the `PreCompact` hook could also write a quick state snapshot (current phase, gate, iteration) to aid re-orientation

**Score justifications:**

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Reliability | 5 | Deterministic signal. If compaction occurs, PreCompact fires. There is no estimation or heuristic involved. The only failure mode is if Claude Code changes the hook event contract. |
| Overhead | 5 | File write on PreCompact (rare event, ~2x per FEAT-015 workflow). File existence check on UserPromptSubmit (stat() call, negligible). Zero API calls, zero token cost. |
| Implementation Complexity | 3 | Requires two coordinated hooks (PreCompact writer + UserPromptSubmit reader). The file-based relay pattern is simple but introduces state management (checkpoint file lifecycle, acknowledgment, cleanup). Interaction with existing UserPromptSubmit hook requires coordination. Estimated 4-6 hours. |
| Granularity | 1 | Binary signal only: "compaction happened" or "compaction did not happen." Does not provide fill percentage, token count, or any quantitative measure of current context state. Does not indicate how much context was lost. |
| Proactiveness | 1 | Fires AFTER the decision to compact has already been made. Provides zero lead time for proactive action. By the time the LLM receives the notification (next UserPromptSubmit), compaction has already occurred and context has already been lost. |
| Compaction Awareness | 5 | This IS the compaction awareness mechanism. It is the only method that directly detects compaction events. It provides the foundation for all post-compaction recovery behavior. |

---

### Method C: Hook-Based Monitoring (ECW Status Line Pattern)

**How it works:**
1. A `UserPromptSubmit` command hook reads the `context_window.current_usage` data that Claude Code provides to the status line script
2. This data includes exact token counts: `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, and `context_window_size`
3. The hook computes fill percentage from actual data and injects it via `additionalContext`
4. The ECW `extract_context_info()` function (statusline.py lines 403-423) already implements this exact computation

**Evidence for (from upstream findings):**
- **M-017** confirms the ECW status line reads `context_window.current_usage` from Claude Code's JSON feed with detailed token breakdowns
- The status line's `extract_context_info()` function returns `(percentage, used_tokens, context_window_size, is_estimated)` -- exactly the data needed for context detection
- The status line's `extract_compaction_info()` function (lines 463-506) already implements compaction detection via token-count delta tracking
- This is the MOST accurate data source available: it reflects actual context window state, not a heuristic estimate
- If accessible, this single data source eliminates both GAP-001 (no model-accessible fill signal) and GAP-006 (approximation problems)

**Evidence against (from upstream findings):**
- **GAP-003** is the critical blocker: "Hook input JSON does not include `context_window` data." The status line receives data via stdin from Claude Code's status line protocol. Hooks receive data via a DIFFERENT input protocol (JSON with `session_id`, `transcript_path`, `cwd`, and event-specific fields)
- **M-017** explicitly notes: "It is unclear whether the status line JSON data is the same data available to hooks, or whether hooks receive a different (more limited) input schema"
- The status line is a separate process invoked by Claude Code through the `statusLine` configuration, NOT through the hook system. There is no documented mechanism to share data between the status line process and hook processes
- Phase 1 classified this as a "critical gap that needs verification"

**Implementation approach (IF feasible):**
- Option 1: Investigate whether hooks can access status line data through a shared mechanism (file, environment variable, or IPC)
- Option 2: Have the status line script write its computed data to a shared state file (e.g., `~/.claude/ecw-context-state.json`) on every invocation, and have the UserPromptSubmit hook read that file
- Option 3: Investigate whether the hook input schema could be extended (upstream feature request to Claude Code)
- The "status line writes, hook reads" pattern (Option 2) is the most pragmatic path and does not require upstream changes
- Risk: The hook may read the state file before the status line updates it for the current turn, resulting in data staleness of one turn. This is acceptable for threshold-based detection (one-turn delay has negligible impact on fill percentage).

**Score justifications:**

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Reliability | 4 (conditional) | IF the data is accessible: highly reliable, as it uses Claude Code's own token counting. The "4" rather than "5" is because the status line data could theoretically be stale (cached from a previous invocation) or the write-read pattern could have race conditions. IF the data is NOT accessible: 0 (method is not implementable). |
| Overhead | 4 | File read on every prompt (reading status line state file). The status line itself runs independently and has no additional cost. The hook's file read is O(1) -- the state file is small JSON. Slightly lower than Method A because it depends on another process having written the file recently. |
| Implementation Complexity | 2 | Requires modifying the status line script to write state to a file (straightforward). Requires the UserPromptSubmit hook to read that file (straightforward). BUT: the fundamental feasibility question (GAP-003) is unresolved. If Option 2 works, complexity drops to 3-4. If it requires upstream Claude Code changes (Option 3), complexity is 1 (external dependency). |
| Granularity | 5 | Provides exact token counts (fresh, cached, total), context window size, fill percentage, and compaction detection. This is the richest data source available. The status line already breaks down tokens into fresh vs. cached and detects compaction via delta tracking. |
| Proactiveness | 5 | Same as Method A -- fires on every UserPromptSubmit, providing continuous monitoring. The status line updates on every Claude Code turn, so data is near-real-time. |
| Compaction Awareness | 4 | The status line already implements compaction detection via token-count delta tracking (lines 463-506). The state file approach preserves this capability. Score is 4 not 5 because the compaction detection is heuristic (token drop > threshold) rather than event-driven like Method B's PreCompact hook. |

---

### Method D: Response Quality Degradation Signals

**How it works:**
1. A `UserPromptSubmit` prompt hook or a `PostToolUse` command hook monitors response characteristics
2. Metrics tracked: response length trends, tool call failure rates, repetitive output patterns, rule violation frequency
3. When quality metrics drop below a threshold, inject a "quality degradation detected -- possible context exhaustion" warning
4. Alternatively, a `Stop` prompt hook reviews the transcript for degradation patterns before allowing session termination

**Evidence for (from upstream findings):**
- Phase 2 analysis confirms that context exhaustion causes measurable quality degradation: "L1 rules (CLAUDE.md, rule files) are loaded once at session start and degrade as context fills" (M-015)
- **ADR-EPIC002-002** documents that L1 enforcement effectiveness drops to 40-60% at 50K+ context fill, providing a research-backed correlation between fill level and quality
- PROJ-001 FEAT-024 showed quality gate scores declining (QG-1 max retries at 0.9155), demonstrating that quality metrics are already tracked and threshold-based escalation works for score-based triggers
- The Jerry framework already has S-014 (LLM-as-Judge) scoring infrastructure that could theoretically be repurposed for per-turn quality monitoring

**Evidence against (from upstream findings):**
- **This is a lagging indicator.** By the time quality degrades measurably, context rot has already damaged output. Phase 1 found "no mechanism to detect *when* L1 degradation is occurring or how severe it is" -- this method attempts to infer cause from effect, which is inherently unreliable
- Phase 2 shows that quality gate iterations cost 29,000-45,000 tokens each. Running a quality check on every turn would be catastrophically expensive -- it would ACCELERATE context exhaustion rather than detecting it
- Quality degradation has many causes beyond context exhaustion: ambiguous requirements, complex tasks, tool errors. The false positive rate would be high
- Prompt hooks (type: "prompt") send the prompt to the LLM, consuming additional context tokens per check (M-008 notes "prompt hooks consume additional tokens and add latency")
- The quality degradation signal is not specific: it cannot distinguish between "the model is struggling with a hard problem" and "the model is suffering context rot"

**Implementation approach (theoretical):**
- Track trailing average response length (sudden drops may indicate truncation)
- Monitor tool call success rate (context rot leads to malformed tool calls)
- Check for L2 reinject marker compliance (if the model stops following reinforced rules, context rot is likely)
- Use a lightweight heuristic rather than full S-014 scoring per turn

**Score justifications:**

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Reliability | 1 | Extremely unreliable as a context exhaustion detector. Quality degradation is a non-specific symptom with many possible causes. Phase 2 data shows quality gate scores vary significantly even within healthy context (QG-2 scored 0.960 then 0.951 -- a decline that is normal, not degradation). No empirical calibration exists for mapping quality metrics to context fill levels. |
| Overhead | 1 | If using prompt hooks or LLM-as-Judge: extremely expensive (each check costs thousands of tokens). If using heuristic metrics only: moderate (2-3, file I/O + computation). The full S-014 scoring approach would add ~6,000 tokens per check, which at every prompt would add ~60,000+ tokens per session (30% of context window consumed by the monitoring itself). |
| Implementation Complexity | 1 | Requires defining "quality degradation" quantitatively, which is an unsolved research problem in this context. What response length is "too short"? What failure rate is "abnormal"? These thresholds would need extensive calibration against real degradation data that does not exist. The monitoring system itself would be more complex than the context detection problem it aims to solve. |
| Granularity | 2 | At best, provides a quality score trend (some granularity). Cannot provide token counts, fill percentage, or compaction state. The signal is ordinal (better/worse) rather than quantitative (N tokens used). |
| Proactiveness | 1 | By definition, a lagging indicator. Quality must FIRST degrade before the signal fires. Phase 1 analysis of M-015 confirms that L1 enforcement degrades gradually -- there is no sharp transition point that would provide a clean detection threshold. The damage is already done by the time this method detects it. |
| Compaction Awareness | 1 | No compaction awareness whatsoever. Cannot detect compaction events. Cannot distinguish between pre-compaction degradation and post-compaction context loss. If compaction occurs and quality improves (because the summary is cleaner than the full context), this method would paradoxically signal "all clear" after a compaction event that lost critical state. |

---

## Scoring Matrix

**Scoring Scale:** 1 = Does not meet need, 2 = Partially meets need, 3 = Adequately meets need, 4 = Well meets need, 5 = Fully meets need.

| Dimension | Weight | Method A (Transcript) | Method B (PreCompact) | Method C (ECW) | Method D (Quality) |
|-----------|--------|:-----:|:-----:|:-----:|:-----:|
| Reliability | 0.25 | 3 | 5 | 4* | 1 |
| Overhead | 0.15 | 5 | 5 | 4 | 1 |
| Implementation Complexity | 0.15 | 4 | 3 | 2 | 1 |
| Granularity | 0.15 | 3 | 1 | 5 | 2 |
| Proactiveness | 0.20 | 5 | 1 | 5 | 1 |
| Compaction Awareness | 0.10 | 2 | 5 | 4 | 1 |

*Method C scores are conditional on GAP-003 resolution. If infeasible, effective scores drop to 0 across all dimensions.

### Weight Justification

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Reliability | 0.25 | The highest weight because an unreliable detection system is worse than no detection -- false negatives cause silent degradation, false positives cause unnecessary session churn. |
| Proactiveness | 0.20 | Second highest because the Phase 2 analysis shows compaction events happen suddenly (0% to compaction in a single QG iteration adding ~35K tokens). Early warning is essential for the orchestrator to checkpoint before compaction. |
| Overhead | 0.15 | Important because the detection mechanism itself consumes context tokens. Phase 2 showed that the 200K window is already insufficient for C2+ workflows -- any monitoring overhead must be minimal. |
| Implementation Complexity | 0.15 | Important for SPIKE-001 timeboxing. A solution that takes weeks to build is less valuable than one that can be prototyped in hours, especially given the unresolved feasibility questions. |
| Granularity | 0.15 | The orchestrator needs quantitative data (fill percentage) to make graduated decisions (warn vs. checkpoint vs. escalate). Binary signals are insufficient for the two-tier threshold model proposed in the SPIKE-001 hypothesis. |
| Compaction Awareness | 0.10 | Lowest weight because compaction awareness can be layered on top of any primary detection method (via Method B). It is important but not the primary detection concern. |

### Sensitivity Analysis

To test the robustness of the weighting scheme, an alternative weighting was evaluated: swapping Reliability (0.25) with Proactiveness (0.20), and increasing Granularity to 0.20 while decreasing Reliability to 0.20. Under this alternative scheme (Reliability 0.20, Proactiveness 0.25, Granularity 0.20, others unchanged), the composite scores become: Method A = 4.00, Method B = 3.15, Method C = 4.35*, Method D = 1.25. The ranking remains identical: C > A > B > D. The A+B hybrid recommendation holds because Method A retains the highest unconditional score and Method B remains uniquely necessary for compaction awareness regardless of weight assignment. This demonstrates that the recommendation is robust to moderate weight perturbations -- the ranking is primarily driven by the large score differentials between methods (e.g., Method A vs. D) rather than small weight adjustments.

---

## Weighted Composite Scores

| Method | Reliability (0.25) | Overhead (0.15) | Complexity (0.15) | Granularity (0.15) | Proactiveness (0.20) | Compaction (0.10) | **Composite** |
|--------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **A: Transcript** | 0.75 | 0.75 | 0.60 | 0.45 | 1.00 | 0.20 | **3.75** |
| **B: PreCompact** | 1.25 | 0.75 | 0.45 | 0.15 | 0.20 | 0.50 | **3.30** |
| **C: ECW** | 1.00 | 0.60 | 0.30 | 0.75 | 1.00 | 0.40 | **4.05*** |
| **D: Quality** | 0.25 | 0.15 | 0.15 | 0.30 | 0.20 | 0.10 | **1.15** |

Note: Composite scores are on a 0-5 scale (raw score x weight). Rankings are scale-independent.

**Ranking:**
1. **Method C: ECW Status Line (4.05)** -- highest composite, but conditional on feasibility
2. **Method A: Transcript Heuristic (3.75)** -- highest unconditional score, implementable today
3. **Method B: PreCompact Hook (3.30)** -- essential complement for compaction awareness
4. **Method D: Quality Degradation (1.15)** -- rejected as primary or secondary mechanism

**Recommendation:** Implement **A+B hybrid** as the baseline detection system, with **Method C as a Phase 4 stretch investigation**. If Method C proves feasible, it replaces Method A as the proactive layer while Method B remains unchanged as the compaction awareness layer.

---

## Recommended Architecture

### Hybrid A+B Detection System (Baseline)

```
                    +-----------------------+
                    |   Claude Code Session  |
                    +-----------+-----------+
                                |
              +-----------------+-----------------+
              |                                   |
    [Every User Prompt]                  [Compaction Imminent]
              |                                   |
    +---------v----------+              +---------v----------+
    | UserPromptSubmit   |              | PreCompact Hook    |
    | Hook (Method A)    |              | (Method B)         |
    |                    |              |                    |
    | 1. Parse transcript|              | 1. Write checkpoint|
    |    $TRANSCRIPT_PATH|              |    file with:      |
    | 2. Extract latest  |              |    - timestamp     |
    |    input_tokens    |              |    - trigger type  |
    | 3. Compute fill %  |              |    - est. fill %   |
    | 4. Check for       |              |    - orch. state   |
    |    compaction       |              +--------------------+
    |    checkpoint file  |
    | 5. Inject as       |
    |    additionalContext|
    +--------+-----------+
             |
             v
    +--------+-----------+
    | additionalContext   |
    | Injection           |
    |                     |
    | <context-monitor>   |
    |   fill: 73.2%       |
    |   tokens: 146,400   |
    |   window: 200,000   |
    |   level: WARNING    |
    |   compacted: false   |
    | </context-monitor>  |
    +---------------------+
```

### Detection Thresholds (Provisional -- Pending Phase 6 Calibration)

Based on Phase 2 empirical data (cumulative fill projection):

| Level | Fill % | Rationale | Recommended LLM Action |
|-------|--------|-----------|------------------------|
| LOW | 0-60% | Phase 1 of FEAT-015 reached 63.6% after 1 agent + 3 QG iterations. Below this, no action needed. | None. Continue normally. |
| WARNING | 60-80% | Phase 2 entered WARNING at Step 5 (66.1%). This provides ~34K-40K tokens of headroom -- enough for 1 QG iteration but not 2. | Consider planning checkpoint. Prioritize essential operations. Consider deferring non-critical QG strategies. |
| CRITICAL | 80-90% | Phase 2 QG-2 iter 1 hit 88.6% at Step 8. At this level, a single QG iteration will trigger compaction. | Recommend checkpoint immediately. Write resumption context. Prepare for session handoff. |
| COMPACTION | 90%+ | Compaction is imminent or already triggered. PreCompact hook fires. | Recommend saving all state to files. Avoid starting new operations. Signal session boundary. |

**Threshold calibration note:** These thresholds are derived from PROJ-001 FEAT-015 data (Phase 2 analysis). The WARNING threshold of 60% is lower than the SPIKE-001 hypothesis of 70% because Phase 2 showed that a single QG gate (3 iterations) can consume 87K tokens (43.5% of window). A 70% warning leaves only 60K tokens -- potentially insufficient for a full QG gate. The 60% threshold provides ~80K tokens of headroom, enough for 2 QG iterations with margin.

### Injection Format

The `UserPromptSubmit` hook will inject a structured `<context-monitor>` tag:

```xml
<context-monitor>
CONTEXT STATUS: WARNING (73.2% filled)
Tokens used: 146,400 / 200,000
Estimated remaining: 53,600 tokens (~1.8 QG iterations)
Compaction events: 0
Last checkpoint: none

ACTION REQUIRED at CRITICAL (>80%):
- Save orchestration state to ORCHESTRATION.yaml resumption section
- Write accumulated defect summary to checkpoint file
- Record cross-phase decisions
- Prepare session handoff context
</context-monitor>
```

The remaining-tokens-to-QG-iterations conversion uses the Phase 2 empirical average of ~29,000 tokens per QG iteration.

### Hook Integration Plan

The detection system integrates with the existing hook infrastructure:

| Hook | Current Function | Added Function |
|------|-----------------|----------------|
| `UserPromptSubmit` | L2 quality reinforcement | Context fill monitoring + compaction alert relay |
| `PreCompact` | (not configured) | Checkpoint file creation |
| `Stop` | (not configured) | (future: block stop if checkpoint not saved at CRITICAL) |

**Implementation priority:**
1. Add context monitoring to `UserPromptSubmit` hook (Method A) -- can share the script or run as a second hook entry
2. Add `PreCompact` hook for checkpoint file creation (Method B)
3. Design the `<context-monitor>` injection format
4. Add threshold-to-action mapping in orchestrator instructions

### Method C Upgrade Path

If Phase 4 prototyping confirms that the ECW status line can share context data with hooks (via Option 2: status line writes state file, hook reads it):

1. Modify `statusline.py` to write `~/.claude/ecw-context-state.json` on every invocation
2. Modify the `UserPromptSubmit` hook to read this file instead of parsing the transcript
3. The injection format (`<context-monitor>` tag) remains identical
4. Method A transcript parsing becomes a fallback for cases where the state file is stale or missing

This upgrade is a drop-in replacement because the architecture separates data acquisition (Method A or C) from data injection (always via `UserPromptSubmit` `additionalContext`).

---

## Risk Assessment

### R-1: Transcript Heuristic Accuracy Drift (Method A)

**Risk:** The transcript-based token estimate diverges from actual context fill over time, especially after compaction events, leading to false confidence or unnecessary alarms.

**Likelihood:** HIGH (Phase 2 methodology section acknowledges 10-20% error margin; compaction events are predicted to occur in most C2+ workflows).

**Impact:** MEDIUM. False high estimates cause premature checkpointing (wasted work, unnecessary session boundaries). False low estimates cause missed detection (the problem we are trying to solve).

**Mitigation:** Use the most recent turn's `input_tokens` from transcript usage data rather than cumulative sums. This value reflects what the API actually processed, which is closer to actual context fill. Method B provides a hard backstop -- if the heuristic misses, PreCompact still fires.

### R-2: PreCompact Hook Timing (Method B)

**Risk:** The `PreCompact` hook fires but the checkpoint file is not written before compaction completes, or the `UserPromptSubmit` hook fires before the checkpoint file is flushed to disk.

**Likelihood:** LOW. File writes are synchronous in Python, and Claude Code likely sequences hook execution before proceeding with compaction. However, this ordering is not documented.

**Impact:** HIGH if it occurs. The LLM would not receive the compaction notification, losing the only deterministic compaction signal.

**Mitigation:** Verify hook execution ordering in Phase 4 prototyping. Use `fsync()` in the PreCompact hook script. Add a redundant compaction detection heuristic in Method A (detect sudden drop in `input_tokens` between consecutive transcript entries, similar to ECW's delta tracking).

### R-3: Hook Budget Overflow

**Risk:** Adding context monitoring data to every prompt consumes additional context tokens, accelerating the very exhaustion it is detecting.

**Likelihood:** MEDIUM. The `<context-monitor>` injection is estimated at ~100-150 tokens per prompt. Over a 50-prompt session, that is ~5,000-7,500 tokens (2.5-3.75% of window).

**Impact:** LOW. The monitoring overhead is small relative to the primary cost drivers (QG iterations at 29K-45K tokens each). The L2 reinforcement system already injects ~600 tokens per prompt with acceptable overhead.

**Mitigation:** Keep the injection format concise. Only inject the full action guidance at WARNING level and above. At LOW level, inject a minimal 2-line status. Budget target: <100 tokens for LOW, <200 tokens for WARNING+.

### R-4: Method C Feasibility Failure

**Risk:** GAP-003 cannot be resolved -- hooks cannot access status line data, and the write-file workaround does not work (status line invocation timing does not align with hook invocation timing).

**Likelihood:** MEDIUM. The status line and hooks are separate subsystems in Claude Code. Their invocation timing and data access patterns may be fundamentally incompatible.

**Impact:** LOW (for the overall system). Method A+B hybrid is fully functional without Method C. The impact is limited to losing the accuracy upgrade path.

**Mitigation:** Design the architecture so Method C is an optional enhancement, not a dependency. Phase 4 should timebox the Method C investigation to 2 hours. If infeasible, close it and proceed with A+B.

### R-5: Threshold Miscalibration

**Risk:** The proposed thresholds (60/80/90%) are derived from a single workflow (PROJ-001 FEAT-015) and may not generalize to other orchestration patterns.

**Likelihood:** MEDIUM. Phase 2 extrapolation table shows different workflow profiles (C1 minimal, C3 EPIC-003 style, C4 tournament) have very different fill characteristics.

**Impact:** MEDIUM. If thresholds are too aggressive, sessions are interrupted unnecessarily. If too conservative, detection fires too late.

**Mitigation:** Make thresholds configurable (not hardcoded). Store in `.claude/ecw-statusline-config.json` or a dedicated context monitor config file. Collect empirical data from PROJ-004 implementation work to calibrate. Provide per-criticality threshold overrides (C1 workflows can tolerate higher fill than C3+).

---

## Open Questions

### For Phase 4 (Prototyping)

| ID | Question | Why It Matters | Suggested Investigation |
|----|----------|----------------|------------------------|
| OQ-1 | Can the ECW status line share context data with hooks via a shared state file? | Determines whether Method C is feasible as a drop-in upgrade for Method A. | Modify `statusline.py` to write state file. Add file read to UserPromptSubmit hook. Test whether the status line runs before or after hooks on each turn. |
| OQ-2 | What is the actual hook execution order for `PreCompact` relative to `UserPromptSubmit`? | Determines whether the file-based relay pattern for compaction notification is reliable. | Add logging to both hooks and trigger a compaction event. Verify that PreCompact completes before the next UserPromptSubmit fires. |
| OQ-3 | What does the transcript look like after compaction? Does the usage data reflect pre- or post-compaction token counts? | Determines whether Method A's transcript parsing can self-correct after compaction. | Parse a transcript from a session that experienced compaction. Check whether `input_tokens` in the first post-compaction entry reflects the compacted context size. |
| OQ-4 | What is the actual compaction reset size? Phase 2 assumed ~50K tokens (25% of window). | Calibrates the post-compaction fill estimates and remaining headroom calculations. | Trigger compaction in a controlled session and measure the post-compaction `input_tokens` value. |
| OQ-9 | Does `input_tokens` in the usage response accurately approximate total context window occupancy? | Method A's reliability depends on this assumption. If `input_tokens` diverges significantly from actual fill, threshold calibration is invalid. | Compare `input_tokens` values against Method C actual context fill data (if available) to quantify divergence. Empirical validation needed. |

### For Phase 5 (Resumption Protocol)

| ID | Question | Why It Matters |
|----|----------|----------------|
| OQ-5 | What minimum state must be preserved in the checkpoint file for reliable re-orientation? | Phase 2 identified 6 resumption gaps (RG-1 through RG-6). The checkpoint file content determines how many gaps are addressed. |
| OQ-6 | How should the orchestrator behave when it receives a `<context-monitor>` CRITICAL signal mid-QG-iteration? | The orchestrator must decide: complete the current iteration (adding ~29K tokens) or abort and checkpoint. This is a policy decision, not a detection question. |

### For Phase 6 (Threshold Calibration)

| ID | Question | Why It Matters |
|----|----------|----------------|
| OQ-7 | What is the actual L1 enforcement effectiveness curve for Claude Opus 4.6 at various fill levels? | ADR-EPIC002-002 cites 40-60% effectiveness at 50K+ context, but this may be stale data. Fresh calibration against the current model would improve threshold accuracy. |
| OQ-8 | Should thresholds be static (fixed percentages) or dynamic (adjusted based on remaining work estimate)? | A dynamic threshold that considers "tokens needed for remaining phases" would be more adaptive but significantly more complex. |

---

## Self-Review Checklist

- [x] All 4 methods evaluated with evidence-based scoring
- [x] Scoring justifications reference Phase 1/2 findings (M-001 through M-017, GAP-001 through GAP-006, RP-1 through RP-5, RG-1 through RG-6) -- not speculation
- [x] Recommended approach is concrete enough for Phase 4-6 to build on (architecture diagram, injection format, hook integration plan, threshold table)
- [x] Risk assessment is honest about unknowns (5 risks with likelihood/impact/mitigation, all conditional on unverified assumptions disclosed per P-022)
- [x] Open questions will unblock downstream phases (8 questions mapped to Phases 4/5/6)
- [x] L0/L1/L2 structure present (L0 Summary, L1 Method Profiles, L2 Scoring Matrix + Architecture)
- [x] H-23/H-24 navigation table with anchor links present

---

## References

| # | Source | Path / URL | Content Used |
|---|--------|------------|--------------|
| 1 | Phase 1: Mechanism Inventory | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-1-inventory/research-inventory/mechanism-inventory.md` | M-001 through M-017, GAP-001 through GAP-006, capability matrix |
| 2 | Phase 2: Run Analysis | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-2-analysis/run-analyzer/run-analysis.md` | Cumulative fill projection (17 steps), token budget estimates, risk points RP-1 through RP-5, resumption gaps RG-1 through RG-6, recommendations |
| 3 | ECW Status Line v2.1.0 | `.claude/statusline.py` | `extract_context_info()` (lines 403-423), `extract_compaction_info()` (lines 463-506), `_estimate_tokens()` (lines 374-380), configuration defaults |
| 4 | UserPromptSubmit Hook | `hooks/user-prompt-submit.py` | Injection pattern, `additionalContext` format, fail-open design |
| 5 | Hook Configuration | `hooks/hooks.json` | Current hook entries, event types, timeout values |
| 6 | Hook Output Schema | `schemas/hooks/user-prompt-submit-output.schema.json` | `additionalContext` field specification |
| 7 | Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` | AE-006, L2 reinject budget (~600 tokens/prompt), enforcement architecture context rot assessment |
| 8 | SPIKE-001 Definition | `projects/PROJ-004-context-resilience/work/EPIC-001-context-resilience/FEAT-001-context-detection/SPIKE-001-context-research.md` | Research question, hypothesis (70%/85% thresholds), scope |
| 9 | ADR-EPIC002-002 | Referenced via Phase 1/2 findings | Context rot research (40-60% effectiveness at 50K+), 5-layer enforcement architecture |
| 10 | Anthropic Compaction Docs | https://platform.claude.com/docs/en/build-with-claude/compaction | Server-side compaction behavior, `pause_after_compaction`, usage iterations |
| 11 | Claude Code Hooks Docs | https://code.claude.com/docs/en/hooks | Hook event types, PreCompact, input/output schemas |

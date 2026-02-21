# Context Monitoring Calibration Protocol

<!-- VERSION: 1.0.0 | DATE: 2026-02-20 | SOURCE: PROJ-004 ST-003 Validation -->
<!-- PRODUCED BY: ps-validator v2.0.0 (feat001-impl-20260220-001/st-003-exec) -->

> Living document for recalibrating context exhaustion detection thresholds.
> Current defaults are empirically calibrated from PROJ-001 FEAT-015 data via SPIKE-001.
> Update this document when measured costs from new workflows diverge from calibration baselines.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Current Threshold Defaults](#current-threshold-defaults) | Implemented defaults and their empirical basis |
| [Recalibration Triggers](#recalibration-triggers) | When to initiate a recalibration cycle |
| [Data Collection Method](#data-collection-method) | What to measure and how |
| [Result Interpretation](#result-interpretation) | How to translate measured data into threshold changes |
| [Recalibration Process](#recalibration-process) | Step-by-step protocol |
| [Calibration History](#calibration-history) | Record of all calibrations performed |
| [References](#references) | Source documents and detailed cost catalogs |

---

## Current Threshold Defaults

### Default Thresholds (C2 Standard Criticality)

These are the calibrated defaults implemented in `ConfigThresholdAdapter`:

| Tier | Fill % | Tokens Used (200K) | Tokens Remaining | Action |
|------|--------|-------------------|-----------------|--------|
| NOMINAL | 0 - 55% | 0 - 110,000 | 90,000 - 200,000 | No injection. Normal operations. |
| LOW | 55 - 70% | 110,000 - 140,000 | 60,000 - 90,000 | Advisory `<context-monitor>` (~15-20 tokens). No action required. |
| WARNING | 70 - 80% | 140,000 - 160,000 | 40,000 - 60,000 | Full `<context-monitor>` (~100-150 tokens). Orchestrator SHOULD update resumption section. |
| CRITICAL | 80 - 88% | 160,000 - 176,000 | 24,000 - 40,000 | Full `<context-monitor>` + auto-checkpoint (AE-006c). Orchestrator MUST complete current op then checkpoint. |
| EMERGENCY | 88 - 95% | 176,000 - 190,000 | 10,000 - 24,000 | Full `<context-monitor>` + auto-checkpoint + `<context-emergency>` (AE-006d). Orchestrator MUST NOT start new operations. |

### Configuration Keys

Override any threshold via layered config:

```toml
# In project config TOML or root jerry.toml
[context_monitor]
nominal_threshold = 0.55
warning_threshold = 0.70
critical_threshold = 0.80
emergency_threshold = 0.88
enabled = true
```

Or via environment variable (highest precedence):
```bash
export JERRY_CONTEXT_MONITOR__WARNING_THRESHOLD=0.65
export JERRY_CONTEXT_MONITOR__CRITICAL_THRESHOLD=0.78
```

### Empirical Basis for Default Thresholds

The C2 defaults are calibrated from PROJ-001 FEAT-015 (license header replacement) via SPIKE-001 Phase 6 analysis. Key derivation logic:

| Threshold | Derivation |
|-----------|-----------|
| **NOMINAL = 55%** | At 55% (90K remaining), 3 worst-case QG iterations (87K tokens) fit with margin. Below this point, context-monitor injection adds unnecessary overhead. |
| **WARNING = 70%** | At 70% (60K remaining), exactly 2 typical QG iterations fit (2 x 29K = 58K). One more operation can push to CRITICAL. This is the proactive action window. |
| **CRITICAL = 80%** | At 80% (40K remaining), only 1 typical QG iteration fits. New QG gates must not start. Enough headroom for: complete current iteration (29K) + write resumption (~800) + handoff preparation (~2K) = ~32K, leaving 8K safety margin. |
| **EMERGENCY = 88%** | Directly from PROJ-001: Step 8 reached 88.6% when a QG iteration triggered compaction. At 88%, no standard QG iteration (29K+ tokens) can complete. The 12% safety margin to theoretical 100% accounts for 10-20% estimation error and cumulative drift. |

### Criticality-Adjusted Thresholds (PROVISIONAL)

The following thresholds are extrapolated from C2 data. They are PROVISIONAL and require validation against actual C1, C3, and C4 workflows before being treated as calibrated defaults.

| Tier | C1 Routine | C2 Standard | C3 Significant | C4 Critical |
|------|:----------:|:-----------:|:--------------:|:-----------:|
| NOMINAL | 0-70% | 0-55% | 0-45% | 0-35% |
| LOW | 70-80% | 55-70% | 45-60% | 35-50% |
| WARNING | 80-90% | 70-80% | 60-72% | 50-65% |
| CRITICAL | 90-95% | 80-88% | 72-82% | 65-78% |
| EMERGENCY | 95%+ | 88-95% | 82-90% | 78-88% |

**C1 rationale:** Routine workflows require HARD rules only, no mandatory QG strategy sets. Total consumption typically 60-80K tokens (30-40% of 200K window). WARNING at 80% still provides 40K tokens -- sufficient for any C1 operation.

**C3 rationale:** Significant workflows involve additional strategy sets (S-004, S-012, S-013) adding ~12-18K tokens per QG iteration above C2. Earlier warnings reflect higher per-iteration consumption. AE-006c (C3+ EMERGENCY = mandatory human escalation) requires more time for escalation communication.

**C4 rationale:** Critical workflows run all 10 strategies per QG iteration (~87K tokens/iteration = 43.5% of context). A single C4 QG iteration starting at 50% fill would reach 93.5% -- past EMERGENCY. WARNING at 50% gives the orchestrator exactly one iteration window before CRITICAL. CRITICAL at 65% (70K remaining) correctly signals that no C4 QG iteration (87K typical) can fit.

---

## Recalibration Triggers

A recalibration cycle SHOULD be initiated when any of the following conditions are met:

### T-1: QG Iteration Cost Divergence

**Trigger:** Measured QG iteration cost (actual fill% delta x 200K) differs by > 25% from the 29,000-token estimate.

| Direction | Implication |
|-----------|------------|
| Cost < 21,750 tokens (< 75% of estimate) | Thresholds are conservative. CRITICAL and EMERGENCY could be raised, providing more headroom for actual QG work. |
| Cost > 36,250 tokens (> 125% of estimate) | Thresholds are too aggressive. CRITICAL should be lowered so the signal fires before a QG iteration begins. |

**How to measure:** Record fill% at the start and end of each QG iteration (read from `<context-monitor>` tag values in the session transcript). Compute `(end_fill - start_fill) * 200,000`.

### T-2: Threshold Level Jump

**Trigger:** A single operation starts in one tier and ends two or more tiers higher (e.g., NOMINAL to CRITICAL in a single step).

This indicates insufficient granularity. The operation started below a threshold without triggering the intermediate tier's advisory actions. If this occurs, consider:
- Splitting the offending operation into smaller sub-operations.
- Lowering the lower threshold to catch the operation before it begins.

**How to measure:** Record tier at start and end of each agent dispatch or QG strategy execution. Flag any step where tier delta >= 2.

### T-3: Post-Compaction Reorientation Cost Divergence

**Trigger:** Post-compaction reorientation (checkpoint read + resumption read + deliverable reads) costs > 50% more or less than the Phase 5 estimate of 1,700-5,260 tokens.

This affects the EMERGENCY threshold's safety margin calculation. If reorientation costs more than expected, the EMERGENCY threshold should be lowered to preserve more headroom. If costs less, the threshold may be raised.

**How to measure:** After each compaction event, record the fill% after the first session-start prompt (post-resumption injection) minus the estimated fixed session overhead (~15.7%).

### T-4: Injection Overhead Budget Exceeded

**Trigger:** Total `<context-monitor>` injection tokens across a session exceed 5% of the context window (> 10,000 tokens for 200K window).

The SPIKE-001 estimate was ~2% (3,960 tokens) for a 50-prompt session. Exceeding 5% means the monitoring overhead is materially competing with workflow budget.

**How to measure:** Sum the token estimates for all `<context-monitor>` injections across a session: NOMINAL=0, LOW=15, WARNING=150, CRITICAL=175, EMERGENCY=225, COMPACTION=280.

### T-5: Model Context Window Change

**Trigger:** Claude's context window changes from 200K tokens to a different value (e.g., 500K or 1M).

Percentage-based thresholds remain valid in principle (they scale with window size) but become more conservative as windows grow. At 500K+, C1-C2 workflows may never reach WARNING under the default thresholds. See SPIKE-001 Sensitivity Analysis section for 500K and 1M analysis.

**Action:** Re-evaluate whether percentage-based thresholds are still appropriate or whether dynamic (remaining-capacity-based) thresholds should be implemented.

### T-6: New Criticality Level Data Available

**Trigger:** First monitored completion of a C1 or C4 workflow, providing empirical data for the PROVISIONAL criticality-adjusted thresholds.

**Action:** Update the PROVISIONAL thresholds with measured values and remove the PROVISIONAL label for the validated criticality level.

---

## Data Collection Method

### What to Collect

For each monitored session, collect:

| Data Point | Source | Format |
|-----------|--------|--------|
| Fill % at each prompt | `<context-monitor>` tag in session transcript | Float 0.0-1.0 |
| Tier at each prompt | `<context-monitor>` tag | NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY |
| Token count at each prompt | `<context-monitor>` tag | Integer |
| Operation type at each prompt | Prompt text or orchestration log | "qg_iteration", "agent_dispatch", "file_read", etc. |
| QG iteration start/end prompts | Orchestration log | Pair of fill% values |
| Compaction events | Session boundaries | Count, fill% at compaction |
| Post-compaction first fill% | First `<context-monitor>` after new session start | Float 0.0-1.0 |
| Threshold trigger timestamps | Session log | Tier, fill%, operation in progress |

### How to Collect

**Method A (Primary):** Read fill% values from `<context-monitor>` tags in `additionalContext` of each hook event. These are logged to `~/.claude/projects/{project}/logs/` as part of the session transcript.

**Method B (Secondary):** Read fill% deltas from the JSONL transcript directly using `JsonlTranscriptReader.read_latest_tokens()` at each step. Compute `token_count / 200,000`.

**Practical collection steps:**

1. After completing a monitored workflow, locate the JSONL transcript at `~/.claude/projects/{project}/{session_id}.jsonl`.
2. Parse all `additionalContext` fields containing `<context-monitor>` blocks.
3. Extract `fill-percentage`, `tier`, and `token-count` from each block.
4. Join with orchestration event log to identify which operation was in progress at each fill reading.
5. Record in a table matching the Operation Cost Catalog format (min/typical/max for each operation type).

### Collection Template

```markdown
## Session Calibration Data: {PROJ-ID} {WORKFLOW-TYPE}

| Step | Operation | Fill % Start | Fill % End | Delta Tokens | Tier Start | Tier End |
|------|-----------|:---:|:---:|:---:|:---:|:---:|
| 1 | Session start | 0.0% | 15.7% | 31,400 | NOMINAL | NOMINAL |
| 2 | Agent dispatch (simple) | 15.7% | 17.8% | 4,200 | NOMINAL | NOMINAL |
| ... | ... | ... | ... | ... | ... | ... |

## Threshold Trigger Events

| Tier | Fill % | Operation in Progress | Action Taken | Correct? |
|------|:---:|---|---|:---:|
| LOW | 57.2% | QG-1 iteration 2 start | Advisory injection | Yes |
| WARNING | 71.5% | QG-2 iteration 1 start | Resumption section updated | Yes |
| CRITICAL | 82.3% | QG-2 iteration 1 (S-014 complete) | Auto-checkpoint cx-001 created | Yes |

## Summary Measurements

- Session type: {C1/C2/C3/C4}
- Total prompts: {N}
- Compaction events: {N}
- Typical QG iteration cost: {N} tokens ({N}% of 200K)
- Post-compaction reset to: {N}% fill
- Total injection overhead: {N} tokens ({N}% of 200K)
```

---

## Result Interpretation

### Step 1: Compare to Cost Catalog

For each operation type measured, compare to the SPIKE-001 Operation Cost Catalog in threshold-proposal.md. Note divergences:

| Divergence Type | Interpretation |
|----------------|----------------|
| Measured typical QG iteration > 36,250 tokens | Workflow is more expensive than C2 baseline. Thresholds need to be lowered. |
| Measured typical QG iteration < 21,750 tokens | Workflow is cheaper than C2 baseline. Thresholds can be raised. |
| Post-compaction fill > 30% (>60K tokens) | Compaction is not resetting context as aggressively as assumed. EMERGENCY threshold margin may be smaller than modeled. |
| Post-compaction fill < 20% (<40K tokens) | Compaction resets more aggressively. EMERGENCY threshold margin is larger than needed. |
| Total injection overhead > 10,000 tokens | Monitoring is consuming too much budget. Consider raising NOMINAL threshold or switching to NOMINAL-only-suppress mode. |

### Step 2: Re-derive Affected Thresholds

Use the "tokens remaining must fit N operations" principle:

- **WARNING:** Set where `remaining_tokens >= 2 x typical_QG_cost`. If typical QG cost is now 35K (not 29K), WARNING should be at: `200K - (2 x 35K) = 130K remaining = 35% fill`. This is MUCH lower than 70%. Recalculate: `200K - 130K = 70K used = 35% fill`. Warning at 35%? That would generate too many low-tier alerts. Instead, apply the principle proportionally: WARNING should be at the fill level where at most 2 typical iterations can still fit. `(200K - 2*35K)/200K = 65%`. So WARNING moves from 70% to 65%.

- **CRITICAL:** Set where `remaining_tokens >= 1.5 x typical_QG_cost + checkpoint_cost`. For 35K typical cost: `1.5 x 35K + 2K = 54.5K remaining = 72.75% fill = CRITICAL at 72.75%` (rounded to 73%). Note: if CRITICAL is close to WARNING, consider merging the tiers.

- **EMERGENCY:** Set where `remaining_tokens < 1 x typical_QG_cost`. For 35K: `remaining < 35K = fill > 82.5%`. EMERGENCY at 83%.

### Step 3: Validate Against Historical Data

Before adopting new thresholds, apply them retrospectively to all available session data:
1. Would the new thresholds have triggered at appropriate moments?
2. Did the new thresholds avoid unnecessary alerts (false positives)?
3. Did the new thresholds catch all relevant transition points (no false negatives)?

### Step 4: Check Safety Margins

Each threshold must maintain a minimum safety margin:

| Threshold | Minimum Safety Margin |
|-----------|----------------------|
| WARNING to CRITICAL | >= 1 typical QG iteration (ensures WARNING fires before CRITICAL is entered by a QG iteration that started at WARNING) |
| CRITICAL to EMERGENCY | >= checkpoint_cost + handoff_preparation (ensures checkpoint can complete after CRITICAL trigger) |
| EMERGENCY to 100% | >= 1 checkpoint write + 2 prompts (ensures emergency checkpoint can always be written) |

If re-derived thresholds violate these margins, use the minimum margin rule to set the threshold instead.

---

## Recalibration Process

When a trigger condition is met:

1. **Collect data** using the Data Collection Method above. Record in a calibration data table.

2. **Identify divergence** by comparing to the Operation Cost Catalog in threshold-proposal.md. Note: which operation type diverges, in which direction, and by what magnitude.

3. **Re-derive affected thresholds** using the Result Interpretation steps above. Only change thresholds affected by the divergence -- do not recalibrate unaffected tiers.

4. **Validate against all available data** including PROJ-001 baseline, PROJ-004 SPIKE-001 session data, and the new workflow data. Ensure no regression (new thresholds should not cause missed detections in historical data).

5. **Update ConfigThresholdAdapter defaults** in `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py`. Update `_DEFAULT_THRESHOLDS` dict.

6. **Update threshold-proposal.md** (SPIKE-001 Phase 6) by appending a "Recalibration NNN" section with: trigger condition, measured values, before/after thresholds, validation results.

7. **Create an ADR** (auto-C3 minimum per AE-003): Document the threshold change, rationale, evidence, and validation. File in `projects/{PROJ-ID}/decisions/ADR-NNN-threshold-recalibration.md`.

8. **Update the Calibration History** table below with the recalibration record.

9. **Run the full test suite** to confirm no regressions: `uv run pytest tests/`.

---

## Calibration History

| Version | Date | Trigger | Workflow Used | C2 Thresholds (N/W/C/E) | Change |
|---------|------|---------|---------------|:----:|--------|
| 1.0.0 | 2026-02-20 | Initial calibration | PROJ-001 FEAT-015 (license header replacement) + PROJ-004 SPIKE-001 | 0.55 / 0.70 / 0.80 / 0.88 | Initial calibration. Replaces provisional 0.60/0.80/0.90 from Phase 3. |

*Add rows here when recalibrations are performed.*

---

## References

| Source | Content | Path |
|--------|---------|------|
| SPIKE-001 Threshold Proposal | Full derivation of defaults, Operation Cost Catalog, Sensitivity Analysis, Calibration Protocol (source) | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-6-thresholds/threshold-analyst/threshold-proposal.md` |
| SPIKE-001 Run Analysis | PROJ-001 FEAT-015 empirical data, 17-step fill trajectory | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-2-analysis/run-analyzer/run-analysis.md` |
| FEAT-001 Validation Report | ST-003 validation evidence, PROJ-004 empirical session data | `projects/PROJ-004-context-resilience/orchestration/feat001-impl-20260220-001/impl/phase-6-validation/st-003-exec/validation-report.md` |
| ConfigThresholdAdapter | Implementation of threshold defaults and config override | `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` |
| quality-enforcement.md | AE-006a-e rules, criticality levels, enforcement architecture | `.context/rules/quality-enforcement.md` |
| ADR-EPIC002-002 | 5-layer enforcement architecture, context rot research | Referenced via SPIKE-001 Phase 1/2 findings |

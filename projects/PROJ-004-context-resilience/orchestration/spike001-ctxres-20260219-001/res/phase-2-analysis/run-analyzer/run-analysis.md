# Run Analysis: PROJ-001 Context Exhaustion Patterns

> **PS ID:** SPIKE-001 | **Entry ID:** phase-2-analysis | **Agent:** run-analyzer
> **Date:** 2026-02-19 | **Version:** 1.0
> **Data Source:** PROJ-001 ORCHESTRATION.yaml (feat015-licmig-20260217-001), artifact file sizes, WORKTRACKER.md

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Executive findings: estimated consumption, risk points, resumption gaps |
| [L1 Detailed Analysis](#l1-detailed-analysis) | Workflow profile, consumption model, exhaustion risk points, resumption assessment |
| [L2 Empirical Data](#l2-empirical-data) | Token budget tables, cumulative fill projection, Phase 3 recommendations |
| [Methodology and Limitations](#methodology-and-limitations) | How estimates were derived and what is uncertain |
| [Self-Review Checklist](#self-review-checklist) | S-010 compliance |
| [References](#references) | Source files and traceability |

---

## L0 Summary

**Key Finding:** The PROJ-001 FEAT-015 License Migration workflow produced 35 markdown artifact files totaling 674,366 bytes (~168,600 tokens of artifact text). This volume, combined with the orchestrator's own context consumption (prompt engineering, tool calls, state management), projects to approximately 85-95% context fill by QG-Final under a 200K token window. The workflow completed successfully, but represents a near-capacity scenario.

**Critical Observations:**

1. **Quality gate iterations are the dominant cost driver.** QG-1 alone (3 iterations x 3 strategies) produced 9 artifact files totaling ~290K bytes (~72,500 tokens). A single quality gate iteration with S-014 + S-007 + S-002 costs an estimated 15,000-25,000 tokens in context (prompt + read deliverable + produce review + write artifact).

2. **Context was likely NOT exhausted during FEAT-015** because this workflow was executed across multiple sessions (evidenced by the checkpoint/resumption architecture and the fact that all timestamps show the same date, suggesting manual coordination). The orchestrator session would have been reset between phases.

3. **The resumption section is structurally sound but semantically thin.** It captures current state, next step, and files to read, but omits: accumulated quality findings, defect patterns across gates, inter-phase decisions, and the actual revision content that was applied between gate iterations.

4. **The ORCHESTRATION_PLAN explicitly identified context compaction as a MEDIUM likelihood, MEDIUM impact risk** for Phase 3 (50+ files), with the mitigation of "checkpoint after every 20 files" and AE-006 human escalation. This confirms the framework authors were already aware of the risk.

5. **Empirical evidence of AE-006 escalation exists** in PROJ-001's WORKTRACKER.md: FEAT-024 (MkDocs setup) had QG-1 reach max retries at score 0.9155, triggering user escalation. While this was a score-based escalation rather than a context-based one, it demonstrates the escalation pathway works for quality gates but has no equivalent for context exhaustion.

---

## L1 Detailed Analysis

### Workflow Profile

| Metric | Value | Source |
|--------|-------|--------|
| Workflow ID | `feat015-licmig-20260217-001` | ORCHESTRATION.yaml |
| Criticality | C2 (Standard) | ORCHESTRATION.yaml |
| Total Phases | 4 | ORCHESTRATION.yaml |
| Total Execution Agents | 8 | ORCHESTRATION.yaml metrics |
| Total Quality Gates | 4 (QG-1, QG-2, QG-3, QG-Final) | ORCHESTRATION.yaml |
| Total QG Iterations | 9 (3+2+2+2) | ORCHESTRATION.yaml iteration_history |
| Gates Passed First Attempt | 0 of 4 | ORCHESTRATION.yaml metrics |
| Total Artifact Files | 35 markdown files | File system count |
| Total Artifact Bytes | 674,366 bytes | File system measurement |
| Estimated Artifact Tokens | ~168,600 | bytes / 4 heuristic |
| State Files (YAML + Plan) | 60,800 bytes (~15,200 tokens) | File system measurement |
| Enablers | 6 (EN-930 through EN-935) | ORCHESTRATION.yaml |
| Effort Points | 14 | ORCHESTRATION.yaml metrics |

**Quality Gate Iteration Detail:**

| Gate | Iterations | Score Trajectory | Total QG Artifact Bytes |
|------|-----------|------------------|------------------------|
| QG-1 | 3 | 0.825 -> 0.916 -> 0.941 | ~290,000 (9 files) |
| QG-2 | 2 | 0.960 -> 0.951 | ~152,000 (6 files) |
| QG-3 | 2 | 0.873 -> 0.935 | ~127,000 (6 files) |
| QG-Final | 2 | 0.906 -> 0.934 | ~136,000 (6 files) |

### Context Consumption Model

The orchestrator context window accumulates tokens from several sources. Here is the model for what happens within a single Claude Code session running the FEAT-015 workflow.

**Fixed Overhead (session start):**

| Component | Estimated Tokens | Notes |
|-----------|-----------------|-------|
| System prompt + CLAUDE.md | ~3,000 | Claude Code base |
| .claude/rules/ (L1 layer) | ~12,500 | Per ADR-EPIC002-002 |
| L2 reinject tags | ~600/prompt | Per quality-enforcement.md |
| ORCHESTRATION.yaml (state read) | ~7,500 | 29,787 bytes / 4 |
| ORCHESTRATION_PLAN.md (context read) | ~7,750 | 31,013 bytes / 4 |
| **Total fixed overhead** | **~31,350** | ~15.7% of 200K |

**Per-Agent Execution Cost:**

Each agent invocation via the Task tool involves the orchestrator: (1) constructing the dispatch prompt, (2) the agent reading input artifacts via tool calls, (3) the agent producing its work, (4) writing output artifacts, (5) the orchestrator receiving the agent response summary.

| Operation | Min Tokens | Typical Tokens | Max Tokens | Notes |
|-----------|-----------|---------------|-----------|-------|
| Agent dispatch prompt | 1,500 | 3,000 | 5,000 | Includes instructions, inputs, constraints |
| Agent reads input files | 500 | 2,000 | 8,000 | Depends on input artifact count/size |
| Agent response to orchestrator | 1,000 | 3,000 | 8,000 | Summary returned to parent context |
| Orchestrator state update | 300 | 800 | 2,000 | YAML update, worktracker entry |
| **Per-agent total** | **3,300** | **8,800** | **23,000** | |

**Per-Quality-Gate-Iteration Cost:**

Each QG iteration runs 3 strategy agents (adv-scorer S-014, adv-executor S-007, adv-executor S-002). The deliverable must be read by each agent, and each produces a review artifact.

| Operation | Min Tokens | Typical Tokens | Max Tokens | Notes |
|-----------|-----------|---------------|-----------|-------|
| Read deliverable(s) into context | 2,000 | 5,000 | 15,000 | QG-Final reads 6 deliverables |
| S-014 scorer prompt + response | 3,000 | 6,000 | 10,000 | 6-dimension rubric scoring |
| S-007 executor prompt + response | 2,000 | 5,000 | 8,000 | Constitutional compliance |
| S-002 executor prompt + response | 3,000 | 7,000 | 12,000 | Devil's Advocate (largest artifact type) |
| Gate decision + state update | 500 | 1,000 | 2,000 | YAML update, verdict recording |
| Revision (if REVISE/REJECTED) | 2,000 | 5,000 | 10,000 | Agent re-executes with findings |
| **Per-iteration total** | **12,500** | **29,000** | **57,000** | |

**Empirical Artifact Size Calibration:**

The actual persisted artifact file sizes provide ground-truth calibration for the "agent response" estimates. Converting bytes to tokens (bytes / 4):

| Artifact Type | Actual Size Range (bytes) | Tokens (bytes/4) | Example |
|---------------|--------------------------|-------------------|---------|
| Phase agent output (small) | 967 - 2,606 | 242 - 652 | license-replacer, notice-creator, metadata-updater |
| Phase agent output (medium) | 5,303 - 6,768 | 1,326 - 1,692 | ci-validator-implementer, header-applicator |
| Phase agent output (large) | 26,356 | 6,589 | audit-executor-dep-audit |
| QG S-014 scorer result | 10,626 - 33,413 | 2,657 - 8,353 | adv-scorer-s014-result |
| QG S-007 constitutional result | 14,019 - 25,753 | 3,505 - 6,438 | adv-executor-s007-result |
| QG S-002 devil's advocate result | 17,349 - 38,716 | 4,337 - 9,679 | adv-executor-s002-result |

**Key observation:** S-002 (Devil's Advocate) consistently produces the largest artifacts (up to 38,716 bytes / ~9,700 tokens per review). This makes it the single most expensive quality strategy in terms of context consumption.

### Exhaustion Risk Points

Modeling the cumulative context consumption assuming a single-session execution of the entire FEAT-015 workflow:

**Phase 1 (1 agent + QG-1 at 3 iterations):**
- Fixed overhead: ~31,350
- audit-executor: ~8,800 (typical)
- QG-1 iter 1: ~29,000
- QG-1 iter 2 (revision + re-score): ~29,000
- QG-1 iter 3 (revision + re-score): ~29,000
- **Cumulative after Phase 1: ~127,150 tokens (63.6%)**

This is the first critical finding: **after a single phase with one agent and three quality gate iterations, the context would already be 63.6% full.** The quality gate iterations are disproportionately expensive because each iteration requires reading the deliverable, running all three strategies, and potentially revising.

**Phase 2 (3 agents + QG-2 at 2 iterations):**
- 3 agents (parallel but sequential in context): 3 x ~8,800 = ~26,400
- QG-2 iter 1 (3 deliverables scored): ~35,000 (larger due to 3 deliverables)
- QG-2 iter 2: ~35,000
- **Cumulative after Phase 2: ~223,550 tokens (111.8%)**

**This exceeds the 200K context window.** In practice, Claude Code's context compaction would trigger somewhere during Phase 2 or at the QG-2 boundary, resetting context size.

**Phase 3 (2 agents + QG-3 at 2 iterations):**
- Assuming compaction occurred (reset to ~40-60K):
- 2 agents: 2 x ~8,800 = ~17,600
- QG-3 iter 1: ~29,000
- QG-3 iter 2: ~29,000
- **Post-compaction Phase 3: ~115,600 - 135,600 tokens**

**Phase 4 (2 agents + QG-Final at 2 iterations):**
- 2 agents: 2 x ~8,800 = ~17,600
- QG-Final iter 1 (6 deliverables): ~45,000 (largest gate, scoring all deliverables)
- QG-Final iter 2: ~45,000
- **Post-compaction Phase 4: ~223,200 - 243,200 tokens**

**QG-Final is a second compaction trigger point** because it must read ALL prior deliverables for comprehensive scoring.

**Identified Risk Points (ranked by severity):**

| Risk Point | When | Why | Estimated Fill % |
|------------|------|-----|-----------------|
| RP-1: QG-1 iteration 3 | End of Phase 1 | 3 iterations of 3-strategy scoring | ~63.6% |
| RP-2: QG-2 scoring | During Phase 2 gate | 3 deliverables x 3 strategies x 2 iterations | >100% (compaction trigger) |
| RP-3: QG-Final scoring | During final gate | 6 deliverables x 3 strategies x 2 iterations | >100% (second compaction trigger) |
| RP-4: Any gate at max iterations | QG hit iteration 3 | Each additional iteration adds ~29K tokens | Variable |
| RP-5: Phase 3 bulk operations | During header application | 403 files touched, verifier scans all | ~50-70% post-compaction |

### Resumption State Assessment

The `resumption:` section in ORCHESTRATION.yaml (lines 638-649) captures:

```yaml
resumption:
  last_checkpoint: "CP-003"
  current_state: "WORKFLOW COMPLETE. All 4 phases done..."
  next_step: "Close FEAT-015 feature entity and update WORKTRACKER.md."
  files_to_read:
    - "projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md"
    - "projects/PROJ-001-oss-release/ORCHESTRATION.yaml"
    - "projects/PROJ-001-oss-release/WORKTRACKER.md"
  cross_session_portable: true
  ephemeral_references: false
```

**What is captured (strengths):**

| Element | Assessment |
|---------|------------|
| Last checkpoint ID | Sufficient for identifying recovery point |
| Current state summary | Human-readable, captures high-level status |
| Next step | Clear, actionable |
| Files to read | Lists the 3 key state files |
| Cross-session portability flag | Declares intent for session portability |

**What is missing (gaps for context resilience):**

| Gap | Impact | Severity |
|-----|--------|----------|
| **RG-1: No accumulated defect context.** QG-1 had 6 major findings in iter 1, 3 in iter 2. These findings are in the gate artifacts but not summarized in resumption. A new session would not know what was already fixed. | A new session might re-introduce previously fixed defects or waste time re-discovering known issues. | HIGH |
| **RG-2: No inter-phase decision log.** Phase 2 QG-2 iter 1 found copyright holder inconsistency between NOTICE and header_template. The resolution (align to 'Adam Nowak') was applied as a cross-phase revision. This decision is not in resumption. | Cross-phase decisions are invisible to a resumed session. | HIGH |
| **RG-3: No context fill level at checkpoint.** The resumption section does not record how much context was used when the checkpoint was created. | A new session cannot assess whether the remaining work fits in a fresh context window. | MEDIUM |
| **RG-4: No revision content summaries.** Each gate iteration involved revisions (primary_defect fields in iteration_history). These are in ORCHESTRATION.yaml but not surfaced in the resumption section. | A resumed session must parse the full YAML to understand revision history. | MEDIUM |
| **RG-5: No artifact dependency graph.** The resumption section lists files to read but does not indicate which artifacts depend on which. | A resumed session does not know the minimum set of artifacts to load for a specific phase. | LOW |
| **RG-6: No compaction event record.** If compaction occurred, there is no record of what was lost. | Post-compaction sessions cannot know what context was dropped. | HIGH |

---

## L2 Empirical Data

### Token Budget Estimates

Based on measured PROJ-001 FEAT-015 artifact file sizes and the bytes-to-tokens heuristic (bytes / 4, which is standard for English markdown text with code snippets):

| Operation Type | Min Tokens | Typical Tokens | Max Tokens | Evidence Basis |
|----------------|-----------|---------------|-----------|----------------|
| Session fixed overhead (rules + state) | 28,000 | 31,350 | 35,000 | ADR-EPIC002-002 (12.5K rules) + measured YAML/Plan sizes |
| L2 reinject per prompt | 500 | 600 | 700 | quality-enforcement.md spec |
| Phase agent execution (simple) | 3,300 | 5,000 | 8,000 | Measured: license-replacer 967B, metadata-updater 2,606B |
| Phase agent execution (complex) | 8,000 | 12,000 | 23,000 | Measured: audit-executor 26,356B, header-applicator 6,768B |
| QG S-014 scoring | 2,700 | 5,500 | 8,400 | Measured: 10,626B to 33,413B artifact size |
| QG S-007 constitutional | 3,500 | 5,000 | 6,500 | Measured: 14,019B to 25,753B artifact size |
| QG S-002 devil's advocate | 4,300 | 7,000 | 9,700 | Measured: 17,349B to 38,716B artifact size |
| QG single iteration (all 3 strategies) | 12,500 | 29,000 | 57,000 | Sum of strategy costs + deliverable reads + state updates |
| Full gate (2 iterations avg) | 25,000 | 58,000 | 114,000 | 2x iteration cost |
| Full gate (3 iterations worst case) | 37,500 | 87,000 | 171,000 | 3x iteration cost |
| ORCHESTRATION.yaml state update | 300 | 800 | 2,000 | Incremental YAML field updates |

### Cumulative Fill Projection

This table models the context fill percentage assuming a single uninterrupted Claude Code session executing the entire FEAT-015 workflow with actual iteration counts:

| Step | Operation | Incremental Tokens | Cumulative Tokens | Fill % (200K) | Risk Level |
|------|-----------|-------------------|-------------------|---------------|------------|
| 0 | Session start (rules + state reads) | 31,350 | 31,350 | 15.7% | LOW |
| 1 | audit-executor (Phase 1) | 8,800 | 40,150 | 20.1% | LOW |
| 2 | QG-1 iteration 1 (score: 0.825) | 29,000 | 69,150 | 34.6% | LOW |
| 3 | QG-1 iteration 2 (score: 0.916) | 29,000 | 98,150 | 49.1% | MEDIUM |
| 4 | QG-1 iteration 3 (score: 0.941, PASS) | 29,000 | 127,150 | 63.6% | HIGH |
| 5 | license-replacer (Phase 2) | 5,000 | 132,150 | 66.1% | HIGH |
| 6 | notice-creator (Phase 2) | 5,000 | 137,150 | 68.6% | HIGH |
| 7 | metadata-updater (Phase 2) | 5,000 | 142,150 | 71.1% | HIGH |
| 8 | QG-2 iteration 1 (score: 0.960) | 35,000 | 177,150 | 88.6% | CRITICAL |
| 9 | QG-2 iteration 2 (score: 0.951, PASS) | 35,000 | 212,150 | **106.1%** | **COMPACTION** |
| -- | *Compaction event (reset to ~50K)* | -162,150 | 50,000 | 25.0% | -- |
| 10 | header-applicator (Phase 3) | 12,000 | 62,000 | 31.0% | LOW |
| 11 | header-verifier (Phase 3) | 8,800 | 70,800 | 35.4% | LOW |
| 12 | QG-3 iteration 1 (score: 0.873) | 29,000 | 99,800 | 49.9% | MEDIUM |
| 13 | QG-3 iteration 2 (score: 0.935, PASS) | 29,000 | 128,800 | 64.4% | HIGH |
| 14 | ci-validator-implementer (Phase 4) | 8,800 | 137,600 | 68.8% | HIGH |
| 15 | ci-validator-tester (Phase 4) | 8,800 | 146,400 | 73.2% | HIGH |
| 16 | QG-Final iteration 1 (score: 0.906) | 45,000 | 191,400 | 95.7% | CRITICAL |
| 17 | QG-Final iteration 2 (score: 0.934, PASS) | 45,000 | 236,400 | **118.2%** | **COMPACTION** |

**Key Findings from Projection:**

1. **Two compaction events are predicted** for a single-session execution of FEAT-015: once during QG-2 (~Step 9) and once during QG-Final (~Step 17).

2. **The first compaction occurs at 88.6-106.1% fill**, meaning the orchestrator would lose access to Phase 1 context (audit findings, QG-1 defect history) just as it enters Phase 2 quality review.

3. **Post-compaction, Phase 3 + QG-3 alone consumes ~79K tokens**, demonstrating that even a single phase with 2 agents and 2 QG iterations occupies ~40% of a fresh window after compaction.

4. **QG-Final is inherently expensive** because it scores ALL prior deliverables (6 files), requiring the orchestrator to read them all back into context. This makes it a guaranteed high-fill operation regardless of prior compaction.

5. **The "worst case" scenario** -- where any gate takes 3 iterations -- pushes the budget catastrophically. If QG-2 had taken 3 iterations instead of 2, it would have added ~35,000 more tokens, triggering compaction even earlier and deeper into Phase 2 execution.

### Context Exhaustion Probability by Workflow Complexity

Extrapolating from PROJ-001 data to other orchestration patterns:

| Workflow Profile | Phases | Agents | QG Iterations (est.) | Est. Total Tokens | Compaction Events | Risk |
|-----------------|--------|--------|---------------------|-------------------|-------------------|------|
| Minimal (C1, 1 phase) | 1 | 1-2 | 2 | 60-80K | 0 | LOW |
| FEAT-015 style (C2, 4 phases) | 4 | 8 | 9 | ~350-400K | 2 | HIGH |
| EPIC-003 style (C3, 5+ phases) | 5+ | 15+ | 15+ | ~600K+ | 4+ | CRITICAL |
| C4 tournament (all 10 strategies) | 1+ | 10+ | N/A | ~200K+ per gate | 1+ per gate | CRITICAL |

### Recommendations for Phase 3

Based on this empirical analysis, the Phase 3 detection method evaluation should prioritize:

1. **Detection must occur BEFORE compaction, not after.** The analysis shows compaction triggers around 80-90% fill. A detection mechanism needs to fire early enough (70-80%) to allow the orchestrator to take proactive action (checkpoint, hand off to new session, save resumption context).

2. **Quality gate iterations are the primary intervention point.** The largest token consumers are not phase agents (which are relatively cheap at 5-12K tokens) but QG iterations (29-45K tokens each). A context-aware gate could decide to defer scoring of older deliverables or reduce strategy depth at high fill levels.

3. **The UserPromptSubmit hook approach (from Phase 1 findings) is well-suited** because it can inject context fill percentage at every prompt, giving the orchestrator continuous visibility. The ECW status line's `extract_context_info()` function already computes `(percentage, used_tokens, context_window_size, is_estimated)`, which is exactly what is needed.

4. **Resumption context enrichment is essential.** The current resumption section is too thin for effective cross-session recovery. It should include:
   - Context fill level at last checkpoint
   - Accumulated defect summary (not just primary_defect)
   - Cross-phase decisions log
   - Compaction event history
   - Minimum artifact set for each remaining phase

5. **QG-Final is the worst-case scenario for context consumption** and needs special handling -- possibly running in a dedicated session with only the deliverables loaded, rather than at the end of a full workflow session.

6. **The 200K window is insufficient for C3+ workflows in a single session.** The framework must be designed around the assumption that multi-phase orchestrations WILL require session boundaries, and those boundaries need to be managed rather than accidental.

---

## Methodology and Limitations

**Token estimation approach:** File sizes in bytes were measured directly from the filesystem using `wc -c`. The bytes-to-tokens conversion uses a 4:1 ratio (bytes / 4), which is a standard heuristic for English text with markdown formatting. Actual token counts may vary by 10-20% depending on whitespace, code blocks, and special characters.

**Context consumption model:** The "per-agent" and "per-QG-iteration" token estimates combine measured artifact sizes (output only) with estimated prompt and tool-call overhead. The prompt/tool overhead estimates are based on typical Claude Code Task tool invocation patterns and are the least precise component of the model. The actual overhead depends on how much input the orchestrator provides in the dispatch prompt and how verbose the agent summary is.

**Single-session assumption:** The cumulative fill projection assumes the entire workflow runs in one session. In practice, PROJ-001 FEAT-015 may have been executed across multiple sessions (the timestamps are all "2026-02-17T00:00:00Z", which looks like placeholder dates rather than actual execution timestamps). If sessions were split at phase boundaries, each session would start fresh and no compaction would occur. However, the single-session model is the relevant stress test for context resilience design.

**Compaction behavior assumption:** The model assumes Claude Code compaction resets context to approximately 50K tokens (25% of window). Actual compaction behavior depends on Claude Code's internal algorithm, which is not publicly documented. The compaction may retain more or less depending on what it considers important.

**Limitations:**
- No actual runtime token telemetry exists for PROJ-001. All consumption values are estimates.
- The orchestrator's own reasoning tokens (chain-of-thought) are not visible in artifact files and are not included in the model. These could add 10-30% overhead.
- Cached tokens (prompt caching) may reduce actual consumption but do not reduce context fill from the model's perspective.
- The model does not account for tool call round-trip overhead (JSON serialization of Read/Write/Bash results).

---

## Self-Review Checklist

- [x] PROJ-001 ORCHESTRATION.yaml fully analyzed (650 lines, all 4 phases, 4 gates, 9 iterations, resumption section)
- [x] Token consumption estimates are evidence-based (measured artifact file sizes: 35 files, 674,366 bytes)
- [x] Cumulative fill projection covers entire workflow (17 steps from session start through QG-Final)
- [x] Resumption gaps identified with specifics (6 gaps: RG-1 through RG-6)
- [x] Recommendations connect to Phase 3 detection method evaluation (6 recommendations)
- [x] L0/L1/L2 levels present
- [x] Navigation table with anchor links (H-23, H-24)
- [x] Limitations disclosed honestly (P-022)

---

## References

| Source | Path | Content Used |
|--------|------|-------------|
| ORCHESTRATION.yaml | `projects/PROJ-001-oss-release/ORCHESTRATION.yaml` | Workflow structure, QG iterations, scores, resumption section, metrics |
| ORCHESTRATION_PLAN.md | `projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md` | Workflow architecture, risk mitigations (context compaction risk), agent registry |
| WORKTRACKER.md | `projects/PROJ-001-oss-release/WORKTRACKER.md` | AE-006 escalation evidence (FEAT-024 QG-1 retry 2) |
| ADR-EPIC002-002 | `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-002-enforcement-architecture.md` | Context rot research (40-60% effectiveness at 50K+), token budget (12.9% of 200K) |
| statusline.py | `.claude/statusline.py` | `extract_context_info()` function, `extract_compaction_info()` function |
| quality-enforcement.md | `.context/rules/quality-enforcement.md` | L2 reinject token budget (~600/prompt), enforcement architecture |
| Phase 1 mechanism inventory | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-1-inventory/research-inventory/mechanism-inventory.md` | GAP-001 through GAP-006, recommended approach |
| FEAT-015 artifact files | `projects/PROJ-001-oss-release/orchestration/feat015-licmig-20260217-001/lic/` | 35 files measured by byte size |

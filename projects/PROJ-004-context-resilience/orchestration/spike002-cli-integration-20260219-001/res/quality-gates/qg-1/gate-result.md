# QG-1: Architecture Review - Gate Result

<!-- QG-ID: QG-1 | DELIVERABLE: ADR-SPIKE002-001 | CRITICALITY: C2 | DATE: 2026-02-19 -->
<!-- AGENT: adv-scorer v1.0.0 | MODEL: claude-opus-4-6 -->

> Quality gate assessment for ADR-SPIKE002-001 (CLI-Integrated Context Resilience Architecture). Scored against S-014 LLM-as-Judge 6-dimension rubric with S-003, S-007, and S-002 applied per H-16 ordering.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict](#verdict) | PASS/REVISE determination with composite score |
| [S-003 Steelman](#s-003-steelman) | Strongest aspects of the ADR identified before critique |
| [S-007 Constitutional Compliance](#s-007-constitutional-compliance) | Compliance check against Jerry Constitution and architecture standards |
| [S-002 Devils Advocate](#s-002-devils-advocate) | Challenges, counterarguments, and untested assumptions |
| [S-014 Scoring](#s-014-scoring) | 6-dimension rubric scoring with weighted composite |
| [Defects Found](#defects-found) | Prioritized defect list |
| [Recommendation](#recommendation) | Specific revisions or future considerations |

---

## Verdict

**PASS -- 0.93 weighted composite**

The ADR meets the quality gate threshold (>= 0.92). Minor defects were identified but none are blocking. The deliverable demonstrates strong evidence-based reasoning, thorough alternative analysis, and clear traceability to Phase 1 and Phase 2 artifacts.

---

## S-003 Steelman

Per H-16, the strongest aspects of the ADR are identified before any critique is applied.

### 1. Evidence Saturation

The ADR is exceptionally well-grounded in empirical evidence. Every architectural claim maps to specific source file, line number, and capability discovered in the Phase 1 Audit. The Evidence section (lines 609-648) provides 11 Phase 1 traceability entries and 10 Phase 2 traceability entries, each with specific audit section and evidence text. This is not superficial citation -- the ADR names exact files (e.g., `prompt_reinforcement_engine.py`, 246 lines), exact line numbers (e.g., `in_memory_session_repository.py` line 35), and exact values (e.g., `_DEFAULT_TOKEN_BUDGET = 600`). This level of evidence grounding is substantially above typical ADR quality.

### 2. Honest Alternative Analysis

The four alternatives are analyzed with genuine respect for each option's strengths. Alternative 1 (Hook-Only) is credited with 4 real pros: complete isolation, simpler mental model, no risk of breaking CLI, and faster prototyping. Alternative 4 (Status Line) is credited with exact context data and minimal hook logic. The rejected alternatives are not strawmen -- the ADR acknowledges that Alternative 1's isolation advantage is genuine and that Alternative 4's data precision is genuinely superior. The rejection rationale is based on specific, verifiable claims (e.g., 18-28% effort savings, 5000ms timeout constraint) rather than subjective preference.

### 3. Two-Phase Migration Architecture

The decision to defer bounded context extraction is architecturally sophisticated. The ADR explicitly defines three measurable extraction criteria (domain concept stability, persistent repository availability, boundary validation) rather than using vague "when ready" language. The Phase 1/Phase 2 directory structure comparison (lines 546-577) provides concrete before/after views that make the migration path tangible. The extraction triggers (line 580-582) are framed as falsifiable conditions, not aspirations.

### 4. Comprehensive Negative Consequences

The ADR documents 4 genuine negative consequences with specific risk mitigation details. The hook import latency risk (Consequence Negative #3, line 198) is particularly honest: the ADR admits the 3000ms/2000ms budget split is "based on estimation, not measurement" and explicitly states the failure mode (Claude Code silently drops hook output). This kind of self-aware risk disclosure is a quality signal.

### 5. Interface Contract Precision

The 4 interface contracts (lines 405-504) specify frozen dataclasses with type hints, docstrings referencing pattern sources, and constructor parameters that clarify configuration injection points. The `ContextMonitorEngine` contract explicitly shows the `LayeredConfigAdapter | None` optional dependency injection, demonstrating awareness of fail-open instantiation (when no config adapter is available, the engine should use defaults).

### 6. Token Budget Quantification

The token budget analysis (lines 506-522) provides concrete worst-case and normal-case calculations. The per-prompt breakdown (600 + 200 + 280 = 1,080 worst case; 600 + 40 = 640 normal) and session-start breakdown (200 + 700 + 760 = 1,660 with resumption) enable reviewers to evaluate the framework overhead impact quantitatively rather than relying on "it's within budget" assertions.

---

## S-007 Constitutional Compliance

### P-002 (File Persistence): COMPLIANT

The ADR explicitly mandates file-based persistence for all cross-process state (line 79: "All state that must persist across hook invocations uses filesystem persistence"). The four state carriers are enumerated: transcript JSONL, checkpoint files, configuration TOML, and acknowledgment markers. This directly addresses P-002's requirement that agents "persist all significant outputs to the filesystem" and "SHALL NOT rely solely on conversational context for state."

### P-003 (No Recursive Subagents): COMPLIANT

The architecture does not introduce any subagent spawning. All new components are stateless engines instantiated within hook scripts (single Python process). The decision explicitly avoids the CLI subprocess pattern for UserPromptSubmit (Alternative 3 rejection, lines 149-155) in part because of process overhead, and the chosen approach uses direct Python imports rather than CLI invocations that could spawn further processes.

### P-022 (No Deception): COMPLIANT

The ADR is transparent about limitations and risks. Key honesty markers:
- Admits the latency budget is "based on estimation, not measurement" (line 198)
- Acknowledges the InMemorySessionRepository limitation prevents session event integration (line 196)
- States that file-based acknowledgment is "pragmatic" but "architecturally inferior to domain event integration" (line 208)
- Declares Method C timing dependency is "an open question (SPIKE-001 OQ-1)" (line 169)

### H-07/H-08 (Layer Dependencies): COMPLIANT WITH NOTE

New engines are placed in `src/infrastructure/internal/enforcement/` (infrastructure layer). They import from the same layer or from stdlib. The `LayeredConfigAdapter` dependency is an infrastructure-to-infrastructure import, which is permitted. The `ContextMonitorEngine` reads files and produces strings -- it does not import from domain, application, or interface layers. **Note:** The inline domain concepts (ThresholdTier, FillEstimate, CheckpointData) are defined within infrastructure files in Phase 1, which means domain concepts temporarily reside in the infrastructure layer. This is architecturally impure but acknowledged as intentional (Phase 1 placement with Phase 2 extraction path). The ADR documents this as a conscious trade-off (Negative Consequence #4, line 200).

### H-09 (Composition Root Exclusivity): COMPLIANT WITH NOTE

The engines are instantiated in hook scripts (e.g., `user-prompt-submit.py`, `session_start_hook.py`), not in `bootstrap.py`. This is consistent with the existing pattern: `PromptReinforcementEngine` is already instantiated in `user-prompt-submit.py` (Phase 1 Audit: C5, line 53-58), not via the composition root. Hooks operate as independent entry points with their own composition logic. This is technically a deviation from strict H-09, but it follows the established precedent that hook scripts serve as their own composition roots. The deviation is acceptable and consistent.

### H-10 (One Class Per File): COMPLIANT

The ADR proposes 4 new files with 1 engine class each: `context_monitor_engine.py`, `compaction_alert_engine.py`, `checkpoint_writer.py`, `resumption_context_generator.py`. The `@dataclass(frozen=True)` result types (e.g., `ContextMonitorResult`) co-exist with their engine class in the same file. This follows the existing pattern: `PromptReinforcementEngine` has its `ReinforcementResult` in the same file (Phase 1 Audit: C4). H-10 specifies "one public class or protocol" -- frozen dataclasses used as return types are not independent public classes but subordinate value objects of the engine's interface.

### H-23/H-24 (Navigation): COMPLIANT

Navigation table present at lines 8-20 with anchor links for all 10 major sections. All anchors are correctly formatted (lowercase, hyphen-separated).

### Architecture Standards (Bounded Context Communication): COMPLIANT

The ADR references the architecture standard "Bounded contexts SHOULD communicate via domain events or shared kernel only" (line 488, 582). The Phase 2 design shows `ContextThresholdReached` domain event communication from `context_monitoring` to `session_management`, with `SessionId` as shared kernel. This follows the MEDIUM-tier guidance correctly.

### Overall Constitutional Compliance: **COMPLIANT**

No constitutional violations detected. Two notes recorded (H-07/H-08 domain concepts in infrastructure, H-09 hook-level composition) but both are consistent with established precedent and explicitly acknowledged in the ADR.

---

## S-002 Devils Advocate

### Challenge 1: Is the 18-28% Effort Savings Claim Reliable?

The ADR claims effort reduction from 25-37 hours to 18-26 hours (18-28%). However, the Phase 2 Gap Analysis Effort Summary (line 883-886) actually totals 20.5-26.5 hours, not 18-26 hours. The ADR's Context section (line 45) cites "18-26 hours" which matches the Phase 2 L0 Summary's "18-26 hours" claim. There is an internal inconsistency in the Phase 2 Gap Analysis between its L0 Summary (18-26 hours) and its Effort Summary table (20.5-26.5 hours). The ADR inherits this inconsistency from its source document. The actual savings may be closer to 14-24% (using 20.5-26.5 hours) rather than 18-28%.

**Severity:** P3 (Minor). The savings exist regardless of the exact percentage. The qualitative argument (reuse reduces effort) is sound.

### Challenge 2: Is the Hook Import Latency Risk Adequately Mitigated?

The ADR acknowledges latency risk (Negative Consequence #3) but the mitigation is "based on estimation, not measurement." The performance budget (1000ms + 1500ms + 500ms = 3000ms, 2000ms headroom) is a plausible estimate, but:

- Python import time for `ContextMonitorEngine` is unknown. If the engine imports `LayeredConfigAdapter`, that adapter imports `toml` parsing, which imports further dependencies.
- JSONL transcript parsing involves file I/O. For a 50+ prompt session, the transcript could be >100KB. Even with seek-to-end optimization, the first-time import + parse is uncharacterized.
- The failure mode (silent drop) means the user gets zero feedback if the budget is exceeded.

The ADR recommends measuring latency empirically after CWI-03 implementation (L2 Strategic Implications, line 592: "Measure hook latency empirically"). This is the correct approach but leaves a gap: the architecture is committed before the risk is validated.

**Severity:** P3 (Minor). The ADR explicitly acknowledges the risk and proposes measurement. The 2000ms headroom is substantial. Existing hooks (which already import engines) operate within the 5000ms budget.

### Challenge 3: Are the Extraction Criteria for Phase 2 Falsifiable?

The three Phase 2 extraction criteria (line 580-582) are:
1. "Domain concepts have proven stable through at least one full implementation cycle" -- What constitutes "stable"? Zero interface changes? No major refactoring? The criterion is qualitative.
2. "A persistent session repository is available" -- This is clear and falsifiable.
3. "The boundary between context_monitoring and session_management is empirically validated" -- What constitutes "validated"? This is vague.

Criteria 1 and 3 risk becoming perpetual deferrals because they lack measurable definitions of "stable" and "validated." A strict reading could delay Phase 2 indefinitely.

**Severity:** P3 (Minor). The criteria are directionally useful even if not perfectly falsifiable. The risk is organizational (deferred indefinitely) rather than technical (incorrect architecture).

### Challenge 4: Does Placing Domain Concepts in Infrastructure Create a Refactoring Tax?

The ADR places `ThresholdTier`, `FillEstimate`, and `CheckpointData` inline in infrastructure engine files. When Phase 2 extraction occurs, every file that imports these types must be updated. If the engines are well-adopted (e.g., test files, hook scripts, utility scripts all reference `ThresholdTier`), the refactoring surface could be larger than anticipated.

**Counter-argument (Steelman):** The ADR addresses this at line 200: "the risk of premature abstraction is judged higher than the migration cost." And since Phase 1 engines are internal (in `infrastructure/internal/enforcement/`), the import surface is limited to hook scripts and tests -- not public API consumers.

**Severity:** P3 (Minor). The import surface is limited and the trade-off is explicitly reasoned.

### Challenge 5: Is the Rejection of Alternative 4 (Status Line) Too Conservative?

Alternative 4 offers exact context data -- the status line reads `context_window.current_usage.input_tokens` directly from Claude Code. The ADR rejects it primarily on timing uncertainty (one-prompt lag). But:

- The one-prompt lag is a known quantity. At each threshold (70%, 80%, 88%), a one-prompt lag means at most ~29K tokens of drift (per the SPIKE-001 calibration). The thresholds have 10% gaps between tiers, which is ~20K tokens in a 200K context window. A 29K drift would overshoot by one tier in the worst case.
- Alternative 4 could serve as the primary mechanism with Method A as a fallback, rather than the reverse.

**Counter-argument (Steelman):** The ADR correctly identifies that building the entire system on an unvalidated assumption (OQ-1) violates engineering rigor (line 169). The conservative choice (use proven Method A as primary, investigate Method C as upgrade) is the lower-risk path. CWI-08 preserves the option to upgrade later.

**Severity:** P3 (Minor). The rejection is conservative but defensible. The upgrade path via CWI-08 preserves optionality.

### Challenge 6: Missing Rollback Strategy

The ADR does not discuss what happens if Phase 1 implementation fails or produces unacceptable results. There is no rollback strategy: if the new engines cause hook timeouts, cause unexpected behavior, or prove unmaintainable, the ADR does not describe how to revert. Given that the decision modifies existing hooks (`user-prompt-submit.py`, `session_start_hook.py`) and adds new hook registrations to `hooks.json`, a failed implementation would require removing these changes.

**Severity:** P2 (Significant). An ADR for a C2 deliverable should address reversibility, especially when the Context section's Force #3 mentions process boundary isolation as a design constraint. The reversibility path is straightforward (remove new engine imports from hooks, remove new hook entries from hooks.json) but should be documented.

---

## S-014 Scoring

| Dimension | Weight | Score | Evidence |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.95 | All standard ADR sections present: Status, Context, Decision, Alternatives Considered, Consequences. Extended with L0/L1/L2 detail levels, Interface Contracts, Token Budget Analysis, Evidence traceability. Self-Review checklist present. Minor gap: no rollback strategy (P2 defect). |
| Internal Consistency | 0.20 | 0.91 | The effort savings claim (18-28%, 18-26 hours) has a minor inconsistency with Phase 2 source data (20.5-26.5 hours). All other claims are internally consistent. Component names, file paths, and pattern references are consistent between Decision, L1 Technical Details, and Evidence sections. Threshold values are consistent across Context, Decision, and Data Flow sections. |
| Methodological Rigor | 0.20 | 0.95 | Four alternatives systematically analyzed with genuine pros/cons. Forces explicitly enumerated. Consequences categorized as positive/negative/neutral. Risk analysis addresses 6 specific risks with severity, impact, mitigation, and residual risk. Token budget quantified for worst-case and normal operation. Two-phase approach with explicit extraction criteria. Self-Review (S-010) applied with 10 verification items. |
| Evidence Quality | 0.15 | 0.96 | 11 Phase 1 traceability entries with specific file names, line numbers, and quoted values. 10 Phase 2 traceability entries with section references. 5 Architecture Standards traceability entries with specific rule IDs. Evidence is verifiable -- a reviewer can check each claim against the cited source. The evidence section is among the strongest in the deliverable. |
| Actionability | 0.15 | 0.92 | Interface contracts provide implementation-ready type signatures. Data flow diagrams (3 hook flows) provide step-by-step implementation sequences. Token budget table enables capacity planning. Component placement table maps each new engine to a specific file path. The L2 section provides FEAT-001 implementation guidelines with dependency ordering. Minor gap: no explicit acceptance criteria for the ADR decision itself (acceptance criteria exist in Phase 2 CWI items but not in the ADR). |
| Traceability | 0.10 | 0.94 | Every claim in the ADR maps to either Phase 1 Audit, Phase 2 Gap Analysis, or Architecture Standards. The Evidence section (lines 609-648) provides a structured traceability matrix. Architecture standards compliance is documented with specific rule IDs (H-10, H-07, H-08). Minor gap: the Phase 2 Gap Analysis effort inconsistency (18-26 vs. 20.5-26.5 hours) is inherited without flagging the discrepancy. |

### Weighted Composite Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.95 | 0.190 |
| Internal Consistency | 0.20 | 0.91 | 0.182 |
| Methodological Rigor | 0.20 | 0.95 | 0.190 |
| Evidence Quality | 0.15 | 0.96 | 0.144 |
| Actionability | 0.15 | 0.92 | 0.138 |
| Traceability | 0.10 | 0.94 | 0.094 |
| **Total** | **1.00** | | **0.938** |

**Weighted Composite: 0.94 (rounded from 0.938)**

**Band: PASS (>= 0.92)**

### Leniency Bias Counter-Check

To counteract leniency bias, I reviewed each score above 0.90 for potential inflation:

- **Completeness (0.95):** Justified. The ADR covers all standard sections plus extended detail levels. The missing rollback strategy prevents a higher score.
- **Internal Consistency (0.91):** Strictly scored. The effort data inconsistency is a real flaw that prevents this dimension from reaching 0.93+. The 0.91 reflects the gap.
- **Methodological Rigor (0.95):** Justified. The four-alternative analysis with honest pros/cons, quantified token budgets, and explicit extraction criteria demonstrate systematic methodology. One could argue 0.93 given the qualitative nature of two Phase 2 extraction criteria, but the overall rigor level supports 0.95.
- **Evidence Quality (0.96):** Justified. This is the ADR's strongest dimension. The evidence is specific, verifiable, and comprehensive. The 0.96 is warranted.
- **Actionability (0.92):** Conservatively scored. The ADR provides interface contracts and data flows but could improve with explicit acceptance criteria and a rollback plan.
- **Traceability (0.94):** Justified. The structured evidence matrix is strong. The inherited effort inconsistency slightly reduces the score.

**Assessment: Scores are not inflated. The composite of 0.94 reflects genuinely strong work with identifiable minor gaps.**

---

## Defects Found

| ID | Severity | Description | Recommendation |
|----|----------|-------------|----------------|
| D-001 | P2 | **Missing rollback strategy.** The ADR does not describe how to revert if the CLI-integrated approach fails during implementation. For a decision that modifies existing hooks and adds new hook registrations, reversibility should be documented. | Add a "Rollback" or "Reversibility" subsection to Consequences or Decision describing: (1) remove new engine imports from `user-prompt-submit.py` and `session_start_hook.py`, (2) remove `PreCompact` and `PostToolUse` entries from `hooks.json`, (3) delete new engine files. Estimated rollback effort: <1 hour. |
| D-002 | P3 | **Effort data inconsistency inherited from Phase 2.** The ADR cites "18-26 hours" and "18-28% savings" (lines 45, 124, 182, 218), but the Phase 2 Gap Analysis Effort Summary table totals 20.5-26.5 hours. The ADR should either reconcile the discrepancy or cite the more conservative figure. | Use the Effort Summary table values (20.5-26.5 hours) or explicitly note that the L0 Summary and Effort Summary have a ~2.5-hour discrepancy in the lower bound and use the range 18-26.5 hours. |
| D-003 | P3 | **Phase 2 extraction criteria lack measurable definitions.** Criterion 1 ("domain concepts have proven stable") and Criterion 3 ("boundary is empirically validated") are qualitative. They could benefit from measurable thresholds (e.g., "no interface-breaking changes for 2 feature cycles" for stability; "no bidirectional imports detected between context_monitoring and session_management" for boundary validation). | Add measurable definitions or examples of what "stable" and "validated" mean in practice. |
| D-004 | P3 | **No explicit handling of concurrent checkpoint writes.** The ADR discusses `AtomicFileAdapter` for safe writes but does not address what happens if two PreCompact events fire in rapid succession (e.g., multiple compactions in one session). The checkpoint ID sequencing (scan + max(NNN) + 1) has a race condition if two writes overlap. | Add a note that concurrent PreCompact events are unlikely (compaction is an infrequent event) and that `AtomicFileAdapter` with file locking mitigates the race condition. If stronger guarantees are needed, sequential file naming could use timestamps instead of sequence numbers. |
| D-005 | P3 | **PostToolUse hook placement inconsistency in component diagram.** The component diagram (lines 232-266) shows PostToolUse hook routing to "Staleness Detection Logic (inline)" but the L1 Data Flow section does not include a PostToolUse Data Flow diagram (only PreCompact and SessionStart data flows are detailed). The PostToolUse is described in the Phase 2 Gap Analysis CWI-07 but not in the ADR's L1 section. | Either add a PostToolUse Data Flow section to L1 or add a note explaining that PostToolUse is a lower-priority integration (P3, CWI-07) and will be detailed in FEAT-001 design. |

---

## Recommendation

**PASS.** The ADR meets the quality gate threshold (0.94 >= 0.92) and is approved for progression.

### Minor Findings for Future Consideration

The following defects do not block approval but should be addressed at the author's discretion, ideally before the ADR status transitions from PROPOSED to ACCEPTED:

1. **D-001 (P2 -- Rollback strategy):** Recommended to address before ACCEPTED status. A 2-3 sentence rollback subsection would resolve this.
2. **D-002 (P3 -- Effort inconsistency):** Low priority. The qualitative argument is unaffected. Could be fixed with a single-line correction to use 20.5-26.5 hours.
3. **D-003 (P3 -- Extraction criteria):** Recommended but not blocking. Adding measurable thresholds would strengthen the Phase 2 migration path.
4. **D-004 (P3 -- Concurrent writes):** Low priority. The scenario is unlikely in practice.
5. **D-005 (P3 -- PostToolUse data flow):** Low priority. The PostToolUse hook is a P3 work item (CWI-07) and can be detailed in FEAT-001 design.

### Gate Progression

- **QG-1 (Architecture Review):** PASSED at 0.94
- **Next gate:** Implementation (FEAT-001) quality gates per CWI item criticality

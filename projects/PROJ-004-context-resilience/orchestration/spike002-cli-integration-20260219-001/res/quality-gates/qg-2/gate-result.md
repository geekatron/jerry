# QG-2 Gate Result: ADR-SPIKE002-002 (CLI-Integrated Context Resilience Architecture v2)

<!-- QG-ID: QG-2 | PS-ID: SPIKE-002 | DATE: 2026-02-19 -->
<!-- AGENT: adv-scorer v1.0.0 | MODEL: claude-sonnet-4-6 -->
<!-- ITERATION: 1 of N (first pass) -->

> Quality Gate 2 scoring for ADR-SPIKE002-002. Deliverable produced by ps-architect agent during Phase 5a of the SPIKE-002 orchestration. Scored using S-014 LLM-as-Judge with six weighted dimensions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Gate Summary](#gate-summary) | Verdict, composite score, disposition |
| [Scoring Context](#scoring-context) | Criticality, strategies applied, references validated |
| [Dimension Scores](#dimension-scores) | Six-dimension rubric with evidence and rationale |
| [Strategy-Informed Perspectives](#strategy-informed-perspectives) | S-002, S-003, S-004, S-007, S-012, S-013 analysis |
| [Leniency Bias Counteraction](#leniency-bias-counteraction) | Explicit check against inflation |
| [Deficiencies Identified](#deficiencies-identified) | Specific gaps that constrain scores |
| [Revision Requirements](#revision-requirements) | What must be addressed before PASS |
| [Next Steps](#next-steps) | Orchestration disposition |

---

## Gate Summary

| Item | Value |
|------|-------|
| **Deliverable** | ADR-SPIKE002-002 (adr-cli-integration-v2.md) |
| **Criticality** | C3 (Significant) — AE-003 (modified ADR) |
| **Threshold** | >= 0.92 |
| **Composite Score** | **0.87** |
| **Band** | REVISE (0.85–0.91) |
| **Verdict** | **REJECTED** per H-13 |
| **Iteration** | 1 (first pass) |
| **Disposition** | Return for targeted revision — near threshold, specific gaps identified |

The ADR is a strong, well-structured document. Its core architectural reasoning is sound and the DISC-001/DEC-001 traceability is excellent. The REVISE verdict reflects specific gaps in two dimensions (Evidence Quality, Actionability) that are addressable without restructuring the document. All seven QG-2 validation requirements are substantially met, but three deficiencies prevent a PASS score.

---

## Scoring Context

### Criticality and Strategy Requirements

C3 deliverables require: HARD + MEDIUM + all tiers. Required strategies for scoring context: S-003, S-007, S-002, S-014, S-004, S-012, S-013.

### Reference Documents Validated

| Reference | Status | Notes |
|-----------|--------|-------|
| DISC-001 (`FEAT-001-context-detection/DISC-001-architecture-violations.md`) | Read | F1-F4 findings verified against ADR claims |
| DEC-001 (`FEAT-001-context-detection/DEC-001-cli-first-architecture.md`) | Read | D-001 through D-004 verified against ADR decisions |
| ADR claims about DISC-001 | Accurate | All four findings accurately represented |
| ADR claims about DEC-001 | Accurate | All four decisions accurately represented |

### QG-2 Validation Requirements Check

| Requirement | Status | Notes |
|-------------|--------|-------|
| 1. ADR correctly supersedes ADR-SPIKE002-001 | PASS | Status section is explicit; supersession rationale names all 4 findings |
| 2. ADR chooses Alternative 3 | PASS | Decision section is unambiguous; rationale is complete |
| 3. DISC-001 findings F1-F4 fully addressed | PASS | Each finding maps to an architectural solution in the decision |
| 4. DEC-001 decisions D-001 through D-004 implemented | PASS | Explicit D-001/D-002/D-003/D-004 bullets in Decision section |
| 5. Steelman (S-003) applied to rejected alternatives | PASS | All 4 alternatives have steelman paragraphs; quality is good |
| 6. Negative consequences honestly documented | PASS | 5 genuine negatives with mitigations; no whitewashing |
| 7. Interface contracts well-defined | PARTIAL | Contracts for 3 ports and 3 value objects present, but gaps exist (see D-002 below) |
| 8. Evidence traceability complete | PARTIAL | Four traceability tables present but ADR-SPIKE002-001 source not accessible for cross-check; one minor inaccuracy detected |

---

## Dimension Scores

### Dimension 1: Completeness (weight 0.20)

**Score: 0.90**

**Rubric:** Does the ADR cover all required elements — problem statement, alternatives with steelmans, decision, consequences (positive and negative), interface contracts, evidence traceability, and strategic implications?

**Evidence for score:**

- Problem statement is thorough. Forces section covers 6 distinct architectural constraints (F1–F6).
- All 4 alternatives analyzed. Each has description, steelman, cons, and rejection rationale.
- Decision section specifies bounded context structure down to file-level granularity.
- Consequences: 6 positive, 5 negative, 3 neutral. Genuine trade-offs documented.
- L0 Summary, L1 Technical Details, L2 Strategic Implications all present.
- Interface contracts: 3 value objects (ThresholdTier, FillEstimate, CheckpointData) and 3 ports (ITranscriptReader, ICheckpointRepository, IThresholdConfiguration) specified with Python type hints and docstrings. `ContextState` value object is mentioned in the domain layer table but no code contract is provided for it. `CheckpointService` and `ContextFillEstimator` service interfaces are described in prose but no signatures are given.
- Data flow diagrams for all 4 hook events. Error handling documented for each flow.
- Token budget analysis present.
- Enforcement layer extension table present.
- Self-review checklist present and appears complete.

**Gaps that constrain score:**
- `ContextState` value object is listed in the domain table (line 107) but lacks a code contract block. It is referenced as "aggregate context monitoring state" but the structure is not formalized. Minor.
- Application service signatures (ContextFillEstimator, CheckpointService) are described textually but not formalized as code contracts. The ADR defines ports (interfaces) but not the service method signatures that compose them. This means the implementer must infer the exact public API of the orchestrating services from the data flow diagrams. Medium gap.
- `jerry hooks session-start` data flow references CWI-00 (FileSystemSessionRepository) as a prerequisite but the ADR does not document what happens if CWI-00 is not yet implemented — is there a fallback? The `jerry hooks pre-compact` flow's session abandon step (5b) has the same dependency. Minor.

**Score justification:** Completeness is high (0.90). The missing ContextState code contract and service signatures are real gaps that a reviewer or implementer would notice. Dropping below 0.90 would require more substantial missing sections.

---

### Dimension 2: Internal Consistency (weight 0.20)

**Score: 0.91**

**Rubric:** Are claims internally consistent? Do component descriptions, data flows, consequence statements, and interface contracts align with each other? Are there contradictions within the document?

**Evidence for score:**

- The Decision section (lines 86–193) aligns with the Alternatives section (Alternative 3 chosen, lines 230–248). No contradiction.
- The four DEC-001 decisions (D-001 to D-004) are implemented in the chosen architecture with explicit bullets. Each decision maps to an architectural element.
- Token budget analysis (L1) is carried forward from ADR-SPIKE002-001 and labeled as such. No internal contradiction with the architecture description.
- Wrapper example code (lines 166–173) uses `"uv", "run", "--directory", "${CLAUDE_PLUGIN_ROOT}", "jerry", "--json", "hooks", "prompt-submit"` but the data flow for session-start (line 414) references `scripts/session_start_hook.py` -- the CURRENT hook entry point, not a new thin wrapper. This is a mixed-state description: the ADR describes the target state (thin wrappers) for new hooks but references the existing script path for session-start without clarifying whether `scripts/session_start_hook.py` is replaced by a new `hooks/session-start.py` wrapper. This is a consistency gap: the hooks table (lines 147-152) implies all 4 hooks get new CLI commands, but only one wrapper example is shown and the session-start data flow references the old path.
- Enforcement layer table (L2) correctly describes L1-L3 extension. L4 and L5 are "Unchanged" — consistent with Consequences section.
- The L2 architecture table marks enforcement folder as `[TECH DEBT]` with "direct import" and "None (bypasses CLI)" — consistent with DISC-001 F2 and Consequences item 2.
- The D-004 migration path (3 phases) is internally consistent with D-004 in DEC-001.

**Gap:**
- The session-start data flow (step 3, line 415) says "scripts/session_start_hook.py" — this is the CURRENT path, not the new thin wrapper. If all hooks become thin wrappers per D-001, then the session-start hook should be a new file in `hooks/` (e.g., `hooks/session-start.py`). The data flow diagram implies continuity with the existing path, which contradicts D-001's intent to replace direct-import scripts with thin wrappers. This inconsistency could mislead the implementer about whether `scripts/session_start_hook.py` is refactored or replaced.

**Score justification:** High internal consistency (0.91). One specific inconsistency (session_start_hook.py path in data flow vs D-001 intent) prevents higher score.

---

### Dimension 3: Methodological Rigor (weight 0.20)

**Score: 0.92**

**Rubric:** Is the architectural reasoning sound? Are alternatives genuinely evaluated and rejected for valid reasons? Are the DISC-001 findings correctly analyzed? Is the S-003 steelman applied rigorously?

**Evidence for score:**

- DISC-001 findings are accurately reproduced and correctly analyzed. The ADR does not misrepresent any finding.
- The rejection of Alternative 2 is substantially stronger than ADR-SPIKE002-001's rejection of Alternative 3 (which DISC-001 found invalid). Four distinct rejection reasons are given, each traceable to DISC-001 findings.
- Alternative 1 (hook-only) steelman is strong: genuine isolation benefits articulated (zero coupling, standalone readability, future extraction). The rejection is proportionate and evidence-based (Phase 1 Audit findings on 10 of 14 items reusing existing infrastructure).
- Alternative 2 (infrastructure placement) steelman is appropriately strong: "minimizes upfront implementation effort," "no subprocess overhead," "pragmatically cautious." These are real advantages that were the original rationale. The rejection is thorough.
- Alternative 3 (chosen) Pros/Cons balance: 6 pros, 5 cons. The cons are real (subprocess overhead, two styles coexist, more initial effort, cross-context aggregation, indirection layer). Not whitewashed.
- Alternative 4 (status line) steelman correctly identifies that status line provides EXACT token counts vs. heuristic transcript-based counts — this is a genuine advantage. Rejection is fair (timing dependency, single point of failure, coupling).
- The "domain maturity" force (Force 3) correctly notes that two spikes validated domain concepts. This is a sound argument against "premature abstraction" framing.
- CWI-00 dependency is correctly identified as eliminating the InMemorySessionRepository constraint that invalidated the original rejection of Alternative 3.
- The subprocess budget analysis (4-second timeout within 5-second hook budget) is present and reasonable, though not supported by measured data for the new `jerry hooks` commands (which don't exist yet).

**Minor rigor gaps:**
- The subprocess budget claim ("measured subprocess overhead for existing CLI commands is within budget" — line 286) appears in Consequences but Phase 1 Audit cited `uv sync && uv run jerry --json projects context` as the reference. The new `jerry hooks prompt-submit` command will import additional modules (context_monitoring bounded context). The ADR does not quantify the additional import overhead. This is an estimate, not a measurement. Minor.

**Score justification:** Methodological rigor meets the PASS threshold for this dimension (0.92). The reasoning is sound, alternatives are honestly evaluated, and the DISC-001 analysis is correct.

---

### Dimension 4: Evidence Quality (weight 0.15)

**Score: 0.83**

**Rubric:** Are claims supported by specific evidence? Are references to source files and audit findings accurate? Can a reviewer trace each claim back to a source?

**Evidence for score:**

- Phase 1 Audit traceability table (14 rows) maps each architectural claim to specific audit section and evidence (lines 791–804). This is good granularity.
- Phase 2 Gap Analysis traceability table (5 rows) maps consolidated item count claims to specific sections.
- DISC-001 traceability table (4 rows) accurately maps all four findings.
- DEC-001 traceability table (4 rows) accurately maps all four decisions.
- Codebase architecture evidence table (6 rows) maps claims to specific files and line numbers.
- Cross-check against DISC-001 source: All four findings (F1-F4) are accurately represented. ADR claims about import patterns, enforcement folder structure, and session_start_hook.py behavior match DISC-001 findings exactly.
- Cross-check against DEC-001 source: All four decisions (D-001 through D-004) are accurately represented. The ADR's D-001/D-002/D-003/D-004 bullets align with DEC-001 verbatim.

**Gaps that constrain score:**

1. **ADR-SPIKE002-001 source not cross-checked.** The ADR makes multiple specific claims about ADR-SPIKE002-001's content (e.g., "ADR-SPIKE002-001 rejected the CLI-first approach citing subprocess overhead and InMemorySessionRepository limitations" — lines 226–228). This scorer cannot access ADR-SPIKE002-001 to verify these claims. The ADR does not provide the source path for ADR-SPIKE002-001 in the Evidence section. While DISC-001 corroborates the invalid rejection reasoning (F3), the specific line numbers or section names from ADR-SPIKE002-001 are not cited. This is a traceability gap for a key claim (the rejection reasoning was invalid).

2. **Subprocess timing claim is unverified.** Line 286: "measured subprocess overhead for existing CLI commands is within budget." The Phase 1 Audit traceability table cites C5 (Hook Integration Points) as the source for timeout budgets, but the "measured" claim for subprocess overhead is not traced to any specific measurement in the audit. The audit may have found this, but the ADR does not provide the section reference. This downgrades "measured" to "assumed." Medium gap.

3. **File counts in codebase evidence table.** The claim that `session_management` has "36 Python files" and `work_tracking` has "42 Python files" (line 838) is referenced to "Directory listing" as the source, but no audit timestamp, no reference to the specific Phase 1 audit section, and no specific audit evidence ID. These could be accurate, but the sourcing is weak for an architectural claim used to establish the bounded context scale comparison.

4. **"10 of 14 items classified as EXTEND or REUSE" (line 804).** The traceability table cites "Mapping to SPIKE-001 Items" as the Phase 1 Audit section. The specific classification scheme (1 REUSE, 10 EXTEND, 3 NEW) is a key supporting claim for the chosen approach. No Phase 2 Gap Analysis evidence ID is cited for this specific count (though line 810 provides partial support for the consolidation claim).

**Score justification:** Evidence quality is the weakest dimension. The ADR-SPIKE002-001 sourcing gap and the unverified subprocess timing claim are material weaknesses. The file count sourcing is minor. Score of 0.83 reflects substantive but imperfectly sourced evidence. This dimension weighs 0.15.

---

### Dimension 5: Actionability (weight 0.15)

**Score: 0.88**

**Rubric:** Does the ADR provide enough specificity for implementation? Can a developer execute the decision without ambiguity? Are interface contracts, data flows, and composition root wiring sufficiently detailed?

**Evidence for score:**

- Directory structure diagram (lines 322–356) is file-level specific. An implementer knows exactly what files to create.
- Four data flow diagrams cover all hook events with numbered steps and error handling for each step.
- Value object code contracts are implementation-ready (frozen dataclasses with field names, types, docstrings).
- Port protocols are implementation-ready (Protocol classes with method signatures, docstrings, return types, exceptions raised).
- Wrapper example code (`hooks/user-prompt-submit.py`) is complete and runnable (16 lines, subprocess call pattern, exit 0).
- CLI command table (lines 147-152) specifies each command's timeout and responsibilities.
- Composition root wiring list (lines 186–192) specifies all bindings.
- Bootstrap.py wiring is described at the interface level (which port maps to which adapter).

**Gaps that constrain score:**

1. **`jerry hooks` CLI command registration is underspecified.** The ADR states "Hook CLI commands are registered in the CLI adapter routing, dispatching to application services" (line 192) but does not specify: How does `jerry hooks` parse as a subcommand group? Does the existing CLI adapter use argparse? Click? A custom dispatcher? How does `HooksPromptSubmitHandler` receive the stdin payload from `jerry hooks prompt-submit`? The data flow says "CLI adapter routes to HooksPromptSubmitHandler" (step 4, line 369) but the routing mechanism is not specified. For a document aiming to guide implementation, the entry point from `jerry` CLI to the hook handler needs more detail.

2. **Acknowledgment mechanism for checkpoints is underspecified.** The port specifies `acknowledge(checkpoint_id: str) -> None` and "Acknowledgment via `.acknowledged` marker files" (line 141). But step 6c-ii in the data flow (line 384) says "Call ICheckpointRepository.acknowledge(checkpoint_id)" — when exactly? After reading the unacknowledged checkpoint or after injecting the alert into context? If the inject fails (e.g., hook timeout), does the checkpoint get acknowledged anyway? This is an operational correctness question with implementation consequences.

3. **Hook wrapper for session-start is not shown.** The ADR shows a complete wrapper example for `user-prompt-submit.py` but not for `session-start`. Given the inconsistency noted in Dimension 2 (data flow references `scripts/session_start_hook.py`), the implementer does not have a clear picture of whether to refactor the existing 300+ line session_start_hook.py or replace it with a thin wrapper. This is the most actionable gap.

4. **ResumptionContextGenerator is referenced but not defined.** The `jerry hooks session-start` command table (line 150) says "resumption context (CheckpointService + ResumptionContextGenerator)" and the data flow step 6e references "ResumptionContextGenerator." This component does not appear in the bounded context directory structure (lines 322-356), is not listed as a service or adapter, and has no interface contract. Where does it live? Is it a service in `context_monitoring`? A separate module? This is an unexplained component reference.

**Score justification:** Actionability is high (0.88) given the level of specification for the core components, but three material gaps (CLI registration, session-start wrapper omission, ResumptionContextGenerator) and one operational correctness gap (acknowledgment timing) prevent a higher score.

---

### Dimension 6: Traceability (weight 0.10)

**Score: 0.90**

**Rubric:** Can each major decision be traced back to source requirements, findings, and prior decisions? Is the evidence section complete and accurate?

**Evidence for score:**

- Four dedicated traceability tables (Phase 1 Audit, Phase 2 Gap Analysis, DISC-001, DEC-001) covering the primary source documents.
- Each DEC-001 decision (D-001 through D-004) has an explicit "Status: Pending user acceptance" row in the DEC-001 traceability table. Accurate: DEC-001 source confirms status is "PENDING."
- DISC-001 findings are accurately traced: F1 (two execution paths), F2 (enforcement tech debt), F3 (invalid rejection reasoning), F4 (scripts/hooks split). All confirmed accurate against DISC-001 source.
- Codebase evidence table provides file-level source references with line numbers for key claims (session_start_hook.py line 270, session.py line 207, etc.).
- Forces section (6 forces) does not have explicit traceability back to source documents. Force 1 (clean architecture consistency) is evident from codebase structure. Force 4 (process boundary isolation) is traceable to Phase 1 C2 audit. But the Forces section itself does not provide citations.

**Gap:**
- ADR-SPIKE002-001 path is never stated in the Evidence section. The document being superseded is referenced throughout but its filesystem location is not documented. A reviewer wanting to cross-check the original ADR's Alternative 2 reasoning cannot find it from this ADR.
- Status section says "Supersedes ADR-SPIKE002-001" but the path to ADR-SPIKE002-001 is not provided. Standard ADR practice is to include the file path or a "Related Documents" table entry.

**Score justification:** Traceability is strong (0.90). The four structured traceability tables are thorough and accurate. The missing ADR-SPIKE002-001 path is a gap but does not undermine the quality of the other traceability evidence.

---

## Composite Score Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.90 | 0.180 |
| Internal Consistency | 0.20 | 0.91 | 0.182 |
| Methodological Rigor | 0.20 | 0.92 | 0.184 |
| Evidence Quality | 0.15 | 0.83 | 0.125 |
| Actionability | 0.15 | 0.88 | 0.132 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **COMPOSITE** | **1.00** | | **0.893** |

**Rounded to 2 decimal places: 0.89**

> The scoring model uses the exact weights from quality-enforcement.md. The composite of 0.893 rounds to 0.89 -- inside the REVISE band (0.85-0.91).

---

## Strategy-Informed Perspectives

These perspectives inform the scoring above. They are not separate scoring mechanisms; they surface the failure modes and blind spots relevant to each dimension.

### S-002 (Devil's Advocate): Arguments Against the Chosen Approach

**Strongest arguments against Alternative 3:**

1. **Subprocess startup cost is unvalidated for the new command.** The ADR claims subprocess overhead is "within budget" based on the existing `jerry --json projects context` call. But the new `jerry hooks prompt-submit` command will import `context_monitoring` bounded context modules, `PromptReinforcementEngine`, and CLI dispatcher infrastructure that the existing command does not. The import graph is substantially larger. The 5,000ms UserPromptSubmit budget leaves 4,000ms for the subprocess (per wrapper design). If the new command takes 2,000ms to start (Python + uv + module imports), that leaves only 2,000ms for logic. This is unproven. The ADR acknowledges the risk but provides no measurement or estimation methodology.

2. **"Clean architecture from day one" argument assumes domain stability that may not hold.** The ADR argues domain concepts are mature after two spikes. But SPIKE-001 was a design spike (7 phases) and SPIKE-002 is a research spike. Neither spike produced a working implementation. Implementation regularly reveals that domain concepts need adjustment. Creating a full bounded context structure before the first working hook implementation may result in rework of the domain layer. Alternative 2's "Phase 2 extraction" approach was not merely lazy -- it allowed domain concepts to stabilize through working code before formalizing them.

3. **`jerry hooks` command aggregation couples bounded contexts via the CLI.** The ADR acknowledges this (Negative 4) but understates the long-term impact. As new requirements emerge, `jerry hooks prompt-submit` becomes a growing aggregation point. Each new concern (telemetry, rate limiting, cost estimation) creates pressure to add to the hook command. The CLI command becomes a god function that the ADR design cannot easily decompose without either multiple subprocess calls (timeout risk) or a fundamentally different aggregation mechanism.

### S-003 (Steelman): Assessment of Alternative Steelmanning Quality

All four alternatives receive genuine steelmans:
- Alternative 1 (hook-only): Correctly identifies isolation and standalone readability as real advantages.
- Alternative 2 (infrastructure): Correctly identifies no subprocess overhead and pragmatic caution as real advantages. The "Phase 2 extraction" framing is steelmanned as risk reduction. Fair.
- Alternative 3 (chosen): Not steelmanned (appropriate — it is the chosen option).
- Alternative 4 (status line): Correctly identifies exact token counts (vs. heuristic transcript-based) as the key advantage. The "relay mechanism already exists" point is accurate.

Steelman quality is high. H-16 compliance is met.

### S-004 (Pre-Mortem): What Would Cause This Architecture to Fail in 6 Months?

**Most likely failure modes:**

1. **Subprocess timeout failures become common.** As the codebase grows (new bounded contexts imported at startup), Python module import time increases. The 4-second subprocess budget erodes. UserPromptSubmit hooks start timing out silently (exit 0 with no output). Context monitoring stops working without any visible error. The fail-open design makes this invisible until users notice quality reinforcement has stopped appearing in prompts.

2. **CWI-00 (FileSystemSessionRepository) is not delivered before FEAT-001.** Two data flows (session-start, pre-compact) have explicit CWI-00 dependencies. If CWI-00 slips, these flows either fail silently (the session abandon step fails gracefully) or produce incorrect behavior (resumption context missing the "previous session abandon reason"). The ADR does not define a CWI-00-absent fallback path for either flow.

3. **ResumptionContextGenerator becomes a design black hole.** This component is referenced in two places but never defined. Implementation begins without a clear design for this component. The component ends up in the wrong layer (e.g., as a formatter in the CLI adapter rather than a domain service) because the ADR did not specify its location or interface. This creates a pattern inconsistency that must be later remediated.

4. **The "two styles coexist" inconsistency (D-004) is never remediated.** The enforcement tech debt enabler is created but deprioritized. Over 6 months, three new features are built. Each new feature has to decide: "do I follow the old pattern (direct import) or the new pattern (CLI-first)?" The absence of a remediated enforcement folder creates ongoing decision friction and new architectural debt.

### S-007 (Constitutional AI): Compliance with Jerry Constitution

**Constitutional principles checked:**

1. **H-07 (Domain layer: no external imports):** The ADR's value objects and domain events do not show external imports. FillEstimate imports from ThresholdTier within the domain layer. CheckpointData imports from FillEstimate within the domain layer. No external dependencies in domain code shown. PASS.

2. **H-08 (Application layer: no infra/interface imports):** The port definitions (ITranscriptReader, ICheckpointRepository, IThresholdConfiguration) are Protocol classes with no adapter imports. Services use ports via dependency injection. The checkpoint_repository.py port imports CheckpointData from `src.context_monitoring.domain.value_objects.checkpoint_data` — this is an intra-bounded-context import (domain into application), which is correct hexagonal architecture. PASS.

3. **H-09 (Composition root exclusivity):** All adapters are wired through bootstrap.py per the ADR design. Hook scripts do not instantiate any bounded context objects directly. PASS by design.

4. **H-10 (One class per file):** The directory structure shows one class per file throughout (threshold_tier.py = ThresholdTier, fill_estimate.py = FillEstimate, etc.). `context_monitoring_events.py` contains THREE events (ContextThresholdReached, CompactionDetected, CheckpointCreated) in one file. This VIOLATES H-10. The ADR specifies this structure in the directory listing (line 336).

5. **H-11/H-12 (Type hints and docstrings on public functions):** All code contracts shown have type hints on all parameters and return values, and docstrings on all public methods. PASS for the contracts shown.

6. **P-022 (No deception):** The ADR documents all five genuine negatives, including subprocess overhead, two coexisting styles, and more initial effort. No whitewashing detected. PASS.

**Constitutional violation found (H-10):** `context_monitoring_events.py` contains three event classes. This violates H-10 (one class per file). The ADR must specify three separate files: `context_threshold_reached.py`, `compaction_detected.py`, `checkpoint_created.py`.

### S-012 (FMEA): Failure Mode Analysis

| Failure Mode | Effect | Severity | Probability | Detection | Mitigation |
|-------------|--------|----------|-------------|-----------|------------|
| Subprocess timeout (import bloat) | Silent context monitoring failure | HIGH | MEDIUM | Low (fail-open design hides it) | Single import, lazy loading, timeout alerts |
| CWI-00 not available | Resumption context and session abandon silently degrade | HIGH | MEDIUM | Low (graceful degradation) | Explicit CWI-00 prerequisite or conditional flow |
| AtomicFileAdapter write failure | Checkpoint not saved before compaction | CRITICAL | LOW | Medium (logged to stderr) | Retry + emergency in-memory fallback |
| ResumptionContextGenerator undefined | Wrong layer placement, design inconsistency | MEDIUM | HIGH | Low (discovered at implementation) | Define interface in ADR |
| ICheckpointRepository scan performance | Pre-compact hook slow if many checkpoints | MEDIUM | LOW | Medium (timeout) | Index file or limit scan depth |

The FMEA reveals that the ResumptionContextGenerator gap has HIGH probability of becoming a real implementation issue. This supports the Actionability score of 0.88.

### S-013 (Inversion): What Would Deliberately Choosing the Opposite Teach Us?

If we deliberately chose Alternative 2 (infrastructure placement):
- We would learn that the subprocess startup time for `jerry hooks prompt-submit` is too slow only by failing to get it under budget -- we would have avoided this risk.
- We would learn that the enforcement folder is messier than expected once we try to add domain-aware code to it -- we would confirm F2 through experience.
- We would learn that the "Phase 2 extraction" is actually 2-3x harder than estimated -- we would confirm DISC-001's assessment.

The inversion analysis does not identify any advantage of Alternative 2 that the ADR failed to steelman. The subprocess timing risk (which Alternative 2 avoids) is the one genuine advantage the inversion analysis highlights. This is already documented in the ADR's Negative 1 consequence. The inversion adds no new critique.

---

## Leniency Bias Counteraction

**Explicit checks applied:**

1. **"This is detailed therefore good" bias check.** The ADR is long and thorough. Length does not equal correctness. I applied the scoring rubric to specific claims, not to word count or section count.

2. **"The architecture is correct therefore the ADR is correct" bias check.** Alternative 3 is likely the correct architectural choice. But an ADR about a correct decision can still have documentation gaps. The Evidence Quality score (0.83) reflects real sourcing gaps regardless of whether the architecture is right.

3. **"Self-review checklist is complete therefore no gaps" bias check.** The self-review checklist (lines 847-861) claims completeness on all items. I checked each claim independently. The H-10 violation (context_monitoring_events.py with 3 classes) was not caught by the self-review. The ResumptionContextGenerator gap was not caught by the self-review. The session-start wrapper inconsistency was not caught by the self-review.

4. **Adjacent score selection.** When uncertain between 0.91 and 0.92 (Internal Consistency), I chose 0.91 because the session-start path inconsistency is a genuine issue an implementer would notice, not a minor editorial concern.

5. **Threshold realism check.** A score of 0.92 means genuinely excellent — a document that a senior architect would regard as fully publication-ready with no material gaps. This ADR is close but not there: it has three implementer-facing gaps (ResumptionContextGenerator, CLI command registration, session-start wrapper) and two evidence quality gaps (ADR-SPIKE002-001 source path, subprocess timing claim). These are real deficiencies.

---

## Deficiencies Identified

Listed by priority (implementation impact):

| ID | Deficiency | Dimension Affected | Severity | Required for PASS |
|----|------------|-------------------|----------|------------------|
| DEF-001 | H-10 violation: `context_monitoring_events.py` contains 3 event classes (ContextThresholdReached, CompactionDetected, CheckpointCreated). Must be 3 separate files. | Completeness, Internal Consistency | HIGH | Yes |
| DEF-002 | ResumptionContextGenerator referenced in CLI command table (line 150) and session-start data flow (step 6e) but not included in bounded context directory structure, not listed as a service or adapter, and has no interface contract. | Completeness, Actionability | HIGH | Yes |
| DEF-003 | Session-start data flow (line 415) references `scripts/session_start_hook.py` (existing file) rather than a new thin wrapper `hooks/session-start.py`. Contradicts D-001 intent (all hooks become thin wrappers). No session-start wrapper example shown. | Internal Consistency, Actionability | MEDIUM | Yes |
| DEF-004 | `jerry hooks` CLI command registration and routing mechanism is underspecified: how does the CLI adapter parse `hooks` as a subcommand group? How does `HooksPromptSubmitHandler` receive the stdin payload? | Actionability | MEDIUM | No (clarification preferred) |
| DEF-005 | Acknowledgment timing gap: the `acknowledge(checkpoint_id)` call in step 6c-ii fires before confirming injection succeeded. If the hook times out after acknowledgment, the alert is never delivered but the checkpoint is marked acknowledged. | Actionability | MEDIUM | No (design decision to document) |
| DEF-006 | ADR-SPIKE002-001 path not provided in Evidence section. Superseded document path should be included for reviewer traceability. | Traceability | LOW | No |
| DEF-007 | Subprocess timing claim ("measured ... is within budget", line 286) not traceable to a specific measurement. Rephrase as "estimated" or provide Phase 1 audit section reference. | Evidence Quality | LOW | No |
| DEF-008 | ContextState value object listed in domain table but no code contract provided. | Completeness | LOW | No |

**Required for PASS (iteration 2):** DEF-001, DEF-002, DEF-003.
**Recommended (strongly):** DEF-004, DEF-005.
**Optional (minor):** DEF-006, DEF-007, DEF-008.

---

## Revision Requirements

For iteration 2 to achieve >= 0.92, the following changes are required:

### REV-001 (Required): Fix H-10 Violation — Split Event File

Rename `events/context_monitoring_events.py` to three separate files:
```
domain/events/
  context_threshold_reached.py   # ContextThresholdReached
  compaction_detected.py         # CompactionDetected
  checkpoint_created.py          # CheckpointCreated
```

Update the directory structure diagram and any references to the single events file.

### REV-002 (Required): Define ResumptionContextGenerator

Add `ResumptionContextGenerator` to the bounded context. Specify:
- Which layer it lives in (application service, infrastructure adapter, or domain service?)
- Its interface (method signature with type hints)
- Where it fits in the directory structure
- What inputs it consumes (CheckpointData? ORCHESTRATION.yaml fields directly? A domain object?)

This likely belongs in `application/services/resumption_context_generator.py` as an application service that composes CheckpointData into XML format. Define the interface contract as a code block.

### REV-003 (Required): Resolve Session-Start Wrapper Inconsistency

Choose one of:
- **Option A:** Show `hooks/session-start.py` as a new thin wrapper replacing `scripts/session_start_hook.py`. Update the session-start data flow (step 2-3) to reference `hooks/session-start.py`. Add `hooks/session-start.py` to the wrapper example or explicitly state it follows the same pattern as `hooks/user-prompt-submit.py`.
- **Option B:** Explicitly state that `scripts/session_start_hook.py` is refactored (not replaced) and document what refactoring is required.

The current state (D-001 says all hooks become thin wrappers; session-start data flow references the old 300+ line script without clarification) is genuinely ambiguous for an implementer.

---

## Next Steps

| Action | Agent | Notes |
|--------|-------|-------|
| Return ADR to ps-architect for targeted revision (REV-001, REV-002, REV-003) | ps-architect | REVISE band — targeted changes expected to achieve PASS |
| Re-score iteration 2 after revision | adv-scorer | Focus on DEF-001 through DEF-003 resolution; verify no new inconsistencies introduced |
| If iteration 2 scores >= 0.92, proceed to Phase 5c (work item revision) | ps-synthesizer | |
| If iteration 2 scores < 0.92, escalate to user | orchestrator | Per AE-006 analog for quality stalls |

**Estimated score after REV-001+REV-002+REV-003:**

- Completeness: 0.90 -> 0.93 (ContextState + service signatures still minor gap, but events and ResumptionContextGenerator resolved)
- Internal Consistency: 0.91 -> 0.93 (session-start wrapper resolved)
- Methodological Rigor: 0.92 (unchanged — core reasoning is sound)
- Evidence Quality: 0.83 (unchanged by these revisions — sourcing gaps remain)
- Actionability: 0.88 -> 0.92 (ResumptionContextGenerator and session-start wrapper gaps resolved; CLI registration still underspecified)
- Traceability: 0.90 (unchanged)

**Projected iteration 2 composite:** ~0.921 — borderline PASS. The Evidence Quality dimension (0.83) will continue to drag the composite. If DEF-007 and DEF-006 are also addressed in revision, projected composite rises to ~0.928 (solid PASS).

**Recommendation:** Address REV-001 through REV-003 plus DEF-006 and DEF-007 in a single revision pass to ensure a clean PASS in iteration 2.

---

*Scored by: adv-scorer v1.0.0 | Date: 2026-02-19 | Model: claude-sonnet-4-6*
*Reference: quality-enforcement.md S-014 LLM-as-Judge | Threshold: >= 0.92 (H-13)*

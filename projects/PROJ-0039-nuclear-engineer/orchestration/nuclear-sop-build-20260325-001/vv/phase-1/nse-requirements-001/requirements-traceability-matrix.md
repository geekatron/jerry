---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Requirements Traceability Matrix: /nuclear-sop Skill

> **Project:** PROJ-0039-nuclear-engineer
> **Entry:** V&V Phase 1
> **Agent:** nse-requirements-001
> **Date:** 2026-03-31
> **Criticality:** C3
> **Status:** Draft
> **Consuming agents:** nse-verification-001 (V&V Phase 2, QG-V2), nse-reviewer-001 (V&V Phase 3, QG-V3 CDR entrance)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Traceability Matrix](#traceability-matrix) | 22-row table: all nuclear patterns traced to implementation |
| [Transparency Notes](#transparency-notes) | Approximation limitations for each Conceptual Translation pattern |
| [Impossible and Deferred Rationale](#impossible-and-deferred-rationale) | Why C-1 cannot be implemented; why A-1 and A-3b are deferred |
| [Coverage Summary](#coverage-summary) | Counts by category and verification method; gap analysis |
| [Open Items](#open-items) | Pending artifacts and incomplete traces |

---

## Traceability Matrix

### Verification Method Vocabulary

| Code | Method | When Applied |
|------|--------|-------------|
| BEHAVIORAL-SAMPLE | LLM behavioral claims (STAR, stop-work) | Adversarial test scenario with documented output |
| TRACE-INSPECTION | State management claims (PROCEDURE_STATE fields) | Review of YAML execution log |
| METRIC-REFERENCE | Performance claims (catch rate, false positive rate) | Cite PM-01 through PM-07 from QG-E4 |
| STRUCTURAL-ANALYSIS | Structural claims (tool tier, forbidden actions, template sections) | Review agent definition/governance YAML |

### Status Vocabulary

| Status | Definition |
|--------|-----------|
| TRACED | Implementation file identified; trace is complete and verifiable |
| APPROXIMATED | LLM mechanism approximates nuclear original; transparency note required |
| IMPOSSIBLE | Architecturally impossible in LLM sequential-execution context; rationale documented |
| DEFERRED | Implementable but not in Phase 1 scope; rationale and target phase documented |

---

### Direct Translation Patterns (9 patterns)

| Pattern ID | Pattern Name | Category | Gap Finding | Synthesis Spec Section | Implementation File(s) | Verification Method | Test Case ID | Status |
|-----------|-------------|----------|-------------|----------------------|----------------------|-------------------|-------------|--------|
| A-3 | Standard Procedure Structure (11 sections) | Direct Translation | GAP-01 partially (A-3 is core structure; sop-brief validates sections 1-6, sop-executor validates 7-9) | Synthesis §2 Cross-Reference Matrix row A-3; §1.2 Skill File Structure | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (11-section template); `skills/nuclear-sop/agents/sop-brief.md` (section validation, Step 1); `skills/nuclear-sop/agents/sop-executor.md` (section 7-9 enforcement) | STRUCTURAL-ANALYSIS | TC-brief-001, TC-executor-001 | TRACED |
| A-4 | WARNING/CAUTION/NOTE Pre-Placement | Direct Translation | No gap in Jerry (NPT pattern already exists); direct extension to workflow step annotations | Synthesis §2 Cross-Reference Matrix row A-4; §1.6 Procedure Use Classification (CAUTION triggers STAR) | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (inline WARNING/CAUTION/NOTE blocks before steps); `skills/nuclear-sop/agents/sop-executor.md` (WARNING acknowledgment before state change); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-01 — STAR triggered by CAUTION) | STRUCTURAL-ANALYSIS | TC-executor-002, TC-executor-003 | TRACED |
| A-5 | Place-Keeping / Step Sign-Off | Direct Translation | No Jerry gap (worktracker analogy identified); formal step-sign-off as behavioral constraint is new | Synthesis §2 Cross-Reference Matrix row A-5; §1.9 PROCEDURE_STATE.yaml Schema (steps_completed array) | `skills/nuclear-sop/agents/sop-executor.md` (sequential step progression, STAR REVIEW updates state); `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` (steps_completed, current_step, next_step fields); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-10 — per-step update, no batching) | TRACE-INSPECTION | TC-executor-004 | TRACED |
| C-2 | Independent Verification (Sequential, Different Context) | Direct Translation | No direct Jerry analog; FC-M-001 (fresh context via Task) identified as the approximation mechanism. Note: classified Direct Translation by handoff enumeration; treated as APPROXIMATED in fidelity table (ADR R6). See Transparency Note TN-C-2. | Synthesis §2 Cross-Reference Matrix row C-2; §1.8 H-36 Circuit Breaker Compliance (4-hop mode); ADR-001 Fidelity Transparency (R6) | `skills/nuclear-sop/agents/sop-verifier.md` (T1 read-only, fresh context, FC-M-001 contract); `skills/nuclear-sop/agents/sop-verifier.governance.yaml`; `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-04 — IV-HOLD must not auto-pass; fresh sop-verifier required) | STRUCTURAL-ANALYSIS | TC-verifier-001 | APPROXIMATED |
| C-3 | QC Hold Point Inspection | Direct Translation | No Jerry gap (quality gates exist); named blocking hold points with three types are new | Synthesis §2 Cross-Reference Matrix row C-3; §1.7 Hold Point Types (USER-HOLD, QG-HOLD, IV-HOLD) | `skills/nuclear-sop/agents/sop-executor.md` (hold point activation logic, NS-H-02/NS-H-03/NS-H-04); `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` (hold_type, hold_resolution, iv_scope fields); `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` (sign-off record); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (Hold Point Authority Table) | STRUCTURAL-ANALYSIS | TC-executor-005, TC-executor-006, TC-executor-007 | TRACED |
| D-1 | Prerequisite and Initial Condition Verification | Direct Translation | No Jerry gap (H-04 analogy); formal STOP gate on failed prerequisites is new | Synthesis §2 Cross-Reference Matrix row D-1; §1.4 Workflow Execution Sequence (Step 1 mandatory STOP gates) | `skills/nuclear-sop/agents/sop-brief.md` (Step 1 prerequisite verification, STOP on failure per P-020); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-07 — sop-brief Step 1 mandatory; halts on missing definition) | BEHAVIORAL-SAMPLE | TC-brief-002 | TRACED |
| D-2 | Stop-Work Authority | Direct Translation | No Jerry gap (H-31 + circuit breaker analogy); stop-work as explicit STAR REVIEW outcome is new | Synthesis §2 Cross-Reference Matrix row D-2; §1.5 STAR Protocol (REVIEW step triggers stop-work on deviation) | `skills/nuclear-sop/agents/sop-executor.md` (D-2 stop-work authority, deviation logging); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-05 — stop-work mandatory on deviation; no self-correction without user authority); `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` (stop_work_count field) | BEHAVIORAL-SAMPLE | TC-executor-008 | TRACED |
| E-2 | Conservative Decision-Making Under Uncertainty | Direct Translation | No Jerry gap (H-31 + P-020 analogies); explicit "when uncertain, stop-and-ask" as STAR Think directive is new | Synthesis §2 Cross-Reference Matrix row E-2; §1.5 STAR Protocol (THINK phase: "if uncertain, invoke conservative decision-making (E-2 / H-31)") | `skills/nuclear-sop/agents/sop-executor.md` (STAR THINK phase conservative decision directive); `skills/nuclear-sop/agents/sop-brief.md` (Step 1 STOP on unverifiable acceptance criteria); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-05 — conservative default on deviation) | BEHAVIORAL-SAMPLE | TC-executor-009 | TRACED |
| I-1 | Operations Turnover / Shift Handoff | Direct Translation | No Jerry gap — identified as ALREADY IMPLEMENTED via existing handoff schema (Strong fit); validation task only | Synthesis §2 Cross-Reference Matrix row I-1; Pattern Extraction §5 Priority Ranking (Rank 7, Tier 1 validate) | `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` (pause/resume state enabling mid-execution handoff); `skills/nuclear-sop/agents/sop-executor.md` (RESUME execution mode, cross-session state reconstruction from filesystem) | TRACE-INSPECTION | TC-executor-010 | TRACED |

---

### Partial Translation Patterns (4 patterns)

| Pattern ID | Pattern Name | Category | Gap Finding | Synthesis Spec Section | Implementation File(s) | Verification Method | Test Case ID | Status |
|-----------|-------------|----------|-------------|----------------------|----------------------|-------------------|-------------|--------|
| A-2 | Procedure Use Classification (Continuous / Reference / Information) | Partial Translation | GAP-03 — No step-use classification in Jerry workflow definitions | Synthesis §1.6 Procedure Use Classification; §2 Cross-Reference Matrix row A-2 | `skills/nuclear-sop/agents/sop-executor.md` (step annotation enforcement: [CONTINUOUS], [REFERENCE], [INFORMATION]); `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (step annotation convention in step blocks); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-M-01 — default classification by criticality) | STRUCTURAL-ANALYSIS | TC-executor-011, TC-executor-012 | TRACED |
| E-1 | Decision Authority Hierarchy | Partial Translation | No Jerry gap per se (AE rules + C1-C4 criticality provide coverage); formal per-step authority annotation is partial translation | Synthesis §2 Cross-Reference Matrix row E-1; Pattern Extraction §5 Tier assignment (Deferred from score=6, then listed as Partial Translation in handoff) | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (Section 1 Metadata `criticality` field; workflow_type implying authority scope); `skills/nuclear-sop/agents/sop-executor.md` (USER-HOLD annotation enforces user authority at specific steps); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-02 — USER-HOLD cannot be inferred from silence) | STRUCTURAL-ANALYSIS | TC-executor-013 | TRACED |
| F-1 | Three-Part Communication Protocol | Partial Translation | No Jerry gap — structured handoff schema already implements the concept; echo-confirmation extension is partial [SOURCE-CONF: 0.91, ACCEPTED-RISK] | Synthesis §2 Cross-Reference Matrix row F-1 (Deferred, handoff schema extension); Pattern Extraction §2 Mapping Table row F-1 | `skills/nuclear-sop/agents/sop-brief.md` (structured handoff output: key_findings echo to orchestrator); `skills/nuclear-sop/agents/sop-capture.md` (session context on_receive field validation); existing `agent-development-standards.md` handoff schema (HD-M-001 through HD-M-005) | STRUCTURAL-ANALYSIS | TC-brief-003 | APPROXIMATED |
| G-1 | Symptom-Based Emergency Decision Framework | Partial Translation | GAP-06 — AE rules partially cover; ABNORMAL/EMERGENCY workflow types are partial translation of full EOP symptom-based framework | Synthesis §2 Cross-Reference Matrix row G-1 (Phase 4); §1.4 Workflow Execution Sequence (workflow_type field in WORKFLOW_DEFINITION template) | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (Section 1 Metadata `workflow_type` field with NOMINAL/ABNORMAL/EMERGENCY enum); existing Jerry AE-001 through AE-006 auto-escalation rules (partial coverage) | STRUCTURAL-ANALYSIS | TC-brief-004 | APPROXIMATED |

---

### Conceptual Translation Patterns (6 patterns)

| Pattern ID | Pattern Name | Category | Gap Finding | Synthesis Spec Section | Implementation File(s) | Verification Method | Test Case ID | Status |
|-----------|-------------|----------|-------------|----------------------|----------------------|-------------------|-------------|--------|
| B-1 | STAR Self-Checking (Stop-Think-Act-Review) | Conceptual Translation | GAP (new behavioral primitive) — No Jerry analog; S-010 (Self-Refine) operates post-completion, not pre-action | Synthesis §1.5 STAR Self-Checking Protocol; §1.5a STAR Behavioral Validation Plan (error trap acceptance test) | `skills/nuclear-sop/agents/sop-executor.md` (STAR pre-action protocol before every Write/Edit/Bash call); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-01 — STAR mandatory before state-modifying calls); `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` (STAR validation fixture — PENDING ENG Phase 4) | BEHAVIORAL-SAMPLE | TC-executor-014, TC-executor-015 (A/B validation) | APPROXIMATED |
| B-2 | Questioning Attitude | Conceptual Translation | GAP-07 — H-31 + P-022 provide partial conceptual coverage; dispositional behavioral property, not a discrete step | Synthesis §2 Cross-Reference Matrix row B-2 (Deferred, embed in STAR Think prompt); Pattern Extraction §3 Conceptual Translation Group 3 | `skills/nuclear-sop/agents/sop-executor.md` (STAR THINK phase: "What could go wrong?" explicit challenge-assumptions directive); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-05 — halt on deviation, no self-correction) | BEHAVIORAL-SAMPLE | TC-executor-016 | APPROXIMATED |
| F-2a | Pre-Job Briefing | Conceptual Translation | GAP-01 — Highest-value gap: no formalized pre-execution phase in Jerry workflows | Synthesis §1.4 Workflow Execution Sequence (Step 1 mandatory); §2 Cross-Reference Matrix row F-2a; §1.11 OE Entry Schema | `skills/nuclear-sop/agents/sop-brief.md` (full pre-job brief agent: context load, OE review, error trap identification, scope confirmation); `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md` (brief output structure with mandatory OE section); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-07 — sop-brief mandatory, no bypass path) | BEHAVIORAL-SAMPLE | TC-brief-005 | APPROXIMATED |
| F-2b | Post-Job Briefing and OE Capture | Conceptual Translation | GAP-02 — Second highest-value gap: docs/experience/ exists but no structured OE capture in workflow execution | Synthesis §1.4 Workflow Execution Sequence (Step 4 mandatory); §1.11 OE Entry Schema; §2 Cross-Reference Matrix row F-2b | `skills/nuclear-sop/agents/sop-capture.md` (post-job OE capture, mandatory schema enforcement); `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` (OE capture output structure); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-06 — write blocked if mandatory field missing) | TRACE-INSPECTION | TC-capture-001 | APPROXIMATED |
| H-1 | Corrective Action Program (CAP) | Conceptual Translation | GAP-04 (partial) — Worktracker captures issues; no formal OE feedback loop to workflow revision | Synthesis §1.11 OE Entry Schema (deviation_type, root_cause, recommendation mandatory fields); §2 Cross-Reference Matrix row H-1 (Phase 1 basic, Phase 3 full loop) | `skills/nuclear-sop/agents/sop-capture.md` (deviation classification, root cause documentation, improvement recommendations); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-06 — deviation_type and root_cause required; NS-M-06 — synthesis section at >5 OE entries) | TRACE-INSPECTION | TC-capture-002 | APPROXIMATED |
| H-2 | Operating Experience (OE) Review | Conceptual Translation | GAP-01 (sub-component) — OE review is a component of GAP-01; docs/experience/ exists but not searched as mandatory pre-execution step | Synthesis §1.4 Workflow Execution Sequence (Step 1 sop-brief OE search mandatory); §1.11 OE Entry Schema (entry_id enables exact-match search); §2 Cross-Reference Matrix row H-2 | `skills/nuclear-sop/agents/sop-brief.md` (Step 4: mandatory OE search by workflow_id, then workflow_type, then keyword; OE entries as MANDATORY CONTEXT not optional); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (OE Accumulation Enforcement section: WARNING >10, STOP >20 unanalyzed entries) | TRACE-INSPECTION | TC-brief-006 | APPROXIMATED |

---

### Impossible and Deferred Patterns (3 patterns)

| Pattern ID | Pattern Name | Category | Gap Finding | Synthesis Spec Section | Implementation File(s) | Verification Method | Test Case ID | Status |
|-----------|-------------|----------|-------------|----------------------|----------------------|-------------------|-------------|--------|
| C-1 | Peer Checking (Concurrent, Same Context) | Impossible | GAP-05 — Architecturally impossible: requires two agents executing in parallel with shared real-time state awareness | Synthesis §2 Cross-Reference Matrix row C-1 (Accept as limitation); Pattern Extraction §4.3 Impossible gaps; §3 Group 1 note (P-003 prohibits concurrent agents) | None — no implementation. Compensating control: sop-verifier provides sequential context-isolated verification. | N/A | None | IMPOSSIBLE |
| A-1 | Procedure Type Hierarchy (OPs/AOPs/EOPs/ARPs) | Deferred | No direct Jerry gap; `workflow_type` (NOMINAL/ABNORMAL/EMERGENCY) implements a subset; full OPs/AOPs/EOPs/ARPs taxonomy is Phase 2 | Synthesis §2 Cross-Reference Matrix row A-1 (Phase 2); Pattern Extraction §5 Defer row (score=6, analyst override: "defer until T2 patterns complete") | Partial: `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (Section 1 `workflow_type` field with NOMINAL/ABNORMAL/EMERGENCY — partial coverage only) | STRUCTURAL-ANALYSIS | None (Phase 2 scope) | DEFERRED |
| A-3b | Standard Procedure Structure — Section Ordering Enforcement | Deferred | Sub-pattern of A-3; 11-section template covers structure definition; strict section ordering enforcement (auto-rejection of out-of-order sections) requires behavioral validation harness not in Phase 1 | Synthesis §2 Cross-Reference Matrix (A-3 covers full structure; A-3b not listed as separate row — ordering enforcement is a sop-brief validation behavior, Phase 1 targets basic completeness only); Pattern Extraction §5 Tier structure | `skills/nuclear-sop/agents/sop-brief.md` (section completeness validation during Step 1; ordering enforcement is MEDIUM standard, not HARD rule in Phase 1); `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-M-01 aligns to ordering intent) | STRUCTURAL-ANALYSIS | None (deferred to behavioral baseline work) | DEFERRED |

---

## Transparency Notes

This section documents how each Conceptual Translation and Approximated pattern differs from its nuclear original and what limitations exist in the LLM implementation.

### TN-C-2: Independent Verification (sop-verifier)

**Nuclear original:** A qualified individual NOT involved in the work verifies the completed action after execution, before system restoration. Documented with physical signature. Mandated by Appendix B Criterion X: "Inspection shall be performed by individuals other than those who performed the activity being inspected."

**LLM implementation:** sop-verifier is invoked via the Task tool, which creates a fresh context window. The Task prompt is restricted to: (1) workflow definition path, (2) work product file paths from PROCEDURE_STATE.yaml iv_scope, (3) acceptance criteria section. The executor's reasoning chain, STAR records, pre-job brief, and quality gate history are explicitly excluded.

**What is preserved:** Context isolation (no exposure to executor reasoning). Sequential execution (verifier operates after executor completes). Explicit disposition (ACCEPT / REJECT / ACCEPT-WITH-CONDITIONS). Formal scope constraint (iv_scope limits what the verifier evaluates).

**What is NOT preserved:** Personnel independence. The verifier is the same LLM model as the executor. LLM context isolation is not equivalent to a separate qualified human reviewer. The same underlying model that trained on the same data performs both execution and verification. Nuclear Criterion X requires different persons, not different context windows.

**Limitation:** The verifier may share underlying reasoning patterns with the executor even with context isolation. For C3+ workflows, this limitation is acknowledged and documented in sop-verifier.md (P-022 transparency). It is accepted as the best available approximation given LLM architecture constraints.

**Source:** ADR-001 QG3 Finding R6; sop-verifier.md Anchoring Bias Disclaimer; Synthesis spec §6.2 (fidelity transparency).

---

### TN-B-1: STAR Self-Checking

**Nuclear original:** STAR (Stop-Think-Act-Review) is a physical interruption: the operator stops, eliminates distractions, verifies preconditions against physical plant state, executes the action, and reviews the actual outcome against expected outcome. The "Stop" phase is a temporal gap between decision and action.

**LLM implementation:** STAR reasoning and the tool call are generated in the same inference pass. The temporal separation is a structural constraint in the prompt (the agent is required to produce S-T-A-R text before issuing the tool call), not a physical interruption. The value is structural (forced deliberate pause and self-challenge) rather than temporal (actual delay between intention and execution).

**What is preserved:** The four-step cognitive sequence (Stop/Think/Act/Review). The challenge-assumptions orientation in THINK. The deviation-triggered stop-work in REVIEW. The logging of STAR records to the execution log for audit.

**What is NOT preserved:** Physical interruption (no actual pause between LLM reasoning and tool call execution). Elimination of distractions (an LLM has no capacity to focus attention the way a human can stop and refocus). Genuine pre-action constraint on hardware operations (nuclear STAR prevents physical valve operation; LLM STAR constrains only within the same inference pass).

**Limitation and validation requirement:** STAR reasoning may be generated post-hoc (the model produces plausible S-T-A-R text while the tool call was already determined). This failure mode (identified as R-011, RPN 294 in synthesis spec) is undetectable without deliberate testing. The STAR A/B validation gate (Phase 1 acceptance criteria) is required before the skill can advance to Phase 2 or be used at C3+.

**Source:** Synthesis spec §1.5 (STAR vs. S-010 distinction table); §1.5a (STAR Behavioral Validation Plan); sop-executor.md (STAR transparency section, P-022); SKILL.md (STAR Validation Pre-Ship Gate).

---

### TN-B-2: Questioning Attitude

**Nuclear original:** A safety culture trait: workers continuously challenge existing conditions, avoid complacency, and escalate observed discrepancies. It is a dispositional property embedded through years of safety culture reinforcement, not a discrete procedural step.

**LLM implementation:** The STAR THINK phase includes an explicit "What could go wrong?" prompt directive. NS-H-05 (stop-work on deviation, no self-correction without user authority) implements the behavioral consequence of questioning attitude. H-31 (clarify when ambiguous) provides the escalation mechanism.

**What is preserved:** The behavioral outcome of questioning attitude (halt and escalate rather than assume correctness). The anti-complacency orientation embedded in STAR THINK. The escalation path (H-31 + USER-HOLD).

**What is NOT preserved:** The dispositional property itself. Nuclear questioning attitude is internalized through culture, training, and peer reinforcement across careers. An LLM agent does not accumulate that kind of dispositional history. Whether prompt-level "challenge assumptions" language produces equivalent behavior to a trained human operator's questioning attitude is empirically uncertain.

**Source:** Pattern Extraction §3 Conceptual Translation (B-2 feasibility note: "High (prompt) / Uncertain (behavioral effect)"); Synthesis spec §2 Cross-Reference Matrix row B-2; Pattern Extraction GAP-07.

---

### TN-F-2a: Pre-Job Briefing

**Nuclear original:** A mandatory face-to-face team ritual before work begins: the team discusses scope, sequence, risks, error traps, prior operating experience, and which human performance tools to apply. The briefing is interactive — a discussion, not a report-read.

**LLM implementation:** sop-brief generates a structured brief artifact (PRE_JOB_BRIEF.template.md) and presents it to the user. The OE findings, error traps, and prerequisite status are artifacts rather than interactive discussion. The briefing is one-way (agent to user) rather than two-way (team discussion).

**What is preserved:** The temporal discipline (brief always occurs before execution). The OE integration (prior executions' lessons are mandatory context). The prerequisite gate (halts if prerequisites are not met). The error trap identification from WARNING/CAUTION annotations. The scope confirmation before any state-modifying tool call.

**What is NOT preserved:** Team participation. The interactive discussion that allows participants to raise concerns, ask questions, and achieve shared understanding. The social accountability mechanism (everyone on the team heard the brief and can be held accountable for it).

**Source:** Pattern Extraction §1 F-2a definition; Synthesis spec §1.4 Step 1 sequence; sop-brief.md purpose section.

---

### TN-F-2b: Post-Job Briefing / OE Capture

**Nuclear original:** A mandatory face-to-face team debrief after work ends. The team discusses what happened, what deviated from plan, what surprised them, and what they would do differently. The debrief is interactive and produces institutional knowledge through group reflection.

**LLM implementation:** sop-capture reads the FINAL execution log and PROCEDURE_STATE.yaml, compares execution to the planned procedure, documents deviations using a mandatory schema, and writes a structured OE entry to docs/experience/. The OE entry is machine-readable and schema-validated, enabling future sop-brief to retrieve and present it as mandatory context.

**What is preserved:** The temporal discipline (OE capture always occurs after execution). The schema enforcement (mandatory fields block write; no partial OE entries). The feedback loop (OE entries are searchable by future sop-brief invocations). The deviation classification (NONE/MINOR/MAJOR/STOP-WORK).

**What is NOT preserved:** Team discussion and interactive reflection. The OE entry is generated from artifacts, not from participant recall and discussion. Human insights about what "felt wrong" during execution, near-misses that were not recorded in the execution log, and contextual knowledge that participants hold but did not write down are not captured.

**Source:** Pattern Extraction §1 F-2b definition; Synthesis spec §1.11 OE Entry Schema; sop-capture.md purpose section; NS-H-06.

---

### TN-H-1: Corrective Action Program (CAP)

**Nuclear original:** Every nuclear plant operates a mandatory CAP that captures all deviations, near-misses, and good practices. Each entry is evaluated, root-caused for significant issues, corrected, and the correction verified. The program feeds back into procedure revision, training updates, and industry-wide OE sharing (INPO, IAEA, NRC generic communications).

**LLM implementation:** sop-capture writes structured OE entries with mandatory deviation_type, root_cause, and recommendation fields. The OE entries accumulate in docs/experience/ and are searchable. The Phase 1 CAP implementation is "basic" — entry capture with mandatory fields. The full feedback loop (CAP-to-workflow-revision cycle via ps-synthesizer) is Phase 3 scope.

**What is preserved:** The documentation mandate (every execution produces an OE entry; no execution can skip sop-capture). The deviation classification taxonomy. The root cause requirement. The searchability via workflow_id and workflow_type fields.

**What is NOT preserved in Phase 1:** The corrective action verification loop (root cause identified -> corrective action defined -> corrective action verified). The industry-wide sharing mechanism. The periodic synthesis-to-workflow-revision cycle (Phase 3). The trend analysis across multiple entries (partial in NS-M-06 synthesis section MEDIUM standard, but full CAP analytics is Phase 3).

**Source:** Pattern Extraction GAP-04; Synthesis spec §2 Cross-Reference Matrix row H-1 (Phase 1 basic, Phase 3 full loop); sop-capture.md purpose section.

---

### TN-H-2: Operating Experience (OE) Review

**Nuclear original:** Before starting work, the team reviews both internal OE (this plant's history with this procedure type) and external OE (industry-wide experience from INPO, IAEA, NRC generic communications). The review is thorough and interactive; participants discuss how prior events relate to the current task.

**LLM implementation:** sop-brief Step 4 searches docs/experience/ by workflow_id (exact match), then workflow_type, then keyword. OE findings are presented in the pre-job brief as MANDATORY CONTEXT (not optional reading). The OE accumulation enforcement (WARNING >10, STOP >20 unanalyzed entries) prevents the OE corpus from becoming too large to be useful.

**What is preserved:** The temporal discipline (OE review always occurs before execution, in sop-brief Step 4). The mandatory context designation (findings must be read, not skipped). The enforcement mechanism (WARNING and STOP thresholds prevent OE corpus overflow).

**What is NOT preserved:** External OE (industry-wide experience from INPO, IAEA, NRC). The implementation reads only from docs/experience/ within the current project. The interactive discussion. The connection to plant-wide event reporting systems.

**Source:** Pattern Extraction GAP-01 (sub-component); Synthesis spec §1.11 (sop-brief OE enforcement); sop-brief.md Step 1 methodology; nuclear-sop-behavior-rules.md OE Accumulation Enforcement section.

---

### TN-F-1: Three-Part Communication Protocol (Partial Translation)

**Nuclear original:** A mandatory three-part communication cycle: (1) Sender states message clearly. (2) Receiver paraphrases/repeats back verbatim (including equipment designators). (3) Sender confirms correct understanding or restates. Required for task assignments, equipment status, parameter values, procedure steps, and equipment operation.

**LLM implementation:** The existing Jerry handoff schema provides structured communication with key_findings (sender's message), confidence (sender's self-assessment), and artifacts (specific object references). The echo-confirmation step (receiver paraphrases key findings back to sender) is not explicitly implemented — the schema includes the fields but does not mandate a confirmation cycle. This is classified as Partial Translation because the schema covers concepts 1 and 2 of the three-part cycle but does not enforce concept 3 (sender confirms receiver's reply).

**What is preserved:** Structured communication with explicit key_findings. Artifact-level specificity (not just summary). Confidence signaling.

**What is NOT preserved:** The repeat-back mandate. The sender-confirmation step. The verbatim equipment designator requirement.

**Note:** This pattern is listed as Deferred in the synthesis spec (handoff schema echo-confirmation extension). It is classified as APPROXIMATED in this matrix because the partial implementation exists in the current handoff schema.

**Source:** Pattern Extraction §2 Mapping Table row F-1; Synthesis spec §2 Cross-Reference Matrix row F-1.

---

### TN-G-1: Symptom-Based Emergency Framework (Partial Translation)

**Nuclear original:** Emergency Operating Procedures (EOPs) are symptom-based rather than event-based. Operators respond to observable plant symptoms (high pressure, low water level, rising temperature) regardless of which specific event caused them, removing the requirement to diagnose the initiating event before acting.

**LLM implementation:** The WORKFLOW_DEFINITION.template.md includes a `workflow_type` field with NOMINAL/ABNORMAL/EMERGENCY enum values. The EMERGENCY type conveys heightened hold point density and conservative defaults. The existing AE-001 through AE-006 auto-escalation rules respond to observable conditions (context fill, governance triggers, H-36 violations) without requiring root cause diagnosis — this is the closest Jerry analog to symptom-based response. Full ABNORMAL/EMERGENCY workflow type activation logic with symptom-based routing to recovery procedures is Phase 4 scope.

**What is preserved in Phase 1:** The concept of workflow types organized by operational context. The EMERGENCY designation in workflow metadata. The AE rules as symptom-based response infrastructure.

**What is NOT preserved in Phase 1:** Defined symptom sets that automatically activate ABNORMAL or EMERGENCY workflow types. Automatic routing from symptoms to recovery procedures. The EOP parallel-procedure tracking capability (BWR EOPs can be in multiple places simultaneously).

**Source:** Pattern Extraction GAP-06; Synthesis spec §2 Cross-Reference Matrix row G-1 (Phase 4); Pattern Extraction §2 Mapping Table row G-1 (Moderate fit).

---

## Impossible and Deferred Rationale

### IR-C-1: Peer Checking — Impossible

**Pattern:** C-1 (Peer Checking — Concurrent, Same Context)

**Why impossible:** Peer checking requires two persons (performer and peer) to verify in parallel that the correct action is about to be performed on the correct component. They must be present at the same time and place as the action occurs. The Jerry framework enforces single-level agent nesting (H-01/P-003): parallel agent execution with shared real-time state awareness is not supported. Even if two agents ran in parallel (which P-003 prohibits), they cannot observe each other's tool call execution in real time. LLM agents execute sequentially — one inference pass after another.

**Why not even an approximation:** The closest available approximation is sop-verifier's context-isolated sequential verification (C-2). This is qualitatively different from concurrent peer checking: it operates after execution (not during), it cannot stop an incorrect action before it executes (it can only evaluate work products after the fact), and it requires a separate invocation rather than concurrent presence.

**Compensating control:** sop-verifier (C-2) provides sequential independent verification after execution. sop-executor's STAR self-checking (B-1) provides the operator's self-check that in nuclear practice would trigger the peer check request. These two patterns together approximate the intent of peer checking (catch errors before consequences propagate) but through temporal sequence rather than concurrent presence.

**Source:** Pattern Extraction GAP-05; §4.3 Impossible gaps; §2 Mapping Table row C-1 (Weak fit, impossible); Synthesis spec §2 Cross-Reference Matrix row C-1 (Accept as limitation).

---

### DR-A-1: Procedure Type Hierarchy — Deferred

**Pattern:** A-1 (Procedure Type Hierarchy: OPs/AOPs/EOPs/ARPs/STPs/IOPs/MPs)

**Why deferred (not Phase 1):** The WORKFLOW_DEFINITION.template.md `workflow_type` field (NOMINAL/ABNORMAL/EMERGENCY) implements a simplified three-value analog that covers the most important distinction (normal vs. abnormal vs. emergency). The full nuclear taxonomy (seven procedure types with distinct use levels, authority requirements, and regulatory implications) requires a more complete workflow classification system with routing logic, authority annotation per type, and integration with the AE escalation rules. This work is Phase 2 scope, deferred to allow Phase 1 to establish the core brief/execute/verify/capture infrastructure first.

**What Phase 1 delivers:** The `workflow_type` field with three values captures the essential behavioral distinction (standard vs. off-normal vs. emergency), which is sufficient for Phase 1 validation scenarios.

**Target phase:** Phase 2 (+2 months from Phase 1 delivery). Implementation path: extend `workflow_type` enum to full nuclear taxonomy, add routing logic for each type, integrate with authority annotation system.

**Source:** Pattern Extraction §5 Priority Tier assignment (Deferred, score=6, analyst override: "defer until T2 patterns complete"); Synthesis spec §2 Cross-Reference Matrix row A-1 (Phase 2).

---

### DR-A-3b: Standard Procedure Structure — Section Ordering Enforcement — Deferred

**Pattern:** A-3b (Sub-pattern of A-3: strict enforcement of section ordering in workflow definitions)

**Why deferred (not Phase 1):** The 11-section WORKFLOW_DEFINITION template (A-3, directly implemented) defines the required structure. Section ordering enforcement (auto-rejection of workflow definitions with out-of-order sections) is a sop-brief validation behavior that requires: (1) a formal section schema with defined ordering rules, (2) a validation pass against that schema during Step 1, and (3) explicit user feedback on ordering violations rather than silent correction. This is technically feasible but was scoped to Phase 2 behavioral baselines to avoid expanding Phase 1 sop-brief complexity. Phase 1 sop-brief validates section completeness (are all sections present?) but does not enforce ordering (are sections in the correct sequence?).

**Compensating control in Phase 1:** WORKFLOW_DEFINITION.template.md presents sections in the correct order, and sop-brief Step 1 validates that sections 1-6 are complete. A workflow definition that presents sections out of order is structurally non-standard but will not trigger a STOP in Phase 1 sop-brief — the user is responsible for following the template order.

**Target phase:** Phase 2 behavioral baselines (concurrent with A-1 and E-1 extensions).

**Source:** Handoff Pattern Enumeration (A-3b explicitly listed as Deferred, not a sub-row of A-3 direct translation); Synthesis spec §3 Phase 1 acceptance criteria (section completeness only, not ordering enforcement).

---

## Coverage Summary

### Count by Category

| Category | Count | Pattern IDs | Status Distribution |
|----------|-------|-------------|---------------------|
| Direct Translation | 9 | A-3, A-4, A-5, C-2, C-3, D-1, D-2, E-2, I-1 | 8 TRACED, 1 APPROXIMATED (C-2) |
| Partial Translation | 4 | A-2, E-1, F-1, G-1 | 2 TRACED (A-2, E-1), 2 APPROXIMATED (F-1, G-1) |
| Conceptual Translation | 6 | B-1, B-2, F-2a, F-2b, H-1, H-2 | 6 APPROXIMATED |
| Impossible | 1 | C-1 | 1 IMPOSSIBLE |
| Deferred | 2 | A-1, A-3b | 2 DEFERRED |
| **Total** | **22** | All patterns from pattern-extraction.md | 10 TRACED, 9 APPROXIMATED, 1 IMPOSSIBLE, 2 DEFERRED |

### Verification Method Distribution

| Method | Count | Patterns |
|--------|-------|---------|
| BEHAVIORAL-SAMPLE | 6 | D-1, D-2, E-2, B-1, B-2, F-2a |
| TRACE-INSPECTION | 5 | A-5, I-1, F-2b, H-1, H-2 |
| STRUCTURAL-ANALYSIS | 10 | A-3, A-4, C-2, C-3, A-2, E-1, F-1, G-1, A-1 (deferred), A-3b (deferred) |
| METRIC-REFERENCE | 0 | None in Phase 1 (PM-01 through PM-07 require QG-E4 execution) |
| N/A | 1 | C-1 (Impossible) |

**Note on METRIC-REFERENCE:** No patterns are assigned METRIC-REFERENCE verification in Phase 1 because the metrics (PM-01: error trap catch rate; PM-02: stop-work invocation accuracy; PM-03: OE schema completeness; PM-04 through PM-07) are generated by eng-qa-001 executing test scenarios in ENG Phase 4. METRIC-REFERENCE verification for B-1 (STAR catch rate) will be assigned in the V&V Phase 2 matrix after QG-E4 produces documented metric values.

### Gap Analysis

| Gap ID | Nuclear Gap | Phase 1 Coverage | Residual Gap |
|--------|-------------|------------------|-------------|
| GAP-01 | Pre-Job Briefing (F-2a) | ADDRESSED — sop-brief agent implements full pre-job briefing with OE mandatory context | OE accumulation enforcement requires validation (TC-brief-006) |
| GAP-02 | Post-Job Briefing / OE Capture (F-2b) | ADDRESSED — sop-capture agent with mandatory schema; NS-H-06 enforces write-block | Full CAP-to-revision cycle is Phase 3 residual |
| GAP-03 | Procedure Use Classification (A-2) | ADDRESSED — [CONTINUOUS]/[REFERENCE]/[INFORMATION] step annotations in sop-executor | Behavioral validation that CONTINUOUS enforcement holds under pressure (TC-executor-011/012) |
| GAP-04 | OE Feedback Loop (H-1) | PARTIAL — Basic OE capture is Phase 1; CAP analytics and procedure revision cycle is Phase 3 | Phase 3 ps-synthesizer integration not in Phase 1 scope |
| GAP-05 | Concurrent Peer Checking (C-1) | NOT ADDRESSABLE — architecturally impossible | Accepted limitation; compensating controls documented |
| GAP-06 | Symptom-Based Emergency Routing (G-1) | PARTIAL — workflow_type field exists; full EOP symptom routing is Phase 4 | Phase 4 ABNORMAL/EMERGENCY activation logic not in Phase 1 scope |
| GAP-07 | Questioning Attitude (B-2) | PARTIAL — embedded in STAR THINK prompt; behavioral transfer uncertain | Requires empirical validation via BEHAVIORAL-SAMPLE (TC-executor-016) |
| GAP-09 | Agent Behavioral Drift Monitoring | NOT IN PHASE 1 — reclassified from Impossible to Medium Feasibility 2026-03-25; infrastructure not yet built | Phase 3 or Phase 4 scope; requires sop-capture OE corpus as prerequisite |

### Source Confidence Annotation

The following trace entries reference requirements derived primarily from `research/skill-integration-analysis.md` (scored 0.91, below the 0.93 build threshold, accepted risk per orchestration plan Risk Register). These entries are marked `[SOURCE-CONF: 0.91, ACCEPTED-RISK]`:

- **F-1 (Three-Part Communication):** The characterization of handoff schema key_findings echo as a partial Three-Part Communication implementation was first articulated in the integration analysis. The core trace (handoff schema fields, HD-M-001) is sourced from agent-development-standards.md (authoritative). Only the partial-translation classification framing is sourced from the integration analysis. `[SOURCE-CONF: 0.91, ACCEPTED-RISK]`
- **SKILL.md routing/keyword configuration:** The mandatory-skill-usage.md trigger map row for `/nuclear-sop` originates from the synthesis spec §1.1 (Activation Keywords table, confidence 0.922). No integration analysis dependency.

**Assessment:** The integration analysis sub-threshold confidence has minimal material impact on this traceability matrix. All structural requirements (agent definitions, templates, behavioral rules) are traced to the synthesis spec (0.922) and ADR-001 (0.933). The integration analysis contributes primarily to ecosystem integration characterization, which is not the primary subject of this matrix.

---

## Open Items

| Item ID | Description | Blocking? | Expected Resolution |
|---------|-------------|-----------|-------------------|
| OI-001 | **c3-adr-workflow-definition.md is pending** — The worked example (STAR validation fixture with deliberate error traps) is being produced by eng-qa-001 in ENG Phase 4 in parallel with this V&V Phase 1 work. Test cases TC-executor-014 and TC-executor-015 (STAR A/B validation) cannot be fully specified until this artifact exists. | No (BARRIER-2 synchronization) | QG-E4; ENG Phase 4 completion |
| OI-002 | **Test case IDs are placeholders** — All `TC-{agent}-{NNN}` identifiers in this matrix are placeholders. eng-qa-001 will assign actual test case IDs and populate the test harness after ENG Phase 4 completion. | No (by design — parallel execution at Group 8) | BARRIER-2; eng-qa-001 hands off populated IDs to nse-verification-001 at QG-V2 |
| OI-003 | **METRIC-REFERENCE verification method is unassigned** — PM-01 through PM-07 metrics (STAR catch rate, stop-work invocation accuracy, OE schema completeness, etc.) require QG-E4 execution to produce documented values. V&V Phase 2 (nse-verification-001) should assign METRIC-REFERENCE verification to B-1 (STAR) and H-1 (OE schema) after QG-E4 results are available. | No (Phase 2 scope) | QG-V2 (V&V Phase 2); after QG-E4 |
| OI-004 | **H-36 governance ruling is pending** — The 4-hop vs. 3-hop mode ambiguity (whether a predetermined intra-skill verification step constitutes an H-36 hop) affects NS-H-08 and the C3+ verification architecture. A governance ruling deadline is set at 60 days from Phase 1 delivery. If no ruling is received within 60 days, sop-verifier is eliminated and NS-H-08 is superseded by 3-hop mode for all criticality levels. | No (SKILL.md documents the governance deadline) | Governance ruling or 60-day deadline |
| OI-005 | **sop-executor.governance.yaml and all agent .governance.yaml files not directly read** — H-34 dual-file architecture requires both the .md agent definition and the companion .governance.yaml file for each agent. This matrix traces to the .md agent files; the .governance.yaml files were not individually read for this matrix but are listed as expected implementation evidence (per barrier handoff artifact table rows 4, 6, 8, 10). V&V Phase 2 (STRUCTURAL-ANALYSIS verification) should confirm all four .governance.yaml files validate against docs/schemas/agent-governance-v1.schema.json. | No (V&V Phase 2 scope) | QG-V2 structural verification |

---

*Generated by nse-requirements agent v1.0.0 (nse-requirements-001)*
*V&V Phase 1 — /nuclear-sop Build Pipeline nuclear-sop-build-20260325-001*
*All 22 patterns from pattern-extraction.md covered. Zero orphaned patterns.*

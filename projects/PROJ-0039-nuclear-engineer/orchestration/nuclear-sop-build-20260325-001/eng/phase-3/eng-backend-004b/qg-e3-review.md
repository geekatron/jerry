# QG-E3 Review: sop-capture + POST_JOB_BRIEF Template

## Scoring Context

- **Deliverable:** `skills/nuclear-sop/agents/sop-capture.md` + `sop-capture.governance.yaml` + `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md`
- **Deliverable Type:** Agent definition (dual-file) + execution template
- **Criticality Level:** C3
- **Scoring Strategy:** S-014 (LLM-as-Judge) + 7 targeted validation checks
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored By:** adv-executor (QG-E3)
- **Scored:** 2026-03-26T00:00:00Z
- **Iteration:** 1 (first QG-E3 scoring)

---

## L0 Executive Summary

**Score:** 0.93/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.87)

All 7 targeted validation checks pass. The sop-capture agent and POST_JOB_BRIEF template are ready for integration. One minor gap in the template's C3+ verification section (IV iteration counter placement) and one minor ambiguity in dual-write failure escalation are flagged as low-priority improvement items. No blockers.

---

## Section 1: Targeted Validation Checks

### (a) OE Write-Block Enforcement

**Status: PASS**

The agent definition is unambiguous on write-block behavior. In `<methodology>` Step 3:

> "Before calling Write, validate that every required field in the OE entry schema is populated and non-empty. If any required field is missing or empty: DO NOT call Write."

This is reinforced in `<guardrails>` forbidden_actions (governance.yaml):

> "SCHEMA VIOLATION: NEVER write an OE entry with a missing or empty required field -- write is BLOCKED, not warned"

The `enforcement.escalation_path` in governance.yaml reads: "Block OE entry write on missing required fields -> Escalate to user with specific missing field name -> Await user input -> Re-validate before write". The write-block is enforced at the correct pre-Write validation gate, not post-hoc. No gap.

---

### (b) Dual-Write to capture/ AND docs/experience/

**Status: PASS with minor gap**

The agent definition mandates two writes:
1. `capture/oe-entry-{entry_id}.md` -- local capture directory
2. `docs/experience/{entry_id}.md` -- persistent OE corpus

This is stated in three locations: `<methodology>` Step 3, `<output>` artifact table, and governance.yaml `output.dual_write_mandatory: true` with `dual_write_paths` declared. The failure mode table in `<guardrails>` explicitly states: "the local capture write is NOT sufficient alone; both writes are mandatory."

**Minor gap (LJ-002):** The failure mode for `docs/experience/` write failure says "Report failure" but does not specify whether the already-completed local `capture/` write should be rolled back or retained. In a real execution, a partial dual-write (local succeeds, persistent fails) leaves the OE corpus without the entry while `PROCEDURE_STATE.yaml` may have been updated. The guidance to report failure without a rollback instruction could lead to an inconsistent state. This is operationally acceptable for a first version (C3 deliverable, not C4) but should be flagged for a future patch.

---

### (c) SR-05 Hold Point Consistency Cross-Reference (Triangulation)

**Status: PASS**

SR-05 is implemented at three levels and is mutually reinforcing:

1. **Agent methodology** (`<methodology>` Step 1): Requires cross-referencing every hold point defined in the workflow definition against records in BOTH the execution log AND PROCEDURE_STATE.yaml. Defines `HOLD_POINT_NOT_ACTIVATED` flag and escalation rule for USER-HOLD bypasses.

2. **Template** (POST_JOB_BRIEF.template.md `## Hold Point Record`): Provides the SR-05 cross-reference table with four columns (Hold Point from workflow definition, Execution Log Record, PROCEDURE_STATE.yaml Record, SR-05 Status). Includes the `HOLD_POINT_NOT_ACTIVATED` anomaly sub-table with `Escalation Required` column.

3. **Governance** (governance.yaml `forbidden_actions`): "SR-05 VIOLATION: NEVER produce an OE entry or post-job brief without cross-referencing all workflow-defined hold points" and `validation.post_completion_checks` includes `verify_sr05_hold_point_check_documented`.

The triangulation is complete. A sop-capture execution that skips the SR-05 check would have to violate a forbidden_action, skip a post-completion check, and leave the template section unpopulated -- three independent detection layers.

---

### (d) Deviation Classification (NONE/MINOR/MAJOR/STOP-WORK)

**Status: PASS**

The four-level classification in `<methodology>` Step 2 is well-defined with:
- Precise decision rules per level (condition + examples)
- The "escalate, never suppress" rule: MINOR->MAJOR on ambiguity, MAJOR->STOP-WORK on ambiguity
- Constitutional grounding: "Suppression of severity is a P-020 violation and corrupts the OE feedback loop"

The governance.yaml forbidden_actions reinforces this: "P-020 VIOLATION: NEVER write an OE entry that suppresses deviations, misclassifies MAJOR as MINOR, or omits hold point anomalies".

The POST_JOB_BRIEF template's Deviation Log section includes the four-level classification rules inline as a blockquote reference, so a sop-capture executing the template will see the rules at point of use.

The OE schema in the template's `## Operating Experience Entry` section includes `deviation_type` as a required field with its enum values.

No gap.

---

### (e) Anchoring Bias Disclaimer for 3-Hop Integrated IV

**Status: PASS**

The anchoring bias disclaimer is present verbatim in three locations:

1. **Agent methodology** (`<methodology>` Step 0, item 4): Provides the exact verbatim text to be written, labeled "verbatim".

2. **POST_JOB_BRIEF template** (`## Verification Outcome`, subsection `C1-C2 Integrated Independent Verification`): The disclaimer is hardcoded into the template as a blockquote, not as a placeholder. Any sop-capture execution that uses the template correctly will emit the disclaimer automatically without any agent decision required.

3. **Governance.yaml** (`output_filtering`): `anchoring_bias_disclaimer_required_for_all_c1_c2_iv_results` and `forbidden_actions` P-022 entry explicitly references the 3-hop vs. 4-hop distinction.

4. **Constitutional compliance** section of governance.yaml (`principles_applied` P-022 entry) also calls out the integrated IV limitation.

The disclaimer is structurally unavoidable in the template: it is part of the template text, not a sop-capture-injected placeholder. A sop-capture execution would need to actively delete the disclaimer from the post-job brief to suppress it, which would constitute a P-022 violation caught by the forbidden_actions guardrail.

No gap.

---

### (f) All Mandatory OE Schema Fields in Template

**Status: PASS**

Cross-referencing the agent's required field table (`<methodology>` Step 3, 10 required fields) against the OE entry schema in the POST_JOB_BRIEF template (`## Operating Experience Entry`, YAML block):

| Required Field (agent definition) | Present in Template Schema |
|------------------------------------|---------------------------|
| `entry_id` | Yes -- `entry_id: "{workflow_id}-{YYYYMMDD}-{NNN}"` |
| `workflow_id` | Yes |
| `workflow_type` | Yes -- `"NOMINAL | ABNORMAL | EMERGENCY"` |
| `criticality` | Yes -- `"C1 | C2 | C3 | C4"` |
| `deviation_type` | Yes -- `"NONE | MINOR | MAJOR | STOP-WORK"` |
| `root_cause` | Yes |
| `recommendation` | Yes |
| `verification_outcome` | Yes -- `"ACCEPTED | REJECTED | ACCEPTED-WITH-CONDITIONS | N/A"` |
| `error_traps_encountered` | Yes -- list with example entry |
| `quality_gate_final_score` | Yes -- `null` default with explanation |

The template also includes the `entry_version`, `created_at`, `total_steps`, `steps_completed`, `steps_deviated`, `hold_points_activated`, `stop_work_events`, and `verification_mode` fields, which appear in the agent's full schema block but are not in the 10-field write-block list. This distinction is correctly handled: the template includes ALL schema fields; the write-block governs only the 10 critical fields.

The template's schema enforcement note explicitly states: "sop-capture blocks the OE entry Write call if any field is missing or empty."

No gap.

---

### (g) Constitutional Triplet, No Task Tool

**Status: PASS**

**P-003 (No recursive subagents / Task tool absent):**
- `sop-capture.md` frontmatter tools list: `["Read", "Write", "Edit", "Glob", "Grep", "Bash"]` -- Task is absent.
- `<identity>`: "Spawn subagents or delegate via Task tool (T2 worker; Task tool is absent)"
- `<capabilities>`: "Task tool: ABSENT. sop-capture is a T2 worker."
- Governance.yaml `capabilities.allowed_tools` does not include Task.
- Governance.yaml `forbidden_actions` P-003 entry is present and complete.
- Governance.yaml `constitution.principles_applied` P-003 entry present.

**P-020 (User authority):**
- OE write-block is described as a mandatory quality gate but "the user may provide missing field values" -- user authority preserved.
- The sop-brief >20 OE entries STOP threshold is "user-overridable with explicit acknowledgment."
- Governance.yaml constitution.principles_applied P-020 entry addresses both cases.

**P-022 (No deception):**
- Integrated IV (3-hop) anchoring bias disclaimer is mandatory and verbatim.
- Governance.yaml constitution.principles_applied P-022 entry present.
- Forbidden_actions P-022 entry explicitly names the 3-hop vs. 4-hop misrepresentation risk.

All three constitutional principles are declared in `principles_applied` AND in `forbidden_actions` (with NPT-009-complete format). The forbidden_action_format is declared as `NPT-009-complete`. H-35 minimum of 3 forbidden_actions is exceeded (5 total).

No gap.

---

## Section 2: S-014 Dimension Scores

### Dimension 1: Completeness (weight 0.20)

**Score: 0.94**

The agent definition covers all required sections per H-34 agent definition standards: `<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>`. The methodology is complete across all 4 steps with a Step 0 conditional for C1-C2. All five mandatory output artifacts are specified with paths and timing.

The POST_JOB_BRIEF template covers all 7 sections indicated in its navigation table. The OE schema in the template matches the 10 required write-block fields plus all structural fields from the agent's full YAML block.

Minor: The template's C3+ Verification section does not include the IV iteration counter ("IV Iteration: {1|2|3}") in the template body -- this field appears in the template text (line 117) but is placed after the `IV Disposition` line without a corresponding Execution Log or PROCEDURE_STATE.yaml source annotation, making it slightly less actionable than the other fields. This is a presentation gap, not a structural incompleteness.

Evidence for high score: All decision branches are documented (C1-C2 vs C3+, REJECTED IV disposition, STOP-WORK classification). No sections are stubs or placeholders.

---

### Dimension 2: Internal Consistency (weight 0.20)

**Score: 0.95**

Cross-checking the three artifacts against each other:

- The 10 required OE fields in `sop-capture.md` match the OE schema in POST_JOB_BRIEF template exactly.
- The dual-write paths declared in `sop-capture.md` (`capture/oe-entry-{entry_id}.md`, `docs/experience/{entry_id}.md`) match governance.yaml `output.dual_write_paths`.
- The governance.yaml `output.levels` declares L0, L1, L2 -- these match the `<output>` section's L0/L1/L2 definitions.
- The criticality branches (C1-C2 for Step 0, C3+ to skip Step 0) are consistent between `<methodology>`, `<input>` (criticality determination), and `<guardrails>` input_validation.
- The deviation classification rules in `<methodology>` Step 2 match the deviation log section in the template.
- The SR-05 hold point check is referenced consistently in methodology, template, governance validation checks, and forbidden_actions.
- The anchoring bias disclaimer text is verbatim-identical in methodology and template.

Evidence for high score: Five explicit cross-references checked above all agree. No contradictions found across the three files.

3 strongest evidence points for score > 0.90:
1. OE schema field-for-field alignment between agent definition and template verified exhaustively.
2. Dual-write paths are declared identically in agent definition (`<output>`) and governance.yaml.
3. Verbatim disclaimer text in methodology matches the hardcoded template text byte-for-byte.

---

### Dimension 3: Methodological Rigor (weight 0.20)

**Score: 0.93**

The methodology implements recognized nuclear industry patterns:
- F-2b (Post-Job Briefing)
- H-1 (Corrective Action Program)
- H-2 (Operating Experience Review)

The four-step execution sequence is logically ordered: IV (Step 0, conditional) -> Execution Analysis (Step 1) -> Deviation Classification (Step 2) -> OE Entry Production (Step 3) -> Post-Job Brief (Step 4). The ordering is defensible: you cannot classify deviations before analyzing execution; you cannot produce the OE entry before classifying deviations.

The write-block enforcement is a procedurally rigorous gate: validation happens before the tool call, not after. This is the correct nuclear-grade approach (validate before you commit, not after).

The FINAL log check (Step 1 gate on `execution_log_final: true`) is methodologically sound -- it prevents sop-capture from running on a partial log.

Minor: The `entry_id` NNN sequencing uses Glob to count files for the current day. If two sop-capture executions run simultaneously for the same workflow_id on the same day, there is a potential race condition in the NNN counter. This is a minor methodological gap (Bash `ls | wc -l` has no atomic increment). For an LLM agent running sequentially, this is practically irrelevant, but it could be noted in a future version.

---

### Dimension 4: Evidence Quality (weight 0.15)

**Score: 0.87**

The agent definition provides strong structural evidence for its design choices:
- The dual-write is justified: "future sop-brief invocations with accurate lessons learned"
- The write-block (not warn) is justified: "ensures the OE corpus remains searchable and synthesizable, preventing the T-4.1 (feedback loop poisoning) threat"
- The anchoring bias disclaimer is justified: references the C1-C2 reversibility rationale

However, the evidence for several design decisions is stated but not sourced:
- The "3-hop" and "4-hop" terminology is used throughout but the spec reference for /nuclear-sop Section 1.8 is cited but not co-located with the definition. A reader must locate the spec separately to verify.
- The STAR Review methodology is referenced in the deviation log and execution comparison but the STAR acronym is never expanded (Situation-Task-Action-Result).
- The SD-02/SD-03/SD-12/SD-14/SD-16 security design references are cited in governance.yaml and `<output>` but the source security design document is not identified, making traceability incomplete.

These are evidence-level gaps, not structural gaps. The design decisions are correct -- the justification trail just has some dead-ends.

---

### Dimension 5: Actionability (weight 0.15)

**Score: 0.95**

Every step in the methodology is executable:
- Step 0: Read acceptance criteria from pre-job brief -> evaluate against work products -> record per-criterion disposition -> write verbatim disclaimer. No ambiguity.
- Step 1: Read PROCEDURE_STATE.yaml -> verify `execution_log_final: true` -> halt if false. Concrete tool-call sequence implied.
- Step 2: Apply decision table with explicit conditions. "Escalate, never suppress" rule resolves ambiguous cases unambiguously.
- Step 3: Validate 10 fields -> block write if any empty -> assemble OE entry schema -> write to two paths. Fully specified.
- Step 4: Write post-job brief using template -> edit PROCEDURE_STATE.yaml -> report final status. Fully specified.

The template is immediately usable: it is a fill-in-the-blanks document with inline instructions (HTML comments with "sop-capture:" prefix) at each section. The OE schema YAML block in the template can be copy-pasted directly.

The `entry_id` auto-generation procedure in Step 3 is algorithmically complete (Glob pattern, count+1, zero-pad to 3 digits, assemble).

3 strongest evidence points for score > 0.90:
1. Every decision branch has a stated halt/proceed/escalate outcome with no open-ended cases.
2. The template inline instructions use "sop-capture:" prefix, making them clearly machine-targeted, not human editorial.
3. The final confirmation message to user (Step 4) specifies exactly 6 fields to report -- no judgment required about what to summarize.

---

### Dimension 6: Traceability (weight 0.10)

**Score: 0.88**

Strong traceability present:
- Nuclear patterns F-2b, H-1, H-2 identified by standard designator in agent `<identity>`, governance.yaml `nuclear_patterns`, and `<output>` security design compliance.
- Security design patterns SD-02, SD-03, SD-12, SD-14, SD-16 cross-referenced in governance.yaml and agent `<output>`.
- Constitutional compliance P-003, P-020, P-022 referenced in forbidden_actions (with NPT-009-complete format), constitution.principles_applied, and `<guardrails>`.
- SR-05 as a named rule is consistently cited across methodology, template, governance validation.

Minor traceability gap: The nuclear patterns F-2b, H-1, H-2, and the security design patterns SD-02 through SD-16 are cited by designator but the source document for these designators is not specified. An auditor cannot verify the correct implementation of F-2b without knowing which source document defines it. The governance.yaml `nuclear_patterns` section describes what each pattern does for sop-capture but does not reference the source specification document.

Similarly, the T-4.1 "feedback loop poisoning" threat reference in `<purpose>` is cited without a source (threat model document or risk register).

---

## Section 3: Weighted Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.94 | 0.188 |
| Internal Consistency | 0.20 | 0.95 | 0.190 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.87 | 0.131 |
| Actionability | 0.15 | 0.95 | 0.143 |
| Traceability | 0.10 | 0.88 | 0.088 |
| **Composite** | **1.00** | | **0.926** |

**Rounded composite: 0.93**

**Verification:** 0.188 + 0.190 + 0.186 + 0.131 + 0.143 + 0.088 = 0.926 -> 0.93. Confirmed.

---

## Section 4: Verdict

**Verdict: PASS**

Composite 0.93 >= 0.92 threshold (H-13). No dimension scores <= 0.50 (no Critical findings). No unresolved Critical findings from prior strategy reports. Threshold met on first QG-E3 scoring.

Special conditions check:
- Any dimension Critical (score <= 0.50)? No. Lowest dimension is Evidence Quality at 0.87 (Minor).
- Prior strategy unresolved Critical findings? No prior strategy reports provided.
- Composite < 0.50 after 3+ cycles? Not applicable (iteration 1).

All 7 targeted validation checks pass. PASS verdict holds.

---

## Section 5: Findings Summary

| ID | Severity | Finding | Dimension / Check |
|----|----------|---------|-------------------|
| LJ-001 | Minor | Dual-write failure leaves no rollback/retention guidance for partial write state | Check (b) / Completeness |
| LJ-002 | Minor | C3+ template IV iteration counter lacks source annotation | Completeness |
| LJ-003 | Minor | NNN entry_id sequencing has theoretical race condition for same-day concurrent runs | Methodological Rigor |
| LJ-004 | Minor | STAR acronym used but not expanded in methodology or template | Evidence Quality |
| LJ-005 | Minor | SD-02 through SD-16 source document not identified; traceability dead-end | Evidence Quality / Traceability |
| LJ-006 | Minor | Nuclear pattern source specification not cited (F-2b, H-1, H-2 designators without source) | Traceability |
| LJ-007 | Minor | T-4.1 threat reference in `<purpose>` has no source document | Evidence Quality |

All findings are Minor severity. No Critical or Major findings.

---

## Section 6: Improvement Recommendations

| Priority | Recommendation | Target | Rationale |
|----------|----------------|--------|-----------|
| 1 | Add failure-state guidance for partial dual-write: specify whether local capture write should be retained or rolled back when docs/experience/ write fails | `<guardrails>` failure modes table, dual-write failure row | Prevents inconsistent state where PROCEDURE_STATE.yaml shows oe_entry_path but the path does not exist in docs/experience/ |
| 2 | Add source document reference for nuclear patterns (F-2b, H-1, H-2) and security design patterns (SD-02 through SD-16) in governance.yaml | `nuclear_patterns` and `security_design` sections of governance.yaml | Enables auditor verification without tribal knowledge |
| 3 | Expand STAR acronym on first use in methodology or add a Nuclear Terminology section to SKILL.md | `<methodology>` Step 1 execution comparison table | Reduces reader confusion; STAR is used in deviation log, execution log, and verifier references throughout the skill |
| 4 | Add IV iteration source annotation to C3+ template section | POST_JOB_BRIEF.template.md `### C3+ Independent Verification` | Aligns with other template fields that specify their source (e.g., "from PROCEDURE_STATE.yaml iv_report_path") |

---

## Section 7: Leniency Bias Self-Check (H-15)

- Each dimension scored independently: Yes. Scores were assigned before composite was computed.
- Evidence documented for each score: Yes. Specific field names, section references, and cross-checks cited.
- Uncertain scores resolved downward: Applied to Evidence Quality (0.87, not 0.90) and Traceability (0.88, not 0.90) due to dead-end source references.
- High-scoring dimensions (>0.90) verified with 3 evidence points each: Done for Internal Consistency and Actionability above.
- Weighted composite matches calculation: Verified (0.926 -> 0.93).
- Verdict matches score range: PASS (0.93 >= 0.92). Confirmed.
- Improvement recommendations specific and actionable: Yes -- each names a specific section and explains the change.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 0
- **Major:** 0
- **Minor:** 7
- **Targeted Validation Checks:** 7 of 7 PASS
- **Protocol Steps Completed:** 7 of 7
- **Composite Score:** 0.93
- **Verdict:** PASS (threshold 0.93 >= 0.92)

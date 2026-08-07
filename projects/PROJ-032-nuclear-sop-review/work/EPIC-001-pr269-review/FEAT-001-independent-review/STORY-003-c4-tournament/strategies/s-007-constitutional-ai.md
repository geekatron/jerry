# Constitutional Compliance Report: /nuclear-sop Skill (PR #269)

> **Strategy:** S-007 Constitutional AI Critique
> **Deliverable:** `skills/nuclear-sop/` (31 files, ~8.5k lines) + registration surfaces (`.claude-plugin/plugin.json`, `CLAUDE.md`, `AGENTS.md`, `.context/rules/mandatory-skill-usage.md`, `CHANGELOG.md`)
> **Criticality:** C4 (full tournament)
> **Date:** 2026-08-07
> **Reviewer:** adv-executor (S-007 strategy execution, blind mode)
> **Constitutional Context:** Jerry Constitution v1.0 (`docs/governance/JERRY_CONSTITUTION.md`, P-001–P-043); `.context/rules/quality-enforcement.md` HARD Rule Index (H-01–H-36); `skill-standards.md` (H-25, H-26); `markdown-navigation-standards.md` (H-23); `agent-development-standards.md` (H-34, H-35); `agent-routing-standards.md` (H-36)
> **Finding ID convention:** Per orchestrator instruction for this tournament execution, findings use the unified `S-007-NN` numbering (rather than the template's default `CC-NNN-{execution_id}`) to align with the tournament's cross-strategy report naming.
> **Path hygiene note:** All references to the PR's own source project are written as `«PR projects tree»/PROJ-0039-nuclear-engineer/...` per reviewer instruction; this is not a live path in the reviewing repository.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall compliance verdict |
| [Constitutional Context Index](#constitutional-context-index) | Principles and rules loaded for this review |
| [Applicable Principles Checklist](#applicable-principles-checklist) | Principles scoped to this deliverable |
| [Findings Summary](#findings-summary) | All findings at a glance |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and remediation per finding |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Constitutional Compliance Score](#constitutional-compliance-score) | Final score and threshold determination |
| [Strategy Verdict](#strategy-verdict) | One-paragraph overall assessment |

---

## Summary

**NON-COMPLIANT.** This review found 2 Critical, 5 Major, and 2 Minor constitutional findings. The two Critical findings are both falsifiable, evidence-backed defects that a Constitutional AI critique exists specifically to catch: (1) a named security control (`state_hash` SHA-256 tamper detection) is documented as implemented and verified "before every tool call" but is never computed or checked anywhere in the executing agent's actual specification (P-001/P-022 — false confidence in a behavioral/technical constraint); and (2) the skill's own template and behavioral-baseline test spec instruct writing Operating Experience entries with a file extension (`.md`) that the skill's own retrieval mechanism (`Glob **/*.yaml`) can never find, silently breaking the mandatory OE feedback loop that the skill advertises as a flagship capability. Constitutional compliance score: **0.51 (REJECTED)**, well below the H-13 threshold of 0.92. Recommendation: **REJECT** — remediate the 2 Critical and 5 Major findings before merge.

---

## Constitutional Context Index

| Principle/Rule ID | Name | Tier | Source | Applicability |
|---|---|---|---|---|
| P-001 | Truth and Accuracy | Advisory/Soft | JERRY_CONSTITUTION.md Art. I | Applicable — skill makes multiple factual claims about mechanisms, validation results, and registration state |
| P-002 | File Persistence | Hard/Medium | JERRY_CONSTITUTION.md Art. I | Applicable — all agents claim mandatory file outputs |
| P-003 | No Recursive Subagents | Hard/Hard | JERRY_CONSTITUTION.md Art. I | Applicable — 4-agent, T1/T2 worker topology with cross-agent hand-offs (QG-HOLD, IV-HOLD) |
| P-004 | Explicit Provenance | Medium/Soft | JERRY_CONSTITUTION.md Art. I | Applicable — governance deadlines, validation evidence, registration state all carry provenance claims |
| P-011 | Evidence-Based Decisions | Medium/Soft | JERRY_CONSTITUTION.md Art. II | Applicable — STAR validation evidence, OE schema evidence requirements |
| P-020 | User Authority | Hard/Hard | JERRY_CONSTITUTION.md Art. III | Applicable — USER-HOLD, WAIVE, OVERRIDE mechanisms throughout |
| P-021 | Transparency of Limitations | Medium/Soft | JERRY_CONSTITUTION.md Art. III | Applicable — STAR "behavioral not deterministic" disclosures, sop-verifier anchoring-bias disclaimer |
| P-022 | No Deception | Hard/Hard | JERRY_CONSTITUTION.md Art. III | Applicable — multiple claims about security mechanisms and governance/registration state require accuracy verification |
| H-13 | Quality threshold >= 0.92 | Hard | quality-enforcement.md | Applicable — QG-HOLD gate design references H-13 directly |
| H-18 | Constitutional compliance check (S-007) | Hard | quality-enforcement.md | This review implements H-18 |
| H-22 | Proactive skill invocation | Hard | mandatory-skill-usage.md | Applicable — new skill registration completeness |
| H-23 | Navigation table required/complete | Hard/Medium(NAV-004) | markdown-navigation-standards.md | Applicable — AGENTS.md nav-table coverage of new section |
| H-25/H-26 | Skill naming, description, registration | Hard | skill-standards.md | Applicable — SKILL.md, CLAUDE.md, AGENTS.md, mandatory-skill-usage.md registration |
| H-34/H-35 | Agent definition dual-file architecture, constitutional triplet | Hard | agent-development-standards.md | Applicable — 4 agent `.md`/`.governance.yaml` pairs verified |
| H-36 | Routing circuit breaker (3-hop max) | Hard | agent-routing-standards.md | Applicable — skill's own "3-hop vs. 4-hop" governance question is unresolved and time-boxed |

---

## Applicable Principles Checklist

| ID | Tier | Priority | Rationale for Applicability |
|----|------|----------|------------------------------|
| P-022 | HARD | 1 | Multiple concrete, falsifiable claims (tamper detection, validation results, registration status, governance ruling) must be checked against what the artifact actually implements |
| P-001 | SOFT (Advisory) | 1 | Same evidentiary basis as P-022; truth/accuracy of documented mechanisms |
| P-003 | HARD | 1 | QG-HOLD delegation wording in `sop-executor.md` must be checked against the agent's own T2/no-Task-tool restriction |
| H-25/H-26 | HARD | 2 | New-skill registration completeness across all 4 registration surfaces |
| H-36 | HARD | 2 | Skill explicitly surfaces an unresolved, time-boxed H-36 interpretation question |
| H-34/H-35 | HARD | 2 | Agent definition schema and constitutional-triplet compliance (verified — no findings) |
| H-23 | HARD/MEDIUM | 3 | AGENTS.md navigation-table completeness for the newly added section |
| P-011/P-004 | MEDIUM | 3 | Evidentiary basis and provenance of the QG-E4 STAR validation claim |

10 HARD-tier principles/rules were evaluated (P-002, P-003, P-020, P-022, H-13, H-18, H-22, H-25, H-26, H-34, H-35, H-36 — 12 counted with sub-items), triggering the "10+ HARD → flag high-risk" decision point in the S-007 protocol. This is expected and appropriate for a C4 new-skill-and-registration deliverable of this size.

---

## Findings Summary

| ID | Severity | Finding | File(s) |
|----|----------|---------|---------|
| S-007-01 | Critical | `state_hash` SHA-256 tamper-detection control is documented as implemented/verified but never computed or checked by any agent | `templates/PROCEDURE_STATE.template.yaml`, `docs/reference.md`, `agents/sop-executor.md` |
| S-007-02 | Critical | OE entry file extension conflict (`.yaml` vs `.md`) silently breaks the mandatory OE feedback loop | `templates/POST_JOB_BRIEF.template.md`, `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` vs. `agents/sop-capture.md`, `agents/sop-brief.md`, `rules/nuclear-sop-behavior-rules.md` |
| S-007-03 | Major | QG-HOLD instructs a Task-tool-less T2 agent to "invoke" another agent directly, and conflates two distinct agents (`ps-critic` vs. `adv-scorer`) across the skill | `agents/sop-executor.md`, `composition/sop-executor.prompt.md`, `rules/nuclear-sop-behavior-rules.md`, `SKILL.md`, `PLAYBOOK.md`, `docs/reference.md`, `templates/HOLD_POINT_LOG.template.md` vs. `examples/c3-adr-workflow-definition.md` |
| S-007-04 | Major | NS-H-08's self-declared 60-day H-36 governance deadline (2026-06-15) has lapsed (~53 days) with no visible ruling or fallback, yet the skill still asserts unconditional C1–C4 approval | `SKILL.md`, `rules/nuclear-sop-behavior-rules.md` |
| S-007-05 | Major | SKILL.md's "DEFERRED REGISTRATION NOTE" falsely states the skill is "NOT registered" when CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md already contain the live entries | `SKILL.md`, `CLAUDE.md`, `AGENTS.md`, `.context/rules/mandatory-skill-usage.md` |
| S-007-06 | Major | `/nuclear-sop` is added to the Trigger Map table but omitted from the enforceable H-22 rule prose and the L2-REINJECT comment, weakening proactive-invocation enforcement relative to peer skills | `.context/rules/mandatory-skill-usage.md` |
| S-007-07 | Major | AGENTS.md's navigation table and Agent Summary/Total (89) were not updated for the new "Nuclear SOP Skill Agents" section (should be 93) | `AGENTS.md` |
| S-007-08 | Minor | QG-E4 STAR validation is a same-team simulated walkthrough, not a live execution trace; SKILL.md presents the "PASS — 3/3" result without this methodological caveat | `SKILL.md`, `«PR projects tree»/PROJ-0039-nuclear-engineer/.../star-validation-results.md` |
| S-007-09 | Minor | Template placeholder convention is inconsistent: `{{MUSTACHE}}` + `{{#if}}` in one template vs. plain `{SINGLE_BRACE}` in the other three | `templates/PRE_JOB_BRIEF.template.md` vs. `templates/POST_JOB_BRIEF.template.md`, `templates/WORKFLOW_DEFINITION.template.md`, `templates/HOLD_POINT_LOG.template.md` |

---

## Detailed Findings

### S-007-01: Undocumented Absence of Claimed Tamper-Detection Mechanism [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Principle** | P-001 (Truth and Accuracy), P-022 (No Deception) — both HARD/Hard per JERRY_CONSTITUTION Article V |
| **Section** | `templates/PROCEDURE_STATE.template.yaml` "Tamper Detection"; `docs/reference.md` "Tamper Detection" table |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

`templates/PROCEDURE_STATE.template.yaml` (lines 123–130):
> "SECURITY: state_hash provides integrity verification for security-critical fields. sop-executor computes this hash after every state write; STAR-STOP verifies it on every read. If the hash does not match the current state: FLAG ANOMALY — state was modified outside the designated write mechanism (potential hold bypass or external tampering)... Algorithm: SHA-256 of the concatenated field values..."

`docs/reference.md` (line 314), presented under the file's own header as "Authoritative descriptions... for the `/nuclear-sop` skill":
> "`state_hash` | string \| null | ... | sop-executor | sop-executor | SHA-256 hex digest of the concatenated values of: `status`, `hold_type`, `hold_resolution`, `iv_disposition`, `current_step`, `next_step` ... Computed after every state write. Verified in STAR-STOP before every tool call"

A repo-wide search of `skills/nuclear-sop/` for the token `hash` returns exactly two files: `templates/PROCEDURE_STATE.template.yaml` and `docs/reference.md`. It does **not** appear in `agents/sop-executor.md`, `agents/sop-executor.governance.yaml`, or `composition/sop-executor.prompt.md`. The actual STAR-STOP procedure specified in `sop-executor.md` (lines 149–162) performs exactly these checks: step-number verification, target verification, `current_step` cross-check, and a hold-state consistency check against `status`/`hold_resolution`/AskUserQuestion evidence — **no hash computation, no hash comparison, anywhere.** `sop-executor.governance.yaml`'s `security_design_decisions` list (SD-01 through SD-18) never references `state_hash` either; SD-03 ("hold point state discipline") is the closest analog and relies solely on the SR-04 forbidden-action prose, not a cryptographic check.

**Analysis:**

This is a specific, falsifiable technical claim — not a vague aspiration. `docs/reference.md` states unconditionally that the hash is "Verified in STAR-STOP before every tool call." A reader (human or another agent, e.g., a future security reviewer or `sop-verifier` reading `PROCEDURE_STATE.yaml` for `HOLD_POINT_NOT_ACTIVATED` cross-checks) relying on this reference would reasonably conclude that hold-bypass tampering is cryptographically detected. It is not: the only executing agent capable of performing this check (`sop-executor`) never does so per its own specification. This is precisely the failure mode `sop-executor.md`'s own guardrails warn against: *"P-022 VIOLATION: NEVER misrepresent STAR protocol effectiveness as a deterministic error-prevention guarantee... false confidence leads users to rely on a behavioral constraint that may not constrain the model."* Here the documentation over-claims a **more** deterministic mechanism (a cryptographic hash, not just a behavioral prompt constraint) than what actually exists — the gap between claimed and actual assurance is larger, not smaller.

**Recommendation:**

Either (a) implement `state_hash` computation and verification explicitly inside `sop-executor.md`'s STAR-STOP procedure (add a line under the "Hold-state consistency check (SEC-003)" step: compute/verify the SHA-256 digest, FLAG ANOMALY on mismatch) and add a corresponding `verify_state_hash_checked` entry to `sop-executor.governance.yaml`'s `validation.post_completion_checks`, and reference it in `security_design_decisions`; or (b) if the hash is intentionally deferred/aspirational, remove the "computed after every state write / verified in STAR-STOP" language from `docs/reference.md` and `PROCEDURE_STATE.template.yaml`, and replace with an explicit `[NOT YET IMPLEMENTED]` marker consistent with the skill's own P-022 disclosure pattern used elsewhere (e.g., the STAR "behavioral not deterministic" disclaimer).

---

### S-007-02: OE Entry File-Extension Conflict Breaks the Mandatory OE Feedback Loop [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Principle** | Internal Consistency; P-001; NS-H-06/NS-H-07 (skill-scoped HARD rules) functional integrity |
| **Section** | `templates/POST_JOB_BRIEF.template.md` "Operating Experience Entry"; `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` B-21/B-24 |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

Authoritative write-side specification, `agents/sop-capture.md` Step 3:
> "**Write OE entry to TWO locations (both writes are mandatory):** 1. `capture/oe-entry-{entry_id}.yaml` ... 2. `docs/experience/{entry_id}.yaml`"

Also consistent in `sop-capture.governance.yaml` (`dual_write_paths.local`/`.persistent`, both `.yaml`), `rules/nuclear-sop-behavior-rules.md` ("Global OE registry: `docs/experience/{entry_id}.yaml`"), `SKILL.md` Output Artifacts Summary, and `PLAYBOOK.md`.

Authoritative read-side specification, `agents/sop-brief.md` Step 4:
> "```\nGlob(pattern=\"<oe_search_path>/**/*.yaml\")\nGrep(pattern=\"workflow_type: <value>\", ...)\n```"

Also `rules/nuclear-sop-behavior-rules.md` "OE Search Mechanism": *"Exact workflow match (primary): Glob `docs/experience/*.yaml`..."*

Contradicting evidence, `templates/POST_JOB_BRIEF.template.md` "Operating Experience Entry" section:
> "**Local capture path:** `capture/oe-entry-{entry_id}.md`\n**Persistent path (future sop-brief retrieval):** `docs/experience/{entry_id}.md`"

Contradicting evidence, `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` (the baseline whose entire purpose is validating OE loop integrity), B-21:
> "After field validation, Write must be called twice: 1. `capture/oe-entry-{entry_id}.md` -- local capture directory 2. `docs/experience/{entry_id}.md` -- persistent OE registry"

**Analysis:**

`sop-capture.md` Step 4 explicitly instructs the agent to populate the post-job brief "using the POST_JOB_BRIEF.template.md structure," and that template hard-codes the `.md` suffix directly into its "Local capture path" / "Persistent path" labels (not as a `{{PLACEHOLDER}}` token subject to override) — so any execution that follows the template literally will document (and by BB-003's evidence, likely produce) `.md`-suffixed OE files. But `sop-brief.md`'s **only** retrieval mechanism Globs `**/*.yaml`. A `.md` OE entry is therefore permanently invisible to every future pre-job briefing: the "Operating Experience Findings" section (explicitly flagged throughout the skill as "MANDATORY CONTEXT, not optional reading") would silently show zero entries, `sop-brief` would report "No prior OE entries found" instead of surfacing real deviation history, and the H-2 (Operating Experience Review) nuclear pattern this skill exists to import would be defeated with no error, no warning, and no stop condition anywhere in the design. This is exactly the "Round 2 pre-job brief does not contain Round 1 OE entry" drift signal that BB-003 itself classifies as **Critical** ("OE feedback loop broken; lessons learned not surfacing") — the behavioral baseline designed to catch this failure mode is itself written using the extension that would trigger it.

**Recommendation:**

Standardize on `.yaml` (the majority convention, and the only one consistent with `sop-brief.md`'s literal Glob pattern and the schema being YAML-shaped). Fix `templates/POST_JOB_BRIEF.template.md`'s "Local capture path"/"Persistent path" fields to `.yaml`, and fix all four occurrences in `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` (B-21 code path list, B-24 Glob pattern reference, the "OE Entry Schema Evidence Format" heading example, and the Round 2/3 scenario narration). Add a cross-file consistency check to whatever pre-merge validation this skill relies on (e.g., a grep for `oe-entry-{entry_id}` and `docs/experience/{entry_id}` across the skill tree) so this class of drift is caught mechanically in the future.

---

### S-007-03: QG-HOLD Delegation Wording Contradicts the Agent's Own Tool Restriction and Conflates Two Distinct Agents [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Principle** | P-003 (No Recursive Subagents, HARD); Internal Consistency; Methodological Rigor |
| **Section** | `agents/sop-executor.md` "Hold Point Activation" → QG-HOLD; identical text in `composition/sop-executor.prompt.md` |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

`agents/sop-executor.md` QG-HOLD procedure, step 2 (byte-identical in `composition/sop-executor.prompt.md`):
> "2. Invoke ps-critic via /adversary S-014 with the following context: ..."

Contrast with the same document's own `<capabilities>` section:
> "**Tools NOT Available** — Task: ABSENT. sop-executor is a T2 worker agent. It cannot spawn subagents, delegate to sop-verifier, or invoke any other agent. All agent coordination is the responsibility of the main context orchestrator."

Contrast with the same document's own, correctly-worded IV-HOLD procedure two paragraphs later:
> "5. Return to the main context orchestrator. The orchestrator is responsible for invoking sop-verifier via Task tool with fresh context (no executor reasoning chain passed)."

Contrast with the skill's own worked example/test fixture, `examples/c3-adr-workflow-definition.md`, Step 8 and the "Hold Points Summary" table, which correctly names the actual S-014 implementer per `.context/rules/quality-enforcement.md`:
> "This step invokes /adversary (adv-scorer) via S-014 LLM-as-Judge scoring..." / "Step 8 | QG-HOLD | S-014 score >= 0.92; max 7 iterations | **/adversary adv-scorer**"

The "ps-critic via /adversary S-014" phrasing recurs in `rules/nuclear-sop-behavior-rules.md` (NS-H-03), `SKILL.md` (Quick Reference), `PLAYBOOK.md`, `docs/reference.md`, `docs/howto-guides.md`, and the example row in `templates/HOLD_POINT_LOG.template.md` ("`resolved_by: ps-critic: {score}`").

**Analysis:**

Two distinct problems compound here. First, `sop-executor` has no Task tool by design (correctly stated in its own `<capabilities>` section and reinforced by its `forbidden_actions`), so it *cannot* "invoke" any other agent — the QG-HOLD wording should follow the same "return to main context, which invokes X" pattern the same document uses correctly for IV-HOLD one section later. As written, the QG-HOLD instruction is either inert (an instruction the agent has no tool to carry out) or an implicit invitation to attempt an unauthorized delegation path, which is exactly the P-003 hazard `.context/rules/agent-development-standards.md`'s Pattern 2 (Orchestrator-Worker) exists to prevent. Second, `ps-critic` (a `/problem-solving` creator-critic-loop agent per `AGENTS.md` and `quality-enforcement.md`'s Skill Routing Decision Table: *"Improve this deliverable iteratively" -> /problem-solving (ps-critic)*) is not the same agent as `adv-scorer` (the actual S-014 LLM-as-Judge implementer in `/adversary`, per the same SSOT: *"Score this deliverable against quality gate" -> /adversary (adv-scorer)*). QG-HOLD is a standalone pass/fail scoring gate, not an iterative creator-critic loop — architecturally it should route to `adv-scorer`, exactly as the skill's own worked example independently (and correctly) states. The inconsistency is not cosmetic: an implementer following `SKILL.md`/`nuclear-sop-behavior-rules.md`/`sop-executor.md` literally would route to the wrong skill's wrong agent, while an implementer following the worked example would route correctly — the deliverable disagrees with itself about which of Jerry's two quality-scoring agents backs a HARD rule (NS-H-03).

**Recommendation:**

Rewrite `sop-executor.md`'s QG-HOLD step 2 to mirror the IV-HOLD pattern: *"Return to the main context orchestrator, which invokes `/adversary` (`adv-scorer`) via S-014 with the following context..."*. Propagate the identical fix to `composition/sop-executor.prompt.md`. Then globally replace "ps-critic via /adversary S-014" / "ps-critic" with "`/adversary` (`adv-scorer`)" in `rules/nuclear-sop-behavior-rules.md` (NS-H-03), `SKILL.md`, `PLAYBOOK.md`, `docs/reference.md`, `docs/howto-guides.md`, and the `HOLD_POINT_LOG.template.md` example row, so the skill is internally consistent with its own worked example and with `quality-enforcement.md`'s SSOT agent-to-capability mapping.

---

### S-007-04: NS-H-08's Self-Declared Governance Deadline Has Lapsed Without Resolution or Fallback [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Principle** | P-001 (Truth and Accuracy); Internal Consistency; H-36 (routing circuit breaker) |
| **Section** | `rules/nuclear-sop-behavior-rules.md` NS-H-08; `SKILL.md` "Governance Ruling Pending" |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

`rules/nuclear-sop-behavior-rules.md` NS-H-08:
> "**GOVERNANCE DEADLINE:** H-36 governance ruling tracked as worktracker entity `TASK-0039-H36-RULING` with deadline 60 days from skill registration (2026-06-15). If the ruling eliminates sop-verifier, NS-H-08 is superseded and MUST be revised."

`SKILL.md` "Governance Ruling Pending":
> "If no H-36 ruling is received within 60 days of Phase 1 delivery, the default behavior is 3-hop mode for all criticality levels. sop-verifier is eliminated as a separate agent; sop-capture's integrated IV (Step 0) becomes the permanent verification mechanism for all criticality levels."

`SKILL.md` "STAR Validation Pre-Ship Gate" (same document): *"The /nuclear-sop skill is approved for all criticality levels (C1 through C4)."*

The current review date is 2026-08-07. The stated deadline (2026-06-15) is **~53 days in the past** (June 15 → June 30 = 15 days; July = 31 days; Aug 1–7 = 7 days; 15+31+7 = 53). A live check of `.context/rules/agent-routing-standards.md` (the authoritative, current H-36 specification in this repository) confirms the underlying ambiguity nuclear-sop raised — "whether a predetermined intra-skill verification step (no routing re-evaluation) constitutes a 'hop'" — is still **not addressed** in the framework's actual H-36 text; no ruling appears to exist.

**Analysis:**

The skill ships with a self-imposed, dated "governance clock" and an explicit, unconditional fallback behavior ("the default behavior is 3-hop mode for all criticality levels... sop-verifier is eliminated") that should already have taken effect by the artifact's own logic, since the deadline has passed with (as far as this artifact's contents show) no ruling. Nothing in the reviewed file set reflects this: NS-H-08 still reads as if the deadline were in the future, and `SKILL.md` continues to assert unconditional "APPROVED for all criticality levels (C1 through C4)." This is a truth/accuracy defect distinct from a simple missed deadline — it means a HARD-tier rule governing which verification mode (anchoring-bias-prone 3-hop vs. bias-free 4-hop) is used for C3+/C4 *irreversible* work is currently running in a state the document's own rules say should already have changed. This is precisely the kind of governance staleness a PR review is the correct point to catch before merge.

**Recommendation:**

Before merge: either (a) obtain and record the H-36 ruling explicitly (update `agent-routing-standards.md` or file the governance decision record referenced by `TASK-0039-H36-RULING`, then update NS-H-08 and `SKILL.md` to reflect the resolved interpretation), or (b) apply the self-declared fallback now (3-hop mode becomes the default for all criticality levels; revise NS-H-08, `SKILL.md`, `PLAYBOOK.md`, and `sop-verifier.md`'s status accordingly), or (c) if neither is feasible pre-merge, extend the deadline explicitly with a dated justification and update the "APPROVED for all criticality levels" claim to note the open governance question rather than presenting it as settled.

---

### S-007-05: "Deferred Registration" Note Is Factually False As-Shipped [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Principle** | P-001 (Truth and Accuracy); P-004 (Provenance); H-26(c) (skill registration) |
| **Section** | `SKILL.md` "Registration Content" |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

`SKILL.md`:
> "**DEFERRED REGISTRATION NOTE:** These entries are applied to the live files (`CLAUDE.md`, `AGENTS.md`, `.context/rules/mandatory-skill-usage.md`) AFTER QG-E6 final review gate PASS... The skill is NOT registered and NOT live-routable until QG-E6 passes and the user applies these entries."

Actual state of the same PR's file set: `CLAUDE.md` Quick Reference table already contains the row `| \`/nuclear-sop\` | Nuclear-inspired SOP execution: pre-job brief, STAR self-check, hold points, OE capture |`; `AGENTS.md` already contains a full populated "## Nuclear SOP Skill Agents" section with all four agents; `.context/rules/mandatory-skill-usage.md` already contains the 5-column trigger-map row for `/nuclear-sop` (priority 16).

**Analysis:**

The registration described as future/pending has already happened in this same PR. This is not a hypothetical risk — it is a verifiable, present-tense factual error in the shipped documentation. Left uncorrected, it will mislead a future reader (human or agent) into believing the skill is unregistered, potentially causing someone to "apply" the registration a second time (producing duplicate table rows / trigger-map entries) or to distrust the accuracy of `SKILL.md`'s other claims.

**Recommendation:**

Delete or rewrite the "DEFERRED REGISTRATION NOTE" to reflect the actual state: registration is complete as of this PR; the "Registration Content" section may be retained as a historical record of what was spliced in, but the "NOT registered and NOT live-routable" language must be removed before merge.

---

### S-007-06: `/nuclear-sop` Registered in the Trigger Map but Not in the Enforceable H-22 Rule or L2-REINJECT Comment [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Principle** | H-22 (proactive skill invocation, HARD); H-26(c) |
| **Section** | `.context/rules/mandatory-skill-usage.md` — HARD Rules section and `L2-REINJECT` comment |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

The H-22 rule text in `.context/rules/mandatory-skill-usage.md` enumerates "MUST invoke `/X` for `Y`" for every one of the file's 15 other proactively-invoked skills (`/problem-solving`, `/nasa-se`, `/orchestration`, `/transcript`, `/adversary`, `/ast`, `/eng-team`, `/red-team`, `/pm-pmm`, `/diataxis`, `/prompt-engineering`, `/user-experience`, `/use-case`, `/test-spec`, `/contract-design`) but contains **no clause for `/nuclear-sop`**, even though the Trigger Map table below it gained a full 5-column row for `/nuclear-sop` at priority 16.

The file's `L2-REINJECT` HTML comment (the per-prompt, context-rot-immune enforcement mechanism that `quality-enforcement.md`'s Tier A table lists as the L2 source for H-22) similarly enumerates all 15 other skills by name ("... `/eng-team` for secure engineering... `/contract-design` for API contract generation from use cases producing OpenAPI 3.1 specifications.") but does **not** mention `/nuclear-sop`.

**Analysis:**

`.context/rules/quality-enforcement.md`'s Two-Tier Enforcement Model classifies H-22 as Tier A ("L2 engine-protected... per-prompt re-injection"), meaning its actual enforcement reliability across a long session depends on the L2-REINJECT comment, not merely on the trigger-map table (which is a Layer 1 keyword-matching data structure, useful but not itself the HARD-rule text). By adding only the trigger-map row and skipping the H-22 prose and L2-REINJECT comment, `/nuclear-sop` is registered with weaker, less context-rot-resistant enforcement than every other skill it now sits alongside — a partial, inconsistent application of H-26(c)'s registration requirement ("if proactive per H-22").

**Recommendation:**

Add a `/nuclear-sop` clause to the H-22 HARD-rule sentence (e.g., "MUST invoke `/nuclear-sop` for workflows requiring mandatory pre-execution context loading, step-level compliance verification, named blocking hold points, and structured lessons-capture as required infrastructure.") and add a corresponding short clause to the `L2-REINJECT` comment, consistent with how every other skill in the file is represented.

---

### S-007-07: AGENTS.md Navigation Table and Agent Total Not Updated for the New Section [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Principle** | H-23 (navigation completeness, NAV-004); P-001 (accuracy of the stated total) |
| **Section** | `AGENTS.md` "Document Sections" nav table; "Agent Summary" table |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

`AGENTS.md`'s "Document Sections" navigation table lists 21 entries (Agent Philosophy, Agent Summary, Problem-Solving, NASA SE, Orchestration, Adversary, Worktracker, Transcript, Framework Voice, Session Voice, Eng-Team, Red-Team, PM/PMM, Prompt Engineering, Diataxis, User-Experience, Use Case, Test Spec, Contract Design, MCP Tool Access, Agent Handoff Protocol, Adding New Agents) — it does **not** include an entry for "Nuclear SOP Skill Agents," even though that `##`-level section exists in the document body (inserted between "NASA SE Skill Agents" and "Orchestration Skill Agents").

The "Agent Summary" table lists per-skill counts summing to a stated **Total: 89**, with an explicit verification footnote: *"82 total files found... Per-skill sum: 9 + 10 + 3 + 3 + 3 + 5 + 3 + 1 + 10 + 11 + 5 + 6 + 3 + 11 + 2 + 2 + 2 = 89 invokable agents. Last verified: 2026-03-09."* This arithmetic and the 2026-03-09 verification date both predate the four `sop-*` agents (`sop-verifier.md` itself is dated "Created: 2026-03-26"). The table has no row for "Nuclear SOP Agents | 4 |," and the total is not updated to 93.

**Analysis:**

This is a straightforward, mechanically verifiable completeness gap in one of the four registration surfaces explicitly in scope for this review. `markdown-navigation-standards.md` NAV-004 ("Coverage: All major sections (`##` headings) SHOULD be listed") is a MEDIUM-tier standard; the omission itself is not a HARD-rule breach (H-23's core requirement — that a nav table exist at all — is satisfied) but it is a real, user-facing accuracy defect: a reader trusting the "Total: 89" figure or navigating via the table will not find or count the newly added agents.

**Recommendation:**

Add `| [Nuclear SOP Skill Agents](#nuclear-sop-skill-agents) | sop-* agents (4 total) |` to the navigation table in the position matching the body's actual heading order (after NASA SE, before Orchestration). Add a `| Nuclear SOP Agents | 4 | /nuclear-sop skill |` row to "Agent Summary," and update the total to **93**, refreshing the verification arithmetic and the "Last verified" date.

---

### S-007-08: STAR Validation Evidence Is a Same-Team Simulated Walkthrough, Presented Without That Caveat in SKILL.md [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Principle** | P-011 (Evidence-Based Decisions); Evidence Quality |
| **Section** | `SKILL.md` "STAR Validation Pre-Ship Gate"; `«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/validation/qg-e4/star-validation-results.md` |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

The validation report itself is transparent about its method: *"Produced by: eng-qa (Security QA Engineer) / Method: Empirical simulation -- STAR walkthrough against three deliberate error traps in the worked example... Confidence: High -- all detection signals are grounded in explicit text citations..."* This is a reasoned textual walkthrough of what the `sop-executor.md` specification says the agent *should* do when it encounters each trap — not a transcript of an actual model invocation executing the workflow definition live.

`SKILL.md`'s "STAR Validation Pre-Ship Gate" reproduces the result — *"QG-E4 STAR A/B validation PASSED on 2026-04-20 with 3/3 catch rate (100%)... Result: PASS — 3/3 catch rate (100%)."* — without carrying forward the "empirical simulation" / walkthrough caveat from the source report.

**Analysis:**

The underlying report is itself honest and well-evidenced (P-021 compliant at the source), and this finding is not a claim that the STAR mechanism is ineffective. The concern is narrower: `SKILL.md` is the document most readers will consult, and it presents "PASS — 3/3 catch rate" with the rhetorical weight of an executed test, when the actual methodology is closer to a design review / spec-trace exercise performed by the same team that wrote the specification being traced (a validity threat the report does not fully address: would an independently-prompted model, without the trap annotations and "TEST HARNESS -- TRAP-0N EXPECTED STAR RESPONSE" blocks visible in the fixture, actually reproduce this reasoning chain unprompted?). This gap in independence is exactly the sort of thing `docs/reference.md`'s SD-05 metadata-review pattern and the skill's own repeated P-022 disclosures elsewhere are designed to surface — but it is not surfaced here.

**Recommendation:**

Add one sentence to `SKILL.md`'s "STAR Validation Pre-Ship Gate" noting the validation methodology (same-team simulated walkthrough against a fixture containing visible expected-response blocks, not an independent live-model execution), consistent with the skill's own transparency pattern used for STAR's "behavioral not deterministic" limitation elsewhere. Consider recommending an independent, blind re-run (fresh session, trap annotations stripped of "TEST HARNESS -- EXPECTED STAR RESPONSE" blocks) as a follow-up validation item.

---

### S-007-09: Inconsistent Template Placeholder Convention Across the 4 Markdown Templates [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Principle** | Internal Consistency |
| **Section** | `templates/PRE_JOB_BRIEF.template.md` vs. `templates/POST_JOB_BRIEF.template.md`, `templates/WORKFLOW_DEFINITION.template.md`, `templates/HOLD_POINT_LOG.template.md` |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

`PRE_JOB_BRIEF.template.md` uses Handlebars-style double-brace placeholders with conditionals, explicitly documented in `sop-brief.md`: *"Template conditional evaluation: The template uses Handlebars-style conditionals (`{{#if CONDITION}}...{{/if}}`)... evaluated by the agent during brief generation."* e.g. `{{WORKFLOW_NAME}}`, `{{#if PREREQ_WAIVED}}...{{/if}}`.

`POST_JOB_BRIEF.template.md`, `WORKFLOW_DEFINITION.template.md`, and `HOLD_POINT_LOG.template.md` all use plain single-brace static placeholders with no conditional syntax, e.g. `{workflow_id}`, `{WORKFLOW_TITLE}`, `{WORKFLOW_ID}`.

**Analysis:**

This is a low-impact but genuine inconsistency: only `sop-brief.md` documents a templating convention at all (Handlebars-style, for the one template it consumes); `sop-capture.md`, `sop-executor.md` give no equivalent guidance for interpreting the single-brace placeholders in the templates they consume, and none of the four templates cross-reference a shared convention. This does not by itself break functionality (an LLM agent can reasonably infer "fill in the placeholder" either way), but it is inconsistent authoring practice within a single skill that otherwise documents its conventions carefully (e.g., the `[CONTINUOUS]`/`[REFERENCE]`/`[INFORMATION]` annotation legend is repeated verbatim and consistently in four separate files).

**Recommendation:**

Either standardize all four templates on one placeholder convention, or add a one-line note to each of the three single-brace templates (mirroring `sop-brief.md`'s existing note for `PRE_JOB_BRIEF.template.md`) stating that placeholders are plain substitution tokens with no conditional syntax.

---

## Remediation Plan

**P0 (Critical — MUST fix before acceptance):**
- S-007-01: Implement `state_hash` compute/verify in `sop-executor.md` STAR-STOP, or explicitly mark it `[NOT YET IMPLEMENTED]` in `docs/reference.md` and the template.
- S-007-02: Standardize OE entry extension on `.yaml` across `POST_JOB_BRIEF.template.md` and `bb-003-oe-feedback-loop-integrity.md`.

**P1 (Major — SHOULD fix; require documented justification if not):**
- S-007-03: Rewrite QG-HOLD delegation wording in `sop-executor.md`/`sop-executor.prompt.md` to match the IV-HOLD "return to main context" pattern; standardize on "`/adversary` (`adv-scorer`)" everywhere `ps-critic via /adversary S-014` currently appears.
- S-007-04: Resolve, apply the fallback for, or explicitly extend-with-justification the lapsed NS-H-08 / H-36 governance deadline before claiming unconditional C1–C4 approval.
- S-007-05: Correct or remove the "DEFERRED REGISTRATION NOTE" in `SKILL.md`; registration is already complete.
- S-007-06: Add a `/nuclear-sop` clause to the H-22 rule prose and the `L2-REINJECT` comment in `mandatory-skill-usage.md`.
- S-007-07: Add the missing nav-table entry and correct the Agent Summary total (89 → 93) in `AGENTS.md`.

**P2 (Minor — CONSIDER fixing):**
- S-007-08: Add a methodology caveat to `SKILL.md`'s STAR validation summary.
- S-007-09: Standardize or document the template placeholder convention across all four templates.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-007-02 (OE loop silently non-functional), S-007-06 (H-22/L2-REINJECT registration incomplete), S-007-07 (AGENTS.md nav/count incomplete) |
| Internal Consistency | 0.20 | Negative | S-007-02, S-007-03, S-007-04, S-007-05, S-007-09 — the deliverable disagrees with itself across multiple file pairs on functionally load-bearing details |
| Methodological Rigor | 0.20 | Negative | S-007-01 (claimed control not implemented), S-007-03 (delegation model violates the agent's own stated tool restriction) |
| Evidence Quality | 0.15 | Negative | S-007-01 (unverifiable/false claim), S-007-08 (validation methodology caveat omitted at point of citation) |
| Actionability | 0.15 | Neutral | No findings reduce the deliverable's own actionability; all 9 findings here include specific, file-anchored remediations |
| Traceability | 0.10 | Negative | S-007-04 (governance deadline tracked but not visibly resolved/traced), S-007-07 (agent count/registry traceability stale) |

---

## Constitutional Compliance Score

**Violation distribution:** N_critical = 2, N_major = 5, N_minor = 2

**Penalty calculation:** `1.00 - (0.10 × 2 + 0.05 × 5 + 0.02 × 2)` = `1.00 - (0.20 + 0.25 + 0.04)` = `1.00 - 0.49` = **0.51**

**Threshold determination:** **REJECTED** (< 0.85 band; far below the H-13 gate of 0.92)

---

## Strategy Verdict

This S-007 Constitutional AI Critique found the `/nuclear-sop` skill to be **NON-COMPLIANT** at a constitutional level, driven by two Critical findings that are not stylistic or speculative but concrete, falsifiable defects: a named security/integrity control (`state_hash` tamper detection) is documented as implemented and verified "before every tool call" yet appears nowhere in the executing agent's actual STAR-STOP methodology, and a file-extension mismatch between the OE-write path (`.yaml`, used consistently by the write-side agent and the SSOT rules) and the OE-write path shown in the post-job-brief template and the skill's own OE-integrity behavioral baseline (`.md`) would silently defeat the mandatory Operating Experience feedback loop that this skill exists to provide — with no error, warning, or stop condition to surface the failure. Five further Major findings compound the picture: a QG-HOLD delegation instruction that both contradicts the agent's own no-Task-tool restriction and misnames the actual `/adversary` scoring agent (contradicted by the skill's own worked example), a self-declared H-36 governance deadline that has already lapsed by about seven weeks without visible resolution while the skill continues to assert unconditional C1–C4 approval, a "deferred registration" claim in SKILL.md that is factually false against the PR's own already-populated registration surfaces, an H-22/L2-REINJECT registration gap that leaves this skill's proactive-invocation enforcement weaker than its peers, and an AGENTS.md navigation/count omission. None of these findings are about the skill's ambition or design philosophy, which is coherent and well-researched (INPO/NRC-sourced patterns, an honestly-disclosed STAR behavioral-not-deterministic limitation, a genuinely well-designed context-isolated `sop-verifier`); the findings are about the deliverable's truthfulness and internal consistency at the level of specific, checkable claims — exactly what a Constitutional AI critique is designed to surface before merge. Constitutional Compliance Score: **0.51 (REJECTED)**. Recommendation: **REJECT** pending remediation of S-007-01 and S-007-02 (mandatory) and the five Major findings (strongly recommended before this skill is trusted for C3+/C4 use).

# Devil's Advocate Report: /nuclear-sop Skill (PR #269)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverable, blindness/H-16 disclosure |
| [Role Assumption](#role-assumption) | Step 1 -- advocate role, scope, criticality |
| [Summary](#summary) | Overall verdict and recommendation |
| [Assumption Inventory](#assumption-inventory) | Step 2 -- explicit/implicit assumptions challenged |
| [Findings Summary](#findings-summary) | All findings at a glance |
| [Detailed Findings](#detailed-findings) | Full counter-argument per finding with evidence |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized response requirements |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 six dimensions |
| [Strategy Verdict](#strategy-verdict) | One-paragraph overall assessment |
| [Execution Statistics](#execution-statistics) | Protocol completion record |

---

## Execution Context

| Field | Value |
|-------|-------|
| **Strategy** | S-002 (Devil's Advocate) |
| **Template** | `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0 |
| **Deliverable** | `/nuclear-sop` skill, PR #269, branch `proj-0039-nuclear-engineer`, head commit `bda64202` -- all 31 files under `skills/nuclear-sop/` plus registration surfaces (`.claude-plugin/plugin.json`, `CLAUDE.md`, `AGENTS.md`, `.context/rules/mandatory-skill-usage.md`, `CHANGELOG.md`) |
| **Criticality** | C4 (full tournament) |
| **Executed** | 2026-08-07 |
| **Reviewer** | adv-executor (background tournament agent, Challenge group) |
| **Finding ID format** | `S-002-NN` per orchestrator instruction (maps to template's `DA-NNN-{execution_id}` convention; `execution_id = 20260807`) |

**H-16 Compliance (disclosed, not independently verified):** This execution ran as an isolated blind background agent. Per explicit orchestrator instruction, this agent did not read `projects/PROJ-032-nuclear-sop-review/` (including any prior strategy outputs) and cannot directly confirm that S-003 (Steelman) completed beforehand. The tournament's documented group order (self-refine -> steelman -> challenge -> verify -> decompose -> score, sequential between groups) places Steelman in the group immediately preceding this Challenge-group execution, so H-16 ordering is understood to be enforced by the orchestrator rather than independently confirmed by this agent. This is disclosed per P-022 rather than silently assumed.

**Scope note:** All findings below are sourced from files inside the reviewed PR snapshot only (the `skills/nuclear-sop/` tree, the 5 registration surfaces, and -- because the deliverable's own text repeatedly cites them as the evidentiary basis for its safety claims -- three files from the PR's own build-provenance tree at `«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/`). No file outside the PR snapshot was consulted. Current-Jerry-standard comparisons (H-13 through H-36) were read from this worktree's `.context/rules/` and `docs/governance/`, never from the PR's copies.

---

## Role Assumption

Deliverable under challenge: the `/nuclear-sop` skill's central thesis is that it imports "50+ years of nuclear power plant SOP methodology" to make AI agent procedure execution safer -- specifically via mandatory pre/post-execution phases, STAR self-checking, three tiers of hold points, and context-isolated independent verification (`sop-verifier`) for C3+ work. The skill claims (SKILL.md, "STAR Validation Pre-Ship Gate") that this has been empirically validated and is "approved for all criticality levels (C1 through C4)."

Advocate mandate for this execution: find the strongest evidence-based reasons the deliverable's safety and readiness claims are wrong, incomplete, or overstated -- using the deliverable's own artifacts as the primary source of contradicting evidence, per the "contradicting evidence" and "historical precedents of failure" counter-argument lenses.

---

## Summary

8 counter-arguments identified (3 Critical, 3 Major, 2 Minor). The skill's architecture, documentation depth, and C1/C2 execution path are comparatively well-constructed and unusually well self-documented -- ironically, that same documentation trail is what exposes the Critical findings. Three Critical findings show the deliverable's own build-pipeline artifacts directly contradicting its headline claims: an unremediated, self-identified RPN-144 security gap in the independent-verification agent that the project's own compliance review named as a blocking condition for C3+ use (S-002-01); a "registration deferred until QG-E6 passes and the user applies it" claim that is contradicted by the PR's own changeset, which already applies the registration (S-002-02); and an "empirically validated" STAR safety claim that rests on a single self-authored narrative walkthrough rather than a live behavioral trial (S-002-03). **Recommend REVISE:** the "approved for all criticality levels (C1 through C4)" claim should not stand as currently worded until the Critical findings are resolved or the claim is explicitly narrowed to match the artifact's own previously-documented conditions.

---

## Assumption Inventory

| # | Assumption (explicit/implicit) | Source | Challenge outcome |
|---|--------------------------------|--------|--------------------|
| A-1 | "The STAR self-checking protocol has been empirically validated" | SKILL.md, "STAR Validation Pre-Ship Gate" | Challenged -- S-002-03: the validation is a self-authored narrative, not a live trial |
| A-2 | "The /nuclear-sop skill is approved for all criticality levels (C1 through C4)" | SKILL.md | Challenged -- S-002-01: a self-identified RPN-144 blocking finding in the exact C3+ safety mechanism was never remediated |
| A-3 | "The skill is NOT registered and NOT live-routable until QG-E6 passes and the user applies these entries" (registration is deferred, user-gated) | SKILL.md, "Registration Content" | Challenged -- S-002-02: this PR's own `CLAUDE.md`/`AGENTS.md`/`mandatory-skill-usage.md`/`plugin.json` already contain the full splice |
| A-4 | The single worked-example fixture is a reliable, internally consistent test instrument | `examples/c3-adr-workflow-definition.md` | Challenged -- S-002-04: the fixture's own TRAP-01 WARNING names two different "wrong paths" |
| A-5 | The three "behavioral baselines" (BB-001/002/003) are live, maintained regression references | `behavioral-baselines/` | Challenged -- S-002-05: BB-003 disagrees with 6 other shipped files on the OE file extension, and would fail if actually run |
| A-6 | Same-framework, same-model self-scoring (QG-E1 through QG-E6, all via Jerry `/adversary` agents) is sufficient assurance for a "nuclear-grade" safety skill | Build-provenance tree | Challenged -- S-002-08: no external/human review is disclosed anywhere in the skill's user-facing security documentation |
| A-7 | The two parallel "canonical" agent definitions (`agents/*.md` and `composition/*.prompt.md`) stay in sync | `agents/`, `composition/` | Challenged -- S-002-07: the SEC-008 defect is duplicated, with slightly different wording, in both copies |
| A-8 | The H-36 governance contingency will resolve before it matters | SKILL.md, `nuclear-sop-behavior-rules.md` NS-H-08 | Challenged -- S-002-06: the stated 60-day deadline (2026-06-15) has already passed as of this review (2026-08-07) with no resolution disclosed in the deliverable |

---

## Findings Summary

| ID | Severity | Finding | File | Dimension |
|----|----------|---------|------|-----------|
| S-002-01 | Critical | Self-identified RPN-144 "OPEN -- REMEDIATION REQUIRED" defect in `sop-verifier`'s hold-point check is still present verbatim in shipped code, yet the skill claims unconditional C1-C4 approval | `skills/nuclear-sop/agents/sop-verifier.md` | Internal Consistency |
| S-002-02 | Critical | SKILL.md's "registration deferred until user applies it" claim is contradicted by this PR's own changeset, which already splices the registration | `skills/nuclear-sop/SKILL.md` | Internal Consistency / Traceability |
| S-002-03 | Critical | The sole "empirical" STAR safety validation is a self-authored narrative walkthrough, not a live behavioral trial, yet it gates C3/C4 approval | `«PR projects tree»/PROJ-0039-nuclear-engineer/.../validation/qg-e4/star-validation-results.md` | Evidence Quality / Methodological Rigor |
| S-002-04 | Major | The sole empirical test fixture contains an internal path inconsistency in its own TRAP-01 annotation | `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` | Evidence Quality |
| S-002-05 | Major | Behavioral baseline BB-003 (a claimed quality/regression mechanism) disagrees with 6 other shipped files on the OE file extension and would fail if run | `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` | Internal Consistency / Methodological Rigor |
| S-002-06 | Major | NS-H-08's self-declared H-36 governance deadline (2026-06-15) has already lapsed with no resolution disclosed, leaving the C3+ 4-hop HARD-rule mandate's current status ambiguous | `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` | Internal Consistency / Traceability |
| S-002-07 | Minor | Dual "canonical" agent-definition sources (`agents/` vs. `composition/`) duplicate the exact defect surfaced in S-002-01, with drifted wording between copies | `skills/nuclear-sop/composition/sop-verifier.prompt.md` | Methodological Rigor |
| S-002-08 | Minor | No disclosure that all build-pipeline quality gates (QG-E1 through QG-E6) were self-scored by same-framework agents with no external/human reviewer | `skills/nuclear-sop/SKILL.md` | Evidence Quality / Traceability |

---

## Detailed Findings

### S-002-01: SEC-008 unremediated -- "if accessible" hold-check defect still ships, while the skill claims unconditional C1-C4 approval [CRITICAL]

**Claim Challenged:** SKILL.md, "STAR Validation Pre-Ship Gate": *"The /nuclear-sop skill is approved for all criticality levels (C1 through C4)."* Reinforced in `nuclear-sop-behavior-rules.md` NS-H-08: *"QG-E4 PASSED (2026-04-20, 3/3 catch rate) — C3+ is APPROVED for all criticality levels."*

**Counter-Argument:** The project's own final compliance-verification report (produced within this PR's build provenance) explicitly conditioned C3+ approval on remediating a named, RPN-144 defect in `sop-verifier`'s hold-point consistency check. That exact defect is still present, unchanged, in the code shipped by this PR. The "approved for all criticality levels" claim is therefore not merely optimistic -- it is falsified by evidence the deliverable's own build pipeline produced.

**Evidence:**

`«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/compliance-verification.md` (QG-E6, dated 2026-04-14):
> "SEC-008 | -- | sop-verifier Step 6 hold check conditional skip | 144 | 36 (projected) | **OPEN -- REMEDIATION REQUIRED** | RPN 144 (> 100 threshold). This is a QG-E5 CONDITIONAL PASS condition. `sop-verifier.md` lines 155-161 still use "if accessible" conditional formulation. **Must be changed to mandatory with anomaly recording before C3+ use.**"

Same document, "Open Items -- Priority 1: SEC-008 Remediation (blocks C3+ use)" gives the exact required replacement text (mandatory access attempt + `PROCEDURE_STATE_NOT_FOUND` anomaly on absence), and its L0 states: *"C3+ use is blocked until two pre-ship conditions are met... 1. SEC-008 OPEN... 2. QG-E4 UNRESOLVED."*

The **currently shipped** `skills/nuclear-sop/agents/sop-verifier.md` (Step 6, "Check PROCEDURE_STATE.yaml for Hold Point Consistency (SD-03)") reads, verbatim:
> "If `PROCEDURE_STATE.yaml` is accessible (path discoverable from the workflow definition's directory):
> - Cross-reference the hold points defined in the workflow definition against the hold point activations recorded in PROCEDURE_STATE.yaml
> - If a hold point defined in the workflow definition has no corresponding activation record in PROCEDURE_STATE.yaml: record `HOLD_POINT_NOT_ACTIVATED` anomaly"

This is the exact unremediated text the compliance report quoted as the defect (silent skip, no anomaly recorded, when the state file is simply "not accessible"). The identical substantive gap also appears in `skills/nuclear-sop/composition/sop-verifier.prompt.md` Step 6 (see S-002-07).

Meanwhile, neither `skills/nuclear-sop/SKILL.md` nor `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` -- the two files a user or reviewer would actually read to learn the skill's current approval status -- mentions SEC-008 anywhere. Both currently assert unconditional C1-C4 approval.

**Impact:** `sop-verifier` is the mechanism this skill relies on to justify C3+/C4 use over the cheaper C1-C2 3-hop mode (the whole point of paying the extra hop and context cost is independent, anomaly-recording verification). A silent no-op on missing state is precisely the failure mode an adversarial or degraded execution would exploit to make hold-point bypass invisible to the one check designed to catch it. Approving C4 (irreversible/architecture-wide) use on this mechanism, without disclosing that its own security review has not accepted it, materially overstates the deliverable's readiness.

**Dimension:** Internal Consistency (primary); also Completeness (the gap disappeared from the record rather than being closed).

**Response Required:** Either (a) apply the exact remediation text already drafted in the compliance report's Priority-1 item to both `agents/sop-verifier.md` and `composition/sop-verifier.prompt.md`, and add a `PROCEDURE_STATE_NOT_FOUND`-trap regression check; or (b) revise SKILL.md and `nuclear-sop-behavior-rules.md` to re-disclose the SEC-008 condition explicitly and narrow the current approval to C1-C2 only until it closes.

**Acceptance Criteria:** `sop-verifier.md` Step 6 (both copies) treats `PROCEDURE_STATE.yaml` access as required and records a `PROCEDURE_STATE_NOT_FOUND` anomaly on absence, matching the disposition logic already drafted in the compliance report -- OR the "approved for all criticality levels" language is replaced with an explicit CONDITIONAL statement naming SEC-008 as open, in both SKILL.md and NS-H-08.

---

### S-002-02: "Registration deferred until QG-E6 passes and the user applies it" is contradicted by this PR's own changeset [CRITICAL]

**Claim Challenged:** SKILL.md, "Registration Content": *"DEFERRED REGISTRATION NOTE: These entries are applied to the live files (`CLAUDE.md`, `AGENTS.md`, `.context/rules/mandatory-skill-usage.md`) AFTER QG-E6 final review gate PASS. They are provided here as copy-ready content for that step. The skill is NOT registered and NOT live-routable until QG-E6 passes and the user applies these entries. Per P-020, the actual splicing is performed by the user, not by an agent."*

**Counter-Argument:** This PR's own registration surfaces already contain the full splice described as pending. Either the disclosure is stale/false about the state of the artifact under review, or the splice was performed by something other than the user as SKILL.md itself insists is required.

**Evidence:**

- `CLAUDE.md` (this PR), Skills table: `| `/nuclear-sop` | Nuclear-inspired SOP execution: pre-job brief, STAR self-check, hold points, OE capture |` -- already present, matching the "copy-ready" row SKILL.md's Registration Content section says is not yet applied.
- `AGENTS.md` (this PR) already contains a full "## Nuclear SOP Skill Agents" section with the 4-agent table.
- `.context/rules/mandatory-skill-usage.md` (this PR) already contains the complete 5-column trigger-map row for `/nuclear-sop` (priority 16, full keyword/negative-keyword/compound-trigger set).
- `.claude-plugin/plugin.json` (this PR) already lists all four `./skills/nuclear-sop/agents/sop-*.md` entries in the top-level `agents` array.
- `CHANGELOG.md` (this PR), `[Unreleased] > Added`: *"`/nuclear-sop` skill — ... agents registered in plugin.json (#269)"* -- the changelog itself describes registration as already done, in the same breath as introducing the skill.

**Impact:** A reviewer relying on SKILL.md's plain-text claim would conclude the skill is not yet live-routable and that a manual, user-gated step remains -- which is false for the artifact actually being merged. This is exactly the kind of claim-vs-artifact mismatch that should concern a reviewer of a *governance* file: either SKILL.md is wrong about the PR's own contents (a P-022 concern), or an agent performed a splice into root governance files that SKILL.md explicitly says only a user may perform (a P-020 process question). Both readings undermine confidence in the reliability of this skill's self-reported state, which is the same self-reporting mechanism underpinning S-002-01 and S-002-03.

**Dimension:** Internal Consistency / Traceability.

**Response Required:** Reconcile the claim with reality: either remove/rewrite the "DEFERRED REGISTRATION" language to reflect that registration is final (and confirm who performed it and when), or revert the four registration splices until the described QG-E6-then-user-applies sequence actually happens as described.

**Acceptance Criteria:** SKILL.md's Registration Content section text matches the actual state of `CLAUDE.md`/`AGENTS.md`/`mandatory-skill-usage.md`/`plugin.json` in the same changeset, with an explicit statement of who performed the splice.

---

### S-002-03: The "empirically validated" STAR safety claim rests on a single self-authored narrative, not a live trial [CRITICAL]

**Claim Challenged:** SKILL.md: *"QG-E4 STAR A/B validation PASSED on 2026-04-20 with 3/3 catch rate (100%)... The STAR self-checking protocol has been empirically validated: STAR-ON caught all 3 deliberate error traps... STAR-OFF caught 0/3."*

**Counter-Argument:** "Empirically validated" implies an observed behavioral trial. What was actually produced is a single hand-authored (or single-LLM-authored) narrative asserting what the STAR protocol *would* log if read faithfully, written by the same methodology that designed the traps, with no independent tester, no live invocation of the actual `sop-executor` agent, no multiple trials, and no adversarial variation. This is a materially weaker evidentiary basis than the word "empirical" and the go/no-go pre-ship gate framing suggest.

**Evidence:**

`«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/validation/qg-e4/star-validation-results.md`, footer:
> *"Method: Empirical simulation -- STAR walkthrough against three deliberate error traps in the worked example. Each STAR phase executed exactly as specified in sop-executor.md lines 144-197 and nuclear-sop-behavior-rules.md STAR Protocol section."*
> *"Confidence: High -- all detection signals are grounded in explicit text citations from the workflow definition, sop-executor.md, and nuclear-sop-behavior-rules.md. No judgment calls required."*

"Condition B -- STAR-OFF Baseline" in the same document is explicitly speculative, not observed: *"Would a non-STAR executor catch this?... Non-STAR catch rate for TRAP-01: Unlikely."* -- hedged predictions, not a transcript of an actual non-STAR run.

"Empirical simulation" is presented as if it were a controlled experiment ("Condition A" vs. "Condition B"), and SKILL.md reproduces the 100%/0% figures as if they were measured outcomes, then uses that single artifact to lift the skill's own previously-documented C3+ restriction (see SKILL.md: *"If QG-E4 PASSES | **PASSED (2026-04-20).** C3+ restriction lifted"*).

**Impact:** The entire risk case for using this skill at C3/C4 (irreversible, architecture-wide work) rests on STAR actually catching injected/adversarial deviations under real model sampling variance -- not on a narrator correctly predicting that a documented protocol, read faithfully, would behave as documented. A genuinely adversarial validation would use traps authored by a party other than the validator and record a real Task-tool invocation's output. As written, the "100% catch rate" is a self-consistency check on the specification, not a safety measurement of the agent.

**Dimension:** Evidence Quality (primary); Methodological Rigor.

**Response Required:** Either re-run QG-E4 as a genuine behavioral test (live `sop-executor` invocation against the fixture, ideally with traps authored independently of the validator, transcript retained), or relabel the current artifact honestly (e.g., "specification walkthrough; live validation pending") in SKILL.md and `nuclear-sop-behavior-rules.md`, consistent with this same skill's own P-022 commitment ("sop-executor does not claim to prevent all errors... this limitation is disclosed per P-022").

**Acceptance Criteria:** Either a transcript of a live, adversarially-authored STAR trial replaces or supplements the narrative walkthrough, or every occurrence of "empirically validated" / "PASSED" tied to QG-E4 is qualified to accurately describe a specification walkthrough rather than an observed trial.

---

### S-002-04: The sole empirical test fixture contradicts itself about which path is the deliberate trap [MAJOR]

**Claim Challenged:** star-validation-results.md's claim that TRAP-01 detection is grounded in unambiguous, explicitly-cited fixture text: *"WARNING annotation in Step 6 explicitly named `docs/design/ADR-NNN.md` as the ERROR TRAP path and named the correct path as `work/adr-authoring-c3-001/drafts/ADR-NNN-draft.md`. Source: `c3-adr-workflow-definition.md:235-246`."*

**Counter-Argument:** The cited WARNING block does not consistently name one wrong path -- it names two different ones in three consecutive sentences, and the validation report's citation silently picks the one that supports its narrative.

**Evidence:**

`skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, Step 6 (as shipped):
> "> **WARNING:** This step writes to `projects/{JERRY_PROJECT}/decisions/ADR-NNN.md`.
> The previous step (Step 5) produced draft content at `work/adr-authoring-c3-001/drafts/ADR-NNN-draft.md`.
> Writing draft content directly to `docs/design/` bypasses the mandatory quality gate (Step 8) and user approval (Step 12). The correct target for this validation step is `work/adr-authoring-c3-001/drafts/ADR-NNN-draft.md`.
>
> **ERROR TRAP (TRAP-01):** The Target field below specifies `docs/design/ADR-NNN.md` (the FINAL placement path)..."

The first sentence names `projects/{JERRY_PROJECT}/decisions/ADR-NNN.md` as "This step writes to." The third sentence and the ERROR TRAP callout (plus the step's actual `**Target:**` field) instead name `docs/design/ADR-NNN.md`. These are two different paths for what is supposed to be one deliberately-specified wrong path.

**Impact:** This does not itself demonstrate a runtime safety failure, but it does undercut the "no judgment calls required" confidence claim of the validation report that Finding S-002-03 already questions on methodology grounds: the one artifact meant to be unambiguous by design is not internally consistent, and the validator's citation did not surface the inconsistency.

**Dimension:** Evidence Quality.

**Response Required:** Correct the WARNING text in Step 6 so both mentions agree on the trap path, and re-verify the validation report's citation against the corrected text.

**Acceptance Criteria:** `c3-adr-workflow-definition.md` Step 6's WARNING names a single, consistent wrong path throughout; `star-validation-results.md`'s TRAP-01 evidence citation is re-confirmed against the corrected text.

---

### S-002-05: Behavioral baseline BB-003 disagrees with 6 other shipped files and would fail its own stated regression purpose [MAJOR]

**Claim Challenged:** BB-003's stated purpose: *"GAP-09 Purpose: Establishes the behavioral reference for the OE feedback loop... Used to detect drift in the feedback loop temporal attack surface... Regression Trigger Conditions: Re-run BB-003 after any of the following changes."* -- i.e., BB-003 is presented as a live, checkable regression reference for the current implementation.

**Counter-Argument:** BB-003 itself is inconsistent with the implementation it is supposed to baseline, on a simple, mechanically-checkable fact (file extension). If BB-003 had ever actually been run against the current codebase, this mismatch would surface immediately.

**Evidence:**

`skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`:
> "**B-21: OE entry written to BOTH locations** ... 1. `capture/oe-entry-{entry_id}.md` -- local capture directory. 2. `docs/experience/{entry_id}.md` -- persistent OE registry."
> "**B-24: OE entries loaded as mandatory context...** sop-brief must retrieve all OE entries... using: 1. Primary: `Glob: docs/experience/*.md`..."

Six other shipped files in the same PR all agree on `.yaml`, not `.md`:
- `skills/nuclear-sop/agents/sop-capture.md`: *"Write OE entry to TWO locations... 1. `capture/oe-entry-{entry_id}.yaml`... 2. `docs/experience/{entry_id}.yaml`..."*
- `skills/nuclear-sop/composition/sop-capture.prompt.md`: identical `.yaml` paths.
- `skills/nuclear-sop/agents/sop-brief.md`, Step 4: `Glob(pattern="<oe_search_path>/**/*.yaml")`.
- `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, OE Search Mechanism: `Glob docs/experience/*.yaml`, and dual-write description: `docs/experience/{entry_id}.yaml`.
- `skills/nuclear-sop/docs/reference.md`: `Glob docs/experience/*.yaml` and `docs/experience/{entry_id}.yaml` throughout.
- `skills/nuclear-sop/docs/tutorial-getting-started.md`: expected tutorial output is `docs/experience/oe-dec-log-001.yaml`.

A second, independent occurrence of the same `.md` drift also exists in `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md`: *"**Persistent path (future sop-brief retrieval):** `docs/experience/{entry_id}.md`."*

This echoes, but is distinct from, the historical SEC-011 finding in the build provenance (which flagged `.yaml` vs. `.md` drift between `nuclear-sop-behavior-rules.md` and `sop-capture.md` at an earlier point in the build; that specific pairing is now internally consistent at `.yaml`, but the inconsistency has resurfaced independently in BB-003 and the template).

**Impact:** BB-003 and POST_JOB_BRIEF.template.md would produce visibly wrong guidance (Glob patterns that never match; paths that are never written) if used as-is. More importantly, this is exactly the kind of one-line, grep-detectable defect that the "S-010 Self-Review... PASS" checklist in the compliance-verification report (which lists "All claims cite specific file paths and line numbers" and "No overclaiming of safety properties" as PASS) should have caught, and did not -- across a 19+-file skill whose selling point is procedural rigor.

**Dimension:** Internal Consistency (primary); Methodological Rigor.

**Response Required:** Correct `.md` to `.yaml` in BB-003 and `POST_JOB_BRIEF.template.md` (or, if `.md` is actually the intended future format, update the 6 agreeing files instead), and add a basic cross-file grep check for `docs/experience/*.{yaml,md}` consistency to the skill's own pre-registration checklist.

**Acceptance Criteria:** All 8+ references to the OE entry file extension across the skill's shipped files agree.

---

### S-002-06: NS-H-08's self-declared H-36 governance deadline has already passed with no resolution disclosed [MAJOR]

**Claim Challenged:** `nuclear-sop-behavior-rules.md`, NS-H-08 (a HARD rule): *"C3+ workflows MUST use 4-hop mode... The 3-hop mode... is PROHIBITED for C3+ criticality until a governance ruling permits it. **GOVERNANCE DEADLINE:** H-36 governance ruling tracked as worktracker entity `TASK-0039-H36-RULING` with deadline 60 days from skill registration (2026-06-15). If the ruling eliminates sop-verifier, NS-H-08 is superseded and MUST be revised. Until that revision is completed, NS-H-08 remains as written."* Mirrored in SKILL.md: *"Governance ruling deadline: If no H-36 ruling is received within 60 days of Phase 1 delivery, the default behavior is 3-hop mode for all criticality levels. sop-verifier is eliminated as a separate agent."*

**Counter-Argument:** The deliverable names its own hard fallback date. That date (2026-06-15) is approximately 53 days before this review (2026-08-07), per the deliverable's own explicit text -- yet nothing in the reviewed file set indicates a ruling was received, and nothing reflects the self-declared fallback (3-hop-only, `sop-verifier` eliminated) having taken effect either. The shipped artifact is therefore ambiguous, by its own stated logic, about whether NS-H-08 -- the HARD rule that Finding S-002-01's entire severity argument depends on ("C3+ MUST use 4-hop mode... `sop-verifier`") -- is still the operative rule.

**Evidence:**

`skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, NS-H-08 (quoted above, verbatim "GOVERNANCE DEADLINE" text with the explicit date "2026-06-15").

`skills/nuclear-sop/SKILL.md`, "H-36 Circuit Breaker Compliance -- Governance Ruling Pending": *"A governance request has been filed: whether a predetermined intra-skill verification step... constitutes a 'hop' under H-36... If no H-36 ruling is received within 60 days of Phase 1 delivery, the default behavior is 3-hop mode for all criticality levels."*

No file in the reviewed set (SKILL.md, PLAYBOOK.md, behavior rules, any agent or governance file) states that `TASK-0039-H36-RULING` was resolved, closed, or superseded, and none acknowledges that the stated deadline has elapsed.

**Impact:** This is not proof the rule has lapsed (an out-of-band ruling may exist outside this deliverable), but the deliverable itself provides no evidence either way, and its own text says the fallback is automatic ("the default behavior is 3-hop mode") rather than requiring further action -- meaning the deliverable's silence is itself informative. A HARD rule whose operative status cannot be confirmed from the artifact that states it is a traceability gap in exactly the mechanism (4-hop/`sop-verifier`) that Findings S-002-01 and S-002-03 already show is under strain.

**Dimension:** Internal Consistency / Traceability.

**Response Required:** Confirm and document the H-36 ruling's actual disposition (issued -- with citation -- or deadline passed with the stated fallback executed and NS-H-08 revised accordingly) before relying on 4-hop/`sop-verifier` as a live, uncontested C3+/C4 control.

**Acceptance Criteria:** SKILL.md and NS-H-08 state the H-36 ruling's actual outcome, with a `TASK-0039-H36-RULING` status reference, or explicitly acknowledge the fallback is now in effect and NS-H-08 is revised to match.

---

### S-002-07: Dual "canonical" agent-definition sources duplicate the same defect with drifted wording [MINOR]

**Claim Challenged:** The skill maintains two parallel definitions per agent (`agents/{name}.md` + `.governance.yaml`, and `composition/{name}.agent.yaml` + `.prompt.md`), implicitly assumed to be kept in sync as equivalent "canonical" sources.

**Counter-Argument:** They already drifted. The SEC-008 defect (S-002-01) exists in both, but with different wording, showing the two sources are edited independently rather than generated from one source of truth.

**Evidence:**

`skills/nuclear-sop/agents/sop-verifier.md`, Step 6: *"If `PROCEDURE_STATE.yaml` is accessible (path discoverable from the workflow definition's directory):"*

`skills/nuclear-sop/composition/sop-verifier.prompt.md`, Step 6: *"If `PROCEDURE_STATE.yaml` is accessible from the workflow definition's directory:"*

Near-identical intent, different phrasing -- confirming these are two hand-maintained copies, not one generated artifact, which means any future one-sided fix (as SEC-011 appears to have received; see S-002-05) can silently leave the other copy stale.

**Impact:** Doubles the maintenance surface for every future correction and makes "fixed in one place" claims unreliable without an explicit diff check.

**Dimension:** Methodological Rigor.

**Recommendation (P2, acknowledgment sufficient):** Document which file set is authoritative at runtime; if both are load-bearing, add a CI diff check across the shared prose sections (STAR protocol text, guardrails, forbidden actions) to catch drift.

---

### S-002-08: No disclosure that all build-pipeline quality gates were self-scored by same-framework agents [MINOR]

**Claim Challenged:** Implicit throughout the Quality Gate History (`compliance-verification.md`): that QG-E1 through QG-E6, QG-R2, and QG-R3 constitute meaningful independent quality assurance for a skill explicitly modeled on nuclear "personnel independence."

**Counter-Argument:** Every gate in the chain -- architecture review, implementation review, security review, red-team recon/vulnerability assessment, and the final compliance verification itself -- was produced by Jerry-framework agents (`eng-architect`, `eng-lead`, `eng-backend`, `eng-qa`, `eng-security`, `red-recon`, `red-vuln`, `eng-reviewer`) scored via the same framework's own `/adversary` S-014 scorer. `qg-e6-score.md` states plainly: *"Scoring Strategy: S-014 (LLM-as-Judge)"* and `compliance-verification.md`'s footer: *"Quality gate: QG-E6 -- this report IS the quality gate deliverable."* No external or human reviewer is named anywhere in the located build-provenance tree.

**Impact:** `sop-verifier`'s own identity section is admirably candid about the limits of *its* independence: *"LLM context isolation is not equivalent to personnel independence as practiced in licensed nuclear operations."* The same candor is not extended to the build pipeline that certified the skill itself, even though the same limitation applies with equal force one level up (agents grading agents within one framework and, in several phases, one model family).

**Dimension:** Evidence Quality / Traceability.

**Recommendation (P2, acknowledgment sufficient):** Add one sentence to SKILL.md's Security Considerations disclosing that QG-E1 through QG-E6 were self-assessed by Jerry-framework agents without external or human review, consistent with the transparency already applied elsewhere in this same document to STAR and `sop-verifier` limitations.

---

## Recommendations

**P0 -- Critical, MUST resolve before the "approved for all criticality levels" claim can stand:**

1. **S-002-01** -- Apply the already-drafted SEC-008 fix to `agents/sop-verifier.md` AND `composition/sop-verifier.prompt.md`, or explicitly narrow the current approval claim to exclude C3+/C4 pending remediation.
2. **S-002-02** -- Reconcile SKILL.md's "deferred registration, user-applied" claim with the fact that this PR's own `CLAUDE.md`/`AGENTS.md`/`mandatory-skill-usage.md`/`plugin.json` already contain the splice.
3. **S-002-03** -- Either produce a genuine live-trial STAR validation, or relabel the existing artifact as a specification walkthrough rather than an empirical validation, in every place SKILL.md and the behavior rules currently say "empirically validated" / "PASSED."

**P1 -- Major, SHOULD resolve; require documented justification if not:**

4. **S-002-04** -- Correct the internally inconsistent TRAP-01 WARNING text in the example fixture and re-verify the validation citation.
5. **S-002-05** -- Correct the `.yaml`/`.md` extension mismatch in BB-003 and `POST_JOB_BRIEF.template.md` to match the other 6 agreeing files.
6. **S-002-06** -- Confirm and document the actual disposition of the H-36 governance ruling before continuing to rely on NS-H-08 as an uncontested HARD rule.

**P2 -- Minor, MAY resolve; acknowledgment sufficient:**

7. **S-002-07** -- Declare one agent-definition source authoritative, or add a drift-detection check between `agents/` and `composition/`.
8. **S-002-08** -- Disclose the self-scored nature of the QG-E1 through QG-E6 pipeline in SKILL.md's Security Considerations.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | The SEC-008 condition and the H-36 deadline both simply disappeared from the current record rather than being closed (S-002-01, S-002-06); nothing documents their resolution. |
| Internal Consistency | 0.20 | Negative | The dimension most impacted: S-002-01, S-002-02, S-002-05, and S-002-06 are all direct, quotable self-contradictions within the deliverable's own file set. |
| Methodological Rigor | 0.20 | Negative | S-002-03 (validation methodology is a narrative, not a trial), S-002-05 (an untested "regression baseline"), S-002-07 (dual unsynchronized sources) all point to process gaps beneath an otherwise well-structured methodology. |
| Evidence Quality | 0.15 | Negative | S-002-03, S-002-04, and S-002-08 each show the strength or independence of the deliverable's central evidence is weaker than represented. |
| Actionability | 0.15 | Neutral | Ironically strong on one axis: the project's own prior compliance report already drafted exact, copy-paste-ready remediation text for SEC-008 (S-002-01) that was simply never applied -- the fixes this review calls for were mostly already written by the deliverable's own authors. |
| Traceability | 0.10 | Mixed | The underlying build-provenance trail is unusually well-cited (specific file:line references throughout, which is precisely how these findings were located) -- but S-002-02 and S-002-06 show that traceability breaking down exactly at the two points (registration timing, governance deadline) that most affect the current safety claim. |

---

## Strategy Verdict

This Devil's Advocate pass finds that `/nuclear-sop`'s architecture and documentation are unusually thorough for a first-cut skill, and that thoroughness is precisely what makes its central safety claim falsifiable from its own paper trail: the deliverable's own prior security review named a specific, RPN-144, C3+-blocking defect in the independent-verification agent and drafted its fix, but the fix was never applied and the condition was quietly dropped from every currently-shipped governance document, which now claims unconditional C1-C4 approval (S-002-01); the "registration is deferred pending user action" disclosure is contradicted by this same PR's changeset (S-002-02); and the sole "empirical" safety validation underwriting that approval is a self-authored narrative walkthrough rather than an observed behavioral trial, a gap compounded by an internal inconsistency in the one test fixture it relies on (S-002-03, S-002-04) and by a "regression baseline" that itself disagrees with six other shipped files on a one-line, grep-detectable fact (S-002-05). None of this indicates the underlying STAR/hold-point/OE design is unsound -- the C1-C2 path in particular reads as coherent and well-guarded -- but the specific, prominently-stated claim that the skill is "approved for all criticality levels (C1 through C4)" is not supportable on the evidence the deliverable itself provides, and should be revised (either by closing the Critical findings or by re-stating the claim to match the conditions the project's own reviewers already documented) before this PR is treated as clearing C3+/C4 for use.

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 3 (S-002-01, S-002-02, S-002-03)
- **Major:** 3 (S-002-04, S-002-05, S-002-06)
- **Minor:** 2 (S-002-07, S-002-08)
- **Protocol Steps Completed:** 5 of 5 (Role Assumption; Assumption Inventory; Counter-Argument Construction; Response Requirements; Synthesis/Scoring Impact)
- **Files read (deliverable):** 31/31 files under `skills/nuclear-sop/` + 5/5 registration surfaces
- **Supplementary evidence files read (deliverable's own cited provenance, same PR):** 3 (`star-validation-results.md`, `qg-e6-score.md`, `compliance-verification.md`)
- **Leniency-bias counteraction:** Applied -- initial pass surfaced 3 findings before deeper cross-file verification; deeper verification (reading the cited build-provenance files and cross-checking file-extension claims across all 31 files) surfaced 5 additional, independently evidenced findings.

---

*Report Version: 1.0.0 | Strategy: S-002 Devil's Advocate | Template: `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0*
*Constitutional Compliance: P-001 (evidence-based, file:line citations throughout), P-003 (no subagents spawned), P-022 (H-16 blindness limitation disclosed above rather than silently assumed)*
*Agent: adv-executor | Tournament: C4 full tournament, Challenge group | Executed: 2026-08-07*

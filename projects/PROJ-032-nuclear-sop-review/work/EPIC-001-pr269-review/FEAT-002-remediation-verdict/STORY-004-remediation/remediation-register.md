# PROJ-032 Remediation Register — PR #269 (/nuclear-sop skill)

> Phase 4 triage of 114 normalized Critical/Major findings from three independent review phases (Phase 1 standards, Phase 2 engineering, Phase 3 C4 tournament). PR head `bda64202`. S-014 composite 0.52 REJECTED. Date: 2026-08-07.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Counts, dispositions, and the honest bottom line |
| [Cluster Index](#cluster-index) | All 14 remediation clusters at a glance |
| [Cluster Details](#cluster-details) | Full detail per cluster: members, files, fix spec or redesign question |
| [Traceability Appendix](#traceability-appendix) | Every input source ID mapped to exactly one cluster |
| [Method](#method) | Dedupe and disposition criteria applied |

---

## L0 Summary

**Input:** 114 findings (44 Critical, 70 Major) → **deduped to 59 unique defects** → **clustered into 14 remediation items** (REM-01..REM-14). Every finding is consumed by exactly one cluster (see [Traceability Appendix](#traceability-appendix)).

| Disposition | Clusters | Findings consumed | Critical findings | Major findings |
|---|---|---|---|---|
| DEFER-REWORK | 7 (REM-01..07) | 57 | 25 | 32 |
| FIX-NOW | 7 (REM-08..14) | 57 | 19 | 38 |
| **Total** | **14** | **114** | **44** | **70** |

Cluster severity: 12 Critical, 2 Major (REM-06, REM-07).

**The honest bottom line:** 25 of 44 Critical findings (**57% of the Critical mass**) are **NOT maintainer-fixable**. They fall in the seven DEFER-REWORK clusters, five of which (REM-01..05) attack the skill's core safety architecture: the quality-gate delegation topology is unimplementable under P-003 (REM-01), the primary user-authority mechanism depends on a tool no agent has (REM-02), the verifier and criticality model derive authority from the untrusted artifact they police and the promised tamper-detection control does not exist (REM-03), the C3+ approval rests on invalid validation evidence (REM-04), and the H-36 governance ruling that decides whether sop-verifier even exists is expired with contradictory fallbacks (REM-05). A maintainer patch on the contributor branch can clear at most 19/44 (43%) of Critical findings — schema errors, false/contradictory claims, registration gaps, extension mismatches, composition drift, and navigation tables. **Applying every FIX-NOW cluster still leaves a skill whose safety mechanisms require contributor redesign before C3+ (arguably any) production use.**

---

## Cluster Index

| ID | Title | Severity | Disposition | Findings | Unique defects |
|----|-------|----------|-------------|----------|----------------|
| [REM-01](#rem-01-qg-hold-and-mid-procedure-delegation-topology) | QG-HOLD and mid-procedure delegation topology | Critical | DEFER-REWORK | 11 | 5 |
| [REM-02](#rem-02-user-hold-mechanism-and-runtime-execution-model) | USER-HOLD mechanism and runtime execution model | Critical | DEFER-REWORK | 8 | 8 |
| [REM-03](#rem-03-trust-boundary-integrity-and-state-tamper-protection) | Trust-boundary integrity and state tamper protection | Critical | DEFER-REWORK | 8 | 4 |
| [REM-04](#rem-04-qg-e4-validation-evidence) | QG-E4 validation evidence | Critical | DEFER-REWORK | 11 | 6 |
| [REM-05](#rem-05-h-36-governance-ruling) | H-36 governance ruling | Critical | DEFER-REWORK | 11 | 3 |
| [REM-06](#rem-06-oe-feedback-loop-design) | OE feedback-loop design | Major | DEFER-REWORK | 3 | 3 |
| [REM-07](#rem-07-executor-command-gating-and-injection-screening) | Executor command gating and injection screening | Major | DEFER-REWORK | 5 | 3 |
| [REM-08](#rem-08-registration-and-status-truth-reconciliation) | Registration and status truth reconciliation | Critical | FIX-NOW | 13 | 3 |
| [REM-09](#rem-09-registration-enforcement-surfaces) | Registration enforcement surfaces | Critical | FIX-NOW | 9 | 3 |
| [REM-10](#rem-10-agent-definition-schema-and-standards-conformance) | Agent definition schema and standards conformance | Critical | FIX-NOW | 10 | 8 |
| [REM-11](#rem-11-oe-artifact-contract-alignment) | OE artifact contract alignment | Critical | FIX-NOW | 11 | 3 |
| [REM-12](#rem-12-state-machine-and-completion-contract-reconciliation) | State machine and completion contract reconciliation | Critical | FIX-NOW | 3 | 3 |
| [REM-13](#rem-13-composition-drift-resynchronization) | Composition drift resynchronization | Critical | FIX-NOW | 9 | 5 |
| [REM-14](#rem-14-navigation-tables) | Navigation tables | Critical | FIX-NOW | 2 | 2 |

---

## Cluster Details

### REM-01: QG-HOLD and mid-procedure delegation topology

**Severity:** Critical | **Disposition:** DEFER-REWORK | **Members:** 11 findings, 5 unique defects

**Why a maintainer patch is inappropriate:** The fix requires new PROCEDURE_STATE states (QG-PENDING / AGENT-PENDING analogs), a suspend/resume handoff protocol that does not exist anywhere in the skill, a rewritten execution model for the flagship example, and an H-36 hop budget for the composed pattern. That is delegation-topology design authority, not text repair. The ps-critic→adv-scorer naming conflation (G3) is textually fixable, but fixing the name does not make the gate executable — whichever topology the contributor chooses rewrites those same lines, so it is subsumed here.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-001, S-001-04, S-013-02, P2-001 (part) | QG-HOLD steps are written as sop-executor's own first-person actions incl. "Invoke ps-critic via /adversary S-014" — but the same file declares Task ABSENT ("cannot invoke any other agent") and there is no return-to-main-context step (the adjacent IV-HOLD correctly has one). H-01/P-003 violation as literally written; the H-13 gate cannot fire as designed. Duplicated in both composition twins. |
| G2 | P2-001, S-004-04, S-010-05 | Flagship example (c3-adr-workflow-definition.md) requires main-context Task calls to ps-researcher/ps-analyst/ps-architect at procedure Steps 2/4/5 *inside* a sop-executor invocation; the state machine has only IV-PENDING as a waiting-on-external-actor status, no suspend/resume protocol, and the STAR Application Scope table has no row for who performs STAR on a delegated step. |
| G3 | S-007-03, S-012-04, S-011-06 | "ps-critic via /adversary S-014" conflates /problem-solving's ps-critic with /adversary's adv-scorer (the actual S-014 implementer per SSOT) consistently across ~8 files (agents, both composition twins, behavior rules NS-H-03, SKILL.md, PLAYBOOK.md, reference.md, howto-guides.md, HOLD_POINT_LOG.template.md example row) — while the skill's own worked example correctly names adv-scorer. |
| G4 | S-012-07 | SKILL.md's H-36 compliance analysis scopes hop counting to the 4 internal agents only; the composed pattern the how-to guide recommends reaches ~7 Task hops vs the HARD 3-hop ceiling; the deferred-to document (skill-integration-analysis.md) is not shipped or citable. |
| G5 | S-004-11 | QG-HOLD release and the wrapped-workflow pattern hard-depend on /adversary's S-014 interface and peer-skill agents with no version pin or compatibility contract; NS-H-03's fail-closed default caps the damage at a stall. |

**Affected files:** `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/composition/sop-executor.prompt.md`, `skills/nuclear-sop/composition/sop-executor.agent.yaml`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml`, `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/docs/reference.md`, `skills/nuclear-sop/docs/howto-guides.md`

**Redesign question for the contributor:** Under H-01/P-003 (one level: orchestrator→worker) and H-36 (3 hops), who invokes quality gates and external agents mid-procedure, and how does sop-executor suspend and resume place-keeping around them? Candidate architectures to choose and specify: (a) QG-HOLD returns control to the main context (mirroring IV-HOLD), with new waiting statuses and a documented suspend/resume handoff; (b) the orchestrator executes any step whose Action is an agent invocation, with sop-executor performing STAR on the returned result; (c) mid-procedure composition is dropped and the example rewritten. The chosen design must also: name adv-scorer (not ps-critic) as the S-014 implementer everywhere; publish a hop-count budget for the composed pattern; and declare the /adversary interface dependency.

---

### REM-02: USER-HOLD mechanism and runtime execution model

**Severity:** Critical | **Disposition:** DEFER-REWORK | **Members:** 8 findings, 8 unique defects

**Why a maintainer patch is inappropriate:** The runtime execution model (worker subagent vs main-context persona) is never pinned down, and every candidate model breaks a different declared guarantee — subagents cannot pause to converse (USER-HOLD dies), persona mode voids T1/T2 tool-tier enforcement and sop-verifier's isolation rationale. NS-H-01 as written is non-terminating; making it terminate requires redefining which writes need STAR. These are architecture decisions with cascading effects on the rules, baselines, and all four agents.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-002, P2-015 (part) | USER-HOLD requires AskUserQuestion — absent from the agent's tool grant, absent from every T1-T5 tier, used by zero of 89 shipped agents — while governance declares it "the sole mechanism" and forbids all fallbacks ("NEVER simulate. NEVER auto-approve."). The safety-critical P-020/H-02 gate stalls or improvises; governance asserts a capability the agent lacks (P-022 concern). sop-brief has the identical defect at all six interactive STOP gates. |
| G2 | P2-015 | The runtime execution model is unpinned: SKILL.md diagrams all four agents as worker subagents, which cannot pause mid-run to converse with the user; each candidate model (subagent vs persona) breaks a different guarantee; bb-002's forbidden-pattern table makes every conceivable run a violation. |
| G3 | S-004-10 | USER-HOLD has no timeout, escalation path, or scope statement for unattended/background contexts — a stalled C3+ procedure at its highest-consequence gate has no described resolution. |
| G4 | S-001-07 | SR-02 (C3+ workflow with state-modifying steps and zero [USER-HOLD]s) is explicitly WARNING-only, permitting a fully autonomous C4 irreversible workflow — while the lower-stakes OE-accumulation condition escalates to a STOP. |
| G5 | P2-002 | NS-H-01 is non-terminating: STAR-before-every-Write, but recording STAR is itself a Write and NS-H-10 mandates a state Edit per step; bb-001 silently exempts bookkeeping writes, contradicting the HARD rule's plain text; `verify_no_star_skipped` is invalidated as a checkable assertion. |
| G6 | P2-019 | Context budget unrealism: ~6 tool calls minimum per step, pre-job brief reproduces the OE corpus verbatim (O(corpus), no size cap), example concedes 60-70% fill by Step 12; step limits asserted without a token model; CB-02 unexamined. |
| G7 | S-004-08 | The example requires checkpoint-at-80%-fill (AE-006c), but no methodology step measures context fill or defines "checkpoint" for this tool set. |
| G8 | S-004-09 | Step ceilings are tight (example at 15/15) yet sub-procedure splitting is under-specified: NS-M-04 is a SHOULD-propose, and NS-H-07's mandatory Step 1 has no carve-out for continuation invocations. |

**Affected files:** `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/agents/sop-executor.governance.yaml`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/behavioral-baselines/` (bb-001, bb-002), `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md`

**Redesign question for the contributor:** Pin the runtime execution model and make the interactive gates real under it. If the agents are worker subagents: USER-HOLD must become a return-to-orchestrator protocol (the orchestrator/main context asks the user via AskUserQuestion and re-invokes), with statuses and resume semantics specified; if main-context persona: re-justify tool-tier enforcement and verifier isolation. Then: rewrite NS-H-01 with a terminating scope (define which writes require STAR — procedure-step mutations vs bookkeeping — and re-align bb-001); give USER-HOLD a timeout/unattended policy; decide whether SR-02 at C3+ escalates to STOP; and publish a token/context model that justifies step limits, brief size, and a concrete checkpoint mechanism.

---

### REM-03: Trust-boundary integrity and state tamper protection

**Severity:** Critical | **Disposition:** DEFER-REWORK | **Members:** 8 findings, 4 unique defects

**Why a maintainer patch is inappropriate:** The verifier and the criticality model derive their authority from the artifact they are supposed to police (the workflow definition, the skill's own named primary trust boundary TB-1), and the promised state_hash tamper-detection control is fabricated-as-documented — implemented nowhere, and even if implemented, a keyless self-computed hash is recomputable by the same actor who tampers. Inserting a real trust anchor changes the data flow between caller, orchestrator, and agents. A maintainer deleting the false state_hash claim would silently remove a promised safety control that SR-04/SD-03 and SEC-003 depend on; a maintainer implementing it would be designing the control.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P2-022 | Authority inversion: sop-verifier's acceptance criteria and expected output paths both originate from the untrusted workflow definition ("the authoritative source", SR-09). A crafted or maliciously Step-0-generated definition supplies criteria its own outputs trivially satisfy → verifier returns ACCEPT with quoted evidence; the skill's differentiating safety mechanism is void against its own primary threat actor. |
| G2 | P2-023 | Criticality is self-declared by the untrusted definition/caller and de-rates every downstream protection (C1 → 3-hop, [REFERENCE] defaults, SR-02 silenced, step limit 20, QG ceiling 3). No cross-check against the framework's auto-escalation table (AE-001/002/004/005), which exists for precisely this function. |
| G3 | S-001-03, S-004-01, S-007-01, S-012-05, S-013-03 | The SHA-256 state_hash control is documented in PROCEDURE_STATE.template.yaml and docs/reference.md as "computed after every state write, verified in STAR-STOP before every tool call" — but no agent file (agents/*.md, composition/*.prompt.md, governance) contains any instruction to compute or verify it. 100% inert while documented as active (P-022). Even as specified, a keyless self-hash is not integrity protection against the knowledgeable adversary SR-04 names. |
| G4 | P2-024 | State-file poisoning steers execution past holds: RESUME trusts current_step/next_step/status, and the SEC-003 hold check fires only on status == HELD — a poisoned IN-PROGRESS file resumes cleanly past all three hold types. The real reconciliation (sop-capture SR-05) runs only after execution, after the irreversible action the hold guarded. |

**Affected files:** `skills/nuclear-sop/agents/sop-verifier.md`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml`, `skills/nuclear-sop/docs/reference.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`

**Redesign question for the contributor:** Establish an authority model in which no safety control derives from the artifact it polices. Specifically: (a) where do sop-verifier's acceptance criteria and expected paths come from if not the TB-1 definition — a user-approved brief pinned at USER-HOLD, orchestrator-supplied criteria, or a signed/pinned copy? (b) how is declared criticality cross-checked and auto-escalated against AE-001/002/004/005 signals (target paths under `.context/rules/`, security-relevant code)? (c) is tamper evidence for PROCEDURE_STATE.yaml implemented for real (integrity mechanism outside the file, hold-state check independent of the status field, orchestrator-held ledger) or is the claim withdrawn everywhere it appears — and how is the RESUME-past-holds path (G4) closed pre-execution rather than post-hoc?

---

### REM-04: QG-E4 validation evidence

**Severity:** Critical | **Disposition:** DEFER-REWORK | **Members:** 11 findings, 6 unique defects

**Why a maintainer patch is inappropriate:** A maintainer cannot manufacture evidence. The "3/3 catch rate (100%), empirically validated" claim that lifted the C3+ restriction rests on a self-authored simulation walkthrough of a fixture that embeds its own answer key, with N=3 against a 60% bar, an internally contradictory trap, an unsatisfiable acceptance criterion, and the evidence file outside the shipped package. Re-validation is contributor work; the interim text corrections (withdrawing the claim) are handled in REM-08.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | S-001-02, S-011-04 | Answer-key contamination: each trap step embeds a "TEST HARNESS — TRAP-NN EXPECTED STAR RESPONSE" block with the fully worked expected reasoning in the same file sop-executor loads into context at Phase 0 — the test measures repetition of nearby context, not blind deviation detection, and the fixture cannot be reused for any genuine blind test without stripping the blocks. |
| G2 | S-002-03, S-011-03, S-004-07 | "Empirically validated" mischaracterizes the evidence: star-validation-results.md is by its own footer an "Empirical simulation — STAR walkthrough" authored by the same engineer who designed the traps and pre-scripted the expected answers; no live sop-executor invocation, no transcript/log, no independent tester; the speculative STAR-OFF baseline was never observed. The entire safety case is a self-policing LLM certified by its own authors. |
| G3 | S-012-09 | N=3 deliberate traps against a self-defined >=60% bar is statistically trivial; AC-7 of the same fixture is literally unsatisfiable (globs `.md`, capture writes `.yaml`), so either AC-7 was checked and could not have passed, or "3/3" describes a narrower verification than the fixture's own criteria. |
| G4 | S-002-04, CC-8 | The fixture is internally inconsistent about its own trap: TRAP-01's WARNING text (line 235) names `projects/{JERRY_PROJECT}/decisions/ADR-NNN.md` while its ERROR TRAP callout (line 242) and Target field (line 249) name `docs/design/ADR-NNN.md`; the validation report silently cites the one supporting its narrative. |
| G5 | P2-006, S-012-11 | Status and packaging drift around the gate: PLAYBOOK.md still asserts the opposite gate status; SKILL.md retains stale future-tense scaffolding next to the PASS result; the sole evidence artifact lives outside the shipped `skills/nuclear-sop/` package, in the contributing project tree («PR projects tree»/PROJ-0039-nuclear-engineer), unverifiable to a package consumer. |
| G6 | S-012-12 | Guardrails cite SD-01..SD-18 security-design decisions, but SD-06/11/13/15/17 are never defined anywhere and no threat-model/security-design register is shipped or cited with a resolvable path — gaps vs descopes cannot be audited. |

**Affected files:** `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/agents/sop-executor.governance.yaml`, star-validation-results.md and skill-integration-analysis.md under «PR projects tree»/PROJ-0039-nuclear-engineer

**Redesign question for the contributor:** Produce validation evidence that would survive independent review: blind fixtures (answer-key blocks stripped; TRAP-01's path contradiction fixed), actually-executed runs with transcripts/tool-call logs from live sop-executor invocations, independent trap authorship and scoring, an N and pass bar with statistical footing, full acceptance-criteria coverage (including AC-7 after REM-11), evidence shipped inside or resolvably cited from the package, and a shipped SD-01..18 security-design-decision register. Until then, C3+ approval claims must remain withdrawn (text handled by REM-08).

---

### REM-05: H-36 governance ruling

**Severity:** Critical | **Disposition:** DEFER-REWORK | **Members:** 11 findings, 3 unique defects

**Why a maintainer patch is inappropriate:** The defect is a missing governance *decision*, not a missing edit. The deadline (2026-06-15) lapsed ~53 days before review; NS-H-08 mandates 4-hop for C3+ "until revised" while SKILL.md/PLAYBOOK mandate the opposite default (automatic 3-hop, sop-verifier eliminated) — two contradictory mandatory instructions with different anchor events. Whichever branch a maintainer picked, they would be silently *making* the ruling that decides whether a safety agent exists, and the ruling itself depends on the hop-model redesign in REM-01. This was the review's highest-RPN failure mode (FMEA RPN 648).

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-018, S-001-05, S-007-04, S-010-06, S-011-07, S-012-01, S-013-05 | Deadline lapsed with no ruling artifact on the branch, no TASK-0039-H36-RULING worktracker entity, no GitHub-issue parity (H-32) — repo-wide grep matches only the rules file itself. The operative status of the C3+ verification-mode HARD rule cannot be determined from the shipped files, which continue asserting 4-hop as current in unqualified present tense. |
| G2 | S-002-06, S-003-02, S-004-03 | Contradictory fallback semantics (SKILL.md: automatic reversion to 3-hop, sop-verifier eliminated; NS-H-08: "remains as written" until revision) and different deadline anchors ("Phase 1 delivery" vs "skill registration (2026-06-15)"); none of H-36's required halt/log/present/escalate termination behavior is implemented; no machine-checkable staleness signal exists. |
| G3 | P2-005 | The default is fail-open: governance *inaction* removes a safety mechanism for all criticality levels, inverting the skill's own conservative-decision principle (E-2), while NS-H-08 simultaneously prohibits 3-hop for C3+; the underlying hop-counting crisis is self-inflicted given H-36 defines hops as routing re-evaluations. |

**Affected files:** `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, worktracker (missing TASK-0039-H36-RULING entity), GitHub issues (missing H-32 twin)

**Redesign question for the contributor:** Obtain the actual H-36 ruling (blocked on REM-01's hop-model definition): does C3+ retain 4-hop mode with sop-verifier, or revert to 3-hop and eliminate it? Then encode exactly one fallback semantics and one anchor date across NS-H-08, SKILL.md, and PLAYBOOK.md; remove or re-justify the fail-open 60-day default (it inverts E-2 — the conservative default is fail-closed: keep the stronger verification until ruled otherwise); and create the TASK-0039-H36-RULING worktracker entity with a GitHub issue per H-32 and a real deadline.

---

### REM-06: OE feedback-loop design

**Severity:** Major | **Disposition:** DEFER-REWORK | **Members:** 3 findings, 3 unique defects

**Why a maintainer patch is inappropriate:** Requires schema design (a synthesis entry type that can actually be written), threshold-policy design (per-workflow_type counters that cannot repo-wide-STOP all executions), and a trust/retention model for the OE corpus. These are decisions about how the skill's flagship feedback loop works, with three files currently giving three different answers on synthesis ownership alone.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P2-007 | Synthesis entries cannot exist: `entry_type: synthesis` is not in the 18-field mandatory OE schema, and sop-capture's all-fields-non-empty write-block rejects any entry lacking per-execution fields. Ownership is contradicted three ways (sop-brief → sop-capture; PLAYBOOK → ps-synthesizer; NS-M-06 → a section in normal entries). The accumulation threshold is keyed per workflow_type (3 values), so 21 unsynthesized NOMINAL entries STOP every NOMINAL execution repo-wide — and since synthesis entries cannot be produced, the count monotonically approaches that STOP. |
| G2 | P2-025 | The OE corpus is a cross-criticality persistence/injection channel: any C1 execution or direct repo write plants entries that all future same-type briefs — including C4 — must load as MANDATORY CONTEXT. SEC-002 guard labels cover only 2 of the interpolated fields; the SR-03 provenance cross-reference is forgeable (both artifacts unauthenticated); "HUMAN INFORMATION ONLY" is model-compliance, not a control; bb-003 tests one field. |
| G3 | S-013-07 | No retention/archival policy for per-execution PROCEDURE_STATE.yaml files: routine work/ cleanup makes every legitimate OE entry permanently [PROVENANCE-UNVERIFIED], degrading corpus signal or perversely incentivizing never cleaning work/. |

**Affected files:** `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`

**Redesign question for the contributor:** Define the OE lifecycle end-to-end: a synthesis artifact type sop-capture can actually write (schema field or separate type with its own mandatory-field set), exactly one synthesis owner, threshold scoping that cannot deadlock unrelated executions, a provenance mechanism that survives work/ cleanup (or an archival rule), and an injection trust model for the corpus (guard labels on every interpolated field, or explicit acceptance of residual risk given C1-writes-feed-C4-briefs).

---

### REM-07: Executor command gating and injection screening

**Severity:** Major | **Disposition:** DEFER-REWORK | **Members:** 5 findings, 3 unique defects

**Why a maintainer patch is inappropriate:** Replacing enumerable-badness with a principled gating model (allowlist or category-based gating integrated with the existing deterministic SecurityEnforcementEngine) and deciding the injection-screening scope are security-architecture choices; a maintainer bolting more substrings onto the denylist would reproduce the exact anti-pattern the findings identify. (Interim mitigations a maintainer *could* take without redesign — narrowing sop-brief/sop-capture's Bash grants, since their declared needs are covered by other tools — are noted, but the cluster's resolution is the gating model.)

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P2-026, S-001-06, S-013-08 | The Bash guard is a static substring denylist (curl, wget, ssh, scp, git push, sudo, chmod 777, rm -rf /) with no principle-based catch-all: nc/ncat, `python -m http.server`, base64 exfil, `chmod -R 777 path`, `rm -rf ./dir`, package-manager code execution all pass without [USER-HOLD]. sop-brief and sop-capture hold full Bash for needs (read-only interrogation, timestamps, file counts) other tools already cover — the read-only restriction is prose only. H-05 (uv-only Python) is never surfaced, so a step saying `python script.py` conflicts with a repo HARD rule the prompts never mention. |
| G2 | P2-027 | SEC-001 screens only WARNING/CAUTION annotation content while Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and Sections 2/3/9 prose are equally attacker-controlled and directly drive tool calls (TRAP-02 tests one channel). On detection, the executor logs the payload verbatim into the execution log sop-capture later reads — a second-order injection channel. PLAYBOOK overstates machine-side coverage by naming SEC-001/002 "the primary mitigations" when SR-06 human review is the actual primary control. |
| G3 | S-004-12 | The blocking is a bespoke, weaker prompt-level copy of a control the repo already provides deterministically (SecurityEnforcementEngine, 82 tests) with no integration or reference. |

**Affected files:** `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`

**Redesign question for the contributor:** What is the command-gating model? Options to choose and specify: allowlist per agent; category-based gating (network egress, package/code execution, privilege change, recursive deletion ⇒ mandatory [USER-HOLD]); and/or delegation to the deterministic SecurityEnforcementEngine instead of prompt-level substring matching. Define the injection-screening scope across *all* definition-sourced fields that drive tool calls (or justify the narrower scope), neutralize payload echo into logs (hash/excerpt, not verbatim), surface H-05 in executor constraints, and drop or narrow the Bash grants for sop-brief/sop-capture. Correct PLAYBOOK's mitigation-hierarchy claim to name SR-06 human review as primary.

---

### REM-08: Registration and status truth reconciliation

**Severity:** Critical | **Disposition:** FIX-NOW | **Members:** 13 findings, 3 unique defects

**Rationale:** All defects are false or contradictory *claims* fixable by text correction. The reconciliation direction is dictated by honesty plus REM-04: registration is a fact (accept and document it); C3+ approval is not currently supportable (withdraw it pending re-validation).

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | S-001-01, S-002-02, S-004-02, S-007-05, S-011-01, S-012-02, S-013-01, P2-009 | SKILL.md's DEFERRED REGISTRATION NOTE ("NOT registered and NOT live-routable until QG-E6 passes and the user applies these entries"; "splicing is performed by the user, not an agent") is false as shipped: the same PR registers the skill in CLAUDE.md:78, AGENTS.md, mandatory-skill-usage.md (priority-16 row), plugin.json:53-56, and CHANGELOG.md — and QG-E6 passed (0.934, 2026-04-14, qg-e6-score.md). |
| G2 | P1-016, S-003-03, S-010-02 | The "copy-ready" trigger row in SKILL.md (priority 12, 9 negatives, 5 compounds) diverges from the applied row (priority 16, expanded negatives, 8 compounds); re-applying it as instructed would collide with /user-experience and regress the live routing table. QG-E6 evidence is not cited from SKILL.md with a resolvable path. |
| G3 | P1-017, S-012-13 | PLAYBOOK.md line ~677 still says "NOT available for C3+ ... restrict to C1-C2 only" while SKILL.md line ~229/244 says "C3+ APPROVED ... all criticality levels" — the two entry-point documents give opposite answers to the package's most safety-relevant question. |

**Affected files:** `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md` (verify consistency: `CHANGELOG.md`)

**Fix specification:**
1. `skills/nuclear-sop/SKILL.md` (~line 446): replace the entire "DEFERRED REGISTRATION NOTE" block with a "REGISTRATION STATUS: APPLIED" note stating: registered in CLAUDE.md, AGENTS.md, `.context/rules/mandatory-skill-usage.md` (trigger map, priority 16), and plugin.json in PR #269; QG-E6 scored 0.934 PASS on 2026-04-14 — cite qg-e6-score.md by resolvable path under «PR projects tree»/PROJ-0039-nuclear-engineer. Remove all "NOT registered", "NOT live-routable", and "user applies these entries" sentences.
2. `skills/nuclear-sop/SKILL.md` (~line 476): delete the stale priority-12 copy-ready trigger-row block; replace with a pointer naming `.context/rules/mandatory-skill-usage.md` as the live SSOT row (do NOT paste a second copy that can drift).
3. C3+ status — reconcile in the conservative direction (required by REM-04): in `skills/nuclear-sop/SKILL.md` (~lines 229, 244) change "C3+ workflow status: APPROVED ... approved for all criticality levels (C1 through C4)" to "C3+ status: WITHDRAWN pending re-validation (QG-E4 evidence invalidated in PROJ-032 review; see remediation register REM-04). Approved use: C1-C2 only." Reword "empirically validated ... 3/3 catch rate (100%)" to "simulation walkthrough (desk-check); not independent execution evidence". In `skills/nuclear-sop/PLAYBOOK.md` (~line 677) keep the C1-C2 restriction and update its stated reason to cite the PROJ-032 invalidation rather than a not-yet-run gate. Remove the stale future-tense QG-E4 scaffolding from SKILL.md's gate table (P2-006 tail).
4. While editing SKILL.md status text, note SEC-008 as OPEN with remediation tracked in REM-12 (do not assert unconditional C1-C4 approval anywhere).
5. **Validate:** `grep -rn "NOT registered\|NOT live-routable\|priority.*12" skills/nuclear-sop/SKILL.md` → 0 hits; `grep -rn "approved for all criticality\|C1 through C4" skills/nuclear-sop/` → 0 unqualified hits; SKILL.md and PLAYBOOK.md state the same C1-C2 restriction.

---

### REM-09: Registration enforcement surfaces

**Severity:** Critical | **Disposition:** FIX-NOW | **Members:** 9 findings, 3 unique defects

**Rationale:** Registration-surface gaps and registry bookkeeping — mechanical edits to `.context/rules/mandatory-skill-usage.md` and `AGENTS.md` with exact prescribed content (the PR's own phase-6 artifact already drafted the missing H-22 sentence).

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-019, S-007-06, S-011-02, S-012-03 | /nuclear-sop is the only trigger-mapped skill absent from both the H-22 rule sentence and the L2-REINJECT comment — the context-rot-immune per-prompt enforcement never covers it; it routes only via the rot-vulnerable L1 trigger map. The PR's own phase-6 artifact (registration-trigger-map-row.md) prescribed the exact sentence but it was never applied. |
| G2 | P1-020 | The documented activation keyword "nuclear workflow" deterministically misroutes to /orchestration ("workflow" positive at priority 1; no "nuclear" negative; no such compound trigger exists) — routing Step 3 resolves priority 1 vs 16. The phase-6 collision analysis falsely claims a compound trigger covers it. |
| G3 | S-003-05, S-003-06, S-007-07, S-012-10 | AGENTS.md not updated for the 4 new agents: no nav-table entry for "Nuclear SOP Skill Agents", no Agent Summary row, Total still 89 (correct: 93), stale "Last verified: 2026-03-09", and sop-* absent from the MCP "Not included (by design)" note despite fitting the documented file-based-persistence exclusion pattern. |

**Affected files:** `.context/rules/mandatory-skill-usage.md`, `AGENTS.md`, phase-6 collision-analysis artifact under «PR projects tree»/PROJ-0039-nuclear-engineer

**Fix specification:**
1. `.context/rules/mandatory-skill-usage.md`, H-22 rule cell: append the sentence prescribed by the PR's phase-6 registration artifact — "MUST invoke `/nuclear-sop` for nuclear-inspired procedural execution ..." (take exact wording from registration-trigger-map-row.md under «PR projects tree»/PROJ-0039-nuclear-engineer), inserted after the `/contract-design` clause.
2. Same file: add `/nuclear-sop` to the L2-REINJECT comment enumeration so per-prompt re-injection covers it.
3. Same file, /nuclear-sop trigger row: extend Compound Triggers with `"nuclear workflow" OR "nuclear sop" (phrase match)`. Do not modify the /orchestration row (compound-trigger specificity overrides numeric priority per the routing algorithm Step 2, resolving the collision without touching a peer skill). Annotate the phase-6 collision-analysis artifact as corrected/superseded.
4. `AGENTS.md`: add "Nuclear SOP Skill Agents" to the Document Sections nav table (anchor link); add an Agent Summary row (Nuclear SOP | 4 agents); change Total 89 → 93 and update "Last verified" to the fix date; append sop-* to the MCP "Not included (by design)" note: file-based persistence per P-002 (PROCEDURE_STATE.yaml, HOLD_POINT_LOG.md, dual-write OE entries), mirroring the wt-*/eng-*/red-* wording.
5. **Validate:** grep confirms "nuclear-sop" appears in H-22 sentence, L2-REINJECT comment, and trigger row of the same file; simulated routing of "nuclear workflow" resolves to /nuclear-sop via compound trigger; AGENTS.md total equals the count of registered agents; every `##` heading in AGENTS.md appears in its nav table.

---

### REM-10: Agent definition schema and standards conformance

**Severity:** Critical | **Disposition:** FIX-NOW | **Members:** 10 findings, 8 unique defects

**Rationale:** Deterministic validator failures and standards-conformance text fixes with exact known corrections; the compliant corpus (66 governance files, reference agents) defines the target form. H-34's consequence ("rejected at CI") makes these mandatory before any re-review.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-003 | `composition/sop-verifier.agent.yaml` is unparseable YAML: unquoted ": " inside the line-9 description scalar → ScannerError; once parseable, output.levels prose strings additionally fail the canonical schema. |
| G2 | P1-004, P2-018 | `sop-brief.governance.yaml` fails agent-governance-v1 (4 errors): post_completion_checks entries are single-key mappings; schema requires strings (0 of 66 existing files use dict style). |
| G3 | P1-005, S-010-01 | `sop-verifier.governance.yaml` fails (2 errors): output.required true without location (AR-010 conditional), and output.levels prose strings match neither schema branch; required:true also misleadingly asserts a file artifact a T1 agent cannot write. Same malformed levels pattern duplicated in `composition/sop-verifier.agent.yaml`. |
| G4 | P1-007 | `composition/sop-brief.agent.yaml` fails its self-declared canonical schema (5 errors): unquoted colon in on_send line 92 plus the same 4 dict-style checks. |
| G5 | P1-012 | Section-numbering contradictions vs the skill's own template (Section 4 Prerequisites, 5 Initial Conditions, 9 Acceptance Criteria): sop-brief Step 1.6 validates "5 (prerequisites)"; purpose claims "sections 1-6 (scope through acceptance criteria)"; identity assigns 7-9 to sop-executor while sop-brief validates 9. Mirrored in domain_extensions A-3 of both YAMLs. |
| G6 | P1-013 | AD-M-011: none of the four agents declares a `projects/${JERRY_PROJECT}/`-anchored output location or filename_pattern, with no documented override; sop-executor's `{execution_dir}` is never defined; sop-capture's location is non-resolvable prose; sop-verifier has none at all. |
| G7 | P1-014 | Hexagonal dependency rule: domain-layer sections in all four .md bodies name concrete tools (incl. load-bearing "steps that use Write, Edit, or Bash MUST receive [CONTINUOUS]" and literal Glob()/Grep()/Read() call syntax). |
| G8 | P1-021 | sop-executor.governance.yaml declares quality_gate_tier C3 but omits reasoning_effort (ET-M-001: C3 = high); execution agent, not validation-only; no documented justification. |

**Affected files:** `skills/nuclear-sop/agents/sop-brief.governance.yaml`, `skills/nuclear-sop/agents/sop-verifier.governance.yaml`, `skills/nuclear-sop/agents/sop-executor.governance.yaml`, `skills/nuclear-sop/agents/sop-capture.governance.yaml`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-verifier.md`, `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/composition/sop-verifier.agent.yaml`, `skills/nuclear-sop/composition/sop-brief.agent.yaml`

**Fix specification:**
1. `composition/sop-verifier.agent.yaml` line 9: convert the description to a `>-` block scalar (or quote it) eliminating the inline ": "; fix output.levels to `[L0, L1, L2]` (move prose into the body/prompt).
2. `agents/sop-brief.governance.yaml` lines 66-70: rewrite each post_completion_checks item as a plain string, e.g. `- "verify_file_created: brief/pre-job-brief.md"`, matching the 66-file corpus style. Apply the identical conversion in `composition/sop-brief.agent.yaml`, and quote its on_send line 92 (`"Provide path to completed pre-job brief: brief/pre-job-brief.md"`).
3. `agents/sop-verifier.governance.yaml`: set `output.required: false` (truthful for a T1 agent returning the report as Task response content — its own note says so) and convert output.levels to the `[L0, L1, L2]` enum form; mirror the levels fix in the composition twin.
4. `agents/sop-brief.md`: Step 1 item 6 → "sections 4 (prerequisites), 5 (initial conditions), and 9 (acceptance criteria)"; purpose line 39 → "validates sections 1-6 plus section 9 (acceptance criteria)"; identity line 12 → assign sections 7-8 to sop-executor with section 9 validated by sop-brief and verified by sop-verifier. Mirror the corrected mapping in domain_extensions A-3 of both sop-brief YAMLs (governance + composition).
5. AD-M-011 declarations in all four governance files: sop-brief `output.location: "projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/brief/pre-job-brief.md"` + filename_pattern; define `{execution_dir}` once in SKILL.md/rules as the caller-provided base path (Priority 2) defaulting to `projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/` and reference it from sop-executor's location; sop-capture: replace the prose location with the two explicit paths (execution-dir copy + global registry `docs/experience/{entry_id}.yaml`) and add a documented MEDIUM-tier override justification for the repo-global OE registry (cross-project OE reuse is the design intent per the behavior rules); sop-verifier: no file output (required:false), so declare none. Reference pattern: ps-researcher.governance.yaml.
6. Hexagonal rewording in all four .md domain sections: replace tool names with capability language ("steps that modify files or execute commands MUST receive [CONTINUOUS]"; "read-only inspection"; "cannot modify files or execute commands" for the T1 constraint); relocate literal Glob/Grep/Read call syntax into `<capabilities>`.
7. `agents/sop-executor.governance.yaml`: add `reasoning_effort: high`; set the other three per their quality_gate_tier under ET-M-001 (sop-verifier, validation-only, MAY stay default — document the choice).
8. **Validate:** `uv run jsonschema` (or repo validator) against `docs/schemas/agent-governance-v1.schema.json` → 0 errors for all four governance files; `yaml.safe_load` succeeds on all four composition agent.yaml files; canonical-schema validation passes for composition files retained per REM-13; grep for `Glob(`/`Grep(`/`Read(` inside `<identity>`/`<purpose>`/`<methodology>`/`<guardrails>` → 0 hits.

---

### REM-11: OE artifact contract alignment

**Severity:** Critical | **Disposition:** FIX-NOW | **Members:** 11 findings, 3 unique defects

**Rationale:** Extension mismatch and retrieval-protocol drift are text corrections toward an unambiguous authoritative convention (`.yaml`, workflow_id-primary) already defined by the rules file and followed by the write path; the missing Section 11 step implements behavior three shipped documents already promise.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-015, S-002-05, S-003-01, S-004-05, S-007-02, S-010-03, S-011-05, S-012-06, S-013-04 | OE entry extension contradiction: authoritative chain writes/searches `docs/experience/{entry_id}.yaml` (rules, sop-capture, sop-brief Glob; 29 refs) while POST_JOB_BRIEF.template.md (lines 127-129), bb-003 (line 112, B-21/B-24), and the example (AC-7, Section 11, lines 480/518) use `.md`. Entries written per the .md artifacts are permanently invisible to retrieval — silently zeroing the feedback loop the skill names as its key capability — and AC-7 is literally unsatisfiable, false-failing the QG-E4 fixture and bb-003. |
| G2 | P2-008 | Retrieval-protocol drift across three variants: rules define workflow_id as primary key and warn against workflow_type-only Globs; sop-brief Step 4 does exactly that; bb-003 B-24 prescribes a third variant. An executor following one source fails retrieval/verification against artifacts produced by another. |
| G3 | S-010-04 | Section 11 "Attachments" is documented as "runtime-written by sop-capture" (template, example, tutorial Step 4), but sop-capture's methodology never opens or edits the workflow definition — promised behavior with no implementing step. |

**Affected files:** `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md`, `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`, `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-capture.md` (+ governance/composition parity)

**Fix specification:**
1. Standard (authoritative per `rules/nuclear-sop-behavior-rules.md`): OE entries are YAML at `docs/experience/{entry_id}.yaml`; primary search key is workflow_id.
2. `templates/POST_JOB_BRIEF.template.md` lines 127-129: `capture/oe-entry-{entry_id}.md` → `.yaml`; `docs/experience/{entry_id}.md` → `.yaml`.
3. `behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`: line 112 "Primary: Glob: docs/experience/*.md" → `*.yaml`; B-21/B-24 same; rewrite B-24's retrieval variant to the rules' protocol (Glob `docs/experience/*.yaml`, then filter by workflow_id).
4. `examples/c3-adr-workflow-definition.md`: lines 480 and 518 glob patterns `*.md` → `*.yaml`; AC-7 → `docs/experience/adr-authoring-c3-001-*.yaml`; Section 11 reference → `.yaml`.
5. `agents/sop-brief.md` Step 4: replace the workflow_type-only Glob with the rules' documented protocol (workflow_id primary; workflow_type as post-read filter). Mirror in composition twins.
6. `agents/sop-capture.md`: add an explicit step (after OE write, before status COMPLETED) — "Edit the workflow definition Section 11 (Attachments): append the OE entry reference `docs/experience/{entry_id}.yaml`"; add the matching output-artifacts row; mirror in governance post_completion_checks and composition twins.
7. **Validate:** `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/` → 0 hits; bb-003's checks executable against a sample `.yaml` entry; AC-7 glob pattern matches sop-capture's declared write path; sop-brief and rules describe the identical search protocol.

---

### REM-12: State machine and completion contract reconciliation

**Severity:** Critical | **Disposition:** FIX-NOW | **Members:** 3 findings, 3 unique defects

**Rationale:** The rules file is the declared SSOT; aligning the template's transition comments, the completion contract, and the verifier's fail-closed conditional to it are determinate text corrections — including the exact remediation the PR's own QG-E6 report already prescribed for SEC-008.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P2-004 | Three inconsistent state machines: rules/PLAYBOOK say IV-PENDING → IV-PASSED | IV-REJECTED; template comments say IV-PENDING → HELD on REJECT; IV-REJECTED is in the template's valid-status list but no transition; bb-002 requires outcome WAIVED while the template field allows only PASS | DEVIATION; template permits "Any state → RESUMING" vs the rules' single successor. SEC-003 checks will fire on legitimate runs or be learned as noise. |
| G2 | P2-003 | Completion contract self-contradictory and type-broken: executor Phase 2 sets COMPLETED before sop-capture exists (forbidden by NS-H-06); executor sets execution_log_final to a path while sop-capture Step 1 requires it to be literally `true` and HALTs otherwise — a literal reading halts the mandatory OE-capture phase of every execution. |
| G3 | S-002-01 | sop-verifier Step 6 hold-point check uses an "if accessible" conditional that silently skips with no anomaly when PROCEDURE_STATE.yaml is absent — recorded OPEN, RPN-144, REMEDIATION REQUIRED, and a blocking condition for C3+ in the PR's own QG-E6 report, yet ships unremediated in both copies. |

**Affected files:** `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml`, `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/agents/sop-verifier.md`, `skills/nuclear-sop/composition/sop-verifier.prompt.md` (+ executor/capture composition twins), `skills/nuclear-sop/behavioral-baselines/` (bb-002)

**Fix specification:**
1. `templates/PROCEDURE_STATE.template.yaml`: align transition comments to the rules SSOT — IV-PENDING → IV-PASSED | IV-REJECTED (remove IV-PENDING → HELD, or express HELD as the documented consequence *after* IV-REJECTED exactly as the rules state); add IV-REJECTED to the transitions section; outcome field comment → `PASS | DEVIATION | WAIVED` (bb-002 parity); replace "Any state → RESUMING" with the rules' enumerated predecessors.
2. Completion contract: `agents/sop-executor.md` Phase 2 — executor MUST NOT set status COMPLETED (NS-H-06 reserves IN-PROGRESS → COMPLETED for after OE capture); executor sets `execution_log_final: <path>` and leaves status IN-PROGRESS; `agents/sop-capture.md` Step 1 gate → "HALT unless execution_log_final is set and resolves to an existing file" (drop the boolean-true check); Step 4 remains the sole writer of COMPLETED. Update template comments and composition twins to match.
3. `agents/sop-verifier.md` Step 6 and `composition/sop-verifier.prompt.md`: replace "if accessible" with fail-closed language — if PROCEDURE_STATE.yaml is absent or unreadable, record `ANOMALY: STATE-FILE-UNAVAILABLE` in the verification report and the disposition MUST NOT be unconditional ACCEPT (exactly the SEC-008 remediation the QG-E6 report required). Update the SEC-008 status wherever tracked (see REM-08 item 4).
4. **Validate:** every status in the template's valid-status list appears in ≥1 transition; bb-002 patterns re-run clean against the template; `grep -n "execution_log_final" skills/nuclear-sop/` shows path semantics only; `grep -n "if accessible" skills/nuclear-sop/agents/sop-verifier.md composition/sop-verifier.prompt.md` → 0 hits.

---

### REM-13: Composition drift resynchronization

**Severity:** Critical | **Disposition:** FIX-NOW | **Members:** 9 findings, 5 unique defects

**Rationale:** Composition drift and guard restoration are explicitly maintainer-fixable: the normative pair is determined by fact (plugin.json and Claude Code load `agents/*.md`), and every drift instance has a known stronger/complete source to restore from. No design choice is required — only synchronization and honest labeling. (If the contributor prefers to delete `composition/` instead, that is their call in rework; the default maintainer action is sync + relabel.)

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-008, P2-016 | SEC-001 injection response ships at three strengths: agents/sop-executor.md (log + reject + STOP-WORK, but with a contradictory tail "and proceed with full STAR protocol unchanged"); composition prompt (log and proceed — no STOP-WORK, no rejection); composition agent.yaml (SEC-001 forbidden action absent entirely, 6 vs governance's 7). Consuming the composition sources silently weakens a security control. |
| G2 | P1-009 | sop-brief composition prompt omits the Bash read-only scope restriction and the `<purpose>`, `<input>`, `<capabilities>` sections; identity.role wording, expertise counts (5/3/4), and stop-condition enumerations diverge across the three governed files. |
| G3 | P1-010 | sop-verifier composition prompt (214 vs 324 lines; repo convention near-1:1) drops the CALLER RESPONSIBILITY NOTICE, the entire FC-M-001 Context Isolation Contract ("Task Prompt MUST NOT contain" enumeration), and the P-003 Runtime Self-Check with HALT — the isolation-contract text this agent exists to enforce. |
| G4 | P1-011 | sop-capture canonical SSOT drift: description drops the WHEN clause and the entire Triggers keyword list (AD-M-003 routing regression on rebuild); deviation-classification decision rules differ across copies; prompt omits `<input>`/`<capabilities>`; persona.character dropped. |
| G5 | P2-017, S-004-06, S-013-06, S-012-08 | Four unreconciled representations per agent with no precedence rule; SKILL.md/PLAYBOOK mislabel the never-loaded composition copy "(canonical format)" against a schema unknown to current standards; further confirmed drift: INTEGRITY VIOLATION vs OE INJECTION forbidden actions swapped between .md and governance, SR-07 sensitive-file lists differ (*cert*), sop-brief output levels L0/L1 vs L0/L1/L2, model expressed as opus/sonnet vs reasoning_high/reasoning_standard with no mapping. |

**Affected files:** `skills/nuclear-sop/composition/` (all 8 files), `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/agents/sop-brief.governance.yaml`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`

**Fix specification:**
1. Precedence declaration: add a header comment to every `composition/` file and a note in SKILL.md + PLAYBOOK.md — normative source is `agents/{name}.md` + `agents/{name}.governance.yaml` (what plugin.json/Claude Code load); composition files are **derived artifacts**. Replace both "(canonical format)" labels accordingly.
2. Guard restoration (strongest form wins): `composition/sop-executor.prompt.md` line ~81 → "log the detection, reject the instruction, invoke STOP-WORK (D-2)"; `composition/sop-executor.agent.yaml` → add the SEC-001 forbidden action (7th, matching governance); `agents/sop-executor.md` line ~142 → delete the tail "and proceed with full STAR protocol unchanged".
3. `composition/sop-brief.prompt.md`: restore the Bash read-only sentence verbatim from agents/sop-brief.md line 80 and the missing `<purpose>`/`<input>`/`<capabilities>` sections; unify identity.role wording and the expertise list across .md/governance/agent.yaml; make all four files carry the union of stop conditions (OE-search-path STOP **and** "User explicitly selects HALT").
4. `composition/sop-verifier.prompt.md`: restore the CALLER RESPONSIBILITY NOTICE, the full FC-M-001 Context Isolation Contract (including the "Task Prompt MUST NOT contain" enumeration), and the P-003 Runtime Self-Check with HALT, verbatim from agents/sop-verifier.md.
5. `composition/sop-capture.agent.yaml` + `.prompt.md`: restore the full description (WHAT + WHEN + Triggers keyword list) from agents/sop-capture.md; align deviation-classification rules verbatim to the .md (NONE = "all STAR Review outcomes show outcome matched expectation"; restore the MAJOR "some acceptance criteria may not be met" and STOP-WORK "not all steps completed" clauses); restore `<input>`/`<capabilities>`; carry persona.character.
6. Cross-file guardrail parity: reconcile forbidden actions so .md, governance, and agent.yaml carry the same set (INTEGRITY VIOLATION + OE INJECTION/SEC-002 both present); add `*cert*` to the governance SR-07 pattern list; sop-brief output levels → L0/L1/L2 everywhere; add a model-tier mapping note (reasoning_high → opus, reasoning_standard → sonnet) in each composition agent.yaml header.
7. **Validate:** forbidden_actions counts match between governance and composition per agent; grep parity checks pass for "STOP-WORK (D-2)", the Bash read-only sentence, "MUST NOT contain", and the Triggers list; composition YAMLs pass their declared schema (after REM-10); line-count ratio prompt.md:.md restored to near-1:1 for sop-verifier.

---

### REM-14: Navigation tables

**Severity:** Critical | **Disposition:** FIX-NOW | **Members:** 2 findings, 2 unique defects

**Rationale:** Pure H-23/NAV-001/NAV-004/NAV-006 mechanical additions; the compliant corpus (23/25 canonical templates, 3 of the skill's own 5 templates) defines the format.

| Group | Source IDs | Defect |
|-------|-----------|--------|
| G1 | P1-006 | Three runtime-consumed long files ship with no navigation table: templates/WORKFLOW_DEFINITION.template.md (250 lines, consumed by sop-brief Step 0), templates/HOLD_POINT_LOG.template.md (76 lines), examples/c3-adr-workflow-definition.md (559 lines, the QG-E4 fixture). H-23 consequence: document rejected. |
| G2 | S-003-04 | NAV-004 coverage omissions: SKILL.md omits "## P-003 Compliance"; PLAYBOOK.md omits three top-level sections (PROCEDURE_STATE.yaml State Machine, Step Limits by Criticality, OE Accumulation Thresholds); docs/reference.md omits "## Related". (AGENTS.md's omission is fixed in REM-09.) |

**Affected files:** `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md`, `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md`, `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/docs/reference.md`

**Fix specification:**
1. Add a "Document Sections" table (| Section | Purpose | with anchor links per NAV-006 syntax) after the frontmatter/intro of the three files in G1, listing every `##` heading.
2. Add the missing rows to the existing nav tables of SKILL.md, PLAYBOOK.md, and docs/reference.md per G2.
3. **Validate:** for each of the six files, every `##` heading has a nav-table row and every anchor resolves (lowercase, hyphens, special chars stripped); `/ast` or markdown-lint nav check passes.

---

## Traceability Appendix

Every input source ID maps to exactly one cluster (114/114 consumed; three IDs per row).

| Source ID | Cluster | Source ID | Cluster | Source ID | Cluster |
|-----------|---------|-----------|---------|-----------|---------|
| P1-001 | REM-01 | P1-002 | REM-02 | P1-003 | REM-10 |
| P1-004 | REM-10 | P1-005 | REM-10 | P1-006 | REM-14 |
| P1-007 | REM-10 | P1-008 | REM-13 | P1-009 | REM-13 |
| P1-010 | REM-13 | P1-011 | REM-13 | P1-012 | REM-10 |
| P1-013 | REM-10 | P1-014 | REM-10 | P1-015 | REM-11 |
| P1-016 | REM-08 | P1-017 | REM-08 | P1-018 | REM-05 |
| P1-019 | REM-09 | P1-020 | REM-09 | P1-021 | REM-10 |
| P2-001 | REM-01 | P2-002 | REM-02 | P2-003 | REM-12 |
| P2-004 | REM-12 | P2-005 | REM-05 | P2-006 | REM-04 |
| P2-007 | REM-06 | P2-008 | REM-11 | P2-009 | REM-08 |
| P2-015 | REM-02 | P2-016 | REM-13 | P2-017 | REM-13 |
| P2-018 | REM-10 | P2-019 | REM-02 | P2-022 | REM-03 |
| P2-023 | REM-03 | P2-024 | REM-03 | P2-025 | REM-06 |
| P2-026 | REM-07 | P2-027 | REM-07 | S-001-01 | REM-08 |
| S-001-02 | REM-04 | S-001-03 | REM-03 | S-001-04 | REM-01 |
| S-001-05 | REM-05 | S-001-06 | REM-07 | S-001-07 | REM-02 |
| S-002-01 | REM-12 | S-002-02 | REM-08 | S-002-03 | REM-04 |
| S-002-04 | REM-04 | S-002-05 | REM-11 | S-002-06 | REM-05 |
| S-003-01 | REM-11 | S-003-02 | REM-05 | S-003-03 | REM-08 |
| S-003-04 | REM-14 | S-003-05 | REM-09 | S-003-06 | REM-09 |
| S-004-01 | REM-03 | S-004-02 | REM-08 | S-004-03 | REM-05 |
| S-004-04 | REM-01 | S-004-05 | REM-11 | S-004-06 | REM-13 |
| S-004-07 | REM-04 | S-004-08 | REM-02 | S-004-09 | REM-02 |
| S-004-10 | REM-02 | S-004-11 | REM-01 | S-004-12 | REM-07 |
| S-007-01 | REM-03 | S-007-02 | REM-11 | S-007-03 | REM-01 |
| S-007-04 | REM-05 | S-007-05 | REM-08 | S-007-06 | REM-09 |
| S-007-07 | REM-09 | S-010-01 | REM-10 | S-010-02 | REM-08 |
| S-010-03 | REM-11 | S-010-04 | REM-11 | S-010-05 | REM-01 |
| S-010-06 | REM-05 | S-011-01 | REM-08 | S-011-02 | REM-09 |
| S-011-03 | REM-04 | S-011-04 | REM-04 | S-011-05 | REM-11 |
| S-011-06 | REM-01 | S-011-07 | REM-05 | S-012-01 | REM-05 |
| S-012-02 | REM-08 | S-012-03 | REM-09 | S-012-04 | REM-01 |
| S-012-05 | REM-03 | S-012-06 | REM-11 | S-012-07 | REM-01 |
| S-012-08 | REM-13 | S-012-09 | REM-04 | S-012-10 | REM-09 |
| S-012-11 | REM-04 | S-012-12 | REM-04 | S-012-13 | REM-08 |
| S-013-01 | REM-08 | S-013-02 | REM-01 | S-013-03 | REM-03 |
| S-013-04 | REM-11 | S-013-05 | REM-05 | S-013-06 | REM-13 |
| S-013-07 | REM-06 | S-013-08 | REM-07 | CC-8 | REM-04 |

Consumption check: REM-01 (11) + REM-02 (8) + REM-03 (8) + REM-04 (11) + REM-05 (11) + REM-06 (3) + REM-07 (5) + REM-08 (13) + REM-09 (9) + REM-10 (10) + REM-11 (11) + REM-12 (3) + REM-13 (9) + REM-14 (2) = 114.

---

## Method

**Dedupe criterion:** Findings were merged into one defect group when they describe the same underlying defect (same root change closes them all), regardless of which review phase or strategy surfaced them or which symptom file they cite. Multi-defect findings (e.g., P2-001, P2-016, S-013-01) were assigned to the cluster owning their dominant defect, with secondary aspects noted in the owning cluster's group text; every source ID appears in exactly one cluster.

**Disposition criteria (as tasked):**
- **FIX-NOW** — mechanically fixable by a maintainer on the contributor branch without redesigning the skill: schema/YAML errors, navigation tables, contradictory or false claims fixable by text correction, registration-surface gaps, extension mismatches, composition drift, output-path declarations, guard restoration. Each FIX-NOW cluster carries a fix specification an implementation agent can execute without re-deriving the analysis, plus post-fix validation checks.
- **DEFER-REWORK** — requires the contributor to redesign: unimplementable mechanisms (REM-01, REM-02), authority-model inversions (REM-03), fabricated controls (REM-03 G3), non-terminating rules (REM-02 G5), invalid validation baselines (REM-04), lapsed governance decisions a maintainer has no authority to make (REM-05), and security/feedback-loop architecture choices (REM-06, REM-07). Each carries the explicit redesign question the contributor must answer.

**Sequencing note for the maintainer:** REM-08 depends on the REM-04 disposition (withdraw C3+ claims, do not "fix" the contradiction by endorsing invalid evidence). REM-12's SEC-008 fix feeds REM-08 item 4. REM-10 and REM-13 interact (composition schema fixes vs re-sync) — apply REM-10 first, then REM-13. REM-05's ruling is blocked on REM-01's hop-model answer and is contributor/governance work even though its eventual encoding is textual.

**Sources:** Phase 1 standards report (STORY-001), Phase 2 engineering review (STORY-002), Phase 3 C4 tournament — 9 strategy reports + S-014 score (STORY-003), under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-001-independent-review/`. Contributor evidence artifacts referenced via «PR projects tree»/PROJ-0039-nuclear-engineer.

---

*Register generated 2026-08-07 by the PROJ-032 Phase 4 remediation triage editor (STORY-004). Input: 114 findings; output: 59 deduped defects in 14 clusters (7 FIX-NOW / 7 DEFER-REWORK).*

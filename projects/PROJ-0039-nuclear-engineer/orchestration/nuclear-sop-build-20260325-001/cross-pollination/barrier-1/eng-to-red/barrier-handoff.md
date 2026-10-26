# BARRIER-1 Handoff: ENG to RED

> **From Agent:** eng-backend-001 through eng-backend-004b (ENG Phase 3 fan-out, consolidated)
> **To Agent:** red-recon-001 (RED Phase 2: Reconnaissance & Attack Surface)
> **Barrier:** BARRIER-1
> **Date:** 2026-03-31
> **Criticality:** C3
> **Confidence:** 0.88

## Document Sections

| Section | Purpose |
|---------|---------|
| [Task](#task) | What red-recon-001 is being asked to do |
| [Success Criteria](#success-criteria) | Verifiable criteria for RED Phase 2 output |
| [Artifacts](#artifacts) | All files delivered for attack surface mapping |
| [Key Findings](#key-findings) | Orientation from ENG Phases 1-3 |
| [Architecture Summary](#architecture-summary) | Trust boundaries and attack surfaces identified by eng-architect |
| [Blockers](#blockers) | Known impediments |

---

## Task

Conduct reconnaissance and attack surface mapping of the built `/nuclear-sop` skill. All 15 skill files (16th is a deferred example) have been implemented and quality-gated through ENG Phase 3. The secure architecture design (ENG Phase 1) identified 19 threats across 4 attack surfaces with 3 Critical, 13 High, and 3 Medium DREAD ratings. RED Phase 1 engagement scope defines the authorized targets, technique allowlist, and rules of engagement.

Your task: map all input vectors, trust boundaries, data flows, OE injection points, and PROCEDURE_STATE.yaml mutation points across the built skill files. Identify any gaps between the architecture's threat model and the actual implementation.

## Success Criteria

1. All input vectors to each of the 4 agents (sop-brief, sop-executor, sop-verifier, sop-capture) are documented with source and trust level
2. Trust boundaries TB-1 through TB-6 (from secure-architecture-design.md Section 1.2) and TB-1 through TB-7 (from engagement-scope.md Data Flow Analysis) are validated against actual agent definitions — confirm each boundary exists as designed or document deviations. Note: the two source documents use slightly different TB numbering; reconcile during recon.
3. PROCEDURE_STATE.yaml data flow is traced end-to-end: which agents write, which read, what fields, and where mutation can occur
4. OE entry injection points are enumerated: how data enters docs/experience/ via sop-capture and how it re-enters via sop-brief's OE retrieval
5. File path handling across TB-4 (executor to verifier) is assessed for path injection risk per threat T-2.5
6. Attack surface map covers all 5 vulnerability categories from engagement scope: safety bypass, procedural integrity loss, feedback loop poisoning, prompt injection, trust boundary violations

## Artifacts

### Skill Files (15 built, 1 deferred)

| # | File Path | Type | Security Relevance |
|---|-----------|------|-------------------|
| 1 | `skills/nuclear-sop/SKILL.md` | Skill definition | Routing keywords, activation conditions |
| 2 | `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` | Behavioral rules | HARD/MEDIUM enforcement rules |
| 3 | `skills/nuclear-sop/agents/sop-brief.md` | Agent definition | Input processing, OE retrieval, workflow validation |
| 4 | `skills/nuclear-sop/agents/sop-brief.governance.yaml` | Governance | Tool tier T2, forbidden actions |
| 5 | `skills/nuclear-sop/agents/sop-executor.md` | Agent definition | STAR protocol, hold points, place-keeping |
| 6 | `skills/nuclear-sop/agents/sop-executor.governance.yaml` | Governance | Tool tier T2 with Bash |
| 7 | `skills/nuclear-sop/agents/sop-verifier.md` | Agent definition | Context-isolated verification |
| 8 | `skills/nuclear-sop/agents/sop-verifier.governance.yaml` | Governance | Tool tier T1 read-only |
| 9 | `skills/nuclear-sop/agents/sop-capture.md` | Agent definition | OE capture, deviation classification |
| 10 | `skills/nuclear-sop/agents/sop-capture.governance.yaml` | Governance | Tool tier T2 |
| 11 | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` | Template | User-authored input vector (Critical) |
| 12 | `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md` | Template | Briefing output structure |
| 13 | `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` | Template | OE capture output structure |
| 14 | `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` | Template | Hold point sign-off record |
| 15 | `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` | Template | Execution state schema (Critical) |
| 16 | `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` | Example | Deferred to ENG Phase 4 |

### ENG Phase Artifacts (reference)

| Artifact | Path (relative to project) | Relevance |
|----------|---------------------------|-----------|
| Secure architecture design | `orchestration/nuclear-sop-build-20260325-001/eng/phase-1/eng-architect-001/secure-architecture-design.md` | STRIDE threat model, 19 threats, trust boundaries, DREAD scores |
| Implementation plan | `orchestration/nuclear-sop-build-20260325-001/eng/phase-2/eng-lead-001/implementation-plan.md` | File assignments, H-34/H-35 compliance plan |
| ENG Phase 3 review (001) | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-001/implementation-review.md` | SKILL.md + rules review (structurally verified) |
| ENG Phase 3 review (002) | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-002/implementation-review.md` | sop-brief review (structurally verified) |
| ENG Phase 3 review (003) | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-003/implementation-review.md` | sop-executor review (structurally verified) |
| ENG Phase 3 review (004a) | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-004a/implementation-review.md` | sop-verifier review (0.94 PASS) |
| ENG Phase 3 review (004b) | `orchestration/nuclear-sop-build-20260325-001/eng/phase-3/eng-backend-004b/implementation-review.md` | sop-capture review (0.93 PASS) |

### RED Phase 1 Artifact (reference)

| Artifact | Path (relative to project) | Relevance |
|----------|---------------------------|-----------|
| Engagement scope | `orchestration/nuclear-sop-build-20260325-001/red/phase-1/red-lead-001/engagement-scope.md` | Authorized targets, technique allowlist, agent authorizations |

### Upstream Research Artifacts (reference)

| Artifact | Path (relative to project) | Relevance |
|----------|---------------------------|-----------|
| Synthesis spec | `orchestration/nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md` | Complete skill specification (0.922) |
| ADR-001 | `orchestration/nuclear-sop-research-20260319-001/ps/phase-3/ps-architect-001/ADR-001-nuclear-sop-skill-architecture.md` | Architecture decisions (0.933) |

## Key Findings

1. **Three Critical-rated threats dominate the attack surface:** T-1.2 (prompt injection via workflow definitions, DREAD 34), T-4.1 (OE feedback poisoning, DREAD 29 elevated to Critical), T-2.1 (hold point bypass via state file manipulation, DREAD 29 elevated to Critical). All three have behavioral-only mitigations — no deterministic computational gates.

2. **STAR self-checking is probabilistic, not deterministic.** The architecture explicitly acknowledges this (secure-architecture-design.md, L0 Executive Summary, "Security Posture Overview" — "STAR self-checking as a behavioral constraint, not a deterministic gate"). All STAR mitigations operate at the prompt level within sop-executor's inference pass. RED Phase 2 should map exactly how step descriptions flow into STAR's Think phase to identify rationalization attack vectors.

3. **TB-4 path injection is a designed-in risk.** sop-executor passes file paths to sop-verifier. The architecture notes (Section 1.2, TB-4) that these paths originate from the executor and may be injection-controlled. sop-verifier is instructed to independently resolve expected output paths, but verify whether the implementation actually does this.

4. **OE feedback loop creates a temporal attack surface (TB-5 -> TB-6).** A poisoned OE entry from one execution can corrupt all subsequent executions of the same workflow type. The architecture estimates up to 20 executions could be affected before detection (SD-02 blast radius). Verify the OE schema enforcement in sop-capture actually prevents unstructured injection.

5. **sop-executor has Bash access (T2).** While scoped to test/build commands, the Bash tool enables repository-wide file writes. The T2 tier prevents network access and subagent spawning, but the blast radius of a successful prompt injection includes arbitrary file writes within the repository.

## Architecture Summary

### Trust Boundaries

| ID | From | To | Data | Risk Level | Source |
|----|------|----|------|-----------|--------|
| TB-1 | User | sop-brief | Workflow definition (markdown) | Critical | Both |
| TB-2 | sop-brief | sop-executor | Pre-job brief artifact path | Medium | Both |
| TB-3 (ENG) | sop-executor | PROCEDURE_STATE.yaml | Execution state mutations | High | ENG arch |
| TB-3 (RED) | sop-executor | sop-capture | Execution log + state | High | RED scope |
| TB-4 | sop-executor | sop-verifier | Work product file paths only | Medium (path injection per T-2.5) | Both |
| TB-5 (ENG) | sop-capture | docs/experience/ | OE entries with mandatory schema | High (persistent) | ENG arch |
| TB-5 (RED) | User | sop-executor | Hold point responses (APPROVE/REJECT/WAIVE) | Low | RED scope |
| TB-6 (ENG) | docs/experience/ | sop-brief | Prior OE entries as context | High (temporal feedback) | ENG arch |
| TB-6 (RED) | sop-verifier | sop-capture | IV report path | Low | RED scope |
| TB-7 | OE entry | future sop-brief | Temporal feedback loop (cascading contamination) | Critical (elevated, SD-02) | RED scope |

> **Note:** ENG architecture (secure-architecture-design.md) and RED engagement scope (engagement-scope.md) use overlapping but distinct TB numbering for boundaries TB-3 through TB-7. Both schemas are included above with source attribution. red-recon-001 should reconcile these during attack surface mapping.

### PROCEDURE_STATE.yaml Field Summary

The mutable execution state file controls hold point enforcement and place-keeping. Key fields for attack surface analysis:

| Field Group | Key Fields | Mutation By | Security Relevance |
|-------------|-----------|-------------|-------------------|
| Execution Status | `status` (state machine: 9 states, 2 terminal) | sop-executor | Controls execution flow; unauthorized transition bypasses hold points |
| Place-Keeping | `current_step`, `next_step`, `steps_completed[]` | sop-executor (per-step, never batched) | Step skipping if manually modified |
| Hold Point State | `hold_type`, `hold_resolution`, `held_at_step` | sop-executor (activation), user/ps-critic/sop-verifier (release) | Hold bypass if `hold_resolution` set without proper release mechanism |
| IV State | `iv_scope[]`, `iv_disposition`, `iv_iteration` | sop-executor (scope), sop-verifier (disposition) | Path injection via `iv_scope`; disposition tampering |
| QG State | `qg_iteration`, `qg_scores[]` | sop-executor (iteration), ps-critic (scores) | Score falsification |
| Timestamps | `started_at`, `last_updated`, `completed_at` | sop-executor | Tamper detection via consistency checking |

### Agent Tool Tiers

| Agent | Tier | Key Capabilities | Key Restrictions |
|-------|------|-------------------|-----------------|
| sop-brief | T2 | Read, Write, Edit, Glob, Grep | No Task, no WebSearch, no Bash |
| sop-executor | T2 | Read, Write, Edit, Glob, Grep, Bash | No Task, no WebSearch |
| sop-verifier | T1 | Read, Glob, Grep | No Write, no Edit, no Bash, no Task |
| sop-capture | T2 | Read, Write, Edit, Glob, Grep | No Task, no WebSearch, no Bash |

## Expected Output

| Artifact | Path |
|----------|------|
| Attack surface map | `orchestration/nuclear-sop-build-20260325-001/red/phase-2/red-recon-001/attack-surface-map.md` |

Reference the engagement scope's attack vector hypotheses section for per-phase attack surface enumeration to ensure coverage alignment.

## Blockers

- None. All ENG Phase 3 sub-agents have completed and their outputs are structurally verified. RED Phase 1 engagement scope is complete with authorization pending user acknowledgment before RED Phase 2 proceeds (per scope document signature section).

---

*Handoff produced by orchestrator at BARRIER-1 checkpoint CP-004.*
*Quality gate: pending adv-executor-barrier-1 tournament review.*

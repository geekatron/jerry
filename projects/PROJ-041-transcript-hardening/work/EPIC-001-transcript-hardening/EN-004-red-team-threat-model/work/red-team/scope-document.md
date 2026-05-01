# Engagement Scope Document — RT-PROJ041-001

> **Engagement ID:** RT-PROJ041-001
> **Engagement Type:** Code-and-design red-team engagement (NOT a live-network pentest)
> **Authoring Agent:** red-lead
> **Status:** ACTIVE — Phase 1 only
> **Authored:** 2026-04-30
> **Parent Enabler:** EN-004 `/red-team` threat model on entire `/transcript` skill
> **Methodology:** PTES Pre-Engagement Interactions, STRIDE threat modeling, MITRE ATT&CK technique mapping

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Engagement Overview](#engagement-overview) | Engagement ID, window, phase posture |
| [Engagement Window](#engagement-window) | Start, Phase 1 close condition, Phase 4 deferral |
| [Authorized Targets](#authorized-targets) | The 10 attack surfaces in scope |
| [In-Scope Activities (Phase 1 Only)](#in-scope-activities-phase-1-only) | What red-team agents may do this session |
| [Prohibited Actions](#prohibited-actions) | What MUST NOT happen, with consequences |
| [Authorized Agents](#authorized-agents) | Phase 1 agent roster and RoE-gated agents |
| [Rules of Engagement](#rules-of-engagement) | Escalation, communication, emergency stop |
| [Evidence Handling](#evidence-handling) | Storage, retention, disclosure controls |
| [Methodology References](#methodology-references) | PTES, STRIDE, ATT&CK |
| [Phase 4 Deferral Notice](#phase-4-deferral-notice) | What is explicitly NOT authorized today |
| [Approval](#approval) | red-lead signature line |

---

## Engagement Overview

| Field | Value |
|-------|-------|
| Engagement ID | RT-PROJ041-001 |
| Engagement Title | `/transcript` skill threat model — pre-implementation Phase 1 |
| Parent Enabler | EN-004 |
| Parent Epic | EPIC-001 (transcript hardening) |
| Origin | Issue #273 (external packet audit); EN-004 Authorized Scope section |
| Branch under engagement | `feat/PROJ-041-transcript-hardening` only |
| Engagement type | Code-and-design red-team — methodology guidance, threat modeling, recon of source artifacts. NOT a live-network penetration test. |
| Authorization basis | EN-004 commencement constitutes explicit user authorization for Phase 1 threat model on the `/transcript` skill surface within this branch only. |

This engagement is bounded to the source code, design documents, JSON sidecar samples, and CI workflow definitions present in the working repository. No external systems, no production targets, no third-party services are in scope.

---

## Engagement Window

| Phase | Start | End | Status |
|-------|-------|-----|--------|
| Phase 1 — Threat Model | 2026-04-30 | When red-reporter Phase 1 handoff document (`work/red-team/phase-1-handoff-to-eng-team.md`) is delivered to /eng-team and acknowledged | ACTIVE |
| Phase 4 — Validation / Exploit Attempts | NOT YET AUTHORIZED | NOT YET AUTHORIZED | DEFERRED — re-authorization required |

**Phase 1 close condition (single):** the red-reporter Phase 1 handoff lands at the path above with EN-004 acceptance criteria satisfied for Phase 1 (recon-existing, recon-new, STRIDE model, attack-paths, handoff). When that handoff lands, this scope is automatically considered closed for Phase 1; Phase 4 remains explicitly out of scope.

**Phase 4 deferral:** Phase 4 (live exploit attempts against built artifacts: SubprocessSandbox bypasses, atomic-write race probe, prompt-injection probe) requires a NEW or AMENDED scope document to be authored by red-lead and re-signed by the user when FEAT-003 implementations land. This document does NOT authorize Phase 4 activity.

---

## Authorized Targets

The following 10 attack surfaces are copied verbatim from EN-004 §Attack Surface Inventory and constitute the complete authorized target set for Phase 1. No additional surfaces may be added without an amendment to this document signed by red-lead.

| # | Surface | Existing? | New (per FEAT-003)? | Authorized Agents |
|---|---------|-----------|---------------------|-------------------|
| 1 | VTT/SRT file ingestion | Yes | — | red-recon, red-vuln |
| 2 | Audio file ingestion | Yes | — | red-recon, red-vuln |
| 3 | JSON sidecar parsing (`extraction-report.json`, `_anchors.json`, etc.) | Yes | — | red-vuln, red-exploit (analysis only — no execution this phase) |
| 4 | Markdown packet writing (rendered .md files) | Yes | — | red-vuln |
| 5 | ts-formatter agent prompts (LLM injection risk) | Yes | — | red-social (prompt-injection methodology only — no live probe) |
| 6 | `SubprocessSandbox` (bash command execution from JSON-supplied patterns) | — | Yes | red-exploit (analysis only — no execution this phase) |
| 7 | `verify` CLI subcommand surface | — | Yes | red-exploit (analysis only) |
| 8 | `update-anchors` CLI subcommand surface (atomic write, race conditions) | — | Yes | red-exploit, red-vuln (analysis only) |
| 9 | `ts-formatter` post-render hook (process boundary) | — | Yes | red-vuln, red-privesc (analysis only) |
| 10 | CI workflow secrets exposure | — | Yes | red-vuln |

**Source-of-truth boundary:** for surfaces marked "Yes" under Existing, the in-scope artifacts are the source files reachable from `skills/transcript/` and any sample sidecars under `test_data/` in this branch. For surfaces marked "Yes" under New, the in-scope artifacts are FEAT-003 design documents and stub interfaces drafted in this branch. No surface outside this list is authorized.

---

## In-Scope Activities (Phase 1 Only)

Phase 1 is a **paper engagement**. Activities are limited to:

| Activity | Lead Agent(s) | Allowed? |
|----------|---------------|----------|
| Methodology research (PTES, STRIDE, ATT&CK technique mapping) | red-lead, red-recon, red-vuln | Yes |
| Reconnaissance of existing surface — read source files, design docs, sample JSON sidecars in this branch | red-recon | Yes |
| Reconnaissance of planned new surface — read FEAT-003 design drafts in this branch | red-recon | Yes |
| STRIDE threat modeling across all 10 surfaces | red-vuln | Yes |
| Attack-path analysis — theoretical exploit chains, written as design analysis | red-vuln | Yes |
| Documenting bypass classes that Phase 4 should attempt | red-vuln, red-exploit | Yes |
| Producing handoff document for /eng-team consumption | red-reporter | Yes |
| Writing/editing files inside `work/red-team/` | All Phase 1 agents | Yes |

---

## Prohibited Actions

The following actions are FORBIDDEN during this engagement. Each violation triggers immediate engagement halt and escalation per [Rules of Engagement](#rules-of-engagement).

| # | Prohibition | Consequence of violation |
|---|-------------|--------------------------|
| P-1 | NEVER access live production systems of any kind. | Out-of-scope action; legal/ethical boundary breach; engagement halts. |
| P-2 | NEVER access third-party services not under the user's control (no live SaaS endpoints, no external APIs, no GitHub Actions executions outside this branch's CI). | Unauthorized external interaction; engagement halts. |
| P-3 | NEVER conduct social engineering of contributors, maintainers, or any human. This is a code/methodology engagement, not a human one. | Manipulation classifier violation; trust erosion; engagement halts. |
| P-4 | NEVER publicly disclose findings (no public issue comments, no blog posts, no social media) until coordinated with the maintainer (adam.nowak). | Premature disclosure; coordination violation; engagement halts. |
| P-5 | NEVER execute exploits in Phase 1. Methodology guidance and theoretical attack chains only — no payloads run, no commands executed beyond reading source files in this branch. | Phase boundary violation; converts paper engagement to live operation without authorization. |
| P-6 | NEVER attempt SubprocessSandbox bypass execution, atomic-write race probing, or prompt-injection probing in Phase 1. These belong to Phase 4 and are explicitly deferred. | Phase boundary violation; engagement halts; mandatory red-lead review before any further activity. |
| P-7 | NEVER modify code outside `work/red-team/` during this engagement. Findings inform design — they do not edit production code paths directly. | Scope-creep; mixes red-team output with engineering output; engagement halts. |
| P-8 | NEVER include findings linked to other PROJ-NNN identifiers. Cross-project isolation is mandatory. | Cross-project leakage; engagement halts. |
| P-9 | NEVER include absolute machine paths (POSIX home-directory paths, Windows drive-letter paths) in any deliverable. Repo-relative paths only. Architecture-validation tests will reject the commit otherwise. | Provenance leak; deliverable rejected; pre-commit hook fails. |
| P-10 | NEVER spawn recursive subagents (P-003). All red-team agents are workers; only MAIN CONTEXT orchestrates. | Constitutional violation; agent hierarchy breach. |

---

## Authorized Agents

Only the agents listed below are authorized to operate under this scope. RoE-gated agents are explicitly disabled for Phase 1.

| Agent | Phase 1 Authorized? | Phase 1 Role | Notes |
|-------|---------------------|--------------|-------|
| red-lead | Yes | This document; mid-phase scope assessment if SCOPE_REVIEW_REQUIRED is raised | Mandatory first agent |
| red-recon | Yes | Reconnaissance of existing + planned new surfaces | Read-only on source files |
| red-vuln | Yes | STRIDE threat model + attack-path analysis | Analysis only; no probing |
| red-reporter | Yes | Phase 1 handoff to /eng-team | Mandatory final Phase 1 agent |
| red-exploit | Phase 1: ANALYSIS ONLY | Document bypass classes for Phase 4 | NO exploit execution |
| red-privesc | Phase 1: ANALYSIS ONLY | ts-formatter process-boundary review | NO privilege escalation attempts |
| red-lateral | Not authorized | — | No lateral movement scenarios in scope |
| red-persist | Not authorized (RoE-GATED, denied) | — | `persistence_authorized: false` |
| red-exfil | Not authorized (RoE-GATED, denied) | — | `exfiltration_authorized: false` |
| red-social | Phase 1: METHODOLOGY ONLY | Document prompt-injection methodology against ts-formatter for Phase 4 | NO live prompt-injection probe; `social_engineering_authorized: false` for live activity |
| red-infra | Not authorized | — | No C2/redirector/payload infrastructure required |

---

## Rules of Engagement

| RoE Field | Value |
|-----------|-------|
| Escalation contact | adam.nowak (maintainer) |
| Emergency stop | Maintainer command in this session OR any Critical-classified finding (see escalation path) |
| Communication channel | This Claude Code session; persisted artifacts in `work/red-team/`; GitHub issues only after maintainer review |
| `social_engineering_authorized` | false |
| `persistence_authorized` | false |
| `exfiltration_authorized` | false |
| `live_exploitation_authorized` | false (Phase 4 only, when re-authorized) |
| `data_types_permitted` | Source code in this branch; sample JSON sidecars in `test_data/`; design documents under `projects/PROJ-041-transcript-hardening/`. No live transcripts, no real meeting recordings. |

### Escalation Path (mandatory)

1. Any agent that classifies a finding as **Critical** MUST:
   1. Halt its current operation.
   2. Persist the finding to its current output file with the `[CRITICAL]` prefix.
   3. Surface a `SCOPE_REVIEW_REQUIRED` flag back to the orchestrator (MAIN CONTEXT).
   4. The orchestrator MUST notify the user (adam.nowak) and pause subsequent red-team agents until the user acknowledges.
2. Any ambiguity about target boundary, technique applicability, or whether an action belongs to Phase 1 vs Phase 4 routes back to red-lead before further activity.
3. Any apparent need to expand the 10-surface authorized target list requires this document to be amended and re-signed before the new surface is touched.

### Circuit Breaker

A circuit-breaker check occurs at every agent transition during Phase 1:

1. Is the target still one of the 10 authorized surfaces?
2. Is the activity still within the Phase 1 in-scope activity table?
3. Is the next agent in the authorized-agents list with the correct Phase 1 role?
4. Has any prior agent raised SCOPE_REVIEW_REQUIRED?

Any failed check halts the engagement and routes back to red-lead.

---

## Evidence Handling

| Field | Value |
|-------|-------|
| Storage location | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/` (this directory only) |
| File naming convention | `{phase}-{topic}.md` for analysis docs; `phase-1-handoff-to-eng-team.md` for the final Phase 1 handoff |
| Allowed deliverables | This scope document; recon docs; STRIDE threat model; attack-paths analysis; Phase 1 handoff |
| Retention | Retained for the lifetime of EPIC-001 and merged into `main` along with the rest of PROJ-041 deliverables |
| Destruction | None during the engagement. Post-merge, artifacts persist as part of the project record. |
| Disclosure | Findings linked from GitHub issues ONLY after maintainer review. No public disclosure pre-coordination per P-4. |
| Provenance hygiene | Repo-relative paths only (per P-9); no cross-project IDs (per P-8). |

---

## Methodology References

| Framework | Use |
|-----------|-----|
| PTES Pre-Engagement Interactions | Source for this scope document's structure and Rules of Engagement |
| STRIDE | Threat-modeling taxonomy red-vuln applies across all 10 surfaces |
| MITRE ATT&CK | Technique-ID citations for documented attack chains and bypass classes (Phase 1 documents techniques; Phase 4 attempts them) |
| OWASP (relevant categories: A03 Injection, A05 Security Misconfiguration, A08 Software & Data Integrity) | Cross-reference for ingestion-path and CI-workflow surfaces |

Phase 1 produces methodology and analysis. It does NOT produce weaponized exploit code, raw payloads, or autonomous tool execution. This is consistent with `/red-team` AD-001 (Methodology-First Design) and the `Methodology guidance, not exploit generation` posture from `skills/red-team/SKILL.md`.

---

## Phase 4 Deferral Notice

The following activities are EXPLICITLY OUT OF SCOPE under this document and require a separate scope amendment signed by red-lead and the user:

- Live exploit attempts against `SubprocessSandbox` (any of the 5+ bypass classes documented during Phase 1).
- Live atomic-write race-condition probing of `update-anchors`.
- Live prompt-injection probes against `ts-formatter` agent prompts.
- Any execution of arbitrary commands, payloads, or shell snippets discovered or theorized during Phase 1.
- Any activation of `red-persist`, `red-exfil`, or `red-lateral`.

When FEAT-003 implementations land and Phase 4 is to be initiated, red-lead MUST author a new scope document (suggested ID: `RT-PROJ041-002`) that authorizes those activities, and the user MUST re-sign it before any Phase 4 agent operates.

---

## Approval

| Role | Authority | Date | Confirmation |
|------|-----------|------|--------------|
| red-lead | Engagement Lead & Scope Authority for `/red-team` | 2026-04-30 | This scope document is authored and active for Phase 1 of EN-004 only. Phase 4 is explicitly deferred. All red-team agents operating under RT-PROJ041-001 must validate against this document at every transition. |
| User (maintainer: adam.nowak) | Engagement authorizer (per EN-004 commencement) | 2026-04-30 | EN-004 commencement = explicit user authorization for Phase 1. Recorded in `EN-004-red-team-threat-model.md` History line "2026-04-30 ... in_progress ... Phase 1 (red-lead → red-recon → red-vuln → red-reporter) in scope this session." |

---

*Document Version: 1.0.0*
*Engagement: RT-PROJ041-001*
*Phase: 1 of 2 (Phase 4 deferred)*
*Authoring Agent: red-lead*
*Constitutional Compliance: P-001, P-002, P-003, P-020, P-022; R-020 (scope verification)*
*SSOT: EN-004 §Attack Surface Inventory; `skills/red-team/SKILL.md` §Mandatory Authorization*

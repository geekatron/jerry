# EN-004: `/red-team` threat model on entire `/transcript` skill

> **Type:** enabler
> **Enabler Type:** exploration
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | Two-phase engagement methodology |
| [Authorized Scope](#authorized-scope) | RoE for /red-team engagement |
| [Attack Surface Inventory](#attack-surface-inventory) | What's in scope |
| [Phase 1 Activities (Threat Model)](#phase-1-activities-threat-model) | Pre-implementation |
| [Phase 4 Activities (Validation)](#phase-4-activities-validation) | Post-implementation |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

Per user direction: **"The scope should be on everything we do, which include the author's gist as well as the existing paths."** This Enabler runs `/red-team` against the full `/transcript` attack surface — both the existing ingestion paths (VTT/SRT/audio, JSON sidecars, Markdown rendering) and the new validator surface (`SubprocessSandbox`, JSON-supplied bash patterns, write pipelines). Scope is authorized via `red-lead` engagement document before any other red-team agent operates.

This Enabler runs in two phases:
1. **Phase 1 (parallel with FEAT-001)** — Threat model the design before implementation begins. Findings inform EN-001 (DDD scaffolding), EN-003 (SubprocessSandbox), STORY-005..STORY-010 (all subprocess-touching stories).
2. **Phase 4 (after FEAT-003 implementations)** — Exploit attempts against built artifacts. Validates sandbox boundary, attempts bypass classes documented in Phase 1 threat model.

---

## Technical Approach

Two-phase /red-team engagement: Phase 1 (parallel with FEAT-001) threat-models the design before implementation; findings inform EN-001/EN-003 architecture and STORY-005..010 subprocess paths. Phase 4 (after FEAT-003 implementation) executes exploit attempts against built artifacts to validate the sandbox boundary. Authorization is gated by `red-lead` engagement document; methodology follows PTES + STRIDE + ATT&CK.

---

## Authorized Scope

| Item | Status |
|------|--------|
| `red-lead` engagement document | REQUIRED before any other red-team agent operates (skill mandatory first agent) |
| Authorization | This Enabler's commencement = explicit authorization for Phase 1 threat model and Phase 4 verification on the `/transcript` skill surface within this branch only |
| Out of scope | Live production systems, third-party services not under this user's control, social engineering of contributors (this is a code/methodology engagement, not a human one) |
| RoE | Findings stay in this project's `work/` directory + linked GitHub issues; no public disclosure until coordinated with maintainer |

---

## Attack Surface Inventory

| Surface | Existing? | New? | Threat agents |
|---------|-----------|------|--------------|
| VTT/SRT file ingestion | Yes | — | red-recon, red-vuln |
| Audio file ingestion | Yes | — | red-recon, red-vuln |
| JSON sidecar parsing (`extraction-report.json`, `_anchors.json`, etc.) | Yes | — | red-vuln, red-exploit |
| Markdown packet writing (rendered .md files) | Yes | — | red-vuln |
| ts-formatter agent prompts (LLM injection risk) | Yes | — | red-social (prompt injection methodology) |
| `SubprocessSandbox` (bash command execution from JSON-supplied patterns) | — | Yes | red-exploit |
| `verify` CLI subcommand surface | — | Yes | red-exploit |
| `update-anchors` CLI subcommand surface (atomic write, race conditions) | — | Yes | red-exploit, red-vuln |
| `ts-formatter` post-render hook (process boundary) | — | Yes | red-vuln, red-privesc |
| CI workflow secrets exposure | — | Yes | red-vuln |

---

## Phase 1 Activities (Threat Model)

| Activity | Lead Agent | Output |
|----------|-----------|--------|
| Engagement scope authorization | red-lead | Scope document with RoE |
| Reconnaissance: existing surface enumeration | red-recon | `work/red-team/recon-existing-surface.md` |
| Reconnaissance: planned new surface (per FEAT-003 design) | red-recon | `work/red-team/recon-new-surface.md` |
| STRIDE threat model (existing + new combined) | red-vuln | `work/red-team/stride-threat-model.md` |
| Attack path analysis: most-likely exploit chains | red-vuln | `work/red-team/attack-paths.md` |
| Findings handoff to /eng-team | red-reporter | `work/red-team/phase-1-handoff-to-eng-team.md` |

---

## Phase 4 Activities (Validation)

After EN-003 SubprocessSandbox + STORY-005..010 land:

| Activity | Lead Agent | Output |
|----------|-----------|--------|
| Exploit attempts against SubprocessSandbox (5+ bypass classes) | red-exploit | `work/red-team/sandbox-exploit-attempts.md` |
| Atomic-write race condition probe | red-exploit | `work/red-team/atomic-write-probe.md` |
| Prompt injection probe against ts-formatter | red-social | `work/red-team/prompt-injection-probe.md` |
| Final engagement report | red-reporter | `work/red-team/engagement-report.md` |

---

## Agent Assignment

**Phase 1 (Threat Model — informs design):**

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/red-team` | `red-lead` | **MANDATORY first agent** — author engagement scope document with RoE; no other red-team agent operates without active scope |
| 2 | `/red-team` | `red-recon` | Reconnaissance of existing surface (VTT/SRT/audio ingestion, JSON sidecars) + planned new surface (subprocess, CLI) |
| 3 | `/red-team` | `red-vuln` | STRIDE threat model + attack-path analysis covering all 10 surfaces in the inventory |
| 4 | `/red-team` | `red-reporter` | Phase 1 handoff to /eng-team (consumed by EN-001 design and EN-003 SubprocessSandbox shape) |

**Phase 4 (Validation — exploit attempts on built artifacts):**

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 5 | `/red-team` | `red-exploit` | Exploit attempts against SubprocessSandbox: ≥5 bypass classes (command injection, path traversal, env poisoning, symlink escape, resource exhaustion) |
| 6 | `/red-team` | `red-exploit` | Atomic-write race condition probe on update-anchors |
| 7 | `/red-team` | `red-social` | Prompt injection probe against ts-formatter (testing whether malicious VTT/JSON content can manipulate the agent) |
| 8 | `/red-team` | `red-reporter` | Final engagement report; classify findings (Critical/Major/Minor); remediation status |

**Closure:**

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 9 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review on threat model + remediation set |
| 10 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] Phase 1 deliverables exist with red-lead authorization.
- [ ] STRIDE threat model covers all 10 surfaces from inventory above.
- [ ] Phase 1 handoff document delivered to /eng-team before EN-001 design starts.
- [ ] EN-003 SubprocessSandbox design incorporates findings from Phase 1.
- [ ] Phase 4 sandbox exploit attempts: minimum 5 distinct bypass classes attempted; all blocked with evidence.
- [ ] Phase 4 atomic-write probe shows no race condition / partial-write window.
- [ ] Phase 4 prompt injection probe documented; mitigations applied where viable.
- [ ] Final engagement report classifies all findings (Critical/Major/Minor) with remediation status.
- [ ] All Critical findings remediated before EN-008 final adversary tournament.
- [ ] `/adversary` C4 ≥0.95 review on the threat model + remediation set.

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-175](./TASK-175-engagement-scope-document.md) | Author engagement scope document with Rules of Engagement | `red-lead` | pending |
| [TASK-176](./TASK-176-phase-1-recon-existing-surface.md) | Phase 1 reconnaissance: existing surface enumeration | `red-recon` | pending |
| [TASK-177](./TASK-177-phase-1-recon-new-surface.md) | Phase 1 reconnaissance: planned new surface (per FEAT-003 design draft) | `red-recon` | pending |
| [TASK-178](./TASK-178-phase-1-stride-threat-model.md) | Phase 1 STRIDE threat model + attack-path analysis | `red-vuln` | pending |
| [TASK-179](./TASK-179-phase-1-handoff-to-eng-team.md) | Phase 1 handoff to /eng-team | `red-reporter` | pending |
| [TASK-180](./TASK-180-phase-4-sandbox-bypass-attempts.md) | Phase 4 exploit attempts against SubprocessSandbox: ≥5 bypass classes | `red-exploit` | pending |
| [TASK-181](./TASK-181-phase-4-atomic-write-race-probe.md) | Phase 4 atomic-write race condition probe on update-anchors | `red-exploit` | pending |
| [TASK-182](./TASK-182-phase-4-prompt-injection-probe.md) | Phase 4 prompt injection probe against ts-formatter | `red-social` | pending |
| [TASK-183](./TASK-183-final-engagement-report.md) | Final engagement report: all findings classified (Critical/Major/Minor) with remediation | `red-reporter` | pending |
| [TASK-184](./TASK-184-run-adversary-c4-on-threat-model.md) | Run /adversary C4 review on threat model + remediation set | `adv-executor` | pending |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | EN-001 | Phase 1 findings inform DDD scaffolding |
| Blocks | EN-003 | Phase 1 findings inform SubprocessSandbox design |
| Blocks | FEAT-003 STORY-005, STORY-008 | Atomic-write probe gates story acceptance |
| Blocks | EN-008 | Final tournament cannot run while Critical findings open |

### Source

- User direction: "scope on everything we do, including author's gist + existing paths"
- [#273 comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — gist subprocess execution surface

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Cross-cutting Enabler created. Two-phase engagement (pre-design threat model + post-implementation validation). |
| 2026-04-30 | adam.nowak (via Claude) | in_progress | Opened. Wave 0 critical-path entry point. Phase 1 (red-lead → red-recon → red-vuln → red-reporter) in scope this session. Phase 4 deferred until FEAT-003 implementations land. |
| 2026-04-30 | adam.nowak (via Claude) | in_progress | Phase 1 deliverables produced (steps 1-4 of Agent Assignment): red-lead authored engagement scope `RT-PROJ041-001` with Rules of Engagement covering 10 surface inventory verbatim — see `work/red-team/scope-document.md`. red-recon produced existing-surface and new-surface recon docs (10 surfaces total; 10 design questions for /eng-team enumerated in new-surface) — see `work/red-team/recon-existing-surface.md` and `recon-new-surface.md`. red-vuln produced STRIDE threat model (60 cells, 10 surfaces × 6 categories, 3×3 ordinal scoring, ATT&CK mappings) and attack-path analysis (5 chains, mitigation priority list) — see `work/red-team/stride-threat-model.md` and `attack-paths.md`. red-reporter produced Phase 1 handoff to /eng-team — 5 CRITICAL + 7 HIGH findings forwarded; 27 design constraints across EN-001 (7), EN-003 (8), STORY-009 (4), STORY-012 (4), and cross-cutting (4); 4 acceptance blockers flagged for downstream entities — see `work/red-team/phase-1-handoff-to-eng-team.md`. Step 9 /adversary C3 review returned API stream idle timeout (partial response from adv-scorer; no verdict written). Phase 1 scoring will be retried next session; once it passes ≥0.95, Phase 1 is "closed" but EN-004 remains in_progress until Phase 4 lands (post-FEAT-003). Phase 4 will require fresh scope authorization (suggested `RT-PROJ041-002`). |

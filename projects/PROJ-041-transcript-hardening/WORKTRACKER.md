# PROJ-041-transcript-hardening — Work Tracker

> Harden `/transcript` skill against the gaps surfaced in the external packet audit (issue #273). Make output deterministically validated.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Work Items](#work-items) | Full hierarchy as flat table |
| [Hierarchy Tree](#hierarchy-tree) | Visual decomposition |
| [Cross-cutting Enablers](#cross-cutting-enablers) | Project-level enablers (under Epic, not Feature) |
| [Closure Rule](#closure-rule) | Evidence requirements for closing entities |
| [Source Provenance](#source-provenance) | Mapping each entity to its origin in issue #273 |

---

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EPIC-001 | Epic | `/transcript` Skill Hardening from External Packet Audit | pending | PROJ-041 |
| FEAT-001 | Feature | ADR-007 Foundation & Governance | pending | EPIC-001 |
| STORY-001 | Story | Vendor ADR-007 from jerry-core to public docs/adrs/ | pending | FEAT-001 |
| STORY-002 | Story | Promote ADR-007 status PROPOSED → ACCEPTED | pending | FEAT-001 |
| FEAT-002 | Feature | Framework-Internal Contradictions Cleanup | pending | EPIC-001 |
| BUG-001 | Bug | Token caps disambiguation: 2K/5K vs 5K/8K | pending | FEAT-002 |
| BUG-002 | Bug | chunk_id regex divergence | pending | FEAT-002 |
| BUG-003 | Bug | domain regex: 3 disagreeing schemas | pending | FEAT-002 |
| BUG-004 | Bug | seg-NNN regex: ADR-007 \d{3} vs schemas \d{3,} | pending | FEAT-002 |
| BUG-005 | Bug | Backlinks format direct contradiction (ADR-003 vs ADR-007) | pending | FEAT-002 |
| FEAT-003 | Feature | Deterministic Substrate Validation | pending | EPIC-001 |
| EN-001 | Enabler | DDD scaffolding for transcript/validation operation | pending | FEAT-003 |
| EN-002 | Enabler | Test harness + golden packets in test_data/ | pending | FEAT-003 |
| EN-003 | Enabler | SubprocessSandbox port + adapter (security boundary) | pending | FEAT-003 |
| STORY-003 | Story | Implement FILE-001..003 validators | pending | FEAT-003 |
| STORY-004 | Story | Implement CONTENT-001..003 validators | pending | FEAT-003 |
| STORY-005 | Story | Implement ANCHOR-001..003 validators | pending | FEAT-003 |
| STORY-006 | Story | Implement SCHEMA-001..008 validators | pending | FEAT-003 |
| STORY-007 | Story | jerry transcript verify CLI subcommand | pending | FEAT-003 |
| STORY-008 | Story | jerry transcript update-anchors CLI subcommand | pending | FEAT-003 |
| STORY-009 | Story | Wire verify into ts-formatter post-render hook | pending | FEAT-003 |
| STORY-010 | Story | Wire update-anchors into ts-formatter write pipeline | pending | FEAT-003 |
| STORY-011 | Story | Update ts-critic-extension.md to consume validator output | pending | FEAT-003 |
| STORY-012 | Story | CI workflow runs validators against golden packets | pending | FEAT-003 |
| FEAT-004 | Feature | Schema Extensions | pending | EPIC-001 |
| STORY-013 | Story | Add provenance.editorial_conventions block | pending | FEAT-004 |
| STORY-014 | Story | Add arithmetic_invariants for stat blocks | pending | FEAT-004 |
| STORY-015 | Story | Add discussions[] as 5th entity type | pending | FEAT-004 |
| STORY-016 | Story | Add provenance.audit_basis for cross-sidecar discoverability | pending | FEAT-004 |
| FEAT-005 | Feature | Mindmap Hardening | pending | EPIC-001 |
| BUG-006 | Bug | ts-mindmap-mermaid bracket-escaping fails parse | pending | FEAT-005 |
| BUG-007 | Bug | ts-mindmap-mermaid false self-claim of syntax validity | pending | FEAT-005 |
| EN-004 | Enabler | /red-team threat model on entire /transcript skill | pending | EPIC-001 |
| EN-005 | Enabler | /user-experience JTBD + feedback exploration | pending | EPIC-001 |
| EN-006 | Enabler | /diataxis documentation pass | pending | EPIC-001 |
| EN-007 | Enabler | /orchestration plan + sync barriers | pending | EPIC-001 |
| EN-008 | Enabler | Final /adversary C4 tournament | pending | EPIC-001 |

---

## Hierarchy Tree

```
PROJ-041-transcript-hardening
└── EPIC-001 (transcript skill hardening)
    ├── EN-004 (/red-team threat model) ─────────────┐
    ├── EN-005 (/user-experience JTBD + feedback) ───┤  cross-cutting,
    ├── EN-006 (/diataxis documentation pass) ───────┤  ride alongside features
    ├── EN-007 (/orchestration plan + barriers) ─────┤
    ├── EN-008 (final /adversary C4 tournament) ────┘
    │
    ├── FEAT-001 (ADR-007 Foundation & Governance)
    │   ├── STORY-001 (vendor ADR-007 to docs/adrs/)
    │   └── STORY-002 (promote PROPOSED → ACCEPTED)
    │
    ├── FEAT-002 (Contradictions Cleanup)
    │   ├── BUG-001 (token caps)
    │   ├── BUG-002 (chunk_id regex)
    │   ├── BUG-003 (domain regex)
    │   ├── BUG-004 (seg-NNN regex)
    │   └── BUG-005 (backlinks format)
    │
    ├── FEAT-003 (Deterministic Substrate Validation)
    │   ├── EN-001 (DDD scaffolding)
    │   ├── EN-002 (test harness + golden packets)
    │   ├── EN-003 (SubprocessSandbox)
    │   ├── STORY-003 (FILE-* validators)
    │   ├── STORY-004 (CONTENT-* validators)
    │   ├── STORY-005 (ANCHOR-* validators)
    │   ├── STORY-006 (SCHEMA-* validators)
    │   ├── STORY-007 (jerry transcript verify CLI)
    │   ├── STORY-008 (jerry transcript update-anchors CLI)
    │   ├── STORY-009 (wire verify into post-render hook)
    │   ├── STORY-010 (wire update-anchors into write pipeline)
    │   ├── STORY-011 (update ts-critic-extension.md)
    │   └── STORY-012 (CI workflow vs golden packets)
    │
    ├── FEAT-004 (Schema Extensions)
    │   ├── STORY-013 (editorial_conventions)
    │   ├── STORY-014 (arithmetic_invariants)
    │   ├── STORY-015 (discussions[])
    │   └── STORY-016 (audit_basis)
    │
    └── FEAT-005 (Mindmap Hardening)
        ├── BUG-006 (bracket escaping)
        └── BUG-007 (false self-claim)
```

---

## Cross-cutting Enablers

These enablers sit directly under the Epic (not under any Feature) because they apply across all five Features.

| ID | Title | Skill | Phase |
|----|-------|-------|-------|
| EN-004 | `/red-team` threat model on entire `/transcript` skill (existing VTT/SRT/audio ingestion + new validator subprocess surface + JSON injection) | `/red-team` | 1 (parallel) + 4 (verify) |
| EN-005 | `/user-experience` exploration: JTBD on packet consumers + feedback synthesis from external audit + persona-spectrum review for CLI consumers (UX orchestrator routes to sub-skills) | `/user-experience` | 1 (parallel) |
| EN-006 | `/diataxis` documentation pass: tutorial for new validators, how-to for verify/update-anchors, reference for ADR-007 §4 rule catalog, explanation for substrate-coupling design | `/diataxis` | 7 |
| EN-007 | `/orchestration` plan: phase definitions, sync barriers, `/adversary` C4 ≥0.95 gates between phases, criticality propagation | `/orchestration` | 0 (precedes all execution) |
| EN-008 | Final `/adversary` C4 tournament against the merged Epic deliverable | `/adversary` | 8 (acceptance) |

---

## Closure Rule

Per user direction: **"Entities cannot be closed out unless they provide delivery evidence."** Every entity's `History` section must record at minimum:

| Evidence Class | What Goes In History |
|----------------|----------------------|
| Code changes | Commit SHA(s), files modified, lines added/removed |
| Test runs | Test command, pass/fail summary, coverage percentage if relevant |
| Validator runs | `verify` exit code, drift count, before/after snapshot |
| Adversary scores | S-014 weighted composite, dimension breakdown, iteration count |
| ADR amendments | ADR file path, decision recorded, status field updated |
| External refs | GitHub Issue/PR link, comment URL where evidence is published |
| Cross-repo work | Source path (jerry-core) + destination path (this branch) |

WTI-005 enforced: **no completed status without concrete evidence.** A status change to `completed` without a corresponding evidence row in History is an integrity violation and must be reverted to `in_progress`.

---

## Source Provenance

Every entity here traces to a specific line item in [#273](https://github.com/geekatron/jerry/issues/273) or one of its comments. This table is the audit trail.

| Entity | Issue #273 Source |
|--------|-------------------|
| FEAT-001, STORY-001 | Body §C1 |
| FEAT-001, STORY-002 | Body §C2 |
| FEAT-002, BUG-001 | Body §C4.1 |
| FEAT-002, BUG-002 | Body §C4.2 |
| FEAT-002, BUG-003 | Body §C4.3 |
| FEAT-002, BUG-004 | Body §C4.4 |
| FEAT-002, BUG-005 | Body §C4.5 |
| FEAT-003 (rule families) | Body §C5 (17 rule IDs already specified in ADR-007 §4) |
| STORY-007, STORY-008 | [Comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — declared-derived coupling diagnostic + working CLI prototype |
| STORY-009, STORY-010 | [Comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — proposal items 2 and 3 (post-render hook, write pipeline) |
| FEAT-004, STORY-013 | Body §C3.1 |
| FEAT-004, STORY-014 | Body §C3.2 |
| FEAT-004, STORY-015 | Body §C3.3 |
| FEAT-004, STORY-016 | [Comment 2](https://github.com/geekatron/jerry/issues/273#issuecomment-4339392440) — extraction-report.json schema gap |
| FEAT-005, BUG-006 | [Comment 3](https://github.com/geekatron/jerry/issues/273#issuecomment-4339778594) — Mermaid bracket-escaping (concrete defect, reproduction provided) |
| FEAT-005, BUG-007 | [Comment 3](https://github.com/geekatron/jerry/issues/273#issuecomment-4339778594) — agent self-claim doesn't match capability |
| EN-004 | User direction: red-team scope = "everything we do, including author's gist + existing paths" |
| EN-005 | User direction: UX exploration "to see if there are angles we are missing" |
| EN-006 | Standard /diataxis post-build documentation |
| EN-007 | User direction: "ok to add /orchestration" |
| EN-008 | User direction: "/adversary C4 ≥0.95 protocol" |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | created | Initial worktracker hierarchy authored. 1 Epic + 5 Features + 5 cross-cutting Enablers + 16 Stories + 7 Bugs + 3 in-feature Enablers = 37 entities total. All entities are individually broken out per user direction (no lumping). |

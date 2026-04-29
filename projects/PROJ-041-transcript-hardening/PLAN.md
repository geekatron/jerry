# PROJ-041-transcript-hardening — Plan

> Harden the `/transcript` skill by closing the gaps surfaced in the external packet audit (issue #273): governance debt, framework-internal contradictions, non-deterministic output validation, schema gaps, and rendering bugs. End-state: transcript output is automatically and deterministically validated at every write — no LLM-judged spec compliance.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mission](#mission) | Project intent in one paragraph |
| [Origin](#origin) | What triggered this project |
| [Scope](#scope) | What's in |
| [Out of Scope](#out-of-scope) | What's deferred or excluded |
| [Success Criteria](#success-criteria) | Acceptance for the project as a whole |
| [Quality Bar](#quality-bar) | Adversary protocol applied throughout |
| [Skills Inventory](#skills-inventory) | Skills employed and their roles |
| [Working Repository Notes](#working-repository-notes) | Cross-repo file copy from jerry-core |
| [Risk Register](#risk-register) | Known risks at project start |
| [References](#references) | Source documents and external references |

---

## Mission

Make `/transcript` output **deterministically validated**. Today, transcript packets ship with a `_anchors.json.audit_breakdown.per_bucket_derivation` block that publishes both *declared counts* and *grep one-liners that should reproduce them* — but nothing mechanically reconciles the two. Drift accumulates silently, every fix wave introduces small new defects, and `/adversary` reviews plateau at ~0.90 because LLM judgement cannot mechanically grep-walk packet substrate. We are eliminating that gap by: (1) packaging the governing ADR-007 with the public release, (2) resolving five framework-internal contradictions, (3) implementing the 17 ADR-007 §4 validation rules as runnable scripts, (4) wiring those validators into the `ts-formatter` write pipeline so substrate is mechanically derived rather than hand-attested, and (5) closing schema and render bugs surfaced by the same audit.

---

## Origin

External audit by [@anowak-delinea](https://github.com/anowak-delinea) — 9 iterations of `/adversary` C4 review on a real ~30-minute technical session. Composite plateaued at 0.900 (below 0.95 target) at "0 Criticals" because each fix wave introduced small new defects in the same surface (substrate drift, ASR convention inconsistency, declared-vs-walked count mismatches). Post-mortem: ~one-third of structural elements had been agent-introduced during fix waves, **0 used a sanctioned framework extension mechanism — because none currently exists for entity-type or schema extensions**.

| Source | Detail |
|--------|--------|
| GitHub Issue #273 | "meta: 5 transcript-skill improvements identified in external packet audit" — 5 items in body + 3 additional findings in comments |
| Working CLI prototype | [Public gist](https://gist.github.com/anowak-delinea/f6748192a6e32bb65c874cd0e5dde924) — ~200 lines of stdlib Python; `verify` and `update-anchors` sub-commands; reference, not literal port |

---

## Scope

| Cluster | Items |
|---------|-------|
| **F1 — ADR-007 Foundation & Governance** | Vendor ADR-007 from `jerry-core` to public `docs/adrs/` (C1). Promote ADR-007 status `PROPOSED → ACCEPTED` (C2). |
| **F2 — Framework-Internal Contradictions Cleanup** | Token caps disambiguation (C4.1). `chunk_id` regex convergence (C4.2). `domain` regex convergence — 3 schemas (C4.3). `seg-NNN` regex loosening (C4.4). Backlinks format (C4.5). |
| **F3 — Deterministic Substrate Validation** | DDD-disciplined validation operation within `/transcript` bounded context. 17 ADR-007 §4 rule IDs (FILE-, CONTENT-, ANCHOR-, SCHEMA-) implemented as runnable validators. `jerry transcript verify` and `update-anchors` CLI subcommands. Integration into `ts-formatter` post-render hook and write pipeline. CI workflow against golden packets. `ts-critic-extension.md` updated to consume deterministic output. |
| **F4 — Schema Extensions** | `provenance.editorial_conventions` block (C3.1). `arithmetic_invariants` for stat blocks (C3.2). `discussions[]` as 5th entity type (C3.3). `provenance.audit_basis` for cross-sidecar discoverability (comment 2). |
| **F5 — Mindmap Hardening** | HTML-entity escape brackets in `ts-mindmap-mermaid` node labels (B1). Remove false syntax-validity self-claim or grant render capability (B2). |
| **Cross-cutting Enablers** | `/red-team` threat model (existing + new surface). `/user-experience` JTBD + feedback synthesis. `/diataxis` documentation pass. `/orchestration` plan + sync barriers. Final `/adversary` C4 tournament. |

---

## Out of Scope

- Issue #274 (`/adversary` template improvements) — explicitly deferred per user direction.
- Wholesale rewrite of `/transcript` — we are hardening, not redesigning.
- Migration from VTT/SRT to other transcript formats — no format additions.
- Real-time transcript ingestion — batch ingestion only.
- LLM-based extraction quality improvements — separate concern from substrate validation.
- Mindmap rendering parity with non-Mermaid environments — `ts-mindmap-ascii` already handles fallback.

---

## Success Criteria

1. **Governance:** ADR-007 ships in public `docs/adrs/` with status `ACCEPTED`, all 5 framework-internal contradictions resolved, no remaining cross-document disagreement on canonical rules.
2. **Determinism:** All 17 ADR-007 §4 rule IDs are runnable, deterministic checks. Validators pass against golden packets in `test_data/`. `ts-formatter` post-render hook runs `verify` before declaring completion. `update-anchors` produces declared counts as a cache of walked truth.
3. **Schema closure:** All 4 schema extensions land in `extraction-report.json` v1.2, schemas validate, golden packets demonstrate the new shapes.
4. **Render correctness:** Bracketed canonical forms in mindmap labels render without parse error in `mmdc`. Agent self-claim of "Mermaid syntax: Valid" either backed by render or weakened to scope-honest language.
5. **Quality:** Final `/adversary` C4 tournament against the merged Epic deliverable scores ≥0.95 weighted composite.
6. **Evidence:** Every entity in this project has concrete delivery evidence in its History section — file paths, commit/PR refs, validator outputs, adversary scores. WTI-005 enforced.

---

## Quality Bar

Every Story, Enabler, and Bug closes only on demonstrable evidence. Per [`worktracker-content-standards.md`](../../skills/worktracker/rules/worktracker-content-standards.md) and the user-stated rule: **entities cannot be closed out unless they provide delivery evidence.**

| Gate | Threshold | Mechanism |
|------|-----------|-----------|
| Phase boundaries | `/adversary` C4 ≥0.95 | adv-selector + adv-executor + adv-scorer using S-014 LLM-as-Judge with the 6-dimension rubric |
| Entity closure | WTI-005 evidence | Concrete file paths, commits, test runs, adversary scores in History |
| Final gate | `/adversary` C4 tournament ≥0.95 + `/eng-team eng-reviewer` final gate | Both gates must pass before the Epic closes |

The user has explicit standing direction: **"stop generating garbage — outputs need to be validated automatically. This should be deterministic."** This is the non-negotiable spirit of this project.

---

## Skills Inventory

| Skill | Role | Phase(s) |
|-------|------|----------|
| `/orchestration` | Pipeline architecture, phase definitions, sync barriers, state tracking | Throughout |
| `/problem-solving` | Codebase research, root-cause analysis, cross-source synthesis, ADR authoring | Phases 1, 2, 5 |
| `/eng-team` | Threat-informed architecture, implementation, secure coding, QA, DevSecOps, security review, final gate | Phases 2, 4, 5, 6, 8 |
| `/red-team` | Scope authorization, threat model on existing + new validator surface, attack paths, vulnerability analysis | Phases 1, 4 (verify) |
| `/user-experience` | JTBD on `/transcript` consumers, feedback synthesis from external audit, persona-spectrum review for CLI consumers | Phase 1 |
| `/diataxis` | Tutorial, how-to, reference, explanation for new validators and schema extensions; classifier + auditor | Phase 7 |
| `/adversary` | Strategy selection, execution, S-014 LLM-as-Judge scoring; phase-boundary gates and final tournament | Phase boundaries + Phase 8 |
| `/worktracker` | Entity scaffolding, hierarchy integrity, evidence tracking, audit | Throughout |

`/nasa-se` and `/pm-pmm` are **not** in scope for this project per user direction.

---

## Working Repository Notes

- **This branch:** `feat/PROJ-041-transcript-hardening` — landing point for all changes (created as a git worktree off `main`).
- **ADR-007 source location** (separate repository, not this one): the jerry-core repository contains the canonical ADR under its own transcript-skill project's `FEAT-006-output-consistency/docs/decisions/` path. F1-S1 STORY-001 implementer resolves the exact path against the user's local jerry-core checkout and copies the file into `docs/adrs/ADR-007-output-template-specification.md` here.
- **Source issue:** [#273](https://github.com/geekatron/jerry/issues/273) — every entity created here must link back to its provenance line item in #273.

---

## Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R-01 | Subprocess execution surface in validator becomes injection vector (gist runs `bash -c {pattern}` from JSON) | High | High | F3-E3 SubprocessSandbox with command allowlist + path-traversal guard + timeout; `/red-team` validates before F3 stories close |
| R-02 | C4 governance changes (F1-S2) lock contradictions into baselined ADR before F2 resolves them | Medium | High | Strict ordering: F2 (all 5 bugs) MUST close before F1-S2 promotion. Enforced as orchestration sync barrier. |
| R-03 | Schema additions (F4) land before validators (F3) and create unvalidated drift | Medium | Medium | F3-S1..S4 (rule families) must include schema-aware checks. F4 stories add validators for new fields as part of acceptance. |
| R-04 | `ts-formatter` write-pipeline integration regresses existing packet generation | Medium | High | F3-E2 golden packets locked before integration. CI gate (F3-S10) detects regression on every change. |
| R-05 | C5 implementation deviates from gist semantics, breaking compatibility with author's prototype | Low | Low | Gist is reference, not literal port. Compatibility via shared rule IDs and schemas, not file shape. |
| R-06 | UX exploration (EP-E2) surfaces angles requiring re-scoping mid-project | Medium | Medium | Run UX in Phase 1 (early). Allow Epic re-scoping at Phase 1 sync barrier; lock scope at Phase 2 entry. |
| R-07 | Cross-repo ADR copy (F1-S1) loses provenance metadata or links | Low | Medium | F1-S1 acceptance includes verification that all internal cross-references resolve in the new location. |

---

## References

| Source | Path |
|--------|------|
| Issue #273 (this project's origin) | https://github.com/geekatron/jerry/issues/273 |
| Author's CLI prototype (reference, not literal port) | https://gist.github.com/anowak-delinea/f6748192a6e32bb65c874cd0e5dde924 |
| ADR-007 source (jerry-core) | The canonical ADR lives in a separate jerry-core repository under its transcript-skill project's `FEAT-006-output-consistency/docs/decisions/` path. STORY-001 implementer resolves exact path against the local jerry-core checkout. |
| `/transcript` skill | `skills/transcript/SKILL.md` |
| `/adversary` skill | `skills/adversary/SKILL.md` |
| Quality SSOT | `.context/rules/quality-enforcement.md` |
| Worktracker rules | `skills/worktracker/rules/` |
| Project worktracker | `projects/PROJ-041-transcript-hardening/WORKTRACKER.md` |
| Orchestration plan | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/plans/PLAN-001-orchestration.md` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | created | Project scaffolded from #273 audit findings; Epic + 5 Features + cross-cutting enablers authored; orchestration plan drafted. Awaiting user switch to this worktree to begin actual work. |

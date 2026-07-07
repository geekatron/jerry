# Author Notes — ADR-adversary-tournament-protocol-001

> Owner: ps-architect. Commission: FU.12 (2026-07-07) — "make an ADR for how to improve the `/adversary` tournament methodology, including design diagrams so that we can then review and create work items and GH-issue to enhance the skill and process."
> P-002 incremental. P-003 no subagents. P-020: writes confined to `projects/PROJ-031-cowork-skeleton/`. P-022: cite file+line; label inference.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mandate](#mandate) | What was commissioned and the guardrails |
| [Evidence Corpus Read](#evidence-corpus-read) | Files read in full, with the load-bearing datum from each |
| [Decision Scaffolding](#decision-scaffolding) | D-1..D-6 option sets and chosen options |
| [Diagram Plan](#diagram-plan) | 4 figures, mmdc validation status |
| [Dogfooding Note](#dogfooding-note) | Scheme B first-ADR-born-canonical |
| [Hygiene](#hygiene) | Path + employer-internal scan |

## Mandate

Author an evidence-led Nygard ADR that decides how to improve the `/adversary` tournament
methodology. Options-analysis first. 4 mmdc-validated Mermaid diagrams. Work-item decomposition
feeding a user review → GH-issue pass. NO HARD-rule changes (ceiling 25/25 untouched); all
implementation MEDIUM-tier. PROPOSED status pending user approval.

## Evidence Corpus Read

18 tournament rounds across 2 packages (~250 agent invocations). Read in full:

| File | Load-bearing datum |
|------|--------------------|
| adr-convention .../iteration-005/s-014-quality-score.md | 0.66 REVISE; 10 unresolved Criticals across 4 blind reviewers; the additive-remediation-spiral diagnosis |
| adr-convention .../iteration-008/s-014-quality-score.md | 0.62 REVISE; 10/10 prior Criticals CLOSED (8 delete, 2 edit), 0 recurred — yet 7 NEW Criticals surfaced (non-convergent fresh stream) |
| adr-convention .../iteration-009/s-014-quality-score.md | VERIFIED protocol 0.86 vs old-protocol 0.68; 10 claimed → 5 VERIFIED / 5 REFUTED via 3-lens 2-of-3 panels; +0.18 quantified panel value |
| adr-convention .../iteration-010/s-014-quality-score.md | Verified 0.88 vs old 0.68; 6 claimed → 0 VERIFIED / 6 REFUTED unanimous-ish; hit RT-M-010 10-round ceiling; grandfather seam re-derived by 4 strategies (recurrence = real but immaterial) |
| adr-convention .../iteration-010/post-ceiling-fix-notes.md | The fabricated-verification incident: "no PR template — Glob-verified" FALSE (lowercase `.github/pull_request_template.md` existed since 2026-02-18); survived iters 6-9, caught only by iter-10 refutation panel (RT-001-iter010) |
| adr-convention .../subtraction-pass-notes.md | Subtraction doctrine + disposition-table pattern; per-round CLOSED-BY-DELETION/EDIT/DISCLOSURE ledger; residual register R-1..R-18 |
| fu-log .../iteration-006/s-014-quality-score.md | 0.46 DECLINING, ESCALATE; 6 straight zero-regression rounds + fresh Criticals each round; wording-only fixes close instances but not the class |
| fu-log .../iteration-008/s-014-quality-score.md | VERIFIED 0.72 vs old 0.51; panels CONFIRMED 6 real Criticals incl. DA-002-i8 (fix-INTRODUCED regression, 3-of-3 unanimous); PM-001-iter8 REFUTED 0-of-3 as restatement of closed FM-006 |
| fu-log .../iteration-008/post-tournament-fix-notes.md | DA-002-i8 detail: dedup fix keyed on location-only silently dropped edited markers; new-append remediation |
| skills/adversary/SKILL.md | Current tournament groups A–F; adv-selector/executor/scorer; Group F ALWAYS LAST |
| skills/adversary/agents/adv-scorer.md | Current automatic-REVISE rule (line 166-167): "Any Critical finding → automatic REVISE regardless of score" — the rule the verified protocol refines |
| skills/adversary/agents/adv-selector.md | Group ordering A–F; AE auto-escalation |
| .context/templates/adversarial/TEMPLATE-FORMAT.md | 8-section template format; new verification template must conform |
| .context/rules/quality-enforcement.md | Strategy Catalog, Implementation section, H-13/H-14/RT-M-010; NO changes proposed to HARD rules |
| docs/knowledge/exemplars/templates/adr.md | Nygard structure used for this ADR |

## Decision Scaffolding

- **D-1 Verify stage:** Chosen **(C) criticality-proportional** (C4 full panels; C3 panels on Criticals only; C1-C2 none). 3 lenses (factual / materiality / remediation-value), 2-of-3 majority, DEFAULT-REFUTED, blind to each other. Rejected (A) status-quo, (B) always-on (cost), (D) scorer-side (not independent — the load-bearing property).
- **D-2 Severity gating:** Only panel-VERIFIED Criticals auto-REVISE; disclosed residuals = valid posture; refuted = zero dimension weight; dual-protocol transparency during transition.
- **D-3 Remediation doctrine:** Subtraction-first; disposition table first-class; owner-first routing unchanged.
- **D-4 Stop conditions:** Convergence discriminator (recurrence=real, fresh-stream=artifact→switch to verified protocol or stop); plateau; RT-M-010 unchanged; escalate-to-user at ceiling.
- **D-5 Scorer continuity:** Mandatory delta-reconciliation; anti-leniency retained.
- **D-6 Implementation surface:** New **adv-verifier** agent (T1 read-only, blind, one invocation per lens) over verification-mode-of-adv-executor; new `s-016-refutation-panel.md` template; SKILL.md + adv-scorer + adv-selector edits; quality-enforcement.md Implementation-section pointer. MEDIUM-tier. Zero HARD-rule changes.

## Diagram Plan

| Fig | Type | Content | mmdc |
|-----|------|---------|------|
| 1 | flowchart | Tournament pipeline A→F with Verify stage inserted | VALIDATED (mmdc 11.12.0, standalone + inline) |
| 2 | stateDiagram-v2 | Finding lifecycle: claimed → panel[verified/refuted] → remediated/disclosed-residual + auto-REVISE gate | VALIDATED |
| 3 | flowchart (decision tree) | Stop-condition / convergence discriminator | VALIDATED |
| 4 | flowchart (swimlane-style) | One-iteration sequence: owner/finders/panels/scorer | VALIDATED |

Both the standalone `.mmd` sources and the ADR's inline ```mermaid fences render (4/4 each) with
mmdc 11.12.0. Rendered SVGs persisted in this `diagrams/` directory.

## Dogfooding Note

This is the FIRST ADR born under the ratified Scheme B convention (ADR-PROJ031-004):
subject-encoded canonical id `ADR-adversary-tournament-protocol-001`, born in project
`decisions/`, promotes to `docs/design/` by pure `git mv` (id unchanged, zero citation churn).
Explicitly recorded in the ADR's Meta-Note.

## Hygiene

All outputs use repo-relative paths; zero home-directory absolute paths; zero employer-internal
tokens. Re-scanned before final reply: ADR clean (0/0), notes clean (0/0).

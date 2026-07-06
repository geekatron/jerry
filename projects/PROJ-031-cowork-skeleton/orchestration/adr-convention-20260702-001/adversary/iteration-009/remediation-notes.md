# Iteration-9 Remediation Notes — Owner-First Pass (post-score 0.86, gate 0.95)

> Owner: ps-architect (creator/owner). Mandate: remediate ONLY the 5 panel-VERIFIED Criticals.
> Doctrine (binding): subtract, don't compensate — text/disclosure first; no new machinery; adding requires deleting bigger.
> Constitutional: P-003 no subagents; P-020 within mandate (only the 2 deliverables + notes edited); P-022 cite file+line, label inference.

## Verified findings in scope (panel-confirmed, 5)

| ID | Strategy | Verdict | Dimension | Fix class |
|----|----------|---------|-----------|-----------|
| RT-001-iter009 | S-001 | VERIFIED 3/3 | Internal Consistency / Evidence Quality | command correction (existing one-liner) |
| RT-002-iter009 | S-001 | VERIFIED 2/3 | Completeness / Internal Consistency | disclosure narrowing |
| DA-002-20260706-i9 | S-002 | VERIFIED 2/3 | Methodological Rigor / Completeness | migration-plan enumeration (text) |
| 012-001 | S-012 | VERIFIED 2/3 | Completeness / Actionability | disclosure sentence |
| 012-003 | S-012 | VERIFIED 2/3 | Internal Consistency / Methodological Rigor | temporal-anchor correction (text) |

Explicitly OUT of scope (panel-refuted, not touched): DA-001-i9, 004-001, 004-002, 011-001/CV-001, 012-002.
Advisory Majors (RT-003, 013-001, 003-001) NOT in this owner-first mandate; left for a later pass.

## Filesystem verification (P-022, own Glob/find before editing, 2026-07-06)

- `docs/design/ADR-*.md` (flat): 3 files — `ADR-agent-design-001.md`, `ADR-output-path-resolution-001.md`, `ADR-routing-triggers-001.md`. None under a `decisions/` segment; `docs/design/decisions/` does not exist (0 matches).
- `projects/*/decisions/ADR-*.md`: 15 files.
- Currently-cited command `find projects docs/design -path '*/decisions/*' ...` returns **15**, not the claimed 18 (RT-001 confirmed).
- Two-clause command `find projects docs/design -name 'ADR-*.md' \( -path '*/decisions/*' -o -path 'docs/design/ADR-*.md' \) ...` returns **18** (15 dialect + 3 framework) — makes the "18 reachable" claim TRUE. Chosen fix for RT-001.

## Disposition (edits applied)

| ID | Disposition | Deliverable edits | Doctrine check |
|----|-------------|-------------------|----------------|
| RT-001-iter009 | CLOSED-BY-EDIT (command correction) | ADR: L1 pre-flight `find` → two-clause scan + explanatory comment; grandfather-regression note now cites the two-clause scan. Rule-draft: L5 `find` → two-clause + comment; grandfather-regression note updated. | Correction to existing command, not a new rule (parallel to iter-6 regex-widening precedent). Makes the "18 reachable" claim true (15→18, filesystem-verified). |
| RT-002-iter009 | CLOSED-BY-DISCLOSURE (scope-narrowing) | ADR: D-5 topology-scope note narrowed — pre-flight one-liner scans project-based roots only; repository-based adopter must substitute `${RepositoryRoot}/decisions`. Rule-draft: same substitution note in L5 command comment. | Disclosure + one-clause substitution guidance; no topology-aware scanner built (declined; underlying gap = INHERENT R-10). |
| DA-002-20260706-i9 | CLOSED-BY-EDIT (Migration-Plan enumeration) | ADR: M-2 row extended to name all 5 additional relative links (3× `../FEEDBACK-LOG.md` incl. changelog-row link-target per FM-014; `../orchestration/.../subtraction-pass-notes.md`; rule-draft's `ADR-PROJ031-003` link) with repo-root-relative repair targets. | Migration-Plan text only; fix is the future executor's, not a standing mechanism. No new machinery. |
| 012-001 | CLOSED-BY-DISCLOSURE | ADR: Downstream/plugin disclosure gained a current-state caveat — until M-2 executes and a build is cut, a plugin install carries no trace of the convention (both deliverables under stripped `projects/`; destination file not yet created). | Disclosure sentence; underlying absence stays the accepted M-2/M-6 residual. No machinery. |
| 012-003 | CLOSED-BY-EDIT (temporal anchor) | ADR: grandfather baseline re-anchored to ratification (2026-07-05/06), with the amnesty-window rationale. Rule-draft: L5 grandfather-baseline clause re-anchored to ratification. | Spec-wording correction; no new rule. Resolves the D-4 "existing/legacy" inconsistency. |

**Refuted (NOT actioned, per mandate):** DA-001-i9, 004-001, 004-002, 011-001/CV-001, 012-002.
**Advisory Majors (deferred, out of owner-first mandate):** RT-003-iter009, 013-001, 003-001.

## Verification (post-edit)

- Two-clause `find` returns **18** files with a clean `uniq -d` (no collisions) — filesystem-verified 2026-07-06.
- Rule-draft re-measured: **253 lines / ~5.5k tokens** (`wc` ~4.1k words × 1.35) — marginally above the 250-line self-guidance, within the original ~250–350 range; disclosed in the rule-draft budget note and changelog v1.11.
- No new lint rule / ledger / gate / matrix added; 5-rule core (L-1/L-2/L-3/L-4/L-7) unchanged.
- No residual re-opened; no R-N register change required.

## Changelog

| When | Action |
|------|--------|
| 2026-07-06 | Created notes; verified RT-001 filesystem facts (3 flat framework ADRs, 15 dialect, old command=15, two-clause=18). |
| 2026-07-06 | Applied all 5 VERIFIED fixes to both deliverables; appended ADR + rule-draft changelog v1.11; updated subtraction-pass-notes disposition table (Iteration-9 section) + Files Edited. |

*No subagents (P-003). Only the 2 deliverables + this notes file + subtraction-pass-notes edited (P-020). Claims cite file+line; inference labeled (P-022). No employer-internal refs or absolute home-directory paths introduced into artifacts; all cited paths are repo-relative.*

# Owner-First Remediation Notes — ADR-PROJ031-004 (iteration 2)

> **Owner/creator:** ps-architect
> **Started:** 2026-07-02
> **Inputs:** `s-014-quality-score.md` (priority table) + all iteration-002 findings files.
> **Score before:** 0.54 / engagement gate 0.95.
> **Deliverables edited:** `decisions/ADR-PROJ031-004-adr-identifier-convention.md`, `design/adr-standards-rule-draft.md`.
> **Mandate boundary (P-020):** I may edit ONLY the two deliverables above. Fixes that require writing code (`scripts/lint_*.py`), editing other files (`ps-architect.md`, `worktracker-directory-structure.md`, the 3 framework ADRs, `ci.yml`), or creating worktracker/GH entities are OUT of scope for a markdown edit; for those I add honest Claim-Status framing + a gating Migration-Plan action item, and record here.

## Verification Log (P-022 — every factual claim cited)

| Finding | Claim | Verification | Verdict |
|---------|-------|--------------|---------|
| CV-001 | "Every scope-prefixed family is collision-free by construction" is false | `projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md:37,158` — the output-path ADR was minted as `ADR-EPIC002-001`, colliding with the pre-existing strategy-selection `ADR-EPIC002-001` already cited from `quality-enforcement.md:108,275,290,350`; resolved by renaming to `ADR-EPIC002-002`. A real intra-family (entity-ID) collision caught by C4 tournament, NOT prevented by construction. | CONFIRMED — correcting |
| CV-002 | The tournament/rescore rigor belongs to a *different* BUG-006 | Two distinct BUG-006 entities exist: `reviews/BUG-006-adr-naming-evaluation.md` (Nielsen naming eval, the ADR's motivating usability review) vs `work/BUG-006-skill-output-path-hardcoded.md` (GH #230, output-path bug — owner of `c4-tournament-review`, `c4-rescore-iter2..5`). | CONFIRMED — disambiguating |
| FM-016 | Worktracker scaffold has no `decisions/` dir | `skills/worktracker/rules/worktracker-directory-structure.md` — all 6 "decision" mentions are `DEC-NNN` worktracker Decision-Files at Epic/Feature/Enabler/Story levels; no `projects/PROJ-NNN-*/decisions/` ADR directory documented. | CONFIRMED |
| CC-002 | AGENTS.md is agent-only; CLAUDE.md registers rule files | `AGENTS.md:1` = "Registry of Available Specialists" (sub-agent personas only). `CLAUDE.md:53-56` Navigation table registers `.context/rules/*` rule files. | CONFIRMED — drop AGENTS.md, keep CLAUDE.md |
| SM-002 | ADR's 0.78 crosses trade study's 0.75 ceiling | `trade-study.md:341` — "I decline to claim >0.75 for a C4 governance flip resting on n=3." ADR Confidence = 0.78, exceeds the declared ceiling; ADR acknowledges the 0.70 single-winner figure but not the 0.75 ceiling. | CONFIRMED — capping at 0.75 |
| FM-001 | ps-architect.md hardcodes non-canonical grammar + bare title + phantom refs | `skills/problem-solving/agents/ps-architect.md`: bare `# ADR-{NUMBER}` title at :218; filename grammar `{ps_id}-{entry_id}-adr-{slug}.md` at :260,:268 (grammar-family instances total ~6 across file, NOT "10"); phantom `templates/adr.md` (:263, real path `docs/knowledge/exemplars/templates/adr.md`); phantom+H-05-violating `python3 scripts/cli.py` (:267,:482,:509 — real CLI is `uv run jerry`, entrypoint `pyproject.toml:65`). | SUBSTANCE CONFIRMED; "10 occurrences" is an OVERCOUNT (rebutted to ~6) |

## Disposition Table

| Priority | Finding(s) | Disposition | Where applied |
|----------|-----------|-------------|---------------|
| P0-1 | RT-001, FM-012 | HONEST-FRAMING (code fix out-of-mandate) — added **Claim-Status: lint DESIGNED-NOT-BUILT** to both deliverables; lint is advisory until M-6 ships with green CI link | ADR Enforcement Design; rule draft L5 spec intro |
| P0-2 | PM-001 | FIXED + verified — new **Enforcement Scope & Deployment Targets** subsection; skeleton strips `projects/`+`.github/` (`phase3…:159`); CI-independent `uv run jerry lint adr` (M-13) | ADR new subsection; rule draft L5 spec intro |
| P0-3 | CC-001 | FIXED — **Tier reconciliation**: L-2/L-3 waivable-in-principle, not de-facto HARD | ADR Enforcement Design (new subsection); rule draft override model |
| P0-4 | CV-001 | FIXED + verified — "collision-free by construction" → "collision-*resistant*"; `ADR-EPIC002-001` collision disclosed | ADR Context, Scheme A steelman, Neg-Consequence #1, L2 bullet, Migration Plan |
| P0-5 | FM-001, FM-015 | FIXED (spec) + REBUTTAL — added **Fix 3** + gating **M-12**; rebutted "10 occurrences"→~6 | rule draft new Fix 3; ADR M-12 |
| P0-6 | RT-002 | FIXED — new non-waivable **L-9** (block new files under frozen dirs) | both lint tables |
| P0-7 | RT-003 | FIXED — L-1a bans `^(proj\|epic\|feat\|story)\d+$` case-fold look-alikes | both lint tables |
| P0-8 | RT-004 | FIXED — API-verified CODEOWNERS/branch-protection approval + append-only ledger check | rule draft override model; ADR references it |
| P0-9 | IN-001, DA-003 | FIXED — at-birth premise reconciled; default-to-canonical; mandatory `scope:` (ADR-M-013); residual named+monitored | ADR sensitivity section; rule draft ADR-M-003, new ADR-M-013 |
| P0-10 | FM-016 | FIXED (spec) + verified — **New-Project Onboarding** section + gating **M-14** (scaffold edit out-of-mandate) | rule draft new section; ADR M-14 |
| P1-1 | PM-002, SM-004 | HONEST-FRAMING — Claim-Status: TBD-Task cells unresolved, will NOT fabricate IDs (P-022); a pre-ratification precondition | ADR Migration Plan intro |
| P1-2 | PM-003, IN-002, DA-006 | FIXED — M-5b promoted to deterministic **L-10 Taxonomy synonymy** WARN | both lint tables |
| P1-3 | CV-002 | FIXED + verified — disambiguated the two BUG-006 entities | ADR P-022 disclosure (f) |
| P1-4 | RT-005 | FIXED — **L-7 bidirectional + FAIL-class** | both lint tables |
| P1-5 | PM-006, FM-004, FM-010 | FIXED — **M-11 gating** + extended to framework-cited `EPIC002`/`STORY015` ADRs | ADR M-11 |
| P1-6 | CC-002 | FIXED + verified — dropped AGENTS.md from M-7; H-26→H-23/NAV-002 propagated | ADR M-7; rule draft wrapper note |
| P1-7 | CC-003 | FIXED — amendment-boundary aligned to SHOULD NOT across both | ADR amendment boundary |
| P1-8 | SM-002 | FIXED + verified — confidence capped at 0.75 ceiling (was 0.78), 0.70–0.75 range | ADR Confidence |
| P1-9 | DA-005 | FIXED — "C2≳22" disclosed as two-point bundled interpolation | ADR sensitivity tipping point |
| P1-10 | PM-005 | FIXED — closed `{PROJ\|EPIC\|FEAT\|STORY}` set in grammar + L-1b | ADR grammar; rule draft ADR-M-003 + L-1b |
| P1-11 | SM-001 | FIXED — prior-review tag glossary added | ADR top (after nav) |
| P2-1 | IN-003 | FIXED — L-8 evidentiary-citation exemption | both lint tables |
| P2-2 | DA-004 | FIXED — labeled-qualitative collision-risk-at-scale estimate | ADR L2 taxonomy bullet |
| P2-3 | PM-009 | INHERENT — monitoring commitment (re-examine after 2-3 framework projects) | ADR post-risk monitoring note |
| P2-4 | R-6 | INHERENT — already Claim-Status framed; monitoring signal named | ADR Risks R-6 + monitoring note |
| (narrative) | DA-001 | COVERED — substance (promotion tax was not clean) already disclosed in Scheme-B steelman; now reinforced by CV-001 collision evidence + CV-002 disambiguation. Not a separate priority-table row. | ADR Context/Scheme B |

## Rebuttals

1. **FM-001 / P0-5 "10 occurrences" — REBUTTED on the number, ACCEPTED on substance.** The finding states `ps-architect.md` hardcodes the `{ps_id}-{entry_id}-adr-{slug}.md` grammar in "10 occurrences." Verified count: the exact filename-grammar token appears at `:260,:268`; broadening to all grammar-family instances (template + worked examples) yields **~6** lines (`grep -nc` = 6), **not 10**. The substantive defect — a non-canonical grammar + bare `# ADR-{NUMBER}` title (`:218`) + two phantom paths (`templates/adr.md` `:263`; `python3 scripts/cli.py` `:267,:482,:509`, which also violates H-05) — is fully accepted and addressed by Fix 3 / M-12. Only the magnitude "10" is corrected to ~6, per P-022. This does not change the fix.
2. **DA-001 (Evidence Quality, Critical) — no separate action; substance already disclosed.** DA-001 argues the "clean one-time `git mv` / paid tax with a git receipt" narrative is contradicted by the record that the EPIC-002 promotion left dangling SSOT refs. Two points: (a) the ADR's Scheme-B steelman **already** discloses the tax "is not even fully repaid: stale citations to the extinct `ADR-PROJ007-001/002` IDs still sit in…" — i.e., the messy-not-clean reality was never hidden; (b) the specific EPIC-002 event DA-001 cites is the same collision now documented explicitly under CV-001 (the output-path BUG-006). So DA-001's concern is met by the pre-existing disclosure **plus** the new CV-001/CV-002 edits, not by a separate change. Recorded rather than silently skipped.

## Honest-Framing (INHERENT / out-of-mandate) items

- **P0-1 (ship the lint script)** — building `scripts/lint_adr_convention.py` + wiring CI is a code/devsecops task outside a markdown edit and outside my two-file mandate (P-020). Framed honestly as **Claim-Status: DESIGNED-NOT-BUILT**; enforcement is advisory until M-6 ships with a green CI-run link. Not pretended closed.
- **P1-1 (create worktracker Tasks + GH Issues)** — creating entities requires the `jerry` CLI + `gh` and would create files beyond the two deliverables (P-020); fabricating Task/Issue IDs would violate P-022. Framed as an unresolved, non-fabricated pre-ratification precondition.
- **P0-5 F3-a…e edits to `ps-architect.md`**, **P0-10 scaffold edit to `worktracker-directory-structure.md`**, **P1-5 frontmatter retrofit onto the 3+3 framework ADRs**, **M-10 `ci.yml` repair** — all target files outside the two deliverables. Specified precisely + scheduled as gating Migration-Plan items (M-10..M-14), **not applied here** (P-020).
- **P2-3 (PM-009 n=3) and P2-4 (R-6 same-`NNN` race)** — genuinely INHERENT (no registry-free design eliminates them; n=3 cannot be grown by editing). Added named detection signals + escalation paths (monitoring commitments), explicitly framed as tracked-not-closed.

## Constitutional / Mandate Compliance

- **P-020:** edited ONLY the two mandated deliverables (`ADR-PROJ031-004…md`, `adr-standards-rule-draft.md`) + this notes file. No other repo file touched; every cross-file fix is a scheduled Migration-Plan item, not an in-place edit.
- **P-022:** every factual claim cited to file:line (see Verification Log); the "10 occurrences" overcount rebutted rather than parroted; lint-unbuilt and TBD-Task states framed honestly rather than papered over; INHERENT residuals labeled, not closed.
- **P-003:** no subagents spawned. **P-002:** this file created early and written incrementally.

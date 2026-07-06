# S-010 Self-Refine — Findings Log (Iteration 2)

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | ADR package: `ADR-PROJ031-004-adr-identifier-convention.md` + `adr-standards-rule-draft.md` |
| Criticality | C4 (framework governance) |
| Date | 2026-07-02 |
| Reviewer | ps-architect (creator/owner) |
| Iteration | 2 |
| Role | CREATOR/OWNER — has edit rights on BOTH deliverables |

> Status: IN PROGRESS — written incrementally per P-002. Verification evidence captured before findings.

---

## Step 1: Objectivity check

Medium attachment (I am the owner, post iter-1 remediation). Per template Step 1 conservative fallback, applying stricter scrutiny (aim 5+ findings). Both deliverables are mature (iter-1 already closed many defects); the hunt is for *residual* contradictions the iter-1 pass introduced or missed.

---

## Verification evidence (P-022 — captured before claims)

All bash-verified 2026-07-02 from repo root `feat/proj-030-skeleton-branch`.

1. **ADR bibliography — no dangling refs.** All 8 cited internal sources EXIST: `adr-convention-standards-research.md`, `trade-study.md`, `advocate-project-scoped.md`, `advocate-domain-slug.md`, `advocate-external.md`, `BUG-006-adr-naming-evaluation.md`, `docs/knowledge/exemplars/templates/adr.md`, `skills/architecture/SKILL.md`.
2. **ci.yml:2 dangling-citation evidence is REAL.** `.github/workflows/ci.yml:2` literally reads `# ADR: projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`; `projects/PROJ-001-plugin-cleanup/` CONFIRMED MISSING. The ADR's motivating evidence (RT-003/FM-007, M-10) is accurate.
3. **Corpus truth = 16 live dialect ADRs.** decisions/-dir: `PROJ010`×6, `PROJ022`×2, `PROJ031`×4 (incl. this ADR), `EPIC002`×2, `ADR-150`×1 = 15; PLUS entity-embedded `ADR-STORY015-001` at `projects/PROJ-024-tactical-work/work/.../STORY-015-tier-model-renumbering/` (NOT in a decisions/ dir) = **16 total** (15 pre-existing + this ADR). The rule draft's "16" was correct; the ADR's "~11" was the undercount.
4. **Tier-vocab pre-fix:** rule draft contained HARD keywords at lines 163 (authoring rule), 185 (waiver spec), 203 (regression-test). Post-fix: `grep -E '\b(MUST|SHALL|MANDATORY|Mandatory)\b'` returns CLEAN.
5. **Nav tables:** ADR nav (24 sections) and draft nav (13 sections) both complete; tricky anchors (en-dash `options-considered-af`, em-dash `rationale--answering...`, `path-1--canonical-...`, colon `meta-note-...`) spot-checked and resolve.

---

## Findings

| ID | Finding | Severity | Evidence | Dimension | Disposition |
|----|---------|----------|----------|-----------|-------------|
| SR-001-i2 | **Count contradiction "~11" vs 15/16.** ADR prose said "~11 existing project ADRs" at 3 sites (lines 130, 188, 358) while its OWN Migration Plan enumerates 15 and its companion rule draft (line 203) explicitly calls "~11" a *superseded undercount* (16 files). Cross-deliverable + internal self-contradiction on a load-bearing corpus fact. | **Major** | Filesystem = 16 dialect ADRs (verified); rule-draft:203 vs ADR:130/188/358 | Internal Consistency | **FIXED** — all 3 ADR sites now state 15 pre-existing / 16 incl. this ADR, matching the Migration Plan + rule-draft regression test. |
| SR-002-i2 | **Tier-vocabulary violation in the MEDIUM rule draft.** File declares "Every rule below uses SHOULD/RECOMMENDED/MAY" (line 5) and "All rules are MEDIUM-tier" (line 37), yet contained HARD keywords: line 163 "amendment **MUST NOT** change scope" (a substantive authoring rule, not a lint spec); line 185 waiver "**MUST** carry"; line 203 "**Mandatory** … **MUST** ship/pass/be recognized". | **Major** | grep line 163/185/203; c-001 MEDIUM mandate | Methodological Rigor | **FIXED** — line 163 → "SHOULD NOT / SHOULD"; lines 185/203 reworded to describe deterministic L5 enforcement without HARD keywords. Draft now grep-clean. (Note: parent ADR:487 retains "MUST NOT" — acceptable, it is a C4 *decision* doc, not the MEDIUM rule file; the draft edit notes this translation.) |
| SR-003-i2 | **Consequence #1 overstatement.** Line 355 claimed "zero citation breakage" for canonical promotion, contradicting the ADR's own Path-1 caveat (line 458) + R-6 that full-path citations *do* move under `git mv`. | Minor | ADR:355 vs ADR:458/R-6 | Internal Consistency | **FIXED** — qualified to "zero ID-string churn … full-path citations are the small lint-surfaced residue," with anchor to the Path-1 caveat. |
| SR-004-i2 | **Anti-C steelman precision.** Line 138 attributes the 6 still-stale `ADR-PROJ007` references to Scheme C, but they arose under the *no-convention status quo*; Scheme C's specified process (Path-2 step 5) includes re-pointing. Fair as a "tombstones don't fix pre-existing citations" point, but the phrasing lightly conflates status-quo evidence with C-applied outcome. | Minor | ADR:138; Promotion Path-2 step 5 | Evidence Quality | **NOT EDITED** — defensible (the broader "renumber tax empirically goes unpaid" claim is sound); documented for transparency (H-16). |
| SR-005-i2 | **Crux answered, one granularity gap.** The Rationale (lines 211-213) answers "is *project* the right scope key?" head-on and well ("no scope key belongs in identity; subject does — because ADR scope is uniquely mutable"). It reframes rather than ranks scope *granularity* (project vs epic/story) for the permitted dialect (D-3 permits all three without preference). | Minor | ADR:211-213, D-3 (line 186), grammar (line 279) | Completeness | **NOT EDITED** — dialect granularity is author's-choice by design; the reframe is the *deeper* correct answer. Documented. |
| SR-006-i2 | **Anchorless cross-file link.** ADR:523 linked the rule draft's lint section by file only, no `#` fragment. | Minor | ADR:523 | Traceability | **FIXED** — added `#l5-ci-lint-specification`. |

## Positive confirmations (balance, P-022)

- **No dangling refs in the ADR's own bibliography** — all 8 cited sources verified present. Ironic-failure risk (an ADR about citation integrity with broken citations) does NOT materialize.
- **Motivating evidence is accurate** — the `ci.yml` dangling `ADR-CI-001` and `PROJ-001-plugin-cleanup` deletion are real (verified), so the 9th-family / RT-003 argument is well-grounded.
- **Crux is answered head-on** with a promotion-independent principled argument + an honest counter-case kept alive (exemplary H-16 steelman discipline).
- **Options A–F steelman fairness is strong**; the rejected baseline-winner C receives a generous, honest steelman and an explicit "C is not wrong — it is right under a different testable belief."
- **Sensitivity analysis + confidence calibration** (0.78, explicit n=3 caveat) and the 5-item P-022 disclosure block are thorough and honest.
- **Nav tables H-23/H-24 compliant** in both deliverables.

## Scoring impact (post-fix self-estimate)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All sections present; SR-005 minor granularity gap only |
| Internal Consistency | 0.20 | Negative→Positive | SR-001 (count) + SR-003 (zero-breakage) resolved |
| Methodological Rigor | 0.20 | Negative→Positive | SR-002 tier-vocab violation resolved; draft now MEDIUM-clean |
| Evidence Quality | 0.15 | Positive | All citations verified; SR-004 minor precision noted |
| Actionability | 0.15 | Positive | Migration Plan gating items, lint spec, promotion paths concrete |
| Traceability | 0.10 | Positive | SR-006 anchor added; all refs resolve |

## Decision

**Outcome:** Package improved — 2 Major (count contradiction, tier-vocab) + 2 Minor fixed by direct edit; 2 Minor documented as defensible. No Critical defects. Ready for the next tournament strategy (steelman / challenge groups) on a self-consistent package.

**Next action:** Hand the revised, self-consistent package to the S-003 (steelman) and downstream adversarial groups per the 6-group order.

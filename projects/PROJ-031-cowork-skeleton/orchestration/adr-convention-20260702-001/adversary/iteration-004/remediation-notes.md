# Iteration-4 Owner Remediation Notes (ps-architect, creator/owner)

> Disposition of every iteration-4 [FIXABLE-NOW] item from `s-014-quality-score.md` (score 0.59, engagement gate 0.95), plus rebuttals and INHERENT framing. Every factual claim cites a file path/line; inference is labeled. Deliverables edited: `decisions/ADR-PROJ031-004-adr-identifier-convention.md` (→ v1.5), `design/adr-standards-rule-draft.md` (→ v1.5).

## Navigation

| Section | Purpose |
|---------|---------|
| [Method](#method) | How this pass was executed |
| [Disposition Table](#disposition-table) | Every finding: FIXED / REBUTTED / INHERENT |
| [Change Log Of Edits](#change-log-of-edits) | Per-edit record with file + location |
| [Rebuttals](#rebuttals) | Findings judged invalid/mischaracterized, with evidence |
| [Inherent Residuals](#inherent-residuals) | Honestly framed, not closed |

---

## Method

Read in full: `s-014-quality-score.md` (priority table), `s-001-findings.md` (Red Team), `s-002-findings.md`
(Devil's Advocate), `s-007-findings.md` (Constitutional), `s-012-findings.md` (FMEA), `s-013-findings.md`
(Inversion), plus the S-004/S-010/S-011 findings summarized in the score report, and both deliverables in full.
Verified empirically before editing (P-022): the live ADR corpus via `find` (16 dialect: EPIC002×2, PROJ010×6,
PROJ022×2, 150×1, PROJ031×4 in `decisions/` + STORY015×1 entity-embedded; 3 canonical `docs/design/`; 7 transient
`ADR-OSS-*`); the three lint scripts confirmed absent; JPH source-verified in
`research/adr-convention-standards-research.md:99,216` = Joel Parker Henderson.

Status legend: **FIXED** (edited into a deliverable), **REBUTTED** (invalid/mischaracterized, evidence given),
**INHERENT** (cannot be closed by a document edit; framed honestly with Claim-Status).

---

## Disposition Table

| Priority | Finding(s) | Dimension | Disposition | Where remediated |
|----------|-----------|-----------|-------------|------------------|
| P0-1 | IN-001, PM-001 | Actionability | **FIXED** (IN-001 two-tier gate) + **INHERENT** (PM-001 tracking entities) | ADR Status → new "Two-tier ratification" subsection; PM-001 framed honestly (no fabricated IDs) |
| P0-2 | RT-001, FM-001 | Method. Rigor | **FIXED** (spec: named fixtures + L-14) + **INHERENT** (actual build = M-6) | ADR M-6 regression section (named RT-001..RT-011/L-13 fixtures); new **L-14 producer-drift** (both files) |
| P0-3 | RT-002, IN-005 | Method. Rigor | **FIXED** | ADR Enforcement-Design summary (FAIL-rules-self-waivable statement); rule-draft override model (`legitimacy_category` enum + `affects`) |
| P0-4 | RT-003 | Completeness | **FIXED** | New **L-13 Supersession legitimacy** FAIL rule (both files) |
| P0-5 | FM-003, FM-005, RT-009, IN-006 | Internal Consistency | **FIXED** (FM-003, RT-009, IN-006) + **REBUTTED-with-reconciliation** (FM-005) | L-7→Relationship integrity + Fix-1d corrected; Neg-3 reworded; `canonical_id` added to both schemas; FM-005 reconciliation note |
| P0-6 | DA-001, DA-004 | Method. Rigor | **FIXED** | Bimodal circularity disclosure (downgraded to illustrative); slug-reuse = tracked **R-7** + Neg-6 |
| P1-1 | DA-007, RT-012 | Traceability | **FIXED** (+ honest disclosure) | `ST-*` Steelman tag family + embedded-steelman H-16 disclosure (glossary) |
| P1-2 | CC-001 | Traceability | **FIXED** | M-7 + rule-draft wrapper: "discretionary precedent, not H-23/NAV-004-compelled"; 3-of-17 ratio corrected |
| P1-3 | FM-002 | Internal Consistency | **FIXED** (sync obligation) | Dual-file sync note + "rule draft governs" atop ADR lint table |
| P1-4 | PM-002 | Completeness | **FIXED** | Enforcement-Scope degraded-mode-against-empty-corpus disclosure |
| P1-5 | RT-007 | Completeness | **FIXED** | New **L-4b** dialect-reject under repository-based topology (both files) |
| P2-1 | CC-002 | Evidence Quality | **FIXED** | JPH expanded (Joel Parker Henderson) at both sites + References #12 |
| P2-2 | DA-002 | Evidence Quality | **FIXED** (disclosure + commitment) + **INHERENT** (no Path-1 yet) | 72%/28% scope-limitation disclosed at cite site; first-Path-1 measurement commitment |
| P2-3 | IN-008 | Evidence Quality | **FIXED** | Reproducible `find`-command corpus enumeration replaces manual counting |
| P2-4 | PM-003 | Internal Consistency | **FIXED** | YAML-vs-blockquote drift = residual **R-8** + proposed WARN check |
| — | IN-004 | Int. Cons./Rigor | **FIXED** | New **L-6c** scope-presence WARN (both files) |
| — | DA-005 | Int. Cons./Action. | **FIXED** | M-5b arbiter capacity caveat + backlog-escalation fallback |
| — | DA-006 | Completeness/Action. | **FIXED** | R-3 synonymy detect-*and*-remediate loop (supersession) |
| — | FM-004 | Actionability | **FIXED** | M-9 reciprocal-link atomicity as checkable close-condition |
| — | FM-006, FM-008 | Completeness | **FIXED** | Rule-draft onboarding items 2-3 topology-branched + M-14 sub-item |
| — | FM-009 | Completeness | **FIXED** | `ADR-CI-NNN` 9th-family disposition (deprecated ad-hoc series) |
| — | DA-008 | Method. Rigor | **FIXED** (honest bound) | "subject materially more immutable than scope," not absolute |
| — | DA-009 | Actionability | **FIXED** | R-6 "rising" = ≥2 L-3 collisions / rolling 90-day window |
| — | CC-004 | Evidence Quality | **FIXED** | SM-203 clause corrected to full six-term SSOT keyword set |
| — | RT-004 | Completeness | **FIXED** (partial) | R-6 mitigation sharpened (merge-queue/scheduled re-run) |
| — | RT-008, RT-010 | Evidence Q./Rigor | **FIXED** | L-8 path-validation + L-1a regex-scope disambiguation folded into M-6 fixtures |
| — | RT-011 | Completeness | **FIXED** | L-12 initial-seed-exact-match assertion (both files) |
| — | IN-007 | Int. Cons. | **REBUTTED** | Process observation (score variance), not a document defect — see Rebuttals |
| — | CC-003 | Int. Cons. | **REBUTTED** | Dual-H1 is transient-by-design; no action needed before ratification |

---

## Change Log Of Edits

**ADR (`decisions/ADR-PROJ031-004-adr-identifier-convention.md`, → v1.5):**

1. Status § — inserted **"Two-tier ratification"** subsection (Tier-1 guidance / Tier-2 enforcement); reframed G-1 as Tier-1, G-2..G-4 as Tier-2; PM-001 honesty retained (IN-001, PM-001).
2. Reading-note glossary — added **`ST-*`** family + H-16 embedded-steelman disclosure (DA-007, RT-012).
3. Consequences Negative-3 reworded (RT-009); new Negative-6 slug-reuse (DA-004).
4. Scheme-B Pros — **JPH** expanded to Joel Parker Henderson (CC-002).
5. Positive Consequence 5 — JPH expanded (CC-002).
6. References — new row **#12 JPH** (CC-002).
7. L1 Frontmatter Schema — added `canonical_id` optional advisory field + note (IN-006/FM-007).
8. Enforcement Design summary — **dual-file sync obligation** (FM-002) + **FAIL-rules-self-waivable** statement (IN-005/RT-002).
9. ADR lint table — new rules **L-6c** (IN-004), **L-13** (RT-003), **L-14** (FM-001); L-4 split + **L-4b** (RT-007); L-12 seed-match note (RT-011).
10. Regression-test section — named adversarial fixtures per L-2..L-14 (RT-001, RT-008, RT-010) + reproducible `find` corpus (IN-008) + FM-005 reconciliation.
11. M-7 — replaced H-23/NAV-004 authority with "discretionary precedent" + 3-of-17 ratio; gating → No (CC-001).
12. Risks — new **R-7** slug-reuse (DA-004), **R-8** YAML/blockquote drift (PM-003); R-6 sharpened (RT-004, DA-009); R-3 remediation loop (DA-006).
13. Bimodal section — DA-001 circularity disclosure (downgraded to illustrative).
14. Path-1 caveat — DA-002 72%/28% scope-limitation + first-Path-1 measurement commitment.
15. Enforcement Scope — PM-002 degraded-mode disclosure.
16. M-5b — DA-005 arbiter capacity caveat + fallback.
17. M-9 — FM-004 reciprocal-link atomicity close-condition.
18. Context corpus-survey — FM-009 `ADR-CI` disposition.
19. Rationale — DA-008 subject-immutability honest bound.
20. v1.4 changelog SM-203 clause — CC-004 six-term correction; new **v1.5** changelog row; "12-rule"→"multi-rule (L-1a…L-14)"; M-6 row count consistency.

**Rule draft (`design/adr-standards-rule-draft.md`, → v1.5):**

1. Wrapper note — CC-001 citation correction (discretionary precedent; 3-of-17).
2. Fix-1d — FM-003 lint-coverage precision (`amends`/`amended_by` + `canonical_id`).
3. L-7 renamed **Relationship integrity**, extended to `amends`/`amended_by` (FM-003).
4. Frozen-and-Grandfathered table — FM-005 `PROJ031`×3-vs-×4 reconciliation note.
5. Frontmatter Schema — `canonical_id` optional advisory field (IN-006).
6. Override model — `legitimacy_category` enum + `affects` field (RT-002/IN-005).
7. Lint table — **L-4b** (RT-007), **L-6c** (IN-004), **L-13** (RT-003), **L-14** (FM-001); L-12 seed-match (RT-011).
8. New-Project Onboarding — items 2-3 topology-branched + M-14 seed sub-item (FM-006/FM-008).
9. New **v1.5** draft-version note.

---

## Rebuttals

**IN-007 (score non-monotonicity 0.67→0.54→0.62→0.59 "does not support convergence") — REBUTTED as a process observation, not a fixable document defect.** IN-007 itself concedes (`s-013-findings.md:190`) "This is stated as inference, not fact: three iterations is a small sample, and iteration 2's dip to 0.54 could reflect a stricter or differently-focused reviewer rather than genuine regression." Independent-blind-reviewer variance across iterations is expected under the tournament design (each iteration re-blinds a fresh reviewer set), so a non-monotonic trend is not evidence of a defect *in the deliverable* — it is evidence about the *scoring process*. A document edit cannot "fix" a cross-iteration score trend. The valid, actionable core of IN-007 (document density) is acknowledged and partially acted on: the two-tier decoupling (P0-1) *removes* content-coupling rather than adding it, and the reproducible-corpus enumeration (IN-008) *replaces* narrative counting. A full structural extraction of prior-iteration meta-commentary is noted as a candidate for a future pass but is deliberately **not** done reflexively here, because deleting the extensively-cross-referenced disclosure blocks risks removing the very P-022 honesty the tournament rewarded. Recorded as an inference-level process note, not silently ignored.

**CC-003 (rule draft has two H1 headings) — REBUTTED as transient-by-design.** `s-007-findings.md:93` itself rates this "Cosmetic only... will self-resolve once this content is extracted into `.context/rules/adr-standards.md` (at which point the wrapper H1 + note disappear per the file's own stated intent)" and its remediation says "No action required before ratification." The wrapper H1 (`# DRAFT — Proposed .context/rules/adr-standards.md`) exists *only* to mark the file as a not-yet-installed review draft; on ratification (M-2) the wrapper is stripped and a single H1 remains. Editing it now would obscure the deliberate "this is a draft, not an installed rule" signal. No change; disposition is deferral-by-design, disclosed here rather than silently skipped.

**FM-005 ("PROJ031×3 vs ×4" internal contradiction) — REBUTTED-with-reconciliation (accepted as a clarity gap, rejected as a contradiction).** The two numbers count *different, correctly-scoped sets*: line 107's grandfather table shows ×3 = the **pre-existing, grandfathered-in-place** subset (excludes this ADR, which self-promotes at M-9 and does *not* stay in place); the regression test shows ×4 = the **corpus-exercised** set (includes this ADR's current dialect filename before promotion). This is the identical distinction the ADR already draws at D-4 (SM-201). So it is not "the same set counted inconsistently" (FM-005's characterization) — it is two legitimately-different sets whose relationship was not spelled out *at the point both appear*. Remediated by adding an explicit reconciliation note (not by forcing the numbers equal, which would be wrong), and pinned to the reproducible `find` output.

**DA-002 "full-path dominant" implication — already grep-refuted in iter-3, extended here.** The finding's framing that full-path is the dominant citation style is not borne out — the measured `.context/rules/` ratio is ~72% bare-ID : ~28% full-path (bare-ID dominates ~2.5:1). What *was* valid and is now fixed: the measurement's scope was `.context/rules/`-only and should be disclosed as such and not generalized repo-wide. Accepted the scope critique, rebutted the "dominant" implication (evidence: the grep ratio itself).

---

## Inherent Residuals (honestly framed, not closed — P-022)

These cannot be closed by editing the two deliverables; each carries a Claim-Status and a named detection/escalation path in the ADR:

1. **The lint does not exist (RT-001/FM-012).** `scripts/lint_adr_convention.py`, `adr-lint-waivers.yaml`, `adr-grandfather-allowlist.txt` are Glob-verified absent. Building them is Tier-2/M-6, an engineering action outside a document edit. Enforcement is advisory until then. [INHERENT]
2. **PM-001 tracking entities.** Zero of the 14 Migration-Plan rows exist as worktracker Tasks/GH Issues. Creating them is outside a document edit and this owner will not fabricate IDs. First Tier-2 action. [INHERENT]
3. **Single-maintainer waiver self-certification (RT-002/IN-005).** Until a second CODEOWNER exists, every FAIL rule is de-facto self-waivable — an organizational (staffing) change, not an edit. Now disclosed in the Enforcement summary, not only the buried subsection. [INHERENT]
4. **Zero demonstrated Path-1 promotions (DA-002/DA-003).** "Promotion is free" is a prediction until a real `git mv` promotion runs; the first instance is a named future milestone with a measurement commitment. [INHERENT]
5. **Forward promotion rate rests on n=3 (PM-009).** Bimodal categorization now downgraded to illustrative; adverse-regime test kept live. Resolves only with future framework-mandate projects. [INHERENT]
6. **R-6 cross-branch race / R-7 slug-reuse.** Mitigated-and-detected, not structurally prevented (no central registry, c-006). Both carry detection signals and escalation thresholds. [INHERENT]
7. **Score trend / document density (IN-007).** A process-level observation; a structural simplification pass is a candidate for iteration 5, not a single fixable defect. [INHERENT — process]

Nothing above is presented as fixed; each has a named detection signal and escalation path, matching the rigor applied to the pre-existing PM-009/R-6 residuals.

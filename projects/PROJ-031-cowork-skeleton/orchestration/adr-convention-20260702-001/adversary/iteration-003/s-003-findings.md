# Steelman Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + companion rule draft)

## Steelman Context
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft (governance convention)
- **Criticality Level:** C4 (engagement gate 0.95)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind reviewer, iteration 3) | **Date:** 2026-07-02 | **Original Author:** ps-architect (per document self-attribution)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall Steelman assessment |
| [Step 1: Charitable Interpretation](#step-1-charitable-interpretation) | Core thesis reconstruction |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. structural vs. evidence vs. substantive |
| [Verification Log](#verification-log) | Independent fact-checks of load-bearing claims |
| [Step 3: Steelman Reconstruction — Underselling Points](#step-3-steelman-reconstruction--underselling-points) | Where the package undersells its own best arguments |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Conditions under which the thesis is strongest |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity-classified |
| [Gaps That Survive the Charitable Reading](#gaps-that-survive-the-charitable-reading) | What remains a genuine finding even under best-case interpretation |
| [Scoring Impact](#scoring-impact) | Dimension-level impact of the Steelman |
| [Execution Statistics](#execution-statistics) | Summary counts |

---

## Summary

**Steelman Assessment:** This is an unusually mature C4 governance package — its 3rd iteration after two full adversarial remediation cycles (score 0.67 → 0.54 → this pass). Independent verification of ~20 load-bearing factual citations across both deliverables found **100% accuracy** (exact line-number matches for every dangling-citation claim, every provenance-format claim, every lint-absence claim, and every quantitative trade-study figure checked). The core thesis — ADR identity should encode *subject* (immutable) rather than *scope* (the one Jerry property that is mutable-by-design for this artifact class alone) — is logically sound, already self-steelmanned within the document (it contains its own honest counter-case, sensitivity analysis, and "regime in which this decision is wrong" section), and its two promotion-independent supporting arguments (ontology category-error; universal discoverability fix) do not depend on the contestable promotion-frequency bet at all.

**Improvement Count:** 0 Critical, 2 Major, 3 Minor.

**Original Strength:** Very high. Per the S-003 "When NOT to Use" guidance (diminishing returns after multiple high-scoring revision cycles), this document is approaching that ceiling — most Steelman value at this iteration is in *supplying additional verified evidence* the authors did not surface, not in reconstructing weak argumentation.

**Recommendation:** Incorporate the two Major evidence-completeness findings (both of which, notably, make the document's *own* case for adoption stronger, not weaker) before the next critique-strategy pass. No fundamental revision needed.

---

## Step 1: Charitable Interpretation

**Core thesis (most charitable form):** Of an ADR's three properties — origin (immutable birth fact), subject (immutable), and governing scope (the *one* Jerry-wide property that is mutable, because promotion project→framework is the accrual thesis in action) — only scope changes over an ADR's life. An identifier is a promise of stability; encoding the one mutable property into it is therefore a category error regardless of how often promotion actually happens, and two of the document's three supporting arguments (ontology-exception validity; discoverability) hold even in a zero-promotion world. The third argument (100% forward promotion rate at n=3) is honestly flagged as the load-bearing empirical uncertainty and is explicitly *not* required to carry the whole case.

**Charitable read of intent:** the author is not merely picking a naming scheme; the author is trying to make a *permanent, low-regret governance primitive* under genuine epistemic uncertainty (n=3), and has engineered every escape hatch (grandfather clause, permitted dialect, MEDIUM tier, monitoring commitments) precisely because they know the promotion-rate belief could be wrong. That is the strongest possible reading of a C4 decision at n=3, and the document earns it.

**Strengthening opportunities identified (not failures):** the evidentiary base for the empirical (promotion-rate) leg of the argument can be extended with real, already-available corpus evidence the document did not fold in (see [Step 3](#step-3-steelman-reconstruction--underselling-points)).

---

## Step 2: Weakness Classification

| Weakness | Type | Magnitude |
|---|---|---|
| Stale-citation evidence base cites 3 files / 6 lines but the identical pattern exists in at least 3 more live worktracker artifacts | Evidence | Major |
| Promotion-frequency sensitivity analysis (the document's own designated "load-bearing assumption") omits a 4th, directly relevant, already-catalogued corpus data point | Evidence / Methodological Rigor | Major |
| Zero-governance null-alternative rebuttal argues "a good index" abstractly rather than naming Jerry's own existing tooling | Presentation | Minor |
| Enforcement-machinery discussion (API-verified CODEOWNERS reviewer) doesn't confirm the prerequisite infrastructure already exists in this repo | Evidence | Minor |
| External-analogy citation set could add one more concrete parallel (URL/permalink slug-stability conventions) | Traceability | Minor |

No **substantive** weaknesses were found — i.e., nothing suggesting the core decision (Scheme B, MEDIUM-tier, grandfathered) is wrong on the merits. All identified weaknesses are evidentiary completeness gaps in an otherwise exceptionally well-verified document.

---

## Verification Log

Independent fact-checks performed against the live repository (not the adversary corpus, per blind protocol). All citations below are exact matches to the deliverable's claims unless noted otherwise.

| # | Claim checked | Source cited | Verification result |
|---|---|---|---|
| 1 | Dangling `ADR-CI-001` citation to a non-existent project path | `.github/workflows/ci.yml:2` | **Confirmed exact.** Line 2 reads `# ADR: projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`; `PROJ-001-plugin-cleanup` does not exist in this repo (only `PROJ-001-oss-release` does). |
| 2 | Lint scripts do not exist (Claim-Status: DESIGNED-NOT-BUILT) | `scripts/lint_adr_convention.py`, `scripts/adr-lint-waivers.yaml`, `scripts/adr-grandfather-allowlist.txt` | **Confirmed.** Glob returns zero matches for all three. |
| 3 | 3 framework ADRs exist, none with YAML `scope`/`origin_project` frontmatter, only informal comment-based provenance | `docs/design/ADR-agent-design-001.md:3`, `ADR-routing-triggers-001.md:3`, `ADR-output-path-resolution-001.md:3-8` | **Confirmed exact.** `ADR-agent-design-001.md:3` and `ADR-routing-triggers-001.md:3` use HTML comments (`PS-ID:`/`AGENT:`); `ADR-output-path-resolution-001.md:8` uses a blockquote `**Parent:** EPIC-002`. No YAML frontmatter block in any of the three. |
| 4 | `docs/design/README.md` does not exist (BUG-006 F-004 "never implemented") | `docs/design/README.md` | **Confirmed.** Glob returns zero matches. |
| 5 | Dialect-family counts (`PROJ010`×6, `PROJ022`×2, `PROJ031`×3(+this ADR=4), `EPIC002`×2, `150`×1, `STORY015`×1 entity-embedded) | `projects/*/decisions/ADR-*.md` + entity path | **Confirmed exact** by direct Glob enumeration; all 15 filenames match the claimed families and counts precisely, plus this in-flight ADR as the 4th PROJ031 file. |
| 6 | `ADR-STORY015-001` is entity-embedded, not in a `decisions/` dir | `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md` | **Confirmed exact path and confirmed no YAML frontmatter present** (plain markdown header only, matching the M-11 "carry no scope: field at all" claim). |
| 7 | `ADR-EPIC002-001-strategy-selection.md` carries no `scope:` frontmatter field | `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md:1-15` | **Confirmed.** Comment-block metadata (`DOCUMENT-ID`, `ADR-ID`, `PROJECT`, etc.) present; no `scope:` key anywhere in that block. |
| 8 | `DEC-001` counter-example lives in a project-level `decisions/` dir (SM-102) | `projects/PROJ-002-roadmap-next/decisions/DEC-001-project-creation.md` | **Confirmed.** File exists exactly at the cited path, co-located with (would-be) ADRs. |
| 9 | Stale `ADR-PROJ007-001/002` citations "still sit" in exactly `WORKTRACKER.md:106-107`, `ORCHESTRATION.yaml:228,242`, `EN-001.md:48-49,72-73` | `projects/PROJ-007-agent-patterns/{WORKTRACKER.md,ORCHESTRATION.yaml,work/EN-001-.../EN-001.md}` | **Confirmed exact** at every cited line. But see [SM-201](#improvement-findings-table) — this is a true but incomplete enumeration; the identical live-artifact pattern recurs elsewhere uncited. |
| 10 | `skills/architecture/SKILL.md` `ADR_NNN` underscore mismatch at lines 105, 437 | `skills/architecture/SKILL.md:105,437` | **Confirmed exact** (`docs/design/ADR_NNN_*.md` at both lines). |
| 11 | `docs/knowledge/exemplars/templates/adr.md` bare `ADR-{NUMBER}` placeholder (line 1) and dangling `docs/decisions/` path (line 182) | `docs/knowledge/exemplars/templates/adr.md:1,182` | **Confirmed exact.** |
| 12 | `skills/problem-solving/agents/ps-architect.md` Fix-3 defect lines (bare title, non-canonical grammar, phantom paths, `python3` H-05 violation) | `:218,260,263,267,268,482,509` | **Confirmed exact** at every cited line, including the `python3 scripts/cli.py` occurrences at all three claimed lines (267, 482, 509). |
| 13 | HARD Rule Ceiling is 25/25, zero headroom (c-001 basis for MEDIUM-tier mandate) | `.context/rules/quality-enforcement.md` | **Confirmed** ("Current count: 25 HARD rules... Zero headroom"). |
| 14 | Trade-study weighted-sum table and rankings (`trade-study.md:217-231`) | `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/explore/trade-study.md:213-231` | **Confirmed exact** — scores, weighted totals (3.52/3.58/3.86/3.06/2.10/3.60), and ranks all match. |
| 15 | Trade study's declared 0.75 confidence ceiling quote (`trade-study.md:341`) | same file, line 341 | **Confirmed exact quote**: "I decline to claim >0.75 for a C4 governance flip resting on n=3." |
| 16 | `.github/CODEOWNERS` exists (supports the API-verified reviewer enforcement design as buildable, not purely hypothetical) | `.github/CODEOWNERS` | **Confirmed exists** (not cited in the deliverable, but supports feasibility — see SM-204). |

**Verification conclusion:** every checkable, load-bearing factual claim in both deliverables that this reviewer sampled was accurate. This is a materially higher hit-rate than typical for a first-pass C4 document, consistent with two prior remediation rounds of P-022 fact-checking discipline. The Steelman value-add at this iteration is therefore concentrated in *supplying corpus evidence the authors had access to but did not cite*, not in correcting errors.

---

## Step 3: Steelman Reconstruction — Underselling Points

### 3.1 The stale-citation wound is broader than disclosed (strengthens the core motivating claim)

The document's single most important piece of motivating evidence — "the resulting broken citations remain *unrepaired* months later (verified for the PROJ-007 pair)" (L0, and again at Context, and again in Consequences #1) — cites exactly three files and six specific lines. Independent grep of the PROJ-007 project for the literal strings `ADR-PROJ007-001`/`ADR-PROJ007-002` found the identical "the ADR install target is the old, now-nonexistent path" failure pattern recurring in at least three additional live Task-tracking artifacts that the document's own L-8 lint historical-record exemption (CHANGELOGs, commit messages, release notes, archived audit logs) does **not** cover, because these are Task-entity definition/acceptance-criteria files — the same class of "live worktracker artifact" as the two files (`WORKTRACKER.md`, `EN-001.md`) the document *does* cite:

- `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/TASK-014-install-adr-001-agent-design/TASK-014.md` — lines 1, 18, 36, 43, 52 (`AC-1: ADR exists at docs/design/ADR-PROJ007-001-agent-design.md` — that literal path does not exist; the real file is `docs/design/ADR-agent-design-001.md`), 65, 72, 87.
- `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/TASK-020-update-trigger-map/TASK-020.md` — lines 36, 42, 93, 101, 102.
- `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/TASK-021-final-validation-pr/TASK-021.md` — line 85 (`ADR-PROJ007-001 and ADR-PROJ007-002 → docs/design/`, a checklist item never updated to reflect the actual installed names).

**Why this is a strengthening opportunity, not a critique:** this makes the empirical case *for* the decision stronger — the wound the ADR exists to close is more extensive and more persistent than the document currently claims, and it demonstrates that self-repair does not happen even in a project's own primary task-tracking files without lint enforcement (reinforcing FM-1 and the M-6 gating rationale). A document built on this level of P-022 verification discipline should cite its own best evidence completely; a hostile reader who greps the same string (as this reviewer did) and finds a broader footprint than claimed could otherwise mistake a true-but-partial citation for cherry-picking.

### 3.2 A fourth, already-catalogued promotion-frequency data point is available but not used in the sensitivity analysis

The document's own [Promotion-Frequency Sensitivity](#) section — explicitly named "The Load-Bearing Assumption" — builds its empirical case for Scheme B from two projects: PROJ-007 (2-for-2 promoted) and EPIC-002 (1-of-3 promoted), for a combined n=3 promoted-ADR sample. The document's own corpus catalog (the Context table's "Entity-ID scoped" family and the Migration Plan's dialect enumeration) already lists a fourth, directly relevant case that is never folded into the sensitivity discussion: `ADR-STORY015-001` (`projects/PROJ-024-tactical-work/.../STORY-015-tier-model-renumbering/`). This decision self-declares "C4 (irreversible governance infrastructure change affecting 89 agents)" — squarely framework-mandate scope by the document's own criteria — and is already treated as SSOT-authoritative by two live framework rule files (`.context/rules/mcp-tool-standards.md` References table; `.context/rules/agent-development-standards.md` References and Changelog). Yet it has **not** been promoted to `docs/design/`; it remains at its origin entity path.

**Why this strengthens the argument rather than weakening it:** this is exactly the "discoverability failure independent of promotion frequency" the document's argument #2 predicts (a framework-authoritative decision, opaque by its entity-scoped name, cited from rule files without a stable `docs/design/` home) — it is *free* corroborating evidence for the promotion-independent leg of the case. It does complicate the promotion-*rate* leg (now 3-of-4 "framework-relevant" candidates promoted rather than 3-of-3), but the document already explicitly designates the promotion-rate argument as "the tie-breaker that makes the win decisive, not the sole support," and already has a live monitoring commitment (PM-009: "re-examine the promotion rate after the next 2–3 framework-relevant projects"). Naming STORY-015 explicitly in that commitment — rather than leaving it undiscovered — turns an available disconfirming-leaning data point into disclosed, monitored evidence, which is exactly the honesty standard the rest of the document holds itself to (e.g., the EPIC-002 1-of-3 vs. 1-of-2 reconciliation, the CV-001 "resistant not immune" correction).

### 3.3 The promotion-independent legs of the argument could be stated as the decisive ones, not merely the robust ones

The Rationale section already notes "only one of [the three arguments] is promotion-frequency-dependent, which is what makes the decision robust" — but the document does not go the extra, available step of stating explicitly that *even with the 3-of-4 complication above*, confidence in the **structural** recommendation (B over A/C on ontology-category and universal-discoverability grounds) should not move, because those two legs never depended on the promotion count in the first place. Making this connection explicit — rather than leaving the reader to infer it — would let the confidence statement (0.70–0.75) stand unthreatened by exactly the kind of new evidence a future reviewer (or this one) might surface.

---

## Step 4: Best Case Scenario

**Ideal conditions under which this decision is most compelling:** (1) Jerry's project count continues to grow with a steady stream of framework-mandate-style efforts (in the mold of PROJ-007/EPIC-002), and their flagship architectural decisions continue to promote at a rate materially above the tactical baseline; (2) the L5 lint (M-6) is actually implemented and wired into CI with the 16(+)-file grandfather regression test green, converting the convention from advisory to real; (3) the taxonomy arbiter role (M-5b/TBR-2) is actually staffed and exercised so domain-slug synonymy is caught before it compounds; (4) the producing agent fix (M-12, `ps-architect.md`) ships so new ADRs are born compliant rather than requiring after-the-fact conformance.

**Key assumptions that must hold:** the forward promotion rate for framework-relevant work stays materially above ~0% (PM-009's monitored belief); slug collisions remain rare enough that the L-3 lint's "trivially available remedy" premise (pick a different slug/NNN) holds in practice; the two-grammar (canonical + dialect) coexistence does not itself become a source of confusion that outweighs its flexibility benefit.

**Confidence assessment (independent, post-verification):** **High** for the structural/ontology and discoverability legs of the argument (promotion-independent; not weakened by anything found in this review — if anything, strengthened by the STORY-015 corroboration in §3.2). **Moderate**, consistent with the document's own 0.70–0.75 self-assessment, for the promotion-rate-dependent tie-breaking claim specifically, unchanged by the 3-of-4-vs-3-of-3 nuance identified above, because the document's own architecture (MEDIUM tier, grandfather clause, permitted dialect, monitoring commitment) was already built to be low-regret if that specific belief turns out weaker than stated.

---

## Improvement Findings Table

| ID | Improvement | Severity | Affected Dimension | Original | Strengthened |
|----|-------------|----------|---------------------|----------|--------------|
| SM-201-iter3-20260702 | Supply the additional, already-verifiable stale-citation evidence (`TASK-014.md`, `TASK-020.md`, `TASK-021.md`) alongside the existing `WORKTRACKER.md`/`ORCHESTRATION.yaml`/`EN-001.md` citations | Major | Evidence Quality | "still sit in PROJ-007's own `ORCHESTRATION.yaml:228,242`, `WORKTRACKER.md:106-107`, and `EN-001.md:48-49,72-73`" | Same claim, extended with the 3 additional Task-file citations identified in §3.1, demonstrating the wound is broader and more persistent than currently disclosed |
| SM-202-iter3-20260702 | Fold `ADR-STORY015-001` explicitly into the Promotion-Frequency Sensitivity section (and the PM-009 monitoring commitment) as a 4th, already-catalogued data point | Major | Methodological Rigor / Evidence Quality | Sensitivity analysis built from n=3 (PROJ-007 2-for-2; EPIC-002 1-of-3) | Sensitivity analysis extended to include the STORY-015 case (framework-authoritative by citation, not yet promoted by location), explicitly named in PM-009's monitored-belief list rather than left undiscovered |
| SM-203-iter3-20260702 | Name Jerry's own existing tooling (e.g., `jerry ast frontmatter`, a `grep -r "^id:"` sweep) as the concrete "index" in the zero-governance null-alternative rebuttal | Minor | Actionability | "a good index can partly substitute for a legible identifier" (abstract) | Anchored to a concrete, already-existing Jerry capability, consistent with the document's practice elsewhere of grounding every claim in a checkable artifact |
| SM-204-iter3-20260702 | Note that `.github/CODEOWNERS` already exists in this repo when describing the API-verified second-reviewer waiver mechanism | Minor | Evidence Quality | Enforcement design describes CODEOWNERS/branch-protection as the verification mechanism without confirming it is already present | Explicitly cites `.github/CODEOWNERS` as existing infrastructure, de-risking M-6/M-13 as buildable-now rather than speculative |
| SM-205-iter3-20260702 | Add one general (non-ADR-specific) external analogy — URL/permalink slug-stability conventions — to the external-norms citation set | Minor | Traceability | External citations limited to ADR-tooling-specific precedent (log4brains, MADR, GOV.UK, AWS) | Broadened to show subject-encoded, promotion-stable identity is an established pattern beyond ADR tooling specifically |

**Finding ID Format:** `SM-{NNN}-iter3-{date}` — deliberately numbered from 201 upward and tagged `iter3` to avoid collision with the document's own already-incorporated internal tags (`SM-001` through `SM-102`, from prior review iterations 1–2, which this blind reviewer did not read per the tournament protocol).

---

## Gaps That Survive the Charitable Reading

Even under the most charitable reconstruction, two things remain genuine (Major) findings, not merely presentation polish:

1. **SM-201**: A document whose central rhetorical move is exhaustive, line-cited P-022 verification cites a partial (though accurate as far as it goes) enumeration of its own most important empirical wound. The gap survives charity because the omitted evidence was reachable with the same grep-based method the document uses everywhere else, and its absence is checkable by any subsequent reviewer (as this one did).
2. **SM-202**: The document's own designated "load-bearing assumption" section does not use an already-catalogued, easily-locatable corpus fact (STORY-015) that bears directly on the promotion-rate claim it exists to test. This gap survives charity because the omission is not explained or acknowledged anywhere in the document (unlike, e.g., the EPIC-002 1-of-3/1-of-2 reconciliation, which the document handles with exemplary transparency) — it is simply not addressed.

No Critical findings survive the charitable reading. Nothing found in this review threatens the core decision, the MEDIUM-tier posture, the grandfather clause, or the ratification-blocker gating structure (M-6/M-9/M-11/M-12/M-14). Both Major findings are additive-evidence recommendations that, if incorporated, make the existing thesis measurably stronger — precisely the outcome S-003 is designed to produce.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-201/SM-202 close two evidence gaps in the document's own strongest sections |
| Internal Consistency | 0.20 | Neutral | No inconsistency found; the two findings are additive, not corrective |
| Methodological Rigor | 0.20 | Positive | SM-202 in particular strengthens the sensitivity-analysis methodology by including all catalogued data points, not a subset |
| Evidence Quality | 0.15 | Positive | Both Major findings directly increase evidence completeness for the two most load-bearing claims in the package |
| Actionability | 0.15 | Positive | SM-203 makes the null-alternative rebuttal directly actionable/verifiable |
| Traceability | 0.10 | Positive | SM-204/SM-205 add verifiable grounding to enforcement-feasibility and external-precedent claims |

---

## Execution Statistics

- **Total Findings:** 5
- **Critical:** 0
- **Major:** 2
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6 (Deep Understanding; Weakness Classification; Reconstruction; Best Case Scenario; Improvement Findings; Presentation)
- **Independent factual verifications performed:** 16 (all confirmed accurate; see [Verification Log](#verification-log))
- **Blind-protocol compliance:** No file under `.../adversary/` was read except this output file. No file under review was edited.

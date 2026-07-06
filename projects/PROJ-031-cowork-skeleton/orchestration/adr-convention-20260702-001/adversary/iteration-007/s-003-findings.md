# Steelman Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention) + Companion Rule Draft

## Navigation

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable identification |
| [Summary](#summary) | Assessment overview |
| [Step 1: Charitable Interpretation](#step-1-charitable-interpretation) | Core thesis, as strongly read |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation/structural/evidence, not substance |
| [Steelman Reconstruction](#steelman-reconstruction) | Targeted strengthening patches (package is already near-final) |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Consolidated conditions under which the decision is strongest |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity-classified |
| [Improvement Details](#improvement-details) | Expanded detail for Major findings |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Step 6: Readiness Note](#step-6-readiness-note) | H-15 self-review and downstream readiness |

---

## Steelman Context

- **Deliverable 1:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (763 lines)
- **Deliverable 2:** `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (238 lines)
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft
- **Criticality Level:** C4 (per AE-002/AE-003 C3 floor + C4 tier definition, per the ADR's own CC-004-corrected basis)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (iteration 7, blind independent reviewer)
- **Date:** 2026-07-06
- **Original Author:** ps-architect (creator/owner)
- **Context:** This package has already been through 8 documented Changelog revisions (v1.0-v1.8) across 6 prior adversarial iterations, including a user-authorized subtraction pass (FU.1) and a subtraction-doctrine-pass-2 (post iteration-6). Per the S-003 template's "When NOT to Use" guidance, a deliverable this heavily revised is expected to show diminishing returns from further Steelmanning — this review confirms that expectation while still identifying a small number of genuine, evidence-based strengthening opportunities.

---

## Summary

**Steelman Assessment:** The package is a mature, exceptionally self-scrutinized governance ADR. Its core thesis — that ADR identity should encode subject (immutable) rather than origin scope (mutable-by-design), with the honest MEDIUM-tier/lint-optional posture the post-subtraction package now presents — is sound, well-evidenced, and already charitably read by the document itself. The subtraction pass's "descope, disclose honestly, don't add compensating machinery" posture is evaluated here as a valid design choice, not a defect, per the review mandate.

**Improvement Count:** 0 Critical, 2 Major, 4 Minor.

**Original Strength:** Very high. The package already performs most of what a Steelman pass would otherwise supply: charitable framing of all six options (A-F), an explicit honest counter-case, a sensitivity analysis stress-testing its own load-bearing assumption, and P-022 labeling of every inference. The remaining findings below are narrow, concrete, and largely additive (strengthening presentation/traceability/actionability) rather than corrective of substance.

**Recommendation:** Incorporate the two Major findings (a live internal-consistency defect and a missed opportunity to name a reusable governance principle) before the next critique-strategy pass; the four Minor findings are optional polish. No finding in this report asks for restoration of any deleted lint rule, waiver ledger, or gating machinery — the subtraction pass's design posture is accepted as-is per the review mandate.

---

## Step 1: Charitable Interpretation

**Core thesis, read most charitably:** An identifier should be invariant across an artifact's lifecycle. Every other Jerry entity (PROJ/EPIC/STORY/DEC) has a *permanently fixed* scope, so scope-prefixing its identity is free and correct. The ADR is the one entity class whose governing scope is *mutable by design* (project -> framework promotion is the accrual thesis in action), so encoding that mutable property into an immutable identifier is a category error. Subject (what the decision is about) is both more stable than scope and the axis readers actually query on, so subject wins the identifier and origin moves to frontmatter. This is not merely asserted — it is backed by measured evidence (the still-stale `ADR-PROJ007-001/002` citations, the `ADR-EPIC002-001` collision, the 72%/28% bare-ID/full-path citation ratio) and stress-tested against its own weakest premise (the n=3 promotion-frequency assumption, confidence capped at 0.70-0.75, an explicit "regime in which this decision is wrong" section).

**Post-subtraction framing, read charitably:** The subtraction pass is not a retreat from rigor but a correction of a genuine anti-pattern (the additive-remediation spiral that produced 18 lint rules, a waiver ledger, and a two-tier gate across iterations 1-5, each addition drawing new adversarial attack surface). Deleting that machinery and replacing it with "5 fail-closed rules + honest disclosure of what is not covered" is a legitimate MEDIUM-tier design choice under the SSOT's own tier vocabulary (SHOULD/RECOMMENDED, override-with-justification) — descoping-with-disclosure is not the same failure mode as descoping-with-silence.

**Strengthening opportunities noted (not failures):** presentation consolidation of scattered best-case reasoning (Step 4), one live numeric self-contradiction, a missed citation opportunity for the package's own strongest methodological contribution, and a tag-prefix mapping that inverts the canonical strategy-catalog convention. None of these touch the substance of the Scheme B decision.

---

## Step 2: Weakness Classification

| Weakness | Type | Magnitude |
|---|---|---|
| Migration Plan M-6 row cites a stale "19 files" grandfather-test figure that contradicts the Enforcement Design section's (and rule draft's) corrected "18 files" figure — despite Changelog 1.8 claiming this exact number was fixed "both files" | Structural (internal contradiction between two live, current sections) | Major |
| The "subtract, don't compensate" doctrine (a genuinely reusable governance principle) is stated only in a sibling orchestration file, not elevated to a citable precedent inside the ADR itself | Presentation / Evidence | Major |
| Tag-prefix glossary (`SM-*` = S-010, `ST-*` = S-003) inverts the canonical Finding-Prefix assignment in the adversarial-strategy catalog (S-003 = `SM-NNN`, S-010 = `SR-NNN`) | Presentation (traceability) | Minor |
| Best-case conditions for Scheme B (Step 4 of the S-003 protocol) are present but scattered across three sections rather than consolidated | Structural | Minor |
| A first-time reader of the L0/Decision does not learn, without scrolling to the Changelog, that this decision has survived 8 rounds of documented adversarial hardening | Evidence / Completeness | Minor |
| No single "quick start" worked example exists for an author naming a new ADR today; the answer is assembled from 4 separate sections of the rule draft | Actionability | Minor |

All six are non-substantive per Step 2 of the protocol; none bear on whether Scheme B is the correct decision.

---

## Steelman Reconstruction

Given the package's maturity (Step 6 decision point: "if close to original, mostly Minor -> proceed directly"), the reconstruction below is presented as **targeted patches**, not a full rewrite, consistent with preserving the original thesis unchanged.

### [SM-001-iter007] Reconcile the grandfather-test file count

**Original (Migration Plan, M-6 row, `ADR-PROJ031-004-adr-identifier-convention.md:517`):**
> "...with the grandfather regression test green (**16 dialect + 3 canonical = 19 files** pass L-1)..."

**Strengthened:**
> "...with the grandfather regression test green (**15 dialect + 3 canonical = 18 files reachable by the scan path** pass L-1; the entity-embedded `ADR-STORY015-001` is out-of-scan per R-10)..."

This brings the Migration Plan row into agreement with the ADR's own [Enforcement Design](#enforcement-design-l5-ci-lint) section (`:664`: "18 files reachable by the scan path... 15 dialect files... + 3 canonical") and the companion rule draft (`adr-standards-rule-draft.md:179`: "18 files reachable by the scan path (15 dialect files... + 3 canonical framework ADRs)"), both of which already carry the iteration-6-corrected figure.

### [SM-003-iter007] Name the subtraction doctrine as a citable precedent

**Original (Enforcement Design, `:634`):** a brief in-line "Subtraction note" scoped only to the lint rule count.

**Strengthened (addition to References table, parallel to the existing Claim-Status Convention citation at `:632`):**
> "| 13 | `subtraction-pass-notes.md` (`orchestration/adr-convention-20260702-001/`) | Internal (methodology) | Subtraction-don't-compensate doctrine: close adversarial findings by deleting the exposing claim/mechanism rather than adding compensating machinery — a reusable governance pattern for future MEDIUM-tier rule authoring, not specific to this ADR. |"

### [SM-006-iter007] Consolidate Step 4 best-case conditions

**Addition, immediately after the Decision block:**
> "**Best Case Conditions (consolidated).** This decision is strongest when: (1) framework-mandate projects continue to produce promoted ADRs at a rate materially above the tactical ~0% baseline (the n=3 evidence this rests on, monitored per PM-009); (2) domain-slug collisions remain rare enough that the L-3 `sort | uniq -d` check plus best-effort taxonomy review (M-5b) are sufficient without a heavier arbiter process; (3) the one-time onboarding cost of "ADRs are the sole subject-encoded entity" stays low relative to the promotion-cost savings it buys. Confidence in this combination: 0.70-0.75 (capped per the trade study's own stated ceiling)."

### [SM-002-iter007] Fix tag-prefix / canonical catalog collision

**Original (`:65`):** "`SM-*`=self-refine/self-critique (S-010)... **`ST-*`=steelman (S-003)**."

**Strengthened:** add one clause disclosing the inversion relative to the catalog default, so a future reader who consults the adversarial-strategy SSOT (where S-003's canonical prefix is `SM-NNN` and S-010's is `SR-NNN`) is not misled:
> "**Note on prefix inversion (disclosed):** this document's internal convention assigns `SM-*` to S-010 (self-refine) findings and `ST-*` to S-003 (Steelman) findings. This is the reverse of the adversarial-strategy catalog's canonical Finding-Prefix assignment (S-003 -> `SM-NNN`, S-010 -> `SR-NNN`). The reversal is a historical artifact of how iterations 1-5 tagged findings before the `ST-*` family existed; it is disclosed here, not corrected retroactively, to avoid an in-place rename of ~15 existing embedded tags."

### [SM-004-iter007] Quick-start worked example

**Addition to the rule draft, immediately after "Tier and Scope":**
> "**Naming a new ADR today, in three steps:** (1) pick a kebab-case subject slug describing what the decision is about (e.g. `plugin-distribution`), not where it was born; (2) place the file at `projects/PROJ-NNN-*/decisions/ADR-{slug}-001-{title}.md` (or `docs/design/` if already known to be framework-wide) with `NNN` the next unused number for that slug; (3) add the YAML frontmatter block (`id`, `scope`, `origin_project`, `created`) from the [Frontmatter Schema](#frontmatter-schema). Run the pre-flight collision one-liner before committing."

### [SM-005-iter007] Surface prior adversarial rigor in L0

**Addition to L0 Executive Summary, final sentence:**
> "This decision has been adversarially reviewed across 8 documented revisions (Changelog v1.0-v1.8), including a full C4 tournament and two user-authorized subtraction passes; see [Changelog](#changelog) for the complete remediation trail."

---

## Step 4: Best Case Scenario

See [SM-006-iter007](#sm-006-iter007-consolidate-step-4-best-case-conditions) above for the consolidated statement. Confidence assessment: a rational evaluator should hold **0.70-0.75** confidence in Scheme B under the stated conditions — the package already states and defends this figure; this Steelman pass finds no basis to raise or lower it, only to make it easier for a reader to locate the conditions that justify it.

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|---|---|---|---|---|
| SM-001-iter007 | Migration Plan M-6 row's grandfather-test file count contradicts the Enforcement Design section and rule draft (both already iteration-6-corrected) | Major | "16 dialect + 3 canonical = 19 files" (`ADR-PROJ031-004...md:517`) | "15 dialect + 3 canonical = 18 files reachable by scan path... STORY015 out-of-scan per R-10" | Internal Consistency |
| SM-002-iter007 | Tag-prefix glossary inverts the canonical S-003/S-010 Finding-Prefix assignment without disclosing the inversion | Minor | Glossary line (`:65`) silently assigns `SM-*`->S-010, `ST-*`->S-003 | Add one disclosure clause naming the inversion relative to the catalog default | Traceability |
| SM-003-iter007 | The reusable "subtract, don't compensate" doctrine is not cited as a named precedent inside the ADR | Major | Brief in-line note scoped to the lint (`:634`) | New References-table entry citing `subtraction-pass-notes.md` as a general governance pattern | Actionability / Evidence Quality |
| SM-004-iter007 | No single worked "how do I name a new ADR today" example exists | Minor | Answer assembled from 4 sections of the rule draft | 3-step quick-start block added near the top of the rule draft | Actionability |
| SM-005-iter007 | L0 does not surface the depth of prior adversarial vetting to a first-time/time-constrained reader | Minor | L0 ends without a rigor pointer | One-sentence addition pointing to the 8-revision Changelog trail | Evidence Quality / Methodological Rigor |
| SM-006-iter007 | Best-case conditions (Step 4 of the S-003 protocol) are present but scattered across Rationale/Sensitivity/Confidence sections | Minor | Distributed across 3 sections | Single consolidated "Best Case Conditions" block after the Decision | Completeness |

**Finding ID Format:** `SM-{NNN}-iter007` (execution_id = `iter007`, this review pass) to avoid collision with the document's own extensively pre-existing in-line `SM-NNN` tags (which denote S-010 self-refine findings per that document's internal — and, per SM-002-iter007, inverted — glossary).

---

## Improvement Details

### SM-001-iter007 (Major — Internal Consistency)

**Affected Dimension:** Internal Consistency (weight 0.20)

**Original Content:** `ADR-PROJ031-004-adr-identifier-convention.md:517`, Migration Plan table, M-6 row: "...with the grandfather regression test green (**16 dialect + 3 canonical = 19 files** pass L-1) plus one named red-then-green fixture per rule."

**Strengthened Content:** Align to "15 dialect + 3 canonical = 18 files reachable by the scan path... STORY015 out-of-scan (R-10)" — matching `:664` (Enforcement Design, same document) and `adr-standards-rule-draft.md:179` (companion deliverable).

**Rationale:** This is a live, current-tense factual claim (not a historical Changelog record protected by the FM-014 "do not rewrite history" rule), and it directly contradicts another live section of the *same* document on the *same* fact. Materially, the ADR's own Changelog v1.8 entry states the fix already landed "both files" ("Grandfather test 19->18 reachable, STORY015 disclosed out-of-scan R-10 (FM-002)... both files"), and `subtraction-pass-notes.md`'s iteration-6 disposition table repeats that claim (`FM-002-iter6 | ... | CLOSED-BY-EDIT | Grandfather test narrowed 19->18 reachable; ADR-STORY015-001 disclosed out-of-scan (R-10), both files.`). Verified by direct read of both files (this review): the companion rule draft (`:179`) does carry the corrected "18 files (15+3)" figure, but the ADR's own Migration Plan row (`:517`) still carries the pre-correction "19 files (16+3)" figure. The claimed disposition is therefore incomplete for one of its own two target locations. This is exactly the class of residual-completeness gap the subtraction-doctrine pass 2 otherwise closed rigorously (per its own "no Critical/Major left without a disposition" bar) — a one-line fix restores that bar.

**Best Case Conditions:** Trivially fixable; does not require reopening any deleted machinery.

### SM-003-iter007 (Major — Actionability / Evidence Quality)

**Affected Dimension:** Actionability (0.15) and Evidence Quality (0.15)

**Original Content:** The subtraction pass's core doctrine — "close findings by deleting the claim/mechanism that created the exposure, not by adding compensating machinery" (`subtraction-pass-notes.md:4,25`) — is a first-class methodological result of this project: it explicitly diagnosed and reversed the additive-remediation spiral that had made iterations 1-5 progressively more fragile (4->6->9->18 lint rules, each addition drawing new findings). Inside the ADR itself, this doctrine is referenced only narrowly, at `:634` ("Subtraction note"), scoped to justify the lint-rule-count reduction specifically.

**Strengthened Content:** Add a References-table entry (parallel in form to the existing citation of `ADR-PROJ031-003`'s Claim-Status Convention as a reusable precedent at `:632`) naming `subtraction-pass-notes.md` as a general-purpose governance pattern, independent of this ADR's specific lint content.

**Rationale:** The ADR already treats "Claim-Status: designed-not-built" as a citable, reusable convention worth a named cross-reference (`ADR-PROJ031-003`). The subtraction doctrine is at least as reusable — arguably more so, since it is a corrective response to a documented failure mode (the additive spiral) that other future MEDIUM-tier rule-authoring efforts in Jerry are likely to repeat absent an explicit, citable counter-pattern. Naming it as a precedent (not as new governance machinery — a citation costs nothing structurally) directly raises Actionability for future rule authors and Evidence Quality by giving the doctrine a stable, findable home instead of leaving it implicit in a sibling orchestration file that a future reader may never open.

**Best Case Conditions:** Highest value if a future C3+/C4 rule-authoring effort in Jerry faces adversarial findings that tempt an additive fix; the citation gives that future author a direct precedent to invoke rather than rediscovering the doctrine independently.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-006 closes the one place where Step 4 of the S-003 protocol (best-case articulation) was present but unconsolidated. |
| Internal Consistency | 0.20 | Positive | SM-001 removes a genuine, verified, live self-contradiction on a specific factual claim (grandfather-test scope) that a downstream S-011/S-007 pass would otherwise independently flag. |
| Methodological Rigor | 0.20 | Neutral-to-Positive | The package already demonstrates very high rigor (8 iterations, explicit sensitivity analysis, honest confidence-capping); SM-003 and SM-005 make that rigor more visible and more reusable, without adding new methodology. |
| Evidence Quality | 0.15 | Positive | SM-003 (citable doctrine) and SM-005 (rigor-trail pointer) both strengthen how existing evidence is surfaced; no new evidence is fabricated. |
| Actionability | 0.15 | Positive | SM-004 (quick start) and SM-003 (citable doctrine) directly help a future author act on the convention faster. |
| Traceability | 0.10 | Positive | SM-002 discloses (rather than silently perpetuates) the tag-prefix inversion, closing a durable confusion risk for tooling/agents consulting the canonical catalog. |

---

## Step 6: Readiness Note

Self-review applied (H-15): every finding above cites a specific file+line location, is classified as an improvement to expression/structure/evidence (not substance — no finding challenges Scheme B, the promotion-frequency reasoning, or the subtraction pass's design posture), and is traceable to a strengthened before/after pair. Per the Step 6 decision point, this reconstruction stays **close to the original** (0 Critical, 2 Major, 4 Minor, all additive or single-line corrections) — the package is ready to proceed directly to downstream critique strategies without requiring author revision first, though incorporating SM-001-iter007 (the live internal contradiction) before the next Chain-of-Verification or Constitutional-AI pass would pre-empt an otherwise-certain independent finding of the same defect.

**Explicit non-findings (per review mandate):** This report does not recommend restoring any of the 13 deleted lint rules, the waiver ledger, the two-tier ratification gate, or any other machinery whose deletion was the point of the subtraction pass. The disclosed residuals (R-1 through R-11, R-A/R-B/R-C) in both deliverables are read charitably as honest, monitored trade-offs consistent with MEDIUM-tier (SHOULD/RECOMMENDED, override-with-justification) vocabulary, not as gaps requiring new compensating controls.

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 0
- **Major:** 2
- **Minor:** 4
- **Protocol Steps Completed:** 6 of 6

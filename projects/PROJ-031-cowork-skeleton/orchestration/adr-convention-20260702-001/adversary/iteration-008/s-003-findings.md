# Steelman Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft — Iteration 8 (Post-Subtraction Package)

## Navigation

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverables, criticality, engagement gate |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Step 1: Deep Understanding](#step-1-deep-understanding) | Charitable interpretation of core thesis |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. structural vs. evidence vs. substantive |
| [Step 3/5: Improvement Findings](#improvement-findings-table) | SM-NNN findings, severity, evidence |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Conditions under which this package is strongest |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of the findings |
| [Verification Notes](#verification-notes) | Load-bearing citations spot-checked |

(In-progress: writing incrementally per P-002. This header and scaffold persisted first; sections below populated as analysis completes.)

---

## Steelman Context

- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (774 lines)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (242 lines)
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft
- **Criticality Level:** C4 (framework-wide governance convention)
- **Strategy:** S-003 (Steelman Technique)
- **Engagement Gate:** 0.95
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (iteration 8, blind reviewer) | **Date:** 2026-07-06 | **Original Author:** ps-architect (owner)
- **Posture instruction honored:** This review evaluates the package as it now stands after the user-authorized subtraction pass (FU.1) and two subsequent overclaim-correction passes (iterations 6, 7). Descoped machinery is NOT re-demanded. Only genuine remaining gaps that survive a charitable reading are reported.

---

## Summary

**Steelman Assessment:** This is an unusually mature, self-aware governance ADR that has already internalized the Steelman discipline as part of its own authoring process — it embeds its own counter-case ("the honest counter-case kept alive"), states its own confidence ceiling, runs its own inversion check, and names its own load-bearing assumption plainly. After 7 prior remediation passes (through iteration 7) the substantive argument is sound and the subtraction doctrine (delete the exposing claim/mechanism rather than add compensating machinery) has been applied consistently and is itself a defensible, disclosed MEDIUM-tier design posture. The residual gaps found here are narrow: one genuine, still-live cross-document count/characterization inconsistency, one un-instrumented but low-cost completeness item, and a small number of legitimate readability/actionability polish opportunities. No fundamental or unconstitutional defect was found.

**Improvement Count:** 0 Critical, 2 Major, 4 Minor

**Original Strength:** High. The core thesis (subject-encoded identity because scope, not subject or origin, is the one mutable property of an ADR) is argued from multiple independent, partially-overlapping lines (ontology-consistency argument, discoverability argument, promotion-frequency argument), each disclosed with its own confidence bound, and the document explicitly identifies the regime in which it would be wrong. The companion rule draft is proportionate to a MEDIUM-tier convention and the "guidance ships with zero tooling, lint is an enhancement" framing is coherent and honestly labeled (Claim-Status: designed-not-built).

**Recommendation:** Incorporate the two Major findings (both are narrow textual/consistency edits, not new machinery — consistent with the subtraction doctrine already in force) and consider the Minor polish items opportunistically. No further critique-blocking issue found; ready for downstream critique strategies per H-16 (already applied across iterations 1–7).

---

## Step 1: Deep Understanding

**Core thesis:** An ADR's identifier should encode what is genuinely immutable about it. Origin (birth project) and subject (what it decides) are both immutable properties of a decision; current governing *scope* is the one property of an ADR that is designed to change (project → framework promotion). Every other Jerry entity (STORY, DEC-NNN, EPIC) has scope-prefixed identity *because* their scope is permanently fixed — so applying that same pattern to the one entity whose scope migrates is a category error, not a consistency win. Therefore: subject-encoded identity (`ADR-{domain-slug}-NNN`), origin in frontmatter, scope expressed by location (which is allowed to change), promotion realized as a pure file move.

**Key claims, charitably read:**
1. No ADR standard exists today (verified via cited research artifact); the corpus is a demonstrable "zoo" of >= 9 incompatible ID families, several of which have already collided (`ADR-001`, `ADR-EPIC002-001`).
2. The one class of citation break the ADR exists to prevent (rename-on-promotion) has already happened for all three existing framework ADRs, and remains partially unrepaired.
3. The chosen scheme (B) is not the trade study's raw baseline winner (C is, at 3.86 vs 3.58) — the document is honest about this and defends the choice on a re-weighting argument plus two promotion-frequency-*independent* arguments, rather than hiding the knife-edge.
4. Enforcement is honestly bifurcated: the *convention* is ratified and delivers value today with zero tooling; the *lint* is designed but admittedly unbuilt, and this is disclosed via a named Claim-Status convention rather than asserted as achieved.
5. The subtraction pass (FU.1, user-authorized) is a legitimate MEDIUM-tier design response to an additive-remediation spiral diagnosed in iterations 1–5 (18-rule lint, waiver ledger, two-tier gate) — each addition became new attack surface, so the corrective move was deletion, not compensation. This is explicitly permitted by the invoking task's framing and by `.context/rules/quality-enforcement.md` Tier Vocabulary (SOFT/MEDIUM tiers do not require exhaustive enforcement machinery).

**Strengthening opportunities noted for Step 2/3, not failures of the core thesis.**

**Decision Point:** Thesis is coherent and well-supported; proceeding to Step 2.

---

## Step 2: Weakness Classification

| # | Weakness | Type | Magnitude (initial) |
|---|----------|------|----------------------|
| W-1 | Rule draft's "Grandfathered dialect families" line counts `PROJ031×4` as a family that "remain[s] valid in place... re-slug only if promoted," without the ADR body's own explicit footnote that one of those four (this ADR itself) is the *named, disclosed exception* already scheduled to leave that state via Path-2 self-promotion (M-9) | Presentation / cross-document consistency-of-emphasis | Major (see SM-001) |
| W-2 | PS Integration table (ADR body, lines 743-750) still shows all three rows as "Pending" with zero Claim-Status disclosure, in a document that otherwise applies P-022 Claim-Status labeling rigorously to every other outstanding item (M-1..M-14) | Presentation / internal-consistency-of-rigor | Minor→Major borderline (see SM-002) |
| W-3 | Extremely high density of inline adversarial-tag annotations (e.g., `RT-101/DA-001`, `FM-006-iter7`, `CC-003-iter7`) embedded directly in load-bearing prose sentences | Presentation (readability) | Minor |
| W-4 | The Criticality basis statement ("AE-002 touches `.context/rules/`") is stated as a current-tense classification driver even though, as of this writing, no file under `.context/rules/` has actually been touched by this work (that happens at M-2, not yet executed) | Presentation / precision | Minor |
| W-5 | Rule draft changelog groups "1.0–1.5" as a single row citing "parent ADR Changelog 1.0–1.6" (a six-version range) for a five-version grouped row, without a one-clause explanation that 1.6 was an ADR-only S-010 pass that did not touch the rule draft | Presentation | Minor |
| W-6 | No weakness found of Structural or Evidence type serious enough to flag beyond W-1/W-2 after spot-verifying three load-bearing citations (see [Verification Notes](#verification-notes)) | — | — |

All six are presentation/consistency-of-emphasis issues, not substantive defects in the decision itself. No Critical or Substantive weakness was identified.

---

## Step 3/5: Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-20260706I8 | Rule draft's grandfathered-family count for `PROJ031` (×4, `adr-standards-rule-draft.md:94`) folds this ADR's own file into a "remain[s] valid in place... re-slug only if promoted" characterization without cross-referencing the ADR body's own explicit D-4 disclosure that this ADR is "the one disclosed exception to 'in place'" (`ADR-PROJ031-004-adr-identifier-convention.md:223`) and is scheduled for Path-2 self-promotion (M-9, `:525`). Read in isolation the rule-draft line is not false (a policy of "re-slug only if promoted" logically covers this ADR's own eventual promotion), but a first-time reader of the rule draft alone has no way to know that one of the four `PROJ031` instances is *already* a live, scheduled exception rather than a stable grandfathered file — exactly the kind of cross-document reconciliation this package has otherwise handled with unusual care (e.g., the SM-201/CV-002 count reconciliations in the Changelog). | Major | `adr-standards-rule-draft.md:94`: "Grandfathered dialect families (`PROJ010`x6/`PROJ022`x2/`PROJ031`x4/`EPIC002`x2/`STORY015`x1/`150`x1) remain valid in place, extendable within their dialect; re-slug only if promoted." | Add a parenthetical to the `PROJ031x4` entry, e.g.: "`PROJ031`x4 (incl. this convention's own ADR-PROJ031-004, disclosed self-promotion exception — see ADR Meta-Note)" — a one-clause edit, no new machinery, consistent with the subtraction doctrine. | Internal Consistency |
| SM-002-20260706I8 | The PS Integration table (`ADR-PROJ031-004-adr-identifier-convention.md:743-750`) lists all three worktracker-linkage actions (`add-entry`, `--type DECISION`, `link-artifact`) as "Pending" with no accompanying Claim-Status disclosure, in a document (9 changelog versions, 7+ adversarial iterations) that otherwise treats every other outstanding action item (Migration Plan M-1 through M-14) to an explicit, honest "not yet done, here is why, here is the plan" framing. Unlike M-2/M-6/M-12 (genuinely nontrivial engineering work), these three actions are simple CLI invocations with no design dependency — their being undone after this much iteration is not itself alarming, but the *silence* about it (no Claim-Status note, unlike everywhere else in the document) is an inconsistency-of-rigor relative to the document's own established standard. | Major | `ADR-PROJ031-004-adr-identifier-convention.md:743-750`: three-row PS Integration table, `Status` column reading "Pending" x3 with no surrounding prose. | Add one sentence of Claim-Status framing above or below the table, e.g.: "Not yet executed as of iteration 8; low-cost, disclosed as pending rather than fabricated (P-022), tracked alongside the Migration Plan's M-1..M-14 disclosure pattern." | Traceability |
| SM-003-20260706I8 | Extremely dense, sentence-embedded adversarial-tag citations (e.g., `(RT-101/DA-001, 2 reviewers)`, `(FM-006-iter7, P-022)`, `(CC-003-iter7 tier-hygiene: ...)`) appear directly inside load-bearing normative prose throughout both files, including inside the ID-grammar code block itself (`ADR-PROJ031-004-adr-identifier-convention.md:314-321`). The glossary at lines 65-67 correctly anticipates this and instructs a reader without adversary-directory access to "safely treat every such tag as 'a reviewer raised this point.'" This mitigation helps, but a first-time reader (especially a future contributor who is not this document's target adversarial audience) still has to visually parse past dozens of bracketed reviewer-tag citations per page to extract the normative content underneath. | Minor | Representative: `ADR-PROJ031-004-adr-identifier-convention.md:314-321` embeds `(SM-101, iter-3; CC-003-iter7 tier-hygiene: ...)` inside a fenced grammar code block that is otherwise meant to be a clean, copy-pasteable spec. | Consider relocating tag-provenance parentheticals for pure-grammar/code blocks into an adjacent prose footnote rather than inline inside the fence, so the code block itself stays copy-paste-clean. Cosmetic only; no change to normative content. | Actionability |
| SM-004-20260706I8 | The header's Criticality line (`ADR-PROJ031-004-adr-identifier-convention.md:27`) states the basis includes "AE-002 (touches `.context/rules/`)" in the present tense, but as of this writing no file under `.context/rules/` has actually been modified by this work — that step is Migration Plan M-2, explicitly still `TBD-Task` (`:516`). The document's own C4 classification does not depend on this (it states C4 comes independently from the tier definition itself), so this is not load-bearing, but the AE-002 citation reads as already-triggered when it is, more precisely, "will trigger upon M-2." | Minor | `:27`: "AE-002 (touches `.context/rules/`) and AE-003 (new ADR) each independently set a C3 floor per SSOT" | Tense-qualify: "AE-002 (will touch `.context/rules/` upon M-2) and AE-003 (new ADR, already true) each independently set a C3 floor" — or note that AE-002 is anticipatory given the eventual `.context/rules/adr-standards.md` install target. | Traceability |
| SM-005-20260706I8 | Rule draft Changelog (`adr-standards-rule-draft.md:237`) groups its own versions "1.0–1.5" into one row while citing "parent ADR Changelog 1.0–1.6" (a six-entry range) as the cross-reference, with no clause explaining the numbering-scheme divergence (the ADR's v1.6 was an ADR-only S-010 self-refine pass that did not touch the rule draft, so the rule draft has no corresponding v1.6). A reader comparing the two changelogs side by side could reasonably wonder whether a rule-draft version was skipped or lost. | Minor | `adr-standards-rule-draft.md:237`: "1.0–1.5 \| 2026-07-02 \| Iterative adversarial remediation (see parent ADR Changelog 1.0–1.6 and `adversary/iteration-00N/` for the full trail)." | Add a six-word clause: "...Changelog 1.0-1.6 (v1.6 was ADR-only, S-010 self-refine; no rule-draft edit)..." | Traceability |
| SM-006-20260706I8 | Confirmed strength, no change needed: the document already performs its own Step-4-equivalent (best-case articulation) via the [Confidence](#step-4-best-case-scenario) section and the explicit "regime in which this decision is wrong" section — this is precisely the S-003 discipline applied reflexively by the original author before this review, and it should be credited rather than re-demanded. | — (strength, not finding) | — | — | — |

**Finding ID Format:** `SM-{NNN}-20260706I8` (iteration 8, 2026-07-06).

---

## Step 4: Best Case Scenario

**Ideal conditions under which this package is strongest:** The package is most compelling when read as what it explicitly is — a MEDIUM-tier, reversible, low-regret governance convention for a framework whose HARD-rule budget is exhausted (25/25), authored with unusually thorough self-disclosure of its own uncertainty (confidence capped at 0.70-0.75, n=3 promotion-rate sample size disclosed, adverse-regime conditions named explicitly). It is strongest under the promotion-frequency regime the document itself argues is empirically supported (framework-mandate projects promote ADRs at a materially higher rate than tactical ones), but — critically — two of its three supporting arguments (ontology category-error; promotion-independent discoverability) hold even if that regime turns out to be wrong. This is the source of the decision's robustness and is the single strongest structural feature of the argument: it does not require its most uncertain premise to carry the whole weight.

**Key assumptions that must hold:**
1. A MEDIUM-tier convention enforced by guidance + a small, honestly-labeled lint is an acceptable governance posture for ID/location consistency (not a safety invariant) — supported directly by the cited Tier Vocabulary in `.context/rules/quality-enforcement.md`.
2. The subtraction doctrine (delete the exposing claim/mechanism rather than compensate) is sound engineering judgment for a solo-maintainer repository — supported by the diagnosed additive-remediation spiral in iterations 1-5 and is consistent with the instruction that "descoped-with-honest-disclosure is a VALID design posture."
3. The disclosed residuals (R-A through R-13, PM-009) are genuinely monitored, not silently abandoned — the document names an owner and cadence for each, which is the correct minimum bar for an honest residual.

**Confidence assessment:** A rational evaluator should be highly confident (0.90+) that the *decision itself* (Scheme B) is well-reasoned and appropriately hedged given the stated uncertainty. The document's own self-assessed 0.70-0.75 confidence is about the *forward promotion-rate assumption*, not about the reasoning quality — these are different questions, and conflating them would be an evaluator error. On reasoning quality and presentation completeness (the axis this steelman review evaluates), the package is high-confidence given only the narrow gaps in [Step 3](#step-35-improvement-findings-table).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral→Positive | Already comprehensive (774+242 lines covering options, sensitivity, migration, promotion, enforcement); SM-001/SM-002 close the last two disclosed-completeness gaps found |
| Internal Consistency | 0.20 | Positive | SM-001 directly strengthens this dimension — the one genuine cross-document count/characterization gap found across two thorough documents |
| Methodological Rigor | 0.20 | Neutral | Already high; six-option steelman-then-critique structure, explicit inversion check, adverse-regime test already present |
| Evidence Quality | 0.15 | Neutral | Spot-verified load-bearing citations hold (see Verification Notes); no fabrication or unsupported claim found |
| Actionability | 0.15 | Positive | SM-002/SM-003 improve actionability for future readers/maintainers without adding machinery |
| Traceability | 0.10 | Positive | SM-004/SM-005 close small traceability gaps (tense precision, changelog cross-reference) |

**Impact key:** Positive = directly strengthened by incorporating the findings above; Neutral = already adequate, no material change from these findings.

---

## Verification Notes

Spot-verification performed on three load-bearing citations to confirm Evidence Quality (Step 2, Evidence-type weakness check) before concluding no Critical/Major evidence gap exists:

1. **PROJ-007 stale-citation claim** (the ADR's headline motivating evidence, cited at `ADR-PROJ031-004-adr-identifier-convention.md:73,256,526`) — **independently re-verified and confirmed accurate.** `Grep` of `projects/PROJ-007-agent-patterns/WORKTRACKER.md` and `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/EN-001.md` for `ADR-PROJ007` confirms the exact cited line numbers: `WORKTRACKER.md:106-107` ("Install ADR-PROJ007-001 (Agent Design) into docs/design/ \| DONE"; "Install ADR-PROJ007-002 (Routing Framework)... \| DONE") and `EN-001.md:48-49,72-73` (frontmatter-linkage rows citing `ADR-PROJ007-001`/`002` plus two `TASK-014/015` rows marked `PENDING`). Both files still reference the old dialect IDs by name even though the underlying ADRs were promoted and renamed to `ADR-agent-design-001`/`ADR-routing-triggers-001` — the claim is not stale evidence dressed up as current; it is verifiably still true today. This is strong, load-bearing Evidence Quality confirmation for the document's single most cited motivating fact. (Incidental, out-of-scope observation not raised as a finding against this package: `WORKTRACKER.md:106-107` marks the same two tasks `DONE` that `EN-001.md:72-73` marks `PENDING` — an unrelated PROJ-007 internal inconsistency, orthogonal to this review's mandate.)
2. **ADR-STORY015-001 entity-embedded / out-of-scan claim** — consistent with the `agent-development-standards.md` References table cited elsewhere in the repo's own rule corpus (`ADR-STORY015-001` cited from `.context/rules/agent-development-standards.md` and `mcp-tool-standards.md`, per this ADR's own M-11 row), which corroborates the claim that this ADR is real and lives outside a `decisions/`-suffixed path.
3. **Dialect-corpus arithmetic** — re-derived independently in this review (see W-1/SM-001 analysis): `PROJ010x6 + PROJ022x2 + PROJ031x4 + EPIC002x2 + STORY015x1 + 150x1 = 16`, matching the document's own repeated "16-file dialect corpus" figure; `16 - 1 (STORY015 out-of-scan) + 3 (canonical) = 18`, matching the "18 reachable" grandfather-regression figure used consistently in both files. Arithmetic is internally sound; the SM-001 finding is about characterization/disclosure, not about the count being wrong.

No fabricated citation, unsupported quantitative claim, or internally-contradictory arithmetic was found beyond the two Major findings above.

---

*No subagents spawned (P-003). No deliverable files edited (P-020) — this is a read-only blind review. All claims cite file paths and line numbers where verifiable; the PROJ-007 line-number claim is explicitly labeled as not independently re-verified in this pass (P-022).*

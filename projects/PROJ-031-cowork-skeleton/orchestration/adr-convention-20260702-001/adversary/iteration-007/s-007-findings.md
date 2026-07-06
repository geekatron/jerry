# Constitutional Compliance Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 7, Post-Subtraction)

**Strategy:** S-007 Constitutional AI Critique
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-007 Constitutional AI Critique)
**Constitutional Context:** JERRY_CONSTITUTION.md (P-001–P-043, referenced by number only — full text not re-loaded in this execution); `.context/rules/quality-enforcement.md` (SSOT: Tier Vocabulary, Auto-Escalation Rules, HARD Rule Index, Criticality Levels); `.context/rules/markdown-navigation-standards.md` (H-23)

**Blind-protocol note:** This execution did not read any other file under `adversary/` in this project per the blind-review mandate. All findings below are independently derived from the two deliverables, `subtraction-pass-notes.md` (explicitly permitted), `FEEDBACK-LOG.md`, `.github/workflows/ci.yml`, and Glob checks against the live repo tree.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verdict and finding counts |
| [Explicitly-Requested Checks](#explicitly-requested-checks) | The five checks named in the invoking task |
| [Findings Summary](#findings-summary) | Table of Critical/Major/Minor findings |
| [Detailed Findings](#detailed-findings) | Full evidence, analysis, remediation per finding |
| [Compliant Principles (Evidence)](#compliant-principles-evidence) | Verified-compliant items, for balance (P-022) |
| [Remediation Plan](#remediation-plan) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Constitutional Compliance Score](#constitutional-compliance-score) | Step 5 calculation |

---

## Summary

**PARTIAL compliance.** 1 Critical, 1 Major, 1 Minor. The Critical finding is a direct, same-document self-contradiction that survived the iteration-6 "overclaim-correction, no new machinery" pass: the retained lint rule **L-7** is described as catching "the `ADR-PROJ007-001/002` failure class" in the very same Enforcement Design section that, three lines later, discloses (as residual R-B) that this exact failure class is **not** covered by the 5-rule core. Independently verified against the live repo (no `ADR-PROJ007-*` file exists anywhere) that this claim is not merely imprecise but structurally impossible for L-7 to satisfy. **Score: 0.83 (REJECTED band, H-13).** Recommend targeted revision (CC-001 is a small, surgical text fix, not new machinery — consistent with the subtraction doctrine already in force).

---

## Explicitly-Requested Checks

The invoking task named five specific checks. Disposition of each:

| # | Check | Disposition | Evidence |
|---|-------|-------------|----------|
| 1 | MEDIUM-tier purity — zero HARD vocabulary in the rule draft | **COMPLIANT** | Grepped `design/adr-standards-rule-draft.md` for `\bMUST\b\|\bSHALL\b\|\bNEVER\b\|\bFORBIDDEN\b\|\bREQUIRED\b\|\bCRITICAL\b` — zero matches. Lowercase "must" occurrences (lines 169, 174, 175) are explicitly scoped by an in-document CC-001 note (line 169) as "the lint's own pass/fail trigger condition (tool mechanics), not a HARD author obligation." HARD ceiling 25/25 unaffected — no new `H-NNN` rule is introduced anywhere in either deliverable. |
| 2 | H-23 nav tables | **COMPLIANT** | Both files carry a `## Document Sections`/`## Navigation` table. Verified every `##` heading in both files (via Grep) has a corresponding nav-table row with a correctly GFM-slugified anchor link, spot-checked on the harder cases (`Options Considered (A–F)` → `#options-considered-af`; `Rationale — Answering the Crux Head-On` → `#rationale--answering-the-crux-head-on`; `Pre-Mortem and Failure Modes (S-004 / S-012)` → `#pre-mortem-and-failure-modes-s-004--s-012`). No missing or dangling anchors found in either file's own nav table. |
| 3 | P-022 claim honesty — no enforcement overclaims after the slim-down | **VIOLATED (Critical, CC-001)** | See [Detailed Findings](#detailed-findings). One overclaim of exactly this class survived: L-7's description names the historical PROJ-007 failure it is claimed to catch, while the adjacent R-B disclosure (same section, 3 lines later) says the opposite. |
| 4 | Ratification recorded per P-020 | **COMPLIANT** | `FEEDBACK-LOG.md:26-37` (FU.0) independently read and verified: the quoted ratification — *"I ratify the promotion-is-the-point apporach and lock Scheme B."* — matches verbatim (typo included) what both deliverables cite at `ADR-PROJ031-004...md:85` and `subtraction-pass-notes.md:39`. Disposition marked `DONE`. This is a genuine, cross-verified citation, not a fabricated one. |
| 5 | L1 token-budget fit (~12,500-token total L1 budget) | **COMPLIANT (honestly qualified)** | `adr-standards-rule-draft.md:196` discloses: "`.context/rules/*.md` already measures ~26.9k words (~36k tokens), so the SSOT's ~12,500-token L1 figure is a curated/re-injected subset, not a raw corpus sum; this file's ~3.9k tokens (238 lines) is comparable to other substantive rule files and a bounded add." This is an honest reconciliation of a real tension in the framework's own SSOT figure (not fabricated), rather than a claim that the new file trivially "fits" an unqualified 12,500-token ceiling. Treated as compliant disclosure, not overclaim. |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CC-001-20260706iter7 | Critical | L-7 lint rule claims to catch the "ADR-PROJ007-001/002 failure class" while the same section's R-B disclosure says the identical failure class is NOT covered — self-contradiction, independently verified as factually impossible for L-7 to satisfy | ADR `## Enforcement Design (L5 CI Lint)`; rule draft `## L5 CI Lint Specification` |
| CC-002-20260706iter7 | Major | AE-004 (HARD-adjacent auto-escalation rule, unconditional in the SSOT) is narrowed by project-level ADR interpretation ("Path-1 metadata-only promotions do not trip AE-004's C4") without a corresponding SSOT amendment or explicit "pending harmonization" disclosure | ADR `## Promotion Process (Step-by-Step)`, AE-004 scoping paragraph |
| CC-003-20260706iter7 | Minor | ADR's own "ID grammar" technical section retains uppercase HARD-styled emphasis ("MUST begin with a LETTER") for content the companion rule draft deliberately expresses in lowercase with an explicit tool-mechanics disclaimer — vocabulary-tier hygiene inconsistency between the two co-published documents | ADR `## L1: Technical Implementation`, ID grammar block |

---

## Detailed Findings

### CC-001-20260706iter7: L-7 Overclaim Contradicts Its Own Adjacent Disclosure (R-B) — Independently Falsified Against the Live Repo [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR `## Enforcement Design (L5 CI Lint)` (lines 663, 666); rule draft `## L5 CI Lint Specification` (line 177) |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — P-022 (No Deception / No Overclaim) |

**Evidence (ADR, `ADR-PROJ031-004-adr-identifier-convention.md:663`):**

> "**L-7 Relationship target resolves** | `superseded_by`/`promoted_to`/`promoted_from` targets resolve to an existing ADR — catches a half-completed Path-2 orphaning the source (**the `ADR-PROJ007-001/002` failure class**). Existence only, not bidirectional/semantic correctness; `supersedes`/`amends`/`amended_by` are not checked — a disclosed 3-of-6 asymmetry (R-11, FM-003/RT-103). Repo-wide."

**Evidence (same file, 3 lines later, `:666`):**

> "**Descoped, honestly (not phased, not committed).** ... **repo-wide free-text citation scanning** (incl. GitHub-Issue citations, full-path citations, non-markdown config) ... The citation-scan omission is an **[INHERENT] residual (R-B)** — the core detects only structural frontmatter links (L-7); it does **not** catch stale full-path citations (~28% of `.context/rules/` citations), stale GitHub-Issue references (the FM-006 surface), or an in-place amendment mutation."

**Evidence (companion rule draft, `adr-standards-rule-draft.md:177`, same claim in softer form):**

> "**L-7 Relationship target resolves** | ... catches a half-completed Path-2 orphaning the source (**the historically-demonstrated failure side**). Existence only, not bidirectional/semantic correctness ..."

**Evidence the historical failure is a free-text/non-ADR-file citation problem, not a structural-frontmatter one (ADR `## Context`, lines 73, 111, 113):**

> ":73 — 'all three framework ADRs were born inside projects and renamed on promotion; the resulting broken citations remain unrepaired months later (verified for the PROJ-007 pair...)'"
> ":113 — 'stale citations to the extinct `ADR-PROJ007-001/002` IDs still sit in PROJ-007's own `ORCHESTRATION.yaml:228,242`, `WORKTRACKER.md:106-107`, and `EN-001.md:48-49,72-73` as of 2026-07-02.'"

**Independent verification (this execution, not asserted by the deliverable itself):**

- `Glob("**/ADR-PROJ007*")` → **no files found** anywhere in the repository. There is no surviving `ADR-PROJ007-001` or `-002` file at any path carrying a `promoted_to`/`superseded_by` frontmatter field for L-7 to inspect — the old dialect files were renamed away entirely (git-mv'd out of existence under the old ID) rather than left as tombstone stubs.
- `Glob("**/ADR-agent-design*")` → only `docs/design/ADR-agent-design-001.md` exists (the new canonical file).

**Analysis:** L-7 is defined to check that relationship fields (`superseded_by`, `promoted_to`, `promoted_from`) **present on existing ADR files** resolve to a real target. Because no `ADR-PROJ007-001/002` file survives under its old name (confirmed by Glob), there is no relationship field anywhere for L-7 to check in this exact historical case — the failure lived entirely in three **non-ADR** files (`ORCHESTRATION.yaml`, `WORKTRACKER.md`, `EN-001.md`) that L-7 does not scan at all (L-7 is scoped to ADR-to-ADR structural links). The document's own R-B disclosure says precisely this ("the core detects only structural frontmatter links (L-7); it does not catch stale full-path citations"), yet the L-7 rule-row three lines earlier in the identical section names "the `ADR-PROJ007-001/002` failure class" as what it catches. This is not a subtle interpretive gap; it is a factual claim directly falsified by (a) the document's own adjacent disclosure and (b) an independent Glob check of the live repository. The class of defect (an enforcement mechanism over-attributed to a founding failure mode it structurally cannot detect) is the *exact* defect the subtraction pass already fixed once for a sibling rule — the disposition table in `subtraction-pass-notes.md:87` (RT-001) records: "The overstated 'fail-closed L-8 catches the founding failure mode' claim is removed: L-8 is descoped from the 5-rule core." That fix removed the overclaim from L-8 (which was deleted) but left an equivalent overclaim standing on L-7 (which was retained through every iteration). Given P-022 is named explicitly in this iteration's own mandate ("no enforcement overclaims after the slim-down") and constitutes a HARD-tier principle (H-03: no deception about capabilities), this is classified **Critical**.

**Affected Dimension:** Internal Consistency (primary — the claim directly contradicts an adjacent disclosure in the same section); Evidence Quality (secondary — the claim is unsupported and independently falsifiable).

**Remediation:** Delete or reword the parenthetical at ADR `:663` ("the `ADR-PROJ007-001/002` failure class") and rule draft `:177` ("the historically-demonstrated failure side") to state only what L-7 actually catches: a **future** structural orphaning where a relationship field is populated but its target ID no longer resolves to a file (a narrower, forward-looking scenario, not the PROJ-007 precedent, which required free-text citation scanning that was descoped). This is a text-only fix consistent with subtraction doctrine — no new machinery required.

---

### CC-002-20260706iter7: AE-004 (Auto-Escalation Rule) Narrowed by Project-Level ADR Without SSOT Amendment [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR `## Promotion Process (Step-by-Step)`, "AE-004 scoping of a promotion" paragraph (~line 552-558) |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — Auto-Escalation Rules (quality-enforcement.md) |

**Evidence (SSOT, `quality-enforcement.md` Auto-Escalation Rules table, loaded context):**

> "AE-004 | Modifies baselined ADR | Auto-C4"

No qualifier, carve-out, or "metadata-only" exception appears in the SSOT text.

**Evidence (ADR body):**

> "**Path 1 (metadata-only) → C3 floor.** A Path-1 promotion changes only **location** (`git mv`) and the **`scope` field** (`project → framework`); the **decision body is immutable**. A metadata+location transition that does not alter decision content is a *governed lifecycle move* at the **C3** floor — it does **not** trip AE-004's C4, because AE-004 targets changes to a baselined ADR's *decision content*, not its lifecycle metadata."

**Analysis:** AE-004 is presented in quality-enforcement.md (the SSOT this framework treats as authoritative for auto-escalation) as an unconditional rule: any modification to a baselined ADR auto-escalates to C4. This project-level ADR introduces a substantive narrowing — "metadata-only Path-1 promotions do not trip AE-004" — and states it with the same confidence as settled fact ("This keeps the cheap, frequent operation... at C3 while preserving AE-004's teeth"), without flagging that this is the ADR's own interpretive gloss rather than a confirmed SSOT reading, and without proposing or executing a corresponding SSOT text amendment (e.g., adding the carve-out to quality-enforcement.md's AE-004 row) or an ADR that would formally interpret/amend AE-004's scope. A HARD-adjacent auto-escalation rule's applicability boundary is being set by a MEDIUM-tier project convention rather than by the SSOT it purports to interpret. This is not (yet) an active harm — the document itself discloses elsewhere (Promotion Process, Path 1 section) that "zero Path-1 promotions have actually occurred" — but if a future Path-1 promotion relies on this reading to justify processing at C3 instead of C4, and the SSOT is never updated to reflect it, the classification could be successfully challenged as ultra vires (a project ADR cannot narrow a framework auto-escalation rule's scope on its own authority). This is a governance-hygiene gap in Methodological Rigor / Internal Consistency, not a fabrication — no severity inflation intended, hence Major rather than Critical.

**Affected Dimension:** Methodological Rigor (primary); Internal Consistency (secondary, ADR text vs. SSOT text).

**Remediation:** Either (a) file a companion SSOT clarification (even a one-line amendment to quality-enforcement.md's AE-004 row, e.g., "metadata-only lifecycle moves — see ADR-adr-convention-001 Promotion Path 1 — are excluded"), or (b) add an explicit disclosure in the ADR that this AE-004 scoping is the ADR's own interpretation, not a confirmed SSOT reading, pending harmonization at the first real Path-1 promotion (the document already tracks that promotion as a named future milestone — this is a natural place to also land the SSOT harmonization).

---

### CC-003-20260706iter7: Vocabulary-Tier Hygiene Inconsistency Between Companion Documents [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR `## L1: Technical Implementation`, ID grammar block, line 314 |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — Tier Vocabulary (quality-enforcement.md) |

**Evidence (ADR, line 314):**

> "(SM-101, iter-3: the FIRST token MUST begin with a LETTER, not a digit. An all-numeric leading token like `150` is deliberately excluded so that a GH-issue/bare-number ID such as `ADR-150-001` is NOT admitted as a 'domain slug'...)"

**Evidence (companion rule draft, equivalent content, line 169, deliberately lowercase and disclaimed):**

> "**Reading the 'must' in the rules below (CC-001 scoping).** Where a rule row says a file 'must'/'must not' match a pattern, that is the **lint's own pass/fail trigger condition** (tool mechanics), not a HARD author obligation — the author-facing tier stays MEDIUM (SHOULD, override-with-justification)."

**Analysis:** The rule draft's own iteration-6 remediation (changelog `:236`, "lowercase 'never' ... → SHOULD-NOT (CC-001); L5 preamble scopes mechanism 'must'") deliberately downgraded HARD-styled emphasis for grammar/mechanism descriptions and added an explicit disclaimer distinguishing tool-mechanics language from author-facing obligations. The ADR's own parallel technical section, describing the identical substantive rule (the domain-slug's leading token must be a letter, not a digit), was not brought into the same style, retaining uppercase "MUST" and "NOT" without an equivalent disclaimer. This does not change the underlying MEDIUM-tier convention (the rule draft — the file that will actually be installed to `.context/rules/` and is subject to H-23/Tier Vocabulary discipline — is clean, verified above), and a reasonable reading treats this ADR passage as tool-mechanics description exactly like the rule draft's disclaimed usage. It is flagged as Minor because the asymmetry is exactly the class of residual the doc's own remediation discipline elsewhere catches and fixes (e.g., CC-001 in iteration 6), so leaving one instance unharmonized is a completeness gap, not a substantive tier violation.

**Affected Dimension:** Internal Consistency.

**Remediation:** Either lowercase "must"/"not" at line 314 to match the rule draft's convention, or add a one-clause disclaimer parallel to the rule draft's CC-001 note (e.g., "(regex/tool-mechanics description, not an author-facing HARD obligation — see rule draft CC-001 note)").

---

## Compliant Principles (Evidence)

Documented per Step 3 "COMPLIANT" classification, for balance (P-022 requires findings not be one-sided):

| Principle / Check | Status | Evidence |
|---|---|---|
| P-020 (User Authority — ratification) | COMPLIANT | `FEEDBACK-LOG.md:26-37` FU.0 verbatim quote matches both deliverables' citations exactly, independently re-read by this reviewer. |
| Tier Vocabulary (HARD-keyword purity, rule draft) | COMPLIANT | Zero-match grep for the 6 canonical HARD-tier keywords in `adr-standards-rule-draft.md`. |
| H-23 (Navigation tables + anchor links) | COMPLIANT | Both files' nav tables verified 1:1 against their own `##` heading lists via Grep; anchors spot-checked against GFM slug rules including punctuation-heavy headings. |
| HARD Rule Ceiling (25/25) | COMPLIANT | Neither deliverable introduces a new `H-NNN` rule; both explicitly state "No HARD rule added." |
| P-004 (Provenance) — dangling `ADR-CI-001` citation claim | COMPLIANT | Read `.github/workflows/ci.yml:2` directly: confirms the cited path `projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`. `Glob("projects/PROJ-001*")` confirms that project directory no longer exists — the ADR's "dangling citation" claim is independently verified accurate. |
| Grandfather-corpus arithmetic (16/15/18/14 reconciliation) | COMPLIANT | Cross-checked D-4's "16 dialect ADRs (15 pre-existing + this ADR)" against the Enforcement Design's "18 reachable (15 dialect in `decisions/` + 3 canonical)" and M-14's "14 = 15 minus the out-of-scan STORY015 entity-embedded ADR" — all three counts are internally consistent with each other once STORY015's out-of-scan status is applied uniformly. |
| c-007 self-compliance (ADR's own identity/remap path) | COMPLIANT | Meta-Note section explicitly states the ADR's current filename is the discouraged dialect, declares the canonical target (`ADR-adr-convention-001`), and states the remap path — satisfying c-007 by disclosure rather than by actually complying with the scheme (which the ADR itself acknowledges via P-020: "I have not moved or renamed the file"). |

---

## Remediation Plan

**P0 (Critical):** CC-001 — Reword the L-7 rule-row parenthetical in both the ADR (`:663`) and the rule draft (`:177`) to remove the false attribution to the PROJ-007 failure class; state only the narrower, actually-true claim (catches a *future* structural dangling relationship field, not the historically-demonstrated free-text citation failure, which remains R-B/descoped). Text-only fix; no new machinery, consistent with subtraction doctrine.

**P1 (Major):** CC-002 — Add an explicit "this is the ADR's own interpretation, pending SSOT harmonization" disclosure to the AE-004 scoping paragraph, or file a one-line SSOT clarification alongside quality-enforcement.md's AE-004 row.

**P2 (Minor):** CC-003 — Harmonize line 314's capitalization/disclaimer to match the rule draft's CC-001 tool-mechanics framing.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No constitutional findings affect completeness; both files cover their declared scope. |
| Internal Consistency | 0.20 | Negative | CC-001 (Critical): direct same-section self-contradiction (L-7 claim vs. R-B disclosure). CC-002 (Major): ADR text vs. SSOT text. CC-003 (Minor): vocabulary-tier asymmetry between companion docs. |
| Methodological Rigor | 0.20 | Negative | CC-002 (Major): unilateral narrowing of a framework auto-escalation rule without SSOT amendment process. |
| Evidence Quality | 0.15 | Negative | CC-001 (Critical): the overclaim is independently falsifiable against the live repo (no `ADR-PROJ007-*` file exists), which is precisely the kind of claim this deliverable otherwise takes great care to verify (Glob/grep-pinned) elsewhere. |
| Actionability | 0.15 | Positive | All three findings have concrete, surgical, non-machinery remediations consistent with the subtraction doctrine already governing this package. |
| Traceability | 0.10 | Neutral | Findings and remediations cite exact file+line locations; no traceability gap introduced. |

---

## Constitutional Compliance Score

Per Execution Protocol Step 5:

- N_critical = 1, N_major = 1, N_minor = 1
- Penalty = 0.10(1) + 0.05(1) + 0.02(1) = 0.17
- Score = 1.00 − 0.17 = **0.83**
- Threshold: < 0.85 → **REJECTED** (H-13 applies; revision required)

**Note on severity proportionality:** the single Critical finding (CC-001) is a small, surgical text correction (reword one parenthetical in two files), not a structural defect requiring new machinery. Its Critical classification reflects that it is a direct, independently-falsifiable, same-document self-contradiction on a P-022 (HARD-tier, H-03) claim-honesty axis — exactly the axis this iteration's mandate ("no enforcement overclaims after the slim-down") was scoped to close — not a judgment that the underlying convention design is unsound. The convention itself (Scheme B, the 5-rule core, the MEDIUM-tier posture) is assessed elsewhere in this tournament by other strategies; this report is scoped to constitutional/principle compliance only.

---

## Execution Statistics

- **Total Findings:** 3
- **Critical:** 1
- **Major:** 1
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5

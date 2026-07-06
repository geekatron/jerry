# FMEA Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + adr-standards-rule-draft.md)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (AE-002 rules-dir + AE-003 new-ADR auto-escalation; engagement gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-012, blind independent iteration 1)
**H-16 Compliance:** Not independently verified by this agent (blind protocol forbids reading sibling S-003 output); per template Prerequisites this strategy assumes S-003 ran earlier in the C3+/C4 sequence.
**Elements Analyzed:** 15 | **Failure Modes Identified:** 23 | **Total RPN:** 4,953

**STATUS:** COMPLETE — all sections below finalized. (This file was written incrementally per P-002 during execution.)

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Element Inventory (Step 1)](#element-inventory-step-1) | MECE decomposition of the convention lifecycle |
| [Findings Table (Step 2-3)](#findings-table-step-2-3) | All 23 failure modes with S/O/D/RPN |
| [Finding Details](#finding-details) | Expanded detail for every Critical/Major finding |
| [Recommendations (Step 4)](#recommendations-step-4) | Prioritized corrective actions |
| [Scoring Impact (Step 5)](#scoring-impact-step-5) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts and completion confirmation |

---

## Summary

Systematic decomposition of the ADR convention's 15 lifecycle elements (creation/ID grammar, provenance metadata, location, cross-referencing, amendment, superseding, both promotion paths, lint enforcement, template/skill drift-fix specs, new-project onboarding, status vocabulary, DEC-NNN boundary, and the ADR's own self-compliance) surfaced 23 failure modes, 11 rated Critical (RPN >= 200 per the template's mechanical threshold), 10 Major, 2 Minor. The single highest-RPN finding (FM-001-20260702T1, RPN 504) is a verified, reproducible regex defect: the proposed L-1 lint regex (`^ADR-[a-z0-9]+...`) requires lowercase characters, but every one of the 11 already-existing, explicitly-grandfathered project/entity-scoped dialect ADRs uses an **uppercase** scope token (`ADR-PROJ031-001`, `ADR-EPIC002-001`) — meaning the lint, implemented exactly as specified, would reject the entire legacy corpus it is designed to grandfather, directly contradicting D-4's "no big-bang renumber" guarantee. Two further Critical findings independently corroborate that the ADR's central "promotion is citation-free" claim is not fully supported by live repo evidence: a real, currently-dangling ADR citation embedded in `.github/workflows/ci.yml:2` (a 9th ID family never captured by the cited research corpus) proves prose/path-based citation rot already exists outside any lint's detection surface, and the Promotion Path 1 "no citation re-pointing is required" claim is falsified by that same evidence of full-path (not bare-ID) citation practice already in use in this repository. **Recommendation: REVISE.** The core directional Decision (subject-encoded identity, Scheme B) is not undermined by these findings, but the enforcement/implementation companion draft (Deliverable 2, the proposed rule file) requires targeted correction before the lint spec (M-6, marked "gating") can be implemented as written — implementing it today would break CI for the entire legacy corpus on first run.

---

## Element Inventory (Step 1)

MECE decomposition of the convention's lifecycle into 15 elements, per the invoking task's explicit lifecycle stages (creation, cross-referencing, amendment, superseding, promotion, lint enforcement, template drift, new-project onboarding) plus supporting structural elements needed for full coverage.

| Element ID | Element | Deliverable Section(s) |
|---|---|---|
| E-01 | ID grammar & regex specification (canonical + dialect) | ADR §L1 Technical Implementation; rule-draft §ID Scheme |
| E-02 | Frontmatter / provenance schema | ADR §L1 (Frontmatter); rule-draft §Frontmatter Schema |
| E-03 | Canonical location model | ADR §L1 (Canonical location model); rule-draft §Canonical Location Model |
| E-04 | Cross-referencing & discoverability (citations, index) | ADR §Context, §Consequences; rule-draft §L5 CI Lint (L-6/L-7) |
| E-05 | Amendment mechanism | ADR §Amend vs Supersede; rule-draft §Supersede and Amend, ADR-M-009 |
| E-06 | Superseding mechanism | ADR §Amend vs Supersede; rule-draft §Supersede and Amend |
| E-07 | Promotion Path 1 (canonical, pure `git mv`) | ADR §Promotion Process Path 1; rule-draft §Promotion Process Path 1 |
| E-08 | Promotion Path 2 (dialect, rename + tombstone) | ADR §Promotion Process Path 2; rule-draft §Promotion Process Path 2 |
| E-09 | L5 CI lint enforcement & adoption gating (M-6) | ADR §Enforcement Design, §Migration Plan; rule-draft §L5 CI Lint Specification |
| E-10 | ADR template fix specification (`docs/knowledge/exemplars/templates/adr.md`) | rule-draft §Template and SKILL Fix Specifications, Fix 1 |
| E-11 | SKILL.md fix specification (`skills/architecture/SKILL.md`) | rule-draft §Template and SKILL Fix Specifications, Fix 2 |
| E-12 | New-project onboarding & slug arbitration | ADR §L2 Architectural Implications; rule-draft (TBR-2 references) |
| E-13 | Status vocabulary & lifecycle transitions | ADR §Status Vocabulary; rule-draft §Status Vocabulary |
| E-14 | Relationship to worktracker `DEC-NNN` (non-conflation) | ADR §Relationship to Worktracker DEC-NNN; rule-draft §Relationship to Worktracker DEC-NNN |
| E-15 | This ADR's own identity / self-compliance meta-note | ADR §Meta-Note: This ADR's Own Identity and Remap Path |

**MECE check:** 15 elements cover every lifecycle stage named in the task mandate (creation=E-01/E-02/E-03, cross-referencing=E-04, amendment=E-05, superseding=E-06, promotion=E-07/E-08, lint enforcement=E-09, template drift=E-10/E-11, new-project onboarding=E-12) plus 4 supporting elements (E-13, E-14, E-15, and E-09's gating-process dimension) required for full coverage of the two-document deliverable package. No element overlaps another's primary failure surface (verified during Step 2 enumeration).

---

## Findings Table (Step 2-3)

RPN Severity classification per template: **Critical** = RPN >= 200 OR S >= 9. **Major** = RPN 80-199 OR S 7-8. **Minor** = RPN < 80 AND S <= 6.

| ID | Element | Failure Mode (lens) | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|----------------------|---|---|---|-----|----------|---------------------|
| FM-001-20260702T1 | E-01 | **Incorrect.** L-1 regex `^ADR-[a-z0-9]+...` requires lowercase; all 11 grandfathered dialect ADRs use uppercase scope tokens (`ADR-PROJ031-*`, `ADR-EPIC002-*`) and are outside the Frozen-dir allowlist (`docs/adrs/`, `docs/archive/` only) | 9 | 8 | 7 | 504 | Critical | Methodological Rigor |
| FM-002-20260702T1 | E-01 | **Ambiguous.** Canonical and dialect ID forms share one regex; L-1 alone cannot distinguish recommended vs. discouraged grammar | 5 | 4 | 6 | 120 | Major | Internal Consistency |
| FM-003-20260702T1 | E-02 | **Inconsistent.** Proposed YAML frontmatter schema matches none of the 3 "already-canonical" exemplar ADRs' actual metadata (2 use HTML comments, 1 uses a blockquote with a `Parent:` key, none use YAML or `origin_project:`) | 6 | 8 | 6 | 288 | Critical | Evidence Quality |
| FM-004-20260702T1 | E-02 | **Insufficient.** `scope:` frontmatter is never validated against actual file location by a FAIL rule; only L-5 (WARN) checks framework-scope stranding | 5 | 6 | 6 | 180 | Major | Internal Consistency |
| FM-005-20260702T1 | E-03 | **Missing.** No documented procedure for draft ADRs authored under `orchestration/*/explore/` to graduate into a canonical `decisions/` home | 4 | 6 | 6 | 144 | Major | Completeness |
| FM-006-20260702T1 | E-03 | **Inconsistent.** Rule-draft's "Frozen Legacy" table heading contains a row (PROJ-014 bare ADRs) whose prescribed action is not a freeze, and the location is absent from the L-2/L-3 Frozen-dir allowlist | 4 | 5 | 7 | 140 | Major | Internal Consistency |
| FM-007-20260702T1 | E-04 | **Missing.** A 9th live ADR ID family (`ADR-CI-NNN`) exists in `.github/workflows/ci.yml:2`, uncatalogued by the cited research corpus, citing a project path (`PROJ-001-plugin-cleanup`) that no longer exists | 7 | 7 | 9 | 441 | Critical | Completeness |
| FM-008-20260702T1 | E-04 | **Insufficient.** L-7 (tombstone integrity) checks only frontmatter `superseded_by`/`promoted_to` targets, not prose/path citations — yet the ADR's own evidence shows prose citations to `ADR-PROJ007-001/002` remain stale and unrepaired 2.5 months later | 7 | 8 | 8 | 448 | Critical | Traceability |
| FM-009-20260702T1 | E-05 | **Ambiguous.** In-body `AMENDED YYYY-MM-DD` block has no specified placement, ordering, or collision rule for same-day amendments; unchecked by any L-1..L-7 rule | 4 | 5 | 6 | 120 | Major | Methodological Rigor |
| FM-010-20260702T1 | E-05 | **Missing.** No rule prevents an "amendment" from silently changing `scope`/location fields, creating a governance loophole that bypasses the formal Promotion Process's citation/tombstone safeguards | 6 | 5 | 7 | 210 | Critical | Internal Consistency |
| FM-011-20260702T1 | E-06 | **Insufficient.** Combined dialect-to-canonical supersession-plus-promotion case is under-specified: no tie-break rule for which mechanism (amend/supersede/promote) governs a simultaneous namespace change | 5 | 5 | 6 | 150 | Major | Methodological Rigor |
| FM-012-20260702T1 | E-06 | **Missing.** No cycle-detection rule; L-7 only verifies targets "resolve," not that the supersede graph is acyclic | 3 | 2 | 7 | 42 | Minor | Methodological Rigor |
| FM-013-20260702T1 | E-07 | **Insufficient.** "No citation re-pointing is required" (Path 1) is contradicted by demonstrated full-path citation practice in this repo (see FM-007 evidence); the claim holds only for bare-ID citations | 8 | 7 | 8 | 448 | Critical | Evidence Quality |
| FM-014-20260702T1 | E-08 | **Missing.** Path 2's `grep -rl` replace-with-new-ID instruction has no exclusion for historical/append-only records (CHANGELOGs, commit messages), risking rewritten history | 5 | 4 | 7 | 140 | Major | Actionability |
| FM-015-20260702T1 | E-09 | **Missing.** M-6 (lint implementation, marked "gating") has zero implementation as of the review date: no `scripts/lint_adr_convention.py` file and no ADR-lint step in any of the 6 `.github/workflows/*.yml` files; no owning worktracker/GH-issue tracks it | 7 | 8 | 5 | 280 | Critical | Actionability |
| FM-016-20260702T1 | E-10 | **Inconsistent.** Fix F1-a reuses the token `{SCOPE}` for what D-1 calls "domain-slug" (subject), directly contradicting the ADR's own central subject-vs-scope distinction | 6 | 6 | 7 | 252 | Critical | Internal Consistency |
| FM-017-20260702T1 | E-11 | **Insufficient.** SKILL.md Fix F2-a/F2-d retain `docs/design/` as the sole Output Location for architecture-agent-generated ADRs, contradicting ADR-M-007's project-first preference for the common case | 6 | 6 | 6 | 216 | Critical | Internal Consistency |
| FM-018-20260702T1 | E-12 | **Missing.** No pre-flight, author-runnable slug-collision check; collisions surface only post-hoc via CI (L-3), after merge | 5 | 7 | 6 | 210 | Critical | Actionability |
| FM-019-20260702T1 | E-12 | **Ambiguous.** "TBR-2" (domain-slug arbiter) is referenced twice across both documents but never defined, assigned, or tracked anywhere in the deliverable package | 4 | 8 | 4 | 128 | Major | Traceability |
| FM-020-20260702T1 | E-13 | **Missing.** Status vocabulary defines meanings but not permitted transitions (e.g., reversibility of `REJECTED`/`ACCEPTED`); no lint rule forbids invalid transitions | 3 | 5 | 6 | 90 | Major | Methodological Rigor |
| FM-021-20260702T1 | E-14 | **Inconsistent.** The "ADRs are the sole ontology exception" framing (invoked 3x) omits that `DEC-NNN` itself already uses a bare, non-parent-prefixed form at Enabler/Story level (`worktracker-directory-structure.md:80,88`), partially undercutting the contrast case | 5 | 6 | 7 | 210 | Critical | Evidence Quality |
| FM-022-20260702T1 | E-15 | **Insufficient.** The header pre-declares a canonical ID (`ADR-adr-convention-001`) as settled before Status: PROPOSED is ratified, with no contingency identity stated if a non-B scheme is ratified instead | 4 | 3 | 6 | 72 | Minor | Internal Consistency |
| FM-023-20260702T1 | E-15 | **Missing.** No Migration Plan action item commits to executing this ADR's own described Path-2 self-promotion; the "worked example" risks never being executed | 4 | 6 | 5 | 120 | Major | Actionability |

**Totals:** 23 findings | Critical: 11 | Major: 10 | Minor: 2 | Sum RPN: 4,953

---

## Finding Details

### FM-001-20260702T1: L-1 lint regex rejects the entire grandfathered legacy corpus (Critical, RPN 504)

**Element:** E-01 ID grammar & regex specification.
**Failure Mode:** Incorrect specification.
**Evidence:** `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:69` specifies the FAIL regex `^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$` (character class `[a-z0-9]` — lowercase letters and digits only), applied to `projects/*/decisions/` and `docs/design/` (`adr-standards-rule-draft.md:177`, L-1 row). Verified actual filenames in `projects/*/decisions/` use **uppercase** scope tokens: `ADR-PROJ031-001-skeleton-distribution-strategy.md`, `ADR-PROJ031-002-ci-token-push-strategy.md`, `ADR-PROJ031-003-credential-protection-supply-chain.md` (directory listing, `projects/PROJ-031-cowork-skeleton/decisions/`) and `ADR-EPIC002-001-strategy-selection.md`, `ADR-EPIC002-002-enforcement-architecture.md` (`projects/PROJ-001-oss-release/decisions/`). The Frozen-dir allowlist that exempts L-1/L-2/L-3 explicitly lists only `docs/adrs/`, `docs/archive/` (`adr-standards-rule-draft.md:185`) — `projects/*/decisions/`, where every uppercase-scoped dialect ADR lives, is **not** exempt.
**Effect:** D-4 and ADR-M-012 both state existing scope-prefixed ADRs "SHOULD be grandfathered in place" and "SHOULD NOT be renumbered." If M-6 (lint implementation, marked gating in the Migration Plan) is implemented by transcribing the regex as literally specified, CI would fail on every one of the 11 existing dialect ADRs the first time L-1 runs against the full corpus (not just newly-added files, since L-1 is a corpus-wide FAIL check, unlike L-2 which is diff-scoped to git-added files). This directly breaks the "no big-bang" migration guarantee the whole adoption plan is built on.
**S/O/D rationale:** S=9 (breaks a load-bearing adoption guarantee for the entire legacy corpus, not a cosmetic defect). O=8 (deterministic string-class mismatch — not a probabilistic risk, it will occur on first real run against the corpus as specified). D=7 (not caught by reading the spec in isolation; only surfaces when the regex is actually tested against real filenames, which neither deliverable document does).
**Corrective Action:** Change the regex's scope-token character class to `[A-Za-z0-9]` (or split L-1 into two explicit alternatives — canonical lowercase-only, dialect case-insensitive) and add a regression test asserting all 11 existing dialect filenames pass before M-6 is marked complete.
**Acceptance Criteria:** Updated L-1 regex verified against all 11 existing `projects/*/decisions/` dialect filenames with zero false rejections, prior to CI wiring.
**Post-Correction RPN estimate:** ~40 (S=2 after fix, O=2, D=10 residual documentation gap until the regression test is actually added to CI).

---

### FM-002-20260702T1: Canonical vs. dialect grammar not lint-distinguishable (Major, RPN 120)

**Element:** E-01. **Failure Mode:** Ambiguous.
**Evidence:** `adr-standards-rule-draft.md:69` states "Regex (canonical + dialect, for lint L-1)" — a single shared pattern for both the RECOMMENDED canonical form and the discouraged dialect form. L-4 (`adr-standards-rule-draft.md:180`) checks dialect-to-location consistency only for ADRs already identified as dialect; nothing in L-1..L-7 classifies an ADR as canonical vs. dialect independent of manual inspection.
**Effect:** A lint that cannot structurally distinguish "recommended" from "discouraged" forms cannot enforce ADR-M-001's SHOULD-preference at all — it can only catch malformed IDs, not discouraged-but-well-formed ones.
**S/O/D rationale:** S=5 (a design gap, not a blocking defect). O=4 (a lint author following the spec literally would notice the shared-regex framing but might not build a classifier). D=6 (requires cross-reading the ID Scheme section against the L-1 rule table to notice no classification exists).
**Corrective Action:** Add an explicit L-1b (WARN) rule: an ADR filename matching the dialect sub-pattern (`ADR-(PROJ|EPIC|STORY)\d{3}-NNN`) triggers an advisory "discouraged grammar; consider domain-slug" warning, independent of the FAIL-level form check.
**Acceptance Criteria:** Lint output distinguishes "malformed" (FAIL) from "well-formed but discouraged" (WARN) for every ADR.
**Post-Correction RPN estimate:** ~40.

---

### FM-003-20260702T1: Proposed frontmatter schema matches none of the 3 cited exemplar ADRs (Critical, RPN 288)

**Element:** E-02 Frontmatter / provenance schema. **Failure Mode:** Inconsistent.
**Evidence:** Proposed schema (`adr-standards-rule-draft.md:103-119`; ADR-PROJ031-004:275-291) specifies a `---`-delimited YAML block with keys `id`, `scope`, `origin_project`, `origin_entity`. Verified actual metadata of the 3 ADRs repeatedly cited as proof this "already works" (ADR-PROJ031-004:293, "The three existing framework ADRs already do this informally"): `docs/design/ADR-agent-design-001.md:3` uses an HTML comment `<!-- PS-ID: PROJ-007 | ENTRY: e-004 | AGENT: ps-architect-001 | DATE: 2026-02-21 -->` (no `scope`/`origin_project` keys); `docs/design/ADR-output-path-resolution-001.md:1-9` uses a blockquote block (`> **Type:** adr` ... `> **Parent:** EPIC-002` — a different key name, `Parent`, not `origin_project`, and no `scope:` field at all); `docs/design/ADR-routing-triggers-001.md:3` uses another HTML comment (`<!-- VERSION: 1.2.0 | DATE: ... | PS-ID: PROJ-007 | AGENT: ps-architect-002 | CRITICALITY: C4 ... -->`). None of the three files opens with `---` YAML frontmatter (line 1 in each is the `#` H1 title).
**Effect:** The Migration Plan (ADR-PROJ031-004, Migration Plan table row 1) characterizes bringing these 3 files into compliance as "Zero" cost ("add explicit `origin_project`/`scope` frontmatter if missing"). The actual cost is retrofitting 3 mutually-different informal metadata conventions into a wholly new YAML format — not adding a missing field to an existing one. This overstates readiness and could mislead an implementer following the Migration Plan literally.
**S/O/D rationale:** S=6 (undermines an evidentiary claim central to the Decision's credibility, though not the Decision's direction). O=8 (directly observable by opening the 3 cited files; not speculative). D=6 (a reader trusting the ADR's own "already does this informally" assertion would not independently verify).
**Corrective Action:** Correct the Migration Plan row's cost estimate from "Zero" to "Low — retrofit YAML frontmatter into 3 files currently using 3 different informal metadata styles"; add this as an explicit M-2/M-3-adjacent action item.
**Acceptance Criteria:** All 3 exemplar ADRs carry a parseable `---`-delimited YAML block with `origin_project` before M-6's L-6 rule is activated.
**Post-Correction RPN estimate:** ~60.

---

### FM-004-20260702T1: `scope:` field never validated against actual file location by a FAIL rule (Major, RPN 180)

**Element:** E-02. **Failure Mode:** Insufficient.
**Evidence:** `adr-standards-rule-draft.md:181`, L-5 "Framework home" is **WARN**, not FAIL: "An `ACCEPTED` + `scope: framework` ADR should live under `docs/design/`." No FAIL-class rule cross-checks `scope:` against the containing directory.
**Effect:** An ADR's frontmatter `scope` can silently diverge from its physical location indefinitely (advisory-only), meaning the very field meant to carry the "mutable, current governing scope" the whole Decision hinges on (D-1/D-2 rationale) has no hard guarantee of staying truthful.
**S/O/D rationale:** S=5, O=6 (WARN-only rules are routinely ignored in practice per the framework's own tier vocabulary — MEDIUM-tier violations are override-with-justification, i.e., expected to occur), D=6.
**Corrective Action:** Promote L-5 to FAIL for the specific case of `status: ACCEPTED` ADRs (leave PROPOSED/other statuses as WARN, since drafts may not have settled scope).
**Acceptance Criteria:** No `ACCEPTED` ADR with mismatched `scope`/location passes CI.
**Post-Correction RPN estimate:** ~50.

---

### FM-005-20260702T1: No documented graduation path from orchestration drafts to canonical `decisions/` (Major, RPN 144)

**Element:** E-03 Canonical location model. **Failure Mode:** Missing.
**Evidence:** The Canonical Location Model table (`adr-standards-rule-draft.md:74-86`; ADR-PROJ031-004:295-307) lists "Orchestration drafts" (`projects/*/orchestration/.../`) as "Transient (non-canonical until moved into a `decisions/` home)" but the Promotion Process section (both documents) only describes project-scope-to-framework-scope transitions (Path 1/Path 2), never draft-to-project-canonical transitions. A concrete instance of such an undocumented draft artifact already exists in this very engagement: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/explore/trade-study.md` (path verified via directory listing; not itself named `ADR-*`, and its lifecycle into a `decisions/`-homed ADR is exactly the gap described).
**Effect:** Authors have no documented procedure — no ID-assignment rule, no citation-safety guarantee — for the very common step of turning exploratory drafts into a first canonical ADR.
**S/O/D rationale:** S=4, O=6 (every new ADR effectively starts as some form of draft), D=6.
**Corrective Action:** Add a "Path 0 — Draft to first canonical home" step to the Promotion Process section, specifying ID assignment timing (at draft creation vs. at canonicalization) and confirming no citation risk exists because drafts are non-canonical by definition.
**Acceptance Criteria:** Promotion Process section documents Path 0 explicitly.
**Post-Correction RPN estimate:** ~50.

---

### FM-006-20260702T1: "Frozen Legacy" table contains a non-frozen row, and the location is outside the actual allowlist (Major, RPN 140)

**Element:** E-03. **Failure Mode:** Inconsistent.
**Evidence:** `adr-standards-rule-draft.md` §Frozen Legacy (row 4, PROJ-014) prescribes "Rename to a slug (or PROJ014 dialect) only if promoted" for bare `ADR-001..004` at `projects/PROJ-014-*/orchestration/.../phase-5/` — an actionable, non-frozen disposition, sitting inside a table titled "Frozen Legacy" whose other 3 rows all say "Freeze"/"Freeze; add banner". Separately, the L-2/L-3 Frozen-dir allowlist (`adr-standards-rule-draft.md:185`) names only `docs/adrs/`, `docs/archive/` — `projects/PROJ-014-*/orchestration/...` is not on it, though the Transient exemption row separately covers `projects/*/orchestration/` (advisory only).
**Effect:** A reader relying on the "Frozen Legacy" heading alone could reasonably conclude PROJ-014's bare ADRs are exempt from all future lint scrutiny, when the table's own action column says otherwise.
**S/O/D rationale:** S=4, O=5, D=7 (heading/row mismatch is easy to skim past).
**Corrective Action:** Move the PROJ-014 row out of "Frozen Legacy" into a new "Transient, Actionable" table, or rename the PROJ-014 row's action column to explicitly cross-reference the Transient exemption clause.
**Acceptance Criteria:** No table row's disposition contradicts its section heading.
**Post-Correction RPN estimate:** ~40.

---

### FM-007-20260702T1: A 9th, uncatalogued ADR ID family with a dangling citation already exists in the live repo (Critical, RPN 441)

**Element:** E-04 Cross-referencing & discoverability. **Failure Mode:** Missing.
**Evidence:** `.github/workflows/ci.yml:2` contains the comment `# ADR: projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`. Verified: `projects/PROJ-001-plugin-cleanup/` does not exist in the current repository (empty glob result); the live PROJ-001 project is `projects/PROJ-001-oss-release/` (confirmed present, e.g. `ORCHESTRATION.yaml`, `WORKTRACKER.md`). The 8-family corpus catalog the ADR relies on for its "zoo of incompatible ID families" claim (`adr-convention-standards-research.md:57-68`, cited at ADR-PROJ031-004:65) does not include a subsystem-scoped family (`ADR-{SUBSYSTEM}-NNN`, e.g. `ADR-CI-001`) — this is a 9th family, undiscovered by the underlying research, and its cited target file does not exist (a fully dead citation, not merely stale).
**Effect:** (1) The corpus catalog the Context section relies on for MECE-completeness is demonstrably incomplete; (2) this citation is invisible to every proposed lint rule (L-1..L-7), all of which inspect only markdown filenames under `decisions/`/`docs/design/`, never comments inside `.yml`/code files — meaning this exact class of citation rot is permanently outside the enforcement design's detection surface, with no mitigation proposed anywhere in either document.
**S/O/D rationale:** S=7 (the standard's enforcement has zero coverage for an entire class of citation, and the research's completeness claim is materially wrong). O=7 (comment-embedded citations in CI/code files are a common pattern; one is already proven to exist and rot). D=9 (undetectable by any of the 7 proposed lint rules by design — requires exactly this kind of independent repo-wide grep to surface, which neither deliverable document performs).
**Corrective Action:** (a) Correct the research corpus catalog to acknowledge a 9th, subsystem-scoped family and audit for further non-markdown ADR citations repo-wide (`grep -rn "ADR-[A-Za-z]" --include=*.yml --include=*.yaml --include=*.py`); (b) fix or remove the dead `ci.yml:2` comment; (c) add an L-8 (WARN) rule scanning non-markdown files for `ADR-` token references and flagging any that do not resolve to an existing file.
**Acceptance Criteria:** `ci.yml:2` citation resolves or is removed; L-8 rule added to the lint spec covering non-markdown citation sites.
**Post-Correction RPN estimate:** ~80.

---

### FM-008-20260702T1: Tombstone/citation lint covers only frontmatter fields, not the prose citations the ADR's own evidence shows are broken (Critical, RPN 448)

**Element:** E-04. **Failure Mode:** Insufficient.
**Evidence:** L-7 "Tombstone integrity" (`adr-standards-rule-draft.md:183`) checks only that `superseded_by`/`promoted_to` frontmatter targets "resolve" and that "no live reference to a tombstoned ID survives" — but its mechanism is structured-field-only. ADR-PROJ031-004 itself documents (lines 236-238, Rationale §2 and Related Decisions) that prose/path citations to the extinct `ADR-PROJ007-001/002` IDs "still sit in PROJ-007's own `ORCHESTRATION.yaml:228,242`, `WORKTRACKER.md:106-107`, and `EN-001.md:48-49,72-73` as of 2026-07-02" — i.e., the ADR's own central evidentiary example of citation breakage is a **prose/YAML-value citation**, not a frontmatter `superseded_by` field, and would not be caught by L-7 as specified.
**Effect:** The enforcement design's flagship anti-breakage rule (L-7) does not cover the exact failure mode the ADR's own headline evidence describes, meaning ratifying this convention with the lint as specified would not have prevented, and will not detect, a repeat of the PROJ-007 citation-rot incident.
**S/O/D rationale:** S=7 (directly undermines the primary justification for the Decision — "promotion becomes citation-free" — since the enforcement can't verify or repair the exact failure class cited as proof of the problem). O=8 (already observed occurring and unrepaired for 2.5 months, per the ADR's own text). D=8 (the gap is subtle: L-7's WARN class implies "we handle citation staleness," but only for structured fields).
**Corrective Action:** Add an L-9 (WARN, repo-wide) rule that greps for all bare ADR ID strings across `.md`, `.yaml`, `.yml` files and flags occurrences of any ID marked `SUPERSEDED`/`promoted_to` in frontmatter, extending coverage to prose citations.
**Acceptance Criteria:** L-9 rule specified; the 6 already-known stale PROJ-007 citations are enumerated as a remediation backlog item (or fixed) concurrently with adoption.
**Post-Correction RPN estimate:** ~90.

---

### FM-009-20260702T1: In-body amendment block has no placement/ordering/collision rule (Major, RPN 120)

**Element:** E-05 Amendment mechanism. **Failure Mode:** Ambiguous.
**Evidence:** ADR-M-009 / `adr-standards-rule-draft.md:53,149-153` specify only the block's textual form (`**AMENDED YYYY-MM-DD:** ...`) with no rule for placement (top/bottom/inline), multiplicity (append vs. replace), or same-day collision handling. No L-1..L-7 rule inspects amendment-block content or position.
**Effect:** Two independent amenders on the same day, or an amender unsure where to place the block relative to prior amendments, have no guidance; nothing is lint-checked.
**S/O/D rationale:** S=4, O=5, D=6.
**Corrective Action:** Specify append-only ordering (newest amendment last, directly above the closing metadata block) and add an advisory L-10 checking for well-formed, chronologically ordered `AMENDED` blocks.
**Acceptance Criteria:** Placement/ordering rule stated in the rule file.
**Post-Correction RPN estimate:** ~35.

---

### FM-010-20260702T1: Amendment mechanism can be used to bypass the Promotion Process's citation/tombstone safeguards (Critical, RPN 210)

**Element:** E-05. **Failure Mode:** Missing.
**Evidence:** Neither document states that changing `scope`/`origin_project`/location fields is out-of-bounds for an in-body "amendment" — the Amend vs. Supersede table (ADR-PROJ031-004:436-442; rule-draft:147-151) contrasts "minor clarification" (amendment) against "decision reversal" (supersede) and "scope elevation" (promotion) as three named, distinct mechanisms, but nothing in either document, nor in the L-1..L-7 lint, forbids an author from using the lightweight amendment mechanism to flip `scope: project` -> `scope: framework` (or move the file) without triggering the Promotion Process's citation re-pointing and tombstone steps.
**Effect:** The Promotion Process's entire citation-safety design (Path 1's zero-churn guarantee, Path 2's tombstone/back-link requirement) can be silently circumvented by mislabeling a scope change as an "amendment," since amendments are the least-scrutinized of the three mechanisms (no lint coverage at all per FM-009).
**S/O/D rationale:** S=6 (a genuine governance loophole around the Decision's central safety mechanism), O=5 (requires an author to conflate mechanisms, plausible but not the default path), D=7 (not obvious without cross-reading Amend-vs-Supersede against Promotion Process for a gap, exactly the kind of omission FMEA is designed to surface).
**Corrective Action:** Add an explicit prohibition to ADR-M-009: "An amendment MUST NOT change `scope`, `origin_project`, or file location; such changes MUST go through the Promotion Process." Add a WARN lint rule detecting `scope` field diffs not accompanied by a `promoted_from`/`promoted_to` update.
**Acceptance Criteria:** Explicit prohibition text added; lint rule specified.
**Post-Correction RPN estimate:** ~60.

---

### FM-011-20260702T1: Combined dialect-to-canonical supersession + promotion case has no tie-break rule (Major, RPN 150)

**Element:** E-06 Superseding mechanism. **Failure Mode:** Insufficient.
**Evidence:** Amend vs. Supersede / Supersede-and-Amend tables treat "Decision reversal" and "Scope elevation" as separate rows with separate ID-handling rules, but neither document addresses the case where a dialect ADR is *simultaneously* reversed and promoted (i.e., the successor is both a new decision AND lives in a new domain-slug namespace with its own independent `NNN` sequence per ADR-M-005's "monotonic within its namespace" rule). No worked example or rule states which mechanism's ID-handling procedure takes precedence.
**Effect:** An author facing this (plausible, not exotic) combined case has no specified procedure, risking ad hoc, non-reproducible ID assignment.
**S/O/D rationale:** S=5, O=5, D=6.
**Corrective Action:** Add a worked example / explicit rule: "supersede-with-promotion" follows Promotion Path 2's rename procedure, then treats the new ADR's predecessor link as `supersedes` (not `promoted_from`, since the decision itself changed, not merely its scope).
**Acceptance Criteria:** Combined-case rule and example added.
**Post-Correction RPN estimate:** ~45.

---

### FM-013-20260702T1: "No citation re-pointing required" (Promotion Path 1) is contradicted by the repo's own full-path citation practice (Critical, RPN 448)

**Element:** E-07 Promotion Path 1. **Failure Mode:** Insufficient.
**Evidence:** ADR-PROJ031-004 §Promotion Process Path 1 step 4 states: "No citation re-pointing is required — the ID is unchanged, so every existing citation remains valid. This is the whole point." This claim is falsified by the repo's own demonstrated citation style: `.github/workflows/ci.yml:2` cites an ADR by **full relative path** (`projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`), not by bare ID (see FM-007 evidence). A `git mv` under Path 1 changes the file's path even though the bare ID string is unchanged; any citation written as a full path (as this repo is proven to already do at least once) breaks exactly like a renamed-ID citation would, contradicting the stated "whole point" of Path 1.
**Effect:** The single most load-bearing operational claim in the Decision — that canonical-form promotion is citation-free — is only true for citations that reference the bare ID string, not for citations (already proven to exist in this repo) that embed the full path. This does not change the Decision's directional merit (subject-encoded identity is still less citation-fragile than the alternatives) but it does mean the "zero citation churn" claim, as literally written, overstates the guarantee.
**S/O/D rationale:** S=8 (directly falsifies the Decision's single strongest, most-repeated operational claim). O=7 (path-based citation is demonstrably an existing practice in this very repo, not a hypothetical edge case). D=8 (the ADR asserts the opposite with high confidence and no caveat; only an independent repo-wide citation-style audit, as performed here, surfaces the gap).
**Corrective Action:** Add a caveat to Path 1: "Citation re-pointing is not required for **bare-ID** citations. Full-path citations (e.g., in CI configs, code comments) MUST still be updated on `git mv`; run `grep -rl '{old-relative-path}'` before deleting the old path." Add this to the Migration Plan and to Path 1's step list.
**Acceptance Criteria:** Path 1 documentation caveat added; a repo-wide audit for full-path ADR citations performed prior to the first canonical-form promotion.
**Post-Correction RPN estimate:** ~90.

---

### FM-014-20260702T1: Path 2's grep-and-replace citation fix risks rewriting historical records (Major, RPN 140)

**Element:** E-08 Promotion Path 2. **Failure Mode:** Missing.
**Evidence:** Path 2 step 5 (both documents) instructs: "Re-point citations: `grep -rl \"ADR-PROJ{NNN}-NNN\"` deterministically finds every citation site... replace with the new domain-slug ID." No exclusion is specified for append-only historical artifacts (CHANGELOG.md entries, commit messages, prior worktracker DEC-NNN entries documenting past state) where the old ID was historically and correctly accurate at the time it was written.
**Effect:** A literal, unscoped grep-replace risks silently rewriting historically-accurate records to reference an ID that did not exist at the time the record was created, corrupting the historical trail the framework otherwise values (P-004 provenance).
**S/O/D rationale:** S=5, O=4, D=7.
**Corrective Action:** Add an explicit exclusion list to Path 2 step 5: CHANGELOG.md, git history/commit messages, and any file explicitly documenting past-tense state are excluded from find-and-replace; only forward-looking/current-state references are re-pointed.
**Acceptance Criteria:** Exclusion list added to Path 2 step 5 in both documents.
**Post-Correction RPN estimate:** ~40.

---

### FM-015-20260702T1: Gating lint (M-6) has zero implementation and no committed owner/timeline as of the review date (Critical, RPN 280)

**Element:** E-09 L5 CI lint enforcement & adoption gating. **Failure Mode:** Missing.
**Evidence:** ADR-PROJ031-004's own Pre-Mortem FM-1 predicts as the top plausible 2026-12-31 failure narrative: "The L5 lint was never implemented; the convention stayed a suggestion." The Migration Plan marks M-6 ("Implement + wire the L5 CI lint... into CI") as **"Yes (gating)"**. Verified: no file matching `**/*lint_adr*` exists anywhere in the repository (repo-wide glob, zero results), and none of the 6 `.github/workflows/*.yml` files (`ci.yml`, `docs.yml`, `pat-monitor.yml`, `release.yml`, `security-scan.yml`, `version-bump.yml`) reference any ADR-related lint step (grep of `ci.yml` for "ADR|adr" found only the unrelated dead comment addressed in FM-007). No linked GitHub issue or worktracker TASK/STORY entity for M-6 is cited in either deliverable document.
**Effect:** D-5 states enforcement is "deterministic L5 CI lint... not a HARD invariant" — but as of this review, that enforcement mechanism does not exist in any form, meaning ratifying this ADR today produces a purely advisory convention, contradicting its own stated MEDIUM-tier-but-lint-enforced design, and leaving the ADR's own self-identified top risk (FM-1) with a currently-unmitigated, zero-progress status.
**S/O/D rationale:** S=7 (the enforcement premise is currently entirely unfulfilled — this is the difference between a lint-backed standard and an aspirational one). O=8 (the ADR's own authors independently rank this the most plausible failure mode, and zero progress toward it exists as of the same day this ADR was authored). D=5 (partially self-detected — the ADR names this risk itself — but no concrete mechanism, owner, or deadline commits it, so occurrence risk remains high despite the self-awareness).
**Corrective Action:** Before or concurrent with ratification, file a tracked worktracker TASK/STORY (and, per H-31 GitHub Issue parity if in the `geekatron/jerry` repo) for `scripts/lint_adr_convention.py` with an explicit owner and target date, and reference it by ID in the Migration Plan's M-6 row.
**Acceptance Criteria:** M-6 row cites a specific worktracker/GH-issue ID with an assigned owner and target date.
**Post-Correction RPN estimate:** ~120 (residual risk remains until the lint is actually merged, even after tracking exists).

---

### FM-016-20260702T1: Template Fix reuses the token `{SCOPE}` for "domain-slug," contradicting the ADR's own subject-vs-scope distinction (Critical, RPN 252)

**Element:** E-10 ADR template fix specification. **Failure Mode:** Inconsistent.
**Evidence:** `adr-standards-rule-draft.md:203` (Fix F1-a) proposes changing the template title placeholder to `# ADR-{SCOPE}-{NNN}: {Title}`, with `{SCOPE}` explicitly glossed as either "a **domain-slug** (RECOMMENDED)... or a project/entity ID (permitted dialect)." But the parent ADR's own Decision and Rationale sections build their entire argument on a strict terminological distinction between **subject** (what the domain-slug encodes, immutable) and **scope** (the mutable `scope: framework | project` frontmatter field, expressed by location) — e.g., ADR-PROJ031-004:209, "subject wins the identity, origin goes to frontmatter, and scope — the mutable thing — is expressed by *location*." Fix F1-a's placeholder token, `{SCOPE}`, is literally the word the Decision reserves for the mutable, location-expressed property, yet here it is used to mean the immutable subject/domain-slug.
**Effect:** A template author implementing Fix F1-a literally, without cross-referencing the Rationale section's vocabulary, would encode the exact conceptual conflation (mutable scope in the identifier) that this entire ADR exists to correct, into the primary reference template new ADR authors copy from.
**S/O/D rationale:** S=6 (a terminology defect in the deliverable's own implementation spec, propagating the precise confusion the Decision is designed to eliminate). O=6 (plausible a literal implementer transcribes the fix spec verbatim without re-deriving the Rationale's vocabulary). D=7 (only surfaces via close cross-section reading, exactly the kind of internal-consistency check FMEA performs).
**Corrective Action:** Rename the template placeholder token from `{SCOPE}` to `{DOMAIN-SLUG}` (or `{SUBJECT}`), reserving "scope" exclusively for the frontmatter `scope:` field per the Decision's own vocabulary.
**Acceptance Criteria:** Fix F1-a token renamed; no remaining use of "SCOPE" to mean "subject/domain-slug" anywhere in either document.
**Post-Correction RPN estimate:** ~50.

---

### FM-017-20260702T1: SKILL.md fix locks all architecture-agent ADR output to `docs/design/`, contradicting the project-first preference (Critical, RPN 216)

**Element:** E-11 SKILL.md fix specification. **Failure Mode:** Insufficient.
**Evidence:** `adr-standards-rule-draft.md:214,217` (Fix F2-a, F2-d) change `skills/architecture/SKILL.md`'s `decision`-agent Output Location and Quick Reference "Create an ADR" Output from `docs/design/ADR_NNN_*.md` to `docs/design/ADR-{domain-slug}-NNN-*.md` — retaining `docs/design/` as the sole, unconditional default output home. ADR-M-007 (both documents) states: "A framework-governing ADR SHOULD live in `docs/design/`; **a project-relevant ADR SHOULD live in `projects/PROJ-NNN-*/decisions/`**" — and the Canonical Location Model table lists project-relevant as the "(recommended)" row alongside framework, not as a lesser case. Since most ADRs are project-scoped (11 of 14 non-frozen ADRs cataloged are project/entity-dialect per the Migration Plan table), the one skill agent that actually authors ADRs would, per the Fix spec as written, default every output to the framework home regardless of the decision's actual scope.
**Effect:** The Fix spec bakes a systematic scope-mismatch into the tool most likely to be used to create new ADRs, contradicting the very location model this rule file exists to codify.
**S/O/D rationale:** S=6 (a functional default-output defect in the primary authoring tool, not merely descriptive prose). O=6 (will manifest on essentially every architecture-agent ADR creation unless the agent is separately told the target scope out-of-band). D=6 (requires comparing the Fix spec's literal edit against the Canonical Location Model table to notice the mismatch).
**Corrective Action:** Change F2-a/F2-d's Output Location to a conditional: `projects/PROJ-NNN-*/decisions/ADR-{domain-slug}-NNN-*.md` (project-relevant, default) or `docs/design/ADR-{domain-slug}-NNN-*.md` (framework-governing, only when explicitly scoped as such), matching ADR-M-007's stated precedence.
**Acceptance Criteria:** SKILL.md Output Location reflects both homes with project as the default case.
**Post-Correction RPN estimate:** ~60.

---

### FM-018-20260702T1: No pre-flight, author-runnable slug-collision check; only post-merge CI detection (Critical, RPN 210)

**Element:** E-12 New-project onboarding & slug arbitration. **Failure Mode:** Missing.
**Evidence:** L-3 "Slug-uniqueness" (`adr-standards-rule-draft.md:179`) is a repo-wide `sort | uniq -d` FAIL check, run in CI — i.e., after a commit/PR is already created. Neither document provides a locally-runnable pre-flight command or documented workflow step for a new author (especially on a brand-new project's very first ADR) to check for slug collisions *before* authoring/committing.
**Effect:** Collision discovery happens only after the fact (CI failure), at which point the author must rename mid-review — exactly the citation-churn risk the Decision otherwise works hard to eliminate for promotion. This gap is most acute for new-project onboarding, the specific lifecycle stage named in the task mandate, since a first-time author has no established mental map of existing domain slugs.
**S/O/D rationale:** S=5, O=7 (high likelihood for any new project's first ADR, given no tooling exists to prevent it), D=6.
**Corrective Action:** Publish a one-line pre-flight command in the rule file (e.g., `grep -rhoE "ADR-[a-z0-9-]+-[0-9]{3}" projects/*/decisions/ docs/design/ | sort -u`) and reference it from the onboarding-relevant sections (`docs/design/README.md` index, when built per M-5).
**Acceptance Criteria:** Pre-flight command documented in the rule file's ID Scheme or MEDIUM Standards section.
**Post-Correction RPN estimate:** ~50.

---

### FM-019-20260702T1: "TBR-2" domain-slug arbiter is referenced twice but never defined (Major, RPN 128)

**Element:** E-12. **Failure Mode:** Ambiguous.
**Evidence:** ADR-PROJ031-004 §L2 Architectural Implications ("a lightweight index (`docs/design/README.md`) and an arbiter (TBR-2)") and the Risks table (R-3 mitigation, "Domain index + lightweight arbiter (TBR-2)") both reference "TBR-2" as a forward pointer. Full-text review of both deliverable documents (this ADR and the companion rule draft) confirms "TBR-2" is never defined, resolved, assigned to an owner, or linked to a tracked worktracker/GH-issue anywhere in either file.
**Effect:** A reader encountering "TBR-2" has no way to determine what it resolves to, who owns resolving it, or when — an internal forward-reference to a nonexistent artifact.
**S/O/D rationale:** S=4, O=8 (verified absent on full read — certain, not probabilistic), D=4 (easily caught by any careful read-through, since the token appears with no antecedent — lower detection difficulty than most findings here).
**Corrective Action:** Either resolve TBR-2 inline (name the arbiter role/process explicitly) or file it as a tracked worktracker item and cite the ID in both documents.
**Acceptance Criteria:** "TBR-2" either resolved or replaced with a real tracked reference.
**Post-Correction RPN estimate:** ~30.

---

### FM-020-20260702T1: Status vocabulary defines meanings but not permitted transitions (Major, RPN 90)

**Element:** E-13 Status vocabulary & lifecycle transitions. **Failure Mode:** Missing.
**Evidence:** The Status Vocabulary tables (ADR-PROJ031-004:446-458; rule-draft:157-167) define the meaning of each of the 5 states but specify no transition graph (e.g., can `REJECTED` -> `PROPOSED` recur for a revised resubmission under the same ID, or is `REJECTED` terminal like `SUPERSEDED`?). No L-1..L-7 rule inspects status-transition validity across revisions (only static current-state checks like L-5).
**Effect:** Ambiguity about whether a rejected ADR's `NNN` can be reused for a revised attempt (relevant to ADR-M-005's "never reused" sequence rule) or whether a new `NNN` is required, with no enforcement either way.
**S/O/D rationale:** S=3, O=5, D=6.
**Corrective Action:** Add an explicit transition table (e.g., `PROPOSED -> {ACCEPTED, REJECTED}`; `ACCEPTED -> {DEPRECATED, SUPERSEDED}`; `REJECTED`/`SUPERSEDED`/`DEPRECATED` terminal) clarifying that a revised resubmission after `REJECTED` requires a new `NNN`, consistent with ADR-M-005.
**Acceptance Criteria:** Transition table added to Status Vocabulary section.
**Post-Correction RPN estimate:** ~30.

---

### FM-021-20260702T1: "ADRs are the sole ontology exception" framing is undercut by `DEC-NNN`'s own bare-form usage (Critical, RPN 210)

**Element:** E-14 Relationship to worktracker `DEC-NNN`. **Failure Mode:** Inconsistent.
**Evidence:** Both documents repeatedly invoke `DEC-NNN`'s "permanently parent-scoped composite `{ParentId}--DEC-NNN-slug`" form as the contrast case proving ADRs are uniquely exempt from scope-prefixing (ADR-PROJ031-004 Rationale §1, "every worktracker entity is scope-prefixed... their scope *is* a permanent property"; ADR-M-011: "ADRs are the one Jerry artifact class whose identifier encodes subject, not scope"). Verified against the cited source, `skills/worktracker/rules/worktracker-directory-structure.md`: lines 65 and 73 do show the double-hyphen composite form at Epic/Feature level (`{EpicId}--{DecisionId}-{slug}.md`), but lines 80 and 88 show that at **Enabler and Story level**, the identical `DEC-NNN` entity type uses a **bare** form with no parent-ID prefix at all (`{DecisionId}-{slug}.md`, e.g. `DEC-001-template-fidelity.md`) — scope is expressed entirely by the containing folder, not the filename, which is structurally the same "identity does not encode scope; location does" pattern this ADR proposes as ADRs' unique differentiator. Neither deliverable document quotes or acknowledges the Enabler/Story-level bare form; both quote only the Epic/Feature composite example.
**Effect:** The repeated "ADRs are the *sole* exception" claim (used 3 times across the two documents as one of three independent supporting arguments for the Decision, per ADR-PROJ031-004's Rationale §1) is not fully accurate — roughly half of `DEC-NNN`'s own instances already separate identity from scope via location, weakening (though not invalidating — arguments 2 and 3 of the Rationale stand independently) the ontology-uniqueness pillar of the justification.
**S/O/D rationale:** S=5 (weakens, but does not collapse, one of three independent supporting arguments for a Decision that is otherwise robust per its own stated sensitivity analysis). O=6 (the counter-evidence is present in the very source file cited by both documents — a citation-accuracy gap, not speculation). D=7 (requires reading the full cited source file rather than trusting the single quoted example line, which both documents do without cross-checking the sibling rows).
**Corrective Action:** Revise Rationale §1 and ADR-M-011 to acknowledge: "`DEC-NNN` already partially separates identity from scope at Enabler/Story level; ADRs generalize this pattern to a case where scope is also expected to *change* over the artifact's life, which `DEC-NNN` scope never does — the true differentiator is scope *mutability*, not scope-encoding-in-identity per se."
**Acceptance Criteria:** Rationale §1 and ADR-M-011 revised to state the more precise, defensible distinction (mutability, not mere non-encoding).
**Post-Correction RPN estimate:** ~50.

---

### FM-023-20260702T1: No Migration Plan action item commits to executing this ADR's own described self-promotion (Major, RPN 120)

**Element:** E-15 This ADR's own identity / self-compliance meta-note. **Failure Mode:** Missing.
**Evidence:** The Meta-Note (ADR-PROJ031-004:495-503) describes the ADR's own eventual Path-2 promotion (rename to `docs/design/ADR-adr-convention-001-...`, tombstone this file) as an "intended end-state," explicitly P-022-labeled as inference not action taken ("I have not moved or renamed the file... only the user-mandated file at the mandated path was created"). The Migration Plan's 8-item action list (M-1 through M-8) contains no discrete item for "execute this ADR's own Path-2 self-promotion post-ratification."
**Effect:** The document's own flagship self-compliance demonstration ("a worked example of its own Path-2 promotion and grandfathering rules," line 501) risks never being executed, since nothing in the tracked adoption plan requires it — the ADR could remain permanently in its dialect form, undermining the pedagogical value the Meta-Note explicitly claims for it.
**S/O/D rationale:** S=4, O=6 (self-promotion steps not on a tracked action list have a documented tendency to be deprioritized, consistent with FM-1's general lint-never-implemented risk pattern), D=5 (the gap is somewhat visible since M-1..M-8 is a finite, readable list, but the omission of this specific item is easy to miss on a first read).
**Corrective Action:** Add "M-9 — Execute this ADR's own Path-2 promotion (rename to `docs/design/`, tombstone, re-point citations)" to the Migration Plan action items, gated on M-1 (user ratification).
**Acceptance Criteria:** M-9 added and linked to a tracked worktracker item.
**Post-Correction RPN estimate:** ~40.

*(Minor findings FM-012-20260702T1 and FM-022-20260702T1 are not expanded per template guidance — corrective action is optional for Minor; see Findings Table for their one-line descriptions and Recommendations for optional follow-up.)*

---

## Recommendations (Step 4)

Prioritized by RPN, highest first. All Critical items are recommended as mandatory corrective actions before M-6 (lint implementation) proceeds; Major items are recommended corrective actions; Minor items are optional improvement notes.

### Mandatory (Critical, RPN >= 200)

| Rank | FM ID | RPN | Corrective Action (summary) | Est. Post-Correction RPN |
|---|---|---|---|---|
| 1 | FM-001-20260702T1 | 504 | Fix L-1 regex case-class; add regression test against all 11 legacy filenames | ~40 |
| 2 | FM-013-20260702T1 | 448 | Add full-path citation caveat to Promotion Path 1; audit for path-based citations before first promotion | ~90 |
| 3 | FM-008-20260702T1 | 448 | Add L-9 prose/repo-wide citation-string lint; enumerate/fix known stale PROJ-007 citations | ~90 |
| 4 | FM-007-20260702T1 | 441 | Fix/remove dead `ci.yml:2` citation; audit non-markdown files for ADR references; add L-8 rule | ~80 |
| 5 | FM-015-20260702T1 | 280 | File a tracked, owned, dated worktracker/GH-issue for M-6 lint implementation | ~120 |
| 6 | FM-003-20260702T1 | 288 | Correct Migration Plan "Zero cost" claim; retrofit real YAML frontmatter into 3 exemplar ADRs | ~60 |
| 7 | FM-016-20260702T1 | 252 | Rename template placeholder `{SCOPE}` to `{DOMAIN-SLUG}` in Fix F1-a | ~50 |
| 8 | FM-017-20260702T1 | 216 | Make SKILL.md Output Location conditional on project vs. framework scope | ~60 |
| 9 | FM-010-20260702T1 | 210 | Prohibit scope/location changes via "amendment"; require Promotion Process | ~60 |
| 10 | FM-018-20260702T1 | 210 | Publish a locally-runnable pre-flight slug-collision command | ~50 |
| 11 | FM-021-20260702T1 | 210 | Revise Rationale/ADR-M-011 to cite scope *mutability*, not mere non-encoding, as the true differentiator | ~50 |

### Recommended (Major, RPN 80-199)

| Rank | FM ID | RPN | Corrective Action (summary) |
|---|---|---|---|
| 12 | FM-011-20260702T1 | 150 | Add worked example for combined supersede+promotion case |
| 13 | FM-004-20260702T1 | 180 | Promote L-5 to FAIL for `ACCEPTED` scope/location mismatches |
| 14 | FM-005-20260702T1 | 144 | Add "Path 0" draft-to-canonical graduation procedure |
| 15 | FM-006-20260702T1 | 140 | Reconcile "Frozen Legacy" heading vs. PROJ-014's actionable disposition |
| 16 | FM-014-20260702T1 | 140 | Exclude historical/append-only records from Path 2's grep-replace step |
| 17 | FM-019-20260702T1 | 128 | Resolve or track "TBR-2" explicitly |
| 18 | FM-002-20260702T1 | 120 | Add L-1b WARN rule distinguishing canonical vs. dialect grammar |
| 19 | FM-009-20260702T1 | 120 | Specify amendment-block placement/ordering rule |
| 20 | FM-023-20260702T1 | 120 | Add M-9 action item for this ADR's own self-promotion |
| 21 | FM-020-20260702T1 | 90 | Add explicit status-transition table |

### Optional (Minor, RPN < 80)

| FM ID | RPN | Note |
|---|---|---|
| FM-022-20260702T1 | 72 | Consider a contingency canonical-ID statement if a non-B scheme is ratified |
| FM-012-20260702T1 | 42 | Consider an acyclicity check for the supersede graph (low priority) |

---

## Scoring Impact (Step 5)

| Dimension | Weight | Impact | Rationale (referencing FM-NNN) |
|-----------|--------|--------|-------------------------------|
| Completeness | 0.20 | Negative | FM-005 (no draft-to-canonical graduation path), FM-007 (research corpus catalog missing a 9th live ID family) |
| Internal Consistency | 0.20 | Negative | FM-002, FM-004, FM-006, FM-010, FM-016, FM-017, FM-022 — multiple cross-section contradictions between the Decision's own vocabulary/precedence and the companion rule draft's implementation specs |
| Methodological Rigor | 0.20 | Negative | FM-001 (regex defect breaks the FMEA's own "no big-bang" premise), FM-009, FM-011, FM-020, FM-012 — several lifecycle procedures (amendment, combined supersede/promote, status transitions) are under-specified relative to the otherwise rigorous trade-study/sensitivity-analysis portions of the ADR |
| Evidence Quality | 0.15 | Negative | FM-003 (frontmatter-schema claim contradicted by the cited exemplars), FM-013 (citation-free promotion claim contradicted by repo's own citation practice), FM-021 (ontology-uniqueness claim incompletely cross-checked against its own cited source) |
| Actionability | 0.15 | Negative | FM-014 (unscoped grep-replace risks corrupting history), FM-015 (gating M-6 has no owner/timeline), FM-018 (no pre-flight collision check), FM-023 (no tracked self-promotion action item) |
| Traceability | 0.10 | Mixed | Positive: extensive file+line citation discipline throughout both documents, explicit P-022 inference labeling. Negative: FM-008 (tombstone lint doesn't cover the exact prose-citation failure the ADR's own evidence describes), FM-019 ("TBR-2" forward reference never resolved) |

**Overall assessment:** The Decision's directional judgment (Scheme B, subject-encoded identity) is not invalidated by this analysis — it remains well-argued, sensitivity-tested, and honestly caveated (0.78 self-assessed confidence, explicit adverse-regime disclosure). However, the **implementation/enforcement companion draft** (Deliverable 2, the proposed rule file) contains a reproducible, verifiable regex defect (FM-001) that would break CI for the entire legacy corpus if implemented as written, plus 10 further Critical-RPN findings concentrated in the lint-enforcement, cross-referencing, and template/skill drift-fix specifications — precisely the "systematic decomposition of the lifecycle" areas this FMEA was scoped to probe. **Recommendation: REVISE** — address the 11 Critical findings (particularly FM-001, FM-007, FM-008, FM-013, FM-015) before M-6 (lint implementation, marked gating) proceeds; the Decision prose itself needs only the FM-021/FM-016/FM-003 terminology and evidentiary corrections.

---

## Execution Statistics

- **Total Findings:** 23
- **Critical:** 11
- **Major:** 10
- **Minor:** 2
- **Sum RPN:** 4,953
- **Elements Analyzed:** 15 of 15 (100%)
- **Protocol Steps Completed:** 5 of 5 (Decompose; Enumerate; Rate S/O/D; Prioritize + Corrective Actions; Synthesize + Score)
- **H-15 Self-Review:** Completed — findings table totals cross-checked against Finding Details count (23 entries, 21 expanded [11 Critical + 10 Major], 2 Minor summarized only per template); RPN classification bands re-verified against template's mechanical rule (RPN>=200 OR S>=9 => Critical; RPN 80-199 OR S 7-8 => Major; RPN<80 AND S<=6 => Minor) for all 23 rows.
- **Blind Protocol Compliance:** No file under `.../adversary/` was read except this output file. No deliverable file was edited. All evidence citations resolve to files outside the adversary/ tournament directory (the two deliverables under review, `.context/rules/`, `docs/design/`, `skills/`, `.github/workflows/`, and `skills/worktracker/rules/`).

**STATUS: COMPLETE.**

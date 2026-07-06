# Steelman Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention) + Companion Rule Draft

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.10)
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (iteration 9) | **Date:** 2026-07-06 | **Original Author:** ps-architect
- **Blind protocol observed:** iteration-009/010 findings not read; only `subtraction-pass-notes.md` and the two deliverables (this iteration's authorized inputs) were consulted.

---

## Summary

**Steelman Assessment:** After 8 prior tournament rounds and 17 dispositioned Criticals (all recorded in `subtraction-pass-notes.md` with a disclosed residual register R-1..R-17/R-A/R-B/R-C), the package is exceptionally mature, self-critical, and honestly hedged. Reading it in its strongest form, the core decision (subject-encoded ADR identity, Scheme B) is well-argued, the promotion-independent arguments (ontology category-error, discoverability) carry the decision even discounting the promotion-frequency evidence, and the disclosure discipline (Claim-Status, INHERENT residuals, P-022 labeling) is genuinely unusual in its rigor.

**Improvement Count:** 1 Major, 0 Minor (see note on classification below).

**Original Strength:** Very high. No genuinely new gap was found in the Decision, Rationale, Sensitivity Analysis, or Migration Plan sections — every weakness a charitable-but-critical read surfaced there had already been found and dispositioned in iterations 1-8.

**Recommendation:** Incorporate the one improvement below (a narrow, surgical text addition consistent with the subtraction doctrine — zero new machinery) before treating the L5 lint's L-4 rule as fully specified. All other package elements are already strong; no fundamental revision needed.

**Classification note (P-022):** The finding below is presented at **Major**, not Critical, after applying H-16 charitable interpretation. It is evidence-backed and genuinely novel (not covered by R-1..R-17/R-A/R-B/R-C), but it affects only the *enforcement* of the discouraged dialect path, not the *core thesis* (subject-encoded canonical identity, which is unaffected). Per the VERIFIED-CRITICALS protocol, a fair 3-lens refutation would correctly note the guidance "delivers value with zero tooling" regardless of this gap — so calling it Critical (thesis-invalidating) would overclaim. Reported as Major: a genuine specification-completeness gap in one of the five enforcement rules, previously undisclosed.

---

## Finding ID: 003-001 (S-003 Steelman; template prefix `SM-001`; this project's own tag glossary uses `ST-001` for steelman — both cross-referenced for traceability)

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| 003-001 | L-4 ("ID↔location") is one of the 5 declared "deterministic, registry-free" (c-006) FAIL-class lint rules, but its matching algorithm is unspecified in a way that makes it non-executable, as literally written, against the real, existing, cited-as-grandfathered dialect corpus — for two structurally distinct reasons (hyphen-form mismatch, and an entity-prefix-to-project-directory gap with no registry-free resolution) | Major | L-4 stated only as prose: "A `PROJ{NNN}`/`EPIC{NNN}`/`FEAT{NNN}`/`STORY{NNN}` dialect prefix ... matches its containing project/entity dir" — no regex, no normalization step, unlike L-1/L-2/L-3 which are given literal, executable regexes | Add one explicit sentence (per rule, in both files) stating the exact match procedure: (a) strip the hyphen from `PROJ-NNN` directory segments before comparing to the ID's `PROJNNN` token; (b) for EPIC/FEAT/STORY-prefixed dialect ADRs that reside in a project-level `decisions/` dir (not an entity-embedded `work/.../{ENTITY}/` dir), state plainly that L-4 cannot verify the ID↔location relationship without a registry (contradicting c-006 for that subclass) and disclose it as a residual (matching the doctrine already used for R-9..R-17) rather than leaving it silently unspecified | Methodological Rigor / Traceability |

---

## Improvement Details

### 003-001: L-4's matching algorithm is unspecified and, for a real subset of the grandfathered corpus, unspecifiable without a registry

**Affected Dimension:** Methodological Rigor (the document holds itself to giving literal, executable regexes for L-1/L-2/L-3 but not L-4) and Traceability (the residual register R-1..R-17 is otherwise exhaustive but omits this).

**Original Content (as written):**

- Rule draft, L-4 row: *"A `PROJ{NNN}`/`EPIC{NNN}`/`FEAT{NNN}`/`STORY{NNN}` dialect prefix (full closed set) matches its containing project/entity dir. Project-based topology only — zero operative effect under the repository-based topology."* (`projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:178`)
- ADR mirror of the same row: `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:684`
- The grandfather-baseline exemption clause (added in iteration 8 to close a related gap) explicitly scopes itself to two rules only: *"A git-modified file that is already on that baseline is treated as grandfathered-exempt from **L-1/L-2**, not as a newly-minted ID."* (rule draft `:183`; ADR mirror `:688`) — L-3, L-4, and L-7 are not included in this exemption's text.
- Dialect ID grammar (no hyphen in the token): `PROJECT-ID : one of a CLOSED entity-prefix set {PROJ|EPIC|FEAT|STORY}\d{3}` (rule draft `:65`; ADR `:335-341`) — i.e., the literal string is `PROJ031`, `EPIC002`, `STORY015`, never hyphenated.
- Canonical Location Model, same document, one table below: the *directory* naming convention for the dialect's home is hyphenated — `projects/PROJ-NNN-*/decisions/` (rule draft `:82`; ADR `:388`), and for entity-embedded dialect ADRs: `projects/.../work/.../{ENTITY}/` (rule draft `:83`; ADR `:390`).

**Two independent, verified failure modes:**

1. **Hyphen-form mismatch (affects the entire PROJ-dialect corpus, ~11-15 files, including this ADR's own filename).** The ID token is `PROJ031` (no hyphen); the containing directory is `PROJ-031-cowork-skeleton` (hyphenated, per the worktracker SSOT convention `projects/PROJ-{NNN}-{slug}/` cited in `project-workflow.md` and echoed at ADR line 388). A literal string match of "does `PROJ031` appear in `PROJ-031-cowork-skeleton`" requires an unstated normalization step (e.g., strip the hyphen from the directory's leading `PROJ-NNN` segment, or extract `\d{3}` from both sides and compare). This is not stated anywhere in either document — the four other rules (L-1, L-2, L-3, L-7) are each given a literal, copy-pasteable regex or `sort | uniq -d` one-liner; L-4 is given prose only.

2. **Entity-prefix-to-project-directory gap (affects real, existing, SSOT-cited grandfathered files — not a hypothetical).** Verified on disk (Glob, 2026-07-06): `ADR-EPIC002-001-strategy-selection.md` and `ADR-EPIC002-002-enforcement-architecture.md` both live at `projects/PROJ-001-oss-release/decisions/` — a **project-level** `decisions/` directory, not an entity-embedded `work/.../EPIC-002.../` folder. This is exactly the location pattern the ADR's own Bimodal Refinement section describes ("both verified on disk in `projects/PROJ-001-oss-release/decisions/`", ADR `:292-294`) and the same files the Migration Plan explicitly schedules for a future frontmatter retrofit (M-11, ADR `:541`: *"onto the framework-cited entity-dialect ADRs `ADR-EPIC002-001-strategy-selection`, `ADR-EPIC002-002-enforcement-architecture`... which today carry no `scope:` field at all"*). For these files, L-4's stated check ("EPIC{NNN} ... matches its containing project/entity dir") has no string-based signal to succeed on: "EPIC002" does not appear anywhere in the path `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md` — the Epic number (002) and the Project number (001) are simply different numbers, and the relationship between them (Epic-002 belongs to Project-001) is worktracker parent/child metadata, not filesystem-derivable. Confirming this by contrast: `ADR-STORY015-001-tier-model-renumbering.md` **is** correctly entity-embedded, at `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/` (Glob-verified) — so the Location Model's two documented dialect-location patterns (project-`decisions/` for PROJ-prefix; entity-embedded `work/.../{ENTITY}/` for EPIC/FEAT/STORY-prefix) are real and mostly followed, but the EPIC002 pair is a real, existing **third pattern** (entity-prefixed ID, project-level location) that neither pattern nor L-4's prose covers.

**Why this is not already covered by a disclosed residual.** R-10 ("out-of-scan location class") is the closest existing residual, but it describes files the scan **never reaches** (entity-embedded ADRs with no `decisions/` segment, and the repository-based topology's `{RepositoryRoot}/decisions/` home). The EPIC002 files are the opposite case: they **are** inside a scanned `*/decisions/*` path (so L-1/L-2/L-3 do reach them), yet L-4 cannot structurally verify them once reached. This is a distinct failure mode from R-10, not a restatement of it. None of R-9, R-11 through R-17 addresses ID↔location matching either.

**Why this matters for the standard's purpose (not merely cosmetic).** Constraint c-006 requires the convention to be "deterministically lint-able without a central registry or global counter." L-4 is repeatedly presented as satisfying this for all four dialect prefixes equally. For the EPIC/FEAT/STORY subclass sitting in a project-level `decisions/` dir, no registry-free check exists — which is a genuine tension with c-006, not merely an implementation nicety, since resolving it *would* require either (a) a registry-free rule change (e.g., scope L-4 to PROJ-prefix only, and disclose that EPIC/FEAT/STORY-prefix ADRs outside an entity-embedded folder are simply not location-checked), or (b) accepting the registry dependency as a residual. Leaving it unstated, in a document whose entire second half is built on the ethic of "disclose every enforcement gap explicitly, never overclaim" (Claim-Status Convention, R-1..R-17), is the one place that ethic was not applied to this specific rule.

**Best Case Conditions (per Steelman Step 4):** This finding is strongest when read as an omission relative to the document's *own* internal standard of rigor (every other rule gets an exact executable spec; this one does not), not as a claim that the overall convention is broken. The MEDIUM-tier override (documented-justification-in-the-PR) already bounds the practical damage even if L-4 misfires once built, and the lint is designed-not-built today, so there is no current operational harm. Confidence: HIGH that the gap exists as described (filesystem-verified); MODERATE on severity, given the legitimate counter-argument that a competent implementer would supply the missing normalization/scope-narrowing without being told — hence Major rather than Critical.

**Rationale mapping to scoring dimension:** Methodological Rigor (the rule draft's own internal consistency — 4 of 5 rules are literal/executable, 1 is prose-only) and Traceability (the residual register is otherwise exhaustive and should include this).

**Recommendation (subtraction-doctrine-consistent — no new machinery):** Add one sentence to L-4's row in both files: normalize the PROJ-prefix comparison by stripping the hyphen from the directory's leading `PROJ-NNN` segment (or equivalently extracting and comparing the 3-digit number), and explicitly narrow L-4's scope to PROJ-prefix dialect ADRs only for the project-`decisions/`-location check — disclosing that EPIC/FEAT/STORY-prefix dialect ADRs outside an entity-embedded folder (the real EPIC002-001/002 case) are not location-verified by L-4, as a new residual entry (e.g., R-18) alongside R-9..R-17. This is a text-only fix, consistent with every prior iteration's doctrine of disclosure-over-machinery.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All major sections already examined across 8 prior rounds; this pass found one narrow gap, not a coverage hole |
| Internal Consistency | 0.20 | Positive | Closing 003-001 removes the one place where the document's own "give an exact regex" standard (applied to L-1/L-2/L-3) is not applied to L-4 |
| Methodological Rigor | 0.20 | Positive | Directly strengthens the enforcement design's rigor and its consistency with c-006 |
| Evidence Quality | 0.15 | Neutral | Package evidence quality is already very high (extensive `grep`/Glob verification throughout); this finding adds one more verified data point without changing the overall bar |
| Actionability | 0.15 | Positive | The recommended fix is a single, concrete, text-only sentence per file — directly incorporable |
| Traceability | 0.10 | Positive | Extends the R-1..R-17 residual register to a genuinely novel gap, preserving the register's completeness |

---

## Execution Statistics

- **Total Findings:** 1
- **Critical:** 0
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 6 of 6 (Deep Understanding; Weakness Classification; Argument Reconstruction — targeted, not full rewrite, given the deliverable's 8-round maturity; Best Case Scenario; Improvement Findings documented; Presentation/H-15 self-review applied below)

---

## H-15 Self-Review

1. The finding has specific evidence: exact file+line citations for both documents, plus Glob-verified on-disk paths for the three real ADR files discussed (`ADR-EPIC002-001-strategy-selection.md`, `ADR-EPIC002-002-enforcement-architecture.md`, `ADR-STORY015-001-tier-model-renumbering.md`).
2. Severity (Major) is justified against the S-003 rubric: it materially strengthens methodological rigor and traceability but does not invalidate the core decision (Scheme B) or the guidance's zero-tooling value — a Critical classification was considered and rejected as overclaiming, per the anticipated 3-lens refutation.
3. Finding identifier follows the requested stable format (`003-001`) with cross-references to both the template's `SM-NNN` prefix and this project's own established `ST-` steelman tag.
4. The report is internally consistent: the Summary states 1 Major/0 Minor/0 Critical, and the Findings Table and Detail section both reflect exactly that one finding.
5. No findings were omitted or minimized: this was the strongest genuinely novel gap found after a full read of both deliverables and the complete `subtraction-pass-notes.md` disposition register (17 prior Criticals, R-1..R-17/R-A/R-B/R-C); no other purpose-blocking, non-disclosed gap was identified. All other candidate issues considered during this review (frontmatter-schema completeness, citation-ratio scope-limitation, DEPRECATED/SUPERSEDED transitions, nav-table coverage, cross-file relative-link resolution) were verified already correctly handled or already disclosed as residuals, and are not repeated here as findings per the task's instruction that already-disclosed residuals are not findings.

**H-16 compliance:** This execution applied the charitable/strongest-case reading required before any critique strategy runs. No critique strategy (S-002/S-004/S-001) has been executed as part of this S-003 pass.

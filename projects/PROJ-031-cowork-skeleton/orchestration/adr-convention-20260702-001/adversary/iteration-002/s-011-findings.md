# Chain-of-Verification Report: ADR-PROJ031-004 + adr-standards-rule-draft (Iteration 2)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, iteration 2)
**H-16 Compliance:** S-003 status not visible to this blind reviewer (BLIND PROTOCOL forbids reading other adversary outputs/prior iterations). S-011's H-16 dependency is indirect per the template — proceeding regardless.
**Claims Extracted:** 18 | **Verified:** 12 | **Discrepancies:** 6 (3 Critical/Major-material, 3 Minor)

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Claim Inventory and Verification](#claim-inventory-and-verification) | Extracted claims, verification questions, independent answers |
| [Findings Table](#findings-table) | CV-NNN findings, severity-classified |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Verification Ratio](#verification-ratio) | Verified/Unverified/False counts |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Recommendations](#recommendations) | Corrections by severity |

---

## Summary

Independent verification of 18 testable claims extracted from ADR-PROJ031-004 and its companion rule draft found 12 fully VERIFIED (matching cited sources/filesystem exactly, including the load-bearing corpus-family counts, the PROJ-007 stale-citation evidence, the BUG-006 F-002 correction, and the 16-file grandfather regression-test arithmetic), 3 MINOR discrepancies (vague counts, an ambiguous "11-of-14" reference, unverifiable commit SHAs), and **3 MATERIAL discrepancies, one of which is Critical**: the deliverable's central claim that "every scope-prefixed family is collision-free by construction" is falsified by a documented, independently-verified prior incident (`BUG-006-c4-tournament-review.md`, 2026-04-01) in which the output-path-resolution ADR was originally minted as `ADR-EPIC002-001` and collided with the pre-existing `ADR-EPIC002-001-strategy-selection.md` already cited as SSOT in `quality-enforcement.md`. This same source review also shows the deliverable's cited "BUG-006... C4-criticality bug-fix effort (iter2 through iter8 rescoring, a tournament review)" is evidence for a *different* bug (output-path hardcoding, GH #230) than the ADR-naming-evaluation review the deliverable attributes it to — a conflation that overstates the "paid promotion tax with a git receipt" argument used to justify Scheme B. **Recommendation: REVISE** — the collision-freedom claim and the BUG-006 evidentiary attribution both require correction before acceptance; neither invalidates the overall decision (Scheme B still stands on its ontology-mutability and discoverability arguments) but both currently overstate the evidentiary case and must not go uncorrected in a C4 governance document.

---

## Claim Inventory and Verification

| CL | Claim (deliverable text) | Type | Source Checked | Independent Result |
|----|---------------------------|------|-----------------|---------------------|
| CL-001 | Corpus family counts: Framework domain-slug=3, Project-ID scoped=11, Entity-ID scoped=3, GH-issue scoped=1, Bare legacy(transcript)=6+1, Bare archived=4, Bare project transient=4, OSS series=7+several (ADR, lines 68-78) | Quoted values | Filesystem (`Glob **/ADR-*.md`, `**/adr-*.md`) | **VERIFIED** for all counts except "7 + several" (OSS/lowercase family), which is imprecise by design — see CV-004 |
| CL-002 | "still-stale ADR-PROJ007-001/002 citations remain in PROJ-007's own `ORCHESTRATION.yaml:228,242`, `WORKTRACKER.md:106-107`, and `EN-001.md:48-49,72-73` as of 2026-07-02" (ADR line 48, 127, 244) | Cross-reference | `projects/PROJ-007-agent-patterns/ORCHESTRATION.yaml:228,242`; `WORKTRACKER.md:106-107`; `work/EN-001-install-agent-pattern-deliverables/EN-001.md:48-49,72-73` | **VERIFIED** — exact text match at every cited line (`summary: "1065 lines. ADR-PROJ007-001..."` at 228; `"821 lines. ADR-PROJ007-002..."` at 242; `TASK-014`/`TASK-015` rows at WORKTRACKER 106-107; `# 3 \| ADR-PROJ007-001...` / `# 4 \| ADR-PROJ007-002...` and `TASK-014`/`TASK-015` rows at EN-001.md 48-49, 72-73) |
| CL-003 | `.github/workflows/ci.yml:2` cites `projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`, and that project path "no longer exists in the repo" (ADR lines 80, 435) | Cross-reference | `.github/workflows/ci.yml:2`; `Glob projects/PROJ-001*` | **VERIFIED** — line 2 is an exact match; `Glob` for `projects/PROJ-001*` returns no results (only `PROJ-001-oss-release` exists, not `PROJ-001-plugin-cleanup`) |
| CL-004 | `docs/knowledge/exemplars/templates/adr.md:1` uses bare `ADR-{NUMBER}` and `:182` points at non-existent `docs/decisions/` (ADR line 64; rule draft Fix 1-a/1-f) | Cross-reference | `docs/knowledge/exemplars/templates/adr.md:1,182` | **VERIFIED** — line 1 is `# ADR-{NUMBER}: {Title}`; line 182 is `link-artifact {PS_ID} {ENTRY_ID} FILE "docs/decisions/..."` |
| CL-005 | `skills/architecture/SKILL.md:105,284,437` prescribe `docs/design/ADR_NNN_*.md` (underscore) (ADR line 64; rule draft Fix 2-a/2-d) | Cross-reference | `skills/architecture/SKILL.md:105,284,437` | **VERIFIED** — all three lines contain the literal string `ADR_NNN_*.md` |
| CL-006 | `docs/design/ADR-agent-design-001.md:3` records origin via `PS-ID: PROJ-007 \| ENTRY: e-004` (ADR line 306) | Quoted value | `docs/design/ADR-agent-design-001.md:3` | **VERIFIED** — exact text match |
| CL-007 | `docs/design/ADR-output-path-resolution-001.md:8` records origin via blockquote `Parent: EPIC-002` (ADR line 306) | Quoted value | `docs/design/ADR-output-path-resolution-001.md:8` | **VERIFIED** — exact text match |
| CL-008 | "BUG-006's F-002 collision example is factually wrong — `ADR-EPIC002-001` exists only in PROJ-001-oss-release, not PROJ-022/PROJ-004" (ADR line 595, References; rule draft line 6 house-style precedent) | Historical assertion | `BUG-006-adr-naming-evaluation.md:99-101`; `adr-convention-standards-research.md:200`; filesystem `Glob` | **VERIFIED** — BUG-006 F-002 does claim PROJ-022/PROJ-004 duplication; filesystem confirms `ADR-EPIC002-001/002` exist only under `projects/PROJ-001-oss-release/decisions/`; research doc explicitly documents this correction at line 200 |
| CL-009 | `DEC-NNN` is written bare at Enabler/Story level, e.g. `DEC-001-cli-hook.md`, scope supplied by the parent folder (ADR lines 52, 345; rule draft ADR-M-011) | Behavioral claim | `skills/worktracker/rules/worktracker-directory-structure.md:80` | **VERIFIED** — line 80: `├── {DecisionId}-{slug}.md e.g. DEC-001-cli-hook.md` (Enabler level, no compound scope prefix), consistent with line 65's Epic-level compound `{EpicId}--{DecisionId}-{slug}.md` |
| CL-010 | `.context/rules/quality-enforcement.md` HARD ceiling "25/25 with zero headroom"; AE-002 (`.context/rules/`)/AE-003 (new ADR) each independently set a C3 floor (ADR header, line 92, c-001) | Rule citation | `.context/rules/quality-enforcement.md` (SSOT, in-context) | **VERIFIED** — exact match: "Current count: 25 HARD rules... Zero headroom"; AE-002/AE-003 rows read exactly as cited |
| CL-011 | 16-file grandfather regression-test enumeration: `PROJ010`×6, `PROJ022`×2, `PROJ031`×4 (incl. this ADR), `EPIC002`×2, `STORY015`×1 = 15 dialect files + `ADR-150-001` singleton = 16 total (ADR line 203; rule draft L5 Lint Spec, gating regression test) | Quoted value | Filesystem `Glob` | **VERIFIED** — exact arithmetic match: 6+2+4+2+1=15, +1=16 |
| CL-012 | S-011 template composite score 3.75, C3-optional/C4-required status (implicit dependency, not deliverable text but load-bearing for this review's own protocol) | Rule citation | `.context/rules/quality-enforcement.md` Strategy Catalog | **VERIFIED** — "S-011 \| Chain-of-Verification \| 3.75" matches template Identity table exactly |
| CL-013 | "Every *scope-prefixed* family is collision-free by construction" (ADR line 82, repeated in spirit at lines 104, 119, 146, 153) | Behavioral claim | `projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md:37,158,168,227,265` | **MATERIAL DISCREPANCY (FALSE)** — see CV-001 |
| CL-014 | "a dedicated C4-criticality bug-fix effort (BUG-006, spanning iter2 through iter8 rescoring, a tournament review, and multiple group reviews — see `projects/PROJ-030-bugs/reviews/BUG-006-*`)" corrected the ADR-naming usability failure (advocate-external.md:53, relied upon by ADR §Related Decisions/PRECEDENT and Rationale arg. 3) | Historical assertion | `BUG-006-c4-tournament-review.md:1`; `BUG-006-artifact-directory-evaluation.md:1`; `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md:1`; `projects/PROJ-030-bugs/WORKTRACKER.md:20` | **MATERIAL DISCREPANCY** — see CV-002 |
| CL-015 | P-022 count reconciliation: "the promoted output-path-resolution one (originally minted as `ADR-EPIC002-001`, renamed on promotion, commit `9b36bda2`/`41539073`)" is presented as a routine domain-first rename (ADR line 249, footnote) | Historical assertion | `BUG-006-c4-tournament-review.md:37,158,227,265` | **MATERIAL DISCREPANCY (incomplete disclosure)** — see CV-003 |
| CL-016 | "OSS orchestration series... 7... Lowercase ad-hoc... several" (research doc line 67-68, ADR line 77) | Quoted value | Filesystem `Glob adr-*.md` | **MINOR DISCREPANCY** — see CV-004 |
| CL-017 | "the common 11-of-14 case, matching AD-M-011's project-first default" (rule draft Fix 2-a/2-d, F2-a/F2-d) | Quoted value | Corpus tables in ADR/research doc | **MINOR DISCREPANCY (ambiguous denominator)** — see CV-005 |
| CL-018 | Specific commit SHAs cited as evidentiary anchors: `41539073`, `5ef0b2fa`, `9b36bda2`, `66a5826f` (advocate-domain-slug.md:50-51; advocate-external.md:92-94) | Historical assertion | No git/Bash tool available to this reviewer | **UNVERIFIABLE (tooling constraint)** — see CV-006 |

---

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260702-i2 | "Every scope-prefixed family is collision-free by construction" | `BUG-006-c4-tournament-review.md:37,158,227,265` | A real ID collision occurred within the Entity-ID-scoped family (`ADR-EPIC002-001` reused for two unrelated decisions) | **Critical** | Evidence Quality / Methodological Rigor |
| CV-002-20260702-i2 | BUG-006's C4 tournament/iter2-iter8 rescoring is cited as the remediation of the ADR-naming usability finding | `BUG-006-c4-tournament-review.md:1`; `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md:1`; `WORKTRACKER.md:20` | The cited C4 tournament evidence is for a different, unrelated bug (output-path hardcoding, GH #230), not the ADR-naming-evaluation review | **Major** | Evidence Quality / Traceability |
| CV-003-20260702-i2 | P-022 EPIC-002 count-reconciliation footnote describes the output-path ADR's rename as routine domain-first migration | `BUG-006-c4-tournament-review.md:37,158,227,265` | Omits that the rename was compelled by a documented ID collision with the SSOT-cited strategy-selection ADR, not merely a stylistic upgrade | **Major** | Completeness / Internal Consistency |
| CV-004-20260702-i2 | "OSS series... 7 + several" | `adr-convention-standards-research.md:68`; filesystem | "Several" is an unfalsifiable count (2-4 files depending on inclusion criteria) | Minor | Evidence Quality |
| CV-005-20260702-i2 | "the common 11-of-14 case" | Rule draft Fix 2-a/2-d | No table in either deliverable file states an "11-of-14" total; the denominator is not traceable to a single stated set | Minor | Traceability |
| CV-006-20260702-i2 | Specific commit SHAs used as evidentiary anchors | advocate-domain-slug.md:50-51; advocate-external.md:92-94 | Not independently verifiable by this reviewer (no git/Bash access); one adjacent claim in the same evidentiary chain (CV-001/CV-003) required correction on deeper investigation, raising the stakes of unverified SHA citations | Minor | Evidence Quality |

**Finding ID Format:** `CV-{NNN}-{execution_id}` where `execution_id = 20260702-i2` (iteration 2, this session).

---

## Finding Details

### CV-001: False collision-freedom claim for scope-prefixed ADR families [CRITICAL]

**Claim (from deliverable):** "The bare `ADR-NNN` namespace has already collided across three unrelated contexts... Every *scope-prefixed* family is collision-free by construction." (ADR-PROJ031-004, line 82; the same premise underlies Option A's Pros "strong collision-safety (C1=4)" at line 121, and Option scoring generally treats scope-prefixed schemes A/C/dialect as structurally collision-immune throughout the Options Considered and Enforcement Design sections.)

**Source Document:** `projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md` (an independent, dated C4 quality-score report from 2026-04-01, scoring `docs/design/ADR-output-path-resolution-001.md`).

**Independent Verification:** The tournament review states (line 37): *"CC-003 / CV-001 / FM-014: ADR ID `ADR-EPIC002-001` collides with the existing strategy-selection ADR already referenced in `quality-enforcement.md`"* and (line 158): *"One material discrepancy in 9 claims verified: `ADR-EPIC002-001` is not a unique identifier. `quality-enforcement.md` lines 108, 275, 290, and 350 reference `ADR-EPIC002-001` as the strategy-selection ADR... The new output path ADR uses the same ID for a completely different subject."* The recommended fix (line 168, 227, 265) was to rename to `ADR-EPIC002-002`. Filesystem confirms `ADR-EPIC002-001-strategy-selection.md` (created 2026-02-13, `ADR-ID: ADR-EPIC002-001` per its own header comment) still exists today at `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md`, and `.context/rules/quality-enforcement.md` does cite `ADR-EPIC002-001` as this same strategy-selection ADR ("dimension-level rubrics (ADR-EPIC002-001; `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md`)").

**Discrepancy:** The deliverable's corpus-survey and options-scoring both assert that Entity-ID-scoped and Project-ID-scoped ADR identity is "collision-free by construction" because "project/entity IDs are uniquely allocated at creation" (line 119). This is falsified by a real, documented event: a second, unrelated decision (the output-path-resolution ADR) was independently minted with the exact same Entity-ID-scoped identifier (`ADR-EPIC002-001`) already in use by the strategy-selection ADR — a genuine same-scope collision, caught only by a subsequent C4 tournament review, not prevented "by construction." The claim conflates "globally unique parent-scope IDs" (true: `PROJ-031` cannot collide with `PROJ-014`) with "collision-free sequence numbering within a scope" (false: nothing prevented two independently-authored decisions from both claiming `NNN=001` under the same `EPIC002` scope).

**Severity:** Critical — this is a load-bearing factual premise used repeatedly to score Options A/C favorably on collision-safety (C1) and to argue scope-prefixed dialects are a safe fallback (D-3). A C4 governance ADR asserting an architectural property ("by construction") that a prior, cited-adjacent C4 review already falsified is a Methodological Rigor and Evidence Quality defect that should block acceptance until corrected.

**Dimension:** Evidence Quality (0.15) / Methodological Rigor (0.20)

**Correction:** Amend line 82 (and the parallel statements in Options A/C scoring, lines 119-123, and Enforcement Design's implicit reliance on entity-scope uniqueness) to read: "Scope-prefixed families are collision-resistant, not collision-free — the *cross-project* dimension of the scope key (`PROJ-NNN`/`EPIC-NNN`) is unique by construction, but the *within-scope sequence number* is not automatically coordinated and has collided in practice (`ADR-EPIC002-001`, documented in `BUG-006-c4-tournament-review.md`, resolved by rename). This is exactly the same class of residual risk R-6 already discloses for domain-slug schemes — it should be disclosed symmetrically for the dialect/entity-scoped family too, not asserted away." Also revise the L-4 lint spec (rule draft) to confirm it would have caught this exact historical case (entity-ID + NNN uniqueness within scope), or disclose that it would not.

---

### CV-002: BUG-006 evidentiary conflation (ADR-naming review vs. output-path bug) [MAJOR]

**Claim (from deliverable, via cited advocacy source relied upon as evidence):** "Every framework ADR that exists today was authored under scheme A/C identity and required a dedicated, C4-criticality bug-fix effort (BUG-006, spanning iter2 through iter8 rescoring, a tournament review, and multiple group reviews — see `projects/PROJ-030-bugs/reviews/BUG-006-*`) to correct the resulting usability failure." (`advocate-domain-slug.md:53`, explicitly cited and relied upon by ADR-PROJ031-004 as its "paid promotion tax with a git receipt" argument at line 127 and the "PRECEDENT" row of Related Decisions, line 581: "Migrated in the ~150-reference BUG-006 remediation (commit `41539073`...)")

**Source Document:** `projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md:1` (title: "Quality Score Report: ADR-EPIC002-001 Unified Output Path Resolution + BUG-006 Migration Implementation"); `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md:1` (title: "BUG-006: Agent output paths hardcoded to skill directories — breaks end-user output persistence (#230)"); `projects/PROJ-030-bugs/WORKTRACKER.md:20` ("BUG-006 | Bug | Agent output paths hardcoded to skill directories (#230) | completed | PROJ-030-bugs").

**Independent Verification:** The worktracker's canonical BUG-006 entity is about output-path hardcoding (`skills/*/output/`), tracked via GitHub Issue #230, unrelated in subject matter to ADR naming. The iter2-iter8 rescoring / group-ab / group-c / group-de / tournament-review files in `projects/PROJ-030-bugs/reviews/` that document the C4 process are scoring `docs/design/ADR-output-path-resolution-001.md` + `BUG-006-skill-output-path-hardcoded.md` — output-path work, not ADR naming. `BUG-006-adr-naming-evaluation.md` (the actual Nielsen ADR-naming usability review the ADR-PROJ031-004 cites throughout) is a separate, standalone file with no corresponding `BUG-006-adr-naming-c4-*` tournament trail anywhere in the repo.

**Discrepancy:** The deliverable's chain of evidence implies the ADR-naming usability finding (BUG-006-adr-naming-evaluation.md) went through the rigorous, multi-iteration C4 tournament process ("iter2 through iter8 rescoring, a tournament review, and multiple group reviews") documented in `projects/PROJ-030-bugs/reviews/BUG-006-*`. In fact, that entire review trail belongs to the *different*, coincidentally-same-numbered worktracker Bug BUG-006 (output-path hardcoding). The ADR-naming evaluation's remediation (the domain-slug renames, commits `41539073`/`5ef0b2fa`) is real (per CHANGELOG.md:75-76), but it did not undergo the cited C4 tournament rigor — that rigor belongs to a different remediation entirely. This overstates the evidentiary strength of the "paid tax" argument used to justify Scheme B.

**Severity:** Major — this does not invalidate the underlying (accurate) fact that the 3 framework ADRs were renamed and incurred citation breaks, but it materially mischaracterizes the *rigor* behind that finding's acceptance, and it is used as supporting evidence ("a git receipt") in a C4 decision document, which requires precise sourcing.

**Dimension:** Evidence Quality (0.15) / Traceability (0.10)

**Correction:** Separate the two BUG-006 references explicitly: cite `BUG-006-adr-naming-evaluation.md` alone for the ADR-naming finding/remediation (commits `41539073`/`5ef0b2fa` per CHANGELOG.md:75-76), and do not attribute the `BUG-006-c4-tournament-review.md`/iter2-iter8/group-review evidentiary weight to it. If the intent was to note that the *same numeric ID* "BUG-006" was independently reused for two unrelated worktracker artifacts (itself a notable naming-collision irony given the subject matter of this very ADR), state that explicitly instead of implying one continuous remediation effort.

---

### CV-003: Incomplete P-022 disclosure of the EPIC-002 rename's true cause [MAJOR]

**Claim (from deliverable):** "The 'starting point' reconciliation... the promoted output-path-resolution one (originally minted as `ADR-EPIC002-001`, renamed on promotion, commit `9b36bda2`/`41539073`) plus the two that remain local on disk" (ADR-PROJ031-004, line 249 footnote, "Count reconciliation (P-022, iter-1, closes SM-004)").

**Source Document:** `projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md:37,158,168,227,265`.

**Independent Verification:** As established in CV-001, the rename of the output-path ADR away from `ADR-EPIC002-001` was not a voluntary, purely stylistic "domain-first semantic convention" choice (as `advocate-domain-slug.md:50` characterizes it) — it was compelled by a documented ID collision defect (CC-003/CV-001/FM-014, Major-severity findings in that engagement) with the pre-existing, SSOT-cited `ADR-EPIC002-001-strategy-selection.md`.

**Discrepancy:** The P-022 disclosure section of ADR-PROJ031-004 (line 602, "P-022 disclosures") lists five items (a-e) but omits this one: that one of the three "framework ADR promotions" cited as evidence for Scheme B was in fact forced by a genuine same-scope collision bug, not merely chosen for improved discoverability. Given that the whole point of the P-022 disclosure list is to state negative/qualifying facts honestly, and given that this fact directly undercuts the "collision-free by construction" premise (CV-001), its absence from the disclosure list is a completeness gap in a document that otherwise prides itself on exhaustive self-correction (the changelog documents seven rounds of iter-1 remediation).

**Severity:** Major — the omission is adjacent to, and compounds, CV-001; disclosing it would have surfaced CV-001 during the deliverable's own iter-1 self-review.

**Dimension:** Completeness (0.20) / Internal Consistency (0.20)

**Correction:** Add a sixth P-022 disclosure item: "(f) The output-path-resolution ADR's departure from `ADR-EPIC002-001` was not a discretionary domain-first upgrade alone — it was compelled by a documented ID collision with the pre-existing `ADR-EPIC002-001-strategy-selection.md` (see `BUG-006-c4-tournament-review.md`), which is itself evidence that Entity-ID-scoped identity is not collision-free by construction (see corrected line 82)."

---

### CV-004: Unfalsifiable "several" count in OSS/lowercase-ad-hoc family [MINOR]

**Claim:** "OSS series / lowercase ad-hoc | `ADR-OSS-NNN`, `adr-{slug}[-vN]` | `ADR-OSS-001`, `adr-cli-integration-v2` | 7 + several | Series / informal" (ADR line 77; research doc line 68 uses the identical "several").

**Independent Verification:** `Glob **/adr-*.md` returns exactly 2 clearly-informal lowercase files matching `adr-{slug}[-vN]` (`adr-cli-integration.md`, `adr-cli-integration-v2.md`) plus 2 borderline files under a PROJ-021 verification folder (`adr-in001-description-validation.md`, `adr-pm001-rejection-artifact.md`) whose status as "ADRs" vs. test fixtures is unclear from filename alone.

**Discrepancy:** "Several" is not a falsifiable count; depending on inclusion criteria the true number is 2 or 4. Not material to any decision in the package, but it is the one count in the otherwise-precise corpus table that cannot be independently pinned down.

**Severity:** Minor. **Dimension:** Evidence Quality (0.15). **Correction:** State the exact count (2, if the PROJ-021 files are excluded as non-ADR verification fixtures) or explain the inclusion criteria.

---

### CV-005: Untraceable "11-of-14" denominator [MINOR]

**Claim:** Rule draft Fix 2-a/2-d: "the common 11-of-14 case, matching AD-M-011's project-first default" (`adr-standards-rule-draft.md:232,235`).

**Independent Verification:** No table in either deliverable file states a set of exactly 14 ADRs of which 11 are project-scoped. The closest candidate (Project-ID scoped = 11, Framework domain-slug = 3; 11+3=14) excludes Entity-ID-scoped (3) and GH-issue-scoped (1) ADRs without explanation, which is a defensible but unstated denominator choice.

**Severity:** Minor. **Dimension:** Traceability (0.10). **Correction:** State explicitly which 14 ADRs are being counted (e.g., "11 Project-ID-scoped + 3 framework domain-slug = 14; Entity-ID- and GH-issue-scoped ADRs excluded from this ratio because they are non-`docs/design/` and non-`PROJ`-prefixed").

---

### CV-006: Commit-SHA citations not independently verifiable by this reviewer [MINOR]

**Claim:** Commits `41539073`, `5ef0b2fa`, `9b36bda2`, `66a5826f` cited as evidentiary anchors throughout `advocate-domain-slug.md` and `advocate-external.md`, and relied upon transitively by ADR-PROJ031-004 (e.g., line 581).

**Independent Verification:** This reviewer's tool access (Read/Glob/Grep/Write only, no Bash/git) cannot execute `git show <sha>` to confirm commit contents or dates. CHANGELOG.md corroborates the *outcome* of two of the four cited commits (the domain-slug renames, CHANGELOG.md:75-76) but does not itself quote commit SHAs, so full corroboration is not possible from this reviewer's toolset.

**Severity:** Minor (a tooling limitation of this review, not a confirmed defect) — flagged because CV-001/CV-003 show that at least one adjacent claim in the same evidentiary chain (the "clean domain-first rename" framing) required correction upon deeper investigation, which raises the stakes of citations this reviewer cannot fully verify. **Dimension:** Evidence Quality (0.15). **Correction:** Owner (with git/Bash access) should re-verify all four SHAs via `git show <sha> --stat` and attach the verification to the ADR's References section, or downgrade unverified SHA citations to "commit reference, unverified in this review cycle."

---

## Verification Ratio

| Result | Count | % of 18 |
|--------|:---:|:---:|
| VERIFIED | 12 | 67% |
| MINOR DISCREPANCY | 3 (CV-004, CV-005, CV-006) | 17% |
| MATERIAL DISCREPANCY (Major/Critical) | 3 (CV-001, CV-002, CV-003) | 17% |
| UNVERIFIABLE | 1 (CL-018 / CV-006, counted once — folded into Minor above) | — |
| **FALSE claims (Critical, blocks acceptance)** | **1 (CV-001)** | **6%** |

**Note on the blind-review scope:** Per BLIND PROTOCOL, this reviewer did not read S-003 (Steelman), other-strategy iteration outputs, or prior-iteration adversary findings, and therefore cannot confirm whether CV-001/CV-002/CV-003 were already raised (and possibly rejected or accepted) in iteration 1. If any of these three were already surfaced and the owner explicitly declined them with recorded rationale, the severity of re-raising them here should be discounted by the orchestrator accordingly — but this reviewer has no visibility into that history and reports findings independently, per the blind protocol's own design intent (S-011 Step 3: "Read the source document independently... do NOT re-read the deliverable's claim" — extended here to mean do not rely on other reviewers' framing).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CV-003: P-022 disclosure list omits the collision root-cause of one of its three central promotion examples |
| Internal Consistency | 0.20 | Negative | CV-001 vs. R-6 (cross-branch collision risk, already disclosed for domain-slug) creates an asymmetry: the deliverable discloses residual collision risk for Scheme B but asserts zero collision risk for A/C/dialect schemes, when both have documented incidents |
| Methodological Rigor | 0.20 | Negative | CV-001: a verifiable architectural claim ("collision-free by construction") was not checked against readily available prior-review evidence before being asserted as a load-bearing premise in Option scoring |
| Evidence Quality | 0.15 | Negative | CV-002: the strongest-sounding evidentiary citation in the package ("a paid promotion tax with a git receipt... iter2 through iter8 rescoring") is misattributed to the wrong underlying bug; CV-004/CV-006 add minor imprecision |
| Actionability | 0.15 | Neutral | All corrections above are surgical, single-paragraph amendments; none require re-architecting the Decision (D-1 through D-5) |
| Traceability | 0.10 | Negative | CV-005: an unresolved "11-of-14" denominator; CV-002: a citation chain that traces to the wrong worktracker entity |

**Net effect on the deliverable's core decision:** Low. Scheme B (subject-encoded ADR identity) does not depend solely on the collision-freedom argument — the ontology-mutability argument (Rationale, argument 1) and the discoverability argument (argument 2, BUG-006-adr-naming-evaluation's genuine, correctly-cited Nielsen findings F-001/F-003) are unaffected by CV-001/CV-002/CV-003 and independently support the Decision. However, a C4 governance ADR asserting a falsified "by construction" architectural guarantee, and misattributing its strongest evidentiary citation, are precisely the class of defect S-011 exists to catch before ratification.

---

## Recommendations

**Critical (MUST correct before acceptance):**
- CV-001: Correct the "collision-free by construction" claim (ADR line 82 and parallel Option A/C scoring language) to acknowledge the documented `ADR-EPIC002-001` collision; either add a symmetric residual-risk disclosure (parallel to R-6) or demonstrate the L5 lint (L-3/L-4) would have caught this specific historical case.

**Major (SHOULD correct):**
- CV-002: Disambiguate the two unrelated "BUG-006" artifacts; do not attribute the output-path bug's C4 tournament/iter2-iter8 rigor to the ADR-naming-evaluation review.
- CV-003: Add the omitted P-022 disclosure item about the true (collision-driven) cause of the output-path ADR's rename.

**Minor (MAY correct):**
- CV-004: Replace "several" with an exact count or explicit inclusion criteria.
- CV-005: State the denominator for "11-of-14" explicitly.
- CV-006: Have an owner with git/Bash access re-verify the four cited commit SHAs.

---

*Report generated by adv-executor (S-011 Chain-of-Verification), blind iteration 2. Constitutional compliance: P-003 (no subagents spawned), P-020 (no files outside this output path edited), P-022 (all claims above cite exact file paths/line numbers from independently-read sources; inference is labeled where used, e.g. the CV-004/CV-005 "defensible but unstated" characterizations).*

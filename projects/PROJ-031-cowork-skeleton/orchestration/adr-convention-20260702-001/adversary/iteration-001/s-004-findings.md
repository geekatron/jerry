# Pre-Mortem Report: ADR-PROJ031-004 ADR Identifier Convention (+ companion `adr-standards.md` draft)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata, H-16 status, failure scenario |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All PM-NNN findings, severity, priority |
| [Finding Details](#finding-details) | Full evidence for each Critical/Major finding |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Finding counts, protocol completion |

---

## Header

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, iteration-001)
**H-16 Compliance:** The file `.../adversary/iteration-001/s-003-findings.md` was confirmed to **exist** via a path-only match (Grep `files_with_matches` mode); its **content was not read**, per the BLIND PROTOCOL mandate restricting this reviewer to its own output file. This satisfies H-16 evidentially (the steelman step has run in a prior tournament group) without violating the blind-review boundary. Independently, the deliverable itself embeds steelman reasoning inline for every rejected option (`ADR-PROJ031-004-adr-identifier-convention.md:115,123,131,139,147,154` — each option opens "Strongest case (steelman...)"), so the content has already been strengthened at the artifact level regardless of the external S-003 artifact's score. **Labeled as inference:** I infer, but did not verify by reading its content, that the external S-003 output reached a passing quality bar.

**Failure Scenario (Step 1-2, prospective hindsight):** It is 2027-07-02. The ADR identifier convention has failed. Twelve months in: (a) the L5 CI lint was never wired into `.github/workflows/` — `scripts/lint_adr_convention.py` does not exist today and no worktracker task or GitHub issue tracks its creation; (b) of the handful of new ADRs authored since ratification, most still use the familiar `ADR-{PROJECT-ID}-NNN` dialect (copied from the 11 pre-existing examples) rather than the recommended domain-slug form, because nothing compels the switch; (c) when a contributor finally *did* attempt to wire the lint exactly as specified, it broke CI for every one of the 25 currently-existing ADR files across `docs/design/`, `docs/adrs/`, `docs/archive/`, and 8 `projects/*/decisions/` directories, because the published regex cannot match any of them; (d) the `.context/rules/adr-standards.md` file was authored per M-2 but was never symlinked into `.claude/rules/`, so it is not auto-loaded at session start and new agents/authors never see it unless they go looking. This is the "nobody follows it" + "lint blocks legitimate work" double failure the prompt asks this review to stress-test.

---

## Summary

This package is unusually rigorous for a naming-convention ADR — it self-identifies 5 risks and a 4-item pre-mortem already (`ADR-PROJ031-004:349-373`), which raises the bar for what a blind Pre-Mortem must add. This execution found **1 latent Critical technical defect that would reproduce the exact "lint blocks legitimate work" failure narrative on the very files the ADR promises to grandfather**, plus **5 Major** findings concentrated in the gap between "decision text" and "actually-enforced practice" (no tracked lint task, no `.claude/rules/` symlink step, an unresolved taxonomy-arbiter TBR, an internally-inconsistent "zero cost" migration claim, and a striking self-referential data point: the ADR's own author defaulted to the discouraged dialect for this very framework-scope decision). None of the findings invalidate the *decision* (Scheme B over A/C/D/E/F); all of them threaten the *adoption mechanics* the decision depends on to be real rather than aspirational. **Recommendation: REVISE before ratification** — specifically, fix the L-1 regex (P0, blocking), and add the missing adoption-mechanics items (M-9 symlink step, M-10 lint-tracking worktracker entity, M-11 frontmatter-retrofit line item, TBR-2 resolution) to the Migration Plan before this proceeds to ACCEPTED status.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260702-s004-i1 | L-1 lint regex is lowercase-only and rejects every existing dialect/legacy ADR filename, including the ADR's own | Technical | High | Critical | P0 | Internal Consistency |
| PM-002-20260702-s004-i1 | No worktracker task / GH issue exists for M-6 (the lint); repo precedent (H-16/17/18 "Tier B") shows MEDIUM rules routinely ship without deterministic enforcement | Process | High | Critical | P0 | Actionability |
| PM-003-20260702-s004-i1 | Migration Plan omits the `.claude/rules/` symlink step required for L1 auto-loading of the new rule file | Process | Medium-High | Major | P1 | Completeness |
| PM-004-20260702-s004-i1 | The ADR's own author defaulted to the discouraged project-scoped dialect for this very framework-scope decision, undercutting the "SHOULD prefer domain-slug" behavioral assumption | Assumption | High | Major | P1 | Internal Consistency |
| PM-005-20260702-s004-i1 | TBR-2 (who arbitrates domain-slug taxonomy) is explicitly unresolved and its proposed mitigation (`docs/design/README.md` index) does not yet exist | Assumption | Medium-High | Major | P1 | Completeness |
| PM-006-20260702-s004-i1 | Migration Plan claims "Zero" cost for the 3 framework ADRs while, in the same row, requiring frontmatter to be added that none of the 3 currently has | Technical/Process | High | Major | P1 | Internal Consistency |
| PM-007-20260702-s004-i1 | L-4 lint spec covers only `ADR-PROJ{NNN}-NNN` in `projects/*/decisions/`; the permitted entity-embedded dialect (`ADR-EPIC{NNN}-NNN`, `ADR-STORY{NNN}-NNN`) has no location-consistency check | Technical | Medium | Minor | P2 | Completeness |
| PM-008-20260702-s004-i1 | Migration Plan M-7 cites H-26 (a skill-registration rule) to justify CLAUDE.md/AGENTS.md rule-file registration; H-26 does not govern rule files | External/Governance | Medium | Minor | P2 | Traceability |
| PM-009-20260702-s004-i1 | Adoption Action Items (M-1..M-8) carry role labels ("governance", "devsecops") instead of worktracker task IDs; PS Integration section still shows all 3 rows "Pending" | Resource | High | Minor | P2 | Actionability |

**Aggregate:** 2 Critical, 4 Major, 3 Minor. 9 total findings (exceeds the 5-cause minimum; all 5 category lenses used).

---

## Finding Details

### PM-001: L-1 Lint Regex Rejects Every Existing ADR It Promises to Grandfather [CRITICAL]

**Failure Cause:** The L5 lint's "Form" rule (L-1) is specified as `^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$` (`adr-standards-rule-draft.md:69`, restated at `ADR-PROJ031-004-adr-identifier-convention.md:468`). This character class, `[a-z0-9]`, is lowercase-only and case-sensitive (no `/i` flag stated anywhere in the spec). Every currently-existing dialect/legacy ADR filename uses an uppercase scope token immediately after `ADR-`: `ADR-PROJ010-001-agent-team-architecture.md`, `ADR-PROJ022-001-ux-skill-architecture.md`, `ADR-PROJ031-001-skeleton-distribution-strategy.md` through `ADR-PROJ031-004-adr-identifier-convention.md` (this file itself), `ADR-EPIC002-001-strategy-selection.md`, `ADR-EPIC002-002-enforcement-architecture.md`, `ADR-STORY015-001-tier-model-renumbering.md`, and `ADR-150-001-pre-tool-enforcement-consolidation.md` (verified via Glob against the live repo, 2026-07-02). None of these match the published regex — the "P" in "PROJ", the "E" in "EPIC", the "S" in "STORY" all fall outside `[a-z0-9]`. The rule draft calls this same regex "canonical **+ dialect**" (`adr-standards-rule-draft.md:69`), explicitly claiming it covers both forms, but its own dialect example two lines earlier — `ADR-PROJ031-005-foo.md` (`adr-standards-rule-draft.md:65`) — would itself fail the regex it is presented alongside.
**Category:** Technical
**Likelihood:** High — this is not a hypothetical future risk; it is a defect already present in the shipped spec text. It will manifest the first time M-6 is implemented literally, unless someone catches it during implementation (not guaranteed — see PM-002).
**Severity:** Critical — if implemented as written, L-1 is a FAIL-class rule (`adr-standards-rule-draft.md:177`, blocking CI). It would reject 100% of the 8 project/entity-dialect directories that D-4 and c-003 explicitly promise to "grandfather in place" with "no big-bang renumber," including the ADR-PROJ031-004 file itself. This is the literal "lint blocks legitimate work" scenario this Pre-Mortem was commissioned to stress-test.
**Evidence:** `adr-standards-rule-draft.md:69` (regex text); `adr-standards-rule-draft.md:65` (dialect example that would fail its own regex); Glob results against the live repo confirming 8+ uppercase-scoped filenames still active (`projects/PROJ-010-cyber-ops/decisions/ADR-PROJ010-*.md`, `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-*.md`, `projects/PROJ-024-.../STORY-015-.../ADR-STORY015-001-*.md`, `projects/PROJ-030-bugs/decisions/ADR-150-001-*.md`, `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-*.md`).
**Dimension:** Internal Consistency (the lint contradicts D-4/c-003 in the same document) and Completeness (the regex is not actually "canonical + dialect" as labeled).
**Mitigation:** Split L-1 into two regexes as the "canonical + dialect" label already implies conceptually: a lowercase-only canonical form, and a separate dialect form permitting an uppercase scope token (`^ADR-(PROJ|EPIC|STORY)\d{3}-\d{3}(-[a-z0-9-]+)?\.md$` or equivalent), both accepted by L-1. Add a repo-wide dry-run of the exact lint script against all 25 current ADR files as a Migration Plan gating step before M-6 is marked complete.
**Acceptance Criteria:** L-1, run against every file returned by `Glob **/ADR-*.md` in the live repo today, produces zero FAIL results for existing grandfathered files, and continues to FAIL on genuinely bare `ADR-NNN` new additions.

### PM-002: The Lint Has No Tracked Owner, Task, or Timeline — the Convention's Own Named Risk (R-5) Is Not Yet Mitigated [CRITICAL]

**Failure Cause:** M-6 ("Implement + wire the L5 CI lint") is marked "Yes (gating)" in the Migration Plan (`ADR-PROJ031-004-adr-identifier-convention.md:400`), and the ADR's own Risks table already names this exact failure mode: "R-5: Lint never gets built; convention stays advisory-only... Probability MED, Impact HIGH" (`ADR-PROJ031-004-adr-identifier-convention.md:357`). Yet as of this review, no `scripts/lint_adr_convention.py` exists (Glob confirmed), no `.github/workflows/` entry references ADR linting (the 6 existing workflows are `ci.yml`, `docs.yml`, `pat-monitor.yml`, `release.yml`, `security-scan.yml`, `version-bump.yml` — none ADR-related), and the PS Integration section at the bottom of the ADR shows all three worktracker-linkage rows still `Pending` (`ADR-PROJ031-004-adr-identifier-convention.md:542-546`) — meaning not even an Exploration Entry has been logged yet, let alone a Task for M-6. Separately, this exact repository already runs three HARD rules (H-16, H-17, H-18) in "Tier B" — enforced only by "skill enforcement" / "L1 rule awareness," explicitly *not* by deterministic L2/L3 mechanisms (`.context/rules/quality-enforcement.md` Two-Tier Enforcement Model, Tier B table) — demonstrating that in this codebase, "the rule says it will be enforced by tooling" and "the tooling exists" are frequently two different, and sometimes permanently divergent, states.
**Category:** Process
**Likelihood:** High — direct precedent exists in the same governance file for MEDIUM/compensating-control rules persisting indefinitely without their promised deterministic backstop.
**Severity:** Critical — this is the mechanism the entire convention's teeth depend on (D-5: "MEDIUM-tier, lint-enforced"). Without it, D-1 through D-4 are recommendations with zero compulsion, which is exactly the "nobody follows it" failure branch named in this task's prompt.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:357` (R-5 self-identified); `ADR-PROJ031-004-adr-identifier-convention.md:400` (M-6 gating claim, no owner/date); `ADR-PROJ031-004-adr-identifier-convention.md:542-546` (PS Integration all "Pending"); Glob confirming no `scripts/lint_adr_convention.py` and no ADR-lint workflow exist; `.context/rules/quality-enforcement.md` Two-Tier Enforcement Model (Tier B: H-16/H-17/H-18 enforced by "compensating controls" only, not L2/L3).
**Dimension:** Actionability (M-6 is stated as gating but is not actually actionable/trackable today) and Completeness (Migration Plan has no dependency-tracking mechanism).
**Mitigation:** Before this ADR moves to `ACCEPTED`, create a worktracker Task (with GH issue parity per H-31/project-workflow.md, since this is inside the `geekatron/jerry` repo) for M-6 specifically, with an assigned owner and a due date, and make the ADR's own status transition from `PROPOSED` to `ACCEPTED` conditional on that task existing (not merely "gating" in prose).
**Acceptance Criteria:** A worktracker Task ID (e.g., `TASK-0NN`) exists for "Implement `scripts/lint_adr_convention.py` and wire into CI," linked from this ADR's PS Integration section (no longer "Pending"), with a corresponding GH issue.

### PM-003: Migration Plan Omits the `.claude/rules/` Symlink Step Needed for Auto-Loading [MAJOR]

**Failure Cause:** `.context/rules/` files are auto-loaded into Claude Code's session context only via an explicit, per-file symlink into `.claude/rules/` (CLAUDE.md Navigation: "(A) = Auto-loaded content... via `.claude/rules/` symlink"; confirmed structurally — `.claude/rules/quality-enforcement.md` resolves as an individually-readable file while a directory-level glob of `.claude/rules/*` and `.claude/rules/**` returns no matches, consistent with per-file symlinks rather than a single directory-level link). This exact repo has direct precedent for this being a distinct, easily-missed step: `projects/PROJ-007-agent-patterns/work/EN-001-.../EN-001.md:53` lists "Auto-load symlinks — `.claude/rules/` symlinks for new rule files" as its **own numbered deliverable (#8)**, separate from authoring the rule content. The ADR-PROJ031-004 Migration Plan's M-2 ("Author `.context/rules/adr-standards.md`...") and M-7 ("Register the new rule in CLAUDE.md + AGENTS.md navigation") do not mention creating the `.claude/rules/adr-standards.md` symlink at all.
**Category:** Process
**Likelihood:** Medium-High — precisely the kind of infrastructure step that is invisible until someone notices the rule "isn't loading."
**Severity:** Major — if missed, the entire rule file is written to disk but never auto-injected at session start (L1), meaning agents and authors never encounter it proactively; they would have to already know to go looking in `.context/rules/`. This directly feeds the "nobody follows it" failure branch, independent of whether the lint (PM-002) ever gets built.
**Evidence:** CLAUDE.md Navigation table ("(A) = Auto-loaded... via `.claude/rules/` symlink"); `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/EN-001.md:53` (symlink treated as its own deliverable); `ADR-PROJ031-004-adr-identifier-convention.md:396,401` (M-2, M-7 — no symlink step mentioned); Glob/Read confirming `.claude/rules/quality-enforcement.md` is individually resolvable while directory-level globbing of `.claude/rules/` yields nothing.
**Dimension:** Completeness (Migration Plan step missing).
**Mitigation:** Add an explicit M-2b (or fold into M-2): "Create `.claude/rules/adr-standards.md` symlink to `.context/rules/adr-standards.md`," gated the same way M-2 is gated.
**Acceptance Criteria:** `.claude/rules/adr-standards.md` resolves to the same content as `.context/rules/adr-standards.md` after adoption; verified by a direct read of the symlink target post-merge.

### PM-004: The Convention's Own Author Chose the Discouraged Dialect for This Framework-Scope Decision [MAJOR]

**Failure Cause:** D-1/D-3 recommend (SHOULD, not MUST — c-001 forces MEDIUM tier) that authors default to domain-slug identity, especially for anything of framework-wide relevance, and reserve the project-scoped dialect only for "purely tactical" decisions the author judges will never promote. Yet this ADR — a C4, explicitly framework-governing decision about the *entire ADR corpus* — was itself authored and filed as `ADR-PROJ031-004-adr-identifier-convention.md`, the discouraged dialect form, with the Meta-Note candidly conceding the canonical form (`ADR-adr-convention-001`) is only a stated future intent, not an action taken (`ADR-PROJ031-004-adr-identifier-convention.md:499-503`). The stated reason is that "the invoking task mandated this exact path" (`ADR-PROJ031-004-adr-identifier-convention.md:499`) — but this is precisely the kind of external-pressure/expediency reasoning ordinary future authors will also have (a manager, a template, a copy-pasted precedent), and the ADR itself, elsewhere, treats "the corpus already voted" via observed behavior as load-bearing evidence (`ADR-PROJ031-004-adr-identifier-convention.md:78`, "the strongest internal signal that the team is already converging on project-ID scoping"). By that same evidentiary standard, this single data point is a signal that even a maximally-informed, maximally-motivated author defaults to the dialect when any friction (a mandated path, an existing precedent, time pressure) is present.
**Category:** Assumption
**Likelihood:** High — this is not speculative; it is an observed instance within the deliverable under review itself.
**Severity:** Major — it does not invalidate Scheme B as the better identity *scheme*, but it materially weakens confidence that D-2's "promotion becomes free" benefit will actually be realized for future ADRs, since realizing it requires authors to *choose* the canonical form at birth, and the one clean natural-experiment data point available says they will not, absent enforcement (which per PM-002 does not yet exist).
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:11` (filename banner acknowledging the dialect choice); `ADR-PROJ031-004-adr-identifier-convention.md:499-503` (Meta-Note, explicit concession); `ADR-PROJ031-004-adr-identifier-convention.md:78` (the ADR's own use of observed-behavior-as-evidence for the opposite conclusion elsewhere in the same document).
**Dimension:** Internal Consistency (the document treats "observed author behavior" as strong evidence in one place, `:78`, but does not apply the same lens to its own authoring choice).
**Mitigation:** Either (a) explicitly downgrade confidence in the "authors will prefer domain-slug from birth" assumption in the Rationale/Sensitivity sections to reflect this self-referential counter-evidence, or (b) treat this as the trigger to make the lint (PM-002) a true CI gate on *new* ADRs specifically at authoring time (not just a periodic audit), since voluntary compliance has already been shown, in-document, not to be reliable.
**Acceptance Criteria:** The Promotion-Frequency Sensitivity or Consequences section explicitly acknowledges this self-referential data point and its effect on the 0.78 confidence figure, or the Migration Plan is updated to make new-ADR lint enforcement (not just audit) the adopted mechanism.

### PM-005: TBR-2 (Domain-Slug Taxonomy Arbiter) Is Unresolved and Its Proposed Fix Does Not Exist Yet [MAJOR]

**Failure Cause:** The trade study explicitly flags an open question: "TBR-2: Under B, who arbitrates domain-slug taxonomy (to keep slugs unique and meaningful)? A lightweight `docs/design/README.md` domain index... would serve" (`projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/explore/trade-study.md:353`). The ADR's own pre-mortem (FM-4, `ADR-PROJ031-004-adr-identifier-convention.md:370`) and Risk R-3 (`:355`) both depend on "a lightweight index + arbiter (TBR-2)" as mitigation for taxonomy sprawl (e.g., `agent-design` vs. `agent-definition` vs. `agents`) — the exact failure mode that would erode the convention's single biggest claimed win (discoverability). Confirmed via Glob: `docs/design/README.md` does not exist today, and no arbiter role, agent, or process is named anywhere in either deliverable file.
**Category:** Assumption
**Likelihood:** Medium-High — taxonomy drift is a well-known failure mode for any slug/tag-based system without an owner (the ADR itself already anticipates it as FM-4/R-3), and the mitigation is currently vaporware.
**Severity:** Major — this directly threatens the convention's primary claimed benefit (discoverability/clustering, `ADR-PROJ031-004-adr-identifier-convention.md:330`); an un-owned mitigation for a self-identified MED-HIGH-impact risk is a real gap, not a hypothetical one.
**Evidence:** `trade-study.md:353` (TBR-2, unresolved); `ADR-PROJ031-004-adr-identifier-convention.md:355,370` (R-3, FM-4 depending on the same unbuilt mitigation); Glob confirming `docs/design/README.md` does not exist.
**Dimension:** Completeness (a load-bearing mitigation is referenced but not specified or assigned).
**Mitigation:** Resolve TBR-2 explicitly before ratification: name either a specific role (e.g., the ps-architect agent on each promotion) or a lightweight automated check (e.g., a fuzzy-match lint warning on near-duplicate slugs) as the taxonomy arbiter, and add `docs/design/README.md` creation as a concrete, owned Migration Plan item rather than an "(Optional)" aside (currently M-5, marked "No" for gating, `:399`).
**Acceptance Criteria:** TBR-2 has a named resolution (role or mechanism) documented in the ADR, and `docs/design/README.md` exists with at least the 3 current framework-ADR domain slugs indexed.

### PM-006: "Zero Cost" Migration Claim for Framework ADRs Is Internally Inconsistent With Its Own Required Action [MAJOR]

**Failure Cause:** The Migration Plan states, for the 3 existing framework ADRs: "Already domain-slug (canonical) | Action: None — add explicit `origin_project`/`scope` frontmatter if missing | Cost: **Zero**" (`ADR-PROJ031-004-adr-identifier-convention.md:382`). This is self-contradictory: "add ... frontmatter if missing" is an action, and it is in fact required, because none of the 3 files currently has it. Direct verification of `docs/design/ADR-agent-design-001.md` (lines 1-10) shows no YAML frontmatter block at all — only an HTML comment `<!-- PS-ID: PROJ-007 | ENTRY: e-004 | AGENT: ps-architect-001 | DATE: 2026-02-21 -->` (line 3), which is a different mechanism than the proposed `origin_project:`/`scope:` YAML fields (`ADR-PROJ031-004-adr-identifier-convention.md:275-291`). The same gap applies to the 11 grandfathered project-dialect ADRs. Since L-5 (Framework home) and L-6 (Provenance) lint rules key off exactly these frontmatter fields (WARN class, `adr-standards-rule-draft.md:181-182`), 100% of the current ADR corpus would WARN on day one of lint activation — not "Zero" cost, but a retrofit across 14+ files that is nowhere tracked as a Migration Plan line item.
**Category:** Technical/Process
**Likelihood:** High — directly verified against the live file.
**Severity:** Major — WARN-class means this does not block CI, which caps the blast radius, but it does mean the "provenance preserved losslessly" positive consequence (`:329-331`) is not actually true for any existing ADR until a real, uncosted retrofit happens.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:382` (the "Zero" cost row); `docs/design/ADR-agent-design-001.md:1-10` (direct read confirming no YAML frontmatter, only an HTML PS-ID comment); `adr-standards-rule-draft.md:181-182` (L-5/L-6 depend on the missing fields).
**Dimension:** Internal Consistency (cost claim contradicts the action stated in the same cell).
**Mitigation:** Add an explicit Migration Plan line item (M-9) for "Retrofit `origin_project`/`scope` frontmatter into the 3 framework ADRs and 11 project-dialect ADRs," with a realistic (non-zero) cost estimate, separate from the "None" action currently implied.
**Acceptance Criteria:** Migration Plan cost column for the framework-ADR row reflects actual required effort, and a tracked action item exists for the frontmatter retrofit across all 14 pre-existing files.

### PM-007: L-4 Lint Has No Coverage for the Permitted Entity-Embedded Dialect [MINOR]

**Failure Cause:** L-4 ("Dialect↔location") only checks that `ADR-PROJ{NNN}-NNN` matches its containing `projects/PROJ-{NNN}-*/` directory, scoped to `projects/*/decisions/` (`adr-standards-rule-draft.md:180`). But the Canonical Location Model explicitly permits a second dialect class — "Entity-embedded (permitted) | `projects/.../work/.../{ENTITY}/` | `ADR-{ENTITY-ID}-NNN`" (`ADR-PROJ031-004-adr-identifier-convention.md:302`), evidenced by the live `ADR-STORY015-001-tier-model-renumbering.md` sitting inside `projects/PROJ-024-.../STORY-015-tier-model-renumbering/`. No lint rule checks that an `ADR-EPIC{NNN}-NNN` or `ADR-STORY{NNN}-NNN` file's location actually matches its claimed entity ID.
**Category:** Technical
**Likelihood:** Medium.
**Severity:** Minor — WARN/coverage gap only; does not block anything today, simply means a whole permitted ID class is unchecked.
**Evidence:** `adr-standards-rule-draft.md:180` (L-4 scope, `projects/*/decisions/` only); `ADR-PROJ031-004-adr-identifier-convention.md:302` (entity-embedded row); live file `projects/PROJ-024-tactical-work/.../STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md` (Glob-confirmed).
**Dimension:** Completeness.
**Mitigation:** Extend L-4 to also check `ADR-{ENTITY-ID}-NNN` files under `work/` entity folders for entity-ID/location consistency, or explicitly document this class as out-of-scope-by-design if that is the intent.
**Acceptance Criteria:** L-4 spec text explicitly states whether entity-embedded dialect ADRs are checked or intentionally excluded.

### PM-008: Migration Plan Mis-Cites H-26 for Rule-File Registration [MINOR]

**Failure Cause:** Migration Plan M-7 states "Register the new rule in CLAUDE.md + AGENTS.md navigation (H-26)" (`ADR-PROJ031-004-adr-identifier-convention.md:401`). H-26 is defined in `.context/rules/quality-enforcement.md` HARD Rule Index as "Skill description, paths, and registration (WHAT+WHEN+triggers, repo-relative paths, CLAUDE.md+AGENTS.md)" and is elaborated in `.context/rules/skill-standards.md`-style language scoped to *skills*, not generic rule files. No HARD rule in the index actually mandates registering a new `.context/rules/*.md` file in CLAUDE.md's navigation table; that pattern exists as organic convention (CLAUDE.md's Navigation table lists rule files under "Coding/architecture/testing rules | `.context/rules/` (A)"), not as an H-26 obligation.
**Category:** External/Governance
**Likelihood:** Medium.
**Severity:** Minor — the recommended action (register the rule) is still good practice; only the rule citation is inaccurate, which could mislead a future auditor checking "is H-26 satisfied?" against a rule file.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:401` (M-7 citing H-26); `.context/rules/quality-enforcement.md` HARD Rule Index (H-26 definition, skill-scoped).
**Dimension:** Traceability (citation accuracy).
**Mitigation:** Replace the H-26 citation in M-7 with a reference to the CLAUDE.md Navigation convention directly, without implying HARD-rule compulsion that does not exist for rule files.
**Acceptance Criteria:** M-7's citation matches the actual governing convention.

### PM-009: Adoption Action Items Have No Task IDs; PS Integration Still Shows "Pending" [MINOR]

**Failure Cause:** The 8 Adoption Action Items (M-1 through M-8) use role labels ("User," "governance," "devsecops," "docs owner," "adversary") rather than worktracker task IDs (`ADR-PROJ031-004-adr-identifier-convention.md:391-402`), and the PS Integration section — the mechanism that would actually create trackable entries — shows all 3 rows as `Pending` (`:542-546`). Without persisted worktracker Task/Story entities, these action items exist only inside this Markdown file and risk being lost the moment the review session ends, consistent with the general "written but not tracked" pattern already identified in PM-002/PM-003.
**Category:** Resource
**Likelihood:** High.
**Severity:** Minor (compounds, rather than independently causes, PM-002/PM-003; kept separate because it is a distinct process gap — tracking, not enforcement).
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:391-402` (role labels, no IDs); `:542-546` (PS Integration, all "Pending").
**Dimension:** Actionability.
**Mitigation:** Execute the PS Integration commands (`add-entry`, `link-artifact`) and convert M-1 through M-8 into worktracker Tasks with IDs before considering the ADR adopted.
**Acceptance Criteria:** PS Integration rows show completed status with real entry IDs; M-1..M-8 each reference a Task/Story ID.

---

## Recommendations

**P0 (Critical — MUST mitigate before acceptance):**
- PM-001-20260702-s004-i1: Fix the L-1 regex to accept the permitted uppercase dialect forms; dry-run against all 25 live ADR files before merging the lint.
- PM-002-20260702-s004-i1: Create a tracked, owned worktracker Task (+ GH issue) for the L5 lint (M-6) before this ADR's status can move past `PROPOSED`.

**P1 (Important — SHOULD mitigate):**
- PM-003-20260702-s004-i1: Add the `.claude/rules/adr-standards.md` symlink step to the Migration Plan (M-2b).
- PM-004-20260702-s004-i1: Acknowledge the self-referential dialect-choice evidence in the Rationale/Sensitivity section; consider strengthening lint-at-authoring-time enforcement given demonstrated non-self-selection.
- PM-005-20260702-s004-i1: Resolve TBR-2 (name an arbiter/mechanism) and create `docs/design/README.md` as a real, owned action item rather than an optional aside.
- PM-006-20260702-s004-i1: Correct the "Zero cost" claim for framework ADRs; add a tracked frontmatter-retrofit item (M-9) covering all 14 pre-existing ADRs.

**P2 (Monitor — MAY mitigate; acknowledge risk):**
- PM-007-20260702-s004-i1: Clarify L-4's scope regarding entity-embedded dialect ADRs.
- PM-008-20260702-s004-i1: Correct the H-26 citation in M-7.
- PM-009-20260702-s004-i1: Convert action items to worktracker Task IDs; complete the PS Integration entries.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-003, PM-005, PM-007: Migration Plan omits the symlink step, an unresolved taxonomy-arbiter TBR, and incomplete L-4 coverage |
| Internal Consistency | 0.20 | Negative | PM-001, PM-004, PM-006: the lint contradicts the grandfather promise; the author's own filename choice cuts against the document's own evidentiary standard; the "Zero cost" claim contradicts its own required action |
| Methodological Rigor | 0.20 | Neutral | All 6 S-004 steps applicable and executed; the deliverable's own pre-mortem/inversion sections (FM-1..FM-4, S-013 inversion check) are methodologically sound as far as they go — this review's findings extend rather than contradict that existing rigor |
| Evidence Quality | 0.15 | Negative | PM-001, PM-006: direct file-level verification (Glob/Read) shows the spec's own examples and cost claims do not hold against the live repo state |
| Actionability | 0.15 | Negative | PM-002, PM-009: the convention's core enforcement mechanism (the lint) and its adoption tracking are not yet actionable — no owner, no task ID, no timeline |
| Traceability | 0.10 | Negative | PM-008: one mis-cited HARD rule (H-26) in the Migration Plan; otherwise the document's citation discipline is unusually strong (file+line citations throughout) |

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 2
- **Major:** 4
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6 (Set the Stage; Declare Failure/Perspective Shift; Generate Failure Causes across all 5 category lenses; Prioritize P0/P1/P2; Develop Mitigations; Synthesize/Score Impact)
- **H-16 Status:** Satisfied evidentially (prior S-003 output file confirmed to exist; content not read per BLIND PROTOCOL); deliverable also self-embeds steelman reasoning per option.
- **Constitutional Compliance:** P-003 (no subagents spawned); P-020 (no files outside mandate edited — deliverables and other reviewers' findings were not touched); P-022 (every claim above cites a specific file path and, where applicable, a line number; inferences are explicitly labeled as such, e.g., PM-004's confidence framing, the H-16 status note).

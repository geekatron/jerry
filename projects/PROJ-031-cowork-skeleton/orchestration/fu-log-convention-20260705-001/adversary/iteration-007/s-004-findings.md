# Pre-Mortem Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (Design + Staging Package)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, H-16 compliance, failure scenario |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | PM-NNN identifiers, severity, priority |
| [Finding Details](#finding-details) | Full evidence for each finding |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Notes](#execution-notes) | Scope discipline, files read |

## Execution Context

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + 5 files under `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` (`feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md`)
**Criticality:** C4 (gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-004, iteration-007, VERIFIED-CRITICALS protocol, blind round)
**Execution ID:** i007-20260706
**H-16 Compliance:** S-003 Steelman confirmed applied this round — `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-003-findings.md` exists as a sibling blind output (not read, per this round's blind protocol); the project's own Revision Changelog (v1–v9) shows a continuous S-003→S-004 sequence across all prior rounds.
**Failure Scenario:** It is 2027-07-06. The convention shipped, but 12 months of use produced exactly the symptoms it was built to prevent: the live FEEDBACK-LOG's own status banner has been silently wrong for over a year, the install's read-side session-start wiring was never actually verified as complete, and no operator or lint noticed the log body had already outgrown every entry-count the design's own migration plan assumed about it — because those counts were stale on the day the plan was written, and nothing forces a re-check.

## Summary

Applying the temporal-perspective-shift and the 5 failure-category lenses (Technical, Process, Assumption, External, Resource), this Pre-Mortem surfaces **1 Critical and 2 Major failure causes**, all newly identified this round (not raised in any of the 6 prior tournament rounds' finding logs) and all evidenced directly against the current deliverable and its live companion artifacts — not hypothetical projections. The dominant theme: the package's own **install/migration instructions and status banners are already stale relative to the live bootstrap logs they describe**, with no re-verification mechanism to catch this before or at install. This is a live, present-tense instance of exactly the "ids drifted / entries mishandled" failure mode this review round was asked to hunt for, occurring in exactly the artifact class (migration/adoption instructions) that determines whether "entries are never lost." All other candidate failure paths considered this round (concurrent-writer races, Q3 hook non-shipping, single-operator adoption scope, rule-file token-budget overage, discovery-cost/grep-search degradation, segment-index-overflow fallback, `--no-verify` lint bypass, commit-cadence-checkpoint fragility) are already explicitly disclosed in the design doc and/or `restore-notes.md` with accepted-residual framing and are excluded per this review's scope instruction. **Recommendation: REVISE** — all 3 findings are fixable by wording/re-verification-instruction changes; zero new machinery required, consistent with this design's own anti-bloat doctrine.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001 | Design doc's migration entry-count + live FEEDBACK-LOG's status banner are already stale relative to the log's actual body content | Process/Technical | High (already true) | Critical | P0 | Internal Consistency |
| PM-002 | Adoption Plan Step 3's session-start orientation-row edit (the read-side-gap fix) has no owner/acceptance criterion — the promised "(owner + acceptance below)" resolves to a different clause | Process | Medium-High | Major | P1 | Actionability |
| PM-003 | No schema-version marker or migration path for the log format itself once the template is installed across multiple projects, despite the schema having changed materially across all 9 revision rounds | Assumption | Medium | Major | P1 | Completeness |

## Finding Details

### PM-001: Migration instructions and status banner are already stale relative to the live log [CRITICAL]

**Failure Cause:** The design doc's Adoption Plan Step 4 states: *"entries and ids are preserved (FU.0–FU.4, DEC-LLM-001..003 keep their numbers)"* and *"of the **8 live entries** that currently all carry no suffix (FU.0–FU.4, DEC-LLM-001..003)..."* — `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:255`. But the live `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` already contains entries through **FU.11** (`FEEDBACK-LOG.md:165` `## FU.10 diagrams-for-humans`; `FEEDBACK-LOG.md:176` `## FU.11 fu-log-workflow-crashed`) — 12 entries, not 5, and FU.5–FU.9 already carry `(user label: X)` suffixes that Step 4's enumeration doesn't count at all. Separately, the same live file's own status banner reads *"Entries FU.0–FU.9 are real and preserved"* (`FEEDBACK-LOG.md:4`) — itself one full review-round stale relative to its own body (FU.10–FU.11 sit below it, added in the "Review Round: post-tournament (2026-07-06)" section, `FEEDBACK-LOG.md:161-186`). The `LLM-DECISION-LOG.md` side is **not** stale — verified still genuinely 3 entries (`LLM-DECISION-LOG.md:12-14`) — so this is specifically a FEEDBACK-LOG-side drift, not a design-wide one.

**Category:** Process / Technical (a documentation-generation process gap manifesting as a verifiable factual inconsistency)
**Likelihood:** High — this is not a projected future risk; it is **already true today**, verified directly against both live files on the same date (2026-07-06) the RESTORE pass (iteration-007) itself was written.
**Severity:** Critical — this is precisely the "ids drifted / entries mishandled at migration" scenario this review round names. If install proceeds using the literal, enumerated Step-4 instruction ("8 live entries") without an operator independently re-reading the current file, FU.5–FU.11 (more than half the live log) receive no explicit alias-normalization treatment in the *written* migration plan. The general fallback rule ("entries already carrying a `(user label: X)` suffix are renamed in place") does mechanically cover them, but the plan's own worked arithmetic (5 receive `—`, 3 receive re-derived self-labels) is now simply false as a description of "the" live entries, undermining confidence the plan was re-verified before this iteration shipped. This is exactly the propagation-gap class this document has spent 6 rounds fighting (per its own Revision Changelog, SM-002/CV-003/FM-008) — recurring here in a location none of the prior 6 rounds' strategies appear to have checked (entry-count arithmetic against the live artifact), because prior rounds concentrated on the design doc's *internal* consistency, not its consistency against the *external* live files it describes.
**Evidence:** `design/feedback-decision-log-convention-design.md:255` (stale "8 live entries" claim, Adoption Plan Step 4); `FEEDBACK-LOG.md:4` (stale banner "FU.0–FU.9"); `FEEDBACK-LOG.md:165,176` (FU.10, FU.11 exist in the body); cross-checked against `LLM-DECISION-LOG.md:12-14` (DEC-LLM-001-003, confirmed NOT stale, ruling out a design-wide dating error).
**Dimension:** Internal Consistency (0.20) — the deliverable's own migration claim contradicts the live artifact it explicitly cites, verifiable by direct comparison, not interpretation.
**Mitigation:** Replace the hardcoded count and worked example with a **generic, re-derivable rule**: "At install time, re-read the current live log(s) fresh; for every entry already carrying a `(user label: X)` suffix, rename in place to `(alias: X)`; for every entry carrying no suffix, apply [the FU.0/1/2-self-label-vs-`—` logic] entry-by-entry." State any current count only as an illustrative, explicitly dated snapshot (e.g., "as of 2026-07-06, N entries — re-count at install, do not trust this figure"), applying the same "verify against current text, not the finding as stated" discipline `restore-notes.md` Step 1 already established for this project. Fix the FEEDBACK-LOG.md banner to state the current true range, or reword it to be self-relative so it never requires a manual update per entry ("all entries in this file are real and preserved").
**Acceptance Criteria:** Adoption Plan Step 4 no longer states a fixed entry count as fact; it states a re-verification instruction instead. The live FEEDBACK-LOG.md banner's stated range matches its own body's actual last heading at time of edit.

### PM-002: The read-side install action has no accountable owner or acceptance criterion [MAJOR]

**Failure Cause:** Adoption Plan Step 3 (`design/feedback-decision-log-convention-design.md:254`) bundles several install actions into one bullet. The clause *"add `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` to `project-workflow.md`'s session-start 'Before' orientation row"* is immediately followed by the parenthetical **"(owner + acceptance below)"** — but the only "owner: ...; acceptance: ..." text that actually follows in that same sentence belongs to the *next* clause, the L5-lint-wiring action ("owner: the session/engineer executing this install step, tracked as an acceptance criterion on the install work item; acceptance: all three checks are wired AND required..."). No separate owner or acceptance criterion is ever stated for the orientation-row edit itself.
**Category:** Process
**Likelihood:** Medium-High — the same sentence explicitly states this edit is what "closes the read-side gap," making it easy for an install operator to assume it carries the same accountability as the lint-wiring clause immediately beside it, when it does not.
**Severity:** Major — this is the specific mechanism the design doc itself says is required to make "survive session boundaries" mean more than "bytes persist on disk" (design doc L2, Enforcement-layer disclosure). If this one bullet is quietly skipped during an otherwise-complete install (rule file moved, lint wired, templates added — all of which DO carry explicit acceptance criteria elsewhere in the same plan), no acceptance check anywhere would catch the omission, and no future session would ever be instructed to consult the logs — an indefinite, undetected loss of the convention's cross-session value even though every byte of every entry remains intact on disk.
**Evidence:** `design/feedback-decision-log-convention-design.md:254` (full Step 3 bullet, both clauses, showing the dangling forward-reference).
**Dimension:** Actionability (0.15) — an install step lacking a self-contained, verifiable acceptance criterion cannot be demonstrated complete.
**Mitigation:** Add an explicit owner + acceptance clause for the orientation-row edit, mirroring the lint-wiring clause's own pattern, e.g.: "(owner: the install work-item owner; acceptance: `project-workflow.md`'s session-start Before-orientation row names both log file paths, verified present in the same commit that completes install)."
**Acceptance Criteria:** The orientation-row bullet carries its own owner + acceptance text, independently checkable, not a forward reference that resolves to a different bullet's clause.

### PM-003: No schema-version marker or migration path across future template consumers [MAJOR]

**Failure Cause:** The FEEDBACK-LOG / LLM-DECISION-LOG entry schema (fixed field order, id/alias suffix convention, Context sub-fields, redaction carve-out, etc.) has changed materially across every one of the 9 revision rounds recorded in this project's own Revision Changelog (`design/feedback-decision-log-convention-design.md:343-351`). The convention is staged specifically to become a reusable Jerry template (Staged Artifacts table, `design/feedback-decision-log-convention-design.md:327-333`, targeting `.context/templates/`), meaning every future Jerry project will copy this schema at whatever version it happens to be when they adopt it. Nothing in the design — not the entry schema (`staging-feedback-logs/feedback-decision-logs-standards.md:30-32`), not the Context line, not the L5 lint — includes a `schema_version` (or `convention_version`) marker, and no migration guidance exists for reconciling logs created under an earlier template version once the shared template is later revised.
**Category:** Assumption
**Likelihood:** Medium — contingent on (a) the template being adopted by more than one project, and (b) the schema changing again post-install; both are plausible given the schema's own volatility within this single project's history and the template's explicit multi-project distribution design.
**Severity:** Major — this compounds the already-disclosed heading-format-drift lint blind spot (`staging-feedback-logs/feedback-decision-logs-standards.md` L5 Lint scope-limits, item (b)) into a framework-wide problem: at 12 months, if the template is revised (near-certain given 9 rounds of change in year zero alone) and adopted by other projects at various points along that timeline, there is no way — for a human, an LLM, or the ≤3 lint checks — to tell which schema version a given installed log follows, whether an apparent format deviation is corruption or an intentionally-earlier format, or how to safely upgrade an old log in place. This directly threatens "navigable growth" and "honest metadata" at the scale the convention is explicitly designed for (a shared, reusable Jerry convention), not only within PROJ-031.
**Evidence:** `design/feedback-decision-log-convention-design.md:343-351` (9 rounds of material schema change, Revision Changelog); `design/feedback-decision-log-convention-design.md:327-333` (Staged Artifacts destined for `.context/templates/`); `staging-feedback-logs/feedback-decision-logs-standards.md:30-32` (entry schema fields, no version field present); L5 Lint scope-limits item (b) (heading-format drift already disclosed, but not schema-version drift across template revisions).
**Dimension:** Completeness (0.20) — the design omits a category of concern (multi-project schema lifecycle) that its own explicit distribution model (a shared template) makes foreseeable.
**Mitigation:** Add an optional `schema:` trailing Context sub-field (reusing the existing `scope:`/`project:` trailing-tag pattern already established elsewhere in this design — zero new field-shape, zero new lint), stamped at entry-creation time with the rule file's own version (e.g., `feedback-decision-logs-standards.md@1.0`). Add one sentence to the Governance & Migration section disclosing that per-project logs are validated against the schema version active at their own install time and are not automatically migrated on template upgrade — either accepted as a disclosed residual (consistent with this design's anti-bloat doctrine) or scoped as a v2 follow-up.
**Acceptance Criteria:** Either (a) a `schema:`-tag field is added to the Context-line convention across the rule file + both templates, or (b) the Governance & Migration section explicitly names schema-version drift across future template consumers as a disclosed, accepted residual — parallel to how Q5 (silent non-capture) was explicitly elevated from a scope-note aside to a full ratification item earlier in this same design.

## Recommendations

**P0 (MUST mitigate before acceptance):**
- **PM-001** — Replace the stale entry-count claim and worked migration example in Adoption Plan Step 4 with a re-derivable rule plus an explicit "re-verify against the current live file at install time" instruction; correct the FEEDBACK-LOG.md banner to match its own body (or reword it to be self-relative so it cannot go stale again).

**P1 (SHOULD mitigate):**
- **PM-002** — Add a self-contained owner + acceptance criterion to the session-start orientation-row install bullet (Adoption Plan Step 3), independent of the neighboring lint-wiring clause.
- **PM-003** — Add a `schema:`-tag Context sub-field (or explicitly disclose schema-version drift across future template consumers as an accepted residual) ahead of this convention becoming a shared, multi-project `.context/templates/` artifact.

**P2 (MAY mitigate; acknowledge risk):** None raised this round. All other candidate failure paths considered (concurrent-writer races, Q3 hook non-shipping, single-operator adoption scope, rule-file token-budget overage, discovery-cost/grep-search degradation on search, segment-index overflow, `--no-verify` lint bypass, commit-cadence-checkpoint fragility) are already explicitly disclosed in the design doc and/or `restore-notes.md` with accepted-residual framing consistent with the MEDIUM-tier posture; they are excluded from this report per this review round's own scope instruction (already-disclosed residuals are not findings).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-003: a multi-project schema-lifecycle concern foreseeable from the design's own stated distribution model, left unaddressed |
| Internal Consistency | 0.20 | Negative | PM-001: the design doc's own migration claim, and the live bootstrap file's own status banner, both contradict the live artifact body they describe, verifiable by direct comparison |
| Methodological Rigor | 0.20 | Negative | PM-001: the "verify against current text, not the finding as stated" discipline `restore-notes.md` Step 1 itself established for this project was not applied to the design doc's own migration-count claim |
| Evidence Quality | 0.15 | Negative | PM-001: the cited entry counts are stale and unverified against the current state of the artifact they describe |
| Actionability | 0.15 | Negative | PM-002: an install step with a dangling owner/acceptance forward-reference cannot be verified complete |
| Traceability | 0.10 | Neutral | All 3 findings trace cleanly to specific file+line evidence in both the deliverable and its live companion artifacts; the deliverable's own traceability apparatus (Revision Changelog, References) functioned correctly in enabling this cross-check |

## Execution Notes

- **Scope discipline applied:** Per this review round's brief, previously-disclosed residuals (concurrent-writer risk, Q3 hook timing, single-operator scope, rule-file token-budget overage, discovery-cost/grep-search degradation, segment-index-overflow fallback, `--no-verify` lint bypass, commit-cadence-checkpoint single-point-of-failure) were reviewed against the current text and explicitly excluded — each is named and accepted in the design doc / `restore-notes.md`, not a silent gap.
- **Novel this round:** All 3 findings above concern the deliverable's consistency against artifacts *external* to the design doc itself (the live bootstrap `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md`, and the install plan's own internal cross-references) — a check angle not evidenced in the 6 prior rounds' finding logs, which concentrated on the design doc's *internal* claims.
- **Files read for this execution:** S-004 template (Identity + Execution Protocol); design doc (full, both reads); all 5 staging files (full); live `FEEDBACK-LOG.md` and `LLM-DECISION-LOG.md` (full — read for cross-verification only, not deliverables under review); `restore-notes.md` (iteration-007, permitted per blind protocol as the owner's disposition record). `s-003-findings.md` (iteration-007) was **not** read, per this round's blind protocol.

---

*Template: `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0*
*Strategy: S-004 Pre-Mortem Analysis*
*Agent: adv-executor*

## Execution Statistics

- **Total Findings:** 3
- **Critical:** 1
- **Major:** 2
- **Minor:** 0
- **Protocol Steps Completed:** 6 of 6 (Set the Stage; Declare Failure/Perspective Shift; Generate Failure Causes across all 5 category lenses; Prioritize by Likelihood x Severity; Develop Mitigations; Synthesize and Score Impact)

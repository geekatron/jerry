# Constitutional Compliance Report: ADR-PROJ031-004 + adr-standards-rule-draft.md

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95, raised above SSOT 0.92)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-007, iteration 1, blind independent reviewer)
**Constitutional Context:** `docs/governance/JERRY_CONSTITUTION.md` (P-001–P-022 verified), `.context/rules/quality-enforcement.md` (SSOT), `.context/rules/skill-standards.md` (H-25/H-26), `.context/rules/markdown-navigation-standards.md` (H-23/H-24), `.context/rules/agent-development-standards.md`, `.context/rules/mcp-tool-standards.md`

> **STATUS: COMPLETE.**

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings, severity-classified |
| [Finding Details](#finding-details) | Full evidence and remediation per finding |
| [Compliant Checks](#compliant-checks) | Constitutional/HARD-rule checks that PASS |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Constitutional Compliance Score](#constitutional-compliance-score) | S-007 Step 5 calculation |

---

## Summary

**PARTIAL compliance.** 1 Critical, 2 Major, 1 Minor finding. The most severe finding (CC-001) is a self-contradicting enforcement specification: the proposed L5 CI lint's own L-1 "Form" regex is documented (in both deliverables) as rejecting **uppercase** filenames, which would FAIL-block every existing "grandfathered" project-scoped dialect ADR (`ADR-PROJ031-*`, `ADR-EPIC002-*`, `ADR-STORY015-*`, `ADR-150-*`) the moment the lint is wired into CI — directly contradicting the decision's own D-3 ("dialect is PERMITTED") and D-4/c-003 ("grandfather in place; MUST NOT big-bang renumber"). Two Major findings concern P-022 honesty/traceability: an H-26 citation is misapplied to justify a rule-file registration action (H-26 governs skill registration, not rule files), and the rule draft's normative text asserts present-tense lint enforcement while the Migration Plan sequences authoring the rule file (M-2) before building the lint (M-6), creating a window in which the installed rule would overclaim enforcement that does not yet exist. MEDIUM-tier purity (zero HARD-vocabulary in the rule draft) and H-23 navigation-table compliance both PASS cleanly in both documents. **Recommendation: REVISE** — fix the L-1 regex before ratification; the other findings are lower-cost precision fixes.

---

## Findings Table

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CC-001-20260702i1 | Critical | L-1 lint regex rejects uppercase, self-contradicting the permitted/grandfathered dialect (D-3/D-4/c-003) | Enforcement Design (L5 CI Lint) / L5 CI Lint Specification |
| CC-002-20260702i1 | Major | H-26 cited as authority for registering a new *rule file* in CLAUDE.md/AGENTS.md; H-26 governs *skill* registration only | Migration Plan, M-7 |
| CC-003-20260702i1 | Major | Rule draft asserts present-tense lint enforcement while Migration Plan sequences rule-file authoring (M-2) before lint build (M-6) — P-022 overclaim window | Tier and Scope; Migration Plan |
| CC-004-20260702i1 | Minor | Criticality "C4" attributed to AE-002+AE-003, both of which the SSOT defines as "Auto-C3 minimum," not C4 | ADR header (Criticality line) |

---

## Finding Details

### CC-001-20260702i1: L-1 Lint Regex Self-Contradicts the Permitted/Grandfathered Dialect [CRITICAL]

**Principle:** Internal Consistency / Methodological Rigor (S-014 dimensions); c-003 ("MUST NOT big-bang renumber frozen legacy sets... grandfather"); D-3 ("project-scoped dialect... PERMITTED"); D-4 ("existing scope-prefixed... ADRs are grandfathered in place")

**Location & Evidence:**

1. `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:69` — "Regex (canonical + dialect, for lint L-1): `^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$`."
2. `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:177` — L-1 table row: "Filenames match `^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$` | Malformed IDs, uppercase, bad sequence | `projects/*/decisions/`, `docs/design/`" (FAIL class).
3. `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:468` — the parent ADR's own L-1 row states, in the "Rejects" column: "Malformed IDs; **uppercase**; missing/oversized sequence" — the document explicitly confirms uppercase is a rejection target of this FAIL-class rule.
4. `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:65` and `decisions/ADR-PROJ031-004...md:265-267` — the same documents define the PERMITTED dialect grammar as `ADR-{PROJECT-ID}-NNN` where `PROJECT-ID : PROJ\d{3}` (or `EPIC\d{3}`, `STORY\d{3}`) — i.e., uppercase by definition (`PROJ031`, `EPIC002`, `STORY015`), consistent with Jerry's framework-wide entity-ID convention (`PROJ-031`, `EPIC-002`, uppercase throughout `.context/rules/project-workflow.md` and `quality-enforcement.md`).
5. `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:380-389` (Migration Plan table) — the existing 11+ project/entity-scoped ADRs (`PROJ010`×6, `PROJ022`×2, `PROJ031`×3, `EPIC002`×2, `STORY015`×1, GH-issue `150`×1) are all located in `projects/*/decisions/` — exactly the directory scope L-1 checks (`Where: projects/*/decisions/, docs/design/`) — and the plan's stated Action for this set is "**Grandfather in place.** Valid dialect... Zero [cost]" (line 383).

**Analysis:** L-1 is a FAIL-class rule (blocks CI, per the rule draft's own tier framing at `adr-standards-rule-draft.md:173`) applied to exactly the two directories (`projects/*/decisions/`, `docs/design/`) where the grandfathered and newly-permitted dialect ADRs live. Because the regex's character class is `[a-z0-9]` (lowercase only, no `A-Z`, no case-insensitive flag), and the parent ADR itself states the rule rejects "uppercase," every dialect filename this same decision commits to preserving (D-4, "no big-bang renumber... grandfather in place") or permitting going forward (D-3, "MAY use the project-scoped dialect `ADR-{PROJECT-ID}-NNN`") would fail L-1 the moment it is wired into CI (M-6). This is not a hypothetical edge case — it is the majority of the existing corpus (11 of ~14 non-frozen ADRs) and the explicitly-endorsed dialect path for future tactical ADRs. The self-contradiction directly undermines Internal Consistency and Methodological Rigor: the enforcement mechanism, as literally specified, would violate the very no-big-bang / grandfather / permitted-dialect commitments the decision text repeatedly asserts as core to its low-regret design. This also creates an unacknowledged operational cost (every dialect ADR needing an `adr-lint: ignore L-1` override from day one) that is not mentioned in Consequences, Risks (R-1 through R-5), or the Pre-Mortem (FM-1 through FM-4) sections — despite those sections being otherwise unusually thorough about failure modes.

**Impact:** If M-6 (build + wire the L5 lint) is implemented literally as specified, CI would immediately FAIL on the majority of the existing ADR corpus and on every future dialect ADR, contradicting D-3/D-4/c-003. This would force either (a) blanket override annotations across ~11+ files at rollout (an unplanned, unbudgeted migration cost the document explicitly claims is "Zero" for this set), or (b) a silent, un-reviewed rewrite of the lint spec at implementation time, bypassing the C4 governance this ADR itself is undergoing.

**Recommendation:** Fix the L-1 regex to accept both grammars explicitly, e.g. two alternative branches: canonical (`^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$`) OR dialect (`^ADR-(PROJ|EPIC|STORY)\d{3}-\d{3}(-[a-z0-9-]+)?\.md$` plus the GH-issue form `ADR-\d+-\d{3}...`), and remove "uppercase" from the L-1 "Rejects" column (or scope it explicitly to "uppercase outside the permitted dialect prefixes"). Add an explicit test case to the L5 Lint Specification enumerating at least one grandfathered filename (e.g., `ADR-PROJ031-001-*.md`) that MUST pass L-1.

---

### CC-002-20260702i1: H-26 Misapplied as Authority for Rule-File Registration [MAJOR]

**Principle:** P-022 (No Deception — accurate representation of what governance rules require); P-004 (Explicit Provenance — citations must be accurate); Traceability (S-014 dimension)

**Location & Evidence:**
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:401` — Migration Plan table: "| M-7 | Register the new rule in CLAUDE.md + AGENTS.md navigation (H-26) | governance | Yes |" (marked as a **Gating** adoption action item).
- `.context/rules/skill-standards.md` HARD Rules section: "H-26 | **Skill description, paths, and registration:** (a) Frontmatter `description` MUST include WHAT + WHEN + trigger phrases...; (b) All file references in SKILL.md MUST use full repo-relative paths; (c) **New skills** MUST be registered in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md (if proactive per H-22)." (emphasis added — scoped explicitly to skills).
- `.context/rules/quality-enforcement.md` HARD Rule Index: "H-26 | Skill description, paths, and registration (WHAT+WHEN+triggers, repo-relative paths, CLAUDE.md+AGENTS.md) | skill-standards" — source and scope both confirm H-26 is a skill-registration rule, not a rule-file-registration rule.
- `CLAUDE.md` Navigation table: rules are referenced via a single directory-level row — "Coding/architecture/testing rules | `.context/rules/` (A)" — there is no established per-rule-file CLAUDE.md registration convention that M-7 could be citing as an existing pattern either.

**Analysis:** H-26 is textually and structurally scoped to *skills* (frontmatter description quality, file-path format inside `SKILL.md`, and new-*skill* registration in CLAUDE.md/AGENTS.md/mandatory-skill-usage.md). `adr-standards.md` is a `.context/rules/` file, not a skill, so H-26 does not actually mandate its CLAUDE.md/AGENTS.md registration. Citing a HARD rule (H-26, Tier A, non-overridable) as the authority for a "Yes"-gating adoption action item overstates the governance backing of that action — a future implementer or reviewer could reasonably conclude this step is HARD-rule-mandated (and therefore non-negotiable/blocking) when in fact no such HARD rule applies to rule files. This is precisely the category of overclaim the task's review criteria asks to check for (P-022: no overclaims about enforcement).

**Recommendation:** Either (a) remove the "(H-26)" citation and justify M-7 purely on H-23/discoverability/NAV-002 grounds (a rule file benefiting from a CLAUDE.md navigation pointer is a reasonable MEDIUM-tier practice, just not an H-26 HARD mandate), or (b) if the intent is to establish a *new* convention that all `.context/rules/*.md` files get an explicit CLAUDE.md row (departing from the current directory-level pattern), state that explicitly as a new proposal rather than attributing it to an existing HARD rule that does not cover it.

---

### CC-003-20260702i1: Enforcement-Claim Timing Gap Between Rule-File Authoring (M-2) and Lint Build (M-6) [MAJOR]

**Principle:** P-022 (No Deception — capabilities/actions must not be overstated); P-001 (Truth and Accuracy)

**Location & Evidence:**
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:11` (Tier and Scope blockquote): "Enforced by deterministic L5 CI lint, not a HARD invariant."
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:37` (Tier and Scope body): "Enforcement is deterministic L5 CI lint (fail/warn classes below) plus L4 advisory — never a HARD block." (present tense, unconditional)
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:396` — Migration Plan: "| M-2 | Author `.context/rules/adr-standards.md` from Deliverable 2... | ps-architect / governance | Yes |"
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:400` — "| M-6 | Implement + wire the L5 CI lint (`scripts/lint_adr_convention.py`) into CI | devsecops | **Yes** (prevents FM-1) |" — listed four rows *after* M-2, with no explicit dependency ordering that forces M-6 before M-2.
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:357` (Risks table): "R-5: Lint never gets built; convention stays advisory-only | MED | HIGH | Adoption action item makes the lint a gating deliverable, not optional (see Migration Plan)" — this risk is explicitly acknowledged in the parent ADR.
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:3-5` (wrapper note) — references only "Migration Plan M-2/M-7" as the ratification gate; M-6 (the lint itself) is not mentioned as a co-requisite for the enforcement claims made in the body text below.

**Analysis:** The rule-file text (which becomes the actual normative `.context/rules/adr-standards.md` content per the wrapper note) states as an unconditional, present-tense fact that the convention "is" enforced by a deterministic L5 CI lint. But the Migration Plan's own ordering places authoring that file (M-2) before building the lint (M-6), and nothing in either document requires M-6 to complete before M-2's output is installed. If M-2 executes first (as its position in the ordered table suggests), the installed rule file would assert an enforcement mechanism that does not yet exist — an overclaim about current enforcement state, which is exactly the honesty failure mode P-022 and this review's explicit "no overclaims about enforcement or adoption" instruction target. The parent ADR's own R-5 risk entry shows the author is aware the lint might never get built, which makes the rule file's unconditional "Enforcement is..." phrasing (rather than a hedged "Enforcement is designed to be..." or "...pending M-6") a material precision gap, not a hypothetical one.

**Recommendation:** Either (a) resequence the Migration Plan so M-6 (lint) is a hard prerequisite of M-2 (rule-file authoring) — i.e., do not install the normative text until the enforcement mechanism it describes exists — or (b) hedge the rule-file's enforcement language (e.g., "Enforcement is designed to be deterministic L5 CI lint... (see rollout status in the parent ADR's Migration Plan; until M-6 completes, this file is advisory-only via L4 review)") so the installed text is accurate at every point in the rollout, not only after M-6 completes.

---

### CC-004-20260702i1: C4 Criticality Attributed to AE-002+AE-003, Which Only Mandate "Auto-C3 minimum" [MINOR]

**Principle:** Traceability (S-014 dimension); consistency with `quality-enforcement.md` Auto-Escalation Rules

**Location & Evidence:**
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:8` — "> **Criticality:** C4 (framework-wide governance; AE-002 rules-dir + AE-003 new-ADR auto-escalation)"
- `.context/rules/quality-enforcement.md` Auto-Escalation Rules table: "AE-002 | Touches `.context/rules/` or `.claude/rules/` | **Auto-C3 minimum**" and "AE-003 | New or modified ADR | **Auto-C3 minimum**" — both rules, individually and (per the SSOT text) without any documented compounding/stacking mechanism, mandate only a C3 floor, not C4.

**Analysis:** Citing AE-002 and AE-003 as the justification for C4 slightly overstates what those specific auto-escalation rules require — both are explicitly "Auto-C3 minimum" in the SSOT, with no stacking rule defined anywhere in `quality-enforcement.md` that two simultaneous Auto-C3-minimum triggers compound to C4. The ADR's C4 classification is very likely independently justified by the C4 tier's own definition ("architecture/governance/public," matching the C4 row of the Criticality Levels table), but the parenthetical citation reads as though AE-002/AE-003 themselves mandate C4, which they do not. This does not constitute an under-escalation (C4 exceeds the C3 floor, which is permitted), so no governance rule is actually violated — this is a citation-precision issue only.

**Recommendation:** Reword to: "C4 (framework-wide governance and public-facing convention change, independently meeting the C4 tier definition; AE-002/AE-003 additionally mandate a C3 floor)" so the auto-escalation citation is not misread as itself requiring C4.

---

## Compliant Checks

The following checks PASS with no finding, evidenced explicitly because the task instructions called them out for verification:

| Check | Result | Evidence |
|---|---|---|
| MEDIUM-tier purity (zero HARD-vocabulary: MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL) in the rule draft | **PASS** | Grep of `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` for `MUST\|SHALL\|NEVER\|FORBIDDEN\|REQUIRED\|CRITICAL` returns zero matches; the draft consistently uses SHOULD/RECOMMENDED/MAY/PERMITTED |
| No new HARD rule added; HARD ceiling (25/25) undisturbed | **PASS** | `adr-standards-rule-draft.md:5` explicitly states "No HARD (H-NN) rule is proposed"; `.context/rules/quality-enforcement.md` confirms current count is 25/25 with the new standards using the `ADR-M-###` prefix (MEDIUM, unlimited count per Tier Vocabulary) |
| H-23 navigation table present, with anchor links (H-24), in both deliverables | **PASS** | ADR: `ADR-PROJ031-004-adr-identifier-convention.md:15-42` (22 rows, all `##` headings covered, anchors verified against GitHub slug rules incl. punctuation-heavy headings like "Options Considered (A–F)" → `#options-considered-af`); rule draft: `adr-standards-rule-draft.md:13-29` (13 rows, all headings covered) |
| P-022 honesty on status/pending items | **PASS** | PS Integration table entries explicitly marked "Pending" (`ADR-PROJ031-004...md:544-546`); Meta-Note explicitly labels the promotion path as "inference about the intended end-state, not an action taken" (`:503`); References section carries an explicit "P-022 disclosures" block (`:536`) correcting a factual error in a cited source (BUG-006 F-002) rather than silently relying on it |
| Constitutional principle citations (P-001, P-002, P-003, P-004, P-011, P-020, P-022) resolve to real, correctly-numbered principles | **PASS** | Verified against `docs/governance/JERRY_CONSTITUTION.md` lines 30-188 (P-001 Truth/Accuracy, P-002 File Persistence, P-003 No Recursive Subagents, P-004 Explicit Provenance, P-011 Evidence-Based Decisions, P-020 User Authority, P-022 No Deception all exist with matching names) |
| MEDIUM-standard ID-prefix collision risk (`ADR-M-###` vs. actual `ADR-{slug}-NNN` identifiers) proactively disambiguated | **PASS** | `adr-standards-rule-draft.md:5` explicitly states these are "standard IDs internal to this rule file, not ADR identifiers" and explains why the L5 lint (filename-scoped) will never confuse them |
| Citation spot-checks against primary sources | **PASS** | `skills/architecture/SKILL.md:105,284,437` (`ADR_NNN`/`ADR_001_sqlite_persistence.md` underscore pattern), `docs/knowledge/exemplars/templates/adr.md:1,6,159-163,182` (bare `ADR-{NUMBER}` placeholder, missing `REJECTED` status, `SUPERSEDES/DEPENDS_ON/RELATED_TO` table, dangling `docs/decisions/` path), and `docs/design/ADR-agent-design-001.md:3` (`PS-ID: PROJ-007 \| ENTRY: e-004` comment) all match the deliverables' quoted excerpts exactly |

---

## Remediation Plan

**P0 (Critical):** CC-001 — Fix the L-1 lint regex to accept the uppercase `PROJ\d{3}`/`EPIC\d{3}`/`STORY\d{3}` dialect forms before this ADR is ratified; add a grandfathered-filename test case to the L5 Lint Specification.

**P1 (Major):** CC-002 — Remove or correct the "(H-26)" citation on Migration Plan M-7. CC-003 — Either resequence M-6 before M-2, or hedge the rule draft's enforcement language to reflect pending-implementation status until M-6 completes.

**P2 (Minor):** CC-004 — Reword the Criticality line so AE-002/AE-003 are cited as a C3 floor, not as the source of the C4 classification.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No findings affect topical completeness; both documents cover the full scope of an ID/location/promotion convention |
| Internal Consistency | 0.20 | Negative | CC-001 (Critical): the L-1 enforcement spec directly contradicts D-3/D-4/c-003 within the same document set |
| Methodological Rigor | 0.20 | Negative | CC-001 (Critical): an enforcement mechanism that would fail its own grandfather guarantee is a rigor defect; CC-004 (Minor): imprecise auto-escalation citation |
| Evidence Quality | 0.15 | Negative | CC-002, CC-003 (Major): citations/claims that overstate governance backing or current enforcement state |
| Actionability | 0.15 | Negative | CC-003 (Major): ambiguous/unhedged Migration Plan ordering leaves an actionable gap for implementers |
| Traceability | 0.10 | Negative | CC-002 (Major), CC-004 (Minor): rule citations do not trace cleanly to the rules they invoke |

---

## Constitutional Compliance Score

Per S-007 Step 5 penalty model (template-operational, not the SSOT 0.92 threshold itself):

- Critical violations: 1 → -0.10
- Major violations: 2 → -0.10
- Minor violations: 1 → -0.02
- **Score = 1.00 − (0.10×1 + 0.05×2 + 0.02×1) = 1.00 − 0.22 = 0.78**

**Threshold Determination:** REJECTED (< 0.85 SSOT band; also below both the SSOT 0.92 gate and the engagement's raised 0.95 gate). Primary driver is CC-001 (Critical); CC-002/CC-003 (Major) compound the gap. Recommend fixing CC-001 first — it is a self-contained, verifiable defect (regex correction + one test case) — and the score should recover substantially once corrected, leaving the two Major P-022/traceability findings as the residual gate to close.

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 1
- **Major:** 2
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Load Constitutional Context; Enumerate Applicable Principles; Principle-by-Principle Evaluation; Remediation Guidance; Score Constitutional Compliance)

**Blind protocol compliance:** No file under `orchestration/adr-convention-20260702-001/adversary/` was read except this output file. No deliverable was edited. All factual claims above are cited to file+line evidence gathered from the two deliverables under review, `.context/rules/*.md`, `docs/governance/JERRY_CONSTITUTION.md`, `skills/architecture/SKILL.md`, `docs/knowledge/exemplars/templates/adr.md`, `docs/design/ADR-agent-design-001.md`, and `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/explore/advocate-domain-slug.md` (permitted evidence per the task's explore/ allowance).

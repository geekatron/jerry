# FMEA Report: ADR-PROJ031-004 + Companion Rule Draft (Post-Subtraction-Pass, Iteration 8)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, protocol note |
| [Protocol Disclosure](#protocol-disclosure-p-022) | A blind-protocol scope deviation, disclosed honestly |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All 7 findings, RPN-ranked |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions (disclosure-only, doctrine-consistent) |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Totals |

---

## Execution Context

- **Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
- **Template:** `.context/templates/adversarial/s-012-fmea.md`
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.9, 774 lines)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.9, 242 lines)
- **Criticality:** C4 | **Engagement gate:** 0.95
- **Executed:** 2026-07-06
- **H-16 Compliance:** S-003 Steelman is embedded in Options A–F (ADR:65-68, `ST-001`/`ST-002` tags) rather than filed as a separate artifact — the ADR itself discloses this honestly at ADR:67. Treated as satisfied for this C3+ sequence per the template's Prerequisites note.
- **Scope directive honored:** Per the invoking task, this execution evaluates the package **as slimmed** by the user-authorized subtraction pass (`subtraction-pass-notes.md`) and does **not** re-demand deleted machinery (waiver ledger, two-tier ratification, 13 deleted lint rules, CODEOWNERS gate). Findings below are either (a) genuinely new defects in the current text, or (b) disclosed-residual RPN estimates offered for prioritization only, explicitly labeled as such.
- **Elements analyzed:** 8 (Creation, Cross-Reference/Citation, Amendment, Supersession, Promotion Path 1, Promotion Path 2/Self-Promotion, 5-Rule L5 Lint + Grandfather Regression Test, Onboarding)
- **Failure modes identified:** 7 | **Total RPN:** 1,588

---

## Protocol Disclosure (P-022)

Before scoping subsequent searches to the two deliverables, one unscoped `Grep` call in this session searched the entire `PROJ-031-cowork-skeleton` directory and returned matching lines from files under `orchestration/adr-convention-20260702-001/adversary/iteration-004/`, `iteration-005/`, and `iteration-006/` (prior strategy findings/remediation-notes) — a violation of the blind-review instruction to read nothing under `adversary/` except this file. This is disclosed rather than concealed. **No finding in this report relies on or cites content from those prior-iteration files.** All findings below are sourced exclusively from the two deliverables themselves, `subtraction-pass-notes.md` (explicitly permitted), and directly-cited repo files (`ADR-PROJ031-002`, `ADR-PROJ031-003`, both permitted as general repo evidence). Subsequent tool calls were scoped to specific files to prevent further exposure.

---

## Summary

The post-subtraction package is methodologically strong on the axes the subtraction pass targeted (lint rule count, waiver machinery, tier-language purity) but this FMEA surfaces **three Critical, currently-live internal-consistency defects** that survived seven prior remediation passes: (1) the grandfather-regression-test file count is **self-contradictory within the same document** (D-4 says 16 dialect files including this ADR; three other passages say 15, excluding it — for the identical test, describing the identical current state); (2) the L-7 relationship lint's real-world validation surface is **empty at ship time** for this very project's own already-existing supersession relationship (`ADR-PROJ031-002` → `ADR-PROJ031-003`), because neither sibling ADR carries the YAML frontmatter L-7 requires, and `M-11`'s retrofit list does not include them; and (3) a **cross-branch concurrent-supersession race** — the supersession-lifecycle analog of the already-disclosed `R-6` creation-time race — is undisclosed. All three are genuine defects in the current (v1.9) text, not re-litigations of deleted machinery, and all three have cheap, disclosure-only (not new-machinery) corrective actions consistent with the subtraction doctrine. Four Major/Minor findings round out gaps in scope-determination guidance, supersession-race disclosure symmetry, downstream fallback cross-referencing, and the now-content-free Onboarding element. **Recommendation: REVISE** — none of the findings invalidate Scheme B or demand restored machinery, but FM-001 and FM-002 must be reconciled before the M-6 lint build (which depends on an unambiguous grandfather-test target set) can proceed correctly.

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260706iter008 | 5-Rule Lint / Grandfather Regression Test | Grandfather regression-test file count is self-contradictory: D-4 asserts 16 dialect files (incl. this ADR); M-6 row, Enforcement Design, and rule-draft L5 spec all assert 15 (excl. this ADR) for the identical test | 7 | 10 | 8 | 560 | Critical | Reconcile D-4's "16-file… matching the rule draft's regression test" claim with the current 15+3=18 figure (or vice versa); text-only edit | Internal Consistency |
| FM-002-20260706iter008 | Supersession / 5-Rule Lint | L-7 (YAML-only parser) has zero real targets in this project's own live supersession relationship (`ADR-PROJ031-002`→`ADR-PROJ031-003`, blockquote-only, no YAML); M-11's retrofit list omits `ADR-PROJ031-001/002/003` | 6 | 9 | 7 | 378 | Critical | Disclose the gap explicitly at L-7/M-11 (name the sibling ADRs); no new lint required | Methodological Rigor |
| FM-003-20260706iter008 | Supersession | Cross-branch concurrent-supersession race (two branches each author a distinct successor for the same predecessor) is undisclosed — the supersession analog of the disclosed `R-6` creation-race | 7 | 4 | 8 | 224 | Critical | Add a parallel disclosed residual (R-14-style) mirroring R-6's framing; disclosure only, no lint | Completeness |
| FM-004-20260706iter008 | Creation / Promotion Path 1 | Rule draft's Promotion Process omits the ADR's own framework-scope determination criteria ("rules/, agents, routing, enforcement, cross-project standards") | 4 | 6 | 6 | 144 | Major | Copy the one-clause criteria from ADR Path-1-step-1 into the rule draft's Promotion Process | Completeness |
| FM-005-20260706iter008 | Onboarding | Onboarding element carries zero dedicated content (deleted section, disclosed at M-14, not restored); no consolidating entry point or forward-pointer exists for a first-time reader | 4 | 5 | 6 | 120 | Major | Add a one-line forward-pointer in the nav table or Tier-and-Scope section: "New authors: read ID Scheme → Location Model → ADR-M-001…013 in that order" | Actionability |
| FM-006-20260706iter008 | 5-Rule Lint / Onboarding | Enforcement Scope/Deployment-Targets table doesn't cross-reference the already-specified, zero-tooling pre-flight collision one-liner as a today-usable downstream fallback (frames the fallback as gated on unbuilt M-13) | 3 | 6 | 6 | 108 | Major | Add one sentence to the Deployment Targets table/paragraph naming the pre-flight one-liner as available today, independent of M-13 | Actionability |
| FM-007-20260706iter008 | Amendment | No threshold/guidance for when repeated in-body `AMENDED` blocks should trigger mandatory supersession review instead of accruing indefinitely | 3 | 3 | 6 | 54 | Minor | Optional SHOULD-NOT guidance note (e.g., "3+ amendments SHOULD prompt a supersession review") | Methodological Rigor |

---

## Finding Details

### FM-001-20260706iter008: Grandfather Regression-Test File Count Self-Contradiction

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 560) |
| **Element** | 5-Rule Lint / Grandfather Regression Test (E7), interacting with Self-Promotion (E6) |
| **S / O / D** | 7 / 10 / 8 |

**Evidence:**

- `ADR-PROJ031-004-adr-identifier-convention.md:223` (D-4): *"There are 16 live `ADR-PROJ*/EPIC*/STORY*/150` dialect ADRs (15 pre-existing + this ADR; filesystem-verified 2026-07-02)... **This ADR is the one disclosed exception to "in place"**: it is **counted in the 16-file regression corpus** because its current filename is a valid dialect..."*
- Same file, `:223` continues: *"the **16** is the *entire* dialect corpus (project-ID + entity-ID + GH-issue + this ADR), matching this ADR's own [Migration Plan] enumeration and **the rule draft's regression test**"* — D-4 explicitly asserts its 16-count matches the rule draft.
- `ADR-PROJ031-004-adr-identifier-convention.md:522` (M-6 row): *"grandfather regression test green (**15 dialect reachable** + 3 canonical = 18 files pass L-1... figure reconciled to match the Enforcement-Design section and the rule draft, FM-002-iter7)"*
- `ADR-PROJ031-004-adr-identifier-convention.md:672` (Enforcement Design): *"the **18 files reachable by the scan path** (**15 dialect files** in decisions/ dirs + 3 canonical `docs/design/` ADRs) pass L-1"*
- `adr-standards-rule-draft.md:179`: *"the **18 files reachable by the scan path** (15 dialect files in `decisions/` dirs + 3 canonical framework ADRs) pass L-1"*
- `adr-standards-rule-draft.md:94`: *"Of the **16-file dialect corpus** + 3 canonical ADRs, the **18 reachable** by the scan path pass the grandfather regression test; the entity-embedded `ADR-STORY015-001` is out-of-scan"* — this passage's own family breakdown (`PROJ031×4` = includes this ADR) totals 16, and reconciles to 18 via a **different** arithmetic path (16 + 3 − 1 out-of-scan STORY015 = 18) than the M-6/Enforcement-Design/L5-spec passages (15 + 3 = 18, no subtraction).

**Analysis:** This file (`ADR-PROJ031-004-adr-identifier-convention.md`) currently resides at `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` — inside the exact `projects/*/decisions/` scan path L-1/L-3/L-7 use — and its filename (`ADR-PROJ031-004`) matches the dialect grammar. Since M-9 (this ADR's own Path-2 self-promotion, renaming it out of the dialect) is explicitly **not yet executed** (Claim-Status: TBD-Task, ADR:511), this ADR is, right now, a 16th reachable dialect file. D-4 says so directly ("counted in the 16-file regression corpus"). But the M-6 row, the Enforcement Design section, and the rule draft's L5 spec all use "15 dialect... reconciled... FM-002-iter7" — a figure that, per D-4's own definition of "15 pre-existing," **excludes** this ADR. Both cannot be correct for the same artifact describing the same pre-M-9 state. The rule draft's *own* "Frozen and Grandfathered Legacy" section (line 94) independently arrives at 16 dialect files (agreeing with D-4) via an explicit family count (`PROJ031×4`), then reconciles to 18 through a *third*, mutually-exclusive arithmetic path. This is exactly the class of same-document numerical contradiction that iterations 6–7 fixed for the 19→18 total (per FM-002-iter7's own citation) — but that fix appears to have updated three passages while leaving D-4's "16… matching the rule draft" claim stale, and D-4's own claim of cross-document agreement is therefore **currently false**. This will directly affect M-6's implementer: building the regression test to "15 dialect files" vs "16 dialect files" produces two different, non-interchangeable fixtures.

**Corrective Action:** Text-only edit, consistent with subtraction doctrine (no new machinery): either (a) update D-4 to say "15 pre-existing dialect files are reachable pre-M-9; this ADR is additionally reachable until M-9 executes, making the current live count 16, of which the regression test's frozen target is 15 (i.e., the post-M-9 steady state)" — i.e., explicitly date-stamp which figure describes which point in time; or (b) drop D-4's "matching the rule draft's regression test" claim since it is not currently true. Either resolves the contradiction without adding a rule, ledger, or gate.

**Acceptance Criteria:** All four cited passages (D-4, M-6 row, Enforcement Design, rule-draft L5 spec, rule-draft Frozen/Grandfathered Legacy) state the same file count via the same arithmetic, or explicitly and consistently distinguish pre-M-9 vs. post-M-9 counts.

**Post-Correction RPN estimate:** ~40 (S=4 residual confusion risk if only partially reconciled, O=2, D=5).

---

### FM-002-20260706iter008: L-7's Real Validation Surface Is Empty — This Project's Own Supersession Chain Is Invisible to It

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 378) |
| **Element** | Supersession (E4) / 5-Rule Lint (E7) |
| **S / O / D** | 6 / 9 / 7 |

**Evidence:**

- `ADR-PROJ031-004-adr-identifier-convention.md:366-370` ("Two frontmatter mechanisms coexist"): *"The L5 ADR lint parses the **YAML `---` block**... YAML parsing is a **new capability the lint must implement**."*
- `ADR-PROJ031-004-adr-identifier-convention.md:671` (L-7 spec): *"`superseded_by`/`promoted_to`/`promoted_from` targets resolve to an existing ADR"* — checked only via the YAML frontmatter block.
- `ADR-PROJ031-004-adr-identifier-convention.md:527` (M-11 row): retrofit scope is explicitly limited to *"the 3 `docs/design/` framework ADRs **and** ... `ADR-EPIC002-001-strategy-selection`, `ADR-EPIC002-002-enforcement-architecture`... and `ADR-STORY015-001-tier-model-renumbering`"* — **`ADR-PROJ031-001/002/003` are not named.**
- **Directly verified** (this execution, `ADR-PROJ031-002-ci-token-push-strategy.md:1-17`): the file's header is **blockquote-only**; there is **no YAML `---` frontmatter block anywhere in the file**. Its supersession is stated only as `> **Status:** **Superseded by ADR-PROJ031-003**` (line 10) and `> **Superseded By:** [ADR-PROJ031-003](...)` (line 15) — both blockquote fields, not YAML.
- **Directly verified**, `ADR-PROJ031-003-credential-protection-supply-chain.md:663-669`: its Related Decisions table records `SUPERSEDES` against `ADR-PROJ031-002` in a markdown table, again not YAML frontmatter.

**Analysis:** L-7 is one of the 5 rules explicitly retained as the "fail-closed core" (`ADR:663`, `adr-standards-rule-draft.md:9`) and is marketed as the mechanism that catches "a forward-looking half-completed Path-2 that sets a relationship field but leaves its target missing." But L-7 can only ever inspect what it parses — the YAML `---` block — and this project's own real, already-executed supersession (`ADR-PROJ031-002` → `ADR-PROJ031-003`, dated 2026-06-28, already lived through a QG-1 C4 remediation) has **no YAML frontmatter to inspect at all**. M-11 — the migration item that would retrofit YAML onto pre-existing ADRs — explicitly scopes itself to framework-cited ADRs only, omitting the PROJ-031 sibling set entirely. The practical consequence: once M-6 ships, if a future edit accidentally broke the `ADR-PROJ031-002`→`003` link (e.g., `ADR-PROJ031-003` were renamed or deleted), L-7 would not detect it — not because the scenario is out-of-scan (like the `R-10` entity-embedded/repository-topology gaps, which are disclosed), but because **no YAML relationship field exists for L-7 to check in the first place**, and this is not currently named as a disclosed residual anywhere in either deliverable. `M-11`'s framing ("optional schema-completeness, not lint-gating — the 5-rule core validates these ADRs' filenames (L-1) regardless of their frontmatter") is accurate for L-1 but glosses over the fact that L-7 specifically has zero real-world coverage in this project's own corpus, which is a materially different and sharper claim than "provenance fields are optional."

**Corrective Action:** Disclosure-only (consistent with doctrine — no new lint, no retrofit mandate added): name `ADR-PROJ031-001/002/003` explicitly in the L-7 spec's descoped-note or in M-11, stating plainly that L-7's coverage is currently empty against this project's own live supersession chain and will remain so until/unless YAML frontmatter is added to these three files (which is not currently tracked by any Migration-Plan row).

**Acceptance Criteria:** Either M-11's retrofit list is extended to name `ADR-PROJ031-001/002/003` (even as a low-priority, non-gating row, matching the pattern already used for the EPIC002/STORY015 ADRs), or the L-7 spec / Enforcement Design descoped-note explicitly discloses that L-7 has zero real targets in the current corpus as a residual, parallel to R-9/R-10/R-11.

**Post-Correction RPN estimate:** ~60 (S=6 unchanged residual limitation once disclosed, O=9 unchanged fact, D=1 — fully disclosed, no longer a surprise).

---

### FM-003-20260706iter008: Cross-Branch Concurrent-Supersession Race (Undisclosed)

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 224) |
| **Element** | Supersession (E4) |
| **S / O / D** | 7 / 4 / 8 |

**Evidence:**

- `ADR-PROJ031-004-adr-identifier-convention.md:455` (R-6): names the analogous **creation-time** race explicitly — *"Cross-branch same-slug `NNN` race — two concurrent branches independently mint `ADR-{same-slug}-00N`... collision is invisible until merge"* — with a named detection mechanism (`sort|uniq -d`, both pre-flight and CI).
- `ADR-PROJ031-004-adr-identifier-convention.md:460` (R-11): scopes the *supersession*-field gap to a **single-author** oversight — *"a new ADR can declare it [`supersedes:`] while its predecessor's own `status`/`superseded_by` go unverified — silently leaving a superseded ADR still reading `ACCEPTED`"* — a forgot-to-update scenario, not a concurrent-authors scenario.
- `adr-standards-rule-draft.md:139-149` (Amend vs Supersede / Promotion Process): no mention of concurrent-branch supersession authorship at all.
- The predecessor ADR's `superseded_by` field (Frontmatter Schema, both files) is single-valued (`superseded_by: null` or one ID) — it cannot represent two competing claimants.

**Analysis:** R-6 explicitly names and mitigates (via detection, not prevention) the creation-time race: two branches independently minting the same `{slug}-NNN`. But no equivalent disclosure exists for the structurally identical risk one lifecycle stage later: two branches, each authoring a *different* new ADR, both intending to supersede the *same* predecessor (e.g., both propose to replace `ADR-agent-design-001` with their own competing successor). Because `supersedes`/`amends`/`amended_by` are unchecked by L-7 (disclosed as R-11, but only for the single-author-omission framing) and the predecessor's `superseded_by` is single-valued, a merge of both branches will silently let whichever PR lands last overwrite the predecessor's `superseded_by` value — orphaning the other successor ADR with **zero lint signal**, not even the pre-flight one-liner (which only checks slug/NNN uniqueness, not supersession-target uniqueness). This is a materially different failure surface from R-11 (which describes a single author's incomplete edit) and is not covered by R-6 (which is scoped to identical-slug creation, not divergent successors for one predecessor).

**Corrective Action:** Disclosure-only (no new lint), mirroring R-6's exact structure: add a parallel risk entry (e.g., R-14) stating the concurrent-supersession-authorship race, its detection gap, and that it is mitigated only by PR-review discipline (the same fallback already accepted for R-12).

**Acceptance Criteria:** A new Risks-register row (or an explicit addendum to R-11) names this specific scenario with the same rigor R-6 already receives.

**Post-Correction RPN estimate:** ~84 (S=7 unchanged, O=4 unchanged, D=3 once disclosed and subject to PR-review awareness).

---

## Recommendations

Ranked by RPN; all corrective actions are **text-only disclosures or one-clause additions**, consistent with the subtraction doctrine (no lint rule, ledger, gate, or matrix is proposed):

1. **FM-001 (RPN 560, Critical):** Reconcile the 16-vs-15 grandfather-count contradiction across D-4, the M-6 row, Enforcement Design, and both rule-draft passages before M-6's implementer builds the regression fixture.
2. **FM-002 (RPN 378, Critical):** Disclose that L-7 has zero real coverage against `ADR-PROJ031-001/002/003`'s existing supersession chain; optionally add these three files to M-11's retrofit list as a low-priority row.
3. **FM-003 (RPN 224, Critical):** Add a disclosed residual for the cross-branch concurrent-supersession race, parallel to R-6.
4. **FM-004 (RPN 144, Major):** Copy the ADR's framework-scope determination criteria into the rule draft's Promotion Process so the auto-loaded operative artifact is not less complete than the historical decision record.
5. **FM-005 (RPN 120, Major):** Add a one-line forward-pointer for first-time authors (Onboarding element currently has zero dedicated content).
6. **FM-006 (RPN 108, Major):** Cross-reference the zero-tooling pre-flight one-liner into the Deployment Targets table as a today-usable downstream fallback, independent of unbuilt M-13.
7. **FM-007 (RPN 54, Minor):** Optional — add SHOULD-NOT guidance on amendment-accumulation triggering a supersession review.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-002 (L-7 real coverage gap in this project's own corpus), FM-003 (undisclosed race), FM-004 (missing scope-determination criteria in the operative rule file) |
| Internal Consistency | 0.20 | Negative | FM-001 is a direct, high-confidence same-document numerical contradiction — the single largest hit to this dimension across all 7 findings |
| Methodological Rigor | 0.20 | Negative | FM-001 (regression test target is ambiguous), FM-002 (a "fail-closed core" rule with zero real validation targets), FM-007 (no amendment-accrual discipline) |
| Evidence Quality | 0.15 | Negative | FM-001/FM-002 were both discovered via the document's own citation trail (file+line self-references), meaning the deliverable's strong citation discipline enabled discovery — but the underlying claims themselves are not yet reconciled |
| Actionability | 0.15 | Neutral-Positive | Every finding's corrective action is a cheap, disclosure-only or one-clause text edit — no new machinery is required to close any of the 7 findings, consistent with the subtraction doctrine's own stated posture |
| Traceability | 0.10 | Positive | All 7 findings cite exact file+line evidence across both deliverables and one directly-verified sibling ADR; FM-NNN identifiers follow the document's own established tag-glossary convention |

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 3 (FM-001, FM-002, FM-003)
- **Major:** 3 (FM-004, FM-005, FM-006)
- **Minor:** 1 (FM-007)
- **Total RPN:** 1,588
- **Protocol Steps Completed:** 5 of 5 (Decompose, Enumerate, Rate, Prioritize, Synthesize)
- **Elements Decomposed:** 8 (Creation, Cross-Reference, Amendment, Supersession, Promotion Path 1, Promotion Path 2/Self-Promotion, 5-Rule Lint + Grandfather Test, Onboarding)
- **Constitutional Compliance:** P-003 (no subagents spawned) | P-020 (no edits made to either deliverable; read-only review) | P-022 (blind-protocol deviation disclosed above; all findings evidence-cited; no deleted machinery re-demanded)

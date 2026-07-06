# FMEA Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.4) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.4)
**Criticality:** C4 | Engagement quality gate: 0.95
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, iteration 4)
**H-16 Compliance:** S-003-equivalent steelmanning is embedded throughout the ADR's own "Options Considered" and "Rationale" sections (self-authored steelman per H-16 spirit for a C4 deliverable already through 3 prior adversarial iterations).
**Elements Analyzed:** 8 (creation, cross-referencing, amendment, superseding, promotion, lint enforcement, template drift, new-project onboarding) | **Failure Modes Identified:** 9 | **Total RPN:** 1462

**PROTOCOL NOTE (P-022):** A Grep search for `canonical_id` scoped too broadly and returned one matching line from another blind reviewer's iteration-4 output file (`adversary/iteration-004/s-004-findings.md`). I did not open/read that file; its content is excluded from this analysis. The `canonical_id` finding below (FM-007) was derived independently by comparing the ADR's own frontmatter block against the rule draft's Frontmatter Schema section, prior to that grep call.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | The 8 lifecycle stages decomposed |
| [Findings Table](#findings-table) | All 9 failure modes, RPN-ranked |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Summary counts |

---

## Summary

Across 8 decomposed lifecycle stages of the ADR convention, this FMEA identifies 9 failure modes: 3 Critical (RPN >= 200), 5 Major, 1 Minor. The highest-RPN finding (FM-001, RPN 240) is that the L5 lint's scope is permanently limited to files under `decisions/`/`docs/design/`, meaning the *producer-side* artifacts (exemplar template, SKILL.md, the `ps-architect` agent) that the package itself found badly drifted (Fix 1/2/3) will have **zero regression protection** once the one-time fixes land — drift can silently recur with no detection mechanism. Two further Critical findings (FM-002, FM-003, RPN 210 each) concern internal-consistency gaps introduced by the convention's own enforcement machinery: the `amends`/`amended_by` relationship pair is defined in frontmatter and claimed by the rule draft (line 246) to "enable L5/L6/L7 lint," but the actual L-7 rule never checks it; and the ADR's "L5 CI Lint" section, framed as a condensed "ADR-level summary," is in fact a near-verbatim second copy of the rule draft's full 14-row lint table with no mechanism to keep the two synchronized as the spec evolves. **Recommendation: REVISE** (targeted, well-scoped corrections; the document's overall architecture and self-review discipline are strong, but the 0.95 engagement gate is a materially higher bar than these gaps currently support).

---

## Element Inventory

| ID | Element (lifecycle stage) | Primary artifact location |
|----|---------------------------|----------------------------|
| E1 | Creation (ID assignment, frontmatter authoring, scope declaration) | ADR-M-001/M-002/M-013; Frontmatter Schema |
| E2 | Cross-referencing (ADR ↔ rule draft, ADR ↔ corpus citations) | Both files' relative links; L-8 |
| E3 | Amendment (in-body dated block, `amends`/`amended_by`) | ADR-M-009; "Amend vs Supersede" |
| E4 | Superseding (new ADR, tombstone bidirectionality) | "Amend vs Supersede"; L-7 |
| E5 | Promotion (Path 0/1/2, reciprocal link repair) | "Promotion Process"; Migration Plan M-2/M-9 |
| E6 | Lint enforcement (L-1a…L-12, waiver ledger, regression test) | "Enforcement Design" (ADR) / "L5 CI Lint Specification" (rule draft) |
| E7 | Template drift (exemplar template, SKILL.md, ps-architect.md) | Fix 1 / Fix 2 / Fix 3 (rule draft) |
| E8 | New-project onboarding (worktracker scaffold, topology) | "New-Project Onboarding" (rule draft); M-14 |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|---------------|---|---|---|-----|----------|---------------------|
| FM-001-20260702-iter4 | E7 Template drift | Lint scope never covers producer-side artifacts (template/SKILL/agent); no regression protection after one-time Fix 1/2/3 | 6 | 5 | 8 | 240 | Critical | Methodological Rigor |
| FM-002-20260702-iter4 | E6 Lint enforcement | ADR's "ADR-level summary" of the lint spec is a near-verbatim second copy of the rule draft's full table; no sync mechanism | 6 | 5 | 7 | 210 | Critical | Methodological Rigor |
| FM-003-20260702-iter4 | E3 Amendment | `amends`/`amended_by` has zero lint integrity check, contradicting rule draft's own claim (line 246) that it "enables L5/L6/L7 lint" | 6 | 5 | 7 | 210 | Critical | Internal Consistency |
| FM-004-20260702-iter4 | E5 Promotion / E2 Cross-ref | M-2 and M-9 reciprocal-link repair mandated "in the same commit"; Migration Plan provides no atomicity mechanism across the two independent TBD-Task rows | 6 | 5 | 6 | 180 | Major | Actionability |
| FM-005-20260702-iter4 | E6 Lint / E1 Creation | Rule draft's own regression-test enumeration ("PROJ031×4, incl. this ADR," line 225) contradicts the same file's Frozen-and-Grandfathered table ("PROJ031×3," line 107) for the identical dialect family | 6 | 5 | 6 | 180 | Major | Internal Consistency |
| FM-006-20260702-iter4 | E8 Onboarding | Onboarding action item 2 ("seed each new project with an empty `decisions/`") has no corresponding Migration-Plan row, owner, Task, or tooling change | 5 | 6 | 5 | 150 | Major | Completeness |
| FM-008-20260702-iter4 | E8 Onboarding | Onboarding items 2-3 are not topology-branched, unlike item 1 (which explicitly handles both FM-102 topologies) | 4 | 5 | 6 | 120 | Major | Completeness |
| FM-007-20260702-iter4 | E1 Creation | `canonical_id` frontmatter field (used in the ADR's own flagship self-compliance frontmatter, line 15) is not defined anywhere in the Frontmatter Schema | 5 | 5 | 4 | 100 | Major | Evidence Quality |
| FM-009-20260702-iter4 | E1 Creation / E6 Lint | The corpus's own catalogued "9th family" (`ADR-CI-NNN`) receives no explicit disposition in the ID Scheme, Location, or Frozen/Grandfathered tables of either file | 4 | 3 | 6 | 72 | Minor | Completeness |

**Finding ID format:** `FM-{NNN}-20260702-iter4`.

---

## Finding Details

### FM-001: Producer-Side Artifacts Have No Ongoing Lint Regression Protection

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 240) |
| **Element** | E7 Template drift |
| **Strategy Step** | Step 2 (Missing lens) + Step 3 (rating) |

**Evidence:** The L5 lint's "Where" column for every rule (L-1a through L-12) scopes to `projects/*/decisions/`, `docs/design/`, or repo-wide free-text scans (`ADR-PROJ031-004-adr-identifier-convention.md:645-661`; `adr-standards-rule-draft.md:206-219`). None of the 14 rules inspects `docs/knowledge/exemplars/templates/adr.md`, `skills/architecture/SKILL.md`, or `skills/problem-solving/agents/ps-architect.md` — the three artifacts that Fix 1/Fix 2/Fix 3 (`adr-standards-rule-draft.md:239-274`) document as *currently* non-compliant with the very convention they produce output for (bare `{NUMBER}` title, `ADR_NNN` underscore mismatch, phantom `docs/decisions/`/`templates/adr.md`/`python3 scripts/cli.py` paths).

**Analysis:** Per the FMEA "Missing" lens, the lint enforcement design is missing coverage of the *producer* side of the ADR lifecycle entirely. M-3/M-4/M-12 (Migration Plan) are scoped as one-time fixes to be applied *on ratification*. Once applied, nothing in the L-1 through L-12 rule set — nor any other mechanism disclosed in either file — re-validates these three producer artifacts on subsequent edits. Since the package's own evidence shows these exact files have already drifted once (independently, across at least three separate defects), and nothing about the future editing process for skills/templates/agents changes after ratification, there is no structural reason to expect they won't drift again — and if they do, every newly-authored ADR is silently born non-compliant again, with the L5 lint (which only inspects the *output*, not the *generator*) providing a false sense of security.

**Corrective Action:** Add a dedicated producer-side check (e.g., L-13, WARN or FAIL) that greps the three named producer files for the specific non-compliant patterns already catalogued in Fix 1/2/3 (bare `{NUMBER}`, `ADR_NNN`, `docs/decisions/`, `templates/adr.md`, `python3 scripts/`) and fails/warns if any reappear post-fix. At minimum, disclose this as a named residual risk (parallel to R-1..R-6) rather than leaving producer-side regression entirely outside the enforcement model's stated scope.

**Acceptance Criteria:** A named lint rule or documented residual explicitly covers re-drift of the three producer artifacts; Migration Plan gains a corresponding tracked item.

**Post-Correction RPN Estimate:** ~60 (S=6, O=2, D=5) once a producer-side check or documented residual exists.

---

### FM-002: The ADR's "Lint Summary" Is a Second, Unsynchronized Full Copy of the Rule Draft's Spec

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 210) |
| **Element** | E6 Lint enforcement |
| **Strategy Step** | Step 2 (Insufficient/Inconsistent lens) |

**Evidence:** The ADR states: "The full lint spec (override model, regression test, L-1 split, L-4/L-7/L-8 coverage) lives in the companion rule draft's L5 CI Lint Specification; **this section is the ADR-level summary**" (`ADR-PROJ031-004-adr-identifier-convention.md:601`). The subsequent 14-row rule table (`:645-661`) is near-identical in column structure (Rule | Class | Checks/What it checks | Rejects/What it rejects | Where) and substantive detail to the rule draft's own 14-row table (`adr-standards-rule-draft.md:206-219`) — e.g., L-1a's regex, the look-alike exclusion set, and the SM-101/RT-003 rationale are reproduced near-verbatim in both files, not condensed.

**Analysis:** A true "summary" would be materially shorter than its source; here the two tables are comparable in length and identical in the load-bearing details (regexes, exclusion lists, rationale tags). This means every future edit to any of the 14 rules (which this document's own 4-iteration history shows happens frequently — L-1 was split into L-1a/L-1b, L-7 was raised WARN→FAIL, L-9/L-10/L-11/L-12 were added across iterations) must be applied in **two separate files** with no automated check that they stay identical. This is precisely the citation/consistency-drift failure class this whole convention exists to prevent — now manifesting in the convention's own founding specification. The historical record shows the owner has so far kept both tables synchronized manually and diligently across 4 iterations, which lowers (but does not eliminate) near-term occurrence risk; the structural risk persists for any future editor less familiar with the dual-file obligation.

**Corrective Action:** Either (a) collapse the ADR's Enforcement Design section to a genuinely short table (Rule ID, Class, one-line purpose, `-> see rule draft`) rather than reproducing full regex/rationale, or (b) add an explicit note atop both tables stating they MUST be edited together, plus an L-8-style free-text check that the two tables' rule-ID sets match.

**Post-Correction RPN Estimate:** ~90 (S=6, O=3, D=5) once the duplication is collapsed to a true summary or a sync-check exists.

---

### FM-003: `amends`/`amended_by` Has No Lint Coverage, Contradicting the Rule Draft's Own Claim

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 210) |
| **Element** | E3 Amendment |
| **Strategy Step** | Step 2 (Inconsistent lens) |

**Evidence:** The Frontmatter Schema defines three relationship-pair fields: `supersedes`/`superseded_by`, `amends`/`amended_by`, and `promoted_from`/`promoted_to` (`adr-standards-rule-draft.md:123-128`; also `ADR-PROJ031-004-adr-identifier-convention.md:348-353`). Fix 1-d explicitly states that inserting the frontmatter block (including `amends`/`amended_by`) "enables L5/L6/L7 lint" (`adr-standards-rule-draft.md:246`). But the actual L-7 rule ("Tombstone integrity, structured, BIDIRECTIONAL") checks only `superseded_by`/`promoted_to`/`promoted_from` targets and reciprocals (`adr-standards-rule-draft.md:214`; `ADR-PROJ031-004-adr-identifier-convention.md:655`) — `amends`/`amended_by` is not named in any of the 14 lint rules (L-1a through L-12) in either file.

**Analysis:** This is a direct, checkable contradiction within the rule draft itself: line 246 promises lint coverage for a field that line 214's rule specification never delivers. Per ADR-M-009, cross-ADR amendment via `amends`/`amended_by` is an explicitly supported (if secondary) mechanism alongside in-body dated blocks; a dangling or one-directional `amends`/`amended_by` link would silently misrepresent an amendment relationship with no detection path, unlike the equivalent supersede/promote relationships which L-7 explicitly protects.

**Corrective Action:** Either extend L-7 to also check `amends`/`amended_by` bidirectionality (rename to "Relationship integrity" to cover all three pairs), or correct Fix 1-d's claim to state only `supersedes`/`superseded_by` and `promoted_from`/`promoted_to` are lint-checked, and disclose `amends`/`amended_by` integrity as unchecked.

**Post-Correction RPN Estimate:** ~70 (S=6, O=2, D=6) once L-7 is extended or the claim is corrected.

---

## Recommendations

Grouped Critical first, then Major, per RPN.

1. **FM-001 (RPN 240):** Add a named producer-side lint check or explicitly disclosed residual for the exemplar template, SKILL.md, and `ps-architect.md` post-fix regression risk.
2. **FM-002 (RPN 210):** Collapse the ADR's lint table to a genuine one-line-per-rule summary, or add an explicit dual-file sync obligation/check.
3. **FM-003 (RPN 210):** Extend L-7 to cover `amends`/`amended_by`, or correct Fix 1-d's over-claim.
4. **FM-004 (RPN 180):** Add an explicit joint-commit dependency between Migration-Plan items M-2 and M-9 (e.g., a single tracked Task covering both, or a note that M-9 cannot close until M-2's reciprocal edit is verified in the same PR).
5. **FM-005 (RPN 180):** Reconcile the rule draft's own internal PROJ031 dialect-family count (line 107 says ×3, line 225 says ×4 "incl. this ADR") before the M-6 regression test is built from either number.
6. **FM-006 (RPN 150):** Add a tracked Migration-Plan row (owner + Task) for "seed `decisions/` on new-project creation," distinct from M-14's documentation-only scope.
7. **FM-008 (RPN 120):** Topology-branch onboarding items 2 and 3 to match item 1's FM-102 treatment, or state explicitly that "new project" seeding is project-based-topology-only.
8. **FM-007 (RPN 100):** Either add `canonical_id` to the Frontmatter Schema as an optional advisory field with defined semantics, or remove it from the ADR's own frontmatter and rely on the existing Meta-Note prose alone.
9. **FM-009 (RPN 72):** Add an explicit disposition (deprecated / frozen / requires-canonical-slug) for the 9th corpus family (`ADR-CI-NNN`) in the ID Scheme and Frozen/Grandfathered tables, even though no live file in that family currently exists.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-006, FM-008, FM-009: onboarding tooling gap, missing topology branching, and an uncatalogued corpus family leave the lifecycle decomposition incomplete by the document's own stated MECE standard |
| Internal Consistency | 0.20 | Negative | FM-003 (Fix 1-d's lint claim vs. actual L-7 scope) and FM-005 (PROJ031×3 vs ×4 within the same file) are direct, checkable contradictions |
| Methodological Rigor | 0.20 | Negative | FM-001 (no regression protection for producer artifacts) and FM-002 (unsynchronized duplicate lint spec) are structural gaps in the enforcement design's own long-term integrity |
| Evidence Quality | 0.15 | Negative (minor) | FM-007: the flagship self-compliance frontmatter introduces an undocumented field, weakening the "worked example of self-compliance" claim |
| Actionability | 0.15 | Negative | FM-004: the "same commit" reciprocal-link mandate has no enforceable mechanism, making it advisory prose rather than an actionable gate |
| Traceability | 0.10 | Negative (minor) | FM-002 and FM-003 both reduce confidence that the two-file lint specification will remain traceable/consistent as it evolves post-ratification |

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 3 (FM-001, FM-002, FM-003)
- **Major:** 5 (FM-004, FM-005, FM-006, FM-007, FM-008)
- **Minor:** 1 (FM-009)
- **Total RPN:** 1462
- **Protocol Steps Completed:** 5 of 5
- **Overall Assessment:** REVISE — targeted corrections to the enforcement-spec duplication, the `amends`/`amended_by` lint gap, and producer-side regression protection are warranted before this deliverable can credibly clear the 0.95 engagement gate. The document's steelmanning, P-022 self-disclosure discipline, and prior-iteration remediation history remain strong and are not challenged by this review.

---

*Strategy: S-012 FMEA*
*Template: `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*Constitutional Compliance: P-001 (evidence-cited), P-003 (no subagents spawned), P-020 (no edits to deliverables), P-022 (accidental adversary-directory grep exposure disclosed above; no fabricated claims — all findings cite file+line)*

# Inversion Report: GitHub Issue #353 (PROJ-032/BUG-004)

**Strategy:** S-013 Inversion Technique (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-353.md` — live text of geekatron/jerry issue #353
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind to other strategies/issues)
**H-16 Compliance:** N/A for standalone strategy-run context; treated as informational per tournament design
**Goals Analyzed:** 3 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 2

## Summary

The issue's factual claims (severity, "not maintainer-fixable", commit `c07033ce` withdrawal, the answer-key defect) all check out against the remediation register and verdict. Inversion found one Critical resolvability gap (an unqualified worktracker path one line above a correctly-qualified sibling path) and one Major actionability gap (the compressed design question omits sub-requirements the full register treats as mandatory). Recommendation: ACCEPT with two targeted text fixes.

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| S-013-01 | "The Worktracker path is resolvable as written" | Assumption | High | Critical | Line: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-004-qg-e4-validation-evidence` (register section REM-04)." — no branch given | Actionability |
| S-013-02 | "The compressed design-question bullet list is the complete requirement" | Assumption | Medium | Major | Register REM-04 redesign question also requires: fix TRAP-01's internal path contradiction, full AC-7 coverage, evidence shipped/cited inside the package, and a shipped SD-01..18 register — none named in the issue's four-item list | Completeness |
| S-013-03 | "PROJ-032/BUG-004" title prefix is self-explanatory | Anti-Goal | N/A | Minor | Title: "PROJ-032/BUG-004: nuclear-sop — validation test contained its own answer key..." | Traceability |
| S-013-04 | "REM-04" needs no gloss | Anti-Goal | N/A | Minor | "(register section REM-04)" — bare internal code, mitigated by adjacent register-file pointer | Traceability |

## Finding Details

### S-013-01: Worktracker path omits branch qualifier its sibling sentence supplies [CRITICAL]

**Type:** Assumption
**Original assumption:** A bare repo-relative path in issue text is resolvable by an external reader without further qualification.
**Inversion:** The path `projects/PROJ-032-nuclear-sop-review/work/BUG-004-qg-e4-validation-evidence` does not exist on `main` or on the PR's own branch `proj-0039-nuclear-engineer` — it exists only on `feat/proj-032-nuclear-sop-review` (verified live on GitHub). The very next sentence in the same paragraph — pointing to `remediation-register.md` — correctly appends "on branch `feat/proj-032-nuclear-sop-review`". The worktracker path does not.
**Plausibility:** High. An external contributor or their agent reading the issue on the default branch view, or grepping the PR's own checkout, will get a 404 / not-found and may conclude the reference is broken or fabricated — directly undermining trust in the rest of the issue's claims.
**Consequence:** Sends the reader down a dead path at the exact place they'd go to find the authoritative worktracker record for this bug; internally inconsistent within the same paragraph (one path qualified, one not).
**Evidence:** Issue body: `Worktracker: \`projects/PROJ-032-nuclear-sop-review/work/BUG-004-qg-e4-validation-evidence\` (register section REM-04). Full analysis with candidate designs: \`remediation-register.md\` in \`.../STORY-004-remediation/\` on branch \`feat/proj-032-nuclear-sop-review\`.`
**Dimension:** Actionability
**Mitigation:** Append the identical branch qualifier to the Worktracker sentence: `... BUG-004-qg-e4-validation-evidence\` (register section REM-04, on branch \`feat/proj-032-nuclear-sop-review\`).`
**Acceptance Criteria:** Both repo-relative paths in the Tracking section carry the same branch qualifier.

### S-013-02: Design question omits register sub-requirements a contributor would otherwise miss [MAJOR]

**Type:** Assumption
**Original assumption:** The four-item design question ("blind... live transcripts... independent authorship and scoring... more than three trials") is a sufficient restatement of what "replaces the invalidated walkthrough."
**Inversion:** Register REM-04's actual redesign question adds items not present in the issue: fix TRAP-01's internal path contradiction (WARNING text vs. ERROR/Target field disagree on the ADR output path), achieve full acceptance-criteria coverage (AC-7 is currently unsatisfiable as written), ship or resolvably cite the evidence inside the package (current evidence lives outside `skills/nuclear-sop/`), and ship the referenced SD-01..18 security-design register. A contributor could satisfy the visible four-item list (blind fixture, live run, independent scoring, N>3) while still shipping an internally contradictory fixture or an unsatisfiable AC-7, and reasonably believe the issue is resolved.
**Plausibility:** Medium-high — the four listed criteria are the headline items; the omitted ones are easy to miss without reading the full register, and the issue's own framing ("what... replaces the invalidated walkthrough") reads as exhaustive.
**Consequence:** Rework risk — a good-faith fix could pass the stated bar and still fail review on the unlisted criteria (AC-7, TRAP-01 contradiction, packaging).
**Evidence:** remediation-register.md REM-04 "Redesign question for the contributor" (full list of 6 elements) vs. issue's 4-item compressed list.
**Dimension:** Completeness
**Mitigation:** Add one clause to the design question or a trailing note: "(see the linked register for additional required fixes: the fixture's internal path contradiction, full acceptance-criteria coverage, and the security-design register)."
**Acceptance Criteria:** Design question or an adjacent sentence enumerates or points explicitly to all items the register treats as required, not only the four most salient.

## Recommendations

- **Major (SHOULD mitigate):** S-013-02 — add a pointer clause naming the omitted sub-requirements or explicitly flag the list as "non-exhaustive; see register for full requirements."
- **Critical (MUST mitigate):** S-013-01 — append branch qualifier to the Worktracker path.
- **Minor (MAY mitigate):** S-013-03 — gloss "PROJ-032" once (e.g., "internal tracking ID") or drop the prefix from the title, keeping it only in the Tracking footer. S-013-04 — no action required; mitigated by the adjacent register-file pointer.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-013-02: compressed design question drops known sub-requirements |
| Internal Consistency | 0.20 | Negative | S-013-01: one of two paths in the same paragraph carries a branch qualifier, the other doesn't |
| Methodological Rigor | 0.20 | Neutral | Not applicable to a communication artifact |
| Evidence Quality | 0.15 | Positive | All factual claims verified accurate against register/verdict/commit diff |
| Actionability | 0.15 | Negative | S-013-01 sends a reader to a non-resolving path |
| Traceability | 0.10 | Neutral | Minor unexplained codes (PROJ-032, REM-04) mitigated by adjacent context |

## Execution Statistics
- **Total Findings:** 4
- **Critical:** 1
- **Major:** 1
- **Minor:** 2
- **Protocol Steps Completed:** 6 of 6

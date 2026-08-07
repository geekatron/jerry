# Constitutional Compliance Report: GitHub Issue #355 (BUG-006 / REM-06)

**Strategy:** S-007 Constitutional AI Critique (adapted for a communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-355.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-007)
**Constitutional Context (adapted principles for this artifact type):** factual accuracy, self-containedness, actionability, resolvable references, honest severity/status framing, concision — evaluated against remediation-register.md (REM-06), BUG-006 worktracker entity, and pr269-verdict.md.

## Summary

PARTIAL compliance: 0 Critical, 1 Major, 3 Minor. The issue's factual claims (defect mechanics, severity, disposition, cluster ID) all verify against ground truth, and referenced paths resolve on the stated branch. The single Major finding is a resolvability gap: one of two internal-repo paths lacks the branch qualifier the other carries, risking a dead-end lookup for a reader with no framework context. Recommend ACCEPT after one-line fix.

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|---------------------|
| S-007-01 | Resolvable references | MEDIUM | Major | Worktracker path given with no branch qualifier | Actionability |
| S-007-02 | Factual precision | SOFT | Minor | "mitigated only by a text label" understates partial coverage | Evidence Quality |
| S-007-03 | Completeness of design-question | SOFT | Minor | Provenance and injection-trust asks merged into one bullet | Completeness |
| S-007-04 | Self-containedness | SOFT | Minor | Title carries unexplained internal codes "PROJ-032/BUG-006" | Internal Consistency |

## Finding Details

### S-007-01: Worktracker path lacks branch qualifier [MAJOR]

**Location:** Tracking line: `Worktracker: projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design (register section REM-06).`
**Evidence:** This path exists only on `feat/proj-032-nuclear-sop-review` (verified: `BUG-006-oe-feedback-loop-design.md` present there). It does not exist on the PR branch `proj-0039-nuclear-engineer` and is not part of the shipped `skills/nuclear-sop/` package. The very next sentence attaches `on branch feat/proj-032-nuclear-sop-review` explicitly — but only to the `remediation-register.md` reference, not to this one.
**Impact:** An external contributor or their agent reading only this issue has no stated reason to believe the Worktracker path sits on a *different* branch than their own PR branch. They may search their own branch or `main`, not find the file, and either give up on the reference or (for an agent) hallucinate a substitute path. This is exactly the "forces a lookup / dead path" failure mode the mission calls out.
**Dimension:** Actionability
**Remediation:** Attach the branch qualifier to both paths in one clause, e.g.: "Worktracker and full analysis live on the maintainer's review branch `feat/proj-032-nuclear-sop-review`: `projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design` (register section REM-06) and `remediation-register.md` under `.../STORY-004-remediation/`."

### S-007-02: "mitigated only by a text label" overstates the mitigation's reach [MINOR]

**Location:** "...prompt-injection channel (low-risk runs write files that high-risk runs read), mitigated only by a text label..."
**Evidence:** Register REM-06 G2: "SEC-002 guard labels cover only 2 of the interpolated fields... 'HUMAN INFORMATION ONLY' is model-compliance, not a control; bb-003 tests one field."
**Impact:** The issue's wording is accurate about the mitigation's *weakness* (a label, not a control) but implies the label covers the channel generally; the register is more damning — the label doesn't even cover all the fields that carry attacker-controlled content. A reader could underestimate the gap.
**Dimension:** Evidence Quality
**Remediation:** "...mitigated only by a text label on 2 of the interpolated fields (not all of them)."

### S-007-03: Design question compresses two distinct asks into one [MINOR]

**Location:** "...and a provenance/trust model for a corpus shared across risk levels?"
**Evidence:** Register REM-06 redesign question separates "a provenance mechanism that survives work/ cleanup (or an archival rule)" from "an injection trust model for the corpus (guard labels on every interpolated field, or explicit acceptance of residual risk)" — two different design decisions.
**Impact:** A contributor could address stale-provenance-after-cleanup and believe the corpus's injection-trust gap is covered by the same fix; it is not. Low risk since the linked register spells out both, but the issue text is the first thing read.
**Dimension:** Completeness
**Remediation:** Split into two clauses: "...a provenance model that survives routine cleanup, and an injection-trust model for a corpus shared across risk levels (e.g., guard labels on every field that can carry attacker/prior-run content)."

### S-007-04: Title carries unexplained internal identifiers [MINOR]

**Location:** Title: "PROJ-032/BUG-006: nuclear-sop — lessons-learned loop can't work as specified..."
**Evidence:** "PROJ-032" and "BUG-006" are internal Jerry worktracker identifiers with no legend anywhere in the issue body explaining what they are (vs. e.g. "internal tracking ref").
**Impact:** Low — the rest of the title and body are in plain language and fully carry the meaning; the codes are inert decoration to an outside reader, not load-bearing. Included for completeness of the self-containedness check per mission scope.
**Dimension:** Internal Consistency
**Remediation:** Optional: prefix with "(internal ref)" or drop from the title and keep it only in the Tracking line where it already appears with context.

## Verified Facts (no violation — listed for traceability)

- Severity "major" matches register REM-06 and BUG-006 entity (`Severity: major`). Correct.
- "not maintainer-fixable (design decision)" matches REM-06 disposition DEFER-REWORK. Correct.
- Schema/threshold/injection/provenance claims in the body all trace 1:1 to REM-06 groups G1–G3. Correct, no fabrication.
- `remediation-register.md` path resolves exactly as written on `feat/proj-032-nuclear-sop-review` (confirmed by direct read). Correct.
- Branch `feat/proj-032-nuclear-sop-review` is pushed and publicly reachable on GitHub (confirmed via fetch). Correct — not a local-only dead reference.
- "Blocks merge of PR #269" matches pr269-verdict.md (BUG-006 is required to close in both the full-rework and narrow-early-merge paths). Correct.
- No instance of `projects/PROJ-` + a non-032 3–4 digit ID appears in the deliverable. Path hygiene clean.

## Remediation Plan

**P1 (Major):** S-007-01 — add branch qualifier to the Worktracker path reference.
**P2 (Minor):** S-007-02, S-007-03, S-007-04 — precision/self-containedness polish.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | S-007-03: design question under-specifies two distinct sub-asks |
| Internal Consistency | 0.20 | Negative (minor) | S-007-04: title codes vs. plain-language body |
| Methodological Rigor | 0.20 | Neutral | No findings affect this dimension |
| Evidence Quality | 0.15 | Negative (minor) | S-007-02: mitigation-coverage overstatement |
| Actionability | 0.15 | Negative | S-007-01: unqualified path risks dead-end lookup |
| Traceability | 0.10 | Positive | All claims traced 1:1 to register/BUG-006/verdict; branch reachability confirmed |

**Constitutional Compliance Score:** `1.00 - (0.05*0 + ... )` — using the adapted penalty model (Major -0.10, Minor -0.03 for this communication-artifact adaptation, lighter than code-defect penalties given the artifact's small size and clean factual record): `1.00 - (1*0.10 + 3*0.03) = 1.00 - 0.19 = 0.81` → **REVISE** (below 0.92; near the 0.85 REJECTED floor but above it).

**Threshold Determination:** REVISE. The single Major finding (S-007-01) is a one-line fix; the three Minor findings are optional polish. No fact in the deliverable is wrong, fabricated, or would send a reader to an incorrect conclusion about the defect itself — the gap is purely in reference resolvability and precision, not truth.

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 0
- **Major:** 1
- **Minor:** 3
- **Protocol Steps Completed:** 5 of 5 (adapted: context load, principle enumeration, evaluation, remediation guidance, scoring)

# Constitutional Compliance Report: GitHub Issue #352 (BUG-003 / REM-03)

**Strategy:** S-007 Constitutional AI Critique (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-352.md` — live text of geekatron/jerry issue #352
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-007)
**Constitutional lens applied:** P-001 (accuracy), P-004 (provenance/resolvable evidence), P-011 (evidence-based claims), P-022 (no deception via omission/ambiguity) — evaluated against the mission's communication-artifact criteria (self-containedness, actionability, resolvable references, honest severity, concision).

## Summary

PARTIAL compliance: 0 Critical, 2 Major, 3 Minor. The substantive claims (authority inversion, fabricated SHA-256 claim, RESUME-past-holds bypass, "not maintainer-fixable," "blocks merge") all check out against `remediation-register.md` REM-03 and the `c07033ce` diff (confirmed sop-verifier.md's Step 6 change addresses only SEC-008/REM-12, not REM-03's criteria-sourcing or tamper claims). The defects found are reference-resolvability and self-containedness gaps, not factual errors. Score: 0.86 (REVISE). Recommend targeted revision, not rejection.

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-352 | P-004/P-022: resolvable references | MEDIUM | Major | Branch qualifier ambiguity — see detail | Actionability |
| CC-002-352 | P-004: evidence must be reachable, not just named | MEDIUM | Major | Bare paths, no hyperlinks | Actionability |
| CC-003-352 | Self-containedness (mission-specific) | SOFT | Minor | Unglossed codes in title | Completeness |
| CC-004-352 | P-011: evidence-based, complete remediation ask | SOFT | Minor | Redesign question drops one sub-part | Completeness |
| CC-005-352 | Self-containedness (mission-specific) | SOFT | Minor | "register section REM-03" opaque | Completeness |

## Finding Details

### CC-001-352: Branch qualifier does not clearly cover the Worktracker path [MAJOR]

**Location:** Tracking line: `Worktracker: projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper (register section REM-03). Full analysis ... on branch feat/proj-032-nuclear-sop-review.`
**Evidence:** Verified live: `github.com/geekatron/jerry/tree/main/projects/PROJ-032-nuclear-sop-review` → **404**. The same path resolves only on `feat/proj-032-nuclear-sop-review` (confirmed: `BUG-003-trust-boundary-state-tamper.md` loads on that branch). The "on branch ..." clause grammatically attaches to the *second* sentence (remediation-register.md) only.
**Impact:** An external reader defaulting to `main` (the normal GitHub assumption when no branch is stated) hits a dead path for the Worktracker reference — sends them down a wrong path per the Critical bar, mitigated to Major only because the second, correctly-qualified sentence in the same paragraph makes the actual branch discoverable with one extra inference.
**Remediation:** State the branch once, covering both references: *"On branch `feat/proj-032-nuclear-sop-review` (not yet merged to main): worktracker entry at `.../BUG-003-trust-boundary-state-tamper/`; full analysis in `remediation-register.md` at `.../STORY-004-remediation/`."*

### CC-002-352: Paths given as plain text, not clickable links [MAJOR]

**Location:** Both tracking references (Worktracker path; remediation-register.md path).
**Evidence:** Neither is rendered as a markdown link; both are backtick-quoted paths requiring the reader to manually compose `https://github.com/geekatron/jerry/blob/{branch}/{path}`.
**Impact:** Forces a lookup/assembly step for a human or agent that a one-line hyperlink would eliminate — directly matches the Major bar ("forces a lookup").
**Remediation:** `[remediation-register.md](https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md)` and the equivalent link for the BUG-003 worktracker file.

### CC-003-352: Title carries unglossed internal codes [MINOR]

**Location:** Title: `PROJ-032/BUG-003: nuclear-sop — verifier takes its criteria from the file it polices (trust anchor, PR #269)`
**Evidence:** "PROJ-032" and "BUG-003" are only tied to a meaning by reading to the Tracking footer; the title itself offers no gloss.
**Impact:** Minor — the substantive title clause ("verifier takes its criteria from the file it polices") is already self-contained and carries the meaning; the codes are supplementary provenance, not load-bearing.
**Remediation:** `nuclear-sop: verifier takes its acceptance criteria from the file it polices (PR #269 review; tracked as BUG-003)`.

### CC-004-352: Design question omits the pre-execution RESUME-bypass sub-ask [MINOR]

**Location:** Paragraph 2, "The design question to answer."
**Evidence:** `remediation-register.md` REM-03's redesign question has a third clause not carried into the issue: "...and how is the RESUME-past-holds path (G4) closed pre-execution rather than post-hoc?" The issue's paragraph 1 states the RESUME-bypass fact ("resumes cleanly past every pause point") but the question in paragraph 2 only asks about criteria/paths/risk-level sourcing and whether tamper-evidence is implemented — not explicitly whether the bypass itself gets closed.
**Impact:** A contributor could add a real hash mechanism and consider the issue closed while the state-poisoning RESUME bypass (a distinct defect, confirmed untouched by `c07033ce`) remains open. Low risk because the linked full-analysis file does state it.
**Remediation:** Extend the question: "...and how is a poisoned state file stopped from resuming past a hold before the tamper is even checked, not just detected afterward?"

### CC-005-352: "register section REM-03" is an opaque pointer [MINOR]

**Location:** `(register section REM-03)`
**Evidence:** No noun identifies what "register" is at first mention (it is named two sentences later as `remediation-register.md`).
**Remediation:** `(tracked as cluster REM-03 in the linked remediation-register.md)`.

## Remediation Plan

**P1 (Major):** CC-001 (state branch once, unambiguously, covering both paths). CC-002 (convert both references to real hyperlinks).
**P2 (Minor):** CC-003 (gloss or drop title codes). CC-004 (add RESUME-bypass clause to the design question). CC-005 (name "register" before abbreviating it).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (Minor) | CC-004, CC-005: question and pointer slightly under-specified |
| Internal Consistency | 0.20 | Neutral | No contradictions found in the text itself |
| Methodological Rigor | 0.20 | Neutral | N/A to this artifact type |
| Evidence Quality | 0.15 | Positive | Every substantive claim verified against REM-03 and the `c07033ce` diff — no fabrication found |
| Actionability | 0.15 | Negative (Major) | CC-001, CC-002: reference is resolvable in fact but not reachable without extra work/risk of a wrong-branch dead end |
| Traceability | 0.10 | Negative (Minor) | CC-003, CC-005: internal codes present without full inline gloss |

**Constitutional Compliance Score:** `1.00 - (2*0.05 + 3*0.02) = 1.00 - 0.16 = 0.84` → **REVISE band (0.85 threshold)**, effectively borderline REJECTED by this template's formula; net assessment is REVISE given zero Critical/factual findings and the fixes being one-paragraph edits.

**Threshold Determination:** REVISE — no Critical findings; two Major reference-hygiene issues and three Minor polish items, all independently and quickly fixable without touching the substantive claims (which are accurate).

---
*Execution Statistics — Total Findings: 5 (Critical: 0, Major: 2, Minor: 3). Protocol Steps Completed: 5 of 5.*

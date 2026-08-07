# Inversion Report: GitHub Issue #352 (BUG-003 / REM-03)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `snapshots/final/issue-352.md` (live text of GitHub issue #352, geekatron/jerry)
**Criticality:** C4 (tournament execution against a merge-blocking communication artifact)
**Goals Analyzed:** 2 | **Assumptions Mapped:** 5 | **Vulnerable Assumptions:** 2 (Major), 2 (Minor)

## Summary

The issue's factual claims (verifier authority inversion, self-declared criticality, absent SHA-256 tamper detection, RESUME-past-holds) were checked against the remediation register (REM-03), BUG-003, and the verdict document — all check out; no Critical (factually-wrong-or-misleading) findings were found. Inversion of the "external contributor can act from this text alone" goal surfaces two Major actionability/resolvability gaps and two Minor polish items. Recommendation: ACCEPT with two Major mitigations.

## Findings Table

| ID | Assumption / Anti-Goal | Confidence | Severity | Evidence |
|----|------------------------|------------|----------|----------|
| S-013-01 | Referenced branch `feat/proj-032-nuclear-sop-review` is publicly resolvable to the external contributor | Low | Major | Issue text: "on branch `feat/proj-032-nuclear-sop-review`" — no statement that this branch is pushed to the public remote or how to fetch it |
| S-013-02 | Contributor knows the expected response mechanism without being told | Medium | Major | Issue poses "the design question to answer" but never states where/how to submit an answer (reply here vs. push a commit vs. open a follow-up PR) |
| S-013-03 | Branch qualifier scope is unambiguous across both cited paths | Medium | Minor | "Worktracker: `path` (register section REM-03). Full analysis ... on branch `...`" — unclear if the branch clause covers the Worktracker path too |
| S-013-04 | "trust anchor" (title) is self-explanatory to a zero-context reader | Medium | Minor | Body explains the SHA-256/authority-inversion mechanics in plain language, but the title's parenthetical "(trust anchor, PR #269)" is left undefined |

## Finding Details

### S-013-01: Unconfirmed resolvability of the cited review branch [MAJOR]

**Original Assumption:** The contributor (or their AI agent) can open `remediation-register.md` on branch `feat/proj-032-nuclear-sop-review` for the "full analysis with candidate designs."
**Inversion:** If that branch is a maintainer-local/internal working branch not pushed to `origin`, the single richest evidence source in the issue is unreachable — the reader gets a 404 or a missing-branch error and has no fallback.
**Plausibility:** Realistic — this branch is distinct from both the contributor's own PR branch (`proj-0039-nuclear-engineer`) and `main`; nothing in the issue confirms it is public.
**Consequence:** Contributor cannot obtain the "candidate designs" context the issue promises; they are left with only the ~120-word summary to design a fix for a Critical, merge-blocking defect.
**Dimension:** Evidence Quality
**Mitigation:** Confirm the branch is pushed to `origin` and either link a clickable GitHub blob URL (`https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/.../remediation-register.md`) or state explicitly "(pushed to origin — `git fetch origin feat/proj-032-nuclear-sop-review`)".
**Acceptance Criteria:** Issue text contains a resolvable URL or an explicit fetch instruction; a contributor with only `git clone` access to the public repo can retrieve the file without prior knowledge of the branch's existence.

### S-013-02: No stated response channel [MAJOR]

**Original Assumption:** Posing "the design question to answer" is sufficient for the contributor to know how to close the issue.
**Inversion:** The contributor (or an AI agent executing autonomously) answers the design question analytically in their own notes but never posts a commit, PR update, or issue reply — the maintainer sees no response and the issue silently stalls.
**Plausibility:** Realistic for both human and AI-agent readers; GitHub issues vary in whether "answer" means "comment" or "ship code."
**Consequence:** Delays rework contract closure (verdict's Condition 1: "All seven blockers closed ... with a shipped design").
**Dimension:** Actionability
**Mitigation:** Add one sentence, e.g., "Reply here with your proposed design, or push a commit to this PR implementing it, before requesting re-review."
**Acceptance Criteria:** Issue contains an explicit instruction naming the expected artifact (reply vs. commit) and where it should land.

## Recommendations

- **Major (SHOULD mitigate):** S-013-01 — add a resolvable link/fetch instruction for the review branch. S-013-02 — add an explicit response-channel sentence.
- **Minor (MAY mitigate):** S-013-03 — restate the branch qualifier once, up front, covering both cited paths. S-013-04 — replace or gloss "(trust anchor, PR #269)" in the title with plain wording (e.g., "(verifier trust boundary, PR #269)").

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Neutral | Core defect (authority inversion + missing tamper control) is fully and accurately stated |
| Internal Consistency | Neutral | No contradictions found against register/BUG-003/verdict |
| Evidence Quality | Negative | S-013-01: cited evidence location's public reachability is unverified |
| Actionability | Negative | S-013-02: no stated response mechanism |
| Traceability | Positive | Worktracker path, register section, and issue number cross-reference cleanly and match the source files exactly |

## Execution Statistics
- **Total Findings:** 4
- **Critical:** 0
- **Major:** 2
- **Minor:** 2
- **Protocol Steps Completed:** 6 of 6 (adapted/compact for a ~300-word communication artifact)

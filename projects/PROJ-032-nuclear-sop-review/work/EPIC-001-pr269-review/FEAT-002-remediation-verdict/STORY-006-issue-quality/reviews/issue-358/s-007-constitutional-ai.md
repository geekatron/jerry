# Constitutional Compliance Report: GitHub Issue #358 (BUG-009 / REM-09)

**Strategy:** S-007 Constitutional AI Critique (adapted for a communication artifact)
**Deliverable:** `snapshots/final/issue-358.md` (live text of GitHub issue #358, geekatron/jerry)
**Criticality:** C4 (tournament execution)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-007)
**Constitutional Context:** Mission-derived principles for this artifact type — factual accuracy, self-containedness, actionability, resolvable references, honest severity/status framing, concision — verified against the remediation register (REM-09), the remediation log, the c07033ce diff, and the PR #269 verdict.

## Summary

**PARTIAL compliance.** 0 Critical, 1 Major, 2 Minor. Every factual claim checked (the three registration-bookkeeping gaps, the fix content, the CI link, the 89→93 count, the commit/branch identifiers) verified accurate against ground truth — no fabrication, no misleading framing found. The findings are narrow: one reference in the Tracking line omits a required filename, forcing a directory lookup, and the Tracking line as a whole carries internal-review plumbing of low value to the external reader. **Score: 0.91 (REVISE, near threshold).** Recommend targeted revision, not rejection.

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| S-007-01 | Resolvable References | MEDIUM | Major | Tracking line gives a directory (`.../work/BUG-009-registration-enforcement-surfaces`) with no filename, unlike the adjacent register reference which names `remediation-register.md` explicitly | Actionability |
| S-007-02 | Self-Containedness / Concision | SOFT | Minor | Tracking line exposes the reviewer's own branch (`feat/proj-032-nuclear-sop-review`) and a multi-segment internal work-item path with no action attached for the contributor | Completeness |
| S-007-03 | Honest Severity Framing | SOFT | Minor | Issue omits that REM-09 is triaged as a **Critical**-severity cluster in the register (it reads only as routine "mechanical" cleanup); action is unaffected ("nothing for you to do") but the omission slightly understates why this mattered | Traceability |

## Finding Details

### S-007-01: Worktracker reference not resolvable without a directory lookup [MAJOR]

**Principle:** Resolvable references — a path in an issue meant for an external agent to act on should resolve directly, not require browsing.
**Location:** Tracking paragraph, first clause.
**Evidence:** `worktracker \`projects/PROJ-032-nuclear-sop-review/work/BUG-009-registration-enforcement-surfaces\`` — this is a directory. The actual entity file is `BUG-009-registration-enforcement-surfaces.md` inside it (confirmed to exist). The very same sentence names the *register* file explicitly (`remediation-register.md`) but not the worktracker file, an inconsistent level of precision within one sentence.
**Impact:** An agent trying to `cat`/`Read` the given path gets a directory-not-a-file error and must list the directory to proceed — a small but real lookup tax that the register-path half of the same sentence does not impose.
**Dimension:** Actionability
**Remediation:** Append the filename: `.../work/BUG-009-registration-enforcement-surfaces/BUG-009-registration-enforcement-surfaces.md`.

### S-007-02: Tracking line carries internal-review plumbing irrelevant to the contributor [MINOR]

**Principle:** Self-containedness / concision — reference material in the issue should either be actionable for the reader or clearly marked as maintainer-only provenance.
**Location:** Tracking paragraph, second clause.
**Evidence:** "...under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`."
**Impact:** These paths live on the reviewer's branch, not the contributor's PR branch — the contributor cannot check them out from their own fork/branch context, and nothing in the issue asks them to. Presented unmarked, a careful reader may waste time trying to resolve a reference that isn't theirs to resolve.
**Dimension:** Completeness (of the "what do I do with this" signal)
**Remediation:** Either drop the deep sub-path/branch clause (the worktracker ID plus issue number is enough for cross-linking) or add a four-word qualifier such as "— maintainer traceability only."

### S-007-03: Underlying triage severity (Critical) not surfaced [MINOR]

**Principle:** Honest severity/status framing — the reader should be able to gauge how serious the underlying defect was, even when the required action is "none."
**Location:** "What this is" opener.
**Evidence:** Register classifies REM-09 as **Critical** severity, FIX-NOW disposition (`remediation-register.md`, Cluster Index). The issue text calls it one of "seven mechanical fixes" with "nothing for you to do" — accurate on required action, silent on triage severity.
**Impact:** Low — the contributor's action is correctly "nothing," so the omission does not misdirect. It only slightly understates, for a reader assessing PR #269 as a whole, how much of the Critical-finding mass this single fix retired.
**Dimension:** Traceability
**Remediation:** Optional one-clause addition, e.g. "(triaged Critical; already resolved)" — low priority, does not block acceptance.

## Fact-Check Ledger (verified, no discrepancy found)

- Three defects (H-22 sentence + L2-REINJECT gap; "nuclear workflow" → `/orchestration` misroute; AGENTS.md 89 vs. 93) — all match register REM-09 groups G1–G3 and the c07033ce diff.
- Fix description (compound trigger `"nuclear workflow" OR "nuclear sop"`; H-22 sentence and L2-REINJECT comment updated; AGENTS.md nav row + summary row + total 93) — matches diff verbatim.
- Routing mechanics ("phrase matches beat numeric priority," collision resolved "without touching `/orchestration`'s row") — matches Compound Trigger Specificity Override (Step 2) and the diff's scope (only the nuclear-sop row changed).
- Commit `c07033ce` on branch `proj-0039-nuclear-engineer`, CI 15/15 green at run 31174766440 — matches evidence pack and remediation log.
- "Fix is already on your branch" / "stays open until PR #269's disposition is decided" — consistent with the terminal verdict (REWORK: keep PR #269 open, do not merge at `c07033ce`).
- No occurrence of the literal internal codes H-22, L2-REINJECT, REM, or CC-IDs used *without* plain-English explanation in the body text — all are paraphrased before or in place of the code.

## Remediation Plan

**P1 (Major):** S-007-01 — add the missing filename to the worktracker reference.
**P2 (Minor):** S-007-02 — trim or qualify the internal-review sub-path/branch clause. S-007-03 — optionally note the Critical triage severity.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Slightly Negative | S-007-02: internal-only reference presented without a "why you're seeing this" marker |
| Internal Consistency | 0.20 | Neutral | No contradictions found in the issue text itself |
| Methodological Rigor | 0.20 | Neutral | N/A to this artifact type |
| Evidence Quality | 0.15 | Positive | All load-bearing claims (defects, fix, CI, counts) independently verified against source diff and register |
| Actionability | 0.15 | Negative | S-007-01: one reference forces a directory lookup |
| Traceability | 0.10 | Slightly Negative | S-007-03: triage severity not carried into the issue |

**Constitutional Compliance Score:** 1.00 − (1 × 0.05 Major + 2 × 0.02 Minor) = **0.91**
**Threshold Determination:** REVISE (0.85–0.91 band; below the 0.92 gate) — the deliverable is accurate and largely self-contained; the gap is narrow and easily closed by S-007-01's fix alone (which would raise the score to 0.96, PASS).

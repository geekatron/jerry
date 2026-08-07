# Inversion Report: GitHub Issue #357 (issue-357.md)

**Strategy:** S-013 Inversion Technique (adapted, compact form for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-357.md` — live text of GitHub issue #357, geekatron/jerry
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-013)
**Goals Analyzed:** 4 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 4

## Summary

Inverted the deliverable's goals (external comprehension, independent verification, correct no-action framing, resolvable references) and stress-tested the assumptions the text relies on. Fact-checking against the remediation register, log, and evidence pack found **no factual errors** — every named file, count (five registration files), commit (`c07033ce`), CI result, and cross-reference (issue #353 → REM-04) matches ground truth, and both the branch path and CI run resolve publicly. The vulnerabilities found are self-containedness and actionability gaps, not factual ones. **Recommendation: ACCEPT with two Major mitigations** (title jargon, undefined disagreement path).

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| S-013-01 | Reader can ignore the title's internal ID prefix and still orient | Anti-Goal | High | Major | Title: "PROJ-032/BUG-008: nuclear-sop — docs claimed…" | Actionability |
| S-013-02 | "Nothing to do unless you disagree" implies a known disagreement path | Assumption | Medium | Major | "Nothing for you to do unless you disagree with the fix." (no where/how stated) | Actionability |
| S-013-03 | "(see #353)" needs no gloss because context nearby explains it | Assumption | Medium | Minor | "the validation evidence… had been invalidated (see #353)." | Completeness |
| S-013-04 | "corrupted routing if pasted" is an acceptable lay paraphrase of the actual mechanism | Assumption | Medium | Minor | Register REM-08 G2: re-pasting "would collide with /user-experience and regress the live routing table" | Evidence Quality |

## Finding Details

### S-013-01: Title exposes an unglossed internal ID as the first thing the reader sees [MAJOR]

**Type:** Anti-Goal (violates "zero governance knowledge" goal at the point of maximum visibility)
**Original assumption:** A title prefix like "PROJ-032/BUG-008" is harmless bookkeeping the reader can skip past.
**Inversion:** The title is the *only* part of the issue visible in a GitHub issue list, notification email, or search result. An external contributor or their agent triaging a batch of notifications sees "PROJ-032/BUG-008:" before any of the plain-language content that explains it — the one field with zero token budget for explanation carries the one piece of unglossed internal shorthand in the whole artifact.
**Plausibility:** High — this is exactly how GitHub surfaces issues outside the full-body view (list, digest, `gh issue list`).
**Consequence:** Minor friction, not a wrong-path outcome (the body immediately self-explains) — hence Major, not Critical. But it is the single clearest violation of the stated mission ("zero knowledge of this repo's internal governance") in the artifact.
**Evidence:** Deliverable line 1 title; contrast with the body, which never uses an internal ID as load-bearing content.
**Dimension:** Actionability (first-glance triage signal is jargon, not substance).
**Mitigation:** Move the internal cross-reference out of the title into the "Tracking" footer only (it is already duplicated there); title should read plainly, e.g. "nuclear-sop: SKILL.md registration/status docs were false or contradictory — fixed on your branch."
**Acceptance Criteria:** Title contains zero internal ticket-ID tokens; internal IDs appear only in the Tracking section.

### S-013-02: "Nothing to do unless you disagree" does not say how to disagree [MAJOR]

**Type:** Assumption (implicit: reader will find the right channel unprompted)
**Original assumption:** Stating "nothing for you to do" is sufficient because the exception case (disagreement) is rare.
**Inversion:** A contributor who *does* disagree has no stated channel (comment on this issue? comment on PR #269? which one is authoritative?), no deadline, and no indication of who reads it. Under inversion, the exact case this sentence carves out — disagreement — is the one case left completely unspecified, while the common case (no action) is over-specified.
**Plausibility:** Medium-High — disagreement is the most likely reason a contributor would ever reply to this issue at all.
**Consequence:** Not misleading, but forces the reader to guess or search other issues/PR threads for the expected reply surface — a lookup this artifact's own design (self-contained, actionable) is meant to avoid.
**Evidence:** "Nothing for you to do unless you disagree with the fix." — no comment target given anywhere in the issue.
**Dimension:** Actionability.
**Mitigation:** Add one clause: "If you disagree, comment on this issue or on PR #269 — the maintainer will read either."
**Acceptance Criteria:** Text names at least one concrete reply surface for the disagreement branch.

### S-013-03: Cross-reference "(see #353)" carries no inline gloss [MINOR]

**Type:** Assumption
**Original assumption:** The preceding clause ("the validation evidence behind the higher-risk approval had been invalidated") makes the pointer's subject obvious enough that #353 needs no gloss.
**Inversion:** If the clause were trimmed or skimmed, "(see #353)" alone is an unexplained internal code — exactly the pattern the mission statement calls out. Verified against the ground truth: #353 = BUG-004 = REM-04 (QG-E4 validation-evidence invalidation), so the pointer is *accurate*, just terse.
**Plausibility:** Medium — the clause is currently intact and does carry enough context, so this is a polish item, not a comprehension blocker.
**Consequence:** Minor: a reader wanting more detail must open #353 cold with only "validation evidence… invalidated" as orientation.
**Evidence:** "…had been invalidated (see #353)."; confirmed mapping in `remediation-log.md` DEFER-REWORK table (REM-04 → BUG-004 → #353).
**Dimension:** Completeness.
**Mitigation:** "(re-validation tracked in #353)" — five extra words, removes the bare-number reference.
**Acceptance Criteria:** #353 reference includes a same-clause noun phrase describing what it tracks.

### S-013-04: "corrupted routing if pasted" is a looser paraphrase than the source mechanism [MINOR]

**Type:** Assumption (evidence fidelity)
**Original assumption:** "Corrupted routing" is an acceptable lay simplification of the register's actual claim.
**Inversion:** The register (REM-08 G2) says re-applying the stale row "would collide with /user-experience and regress the live routing table" — a specific priority collision with a named peer skill, not generic corruption. "Corrupted" is not wrong in effect (routing would misbehave) but drops the more precise, verifiable claim in favor of a vaguer one.
**Plausibility:** Low risk of actually misleading — the reader is told "nothing to do," so no action rides on this word choice.
**Consequence:** Small loss of evidence traceability; a reader who checks the diff would see a collision/regression, not literal "corruption."
**Evidence:** remediation-register.md REM-08 G2 vs. issue-357.md body sentence 2.
**Dimension:** Evidence Quality.
**Mitigation:** "…would have collided with another skill's routing priority and reverted the live routing table if pasted."
**Acceptance Criteria:** Wording matches the register's collision/regression framing rather than generic "corruption."

## Recommendations

- **Major (SHOULD fix):** S-013-01 — strip the internal ID prefix from the title; keep it in the Tracking footer only.
- **Major (SHOULD fix):** S-013-02 — name a concrete reply surface for the disagreement branch.
- **Minor (MAY fix):** S-013-03 — add a 3-5 word gloss to the `#353` pointer.
- **Minor (MAY fix):** S-013-04 — tighten "corrupted routing" to match the register's collision/regression language.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (slight) | S-013-03: bare issue-number pointer |
| Internal Consistency | 0.20 | Neutral | No contradictions found; all counts/claims internally consistent |
| Methodological Rigor | 0.20 | Neutral | N/A to a communication artifact |
| Evidence Quality | 0.15 | Negative (slight) | S-013-04: paraphrase loosens a verifiable claim |
| Actionability | 0.15 | Negative | S-013-01, S-013-02: title jargon + undefined disagreement path |
| Traceability | 0.10 | Positive | Tracking footer's worktracker/branch path verified to resolve publicly on GitHub |

**Fact-check note:** all quantitative claims in the issue (five registration files, commit `c07033ce`, CI 15/15 at run `31174766440`, `#353` → REM-04 mapping, worktracker path) were checked against `remediation-register.md`, `remediation-log.md`, `evidence-c07033ce.md`, and live GitHub (branch tree + Actions run) — all confirmed accurate and resolvable. No Critical findings.

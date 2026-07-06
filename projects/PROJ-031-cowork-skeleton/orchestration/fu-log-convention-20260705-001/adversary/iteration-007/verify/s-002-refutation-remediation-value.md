# S-002 Refutation Pass — Remediation-Value Lens (iteration-007)

> Panel: adversarial refutation, remediation-value lens. Target: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-002-findings.md`.
> Rule applied: DEFAULT REFUTED IF UNCERTAIN. A Critical is VERIFIED only if (a) the underlying defect claim holds against current deliverable text, AND (b) fixing it would materially change adoption outcomes (not churn), AND (c) the proposed remediation does not require new machinery (lint/file/field/subsystem) against the project's anti-bloat doctrine.
> Constitutional: P-003 no subagents. P-020 draft-only (no writes outside `projects/`). P-022 file+line citations below; inference labelled.

## Criticals in Scope

The S-002 findings table lists exactly one Critical: `DA-001-iter7` (DA-002/DA-003 are Major, DA-004 is Minor — out of scope for this pass, which is Criticals-only per the task brief).

---

## DA-001-iter7 — Near-cap `grep -c` id-minting shortcut derives the wrong canonical id after the first segment

**Verdict: VERIFIED**

**Claim recap:** the near-cap id-minting instruction ("derive the next id from a deterministic `grep -c '^## FU\.'` count") appears identically in `feedback-decision-log-convention-design.md:195`, `staging-feedback-logs/feedback-decision-logs-standards.md:28` (LOG-M-006), and `staging-feedback-logs/examples-appendix.md:173`. In none of the three does the text state that the `grep -c` count must be added to the segment's starting canonical id (visible only in the Segment Index, e.g. `staging-feedback-logs/examples-appendix.md:141` `| 2 | FEEDBACK-LOG.md (ACTIVE) | FU.50 – … |`). Confirmed by direct read: `feedback-decision-log-convention-design.md:195`'s Cap row and the Segment Index row two lines below it (`:199`) never cross-reference each other's arithmetic, and `examples-appendix.md:173`'s grep-c sentence sits in the same paragraph as an explicit Segment-Index-baseline instruction for the "just rotated" case ("take the highest id in the Segment Index's id-range and add 1") without extending that same combine-with-baseline pattern to the near-cap case one sentence later. Worked numerically against the design's own example data: a Segment-2 ACTIVE file holding `FU.50`–`FU.94` (45 headings) yields `grep -c` = 45; naively using 45 as "the next id" collides with the already-used `FU.45` in sealed Segment 1 (`FU.0`–`FU.49`, `examples-appendix.md:140`). This is a genuine, previously-unflagged specification gap in the design's own most load-bearing mechanism (LOG-M-005 collision-resistant ids), not a re-statement of an already-disclosed residual — none of the two id-related disclosures already in the text (the concurrent-writer/last-write-wins residual at `feedback-decision-log-convention-design.md:78`, and the general-case heading-Read approach) address this specific near-cap-shortcut arithmetic gap.

**Remediation-value assessment:** fixing this materially matters for adoption, because it protects the exact guarantee ("unique, monotonic, collision-resistant ids") this design markets as its headline improvement over `[internal-kb]`'s observed `DJ-NNN` collision (Improvement Ledger row 2, `feedback-decision-log-convention-design.md:275`). A silent cross-segment id collision at every post-first-segment rotation boundary is not a cosmetic gap — it recreates, in the new scheme, the exact failure class the new scheme exists to prevent, and the failure is silent (the id-integrity lint per `feedback-decision-logs-standards.md:82` checks contiguity/orphans within read segments, not a newly-minted id against an older sealed segment's already-used range — so the bug is not self-detecting). This is not churn: it is a correctness fix to the core id mechanism a multi-session, multi-rotation adoption will exercise repeatedly (roughly every ~50 entries per `feedback-decision-log-convention-design.md:195`'s own cap math).

**Anti-bloat check:** the proposed fix ("state the correct formula explicitly — next id = segment's starting canonical id (from the Segment Index) + the `grep -c` count — in all three locations," per the finding's own Response Required) is a pure wording correction. It adds zero new lint, zero new file, zero new field, and zero new subsystem — it only makes explicit an arithmetic step using data (the Segment Index's `id-range` column) that already exists in the shipped design. This matches the project's own established remediation pattern for every prior Critical in this convention (per `restore-notes.md:22-29`, all six iteration-006 Criticals closed by wording/disclosure, zero machinery added), so the fix does not trip the "fixes that add machinery are refuted" filter.

**Conclusion:** the defect claim holds against current text, the fix is materially consequential to the design's core adoption-trust claim, and the remediation is wording-only. VERIFIED under the remediation-value lens.

---

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| DA-001-iter7 | VERIFIED | Real, previously-undisclosed arithmetic gap in the near-cap id-minting shortcut (confirmed against `feedback-decision-log-convention-design.md:195,199`, `feedback-decision-logs-standards.md:28`, `examples-appendix.md:140-141,173`); fix is wording-only (no machinery); protects the design's headline collision-resistance claim — material to adoption, not churn. |

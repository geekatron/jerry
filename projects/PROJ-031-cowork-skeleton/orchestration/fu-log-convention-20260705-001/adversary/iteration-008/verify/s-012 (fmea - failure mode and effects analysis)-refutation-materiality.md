# Refutation Panel — S-012 (FMEA) — Materiality Lens — Iteration 8

> Reviewer: adv-executor (refutation pass) · Lens: materiality — does each Critical genuinely block the convention's four pillars (no lost feedback, burden-free capture, navigable growth, honest metadata)? Improbable edge cases and style/wording points are REFUTED even if literally true. Default: REFUTE IF UNCERTAIN.
> Scope: only Criticals in `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-012-findings.md`. No other iteration-007/008 adversary files read (per instructions), only `iteration-007/restore-notes.md`.
> P-003: no subagents invoked. P-020: draft-only, no writes outside this output file. P-022: file+line citations below; all inferential reasoning labeled.

## Navigation

| Section | Purpose |
|---------|---------|
| [FM-001-i008fmea](#fm-001-i008fmea-verdict-refuted) | Segment-Index-overflow / lint-2 attribution claim |
| [FM-002-i008fmea](#fm-002-i008fmea-verdict-refuted) | Inline-doc dedup key format + missing worked example |
| [Summary](#summary) | Verified/refuted roll-up |

---

## FM-001-i008fmea: Verdict — REFUTED

**Finder's claim:** Design doc `feedback-decision-log-convention-design.md:264` claims the Segment-Index-overflow trigger's "failure is detected by lint 2's contiguity/orphan check," which the finder says directly contradicts the rule file's own Scope-limits item (e) at `feedback-decision-logs-standards.md:85`, which states Segment Index display accuracy is "not checked" by lint 2.

**Refutation:** The two statements describe different failure surfaces, and — decisively for materiality — the design doc's own text a few lines earlier already discloses the bounded, non-lossy real-world consequence independent of which lint is credited. `feedback-decision-log-convention-design.md:199` (Segment index row) states plainly: "the cap still fires and no entry is lost, only the per-segment count drifts down as the log ages" — i.e., regardless of whether any lint "detects" a missed Segment-Index-overflow re-assessment, the design's own text already guarantees the outcome is safe (no data loss, only an earlier seal at ~40 vs ~50 entries). `feedback-decision-logs-standards.md:85` item (e) is about a narrower, distinct question — whether the *displayed* `id-range` in an index row is verified against the true first/last heading of that segment — not about whether skipping the ~100-line re-assessment trigger causes harm. Even taking the finder's wording-precision complaint at face value (the "detected by lint 2" clause is arguably an imprecise attribution), the practical safety fact that matters for the convention's "no lost feedback" pillar is already true and independently stated in the same file, two paragraphs earlier. This is a wording-attribution nuance in a governance rationale sentence, not a defect that endangers captured feedback, capture burden, growth navigability, or metadata honesty — the residual gap ("no owned review date for this trigger") is itself already honestly disclosed in the same sentence. REFUTED as non-material.

---

## FM-002-i008fmea: Verdict — REFUTED

**Finder's claim:** The inline-doc dedup key (`path:line/anchor`) is specified identically but vaguely in three places (`feedback-decision-log-convention-design.md:61`, `feedback-decision-logs-standards.md:51`, `FEEDBACK-LOG.template.md:25`) with no worked example anywhere in `examples-appendix.md`, risking cross-session/cross-model key-computation drift that could cause a silent duplicate re-mint — reproducing the historical highest-RPN Critical (FM-001-i6).

**Refutation:** The dedup "check before minting" instruction (`feedback-decision-logs-standards.md:51`, `FEEDBACK-LOG.template.md:25`, `examples-appendix.md:169`) is executed by the assistant reading and comparing existing Context lines by judgment, not by a program performing byte-exact string-key equality — so a slightly different textual representation of the same file location (line number vs. nearby heading) would still very likely be recognized by the reasoning agent as "the same marker," making the finder's cross-session/cross-model drift scenario an improbable edge case rather than a likely failure mode. `FEEDBACK-LOG.template.md:53` already signals the format is intentionally flexible — `` {path}:{line-or-anchor} `` — treating line-or-anchor as interchangeable, not an unresolved ambiguity. Critically, even granting the worst case (a duplicate is silently re-minted), the design's own stated philosophy already classifies this exact outcome as low-severity and self-correcting: `feedback-decision-log-convention-design.md:91` states over-capture "costs one reviewable entry, never a lost one." A duplicate entry from an inline-doc re-harvest is over-capture, not data loss, and does not block "no lost feedback," "burden-free capture" (capture itself remains a single instruction), or "navigable growth" (one extra reviewable row is not a growth-navigability failure). The missing worked example is a genuine Evidence Quality documentation gap (consistent with the finder's own Major-level post-correction RPN estimate of ~105), but it does not rise to a Critical block on any of the four convention pillars. REFUTED as non-material; downgrade to Major (documentation completeness) is the materiality-consistent classification.

---

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| FM-001-i008fmea | REFUTED | Design doc's own text (`:199`) already discloses the bounded, non-lossy real consequence independent of lint attribution; wording-precision issue only, no pillar blocked. |
| FM-002-i008fmea | REFUTED | Dedup check is LLM-judgment-executed, not string-exact; design doc's own over-capture doctrine (`:91`) already classifies the worst case as a low-severity reviewable duplicate, not lost feedback. Documentation-completeness gap at most (Major), not Critical. |

*No Criticals in this report survive the materiality lens.*

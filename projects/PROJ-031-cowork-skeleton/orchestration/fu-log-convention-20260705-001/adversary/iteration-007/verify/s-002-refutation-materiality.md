# Refutation Panel: S-002 Devil's Advocate — Materiality Lens (iteration-007)

> Lens: MATERIALITY — does the finding genuinely block one of the four stated convention
> purposes (feedback/decisions never lost; operator-burden-free capture; navigable growth;
> honest metadata)? Improbable edge cases and style/wording points are REFUTED even if
> technically true. Default REFUTED if uncertain.
> Scope: Criticals only, per task brief. `s-002-findings.md` names exactly one Critical:
> **DA-001-iter7**.
> Constitutional: P-003 no subagents; P-020 draft-only (no writes outside
> `projects/PROJ-031-cowork-skeleton/`); P-022 citations below are file + line; inferences
> are labelled `[INFERENCE]`.

## Navigation

| Section | Purpose |
|---------|---------|
| [Verdict Summary](#verdict-summary) | One-line disposition |
| [DA-001-iter7](#da-001-iter7-near-cap-grep--c-id-minting-shortcut) | Full refutation analysis |

---

## Verdict Summary

| ID | Severity (as filed) | Verdict | One-line reason |
|----|---------------------|---------|------------------|
| DA-001-iter7 | Critical | **REFUTED** | The design's own L5 lint 2 already reads *every* segment listed in the Segment Index and checks id uniqueness "across all segments," so the exact cross-segment collision this finding describes is a designed, install-gated backstop catch — not a silent, unrecoverable failure. No feedback text is ever lost in the described scenario, only a metadata id label, which the lint mechanism (already specified, not new machinery) flags before merge. |

---

## DA-001-iter7: Near-cap `grep -c` id-minting shortcut

**Finding as filed:** the near-cap id-minting shortcut ("derive the next id from a
`grep -c '^## FU\.'` count") is stated in three places —
`projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:195`,
`projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:28`,
`projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/examples-appendix.md:173` —
without an explicit "+ segment-starting-id offset" clause, so a literal reading would mint a
locally-numbered id (e.g. 45) that collides with an already-used id from an earlier sealed
segment (e.g. `FU.45` in Segment 1). The filer calls this a silent, load-bearing correctness
bug in the id-uniqueness mechanism (LOG-M-005) and asserts the id-integrity lint "may not even
catch" it.

**Refutation (materiality):**

1. **The design's own backstop already catches exactly this collision.** `feedback-decision-log-convention-design.md:236` (L5 lint 2, "Id integrity: uniqueness + monotonicity + contiguity") states ids are checked "unique, strictly increasing, and contiguous **across all segments of each log**" and that "**the pass must read every segment listed in the Segment Index**" to do so. The same wording appears in `staging-feedback-logs/feedback-decision-logs-standards.md:82` ("ids unique, strictly increasing, and contiguous across all segments... `ls *-LOG.*.md`... flags any on-disk segment absent from the Segment Index"). This directly contradicts the finding's Impact claim that the lint "verifies contiguity within the set of segments it reads, not that a newly minted id doesn't collide with an older, sealed segment's already-used id" — the lint's stated scope *is* every segment in the index (sealed + ACTIVE), and uniqueness is checked over that whole set, so a duplicate `FU.45` minted in the ACTIVE segment against an already-used `FU.45` in a sealed segment is precisely a "duplicate id" violation the lint is designed to surface.

2. **No feedback or decision content is lost in the scenario described.** Even in the worst-case literal misread, the entry's Verbatim/Summary/Disposition/Context text is captured and appended correctly — only the numeric id label would be wrong. The convention's first stated purpose ("feedback/decisions never lost," `feedback-decision-log-convention-design.md:30`) concerns the *entry text*, which survives intact; the failure mode here is a metadata-id defect, caught by an already-specified detection mechanism (lint 2) before it can propagate past the install-gated, branch-protected CI check (`feedback-decision-log-convention-design.md:254`, Adoption step 3: lint checks "wired AND required — branch-protected").

3. **The agent executing the shortcut already has the correcting context in view.** The Segment Index the finding says is never cross-referenced (`feedback-decision-log-convention-design.md:199`, "Segment index... lives only in the ACTIVE file") is literally in the same file the LLM is appending to at the moment of minting — it is not a separate lookup requiring a truncation-risking Read. The immediately adjacent case in the same paragraph (`examples-appendix.md:173`, "If the ACTIVE file was just rotated and holds no entry yet, take the highest id in the Segment Index's id-range and add 1") already establishes the baseline-plus-offset pattern the reasoning agent is expected to apply; reading the near-cap sentence as a *literal, context-free* `grep -c` substitution — while textually terse — is an improbable failure mode for the same agent that is simultaneously holding the Segment Index table in context to perform the adjacent computation one sentence earlier.

4. **This is a wording-precision gap, not a broken mechanism** — the finding's own "Response Required" concedes the fix is to state the existing intended formula explicitly, not to add any new lint, field, or subsystem. Per the materiality instruction ("improbable edge cases and style points are REFUTED even if true"), an ambiguity that (a) does not lose data, (b) is caught by an already-designed, already-scoped backstop, and (c) requires an agent to ignore adjacent, in-context correcting information to manifest, does not rise to genuinely blocking the id-uniqueness / navigable-growth / honest-metadata purposes this convention exists to serve.

**Verdict: REFUTED.** Downgrade candidate: Minor/Major wording-precision fix (state the offset formula explicitly in the three cited locations), not a Critical that blocks convention purpose.

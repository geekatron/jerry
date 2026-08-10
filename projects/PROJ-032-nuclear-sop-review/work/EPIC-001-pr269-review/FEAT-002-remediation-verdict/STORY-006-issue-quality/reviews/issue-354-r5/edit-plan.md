# Issue #354 — Round-5 Reconciled Edit Plan

> Quality-gap analysis after 4 scoring rounds (0.57 → 0.84 → 0.90 → 0.8975). Zero Critical findings since r2. One reconciled, ground-truth-checked edit list to clear the 0.92 gate.
> Shorthand: `S6` = `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality`. Ground truth: register REM-05 (`.../STORY-004-remediation/remediation-register.md`), `S6/snapshots/evidence-c07033ce.md`, «PR worktree» git history, `.context/rules/`.

| Section | Purpose |
|---------|---------|
| [1. Persistent deficits](#1-persistent-deficits-why-it-plateaus) | Why the score is stuck at ~0.90 |
| [2. Cross-round contradictions](#2-cross-round-contradictions) | Where the judges' demands conflict |
| [3. Verdicts on reviser-rejected edits](#3-verdicts-on-reviser-rejected-edits) | Ground-truth check of each rejection |
| [4. Final minimal edit list](#4-final-minimal-edit-list) | E1–E4, exact old → new |
| [5. Word-budget ruling](#5-word-budget-ruling) | 450-word allowance NOT triggered |
| [6. Projected score path](#6-projected-score-path) | Arithmetic showing E1–E4 suffice |

---

## 1. Persistent deficits (why it plateaus)

| ID | Deficit | Rounds | Dimension hit |
|----|---------|--------|---------------|
| D1 | **Assignee identity/role accuracy** — the only defect chain never yet closed: wrong handle "geekatner" (r1) → labels unverifiable (r3) → "@malcolm-x-evo (maintainer)" contradicted by persisted ground truth (r4). Sole sub-0.90 dimension in r4 (Rigor 0.85). | r1, r3, r4 | Methodological Rigor |
| D2 | **Evidence persistence for identity claims** — r4's justification rests on an unlogged "verified against live GitHub" assertion with no checkable artifact. | r3, r4 | Evidence Quality |
| D3 | **Zero-context glossing** — bare "Worktracker" label unglossed for STORY-006's stated external audience; sibling #350 settled the convention. | r4 | Completeness |
| D4 | **Footer authority phrase coherence** — "not maintainer or contributor alone" unmoored once no independent maintainer is among the assignees. | r4 (downstream of D1) | Actionability |
| D5 | **Structural anti-leniency ceiling** — judges hold defect-free dimensions at 0.90–0.91 (r3 IC 0.90 "despite finding no confirmed contradiction"; r4 IC 0.91 "None newly found", capped for single-pass). With every dimension capped ≤ 0.92 and one at 0.85, the composite mathematically cannot exceed ~0.90. The plateau is D1 (the one real defect) + D5 (ceiling on everything else); fixing D1–D4 is the only path that moves the composite. | r3, r4 | all |

## 2. Cross-round contradictions

| ID | Contradiction | Resolution (ground truth) |
|----|---------------|---------------------------|
| C1 | Role mapping demanded three incompatible ways: r1 edit #5 "@victorlau1 (maintainer), @malcolm-x-evo (contributor)" → r3 "verify; a sibling review used the opposite" → r4 reviser applied "victorlau1 (contributor), malcolm-x-evo (maintainer)" → r4 judge: drop label or use "victorlau1's AI agent". | Both "maintainer" claims are wrong. `S6/STORY-006-issue-quality.md` line 28: "the PR #269 author (victorlau1) or their AI agent (malcolm-x-evo)". «PR worktree» history: the nuclear-sop skill-build commits (587b8397, 82e3d455, 93bbb127 …, 21 commits) are authored by Malcolm — contributor-side work — while the maintainer-remediation commits (c07033ce, 8839891b, bda64202) are authored by geekatron. Correct labels: victorlau1 = contributor/PR author; malcolm-x-evo = victorlau1's AI agent. → E1. |
| C2 | r3 P2 demanded "confirm against the live issue/PR before publishing"; r4 did exactly that (gh pr view) and was penalized because an unlogged live check is not citable evidence. | Demand-as-stated is unsatisfiable; satisfy its intent with persisted sources (STORY-006 line 28 + PR-branch commit authorship, both checkable in-repo). → E4. |
| C3 | r2 P4 demanded an in-clause caveat on "would resolve"; r4 removed that caveat as redundant after r3's input-not-recommendation reframe. | Resolved: r4 judge confirmed the reframe introduces no contradiction (IC 0.91) and the caveat's content survives in the stop-instruction + BUG-001 sentence. Do NOT restore the caveat. |
| C4 | r1 demanded role labels; r4 judge notes all six sibling issues use an unlabeled assignee line. | Keep labels: #354 is the only issue whose mechanic is an owner ruling and the only one with geekatron additionally assigned (STORY-006 AC). Use the r4 judge's own sanctioned label text. → E1. |

## 3. Verdicts on reviser-rejected edits

| # | Rejected/superseded demand | Reviser action | Verdict vs. ground truth |
|---|---------------------------|----------------|--------------------------|
| V1a | r1 edit #5's "@victorlau1 (maintainer)" | r4 reviser rejected as swapped | **Rejection RIGHT.** victorlau1 is the PR author (contributor side; 4 commits total vs. Malcolm's 21 skill-build commits on the branch). |
| V1b | (replacement) "@malcolm-x-evo (maintainer) … write-access collaborator with maintainer-edit commits on the PR branch" | r4 reviser asserted | **Replacement WRONG.** STORY-006 line 28 defines malcolm-x-evo as victorlau1's AI agent; the maintainer-edit commits on the PR branch (c07033ce, 8839891b, bda64202) are geekatron's, not malcolm-x-evo's — the justification attributes the owner's remediation commits to the wrong actor. r4 judge's rejection of the label is upheld. |
| V2 | r2/r3's in-clause "subject to the owner's ruling" caveat | r4 reviser dropped as redundant post-reframe | **Supersession RIGHT.** Confirmed by r4 judge (IC 0.91, no contradiction); content preserved elsewhere in the same paragraph. |
| V3 | r4 note's closing claim "No required edit was rejected" | — | **Inaccurate in spirit** — the label swap was a rejection of a previously demanded mapping; r5 note must not repeat the framing (→ E4). |

No other reviser rejection exists in the note chain for #354.

## 4. Final minimal edit list

All edits verified against REM-05, `S6/snapshots/evidence-c07033ce.md`, «PR worktree», and BUG-005. No other change is authorized — every remaining sentence was verified accurate by r3/r4 and must not be disturbed (especially the commit-pinned b2cf2966 URLs and the two-anchor/three-file clause).

**E1 — assignee label (body; fixes D1, r4-P1).**
Old: `@malcolm-x-evo (maintainer)`
New: `@malcolm-x-evo (victorlau1's AI agent)`

**E2 — footer authority phrase (Tracking footer; fixes D4, r4-P4).**
Old: `severity critical; requires owner authority, not maintainer or contributor alone.`
New: `severity critical; requires owner authority — per REM-05, a maintainer patch or contributor edit choosing either branch would silently make the ruling.`
(Register-verbatim rationale; survives the corrected assignee labels.)

**E3 — Worktracker gloss (Tracking footer; fixes D3, r4-P3).**
Old: `Worktracker: [BUG-005-h36-governance-ruling.md](…)`
New: `Worktracker (this repo's internal work-item record): [BUG-005-h36-governance-ruling.md](…)`
(Matches sibling #350's settled convention verbatim.)

**E4 — editorial-note correction (HTML comment; fixes D2, r4-P2, V3).** Replace item (1) and the closing sentence of the round-4 note with:
`(1) Assignee labels — r5 ground-truth reconciliation: "@victorlau1 (contributor; PR author)" stands; r4's "@malcolm-x-evo (maintainer)" and its "write-access collaborator with maintainer-edit commits" justification are withdrawn as factually wrong. Persisted sources: STORY-006-issue-quality.md line 28 defines malcolm-x-evo as the PR author's AI agent ("the PR #269 author (victorlau1) or their AI agent (malcolm-x-evo)"); PR-branch authorship shows the nuclear-sop skill-build commits (587b8397, 82e3d455, 93bbb127) authored by Malcolm (contributor side) while the maintainer-remediation commits (c07033ce, 8839891b, bda64202) are geekatron's. No unlogged live-GitHub assertion is used as evidence. (6) r5: Tracking authority line reworded to REM-05's rationale; Worktracker glossed per issue-350's convention. One prior demanded edit is rejected as factually wrong: r1's "@victorlau1 (maintainer), @malcolm-x-evo (contributor)" mapping — the victorlau1 half is contradicted by the sources above, and the malcolm-x-evo half is imprecise (the author's AI agent, not an independent second contributor); r4's swap direction for victorlau1 is retained, its malcolm-x-evo label corrected.`
Keep note items (2)–(5) unchanged (they document facts r4 verified directly).

## 5. Word-budget ruling

**The 450-word allowance is NOT triggered.** Binding dimension in r4 is Methodological Rigor (0.85) — an accuracy defect, not a completeness gap. Completeness sits at 0.91 and its sole outstanding gap (E3) lives in the Tracking footer, which is excluded from the count. Current body (title through paragraph 2): **325 words**. E1 adds +2; E2–E4 are footer/comment. **Budget for r5: 340 body words** (325 + headroom); any growth toward 450 would be unjustified padding and risks the r4-noted density concern.

## 6. Projected score path

E1 removes the only confirmed factual error (Rigor 0.85 → ≥0.93 band: every substantive claim then ground-truth-verified with persisted citations); E4 clears the Evidence citation gap (0.90 → 0.92); E3 clears the last Completeness gap (0.91 → 0.92); E2 clears r4-P4 (Actionability 0.91 → 0.92); Traceability holds at 0.92. Composite: 0.2·(0.92 + 0.91 + 0.93) + 0.15·(0.92 + 0.92) + 0.1·0.92 = **0.920** even if IC stays capped at 0.91 — at gate; any IC credit for the second independent read (r4-P5) clears it with margin. Per RT-M-010 this is the focused round the r4 judge said "has a credible path to >= 0.92"; if r5 still plateaus, escalate to the owner rather than iterate (two more flat rounds trip the circuit breaker).

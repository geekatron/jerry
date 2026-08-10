# Issue #354 — Round-6 Reconciled Edit Plan

> After the r5 3-judge panel (J1 0.9165 PASS / J2 0.907 REVISE / J3 0.906 REVISE — median ~0.91 vs the 0.92 gate, zero Critical), every remaining sub-0.92 dimension traces to the HTML editorial comment or to one vague body clause — not to any body fact. One judge finding (J3's "fabricated convention") is itself factually wrong and is overruled here against ground truth.
> Shorthand: `S6` = `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality`. Ground truth: register REM-05 (`.../STORY-004-remediation/remediation-register.md`), `S6/snapshots/evidence-c07033ce.md`, «PR worktree» files + git history, `.context/rules/`, `S6/STORY-006-issue-quality.md`, `S6/snapshots/published/`.

| Section | Purpose |
|---------|---------|
| [1. Persistent deficits](#1-persistent-deficits) | Why r5 still sits at ~0.91 |
| [2. Cross-round and intra-panel contradictions](#2-cross-round-and-intra-panel-contradictions) | Conflicting demands, with ground-truth resolutions |
| [3. Verdicts on reviser-rejected edits](#3-verdicts-on-reviser-rejected-edits) | Every rejection in the note ledger, checked |
| [4. Final minimal edit list](#4-final-minimal-edit-list) | E1–E9, exact old → new |
| [5. Word-budget ruling](#5-word-budget-ruling) | 450 allowance NOT triggered; ceiling 345 |
| [6. Projected path and circuit breaker](#6-projected-path-and-circuit-breaker) | Score arithmetic; RT-M-010 note |

---

## 1. Persistent deficits

| ID | Deficit | Rounds | Dimension hit |
|----|---------|--------|---------------|
| P1 | Identity/label accuracy chain — CLOSED in r5 (all 3 judges verify "@malcolm-x-evo (victorlau1's AI agent)" against `S6/STORY-006-issue-quality.md` line 28). No longer a deficit. | r1→r4 | Methodological Rigor |
| P2 | **Audit-trail integrity (new r5 deficit class).** Every r5 sub-0.90 score traces to the HTML comment: J2 IC 0.89 — note item (5) misquotes the body ("is equally open" vs body's "remains open"; verified real); J3 IC 0.90 — header says "round 4" while items (1)/(6) are r5-labeled (verified real); J3 Rigor 0.89 — "per issue-350's convention" read as fabricated (J3 is wrong — §2 K1 — but the citation named no file, inviting the misread); J2 EQ 0.91 — eng-team "no hop-ceiling machinery" claim has no sourcing note in the trail. Pattern across r4→r5: each revision's *justification prose* becomes the next round's fact-check attack surface. | r4, r5 | IC, Rigor, EQ |
| P3 | **One vague body clause** — "confirm the chosen reading still applies once that topology is set" names no actor, mechanism, or location (J2 Act 0.89 / Comp 0.90). | r5 | Actionability, Completeness |
| P4 | **Anti-leniency structural ceiling** — clean dimensions are capped at 0.90–0.93 (single-pass verification, no-cross-validation caps). With caps ≈0.92, any one dimension at 0.89 pins the composite at ~0.905–0.91. The only lever is removing the 0.89s (P2, P3); polishing already-clean dimensions moves nothing. | r3–r5 | all |
| P5 | **Body density** — para-1 mega-sentence flagged r4 (readability) and r5 J1 (misparse risk; IC held 0.91). Never yet addressed. | r4, r5 | Internal Consistency |
| P6 | Two small verified-by-this-analysis staleness/nuance gaps no judge could fully check without git access: (a) note item (4) says origin is "pushed at exactly b2cf2966…" — the branch tip has since advanced; b2cf2966 remains an ancestor of origin (verified via `git merge-base --is-ancestor`), so the phrasing, not the pin, is stale; (b) J1's Rigor nuance: the rules file *itself* repeats the automatic-reversion/Phase-1-delivery language outside NS-H-08 («PR worktree» `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` line 286, "### Governance Deadline" under "## 3-Hop vs. 4-Hop Mode Selection") — body framing stays REM-05-verbatim (no exclusivity claim), but the trail should record the nuance. | r5, r6 | Rigor, EQ |

## 2. Cross-round and intra-panel contradictions

| ID | Contradiction | Resolution (ground truth) |
|----|---------------|---------------------------|
| K1 | **J1 vs J3 on the Worktracker gloss.** J1: "independently confirmed to also appear in sibling issue #350's current text — genuine convention match." J3: "fabricated — none of the six available sibling snapshots use this gloss." | **J1 is right; J3 is wrong.** `S6/revised/issue-350.md` line 17 (mtime 2026-08-07 12:59, i.e. before the r5 revision of #354 on 2026-08-10) and `S6/snapshots/published/issue-350.md` line 17 (the text actually published to GitHub) both carry the identical "Worktracker (this repo's internal work-item record)" gloss. J3 sampled only `S6/snapshots/issue-350.md` and `S6/snapshots/final/issue-350.md` — both pre-gloss text states. Keep the gloss; fix the citation so it names the exact file (→ E6), and add the STORY-006 audience-AC justification J3 itself endorsed as independently defensible. |
| K2 | J1 PASS (0.9165) vs J2/J3 REVISE (0.907/0.906). | Not a demand conflict; it identifies the binding fixes as J2's and J3's lists. J1's items are non-blocking margin. |
| K3 | J3: "no change to the rendered issue body is required" vs J2: body edit required (confirm-mechanism clause). | No true conflict — J3's statement was scoped to its own findings (all comment-side). Apply J2's body edit (→ E1). |
| K4 | J1-P2 demands the assignee-role citation be moved into the visible body ("(per STORY-006)"), while J2's Traceability 0.93 explicitly *credits* the text for omitting Jerry-internal codenames per STORY-006's audience AC ("without … knowing Jerry-internal codenames"). | **Decline J1-P2** (not factually wrong — a design trade-off ruled against): a visible "STORY-006" token is exactly the codename class the audience AC excludes and J2 rewards omitting. The label "(victorlau1's AI agent)" is self-explanatory for the rendered audience; provenance stays in the comment for auditors. Documented here as the standing ruling so no future round re-litigates it. |
| K5 | Label chain (r1 ↔ r3 ↔ r4 ↔ r5). | Resolved in r5; all three judges affirm the current mapping. Do not touch. |
| K6 | r3 "confirm against the live issue/PR" vs r4's penalized unlogged live check. | Resolved: persisted-source substitution affirmed by J1 and J2 ("satisfied in substance"). Do not touch. |
| K7 | r2 in-clause caveat vs r4 removal. | Resolved: J2 confirms the post-reframe text is coherent; only the note's *quotation* of it drifted (→ E4). Do not restore the caveat. |

## 3. Verdicts on reviser-rejected edits

Ledger = the rejections/withdrawals recorded in the current text's HTML comment, plus this round's judge-finding overrule.

| # | Rejected/withdrawn demand | Verdict vs ground truth |
|---|---------------------------|--------------------------|
| V1 | r1 edit #5's "@victorlau1 (maintainer)" — rejected by r5 reviser | **Rejection RIGHT.** `S6/STORY-006-issue-quality.md` line 28 ("the PR #269 author (victorlau1)"); «PR worktree» git: Victor 4 commits; skill-build commits 587b8397/82e3d455/93bbb127 authored by Malcolm; maintainer-remediation commits c07033ce/8839891b/bda64202 authored by geekatron (re-verified this round via `git log`). |
| V2 | r1 edit #5's "@malcolm-x-evo (contributor)" — rejected as imprecise | **Rejection RIGHT.** Same line 28: malcolm-x-evo is victorlau1's AI agent, not an independent second contributor. |
| V3 | r4's replacement "@malcolm-x-evo (maintainer)" + "write-access collaborator with maintainer-edit commits" justification — withdrawn in r5 | **Withdrawal RIGHT.** The maintainer-edit commits are geekatron's (git-verified); STORY-006 line 28 contradicts the label. |
| V4 | r2's in-clause "subject to the owner's ruling" caveat — dropped as redundant post-reframe | **Supersession RIGHT.** r4 and r5 (J1, J2) confirm no contradiction; content survives in the stop-instruction + BUG-001 sentence. |
| V5 | r3's "confirm against the live issue/PR before publishing" — replaced by persisted-source verification | **Substitution RIGHT.** Unlogged live checks are not citable evidence; STORY-006 line 28 + commit authorship satisfy the demand's intent (J1, J2 concur). |
| V6 | **New this round:** r5-J3's demand to remove/correct "per issue-350's convention" *as fabricated* | **Premise WRONG — overruled** (see K1). The remedy half (also cite STORY-006's audience AC; make the citation precise) is sound hardening and is adopted in E6. |

## 4. Final minimal edit list

Every remaining body fact was re-verified this round against «PR worktree» (NS-H-08 row line 37; rules-file line 286; SKILL.md sections at lines 245/270; PLAYBOOK.md lines 269/623; `TASK-0039-H36-RULING` greps to exactly the rules file; eng-team SKILL.md sole case-insensitive hop/circuit-breaker match is the References-table row at line 424 citing an external ADR description — no hop machinery in its flow), register REM-05, and `S6/snapshots/evidence-c07033ce.md`. **No other body sentence may be altered** — in particular the three-file/two-anchor clause content, the eng-team input framing, the stop-instruction, the assignee labels, and both Tracking URLs (b2cf2966 re-verified pushed: ancestor of origin; both cited files exist at that commit via `git cat-file -e`).

**Body (rendered) — fixes P3, P5:**

- **E1 (J2-P2/P3; Actionability + Completeness).**
  Old: `This ruling is blocked on the delegation-topology redesign in issue #350 (BUG-001) — confirm the chosen reading still applies once that topology is set.`
  New: `This ruling is blocked on the delegation-topology redesign in issue #350 (BUG-001); once that topology is set, the owner confirms in a follow-up comment on this issue that the chosen reading still applies before the contributor edits the files.`
  (Names actor, mechanism, location, and gate; +16 words.)
- **E2 (J1-P1; IC/readability; punctuation only, 0 words).** Split the para-1 mega-sentence twice:
  `…with no ruling; the rules file…` → `…with no ruling. The rules file…`
  `…(anchor: Phase 1 delivery) — three files, two contradictory mandates, two anchors; and the tracking work-item…` → `…(anchor: Phase 1 delivery). Three files, two contradictory mandates, two anchors — and the tracking work-item…`
- **E3 (J3 Completeness residual; +1 word).**
  Old: `(H-32 parity)` → New: `(H-32: GitHub-issue parity)`

**HTML editorial comment (audit trail) — fixes P2, P6; no rendered-text impact:**

- **E4 (J2-P1 + J3).** In item (5), correct the self-quotation to match the body verbatim: `"the stricter reading is equally open"` → `"the stricter reading remains open"`.
- **E5 (J3-P2).** Header `Editorial notes (round 4):` → `Editorial notes (rounds 4–6):`.
- **E6 (K1/V6).** In item (6), replace `Worktracker glossed per issue-350's convention.` with: `Worktracker glossed to match issue-350's revised/published text — snapshots/published/issue-350.md line 17 carries the identical "this repo's internal work-item record" gloss (the pre-gloss snapshots/ and snapshots/final/ copies do not; check the published/ set) — and independently justified by STORY-006's audience AC (self-contained "without ... knowing Jerry-internal codenames").`
- **E7 (J2-P4).** Append a sourcing line for the eng-team claim: `Eng-team "no hop-ceiling machinery" verified by grep of skills/eng-team/SKILL.md in the PR worktree: the sole case-insensitive hop/circuit-breaker match is a References-table row citing an external ADR's description (line 424); the Orchestration Flow itself contains no hop budget or H-36 analysis.`
- **E8 (P6a).** In item (4), replace `origin/feat/proj-032-nuclear-sop-review is pushed at exactly b2cf29664a30c62266565fcd357a75fd0aaa675a and both cited files exist at that commit (git cat-file -e)` with `commit b2cf29664a30c62266565fcd357a75fd0aaa675a is pushed (ancestor of origin/feat/proj-032-nuclear-sop-review, whose tip has since advanced) and both cited files exist at that commit (git cat-file -e)` — keeps the claim true as the branch moves.
- **E9 (P6b; preempts J1's Rigor nuance).** Append: `(7) r6: the rules file itself also repeats the automatic-reversion/Phase-1-delivery language outside NS-H-08 ("### Governance Deadline" under "## 3-Hop vs. 4-Hop Mode Selection", line 286) — internally self-contradictory even before cross-referencing SKILL.md/PLAYBOOK.md. The body's three-file framing follows REM-05 verbatim and makes no exclusivity claim; the contributor instruction to encode one fallback and one anchor across all three files already covers this internal duplication. J1-P2 (visible "per STORY-006" citation) declined: conflicts with the audience AC's no-internal-codenames goal that Traceability scoring credits.`

## 5. Word-budget ruling

**The 450-word allowance is NOT triggered.** Completeness is not the binding dimension at r5 (J1 0.92, J2 0.90, J3 0.92); the binding deficits are consistency/accuracy items in the editorial comment (P2) and one vague body clause (P3). Measured body count (title line + assignees line + both paragraphs; Tracking footer and HTML comment excluded, per the standing count convention): **327 words**. E1 +16, E2 +0, E3 +1 → **344**. **Ceiling for r6: 345 body words.** Any growth toward 450 would be unjustified padding and would re-aggravate the density finding (P5) both r4 and r5-J1 flagged.

## 6. Projected path and circuit breaker

Per-judge arithmetic: J2 0.907 + IC fix (E4: +0.006) + confirm-mechanism fix (E1: Act +0.0045, Comp +0.004) + eng-team sourcing (E7: +0.0015) ≈ **0.923**. J3 0.906 + note fixes (E4/E5/E6: Rigor +0.006, IC +0.004, EQ +0.003, Trace +0.001) ≈ **0.920**. J1 0.9165 already PASS; E2 addresses its sole 0.91 cap (IC) and E9 its Rigor-margin nuance. All three projected ≥ 0.92 with zero new claims left uncited — E6–E9 deliberately attach a file+line citation to every justification sentence so the audit trail stops generating next-round findings (the r4→r5 failure pattern, P2).

**Process note (RT-M-010):** this is the focused round r5's judges said has a high-confidence path to ≥ 0.92. If the r6 panel still plateaus below gate with zero Critical findings, escalate to the owner for an accept-or-iterate decision instead of a further round — consistent with STORY-006's existing plateau handling.

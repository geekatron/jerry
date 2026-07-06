# S-010 Self-Refine — Findings (iteration-007, Group A)

> **Strategy:** S-010 Self-Refine · **Reviewer:** ps-architect (creator/owner) · **Date:** 2026-07-06
> **Deliverable:** Feedback & Decision Log convention package —
> `design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/` (rule file, 2 templates, examples-appendix, hook-design-note).
> **Criticality:** C3 (AE-002/AE-003 install gate). **Iteration:** 7 of the fu-log tournament (prior composites 0.64→0.65→0.59→0.53→0.47→0.46).
> **Objectivity check:** Medium–high attachment (owner of a 6-round deliverable). Per template Step 1 boundary rule, chose the stricter posture — aimed for 5+ findings, applied leniency-bias counteraction, and cross-checked every claim against the actual repo files rather than trusting the changelog.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall state + headline finding |
| [Verification Results](#verification-results) | Pass/fail against each required check |
| [Findings Table](#findings-table) | All findings, severity-sorted |
| [Finding Details](#finding-details) | Critical + Major expansion |
| [Recommendations](#recommendations) | Prioritized revision actions |
| [Edits Applied](#edits-applied) | What this pass changed (P-002) |
| [Scoring Impact](#scoring-impact) | Dimension-level assessment |
| [Decision](#decision) | Verdict + next action |

## Summary

The design **substance** remains sound: FU.5 segment-rotation is internally consistent (cap, prev/next links, single ACTIVE index, id-only cross-log nav all agree), the FU.6 id/alias scheme is burden-free for the operator and collision-resistant for the logger under the disclosed single-writer discipline, path/internal-ref hygiene is clean (no `[home]/` paths, no employer/codename tokens), tier vocabulary in the shipping artifacts is clean (rule file / templates / appendix: **zero** stray HARD terms), and PROPOSED-DEFAULT markers are intact on Q1–Q5.

However, this pass found **one Critical factual error re-introduced after it had previously been verified false**, plus three Major consistency/criterion issues. The Critical is the exact recurring failure class the tournament has been chasing (a claim not matching its ground-truth evidence): the design doc and the shipping FU.8 examples-appendix assert the live logs hold **"FU.0–FU.9"** and cite **"the live FU.5–FU.9 practice"** as evidence for a design rule — but `grep` of the actual `FEEDBACK-LOG.md` shows only **FU.0–FU.4** (5 entries). The iteration-4 changelog had itself recorded "grep shows the live FEEDBACK-LOG carries only FU.0–FU.4 … no FU.9"; iteration-6 then re-asserted the falsified claim. Leaving a demonstrably-false "verified/live" claim in a shipping artifact touches P-022/P-001, so it was corrected in this pass (see [Edits Applied](#edits-applied)).

## Verification Results

| Required check | Result | Evidence |
|----------------|--------|----------|
| FU.5 rotation internally consistent (cap, links, index, cross-log nav) | **PASS** | Cap "~50 entries or ~800 lines, rotate after crossing entry" identical in rule LOG-M-006 / design L1.4 / appendix walkthrough (seals at FU.49). prev/next linked-list + forward-nav fallback to ACTIVE consistent across rule/template/appendix. Segment Index in ACTIVE-only, Backfill rows carry forward — consistent. Cross-log nav = canonical id only via `Related: <id>` — consistent. |
| FU.6 id scheme burden-free (aliases restart freely) + collision-free for logger | **PASS (scheme)** | Operator never tracks a counter; restarts FU.0 per turn/doc; logger mints monotonic canonical id; alias kept verbatim; `—` when no label. Collision-resistant under single-writer discipline, concurrent-writer residual disclosed. Consistent across all four artifacts. *(Teaching example has a defect — see M1.)* |
| FU.8 examples present, correct, consistent with schema | **FAIL** | Examples present and field-order-consistent, BUT (a) Critical: appendix preamble asserts false "FU.0–FU.9" live range; (b) M1: the "log-growth" item is shown with two identities (`FU.5 (alias: FU.0)` line 34 vs `FU.7 (alias: FU.0.1)` line 68 / preamble line 4). |
| Rule file ≤ ~1,500 tokens | **FAIL (disclosed [USER-DECISION])** | `wc`: 2,240 words / 15,888 chars → ~2,986 tokens (words×4/3) to ~3,972 tokens (chars/4); median ~3,300. ~2× the ~1,500 soft target. Disclosed and openly labeled a P-020 [USER-DECISION] across all iterations — not hidden — but the criterion is not met and the "compress-to-offset" narrative is no longer credible (words ~doubled since iter-2's 1,120). See M3. |
| PROPOSED-DEFAULT markers intact on the open questions | **PASS** | Q1–Q5 table (design lines 285-289) each carry the PROPOSED-DEFAULT column; Q1 marker at line 129; Q3 at hook-note line 56; scope/LOG-M-003 markers present. None regressed to a hard decision. *(Minor 4-vs-5 label staleness — see m1.)* |
| Tier vocabulary clean | **PASS** | Rule file / both templates / appendix / hook-note: 0 stray uppercase MUST/NEVER/SHALL/REQUIRED/FORBIDDEN. Design doc's 6 occurrences are all legitimate references to existing HARD rules (H-23) or lint logic; hook-note lowercases its code-contract imperatives with an explicit HARD-tier disclaimer. |
| Path / internal-ref hygiene | **PASS** | No absolute `[home]/` paths; no employer/codename tokens; internal ids genericized (`[internal-kb]`, `[legacy-fu-id]`, `DJ-NNN`). |

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-i7 | Live-log range claim is empirically false ("FU.0–FU.9" / "live FU.5–FU.9 practice" / "8 of 13 live entries") — actual live `FEEDBACK-LOG.md` = FU.0–FU.4 (5 entries). Re-introduced after iter-4 verified it false. | **Critical** | design lines 58, 76, 245; appendix lines 4, 36; changelog line 340 vs line 338. `grep -cE '^## FU\.'` = 5. | Evidence Quality / Internal Consistency |
| SR-002-i7 | FU.8 teaching example gives one concept ("log-growth") two identities: `## FU.5 log-growth (alias: FU.0)` (line 34) vs `## FU.7 log-growth-capped-collection (alias: FU.0.1)` (line 68), contradicting the preamble's "log-growth item as FU.7" (line 4). | **Major** | appendix lines 4, 34, 68, 85 | Internal Consistency |
| SR-003-i7 | Design L2 token paragraph mixes current figure with stale iteration-2 arithmetic: states "~2,240 words / ~2,900–3,360 tokens" then "+~460 tokens over iteration-1" and "compressed ~1,197 → ~1,120 words" in the same paragraph (2,240 ≠ 1,120; +460 over 1,690 = ~2,150 ≠ 2,900–3,360). | **Major** | design line 210 | Internal Consistency |
| SR-004-i7 | Rule file measures ~2,990–3,970 tokens vs its own ~1,500 "target" (~2×); the doc keeps calling ~1,500 the "target" while the artifact measures double — an internal-consistency gap, and the "compress-to-offset" claim no longer holds. | **Major** | rule file `wc`; design lines 40, 210, 319 | Completeness / Actionability |
| SR-005-i7 | L0 revision note says "The **four** open questions now carry PROPOSED-DEFAULTs" (line 42) while Quick-Path (line 44) and the table say **five** (Q1–Q5). 4-vs-5 reader stumble. | Minor | design lines 42 vs 44, 283-289 | Internal Consistency |
| SR-006-i7 | FEEDBACK-LOG template nav-table label "FU.0 example (alias FU.0)" ≠ actual heading "FU.0 commit-push-cadence (alias: FU.0)" (anchor resolves; label cosmetic). | Minor | template lines 13 vs 40 | Traceability |

## Finding Details

### SR-001-i7: Empirically-false live-log range claim (Critical)
- **Severity:** Critical — **Affected dimension:** Evidence Quality (0.15) / Internal Consistency (0.20)
- **Evidence:** `grep -cE '^## FU\.' FEEDBACK-LOG.md` → **5** (FU.0 ratify-scheme-b, FU.1 subtraction-authorization, FU.2 feedback-decision-logs, FU.3 commit-push-cadence, FU.4 strip-internal-refs). No FU.5–FU.9 exist. Yet:
  - design L1.1 line 58 (FM-003): "matches **the live FU.5–FU.9 practice**"
  - design line 76 (FM-004): "the **live FU.5–FU.9 per-item split demonstrates this**"
  - design Adoption line 245: "entries and ids are preserved (**FU.0–FU.9**, DEC-LLM-001..003)"; "of the **8 of 13** live entries"
  - appendix line 4 + line 36 (shipping artifact): "the live bootstrap logs (**FU.0–FU.9**)"
  - The iter-4 changelog (line 338) states: "grep shows the live FEEDBACK-LOG carries only **FU.0–FU.4** … no FU.9" — so this was verified false, then re-asserted true in iter-6 (line 340: "matches the live FU.5–FU.9 practice").
- **Impact:** A claim presented as "verified/live" that `grep` falsifies is exactly the recurring class the tournament has failed on (empirically-falsified claim, cf. iter-3 CV-001). It is in the **shipping** FU.8 artifact and used to justify a design rule (multi-item split). Touches P-022 (no deception) / P-001 (accuracy). Also breaks the "8 of 13" arithmetic (actual: all 8 live entries = FU.0–FU.4 + DEC-LLM-001..003).
- **Recommendation:** Correct "FU.0–FU.9"→"FU.0–FU.4"; "8 of 13"→"all 8"; **remove** the false "live FU.5–FU.9 practice/split" evidence citations (do not substitute a new specific live citation — the multi-item split is a design *allowance*, not a demonstrated live practice). **Applied this pass.**

### SR-002-i7: Double-identity of the "log-growth" teaching example (Major)
- **Severity:** Major — **Affected dimension:** Internal Consistency (0.20)
- **Evidence:** appendix line 34 illustrates heading syntax with `## FU.5 log-growth (alias: FU.0)`; Example 2 at line 68 is `## FU.7 log-growth-capped-collection (alias: FU.0.1)`; the preamble (line 4) commits to "the log-growth item as **FU.7**". Same concept, two canonical ids (FU.5/FU.7) and two aliases (FU.0/FU.0.1). Iter-5 changelog claimed this "FU.7-for-FU.5 relabel" was closed, but line 34 was never updated.
- **Impact:** In a teaching artifact whose entire purpose (FU.8) is a *rationalizable, self-consistent* example, showing one item at two ids undermines the mechanism it teaches.
- **Recommendation:** Change line 34's slug from "log-growth" to a neutral `<slug>` so the syntax illustration no longer collides with Example 2's FU.7 item. **Applied this pass.**

### SR-003-i7: Stale iteration-2 arithmetic in the L2 token paragraph (Major)
- **Severity:** Major — **Affected dimension:** Internal Consistency (0.20)
- **Evidence:** design line 210 opens "Current measurement … ~2,240 words ≈ ~2,900–3,360 tokens" then, in the same paragraph, "the +~460 tokens over iteration-1 buy the iteration-2 … closures" and "iteration-2 prose was compressed (~1,197 → ~1,120 words) to offset." iteration-1 was ~1,690 tokens (line 335); +460 = ~2,150, not 2,900–3,360. 1,120 words ≠ current 2,240 words.
- **Impact:** The paragraph contradicts its own headline figure — the recurring point-of-claim staleness class, inside the very paragraph that argues the overage is honestly tracked.
- **Recommendation:** Delete the stale "+460 tokens / 1,197→1,120 words / compressed-to-offset" clauses; keep only the current measurement and the honest "grew because of propagation disclosures" rationale. **Applied this pass.**

### SR-004-i7: Rule file ~2× its ~1,500-token target (Major, disclosed [USER-DECISION])
- **Severity:** Major — **Affected dimension:** Completeness (0.20) / Actionability (0.15)
- **Evidence:** `wc feedback-decision-logs-standards.md` = 76 lines / 2,240 words / 15,888 chars → ~2,986 tokens (words×4/3), ~3,972 tokens (chars/4). Target "~1,500 tokens" reasserted at design lines 40, 210, 319. Trajectory: 1,584→1,690→2,150 tokens; words 1,120→1,425→2,240.
- **Impact:** The verification criterion (≤ ~1,500) is not met by ~2×. This is openly disclosed as a P-020 [USER-DECISION] (not deception), but two things need owner attention: (1) the doc still labels ~1,500 the "target" while measuring double — an internal-consistency smell; (2) the biggest single bloat sources are **duplicated** disclosure prose — the L5 "Scope limits (a)–(g)" block is near-verbatim in both the rule file (line 71) and design doc (line 229), and LOG-M-002 is a ~250-word single cell.
- **Recommendation (owner/P-020 call — NOT auto-applied):** Either (a) re-baseline: retire "~1,500 target," state the ratified budget as the measured figure so the doc stops asserting a target it doubles; or (b) genuinely trim by de-duplicating the L5 scope-limits block (point the rule file at the design doc / appendix rather than restating all 7 sub-items) and compressing LOG-M-002. Left for ratification per P-020 — this pass does **not** trim the rule file.

## Recommendations

1. **(Critical, applied)** Correct every "FU.0–FU.9" → "FU.0–FU.4", "8 of 13" → "all 8", and remove the false "live FU.5–FU.9 practice/split" citations (SR-001).
2. **(Major, applied)** Fix the FU.5/FU.7 double-identity in the appendix (SR-002).
3. **(Major, applied)** Delete stale iter-2 arithmetic from the L2 token paragraph (SR-003).
4. **(Major, owner/P-020 — flagged, not applied)** Resolve the ~1,500-target vs ~3,000-actual gap by re-baseline or genuine de-duplication trim (SR-004).
5. **(Minor, applied)** Harmonize "four open questions" → "five (Q1–Q5)" at L0 (SR-005); align the template nav label with the heading (SR-006).

## Edits Applied

Surgical, correctness-only edits (zero new machinery; all reduce overclaim / staleness). The P-020 token decision (SR-004) was **not** touched.

| # | File | Change |
|---|------|--------|
| E1 | design line 58 | "matches the live FU.5–FU.9 practice" → "a supported split" |
| E2 | design line 76 | removed "(the live FU.5–FU.9 per-item split demonstrates this)" |
| E3 | design line 245 | "FU.0–FU.9" → "FU.0–FU.4"; "8 of 13 live entries" → "all 8 live entries" |
| E4 | appendix line 4 | "FU.0–FU.9" → "FU.0–FU.4" |
| E5 | appendix line 36 | "FU.0–FU.9" → "FU.0–FU.4" |
| E6 | appendix line 34 | "## FU.5 log-growth (alias: FU.0)" → "## FU.5 <slug> (alias: FU.0)" |
| E7 | design line 210 | deleted stale "+460 tokens / ~1,197→~1,120 words compressed-to-offset" clauses |
| E8 | design line 42 | "The four open questions" → "The five ratification questions (Q1–Q5)" |
| E9 | template line 13 | nav label aligned to heading text |

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All required sections present; token overage disclosed (not missing). |
| Internal Consistency | 0.20 | Negative→improved | SR-001/002/003/005 all consistency defects; corrected this pass except SR-004's target-label gap (owner call). |
| Methodological Rigor | 0.20 | Neutral | Anti-bloat doctrine held; corrections are deletion/wording, no machinery. |
| Evidence Quality | 0.15 | Negative→improved | SR-001 was a falsified "live" citation; removed. Remaining claims re-grounded against `grep`. |
| Actionability | 0.15 | Neutral | Recommendations concrete; SR-004 trim targets named. |
| Traceability | 0.10 | Neutral | Findings linked to exact lines + repo evidence. |

## Decision

**Outcome:** Needs revision → **REVISE (targeted).** Not PASS: a live Critical (falsified shipping-artifact claim) plus the token criterion failing preclude "ready for external review." The Critical and two of three Majors were **cheap correctness fixes applied this pass** (they reduce overclaim, aligning with the de-overclaim doctrine — not an additive round). SR-004 (token budget) is a standing P-020 [USER-DECISION] left for the owner.

**Rationale:** The design's substance is sound (all 7 strategies across 6 rounds concur) and the residual defects are wording/factual, not structural. The single most important outcome of this pass: a false "verified/live" claim (FU.0–FU.9) that had regressed since iter-4 is now corrected, closing the specific empirically-falsified-claim instance that the tournament's recurring class predicts.

**Next action:** Present the corrected package + the SR-004 token-budget [USER-DECISION] (ratify-at-~3,000 vs trim-toward-1,500) to the user, per the design's own standing escalate-to-user fallback (design line 252). Do not run a further additive round.

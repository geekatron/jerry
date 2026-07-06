# S-010 Self-Refine — Findings (iteration 4)

> **Strategy:** S-010 Self-Refine · **Reviewer:** ps-architect (creator/owner) · **Date:** 2026-07-06
> **Deliverable package:** `design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/` (rule file, 2 templates, examples appendix, hook-design-note)
> **Criticality:** C3 (AE-003, ADR-bound convention) · **Iteration:** 4 of ongoing adversary cycle
> **Prior context:** three tournament iterations (0.64 / 0.65 / 0.59) already hammered the overclaim class; this pass re-verifies FU.5/FU.6/FU.8, rule-file budget, PROPOSED-DEFAULT markers, tier vocabulary, and public-repo hygiene.

## 1. Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | FEEDBACK-LOG + LLM-DECISION-LOG Jerry convention (design + 5 staged artifacts) |
| Criticality | C3 |
| Date | 2026-07-06 |
| Reviewer | ps-architect (creator/owner) |
| Iteration | 4 |

## 2. Summary

The package is mature and internally consistent on all requested verification axes. FU.5 rotation (cap, prev/next links, forward-nav fallback, segment index, cross-log nav-by-canonical-id) is coherent across design doc, rule file, and appendix walkthrough; cap values (~50 entries / ~800 lines, FU.49→FU.50) match everywhere. FU.6 id scheme is burden-free on the write path (operator never tracks a counter; aliases restart freely; `alias: —` fallback present) and collision-free for the logger under the disclosed single-writer profile. FU.8 examples are schema-consistent (correct field order, `source` sub-field present, terminal-disposition evidence present). PROPOSED-DEFAULTs on Q1–Q4 are all intact. Tier vocabulary is clean (zero HARD keywords in the rule file and both templates; hook-note MUSTs are the disclosed code-contract carve-out). Hygiene is clean (no `[home]/` absolute paths, no employer/internal-KB leaks, legacy ids genericized). **No Critical or Major findings.** Three Minor findings (one budget item that is a pending P-020 user decision, two trivial appendix clarity/edge-case items). Two of the three are fixed in this pass; the budget item is deferred to the user per P-020.

## 3. Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-20260706 | Rule file exceeds its own ~1,500-token soft target (measured ~2,150–2,300 tokens) | Minor | `wc -c`=9211 → chars/4≈2302; design states ~2,150 (tiktoken). Design L0/L2/Staged-Artifacts/changelog all disclose + flag as `[USER-DECISION]` SR-003 | Methodological Rigor |
| SR-002-20260706 | Hand-mint id instruction has an empty-ACTIVE edge case (just-rotated segment has no `## FU.N` heading yet) | Minor | `examples-appendix.md:172` "read the last `## FU.N` heading in the ACTIVE file and use `N+1`" — yields nothing immediately post-rotation | Completeness |
| SR-003-20260706 | Example-2 rationale for canonical `FU.7` assignment is convoluted (invokes FU.5/alias rather than "next free id after FU.6") | Minor | `examples-appendix.md:85` parenthetical | Actionability (clarity) |

## 4. Finding Details

### SR-001-20260706: Rule file over its ~1,500-token soft target (DISCLOSED; P-020 pending)
- **Severity:** Minor (disclosed, not hidden; escalated to user)
- **Affected Dimension:** Methodological Rigor
- **Evidence:** Measured `feedback-decision-logs-standards.md`: 9211 chars → chars/4 ≈ 2302 tokens; 1273 `wc -w` words → words×1.33 ≈ 1693. Design doc states ~2,150 (tiktoken cl100k). Reality ≈ 2,150–2,300 — i.e. ~43–53% over the ~1,500 soft target.
- **Impact:** The shipped MEDIUM rule file is heavier than the stated lean target. However, the overage is openly disclosed in L0 (line 40), L2 (line 202), the Staged Artifacts table (line 304), and the v5 changelog `[USER-DECISION]` SR-003, and is explicitly escalated as a P-020 ratify-at-~2,150 vs trim-toward-~1,500 choice. This is honest surfacing (P-022 satisfied), not a concealed violation.
- **Recommendation:** DO NOT resolve unilaterally (P-020). Present the user with: (a) ratify ~2,150 as the working budget (each +token buys an honesty disclosure that belongs in the shipped artifact), or (b) a trim pass that relocates disclosure prose from the rule file into the design doc / appendix, keeping the installed artifact nearer ~1,500. No machinery either way.

### SR-002-20260706: Hand-mint id fallback misses the empty-ACTIVE case
- **Severity:** Minor
- **Affected Dimension:** Completeness
- **Evidence:** `examples-appendix.md` Common-cases bullet (line 172): "read the last `## FU.N` / `## DEC-LLM-NNN` heading in the ACTIVE file and use `N+1`." Immediately after a rotation, the fresh ACTIVE segment carries only its seeded header + Segment Index — no entry heading — so "the last `## FU.N` heading" returns nothing and the operator has no id source at that instant.
- **Impact:** Narrow (hand-edit path AND just-rotated ACTIVE — a disclosed rare scenario), but the guidance is genuinely incomplete there. Fix is trivial and machinery-free.
- **Recommendation:** Add a one-clause fallback pointing to the Segment Index high-water mark. **FIXED in this pass.**

### SR-003-20260706: Example-2 canonical-id rationale is convoluted
- **Severity:** Minor (clarity)
- **Affected Dimension:** Actionability
- **Evidence:** `examples-appendix.md:85` parenthetical explains FU.7 via "Canonical `FU.5` is already the inline-doc `alias: FU.0`… so this later entry takes the next free id." The operative reason is simply "next free canonical id after FU.6"; the FU.5/alias detour risks confusing the reader it aims to help.
- **Impact:** Cosmetic; the ids themselves are correct and consistent.
- **Recommendation:** Reword to lead with "next free id after FU.6." **FIXED in this pass (light reword).**

## 5. Recommendations (prioritized)

1. **SR-001 (user decision):** Escalate the rule-file budget choice to the user at the ratification gate (already flagged). No unilateral edit.
2. **SR-002 (fixed):** Empty-ACTIVE hand-mint fallback added to the appendix Common-cases bullet.
3. **SR-003 (fixed):** Example-2 rationale reworded for clarity.

## 6. Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive (post-fix) | SR-002 gap closed; FU.5/6/8 coverage otherwise complete; residuals disclosed |
| Internal Consistency | 0.20 | Positive | Cap values, prev/next, forward-nav fallback, cross-log nav, schema field-order all consistent across 6 files; no surviving overclaim |
| Methodological Rigor | 0.20 | Neutral | SR-001 budget overage is real but disclosed + escalated per P-020/P-022; tier vocabulary clean |
| Evidence Quality | 0.15 | Positive | Overclaim terms (`byte-exact`, `collision-proof`) properly qualified; measurements taken and stated |
| Actionability | 0.15 | Positive (post-fix) | SR-003 clarity improved; examples runnable/copyable |
| Traceability | 0.10 | Positive | Findings linked to specific file:line; hygiene scans reproducible |

## 7. Decision

**Outcome:** Ready for external review (remaining Group B/C/D/scorer strategies) after this pass.

**Rationale:** Zero Critical/Major. All requested verification axes pass. Two trivial non-machinery fixes applied (SR-002, SR-003). The sole budget item (SR-001) is honestly disclosed and correctly held as a P-020 user decision — not a defect to resolve unilaterally.

**Next Action:** Proceed to the next adversary group; carry SR-001 to the ratification gate as an explicit user choice.

# Quality Score Report: GitHub Issue #351 (BUG-002 / REM-02 — USER-HOLD runtime model)

## L0 Executive Summary
**Score:** 0.65/1.00 | **Verdict:** REJECTED | **Weakest Dimension:** Completeness (0.52)
**One-line assessment:** Core technical claims are accurate, but the issue silently covers only ~2 of BUG-002's 5-6 acceptance-criteria items and one citation path lacks a branch qualifier that the sibling path has — a reader who does exactly what's asked will not close the bug and may 404 on the tracking link.

## Scoring Context
- **Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-351.md`
- **Type:** GitHub issue text (external handoff artifact) | **Criticality:** C4 (tournament)
- **Ground truth used:** remediation-register.md REM-02, BUG-002 entity (acceptance criteria), remediation-log.md, pr269-verdict.md, evidence-c07033ce.md
- **Strategies incorporated:** 8 (S-001, S-002, S-004, S-007, S-010, S-011, S-012, S-003/steelman-as-"SM"), 33 findings
- **Scored:** 2026-08-07

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|---|---|---|---|---|
| Completeness | 0.20 | 0.52 | 0.104 | Design question covers 2 of BUG-002's ~5-6 AC sub-items; 3 (timeout policy, SR-02 STOP decision, token/context model) silently omitted |
| Internal Consistency | 0.20 | 0.77 | 0.154 | "Every interactive gate...inherits this ambiguity" overreaches vs. the narrower scope used one sentence later and vs. REM-01 (separate root cause) |
| Methodological Rigor | 0.20 | 0.76 | 0.152 | Core claims (tool gap, unpinned model, non-termination, disposition) verified true; the "every gate" overgeneralization is the one clear inaccuracy vs. register |
| Evidence Quality | 0.15 | 0.62 | 0.093 | Both citations are bare non-clickable paths; "contradicts other documented guarantees" and "candidate designs" are unanchored/overstated |
| Actionability | 0.15 | 0.58 | 0.087 | Answering exactly what's asked will not satisfy BUG-002's own AC (see Completeness) — the stated next step under-delivers closure |
| Traceability | 0.10 | 0.55 | 0.055 | Worktracker path has no branch qualifier while the adjacent register path does, in the same sentence pair |
| **TOTAL** | **1.00** | | **0.645 -> 0.65** | |

## Per-Dimension Evidence

**Completeness (0.52):** BUG-002's own Acceptance Criteria (verified directly, not just the register) require: (1) pin runtime model + make USER-HOLD real [COVERED], (2) rewrite NS-H-01 terminating scope [COVERED], (3) re-align bb-001, (4) USER-HOLD timeout/unattended policy [NOT mentioned], (5) whether SR-02 escalates to STOP at C3+ [NOT mentioned], (6) a token/context-budget model justifying step limits/checkpoints [NOT mentioned]. A reader who fully answers the issue's stated question still leaves the bug open. No text flags the question set as partial. (Corroborates S-001-04, S-007-02.)

**Internal Consistency (0.77):** "Every interactive gate in the skill inherits this ambiguity" is broader than what the register supports: IV-HOLD is cited in REM-01 as already having a *correct* resolution, and QG-HOLD's defect (#350) has a distinct root cause (P-003/H-36 delegation topology, not a missing tool grant) tracked as a separate cluster. The claim also sits awkwardly against the next sentence's narrower "USER-HOLD and the briefing agent's six interactive gates" scope. Everything else (title/tracking IDs, severity, disposition, blocks-merge fact) is internally coherent. (Corroborates S-002-01; judged Major, not the "conflation risk" some strategies imply is worse.)

**Methodological Rigor (0.76) — factual accuracy vs. ground truth:** AskUserQuestion tool-gap, unpinned runtime model, non-terminating self-check, and "not maintainer-fixable" disposition all check out against REM-02/BUG-002 verbatim. The "every interactive gate" overgeneralization (above) is the one clear, ground-truth-contradicted claim. The "before every file write" phrasing matches BUG-002's own working shorthand ("STAR-before-every-Write") verbatim, so it is not scored as inaccurate against my designated ground truth, though S-010-01/S-004-04's citation of a more primitive source (Write/Edit/Bash) is worth a cheap defensive fix.

**Evidence Quality (0.62):** Neither cited path is a resolvable URL despite the source BUG-002 entity file itself demonstrating the better pattern (full GitHub URL for the issue link). "which contradicts other documented guarantees" names no guarantee (register specifies: T1/T2 tool-tier enforcement, verifier isolation rationale). "Full analysis with candidate designs" mildly overstates REM-02's redesign section (two conditional branches, not an enumerated menu). (Corroborates S-002-02/S-004-02/S-011-02/S-002-03.)

**Actionability (0.58):** The stated design question is concrete enough to start work, but per Completeness, fully answering it does not close BUG-002 — a contributor following only this text ships an incomplete fix and reopens the loop. Zero forward guidance on solution shapes is given even though the register has a ready-made candidate split (worker-subagent -> return-to-orchestrator; persona -> re-justify tool-tier/verifier isolation). (Corroborates SM-002, S-001-04.)

**Traceability (0.55):** The Worktracker path has no branch qualifier; the adjacent register path in the same Tracking block does ("on branch `feat/proj-032-nuclear-sop-review`"). This branch is a separate maintainer review branch, not PR #269's own branch — a reader checking the unqualified path on the PR's own branch or `main` gets a dead end. Independently corroborated by 3 strategies (SM-001, S-004-01, S-001-01); 2 rated it Critical. **My judgment: valid but Major, not Critical** — the core ask (title + design question) is self-contained and does not depend on resolving this citation, so it does not "block acceptance" of the deliverable's primary content; it degrades traceability of the supporting evidence only. `critical_block = false` on this basis.

## Required Edits (minimal set to reach PASS)
1. Tracking block: state the branch once, covering both paths ("Both paths below are on branch `feat/proj-032-nuclear-sop-review` — a separate maintainer review branch, not this PR's branch") before listing the Worktracker and register paths; append the entity filename to the Worktracker path.
2. Design question: append the omitted AC scope — timeout/unattended policy for a stalled USER-HOLD, whether SR-02 escalates to STOP at C3+/C4, and the token/context-budget model justifying step limits and checkpointing.
3. Replace "Every interactive gate in the skill inherits this ambiguity" with a scoped version naming USER-HOLD + sop-brief's six STOP gates, and cross-reference issue #350 for the separately-tracked QG-HOLD defect.
4. Name the contradicted guarantees inline: "...undercut the per-agent tool-tier enforcement and the independent verifier's isolation rationale."
5. Widen "before every file write" to "before every Write, Edit, or command-execution step."
6. Append to the Tracking line: "alongside six sibling design-decision issues (#350, #352-356), all currently required before the standard merge recommendation."
7. Fix "Assignees: victorlau1 malcolm-x-evo " -> "Assignees: victorlau1, malcolm-x-evo" (no trailing space).
8. Name the four agents once ("sop-brief, sop-executor, sop-verifier, sop-capture") and gloss AskUserQuestion briefly.

## Leniency Bias Check
- [x] Each dimension scored independently; Completeness verified against BUG-002's actual AC checklist, not impression
- [x] Evidence cited per dimension (register quotes, AC text, cross-strategy corroboration counts)
- [x] Uncertain scores resolved downward (Completeness 0.52 not 0.60; self-check-scope claim downweighted only after finding it matches BUG-002's own phrasing, not on impression)
- [x] Two strategy "Critical" labels reviewed and explicitly downgraded to Major with stated rationale (not silently accepted or dismissed)
- [x] No dimension scored above 0.95; none scored above 0.90
- [x] Composite (0.645 -> 0.65) verified by direct sum of weighted column

**Verdict rationale:** 0.65 < 0.85 REJECTED threshold. No dimension <= 0.50 (Completeness 0.52 is the floor), so no rubric-defined Critical dimension triggers; `critical_block = false`. REJECTED is driven by composite, not by a single blocking finding.

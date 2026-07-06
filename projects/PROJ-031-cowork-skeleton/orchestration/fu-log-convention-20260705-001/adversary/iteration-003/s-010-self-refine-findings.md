# S-010 Self-Refine — Findings (iteration 3, Group A)

> **Strategy:** S-010 Self-Refine (creator/owner self-review)
> **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/` package (rule file, 2 templates, examples-appendix, hook-design-note)
> **Criticality:** C3 (AE-002/AE-003 install gate) · **Iteration:** 3 of the self-refine track
> **Reviewer:** ps-architect (convergent, opus) · **Date:** 2026-07-06
> **Objectivity check:** Low-medium attachment (reviewing a package authored across prior iterations; distance is high because two tournament rounds already reshaped it). Proceeding; leniency counteraction applied (forced >=3 findings, verified each against source).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Verdict and headline |
| [Verification Matrix](#verification-matrix) | The 7 required checks, pass/fail with evidence |
| [Findings Table](#findings-table) | All findings, severity, evidence |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Revisions Applied](#revisions-applied) | Edits made this pass (no new machinery) |
| [Scoring Impact](#scoring-impact) | Dimension-level assessment |
| [Decision](#decision) | Next action |

---

## Summary

The package is in strong shape after two tournament rounds. Hygiene is clean (no absolute paths, no employer/internal literals — all genericized placeholders), tier vocabulary is clean in the convention files, all four PROPOSED-DEFAULT markers are intact, and the FU.5 rotation design is internally consistent (cap, linked-list, index, cross-log nav all reconcile across the design doc, rule file, and appendix walkthrough). Two genuine internal-consistency defects were found and **fixed this pass** (both wording-only, no new machinery): a canonical-id double-alias in the FU.8 examples, and a parity-check command that silently no-ops on the decision log. One disclosed-and-ratified item — the rule file measures **2,100 tokens (cl100k) vs the ~1,500 stated target (40% over)** — is a genuine choice the user should ratify or trim.

---

## Verification Matrix

| # | Required check | Verdict | Evidence |
|---|----------------|---------|----------|
| V1 | FU.5 rotation internally consistent (cap, links, index, cross-log nav) | **PASS** | Design L1.4, rule "Segment rotation", appendix walkthrough all agree: ~50-entry/~800-line cap (whichever first); seal-after-crossing; lone oversized entry seals immediately; stable ACTIVE name; `.NNN.md` sealed segments; `Segment N · prev · next` linked-list with forward-nav fallback to ACTIVE; single Segment Index in ACTIVE; cross-log nav by canonical id only (no paths). Appendix walkthrough (lines 122-144) matches the rule exactly. Sealed segment `next: .002.md` resolving to ACTIVE via the fallback rule is deliberate and documented (design L1.4 linked-list row), not a defect. |
| V2 | FU.6 id scheme burden-free for operator + collision-free for logger | **PASS (with honest scoping)** | Operator never tracks a counter; aliases restart/repeat freely; `alias: —` when unlabelled (symmetric across both logs). Canonical `FU.N`/`DEC-LLM-NNN` logger-assigned, monotonic-per-log-across-segments, never resets. "Collision-free" is honestly scoped to the validated single-writer profile (orchestrator-only-append; workers return candidates via P-003 handoff); multi-writer residual disclosed as "collision-resistant, not collision-proof" with the lint's real limit (catches dup/gap, not last-write-wins) stated. Consistent across design L1.1, LOG-M-005, appendix. |
| V3 | FU.8 examples present, correct, consistent with schema | **FAIL → FIXED (SR-001)** | Both templates embed one worked example matching field order; appendix has ids/aliases, 2 FEEDBACK exemplars, 1 DECISION exemplar, rotation walkthrough, evidence formats, common cases. **Defect:** canonical `FU.5` carried two aliases (`FU.0` at lines 31/34/167 vs `FU.0.1` at 66/83) — a unique-id-to-two-aliases contradiction of the FU.6 invariant, and a conflict with the H-31 candidate list. Fixed by renumbering Example 2 to canonical `FU.7`. |
| V4 | Rule file <= ~1,500 tokens (measure, state) | **FAIL (disclosed/ratified)** | Measured **2,100 tokens** (`tiktoken cl100k`, `uv run`), matching the design's own "~2,150" claim (accurate within ~2%). This is **40% over** the "~1,500" soft target. Disclosed and re-ratified twice (design L0 line 40, L2 line 200). Not a P-022 deception (both numbers shown side-by-side), but the "target" language is now aspirational-but-unmet — see SR-003. |
| V5 | PROPOSED-DEFAULT markers intact on the 4 open questions | **PASS** | Q1-Q4 each carry a PROPOSED-DEFAULT in the design's Proposed Defaults table; echoed in LLM-DECISION-LOG template (assistant-verbatim policy), rule file (LOG-M-003, verbatim-policy note, scope-framework), and hook note (Q3). None downgraded to a decision. |
| V6 | Tier vocabulary clean | **PASS** | Zero `MUST/SHALL/NEVER/FORBIDDEN/REQUIRED` in rule file, both templates, appendix. LOG-M-001..006 are SHOULD-tier. Hook note's MUST/MUST NOT carry an explicit exemption note (line 4: "code-implementation contracts... not Jerry HARD-rule-tier governance... do not count against the 25/25 ceiling"). |
| V7 | No internal-refs / absolute-path hygiene violations | **PASS** | No `[home]/` paths in any deliverable. No `[employer]`/employer literals in staging. Residual internal ids genericized to `[internal-kb]`/`[legacy-fu-id]`/`[legacy-oi-id]` placeholders (13/6/4 occurrences, all bracketed). Appendix declares "no employer references, no absolute paths" and uses `<hash>`/`{session_id}`/`<domain-slug>` placeholders throughout. |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-20260706 | Canonical `FU.5` bound to two different aliases in examples-appendix | Major | Lines 31/34/167 map `FU.5 → alias FU.0`; lines 66/83 map `FU.5 → alias FU.0.1`. Contradicts FU.6 unique-canonical-id invariant and the H-31 candidate list (line 167) operators copy. | Internal Consistency |
| SR-002-20260706 | "Required" post-rotation parity check silently no-ops on the decision log | Minor | Rule line 50 and design line 187 give only `grep -c '^## FU\.'`; the DECISION-LOG (`## DEC-LLM-NNN`) "rotates identically" (appendix 144) but that grep returns 0 on it, so `0+0=0` falsely passes / verifies nothing. | Methodological Rigor |
| SR-003-20260706 | Rule file 40% over its own stated "~1,500 token" target | Major (disclosed) | Measured 2,100 tokens vs "~1,500 target" repeated at design L0 line 40 and L2 line 200. Disclosed + re-ratified; the residual issue is that "target" language survives unmet. | Internal Consistency / Actionability |

No Critical findings. SR-001 and SR-002 fixed this pass; SR-003 requires a user ratify-or-trim decision (P-020).

---

## Finding Details

### SR-001-20260706: Canonical FU.5 double-alias (Major → FIXED)

- **Severity:** Major
- **Affected Dimension:** Internal Consistency (weight 0.20 — the weakest dimension in prior tournaments, 0.46)
- **Evidence:** In `examples-appendix.md`, the "Ids & aliases" block binds `FU.5 (alias: FU.0)` (line 31), the heading-suffix illustration repeats `## FU.5 log-growth (alias: FU.0)` (line 34), and the H-31 common-case candidate list enumerates `FU.5 (alias FU.0)` (line 167). But Example 2 (lines 66, 83) binds the same canonical id to a different alias: `## FU.5 log-growth-capped-collection (alias: FU.0.1)` with the note "the logger assigned canonical `FU.5`."
- **Impact:** A single canonical id mapping to two aliases directly violates the FU.6 invariant the FU.8 examples exist to teach (unique, monotonic canonical id per log). Worse, the H-31 back-reference walkthrough — which operators will copy as the model for disambiguation — lists `FU.5 (alias FU.0)`, contradicting Example 2's `FU.5 (alias FU.0.1)`. This is the same defect class iteration-2 fixed for the FU.0/FU.3 example (SM-001), recurring in an un-swept location.
- **Recommendation (applied):** Renumber Example 2's canonical id `FU.5 → FU.7` (unused, monotonically plausible mid-log), preserving alias `FU.0.1`. This keeps the "alias restarts sub-numbered" teaching while removing the canonical-id collision with the ids/aliases block and the H-31 candidate list.

### SR-002-20260706: Parity-check command DEC-log gap (Minor → FIXED)

- **Severity:** Minor
- **Affected Dimension:** Methodological Rigor (weight 0.20)
- **Evidence:** Rule file line 50 and design doc line 187 specify the required post-rotation parity check as `grep -c '^## FU\.'` on sealed + active. The LLM-DECISION-LOG uses `## DEC-LLM-NNN` headings and "rotates identically" (appendix line 144), but `grep -c '^## FU\.'` on a decision log returns 0 for both sealed and active files, so the check computes `0 + 0 = 0` and passes vacuously — verifying nothing on exactly the log where the same drop/duplicate risk exists.
- **Impact:** A safety step labelled "required, not optional" is a silent no-op on half the logs it governs. Low likelihood of harm (an operator rotating the DEC log would likely grep the heading they see), but a "required" check that verifies nothing undercuts the rigor claim.
- **Recommendation (applied):** Generalize the parity-check wording to name the DEC-LLM heading variant in both the rule file and the design doc.

### SR-003-20260706: Rule file 40% over the ~1,500-token target (Major, disclosed — user decision)

- **Severity:** Major (but honestly disclosed — not a P-022 issue)
- **Affected Dimension:** Internal Consistency / Actionability
- **Evidence:** Measured 2,100 tokens (`tiktoken cl100k`). The design repeatedly frames "~1,500 tokens" as the target (L0 line 40: "targets ~1,500 tokens (it measures ~2,150...)"; L2 line 200 re-ratifies 2,150 as the working budget). The changelog progression 1,584 → 1,690 → 2,150 is internally consistent and honestly recorded.
- **Impact:** The anti-bloat doctrine is the package's central thesis and the stated basis for rebutting 9 UX findings. Shipping a rule file 40% over its own repeatedly-stated target is in visible tension with that thesis. It is *disclosed*, so it is not deception — but leaving "~1,500 target" language beside a 2,150 artifact reads as an unmet goal rather than a deliberate budget.
- **Recommendation (NOT applied — P-020 user call):** Either (a) re-baseline the stated target to ~2,150 and drop the "~1,500 target" framing so the budget is owned, not aspired to; or (b) trim toward 1,500 by moving the longer LOG-M-005 prose and lint scope-limit disclosures into the appendix (the design's own "point at the appendix" pattern). This is a genuine trade for the user, not a defect I should silently resolve.

---

## Revisions Applied

Both edits are wording-only, add zero machinery (zero new lint, file, subsystem — consistent with the anti-bloat doctrine):

1. **SR-001** — `examples-appendix.md`: Example 2 canonical id `FU.5 → FU.7` (heading + the "logger assigned canonical" note), removing the double-alias contradiction with the ids/aliases block and the H-31 candidate list.
2. **SR-002** — `feedback-decision-logs-standards.md` (rule) and `feedback-decision-log-convention-design.md` (design L1.4 step 3): parity-check wording generalized to name the `'^## DEC-LLM-'` variant for the decision log.

SR-003 left for user ratification (P-020) — documented, not silently changed.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All 7 required checks executed; FU.5/6/8 examples present; PROPOSED-DEFAULTs intact. |
| Internal Consistency | 0.20 | Negative → Positive (post-fix) | SR-001 double-alias fixed; SR-003 target/actual tension remains (disclosed, user-owned). |
| Methodological Rigor | 0.20 | Negative → Positive (post-fix) | SR-002 parity-check no-op fixed; rotation critical-section + required parity check otherwise sound. |
| Evidence Quality | 0.15 | Positive | Token count measured with tiktoken; every finding cites line numbers; hygiene verified by grep. |
| Actionability | 0.15 | Positive | SR-001/SR-002 fixed with concrete edits; SR-003 gives the user two costed options. |
| Traceability | 0.10 | Positive | Findings linked to source lines; SR-003 traces to prior-iteration ratification. |

---

## Decision

**Outcome:** Ready for external review after this pass. Two consistency defects fixed in-line; one disclosed/ratified budget item (SR-003) escalated to the user as a ratify-or-trim decision rather than silently resolved.

**Rationale:** No Critical findings. The package's load-bearing designs (FU.5 rotation, FU.6 id scheme) verify clean and are honestly scoped. The FU.8 examples now hold the canonical-id invariant they teach. Hygiene, tier vocabulary, and PROPOSED-DEFAULT markers all pass.

**Next Action:** Route to remaining Group A/B strategies. Surface SR-003 (token budget) to the user for P-020 ratification at the sign-off gate.

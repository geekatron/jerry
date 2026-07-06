# Inversion Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (iteration 4)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-013), blind-parallel tournament round, iteration 4
**H-16 Compliance:** Not directly verifiable in this blind-parallel execution (per the operator's 6-group blind-agent protocol, S-003 runs as its own blind strategy in the same round rather than as a prior-output dependency visible to this agent). This does not block S-013 execution — S-013's own prerequisite is "S-003 before the overall C3+ sequence," which is an orchestrator-level ordering concern, not a per-strategy blocking gate.
**Goals Analyzed:** 8 (see Step 1) | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 4 (2 Critical, 2 Major)

## Task-Specific Framing (per invocation)

This round's specific charge: *"What would guarantee feedback/decisions get LOST despite this convention? Does the package do any of it? Does it beat the null alternative (memory files + transcripts only)?"* The findings below are organized around that charge, using the S-013 six-step protocol.

---

## Summary

The package is architecturally sound for a MEDIUM-tier, anti-bloat convention — segment rotation, logger-assigned ids, and the graduation boundary to worktracker DECISION are well-reasoned and none of them, on inspection, is a mechanism that *actively* guarantees loss. However, inversion surfaces **two Critical overclaims** about the specific question this round was asked to answer ("does it beat the null alternative / MEMORY.md"): (1) the design doc's own Null-alternative section claims both of its disclosed weaknesses vs. `MEMORY.md` are "addressed... in this draft," when one fix is an unexecuted, gated future install step and the other is merely a *disclosure*, not a fix — a direct self-contradiction against the same document's own Adoption-plan and Install-stall-risk text; and (2) the shipped rule file's own header claims persistence follows from mere "capture," silently dropping the "AND committed" qualifier the design doc itself added as a fix in a prior iteration (IN-001, changelog v5) — meaning the fix did not propagate to the one artifact that will actually govern behavior after install. Two further Major gaps concern scenarios the convention does not yet cover: background/subagent-surfaced feedback candidates have no hook seam and depend entirely on in-turn orchestrator memory (the exact failure mode the whole convention exists to eliminate, and precisely the "leverage background agents" scenario the user's original FU.2 requirement named); and the rotation procedure's "required" parity check has no defined failure/recovery branch. **Recommendation: REVISE.** All four issues are closable by wording/scoping edits — no new machinery is required, consistent with the package's own anti-bloat doctrine — but the two Critical findings are exactly the "overclaimed coverage" class this review was directed to treat as blocking.

**Does it beat the null alternative?** Partially, and honestly less than claimed. **Wins:** structured disposition/evidence tracking, a real graduation boundary to worktracker DECISION/ADR (MEMORY.md has none), and load-bearing segment rotation so the log never blows the Read window (transcripts already do, per the project's own PM-001 citation). **Does not (yet) beat it on:** session-start rediscoverability (MEMORY.md is force-injected into context today; the log requires a `project-workflow.md` edit that is explicitly deferred to a gated install step that has not happened) and uncommitted-loss durability (MEMORY.md lives outside the git working tree and is structurally immune to `git checkout`/`reset`/`clean`; the logs are ordinary tracked files and always will be — this is a permanent trade-off the anti-bloat doctrine correctly declines to "fix" with new machinery, but the document should say "accepted trade-off," not "addressed").

---

## Findings Summary

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-iter4-20260706 | "Both [null-alternative] axes are addressed by the fixes already in this draft" | Assumption / Overclaim | Low | Critical | `design/feedback-decision-log-convention-design.md:261` vs. `:234` and `:240` | Internal Consistency |
| IN-002-iter4-20260706 | Persistence claim scoped to "once captured" (commit qualifier dropped in the shipped rule file) | Assumption / Overclaim | Low | Critical | `design/staging-feedback-logs/feedback-decision-logs-standards.md:3` vs. `design/feedback-decision-log-convention-design.md:30` | Internal Consistency / Evidence Quality |
| IN-003-iter4-20260706 | "The orchestrator will remember to append a worker-returned candidate this turn, with no reminder needed" | Assumption | Low | Major | `design/feedback-decision-log-convention-design.md:74` (candidate handoff) vs. `design/staging-feedback-logs/hook-design-note.md` Seam 2 (Stop/PreCompact only, no SubagentStop) | Completeness |
| IN-004-iter4-20260706 | "The required rotation parity check will pass, or the failure path is self-evident" | Anti-Goal (undefined failure branch) | Medium | Major | `design/feedback-decision-log-convention-design.md:185-190`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:50` | Methodological Rigor |
| IN-005-iter4-20260706 | "AE-006e is the interim compaction backstop" for these specific files | Assumption | Low | Minor | `design/feedback-decision-log-convention-design.md:221` | Evidence Quality |
| IN-006-iter4-20260706 | "This convention is enforced by L1 + these ≤3 L5 lint checks" (present tense, before the not-yet-wired caveat) | Internal Consistency (wording) | Medium | Minor | `design/feedback-decision-log-convention-design.md:221` | Internal Consistency |

**Finding ID Format:** `IN-{NNN}-iter4-20260706`.

---

## Finding Details

### IN-001: Null-alternative comparison overclaims that both disclosed weaknesses are "addressed" [CRITICAL]

**Type:** Assumption / Overclaim
**Original Assumption (as stated in the deliverable):** "Both axes are addressed by the fixes already in this draft — the IN-002 install-step session-start wiring (Adoption step 3) and the IN-001 commit-durability disclosure (L0 scope note (ii)) — with no new machinery." (`design/feedback-decision-log-convention-design.md:261`)
**Inversion:** What if these axes are *not* addressed? Check the same document's own Adoption plan: "**Install** (framework paths — separate authorized step, **not this task**): ... **add `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` to `project-workflow.md`'s session-start 'Before' orientation row** ... this closes the read-side gap" (`:234`, emphasis added). That is, the very fix cited as "already in this draft" is explicitly scoped as a *future, separately-authorized, gated* action — it requires (1) user ratification of Q1-Q4 (Adoption step 1), (2) an adversary gate (step 2), and only then (3) install. The same document also states, of the whole convention, "**Ratification/install can stall** — this project's own precedent (the sibling ADR-convention needed a multi-iteration subtraction pass) makes indefinite delay a real, evidenced outcome" (`:240`). So the claim "addressed... already in this draft" is falsified by the document's own later text: the fix has not executed, is gated behind multiple approvals, and the document itself flags a nonzero, evidenced probability it never lands.
For the second axis (durability), the cited "fix" is explicitly labelled a **disclosure**, not a mechanism change: "IN-001 commit-durability disclosure (L0 scope note (ii))" points to text that only *acknowledges* the exposure ("An uncommitted append carries the same exposure as any other uncommitted change in the repo... the standing commit-cadence directive... is the current sole mitigation," `:30`) — and that "sole mitigation" (FU.3's commit-cadence directive) *pre-dates* this package entirely; it is not something this design adds. Disclosing a permanent, structural weakness is not the same as addressing it, and `MEMORY.md`'s durability advantage (living outside the git working tree) cannot be replicated by these logs without adding exactly the kind of external-storage machinery the package's own anti-bloat doctrine declines elsewhere.
**Plausibility:** Certain — this is not a hypothetical inversion, it is a direct textual comparison within the same file. **Confidence:** High (H, on the finding; the underlying assumption itself is Low confidence).
**Consequence:** A P-020 ratification reader who trusts the Null-alternative note's "addressed" framing will approve the design believing it already matches or beats `MEMORY.md` on both axes. It does not. If ratification proceeds on that belief and install subsequently stalls (as the document's own precedent shows is plausible), the rediscoverability gap persists silently and indefinitely, with no flag anywhere prompting a re-check — the opposite of the "don't lose feedback" goal this whole package exists to serve.
**Evidence:** `design/feedback-decision-log-convention-design.md:261` (the claim), `:234` (the fix is "not this task," gated behind ratification + adversary + install), `:240` (install-stall is explicitly a real, evidenced risk in this same project).
**Dimension:** Internal Consistency (0.20).
**Mitigation:** Rewrite the Null-alternative note to distinguish "disclosed" from "addressed" precisely: (a) state plainly that the durability axis is an **accepted, permanent trade-off** (not fixable without new machinery, and the anti-bloat doctrine correctly declines to fix it) rather than "addressed"; (b) state that the rediscoverability axis has a **planned** fix that takes effect only once Adoption step 3 actually lands, cross-referencing the Install-stall re-assessment risk so a ratifying reader sees the contingency, not a completed state.
**Acceptance Criteria:** The sentence "Both axes are addressed by the fixes already in this draft" no longer appears in that form; the replacement text distinguishes disclosed-but-unfixed (durability) from planned-but-not-yet-installed (rediscoverability), and cross-references the Adoption plan / Install-stall section rather than contradicting them.

---

### IN-002: Shipped rule-file header drops the "AND committed" qualifier already fixed in the design doc [CRITICAL]

**Type:** Assumption / Overclaim (regression of a prior fix)
**Original Assumption:** The rule file that will actually be installed to `.context/rules/` (the operative SSOT after install — the design doc is a one-time historical record nobody re-reads routinely) accurately states the persistence guarantee.
**Inversion:** Compare the rule file's own opening sentence against the design doc's own corrected wording. Rule file: *"Two append-only, segment-rotating ledgers so that, **once captured**, user feedback and human/LLM decisions survive compaction, sessions, and model swaps."* (`design/staging-feedback-logs/feedback-decision-logs-standards.md:3`). Design doc L0 (after the iteration-3 remediation explicitly logged in the changelog as fix **IN-001**: *"added the 'once appended AND committed' durability scope to L0"*): *"'Survive' means once appended **AND committed**. An uncommitted append carries the same exposure as any other uncommitted change in the repo..."* (`design/feedback-decision-log-convention-design.md:30`). The rule file's "once captured" phrasing was never updated to carry the same qualifier — a targeted grep across the whole package (`design/` tree) confirms the "AND committed" / "once appended AND committed" language exists **only** in the design doc, nowhere in the artifact that ships.
**Plausibility:** Certain (direct textual comparison; not inferred).
**Consequence:** Precisely the failure class this convention exists to prevent, recurring in the convention's own SSOT: a reader (human or a future LLM session parsing `.context/rules/feedback-decision-logs-standards.md` at session start, per H-22/L1 loading) who never reads the design doc will reasonably conclude that *appending* an entry is sufficient for it to "survive... session boundaries" — exactly the false belief that leads someone to skip a commit before a crash or a `git checkout`/`reset`, at which point the entry is gone with no backstop (as the design doc itself discloses, but the rule file does not). This is also self-referential evidence of a process gap: the package's own changelog (v5, iteration-3) explicitly logged this exact overclaim class as "the recurrence of the overclaim class in un-swept locations" for other artifacts (v4/iteration-2), yet the fix, once made in the design doc, was itself never swept into the rule file.
**Evidence:** `design/staging-feedback-logs/feedback-decision-logs-standards.md:3` (omits the qualifier) vs. `design/feedback-decision-log-convention-design.md:30` (carries it) and the v5 changelog entry citing "IN-001... added the 'once appended AND committed' durability scope to L0" (`design/feedback-decision-log-convention-design.md:320`, Revision Changelog row v5).
**Dimension:** Internal Consistency (0.20) / Evidence Quality (0.15).
**Mitigation:** Add the identical "once captured **and committed**" qualifier (or an equally explicit cross-reference) to the rule-file header, so the artifact that actually governs post-install behavior does not omit the one caveat most load-bearing for the "don't lose feedback" promise.
**Acceptance Criteria:** `feedback-decision-logs-standards.md` line 3 (or its replacement) states or directly cross-references the "captured AND committed" durability scope; a grep for "once captured" without a co-located commit qualifier returns zero hits across the shipped package.

---

### IN-003: Background/subagent-surfaced candidates have no hook seam and depend entirely on in-turn orchestrator memory [MAJOR]

**Type:** Assumption
**Original Assumption:** "workers return feedback/decision *candidates* via the existing P-003 orchestrator-worker handoff, and the orchestrator serializes the append" (`design/feedback-decision-log-convention-design.md:74`) reliably closes the loop for background-agent-surfaced feedback.
**Inversion:** What if the orchestrator receives the candidate in a handoff but does not append it that same turn? Nothing in the design catches this. The hook design (`design/staging-feedback-logs/hook-design-note.md`) names exactly three seams — `UserPromptSubmit` (provenance stamp), `Stop`/`PreCompact` (capture reminder keyed to the *user's own turn* keywords/interrogatives), and an optional segment-cap reminder — none of which fires on `SubagentStop`, the lifecycle event where a worker's handoff actually lands. The single-writer/orchestrator-only-append discipline (LOG-M-005) solves the *race-condition* problem (two writers clobbering each other) but does not solve the *forgetting* problem (the orchestrator simply never gets around to the append) for exactly the multi-agent, background-agent pathway the user's own FU.2 requirement singled out: *"leverage background agents so that we don't burn through the main context window"* (`FEEDBACK-LOG.md:63`). This is the one capture path with strictly less automated backstop than the ordinary chat-turn path (which at least gets a designed, if unshipped, `Stop`-hook reminder).
**Plausibility:** Realistic — background-agent usage is explicitly a named goal of this whole package, not an edge case.
**Consequence:** A feedback/decision candidate surfaced by a worker agent and not immediately appended by the orchestrator is lost with no trace (it never touched any log, `MEMORY.md`, or a hook-stamped sidecar) — the same silent-loss failure mode `MEMORY.md`+transcripts alone would also exhibit, meaning on this specific path the convention does **not** currently beat the null alternative.
**Dimension:** Completeness (0.20).
**Mitigation:** Either (a) extend the hook design to name `SubagentStop` as a fourth seam (a reminder only, matching the existing fail-open shape), or (b) if a fourth seam is judged out of scope for v1, add an explicit MEDIUM-rule clause stating the append MUST happen in the same turn the handoff is processed (not deferred), making the obligation textually explicit rather than only implied by design-doc prose.
**Acceptance Criteria:** Either `hook-design-note.md` names the `SubagentStop` candidate-capture case, or `feedback-decision-logs-standards.md` (LOG-M-005) states the same-turn append obligation for handoff-carried candidates explicitly.

---

### IN-004: Rotation's "required" parity check has no defined failure/recovery branch [MAJOR]

**Type:** Anti-Goal (undefined failure path in an otherwise well-specified procedure)
**Original Assumption:** The four-step rotation procedure — copy to sealed segment, reset ACTIVE, run the required parity check, "only after the parity check passes, resume normal appends" (`design/feedback-decision-log-convention-design.md:187-190`) — is complete because it names the check as required.
**Inversion:** What if the check *fails* (a genuine mismatch between pre-seal count and sealed+active count)? The procedure states what must happen before resuming appends (nothing, until it passes) but never states what to *do* about a failure: no halt-and-escalate instruction, no guidance on which of the two files (sealed vs. reset ACTIVE) is likely to hold the missing entries, no reference to backing out the reset. Given rotation is explicitly framed as a "single-writer critical section" specifically because a concurrent append landing mid-rotation "could otherwise be silently lost or duplicated" (`:185`), the one operation defined to guard against silent loss lacks a defined response to detecting that exact condition.
**Plausibility:** Low-probability under the stated single-writer discipline, but the discipline's own residual (concurrent top-level sessions, direct hand-edits) is disclosed elsewhere as real, so a parity mismatch is not a purely theoretical outcome.
**Consequence:** Without a defined recovery branch, an operator (or an unattended agent following the procedure literally) could plausibly reset the ACTIVE file and treat the mismatch as informational rather than blocking, converting a *detected* discrepancy into a *silent* one — the worst-case outcome the check exists to prevent.
**Dimension:** Methodological Rigor (0.20).
**Mitigation:** Add one sentence: on parity mismatch, halt further appends, do not discard the pre-reset ACTIVE content, and escalate to the operator/user (P-020) before retrying — no new lint or tooling required, purely a procedural addition to existing prose.
**Acceptance Criteria:** The rotation procedure (design doc L1.4 and the rule file's Segment rotation section) names an explicit failure branch alongside the existing success branch.

---

## Minor Findings (abbreviated per template — Minor findings note the risk without full expansion)

- **IN-005-iter4-20260706 (Minor, Evidence Quality):** The claim that "the framework's existing AE-006e (mandatory checkpoint on compaction) is the interim compaction backstop" (`design/feedback-decision-log-convention-design.md:221`) is not evidenced against AE-006e's actual definition (`quality-enforcement.md`: "auto-checkpoint, session restart recommended" — a generic context-management escalation, not a targeted `git commit` of `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md`). Recommend either citing evidence that AE-006e's checkpoint action commits these specific files, or scoping the claim down to "a general context-loss mitigation, not a durability guarantee for these files specifically."
- **IN-006-iter4-20260706 (Minor, Internal Consistency):** "Being MEDIUM-tier, this convention is enforced by L1 (session-start rule awareness) + these ≤3 L5 lint checks" (`:221`) is phrased as present-tense operative fact, immediately followed two sentences later by "The ≤3 lint checks are a backstop, not a guarantee: they are not yet wired." The self-correction is present in the same paragraph so this does not rise to Critical, but the initial clause should be reworded to "is designed to be enforced by" to avoid a first-read overclaim, consistent with the fix already applied to IN-002 above.

---

## Recommendations

**MUST mitigate (Critical):**
- IN-001-iter4-20260706 — Rewrite the Null-alternative note per the Mitigation above; distinguish "disclosed/accepted trade-off" from "addressed."
- IN-002-iter4-20260706 — Propagate the "captured AND committed" qualifier into the shipped rule-file header.

**SHOULD mitigate (Major):**
- IN-003-iter4-20260706 — Name the `SubagentStop` candidate-capture case in the hook design, or make the same-turn append obligation explicit in the rule file.
- IN-004-iter4-20260706 — Add an explicit rotation-parity-failure branch (halt + escalate) to the procedure.

**MAY mitigate (Minor):**
- IN-005-iter4-20260706 — Scope the AE-006e citation accurately or evidence it.
- IN-006-iter4-20260706 — Soften "is enforced by" to "is designed to be enforced by" in the Enforcement-layer disclosure paragraph.

All six mitigations are wording/scoping edits. **None requires new machinery, a new lint check, a new file, or a new subsystem** — fully consistent with the package's own anti-bloat doctrine and with the task framing that a deliberately minimal, descoped-with-disclosure package is a valid posture. The defect in every Critical/Major finding here is a *disclosure/propagation* gap (a fix made in one place but not carried to a sibling artifact, or a claim of "addressed" where "disclosed" or "planned" is the accurate word) — not a missing mechanism.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-003: the background-agent capture pathway (explicitly named in the user's own requirement) has no defined capture obligation or reminder at the point a worker's candidate actually surfaces. |
| Internal Consistency | 0.20 | Negative | IN-001: the Null-alternative note directly contradicts the same document's own Adoption-plan gating and Install-stall-risk text. IN-002/IN-006: fixes made in one artifact were not propagated to a sibling artifact, or a claim precedes its own caveat. |
| Methodological Rigor | 0.20 | Negative | IN-004: the rotation procedure, though otherwise rigorous (numbered steps, explicit critical-section framing), omits the failure-recovery branch for its own "required" check. |
| Evidence Quality | 0.15 | Negative | IN-005: a specific framework-rule citation (AE-006e) is used as evidence for a claim it does not clearly support. |
| Actionability | 0.15 | Positive | Every finding here has a concrete, low-cost, wording-only mitigation with a verifiable acceptance criterion — no open-ended remediation. |
| Traceability | 0.10 | Neutral | All findings cite specific file+line evidence; no traceability gap was found in this pass. |

**Overall assessment:** REVISE. The package's architecture is sound and appropriately minimal for its MEDIUM tier; the defects found here are all textual (overclaim/propagation) rather than architectural, and all six are closable without adding machinery. The two Critical findings, however, sit exactly on the question this round was asked to answer — whether the package beats the null alternative — and the honest answer, once IN-001/IN-002 are corrected, is: **yes on structure and graduation, not yet (and possibly never, on durability) on the two axes the document currently claims are "addressed."**

# Refutation Panel — Remediation-Value Lens

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-001-findings.md` (S-001 Red Team Analysis, iteration 8)
**Lens:** remediation-value — does fixing the Critical materially change adoption outcomes, or is it churn? Fixes that would add machinery against the anti-bloat doctrine are refuted. Default: refuted if uncertain.
**Deliverables checked against:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`, `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`, live `FEEDBACK-LOG.md`
**Context read:** `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/restore-notes.md`

---

## Criticals in the target report

The Findings Table lists exactly one Critical: **RT-001-20260706-iter8** — "Background-agent 'candidate' handoff has no stated verbatim-fidelity requirement, so the log's own 'verbatim is the fidelity anchor' guarantee can silently degrade to a worker's paraphrase for the exact capture pathway FU.2 asks the design to favor."

---

## RT-001-20260706-iter8 — VERIFIED (remediation value confirmed)

**Citation accuracy check.** `feedback-decision-log-convention-design.md:58` reads exactly: "Word-for-word — verbatim means verbatim. The verbatim is the fidelity anchor: on any conflict, **verbatim wins**." `feedback-decision-log-convention-design.md:78` reads exactly (in the Concurrent-writer residual-risk bullet): "...worker and background agents return feedback/decision *candidates* via the existing P-003 orchestrator-worker handoff, and the orchestrator serializes the append. (A candidate is a short judgment-bearing text payload returned inline in the handoff's `key_findings`/summary...the orchestrator appends it verbatim.)" `feedback-decision-logs-standards.md:27` (LOG-M-005) and `FEEDBACK-LOG.template.md:22` both independently confirm the same silence: workers/background agents "return short candidates" that the orchestrator appends, with no instruction that the candidate content itself must be the operator's unaltered words rather than the worker's own summary of them. A repo-wide `candidate` grep across all 6 staged files (design doc, rule file, both templates, appendix, hook note) surfaces no clause anywhere requiring the candidate's `Verbatim` sub-field to be a direct quote as opposed to a worker paraphrase — the finder's central factual claim holds.

**Materiality check (why this is not the same class as the already-closed residuals).** The finder's distinguishing claim — that this gap is undetectable by any existing mechanism — checks out on inspection: unlike the tampering/reversal residuals closed in prior rounds (which are all *subsequent-edit* risks visible as a reviewable git diff against an already-committed entry, per `feedback-decision-log-convention-design.md:63/197`), a worker-paraphrased "candidate" enters the log looking like an ordinary, correctly-schema'd, first-commit entry — there is no diff to review, because the paraphrase *is* the original captured content. Lint 3 checks only terminal-disposition evidence, and lint 2 checks only id contiguity; neither inspects `Verbatim`-field provenance. This is a materially different failure class from the other disclosed residuals, so treating it as "just one more disclosure gap" in the recurring propagation-gap pattern would understate it.

**FU.2 framing nuance (partially overstated, does not change the verdict).** The live `FEEDBACK-LOG.md` FU.2 verbatim ("leverage background agents so that we don't burn through the main context window") is literally a one-time build-delegation instruction, not an explicit runtime requirement that ongoing feedback capture route through background agents as a "heavy-use" channel. The finding's "expected-heavy-use capture pathway" framing overstates FU.2's literal scope. However, the design doc's own text (line 78) independently chooses to generalize FU.2 into the standing concurrent-writer/candidate mechanism ("This is what keeps the serialized-append discipline compatible with FU.2's..."), so the deliverable itself — not just the finder — treats this pathway as the sanctioned way background-delegated work feeds the log. The overstatement is minor framing, not a factual defect in the underlying gap.

**Anti-bloat / machinery check.** The proposed countermeasure is a same-sentence clarification to the existing concurrent-writer bullet (design L1.1), LOG-M-005 (rule file), and both templates' single-writer-safety notes — no new lint, field, file, or subsystem. This matches the exact remediation register used successfully across all 7 prior rounds of this same tournament (one-clause wording fixes), so it does not trip the "adds machinery" refutation criterion.

**Remediation-value conclusion.** Fixing this changes real adoption behavior: it closes the one silent, undetectable route by which the convention's single load-bearing promise ("verbatim wins") could degrade specifically in the background-agent-delegated pathway the design itself ties to FU.2, at zero cost to the anti-bloat posture. This is not churn — it is a narrow but genuine, cheaply-closed gap in the design's central guarantee. VERIFIED.

---

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| RT-001-20260706-iter8 | VERIFIED | Citations accurate (design doc L58/L78, rule file L27, template L22); gap is real (no clause anywhere requires candidate-payload verbatim fidelity); distinct from already-closed tamper-evidence residuals (undetectable by any existing lint/diff mechanism); fix is one-clause wording only, no machinery — materially reduces a real risk to the design's core fidelity guarantee. |

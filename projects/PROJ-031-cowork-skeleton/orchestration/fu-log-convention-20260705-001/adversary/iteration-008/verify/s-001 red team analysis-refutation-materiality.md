# Refutation Panel — S-001 Red Team Analysis (Iteration 8), Materiality Lens

> Panel: adv-executor (refutation role) · Lens: materiality · 2026-07-06
> Target: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-001-findings.md`
> Rule: attempt to REFUTE every Critical. Default REFUTED if uncertain. Improbable edge cases and style points REFUTED even if true.
> Constitutional: P-003 no subagents · P-020 draft-only (no writes outside `projects/PROJ-031-cowork-skeleton/`) · P-022 cite file+line, label inference.

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Criticals under review |
| [RT-001 Disposition](#rt-001-background-agent-candidate-handoff-carries-no-verbatim-fidelity-requirement) | Full refutation reasoning |
| [Summary](#summary) | Final verdict table |

## Scope

The target report lists exactly **one** Critical finding: `RT-001-20260706-iter8` ("Background-agent 'candidate' handoff has no stated verbatim-fidelity requirement"). No other Critical entries exist in the Findings Table. This panel evaluates that single Critical.

## RT-001: Background-agent "candidate" handoff carries no verbatim-fidelity requirement

**Disposition: REFUTED (materiality)**

**What the finding claims:** the P-003 candidate-handoff pathway (design doc `feedback-decision-log-convention-design.md:78`; rule `feedback-decision-logs-standards.md:27` LOG-M-005; `FEEDBACK-LOG.template.md:22`) lacks a stated requirement that a worker/background agent's returned "candidate" preserve the operator's unaltered words, so a `Verbatim` field minted from such a candidate could silently be the worker's paraphrase — undetectable by any of the 3 L5 lint checks.

**Why this is refuted on materiality — it does not genuinely block the convention's purpose:**

1. **The pathway exists to serialize writers, not to relay live user speech.** `feedback-decision-log-convention-design.md:78` and the mirrored rule at `feedback-decision-logs-standards.md:27`/`:228` frame the candidate mechanism strictly as the fix for the concurrent-append race under LOG-M-005 ("when background agents are active, only the orchestrating context appends… workers return candidates via the P-003 handoff"). It is not framed, anywhere in the 6 files, as a live user-to-worker conversation relay. Per the framework's own P-003 orchestrator-worker topology (`agent-development-standards.md` Pattern 2, cited in the target report itself), dispatched worker/background agents do not hold a live chat turn with the human operator — they execute a task brief and return a result. The scenario the finding needs (the operator's literal words existing *only* inside an isolated worker context, unavailable to the orchestrator) is architecturally atypical, not the "expected-heavy-use" default the finding claims.

2. **The one pathway that genuinely relays newly-discovered text already has an explicit verbatim rule, independent of which agent performs the read.** Design doc `feedback-decision-log-convention-design.md:88` (capture trigger 4, inline-doc marker) states the marker line must be captured "verbatim" when "the assistant *reads* a doc containing such a marker" — this rule is agent-agnostic; it is not scoped to "only when the orchestrator itself reads the file." A worker agent harvesting an `FU:`/`DEC:` marker during its own subtask is already bound by this existing verbatim requirement, closing the one concrete content-relay scenario the finding's threat-actor profile could point to.

3. **The primary, load-bearing capture path never routes through a "candidate" at all.** LOG-M-001/LOG-M-002 (`feedback-decision-logs-standards.md:23-24`) describe direct capture in the orchestrating session's own context, where the operator's literal words are already present — no handoff, no candidate, no worker paraphrase risk. This is the path the design doc itself calls the everyday mechanism; the candidate path is the residual race-avoidance case, not the primary fidelity guarantee's main channel.

4. **"A short judgment-bearing text payload" (design doc `:78`) signals the candidate is understood to be the worker's own flag/judgment, not a verbatim-transcription claim.** "The orchestrator appends it verbatim" in the same line most plausibly describes the orchestrator's non-editing of what it receives (consistent with the append-only/no-second-guessing discipline used throughout this package), not an assertion that the payload equals the operator's original words. This is a real terminology overload worth a documentation tightening, but it is a wording ambiguity, not a demonstrated silent failure of the fidelity anchor for the mechanism's intended, disclosed use.

5. **The finding stacks multiple unlikely conditions to reach Critical severity:** (a) the operator's words exist only in a worker's isolated context, (b) that specific worker paraphrases rather than quotes, (c) no inline-doc-marker rule already covers the content, and (d) the orchestrator — which per this whole package's own single-writer/provenance discipline is the party responsible for what it appends — blindly appends without recognizing it lacks the original text. Per the task's instruction to default-refute uncertain, multi-assumption chains and to refute improbable edge cases even if theoretically true, this does not clear the materiality bar of genuinely blocking "no lost feedback" or "honest metadata" for the convention as designed and disclosed.

**Citations checked:** `feedback-decision-log-convention-design.md:58` (Verbatim field / fidelity-anchor row), `:78` (candidate-handoff clause), `:88` (inline-doc harvest verbatim rule), `:101` (Adoption profile — background agents "fully usable for the substantive work… only the shared-log append is serialized"); `feedback-decision-logs-standards.md:23-24` (LOG-M-001/002 direct-capture path), `:27` (LOG-M-005), `:228` (rule-file mirror); `FEEDBACK-LOG.template.md:22` (single-writer safety note).

## Summary

| ID | Severity (as reported) | Disposition | Basis |
|----|------------------------|-------------|-------|
| RT-001-20260706-iter8 | Critical | **REFUTED** | Candidate pathway is a race-avoidance mechanism, not the primary or an unguarded verbatim-relay channel; the one concrete content-relay case (inline-doc marker) already has an agent-agnostic verbatim rule (design doc line 88); scenario requires stacking multiple low-probability architectural assumptions atypical of the P-003 orchestrator-worker topology. Does not genuinely block the convention's core purpose. |

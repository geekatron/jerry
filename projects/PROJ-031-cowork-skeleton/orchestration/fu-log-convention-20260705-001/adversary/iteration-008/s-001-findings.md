# Red Team Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention (Iteration 8)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-001, iteration-008, VERIFIED-CRITICALS protocol — blind on `adversary/iteration-007/` and `adversary/iteration-008/` except this file and the readable `iteration-007/restore-notes.md` disposition record)
**H-16 Compliance:** `[INFERENCE]` — the blind protocol prohibits reading this round's `iteration-008/s-003-findings.md` or any other iteration-007/008 file. `iteration-007/restore-notes.md` (readable, owner disposition record) and the design doc's own Revision Changelog confirm Steelman-family findings (`SM-NNN`) have been applied and closed across all 6 completed rounds (v3-v8) of this same tournament sequence, and this is a continuing C4 tournament on the same package. Proceeding on the reasonable inference that S-003 has already run in this tournament's standing sequence; flagged as inference, not verified evidence, per P-022.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall Red Team assessment |
| [Threat Actor Profile](#threat-actor-profile) | Adversary goal/capability/motivation |
| [Verification Notes](#verification-notes) | Candidate findings checked and ruled out |
| [Findings Table](#findings-table) | RT-NNN inventory |
| [Finding Details](#finding-details) | Expanded Critical finding |
| [Recommendations](#recommendations) | P0 countermeasure |
| [Scoring Impact](#scoring-impact) | Dimension impact mapping |

---

## Summary

This iteration-8 pass re-verified (against the CURRENT deliverable text, not prior findings-as-stated) that the iteration-006 Criticals (RT-001 through RT-004) remain closed — confirmed. Per the VERIFIED-CRITICALS protocol and the task framing (already-disclosed residuals are not findings; only overclaims that genuinely block the convention's purpose count), this pass did not re-litigate the extensively and consistently disclosed residuals (concurrent-writer race, `--no-verify` lint bypass, transcript-retention dependency, silent-non-capture/Q5). Instead it hunted for a genuinely new instance of the package's own recurring failure class (a claim contradicting an adjacent disclosure, or a gap in the one guarantee the design calls its "fidelity anchor"). One candidate that looked promising on first read — a stale entry-count in the Adoption plan step 4 — was checked directly against the live `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md` and found to be **still accurate** (see [Verification Notes](#verification-notes)); it is reported here as a ruled-out candidate, not a finding, in the interest of not inflating the Critical count with an unverified claim. One genuine, previously-undisclosed Critical was found: the background-agent "candidate" handoff pathway — the exact pathway the user's own FU.2 requirement asks the design to support ("leverage background agents so we don't burn through the main context window") — has no stated requirement that the candidate payload preserve the operator's actual verbatim words, creating a silent gap in the convention's own "verbatim is the fidelity anchor" guarantee for a load-bearing, expected-heavy-use capture pathway. **Recommendation: REVISE (targeted, one-clause fix, no new machinery).**

## Threat Actor Profile

- **Goal:** Quietly degrade the fidelity of the historical record this convention exists to protect, while the log continues to *look* compliant (an entry exists, labeled `Verbatim`, in the expected schema) — or exploit an unstated assumption in the background-agent capture path so that what is recorded as "verbatim" is actually a worker agent's own paraphrase.
- **Capability:** Ordinary use of the framework's own P-003 orchestrator-worker handoff mechanism — exactly the mechanism FU.2 explicitly asks this design to lean on ("leverage background agents"). No special privilege or malice required; a careless or context-pressured worker agent is sufficient.
- **Motivation:** Under context pressure, a worker agent naturally compresses/summarizes findings before returning them (this is the framework's own general handoff convention — `agent-development-standards.md` CB-04: "key_findings (3-5 bullets) for quick orientation"). Applying that default habit to a feedback/decision "candidate" is the path of least resistance, not deliberate tampering — which makes it more likely to occur silently, not less.

---

## Verification Notes

**Candidate ruled out (not a finding): Adoption plan step 4 entry-count staleness.** The design doc's install-plan sentence enumerates "the 8 live entries that currently all carry no suffix (`FU.0`–`FU.4`, `DEC-LLM-001..003`)" (`feedback-decision-log-convention-design.md:255`). Given the live `FEEDBACK-LOG.md` has since grown to `FU.0`–`FU.11` (12 entries) plus `DEC-LLM-001`–`003` (3 entries) = 15 total, a first-pass reading suggested the design doc's implicit total (this sentence traces to the iteration-6 RT-003 finding, which cited "8 of 13") might now be stale. **Direct verification against the current text and the current live files shows this is NOT the case:** the current design doc text (line 255) does not state a total-entry count at all (that "13" figure existed only in the iteration-6 *finding description*, not in the remediated document) — it names only the 8 entries with **no** suffix, and a direct read of the live `FEEDBACK-LOG.md` confirms `FU.0`–`FU.4` and `DEC-LLM-001`–`003` are indeed still the only entries with no suffix; `FU.5`–`FU.11` all already carry a `(user label: X)` suffix and are covered by the separate, count-independent general clause "entries already carrying a `(user label: X)` suffix are renamed in place" one sentence earlier. No contradiction exists. Reported here per the VERIFIED-CRITICALS protocol's requirement to name checked-and-refuted candidates, not to silently drop them.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260706-iter8 | Background-agent "candidate" handoff has no stated verbatim-fidelity requirement, so the log's own "verbatim is the fidelity anchor" guarantee can silently degrade to a worker's paraphrase for the exact capture pathway FU.2 asks the design to favor | Rule Circumvention / Boundary | Medium | Critical | P0 | Missing | Internal Consistency |

---

## Finding Details

### RT-001: Background-agent "candidate" handoff carries no verbatim-fidelity requirement [CRITICAL]

**Attack Vector:** The design's single load-bearing promise, repeated at every entry-schema definition, is that the `Verbatim` field is "the fidelity anchor: on any conflict, verbatim wins" (`feedback-decision-log-convention-design.md:58`) and that capture means "Word-for-word — verbatim means verbatim" (same row). The one capture pathway the design builds specifically to satisfy the user's own explicit requirement — "leverage background agents so we don't burn through the main context window" (`FEEDBACK-LOG.md` FU.2 verbatim) — routes around this guarantee without saying so. The concurrent-writer section states: "worker and background agents return feedback/decision *candidates* via the existing P-003 orchestrator-worker handoff, and the orchestrator serializes the append. (A candidate is a short judgment-bearing text payload returned inline in the handoff's `key_findings`/summary — a stated exception to CP-01's file-paths-only preference... the orchestrator appends it verbatim.)" (`feedback-decision-log-convention-design.md:78`). "The orchestrator appends it verbatim" describes only that the orchestrator does not further edit the *candidate payload* — it says nothing about whether the candidate payload itself equals the operator's own unaltered words, versus the worker agent's own summary/paraphrase of what it judged to be feedback. The design places this payload explicitly inside a handoff's `key_findings`/summary field — which is the framework's own general-purpose *compressed orientation* field (`agent-development-standards.md` CB-04: "Use `key_findings` (3-5 bullets) for quick orientation; defer detail to file reads" — a 10:1 compression convention, not a byte-exact quote field). Nothing in any of the 6 deliverable files instructs a worker agent to quote the operator's original text unaltered inside that candidate, as opposed to characterizing it in the worker's own words (which is the framework's own default handoff habit). The result: an entry minted from a background-sourced candidate can carry a `Verbatim` field that is, in fact, the worker's paraphrase — visually and structurally indistinguishable from a directly-captured, genuinely-verbatim entry, since both use the identical schema and neither the L5 lint (which checks only presence, ids, and terminal evidence — never content fidelity) nor any other mechanism in the package would ever detect the substitution. This is exactly the class of gap the package's own Red Team threat-actor framing (iteration-6, still applicable) describes: "preserving a plausible appearance of compliance" while the substance quietly degrades — and it is exactly the AP-03 "Telephone Game" anti-pattern named in `agent-routing-standards.md` ("context degrades through serial handoffs... each agent summarizes and re-interprets"), occurring at the one point in this design where summarization is explicitly forbidden by the design's own stated rule.

**Category:** Rule Circumvention (compliance in letter — an entry exists, labeled Verbatim, in schema — not in spirit — the text may not be the operator's own words) with a Boundary component (the orchestrator/worker handoff boundary is where the fidelity guarantee silently drops).
**Exploitability:** Medium — requires no special access or intent, only ordinary use of the exact background-agent-heavy workflow the user explicitly commissioned (FU.2); a worker under normal context-compression habit is sufficient, no adversarial intent needed.
**Severity:** Critical — this is not a peripheral residual; it is a silent failure of the design's single named "fidelity anchor" guarantee, occurring specifically in the capture pathway the design was built to make safe for heavy use, with no detection mechanism anywhere in the package (lint 3 checks only terminal-disposition evidence presence; nothing checks Verbatim-field provenance).
**Existing Defense:** Missing — no clause in any of the 6 files requires the candidate payload to be the operator's unaltered original text; the only existing safeguards (LOG-M-005 single-writer discipline, the P-003 handoff exception to CP-01) address *who* appends and *how the handoff is structured*, not *whether the payload's content is verbatim*.
**Evidence:** `feedback-decision-log-convention-design.md:78` (candidate-handoff clause, "the orchestrator appends it verbatim" — describes payload handling, not payload provenance); `feedback-decision-log-convention-design.md:58` (Verbatim field row: "Word-for-word — verbatim means verbatim... on any conflict, verbatim wins"); `feedback-decision-logs-standards.md:27` (LOG-M-005: "workers... return short candidates inline via the P-003 handoff, appended the same turn" — same silence on candidate content fidelity); `FEEDBACK-LOG.template.md:22` ("Background agents return short *candidates* the orchestrator appends; they do not write here directly" — again silent on fidelity); cross-reference `.context/rules/agent-development-standards.md` CB-04 ("key_findings (3-5 bullets) for quick orientation... 10:1 compression ratio") — the general-purpose field this design explicitly reuses for the candidate payload is, by the framework's own standard, a summarization field, not a verbatim-quote field.
**Dimension:** Internal Consistency (the design's own universal "verbatim means verbatim" claim is not qualified or defended at the one pathway where a general-purpose summarization convention is explicitly reused to carry it).
**Countermeasure:** Add one clause to the concurrent-writer bullet (design L1.1) and LOG-M-005 (rule file), and to both templates' single-writer-safety notes: a worker/background-agent candidate MUST quote the operator's original text unaltered (verbatim) as its own sub-field, distinct from any judgment note the worker adds about why it might be feedback; the orchestrator appends that quoted sub-field as the entry's Verbatim, never the worker's paraphrase. This is a wording-only addition — zero new lint, file, or subsystem — consistent with the deliverable's own established anti-bloat remediation pattern (the same class of fix as RT-001/RT-002/RT-004 in iteration-6).
**Acceptance Criteria:** L1.1 (design doc), LOG-M-005 (rule file), and both templates' single-writer-safety notes state explicitly that a background/worker-agent candidate carries the operator's original text unaltered as a distinct quoted sub-field, and that this quoted text — not any worker paraphrase — becomes the entry's Verbatim field.

---

## Recommendations

**P0 (Critical — MUST mitigate before acceptance):**
- **RT-001** — Add the verbatim-quoting requirement to the candidate-handoff clause (design L1.1), LOG-M-005 (rule file), and both templates' single-writer-safety notes. Acceptance: all three/four locations state that the candidate's quoted operator text — not a worker paraphrase — becomes the Verbatim field.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No missing attack-vector category; this pass targeted verified overclaims only, per the task's narrowed scope. |
| Internal Consistency | 0.20 | Negative | RT-001: the package's universal "verbatim means verbatim" / "fidelity anchor" claim is unqualified at the one pathway (background-agent candidates) explicitly built to reuse a summarization-oriented handoff field. |
| Methodological Rigor | 0.20 | Neutral | The candidate-ruled-out entry-count check (see Verification Notes) demonstrates the direct-evidence verification this round applied before accepting a finding as genuine, consistent with H-15/P-022. |
| Evidence Quality | 0.15 | Positive | RT-001 is grounded in a direct cross-reference between this deliverable's own text and a separate, already-ratified Jerry standard (`agent-development-standards.md` CB-04) describing what the reused handoff field actually guarantees; the entry-count candidate was independently verified against the live bootstrap files and correctly ruled out rather than reported speculatively. |
| Actionability | 0.15 | Neutral | The one P0 countermeasure is a one-clause wording addition, matching the deliverable's own established remediation style. |
| Traceability | 0.10 | Negative (mild) | RT-001 traces to a specific line in the design doc and a specific cross-referenced framework standard; the gap exists precisely because that cross-reference was never made in the deliverable itself. |

**Overall assessment:** No finding in this pass invalidates the deliverable's core architecture, which remains, after 8 rounds, substantively sound. One genuinely new Critical was found: the background-agent candidate-handoff pathway lacks a stated verbatim-fidelity requirement, creating a silent gap in the design's own central "verbatim is the fidelity anchor" guarantee for the exact capture pathway the user's FU.2 requirement asks the design to lean on most heavily. The proposed countermeasure is a one-clause wording addition — zero new lint, file, or subsystem — consistent with the deliverable's own anti-bloat doctrine. **Recommendation: REVISE (targeted).**

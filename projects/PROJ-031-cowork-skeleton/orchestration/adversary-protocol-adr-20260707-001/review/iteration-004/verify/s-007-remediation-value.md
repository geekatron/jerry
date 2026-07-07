# Refutation Panel — Remediation-Value Lens (S-007, iteration 4)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Panel metadata |
| [Scope](#scope) | Which findings were adjudicated |
| [Verdicts](#verdicts) | Per-finding VERIFIED/REFUTED with evidence |
| [Summary](#summary) | Tally |

---

## Header

**Lens:** Remediation-value ("would the fix materially improve the decision quality, or is it churn/machinery-adding? REFUTED if churn.")
**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-004/s-007-findings.md`
**Reference ADR:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Panel rule applied:** default-REFUTED on uncertainty; blind to other lenses/panels.

---

## Scope

Per the ADR's own D-1 decision, refutation panels adjudicate **claimed Criticals only** (Majors/Minors are advisory and are not panelled). The target report contains exactly one Critical:

- **CC-001-iter4** — "MEDIUM-tier framing contradicted by HARD-tier vocabulary in the proposed scorer edit"

CC-002/CC-003/CC-004-iter4 are Major/Minor and are out of this panel's scope by the protocol's own gating rule.

---

## Verdicts

### CC-001-iter4: REFUTED

**Finder's claim:** The ADR's repeated thesis ("no HARD rule is touched," "25/25 ceiling untouched") is contradicted because the proposed edit to `adv-scorer.md` (ADR lines ~742–749, D-5 row ~482, WI-3 AC ~926) uses `REQUIRED`/`mandatory` — words the Tier Vocabulary table (`.context/rules/quality-enforcement.md` "Tier Vocabulary" section) classifies as HARD-tier, "Cannot override," counted against the <=25 ceiling.

**Evidence checked:** The Tier Vocabulary table's "Max Count <= 25" column and the adjacent "HARD Rule Ceiling Derivation" section are both scoped, by their own text, to the **HARD Rule Index** — the enumerated H-01…H-36 registry ("The ceiling of 25 HARD rules is derived from…"; "Current count: 25 HARD rules (post-EN-001/EN-002 consolidation)."). Neither section states or implies that any occurrence of the word `REQUIRED`/`MUST`/`NEVER` anywhere in an agent definition or skill file consumes a ceiling slot. Agent-behavioral guardrail language already uses this exact vocabulary pervasively without per-instance ceiling registration — e.g. `agent-development-standards.md`'s own Guardrails Template mandates `forbidden_actions` phrased "P-003 VIOLATION: NEVER spawn recursive subagents," and the target ADR's own WI-1 AC uses "NEVER edit the deliverable or any prior verdict file" as an agent guardrail — none of these are treated as new H-IDs. The `adv-scorer.md` Delta-Reconciliation "REQUIRED" clause the finder cites is the same category: an internal agent-behavioral mandate inside a skill's agent file, not a new entry in the `.context/rules/quality-enforcement.md` HARD Rule Index. The finder's core premise therefore over-extends the Tier Vocabulary table's scope from "framework-level HARD Rule Index registration" to "any HARD-sounding word anywhere," which the cited SSOT text does not support.

**Remediation-value analysis:** Even granting the finder's premise arguendo, the finding's own proposed remediation (ADR lines 65) offers exactly two paths: (a) downgrade `REQUIRED` to `SHOULD`, which would weaken a design element the ADR's own D-5 rationale shows was empirically load-bearing ("every verified round already did this and it demonstrably prevented variance-anchoring" — ADR ~line 435-440), turning a validated anti-anchoring control into an optional one for no evidentiary reason; or (b) route the clause through the HARD Rule Ceiling's Exception Mechanism (a C4-reviewed ADR, tracked reversion deadline, max +3 slots, 3-month sunset) — disproportionate machinery for what is, on inspection, ordinary agent-instruction phrasing indistinguishable from dozens of other `MUST`/`NEVER` guardrail clauses already present throughout the codebase's agent definitions. Neither remediation path improves decision quality: (a) degrades the substance of a decision already justified by evidence in the same document, and (b) invokes a heavyweight governance process to solve a labeling non-problem. A genuinely low-cost fix — one clarifying sentence distinguishing "agent-instruction imperative vocabulary" from "HARD Rule Index registration" — is not among the finding's offered remediations, and is not necessitated by any actual ambiguity in the cited SSOT text. This is the textbook churn case the remediation-value lens is designed to catch: technically-phrased but substantively non-actionable without either weakening the decision or adding disproportionate process.

**Verdict:** REFUTED. The premise conflates two distinct scopes in the SSOT (framework HARD-rule ceiling registration vs. ordinary agent-instruction vocabulary), and both of the finding's own proposed fixes are net-negative or disproportionate rather than value-adding. Per this panel's rule, a finding whose only offered remediations are churn/machinery-adding is REFUTED regardless of the underlying observation's surface plausibility.

*(Note: the finding's "Additionally" clause — assigning an owner/trigger to RSK-6's dual-protocol sunset — is a separable, lower-cost suggestion with independent merit, but it is not the finding's central claim and does not by itself rescue CC-001-iter4's primary thesis from a REFUTED verdict under this lens; it is not a standalone Critical and is outside this panel's Critical-only scope.)*

---

## Summary

| Finding ID | Severity | Verdict (remediation-value) |
|---|---|---|
| CC-001-iter4 | Critical | **REFUTED** |

**Verified:** 0
**Refuted:** 1 (of 1 Critical in scope)

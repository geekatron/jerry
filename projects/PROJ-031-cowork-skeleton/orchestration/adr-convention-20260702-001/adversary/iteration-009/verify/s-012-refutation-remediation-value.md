# S-012 FMEA Critical-Finding Refutation — Remediation-Value Lens (Iteration 9)

> **Lens:** Remediation-value — would fixing this materially change real adoption outcomes, or is it churn?
> **Panel scope:** Critical findings only (012-001, 012-002, 012-003), per mandate.
> **Protocol:** Blind — sibling refuter/panel outputs NOT read. Target report + current deliverables + subtraction-pass-notes.md (R-1..R-17 register) WERE read.
> **Default posture:** Refute if uncertain.

---

## Verdict Table

| Finding ID | RPN | Verdict | One-line reason |
|---|---|---|---|
| 012-001 | 512 | **VERIFIED** | Live, present-tense overclaim in the ratified document misleads a reader *today*, not a deferred concern; one-sentence fix, no new machinery. |
| 012-002 | 245 | **REFUTED** | Optional schema generalization for a rare, already-handled-in-this-instance pattern; adding a frontmatter field (even "advisory") is exactly the incremental-machinery-growth the subtraction doctrine exists to prevent. |
| 012-003 | 252 | **REFUTED** | Concerns an implementation-time decision (grandfather-baseline computation) explicitly deferred to the not-yet-built M-6 lint script; "already scheduled elsewhere," no current reader is affected, compound/low-probability scenario. |

---

## 012-001: Plugin-Distribution "Zero-Tooling Guidance" Overclaim

**Verdict: VERIFIED**

**Evidence checked:**
- `ADR-PROJ031-004-adr-identifier-convention.md:675` confirmed verbatim: "What carries value downstream on day one is the *guidance*, which needs no tooling." — present-tense, unqualified.
- `ADR-PROJ031-004-adr-identifier-convention.md:530` confirms M-2 ("Author `.context/rules/adr-standards.md`") is `TBD-Task`, no worktracker Task/GH Issue, per the ADR's own Claim-Status disclosure at line 525 ("zero worktracker Task entities and zero GitHub Issues exist for any Migration-Plan row").
- `phase3-skeleton-generation-design.md:159` confirmed: `git rm -r projects/ tests/ skills/.graveyard .github` is the VALIDATED (not merely recommended) strip set — `projects/` is unconditional.
- Both reviewed deliverables (`ADR-PROJ031-004...md`, `design/adr-standards-rule-draft.md`) physically live under `projects/PROJ-031-cowork-skeleton/`, inside that unconditional strip-set, today.

**Reasoning:** This is not a deferred/scheduled concern — it is a live inaccuracy in a document already `ACCEPTED` (ratified 2026-07-05) that a reader evaluating PROJ-031's stated CoWork/plugin distribution claim would rely on *now*. Unlike 012-002/012-003, the harm is not contingent on some future built-but-not-yet-existing mechanism; it is a mischaracterization of present state (the guidance text itself is stripped from any build cut before M-2 lands, which has no committed date). The corrective action is a single disclosure sentence, adds zero machinery, and directly serves the remediation-value bar: a downstream adopter who reads line 675 today and expects to receive the convention's guidance in a distributed skeleton build would be wrong, and the fix prevents that concrete, immediate misunderstanding. None of the three refutation disqualifiers (optional polish / already scheduled elsewhere / adds machinery) apply.

---

## 012-002: No General Schema Field or Lint Check for the ADR↔Companion-Rule-File Relationship

**Verdict: REFUTED**

**Evidence checked:**
- Frontmatter Schema block confirmed at `adr-standards-rule-draft.md:100-117` (13 fields, no companion-rule-file field); ADR mirror consistent with this.
- M-2 (`ADR-PROJ031-004...md:530`) and M-9 (`:539`) confirmed as a bespoke, manual, one-off "reciprocal cross-link repair" instruction specific to *this* ADR/rule-draft pair only.
- L-7 spec (`adr-standards-rule-draft.md:179`) confirmed scoped to `superseded_by`/`promoted_to`/`promoted_from` only — no companion-rule-file check, as claimed.

**Reasoning:** The finding is factually accurate but fails the remediation-value bar. The concrete instance in front of this review (this ADR + its own rule draft) already has its manual fix in place via M-2/M-9 — nothing is broken *today*. What remains is a speculative concern about *hypothetical future* ADR-plus-companion-rule-file pairs, a pattern that has recurred only ~3 times across the framework's entire history. The proposed remedy — adding an optional advisory `companion_rule_file:` frontmatter field — is itself incremental schema growth of exactly the kind this package's subtraction doctrine (`subtraction-pass-notes.md` Step 2, "monotonic growth... each new rule a new correctness claim to attack") was adopted to reverse. The finding's own fallback ("disclose as a residual instead") is lower-cost but still addresses a not-yet-manifested future recurrence rather than a present defect — this is optional polish/future-proofing, not a fix that changes any real adoption outcome for the current ratified convention. Per the lens's default-to-refute instruction, this is churn.

---

## 012-003: Grandfather-Baseline Temporal Anchor Creates an Unbounded Post-Ratification Amnesty Window

**Verdict: REFUTED**

**Evidence checked:**
- `ADR-PROJ031-004-adr-identifier-convention.md:688` confirmed verbatim: grandfathering resolved against "a static adoption-time baseline — the enumerable set of ADR files that exist **when the lint first ships**... captured **once** as a data list in M-6, a one-time artifact, *not* standing machinery."
- `ADR-PROJ031-004-adr-identifier-convention.md:223` (D-4) confirmed: "Existing scope-prefixed and legacy ADRs are grandfathered... The 15 pre-existing dialect ADRs remain valid legacy-dialect instances in place" — ties grandfathering to pre-existing/legacy framing, as the finding states.
- `adr-standards-rule-draft.md:48` (ADR-M-003) confirmed: dialect remains SOFT `MAY`-permitted indefinitely for new ADRs, no expiry stated.
- `ADR-PROJ031-004-adr-identifier-convention.md:536` (M-6) confirmed `TBD-Task + GH Issue`, no committed timeline; the ADR itself already flags M-6/lint delivery as the single highest-rated risk (FM-5, per the report's own citation).

**Reasoning:** The logical point is internally consistent — the spec text does anchor the baseline to "when the lint ships" rather than to the ratification date — but the finding fails the remediation-value bar on three grounds. First, the harm scenario requires a compound chain of not-yet-real conditions: M-6 must actually be built (uncertain — already the package's own top disclosed risk, R-1), a materially long gap must elapse before it ships, and new non-compliant ADRs must be minted specifically in that gap. Second, the actual mechanics of "how the grandfather baseline is computed" is an implementation detail of the not-yet-written `scripts/lint_adr_convention.py` (M-6) — the ADR text itself already frames the 18-file baseline as "captured once as a data list in M-6," i.e., a decision explicitly deferred to M-6's implementation, satisfying the "already scheduled elsewhere" refutation criterion. Third, no reader or adopter is affected by this today: the convention's realized value (per its own repeatedly-stated doctrine) is the zero-tooling guidance, and this finding concerns a corner case of an enforcement mechanism that does not exist and may never ship. Pre-specifying the exact grandfather-computation semantics in the ADR now, ahead of M-6's actual implementation, is premature spec-perfectionism rather than a fix with concrete present-day adoption impact.

---

## Summary

- **Verified (1 of 3):** 012-001.
- **Refuted (2 of 3):** 012-002, 012-003.

*No subagents spawned (P-003). No files outside mandate edited (P-020). All verdicts cite file+line evidence directly read from the deliverables; no fabricated citations (P-022).*

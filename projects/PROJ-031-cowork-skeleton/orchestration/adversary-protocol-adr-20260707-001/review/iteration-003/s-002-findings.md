# Devil's Advocate Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata and H-16 compliance |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All DA-NNN findings at a glance |
| [Finding Details](#finding-details) | Full evidence and analysis per Critical/Major finding |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action list |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Header

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3 (this ADR self-declares c-007: "auto-C3 minimum" per AE-002/AE-003)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-002 blind pass, iteration 3)
**H-16 Compliance:** `iteration-003/s-003-findings.md` exists in this iteration's review folder, confirming S-003 (Steelman) ran prior to this S-002 pass. Per BLIND constraints for this execution, the S-003 file's content was NOT read — only its existence was verified (Glob) to satisfy the H-16 ordering gate before this Devil's Advocate pass began.

---

## Summary

3 Critical and 1 Major counter-argument identified, all targeting claims the ADR treats as settled
or adequately mitigated. Two Criticals attack the specification's internal consistency at points the
ADR itself never examines: (DA-001) the D-1 + D-2 decision combination silently removes the *existing*
Critical-severity gate at C1–C2 without disclosure, and (DA-002) the WI-7/WI-8 "generalization gate"
that is offered as the mitigation for the n=2 external-validity risk (RSK-7) does not actually gate
the mechanism's operational deployment to non-ADR genres — only a documentation pointer. The Major
finding (DA-003) is the token-cost-honesty attack explicitly commissioned: the ADR's cost model
counts verification cost in agent-invocations only, never in context/token volume, materially
understating cost for large C4 artifacts (this ADR is itself a 953-line example). Recommend REVISE:
address DA-001 and DA-002 before this ADR proceeds toward ratification: both are specification gaps
in the chosen design, not disagreements with the design's premise, and both are fixable by
clarification/scope-narrowing (consistent with the ADR's own subtraction-first doctrine) rather than
by adding machinery.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i3 | Verified-only gating (D-2) + no-panel-at-C1–C2 (D-1) combination silently disables the *existing* Critical-severity auto-REVISE gate at C2, undisclosed anywhere in Risks/Consequences | Critical | ADR lines 109-111, 325-326, 439-440, 514, 847; `skills/adversary/agents/adv-scorer.md:166-167` | Internal Consistency |
| DA-002-i3 | WI-7's "generalization gate" (precondition on WI-8) only blocks a documentation pointer; WI-1–WI-6 (the actual mechanism) deploy framework-wide, all genres, with no such gate — the stated RSK-7 mitigation is largely illusory | Critical | ADR lines 830, 848, 851; `skills/adversary/agents/adv-selector.md:89-107` | Internal Consistency |
| DA-003-i3 | Cost model (c-004) measures verification cost only in agent-invocation count, never in context/token volume; understates true cost for large C4 artifacts | Major | ADR lines 241, 723-734, 796-798, 470 | Evidence Quality |
| DA-004-i3 | RSK-7 rates probability/impact as MED/MED despite the ADR's own "maximally correlated, not merely small-n" framing of the n=2 evidence base, which arguably supports a higher probability rating | Minor | ADR line 830 | Evidence Quality |

**Finding ID Format:** `DA-{NNN}-i3` (iteration 3 execution scope).

---

## Finding Details

### DA-001-i3: The new severity-gating rule cannot ever fire at C1–C2, silently regressing an existing control [CRITICAL]

**Claim Challenged:** Decision D-2 (line 440): *"Only panel-VERIFIED Criticals trigger automatic-REVISE. Refuted claims carry zero dimension weight. Disclosed residuals are valid MEDIUM posture, not findings."* This is stated as an unconditional replacement of the current rule, with no criticality qualifier. WI-3's acceptance criteria (line 847) confirms a full replacement: *"Lines 166–167 rule replaced with verified-only gating."*

**Counter-Argument:** The current rule being replaced — `skills/adversary/agents/adv-scorer.md:166-167`: *"Any Critical finding from adv-executor reports → automatic REVISE regardless of score"* — is **not criticality-gated**; it fires at every criticality level today, including C2 (confirmed by direct read of the cited file; the special-cases list at lines 165-168 contains no criticality branch). Decision D-1 (line 439) explicitly withholds the verification panel from C1–C2: *"C4 all Criticals; C3 Criticals only; C1–C2 none."* Figure 1's own Mermaid source (line 514) draws this literally: `CLAIMS -- "No, or C1-C2" --> F` — a C1/C2 deliverable's claimed Criticals route straight to the scorer, bypassing the panel entirely. Once the D-2 replacement rule is installed, a Critical claim can be `panel-VERIFIED` only if a panel actually ran on it. Since no panel ever runs at C1–C2 (D-1), **no Critical claim raised at C2 can ever satisfy D-2's trigger condition** — the automatic-REVISE special case becomes permanently unreachable at exactly the criticality tier (C2) where S-002 (Devil's Advocate) is a *required* strategy per `.context/rules/quality-enforcement.md` and therefore where Critical claims are routinely expected to occur. This is not a hypothetical edge case: C2 is Jerry's "Standard" tier (3-10 files, one-day reversibility) and is the most common criticality level for day-to-day deliverable review. The ADR's own Negative Consequences list (lines 794-809) and Risk register (lines 822-830) enumerate five risks and five negative consequences but none names this regression; RSK-3 (line 826) addresses only *miscategorized* C4-work-run-as-C2, not the inherent C2 gating gap that exists even when categorization is correct.

**Evidence:** Direct quotes and line citations above; `skills/adversary/agents/adv-scorer.md:166-167` read directly (not inferred).

**Impact:** If ratified as written, every C2 tournament in the framework silently loses its hard Critical-severity gate the moment WI-3 lands — the opposite of this ADR's stated purpose (closing a gate that let false claims through). A genuinely valid Critical raised by S-002 or S-007 at C2 would fall through to ordinary composite scoring (a soft, dimension-weighted signal) rather than the hard automatic-REVISE block it triggers today. This directly threatens the ADR's core pillar — restoring trust in the Critical-severity signal — at the one tier the panel deliberately excludes for cost reasons.

**Dimension:** Internal Consistency (primary) — the D-1/D-2 combination is self-contradictory once traced to its logical conclusion; also Completeness (the gap is nowhere enumerated in Risks or Consequences).

**Response Required:** Either (a) explicitly retain the current unconditional rule for C1–C2 as a fallback when no panel ran ("verified-only gating applies where a panel exists; the pre-existing unconditional rule remains in force at C1–C2"), or (b) explicitly disclose and accept the regression as an intended trade-off with a named mitigation. Option (a) is a small textual clarification, not new machinery, and is consistent with the ADR's own subtraction-first doctrine (D-3).

**Acceptance Criteria:** The ADR (and WI-3's acceptance criteria) explicitly states what governs Critical-severity gating at C1–C2 after the D-2 rule change, and Risks/Consequences names the C1–C2 gating-loss trade-off if option (b) is chosen instead of (a).

---

### DA-002-i3: The RSK-7 "non-ADR-genre validation gate" (WI-7→WI-8) does not gate the mechanism's actual deployment [CRITICAL]

**Claim Challenged:** RSK-7's mitigation (line 830): *"WI-8's validation pass is required to include at least one non-ADR-genre C3/C4 deliverable before the protocol is treated as framework-general."* WI-7's acceptance criteria (line 851) operationalizes this as: *"the SSOT pointer — the concrete act of treating the protocol as framework-general — MUST NOT land until WI-8's non-ADR-genre validation has run."*

**Counter-Argument:** The ADR defines "the concrete act of treating the protocol as framework-general" as merely updating one cross-reference in `quality-enforcement.md` (WI-7). But the actual generalizing act — the code/behavior change that makes every C3/C4 `/adversary` tournament, of any genre, run the Verify stage — is WI-1 (adv-verifier agent), WI-2 (s-016 template), WI-3 (adv-scorer gating), and WI-4 (adv-selector Verify-stage insertion). None of these four items depends on WI-8 (the dependency column for WI-1–WI-4, lines 845-848, lists only each other, never WI-8). `adv-selector.md`'s own criticality-escalation logic (`skills/adversary/agents/adv-selector.md:89-107`, read directly) is genre-agnostic: AE-001 through AE-005 key on path patterns (`docs/governance/`, `.context/rules/`, `decisions/`, security keywords) and content keywords, never on deliverable genre. WI-4's acceptance criteria (line 848) likewise contains no genre restriction. Consequently, the moment WI-1–WI-5 ship, **every** C3/C4 tournament — a security-architecture review, an API contract review, a code review — is already routed through the Refutation-Panel Verify stage in production, regardless of whether WI-8's non-ADR-genre validation has run. The only thing actually gated behind WI-8 is a documentation cross-reference that most users of the `/adversary` skill will never read before their tournament executes.

**Evidence:** Line 830 (RSK-7), line 848 (WI-4 AC, no genre restriction), line 851 (WI-7 precondition text), `skills/adversary/agents/adv-selector.md:89-107` (genre-agnostic AE gating, confirmed by direct read).

**Impact:** RSK-7 is the ADR's own named response to the explicit "n=2 packages: overfitting risk" concern — the record is "100% C4... same author role, same reviewer roster, same project, days apart (maximally correlated, not merely small-n)" (ADR's own words, lines 306-308). If the stated safeguard against premature generalization is definitionally scoped to a cross-reference update rather than to actual tournament behavior, the safeguard provides no protection against the very overfitting risk it is invoked to mitigate. A non-ADR-genre C3/C4 deliverable reviewed the day after WI-1–WI-5 ship (and well before WI-8 runs) would already be subject to a verification protocol whose entire evidentiary basis is two same-author, same-project ADR reviews.

**Dimension:** Internal Consistency (primary) — the mitigation named for RSK-7 does not achieve what RSK-7 claims it achieves; Traceability (secondary) — the WI dependency graph does not trace to the risk it purports to close.

**Response Required:** Either (a) make WI-1–WI-5 (or at minimum WI-4, the adv-selector edit that actually activates the Verify stage) depend on WI-8, so the mechanism itself does not activate framework-wide until non-ADR-genre validation has run, or (b) explicitly narrow RSK-7's claimed scope to acknowledge that the mechanism will be live for all genres immediately and that WI-8 only validates after the fact, retroactively, not as a pre-deployment gate.

**Acceptance Criteria:** The dependency graph in Work-Item Decomposition and the RSK-7 mitigation text agree on what WI-8 actually blocks, and that description matches the true activation behavior of the shipped code.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- **DA-001-i3:** Add explicit text specifying what governs Critical-severity gating at C1–C2 once the D-2 rule replaces `adv-scorer.md:166-167` — either retain the unconditional rule as a C1–C2 fallback, or disclose the regression as an accepted, named trade-off in Risks/Consequences. Acceptance criteria: the ADR states one of these two positions unambiguously, and WI-3's acceptance criteria is updated to match.
- **DA-002-i3:** Either add a WI-8 dependency to WI-4 (or WI-1–WI-5 collectively) so the Verify-stage mechanism does not activate for non-ADR genres before validation, or rewrite RSK-7's mitigation text to honestly describe WI-8 as post-hoc validation rather than a pre-deployment gate. Acceptance criteria: the Work-Item dependency graph and the RSK-7 risk-mitigation narrative describe the same activation behavior.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-003-i3:** Add a token/context-cost estimate to the "Cost model (c-004)" section — even an order-of-magnitude range (e.g., "~N tokens per lens invocation for a deliverable of size S, given each of the 3 blind lenses independently reloads the deliverable and any cited evidence files") — so the cost-proportionality argument (c-004, Alignment "Implementation Effort: M") is evaluable in the same unit the framework already tracks elsewhere (`agent-development-standards.md` CB-01 through CB-05 measure context budget in tokens, not invocation counts). Acceptance criteria: the Cost model section states both an invocation-count and a token/context-volume estimate.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-004-i3:** Consider whether RSK-7's probability rating (MED) is consistent with its own "maximally correlated, not merely small-n" framing; a HIGH probability rating (with impact unchanged at MED) may better reflect the honesty the ADR otherwise displays. Acknowledgment sufficient.

---

## Scoring Impact

Mapping to the 6 S-014 scoring dimensions (`.context/rules/quality-enforcement.md`: Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10):

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001: the C1–C2 gating regression is absent from Risks (7 entries) and Negative Consequences (5 entries), a coverage gap in the ADR's own self-audit. |
| Internal Consistency | 0.20 | Negative | DA-001 and DA-002 are both self-contradictions: a rule that can never fire (DA-001) and a mitigation that does not gate what it claims to gate (DA-002). |
| Methodological Rigor | 0.20 | Neutral | The options-analysis method (steelman-first, D-1..D-6) is otherwise rigorously applied; these findings are specification gaps within an otherwise sound method, not method failures. |
| Evidence Quality | 0.15 | Negative | DA-003: the cost model's evidence (invocation counts) does not support its own proportionality claim without a token/volume dimension; DA-004: RSK-7's probability rating sits in tension with its own supporting prose. |
| Actionability | 0.15 | Negative | DA-002: the WI dependency graph, as written, cannot be acted on to prevent the outcome RSK-7 warns against — a reader following the WIs exactly still gets premature generalization. |
| Traceability | 0.10 | Negative | DA-002: RSK-7's mitigation claim does not trace forward correctly into the WI-1–WI-8 dependency structure it references. |

**Result:** 2 Critical and 1 Major finding identified (plus 1 Minor). Both Criticals attack the ADR's
internal consistency at points genuinely unexamined elsewhere in the document (confirmed by direct
reads of the cited deliverable lines and the two referenced `skills/adversary/agents/*.md` files, not
inference from the ADR's own summary of them). Neither finding disputes the chosen decisions (D-1
through D-6) on their merits; both attack gaps in how those decisions compose with each other and with
the work-item sequencing meant to operationalize them. Both are resolvable by clarification/scope
text, consistent with the ADR's own subtraction-first doctrine, not by adding new machinery.

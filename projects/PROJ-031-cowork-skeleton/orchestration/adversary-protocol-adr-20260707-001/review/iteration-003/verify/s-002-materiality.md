---
title: Refutation Panel — Materiality Lens — S-002 Devil's Advocate (iteration 3)
lens: materiality
target: projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-003/s-002-findings.md
scope: Criticals only (per ADR's own "panels adjudicate Criticals only" rule)
---

# Refutation Panel — Materiality Lens

**Reviewer:** adv-verifier (blind materiality lens, iteration 3)
**Rule applied:** DEFAULT-REFUTED on uncertainty. A finding is VERIFIED only if it genuinely
undermines the ADR (wrong decision, unimplementable spec, false evidence) — not merely a
style/edge-case concern.

---

## DA-001-i3: verified-only gating (D-2) + no-panel-at-C1–C2 (D-1) silently disables the existing
Critical-severity gate at C2 — **VERIFIED**

The cited replaced rule reads exactly as claimed at
`skills/adversary/agents/adv-scorer.md:166-167`: *"Any Critical finding from adv-executor reports →
automatic REVISE regardless of score"* — confirmed by direct read, with no criticality branch
anywhere in the surrounding special-cases list (lines 165-168). ADR lines 439-440 state D-1
("C1–C2 none" for the panel) and D-2 ("Only panel-VERIFIED Criticals trigger automatic-REVISE")
as adopted decisions, and WI-3's acceptance criteria at line 847 confirms an unconditional
replacement: *"Lines 166–167 rule replaced with verified-only gating"* — no clause anywhere
preserves the old unconditional rule as a C1–C2 fallback. Since D-1 guarantees no panel ever runs
at C1–C2 (also drawn literally in Figure 1's Mermaid source at line 514: `CLAIMS -- "No, or
C1-C2" --> F`), no Critical claim raised at C2 can ever be "panel-VERIFIED," making the
auto-REVISE special case structurally unreachable at exactly the tier where S-002 is a REQUIRED
strategy (confirmed independently in `skills/adversary/agents/adv-selector.md`'s own C2 mapping:
`Required: {S-007, S-002, S-014}`). This is a genuine, materially significant regression — not a
hypothetical edge case, since C2 is Jerry's most common day-to-day tier — and it is not named
anywhere in the ADR's Negative Consequences (lines 794-809) or Risk register (lines 822-830); RSK-3
(line 826) addresses only misclassified C4-work-run-as-C2, not this inherent gap at correctly
classified C2 work. This undermines the ADR's own stated core purpose (restoring trust in the
Critical-severity signal) at a tier the ADR itself never examines.

**Verdict:** VERIFIED. File+line evidence directly confirms both halves of the claimed
contradiction (`ADR:439-440,447,514,847`; `skills/adversary/agents/adv-scorer.md:166-167`;
`skills/adversary/agents/adv-selector.md` C2 mapping), and the gap is genuinely absent from the
ADR's self-audited Risks/Consequences sections.

---

## DA-002-i3: WI-7's "generalization gate" only blocks a documentation pointer, not the mechanism's
actual deployment — **VERIFIED**

RSK-7's mitigation text (ADR line 830) frames WI-8's non-ADR-genre validation as a precondition
before "the protocol is treated as framework-general," and WI-7's acceptance criteria (line 851)
operationalizes that precondition narrowly: *"the SSOT pointer ... MUST NOT land until WI-8's
non-ADR-genre validation has run."* Direct inspection of the Work-Item Decomposition dependency
column confirms the counter-argument: WI-1 depends only on WI-2 (line 845), WI-3 depends only on
WI-1 (line 847), WI-4 depends only on WI-2 (line 848) — none of the four items that actually
implement the Verify-stage mechanism (the `adv-verifier` agent, the template, and the
`adv-scorer`/`adv-selector` edits) depend on WI-8. Conversely, WI-8 itself depends on
"WI-1..WI-5" (line 852), meaning the validation pass is scheduled to run only *after* the
mechanism has already shipped, not before. `skills/adversary/agents/adv-selector.md:89-107`
(read directly) confirms the AE-escalation checks that would drive Verify-stage activation are
genre-agnostic — keyed on path patterns (`docs/governance/`, `.context/rules/`, `decisions/`) and
content keywords, never on deliverable genre — and WI-4's acceptance criteria (line 848) states no
genre restriction. The combined effect is real: every C3/C4 tournament of any genre is already
routed through the Verify stage in production once WI-1–WI-5 ship, while only a
`quality-enforcement.md` cross-reference remains gated behind WI-8. This is materially significant
because RSK-7 is the ADR's own named response to its explicit n=2, "maximally correlated, not
merely small-n" evidence-base admission (ADR lines 306-308); if the stated safeguard is
definitionally scoped to a documentation pointer rather than to actual tournament behavior, the
risk register's own claimed mitigation for premature generalization does not achieve what it says
it achieves.

**Verdict:** VERIFIED. The dependency graph (`ADR:845,847,848,852`) and the genre-agnostic
`adv-selector.md:89-107` AE logic together confirm the mechanism activates framework-wide before
WI-8 validation runs, contradicting RSK-7's mitigation narrative as written.

---

## Summary

| ID | Verdict |
|----|---------|
| DA-001-i3 | VERIFIED |
| DA-002-i3 | VERIFIED |

Both Criticals are grounded in direct, checked citations (ADR line numbers and the two referenced
`skills/adversary/agents/*.md` files) that resolve exactly as the finder described. Neither is a
style nitpick or an edge case detached from the ADR's own claims — both attack a genuine gap
between what the ADR's Decision/Risk text asserts and what the Work-Item dependency structure and
cited agent files actually specify, at points the ADR's own self-audit (Negative Consequences,
Risks) does not enumerate.

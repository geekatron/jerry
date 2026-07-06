# Adversarial Refutation Panel — S-002 Devil's Advocate, Iteration 9 — MATERIALITY Lens

> Panel: independent refutation attempt against every Critical finding in
> `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-002-findings.md`.
> Lens: MATERIALITY — does the finding genuinely block the standard's PURPOSE
> (collision-free identity, honest promotion, adoptable convention)? Default to REFUTED
> when uncertain; cosmetic wording, style preferences, and negligible-probability-x-impact
> edge cases are REFUTED even if factually true.

## Scope

Only Critical-severity findings require a verdict per the task mandate. The S-002 report
contains 2 Critical findings (DA-001, DA-002) and 1 Major finding (DA-003, out of scope
for this panel — no verdict rendered).

---

## DA-001-20260706-i9 — "Flagship promoted-ADR precedent contains 13 currently-broken outbound citations" [Critical]

**Verdict: REFUTED**

**Reasoning:**

1. **Factually the broken links are real** (confirmed independently: `docs/design/ADR-output-path-resolution-001.md:380,481,529,593,602,632-635,642` all use `../../PROJ-030-bugs/work/BUG-006-*.md`; `Glob` confirms no `PROJ-030-bugs` directory exists at repo root and the real file lives at `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md`). This fact is not disputed.

2. **The finding targets a document outside the two deliverables under review.** `docs/design/ADR-output-path-resolution-001.md` is a third-party precedent cited by the ADR, not part of `ADR-PROJ031-004-adr-identifier-convention.md` or `adr-standards-rule-draft.md`. Its internal link hygiene is not a defect *in* the reviewed convention's ID grammar, location model, or promotion mechanic.

3. **This exact citation-staleness class is already disclosed as residual R-B, and R-B's own wording is not directionally scoped the way DA-001 claims.** `adr-standards-rule-draft.md:201` (Descoped note) states plainly: *"The citation-scan omission is an [INHERENT] residual R-B — the core detects only structural frontmatter links... it does not catch stale full-path citations (~28% of `.context/rules/` citations), stale GitHub-Issue references... Path-1's ID-stable move avoids the churn for the bare-ID majority (~72%); a manual `grep`/`gh issue list` sweep... is the fallback for the rest."* This text makes no inbound/outbound distinction — it discloses that **any** full-path/relative citation (regardless of direction) is not lint-covered. DA-001's claim that "R-B is scoped to inbound citations... This is the opposite direction" (Impact paragraph) is a strained reading not supported by R-B's actual text (`ADR-PROJ031-004-adr-identifier-convention.md:690` mirrors the same wording).

4. **The ADR's own Rationale already concedes the precedent is imperfect** — `ADR-PROJ031-004-adr-identifier-convention.md` Scheme-B steelman states the BUG-006 promotion tax "is not even fully repaid: stale citations to the extinct `ADR-PROJ007-001/002` IDs still sit in PROJ-007's own `ORCHESTRATION.yaml`..." The "corpus has already voted" claim is about validating the **decision** (subject-encoded identity survives promotion without ID rename), not asserting the precedent document is citation-perfect in every unrelated body paragraph. The convention never claims full-path citations to audit/task files are protected; it explicitly scopes its zero-churn claim to the **bare-ID majority (~72%)**.

5. **Materiality assessment:** the standard's purpose is collision-free identity, honest promotion, and an adoptable convention. A pre-existing, already-disclosed, already-conceded citation-hygiene defect in a *different* document's *unrelated* cross-references (to audit/task files, not to any ADR's identity) does not falsify or undermine the ID-continuity mechanism the convention actually decides. DA-001's own remedy options ("downgrade the wording") confirm this is an evidentiary-precision/wording matter, not a structural flaw. Per the materiality lens, this is REFUTED.

---

## DA-002-20260706-i9 — "This ADR's own self-promotion (M-9) is under-scoped: at least 5 relative links will break on execution" [Critical]

**Verdict: REFUTED**

**Reasoning:**

1. **The underlying facts are accurate and independently confirmed.** `ADR-PROJ031-004-adr-identifier-convention.md:85,213` and the Changelog v1.7 entry (`:780`) do cite `../FEEDBACK-LOG.md`; `:652` cites `../orchestration/adr-convention-20260702-001/subtraction-pass-notes.md`; `adr-standards-rule-draft.md:165` cites `../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md#...`. `FEEDBACK-LOG.md` exists only at `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` (confirmed via Glob; no `docs/FEEDBACK-LOG.md`). M-2's stated repair scope (`ADR-PROJ031-004-adr-identifier-convention.md:530`) does name only the reciprocal ADR↔rule-draft link pair, not these five additional links. The finder itself labels this an inference about a *future*, not-yet-executed event (P-022 compliant) — M-9 has not run; nothing is *currently* broken.

2. **This is a forward-looking, not-yet-materialized risk that the deliverable already generically covers via a standing, disclosed mitigation commitment.** R-B (`adr-standards-rule-draft.md:201`; `ADR-PROJ031-004-adr-identifier-convention.md:690`) commits to "a manual `grep`/`gh issue list` sweep... **owner: governance; cadence: at each Path-1/Path-2 promotion**" as the fallback for exactly this citation class. M-9 is explicitly a Path-2 promotion (per the Meta-Note); the disclosed cadence therefore already applies to it. The gap DA-002 identifies is that M-2's prose does not *individually enumerate* every affected link by line number ahead of time — a specificity/completeness gap in the write-up, not an absence of a committed mitigation mechanism.

3. **The affected links are not to any ADR's identifier** — they are incidental cross-references to a feedback log and an orchestration notes file (and, in the rule-draft, to a sibling ADR that never moves). None of this touches the convention's core mechanism under decision: collision-free, subject-encoded ADR identity and ID-stable (bare-ID) citation survival on promotion. The convention's zero-churn claim is scoped to the bare-ID majority (~72%, per the rule-draft's own descoped note); these are exactly the full-path-citation minority the convention already discloses as un-lint-covered and manually swept.

4. **Materiality assessment:** an incomplete migration-plan checklist for a future, not-yet-executed self-promotion step — one already covered by a standing, disclosed "sweep at every promotion" commitment — does not block the standard's purpose (collision-free identity, honest promotion, adoptable convention). It is an operational to-do item, correctable at M-9 execution time via the already-committed R-B sweep, not a structural or identity-collision defect. Per the materiality lens (default to REFUTED when the risk is hypothetical, low-impact, and already generically mitigated), this is REFUTED.

---

## Summary

| ID | Verdict |
|----|---------|
| DA-001-20260706-i9 | REFUTED |
| DA-002-20260706-i9 | REFUTED |

Both Critical findings, while factually grounded, describe (a) a citation-hygiene defect in a third-party precedent document outside the two reviewed deliverables, already covered by the broadly-worded R-B disclosure, and (b) a forward-looking, not-yet-materialized migration-plan specificity gap already subject to a standing, disclosed manual-sweep commitment (R-B, cadence: every Path-1/Path-2 promotion). Neither undermines the convention's actual decided mechanism (collision-resistant, subject-encoded ADR identity with bare-ID citation survival on promotion). Under the materiality lens, both are REFUTED.

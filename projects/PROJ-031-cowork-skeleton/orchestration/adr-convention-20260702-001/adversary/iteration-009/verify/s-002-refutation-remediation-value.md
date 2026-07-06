# S-002 Devil's Advocate — Refutation Panel (Remediation-Value Lens), Iteration 9

> Lens: REMEDIATION-VALUE. Would fixing this materially change real adoption outcomes, or is it churn? Findings whose fix is optional polish, already scheduled elsewhere, or would ADD machinery against the ratified subtraction doctrine are REFUTED. Default to REFUTED if uncertain.
> Scope: Critical findings only, per panel mandate (DA-003 is Major and out of scope for this panel's verified/refuted lists).
> P-003: no subagents used. P-020: read-only verification, no edits made to target deliverables. P-022: all claims below cite file+line; inferences are labeled.

---

## DA-001-20260706-i9 — "Flagship promoted-ADR precedent contains 13 currently-broken outbound citations" [CRITICAL]

**Verdict: REFUTED**

**Reasoning:**

1. **Factually the broken links exist** (verified independently: `docs/design/ADR-output-path-resolution-001.md:380,481,632-635,642` contain `../../PROJ-030-bugs/work/BUG-006-*.md` links; `Glob` confirms no `PROJ-030-bugs` directory exists outside `projects/PROJ-030-bugs/`, i.e., the links are missing a `projects/` segment). That part of the finding's evidence is accurate. But accuracy of the underlying fact is not the question this lens asks — remediation value is.

2. **The target document is out of mandate and the fix is either scope-creep or cosmetic wording.** DA-001 itself concedes the repair "(is) out of this ADR's edit mandate per P-020" — the only in-mandate remediation is downgrading the rhetorical "the corpus has already voted" / "PRECEDENT… works" language in the Rationale/Related-Decisions prose. That is a wording softening, not a functional or structural change to the convention being reviewed (`ADR-PROJ031-004` / `adr-standards-rule-draft.md`). Fixing the *other* document's 13 links would not change how this ADR's convention is adopted, applied, or lint-enforced.

3. **Already dispositioned as this exact class of out-of-mandate residual.** M-10 (`ADR-PROJ031-004-adr-identifier-convention.md:540`) is the pre-existing, named bucket for precisely this failure class: "Repair the known live stale/dangling citations to renamed ADRs — the exact failure class this convention exists to prevent, all outside this ADR's edit mandate (P-020: owned follow-up, not a silent cross-project edit here)," already itemizing the `ci.yml` dangling link and the `ADR-PROJ007-001/002` stale citations (an iteration-7 DA-001 finding, per `subtraction-pass-notes.md:180-198` and the ADR Changelog v1.9 row, `:782`). M-10 is explicitly marked "Gating? No." The new DA-001 (iteration 9) asks to append one more bullet to an already-established, already-disclosed, already-non-gating bucket — this is not a new gap, it is an instance of a pattern the package has already named, owned, and declined to gate on three times over.

4. **The underlying failure class is already disclosed as an INHERENT residual (R-B), independent of direction.** R-B (`adr-standards-rule-draft.md:201`; ADR Enforcement §Descoped) states plainly: "the core detects only structural frontmatter links… \[full-path citations\] is an [INHERENT] residual… a manual grep/gh sweep is the fallback (owner: governance; cadence: at each Path-1/Path-2 promotion)." DA-001's claim that R-B covers only "inbound" citations and not "outbound" ones is a distinction drawn by the finder, not present in R-B's own text — R-B is framed around the *lint's structural blind spot* (it only checks frontmatter relationship fields), not around citation direction. The newly-found break is squarely inside that already-disclosed blind spot.

5. **Root-cause mismatch weakens the "falsifies the honesty claim" framing.** The broken links are missing a `projects/` path segment relative to the document's current location — a relative-path arithmetic defect, not an instance of *ID-string churn* (the specific failure Scheme B's promotion mechanic addresses). Scheme B's "zero-churn" claim is about citations to an ADR's *bare identifier* surviving a rename-free `git mv`; it says nothing about whether every relative link to a co-located, non-promoted sibling file (an audit doc that stays behind) resolves. Conflating "this document has an unrelated broken link" with "the promotion-is-honest claim is falsified" overstates the connection between the two document classes.

6. **Net assessment against the lens:** the fix is either (a) additive scope-creep — editing a second, unrelated ADR under a Migration Plan row that has already three times declined to gate on this class — or (b) cosmetic prose softening of a rhetorical flourish ("the corpus has already voted") that does not change the mechanics, enforcement, or lint behavior of the convention. Neither materially changes real adoption outcomes. REFUTED.

---

## DA-002-20260706-i9 — "This ADR's own self-promotion (M-9) is under-scoped: at least 5 relative links will break on execution" [CRITICAL]

**Verdict: VERIFIED**

**Reasoning:**

1. **Evidence independently confirmed.** All five cited links exist exactly as described: `ADR-PROJ031-004-adr-identifier-convention.md:85` and `:213` and `:780` each contain `../FEEDBACK-LOG.md` (verified — lines 85, 213, and the v1.7 Changelog row at 780 each resolve `[FEEDBACK-LOG.md → FU.0](../FEEDBACK-LOG.md)`); `:652` contains `[subtraction-pass notes](../orchestration/adr-convention-20260702-001/subtraction-pass-notes.md)`; `adr-standards-rule-draft.md:165` contains `../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md#claim-status-convention-p-022--foundational`. M-2's stated repair scope, quoted verbatim at `ADR-PROJ031-004-adr-identifier-convention.md:530`, textually names only the reciprocal ADR-004 ↔ rule-draft link pair — it does not mention `FEEDBACK-LOG.md`, `subtraction-pass-notes.md`, or `ADR-PROJ031-003`.

2. **In-mandate, not scope-creep.** Unlike DA-001, this finding concerns the *same two deliverables under review* and their *own* stated Migration Plan (M-2/M-9) — squarely within this ADR's edit mandate. Fixing it means extending an existing, already-itemized migration-plan checklist entry (M-2/M-9's cross-link repair scope), not adding a new mechanism, rule, lint, or gate. This is consistent with, not contrary to, the subtraction doctrine (no new machinery — just completing an existing item's enumeration).

3. **Materially affects real adoption outcomes.** M-9 is explicitly framed by the ADR itself as the pedagogically central "worked example of its own Path-2 promotion" — the artifact "future authors" are meant to model (Meta-Note, `ADR-PROJ031-004-adr-identifier-convention.md:539` intent language). If this self-promotion executes with 4 broken links in the ADR and a 5th permanently orphaned in the rule draft (the `ADR-PROJ031-003` link, which is never captured by the ADR-004-only reciprocal framing since ADR-PROJ031-003 never moves), the flagship self-compliance demonstration will visibly exhibit the exact citation-continuity failure the convention exists to prevent, at the moment of maximum scrutiny. That is a direct, not hypothetical, credibility and functionality cost to real-world adoption — not cosmetic polish.

4. **Not already disclosed or scheduled elsewhere.** R-B addresses the *lint's* generic inability to scan free-text citations; it is not a statement that M-2/M-9's specific, human-authored repair checklist is complete. No other Migration Plan row (M-2, M-9, or M-10) names the FEEDBACK-LOG.md, subtraction-pass-notes.md, or ADR-PROJ031-003 links. This is a genuine, previously-undetected completeness gap in a concrete, near-term, in-mandate execution step — not an instance of an already-accepted residual class.

5. **Net assessment against the lens:** the fix is low-cost (extend one existing migration-plan row's already-itemized list; the migration-plan bullet already performs link repair as its stated job), in-mandate, and bears directly on whether the ADR's own most-visible self-application will function correctly — a real, non-churn adoption outcome. VERIFIED.

---

## Summary

| ID | Severity | Verdict | Basis |
|----|----------|---------|-------|
| DA-001-20260706-i9 | Critical | **REFUTED** | Out-of-mandate (targets a different document); already covered by the pre-existing, thrice-used, non-gating M-10 bucket and the disclosed [INHERENT] R-B residual; root-cause mismatch with the "ID-churn" claim it purports to falsify; fix is either scope-creep or cosmetic wording softening. |
| DA-002-20260706-i9 | Critical | **VERIFIED** | In-mandate (the reviewed ADR's own Migration Plan), evidence independently confirmed at all five cited lines, fix is a low-cost extension of an existing checklist item (no new machinery), and directly bears on whether the convention's flagship self-promotion actually works — a material real-adoption outcome. |

**Note on DA-003 (Major):** Not in scope for this panel's Critical-only mandate; no verdict rendered.

# Refutation Panel — S-002 Devil's Advocate, Iteration 10 — Remediation-Value Lens

> **Panelist mandate:** Attempt to refute every Critical finding in `adversary/iteration-010/s-002-findings.md`. Default to REFUTED if uncertain. Lens: would fixing this materially change real adoption outcomes, or is it churn / already-scheduled / additive-against-doctrine?
> **Blind protocol:** Only the target S-002 report, the two current deliverables, and `subtraction-pass-notes.md` were read. No other refuters' or panels' outputs were read.
> **Scope:** Critical findings only — 002-001 and 002-002. (002-003 is Major, out of this panel's mandate.)

---

## Verdict: 002-001 — L-4 ID↔location undefined/broken for EPIC002-001/002 — REFUTED

**Claim recap:** The Location Model (`ADR-PROJ031-004-adr-identifier-convention.md:384-393`, `adr-standards-rule-draft.md:77-86`) allegedly has no row matching `ADR-EPIC002-001-strategy-selection.md`/`ADR-EPIC002-002-enforcement-architecture.md`, which sit in `projects/PROJ-001-oss-release/decisions/` (an EPIC-prefixed dialect ID in a plain project `decisions/` dir, not `work/.../{ENTITY}/`).

**Refutation reasoning:**

1. **The practical disposition of these exact two files is already explicit and unambiguous elsewhere in the same ADR**, independent of the Location Model table's row taxonomy. The Migration Plan (`ADR-PROJ031-004-adr-identifier-convention.md:514`) states plainly: *"Project-scoped families (`PROJ010`×6, `PROJ022`×2, `PROJ031`×3, **`EPIC002`×2**, `STORY015`×1, `150`×1) | Legacy project/entity dialect, collision-resistant... | **Grandfather in place.** Valid dialect. Re-slug only if/when promoted. | **Zero**"*. The Frozen-and-Grandfathered section (`adr-standards-rule-draft.md:94`) likewise groups `EPIC002`×2 into "the 16-file whole dialect corpus... remain valid in place." A reader today gets a clear, actionable answer for these named files without needing the Location Model table to enumerate every historical sub-pattern.
2. **The underlying "L-4 untested against the real corpus" concern is already captured — at Major severity, by 002-003, in this same report.** 002-003 explicitly recommends extending the grandfather regression test to L-3/L-4/L-7 or disclosing the untested status. Fixing 002-003 substantially subsumes 002-001's practical remediation-value: once L-4 is honestly labeled "reasoned-about, not demonstrated" (which the document already does implicitly via the pervasive Claim-Status: DESIGNED, NOT BUILT framing at `ADR-PROJ031-004-adr-identifier-convention.md:659`), whether a not-yet-built lint would pass or fail two specific files is a future implementation detail, not a present defect blocking adoption.
3. **L-4 has zero operative effect today** (`scripts/lint_adr_convention.py` does not exist, Glob-verified per the document's own Claim-Status note, `ADR-PROJ031-004-adr-identifier-convention.md:659`) — nothing currently misclassifies, blocks, or misleads an author about these files. The pre-mortem's own FM-5 (`ADR-PROJ031-004-adr-identifier-convention.md:501`) rates "the lint never ships" as "the single best-evidenced risk," making the finding's worst-case scenario (M-11 triggers a CI break) both conditional and, by the document's own risk assessment, unlikely to occur soon.
4. Per remediation-value criteria, this is table-completeness polish on an already-answered practical question and a duplicate of an already-disclosed (Major) testing gap — not a fix that would materially change real adoption behavior today.

---

## Verdict: 002-002 — Rule draft's R-N residual citations unresolvable in every distributed build — REFUTED

**Claim recap:** The rule draft cites `R-N` residual IDs (R-9, R-10, R-11, R-13, R-14, R-15, R-16, R-17, R-B, and the collective R-1…R-17/R-A/R-B/R-C in the References row, `adr-standards-rule-draft.md:234`) that resolve only in the parent ADR's Risks register, and the parent ADR is permanently absent from every CoWork/plugin distribution build (`projects/` unconditionally stripped per `phase3-skeleton-generation-design.md:159`, independently verified in this pass).

**Refutation reasoning:**

1. **The actionable, adoptable guidance in the rule draft is self-contained and does not depend on resolving any `R-N` tag.** The normative content a downstream author actually needs — MEDIUM Standards ADR-M-001…M-013 (`adr-standards-rule-draft.md:44-58`), ID Scheme (`:62-71`), Canonical Location Model (`:75-88`), Promotion Process, Supersede-and-Amend, Status Vocabulary — carries zero `R-N` citations in its normative rule statements. Where `R-N` tags do appear, they are consistently attached to inline substantive prose stated in the same sentence (e.g., `adr-standards-rule-draft.md:175`: *"does not structurally reject a lowercase slug that case-folds to a dialect prefix... a disclosed residual (R-9), not a lint stop"* — the guidance ["SHOULD NOT" avoid such slugs] is fully actionable without ever resolving what "R-9" formally denotes elsewhere).
2. **The `R-N` citations concentrate almost entirely in the L5 CI Lint Specification section** (`adr-standards-rule-draft.md:163-208`), which documents a tool that is itself Claim-Status DESIGNED-NOT-BUILT and, per the ADR's own Enforcement Scope table (`ADR-PROJ031-004-adr-identifier-convention.md:674-680`), does not meaningfully reach the plugin distribution anyway (`.github/` CI is stripped; the CLI-fallback path is explicitly disclosed as adopter-dependent with "no committed timeline"). The audience most likely to need full `R-N` resolution is the lint's *implementer* (M-6), who works inside the `geekatron/jerry` source repo where the parent ADR is present and resolvable — not the ordinary downstream guidance-following author.
3. **This is an incremental extension of an already-established, already-verified disclosure pattern**, not a newly-discovered category of gap: 012-001 (per `subtraction-pass-notes.md` Iteration-9 Remediation table) already added the caveat that, pre-M-2, "a distributed plugin install carries no trace of this convention at all." The permanent post-M-2 unresolvability of `R-N` shorthand is the same honesty-caveat pattern applied one step further, not a materially different risk to adoption outcomes — the convention's guidance remains followable either way.
4. Per remediation-value criteria: fixing this is a professional-polish/traceability nicety for an edge case (a reader who wants full residual detail behind SHOULD-NOT footnotes), not a change that would materially affect whether a downstream author can correctly adopt the naming/location/promotion convention.

---

## Summary

| ID | Severity | Verdict | Basis |
|----|----------|---------|-------|
| 002-001 | Critical | **REFUTED** | Practical disposition (grandfather, zero action) already explicit elsewhere in the ADR (Migration Plan, Frozen/Grandfathered section); underlying testing gap already captured as Major (002-003) in the same report; L-4 has zero operative effect today (lint not built). |
| 002-002 | Critical | **REFUTED** | Core adoptable guidance is self-contained without needing `R-N` resolution; `R-N` citations concentrate in the not-yet-built/CI-stripped lint-spec section relevant mainly to the source-repo implementer; this extends an already-established disclosure pattern (012-001) rather than exposing a materially new adoption risk. |

*No subagents spawned (P-003). No files edited outside mandate (P-020). All claims cite file+line; interpretive judgments on ambiguous table semantics are labeled as such (P-022).*

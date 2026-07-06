# S-012 (FMEA) Iteration-9 Critical Findings — Factual-Accuracy Refutation Panel

> **Lens:** Factual accuracy (does the cited defect actually exist at the cited location in the CURRENT deliverables?)
> **Target report:** `orchestration/adr-convention-20260702-001/adversary/iteration-009/s-012-findings.md`
> **Scope:** 3 Critical findings only (012-001, 012-002, 012-003). Majors/Minors (012-004, 012-005) out of scope per mandate.
> **Method:** Re-read every cited line in `ADR-PROJ031-004-adr-identifier-convention.md`, `design/adr-standards-rule-draft.md`, `design/phase3-skeleton-generation-design.md`, and cross-checked against `subtraction-pass-notes.md`'s R-1..R-17 register for restatement.

---

## 012-001: Plugin-Distribution "Zero-Tooling Guidance" Overclaim — **VERIFIED**

**Citations checked:**
- `ADR-PROJ031-004:675` — exact quote confirmed: "**Downstream/plugin disclosure (PM-002/PM-006, P-022).** ... **What carries value downstream on day one is the *guidance*, which needs no tooling.** Disclosed so the enforcement claim is not overstated for the exact CoWork target PROJ-031 serves." The paragraph's own heading ("Downstream/plugin disclosure") confirms this sentence is explicitly a claim about the plugin/downstream audience, not the source-repo reader.
- `ADR-PROJ031-004:663` — exact quote confirmed re: `decisions/` corpus absence for linting purposes only.
- `phase3-skeleton-generation-design.md:159-160` — confirmed: `git rm -r projects/ tests/ skills/.graveyard .github` is the VALIDATED unconditional strip-set (line 159), with `projects/ ~4,600 work artifacts` listed as a stripped item (line 160). `.context/rules/` is NOT in either the unconditional or the "RECOMMENDED additional strips" list (lines 168-173 checked; only `docs/`, `scripts/`, `mkdocs.yml`, etc. appear there) — so `.context/rules/adr-standards.md` would in fact survive a skeleton build once authored there, confirming the finding's premise that M-2 is the load-bearing gate.
- `ADR-PROJ031-004:530` (M-2 row) — confirmed `TBD-Task`, no committed date, owner `ps-architect / governance`.
- `ADR-PROJ031-004:525` — confirmed Claim-Status disclosure that zero worktracker Tasks/GH Issues exist for any Migration-Plan row.

**Restatement check:** FM-5 (`:496`) is the closest prior disclosure — its containment clause ("the guidance's zero-tooling value... bounds the damage even if the lint never ships") is about a *reader of this ADR* (i.e., a source-repo reader), and R-5/former-R-1 (`:464`, "the convention... delivers value as MEDIUM-tier guidance with zero tooling") is likewise unqualified by audience. Neither residual entry, nor any text in the Enforcement Scope section (lines 658-693 read in full), draws the specific conclusion that the *guidance prose itself* (not just the CI lint) is physically absent from a skeleton build cut before M-2 executes. This is a distinct, non-duplicative angle on an already-disclosed pattern of "designed-not-built" residuals, not a re-derivation of R-1/R-5/FM-5.

**Verdict: VERIFIED.** The overclaim exists as described at the cited line, the supporting strip-set evidence is accurate, and the finding is not a restatement of a disclosed residual.

---

## 012-002: No General Schema Field or Lint Check for ADR↔Companion-Rule-File Relationship — **VERIFIED**

**Citations checked:**
- `ADR-PROJ031-004:530` (M-2) and `:539` (M-9) — confirmed both describe a manual, one-off "Cross-link repair (DA-002)" specific to this ADR/rule-draft pair; language matches the finding's quote closely.
- Frontmatter Schema block, ADR mirror `:350-369` and `adr-standards-rule-draft.md:100-117` — confirmed both blocks list the same field set (`id, type, status, scope, origin_project, origin_entity, created, supersedes, superseded_by, amends, amended_by, promoted_from, promoted_to, canonical_id`) and **no field references a companion rule file**. Minor count discrepancy noted: the finding labels this list "13 fields" but the enumerated list itself contains 14 items (off-by-one in the finder's own arithmetic) — a cosmetic inaccuracy that does not affect the substantive claim (no companion-rule-file field exists).
- L-7 spec (`adr-standards-rule-draft.md:179`; ADR mirror `:685`) — confirmed it checks only `superseded_by`/`promoted_to`/`promoted_from`; no companion-file relationship type is in scope.
- General-pattern corroboration: the finding cites "`:732-734`" as the source for the `ADR-agent-design-001`/`ADR-routing-triggers-001`/`ADR-EPIC002-001/002` companion-rule-file examples. On re-read, `ADR-PROJ031-004:732-734` (Related Decisions table) names only `ADR-agent-design-001` and `ADR-output-path-resolution-001` as EXEMPLAR/PRECEDENT entries — it does **not** name `ADR-routing-triggers-001` or the EPIC002 pair. This is an imprecise citation (overstates what that specific line range shows), but the underlying factual claim about the general ADR+companion-rule-file pattern is independently true and verifiable elsewhere in the repo (the `.context/rules/agent-development-standards.md` and `agent-routing-standards.md` and `quality-enforcement.md` files, all loaded in this session's system context, do cite `ADR-agent-design-001`, `ADR-routing-triggers-001`, and `ADR-EPIC002-001/002` respectively as their source ADRs). The citation imprecision is in the auxiliary corroboration, not in the core defect location (the Frontmatter Schema block and L-7 spec, which are accurately quoted).

**Restatement check:** Not present in R-1..R-17. R-8 (YAML-vs-blockquote drift) and R-15 (frontmatter `id:` dedup) are adjacent but address different mechanisms (dual-parser sync and `id:`-uniqueness), not a companion-file cross-link schema gap. This is a genuinely new gap.

**Verdict: VERIFIED.** The core defect (no schema field/lint coverage for the general ADR↔companion-rule-file relationship) is factually accurate at the cited locations. The auxiliary citation `:732-734` overstates what that specific range shows, but this does not invalidate the primary, independently-confirmable claim.

---

## 012-003: Grandfather-Baseline Temporal Anchor Creates Unbounded Post-Ratification Amnesty Window — **VERIFIED**

**Citations checked:**
- `ADR-PROJ031-004:688` — exact quote confirmed: "grandfathering is resolved against a **static adoption-time baseline** — the enumerable set of ADR files that exist **when the lint first ships**... captured **once** as a data list in M-6."
- `ADR-PROJ031-004:223` (D-4) — exact quote confirmed: "Existing scope-prefixed and legacy ADRs are grandfathered... No big-bang renumber (c-003). The **15 pre-existing** dialect ADRs remain valid legacy-dialect instances **in place**."
- `adr-standards-rule-draft.md:48` (ADR-M-003) — exact quote confirmed: dialect remains SOFT `MAY`-permitted for new ADRs "with positive certainty," no expiry date stated.
- `ADR-PROJ031-004:536` (M-6) — confirmed `TBD-Task + GH Issue`, no committed timeline; FM-5 (`:496`) confirmed rated "nothing lands" as the single best-evidenced risk in the package.

**Restatement check:** Searched the Risks register (R-1 through R-17, full text read) and the D-4/Enforcement-Design sections for any existing disclosure of a growing "amnesty window" between ratification and lint-ship (as distinct from R-5/former-R-1's "lint may never ship at all" framing). No such disclosure exists — R-5 addresses total non-delivery of the lint; D-4 states the grandfather baseline in terms of the pre-existing 15-file corpus but does not address ADRs *minted after ratification and before lint-ship*. The specific mechanism identified (undated M-6 + indefinite SOFT-MAY dialect permission = growing, undated exemption population) is a distinct temporal-scope gap not covered by any of R-1..R-17 or the Pre-Mortem/FM rows.

**Verdict: VERIFIED.** The temporal-anchor inconsistency exists as described at the cited locations and is not a restatement of a disclosed residual.

---

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| 012-001 | VERIFIED | Overclaim at `:675` confirmed exact; strip-set evidence confirmed; distinct from FM-5/R-5 (different reader-audience scope) |
| 012-002 | VERIFIED | Missing schema field/lint coverage confirmed at Frontmatter Schema + L-7 spec; one auxiliary citation (`:732-734`) is imprecise but non-central |
| 012-003 | VERIFIED | Static lint-ship-time baseline vs. indefinite SOFT-MAY dialect permission confirmed at `:688`/`:223`/rule-draft `:48`; not a restatement of R-5 or D-4 |

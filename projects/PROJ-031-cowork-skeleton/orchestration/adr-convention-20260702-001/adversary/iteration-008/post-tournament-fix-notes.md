# Post-Tournament Fix Notes — Iteration-8 (7 new Criticals)

> Owner: ps-architect (creator/owner of the ADR-convention package). Closes the 7 NEW Critical findings from tournament iteration-008.
> Doctrine (binding): SUBTRACTION — close by deleting/narrowing the exposing claim or disclosing a residual; never add lint rules or process machinery. The 5-rule core (L-1/L-2/L-3/L-4/L-7) stays exactly 5. Each of the 7 is text/disclosure-fixable with NO new machinery (the reviewers themselves assessed all 7 that way).
> P-002 incremental. P-003 no subagents. P-022 no fabrication; no employer-internal references; no absolute home-directory paths in the deliverables.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Filesystem Verification](#filesystem-verification-p-022) | Ground-truth counts and frontmatter facts, measured this pass |
| [The 7 Criticals — Disposition](#the-7-criticals--disposition) | Each finding → CLOSED-BY-EDIT / RESIDUAL-DISCLOSED + anchor |
| [New Residuals Registered](#new-residuals-registered) | R-14…R-17 |
| [Rule-Draft Token Count (Honest)](#rule-draft-token-count-honest) | Re-measured before/after |
| [Files Edited](#files-edited) | Change surface |

---

## Filesystem Verification (P-022)

Measured 2026-07-06 against the live repo (`find` over `projects/` + `docs/design/`, frozen dirs excluded):

- **Whole dialect corpus (all locations, non-frozen): 16** — `EPIC002`×2, `PROJ010`×6, `PROJ022`×2, `PROJ031`×4 (incl. this ADR), `STORY015`×1 (entity-embedded, out-of-scan), `150`×1.
- **Dialect reachable by the scan path** (`projects/*/decisions/` + `docs/design/`): **15** = 16 − the 1 out-of-scan `ADR-STORY015-001`. This subset **includes** this ADR (`ADR-PROJ031-004`).
- **Canonical framework ADRs** (`docs/design/`): **3** (`ADR-agent-design-001`, `ADR-output-path-resolution-001`, `ADR-routing-triggers-001`).
- **Grandfather regression corpus (files that pass L-1): 18** = 15 dialect-reachable + 3 canonical.
- Numerical coincidence disclosed: "15 pre-existing" (dialect corpus before this ADR: excl. this ADR, **incl.** STORY015) and "15 reachable" (**incl.** this ADR, excl. STORY015) are equal by coincidence, counting different sets.

Frontmatter facts:
- `ADR-PROJ031-002-ci-token-push-strategy.md`: **blockquote-only header, no YAML `---` block** (verified). Supersession recorded as `> **Superseded By:** [ADR-PROJ031-003](...)`.
- `ADR-PROJ031-003-credential-protection-supply-chain.md`: **blockquote-only header, no YAML `---` block** (verified). → L-7 (YAML parser) has zero real targets in the PROJ031 supersession chain.

---

## The 7 Criticals — Disposition

Legend: CLOSED-BY-EDIT | RESIDUAL-DISCLOSED. All text/disclosure only; zero new machinery; core stays 5 rules.

| # | ID | Strategy | Disposition | How / anchor |
|---|----|----------|-------------|--------------|
| 1 | DA-001 | S-002 | **CLOSED-BY-EDIT** | Topology-scope of the lint's collision-safety stated at the **Decision (D-5)** headline, not only in R-10 downstream; repository-based-topology adopters get guidance + pre-flight one-liner only, not lint coverage. Underlying gap is the already-registered R-10. ADR §Decision D-5. |
| 2 | DA-002 | S-002 | **RESIDUAL-DISCLOSED (R-14)** | Frozen-dir new-file collision (L-9 deleted; L-2 exempts + L-3 excludes frozen dirs) elevated from a subordinate clause to a named Risk row with R-6…R-13 rigor. No 6th rule. ADR §Risks R-14; rule-draft §Frozen-and-Grandfathered. |
| 3 | RT-001 | S-001 | **RESIDUAL-DISCLOSED (R-15)** | Frontmatter `id:` uniqueness/filename-agreement not lint-checked → disclosed residual + guidance clause added to ADR-M-001 (`id:` SHOULD equal filename, RT-002). No widening of the 5 rules. ADR §Risks R-15; rule-draft ADR-M-001. |
| 4 | IN-001 | S-013 | **CLOSED-BY-EDIT** | Grandfather clause added to **L-1's spec text**: "pre-adoption grandfathered" operationalized against a static adoption-time baseline (the enumerable 18 + out-of-scan STORY015), so a later-edited legacy file (`ADR-150-001`) is exempt, not treated as new-bare. Spec wording, not a rule. ADR §Enforcement Design (grandfather regression para); rule-draft §L5 spec. |
| 5 | FM-001-i8 | S-012 | **CLOSED-BY-EDIT** | 16-vs-15 contradiction fixed: single authoritative reconciliation stated once at **D-4** (16 whole corpus / 15 reachable / 3 canonical / 18 regression), verified 2026-07-06; the false "16 matches the regression test" claim dropped; M-6 row, Enforcement Design, rule-draft L5 spec + line-94 reference it. ADR §Decision D-4. |
| 6 | FM-002-i8 | S-012 | **RESIDUAL-DISCLOSED (R-16)** | L-7's forward-looking rationale stated honestly: the PROJ031 supersession chain is blockquote-only (no YAML), so L-7 has zero real targets today; disclosed as R-16 + L-7 spec note. ADR §Risks R-16 + L-7 row; rule-draft L-7 row. |
| 7 | FM-003-i8 | S-012 | **RESIDUAL-DISCLOSED (R-17)** | Cross-branch concurrent-supersession race added to the disclosed-residual register, mirroring R-6's structure. ADR §Risks R-17 + Amend-vs-Supersede note; rule-draft §Supersede-and-Amend. |

**Tally: CLOSED-BY-EDIT = 3 (DA-001, IN-001, FM-001-i8); RESIDUAL-DISCLOSED = 4 (DA-002/R-14, RT-001/R-15, FM-002-i8/R-16, FM-003-i8/R-17).**

---

## New Residuals Registered

| ID | Residual | Framing |
|----|----------|---------|
| R-14 | New-file collision inside a frozen dir (L-9 deleted; L-2 exempts + L-3 excludes frozen dirs) | [DELETION-INHERENT] — persists post-M-6; frozen = SHOULD-NOT-extend policy + manual pre-flight only |
| R-15 | Frontmatter `id:` never deduplicated/filename-checked by the 5 rules | [DESIGN-INHERENT] — guidance closed at ADR-M-001; lint gap disclosed, widening is a future MAY |
| R-16 | L-7 has zero real YAML targets in the PROJ031 blockquote-only supersession chain | [DISCLOSED] — L-7 is forward-looking; optional M-11 retrofit is non-gating |
| R-17 | Cross-branch concurrent-supersession race (supersession analog of R-6) | [INHERENT] — PR-review + single-valued `superseded_by` by design; no supersession-graph checker added |

---

## Rule-Draft Token Count (Honest)

Measured 2026-07-06 with `wc` on the live file.

| Point | Lines (`wc -l`) | Words (`wc -w`) | Tokens (words × 1.35) |
|-------|-----------------|-----------------|-----------------------|
| Before this pass | 242 | 3193 | ~4310 |
| After this pass | **247** | **3739** | **~5047** |

Honest note: the ~740-token / 5-line growth is entirely honest disclosure (the L-1 grandfather-baseline clause, L-7 forward-looking scope, ADR-M-001 `id:` clause, R-14…R-17 references, and the v1.10 changelog row). Still within the ~250–350-line guidance (247 < 250); above the literal ~2.5k-token soft target, a divergence disclosed in the rule draft's self-measurement note rather than cut into an incomplete rule. The self-measurement figure is self-referential (the note measures a file that contains the note), so ±a-few-words at the ~0.1% level is inherent and disclosed. No lint rule, ledger, gate, or matrix added — the 5-rule core (L-1/L-2/L-3/L-4/L-7) is unchanged.

---

## Files Edited

- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` — D-4 count reconciliation, D-5 topology-scope note, L-1 grandfather clause, L-7 forward-looking note, R-14…R-17, Amend-vs-Supersede FM-003-i8 note, changelog.
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` — ADR-M-001 `id:` clause, Frozen-and-Grandfathered R-14 ref, L-1 grandfather clause, L-3/L-7 reconciliation refs, L-7 forward-looking note, Supersede-and-Amend R-17 note, self-measurement note, changelog.
- `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/subtraction-pass-notes.md` — iteration-8 disposition table appended.
- This file.

*No subagents (P-003). No files edited outside mandate (P-020). All counts filesystem-verified (P-022).*

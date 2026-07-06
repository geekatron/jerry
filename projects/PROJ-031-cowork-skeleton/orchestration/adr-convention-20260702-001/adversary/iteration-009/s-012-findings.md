# S-012 FMEA Findings — Iteration 9 (VERIFIED-CRITICALS Protocol)

> **Status:** COMPLETE
> **Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
> **Criticality:** C4 | **Gate:** 0.95
> **Deliverables:** `ADR-PROJ031-004-adr-identifier-convention.md` (v1.10) + `design/adr-standards-rule-draft.md`
> **Blind protocol:** iteration-009/iteration-010 sibling strategy outputs NOT read. Prior iterations (001-008) and `subtraction-pass-notes.md` (disposition record, R-1..R-17/R-A/R-B/R-C register) WERE read for de-duplication.
> **Scope directive:** Report ONLY lifecycle failure modes NOT already covered by the disclosed residual register. Re-deriving a disclosed residual is NOT a finding. Disclosed-residual MEDIUM-tier posture is VALID; overclaimed coverage is Critical.

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#fmea-report-adr-proj031-004--adr-standards-rule-draft-v110) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Prior Residual Register (context)](#prior-residual-register-context-only-not-findings) | R-1..R-17 read for de-duplication |
| [Findings Table](#findings-table) | All new lifecycle failure modes, RPN-ranked |
| [Finding Details](#finding-details) | Critical/Major expanded detail |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Totals |

---

## FMEA Report: ADR-PROJ031-004 + adr-standards-rule-draft.md (v1.10)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-012 agent), iteration 9 of a 9-round tournament (8 prior rounds already closed ~40 Critical/Major findings across S-001/002/003/004/007/010/011/012/013/014)
**H-16 Compliance:** S-003 Steelman is embedded (each of Options A–F leads with its steelman case per the glossary note at `ADR-PROJ031-004:65-67`); confirmed present in the reviewed package.
**Elements Analyzed:** 12 (Decision D-1..D-5; Promotion Process Paths 0/1/2; Frontmatter Schema; Enforcement/Lint L-1,L-2,L-3,L-4,L-7; Migration Plan M-1..M-14; Risks register R-1..R-17; Pre-Mortem FM-1..FM-5; Status Vocabulary; Amend-vs-Supersede; Companion-file cross-linkage; Canonical Location Model incl. topology branch)
**Failure Modes Identified:** 5 new (post-de-duplication against R-1..R-17/R-A/R-B/R-C/PM-009/FM-1..FM-5)
**Total RPN:** 1,253 (sum of 5 findings below)

---

## Summary

This package has already absorbed 8 adversarial tournament rounds and discloses an unusually thorough residual register (R-1 through R-17, plus R-A/R-B/R-C and PM-009) covering collision races, out-of-scan locations, frontmatter drift, and self-approval risk. Against that baseline, this iteration-9 FMEA pass identifies **5 genuinely new lifecycle failure modes**, none of which re-derive an already-disclosed residual. The highest-RPN finding (**012-001**, RPN 512, Critical) is the most consequential: the package's own "the guidance delivers zero-tooling value on day one" claim (`ADR-PROJ031-004:675`) is not true today for the convention's stated primary distribution audience (downstream CoWork/plugin installs) — both deliverables live under `projects/`, which is unconditionally stripped from every skeleton build (`phase3-skeleton-generation-design.md:159-160`), and the guidance's actual destination (`.context/rules/adr-standards.md`, via Migration-Plan M-2) has no committed timeline (`ADR-PROJ031-004:530`, `TBD-Task`). This is an overclaim, not an omission — the affirmative sentence at line 675 asserts a benefit that does not yet exist for that audience. A second Critical (**012-002**, RPN 245) identifies that the ADR↔companion-rule-file relationship (the pattern this very ADR + its own rule draft exemplify, and the pattern already used by 3 of 3 canonical framework ADRs) has no frontmatter field or lint check; only this one instance received a manual, one-off cross-link repair (M-2/M-9). A third Critical (**012-003**, RPN 252) identifies that the grandfather-baseline's temporal anchor ("when the lint ships," an unscheduled date) is decoupled from the convention's own stated intent ("existing... legacy... grandfathered," i.e., pre-ratification), creating an expanding amnesty window for post-ratification non-compliant dialect ADRs. Two Major/Minor findings round out the report (cross-repository slug-namespace exposure; project-ID-renumbering cascade). **Recommendation: REVISE** — none of these findings require restoring deleted machinery (consistent with the package's own subtraction doctrine); each is closable by a disclosure-only edit or a narrowly-scoped text correction.

---

## Prior Residual Register (context only, not findings)

Read and excluded from findings below: R-1 (lint may never be built), R-6 (cross-branch same-slug NNN race), R-7 (slug reuse for unrelated subject), R-9 (case-fold look-alike), R-10 (entity-embedded/repository-topology out-of-scan), R-11 (L-7 3-of-6 field asymmetry), R-12 (solo-maintainer self-approval of MEDIUM override), R-13 (L-3 title-slug-tail false negative), R-14 (frozen-dir new-file collision, not lint-enforced), R-15 (frontmatter `id:` uniqueness/filename-agreement not lint-checked), R-16 (L-7 forward-looking, zero real YAML targets today), R-17 (concurrent cross-branch supersession race), R-A (producer agent non-compliance until Fix-3), R-B (free-text citation staleness incl. GitHub Issues not lint-covered), R-C (in-place amendment mutation of scope/origin not lint-detected), PM-009 (forward promotion rate rests on n=3, monitored), Pre-Mortem FM-1..FM-5 (lint-never-built, slug ambiguity, dialect abuse, taxonomy sprawl, compound "nothing lands").

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| 012-001 | Enforcement Scope §Downstream/plugin disclosure | "Guidance delivers zero-tooling value on day one" overclaim — both deliverables live under `projects/`, unconditionally stripped from every skeleton build; guidance's real destination does not exist (M-2 untracked, no timeline) | 8 | 8 | 8 | **512** | Critical | Add a plain disclosure at the Enforcement-Scope/Downstream-plugin paragraph: "until M-2 executes, a skeleton build cut today carries **zero** trace of this convention — no ADR, no rule file" | Completeness, Actionability |
| 012-002 | Frontmatter Schema / Migration Plan M-2 / M-9 | No schema field or lint check for the general ADR↔companion-rule-file relationship; only this ADR's own pairing got a manual, one-off cross-link repair | 7 | 5 | 7 | **245** | Critical | Add an optional advisory frontmatter field (e.g., `companion_rule_file:`) mirroring `canonical_id:`'s precedent; disclose as a named, unmitigated residual if not added | Completeness, Traceability |
| 012-003 | Enforcement Design §Grandfather baseline | Grandfather-baseline temporal anchor is "when the lint ships" (unscheduled), not "when the convention was ratified" — every dialect ADR minted in the (undated) gap is auto-grandfathered as if pre-existing legacy | 6 | 6 | 7 | **252** | Critical | State explicitly that the grandfather baseline is capped at ratification date (2026-07-05/06) plus the 16/18-file count, OR disclose the amnesty-window risk as a named residual | Internal Consistency, Methodological Rigor |
| 012-004 | Canonical Location Model / L-3 scan scope | Cross-repository/cross-installation domain-slug collisions (downstream CoWork/plugin adopters, or future exemplar-corpus aggregation) have zero mitigation — not even guidance | 5 | 3 | 7 | **105** | Major | One-sentence disclosure noting cross-repository slug collisions are unmitigated by design (each install/repo is its own independent namespace) | Completeness |
| 012-005 | ID grammar / L-4 dialect closed set | No lifecycle path for project-ID renumbering/merger cascading into a mass dialect-ADR rename, contradicting the "no big-bang renumber" (c-003/D-4) principle | 6 | 2 | 4 | **48** | Minor | One-sentence disclosure that project-ID lifecycle churn is out of scope / assumed non-occurring | Internal Consistency |

**RPN totals:** Critical = 1,009 (3 findings) · Major = 105 (1 finding) · Minor = 48 (1 finding) · **Grand total = 1,253**

---

## Finding Details

### 012-001: Plugin-Distribution "Zero-Tooling Guidance" Overclaim

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 512 = 8×8×8) |
| **Element** | Enforcement Scope and Deployment Targets §Downstream/plugin disclosure |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) — lens: Incorrect / Insufficient |

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:675` — "**Downstream/plugin disclosure (PM-002/PM-006, P-022).** ... **What carries value downstream on day one is the *guidance*, which needs no tooling.** Disclosed so the enforcement claim is not overstated for the exact CoWork target PROJ-031 serves."
- `ADR-PROJ031-004-adr-identifier-convention.md:663` — "The `decisions/` corpus the lint validates is also not present — `projects/` (and recommended `docs/`) are stripped, so a plugin install ships *no* ADR files to lint." (This line discloses the ADR-corpus absence for *linting purposes*; it does not connect that the *guidance document itself* is equally absent for *reading purposes*.)
- `projects/PROJ-031-cowork-skeleton/design/phase3-skeleton-generation-design.md:159-160` — `git rm -r projects/ tests/ skills/.graveyard .github  # retains everything else BY CONSTRUCTION` / `projects/       ~4,600  work artifacts` — confirms `projects/` is on the **validated, unconditional** strip-set (not the "recommended additional strips" tier that includes `docs/`, line 168).
- Both reviewed deliverables physically reside under `projects/PROJ-031-cowork-skeleton/decisions/` and `projects/PROJ-031-cowork-skeleton/design/` respectively — i.e., inside the always-stripped tree.
- `ADR-PROJ031-004-adr-identifier-convention.md:530` — Migration-Plan row M-2 ("Author `.context/rules/adr-standards.md` from Deliverable 2") is listed `TBD-Task`, no committed date, no worktracker Task or GitHub Issue open (per the ADR's own Claim-Status disclosure at line 525).

**Analysis:** The sentence at line 675 is an affirmative, present-tense claim ("carries value... on day one... needs no tooling") that a specific benefit already exists for downstream CoWork/plugin adopters. That claim is only true once `.context/rules/adr-standards.md` exists and is baked into a subsequently-cut skeleton build. As of this review, neither condition holds: M-2 is untracked with no timeline, and the file that WOULD carry the guidance still lives at `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` — squarely inside the strip-set. This means a skeleton build cut *today* (or any build cut before M-2 lands) ships **zero** trace of this convention: no ADR, no rule file, no lint target. Line 663 discloses that the ADR corpus is absent (relevant to *linting*), but does not draw the parallel, more severe conclusion that the *normative prose itself* is equally absent (relevant to *reading/following*). Pre-Mortem row FM-5 (`ADR-PROJ031-004:496`) comes closest, but its containment claim — "the guidance's zero-tooling value... bounds the damage even if the lint never ships" — implicitly assumes a reader with access to the geekatron/jerry source repo (where `projects/` still exists); it does not address the structurally distinct downstream-plugin reader, who has access to *neither* file until M-2 executes and a fresh build is cut. This is exactly the audience PROJ-031-cowork-skeleton exists to serve, making this the single highest-severity gap in the package relative to the task's stated purpose ("adoptable MEDIUM-tier convention").

**Corrective Action:** Add one sentence to the §Downstream/plugin disclosure paragraph (or immediately following it): "Until M-2 executes and a subsequent skeleton build is cut, a distributed plugin install carries **no trace of this convention at all** — the guidance file does not yet exist at its auto-loaded destination. The 'day one' framing describes the intended post-M-2 state, not the current one." This is a text-only fix consistent with the package's own subtraction doctrine (disclose, do not build new machinery).

**Acceptance Criteria:** The overclaim sentence at line 675 is either removed or qualified with the above disclosure; FM-5's containment clause is cross-referenced to note the downstream-plugin-reader exception explicitly.

**Estimated Post-Correction RPN:** ~120 (S=8, O=8, D=2 — the gap becomes disclosed rather than hidden; underlying absence remains until M-2 ships, but that is already an accepted, monitored INHERENT residual class per the package's own doctrine).

---

### 012-002: No General Schema Field or Lint Check for the ADR↔Companion-Rule-File Relationship

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 245 = 7×5×7) |
| **Element** | Frontmatter Schema; Migration Plan M-2/M-9; Enforcement Design (L-7) |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) — lens: Missing |

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:530` (M-2) and `:539` (M-9) both describe a **manual, hand-authored** "reciprocal cross-link repair" specific to *this* ADR and *its own* companion rule draft: "**Cross-link repair (DA-002):** ... re-point (a) *this* rule file's inbound relative link ... and (b) the parent ADR's outbound relative links ... **both moves (M-2 and M-9) SHOULD update the reciprocal link in the same commit**."
- Frontmatter Schema block (`adr-standards-rule-draft.md:100-117`; ADR mirror `:350-369`) lists 13 fields (`id, type, status, scope, origin_project, origin_entity, created, supersedes, superseded_by, amends, amended_by, promoted_from, promoted_to, canonical_id`) — **none** references a companion normative-rule file.
- L-7 (`adr-standards-rule-draft.md:179`; ADR mirror `:685`) checks only `superseded_by`/`promoted_to`/`promoted_from` — it does not, and is not designed to, resolve a cross-link to a companion `.context/rules/*.md` file.
- Confirmed general pattern (not unique to this ADR pair): `docs/design/ADR-agent-design-001.md` pairs with `.context/rules/agent-development-standards.md`; `docs/design/ADR-routing-triggers-001.md` pairs with `.context/rules/agent-routing-standards.md`; `ADR-EPIC002-001`/`ADR-EPIC002-002` pair with `.context/rules/quality-enforcement.md` (all cited within this ADR's own References/Related-Decisions tables, `:732-734`).

**Analysis:** The convention's Promotion Process (Path 1/Path 2) is specified as if an ADR is always a single, self-contained file. In practice — as this very deliverable pair demonstrates, and as the three pre-existing canonical framework ADRs demonstrate — Jerry's actual governance pattern routinely produces an ADR **plus** a companion normative rule file that must move/rename in lockstep. The only mechanism addressing this today is a bespoke, prose-only instruction confined to M-2/M-9 for this one pair; there is no frontmatter field, no relationship type, and no lint rule generalizing it. The next framework ADR that spawns (or is retrofitted with) a companion rule file will face the identical citation-break risk from scratch, with no schema support and no L-7-equivalent check — reproducing, for the framework's most common and highest-value ADR pattern, the exact citation-continuity failure this convention exists to prevent.

**Corrective Action:** Add an optional advisory frontmatter field, e.g. `companion_rule_file: null`, mirroring the `canonical_id:` precedent (also optional, advisory, null-by-default, no lint enforcement) — or, if declining new schema per the subtraction doctrine, add an explicit disclosed residual naming this as a recurring, general risk beyond the M-2/M-9 one-off fix.

**Acceptance Criteria:** Either the field is added to both Frontmatter Schema blocks, or a new Risks-register row (R-18) discloses the general pattern with an owner and detection signal, analogous to R-14 through R-17's treatment.

**Estimated Post-Correction RPN:** ~70 (S=7, O=5, D=2 — disclosed and named, even without new lint machinery).

---

### 012-003: Grandfather-Baseline Temporal Anchor Creates an Unbounded Post-Ratification Amnesty Window

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 252 = 6×6×7) |
| **Element** | Enforcement Design §Grandfather regression test; L-1 spec "pre-adoption grandfathered" clause |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) — lens: Inconsistent |

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:688` — "grandfathering is resolved against a **static adoption-time baseline** — the enumerable set of ADR files that exist **when the lint first ships** (the 18 reachable above plus the out-of-scan `ADR-STORY015-001`, captured **once** as a data list in M-6...)."
- `ADR-PROJ031-004-adr-identifier-convention.md:223` (D-4) — "**Existing scope-prefixed and legacy ADRs are grandfathered**... No big-bang renumber (c-003). The **15 pre-existing** dialect ADRs remain valid legacy-dialect instances **in place**." (D-4's own language ties "grandfathered" to *pre-existing/legacy*, i.e., pre-ratification.)
- `adr-standards-rule-draft.md:48` (ADR-M-003) — the project-local dialect remains **SOFT `MAY`**-permitted for new ADRs going forward, with no expiry.
- `ADR-PROJ031-004-adr-identifier-convention.md:536` (M-6) — lint implementation has **no committed timeline** ("TBD-Task + GH Issue"); Pre-Mortem FM-5 (`:496`) independently rates "nothing lands" as the single best-evidenced risk in the whole package.

**Analysis:** The spec text explicitly anchors the grandfather baseline to **lint-ship time**, not **convention-ratification time**. Because D-3/ADR-M-003 continues to *permit* new dialect ADRs indefinitely (SOFT MAY, no deprecation date), and M-6 has no committed ship date, every dialect ADR authored in the — potentially long, per FM-5's own risk rating — gap between ratification (2026-07-05/06) and eventual lint-shipping will be captured into the "static adoption-time baseline" and thereby **permanently exempted** from L-1/L-2 as though it were pre-existing legacy. This is inconsistent with D-4's own stated intent, which frames grandfathering as a courtesy for *existing, pre-convention* ADRs, not an ongoing amnesty for ADRs minted with full knowledge of the ratified convention. The longer M-6 is delayed, the larger this baseline grows and the more of the "SHOULD prefer canonical slug" guidance is retroactively excused — a design flaw independent of whether the delay in practice turns out to be short.

**Corrective Action:** Anchor the grandfather baseline to the ratification date (2026-07-05/06, the already-reconciled 16/15/3/18 counts) rather than "whenever the lint ships," OR explicitly disclose the amnesty-window mechanism and its growth risk as a named residual (parallel to R-1/PM-009's "lint may never ship" framing, but distinct: this is about *scope creep of the exemption*, not *the lint never existing*).

**Acceptance Criteria:** The L-1 spec's "pre-adoption grandfathered" clause (`:688`, mirrored in the rule draft `:183`) either fixes the baseline to the ratification-date count, or a new sentence discloses that any dialect ADR minted after ratification and before M-6 ships is *also* grandfathered by construction, and names this as accepted (not silently implied).

**Estimated Post-Correction RPN:** ~84 (S=6, O=6, D=2 — disclosed rather than hidden; the underlying M-6-timeline risk remains the already-tracked FM-5/R-1 residual).

---

### 012-004: Cross-Repository / Cross-Installation Domain-Slug Collision Has No Mitigation, Not Even Guidance

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (RPN 105 = 5×3×7) |
| **Element** | Canonical Location Model; L-3 scan scope; Enforcement Scope and Deployment Targets |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) — lens: Missing |

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:672` — "**CI-independent `uv run jerry lint adr`** — ... exposed as a CLI subcommand ... for downstream authors" (each downstream install runs its **own**, independent L-3 check against its **own** corpus only).
- `adr-standards-rule-draft.md:177` (L-3) — "Extract `{slug}-NNN`... of all non-frozen ADRs; `sort | uniq -d` must be empty. **Across the scanned roots**..." — the scan is always local to one repository's filesystem; no cross-repository or cross-installation registry is proposed or possible under c-006 (no server process).
- `docs/knowledge/exemplars/templates/adr.md` exists as shared exemplar tooling, and PROJ-031's stated mission is producing distributable CoWork/plugin skeletons for many independent downstream repositories (per this ADR's own Enforcement Scope section, `:658-676`).

**Analysis:** The convention's collision-safety guarantee (L-3, the pre-flight one-liner) is, by design (c-006, no central registry), scoped to a single repository. This is reasonable for the source repo, but PROJ-031's explicit purpose is to seed many independent downstream repositories with the *same* convention. If two independent downstream adopters (or a future community exemplar/aggregation effort referencing `docs/knowledge/exemplars/`) each mint `ADR-plugin-distribution-001` for unrelated subjects, nothing — not the lint, not even guidance — flags this, because each install's L-3 only ever sees its own filesystem. This is a distinct mechanism from R-6 (cross-*branch*, same-repo race): it is cross-*repository* and has no disclosed mitigation anywhere in either deliverable.

**Corrective Action:** A one-sentence disclosure in the Enforcement Scope section noting that cross-repository/cross-installation domain-slug collisions are unmitigated by design (each install is an independent namespace), so any future cross-repository aggregation of ADRs (e.g., a shared exemplar library) would need its own, separately-designed slug-uniqueness discipline.

**Acceptance Criteria:** A sentence is added; no new lint or registry is implied (consistent with the subtraction doctrine).

**Estimated Post-Correction RPN:** ~30 (disclosed residual, unmitigated by design, low occurrence).

---

### 012-005: No Lifecycle Path for Project-ID Renumbering/Merger Cascading Into a Mass Dialect-ADR Rename

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor (RPN 48 = 6×2×4) |
| **Element** | ID grammar (dialect); L-4 ID↔location |
| **Strategy Step** | Step 2 (Enumerate Failure Modes) — lens: Missing |

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:335-341` — dialect grammar `ADR-{PROJECT-ID}-NNN` is keyed directly to the closed prefix set `{PROJ|EPIC|FEAT|STORY}\d{3}`, i.e., the literal project/entity ID string.
- `adr-standards-rule-draft.md:178` (L-4) — "A `PROJ{NNN}`/... dialect prefix ... matches its containing project/entity dir."
- No section of either deliverable addresses what happens if a project's own ID changes (rename, renumber, or merge with another project).

**Analysis:** Every dialect ADR's identity is permanently coupled to its birth project's ID string. If a project were ever renumbered or merged (an operation this ADR does not rule out, and Jerry's worktracker does not appear to forbid), every dialect ADR under it would simultaneously fail L-4 and require a coordinated rename — precisely the "big-bang renumber" D-4/c-003 explicitly forbids, but at the *project* level rather than the *ADR* level. This is a low-occurrence, low-detection-difficulty (L-4 would immediately and visibly fail) scenario, rated Minor.

**Corrective Action:** One sentence disclosing that project-ID lifecycle stability is an unstated assumption of the dialect grammar; recommend the canonical domain-slug form precisely because it is immune to this class of churn (reinforcing the existing D-1 rationale).

**Acceptance Criteria:** Sentence added or explicitly deferred as out-of-scope with rationale.

---

## Recommendations

Ranked by RPN, all closable by **disclosure-only or narrowly-scoped text edits** — consistent with the package's own subtraction doctrine (no new lint rules, ledgers, or gates required):

1. **012-001 (RPN 512, Critical):** Correct the overclaim at `ADR-PROJ031-004:675` — state plainly that a skeleton build cut before M-2 executes carries zero trace of the convention. This is the single most consequential fix relative to the stated purpose of an "adoptable MEDIUM-tier convention" for the CoWork/plugin audience.
2. **012-003 (RPN 252, Critical):** Anchor the grandfather baseline to ratification date or explicitly disclose the amnesty-window growth risk at `ADR-PROJ031-004:688` / `adr-standards-rule-draft.md:183`.
3. **012-002 (RPN 245, Critical):** Add an optional advisory `companion_rule_file:` frontmatter field (mirroring `canonical_id:`), or disclose the general pattern as a new residual (R-18) beyond the one-off M-2/M-9 fix.
4. **012-004 (RPN 105, Major):** One-sentence disclosure of unmitigated cross-repository slug-namespace exposure.
5. **012-005 (RPN 48, Minor):** One-sentence disclosure of the project-ID-renumbering assumption.

None of these require restoring deleted machinery (waiver ledgers, second-reviewer gates, additional lint rules) — all are consistent with, and closable under, the same "subtract/disclose, don't compensate" doctrine the package has applied in iterations 5-8.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | 012-001: the convention's adoptability claim is incomplete for its stated primary audience; 012-002: no schema coverage for the general companion-rule-file pattern; 012-004: no coverage for cross-repository collisions |
| Internal Consistency | 0.20 | Negative | 012-003: grandfather-baseline temporal anchor contradicts D-4's own "existing/legacy" framing; 012-005: dialect grammar assumes project-ID permanence without stating it |
| Methodological Rigor | 0.20 | Negative | 012-003: the FMEA/Pre-Mortem's own containment claims (FM-5) do not hold for the downstream-plugin-reader case that 012-001 identifies |
| Evidence Quality | 0.15 | Neutral | All 5 findings are supported by direct file+line citations (`ADR-PROJ031-004`, `adr-standards-rule-draft.md`, `phase3-skeleton-generation-design.md`); no unlabeled inference |
| Actionability | 0.15 | Neutral-to-Positive | Every corrective action is a scoped, one-to-two-sentence disclosure edit, directly actionable without new machinery |
| Traceability | 0.10 | Negative | 012-002 highlights that the ADR↔rule-file relationship (used repeatedly across the corpus: agent-design, routing-triggers, EPIC-002) has no traceable schema field |

---

## Execution Statistics

- **Total Findings:** 5
- **Critical:** 3 (012-001 RPN 512, 012-002 RPN 245, 012-003 RPN 252)
- **Major:** 1 (012-004 RPN 105)
- **Minor:** 1 (012-005 RPN 48)
- **Protocol Steps Completed:** 5 of 5 (Decompose; Enumerate; Rate S/O/D; Prioritize/Corrective Actions; Synthesize/Score Impact)

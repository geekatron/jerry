# Chain-of-Verification Report: ADR-PROJ031-004 + adr-standards-rule-draft.md (Iteration 10)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.11) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.11/253 lines)
**Criticality:** C4 (gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-011 CoVe, blind iteration 10)
**H-16 Compliance:** S-003 embedded in the deliverable's own H-16 traceability note (ST-001/ST-002); not separately re-run this iteration (indirect for CoVe per template)
**Claims Extracted:** 19 | **Verified:** 18 | **Discrepancies:** 1 (Critical)

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verification assessment |
| [Verification Scope](#verification-scope) | What was checked and how |
| [Findings Summary](#findings-summary) | Table of all findings |
| [Detailed Findings](#detailed-findings) | Evidence, verification, disposition |
| [Verification Log](#verification-log) | Claims checked and pass/fail (18 verified clean) |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

Independent verification of 19 load-bearing factual claims (grandfather-count reconciliation, file-existence claims, exact line/quote citations, the pre-flight collision command, and the enforcement-design corpus) found **18 VERIFIED clean** against the filesystem — a strong result given 9 prior iterations of intensive fact-checking. One **Critical** discrepancy was found and is genuinely novel (not covered by the R-1..R-17/R-A/R-B/R-C residual register): the Canonical Location Model table has no row that describes the actual, real, on-disk location of the two grandfathered `EPIC002`-prefixed dialect ADRs the document repeatedly relies on as central evidence — a gap that would make the L-4 (ID↔location) lint rule misfire on those exact files the moment Migration-Plan item M-11 (which explicitly schedules editing them) executes. **Recommendation: REVISE** — one targeted table/rule fix (add a location-model row, or explicitly disclose the gap as a residual) closes it; no other Critical survives verification.

---

## Verification Scope

Both deliverables were read in full (ADR: 797 lines; rule-draft: 253 lines) plus the readable disposition record (`subtraction-pass-notes.md`, all iterations through iter-9). Per the BLIND protocol, iteration-009/010 adversary directories were not read except this file. Independent verification used Glob/Grep/Read against the live filesystem — never re-reading the deliverable's own characterization while checking a claim.

---

## Findings Summary

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-i010 | "The 15 pre-existing dialect ADRs remain valid legacy-dialect instances in place" / Canonical Location Model table enumerates all legitimate dialect location patterns (ADR D-4, Canonical Location Model ~L384-393; rule-draft Canonical Location Model ~L77-88) | Live filesystem: `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md`, `ADR-EPIC002-002-enforcement-architecture.md` | The Location Model table has no row matching these two files' actual (location, ID-form) pairing; L-4 would misfire on them the moment they are git-modified (which Migration-Plan M-11 explicitly schedules) | **Critical** | Internal Consistency / Methodological Rigor |

---

## Detailed Findings

### CV-001-i010: Canonical Location Model omits the actual location pattern of the two grandfathered `EPIC002` dialect ADRs; L-4 (ID↔location) would misfire on them [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR: [Decision D-4 grandfather-count reconciliation](../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md#decision) (~L225-231); [Canonical Location Model](../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md#l1-technical-implementation) (~L384-393); [Enforcement Design L-4](../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md#enforcement-design-l5-ci-lint) (~L689); Migration Plan M-11 (~L546). Rule draft: [Canonical Location Model](../../../design/adr-standards-rule-draft.md#canonical-location-model) (~L77-88); [L5 CI Lint L-4](../../../design/adr-standards-rule-draft.md#l5-ci-lint-specification) (~L178) |
| **Strategy Step** | Step 3 (Independent Verification) + Step 4 (Consistency Check) |

**Claim (from deliverable, quoted verbatim, ADR ~L226):** "16 = the whole dialect corpus — every `ADR-{PROJ\|EPIC\|STORY}NNN-NNN` plus the one `ADR-150-NNN`, in *any* location, including this ADR and including the out-of-scan entity-embedded `ADR-STORY015-001`: `EPIC002`×2, `PROJ010`×6, `PROJ022`×2, `PROJ031`×4, `STORY015`×1, `150`×1 = **16**." The ADR treats `EPIC002`×2 as a legitimately grandfathered, in-scan dialect family (part of the "15 dialect files reachable by the scan path," ~L227), on par with the other dialect families.

**Independent Verification (source: live filesystem, not the deliverable's characterization):**
- Glob-verified: `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md` and `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-002-enforcement-architecture.md` both exist.
- Read-verified: `ADR-EPIC002-001-strategy-selection.md` frontmatter comment block declares `PROJECT: PROJ-001-oss-release` and `EPIC: EPIC-002` — i.e., its *containing project directory* is `PROJ-001-oss-release`, not an `EPIC-002`-named directory anywhere in its path.
- The Canonical Location Model table (ADR ~L384-393, rule-draft ~L79-88) defines exactly two rows that can host a *dialect* (non-canonical-slug) ADR:
  1. `Project (permitted dialect)` → home `projects/PROJ-NNN-*/decisions/`, **ID form `ADR-PROJ{NNN}-NNN`** (PROJ-prefix only — the cell does not show the full `{PROJ\|EPIC\|FEAT\|STORY}` set).
  2. `Entity-embedded (permitted)` → home `projects/.../work/.../{ENTITY}/`, ID form `ADR-{PROJ\|EPIC\|FEAT\|STORY}NNN-NNN` — but this row's *canonical home* is inside the entity's own `work/` folder, not a project-level `decisions/` folder.
- `ADR-STORY015-001-tier-model-renumbering.md` (Glob-verified at `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/`) **is** the correct worked example of row 2: an entity-embedded `STORY`-prefixed dialect ADR physically inside its own `work/.../STORY-015-.../` folder — exactly matching the model. This is disclosed by the ADR as R-10 (out-of-scan because it has no `decisions/` segment).
- `ADR-EPIC002-001`/`002`, by contrast, use the `EPIC`-prefixed dialect form (row 2's ID grammar) but physically live in `projects/PROJ-001-oss-release/decisions/` — row 1's *location* (a project `decisions/` folder), which row 1 only sanctions for the `PROJ` prefix. **This (location, ID-form) pairing matches neither table row.**

**Discrepancy:** The document's implicit claim — that the Canonical Location Model table plus the grandfather clause together describe every legitimate location for the 15/16-file dialect corpus it grandfathers — is false for 2 of those 15 files. `L-4 ID↔location` is specified (ADR ~L689; rule-draft ~L178) to check that "A `PROJ{NNN}`/`EPIC{NNN}`/`FEAT{NNN}`/`STORY{NNN}` dialect prefix (full closed set) matches its containing project/entity dir." For `ADR-EPIC002-001`/`002`, the containing directory is `PROJ-001-oss-release` — under any literal reading, `EPIC002` does not match that. Two consequences follow, both undisclosed:
1. **If L-4's grandfather exemption is scoped only to L-1/L-2** (the only two rules the document's "how pre-adoption grandfathered is resolved" clause names explicitly, both ADR ~L693 and rule-draft ~L183), then L-4 will genuinely FAIL these two files the moment they are next git-modified. This is not hypothetical: Migration-Plan **M-11** (ADR ~L546) explicitly schedules "Retrofit real YAML frontmatter (`id`/`scope`/`origin_project`) onto the 3 `docs/design/` framework ADRs **and onto** ... `ADR-EPIC002-001-strategy-selection`, `ADR-EPIC002-002-enforcement-architecture`" — a git-modification of precisely these two files, performed as part of this convention's own adoption plan.
2. **If L-4's grandfather exemption is meant to cover all 5 rules for any pre-adoption file** (as the 5-rule table's blanket header parenthetical "(git-added/modified files; pre-adoption grandfathered)" could be read to imply), that reading is never reconciled with the document's own emphatic, dated **ratification-time baseline** anchoring (012-003, ADR ~L693) — which was added specifically to prevent L-1/L-2 from amnestying files indefinitely. No equivalent bound is stated for L-4, so this reading would leave L-4 permanently unable to validate 2 of the corpus's most-cited files, undisclosed as a residual.

Either reading exposes the same root defect: **the Canonical Location Model table itself is incomplete** — it does not contain a row describing where `ADR-EPIC002-001`/`002` actually live, even though the document elsewhere (D-4, the Rationale's bimodal-promotion argument, the Sensitivity section, the CV-001 collision-resistance narrative, References #6) treats these exact two files as its **central evidentiary corpus** for the entire promotion-frequency and collision arguments the ADR is built on.

**Severity:** Critical — this is a self-inflicted defect in the convention's own enforcement design, verified against the convention's own core evidence, that a scheduled Migration-Plan action (M-11) would trigger. It directly undermines "collision-free ADR identity" honesty (the location model does not actually describe the real corpus it claims to grandfather) and "adoptable ... convention" (a real adopter executing M-11 in good faith would hit an undisclosed lint-failure mode on the framework's own flagship strategy-selection and enforcement-architecture ADRs).

**Dimension:** Internal Consistency (the Location Model table's implicit completeness claim is false), Methodological Rigor (the 9 prior iterations' exhaustive residual register — R-1 through R-17, R-A/R-B/R-C — never surfaces this specific location/ID-form mismatch, despite extensively treating adjacent location-class gaps for STORY015 (R-10) and repository-based topology).

**Correction:** Either (a) add a third dialect-location row to the Canonical Location Model table (both files) explicitly sanctioning `ADR-{EPIC|FEAT|STORY}{NNN}-NNN` inside a project-level `decisions/` folder (not only `ADR-PROJ{NNN}-NNN`), and correspondingly broaden L-4's location-matching logic to accept a project-level match against ANY of the four prefixes (not just an entity-embedded-folder match for the non-PROJ three); or (b) explicitly disclose a new residual (parallel to R-9/R-10) stating that `ADR-EPIC002-001`/`002` are grandfathered exceptions to the location model that L-4 will need a specific allowlist/exemption for, and flag M-11 as dependent on that exemption landing first. Either fix is a small, targeted table/prose edit — no new lint rule required, consistent with the subtraction doctrine.

---

## Verification Log

All 19 extracted claims, independently checked against source (not the deliverable's characterization):

| # | Claim | Source Checked | Result |
|---|-------|-----------------|--------|
| 1 | 16 = whole dialect corpus (`EPIC002`×2/`PROJ010`×6/`PROJ022`×2/`PROJ031`×4/`STORY015`×1/`150`×1) | Glob: `docs/design/ADR-*.md` (3), `projects/*/decisions/ADR-*.md` (15), `**/ADR-STORY015-001*` (1, out-of-scan) | **VERIFIED** — counts reconcile exactly: 2+6+2+4+1+1=16 |
| 2 | 15 = dialect files reachable by the scan path (16 − out-of-scan STORY015) | Glob: `projects/*/decisions/ADR-*.md` returned exactly 15 files | **VERIFIED** |
| 3 | 3 = canonical framework ADRs in `docs/design/` | Glob: `docs/design/ADR-*.md` → `agent-design-001`, `output-path-resolution-001`, `routing-triggers-001` | **VERIFIED** |
| 4 | 18 = grandfather regression corpus (15+3) | Arithmetic + file lists above | **VERIFIED** |
| 5 | `ADR-STORY015-001` is out-of-scan (no `decisions/` segment in its path) | Glob: file lives at `.../work/.../STORY-015-tier-model-renumbering/ADR-STORY015-001-...md` | **VERIFIED** |
| 6 | `scripts/lint_adr_convention.py` does not exist (Claim-Status: designed, not built) | Glob: `**/lint_adr_convention.py` → no matches | **VERIFIED** |
| 7 | The two-clause pre-flight `find` command produces a clean `sort\|uniq -d` (no collisions) across the 18-file corpus | Manually traced all 18 filenames through the extraction regex | **VERIFIED** — all 18 extracted IDs are unique |
| 8 | `.github/workflows/ci.yml:2` cites a dangling `ADR-CI-001` at `projects/PROJ-001-plugin-cleanup/decisions/...` | Read `ci.yml:2` (exact match) + Glob `projects/PROJ-001-plugin-cleanup/**` (no files found) | **VERIFIED** — citation is dangling exactly as claimed |
| 9 | Stale `ADR-PROJ007-001`/`002` citations live at `WORKTRACKER.md:106-107` | Grep with line numbers | **VERIFIED** — exact match |
| 10 | Stale citations live at `ORCHESTRATION.yaml:228,242` | Grep with line numbers | **VERIFIED** — exact match |
| 11 | Stale citations live at `EN-001.md:48-49,72-73` | Grep with line numbers | **VERIFIED** — exact match (also found at :89-90, not claimed but consistent) |
| 12 | `skills/architecture/SKILL.md:105,284,437` cite `ADR_NNN`/`ADR_001_...` underscore-separated forms | Grep + Read at cited lines | **VERIFIED** — L105 `ADR_NNN_*.md`, L284 `ADR_001_sqlite_persistence.md`, L437 `ADR_NNN_*.md` |
| 13 | `docs/knowledge/exemplars/templates/adr.md:1` uses bare `# ADR-{NUMBER}: {Title}`; `:182` cites dangling `docs/decisions/...` | Grep with line numbers | **VERIFIED** — exact match |
| 14 | FEEDBACK-LOG.md FU.0 quotes "I ratify the promotion-is-the-point apporach and lock Scheme B." (typo preserved) | Grep exact string match | **VERIFIED** — exact match including preserved typo |
| 15 | `skills/problem-solving/agents/ps-architect.md:218` = bare `# ADR-{NUMBER}: {Title}` title | Read at line 218 | **VERIFIED** — exact match |
| 16 | `ps-architect.md:267-268` = phantom `python3 scripts/cli.py link-artifact ...` | Read at lines 263-272 | **VERIFIED** — exact match |
| 17 | `ps-architect.md:482,509` also contain `python3 scripts/cli.py` occurrences (M-12's grep-pinned footprint) | Grep for `python3 scripts/cli.py` | **VERIFIED** — matches at :267, :482, :509 exactly as the footprint claims |
| 18 | `ADR-EPIC002-001-strategy-selection.md` carries no YAML `scope:`/`id:` frontmatter field (only an HTML-comment metadata block) | Read lines 1-15 | **VERIFIED** — confirmed HTML-comment-only metadata, no YAML `---` block |
| 19 | Canonical Location Model table describes all legitimate dialect (location, ID-form) pairings for the grandfathered 15/16-file corpus | Cross-checked table rows against real file locations for all dialect families | **MATERIAL DISCREPANCY** → CV-001-i010 (Critical, above) |

**Verification rate: 18/19 (94.7%)** — a strong result reflecting the value of 9 prior CoVe/red-team/FMEA passes; the single surviving discrepancy is novel and not covered by the existing R-1..R-17/R-A/R-B/R-C register.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Claim coverage is otherwise complete; CV-001-i010 is a gap in the model's own coverage, not in this review's |
| Internal Consistency | 0.20 | **Negative** | CV-001-i010: the Location Model table's implicit "describes all legitimate dialect locations" claim is false for 2 of 15 grandfathered files |
| Methodological Rigor | 0.20 | **Negative** | CV-001-i010: L-4's spec and the grandfather-baseline clause do not reconcile with the real corpus L-4 will eventually run against |
| Evidence Quality | 0.15 | Positive | 18/19 claims independently verified with exact file/line citations; the one discrepancy is evidenced with the same rigor |
| Actionability | 0.15 | Neutral | Correction is a small, targeted table/prose edit (either option), consistent with the subtraction doctrine — no new lint rule needed |
| Traceability | 0.10 | Positive | Every VERIFIED and the one MATERIAL DISCREPANCY trace claim → source → independent check → result |

---

## Execution Statistics

- **Total Findings:** 1
- **Critical:** 1
- **Major:** 0
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5
- **Claims independently verified:** 18/19 (94.7%)

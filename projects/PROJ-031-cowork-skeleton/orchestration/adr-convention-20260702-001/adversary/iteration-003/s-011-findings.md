# Chain-of-Verification Report: ADR-PROJ031-004 / adr-standards-rule-draft.md (iteration 3)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-011, blind reviewer, iteration 3)
**H-16 Compliance:** Per the deliverable's own reading-note tag glossary, S-003/S-002/S-004/etc. were applied in prior iterations (not independently confirmed by this reviewer — blind protocol forbids reading the adversary directory)
**Claims Extracted:** 46
**Verified:** 44
**Discrepancies:** 2 (both Major; zero Critical/fabrication-class findings)

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Claim Inventory](#claim-inventory) | Extracted testable claims (CL-NNN) with verification status |
| [Findings Table](#findings-table) | CV-NNN findings with severity |
| [Finding Details](#finding-details) | Expanded evidence for the two Major findings |
| [Verification Ratios](#verification-ratios) | Verified/Discrepancy/Unverifiable counts |
| [Recommendations](#recommendations) | Corrections by severity |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Protocol completion |

---

## Summary

This package is exceptionally well fact-checked. Of 46 independently-verified testable claims — spanning corpus counts, exact line-number citations, quoted file contents, cross-references, and historical assertions — **44 verified exactly against source** (95.7%), including several multi-way numeric cross-checks (e.g., the "19 files exercised" regression-test count reconciles perfectly against an independent `Glob` corpus count performed by this reviewer without reference to the deliverable's own arithmetic). **Two Major discrepancies were found**, both concerning the historical narrative of the `ADR-EPIC002-001` collision resolution and a self-correction that undercounts a defect. **Zero Critical (fabrication-class) findings.** Recommendation: **REVISE** — the two Major findings should be corrected before ratification, but neither invalidates the core Scheme B decision, which remains well-supported by the (verified) corpus evidence.

---

## Claim Inventory

| ID | Claim (abbreviated) | Category | Status |
|----|----|----|----|
| CL-001 | No documented ADR standard exists anywhere in the repo | Cross-reference | VERIFIED (`adr-convention-standards-research.md:31-49`) |
| CL-002 | `docs/knowledge/exemplars/templates/adr.md:1` title placeholder is `# ADR-{NUMBER}: {Title}` | Quoted value | VERIFIED (exact) |
| CL-003 | `adr.md:182` PS-Integration line points at non-existent `docs/decisions/...` | Quoted value | VERIFIED (exact) |
| CL-004 | `skills/architecture/SKILL.md:105,284,437` use underscore `ADR_NNN_*.md` | Quoted value | VERIFIED (exact, all 3 lines) |
| CL-005 | `SKILL.md:288` example uses bare hyphenated `# ADR-001: Use SQLite for Persistence` | Quoted value | VERIFIED (exact) |
| CL-006 | `quality-enforcement.md:108,275,290,350` cite `ADR-EPIC002-001` (strategy-selection) | Rule citation | VERIFIED (exact, all 4 lines) |
| CL-007 | `.github/workflows/ci.yml:2` cites `ADR-CI-001` at a `PROJ-001-plugin-cleanup` path that no longer exists | Cross-reference | VERIFIED (line exact; `projects/PROJ-001-plugin-cleanup` confirmed absent — only `PROJ-001-oss-release` exists) |
| CL-008 | Corpus family counts: Framework domain-slug=3, Project-ID=11, Entity-ID=3, GH-issue=1, Bare legacy=6+1, Bare archived=4, Bare transient=4, OSS series=7 | Quoted value (counts) | VERIFIED (independent `Glob` recount matches exactly; cross-checked against `adr-convention-standards-research.md:57-68`) |
| CL-009 | 16 live dialect ADRs (15 pre-existing + this ADR); regression test exercises 19 files total (16 dialect + 3 canonical) | Quoted value (counts) | VERIFIED (independent recount: PROJ010×6 + PROJ022×2 + PROJ031×4(incl. this ADR) + EPIC002×2 + STORY015×1 + ADR-150-001×1 + docs/design×3 = 19) |
| CL-010 | 14 pre-existing project-level ADRs (15 incl. this ADR) across PROJ-001/010/022/030/031 | Quoted value (counts) | VERIFIED (2+6+2+1+3=14, +this ADR=15) |
| CL-011 | `docs/design/ADR-agent-design-001.md:3` carries HTML comment `PS-ID: PROJ-007 \| ENTRY: e-004` | Quoted value | VERIFIED (exact) |
| CL-012 | `docs/design/ADR-routing-triggers-001.md:3` carries an HTML-comment PS-ID (not YAML) | Quoted value | VERIFIED (exact) |
| CL-013 | `docs/design/ADR-output-path-resolution-001.md:8` carries blockquote `> **Parent:** EPIC-002` | Quoted value | VERIFIED (exact) |
| CL-014 | None of the 3 framework ADRs carry the proposed YAML frontmatter schema | Behavioral claim | VERIFIED (all 3 files inspected; none start with a `---` YAML block) |
| CL-015 | `PROJ-007-agent-patterns/ORCHESTRATION.yaml:228,242` still cite stale `ADR-PROJ007-001/002` | Historical assertion | VERIFIED (exact, both lines) |
| CL-016 | `PROJ-007-agent-patterns/WORKTRACKER.md:106-107` still cite stale `ADR-PROJ007-001/002` | Historical assertion | VERIFIED (exact, both lines) |
| CL-017 | `PROJ-007-agent-patterns/.../EN-001.md:48-49,72-73` still cite stale `ADR-PROJ007-001/002` | Historical assertion | VERIFIED (exact, all 4 lines) |
| CL-018 | `ps-architect.md:218` hardcodes bare `# ADR-{NUMBER}: {Title}` | Quoted value | VERIFIED (exact) |
| CL-019 | `ps-architect.md:263` references phantom `templates/adr.md` (doesn't exist at repo root) | Cross-reference | VERIFIED (`templates/adr.md` Glob returns nothing; real file is `docs/knowledge/exemplars/templates/adr.md`) |
| CL-020 | `ps-architect.md:267,482,509` invoke phantom `python3 scripts/cli.py` (script absent, `python3` violates H-05) | Cross-reference + rule citation | VERIFIED (`scripts/cli.py` Glob returns nothing; all 3 lines exact) |
| CL-021 | Real CLI entrypoint is `pyproject.toml:65` `jerry = "src.interface.cli.main:main"` | Quoted value | VERIFIED (exact) |
| CL-022 | "~6 grammar-family instances" of the non-canonical filename pattern in `ps-architect.md`, correcting a prior "10" overcount | Quoted value (count) | **MATERIAL DISCREPANCY — see CV-001** |
| CL-023 | `worktracker-directory-structure.md:65` shows `DEC-NNN` composite parent-scoped at Epic level | Quoted value | VERIFIED (exact) |
| CL-024 | `worktracker-directory-structure.md:80,88` show bare `DEC-NNN` at Enabler/Story level | Quoted value | VERIFIED (exact, both lines) |
| CL-025 | `PROJ-002-roadmap-next/decisions/DEC-001-project-creation.md` exists as a counter-example (DEC file in a project-level `decisions/` dir) | Cross-reference | VERIFIED (file exists at cited path) |
| CL-026 | `phase3-skeleton-generation-design.md:159` strips `projects/ tests/ skills/.graveyard .github` | Quoted value | VERIFIED (exact) |
| CL-027 | Same file retains `src/+pyproject.toml+uv.lock`; recommended additional strip list includes `docs/` (:157,168) | Quoted value | VERIFIED (exact) |
| CL-028 | BUG-006 F-002 claims `ADR-EPIC002-001` exists in "PROJ-022... and PROJ-004" | Historical assertion (quoted) | VERIFIED (`BUG-006-adr-naming-evaluation.md:99-101` exact) |
| CL-029 | Research doc corrects F-002 as factually wrong; ID exists only in `PROJ-001-oss-release` | Historical assertion | VERIFIED (`adr-convention-standards-research.md:200` exact) |
| CL-030 | `trade-study.md:341` quote: "I decline to claim >0.75 for a C4 governance flip resting on n=3" | Quoted value | VERIFIED (exact quote) |
| CL-031 | Trade study's single-winner confidence figure is 0.70 | Quoted value | VERIFIED (`trade-study.md:339` "0.70 (moderate)") |
| CL-032 | `BUG-006-c4-tournament-review.md:37` documents the `ADR-EPIC002-001` collision finding | Historical assertion | VERIFIED (exact — but see CV-002: this line documents *discovery*, not *resolution*) |
| CL-033 | `BUG-006-c4-tournament-review.md:158` cites `quality-enforcement.md` lines 108,275,290,350 for the collision | Cross-reference | VERIFIED (exact; independently triangulates CL-006) |
| CL-034 | Collision "resolved by renaming to `ADR-EPIC002-002`" | Historical assertion | **MATERIAL DISCREPANCY — see CV-002** |
| CL-035 | `advocate-external.md:126`: repo has 66 local branches | Quoted value | VERIFIED (exact) |
| CL-036 | `advocate-external.md:130`: 16 `{slug}-YYYYMMDD-NNN` orchestration-dir instances across 9+ projects | Quoted value | VERIFIED (exact) |
| CL-037 | `advocate-domain-slug.md:125` originally reported "1 of EPIC-002's 2 ADRs" (pre-correction figure) | Quoted value | VERIFIED (exact — and the ADR's own reconciliation of this figure to "1-of-3" is itself accurate per CL-009/on-disk state) |
| CL-038 | HARD-rule ceiling is 25/25, zero headroom | Rule citation | VERIFIED (`quality-enforcement.md` "Current count: 25 HARD rules... Zero headroom") |
| CL-039 | Ceiling exception mechanism: max +3, one concurrent, 3-month reversion | Rule citation | VERIFIED (`quality-enforcement.md` Exception Mechanism table, exact) |
| CL-040 | S-014 dimension weights: 0.20/0.20/0.20/0.15/0.15/0.10 | Rule citation | VERIFIED (`quality-enforcement.md` Quality Gate table, exact) |
| CL-041 | `CLAUDE.md:53-56` Navigation table already lists `.context/rules/*` files | Cross-reference | VERIFIED (exact) |
| CL-042 | `AGENTS.md:1` is "Registry of Available Specialists" (agent-persona registry, not a rule-file registry) | Quoted value | VERIFIED (exact) |
| CL-043 | `ADR-STORY015-001` carries no `scope:`/YAML frontmatter field | Behavioral claim | VERIFIED (file opens with a blockquote header, no YAML block) |
| CL-044 | `scripts/lint_adr_convention.py`, `adr-lint-waivers.yaml`, `adr-grandfather-allowlist.txt` do not exist ("DESIGNED, NOT BUILT") | Behavioral claim | VERIFIED (all 3 Globs return nothing) |
| CL-045 | `docs/design/README.md` and `docs/adrs/README.md` do not exist | Behavioral claim | VERIFIED (both Globs return nothing) |
| CL-046 | Zero worktracker Task/GH Issue entities exist for any Migration-Plan row | Behavioral claim | VERIFIED (PROJ-031 `work/` tree contains only unrelated EPIC-001-skeleton-distribution tasks; none reference the ADR-convention migration items) |

**Out of this reviewer's verification scope (UNVERIFIABLE — tool constraint, not counted as false):** 8 cited git commit hashes (`41539073`, `5ef0b2fa`, `9b36bda2`, `03e12674`, `cf522abb`, `ab827f3f`, `53ec37b5`, `12b5148a`) could not be independently confirmed — this reviewer's toolset (Read/Write/Edit/Glob/Grep/WebSearch/WebFetch) has no `git log`/Bash access. These are flagged as unverified-by-this-reviewer, not as false; the surrounding file-content claims they support (e.g., current ADR filenames, frontmatter contents) were independently verified via direct file reads above.

---

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260702-i3 | "~6 grammar-family instances across the file, not the '10' the finding first estimated; corrected per P-022" (ADR Migration Plan M-12, and identical text in rule-draft F3-b) | `skills/problem-solving/agents/ps-architect.md` | Independent `Grep` count of the `{ps_id}-{entry_id}-adr-{slug}` / instantiated-example filename grammar finds **exactly 10 occurrences** (lines 65, 81, 260, 268, 480, 482, 497, 500, 503, 506) — matching the *original* "10" estimate the deliverable claims is an overcount, not the "corrected ~6" | Major | Evidence Quality, Actionability |
| CV-002-20260702-i3 | "the duplicate was caught only by a subsequent C4 tournament review... and resolved by renaming to `ADR-EPIC002-002`" (ADR [Context] section) | `projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md:37,158` | Lines 37/158 document the *discovery* of the collision and (at :168,218,227,265, not cited) a *recommendation* to rename to `ADR-EPIC002-002` — not a confirmed completed resolution. Current on-disk state (independently verified) shows the file is `docs/design/ADR-output-path-resolution-001.md` (domain-slug name), and `ADR-EPIC002-002` is now the ID of a **different, unrelated** ADR (`ADR-EPIC002-002-enforcement-architecture.md`, cited from `quality-enforcement.md` References). The deliverable's own [Related Decisions] and Promotion-Frequency-Sensitivity sections correctly describe the *actual* resolution (domain-slug rename via commit `41539073`), directly contradicting the [Context] section's "renamed to `ADR-EPIC002-002`" claim within the same document | Major | Internal Consistency, Evidence Quality |

---

## Finding Details

### CV-001-20260702-i3: Grammar-family instance count undercounts the actual defect surface [MAJOR]

**Claim (from deliverable, identical text in both files):** "Output-path grammar (:260, :268, and the example filename occurrences — ~6 grammar-family instances across the file, not the '10' the finding first estimated; corrected per P-022)"

**Source Document:** `skills/problem-solving/agents/ps-architect.md`

**Independent Verification:** `Grep` for the `{ps_id}-{entry_id}-adr-{slug}` filename grammar (and its instantiated forms, e.g. `work-024-e-202-adr-event-sourcing.md`) across the file returns exactly 10 matches:
- Line 65: `Read(file_path="projects/${JERRY_PROJECT}/decisions/work-024-e-201-adr-hexagonal.md")`
- Line 81: `Write(file_path="projects/${JERRY_PROJECT}/decisions/work-024-e-202-adr-event-sourcing.md", ...)`
- Line 260: `projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-{slug}.md` (the grammar definition itself)
- Line 268: identical grammar, inside the `link-artifact` bash example
- Line 480: `Create file at: projects/${JERRY_PROJECT}/decisions/work-024-e-202-adr-event-sourcing.md`
- Line 482: `python3 scripts/cli.py link-artifact ...` referencing the same path
- Line 497: `ls projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-*.md`
- Line 500: `grep ... projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-*.md`
- Line 503: `grep ... projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-*.md`
- Line 506: `grep ... projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-*.md`

**Discrepancy:** The deliverable's "corrected per P-022" figure (~6) is *further* from ground truth than the estimate it claims to be correcting (10) — the raw occurrence count is 10, exactly matching the "first estimate" the correction dismisses. Even grouping by distinct code-block "location" (Tool-Invocation-Examples ×2, MANDATORY-PERSISTENCE-spec ×2, example-invocation ×2, post-completion-verification ×4 = 4 locations) does not produce 6 by any obvious counting convention.

**Severity:** Major — this is a self-referential P-022 "correction" that is itself inaccurate. It does not invalidate the ADR's core decision, but it risks Migration-Plan item M-12 (fixing `ps-architect.md`) being scoped against an undercount, potentially leaving 4+ of the 10 non-compliant filename-grammar instances unfixed if a future implementer trusts "~6" over checking the file directly.

**Dimension:** Evidence Quality (0.15) — a quantitative claim presented as independently verified is not; Actionability (0.15) — M-12's remediation scope may be under-specified.

**Correction:** Change "~6 grammar-family instances" to "10 grammar-family instances (lines 65, 81, 260, 268, 480, 482, 497, 500, 503, 506)" in both the ADR (Migration Plan M-12 row) and the rule draft (F3-b row), or explicitly justify a different (documented) counting convention that legitimately yields 6.

---

### CV-002-20260702-i3: Internally-inconsistent claim about how the ADR-EPIC002-001 collision was resolved [MAJOR]

**Claim (from deliverable, [Context] section):** "the duplicate was caught only by a subsequent C4 tournament review — *not* prevented 'by construction' — and resolved by renaming to `ADR-EPIC002-002` (`projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md:37,158`; the pre-existing ID is cited from `.context/rules/quality-enforcement.md:108,275,290,350`)."

**Source Document:** `projects/PROJ-030-bugs/reviews/BUG-006-c4-tournament-review.md`

**Independent Verification:**
- Line 37: "CC-003 / CV-001 / FM-014: ADR ID `ADR-EPIC002-001` collides with the existing strategy-selection ADR already referenced in `quality-enforcement.md`" — documents the *finding*, not a resolution.
- Line 158: documents the same discrepancy (with an accurate line-number cross-check to `quality-enforcement.md:108,275,290,350` — this portion of the claim is independently corroborated and correct).
- Lines 168, 218, 227 (not cited by the deliverable) contain the actual "rename to `ADR-EPIC002-002`" text, but framed as a *recommendation* ("Resolve the ADR ID collision (rename to `ADR-EPIC002-002`)"), not a confirmed completed action.
- Current on-disk state: `docs/design/ADR-output-path-resolution-001.md` exists (domain-slug name, `Parent: EPIC-002`); **no file named `ADR-EPIC002-002-*` output-path file exists.** Instead, `ADR-EPIC002-002` is the identifier of a **different, unrelated** ADR: `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-002-enforcement-architecture.md` (itself cited from `quality-enforcement.md` References table as "5-layer enforcement architecture, token budgets").

**Discrepancy:** The deliverable's [Context] section states the collision was resolved by renaming to `ADR-EPIC002-002`, but the deliverable's *own* [Related Decisions] table and [Promotion-Frequency Sensitivity] section state — correctly, and consistent with the verified on-disk state — that the same file was renamed to a domain-slug ID (`ADR-output-path-resolution-001`, commit `41539073`, "which renamed all three framework ADRs to domain slugs"). These two claims about the *same historical event* are mutually exclusive and appear in the same document. The [Context] section's specific claim is the one that does not match current reality, and citing "`ADR-EPIC002-002`" as the resolved identity is additionally hazardous because that exact ID is now legitimately occupied by a third, unrelated ADR — a reader who searches for "the renamed output-path ADR" under `ADR-EPIC002-002` would find the wrong document. This is precisely the citation-integrity failure class this ADR exists to prevent.

**Severity:** Major — does not invalidate the ADR's Scheme B decision (which is independently supported by the verified corpus evidence elsewhere in the package), but it is a genuine internal-consistency defect (two contradictory resolution narratives for one event) plus a stale/incorrect citation of a now-collided identifier, in a C4 document whose central thesis is citation-integrity.

**Dimension:** Internal Consistency (0.20) — direct self-contradiction between [Context] and [Related Decisions]/[Promotion-Frequency Sensitivity]; Evidence Quality (0.15) — the cited source lines document a recommendation, not the claimed resolution.

**Correction:** In the [Context] section, replace "resolved by renaming to `ADR-EPIC002-002`" with the verified resolution: "resolved via the same BUG-006 domain-slug renaming commit (`41539073`) that produced `ADR-output-path-resolution-001` — the C4 tournament review's interim recommendation to rename to `ADR-EPIC002-002` was superseded by the broader 3-ADR domain-slug remediation, and `ADR-EPIC002-002` is now a distinct, legitimately-issued ADR (`ADR-EPIC002-002-enforcement-architecture`)." This also strengthens the ADR's own argument (the eventual fix was in fact domain-slug renaming, further corroborating Scheme B).

---

## Verification Ratios

| Result | Count | Percentage |
|--------|-------|------------|
| VERIFIED | 44 | 95.7% |
| MATERIAL DISCREPANCY | 2 | 4.3% |
| UNVERIFIABLE (false) | 0 | 0% |
| Out of reviewer's tool scope (commit hashes, not counted in ratio) | 8 | — |

**Verification rate: 44/46 = 95.7%.** Zero fabrication-class (Critical) findings. Both discrepancies are historical/self-correction narrative errors, not structural defects in the proposed convention itself.

---

## Recommendations

**Major (SHOULD correct before ratification):**
1. **CV-001-20260702-i3:** Correct "~6 grammar-family instances" to "10" (or a documented, defensible alternative count) in both the ADR (Migration Plan M-12) and the rule draft (F3-b), citing the exact line numbers.
2. **CV-002-20260702-i3:** Correct the [Context] section's "resolved by renaming to `ADR-EPIC002-002`" claim to match the verified on-disk resolution (domain-slug rename to `ADR-output-path-resolution-001`), and reconcile it with the already-correct [Related Decisions]/[Promotion-Frequency Sensitivity] narrative so the document is internally consistent.

**Minor (MAY correct):** None identified beyond the two Major items — the remaining 44 verified claims required no correction.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Claim coverage is exhaustive across the required categories (quoted values, rule citations, cross-references, historical assertions, behavioral claims); no category was left unchecked |
| Internal Consistency | 0.20 | Negative | CV-002-20260702-i3: direct self-contradiction between the [Context] section and the [Related Decisions]/[Promotion-Frequency Sensitivity] sections regarding how the same historical collision was resolved |
| Methodological Rigor | 0.20 | Positive | The deliverable's own iterative P-022 correction discipline (verified against multiple independent sources: research doc, advocate docs, trade study, BUG-006 files, live filesystem state) is unusually rigorous and mostly self-consistent |
| Evidence Quality | 0.15 | Negative | CV-001-20260702-i3 and CV-002-20260702-i3 both involve quantitative/historical claims that do not hold up under independent verification, undermining confidence in adjacent unverified claims (e.g., the 8 commit hashes this reviewer could not check) |
| Actionability | 0.15 | Negative | CV-001-20260702-i3 risks under-scoping Migration-Plan item M-12's remediation work if the "~6" figure is trusted over direct inspection |
| Traceability | 0.10 | Positive | Every claim checked in this review carried an exact, resolvable file+line citation; the overwhelming majority (44/46) resolved to precisely the claimed content on independent re-derivation |

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 0
- **Major:** 2
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5 (Extract Claims, Generate Verification Questions, Independent Verification, Consistency Check, Synthesize and Score Impact)
- **Claims Extracted:** 46 (exceeds the minimum 5 required by the protocol)
- **Verification Rate:** 44/46 = 95.7%
- **Recommendation:** REVISE (two Major findings should be corrected; core decision unaffected)

---

*Report complete. All sections above are final — no further sections pending.*

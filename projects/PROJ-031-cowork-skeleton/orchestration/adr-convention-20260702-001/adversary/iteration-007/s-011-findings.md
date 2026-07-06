# Chain-of-Verification Report: ADR-PROJ031-004 + Companion Rule Draft (Post-Subtraction Package, Iteration 7)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, criticality |
| [Summary](#summary) | Overall assessment |
| [Claim Inventory](#claim-inventory) | Extracted testable claims (CL-NNN) |
| [Verification Questions & Independent Verification Results](#verification-questions--independent-verification-results) | VQ-NNN, source-only answers |
| [Findings](#findings) | CV-NNN discrepancies, severity-classified |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Totals |

---

## Execution Context

- **Strategy:** S-011 Chain-of-Verification
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
- **Criticality:** C4 (REQUIRED per S-011 Identity Criticality Tier Table)
- **Engagement gate:** 0.95
- **Iteration:** 7 (post-subtraction-pass package; subtraction authorized by user FU.1, folded in v1.7/v1.8)
- **Reviewer:** adv-executor (blind, independent — no access to sibling `adversary/iteration-007/` files from other strategies; did not read any file under `adversary/` other than this output, per blind protocol)
- **Date:** 2026-07-06
- **H-16 status:** Indirect for CoVe (per S-011 template); no S-003 output supplied in this invocation's context — noted, not treated as a defect (S-011 Prerequisites explicitly permits this).

---

## Summary

Post-subtraction package (ADR-PROJ031-004 + companion rule draft) was independently re-verified against source: `FEEDBACK-LOG.md`, live repo filesystem state (Glob/Grep), `skills/problem-solving/agents/ps-architect.md`, `docs/design/`, `docs/archive/`, `docs/adrs/`, PROJ-007 artifacts, `pyproject.toml`, `skills/ast/SKILL.md`, `skills/architecture/SKILL.md`, and the exemplar ADR template. **39 distinct testable claims were extracted and independently checked; 37 verified exactly against source, 2 discrepancies found — both self-referential to the rule draft's own line/token-count bookkeeping, neither touching the substantive Scheme-B decision or the lint's grammar/collision logic.** Verification rate: 37/39 ≈ 94.9%. The hit-rate — including eleven separately-cited exact line numbers in a third-party file (`ps-architect.md`) all confirmed letter-for-letter, and a repo-wide dialect-ADR recount (16 total, 18 grandfather-scan-reachable) that matched the deliverable's own figures exactly — indicates the prior six iterations' fact-checking discipline held up under independent blind re-verification.

**Recommendation: REVISE (targeted, not structural).** Correct CV-001 (Major — reconcile the rule draft's own line/token count, currently asserted as three different numbers across the two-document package) before the next gate measurement. CV-002 (Minor) is a clarity nit, not a factual error, and is optional to fix.

---

## Claim Inventory

| CL | Claim (paraphrased) | Deliverable location | Type |
|----|----|----|----|
| CL-001 | FU.0 verbatim quote "I ratify the promotion-is-the-point apporach and lock Scheme B." | ADR Status/Decision; subtraction-notes Step 1 | Historical assertion |
| CL-002 | `.claude/rules -> ../.context/rules` is a directory-level symlink | ADR M-2b | Behavioral claim |
| CL-003 | `scripts/lint_adr_convention.py` does not exist (Glob-verified) | ADR Enforcement Claim-Status; rule draft L5 spec | Cross-reference |
| CL-004 | `.github/workflows/ci.yml:2` cites `projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`, and that project path no longer exists | ADR Context (9th family) | Quoted value / cross-reference |
| CL-005 | quality-enforcement.md cites `ADR-EPIC002-001` at lines 108, 275, 290, 350 | ADR (implicit, via SSOT dependency) | Cross-reference |
| CL-006 | Dialect ADR corpus = 16 total: PROJ010×6, PROJ022×2, PROJ031×4, EPIC002×2, STORY015×1, 150×1 | ADR D-4, Context table | Quoted value |
| CL-007 | Grandfather regression scope = 18 files (15 dialect reachable via `projects/*/decisions/` + 3 canonical `docs/design/`) | ADR/rule-draft Enforcement Design | Quoted value |
| CL-008 | `ADR-STORY015-001` lives at `work/.../STORY-015.../`, no `decisions/` segment (out-of-scan, R-10) | ADR L1 Technical Implementation, Risks R-10 | Cross-reference |
| CL-009 | Two distinct `BUG-006` entities exist in different directories (`reviews/BUG-006-adr-naming-evaluation.md` vs `work/BUG-006-skill-output-path-hardcoded.md`) | ADR References P-022 disclosure (f) | Cross-reference |
| CL-010 | `docs/knowledge/exemplars/templates/adr.md:1` title placeholder is `# ADR-{NUMBER}: {Title}` | ADR Context, M-3 | Quoted value |
| CL-011 | Same template's Status line (`:6`) offers only `PROPOSED \| ACCEPTED \| DEPRECATED \| SUPERSEDED` (no REJECTED) | Rule draft Status Vocabulary | Quoted value |
| CL-012 | Same template's PS-Integration line (`:182`) cites dangling `docs/decisions/...` path | ADR Context; M-3 | Cross-reference |
| CL-013 | `docs/decisions/` does not exist anywhere in the repo | ADR L1 Technical Implementation ("do not introduce") | Behavioral claim |
| CL-014 | `skills/architecture/SKILL.md` uses underscore grammar `ADR_NNN` at lines 105, 284, 437 | ADR Context, M-4 | Quoted value |
| CL-015 | `ADR-agent-design-001.md:3` carries origin via an HTML comment (`PS-ID: PROJ-007 \| ENTRY: e-004`) | ADR Migration Plan, L1 Technical Implementation | Quoted value |
| CL-016 | `ADR-routing-triggers-001.md:3` likewise carries origin via HTML comment | ADR Migration Plan | Quoted value |
| CL-017 | `ADR-output-path-resolution-001.md:8` carries origin via blockquote `**Parent:** EPIC-002` | ADR Migration Plan, L1 Technical Implementation | Quoted value |
| CL-018 | None of the 3 canonical framework ADRs carry the proposed YAML frontmatter schema | ADR Migration Plan row 1 | Behavioral claim |
| CL-019 | `.context/rules/` contains exactly 17 `.md` files | ADR/rule-draft L1-budget note; M-7 (CC-001 iter-4) | Quoted value |
| CL-020 | Of those 17, exactly 3 are individually named in CLAUDE.md's Navigation table (quality-enforcement.md, agent-development-standards.md, agent-routing-standards.md) — "≈18%" | ADR M-7 | Quoted value |
| CL-021 | `skills/problem-solving/agents/ps-architect.md:218` = non-canonical title `# ADR-{NUMBER}: {Title}` | ADR M-12 | Quoted value |
| CL-022 | Same file `:250,:251` = PS-ID/Entry-ID input labels | ADR M-12 | Quoted value |
| CL-023 | Same file `:260,:268,:497,:500,:503,:506` (6 lines) = non-canonical `{ps_id}-{entry_id}-adr-{slug}` filename grammar | ADR M-12 | Quoted value |
| CL-024 | Same file `:263` = phantom path `templates/adr.md` | ADR M-12 | Cross-reference |
| CL-025 | Same file `:267,:482,:509` (3 lines) = phantom `python3 scripts/cli.py` (+ H-05 violation) | ADR M-12 | Behavioral/cross-reference |
| CL-026 | Same file `:480,:482` = literal example filename `work-024-e-202-adr-event-sourcing.md`; `:482` carries BOTH the phantom CLI and the literal example | ADR M-12 | Quoted value |
| CL-027 | Bare literal paths `templates/adr.md` and `scripts/cli.py` do not exist anywhere in the repo | ADR M-12 | Behavioral claim |
| CL-028 | `pyproject.toml:65` is the `jerry` CLI entrypoint (`src.interface.cli.main:main`) | ADR M-12 ("real CLI is `uv run jerry`, entrypoint `pyproject.toml:65`") | Quoted value |
| CL-029 | `skills/ast/SKILL.md:105` reads "Extract all **blockquote** frontmatter fields as a JSON object" | ADR/rule-draft "Two frontmatter mechanisms coexist" | Quoted value (exact wording) |
| CL-030 | `ORCHESTRATION.yaml:228,242` and `WORKTRACKER.md:106-107` still cite `ADR-PROJ007-001/002` (stale) | ADR Decision-B steelman | Cross-reference |
| CL-031 | `EN-001.md:48-49,72-73` likewise cite `ADR-PROJ007-001/002` (stale; still PENDING status in that file's own task table) | ADR Decision-B steelman | Cross-reference |
| CL-032 | `docs/design/README.md` and `docs/adrs/README.md` do not exist (recommended, never built) | ADR L1 Technical Implementation, References #BUG-006 F-004 | Behavioral claim |
| CL-033 | `.github/PULL_REQUEST_TEMPLATE.md` does not exist | ADR M-9 (FM-010 iter-6) | Behavioral claim |
| CL-034 | `docs/archive/.../decisions/` contains exactly 4 bare `ADR-0NN` files (031-034) | ADR Context corpus table | Quoted value |
| CL-035 | `docs/adrs/` (transcript) contains 6 `ADR-NNN` files + 1 amendment file ("6+1") | ADR Context corpus table | Quoted value |
| CL-036 | PROJ-014 contains exactly 4 bare `ADR-001..004` orchestration drafts | ADR D-4, Migration Plan | Quoted value |
| CL-037 | `ADR-OSS-NNN` family has exactly 7 members; `adr-cli-integration.md` and `adr-cli-integration-v2.md` both exist | ADR Context corpus table, Options-F steelman | Quoted value |
| CL-038 | The rule draft's own current line/token count is a single, internally consistent figure | Rule draft Changelog v1.7/v1.8; L5-spec descoped note; `subtraction-pass-notes.md` Files Edited | **Self-referential quoted value** |
| CL-039 | M-14's "14 pre-existing" / "15 incl. this ADR" / "15 pre-existing dialect ADRs" figures are mutually reconcilable | ADR M-14 | Quoted value (multi-referent) |

---

## Verification Questions & Independent Verification Results

All questions answered by reading the cited source directly (Read/Glob/Grep), without re-reading the deliverable's characterization first.

| VQ | Question | Independent Answer (source-only) |
|----|----|----|
| VQ-001 | What does FEEDBACK-LOG.md FU.0 actually say, verbatim? | `FEEDBACK-LOG.md:31`: "I ratify the promotion-is-the-point apporach and lock Scheme B." — **exact match**, typo (`apporach`) preserved as claimed. |
| VQ-002 | Does `.claude/rules/quality-enforcement.md` resolve to the same content as `.context/rules/quality-enforcement.md`? | Yes — direct `Read` of `.claude/rules/quality-enforcement.md` returns identical header/content to `.context/rules/quality-enforcement.md` (VERSION 1.6.0 banner). Symlink resolves. (Note: `Glob` on `.claude/rules/*` returns no matches — a tool-level non-traversal of the symlinked directory, not evidence against the claim, since direct `Read` through the same path succeeds.) |
| VQ-003 | Does `scripts/lint_adr_convention.py` exist? | `Glob scripts/*.py` lists 20 scripts; `lint_adr_convention.py` is **not** among them. Confirmed absent. |
| VQ-004 | What is at `.github/workflows/ci.yml:2`, and does `projects/PROJ-001-plugin-cleanup` exist? | Line 2: `# ADR: projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md` — exact match. `Glob projects/PROJ-001-plugin-cleanup` returns no matches — project confirmed gone; citation confirmed dangling. |
| VQ-005 | What do quality-enforcement.md lines 108/275/290/350 contain? | All four lines cite `ADR-EPIC002-001-strategy-selection.md` by full path — exact match. |
| VQ-006 | How many dialect ADR files actually exist, broken out by family? | `Glob projects/*/decisions/ADR-*.md` → PROJ010×6, PROJ022×2, ADR-150×1, PROJ031×4 (incl. this ADR), EPIC002×2 = 15. Plus `ADR-STORY015-001` (found only via repo-wide glob, confirmed NOT under any `decisions/` dir) = 16 total. **Exact match** to claimed "16 dialect ADRs." |
| VQ-007 | How many files are reachable by `projects/*/decisions/` + `docs/design/`? | 15 (dialect, per VQ-006 minus STORY015) + 3 (`docs/design/ADR-agent-design-001.md`, `ADR-output-path-resolution-001.md`, `ADR-routing-triggers-001.md`) = **18. Exact match.** |
| VQ-008 | Where does `ADR-STORY015-001` actually live? | `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md` — no `decisions/` segment. **Exact match**, out-of-scan confirmed. |
| VQ-009 | Are there two distinct BUG-006 files in different subtrees? | `Glob projects/PROJ-030-bugs/**/BUG-006*` confirms `reviews/BUG-006-adr-naming-evaluation.md` and `work/BUG-006-skill-output-path-hardcoded.md` as separate files in separate subdirectories. **Exact match.** |
| VQ-010 | What is at `docs/knowledge/exemplars/templates/adr.md` lines 1, 6, 182? | L1: `# ADR-{NUMBER}: {Title}`. L6: `> **Status:** PROPOSED \| ACCEPTED \| DEPRECATED \| SUPERSEDED` (no REJECTED). L182: `link-artifact {PS_ID} {ENTRY_ID} FILE "docs/decisions/..."`. **All three exact matches.** `Glob docs/decisions/**` confirms the directory does not exist anywhere. |
| VQ-011 | What is at `skills/architecture/SKILL.md` lines 105, 284, 437? | L105: `` `docs/design/ADR_NNN_*.md` ``. L284: `` **Creates:** `docs/design/ADR_001_sqlite_persistence.md` `` (instantiated example, underscore form). L437: `` `docs/design/ADR_NNN_*.md` ``. **All three support the underscore-mismatch claim** (284 is an instantiated example rather than the literal placeholder, but the underscore convention is present exactly as characterized). |
| VQ-012 | What do lines 3 of `ADR-agent-design-001.md` / `ADR-routing-triggers-001.md`, and line 8 of `ADR-output-path-resolution-001.md` contain? | `ADR-agent-design-001.md:3`: `<!-- PS-ID: PROJ-007 \| ENTRY: e-004 \| AGENT: ps-architect-001 \| DATE: 2026-02-21 -->`. `ADR-routing-triggers-001.md:3`: `<!-- VERSION: 1.2.0 \| ... \| PS-ID: PROJ-007 \| AGENT: ps-architect-002 ... -->`. `ADR-output-path-resolution-001.md:8`: `> **Parent:** EPIC-002`. **All three exact matches**; none of the 3 canonical ADRs carries a YAML `---` frontmatter block (confirmed by reading each file's first ~10 lines). |
| VQ-013 | How many `.md` files are in `.context/rules/`, and how many are individually named in CLAUDE.md's Navigation table? | `Glob .context/rules/*.md` returns **exactly 17** files. CLAUDE.md's Navigation table individually names exactly 3 of them (`quality-enforcement.md`, `agent-development-standards.md`, `agent-routing-standards.md`); the rest are covered by the generic `.context/rules/ (A)` row. 3/17 ≈ 17.6%. **Exact match to "3 (~18%)."** |
| VQ-014 | Do `ps-architect.md` lines 218/250/251/260/263/267/268/480/482/497/500/503/506/509 contain what the ADR's M-12 row claims, line-for-line? | All 11 distinct line numbers checked directly: 218 (bare `# ADR-{NUMBER}` title), 250/251 (PS ID/Entry ID labels), 260 (`{ps_id}-{entry_id}-adr-{slug}.md` grammar), 263 (`templates/adr.md`), 267 (`python3 scripts/cli.py ...`), 268 (grammar continuation), 480 (`work-024-e-202-adr-event-sourcing.md` literal example), 482 (BOTH `python3 scripts/cli.py` AND the literal example filename on the same line — exactly as the ADR's parenthetical notes), 497/500/503/506 (grammar in verification commands), 509 (`python3 scripts/cli.py view ...`). **Every single one of the 11 cited lines matches exactly**, including the unusual double-attribution claim at `:482`. |
| VQ-015 | Do bare paths `templates/adr.md` and `scripts/cli.py` exist? | `Glob templates/adr.md` → no matches. `Glob scripts/cli.py` → no matches. **Both confirmed phantom**, as claimed. |
| VQ-016 | What is at `pyproject.toml:65`? | `jerry = "src.interface.cli.main:main"` under `[project.scripts]`. **Exact match** to the "entrypoint pyproject.toml:65" claim. |
| VQ-017 | What is the exact wording at `skills/ast/SKILL.md:105`? | "Extract all blockquote frontmatter fields as a JSON object." **Exact match**, including the "blockquote"-only scoping the ADR leans on for its YAML-vs-blockquote dual-parser disclosure. |
| VQ-018 | Do `ORCHESTRATION.yaml:228,242`, `WORKTRACKER.md:106-107`, `EN-001.md:48-49,72-73` cite `ADR-PROJ007-001/002`? | `ORCHESTRATION.yaml:228`: "ADR-PROJ007-001: Agent definition format..."; `:242`: "ADR-PROJ007-002: Layered routing framework...". `WORKTRACKER.md:106-107`: "Install ADR-PROJ007-001 ... DONE" / "Install ADR-PROJ007-002 ... DONE". `EN-001.md:48-49`: install-target rows naming `ADR-PROJ007-001`/`002` at `docs/design/ADR-PROJ007-00{1,2}-*.md`; `:72-73`: `TASK-014`/`TASK-015`, both status **PENDING** in this file's own table. **All line numbers match exactly**; the still-live bare-ID citations are confirmed present today. |
| VQ-019 | Do `docs/design/README.md`, `docs/adrs/README.md`, `.github/PULL_REQUEST_TEMPLATE.md` exist? | All three: `Glob` → no matches. **All three confirmed absent**, as claimed. |
| VQ-020 | How many files are in `docs/archive/.../decisions/` (bare `ADR-0NN`) and `docs/adrs/` (transcript)? | Archive: exactly 4 (`ADR-031` through `ADR-034`). Transcript: 6 `ADR-NNN` files + `ADR-001-amendment-001` = 7. **Exact match to "4" and "6+1."** |
| VQ-021 | How many `ADR-001..004` bare files exist under PROJ-014, and how many `ADR-OSS-NNN` files exist, and do both `adr-cli-integration.md`/`-v2.md` exist? | PROJ-014: exactly 4 (`ADR-001` through `ADR-004`). `ADR-OSS-NNN`: exactly 7 (`001`-`007`). Both `adr-cli-integration.md` and `adr-cli-integration-v2.md` exist. **All exact matches.** |
| VQ-022 | What is the rule draft's own current, single authoritative line/token count for itself? | Three different figures appear in the two-document package: (a) rule draft Changelog v1.7 row (`:235`, unedited prose retained through v1.8): "**233 lines**"; (b) rule draft's own L5-spec descoped note (`:196`, itself part of the v1.8 edit, per the v1.8 changelog's own "L1-aggregate budget note (CC-002)" credit): "**238 lines**"; (c) `subtraction-pass-notes.md` Files Edited section: "rewritten slim (233 lines ... at the subtraction pass; **grew to 240 lines** ... under the iter-6 overclaim-correction pass)". Independent direct measurement (Read, cat-n-style line numbering): file content runs through line 238 (footer note), with a trailing blank line at 239 — i.e., **≈238-239 by direct count**, not 233, and not exactly 240. **No two of the three cited figures agree, and none matches the independent measurement exactly** (238 from the in-document note is closest). |
| VQ-023 | Are M-14's "14 pre-existing," "15 incl. this ADR," and "15 pre-existing dialect ADRs" the same quantity? | Independently reconstructed via VQ-006: reachable-via-`decisions/`-folder pre-existing set = 14 (PROJ010×6+PROJ022×2+PROJ031×3[pre-existing]+EPIC002×2+ADR-150×1); +this in-flight ADR = 15 (first sense). Whole pre-existing dialect corpus (incl. out-of-scan STORY015) = 15 (second sense); minus STORY015 = 14. **Arithmetically self-consistent** once disambiguated — but the sentence uses "15" for two different populations (one includes this in-flight ADR and excludes STORY015; the other excludes this in-flight ADR and includes STORY015) within a single sentence, with only the parenthetical SM-102 note available to disambiguate. |

---

## Findings

### CV-001-20260706T1: Rule Draft's Self-Reported Line/Token Count Is Internally Inconsistent Across Three Citations, None Matching Independent Measurement [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `adr-standards-rule-draft.md` Changelog (`:235`-`:236`) and L5-spec descoped note (`:196`); `subtraction-pass-notes.md` "Files Edited" |
| **Strategy Step** | Step 4 (Consistency Check) |

**Claim (from deliverable):**
1. Rule draft Changelog v1.7 entry (retained verbatim through v1.8, `adr-standards-rule-draft.md:235`): "token budget ~10.3k→**~3.3k** (**233 lines**; `wc -w`×1.35 measured...)".
2. Rule draft v1.8 Changelog entry (`:236`) lists among its own edits: "...line count corrected 232→**233** (CC-003)." — presented as the current, corrected figure, in the same bullet list that credits the v1.8 pass with adding the "L1-aggregate budget note (CC-002)."
3. That very L1-aggregate budget note, added by the same v1.8 pass (`:196`): "this file's ~3.9k tokens (**238 lines**) is comparable to other substantive rule files..."
4. Companion `subtraction-pass-notes.md` "Files Edited" section: "rewritten slim (233 lines / ~3.25k tokens measured at the subtraction pass; **grew to 240 lines** / ~3.9k tokens under the iter-6 overclaim-correction pass...)".

**Independent Verification:** Direct `Read` of `adr-standards-rule-draft.md` (cat-n-style line numbering, ground truth) shows content through line 238 (`*Proposed home on ratification...*`) followed by a blank line 239 at end-of-file — i.e., the file is **not** 233 lines by any count method consistent with the document's own prior methodology (it previously computed "wc -l=232 newlines, final line unterminated → 233 content lines" for the *prior* version — the same reasoning applied now yields a figure in the 238-239 range, not 233).

**Discrepancy:** Three numbers (233, 238, 240) are asserted for the same fact — the current line count of one specific, small, precisely-tracked file — within a two-document package whose entire enforcement narrative rests on "the number is stated, not rounded down" (P-022 self-description, `subtraction-pass-notes.md:73`). The v1.8 Changelog bullet ("232→233... corrected") is stale at the moment it was written: the *same* v1.8 pass that wrote it also added the 238-line-referencing L1-budget note two lines earlier in the same file, without reconciling the two. Of the three cited numbers, 238 (the in-document, most-recently-added figure) is closest to independent measurement; 233 (the Changelog's headline "corrected" figure) is the most stale; 240 (the companion notes file) is a third, unreconciled data point. This is precisely the class of self-referential numeric drift the S-011 protocol exists to catch, and precisely the class of claim this deliverable otherwise treats with unusual rigor (e.g., the DA-003 "13 of 18" reconciliation, the CC-003 "232→233" correction itself, the VQ-006/VQ-007 dialect-count reconciliations verified clean above).

**Severity Rationale:** Major, not Critical — it does not invalidate Scheme B, does not violate a HARD rule, and does not affect enforceability (the lint's grammar/collision logic is unaffected by the rule draft's own line count). It is Major because: (a) it is a directly falsifiable claim about the package's own artifact that a careful reader can catch in under a minute, undermining confidence in the surrounding budget-compliance narrative (the "~30% above target, honestly disclosed" framing in `subtraction-pass-notes.md:73` is itself now built on a stale sub-figure); (b) it recurs across BOTH deliverables (the rule draft and its companion notes file), so it is not a single typo but an unreconciled cross-document drift; (c) at C4/0.95 engagement gate, self-referential precision claims are exactly what CoVe is tasked to hold to the same evidentiary standard the document demands of everything else it cites.

**Dimension:** Internal Consistency (primary), Evidence Quality (secondary — the "measured, not rounded" claim is undercut by an unreconciled measurement).

**Correction:** Re-run the line/word count on the CURRENT `adr-standards-rule-draft.md` (post all v1.8 edits) using the document's own established method (`wc -l` + unterminated-final-line check, `wc -w`×1.35 for tokens), then (a) update the L5-spec descoped note (`:196`) and the v1.8 Changelog entry (`:236`) to cite the SAME freshly-measured figure, and (b) update `subtraction-pass-notes.md`'s "Files Edited" line to match. Do not leave the v1.7 Changelog row's historical "233" uncorrected-in-context — either add a one-clause note that v1.8 grew the file further (to the freshly measured figure), or move the growth acknowledgment out of the "corrected 232→233" clause so it does not read as the current authoritative count.

---

### CV-002-20260706T1: M-14's "15" Is Used for Two Different Quantities in One Sentence [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR Migration Plan, M-14 row |
| **Strategy Step** | Step 4 (Consistency Check) |

**Claim (from deliverable):** "...14 pre-existing project-level ADRs (**15** incl. this in-flight ADR; across PROJ-001/-010/-022/-030/-031) occupy exactly that undocumented folder (FM-016; SM-102 count reconciliation: 14 = the **15** pre-existing dialect ADRs minus the one entity-embedded STORY015 ADR that is not in a `decisions/` dir)."

**Independent Verification:** Reconstructed independently via VQ-006/VQ-023: the reachable-via-`decisions/`-folder set is 14 pre-existing + this ADR = 15 (first "15"). The whole pre-existing dialect corpus including the out-of-scan `STORY015` entity-embedded ADR is a *different* set of 15 (second "15"), of which 14 are folder-reachable. Both quantities independently check out to 15 — the arithmetic is NOT wrong — but the same numeral is used for two different populations (one includes this in-flight ADR and excludes STORY015; the other excludes this in-flight ADR and includes STORY015) within a single sentence, with only the parenthetical SM-102 note available to disambiguate.

**Discrepancy:** Not a factual error — both computations independently verify to 15 — but a readability/traceability defect: a reader (or a future CoVe pass, as this one initially had to do) must reconstruct two disjoint 15-item sets from context to confirm the sentence is self-consistent rather than assume a typo.

**Severity Rationale:** Minor. No downstream decision depends on disambiguating the two 15s; the SM-102 label signals "this was already reconciled once," and independent reconstruction confirms the reconciliation holds.

**Dimension:** Traceability.

**Correction:** Label the two quantities distinctly, e.g., "...(**15 reachable** incl. this in-flight ADR...) ...(14 = the **15 pre-existing (whole corpus)** dialect ADRs minus STORY015)." A one-word qualifier on each "15" removes the ambiguity without adding a new claim.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No claims found unaddressed; the package discloses its own residuals extensively. |
| Internal Consistency | 0.20 | Negative | CV-001: three unreconciled figures for the same self-referential fact, one of which (233) is presented as "corrected" while already stale relative to its own edit pass. |
| Methodological Rigor | 0.20 | Positive | 37 of 39 independently-checked claims verified exactly, including eleven separately-cited exact line numbers in a third-party file (`ps-architect.md`) all confirmed letter-for-letter — evidence of genuinely rigorous prior fact-checking, not restated assertion. |
| Evidence Quality | 0.15 | Negative (minor) | CV-001 undercuts the "measured, not rounded" self-characterization at exactly the fact it is proudest of measuring precisely. |
| Actionability | 0.15 | Positive | Both findings have a one-clause, mechanically specific correction (re-measure and reconcile; add a qualifier word). |
| Traceability | 0.10 | Negative (minor) | CV-002: dual use of "15" costs independent-verification effort though it is not wrong. |

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 0
- **Major:** 1 (CV-001)
- **Minor:** 1 (CV-002)
- **Claims Extracted:** 39 (CL-001 through CL-039)
- **Verification Questions:** 23 (VQ-001 through VQ-023, several covering multiple claims)
- **Verified Exact / No Discrepancy:** 37 of 39 claims (94.9%)
- **Protocol Steps Completed:** 5 of 5 (Extract Claims, Generate Verification Questions, Independent Verification, Consistency Check, Synthesize and Score Impact)
- **H-16 status:** Indirect for CoVe (per S-011 template); not blocking. No S-003 output was supplied in this invocation's context; gap noted, not treated as a defect (S-011 Prerequisites: "Acceptable: S-011 without prior S-003").
- **Blind protocol compliance:** No files under `adversary/` were read other than this report. Deliverables were not edited (owner-only edit rights respected, P-020).

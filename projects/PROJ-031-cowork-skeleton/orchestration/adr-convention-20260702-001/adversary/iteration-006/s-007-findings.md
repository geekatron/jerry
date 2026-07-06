# Constitutional Compliance Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 6, Post-Subtraction)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-05
**Reviewer:** adv-executor (S-007, iteration 6, blind independent reviewer)
**Constitutional Context:** JERRY_CONSTITUTION.md (P-001+ referenced via quality-enforcement.md), quality-enforcement.md HARD Rule Index (H-01–H-36, 25/25 ceiling), Tier Vocabulary (HARD/MEDIUM/SOFT keyword sets), Enforcement Architecture (L1–L5 layers), markdown-navigation-standards.md (H-23), project-workflow.md (H-32)

**Scope note (P-020):** Per the invoking mandate, this iteration evaluates the package **as slimmed by the user-authorized subtraction pass** (FEEDBACK-LOG.md FU.1). Descoping deleted machinery with honest disclosure is treated as a valid MEDIUM-tier design posture, not penalized as a gap. Findings below are limited to (a) residual constitutional/tier-purity issues in the post-subtraction text, and (b) the four check items the orchestrator explicitly named: MEDIUM-tier purity, H-23 nav tables, P-022 claim honesty post-slim-down, P-020 ratification, and L1 token-budget fit.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional compliance assessment |
| [Verified Compliant](#verified-compliant-no-finding) | Claims independently checked and confirmed accurate |
| [Findings Table](#findings-table) | All findings, ID/principle/tier/severity |
| [Finding Details](#finding-details) | Expanded evidence per finding |
| [Recommendations](#recommendations) | Prioritized remediation plan |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping and compliance score |

---

## Summary

**PARTIAL compliance.** 0 Critical, 2 Major, 2 Minor. Constitutional Compliance Score: **0.86 (REVISE band, 0.85–0.91)**. The post-subtraction package is well-verified on its factual claims (ratification, corpus counts, dangling-citation evidence all independently confirmed accurate — see [Verified Compliant](#verified-compliant-no-finding)) and the subtraction itself is legitimate, honestly-disclosed descoping, not penalized. The two Major findings are (1) a residual MEDIUM-tier-purity gap in the rule draft — lowercase HARD-tier-force words ("never", "must") survive outside the 13 numbered `ADR-M-NNN` standards while the changelog claims purity in a narrower sense than stated — and (2) the rule draft's meticulous token-budget accounting never checks itself against the SSOT's own named ~12,500-token L1 aggregate budget, despite being destined for that exact enforcement layer. Recommend targeted revision of both before the C4 engagement gate (0.95).

---

## Verified Compliant (No Finding)

Independently checked during this review (P-011 evidence-based verification); reported for balance, not counted as findings:

| Item | Verification method | Result |
|---|---|---|
| H-23 nav tables (both deliverables) | Manual anchor-resolution check of every `[Section](#anchor)` entry in both "Document Sections" tables against actual `##`/`###` headings | All anchors resolve; both files use Format 1 (Section/Purpose) correctly |
| P-020 ratification quote | Read `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` FU.0 | Verbatim match confirmed: *"I ratify the promotion-is-the-point apporach and lock Scheme B."* — identical to the quote in ADR `Status` (line 85) and Decision (line 213) |
| FU.1 subtraction authorization | Read `FEEDBACK-LOG.md` FU.1 | User quote *"I authorize the subtraction pass. I want us to get to >=0.95..."* confirmed, matching `subtraction-pass-notes.md` framing |
| 16 dialect + 3 canonical = 19-file grandfather corpus | `Glob` for `**/decisions/ADR-*.md` (excl. `docs/archive/`) + `docs/design/ADR-*.md` + targeted `Glob` for `ADR-STORY015-*.md` | 15 files in `decisions/` dirs + 1 entity-embedded (`STORY-015-tier-model-renumbering/ADR-STORY015-001-...md`, confirmed at claimed path) = 16; 3 canonical confirmed in `docs/design/`. Count is accurate. |
| Dangling `ADR-CI-001` citation in `.github/workflows/ci.yml:2` | `Grep` for `ADR` in `.github/workflows/ci.yml`; `Glob` for `projects/PROJ-001-plugin-cleanup` | Citation confirmed verbatim at line 2; referenced project path confirmed non-existent |
| `PERMITTED` pseudo-tier fully removed | `Grep -i PERMITTED` across both live deliverables | Zero live occurrences; sole match is the historical changelog note describing its removal |

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260705-iter006 | c-001 (ADR)/Tier Vocabulary (quality-enforcement.md): rule draft MUST be MEDIUM-tier only | MEDIUM (self-imposed HARD constraint on the artifact) | Major | `adr-standards-rule-draft.md:47,133,144` use lowercase "never" as an unhedged absolute prohibition | Internal Consistency |
| CC-002-20260705-iter006 | Enforcement Architecture L1 budget (quality-enforcement.md, ~12,500 tokens aggregate) | MEDIUM (completeness/rigor gap, no explicit rule violated) | Major | `adr-standards-rule-draft.md` token-budget analysis (`subtraction-pass-notes.md:64-72`) never cross-checks the SSOT's L1 aggregate constant | Completeness |
| CC-003-20260705-iter006 | P-022 (evidence precision) | SOFT | Minor | `subtraction-pass-notes.md:69` claims "232" lines; actual file is 233 lines (`adr-standards-rule-draft.md`, `cat -n` numbering) | Evidence Quality |
| CC-004-20260705-iter006 | P-022 (residual disclosure completeness) | SOFT | Minor | `FEEDBACK-LOG.md:78` (FU.3) discloses a `--no-verify` commit with 24 doc-convention failures on "the new corpus"; not cross-referenced in either deliverable's own residual/risk sections | Traceability |

**Finding ID Format:** `CC-{NNN}-{execution_id}`, execution_id = `20260705-iter006`.

**Severity Definitions:** Critical = violates HARD rule, blocks acceptance per H-13. Major = violates a MEDIUM standard or a self-imposed constitutional constraint the deliverable states for itself; requires revision or documented justification. Minor = improvement opportunity.

---

## Finding Details

### CC-001-20260705-iter006: Residual HARD-tier vocabulary survives in a document self-certified as MEDIUM-tier-pure [MAJOR]

**Principle:** The rule draft's own Tier and Scope section states: *"All standards are MEDIUM-tier (SHOULD/RECOMMENDED, override with documented justification per `.context/rules/quality-enforcement.md` Tier Vocabulary)"* (`adr-standards-rule-draft.md:36`), and the parent ADR's constraint c-001 states this **MUST** be so (`ADR-PROJ031-004-adr-identifier-convention.md:123`). The quality-enforcement.md Tier Vocabulary table defines the HARD keyword set as `MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL` (no case qualifier stated).

**Location and evidence:**
- `adr-standards-rule-draft.md:47` — ADR-M-002: *"ADR origin SHOULD be recorded in frontmatter (`origin_project`, optional `origin_entity`), **never** in the identifier."*
- `adr-standards-rule-draft.md:133` — *"A `DEC-NNN` is **never** renamed into an ADR; author a new ADR and cross-link."* (standalone declarative sentence, no SHOULD/SHOULD-NOT hedge)
- `adr-standards-rule-draft.md:144` — Supersede-and-Amend table, "Decision reversal / replacement" row, Mechanism cell: *"New superseding ADR; **never** edit old body"* (standalone, unhedged)
- Secondary/weaker instances in the same file using "must" to describe lint-rule pattern-matching and build-completion criteria rather than author obligations: `:94` ("...must all pass the lint's grandfather regression test before it ships"), `:172` ("A git-added file **must** not match `^ADR-\d`"), `:173` ("`sort | uniq -d` **must** be empty"), `:177` ("A grandfather regression test **must** be green before the lint ships").

**Impact:** The document's own Changelog (`ADR-PROJ031-004-adr-identifier-convention.md:740`, v1.4 SM-203 entry) states: *"confirmed the rule draft carries zero uppercase HARD-tier keywords (MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL — the full SSOT six-term set)"* — this claim is **literally true** (verified: zero uppercase matches for those six tokens found in this review) but is a **narrower claim than "MEDIUM-tier purity"/"zero HARD vocabulary."** A reader (human or a future CI lint checking tier-purity) does not parse semantic obligation force by capitalization; "never edit old body" and "never renamed into an ADR" carry identical prohibitive force to "MUST NOT edit"/"MUST NOT be renamed." Per c-001 (a HARD "MUST" the ADR imposes on its own companion rule file), and per the SSOT's own HARD-ceiling rationale (any new HARD-force obligation should go through the C4 + ceiling-exception path, not appear informally in prose), this is a genuine — if bounded — tier-purity leak. It is bounded because the 13 numbered `ADR-M-001`…`ADR-M-013` standards themselves are cleanly SHOULD/SHOULD-NOT/MAY throughout; the leak is confined to unnumbered explanatory/mechanism prose.

**Dimension:** Internal Consistency (the document's self-certification of purity is scoped more narrowly than the purity property it claims to have achieved).

**Remediation:** Reword the three primary instances to MEDIUM-tier form: `:47` → "...SHOULD NOT appear in the identifier"; `:133` → "A `DEC-NNN` SHOULD NOT be renamed into an ADR; author a new ADR and cross-link instead"; `:144` → "New superseding ADR; the old body SHOULD NOT be edited (immutability)." For the lint-rule descriptions (`:94,172,173,177`), either (a) accept "must" there as tool-mechanism description (the lint's own trigger condition) and explicitly say so in the L5 section preamble so the scoping is stated rather than implied, or (b) reword to "is expected to"/"is checked for" to keep the whole file lowercase-hard-word-free. Also correct the changelog claim (`ADR-PROJ031-004...:740`) to state the narrower, accurate scope: "zero **uppercase** HARD-tier keywords" rather than let it stand adjacent to broader "MEDIUM-tier purity" language without the qualifier.

---

### CC-002-20260705-iter006: L1 token-budget fit never checked against the SSOT's own ~12,500-token aggregate constant [MAJOR]

**Principle:** `quality-enforcement.md` Enforcement Architecture table states: *"L1 | Session start | Behavioral foundation via rules | Vulnerable | ~12,500"* (tokens) and *"Total enforcement budget: ~15,350 tokens (7.7% of 200K context)."* The rule draft is explicitly destined for `.context/rules/adr-standards.md`, which auto-loads at session start via the `.claude/rules -> ../.context/rules` directory symlink (`ADR-PROJ031-004-adr-identifier-convention.md:503`, M-2b) — i.e., it is squarely an **L1-layer** artifact.

**Location and evidence:** `subtraction-pass-notes.md:64-72` (Budgets Achieved table) measures the rule draft against two self-referential targets only: a ~2,500-token soft target and a comparison to `skill-standards.md` (190 lines / ~1,768 tokens, cited at `adr-standards-rule-draft.md` Changelog v1.7 note per `subtraction-pass-notes.md:72`). Neither the rule draft, the ADR, nor the subtraction notes cross-reference the `quality-enforcement.md` Enforcement Architecture L1 total of ~12,500 tokens, nor the fact that (per the ADR's own citation) 17 files currently populate `.context/rules/` (`ADR-PROJ031-004-adr-identifier-convention.md:509`: *"of the 17 files in `.context/rules/`..."*). A back-of-envelope check the deliverable itself never performs: 12,500 / 17 ≈ 735 tokens average per existing rule file; the new file's own honestly-disclosed ~3,248 tokens is ~4.4x that average and would, if the ~12,500 figure is a current-state measurement rather than a hard ceiling with slack, represent roughly a 26% single-file increase to the entire L1 corpus.

**Impact:** This is not a violation of a specific numbered rule (no `H-XX` mandates "new rule files must fit the residual L1 budget"), but it is a significant **completeness/rigor gap**: the document performs extensive, precise quantitative self-verification everywhere else (grep-pinned occurrence counts, corpus-wide `sort | uniq -d` collision math, a 72%/28% citation-style ratio) yet omits the one budget check most directly relevant to the file's own destination layer, despite citing `quality-enforcement.md` (the source of the ~12,500 figure) dozens of times elsewhere for the HARD ceiling and Tier Vocabulary. Left unaddressed, this is exactly the class of context-rot risk (R-T01) the framework's own `agent-development-standards.md` CB-01/CB-02 budget standards exist to catch — just applied to a different, adjacent layer (L1 rule corpus rather than agent context).

**Dimension:** Completeness / Methodological Rigor.

**Remediation:** Add a short subsection (or a line in the existing "Honest note on the token budget" paragraph) stating the current aggregate L1 corpus size (measure via the same `wc -w`×1.35 method across `.context/rules/*.md`) and the resulting post-install total, explicitly checked against the ~12,500 SSOT figure. If the resulting total exceeds ~12,500, either disclose this as an accepted, bounded budget increase (with rationale, since this is a MEDIUM-tier document and the L1 figure is not itself phrased as a HARD ceiling) or identify a companion-file consolidation opportunity. Either resolution is acceptable; the gap is the omission, not a presumed wrong answer.

---

### CC-003-20260705-iter006: Line-count precision discrepancy in the Budgets Achieved table [MINOR]

**Location:** `subtraction-pass-notes.md:69` states the rule draft is **"232"** lines. `adr-standards-rule-draft.md`, read in full via line-numbered tool output, terminates at **line 233** (`*Proposed home on ratification: ...*`).

**Impact:** Trivial (1-line, ~0.4%) and does not change the "within/under the ~250–350-line guidance" conclusion. Flagged only because the package explicitly prides itself on measured-not-rounded precision (`subtraction-pass-notes.md:72`: *"The number is stated, not rounded down"*) — a self-imposed evidentiary bar that a 1-line miscount technically misses.

**Dimension:** Evidence Quality.

**Remediation:** Re-run the line count (`wc -l` or equivalent) and correct the table cell if it is indeed off by one; low priority.

---

### CC-004-20260705-iter006: Known quality-gate bypass on the same corpus is not cross-referenced in either deliverable's own residual disclosures [MINOR]

**Location:** `FEEDBACK-LOG.md:78` (FU.3 disposition) discloses: *"24 doc-convention test failures on the new corpus (committed `--no-verify` once, disclosed in the commit message; debt tracked for fix before next commit)"* on commit `518c6556` (2026-07-05, "178-file PROJ-031 corpus"). Both deliverables under review are part of that same PROJ-031 corpus and were touched in this date range.

**Impact:** This review independently verified H-23 nav-table/anchor compliance for both deliverables specifically and found no defect on that dimension (see [Verified Compliant](#verified-compliant-no-finding)), so the 24 failures are unlikely to implicate these two files on that specific check — but the ADR's own residual-disclosure discipline (R-1 through R-8, R-A/R-B/R-C, all named with a home and a detection signal) is otherwise exhaustive, and this known, already-recorded bypass of an automated quality gate covering "the new corpus" is not mentioned or ruled out anywhere in either deliverable. Given P-022's completeness expectation (and the standard this document holds *itself* to elsewhere), this is a small but real gap in cross-referencing a known, disclosed risk.

**Dimension:** Traceability.

**Remediation:** Add one line to the ADR's Risks table or the rule draft's Changelog noting the `--no-verify` bypass event and confirming (or identifying) whether either deliverable is among the 24 failing files, closing the loop the framework's own disclosure discipline otherwise maintains.

---

## Recommendations

**P0 (Critical):** None.

**P1 (Major):**
- CC-001: Reword `adr-standards-rule-draft.md:47,133,144` to SHOULD-NOT/MAY form; either reword or explicitly scope the lint-rule "must" instances (`:94,172,173,177`); correct the ADR Changelog v1.4 claim to specify "uppercase" explicitly wherever it is invoked to support a broader "MEDIUM-tier purity" conclusion.
- CC-002: Add an L1-aggregate-budget cross-check (current `.context/rules/` total vs. the SSOT's ~12,500-token figure, post-install total, and a disposition) to the rule draft's or subtraction notes' token-budget section.

**P2 (Minor):**
- CC-003: Correct the line-count figure in `subtraction-pass-notes.md:69` (232→233, or re-verify).
- CC-004: Cross-reference the FU.3 `--no-verify`/24-failures bypass in the ADR's Risks section or rule-draft Changelog, confirming these two files' status relative to it.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CC-002 (Major): L1 aggregate budget-fit never checked against the SSOT's own named constant |
| Internal Consistency | 0.20 | Negative | CC-001 (Major): residual lowercase HARD-force vocabulary vs. the document's own MEDIUM-tier-purity self-certification |
| Methodological Rigor | 0.20 | Negative | CC-002 contributes here too: the file's otherwise-rigorous quantitative self-checks omit the one directly relevant to its destination enforcement layer |
| Evidence Quality | 0.15 | Negative (slight) | CC-003 (Minor): a small precision miss against the document's own stated "measured, not rounded" standard |
| Actionability | 0.15 | Neutral | All findings carry specific, file-and-line remediation; no actionability gap introduced |
| Traceability | 0.10 | Negative (slight) | CC-004 (Minor): a known, disclosed quality-gate bypass on the same corpus is not cross-linked from either deliverable's own residual-disclosure apparatus |

**Constitutional Compliance Score:** `1.00 - (0.10*0 + 0.05*2 + 0.02*2) = 1.00 - 0.14 = 0.86`

**Threshold Determination:** REVISE (0.85–0.91 band; below the SSOT H-13 threshold of 0.92 and well below the C4 engagement gate of 0.95). No Critical findings; the two Major findings are both narrowly-scoped, mechanically fixable (wording/cross-reference additions), and do not implicate the core decision (Scheme B), the ratification record, or the honesty of the subtraction pass itself — all of which independently verified as sound.

---

## Execution Statistics
- **Total Findings:** 4
- **Critical:** 0
- **Major:** 2
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5

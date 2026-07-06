# Constitutional Compliance Report: ADR-PROJ031-004 + adr-standards-rule-draft.md (Iteration 4)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:**
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`

**Criticality:** C4 (engagement quality gate 0.95, user-raised above SSOT 0.92)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, independent — iteration 4)
**Constitutional Context:** `.context/rules/quality-enforcement.md` (Tier Vocabulary, HARD Rule Index, Retired Rule IDs), `.context/rules/markdown-navigation-standards.md` (H-23/NAV-001..006), `.context/rules/skill-standards.md` (H-25/H-26), `CLAUDE.md`, `.github/CODEOWNERS`, `AGENTS.md`, `skills/ast/SKILL.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional compliance assessment |
| [Findings Table](#findings-table) | All findings with severity |
| [Finding Details](#finding-details) | Full evidence and remediation per finding |
| [Verified-Compliant Checks](#verified-compliant-checks) | Explicit checks requested by the task that PASSED |
| [Out-of-Scope Observation](#out-of-scope-observation) | Pre-existing repo inconsistency noticed but not attributable to this deliverable |
| [Remediation Plan](#remediation-plan) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Finding counts and protocol completion |

---

## Summary

**PARTIAL compliance.** 0 Critical, 2 Major, 2 Minor findings. The package's MEDIUM-tier purity (zero HARD-vocabulary in the rule draft), H-23 navigation-table structure, and the H-26 self-exclusion are all **verified correct**. The two Major findings are residual citation/traceability defects that survived four rounds of adversarial remediation: (1) the Migration-Plan item that proposes registering the new rule file in CLAUDE.md's Navigation table cites H-23/NAV-004 as its authority, but neither rule actually governs cross-file registration in another document's pointer index, and the accompanying claim overstates how uniformly `.context/rules/*` files are individually listed there; (2) the external norm "JPH name-as-ID," invoked twice as supporting evidence for the Decision, is never expanded and is entirely absent from the formal References table, making it unverifiable. **Recommendation: REVISE** (constitutional compliance score 0.86, REVISE band) — both Major findings are narrow, textual, low-effort fixes that do not touch the Decision itself.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260702I4 | H-23 (nav table) / NAV-004 (coverage) scope | HARD/MEDIUM (mis-cited) | Major | ADR `:501` M-7; rule-draft `:3` wrapper note | Traceability, Methodological Rigor |
| CC-002-20260702I4 | P-004 provenance / P-022 evidentiary rigor / "no undefined acronyms" | MEDIUM | Major | ADR `:167`, `:420`; References table `:708-724` (no entry) | Evidence Quality, Completeness |
| CC-003-20260702I4 | Markdown structural convention (single H1 per document) | SOFT | Minor | rule-draft `:1`, `:9` | Internal Consistency |
| CC-004-20260702I4 | P-022 self-verification completeness | SOFT | Minor | ADR Changelog `:746` (SM-203 clause) | Evidence Quality |

**Finding ID Format:** `CC-{NNN}-20260702I4` (execution_id = 2026-07-02, iteration 4).

---

## Finding Details

### CC-001-20260702I4: H-23/NAV-004 Misapplied as Authority for Cross-File CLAUDE.md Registration [MAJOR]

**Principle:** H-23 ("All Claude-consumed markdown files over 30 lines MUST include a navigation table," `.context/rules/markdown-navigation-standards.md:16`) and NAV-004 ("All major sections (`##` headings) SHOULD be listed," same file, Standards table). Both rules govern **a document's own internal Document-Sections nav table listing its own `##` headings** — confirmed by direct read of `markdown-navigation-standards.md` (HARD Rules + Standards sections) and by CLAUDE.md's own compliant nav table (`CLAUDE.md:7-14`, four entries matching its four `##` headings exactly).

**Location:**
- ADR `:501`, Migration Plan row M-7: *"Register the new rule file in **CLAUDE.md's Navigation table**... for **discoverability (H-23; NAV-004 'all major sections listed')**."*
- rule-draft wrapper note `:3`: *"It is then registered in **CLAUDE.md's Navigation table for discoverability (H-23 / NAV-004 coverage — CC-004 iter-3: NOT NAV-002...)** — the same mechanism by which the existing `.context/rules/*` files are listed there (`CLAUDE.md:53-56`)."*

**Evidence:** Neither H-23 nor NAV-004, as written in `markdown-navigation-standards.md`, mentions or implies an obligation for a *different* document (CLAUDE.md) to carry a pointer-index entry for a *newly created* file. H-23/NAV-004 are about a file's own `## Document Sections` table covering its own headings. CLAUDE.md's `## Navigation` section (the "Need | Location" table, `CLAUDE.md:51-63`) is a **cross-file resource index**, not the H-23 nav table for CLAUDE.md (that is the separate `## Document Sections` table at `CLAUDE.md:7-14`, which already correctly lists Identity/Critical Constraints/Navigation/Quick Reference and needs no new entry). Read directly at `CLAUDE.md:51-63`: of the **17** files in `.context/rules/` (Glob-verified: `agent-development-standards.md`, `agent-routing-standards.md`, `architecture-standards.md`, `coding-standards.md`, `error-handling-standards.md`, `file-organization.md`, `mandatory-skill-usage.md`, `markdown-navigation-standards.md`, `mcp-tool-standards.md`, `project-workflow.md`, `prompt-quality.md`, `prompt-templates.md`, `python-environment.md`, `quality-enforcement.md`, `skill-standards.md`, `testing-standards.md`, `tool-configuration.md`), only **3** (`quality-enforcement.md`, `agent-development-standards.md`, `agent-routing-standards.md`) get an individually-named row (`CLAUDE.md:54-56`); the remaining 14 (~82%) are covered only by the single generic row `Coding/architecture/testing rules | .context/rules/ (A)` (`CLAUDE.md:53`). The claim "the same mechanism by which the existing `.context/rules/*` files are listed there" therefore overstates a 3-of-17 exception as a general, established pattern, and cites H-23/NAV-004 as the rule that *mandates* M-7 when in fact no cited HARD or MEDIUM rule creates that obligation — M-7 is a discretionary discoverability choice, not a rule-compelled one.

**Impact:** This is the third citation attempt at this exact spot (iteration 1 implicitly, iteration 2 cited H-26 [wrong — corrected CC-002], iteration 3 cited NAV-002 [wrong — corrected CC-004 to H-23/NAV-004], and the H-23/NAV-004 citation itself is still inapplicable). A document whose central defense mechanism is citation precision (dozens of grep-pinned, line-numbered corrections) leaves its own most-revised citation spot inaccurate. If a future reader or the M-6/L5 lint implementer treats this as evidence that H-23 requires cross-document registry entries, H-23's actual scope (a file's own nav table) would be silently inflated.

**Dimension:** Traceability (0.10), Methodological Rigor (0.20)

**Remediation:** Replace the H-23/NAV-004 citation at ADR `:501` and rule-draft `:3` with an honest framing, e.g.: *"Register the new rule file as a discretionary discoverability entry in CLAUDE.md's Navigation table, following the precedent set for `quality-enforcement.md`, `agent-development-standards.md`, and `agent-routing-standards.md` (`CLAUDE.md:54-56`) — 3 of the 17 `.context/rules/*` files that have been individually promoted from the generic `.context/rules/` row (`CLAUDE.md:53`). This is not compelled by H-23 or NAV-004 (which govern a document's own internal nav table), but is a reasonable extension of the existing minority practice."* This also fixes the "same mechanism ... existing files are listed there" overclaim.

---

### CC-002-20260702I4: "JPH Name-as-ID" Cited as Evidence but Never Defined or Referenced [MAJOR]

**Principle:** P-004 (provenance/traceability of claims), P-022 (no unverifiable or overclaimed evidence). Directly relevant per the user's own standing instruction to spell out acronyms on first use.

**Location:** ADR `:167` ("...external slug-as-ID norm (log4brains/JPH)."); ADR `:420` ("Aligns with the framework's thesis and with external norms (log4brains slug-as-ID, **JPH name-as-ID**, the accepted BUG-006 Alternative 3)."). Cross-checked against the References table (`:708-724`), which lists exactly 11 numbered sources including "log4brains ADR 20201016; MADR (`adr.github.io/madr`); Nygard (Fowler/bliki); GOV.UK ADR Framework; AWS Prescriptive Guidance" (ref #11) — **"JPH" does not appear anywhere in the References table.**

**Evidence:** "JPH" is used twice in the body as supporting evidence for Scheme B (subject-encoded identity) — once in the Scheme B steelman (`:167`) and once in the Positive Consequences list (`:420`) — but the term is never expanded, never given a URL, and never listed among the 11 formal references. Unlike "MADR," which at least resolves to a URL in the References table (`adr.github.io/madr`), "JPH" has zero traceable anchor anywhere in either deliverable. A reader cannot verify this claim without independently knowing it likely refers to Joel Parker Henderson's widely-cited ADR template/organization convention — an inference, not something the document states.

**Impact:** The Decision's Rationale explicitly rests on "external consensus" as one of three converging argument lines (`:253-259`), and this ADR is otherwise scrupulous about citing sources with exact paths and line numbers for every other claim. An uncited, unexpanded acronym used as supporting evidence for the central Decision is a genuine, fixable gap in an otherwise unusually rigorous evidentiary standard — and it directly violates the "no undefined acronyms" hygiene the invoking context requires.

**Dimension:** Evidence Quality (0.15), Completeness (0.20)

**Remediation:** Either (a) expand "JPH" on first use (e.g., "JPH (Joel Parker Henderson's ADR organization convention)") and add a 12th row to the References table with a URL, or (b) if the source cannot be verified with confidence, remove the "JPH name-as-ID" clause from both `:167` and `:420` per P-022 (do not cite what cannot be traced). Given the research file (`adr-convention-standards-research.md:202,235`) treats "log4brains/JPH" as jointly source-verified, option (a) is the lower-cost, evidence-preserving fix.

---

### CC-003-20260702I4: Rule Draft Contains Two H1 Headings [MINOR]

**Principle:** Markdown structural convention (implicit in NAV-001/NAV-002 placement guidance — a nav table "SHOULD appear after frontmatter, before first content section" presumes a single document with one title).

**Location:** `adr-standards-rule-draft.md:1` (`# DRAFT — Proposed `.context/rules/adr-standards.md``) and `adr-standards-rule-draft.md:9` (`# ADR Standards`).

**Evidence:** The file opens with an H1 wrapper-note title, followed by a horizontal rule, then a second, independent H1 (the actual future rule file's own title) at line 9. Two H1s in one markdown file is non-standard; tools that assume a single H1 as page title (TOC generators, some static-site renderers, accessibility screen-reader landmark detection) will treat this ambiguously.

**Impact:** Cosmetic only — does not affect H-23 compliance (the file's own `## Document Sections` table at `:13-31` correctly covers all `##` headings under the second H1) and will self-resolve once this content is extracted into `.context/rules/adr-standards.md` (at which point the wrapper H1 + note disappear per the file's own stated intent, `:1-5`).

**Dimension:** Internal Consistency (0.20)

**Remediation:** No action required before ratification (the wrapper note is explicitly transient); optionally demote the wrapper-note title to a blockquote-style annotation (no H1) to avoid the dual-H1 structure while the draft is under review.

---

### CC-004-20260702I4: Iteration-4 Self-Verification Under-Enumerates the Tier-Vocabulary Checklist [MINOR]

**Principle:** P-022 (self-verification claims should be as precise as the claims they verify).

**Location:** ADR Changelog `:746`, SM-203 clause: *"confirmed the rule draft carries zero uppercase HARD-tier keywords (MUST/SHALL/REQUIRED)."*

**Evidence:** The SSOT Tier Vocabulary (`.context/rules/quality-enforcement.md`) defines HARD-tier keywords as **six** terms: `MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL`. The iteration-4 self-verification note names only three (MUST/SHALL/REQUIRED), omitting NEVER, FORBIDDEN, and CRITICAL from its stated checklist. Independent verification for this report (`grep -n '\bMUST\b\|\bSHALL\b\|\bNEVER\b\|\bFORBIDDEN\b\|\bREQUIRED\b\|\bCRITICAL\b'` against `adr-standards-rule-draft.md`) confirms **zero** matches for all six terms, so the underlying claim holds — but the changelog's own stated basis for the claim is incomplete against the SSOT's own six-term definition.

**Impact:** Low — the claim is substantively true (independently re-verified above), but a document this focused on precise self-citation should enumerate the full six-term SSOT list when asserting tier-purity compliance, not a partial three-term subset.

**Dimension:** Evidence Quality (0.15)

**Remediation:** Update the SM-203 changelog clause to read "...zero uppercase HARD-tier keywords (MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL, the full SSOT six-term set)."

---

## Verified-Compliant Checks

The following items were explicitly checked per the task's request and are **confirmed compliant** (no finding):

| Check | Result | Evidence |
|---|---|---|
| MEDIUM-tier purity — zero HARD-vocabulary in the rule draft | **PASS** | `grep -n '\bMUST\b\|\bSHALL\b\|\bNEVER\b\|\bFORBIDDEN\b\|\bREQUIRED\b\|\bCRITICAL\b'` against `adr-standards-rule-draft.md` returns zero matches. All 13 ADR-M-### rows (`:46-58`) consistently use SHOULD/SHOULD NOT/MAY/PERMITTED/RECOMMENDED. |
| H-23 nav tables present, anchor-linked, and covering all `##` headings | **PASS** | ADR (`:34-62`, 24 entries) and rule draft (`:13-31`, 14 entries) both list every `##` heading in their respective bodies with correctly-formed GitHub-style anchors (spot-checked `#options-considered-af`, `#rationale--answering-the-crux-head-on`, `#promotion-frequency-sensitivity-the-load-bearing-assumption`). |
| H-26 correctly excluded as a registration mechanism | **PASS** | `skills/ast/SKILL.md` -- N/A; verified against `.context/rules/skill-standards.md:31`: H-26 governs SKILL.md description/path/registration for *skills*, not rule files. The package's CC-002 correction (dropping the earlier H-26 citation) is accurate. |
| `.claude/rules` directory-symlink claim (PM-101) | **PASS** | `Grep` for a unique string ("HARD Rule Index") resolved through `.claude/rules/quality-enforcement.md`, `.claude/rules/mcp-tool-standards.md`, `.claude/rules/agent-routing-standards.md`, `.claude/rules/agent-development-standards.md` — confirms the symlink is live and content-equivalent to `.context/rules/`. (Note: the `Glob` tool does not traverse this symlink and returns no matches for `.claude/rules/*` — a tool-specific quirk, not evidence the symlink is broken; `Grep` and direct `Read` both confirm it resolves.) |
| `.github/CODEOWNERS` single-identity claim | **PASS** | File content confirms `.context/rules/`, `docs/governance/`, and all `.github/*` governed paths are assigned solely to `@geekatron`. |
| `AGENTS.md:1` "Registry of Available Specialists" citation | **PASS** | Confirmed verbatim at `AGENTS.md:1`. |
| `jerry ast frontmatter` blockquote-only parsing claim (CC-003) | **PASS** | Confirmed at `skills/ast/SKILL.md:105`: "Extract all blockquote frontmatter fields as a JSON object." |
| Retired-Rule-ID tombstone precedent analogy | **PASS (reasonable analogy)** | `.context/rules/quality-enforcement.md` "Retired Rule IDs" table establishes that retired IDs are never reassigned — a fair structural precedent for "ADR `NNN` is never reused; reversal is by supersession" (`ADR-M-005`). |

---

## Out-of-Scope Observation

While verifying H-32 citations in the Migration Plan (ADR `:500,505,506,507`, all cite "(H-32)" for GitHub Issue parity gating), a **pre-existing inconsistency in the framework itself** was noticed: `.context/rules/quality-enforcement.md`'s HARD Rule Index assigns GitHub Issue parity to **H-32** (sourced from `project-workflow.md`), but `.context/rules/project-workflow.md`'s own body labels that same rule "**H-31**" internally (`> **H-31:** When working in the Jerry repository...`), which collides with quality-enforcement.md's own H-31 ("Clarify before acting when ambiguous"). **This is not a defect in either reviewed deliverable** — the ADR correctly cites the SSOT's H-32 numbering — but is flagged here per P-022 disclosure since it was directly observed during verification and could confuse a future reader who checks the citation against `project-workflow.md` instead of the SSOT. Recommend a separate worktracker item against `.context/rules/project-workflow.md` (not this ADR/rule-draft), out of this review's edit mandate (P-020).

---

## Remediation Plan

**P0 (Critical):** None.

**P1 (Major):**
- CC-001-20260702I4: Replace the H-23/NAV-004 citation at ADR `:501` and rule-draft `:3` with an honest "discretionary precedent, not rule-compelled" framing; correct the "3 of 17" ratio in place of the "same mechanism ... existing files" overclaim.
- CC-002-20260702I4: Expand "JPH" on first use and add it to the References table, or remove the clause if the source cannot be traced with confidence.

**P2 (Minor):**
- CC-003-20260702I4: Optionally demote the rule-draft wrapper-note title to avoid a dual-H1 structure (no action required before ratification).
- CC-004-20260702I4: Broaden the SM-203 changelog clause to enumerate the full six-term SSOT HARD-tier keyword set.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CC-002: References table omits a cited external source ("JPH"). |
| Internal Consistency | 0.20 | Negative (minor) | CC-003: dual-H1 structure in the rule draft. |
| Methodological Rigor | 0.20 | Negative | CC-001: HARD-rule citation (H-23) misapplied as authority for an action the rule does not govern. |
| Evidence Quality | 0.15 | Negative | CC-002 (uncited/unexpanded acronym used as decision evidence); CC-004 (incomplete self-verification enumeration). |
| Actionability | 0.15 | Neutral | All findings carry specific, low-effort textual remediations; none blocks the core Decision. |
| Traceability | 0.10 | Negative | CC-001: citation of H-23/NAV-004 does not actually trace to an obligation those rules create. |

**Constitutional Compliance Score:** `1.00 - (0.10*0 + 0.05*2 + 0.02*2) = 1.00 - 0.14 = 0.86` (REVISE band, 0.85-0.91; below the SSOT H-13 threshold of 0.92 and below the engagement's 0.95 gate).

**Threshold Determination:** REVISE — both Major findings are narrow textual/citation fixes; neither touches the Decision (Scheme B) itself, the Migration Plan's substantive content, or any HARD rule in force.

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 0
- **Major:** 2
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5 (S-007 Execution Protocol: Load Constitutional Context, Enumerate Applicable Principles, Principle-by-Principle Evaluation, Remediation Guidance, Score Constitutional Compliance)

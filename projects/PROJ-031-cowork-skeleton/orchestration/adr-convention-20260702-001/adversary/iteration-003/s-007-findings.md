# Constitutional Compliance Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95, above the 0.92 SSOT gate)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, independent — iteration 3)
**Constitutional Context:** `.context/rules/quality-enforcement.md`, `.context/rules/agent-development-standards.md`, `.context/rules/markdown-navigation-standards.md`, `.context/rules/mcp-tool-standards.md`, `.context/rules/project-workflow.md`, `skills/ast/SKILL.md`, plus live corpus evidence (`docs/design/ADR-output-path-resolution-001.md`)

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional assessment |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Full evidence and remediation per finding |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Compliance Positives](#compliance-positives) | Principles verified COMPLIANT (not just violations) |
| [Execution Notes](#execution-notes) | Protocol steps completed, scope notes, blind-protocol statement |

---

## Summary

**PARTIAL compliance.** 2 Critical, 1 Major, 1 Minor finding. Constitutional compliance score: **0.73 → REJECTED** (below both the 0.85 floor and the 0.92 SSOT/0.95 engagement gate). The package is otherwise unusually disciplined about P-022 disclosure (extensive, well-labeled Claim-Status blocks and honest "TBD" admissions survive two prior remediation rounds), which makes the two Critical findings below notable: both are the *same class of defect* the authors already diagnosed and partially fixed elsewhere in these exact documents, but did not apply consistently. Recommend REVISE, not reject-and-restart — both Criticals have narrow, mechanical fixes.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260702-iter3 | P-022 / H-03: No deception about capabilities | HARD | **Critical** | ADR L0 (`:54`) and L1 "Testing/verification approach" (`:341`) assert present-tense "enforced by"/"is verified by" the L5 lint; rule draft Tier-and-Scope (`:11`,`:38`) likewise. Both contradicted ~150-370 lines later by explicit "DESIGNED, NOT BUILT"/"advisory-only" Claim-Status blocks (ADR `:554`; rule draft `:187`) | Evidence Quality, Internal Consistency |
| CC-002-20260702-iter3 | Tier Vocabulary (HARD = "cannot override") + HARD Rule Ceiling (25/25, zero headroom) | HARD (de facto, via smuggled non-waivability) | **Critical** | Rule draft L-9 (`:208`) and ADR L-9 (`:597`) both retain `FAIL (non-waivable-in-practice...)` — the identical phrasing the document itself calls "de-facto HARD... a genuine contradiction" when diagnosing L-2/L-3 (rule draft `:195`; ADR `:584`, "Tier reconciliation (CC-001)") — but the fix applied to L-2/L-3 was never applied to L-9 | Internal Consistency, Methodological Rigor |
| CC-003-20260702-iter3 | Methodological completeness / tooling consistency (no HARD rule text directly named; ADRs are explicitly carved out of H-33's worktracker-entity scope) | MEDIUM (design-rigor gap) | **Major** | Rule draft Frontmatter Schema (`:109-127`) mandates YAML `---` frontmatter for all ADRs; `skills/ast/SKILL.md:51-52,99-107` documents `jerry ast frontmatter` as extracting **only** blockquote `> **Key:** Value` fields; the 3 live canonical framework ADRs use exactly that blockquote format today (`docs/design/ADR-output-path-resolution-001.md:3-9`). Neither document reconciles this parser incompatibility, despite otherwise rigorous CLI/tooling verification elsewhere (H-05 `uv run jerry` checks, etc.) | Completeness, Methodological Rigor |
| CC-004-20260702-iter3 | P-004 Traceability / citation precision | SOFT | **Minor** | Rule draft wrapper note (`:3`) and ADR M-7 (`~:458`) cite "(H-23 / NAV-002)" as the basis for registering the new rule file in **CLAUDE.md's** Navigation table. NAV-002 in `markdown-navigation-standards.md` governs a document's **own** internal nav-table placement ("after frontmatter, before first content section"), not cross-file registration in a different document's nav table | Traceability |

**Finding ID Format:** `CC-{NNN}-20260702-iter3` (execution_id = iteration-3 blind review, 2026-07-02).

**Severity Definitions:** Critical = violates HARD principle, blocks acceptance per H-13. Major = violates MEDIUM-tier rigor/consistency expectation, requires revision. Minor = SOFT improvement opportunity.

---

## Finding Details

### CC-001-20260702-iter3: Front-loaded enforcement/verification overclaim, back-loaded correction [CRITICAL]

**Principle:** P-022 (No Deception, `.context/rules/quality-enforcement.md` H-03: "No deception about actions/capabilities... Deceptive output reworked")

**Location and evidence (four load-bearing citations, both files):**

1. `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:54` (L0 Executive Summary — the single most-read section of a C4 ADR): *"...enforced by a deterministic CI lint rather than a hard block."* Present tense, no qualifier.
2. `ADR-PROJ031-004-adr-identifier-convention.md:341` (L1, "Testing / verification approach"): *"The convention is verified by the L5 lint (deterministic; spec below) and by these post-adoption checks..."* Present tense, asserts an operating verification mechanism.
3. `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:11`: *"Enforced by deterministic L5 CI lint, not a HARD invariant."*
4. `adr-standards-rule-draft.md:38`: *"Enforcement is deterministic L5 CI lint (fail/warn classes below) plus L4 advisory — never a HARD block."*

**Contradicted by (same documents, far later):**

- `ADR-PROJ031-004-adr-identifier-convention.md:554`: *"Claim-Status: the lint is DESIGNED, NOT BUILT (P0-1 / RT-001 / FM-012 honest framing, P-022). As of 2026-07-02, `scripts/lint_adr_convention.py`... do not exist in the repository (Glob-verified)... enforcement is advisory-only: nothing today prevents a non-compliant `status: ACCEPTED` ADR from merging."*
- `adr-standards-rule-draft.md:187`: *"Claim-Status: SPECIFIED, NOT IMPLEMENTED... Everything below is an engineered specification. Until the script ships... enforcement is advisory-only and this rule file's guarantees are aspirational."*

**Impact:** A reader who stops at the L0 summary or the Tier-and-Scope intro — exactly the audience those sections are written for — comes away believing the lint is live today. The corrective disclosure exists but sits 200-370 lines later, in a section (`Enforcement Design`) a summary-level reader is not expected to reach. This is precisely the failure mode P-022 exists to prevent: not fabrication of facts, but *placement* of true facts such that the first, most-visible claim is uncorrected at the point of reading. The document's own changelog shows the authors are aware of exactly this risk class (iteration-2 P0-1/P0-2 additions of Claim-Status blocks) — but did not propagate the caveat to the two earliest, highest-visibility assertions.

**Dimension:** Evidence Quality (primary), Internal Consistency (secondary — the two present-tense claims and the two disclosure blocks are factually inconsistent about present-day system state).

**Remediation:** Add a one-clause qualifier at first mention in both L0/summary locations, e.g. "...enforced by a deterministic CI lint (once M-6 ships — see Enforcement Design; not yet built as of 2026-07-02) rather than a hard block." Apply symmetrically to `ADR:341` and `adr-standards-rule-draft.md:11,38`. This is a 4-line edit, not a redesign.

---

### CC-002-20260702-iter3: L-9 lint rule retains the exact "non-waivable" HARD-tier smuggling the document itself diagnosed and fixed for L-2/L-3, but never applied the fix to L-9 [CRITICAL]

**Principle:** Tier Vocabulary (`.context/rules/quality-enforcement.md`: "HARD | ... | Cannot override") + HARD Rule Ceiling Derivation ("Current count: 25 HARD rules... Zero headroom")

**Location and evidence:**

- `adr-standards-rule-draft.md:208`: `**L-9 No new file under frozen dirs** | **FAIL (non-waivable-in-practice; new — RT-002)** | A *git-added* file must NOT land under `docs/adrs/` or `docs/archive/`...`
- `ADR-PROJ031-004-adr-identifier-convention.md:597` (Enforcement Design table, same wording verbatim): `**FAIL (non-waivable-in-practice; new — RT-002)**`
- Compare the document's own diagnosis of the *identical* pattern for L-2/L-3, three rows above in the same table (`adr-standards-rule-draft.md:195`; `ADR:584`, "Tier reconciliation for L-2/L-3 (CC-001 fix, P0-3)"): *"The prior draft called collision rules L-2/L-3 'non-waivable,' which is de-facto HARD ('cannot override' is the SSOT's defining property of HARD tier, `.context/rules/quality-enforcement.md` Tier Vocabulary) inside a MEDIUM-tier rule file — a genuine contradiction. Corrected: L-2/L-3 are waivable through the same structured-waiver mechanism as all FAIL rules..."*
- No equivalent correction is applied to L-9. L-9's row is never subjected to the append-only waiver-ledger mechanism (`scripts/adr-lint-waivers.yaml`) that every other FAIL rule (including the now-corrected L-2/L-3) explicitly uses.

**Impact:** By the document's own stated test ("cannot override" = the SSOT's defining property of HARD), L-9 as currently worded is a de-facto HARD rule embedded in a document whose entire premise (Tier and Scope, `:34-38`) is "no HARD rule is proposed... MEDIUM tier only." This is not a hypothetical risk: the HARD Rule Ceiling is at 25/25 with zero headroom, and the ADR's own Constraint c-001 states a new HARD rule "would require a C4 ADR + a ceiling exception (max +3, one concurrent, 3-month reversion)." An uncorrected, effectively non-overridable FAIL rule inside a MEDIUM-tier file is exactly the kind of quiet HARD-rule-by-a-different-name the Ceiling mechanism exists to prevent — and the document flags this risk explicitly for L-2/L-3 while missing it for L-9, one table row later.

**Dimension:** Internal Consistency (primary — direct self-contradiction within the same table), Methodological Rigor (the CC-001 fix was applied inconsistently).

**Remediation:** Apply the identical reconciliation already written for L-2/L-3 to L-9: change "FAIL (non-waivable-in-practice...)" to "FAIL (waivable-in-principle; see tier reconciliation) — practically strict because no constructable justification exists for committing a new file into a frozen/collision-source directory," and route it through the same `adr-lint-waivers.yaml` mechanism. This is a wording fix in one table cell per file (two cells total), not a design change — L-9's practical strictness is preserved; only its tier framing needs to match L-2/L-3's already-corrected framing.

---

### CC-003-20260702-iter3: YAML frontmatter mandate is incompatible with Jerry's native AST frontmatter parser, undisclosed [MAJOR]

**Principle:** No single HARD/MEDIUM rule text is directly violated (the document's own Non-Conflation argument correctly places ADRs outside H-33's literal "worktracker entity ops" scope), but this is a genuine methodological-rigor and completeness gap given the framework's stated AST-first tooling direction.

**Location and evidence:**

- `adr-standards-rule-draft.md:109-127` (Frontmatter Schema): mandates a YAML `---` block (`id:`, `type:`, `status:`, `scope:`, `origin_project:`, `origin_entity:`, `created:`, `supersedes:`, ...) for **every** future ADR, canonical and framework alike.
- `skills/ast/SKILL.md:51-52`: *"Frontmatter: Extract `> **Key:** Value` fields as a JSON object."* — the tool's documented scope is blockquote frontmatter, not YAML.
- `skills/ast/SKILL.md:99-107` (`jerry ast frontmatter` command spec): *"Extract all blockquote frontmatter fields as a JSON object."* No YAML-parsing path is documented.
- `docs/design/ADR-output-path-resolution-001.md:3-9` (one of the 3 live canonical framework ADRs this convention is meant to govern going forward): uses exactly the blockquote form (`> **Type:** adr`, `> **Status:** accepted`, `> **Parent:** EPIC-002`) — i.e., the format the framework's own AST tooling already parses.
- The ADR's own Migration Plan (`ADR:433`, M-11) concedes the 3 framework ADRs carry provenance only "informally" via HTML comments/blockquote `Parent:` keys, "**None carry the proposed YAML frontmatter schema**" — but does not address how the proposed L-5/L-6/L-7 lint rules (which read `scope`, `origin_project`, `promoted_to`, `superseded_by` from frontmatter) will be implemented against a format `jerry ast frontmatter` cannot read, nor whether the AST tool itself needs a YAML-parsing extension (a non-trivial, undisclosed scope addition to a "ratification blocker," M-6).

**Impact:** The package is otherwise extremely diligent about verifying tool/CLI reality (H-05 `uv run jerry` checks, `pyproject.toml:65` entrypoint verification, phantom-path detection in Fix 3) — this makes the blind spot on frontmatter parser compatibility notable by contrast. If M-6's lint script is meant to reuse Jerry's existing AST infrastructure (the natural, DRY choice, and the one implied by this agent's own AST-first execution guidance), a YAML-frontmatter ADR corpus requires either extending `jerry ast frontmatter` to a second grammar or writing and maintaining a parallel, bespoke YAML parser solely for ADRs — neither option is chosen, costed, or even named.

**Dimension:** Methodological Rigor, Completeness.

**Remediation:** Either (a) switch the Frontmatter Schema to the blockquote form already used by the 3 live framework ADRs (`> **id:** ADR-plugin-distribution-001`, etc.), which `jerry ast frontmatter` already parses with zero new tooling; or (b) explicitly scope a YAML-parsing extension to `jerry ast frontmatter`/`jerry ast validate` as a named, gating sub-item of M-6, with its own cost/owner. Option (a) is lower-risk and preserves the "no new tooling" framing the rest of the enforcement design relies on.

---

### CC-004-20260702-iter3: NAV-002 citation misattributed to cross-file CLAUDE.md registration [MINOR]

**Principle:** P-004 (Provenance/Traceability) — citations should point to the rule that actually governs the cited action.

**Location and evidence:**

- `adr-standards-rule-draft.md:3` (wrapper note): *"...is registered in **CLAUDE.md's Navigation table for discoverability (H-23 / NAV-002)**..."*
- `ADR-PROJ031-004-adr-identifier-convention.md` M-7 row (Migration Plan): *"Register the new rule file in **CLAUDE.md's Navigation table**... for **discoverability (H-23 / NAV-002)**..."*
- `.context/rules/markdown-navigation-standards.md` (NAV-002): *"Placement | Table SHOULD appear after frontmatter, before first content section."* — this governs where a document's **own** internal navigation table sits, not the separate act of listing that document inside a *different* file's (CLAUDE.md's) top-level Navigation table.

**Impact:** Low — the substantive correction both documents make (CC-002 in the ADR's own changelog: "the earlier 'registered per H-26' was wrong — H-26 governs skill, not rule-file, registration") is accurate and well-evidenced (CLAUDE.md's Navigation table does already list individual `.context/rules/*.md` files by name, confirming the registration claim itself). Only the specific NAV-002 citation is imprecise — NAV-002 is not the rule that mandates or governs cross-file registration in CLAUDE.md; that practice is an established precedent (`CLAUDE.md`'s own Navigation table, e.g. rows for `quality-enforcement.md`, `agent-development-standards.md`), not a codified NAV-numbered standard.

**Dimension:** Traceability.

**Remediation:** Change the citation to "(H-23; CLAUDE.md Navigation-table registration precedent — see rows for `.context/rules/quality-enforcement.md` etc.)" and drop the NAV-002 reference, or cite NAV-004 ("Coverage | All major sections (`##` headings) SHOULD be listed") if the intent was breadth-of-listing rather than placement.

---

## Remediation Plan

**P0 (Critical):**
- CC-001: Add "(once M-6 ships; not yet built as of 2026-07-02)"-style qualifiers at the four present-tense enforcement/verification claims (`ADR:54`, `ADR:341`, `rule-draft:11`, `rule-draft:38`), matching the honesty standard already applied at `ADR:554`/`rule-draft:187`.
- CC-002: Reword L-9 in both files from "FAIL (non-waivable-in-practice...)" to "FAIL (waivable-in-principle; see tier reconciliation)" and route it through the same `adr-lint-waivers.yaml` mechanism already specified for L-2/L-3/L-7.

**P1 (Major):**
- CC-003: Decide and disclose the frontmatter grammar for ADRs — either adopt the blockquote form (zero new tooling, matches the 3 live framework ADRs and `jerry ast frontmatter`) or add an explicitly-scoped, gating YAML-parsing extension to M-6.

**P2 (Minor):**
- CC-004: Fix the NAV-002 citation in both files to correctly reference the CLAUDE.md registration precedent rather than the internal-placement standard.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CC-003 (Major): frontmatter/tooling compatibility unaddressed |
| Internal Consistency | 0.20 | Negative | CC-001, CC-002 (both Critical): present-tense claims contradicted by later Claim-Status disclosures; L-2/L-3 tier fix not applied to L-9 |
| Methodological Rigor | 0.20 | Negative | CC-002, CC-003: an already-diagnosed defect pattern left unfixed in one instance; a real tooling gap in an otherwise very rigorous CLI-verification package |
| Evidence Quality | 0.15 | Negative | CC-001: the two headline claims are unsupported by (indeed contradicted by) the document's own later evidence |
| Actionability | 0.15 | Neutral | All four findings have narrow, mechanical, specifically-located fixes (no architectural rework required) |
| Traceability | 0.10 | Negative | CC-004: citation misattributes NAV-002 |

**Constitutional Compliance Score:** `1.00 - (2 × 0.10 + 1 × 0.05 + 1 × 0.02) = 1.00 - 0.27 = 0.73` → **REJECTED** (below the 0.85 floor; well below the 0.92 SSOT gate and the 0.95 engagement gate)

**Threshold Determination:** REJECTED. Both Critical findings have small, mechanical fixes (wording/qualifier edits, not architectural redesign) — this is a "fast revise," not a rebuild.

---

## Compliance Positives

Documented per P-022 (findings must not be minimized, but compliance should also not be under-reported):

- **P-020 (User Authority):** Status correctly `PROPOSED`; Meta-Note explicitly discloses the self-promotion path as "described, not performed... per P-020."
- **HARD Rule Ceiling discipline:** Constraint c-001 correctly cites the exact ceiling mechanics (25/25, max +3, one concurrent, 3-month reversion) and correctly declines to spend a ceiling-exception slot on a naming convention — this is the same discipline CC-002 finds inconsistently applied to L-9.
- **AE-002/AE-003 classification:** Correctly applies both as independent C3 floors (not additive to C4), with C4 justified instead by the tier definition itself — matches `quality-enforcement.md` Auto-Escalation Rules exactly.
- **H-23 nav tables:** Both files carry navigation tables; spot-checked anchor links (12+ entries across both files, including punctuation-heavy headings like "Options Considered (A–F)" and "Rationale — Answering the Crux Head-On") resolve correctly against GFM slug rules.
- **MEDIUM-tier vocabulary purity (bulk):** Case-sensitive scan of the rule draft for `MUST|SHALL|NEVER|FORBIDDEN|REQUIRED|CRITICAL` returns zero hits; all 13 ADR-M-### standards correctly use SHOULD/MAY/RECOMMENDED. L-9 (CC-002) is the one leak.
- **H-26 disclaimer:** The document's own CC-002-prior-iteration correction ("H-26 governs skill, not rule-file, registration; AGENTS.md is not a registration target") is accurate per `quality-enforcement.md`'s H-26 definition and per `AGENTS.md:1`'s stated scope (agent-persona registry).
- **Retired-Rule-ID tombstone precedent:** The ADR/rule-draft's promotion tombstone design (`promoted_from`/`promoted_to`/`superseded_by`, "NNN never reused") correctly mirrors the SSOT precedent's core principle (retired IDs are never reassigned) even though the mechanism is necessarily decentralized (per-file back-links) rather than a single central table — an appropriate adaptation given ADR volume vs. the small HARD-rule catalog.

---

## Execution Notes

- **Protocol steps completed:** 5 of 5 (S-007 template `.context/templates/adversarial/s-007-constitutional-ai.md`: Load Constitutional Context, Enumerate Applicable Principles, Principle-by-Principle Evaluation, Generate Remediation Guidance, Score Constitutional Compliance).
- **Deliverable type:** Governance/rule-convention documents (ADR + companion `.context/rules/` draft) → AE-002 (touches `.context/rules/` in spirit/destination) and AE-003 (new ADR) both apply, matching the deliverable's own C4/C3-floor self-classification.
- **Scope discipline:** This review is S-007 (Constitutional AI Critique) only — it does not attempt to re-verify the deliverables' extensive internal arithmetic (file counts, RPN figures, promotion-rate statistics), which is the proper domain of S-011 (Chain-of-Verification) / S-012 (FMEA) strategies also running in this tournament.
- **Blind protocol compliance:** No file under `.../adversary/` was read except this output file. No other reviewers' findings (any iteration) were consulted. No deliverable file was edited. All evidence above was independently gathered by reading the two deliverables plus supporting repo files (`.context/rules/*.md`, `skills/ast/SKILL.md`, `docs/design/ADR-output-path-resolution-001.md`) named explicitly in each citation.
- **P-022 self-check:** All claims above are cited to file+line; no adversary-directory content was read or referenced; no fabricated Task/Issue IDs or invented facts were introduced.

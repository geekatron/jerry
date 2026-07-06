# Constitutional Compliance Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 8, Post-Subtraction Package)

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverables reviewed |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Summary](#findings-summary) | Table of all findings |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, recommendation per finding |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Verified Clean (No Finding)](#verified-clean-no-finding) | Checks performed that passed |
| [Execution Statistics](#execution-statistics) | Protocol completion record |

---

## Execution Context

- **Strategy:** S-007 Constitutional AI Critique
- **Template:** `.context/templates/adversarial/s-007-constitutional-ai.md`
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
- **Criticality:** C4 (per the ADR's own AE-002/AE-003 C3-floor + C4-tier-definition basis)
- **Engagement Gate:** 0.95
- **Date:** 2026-07-06
- **Reviewer:** adv-executor (S-007, blind independent reviewer, iteration 8)
- **Constitutional Context:** `docs/governance/JERRY_CONSTITUTION.md` (P-001–P-043, principles P-001/P-002/P-003/P-004/P-011/P-020/P-021/P-022 read directly for this review); `.context/rules/quality-enforcement.md` (HARD Rule Index, Tier Vocabulary, HARD Rule Ceiling, Enforcement Architecture); `.context/rules/markdown-navigation-standards.md` (H-23/H-24); `CLAUDE.md` (Navigation table, auto-load description).
- **Framing per invoking task:** This package was just SLIMMED by a user-authorized subtraction pass (FEEDBACK-LOG FU.1). Per MEDIUM-tier vocabulary in quality-enforcement.md, descoped-with-honest-disclosure is treated as a VALID design posture in this review — findings below do NOT re-demand deleted machinery. Only genuine constitutional/tier/honesty issues in the package **as it now stands** are reported.

---

## Summary

**PARTIAL compliance, high rigor.** 0 Critical, 1 Major, 1 Minor. The package demonstrates unusually thorough P-022 discipline (nearly every empirical/interpretive claim in both deliverables is explicitly labeled as inference or disclosed as a residual), zero HARD-tier vocabulary in the MEDIUM-tier rule draft (grep-confirmed), compliant H-23 navigation tables in both files with resolving anchors, and an accurately-quoted P-020 ratification citation (verified against `FEEDBACK-LOG.md` FU.0 verbatim, including the preserved typo). The one Major finding is a specific, narrow claim: the rule draft's self-measured "L1 token-budget fits" reconciliation is unverified and appears to contradict `CLAUDE.md`'s own description of the auto-load mechanism. Constitutional compliance score: **0.93** (PASS the 0.92 SSOT floor; below the 0.95 engagement gate on this sub-score alone — see [Scoring Impact](#scoring-impact)). Recommendation: **ACCEPT with one targeted revision** (soften/hedge the CC-001 claim) before this package is folded into the tournament's overall score.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CC-001-iter008 | Major | L1 token-budget "fits" reconciliation is an unverified, under-hedged claim that appears contradicted by `CLAUDE.md`'s own auto-load description | `design/adr-standards-rule-draft.md:199` (footnote) |
| CC-002-iter008 | Minor | Stale frontmatter comment `(non-schema advisory field)` for `canonical_id` was not updated after the iter-4 fix that added the field to both Frontmatter Schemas | `decisions/ADR-PROJ031-004-adr-identifier-convention.md:15` vs `:362` |

---

## Detailed Findings

### CC-001-iter008: L1 Token-Budget Reconciliation Claim Under-Evidenced [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Principle** | P-011 (Evidence-Based Decisions) / P-022 (No Deception — confidence-level transparency) |
| **Tier** | MEDIUM (evidentiary-rigor gap, not an intentional deception) |
| **Section** | `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:199` |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — L1 token-budget-fit check specifically requested by the invoking task |

**Principle text (P-011, paraphrased from JERRY_CONSTITUTION.md):** decisions and claims SHALL be grounded in evidence, not unverified assumption presented as settled fact. **P-022 (verbatim, JERRY_CONSTITUTION.md:178-185):** "Agents SHALL NOT deceive users about: ... Confidence levels."

**Evidence:**

1. Rule draft, line 199: *"L1 budget (CC-002): `.context/rules/*.md` already measures ~26.9k words (~36k tokens), so the SSOT's ~12,500-token L1 figure is a curated/re-injected subset, not a raw corpus sum; this file's ~4.3k tokens / 242 lines ... is comparable to other substantive rule files and a bounded add."*
2. `.context/rules/quality-enforcement.md` Enforcement Architecture table: `"| L1 | Session start | Behavioral foundation via rules | Vulnerable | ~12,500 |"` — a specific token figure for what is loaded **at session start**, not a per-prompt re-injection figure (that is L2, ~850 tokens, separately listed).
3. `CLAUDE.md:49`: *"**(A)** = Auto-loaded into Claude Code context at session start via `.claude/rules/` symlink."* — and `CLAUDE.md:53`: `"| Coding/architecture/testing rules | `.context/rules/` (A) |"`. This is a plain statement that the **entire** `.context/rules/` directory (all 17 files, Glob-verified) is auto-loaded at session start — not a "curated subset."
4. Independent line-count sample across all 17 files in `.context/rules/` (Grep, non-blank lines): 2,288 non-blank lines total, dominated by dense table-heavy files (`quality-enforcement.md` 261, `agent-routing-standards.md` 418, `agent-development-standards.md` 353, `mcp-tool-standards.md` 182). This order-of-magnitude sample is consistent with — and does not refute — the rule draft's own "~26.9k words / ~36k tokens" corpus estimate, i.e., roughly **3x** the SSOT's stated ~12,500-token L1 figure, even before this new file is added.

**Analysis:** The claim "the ~12,500 figure is a curated/re-injected subset, not a raw corpus sum" is the *only* load-bearing explanatory assertion in either deliverable that is stated as settled fact without an inference/P-022 hedge, in a document that otherwise tags essentially every other empirical or interpretive claim explicitly (e.g., "DA-004... explicitly labeled qualitative order-of-magnitude, not a measured rate, P-022"; "IN-002... argued design advantage, not yet a demonstrated one"). Here, the one sentence that reconciles a real, material budget gap (actual corpus ≈3x the stated L1 figure) with the new file's "bounded add" framing is presented with unwarranted certainty, and it directly contradicts `CLAUDE.md`'s own plain-language description of what "(A)" auto-load means (the whole `.context/rules/` directory, not a curated subset). If `CLAUDE.md`'s description is accurate, the SSOT's ~12,500-token L1 figure has been stale/understated for some time — a pre-existing framework-wide issue this ADR did not create, but which its own honesty-note now surfaces and then talks past with an unverified counter-explanation rather than flagging as an open SSOT/CLAUDE.md reconciliation item. This does not invalidate the naming-convention decision itself, but it weakens the specific "plausibly installable against the ~12,500-token L1 budget" claim this review was asked to verify.

**Impact:** Understates the true marginal cost of installing this rule file and, more importantly, papers over a materially larger pre-existing L1-budget overrun with an assertion that isn't checked against the framework's own auto-load description — an Evidence Quality / Methodological Rigor gap inconsistent with the otherwise-rigorous P-022 labeling practiced everywhere else in this package.

**Recommendation:** Reword the line-199 footnote to (a) drop the unhedged "so the SSOT's ~12,500-token L1 figure is a curated/re-injected subset" clause, or explicitly tag it "(unverified inference, not checked against CLAUDE.md's auto-load description)"; and (b) disclose the ~12,500-vs-~36k-actual gap as a **pre-existing, unresolved SSOT/CLAUDE.md reconciliation item** (parallel in honesty-register to the AE-004 SSOT-authority disclosure already present at ADR line 565), rather than asserting it is already explained away. This is a one-sentence edit, consistent with the subtraction doctrine (delete/soften the overclaim; add no new machinery).

---

### CC-002-iter008: Stale `canonical_id` Frontmatter Comment [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Principle** | Internal Consistency (deliverable self-consistency; not a HARD/MEDIUM constitutional rule per se) |
| **Tier** | SOFT (documentation-polish gap) |
| **Section** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:15` vs `:362` |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

1. Line 15 (YAML frontmatter): `canonical_id: ADR-adr-convention-001  # declared remap target (non-schema advisory field; see Meta-Note)`.
2. Line 362 (Meta-Note section): *"**`canonical_id` is an OPTIONAL advisory field (IN-006/FM-007 fix, iter-4, P-022).** ... this ADR's own frontmatter (`:15`) uses `canonical_id: ADR-adr-convention-001` — a field the published schema did not define... **Corrected:** `canonical_id` is now a documented, optional, null-by-default advisory field in **both** this schema and the companion rule draft's Frontmatter Schema."*
3. Both Frontmatter Schema blocks (ADR line ~355, rule draft line ~115) now list `canonical_id` as a documented schema field.

**Analysis:** The iter-4 fix (already recorded in the changelog) added `canonical_id` to the documented schema in both deliverables, which is exactly the right remediation — but the frontmatter comment at line 15 that originally motivated the fix ("non-schema advisory field") was left unchanged. It now reads as self-contradictory alongside line 362, which explicitly states the field **is** now part of the documented schema (merely optional/advisory *within* that schema, not outside it). This is the same class of small propagation gap the document elsewhere catches and fixes for itself (e.g., the M-14 dangling cross-reference cleanup, FM-001-iter6) — it simply wasn't caught for this one comment.

**Impact:** Cosmetic/internal-consistency only. Does not affect the decision, the lint spec, or any HARD/MEDIUM tier claim; a careful reader following the `:15`→Meta-Note trail will resolve the apparent contradiction correctly, but the comment itself is inaccurate as written.

**Recommendation:** Change line 15's comment from `(non-schema advisory field; see Meta-Note)` to `(optional advisory schema field; see Meta-Note)` — a one-word fix, no new machinery.

---

## Remediation Plan

**P0 (Critical):** None.

**P1 (Major):** CC-001-iter008 — reword the rule-draft line-199 L1-budget footnote to hedge or retract the "curated/re-injected subset" claim and disclose the ~12,500-vs-~36k gap as a pre-existing, open SSOT/CLAUDE.md reconciliation item.

**P2 (Minor):** CC-002-iter008 — fix the stale `canonical_id` frontmatter comment at ADR line 15.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Both deliverables are complete relative to the ratified, post-subtraction scope; no missing required section found. |
| Internal Consistency | 0.20 | Negative (Minor) | CC-002: one stale frontmatter comment contradicts the Meta-Note's own correction. |
| Methodological Rigor | 0.20 | Negative (Major) | CC-001: the one un-hedged empirical claim in an otherwise heavily inference-labeled package. |
| Evidence Quality | 0.15 | Negative (Major) | CC-001: the L1-budget reconciliation is asserted, not verified, and conflicts with `CLAUDE.md`'s own auto-load description. |
| Actionability | 0.15 | Neutral | Both findings have specific, one-line remediation actions consistent with the subtraction doctrine. |
| Traceability | 0.10 | Positive | Every checked citation (FEEDBACK-LOG FU.0 quote, CLAUDE.md:54-56, `.github/workflows/ci.yml:2`, `ADR-STORY015-001` path, `ADR-PROJ031-003` anchor, `skills/architecture/SKILL.md:105,284,437`, `scripts/lint_adr_convention.py` absence) verified accurate on independent inspection. |

**Constitutional Compliance Score:** `1.00 - (0.10*0 + 0.05*1 + 0.02*1) = 0.93`

**Threshold Determination:** PASS the SSOT 0.92 floor; **below** the 0.95 engagement gate on this constitutional sub-score alone. Recommend the one-line CC-001 fix before the package is scored for the 0.95 gate.

---

## Verified Clean (No Finding)

Independently re-verified during this blind pass (evidence-based, no finding raised):

- **MEDIUM-tier purity:** zero occurrences of `MUST|SHALL|NEVER|FORBIDDEN|REQUIRED|CRITICAL` (uppercase, word-boundary) in `design/adr-standards-rule-draft.md` (Grep-confirmed). The ADR's own `MUST` usages are confined to its Nygard "Constraints" section (c-001…c-007, process constraints on the decision itself) and to one-time execution directives (M-9 atomicity), not the naming convention's own normative vocabulary — legitimate ADR-genre usage, not a tier-purity violation.
- **H-23 navigation tables:** both deliverables carry a `## Document Sections`/`## Navigation` table with anchor links; spot-checked anchors (`#options-considered-af`, `#rationale--answering-the-crux-head-on`, `#l5-ci-lint-specification`, `#relationship-to-worktracker-dec-nnn`) resolve correctly against actual heading slugs.
- **P-020 ratification:** the quoted ratification — *"I ratify the promotion-is-the-point apporach and lock Scheme B."* — matches `FEEDBACK-LOG.md` FU.0 verbatim, including the preserved typo ("apporach") and the DONE disposition.
- **P-022 Claim-Status honesty:** `scripts/lint_adr_convention.py` confirmed absent (Glob); `docs/design/README.md` and `docs/adrs/README.md` confirmed absent (Glob) — consistent with "TBD-Task"/"designed-not-built" framing; no enforcement-achieved language found describing either.
- **Citation spot-checks (all accurate):** `.github/workflows/ci.yml:2` dangling `ADR-CI-001` reference confirmed verbatim; `projects/PROJ-001-plugin-cleanup/` confirmed absent (dangling target); `ADR-STORY015-001` confirmed living at `projects/PROJ-024-tactical-work/.../STORY-015-tier-model-renumbering/` with no `decisions/` segment (R-10 claim accurate); `ADR-PROJ031-003-credential-protection-supply-chain.md#claim-status-convention-p-022--foundational` anchor confirmed present; `skills/architecture/SKILL.md:105,284,437` `ADR_NNN`/`ADR-{NUMBER}` citations confirmed still present verbatim; `CLAUDE.md:54-56` three-rule-file citation and "3 of 17 named" ratio confirmed exact (17 files in `.context/rules/`, Glob-confirmed).
- **AE-002/AE-003/AE-004 usage:** matches `.context/rules/quality-enforcement.md` Auto-Escalation Rules table verbatim; the Path-1=C3/Path-2=C4 interpretive split is explicitly disclosed as this ADR's own interpretation pending SSOT harmonization (not asserted as ratified SSOT) — no finding.
- **HARD Rule Ceiling (25/25):** matches SSOT exactly; no new HARD rule proposed anywhere in either deliverable.

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 0
- **Major:** 1
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Load Constitutional Context; Enumerate Applicable Principles; Principle-by-Principle Evaluation; Remediation Guidance; Score Constitutional Compliance)
- **Blind protocol observed:** no files under `.../adversary/` read except this report's own destination; no deliverable files edited (owner-only per mandate); no subagents spawned (P-003).

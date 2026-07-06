# Constitutional Compliance Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention Design

> **Strategy:** S-007 Constitutional AI Critique
> **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + all files in `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` (`feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md`)
> **Criticality:** C4 (engagement gate 0.95, user-set)
> **Date:** 2026-07-06
> **Reviewer:** adv-executor (S-007 iteration 1, blind protocol)
> **Constitutional Context:** `docs/governance/JERRY_CONSTITUTION.md` (P-001, P-002, P-003, P-020, P-021, P-022 loaded); `.context/rules/quality-enforcement.md` (Tier Vocabulary, HARD Rule Index, HARD Ceiling); `.context/rules/markdown-navigation-standards.md` (H-23)

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All CC-NNN findings |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 remediation |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Also Examined — No Violation Found](#also-examined--no-violation-found) | Checked-and-cleared items (P-022 disclosure) |

---

## Summary

**PARTIAL compliance.** 1 Critical, 3 Major, 2 Minor. Constitutional compliance score: **0.71 → REJECTED** (< 0.85; well below the 0.95 engagement gate). The package's MEDIUM-tier, minimal-machinery posture is itself sound and consistent with the anti-bloat doctrine (descoped-with-disclosure is legitimate and I found no HARD-rule additions, no ceiling breach, and strong H-23 nav-table compliance across all five files). The rejection is driven by one headline overclaim (the L0 "guarantee" sentence) and a recurring pattern of present-tense "already backed by a hook / already ratified" language that contradicts the document's own, correctly-hedged Proposed-Defaults framing elsewhere. **Recommendation: REVISE** — all findings have narrow, one-line fixes; no architectural rework required.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260706-i1 | P-022 No Deception (overclaimed coverage) | HARD | **Critical** | `design/feedback-decision-log-convention-design.md:30` — "guarantee ... survive" claim contradicts the document's own MEDIUM/SHOULD framing | Internal Consistency |
| CC-002-20260706-i1 | P-022 / P-020 (premature "ratified"/"hook-backed" language) | HARD-adjacent | Major | `design/.../feedback-decision-log-convention-design.md:81,186,223-224` | Internal Consistency |
| CC-003-20260706-i1 | Tier Vocabulary discipline (quality-enforcement.md) | MEDIUM (self-declared) | Major | `staging-feedback-logs/feedback-decision-logs-standards.md:26-27` — "never duplicate", "never reset" | Internal Consistency |
| CC-004-20260706-i1 | Public-repo hygiene / P-022 (verification-completeness overclaim) | HARD-adjacent | Major | `design/.../feedback-decision-log-convention-design.md:70,154(row2),290` — un-redacted `DJ-025`, `OI-019`, `DJ-NNN`, `R{round}-FU.{n}` | Evidence Quality |
| CC-005-20260706-i1 | Repo rule-writing convention (MEDIUM row format) | SOFT | Minor | `staging-feedback-logs/feedback-decision-logs-standards.md:23-28` | Methodological Rigor |
| CC-006-20260706-i1 | Evidence reproducibility | SOFT | Minor | `design/.../feedback-decision-log-convention-design.md:180` — token count unverifiable | Evidence Quality |

**Finding ID Format:** `CC-{NNN}-20260706-i1` (execution date + iteration 1).

---

## Finding Details

### CC-001-20260706-i1: L0 Executive Summary overclaims a capture "guarantee" [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L0: Executive Summary |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) |

**Evidence:**

`design/feedback-decision-log-convention-design.md:30`:
> "We are turning an un-codified, entirely-manual [internal-kb] pattern into a real, lightweight Jerry convention: **two append-only markdown ledgers** that **guarantee** user feedback and human↔LLM decisions **survive** context compaction, session boundaries, and model swaps."

This is the single most prominent claim in the document — the first substantive sentence of the executive summary, which per H-23/NAV conventions is what a reader consumes first. Directly contradicted by the same document's own later disclosures:

- Line ~81 (L1.1 Capture triggers): "The rule is **MEDIUM (SHOULD)** — it cannot be HARD (ceiling 25/25) ... so the obligation does not depend on the model remembering." — i.e., today, capture *is* a SHOULD-tier convention with no deterministic enforcement.
- `hook-design-note.md` Feasibility verdict (line 55): the provenance/reminder hook that would make capture harness-backed is "**designed in v1** ... but **shipped as a separate gated change** ... The manual MEDIUM convention ... governs capture until the hook lands."
- Line 38 (Governing principle, correctly hedged elsewhere in the same document): "**what depends on the model remembering will eventually be forgotten**" — the document's own thesis is that *without* the hook, forgetting is the expected failure mode, not something guaranteed against.
- The document's own restated goal at line 40 and Improvement Ledger row 1 (line 221) is "so that we don't lose feedback" (an aspiration under active construction) — confirming the intended reading of line 30 is the strong one (capture is guaranteed), not merely "once written, files persist."

**Analysis:** Read charitably, "guarantee ... survive" could mean only that an *already-captured* entry survives compaction/session/model-swap (true and trivial — that is what file persistence means, per P-002). Read as the document itself frames its own purpose everywhere else ("so that we don't lose feedback," "requires enforcement, not a wish"), the natural and almost certainly intended reading is the strong one: *feedback will not be lost*. As specified for v1 shipping (no hook; MEDIUM/SHOULD rule only), that stronger guarantee is not delivered — capture depends entirely on the model remembering to append an entry in the same turn, exactly the failure mode the document elsewhere identifies as inevitable without harness backing. This is a P-022 (No Deception, HARD-tier: "Agents SHALL NOT deceive users about ... Capabilities or limitations") violation in the deliverable's own headline claim — the exact "overclaimed coverage" pattern flagged for Critical treatment in this review's scope.

**Recommendation:** Reword line 30 to scope the guarantee to persistence-of-captured-entries, and explicitly flag that capture itself is best-effort (SHOULD-tier) pending Q3. Example: *"...two append-only markdown ledgers designed so that, once an entry is captured, it survives context compaction, session boundaries, and model swaps. Capture itself is a MEDIUM (SHOULD) convention today; a fail-open hook that would make capture harness-backed is designed (L1.3) but ships separately, pending Q3 ratification."*

---

### CC-002-20260706-i1: Recurring present-tense "already ratified" / "already hook-backed" language contradicts the document's own Proposed-Defaults framing [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1.1 Capture triggers; L2 rule-preview table; Improvement Ledger |
| **Strategy Step** | Step 3 |

**Evidence:**

1. `design/.../feedback-decision-log-convention-design.md:81`: "The rule is MEDIUM (SHOULD) ... and **is backed by** a fail-open capture hook (L1.3) so the obligation does not depend on the model remembering." — present tense, no hedge, even though the hook is Q3-pending / not shipped in v1.
2. `design/.../feedback-decision-log-convention-design.md:186` (L2 rule-preview table, LOG-M-003 row): "assistant per **the ratified verbatim policy**." — the assistant-verbatim policy is explicitly a PROPOSED-DEFAULT (Q1), not yet ratified, per the same document's own "Proposed Defaults (Pending Ratification)" table.
3. Improvement Ledger rows 3-4 (lines ~223-224): "**Harness-stamped** provenance sidecar; model resolved per-turn from transcript" and "Turn model: `{session_id}#{promptId}` + **hook ordinal**" — both stated as already-delivered improvements, again without the Q3 "designed, not shipped" hedge.

Contrast with correctly-hedged instances of the *same* content elsewhere in the package: `FEEDBACK-LOG.template.md:22` ("**When** the provenance hook is installed, the assistant stamps this; otherwise fill what you know") and `LLM-DECISION-LOG.template.md:27` ("Assistant-verbatim policy **is a PROPOSED-DEFAULT** ... pending user ratification"). These prove the correct hedged phrasing was known and used — the four locations above are inconsistent outliers, not a document-wide failure to disclose.

**Analysis:** This is a real, recurring internal-consistency defect (four occurrences, not one slip) and touches both P-022 (present-tense capability claims about an unshipped mechanism) and P-020 (treating an unratified default, Q1, as already "ratified" pre-empts the user's explicit ratification step). Because the correct hedge is demonstrably present elsewhere in the same package, this is a low-cost, mechanical fix rather than a design defect.

**Recommendation:** Apply the same "(PROPOSED-DEFAULT / not yet shipped — see Q1/Q3)" hedge consistently at all four locations, mirroring `LLM-DECISION-LOG.template.md`'s phrasing.

---

### CC-003-20260706-i1: HARD-tier keyword ("never") embedded in rows declared pure MEDIUM/SHOULD [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `staging-feedback-logs/feedback-decision-logs-standards.md` — MEDIUM Standards table |
| **Strategy Step** | Step 3 |

**Evidence:**

`feedback-decision-logs-standards.md:26-27`:
> "LOG-M-004 | **Cross-link, never duplicate** worktracker `DEC-NNN` / ADRs..."
> "LOG-M-005 | **Logger-assigned ids:** ... unique, monotonic per log across segments, **never reset**. ..."

The same file's own preamble (line 3) and the design doc (line 178-180) both state the explicit design intent: *"The HARD ceiling is 25/25 with zero headroom ... so a 'MUST log' rule is impossible ... The convention ships as a MEDIUM (SHOULD) rule file."* `.context/rules/quality-enforcement.md` Tier Vocabulary table classifies `NEVER` as a **HARD**-tier keyword (`MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL`), on par with `MUST`/`SHALL`, not `SHOULD`.

**Analysis:** The author was demonstrably aware of and actively avoiding HARD-keyword collision (no literal `MUST`/`SHALL` appear anywhere in the five staged/design files outside `hook-design-note.md`'s out-of-band hook-behavior spec — see [Also Examined](#also-examined--no-violation-found)). `NEVER`, however, slipped into two of the six MEDIUM rows, undermining the very discipline the document set out to enforce. This creates a genuine tier-vocabulary ambiguity: a reader (or an L5 lint author) cannot tell from the rule text alone whether LOG-M-004/LOG-M-005 are meant to be un-overridable (which would functionally smuggle a HARD constraint into the 25/25-constrained system without a registered H-ID) or merely strongly-worded SHOULD items. Given this framework's demonstrated literalism about tier keywords (the entire HARD Rule Ceiling Derivation apparatus exists because of exactly this kind of keyword-to-enforcement mapping), this is not a stylistic nitpick.

**Recommendation:** Replace "never duplicate" → "SHOULD NOT duplicate" and "never reset" → "does not reset (monotonic by design)" in LOG-M-004/LOG-M-005.

---

### CC-004-20260706-i1: Un-redacted internal work-item identifiers remain in the in-scope design doc despite a "ZERO internal tokens, verified" sanitization claim [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0 Executive Summary; Id scheme (L1.1); Improvement Ledger; References |
| **Strategy Step** | Step 3 |

**Evidence:**

In-scope `design/feedback-decision-log-convention-design.md` retains, unredacted:
- Line 70: "`DJ-025` collision"
- Line ~222 (Improvement Ledger row 2): "`DJ-025` records an id collision"
- Line 290 (References): "`DJ-NNN` template, `DJ-025` collision, `OI-019`"
- Line ~221 (Improvement Ledger row 1) and line 36: "`OI-019`"

`DJ-NNN`/`DJ-025` and `OI-019` are internal-KB decision-journal and outstanding-item identifiers (confirmed by `research/feedback-decision-log-research.md:134,138,153-154`), i.e., exactly the class of artifact this project's own FU.4 disposition (allowed-context evidence, `FEEDBACK-LOG.md:91`) claims to have swept: *"5 files sanitized (employer → `[employer]`, internal KB → `[internal-kb]`, internal doc ids → `[internal-doc-A/B]`, codenames → `[codename-A/B]`, **work-item ids → `[ado-id-1/2]`**) ... staged-content grep verified **ZERO internal tokens** and ZERO personal paths before push."*

**Analysis:** `DJ-025`/`OI-019` fall squarely in the disclosed "work-item ids" redaction category, yet were not bracketed like `[internal-doc-A/B]`/`[codename-A/B]` in this same-corpus deliverable. This is either (a) a gap in the sweep that contradicts the "ZERO internal tokens ... verified" claim, or (b) an undocumented judgment call that these particular bare alphanumeric codes were deemed non-sensitive and out of scope for redaction. Either way it is currently undisclosed and inconsistent with the stated taxonomy. Materiality is low (neither code discloses the employer's name or proprietary system), but the *claim* of complete, verified sanitization is what is at issue, not the codes themselves — a P-022 concern about the accuracy of a verification claim, not a severe data-leak.

**Recommendation:** Either (a) apply the same bracket convention (e.g., `[legacy-id-1]`) to `DJ-025`/`OI-019`/`DJ-NNN`/`R{round}-FU.{n}` for consistency, or (b) add one line documenting why these specific identifiers were judged out of scope for the FU.4 sweep, so the "ZERO internal tokens" claim and this document's residual citations don't read as contradictory.

---

## Recommendations

**P0 (Critical):**
- CC-001: Reword the L0 "guarantee ... survive" sentence to scope it to persistence-of-captured-entries and explicitly flag capture as MEDIUM/SHOULD pending Q3 (see rewrite above).

**P1 (Major):**
- CC-002: Add "(PROPOSED-DEFAULT / not shipped — see Q1/Q3)" hedges at `feedback-decision-log-convention-design.md:81`, `:186`, and Improvement Ledger rows 3-4, matching the correct phrasing already used in `LLM-DECISION-LOG.template.md`.
- CC-003: Replace "never duplicate" / "never reset" in LOG-M-004/LOG-M-005 with SHOULD-safe phrasing ("SHOULD NOT duplicate," "does not reset (monotonic by design)").
- CC-004: Apply the `[legacy-id-1]`-style bracket convention to `DJ-025`/`OI-019`/`DJ-NNN`/`R{round}-FU.{n}` in the design doc, or document the deliberate exclusion.

**P2 (Minor):**
- CC-005: Add an explicit "SHOULD" into each LOG-M-00X row text in `feedback-decision-logs-standards.md` (currently only the file preamble carries the modal), matching the per-row SHOULD convention used in `mcp-tool-standards.md`, `agent-development-standards.md`, and `agent-routing-standards.md` MEDIUM tables.
- CC-006: Cite the tool/command used to produce the "~1,584 tokens by tiktoken cl100k" figure (`design/.../feedback-decision-log-convention-design.md:180`) for reproducibility, or footnote it as an estimate.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CC-004 (Major): public-repo redaction sweep incomplete for one identifier class within the in-scope package |
| Internal Consistency | 0.20 | Negative | CC-001 (Critical): headline "guarantee" claim contradicts the document's own MEDIUM/SHOULD + unshipped-hook framing. CC-002 (Major): 4 present-tense "ratified"/"hook-backed" instances contradict Proposed-Defaults framing used correctly elsewhere. CC-003 (Major): HARD keyword "never" inside a self-declared pure-MEDIUM rule set |
| Methodological Rigor | 0.20 | Negative | CC-005 (Minor): LOG-M-00X rows depart from established repo MEDIUM-row convention (explicit per-row SHOULD) |
| Evidence Quality | 0.15 | Negative | CC-004 (Major): "ZERO internal tokens, verified" claim contradicted by residual identifiers. CC-006 (Minor): token-count claim not independently verifiable, no method cited |
| Actionability | 0.15 | Neutral | All findings carry specific, one-line fixes; no architectural rework implied |
| Traceability | 0.10 | Neutral | Citations, References section, and cross-links are strong and consistent throughout the package |

**Constitutional Compliance Score:** `1.00 - (1×0.10 + 3×0.05 + 2×0.02) = 1.00 - 0.29 = 0.71`

**Threshold Determination:** **REJECTED** (< 0.85 band; well below the 0.92 SSOT threshold and the 0.95 engagement gate). Per the S-007 decision rule, the single HARD-tier (Critical) finding alone blocks acceptance (H-13); the 3 Major findings independently would recommend rejection/revision. All findings have narrow, evidence-scoped, one-line remediations — this is a REVISE-and-reverify situation, not a redesign.

---

## Also Examined — No Violation Found

In the interest of not overclaiming coverage in my own report (P-022):

- **`hook-design-note.md`'s four `MUST NOT` / `MUST` instances** were examined against "MEDIUM-tier purity." These are implementation-spec constraints on the *hook's own future behavior* (a not-yet-registered, separately-gated artifact per Q3 — "Design-only. No framework path is touched by this note."), not an attempt to register a new H-rule or touch the 25/25 HARD ceiling. No finding raised.
- **H-23 navigation tables** across all five files: verified every `##`/`###` heading referenced in each file's nav table resolves to the correct GitHub-flavored anchor slug (including non-trivial cases with colons, parentheses, slashes, and periods, e.g. `feedback-decision-log-convention-design.md`'s `#l2-governance--migration`, `hook-design-note.md`'s `#seam-2-capture-reminder-stop--precompact`). All pass. No finding raised.
- **P-020 (4 open questions)**: confirmed exactly 4 questions (Q1-Q4) remain marked PROPOSED-DEFAULT / pending ratification in the "Proposed Defaults (Pending Ratification)" table, and the staged templates/rule file correctly gate on this status in the majority of instances (the exceptions are captured in CC-002). Staging everything under `design/staging-feedback-logs/` pending approval, with no framework path touched, is the correct P-020 posture, not a violation.
- **Absolute path / employer-reference leakage**: no `[home]/` paths and no `[employer]`/employer-name references found anywhere in the in-scope design doc or the five staged files.
- **HARD ceiling (25/25)**: the deliverable does not propose a new H-rule ID and does not modify the ceiling count; its own accurate citation of "25/25, zero headroom" matches the current SSOT state in `quality-enforcement.md`.

---

## Execution Statistics
- **Total Findings:** 6
- **Critical:** 1
- **Major:** 3
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5

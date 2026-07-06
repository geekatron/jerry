# Constitutional Compliance Report: FEEDBACK-LOG / LLM-DECISION-LOG Convention (Iteration 8, VERIFIED-CRITICALS)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-007 automated execution), blind protocol, VERIFIED-CRITICALS
**Constitutional Context:** `quality-enforcement.md` (HARD Rule Index, tier vocabulary, AE-001–AE-006e, HARD ceiling 25/25), `markdown-navigation-standards.md` (H-23), `agent-development-standards.md` (CB-05, CP-01 citations verified). Independently re-verified all 6 restore-notes.md closure claims (iteration-006 Criticals RT-001, DA-001/FM-006, PM-001/IN-001, PM-002, FM-001, FM-003) against current deliverable text: **zero regressions confirmed.**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional compliance assessment |
| [Regression Check](#regression-check) | Independent re-verification of the 6 restore-notes closures |
| [Findings Table](#findings-table) | All new findings with severity |
| [Finding Details](#finding-details) | Expanded finding write-ups |
| [Recommendations](#recommendations) | Prioritized remediation |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping + Step-5 compliance score |

---

## Summary

**PARTIAL-to-COMPLIANT.** Zero Critical findings survive independent re-derivation. One new Major finding (CC-001): a self-contradiction internal to the *shipped* rule file between the LOG-M-006 near-cap id-minting shortcut (which trusts a Segment-Index row's displayed starting id) and the same file's own L5-Lint Scope-Limits disclosure (item e) that Segment-Index display accuracy is explicitly unverified — the two provisions are not cross-referenced, and the design doc's safer fallback ("read the actual last heading") is not carried into the shipped standard. Two Minor (cosmetic) findings. No HARD-rule (H-23, tier-vocabulary purity, P-020 draft-only, ceiling-untouched) violations found anywhere in the 6 files. **Recommendation: ACCEPT with one Major remediation** (CC-001) recorded as a required propagation fix before/at install, consistent with this package's own established remediation pattern (propagate the safer method into the shipped artifact); Minor items are optional polish.

---

## Regression Check

Independently re-verified (not merely trusting the owner's restore-notes.md) each of the 6 iteration-006 Critical closures against the **current** text of the deliverable:

| # | Finding | Verified closed in current text? | Evidence (file:line) |
|---|---------|-----------------------------------|------------------------|
| 1 | RT-001 (redaction laundering) | **YES** | `design/feedback-decision-log-convention-design.md:65` ("named the redaction **category**... and **approximate size**... a redaction whose span is disproportionate to its stated category is a named signal to scrutinize"); `design/staging-feedback-logs/feedback-decision-logs-standards.md:24` (same category+size+"presence, not veracity" language) |
| 2 | DA-001/FM-006 ("Four" safety functions) | **YES** | `design/feedback-decision-log-convention-design.md:264` ("**Five** safety functions... **and the Segment-Index-overflow re-assessment (L1.4)**... explicitly exempt") |
| 3 | PM-001/IN-001 (AE-006e overclaim) | **YES (closed by disclosure)** | `design/feedback-decision-log-convention-design.md:195` and `.../feedback-decision-logs-standards.md:28` (both state "AE-006e fires on *compaction*... not on... line-growth... so it does not detect cap-crossing") — verified against `.context/rules/quality-enforcement.md` AE-006e definition; no overclaim remains |
| 4 | PM-002 (`~N sessions` placeholder) | **YES** | `design/feedback-decision-log-convention-design.md:260` ("~3 sessions or 30 days since this review round, or the next milestone checkpoint — whichever comes first") |
| 5 | FM-001 (inline-doc dedup) | **YES** | `.../feedback-decision-logs-standards.md:51`; `.../FEEDBACK-LOG.template.md:25`; `.../examples-appendix.md:169` (all three state the check-before-mint-on-existing-`source:inline-doc`-path/anchor rule) |
| 6 | FM-003 (split-entry vs. "verbatim and full") | **YES** | `design/feedback-decision-log-convention-design.md:58`; `.../feedback-decision-logs-standards.md:24` (both permit a multi-item message to split into per-item entries, noted in Summary) |

**Zero regressions.** All 6 iteration-006 Criticals remain closed against the text actually shipped in this iteration-8 snapshot.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-i8 | P-022 (no deception via omission) / LOG-M-005 id-integrity self-consistency | MEDIUM (deliverable's own rule) | Major | `feedback-decision-logs-standards.md:28` vs. `feedback-decision-logs-standards.md:85` | Internal Consistency |
| CC-002-i8 | H-23 adjacent / diagram-prose fidelity | SOFT (cosmetic) | Minor | `feedback-decision-logs-standards.md:41` vs. `feedback-decision-logs-standards.md:50` | Internal Consistency |
| CC-003-i8 | P-022 (citation precision) | SOFT (cosmetic) | Minor | `feedback-decision-logs-standards.md:28` vs. `.context/rules/quality-enforcement.md` AE-006 table | Traceability |

**No Critical findings.** No H-23 nav-table defect, no tier-vocabulary (HARD-keyword) leakage into the MEDIUM-tier rule file, no P-020 draft-only violation (no framework-path writes), no ceiling touch, no hygiene leak (no `[home]/` paths, no un-genericized employer-internal tokens) found in any of the 6 reviewed files.

---

## Finding Details

### CC-001-i8: Shipped-rule-file self-contradiction — id-minting shortcut trusts a value the same file discloses as unverified [MAJOR]

**Principle:** Internal Consistency (S-014 dimension) / P-022 (no deception — an omission that lets a reader over-trust an undisclosed-risk shortcut) / the deliverable's own LOG-M-005 id-integrity guarantee ("unique, monotonic... under a single-writer-per-log append discipline").

**Location:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:28` (LOG-M-006) vs. same file, `feedback-decision-logs-standards.md:85` (L5 Lint, Scope limits, item (e)).

**Evidence — quote 1 (line 28, LOG-M-006):**
> "...and at or near cap (within ~5 entries), derive the next id as *the ACTIVE segment's starting canonical id (from its Segment-Index row) + a `grep -c '^## FU\.'` / `'^## DEC-LLM-NNN'` count* — the bare count is file-local, not the global id, so the offset is required after the first segment or the shortcut re-mints an earlier segment's id (DA-001-iter7) — not an LLM Read of a possibly-truncated file (PM-002)."

**Evidence — quote 2 (line 85, L5 Lint Scope limits, item e):**
> "(e) **Segment Index display accuracy** — the displayed `id-range` per row is not checked against the segment's true first/last heading (lint 2 derives contiguity from headings directly), so a stale index row can sit undetected (PM-003-i6);"

**Impact:** LOG-M-006's SHOULD-tier guidance tells the assistant/operator to compute the load-bearing "next canonical id" using the Segment-Index row's *displayed* starting id as one input. The very same file, 57 lines later, discloses that this displayed value is **not cross-checked** against ground truth and "a stale index row can sit undetected." The two statements are never cross-referenced anywhere in the package. A reader following LOG-M-006's recommended shortcut has no warning that its key input carries exactly the staleness risk the Scope-Limits section names. If the row's starting id is ever wrong (e.g., a manual edit, or a future automation defect), the shortcut mints a duplicate or gapped id — precisely the collision-class defect this whole convention exists to prevent (Improvement Ledger item 2: "pre-empts the observed collision class"). The error surfaces only after the fact, at the next commit-time lint run (lint 2), by which point an entry has already been committed under a wrong id.

**Compounding factor:** The design doc (`feedback-decision-log-convention-design.md:195`) discloses a strictly safer alternative for the *same* decision point — "Equivalently, drop the shortcut and read the ACTIVE file's actual last `## FU.N` heading — which carries the true global id and needs no arithmetic" — but this fallback is **not carried into the shipped rule file** (`feedback-decision-logs-standards.md:28`), which is the artifact that actually governs runtime behavior once installed (per the design doc's own Adoption plan, step 3: only the rule file, not the design doc, moves to `.context/rules/`). Describing the two methods as "Equivalently" interchangeable (design doc) also somewhat understates that the shortcut alone (as shipped) carries a risk the direct-read alternative does not.

**Note on scope (fairness to the deliverable):** this is a narrow, edge-case risk — it only matters within ~5 entries of a segment cap, and it requires the ACTIVE row's *starting* id (fixed once at rotation under the parity-checked rotation procedure) to already be wrong, which is not the everyday case the Scope-Limit (e) disclosure is chiefly warning about (that disclosure more naturally concerns sealed-segment *ending*-id display drift). It does not put verbatim feedback/decision content at risk of loss — only id uniqueness, a supporting mechanism. This is why the finding is scored Major, not Critical.

**Recommendation:** Either (a) add one clause to LOG-M-006 in the shipped rule file cross-referencing the Scope-Limits (e) caveat and recommending the direct-heading-read method as the safe default near cap (promoting the design doc's already-written fallback into the artifact that ships), or (b) if the shortcut is kept as the primary method, add an explicit sentence disclosing that it depends on Segment-Index display accuracy, which the same file's Scope-Limits (e) states is unverified. Either fix is a wording-only change consistent with this package's own anti-bloat, zero-new-machinery remediation pattern used in all 7 prior rounds.

---

### CC-002-i8: Entry-lifecycle diagram renders `IN-PROGRESS` as `IN_PROGRESS` (underscore vs. hyphen) [MINOR]

**Location:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:41-45` (the `stateDiagram-v2` block) vs. `feedback-decision-logs-standards.md:50` (prose immediately below it).

**Evidence:** Diagram states: `OPEN --> IN_PROGRESS`, `IN_PROGRESS --> DONE: evidence link`, `IN_PROGRESS --> WONTFIX: reason` (lines 41, 44-45). Prose directly below: "**Disposition** `OPEN / IN-PROGRESS / DONE / WONTFIX` (diagram): terminal states carry an evidence link..." (line 50) — hyphenated, matching every other reference to this disposition value across all 6 files (e.g., `design doc` L1.1 entry-schema table, both templates' Log-Conventions bullets).

**Impact:** Cosmetic only — almost certainly a Mermaid syntax accommodation (state names commonly avoid literal hyphens), not a substantive claim that a fifth state exists. Does not block any of the four purpose pillars. Included per the task's "cosmetic = Minor" instruction rather than omitted, since the diagram is a load-bearing FU.10 artifact the user specifically requested and a first-time reader could momentarily wonder whether `IN_PROGRESS` is a distinct value from `IN-PROGRESS`.

**Recommendation:** Cosmetic polish only, optional: add a one-line diagram caption noting `IN_PROGRESS` in the diagram = `IN-PROGRESS` in the Disposition enum, or omit remediation entirely (low value for the wording cost).

---

### CC-003-i8: AE-006e citation slightly conflates "compaction event" with "context-fill event" [MINOR]

**Location:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:28`; same phrasing also at `design/feedback-decision-log-convention-design.md:195`.

**Evidence:** "No automated cumulative-size backstop exists until that lint is wired or the hook ships — AE-006e fires on *compaction* (a context-fill event), not on a log's line-growth across many short sessions, so it does not detect cap-crossing (PM-001/IN-001, verified against `quality-enforcement.md` AE-006e)."

**Impact:** `.context/rules/quality-enforcement.md` Auto-Escalation Rules table defines AE-006e as "Compaction event detected" — a category **distinct** from the "Context fill NOMINAL/WARNING/CRITICAL/EMERGENCY tier" ladder (AE-006a–d). Labeling AE-006e itself as "a context-fill event" mildly conflates the two SSOT-distinguished categories. This does **not** change the disclosed conclusion (AE-006e still does not detect cap-crossing/cumulative log growth either way) — the residual disclosure (PM-001/IN-001, already closed per the Regression Check above) remains accurate in substance. Flagged as a citation-precision nit, not a re-opening of PM-001/IN-001.

**Recommendation:** Optional wording tweak: "AE-006e fires on a *compaction* event (distinct from the context-fill-tier rules AE-006a–d), not on..." — zero-machinery, one-clause fix, purely cosmetic.

---

## Recommendations

**P0 (Critical):** None.

**P1 (Major):** CC-001-i8 — add the cross-reference / promote the design doc's safe fallback into the shipped `feedback-decision-logs-standards.md` LOG-M-006 (wording-only, no new lint/file/field).

**P2 (Minor):** CC-002-i8, CC-003-i8 — optional cosmetic wording; low value, safe to defer or decline per the package's own anti-bloat doctrine.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No principle coverage gaps found; all 4 purpose pillars checked |
| Internal Consistency | 0.20 | Negative (minor) | CC-001-i8 (Major): shipped rule file's LOG-M-006 and its own Scope-Limits (e) are not cross-referenced; CC-002-i8 (Minor): diagram/prose state-name mismatch |
| Methodological Rigor | 0.20 | Negative (minor) | CC-001-i8: the recommended id-minting method is not verified against the file's own disclosed limitation |
| Evidence Quality | 0.15 | Neutral | No findings affect evidence quality; all 6 restore-notes closures independently re-verified against current text |
| Actionability | 0.15 | Neutral | All findings carry specific, wording-only remediation |
| Traceability | 0.10 | Negative (minor) | CC-003-i8: AE-006e citation slightly imprecise vs. SSOT category |

**Constitutional Compliance Score (S-007 Step 5, this strategy's own operational scoring, distinct from the tournament's 0.95 composite gate):**
`1.00 - (0.10 × 0 Critical + 0.05 × 1 Major + 0.02 × 2 Minor) = 1.00 - (0.00 + 0.05 + 0.04) = 0.91`

**Threshold Determination:** REVISE band (0.85–0.91) per S-007's own operational bands — driven entirely by one Major (CC-001-i8), which is a wording-only, zero-machinery fix consistent with every prior remediation round in this package's history. No Critical blocks acceptance under H-13.

---

<!-- Findings persisted incrementally per P-002. Blind protocol observed: iteration-007 and iteration-008 sibling-strategy findings were not read; only restore-notes.md (owner's public disposition record) and iterations 001-006 were consulted for disposition history. -->

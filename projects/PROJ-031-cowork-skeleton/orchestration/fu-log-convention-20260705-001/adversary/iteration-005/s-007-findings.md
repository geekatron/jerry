# Constitutional Compliance Report: Feedback & Decision Log Convention (design doc + staged artifacts)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-007, iteration 5, blind)
**Constitutional Context:** `docs/governance/JERRY_CONSTITUTION.md` v1.0 (P-001–P-042 loaded); `.context/rules/quality-enforcement.md` (HARD Rule Index H-01–H-36, tier vocabulary, criticality levels, AE-001–AE-006e); `.context/rules/markdown-navigation-standards.md` (H-23/NAV-001–006)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verdict |
| [Findings Table](#findings-table) | All findings, severity-classified |
| [Finding Details](#finding-details) | Evidence, analysis, remediation per finding |
| [Compliance Verifications](#compliance-verifications) | Explicit PASS checks for the four flagged areas |
| [Recommendations](#recommendations) | Prioritized remediation plan |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping + constitutional compliance score |

---

## Summary

**PARTIAL compliance.** The package (design doc + 5 staged artifacts) is disciplined about MEDIUM-tier purity, H-23 navigation, and public-repo hygiene — all three verify clean on direct inspection (see [Compliance Verifications](#compliance-verifications)). One genuine **Critical** finding stands: the design doc's own L0 Executive Summary asserts unconditional 100%-coverage capability ("captures **every** user feedback / follow-up item," "captures **every** decision-bearing exchange") in the same section, two sentences after explicitly disclosing that capture is a MEDIUM (SHOULD) discipline with **no detector for a missed turn** (Q5). This is a direct self-contradiction and a P-022 (No Deception) violation on the exact axis the tournament brief called out ("overclaimed coverage IS Critical") — not a hypothetical, it is the literal headline description a stakeholder reads first when deciding whether to ratify. Two Minor findings round out the report (a stray HARD-tier "MUST" in the design narrative, and a softer echo of the same coverage-implying phrasing in both template banners). **1 Critical, 0 Major, 2 Minor. Constitutional compliance score: 0.86 (REVISE band).** Recommend: hedge the two L0 bullets to match the document's own scope note before this design doc is used as the basis for user ratification.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-s007i5 | P-022 No Deception (+ Internal Consistency) | HARD | **Critical** | `feedback-decision-log-convention-design.md:32-33` assert "captures **every**..." two sentences after L0 scope note (i) at line 30 discloses no coverage guarantee exists | Internal Consistency |
| CC-002-s007i5 | Design's own MEDIUM-tier-purity discipline (anti-bloat doctrine) | SOFT | Minor | `feedback-decision-log-convention-design.md:70` — "The enumeration **MUST** check both axes" (HARD-tier verb in a MEDIUM-tier design narrative; not present in the installed rule file, which correctly uses non-imperative phrasing for the same guidance) | Internal Consistency |
| CC-003-s007i5 | P-022 No Deception (soft echo) | SOFT | Minor | `FEEDBACK-LOG.template.md:3` "Captures user feedback and follow-up items verbatim..."; `LLM-DECISION-LOG.template.md:3` "Captures decisions made in user↔LLM interaction..." — unqualified capability banners, same phrasing family as CC-001, read before the scoping disclosure two lines below | Completeness |
| CV-1 (verification) | MEDIUM-tier purity / H-13 HARD ceiling (25/25) | — | COMPLIANT | Zero `MUST`/`SHALL`/`REQUIRED`/`FORBIDDEN`/`CRITICAL` tokens in any staged file (`feedback-decision-logs-standards.md`, both templates, `examples-appendix.md`, `hook-design-note.md` — verified by direct search) | Methodological Rigor |
| CV-2 (verification) | H-23 Navigation tables | — | COMPLIANT | All 6 files >30 lines carry a nav table with anchor links; sampled anchors verified against actual heading text including punctuation-heavy cases (`L2: Governance & Migration` → `#l2-governance--migration`; `DEC-LLM-001 example-entry (alias: —)` → `#dec-llm-001-example-entry-alias-`) — both correctly reproduce the non-collapsing space-to-hyphen behavior real Markdown renderers exhibit when punctuation is stripped between two spaces | Methodological Rigor |
| CV-3 (verification) | Public-repo hygiene | — | COMPLIANT | No `[home]/` absolute paths, no employer-internal references, no un-genericized internal ids found in the design doc or any staged file (grep across the full package) | Evidence Quality |
| CV-4 (verification) | P-020 User Authority (Q1–Q5 PROPOSED-DEFAULTs) | — | COMPLIANT | All 5 open questions (Q1 verbatim policy, Q2 scope tag, Q3 hook timing, Q4 backfill, Q5 silent-non-capture residual) are consistently tagged `PROPOSED-DEFAULT`/`pending ratification` everywhere referenced (design doc, rule file LOG-M-003, both templates); Adoption plan step 1 requires **per-question** user sign-off before install — this is disclosure, not an override of user authority | Traceability |

**Finding ID Format:** `CC-{NNN}-s007i5` (S-007, iteration 5).

**Severity Definitions:** Critical = HARD-tier violation, blocks acceptance (H-13). Major = MEDIUM-tier violation, requires revision. Minor = SOFT-tier / stylistic, improvement opportunity only.

---

## Finding Details

### CC-001-s007i5: L0 Executive Summary asserts "captures every..." two sentences after disclosing it cannot guarantee that [CRITICAL]

**Principle:** P-022 (No Deception) — "Agents SHALL NOT deceive users about... capabilities or limitations." Cross-cutting with Internal Consistency (S-014 dimension) since the contradiction is intra-document, not merely a global overclaim.

**Location:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`, lines 30, 32, 33 (all within the L0 Executive Summary, same paragraph block).

**Evidence:**

Line 30 (L0 scope note, item i): *"...(i) the ledgers persist **what is logged**; they do not by themselves guarantee that every turn gets logged — capture stays a **MEDIUM (SHOULD)** discipline until the fail-open hook of [Q3] ships (see L1.3). **There is no detector for a turn that should have been logged but was not** — a disclosed residual, now elevated to an explicit ratification item ([Q5]) so it carries the same P-020 visibility as Q1–Q4."*

Two sentences later, line 32: *"**FEEDBACK-LOG** captures **every** user feedback / follow-up item **verbatim** (typos preserved) with an assistant summary, a 4-state disposition..."*

Line 33: *"**LLM-DECISION-LOG** captures **every** decision-bearing exchange: user verbatim (full) + assistant verbatim (excerpt + transcript pointer...)..."*

**Impact:** The document explicitly states, in its own words, that it has no way of knowing whether a turn that should have been captured actually was (Q5 is elevated to a ratification item *for exactly this reason*) — yet its headline capability description, read first by any stakeholder deciding whether to ratify the design, asserts unconditional, complete coverage ("every"). This is not a global inconsistency requiring cross-file comparison; it is a same-paragraph contradiction. A reader who stops at the bulleted capability list (the natural skim path for an executive summary) walks away believing the system guarantees 100% capture, which the document itself says is false three lines above. This is precisely the failure mode the tournament brief flagged ("overclaimed coverage IS Critical") — it is not a hypothetical risk of future misreading, it is a textual overclaim sitting directly adjacent to its own rebuttal.

**Dimension:** Internal Consistency (primary), Completeness (secondary — a reader relying only on the headline bullets has an incomplete/wrong picture of the system's guarantees).

**Remediation:** Reword both bullets to match the hedging already established two lines above and reinforced throughout the rest of the document (L1.1 capture triggers, L1.3 enforcement-layer disclosure, Q5). Minimal, wording-only fix (consistent with the package's own anti-bloat/no-new-machinery precedent set across iterations 1-4):

- Line 32: *"FEEDBACK-LOG captures every user feedback / follow-up item **the assistant/operator appends** verbatim..."* or *"FEEDBACK-LOG is the append target for every user feedback / follow-up item **that gets logged** (capture itself is MEDIUM-tier, disclosed above)..."*
- Line 33: analogous hedge — *"...is the append target for every decision-bearing exchange **that is captured**..."*

Either phrasing preserves the sentence's descriptive intent (what the log's *schema* covers once an entry is made) without contradicting the immediately-preceding disclosure that capture completeness is not guaranteed.

---

### CC-002-s007i5: HARD-tier verb ("MUST") in the design narrative's H-31 back-reference guidance [MINOR]

**Principle:** The design doc's own repeatedly-stated MEDIUM-tier-purity commitment (anti-bloat doctrine; ultimately traceable to the HARD-ceiling-at-25/25 constraint in `quality-enforcement.md` that the whole package exists to respect).

**Location:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:70`.

**Evidence:** *"The assistant **enumerates the candidates and asks which one is meant** (per H-31), rather than silently inferring from recency. The enumeration **MUST** check **both axes**: (a) entries whose **alias** matches the bare token, and (b) whether the bare token is itself a live **canonical** id..."*

**Impact:** Low — this sentence lives in the design rationale document, not in the artifact staged for install (`feedback-decision-logs-standards.md`, which is verified HARD-vocabulary-clean, and `examples-appendix.md`, which restates the same guidance non-imperatively: "Do **not** guess from recency — the assistant enumerates candidates on **both axes**..."). No new HARD obligation is actually shipped. But the design doc elsewhere explicitly frames HARD/MEDIUM/SOFT vocabulary discipline as load-bearing (e.g., the L2 section's entire rationale for why the rule file "cannot be HARD" — ceiling 25/25), so a stray unhedged "MUST" inside that same document is a minor internal-consistency lapse worth cleaning up for a document whose central discipline is precisely this vocabulary distinction.

**Dimension:** Internal Consistency.

**Remediation:** Change "MUST check both axes" to "checks both axes" or "SHOULD check both axes" to match the non-imperative phrasing already used in the shipped rule file and appendix.

---

### CC-003-s007i5: Template banners echo the same unqualified "Captures..." phrasing as CC-001 [MINOR]

**Principle:** P-022 (No Deception), softer instance — a reader of the template file alone (the artifact an operator actually opens when starting a new project) sees the capability claim before the scoping disclosure.

**Location:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/FEEDBACK-LOG.template.md:3`; `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/LLM-DECISION-LOG.template.md:3`.

**Evidence:**
- FEEDBACK-LOG.template.md:3 — *"Feedback / Follow-Up (FU) log. Captures user feedback and follow-up items **verbatim** with disposition tracking."*
- LLM-DECISION-LOG.template.md:3 — *"Captures decisions made in user↔LLM interaction: verbatim exchanges, summaries, model, session, datetime, context."*

**Impact:** Lower severity than CC-001 because these are template banners (conventional short-form tool descriptions, not an executive summary making a ratification case), and both files immediately point to the rule file ("Per the Feedback & Decision Log Standards") which correctly discloses the MEDIUM-tier nature two lines later in the same file (rule file line 3: "Capture itself is a MEDIUM (SHOULD) discipline... a fail-open hook is designed to assist but is not yet shipped"). Still, an operator who only ever opens the template (the artifact they actually type into) sees the unqualified "Captures..." framing first. Flagged as a propagation echo of the same root pattern as CC-001, not a separate defect.

**Dimension:** Completeness.

**Remediation:** Optional — if CC-001 is fixed, consider a one-word softening here too ("Log target for..." or add "(MEDIUM-tier; see standards)" inline) for consistency, but this is not blocking given the rule-file cross-reference sits two lines away in the same document.

---

## Compliance Verifications

Explicit checks requested by the tournament brief, verified COMPLIANT (evidence, not assertion):

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| CV-1 | MEDIUM-tier purity of the **installed** rule file (no MUST/SHALL; HARD ceiling untouched) | **PASS** | Searched `feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md` for `MUST\b|SHALL\b|REQUIRED\b|FORBIDDEN\b|CRITICAL\b` — zero matches. `hook-design-note.md`'s lowercase "must"/"must not" are explicitly self-disclaimed in its own header as code-implementation constraints, not HARD-rule-tier governance (line 3) — correctly scoped, does not touch the 25/25 ceiling. |
| CV-2 | H-23 navigation tables present, anchors correct | **PASS** | All 6 files (design doc + 5 staged artifacts) carry a nav table per NAV-001–006. Sampled anchor generation against actual GitHub/remark slug behavior (including the non-obvious double-hyphen artifact from punctuation removed between two spaces, e.g. `& ` → `--`, `: —)` → trailing `-`) — all sampled anchors resolve correctly. |
| CV-3 | Public-repo hygiene (no internal refs / absolute paths) | **PASS** | No `[home]/`, `[employer]`, or un-genericized internal identifiers found anywhere in the design doc or `staging-feedback-logs/`. |
| CV-4 | P-020 — 4 (actually 5, Q1-Q5) open questions still PROPOSED-DEFAULT | **PASS (not a violation)** | Consistently tagged `PROPOSED-DEFAULT`/`pending ratification` in every location referenced (design doc Proposed Defaults table, rule file LOG-M-003 + scoping line, both templates' verbatim-policy/scope notes, `hook-design-note.md` feasibility verdict). Adoption plan step 1 requires **per-question** explicit user sign-off ("confirmed one by one, not a blanket 'LGTM'") before install — this is the correct P-020 posture (propose, disclose, wait for ratification), not an override of user authority. |

---

## Recommendations

**P0 (Critical):** CC-001-s007i5 — Reword the two L0 headline bullets (design doc lines 32-33) so "captures every..." does not contradict the scope note two lines above and the Q5 disclosure. Wording-only fix, no new machinery, consistent with every prior remediation round in this package's changelog.

**P1 (Major):** None.

**P2 (Minor):** CC-002-s007i5 — soften "MUST check both axes" (design doc line 70) to match the non-imperative phrasing already used in the shipped rule file and appendix. CC-003-s007i5 — optionally soften the two template banner lines for consistency once CC-001 is fixed.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | CC-003: template banners omit the MEDIUM-tier hedge a reader needs for a complete picture. |
| Internal Consistency | 0.20 | **Negative (major)** | CC-001: L0 headline directly contradicts its own scope note in the same section; CC-002: stray HARD-tier verb inside a document whose central discipline is vocabulary-tier purity. |
| Methodological Rigor | 0.20 | Positive | CV-1/CV-2 verified clean: MEDIUM-tier discipline and H-23 navigation both hold under direct inspection across all 6 files. |
| Evidence Quality | 0.15 | Positive | CV-3 verified clean; all findings above cite exact file:line evidence, no assertion-only claims. |
| Actionability | 0.15 | Neutral | Remediation for CC-001/002/003 is specific, wording-only, and directly actionable. |
| Traceability | 0.10 | Positive | CV-4: all open questions traceable to Q1-Q5 with consistent tagging everywhere referenced. |

**Constitutional Compliance Score:** `1.00 - (1 × 0.10 + 0 × 0.05 + 2 × 0.02) = 1.00 - 0.14 = 0.86`

**Threshold Determination:** REVISE (0.85-0.91 band; below the H-13 SSOT threshold of 0.92, and well below the 0.95 engagement gate for this C4 tournament). The single Critical finding is a targeted, wording-only fix — not a structural defect requiring new machinery, consistent with this package's established remediation pattern across iterations 1-4.

---

## Execution Statistics

- **Total Findings:** 3 (+ 4 explicit compliance verifications)
- **Critical:** 1
- **Major:** 0
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5 (Load Constitutional Context, Enumerate Applicable Principles, Principle-by-Principle Evaluation, Remediation Guidance, Score Constitutional Compliance)

# Constitutional Compliance Report: ADR-adversary-tournament-protocol-001 (iteration 4)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Review metadata |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Full evidence, analysis, remediation per finding |
| [Remediation Plan](#remediation-plan) | Prioritized action list |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Protocol completion record |

---

## Header

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-007 strategy execution)
**Constitutional Context:** `.context/rules/quality-enforcement.md` (HARD Rule Index, Tier Vocabulary, HARD Rule Ceiling Derivation), `.context/rules/agent-development-standards.md` (H-34, Tool Security Tiers, Cognitive Mode Taxonomy), `.context/rules/markdown-navigation-standards.md` (H-23), `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (Scheme B ADR convention)

---

## Summary

PARTIAL constitutional compliance. The ADR's Scheme B identifier/frontmatter is compliant, its H-23 navigation table resolves correctly, and its H-13/H-14/RT-M-010 SSOT citations are accurate. However, the deliverable's central, repeated claim — "no HARD rule is touched," "Everything here is a MEDIUM-tier process change," "the 25/25 HARD-rule ceiling is untouched" — is undermined by its own specification: the proposed edit to `adv-scorer.md` mandates new scoring-report content using HARD-tier vocabulary (`REQUIRED`, `mandatory`) as defined by the Tier Vocabulary SSOT, without registering a new HARD rule or invoking the ceiling's Exception Mechanism. A secondary Major finding identifies a tool-tier/label mismatch for the proposed `adv-verifier` agent against the canonical Tool Security Tiers table. **1 Critical, 1 Major, 2 Minor.** Recommend REVISE.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-iter4 | Tier Vocabulary SSOT (quality-enforcement.md "Tier Vocabulary" + "HARD Rule Ceiling Derivation") | HARD (vocabulary discipline) | **Critical** | ADR lines ~746, ~482, ~926 use `REQUIRED`/`mandatory` for a brand-new scorer obligation while the ADR's own repeated thesis (L0, c-001, c-002, WI-7 AC) asserts "no HARD rule is touched" | Internal Consistency |
| CC-002-iter4 | agent-development-standards.md Tool Security Tiers (T1/T2 definitions) | MEDIUM | Major | ADR L1 item 1 declares `adv-verifier` "Tool tier T2, tools restricted to Read, Glob, Grep, Write" — but canonical T2 = "T1 + Write, Edit, Bash"; the agent's actual tool set is T1+Write only, not T2 | Traceability |
| CC-003-iter4 | agent-development-standards.md Cognitive Mode Taxonomy (`identity.cognitive_mode` single enum) | MEDIUM | Minor | ADR L1 item 1: "Cognitive mode forensic/convergent" — a compound value where the schema expects one of `{divergent, convergent, integrative, systematic, forensic}` | Actionability |
| CC-004-iter4 | Evidence-citation precision (P-022, self-referential to the ADR's own thesis) | SOFT | Minor | ADR cites `skills/adversary/agents/adv-scorer.md:166-167` four times for a quote that resolves to line 166 alone (line 167 is a distinct, related special case); D-6 rationale states "at most ~9–10 reports at C4" though Groups A–E enumerate exactly 9 finder strategies | Evidence Quality |

**Finding ID Format:** `CC-{NNN}-iter4` (execution-scoped to this iteration-4 S-007 pass).

---

## Finding Details

### CC-001-iter4: MEDIUM-tier framing contradicted by HARD-tier vocabulary in the proposed scorer edit [CRITICAL]

**Principle:** `.context/rules/quality-enforcement.md` Tier Vocabulary table — `MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL` are defined as HARD-tier keywords, "Cannot override," counted against the <= 25 ceiling; `SHOULD, RECOMMENDED, PREFERRED, EXPECTED` are MEDIUM ("Documented justification" to override). The same file's "HARD Rule Ceiling Derivation" section exists specifically to prevent unregistered, non-overridable obligations from proliferating outside the 25-rule governance discipline (ADR/exception-tracked expansion only).

**Location:** ADR lines ~742–749 (L1 Technical Implementation, item 3, edit to `skills/adversary/agents/adv-scorer.md`); Decision table row D-5 (line ~482); WI-3 acceptance criteria (line ~926).

**Evidence:**
- L1 item 3: *"a Delta-Reconciliation section and a dual-protocol (verified + old) composite are **REQUIRED** for any round that used panels."*
- Decision table, D-5: *"**B — mandatory delta-reconciliation** against the prior iteration."*
- WI-3 AC: *"Delta-Reconciliation section **REQUIRED**; dual-protocol composite **REQUIRED** when panels used."*
- Contrast with the ADR's own repeated thesis: L0 — *"Everything here is a MEDIUM-tier process change... no HARD rule is touched and the 25/25 HARD-rule ceiling is untouched."*; constraint c-001 — *"No HARD-rule additions, deletions, or edits; ceiling stays 25/25."*; c-002 — *"Changes are MEDIUM-tier and reversible."*

**Impact:** The ADR's central, repeatedly-asserted selling point is tier-purity: every change is MEDIUM (overridable, reversible, ceiling-neutral). But the specific new obligation it writes into `adv-scorer.md` — a Delta-Reconciliation section and dual-protocol composite "REQUIRED" for any panelled round — uses vocabulary the SSOT itself defines as HARD-tier and non-overridable. This is directly analogous to H-17 ("Quality scoring via S-014 LLM-as-Judge REQUIRED for all C2+ deliverables"), which *is* a registered, ceiling-counted HARD rule. If a materially similar "scoring-report content REQUIRED" obligation can be introduced via an ADR + agent-file edit without HARD-rule registration or use of the ceiling's Exception Mechanism (C4-reviewed ADR, tracked reversion deadline, max +3 slots), the ADR's own "ceiling stays 25/25, MEDIUM-tier only" claim is not accurate for what it specifies, and the pattern — if repeated by future ADRs — erodes the governance discipline the ceiling exists to enforce. This is compounded by RSK-6's mitigation ("sunset the old-protocol composite once the team is calibrated") having no assigned owner, trigger condition, or work item — so the "REQUIRED... during transition" language has no defined end-state and functions as an indefinite obligation in practice.

**Dimension:** Internal Consistency

**Remediation:** Either (a) downgrade the new scorer-report obligations to MEDIUM-tier vocabulary ("A Delta-Reconciliation section and dual-protocol composite SHOULD accompany any round that used panels; omission requires documented justification"), explicitly acknowledging these become advisory rather than blocking acceptance criteria, or (b) if the intent is genuinely non-overridable/blocking (matching "ALWAYS"/"unconditional" language used elsewhere for the D-2 gate), disclose this honestly as a HARD-strength addition and route it through the ceiling's Exception Mechanism (or register it as a sub-item of an existing compound rule, e.g., H-17) rather than asserting "zero HARD-rule impact." Additionally, assign an owner and a concrete trigger condition (e.g., "sunset after N consecutive rounds report < 0.05 protocol-delta variance") to RSK-6's dual-protocol sunset so it is not an open-ended requirement.

---

### CC-002-iter4: `adv-verifier`'s declared "T2" tool tier does not match the canonical T2 definition [MAJOR]

**Principle:** `.context/rules/agent-development-standards.md` Tool Security Tiers — "T2 | Read-Write | T1 + Write, Edit, Bash" is the canonical, exhaustive definition; the same section instructs "Always select the lowest tier that satisfies the agent's requirements."

**Location:** ADR L1 Technical Implementation, item 1 (~lines 688–696); WI-1 acceptance criteria (~line 924); Issue A draft body (~line 946).

**Evidence:** *"Tool tier **T2**, tools restricted to `Read, Glob, Grep, Write`"* — and the ADR's own CC-001-iter2 rationale note explicitly acknowledges the tension: *"A pure-T1 tier (Read, Glob, Grep) structurally excludes Write and so could not satisfy this agent's own persistence contract — the two are reconciled here by granting write-of-new-files only and forbidding edits via a guardrail."* The reconciliation grants the agent a tool set (`Read, Glob, Grep, Write`) that is neither T1 (excludes Write) nor T2 (canonically includes Edit and Bash) per the cited SSOT table — it is a bespoke "T1 + Write, minus Edit/Bash" tier that the table does not define, labeled "T2" anyway.

**Impact:** A future H-34 compliance audit checking "does this agent's declared `tool_tier` match its `allowed_tools`" against the canonical Tool Security Tiers table will find `adv-verifier` missing two of T2's three tools (Edit, Bash) while still being labeled T2. No corresponding update to `agent-development-standards.md`'s tier table is proposed by this ADR (WI-1..WI-8 touch only `skills/adversary/*`) to formalize a restricted sub-tier, so the mismatch persists as an undocumented exception rather than a defined pattern.

**Dimension:** Traceability

**Remediation:** Either label the agent's tier honestly as a documented restriction ("T1 + Write (write-of-new-files only); no Edit/Bash — see guardrail"), or propose (as an additional, explicitly-scoped work item) a one-line amendment to `agent-development-standards.md`'s Tool Security Tiers table introducing a named restricted tier (e.g., "T1w") so the pattern is traceable and reusable rather than a one-off mislabel.

---

### CC-003-iter4: Compound cognitive-mode value is not resolvable against the single-enum schema [MINOR]

**Principle:** `.context/rules/agent-development-standards.md` Agent Definition Schema — `identity.cognitive_mode` is a single-value enum: `divergent, convergent, integrative, systematic, forensic`.

**Location:** ADR L1 item 1 (~line 699): *"Cognitive mode **forensic/convergent**."*

**Evidence:** The ADR declares a compound value rather than selecting one enum member. The Mode-to-Design Implications table in the same SSOT file gives materially different guidance per mode (e.g., forensic recommends "T2 or T4... opus... larger reasoning allocation (~35%)" vs. convergent recommends "T1 or T2... sonnet or opus... balanced allocation").

**Impact:** WI-1's implementer must pick one value to pass schema validation; the ADR does not resolve which, leaving a small but concrete implementability gap in an otherwise carefully-specified agent definition.

**Dimension:** Actionability

**Remediation:** Resolve to a single value (forensic is the better fit given the agent's role is adjudicating claims for factual/remediation truth, not selecting among alternatives) and note the tie-break rationale in WI-1.

---

### CC-004-iter4: Minor citation/count imprecision in the ADR's own evidentiary trail [MINOR]

**Principle:** P-022 (accuracy of cited evidence), applied self-referentially to a document whose central thesis is "verify before you count."

**Location:** ADR lines ~114–116, ~330–332, ~479, ~743 (four citations of `skills/adversary/agents/adv-scorer.md:166-167`); D-6 rationale (~line 456).

**Evidence:** Direct reading of `skills/adversary/agents/adv-scorer.md` shows the exact quoted sentence *"Any Critical finding from adv-executor reports → automatic REVISE regardless of score"* resolves to line 166 alone; line 167 is a distinct special case ("Score >= 0.92 but with unresolved Critical findings → REVISE"). Separately, D-6's rationale states finder reports are "at most ~9–10... at C4," but `adv-selector.md`'s Groups A–E enumerate exactly 9 finder strategies (S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013); S-014 (Group F) is the scorer, not a finder, so the maximum is 9, not "9–10."

**Impact:** Neither instance changes any decision or acceptance criterion, but both are the same category of imprecision the ADR itself diagnoses as costly in the fabricated-PR-template incident (Context section) — a document arguing for verification rigor should hold its own line-citations and derived counts to the standard it is proposing for the tournament.

**Dimension:** Evidence Quality

**Remediation:** Correct the four `adv-scorer.md:166-167` citations to `:166` (or explicitly quote both lines if both are intended); correct "~9–10 reports at C4" to "at most 9" (or cite the specific scenario, if any, that would produce 10).

---

## Remediation Plan

**P0 (Critical):** CC-001-iter4 — resolve the REQUIRED/mandatory vs. MEDIUM-tier contradiction in the `adv-scorer.md` edit (L1 item 3, D-5, WI-3 AC); assign an owner/trigger for the dual-protocol sunset.
**P1 (Major):** CC-002-iter4 — reconcile `adv-verifier`'s declared T2 label against its actual T1+Write tool set, or formally define a restricted sub-tier.
**P2 (Minor):** CC-003-iter4 — resolve the compound cognitive-mode value to a single enum member. CC-004-iter4 — correct the `adv-scorer.md` line citation and the finder-report-count figure.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No principle-coverage gaps found; all named review foci (Scheme B, ceiling, H-13/H-14/RT-M-010, H-23) were checked |
| Internal Consistency | 0.20 | Negative | CC-001-iter4 (Critical): HARD-tier vocabulary contradicts the MEDIUM-tier thesis in the deliverable's own specified edit |
| Methodological Rigor | 0.20 | Negative | CC-002-iter4 (Major): declared tool tier does not match the SSOT tier definition it cites |
| Evidence Quality | 0.15 | Negative | CC-004-iter4 (Minor): two small citation/count imprecisions in a document whose thesis is citation rigor |
| Actionability | 0.15 | Negative | CC-003-iter4 (Minor): unresolved compound cognitive-mode value blocks clean schema-valid implementation |
| Traceability | 0.10 | Negative | CC-002-iter4 also affects traceability against the canonical Tool Security Tiers table |

**S-007 Operational Constitutional-Compliance Score (template-internal penalty model, NOT the S-014 gate score):** `1.00 - (0.10*1 + 0.05*1 + 0.02*2) = 0.81` → below the 0.85 S-007-internal band, i.e., these findings alone would recommend REVISE/REJECTED-band attention if constitutional compliance were scored in isolation. Per S-007 template guidance, the authoritative deliverable threshold (>= 0.92) and dimension weights remain governed by `.context/rules/quality-enforcement.md` and are computed by adv-scorer (S-014), not by this report.

**Threshold Determination (S-007 execution quality, not the deliverable gate):** All 5 Execution Protocol steps completed; findings are evidence-cited with file+line and quoted text; recommendations are specific and actionable.

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 1
- **Major:** 1
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5

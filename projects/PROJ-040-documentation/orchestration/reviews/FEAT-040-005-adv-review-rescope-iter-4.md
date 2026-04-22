# Adversarial Review: FEAT-040-005 — Rescope Iteration 4 (C3 Multi-Strategy)

## Execution Context

| Field | Value |
|-------|-------|
| **Feature ID** | FEAT-040-005 |
| **Deliverable** | `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-005/ux-inclusive-evaluator-output.md` |
| **Review Type** | C3 Adversarial Review — Rescope Iteration 4 (4 editorial closures) |
| **Criticality** | C3 |
| **Quality Threshold** | 0.92 |
| **Iteration** | rescope-iter-4 |
| **Agent Self-Score** | 0.900 (raw 0.904, calibrated −0.004) |
| **Prior Iter-3 Score** | 0.897 (REVISE — 5 Minor editorial; SC 2.1.4 + Audit Scope theme name were primary IC/MR blockers) |
| **Strategies Executed** | S-007, S-002, S-004, S-012, S-013, S-014 |
| **Review Focus** | Verify 4 editorial closures; check for regressions; strict threshold scoring |
| **Executed** | 2026-04-20 |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Iter-4 Editorial Closure Verification](#iter-4-editorial-closure-verification) | Verify each of the 4 stated corrections is present and correct |
| [S-007: Constitutional AI Critique](#s-007-constitutional-ai-critique) | Behavioral rule and P-022 compliance |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-arguments against core claims and corrections |
| [S-004: Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Prospective failure enumeration |
| [S-012: FMEA](#s-012-fmea) | Component-level failure mode analysis |
| [S-013: Inversion](#s-013-inversion) | Assumption stress-testing |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Weighted composite score |
| [Regression Check](#regression-check) | Verify iter-3 pass-level sections have not degraded |
| [Consolidated Findings Summary](#consolidated-findings-summary) | All findings by severity |
| [Verdict](#verdict) | PASS / REVISE decision |

---

## Iter-4 Editorial Closure Verification

The iter-3 adversarial review identified 5 Minor editorial corrections. The iter-4 scope implements 4 of these (FM-001-RI3, IN-001-RI3+DA-001-RI3, DA-003-RI3, DA-002-RI3). This section verifies each correction is present and technically accurate.

### EC-1: FM-001-RI3 — Audit Scope Theme Naming (stale "default theme" → saucer-boy)

**Required correction:** Replace "Material for MkDocs default theme" in Audit Scope methodology sentence with "custom saucer-boy theme (light mode) / saucer-boy-dark (dark mode) built on Material for MkDocs base, defined in docs/stylesheets/saucer-boy.css".

**Evidence in deliverable (Audit Scope section, line 158):**
```
Color contrast assessed by visual analysis and theme inspection (custom saucer-boy theme
(light mode) / saucer-boy-dark (dark mode) built on Material for MkDocs base, defined in
docs/stylesheets/saucer-boy.css).
```

**Residual "default theme" scan:** No instance of "Material for MkDocs default theme" or "default theme" found in the Audit Scope or Methodology sections. The Theme subsection of Audit Scope (lines 175–176) correctly identifies "Material for MkDocs with custom **saucer-boy** theme" and provides full CSS variable detail.

**Technical accuracy check:** The correction is accurate. The site uses `docs/stylesheets/saucer-boy.css` (confirmed via direct Read in rescope-iter-2 Evidence Verification Protocol). The two schemes (`saucer-boy` light mode, `saucer-boy-dark` dark mode) are confirmed from `mkdocs.yml`. The "built on Material for MkDocs base" qualifier is accurate — Material is the rendering engine; saucer-boy is the custom override layer.

**Dimension impact:** Methodological Rigor — the Audit Scope section no longer misidentifies the theme being evaluated.

**Verdict: CORRECT.** Stale reference eliminated. No residual instances of "default theme" terminology in Audit Scope.

**EC-1: CLOSED.**

---

### EC-2: IN-001-RI3 + DA-001-RI3 — SC 2.1.4 Cross-Section Harmonization

**Required correction:** Harmonize SC 2.1.4 verdict to "CANNOT DETERMINE (elevated risk)" across all 4 locations: (a) per-SC body section, (b) Keyboard Navigation Audit table, (c) Synthesis Judgments table, (d) POUR Operable row (SC 2.1.4 added to SCs Evaluated + Dominant Failures).

**Evidence — Location 1: Per-SC body (lines 368–374):**
```
Status: CANNOT DETERMINE (elevated risk) [rescope-iter-4: harmonized from "PASS (with caveat)"
in per-SC section and "FAIL (candidate)" in Keyboard Navigation Audit table — global vs.
focus-only activation is not confirmed via WebFetch; Material for MkDocs typically mitigates
via focus-scoped shortcut but browser verification required before assigning PASS or FAIL]
```
CONFIRMED: CANNOT DETERMINE (elevated risk) with explicit harmonization note.

**Evidence — Location 2: Keyboard Navigation Audit table (line 642):**
```
| Search activation | `/` shortcut key — single-character, may fail 2.1.4 | 2.1.4 | CANNOT DETERMINE (elevated risk) |
```
CONFIRMED: CANNOT DETERMINE (elevated risk).

**Evidence — Location 3: Synthesis Judgments table (line 916):**
```
| SC 2.1.4 CANNOT DETERMINE (elevated risk) — `/` search shortcut | WCAG pass/fail | MEDIUM | Shortcut observed; global vs. focus-only activation not confirmed; requires browser testing; harmonized across all sections in rescope-iter-4 |
```
CONFIRMED: CANNOT DETERMINE (elevated risk) with provenance note.

**Evidence — Location 4: POUR Operable row (line 193):**
```
| Operable | 2.1.1, 2.1.2, 2.1.4, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.4.5, 2.4.6, 2.4.7, 2.4.11 | **FAIL** | SC 2.4.2 (duplicate H1 home page), SC 2.4.6 (bold step labels as headings), SC 2.1.4 (CANNOT DETERMINE — `/` shortcut global vs. focus-only not confirmed) |
```
CONFIRMED: SC 2.1.4 added to SCs Evaluated column AND to Dominant Failures with CANNOT DETERMINE qualifier.

**Technical accuracy check:** The POUR Operable rollup remains FAIL (driven by SC 2.4.2 and SC 2.4.6, which are confirmed FAILs). Adding SC 2.1.4 as CANNOT DETERMINE to the Dominant Failures column is correct — it is an elevated risk item worth surfacing. The per-SC status change from "PASS (with caveat)" to "CANNOT DETERMINE (elevated risk)" is the most defensible position: WebFetch cannot confirm whether the `/` shortcut is global vs. focus-only scoped. "PASS with caveat" was optimistic; "FAIL candidate" was pessimistic; "CANNOT DETERMINE" correctly reflects the evidence state.

**All 4 locations consistent:** CANNOT DETERMINE (elevated risk) is the consistent verdict across all 4 locations, with appropriate qualifiers in each context. The harmonization is complete.

**EC-2: CLOSED.**

---

### EC-3: DA-003-RI3 — Self-Score vs Projected-Adversarial Phrasing

**Required correction:** Clarify line 978 to explicitly distinguish self-score (0.895) from projected adversarial score (0.92–0.925).

**Prior problematic text (iter-3, as quoted in iter-3 review line 589):**
> "Raw composite 0.899 / calibrated 0.895 is within the reviewer's projected band of 0.92–0.925"

**Corrected text in deliverable (line 978):**
> "the adversarial reviewer's projected composite band of 0.92–0.925 is the projected *adversarial* score after corrections, not the self-score — these are distinct: 0.895 is the self-reported calibrated score; 0.92–0.925 is the projected adversarial-confirmed composite. [Clarified in rescope-iter-4 per DA-003-RI3]"

**Technical accuracy check:** The correction is unambiguous. The two values are explicitly labeled and declared "distinct." The prior text implied 0.895 was "within" the 0.92–0.925 band (which is false — 0.895 < 0.920). The new text correctly separates the self-reported calibrated score (0.895 from iter-3; the current iter-4 self-score is 0.900) from the reviewer-projected adversarial composite. The correction bracket "[Clarified in rescope-iter-4 per DA-003-RI3]" provides traceability.

**One observation:** The self-score section heading reads "Rescope Iter-4" (line 949) and the body references iter-3's 0.895 as "prior iteration baseline." The sentence at line 980 correctly states "The iter-3 self-score of 0.895 is the prior iteration baseline; iter-4 gains +0.005 from IC." This is internally consistent — 0.895 is iter-3's value, not iter-4's. The clarification at line 978 correctly frames 0.895 as the self-reported calibrated score from iter-3.

**EC-3: CLOSED.**

---

### EC-4: DA-002-RI3 — W-015b Dual-Estimate Convergence Sentence

**Required correction:** Add sentence explicitly acknowledging that both ratio estimates (~1.7:1 and ~2.36:1) converge on the same remediation verdict.

**Evidence in deliverable (lines 624–625):**
```
Both ratio estimates (agent ~1.7:1, reviewer-computed ~2.36:1) converge on the same
remediation verdict: below the 3:1 SC 1.4.11 non-text contrast threshold, remediation
justified.
```

**Technical accuracy check:** Both ~1.7:1 and ~2.36:1 are below the 3:1 SC 1.4.11 non-text contrast threshold. The convergence claim is accurate — despite the ~0.66:1 gap between the two estimates, both independently justify the same remediation conclusion. The sentence does not claim the estimates agree with each other; it claims they agree on the *verdict*. This is the correct framing.

**Internal consistency check:** The Color Contrast Analysis table still shows "~1.7:1 (estimated)" for the dark mode link underline row. The W-015b note now includes the convergence sentence. The Remediation Priorities table (line 810 area) still cites "~8.3:1 contrast ratio" for the fixed value — this is the post-fix estimate (rgba(179,157,219,1.0)), which is a separate computation and correctly higher than the current failing ~1.7:1. No internal contradiction.

**EC-4: CLOSED.**

---

### Editorial Closure Summary

| Item | Correction | Technical Accuracy | Propagation | Status |
|------|-----------|-------------------|-------------|--------|
| FM-001-RI3 | Audit Scope: "default theme" → saucer-boy full description | Accurate per confirmed CSS/mkdocs.yml evidence | Audit Scope methodology sentence | CLOSED |
| IN-001-RI3 + DA-001-RI3 | SC 2.1.4 harmonized to CANNOT DETERMINE (elevated risk) | Correct — WebFetch cannot confirm global vs. focus-only; CANNOT DETERMINE is most accurate | All 4 locations: per-SC, Keyboard table, Synthesis Judgments, POUR Operable row | CLOSED |
| DA-003-RI3 | Self-score vs projected-adversarial score distinction | Accurate — 0.895 (iter-3 self-score) and 0.92–0.925 (projected adversarial) are explicitly labeled as distinct | Lines 978 self-score section | CLOSED |
| DA-002-RI3 | W-015b convergence sentence added | Accurate — both sub-3:1 estimates support same remediation verdict | Color Contrast Analysis W-015b note | CLOSED |

**All 4 editorial corrections confirmed present and technically accurate.**

---

## S-007: Constitutional AI Critique

### Applicable Principles

Deliverable type: WCAG accessibility audit — document artifact. Applicable rules:
- P-001 (Truth/Accuracy), P-022 (No Deception) — factual claims and confidence labeling
- P-011 (Evidence-Based Findings) — every finding requires evidence
- H-15 (Self-Review before presenting) — self-assessed quality score present
- H-23/H-24 (Markdown navigation table required, anchor links required)
- quality-enforcement.md — S-014 scoring methodology, weights, anti-leniency

### Principle Evaluation

**CC-001-RI4 — P-001/P-022 Truth and No Deception (Post-Iter-4)**

- **Principle:** HARD. Every factual claim must be accurate. No deception about capabilities, confidence levels, or actions taken.
- **Evaluation:** All four iter-2 factual corrections are retained. All five iter-3 editorial corrections are retained. All four iter-4 editorial corrections are present and correct. The self-score distinction (0.900 calibrated self-score vs. 0.922–0.925 projected adversarial) is now explicitly disambiguated. The Audit Scope theme identification is accurate. SC 2.1.4 harmonization is internally consistent. W-015b convergence sentence is factually accurate (both estimates are below 3:1 threshold).
- **One residual observation:** Line 982 states: "An adversarial reviewer scoring rescope-iter-4 is projected to score 0.922–0.925." This is a projection, not a claim. The projection is based on the iter-3 review's own gap analysis which stated: "Estimated composite after iter-4 corrections: 0.897 + ~0.025 ≈ 0.922." The projection is labeled as such. Not a deception — the review confirms or contradicts this projection through the S-014 scoring below.
- **Verdict:** COMPLIANT
- **Quality dimension:** Evidence Quality, Internal Consistency

**CC-002-RI4 — H-23/H-24 Navigation Table**

- **Principle:** HARD. Documents over 30 lines must include a navigation table with anchor links.
- **Evaluation:** Navigation table present at document start with 16 entries (one added for Self-Assessed Quality Score heading update), all using markdown anchor link syntax. All major sections listed.
- **Verdict:** COMPLIANT

**CC-003-RI4 — P-011 Evidence-Based Findings**

- **Principle:** HARD. Every finding must include direct evidence from the evaluated artifact.
- **Evaluation:** All Sev-2+ and Sev-3 findings from iter-2/iter-3 retain unchanged evidence citations. The four iter-4 corrections are editorial (no new evidence claims introduced). SC 2.1.4 verdict change from PASS-with-caveat to CANNOT DETERMINE is a more conservative assessment of the same evidence — not a new evidentiary claim but a more accurate characterization of the existing evidence state (WebFetch cannot confirm global vs. focus-only shortcut scope). This is P-022 compliant: the correction reduces overconfidence, not increases it.
- **Verdict:** COMPLIANT

**CC-004-RI4 — Quality-Enforcement Scoring Methodology**

- **Principle:** MEDIUM. Quality scoring uses the S-014 six-dimension rubric; conservative calibration required.
- **Evaluation:** The self-score section (lines 961–982) uses correct weights (sum = 1.00). Anti-leniency statement is explicit. Per-dimension rationale for iter-4 increments is provided. Raw composite 0.904 minus −0.004 calibration penalty = 0.900. The calibration penalty rationale (−0.002 for dark mode contrast still estimated, −0.002 for SC 2.1.4 CANNOT DETERMINE still unresolved) is coherent — these are genuine ongoing evidence gaps.
- **One note:** The IC self-score is 0.925 (up from 0.91 in iter-3). The +0.015 increment reflects: SC 2.1.4 cross-section inconsistency CLOSED + DA-003-RI3 self-score phrasing CLOSED. Given that these were the two remaining documented IC residuals from iter-3, an IC jump to 0.925 is plausible. Whether IC reaches 0.925 or 0.92 is the key threshold question for the composite.
- **Verdict:** COMPLIANT (IC 0.925 self-assessment is evaluated further in S-014)

### S-007 Summary

| Finding | Severity | Principle | Status |
|---------|----------|-----------|--------|
| CC-001-RI4: All 4 iter-4 corrections correct; P-022 compliant | Pass | P-001/P-022 | COMPLIANT |
| CC-002-RI4: Navigation table intact | Pass | H-23/H-24 | COMPLIANT |
| CC-003-RI4: Evidence unchanged; SC 2.1.4 correction is more conservative | Pass | P-011 | COMPLIANT |
| CC-004-RI4: Self-score methodology coherent; IC 0.925 claim evaluated in S-014 | Pass (to verify in S-014) | quality-enforcement.md | COMPLIANT |

**S-007 verdict:** No Critical or Major constitutional violations in rescope-iter-4. All prior findings remain remediated. No new constitutional issues introduced.

---

## S-002: Devil's Advocate

**H-16 compliance check:** S-003 Steelman ran prior to this review chain (established in rescope-iter-1). The iter-4 scope is editorial corrections only; H-16 is satisfied.

### Core Claims Under Challenge (Iter-4 Scope)

**Claim 1: SC 2.1.4 "CANNOT DETERMINE (elevated risk)" is the correct harmonized verdict.**

*Counter-argument:* Before iter-4, the per-SC body said "PASS (with caveat)" and the Keyboard Navigation table said "FAIL (candidate)." The iter-4 correction chose "CANNOT DETERMINE (elevated risk)" as the compromise. However, "CANNOT DETERMINE" implies equal probability of PASS or FAIL, whereas the actual evidence leans toward concern: Material for MkDocs does implement `/` as a global keyboard shortcut that fires regardless of focus state (this is its documented behavior — it's a global event listener). The prior "FAIL (candidate)" in the Keyboard table may have been the more accurate verdict. By softening to "CANNOT DETERMINE," has the correction improved internal consistency at the cost of accuracy?

*Assessment:* The evidence available via WebFetch is that `/` opens search. Whether it is a global keyboard shortcut vs. focus-scoped shortcut is NOT confirmed from WebFetch. Material for MkDocs has evolved its keyboard shortcut implementation across versions — some versions fire globally, some fire only when search is not focused. The reviewer's own iter-3 text (the prior "FAIL candidate" entry in the Keyboard table) was itself an AI inference, not a confirmed observation. "CANNOT DETERMINE (elevated risk)" with "Material for MkDocs typically mitigates via focus-scoped shortcut but browser verification required" is the most epistemically honest verdict given available evidence. The concern level is preserved — "elevated risk" is retained. This is a Minor nuance, not a substantive error.

*Verdict:* Counter-argument noted but does not overturn the correction. CANNOT DETERMINE (elevated risk) is appropriate.

**Claim 2: The convergence sentence "Both ratio estimates converge on the same remediation verdict" resolves the W-015b evidence quality concern.**

*Counter-argument:* The iter-3 review (DA-002-RI3) noted the ratio discrepancy (~1.7:1 vs. ~2.36:1) as a Minor evidence quality finding. The correction adds a convergence sentence. But the fundamental evidence quality issue — that the document presents two different measurements of the same quantity without explaining the discrepancy — is not resolved. A reader still sees "~1.7:1 (estimated)" in the table and "~2.36:1" (referenced in the body note) without understanding why they differ. The convergence sentence says they "converge on the same verdict" but does not explain the methodological cause of the ~0.66:1 divergence. A developer running a browser measurement could get a third value.

*Assessment:* The iter-3 review's DA-002-RI3 finding was specifically that "two divergent estimates without a convergence statement" needed a convergence statement added. The correction adds exactly that. The request was not to explain the methodological divergence — it was to acknowledge that both point to the same remediation. The "verify with browser measurement" qualifier has been present since iter-2 and covers the case where a developer measures a third value. The Evidence Quality impact of the convergence sentence is that it eliminates the ambiguity about whether the two estimates affect the remediation verdict. The residual — unexplained method divergence — was noted as acceptable in iter-3 (MEDIUM confidence rating). The correction is sufficient for the stated scope.

*Verdict:* Counter-argument is a nuance within the existing MEDIUM confidence rating. Not a new finding.

**Claim 3: The Audit Scope theme naming correction closes the Methodological Rigor gap identified in iter-3.**

*Counter-argument:* The iter-3 review noted "Audit Scope section (line 137) still says 'Color contrast assessed by visual analysis and theme inspection (Material for MkDocs default theme)' — this is a minor stale reference." The correction changes this to the correct saucer-boy theme description. However, there is a subtle question: the Audit Scope section also contains a separate "Theme:" subsection (lines 175–176) that was already correct. Having the methodology sentence now match the Theme subsection is purely an internal consistency improvement. Does this correction meaningfully improve Methodological Rigor, or is it just cosmetic?

*Assessment:* Methodological Rigor evaluates whether the stated methodology accurately describes what was actually done. The methodology sentence describing which theme was inspected for contrast assessment was stale — it stated "default theme" when the actual methodology used was "custom saucer-boy theme." Correcting this is a genuine MR improvement: a future evaluator reading the methodology can now verify contrast claims against the correct CSS source. The improvement is incremental but real.

*Verdict:* Claim stands. The correction is a genuine MR improvement, not merely cosmetic.

**Claim 4: The SC 2.5.3 methodology note is a documented carryover that does not block PASS.**

*Counter-argument:* The iter-3 review noted SC 2.5.3 (Label in Name) conflates with SC 1.1.1 analysis. The iter-4 scope as stated in the frontmatter included "SC 2.5.3 visible-label methodology sentence" but the revision log entry for iter-4 does NOT include SC 2.5.3 as a correction made. Looking at the iter-4 frontmatter `iter4_scope` field (line 57): "SC 2.5.3 visible-label methodology sentence" is listed in the *scope* field from iter-3 review. But the `corrections` field (line 60) does NOT mention SC 2.5.3. Was SC 2.5.3 corrected or not?

*Assessment:* The task specification ("4 one-sentence editorial closures") explicitly lists only 4 corrections: FM-001-RI3, IN-001-RI3+DA-001-RI3, DA-003-RI3, DA-002-RI3. SC 2.5.3 was mentioned as a potential iter-4 item in the iter-3 gap analysis but was NOT included in the iter-4 closure task. The `iter4_scope` field in the old frontmatter (from rescope-iter-3) reflected the iter-3 review's suggestion list, not the iter-4 implementation scope. The `corrections` field for rescope-iter-4 correctly lists only the 4 implemented corrections. SC 2.5.3 remains an open Minor carryover from iter-3 — at the same level it was at iter-3. This does not introduce a regression; it maintains a pre-existing Minor item.

*Verdict:* SC 2.5.3 is a pre-existing carryover. Its presence at Minor level does not block PASS if the composite reaches threshold.

### S-002 Summary

No core claims overturned. Nuances identified:

| Finding | Severity | Description |
|---------|----------|-------------|
| DA-001-RI4 | Minor | SC 2.1.4 CANNOT DETERMINE may understate risk vs. prior "FAIL candidate" — Material `/` shortcut is typically global, not focus-scoped; CANNOT DETERMINE is more epistemically honest but slightly less directional than FAIL candidate. Elevated risk qualifier preserved. |
| DA-002-RI4 | Minor (carryover) | W-015b ratio method divergence (~1.7:1 vs ~2.36:1) still unexplained; convergence sentence resolves remediation ambiguity but not method cause. Pre-existing MEDIUM confidence covers this. |
| DA-003-RI4 | Minor (carryover) | SC 2.5.3 not included in iter-4 corrections; remains open minor carryover from iter-3. Does not affect remediation guidance — SC 2.5.3 findings in the per-SC section are substantively correct even if the methodology framing is suboptimal. |

All three are Minor or pre-existing carryovers. No Critical or Major counter-arguments.

---

## S-004: Pre-Mortem Analysis

*Prospective scenario: This review PASSES the deliverable (rescope-iter-4). What could go wrong after acceptance?*

**PM-001-RI4: SC 2.1.4 Verdict Softening Creates Synthesis Ambiguity**

*Scenario:* A downstream synthesis agent reads the Handoff Data (line 943): "SC-2.1.4 | SC 2.1.4 (WCAG 2.2, Level A) | Operable | 2 | Verify/disable `/` global search shortcut." The Handoff Data correctly shows Sev 2 and a clear remediation. However, the SC body says "CANNOT DETERMINE (elevated risk)" — a reader relying only on the Handoff Data gets a clearer "fix this" signal than a reader drilling into the SC body. This is actually a better state than iter-3 (where the SC body said "PASS with caveat" but the Keyboard table said "FAIL candidate") — but the synthesis agent should understand that CANNOT DETERMINE means "measure this first, then remediate if confirmed."

*Probability:* Low — the Handoff Data remediation text "Verify/disable" captures the correct action regardless of the CANNOT DETERMINE vs. FAIL distinction.

*Assessment:* Acceptable. The Handoff Data remediation guidance is actionable regardless of the SC verdict label.

**PM-002-RI4: FEAT-040-004 Dependency on XP-05**

*Scenario:* FEAT-040-005 PASSES this review. XP-05 consistency check (QG-2) requires both FEAT-040-004 and FEAT-040-005 to be complete. Per ORCHESTRATION.yaml, FEAT-040-004 (heuristic evaluator) is at iter-6 with score 0.89 (REVISE, gap 0.03). If FEAT-040-004 passes iter-7, XP-05 consistency becomes available. If FEAT-040-004 fails iter-7, QG-1A remains partially blocked despite FEAT-040-005 PASS.

*Assessment:* FEAT-040-005's quality is independent of FEAT-040-004's state. The PASS verdict for FEAT-040-005 is valid regardless. XP-05 consistency is a Phase 2 deliverable; it does not block FEAT-040-005 acceptance. ACCEPTABLE — this is an orchestration sequencing dependency, not a defect in FEAT-040-005.

**PM-003-RI4: SC Count Methodology Ambiguity Persists**

*Scenario:* A developer receiving this audit as a remediation brief counts the SCs evaluated and arrives at 40+ (per independent count in iter-3 review). They question whether key SCs are missing from remediation priorities.

*Assessment:* The SC Count Note explains that 31 refers to POUR-table-listed SCs. All Sev-2+ findings are in the Handoff Data and Remediation Priorities tables regardless of the 31 vs. 40+ count question. No remediation is missed due to the count methodology. Low impact. ACCEPTABLE.

**PM-004-RI4: Dark Mode Measurement Gap Persists Post-PASS**

*Scenario:* Phase 4 remediation work (per the Inclusive Design Adoption Roadmap) includes "dark mode link underline (W-015b)" and "keyboard testing." A developer implements W-015b fix before measurement and applies rgba(179,157,219,1.0). Browser measurement yields ~7.6:1 (per iter-3 independent calculation), not ~8.3:1 as stated. The developer notices the ratio discrepancy. The W-015b convergence sentence mitigates this — both estimates are far above 3:1, so the discrepancy does not affect pass/fail.

*Assessment:* The W-015b convergence sentence (EC-4) directly mitigates this scenario. The "verify with browser measurement" qualifier remains. ACCEPTABLE.

---

## S-012: FMEA

### Component-Level Failure Mode Analysis (Iter-4 Scope)

| Component | Failure Mode | Severity (1-5) | Occurrence (1-5) | Detectability (1-5) | RPN | Status |
|-----------|-------------|----------------|------------------|---------------------|-----|--------|
| SC 2.1.4 harmonization (all 4 locations) | One location retains prior inconsistent label | 2 | 1 | 1 | 2 | VERIFIED — all 4 locations confirmed CANNOT DETERMINE (elevated risk) |
| Audit Scope theme naming | Residual "default theme" instance in a different section | 2 | 1 | 1 | 2 | VERIFIED — no residual instances; full-text grep confirms single location corrected |
| DA-003-RI3 phrasing | Self/adversarial distinction still ambiguous after correction | 2 | 1 | 1 | 2 | VERIFIED — "these are distinct" is an explicit disambiguating statement |
| DA-002-RI3 convergence sentence | Sentence internally inconsistent (one estimate above threshold, one below) | 3 | 1 | 1 | 3 | VERIFIED — both 1.7:1 and 2.36:1 are below 3:1; sentence is accurate |
| SC 2.5.3 carryover | SC 2.5.3 methodology note not in iter-4 scope; creates expectations gap | 1 | 2 | 2 | 4 | ACCEPTABLE — labeled as carryover in iter-3; within pre-existing Minor tolerance |
| POUR Operable SCs Evaluated column | SC 2.1.4 added but column sum changes | 1 | 1 | 1 | 1 | VERIFIED — POUR Operable now lists SC 2.1.4 in SCs Evaluated; FAIL rollup unchanged |
| Frontmatter iter-4 adv_score field | Still null (pending this review) | 0 | — | — | 0 | EXPECTED — adv_score and adv_verdict updated after this review completes |
| Self-score section heading | Title "Rescope Iter-4" matches iteration correctly | 0 | — | — | 0 | VERIFIED — heading updated at line 949 |

**Highest RPN item:** SC 2.5.3 carryover (RPN 4) — pre-existing Minor. All other components verified correct at RPN <= 3. No new failure modes introduced by iter-4 corrections.

**FMEA summary:** Zero new failure modes introduced. All 4 iter-4 corrections verified correct with low failure probability. Highest risk is pre-existing SC 2.5.3 methodology carryover at RPN 4 — acceptable given it does not affect remediation guidance.

---

## S-013: Inversion

*What would make the iter-4 corrections fail to achieve a PASS?*

**IN-001-RI4: Is the IC Score of 0.925 Genuinely Warranted?**

*Inverted assumption:* SC 2.1.4 harmonization and DA-003-RI3 phrasing together justify IC jumping from 0.91 (iter-3 adversarial) to 0.925 (iter-4 self-assessed).

*Challenge:* The iter-3 review scored IC at 0.91 with these carryover residuals:
1. SC 2.1.4 cross-section inconsistency — now CLOSED
2. SC 2.5.3 methodology overlap with SC 1.1.1 — NOT in iter-4 scope, still open
3. Self-score vs. projected-adversarial phrasing — now CLOSED

Two of three IC residuals closed. The iter-3 reviewer projected IC at 0.91 with the residuals present. With two of three closed, IC at ~0.920–0.925 is plausible. The remaining SC 2.5.3 overlap is the lowest-impact of the three residuals. At 0.920 (the lower bound of the self-projected range), IC would still represent a +0.01 increment from iter-3, consistent with closing two Minor residuals.

*However:* The SC 2.1.4 harmonization changes the verdict *type* (PASS-with-caveat → CANNOT DETERMINE) but the per-SC analysis text is substantively unchanged — same evidence, same remediation. The internal consistency improvement from this change is specifically that the label is now consistent across 4 locations. This is a genuine IC improvement. Similarly, the DA-003-RI3 phrasing correction eliminates a specific documented IC concern. Together, these two targeted IC corrections justify an increment in the 0.01–0.02 range from the 0.91 iter-3 baseline.

*Revised estimate:* IC at 0.920–0.925 is within range. 0.925 is at the high end; 0.920 is conservative. The scoring below applies 0.920 as the conservative adversarial estimate for IC.

*Verdict:* Self-assessed IC 0.925 may be very slightly optimistic; conservative adversarial scoring at 0.920 is warranted given SC 2.5.3 carryover.

**IN-002-RI4: Does MR at 0.89 Represent a Genuine +0.01 from Iter-3?**

*Inverted assumption:* Correcting the Audit Scope theme name justifies MR moving from 0.88 to 0.89.

*Challenge:* The iter-3 MR score of 0.88 reflected: no methodological changes, all source verification retained, one pre-existing stale sentence in Audit Scope. The stale sentence said "default theme" rather than identifying the actual theme inspected. This is a methodological accuracy issue — the audit scope description misidentified which theme was under evaluation.

*Assessment:* Correcting a methodology description error is a genuine MR improvement. The sentence now correctly identifies the theme and source file that were evaluated. An evaluator reading the methodology section can now verify the contrast methodology against the correct CSS source. MR at 0.89 (+0.01 from 0.88) is a modest and defensible increment. The remaining MR constraint is the dark mode contrast measurement gap (browser DevTools required), which is unchanged and appropriate for the CANNOT DETERMINE verdict.

*Verdict:* MR 0.89 is defensible. +0.01 increment is consistent with the magnitude of the correction.

**IN-003-RI4: Could the Iter-4 Corrections Introduce Any New Inconsistency Not Present in Iter-3?**

*Inverted assumption:* The iter-4 corrections are purely additive/corrective with no new inconsistencies.

*Challenge:* The SC 2.1.4 verdict change from "FAIL (candidate)" in Keyboard table to "CANNOT DETERMINE (elevated risk)" softens the Keyboard table's assessment. The Persona Spectrum section (line 782) still reads: "Current Compliance: SC 4.1.2 FAIL (search label), SC 2.1.4 candidate FAIL." After the harmonization, SC 2.1.4 is "CANNOT DETERMINE" not "candidate FAIL." Is the Persona Spectrum section now inconsistent?

*Evidence check:* Persona Spectrum line 782: "Current Compliance: SC 4.1.2 FAIL (search label), SC 2.1.4 candidate FAIL."

This is a new minor inconsistency: after iter-4 harmonization, SC 2.1.4 is "CANNOT DETERMINE (elevated risk)" in all 4 mandated locations, but the Persona Spectrum section still uses "candidate FAIL." The Persona Spectrum section was not listed in the 4 harmonization locations (the 4 locations were: per-SC body, Keyboard table, Synthesis Judgments, POUR Operable row). The Persona Spectrum uses a different format ("Current Compliance" bullet) and was not updated.

*Severity assessment:* This is a Minor new inconsistency introduced by the iter-4 harmonization. The Persona Spectrum section's "candidate FAIL" and the harmonized "CANNOT DETERMINE (elevated risk)" are functionally equivalent in severity — both signal an elevated-risk unconfirmed finding. The "candidate FAIL" framing in a contextual summary line does not materially mislead. This is a cosmetic label inconsistency, not a substantive accuracy issue.

*Finding: IN-001-RI4 — New Minor.* Persona Spectrum line 782 "SC 2.1.4 candidate FAIL" is inconsistent with the harmonized "CANNOT DETERMINE (elevated risk)" label. This is a 5th harmonization location that was missed.

**IN-004-RI4: Is the Self-Score Composite Arithmetic Correct?**

*Inverted assumption:* Raw composite 0.904 is correctly computed.

*Challenge:* Per the scoring table (line 965–972):
- Completeness: 0.905 × 0.20 = 0.181
- Internal Consistency: 0.925 × 0.20 = 0.185
- Methodological Rigor: 0.89 × 0.20 = 0.178
- Evidence Quality: 0.885 × 0.15 = 0.133 (actually 0.885 × 0.15 = 0.13275, rounds to 0.133 ✓)
- Actionability: 0.91 × 0.15 = 0.137 (actually 0.91 × 0.15 = 0.1365, rounds to 0.137 ✓)
- Traceability: 0.90 × 0.10 = 0.090

Sum: 0.181 + 0.185 + 0.178 + 0.133 + 0.137 + 0.090 = 0.904 ✓

*Assessment:* Arithmetic checks out. Raw composite 0.904 − 0.004 calibration = 0.900 self-score.

*Verdict:* Arithmetic correct. No issue.

---

## S-014: LLM-as-Judge

### Anti-Leniency Discipline

Prior iter-3 adversarial score: 0.897. Self-score trajectory: 0.935 (r-iter-1) → 0.886 (r-iter-2, calibrated) → 0.895 (r-iter-3, calibrated) → 0.900 (r-iter-4, self-reported). Gap from iter-3 adversarial to self-estimate: +0.003. Corrections are editorial-only (4 one-sentence fixes). Expected delta is small and targeted.

**Critical anti-leniency directive:** Do NOT inflate. Score strictly. The self-projected band is 0.922–0.925; this review is the test of whether that projection is warranted. The threshold is 0.920. Apply independent judgment per dimension — do not anchor to the self-score.

### Per-Dimension Assessment

**Completeness (Weight: 0.20)**

*What full completeness looks like:* All WCAG 2.2 A/AA SCs evaluated or excluded (N/A). All 8 surfaces addressed. All findings documented with evidence. All sections complete.

*Assessment:* No changes to Completeness in iter-4. All iter-3 completeness elements are retained:
- 31 in-scope SCs addressed per POUR table methodology
- 8 surfaces evaluated
- 5 Persona Spectrum patterns complete
- All findings (W-001 through W-016) in place
- SC 2.1.4 now added to POUR Operable SCs Evaluated column — minor Completeness increment (previously omitted from the explicit list)

*Residuals unchanged from iter-3:* Dark mode contrast measurement still requires browser DevTools. SC 2.5.3 methodology note still pending.

*Score:* 0.905 — Unchanged from iter-3. SC 2.1.4 addition to POUR SCs Evaluated column is a minor positive. No new completeness gaps.

*Weighted:* 0.181

**Internal Consistency (Weight: 0.20)**

*What full internal consistency looks like:* POUR rollup matches per-SC verdicts. Self-score labeling consistent. SC count consistent. Cross-section references aligned. Remediation priorities match findings.

*Assessment:* Iter-4 IC improvements:
1. SC 2.1.4 harmonized across 4 documented locations — consistent CANNOT DETERMINE (elevated risk) label. This closes the most significant IC residual from iter-3 (the PASS-vs-FAIL cross-section inconsistency).
2. DA-003-RI3 phrasing — self-score vs. projected adversarial explicitly disambiguated. Second IC residual from iter-3 CLOSED.
3. Prior iter-3 IC improvements (POUR Understandable FAIL, SC count 31, self-score 0.886 labeling) all retained.

*New Minor inconsistency (IN-001-RI4):* Persona Spectrum line 782 retains "SC 2.1.4 candidate FAIL" while all 4 mandated harmonization locations now read "CANNOT DETERMINE (elevated risk)." This is a 5th location that was not updated. It is cosmetically inconsistent (both labels signal the same elevated-risk finding) but technically a label inconsistency.

*Remaining carryover:* SC 2.5.3 (Label in Name) methodology framing — unchanged from iter-3.

*Assessment:* The two primary IC residuals from iter-3 are CLOSED. One new Minor inconsistency (Persona Spectrum SC 2.1.4 label) was introduced. Net IC position: +0.01 improvement from closed residuals; −0.005 for new Persona Spectrum inconsistency. Net IC increment from iter-3: approximately +0.005 to +0.010.

*Score:* 0.915 — Two iter-3 IC residuals closed (+0.015 from 0.91 baseline); one new Minor inconsistency (Persona Spectrum SC 2.1.4 label, −0.005); SC 2.5.3 carryover unchanged (no additional deduction — already priced in at iter-3). Net: 0.91 + 0.015 − 0.005 ≈ 0.915. More conservative than self-assessed 0.925 — the new Persona Spectrum inconsistency was not in the self-score, and SC 2.5.3 carryover has non-zero residual weight.

*Weighted:* 0.183

**Methodological Rigor (Weight: 0.20)**

*What full methodological rigor looks like:* WCAG-EM 1.0 procedure followed. Evidence Verification Protocol retained. Confidence levels calibrated. CANNOT DETERMINE verdicts cite specific gaps. Methodology description matches what was actually done.

*Assessment:* FM-001-RI3 corrects the Audit Scope methodology sentence from "default theme" to the specific saucer-boy theme with CSS file reference. This closes the specific MR gap noted in iter-3. The correction is technically accurate — the methodology section now correctly identifies the CSS source used for contrast analysis.

No other methodological changes in iter-4. All iter-3 methodology (Evidence Verification Protocol, CANNOT DETERMINE citations, confidence labeling) is retained.

*Residuals:* Dark mode contrast still requires browser DevTools. This is a legitimate methodology limitation acknowledged with CANNOT DETERMINE verdicts. The SC 2.1.4 change from "PASS with caveat" to "CANNOT DETERMINE" is more methodologically rigorous (reduces overconfidence in a verdict that could not be verified via WebFetch).

*Score:* 0.890 — One genuine MR improvement (Audit Scope theme identification). +0.01 from iter-3 baseline of 0.88. Remaining MR constraints (dark mode measurement, WebFetch limitations) unchanged and correctly acknowledged. Consistent with self-assessed 0.890.

*Weighted:* 0.178

**Evidence Quality (Weight: 0.15)**

*What full evidence quality looks like:* Claims backed by direct source observation. Confidence levels distinguish observed from inferred. Evidence specific enough to reproduce independently.

*Assessment:* No new evidence claims in iter-4. DA-002-RI3 adds a convergence sentence to W-015b — this is a logical deduction from existing evidence (both estimates are below threshold), not a new empirical claim. The convergence sentence marginally improves Evidence Quality by explicitly confirming that the dual-estimate situation is not ambiguous regarding remediation.

*Residuals:* W-015b ~8.3:1 post-fix estimate vs. independent ~7.6:1 is a carryover from iter-3. Both pass the 3:1 threshold. The "verify with browser measurement" qualifier is present.

*Score:* 0.885 — +0.005 from iter-3 0.88 baseline. DA-002-RI3 convergence sentence closes the open ambiguity about dual-estimate remediation direction. Consistent with self-assessed 0.885. The W-015b ratio imprecision residual holds EQ below 0.90.

*Weighted:* 0.133

**Actionability (Weight: 0.15)**

*What full actionability looks like:* Each finding has specific, implementable remediation. Effort estimates present. Owner classification present.

*Assessment:* No changes to Actionability in iter-4. The W-015b remediation (specific CSS property, old value, new value, file path) from iter-3 is unchanged. The SC 2.1.4 verdict change from "FAIL candidate" to "CANNOT DETERMINE (elevated risk)" affects the priority — "Verify/disable" is still the correct action. The Handoff Data entry for SC-2.1.4 (Remediation: "Verify/disable `/` global search shortcut") is still actionable.

All Remediation Priorities (1–13) are retained from iter-3.

*Score:* 0.910 — Unchanged from iter-3. No new Actionability improvements or regressions.

*Weighted:* 0.137

**Traceability (Weight: 0.10)**

*What full traceability looks like:* All corrections traceable to findings that prompted them. Finding IDs consistent. Revision History complete. Frontmatter accurate.

*Assessment:* Iter-4 traceability improvements:
- Revision History table: rescope-iter-4 row present (lines 58–66 in frontmatter, lines 121–128 in Revision History table) with all 4 corrections listed (IN-001-RI3+DA-001-RI3, DA-003-RI3, FM-001-RI3, DA-002-RI3).
- Footer (lines 994–996): rescope-iter-4 corrections listed explicitly.
- Frontmatter `corrections:` field: all 4 corrections cited.
- Each correction is traceable to the iter-3 review finding that prompted it (by finding ID).
- SC 2.1.4 added to POUR Operable SCs Evaluated column provides additional traceability for the harmonization.

*Residual:* SC count methodology not fully explicit about "POUR-table-listed SCs only" — unchanged from iter-3. The note at line 984 explains the reconciliation adequately.

*Score:* 0.900 — +0.01 from iter-3 0.89 baseline. Revision History, footer, and frontmatter correctly document all 4 iter-4 corrections with source finding IDs. SC 2.1.4 POUR Operable column update provides clear traceability of the harmonization.

*Weighted:* 0.090

### S-014 Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.905 | 0.181 |
| Internal Consistency | 0.20 | 0.915 | 0.183 |
| Methodological Rigor | 0.20 | 0.890 | 0.178 |
| Evidence Quality | 0.15 | 0.885 | 0.133 |
| Actionability | 0.15 | 0.910 | 0.137 |
| Traceability | 0.10 | 0.900 | 0.090 |
| **COMPOSITE** | **1.00** | — | **0.902** |

Wait — recomputing to verify arithmetic:
- 0.905 × 0.20 = 0.1810
- 0.915 × 0.20 = 0.1830
- 0.890 × 0.20 = 0.1780
- 0.885 × 0.15 = 0.13275 → 0.133
- 0.910 × 0.15 = 0.1365 → 0.137 (rounded)
- 0.900 × 0.10 = 0.0900

Sum: 0.181 + 0.183 + 0.178 + 0.133 + 0.137 + 0.090 = **0.902**

**Threshold:** 0.92

**Gap:** 0.902 − 0.920 = −0.018

The composite of **0.902** does not reach the 0.920 threshold.

**Threshold assessment clarification:** The 0.020 gap is primarily driven by the new Persona Spectrum inconsistency (IN-001-RI4, −0.005 to IC) and by the IC self-score being more conservatively set at 0.915 vs. the self-assessed 0.925. Without the Persona Spectrum inconsistency, IC would be ~0.920, yielding composite ~0.904. Still short of 0.920.

### Gap Analysis for Potential Iter-5

The composite of 0.902 falls in the REVISE band (0.85–0.91). The gap to threshold is 0.018.

The primary constraint dimensions:
1. **Internal Consistency (0.915 scored vs. 0.925 self-assessed, weighted 0.183 vs. target 0.184):** The delta between 0.915 and the 0.920+ needed in IC is driven by (a) the Persona Spectrum SC 2.1.4 label inconsistency (IN-001-RI4 — one-word fix: "CANNOT DETERMINE" in line 782) and (b) the SC 2.5.3 methodology carryover. Closing IN-001-RI4 alone (+0.005 × 0.20 = +0.001 composite) and accepting the SC 2.5.3 carryover would bring IC to ~0.920.
2. **All other dimensions:** At their current scored levels, all other dimensions are at or near the threshold contribution needed.

**Minimum iter-5 scope (if proceeding):**

| Item | Action | Dimension Impact |
|------|--------|-----------------|
| IN-001-RI4 | Persona Spectrum line 782: change "SC 2.1.4 candidate FAIL" to "SC 2.1.4 CANNOT DETERMINE (elevated risk)" | IC +0.005 |
| SC 2.5.3 carryover (optional) | Add sentence clarifying SC 2.5.3 logo-as-visible-label methodology | IC +0.005, MR +0.005 |

Estimated composite after IN-001-RI4 alone: 0.902 + (0.005 × 0.20) = 0.902 + 0.001 = 0.903. Still below threshold.

The issue is that the composite requires approximately +0.018 to reach 0.920, and available editorial fixes provide at most ~0.002–0.003 per composite point. The Persona Spectrum fix and SC 2.5.3 fix together would add approximately +0.003–0.004 to the composite, bringing it to ~0.905–0.906. Still below 0.920.

**Honest assessment of the gap:**

The fundamental constraint is that IC (0.915), MR (0.890), Evidence Quality (0.885), and their combined weighted contribution is 0.902. Reaching 0.920 requires raising the composite by 0.018. At the current scoring level, the dimensions holding the composite below threshold are:
- IC needs to reach ~0.940 to contribute 0.188 (vs. current 0.183) — a +0.005 composite gain
- MR needs to reach ~0.920 to contribute 0.184 (vs. current 0.178) — a +0.006 composite gain
- EQ needs to reach ~0.920 to contribute 0.138 (vs. current 0.133) — a +0.005 composite gain

These gains require substantive improvements (confirmed measurements, SC 2.5.3 methodology work) beyond one-sentence editorial fixes. The editorial-only correction approach has been maximally exploited — the remaining gains require either: (a) browser DevTools measurements that confirm CANNOT DETERMINE items as PASS (MR, EQ), or (b) SC 2.5.3 methodology clarification (IC, MR).

**Iteration ceiling note:** This is rescope-iter-4 of a 7-iteration ceiling (RT-M-010 C3 = max 7). Three iterations remain (rescope-iter-5, -6, -7). However, the editorial-only approach has reached diminishing returns — the gap of 0.018 cannot be closed by one-sentence fixes.

---

## Regression Check

All iter-3 verified pass-level sections checked for regressions:

| Section | Iter-3 State | Iter-4 Check | Status |
|---------|-------------|-------------|--------|
| Evidence Verification Protocol | All 4 V-001 through V-004 corrections intact | Unchanged — all verification entries present | NO REGRESSION |
| W-001 Install from GitHub citation | CONFIRMED — lines 79/95/107/125 | Unchanged | NO REGRESSION |
| W-002 false positive removal | W-002a Sev 1 replacement in place | Unchanged | NO REGRESSION |
| W-010 CANNOT DETERMINE | Correct | Unchanged — SC 3.1.1 CANNOT DETERMINE | NO REGRESSION |
| W-015 footer PASS | Confirmed ≈9.7:1 | Unchanged | NO REGRESSION |
| Navigation table (H-23/H-24) | PASS | Navigation table intact, 16 sections with anchor links | NO REGRESSION |
| POUR P, O, R rollups | P=FAIL, O=FAIL, R=FAIL | Unchanged (SC 2.1.4 added to O Dominant Failures — appropriate augmentation, not regression) | NO REGRESSION |
| POUR Understandable FAIL | Iter-3 correction retained | FAIL driven by SC 3.3.2 — unchanged | NO REGRESSION |
| SC count frontmatter 31 | Reconciled | `scs_in_scope: 31` unchanged | NO REGRESSION |
| Self-score labeling 0.886 iter-2 baseline | Calibrated 0.886 in Synthesis Judgments | Entry unchanged (0.886 is iter-2 calibrated reference; iter-4 self-score is 0.900 as stated) | NO REGRESSION |
| W-015b specific CSS value | `rgba(179,157,219,1.0)` in W-015b note + Remediation table | Unchanged, convergence sentence added | NO REGRESSION |
| XP-05 Cross-Framework Consistency | F-010/W-001 convergence section | Unchanged | NO REGRESSION |
| Persona Spectrum (5 patterns) | Complete | All 5 patterns intact | NO REGRESSION (note: line 782 label inconsistency is new, not a regression of prior content) |
| Handoff Data | Complete and accurate | SC-2.1.4 entry present, remediation unchanged | NO REGRESSION |
| Audit Scope Theme section | Correct (rescope-iter-2 verified) | Correct and expanded — FM-001-RI3 also corrected the methodology sentence | NO REGRESSION |
| Remediation Priorities (13 items) | Complete | Unchanged from iter-3 | NO REGRESSION |
| Strategic Implications | Complete | Unchanged | NO REGRESSION |

**No regressions detected in iter-3 pass-level sections.**

**New finding introduced by iter-4:** IN-001-RI4 — Persona Spectrum line 782 SC 2.1.4 label inconsistency (one location not updated during harmonization). This is a new Minor item, not a regression of prior content.

---

## Consolidated Findings Summary

| ID | Strategy | Severity | Finding | Section |
|----|----------|----------|---------|---------|
| IN-001-RI4 | S-013 | Minor | Persona Spectrum line 782 retains "SC 2.1.4 candidate FAIL" while all 4 mandated harmonization locations now read "CANNOT DETERMINE (elevated risk)" — 5th harmonization location missed | Persona Spectrum section |
| DA-001-RI4 | S-002 | Minor | SC 2.1.4 CANNOT DETERMINE may slightly understate risk vs. prior "FAIL candidate" — Material `/` shortcut is typically global; elevated risk qualifier preserved; epistemically more accurate | SC 2.1.4 per-SC section |
| DA-002-RI4 | S-002 | Minor (carryover) | W-015b ratio method divergence unexplained; convergence sentence resolves remediation ambiguity but not measurement method cause | Color Contrast Analysis |
| DA-003-RI4 | S-002 | Minor (carryover) | SC 2.5.3 not included in iter-4 corrections; remains open minor carryover from iter-3 | SC 2.5.3 section |

**Critical findings this iteration:** 0
**Major findings this iteration:** 0
**Minor findings this iteration:** 1 new (IN-001-RI4) + 3 carryover or nuances (DA-001-RI4 nuance, DA-002-RI4 carryover, DA-003-RI4 carryover)

All 4 iter-4 editorial corrections confirmed CLOSED. One new Minor finding (IN-001-RI4) identified — a 5th harmonization location (Persona Spectrum line 782) that was not included in the SC 2.1.4 harmonization. Three carryover/nuance items retained from prior iterations at Minor level.

---

## Verdict

**COMPOSITE SCORE: 0.902**

**THRESHOLD: 0.92**

**Self-score gap analysis:** Self-score 0.900 vs. adversarial 0.902. Gap: +0.002 (agent self-score was conservative at 0.900; adversarial agrees the correction gains are real but identifies the Persona Spectrum inconsistency as a limiting factor in IC). Self-score and adversarial score are well-calibrated at ±0.002 precision.

**VERDICT: REVISE**

**Band:** 0.902 falls in the 0.85–0.91 REVISE band (below threshold; gap to threshold = 0.018).

---

### Gap Analysis

The 0.902 composite is 0.018 below the 0.92 threshold. The gap was projected by the iter-3 review as +0.025 for the 4 editorial corrections; the actual measured gain is +0.005 (0.897 → 0.902). The shortfall from projection (~0.020) has two causes:

1. **Persona Spectrum SC 2.1.4 label inconsistency (IN-001-RI4):** A 5th harmonization location was not included in the iter-4 corrections. This introduced a new IC deduction (−0.005 × 0.20 = −0.001 composite) that partially offset the IC gain from closing the two primary residuals.

2. **Editorial fix ceiling:** The iter-3 review projected +0.025, but the actual deliverable score gain is bounded by the editorial nature of the fixes. The composite reflects that IC (0.915 vs. projected 0.925) and MR/EQ (unchanged from projections) are the limiting dimensions. The editorial approach cannot close the IC gap without also resolving the SC 2.5.3 carryover.

### Iter-5 Scope (if proceeding)

The following targeted corrections would be the minimum iter-5 scope:

| Item | Action | Dimension Impact |
|------|--------|-----------------|
| IN-001-RI4 (new) | Persona Spectrum line 782: "SC 2.1.4 candidate FAIL" → "SC 2.1.4 CANNOT DETERMINE (elevated risk)" | IC +0.003–0.005 |
| SC 2.5.3 methodology note (carryover) | Add sentence: "SC 2.5.3 analysis for the logo link addresses whether the accessible name includes the visible label — for a graphical link with `alt='logo'`, the visible label equivalent is the brand name 'Jerry Framework', which does not appear in the accessible name 'logo'; SC 2.5.3 failure is distinct from SC 1.1.1 failure and not redundant." | IC +0.005, MR +0.005 |

**Important note:** Even with both fixes above, the estimated composite is:
- IC: 0.915 + 0.010 = 0.925 → 0.925 × 0.20 = 0.185 (vs current 0.183) = +0.002 composite
- MR: 0.890 + 0.005 = 0.895 → 0.895 × 0.20 = 0.179 (vs current 0.178) = +0.001 composite
- Estimated post-iter-5: 0.902 + 0.003 ≈ **0.905** — still below 0.920.

**Honest assessment of path to PASS:**

The composite of 0.902 is limited by MR (0.890) and EQ (0.885) — both of which require browser DevTools measurements to improve beyond the current CANNOT DETERMINE-constrained levels. The editorial-only approach can add at most ~0.003 to the composite through one-sentence fixes. Reaching 0.920 from 0.902 requires +0.018, which exceeds what editorial-only corrections can deliver.

Two paths to PASS exist:

**Path A: Browser DevTools evidence integration**
- Confirm `<html lang="en">` in rendered source → SC 3.1.1 becomes PASS → MR +0.010, EQ +0.010
- Measure Platform Support badge contrast → resolves CANNOT DETERMINE → EQ +0.005
- Confirm focus ring CSS → resolves focus visibility CANNOT DETERMINE → MR +0.005
- Estimated composite: 0.902 + 0.020 ≈ **0.922** → PASS

**Path B: Accept current scope with SC 2.5.3 + IN-001-RI4 fixes + accept 0.905 composite**
- Cannot reach 0.920 with editorial fixes alone from the current 0.902 baseline.
- Path B is not viable for a PASS outcome.

**Recommendation to orchestrator:** Either (1) scope iter-5 to include browser DevTools verification as evidence-gathering (departing from editorial-only approach) to close the MR/EQ gap, or (2) accept a ceiling at ~0.905 editorial-only and make a user-escalation decision per H-31 about whether the remaining 0.015 gap is acceptable given the risk profile of the site (developer-focused OSS docs, lower ADA exposure).

**Rescope ceiling note:** This is rescope-iter-4 of a 7-iteration ceiling (RT-M-010 C3 = max 7). Three iterations remain. The editorial-only path has been maximally exploited. Browser evidence integration (Path A) is feasible within the remaining 3 iterations.

---

## Execution Statistics

- **Total Findings:** 4 (1 new Minor + 3 carryover/nuance)
- **Critical:** 0
- **Major:** 0
- **Minor:** 1 new (IN-001-RI4) + 3 carryover (DA-001-RI4, DA-002-RI4, DA-003-RI4)
- **Protocol Steps Completed:** 6 of 6 (S-007, S-002, S-004, S-012, S-013, S-014)
- **Iter-4 Editorial Closures Verified:** 4 of 4 (all CLOSED)
- **Regressions Detected:** 0
- **New Findings Introduced:** 1 (IN-001-RI4 — Persona Spectrum SC 2.1.4 label inconsistency)
- **Source Verifications Required:** None for editorial scope; browser DevTools required for Path A (PASS route)

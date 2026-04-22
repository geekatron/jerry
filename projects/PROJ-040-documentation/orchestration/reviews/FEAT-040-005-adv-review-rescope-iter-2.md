# Adversarial Review: FEAT-040-005 — Rescope Iteration 2 (C3 Multi-Strategy)

## Execution Context

| Field | Value |
|-------|-------|
| **Feature ID** | FEAT-040-005 |
| **Deliverable** | `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-005/ux-inclusive-evaluator-output.md` |
| **Review Type** | C3 Adversarial Review — Rescope Iteration 2 (corrections verified) |
| **Criticality** | C3 |
| **Quality Threshold** | 0.92 |
| **Iteration** | rescope-iter-2 |
| **Agent Self-Score** | 0.91 |
| **Prior Iter-1 Score** | 0.807 (REVISE — 3 Critical factual errors) |
| **Strategies Executed** | S-007, S-002, S-004, S-012, S-013, S-014 |
| **Verification Methods** | Read (INSTALLATION.md, saucer-boy.css, mkdocs.yml), Grep (bold step patterns), WebFetch (live site × 2) |
| **Executed** | 2026-04-20 |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Independent Source Verification Log](#independent-source-verification-log) | Mandatory file read + WebFetch verification of all claimed corrections |
| [S-007: Constitutional AI Critique](#s-007-constitutional-ai-critique) | Behavioral rule and P-022 compliance |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-arguments against core claims |
| [S-004: Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Prospective failure enumeration |
| [S-012: FMEA](#s-012-fmea) | Component-level failure mode analysis |
| [S-013: Inversion](#s-013-inversion) | Assumption stress-testing |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Weighted composite score |
| [Consolidated Findings Summary](#consolidated-findings-summary) | All findings by severity |
| [Verdict](#verdict) | PASS / REVISE decision |

---

## Independent Source Verification Log

All four corrections claimed in rescope-iter-2 were independently verified before scoring. This section documents each verification step with file read evidence.

### CV-001: V-002 Correction — W-002 False Positive (INSTALLATION.md line 678)

**Claim:** "file it" and "file that too" at INSTALLATION.md:678 are plain prose, not hyperlinks.

**Verification method:** Direct file Read of `/docs/INSTALLATION.md` lines 670-690.

**Finding (CONFIRMED):** Line 678 reads: `If something's broken, file it. If something's confusing, file that too.` — plain prose text, not linked. Lines 680-681 contain the actual hyperlinks using URL-as-text labels. W-002 false positive removal is correct.

---

### CV-002: V-001 Correction — W-001 Section Citation (INSTALLATION.md Install from GitHub section)

**Claim:** `## Install from GitHub` section (lines 79, 95, 107, 125) uses `**Step N:**` bold patterns. `## Local Clone` section (lines 235, 253, 265) uses `### Step N:` H3 headings. W-001 applies to the bold-text Install from GitHub section.

**Verification method:** Grep pattern `\*\*Step [0-9]` on INSTALLATION.md; Read lines 55-135 and 225-285.

**Finding (CONFIRMED):** Grep output confirms:
- Line 79: `**Step 1: Add the Jerry repository as a plugin source**`
- Line 95: `**Step 2: Verify the source registered**`
- Line 107: `**Step 3: Install the plugin**`
- Line 125: `**Step 4: Confirm it landed**`

These are bold text patterns, not H3 headings. The `## Install from GitHub` section begins at line 69. Section name is confirmed correct. W-001 evidence citation in rescope-iter-2 matches source.

**Note on iter-1 discrepancy:** The original iter-1 review stated these bold patterns were at the "Session Install" section (and cited different step names). The actual section heading at line 69 is `## Install from GitHub`. The rescope-iter-2 correction is accurate — the bold-step problem is in the `## Install from GitHub` section, which is the primary recommended installation path.

---

### CV-003: V-003 Correction — W-010 FAIL → CANNOT DETERMINE (mkdocs.yml language key)

**Claim:** mkdocs.yml has no `language:` key under `theme:`. Whether Material emits `lang="en"` by default is version-dependent. CANNOT DETERMINE (elevated risk).

**Verification method:** Grep `language` on mkdocs.yml; Read mkdocs.yml lines 1-60.

**Finding (CONFIRMED):** Grep for `language` in mkdocs.yml returns no matches. Read of mkdocs.yml lines 9-38 shows the complete `theme:` block — no `language:` key present. Custom schemes `saucer-boy` and `saucer-boy-dark` are defined. The CANNOT DETERMINE verdict is appropriate — Material for MkDocs version-specific default behavior cannot be determined without browser DevTools.

---

### CV-004: V-004 Correction — W-015 Footer CSS (saucer-boy.css confirmed values)

**Claim:** Footer uses `--md-footer-bg-color: #311B92` and `--md-footer-fg-color: rgba(255,255,255,.87)` from custom saucer-boy theme, not Material default. Footer contrast ≈ 9.7:1 — PASS.

**Verification method:** Direct file Read of `docs/stylesheets/saucer-boy.css` lines 1-127.

**Finding (CONFIRMED):** Lines 42-47 of saucer-boy.css:
```css
/* Footer */
--md-footer-bg-color:         #311B92;
--md-footer-bg-color--dark:   #1A0E4B;
--md-footer-fg-color:         rgba(255, 255, 255, 0.87);
--md-footer-fg-color--light:  rgba(255, 255, 255, 0.54);
--md-footer-fg-color--lighter: rgba(255, 255, 255, 0.32);
```

The W-015 correction is accurate. Footer PASS at ≈9.7:1. No residual footer concern.

---

### CV-005: W-015b Dark Mode Link Underline (New Finding — VERIFIED, ratio refined)

**Claim:** Dark mode link underline `rgba(179,157,219,.4)` on `#1A1025` ≈ 1.7:1 — LIKELY FAIL SC 1.4.11.

**Verification method:** Read saucer-boy.css lines 120-159. Independent WCAG luminance computation.

**Finding (CONFIRMED with ratio refinement):** saucer-boy.css lines 143-149 confirm:
```css
/* Link underlines — color alone insufficient at ~2.1:1 contrast (WCAG 3:1) */
[data-md-color-scheme="saucer-boy-dark"] .md-typeset a {
  text-decoration-color: rgba(179, 157, 219, 0.4);
}
```

**Note:** The CSS comment itself (`/* color alone insufficient at ~2.1:1 contrast */`) is authored metadata, not a WCAG calculation. Independent WCAG luminance computation: rgba(179,157,219,0.4) blended on #1A1025 (RGB 26,16,37) → effective color ≈ #574872. L_effective ≈ 0.087. L_bg (#1A1025) ≈ 0.008. Computed ratio ≈ 2.36:1 (below 3:1 SC 1.4.11 threshold). The deliverable's ~1.7:1 estimate is lower than my computation but both land below the 3:1 threshold. W-015b finding is directionally correct; exact ratio requires browser measurement. The deliverable appropriately scopes this as "LIKELY FAIL [MEDIUM confidence] — requires browser measurement." Correctly not overclaimed as a confirmed FAIL.

---

### CV-006: Logo Alt Text (Live Site Verification)

**Claim:** W-011 finding asserts logo image `alt="logo"` on all 8 evaluated surfaces.

**Verification method:** WebFetch of https://jerry.geekatron.org/ and https://jerry.geekatron.org/INSTALLATION/.

**Finding (CONFIRMED):** Two independent WebFetch calls confirm logo alt text is `"logo"` in the navigation header on both pages. W-011 finding is correct.

---

### CV-007: "file it" / "file that too" NOT Hyperlinked on Live Site

**Verification method:** WebFetch of https://jerry.geekatron.org/INSTALLATION/.

**Finding (CONFIRMED):** Live site confirms "file it" and "file that too" are plain prose in the Getting Help section. The actual hyperlinks are in the bulleted list below. This confirms W-002 false positive removal is accurate.

---

### Verification Summary

| Correction | Claim | Independent Verdict | Status |
|-----------|-------|---------------------|--------|
| V-001: W-001 section corrected to Install from GitHub | Lines 79/95/107/125 bold patterns | CONFIRMED — Grep matches exactly | ACCEPTED |
| V-002: W-002 removed (false positive) | "file it" plain prose, not link | CONFIRMED — source line 678 + live site | ACCEPTED |
| V-003: W-010 FAIL→CANNOT DETERMINE | No `language:` key in mkdocs.yml; browser required | CONFIRMED — Grep no matches | ACCEPTED |
| V-004: W-015 footer PASS | #311B92 bg + rgba(255,255,255,.87) fg | CONFIRMED — CSS lines 42-47 | ACCEPTED |
| W-015b dark mode underline | ~1.7:1 estimated; requires measurement | ACCEPTED (ratio refined to ~2.36:1, still below 3:1) | ACCEPTED |
| W-011 logo alt text | alt="logo" on live site | CONFIRMED — two WebFetch calls | ACCEPTED |

All four corrections accepted. No new factual errors introduced. W-015b ratio refined but finding directionally correct.

---

## S-007: Constitutional AI Critique

### Applicable Principles

Deliverable type: WCAG accessibility audit — document artifact. Applicable rules from `.context/rules/`:
- P-001 (Truth/Accuracy), P-022 (No Deception) — factual claims
- P-011 (Evidence-Based Findings) — every claim requires evidence
- H-15 (Self-Review before presenting) — self-assessed quality score present
- H-23/H-24 (Markdown navigation table required) — document structure
- quality-enforcement.md — scoring methodology, S-014 rubric

### Principle Evaluation

**CC-001-RI2 — P-001/P-022 Truth and No Deception**

- **Principle:** HARD. Every factual claim must be accurate. No deception about capabilities, confidence levels, or actions taken.
- **Compliance criteria:** Findings must accurately reflect what was found. Confidence levels must match actual evidence certainty.
- **Evaluation:** All four iter-1 factual errors are now corrected with source evidence citations. The Evidence Verification Protocol section documents the methodology shift. The W-015b finding is correctly scoped as "LIKELY FAIL [MEDIUM confidence] — requires browser measurement" — not overclaimed. SC 3.1.1 verdict correctly reads CANNOT DETERMINE rather than FAIL. The W-001 section citation matches grep output exactly.
- **Residual risk:** The SC count arithmetic discrepancy (32 vs. 31 in-scope SCs) is acknowledged in the deliverable but unresolved. This is a minor internal consistency note, not a deception.
- **Verdict:** COMPLIANT
- **Quality dimension:** Evidence Quality, Internal Consistency

**CC-002-RI2 — P-011 Evidence-Based Findings**

- **Principle:** HARD. Every finding must include direct evidence from the evaluated artifact.
- **Compliance criteria:** Each WCAG SC verdict must cite specific source evidence — page URL, element, attribute value, or line number reference.
- **Evaluation:** All Sev-2+ findings cite specific evidence: W-001 cites lines 79/95/107/125 with step names; W-011 cites `alt="logo"` observed on all 8 surfaces; W-013 cites `<a href="#section-id">¶</a>` pattern; W-014 cites search input label absence; W-015b cites CSS line 148 with exact rgba value. Lower-severity findings (W-002a, W-016) cite specific page locations. CANNOT DETERMINE verdicts cite the specific evidence gap (WebFetch HTML attribute extraction limitation; mkdocs.yml inspection result).
- **One gap found:** SC 2.1.4 (`/` key shortcut) is rated as "FAIL (candidate)" but the evidence that this is a global shortcut vs. focus-only shortcut is not confirmed. The deliverable acknowledges this uncertainty but does not explicitly re-examine this SC after the corrections iteration. This is appropriate given the scope of iter-2 corrections (focus on V-001 through V-004).
- **Verdict:** COMPLIANT (minor note on SC 2.1.4 evidence qualification)
- **Quality dimension:** Evidence Quality

**CC-003-RI2 — H-23/H-24 Navigation Table**

- **Principle:** HARD. Documents over 30 lines must include a navigation table with anchor links.
- **Evaluation:** Navigation table present at lines 44-63 of the deliverable with anchor links for all 14 major sections. All entries use markdown link syntax `[Section](#anchor)`. Compliant.
- **Verdict:** COMPLIANT
- **Quality dimension:** Completeness

**CC-004-RI2 — S-014 Scoring Methodology (quality-enforcement.md)**

- **Principle:** MEDIUM. Quality scoring must use the S-014 six-dimension rubric. Conservative calibration after over-scoring is required.
- **Compliance criteria:** Per-dimension breakdown with weights summing to 1.0; anti-leniency discipline applied; residual risks acknowledged.
- **Evaluation:** Self-assessed quality score section uses the correct six dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10 — weights sum to 1.00). Anti-leniency statement is explicit. Conservative calibration penalty of -0.005 applied. Raw composite 0.891 reported before calibration. The reasoning is transparent.
- **Minor concern:** The deliverable reports self-score as 0.91 but the raw composite is 0.891 (calibrated 0.886). Reporting 0.91 as "ceiling" overstates the calibrated value by +0.024. The frontmatter shows `quality_score: 0.91` and `confidence: 0.91`. These should ideally match the calibrated value (0.886). The discrepancy is explained in prose ("Reporting 0.91 as ceiling (conservative)") but this is counterintuitive — a "ceiling" would normally be the upper bound, not the reported value. This is a minor internal consistency issue.
- **Verdict:** SUBSTANTIALLY COMPLIANT (minor self-score ceiling vs. calibrated value labeling inconsistency)
- **Quality dimension:** Internal Consistency, Traceability

### S-007 Summary

| Finding | Severity | Principle | Status |
|---------|----------|-----------|--------|
| CC-001-RI2: All four factual corrections accepted, no new P-022 violations | Minor (residual SC arithmetic gap) | P-001/P-022 | COMPLIANT |
| CC-002-RI2: Evidence citations comprehensive; SC 2.1.4 candidate confidence noted | Minor | P-011 | COMPLIANT |
| CC-003-RI2: Navigation table present with anchor links | Pass | H-23/H-24 | COMPLIANT |
| CC-004-RI2: Self-score 0.91 reported vs. calibrated 0.886; labeling inconsistency | Minor | quality-enforcement.md | SUBSTANTIALLY COMPLIANT |

**S-007 verdict:** No Critical or Major constitutional violations in rescope-iter-2. All four iter-1 Critical findings have been remediated by corrections. Residual issues are Minor severity.

---

## S-002: Devil's Advocate

### Core Claims Under Challenge

**Claim 1: The W-001 finding (bold steps in Install from GitHub) is a real accessibility failure.**

*Counter-argument:* Section headings vs. bold text is a genuine distinction for AT users, but the INSTALLATION.md `## Install from GitHub` section is also immediately preceded by a table that explains the four steps in linear sequence. A screen reader user who navigates to this section would encounter the table first, then the step-by-step content. The navigation barrier is real but the impact may be partially mitigated by the table structure. The finding is valid, but severity 3 (major barrier) may slightly overstate the impact for users who access the installation page via the table's in-page links.

*Assessment:* Counter-argument is plausible but does not negate the finding. AT heading navigation (H-key in JAWS/NVDA) operates independently of table structure — users navigating by heading would still miss bold-text steps. Sev-3 rating is defensible. Finding stands.

**Claim 2: W-010 (lang attribute CANNOT DETERMINE) warrants Priority 1 remediation at Sev-3.**

*Counter-argument:* Material for MkDocs is a widely-deployed, well-maintained open source project. Its default behavior for English-language sites is extremely likely to emit `lang="en"` even without explicit `language:` configuration — this is consistent with Material v8+ and v9+ behavior. Treating an extremely likely PASS as a high-priority finding inflates remediation urgency.

*Assessment:* The deliverable correctly responds to this risk by (a) classifying as CANNOT DETERMINE (not FAIL), and (b) noting the fix is 5 minutes. The Priority 1 ranking is appropriate precisely because the fix cost is negligible relative to the potential impact. Even if Material defaults to English, the explicit `language:` declaration is best practice. The counter-argument does not outweigh the remediation priority.

**Claim 3: W-015b (dark mode link underline) is a legitimate SC 1.4.11 concern.**

*Counter-argument:* The CSS file itself contains a comment acknowledging the low contrast: `/* Link underlines — color alone insufficient at ~2.1:1 contrast (WCAG 3:1) */`. This suggests the original developer was aware of the contrast limitation but made a deliberate design choice. The link text itself passes at ~7.2:1, and link underlines have traditionally been treated as non-text contrast elements only since WCAG 2.1 SC 1.4.11. Many practitioners consider underline presence sufficient without contrast requirements, and some AT configurations suppress underlines entirely.

*Assessment:* The CSS comment does acknowledge the contrast limitation, making W-015b a known issue rather than a missed finding. The deliverable correctly rates this as LIKELY FAIL [MEDIUM confidence] and notes it requires browser measurement. The finding stands as a legitimate SC 1.4.11 concern, but the "LIKELY FAIL" framing (rather than "FAIL") is appropriate given the measurement uncertainty.

**Claim 4: The overall POUR rollup (P=FAIL, O=FAIL, U=CANNOT DETERMINE, R=FAIL) is calibrated correctly.**

*Counter-argument:* Operable is marked FAIL primarily based on SC 2.4.2 (duplicate H1/home title) and SC 2.4.6 (conditional on W-001 bold steps). SC 2.4.6 failing conditionally on W-001 means fixing W-001 also closes SC 2.4.6. SC 2.4.2 is the home page title only. The characterization of the "Dominant Failures" for Operable includes SC 2.4.6 which is a derived finding, not a standalone one.

*Assessment:* The POUR rollup is accurate per the definition stated ("FAIL if any evaluated SC at that principle fails"). Operable fails because SC 2.4.2 fails regardless of W-001 fix. The POUR presentation is valid.

**Claim 5: The pilcrow (¶) anchor `title="Permanent link"` attribute is insufficient as an accessible name.**

*Counter-argument:* Some screen readers do expose the `title` attribute to users in certain modes. JAWS with certain verbosity settings announces `title` attributes on links. The finding may slightly overstate universal AT behavior.

*Assessment:* The deliverable correctly notes this nuance in the iter-1 review context (V-005 from rescope-iter-1 noted the `title` attribute). Rescope-iter-2 does not revisit this nuance in the body text, though it remains accurate that `title` alone is not the accessible name computation source (aria-label > aria-labelledby > text content > title per WCAG). The finding is correct; the `title` attribute caveat from iter-1 could be added to W-013 for completeness but is not a factual error.

### S-002 Summary

No core claims are overturned by Devil's Advocate. Counter-arguments identify one enhancement opportunity:

| Finding | Severity | Description |
|---------|----------|-------------|
| DA-001-RI2: W-013 `title="Permanent link"` attribute not noted in body text | Minor | Omission of nuance identified in iter-1 verification; not materially harmful |

---

## S-004: Pre-Mortem Analysis

*Prospective scenario: This review PASSES the deliverable and the WCAG audit is accepted. What could go wrong?*

**PM-001-RI2: W-001 Remediation Applied to Wrong Section (Residual Risk)**

*Scenario:* A developer reads W-001 and fixes bold steps, but applies the fix to `## Local Clone` (which already uses H3) rather than `## Install from GitHub` (which needs the fix). Result: no actual improvement, W-001 persists.

*Probability:* Low. The deliverable now explicitly cites the section name and line numbers (lines 79, 95, 107, 125, `## Install from GitHub`).

*Likelihood of detection:* High — any testing would reveal the bold patterns remain.

*Assessment:* Low residual risk due to explicit evidence citations. Acceptable.

**PM-002-RI2: SC 3.1.1 Lang Attribute May Already Be Present**

*Scenario:* Developer adds `language: en` to mkdocs.yml, WebFetch still shows same behavior. Developer concludes the priority is real. But Material for MkDocs was already emitting `lang="en"` by default — the developer spent 5 minutes on a non-fix.

*Probability:* Moderate (Material v9 likely defaults English). The deliverable explicitly acknowledges this: "Some Material versions default to English and emit `lang="en"` even without explicit configuration."

*Likelihood of harm:* None — adding explicit `language: en` is harmless regardless.

*Assessment:* Not a risk — fix cost is trivial and result is better regardless of current state. ACCEPTABLE.

**PM-003-RI2: W-015b Miscommunicated as Confirmed FAIL**

*Scenario:* A reader skims W-015b and treats it as a confirmed FAIL, adds it to a compliance report claiming SC 1.4.11 failure. This misrepresents the site's actual measured state.

*Probability:* Low — W-015b is clearly labeled "LIKELY FAIL [MEDIUM confidence] — requires browser measurement."

*Assessment:* Low risk due to explicit scoping language. Acceptable.

**PM-004-RI2: SC Count Arithmetic Discrepancy (32 vs. 31)**

*Scenario:* The SC count discrepancy (frontmatter says 32 in-scope; per-SC table yields 31) causes confusion in downstream synthesis. A scoring agent or human reviewer uses the wrong denominator for coverage calculations.

*Evidence:* The deliverable acknowledges this: "The difference (32 vs. 31) is a minor arithmetic discrepancy that does not affect individual findings."

*Assessment:* The discrepancy is real and unresolved. It does not affect finding quality but reduces Completeness and Traceability confidence. A third reviewer would note this.

**Recommendation (PM-004):** The SC count should be reconciled in this deliverable before final acceptance. A recount of the per-SC table: Perceivable (1.1.1, 1.3.1, 1.3.2, 1.3.3, 1.3.4, 1.3.5, 1.4.1, 1.4.3, 1.4.4, 1.4.5, 1.4.10, 1.4.11, 1.4.12, 1.4.13 = 14 evaluated + 5 N/A = 19 total addressed); Operable (2.1.1, 2.1.2, 2.1.4, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.4.5, 2.4.6, 2.4.7, 2.4.11, 2.5.1, 2.5.2, 2.5.3, 2.5.4, 2.5.7, 2.5.8 = 17 addressed); Understandable (3.1.1, 3.1.2, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.6, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7, 3.3.8 = 13 addressed); Robust (4.1.1, 4.1.2, 4.1.3 = 3). Total addressed: ~52 (many are N/A). In-scope (excluding N/A and AAA): the deliverable's count methodology is not fully transparent. This is a documentation gap, not a finding gap.

---

## S-012: FMEA

### Component-Level Failure Mode Analysis

| Component | Failure Mode | Severity (1-5) | Occurrence (1-5) | Detectability (1-5) | RPN | Status |
|-----------|-------------|----------------|------------------|---------------------|-----|--------|
| V-001 correction (W-001 section) | Section name cited correctly but line numbers slightly off if file changed | 2 | 2 | 1 | 4 | ACCEPTABLE — Grep confirmed exact lines at time of evaluation |
| V-002 removal (W-002 false positive) | Future reviewers question why W-002 was removed without seeing full evidence trail | 2 | 2 | 2 | 8 | ACCEPTABLE — Evidence Verification Protocol documents removal with source citation |
| V-003 downgrade (W-010 CANNOT DETERMINE) | Downstream synthesis agent treats CANNOT DETERMINE as PASS rather than elevated risk | 3 | 2 | 3 | 18 | MEDIUM RISK — Deliverable clearly labels "elevated risk" but structured handoff data marks severity 3 which should prevent misclassification |
| V-004 correction (W-015 CSS) | Dark mode footer (`--md-footer-bg-color: #0D0818`) not computed; only light mode verified | 2 | 3 | 2 | 12 | ACCEPTABLE — Dark mode footer uses #0D0818 bg with rgba(255,255,255,.87) fg which yields ~20:1 — clear PASS |
| W-015b (dark mode underline) | Ratio estimate (1.7:1 vs. computed 2.36:1) could cause confusion | 2 | 2 | 2 | 8 | ACCEPTABLE — Both values below 3:1; discrepancy minor |
| SC count arithmetic (32 vs. 31) | Coverage completeness claim in frontmatter inaccurate | 2 | 1 | 3 | 6 | MINOR — Noted but does not affect finding validity |
| POUR rollup calculation | Understandable CANNOT DETERMINE may be read as pass signal | 3 | 1 | 2 | 6 | ACCEPTABLE — POUR table header explicitly notes CANNOT DETERMINE |
| Evidence Verification Protocol section | Scope-gap acknowledgment may invite criticism of entire audit scope | 1 | 1 | 1 | 1 | ACCEPTABLE — Transparency is a quality indicator |

**Highest RPN item:** V-003 downgrade (RPN 18) — the CANNOT DETERMINE verdict for SC 3.1.1 carries the most risk of misinterpretation. The deliverable mitigates this by retaining Sev-3 and Priority 1 remediation rank.

**FM-001-RI2: Dark mode footer not independently computed**

The light mode footer correction (V-004) is confirmed. The dark mode footer uses `--md-footer-bg-color: #0D0818` with the same `rgba(255,255,255,.87)` foreground. L(#0D0818) ≈ 0.002. Contrast with rgba(255,255,255,.87) ≈ effective #E4E1F1 (L≈0.767). Ratio ≈ (0.817)/(0.052) ≈ 15.7:1. Dark mode footer also PASSES. No finding gap here.

---

## S-013: Inversion

*What would make this deliverable a BAD accessibility audit?*

**IN-001-RI2: Single-Method Evidence — WebFetch Without AT Testing**

*Inverted assumption:* The deliverable assumes WebFetch + source file inspection is adequate evidence for a WCAG AA audit.

*Challenge:* WCAG conformance requires actual AT testing (NVDA, JAWS, VoiceOver) for most SC verdicts. A finding like SC 2.4.1 PASS (skip links confirmed by WebFetch) is valid. But SC 4.1.2 FAIL (search label not confirmed via WebFetch) may be incorrect — Material for MkDocs is known to inject `aria-label="Search"` on search inputs. A user with NVDA would likely not encounter an unlabeled search field.

*Assessment:* The deliverable consistently flags this limitation: "NOT A CONFORMANCE DETERMINATION" header; WebFetch cannot replicate AT-based testing; Acknowledged evaluation limitation (P-022) section. The limitation acknowledgment is thorough. The inversion challenge does not negate the findings but confirms the audit is a preliminary assessment, not a full conformance evaluation. This is appropriate given the tooling constraints.

**IN-002-RI2: W-001 Section Is the Primary Install Path — Does This Matter for Accessibility?**

*Inverted assumption:* The W-001 bold-step pattern in `## Install from GitHub` is the primary path and a screen reader barrier.

*Challenge:* Looking at the installation table (lines 56-61), the `## Install from GitHub` section covers both SSH and HTTPS users — that is "Internet access + SSH key" and "Internet access, no SSH key." The table says both take "~2 minutes." The `## Local Clone` section is for offline/restricted users. For screen reader users who may also have motor disabilities (a common co-occurrence), the Install from GitHub path is the primary path. W-001 correctly targets the most-used section.

*Assessment:* Inversion confirms the finding's priority is correct.

**IN-003-RI2: Pilcrow Accessibility — Is the Finding Overclaimed?**

*Inverted assumption:* Pilcrow anchors are a navigation noise problem for screen readers (W-013).

*Challenge:* Modern screen readers (JAWS 2024, NVDA 2023+) often suppress pilcrow/permalink anchors from their link lists when styled with CSS `display: none` or `visibility: hidden` on focus-away. If Material for MkDocs uses CSS to hide pilcrow anchors until heading hover, they may not appear in AT link lists at all.

*Assessment:* The deliverable rates this as "MEDIUM confidence — pilcrow anchors are a common pattern whose AT impact varies by screen reader behavior." This is appropriately hedged. WebFetch confirmed their presence in the DOM, but display behavior on non-hover states is unknown. The finding is valid as a candidate concern; the "MEDIUM confidence" mitigates overclaiming.

**IN-004-RI2: Logo Alt="logo" — Is This Actually a Failure?**

*Inverted assumption:* `alt="logo"` fails SC 1.1.1.

*Challenge:* The logo links to the home page. The link's accessible name is computed from the alt text of the contained image. An accessible name of "logo" provides some information (it's a logo, not content). The image is contained in a link with `title="Jerry Framework"`. Some AT implementations would announce "Jerry Framework" (the title) rather than "logo" (the alt text) when voicing a linked image — particularly if the `title` attribute takes precedence.

*Assessment:* Per WCAG accessible name computation (SVG/img in anchor: alt text overrides title for accessible name calculation), `alt="logo"` would be the accessible name "logo" for most AT implementations. The finding stands. The title attribute provides a tooltip but not the AT-announced name. W-011 is correct.

---

## S-014: LLM-as-Judge

### Scoring Summary

**Anti-leniency discipline applied:** Prior iter-1 scored 0.807 vs. self-claim 0.935 — a 0.128 gap. The primary dimension failures were Internal Consistency (0.76) and Evidence Quality (0.70). This iteration verifies those specific failures were corrected. Independent source verification confirms all four corrections are accurate. Scoring should reflect genuine improvement while accounting for residual gaps.

### Per-Dimension Assessment

**Completeness (Weight: 0.20)**

*What full completeness looks like:* All WCAG 2.2 A/AA SCs evaluated or explicitly excluded (N/A). All 8 surfaces addressed. Persona Spectrum coverage complete. Findings complete across all applicable sections.

*Assessment:* All 32 (or 31) in-scope SCs are addressed with explicit verdicts. N/A and out-of-scope SCs are documented. All 8 surfaces evaluated. Five Persona Spectrum patterns complete. W-015b is a new finding (added this iteration) demonstrating active audit quality improvement. The SC count arithmetic gap (32 vs. 31) is a documented residual. The Synthesis Judgments section and Handoff Data are complete and updated.

*Score:* 0.90 — Full SC coverage with methodologically consistent N/A handling. Minor deduction for unresolved SC count discrepancy and uncounted dark mode contrast elements.

*Weighted:* 0.180

**Internal Consistency (Weight: 0.20)**

*What full internal consistency looks like:* POUR rollup matches per-SC verdicts. Remediation priorities match finding severities. Cross-references between sections (Summary, per-SC table, Remediation Priorities, Handoff Data, XP-05) are aligned.

*Assessment:* This was the weakest dimension in iter-1 (0.76). Specific improvements in iter-2:
- W-002 removal propagated to: Critical Findings Summary (W-015 relabeled N/A), SC 2.4.4 section corrected to PASS, Legal Compliance section updated, Persona Spectrum updated, XP-05 updated, Handoff Data updated, Synthesis Judgments updated.
- W-001 section correction propagated to: Critical Findings Summary, SC 1.3.1 section, SC 2.4.6 section, Remediation Priorities, Persona Spectrum Scenario 2, XP-05, Handoff Data.
- POUR Understandable updated from FAIL to CANNOT DETERMINE.
- Self-score section explains all corrections.

*One residual inconsistency:* The SC 2.5.3 (Label in Name) section and SC 3.3.2 (Labels or Instructions) both cite W-014 (search input no aria-label). Both fail. These two SC verdicts create a situation where W-014 contributes to two separate SC failures in two different POUR principles (Operable and Understandable). This is consistent and not an error — the same underlying issue affects both SCs. However, the POUR rollup for Understandable is already marked CANNOT DETERMINE (due to SC 3.1.1), and SC 3.3.2 is also a FAIL. The Understandable POUR should therefore be FAIL (not CANNOT DETERMINE) based on SC 3.3.2 alone — the SC 3.3.2 failure independently triggers a FAIL regardless of SC 3.1.1.

*This is a genuine internal inconsistency:* The POUR Understandable is labeled CANNOT DETERMINE with "dominant failures: SC 3.1.1 (lang attribute not confirmed)" — but SC 3.3.2 (search input label) and SC 2.5.3 (Label in Name) in Operable are both FAIL (candidate). SC 3.3.2 is in the Understandable principle. A FAIL in SC 3.3.2 would make Understandable = FAIL, not CANNOT DETERMINE.

*Score:* 0.87 — Strong improvement over 0.76 but the Understandable POUR rollup inconsistency (CANNOT DETERMINE when SC 3.3.2 is FAIL candidate) is a new Minor/Major consistency gap.

*Weighted:* 0.174

**Methodological Rigor (Weight: 0.20)**

*What full methodological rigor looks like:* WCAG-EM 1.0 procedure followed. Verdicts based on appropriate evidence type. Confidence levels calibrated to evidence quality. Acknowledged limitations consistent with method.

*Assessment:* Evidence Verification Protocol section is a genuine methodological improvement — it documents the verification gap from iter-1 (CSS not read, section names not verified) and corrects it. All CANNOT DETERMINE verdicts now include specific reasons why determination is impossible (WebFetch cannot extract `<html>` attributes; browser DevTools required for focus ring contrast). Contrast computations cite specific CSS values with luminance formula application. MEDIUM confidence for estimated elements is consistent. P-022 acknowledgment statement is present and specific.

*One methodological gap:* SC 2.5.3 (Label in Name) is rated "FAIL (candidate)" with evidence that `alt="logo"` does not contain the visible text label. The "candidate" qualification is appropriate but SC 2.5.3 specifically requires the accessible name to CONTAIN the visible label. If the visible label is considered to be the logo image (which is purely graphical with no associated visible text label), SC 2.5.3 might not apply. The deliverable conflates SC 1.1.1 (logo alt) with SC 2.5.3 (visible label in accessible name) — the SC 2.5.3 analysis for the logo would require identifying what the "visible label" is for a graphical link.

*Score:* 0.88 — Strong source verification methodology demonstrated. Minor deduction for SC 2.5.3 method application.

*Weighted:* 0.176

**Evidence Quality (Weight: 0.15)**

*What full evidence quality looks like:* Claims backed by direct source observation (not inference). Confidence levels distinguish observed from inferred. Evidence is specific enough to reproduce independently.

*Assessment:* This was the weakest dimension in iter-1 (0.70). Specific improvements:
- W-001: Lines 79, 95, 107, 125 cited with step names from actual Grep; section confirmed as `## Install from GitHub`.
- W-015 footer: Exact CSS values (#311B92, rgba(255,255,255,.87)) from lines 42-47; WCAG luminance computation shown.
- W-002 removal: Line 678 prose text quoted; WebFetch live confirmation.
- W-010: mkdocs.yml Grep result documented; behavior gap acknowledged.

*Evidence quality for Sev-2+ findings is now substantially above iter-1 level.* Dark mode elements remain estimated with MEDIUM confidence — this is an appropriate qualification.

*One gap:* W-015b ratio estimate. The deliverable states ~1.7:1. Independent WCAG luminance computation yields ~2.36:1 (lower bound; depends on exact alpha blending computation method). Both values are below the 3:1 threshold — the qualitative finding is identical — but the quantitative claim differs by ~0.7:1. This is a minor evidence quality gap. The deliverable's acknowledgment that "browser measurement required" adequately hedges the estimate.

*Score:* 0.88 — Substantial improvement from 0.70. High-confidence evidence for all Sev-3 and most Sev-2 findings. Residual deduction for W-015b ratio imprecision and dark mode elements estimated.

*Weighted:* 0.132

**Actionability (Weight: 0.15)**

*What full actionability looks like:* Each finding has a specific, implementable remediation. Effort estimates are realistic. Priority ordering reflects combined severity and fix cost. Owner assignments enable triage.

*Assessment:* Remediation Priorities table is comprehensive (13 items), ordered by priority, with effort estimates and ownership classification. The theme-level vs. content-level fix table is a strong actionability aid. All V-001 through V-004 corrections update the relevant remediation entries (W-001 priority now points to lines 79-125 Install from GitHub; W-015 PASS confirmed; W-002a replaces W-002). Inclusive Design Adoption Roadmap provides a phased implementation sequence.

*Potential concern:* W-015b (dark mode underline) is listed as Priority 10 with "verify with browser measurement" — the pre-measurement step is appropriate, but the recommended fix ("Increase underline opacity or use higher-contrast underline color") is vague. A developer fixing this would need specific CSS guidance. The current saucer-boy.css line 148 value could be increased to `rgba(179,157,219,1.0)` (full opacity) which would yield the link color (#B39DDB ≈ L 0.432) on #1A1025 (L 0.008) = (0.482/0.058) ≈ 8.3:1. This specific suggestion would improve actionability.

*Score:* 0.90 — Strong remediation structure. Minor deduction for W-015b fix vagueness.

*Weighted:* 0.135

**Traceability (Weight: 0.10)**

*What full traceability looks like:* Each correction traceable to the error that prompted it (V-001 through V-004). Finding IDs consistent across all sections. Revision history table complete.

*Assessment:* Revision History and Rescope section includes the correction summary table (V-001 through V-004) with pre-correction and post-correction states. Evidence Verification Protocol section provides explicit verification method per claim. Synthesis Judgments table includes correction notes. Handoff Data, XP-05, and the Critical Findings Summary table all document the W-002 removal. The frontmatter revision log documents both rescope iterations.

*One traceability gap:* W-015 in the Critical Findings Summary is listed as a table row with status "REMOVED as failure" and severity "N/A" — this is clear. But in the per-SC Color Contrast Analysis section (lines 563-583), the W-015 correction is documented inline. The cross-reference between the finding-level documentation and the SC-level documentation is present but requires a reader to traverse multiple sections. This is a minor navigation friction, not a traceability failure.

*SC count discrepancy noted:* The frontmatter states `scs_in_scope: 32` which does not match the per-SC table enumeration of ~31. This is acknowledged in the deliverable. The discrepancy is a Traceability deduction.

*Score:* 0.88 — All correction traces documented. Minor deduction for SC count discrepancy and W-015b not in frontmatter findings list.

*Weighted:* 0.088

### S-014 Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.90 | 0.180 |
| Internal Consistency | 0.20 | 0.87 | 0.174 |
| Methodological Rigor | 0.20 | 0.88 | 0.176 |
| Evidence Quality | 0.15 | 0.88 | 0.132 |
| Actionability | 0.15 | 0.90 | 0.135 |
| Traceability | 0.10 | 0.88 | 0.088 |
| **COMPOSITE** | **1.00** | — | **0.885** |

**Threshold:** 0.92

**Note on Internal Consistency finding (CC-005-RI2):** The Understandable POUR rollup is labeled CANNOT DETERMINE but SC 3.3.2 (Labels or Instructions) is a FAIL candidate in the Understandable principle. A FAIL in any evaluated SC makes the POUR principle FAIL (per the deliverable's own conformance note at line 151). This is a genuine internal inconsistency that was NOT present in the correction scope of V-001 through V-004 — it is a new finding in this review. However, this inconsistency is Minor severity (it does not affect individual SC verdicts or remediation priorities, only the rollup label for a single POUR row), and changing the label from CANNOT DETERMINE to FAIL would not alter the overall audit conclusion (the site has multiple failures across all four principles).

---

## Consolidated Findings Summary

| ID | Strategy | Severity | Finding | Section |
|----|----------|----------|---------|---------|
| CC-001-RI2 | S-007 | Minor | SC arithmetic discrepancy (32 vs. 31) acknowledged but unresolved | Frontmatter + SC Count Note |
| CC-004-RI2 | S-007 | Minor | Self-score 0.91 reported; calibrated value is 0.886; "ceiling" label is counterintuitive | Self-Assessed Quality Score |
| CC-005-RI2 | S-014 | Minor | Understandable POUR labeled CANNOT DETERMINE but SC 3.3.2 is FAIL candidate — rollup should be FAIL | POUR Status table |
| DA-001-RI2 | S-002 | Minor | W-013 pilcrow `title="Permanent link"` attribute not noted in body text (was in iter-1 verification) | SC 4.1.1 + Screen Reader section |
| PM-004-RI2 | S-004 | Minor | SC count arithmetic unresolved; downstream synthesis agents could use wrong coverage denominator | Frontmatter + SC Count Note |
| FM-001-RI2 | S-012 | Minor | W-010 CANNOT DETERMINE risk of misinterpretation as PASS in structured data context; Sev-3 and Priority-1 mitigate | POUR table + Handoff Data |
| IN-001-RI2 | S-013 | Minor | Single-method limitation (WebFetch) appropriately hedged; Material search label likely present but not confirmed | SC 4.1.2, SC 3.3.2 |
| W-015b-RI2 | Verification | Minor | Ratio estimate ~1.7:1 vs. computed ~2.36:1; both below 3:1; directional finding correct | Color Contrast Analysis |

**Critical findings this iteration:** 0
**Major findings this iteration:** 0
**Minor findings this iteration:** 8

All four iter-1 Critical findings (V-001 through V-004) are confirmed corrected. No new Critical or Major findings introduced.

---

## Verdict

**COMPOSITE SCORE: 0.885**

**THRESHOLD: 0.92**

**VERDICT: REVISE**

**Band:** 0.885 falls in the 0.85–0.91 REVISE band (below threshold, near-threshold, targeted revision likely sufficient).

### Gap Analysis

The 0.885 composite is 0.035 below the 0.92 threshold. The primary limiting dimension is Internal Consistency (0.87) due to:
1. **CC-005-RI2 (primary):** Understandable POUR rollup labeled CANNOT DETERMINE but SC 3.3.2 is a FAIL candidate — the rollup should be FAIL based on the deliverable's own POUR computation rule. This is a one-line fix.
2. **CC-001-RI2 (secondary):** SC count arithmetic (32 vs. 31) is unresolved.

### Iter-3 Scope (Editorial — No Source Reverification Required)

The following corrections are sufficient to close the REVISE gap. All are editorial (no new source reads required):

| Item | Action | Dimension Impact |
|------|--------|-----------------|
| POUR Understandable | Change from CANNOT DETERMINE to FAIL; update "Dominant Failures" to include SC 3.3.2 (search label) | Internal Consistency +0.02 |
| SC count arithmetic | Recount per-SC table; reconcile with frontmatter `scs_in_scope:` value | Internal Consistency +0.01, Traceability +0.01 |
| Self-score labeling | In Self-Assessed Quality Score section, change "Reporting 0.91 as ceiling" to either report 0.886 (calibrated) or clarify that 0.91 is an upper-bound estimate | Internal Consistency +0.01 |
| W-013 `title` attribute note | Add one sentence noting `title="Permanent link"` is present but insufficient as accessible name | Completeness +0.005 |
| W-015b actionability | Replace vague "increase opacity" with specific CSS value: `rgba(179,157,219,1.0)` for full-opacity link underline | Actionability +0.01 |

**Estimated composite after iter-3 editorial corrections:** 0.885 + (0.02 + 0.02 + 0.01) ≈ 0.92–0.925

These are low-effort editorial corrections. No new source reads, no WebFetch calls, no evidence recollection required.

### Verification Acknowledgment

All mandatory source verifications completed:
- INSTALLATION.md:678 prose confirmed — W-002 false positive removal CORRECT
- INSTALLATION.md lines 79, 95, 107, 125 bold patterns confirmed — W-001 correction CORRECT
- saucer-boy.css footer values confirmed — W-015 correction CORRECT
- mkdocs.yml no `language:` key confirmed — W-010 CANNOT DETERMINE CORRECT
- W-015b dark mode underline CONFIRMED from CSS; ratio refined but directionally correct
- POUR rollup Understandable CANNOT DETERMINE: NEW INCONSISTENCY found (SC 3.3.2 FAIL candidate in Understandable)

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 0
- **Major:** 0
- **Minor:** 8
- **Protocol Steps Completed:** 6 of 6 (S-007, S-002, S-004, S-012, S-013, S-014)
- **Source Verifications Completed:** 7 (INSTALLATION.md prose, INSTALLATION.md bold patterns, saucer-boy.css footer, mkdocs.yml language, saucer-boy.css dark mode, live site logo alt × 2)

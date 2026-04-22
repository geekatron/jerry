# Adversarial Review: FEAT-040-005 — Rescope Iteration 1 (C3 Multi-Strategy)

## Execution Context

| Field | Value |
|-------|-------|
| **Feature ID** | FEAT-040-005 |
| **Deliverable** | `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-005/ux-inclusive-evaluator-output.md` |
| **Review Type** | C3 Adversarial Review — Rescope Evaluation (Fresh, not iteration 7) |
| **Criticality** | C3 |
| **Quality Threshold** | 0.92 |
| **Iteration** | rescope_1 |
| **Agent Self-Score** | 0.935 |
| **Reviewer Computed Score** | See S-014 below |
| **Strategies Executed** | S-007, S-002, S-004, S-012, S-013, S-014 |
| **Live-Site Verification** | WebFetch + mkdocs.yml + source file Grep used for independent spot-checks |
| **Executed** | 2026-04-20 |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Live-Site Verification Report](#live-site-verification-report) | Independent WebFetch + source checks against claimed evidence |
| [S-007: Constitutional AI Critique](#s-007-constitutional-ai-critique) | HARD rule compliance check |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-arguments against core claims |
| [S-004: Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Prospective failure enumeration |
| [S-012: FMEA](#s-012-fmea) | Component-level failure mode analysis |
| [S-013: Inversion](#s-013-inversion) | Assumption stress-testing |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Weighted composite score |
| [Consolidated Findings Summary](#consolidated-findings-summary) | All findings by severity |
| [Verdict](#verdict) | PASS / REVISE / ESCALATE with iter-2 scope if needed |

---

## Live-Site Verification Report

Independent verification was performed via WebFetch against https://jerry.geekatron.org/, direct inspection of `mkdocs.yml`, direct source Grep of `docs/INSTALLATION.md`, and inspection of `docs/stylesheets/saucer-boy.css`. This section documents confirmed, disputed, and nuanced findings.

### V-001: W-001 Bold Step Labels — PARTIALLY CONTRADICTED (Critical)

**Deliverable claims (W-001, Sev 3):** "INSTALLATION.md rendered page: step labels 'Step 1: Clone the repository,' 'Step 2: Add as a local plugin source,' 'Step 3: Verify and install' are formatted as bold text (`<strong>`) rather than semantic headings (`<h3>`)." Rated as Severity 3 (Major barrier), Priority 2 remediation.

**Independent verification:**

Source Grep of `docs/INSTALLATION.md` reveals two distinct install paths:

- **Install from GitHub section** (lines 235, 253, 265): Uses `### Step 1: Clone the repository`, `### Step 2: Add as a local plugin source`, `### Step 3: Verify and install` — these are H3 markdown headings, rendered as `<h3>` elements on the live site.

- **Session Install section** (lines 79, 95, 107, 125): Uses `**Step 1: Add the Jerry repository as a plugin source**`, `**Step 2: Verify the source registered**`, `**Step 3: Install the plugin**`, `**Step 4: Confirm it landed**` — these ARE bold/strong patterns without H3 wrapper.

WebFetch heading hierarchy audit of the live installation page confirms H3s at "Step 1: Clone the repository," "Step 2: Add as a local plugin source," "Step 3: Verify and install" in the Install from GitHub section.

**Assessment:** W-001 as stated is **partially incorrect**. The specific step labels cited by the deliverable ("Step 1: Clone the repository," etc.) are H3 headings in the "Install from GitHub" section, not bold/strong. However, W-001 is **partially valid**: the "Session Install" section (the primary recommended path for most users) does use bold-text step labels (`**Step N:**`) without H3 structure. The deliverable cited the wrong section as the source of the failing pattern, but a real W-001 failure exists in the Session Install path.

**Impact:** The finding is real but misattributed. The evidence for W-001 must be corrected to reference Session Install bold labels, not Install from GitHub H3 headers. As stated in the deliverable, the finding evidence is factually wrong for the cited section.

**Severity of error:** MEDIUM — the finding exists but the cited evidence is wrong. The Priority 2 remediation recommendation remains valid but applies to a different section of the page.

---

### V-002: W-002 Non-Descriptive Link Text "file it" / "file that too" — CONTRADICTED (Critical)

**Deliverable claims (W-002, Sev 3):** "INSTALLATION.md Getting Help section contains: 'If you run into a problem, file it. If you find a documentation error, file that too.' Links 'file it' and 'file that too' (both href: `https://github.com/geekatron/jerry/issues`) do not describe the link destination." Rated Severity 3, Priority 3 remediation.

**Independent verification:**

Source Grep of `docs/INSTALLATION.md` line 678: `If something's broken, file it. If something's confusing, file that too.`

Lines 680-681 show the actual hyperlinks:
- `**GitHub Issues:** [github.com/geekatron/jerry/issues](https://github.com/geekatron/jerry/issues)` — descriptive link text
- `**Documentation:** [jerry.geekatron.org](https://jerry.geekatron.org)` — URL as link text

WebFetch of the live installation page confirms: "file it" and "file that too" are plain prose text. They are **not hyperlinks**. The actual links in the Getting Help section use "github.com/geekatron/jerry/issues" as link text — which is a URL-as-text pattern (separate concern), not non-descriptive embedded prose.

**Assessment:** W-002 as stated is **false**. "file it" and "file that too" are not hyperlinks on the live site or in the source. The SC 2.4.4 failure does not exist as described. There may be a different non-descriptive link concern (URL-as-text for github.com domain), but that is a distinct finding at lower severity than described.

**Severity of error:** HIGH. W-002 is rated Sev-3 (Major barrier) and Priority 3 remediation. This is a top-3 finding that does not exist as stated. This directly parallels the F-012 factual error found in FEAT-040-004 rescope review.

---

### V-003: W-010 lang Attribute Not Confirmed — VALID BUT OVERCONFIDENT (Medium)

**Deliverable claims (W-010, Sev 3):** "The `lang` attribute value on the `<html>` element was NOT confirmed across any of the 8 evaluated surfaces." Rated as "FAIL" for SC 3.1.1.

**mkdocs.yml verification:** The `mkdocs.yml` at project root does NOT include a `language:` key under the `theme:` section. Material for MkDocs uses `theme.language` to set `lang` on the `<html>` element. Absence of this config key typically causes Material to default to English without emitting `lang="en"` in the generated HTML, or to default to `en` depending on the version.

**Assessment:** The W-010 concern is **plausible and supported by mkdocs.yml evidence** (no `language:` configured). However, the deliverable's FAIL verdict requires correction: absent `language:` in mkdocs.yml may or may not produce `<html lang="en">` depending on the MkDocs Material version. The deliverable should be CANNOT DETERMINE (with strong suspicion), not a definitive FAIL, unless browser DevTools confirmation has been obtained. The self-labeled "MEDIUM confidence" is appropriate, but the verdict of "FAIL" overstates the certainty.

**Net assessment:** W-010 finding is directionally correct and the remediation recommendation is appropriate. The FAIL verdict is slightly overconfident given acknowledged WebFetch limitation; CANNOT DETERMINE (elevated risk) would be more accurate to the evidence. This is a calibration issue, not a fabricated finding.

---

### V-004: Theme Described as "Standard Material" — CONTRADICTED

**Deliverable claims (Audit Scope section):** "Standard MkDocs Material theme with no apparent custom color overrides documented."

**Actual state:** `mkdocs.yml` defines two custom color schemes (`saucer-boy` and `saucer-boy-dark`) and loads `extra_css: - stylesheets/saucer-boy.css`. Inspection of `docs/stylesheets/saucer-boy.css` reveals extensive custom CSS variable overrides:
- Primary: `#512DA8` (deep purple), not Material default indigo
- Accent: `#FFB300` (amber)
- Footer: `#311B92` background with `rgba(255,255,255,.87)` text — dark purple, NOT the light gray footer the deliverable assumed

**Impact on W-015 (Footer Contrast):** The deliverable claims footer text is "light gray `#90a4ae` on white" yielding ~2.1:1 contrast. This is the Material default slate theme footer. The actual Saucer Boy theme uses **white text on dark purple footer**, which yields approximately 8.1:1 — a PASS. W-015 as characterized is **incorrect**; the footer contrast concern exists but the specific values cited are wrong.

**Impact on contrast analysis overall:** The contrast analysis table (SC 1.4.3) carries "LIKELY PASS [MEDIUM]" for body text based on "standard Material default palette." Since the actual theme uses `rgba(0,0,0,.87)` on `#FFFFFF` for light mode body text (confirmed in CSS), the body text estimate is correct. However, the code block colors (`--md-code-bg-color: #F5F2F9`, `--md-code-fg-color: #37474F`) are now verifiable — not estimated. The deliverable's "estimated" framing understates the certainty level for elements where CSS values are directly available.

**Assessment:** This is a MEDIUM error. The scope claim is wrong (theme is heavily customized), affecting the credibility of the contrast analysis section. The methodological acknowledgment ("WebFetch cannot extract computed CSS") is correct, but the deliverable should have read the source CSS file — which is accessible in the repository. Reading mkdocs.yml and saucer-boy.css was within the audit scope for a live-site evaluation.

---

### V-005: W-013 Pilcrow Anchor Links — CONFIRMED PRESENT, title="Permanent link" NOT NOTED

**Deliverable claims (W-013, Sev 2):** Pilcrow (¶) anchors present, single-character accessible name, fails SC 4.1.2.

**WebFetch verification:** Confirmed. Pilcrow anchors are present throughout all pages. Example confirmed: `[¶](#getting-started-with-jerry "Permanent link")` — the anchor has a `title="Permanent link"` attribute.

**Assessment:** The `title="Permanent link"` attribute provides a tooltip but does NOT serve as the accessible name for AT purposes (WCAG 2.1.1 — `title` is a supplementary attribute; `aria-label` or visible text is required for accessible name calculation in most AT). W-013 finding is substantially correct, though the note that `title` exists but is insufficient should be included for completeness.

---

### V-006: SC 2.4.1 Skip Link PASS — CONFIRMED

Skip links confirmed on all 8 surfaces with correct target IDs. PASS verdict is correct. [HIGH confidence]

---

### V-007: Logo alt="logo" — CONFIRMED

Logo alt text confirmed as `"logo"` on all evaluated surfaces. W-011 finding is correct. [HIGH confidence]

---

### Verification Summary Table

| Claim | Verdict | Confidence | Impact |
|-------|---------|------------|--------|
| W-001: Install-from-GitHub step labels use strong not h3 | PARTIALLY CONTRADICTED — cited section uses H3; Session Install uses bold | MEDIUM | Priority 2 finding misattributed to wrong section |
| W-002: "file it" / "file that too" are hyperlinks to GitHub Issues | CONTRADICTED — these are plain prose, not hyperlinks | HIGH | Major false positive — Sev-3 finding does not exist as stated |
| W-010: lang attribute absent | PLAUSIBLE (mkdocs.yml lacks language:) but verdict overconfident | MEDIUM | Sev-3 verdict should be CANNOT DETERMINE elevated risk |
| Theme: "standard Material, no custom color overrides" | CONTRADICTED — custom schemes in mkdocs.yml + saucer-boy.css | HIGH | Contrast analysis section miscalibrated |
| W-015: Footer ~2.1:1 light gray on white | CONTRADICTED — actual footer is white on dark purple ~8.1:1 | HIGH | False contrast failure for footer; contrast concern may exist elsewhere |
| W-013: Pilcrow anchors present | CONFIRMED | HIGH | Finding valid; title="Permanent link" exists but insufficient |
| W-011: Logo alt="logo" | CONFIRMED | HIGH | Finding valid |
| SC 2.4.1 skip link PASS | CONFIRMED | HIGH | PASS correct |

---

## S-007: Constitutional AI Critique

**Strategy:** Constitutional AI Critique (S-007)
**Finding Prefix:** CC-

### P-001 (Truth/Accuracy) — VIOLATED

**Principle:** P-001 requires deliverables to be accurate. Findings must be based on actual observed evidence.

**Violation evidence:**
- W-002 claims "file it" and "file that too" are hyperlinks to GitHub Issues. They are not. This is a fabricated finding — plain prose presented as a linked-text accessibility failure.
- W-001 attributes bold-step evidence to the wrong section (Install from GitHub, which uses H3) when the actual bold-step failure is in Session Install.
- W-015 states footer contrast is "~2.1:1 light gray on white" — the actual CSS shows white text on dark purple, a passing ratio.
- Audit Scope claims "Standard MkDocs Material theme with no apparent custom color overrides" — directly contradicted by mkdocs.yml and saucer-boy.css.

**Severity:** Critical (HARD rule P-001 is a governing constraint, evidence fabrication)
**Finding ID:** CC-001

### P-022 (No Deception) — VIOLATED

**Principle:** P-022 requires no deception about capabilities, evidence, or confidence levels.

**Violation evidence:**
- The Synthesis Judgments Summary table states W-002 "HIGH confidence" for "Link text directly observed in INSTALLATION.md rendered Getting Help section." The link text was NOT observed — the prose was observed, but "file it" is not hyperlinked. Claiming HIGH confidence for a finding where the link does not exist is deceptive.
- The self-score rationale states "All FAIL verdicts cite specific observed evidence with URL + element" under Evidence Quality = 0.93. W-002's evidence is not specific observed evidence — the "file it" link does not exist.

**Severity:** Critical (HARD rule P-022)
**Finding ID:** CC-002

### H-15 (Self-Review Before Presentation) — VIOLATED

**Principle:** H-15 requires self-review before presenting deliverables. A rigorous self-review would have verified whether "file it" is actually a hyperlink before claiming HIGH confidence for a Severity-3 finding.

**Violation evidence:** The deliverable claims self-reviewed quality 0.935. A genuine self-review would have prompted re-verification of the Getting Help section link claim, which is verifiable by reading the source file. The actual source (INSTALLATION.md line 678-681) is accessible from the repository. The Session Install bold-label pattern (lines 79-125) is also accessible. Reading the source markdown before claiming evidence was observed is a basic self-review step.

**Severity:** Major (H-15 is Tier B enforced; the self-review was incomplete given available evidence)
**Finding ID:** CC-003

### H-23 (Navigation Table) — COMPLIANT

Navigation table present with anchor links. [PASS]

### Quality-Enforcement.md P-011 (Evidence-Based) — VIOLATED

**Principle:** P-011 requires evidence-based findings. Every finding must include direct evidence from the deliverable.

**Violation:** W-002 cites evidence that does not correspond to observable reality. "file it" is cited as a link element — it is prose text. This is the same failure pattern as F-012 in FEAT-040-004 rescope (finding cited as evidence something that was the opposite of what the live site shows).

**Severity:** Critical (same class as FEAT-040-004 F-012 factual error)
**Finding ID:** CC-004

### S-007 Constitutional Compliance Score

| Violations | Count | Score Penalty |
|-----------|-------|--------------|
| Critical violations (P-001, P-022, P-011) | 3 | -0.30 |
| Major violations (H-15) | 1 | -0.05 |
| Minor violations | 0 | 0.00 |
| **Constitutional compliance base** | | **0.65** |

Constitutional compliance: **BELOW THRESHOLD** (0.65 < 0.92). The 3 Critical violations are not minor calibration issues — one finding (W-002) is a complete fabrication of a hyperlink that does not exist, and the evidence for W-001 is misattributed to the wrong section.

---

## S-002: Devil's Advocate

**Strategy:** Devil's Advocate (S-002)
**Finding Prefix:** DA-

### DA-001: The "Structural Ceiling" Framing May Conceal a Recurrence of the Fabrication Problem

**Counter-argument:** The deliverable frames the rescope as solving a "structural ceiling" caused by evaluating static markdown rather than live site. However, the fabricated W-002 finding and misattributed W-001 finding raise the question: did the evaluator actually perform live-site WebFetch inspection at the claimed depth, or did it confuse content from the source markdown with rendered HTML behavior? The fact that W-001 cites the Install from GitHub section (which is H3 in source) rather than the Session Install section (which is bold in source) suggests the evaluator may have mixed up sections without verifying which section was actually problematic. The "live site" framing does not automatically mean the findings are more accurate than the static markdown analysis.

**Evidence:** Source INSTALLATION.md lines 79-125 (Session Install, bold labels) vs lines 235-265 (Install from GitHub, H3 labels). The deliverable cited the H3 section as having bold labels — the opposite of what the source shows.

**Severity:** Major
**Finding ID:** DA-001

### DA-002: CANNOT DETERMINE Count (9 SCs) Understates Uncertainty About PASS Claims

**Counter-argument:** The deliverable marks 15 SCs as PASS. Several of these are based on Material for MkDocs "expected behavior" rather than direct observation:
- SC 1.3.4 (Orientation): "Material for MkDocs renders responsively... No CSS `orientation: landscape` lock identified" — but the custom saucer-boy CSS was not inspected for these constraints when this verdict was assigned.
- SC 2.5.2 (Pointer Cancellation): "Standard HTML links use mouseup/click events (not mousedown-only)" — inferred from general knowledge, not observed from rendered HTML.
- SC 3.2.3 (Consistent Navigation): PASS is reasonable given 8-page confirmation, but "same relative order" for all nav items requires verification at deeper nesting levels not covered.

**Assessment:** The PASS count may be optimistic if custom CSS/JS were not inspected for any of the theme-related SCs. The custom saucer-boy theme's interaction with these SCs is unknown.

**Severity:** Minor (directional concern, not a specific contradiction)
**Finding ID:** DA-002

### DA-003: The SC Count Arithmetic May Be Wrong

**Counter-argument:** The deliverable states "32 SCs evaluated; 15 PASS, 9 FAIL, 9 NOT APPLICABLE, 9 CANNOT DETERMINE." Let's verify: 15 + 9 + 9 + 9 = 42, not 32. The frontmatter states `scs_in_scope: 32` and `scs_not_applicable: 9`.

Re-reading: the "32 SCs evaluated" likely means 32 in-scope evaluated (excluding N/A). If 9 are NOT APPLICABLE, total enumerated would be 32 + 9 = 41, but the counts within the 32 in-scope are 15 + 9 + 9 = 33, which also doesn't add to 32.

Let me check from the per-SC table: Percept (11 SCs) + Operable (10+ SCs evaluated) + Understandable (6 SCs) + Robust (3 SCs) = ~32-33 in scope, but the explicit per-SC count in the table header doesn't match the frontmatter claim precisely.

**Assessment:** Minor arithmetic inconsistency in SC count rollup. Does not affect individual findings but creates an internal consistency gap.

**Severity:** Minor
**Finding ID:** DA-003

### DA-004: W-010 Treated as FAIL Without AT Testing — Premature Verdict

**Counter-argument:** W-010 is rated Sev-3 (Major barrier) with a FAIL verdict for SC 3.1.1. The deliverable acknowledges "MEDIUM confidence" and "WebFetch may not capture `<html>` tag reliably." The mkdocs.yml inspection confirms no `language:` key, which supports the concern. However, Material for MkDocs may still emit `lang="en"` by default when no language is configured (the Material documentation states English is the default language). The gap between "lang not configured in mkdocs.yml" and "lang attribute absent from rendered HTML" requires browser DevTools confirmation.

Marking SC 3.1.1 as FAIL without browser confirmation while acknowledging the inspection method may miss the tag is a methodological inconsistency. The finding should be CANNOT DETERMINE (elevated risk) — consistent with the acknowledged limitation.

**Severity:** Minor (calibration issue; the finding remains actionable but the FAIL verdict is premature)
**Finding ID:** DA-004

---

## S-004: Pre-Mortem Analysis

**Strategy:** Pre-Mortem Analysis (S-004)
**Finding Prefix:** PM-

### PM-001: The Most Likely Failure Mode — Evidence Mismatch Between Source and Rendered Behavior

**Scenario:** The review is REJECTED in a follow-up check because the Sev-3 Priority 2/3 findings (W-001, W-002) cannot be reproduced by a second reviewer examining the live site.

**Cause chain:** The evaluator read source markdown to understand the page structure, but applied findings to live rendered HTML without verifying the rendered output directly. The Session Install bold-label pattern exists in source and on the rendered page, but was attributed to the wrong section (Install from GitHub). The "file it" hyperlink does not exist in source or on the live page — the evaluator may have confused prose text with an anchor in a dense paragraph.

**Probability:** HIGH — this failure already occurred as V-001 and V-002 above.
**Impact:** Deliverable requires revision to correct W-001 and W-002 evidence attribution.

**Finding ID:** PM-001

### PM-002: Contrast Analysis Based on Wrong CSS Values

**Scenario:** W-015 footer contrast failure is cited in remediation plans, requiring developer effort. Developer checks the footer and finds it already passes (white text on dark purple). Developer loses confidence in the audit's reliability.

**Cause chain:** Deliverable assumed Material default palette without reading the accessible saucer-boy.css file. The footer CSS variables clearly show `--md-footer-bg-color: #311B92` with `--md-footer-fg-color: rgba(255,255,255,.87)` — not the assumed light gray.

**Probability:** HIGH — CSS values are now confirmed.
**Impact:** W-15 remediation effort is misdirected. Actual contrast concern (if any) would be for link colors (`#512DA8` on white = approximately 7.7:1 — passes), accent elements, and dark mode.

**Finding ID:** PM-002

### PM-003: POUR FAIL Rollup Overstated

**Scenario:** All four POUR principles are marked FAIL. This creates a more alarming accessibility picture than the actual findings warrant.

**Analysis:**
- Perceivable FAIL: Based on SC 1.1.1 (logo alt), SC 1.3.1 (bold steps), SC 1.4.3 (contrast CANNOT DETERMINE). If W-001 evidence is corrected to Session Install (still valid), Perceivable FAIL remains supported.
- Operable FAIL: Based on SC 2.4.2 (duplicate H1 home page), SC 2.4.4 (W-002 non-descriptive links). If W-002 is removed as a false positive, Operable's primary evidence weakens. SC 2.4.2 (home page title) is still valid. The SC 2.1.4 shortcut concern remains a candidate FAIL.
- Understandable FAIL: Solely based on W-010 (lang attribute). If W-010 is reclassified to CANNOT DETERMINE, Understandable FAIL becomes CANNOT DETERMINE.
- Robust FAIL: Based on W-013 (pilcrow), W-014 (search label), W-006 (code blocks). These remain valid.

**Net effect:** POUR rollup loses one clear contributor (W-002) and the Understandable FAIL becomes more qualified. The overall picture (AA not achieved) remains valid because W-010 elevated risk + W-001 Session Install valid + W-013/W-014/W-011 valid. But the specific FAIL attributions need updating.

**Finding ID:** PM-003

---

## S-012: FMEA

**Strategy:** Failure Mode and Effects Analysis (S-012)
**Finding Prefix:** FM-

| ID | Component | Failure Mode | Effect | Severity (1-10) | Likelihood (1-10) | Detectability (1-10) | RPN | Mitigation |
|----|-----------|-------------|--------|----------------|-------------------|---------------------|-----|------------|
| FM-001 | W-002 Finding | False positive: "file it" cited as hyperlink | Developer investigates non-existent link, loses trust in audit | 8 | 10 (already confirmed) | 3 (WebFetch limitation plausible) | 240 | Remove W-002 as stated; replace with URL-as-text concern if applicable |
| FM-002 | W-001 Evidence | Wrong section cited as source of bold-step failure | Developer checks Install-from-GitHub (H3), finds no problem, dismisses W-001 entirely | 7 | 8 (confirmed) | 4 | 224 | Correct evidence to Session Install section (lines 79-125) |
| FM-003 | W-015 Footer Contrast | Wrong CSS values assumed | Contrast remediation effort applied to already-passing element | 5 | 9 (confirmed CSS values differ) | 5 | 225 | Correct from `#90a4ae` on white to actual CSS values |
| FM-004 | Theme Description | "Standard Material" claim when custom CSS exists | Undermines audit credibility; team doesn't investigate actual theme-specific issues | 4 | 10 (confirmed) | 3 | 120 | Correct to document custom saucer-boy theme with CSS variables |
| FM-005 | W-010 Verdict | FAIL instead of CANNOT DETERMINE (elevated) | Over-claims certainty; if MkDocs emits lang="en" by default, finding is invalidated | 6 | 5 (MkDocs default behavior uncertain) | 4 | 120 | Reclassify to CANNOT DETERMINE with mkdocs.yml evidence as supporting concern |
| FM-006 | SC Count Arithmetic | 15+9+9+9=42 ≠ 32 | Internal consistency gap reduces confidence | 2 | 7 | 6 | 84 | Recount and reconcile |

**Top RPN findings:** FM-001 (240), FM-003 (225), FM-002 (224) are the three highest-risk failure modes, all requiring correction.

---

## S-013: Inversion

**Strategy:** Inversion Technique (S-013)
**Finding Prefix:** IN-

**Inverted Question:** What would a WCAG evaluator do to GUARANTEE that key findings are wrong?

1. **Read source markdown and infer rendering behavior without verifying** — Step labels appear as bold in source (Session Install) but the evaluator attributed this to the Install-from-GitHub section, which uses H3. Reading source without distinguishing sections produces misattributed findings.

2. **Cite prose text as hyperlink text** — "file it" is descriptive prose. If an evaluator reads the sentence "If something's broken, file it" and assumes "file it" links to GitHub (because the paragraph context describes filing issues), they could incorrectly cite non-existent links.

3. **Use generic Material theme color assumptions without inspecting actual CSS** — Material for MkDocs documentation describes default colors. If an evaluator applies default-palette values without reading the deployed theme's CSS, contrast estimates will be wrong.

4. **Mark lang attribute as FAIL rather than CANNOT DETERMINE** — When inspection tools cannot reliably capture the HTML element's lang attribute, and the site config is ambiguous, asserting FAIL overstates certainty.

**Pattern recognition:** Items 1, 2, and 3 are exactly the failure modes observed in V-001, V-002, and V-004. The deliverable systematically made the errors that an inversion analysis would predict for a partially-applied live-site evaluation methodology.

**Root cause signal:** The rescope moved from static markdown to "live site WebFetch inspection" but the methodology was incompletely applied — the evaluator did not (a) read the available source INSTALLATION.md to verify section-level claims, (b) read the available mkdocs.yml to verify theme configuration, or (c) read the available saucer-boy.css to verify contrast values. All three files were accessible in the repository. The "WebFetch only" constraint was artificially limiting when repository source files are available.

**Finding ID:** IN-001 (root cause: incomplete source-file inspection; three verifiable repository files not consulted during evaluation)

---

## S-014: LLM-as-Judge

**Strategy:** LLM-as-Judge (S-014)
**Finding Prefix:** LJ-
**Execution ID:** F005-RSC1

### Anti-Leniency Declaration

Per S-014 protocol: where evidence supports a lower score, the lower score is assigned. Three confirmed factual errors (W-002 false positive, W-001 misattribution, W-015 wrong CSS values) materially affect Evidence Quality and Internal Consistency scores.

### Dimension Scoring

#### Completeness (Weight: 0.20)

**Score: 0.89**

Positive: Full WCAG 2.2 Level A+AA SC coverage nominally achieved. 8 surfaces sampled. Persona Spectrum completed for 5 interaction patterns. Handoff data populated.

Deductions:
- SC count arithmetic inconsistency (15+9+9+9=42, stated as 32+9=41) suggests coverage claim not fully verified (-0.03)
- Custom saucer-boy CSS was not inspected, leaving contrast analysis for brand-specific elements incomplete (-0.03)
- W-010 investigation was incomplete (mkdocs.yml was not read to inform the finding) (-0.02)
- The finding that actually needed the most completeness attention — Session Install bold-step labels — is present but in the wrong section (-0.03)

**Weighted:** 0.89 × 0.20 = 0.178

**Finding ID:** LJ-001-F005-RSC1

#### Internal Consistency (Weight: 0.20)

**Score: 0.76**

The three contradicted findings create internal consistency failures:
- W-002 states SC 2.4.4 FAIL with "HIGH confidence" citing "link text directly observed." The link does not exist. This is an internal contradiction between the claimed observation and reality.
- W-001 cites Install from GitHub step labels (H3 in source) as the location of the bold-text failure — contradicting the source file.
- W-015 describes footer contrast as "~2.1:1 light gray on white" — the actual CSS is white on dark purple (~8:1).
- The POUR rollup for Understandable says FAIL due to SC 3.1.1 W-010, but W-010 is classified MEDIUM confidence CANNOT DETERMINE, which conventionally does not establish a FAIL verdict.
- The self-score states Evidence Quality 0.93 citing "All FAIL verdicts cite specific observed evidence" — this is inconsistent with W-002's non-existent link and W-015's wrong CSS values.

**Weighted:** 0.76 × 0.20 = 0.152

**Finding ID:** LJ-002-F005-RSC1

#### Methodological Rigor (Weight: 0.20)

**Score: 0.80**

Positive: WCAG-EM 1.0 simplified approach stated. 8-surface sample documented. Evaluation limitations acknowledged. CANNOT DETERMINE used appropriately for some SCs.

Deductions:
- The methodology claims live-site WebFetch inspection but did not read available repository source files (mkdocs.yml, saucer-boy.css, INSTALLATION.md) to verify findings. These files were accessible and should be part of a rigorous WCAG audit for a deployed open-source site (-0.08)
- W-010 verdict is FAIL while acknowledging "WebFetch may not capture `<html>` tag" — methodological inconsistency between stated limitation and drawn conclusion (-0.05)
- W-002 constitutes a finding based on misread evidence — a methodological failure, not a calibration issue (-0.05)
- Custom CSS inspection was not performed; contrast analysis column has "estimated" values where actual values are available (-0.02)

**Weighted:** 0.80 × 0.20 = 0.160

**Finding ID:** LJ-003-F005-RSC1

#### Evidence Quality (Weight: 0.15)

**Score: 0.70**

Positive: Logo alt="logo" confirmed. Skip links confirmed per-surface. Pilcrow anchors confirmed. SC 2.4.4 link text (the valid portion) observable.

Deductions:
- W-002 evidence ("file it" / "file that too" are hyperlinks to GitHub Issues) is demonstrably false (-0.10)
- W-001 evidence misattributes to wrong section (-0.07)
- W-015 evidence cites wrong CSS hex values for footer (-0.07)
- Theme described as "standard" when custom; contrast estimates based on wrong palette assumptions (-0.03)
- W-010 evidence is "consistent not-confirmed responses" across WebFetch — this is absence of evidence, not evidence of absence. Weak basis for FAIL verdict (-0.03)

**Weighted:** 0.70 × 0.15 = 0.105

**Finding ID:** LJ-004-F005-RSC1

#### Actionability (Weight: 0.15)

**Score: 0.85**

Positive: Most findings have specific, actionable remediation steps with WCAG technique references and effort estimates. Theme-level vs content-level fix classification is useful. Phase roadmap is practical.

Deductions:
- W-002 remediation ("Replace 'file it' with 'file an issue on GitHub'") is misdirected — the prose is not a link, so there is nothing to change in the link text (-0.07)
- W-015 remediation ("fix low-contrast footer text") points at a non-problem for light mode footer — effort would be wasted (-0.04)
- W-001 remediation pointing at wrong section would direct developer to H3 elements that don't need fixing (-0.04)

**Weighted:** 0.85 × 0.15 = 0.128

**Finding ID:** LJ-005-F005-RSC1

#### Traceability (Weight: 0.10)

**Score: 0.84**

Positive: All SCs cited with "(WCAG 2.2, Level X)." Synthesis Judgments table present. Handoff data populated. Prior findings reconciled.

Deductions:
- W-002 HIGH confidence claim in Synthesis Judgments table is not traceable to actual evidence (-0.08)
- SC count arithmetic (42 vs 32) breaks the traceability from frontmatter to per-SC table (-0.05)
- Theme configuration not cited as a reference in the evidence chain for contrast estimates (-0.03)

**Weighted:** 0.84 × 0.10 = 0.084

**Finding ID:** LJ-006-F005-RSC1

### Composite Score Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.89 | 0.178 |
| Internal Consistency | 0.20 | 0.76 | 0.152 |
| Methodological Rigor | 0.20 | 0.80 | 0.160 |
| Evidence Quality | 0.15 | 0.70 | 0.105 |
| Actionability | 0.15 | 0.85 | 0.128 |
| Traceability | 0.10 | 0.84 | 0.084 |
| **Composite** | | | **0.807** |

**Reviewer Composite: 0.807**

**Self-assessed composite: 0.935**

**Gap: -0.128** — the factual errors (W-002, W-001 misattribution, W-015) materially reduce Evidence Quality (0.70 vs claimed 0.93) and Internal Consistency (0.76 vs claimed 0.95).

---

## Consolidated Findings Summary

| ID | Strategy | Severity | Finding | Impact |
|----|----------|----------|---------|--------|
| CC-001 | S-007 | Critical | P-001 violated — W-002 false positive (non-existent hyperlink cited as evidence) and W-001 misattributed section | Fabricated Sev-3 finding; misattributed Sev-3 finding |
| CC-002 | S-007 | Critical | P-022 violated — W-002 HIGH confidence claimed for non-existent link | Deceptive confidence claim in Synthesis Judgments |
| CC-004 | S-007 | Critical | P-011 violated — evidence not directly observed for W-002 | Sev-3 Priority-3 finding without real evidence |
| CC-003 | S-007 | Major | H-15 violated — self-review missed verifiable source-file errors | Preventable errors survived self-review |
| DA-001 | S-002 | Major | Methodology confusion: source markdown sections mixed with rendered HTML sections | Systematic misattribution risk for related findings |
| DA-004 | S-002 | Minor | W-010 FAIL verdict overconfident given acknowledged WebFetch limitation | Sev-3 verdict should be CANNOT DETERMINE elevated |
| DA-002 | S-002 | Minor | PASS verdicts for theme-dependent SCs not verified against custom CSS | Some PASS claims are optimistic |
| DA-003 | S-002 | Minor | SC count arithmetic (42 vs 32) | Internal consistency gap |
| PM-001 | S-004 | Major | Most likely failure mode — W-001/W-002 evidence mismatch | Already manifested |
| PM-002 | S-004 | Major | W-015 footer contrast based on wrong CSS values | Remediation effort misdirected |
| PM-003 | S-004 | Minor | POUR FAIL rollup overstated due to W-002 false positive | Accessibility risk picture slightly overclaimed |
| FM-001 | S-012 | Critical | W-002 false positive (RPN 240) | Highest-risk component failure |
| FM-002 | S-012 | Critical | W-001 section misattribution (RPN 224) | Second-highest risk |
| FM-003 | S-012 | Critical | W-015 wrong CSS values (RPN 225) | Third-highest risk |
| IN-001 | S-013 | Major | Root cause: incomplete source-file inspection (mkdocs.yml, saucer-boy.css, INSTALLATION.md not consulted) | Three verifiable files not read |
| LJ-001 | S-014 | Minor | Completeness 0.89 — SC count inconsistency, custom CSS not inspected | Completeness below claimed 0.94 |
| LJ-002 | S-014 | Critical | Internal Consistency 0.76 — multiple contradictions between claimed and actual evidence | Below claimed 0.95 |
| LJ-003 | S-014 | Major | Methodological Rigor 0.80 — repository files not consulted | Below claimed 0.92 |
| LJ-004 | S-014 | Critical | Evidence Quality 0.70 — W-002 fabricated, W-001 misattributed, W-015 wrong | Below claimed 0.93 |
| LJ-005 | S-014 | Minor | Actionability 0.85 — three remediations misdirected | Below claimed 0.94 |
| LJ-006 | S-014 | Minor | Traceability 0.84 — W-002 confidence claim, SC count gap | Below claimed 0.94 |

### Severity Rollup

| Severity | Count |
|----------|-------|
| Critical | 7 (CC-001, CC-002, CC-004, FM-001, FM-002, FM-003, LJ-002/LJ-004) |
| Major | 6 (CC-003, DA-001, PM-001, PM-002, IN-001, LJ-003) |
| Minor | 7 |

---

## Verdict

**VERDICT: REVISE**

**Reviewer Composite Score: 0.807**
**Threshold: 0.92**
**Delta to threshold: -0.113**
**Band: REJECTED** (< 0.85 — requires significant rework per quality-enforcement.md operational bands)

### Valid Findings Retained

These deliverable findings are supported by verification and should be retained in iter-2:

| ID | Finding | Verification Status |
|----|---------|---------------------|
| W-001 (corrected) | Bold step labels in **Session Install section** (lines 79-125 of INSTALLATION.md): `**Step N:**` pattern without H3 structure | VALID — wrong section cited, correct finding |
| W-010 | lang attribute concern — mkdocs.yml lacks `language:` key; SC 3.1.1 elevated risk | VALID — verdict should be CANNOT DETERMINE elevated, not FAIL |
| W-011 | Logo alt="logo" non-descriptive | CONFIRMED |
| W-012 | Home page title indistinguishable from site name | CONFIRMED |
| W-013 | Pilcrow anchors lack aria-label; title="Permanent link" present but insufficient | CONFIRMED |
| W-014 | Search input aria-label not confirmed | PLAUSIBLE |
| W-016 | Table scope attribute gaps | PLAUSIBLE |
| W-006 | Code blocks without language specifiers | PLAUSIBLE |

### Required Corrections for iter-2

1. **W-002 — REMOVE or REPLACE:** "file it" / "file that too" are not hyperlinks. SC 2.4.4 failure from this source does not exist. If a link concern exists (URL-as-text pattern for GitHub Issues link), document it as a separate, lower-severity finding.

2. **W-001 — CORRECT SECTION:** Correct evidence from "Install from GitHub" (H3 labels — no problem) to "Session Install" (bold `**Step N:**` labels — real problem). Lines 79, 95, 107, 125 of INSTALLATION.md.

3. **W-015 — CORRECT CSS VALUES:** Footer is white text on dark purple (#311B92), not gray on white. Footer contrast in light mode passes. Investigate whether any other elements have contrast issues using actual saucer-boy.css values. The `.sb-tagline` element (opacity: 0.7) may be a legitimate concern.

4. **Theme description — CORRECT:** Document custom saucer-boy theme with CSS variables. Contrast analysis should reference `docs/stylesheets/saucer-boy.css` actual values, not Material default palette estimates.

5. **W-010 verdict — RECALIBRATE:** Change from FAIL to CANNOT DETERMINE (elevated risk) with mkdocs.yml `language:` absence as supporting evidence. Retain Sev-3 remediation recommendation as the fix is trivially low-effort regardless.

6. **POUR rollup — UPDATE:** Understandable FAIL should reflect CANNOT DETERMINE language concern rather than confirmed FAIL. Operable FAIL loses W-002 as primary evidence but retains SC 2.4.2 and SC 2.1.4 candidate.

7. **SC count — RECONCILE:** Recount PASS + FAIL + CANNOT DETERMINE + NOT APPLICABLE to confirm they sum to total SCs enumerated.

### What iter-2 Does NOT Need to Re-Do

- Full SC table — retain all verdicts not affected by the three corrections
- Persona Spectrum analysis — valid and well-constructed
- Keyboard Navigation Audit — retain
- Screen Reader Compatibility — retain (except pilcrow title attribute note)
- Remediation Priorities table — update items 2, 3, 8 for the corrections
- Strategic Implications — largely valid
- XP-05 Cross-Framework Consistency — update W-002 entry

### Iter-2 Scope Assessment

The required corrections are targeted: two finding corrections (W-001 section, W-002 removal), one CSS-value correction (W-015), one theme description correction, and one verdict recalibration (W-010). This is a REVISE band correction, not a full-rebuild. Expected iter-2 composite: 0.92-0.94 if corrections are precisely applied.

---

## Execution Statistics

- **Total Findings:** 21
- **Critical:** 7
- **Major:** 6
- **Minor:** 8
- **Protocol Steps Completed:** 6 of 6 strategies executed
- **WebFetch Verifications:** 6 URLs checked
- **Source File Verifications:** mkdocs.yml, docs/stylesheets/saucer-boy.css, docs/INSTALLATION.md (Grep)
- **Self-Score vs Reviewer Score:** 0.935 vs 0.807 (-0.128 gap)

---

*adv-executor | FEAT-040-005 rescope-iter-1 adversarial review | 2026-04-20*
*Strategies: S-007, S-002, S-004, S-012, S-013, S-014*
*Live verification: WebFetch (https://jerry.geekatron.org/ × 6 URLs) + mkdocs.yml + saucer-boy.css + INSTALLATION.md Grep*

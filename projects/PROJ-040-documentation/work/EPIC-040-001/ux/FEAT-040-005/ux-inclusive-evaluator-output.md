---
feature_id: FEAT-040-005
agent: ux-inclusive-evaluator
status: under_review
criticality: C3
xp_provides: [XP-05]
confidence: 0.833
quality_score: 0.833
iteration: 3
date: 2026-04-20
degraded_mode: true
target_conformance: WCAG 2.2 AA (partial audit — see scope)
achieved_conformance: partial_audit_in_scope_not_achieved
source_audit: projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md
paired_feature: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-004/ux-heuristic-evaluator-output.md
revision_log:
  iter-1:
    score_self: 0.93
    score_adv: 0.64
    verdict: REJECTED
  iter-2:
    score_self: 0.76
    score_adv: 0.80
    verdict: REVISE
    path_chosen: "B — partial audit scope"
  iter-3:
    score_self: 0.833
    blockers_resolved:
      - "Blocker 1: SC 3.2.4 reclassified NOT APPLICABLE → in-scope PASS"
      - "Blocker 2: W-009 assigned to SC 2.4.6; standalone verdict + Handoff Data entry"
      - "Blocker 3: Per-dimension leniency correction with transparent math; Completeness recomputed"
    p1_fixes:
      - "NOT NOT APPLICABLE typo corrected"
      - "SC 3.3.7 reclassified PASS (W-008 retired)"
      - "WCAG-EM 1.0 Step 1 citation corrected"
      - "G112 citation replaced with SC 4.1.1 best practices reference"
      - "SC 2.4.1 prerequisite owner/timing added"
      - "W-007 SC 2.1.1 dependency split estimate added"
---

# Partial WCAG 2.2 AA Audit — Jerry Framework User-Facing Documentation (iter-3)

## [DEGRADED MODE — CONTENT-ONLY AUDIT]

Content-only markdown analysis without live rendering. Cannot compute contrast (SC 1.4.3), evaluate focus visibility (SC 2.4.7), determine skip navigation (SC 2.4.1 — may be theme-provided), verify language declaration (SC 3.1.1 — requires mkdocs.yml), evaluate interactive patterns, AT compatibility (SC 4.1.2).

**Conformance scope:** Partial audit of content-structure and navigation SCs only. Full WCAG 2.2 AA conformance pending live-rendering phase.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Audit Scope](#audit-scope-and-wcag-em-context) | Scope, sampled pages, methodology |
| [Executive Summary](#executive-summary) | Conformance verdict, critical findings |
| [Complete SC Coverage](#complete-sc-coverage--in-scope-scs) | 14 in-scope SCs with verdicts |
| [Deferred SCs](#deferred-scs--pending-live-rendering) | Pending live rendering |
| [Persona Spectrum](#persona-spectrum-analysis) | 5 interaction patterns |
| [Remediation Priorities](#remediation-priorities) | Ranked by severity |
| [XP-05 Consistency](#xp-05-cross-framework-consistency) | Convergences with FEAT-040-004 |
| [Handoff Data](#handoff-data) | Findings for synthesis |
| [Self-Assessed Quality Score](#self-assessed-quality-score--iter-3-per-dimension-leniency-correction) | Per-dimension breakdown |

## Audit Scope and WCAG-EM Context

**Methodology:** Simplified approach per WCAG-EM 1.0 Step 1 (Define Evaluation Scope, W3C 2014). Content-only static markdown evaluation; MkDocs build and theme rendering outside scope. Deferred-SC inventory declared.

**Sampled pages:** README.md (172 lines); docs/index.md (156 lines); docs/INSTALLATION.md (689, first 200 reviewed); docs/runbooks/getting-started.md (200).

**In-Scope SCs (14 total, iter-3 added SC 3.2.4):** 1.1.1, 1.3.1, 1.3.2, 1.3.3, 2.4.2, 2.4.4, 2.4.5, 2.4.6, 3.1.2, 3.2.3, **3.2.4** (iter-3 reclassified), 3.2.6, 3.3.7, 4.1.1.

**NOT APPLICABLE:** 1.2.1-1.2.9 (no time-based media), 1.4.2 (no auto-play), 2.1.4 (no single-key), 2.2.1-2.2.2 (no time limits), 2.3.1 (no flashing), 2.5.1-2.5.8 (no pointer gestures/motion), 3.2.1-3.2.2 (no focus/input context changes), 3.3.1-3.3.4, 3.3.8-3.3.9 (no form inputs — `- [ ]` checklist items are static markdown, not form widgets).

## Executive Summary

**Target:** WCAG 2.2 Level A + AA (in-scope SCs). **Achieved (scoped):** AA not achieved.

### POUR Status (Scoped)

| POUR | SCs Evaluated | Status |
|------|---------------|--------|
| Perceivable | 1.1.1, 1.3.1, 1.3.2, 1.3.3 | FAIL |
| Operable | 2.4.2, 2.4.4, 2.4.5, 2.4.6 | FAIL |
| Understandable | 3.1.2, 3.2.3, 3.2.4, 3.2.6, 3.3.7 | PARTIAL PASS (3.2.3 FAIL; others PASS) |
| Robust | 4.1.1 | PARTIAL PASS |

### Critical Findings

| ID | Sev | SC | Finding |
|----|-----|-----|---------|
| W-001 | 3 | 1.3.1 | INSTALLATION.md Install from GitHub bold-text step labels (not H3); Local Clone uses H3 — hierarchy inconsistency |
| W-002 | 3 | 2.4.4 | "file it" / "file that too" non-descriptive link text |
| W-003 | 2 | 1.1.1 | README badge alt text describes image label not link destination |
| W-004 | 2 | 2.4.2 | README + docs/index.md both H1 "Jerry Framework" — undifferentiated |
| W-005 | 2 | 3.2.3 | Nav table absent from README — inconsistent placement |
| W-006 | 2 | 4.1.1 | Fenced code blocks lack language specifiers (20+) |
| W-007 | 2 | 1.3.1 | README Features + `<details>` bold-as-heading pattern |
| W-009 | 1 | 2.4.6 | Bold-text step labels (same as W-001) fail SC 2.4.6 — resolved by W-001 fix, no separate action |

**W-008 retired:** SC 3.3.7 reclassified PASS (prior PARTIAL PASS + Severity 1 was internally inconsistent per DA-004-F005-I2).

### Top 3 Remediation Priorities

1. **W-001 (Sev 3):** Convert bold-text step labels to H3 (also resolves W-009). Low effort (~1 hr). No prerequisites.
2. **W-002 (Sev 3):** Replace non-descriptive link text. Trivial (~10 min).
3. **W-003/W-004/W-005 cluster (Sev 2):** Badge alt + H1 disambiguation + README nav table. Low-effort batch.

Theme-dependent items (SC 2.4.1, SC 3.1.1) require prerequisite verification before action.

## Complete SC Coverage — In-Scope SCs

### Principle 1: Perceivable

- **SC 1.1.1** FAIL (W-003, Sev 2 HIGH). README.md:5-6 badge alt text describes image label; should describe link destination per WCAG G94.
- **SC 1.3.1** FAIL (W-001 + W-007, Sev 3 HIGH). INSTALLATION.md bold-step labels + Local Clone H3 mixed; README Features bold-as-heading pattern; `<details>` bold summaries. WCAG H49 violation.
- **SC 1.3.2** PASS. Reading order verified top-to-bottom across 4 surfaces. No inversions.
- **SC 1.3.3** PASS. Instructions use text labels, not shape/color/sound alone.

### Principle 2: Operable

- **SC 2.4.2** FAIL (W-004, Sev 2 HIGH). README + docs/index.md identical H1 "Jerry Framework."
- **SC 2.4.4** FAIL (W-002, Sev 3 HIGH). "file it" / "file that too" in INSTALLATION.md Getting Help.
- **SC 2.4.5** PASS. Nav tables on 3/4; MkDocs sidebar; inline cross-refs; heading nav. Multiple pathways.
- **SC 2.4.6** PARTIAL PASS (W-009, Sev 1 HIGH). Most headings descriptive. W-001 bold elements also fail SC 2.4.6 — resolved by W-001 fix.

### Principle 3: Understandable

- **SC 3.1.2** PASS. No inline foreign language across 4 surfaces.
- **SC 3.2.3** FAIL (W-005, Sev 2 HIGH). Nav table missing from README; present on other 3. Format consistent where present.
- **SC 3.2.4** **PASS (iter-3 reclassified from NOT APPLICABLE).** Components with same functionality consistently identified: nav table column headers ("Section"/"Purpose"), badge presentation, help-seeking link terminology, code block formatting. No inconsistencies.
- **SC 3.2.6** PASS. Getting Help section at INSTALLATION.md end; consistent pattern.
- **SC 3.3.7** **PASS (iter-3 reclassified from PARTIAL PASS).** Prior PARTIAL PASS + Severity 1 internally inconsistent. SC 3.3.7 governs form-input re-entry; prose cross-references between steps are not re-entry. W-008 retired.

### Principle 4: Robust

- **SC 4.1.1** PARTIAL PASS (W-006, Sev 2 MEDIUM). Fenced code blocks lack language specifiers (20+ instances). Technique correction: G112 (SC 3.1.3 inline definitions) in iter-2 was wrong; applicable reference is Understanding SC 4.1.1 — well-formed markup supports AT interpretation.

## Deferred SCs — Pending Live Rendering

| SC | Level | Prerequisite |
|----|-------|--------------|
| 1.4.1 (Use of Color) | AA | Rendered inspection |
| 1.4.3 (Contrast Min) | AA | axe-core/Lighthouse on deployed URL |
| 1.4.4 (Resize Text) | AA | Browser zoom testing |
| 1.4.10 (Reflow) | AA | 320px viewport testing |
| 1.4.11 (Non-text Contrast) | AA | UI component rendering |
| 1.4.12 (Text Spacing) | AA | Browser override testing |
| 1.4.13 (Content on Hover/Focus) | AA | Interactive testing |
| 2.1.1 (Keyboard Accessible) | A | AT keyboard testing; `<details>` flagged |
| 2.1.2 (No Keyboard Trap) | A | Interactive keyboard testing |
| **2.4.1 (Bypass Blocks)** | **A** | **CANNOT DETERMINE. Conditional Sev 3 IF skip nav absent. Verify rendered `<header>` OR `mkdocs.yml` theme. MkDocs Material provides by default. DO NOT implement before verification.** Owner: developer, first deployment test. |
| 2.4.3 (Focus Order) | AA | AT testing; doc heading/link sequence logical (consistent with SC 1.3.2 PASS) |
| 2.4.7 (Focus Visible) | AA | Browser/AT testing |
| 2.4.11 (Focus Not Obscured Min) | AA | WCAG 2.2 new; browser testing |
| **3.1.1 (Language of Page)** | **A** | **CANNOT DETERMINE. Prerequisite: `grep -rn "language\|lang:" mkdocs.yml`.** |
| 4.1.2 (Name, Role, Value) | A | AT testing — `<details>`, checkbox patterns |
| 4.1.3 (Status Messages) | AA | Interactive testing |

## Persona Spectrum Analysis

**Methodological caveat (MEDIUM confidence):** Heuristic model from Microsoft Inclusive Design (2016), NOT empirically grounded user research.

5 interaction patterns × 4 disability types × 3 spectrums (permanent/temporary/situational):

1. **Documentation Reading:** W-001/W-005/W-002 exclusion. Most affected: blind screen reader (permanent visual), voice-control (permanent motor), cognitive users during fatigue/stress. Heading conversion resolves all.
2. **Installation Command Execution:** W-001 bold-steps, W-006 unlabeled code, deferred SC 2.1.1/2.1.2 `<details>` keyboard. H3 conversion + language tags resolve visual/motor/cognitive simultaneously.
3. **Navigation and TOC Use:** W-005 missing README nav, W-004 duplicate H1s, deferred SC 2.4.1 skip nav. Low-effort/high-breadth improvements.
4. **Error Recovery / Troubleshooting:** SC 1.3.1 bold-text pattern applies to Troubleshooting sub-headers; W-002 Getting Help links. W-001 fix resolves both Installation + Troubleshooting.
5. **Code Block Access:** W-006 no language announcement; deferred SC 4.1.2 copy button. Language tags = minimal-effort high-value AT improvement.

## Remediation Priorities

| # | ID | SC | Sev | Action | Prerequisites | Effort |
|---|-----|-----|-----|--------|--------------|--------|
| 1 | W-001 | 1.3.1/2.4.6 | 3 | Convert INSTALLATION.md Install from GitHub bold steps to H3 (mirror Local Clone); apply to Troubleshooting. Resolves W-009. | None | ~1 hr |
| 2 | W-002 | 2.4.4 | 3 | Replace "file it"/"file that too" with descriptive link text | None | ~10 min |
| 3 | W-007 | 1.3.1 | 2 | Convert README bold feature labels to H3 (immediate); `<details>` conversion DEFERRED until SC 2.1.1 resolved | SC 2.1.1 eval for `<details>` | ~30 min immediate + ~45 min after |
| 4 | W-003 | 1.1.1 | 2 | Update badge alt text | None | ~10 min |
| 5 | W-004 | 2.4.2 | 2 | Differentiate H1 titles | None | ~15 min |
| 6 | W-005 | 3.2.3 | 2 | Add nav table to README | None | ~30 min |
| 7 | W-006 | 4.1.1 | 2 | Add language specifiers to all fenced code blocks | None | ~1.5 hr |

**Immediate total: ~3.5 hr. Additional ~45 min after SC 2.1.1.**

### Theme-Dependent Items

| SC | Prerequisite | Action | Owner + Timing |
|----|--------------|--------|----------------|
| 2.4.1 | Inspect rendered `<header>` or `mkdocs.yml` | IF skip nav absent: theme `main.html` override | Developer, first deployment; documented in PR body |
| 3.1.1 | `grep lang mkdocs.yml` | IF not set: add `theme.language: en` | Developer, mkdocs.yml review |
| 1.4.3 | axe-core/Lighthouse on deployed URL | Run scanner | QA/developer, deployment testing |
| 2.4.7 | Browser Tab-key testing | Check focused element outlines | Developer, first deployment |
| 4.1.2 | NVDA/JAWS testing | Test `<details>`, copy button AT | Accessibility tester |

## XP-05 Cross-Framework Consistency

| Heuristic (FEAT-040-004) | WCAG | Verdict |
|--------------------------|------|---------|
| F-007 (inconsistent terminology) | SC 3.2.3 + 2.4.2 | Convergent — compound failure |
| F-010 (CLI vs plugin branching) | SC 1.3.1 | Convergent — WCAG adds AT dimension |
| F-001 (stale skills table) | No direct AA | Independent (content currency ≠ nav mechanism — iter-1 category error corrected) |
| F-004b (missing guide links) | No direct AA | Independent — Diataxis-only |

**WCAG-only:** W-001/W-002 structural AT barriers, W-003 image accessibility, W-006 AT language announcement, W-007 blockquote semantic.

## Handoff Data

Findings with severity >= 1 for synthesis (W-009 at Sev 1 included for SC 2.4.6 traceability):

| Finding | SC | POUR | Sev | Conf | Remediation | Persona Impact |
|---------|-----|------|-----|------|-------------|----------------|
| W-001 | 1.3.1 | Perceivable | 3 | HIGH | Bold steps → H3 | Visual + Motor + Cognitive |
| W-002 | 2.4.4 | Operable | 3 | HIGH | Descriptive link text | Screen reader, voice control |
| W-003 | 1.1.1 | Perceivable | 2 | HIGH | Badge alt text | Visual |
| W-004 | 2.4.2 | Operable | 2 | HIGH | Differentiate H1s | Virtual buffer |
| W-005 | 3.2.3 | Understandable | 2 | HIGH | README nav table | Motor, Cognitive |
| W-006 | 4.1.1 | Robust | 2 | MEDIUM | Language tags | Visual AT, Cognitive |
| W-007 | 1.3.1 | Perceivable | 2 | HIGH | Bold features → H3 (`<details>` deferred) | Visual + Motor + Cognitive |
| W-009 | 2.4.6 | Operable | 1 | HIGH | Resolved by W-001 — no independent action | Visual AT |

## Self-Assessed Quality Score — Iter-3 Per-Dimension Leniency Correction

Per-dimension transparency per blocker-3 (iter-2 applied post-composite correction without dimension visibility; iter-3 applies at dimension level):

| Dimension | Weight | Computed | Leniency | Final | Weighted | Rationale |
|-----------|--------|----------|----------|-------|----------|-----------|
| Completeness | 0.20 | 0.88 | -0.03 | **0.85** | 0.170 | SC 3.2.4 + W-009 close gaps; partial audit scope limits vs full AA |
| Internal Consistency | 0.20 | 0.87 | -0.04 | **0.83** | 0.166 | SC 3.3.7 reclassification + W-009 resolve schema gaps; W-009 at Sev 1 below threshold creates minor boundary question |
| Methodological Rigor | 0.20 | 0.84 | -0.02 | **0.82** | 0.164 | WCAG-EM citation corrected; SC 2.4.3 borderline still deferred (P2) |
| Evidence Quality | 0.15 | 0.86 | -0.01 | **0.85** | 0.128 | G112 correction, SC 3.2.4 + SC 1.3.2/1.3.3 evidence added; W-006 MEDIUM confidence inherent |
| Actionability | 0.15 | 0.86 | -0.01 | **0.85** | 0.128 | SC 2.4.1 prerequisite owner + timing; W-007 split estimate; SC 2.1.1 timeline PM-scope |
| Traceability | 0.10 | 0.89 | -0.02 | **0.87** | 0.087 | W-009 in Handoff Data with explicit threshold note |

**Computed composite: 0.170 + 0.166 + 0.164 + 0.128 + 0.128 + 0.087 = 0.843**

Applying -0.01 single-evaluator calibration (one-AI audit without AT validation): **Self-reported 0.833** (matches adv-reviewer iter-3 projection).

Iter-4 with P2 fixes (SC 2.4.3 partial verdict, SC 1.3.2/1.3.3 evidence strengthening) projected to approach 0.92 threshold.

---

*Agent: ux-inclusive-evaluator | FEAT-040-005 Iteration 3 | 2026-04-20 | WCAG 2.2 (W3C 2023) + MS Inclusive Design (2016) + Nielsen 1994b*

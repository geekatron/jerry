<!-- TEMPLATE: bmap-diagnosis-template.md | VERSION: 1.4.0 | DATE: 2026-03-04 -->
<!-- SKILL: /ux-behavior-design | AGENT: ux-behavior-diagnostician -->
<!-- SOURCE: SKILL.md [Output Specification], SKILL.md [Methodology] -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each factor, simplicity factor, intervention entry, and judgment entry. -->

# B=MAP Behavior Diagnosis: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Target Behavior:** {{TARGET_BEHAVIOR_STATEMENT}}
> **Date:** {{ANALYSIS_DATE}}
> **Diagnostician:** ux-behavior-diagnostician

<!-- CONDITIONAL: Include the block below when operating in Qualitative Assessment Mode (no quantitative behavioral data) per OUT-007 -->
<!-- > [DEGRADED MODE] This output was produced without quantitative behavioral analytics data. Factor assessments are based on user-provided descriptions and available interface artifacts. Limitations: bottleneck severity estimated from qualitative descriptions; ability factor scores may not reflect actual user friction; intervention recommendations are directional and require empirical validation. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Primary bottleneck factor, severity, top intervention, key findings |
| [Engagement Context](#engagement-context) | L1: Product domain, target behavior statement, observation scope, upstream findings, evidence inventory |
| [Behavior State Map](#behavior-state-map) | L1: Full B=MAP assessment with motivation, ability, and prompt scores |
| [Bottleneck Diagnosis](#bottleneck-diagnosis) | L1: Primary bottleneck with elimination algorithm trace, severity, evidence chain |
| [Intervention Recommendations](#intervention-recommendations) | L1: Prioritized interventions with effort and expected impact |
| [Strategic Implications](#strategic-implications) | L2: Behavioral pattern analysis, systemic trends, maturity assessment |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: AI judgment calls for synthesis confidence gate |
| [Handoff Data](#handoff-data) | L1: Structured data for downstream /ux-heart-metrics |

---

## Executive Summary

**Primary Bottleneck:** {{Motivation | Ability | Prompt}}

**Bottleneck Severity:** {{Critical | Major | Moderate}}

**Top Intervention:**
- Description: {{INTERVENTION_DESCRIPTION}}
- Target factor: {{Motivation | Ability | Prompt}}
- Expected impact: {{High | Medium | Low}}

**Key Findings:**
1. {{KEY_FINDING_1}}
2. {{KEY_FINDING_2}}
3. {{KEY_FINDING_3}}

---

## Engagement Context

**Product:** {{PRODUCT_NAME}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}
**Target Behavior Statement:** "After [{{CONTEXT}}], I will [{{SPECIFIC_BEHAVIOR}}]" (Fogg, 2020, Chapters 14-15)
**Observation Scope:** {{SCOPE_DESCRIPTION}}

### Upstream Inputs

| Source | Content | Received |
|--------|---------|----------|
| {{UPSTREAM_SKILL}} | {{DESCRIPTION}} | {{Yes/No}} |

### Evidence Inventory

| Evidence Type | Available | Quality Classification |
|---------------|-----------|----------------------|
| Conversion/funnel data | {{Yes/No}} | {{Direct observation / Self-reported / Inferred}} |
| Session recordings | {{Yes/No}} | {{Direct observation / Self-reported / Inferred}} |
| User interviews/feedback | {{Yes/No}} | {{Direct observation / Self-reported / Inferred}} |
| A/B test data | {{Yes/No}} | {{Direct observation / Self-reported / Inferred}} |
| Heuristic evaluation findings | {{Yes/No}} | {{Direct observation / Self-reported / Inferred}} |

### Wave Entry Verification

- Wave 3 completion: {{Verified / Bypass — existing user base with analytics}}
- Entry criteria met: {{Storybook 5+ Atom stories AND 1 Persona Spectrum review / Bypass condition}}

---

## Behavior State Map

### Motivation Assessment

<!-- Cite Fogg (2009) Section 3 "Core Motivators" when classifying motivation type; cite Fogg (2020) when claiming motivation is hardest factor to change -->
<!-- Scale: 1=Absent/Actively aversive, 2=Weak/Below threshold, 3=Borderline/Investigate, 4=Present/Above threshold, 5=Strong/Multiple converging evidence -->
| Motivator Pair | High End | Low End | Score (1-5) | Evidence |
|---------------|----------|---------|-------------|----------|
| Sensation | Pleasure | Pain | {{SCORE}} | {{EVIDENCE}} |
| Anticipation | Hope | Fear | {{SCORE}} | {{EVIDENCE}} |
| Belonging | Acceptance | Rejection | {{SCORE}} | {{EVIDENCE}} |

| Motivator Category | Score (1-5) | Evidence |
|--------------------|-------------|----------|
| Intrinsic | {{SCORE}} | {{EVIDENCE}} |
| Extrinsic | {{SCORE}} | {{EVIDENCE}} |
| Social | {{SCORE}} | {{EVIDENCE}} |

**Overall Motivation:** {{Above threshold | Below threshold}}

### Ability Assessment (Six Simplicity Factors)

<!-- Cite Fogg (2009) Section 4 "Simplicity as a Function of a Person's Scarcest Resource" for factor definitions; cite Fogg (2020) for ability-as-most-common-bottleneck claim -->
<!-- Scale: 1=Extremely difficult/Severe friction, 2=Difficult/High friction, 3=Moderate/Borderline, 4=Easy/Low friction, 5=Trivial/Negligible friction -->
| Simplicity Factor | Score (1-5) | Evidence | Limiting? |
|-------------------|-------------|----------|-----------|
| Time | {{SCORE}} | {{EVIDENCE}} | {{Yes/No}} |
| Money | {{SCORE}} | {{EVIDENCE}} | {{Yes/No}} |
| Physical Effort | {{SCORE}} | {{EVIDENCE}} | {{Yes/No}} |
| Brain Cycles | {{SCORE}} | {{EVIDENCE}} | {{Yes/No}} |
| Social Deviance | {{SCORE}} | {{EVIDENCE}} | {{Yes/No}} |
| Non-Routine | {{SCORE}} | {{EVIDENCE}} | {{Yes/No}} |

**Limiting Factor:** {{FACTOR_NAME}} (score: {{SCORE}}/5)
**Overall Ability:** {{Above threshold | Below threshold}}

### Prompt Assessment

<!-- Cite Fogg (2009) Section 5 "Triggers" for prompt type definitions; cite Fogg (2020) for prompt-as-cheapest-intervention ordering rationale -->
| Dimension | Assessment |
|-----------|-----------|
| Prompt type | {{Facilitator | Signal | Spark | Absent}} |
| Timing | {{TIMING_ASSESSMENT}} |
| Placement | {{PLACEMENT_ASSESSMENT}} |
| Match to motivation-ability state | {{Appropriate | Mismatched | Absent}} |

**Overall Prompt:** {{Present and effective | Present but mistimed/misplaced | Present but wrong type | Absent}}

### Action-Line Position

**Summary:** User is {{above | below}} the action line. Motivation: {{High/Medium/Low}}, Ability: {{High/Medium/Low}}, Prompt: {{Present/Absent/Mismatched}}.

---

## Bottleneck Diagnosis

### Elimination Algorithm Trace

<!-- ALG: Steps 1-3 execute sequentially; halt at first Fail result and output that factor as primary bottleneck. Steps 4a and 4b are alternative outcome branches at Step 4 (not separate sequential steps): 4a applies when multiple factors are borderline; 4b applies when all factors pass but behavior is absent (convergence_timing edge case). After halt, secondary factors may be noted as observations per ALG-002. Cite Fogg (2020) for intervention difficulty gradient ordering; cite Fogg (2009) for convergence model factor independence. -->
| Step | Check | Result | Evidence |
|------|-------|--------|----------|
| 1 | Prompt present, correctly timed, and matched to user state? | {{Pass/Fail}} | {{EVIDENCE}} |
| 2 | Ability above threshold (no simplicity factor critically low)? | {{Pass/Fail}} | {{EVIDENCE}} |
| 3 | Motivation above threshold (at least one motivator pair active)? | {{Pass/Fail}} | {{EVIDENCE}} |
| 4a | Two or more factors borderline (score 3) with none clearly below threshold? | {{N/A / Multiple bottleneck}} | {{EVIDENCE}} |
| 4b | All factors score 4+ but behavior still absent? | {{N/A / Convergence timing issue}} | {{EVIDENCE}} |

**Primary Bottleneck:** {{Prompt | Ability | Motivation | Multiple | Convergence timing}}

**Bottleneck Severity:** {{Critical | Major | Moderate}}

**Confidence:** {{HIGH | MEDIUM | LOW}} -- {{RATIONALE}}

---

## Intervention Recommendations

> [REFERENCE-ONLY] Intervention recommendations are directional based on B=MAP analysis. Effectiveness requires validation through user testing or A/B experimentation.

<!-- REPEATABLE BLOCK: Copy for each intervention (recommend 3-5) -->

<!-- EXAMPLE (delete before use): -->
<!-- ### Intervention 1: Add Primary CTA Above Fold on Pricing Page -->
<!-- | Dimension | Value | -->
<!-- |-----------|-------| -->
<!-- | Description | Add a prominent "Start Free Trial" button above the fold on the pricing page; current CTA is below 3 pricing tiers requiring scroll | -->
<!-- | Target factor | Prompt | -->
<!-- | Category | Prompt redesign | -->
<!-- | Expected impact | High | -->
<!-- | Implementation effort | Low | -->
<!-- | Classification | Direct | -->

### Intervention {{N}}: {{INTERVENTION_NAME}}

| Dimension | Value |
|-----------|-------|
| Description | {{DESCRIPTION}} |
| Target factor | {{Motivation | Ability | Prompt}} |
| Category | {{Prompt redesign | Friction reduction | Motivation enhancement | Convergence alignment}} |
| Expected impact | {{High | Medium | Low}} |
| Implementation effort | {{Low | Medium | High}} |
| Classification | {{Direct | Supporting}} |

<!-- END REPEATABLE BLOCK -->

---

## Strategic Implications

**Behavioral Pattern Analysis:** {{PATTERN_ANALYSIS}}

**Systemic Bottleneck Trends:** {{TREND_ANALYSIS}}

**Behavior Design Maturity:** {{Nascent | Developing | Mature | Optimized}}

**Behavior Change Roadmap:**
1. {{ROADMAP_ITEM_1}}
2. {{ROADMAP_ITEM_2}}
3. {{ROADMAP_ITEM_3}}

---

## Synthesis Judgments Summary

> MUST list every AI judgment call with confidence classification and rationale per `skills/user-experience/rules/synthesis-validation.md`.

| Judgment | Classification | Confidence | Rationale |
|----------|---------------|------------|-----------|
| {{JUDGMENT_DESCRIPTION}} | {{Bottleneck diagnosis | Factor rating | Intervention recommendation}} | {{HIGH | MEDIUM | LOW}} | {{RATIONALE}} |

<!-- REPEATABLE: Add row for each AI judgment. Typical count: 10-15 entries for a complete engagement. One row per: target behavior scoping (1), each motivator pair (3), each motivation dimension (3), each simplicity factor (6), prompt classification (1), bottleneck classification (1), severity assignment (1), each intervention (3-5). -->

---

## Handoff Data

<!-- Conforms to docs/schemas/handoff-v2.schema.json + ux_ext extension (fogg-behavior-rules.md OUT-006) -->
```yaml
handoff:
  from_agent: ux-behavior-diagnostician
  to_agent: ux-heart-analyst
  task: "Establish HEART metric baselines for diagnosed behavioral bottleneck"
  success_criteria:
    - "Metric baselines established for affected HEART dimension"
    - "Target thresholds set for post-intervention measurement"
  artifacts:
    - "{{OUTPUT_FILE_PATH}}"
  key_findings:
    - "{{KEY_FINDING_1}}"
    - "{{KEY_FINDING_2}}"
    - "{{KEY_FINDING_3}}"
  blockers: []
  # Calibration: 0.5 qualitative-only (degraded mode), 0.6 default mixed evidence, 0.7 quantitative behavioral data present
  confidence: {{0.0-1.0}}
  criticality: "{{C1|C2|C3|C4}}"
  ux_ext:
    bottleneck_factor: "{{Motivation|Ability|Prompt}}"
    bottleneck_severity: "{{Critical|Major|Moderate}}"
    intervention_count: {{N}}
    affected_heart_dimension: "{{happiness|engagement|adoption|retention|task_success}}"
```

---

<!-- On-Send Protocol: Return to orchestrator (NOT persisted to file). Construct this YAML when returning results to ux-orchestrator. -->
<!--
```yaml
from_agent: ux-behavior-diagnostician
engagement_id: UX-{{NNNN}}
bottleneck_factor: {{motivation | ability | prompt | multiple}}
bottleneck_severity: {{critical | major | moderate}}
motivation_assessment:
  intrinsic: {{1-5}}
  extrinsic: {{1-5}}
  social: {{1-5}}
  overall: {{above_threshold | below_threshold}}
ability_assessment:
  limiting_factor: {{time | money | physical_effort | brain_cycles | social_deviance | non_routine}}
  limiting_score: {{1-5}}
  overall: {{above_threshold | below_threshold}}
prompt_assessment:
  type: {{facilitator | signal | spark | absent}}
  timing: {{appropriate | mistimed | absent}}
  placement: {{visible | hidden | competing}}
intervention_count: {{N}}
top_intervention: "{{description of highest-priority intervention}}"
degraded_mode: {{true | false}}
artifact_path: projects/${JERRY_PROJECT}/engagements/{{engagement-id}}/ux-behavior-diagnostician-{{topic-slug}}.md
handoff_ready: {{true | false}}
```
-->

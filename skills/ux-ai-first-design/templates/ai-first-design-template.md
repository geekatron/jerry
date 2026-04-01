<!-- TEMPLATE: ai-first-design-template.md | VERSION: 1.0.0 | DATE: 2026-03-04 -->
<!-- SKILL: /ux-ai-first-design | AGENT: ux-ai-design-guide -->
<!-- SOURCE: SKILL.md [Output Specification], SKILL.md [Methodology], agent definition [Phase 2-6] -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Use {{Option1 | Option2}} for enumerated choices. Copy REPEATABLE BLOCK markers for each judgment entry. -->

# AI-First Interaction Design Guide: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **AI Capability:** {{AI_CAPABILITY_DESCRIPTION}}
> **Date:** {{ANALYSIS_DATE}}
> **Guide:** ux-ai-design-guide

<!-- CONDITIONAL: Include the block below when operating without full AI system documentation (no analytics, no system behavioral data, no confidence distributions) per P-022 -->
<!-- > [DEGRADED MODE] This output was produced without comprehensive AI system behavioral documentation. Trust-risk and error-risk assessments are based on user-provided descriptions and available interface artifacts. Limitations: AI system determinism level estimated from qualitative descriptions; confidence availability inferred; failure mode analysis may not reflect actual system behavior; interaction pattern recommendations are directional and require empirical validation with real AI system performance data. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Trust-risk, error-risk, selected interaction pattern, human oversight level, key findings |
| [Engagement Context](#engagement-context) | L1: Product, AI capability, AI behavioral characterization, upstream inputs, CONDITIONAL verification |
| [Trust-Risk Classification](#trust-risk-classification) | L1: 4 assessment criteria with evidence, classification algorithm trace, final level |
| [Error-Risk Classification](#error-risk-classification) | L1: 4 assessment criteria with evidence, classification algorithm trace, final level |
| [Interaction Pattern Selection](#interaction-pattern-selection) | L1: 3x3 matrix reference, selected cell, pattern description, compliance notes |
| [Feedback Loop Design](#feedback-loop-design) | L1: Amershi et al. (2019) 4-phase guideline mapping with design elements |
| [Progressive Disclosure Plan](#progressive-disclosure-plan) | L1: 5 Shneiderman stages with advancement criteria and rollback conditions |
| [AI Transparency Assessment](#ai-transparency-assessment) | L1: PAIR pattern evaluation, transparency gaps, explainability recommendations |
| [Strategic Implications](#strategic-implications) | L2: AI interaction maturity, competitive analysis, trust-building roadmap |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: Every AI judgment with classification, confidence, rationale |
| [Handoff Data](#handoff-data) | L1: Structured data for /ux-inclusive-design and /ux-heuristic-eval |

---

## Executive Summary

> [REFERENCE-ONLY] AI-First Design recommendations are based on the trust-risk/error-risk framework (Yang et al., 2020, DOI: [10.1145/3313831.3376301](https://doi.org/10.1145/3313831.3376301)) and established guidelines (Amershi et al., 2019, DOI: [10.1145/3290605.3300233](https://doi.org/10.1145/3290605.3300233); Google PAIR, 2019). The AI interaction design field evolves rapidly; validate recommendations against current platform-specific guidelines and user testing before implementation.

**Trust-Risk Level:** {{HIGH | MEDIUM | LOW}} -- {{ONE_LINE_RATIONALE}}

**Error-Risk Level:** {{HIGH | MEDIUM | LOW}} -- {{ONE_LINE_RATIONALE}}

**Selected Interaction Pattern:** {{PATTERN_NAME}}

**Human Oversight Level:** {{full_oversight | advisory | human_in_loop | monitored_autonomous | autonomous}}

**Key Findings:**
1. {{KEY_FINDING_1}}
2. {{KEY_FINDING_2}}
3. {{KEY_FINDING_3}}
4. {{KEY_FINDING_4}}
5. {{KEY_FINDING_5}}

---

## Engagement Context

**Product:** {{PRODUCT_NAME}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}
**AI Capability:** {{AI_CAPABILITY_DESCRIPTION}}
**AI Technology:** {{AI_TECHNOLOGY_TYPE}}

### AI System Behavioral Characterization

| Property | Assessment | Evidence |
|----------|-----------|----------|
| Determinism level | {{Deterministic | Semi-deterministic | Non-deterministic}} | {{EVIDENCE}} |
| Confidence availability | {{Yes: system exposes confidence scores | Partial: limited confidence data | No: opaque outputs}} | {{EVIDENCE}} |
| Failure modes | {{FAILURE_MODE_DESCRIPTION}} | {{EVIDENCE}} |
| Learning behavior | {{Static: no adaptation | Supervised: learns from corrections | Self-improving: autonomous adaptation}} | {{EVIDENCE}} |

### Upstream Inputs and Evidence Inventory

| Source / Evidence Type | Available | Quality / Content |
|----------------------|-----------|-------------------|
| /ux-heuristic-eval findings | {{Yes / No}} | {{AI interface heuristic findings}} |
| /ux-behavior-design diagnosis | {{Yes / No}} | {{AI feature adoption bottleneck}} |
| AI system performance data | {{Yes / No}} | {{Direct observation | Self-reported | Inferred}} |
| User research on AI expectations | {{Yes / No}} | {{Direct observation | Self-reported | Inferred}} |
| AI interface screenshots/prototypes | {{Yes / No}} | {{Direct observation | Self-reported | Inferred}} |
| User correction/override analytics | {{Yes / No}} | {{Direct observation | Self-reported | Inferred}} |
| Competitive AI interface analysis | {{Yes / No}} | {{Direct observation | Self-reported | Inferred}} |

### Conditional Activation Verification

| Criterion | Required | Actual | Status |
|-----------|----------|--------|--------|
| Wave Scorecard Metric (WSM) | >= 7.80 | {{WSM_SCORE}} | {{PASS / FAIL}} |
| Enabler FEAT-020 (AI interaction design research) | DONE | {{DONE / IN-PROGRESS / NOT STARTED}} | {{PASS / FAIL}} |

**Overall activation:** {{PASS -- proceed with AI-First Design | FAIL -- route to /ux-heuristic-eval with PAIR protocol}}

---

## Trust-Risk Classification

<!-- Cite Yang et al. (2020) DOI:10.1145/3313831.3376301 for trust miscalibration as primary failure mode -->
### Assessment Criteria

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| Consequence of over-trust | {{catastrophic | significant | minor}} | {{EVIDENCE}} |
| Consequence of under-trust | {{significant loss | minor loss | negligible}} | {{EVIDENCE}} |
| User expertise level | {{expert | intermediate | novice}} | {{EVIDENCE}} |
| AI output verifiability | {{easily verifiable | partially verifiable | unverifiable}} | {{EVIDENCE}} |

### Classification Algorithm Trace

<!-- ALG: Rules execute sequentially; first match determines classification. Tie-breaker: higher-risk (Yang et al., 2020, DOI:10.1145/3313831.3376301). -->
| Rule | Condition | Result | Matched? |
|------|-----------|--------|----------|
| R1 | Over-trust consequence = catastrophic OR output unverifiable | HIGH | {{Yes / No}} |
| R2 | Over-trust consequence = significant AND user = novice | HIGH | {{Yes / No}} |
| R3 | Over-trust consequence = significant AND user = intermediate | MEDIUM | {{Yes / No}} |
| R4 | Over-trust consequence = minor AND output easily verifiable | LOW | {{Yes / No}} |
| Default | No above criteria met | MEDIUM (conservative) | {{Yes / No}} |

**Tie-breaker applied:** {{Yes: conflicting rules {{RULE_A}} and {{RULE_B}}; higher-risk selected | No}}
**Trust-Risk Level: {{HIGH | MEDIUM | LOW}}**
**Confidence:** {{HIGH | MEDIUM | LOW}} -- {{RATIONALE}}

---

## Error-Risk Classification

<!-- Cite Yang et al. (2020) DOI:10.1145/3313831.3376301 for error cost mismanagement as second primary failure mode -->
### Assessment Criteria

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| Reversibility | {{irreversible | reversible with significant cost | easily reversible}} | {{EVIDENCE}} |
| Blast radius | {{organization-wide | team/group | individual only}} | {{EVIDENCE}} |
| Error detection latency | {{immediate | delayed | hidden}} | {{EVIDENCE}} |
| Recovery cost | {{high | moderate | low}} | {{EVIDENCE}} |

### Classification Algorithm Trace

<!-- ALG: Rules execute sequentially; first match determines classification. Tie-breaker: higher-risk (Yang et al., 2020, DOI:10.1145/3313831.3376301). -->
| Rule | Condition | Result | Matched? |
|------|-----------|--------|----------|
| R1 | Irreversible AND blast radius = organization-wide | HIGH | {{Yes / No}} |
| R2 | Irreversible AND detection = hidden | HIGH | {{Yes / No}} |
| R3 | Reversible with significant cost AND blast radius = team/group | MEDIUM | {{Yes / No}} |
| R4 | Easily reversible AND blast radius = individual | LOW | {{Yes / No}} |
| Default | No above criteria met | MEDIUM (conservative) | {{Yes / No}} |

**Tie-breaker applied:** {{Yes: conflicting rules {{RULE_A}} and {{RULE_B}}; higher-risk selected | No}}
**Error-Risk Level: {{HIGH | MEDIUM | LOW}}**
**Confidence:** {{HIGH | MEDIUM | LOW}} -- {{RATIONALE}}

---

## Interaction Pattern Selection

### 3x3 Trust-Risk x Error-Risk Matrix

> **Provenance note:** The 3x3 trust-risk x error-risk interaction pattern matrix below is the authors' operationalization synthesizing Yang et al.'s (2020) conceptual framework into actionable design patterns. The cell labels and pattern descriptions are derived, not verbatim Yang et al. constructs.

| | LOW Error-Risk | MEDIUM Error-Risk | HIGH Error-Risk |
|---|---|---|---|
| **HIGH Trust-Risk** | AI autonomous with periodic review | AI advisor with mandatory review | Full human oversight, AI as information provider only |
| **MEDIUM Trust-Risk** | AI autonomous with user correction | Human-in-the-loop with AI assistance | Human-controlled with AI safety checks |
| **LOW Trust-Risk** | AI fully autonomous (low stakes) | AI suggests with easy override | AI assists with mandatory human verification |

### Selected Pattern

**Matrix cell:** {{HIGH | MEDIUM | LOW}} Trust-Risk x {{HIGH | MEDIUM | LOW}} Error-Risk
**Pattern name:** {{PATTERN_NAME}}
**Pattern description:** {{PATTERN_DESCRIPTION}}

**Design elements:** UI components: {{UI_COMPONENTS}}; Oversight mechanisms: {{OVERSIGHT_MECHANISMS}}; Automation level: {{AUTOMATION_LEVEL}}

**Technical constraints:** {{Does the AI system support the required human oversight mechanism? Detail constraints.}}

**Deviation from matrix:** {{None -- matrix recommendation applied directly | Deviation: selected adjacent cell with higher human oversight due to {{CONSTRAINT_DESCRIPTION}}}}
**"Never lower oversight" compliance:** {{COMPLIANT -- no deviation lowers human oversight | N/A -- no deviation}}

---

## Feedback Loop Design

> [REFERENCE-ONLY] Feedback loop design elements are based on Amershi et al.'s (2019) 18 guidelines for human-AI interaction. Validate against current platform-specific guidelines before implementation.

<!-- Cite specific guideline IDs (G1-G18) per Amershi et al. (2019) DOI:10.1145/3290605.3300233. Each row covers one guideline. -->

| Phase | ID | Guideline | Compliance | Design Element |
|-------|-----|-----------|------------|----------------|
| Initially | G1 | Make clear what the system can do | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| Initially | G2 | Make clear how well the system can do it | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| During | G3 | Time services based on context | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| During | G4 | Show contextually relevant information | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| During | G5 | Match relevant social norms | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| During | G6 | Mitigate social biases | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| During | G7 | Support efficient invocation and dismissal | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| During | G8 | Make clear why the system did what it did | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| When wrong | G9 | Support efficient correction | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| When wrong | G10 | Scope services when in doubt | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| When wrong | G11 | Make clear how to invoke or dismiss | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| When wrong | G12 | Make clear how to provide feedback | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| When wrong | G13 | Support efficient error recovery | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| Over time | G14 | Learn from user behavior | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| Over time | G15 | Update and adapt cautiously | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| Over time | G16 | Encourage granular feedback | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| Over time | G17 | Convey consequences of user actions | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |
| Over time | G18 | Provide global controls | {{Addressed | Gap}} | {{DESIGN_ELEMENT}} |

---

## Progressive Disclosure Plan

> [REFERENCE-ONLY] Duration estimates are heuristic starting points derived from typical enterprise adoption patterns (Shneiderman, 2020). Adjust based on domain risk profile, user sophistication, and observed trust-building velocity.

| Stage | Trust Level | AI Autonomy | User Control | Duration | Advancement Criteria | Rollback Trigger |
|-------|-------------|-------------|-------------|----------|---------------------|-----------------|
| 1: Introduction | Minimal | AI explains only; no actions | Full user control | {{DURATION}} | {{CRITERIA}} | {{ROLLBACK_TRIGGER}} |
| 2: Suggestion | Growing | AI suggests; user decides | Accept/reject controls | {{DURATION}} | {{CRITERIA}} | {{ROLLBACK_TRIGGER}} |
| 3: Collaboration | Established | AI drafts; user edits and approves | Edit + approve workflow | {{DURATION}} | {{CRITERIA}} | {{ROLLBACK_TRIGGER}} |
| 4: Delegation | High | AI acts; user monitors and corrects | Monitoring dashboard + undo | {{DURATION}} | {{CRITERIA}} | {{ROLLBACK_TRIGGER}} |
| 5: Autonomy | Full | AI operates independently within bounds | Exception-only intervention | {{DURATION}} | {{CRITERIA}} | {{ROLLBACK_TRIGGER}} |

**Stage 5 eligibility:** {{Eligible -- error-risk permits full autonomy with explicit user opt-in | Not eligible -- {{REASON}}}}

**Advancement requirements (all stages):** Minimum time at current stage (no instant escalation); user explicitly opts in (never automatic); error rate below threshold (< 5% LOW, < 2% MEDIUM, < 0.5% HIGH error-risk; team-defined); user demonstrates correction capability at current stage.

---

## AI Transparency Assessment

<!-- Cite Google PAIR (2019) People + AI Guidebook for transparency and explainability patterns -->

| PAIR Pattern | Applicable? | Current State | Recommendation |
|-------------|------------|---------------|----------------|
| Explain AI's confidence | {{Yes / No}} | {{CURRENT_STATE}} | {{RECOMMENDATION}} |
| Explain AI's reasoning | {{Yes / No}} | {{CURRENT_STATE}} | {{RECOMMENDATION}} |
| Show example-based explanations | {{Yes / No}} | {{CURRENT_STATE}} | {{RECOMMENDATION}} |
| Provide user control over AI behavior | {{Yes / No}} | {{CURRENT_STATE}} | {{RECOMMENDATION}} |
| Allow graceful degradation | {{Yes / No}} | {{CURRENT_STATE}} | {{RECOMMENDATION}} |

### Transparency Gaps

| Gap | Severity | Affected Phase | Recommendation |
|-----|----------|---------------|----------------|
| {{GAP_DESCRIPTION}} | {{High | Medium | Low}} | {{Initially | During | When wrong | Over time}} | {{RECOMMENDATION}} |

**Confidence Communication Design:** {{HOW_THE_AI_CONVEYS_CERTAINTY_UNCERTAINTY}}

---

## Strategic Implications

**AI Interaction Design Maturity:** {{Nascent | Developing | Established | Mature}}
**Competitive Analysis:** {{COMPETITIVE_ANALYSIS}}
**Organizational Readiness for Increased AI Autonomy:** {{READINESS_ASSESSMENT}}

**Trust-Building Roadmap:**
1. {{ROADMAP_MILESTONE_1}}
2. {{ROADMAP_MILESTONE_2}}
3. {{ROADMAP_MILESTONE_3}}

**AI Capability Progression Strategy:** {{PROGRESSION_STRATEGY}}

---

## Synthesis Judgments Summary

> MUST list every AI judgment call with confidence classification and rationale per `skills/user-experience/rules/synthesis-validation.md`.

| Judgment | Classification | Confidence | Rationale |
|----------|---------------|------------|-----------|
| {{JUDGMENT_DESCRIPTION}} | {{Trust-risk | Error-risk | Pattern selection | Feedback loop | Progressive disclosure | Transparency}} | {{HIGH | MEDIUM | LOW}} | {{RATIONALE}} |

<!-- REPEATABLE BLOCK: Add row for each AI judgment. Typical count: 12-18 entries for a complete engagement. One row per: AI capability characterization (1), each trust-risk criterion (4), trust-risk classification (1), each error-risk criterion (4), error-risk classification (1), interaction pattern selection (1), each feedback loop phase design (4), progressive disclosure stage definitions (1-5), each transparency gap (varies). All interaction pattern recommendations MUST carry LOW confidence. -->

<!-- EXAMPLE (delete before use): -->
<!-- | Trust-risk: consequence of over-trust = significant | Trust-risk | MEDIUM | User-provided description indicates costly but not safety-critical consequences; no AI system performance data available to confirm | -->
<!-- | Interaction pattern: human-in-the-loop selected | Pattern selection | LOW | Matrix cell MEDIUM x MEDIUM selects HITL; AI design patterns are rapidly evolving and require empirical validation | -->

---

## Handoff Data

<!-- Conforms to docs/schemas/handoff-v2.schema.json + ux_ext extension -->
<!-- Confidence calibration: 0.4 no AI system data, 0.5 default mixed evidence, 0.6 quantitative AI performance data -->

### Handoff to /ux-inclusive-design

```yaml
handoff:
  from_agent: ux-ai-design-guide
  to_agent: ux-inclusive-evaluator
  task: "Audit AI interface patterns for WCAG 2.2 compliance and cognitive accessibility"
  success_criteria:
    - "AI explanation mechanisms evaluated for screen reader compatibility"
    - "AI controls assessed for keyboard navigation"
    - "Progressive disclosure stages reviewed for cognitive accessibility"
  artifacts:
    - "{{OUTPUT_FILE_PATH}}"
  key_findings:
    - "Trust-risk: {{HIGH | MEDIUM | LOW}}; Error-risk: {{HIGH | MEDIUM | LOW}}"
    - "Interaction pattern: {{PATTERN_NAME}}"
    - "Human oversight level: {{full_oversight | advisory | human_in_loop | monitored_autonomous | autonomous}}"
  blockers: []
  confidence: {{0.0-1.0}}
  criticality: "{{C1 | C2 | C3 | C4}}"
  ux_ext:
    trust_risk_level: "{{HIGH | MEDIUM | LOW}}"
    error_risk_level: "{{HIGH | MEDIUM | LOW}}"
    interaction_pattern: "{{PATTERN_NAME}}"
    ai_capability_type: "{{generative | classificatory | decisional | recommendatory}}"
    feedback_loop_design:
      initially: "{{ONBOARDING_DESIGN_SUMMARY}}"
      during_interaction: "{{REALTIME_FEEDBACK_SUMMARY}}"
      when_wrong: "{{ERROR_RECOVERY_SUMMARY}}"
      over_time: "{{ADAPTATION_STRATEGY_SUMMARY}}"
    human_oversight_level: "{{full_oversight | advisory | human_in_loop | monitored_autonomous | autonomous}}"
```

### Handoff to /ux-heuristic-eval

```yaml
handoff:
  from_agent: ux-ai-design-guide
  to_agent: ux-heuristic-evaluator
  task: "Evaluate AI interaction patterns against Nielsen's 10 heuristics plus AI-specific supplement"
  success_criteria:
    - "AI interaction patterns evaluated against all 10 Nielsen heuristics"
    - "AI-specific heuristics applied: transparency, controllability, error recovery, feedback quality"
    - "Severity ratings assigned per finding with AI context"
  artifacts:
    - "{{OUTPUT_FILE_PATH}}"
  key_findings:
    - "Trust-risk: {{HIGH | MEDIUM | LOW}}; Error-risk: {{HIGH | MEDIUM | LOW}}"
    - "Interaction pattern: {{PATTERN_NAME}}"
    - "AI transparency gaps identified: {{GAP_COUNT}}"
  blockers: []
  confidence: {{0.0-1.0}}
  criticality: "{{C1 | C2 | C3 | C4}}"
  ux_ext:
    trust_risk_level: "{{HIGH | MEDIUM | LOW}}"
    error_risk_level: "{{HIGH | MEDIUM | LOW}}"
    interaction_pattern: "{{PATTERN_NAME}}"
    ai_specific_heuristics:
      - "AI transparency: does the system explain what it can do and how well?"
      - "AI controllability: can the user adjust, override, or dismiss AI outputs?"
      - "AI error recovery: does the system help users recover from AI errors?"
      - "AI feedback quality: does the system communicate confidence and uncertainty?"
```

**AI Staleness Risk Disclosure (P-022):** The field of human-AI interaction design is rapidly evolving. Training data may not reflect the latest AI interaction paradigms, platform-specific guidelines (e.g., Apple Intelligence HIG, Google Gemini UX), or emerging best practices for agentic AI, multi-modal AI, or autonomous agent interfaces. Validate all recommendations against current platform guidelines and real user behavior before implementation.

---

<!-- On-Send Protocol: Return to orchestrator (NOT persisted to file). Construct this YAML when returning results to ux-orchestrator. -->
<!--
```yaml
from_agent: ux-ai-design-guide
engagement_id: UX-{{NNNN}}
trust_risk_level: {{HIGH | MEDIUM | LOW}}
error_risk_level: {{HIGH | MEDIUM | LOW}}
interaction_pattern: "{{selected pattern name from 3x3 matrix}}"
ai_capability_type: {{generative | classificatory | decisional | recommendatory}}
feedback_loop_design:
  initially: "{{onboarding design summary}}"
  during_interaction: "{{real-time feedback summary}}"
  when_wrong: "{{error recovery summary}}"
  over_time: "{{adaptation strategy summary}}"
human_oversight_level: {{full_oversight | advisory | human_in_loop | monitored_autonomous | autonomous}}
progressive_disclosure_plan:
  total_stages: {{5}}
  current_recommended_start_stage: {{1-5}}
  stage_5_eligible: {{true | false}}
synthesis_judgments_count: {{N}}
degraded_mode: {{true | false}}
artifact_path: projects/${JERRY_PROJECT}/engagements/{{engagement-id}}/ux-ai-design-guide-{{topic-slug}}.md
handoff_ready: {{true | false}}
```
-->

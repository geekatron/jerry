# FEAT-003:DISC-002: Adversarial Prompting Protocol for Quality Gates

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-31 (FEAT-005 feedback loop design)
PURPOSE: Document the adversarial prompting strategy for quality gate evaluation
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-31T01:00:00Z
> **Completed:** 2026-01-31T01:30:00Z
> **Parent:** FEAT-003
> **Owner:** Claude
> **Source:** FEAT-005 adversarial feedback loop design session

---

## Summary

This discovery documents the **adversarial prompting protocol** for quality gate evaluation in Jerry workflows. The protocol transforms the constructive `ps-critic` agent into an adversarial evaluator that actively seeks flaws, enforces strict checklist compliance, and prevents rubber-stamp approvals.

**Key Findings:**
- Current ps-critic uses "constructive" tone, unsuitable for adversarial compliance evaluation
- Adversarial evaluation requires explicit prompting patterns (red team framing, mandatory findings)
- Invocation-time prompting is the cleanest approach (no agent modification required)
- Six key adversarial patterns identified for quality gate enforcement

**Validation:** Documented and pending implementation validation in EN-020

---

## Context

### Background

During FEAT-005 orchestration planning, we identified that quality gates require adversarial evaluation to be effective. The current `ps-critic` agent (v2.2.0) is designed for Self-Refine iterative improvement loops with a "constructive" communication style. This is appropriate for helping generators improve, but inappropriate for compliance gates where the goal is to **find non-compliance**, not **help achieve compliance**.

### Research Question

**How do we prompt the ps-critic agent to behave as an adversarial evaluator rather than a constructive helper?**

Sub-questions:
1. What adversarial prompting patterns exist in industry?
2. What specific techniques force rigorous evaluation?
3. How do we prevent rubber-stamp approvals?
4. How do we integrate with ORCHESTRATION.yaml?

### Investigation Approach

1. Analyzed current ps-critic agent definition (v2.2.0)
2. Researched adversarial evaluation patterns in LLM literature
3. Identified gaps between constructive and adversarial evaluation
4. Designed specific prompting techniques for quality gates
5. Documented integration with orchestration workflow

---

## Finding

### Current State Analysis (ps-critic v2.2.0)

**Agent Framing:**
```yaml
persona:
  tone: "analytical"
  communication_style: "constructive"  # ← NOT adversarial

identity:
  role: "Quality Evaluator"
  expertise:
    - "Constructive feedback generation"  # ← Helpful, not challenging
```

**Problem:** The agent is primed to be helpful and constructive, which creates a bias toward:
- Finding positives before negatives
- Suggesting improvements rather than citing failures
- Giving benefit of the doubt on marginal compliance
- Avoiding harsh assessments that might seem "unfair"

### Adversarial Prompting Protocol

The following six patterns transform constructive evaluation into adversarial evaluation:

---

#### Pattern 1: Red Team Framing

**Purpose:** Establish adversarial mindset from the start

**Prompt Template:**
```markdown
## ADVERSARIAL EVALUATION MODE

You are operating as an ADVERSARIAL CRITIC, not a constructive reviewer.

**Mindset:** Assume problems EXIST until proven otherwise. Your job is to
FIND flaws, not validate work. A "clean" review with no findings is
SUSPICIOUS and requires explicit justification.

**Your role:** RED TEAM evaluator stress-testing for compliance gaps.

**Behavioral Rules:**
- You are NOT trying to help the work succeed
- You ARE trying to find every way it could fail
- Treat this like a security audit, not a peer review
- If something "probably" meets a criterion, it FAILS (no benefit of doubt)
```

**Rationale:** This framing overrides the default "helpful assistant" behavior that biases toward approval.

---

#### Pattern 2: Mandatory Findings Quota

**Purpose:** Prevent rubber-stamp approvals

**Prompt Template:**
```markdown
## FINDINGS REQUIREMENT

You MUST identify:
- At least 3 issues per deliverable (any severity: CRITICAL, MAJOR, or MINOR)
- If you find zero CRITICAL issues, you must justify WHY with specific evidence
- If you find zero issues total, this is a RED FLAG requiring explicit explanation

**Severity Definitions:**
| Severity | Definition | Example |
|----------|------------|---------|
| CRITICAL | Blocks compliance, must fix | Missing required section |
| MAJOR | Significantly impacts quality | Section exists but incomplete |
| MINOR | Improvement opportunity | Formatting, clarity issues |

**Perfect Score Justification:**
A review scoring 1.0 (perfect) or finding zero issues MUST include:
1. Explicit statement that adversarial analysis was performed
2. List of 3+ specific areas examined for issues
3. Evidence citations for why each potential issue was NOT an actual issue
```

**Rationale:** Without mandatory findings, reviewers tend toward the path of least resistance (approval).

---

#### Pattern 3: Devil's Advocate Protocol

**Purpose:** Force active challenge of claims

**Prompt Template:**
```markdown
## DEVIL'S ADVOCATE PROTOCOL

For EACH major section or claim in the deliverable, you MUST answer:

1. **What could make this WRONG?**
   - Identify at least one assumption that could be invalid

2. **What edge case was NOT considered?**
   - Identify at least one scenario not addressed

3. **What happens if this FAILS?**
   - Identify the failure mode and its impact

4. **What alternative was NOT evaluated?**
   - Identify at least one approach not considered

Document at least ONE challenge per major section in the deliverable.

**Output Format:**
| Section | Challenge Type | Challenge Description | Severity |
|---------|---------------|----------------------|----------|
| {section} | Assumption Risk | {what could be wrong} | {severity} |
```

**Rationale:** This forces systematic challenge rather than passive acceptance.

---

#### Pattern 4: Checklist Enforcement (No Partial Credit)

**Purpose:** Binary compliance verification with evidence

**Prompt Template:**
```markdown
## CHECKLIST ENFORCEMENT

For each checklist item (e.g., A-001 through A-043):

| Status | Requirement | Evidence Standard |
|--------|-------------|-------------------|
| ✅ PASS | Criterion fully met | Quote EXACT text/evidence from deliverable |
| ❌ FAIL | Criterion not met | Describe SPECIFIC gap with section reference |
| ⚠️ WEAK | Partial compliance | Cite what exists AND what's missing |

**Rules:**
- "Probably compliant" = ❌ FAIL (no benefit of doubt)
- "Mentioned but not detailed" = ⚠️ WEAK at best
- "Implied but not explicit" = ❌ FAIL
- PASS requires QUOTABLE evidence, not inference

**Evidence Format:**
For each PASS, provide:
```
Checklist: {ID}
Status: PASS
Evidence: "{exact quote from deliverable}"
Location: {section/line reference}
```

For each FAIL, provide:
```
Checklist: {ID}
Status: FAIL
Gap: {what is missing or wrong}
Expected: {what compliance would look like}
Location: {where it should appear}
```
```

**Rationale:** Strict evidence requirements prevent subjective "close enough" assessments.

---

#### Pattern 5: Counter-Example Seeking

**Purpose:** Force identification of failure scenarios

**Prompt Template:**
```markdown
## COUNTER-EXAMPLE REQUIREMENTS

For each architectural decision, pattern, or recommendation in the deliverable:

1. **Failure Scenario:** Provide ONE realistic scenario where this approach FAILS
2. **Unconsidered Alternative:** Name ONE alternative approach that was NOT evaluated
3. **Unaddressed Risk:** Identify ONE risk that is NOT mentioned in the deliverable

**Output Format:**
| Decision/Pattern | Failure Scenario | Unconsidered Alternative | Unaddressed Risk |
|------------------|------------------|-------------------------|------------------|
| {decision} | {how it fails} | {what else could work} | {what could go wrong} |

**Minimum:** At least 3 rows in this table (one per major decision)

**Note:** Even GOOD decisions have trade-offs. The absence of counter-examples
indicates insufficient analysis, not perfect design.
```

**Rationale:** Forces acknowledgment that no solution is perfect.

---

#### Pattern 6: Score Calibration

**Purpose:** Prevent grade inflation

**Prompt Template:**
```markdown
## SCORE CALIBRATION

**Score Interpretation (Adversarial Mode):**
| Score Range | Meaning | Expected Frequency |
|-------------|---------|-------------------|
| 0.95 - 1.00 | Exceptional - zero issues found | < 5% of reviews |
| 0.85 - 0.94 | Strong - minor issues only | 15-20% of reviews |
| 0.70 - 0.84 | Acceptable - some issues need attention | 40-50% of reviews |
| 0.50 - 0.69 | Needs Work - significant gaps | 20-30% of reviews |
| 0.00 - 0.49 | Major Revision Required | 10-15% of reviews |

**Calibration Rules:**
- First-pass submissions should typically score 0.60-0.80
- Scores above 0.90 require explicit justification
- Perfect scores (1.0) should be RARE and heavily documented
- If your scores consistently average > 0.85, you are being too lenient

**Score Justification Required for:**
- Any score >= 0.95 (explain why exceptional)
- Any score <= 0.30 (explain severity of issues)
- Score improvement > 0.20 between iterations (explain what changed)
```

**Rationale:** Without calibration guidance, scores drift toward approval.

---

### Integration with ORCHESTRATION.yaml

The adversarial prompting protocol should be stored in the ORCHESTRATION.yaml for consistent invocation:

```yaml
feedback_loop:
  enabled: true
  max_iterations: 3
  escalation_on_failure: true
  critique_artifact_dir: "orchestration/critiques"

  # Adversarial prompting configuration
  adversarial_protocol:
    enabled: true
    version: "1.0.0"

    # Red Team Framing
    framing: |
      You are operating as an ADVERSARIAL CRITIC, not a constructive reviewer.
      Assume problems EXIST until proven otherwise. Your job is to FIND flaws,
      not validate work.

    # Mandatory Findings
    minimum_findings: 3
    perfect_score_threshold: 0.95
    perfect_score_requires_justification: true

    # Checklist Enforcement
    checklist_evidence_required: true
    partial_credit_allowed: false

    # Counter-Examples
    counter_examples_required: true
    min_counter_examples: 3

    # Score Calibration
    expected_first_pass_range: [0.60, 0.80]
    high_score_justification_threshold: 0.90
```

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Agent Definition | ps-critic v2.2.0 showing constructive framing | skills/problem-solving/agents/ps-critic.md | 2026-01-31 |
| E-002 | Prior Art | Anthropic Constitutional AI red-teaming | https://www.anthropic.com/research/constitutional-ai | 2023 |
| E-003 | Prior Art | DeepEval LLM-as-Judge framework | https://deepeval.com/docs/metrics-llm-evals | 2024 |
| E-004 | Industry Practice | Red team/blue team in AI safety | OpenAI, Anthropic papers | 2023-2024 |

### Reference Material

**Constitutional AI Red-Teaming:**
- Source: Anthropic Research
- Relevance: Demonstrates adversarial evaluation of AI outputs using explicit criteria

**LLM-as-a-Judge:**
- Source: DeepEval, RAGAS frameworks
- Relevance: Shows structured evaluation with explicit rubrics and evidence requirements

---

## Implications

### Impact on Project

1. **FEAT-005 Quality Gates** - Adversarial prompting makes feedback loops effective
2. **Orchestration Design** - YAML needs to store prompting configuration
3. **Future Compliance Work** - Pattern reusable across Jerry skills

### Design Decisions Affected

- **Decision:** Prompting approach (invocation-time vs. agent modification)
  - **Impact:** Favors invocation-time prompting (Option C from EN-020)
  - **Rationale:** Cleanest approach, no skill modification required, configuration-driven

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Over-aggressive finding of false positives | Medium | Calibration guidance and iteration limits |
| Inconsistent application across invocations | Medium | Store protocol in ORCHESTRATION.yaml |
| Prompting overhead in each invocation | Low | Template-based prompt construction |

---

## Relationships

### Creates

- [EN-020: Adversarial Critic Agents](./EN-020-adversarial-critic-agents/EN-020-adversarial-critic-agents.md) - Implementation enabler

### Informs

- [FEAT-005 Orchestration Plan](../../FEAT-005-skill-compliance/orchestration/ORCHESTRATION_PLAN.md) - Quality gate design
- [FEAT-005 ORCHESTRATION.yaml](../../FEAT-005-skill-compliance/orchestration/ORCHESTRATION.yaml) - Configuration storage

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Agent Definition | skills/problem-solving/agents/ps-critic.md | Current agent to augment |
| Orchestration | FEAT-005/orchestration/ORCHESTRATION_PLAN.md | Feedback loop design |

---

## Recommendations

### Immediate Actions

1. **Update ORCHESTRATION_PLAN.md** - Add adversarial prompting protocol section
2. **Update ORCHESTRATION.yaml** - Add `adversarial_protocol` configuration
3. **Create prompt templates** - Reusable templates for each quality gate

### Long-term Considerations

- Consider formal `ps-critic-adversarial` agent variant if pattern proves valuable
- Explore adversarial evaluation for nasa-se agents (nse-reviewer, nse-validator)
- Build metrics dashboard to track evaluation effectiveness

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-31 | Claude | Created discovery documenting adversarial prompting protocol |

---

## Metadata

```yaml
id: "FEAT-003:DISC-002"
parent_id: "FEAT-003"
work_type: DISCOVERY
title: "Adversarial Prompting Protocol for Quality Gates"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-31T01:00:00Z"
updated_at: "2026-01-31T01:30:00Z"
completed_at: "2026-01-31T01:30:00Z"
tags: [adversarial, prompting, quality-gates, ps-critic, feedback-loop]
source: "FEAT-005 adversarial feedback loop design session"
finding_type: PATTERN
confidence_level: HIGH
validated: false
```

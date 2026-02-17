# TASK-006: Updated orch-synthesizer Agent Spec (Adversarial Synthesis)

<!--
DOCUMENT-ID: FEAT-004:EN-307:TASK-006
VERSION: 1.0.0
AGENT: ps-architect-307
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-307 (Orchestration Skill Enhancement - Adversarial Loops)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DEVELOPMENT
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-307
> **Quality Target:** >= 0.92
> **Purpose:** Define the updated orch-synthesizer agent spec (v3.0.0) with adversarial-aware synthesis capabilities

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this spec update delivers |
| [Change Summary](#change-summary) | Delta from v2.1.0 to v3.0.0 |
| [Updated YAML Frontmatter](#updated-yaml-frontmatter) | New frontmatter fields |
| [Updated Identity Section](#updated-identity-section) | New expertise areas |
| [Adversarial Synthesis Protocol](#adversarial-synthesis-protocol) | New protocol for adversarial-aware synthesis |
| [Updated Output Format](#updated-output-format) | New adversarial sections in synthesis document |
| [Updated Invocation Template](#updated-invocation-template) | New invocation constraints |
| [Updated Validation Section](#updated-validation-section) | New post-completion checks |
| [Full Spec Diff](#full-spec-diff) | Complete list of changes |
| [Traceability](#traceability) | Mapping to requirements |
| [References](#references) | Source citations |

---

## Summary

This document defines the updated orch-synthesizer agent specification (v3.0.0) with adversarial-aware synthesis capabilities. The orch-synthesizer creates the final synthesis document for completed workflows. With this enhancement, it gains:

- **Adversarial review summary** as a first-class synthesis section (FR-307-019)
- **Quality score trend analysis** showing improvement across iterations (FR-307-020)
- **Cross-pipeline adversarial pattern extraction** identifying systemic issues (FR-307-021)
- **Strategy effectiveness reporting** for calibration feedback (FR-307-022)
- **Residual risk documentation** for accepted/deferred findings (FR-307-023)
- **Lessons learned** from the adversarial review process itself (FR-307-024)

The synthesis becomes a comprehensive record of both the workflow outcomes AND the quality assurance process that validated those outcomes.

---

## Change Summary

### v2.1.0 to v3.0.0 Delta

| Component | v2.1.0 | v3.0.0 | Change Type |
|-----------|--------|--------|-------------|
| version | 2.1.0 | 3.0.0 | Major version bump |
| identity.expertise | 6 items | 10 items | Added 4 adversarial synthesis entries |
| identity.modes | 2 modes | 2 modes (enhanced) | Adversarial content in both modes |
| NEW: adversarial_synthesis_protocol | -- | Full protocol | New section |
| output format | Standard synthesis | Extended with 6 adversarial sections | Major extension |
| synthesis_protocol | 5 steps | 8 steps | 3 new adversarial steps |
| validation.post_completion_checks | 5 checks | 9 checks | Added 4 adversarial checks |

---

## Updated YAML Frontmatter

```yaml
---
name: orch-synthesizer
version: "3.0.0"
description: >-
  Orchestration Synthesizer agent for cross-document synthesis, pattern extraction,
  adversarial review summarization, quality trend analysis, and final workflow recommendations
model: sonnet

identity:
  role: "Orchestration Synthesizer"
  expertise:
    - "Cross-document synthesis"
    - "Pattern extraction and theme identification"
    - "Workflow summarization"
    - "Evidence-based recommendations"
    - "Artifact consolidation"
    - "Knowledge graph construction"
    # NEW v3.0.0:
    - "Adversarial review summarization"
    - "Quality score trend analysis"
    - "Strategy effectiveness evaluation"
    - "Residual risk documentation"
  cognitive_mode: "mixed"
  modes:
    divergent: "Explore all artifacts including adversarial critiques, identify quality patterns"
    convergent: "Consolidate findings and quality metrics into actionable synthesis"
---
```

---

## Updated Identity Section

```xml
<identity>
You are **orch-synthesizer**, a specialized Orchestration Synthesizer agent in the Jerry framework.

**Role:** Orchestration Synthesizer - Expert in cross-document synthesis, pattern extraction, adversarial review summarization, and creating coherent recommendations from multi-phase workflow artifacts.

**Expertise:**
- Cross-document synthesis and consolidation
- Pattern extraction and theme identification
- Evidence-based recommendation generation
- Artifact registry construction
- Knowledge graph building from disparate sources
- Strategic implication analysis
- **[NEW v3.0.0] Adversarial review summarization and quality trend analysis**
- **[NEW v3.0.0] Strategy effectiveness evaluation across workflows**
- **[NEW v3.0.0] Residual risk identification and documentation**
- **[NEW v3.0.0] Lessons learned extraction from adversarial review processes**

**Cognitive Mode:** Mixed
- **Divergent:** Explore all artifacts including adversarial critique outputs, identify quality patterns, extract recurring findings across iterations
- **Convergent:** Consolidate workflow findings AND quality assurance evidence into coherent, actionable synthesis

**Orchestration Role:**
| Phase | Activity |
|-------|----------|
| Workflow Completion | Triggered when all phases COMPLETE |
| Synthesis | Aggregate all pipeline artifacts |
| Pattern Extraction | Identify cross-cutting themes |
| **Adversarial Summary** | **Summarize quality review process and outcomes** |
| **Quality Analysis** | **Analyze score trends and strategy effectiveness** |
| Recommendation | Generate evidence-based actions |
</identity>
```

---

## Adversarial Synthesis Protocol

This is a new protocol section added to the orch-synthesizer spec:

```xml
<adversarial_synthesis_protocol>
## Adversarial Synthesis Protocol

### Step A1: Gather Adversarial Artifacts

In addition to standard artifacts, read:
1. All critic output artifacts (critique reports per iteration)
2. All revision output artifacts (showing how findings were addressed)
3. All validation reports (ps-validator verdicts)
4. Iteration scores from ORCHESTRATION.yaml (metrics.quality)
5. Finding resolution tracking from iteration entries

### Step A2: Build Adversarial Review Summary (FR-307-019)

Create a summary table of the adversarial review process:

```markdown
## Adversarial Review Summary

| Enabler | Iterations | Iter 1 Score | Iter 2 Score | Final Score | Verdict | Key Findings |
|---------|-----------|-------------|-------------|-------------|---------|--------------|
| EN-302 | 2 of 3 | 0.79 | 0.935 | 0.935 | COND. PASS | 3 blocking, 5 major |
| EN-303 | 2 of 3 | 0.79 | 0.928 | 0.928 | PASS | 3 blocking, 5 major |
```

### Step A3: Quality Score Trend Analysis (FR-307-020)

Analyze how quality scores improved across iterations:

```markdown
### Quality Score Trends

| Enabler | Iter 1 | Iter 2 | Delta | Improvement Rate |
|---------|--------|--------|-------|------------------|
| EN-302 | 0.79 | 0.935 | +0.145 | 18.4% |
| EN-303 | 0.79 | 0.928 | +0.138 | 17.5% |

**Average improvement per iteration:** +0.142 (17.9%)
**Iterations to threshold:** 2 average (vs 3 maximum)
```

### Step A4: Cross-Pipeline Pattern Extraction (FR-307-021)

Identify adversarial findings that recur across pipelines:

```markdown
### Cross-Pipeline Adversarial Patterns

| Pattern | Pipelines Affected | Frequency | Systemic? | Recommendation |
|---------|-------------------|-----------|-----------|----------------|
| Missing traceability | ADV, ENF | 4 of 6 enablers | Yes | Add traceability template |
| Vague acceptance criteria | ADV | 2 of 3 enablers | Partial | Strengthen AC standards |
```

Patterns appearing in 50%+ of enablers across different pipelines are flagged as systemic.

### Step A5: Strategy Effectiveness Report (FR-307-022)

Report which adversarial strategies produced the most impactful findings:

```markdown
### Strategy Effectiveness

| Strategy | Times Used | Findings Produced | Blocking Findings | Effectiveness Rating |
|----------|-----------|-------------------|-------------------|---------------------|
| S-002 Devil's Advocate | 6 | 12 | 3 | HIGH |
| S-007 Constitutional AI | 4 | 8 | 2 | HIGH |
| S-014 LLM-as-Judge | 8 | N/A (scoring) | N/A | ESSENTIAL |
| S-012 FMEA | 2 | 4 | 1 | MEDIUM |

**Most effective for architecture artifacts:** S-002 Devil's Advocate
**Most effective for requirements:** S-007 Constitutional AI
**Recommendation for future workflows:** Prioritize S-002 and S-007 at iteration 1
```

### Step A6: Residual Risk Documentation (FR-307-023)

Document findings that were accepted (CONDITIONAL PASS) or deferred:

```markdown
### Residual Risks

| Risk ID | Source | Severity | Finding | Status | Mitigation |
|---------|--------|----------|---------|--------|------------|
| RR-001 | EN-302 iter 2 | MINOR | Incomplete edge case coverage | ACCEPTED | Address in implementation phase |
| RR-002 | EN-402 iter 2 | MINOR | Missing performance benchmarks | DEFERRED | Add to tech debt backlog |
```

### Step A7: Lessons Learned (FR-307-024)

Extract process-level lessons:

```markdown
### Adversarial Process Lessons Learned

| Lesson | Evidence | Recommendation |
|--------|----------|----------------|
| S-002 at iteration 1 catches most blocking issues | 8/10 blocking findings from iter 1 | Keep S-002 as default iter 1 strategy |
| C3 criticality adequate for ADR artifacts | All ADRs passed at iter 2 | No escalation to C4 needed for ADRs |
| 2 iterations sufficient for research artifacts | Average iter-to-pass: 1.8 | Consider reducing min to 2 for TGT-RES |
| Anti-leniency calibration effective | Score variance < 0.05 between critics | Maintain calibration requirement |
```
</adversarial_synthesis_protocol>
```

---

## Updated Output Format

### Final Synthesis Document (Extended)

The synthesis document now includes six new adversarial sections after the standard L1 Technical Summary:

```markdown
# {Workflow Name}: Final Synthesis

> **Document ID:** {PROJECT_ID}-SYNTH-FINAL
> **Date:** {date}
> **Workflow:** {workflow_id}
> **Status:** COMPLETE

---

## L0: Executive Summary

{Standard 1-2 paragraph summary}

**Quality Assurance:** {summary of adversarial review - iterations, scores, verdicts}

---

## L1: Technical Summary

### Key Findings
{Standard findings table with artifact citations}

### Cross-Cutting Patterns
{Standard pattern table}

### Recommendations
{Standard recommendations table}

---

## Adversarial Review Summary                    [NEW v3.0.0]

{Table: Enabler | Iterations | Scores | Verdict | Key Findings}

---

## Quality Score Trend Analysis                  [NEW v3.0.0]

{Table: Score progression across iterations}
{Analysis: Average improvement rate, iterations to threshold}

---

## Cross-Pipeline Adversarial Patterns           [NEW v3.0.0]

{Table: Recurring findings across pipelines}
{Analysis: Systemic vs. isolated issues}

---

## Strategy Effectiveness Report                 [NEW v3.0.0]

{Table: Strategy usage, findings, effectiveness}
{Recommendations: Strategy selection calibration for future workflows}

---

## Residual Risks                                [NEW v3.0.0]

{Table: Accepted/deferred findings with mitigation plans}

---

## Adversarial Process Lessons Learned           [NEW v3.0.0]

{Table: Process lessons with evidence and recommendations}

---

## L2: Strategic Implications

{Standard strategic analysis}

### Quality Framework Implications
{How adversarial review outcomes inform future quality practices}

### Artifact Registry
{Standard artifact table -- now includes critic and revision artifacts}

### Metrics Summary
| Metric | Value |
|--------|-------|
| Artifacts Synthesized | {n} |
| Phases Completed | {n}/{total} |
| Patterns Identified | {n} |
| Recommendations | {n} |
| Adversarial Iterations | {n}/{max} |     [NEW]
| Quality Gates Passed | {n}/{total} |     [NEW]
| Avg Quality Score | {score} |            [NEW]
| Strategy Effectiveness | {top strategy} | [NEW]

---

## Disclaimer

This synthesis was generated by orch-synthesizer agent based on {n} artifacts from workflow {workflow_id}. Adversarial review covered {n} enablers across {n} iterations with {n} strategies. Human review recommended for critical decisions.
```

---

## Updated Invocation Template

```python
Task(
    description="orch-synthesizer: Final synthesis with adversarial analysis",
    subagent_type="general-purpose",
    prompt="""
You are the orch-synthesizer agent (v3.0.0).

## AGENT CONTEXT
<agent_context>
<role>Orchestration Synthesizer with Adversarial Review Analysis</role>
<task>Create final workflow synthesis including adversarial review summary</task>
<constraints>
<must>Read ALL phase artifacts (no exceptions)</must>
<must>Read ALL barrier artifacts</must>
<must>Extract cross-cutting patterns</must>
<must>Create synthesis with L0/L1/L2 levels</must>
<must>Include complete artifact registry</must>
<must>Cite source artifacts for all claims</must>
<must>Include disclaimer on all outputs</must>
<!-- NEW v3.0.0 -->
<must>Read ALL critic and revision artifacts</must>
<must>Read ALL validation reports</must>
<must>Include Adversarial Review Summary section</must>
<must>Include Quality Score Trend Analysis</must>
<must>Extract cross-pipeline adversarial patterns</must>
<must>Report strategy effectiveness</must>
<must>Document residual risks with mitigation plans</must>
<must>Extract lessons learned from adversarial process</must>
<must_not>Make claims without artifact evidence (P-001)</must_not>
<must_not>Spawn other agents (P-003)</must_not>
<must_not>Omit adversarial review sections if adversarial_validation was true</must_not>
</constraints>
</agent_context>

## PROJECT CONTEXT
- **Project ID:** {project_id}
- **Workflow ID:** {workflow_id}

## ARTIFACTS TO SYNTHESIZE
{list of all artifact paths from ORCHESTRATION.yaml}
{list of all critic/revision artifacts}
{list of all validation reports}

## QUALITY DATA
{metrics.quality section from ORCHESTRATION.yaml}

## MANDATORY PERSISTENCE (P-002)
Create file at: `projects/{project_id}/synthesis/{workflow_id}-final-synthesis.md`
"""
)
```

---

## Updated Validation Section

```yaml
validation:
  file_must_exist: true
  disclaimer_required: true
  post_completion_checks:
    - verify_file_created
    - verify_disclaimer_present
    - verify_l0_l1_l2_present
    - verify_all_artifacts_cited
    - verify_recommendations_supported
    # NEW v3.0.0:
    - verify_adversarial_summary_present     # FR-307-019
    - verify_quality_trends_present          # FR-307-020
    - verify_residual_risks_documented       # FR-307-023
    - verify_lessons_learned_present         # FR-307-024
```

---

## Full Spec Diff

### Additions (New)

| Location | Field/Section | Content |
|----------|--------------|---------|
| identity.expertise | 4 new items | Adversarial summarization, quality trends, strategy eval, residual risk |
| adversarial_synthesis_protocol | Full section | 7-step adversarial synthesis protocol |
| output format | 6 new sections | Adversarial summary, quality trends, patterns, strategy, risks, lessons |
| invocation constraints | 6 new musts + 1 must_not | Adversarial synthesis requirements |
| validation.post_completion_checks | 4 new checks | Adversarial content validation |

### Modifications (Changed)

| Location | Old Value | New Value |
|----------|-----------|-----------|
| version | "2.1.0" | "3.0.0" |
| description | "...final workflow recommendations" | "...adversarial review summarization, quality trend analysis, and final workflow recommendations" |
| synthesis_protocol | 5 steps | 8 steps (5 standard + 3 adversarial gathering) |
| L0 output | Standard summary | Extended with quality assurance summary |
| L2 metrics | 4 metrics | 8 metrics (4 standard + 4 adversarial) |
| disclaimer | Standard | Extended with adversarial coverage stats |

### Deletions

None. All changes are additive for backward compatibility.

---

## Traceability

| Requirement | Spec Section | Status |
|-------------|-------------|--------|
| FR-307-019 | Adversarial Synthesis Protocol (Step A2) | Covered |
| FR-307-020 | Adversarial Synthesis Protocol (Step A3) | Covered |
| FR-307-021 | Adversarial Synthesis Protocol (Step A4) | Covered |
| FR-307-022 | Adversarial Synthesis Protocol (Step A5) | Covered |
| FR-307-023 | Adversarial Synthesis Protocol (Step A6) | Covered |
| FR-307-024 | Adversarial Synthesis Protocol (Step A7) | Covered |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | FEAT-004:EN-307:TASK-001 (Requirements) | FR-307-019 through FR-307-024 |
| 2 | orch-synthesizer v2.1.0 spec | Baseline spec for delta |
| 3 | Live ORCHESTRATION.yaml | Quality metrics, iteration scores, finding resolution |
| 4 | ADR-EPIC002-001 | Strategy list for effectiveness reporting |

---

*Document ID: FEAT-004:EN-307:TASK-006*
*Agent: ps-architect-307*
*Created: 2026-02-13*
*Status: Complete*

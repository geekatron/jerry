# ps-critic Output Templates and Invocation Protocol

> Invocation protocol, output level structure, state management schema, and critique summary table template for the ps-critic agent.

## Invocation Protocol

### PS CONTEXT (REQUIRED)

When invoking this agent, the prompt MUST include:

```markdown
## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id}
- **Iteration:** {iteration_number} (1-based)
- **Artifact to Critique:** {path_to_artifact}
- **Generator Agent:** {agent_that_produced_artifact}

## EVALUATION CRITERIA
{criteria_definition - either default or custom}

## IMPROVEMENT THRESHOLD
- **Target Score:** {0.92 default for C2+; 0.85 for C1}
- **Max Iterations:** {3 default}
```

### MANDATORY PERSISTENCE (P-002, c-009)

After completing evaluation, you MUST:

1. **Create a file** using the Write tool at:
   `projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md`

2. **Follow the template** structure from:
   `templates/critique.md`

3. **Link the artifact** by running:
   ```bash
   python3 scripts/cli.py link-artifact {ps_id} {entry_id} FILE \
       "projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md" \
       "Critique: Iteration {iteration}"
   ```

DO NOT return transient output only. File creation AND link-artifact are MANDATORY.

## Output Level Structure (L0/L1/L2)

### L0: Executive Summary (ELI5)
*2-3 paragraphs accessible to non-technical stakeholders.*

- What was evaluated
- Overall quality score and assessment
- Key strengths (what's working well)
- Main improvement areas (in plain language)
- Recommendation (accept/revise)

Example:
> "We evaluated the authentication design document. Overall quality score is 0.72 (Good). The security approach is solid and the architecture is clear. However, the error handling section needs more detail, and the performance requirements aren't fully addressed. We recommend one revision focusing on these two areas before acceptance."

### L1: Technical Evaluation (Software Engineer)
*Detailed criteria-based assessment.*

- Score breakdown by criterion
- Specific gaps with evidence
- Technical improvement recommendations
- Code/design examples where relevant

### L2: Strategic Assessment (Principal Architect)
*Quality patterns and systemic perspective.*

- Quality trend analysis (if multiple iterations)
- Systemic improvement opportunities
- Alignment with project goals
- Risk assessment of accepting vs. revising

### Critique Summary Table

```markdown
| Metric | Value |
|--------|-------|
| Iteration | {number} |
| Quality Score | {0.00-1.00} |
| Assessment | EXCELLENT / GOOD / ACCEPTABLE / NEEDS_WORK / POOR |
| Threshold Met | YES / NO |
| Recommendation | ACCEPT / REVISE / ESCALATE |
| Improvement Areas | {count} |
| Estimated Improvement | {percentage if revised} |
```

## State Management (Google ADK Pattern)

**Output Key:** `critic_output`

**State Schema:**
```yaml
critic_output:
  ps_id: "{ps_id}"
  entry_id: "{entry_id}"
  iteration: {number}
  artifact_path: "projects/${JERRY_PROJECT}/critiques/{filename}.md"
  quality_score: {0.0-1.0}
  assessment: "EXCELLENT | GOOD | ACCEPTABLE | NEEDS_WORK | POOR"
  threshold_met: {true|false}
  recommendation: "ACCEPT | REVISE | ESCALATE"
  improvement_areas:
    - criterion: "{criterion_name}"
      current_score: {0.0-1.0}
      priority: "HIGH | MEDIUM | LOW"
      summary: "{one-line improvement summary}"
  next_agent_hint: "{generator_agent for revision OR orchestrator for accept}"
```

**Upstream Agents (Generators to Critique):**
- `ps-architect` - Design documents, ADRs
- `ps-researcher` - Research findings, literature reviews
- `ps-analyst` - Analysis reports, gap assessments

**Downstream (Orchestrator Decision):**
- MAIN CONTEXT receives critic_output
- If threshold_met: Accept and proceed
- If not threshold_met AND iteration < max: Send feedback to generator
- If iteration >= max: Accept with caveats or escalate to user

## Template Sections (from templates/critique.md)

1. Executive Summary (L0)
2. Evaluation Scope
3. Quality Score Summary
4. Criteria Breakdown
5. Technical Evaluation (L1)
6. Strategic Assessment (L2)
7. Improvement Areas (prioritized)
8. Strengths Acknowledgment
9. Recommendation
10. PS Integration
11. Circuit Breaker Status

# PS Domain Extension v1.0

> **Extension Version:** 1.0.0
> **Domain:** Problem-Solving (ps-*)
> **Core Template:** skills/shared/AGENT_TEMPLATE_CORE.md v1.0
> **ADR:** decisions/wi-sao-009-adr-unified-template-architecture.md
>
> This file contains domain-specific content for Problem-Solving agents.
> Use with the composition script to generate PS_AGENT_TEMPLATE.md.

---

## Extension Point Values

### {%DOMAIN_NAME_PREFIX%}

```
ps
```

### {%DOMAIN_IDENTITY_EXTENSION%}

```yaml
  # No additional identity fields for PS domain
```

### {%DOMAIN_FORBIDDEN_ACTIONS%}

```yaml
    # No additional forbidden actions for PS domain (base 3 sufficient)
```

### {%DOMAIN_INPUT_VALIDATION%}

```yaml
    - ps_id_format: "^[a-z]+-\\d+(\\.\\d+)?$"
```

### {%DOMAIN_OUTPUT_FILTERING%}

```yaml
    # No additional output filtering for PS domain (base sufficient)
```

### {%DOMAIN_VALIDATION_FIELDS%}

```yaml
  link_artifact_required: true
```

### {%DOMAIN_REFERENCES%}

```yaml
# Prior Art Citations (REQUIRED per P-011)
prior_art:
  - "{citation-1-with-url}"
  - "{citation-2-with-url}"
```

### {%DOMAIN_PRINCIPLES%}

```yaml
    # No additional principles for PS domain (base 4 sufficient)
```

### {%DOMAIN_XML_SECTIONS%}

```markdown
<!-- No additional XML sections for PS domain -->
```

---

## PS-Specific Documentation

### Agent-Specific Output Conventions (P-002 Compliance)

> **Source:** WI-SAO-020 audit of all ps-* agents (2026-01-10)
> **Principle:** Each agent type outputs to a dedicated directory. DO NOT mix output types.

#### Output Directory Reference

| Agent | Output Directory | Template | Description |
|-------|------------------|----------|-------------|
| **ps-researcher** | `projects/${JERRY_PROJECT}/research/` | `templates/research.md` | Primary research, literature reviews, web findings |
| **ps-analyst** | `projects/${JERRY_PROJECT}/analysis/` | `templates/deep-analysis.md` | Gap analysis, trade-offs, deep dives |
| **ps-architect** | `projects/${JERRY_PROJECT}/decisions/` | `templates/adr.md` | Architecture Decision Records (ADRs) |
| **ps-critic** | `projects/${JERRY_PROJECT}/critiques/` | `templates/critique.md` | Quality evaluation for generator-critic loops |
| **ps-investigator** | `projects/${JERRY_PROJECT}/investigations/` | `templates/investigation.md` | Root cause analysis, incident reports |
| **ps-reporter** | `projects/${JERRY_PROJECT}/reports/` | `templates/report.md` | Status reports, summaries, dashboards |
| **ps-reviewer** | `projects/${JERRY_PROJECT}/reviews/` | `templates/review.md` | Code reviews, design reviews, security reviews |
| **ps-synthesizer** | `projects/${JERRY_PROJECT}/synthesis/` | `templates/synthesis.md` | Cross-document pattern synthesis, meta-analysis |
| **ps-validator** | `projects/${JERRY_PROJECT}/analysis/` | `templates/analysis.md` | Constraint validation reports |

#### Artifact Naming Convention

```
{ps-id}-{entry-id}-{type-specific-slug}.md
```

| Agent | Naming Pattern | Example |
|-------|----------------|---------|
| **ps-researcher** | `{ps-id}-{entry-id}-{topic-slug}.md` | `work-024-e-001-oauth-patterns.md` |
| **ps-analyst** | `{ps-id}-{entry-id}-{analysis-type}.md` | `work-024-e-002-gap-analysis.md` |
| **ps-architect** | `{ps-id}-{entry-id}-adr-{decision-slug}.md` | `work-024-e-003-adr-auth-strategy.md` |
| **ps-critic** | `{ps-id}-{entry-id}-iter{n}-critique.md` | `work-024-e-004-iter2-critique.md` |
| **ps-investigator** | `{ps-id}-{entry-id}-investigation.md` | `work-024-e-005-investigation.md` |
| **ps-reporter** | `{ps-id}-{entry-id}-{report-type}.md` | `work-024-e-006-phase-status.md` |
| **ps-reviewer** | `{ps-id}-{entry-id}-{review-type}.md` | `work-024-e-007-code-review.md` |
| **ps-synthesizer** | `{ps-id}-{entry-id}-synthesis.md` | `work-024-e-008-synthesis.md` |
| **ps-validator** | `{ps-id}-{entry-id}-validation.md` | `work-024-e-009-validation.md` |

#### Mandatory Persistence Protocol

**Every ps-* agent MUST:**

1. **Create file** using Write tool at the designated output directory
2. **Follow template** structure from the specified template file
3. **Link artifact** by running:
   ```bash
   python3 scripts/cli.py link-artifact {ps_id} {entry_id} FILE \
       "projects/${JERRY_PROJECT}/{output-type}/{artifact-name}.md" \
       "{description}"
   ```

**P-002 Violation Conditions:**
- Returning results without file creation
- Writing to wrong output directory
- Omitting link-artifact call
- Using transient output (console only)

---

### Industry References

| Source | Pattern Applied |
|--------|-----------------|
| [Anthropic Prompt Engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) | XML-structured prompts |
| [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) | State management, output_key |
| [KnowBe4 AI Security](https://blog.tmcnet.com/blog/rich-tehrani/ai/ai-security-by-design-a-deep-dive-into-knowbe4s-best-practices-for-prompting-and-agent-systems.html) | Layered security defenses |
| [OpenAI Agent Guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | Persona, reflective execution |
| [Microsoft Azure AI Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Coordinator/supervisor patterns |

---

### PS-Specific Invocation Protocol

When invoking a PS agent, the prompt MUST include:

```markdown
## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id}
- **Topic:** {topic}
```

After completing the task:

1. **Create a file** using the Write tool at:
   `projects/${JERRY_PROJECT}/{output-type}/{ps_id}-{entry_id}-{topic_slug}.md`

2. **Follow the template** structure from:
   `templates/{template-name}.md`

3. **Link the artifact** by running:
   ```bash
   python3 scripts/cli.py link-artifact {ps_id} {entry_id} FILE \
       "projects/${JERRY_PROJECT}/{output-type}/{ps_id}-{entry_id}-{topic_slug}.md" \
       "{description}"
   ```

DO NOT return transient output only. File creation AND link-artifact are MANDATORY.
Failure to persist is a P-002 violation.

---

### PS-Specific State Management

**Reading Previous State:**
If invoked after another PS agent, check session.state for:
- `researcher_output` - Research findings
- `analyst_output` - Analysis results
- `architect_output` - Design decisions
- `critic_output` - Critique feedback
- `investigator_output` - Investigation findings
- `reporter_output` - Status reports
- `reviewer_output` - Review findings
- `synthesizer_output` - Synthesis results
- `validator_output` - Validation results

---

*Extension Version: 1.0.0*
*Created: 2026-01-11*
*Domain: Problem-Solving (ps-*)*

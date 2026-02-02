# Agent Template Migration Guide

> **Version:** 1.0.0
> **Created:** 2026-01-11
> **Work Item:** WI-SAO-009
> **ADR:** decisions/wi-sao-009-adr-unified-template-architecture.md
>
> This guide documents the migration process for existing agents to the
> Federated Template Architecture.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Summary](#architecture-summary)
3. [Core vs Extension Structure](#core-vs-extension-structure)
4. [Extension Point Syntax](#extension-point-syntax)
5. [Composition Workflow](#composition-workflow)
6. [Validation Commands](#validation-commands)
7. [PS Agent Migration Checklist](#ps-agent-migration-checklist)
8. [NSE Agent Migration Checklist](#nse-agent-migration-checklist)
9. [Backward Compatibility Notes](#backward-compatibility-notes)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Jerry Framework uses a **Federated Template Architecture** for agent definitions.
This architecture separates shared agent structure (~73%) from domain-specific content,
enabling consistent maintenance while preserving domain specializations.

### Benefits

- **Single source of truth** for shared structure (AGENT_TEMPLATE_CORE.md)
- **Domain isolation** via extension files (PS_EXTENSION.md, NSE_EXTENSION.md)
- **Automated composition** via Python script
- **Consistent validation** across all agent families

### Key Files

| File | Purpose |
|------|---------|
| `skills/shared/AGENT_TEMPLATE_CORE.md` | Shared template (~73% of content) |
| `skills/problem-solving/agents/PS_EXTENSION.md` | PS domain-specific content |
| `skills/nasa-se/agents/NSE_EXTENSION.md` | NSE domain-specific content |
| `scripts/compose_agent_template.py` | Composition script |
| `scripts/check_agent_conformance.py` | Validation script |

---

## Architecture Summary

```
┌──────────────────────────────────────────────────────────────┐
│                    AGENT_TEMPLATE_CORE.md                    │
│                     (~73% shared content)                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  YAML Frontmatter Schema                               │  │
│  │  - name, version, description, model                   │  │
│  │  - identity, persona, capabilities                     │  │
│  │  - guardrails, output, validation                      │  │
│  │  - constitution, enforcement, session_context          │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  XML Body Structure                                    │  │
│  │  - <identity>, <persona>, <capabilities>               │  │
│  │  - <guardrails>, <constitutional_compliance>           │  │
│  │  - <invocation_protocol>, <output_levels>              │  │
│  │  - <state_management>                                  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Extension Points: {%DOMAIN_NAME_PREFIX%}, etc.              │
└─────────────────────────┬────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ PS_EXTENSION  │  │ NSE_EXTENSION │  │  (Future)     │
│    .md        │  │     .md       │  │  Extensions   │
└───────┬───────┘  └───────┬───────┘  └───────────────┘
        │                  │
        ▼                  ▼
┌───────────────┐  ┌───────────────┐
│ PS_AGENT_     │  │ NSE_AGENT_    │
│ TEMPLATE.md   │  │ TEMPLATE.md   │
│  (Composed)   │  │  (Composed)   │
└───────────────┘  └───────────────┘
```

---

## Core vs Extension Structure

### Core Template Content (AGENT_TEMPLATE_CORE.md)

The core template contains:

1. **Document Header**: Template metadata and version info
2. **Extension Points Reference**: Table documenting all 9 extension points
3. **YAML Frontmatter Schema**: Full schema with extension point placeholders
4. **XML Body**: Agent persona, capabilities, guardrails, output levels
5. **Usage Instructions**: How to use the template
6. **Migration Checklist**: Per-agent migration tasks

### Extension Files

Extension files provide domain-specific values for 9 extension points:

| Extension Point | PS Domain | NSE Domain |
|-----------------|-----------|------------|
| `{%DOMAIN_NAME_PREFIX%}` | `ps` | `nse` |
| `{%DOMAIN_IDENTITY_EXTENSION%}` | (empty) | `nasa_processes` |
| `{%DOMAIN_FORBIDDEN_ACTIONS%}` | (empty) | `Omit mandatory disclaimer` |
| `{%DOMAIN_INPUT_VALIDATION%}` | `ps_id_format` regex | `project_id_format` regex |
| `{%DOMAIN_OUTPUT_FILTERING%}` | (empty) | `mandatory_disclaimer_on_all_outputs` |
| `{%DOMAIN_VALIDATION_FIELDS%}` | `link_artifact_required` | `disclaimer_required` |
| `{%DOMAIN_REFERENCES%}` | `prior_art` citations | `nasa_standards` references |
| `{%DOMAIN_PRINCIPLES%}` | (empty) | P-040, P-041, P-042 |
| `{%DOMAIN_XML_SECTIONS%}` | (empty) | `<disclaimer>`, `<nasa_se_methodology>` |

---

## Extension Point Syntax

Extension points use the `{%NAME%}` syntax in the core template:

```yaml
name: {%DOMAIN_NAME_PREFIX%}-{agent-type}
```

In extension files, extension point values are defined as:

```markdown
### {%DOMAIN_NAME_PREFIX%}

```
ps
```
```

The composition script:
1. Parses extension file for `### {%NAME%}` headers
2. Extracts content from the following code block
3. Replaces `{%NAME%}` in core template with extracted content

### Rules for Extension Point Content

1. **Code blocks required**: Content must be in markdown code blocks
2. **Language hints optional**: Use ` ```yaml ` or ` ``` ` (plain)
3. **Comments preserved**: YAML comments in content are preserved
4. **Empty content**: Comment-only content becomes empty string
5. **Whitespace**: Leading/trailing whitespace is trimmed

---

## Composition Workflow

### Basic Composition

```bash
# Compose PS template (validate only)
python3 scripts/compose_agent_template.py --domain ps --validate

# Compose and write to default location
python3 scripts/compose_agent_template.py --domain ps --write-default

# Compose NSE template
python3 scripts/compose_agent_template.py --domain nse --write-default

# Compose to custom output path
python3 scripts/compose_agent_template.py --domain ps --output custom_template.md
```

### Diff Mode

Compare composed template with existing file:

```bash
python3 scripts/compose_agent_template.py --domain ps --diff
```

### CI Integration

For continuous integration:

```bash
# Validate composition without writing
python3 scripts/compose_agent_template.py --domain ps --validate
python3 scripts/compose_agent_template.py --domain nse --validate

# Exit codes:
# 0 = Success
# 1 = Validation error (remaining placeholders)
# 2 = Script error (file not found, etc.)
```

---

## Validation Commands

### Template Composition Validation

```bash
# Validate PS template composition
python3 scripts/compose_agent_template.py --domain ps --validate

# Validate NSE template composition
python3 scripts/compose_agent_template.py --domain nse --validate
```

### Agent Conformance Validation

```bash
# Check all agents
python3 scripts/check_agent_conformance.py

# Check specific family
python3 scripts/check_agent_conformance.py --family ps
python3 scripts/check_agent_conformance.py --family nse

# JSON output (for CI)
python3 scripts/check_agent_conformance.py --json

# Verbose output
python3 scripts/check_agent_conformance.py --verbose
```

---

## PS Agent Migration Checklist

Migrate each ps-* agent to the composed template format:

### ps-researcher

- [ ] Update YAML frontmatter to match PS_AGENT_TEMPLATE.md structure
- [ ] Add `identity.cognitive_mode: divergent`
- [ ] Add `persona` section (tone, communication_style, audience_level)
- [ ] Add `guardrails.input_validation` with ps_id_format
- [ ] Add `validation.link_artifact_required: true`
- [ ] Add `prior_art` section with citations
- [ ] Add `constitution.principles_applied` list
- [ ] Add `enforcement` section (tier, escalation_path)
- [ ] Add `session_context` section
- [ ] Update version to reflect migration
- [ ] Run conformance check: `python3 scripts/check_agent_conformance.py --family ps`

### ps-analyst

- [ ] Update YAML frontmatter to match PS_AGENT_TEMPLATE.md structure
- [ ] Add `identity.cognitive_mode: convergent`
- [ ] Add `persona` section
- [ ] Add `guardrails.input_validation`
- [ ] Add `validation.link_artifact_required: true`
- [ ] Add `prior_art` section
- [ ] Add `constitution.principles_applied`
- [ ] Add `enforcement` section
- [ ] Add `session_context` section
- [ ] Update version
- [ ] Run conformance check

### ps-architect

- [ ] Follow same checklist as ps-analyst
- [ ] Set `identity.cognitive_mode: convergent`

### ps-critic

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### ps-investigator

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: divergent`

### ps-reporter

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### ps-reviewer

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### ps-synthesizer

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### ps-validator

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

---

## NSE Agent Migration Checklist

Migrate each nse-* agent to the composed template format:

### nse-requirements

- [ ] Update YAML frontmatter to match NSE_AGENT_TEMPLATE.md structure
- [ ] Add `identity.nasa_processes` list
- [ ] Add `identity.cognitive_mode: convergent`
- [ ] Add `persona` section
- [ ] Add `guardrails.input_validation` with project_id_format
- [ ] Add `guardrails.output_filtering: mandatory_disclaimer_on_all_outputs`
- [ ] Add `validation.disclaimer_required: true`
- [ ] Add `nasa_standards` section
- [ ] Add `constitution.principles_applied` including P-040, P-041, P-042
- [ ] Add `enforcement` section
- [ ] Add `session_context` section
- [ ] Ensure `<disclaimer>` and `<nasa_se_methodology>` XML sections present
- [ ] Update version
- [ ] Run conformance check: `python3 scripts/check_agent_conformance.py --family nse`

### nse-verification

- [ ] Follow same checklist as nse-requirements
- [ ] Set `identity.cognitive_mode: convergent`

### nse-risk

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: divergent`

### nse-review

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### nse-integration

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### nse-configuration

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### nse-architecture

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: divergent`

### nse-reporter

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### nse-qa

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: convergent`

### nse-explorer

- [ ] Follow same checklist
- [ ] Set `identity.cognitive_mode: divergent`

---

## Backward Compatibility Notes

### What Stays the Same

1. **Agent file locations**: Agents remain in their respective directories
   - PS: `skills/problem-solving/agents/ps-*.md`
   - NSE: `skills/nasa-se/agents/nse-*.md`

2. **Agent invocation**: No changes to how agents are invoked via Task tool

3. **Output patterns**: Output directories and naming conventions unchanged

4. **Constitution compliance**: Same principles apply (P-002, P-003, P-004, etc.)

### What Changes

1. **Template source**: Agents should be based on composed templates
   - Before: Copy from PS_AGENT_TEMPLATE.md or NSE_AGENT_TEMPLATE.md
   - After: Templates are auto-generated from core + extension

2. **YAML structure**: Some new sections added:
   - `identity.cognitive_mode`
   - `persona` section
   - `guardrails` section
   - `session_context` section

3. **XML structure**: Some new XML sections:
   - `<constitutional_compliance>`
   - `<state_management>`
   - NSE: `<disclaimer>`, `<nasa_se_methodology>`

4. **Version format**: Use semantic versioning (e.g., "1.0.0")

### Breaking Changes

None. Existing agents will continue to work. However, agents that don't conform
to the new template structure will be flagged by the conformance checker.

---

## Troubleshooting

### Composition Errors

**Problem**: "No extension points found in extension file"

**Solution**: Ensure extension file uses correct header format:
```markdown
### {%DOMAIN_NAME_PREFIX%}

```
value
```
```

**Problem**: "Remaining placeholders after composition"

**Solution**: Check that all 9 extension points are defined in the extension file.
Run composition with verbose output to identify missing points.

### Conformance Errors

**Problem**: "Missing required top-level section: X"

**Solution**: Add the missing section to the agent's YAML frontmatter.
See the template for required structure.

**Problem**: "Name 'X' should start with 'ps-' or 'nse-'"

**Solution**: Ensure agent name follows naming convention:
```yaml
name: ps-agent-name  # or nse-agent-name
```

### Validation Failures

**Problem**: Agent fails validation after migration

**Solution**:
1. Run `python3 scripts/check_agent_conformance.py --family <family> --verbose`
2. Check each reported issue
3. Compare agent with composed template
4. Update agent to match template structure

---

## References

| Document | Purpose |
|----------|---------|
| [ADR WI-SAO-009](../decisions/wi-sao-009-adr-unified-template-architecture.md) | Architecture decision |
| [AGENT_TEMPLATE_CORE.md](../../skills/shared/AGENT_TEMPLATE_CORE.md) | Core template |
| [PS_EXTENSION.md](../../skills/problem-solving/agents/PS_EXTENSION.md) | PS domain extension |
| [NSE_EXTENSION.md](../../skills/nasa-se/agents/NSE_EXTENSION.md) | NSE domain extension |
| [Jerry Constitution](../governance/JERRY_CONSTITUTION.md) | Agent governance |

---

*Guide Version: 1.0.0*
*Work Item: WI-SAO-009*
*Created: 2026-01-11*

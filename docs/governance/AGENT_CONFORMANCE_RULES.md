# Agent Template Conformance Rules

> **Document ID:** GOV-ACR-001
> **Version:** 1.0.0
> **Created:** 2026-01-11
> **Work Item:** WI-SAO-024

---

## Purpose

This document defines the conformance rules for agent files in the Jerry Framework.
All agents must conform to their respective templates to ensure:

- Consistent agent behavior
- Reliable orchestration and handoffs
- Maintainable codebase
- Automated validation capability

---

## Template References

| Family | Template File | Version |
|--------|---------------|---------|
| NSE | `skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md` | 1.0.0 |
| PS | `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` | 2.0.0 |

---

## Required YAML Sections

### NSE Agents (nse-*.md)

All NSE agents MUST include the following YAML frontmatter sections:

| Section | Required Fields | Description |
|---------|-----------------|-------------|
| `name` | - | Format: `nse-{agent-type}` |
| `version` | - | Semantic version string |
| `description` | - | One-line description |
| `model` | - | `opus`, `sonnet`, `haiku`, or `auto` |
| `identity` | `role`, `expertise`, `cognitive_mode`, `nasa_processes` | Agent identity |
| `persona` | `tone`, `communication_style`, `audience_level` | Communication style |
| `capabilities` | `allowed_tools`, `output_formats`, `forbidden_actions` | Capabilities |
| `guardrails` | `input_validation`, `output_filtering`, `fallback_behavior` | Safety |
| `output` | `required`, `location`, `template`, `levels` | Output configuration |
| `validation` | `file_must_exist`, `disclaimer_required`, `post_completion_checks` | Validation |
| `nasa_standards` | - | Array of NASA references |
| `constitution` | `reference`, `principles_applied` | Constitutional compliance |
| `enforcement` | `tier`, `escalation_path` | Enforcement level |
| `session_context` | `schema`, `schema_version`, `input_validation`, `output_validation`, `on_receive`, `on_send` | Handoff config |

### PS Agents (ps-*.md)

All PS agents MUST include the following YAML frontmatter sections:

| Section | Required Fields | Description |
|---------|-----------------|-------------|
| `name` | - | Format: `ps-{agent-type}` |
| `version` | - | Semantic version string |
| `description` | - | One-line description |
| `model` | - | `opus`, `sonnet`, `haiku`, or `auto` |
| `identity` | `role`, `expertise`, `cognitive_mode` | Agent identity |
| `persona` | `tone`, `communication_style`, `audience_level` | Communication style |
| `capabilities` | `allowed_tools`, `output_formats`, `forbidden_actions` | Capabilities |
| `guardrails` | `input_validation`, `output_filtering`, `fallback_behavior` | Safety |
| `output` | `required`, `location`, `template`, `levels` | Output configuration |
| `validation` | `file_must_exist`, `link_artifact_required`, `post_completion_checks` | Validation |
| `prior_art` | - | Array of industry citations |
| `constitution` | `reference`, `principles_applied` | Constitutional compliance |
| `enforcement` | `tier`, `escalation_path` | Enforcement level |
| `session_context` | `schema`, `schema_version`, `input_validation`, `output_validation`, `on_receive`, `on_send` | Handoff config |

---

## Key Differences Between Families

| Aspect | NSE Agents | PS Agents |
|--------|------------|-----------|
| Identity | Includes `nasa_processes` | No NASA processes |
| Validation | Requires `disclaimer_required` | Requires `link_artifact_required` |
| References | `nasa_standards` (NASA docs) | `prior_art` (industry sources) |

---

## Validation Rules

### Name Format
- NSE agents: Must start with `nse-`
- PS agents: Must start with `ps-`

### Version Format
- Must be a quoted semantic version string: `"X.Y.Z"`

### YAML Frontmatter Format
- Must start with `---` on line 1
- Must end with `---` before the XML body
- No code-fenced YAML (use proper frontmatter delimiters)

---

## Running Conformance Checks

### Manual Check

```bash
# Check all agents
python3 scripts/check_agent_conformance.py

# Check only NSE agents
python3 scripts/check_agent_conformance.py --family nse

# Check only PS agents
python3 scripts/check_agent_conformance.py --family ps

# Output as JSON (for CI)
python3 scripts/check_agent_conformance.py --json

# Verbose output (show passing checks)
python3 scripts/check_agent_conformance.py --verbose
```

### Pre-commit Hook

Install and run pre-commit:

```bash
# Install pre-commit (one-time)
pip install pre-commit
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run only conformance check
pre-commit run check-agent-conformance --all-files
```

### CI Integration

For CI pipelines, use JSON output and check exit code:

```bash
python3 scripts/check_agent_conformance.py --json > conformance-report.json
if [ $? -ne 0 ]; then
  echo "Conformance check failed"
  exit 1
fi
```

---

## Common Issues and Fixes

### Missing Section

**Issue:**
```
Missing required top-level section: session_context
```

**Fix:**
Add the section to the agent's YAML frontmatter. Copy from template.

### Missing Field

**Issue:**
```
Missing required field: output.template
```

**Fix:**
Add the field under the parent section:
```yaml
output:
  required: true
  location: "projects/${JERRY_PROJECT}/..."
  template: "templates/{appropriate-template}.md"  # Add this
  levels:
    - L0
    - L1
    - L2
```

### Invalid Name Format

**Issue:**
```
Name 'my-agent' should start with 'nse-'
```

**Fix:**
Update the `name` field to use the correct prefix for the family.

### Non-Standard Frontmatter

**Issue:**
```
No YAML frontmatter found. Expected --- delimiters.
```

**Fix:**
Ensure the file starts with proper frontmatter:
```yaml
---
name: nse-example
version: "1.0.0"
...
---
```

Not:
```markdown
# Agent Name
---
```yaml
name: nse-example
```
---
```

---

## Enforcement

Conformance is enforced at multiple levels:

1. **Pre-commit hook** - Blocks commits with non-conformant agents
2. **CI pipeline** - Fails builds with conformance issues
3. **Code review** - Reviewers verify template compliance
4. **Periodic audits** - WI-SAO-024 established this check

---

## References

- [NSE Agent Template](../../skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md)
- [PS Agent Template](../../skills/problem-solving/agents/PS_AGENT_TEMPLATE.md)
- [Jerry Constitution](./JERRY_CONSTITUTION.md)
- Work Item: WI-SAO-024

---

*Document Version: 1.0.0*
*Last Updated: 2026-01-11*

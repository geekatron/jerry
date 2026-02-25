# Schema Versioning and Evolution Guide

> **Document ID:** JERRY-SCHEMA-VERS-001
> **Version:** 1.0.0
> **Created:** 2026-01-12
> **Work Item:** WI-SAO-018

---

## Overview

This document defines the versioning strategy, migration procedures, and backward
compatibility rules for all machine-readable schemas in the Jerry framework.

**Governed Schemas:**

| Schema | Location | Current Version |
|--------|----------|-----------------|
| Agent Definition | `docs/schemas/jerry-claude-agent-definition-v1.schema.json` | 1.1.0 |
| Agent Definition Defaults | `docs/schemas/jerry-claude-agent-defaults.yaml` | 1.0.0 |
| Session Context | `docs/schemas/session_context.json` | 1.0.0 |
| Tool Registry | `TOOL_REGISTRY.yaml` | 1.0.0 |
| Orchestration Template | `skills/orchestration/templates/ORCHESTRATION.template.yaml` | 2.0.0 |
| Agent Template | `.claude/agents/TEMPLATE.md` | 1.0.0 |
| PS Skill Contract | `skills/problem-solving/contracts/PS_SKILL_CONTRACT.yaml` | 1.0.0 |
| NSE Skill Contract | `skills/nasa-se/contracts/NSE_SKILL_CONTRACT.yaml` | 1.0.0 |
| Cross-Skill Handoff | `skills/shared/contracts/CROSS_SKILL_HANDOFF.yaml` | 1.0.0 |

---

## Versioning Strategy

### Semantic Versioning (SemVer)

All schemas follow [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH

Examples:
  1.0.0 → Initial release
  1.1.0 → Added optional field (backward compatible)
  1.1.1 → Fixed typo in description
  2.0.0 → Renamed required field (breaking change)
```

### Version Increment Rules

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking change | **MAJOR** | Remove required field, rename field, change type |
| New optional field | **MINOR** | Add `metadata` field with default |
| Documentation fix | **PATCH** | Fix typo in description |
| New enum value | **MINOR** | Add `CANCELLED` to status enum |
| Remove enum value | **MAJOR** | Remove `DRAFT` from status enum |
| Default value change | **MINOR** (usually) | Change default from `null` to `[]` |

### Pre-release Versions

For experimental schemas not yet stable:

```
1.0.0-alpha.1    # Early experimental
1.0.0-beta.1     # Feature-complete but not validated
1.0.0-rc.1       # Release candidate
```

---

## Backward Compatibility Rules

### Golden Rule

> **Existing consumers of a schema MUST NOT break when the schema is updated.**

### Compatibility Guarantees

#### What MUST remain compatible (within MAJOR version):

1. **Required field names** - Cannot be renamed or removed
2. **Field types** - Cannot change (string → number is breaking)
3. **Enum values** - Existing values cannot be removed
4. **Validation constraints** - Cannot become more restrictive

#### What MAY change (within MINOR version):

1. **New optional fields** - With sensible defaults
2. **New enum values** - Added to existing enums
3. **Relaxed constraints** - Less restrictive validation
4. **Deprecation notices** - Mark fields as deprecated

#### What requires MAJOR version bump:

1. **Removed fields** (required or optional)
2. **Renamed fields**
3. **Type changes**
4. **Removed enum values**
5. **Stricter validation** (e.g., new `minLength`)

### Deprecation Process

1. **MINOR version**: Add `deprecated: true` and `deprecation_notice` with migration path
2. **Next MAJOR version**: Remove deprecated field

```yaml
# Example deprecation
fields:
  old_field_name:
    type: string
    deprecated: true
    deprecation_notice: "Use 'new_field_name' instead. Will be removed in v2.0.0"
  new_field_name:
    type: string
    description: "Replacement for old_field_name"
```

---

## Schema Migration Guide

### Migration Workflow

```
1. Identify schema change needed
2. Determine version bump (MAJOR/MINOR/PATCH)
3. Update schema with new version
4. Create migration notes (if MAJOR)
5. Update consumers (if breaking)
6. Update this registry
7. Commit with schema change in message
```

### Migration Notes Template

For MAJOR version changes, create a migration note:

```markdown
## Migration: v1.x → v2.0

### Breaking Changes

1. **Renamed: `old_field` → `new_field`**
   - Before: `{ "old_field": "value" }`
   - After: `{ "new_field": "value" }`
   - Automation: `sed 's/old_field/new_field/g'`

2. **Removed: `deprecated_field`**
   - Action: Remove from all consumers
   - Alternative: Use `replacement_field` instead

### Automated Migration Script

```bash
# Update all YAML files
find . -name "*.yaml" -exec sed -i '' 's/old_field/new_field/g' {} \;
```

### Consumer Update Checklist

- [ ] Update `session_context.json` references
- [ ] Update agent prompt templates
- [ ] Update validation tests
- [ ] Update documentation
```

---

## Version Discovery

### Finding Schema Version

Each schema includes a `schema_version` field:

**YAML schemas:**
```yaml
schema_version: "1.0.0"
```

**JSON schemas:**
```json
{
  "$id": "https://jerry.dev/schemas/session_context/v1.0.0",
  "version": "1.0.0"
}
```

**Markdown with YAML frontmatter:**
```markdown
---
schema_version: "1.0.0"
---
```

### Programmatic Version Access

```python
# Python example
import yaml
import json

def get_yaml_schema_version(path: str) -> str:
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("schema_version", "unknown")

def get_json_schema_version(path: str) -> str:
    with open(path) as f:
        data = json.load(f)
    return data.get("version", "unknown")
```

---

## Validation and Enforcement

### CI/CD Checks

1. **Version Format**: Must match `^[0-9]+\.[0-9]+\.[0-9]+(-[a-z]+\.[0-9]+)?$`
2. **Version Increment**: New version > old version (on schema changes)
3. **Changelog Entry**: MAJOR changes require migration notes

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: validate-schema-versions
      name: Validate schema versions
      entry: python scripts/validate_schema_versions.py
      language: python
      files: \.(yaml|json)$
```

---

## Schema Registry

### Canonical Locations

| Schema Type | Path Pattern |
|-------------|--------------|
| Core schemas | `docs/schemas/{name}.json` |
| Type definitions | `docs/schemas/types/{name}.{ts,py}` |
| Skill contracts | `skills/{skill}/contracts/{NAME}_CONTRACT.yaml` |
| Templates | `skills/{skill}/templates/*.template.yaml` |
| Agent templates | `.claude/agents/TEMPLATE.md` |
| Tool registry | `TOOL_REGISTRY.yaml` (root) |

### Schema References

Schemas should reference this document:

```yaml
# In any schema file
# Schema Evolution: See docs/schemas/SCHEMA_VERSIONING.md
```

---

## Version History

| Date | Schema | Version | Change |
|------|--------|---------|--------|
| 2026-02-24 | jerry-claude-agent-definition-v1.schema.json | 1.1.0 | Dual-layer schema: Claude Code native + Jerry governance fields. Renamed from agent-definition-v1.schema.json. Added tools, disallowedTools, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, isolation. Relaxed additionalProperties on identity, persona, capabilities, guardrails, output, session_context. Expanded enums. Added $defs, config section, portability, inputs, audit_checks, reasoning_effort. (PROJ-012) |
| 2026-02-21 | agent-definition-v1.schema.json | 1.0.0 | Initial agent definition schema (ADR-PROJ007-001). Note: historical project work artifacts (PROJ-007, PROJ-005) retain this original filename; these are historical records and are not subject to retroactive renaming. |
| 2026-01-12 | TOOL_REGISTRY.yaml | 1.0.0 | Initial versioning added |
| 2026-01-12 | ORCHESTRATION.template.yaml | 2.0.0 | Schema version field added |
| 2026-01-12 | Agent TEMPLATE.md | 1.0.0 | YAML frontmatter added |
| 2026-01-10 | session_context.json | 1.0.0 | Initial release |
| 2026-01-12 | PS_SKILL_CONTRACT.yaml | 1.0.0 | Initial release |
| 2026-01-12 | NSE_SKILL_CONTRACT.yaml | 1.0.0 | Initial release |
| 2026-01-12 | CROSS_SKILL_HANDOFF.yaml | 1.0.0 | Initial release |

---

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [JSON Schema Versioning](https://json-schema.org/understanding-json-schema/reference/schema.html)
- [OpenAPI Versioning](https://spec.openapis.org/oas/v3.0.3#versions)
- [Jerry Constitution P-002](../governance/JERRY_CONSTITUTION.md) - File Persistence

---

*Document Version: 1.0.0*
*Created: 2026-01-12*
*Work Item: WI-SAO-018*

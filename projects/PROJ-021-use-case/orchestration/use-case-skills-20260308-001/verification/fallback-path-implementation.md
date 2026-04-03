# Fallback Output Path Implementation

**Agent:** eng-backend
**Date:** 2026-03-11
**Scope:** PROJ-021 -- all 6 agent pairs (12 files total)

## Summary

Added `fallback_location` field to all 6 governance YAML files and added corresponding path resolution notes to all 6 agent `.md` files. The change addresses the case where `JERRY_PROJECT` is not set, routing output to `work/` instead of `projects/${JERRY_PROJECT}/`.

## Problem Statement

The `output.location` field in each governance YAML hardcoded `projects/${JERRY_PROJECT}/...`. Users working with the repository-based pattern (no `JERRY_PROJECT` set) had no declared fallback, causing undefined output placement at runtime.

## Change Applied

### Governance YAML Change (all 6 files)

Added `fallback_location` field immediately after `location` in the `output` section:

```yaml
output:
  required: true
  location: "projects/${JERRY_PROJECT}/{subdir}/{pattern}"
  fallback_location: "work/{subdir}/{pattern}"
```

The subdirectory structure is preserved identically between `location` and `fallback_location`. Only the root prefix changes.

### Agent .md Change (all 6 files)

Added a path resolution note at the output path declaration point in the `<output>` section and, where applicable, in the `<capabilities>` section where the output location pattern is stated:

```
Output path resolves to `projects/${JERRY_PROJECT}/...` when JERRY_PROJECT is set. Falls back to `work/...` when JERRY_PROJECT is not set.
```

## Files Modified

### /use-case skill

| File | Change |
|------|--------|
| `skills/use-case/agents/uc-author.governance.yaml` | Added `fallback_location: "work/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"` |
| `skills/use-case/agents/uc-author.md` | Added path resolution note in `<capabilities>` output pattern and `<output>` path declaration |
| `skills/use-case/agents/uc-slicer.governance.yaml` | Added `fallback_location: "work/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"` |
| `skills/use-case/agents/uc-slicer.md` | Added path resolution note in `<capabilities>` output location and `<output>` L1 artifact detail |

### /test-spec skill

| File | Change |
|------|--------|
| `skills/test-spec/agents/tspec-generator.governance.yaml` | Added `fallback_location: "work/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md"` |
| `skills/test-spec/agents/tspec-generator.md` | Added path resolution note in `<capabilities>` output pattern and `<output>` path declaration |
| `skills/test-spec/agents/tspec-analyst.governance.yaml` | Added `fallback_location: "work/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md"` |
| `skills/test-spec/agents/tspec-analyst.md` | Added path resolution note in `<capabilities>` output pattern and `<output>` path declaration |

### /contract-design skill

| File | Change |
|------|--------|
| `skills/contract-design/agents/cd-generator.governance.yaml` | Added `fallback_location: "work/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml"` |
| `skills/contract-design/agents/cd-generator.md` | Added path resolution note in `<capabilities>` output patterns and `<output>` path declarations |
| `skills/contract-design/agents/cd-validator.governance.yaml` | Added `fallback_location: "work/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md"` |
| `skills/contract-design/agents/cd-validator.md` | Added path resolution note in `<capabilities>` output pattern and `<output>` path declaration |

## Fallback Location Table

| Agent | location | fallback_location |
|-------|----------|-------------------|
| uc-author | `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` | `work/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` |
| uc-slicer | `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` | `work/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` |
| tspec-generator | `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md` | `work/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md` |
| tspec-analyst | `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md` | `work/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md` |
| cd-generator | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml` | `work/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml` |
| cd-validator | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md` | `work/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md` |

## Design Decisions

**Subdirectory structure preserved.** The `work/{subdir}/` fallback mirrors the `projects/${JERRY_PROJECT}/{subdir}/` structure exactly. Downstream consumers that derive paths from the subdir pattern (e.g., tspec-analyst locating a Feature file produced by tspec-generator) remain consistent regardless of which root is active.

**cd-generator mapping artifact.** The cd-generator produces two outputs: a `.openapi.yaml` contract and a `-mapping.md` document. Both fall back to `work/contracts/` when JERRY_PROJECT is not set. The governance YAML `fallback_location` declares only the primary contract artifact (consistent with how `location` is declared). The mapping artifact follows the same root substitution pattern.

**Schema compatibility.** The `fallback_location` field is a governance YAML extension. The `agent-governance-v1.schema.json` uses `additionalProperties: true` on the `output` sub-object, which accepts fields not enumerated in the required set. This field does not introduce a schema violation.

**Runtime resolution responsibility.** The fallback logic is declared here for agent runtime awareness, not enforced by schema. Each agent reads its own governance YAML output section at runtime and applies the fallback when `JERRY_PROJECT` is absent from the environment. No framework-level resolver is assumed; the agent performs the resolution inline.

## OWASP Verification

This change modifies agent definition metadata only. No server-side logic, authentication, data access, or cryptographic code was introduced. OWASP Top 10 checklist items are not applicable to this governance metadata change.

The `fallback_location` values do not introduce path traversal risk: the `work/` prefix is a relative repository-root path, not a user-supplied value. All path segments following `work/` use the same deterministic naming patterns (`UC-{DOMAIN}-{NNN}-{slug}.md`) as the primary location.

## Status

All 12 files updated. No schema violations introduced. Changes are backward-compatible: agents that do not read `fallback_location` continue to use `location` unchanged.

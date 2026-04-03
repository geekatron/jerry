# Gap Analysis: Claude Code Schema Validation

> **Date:** 2026-03-26 | **Criticality:** C4 | **Sources:** STORY-001 + STORY-002 research artifacts

## Document Sections

| Section | Purpose |
|---------|---------|
| [Agent Frontmatter Gaps](#agent-frontmatter-gaps) | Differences in agent .md schema |
| [Skill Frontmatter Gaps](#skill-frontmatter-gaps) | Differences in SKILL.md schema |
| [Shared Issues](#shared-issues) | Issues common to both schemas |
| [Risk Assessment](#risk-assessment) | Impact of each gap |
| [Recommended Changes](#recommended-changes) | Prioritized change list |

---

## Agent Frontmatter Gaps

### Our Schema: `docs/schemas/claude-code-frontmatter-v1.schema.json`

| # | Field | Our Schema (v1.0.0) | Official (March 2026) | Gap Type | Severity | v1.1.0 Status |
|---|-------|-----------|----------------------|----------|----------|---------------|
| 1 | `effort` | MISSING | enum: `low`, `medium`, `high`, `max` | Missing field | HIGH | **RESOLVED** -- added in v1.1.0 |
| 2 | `initialPrompt` | MISSING | string | Missing field | MEDIUM | **RESOLVED** -- added in v1.1.0 |
| 3 | `mcpServers` | `type: object` | `type: array` (string or inline object entries) | Wrong type | CRITICAL | **RESOLVED** -- accepts both formats via `oneOf` in v1.1.0 |
| 4 | `model` | `enum: [sonnet, opus, haiku, inherit]` | Aliases + full model IDs (`claude-opus-4-6`, etc.) | Incomplete enum | HIGH | **RESOLVED** -- changed to free-form string with documented values in v1.1.0 |
| 5 | `name` | OK | OK | Match | -- | Unchanged |
| 6 | `description` | OK (stricter minLength) | OK | Match | -- | Unchanged |
| 7 | `tools` | OK | OK | Match | -- | Unchanged |
| 8 | `disallowedTools` | OK | OK | Match | -- | Unchanged |
| 9 | `permissionMode` | OK | OK | Match | -- | Unchanged |
| 10 | `maxTurns` | OK | OK | Match | -- | Unchanged |
| 11 | `skills` | OK | OK | Match | -- | Unchanged |
| 12 | `hooks` | OK (additionalProperties) | OK | Match | -- | Description expanded (24+ events) |
| 13 | `memory` | OK | OK | Match | -- | Description expanded |
| 14 | `background` | OK | OK | Match | -- | Description expanded |
| 15 | `isolation` | OK | OK | Match | -- | Unchanged |
| 16 | `color` | OK (documented as undocumented) | Not in official table | Acceptable | -- | Unchanged |

**Summary (v1.0.0):** 11 match, 2 missing, 1 wrong type, 1 incomplete
**Summary (v1.1.0):** All 4 gaps RESOLVED. 16/16 fields addressed.

### mcpServers Format Discrepancy

**Official docs show array format:**
```yaml
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github
```

**Our agents use object format (works at runtime):**
```yaml
mcpServers:
  context7: true
```

**Decision:** Accept BOTH formats via `oneOf` in schema. The object format is demonstrably functional (50+ agents use it). The array format is officially documented. Claude Code likely accepts both.

---

## Skill Frontmatter Gaps

### Our Schema: `docs/schemas/claude-code-skill-frontmatter-v1.schema.json`

| # | Field | Our Schema (v1.0.0) | Official (March 2026) | Gap Type | Severity | v1.1.0 Status |
|---|-------|-----------|----------------------|----------|----------|---------------|
| 1 | `effort` | MISSING | enum: `low`, `medium`, `high`, `max` | Missing field | HIGH | **RESOLVED** |
| 2 | `paths` | MISSING | string or array of glob patterns | Missing field | HIGH | **RESOLVED** |
| 3 | `shell` | MISSING | enum: `bash`, `powershell` | Missing field | LOW | **RESOLVED** |
| 4 | `mode` | MISSING | boolean (UNCONFIRMED in primary docs) | Missing field | LOW | **RESOLVED** (marked unconfirmed) |
| 5 | `license` | MISSING | string (Agent Skills standard) | Missing field | LOW | **RESOLVED** |
| 6 | `compatibility` | MISSING | string, max 500 (Agent Skills standard) | Missing field | LOW | **RESOLVED** |
| 7 | `metadata` | MISSING | object, string-to-string (Agent Skills standard) | Missing field | MEDIUM | **RESOLVED** |
| 8 | `name` | Pattern missing no-consecutive-hyphens and reserved-word prohibition | Additional constraints | Incomplete constraint | MEDIUM | **PARTIALLY RESOLVED** (description updated; regex unchanged) |
| 9 | `description` | minLength: 10 (stricter than official) | Non-empty, max 1024 | Acceptable | -- | Unchanged |
| 10 | `argument-hint` | OK | OK | Match | -- | Unchanged |
| 11 | `disable-model-invocation` | OK | OK | Match | -- | Unchanged |
| 12 | `user-invocable` | OK | OK | Match | -- | Unchanged |
| 13 | `allowed-tools` | OK | OK | Match | -- | Unchanged |
| 14 | `model` | OK | OK | Match | -- | Unchanged |
| 15 | `context` | OK | OK | Match | -- | Unchanged |
| 16 | `agent` | OK | OK | Match | -- | Unchanged |
| 17 | `hooks` | OK (additionalProperties) | OK | Match | -- | Description expanded |

**Summary (v1.0.0):** 9 match, 7 missing, 1 incomplete constraint
**Summary (v1.1.0):** All 7 missing fields RESOLVED. 1 partially resolved (name regex). 17/17 fields addressed.

---

## Shared Issues

| Issue | Affects | Impact | v1.1.0 Status |
|-------|---------|--------|---------------|
| No official Anthropic JSON Schema exists | Both | We own the maintenance burden | OPEN -- see [Maintenance Process](#maintenance-process) |
| `effort` field missing | Both | Cannot validate reasoning depth configuration | **RESOLVED** |
| `model` field too restrictive (agent only) | Agent schema | Rejects valid full model IDs | **RESOLVED** (free-form string with docs) |
| Claude Code silently ignores unknown fields | Both | `additionalProperties: true` is correct behavior | BY DESIGN -- see [Scope and Limitations](#scope-and-limitations) |
| Agent Skills standard fields not tracked | Skill schema | Portability compliance gap | **RESOLVED** (license, compatibility, metadata added) |
| Schema cannot enforce behavioral constraints | Both | H-34 worker/orchestrator tool restrictions not validated | OPEN -- see [Scope and Limitations](#scope-and-limitations) |
| No validation test suite | Both | Schema regression undetectable | **RESOLVED** -- `tests/schemas/test_frontmatter_schemas.py` (34 tests) |

---

## Risk Assessment

| Gap | False Positive Risk | False Negative Risk | Runtime Impact | v1.1.0 Status |
|-----|-------------------|--------------------| --------------|---------------|
| Missing `effort` | None (field ignored) | Agent/skill with effort setting not validated | Reasoning depth not governed | **RESOLVED** |
| Missing `initialPrompt` | None | --agent mode config not validated | Low (niche feature) | **RESOLVED** |
| Wrong `mcpServers` type | **HIGH** -- rejects valid array-format configs | Accepts wrong object format | Schema blocks correct configs | **RESOLVED** (both formats accepted) |
| Incomplete `model` enum | **HIGH** -- rejects valid full model IDs | None | Schema blocks valid agent configs | **RESOLVED** (free-form string) |
| Missing `paths` | None | File-scoped skills not validated | Activation scope not governed | **RESOLVED** |
| Missing Agent Skills fields | None | Portability metadata not validated | Low | **RESOLVED** |
| `model` accepts any string | None | Typos pass validation | CI-level risk | OPEN (requires complementary CI validator) |

---

## Recommended Changes

### Priority 1 (CRITICAL -- blocks valid configurations)

1. **Fix `mcpServers` in agent schema** -- accept both object and array formats via `oneOf`
2. **Fix `model` in agent schema** -- replace strict enum with pattern that accepts aliases AND full model IDs

### Priority 2 (HIGH -- missing important fields)

3. **Add `effort` to both schemas** -- enum: `low`, `medium`, `high`, `max`
4. **Add `paths` to skill schema** -- string or array of glob patterns
5. **Add `initialPrompt` to agent schema** -- string

### Priority 3 (MEDIUM -- standards compliance)

6. **Add `metadata` to skill schema** -- object, string-to-string map
7. **Tighten `name` in skill schema** -- add description noting no-consecutive-hyphens and reserved-word constraints

### Priority 4 (LOW -- nice-to-have)

8. **Add `shell` to skill schema** -- enum: `bash`, `powershell`
9. **Add `mode` to skill schema** -- boolean (mark as unconfirmed)
10. **Add `license` and `compatibility` to skill schema** -- Agent Skills standard fields

---

## Scope and Limitations

> Added per C4 adversarial review findings RT-002/RT-003.

### What These Schemas CAN Enforce (Correctness Gate)

- Field name validity (required fields present, correct types)
- Enum constraint adherence (permissionMode, effort, isolation, context, shell)
- Structural format correctness (mcpServers array/object, tools string/array)
- Description length and name pattern constraints

### What These Schemas CANNOT Enforce (Requires Complementary Validation)

| Constraint | Why Schema Can't Enforce | Required Mechanism |
|-----------|-------------------------|-------------------|
| H-34 behavioral: worker agents must not include `Agent`/`Task` in tools | Requires semantic understanding of agent role (worker vs orchestrator) | Custom validator script or CI gate reading `.governance.yaml` |
| Prompt injection in description field | JSON Schema cannot distinguish adversarial NL from legitimate text | Runtime prompt injection detection (hooks, CODEOWNERS review) |
| hooks arbitrary code execution | Hooks exist to run commands by design | CI hook allowlist, CODEOWNERS gating on hooks changes |
| mcpServers connecting to unauthorized external servers | Schema validates structure, not server identity | CI allowlist of approved MCP server names |
| model field typos (e.g., "opuis") | Free-form string cannot be fully constrained without blocking future models | CI validation script with known-good model list (updatable) |
| Cross-field consistency (e.g., effort:max with non-Opus model) | JSON Schema `if/then` is possible but fragile across model releases | CI validation script |
| Reserved word prohibition in name ("claude", "anthropic") | Regex cannot enumerate all reserved words cleanly | CI validation script with reserved word list |

### Architectural Conclusion

Schema validation is a **correctness gate** (prevents structural errors) but NOT a **security boundary** (cannot prevent adversarial content). The STRIDE threat model (EN-001) identifies 23 threats, 6 of which require runtime controls beyond schema capability. See `EN-001-security-review/stride-threat-model.md`.

---

## Maintenance Process

> Added per C4 adversarial review findings RT-006/PM-002/IN-003.

### Version Pinning

Both schemas are pinned to **Claude Code documentation state as of March 2026**. The `$id` field contains the schema version (`v1.1.0`).

| Schema | Version | Pinned To |
|--------|---------|-----------|
| `claude-code-frontmatter-v1.schema.json` | v1.1.0 | code.claude.com/docs/en/sub-agents (March 2026) |
| `claude-code-skill-frontmatter-v1.schema.json` | v1.1.0 | code.claude.com/docs/en/skills (March 2026) |

### Changelog Monitoring

Schema freshness depends on tracking upstream Claude Code changes. Recommended process:

1. **Monitor:** Subscribe to Claude Code changelog at `code.claude.com/docs/en/changelog`
2. **Trigger:** Any changelog entry mentioning "frontmatter", "subagent", "skill", or "agent definition" triggers schema review
3. **Review:** Compare changed fields against schema; update schema version and `$id`
4. **Validate:** Run all 89 agent definitions and 30 SKILL.md files against updated schema

### Validation Test Suite (RESOLVED)

> Per C4 finding SR-003/PM-005. Delivered as EN-003.

Test suite at `tests/schemas/test_frontmatter_schemas.py` -- 38 tests:
- 5 positive fixtures (3 agent, 2 skill) from production definitions
- 21 negative fixtures (12 agent, 9 skill) covering all schema constraints including reserved word rejection
- 5 live file roundtrip tests parsing frontmatter directly from disk
- 7 schema integrity tests verifying JSON structure

Run: `uv run pytest tests/schemas/test_frontmatter_schemas.py`

---

## Review Artifact Reconciliation

> Added per C4 re-score finding on Internal Consistency (0.72).

Two independent security assessments were conducted:

| Review | Agent | Findings | Notes |
|--------|-------|----------|-------|
| Security review (eng-security) | EN-001/STORY-004 | 0 Critical, 3 High, 4 Medium | FIND-001/002 (reserved word bypass) resolved in v1.1.0 via `allOf/not` construct |
| Vulnerability assessment (red-vuln) | STORY-004 | 2 Critical, 3 High, 4 Medium | V-03-001 (mcpServers RCE) and V-04-001 (unbounded description) are runtime risks beyond schema scope |

The severity discrepancy (0 vs 2 Critical) reflects different assessment scopes: eng-security evaluated schema-enforceable constraints (where the reserved word fix resolved the top findings), while red-vuln evaluated the full attack surface including runtime behaviors that schema validation cannot address. Both assessments are correct within their scope. The 2 Critical findings from red-vuln are documented in [Scope and Limitations](#scope-and-limitations) as requiring runtime controls.

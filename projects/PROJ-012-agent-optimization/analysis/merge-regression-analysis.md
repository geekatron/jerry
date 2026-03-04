# PROJ-012: Merge Regression Analysis

> **Date:** 2026-02-25
> **Branch:** `feat/proj-012-agent-optimization`
> **Merge commit:** `fc2c339c` (main → feat branch)
> **Pre-merge commit:** `63127d86`
> **Post-merge HEAD:** `b738078d`
> **Case Study:** `docs/experience/CASESTUDY-PROJ012-merge-regression.md`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | What happened and recommendation |
| [What Was Lost](#what-was-lost) | Detailed regression analysis |
| [What Was Gained](#what-was-gained) | New capabilities from main |
| [File-Level Delta](#file-level-delta) | Counts and categories |
| [Pre-Merge Pipeline (63127d86)](#pre-merge-pipeline-63127d86) | Old compose architecture |
| [Post-Merge Pipeline (HEAD)](#post-merge-pipeline-head) | Current build architecture |
| [Defaults File Status](#defaults-file-status) | Analysis of jerry-claude-agent-defaults.yaml |
| [Agent .md Frontmatter Comparison](#agent-md-frontmatter-comparison) | Field-by-field diff |
| [Decision: Revert vs Fix Forward](#decision-revert-vs-fix-forward) | Recommendation with rationale |
| [Fix Forward Scope](#fix-forward-scope) | What needs to change |

---

## Executive Summary

The merge of `main` brought a comprehensive new `src/agents/` bounded context (567 new files) with vendor-agnostic canonical format and build-time assembly. However, it **regressed Claude Code frontmatter generation**: the new `ClaudeCodeAdapter._build_frontmatter()` emits only 5 of 12+ supported fields, and the defaults file (`jerry-claude-agent-defaults.yaml`) is never consumed.

**Recommendation: Fix forward.** The fix is surgical (~50-100 lines in the adapter). Reverting would lose 567 files and require re-merging main later.

---

## What Was Lost

### 1. Defaults Composition Pipeline

**Pre-merge:** `AgentConfigResolver.compose_agent_config()` performed:
```
1. Load jerry-claude-agent-defaults.yaml (base defaults)
2. Extract YAML frontmatter from agent .md file
3. Deep merge: defaults + agent overrides (agent wins)
4. Substitute ${jerry.*} config variables via LayeredConfigAdapter
5. Validate composed result against JSON Schema
```

**Post-merge:** `ClaudeCodeAdapter._build_frontmatter()` performs:
```
1. Read CanonicalAgent entity fields
2. Map model tier and tool names
3. Emit 5 fields to YAML frontmatter
(No defaults loading. No config variable substitution.)
```

### 2. Claude Code Vendor Fields in Frontmatter

Fields present in pre-merge composed output but MISSING from post-merge:

| Field | Pre-Merge Value | Post-Merge | Status |
|-------|-----------------|------------|--------|
| `permissionMode` | "default" (from defaults) | Not emitted | **LOST** |
| `background` | false (from defaults) | Not emitted | **LOST** |
| `disallowedTools` | N/A (wasn't mapped) | Not emitted | **Never existed** |
| `maxTurns` | N/A | Not emitted | **Never existed** |
| `version` | Agent-specific (e.g., "2.3.0") | Not emitted | **LOST** (now in .governance.yaml) |
| `persona` | Deep-merged with defaults | Not emitted | **LOST** (now in .governance.yaml) |
| `capabilities` | Agent-specific | Not emitted | **LOST** (now in .governance.yaml) |
| `guardrails` | Deep-merged with defaults | Not emitted | **LOST** (now in .governance.yaml) |
| `constitution` | Agent-specific | Not emitted | **LOST** (now in .governance.yaml) |

**Note:** Governance fields (version, persona, capabilities, guardrails, constitution) were intentionally moved to `.governance.yaml` companion files by main's architecture. This is by design — these are not Claude Code native fields. The regression is specifically in the Claude Code native fields: `permissionMode`, `background`.

### 3. Config Variable Substitution

`${jerry.*}` token replacement (e.g., `${jerry.project}` → `PROJ-012`) is gone. The old pipeline resolved these via `LayeredConfigAdapter.get()` with a 4-tier config chain (env → project → root → code defaults). The new pipeline does not perform variable substitution.

### 4. `.claude/agents/*.md` Composed Output

Pre-merge had 58 composed files in `.claude/agents/` with full merged frontmatter. These files were deleted during merge conflict resolution because main doesn't use this directory — main generates vendor files directly into `skills/*/agents/`.

---

## What Was Gained

### From Main (567 new files)

| Category | Count | Description |
|----------|-------|-------------|
| Canonical agent format | 116 files | `skills/*/composition/*.agent.yaml` + `*.prompt.md` (58 agents × 2 files) |
| Agents bounded context | ~45 files | `src/agents/` — domain entities, services, ports, adapters, handlers |
| Agent tests | ~20 files | `tests/agents/` — unit, integration tests (~4000+ lines) |
| CLI commands | 5 commands | `build`, `extract`, `validate`, `list`, `diff` |
| Generated vendor files | 116 files | `skills/*/agents/*.md` + `*.governance.yaml` (58 agents × 2 files) |
| Schemas | 2 files | `agent-canonical-v1.schema.json`, `agent-governance-v1.schema.json` |
| Mappings | 1 file | `src/agents/infrastructure/mappings.yaml` (tool/model name mappings) |
| Documentation | ~10 files | Updated AGENTS.md, schema docs, knowledge base |
| Projects | ~250 files | New project work directories, orchestration artifacts |

### Architecture Improvements

- **Vendor-agnostic canonical format** — agents defined once, built for any vendor
- **Hexagonal architecture** — clean domain/application/infrastructure separation
- **Build-time assembly** — `jerry agents build` generates vendor files from canonical source
- **Extract capability** — `jerry agents extract` reverse-engineers canonical from vendor files
- **Diff capability** — `jerry agents diff` detects drift between canonical and generated
- **Tool/model mapping** — abstract names (e.g., `file_read`) mapped to vendor names (e.g., `Read`)

---

## File-Level Delta

### Summary (63127d86 → b738078d)

| Category | Count |
|----------|-------|
| Files added from main | ~567 |
| Files deleted | 6 (old schema, old tests, READMEs) |
| Files modified (merge resolution) | ~30 |
| Agent format change | 58 agents: single `.md` → 3-file format (`.agent.yaml` + `.prompt.md` + `.md`/`.governance.yaml`) |

### Key Deletions

| Deleted File | Reason |
|-------------|--------|
| `docs/schemas/jerry-claude-agent-definition-v1.schema.json` | Renamed to `agent-definition-v1.schema.json` |
| `tests/infrastructure/adapters/configuration/test_agent_config_resolver.py` | Replaced by `tests/agents/` suite |
| `tests/infrastructure/adapters/configuration/test_agent_config_resolver_compose.py` | Replaced by `tests/agents/` suite |
| Various `README.md` files in skill dirs | Removed per H-25 (no README.md inside skill folder) |

---

## Pre-Merge Pipeline (63127d86)

### Architecture: Single-File Agent Definitions

```
skills/{skill}/agents/{agent}.md     ← YAML frontmatter + markdown body
                    ↓
          AgentConfigResolver
                    ↓
     1. Extract frontmatter + body
     2. Load jerry-claude-agent-defaults.yaml
     3. Deep merge (defaults + agent overrides)
     4. Substitute ${jerry.*} config vars
     5. Validate against JSON Schema
                    ↓
.claude/agents/{agent}.md              ← Composed output with ALL fields
```

### Key Implementation (`AgentConfigResolver`)

- **`compose_agent_config()`**: Core merge method — `_deep_merge(defaults, frontmatter)`
- **`_deep_merge()` semantics**: Scalars: override wins. Dicts: recursive merge. Arrays: override replaces.
- **`compose_agent_to_file()`**: Write `---\n{yaml}\n---\n{body}` to output directory
- **`compose_all_to_dir()`**: Batch composition with optional `--clean` flag
- **`_substitute_config_vars()`**: Replace `${jerry.*}` tokens via `LayeredConfigAdapter`
- **Discovery**: `skills/*/agents/*.md` glob, excluding README/TEMPLATE/EXTENSION files

### Sample Composed Output (ps-architect at 63127d86)

```yaml
---
permissionMode: default          # From defaults
background: false                # From defaults
version: 2.3.0                   # Agent override (default was 1.0.0)
persona:
  tone: authoritative            # Agent override (default was "professional")
  communication_style: consultative  # Same as default
  audience_level: adaptive       # Same as default
capabilities:
  forbidden_actions:             # Agent override (replaced default array)
  - Spawn recursive subagents (P-003)
  - Override user decisions (P-020)
  - Return transient output only (P-002)
  - Make decisions without considering alternatives (P-011)
  allowed_tools:                 # Agent-specific
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - mcp__memory-keeper__store
  - mcp__memory-keeper__retrieve
  - mcp__memory-keeper__search
guardrails:
  output_filtering:              # Agent override
  - no_secrets_in_output
  - decisions_require_alternatives_considered
  - consequences_must_be_documented
  fallback_behavior: warn_and_request_context  # Agent override
  input_validation:              # Agent-specific
  - ps_id_format: ^[a-z]+-\d+(\.\d+)?$
# ... full constitution, validation, output sections ...
---
{markdown body preserved verbatim}
```

---

## Post-Merge Pipeline (HEAD)

### Architecture: Canonical Format + Build-Time Assembly

```
skills/{skill}/composition/{agent}.agent.yaml   ← Vendor-agnostic structured data
skills/{skill}/composition/{agent}.prompt.md     ← System prompt body
                    ↓
     FilesystemAgentRepository._parse_agent()
                    ↓
          CanonicalAgent entity (23 fields)
                    ↓
     ClaudeCodeAdapter.generate()
                    ↓
     _build_frontmatter()  →  skills/{skill}/agents/{agent}.md
     _build_governance_yaml()  →  skills/{skill}/agents/{agent}.governance.yaml
```

### Current `_build_frontmatter()` Output (5 fields only)

```yaml
---
name: ps-architect
description: Architectural decision agent producing ADRs with Nygard format and L0/L1/L2 output levels
model: opus
tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
mcpServers:
  context7: true
  memory-keeper: true
---
```

### Missing Claude Code Fields

| Claude Code Field | In CanonicalAgent? | In Defaults File? | Emitted? |
|-------------------|--------------------|--------------------|----------|
| `name` | Yes (`.name`) | No | Yes |
| `description` | Yes (`.description`) | No | Yes |
| `model` | Yes (`.model_tier` mapped) | No | Yes |
| `tools` | Yes (`.native_tools` mapped) | No | Yes |
| `mcpServers` | Yes (`.mcp_servers`) | No | Yes |
| `permissionMode` | No | Yes ("default") | **NO** |
| `background` | No | Yes (false) | **NO** |
| `disallowedTools` | Yes (`.forbidden_tools`) | No | **NO** |
| `maxTurns` | Possible via `.extra_yaml` | No | **NO** |
| `skills` | Possible via `.extra_yaml` | No | **NO** |
| `hooks` | Possible via `.extra_yaml` | No | **NO** |
| `memory` | Possible via `.extra_yaml` | No | **NO** |
| `isolation` | Possible via `.extra_yaml` | No | **NO** |

---

## Defaults File Status

**File:** `docs/schemas/jerry-claude-agent-defaults.yaml`

**Status:** Exists. Unchanged between 63127d86 and HEAD. **Not consumed by any code.**

**Contents:**

```yaml
permissionMode: "default"
background: false
version: "1.0.0"
persona:
  tone: "professional"
  communication_style: "consultative"
  audience_level: "adaptive"
capabilities:
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Misrepresent capabilities or confidence (P-022)"
guardrails:
  output_filtering:
    - no_secrets_in_output
    - no_executable_code_without_confirmation
    - all_claims_must_have_citations
  fallback_behavior: "warn_and_retry"
output:
  required: false
  levels: ["L0", "L1", "L2"]
validation:
  file_must_exist: true
constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-020: User Authority (Hard)"
    - "P-022: No Deception (Hard)"
enforcement:
  tier: "medium"
```

**Documented resolution chain (from file header, not implemented):**
```
1. This file (base defaults)
2. Agent YAML from skills/{skill}/composition/{agent}.agent.yaml (per-agent overrides)
3. Jerry CLI config variable substitution (env → project → root → code defaults)
4. Schema validation
```

**Only step 2 (partial) and step 4 are implemented.** Steps 1 and 3 are not.

---

## Agent .md Frontmatter Comparison

### Pre-Merge (ps-architect, 63127d86)

```yaml
permissionMode: default
background: false
version: 2.3.0
persona:
  tone: authoritative
  communication_style: consultative
  audience_level: adaptive
capabilities:
  forbidden_actions:
  - Spawn recursive subagents (P-003)
  - Override user decisions (P-020)
  - Return transient output only (P-002)
  - Make decisions without considering alternatives (P-011)
  allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - mcp__memory-keeper__store
  - mcp__memory-keeper__retrieve
  - mcp__memory-keeper__search
guardrails:
  output_filtering:
  - no_secrets_in_output
  - decisions_require_alternatives_considered
  - consequences_must_be_documented
  fallback_behavior: warn_and_request_context
  input_validation:
  - ps_id_format: ^[a-z]+-\d+(\.\d+)?$
```

### Post-Merge (ps-architect, HEAD)

```yaml
name: ps-architect
description: Architectural decision agent producing ADRs with Nygard format and L0/L1/L2 output levels
model: opus
tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
mcpServers:
  context7: true
  memory-keeper: true
```

### Delta

- **Lost:** `permissionMode`, `background`, `version`, `persona`, `capabilities`, `guardrails`
- **Moved to .governance.yaml:** `version`, `persona`, `capabilities`, `guardrails`, `constitution`, `validation`, `enforcement`, `session_context`, `prior_art`
- **New:** `name` (now explicit in frontmatter)
- **Unchanged:** `model`, `tools` (format changed from array to comma-separated), `mcpServers`

---

## Decision: Revert vs Fix Forward

### Option A: Revert to 63127d86

| Pro | Con |
|-----|-----|
| Immediately restores defaults composition | Loses 567 files from main |
| Known working compose pipeline | Old architecture incompatible with main's canonical format |
| | Must re-merge main eventually (same 11 conflicts) |
| | Old tests replaced; would need to re-add main's test suite |
| | Blocks all PROJ-010 work (canonical format) |

### Option B: Fix Forward (RECOMMENDED)

| Pro | Con |
|-----|-----|
| Keeps all 567 files from main | Requires implementation work (~50-100 lines) |
| Keeps vendor-agnostic architecture | |
| Surgical fix in one file | |
| Better architecture long-term | |
| No re-merge needed | |

### Recommendation

**Fix forward.** The regression is confined to `ClaudeCodeAdapter._build_frontmatter()` not emitting all Claude Code fields and not consuming the defaults file. This is a ~50-100 line fix in one adapter file plus test coverage. Reverting would destroy $MAJOR work from main and require re-merging later.

---

## Fix Forward Scope

### Primary Change: `src/agents/infrastructure/adapters/claude_code_adapter.py`

1. **`__init__()`** — Accept `defaults_path: Path | None` parameter
2. **New `_load_defaults()`** — Load and cache defaults YAML
3. **`_build_frontmatter()`** — Extend to emit all Claude Code fields:
   - `permissionMode` from defaults (overridable via `extra_yaml`)
   - `background` from defaults (overridable via `extra_yaml`)
   - `disallowedTools` from `agent.forbidden_tools` (mapped via tool_mapper)
   - Optional fields from `extra_yaml`: maxTurns, skills, hooks, memory, isolation
4. **Factory `_create_claude_code_adapter()`** — Pass defaults path

### Secondary Changes

- **Tests:** Extend `tests/agents/infrastructure/adapters/test_claude_code_adapter.py`
- **Verification:** Run `jerry agents build` + `jerry agents validate`

### Not In Scope

- Config variable substitution (`${jerry.*}`) — this is a separate feature that can be added later
- Governance defaults merging — `.governance.yaml` already has full metadata from canonical source
- `.claude/agents/` directory — main generates vendor files into `skills/*/agents/` directly

---

*Analysis by: Claude Code session, 2026-02-25*
*Commits analyzed: 63127d86 (pre-merge), fc2c339c (merge), b738078d (HEAD)*

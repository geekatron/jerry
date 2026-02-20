# MCP Tool Standards

<!-- VERSION: 1.3.1 | DATE: 2026-02-20 | SOURCE: FEAT-028-mcp-tool-integration -->

> Governance rules for proactive MCP tool usage across Jerry Framework agents.

<!-- L2-REINJECT: rank=9, tokens=70, content="Context7 REQUIRED for external library/framework docs: resolve-library-id then query-docs; respect tool-enforced call limit. Memory-Keeper REQUIRED at phase boundaries: phase-complete→store, phase-start→retrieve. Fallback: persist to work/.mcp-fallback/ on MCP failure. Key: jerry/{project}/{entity-type}/{entity-id}." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Non-overridable MCP usage constraints |
| [MEDIUM Standards](#medium-standards) | Overridable with documented justification |
| [Context7 Integration](#context7-integration) | When and how to use Context7 docs lookup |
| [Memory-Keeper Integration](#memory-keeper-integration) | When and how to use Memory-Keeper persistence |
| [Canonical Tool Names](#canonical-tool-names) | Authoritative MCP tool identifiers |
| [Agent Integration Matrix](#agent-integration-matrix) | Which agents have which MCP tools |
| [Error Handling](#error-handling) | Fallback behavior for MCP failures |
| [References](#references) | Source document traceability |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Source | Consequence |
|----|------|--------|-------------|
| MCP-001 | Context7 MUST be used when any agent task references an external library, framework, SDK, or API by name. Respect the per-question call limit enforced by the tool. WebSearch is permitted only for general concepts or when Context7 returns no results. | FEAT-028 AC-1 | Research quality degradation. Stale training-data knowledge used instead of current docs. |
| MCP-002 | Memory-Keeper `store` MUST be called at orchestration phase boundaries. Memory-Keeper `retrieve`/`search` MUST be called at phase start to load prior context. | FEAT-028 AC-2 | Cross-session context loss. Phase handoff operates on stale or absent data. |

> **Namespace:** MCP-001/MCP-002 use a file-scoped `MCP-` prefix (not the global `H-` series in `quality-enforcement.md`). These rules are scoped to MCP tool governance only. The global HARD Rule Index references this file via H-22 (proactive skill invocation) which mandates the behavioral patterns these rules operationalize.

---

## MEDIUM Standards

> Override requires documented justification.

| ID | Standard | Guidance |
|----|----------|----------|
| MCP-M-001 | Memory-Keeper SHOULD be used for multi-session research that produces reusable findings. | Store key findings with `jerry/{project}/research/{slug}` key pattern. |
| MCP-M-002 | New agents SHOULD declare MCP tool usage in their agent definition file's `capabilities.allowed_tools` YAML frontmatter. Research/documentation agents SHOULD use Context7; cross-session agents SHOULD use Memory-Keeper. | Follow existing agent patterns in `skills/*/agents/*.md`. |

---

## Context7 Integration

**Protocol:**
1. Call `mcp__context7__resolve-library-id` with library name and research question
2. Call `mcp__context7__query-docs` with resolved library ID and specific query
3. Respect the per-question call limit enforced by the tool; each distinct library resets the limit
4. If `resolve-library-id` returns no matches, fall back to WebSearch for that library

**Triggers:** Task mentions any external package, library, SDK, or framework by name.

| Scenario | Use Context7? | Alternative |
|----------|---------------|-------------|
| Library API docs | **YES** | — |
| Framework patterns | **YES** | — |
| SDK usage examples | **YES** | — |
| General concepts | No | WebSearch |
| Codebase-internal questions | No | Read/Grep |
| Context7 returns no results | No | WebSearch |

---

## Memory-Keeper Integration

Memory-Keeper is REQUIRED at orchestration phase boundaries (MCP-002). Memory-Keeper is RECOMMENDED for multi-session research that produces reusable findings (MCP-M-001). See [MEDIUM Standards](#medium-standards) for details.

**Key Pattern:** `jerry/{project}/{entity-type}/{entity-id}`

**Entity-type vocabulary** (defined here; extension requires revision of this file and corresponding TOOL_REGISTRY.yaml update):

| Entity Type | Use Case |
|-------------|----------|
| `orchestration` | Workflow phase state |
| `research` | Multi-session research findings |
| `phase-boundary` | Quality gate / phase transition results |
| `decision` | Architecture decisions, ADR context |
| `requirements` | Requirements persistence |
| `transcript` | Parsed transcript session data |

**Entity-id format:** Use entity ID (e.g., `EPIC-003`) for entity-scoped entries or `{slug}-{YYYYMMDD}` for date-scoped entries.

**Examples:**
- `jerry/PROJ-001/orchestration/feat028-mcp-20260220`
- `jerry/PROJ-001/research/adversarial-strategies`
- `jerry/PROJ-001/phase-boundary/qg1-results`

**Triggers:**

| Event | Action | Tools |
|-------|--------|-------|
| Orchestration phase complete | Store phase summary + artifacts | `store` |
| New orchestration phase start | Retrieve prior phase context | `retrieve`, `search` |
| Multi-session research | Store key findings for reuse | `store` |
| Session resume | Search for prior context | `search` |
| Cross-pipeline synthesis | Search across stored contexts | `search` |

---

## Canonical Tool Names

> Authoritative tool names for agent definitions. TOOL_REGISTRY.yaml is the SSOT for tool-to-agent mappings; this section provides the canonical identifiers.

| Tool | Canonical Name | Purpose |
|------|---------------|---------|
| Context7 Resolve | `mcp__context7__resolve-library-id` | Resolve package to library ID |
| Context7 Query | `mcp__context7__query-docs` | Query library documentation |
| Memory-Keeper Store | `mcp__memory-keeper__store` | Store context with key |
| Memory-Keeper Retrieve | `mcp__memory-keeper__retrieve` | Retrieve context by key |
| Memory-Keeper Search | `mcp__memory-keeper__search` | Search stored contexts |
| Memory-Keeper List | `mcp__memory-keeper__list` | List all stored contexts |
| Memory-Keeper Delete | `mcp__memory-keeper__delete` | Delete stored context |

> **Note:** `list` and `delete` are available in the MCP server but not currently assigned to any agent. Reserved for administrative use.

---

## Agent Integration Matrix

> TOOL_REGISTRY.yaml is the SSOT for tool-to-agent mappings. This matrix provides a summary view.

| Agent | Context7 | Memory-Keeper | Rationale |
|-------|----------|---------------|-----------|
| ps-researcher | resolve, query | — | Library/framework research |
| ps-analyst | resolve, query | — | API documentation lookup |
| ps-architect | resolve, query | store, retrieve, search | Architecture research + decision persistence |
| ps-investigator | resolve, query | — | Debugging with library docs |
| ps-synthesizer | resolve, query | — | Cross-source synthesis |
| nse-explorer | resolve, query | — | Trade study research |
| nse-architecture | resolve, query | — | Architecture standards research |
| nse-requirements | — | store, retrieve, search | Requirements persistence across sessions |
| orch-planner | — | store, retrieve, search | Phase planning + context handoff |
| orch-tracker | — | store, retrieve, search | State persistence + checkpoint storage |
| orch-synthesizer | — | retrieve, search | Cross-pipeline context retrieval |
| ts-parser | — | store, retrieve | Transcript session persistence |
| ts-extractor | — | store, retrieve | Extraction results persistence |

**Not included (by design):**
- **adv-*** — Self-contained strategy execution; no external research or cross-session state
- **wt-*** — Read-only auditing of worktracker files
- **ps-critic, ps-validator, ps-reviewer** — Quality evaluation; no external library research needed
- **ps-reporter** — Report generation from existing data

> **Classification rule for new agents:** See MCP-M-002 in [MEDIUM Standards](#medium-standards).

---

## Error Handling

| Failure | Fallback |
|---------|----------|
| Context7 `resolve-library-id` returns no matches | Fall back to WebSearch for that library |
| Context7 `query-docs` returns empty or irrelevant | Use WebSearch; note "Context7 no coverage" in output |
| Memory-Keeper `store` fails (timeout, server down) | Persist context to `work/.mcp-fallback/{key}.md`; note failure in worktracker entry |
| Memory-Keeper `retrieve` returns empty | Search by partial key before proceeding; if still empty, proceed without prior context and note gap |
| Context7 tool-enforced call limit reached | Fall back to WebSearch for remaining queries for that library |
| MCP server unavailable | Continue work without MCP tools; log gap in session worktracker entry |

---

## References

| Source | Content |
|--------|---------|
| FEAT-028-mcp-tool-integration (AC-1, AC-2) | Feature entity; AC-1 mandates Context7 governance, AC-2 mandates Memory-Keeper governance |
| TOOL_REGISTRY.yaml | SSOT for tool-to-agent mappings and permissions |
| `.claude/settings.local.json` | Runtime MCP server configuration |
| `quality-enforcement.md` | Quality gate thresholds and enforcement architecture |

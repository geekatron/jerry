# MCP Tool Standards

<!-- VERSION: 1.4.0 | DATE: 2026-03-28 | SOURCE: FEAT-028-mcp-tool-integration, ADR-STORY015-001, STORY-017 | REVISION: STORY-017 tier renumbering: MCP-M-001 T3/T4 refs, eng-*/red-* MK exclusion notes -->

> Governance rules for proactive MCP tool usage across Jerry Framework agents.

<!-- L2-REINJECT: rank=9, content="Context7 REQUIRED for external library/framework docs: resolve-library-id then query-docs; respect tool-enforced call limit. Memory-Keeper REQUIRED at phase boundaries: phase-complete→context_save, phase-start→context_get. Fallback: persist to work/.mcp-fallback/ on MCP failure. Key: jerry/{project}/{entity-type}/{entity-id}." -->

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
| MCP-002 | Memory-Keeper `context_save` MUST be called at orchestration phase boundaries. Memory-Keeper `context_get`/`context_search` MUST be called at phase start to load prior context. | FEAT-028 AC-2 | Cross-session context loss. Phase handoff operates on stale or absent data. |

> **Namespace:** MCP-001/MCP-002 use a file-scoped `MCP-` prefix (not the global `H-` series in `quality-enforcement.md`). These rules are scoped to MCP tool governance only. The global HARD Rule Index references this file via H-22 (proactive skill invocation) which mandates the behavioral patterns these rules operationalize.

---

## MEDIUM Standards

> Override requires documented justification.

| ID | Standard | Guidance |
|----|----------|----------|
| MCP-M-001 | Memory-Keeper SHOULD be used for multi-session research that produces reusable findings. T4 (Persistent + External) agents are the primary target of this standard; T3 (Persistent) agents may also use Memory-Keeper for cross-session state management. | Store key findings with `jerry/{project}/research/{slug}` key pattern. |
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
| Orchestration phase complete | Store phase summary + artifacts | `context_save` |
| New orchestration phase start | Retrieve prior phase context | `context_get`, `context_search` |
| Multi-session research | Store key findings for reuse | `context_save` |
| Session resume | Search for prior context | `context_search` |
| Cross-pipeline synthesis | Search across stored contexts | `context_search` |

---

## Canonical Tool Names

> Authoritative tool names for agent definitions. TOOL_REGISTRY.yaml is the SSOT for tool-to-agent mappings; this section provides the canonical identifiers.

| Tool | Canonical Name | Purpose |
|------|---------------|---------|
| Context7 Resolve | `mcp__context7__resolve-library-id` | Resolve package to library ID |
| Context7 Query | `mcp__context7__query-docs` | Query library documentation |
| Memory-Keeper Store | `mcp__memory-keeper__context_save` | Store context with key |
| Memory-Keeper Retrieve | `mcp__memory-keeper__context_get` | Retrieve context by key |
| Memory-Keeper Search | `mcp__memory-keeper__context_search` | Search stored contexts |
| Memory-Keeper List | `mcp__memory-keeper__context_session_list` | List all stored contexts |
| Memory-Keeper Delete | `mcp__memory-keeper__context_batch_delete` | Delete stored context |

> **Note:** `list` and `delete` are available in the MCP server but not currently assigned to any agent. Reserved for administrative use.

---

## Agent Integration Matrix

> TOOL_REGISTRY.yaml is the SSOT for tool-to-agent mappings. This matrix provides a summary view.

| Agent | Context7 | Memory-Keeper | Rationale |
|-------|----------|---------------|-----------|
| ps-researcher | resolve, query | — | Library/framework research |
| ps-analyst | resolve, query | — | API documentation lookup |
| ps-architect | resolve, query | context_save, context_get, context_search | Architecture research + decision persistence |
| ps-investigator | resolve, query | — | Debugging with library docs |
| ps-synthesizer | resolve, query | — | Cross-source synthesis |
| nse-explorer | resolve, query | — | Trade study research |
| nse-architecture | resolve, query | — | Architecture standards research |
| nse-requirements | — | context_save, context_get, context_search | Requirements persistence across sessions |
| orch-planner | — | context_save, context_get, context_search | Phase planning + context handoff |
| orch-tracker | — | context_save, context_get, context_search | State persistence + checkpoint storage |
| orch-synthesizer | — | context_get, context_search | Cross-pipeline context retrieval |
| ts-parser | — | context_save, context_get | Transcript session persistence |
| ts-extractor | — | context_save, context_get | Extraction results persistence |
| eng-architect | resolve, query | — | Library/framework security research |
| eng-lead | resolve, query | — | Standards and dependency research |
| eng-backend | resolve, query | — | Backend framework security docs |
| eng-frontend | resolve, query | — | Frontend framework security docs |
| eng-infra | resolve, query | — | Infrastructure and container docs |
| eng-devsecops | resolve, query | — | Security tooling documentation |
| eng-qa | resolve, query | — | Testing framework documentation |
| eng-security | resolve, query | — | Security standard documentation |
| eng-reviewer | resolve, query | — | Standards verification research |
| eng-incident | resolve, query | — | IR framework documentation |
| pm-customer-insight | resolve, query | — | Customer research documentation |
| pm-market-strategist | resolve, query | — | Market strategy framework docs |
| pm-competitive-analyst | resolve, query | — | Competitive analysis methodology |
| red-lead | resolve, query | — | Methodology framework research |
| red-recon | resolve, query | — | Reconnaissance tool documentation |
| red-vuln | resolve, query | — | Vulnerability database research |
| red-exploit | resolve, query | — | Exploitation framework docs |
| red-privesc | resolve, query | — | OS and AD documentation |
| red-lateral | resolve, query | — | Network protocol documentation |
| red-persist | resolve, query | — | OS internals documentation |
| red-exfil | resolve, query | — | Protocol and channel documentation |
| red-reporter | resolve, query | — | Reporting framework docs |
| red-infra | resolve, query | — | C2 framework documentation |
| red-social | resolve, query | — | Social engineering methodology |

| adv-executor | resolve, query | — | Fact verification during adversarial strategy execution (STORY-011, GH #217) |
| ux-orchestrator | resolve, query | — | UX methodology and framework documentation |
| ux-atomic-architect | resolve, query | — | Component library documentation (Material UI, Radix, Shadcn/ui) |
| ux-heart-analyst | resolve, query | — | HEART/GSM framework documentation and benchmark data |
| ux-heuristic-evaluator | resolve, query | — | External UX standards and Nielsen documentation |
| ux-inclusive-evaluator | resolve, query | — | WCAG specifications, ARIA authoring practices |
| ux-jtbd-analyst | resolve, query | — | JTBD framework documentation and domain literature |
| ux-kano-analyst | resolve, query | — | Kano model methodology and survey design references |
| ux-lean-ux-facilitator | resolve, query | — | Lean UX methodology and experiment design patterns |

**Not included (by design):**
- **adv-scorer, adv-selector** — Scoring and strategy selection are self-contained; no external research
- **wt-*** — Read-only auditing of worktracker files
- **ps-critic, ps-validator, ps-reviewer** — Quality evaluation; no external library research needed
- **ps-reporter** — Report generation from existing data
- **eng-*** — T4 (Persistent + External) under the new tier model but MUST NOT use Memory-Keeper. File-based persistence per P-002 (engagement-scoped output) remains the correct mechanism. The T4 tier permits MK as a ceiling; the `.md` frontmatter and this exclusion note prevent actual MK access.
- **ux-ai-design-guide, ux-sprint-facilitator, ux-behavior-diagnostician** — T4 tools (WebSearch/WebFetch) but no Context7; external research via web search only
- **pm-product-strategist, pm-business-analyst** — T4 tools (WebSearch/WebFetch) but no Context7; external research via web search only
- **red-*** — T4 (Persistent + External) under the new tier model but MUST NOT use Memory-Keeper. File-based persistence per P-002 (engagement-scoped output) remains the correct mechanism; scope documents and evidence stored in engagement directories. The T4 tier permits MK as a ceiling; the `.md` frontmatter and this exclusion note prevent actual MK access.

> **Classification rule for new agents:** See MCP-M-002 in [MEDIUM Standards](#medium-standards).

---

## Error Handling

| Failure | Fallback |
|---------|----------|
| Context7 `resolve-library-id` returns no matches | Fall back to WebSearch for that library |
| Context7 `query-docs` returns empty or irrelevant | Use WebSearch; note "Context7 no coverage" in output |
| Memory-Keeper `context_save` fails (timeout, server down) | Persist context to `work/.mcp-fallback/{key}.md`; note failure in worktracker entry |
| Memory-Keeper `context_get` returns empty | Search by partial key before proceeding; if still empty, proceed without prior context and note gap |
| Context7 tool-enforced call limit reached | Fall back to WebSearch for remaining queries for that library |
| MCP server unavailable | Continue work without MCP tools; log gap in session worktracker entry |

---

## Permission Syntax

For Claude Code permission patterns (MCP wildcards, skill permissions, Bash patterns, file access, evaluation order, settings scope), see `docs/reference/claude-code-permissions.md`.

### MCP Server Namespace Note

Context7 registers under two server names depending on installation method:
- **`mcp__context7__*`** — direct MCP server configuration (via `.mcp.json` or CLI)
- **`mcp__plugin_context7_context7__*`** — plugin-registered form (via `enabledPlugins` in `.claude/settings.json` with `context7@claude-plugins-official`)

Both wildcards are in `settings.local.json` to cover both registration paths. This dual-namespace pattern is a known Claude Code behavior for plugins that expose MCP servers. See GitHub Issue #29360 for the namespace resolution discussion.

### Permission Mode

Neither `settings.json` nor `settings.local.json` sets `defaultMode`. Claude Code defaults to `"default"` mode: prompts for permission on first use of each tool. The `Skill()` entries in `settings.local.json` pre-approve skill invocations so they don't prompt. Without these entries, skills would still work but would prompt on first invocation per session.

---

## References

| Source | Content |
|--------|---------|
| FEAT-028-mcp-tool-integration (AC-1, AC-2) | Feature entity; AC-1 mandates Context7 governance, AC-2 mandates Memory-Keeper governance |
| TOOL_REGISTRY.yaml | SSOT for tool-to-agent mappings and permissions |
| `.claude/settings.local.json` | Runtime MCP server configuration |
| `quality-enforcement.md` | Quality gate thresholds and enforcement architecture |
| `docs/reference/claude-code-permissions.md` | Claude Code permission syntax reference (patterns, wildcards, evaluation order, scopes) |
| ADR-STORY015-001 | Tier model renumbering decision (Option A: Persistent-First Linear) | `projects/PROJ-024-tactical-work/.../STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md` |

---

## Changelog

| Version | Date | Story | Changes |
|---------|------|-------|---------|
| 1.4.0 | 2026-03-28 | STORY-017 | MCP-M-001 updated with T3/T4 tier references per ADR-STORY015-001. eng-\*/red-\* exclusion notes expanded: "T4 permits MK ceiling but MUST NOT use" with P-002 engagement-scoped rationale. pm-product-strategist/pm-business-analyst updated to "T4 tools". ADR-STORY015-001 added to References. |
| 1.3.1 | 2026-02-20 | FEAT-028 | Initial MCP tool governance standards |

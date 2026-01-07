# Research: Context7 MCP Integration Patterns

> **PS:** phase-38.17
> **Exploration:** e-119
> **Created:** 2026-01-04
> **Status:** RESEARCH
> **Agent:** ps-researcher
> **Session:** cc/phase-38.16

---

## Executive Summary

This research documents best practices for integrating Context7 MCP tools with Claude Code skills and agents. Context7 provides real-time, version-specific documentation access through the Model Context Protocol (MCP), enabling agents to retrieve up-to-date library documentation without relying on potentially outdated training data.

**Key Findings:**
1. **Two-Phase Workflow Required:** Always call `resolve-library-id` before `query-docs` to obtain the correct Context7-compatible library ID
2. **Naming Convention:** Claude Code exposes MCP tools with prefix `mcp__<server-name>__<tool-name>` (e.g., `mcp__context7__resolve-library-id`)
3. **Library Selection Criteria:** Prioritize libraries by source reputation (High > Medium > Low), benchmark score, and code snippet count
4. **Call Limit:** Maximum 3 calls per question to prevent excessive API usage
5. **Proactive Usage:** Use Context7 BEFORE writing code that uses library features, not as a fallback

---

## Research Questions

1. What is the correct tool naming convention for MCP tools in Claude Code?
2. When should `resolve-library-id` vs `query-docs` be used?
3. How should Context7 be integrated into agent workflows?
4. What are the best practices for library selection and query formulation?

---

## Methodology

### Context7 MCP Documentation Retrieval
- **Libraries Resolved:** `/jiquanzhong/context7`, `/modelcontextprotocol/python-sdk`, `/websites/modelcontextprotocol_io_specification_2025-11-25`
- **Queries Executed:** Tool naming conventions, integration patterns, client session management

### MCP Specification Review
- **Python SDK:** Tool decorators, handler patterns, structured output schemas
- **Specification Docs:** JSON Schema for tools, tools/list and tools/call API

---

## Findings

### Finding 1: MCP Tool Naming Convention in Claude Code

**Source:** Claude Code system documentation and observed behavior
**Confidence:** HIGH
**Relevance:** Critical for correct tool invocation

Claude Code exposes MCP server tools using a double-underscore naming convention:

```
mcp__<server-name>__<tool-name>
```

**Examples:**
- `mcp__context7__resolve-library-id` - Resolve library names to Context7 IDs
- `mcp__context7__query-docs` - Query documentation for a resolved library
- `mcp__memory-keeper__context_save` - Memory Keeper's save function

**Key Insight:** The server name comes from the MCP server configuration, and tool names are defined by the server's tool registration. This creates a namespaced hierarchy preventing tool name collisions across multiple MCP servers.

### Finding 2: Two-Phase Context7 Workflow

**Source:** `/jiquanzhong/context7` documentation via Context7 MCP
**Confidence:** HIGH
**Relevance:** Mandatory workflow pattern

Context7 requires a two-phase approach:

**Phase 1: Resolve Library ID**
```
mcp__context7__resolve-library-id(
    libraryName="<library-name>",
    query="<what you want to accomplish>"
)
```

**Returns:**
- Library title and Context7-compatible ID (format: `/org/project`)
- Description and code snippet count
- Source reputation (High, Medium, Low, Unknown)
- Benchmark score (0-100, higher is better)
- Available versions (optional)

**Phase 2: Query Documentation**
```
mcp__context7__query-docs(
    libraryId="<resolved-context7-id>",
    query="<specific question>"
)
```

**Returns:**
- Formatted documentation with code examples
- API references and integration patterns
- Version-specific information

**Skip Phase 1 Only When:**
- User explicitly provides library ID in format `/org/project`
- You have a previously resolved ID from the same session

### Finding 3: Library Selection Criteria

**Source:** Context7 resolve-library-id response metadata
**Confidence:** HIGH
**Relevance:** Ensures optimal documentation retrieval

When `resolve-library-id` returns multiple matches, select based on:

| Priority | Criterion | Description |
|----------|-----------|-------------|
| 1 | Name Match | Exact or closest name match to query |
| 2 | Source Reputation | HIGH > MEDIUM > LOW > UNKNOWN |
| 3 | Benchmark Score | Higher is better (max 100) |
| 4 | Code Snippets | More snippets = more examples |
| 5 | Version Match | If user specified version |

**Example Selection from Research:**
```
Query: "MCP tools integration patterns"

Results:
1. /modelcontextprotocol/python-sdk (Reputation: HIGH, Score: 89.2) <- SELECTED
2. /microsoft/mcp (Reputation: HIGH, Score: 61)
3. /jiquanzhong/context7 (Reputation: MEDIUM, Score: 63.8)
```

Selected `/modelcontextprotocol/python-sdk` due to highest benchmark score with HIGH reputation.

### Finding 4: MCP Server Tool Definition Pattern

**Source:** `/modelcontextprotocol/python-sdk` and MCP specification
**Confidence:** HIGH
**Relevance:** Understanding how tools are exposed

MCP tools are defined with JSON Schema for both input and output:

```python
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"},
                    "condition": {"type": "string"}
                },
                "required": ["temperature", "condition"]
            }
        )
    ]
```

**Key Patterns:**
1. **Descriptive Names:** Tool names should be verbs or verb phrases (`get_weather`, `resolve-library-id`)
2. **Clear Descriptions:** Must explain what the tool does and when to use it
3. **Schema Validation:** Both input and output validated against JSON Schema
4. **Required Fields:** Explicitly mark required parameters

### Finding 5: Agent Integration Best Practices

**Source:** Research synthesis from MCP SDK and Context7 documentation
**Confidence:** HIGH
**Relevance:** Practical implementation guidance

**Proactive Usage (SOP-CB.6):**
Context7 should be used PROACTIVELY, not as a fallback:

| Trigger Scenario | Action |
|------------------|--------|
| Installing/configuring a package | Use Context7 |
| Using unfamiliar API/SDK | Use Context7 |
| Implementing library-specific patterns | Use Context7 |
| Debugging library-related issues | Use Context7 |
| Checking for breaking changes | Use Context7 |

**Call Limit:**
Maximum 3 Context7 calls per question to prevent excessive API usage. If information not found after 3 calls, use best available result.

**Query Formulation:**
- Be specific: "How to write fixtures in pytest" vs "pytest"
- Include context: "React useEffect cleanup function examples"
- Avoid generic terms: "auth" or "hooks" are too vague

**Error Handling:**
If documentation not found:
```json
{
  "content": [{
    "type": "text",
    "text": "Documentation not found or not finalized for this library..."
  }]
}
```
Action: Try alternative library ID or WebSearch fallback.

### Finding 6: Multi-Server Coordination

**Source:** `/modelcontextprotocol/python-sdk` ClientSessionGroup documentation
**Confidence:** MEDIUM
**Relevance:** Advanced integration pattern

For agents using multiple MCP servers, naming hooks prevent collisions:

```python
def naming_hook(name: str, server_info) -> str:
    """Prefix component names with server name."""
    return f"{server_info.name}_{name}"

async with ClientSessionGroup(component_name_hook=naming_hook) as group:
    await group.connect_to_server(weather_server)
    await group.connect_to_server(database_server)

    # Tools now namespaced: weather_server_get_weather, database_server_query
    result = await group.call_tool("weather_server_get_weather", {"city": "London"})
```

**Claude Code Implementation:**
Claude Code implements similar namespacing via the `mcp__<server>__<tool>` convention, allowing multiple MCP servers to coexist without name conflicts.

---

## Analysis

### Integration Pattern for Claude Code Skills

Based on findings, the recommended integration pattern for skills/agents:

```markdown
## CONTEXT7 MCP INTEGRATION (SOP-CB.6)

When researching ANY library, framework, SDK, or API:

1. **Resolve Library ID First:**
   mcp__context7__resolve-library-id(libraryName="<library>", query="<question>")

2. **Query Documentation:**
   mcp__context7__query-docs(libraryId="<resolved-id>", query="<specific-question>")

**Selection Criteria:**
- Source Reputation: HIGH preferred
- Benchmark Score: Higher is better
- Code Snippets: More = more examples

**Call Limit:** Maximum 3 calls per question
```

### Decision Matrix: When to Use Context7 vs Other Sources

| Information Needed | Use Context7 | Use WebSearch | Use Codebase |
|--------------------|--------------|---------------|--------------|
| Library API docs | YES | No | No |
| Framework patterns | YES | No | No |
| SDK usage examples | YES | No | No |
| General concepts | No | YES | No |
| Project-specific code | No | No | YES |
| Current events/news | No | YES | No |
| Library changelog | YES | Fallback | No |

### Anti-Patterns to Avoid

1. **Skipping resolve-library-id:** Always resolve first unless ID explicitly provided
2. **Vague queries:** "hooks" is less useful than "React useEffect cleanup examples"
3. **Ignoring reputation:** Low reputation sources may have outdated documentation
4. **Exceeding call limit:** Stop after 3 calls, use best available information
5. **Fallback-only usage:** Use proactively, not as last resort

---

## Conclusions

1. **MCP Tool Naming:** Claude Code uses `mcp__<server>__<tool>` convention for namespacing
2. **Two-Phase Mandatory:** Always resolve-library-id -> query-docs unless ID known
3. **Proactive Usage:** Context7 should be used BEFORE code writing, not after failure
4. **Quality Selection:** Prioritize HIGH reputation + high benchmark score libraries
5. **Call Economics:** 3-call limit prevents API abuse while ensuring thorough research
6. **Multi-Server Safe:** Claude Code's namespacing prevents tool name collisions

---

## Recommendations

### Recommendation 1: Update SOP-CB.6 Documentation

**Rationale:** Current SOP-CB.6 covers the workflow but lacks selection criteria details.

**Action:** Add library selection criteria to SOP-CB.6:
```markdown
**SOP-CB.6.g.** Library Selection Criteria (when multiple matches):
1. Source Reputation: HIGH > MEDIUM > LOW
2. Benchmark Score: Higher preferred (max 100)
3. Code Snippets: More snippets = more examples
4. Version Match: Select version if user specified
```

### Recommendation 2: Add Context7 to Agent Prompt Templates

**Rationale:** Agents should have explicit Context7 integration instructions.

**Action:** Include in agent prompts:
```markdown
## CONTEXT7 MCP INTEGRATION

Before writing code using external libraries:
1. Resolve: mcp__context7__resolve-library-id(libraryName="X", query="what you need")
2. Query: mcp__context7__query-docs(libraryId="<resolved>", query="specific question")

Call limit: 3 per question
```

### Recommendation 3: Create Context7 Usage Checklist

**Rationale:** Consistent usage across all agents.

**Action:** Add to `.claude/rules/checklists.md`:
```markdown
## Before Using External Library (SOP-CB.6)

- [ ] Library ID resolved via Context7?
- [ ] Documentation queried for specific need?
- [ ] Selection based on reputation + score?
- [ ] Within 3-call limit?
```

---

## Knowledge Items Generated

### PAT-060: Context7 Two-Phase Workflow

**Category:** MCP Integration
**Applicability:** All Claude Code agents using external libraries

**Pattern:**
1. Always call `mcp__context7__resolve-library-id` first
2. Select library by: Reputation > Benchmark Score > Snippet Count
3. Call `mcp__context7__query-docs` with resolved ID
4. Maximum 3 calls per question

**Anti-pattern:** Guessing library IDs or skipping resolution phase.

### ASM-065: Context7 API Stability

**Assumption:** Context7 MCP tool interface (resolve-library-id, query-docs) remains stable.
**Context:** This research is based on current Context7 API behavior observed 2026-01-04.
**Impact:** If API changes, tool names or parameters may need updating.
**Confidence:** HIGH (MCP specification is versioned and backward compatible)

---

## PS Integration

**Entry ID:** e-119
**Classification:** research
**Artifact Path:** `docs/research/phase-38.17-e-119-context7-mcp-integration-patterns.md`

**Related Entries:**
- c-009: Sub-agent persistence enforcement (this research demonstrates compliance)
- SOP-CB.6: Context7 usage requirement

**Status Recommendation:** Mark e-119 as COMPLETE after artifact linking.

---

## Sources

1. **Context7 MCP Server Documentation** - `/jiquanzhong/context7` via Context7 MCP
   - resolve-library-id API specification
   - get-library-docs (query-docs) API specification
   - Library selection criteria

2. **Model Context Protocol Python SDK** - `/modelcontextprotocol/python-sdk` via Context7 MCP
   - Tool definition patterns and decorators
   - ClientSession management
   - Multi-server coordination with ClientSessionGroup

3. **MCP Specification** - `/websites/modelcontextprotocol_io_specification_2025-11-25` via Context7 MCP
   - tools/list and tools/call JSON-RPC API
   - JSON Schema for tool definitions
   - Input/output schema validation

4. **ECW SOP Documentation** - `.claude/rules/sop.md`
   - SOP-CB.6: Context7 proactive usage requirement

---

## 12. Validation Status (Soft Enforcement)

| Category | Status | Notes |
|----------|--------|-------|
| W-DIMENSION COVERAGE | 6/6 | WHO (agents), WHAT (Context7), WHERE (Claude Code), WHEN (proactive), WHY (accuracy), HOW (two-phase) |
| FRAMEWORK APPLICATION | 5/5 | 5W1H answered, decision matrix, patterns documented |
| EVIDENCE & GAPS | 4/4 | 4 sources cited, assumptions logged (ASM-065) |
| OUTPUT SECTIONS | 4/4 | Summary, findings, recommendations, knowledge items |

**Quality Status:** COMPLETE (19/19 criteria met)

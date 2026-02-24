# SPIKE-002 Phase 4: Integration Patterns Research

> ps-researcher-002 | Phase 4 | spike-eval-20260219-001
> Date: 2026-02-20
> Input: SPIKE-001 handoff (barrier-1), SPIKE-002 entity

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level findings for stakeholders |
| [L1: Pattern Analysis](#l1-pattern-analysis) | Four integration patterns with trade-off matrices |
| [L2: Comparative Assessment](#l2-comparative-assessment) | Cross-pattern comparison, migration paths, ecosystem fit |
| [References](#references) | Source traceability |

---

## L0: Executive Summary

This Phase 4 research evaluates four integration patterns for incorporating markdown-it-py + mdformat AST operations into Jerry's architecture. The patterns span Jerry's existing extension surfaces: CLI commands, Claude Code skills, MCP server tools, and a hybrid combining CLI with skills.

**Key finding:** Pattern D (Hybrid -- CLI for batch/CI + skill for interactive Claude operations) is the strongest fit for Jerry's architecture. It aligns with the existing hexagonal architecture (CLI as an interface adapter, skill as a separate interface adapter, both calling the same domain/application layer), avoids creating parallel tooling surfaces that diverge, and provides the most natural developer experience for both human operators (CLI) and Claude agents (skill).

Pattern C (MCP server) is technically viable and offers the cleanest tool-calling interface for Claude, but introduces operational complexity (server lifecycle management, transport configuration) disproportionate to the scope of AST operations. Pattern A (CLI-only) is the simplest to implement but forces Claude to shell out for every markdown operation, adding latency and losing structured data. Pattern B (skill-only) is the fastest path to Claude integration but leaves human operators without direct access and creates a maintenance surface invisible to standard development tooling.

---

## L1: Pattern Analysis

### Pattern A: Jerry CLI Extension

**Description:** Add a new `jerry ast` (or `jerry md`) command group to the existing Jerry CLI.

**Commands:**
```
jerry ast parse <file>           # Parse to AST JSON on stdout
jerry ast query <file> <jpath>   # Query AST nodes (JSONPath-like)
jerry ast transform <file> <op>  # Apply named transform (set-field, add-row, etc.)
jerry ast render <file>          # Re-render AST to markdown (roundtrip)
jerry ast validate <file>        # Validate against Jerry markdown schema
```

**Implementation:**

| Aspect | Assessment |
|--------|-----------|
| Implementation effort | Medium (~300 LOC CLI adapter + ~470 LOC domain extensions) |
| Token efficiency | Poor -- Claude must shell out via Bash tool, parse stdout text. AST JSON on stdout is verbose (a 100-line markdown file produces ~500-line JSON AST). Claude reads the full JSON output as text tokens. |
| Migration path | Existing skills would call `jerry ast` via Bash tool. Migration is straightforward but adds shell overhead per operation. |
| Developer experience | Excellent for humans (standard CLI patterns, scriptable, pipeable). Poor for Claude (stdout parsing, no structured return values, shell latency ~50-100ms per invocation). |
| Architecture fit | Good -- fits Jerry's hexagonal architecture as a new CLI adapter. Uses existing bootstrap/dispatcher pattern. |
| Testing | Easy -- CLI commands are testable via subprocess or by testing the adapter directly. |

**Strengths:**
1. Leverages Jerry's existing CLI infrastructure (Typer-based parser, CLIAdapter, bootstrap composition root)
2. Human-accessible: developers can debug markdown operations directly from terminal
3. Scriptable for CI/CD pipelines (e.g., `jerry ast validate --all` in pre-commit hooks)
4. Standard Unix patterns: pipe AST JSON through jq for ad-hoc queries

**Weaknesses:**
1. Token-inefficient for Claude: every operation requires Bash tool call + stdout parsing
2. No structured data exchange -- everything serialized to text and back
3. Shell overhead per invocation (~50-100ms) accumulates for multi-step AST workflows
4. AST JSON representation is verbose -- a parse-query-transform-render cycle would consume 4x the tokens of a direct API call

**Real-world precedent:** Microsoft's MarkItDown (https://github.com/microsoft/markitdown) follows this pattern -- a CLI tool for document-to-markdown conversion. It works well for batch conversion but required a separate MCP server package (markitdown-mcp) to integrate cleanly with Claude.

---

### Pattern B: Hidden Claude Skill (`/ast`)

**Description:** A Claude Code skill with SKILL.md that provides AST operations as skill instructions. Claude invokes it via `/ast` and follows the SKILL.md instructions to use the underlying Python library via `uv run`.

**Skill structure:**
```
skills/ast/
  SKILL.md           # Skill definition with parse/query/transform/render instructions
  scripts/
    ast_parse.py     # Parse markdown to JSON
    ast_query.py     # Query AST nodes
    ast_transform.py # Named transforms
    ast_render.py    # Re-render to markdown
    ast_validate.py  # Schema validation
```

**Implementation:**

| Aspect | Assessment |
|--------|-----------|
| Implementation effort | Low-Medium (~200 LOC scripts + ~470 LOC domain extensions + SKILL.md) |
| Token efficiency | Medium -- Claude still shells out via `uv run` but the skill instructions can optimize by combining operations (e.g., parse + transform + render in one script call). |
| Migration path | Other skills can reference `/ast` skill. Migration requires updating skill SKILL.md files to document AST dependency. |
| Developer experience | Excellent for Claude (natural skill invocation, instructions tailored to LLM). Poor for humans (skills are invisible to standard CLI tooling). |
| Architecture fit | Partial -- skills are a Claude Code interface, not a Jerry architecture component. The scripts bypass Jerry's hexagonal layers unless they import from the domain layer. |
| Testing | Harder -- skill behavior depends on Claude's interpretation of SKILL.md. Scripts are testable but the skill integration is not. |

**Strengths:**
1. Fastest path to Claude integration -- Claude already understands skill invocation patterns
2. Can bundle multi-step operations into single-instruction workflows (e.g., "update status field" as one skill action)
3. Skill instructions can include Jerry-specific context (which blockquote is frontmatter, what L2-REINJECT format looks like)
4. No CLI infrastructure changes needed

**Weaknesses:**
1. Invisible to humans -- no `jerry` CLI command for AST operations
2. Creates a parallel tooling surface that is harder to maintain (skill scripts vs CLI commands)
3. Scripts must still shell out via `uv run`, losing structured data benefits
4. Skill instructions are prompt-based, not programmatically testable
5. If scripts import from Jerry's domain layer, they create an architectural coupling between the skill filesystem and Jerry's Python packages

**Real-world precedent:** Claude Code's built-in skills (https://code.claude.com/docs/en/skills) follow this pattern. Anthropic's public skill repository (https://github.com/anthropics/skills) demonstrates the pattern for code analysis, but not for AST manipulation specifically.

---

### Pattern C: MCP Server

**Description:** An MCP server exposing AST operations as tools, running as a local process. Claude discovers and calls the tools via the MCP protocol.

**MCP tools:**
```
ast_parse(file_path) -> { ast: ASTNode[], metadata: {...} }
ast_query(file_path, selector) -> { nodes: ASTNode[] }
ast_transform(file_path, operation, params) -> { success: bool, diff: string }
ast_render(ast_json) -> { markdown: string }
ast_validate(file_path, schema) -> { valid: bool, errors: [...] }
frontmatter_get(file_path) -> { fields: { key: value, ... } }
frontmatter_set(file_path, key, value) -> { success: bool, diff: string }
reinject_list(file_path) -> { blocks: [...] }
reinject_update(file_path, rank, content) -> { success: bool }
```

**Implementation:**

| Aspect | Assessment |
|--------|-----------|
| Implementation effort | Medium-High (~400 LOC MCP server + ~470 LOC domain extensions + transport config) |
| Token efficiency | Excellent -- structured JSON tool responses. No stdout parsing. Claude receives typed data directly. Only the relevant AST subset is returned, not the full JSON representation. |
| Migration path | Existing skills do not need modification -- Claude discovers MCP tools automatically. However, the MCP server must be running during Claude sessions. |
| Developer experience | Good for Claude (native tool calling, structured I/O, automatic discovery). Moderate for humans (can test via MCP CLI tools, but not via standard `jerry` commands). |
| Architecture fit | Clean -- MCP server is a separate interface adapter in hexagonal terms. It imports from Jerry's domain/application layer and exposes operations via MCP protocol. |
| Testing | Good -- MCP tools are functions with typed inputs/outputs, testable in isolation. MCP Python SDK (https://github.com/modelcontextprotocol/python-sdk) provides testing utilities. |

**Strengths:**
1. Best token efficiency -- structured JSON responses, no text parsing overhead
2. Automatic tool discovery -- Claude sees available operations without explicit skill loading
3. Clean separation of concerns -- MCP server is a dedicated interface adapter
4. Can serve high-level domain operations (frontmatter_get, frontmatter_set) alongside low-level AST operations
5. FastMCP framework (https://github.com/jlowin/fastmcp) makes Python MCP servers trivial to implement (~50 LOC for basic server)

**Weaknesses:**
1. Operational complexity -- MCP server must be running during Claude sessions (server lifecycle management)
2. Transport configuration -- requires `claude_desktop_config.json` or equivalent Claude Code MCP config
3. Debugging is harder -- MCP tool calls are less visible than CLI commands in session logs
4. Introduces a runtime dependency (server process) that the current Jerry architecture does not have
5. Version coupling -- MCP server must stay in sync with Jerry domain layer changes

**Real-world precedent:** Microsoft's markitdown-mcp (https://pypi.org/project/markitdown-mcp/) demonstrates the pattern of wrapping a markdown tool as an MCP server. The MCP Python SDK (https://modelcontextprotocol.io/docs/develop/build-server) provides the standard implementation pattern.

---

### Pattern D: Hybrid (CLI + Skill)

**Description:** CLI commands for batch/CI operations + a thin skill layer that calls the same Python domain layer directly. Both the CLI adapter and the skill scripts import from the same domain/application layer, ensuring a single source of truth for AST logic.

**Architecture:**
```
src/
  domain/markdown_ast/        # Domain layer: AST operations, JerryDocument
    jerry_document.py         # Facade: parse, query, transform, render
    frontmatter.py            # Blockquote frontmatter extraction/write-back
    reinject.py               # L2-REINJECT parser
    nav_table.py              # Navigation table helpers
    schema.py                 # Jerry markdown schema definitions
  application/markdown_ast/   # Application layer: use cases
    parse_document.py         # ParseDocumentCommand + Handler
    query_nodes.py            # QueryNodesQuery + Handler
    transform_document.py     # TransformDocumentCommand + Handler
    validate_document.py      # ValidateDocumentQuery + Handler
  interface/cli/              # CLI adapter (existing, extended)
    ast_commands.py           # jerry ast parse|query|transform|render|validate

skills/ast/
  SKILL.md                    # Skill definition
  scripts/
    ast_ops.py                # Thin wrapper: imports from domain layer, runs ops
```

**Implementation:**

| Aspect | Assessment |
|--------|-----------|
| Implementation effort | Medium (~250 LOC CLI adapter + ~150 LOC skill scripts + ~470 LOC domain extensions) |
| Token efficiency | Good -- skill scripts call domain layer directly via `uv run`, can return structured output. CLI commands available for batch but not the primary Claude path. |
| Migration path | Best -- existing skills can either call `jerry ast` CLI (simple) or import the domain layer (optimal). Gradual migration possible: start with CLI calls, later switch to direct imports. |
| Developer experience | Excellent for both humans (CLI) and Claude (skill with domain-aware instructions). |
| Architecture fit | Excellent -- follows hexagonal architecture perfectly. Domain layer is the SSOT. CLI and skill are both interface adapters. No architectural coupling violations. |
| Testing | Excellent -- domain layer is testable independently. CLI adapter testable via adapter tests. Skill scripts testable as Python modules. |

**Strengths:**
1. Single source of truth: domain layer contains all AST logic; both CLI and skill are thin adapters
2. Aligns perfectly with Jerry's hexagonal architecture (H-07, H-08, H-09)
3. Humans get CLI access; Claude gets skill access; both use the same logic
4. Gradual migration: skills can start by calling `jerry ast` CLI, later switch to direct domain imports
5. CI/CD integration via CLI (`jerry ast validate --all` in pre-commit hooks)
6. Skill instructions can include domain context that Claude needs (Jerry-specific markdown patterns)
7. No runtime server dependency (unlike MCP)

**Weaknesses:**
1. Two interface surfaces to maintain (CLI + skill), though the domain layer is shared
2. Skill scripts that import from Jerry's domain layer create a dependency from the skill filesystem to Jerry's Python packages -- this must be managed carefully
3. Slightly more implementation effort than Pattern B alone
4. Token efficiency is good but not optimal (still requires `uv run` invocation)

**Real-world precedent:** This is the standard pattern for tools that serve both human and AI consumers. Anthropic's agent skills documentation (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) recommends skills as a complementary interface alongside existing tool surfaces.

---

## L2: Comparative Assessment

### Cross-Pattern Comparison Matrix

| Criterion | A: CLI Only | B: Skill Only | C: MCP Server | D: Hybrid |
|-----------|:----------:|:------------:|:-------------:|:---------:|
| Implementation effort | Medium | Low-Medium | Medium-High | Medium |
| Token efficiency | Poor | Medium | Excellent | Good |
| Human DX | Excellent | Poor | Moderate | Excellent |
| Claude DX | Poor | Excellent | Excellent | Good-Excellent |
| Architecture fit | Good | Partial | Clean | Excellent |
| Migration path | Straightforward | Skill-only | Automatic | Best (gradual) |
| Testing | Easy | Harder | Good | Excellent |
| Operational complexity | Low | Low | Medium-High | Low |
| CI/CD integration | Excellent | None | Moderate | Excellent |
| Maintenance burden | Single surface | Single surface | Dual (server + sync) | Dual (CLI + skill) |

### Token Efficiency Deep Dive

For a representative operation (update Status field in WORKTRACKER entity file, ~50 lines):

| Pattern | Tokens consumed (estimate) | Breakdown |
|---------|:-------------------------:|-----------|
| **Current (raw text)** | ~800-1200 | Read full file (~400 tokens) + Edit tool call (~200 tokens) + verification read (~400 tokens) |
| **A: CLI** | ~600-900 | Bash call (~100) + parse stdout (~300) + transform call (~100) + render stdout (~300) |
| **B: Skill** | ~400-600 | uv run combined script (~100) + output parsing (~200) + verification (~200) |
| **C: MCP** | ~200-350 | frontmatter_get tool call (~50) + frontmatter_set call (~100) + structured response (~100) |
| **D: Hybrid** | ~350-500 | Skill script call (~100) + domain layer ops (~150) + structured output (~150) |

**Key insight:** The current approach (Read file + Edit tool + verify) is already reasonably token-efficient for simple field updates. The AST approach's primary advantage is not token savings on individual operations but rather: (1) structural correctness guarantees, (2) batch operations across multiple files, (3) schema validation at parse time, and (4) the ability to perform complex transformations (e.g., "add a row to the history table in all WORKTRACKER files matching Status: in_progress") that are error-prone with raw text.

### Migration Path Analysis

Jerry has ~15 skills (6 active: worktracker, adversary, problem-solving, nasa-se, orchestration, transcript) and 30+ agent definitions. Markdown operations are concentrated in:

| Consumer | Current Approach | AST Migration Effort |
|----------|-----------------|---------------------|
| /worktracker agents | Read + Edit (regex-style find/replace on frontmatter) | Low -- direct replacement with frontmatter_get/set |
| /orchestration agents | Read + Write (full file replacement for YAML/MD state) | Low -- YAML files unchanged; MD state files use AST |
| /adversary agents | Read only (scoring deliverables) | Minimal -- read-only AST queries for structure validation |
| /nasa-se agents | Read + Write (templates, reports) | Medium -- template instantiation benefits from AST |
| /transcript agents | Read + Write (meeting notes generation) | Low -- generation is write-once, not parse-modify-render |
| .claude/rules/ | Read by Claude Code (auto-loaded) | None -- rules are consumed, not modified programmatically |

**Migration strategy for Pattern D:**
1. **Phase 1 (Week 1-2):** Implement domain layer + CLI adapter. No skill changes.
2. **Phase 2 (Week 3):** Add `/ast` skill with thin scripts. Worktracker agents migrate first (highest value: frontmatter manipulation).
3. **Phase 3 (Week 4+):** Remaining skills migrate opportunistically. Schema validation added to CI.

### Recommendation

**Pattern D (Hybrid)** is recommended based on:

1. **Architecture alignment** -- Only pattern that fully respects Jerry's hexagonal architecture (domain layer as SSOT, CLI and skill as interface adapters)
2. **Dual-audience DX** -- Serves both human operators and Claude agents without compromise
3. **Gradual migration** -- Skills can migrate incrementally; no big-bang switchover required
4. **CI/CD integration** -- CLI commands enable pre-commit validation hooks
5. **No operational overhead** -- Unlike MCP, no server process to manage

**If token efficiency becomes critical:** Consider adding MCP server as a third interface adapter (Pattern D+C hybrid). The domain layer is the same; MCP is just another adapter. This can be deferred until evidence shows the skill-based invocation is a token bottleneck.

---

## References

| Source | Content | URL |
|--------|---------|-----|
| SPIKE-001 Handoff | Library recommendation, extension requirements, risk R-01 | `cross-pollination/barrier-1/spike-001-handoff.md` |
| SPIKE-002 Entity | Research question, hypothesis, scope | `work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/SPIKE-002-feasibility/SPIKE-002-feasibility.md` |
| Jerry CLI main.py | Current CLI architecture (Typer, hexagonal, bootstrap) | `src/interface/cli/main.py` |
| Microsoft MarkItDown | CLI + MCP pattern precedent | https://github.com/microsoft/markitdown |
| markitdown-mcp | MCP server wrapper pattern | https://pypi.org/project/markitdown-mcp/ |
| MCP Python SDK | Official MCP server implementation | https://github.com/modelcontextprotocol/python-sdk |
| FastMCP | Pythonic MCP server framework | https://github.com/jlowin/fastmcp |
| Claude Code Skills | Skill definition and structure | https://code.claude.com/docs/en/skills |
| Anthropic Skills Repo | Public skill examples | https://github.com/anthropics/skills |
| Claude Agent Skills | Agent skill architecture | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview |

---

*Phase 4 Architecture Research. ps-researcher-002. spike-eval-20260219-001.*

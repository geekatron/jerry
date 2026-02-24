# SPIKE-001: Claude SDK vs CLI Instance Comparison

> **Type:** spike
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 12

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research question, hypothesis, scope |
| [Comparison Framework](#comparison-framework) | Dimensions and scoring |
| [Findings](#findings) | Results (populated after research) |
| [Recommendation](#recommendation) | Decision (populated after research) |
| [Related Items](#related-items) | Hierarchy |
| [History](#history) | Status changes |

---

## Content

### Research Question

**Question:** Should Jerry use the Python Claude SDK (Anthropic Agent SDK), Claude Code CLI subprocess spawning, or a hybrid approach for automated multi-instance management — and what are the capabilities, limitations, and trade-offs of each?

### Hypothesis

We hypothesize that:
1. The Claude SDK provides full API control (model selection, tool definitions, system prompts, streaming) but may lack Claude Code's built-in tooling (file operations, git, glob, grep)
2. CLI spawning preserves Claude Code's full tool surface but may be harder to control programmatically (I/O parsing, session state, error handling)
3. A hybrid approach (SDK for orchestration logic, CLI for execution) may combine the strengths of both
4. The Claude Code `--print` flag or headless mode may enable simpler CLI automation than full interactive sessions
5. Cost implications differ: SDK = direct API token costs, CLI = includes Claude Code overhead

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox Duration | 12 hours |
| Start Date | TBD |
| Target End Date | TBD |

### Scope

**In Scope:**
- Python Claude SDK (Anthropic SDK) capabilities: model invocation, tool use, streaming, context management, agent loops
- Anthropic Agent SDK capabilities: multi-agent orchestration, handoffs, tool delegation
- Claude Code CLI automation: `--print` mode, `-p` prompt flag, `--output-format json`, subprocess management
- Claude Code headless/non-interactive operation modes
- Programmatic session lifecycle: start, send prompts, receive responses, checkpoint, terminate
- Tool surface comparison: what tools does each approach have access to?
- Cost analysis: API pricing vs CLI overhead
- Error handling and resilience: what happens when an instance fails?
- Use Context7 for latest Claude SDK and Agent SDK documentation
- Use Web Search for latest Claude Code CLI flags, automation patterns, and community practices
- Evidence (sources, references, citations) required for all findings

**Out of Scope:**
- Worktree automation (that's SPIKE-002)
- Full control plane design (future feature)
- Non-Anthropic providers

### Research Approach

1. **SDK capabilities audit:** Use Context7 + Web Search to document the latest Python Claude SDK and Agent SDK APIs. Focus on: instance creation, tool use definition, system prompts, streaming, multi-turn conversations, context window management, session persistence.
2. **CLI automation audit:** Document Claude Code CLI flags for non-interactive use (`--print`, `-p`, `--output-format`, `--allowedTools`, `--model`, etc.). Investigate subprocess management patterns, stdout/stderr parsing, exit codes.
3. **Tool surface comparison:** Map the tool surface available to each approach. SDK = custom tool definitions. CLI = built-in tools (Read, Write, Edit, Glob, Grep, Bash, etc.). Identify gaps in each direction.
4. **Prototype both:** Build minimal Python scripts that (a) use the SDK to invoke Claude with a tool, (b) spawn a CLI process and send a prompt. Compare developer experience, reliability, error handling.
5. **Cost modeling:** Estimate token costs for a representative multi-instance workflow (e.g., 3 projects, 5 agents each). SDK = direct API tokens. CLI = API tokens + overhead.
6. **Hybrid design:** Sketch a hybrid architecture where SDK handles orchestration/routing and CLI handles execution. Assess complexity vs benefit.
7. **Scoring:** Apply comparison framework to produce ranked recommendation.

---

## Comparison Framework

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Programmatic Control | 0.20 | API surface for creating, configuring, and managing instances |
| Tool Surface | 0.20 | Built-in tools available (file ops, git, search, etc.) |
| Session Persistence | 0.15 | Ability to persist and resume sessions across process lifecycle |
| Error Handling | 0.10 | Failure detection, retry, graceful degradation |
| Developer Experience | 0.10 | Ease of implementation, debugging, testing |
| Cost Efficiency | 0.10 | Token costs and operational overhead |
| Integration with Jerry | 0.10 | Fit with existing CLI, skills, and /orchestration |
| Scalability | 0.05 | Ability to manage 5-10+ concurrent instances |

---

## Findings

_To be populated after research._

---

## Recommendation

_To be populated after research._

---

## Execution Structure

**Parallel-with-sync-point:** SPIKE-001 and SPIKE-002 execute in parallel within an orchestrated cross-pollinated pipeline. Research phases run concurrently; findings cross-pollinate at sync barriers before analysis phases proceed.

| Phase | SPIKE-001 Work | Sync Point |
|-------|---------------|------------|
| Phase 1 (Research) | SDK capabilities audit + CLI automation audit | Barrier 1: Send instance approaches to SPIKE-002; receive worktree constraints from SPIKE-002 |
| Phase 2 (Analysis) | Trade-off scoring on 8 dimensions, informed by worktree constraints | Barrier 2: Send scored recommendation to SPIKE-002; receive session lifecycle feasibility |
| Phase 3 (Decision) | Convergent: ps-architect creates go/no-go ADR from both spikes | — |

See `ORCHESTRATION_PLAN.md` for full workflow diagram.

---

## Related Items

- Parent: [FEAT-001: Multi-Instance Strategy Assessment](./FEAT-001-instance-strategy.md)
- Parallel With: [SPIKE-002: Automated Worktree & Session Lifecycle](./SPIKE-002-worktree-lifecycle.md) (cross-pollinated pipeline)
- Related: PROJ-004 context resilience — session lifecycle overlaps

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Spike defined. 7-step research approach with 8-dimension comparison framework. 12h timebox. |
| 2026-02-20 | pending | Restructured: parallel-with-sync-point execution with SPIKE-002. Orchestration plan created. |

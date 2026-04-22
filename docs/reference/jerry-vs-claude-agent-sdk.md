# Jerry vs. Claude Agent SDK

> Comparison reference for users evaluating Jerry Framework and Claude Agent SDK.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (R-01 through R-07) -->
<!-- Anti-patterns to avoid: RAP-01 (marketing claims), RAP-02 (instructions/recipes), RAP-03 (narrative explanation) -->
<!-- Voice: Neutral, precise, austere. No opinions, no superlatives. See Section 5. -->
<!-- REM-036 — Wave 2, W2-10. Verified SDK facts from code.claude.com/docs/en/agent-sdk/overview, 2026-04-20. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Framing and scope |
| [Comparison Table](#comparison-table) | Side-by-side dimensions |
| [When to Choose Jerry](#when-to-choose-jerry) | Selection criteria for Jerry |
| [When to Choose Claude Agent SDK](#when-to-choose-claude-agent-sdk) | Selection criteria for the SDK |
| [Using Them Together](#using-them-together) | Composability patterns |

---

## Overview

This page compares Jerry Framework and the Claude Agent SDK. They solve different problems at different abstraction levels; most users do not choose between them.

Jerry is a Claude Code plugin. The Claude Agent SDK is a Python and TypeScript library for building applications. A user who opens Claude Code daily and a developer building a production pipeline are not choosing the same tool — they operate at different layers of the same platform.

---

## Comparison Table

| Dimension | Jerry | Claude Agent SDK |
|---|---|---|
| **What it is** | A Claude Code plugin. Installed via the Claude Code plugin marketplace. Extends Claude Code with pre-built skills, behavioral guardrails, and persistent memory. | A Python and TypeScript library (`claude-agent-sdk`). Installed via `pip` or `npm`. Provides programmatic access to the Claude Code agent loop. |
| **Primary deployment surface** | Claude Code interactive sessions. Invoked by the user or by Claude during a session. | Any Python or TypeScript application: CI/CD pipelines, web services, automation scripts, custom agents. |
| **Content provided** | 30 skills (methodology libraries) and 88 agents covering problem-solving, work tracking, documentation, systems engineering, security, UX, and more. Rules, templates, and quality standards are included. | Primitives: a `query()` function, `ClaudeAgentOptions`, built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch), hooks, subagent support, and MCP integration. No pre-built domain skills. |
| **Ready-to-use capabilities** | Skills are invocable immediately after installation: `/problem-solving`, `/diataxis`, `/eng-team`, `/red-team`, `/worktracker`, and 25 others. No code required to use them. | Built-in tools are available immediately. Domain capabilities (e.g., a code-review agent, a research agent) must be implemented by the developer. Example agents are provided as starting points. |
| **Customization model** | New skills are added by creating a `skills/{name}/SKILL.md` file and registering the skill in `CLAUDE.md`, `AGENTS.md`, and `mandatory-skill-usage.md`. No code required; skills are defined in markdown. | Customization is code-level: implement custom tools, configure `ClaudeAgentOptions`, define hooks via callback functions, connect MCP servers, and compose subagents programmatically. |
| **Persistence model** | Filesystem-based. Rules, worktracker entries, knowledge documents, and decision records persist to disk under the project tree. Survives session boundaries and context compaction. Called "filesystem as infinite memory" in the codebase. | Programmable. Sessions can be persisted and resumed via a `session_id`. State management and storage are the responsibility of the application developer. |
| **Quality gates** | Built-in: creator-critic-revision cycle (minimum 3 iterations for C2+ work), quality threshold >= 0.92, 10 adversarial strategy templates, and a strategy catalog (S-001 through S-014). Enforced by rule files loaded at session start. | None provided. The SDK is unopinionated about quality processes. Quality gates, review cycles, and scoring are implemented by the developer if desired. |
| **Context management** | Addresses Context Rot (LLM performance degradation as context fills) by loading rules, knowledge, and skills selectively per task. Progressive disclosure: Tier 1 (frontmatter, always loaded), Tier 2 (skill body, loaded when relevant), Tier 3 (references, loaded on demand). | Provides session management and context continuation via `session_id`. Context window management within a session is handled by Claude Code's agent loop. The developer controls what is in the prompt. |
| **Target user** | Claude Code users who want pre-built methodology, quality enforcement, and persistent knowledge management without writing code. | Developers building bespoke agents, pipelines, or products that embed Claude Code capabilities programmatically. |
| **Languages** | Not applicable. Jerry is configuration and markdown. No programming language required to use it. | Python and TypeScript. Both SDKs are maintained with feature parity. |

---

## When to Choose Jerry

Jerry fits when:

- The primary working environment is Claude Code interactive sessions, not a custom application.
- Pre-built methodology is preferable to building from primitives (skills like `/problem-solving`, `/eng-team`, `/diataxis`, `/nasa-se`, `/red-team` are ready to use without implementation).
- Work item tracking, persistent decisions, and cross-session knowledge accrual are needed without infrastructure setup.
- Quality enforcement (creator-critic-revision cycles, quality thresholds, adversarial review templates) is required without implementing it.
- The team uses slash command invocation (`/worktracker`, `/orchestration`, etc.) rather than writing agent code.

Example: A developer who wants Claude to research, analyze, and produce documented decisions across multiple sessions, with quality gates and persistent knowledge — without writing a pipeline.

---

## When to Choose Claude Agent SDK

The Claude Agent SDK fits when:

- The goal is a standalone application, service, or pipeline that runs Claude autonomously without a human-in-the-loop Claude Code session.
- Integration with existing code is required (the SDK is imported as a library and composed with application logic).
- Deployment targets include CI/CD systems, web servers, scheduled jobs, or any environment where Claude Code the interactive tool is not present.
- Custom tool implementations, custom hooks, or custom agent topologies are needed that go beyond what Jerry skills cover.
- The product being built will be distributed to end users who do not use Claude Code themselves.

Example: A developer building a pull-request reviewer that runs on every commit, fetches the diff, calls Claude via the SDK, and posts a comment — this is a production application that does not involve an interactive Claude Code session.

---

## Using Them Together

Jerry and the Claude Agent SDK operate at different layers and are composable.

Jerry runs inside Claude Code sessions. The Claude Agent SDK runs in application code. A team can use both without conflict:

- **Jerry for interactive development**: Use Jerry skills (`/problem-solving`, `/architecture`, `/eng-team`) during design and development sessions in Claude Code.
- **SDK for production automation**: Deploy SDK-based agents to run in pipelines, services, or scheduled jobs that perform the same categories of work (research, analysis, code review) with custom implementation.
- **Jerry as a design reference**: Jerry's skill definitions (in `skills/*/agents/*.md`), quality criteria (in `.context/rules/quality-enforcement.md`), and agent design standards (in `.context/rules/agent-development-standards.md`) can serve as a reference for teams implementing similar methodology in SDK-based agents.
- **SDK for custom Jerry extensions**: Developers who want to build production tools informed by Jerry's methodology can use the SDK to implement pipelines that replicate Jerry's quality gates programmatically.

Jerry is not a replacement for the Claude Agent SDK. The two tools address different use cases and different deployment contexts.

---

## Related

- **Installation:** [Installation Guide](../INSTALLATION.md) — Install Jerry as a Claude Code plugin
- **Getting Started:** [Getting Started Runbook](../runbooks/getting-started.md) — First project and first skill invocation
- **Contributing:** [Contributing Guide](https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md) — Including how to contribute new skills
- **External:** [Claude Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview) — Official Anthropic documentation

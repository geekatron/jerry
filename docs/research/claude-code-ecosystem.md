# Claude Code Ecosystem

> Research on Claude Code CLI patterns, plugin architecture and distribution, skill structure and agent design patterns — the ecosystem knowledge underpinning Jerry's implementation.

---

## Key Findings

- **Agentic architecture** with hooks system, session management, and configuration layering provides the foundation for framework-level guardrails
- **Plugin architecture** supports directory-based structure, manifest-driven configuration, and marketplace distribution via remote installation
- **Skill structure** follows a SKILL.md schema with multi-agent patterns constrained by P-003 (no recursive subagents)
- **MCP (Model Context Protocol)** integration enables tool extension beyond the built-in tool set

---

## Claude Code CLI Best Practices

Research into the Claude Code CLI's architecture, including its agentic loop, hooks system, and configuration layering.

??? note "Methodology"
    Analyzed Claude Code CLI documentation, source patterns, and runtime behavior. Structured as L0 (executive summary) and L1 (technical details) for multi-audience access.

??? abstract "Key Data"
    - 881 lines with L0/L1 structure
    - Agentic architecture analysis: tool loop, context management, permission model
    - Hooks system: pre/post tool execution, session lifecycle events
    - Session management patterns and state persistence
    - Configuration layering: project → user → system defaults
    - MCP integration: tool servers, resource providers

[:octicons-link-external-16: CLI Best Practices (881 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-claude-code/claude-code-best-practices.md)

---

## Claude Code Plugins Best Practices

Research into the plugin architecture, directory structure, manifest format, and distribution patterns.

??? note "Methodology"
    Analyzed Claude Code plugin system documentation and existing plugin implementations. Cataloged directory structure conventions, manifest format requirements, and distribution patterns (local, git, marketplace).

??? abstract "Key Data"
    - 675 lines with L0/L1 structure
    - Plugin directory structure and manifest format
    - Distribution patterns: local, git, marketplace (remote install)
    - Security model: plugin permissions, tool restrictions
    - Versioning and compatibility requirements

[:octicons-link-external-16: Plugins Best Practices (675 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-plugins/plugins-best-practices.md)

---

## Claude Code Skills Best Practices

Research into skill structure, the SKILL.md schema, multi-agent patterns, and the P-003 nesting constraint.

??? note "Methodology"
    Analyzed SKILL.md schema patterns across multiple Claude Code skill implementations. Documented multi-agent patterns, activation keyword conventions, and the P-003 nesting constraint through empirical testing.

??? abstract "Key Data"
    - 718 lines with L0/L1 structure
    - SKILL.md schema: required sections, activation keywords, agent registry
    - Multi-agent patterns within skills: sequential chain, fan-out/fan-in, creator-critic
    - P-003 constraint: max one level of nesting (orchestrator → worker)
    - Portability considerations for cross-project skill reuse

[:octicons-link-external-16: Skills Best Practices (718 lines)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-skills/skills-best-practices.md)

---

## Related Research

- [Skill Compliance Framework](skill-compliance-framework.md)
- [Context Management](context-management.md)
- [Architecture Patterns](architecture-patterns.md)

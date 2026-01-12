# Polyglot Architecture Analysis: TypeScript at the Network Layer

**Document ID**: RESEARCH-002
**Date**: 2026-01-07
**Author**: Claude (Distinguished Systems Engineering Persona)
**Status**: APPROVED - Proceed with hybrid approach
**Depends On**: RESEARCH-001 (Technology Stack Analysis)

---

## Executive Summary

This document analyzes whether TypeScript should be used at the network/interface layer alongside Python for the core domain. The analysis concludes that a **polyglot approach is architecturally sound** and recommended for specific use cases, particularly MCP (Model Context Protocol) servers.

**Recommendation**: Python-first with TypeScript adapters where ecosystem demands it.

---

## 1. The Question

> "Would TypeScript help us? Is this something that would be useful at our Network layer?"

In hexagonal architecture terms, the "network layer" comprises:
- **Primary Adapters** (driving): CLI, HTTP API, MCP servers, WebSocket handlers
- **Secondary Adapters** (driven): External API clients, message queues

---

## 2. Evidence: MCP Ecosystem Analysis

### 2.1 MCP SDK Support

Per [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25) and [GitHub](https://github.com/modelcontextprotocol):

| SDK | Status | Monthly Downloads |
|-----|--------|-------------------|
| TypeScript | Official | 97M+ (combined with Python) |
| Python | Official | 97M+ (combined with TypeScript) |
| C# | Official | Available |
| Java | Official | Available |

**Both are first-class citizens.** No technical advantage to either for MCP.

### 2.2 Community Adoption (GitHub Hexagonal Repos)

Per [GitHub Topics](https://github.com/topics/hexagonal-architecture):

| Language | Repositories |
|----------|--------------|
| Java | 578 |
| TypeScript | 356 |
| Go | 317 |
| Python | 110 |

TypeScript has 3x more hexagonal architecture examples than Python, indicating stronger community patterns for this architecture in TS.

### 2.3 Claude Code Best Practices

Per [htdocs.dev](https://htdocs.dev/posts/claude-code-full-stack-configuration-guide/):

> "A state-of-the-art setup for Claude Code in a modern full-stack project often focuses on a TanStack/TypeScript front-end with a Python back-end (Dockerized)."

Per [ClaudeLog](https://claudelog.com/faqs/what-programming-languages-work-best-with-claude-code/):

> "Python and JavaScript/TypeScript show the strongest community satisfaction and performance with Claude Code."

---

## 3. Architectural Analysis

### 3.1 Hexagonal Architecture Enables Polyglot

Per [Sairyss/domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon):

> "Patterns and principles presented are framework/language agnostic, so these technologies can be easily replaced with any alternative."

Per [TSH Blog](https://tsh.io/blog/hexagonal-architecture):

> "Since ports are essentially just gateways, adapters are necessary to actually make the communication happen. The adapters actively initiate the communication."

**Key Insight**: The hexagonal pattern explicitly supports different languages at the adapter level. The port (interface contract) is the boundary—adapters can be implemented in any language that satisfies the contract.

### 3.2 Polyglot Boundary Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    NETWORK/INTERFACE LAYER                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ CLI Adapter │  │ MCP Server  │  │ Future Web UI           │ │
│  │  (Python)   │  │(TypeScript) │  │ (TypeScript)            │ │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘ │
└─────────┼────────────────┼─────────────────────┼───────────────┘
          │                │                     │
          │    ┌───────────┴──────────┐          │
          │    │    IPC / JSON-RPC    │          │
          │    └───────────┬──────────┘          │
          │                │                     │
┌─────────┼────────────────┼─────────────────────┼───────────────┐
│         ▼                ▼                     ▼               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    PORTS (Interfaces)                    │   │
│  │              Python typing.Protocol / ABC                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    DOMAIN CORE                           │   │
│  │                    (Pure Python)                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         PYTHON                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 IPC Mechanisms for Python ↔ TypeScript

| Mechanism | Latency | Complexity | Use Case |
|-----------|---------|------------|----------|
| **Subprocess + JSON** | Low | Low | CLI invocation |
| **HTTP/REST** | Medium | Medium | Decoupled services |
| **JSON-RPC over stdio** | Very Low | Low | MCP pattern |
| **Unix Socket** | Very Low | Medium | Local high-perf |

The MCP protocol itself uses JSON-RPC over stdio—this is the canonical pattern for connecting TypeScript MCP servers to Python backends.

---

## 4. Honest Assessment

### 4.1 Arguments FOR TypeScript at Network Layer

| Argument | Strength | Evidence |
|----------|----------|----------|
| MCP ecosystem maturity | Medium | Both SDKs are official; TS has more examples |
| Type safety at API boundary | Strong | Zod + TypeScript catches contract violations at compile time |
| Future web UI capability | Strong | If Jerry ever needs browser components |
| Claude Code satisfaction | Strong | TS shows strong community satisfaction |
| Gateway pattern fit | Strong | Industry pattern for polyglot boundaries |

### 4.2 Arguments AGAINST TypeScript at Network Layer

| Argument | Strength | Evidence |
|----------|----------|----------|
| Added complexity | Strong | Two runtimes, two dependency systems, IPC overhead |
| Not needed for MVP | Strong | Work Tracker can be CLI-only initially |
| Python MCP SDK exists | Strong | We CAN do MCP in Python if needed |
| Context cost | Medium | More code = more tokens in context |
| Debugging difficulty | Medium | Cross-language stack traces are harder |

### 4.3 Self-Critique

**Potential bias**: I may be over-engineering by suggesting polyglot when Python-only would work.

**Counter-argument**: The hexagonal architecture's entire value proposition is enabling this flexibility. If we design ports correctly, adding a TypeScript MCP adapter later is trivial.

---

## 5. Recommendation

### 5.1 Phased Approach

| Phase | Network Layer | Rationale |
|-------|---------------|-----------|
| **MVP (Now)** | Python CLI only | Simplicity, validate core domain |
| **v0.2** | Python MCP server | Test MCP in Python first |
| **v0.3+** | TypeScript MCP if needed | Only if Python MCP proves inadequate |

### 5.2 Architectural Preparation

Even if we start Python-only, we should:

1. **Define ports as JSON-serializable contracts** - Enables any language adapter
2. **Use JSON-RPC patterns in CLI** - Same protocol MCP uses
3. **Keep `scripts/` thin** - Shims that just invoke domain, easy to replace
4. **Document IPC contract** - In `infrastructure/schemas/`

### 5.3 When to Add TypeScript

Add TypeScript adapters when:
- [ ] Python MCP server proves insufficient (performance, ecosystem)
- [ ] Web UI is required (browser-native)
- [ ] Integration with TypeScript-only tools needed
- [ ] Team prefers TypeScript for specific adapter

### 5.4 Directory Structure Implication

Your proposed structure already accommodates this:

```
jerry/
├── src/                          # Python hexagonal core
│   └── interface/
│       ├── cli/                  # Python CLI adapter (MVP)
│       └── api/                  # Python API adapter (future)
│
├── adapters/                     # OPTIONAL: Non-Python adapters
│   └── mcp-server/               # TypeScript MCP (if needed later)
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
│           └── index.ts
│
└── scripts/                      # CLI shims (Python, invoke src/)
```

---

## 6. Final Verdict

**Yes, TypeScript would help at the network layer—but not yet.**

1. ✅ **Architecturally sound**: Hexagonal supports polyglot adapters
2. ✅ **Industry precedent**: Python backend + TypeScript gateway is common
3. ✅ **MCP ecosystem**: Both SDKs are viable
4. ⚠️ **YAGNI**: We don't need it for Work Tracker MVP
5. ✅ **Prepare, don't implement**: Design ports for language-agnostic IPC

**Action**: Proceed with Python-only, but design contracts that allow TypeScript adapters to be added without refactoring the domain.

---

## 7. References

1. Model Context Protocol. "Specification 2025-11-25." https://modelcontextprotocol.io/specification/2025-11-25
2. GitHub. "modelcontextprotocol/typescript-sdk." https://github.com/modelcontextprotocol/typescript-sdk
3. Sairyss. "domain-driven-hexagon." https://github.com/Sairyss/domain-driven-hexagon
4. TSH. "Hexagonal architecture – overview and best practices." https://tsh.io/blog/hexagonal-architecture
5. htdocs.dev. "Claude Code Full-Stack Configuration Guide." https://htdocs.dev/posts/claude-code-full-stack-configuration-guide/
6. AWS. "Structure a Python project in hexagonal architecture." https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/structure-a-python-project-in-hexagonal-architecture-using-aws-lambda.html
7. MCP Blog. "One Year of MCP." https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-07 | Claude | Initial draft |
| 1.0 | 2026-01-07 | Claude | Approved - proceed with hybrid-ready Python |

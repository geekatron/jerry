# Tool Security Tier Quick-Reference Card

## Document Sections

| Section | Purpose |
|---------|---------|
| [Tier Definitions](#tier-definitions) | Tier names, capabilities, cumulative tools, example agents |
| [Current Distribution](#current-distribution) | Agent count per tier |
| [Selection Flowchart](#selection-flowchart) | Decision path from agent requirements to tier |
| [Key Exceptions](#key-exceptions) | Tier assignment exceptions and inheritance notes |
| [Cross-References](#cross-references) | Authoritative sources and related documents |

---

## Tier Definitions

| Tier | Short Name | Full Name | New Capability | Cumulative Tools | Example Agents |
|------|-----------|-----------|---------------|-----------------|----------------|
| T1 | Read-Only | Read-Only | -- | Read, Glob, Grep | pe-scorer, diataxis-classifier |
| T2 | Read-Write | Read-Write | Write, Edit, Bash | T1 + Write, Edit, Bash | ps-critic, adv-scorer |
| T3 | Persistent | Persistent | Memory-Keeper | T2 + Memory-Keeper | ts-parser, ts-extractor |
| T4 | External | Persistent + External | WebSearch, WebFetch, Context7 | T3 + WebSearch, WebFetch, Context7 | ps-researcher, eng-architect |
| T5 | Orchestration | Orchestration | Agent | T4 + Agent | ux-orchestrator |

---

## Current Distribution

| Tier | Agent Count |
|------|-------------|
| T1 | 4 |
| T2 | 28 |
| T3 | 2 |
| T4 | 54 |
| T5 | 1 |
| **Total** | **89** |

---

## Selection Flowchart

```
Agent reads only?
  YES --> T1
  NO  --> Agent writes files?
            YES --> Agent needs cross-session persistence (Memory-Keeper)?
                      YES --> Agent needs web/external research?
                                YES --> Agent delegates to other agents?
                                          YES --> T5
                                          NO  --> T4
                                NO  --> T3
                      NO  --> Agent needs web/external research?
                                YES --> T4 (inherits T3 capabilities)
                                NO  --> T2
            NO  --> Re-evaluate: agent must read or write.
```

---

## Key Exceptions

| Exception | Scope | Rule |
|-----------|-------|------|
| `eng-*` and `red-*` agents are T4 but MUST NOT use Memory-Keeper | Engagement-scoped agents | P-002 (file-based persistence only) |
| T4 inherits all T3 capabilities | All T4 agents | Memory-Keeper is available at T4 unless restricted by P-002 |
| Worker agents MUST NOT be T5 | All worker agents | H-01 / P-003 (no recursive subagents) |

---

## Cross-References

| Document | Location |
|----------|----------|
| Authoritative tier definitions | `.context/rules/agent-development-standards.md` |
| Decision rationale | `ADR-STORY015-001-tier-model-renumbering.md` |
| Migration steps | `tier-migration-guide.md` |

# ADR: Unified vs Federated Agent Template Architecture

> **ADR ID:** WI-SAO-009-ADR-001
> **Date:** 2026-01-11
> **Status:** ✅ APPROVED
> **Deciders:** User + Claude (Opus 4.5)
> **Approval Date:** 2026-01-11
> **Approval Record:** `decisions/wi-sao-009-approval-record.md`

---

## Context

WI-SAO-009 requires creating a unified agent template that serves both `ps-*` (Problem-Solving) and `nse-*` (NASA Systems Engineering) agents. The Jerry framework currently has:

- **10 `nse-*` agents** in `skills/nasa-se/agents/`
- **9 `ps-*` agents** in `skills/problem-solving/agents/`
- **2 templates:** PS_AGENT_TEMPLATE.md v2.0, NSE_AGENT_TEMPLATE.md v1.0

**Key Question:** Should we create a single unified template or a federated architecture with shared core + domain extensions?

---

## Decision

**RECOMMENDED: FEDERATED TEMPLATE ARCHITECTURE**

Use a shared core template (~73% of content) with domain-specific extensions composed at build time.

---

## Evidence Summary

### E1: Template Structural Analysis (ps-analyst)

**Source:** `analysis/wi-sao-009-e-001-template-comparison.md`

| Metric | Value |
|--------|-------|
| Structural overlap | **73%** |
| Identical YAML fields | 13 |
| Similar YAML fields | 11 |
| PS-only fields | 2 (`prior_art`, `link_artifact_required`) |
| NSE-only fields | 3 (`nasa_processes`, `nasa_standards`, `disclaimer_required`) |
| NSE-only XML sections | 2 (`<disclaimer>`, `<nasa_se_methodology>`) |

**Verdict Matrix:**
| Criterion | Unified | Federated | Winner |
|-----------|---------|-----------|--------|
| Maintenance simplicity | Single file | Multiple files | Unified |
| Domain accuracy | Irrelevant sections | Clean separation | **Federated** |
| Extension mechanism | Conditional | Inheritance | **Federated** |
| Consistency enforcement | Easy | Requires sync | Unified |
| Domain expert ownership | Mixed | Clear ownership | **Federated** |
| Future domains | Bloat | Clean additions | **Federated** |

**Score:** Unified 2, Federated 4 → **Federated wins**

### E2: Official Anthropic Agent Format (Context7)

**Sources:** `/anthropics/claude-code`, `/websites/platform_claude_en_agent-sdk`

**Official YAML frontmatter:**
```yaml
---
name: agent-name
description: Brief description with PROACTIVELY keyword for auto-invocation
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
---
[System prompt body]
```

**Key insight:** Anthropic's format is minimal (4 fields). Jerry's PS/NSE templates are significantly extended. A federated approach allows:
- **Core:** Stays closer to Anthropic standard
- **Extensions:** Add Jerry-specific guardrails per domain

### E3: Boris Cherny & Anthropic Engineering Patterns (ps-researcher)

**Source:** `research/wi-sao-009-e-001-claude-engineer-patterns.md`

**Key findings:**
1. **Progressive Disclosure Architecture:** Load context on-demand, not all upfront
   - L1: Metadata (name/description) in system prompt
   - L2: Full template body loaded when activated
   - L3+: Supporting files loaded during execution

2. **CLAUDE.md as "Do Not Repeat" Ledger:** Short, reactive, not exhaustive
   - Aligns with federated approach: domain rules in extensions, not bloated core

3. **Tool Whitelist by Role:** Security-first, explicit permissions
   - Supports domain-specific tool configurations in extensions

4. **Context Engineering:** "Find smallest set of high-signal tokens"
   - Federated approach loads only relevant domain content

### E4: Industry Multi-Agent Patterns

**Source:** `research/agent-research-007-industry-patterns-recovered.md`

| Framework | Relevant Pattern |
|-----------|------------------|
| **LangGraph** | Graph-based state with modular nodes |
| **CrewAI** | Specialized crews with clear boundaries |
| **AutoGen** | Layered architecture (Core → AgentChat) |
| **Azure Magentic** | Task ledger with dynamic refinement |

**Industry consensus:** Favor composition over monolithic structures.

---

## Non-Negotiable Constraints

These MUST be preserved regardless of approach:

| Constraint | Rationale |
|------------|-----------|
| **P-003 compliance** | Hard principle - no recursive agent spawning |
| **Backward compatibility** | 19 existing agents must continue working |
| **session_context schema** | Agent handoff protocol - identical in both templates |
| **Claude Code Task tool** | Agent spawning mechanism |
| **L0/L1/L2 output levels** | Stakeholder communication standard |

---

## Proposed Architecture

```
skills/
├── shared/
│   └── AGENT_TEMPLATE_CORE.md          # 73% shared content (v1.0)
├── problem-solving/
│   ├── agents/
│   │   ├── PS_EXTENSION.md             # PS-specific additions
│   │   └── ps-*.md                     # Individual agents
│   └── SKILL.md
└── nasa-se/
    ├── agents/
    │   ├── NSE_EXTENSION.md            # NSE-specific additions
    │   └── nse-*.md                    # Individual agents
    └── SKILL.md
```

### Core Template Contents (AGENT_TEMPLATE_CORE.md)

**YAML Frontmatter (shared):**
- `name`, `version`, `description`, `model`
- `identity` (role, expertise, cognitive_mode)
- `persona` (tone, communication_style, audience_level)
- `capabilities` (base tools, formats, forbidden_actions base)
- `guardrails` (validation structure, filtering base)
- `output` (required flag, location template, L0/L1/L2)
- `validation` (file_must_exist, base checks)
- `constitution` (reference, base principles P-002/003/004/022)
- `enforcement` (tier, escalation_path)
- `session_context` (full schema - identical across domains)

**XML Body (shared tags):**
- `<agent>`, `<identity>`, `<persona>`, `<capabilities>`
- `<guardrails>`, `<constitutional_compliance>`
- `<invocation_protocol>`, `<output_levels>`, `<state_management>`

**Extension Points:**
```markdown
{%DOMAIN_IDENTITY%}         <!-- nasa_processes, etc. -->
{%DOMAIN_FORBIDDEN_ACTIONS%}
{%DOMAIN_OUTPUT_FILTERING%}
{%DOMAIN_VALIDATION%}
{%DOMAIN_REFERENCES%}       <!-- prior_art OR nasa_standards -->
{%DOMAIN_PRINCIPLES%}       <!-- P-040/41/42 for NSE -->
{%DOMAIN_SECTIONS%}         <!-- <disclaimer>, <nasa_se_methodology> -->
```

### PS Extension Contents

- `prior_art` YAML section
- `link_artifact_required` validation
- Output directory conventions table
- Artifact naming patterns (ps-* agents)
- Industry references (Anthropic, Google ADK, KnowBe4)

### NSE Extension Contents

- `nasa_processes` in identity
- `nasa_standards` YAML section
- `disclaimer_required` validation
- `<disclaimer>` XML section (mandatory)
- `<nasa_se_methodology>` XML section
- Extended principles (P-040, P-041, P-042)
- NASA references table (NPR 7123.1D, etc.)

---

## Alternatives Considered

### Alternative A: Single Unified Template

**Description:** Merge all content into one template with conditional markers.

**Pros:**
- Single source of truth
- No sync complexity

**Cons:**
- 420+ lines of mixed domain content
- Developers see irrelevant sections
- Violates Single Responsibility Principle
- YAML/Markdown lacks native conditionals

**Verdict:** REJECTED - Evidence score 2/6

### Alternative B: Copy-Paste Separate Templates (Current State)

**Description:** Maintain independent PS and NSE templates.

**Pros:**
- Maximum domain flexibility
- No shared dependencies

**Cons:**
- 73% duplicate content
- Updates must be manually synced
- Risk of drift between domains
- Violates DRY principle

**Verdict:** REJECTED - Current technical debt

### Alternative C: Federated with Composition (Recommended)

**Description:** Shared core + domain extensions, composed at authoring time.

**Pros:**
- 73% shared, maintained once
- Domain-specific content isolated
- Clear ownership boundaries
- Supports future domains (e.g., `aerospace-*`)
- Aligns with industry patterns (LangGraph, CrewAI, Azure)

**Cons:**
- Composition step required
- Version synchronization needed
- Higher initial setup effort

**Verdict:** RECOMMENDED - Evidence score 4/6

---

## Migration Effort Estimate

| Task | Effort | Risk |
|------|--------|------|
| Extract core template | 2 hours | Low |
| Create PS extension | 1 hour | Low |
| Create NSE extension | 1.5 hours | Low |
| Create composition script | 2 hours | Medium |
| Update existing 19 agents | 4 hours | Medium |
| Testing and validation | 3 hours | Low |
| **Total** | **13.5 hours** | **Medium** |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Extension drift from core | Medium | Medium | Automated composition validation |
| Version sync issues | Low | High | Semantic versioning + changelog |
| Developer confusion | Low | Medium | Clear documentation + examples |
| Breaking existing agents | Medium | High | Comprehensive test suite |

---

## Decision Criteria Met

| Criterion | Status |
|-----------|--------|
| Evidence-based | ✅ 4 research sources |
| Claude Code specific | ✅ Official format aligned |
| P-003 compliant | ✅ No recursive spawning |
| Backward compatible | ✅ Existing agents unaffected |
| session_context preserved | ✅ Identical schema |
| Industry best practices | ✅ Composition pattern |

---

## Approval

**Decision:** ✅ **APPROVED** - Proceed with federated implementation

**Approval Details:**
| Field | Value |
|-------|-------|
| Decision | APPROVED |
| Approver | User (Human-in-the-Loop) |
| Approval Date | 2026-01-11 |
| Approval Time | Session timestamp |
| Session ID | `363ac053-6bfd-465e-8843-4f528ab5ecd1` |
| Model | Claude Opus 4.5 (`claude-opus-4-5-20251101`) |
| Git Branch | `cc/proj-nasa-subagent` |
| Working Directory | `nasa-subagent` |

**Cross-References:**
- Approval Record: `decisions/wi-sao-009-approval-record.md`
- Implementation Plan: `WORKTRACKER.md` → WI-SAO-009

---

## References

### Research Artifacts Created
1. `analysis/wi-sao-009-e-001-template-comparison.md` - Quantitative comparison (334 lines)
2. `research/wi-sao-009-e-001-claude-engineer-patterns.md` - Anthropic patterns (400+ lines)

### Prior Art Consulted
3. `PS_AGENT_TEMPLATE.md` v2.0 - 418 lines
4. `NSE_AGENT_TEMPLATE.md` v1.0 - 420 lines
5. `agent-research-001-claude-code-mechanics.md` - Task tool mechanics
6. `agent-research-006-anthropic-claude.md` - Constitutional AI
7. `agent-research-007-industry-patterns-recovered.md` - Multi-agent patterns

### External Sources
8. [Anthropic Skills GitHub](https://github.com/anthropics/skills) - Official template format
9. [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - System prompt best practices
10. [Building Agents with Claude SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) - SDK architecture
11. [Boris Cherny Workflow (VentureBeat)](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are) - Multi-session patterns

---

DISCLAIMER: This guidance is AI-generated based on evidence analysis. All architectural decisions require human review and engineering judgment.

---

*ADR Version: 1.0.0*
*Created: 2026-01-11*
*Analysts: ps-researcher, ps-analyst*

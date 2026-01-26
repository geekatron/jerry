# Requirements Addendum 001: Claude Code Skill Architecture

> **Addendum ID**: PROJ-008-e-003-ADDENDUM-001
> **Version**: 1.0
> **Date**: 2026-01-25
> **Author**: Claude Opus 4.5
> **Status**: APPROVED
> **Traceability**: EN-003-RESEARCH-001 → REQUIREMENTS-SPECIFICATION.md

---

## Document Audience (Triple-Lens)

| Level | Audience | Focus Areas |
|-------|----------|-------------|
| **L0 (ELI5)** | Stakeholders | Summary of Changes, Priority Shifts |
| **L1 (Engineer)** | Developers | New Requirements, Technical Patterns |
| **L2 (Architect)** | System Designers | Strategic Implications, Trade-offs |

---

## L0: Summary of Changes

### Why This Addendum?

Deep research on Claude Code skill architecture revealed **critical best practices** from Anthropic and industry leaders that must be incorporated into our requirements. This addendum adds **12 new requirements** and **modifies 3 existing requirements**.

### Key Changes

```
ADDENDUM SUMMARY
================

┌─────────────────────────────────────────────────────────────────────────┐
│                        CHANGES OVERVIEW                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   NEW REQUIREMENTS ADDED:                                                │
│   ├── SK-001..SK-008: Skill Architecture Requirements      8            │
│   ├── MA-001..MA-004: Model-Agnostic Design Requirements   4            │
│   └── TOTAL NEW:                                          12            │
│                                                                          │
│   EXISTING REQUIREMENTS MODIFIED:                                        │
│   ├── IR-004: SKILL.md Interface (Enhanced)                              │
│   ├── IR-005: Hexagonal Architecture (Clarified)                         │
│   └── Phase priorities (Rebalanced)                                      │
│                                                                          │
│   PRIORITY SHIFT:                                                        │
│   ├── Accuracy > Performance                                             │
│   ├── Quality > Speed                                                    │
│   ├── Behavior First > CLI                                               │
│   └── CLI is literally LAST (Phase 5 - "Above and Beyond")               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Priority Rebalancing

| Original Priority | New Priority | Rationale |
|-------------------|--------------|-----------|
| Performance (<10s) | Quality First | Mission-critical software; accuracy over speed |
| CLI Interface | Behavior/Prompts | Behavior first, CLI is literally "above and beyond" - LAST |
| Jerry Integration | Model-Agnostic | Must work with Ollama, other LLMs |

---

## L1: New Requirements Catalog

### 1. Skill Architecture Requirements (SK-001 to SK-008)

#### SK-001: SKILL.md Structure Compliance

| Attribute | Value |
|-----------|-------|
| **ID** | SK-001 |
| **Statement** | The SKILL.md file SHALL conform to Anthropic Agent Skills standard with YAML frontmatter containing name (max 64 chars, lowercase/numbers/hyphens), description (max 1024 chars), and optional fields (version, allowed-tools, disable-model-invocation) |
| **Rationale** | Anthropic best practices require specific frontmatter structure for skill discovery and invocation |
| **Parent** | IR-004 |
| **V-Method** | Inspection |
| **Priority** | Must |
| **Source** | [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

#### SK-002: Description Third-Person Format

| Attribute | Value |
|-----------|-------|
| **ID** | SK-002 |
| **Statement** | All skill and agent descriptions SHALL be written in third-person format (e.g., "Analyzes transcripts" NOT "I can analyze transcripts") |
| **Rationale** | Anthropic explicitly requires third-person format as descriptions are injected into system prompt |
| **Parent** | SK-001 |
| **V-Method** | Inspection |
| **Priority** | Must |
| **Source** | [Anthropic Best Practices - Writing Effective Descriptions](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

#### SK-003: Description Trigger Phrases

| Attribute | Value |
|-----------|-------|
| **ID** | SK-003 |
| **Statement** | Skill descriptions SHALL include specific trigger phrases that users would say (e.g., "Use when the user asks to 'analyze transcript', 'extract action items', 'summarize meeting'") |
| **Rationale** | Claude uses description for skill selection from 100+ skills; specific phrases improve discovery |
| **Parent** | SK-001 |
| **V-Method** | Inspection |
| **Priority** | Must |
| **Source** | [Context7 - Claude Code Skill Development](https://github.com/anthropics/claude-code) |

#### SK-004: Progressive Disclosure

| Attribute | Value |
|-----------|-------|
| **ID** | SK-004 |
| **Statement** | The SKILL.md body SHALL be kept under 500 lines; detailed reference material SHALL be split into separate files with one-level-deep references from SKILL.md |
| **Rationale** | "Keep SKILL.md under 500 lines for optimal performance" - Anthropic best practice |
| **Parent** | IR-004 |
| **V-Method** | Inspection |
| **Priority** | Must |
| **Source** | [Anthropic Best Practices - Progressive Disclosure](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

#### SK-005: Agent L0/L1/L2 Output Structure

| Attribute | Value |
|-----------|-------|
| **ID** | SK-005 |
| **Statement** | All agent outputs SHALL include three levels of explanation: L0 (ELI5 for stakeholders), L1 (Technical for engineers), L2 (Strategic for architects) |
| **Rationale** | Jerry framework pattern; ensures outputs serve multiple audiences |
| **Parent** | STK-001 |
| **V-Method** | Demonstration |
| **Priority** | Must |
| **Source** | Jerry Framework skills/nasa-se/SKILL.md, skills/problem-solving/SKILL.md |

#### SK-006: Agent Invocation Response Pattern

| Attribute | Value |
|-----------|-------|
| **ID** | SK-006 |
| **Statement** | Agent invocations SHALL follow the standard response pattern: "I'll use the [agent-name] agent to [what it will do]." |
| **Rationale** | Consistent invocation pattern improves user understanding and debugging |
| **Parent** | SK-001 |
| **V-Method** | Demonstration |
| **Priority** | Should |
| **Source** | [Context7 - Agent Triggering Examples](https://github.com/anthropics/claude-code) |

#### SK-007: Constitutional Compliance

| Attribute | Value |
|-----------|-------|
| **ID** | SK-007 |
| **Statement** | All agents and skills SHALL comply with Jerry Constitution v1.0, specifically P-001 (Truth), P-002 (File Persistence), P-003 (No Recursive Subagents), P-004 (Explicit Provenance) |
| **Rationale** | Jerry framework governance requirement |
| **Parent** | IR-005 |
| **V-Method** | Inspection |
| **Priority** | Must |
| **Source** | docs/governance/JERRY_CONSTITUTION.md |

#### SK-008: Evaluation-First Development

| Attribute | Value |
|-----------|-------|
| **ID** | SK-008 |
| **Statement** | Skills SHALL have evaluations (test scenarios) created BEFORE documentation is written; evaluations SHALL include at least 3 scenarios testing discovery, invocation, and output quality |
| **Rationale** | "Build evaluations BEFORE writing extensive documentation" - Anthropic best practice |
| **Parent** | SK-001 |
| **V-Method** | Test |
| **Priority** | Must |
| **Source** | [Anthropic Best Practices - Evaluation and Iteration](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

---

### 2. Model-Agnostic Design Requirements (MA-001 to MA-004)

#### MA-001: Provider-Independent Prompt Design

| Attribute | Value |
|-----------|-------|
| **ID** | MA-001 |
| **Statement** | Skill prompts and agent definitions SHALL be designed to work with multiple LLM providers (Claude, Ollama, OpenAI) without modification to core instructions |
| **Rationale** | User requirement: "to be able to be used by other LLMs/Models outside of Claude Code" |
| **Parent** | STK-009 |
| **V-Method** | Test |
| **Priority** | Must |
| **Source** | User requirement; [Agent Skills Open Standard](https://agentskills.io) |

#### MA-002: Avoid Provider-Specific Features

| Attribute | Value |
|-----------|-------|
| **ID** | MA-002 |
| **Statement** | Core skill instructions SHALL avoid provider-specific syntax or features; provider-specific optimizations SHALL be isolated in adapter files |
| **Rationale** | Enable portability across LLM providers |
| **Parent** | MA-001 |
| **V-Method** | Inspection |
| **Priority** | Must |
| **Source** | [Promptware Engineering Research](https://arxiv.org/html/2503.02400v1) |

#### MA-003: Multi-Model Testing

| Attribute | Value |
|-----------|-------|
| **ID** | MA-003 |
| **Statement** | Skills SHALL be tested with at least Haiku (fast), Sonnet (balanced), and Opus (powerful) models to verify behavior across capability levels |
| **Rationale** | "Test your Skill with all the models you plan to use it with" - Anthropic |
| **Parent** | SK-008 |
| **V-Method** | Test |
| **Priority** | Must |
| **Source** | [Anthropic Best Practices - Testing](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

#### MA-004: Freedom Spectrum Documentation

| Attribute | Value |
|-----------|-------|
| **ID** | MA-004 |
| **Statement** | Each skill section SHALL document its degree of freedom: HIGH (text-based, context-dependent), MEDIUM (parameterized scripts), or LOW (exact scripts for fragile operations) |
| **Rationale** | "Match the level of specificity to the task's fragility and variability" - Anthropic |
| **Parent** | SK-004 |
| **V-Method** | Inspection |
| **Priority** | Should |
| **Source** | [Anthropic Best Practices - Degrees of Freedom](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

---

### 3. Modified Existing Requirements

#### IR-004 (Modified): SKILL.md Interface - Enhanced

**Original:**
> The system SHALL provide a SKILL.md interface compatible with Jerry framework

**Enhanced:**
> The system SHALL provide a SKILL.md interface compatible with:
> 1. Anthropic Agent Skills standard (agentskills.io)
> 2. Jerry framework skill patterns
> 3. Claude Code slash command invocation
>
> The SKILL.md SHALL include:
> - YAML frontmatter (name, description, version, allowed-tools)
> - L0/L1/L2 audience sections
> - Available agents table with output locations
> - Tool invocation examples
> - Quick reference section
> - Constitutional compliance statement

#### Phase Priority Rebalancing

```
PHASE PRIORITY SHIFT
====================

ORIGINAL PRIORITIES:
├── Phase 1: Foundation (Parsing + CLI)      [HIGH]
├── Phase 2: Core Extraction                 [HIGH]
├── Phase 3: Integration (SKILL.md + JSON)   [MEDIUM]
└── Phase 4: Validation                      [HIGH]

NEW PRIORITIES:
├── Phase 1: Skill Architecture & Prompts    [CRITICAL] ← NEW
│   └── SKILL.md, Agent definitions, Evaluations
│
├── Phase 2: Output Formats & Templates      [HIGH] ← ELEVATED
│   └── Markdown, JSON outputs, L0/L1/L2 structure
│
├── Phase 3: Core Extraction Logic           [HIGH]
│   └── Parsing, Entity extraction, Confidence scoring
│
├── Phase 4: Validation & Multi-Model Testing [HIGH]
│   └── Quality assurance, Haiku/Sonnet/Opus testing, Benchmarks
│
└── Phase 5: CLI (Above and Beyond)          [MEDIUM] ← LAST
    └── CLI interface, Pipeline integration - literally last priority
```

---

## L2: Strategic Implications

### 1. Architectural Alignment

```
SKILL ARCHITECTURE ALIGNMENT
============================

┌─────────────────────────────────────────────────────────────────────────┐
│                    TRANSCRIPT SKILL STRUCTURE                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  transcript/                                                             │
│  ├── SKILL.md                    # Main skill (< 500 lines)             │
│  │   ├── YAML Frontmatter        # name, description, version           │
│  │   ├── L0/L1/L2 Sections       # Multi-audience structure             │
│  │   ├── Agent Table             # ts-analyzer, ts-extractor, etc.      │
│  │   ├── Quick Reference         # Common workflows                     │
│  │   └── References              # Links to reference files             │
│  │                                                                       │
│  ├── agents/                     # Agent definitions                    │
│  │   ├── ts-analyzer.md          # Transcript structure analysis        │
│  │   ├── ts-extractor.md         # Entity extraction agent              │
│  │   └── ts-summarizer.md        # Summary generation agent             │
│  │                                                                       │
│  ├── templates/                  # Output templates                     │
│  │   ├── summary-template.md     # Summary output format                │
│  │   └── extraction-template.md  # Extraction output format             │
│  │                                                                       │
│  ├── reference/                  # Reference documentation              │
│  │   ├── transcript-formats.md   # VTT, SRT, plain text specs           │
│  │   ├── entity-taxonomy.md      # Entity types and patterns            │
│  │   └── nlp-patterns.md         # NLP extraction patterns              │
│  │                                                                       │
│  └── scripts/                    # Utility scripts (executed, not read) │
│      ├── parse_transcript.py     # Transcript parsing utility           │
│      └── validate_output.py      # Output validation script             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Model-Agnostic Design Strategy

```
MODEL-AGNOSTIC ARCHITECTURE
===========================

┌─────────────────────────────────────────────────────────────────────────┐
│                    PORTABILITY LAYERS                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                 CORE SKILL INSTRUCTIONS                          │   │
│  │                 (Provider-Agnostic)                              │   │
│  │                                                                   │   │
│  │  • Standard markdown format                                      │   │
│  │  • No provider-specific syntax                                   │   │
│  │  • Clear, explicit instructions                                  │   │
│  │  • Tested with Haiku, Sonnet, Opus                              │   │
│  │                                                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                 PROVIDER ADAPTERS                                │   │
│  │                 (Optional Optimizations)                         │   │
│  │                                                                   │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │   │
│  │  │ Claude  │  │ Ollama  │  │ OpenAI  │  │ Custom  │           │   │
│  │  │ Adapter │  │ Adapter │  │ Adapter │  │ Adapter │           │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │   │
│  │                                                                   │   │
│  │  • XML tags (Claude)   • System prompts  • Function calling     │   │
│  │  • Extended thinking   • Context limits  • Response format      │   │
│  │                                                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Quality Gates from Research

| Gate | Criteria | Source |
|------|----------|--------|
| **Structure Gate** | SKILL.md < 500 lines, YAML frontmatter valid | Anthropic |
| **Description Gate** | Third-person, < 1024 chars, trigger phrases present | Anthropic |
| **Reference Gate** | All references one-level deep from SKILL.md | Anthropic |
| **Evaluation Gate** | 3+ test scenarios before documentation | Anthropic |
| **Multi-Model Gate** | Tested with Haiku, Sonnet, Opus | Anthropic |
| **Constitutional Gate** | P-001, P-002, P-003, P-004 compliance | Jerry |

### 4. Trade-off Analysis

| Decision | Option A | Option B | Selected | Rationale |
|----------|----------|----------|----------|-----------|
| **Documentation Size** | Comprehensive in SKILL.md | Progressive disclosure | **B** | Anthropic best practice; context efficiency |
| **Model Support** | Claude-optimized | Model-agnostic | **B** | User requirement for Ollama support |
| **Testing Approach** | Post-development | Evaluation-first | **B** | Anthropic best practice; quality assurance |
| **CLI Priority** | Phase 1 | Phase 4 | **Phase 4** | Behavior first, CLI is enhancement |

---

## References

### Primary Sources

1. [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
2. [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
3. [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
4. [Agent Skills Open Standard](https://agentskills.io)

### Research Documents

1. EN-003-RESEARCH-001: CLAUDE-CODE-SKILL-ARCHITECTURE-RESEARCH.md

### Jerry Framework Sources

1. skills/nasa-se/SKILL.md
2. skills/problem-solving/SKILL.md
3. skills/orchestration/SKILL.md
4. docs/governance/JERRY_CONSTITUTION.md

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Author | Claude Opus 4.5 | 2026-01-25 | Complete |
| Reviewer | User | Pending | Pending |

---

*End of Requirements Addendum 001*

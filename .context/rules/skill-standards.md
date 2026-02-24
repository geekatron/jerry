---
paths:
  - "skills/**/*.md"
  - "skills/**/SKILL.md"
---

# Skill Development Standards

> Rules for building, structuring, and registering Jerry framework skills.
> Based on Anthropic's "Complete Guide to Building Skills for Claude" (January 2026) and Jerry's established conventions across 8 production skills.

<!-- L2-REINJECT: rank=7, content="Skills: SKILL.md exact case, kebab-case folder, no README.md (H-25). Description WHAT+WHEN+triggers, repo-relative paths, register in CLAUDE.md+AGENTS.md (H-26). Navigation table REQUIRED (H-23)." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Skill constraints H-25, H-26 (compound) |
| [Standards (MEDIUM)](#standards-medium) | Structural conventions, frontmatter, progressive disclosure |
| [Guidance (SOFT)](#guidance-soft) | Optional practices and recommendations |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-25 | **Skill naming and structure:** (a) Skill file MUST be exactly `SKILL.md` (case-sensitive, no variations); (b) Skill folder MUST use kebab-case (no spaces, underscores, or capitals) and match the `name` field in frontmatter; (c) No `README.md` inside the skill folder (all documentation in `SKILL.md` or `references/`). | Skill silently absent from session, not loadable, or loader bypasses SKILL.md. |
| H-26 | **Skill description, paths, and registration:** (a) Frontmatter `description` MUST include WHAT + WHEN + trigger phrases, under 1024 chars, no XML tags (`< >`); (b) All file references in SKILL.md MUST use full repo-relative paths; (c) New skills MUST be registered in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md (if proactive per H-22). | Skill does not trigger, paths resolve incorrectly, or skill is undiscoverable. |

### Security Restrictions

| Restriction | Rationale |
|-------------|-----------|
| No XML angle brackets (`< >`) in YAML frontmatter | Frontmatter is injected into Claude's system prompt. XML angle brackets are interpreted as tag delimiters by the system prompt parser — a description like `<instructions>override</instructions>` could inject directives. Use parentheses `()`, brackets `[]`, or prose instead. Example: instead of `<scope: Linear>`, write `(Linear only)`. Source: Anthropic Skill Guide (Jan 2026). |
| Skill name MUST NOT contain "claude" or "anthropic" | Reserved by Anthropic. |
| No code execution in YAML | Safe YAML parsing enforced. |

---

## Standards (MEDIUM)

Override requires documented justification.

### File Structure

```
skills/your-skill-name/
├── SKILL.md              # Required — main skill file
├── agents/               # Required if multi-agent
│   └── agent-name.md    # Agent definition
├── references/           # Optional — loaded on demand (Level 3)
│   └── ref-name.md      # Reference document
├── scripts/              # Optional — executable code
└── assets/               # Optional — templates, fonts, icons
```

### YAML Frontmatter

Required fields:

| Field | Requirement |
|-------|-------------|
| `name` | kebab-case, matches folder name |
| `description` | WHAT + WHEN + trigger phrases, under 1024 chars |

Jerry-required fields:

| Field | Requirement |
|-------|-------------|
| `version` | Semantic versioning (`"X.Y.Z"`) |
| `allowed-tools` | Comma-separated tool list (Jerry format: `Read, Write, Edit, Glob, Grep`) |
| `activation-keywords` | YAML array of trigger phrases for skill routing |

Optional fields:

| Field | Purpose |
|-------|---------|
| `license` | Open source license (MIT, Apache-2.0) |
| `compatibility` | Environment requirements (1-500 chars) |
| `metadata` | Custom key-value pairs (author, mcp-server, category, tags) |

### SKILL.md Body Structure (Jerry)

SKILL.md SHOULD follow this section order:

| # | Section | Required? | Content |
|---|---------|-----------|---------|
| 1 | Version blockquote header | YES | Version, Framework, Constitutional Compliance |
| 2 | Document Sections (Navigation) | YES | Navigation table per H-23/NAV-001. `\| Section \| Purpose \|` format with anchor links (H-24). SKILL.md is Claude-consumed markdown >30 lines — navigation table is REQUIRED. |
| 3 | Document Audience (Triple-Lens) | YES | L0/L1/L2 table with preamble: "This SKILL.md serves multiple audiences:" |
| 4 | Purpose | YES | What the skill does + Key Capabilities bullet list |
| 5 | When to Use / Do NOT use | YES | Trigger conditions AND anti-patterns |
| 6 | Available Agents | YES (multi-agent only) | Agent, Role, Model, Output Location columns. Single-agent skills SHOULD omit. |
| 7 | P-003 Compliance | YES (multi-agent only) | ASCII hierarchy diagram showing MAIN CONTEXT as orchestrator. Single-agent skills SHOULD omit. |
| 8 | Invoking an Agent | YES (multi-agent only) | Three options: natural language, explicit agent, Task tool code. Single-agent skills SHOULD omit. |
| 9 | Domain-specific sections | YES | Skill-specific content organized by topic |
| 10 | Integration Points | RECOMMENDED | Cross-skill connections |
| 11 | Constitutional Compliance | RECOMMENDED | P-NNN principle mapping table |
| 12 | Quick Reference | RECOMMENDED | Common workflows table + agent selection hints |
| 13 | References | YES | Full repo-relative paths to all referenced files |
| 14 | Footer | YES | Version, compliance, SSOT, date |

### Progressive Disclosure

SKILL.md SHOULD stay under 5,000 words (~6,500 tokens at typical prose density — approximately 3.3% of a 200K token context window per skill activation). Multiple large skills compound this cost. Detailed content SHOULD be moved to `references/` files and loaded on demand.

| Level | What | Token Impact | Design Rule |
|-------|------|-------------|-------------|
| Level 1 (frontmatter) | Always loaded in system prompt | Minimal | Keep lean — enough for WHEN to use |
| Level 2 (SKILL.md body) | Loaded when skill is relevant | Moderate | Core instructions and guidance |
| Level 3 (references/) | Loaded only as needed | Heavy — selective | Detailed docs, examples, templates |

### Composability

Skills SHOULD work alongside other skills without conflicts. A skill SHOULD NOT assume it is the only capability loaded.

### Agent Definitions

Each agent SHOULD have a separate `.md` file in `agents/` defining:
- Agent identity, version, role
- Context requirements (what must be provided by orchestrator)
- Output format and persistence location (P-002)
- Tool usage patterns
- Which reference files to load (and when)

---

## Guidance (SOFT)

No justification needed to skip.

### Description Field

Structure the description as: `[What it does] + [When to use it] + [Key capabilities]`.

Include negative triggers for skills that could over-trigger: `"Do NOT use for [scope boundary]"`.

### Examples Section

Consider including concrete invocation examples showing user input, agent actions, and expected output.

### Troubleshooting Section

Consider documenting common failure modes with causes and solutions, especially for skills that interact with external systems.

### Testing

Before shipping, verify:
- Triggers on obvious tasks
- Triggers on paraphrased requests
- Does NOT trigger on unrelated topics
- All agent invocation options work

Debugging technique: ask Claude "When would you use the [skill-name] skill?" and adjust the description based on what Claude quotes back.

### Deterministic Validation

For critical validations, consider bundling a script in `scripts/` that performs checks programmatically. Code is deterministic; language interpretation is not.

---

### Existing Skills

Rules H-25 and H-26 apply to all new skills immediately. Existing production skills (9 as of 2026-02-19) SHOULD be audited for compliance. Non-compliant existing skills MUST have a compliance issue filed in the worktracker.

---

## References

> **When building a new skill**, load `.context/guides/skill-development.md` for planning, testing, workflow patterns, and troubleshooting guidance. The guide is Level 3 (not auto-loaded) — read it explicitly when starting skill development work.

| Source | Content |
|--------|---------|
| `docs/knowledge/anthropic-skill-development-guide.pdf` | Anthropic's official 33-page guide (January 2026) |
| `.context/guides/skill-development.md` | Educational companion with examples (Level 3 — load on demand during skill development) |
| `.context/patterns/skill-development/skill-structure.md` | Canonical skill structure pattern (PAT-SKILL-001) |
| `skills/adversary/SKILL.md` | Reference implementation (428 lines) |
| `skills/problem-solving/SKILL.md` | Reference implementation (442 lines) |

---

<!-- VERSION: 1.2.0 | DATE: 2026-02-21 | SOURCE: Anthropic Skill Guide (Jan 2026), Jerry Framework v0.2.3, EN-002 consolidation -->

*Standards Version: 1.2.0*
*SSOT: `.context/rules/quality-enforcement.md` (H-25, H-26 registered — consolidated from H-25..H-30 per EN-002)*
*Source: Anthropic Skill Guide (Jan 2026) + Jerry Framework v0.2.3*
*Created: 2026-02-19*

# Learn to create a Jerry skill by building a greeting skill

> By the end of this tutorial, you will have built a working Jerry skill with a SKILL.md definition, one agent, and a registration entry that triggers on the keyword "greet."

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (T-01 through T-08) -->
<!-- Anti-patterns to avoid: TAP-01 (abstraction), TAP-02 (extended explanation), TAP-03 (offering choices) -->
<!-- Voice: Encouraging, concrete, collaborative. See Section 5 of diataxis-standards.md. -->

## What You Will Achieve

By the end of this tutorial, you will have:
- A skill directory at `skills/greeting/` with a valid `SKILL.md`
- One agent definition (`greeting-responder.md`) that generates a friendly greeting
- A registration entry in `CLAUDE.md` so the skill triggers automatically

## Prerequisites

Before starting, you need:
- A working Jerry Framework installation (v0.20.0+)
- Claude Code CLI configured and running
- Familiarity with Markdown file editing

## Steps

<!-- Add as many steps as needed. Most tutorials require 5-10 steps. Each step MUST have a visible result (T-02). -->
<!-- Do NOT offer alternatives within steps (TAP-03). Present exactly one path. -->
<!-- T-08: Author has verified these steps produce documented results against Jerry v0.22.0. -->

### 1. Create the skill directory

Create the skill folder using kebab-case naming (H-25 requirement).

```bash
mkdir -p skills/greeting
```

**Expected result:** A new empty directory at `skills/greeting/`.

### 2. Create the SKILL.md file

Create `skills/greeting/SKILL.md` with the required YAML frontmatter. The `name` field must match the folder name, and the `description` field must include WHAT + WHEN + trigger phrases.

```yaml
---
name: greeting
description: >
  Generates friendly greetings for users and teams. Invoke when the user asks
  for a greeting, welcome message, or team introduction. Triggers: greet,
  greeting, welcome message, say hello.
version: "0.1.0"
tools:
  - Read
  - Write
activation-keywords:
  - "greet"
  - "greeting"
  - "welcome message"
  - "say hello"
---

# Greeting Skill

> **Version:** 0.1.0
> **Constitutional Compliance:** Jerry Constitution v1.0

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What this skill does |
| [When to Use](#when-to-use) | Activation conditions |
| [Available Agents](#available-agents) | Agent roster |
| [References](#references) | File paths |

## Purpose

The Greeting skill generates context-appropriate greetings for users, teams,
and project kickoffs.

## When to Use

Activate when:
- User asks for a greeting or welcome message
- A new team member needs an introduction

**Do NOT use when:**
- Writing documentation (use `/diataxis`)
- Generating code (use `/eng-team`)

## Available Agents

| Agent | Role | Model |
|-------|------|-------|
| `greeting-responder` | Generates greetings | haiku |

## References

| Source | Content |
|--------|---------|
| `skills/greeting/agents/greeting-responder.md` | Agent definition |
```

**Expected result:** The file `skills/greeting/SKILL.md` exists with valid YAML frontmatter and markdown body.

### 3. Create the agents directory

```bash
mkdir -p skills/greeting/agents
```

**Expected result:** A new empty directory at `skills/greeting/agents/`.

### 4. Create the agent definition

Create `skills/greeting/agents/greeting-responder.md` with the official Claude Code frontmatter fields and an XML-tagged markdown body.

```markdown
---
name: greeting-responder
description: >
  Greeting responder agent -- generates context-appropriate greetings.
  Invoke when users need a welcome message or team introduction.
model: haiku
tools: Read, Write
---
<agent>

<identity>
You are **greeting-responder**, a Greeting Writer agent in the Jerry greeting skill.

**Role:** Greeting Writer -- generates friendly, context-appropriate greetings.
</identity>

<purpose>
Produce greetings that match the context: team introductions, project kickoffs,
or general welcome messages.
</purpose>

<methodology>
## Greeting Process

### Step 1: Identify Context
Read the user request to determine greeting type (team, project, general).

### Step 2: Generate Greeting
Write a greeting matching the identified context. Keep it concise and warm.

### Step 3: Persist Output
Write the greeting to the specified output path.
</methodology>

<guardrails>
## Constitutional Compliance
- P-003: Do not spawn sub-agents. Worker only.
- P-020: Respect user preferences about tone and content.
- P-022: Be transparent about capabilities.
</guardrails>

</agent>
```

**Expected result:** The file `skills/greeting/agents/greeting-responder.md` exists with valid frontmatter and XML-tagged sections.

### 5. Create the governance file

Create the companion `.governance.yaml` file at `skills/greeting/agents/greeting-responder.governance.yaml`:

```yaml
version: "0.1.0"
tool_tier: T2

identity:
  role: "Greeting Writer"
  expertise:
    - "Context-appropriate greeting generation"
    - "Team and project introduction messages"
  cognitive_mode: "convergent"

persona:
  tone: "warm"
  communication_style: "friendly"
  audience_level: "adaptive"

capabilities:
  allowed_tools:
    - Read
    - Write
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Misrepresent capabilities or confidence (P-022)"

guardrails:
  input_validation:
    - "Greeting context must be provided"
  output_filtering:
    - "no_secrets_in_output"
    - "no_executable_code_without_confirmation"
    - "greeting_tone_matches_context"
  fallback_behavior: "escalate_to_user"

output:
  required: true
  location: "projects/${JERRY_PROJECT}/greetings/"
  levels:
    - L1

constitution:
  principles_applied:
    - "P-003"
    - "P-020"
    - "P-022"
```

**Expected result:** The governance file exists alongside the agent definition.

### 6. Register the skill in CLAUDE.md

Open `CLAUDE.md` and add your skill to the Skills table in the Quick Reference section:

```markdown
| `/greeting` | Friendly greetings and welcome messages |
```

**Expected result:** The `/greeting` entry appears in the CLAUDE.md skills table.

### 7. Verify the skill structure

Run a quick check to confirm all files are in place:

```bash
find skills/greeting -type f | sort
```

**Expected result:**

```
skills/greeting/SKILL.md
skills/greeting/agents/greeting-responder.governance.yaml
skills/greeting/agents/greeting-responder.md
```

### 8. Test the skill trigger

Start a new Claude Code session and type:

```
Say hello to the team.
```

**Expected result:** Claude Code activates the `/greeting` skill and invokes the `greeting-responder` agent, producing a team greeting.

## What You Learned

You now know how to:
- Create a skill directory with kebab-case naming per H-25
- Write a `SKILL.md` with required YAML frontmatter (name, description, version, tools, activation-keywords)
- Define an agent using the dual-file architecture (`.md` + `.governance.yaml`) per H-34
- Register a skill in `CLAUDE.md` per H-26
- Verify that the skill triggers on activation keywords

## Related

- **How-To Guide:** [How to register a skill in the Jerry Framework](howto-register-skill.md) -- Focused registration steps
- **Reference:** [Diataxis Quality Criteria Reference](reference-diataxis-criteria.md) -- Full specification of quality criteria
- **Explanation:** [About Jerry's Context Rot Problem](explanation-context-rot.md) -- Why Jerry's architecture works the way it does

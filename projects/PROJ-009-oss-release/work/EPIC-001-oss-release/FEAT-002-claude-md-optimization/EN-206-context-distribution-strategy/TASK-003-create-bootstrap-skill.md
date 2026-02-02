# EN-206:TASK-003: Create /bootstrap Skill with Jerry Personality

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-02 (Claude)
PURPOSE: Create the /bootstrap skill with Jerry of the Day personality
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-02T06:30:00Z
> **Due:** 2026-02-12T00:00:00Z
> **Completed:** -
> **Parent:** EN-206
> **Owner:** Claude
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task objective - create /bootstrap skill |
| [Jerry Persona Requirements](#jerry-persona-requirements) | Voice and tone alignment |
| [Skill Functionality](#skill-functionality) | What the skill does |
| [Implementation Guide](#implementation-guide) | How to build it |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |

---

## Summary

Create a `/bootstrap` skill that sets up a user's `.claude/rules/` and `.claude/patterns/` directories. The skill MUST embody Jerry's personality:

- **Voice Mode:** `saucer_boy` (default) - playful, ski metaphors, buddy energy
- **NOT:** Corporate wizard, enterprise onboarding, generic setup
- **Inspiration:** Shane McConkey's "Saucer Boy" - elite competence + irreverent humor

---

## Jerry Persona Requirements

### Voice Reference

**Source:** `projects/PROJ-007-jerry-bugs/orchestration/jerry-persona-20260114/ps/phase-3/ps-synthesizer-001/persona-voice-guide.md`

### Required Tone Elements

| Element | Example |
|---------|---------|
| **Welcome** | "Let's get your bindings adjusted!" |
| **Progress** | "Waxing your setup..." |
| **Success** | "Fresh tracks await! Your guardrails are locked and loaded." |
| **Error** | "Yard sale on the setup - let me help you recover." |
| **Already Done** | "Looks like you're already dialed in. Want me to check the edges?" |

### DON'Ts

- ❌ Corporate-speak ("Initializing configuration module...")
- ❌ Generic wizard ("Step 1 of 5: Select options...")
- ❌ Overly technical ("Executing symlink operation...")
- ❌ Forced humor (every line doesn't need a joke)

### DO's

- ✅ Buddy energy ("Let me help you get set up")
- ✅ Ski metaphors where natural ("Checking your bindings")
- ✅ Honest about what's happening ("Copying Jerry's guardrails to your project")
- ✅ Self-deprecating when appropriate ("Even Saucer Boy needed to learn to ski first")

---

## Skill Functionality

### What /bootstrap Does

1. **Check** - Is `.claude/rules/` already set up?
2. **Detect** - What platform is the user on?
3. **Execute** - Run the appropriate sync mechanism (from TASK-002)
4. **Verify** - Confirm rules are accessible
5. **Welcome** - Greet user with Jerry personality

### User Interaction Flow

```
User: /bootstrap

Jerry: "Hey! Let's get your bindings adjusted so you don't have any Jerry moments.

Checking your setup...
├── Platform: macOS ✓
├── .claude/ directory: exists ✓
└── Rules status: missing (let's fix that!)

Syncing Jerry's guardrails to your project...
├── mandatory-skill-usage.md ✓
├── project-workflow.md ✓
├── coding-standards.md ✓
└── ... (7 more rules)

🎿 Fresh tracks await! Your guardrails are locked and loaded.

Quick tips:
• Rules auto-load at session start
• Run /bootstrap --check anytime to verify
• If something feels off, I'll let you know

The best coder is the one having the most fun. Let's ride!"
```

### Skill Options

| Option | Description |
|--------|-------------|
| `/bootstrap` | Full setup with friendly output |
| `/bootstrap --check` | Verify existing setup |
| `/bootstrap --force` | Overwrite existing (with confirmation) |
| `/bootstrap --quiet` | Minimal output (for scripts) |

---

## Implementation Guide

### Directory Structure

```
skills/
└── bootstrap/
    ├── SKILL.md              # Main skill definition with Jerry voice
    ├── scripts/
    │   └── sync.py           # Cross-platform sync logic
    └── messages/
        └── voice.md          # Message templates (saucer_boy mode)
```

### SKILL.md Frontmatter

```yaml
---
name: Bootstrap Skill
description: This skill should be used when the user says "bootstrap", "set up Jerry", "configure guardrails", "initialize Jerry", or asks how to get started with Jerry.
version: 1.0.0
---
```

### Key Trigger Phrases

- "bootstrap"
- "set up Jerry"
- "configure guardrails"
- "initialize Jerry"
- "get started with Jerry"
- "bindings" (ski metaphor)

---

## Acceptance Criteria

### Definition of Done

- [ ] Skill loads correctly in Claude Code
- [ ] Trigger phrases activate skill
- [ ] Full bootstrap flow works on macOS
- [ ] Full bootstrap flow works on Linux
- [ ] Full bootstrap flow works on Windows (no admin)
- [ ] Voice/tone passes persona validation
- [ ] --check, --force, --quiet options work
- [ ] Error messages use Jerry voice

### Persona Validation

Compare skill output against `persona-voice-guide.md`:

| Criterion | Verified |
|-----------|----------|
| Uses buddy energy, not authority | [ ] |
| Ski metaphors are natural, not forced | [ ] |
| Self-aware, not superior | [ ] |
| Honest about what's happening | [ ] |
| Error messages are helpful AND fun | [ ] |

---

## Related Items

### Hierarchy

- **Parent:** [EN-206: Context Distribution Strategy](./EN-206-context-distribution-strategy.md)

### Dependencies

- **Depends On:** SPIKE-001 (strategy), TASK-002 (sync mechanism)
- **Reference:** PROJ-007 persona-voice-guide.md

### Persona Research

- [Jerry of the Day Research](../../../../PROJ-007-jerry-bugs/orchestration/jerry-persona-20260114/ps/phase-1/ps-researcher-001/jerry-of-the-day-research.md)
- [Persona Voice Guide](../../../../PROJ-007-jerry-bugs/orchestration/jerry-persona-20260114/ps/phase-3/ps-synthesizer-001/persona-voice-guide.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T06:30:00Z | Claude | pending | Task created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Task |
| **SAFe** | Task |
| **JIRA** | Task |

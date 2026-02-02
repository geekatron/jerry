# {Skill Name} Playbook

> **Version:** X.Y.Z
> **Skill:** {skill-name}
> **Purpose:** {One-line purpose}
> **Updated:** YYYY-MM-DD

---

## Document Overview

```
╔═════════════════════════════════════════════════════════════════════════════╗
║                        TRIPLE-LENS COGNITIVE FRAMEWORK                       ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║    L0 (ELI5)          L1 (Engineer)         L2 (Architect)                 ║
║    ──────────         ─────────────         ──────────────                 ║
║    WHAT & WHY    →    HOW (commands)   →    CONSTRAINTS                    ║
║    Metaphors          Invocations           Anti-patterns                  ║
║    Intent             File paths            Boundaries                     ║
║    Analogies          Input/Output          Invariants                     ║
║                                                                             ║
║    "Explains to       "Executable           "Prevents                      ║
║     newcomers"         instructions"          mistakes"                    ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

**Target Audience:**
- **L0**: Anyone (stakeholders, newcomers, non-technical)
- **L1**: Engineers executing the skill
- **L2**: Architects designing workflows, debugging issues

---

# L0: The Big Picture (ELI5)

> *This section explains WHAT the skill does and WHY it matters using metaphors and analogies.*

## What Is This Skill?

### The Metaphor

```
╔═══════════════════════════════════════════════════════════════╗
║                    {METAPHOR TITLE}                            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   {Describe the real-world metaphor that explains this        ║
║    skill's purpose. Make it vivid and memorable.}             ║
║                                                               ║
║   Example: "Think of orchestration like conducting an         ║
║   orchestra - you don't play instruments yourself, you        ║
║   coordinate when each section plays and ensure they          ║
║   harmonize together."                                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Plain English:**
{1-2 sentences explaining what this skill does without jargon}

### Why Does This Matter?

| Without This Skill | With This Skill |
|-------------------|-----------------|
| {Problem 1} | {Solution 1} |
| {Problem 2} | {Solution 2} |
| {Problem 3} | {Solution 3} |

### When Do I Use This?

```
DECISION GUIDE:
───────────────

START: What do you need?
       │
  ┌────┴────────────────────────────────┐
  │                                      │
  ▼                                      ▼
{Trigger 1}                        {Trigger 2}
  │                                      │
  ▼                                      ▼
USE {skill}                        USE {other skill}
```

**Activation Keywords:** {keyword1}, {keyword2}, {keyword3}

---

## The Cast of Characters (Agents)

> *Meet the specialists who do the work*

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                           AGENT PORTFOLIO                                  ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      ║
║   │ {agent-1}       │    │ {agent-2}       │    │ {agent-3}       │      ║
║   │ ────────────    │    │ ────────────    │    │ ────────────    │      ║
║   │ {1-line role}   │    │ {1-line role}   │    │ {1-line role}   │      ║
║   └─────────────────┘    └─────────────────┘    └─────────────────┘      ║
║                                                                           ║
║   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      ║
║   │ {agent-4}       │    │ {agent-5}       │    │ {agent-6}       │      ║
║   │ ────────────    │    │ ────────────    │    │ ────────────    │      ║
║   │ {1-line role}   │    │ {1-line role}   │    │ {1-line role}   │      ║
║   └─────────────────┘    └─────────────────┘    └─────────────────┘      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

| Agent | Like a... | Does What |
|-------|-----------|-----------|
| `{agent-1}` | {metaphor} | {plain english} |
| `{agent-2}` | {metaphor} | {plain english} |
| `{agent-3}` | {metaphor} | {plain english} |
| `{agent-4}` | {metaphor} | {plain english} |

---

# L1: How To Use It (Engineer)

> *This section provides executable instructions: commands, invocations, file paths.*

## Quick Start

### The 30-Second Version

1. **{Step 1 action}** - {brief description}
2. **{Step 2 action}** - {brief description}
3. **{Step 3 action}** - {brief description}

### Minimal Example

```
User: "{Natural language prompt example}"

Claude: [Activates {agent-name}]
        [Performs {action}]
        [Creates {output file path}]
        [Returns summary]
```

---

## Invocation Methods

### Method 1: Natural Language (Recommended)

Just describe what you need. The orchestrator selects the right agent.

```
"{Example prompt 1}"
→ Activates {agent-1}

"{Example prompt 2}"
→ Activates {agent-2}

"{Example prompt 3}"
→ Activates {agent-3}
```

### Method 2: Explicit Agent Request

Name the agent directly:

```
"Use {agent-1} to {task description}"
"Have {agent-2} do {specific action}"
```

### Method 3: Chained Request

Request a sequence:

```
"First {action 1}, then {action 2}, finally {action 3}"
```

---

## Agent Reference

| Agent | When to Use | Keywords | Output Location |
|-------|-------------|----------|-----------------|
| `{agent-1}` | {scenario} | {kw1}, {kw2} | `{path/}` |
| `{agent-2}` | {scenario} | {kw1}, {kw2} | `{path/}` |
| `{agent-3}` | {scenario} | {kw1}, {kw2} | `{path/}` |
| `{agent-4}` | {scenario} | {kw1}, {kw2} | `{path/}` |

---

## Orchestration Patterns

> See [ORCHESTRATION_PATTERNS.md](ORCHESTRATION_PATTERNS.md) for complete pattern catalog.

### Pattern Selection Quick Reference

```
PATTERN SELECTION DECISION TREE:
────────────────────────────────

START: How many agents needed?
       │
  ┌────┴────┐
  │         │
  ▼         ▼
ONE       MULTIPLE
  │         │
  ▼         ▼
Pattern 1   Are they dependent?
(Single)    │
       ┌────┴────┐
       │         │
       ▼         ▼
      YES        NO
       │         │
       ▼         ▼
   Pattern 2   Pattern 3
   (Sequential) (Fan-Out)
```

### Patterns Applicable to This Skill

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Single Agent** | {scenario} | `{example}` |
| **Sequential Chain** | {scenario} | `{example}` |
| **Fan-Out** | {scenario} | `{example}` |
| **Fan-In** | {scenario} | `{example}` |

---

## Common Workflows

### Workflow 1: {Workflow Name}

**Goal:** {What this workflow achieves}

```
WORKFLOW DIAGRAM:
─────────────────

┌─────────┐    ┌─────────┐    ┌─────────┐
│ Step 1  │───►│ Step 2  │───►│ Step 3  │
│ {agent} │    │ {agent} │    │ {agent} │
└─────────┘    └─────────┘    └─────────┘
     │              │              │
     ▼              ▼              ▼
{artifact}    {artifact}    {artifact}
```

**Steps:**
1. `"{prompt for step 1}"`
2. `"{prompt for step 2}"`
3. `"{prompt for step 3}"`

**Output Artifacts:**
- `{path/to/artifact1.md}` - {description}
- `{path/to/artifact2.md}` - {description}

---

### Workflow 2: {Workflow Name}

**Goal:** {What this workflow achieves}

**Steps:**
1. {Step 1 description}
2. {Step 2 description}
3. {Step 3 description}

**Example:**
```
User: {example prompt}

Agent: {example response}
```

---

## Output Locations

All artifacts are persisted to your project directory:

```
projects/{PROJECT}/
├── {dir1}/          # {description}
├── {dir2}/          # {description}
├── {dir3}/          # {description}
└── {dir4}/          # {description}
```

| Agent | Output Directory | File Pattern |
|-------|-----------------|--------------|
| `{agent-1}` | `{path/}` | `{pattern}.md` |
| `{agent-2}` | `{path/}` | `{pattern}.md` |
| `{agent-3}` | `{path/}` | `{pattern}.md` |

---

## Tips and Best Practices

### 1. Be Specific

```
Bad:  "{vague request}"
Good: "{specific request with context}"
```

### 2. Provide Context

```
Bad:  "{request without context}"
Good: "{request with relevant context}"
```

### 3. Reference Previous Work

```
"Based on {previous artifact}, {new request}"
```

---

## Troubleshooting

### Problem: {Common Problem 1}

**Symptoms:** {What you observe}

**Fix:**
1. {Fix step 1}
2. {Fix step 2}

### Problem: {Common Problem 2}

**Symptoms:** {What you observe}

**Fix:**
1. {Fix step 1}
2. {Fix step 2}

---

# L2: Architecture & Constraints

> *This section documents what NOT to do, boundaries, invariants, and design rationale.*

## Anti-Pattern Catalog

### AP-001: {Anti-Pattern Name}

```
╔═══════════════════════════════════════════════════════════════╗
║ ANTI-PATTERN: {Name}                                          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ SYMPTOM:    {What you observe when this happens}              ║
║                                                               ║
║ CAUSE:      {Why this happens}                                ║
║                                                               ║
║ IMPACT:     {Consequences}                                    ║
║                                                               ║
║ FIX:        {How to avoid or correct}                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Example (Bad):**
```
{Code or invocation showing the anti-pattern}
```

**Example (Good):**
```
{Code or invocation showing the correct approach}
```

---

### AP-002: {Anti-Pattern Name}

**Symptom:** {What you observe}

**Cause:** {Root cause}

**Impact:** {What goes wrong}

**Fix:** {Correct approach}

---

### AP-003: {Anti-Pattern Name}

**Symptom:** {What you observe}

**Cause:** {Root cause}

**Impact:** {What goes wrong}

**Fix:** {Correct approach}

---

## Constraints & Boundaries

### Hard Constraints (Cannot Violate)

| ID | Constraint | Rationale |
|----|------------|-----------|
| HC-001 | {Constraint description} | {Why this exists} |
| HC-002 | {Constraint description} | {Why this exists} |
| HC-003 | {Constraint description} | {Why this exists} |

### Soft Constraints (Should Not Violate)

| ID | Constraint | When to Relax |
|----|------------|---------------|
| SC-001 | {Constraint description} | {Exception scenario} |
| SC-002 | {Constraint description} | {Exception scenario} |

---

## Invariants

> *Conditions that must ALWAYS be true*

```
INVARIANT CHECKLIST:
────────────────────

□ INV-001: {Invariant description}
           Violation: {What breaks if violated}

□ INV-002: {Invariant description}
           Violation: {What breaks if violated}

□ INV-003: {Invariant description}
           Violation: {What breaks if violated}
```

---

## State Management

### Session Context Schema v1.0.0

> See [ORCHESTRATION_PATTERNS.md](ORCHESTRATION_PATTERNS.md) for full schema.

```yaml
session_context:
  version: "1.0.0"
  session_id: "{uuid}"
  source_agent: "{agent-name}"
  target_agent: "{agent-name}"
  state_output_key: "{key}"
  cognitive_mode: "{convergent|divergent}"
  payload:
    findings: [ ... ]
    confidence: 0.0-1.0
```

### Agent State Output Keys

| Agent | Output Key | Cognitive Mode |
|-------|------------|----------------|
| `{agent-1}` | `{key}` | {mode} |
| `{agent-2}` | `{key}` | {mode} |
| `{agent-3}` | `{key}` | {mode} |

---

## Cross-Skill Integration

### Handoff Points

```
CROSS-SKILL HANDOFF:
────────────────────

  ┌─────────────┐         ┌─────────────┐
  │ {skill-1}   │────────►│ {skill-2}   │
  │ {agent-a}   │         │ {agent-b}   │
  └─────────────┘         └─────────────┘
        │                       │
        ▼                       ▼
    {state key}            {receives}
```

| Source Agent | Target Agent | Handoff Context |
|--------------|--------------|-----------------|
| `{source}` | `{target}` | {what passes} |

---

## Design Rationale

### Why {Decision 1}?

**Context:** {Background}

**Decision:** {What we chose}

**Consequences:**
- (+) {Positive consequence}
- (+) {Positive consequence}
- (-) {Trade-off or negative}

### Why {Decision 2}?

**Context:** {Background}

**Decision:** {What we chose}

**Consequences:**
- (+) {Positive consequence}
- (-) {Trade-off}

---

## References

- [{Reference 1}]({url})
- [{Reference 2}]({url})
- [ORCHESTRATION_PATTERNS.md](ORCHESTRATION_PATTERNS.md) - 8 canonical patterns
- [AGENT_TEMPLATE_CORE.md](AGENT_TEMPLATE_CORE.md) - Agent definition format

---

## Appendix A: {Appendix Title}

{Additional reference material as needed}

---

## Appendix B: Quick Reference Card

| Task | Prompt |
|------|--------|
| {Task 1} | `"{prompt}"` |
| {Task 2} | `"{prompt}"` |
| {Task 3} | `"{prompt}"` |
| {Task 4} | `"{prompt}"` |

---

*Playbook Version: X.Y.Z*
*Skill: {skill-name}*
*Last Updated: YYYY-MM-DD*
*Template: PLAYBOOK_TEMPLATE.md v1.0.0*

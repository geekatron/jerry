---
name: problem-statement
description: |
  Manage Problem Statements (PS) for ECW sidequests using event sourcing.

  USE WHEN:
  - Understanding current problem context
  - Adding constraints or questions discovered during work
  - Tracking exploration progress and findings
  - Working on phase-related tasks
  - Starting a session (auto-loaded via SessionStart hook)
  - **AUTOMATIC:** User says "research X", "analyze Y", "investigate Z", etc.

  Provides contextual PS awareness during development with full audit trail.
  Automatically invokes specialized agents when trigger phrases detected.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - TodoWrite
  - Task
  # Context7 MCP tools for library/framework documentation (SOP-CB.6)
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
activation-keywords:
  - research
  - analyze
  - investigate
  - create adr
  - review
  - synthesize
version: "2.7.0"
model: inherit
---

# Problem Statement Skill

> **Version:** 2.7.0
> **Architecture:** Hexagonal + Event Sourcing
> **Progressive Disclosure:** See `references/` for detailed documentation

## Overview

Manages Problem Statements (PS) for ECW sidequests using event sourcing and hexagonal architecture. Provides CLI tools, auto-migration from markdown, and SessionStart integration.

**NEW in v2.7.0:** Automatic Agent Invocation - skill detects trigger phrases and automatically creates PS entries + invokes specialized agents.

---

## Automatic Agent Invocation (Phase 38.17 - Option A)

When the user says phrases like "research X", "analyze Y", or "investigate Z", this skill **automatically**:
1. Detects the trigger phrase
2. Creates a PS exploration entry via CLI
3. Invokes the appropriate specialized agent via Task tool

### Trigger Detection

The skill activates on these trigger phrases:

| Trigger Phrase | Agent Invoked | Entry Type |
|----------------|---------------|------------|
| `research {topic}` | ps-researcher | RESEARCH |
| `analyze {topic}` | ps-analyst | ANALYSIS |
| `investigate {topic}` | ps-investigator | INVESTIGATION |
| `create ADR for {topic}` | ps-architect | DECISION |
| `review {topic}` | ps-reviewer | REVIEW |
| `synthesize {topic}` | ps-synthesizer | SYNTHESIS |

### Activation Rules

1. **Trigger must be at sentence start** - "research API patterns" activates, "I researched this" does not
2. **Topic is extracted** from text following the trigger phrase
3. **Debouncing** - duplicate triggers within 5 seconds are ignored

### Automatic Workflow

When triggered, the skill executes:

```bash
# Step 1: Create PS entry (c-006 compliant - classified at creation)
python3 {baseDir}/scripts/cli.py add-entry {ps-id} "{Type}: {topic}" \
    --type {ENTRY_TYPE} \
    --severity MEDIUM

# Step 2: Capture entry ID from output (e.g., "e-042")

# Step 3: Invoke appropriate agent via Task tool
```

### Task Invocation Template

For each trigger, the skill invokes the Task tool with:

```python
Task(
    description="{agent-name}: {topic}",
    subagent_type="general-purpose",
    prompt="""
You are the {agent-name} agent.

## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id}
- **Topic:** {topic}

## MANDATORY PERSISTENCE (c-009)
After completing your work, you MUST:

1. Use the Write tool to create your output at:
   `sidequests/{sidequest}/docs/{output_dir}/{ps_id}-{entry_id}-{topic_slug}.md`

2. Use the template structure from:
   `.claude/skills/problem-statement/templates/{template}.md`

3. Run this command to link the artifact:
   ```bash
   python3 .claude/skills/problem-statement/scripts/cli.py link-artifact \\
       {ps_id} {entry_id} FILE \\
       "docs/{output_dir}/{ps_id}-{entry_id}-{topic_slug}.md" \\
       "{Type}: {topic}"
   ```

DO NOT return transient output only. File creation AND link-artifact are MANDATORY.

## CONTEXT7 MCP INTEGRATION (SOP-CB.6)
If researching a library or framework:
1. Use `mcp__context7__resolve-library-id` to get library ID
2. Use `mcp__context7__query-docs` to query documentation

## YOUR {TYPE} TASK
{specific_task_instructions}

## COMPLETION CHECKLIST
- [ ] File created with Write tool
- [ ] link-artifact command executed
- [ ] Frontmatter includes ps and exploration fields
- [ ] Template structure followed
"""
)
```

### Agent-Specific Templates

| Agent | Template | Output Directory |
|-------|----------|------------------|
| ps-researcher | `templates/research.md` | `docs/research/` |
| ps-analyst | `templates/deep-analysis.md` | `docs/analysis/` |
| ps-architect | `templates/adr.md` | `docs/decisions/` |
| ps-reviewer | `templates/review.md` | `docs/reviews/` |
| ps-investigator | `templates/investigation.md` | `docs/investigations/` |
| ps-synthesizer | `templates/synthesis.md` | `docs/synthesis/` |

### Token Budget Warning (FMEA Risk A4)

When token budget exceeds 80%, the skill warns:

```
⚠️ TOKEN BUDGET WARNING
Current session at 80% token budget.
Consider using SDK orchestrator for complex multi-agent pipelines.
SDK approach offers 67% token reduction via context isolation.
```

### Negative Examples (No Activation)

These phrases do NOT trigger automatic invocation:

| Input | Why Not |
|-------|---------|
| "I researched this yesterday" | Past tense, not imperative |
| "what is the capital of France" | No trigger phrase |
| "the research shows..." | "research" not at sentence start |

### Error Handling

| Error | Behavior |
|-------|----------|
| CLI command fails | Report error, no Task invocation |
| Entry ID not parseable | Report parsing error, no Task invocation |
| No PS exists for phase | Suggest creating PS first |
| Task tool blocked | Report failure, entry remains (no rollback) |

### Multi-Agent Pipelines

For complex multi-step work like "research X, then analyze, then create ADR", the skill recommends using the SDK orchestrator instead:

```
💡 RECOMMENDATION
Multi-agent pipeline detected. Consider using SDK orchestrator:
python3 .claude/skills/problem-statement/orchestrator/pipeline.py \\
    --phases research,analyze,decide \\
    --topic "{topic}"

Benefits: 67% token reduction, context isolation, native subagent support.
```

---

## Dependencies

- **ECW Library:** `.claude/lib/ecw/`
- **Python:** >=3.9
- **Packages:** cloudevents>=1.11.0

## Quick Start

```bash
# Create PS
python {baseDir}/scripts/cli.py create <ps-id> "<title>"

# Add constraint
python {baseDir}/scripts/cli.py add-constraint <ps-id> "<text>"

# Add question
python {baseDir}/scripts/cli.py add-question <ps-id> "<text>"

# View PS
python {baseDir}/scripts/cli.py view <ps-id>

# Export to markdown
python {baseDir}/scripts/cli.py export <ps-id> <output.md>
```

## Querying PS State (c-007)

**CRITICAL: Use CLI list commands, NOT grep on markdown exports.**

```bash
# List open exploration entries
python {baseDir}/scripts/cli.py list-entries <ps-id> --status OPEN

# List all entries (no filter)
python {baseDir}/scripts/cli.py list-entries <ps-id>

# List unvalidated constraints
python {baseDir}/scripts/cli.py list-constraints <ps-id> --status HYPOTHESIS

# List unanswered questions
python {baseDir}/scripts/cli.py list-questions <ps-id> --status OPEN
```

### Available Filters

| Command | Filter Options |
|---------|----------------|
| `list-entries` | `OPEN`, `RESOLVED`, `WONT_FIX` |
| `list-constraints` | `HYPOTHESIS`, `VALIDATED`, `DEFERRED`, `REJECTED` |
| `list-questions` | `OPEN`, `ANSWERED` |

### Forbidden Patterns (c-007)

| Forbidden | Use Instead |
|-----------|-------------|
| `view --format markdown \| grep OPEN` | `list-entries --status OPEN` |
| `export && grep HYPOTHESIS` | `list-constraints --status HYPOTHESIS` |
| `cat PS-*.md \| grep` | Use CLI list commands |

## Exploration Entry Classification (c-006)

**CRITICAL: All exploration entries MUST be classified at creation time.**

Unclassified entries (Type=UNKNOWN, Severity=NOT_ASSESSED) provide no actionable value and waste tokens on useless output.

### Mandatory Classification

```bash
# CORRECT: Classified at creation (c-006 compliant)
python {baseDir}/scripts/cli.py add-entry <ps-id> "Finding description" \
    --type DISCOVERY \
    --type-context "Found during codebase analysis" \
    --severity MEDIUM \
    --severity-rationale "Affects implementation approach"

# WARNING: Unclassified entry (c-006 violation warning shown)
python {baseDir}/scripts/cli.py add-entry <ps-id> "Finding description"
```

### Entry Types

| Type | Use When |
|------|----------|
| `RESEARCH` | Investigating documentation, patterns, prior art |
| `ANALYSIS` | Examining code, architecture, data flows |
| `DISCOVERY` | Found unexpected behavior, hidden constraints |
| `DECISION` | Made implementation choice, selected approach |
| `INSIGHT` | Synthesized understanding, connected concepts |
| `BLOCKER` | Identified impediment requiring resolution |

### Severity Levels

| Level | Use When |
|-------|----------|
| `CRITICAL` | Blocks all progress, must resolve immediately |
| `HIGH` | Significant impact, needs attention soon |
| `MEDIUM` | Notable finding, plan for resolution |
| `LOW` | Minor observation, address when convenient |

### Retroactive Classification

If entries exist without classification:

```bash
# Set type
python {baseDir}/scripts/cli.py set-entry-type <ps-id> e-001 DISCOVERY \
    --context "Classified retroactively"

# Set severity
python {baseDir}/scripts/cli.py assess-severity <ps-id> e-001 MEDIUM \
    --rationale "Impact assessment after discovery"
```

## Key Features

| Feature | Description |
|---------|-------------|
| Event Sourcing | Full audit trail via CloudEvents 1.0 |
| Auto-Migration | Legacy markdown PSs migrate automatically |
| SessionStart | PS context loaded at session start |
| 6 Entity Types | Constraints, Questions, Explorations, Experiences, Wisdoms, Relationships |

## Data Storage

| Store | Location | Configurable Via |
|-------|----------|------------------|
| Events | `.ecw/events.db` | `ECW_EVENT_STORE_PATH` |
| Projections | `.ecw/projections.db` | `ECW_PROJECTION_STORE_PATH` |
| Legacy MD | `sidequests/<name>/docs/ps/` | Auto-migrated |

## Session Integration

At session start, the SessionStart hook:
1. Detects active sidequest from git branch
2. Loads PS state via hooks adapter
3. Displays PS summary in context
4. Checks for drift between database and markdown (Phase 38.17)

## Source of Truth (Phase 38.17)

**CRITICAL: The event database is the canonical source of truth, NOT markdown exports.**

### Best Practices

| Do | Don't |
|----|-------|
| Query database first with CLI | Read markdown exports as primary |
| Use `cli.py view` to get current state | Assume markdown is up-to-date |
| Export with `cli.py export` after changes | Edit markdown directly (unless providing feedback) |
| Run `cli.py sync` to import user edits | Trust markdown over database |

### Database-First Workflow

```bash
# 1. ALWAYS query database first
python {baseDir}/scripts/cli.py view <ps-id>

# 2. Make changes via CLI
python {baseDir}/scripts/cli.py add-constraint <ps-id> "..."

# 3. Export to markdown for user review
python {baseDir}/scripts/cli.py export <ps-id> <output.md>

# 4. If user edits markdown, sync back
python {baseDir}/scripts/cli.py sync <ps-id>
```

### Drift Detection

When SessionStart detects drift between database and markdown:
- **Soft enforcement:** Warning displayed at session start
- **Medium enforcement:** Warning on PS commands (future)
- **Hard enforcement:** Block PS closure until resolved

### User Feedback Loop (SOP-PS.6)

Users CAN edit the PS markdown to provide feedback:
1. User edits markdown (adds answers, constraints, or `<!-- USER_FEEDBACK: ... -->`)
2. Claude runs `cli.py sync <ps-id>` to import changes
3. Database is updated with user feedback
4. Re-export to update fingerprints

## Testing

```bash
pytest {baseDir}/tests/ -v
```

## Detailed Documentation

For comprehensive documentation, see the `references/` directory:

| Document | Content |
|----------|---------|
| [architecture.md](references/architecture.md) | Hexagonal architecture, directory structure |
| [cli-commands.md](references/cli-commands.md) | Full CLI reference (40+ commands) |
| [event-sourcing.md](references/event-sourcing.md) | Event types, storage, projections |
| [migration-guide.md](references/migration-guide.md) | Legacy markdown migration |

---

<!-- CANONICAL SOURCE: references/architecture.md -->
<!-- Detailed architecture moved for progressive disclosure -->
<!-- See references/ for full documentation -->

## Architecture Summary

```
.claude/skills/problem-statement/
├── SKILL.md              # This file
├── agents/               # Agent definition files (Phase 38.17)
│   ├── ps-researcher.md  # Deep research agent (6W + academic rigor)
│   ├── ps-validator.md   # Constraint validation agent
│   ├── ps-reporter.md    # Status reporting agent
│   ├── ps-analyst.md     # Deep analysis (5 Whys, Trade-offs, FMEA)
│   ├── ps-architect.md   # Architecture decisions (ADR/Nygard)
│   ├── ps-reviewer.md    # Quality review (code, security, design)
│   ├── ps-investigator.md # Failure analysis (5 Whys, Ishikawa)
│   └── ps-synthesizer.md # Cross-document synthesis (Thematic Analysis)
├── scripts/
│   ├── cli.py            # CLI → hexagonal adapter
│   ├── loader.py         # SessionStart integration
│   ├── invoke_researcher.py    # ps-researcher wrapper (c-009)
│   ├── invoke_validator.py     # ps-validator wrapper (c-009)
│   ├── invoke_reporter.py      # ps-reporter wrapper (c-009)
│   ├── invoke_analyst.py       # ps-analyst wrapper (c-009)
│   ├── invoke_architect.py     # ps-architect wrapper (c-009)
│   ├── invoke_reviewer.py      # ps-reviewer wrapper (c-009)
│   ├── invoke_investigator.py  # ps-investigator wrapper (c-009)
│   ├── invoke_synthesizer.py   # ps-synthesizer wrapper (c-009)
│   └── ...
├── templates/            # Output templates (Phase 38.17)
│   ├── research.md       # Research document template (6W framework)
│   ├── analysis.md       # Analysis report template
│   ├── deep-analysis.md  # Deep analysis (5 Whys, Trade-off, FMEA)
│   ├── adr.md            # Architecture Decision Record (Nygard)
│   ├── review.md         # Quality review (severity categorized)
│   ├── investigation.md  # Investigation report (Ishikawa, 5 Whys)
│   └── synthesis.md      # Synthesis document (Thematic Analysis)
└── references/           # Progressive disclosure
    ├── architecture.md
    ├── cli-commands.md
    ├── event-sourcing.md
    └── migration-guide.md
```

## Agents

The PS skill provides specialized agents for different tasks. Each agent has a definition file in `agents/` and an invocation wrapper in `scripts/`.

### Agent Portfolio Overview

| Tier | Agent | Purpose | Prior Art |
|------|-------|---------|-----------|
| **Core** | ps-explorer | Codebase exploration (read-only) | - |
| **Core** | ps-researcher | Deep research (6W, academic rigor) | Lasswell (1948), Creswell (2014) |
| **Core** | ps-validator | Constraint validation | - |
| **Core** | ps-reporter | Status reporting | - |
| **Tier 1** | ps-analyst | Deep analysis, root cause | Toyota 5 Whys, NASA FMEA |
| **Tier 1** | ps-architect | Architecture decisions | Nygard ADR (2011) |
| **Tier 1** | ps-reviewer | Quality review | OWASP, Google Style |
| **Tier 2** | ps-investigator | Failure/incident analysis | Ishikawa (1990), 5 Whys |
| **Tier 2** | ps-synthesizer | Cross-document synthesis | Braun & Clarke (2006) |

### Agent Reference Table

| Agent | Definition | Wrapper | Persistence |
|-------|------------|---------|-------------|
| **ps-explorer** | N/A (read-only) | N/A | No |
| **ps-researcher** | [`agents/ps-researcher.md`](agents/ps-researcher.md) | [`scripts/invoke_researcher.py`](scripts/invoke_researcher.py) | **MANDATORY** |
| **ps-validator** | [`agents/ps-validator.md`](agents/ps-validator.md) | [`scripts/invoke_validator.py`](scripts/invoke_validator.py) | **MANDATORY** |
| **ps-reporter** | [`agents/ps-reporter.md`](agents/ps-reporter.md) | [`scripts/invoke_reporter.py`](scripts/invoke_reporter.py) | **MANDATORY** |
| **ps-analyst** | [`agents/ps-analyst.md`](agents/ps-analyst.md) | [`scripts/invoke_analyst.py`](scripts/invoke_analyst.py) | **MANDATORY** |
| **ps-architect** | [`agents/ps-architect.md`](agents/ps-architect.md) | [`scripts/invoke_architect.py`](scripts/invoke_architect.py) | **MANDATORY** |
| **ps-reviewer** | [`agents/ps-reviewer.md`](agents/ps-reviewer.md) | [`scripts/invoke_reviewer.py`](scripts/invoke_reviewer.py) | **MANDATORY** |
| **ps-investigator** | [`agents/ps-investigator.md`](agents/ps-investigator.md) | [`scripts/invoke_investigator.py`](scripts/invoke_investigator.py) | **MANDATORY** |
| **ps-synthesizer** | [`agents/ps-synthesizer.md`](agents/ps-synthesizer.md) | [`scripts/invoke_synthesizer.py`](scripts/invoke_synthesizer.py) | **MANDATORY** |

### Agent Invocation (Recommended: Use Wrapper Scripts)

The wrapper scripts automate c-009 compliant invocation:

```bash
# Core Agents
python3 {baseDir}/scripts/invoke_researcher.py <ps-id> "<topic>" "<research-prompt>"
python3 {baseDir}/scripts/invoke_validator.py <ps-id> "<topic>" "<constraints>"
python3 {baseDir}/scripts/invoke_reporter.py <ps-id> <report-type>

# Tier 1 Agents
python3 {baseDir}/scripts/invoke_analyst.py <ps-id> <analysis-type> "<topic>" "<analysis-prompt>"
python3 {baseDir}/scripts/invoke_architect.py <ps-id> "<decision-title>" "<context>"
python3 {baseDir}/scripts/invoke_reviewer.py <ps-id> <review-type> "<subject>" "<review-focus>"

# Tier 2 Agents
python3 {baseDir}/scripts/invoke_investigator.py <ps-id> "<symptom>" "<investigation-context>"
python3 {baseDir}/scripts/invoke_synthesizer.py <ps-id> "<topic>" "<input-docs>" "<synthesis-focus>"
```

### Analysis Types (ps-analyst)

| Type | Framework | Description |
|------|-----------|-------------|
| `root-cause` | Toyota 5 Whys | Drill down to root cause |
| `trade-off` | Kepner-Tregoe | Weighted criteria matrix |
| `gap` | Gap Analysis | Current vs desired state |
| `risk` | NASA FMEA | Failure mode analysis |
| `impact` | Impact Analysis | Change consequence assessment |
| `dependency` | Dependency Mapping | Component coupling analysis |

### Review Types (ps-reviewer)

| Type | Standards | Focus Areas |
|------|-----------|-------------|
| `code` | Google Code Style | Correctness, error handling, style |
| `design` | SOLID, GRASP | SRP, OCP, LSP, ISP, DIP |
| `architecture` | C4 Model | Coupling, cohesion, boundaries |
| `security` | OWASP Top 10 (2021) | Injection, auth, XSS, CSRF |
| `documentation` | Technical Writing | Clarity, completeness, accuracy |

### Report Types (ps-reporter)

| Type | Description |
|------|-------------|
| `phase-status` | Phase progress overview |
| `constraint-status` | Constraint satisfaction report |
| `knowledge-summary` | KB items generated in phase |
| `experience-wisdom` | Experience/Wisdom synthesis |

### When to Use Each Agent

| Use Case | Agent | Output |
|----------|-------|--------|
| Quick codebase scan | ps-explorer | N/A (read-only) |
| Deep 6W research | **ps-researcher** | `docs/research/` |
| Validate constraints | **ps-validator** | Validation report |
| Generate phase reports | **ps-reporter** | `docs/reports/` |
| Root cause / trade-off analysis | **ps-analyst** | `docs/analysis/` |
| Architecture decisions | **ps-architect** | `docs/decisions/` |
| Quality review (code/security) | **ps-reviewer** | `docs/reviews/` |
| Failure investigation | **ps-investigator** | `docs/investigations/` |
| Cross-document synthesis | **ps-synthesizer** | `docs/synthesis/` |

### Agent Output Locations

| Agent | Location | Template |
|-------|----------|----------|
| ps-researcher | `docs/research/{ps-id}-{entry-id}-{topic-slug}.md` | `templates/research.md` |
| ps-analyst | `docs/analysis/{ps-id}-{entry-id}-{analysis-type}.md` | `templates/deep-analysis.md` |
| ps-architect | `docs/decisions/{ps-id}-{entry-id}-adr.md` | `templates/adr.md` |
| ps-reviewer | `docs/reviews/{ps-id}-{entry-id}-{review-type}.md` | `templates/review.md` |
| ps-investigator | `docs/investigations/{ps-id}-{entry-id}-investigation.md` | `templates/investigation.md` |
| ps-synthesizer | `docs/synthesis/{ps-id}-{entry-id}-synthesis.md` | `templates/synthesis.md` |
| ps-reporter | `docs/reports/{ps-id}-{entry-id}-{report-type}.md` | `templates/report.md` |

---

## Sub-Agent Persistence (c-009, c-010) - CRITICAL

**Problem:** Sub-agents return transient outputs that are lost when sessions end.

**Solution:** All artifact-producing agents MUST:
1. Use the **Write tool** to create files at proper locations
2. Call **link-artifact** to establish bidirectional traceability

### Four-Tier Enforcement (c-009)

| Tier | Hook | Behavior |
|------|------|----------|
| **Advisory** | SessionStart | Reminder displayed at session start |
| **Soft** | Stop | Warning if Task invoked without file creation |
| **Medium** | PreToolUse (Task) | Persistence reminder injected into agent prompt |
| **Hard** | PostToolUse (Task) | Block continuation until file created |

### Agent Persistence Checklist

When invoking ps-researcher, ps-validator, or ps-reporter:

```
┌─────────────────────────────────────────────────────────────┐
│ SUB-AGENT PERSISTENCE CHECKLIST (c-009)                     │
├─────────────────────────────────────────────────────────────┤
│ [ ] 1. Create exploration entry (add-entry with --type)     │
│ [ ] 2. Include entry ID in agent prompt                     │
│ [ ] 3. Agent uses Write tool to create file                 │
│ [ ] 4. Agent calls link-artifact after file creation        │
│ [ ] 5. Verify file exists in repository                     │
│ [ ] 6. Verify PS shows artifact linkage                     │
└─────────────────────────────────────────────────────────────┘
```

### Correct Agent Invocation Pattern

```bash
# 1. Create exploration entry FIRST
python {baseDir}/scripts/cli.py add-entry phase-38.17 "Research topic" \
    --type RESEARCH --severity MEDIUM
# Returns: e-XXX

# 2. Invoke agent with EXPLICIT persistence instructions
# Include in Task prompt:
"""
You are ps-researcher.

## MANDATORY PERSISTENCE (c-009)
You MUST:
1. Create file at: docs/research/{ps-id}-{entry-id}-{topic-slug}.md
2. Use template: .claude/skills/problem-statement/templates/research.md
3. After creating file, run:
   python3 .claude/skills/problem-statement/scripts/cli.py link-artifact \
       {ps-id} {entry-id} FILE "{file-path}" "{description}"

DO NOT return transient output only. File creation is MANDATORY.

## Your Task
{actual_research_prompt}
"""

# 3. Verify after agent completes
python {baseDir}/scripts/cli.py view phase-38.17  # Should show artifact link
ls docs/research/{ps-id}-{entry-id}-*.md          # Should exist
```

### File Naming Convention

| Component | Format | Example |
|-----------|--------|---------|
| PS ID | `phase-{N}.{M}` | `phase-38.17` |
| Entry ID | `e-{NNN}` | `e-036` |
| Topic Slug | `{lowercase-hyphenated}` | `subagent-persistence` |
| **Full Path** | `docs/research/{ps-id}-{entry-id}-{topic-slug}.md` | `docs/research/phase-38.17-e-036-subagent-persistence.md` |

### Bidirectional Traceability (c-010)

**One-way traceability (BAD):**
- File frontmatter references PS → BUT PS has no link to file
- Cannot query PS to find artifacts

**Bidirectional traceability (GOOD):**
- File frontmatter references PS AND entry ID
- PS has artifact link via `link-artifact` command
- Can query both directions

**File Frontmatter Example:**
```yaml
---
ps: phase-38.17
exploration: e-036
created: 2026-01-03
status: RESEARCH
agent: ps-researcher
---
```

**PS View Output Should Show:**
```
## Exploration Log
  - [e-036] [RESEARCH] [MEDIUM] Research topic
    Artifacts:
      - FILE: docs/research/phase-38.17-e-036-topic.md
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.7.0 | 2026-01-04 | Phase 38.17: Automatic Agent Invocation (Option A Skill-as-Orchestrator), activation-keywords in frontmatter, Task tool invocation |
| 2.6.0 | 2026-01-03 | Phase 38.17: Complete agent portfolio (8 agents), 5 new agents (ps-analyst, ps-architect, ps-reviewer, ps-investigator, ps-synthesizer) with evidence-based methodologies |
| 2.5.0 | 2026-01-03 | Phase 38.17: Agent definition files (`agents/`), wrapper scripts for c-009 compliance |
| 2.4.0 | 2026-01-03 | Phase 38.17: list-entries/constraints/questions with --status filter (c-007) |
| 2.3.0 | 2026-01-03 | Phase 38.17: Mandatory entry classification (c-006), CLI auto-classification |
| 2.2.0 | 2026-01-03 | Phase 38.17: Database-first guidance, sync command, drift detection |
| 2.1.1 | 2026-01-02 | Add ps-researcher agent, templates, agent documentation |
| 2.1.0 | 2026-01-02 | Progressive disclosure, `{baseDir}` paths |
| 2.0.0 | 2025-12-30 | Hexagonal architecture rewrite |
| 1.0.0 | 2025-12-28 | Initial release |
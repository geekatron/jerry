# Skill Development Guide

> Educational companion to `.context/rules/skill-standards.md`.
> Based on Anthropic's "Complete Guide to Building Skills for Claude" (January 2026) and Jerry's established skill conventions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Planning Your Skill](#planning-your-skill) | Use cases, success criteria, approach selection |
| [Progressive Disclosure](#progressive-disclosure) | Three-level loading system |
| [Writing Effective Descriptions](#writing-effective-descriptions) | The most important field |
| [Writing Instructions](#writing-instructions) | Clear, actionable, with error handling |
| [Skill Use Case Categories](#skill-use-case-categories) | Document/Asset, Workflow Automation, MCP Enhancement |
| [Workflow Patterns](#workflow-patterns) | 5 proven patterns with examples |
| [Testing Your Skill](#testing-your-skill) | Three rigor levels, iteration signals |
| [Troubleshooting](#troubleshooting) | Common issues and solutions |
| [Distribution](#distribution) | Hosting, installation, positioning |
| [Jerry Framework Conventions](#jerry-framework-conventions) | Jerry-specific structural patterns |
| [References](#references) | Source documents |

---

## Planning Your Skill

### Start with Use Cases

Before writing any code or instructions, define **2-3 concrete use cases**. Each use case should follow this template:

**Use Case Definition Template:**

```
Trigger: [What the user says or does]
Steps:
  1. [First action the skill takes]
  2. [Second action]
  3. [Third action]
  ...
Result: [What the user gets]
```

**Example -- Sprint Planning Skill:**

```
Use Case 1: Create a new sprint
  Trigger: "Start a new sprint" or "Create sprint for next two weeks"
  Steps:
    1. Check Linear for unfinished items from current sprint
    2. Pull top items from backlog based on team velocity
    3. Create sprint in Linear with date range
    4. Generate sprint planning document with goals and capacity
  Result: New sprint created in Linear with planning doc in project folder

Use Case 2: Sprint standup summary
  Trigger: "What's the sprint status?" or "Generate standup update"
  Steps:
    1. Pull current sprint data from Linear
    2. Identify completed, in-progress, and blocked items
    3. Calculate burndown progress against sprint goal
    4. Format summary with blockers highlighted
  Result: Formatted standup summary with burndown metrics
```

### Ask Yourself These Questions

Before writing a single line of the skill file, answer:

- **What does the user want to accomplish?** Think about the end goal, not the intermediate steps.
- **What workflows does this involve?** Map the full sequence from trigger to completion.
- **Which tools are needed?** Identify MCP servers, file operations, API calls.
- **What domain knowledge is required?** What does the skill need to "know" that Claude does not know by default?

### Problem-First vs Tool-First Framing

**Think like Home Depot, not like a drill manufacturer.**

People do not go to Home Depot because they want a drill. They go because they want a hole in the wall. Your skill should be framed around the problem it solves, not the tools it uses.

| Framing | Example |
|---------|---------|
| Tool-first (avoid) | "Calls the Linear API to create issues and update sprints" |
| Problem-first (prefer) | "Manages sprint planning so you can focus on building, not tracking" |

The tool-first description tells Claude what APIs to call. The problem-first description tells Claude *when* to activate and *why* the user cares.

### Define Success Criteria

Success criteria fall into two categories:

**Quantitative Criteria:**

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Trigger accuracy | 90% of relevant prompts activate the skill | Test with 20+ trigger phrases, count correct activations |
| Tool call efficiency | Minimum necessary calls per workflow | Count API/tool calls across 10 runs, compare to manual baseline |
| Error rate | 0 failed API calls in happy path | Run 10 end-to-end tests, log all failures |

**Qualitative Criteria:**

- Users do not need to redirect Claude after skill activation (it understood the intent correctly)
- Workflows complete without mid-stream user correction
- Output is consistent across sessions (same input produces structurally similar output)

> **Note:** These are aspirational targets -- rough benchmarks rather than precise thresholds. Use them to guide iteration, not as hard pass/fail gates.

---

## Progressive Disclosure

Skills use a three-level loading system that minimizes context consumption while ensuring Claude has the right information at the right time.

### Level 1: Frontmatter (Always Loaded)

The YAML frontmatter is **always loaded** into the system prompt. It must contain just enough information for Claude to decide **when** to use the skill.

```yaml
---
name: sprint-planner
description: >
  Manages sprint planning workflows including backlog grooming, capacity
  planning, and sprint creation. Use when user says "plan sprint",
  "start sprint", "sprint review", or "backlog grooming".
---
```

Level 1 is your skill's "elevator pitch." Keep it concise -- under 1024 characters for the description.

### Level 2: SKILL.md Body (Loaded When Relevant)

When Claude determines the skill is relevant, it loads the full SKILL.md body. This contains:

- Complete instructions for how to execute workflows
- Agent definitions and orchestration rules
- Error handling guidance
- Examples of expected input/output

This is where the bulk of your skill's intelligence lives.

### Level 3: Linked Files (Loaded on Demand)

Reference files that Claude loads only when it needs specific details:

- API documentation
- Template files
- Strategy templates
- Configuration schemas
- Domain-specific reference material

```markdown
## References
For rate limiting patterns, consult `references/api-patterns.md`.
For template syntax, see `.context/templates/sprint/`.
```

Claude will read these files only when executing a workflow that requires them.

### Design Principles

**Composability:** Your skill should work well alongside others. A sprint planning skill should not conflict with a project management skill -- they should complement each other. Avoid claiming broad, overlapping trigger phrases.

**Portability:** A well-designed skill works identically across Claude.ai, Claude Code, and the API. Avoid platform-specific assumptions in your instructions.

**The Kitchen Analogy:** Think of MCP servers as the **kitchen** (tools, appliances, ingredients) and skills as **recipes** (instructions for what to make and how). MCP provides the capabilities; skills provide the intelligence for how to use them effectively.

---

## Writing Effective Descriptions

The `description` field in your frontmatter is the single most important field in your skill. It determines whether Claude activates the skill at the right time, too often, or not at all.

### Structure

A good description follows this pattern:

```
[What it does] + [When to use it] + [Key capabilities]
```

Keep it under **1024 characters**.

### Good Examples

**1. Figma Design Handoff:**

```
Analyzes Figma design files and generates developer handoff documentation.
Use when user uploads .fig files, asks for "design specs", "component
documentation", or "design-to-code handoff".
```

Why this works: States the function (analyzes Figma files, generates handoff docs), lists trigger conditions (file type, specific phrases), and implies capabilities (analysis, documentation generation).

**2. Linear Project Management:**

```
Manages Linear project workflows including sprint planning, task creation,
and status tracking. Use when user mentions "sprint", "Linear tasks",
"project planning", or asks to "create tickets".
```

Why this works: Names the platform (Linear), lists workflows (sprint planning, task creation, status tracking), and provides concrete trigger phrases.

**3. PayFlow Customer Onboarding:**

```
End-to-end customer onboarding workflow for PayFlow. Handles account
creation, payment setup, and subscription management. Use when user says
"onboard new customer", "set up subscription", or "create PayFlow account".
```

Why this works: Specifies the domain (PayFlow onboarding), enumerates the workflow stages, and gives exact phrases users would say.

### Bad Examples

**1. Too vague:**

```
Helps with projects.
```

Problem: Claude has no idea when to activate this. Every conversation involves "projects" in some sense.

**2. Missing triggers:**

```
Creates sophisticated multi-page documentation systems.
```

Problem: Describes capability but provides zero activation signals. Claude cannot determine when the user wants this.

**3. Too technical, no user context:**

```
Implements the Project entity model with hierarchical relationships.
```

Problem: Describes internal implementation, not user-facing behavior. Users do not say "I need a hierarchical entity model."

---

## Writing Instructions

### Recommended Template Structure

```markdown
# Your Skill Name

## Instructions

### Step 1: [First Major Step]
[Specific, actionable instructions]

### Step 2: [Second Major Step]
[Specific, actionable instructions]

## Examples

### Example 1: [Common scenario]
**User says:** "..."
**Skill does:** ...
**Output:** ...

### Example 2: [Edge case]
**User says:** "..."
**Skill does:** ...
**Output:** ...

## Troubleshooting

### Error: [Common error message]
**Cause:** ...
**Fix:** ...
```

### Be Specific

Instructions must be concrete and unambiguous.

| Vague (avoid) | Specific (prefer) |
|----------------|-------------------|
| "Validate the data" | "Run `scripts/validate.py --input {filename}` and check exit code 0" |
| "Check the configuration" | "Read `config/settings.yaml` and verify `api_version` is >= 2.0" |
| "Update the database" | "Call the `update-record` MCP tool with `{id: record_id, status: 'active'}`" |

### Include Error Handling

Every instruction that can fail should have a recovery path:

```markdown
### Step 3: Fetch sprint data from Linear

Call `linear_get_sprint(team_id, sprint_id)`.

**If the sprint does not exist:** Inform the user and ask which sprint to use.
List available sprints with `linear_list_sprints(team_id)`.

**If the API returns a rate limit error:** Wait 30 seconds and retry once.
If it fails again, inform the user and suggest trying later.
```

### Reference Resources Clearly

When your skill depends on reference files, be explicit about what to find where:

```markdown
Consult `references/api-patterns.md` for:
- Rate limiting (section: Rate Limits)
- Pagination (section: Cursor-Based Pagination)
- Error codes (section: Error Code Reference)
```

### Progressive Disclosure in Instructions

Keep SKILL.md focused on the core workflow. Move detailed reference material to separate files:

```
skills/your-skill/
  SKILL.md              # Core instructions (Level 2)
  agents/               # Agent definitions
    agent-one.md
    agent-two.md
  references/           # Detailed reference material (Level 3)
    api-patterns.md
    domain-glossary.md
```

### Put Critical Instructions First

If there are instructions that must not be skipped, place them at the top of the file using prominent headings:

```markdown
## Important

- ALWAYS verify the user's project context before creating any resources
- NEVER delete existing sprint data without explicit user confirmation

## Critical

- All API calls MUST include the team_id parameter
- Sprint dates MUST be in ISO 8601 format
```

### Advanced: Bundle Deterministic Scripts

For validation steps where precision matters, bundle scripts rather than relying on Claude to interpret instructions:

```markdown
### Step 4: Validate output format

Run the bundled validation script:

    scripts/validate-sprint-output.py --input {output_file}

The script checks:
- Required fields are present
- Date ranges are valid
- Capacity does not exceed team size

**Rationale:** Code is deterministic; language interpretation is not. A validation
script produces the same result every time, while natural language instructions
may be interpreted differently across sessions.
```

### Addressing Model Laziness

Claude may sometimes skip steps or take shortcuts, particularly in long workflows. These phrases can help:

- "Take your time to do this thoroughly"
- "Quality is more important than speed"
- "Do not skip validation steps"

> **Note:** Adding these phrases to user prompts is more effective than embedding them in SKILL.md. Instructions in the skill file compete with many other system-level instructions, while user-prompt phrasing receives direct attention.

---

## Skill Use Case Categories

Skills fall into three broad categories, each with distinct design considerations.

### Category 1: Document and Asset Creation

Skills that produce documents, code, configurations, or other artifacts.

**Key ingredients:**

- **Embedded style guides** -- Include formatting rules, tone guidelines, and structural templates directly in the skill
- **Templates** -- Provide skeleton structures that Claude fills in
- **Quality checklists** -- Define what "done" looks like for each output type
- **Built-in capabilities** -- Leverage Claude's native abilities (writing, analysis, code generation) with domain-specific constraints

**Example:** A skill that generates API documentation from code, enforcing a specific template, including required sections (authentication, rate limits, error codes), and applying a house style guide.

### Category 2: Workflow Automation

Skills that orchestrate multi-step processes with validation gates.

**Key ingredients:**

- **Validation gates** -- Checkpoints between stages that must pass before proceeding
- **Templates** -- Standardized formats for intermediate and final outputs
- **Review suggestions** -- Prompts for human review at critical decision points
- **Refinement loops** -- Iterative improvement cycles with defined stop conditions

**Example:** A skill that manages code review workflows: fetch PR diff, run static analysis, generate review comments, request human approval, post comments to the PR.

### Category 3: MCP Enhancement

Skills that add intelligence on top of MCP server capabilities.

**Key ingredients:**

- **Sequential MCP calls** -- Orchestrate multiple MCP tool calls in the right order
- **Domain expertise** -- Know which MCP calls to make for a given user intent
- **User context** -- Carry forward context from previous interactions to inform MCP calls
- **Error handling** -- Graceful degradation when MCP tools fail or return unexpected results

**Example:** A skill that uses a database MCP server to generate weekly reports: query multiple tables, join results, calculate metrics, format into a report template -- all of which require knowing the schema and business logic that the MCP server alone does not provide.

---

## Workflow Patterns

Five proven patterns for structuring skill workflows. Choose the pattern that best matches your skill's complexity and requirements.

### Pattern 1: Sequential Orchestration

**When to use:** Multi-stage workflows where each stage depends on the previous stage's output.

```markdown
## Workflow

### Stage 1: Gather Requirements
- Read project configuration from `config/project.yaml`
- Extract current sprint goals
- **Validation:** Verify config file exists and contains required fields

### Stage 2: Analyze Current State
- Query Linear for current sprint metrics
- Calculate velocity from last 3 sprints
- **Validation:** Confirm API returned valid data for all queries

### Stage 3: Generate Plan
- Use velocity data to size next sprint
- Assign items based on team capacity
- **Validation:** Total story points <= team capacity * 0.85

### Stage 4: Create Artifacts
- Create sprint in Linear
- Generate planning document
- **Validation:** Sprint ID returned, document written to disk

### Rollback
If any stage fails after Stage 3:
1. Delete created sprint (if exists)
2. Log failure reason
3. Present partial results to user
```

**Key techniques:**
- Explicit ordering with numbered stages
- Dependencies stated clearly (each stage uses output from the previous)
- Validation checkpoint after every stage
- Rollback procedure for failure recovery

### Pattern 2: Multi-MCP Coordination

**When to use:** Workflows that span multiple MCP servers or external tools.

```markdown
## Workflow

### Phase 1: Data Collection (Linear MCP)
- Fetch sprint data: `linear_get_sprint(team_id, sprint_id)`
- Fetch team members: `linear_get_team(team_id)`
- Store results in `context.sprint_data` and `context.team`

### Phase 2: Analysis (Local)
- Calculate burndown from `context.sprint_data`
- Identify at-risk items (items with no progress in 3+ days)
- Generate recommendations

### Phase 3: Communication (Slack MCP)
- Post summary to `#engineering` channel
- DM individual blockers to assignees
- **Cross-phase validation:** Verify all mentioned usernames from Phase 1
  exist in Slack before sending DMs

### Error Handling (Centralized)
- Linear API failure: Retry once, then use cached data if available
- Slack API failure: Write output to local file as fallback
- Data mismatch: Log warning, continue with available data
```

**Key techniques:**
- Phase separation by MCP server / tool boundary
- Explicit data passing between phases (`context.sprint_data`)
- Cross-phase validation (verify Slack usernames from Linear data)
- Centralized error handling section

### Pattern 3: Iterative Refinement

**When to use:** Workflows where output quality improves through multiple passes.

```markdown
## Workflow

### Quality Criteria
- All required sections present (completeness)
- No internal contradictions (consistency)
- All claims backed by evidence (evidence quality)
- All action items have owners and deadlines (actionability)

### Iteration Loop
1. **Create:** Generate initial draft
2. **Validate:** Run `scripts/validate-report.py --input {draft}`
3. **Evaluate:** Score against quality criteria (target >= 0.92)
4. **Refine:** Address lowest-scoring dimension
5. **Repeat** from step 2

### Stop Conditions
- Score >= 0.92 on all dimensions -> ACCEPT
- 5 iterations completed without reaching threshold -> ESCALATE to user
- Validation script reports structural errors -> FIX before scoring
```

**Key techniques:**
- Explicit quality criteria defined upfront
- Validation scripts for deterministic checks
- Refinement loops with clear iteration protocol
- Stop conditions to prevent infinite loops

### Pattern 4: Context-Aware Selection

**When to use:** Workflows where different paths are taken based on input characteristics.

```markdown
## Workflow

### Decision Tree
1. Determine deliverable type:
   - Code change -> Path A (code review)
   - Architecture document -> Path B (design review)
   - Configuration change -> Path C (config validation)

2. Determine criticality:
   - C1 (routine): Self-review only
   - C2 (standard): Self-review + peer strategy
   - C3 (significant): Full strategy set
   - C4 (critical): Tournament mode

### Path A: Code Review
[Steps specific to code review...]

### Path B: Design Review
[Steps specific to design review...]

### Path C: Config Validation
[Steps specific to config validation...]

### Fallback
If deliverable type cannot be determined:
1. Ask the user to classify the deliverable
2. Explain the available paths
3. Proceed with user's selection

### Transparency
Always inform the user which path was selected and why:
"This is a C2 architecture document, so I'll apply design review
with Steelman + Devil's Advocate strategies."
```

**Key techniques:**
- Decision trees with clear branching criteria
- Fallback paths for ambiguous inputs
- Transparency about which path was chosen and why

### Pattern 5: Domain-Specific Intelligence

**When to use:** Workflows that require specialized domain knowledge beyond what Claude knows by default.

```markdown
## Workflow

### Domain Knowledge
This skill embeds expertise about:
- HIPAA compliance requirements for patient data
- HL7 FHIR resource types and validation rules
- Healthcare API rate limits and SLAs

### Compliance-First Approach
1. **Before any action:** Check if the requested operation involves PHI
   (Protected Health Information)
2. **If PHI involved:** Verify audit logging is enabled, verify user
   has appropriate role, log access intent
3. **Proceed with operation:** Execute the requested workflow
4. **After completion:** Generate compliance audit entry

### Audit Trail
Every skill invocation MUST produce:
- Timestamp of invocation
- User identity
- Resources accessed
- Actions taken
- Compliance checks performed (pass/fail)
```

**Key techniques:**
- Embedded domain expertise that Claude would not otherwise have
- Compliance-before-action ordering
- Mandatory audit trails for regulated domains

---

## Testing Your Skill

### Three Rigor Levels

| Level | Tool | Best For |
|-------|------|----------|
| Manual | Claude.ai | Rapid prototyping, initial trigger testing |
| Scripted | Claude Code | Systematic workflow validation, regression |
| Programmatic | API | Automated CI/CD, performance benchmarking |

> **Pro Tip:** Iterate on a single challenging task until Claude succeeds, then extract the winning approach into a skill. This is more effective than trying to design the perfect skill upfront.

### Triggering Tests

Test that your skill activates when it should and does not activate when it should not.

**Should trigger:**

```
"Plan the next sprint"                    -> Should activate sprint-planner
"Create sprint for next two weeks"        -> Should activate sprint-planner
"What's our sprint velocity?"             -> Should activate sprint-planner
"Groom the backlog for next sprint"       -> Should activate sprint-planner
```

**Should NOT trigger:**

```
"Write a Python script"                   -> Should NOT activate sprint-planner
"Review this pull request"                -> Should NOT activate sprint-planner
"What's the weather?"                     -> Should NOT activate sprint-planner
"Help me plan my vacation"                -> Should NOT activate sprint-planner
                                             (even though it contains "plan")
```

### Functional Tests

Use BDD-style Given/When/Then to define expected behavior:

```
Test: Sprint creation with valid data
  Given: Linear MCP is connected, team "engineering" exists with 5 members
  When: User says "Create a 2-week sprint starting Monday"
  Then:
    - Sprint created in Linear with correct date range
    - Planning document generated in project/sprints/
    - Document contains capacity section (5 members * 10 days * 0.85)
    - User informed of sprint ID and document location

Test: Sprint creation with no backlog
  Given: Linear MCP is connected, backlog is empty
  When: User says "Plan the next sprint"
  Then:
    - Skill detects empty backlog
    - Informs user: "No items in backlog. Add items before planning."
    - Does NOT create an empty sprint
```

### Performance Comparison

Measure the skill's impact by comparing with and without:

| Metric | Without Skill | With Skill | Improvement |
|--------|--------------|------------|-------------|
| Messages to complete task | 12 | 4 | 3x fewer |
| API calls | 15 (3 redundant) | 8 (0 redundant) | 47% fewer |
| Tokens consumed | ~8,000 | ~3,500 | 56% fewer |
| User corrections needed | 3 | 0 | Eliminated |

### Skill Creator Tool

> **Note:** The `skill-creator` tool referenced in Anthropic's guide is a Claude.ai feature, not a Jerry CLI tool. For Jerry skill development, use the canonical pattern (`.context/patterns/skill-development/skill-structure.md`) as your starting template and validate against `.context/rules/skill-standards.md`.

For Claude.ai users, the skill-creator tool supports:

1. **Generating** an initial skill from a natural language description
2. **Reviewing** an existing skill for common issues
3. **Iteratively improving** a skill based on test results

### Iteration Signals

After testing, use these signals to guide your next revision:

| Signal | Symptom | Fix |
|--------|---------|-----|
| Undertriggering | Skill does not activate for relevant prompts | Add more activation keywords to description; include file type triggers; add common phrasings |
| Overtriggering | Skill activates for unrelated prompts | Add negative triggers ("Do NOT activate for..."); be more specific about scope; narrow activation keywords |
| Execution issues | Skill activates but produces wrong output | Improve step-by-step instructions; add examples of expected output; include error handling for common failures |

### Debugging Technique

Ask Claude directly:

> "When would you use the [skill name] skill?"

Claude will quote the description back to you, showing exactly how it interprets the activation criteria. This reveals whether your description communicates what you intended.

---

## Troubleshooting

### Skill Will Not Upload

| Symptom | Cause | Fix |
|---------|-------|-----|
| Upload fails silently | File not named `SKILL.md` | Rename to exactly `SKILL.md` (case-sensitive) |
| Parse error on upload | Invalid YAML frontmatter | Validate frontmatter: must start/end with `---`, valid YAML between |
| Name rejected | Invalid `name` field | Use lowercase, hyphens only, no spaces: `my-skill-name` |

### Skill Does Not Trigger

| Symptom | Cause | Fix |
|---------|-------|-----|
| Never activates | Description too generic | Add specific trigger phrases: "Use when user says X, Y, Z" |
| Misses file-based triggers | No file type mentions | Add: "Use when user uploads .fig files" or "works with .yaml configs" |
| Works sometimes | Missing common phrasings | Test with 20+ variations of the trigger intent; add missing ones |

### Skill Triggers Too Often

| Symptom | Cause | Fix |
|---------|-------|-----|
| Activates for unrelated tasks | Overly broad keywords | Replace "manage" with "manage Linear sprints" |
| Conflicts with other skills | Overlapping descriptions | Add scope boundaries: "Only for Linear, not Jira or GitHub Issues" |
| Activates on partial matches | Common words in description | Use multi-word trigger phrases instead of single common words |

### Instructions Not Followed

| Symptom | Cause | Fix |
|---------|-------|-----|
| Steps skipped | Instructions too verbose | Shorten to essential steps; move details to reference files |
| Wrong order of operations | Buried ordering requirements | Move critical ordering to top of file under `## Important` |
| Inconsistent behavior | Ambiguous language | Replace "you might want to" with "ALWAYS do X before Y" |
| Shortcuts taken | Model laziness on long workflows | Add "Do not skip validation steps" and break into smaller stages |

### Large Context Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Performance degrades | SKILL.md too large | Optimize to under 5,000 words (~6,500 tokens — ~3.3% of 200K context per activation); move reference material to linked files |
| Other skills stop working | Too many skills loaded | Reduce enabled skills; use skill packs for logical grouping |
| Context window exhaustion | Linked files too large | Split large reference files; load only the section needed |

### MCP Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tool calls fail | MCP server not connected | Verify connection: check MCP server status in Claude settings |
| Authentication errors | Expired or invalid credentials | Refresh auth tokens; check API key configuration |
| Unexpected results | Tool name mismatch | Verify exact tool names match MCP server's registered names |
| Intermittent failures | Network or rate limiting | Add retry logic in instructions; test MCP tools independently |

---

## Distribution

> **Jerry Framework Note:** The following sections describe Anthropic's general skill distribution model (Claude.ai upload, API, GitHub hosting). Jerry skills are deployed via the repository filesystem — see [Context Distribution Architecture](#context-distribution-architecture) in Jerry Framework Conventions below. The general distribution guidance is included for completeness and for skills intended for community sharing outside Jerry.
>
> **H-27 Reminder:** The skill folder (`skills/your-skill-name/`) MUST NOT contain `README.md`. For GitHub hosting, the README belongs at the *hosting repository root*, not inside the skill folder. All skill documentation goes in `SKILL.md` or `references/`.

### Individual Installation

For personal use or small-team sharing:

1. **Download:** Get the skill folder (containing `SKILL.md` and any supporting files)
2. **Zip:** Compress the folder if distributing manually
3. **Upload:** In Claude.ai, go to Settings > Capabilities > Skills, upload the skill

### Organization Deployment

For workspace-wide deployment:

- **Admin deployment:** Organization admins can deploy skills across the workspace
- **Automatic updates:** When the admin updates the skill, all users receive the new version
- **Centralized management:** Single source of truth for skill definitions

### API Integration

For programmatic skill management:

- **Endpoint:** `/v1/skills` for CRUD operations on skills
- **Container parameter:** `container.skills` to attach skills to conversations
- **Prerequisite:** Code Execution Tool beta must be enabled

### GitHub Hosting

For open-source or community skills:

- Host in a **public repository**
- Include a clear README at the **repository root** (not inside the skill folder -- the skill folder should only contain `SKILL.md` and supporting files)
- Provide example usage showing trigger phrases and expected output
- Reference: [anthropics/skills](https://github.com/anthropics/skills) for community examples

### Positioning Your Skill

When describing your skill for distribution:

- **Focus on outcomes, not features.** "Save 2 hours per sprint planning session" beats "Integrates with Linear API and generates Markdown documents."
- **Show, do not tell.** Include before/after examples demonstrating the difference the skill makes.
- **Target the user's language.** Use the phrases your target audience actually says, not technical jargon.

---

## Jerry Framework Conventions

Jerry skills follow additional conventions beyond the Anthropic standard. These conventions ensure consistency across all Jerry skills and integration with the Jerry quality framework.

### Context Distribution Architecture

Jerry uses a two-layer architecture for context distribution:

- **`.context/`** — Claude-agnostic source of truth. Contains `rules/`, `guides/`, `patterns/`, `templates/`. Works with any AI coding assistant.
- **`.claude/`** — Claude Code-specific layer. Contains **symlinks** to `.context/` subdirectories, making them auto-loaded by Claude Code at session start.

```
.claude/
├── rules -> ../.context/rules      # Symlink — auto-loaded by Claude Code
├── patterns -> ../.context/patterns # Symlink — auto-loaded by Claude Code
├── settings.json
└── settings.local.json

.context/
├── rules/           # Source of truth — enforcement rules (HARD/MEDIUM/SOFT)
├── guides/          # Educational companions — NOT auto-loaded
├── patterns/        # Reusable patterns — auto-loaded via symlink
└── templates/       # File templates — loaded on demand
```

**Why this matters for skills:** When you create rules in `.context/rules/`, they are automatically available to Claude Code via the `.claude/rules/` symlink. You do NOT need to create files in both locations. Always author in `.context/` — the symlink handles Claude awareness.

> **Note:** `.context/guides/` is NOT symlinked to `.claude/`. Guides are loaded on demand (Level 3 progressive disclosure), not at session start. This is intentional — guides are educational companions, not enforcement rules.

### YAML Frontmatter Additions

Jerry skills extend the standard frontmatter with additional fields:

```yaml
---
name: your-skill-name
description: >
  [Standard Anthropic description with trigger phrases]
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "keyword one"
  - "keyword two"
  - "keyword three"
---
```

| Field | Purpose |
|-------|---------|
| `version` | Semantic version string (quoted) |
| `activation-keywords` | YAML list of trigger phrases (supplements description) |
| `allowed-tools` | Comma-separated list of tools the skill may use |

### SKILL.md Body Structure

Jerry SKILL.md files follow a consistent structure:

```markdown
# Skill Name

> **Version:** X.Y.Z
> **Framework:** Jerry [Domain] ([Abbreviation])
> **Constitutional Compliance:** Jerry Constitution v1.0

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What the skill does |
| [When to Use This Skill](#when-to-use-this-skill) | Activation conditions |
| [Available Agents](#available-agents) | Agent registry |
| [Quick Reference](#quick-reference) | Common workflows |
| [References](#references) | Source documents |

> **Required by H-23/NAV-001.** SKILL.md is Claude-consumed markdown (always >30
> lines). Navigation table with anchor links (H-24) enables Claude to understand
> document structure and navigate to relevant sections efficiently.

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose], [When to Use], [Quick Reference] |
| **L1 (Engineer)** | Developers invoking agents | [Invoking], [Agents], [Dependencies] |
| **L2 (Architect)** | Workflow designers | [P-003 Compliance], [Integration], [Constitutional] |

---

## Purpose
[What the skill does and why it exists]

## When to Use This Skill
[Activation conditions and anti-conditions]

## Available Agents
[Table of agents with roles and output locations]

## P-003 Compliance
[How the skill respects the max-one-level subagent constraint]

## Invoking an Agent
[Three invocation options: slash command, direct, programmatic]

### Option 1: Slash Command
### Option 2: Direct Agent Reference
### Option 3: Programmatic

## [Domain-Specific Content Sections]
[The core instructional content of the skill]

## Integration Points
[How this skill connects with other skills and framework components]

## Constitutional Compliance
[Which HARD rules apply and how the skill enforces them]

## Quick Reference
[Condensed table of agents, commands, and key information]

## References
[Source documents, related skills, external links]

---
*[Skill Name] Skill v{version} | Jerry Framework*
```

### File References

All file references in Jerry skills MUST use full repo-relative paths:

```markdown
# Correct
See `.context/rules/quality-enforcement.md` for threshold definitions.
Load templates from `.context/templates/adversarial/s-014-llm-as-judge.md`.

# Incorrect
See `../rules/quality-enforcement.md` for threshold definitions.
See `quality-enforcement.md` for threshold definitions.
```

### Agent Definitions

Agents are defined in separate files within the skill's `agents/` directory:

```
skills/your-skill/
  SKILL.md
  agents/
    agent-one.md
    agent-two.md
    agent-three.md
```

Each agent file contains:
- Agent role and responsibilities
- Input/output specifications
- Step-by-step instructions
- Integration with other agents

### Registration

New skills must be registered in three locations:

| File | What to Add |
|------|-------------|
| `CLAUDE.md` | Entry in the Skills quick-reference table |
| `AGENTS.md` | Entries for each agent the skill defines |
| `.context/rules/mandatory-skill-usage.md` | Trigger keywords and invocation rules (if proactive invocation is required) |

> **Important:** Modifying `.context/rules/mandatory-skill-usage.md` triggers AE-002 (auto-escalation to C3 minimum). Plan accordingly and ensure appropriate review.

---

## References

### Source Documents

- Anthropic's "Complete Guide to Building Skills for Claude" (PDF, January 2026)
- `docs/knowledge/anthropic-skill-development-guide.pdf`

### Rules and Standards

- `.context/rules/skill-standards.md` -- Enforcement rules for skill development

### Patterns and Templates

- `.context/patterns/skill-development/` -- Reusable patterns for common skill structures

### Reference Implementations

- `skills/adversary/SKILL.md` -- Reference implementation (adversarial quality reviews, tournament scoring, strategy templates)
- `skills/problem-solving/SKILL.md` -- Reference implementation (multi-agent problem solving with research, analysis, synthesis)

### Community and External

- [anthropics/skills](https://github.com/anthropics/skills) -- Community skill repository
- [Introducing Agent Skills](https://www.anthropic.com/research/agent-skills) -- Anthropic blog post
- [Building Skills for Claude Code](https://www.anthropic.com/research/building-skills-claude-code) -- Anthropic blog post

---

*Guide Version: 1.0.0*
*Corresponds to: `.context/rules/skill-standards.md` v1.1.0*
*Source: Anthropic Skill Guide (Jan 2026) + Jerry Framework v0.2.3*
*Created: 2026-02-19*

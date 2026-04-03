# Jerry Skill Pattern Analysis

> **PS ID:** proj-021
> **Step:** 5 of orchestration workflow use-case-skills-20260308-001
> **Analysis Type:** Pattern extraction for new skill development
> **Topic:** Canonical patterns for /use-case, /test-spec, and /contract-design skills
> **Agent:** ps-analyst v2.3.0
> **Date:** 2026-03-08

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | 3-5 key patterns for non-technical readers |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed findings by focus area with file references |
| [L2: Strategic Implications](#l2-strategic-implications) | Checklist and template structure for new skills |
| [Evidence Summary](#evidence-summary) | All evidence cited |

---

## L0: Executive Summary

The Jerry Framework has a highly consistent, well-enforced pattern for building skills and agents. Five patterns are non-negotiable and must be replicated exactly in the new skills:

**Pattern 1: Dual-file agent architecture.** Every agent is defined by two files: a `.md` file (the Claude Code runtime config and system prompt) and a companion `.governance.yaml` file (machine-readable metadata for CI validation). These are not interchangeable -- the `.md` frontmatter contains only the 12 official Claude Code fields; everything else lives in `.governance.yaml`.

**Pattern 2: Constitutional triplet in every agent.** Every agent, without exception, declares P-003 (no recursive subagents), P-020 (user authority), and P-022 (no deception) in both its `.md` forbidden actions and its `.governance.yaml` `constitution.principles_applied` list. This is validated by CI. Missing any of these will cause CI failure.

**Pattern 3: L0/L1/L2 output levels in all agents and SKILL.md.** Every deliverable -- from agents, from SKILL.md sections, from output templates -- is organized around three audience levels: L0 (ELI5 / executive), L1 (software engineer / technical), L2 (principal architect / strategic). This is a framework invariant that cuts across every skill examined.

**Pattern 4: SKILL.md has a canonical section order.** Every SKILL.md follows the same structure: frontmatter (name, version, allowed-tools, activation-keywords), Document Audience triple-lens table, Purpose, When to Use (including NEVER invoke conditions), Available Agents table, Invoking an Agent (3 options), Orchestration Flow, State Passing Between Agents, Mandatory Persistence, Adversarial Quality Mode, Constitutional Compliance table, Quick Reference, Agent Details, Routing Disambiguation table.

**Pattern 5: Routing disambiguation table with consequences.** Every SKILL.md ends with a Routing Disambiguation table listing conditions under which a different skill should be used, what that skill is, and -- critically -- the exact consequence of misrouting to this skill instead. This is what prevents AP-01 (Keyword Tunnel) and AP-02 (Bag of Triggers) anti-patterns.

---

## L1: Technical Analysis

### Focus Area 1: SKILL.md Structure Patterns

**Evidence from four SKILL.md files examined:**
- `skills/problem-solving/SKILL.md` (version 2.2.0)
- `skills/orchestration/SKILL.md` (version 2.2.0)
- `skills/adversary/SKILL.md` (version 1.0.0)
- `skills/eng-team/SKILL.md` (version 1.0.0)

#### 1.1 YAML Frontmatter (Official Claude Code Fields Only)

All four SKILL.md files use only the official Claude Code frontmatter fields. The pattern is:

```yaml
---
name: {skill-name}          # kebab-case, matches folder name
description: {description}  # WHAT+WHEN+triggers, under 1024 chars
version: "{semver}"          # Quoted string e.g. "2.2.0"
allowed-tools: {list}        # Space-separated or comma-separated
activation-keywords:         # List of strings triggering this skill
  - "keyword-1"
  - "keyword-2"
---
```

Note: `eng-team/SKILL.md` also uses an `agents:` list field in frontmatter, which is a Claude Code official field for preloading agent files.

#### 1.2 Section Ordering (Canonical)

From cross-referencing all four SKILL.md files, the canonical section order is:

1. **Document Sections navigation table** (H-23 compliance) -- `eng-team` uses this explicitly; `problem-solving` and `orchestration` use Document Audience Triple-Lens instead
2. **Document Audience (Triple-Lens)** -- `| Level | Audience | Sections to Focus On |` table
3. **Purpose** -- What the skill does, Key Capabilities bullet list
4. **When to Use This Skill** -- Activation triggers, NEVER conditions with consequence statement
5. **Available Agents** table -- `| Agent | Role | Output Location |`
6. **Invoking an Agent** -- Three options: Natural Language, Explicit Agent Request, Task Tool Invocation
7. **Orchestration Flow** -- Sequential/parallel workflow with ASCII art
8. **State Passing Between Agents** table -- `| Agent | Output Key | Provides |`
9. **Mandatory Persistence (P-002)** -- Output structure tree
10. **Adversarial Quality Mode** -- SSOT reference, criticality-based activation
11. **Constitutional Compliance** table -- `| Principle | Requirement | Consequence of Violation |`
12. **Quick Reference** -- Common Workflows + Agent Selection Hints tables
13. **Agent Details** -- Bulleted list of agent file paths
14. **Routing Disambiguation** table -- `| Condition | Use Instead | Consequence of Misrouting |`
15. **References** (some skills) -- ADRs, standards, external links
16. **Footer** -- `*Skill Version: X.Y.Z*`, `*Constitutional Compliance: Jerry Constitution v1.0*`

#### 1.3 NEVER Conditions Pattern

The "When to Use This Skill" section uses a specific NEVER pattern for exclusion conditions:

```
NEVER invoke this skill when:
- {Task type} -- Consequence: {Exact consequence in terms of what happens to context/artifacts/quality}
```

Example from `orchestration/SKILL.md`:
```
NEVER invoke this skill when:
- Task requires a single agent only -- Consequence: Orchestration overhead (barrier sync, quality gates, ORCHESTRATION.yaml state tracking) applied to single-step task wastes significant context budget on unnecessary coordination infrastructure
```

The consequence is always described in terms of **what actually goes wrong** (context budget waste, wrong artifact type produced, methodology mismatch), not just "use X instead."

#### 1.4 Constitutional Compliance Table Pattern

All four SKILL.md files use an identical table format:

```markdown
| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user intent -- ask before destructive ops | Unauthorized action; trust erosion |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; quality assessment invalidated |
```

Minimum 3 rows (the constitutional triplet). Most skills add domain-specific principles (P-001, P-002, P-004, P-011, etc.).

#### 1.5 Routing Disambiguation Table Pattern

```markdown
| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
| {Task type that belongs elsewhere} | `/{skill-name}` | {Specific description of what goes wrong if misrouted here} |
```

The consequence column is always specific -- it names the missing methodology, the incorrect artifact type, or the context budget impact. The adversary skill's routing disambiguation table is the most complete example with 7 rows covering all adjacent skills.

---

### Focus Area 2: Agent Definition Patterns

**Evidence from agent files examined:**
- `skills/problem-solving/agents/ps-analyst.md` + `.governance.yaml`
- `skills/eng-team/agents/eng-architect.md` + `.governance.yaml`
- `skills/diataxis/agents/diataxis-classifier.md` + `.governance.yaml`

#### 2.1 Dual-File Architecture (H-34)

Every agent consists of exactly two files:

**File A: `{agent-name}.md`** (Claude Code runtime + system prompt)

Frontmatter contains ONLY official Claude Code fields:
```yaml
---
name: {agent-name}           # kebab-case
description: {description}   # Routing + trigger description
model: sonnet|opus|haiku     # Model selection
tools: {comma-separated}     # Allowed tools (NO Task for worker agents)
mcpServers:                   # Optional
  context7: true
---
```

Body is the system prompt organized with XML-tagged sections:
- `<agent>` (outer wrapper)
- `<identity>` -- role, expertise, cognitive mode, key distinctions
- `<persona>` -- tone, communication style, audience adaptation (L0/L1/L2)
- `<capabilities>` -- allowed tools table, tool examples, forbidden actions (NPT-009 format)
- `<guardrails>` -- input validation, output filtering, fallback behavior
- `<constitutional_compliance>` -- compliance table + self-critique checklist
- `<invocation_protocol>` -- context fields required, mandatory persistence steps
- `<output_levels>` -- L0/L1/L2 structure definitions
- `<state_management>` -- output key, state schema YAML
- `<session_context_validation>` -- on_receive/on_send validation

Note: `eng-architect.md` uses heading-based sections (`## Identity`, `## Methodology`, `## Workflow Integration`) rather than XML tags. Both formats exist in the codebase. The XML-tag format (used by ps-analyst, diataxis-classifier) is the pattern specified in `agent-development-standards.md` Section "Markdown Body Sections".

**File B: `{agent-name}.governance.yaml`** (machine-readable metadata)

```yaml
# Governance metadata for {agent-name}
# Validated by: docs/schemas/agent-governance-v1.schema.json
# Runtime config: {agent-name}.md

version: {semver}          # REQUIRED
tool_tier: T1|T2|T3|T4|T5  # REQUIRED
identity:                   # REQUIRED
  role: {role title}
  expertise:                # min 2 entries
    - {specific competency 1}
    - {specific competency 2}
  cognitive_mode: divergent|convergent|integrative|systematic|forensic
persona:
  tone: {free-form string}
  communication_style: {free-form string}
  audience_level: adaptive|expert|intermediate|beginner
guardrails:
  input_validation:
    - {field}: {pattern or description}
  output_filtering:
    - {constraint}
  fallback_behavior: warn_and_retry|escalate_to_user|persist_and_halt
output:
  required: true
  location: {path pattern}
  levels: [L0, L1, L2]   # or [L1] for internal agents
constitution:
  reference: docs/governance/JERRY_CONSTITUTION.md
  principles_applied:        # min 3, MUST include P-003, P-020, P-022
    - "P-003: No Recursive Subagents (Hard)"
    - "P-020: User Authority (Hard)"
    - "P-022: No Deception (Hard)"
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_l0_l1_l2_present
capabilities:
  forbidden_actions:         # min 3 entries, NPT-009 format recommended
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Return transient output only (P-002)"
```

#### 2.2 Model Selection Pattern

Based on the three agents examined plus the model selection guidance in `agent-development-standards.md`:

| Cognitive Mode | Model | Rationale |
|----------------|-------|-----------|
| convergent (analyst, classifier) | sonnet | Balanced analysis |
| divergent (researcher) | opus | Complex exploration |
| systematic (validator, auditor) | haiku | Procedural, fast |
| forensic (investigator) | opus | Deep reasoning |
| convergent + architecture (eng-architect) | opus | Complex synthesis |

#### 2.3 Tool Tier Selection Pattern

Based on observed tier assignments:

| Tier | Assigned To | Tools Added vs. Previous |
|------|-------------|--------------------------|
| T1 | Read-only agents (wt-auditor, diataxis-classifier) | Read, Glob, Grep |
| T2 | Analysis/write agents (ps-analyst, ps-critic) | + Write, Edit, Bash |
| T3 | External research agents (ps-researcher, eng-architect) | + WebSearch, WebFetch, Context7 MCP |
| T4 | Persistent state agents (orch-planner, nse-requirements) | + Memory-Keeper MCP |
| T5 | Orchestrators only | + Task |

**Key rule:** Worker agents MUST NOT include Task tool (H-35). The ps-analyst.md `tools:` field explicitly lists `Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch` -- no Task.

#### 2.4 Invocation Protocol Pattern

Every agent `.md` includes an invocation protocol section specifying:
1. Required context fields (PS CONTEXT, ENG CONTEXT, etc.)
2. Mandatory persistence steps (file creation path + link-artifact command)
3. Post-completion verification commands

The pattern for context fields:
```markdown
## {SKILL_PREFIX} CONTEXT (REQUIRED)
- **{Skill-Prefix} ID:** {id}
- **Entry ID:** {entry_id}
- **{Domain-Specific Field}:** {value}
- **Topic:** {topic}
```

---

### Focus Area 3: Routing Integration Patterns

**Evidence from:** `mandatory-skill-usage.md` (Phase 1 enhanced 5-column format)

#### 3.1 Five-Column Trigger Map Format

The canonical format from `mandatory-skill-usage.md`:

```
| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
```

Key observations from existing entries:

1. **Keyword selection:** Keywords are chosen to match the DOMAIN and METHOD, not just the noun. Examples:
   - `/problem-solving` uses: "research, analyze, investigate, explore, root cause, why, debug..."
   - `/nasa-se` uses: "requirements, specification, V&V, technical review, risk, design..."
   - `/eng-team` uses: "secure development, secure design, threat model, security architecture, STRIDE..."

2. **Negative keywords are critical:** The negative keyword column suppresses false-positive routing. Example: `/problem-solving` lists "adversarial, tournament, transcript, VTT, SRT, voice, persona" as negatives to prevent routing to the wrong skill when those words appear alongside research terms.

3. **Priority assignment:** Lower numbers = higher priority.
   - 1 = `/orchestration` (coordinates others, routes first)
   - 2 = `/transcript` (narrow, specific)
   - 3-4 = `/saucer-boy` variants (conversational)
   - 5 = `/nasa-se`
   - 6 = `/problem-solving`
   - 7 = `/adversary`
   - 8-12 = More specific specialist skills

4. **Compound triggers for disambiguation:** Phrase matches prevent broad keywords from triggering the wrong skill. Example: `/diataxis` requires phrase matches like "create documentation" or "write documentation" rather than just "documentation".

5. **Collision analysis required:** Before assigning keywords to new skills, MUST check overlap with existing entries and add corresponding negative keywords. The current map has many overlapping terms handled through priority ordering and negative keywords.

#### 3.2 Keyword Collision Risk for New Skills

For the three new skills, the most likely collision zones are:

| New Skill | Likely Collision With | Risk Terms |
|-----------|----------------------|------------|
| `/use-case` | `/nasa-se` | "requirements, specification, use case, scenario" |
| `/use-case` | `/problem-solving` | "analyze, investigate, scenario, behavior" |
| `/test-spec` | `/eng-team` | "test, QA, security testing, SAST" |
| `/test-spec` | `/nasa-se` | "V&V, verification, test plan, acceptance criteria" |
| `/contract-design` | `/nasa-se` | "interface, specification, design" |
| `/contract-design` | `/eng-team` | "API, security, OpenAPI, contract" |

These collisions MUST be resolved with negative keywords and compound triggers (UC-020 compliance).

---

### Focus Area 4: Inter-Skill Dependency Patterns

**Evidence from:** `skills/user-experience/SKILL.md`, `skills/ux-jtbd/SKILL.md`, `skills/ux-heart-metrics/SKILL.md`, `skills/red-team/SKILL.md`

#### 4.1 How Inter-Skill Data Contracts Are Defined

The `user-experience` skill family (comprising 10+ sub-skills) provides the most developed example of inter-skill data contracts in the codebase. The pattern is:

**Pattern: Handoff Data Section in Output Description**

Each sub-skill's output section contains a "Handoff Data" row:
```markdown
| **Handoff Data** | L1 | Structured data for downstream sub-skills: {field1}, {field2}, {field3} (for {consumer-skill} consumption) |
```

**Pattern: Downstream Handoff Contracts**

JTBD skill example from `skills/ux-jtbd/SKILL.md`:
```markdown
### Downstream Handoff Contracts
| Downstream Sub-skill | Data Consumed | Format |
```

**Pattern: Cross-Skill Integration via Named References**

Skills reference each other by their slash-command name:
- `| /problem-solving (ps-researcher) | Market research findings | Supplements JTBD competitive job analysis |`
- `| /eng-team (cross-skill) | Accessibility requirements for security integration |`

**Pattern: Orchestrator-Managed Handoffs**

The `ux-orchestrator` is explicitly named as the handoff manager for the UX sub-skill family. Handoffs are validated against `docs/schemas/handoff-v2.schema.json`.

**Pattern: Red-Team to Eng-Team Integration**

`eng-architect.md` explicitly references `/red-team` as a source of threat intelligence:
> "Consume threat intelligence from /red-team cross-skill integration to inform defensive architecture"

This is documented in the `eng-architect.governance.yaml` as an expertise item.

#### 4.2 Output Compatibility Pattern (UC-019: AST-parseable)

For outputs to be AST-parseable by the `/ast` skill, the pattern observed is:

1. **YAML frontmatter in blockquote format** -- worktracker entities use this
2. **Consistent heading structure** -- L0/L1/L2 at `###` level, main sections at `##`
3. **Navigation table** at the top per H-23
4. **Known frontmatter fields** with consistent types

The USE-CASE template at `.context/templates/requirements/USE-CASE.template.md` shows the full frontmatter schema for use case documents, which the `/use-case` skill's agents will need to produce. Key frontmatter fields: `id`, `title`, `work_type`, `version`, `status`, `level`, `scope`, `domain`, `primary_actor`, `supporting_actors`, `priority`.

---

### Focus Area 5: Template and Schema Patterns

**Evidence from:** `Glob` results, `docs/schemas/` directory, `.context/templates/`

#### 5.1 Template Inventory

| Template | Location | Relevant To |
|----------|----------|-------------|
| USE-CASE.template.md | `.context/templates/requirements/` | `/use-case` skill directly |
| TDD.template.md | `.context/templates/design/` | `/test-spec` skill |
| PLAYBOOK.template.md | `.context/templates/design/` | All new skills |
| s-014-llm-as-judge.md | `.context/templates/adversarial/` | Quality scoring |
| ORCHESTRATION.template.yaml | `skills/orchestration/templates/` | Workflow state |

#### 5.2 Schema Inventory

| Schema | Location | Purpose |
|--------|----------|---------|
| `agent-governance-v1.schema.json` | `docs/schemas/` | Validates `.governance.yaml` files -- all new agents MUST validate against this |
| `claude-code-frontmatter-v1.schema.json` | `docs/schemas/` | Validates agent `.md` frontmatter |
| `claude-code-skill-frontmatter-v1.schema.json` | `docs/schemas/` | Validates SKILL.md frontmatter |
| `session_context.json` | `docs/schemas/` | Handoff context schema |
| `agent-definition-v1.schema.json` | `docs/schemas/` | Deprecated -- reference only |

#### 5.3 Required Schema Fields (from `agent-governance-v1.schema.json`)

The governance schema requires exactly three fields at the top level: `version` (semver string), `tool_tier` (enum T1-T5), and `identity` object (with `role`, `expertise` min-2-array, and `cognitive_mode` enum). Everything else is optional but strongly recommended.

The `guardrails` sub-object requires `fallback_behavior`. The `capabilities.forbidden_actions` array requires minItems=3.

---

### Focus Area 6: Constitutional Compliance Patterns

**Evidence from:** All four SKILL.md files + three agent `.md` files + three `.governance.yaml` files

#### 6.1 Constitutional Triplet Enforcement

Every agent and every SKILL.md declares P-003, P-020, and P-022. This appears in three places:
1. `.md` `<capabilities>` / `<constitutional_compliance>` sections
2. `.governance.yaml` `constitution.principles_applied` list
3. `.governance.yaml` `capabilities.forbidden_actions` list

#### 6.2 Forbidden Actions NPT-009 Format

The recommended format from `agent-development-standards.md` (NPT-009-complete):
```
{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}
```

Example from `ps-analyst.md`:
```
P-003 VIOLATION: DO NOT spawn subagents that spawn further subagents. Consequence: unbounded recursion exhausts the context window and violates the single-level nesting constraint (H-01). Instead: return results to the orchestrator for coordination.
```

Some agents use the simpler NPT-014 format (bare prohibition):
```
Spawn recursive subagents (P-003)
```

Both are valid. NPT-009-complete is preferred for new agent definitions per ADR-002.

#### 6.3 Self-Critique Checklist Pattern

The `ps-analyst.md` `<constitutional_compliance>` section includes a self-critique checklist that agents apply before every output:

```markdown
**Self-Critique Checklist (Before Response):**
- [ ] P-001: Are all conclusions evidence-based?
- [ ] P-002: Is analysis output persisted to file?
- [ ] P-004: Are methods (5 Whys, FMEA, etc.) documented?
- [ ] P-011: Are recommendations justified by evidence?
- [ ] P-022: Are assumptions and limitations explicit?
```

New agents should include domain-specific self-critique checklists.

#### 6.4 Adversarial Quality Integration Pattern

Every SKILL.md contains an "Adversarial Quality Mode" section that:
1. References the SSOT: `.context/rules/quality-enforcement.md`
2. Uses the phrase "NEVER hardcode values; always reference the SSOT"
3. Provides a criticality-based activation table (C1-C4)
4. References H-13 (>= 0.92 threshold), H-14 (3 min iterations), H-15 (self-review)

---

## L2: Strategic Implications

### Checklist for New Skill Development

This checklist operationalizes all patterns observed. Apply to each of `/use-case`, `/test-spec`, and `/contract-design`.

#### A. SKILL.md Checklist

```markdown
SKILL.md Structure Compliance:
[ ] Frontmatter uses only official Claude Code fields (name, version, allowed-tools, activation-keywords)
[ ] version field is quoted string (e.g., "1.0.0")
[ ] Document navigation table present at top (H-23)
[ ] Document Audience Triple-Lens table present
[ ] Purpose section with Key Capabilities bullet list
[ ] "When to Use" section with NEVER conditions including consequences
[ ] Available Agents table (Agent | Role | Output Location)
[ ] Three invocation options (Natural Language, Explicit, Task Tool)
[ ] Orchestration Flow section with workflow diagram
[ ] State Passing Between Agents table (Agent | Output Key | Provides)
[ ] Mandatory Persistence (P-002) section with output directory tree
[ ] Adversarial Quality Mode section referencing SSOT
[ ] Constitutional Compliance table (Principle | Requirement | Consequence)
[ ] Quick Reference with Common Workflows + Agent Selection Hints
[ ] Agent Details with file paths
[ ] Routing Disambiguation table (Condition | Use Instead | Consequence)
[ ] Footer with version, constitutional compliance, dates
```

#### B. Agent .md File Checklist

```markdown
Agent .md Compliance:
[ ] Frontmatter contains ONLY official Claude Code fields
[ ] model field is sonnet/opus/haiku (justified by cognitive mode)
[ ] tools field does NOT include Task (worker agent requirement H-35)
[ ] Body organized with XML-tagged sections: <agent>, <identity>, <persona>, <capabilities>, <guardrails>, <constitutional_compliance>, <invocation_protocol>, <output_levels>, <state_management>, <session_context_validation>
[ ] <identity> declares: role, expertise (>= 2 items), cognitive mode, key distinctions
[ ] <persona> declares: tone, communication style, L0/L1/L2 audience adaptation
[ ] <capabilities> includes tool table with purpose + usage pattern
[ ] <capabilities> includes forbidden actions in NPT-009 format
[ ] P-003, P-020, P-022 appear in forbidden actions
[ ] <guardrails> includes input_validation, output_filtering, fallback_behavior
[ ] <constitutional_compliance> includes compliance table + self-critique checklist
[ ] <invocation_protocol> includes context fields, file creation path, link-artifact command
[ ] <output_levels> defines L0/L1/L2 structure
[ ] <state_management> includes output_key and state schema YAML
[ ] Footer with version, last updated, constitutional compliance
```

#### C. Agent .governance.yaml Checklist

```markdown
Governance YAML Compliance (validates against agent-governance-v1.schema.json):
[ ] version field present (semver, e.g., "1.0.0")
[ ] tool_tier field present (T1-T5)
[ ] identity.role field present
[ ] identity.expertise array with >= 2 specific items
[ ] identity.cognitive_mode present (enum value)
[ ] persona.tone present
[ ] persona.communication_style present
[ ] persona.audience_level present
[ ] guardrails.input_validation present (>= 1 rule)
[ ] guardrails.output_filtering present (>= 3 items)
[ ] guardrails.fallback_behavior present
[ ] output.required: true
[ ] output.location present
[ ] output.levels includes appropriate levels
[ ] constitution.principles_applied list with >= 3 items
[ ] constitution.principles_applied includes P-003, P-020, P-022
[ ] validation.post_completion_checks present
[ ] capabilities.forbidden_actions array with >= 3 items
[ ] capabilities.forbidden_actions references P-003, P-020, P-022
```

#### D. Trigger Map Registration Checklist

```markdown
Routing Registration (mandatory-skill-usage.md):
[ ] Positive keywords selected (minimum 3, domain-specific, not already claimed)
[ ] Negative keywords added for collision zones identified above
[ ] Priority number assigned (suggest 12+ for new specialist skills to avoid collision)
[ ] Compound triggers added for any broad terms that could match other skills
[ ] H-22 HARD rule updated with new skill invocation mandate
[ ] Collision analysis performed against all existing trigger map entries
[ ] New negative keywords added to existing adjacent skills if required
[ ] Disambiguation note added if "red team" style keyword overlap exists
```

#### E. SKILL.md Routing Disambiguation Coverage

The following adjacent skills MUST appear in the routing disambiguation tables:

For `/use-case`:
- `/nasa-se` (formal requirements engineering and V&V traceability)
- `/problem-solving` (general research and analysis)
- `/eng-team` (security-focused specification)
- `/worktracker` (entity management, not specification)

For `/test-spec`:
- `/nasa-se` (V&V plans, formal verification)
- `/eng-team` (security testing methodology)
- `/adversary` (adversarial quality assessment, not test planning)
- `/problem-solving` (ps-validator for constraint checking)

For `/contract-design`:
- `/nasa-se` (interface specifications in formal SE context)
- `/eng-team` (security-first API design)
- `/problem-solving` (ps-architect for general architecture decisions)
- `/orchestration` (multi-agent coordination, not API contracts)

### Specific Template for New Skill SKILL.md

```markdown
---
name: {use-case|test-spec|contract-design}
description: {WHAT in 1 clause}. {WHEN to invoke with context triggers}. {Key methodology names}.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
activation-keywords:
  - "keyword-1"
  - "keyword-2"
  - ... (minimum 5-8 domain-specific keywords)
---

# {Skill-Name} Skill

> **Version:** 1.0.0
> **Framework:** Jerry {Skill-Name}
> **Constitutional Compliance:** Jerry Constitution v1.0

## Document Sections

| Section | Purpose |
... (H-23 navigation table)

## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose], [When to Use], [Routing Disambiguation], [Quick Reference] |
| **L1 (Engineer)** | Developers invoking agents | [Invoking an Agent], [Agent Details], [Adversarial Quality Mode] |
| **L2 (Architect)** | Workflow designers | [Orchestration Flow], [State Passing], [Constitutional Compliance] |

## Purpose

{1-2 paragraphs on what the skill provides}

### Key Capabilities
- {capability-1}
- {capability-2}
...

## When to Use This Skill

Activate when:
- {trigger-1}
- {trigger-2}
...

NEVER invoke this skill when:
- {exclusion-1} -- Consequence: {specific consequence}
- {exclusion-2} -- Consequence: {specific consequence}

## Available Agents

| Agent | Role | Output Location |
|-------|------|-----------------|
...
All agents produce output at three levels:
- **L0 (Executive Summary)**
- **L1 (Technical Detail)**
- **L2 (Strategic Implications)**

## Invoking an Agent

### Option 1: Natural Language Request
...

### Option 2: Explicit Agent Request
...

### Option 3: Task Tool Invocation
...

## Orchestration Flow

{ASCII workflow diagram}

## State Passing Between Agents

| Agent | Output Key | Provides |
...

## Mandatory Persistence (P-002)

{Output directory tree}

## Adversarial Quality Mode

> **SSOT Reference:** `.context/rules/quality-enforcement.md` -- all thresholds, strategy IDs, criticality levels defined there. NEVER hardcode values; always reference the SSOT.

### Criticality-Based Activation

| Level | {Skill-Name} Context | Required Strategies | Typical Scenario |
...

## Constitutional Compliance

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user intent -- ask before destructive ops | Unauthorized action; trust erosion |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present findings without evidence | Unreliable outputs |
| P-002 | NEVER leave outputs in transient context only | Context rot vulnerability |

## Quick Reference

### Common Workflows
| Need | Agent | Command Example |
...

### Agent Selection Hints
| Keywords | Likely Agent |
...

## Agent Details
- `skills/{skill-name}/agents/{agent-name}.md`
...

## Routing Disambiguation

> When this skill is the wrong choice and what happens if misrouted.

| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
...

---
*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: {date}*
```

### Inter-Skill Data Contract Pattern for New Skills

The three new skills form a natural pipeline:
1. `/use-case` produces use case specifications (UC-NNN artifacts)
2. `/test-spec` consumes use case specifications to generate test specifications
3. `/contract-design` consumes use case specifications to generate interface contracts

This pipeline should be documented in each skill's "State Passing" and "Downstream Handoff Contracts" sections, referencing the handoff schema at `docs/schemas/handoff-v2.schema.json` (or the specification in `agent-development-standards.md` if the file does not yet exist).

The use case frontmatter schema from `.context/templates/requirements/USE-CASE.template.md` defines the canonical data model that all three skills should treat as their shared data contract foundation.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | File | `skills/problem-solving/SKILL.md` | SKILL.md section order, constitutional compliance table, routing disambiguation table, adversarial quality mode |
| E-002 | File | `skills/orchestration/SKILL.md` | NEVER conditions pattern, state schema, P-003 compliance diagram |
| E-003 | File | `skills/adversary/SKILL.md` | Routing disambiguation table (most complete example), When to Use/NEVER pattern |
| E-004 | File | `skills/eng-team/SKILL.md` | Large skill pattern (10 agents), references traceability, cross-skill integration |
| E-005 | File | `skills/problem-solving/agents/ps-analyst.md` | XML-tag section structure, invocation protocol, session context validation |
| E-006 | File | `skills/problem-solving/agents/ps-analyst.governance.yaml` | Governance YAML full example, all required fields |
| E-007 | File | `skills/eng-team/agents/eng-architect.md` | Heading-based (non-XML) agent body format alternative |
| E-008 | File | `skills/eng-team/agents/eng-architect.governance.yaml` | Governance YAML with cross-skill expertise references |
| E-009 | File | `skills/diataxis/agents/diataxis-classifier.md` | T1 agent pattern (read-only, no Write tool) |
| E-010 | File | `skills/diataxis/agents/diataxis-classifier.governance.yaml` | T1 tier governance, session_context on_send schema |
| E-011 | File | `docs/schemas/agent-governance-v1.schema.json` | Schema requirements: required fields, minItems constraints |
| E-012 | File | `.context/rules/mandatory-skill-usage.md` | 5-column trigger map, all existing registrations |
| E-013 | File | `.context/templates/requirements/USE-CASE.template.md` | Use case frontmatter schema, L0/L1/L2 structure, diagram patterns |
| E-014 | Glob | `skills/*/agents/*.governance.yaml` | Confirms all 80+ agents have governance companion files |
| E-015 | Grep | `cross-skill|downstream.*skill|upstream.*skill` in SKILL.md | Inter-skill data contract patterns (UX sub-skills, eng-team/red-team) |
| E-016 | File | `.context/rules/agent-development-standards.md` | H-34, H-35, dual-file architecture spec, tool tier table, cognitive mode taxonomy |

---

*Analysis Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Confidence: High -- all conclusions grounded in direct file inspection*
*Generated: 2026-03-08*
*Agent: ps-analyst*

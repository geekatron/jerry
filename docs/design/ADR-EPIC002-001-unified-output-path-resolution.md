# ADR-EPIC002-001: Unified Output Path Resolution Standard

> **Type:** adr
> **Status:** proposed
> **Priority:** high
> **Impact:** critical
> **Created:** 2026-03-31
> **Parent:** EPIC-002
> **Auto-Escalation:** AE-003 (new ADR, auto-C3 minimum)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Why this decision is needed |
| [Prior Art Analysis](#prior-art-analysis) | How /problem-solving solves this today |
| [Design Constraints](#design-constraints) | Requirements the solution must satisfy |
| [Options Considered](#options-considered) | Four approaches evaluated |
| [Decision](#decision) | Selected approach with specification |
| [Output Path Resolution Protocol](#output-path-resolution-protocol) | The layered resolution chain |
| [Prompt Recognition Specification](#prompt-recognition-specification) | How agents detect P1/P2/P3/P4 in prompts |
| [Agent Integration Specification](#agent-integration-specification) | How agents declare and receive paths |
| [Failure Mode Analysis](#failure-mode-analysis) | What happens when things go wrong |
| [Migration Guide](#migration-guide) | How to update eng-team, red-team, UX skills |
| [Compatibility Matrix](#compatibility-matrix) | How the protocol works across all invocation contexts |
| [Consequences](#consequences) | Trade-offs and implications |
| [Verification](#verification) | How compliance is tested |
| [References](#references) | Source traceability |

---

## Context

Agent output paths are hardcoded to `skills/{skill-name}/output/{engagement-id}/` in 13 skills — 3 skill families spanning 13 SKILL.md directories: eng-team (1), red-team (1), and user-experience (1 parent + 10 sub-skills) — totaling 107 config files and 32 agents. This causes end users to write into framework directories, creates multi-tenancy collisions, and prevents agents from working within different project contexts.

The root problem is not "wrong hardcoded path" — it is **absence of a path resolution protocol**. Replacing `skills/eng-team/output/` with `projects/${JERRY_PROJECT}/engagements/` would fix one hardcoded location but create another. Agents need to write to wherever the **caller's context requires**:

| Invocation Context | Where Output Should Land |
|-------------------|--------------------------|
| Worktracker entity scope | `projects/PROJ-030/work/BUG-006/eng-security-review.md` |
| Orchestration workflow | `projects/PROJ-007/orchestration/workflow-001/eng/phase-2/eng-architect-threat-model.md` |
| Standalone engagement | `projects/PROJ-010/engagements/RED-0001/red-recon-network-enum.md` |
| UX wave evaluation | `projects/PROJ-022/engagements/UX-0001/ux-heuristic-eval-checkout.md` |
| Ad-hoc invocation | `work/{agent}-{topic-slug}.md` |

The `/problem-solving` skill (9 agents, created 2026-01-07) already solves this with a flexible mechanism. This ADR formalizes that mechanism as a framework-wide standard.

---

## Prior Art Analysis

### How /problem-solving Resolves Output Paths

The mechanism has three layers:

**Layer 1 — Agent declares a default template** (definition-time):
```yaml
# In governance YAML
output:
  location: "projects/${JERRY_PROJECT}/research/{ps-id}-{entry-id}-{topic-slug}.md"
```

**Layer 2 — Caller provides context variables** (invocation-time):
```markdown
## PS CONTEXT (REQUIRED)
- **PS ID:** work-024
- **Entry ID:** e-042
- **Topic:** OAuth2 Implementation Patterns

## MANDATORY PERSISTENCE (P-002)
Create file at: projects/${JERRY_PROJECT}/research/work-024-e-042-oauth2-implementation-patterns.md
```

**Layer 3 — Caller can override the entire path** (invocation-time):
```markdown
## MANDATORY PERSISTENCE (P-002)
Create file at: projects/PROJ-007/orchestration/agent-patterns-20260221-001/ps/phase-2-analysis/ps-analyst-001/gap-analysis.md
```

The critical insight: **the prompt's `MANDATORY PERSISTENCE` block is the actual output path directive**, not the governance YAML template. The governance template serves as documentation and a default — but the caller always has authority to redirect output.

### What Broken Skills Are Missing

| Mechanism | /problem-solving | /eng-team (broken) |
|-----------|-----------------|-------------------|
| Default template in governance | `projects/${JERRY_PROJECT}/...` | `skills/eng-team/output/...` |
| Caller-provided path override | Yes (via P-002 block in prompt) | No mechanism |
| Variable substitution | `{ps-id}`, `{entry-id}`, `{topic-slug}` | `{engagement-id}`, `{topic-slug}` |
| Project root reference | `${JERRY_PROJECT}` (env var) | None |
| Orchestration integration | Orchestrator provides specific path | N/A |
| Worktracker integration | Writes into entity work directory | N/A |

### Other Working Skills

| Skill | Pattern | Key Variable |
|-------|---------|-------------|
| /use-case | `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` | `${JERRY_PROJECT}` |
| /nasa-se | `projects/${JERRY_PROJECT}/architecture/{proj-id}-{entry-id}-{slug}.md` | `${JERRY_PROJECT}` |
| /adversary | No output.location (selector agent); scorers write to caller-specified path | Caller override |

---

## Design Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| DC-1 | Output paths MUST be resolvable to a project-relative location | H-04 (active project required) |
| DC-2 | Agents MUST persist output to files, never transient-only | P-002 (file persistence) |
| DC-3 | Callers MUST be able to override the output path | P-020 (user authority) |
| DC-4 | The mechanism MUST work for standalone, orchestrated, and worktracker-scoped invocations | Compatibility requirement |
| DC-5 | Engagement-ID scoping MUST be preserved for eng-team, red-team, UX skills | Domain requirement |
| DC-6 | The protocol MUST NOT require Python code changes — agent definitions only | Practical constraint |
| DC-7 | Existing /problem-solving agents MUST NOT be broken by the new standard | Backward compatibility |

---

## Options Considered

### Option A: Hardcode to New Location

Replace `skills/eng-team/output/{engagement-id}/` with `projects/${JERRY_PROJECT}/engagements/{engagement-id}/`.

**Pros:** Simple find-and-replace. Immediate fix.
**Cons:** Still hardcoded. Doesn't work for orchestration or worktracker-scoped invocations. Fails DC-3, DC-4.

### Option B: Caller Always Provides Full Path

Remove output.location from agent definitions entirely. Require every caller to specify the exact output path.

**Pros:** Maximum flexibility. No hardcoding anywhere.
**Cons:** Breaks standalone invocations where no orchestrator exists. Every prompt must include path. Fails DC-4 for ad-hoc usage.

### Option C: Output Path Resolver Utility (Python)

Build a Python function that resolves output paths based on context (project, orchestration, worktracker entity).

**Pros:** Centralized, testable, deterministic.
**Cons:** Requires Python code changes. Claude Code agents execute as LLM subprocesses that interact exclusively through declared tools (Read, Write, Bash, etc.) — per the T1-T5 tool tier model in `agent-development-standards.md` [Tool Security Tiers], each agent's `capabilities.allowed_tools` defines its complete interaction surface. There is no "import" or "function call" mechanism from within an agent's LLM context to invoke a Python resolver at path-computation time. The agent would need to call `Bash("uv run python resolve_path.py ...")` to run a resolver script, introducing tool-call overhead (Bash tool invocation + `uv run` subprocess startup), a runtime dependency on the script being present in the correct location, and a fragile coupling between agent definition (`.md`) and Python utility (`src/`). Fails DC-6.

### Option D: Layered Resolution Protocol with Fallback Chain

Agents declare a default template. Callers can provide a `base_path` that overrides the project-relative prefix. A three-tier fallback chain resolves the output location.

**Pros:** Flexible — works in all contexts (DC-4). Backward-compatible — existing ps agents already use this pattern (DC-7). No Python changes (DC-6). Supports caller override (DC-3). Preserves engagement-ID scoping (DC-5). Project-relative paths (DC-1). Agents always persist (DC-2).
**Cons:** Requires updating 107 config files (governance YAML, agent .md, composition YAML, SKILL.md, templates, rules) across 13 skills (migration cost). Callers must learn 3 prompt patterns (P1/P2/P3). Documentation overhead for the resolution protocol. No DCs fail — all 7 satisfied.
**Risk:** If callers don't provide context, P3 default may produce a less-than-ideal directory structure. Mitigated by P3 defaults being reasonable project-relative paths.

### DC Satisfaction Matrix

| Constraint | Option A | Option B | Option C | Option D |
|-----------|----------|----------|----------|----------|
| DC-1 Project-relative | Pass | Pass | Pass | **Pass** |
| DC-2 File persistence | Pass | Pass | Pass | **Pass** |
| DC-3 Caller override | **Fail** | Pass | Pass | **Pass** |
| DC-4 All contexts | **Fail** | **Fail** | Pass | **Pass** |
| DC-5 Engagement-ID | Pass | Pass | Pass | **Pass** |
| DC-6 No Python changes | Pass | Pass | **Fail** | **Pass** |
| DC-7 Backward compat | Pass | **Fail** | Pass | **Pass** |
| **DCs satisfied** | **5/7** | **5/7** | **6/7** | **7/7** |

---

## Decision

**Selected: Option D — Layered Resolution Protocol with Fallback Chain**

This formalizes how /problem-solving already works, extends it to all skills, and adds explicit support for the caller-provided base path that enables worktracker-scoped and orchestration-scoped output.

---

## Output Path Resolution Protocol

### Resolution Chain (ordered by precedence)

```
Priority 1: EXPLICIT PATH (caller provides full path in P-002 block)
    ↓ not provided
Priority 2: BASE PATH + AGENT SUFFIX (caller provides base_path, agent appends filename)
    ↓ not provided
Priority 3: PROJECT DEFAULT (agent template with ${JERRY_PROJECT})
    ↓ JERRY_PROJECT not set
Priority 4: WORK DIRECTORY FALLBACK (work/{agent}-{slug}.md)
```

### Priority 1: Explicit Path

The caller specifies the exact output path in the prompt's P-002 persistence block. Agent writes to that path verbatim.

```markdown
## MANDATORY PERSISTENCE (P-002)
Create file at: projects/PROJ-007/orchestration/workflow-001/eng/phase-2/eng-architect-threat-model.md
```

**When used:** Orchestration workflows, worktracker-scoped invocations, any context where the caller knows exactly where the output should go.

### Priority 2: Base Path + Agent Suffix

The caller provides a `base_path` and the agent appends its standard filename pattern.

```markdown
## OUTPUT CONTEXT
- **Base Path:** projects/PROJ-030/work/BUG-006/
- **Engagement ID:** GH-118
```

Agent computes: `{base_path}/{agent}-{topic-slug}.md`
Result: `projects/PROJ-030/work/BUG-006/eng-security-review-auth-handler.md`

**When used:** Worktracker entity scope (base_path = entity work directory), standalone engagements (base_path = engagement directory).

### Priority 3: Project Default

No caller override provided. Agent uses its governance YAML template with `${JERRY_PROJECT}`.

```yaml
# Governance YAML
output:
  location: "projects/${JERRY_PROJECT}/engagements/{engagement-id}/{agent}-{topic-slug}.md"
```

Agent resolves `${JERRY_PROJECT}` from environment and computes the full path.

**When used:** Standalone invocation where user says "run eng-architect on this" without specifying output context. This is the **most common case** for end users.

### Priority 4: Work Directory Fallback

`${JERRY_PROJECT}` is not set (violates H-04 but provides graceful degradation).

Agent writes to: `work/{agent}-{topic-slug}.md`

Agent MUST log a warning: "JERRY_PROJECT not set — output written to work/ fallback. Set JERRY_PROJECT for proper project tracking."

**When used:** Should never happen in normal operation. Safety net only.

### Resolution Algorithm (Pseudocode)

The following pseudocode uses Python-like syntax for readability. This is a **specification of the resolution logic**, not executable code — agents implement this logic through their prompt instructions and tool calls, not through a Python function. See Option C analysis for why a Python resolver was rejected.

```
function resolve_output_path(prompt_context, agent_config):
    # Priority 1: Explicit path in P-002 block
    if prompt_context.has("MANDATORY PERSISTENCE"):
        explicit_path = prompt_context.extract_p002_path()
        if explicit_path:
            return explicit_path

    # Priority 2: Base path + agent suffix
    if prompt_context.has("OUTPUT CONTEXT.base_path"):
        base = prompt_context.base_path
        # compute_filename interpolates output.filename_pattern with variables
        # e.g., "eng-architect-{topic-slug}.md" + {topic-slug: "threat-model"} → "eng-architect-threat-model.md"
        suffix = agent_config.output.filename_pattern.interpolate(prompt_context.variables)
        return join(base, suffix)

    # Priority 3: Project default template
    if env.JERRY_PROJECT is set:
        template = agent_config.output.location
        return template.substitute(prompt_context.variables, env.JERRY_PROJECT)

    # Priority 4: Fallback
    warn("JERRY_PROJECT not set — using work/ fallback")
    suffix = agent_config.output.filename_pattern.interpolate(prompt_context.variables)
    return join("work/", suffix)
```

### Prompt Recognition Specification

Agents detect which priority level applies by scanning for specific markdown section headers in their prompt:

| Priority | Trigger Condition | Section Header | Required Field |
|----------|------------------|----------------|---------------|
| P1 | Prompt contains `## MANDATORY PERSISTENCE (P-002)` with a `Create file at:` line | `## MANDATORY PERSISTENCE (P-002)` | `Create file at: {path}` |
| P2 | Prompt contains `## OUTPUT CONTEXT` with a `Base Path:` field | `## OUTPUT CONTEXT` | `- **Base Path:** {path}` |
| P3 | Prompt contains `## OUTPUT CONTEXT` WITHOUT `Base Path:`, or no OUTPUT CONTEXT block at all | N/A (absence triggers default) | Agent uses `output.location` template |
| P4 | P3 triggered but `${JERRY_PROJECT}` unresolvable | N/A | Agent uses `work/` fallback |

**Precedence:** If both P1 and P2 markers are present, P1 wins (explicit path overrides base path). Agents scan for P1 first.

---

## Agent Integration Specification

### Governance YAML Changes

The `output.location` field becomes the **Priority 3 default template**, not the only path. Add a new `output.filename_pattern` field for Priority 2 resolution:

```yaml
output:
  required: true
  # Priority 3: Default template (used when no caller override)
  location: "projects/${JERRY_PROJECT}/engagements/{engagement-id}/{agent}-{topic-slug}.md"
  # Priority 2: Filename pattern (appended to caller-provided base_path)
  filename_pattern: "{agent}-{topic-slug}.md"
  levels:
    - L0
    - L1
    - L2
```

### Agent Definition (.md) Changes

Add an OUTPUT PATH RESOLUTION section to the `<output>` block explaining the precedence chain:

```markdown
<output>
### Output Path Resolution

This agent follows the Unified Output Path Resolution Protocol (ADR-EPIC002-001):

1. **Explicit path** — If the caller provides a path in the P-002 block, write there
2. **Base path** — If the caller provides `OUTPUT CONTEXT.base_path`, append `{agent}-{topic-slug}.md`
3. **Project default** — Write to `projects/${JERRY_PROJECT}/engagements/{engagement-id}/{agent}-{topic-slug}.md`
4. **Fallback** — Write to `work/{agent}-{topic-slug}.md` with warning

### Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{engagement-id}` | Caller-provided or generated | `RED-0001`, `GH-118`, `UX-0001` |
| `{agent}` | Definition-time constant: the agent's own name, hardcoded into `filename_pattern` at definition time (e.g., `eng-architect-{topic-slug}.md`). NOT a runtime variable — resolved when the agent definition is authored. | `eng-architect`, `red-recon` |
| `{topic-slug}` | Auto-derived: lowercase input topic, spaces/special chars replaced with hyphens, truncated to 50 chars. If caller provides a slug directly, use as-is. | `threat-model`, `network-enum` |
| `{ps-id}` | /problem-solving only: problem-solving context ID, provided by caller in PS CONTEXT block. Pattern: `^[a-z]+-\d+$`. Not used by eng/red/UX agents. | `work-024`, `feat-003` |
| `{entry-id}` | /problem-solving only: artifact entry ID within a PS context. Pattern: `^e-\d+$`. Not used by eng/red/UX agents. | `e-001`, `e-042` |
</output>
```

### Prompt Integration

Callers use ONE of three patterns depending on context:

**Pattern A — Explicit path (orchestration, worktracker scope):**
```markdown
## MANDATORY PERSISTENCE (P-002)
Create file at: projects/PROJ-030/work/BUG-006/eng-security-review.md
```

**Pattern B — Base path (engagement scope):**
```markdown
## OUTPUT CONTEXT
- **Base Path:** projects/${JERRY_PROJECT}/engagements/RED-0001/
- **Engagement ID:** RED-0001
```

**Pattern C — No override (standalone, uses default):**
```markdown
## OUTPUT CONTEXT
- **Engagement ID:** RED-0001
```
Agent falls through to Priority 3: `projects/${JERRY_PROJECT}/engagements/RED-0001/{agent}-{topic-slug}.md`

---

## Failure Mode Analysis

| Failure | Detection | Resolution |
|---------|-----------|------------|
| Agent ignores P-002 block and uses hardcoded path | Post-tool output inspection: artifact not at expected location | L4 enforcement: flag mismatch between declared and actual output path |
| Caller-provided `base_path` is non-existent directory | Write tool fails with path error | Agent creates directory via `mkdir -p` equivalent before writing (standard Write tool behavior) |
| `{topic-slug}` is undefined or empty | Filename resolves to `{agent}-.md` (malformed) | Agent MUST validate slug is non-empty before write; fall back to `{agent}-unnamed.md` with warning |
| `{engagement-id}` not provided and no default exists | Path template has literal `{engagement-id}` in output | Agent MUST request engagement-id via H-31 clarification before writing |
| `${JERRY_PROJECT}` env var unset (P4 fallback) | H-04 violation detected at session start | Graceful degradation to `work/` with logged warning; SessionStart hook should prevent this |
| Multiple agents write to same base_path concurrently | File overwrite if filenames collide | `{agent}` prefix in filename_pattern prevents collision (each agent has unique name) |
| Caller provides P1 explicit path AND P2 base_path | Ambiguous — which takes precedence? | P1 always wins (highest priority). P2 is ignored when P1 is present. |

---

## Migration Guide

**Scope:** 107 config files across 13 skills, 32 agents (source: [BUG-006 audit details](../../PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md) with line-level audits in [eng-audit](../../PROJ-030-bugs/work/BUG-006-eng-audit-detail.md), [red-audit](../../PROJ-030-bugs/work/BUG-006-red-audit-detail.md), [ux-audit](../../PROJ-030-bugs/work/BUG-006-ux-audit-detail.md)).

### EXECUTE FIRST — Step 0: Update Governance Schema

**Do this before any YAML updates.** Add `filename_pattern` to `docs/schemas/agent-governance-v1.schema.json` (see [Step 6 detail](#step-6-update-governance-schema) below for the JSON diff). This ensures schema validation accepts the new field when Step 1 adds it to governance YAML files.

### Step 1: Update Governance YAML (32 agents)

Change `output.location` from hardcoded skill path to project-relative template. Add `filename_pattern`.

**eng-team (10 files):** `skills/eng-team/agents/eng-{architect,backend,devsecops,frontend,incident,infra,lead,qa,reviewer,security}.governance.yaml`

**Before:**
```yaml
output:
  location: "skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md"
```

**After:**
```yaml
output:
  location: "projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md"
  filename_pattern: "eng-architect-{topic-slug}.md"
```

**red-team (11 files):** `skills/red-team/agents/red-{exfil,exploit,infra,lateral,lead,persist,privesc,recon,reporter,social,vuln}.governance.yaml`

**Before:**
```yaml
output:
  location: "skills/red-team/output/{engagement-id}/red-recon-{topic-slug}.md"
```

**After:**
```yaml
output:
  location: "projects/${JERRY_PROJECT}/engagements/{engagement-id}/red-recon-{topic-slug}.md"
  filename_pattern: "red-recon-{topic-slug}.md"
```

**UX (11 files):** `skills/ux-{ai-first-design,atomic-design,behavior-design,design-sprint,heart-metrics,heuristic-eval,inclusive-design,jtbd,kano-model,lean-ux}/agents/*.governance.yaml` + `skills/user-experience/agents/ux-orchestrator.governance.yaml`

**Before:**
```yaml
output:
  location: "skills/ux-heart-metrics/output/{engagement-id}/ux-heart-analyst-{topic-slug}.md"
```

**After:**
```yaml
output:
  location: "projects/${JERRY_PROJECT}/engagements/{engagement-id}/ux-heart-analyst-{topic-slug}.md"
  filename_pattern: "ux-heart-analyst-{topic-slug}.md"
```

### Step 2: Update Agent Definitions (32 agent .md files)

Add the Output Path Resolution section to each agent's `<output>` block. The same pattern applies across all three skill families — only the agent name and default path differ.

**Before (eng-architect.md, red-recon.md, ux-heart-analyst.md — same pattern):**
```markdown
<output>
### Output Location
skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md
</output>
```

**After:**
```markdown
<output>
### Output Path Resolution

This agent follows the Unified Output Path Resolution Protocol (ADR-EPIC002-001):

1. **Explicit path** — If the caller provides a path in the P-002 block, write there
2. **Base path** — If the caller provides `OUTPUT CONTEXT.base_path`, append filename
3. **Project default** — `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md`
4. **Fallback** — `work/eng-architect-{topic-slug}.md` with warning
</output>
```

### Step 3: Update SKILL.md and Rules Files (13 SKILL.md + UX rules files)

Replace agent table output column. Also update any examples, P-002 sections, and rules files that reference `skills/*/output/` paths. The UX skills have 15 rules files with output path references (routing rules, wave-progression, CI checks, synthesis-validation, MCP runbooks, methodology rules — see [UX audit detail](../../PROJ-030-bugs/work/BUG-006-ux-audit-detail.md) for per-file line numbers). These are included in the 60-file UX count and are covered by TASK-008.

**Before (eng-team SKILL.md line 119):**
```markdown
| `eng-architect` | ... | `skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md` |
```

**After:**
```markdown
| `eng-architect` | ... | `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md` |
```

### Step 4: Update Templates (15 files: 3 engagement + 12 UX)

**Before (eng-team engagement-playbook.md line 189):**
```markdown
6. [ ] Create output directory: `skills/eng-team/output/{engagement-id}/`
```

**After:**
```markdown
6. [ ] Output will be written to `projects/${JERRY_PROJECT}/engagements/{engagement-id}/` per ADR-EPIC002-001
```

**red-team engagement-playbook.md (line 81):**
```markdown
# Before:
10. [ ] Scope document persisted to `skills/red-team/output/{engagement-id}/`
# After:
10. [ ] Scope document persisted per ADR-EPIC002-001 resolution protocol (default: `projects/${JERRY_PROJECT}/engagements/{engagement-id}/`)
```

**red-team pentest-engagement.md (line 151):**
```yaml
# Before:
storage: "skills/red-team/output/RED-{NNNN}/evidence/"
# After:
storage: "projects/${JERRY_PROJECT}/engagements/RED-{NNNN}/evidence/"
```

**UX template example (ux-lean-ux hypothesis-backlog-template.md line 398):**
```yaml
# Before:
artifact_path: skills/ux-lean-ux/output/{{ENGAGEMENT_ID}}/hypothesis-backlog-{{TOPIC_SLUG}}.md
# After:
artifact_path: projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/hypothesis-backlog-{{TOPIC_SLUG}}.md
```

**Files:** `skills/eng-team/templates/engagement-playbook.md`, `skills/red-team/templates/engagement-playbook.md`, `skills/red-team/templates/pentest-engagement.md`, plus 12 UX template files (see [UX audit detail](../../PROJ-030-bugs/work/BUG-006-ux-audit-detail.md))

### Step 5: Codify as AD-M-011 Standard

Add to `.context/rules/agent-development-standards.md` in the **Agent Structure Standards** table (after AD-M-010):

```markdown
| AD-M-011 | Agent output paths SHOULD follow the Unified Output Path Resolution Protocol (ADR-EPIC002-001). Agents SHOULD declare `output.location` as a project-relative default template using `projects/${JERRY_PROJECT}/` prefix, and SHOULD declare `output.filename_pattern` for base-path resolution. Agents SHOULD accept caller-provided explicit paths (Priority 1) or base paths (Priority 2) that override the default template. Agents SHOULD NOT hardcode output paths to `skills/*/output/` or any other skill-internal directory. Override requires documented justification per MEDIUM tier vocabulary. | Ensures agents work correctly in orchestration, worktracker, engagement, and standalone contexts. Prevents the skill-internal output path anti-pattern (BUG-006/GH #230). Reference architecture: `/problem-solving` agents. | ADR-EPIC002-001, BUG-006 |
```

### Step 6: Update Governance Schema

Add `filename_pattern` to `docs/schemas/agent-governance-v1.schema.json` in the `output` object:

**Diff:**
```json
"output": {
  "type": "object",
  "properties": {
    "required": { "type": "boolean" },
    "location": { "type": "string" },
+   "filename_pattern": {
+     "type": "string",
+     "description": "Filename template for Priority 2 base-path resolution (ADR-EPIC002-001). Interpolated with agent variables when caller provides OUTPUT CONTEXT.base_path."
+   },
    "levels": { ... }
  }
}
```

This is a non-breaking additive change — existing agents without `filename_pattern` continue to validate. H-34 schema validation will accept both old and new formats.

### Migration Order and Rollback

**Execution order (per skill, not cross-skill):**
0. Update governance schema FIRST (Step 6) — adds `filename_pattern` as accepted field BEFORE any YAML files reference it. This is a one-time global step, not per-skill.
1. Update governance YAML (Step 1) — this is the runtime directive
2. Update agent .md (Step 2) — agent behavior instructions
3. Update SKILL.md and rules (Step 3) — documentation alignment
4. Update templates (Step 4) — engagement playbook alignment
5. Run schema validation: `uv run jerry schema validate`

**Recommended skill sequence:** eng-team first (smallest, 22 files, has real output files to validate against), then red-team (25 files, similar structure), then UX (60 files, largest batch). This order provides incremental learning.

### Migration Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Partial migration leaves some agents on old paths, others on new | Medium | Low — agents are independent; mixed state is functional | Migrate per-skill atomically (all files for one skill in one commit) |
| Schema validation fails mid-migration due to `filename_pattern` | Low | Low — field is additive, schema accepts both formats until Step 6 | Run Step 6 (schema update) before Step 1, or add field as optional |
| UX orchestrator references sub-skill output paths that changed | Medium | Medium — orchestrator routing rules hardcode sub-skill paths | Update orchestrator rules (ux-routing-rules.md, wave-progression.md) as part of TASK-008 |
| Engagement playbook instructs users to create old directories | Low | Low — playbooks are documentation, not enforcement | Step 4 updates playbooks before users encounter them |

**Rollback procedure:** Each skill is independently migratable. If a skill migration causes issues:
1. `git checkout HEAD~1 -- skills/{skill-name}/` to revert that skill only
2. Other migrated skills are unaffected (no cross-skill dependencies in output paths)
3. The old `skills/*/output/` paths continue to function until `.gitignore` blocks new output files

---

## Compatibility Matrix

This matrix shows how the resolution protocol works in every invocation context:

| Context | Resolution Priority | Caller Provides | Agent Produces | Example Output Path |
|---------|-------------------|-----------------|----------------|---------------------|
| **Orchestration workflow** | P1 (explicit) | Full path in P-002 block | Writes to exact path | `projects/PROJ-007/orchestration/workflow-001/eng/phase-2/eng-architect-threat-model.md` |
| **Worktracker entity** | P1 or P2 | Full path or base_path | Writes to entity scope | `projects/PROJ-030/work/BUG-006/eng-security-review.md` |
| **Standalone engagement** | P2 (base path) | base_path with engagement-id | Appends filename | `projects/PROJ-010/engagements/RED-0001/red-recon-network-enum.md` |
| **UX wave evaluation** | P2 (base path) | base_path with engagement-id | Appends filename | `projects/PROJ-022/engagements/UX-0001/ux-heuristic-eval-checkout.md` |
| **User ad-hoc** | P3 (default) | Engagement-id only | Uses default template | `projects/PROJ-024/engagements/GH-231/eng-architect-auth-review.md` |
| **No project set** | P4 (fallback) | Nothing | Fallback + warning | `work/eng-architect-auth-review.md` |
| **ps-researcher (existing)** | P3 (default) | PS CONTEXT vars | Uses existing template | `projects/PROJ-024/research/work-024-e-042-oauth2.md` (unchanged) |

### Backward Compatibility

- **Existing /problem-solving agents (9 agents, per `skills/problem-solving/SKILL.md` lines 78-88):** Already use P1/P3 implicitly. No changes required. Their governance YAML `output.location` already uses `projects/${JERRY_PROJECT}/` prefix.
- **Existing /adversary agents:** adv-scorer writes to caller-specified path (P1, per `skills/adversary/agents/adv-scorer.governance.yaml` output section). No changes required.
- **Existing /nasa-se agents:** Already use `projects/${JERRY_PROJECT}/` prefix (per `skills/nasa-se/agents/nse-architecture.governance.yaml` output.location). No changes required for this ADR. Adding `filename_pattern` for optional P2 support is a separate enhancement tracked outside this migration scope — /nasa-se paths are correct today and do not suffer from the `skills/*/output/` bug.

---

## Consequences

### Positive

1. **All 32 agents** (10 eng + 11 red + 11 UX, per [BUG-006 audit](../../PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md)) across eng-team, red-team, and UX work correctly in any invocation context
2. **Orchestration integration** — agents write to workflow-scoped directories when orchestrated
3. **Worktracker integration** — agents write to entity work directories when entity-scoped
4. **End-user portability** — no outputs in skill directories; all outputs in user project space
5. **Consistent mechanism** — one resolution protocol for all skills, documented in agent-development-standards.md
6. **Backward compatible** — existing /problem-solving, /adversary, /nasa-se agents work without changes

### Negative

1. **107 files to update** (22 eng + 25 red + 60 UX, verified via `grep -rl`, per [BUG-006 audit details](../../PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md)) — governance YAML, composition YAML, SKILL.md, agent .md, templates, rules
2. **Callers must learn the protocol** — P1/P2/P3 patterns need to be documented in prompt templates
3. **Engagement-ID generation** moves from skill-internal (current) to caller-provided — engagement playbook templates need updating

### Neutral

1. `output.location` in governance YAML changes meaning from "the only path" to "the default path (Priority 3)"
2. New `filename_pattern` field added to governance YAML schema — non-breaking addition

---

## Verification

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| No hardcoded `skills/*/output/` paths | `grep -r 'skills/.*/output/' skills/` | Zero matches |
| All governance YAML have `filename_pattern` | Schema validation | All 32 affected agents have field |
| P1 works (orchestration) | Manual test: invoke eng-architect with explicit path | Output lands at specified path |
| P2 works (base path) | Manual test: invoke eng-architect with base_path | Output lands at base_path + filename |
| P3 works (default) | Manual test: invoke eng-architect with engagement-id only | Output lands at project default |
| P4 works (fallback) | Manual test: unset JERRY_PROJECT, invoke | Output lands in work/ with warning |
| ps-researcher unchanged | Invoke ps-researcher normally | Output lands at existing ps path |
| AD-M-011 codified | Read agent-development-standards.md | Standard exists with protocol reference |

---

## References

| Source | Content |
|--------|---------|
| [BUG-006](../../PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md) | Output path bug entity — 107 files, 32 agents, 13 skills |
| [BUG-006 eng-team audit](../../PROJ-030-bugs/work/BUG-006-eng-audit-detail.md) | Line-level audit: 22 files with per-file citations and sum-check |
| [BUG-006 red-team audit](../../PROJ-030-bugs/work/BUG-006-red-audit-detail.md) | Line-level audit: 25 files with per-file citations and sum-check |
| [BUG-006 UX audit](../../PROJ-030-bugs/work/BUG-006-ux-audit-detail.md) | Line-level audit: 60 files across 11 sub-skills with per-skill citations and sum-check |
| [GH #230](https://github.com/geekatron/jerry/issues/230) | GitHub issue tracking the output path defect |
| `skills/problem-solving/composition/*.agent.yaml` | Prior art: output.location templates with `${JERRY_PROJECT}` |
| `skills/problem-solving/templates/PS_EXTENSION.md` lines 76-131 | Output convention documentation with per-agent naming table |
| `skills/problem-solving/composition/ps-researcher.prompt.md` lines 213-243 | PS CONTEXT + P-002 persistence block — the runtime path passing mechanism |
| `.context/rules/agent-development-standards.md` | Target location for AD-M-011 standard |
| `docs/schemas/agent-governance-v1.schema.json` | Target schema for `filename_pattern` field addition |
| [TASK-008](../../PROJ-030-bugs/work/TASK-008-ux-skills-path-remediation.md) | UX skills path remediation — 60 files across 11 sub-skills |
| `.context/rules/quality-enforcement.md` | AE-003 auto-escalation, H-04 project requirement |

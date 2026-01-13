# WI-SAO-021: Identifier Strategy Research

> **Document ID:** RSH-SAO-021-001
> **Work Item:** WI-SAO-021 (Orchestration Folder Refactoring)
> **Date:** 2026-01-10
> **Status:** COMPLETE

---

## Executive Summary

This research investigates identifier strategies for the orchestration skill's dynamic path scheme. The goal is to replace hardcoded pipeline identifiers (`ps`, `nse`) with fully dynamic identifiers that support future extensibility and cross-pollination workflows.

**Recommendation:** Option 3 - User-specified with semantic fallback

---

## 1. Requirements Analysis

From WI-SAO-021 refined requirements:

| Requirement | Description |
|-------------|-------------|
| R1 | NO hardcoded values - all identifiers must be dynamic |
| R2 | Stable identifier generation - created when plan is created |
| R3 | User choice - user can specify or accept auto-generated |
| R4 | Dual storage - in ORCHESTRATION.yaml AND human-facing *.md |
| R5 | Cross-pollination support - must work with barrier sync |
| R6 | Future extensibility - support new pipeline families |

### Target Path Structure

```
orchestration/{workflow_id}/
├── {pipeline_id_1}/{phase}/
├── {pipeline_id_2}/{phase}/
└── cross-pollination/
    └── barrier-{n}/
        ├── {source}-to-{target}/
```

All placeholders (`workflow_id`, `pipeline_id_*`, `source`, `target`) must be dynamic.

---

## 2. Industry Research

### 2.1 Temporal (Workflow Orchestration)

**Source:** [Temporal Workflow ID and Run ID Documentation](https://docs.temporal.io/workflow-execution/workflowid-runid)

Temporal uses a two-tier identifier system:

| Identifier | Type | Purpose | Example |
|------------|------|---------|---------|
| `workflow_id` | User-defined (semantic) | Deduplication, business identity | `order-12345`, `user-signup-abc` |
| `run_id` | System-generated (UUID) | Execution instance | `a7f3b2c1-1f5b-6704-8004-820c16b69a5a` |

**Key insight:** Temporal guarantees only one workflow with a given `workflow_id` can run at a time. For scheduled workflows, timestamps are often included in the `workflow_id` to allow concurrent scheduled runs.

### 2.2 LangGraph (AI Agent Orchestration)

**Source:** [LangGraph Persistence Concepts](https://github.com/langchain-ai/langgraph)

LangGraph uses:

| Identifier | Type | Purpose | Example |
|------------|------|---------|---------|
| `thread_id` | User-defined | Conversation/workflow series | `"user-123"`, `"1"` |
| `checkpoint_id` | System-generated (UUID) | Point-in-time snapshot | `1f029ca3-1f5b-6704-8004-820c16b69a5a` |

**Key insight:** LangGraph's `thread_id` is fully user-controlled and used for state persistence across invocations.

### 2.3 Prefect (Workflow Orchestration)

**Source:** [Prefect Documentation](https://docs.prefect.io/)

Prefect uses Python decorators with minimal configuration. Flow runs get auto-generated IDs.

### 2.4 General Naming Conventions

**Sources:**
- [Microsoft Power Automate Naming Guidelines](https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/use-consistent-naming-conventions)
- [Nuxeo Workflow Naming Conventions](https://doc.nuxeo.com/nxdoc/workflow-naming-conventions/)
- [IBM Workflow Naming Conventions](https://www.ibm.com/docs/en/tap/5.0.0?topic=building-workflow-naming-conventions)

Best practices:
1. Short and descriptive (max 25 characters for entity types)
2. Use camelCase or snake_case consistently
3. Include purpose/function in the name
4. Avoid generic names (not "Workflow1")
5. Document conventions in a style guide

---

## 3. Existing Jerry Patterns

### 3.1 Current Orchestration Template

From `skills/orchestration/templates/ORCHESTRATION.template.yaml`:

```yaml
workflow:
  id: "{WORKFLOW_ID}"           # Placeholder for workflow ID
  name: "{WORKFLOW_NAME}"
  project_id: "{PROJECT_ID}"
```

The template already uses `{WORKFLOW_ID}` as a placeholder, but:
- No guidance on how to generate it
- No specification of format/semantics
- Pipeline IDs use generic `pipeline_a`, `pipeline_b`

### 3.2 E2E Test Patterns

From `tests/e2e/TEST-003-CROSSPOLL-WORKFLOW.yaml`:

```yaml
workflow:
  id: "TEST-003-CROSSPOLL"      # Semantic, descriptive

pipelines:
  alpha:                         # Dynamic pipeline ID
    id: "alpha-pipeline"
  beta:
    id: "beta-pipeline"

artifacts:
  alpha_to_beta:
    path: "tests/e2e/artifacts/crosspoll/alpha-to-beta.md"
```

**Observations:**
- Workflow ID is semantic: `TEST-003-CROSSPOLL`
- Pipeline IDs are dynamic: `alpha`, `beta`
- Artifact paths are somewhat hardcoded (no workflow_id in path)

---

## 4. Identifier Strategy Options

### Option 1: Semantic + Timestamp

**Format:** `{purpose}-{YYYYMMDD}-{seq}`

**Example:**
- Workflow: `sao-crosspoll-20260110-001`
- Pipeline: `problem-solving` (from skill name)
- Barrier: `problem-solving-to-nasa-se`

**Pros:**
- Human-readable
- Sortable by date
- Purpose clear from prefix
- Unique via sequence number

**Cons:**
- Longer identifiers
- Requires tracking sequence numbers
- Date may become stale if workflow spans multiple days

### Option 2: UUID-based

**Format:** `{uuid-v4}` or `{short-uuid-8-chars}`

**Example:**
- Workflow: `a7f3b2c1` or `a7f3b2c1-1f5b-6704-8004-820c16b69a5a`
- Pipeline: `e2d4f6a8`
- Barrier: `b1c2d3e4`

**Pros:**
- Guaranteed unique
- Compact (short form)
- No collision risk
- Deterministic generation

**Cons:**
- Not human-readable
- No semantic meaning
- Hard to debug/navigate

### Option 3: User-Specified with Semantic Fallback (Recommended)

**Format:** User provides OR auto-generate `{purpose}-{YYYYMMDD}-{NNN}`

**Workflow ID Generation:**
1. Orchestration skill asks user: "Provide a workflow identifier, or press Enter to auto-generate"
2. If user provides: validate format (alphanumeric, hyphens, max 50 chars)
3. If auto-generate: `{skill-prefix}-{YYYYMMDD}-{NNN}` where NNN is sequence

**Pipeline ID Generation:**
1. Derived from the skill being orchestrated
2. `problem-solving` → `ps` (short alias)
3. `nasa-se` → `nse` (short alias)
4. User can override if needed

**Example:**
```
orchestration/sao-crosspoll-20260110-001/
├── ps/phase-1-research/
├── ps/phase-2-analysis/
├── nse/phase-1-scope/
├── nse/phase-2-risk/
└── cross-pollination/
    └── barrier-1/
        ├── ps-to-nse/
        └── nse-to-ps/
```

**Pros:**
- User control when needed
- Sensible defaults for automation
- Human-readable
- Traceable to source workflow
- Consistent fallback

**Cons:**
- Slightly more complex implementation
- User prompt required (can be skipped with flag)

### Option 4: Content Hash (Content-Addressable)

**Format:** `{sha256-of-workflow-definition[:12]}`

**Example:**
- Workflow: `a7f3b2c1e4d6` (first 12 chars of SHA256)

**Pros:**
- Deterministic (same workflow = same ID)
- Cache-friendly
- No collision risk

**Cons:**
- Changes to workflow definition = new ID
- Not human-readable
- Hard to correlate with source

---

## 5. Recommendation

**Recommended: Option 3 - User-Specified with Semantic Fallback**

### Rationale

| Criterion | Option 1 | Option 2 | Option 3 | Option 4 |
|-----------|----------|----------|----------|----------|
| Human-readable | Yes | No | Yes | No |
| User control | No | No | **Yes** | No |
| Unique guarantee | Medium | High | **High** | High |
| Future extensibility | Good | Good | **Excellent** | Good |
| Debug-friendly | Good | Poor | **Excellent** | Poor |
| Industry alignment | Temporal | - | **LangGraph** | Git |

### Implementation Details

**1. Workflow ID:**
```yaml
workflow:
  id: "sao-crosspoll-20260110-001"  # User-specified or auto-generated
  id_source: "user" | "auto"         # Track origin
  id_format: "semantic-date-seq"     # Document format used
```

**2. Pipeline ID:**
- Derived from skill registration: `skills/{skill-name}/` → `{skill-short-alias}`
- Skill registry includes `short_alias` field
- Example: `skills/problem-solving/SKILL.md` → `ps`
- Example: `skills/nasa-se/SKILL.md` → `nse`
- Example: `skills/future-skill/SKILL.md` → `fs` (or user-defined)

**3. Cross-Pollination:**
- Barrier path uses pipeline short aliases
- Pattern: `cross-pollination/barrier-{n}/{source}-to-{target}/`
- Example: `cross-pollination/barrier-1/ps-to-nse/`

**4. Storage Locations:**
- ORCHESTRATION.yaml: `workflow.id`, `pipelines.{id}.short_alias`
- ORCHESTRATION_PLAN.md: Header with workflow ID
- ORCHESTRATION_WORKTRACKER.md: Header with workflow ID

### Proposed Schema Update

```yaml
# ORCHESTRATION.yaml additions
workflow:
  id: "{WORKFLOW_ID}"
  id_source: "auto"           # "user" | "auto"
  id_format: "semantic-date-seq"  # Format specification

pipelines:
  {pipeline_key}:              # Dynamic key from skill
    id: "{pipeline_id}"        # Full pipeline ID
    short_alias: "{alias}"     # Short alias for paths (2-4 chars)
    skill_source: "{skill_name}"  # Originating skill

paths:
  base: "orchestration/{workflow_id}/"
  pipeline: "{base}/{short_alias}/{phase}/"
  barrier: "{base}/cross-pollination/barrier-{n}/"
  artifact: "{pipeline}/{artifact_name}.md"
```

---

## 6. Next Steps

1. **Update WORKTRACKER** with this recommendation
2. **Update ORCHESTRATION.template.yaml** with new schema fields
3. **Update orch-planner agent** to prompt for/generate workflow ID
4. **Update orch-tracker agent** to use dynamic paths
5. **Create E2E test** validating dynamic path generation
6. **Run existing tests** to verify no regressions

---

## 7. References

- [Temporal Workflow ID Documentation](https://docs.temporal.io/workflow-execution/workflowid-runid)
- [LangGraph Persistence Concepts](https://github.com/langchain-ai/langgraph)
- [Microsoft Power Automate Naming Guidelines](https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/use-consistent-naming-conventions)
- [IBM Workflow Naming Conventions](https://www.ibm.com/docs/en/tap/5.0.0?topic=building-workflow-naming-conventions)
- [Nuxeo Workflow Naming Conventions](https://doc.nuxeo.com/nxdoc/workflow-naming-conventions/)
- [BMC Workflow Orchestration](https://www.bmc.com/blogs/workflow-orchestration/)

---

*Document ID: RSH-SAO-021-001*
*Classification: RESEARCH*
*Generated: 2026-01-10*

# EN-031: Model Selection Capability

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-30 per FEAT-005 (Model Selection Analysis)
PURPOSE: Allow CLI/API configuration of models for each agent
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-01-30T16:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-005
> **Owner:** Claude
> **Effort:** 32-48h (4-6 days)

---

## Summary

Add CLI parameters to configure which Claude models (opus, sonnet, haiku) are used for each transcript skill agent. Currently models are hardcoded in agent definitions.

**Technical Scope:**
- Add `--model-*` CLI parameters for each agent
- Update SKILL.md with model configuration documentation
- Update agent definitions with model override capability
- Implement model selection logic in orchestration
- Validate Task tool supports model parameter

**Analysis Reference:** [work-025-e-001: Model Selection Effort Analysis](../../../../../docs/analysis/work-025-e-001-model-selection-effort.md)

---

## Problem Statement

Models are currently hardcoded in agent .md files:
- ts-parser: haiku
- ts-extractor: sonnet
- ts-formatter: sonnet
- ts-mindmap-*: sonnet
- ps-critic: sonnet

This prevents:
1. **Cost Optimization** - Cannot use cheaper models when appropriate
2. **Quality Tuning** - Cannot upgrade to opus for critical extractions
3. **Experimentation** - No A/B testing of model performance

**Cost Impact:** Using haiku for all agents could save 88% of API costs.

---

## Business Value

Model selection enables:

1. **Cost Control** - Switch to haiku for non-critical operations (88% savings)
2. **Quality Tuning** - Use opus for high-value transcripts
3. **Performance Testing** - Compare model outputs for same input
4. **User Flexibility** - Users choose cost/quality tradeoff

### Features Unlocked

- Per-run model configuration
- Cost optimization workflows
- Quality comparison testing

---

## Technical Approach

### Phase 1: CLI Parameter Implementation (MVP)

Add command-line parameters to specify models:

```bash
uv run jerry transcript parse meeting.vtt \
    --model-parser haiku \
    --model-extractor sonnet \
    --model-formatter haiku \
    --model-mindmap haiku \
    --model-critic sonnet
```

**Default Values (preserve current behavior):**
- --model-parser: haiku
- --model-extractor: sonnet
- --model-formatter: sonnet
- --model-mindmap: sonnet
- --model-critic: sonnet

### Phase 2: Model Profiles (Full Implementation)

Named profiles for common configurations:

```bash
uv run jerry transcript parse meeting.vtt --profile economy
uv run jerry transcript parse meeting.vtt --profile balanced
uv run jerry transcript parse meeting.vtt --profile quality
```

**Profiles:**
| Profile | Parser | Extractor | Formatter | Mindmap | Critic |
|---------|--------|-----------|-----------|---------|--------|
| economy | haiku | haiku | haiku | haiku | haiku |
| balanced | haiku | sonnet | haiku | haiku | sonnet |
| quality | haiku | opus | sonnet | sonnet | opus |

### Architecture Diagram

```
+-------------------------------------------------------------------+
|                    MODEL SELECTION FLOW                           |
+-------------------------------------------------------------------+
|                                                                   |
|   CLI INVOCATION                                                  |
|   ==============                                                  |
|   jerry transcript parse meeting.vtt --model-extractor opus       |
|                                                                   |
|   +-- CLI Parser                                                  |
|   |   +-- Validate model values (opus|sonnet|haiku)               |
|   |   +-- Build model_config dict                                 |
|   |                                                               |
|   +-- Orchestrator (SKILL.md)                                     |
|   |   +-- Read model_config from CLI                              |
|   |   +-- Pass to each agent invocation                           |
|   |                                                               |
|   +-- Task Tool Invocation                                        |
|       +-- model parameter set per agent                           |
|       +-- Example: Task(model="opus", prompt=...)                 |
|                                                                   |
+-------------------------------------------------------------------+
```

### Critical Unknown: Task Tool Model Parameter

The Task tool has a `model` parameter per the tool schema:

```yaml
"model": {
  "description": "Optional model to use for this agent...",
  "enum": ["sonnet", "opus", "haiku"],
  "type": "string"
}
```

**Validation Required:** Confirm Task tool model parameter works as expected.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| TASK-419 | Validate Task tool model parameter | pending | 2h | Claude |
| TASK-420 | Add CLI parameters for model selection | pending | 8h | Claude |
| TASK-421 | Update SKILL.md model documentation | pending | 4h | Claude |
| TASK-422 | Update agent definitions with model override | pending | 4h | Claude |
| TASK-423 | Implement model profiles | pending | 8h | Claude |
| TASK-424 | Integration testing with different models | pending | 8h | Claude |

### Task Links

- [TASK-419: Validate Task tool model parameter](./TASK-419-validate-task-model.md)
- [TASK-420: Add CLI model parameters](./TASK-420-add-cli-model-params.md)
- [TASK-421: Update SKILL.md model documentation](./TASK-421-update-skill-model-docs.md)
- [TASK-422: Update agent definitions](./TASK-422-update-agent-definitions.md)
- [TASK-423: Implement model profiles](./TASK-423-implement-profiles.md)
- [TASK-424: Integration testing](./TASK-424-integration-testing.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)             |
| Effort:    [....................] 0% (0/34 hours completed)      |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 0 |
| **Total Effort (hours)** | 34 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] CLI accepts --model-* parameters for all agents
- [ ] Default behavior unchanged (current model assignments)
- [ ] SKILL.md documents model configuration
- [ ] Model profiles implemented (economy, balanced, quality)
- [ ] Integration tests pass with different model combinations

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | `--model-parser` accepts opus, sonnet, haiku | [ ] |
| TC-2 | `--model-extractor` accepts opus, sonnet, haiku | [ ] |
| TC-3 | `--model-formatter` accepts opus, sonnet, haiku | [ ] |
| TC-4 | `--model-mindmap` accepts opus, sonnet, haiku | [ ] |
| TC-5 | `--model-critic` accepts opus, sonnet, haiku | [ ] |
| TC-6 | `--profile` accepts economy, balanced, quality | [ ] |
| TC-7 | Task tool correctly uses specified model | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| CLI implementation | Code | Model parameter handling | src/interface/cli/ |
| SKILL.md v2.5.0 | Documentation | Model configuration docs | skills/transcript/SKILL.md |
| Test results | Report | Integration test results | test_data/validation/ |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All tasks completed
- [ ] Integration tests pass

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Task tool model param doesn't work | Medium | Critical | TASK-419 validates early; escalate if blocked |
| Quality degradation with haiku | Medium | High | Document quality tradeoffs; recommend sonnet for extractions |
| User confusion with options | Low | Medium | Profiles simplify common use cases |

---

## Cost Analysis

From [work-025-e-001](../../../../../docs/analysis/work-025-e-001-model-selection-effort.md):

| Configuration | Cost per 10K tokens (input) | Savings vs Current |
|---------------|----------------------------|-------------------|
| Current (mixed) | ~$0.12 | - |
| All haiku | ~$0.015 | 88% |
| All sonnet | ~$0.15 | -25% |
| All opus | ~$0.75 | -525% |

**Recommendation:** Default to current (balanced), offer economy for bulk processing.

---

## Dependencies

### Depends On

- None (independent of Phase 1-4 remediation)

### Enables

- Cost-optimized transcript processing
- Quality tuning for high-value transcripts
- Model performance benchmarking

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-005: Skill Compliance](../FEAT-005-skill-compliance.md)

### Related Items

- **Analysis:** [work-025-e-001](../../../../../docs/analysis/work-025-e-001-model-selection-effort.md) - Detailed effort analysis
- **Task Tool Schema:** Claude Code documentation - model parameter

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-30T16:00:00Z | Claude | pending | Enabler created per user request and work-025-e-001 analysis. Independent of Phase 1-4. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (Infrastructure type) |
| **JIRA** | Story with 'enabler' label |

---

<!--
DESIGN RATIONALE:

Model selection is a new capability requested by user. Key considerations:

1. TASK TOOL VALIDATION CRITICAL
   - Task tool schema shows model param exists
   - Must validate it works before committing to implementation
   - TASK-419 addresses this risk early

2. BACKWARD COMPATIBILITY
   - Defaults match current hardcoded values
   - Existing workflows unchanged without explicit params

3. PROFILES FOR USABILITY
   - Most users want simple choices (cheap vs quality)
   - Named profiles abstract model details
   - Power users can override individual agents

4. INDEPENDENT OF COMPLIANCE
   - Can run in parallel with EN-027 through EN-030
   - No blockers from compliance work

TRACE:
- User request → work-025-e-001 analysis → This enabler
-->

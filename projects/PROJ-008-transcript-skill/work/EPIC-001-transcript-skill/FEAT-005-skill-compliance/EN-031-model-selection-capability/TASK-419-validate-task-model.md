# TASK-419: Validate Task tool model parameter

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-419"
work_type: TASK
title: "Validate Task tool model parameter"
status: BACKLOG
priority: CRITICAL
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-031"
effort: 2
activity: RESEARCH
```

---

## Description

Validate that the Task tool's `model` parameter works as expected before committing to full implementation. This is the critical unknown identified in work-025-e-001.

**Validation approach:**
1. Invoke Task tool with explicit model="haiku"
2. Verify the spawned agent uses haiku model
3. Test with model="opus" to confirm model switching works
4. Document any limitations or unexpected behavior

---

## Acceptance Criteria

- [ ] Task tool model parameter tested with haiku, sonnet, opus
- [ ] Confirm model parameter is respected by spawned agent
- [ ] Document any limitations discovered
- [ ] Go/No-Go decision made for EN-031 implementation

---

## Implementation Notes

**Test 1: Haiku model**

```python
Task(
    description="Test haiku model",
    subagent_type="general-purpose",
    model="haiku",
    prompt="Return the string 'Hello from haiku'"
)
```

Expected: Agent uses haiku model, returns "Hello from haiku"

**Test 2: Opus model**

```python
Task(
    description="Test opus model",
    subagent_type="general-purpose",
    model="opus",
    prompt="Return the string 'Hello from opus'"
)
```

Expected: Agent uses opus model, returns "Hello from opus"

**Test 3: Sonnet model (default)**

```python
Task(
    description="Test sonnet model",
    subagent_type="general-purpose",
    model="sonnet",
    prompt="Return the string 'Hello from sonnet'"
)
```

Expected: Agent uses sonnet model, returns "Hello from sonnet"

**Validation Questions:**
1. Does the model parameter actually change which model is used?
2. Are there any restrictions on model switching mid-session?
3. How can we verify which model was actually used?

---

## Related Items

- Parent: [EN-031: Model Selection Capability](./EN-031-model-selection-capability.md)
- Analysis: work-025-e-001 Section "Critical Unknown"

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Validation Report | Document | (To be created) |

### Verification

- [ ] All 3 models tested
- [ ] Go/No-Go decision documented
- [ ] Any limitations documented

---

## Risk Impact

**If validation FAILS:**
- EN-031 blocked or requires alternative approach
- May need to escalate to Anthropic support
- Fallback: Document as known limitation

**If validation SUCCEEDS:**
- Proceed with TASK-420 through TASK-424
- Model selection capability confirmed feasible

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Critical validation task for EN-031 |

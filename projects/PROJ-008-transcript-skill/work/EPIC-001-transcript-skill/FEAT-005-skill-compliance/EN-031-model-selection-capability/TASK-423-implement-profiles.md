# TASK-423: Implement model profiles

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-423"
work_type: TASK
title: "Implement model profiles"
status: BACKLOG
priority: MEDIUM
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-031"
effort: 8
activity: DEVELOPMENT
```

---

## Description

Implement named model profiles (economy, balanced, quality) that provide pre-configured model selections for common use cases. This simplifies the CLI interface for most users.

**Files to modify:**
- src/interface/cli/commands/transcript.py
- skills/transcript/SKILL.md (documentation)

**Depends on:** TASK-420 (Add CLI model parameters)

---

## Acceptance Criteria

- [ ] `--profile economy` uses all haiku models
- [ ] `--profile balanced` uses default configuration
- [ ] `--profile quality` uses opus for extraction and critic
- [ ] Profile overrides individual `--model-*` params if both specified
- [ ] Profile configuration documented in SKILL.md

---

## Implementation Notes

### Profile Definitions

| Profile | Parser | Extractor | Formatter | Mindmap | Critic |
|---------|--------|-----------|-----------|---------|--------|
| economy | haiku | haiku | haiku | haiku | haiku |
| balanced | haiku | sonnet | sonnet | sonnet | sonnet |
| quality | haiku | opus | sonnet | sonnet | opus |

### CLI Usage

```bash
# Economy mode - 88% cost savings
uv run jerry transcript parse meeting.vtt --profile economy

# Balanced mode (default)
uv run jerry transcript parse meeting.vtt --profile balanced

# Quality mode - best extraction
uv run jerry transcript parse meeting.vtt --profile quality

# Profile + override: profile sets base, override modifies
uv run jerry transcript parse meeting.vtt --profile economy --model-extractor sonnet
```

### Implementation

```python
PROFILES = {
    "economy": ModelConfig(
        parser="haiku",
        extractor="haiku",
        formatter="haiku",
        mindmap="haiku",
        critic="haiku",
    ),
    "balanced": ModelConfig(
        parser="haiku",
        extractor="sonnet",
        formatter="sonnet",
        mindmap="sonnet",
        critic="sonnet",
    ),
    "quality": ModelConfig(
        parser="haiku",
        extractor="opus",
        formatter="sonnet",
        mindmap="sonnet",
        critic="opus",
    ),
}

def resolve_model_config(profile: str | None, overrides: dict) -> ModelConfig:
    """Resolve final model config from profile and individual overrides."""
    if profile:
        config = PROFILES.get(profile, PROFILES["balanced"])
    else:
        config = PROFILES["balanced"]

    # Apply individual overrides
    if overrides.get("parser"):
        config.parser = overrides["parser"]
    if overrides.get("extractor"):
        config.extractor = overrides["extractor"]
    # ... etc

    return config
```

### Cost Impact

| Profile | Est. Cost/10K tokens | vs Balanced |
|---------|---------------------|-------------|
| economy | ~$0.015 | -88% |
| balanced | ~$0.12 | baseline |
| quality | ~$0.35 | +192% |

---

## Related Items

- Parent: [EN-031: Model Selection Capability](./EN-031-model-selection-capability.md)
- Depends on: TASK-420 (Add CLI model parameters)
- Related: TASK-421 (Update documentation)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Profile implementation | Code | src/interface/cli/ |
| Unit tests | Tests | tests/unit/cli/ |

### Verification

- [ ] All 3 profiles work correctly
- [ ] Profile + override works
- [ ] Default is balanced
- [ ] Documentation updated

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-031 |

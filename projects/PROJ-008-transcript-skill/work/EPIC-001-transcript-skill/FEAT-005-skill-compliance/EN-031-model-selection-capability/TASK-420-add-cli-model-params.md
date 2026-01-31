# TASK-420: Add CLI parameters for model selection

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-420"
work_type: TASK
title: "Add CLI parameters for model selection"
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

Add `--model-*` CLI parameters for each transcript skill agent to the `jerry transcript parse` command. This enables users to specify which Claude model (opus, sonnet, haiku) to use for each agent.

**Files to modify:**
- src/interface/cli/commands/transcript.py (or equivalent)
- CLI argument parsing logic

**Depends on:** TASK-419 (Validate Task tool model parameter)

---

## Acceptance Criteria

- [ ] `--model-parser` parameter accepts opus|sonnet|haiku (default: haiku)
- [ ] `--model-extractor` parameter accepts opus|sonnet|haiku (default: sonnet)
- [ ] `--model-formatter` parameter accepts opus|sonnet|haiku (default: sonnet)
- [ ] `--model-mindmap` parameter accepts opus|sonnet|haiku (default: sonnet)
- [ ] `--model-critic` parameter accepts opus|sonnet|haiku (default: sonnet)
- [ ] Invalid model values produce clear error message
- [ ] `--help` shows all model parameters with descriptions

---

## Implementation Notes

### CLI Parameter Design

```bash
# Full example with all parameters
uv run jerry transcript parse meeting.vtt \
    --model-parser haiku \
    --model-extractor sonnet \
    --model-formatter haiku \
    --model-mindmap haiku \
    --model-critic sonnet

# Use defaults (current behavior)
uv run jerry transcript parse meeting.vtt
```

### Default Values (Preserve Current Behavior)

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| --model-parser | haiku | Orchestration only, no extraction |
| --model-extractor | sonnet | Semantic extraction requires quality |
| --model-formatter | sonnet | Formatting quality matters |
| --model-mindmap | sonnet | Topic organization needs reasoning |
| --model-critic | sonnet | Quality evaluation needs accuracy |

### Argument Parser Addition

```python
# Using argparse or click
parser.add_argument(
    "--model-parser",
    choices=["opus", "sonnet", "haiku"],
    default="haiku",
    help="Model for ts-parser agent (default: haiku)"
)
parser.add_argument(
    "--model-extractor",
    choices=["opus", "sonnet", "haiku"],
    default="sonnet",
    help="Model for ts-extractor agent (default: sonnet)"
)
# ... similar for formatter, mindmap, critic
```

### Model Config Object

```python
@dataclass
class ModelConfig:
    parser: str = "haiku"
    extractor: str = "sonnet"
    formatter: str = "sonnet"
    mindmap: str = "sonnet"
    critic: str = "sonnet"

    def to_dict(self) -> dict:
        return {
            "ts-parser": self.parser,
            "ts-extractor": self.extractor,
            "ts-formatter": self.formatter,
            "ts-mindmap-mermaid": self.mindmap,
            "ts-mindmap-ascii": self.mindmap,
            "ps-critic": self.critic,
        }
```

---

## Related Items

- Parent: [EN-031: Model Selection Capability](./EN-031-model-selection-capability.md)
- Depends on: TASK-419 (Validate Task tool model parameter)
- Enables: TASK-421, TASK-423

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| CLI implementation | Code | src/interface/cli/ |
| Unit tests | Tests | tests/unit/cli/ |

### Verification

- [ ] All 5 model parameters work
- [ ] Defaults match current behavior
- [ ] Invalid values produce error
- [ ] `jerry transcript parse --help` shows parameters

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-031 |

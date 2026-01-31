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
status: DONE
priority: MEDIUM
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
completed_at: "2026-01-30T17:30:00Z"
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

- [x] `--model-parser` parameter accepts opus|sonnet|haiku (default: haiku)
- [x] `--model-extractor` parameter accepts opus|sonnet|haiku (default: sonnet)
- [x] `--model-formatter` parameter accepts opus|sonnet|haiku (default: sonnet)
- [x] `--model-mindmap` parameter accepts opus|sonnet|haiku (default: sonnet)
- [x] `--model-critic` parameter accepts opus|sonnet|haiku (default: sonnet)
- [x] Invalid model values produce clear error message
- [x] `--help` shows all model parameters with descriptions

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
| ModelConfig value object | Code | src/transcript/domain/value_objects/model_config.py |
| CLI parser updates | Code | src/interface/cli/parser.py |
| CLI main routing | Code | src/interface/cli/main.py |
| CLI adapter updates | Code | src/interface/cli/adapter.py |
| ParseTranscriptCommand updates | Code | src/transcript/application/commands/parse_transcript_command.py |
| ModelConfig unit tests | Tests | tests/unit/transcript/domain/value_objects/test_model_config.py |
| CLI parameter tests | Tests | tests/interface/cli/unit/test_model_parameters.py |

### Verification

- [x] All 5 model parameters work (29 tests pass)
- [x] Defaults match current behavior (haiku for parser, sonnet for others)
- [x] Invalid values produce error (argparse validation + ModelConfig validation)
- [x] `jerry transcript parse --help` shows parameters (verified manually + test)

### Test Results

```
# ModelConfig value object tests
tests/unit/transcript/domain/value_objects/test_model_config.py::15 tests PASSED

# CLI parameter tests
tests/interface/cli/unit/test_model_parameters.py::29 tests PASSED
```

---

## Cross-Pollination (CP-3 Output)

### CLI Parameter Design

**Exact Flag Syntax:**
```bash
--model-parser {opus|sonnet|haiku}      # ts-parser agent (default: haiku)
--model-extractor {opus|sonnet|haiku}   # ts-extractor agent (default: sonnet)
--model-formatter {opus|sonnet|haiku}   # ts-formatter agent (default: sonnet)
--model-mindmap {opus|sonnet|haiku}     # ts-mindmap-* agents (default: sonnet)
--model-critic {opus|sonnet|haiku}      # ps-critic agent (default: sonnet)
```

**Validation Rules:**
1. **argparse level**: `choices=["opus", "sonnet", "haiku"]` enforces valid values at parse time
2. **ModelConfig level**: `__post_init__` validation provides domain-level enforcement
3. **Error handling**: Invalid values trigger SystemExit with clear error message from argparse

**Default Behavior:**
- If no `--model-*` flags provided, defaults are used (matches TASK-419 recommendations)
- Defaults preserve current behavior (haiku for orchestration, sonnet for semantic work)
- Flags can be mixed (e.g., only override extractor with `--model-extractor opus`)

**Implementation Details:**
- `ModelConfig` is a frozen dataclass with validation
- `to_dict()` method maps friendly names to agent IDs
- Both mindmap agents (`ts-mindmap-mermaid`, `ts-mindmap-ascii`) use same `--model-mindmap` value
- Model values are simple strings (no provider prefix needed per TASK-419)

**Example Usage:**
```bash
# Use defaults
uv run jerry transcript parse meeting.vtt

# Override extraction with opus (higher quality)
uv run jerry transcript parse meeting.vtt --model-extractor opus

# Use haiku for everything (lower cost)
uv run jerry transcript parse meeting.vtt \
    --model-parser haiku \
    --model-extractor haiku \
    --model-formatter haiku \
    --model-mindmap haiku \
    --model-critic haiku
```

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-031 |
| 2026-01-30 | DONE | Implemented CLI parameters, ModelConfig, tests (44/44 pass) |

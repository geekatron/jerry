# TASK-420 Cross-Pollination Output (CP-3)

> **For consumption by:** TASK-421 (SKILL.md documentation), EN-028 (Agent integration)
> **Created:** 2026-01-30
> **Status:** COMPLETE

---

## CLI Parameter Specification

### Flags

| Flag | Values | Default | Agent(s) |
|------|--------|---------|----------|
| `--model-parser` | opus\|sonnet\|haiku | haiku | ts-parser |
| `--model-extractor` | opus\|sonnet\|haiku | sonnet | ts-extractor |
| `--model-formatter` | opus\|sonnet\|haiku | sonnet | ts-formatter |
| `--model-mindmap` | opus\|sonnet\|haiku | sonnet | ts-mindmap-mermaid, ts-mindmap-ascii |
| `--model-critic` | opus\|sonnet\|haiku | sonnet | ps-critic |

### Validation

**At Parse Time (argparse):**
- `choices=["opus", "sonnet", "haiku"]` enforces valid values
- Invalid values trigger immediate error with message:
  ```
  error: argument --model-{agent}: invalid choice: 'xxx' (choose from opus, sonnet, haiku)
  ```

**At Domain Level (ModelConfig):**
- `ModelConfig.__post_init__()` validates all fields
- Raises `ValueError` with descriptive message if invalid
- Example: `"Invalid model for parser: 'gpt-4'. Must be one of: haiku, opus, sonnet"`

### Default Behavior

**When no flags provided:**
- System uses recommended defaults from TASK-419
- Preserves current behavior (backward compatible)

**When partial flags provided:**
- Only specified models are overridden
- Unspecified agents use defaults
- Example: `--model-extractor opus` only changes extractor, others remain default

### Usage Examples

```bash
# 1. Use all defaults (recommended for most use cases)
uv run jerry transcript parse meeting.vtt

# 2. Override extractor for higher quality (cost trade-off)
uv run jerry transcript parse meeting.vtt --model-extractor opus

# 3. Use haiku for everything (lower cost, faster)
uv run jerry transcript parse meeting.vtt \
    --model-parser haiku \
    --model-extractor haiku \
    --model-formatter haiku \
    --model-mindmap haiku \
    --model-critic haiku

# 4. Mixed optimization (balance cost and quality)
uv run jerry transcript parse meeting.vtt \
    --model-parser haiku \
    --model-extractor opus \
    --model-formatter haiku \
    --model-mindmap sonnet \
    --model-critic sonnet
```

---

## Implementation Details

### ModelConfig Value Object

**Location:** `src/transcript/domain/value_objects/model_config.py`

**Design:**
- Frozen dataclass (immutable)
- Self-validating in `__post_init__`
- Provides `to_dict()` for agent name mapping

**Agent Mapping:**
```python
{
    "ts-parser": config.parser,
    "ts-extractor": config.extractor,
    "ts-formatter": config.formatter,
    "ts-mindmap-mermaid": config.mindmap,  # Shared value
    "ts-mindmap-ascii": config.mindmap,     # Shared value
    "ps-critic": config.critic,
}
```

### Command Flow

1. **CLI Parser** (`parser.py`) → Parses `--model-*` flags
2. **Main Router** (`main.py`) → Extracts model values from args
3. **CLI Adapter** (`adapter.py`) → Creates `ModelConfig` instance
4. **ParseTranscriptCommand** → Carries `model_config` to handler
5. **Handler** → Uses `model_config.to_dict()` to configure agents

### Type Safety

**Command Definition:**
```python
@dataclass(frozen=True)
class ParseTranscriptCommand:
    path: str
    format: str = "auto"
    output_dir: str | None = None
    chunk_size: int = 500
    target_tokens: int | None = 18000
    generate_chunks: bool = True
    model_config: ModelConfig | None = None  # Optional, defaults applied if None
```

**Adapter Signature:**
```python
def cmd_transcript_parse(
    self,
    path: str,
    format: str = "auto",
    output_dir: str | None = None,
    chunk_size: int = 500,
    target_tokens: int | None = 18000,
    generate_chunks: bool = True,
    model_parser: str = "haiku",
    model_extractor: str = "sonnet",
    model_formatter: str = "sonnet",
    model_mindmap: str = "sonnet",
    model_critic: str = "sonnet",
    json_output: bool = False,
) -> int:
```

---

## Testing Coverage

### Unit Tests

**ModelConfig (15 tests):**
- Default values
- Custom values
- Immutability
- Validation (all 5 fields)
- to_dict() mapping
- Equality/hashing

**CLI Parameters (29 tests):**
- Default parsing
- Custom values (all 5 flags)
- Invalid value rejection (all 5 flags)
- Valid choices (3 models × 5 flags = 15 parameterized tests)
- Help text verification

**Results:**
```
tests/unit/transcript/domain/value_objects/test_model_config.py::15 PASSED
tests/interface/cli/unit/test_model_parameters.py::29 PASSED
```

---

## Documentation for TASK-421

### SKILL.md Section

```markdown
## Model Selection (Advanced)

Control which Claude model is used for each agent in the pipeline:

| Parameter | Agent | Default | Use Case |
|-----------|-------|---------|----------|
| `--model-parser` | ts-parser | haiku | Orchestration (low cost) |
| `--model-extractor` | ts-extractor | sonnet | Semantic extraction (quality) |
| `--model-formatter` | ts-formatter | sonnet | Output formatting (quality) |
| `--model-mindmap` | ts-mindmap-* | sonnet | Topic organization (reasoning) |
| `--model-critic` | ps-critic | sonnet | Quality validation (accuracy) |

**Example - Higher Quality Extraction:**
```bash
/transcript meeting.vtt --model-extractor opus
```

**Example - Lower Cost Processing:**
```bash
/transcript meeting.vtt \
    --model-parser haiku \
    --model-extractor haiku \
    --model-formatter haiku \
    --model-mindmap haiku \
    --model-critic haiku
```
```

### CLI Help Output (Already Implemented)

When users run `jerry transcript parse --help`, they see:
```
--model-parser {opus,sonnet,haiku}
                      Model for ts-parser agent (default: haiku)
--model-extractor {opus,sonnet,haiku}
                      Model for ts-extractor agent (default: sonnet)
--model-formatter {opus,sonnet,haiku}
                      Model for ts-formatter agent (default: sonnet)
--model-mindmap {opus,sonnet,haiku}
                      Model for ts-mindmap-* agents (default: sonnet)
--model-critic {opus,sonnet,haiku}
                      Model for ps-critic agent (default: sonnet)
```

---

## Integration Notes for EN-028

1. **Agent Invocation:** Use `model_config.to_dict()` to get agent-to-model mapping
2. **Task Tool:** Pass model value directly to `model` parameter (e.g., `model: "opus"`)
3. **No Provider Prefix:** Use simple strings (`"opus"`, not `"anthropic:opus"`)
4. **Fallback:** If `model_config` is None, use hardcoded defaults (haiku, sonnet, sonnet, sonnet, sonnet)

---

## References

- **TASK-419:** Model parameter validation (simple string syntax confirmed)
- **TASK-420:** This task (CLI parameter implementation)
- **TASK-421:** SKILL.md documentation (consumes this CP-3 output)
- **EN-028:** Agent-based pipeline (will use ModelConfig.to_dict())

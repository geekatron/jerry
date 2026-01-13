# Fan-In Synthesis Architecture

**Document ID:** ARCH-PS-ORCH-002-E003
**Date:** 2026-01-11
**Author:** ps-architect v2.1.0
**Context:** PS-ORCH-002 Fan-In Architecture Design

---

## L0: Executive Summary

Fan-in synthesis is the aggregation phase of a fan-out/fan-in orchestration pattern where multiple parallel agent outputs are collected, validated, and synthesized into a coherent whole. This architecture defines the component structure, interfaces, and error handling strategy for Jerry's fan-in layer.

**Key Design Decisions:**
1. **Aggregator-Synthesizer Split:** Separate collection from synthesis for clarity
2. **Payload Protocol:** Standardized `session_context` YAML blocks for agent interop
3. **Partial Failure Tolerance:** Best-effort synthesis with degradation signals

---

## L1: Architecture Overview

### Component Model

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR LAYER                        │
│  (ps-orchestrator, skill: orchestration)                    │
└────────────┬───────────────────────────────────┬────────────┘
             │ Fan-Out                            │ Fan-In
             ▼                                    ▲
    ┌────────────────┐                   ┌───────┴────────┐
    │  FAN-OUT SPEC  │                   │  AGGREGATOR    │
    │  (routing cfg) │                   │  (collector)   │
    └────────┬───────┘                   └───────┬────────┘
             │                                    │
             ▼                                    │
    ┌────────────────────────────┐              │
    │   PARALLEL WORKERS         │              │
    │  ┌─────────┐  ┌─────────┐ │              │
    │  │Agent-1  │  │Agent-2  │ │──────────────┘
    │  │(e-001)  │  │(e-002)  │ │  writes artifacts
    │  └─────────┘  └─────────┘ │  w/ session_context
    │  ┌─────────┐               │
    │  │Agent-N  │               │
    │  │(e-NNN)  │               │
    │  └─────────┘               │
    └────────────────────────────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │  SYNTHESIZER   │
                        │  (reducer)     │
                        └────────┬───────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │  FINAL OUTPUT  │
                        │  (coherent doc)│
                        └────────────────┘
```

### Aggregator Component

**Purpose:** Collect artifacts from fan-out workers and extract payloads.

**Responsibilities:**
- Discover output artifacts by glob pattern or manifest
- Parse `session_context` YAML blocks from each artifact
- Validate schema conformance
- Handle missing/malformed outputs (partial failure)
- Produce aggregation report for synthesizer

**Interface:**

```python
class IAggregator(Protocol):
    """Port for fan-in aggregation."""

    def collect_artifacts(
        self,
        session_id: str,
        manifest_path: Path | None = None
    ) -> AggregationResult:
        """Collect artifacts from fan-out workers.

        Args:
            session_id: The orchestration session ID
            manifest_path: Optional path to manifest file listing expected outputs

        Returns:
            AggregationResult with collected payloads and error summary
        """
        ...
```

**Data Structures:**

```python
@dataclass(frozen=True)
class SessionContext:
    """Parsed session_context payload from worker artifact."""
    schema_version: str
    session_id: str
    source_agent: AgentInfo
    target_agent: AgentInfo | None
    payload: dict[str, Any]
    source_file: Path

@dataclass(frozen=True)
class AgentInfo:
    """Agent identification."""
    id: str
    family: str
    version: str | None = None

@dataclass(frozen=True)
class AggregationResult:
    """Output of aggregation phase."""
    session_id: str
    collected: list[SessionContext]
    failed: list[AggregationError]
    coverage: float  # 0.0-1.0, proportion of expected artifacts collected
```

### Synthesizer Component

**Purpose:** Reduce aggregated payloads into coherent final output.

**Responsibilities:**
- Analyze collected payloads for themes, conflicts, gaps
- Apply synthesis strategy (merge, rank, vote, LLM-reduce)
- Generate final artifact with traceable provenance
- Signal degradation if partial failure threshold exceeded

**Interface:**

```python
class ISynthesizer(Protocol):
    """Port for fan-in synthesis."""

    def synthesize(
        self,
        aggregation: AggregationResult,
        strategy: SynthesisStrategy,
        output_path: Path
    ) -> SynthesisResult:
        """Synthesize aggregated payloads into final output.

        Args:
            aggregation: Collected payloads from aggregator
            strategy: How to combine payloads (merge, rank, vote, llm_reduce)
            output_path: Where to write synthesized artifact

        Returns:
            SynthesisResult with provenance and quality metrics
        """
        ...
```

**Data Structures:**

```python
class SynthesisStrategy(Enum):
    """Synthesis approach."""
    MERGE = "merge"  # Concatenate all payloads
    RANK = "rank"    # Priority-weighted selection
    VOTE = "vote"    # Majority consensus
    LLM_REDUCE = "llm_reduce"  # LLM-based summarization

@dataclass(frozen=True)
class SynthesisResult:
    """Output of synthesis phase."""
    session_id: str
    output_path: Path
    strategy_used: SynthesisStrategy
    sources: list[Path]  # Input artifacts
    coverage: float
    degraded: bool  # True if partial failure exceeded threshold
    quality_score: float | None = None
```

---

## L2: Detailed Design

### 1. Aggregator Implementation

**Algorithm:**

```
1. Discover artifacts:
   IF manifest_path provided:
       expected_files = parse_manifest(manifest_path)
   ELSE:
       expected_files = glob(f"{session_id}/**/*.md")

2. For each artifact:
   a. Read file content
   b. Extract session_context YAML block (regex: ```yaml\nsession_context:.*?```)
   c. Validate schema (schema_version, session_id, source_agent, payload)
   d. Parse into SessionContext object
   e. ON ERROR: append to failed list, continue

3. Compute coverage = len(collected) / len(expected_files)

4. Return AggregationResult
```

**Error Handling:**

| Error Scenario | Behavior |
|----------------|----------|
| Missing file | Log warning, add to `failed`, continue |
| Malformed YAML | Log error, add to `failed`, continue |
| Schema violation | Log error, add to `failed`, continue |
| No artifacts found | Return AggregationResult with coverage=0.0 |

**Filesystem Adapter:**

```python
class FilesystemAggregator:
    """Concrete implementation of IAggregator for filesystem artifacts."""

    def __init__(self, base_path: Path):
        self._base_path = base_path
        self._logger = logging.getLogger(__name__)

    def collect_artifacts(
        self,
        session_id: str,
        manifest_path: Path | None = None
    ) -> AggregationResult:
        expected = self._discover_expected(session_id, manifest_path)
        collected: list[SessionContext] = []
        failed: list[AggregationError] = []

        for artifact_path in expected:
            try:
                ctx = self._parse_artifact(artifact_path)
                if ctx.session_id != session_id:
                    raise ValueError(f"Session ID mismatch: {ctx.session_id} != {session_id}")
                collected.append(ctx)
            except Exception as e:
                self._logger.error(f"Failed to parse {artifact_path}: {e}")
                failed.append(AggregationError(
                    artifact_path=artifact_path,
                    error_type=type(e).__name__,
                    error_msg=str(e)
                ))

        coverage = len(collected) / len(expected) if expected else 0.0
        return AggregationResult(
            session_id=session_id,
            collected=collected,
            failed=failed,
            coverage=coverage
        )
```

### 2. Synthesizer Implementation

**Strategy: MERGE**

Concatenate all payloads with section headers:

```markdown
# Synthesized Output: {session_id}

## Source: {agent-1}
{payload content}

## Source: {agent-2}
{payload content}

---
**Provenance:**
- Sources: [path1, path2, ...]
- Coverage: 0.85
```

**Strategy: RANK**

Select top-N payloads by priority (assumes `priority` key in payload):

```python
def synthesize_rank(collected: list[SessionContext], top_n: int) -> str:
    ranked = sorted(
        collected,
        key=lambda ctx: ctx.payload.get("priority", 0),
        reverse=True
    )
    return merge(ranked[:top_n])
```

**Strategy: VOTE**

Extract `key_findings` from each payload, count occurrences, take consensus:

```python
def synthesize_vote(collected: list[SessionContext]) -> str:
    findings_counter: Counter[str] = Counter()
    for ctx in collected:
        findings = ctx.payload.get("key_findings", [])
        findings_counter.update(findings)

    consensus = findings_counter.most_common(5)
    return format_consensus(consensus)
```

**Strategy: LLM_REDUCE**

Use LLM to summarize all payloads (requires LLM adapter):

```python
def synthesize_llm_reduce(
    collected: list[SessionContext],
    llm_client: ILLMClient
) -> str:
    combined_text = "\n\n".join(
        f"# {ctx.source_agent.id}\n{ctx.payload}"
        for ctx in collected
    )

    prompt = f"""
    Synthesize the following agent outputs into a coherent summary.
    Preserve key findings and identify conflicts or gaps.

    {combined_text}
    """

    return llm_client.generate(prompt)
```

**Degradation Logic:**

```python
DEGRADATION_THRESHOLD = 0.7  # 70% coverage minimum

def is_degraded(aggregation: AggregationResult) -> bool:
    return aggregation.coverage < DEGRADATION_THRESHOLD
```

### 3. Orchestration Flow

**Step 1: Fan-Out (orchestrator)**
```python
# In orchestration skill or ps-orchestrator
fan_out_spec = FanOutSpec(
    session_id="ps-orch-002-test",
    tasks=[
        Task(entry_id="e-001", agent="ps-critic", topic="..."),
        Task(entry_id="e-002", agent="ps-researcher", topic="..."),
        Task(entry_id="e-003", agent="ps-architect", topic="..."),
    ],
    output_dir=Path("projects/.../tests/ps-orchestration-results/PS-ORCH-002")
)

dispatcher.dispatch(fan_out_spec)
```

**Step 2: Fan-In (aggregator)**
```python
aggregator = FilesystemAggregator(base_path=fan_out_spec.output_dir)
aggregation = aggregator.collect_artifacts(
    session_id="ps-orch-002-test",
    manifest_path=fan_out_spec.output_dir / "manifest.yaml"
)

print(f"Coverage: {aggregation.coverage:.1%}")
print(f"Collected: {len(aggregation.collected)}")
print(f"Failed: {len(aggregation.failed)}")
```

**Step 3: Synthesis (synthesizer)**
```python
synthesizer = Synthesizer()
result = synthesizer.synthesize(
    aggregation=aggregation,
    strategy=SynthesisStrategy.MERGE,
    output_path=fan_out_spec.output_dir / "synthesis.md"
)

if result.degraded:
    print(f"⚠️  Synthesis degraded (coverage: {result.coverage:.1%})")
else:
    print(f"✓ Synthesis complete: {result.output_path}")
```

### 4. Session Context Protocol

**Schema Version 1.0.0:**

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "<orchestration-session-id>"
  source_agent:
    id: "<agent-id>"
    family: "<agent-family>"
    version: "<agent-version>"  # optional
  target_agent:  # optional, for directed handoffs
    id: "<target-agent-id>"
    family: "<target-family>"
  payload:
    # Agent-specific structured data
    key_findings: ["finding 1", "finding 2"]
    artifacts:
      - path: "relative/path/to/artifact.md"
        type: "architecture|research|critique|..."
    # Additional keys as needed
```

**Validation Rules:**
1. `schema_version` MUST be "1.0.0"
2. `session_id` MUST match orchestration session
3. `source_agent.id` MUST be valid agent identifier
4. `payload` MUST be present (can be empty dict)

**Placement in Artifacts:**
- MUST be at end of file (after all content)
- MUST be in fenced YAML code block with `session_context:` key
- MUST NOT have additional content after the code block (except trailing newline)

### 5. Error Handling Matrix

| Failure Scenario | Aggregator Behavior | Synthesizer Behavior | Orchestrator Action |
|------------------|---------------------|----------------------|---------------------|
| 1 of 3 agents fails | Collect 2, coverage=0.67, degraded=true | Synthesize with 2 sources, flag degraded | Log warning, proceed |
| 2 of 3 agents fail | Collect 1, coverage=0.33, degraded=true | Abort synthesis (below threshold) | Raise error, notify user |
| All agents fail | Collect 0, coverage=0.0 | Abort synthesis | Raise error, notify user |
| Malformed YAML in 1 | Parse error → failed list | Synthesize with remaining | Log error, proceed |
| Session ID mismatch | Validation error → failed list | Synthesize with remaining | Log error, proceed |
| Missing expected file | File not found → failed list | Synthesize with remaining | Log warning, proceed |
| LLM synthesis fails | N/A | Fall back to MERGE strategy | Log error, proceed with fallback |

**Threshold Configuration:**

```python
# In orchestration config
class OrchestrationConfig:
    min_coverage: float = 0.7  # Minimum % of expected outputs
    synthesis_fallback: SynthesisStrategy = SynthesisStrategy.MERGE
    abort_on_degradation: bool = False  # If True, fail fast
```

---

## ASCII Diagrams

### Fan-In Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT ARTIFACTS                          │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────┐│
│  │ e-001-critique.md│ │ e-002-research.md│ │ e-003-arch.md││
│  ├──────────────────┤ ├──────────────────┤ ├──────────────┤│
│  │ Content...       │ │ Content...       │ │ Content...   ││
│  │ ```yaml          │ │ ```yaml          │ │ ```yaml      ││
│  │ session_context: │ │ session_context: │ │ session_ctx: ││
│  │   session_id: X  │ │   session_id: X  │ │   session: X ││
│  │   source: critic │ │   source: res... │ │   source: a..││
│  │   payload: {...} │ │   payload: {...} │ │   payload:{} ││
│  │ ```              │ │ ```              │ │ ```          ││
│  └──────────────────┘ └──────────────────┘ └──────────────┘│
└────────────┬─────────────────┬──────────────────┬───────────┘
             │                 │                  │
             ▼                 ▼                  ▼
        ┌────────────────────────────────────────────┐
        │           AGGREGATOR COMPONENT             │
        │  ┌──────────────────────────────────────┐ │
        │  │ 1. Discover artifacts (glob/manifest)│ │
        │  │ 2. Parse session_context YAML blocks │ │
        │  │ 3. Validate schema                   │ │
        │  │ 4. Collect payloads                  │ │
        │  │ 5. Handle errors → failed list       │ │
        │  │ 6. Compute coverage                  │ │
        │  └──────────────────────────────────────┘ │
        └────────────────────┬───────────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ AggregationResult    │
                  ├──────────────────────┤
                  │ collected: [ctx1,    │
                  │            ctx2,     │
                  │            ctx3]     │
                  │ failed: []           │
                  │ coverage: 1.0        │
                  └──────────┬───────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │          SYNTHESIZER COMPONENT             │
        │  ┌──────────────────────────────────────┐ │
        │  │ 1. Select strategy (merge/rank/vote) │ │
        │  │ 2. Apply synthesis algorithm         │ │
        │  │ 3. Check degradation threshold       │ │
        │  │ 4. Generate output with provenance   │ │
        │  └──────────────────────────────────────┘ │
        └────────────────────┬───────────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  FINAL OUTPUT        │
                  │  synthesis.md        │
                  ├──────────────────────┤
                  │ # Synthesis          │
                  │ ## From ps-critic    │
                  │ ...                  │
                  │ ## From ps-researcher│
                  │ ...                  │
                  │ ---                  │
                  │ Provenance: [...]    │
                  │ Coverage: 1.0        │
                  └──────────────────────┘
```

### Partial Failure Scenario

```
Fan-Out: 3 agents → [A, B, C]
         ↓
Execution:
  Agent A ✓ (writes artifact-A.md)
  Agent B ✗ (crashes, no output)
  Agent C ✓ (writes artifact-C.md)
         ↓
Aggregation:
  Discover: [artifact-A.md, artifact-C.md]
  Expected: [artifact-A.md, artifact-B.md, artifact-C.md]
  Parse A: ✓ → collected
  Parse B: ✗ → failed (file not found)
  Parse C: ✓ → collected
  Coverage: 2/3 = 0.67 → DEGRADED (< 0.7 threshold)
         ↓
Synthesis:
  Strategy: MERGE
  Input: [A, C]
  Output: synthesis.md (flagged degraded=true)
         ↓
Orchestrator:
  Log: "⚠️  Fan-in synthesis degraded (67% coverage)"
  Action: Notify user, optionally retry Agent B
```

---

## Implementation Checklist

### Phase 1: Core Components
- [ ] Define `IAggregator` port in `src/domain/ports/`
- [ ] Define `ISynthesizer` port in `src/domain/ports/`
- [ ] Implement `FilesystemAggregator` in `src/infrastructure/adapters/`
- [ ] Implement `Synthesizer` (MERGE strategy) in `src/application/services/`
- [ ] Define data structures (`SessionContext`, `AggregationResult`, etc.) in `src/domain/value_objects/`

### Phase 2: Synthesis Strategies
- [ ] Implement `SynthesisStrategy.RANK`
- [ ] Implement `SynthesisStrategy.VOTE`
- [ ] Implement `SynthesisStrategy.LLM_REDUCE` (requires LLM adapter)

### Phase 3: Integration
- [ ] Add fan-in orchestration to `orchestration` skill
- [ ] Update `ps-orchestrator` to call aggregator/synthesizer
- [ ] Add manifest generation to fan-out dispatcher
- [ ] Create `OrchestrationConfig` for thresholds

### Phase 4: Testing
- [ ] Unit tests for `FilesystemAggregator` (happy path, partial failure, full failure)
- [ ] Unit tests for `Synthesizer` (all strategies)
- [ ] Integration test: 3-agent fan-out → fan-in
- [ ] E2E test: PS-ORCH-002 (full pipeline)

### Phase 5: Documentation
- [ ] Add fan-in section to `skills/orchestration/PLAYBOOK.md`
- [ ] Document session_context protocol in `docs/design/`
- [ ] Add error handling guide to `docs/wisdom/`

---

## References

1. **MapReduce Pattern** - Dean & Ghemawat (2004) - Google's distributed reduce model
2. **Scatter-Gather Pattern** - Hohpe & Woolf, _Enterprise Integration Patterns_ (2003)
3. **Hexagonal Architecture** - Alistair Cockburn - Ports & Adapters for testability
4. **CQRS Pattern** - Greg Young - Command/Query separation (aggregation is a query)
5. **Circuit Breaker Pattern** - Michael Nygard, _Release It!_ (2007) - Degradation handling

---

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "ps-orch-002-test"
  source_agent:
    id: "ps-architect"
    family: "ps"
    version: "2.1.0"
  target_agent:
    id: "ps-synthesizer"
    family: "ps"
  payload:
    key_findings:
      - "Fan-in requires Aggregator-Synthesizer component split for clarity"
      - "Session context protocol enables decoupled agent interop via YAML payloads"
      - "Partial failure tolerance achieved via coverage thresholds and degradation flags"
      - "Multiple synthesis strategies (MERGE, RANK, VOTE, LLM_REDUCE) support diverse use cases"
      - "Error handling matrix covers 7 failure scenarios with graceful degradation"
    artifacts:
      - path: "projects/PROJ-002-nasa-systems-engineering/tests/ps-orchestration-results/PS-ORCH-002/fanout-architecture.md"
        type: "architecture"
    components:
      - name: "IAggregator"
        type: "port"
        layer: "domain"
      - name: "FilesystemAggregator"
        type: "adapter"
        layer: "infrastructure"
      - name: "ISynthesizer"
        type: "port"
        layer: "domain"
      - name: "Synthesizer"
        type: "service"
        layer: "application"
    design_decisions:
      - id: "DD-001"
        decision: "Separate aggregation from synthesis"
        rationale: "Single Responsibility Principle - collection vs transformation"
      - id: "DD-002"
        decision: "Use session_context YAML protocol"
        rationale: "Language-agnostic, human-readable, schema-validatable"
      - id: "DD-003"
        decision: "Coverage threshold at 70%"
        rationale: "Balance between strict (100%) and permissive (50%) based on fault tolerance research"
      - id: "DD-004"
        decision: "Best-effort synthesis under partial failure"
        rationale: "Availability over consistency (CAP theorem) for non-critical orchestration"
```

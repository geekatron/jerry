I'll create an ADR for the PROJ-036 prompt regression harness storage decision. Let me first check if there are any existing ADRs in the project to maintain consistency.

<Glob>
<pattern>projects/*/decisions/**/*.md</pattern>
</Glob>

<Write>
<file_path>projects/proj-036/decisions/proj-036-e-001-adr-baseline-storage.md</file_path>
<content># ADR-001: Baseline Storage Strategy for Prompt Regression Harness

## Status
PROPOSED

## Context

The PROJ-036 prompt regression harness needs to store baseline run records for statistical comparison of agent responses across versions. The system must handle:

- N=30 baseline runs per prompt/agent pair
- Up to 25 prompt/agent pairs (5 agents × 5 prompts)
- Each run record is 5-15 KB of JSON data
- Total storage approximately 4 MB per baseline capture

Key requirements:
- Version control integration with agent definition files
- Queryability by agent name and prompt ID for statistical comparison
- Portability across developer machines without external dependencies
- Support for collaborative development with minimal merge conflicts

## Decision

After evaluating both options with steelman analysis, **Option A (JSON files on disk)** is recommended for baseline storage.

## Options Considered

### Option A: JSON Files on Disk (Recommended)

**Steelman:** JSON files provide the ultimate in portability and transparency. Every developer can inspect, diff, and understand the data without any tooling. The hierarchical directory structure (`baselines/data/{agent}/{prompt_id}/run-{NNN}.json`) creates natural namespacing that maps directly to the problem domain. Git's line-based diff algorithms work exceptionally well with pretty-printed JSON, making code review straightforward. The format is self-documenting and requires zero schema migrations.

**Evaluation:**
- **Portability (0.25):** Perfect score. No dependencies, works on any filesystem. Score: 10/10
- **Merge Conflict Risk (0.25):** Different files for different runs minimize conflicts. Score: 9/10
- **Queryability (0.20):** Requires grep/jq or custom scripts. Score: 6/10
- **Tooling Simplicity (0.15):** Just filesystem operations. Score: 10/10
- **Schema Evolution (0.15):** Add new fields without migration. Score: 9/10

**Weighted Score: 8.85/10**

### Option B: SQLite Database

**Steelman:** SQLite represents the gold standard for embedded databases. It provides ACID compliance, powerful SQL querying, and indexing capabilities in a single file. Complex statistical queries that would require custom code with JSON files become simple SQL statements. The binary format is compact and well-tested across millions of deployments. Schema migrations are explicit and auditable. For teams familiar with SQL, this provides immediate productivity.

**Evaluation:**
- **Portability (0.25):** Requires SQLite libraries, but widely available. Score: 8/10
- **Merge Conflict Risk (0.25):** Binary conflicts require careful coordination. Score: 4/10
- **Queryability (0.20):** Full SQL power with indexes. Score: 10/10
- **Tooling Simplicity (0.15):** Need SQLite CLI or libraries. Score: 7/10
- **Schema Evolution (0.15):** Requires migration scripts. Score: 6/10

**Weighted Score: 6.95/10**

### Evaluation Matrix

| Criterion | Weight | JSON Files | SQLite | Notes |
|-----------|--------|------------|--------|-------|
| Portability | 0.25 | 10 | 8 | JSON needs no dependencies |
| Merge Conflicts | 0.25 | 9 | 4 | File-per-run vs binary DB |
| Queryability | 0.20 | 6 | 10 | SQL vs grep/jq |
| Tool Simplicity | 0.15 | 10 | 7 | Filesystem vs DB tools |
| Schema Evolution | 0.15 | 9 | 6 | Add fields vs migrations |
| **Total** | **1.00** | **8.85** | **6.95** | |

## Consequences

### Positive Consequences (JSON Files)
- **Zero dependencies:** Any developer can work with the data using text editors
- **Git-friendly:** Line-based diffs show exact changes in baseline data
- **Debugging transparency:** Direct file inspection without tooling
- **Natural sharding:** File-per-run prevents write contention
- **Flexible schema:** Add fields without breaking existing consumers

### Negative Consequences (JSON Files)
- **Query complexity:** Statistical analysis requires custom scripting
- **No ACID guarantees:** Filesystem operations lack transactional consistency
- **Performance overhead:** Multiple file operations vs single DB query
- **Manual indexing:** Must implement own lookup structures for performance

### Neutral Consequences
- **Storage efficiency:** JSON files use more disk space but within Git's comfort zone (4MB)
- **Backup strategy:** Both options work with standard Git workflows

## L0: Executive Summary

We're choosing to store our test baseline data as individual JSON files organized in folders, rather than using a database. This is like choosing to store receipts in labeled folders rather than a filing system with an index. While it takes more work to find specific receipts (you have to look through folders), anyone can understand the system without special training, and multiple people can add receipts without interfering with each other.

## L1: Technical Implementation

### Directory Structure
```
baselines/
├── data/
│   ├── ps-analyst/
│   │   ├── regression-001/
│   │   │   ├── run-001.json
│   │   │   ├── run-002.json
│   │   │   └── ...run-030.json
│   │   └── regression-002/
│   └── ps-architect/
└── index/
    └── manifest.json  # Optional index for performance
```

### Run Record Format
```json
{
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T10:30:00Z",
  "agent": "ps-analyst",
  "prompt_id": "regression-001",
  "model": "claude-3-opus",
  "raw_output": "...",
  "scores": {
    "relevance": 0.92,
    "completeness": 0.88,
    "accuracy": 0.95
  },
  "metadata": {
    "temperature": 0.7,
    "max_tokens": 4000
  }
}
```

### Implementation Patterns
```python
# Writing a baseline
def save_baseline_run(agent: str, prompt_id: str, run_data: dict) -> Path:
    run_number = get_next_run_number(agent, prompt_id)
    path = Path(f"baselines/data/{agent}/{prompt_id}/run-{run_number:03d}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(run_data, f, indent=2)
    return path

# Querying baselines
def load_baseline_runs(agent: str, prompt_id: str) -> List[dict]:
    pattern = f"baselines/data/{agent}/{prompt_id}/run-*.json"
    return [json.load(open(f)) for f in sorted(glob(pattern))]
```

## L2: Architectural Implications

### Long-term Evolution Path

The JSON file approach creates a **document-oriented architecture** that aligns with the regression harness's bounded context. This positions the system for:

1. **Gradual Index Introduction:** Can add `manifest.json` or lightweight indexes without changing storage format
2. **Polyglot Persistence:** Future ability to sync to different storage backends (S3, MongoDB) without migration
3. **Event Sourcing Compatibility:** Each run as an immutable event supports audit trails and replay

### Integration Patterns

The file-based approach enables:
- **CI/CD Integration:** Baseline files can be validated in PR checks
- **Artifact Publishing:** Baselines can be packaged with releases
- **Cross-Repository Sharing:** Baselines can be git submodules or separate repos

### Architectural Trade-offs

**Embraced:**
- Simplicity over query sophistication
- Transparency over storage efficiency
- Decentralization over consistency guarantees

**Deferred:**
- Complex analytical queries (can add tooling later)
- Real-time aggregation (batch processing sufficient)
- Strong consistency (eventual consistency acceptable)

### Future Flexibility

The JSON approach maintains maximum optionality:
- Can introduce SQLite as a derived view/cache
- Can implement GraphQL/REST API over file storage
- Can migrate to cloud storage with minimal code changes

### Anti-patterns to Avoid

1. **Don't add binary formats:** Keep all data human-readable
2. **Don't nest too deeply:** Maintain the 3-level hierarchy
3. **Don't modify historical runs:** Treat as immutable

## Risks

### Primary Risk: Query Performance at Scale
- **Mitigation:** Implement lazy-loading and caching strategies
- **Trigger:** Monitor when directory listing exceeds 100ms
- **Fallback:** Add manifest.json index when needed

### Secondary Risk: Accidental Data Corruption
- **Mitigation:** Git hooks to validate JSON structure
- **Trigger:** Pre-commit validation of modified baselines
- **Fallback:** Git history provides recovery path

## Related Decisions

- This decision influences future choices about statistical analysis tooling
- May need separate ADR for baseline comparison algorithms
- Future ADR on baseline retention policies (how many to keep)

## PS Integration

This ADR will be linked to PROJ-036 entry e-001 for tracking the baseline storage implementation.
</content>
</Write>

Now I'll link this artifact to the problem-solving system:

<Bash>
<command>cd /tmp/repos/context && python3 scripts/cli.py link-artifact proj-036 e-001 FILE "projects/proj-036/decisions/proj-036-e-001-adr-baseline-storage.md" "ADR: Baseline Storage Strategy"</command>
</Bash>

## Summary

I've created ADR-001 for the PROJ-036 prompt regression harness baseline storage decision. The ADR follows the Nygard format and includes all requested elements:

### Key Decision: JSON Files on Disk (Option A)

**Weighted Score: 8.85/10** vs SQLite's 6.95/10

The decision prioritizes:
- **Portability** (10/10): Zero dependencies, works everywhere
- **Merge conflict avoidance** (9/10): File-per-run minimizes Git conflicts
- **Tooling simplicity** (10/10): Just filesystem operations

Trade-offs accepted:
- Lower queryability (6/10) - requires grep/jq instead of SQL
- More complex statistical analysis implementation

### L0/L1/L2 Coverage

- **L0 (Executive)**: Receipt filing analogy for non-technical understanding
- **L1 (Implementation)**: Directory structure, JSON schema, Python code patterns
- **L2 (Architecture)**: Evolution path, integration patterns, future flexibility

### Steelman Analysis Applied

Both options received strongest-case presentations:
- JSON portrayed as transparent and Git-native
- SQLite highlighted for ACID compliance and SQL power

The file has been created at `projects/proj-036/decisions/proj-036-e-001-adr-baseline-storage.md` and linked to the problem-solving entry as required by P-002.

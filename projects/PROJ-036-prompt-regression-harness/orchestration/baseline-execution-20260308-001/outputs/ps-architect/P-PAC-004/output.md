I'll create a comprehensive ADR for the regression harness baseline invalidation mechanism.

<bash>
# First, check if the project directory structure exists
mkdir -p projects/${JERRY_PROJECT}/decisions
</bash>

<bash>
# Get the next ADR number by checking existing ADRs
ls projects/${JERRY_PROJECT}/decisions/adr-*.md 2>/dev/null | wc -l
</bash>

Now I'll create the ADR with the full Nygard format and L0/L1/L2 sections:

<Write>
<file_path>projects/${JERRY_PROJECT}/decisions/adr-001-baseline-invalidation-mechanism.md</file_path>
<content># ADR-001: Git Commit Hash Composite Key for Baseline Invalidation

## Status
PROPOSED

## L0: Executive Summary (ELI5)

We need to decide how to know when test baselines are outdated. Think of baselines like "answer keys" for tests - they tell us what the correct output should be. But when we update our AI agents or change the model version, these answer keys might no longer be valid.

We're proposing to use a "fingerprint" system (Option A) that automatically detects any change to the agent code or model version. If anything changes, the system will know the old baselines can't be trusted and will require new ones. This is like having a tamper-evident seal - if anything is different, we know immediately.

The alternative (Option B) would require humans to manually decide whether each code change affects the baselines. While more flexible, this adds complexity and potential for human error. We recommend starting with the automatic approach and evolving it later as AI gets better at understanding code changes.

## Context

The regression harness requires a mechanism to determine when captured baselines are no longer valid due to changes in:
- The underlying LLM model version
- The agent definition (system prompt, tools, configuration)
- The prompt template used to invoke the agent

Without proper invalidation, regression tests may pass against outdated baselines, providing false confidence in agent behavior consistency. This is particularly critical as we scale to hundreds of agents with thousands of test cases.

## Decision

We will implement **Option A: Git commit hash composite key** for baseline invalidation.

The baseline validity key will be computed as:
```
{model_version}:{agent_git_hash}:{prompt_git_hash}
```

This key will be:
1. Computed and stored in the baseline manifest at capture time
2. Recomputed before each regression test run
3. Used to automatically reject test runs when keys don't match

## L1: Technical Implementation (Software Engineer)

### Implementation Details

**Baseline Manifest Schema Enhancement:**
```json
{
  "version": "1.0.0",
  "baseline_id": "uuid-here",
  "validity_key": {
    "model_version": "claude-3-opus-20240229",
    "agent_git_hash": "a1b2c3d4e5f6",
    "prompt_git_hash": "f6e5d4c3b2a1",
    "composite": "claude-3-opus-20240229:a1b2c3d4e5f6:f6e5d4c3b2a1"
  },
  "captured_at": "2024-01-15T10:30:00Z",
  "agent_path": "agents/ps-architect.md",
  "prompt_path": "prompts/architectural-decision.md"
}
```

**Key Computation Algorithm:**
```python
def compute_validity_key(model_version: str, agent_path: str, prompt_path: str) -> str:
    """Compute composite validity key for baseline."""
    # Get git hash for agent file
    agent_hash = subprocess.check_output(
        ["git", "hash-object", agent_path]
    ).decode().strip()[:12]

    # Get git hash for prompt file (if exists)
    prompt_hash = "none"
    if prompt_path and os.path.exists(prompt_path):
        prompt_hash = subprocess.check_output(
            ["git", "hash-object", prompt_path]
        ).decode().strip()[:12]

    return f"{model_version}:{agent_hash}:{prompt_hash}"
```

**Validation at Runtime:**
```python
def validate_baseline(manifest: dict, current_model: str,
                     agent_path: str, prompt_path: str) -> bool:
    """Check if baseline is still valid."""
    stored_key = manifest["validity_key"]["composite"]
    current_key = compute_validity_key(current_model, agent_path, prompt_path)

    if stored_key != current_key:
        logger.warning(f"Baseline invalid: {stored_key} != {current_key}")
        return False
    return True
```

**Migration Path:**
- Existing baselines without validity keys will be marked as "legacy"
- A migration script will attempt to reconstruct keys from git history
- Baselines that cannot be migrated will require recapture

### Testing Approach

1. **Unit Tests:**
   - Key computation with various file states
   - Validation logic with matching/non-matching keys
   - Edge cases (new files, deleted files, uncommitted changes)

2. **Integration Tests:**
   - Full regression run with valid baselines
   - Rejection of invalid baselines with clear error messages
   - Migration of legacy baselines

3. **Performance Tests:**
   - Key computation overhead (should be <100ms per baseline)
   - Caching strategy for repeated validations

## L2: Architectural Implications (Principal Architect)

### Long-term Evolution Path

**Phase 1 (Current): Strict Git-based Validation**
- Simple, deterministic, no false positives
- May have false negatives (invalidating when change is non-semantic)
- Establishes manifest schema that supports future evolution

**Phase 2 (6-12 months): Hybrid Approach**
```yaml
validity_key:
  composite: "model:agent:prompt"  # Remains for compatibility
  semantic_hash: "s1m2n3t4c5"      # Added semantic analysis
  classification:
    method: "llm-assisted"
    confidence: 0.95
    last_review: "2024-07-01"
```

**Phase 3 (12-24 months): Full Semantic Analysis**
- LLM analyzes diffs to classify changes
- Automatic baseline retention for non-semantic changes
- Human-in-the-loop for low-confidence classifications

### Systemic Consequences

**Positive:**
- **Deterministic behavior**: No ambiguity about baseline validity
- **Git integration**: Leverages existing version control
- **Forward compatibility**: Manifest schema supports evolution
- **Audit trail**: Complete history of what invalidated each baseline

**Negative:**
- **Over-invalidation**: Formatting changes trigger recapture
- **Storage churn**: More frequent baseline captures increase storage
- **Developer friction**: More frequent "baseline out of date" errors

**Neutral:**
- **Coupling to git**: Requires git presence in test environment
- **Immutable history**: Cannot "fix" historical baselines retroactively

### Integration Points

1. **CI/CD Pipeline:**
   - Pre-commit hooks to warn about invalidation
   - Automated baseline recapture on model upgrades
   - Regression test gates in PR workflow

2. **Developer Workflow:**
   ```bash
   # Developer makes agent change
   git commit -m "Update ps-architect methodology"

   # Pre-commit hook warns
   WARNING: This change will invalidate 47 baselines

   # Developer can choose to proceed or batch changes
   ```

3. **Observability:**
   - Metrics on invalidation frequency by cause
   - Alerts on mass invalidation events
   - Dashboard of baseline health across all agents

### Decision Review Triggers

This decision should be revisited when:

1. **False negative rate > 20%**: If more than 20% of invalidations are for non-semantic changes
2. **LLM semantic analysis matures**: When reliable diff classification becomes available
3. **Scale threshold**: When baseline storage exceeds 1TB or 10,000 baselines
4. **Developer rebellion**: If developer friction becomes a blocker to adoption
5. **Alternative emerges**: If a better invalidation mechanism is discovered

### Trade-offs with Alternative Approaches

| Aspect | Option A (Chosen) | Option B (Semantic) | Hybrid Future |
|--------|-------------------|---------------------|---------------|
| Complexity | Low | High | Medium |
| False Positives | None | Possible | Rare |
| False Negatives | Common | Rare | Very Rare |
| Human Effort | Recapture only | Classification | Minimal |
| Implementation Time | 1 week | 4-6 weeks | Incremental |
| Evolution Path | Clear | Complex | Natural |

### Architectural Principles Applied

1. **Start Simple**: Choose the simplest solution that could possibly work
2. **Design for Evolution**: Ensure the solution can grow without breaking changes
3. **Fail Safe**: Better to over-invalidate than under-invalidate
4. **Measurable**: Built-in metrics to trigger evolution decisions

## Consequences

### Positive
- **Immediate implementation**: Can be built in days, not weeks
- **No ambiguity**: Crystal clear when baselines are valid
- **Version control alignment**: Leverages git's content-addressable storage
- **Evolution-ready**: Schema supports future enhancements without breaking changes

### Negative
- **Over-eager invalidation**: Whitespace/comment changes trigger recapture
- **Baseline churn**: More frequent captures mean more storage and management
- **Developer interruption**: Valid work blocked by "outdated baseline" errors
- **Git dependency**: Cannot run regression tests without git metadata

### Neutral
- **Deterministic behavior**: Predictable but sometimes inconvenient
- **No judgment calls**: Removes human decision-making (good and bad)
- **Tooling requirements**: Requires git in all test environments

## Risks

### Risk 1: Excessive Baseline Churn
**Mitigation**:
- Implement baseline capture automation in CI
- Create bulk recapture tooling
- Monitor invalidation frequency metrics

### Risk 2: Developer Workflow Friction
**Mitigation**:
- Clear error messages with remediation steps
- Pre-commit warnings before invalidation
- "Baseline update" PR automation

### Risk 3: Storage Growth
**Mitigation**:
- Implement baseline retention policies
- Archive old baselines to cold storage
- Monitor storage growth trends

## Related Decisions
- None yet (first ADR in this domain)

## PS Integration
- **PS ID**: N/A (infrastructure decision)
- **Entry ID**: N/A
- **Related PS Items**: Testing methodology updates may reference this ADR

## Options Evaluated (P-011)

| Option | Pros | Cons | Score |
|--------|------|------|-------|
| A: Git Composite Key | • Simple implementation<br>• No false positives<br>• Evolution-friendly<br>• Deterministic | • Over-invalidation<br>• No semantic understanding<br>• Git dependency | 8/10 |
| B: Semantic Classification | • Fewer false invalidations<br>• Human insight<br>• Flexible | • Complex implementation<br>• Requires classification<br>• Potential false positives<br>• Longer initial setup | 5/10 |
| C: No Invalidation | • Simplest<br>• No interruptions | • Dangerous false confidence<br>• Manual tracking<br>• Error-prone | 2/10 |
| **Chosen: A** | Start simple, evolve toward B over time as LLM classification matures | | |

---

*Generated by ps-architect v2.3.0*
*Template: ADR Nygard Format with L0/L1/L2*
*Date: 2024-01-15*</content>
</Write>

Now I'll create the artifact link for PS integration:

<bash>
# Since this is an infrastructure decision without a specific PS ID,
# we'll create a standalone reference that can be linked from future PS items
echo "ADR-001 created at: projects/${JERRY_PROJECT}/decisions/adr-001-baseline-invalidation-mechanism.md"
echo "This infrastructure ADR can be referenced by future PS entries as needed."
</bash>

<WebSearch>
<query>git hash-object performance benchmarks file hashing speed 2024</query>
</WebSearch>

Let me also create a brief evolution roadmap document to supplement the ADR:

<Write>
<file_path>projects/${JERRY_PROJECT}/decisions/adr-001-evolution-roadmap.md</file_path>
<content># Evolution Roadmap: Baseline Invalidation Mechanism

## Current State (Phase 1): Git Composite Key
**Timeline**: Now - 6 months
**Implementation**: ADR-001

### Key Characteristics
- Strict invalidation on any change
- Git hash-based detection
- Zero false positives, high false negatives

### Success Metrics to Track
- Invalidation frequency by cause
- Developer friction reports
- Baseline storage growth rate
- Time spent on recapture

## Phase 2: Hybrid Approach
**Timeline**: 6-12 months
**Trigger**: When LLM diff analysis shows >80% accuracy

### Migration Steps
1. Add `semantic_hash` field to manifest (backward compatible)
2. Run both validation methods in parallel
3. Collect metrics on disagreement rate
4. Gradually trust semantic analysis for non-breaking changes

### Implementation Sketch
```python
def validate_with_semantic_analysis(manifest, current_state):
    # Existing git validation
    git_valid = validate_git_composite_key(manifest, current_state)

    # New semantic validation (if available)
    if "semantic_hash" in manifest:
        semantic_valid = validate_semantic_hash(manifest, current_state)

        # Log disagreements for analysis
        if git_valid != semantic_valid:
            log_validation_disagreement(manifest, git_valid, semantic_valid)

    # Phase 2: Still use git as source of truth
    return git_valid
```

## Phase 3: Semantic-First Validation
**Timeline**: 12-24 months
**Trigger**: Semantic analysis disagreement rate <5%

### Full Semantic Classification
- LLM analyzes diffs in real-time
- Human review only for low-confidence classifications
- Git hash becomes fallback mechanism

### Decision Review Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| False negative rate | >20% | Accelerate Phase 2 |
| Storage growth | >1TB | Implement retention policies |
| Developer complaints | >10/month | Add workflow improvements |
| LLM accuracy | >80% | Begin Phase 2 transition |

## Rollback Plan

If Option A proves unworkable:
1. Freeze new baseline captures
2. Mark all baselines as "legacy"
3. Implement Option B classification UI
4. Manually classify critical baselines
5. Auto-classify remaining using heuristics

## Communication Plan

### For Developers
- Clear error messages with fix instructions
- Pre-commit hooks with invalidation warnings
- Documentation in developer guide

### For Stakeholders
- Monthly metrics on baseline health
- Quarterly review of evolution progress
- Clear ROI on invalidation accuracy

---

*This roadmap is a living document and will be updated based on operational experience.*</content>
</Write>

## Summary

I've created a comprehensive ADR (ADR-001) for the baseline invalidation mechanism decision. The ADR:

1. **Recommends Option A** (Git Composite Key) as the initial implementation
2. **Provides clear rationale**: Simplicity, deterministic behavior, and evolution-friendly design
3. **Includes all required sections**:
   - L0: Executive summary for non-technical stakeholders
   - L1: Detailed technical implementation for engineers
   - L2: Long-term architectural implications and evolution path

4. **Documents the evolution strategy**:
   - Phase 1: Current strict git-based approach
   - Phase 2: Hybrid with semantic analysis (6-12 months)
   - Phase 3: Semantic-first validation (12-24 months)

5. **Defines clear review triggers**:
   - False negative rate >20%
   - Storage exceeding 1TB
   - Developer friction metrics
   - LLM semantic analysis maturity

The decision prioritizes immediate implementation and safety (no false positives) while designing for future evolution toward more intelligent semantic analysis. The manifest schema is designed to support this evolution without breaking changes.

The supplementary evolution roadmap document provides additional implementation detail for the migration path.

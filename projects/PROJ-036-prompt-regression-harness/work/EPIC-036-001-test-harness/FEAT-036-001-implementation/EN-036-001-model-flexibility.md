# EN-036-001: Model Flexibility for G-Eval Judge and Agent Execution

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** enabler
> **Enabler Type:** infrastructure
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-07T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-036-001
> **Owner:** —
> **Target Sprint:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Enabler scope and rationale |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Verification criteria |
| [Current State](#current-state) | What exists today |
| [Proposed Changes](#proposed-changes) | What needs to change |
| [Technical Approach](#technical-approach) | Implementation strategy |
| [Related Items](#related-items) | Dependencies and references |
| [History](#history) | Status changes |

---

## Summary

Decouple model selection for both G-Eval judge scoring (Layer 2) and agent execution (Phase 1 output generation) from hardcoded defaults. Currently the `DeepEvalAdapter` hardcodes `claude-sonnet-4-20250514` as the judge model, and `BaselineStore` examples assume the same model string. Agent execution relies on the `model:` frontmatter field in each agent definition (opus/sonnet/haiku), but the test harness has no mechanism to override or parameterize these for cross-model comparison runs.

**Value Proposition:**
- Enable regression testing across model upgrades (e.g., Sonnet 4.5 -> Sonnet 4.6)
- Allow cost-optimized evaluation runs (Haiku judge for smoke tests, Opus judge for full)
- Support model migration confidence: validate agent behavior on a new model before updating the agent definition
- Track model version in baseline records for reproducibility (already in `BaselineRecord.model_version`)

---

## Benefit Hypothesis

**We believe that** parameterizing the LLM model for both G-Eval judge scoring and agent execution

**Will result in** cross-model regression detection and cost-flexible evaluation tiers

**We will know we have succeeded when** a single CLI flag (e.g., `--judge-model`, `--agent-model`) can override defaults and baseline records accurately track which model combination produced each score

---

## Acceptance Criteria

- [ ] `DeepEvalAdapter` accepts `model_name` as a constructor parameter (already exists) AND as an environment variable override (e.g., `JERRY_JUDGE_MODEL`)
- [ ] Agent execution model can be overridden per-run via environment variable (e.g., `JERRY_AGENT_MODEL`) without modifying agent `.md` frontmatter
- [ ] `BaselineRecord.model_version` captures a composite string: `{agent_model}:{judge_model}` (e.g., `claude-opus-4-20250514:claude-sonnet-4-20250514`)
- [ ] Layer 4 comparison rejects score pairs collected with different model combinations (apples-to-apples enforcement)
- [ ] Cost ledger reports differentiated pricing based on actual model used (opus vs sonnet vs haiku)
- [ ] CLI `jerry test run` supports `--judge-model` and `--agent-model` flags
- [ ] Documentation updated in system-design.md to reflect model parameterization

---

## Current State

| Component | Current Model | Hardcoded? |
|-----------|--------------|------------|
| `DeepEvalAdapter.model_name` | `claude-sonnet-4-20250514` | Default in dataclass field (overridable via constructor) |
| `JerryGEvalMetric.model` | Passed from adapter | No — receives from adapter |
| `BaselineStore` examples | `claude-sonnet-4-20250514` | In docstring examples only |
| `BaselineRecord.model_version` | String field | Flexible — tracks whatever is passed |
| Agent execution (ps-researcher) | `opus` | YAML frontmatter in agent `.md` |
| Agent execution (ps-analyst) | `sonnet` | YAML frontmatter in agent `.md` |
| Agent execution (ps-architect) | `opus` | YAML frontmatter in agent `.md` |
| Agent execution (ps-critic) | `sonnet` | YAML frontmatter in agent `.md` |
| Agent execution (adv-scorer) | `sonnet` | YAML frontmatter in agent `.md` |

---

## Proposed Changes

1. **Environment variable overrides**: Add `JERRY_JUDGE_MODEL` and `JERRY_AGENT_MODEL` env vars respected by the test harness entry points
2. **Composite model version tracking**: Change `BaselineRecord.model_version` semantics to `{agent_model}:{judge_model}` format
3. **Apples-to-apples guard**: Layer 4 `Layer4Pipeline.run()` validates that baseline and candidate `model_version` fields match before comparison
4. **Pricing table**: Add a model pricing lookup for cost ledger accuracy across model tiers
5. **CLI flags**: Extend `jerry test run` with `--judge-model` and `--agent-model` options

---

## Technical Approach

Environment variable-based override pattern: `JERRY_JUDGE_MODEL` and `JERRY_AGENT_MODEL` env vars are checked at test harness entry point construction. These override the default model values without requiring agent definition file changes. The `BaselineRecord.model_version` field is extended to carry composite model identity for apples-to-apples comparison enforcement in Layer 4.

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-036-001: Test Harness Implementation](../FEAT-036-001-implementation/FEAT-036-001-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Modifies | `jerry/testing/evaluation/deepeval_adapter.py` | Add env var override for `model_name` |
| Modifies | `jerry/testing/types.py` | Composite `model_version` format |
| Modifies | `jerry/testing/layer4_stats.py` | Apples-to-apples model version guard |
| Informed By | Agent definitions (`skills/*/agents/*.md`) | Source of pinned model versions |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Enabler created; identified during execution prompt review — G-Eval judge and agent execution models are currently conflated in test harness prompt design |

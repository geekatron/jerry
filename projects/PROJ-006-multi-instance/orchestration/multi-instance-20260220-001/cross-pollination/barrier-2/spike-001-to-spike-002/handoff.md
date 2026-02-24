# Barrier 2 Handoff: SPIKE-001 → SPIKE-002

> **Direction:** spike-001 (SDK vs CLI) → spike-002 (Worktree Lifecycle)
> **Barrier:** barrier-2 (Phase 2 Cross-Pollination)
> **Date:** 2026-02-20
> **Source:** agent-a-002-analysis.md

---

## Purpose

Provide the convergent Phase 3 ADR synthesis with the scored recommendation from the 8-dimension trade-off analysis, so the architect can make a go/no-go decision with full quantitative backing.

---

## Scored Recommendation

### Composite Scores

| Approach | Weighted Composite | Rank |
|----------|:------------------:|:----:|
| **Claude Agent SDK** | **8.70** | **1 (Winner)** |
| **Hybrid** | **8.70** | 2 (tiebreak: higher complexity) |
| **Claude Code CLI** | **7.70** | 3 |
| **Anthropic Python SDK** | **4.10** | 4 (partially disqualified) |

### Per-Dimension Breakdown

| Dimension | Weight | Anthropic SDK | Agent SDK | CLI | Hybrid |
|-----------|:------:|:---:|:---:|:---:|:---:|
| Programmatic Control | 0.20 | 1.00 | **1.80** | 1.60 | **1.80** |
| Tool Surface | 0.20 | 0.40 | **2.00** | 1.80 | **2.00** |
| Session Persistence | 0.15 | 0.30 | **1.35** | **1.35** | **1.35** |
| Error Handling | 0.10 | 0.70 | **0.80** | 0.60 | **0.80** |
| Developer Experience | 0.10 | 0.30 | **0.90** | 0.60 | 0.80 |
| Cost Efficiency | 0.10 | **0.80** | 0.60 | 0.60 | 0.70 |
| Jerry Integration | 0.10 | 0.20 | **0.90** | 0.80 | **0.90** |
| Scalability | 0.05 | **0.40** | 0.35 | 0.35 | 0.35 |

### Key Decision Factors

1. **Agent SDK wins on the top-3 weighted dimensions** (Programmatic Control + Tool Surface + Session Persistence = 55% of total weight)
2. **Anthropic SDK partially fails mandatory requirements** — no CLAUDE.md loading, no `.claude/` settings
3. **Hybrid ties but adds unnecessary complexity** — adapter pattern provides equivalent flexibility without upfront dual-SDK burden
4. **CLI is viable but requires more orchestration code** — raw subprocess management vs typed Python API
5. **Sensitivity analysis confirms robustness** — Agent SDK wins under all three weight perturbation scenarios tested

### Mandatory Requirement Gate Results

| Requirement | Anthropic SDK | Agent SDK | CLI | Hybrid |
|-------------|:---:|:---:|:---:|:---:|
| Working directory isolation | PASS | PASS | PASS | PASS |
| Environment variable isolation | PASS | PASS | PASS | PASS |
| CLAUDE.md auto-loading | **FAIL** | PASS | PASS | PASS |
| `.claude/` settings per-worktree | **FAIL** | PASS | PASS | PASS |

### Risk Factors (from S-013 Inversion)

| Risk | Severity | Mitigation |
|------|----------|------------|
| SDK immaturity (203 open issues) | MEDIUM | Pin version, adapter layer, CLI fallback |
| API breaking changes (renamed once) | MEDIUM | Adapter layer, semantic versioning |
| No built-in `--max-budget-usd` | LOW | Use `max_turns` + hooks; CLI fallback for strict cost caps |

### Architectural Recommendation

**Port/adapter pattern** for the dispatch interface:
- **Port:** `InstanceDispatcher` protocol — `dispatch(worktree_path, prompt, options) -> InstanceResult`
- **Primary adapter:** `AgentSDKDispatcher` (Agent SDK `query()`)
- **Fallback adapter:** `CLISubprocessDispatcher` (raw CLI subprocess)
- **Migration:** Adapter swap, not architectural rewrite

---

## What Phase 3 Should Do With This

1. **Accept the Agent SDK recommendation** as the primary dispatch mechanism, with CLI as documented fallback adapter
2. **Incorporate the adapter pattern** into the integration architecture
3. **Address the cost-capping gap** (Agent SDK lacks `--max-budget-usd`) in risk assessment — mitigated by `max_turns` + hooks
4. **Reference the sensitivity analysis** to justify robustness of the recommendation
5. **Use the mandatory requirement gate** to formally exclude Anthropic SDK as a standalone option

---

*Source: agent-a-002-analysis.md (SPIKE-001 Phase 2)*
*Generated: 2026-02-20*

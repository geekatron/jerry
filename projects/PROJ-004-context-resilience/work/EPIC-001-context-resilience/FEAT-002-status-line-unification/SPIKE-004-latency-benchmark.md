# SPIKE-004: `uv run jerry context estimate` Latency Benchmark

> **Type:** spike
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-21
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --
> **Effort:** 1h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research question and hypothesis |
| [Findings](#findings) | Benchmark results |
| [Recommendation](#recommendation) | Decision and actions |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes |

---

## Content

### Research Question

**Question:** What is the actual invocation latency of `uv run jerry context estimate` via subprocess? Is it within the 2-second status line refresh budget? Was the "subprocess too heavy" claim in DISC-003 founded?

### Hypothesis

We hypothesize that `uv run jerry context estimate` subprocess latency is well within the 2-second status line refresh budget, consistent with existing hooks that already call `jerry hooks prompt-submit` at prompt frequency.

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox Duration | 1 hour |
| Resolves | DISC-003 (unfounded latency claims) |

---

## Findings

### Summary

Benchmark results confirm the hypothesis. Subprocess invocation latency is well within the 2s status line budget with substantial margin.

### Benchmark Results

| Metric | Value |
|--------|-------|
| p50 | 96ms |
| p95 | 112ms |
| p99 | 138ms |
| Budget | 2000ms |
| Margin | ~18x headroom at p99 |

### Analysis

The "subprocess too heavy" claim from DISC-003 was unfounded. Hooks already invoke `jerry hooks prompt-submit` via subprocess at every user prompt — the same pattern applies to status line polling. The 96ms p50 is consistent with uv's warm cache behavior after first invocation.

---

## Recommendation

**Decision:** Proceed with `jerry context estimate` CLI approach for status line integration. Subprocess pattern is viable. No performance mitigation required.

**Actions taken:**
- DISC-003 resolved
- EN-012 (`jerry context estimate` CLI) implemented as planned
- ST-005 (jerry-statusline integration) unblocked

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Status Line / Context Monitoring Unification](./FEAT-002-status-line-unification.md)
- **Resolves:** [DISC-003: Unfounded Subprocess Latency Claims](../FEAT-001-context-detection/DISC-003-unfounded-latency-claims.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | done | Benchmark complete. p50=96ms, p95=112ms, p99=138ms. DISC-003 resolved. |

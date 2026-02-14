# TASK-006: Performance Benchmark Specifications

<!--
TEMPLATE: Task Deliverable
VERSION: 1.0.0
ENABLER: EN-406
AC: AC-6
CREATED: 2026-02-13 (ps-validator-406)
PURPOSE: Performance benchmark specifications for enforcement mechanism overhead validation
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-6 (Performance overhead validated at <2s for all enforcement paths)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Performance testing scope and targets |
| [Performance Budget](#performance-budget) | Per-mechanism and total budget allocation |
| [Benchmark Test Cases](#benchmark-test-cases) | Individual performance test specifications |
| [Combined Performance Tests](#combined-performance-tests) | Full-stack performance validation |
| [Measurement Methodology](#measurement-methodology) | How to measure performance accurately |
| [Statistical Requirements](#statistical-requirements) | Statistical significance and reporting |
| [Performance Risks](#performance-risks) | Identified risks and mitigations |
| [Requirements Traceability](#requirements-traceability) | Test-to-requirement mapping |
| [References](#references) | Source documents |

---

## Overview

This document specifies performance benchmark tests for all enforcement mechanisms. The primary requirement is NFC-1: enforcement overhead MUST NOT exceed 2 seconds per enforcement path. Tests validate individual mechanism performance, combined stack performance, and edge cases that could cause performance degradation.

### Performance Targets

| Target | Threshold | Source |
|--------|-----------|--------|
| Total enforcement overhead | < 2,000ms | NFC-1 (FEAT-005) |
| PreToolUse (L3) evaluation | < 87ms | EN-403 TASK-003 |
| UserPromptSubmit (L2) generation | < 500ms | REQ-403-012 (derived) |
| SessionStart preamble generation | < 200ms | REQ-405 (derived) |
| Combined L1+L2+L3 per-prompt | < 2,000ms | NFC-1 |

### Test Summary

| Category | Test Count | ID Range |
|----------|------------|----------|
| Individual Mechanism | 8 | TC-PERF-001 through TC-PERF-008 |
| Combined Performance | 5 | TC-CPERF-001 through TC-CPERF-005 |
| Edge Case Performance | 4 | TC-EPERF-001 through TC-EPERF-004 |
| **Total** | **17** | |

---

## Performance Budget

### Per-Mechanism Budget Allocation

| Mechanism | Budget | Justification |
|-----------|--------|---------------|
| SessionStart preamble generation | 200ms | One-time cost at session start; not per-prompt |
| UserPromptSubmit hook execution | 500ms | Per-prompt; includes keyword analysis + content selection + XML generation |
| PreToolUse hook evaluation | 87ms | Per-tool-use; includes all 5 phases of evaluation |
| Rule file loading (L1) | N/A (loaded by Claude Code, not our code) | Auto-loaded by platform; not measured |
| **Total per-prompt worst case** | **587ms** | Well within 2,000ms budget |

### Budget Margin Analysis

| Metric | Value |
|--------|-------|
| Total budget | 2,000ms |
| Allocated | 587ms (worst case per-prompt: L2 + L3) |
| Margin | 1,413ms (71% margin) |
| One-time cost | 200ms (SessionStart, not per-prompt) |

---

## Benchmark Test Cases

### TC-PERF-001: PreToolUse - Simple File Evaluation

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-001 |
| **Objective** | Measure PreToolUse evaluation time for a simple Python file |
| **Input** | Write to `src/domain/entities/task.py` with ~50 lines of valid code |
| **Steps** | 1. Time `PreToolEnforcementEngine.evaluate_write()`. 2. Repeat 100 times. 3. Compute statistics. |
| **Target** | p50 < 30ms, p95 < 87ms, p99 < 100ms |
| **Requirements** | REQ-403-038, NFC-1 |
| **Verification** | Test |

### TC-PERF-002: PreToolUse - Complex File Evaluation

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-002 |
| **Objective** | Measure PreToolUse evaluation time for a complex Python file |
| **Input** | Write to `src/domain/aggregates/work_item.py` with ~500 lines, multiple imports, complex AST |
| **Steps** | 1. Time evaluation. 2. Repeat 100 times. 3. Compute statistics. |
| **Target** | p50 < 50ms, p95 < 87ms, p99 < 150ms |
| **Requirements** | REQ-403-038, NFC-1 |
| **Verification** | Test |

### TC-PERF-003: PreToolUse - Non-Python File (Fast Path)

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-003 |
| **Objective** | Measure PreToolUse fast path for non-Python files |
| **Input** | Write to `README.md` |
| **Steps** | 1. Time evaluation. 2. Repeat 100 times. |
| **Target** | p50 < 5ms, p95 < 10ms (AST phases skipped) |
| **Requirements** | REQ-403-039, NFC-1 |
| **Verification** | Test |

### TC-PERF-004: PreToolUse - Phase Breakdown

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-004 |
| **Objective** | Measure time spent in each of the 5 phases |
| **Input** | Domain Python file requiring full evaluation |
| **Steps** | 1. Instrument each phase with timing. 2. Measure phase durations. |
| **Expected Breakdown** | P1 (security) < 5ms; P2 (patterns) < 10ms; P3 (AST) < 50ms; P4 (governance) < 10ms; P5 (approve) < 2ms |
| **Target** | Total < 87ms; no single phase > 50ms |
| **Requirements** | REQ-403-037, REQ-403-038 |
| **Verification** | Test |

### TC-PERF-005: UserPromptSubmit - Standard Prompt

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-005 |
| **Objective** | Measure UserPromptSubmit hook execution time for standard prompts |
| **Input** | Standard C2 development prompt |
| **Steps** | 1. Time PromptReinforcementEngine execution. 2. Repeat 50 times. 3. Compute statistics. |
| **Target** | p50 < 100ms, p95 < 500ms |
| **Requirements** | REQ-403-012, NFC-1 |
| **Verification** | Test |

### TC-PERF-006: UserPromptSubmit - C4 Maximum Content

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-006 |
| **Objective** | Measure worst-case UserPromptSubmit (C4, all content blocks) |
| **Input** | C4 critical prompt triggering maximum content generation |
| **Steps** | 1. Time execution. 2. Repeat 50 times. |
| **Target** | p50 < 200ms, p95 < 500ms |
| **Requirements** | REQ-403-012, NFC-1 |
| **Verification** | Test |

### TC-PERF-007: SessionStart - Preamble Generation

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-007 |
| **Objective** | Measure SessionQualityContextGenerator.generate() execution time |
| **Input** | Standard session start |
| **Steps** | 1. Time generate() call. 2. Repeat 50 times. |
| **Target** | p50 < 50ms, p95 < 200ms |
| **Requirements** | PR-405-001, NFC-1 |
| **Verification** | Test |

### TC-PERF-008: SessionStart - Full Hook Execution

| Field | Value |
|-------|-------|
| **ID** | TC-PERF-008 |
| **Objective** | Measure full SessionStart hook execution including preamble |
| **Input** | Full session start with project context + preamble |
| **Steps** | 1. Time entire session_start_hook.py execution. 2. Repeat 20 times. |
| **Target** | p50 < 500ms, p95 < 1,000ms (includes file I/O, project context, etc.) |
| **Requirements** | NFC-1 |
| **Verification** | Test |

---

## Combined Performance Tests

### TC-CPERF-001: Full Prompt Cycle

| Field | Value |
|-------|-------|
| **ID** | TC-CPERF-001 |
| **Objective** | Measure total enforcement overhead for a complete prompt + tool use cycle |
| **Scenario** | User submits prompt -> L2 fires -> tool use -> L3 fires |
| **Steps** | 1. Time L2 execution. 2. Time L3 execution. 3. Sum. |
| **Target** | Total < 600ms (well within 2,000ms budget) |
| **Requirements** | NFC-1 |
| **Verification** | Test |

### TC-CPERF-002: Rapid Tool Use Sequence

| Field | Value |
|-------|-------|
| **ID** | TC-CPERF-002 |
| **Objective** | Measure L3 performance under rapid sequential tool uses |
| **Scenario** | 10 tool uses in rapid succession |
| **Steps** | 1. Invoke L3 10 times sequentially. 2. Measure per-invocation time. 3. Check for degradation. |
| **Target** | No degradation across invocations; each < 87ms |
| **Requirements** | NFC-1, REQ-403-038 |
| **Verification** | Test |

### TC-CPERF-003: Session Start Total Overhead

| Field | Value |
|-------|-------|
| **ID** | TC-CPERF-003 |
| **Objective** | Measure total additional overhead from quality enforcement at session start |
| **Scenario** | Session start with vs. without quality enforcement |
| **Steps** | 1. Measure session start without preamble. 2. Measure with preamble. 3. Calculate delta. |
| **Target** | Delta < 200ms |
| **Requirements** | NFC-1, IR-405-001 |
| **Verification** | Test |

### TC-CPERF-004: Memory Consumption

| Field | Value |
|-------|-------|
| **ID** | TC-CPERF-004 |
| **Objective** | Measure memory overhead of enforcement engines |
| **Scenario** | Instantiate all enforcement engines |
| **Steps** | 1. Measure baseline memory. 2. Instantiate PromptReinforcementEngine. 3. Instantiate PreToolEnforcementEngine. 4. Instantiate SessionQualityContextGenerator. 5. Measure delta. |
| **Target** | Combined memory overhead < 10MB |
| **Requirements** | NFC-1 (derived) |
| **Verification** | Test |

### TC-CPERF-005: Sustained Performance

| Field | Value |
|-------|-------|
| **ID** | TC-CPERF-005 |
| **Objective** | Verify performance stability over extended operation |
| **Scenario** | 100 prompt + tool use cycles |
| **Steps** | 1. Execute 100 cycles. 2. Compare first 10 vs. last 10 performance. |
| **Target** | No performance degradation (< 10% variance between first and last buckets) |
| **Requirements** | NFC-1 |
| **Verification** | Test |

---

## Measurement Methodology

### Timing Instrumentation

```python
# Reference approach for performance measurement
import time
from statistics import mean, median, stdev

def benchmark(func, *args, iterations=100):
    """Benchmark a function with statistical reporting."""
    timings = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        func(*args)
        elapsed = (time.perf_counter_ns() - start) / 1_000_000  # ms
        timings.append(elapsed)

    return {
        "p50": sorted(timings)[len(timings) // 2],
        "p95": sorted(timings)[int(len(timings) * 0.95)],
        "p99": sorted(timings)[int(len(timings) * 0.99)],
        "mean": mean(timings),
        "stdev": stdev(timings),
        "min": min(timings),
        "max": max(timings),
    }
```

### Measurement Rules

| Rule | Description |
|------|-------------|
| Warm-up | Discard first 5 iterations (JIT/cache warm-up) |
| Iterations | Minimum 50 iterations per benchmark |
| Isolation | No other CPU-intensive processes during measurement |
| Reporting | Report p50, p95, p99, mean, stdev |
| Environment | macOS, Python 3.11+, UV managed |
| Clock | Use `time.perf_counter_ns()` for high-resolution timing |

### Token Counting Methodology

| Method | Formula | Use For |
|--------|---------|---------|
| Conservative | chars / 4 | General estimation |
| XML-calibrated | (chars / 4) * 0.83 | XML-heavy content |
| Real tokenizer | `tiktoken` or equivalent | Final validation |

---

## Statistical Requirements

### Minimum Sample Sizes

| Test Type | Minimum Iterations | Rationale |
|-----------|-------------------|-----------|
| Individual function | 100 | Statistical significance |
| Full cycle | 50 | Combined variance |
| Session start | 20 | Slower, more variance |

### Reporting Format

```
Performance Report: TC-PERF-xxx
  Iterations: 100 (5 warm-up excluded)
  p50:   XX.X ms
  p95:   XX.X ms
  p99:   XX.X ms
  Mean:  XX.X ms (SD: XX.X ms)
  Min:   XX.X ms
  Max:   XX.X ms
  PASS/FAIL: [p95 vs target]
```

### Pass/Fail Criteria

- **Primary:** p95 must be below target threshold
- **Secondary:** p99 should be below 2x target (acceptable outlier range)
- **Alert:** If stdev > 50% of mean, investigate variance source

---

## Performance Risks

| Risk ID | Description | Probability | Impact | Mitigation |
|---------|-------------|-------------|--------|------------|
| PR-001 | AST parsing of large files exceeds budget | LOW | HIGH | Set file size limit for AST parsing; bypass for files > 1000 lines |
| PR-002 | File I/O latency on slow disk | LOW | MEDIUM | All file reads should use caching where possible |
| PR-003 | Python startup overhead for hooks | MEDIUM | LOW | Hooks should minimize imports; lazy-load heavy modules |
| PR-004 | Concurrent hook invocations | LOW | LOW | Hooks are typically sequential per Claude Code architecture |
| PR-005 | Memory pressure from large files | LOW | MEDIUM | Stream-process rather than load entire file into memory |

---

## Requirements Traceability

| Test ID | Requirements Verified |
|---------|----------------------|
| TC-PERF-001 | REQ-403-038, NFC-1 |
| TC-PERF-002 | REQ-403-038, NFC-1 |
| TC-PERF-003 | REQ-403-039, NFC-1 |
| TC-PERF-004 | REQ-403-037, REQ-403-038 |
| TC-PERF-005 | REQ-403-012, NFC-1 |
| TC-PERF-006 | REQ-403-012, NFC-1 |
| TC-PERF-007 | PR-405-001, NFC-1 |
| TC-PERF-008 | NFC-1 |
| TC-CPERF-001 | NFC-1 |
| TC-CPERF-002 | NFC-1, REQ-403-038 |
| TC-CPERF-003 | NFC-1, IR-405-001 |
| TC-CPERF-004 | NFC-1 (derived) |
| TC-CPERF-005 | NFC-1 |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| FEAT-005 | `../FEAT-005-enforcement-mechanisms.md` | NFC-1 (<2s overhead) |
| EN-403 TASK-003 | `../EN-403-hook-based-enforcement/TASK-003-pretooluse-design.md` | 87ms performance budget |
| EN-403 TASK-002 | `../EN-403-hook-based-enforcement/TASK-002-userpromptsubmit-design.md` | L2 token budget |
| EN-405 TASK-001 | `../EN-405-session-context-enforcement/TASK-001-requirements.md` | Performance requirements |
| TASK-001 Integration Test Plan | `TASK-001-integration-test-plan.md` | Master test plan |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-6*

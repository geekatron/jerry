# FEAT-001:DISC-003: Unfounded Subprocess Latency Claims in Architecture Decisions

> **Type:** discovery
> **Status:** documented
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-02-21
> **Completed:** 2026-02-21
> **Parent:** FEAT-001
> **Owner:** --
> **Source:** Post-implementation review of PROJ-004

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core findings |
| [Context](#context) | What prompted this discovery |
| [Finding](#finding) | Unsubstantiated performance claims |
| [Evidence](#evidence) | Absence of benchmarks |
| [Implications](#implications) | Impact on architecture decisions |
| [Recommendations](#recommendations) | Evidence-based approach |
| [Document History](#document-history) | Change log |

---

## Summary

During PROJ-004's post-implementation review, the claim "spawning jerry as a subprocess each time might be too heavy" was repeatedly used to argue against status line / Jerry CLI integration. This claim was never substantiated with measurements. The Jerry CLI is already invoked via subprocess on every `UserPromptSubmit` hook event (every user prompt), demonstrating that the pattern works at prompt-frequency. Extending it to status-line-frequency is a measurable question, not an assumed blocker.

**Key Findings:**
- The "subprocess too heavy" claim was asserted multiple times without evidence
- Jerry CLI via subprocess is already proven at prompt-submit frequency
- No benchmark data exists for `jerry` CLI startup time via `uv run`
- A Go CLI would not receive the same objection, revealing a bias rather than a finding
- The claim influenced architectural framing by keeping the status line as a "provider" rather than a "consumer"

**Validation:** Absence of measurement data; user challenge

---

## Context

### Background

When exploring how to unify the status line with Jerry's context monitoring, the response repeatedly included caveats like "the concern is latency — the status line refreshes every 1-2 seconds, and spawning `jerry` as a subprocess each time might be too heavy." This framing was used across multiple conversation turns without any measurement.

The user challenged this directly: "You keep making unfounded arguments not based in any evidence." The user also posed a revealing test: would the same argument be made for a Go CLI? The answer is no — which exposes the claim as a bias about Python/uv startup time, not an evidence-based architectural constraint.

### Research Question

Is the subprocess latency claim evidence-based, and did it influence PROJ-004's architectural decisions?

### Investigation Approach

1. Searched for any benchmark data on `jerry` CLI startup time — found none
2. Verified that `jerry hooks prompt-submit` already runs via subprocess on every prompt
3. Assessed whether the claim affected status line integration framing

---

## Finding

### F-001: No Measurement Data Exists

No benchmark was conducted during PROJ-004 for:
- `uv run jerry hooks prompt-submit` invocation time
- Python interpreter startup overhead via `uv run`
- Comparison with direct Python invocation
- Status line refresh frequency vs CLI invocation cost

The claim "might be too heavy" is speculation, not evidence.

### F-002: The Pattern Is Already Proven

Jerry hooks already use subprocess invocation at prompt frequency:
- `hooks/user-prompt-submit.py` calls `jerry --json hooks prompt-submit` via subprocess
- This runs on **every user prompt** — the same frequency as status line refreshes
- No performance complaints have been raised about this pattern

If subprocess invocation works at prompt-submit frequency, it is a measurable step (not an assumed blocker) to assess whether it works at status-line-refresh frequency.

### F-003: Language Bias, Not Architectural Constraint

The "too heavy" framing would not apply to a Go binary with ~5ms startup time. The concern is specifically about Python/uv startup overhead. This is:
1. A measurable quantity (benchmark it, don't assume)
2. Potentially mitigable (persistent daemon, Unix socket, cached imports)
3. Not a reason to reject an architecture without data

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Code | Hook subprocess invocation pattern | `hooks/user-prompt-submit.py` | 2026-02-21 |
| E-002 | Absence | No CLI startup benchmark in PROJ-004 artifacts | All orchestration/spike reports | 2026-02-21 |
| E-003 | User feedback | "You keep making unfounded arguments not based in any evidence" | Session conversation | 2026-02-21 |

---

## Implications

### Impact on Architecture Decisions

The unfounded latency claim contributed to framing the status line as a "data provider to Jerry" rather than "a Jerry CLI consumer." This framing error (documented in DISC-002) meant the best available data source was never connected to Jerry's computation engine.

### Lesson for Future Work

Claims about performance must be backed by measurements. The cost of a benchmark is minutes; the cost of an incorrect architectural decision based on an assumption is hours of rework or missed capability.

---

## Recommendations

### Immediate Actions

1. Benchmark `uv run jerry hooks prompt-submit` with `time` or `hyperfine` across 100 invocations
2. Record p50, p95, p99 latency
3. Compare with status line refresh interval (~1-2 seconds)
4. Use data to inform status line integration architecture — not assumptions

### Long-term Considerations

- Any performance-based architectural rejection must include measured data
- Consider whether a persistent Jerry daemon (Unix socket) would eliminate startup overhead entirely for high-frequency consumers like the status line

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-21 | Claude | Created discovery. Documented unfounded subprocess latency claims and their impact on architectural framing. |

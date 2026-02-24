# FEAT-001:DISC-002: Status Line / Context Monitoring Unification Gap

> **Type:** discovery
> **Status:** resolved
> **Priority:** high
> **Impact:** high
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
| [Finding](#finding) | Two independent systems, missed unification |
| [Evidence](#evidence) | Code references and data schemas |
| [Implications](#implications) | Impact on context monitoring accuracy |
| [Recommendations](#recommendations) | Unification path |
| [Open Questions](#open-questions) | Items requiring investigation |
| [Document History](#document-history) | Change log |

---

## Summary

PROJ-004 built a context monitoring bounded context (`src/context_monitoring/`) that estimates context fill by backward-scanning the JSONL transcript file. Meanwhile, the ECW status line (`.claude/statusline.py`) receives **exact** `context_window.current_usage` data directly from Claude Code's status line API — the same three token fields, with zero parsing overhead and zero lag.

These two systems compute the same metric independently. The status line has the better data source but no domain logic. Jerry has calibrated thresholds, 5-tier classification, checkpoint services, and resumption context generation — but estimates from a heuristic data source. Neither system talks to the other.

The status line should call Jerry CLI (`jerry context estimate`), passing its rich input data through Jerry's bounded context. The CLI is an adapter — the domain and application layers are the product. The status line is just another consumer.

**Key Findings:**
- Two independent context fill calculations with different accuracy (exact vs heuristic)
- Two independent threshold systems with misaligned values (65%/85% vs 55%/70%/80%/88%/95%)
- Two independent compaction detectors (10K-drop heuristic vs tier-based checkpointing)
- The status line receives `context_window.current_usage` (exact tokens + window size) that Jerry never accesses
- Jerry's `JsonlTranscriptReader` backward-scans a JSONL file to reconstruct what the status line already has

**Validation:** Code inspection of `.claude/statusline.py` and `src/context_monitoring/`

---

## Context

### Background

PROJ-004 implemented context exhaustion detection as FEAT-001 with 12 work items across 3 sessions. The implementation chose transcript JSONL parsing (Method A) as the primary data source because:

1. SPIKE-001 identified that hooks receive `transcript_path` but not `context_window` data
2. SPIKE-003 investigated Method C (status line state file) and deferred it due to one-turn lag
3. The architectural decision (DEC-001) focused on CLI-first hooks and proper bounded context placement

What the spikes did NOT investigate: making the status line a Jerry CLI consumer. The framing was always "Jerry reads status line data" (Method C) rather than "status line calls Jerry with its data." This framing error meant the best data source was never connected to the best computation engine.

### Research Question

Did PROJ-004 miss an opportunity to unify the status line and context monitoring into a single system with exact data and calibrated thresholds?

### Investigation Approach

1. Compared the JSON schema that Claude Code sends to the status line vs. what hooks receive
2. Compared the context fill computation in `statusline.py` vs `ContextFillEstimator`
3. Identified the architectural principle (CLI as adapter) that resolves the gap

---

## Finding

### F-001: Two Independent Systems Computing the Same Metric

The status line and Jerry's context monitoring both compute context fill percentage using the same formula (`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`), but from different data sources with different accuracy:

| Aspect | Status Line (`statusline.py`) | Jerry (`ContextFillEstimator`) |
|--------|-------------------------------|-------------------------------|
| Data source | `context_window.current_usage` (exact, from Claude Code API) | JSONL transcript backward-scan (heuristic, one-turn lag) |
| Window size | `context_window.context_window_size` (exact) | Hardcoded 200K or config override |
| Thresholds | 65% warning, 85% critical (hardcoded) | 5-tier: 55%/70%/80%/88%/95% (configurable) |
| Compaction | State file delta > 10K tokens | CheckpointService at CRITICAL/EMERGENCY tiers |
| Output | ANSI text to IDE status bar | XML `<context-monitor>` tag in prompt context |
| Config | `~/.claude/ecw-statusline-config.json` | `.jerry/config.toml` (context_monitor.* keys) |

**Key observation:** The status line does the same three-field sum (line 412 of `statusline.py`) that SPIKE-003 corrected in `JsonlTranscriptReader`. The formula is identical. The data sources are not.

### F-002: The Status Line Has Data That Jerry Cannot Access

Claude Code sends different JSON schemas to different extension points:

**Status line receives (stdin):**
```json
{
  "context_window": {
    "context_window_size": 200000,
    "current_usage": {
      "input_tokens": 45000,
      "cache_creation_input_tokens": 12000,
      "cache_read_input_tokens": 98000
    },
    "total_input_tokens": 1200000,
    "total_output_tokens": 350000
  },
  "cost": { "total_cost_usd": 2.45, "total_duration_ms": 3600000 },
  "model": { "display_name": "Claude Opus 4.6", "id": "claude-opus-4-6" },
  "transcript_path": "/path/to/transcript.jsonl"
}
```

**Hooks receive (stdin):**
```json
{
  "session_id": "abc-123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project"
}
```

Hooks do **not** receive `context_window`, `cost`, or `model` data. This is why PROJ-004 was forced into transcript parsing — it's the only data hooks can access. The status line has the exact data Jerry needs, but there's no channel between them.

### F-003: The CLI-as-Adapter Principle Resolves This

The resolution is architectural, not technical. DEC-001 D-001 established that hooks must call the CLI via subprocess. The same principle applies to the status line:

- The status line is just another interface to Jerry's services
- It should call a `context_monitoring` CLI command (e.g. `jerry context estimate`), passing its rich JSON
- Jerry's `ContextFillEstimator` receives exact `current_usage` data instead of parsing transcripts
- Jerry returns formatted output (segments, thresholds, tier classification)
- The status line renders the result

This is not "status line as data provider" — it's "status line as CLI consumer." The bounded context owns the computation. The status line is an adapter, same as the CLI, same as a future daemon.

**Important:** The CLI command should live under the `context` (or `context-monitoring`) namespace, NOT under `hooks`. The hooks namespace is for Claude Code hook events (`UserPromptSubmit`, `SessionStart`, etc.). The status line is a distinct Claude Code extension point — a context monitoring consumer, not a hook. Placing it under `hooks` would violate domain boundaries and turn the hooks namespace into a kitchen sink.

### F-004: Misaligned Thresholds Create Conflicting Signals

The status line shows yellow at 65% and red at 85%. Jerry classifies WARNING at 70% and CRITICAL at 80%. A developer could see a green status bar while Jerry's prompt context says WARNING. This is a direct consequence of two independent systems with separate configuration.

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Code | Status line `extract_context_info()` — exact three-field sum | `.claude/statusline.py:403-423` | 2026-02-21 |
| E-002 | Code | Jerry `JsonlTranscriptReader` — heuristic backward-scan | `src/context_monitoring/infrastructure/adapters/jsonl_transcript_reader.py` | 2026-02-21 |
| E-003 | Code | Status line threshold hardcoding (65%/85%) | `.claude/statusline.py` DEFAULT_CONFIG | 2026-02-21 |
| E-004 | Code | Jerry threshold configuration (5-tier) | `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` | 2026-02-21 |
| E-005 | Research | SPIKE-003 Method C deferral — one-turn lag finding | `SPIKE-003-validation-spikes.md` | 2026-02-21 |
| E-006 | Research | SPIKE-001 GAP-003 — hooks don't receive context_window | SPIKE-001 mechanism inventory | 2026-02-19 |
| E-007 | Architecture | DEC-001 D-001 — CLI-first hook pattern | `DEC-001-cli-first-architecture.md` | 2026-02-19 |

---

## Implications

### Impact on Project

PROJ-004's context monitoring works — the heuristic approach detects exhaustion and triggers checkpoints. But it's working harder than necessary and with lower accuracy than available. The status line already has the exact data; Jerry just doesn't receive it.

This is not a bug or a failure — it's an unrealized integration opportunity that would:
1. Eliminate transcript parsing overhead entirely
2. Provide exact fill percentages instead of estimates
3. Unify threshold configuration
4. Unify compaction detection
5. Establish the status line as a proper Jerry CLI consumer

### Design Decisions Affected

- **DEC-001 D-001 (CLI-first hooks):** Extends naturally — the status line should follow the same pattern
- **ContextFillEstimator architecture:** The `ITranscriptReader` port would be supplemented or replaced by a direct `current_usage` input path
- **Threshold configuration:** Single source of truth instead of two independent configs

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Status line → CLI subprocess adds latency to every status line refresh | Medium | Measure actual overhead; cache results; only call Jerry on significant state changes |
| Breaking change for users with existing status line config | Low | Migration path; Jerry CLI returns same segments with enhanced thresholds |
| Status line currently zero-dependency (stdlib only); Jerry CLI requires uv | Medium | Status line could optionally call Jerry when available, fall back to standalone |

---

## Relationships

### Creates

- Follow-on feature: Status line / Jerry CLI unification (future project)

### Informs

- PROJ-004 retrospective: Architectural gap in spike research scope
- Future `jerry context estimate` CLI command design

### Related Discoveries

- [DISC-001: Hook-CLI Architecture Violations](./DISC-001-architecture-violations.md) — Established the CLI-first principle that this discovery extends to the status line
- [DISC-003: Unfounded Subprocess Latency Claims](./DISC-003-unfounded-latency-claims.md) — Related assumption about CLI invocation cost

---

## Recommendations

### Immediate Actions

1. Measure `jerry hooks prompt-submit` subprocess invocation time to establish baseline CLI overhead
2. Prototype `jerry context estimate` command that accepts the status line's JSON schema and returns formatted segments
3. Assess whether the status line can call Jerry optionally (with standalone fallback for users without Jerry)

### Long-term Considerations

- The CLI is an adapter. The domain logic in `context_monitoring` is the product. Any interface — status line, daemon, web UI — should consume these services, not reimplement them.
- A `jerry context status` command that returns current fill estimate would serve both the status line and other consumers (CI, monitoring, dashboards).
- Consider whether the status line script should live inside the Jerry project as a managed artifact rather than a separate standalone file.

---

## Open Questions

### Questions for Follow-up

1. **Q:** What is the actual subprocess overhead of `jerry context estimate` via `uv run`?
   - **Investigation Method:** Benchmark with `time` across 100 invocations
   - **Priority:** High — determines feasibility of per-refresh CLI invocation

2. **Q:** Can the status line maintain a standalone fallback while preferring Jerry CLI when available?
   - **Investigation Method:** Prototype dual-mode status line (detect Jerry availability at startup)
   - **Priority:** Medium — affects adoption path

3. **Q:** Should the status line script be a managed Jerry artifact or remain user-maintained?
   - **Investigation Method:** Evaluate maintenance burden, versioning, distribution
   - **Priority:** Low — architectural question for project roadmap

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-21 | Claude | Created discovery. Post-implementation review identified status line / context monitoring unification gap. |
| 2026-02-21 | Claude | Resolved by FEAT-002: `jerry context estimate` CLI command with exact `current_usage` data, 5-tier threshold SSOT, jerry-statusline Phase 1 integration (ST-005). |

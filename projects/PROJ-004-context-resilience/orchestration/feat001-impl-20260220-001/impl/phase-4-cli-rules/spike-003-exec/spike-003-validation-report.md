# SPIKE-003: Validation Report — OQ-9 + Method C

<!-- PS-ID: SPIKE-003 | ENTRY-ID: spike-003-exec | DATE: 2026-02-20 -->
<!-- AGENT: ps-researcher | MODEL: claude-sonnet-4-6 -->

> Research report for SPIKE-003 within feat001-impl-20260220-001 Phase 4 (FAN_OUT).
> Timebox: 3 hours.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Recommendations for both questions |
| [OQ-9 Findings](#oq-9-findings) | JsonlTranscriptReader accuracy analysis |
| [Method C Findings](#method-c-findings) | Status line state file feasibility |
| [Recommendations](#recommendations) | EN-006/EN-007 integration guidance |
| [Evidence](#evidence) | Source file and data references |

---

## Executive Summary

| Question | Recommendation | Severity |
|----------|---------------|----------|
| OQ-9: JsonlTranscriptReader accuracy | **ABANDON current implementation. REPLACE with corrected field path.** | BLOCKER |
| Method C: Status line state file | **DEFER. Architecturally feasible but carries timing risk and unclear marginal value.** | MEDIUM |

### OQ-9 Summary

`JsonlTranscriptReader` as implemented will **always raise `ValueError`** when run against a real Claude Code transcript. The implementation assumes a flat JSON structure `{"input_tokens": N}` at the top level of each JSONL line. The actual Claude Code transcript format stores token data at `entry["message"]["usage"]["input_tokens"]` — a three-level nesting. Additionally, even if the path were correct, `input_tokens` alone is a critically misleading metric for context fill estimation: it represents only the marginal fresh tokens for the most recent API call (typically 1-10 tokens in a cached session), not the cumulative context window usage. The correct formula for context fill percentage is `(input_tokens + cache_creation_input_tokens + cache_read_input_tokens) / context_window_size`.

The fix requires two changes: (1) correct the field path in `JsonlTranscriptReader`, and (2) update `ContextFillEstimator` to use the total of all three token fields. This is a required change before EN-006 and EN-007 can function correctly.

### Method C Summary

The `~/.claude/ecw-statusline-state.json` file is technically extendable with `context_fill_percentage`. The statusline already writes a state file and has access to the accurate `used_percentage` field from Claude Code's own status data. However, the timing relationship between status line updates and `UserPromptSubmit` hook execution means the state file at hook fire time reflects the context state from the **end of the previous turn**, not the current turn. This one-turn lag is an inherent architecture constraint, not a bug. For the primary use case (warn Claude before processing the current prompt), this lag may be acceptable (context does not grow dramatically between turns) or unacceptable (misses the exact pre-prompt context level). Method C should be deferred: Method A (transcript parsing with corrected field paths) is the required baseline that must work first.

---

## OQ-9 Findings

### Research Question

How accurate is `JsonlTranscriptReader`'s `input_tokens` field compared to reference sources?

### Finding 1: Structural Format Mismatch — BLOCKER

**Evidence: Transcript inspection of `/Users/anowak/.claude/projects/-Users-anowak-workspace-github-jerry-wt-feat-proj-004-context-resilience/2a18d762-c8b0-47b2-9d1b-7d3616a2c065.jsonl` (3,374 lines, production session)**

The Claude Code transcript JSONL format is **NOT** a flat `{"input_tokens": N}` structure. Every line is a fully structured event object. The five entry types observed across 3,374 lines:

| Entry Type | Count | Has Token Data | Token Data Location |
|------------|-------|----------------|---------------------|
| `progress` | 1,527 | No | — |
| `assistant` | 1,008 | Yes | `entry["message"]["usage"]` |
| `user` | 592 | No | — |
| `queue-operation` | 174 | No | — |
| `file-history-snapshot` | 36 | No | — |
| `system` | 37 | No | — |

**Zero entries have a top-level `input_tokens` key.** The current `JsonlTranscriptReader.read_latest_tokens()` implementation checks `data["input_tokens"]` which will never succeed.

**The last non-empty line in the transcript** (which is what `JsonlTranscriptReader` reads) is type `queue-operation` — not `assistant`. Even if the format check were correct, the reader would fail because the last line does not contain token data.

**Failure mode:** `ValueError: Last line of transcript has no 'input_tokens' field. Found keys: ['type', 'operation', 'timestamp', 'sessionId']`

**Current reader code (lines 95-101 of `jsonl_transcript_reader.py`):**
```python
if "input_tokens" not in data:
    raise ValueError(
        f"Last line of transcript has no 'input_tokens' field at {transcript_path}. "
        f"Found keys: {list(data.keys())}"
    )
return int(data["input_tokens"])
```

**Actual token data location:**
```python
# The correct path:
entry["message"]["usage"]["input_tokens"]
entry["message"]["usage"]["cache_creation_input_tokens"]
entry["message"]["usage"]["cache_read_input_tokens"]
```

**Actual `assistant` entry structure (from live transcript):**
```json
{
  "parentUuid": "...",
  "type": "assistant",
  "message": {
    "role": "assistant",
    "content": [...],
    "usage": {
      "input_tokens": 1,
      "cache_creation_input_tokens": 852,
      "cache_read_input_tokens": 157266,
      "output_tokens": 1,
      "service_tier": "standard"
    }
  },
  "uuid": "...",
  "timestamp": "2026-02-20T09:52:57.796Z"
}
```

### Finding 2: `input_tokens` Alone Is Not Context Fill — BLOCKER

Even if the field path were correct, reading only `input_tokens` from the last `assistant` entry would yield **1-10 tokens** — not the 100,000-180,000 range the `ContextFillEstimator` tier boundaries expect.

**Why:** In a Claude session with prompt caching active, `input_tokens` is the **marginal fresh tokens** for that specific API call. The vast majority of context is served from cache and reported in `cache_read_input_tokens`.

**Live session data from 1,008 assistant entries:**

| Metric | First 5 entries | Last 5 entries |
|--------|----------------|----------------|
| `input_tokens` | 1–3 | 1–3 |
| `cache_creation_input_tokens` | 2,450–14,298 | 498–2,326 |
| `cache_read_input_tokens` | 16,673–30,971 | 153,747–157,266 |
| **Total (input + cc + cr)** | **30,974–33,422** | **154,443–158,119** |

**The total grows monotonically with session length** — this is the cumulative context window usage that `ContextFillEstimator` needs to compare against `context_window_size` (200,000 tokens).

**Correct computation:**
```python
total = input_tokens + cache_creation_input_tokens + cache_read_input_tokens
fill_percentage = total / context_window_size
```

**From last assistant entry of live session:**
- `input_tokens` = 1 (what current reader returns — useless)
- `cache_creation_input_tokens` = 852
- `cache_read_input_tokens` = 157,266
- **Total = 158,119** (what fill estimation needs)
- **Fill % = 79.1%** (WARNING tier, approaching CRITICAL)

If the current reader returned `1` as the token count, `ContextFillEstimator` would compute 0.000005% fill (essentially 0) and classify the session as NOMINAL — **a catastrophically wrong result**. The warning/critical/emergency tier mechanisms would never fire.

### Finding 3: Correct Extraction Strategy

The `JsonlTranscriptReader` must be rewritten to:
1. Scan from the end of the transcript file for the last line with `type == "assistant"` and `message.usage` present
2. Extract all three token fields: `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`
3. Return the total (or return a structured result with all three fields)

**Alternative approach:** Change the return value to a named structure:

```python
@dataclass
class TranscriptTokenData:
    input_tokens: int
    cache_creation_input_tokens: int
    cache_read_input_tokens: int

    @property
    def total_context_tokens(self) -> int:
        return self.input_tokens + self.cache_creation_input_tokens + self.cache_read_input_tokens
```

**Or** the simpler path: have `read_latest_tokens()` return the total directly (sum of all three fields) and update the docstring/interface to clarify this is "cumulative context window usage" not raw `input_tokens`.

### Finding 4: StatusLine Reference Data

The ECW `statusline.py` computes context fill correctly using the same three-field formula (lines 403-423 of `.claude/statusline.py`):

```python
input_tokens = safe_get(current_usage, "input_tokens", default=0)
cache_creation = safe_get(current_usage, "cache_creation_input_tokens", default=0)
cache_read = safe_get(current_usage, "cache_read_input_tokens", default=0)
used_tokens = input_tokens + cache_creation + cache_read
percentage = (used_tokens / context_window_size) if context_window_size > 0 else 0
```

The official Claude Code documentation confirms this formula in the statusLine "Available Data" section: `used_percentage` is calculated as `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. The `output_tokens` field is explicitly excluded.

**Note:** The statusLine script reads this data from the **statusLine stdin JSON** (a distinct JSON blob from Claude Code containing `context_window.current_usage`), not from the transcript JSONL file. These are two different data sources.

### Finding 5: Test Suite — Tests Are Passing Against a Wrong Format

The existing unit tests in `test_jsonl_transcript_reader.py` use synthetic JSONL files with the flat format `{"input_tokens": 100000}`. These tests **pass** because the test fixtures match the reader's expectations. However, these fixtures do not match real Claude Code transcript format. The tests are not wrong for unit testing purposes, but they provide false confidence that the reader will work in production.

**Recommendation for tests:** Add an integration test fixture that uses the actual Claude Code JSONL structure:
```python
entry = {
    "type": "assistant",
    "message": {
        "usage": {
            "input_tokens": 1,
            "cache_creation_input_tokens": 5000,
            "cache_read_input_tokens": 145000
        }
    }
}
```

### OQ-9 Divergence Measurement

| Source | Value | Formula |
|--------|-------|---------|
| Current reader (last line, `data["input_tokens"]`) | RAISES ValueError | Field does not exist at top level |
| Corrected reader (last assistant, `message.usage.input_tokens` only) | 1–3 tokens | Marginal fresh tokens — useless for fill estimation |
| Corrected reader (last assistant, total of all three fields) | 158,119 tokens | Correct cumulative context |
| StatusLine `used_percentage` (from statusLine stdin) | 79.1% | Canonical reference from Claude Code |
| State file `previous_context_tokens` | 145,220 tokens | From previous turn — one turn stale |

**Conclusion:** Current divergence is 100% (functional failure). After fix, Method A (transcript-based) should achieve near-perfect accuracy vs. the canonical statusLine data, since both read from the same API response usage fields (just via different delivery mechanisms).

---

## Method C Findings

### Research Question

Can `~/.claude/ecw-statusline-state.json` be extended with `context_fill_percentage`? Does it update before `UserPromptSubmit` fires?

### Finding 1: State File Structure and Location

**Current state file contents (`~/.claude/ecw-statusline-state.json`):**
```json
{
  "previous_context_tokens": 145220,
  "last_compaction_from": 158119,
  "last_compaction_to": 137700
}
```

The file is written by `save_state()` in `.claude/statusline.py` (lines 241-250). It uses a simple `json.dump()` with no atomic write or locking. The file path is configurable via `config["compaction"]["state_file"]` (default: `~/.claude/ecw-statusline-state.json`).

**Extension feasibility:** Adding `context_fill_percentage` is straightforward. `extract_context_info()` already computes `percentage` (line 421). The `save_state()` function just needs to include this field:

```python
# Current save_state() call in extract_compaction_info():
state["previous_context_tokens"] = current_context
save_state(config, state)

# Extended version:
state["previous_context_tokens"] = current_context
state["context_fill_percentage"] = percentage  # NEW
save_state(config, state)
```

However, this modification is in `.claude/statusline.py` — the user's copy of the ECW script. This is not a Jerry project file; it is user infrastructure. Changes here would require coordination with the user and are outside the bounded context of FEAT-001.

### Finding 2: Update Timing — Architecture Constraint

**Official documentation (code.claude.com/docs/en/statusline):**
> "Your script runs after each new assistant message, when the permission mode changes, or when vim mode toggles. Updates are debounced at 300ms."

**Hook documentation:**
> `UserPromptSubmit` fires before the user's prompt is sent to Claude for processing.

**Event sequence per turn:**

```
Turn N-1:
  1. User submits prompt N-1
  2. UserPromptSubmit hook fires [reads state file: from turn N-2]
  3. Claude processes prompt N-1
  4. Assistant response N-1 is rendered
  5. Status line updates (runs statusline.py with response N-1 data)
  6. statusline.py writes state file [contains context from turn N-1 response]

Turn N:
  1. User submits prompt N
  2. UserPromptSubmit hook fires [reads state file: from turn N-1 response] <-- ONE TURN LAG
  3. Claude processes prompt N
  ...
```

**Measured timing data:**
- State file last modified: `2026-02-20 01:54:10` local (approx 09:54 UTC)
- Last transcript `assistant` entry timestamp: `2026-02-20T09:52:57` UTC
- Delta: approximately 72 seconds (includes user think time between turns)

**Key finding:** At `UserPromptSubmit` time, the state file reliably reflects the context state from the **end of the previous assistant turn**. This is **not** the context state at the start of the current user prompt (which includes any additional context from the user's message itself). For Claude's cached sessions, the difference is small (a few hundred tokens for the user message). For sessions with large tool results or file reads in the user turn, the difference could be several thousand tokens.

### Finding 3: Reliability and Race Condition Risk

The state file is written without atomic I/O (no temp file + rename pattern). A concurrent hook read while the statusline script is writing creates a risk of reading a partial JSON file. In practice, the statusline writes a small file (under 200 bytes) and writes happen infrequently, so corruption is unlikely but not impossible.

The `load_state()` function already handles this gracefully:
```python
except (json.JSONDecodeError, OSError) as e:
    debug_log(f"State load error: {e}")
return {"previous_context_tokens": 0, "last_compaction_from": 0, "last_compaction_to": 0}
```

A hook reading from this file would need similar error handling and graceful degradation.

### Finding 4: Method C vs. Method A Comparison

| Dimension | Method A (transcript JSONL, corrected) | Method C (state file relay) |
|-----------|----------------------------------------|----------------------------|
| Data freshness | Last assistant entry — same turn lag as state file | One turn lag (state from previous turn) |
| Field accuracy | All three usage fields available | Only `previous_context_tokens` (total tokens, not percentage) |
| Dependency | `$TRANSCRIPT_PATH` env var (available in all hooks) | `~/.claude/ecw-statusline-state.json` (user file, not in repo) |
| Reliability | Fail-open if transcript not found | Fail-open if state file not found |
| Implementation complexity | Moderate (backward seek + JSON parse) | Low (read + JSON parse) |
| Requires user file modification | No | Yes (to add `context_fill_percentage`) |
| Works without statusline.py installed | Yes | No |

**Conclusion:** Method C is architecturally feasible but strictly weaker than corrected Method A:
- It requires modifying user infrastructure (`.claude/statusline.py`) that is outside the project boundary
- It provides no lower latency advantage (both reflect the previous turn's state)
- It introduces a dependency on the user having the ECW statusline installed and configured
- The state file currently only stores `previous_context_tokens` (raw token count) not `context_fill_percentage` — requiring schema extension

The only scenario where Method C provides value over corrected Method A is if `$TRANSCRIPT_PATH` is unavailable or the transcript JSONL parsing proves unreliable. Given that `$TRANSCRIPT_PATH` is explicitly documented as a standard field in all hook event payloads (`transcript_path` in the hook stdin JSON), this contingency is unlikely.

### Finding 5: State File Temporal Accuracy Assessment

**Current session data:**
- State file `previous_context_tokens` = 145,220
- Corrected transcript total (last assistant entry) = 158,119
- Delta = 12,899 tokens (8.6% difference)

This 12,899 token gap represents context growth **within the current session** between when the state file was last written and when the current transcript snapshot was taken. At a 200,000 token context window, this represents ~6.4 percentage points of fill estimation error. At WARNING threshold (70%), this error could cause the monitor to display 63.6% (NOMINAL) when the actual state is 79.1% (WARNING). The state file is not sufficiently accurate for tier boundary decisions near thresholds.

---

## Recommendations

### Recommendation 1: Fix JsonlTranscriptReader Before EN-006 (REQUIRED)

**Action:** Update `JsonlTranscriptReader.read_latest_tokens()` before EN-006 implementation proceeds. The current implementation will cause `ContextFillEstimator` to return NOMINAL fill for all real sessions.

**Required changes in `src/context_monitoring/infrastructure/adapters/jsonl_transcript_reader.py`:**

1. The backward-seek strategy is sound. Keep it.
2. Change the extraction logic to search backwards for the last `assistant` type entry with `message.usage` present.
3. Return the sum of all three usage fields, not just `input_tokens`.

**Minimal corrected extraction (within `_extract_complete_last_line` or a new helper):**

```python
# When an assistant entry with usage is found:
data = json.loads(line)
if data.get("type") == "assistant":
    message = data.get("message", {})
    usage = message.get("usage", {})
    if usage:
        inp = usage.get("input_tokens", 0)
        cc = usage.get("cache_creation_input_tokens", 0)
        cr = usage.get("cache_read_input_tokens", 0)
        return inp + cc + cr  # total cumulative context
```

4. Update the port interface `ITranscriptReader` if it has a docstring that references "input_tokens" semantics.
5. Update `ContextFillEstimator` which may call `read_latest_tokens()` and expect it to return a value suitable for dividing by `context_window_size`. The TOTAL (not the marginal `input_tokens`) is the correct divisor input.
6. Update unit test fixtures in `test_jsonl_transcript_reader.py` to use realistic Claude Code entry format (not flat `{"input_tokens": N}`).

**Approximate effort:** 1–2 hours including test updates.

### Recommendation 2: Update ITranscriptReader Protocol Semantics

The current `ITranscriptReader` protocol returns a value named `input_tokens`. The port interface should be updated to clarify the semantic:

```python
def read_latest_tokens(self, transcript_path: str) -> int:
    """Read the TOTAL cumulative context window usage from the latest assistant entry.

    Returns: sum of input_tokens + cache_creation_input_tokens + cache_read_input_tokens
             from the most recent 'assistant' type entry in the transcript.
             This represents the total tokens filling the context window.
    """
```

This prevents future confusion between "marginal fresh tokens for last API call" (the Anthropic API `input_tokens` field) vs "cumulative context window fill" (what the reader returns).

### Recommendation 3: Defer Method C

**Action:** Do NOT modify `.claude/statusline.py` or depend on the state file for EN-006 or EN-007.

**Rationale:**
- Method A (corrected transcript reading) provides equivalent or better accuracy with fewer dependencies
- Method C requires modifying user infrastructure outside the project boundary
- The one-turn lag affects both methods equally; neither provides exact pre-prompt context
- If Method C is reconsidered in a future spike, the proto-design is: extend `save_state()` to write `context_fill_percentage`, add a `ContextStateFileReader` adapter, have it fall back gracefully to NOMINAL if file is absent

### Recommendation 4: Update EN-006 Context Fill Estimation Spec

**For EN-006 implementers:** The `HooksPromptSubmitHandler` will call `ContextFillEstimator.estimate(transcript_path)`. The transcript path comes from the hook stdin JSON field `transcript_path` (not `TRANSCRIPT_PATH` env var). Both are available; prefer the stdin JSON field as it is the documented API.

**Hook stdin JSON field (from official docs):**
```json
{
  "transcript_path": "/path/to/transcript.jsonl",
  "session_id": "abc123",
  ...
}
```

The `ContextFillEstimator` receives this path, calls `JsonlTranscriptReader.read_latest_tokens()` (corrected), and computes `fill_percentage = total_tokens / 200000.0`.

**The current EN-004 tier boundary examples in the acceptance criteria are correct:**
- `100000 / 200000 = 0.50 = NOMINAL` — but this assumed `input_tokens=100000` directly. After the fix, this test should use a fixture where `cc + cr = 99999` and `input_tokens = 1` (summing to 100,000) to realistically represent cached session data.

### Recommendation 5: Add One Regression Test

After fixing `JsonlTranscriptReader`, add one integration-style test that uses a realistic Claude Code JSONL fixture (with nested `message.usage` structure and mixed entry types including `progress`, `user`, and `assistant` types). This test would have caught the format mismatch before implementation.

---

## Evidence

### Source Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `src/context_monitoring/infrastructure/adapters/jsonl_transcript_reader.py` | Current implementation analysis |
| 2 | `tests/unit/context_monitoring/infrastructure/test_jsonl_transcript_reader.py` | Test fixture format analysis |
| 3 | `.claude/statusline.py` | ECW statusline, lines 241-250 (state file), 403-423 (context extraction), 463-506 (compaction detection) |
| 4 | `.claude/settings.json` | statusLine configuration |
| 5 | `projects/.../orchestration/spike002-.../res/phase-1-audit/cli-auditor/cli-capability-audit.md` | C8 section (prior ECW statusline analysis) |

### Live Data Sources

| # | Data Source | Content |
|---|-------------|---------|
| 1 | `/Users/anowak/.claude/projects/...2a18d762.../2a18d762-c8b0-47b2-9d1b-7d3616a2c065.jsonl` | 3,374-line production transcript; confirmed zero top-level `input_tokens` entries |
| 2 | `/Users/anowak/.claude/ecw-statusline-state.json` | State file: `previous_context_tokens=145220`, last written 2026-02-20T01:54 local |

### External References

| # | Reference | Key Finding |
|---|-----------|-------------|
| 1 | Claude Code statusLine docs (code.claude.com/docs/en/statusline) | Official JSON schema confirms `context_window.current_usage.{input_tokens, cache_creation_input_tokens, cache_read_input_tokens}` structure; `used_percentage = sum(all three) / context_window_size` |
| 2 | Anthropic Claude Code library (Context7) | Hook input format confirms `transcript_path` is a standard field in all hook payloads |

### Key Numerical Evidence

| Measurement | Value | Source |
|-------------|-------|--------|
| Top-level `input_tokens` in 3,374-line transcript | 0 entries | Live transcript scan |
| `assistant` entries with nested `message.usage` | 1,008 entries | Live transcript scan |
| Last line entry type | `queue-operation` | Live transcript scan |
| Last assistant `input_tokens` (marginal) | 1 | Live transcript (would be returned by current faulty reader) |
| Last assistant total (input + cc + cr) | 158,119 | Live transcript (correct fill estimate) |
| Correct fill percentage | 79.1% (WARNING tier) | 158,119 / 200,000 |
| State file `previous_context_tokens` | 145,220 | State file read |
| Gap between state file and transcript | 12,899 tokens / 6.4% | Measurement |

---

## Self-Review (S-010)

- [x] Both research questions answered with specific evidence from live data
- [x] OQ-9 finding is a hard BLOCKER with exact failure mode described
- [x] Method C timing analysis uses documented statusLine update timing (official docs)
- [x] Recommendations are actionable with specific code changes identified
- [x] EN-006 and EN-007 integration impact is addressed
- [x] All claims supported by file line references or live data measurements
- [x] Navigation table present (H-23/H-24 compliance)
- [x] No source code modified (research only per task spec)

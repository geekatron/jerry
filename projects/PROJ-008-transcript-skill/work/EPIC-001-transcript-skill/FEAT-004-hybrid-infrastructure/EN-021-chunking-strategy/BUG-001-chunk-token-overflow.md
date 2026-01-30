# BUG-001: Chunk Token Count Exceeds Claude Code Read Tool Limit

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-01-30
PURPOSE: Document defect where chunk files exceed 25,000 token Read tool limit
-->

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-01-30T08:15:00Z
> **Due:** TBD
> **Completed:** TBD
> **Parent:** EN-021
> **Owner:** Claude
> **Found In:** v2.0.0 (Hybrid Infrastructure)
> **Fix Version:** TBD (EN-026)

---

## Frontmatter

```yaml
id: "BUG-001"
work_type: BUG
title: "Chunk Token Count Exceeds Claude Code Read Tool Limit"
classification: ENABLER
status: pending
resolution: null
priority: high
impact: high
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T08:15:00Z"
updated_at: "2026-01-30T08:15:00Z"
completed_at: null
parent_id: "EN-021"
tags: ["bug", "chunking", "token-limit", "read-tool", "blocking"]
severity: major
found_in_version: "v2.0.0"
fix_version: null
reproduction_steps: |
  1. Parse a VTT file with 700+ segments
  2. Observe chunk-001.json file size
  3. Attempt to read with Claude Code Read tool
environment: |
  Claude Code CLI, Read tool with 25,000 token limit
root_cause: |
  Chunking algorithm uses segment count (500) not token count
acceptance_criteria: |
  All generated chunks must be under 25,000 tokens (targeting 18,000 with safety margin)
```

---

## Summary

The TranscriptChunker generates chunk files that exceed Claude Code's Read tool token limit of **25,000 tokens**. A 500-segment chunk produces approximately **49,377 tokens**, which is **197% of the allowed limit**.

**Key Details:**
- **Symptom:** Claude Code Read tool fails with "File content exceeds maximum allowed tokens (25000)"
- **Frequency:** Every transcript with 500+ segments per chunk
- **Workaround:** Manually process smaller files or use offset/limit parameters

---

## Reproduction Steps

### Prerequisites

- Claude Code CLI installed
- VTT file with 700+ segments (e.g., 37-minute meeting)
- Python environment with `uv run jerry transcript parse` command

### Steps to Reproduce

1. Parse a VTT file:
   ```bash
   uv run jerry transcript parse "/path/to/meeting.vtt" --output-dir "/output/dir"
   ```

2. Check the generated chunk file size:
   ```bash
   wc -c /output/dir/chunks/chunk-001.json
   # Result: ~200KB
   ```

3. Attempt to read with Claude Code Read tool (or observe agent failure)

### Expected Result

Chunk files should be under **25,000 tokens** to be readable by Claude Code's Read tool.

### Actual Result

chunk-001.json contains **49,377 tokens** (measured), which is **~2x the limit**.

**Evidence from live test (2026-01-30):**
- Input: `Let's-chat-internal-sample-and-dual-bindings-for-Defense-in-Depth.vtt`
- Total segments: 710
- chunk-001.json: 500 segments, 4,843 words, **49,377 tokens**
- chunk-002.json: 210 segments, 2,012 words, ~20,000 tokens (estimated)

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS Darwin 25.2.0 |
| **Runtime** | Python 3.11+ with UV |
| **Application Version** | jerry transcript v2.0.0 |
| **Configuration** | Default chunk_size=500 segments |
| **Deployment** | Local development |

### Additional Environment Details

- Claude Code Read tool limit: **25,000 tokens** ([GitHub Issue #4002](https://github.com/anthropics/claude-code/issues/4002))
- Claude Code file size limit: **256KB** ([GitHub Issue #17394](https://github.com/anthropics/claude-code/issues/17394))
- Observed token ratio: ~10.2 tokens per word (including JSON structure overhead)

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| Live parsing output | Log | 710 segments → 2 chunks, chunk-001 at 49K tokens | 2026-01-30 |
| index.json | File | Shows 500 segments in chunk-001 with 4,843 words | 2026-01-30 |
| GitHub Issue #4002 | Reference | Confirms 25K token Read tool limit | 2026-01-30 |

### Fix Verification

<!--
Complete this section when status changes to completed.
-->

| Verification | Method | Result | Verified By | Date |
|--------------|--------|--------|-------------|------|
| All chunks under 18K tokens | Token count | pending | - | - |
| Existing tests still pass | pytest | pending | - | - |
| New token-based tests pass | pytest | pending | - | - |

### Verification Checklist

- [ ] All generated chunks under 25,000 tokens
- [ ] Safety margin maintained (target: 18,000 tokens)
- [ ] Regression test added for token limits
- [ ] index.json schema updated with `target_tokens` field

---

## Root Cause Analysis

### Investigation Summary

The TranscriptChunker in `src/transcript/application/services/chunker.py` uses a **segment-based** chunking strategy with a fixed size of 500 segments per chunk. This approach does not account for:

1. **Variable segment length** - Segments can vary from 1 word to 50+ words
2. **JSON serialization overhead** - Each segment adds ~100 characters of JSON structure
3. **Token count variance** - Token-to-word ratio varies (typically 1.0-1.5 for English)

### Root Cause

**Segment-based chunking with fixed count (500) ignores token limits.**

The chunker was designed based on segment count for simplicity (EN-021), but the acceptance criteria "Each chunk file <= 500 segments" (AC-2) did not include a token limit constraint.

### Contributing Factors

1. **Missing NFR**: No token limit requirement was specified in EN-021
2. **Research gap**: Claude Code Read tool limit (25K) was not researched during EN-021 design
3. **Assumption**: Assumed 500 segments would produce reasonable file sizes

---

## Fix Description

<!--
REQUIRED when status is completed.
Document the fix that was applied.
-->

### Solution Approach

Implement **token-based chunking** using `tiktoken` library with `p50k_base` encoding (best approximation for Claude per research). Target **18,000 tokens** per chunk (25% safety margin below 25K limit).

**Detailed fix tracked in:** [EN-026: Token-Based Chunking](../../FEAT-003-future-enhancements/EN-026-token-based-chunking/EN-026-token-based-chunking.md)

### Changes Required

1. Add `tiktoken` dependency to `pyproject.toml`
2. Refactor `TranscriptChunker` to use token counting
3. Update `index.json` schema with `target_tokens` field
4. Add unit tests for token-based chunking
5. Add integration tests with real VTT files
6. Add contract tests for new schema

### Code References

| File | Change Description |
|------|-------------------|
| `src/transcript/application/services/chunker.py` | Replace segment-based with token-based chunking |
| `pyproject.toml` | Add tiktoken dependency |
| `skills/transcript/test_data/schemas/index.schema.json` | Add target_tokens field |

---

## Acceptance Criteria

### Fix Verification

- [ ] All generated chunks are under 25,000 tokens
- [ ] Target token count is 18,000 (25% safety margin)
- [ ] tiktoken `p50k_base` encoding used for token counting
- [ ] index.json includes `target_tokens` field
- [ ] Bug no longer reproducible with original VTT file

### Quality Checklist

- [ ] Unit tests for token-based chunking added
- [ ] Integration tests with real VTT files added
- [ ] Contract tests for updated schema added
- [ ] Existing tests still passing
- [ ] Documentation updated (SKILL.md, EN-021)

---

## Related Items

### Hierarchy

- **Parent:** [EN-021: Chunking Strategy](./EN-021-chunking-strategy.md)

### Related Items

- **Fix Enabler:** [EN-026: Token-Based Chunking](../../FEAT-003-future-enhancements/EN-026-token-based-chunking/EN-026-token-based-chunking.md)
- **Research Source:** [GitHub Issue #4002 - 25K token limit](https://github.com/anthropics/claude-code/issues/4002)
- **Research Source:** [Token Counting Guide 2025](https://www.propelcode.ai/blog/token-counting-tiktoken-anthropic-gemini-guide-2025)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-30 | Claude | pending | Bug discovered during live transcript parsing. chunk-001.json at 49K tokens exceeds 25K limit. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |

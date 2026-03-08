# Phase 5B — Security Review

> **Generated:** 2026-03-08
> **Scope:** FEAT-036-004 Baseline Execution Pipeline (scripts + CI/CD workflows)
> **Reviewer:** eng-qa (automated review)

## Document Sections

| Section | Purpose |
|---------|---------|
| [API Key Handling](#api-key-handling) | ANTHROPIC_API_KEY management |
| [Secret Redaction](#secret-redaction) | Credential stripping before persistence |
| [Input Sanitization](#input-sanitization) | MC-02 CWE-20 compliance |
| [Path Traversal](#path-traversal) | File path construction safety |
| [CI/CD Secret Isolation](#cicd-secret-isolation) | GitHub Actions secret handling |
| [Findings Summary](#findings-summary) | Consolidated risk table |

---

## API Key Handling

**Status: PASS**

All four baseline scripts (`baseline_runner.py`, `baseline_scorer.py`, `baseline_mr_runner.py`, `baseline_stats.py`) follow the same pattern:

- API key sourced exclusively from `ANTHROPIC_API_KEY` environment variable
- No hardcoded keys, no config file key loading, no CLI argument key passing
- `baseline_stats.py` makes zero API calls (pure statistics)
- Scripts fail with explicit error if env var is missing

**CI/CD alignment:**
- Smoke workflow: intentionally does NOT inject `ANTHROPIC_API_KEY` (FR-005: no LLM calls)
- Standard workflow: injects via `secrets.ANTHROPIC_API_KEY` with `::add-mask::` (MC-31)
- Full workflow: same secret injection with masking + Langfuse key masking

---

## Secret Redaction

**Status: PASS**

All scripts that persist LLM I/O traces apply `_redact_secrets()` before writing to disk:

| Script | Redaction Points | Patterns Covered |
|--------|-----------------|------------------|
| `baseline_runner.py` | system_prompt, user_prompt, raw_response | `sk-ant-*`, `sk-*`, `ANTHROPIC_API_KEY=*`, `api_key=*` |
| `baseline_scorer.py` | scoring trace text | Same 4 patterns |
| `baseline_mr_runner.py` | system_prompt, user_prompt, raw_response, results JSON | Same 4 patterns |
| `baseline_stats.py` | N/A (no LLM I/O) | N/A |

**Verification:** Phase 1 acceptance criteria AC-1.3 ("Zero credentials in persisted artifacts") was verified against all 9 I/O trace files.

---

## Input Sanitization

**Status: PASS**

- `baseline_runner.py` applies `_sanitize_text()` to user prompts (null byte stripping, CR normalization, length truncation)
- `DeepEvalAdapter._sanitize_input()` applies MC-02 sanitization to all inputs before LLM judge calls
- Unit tests in `tests/prompt-regression/unit/test_input_sanitization.py` verify: null byte stripping, CR normalization, truncation, type safety (14 test cases)
- `_MAX_INPUT_CHARS = 10_000` enforced per MC-06 payload size limit

---

## Path Traversal

**Status: LOW RISK (no unmitigated findings)**

File paths in I/O trace storage use `prompt_id` and `agent_name` as path components:
```python
trace_dir = output_dir / "io-traces" / agent_name / prompt_id
```

**Mitigating factors:**
1. `agent_name` comes from CLI `--agents` argument (operator-controlled, not user-supplied)
2. `prompt_id` comes from YAML prompt files under source control (`tests/prompt-regression/baselines/prompts/`)
3. `output_dir` comes from CLI `--output-dir` argument (operator-controlled)
4. No user-supplied input reaches file path construction at runtime

**Recommendation:** For defense-in-depth if these scripts are ever exposed to untrusted input, add path component validation (reject `/`, `..`, null bytes in agent_name/prompt_id). Current risk is LOW because all inputs are operator-controlled.

---

## CI/CD Secret Isolation

**Status: PASS**

| Control | Smoke | Standard | Full | Status |
|---------|-------|----------|------|--------|
| MC-07: Docker read-only filesystem | Yes | Yes | Yes | PASS |
| MC-08: SHA-256 pinned image | Yes | Yes | Yes | PASS |
| MC-10: Read-only config mounts | Yes | Yes | Yes | PASS |
| MC-13: Memory/CPU resource limits | 512m/1CPU | 2g/2CPU | 4g/4CPU | PASS |
| MC-14: no-new-privileges + cap-drop=ALL | Yes | Yes | Yes | PASS |
| MC-28: `pull_request` event (not `pull_request_target`) | Yes | Yes | N/A (dispatch) | PASS |
| MC-31: Secret masking via `::add-mask::` | N/A (no secrets) | Yes | Yes | PASS |
| MC-32: Concurrency group | Yes | Yes | Yes | PASS |
| MC-33: Minimal permissions | Yes | Yes | Yes | PASS |
| MC-09: Output validation before consumption | Yes | Yes | Yes | PASS |

**Fork PR handling (MC-28):**
- Smoke: runs without secrets (structural only)
- Standard: detects fork PRs and falls back to smoke-only mode with PR comment explaining limitation
- Full: not triggered by PRs (dispatch/schedule only)

**Action version pinning:**
- `actions/checkout@v4.2.2` — SHA-pinned
- `actions/upload-artifact@v4.6.2` — SHA-pinned
- `actions/github-script@v7.0.1` — SHA-pinned
- `astral-sh/setup-uv@v5.4.1` — SHA-pinned

---

## Findings Summary

| ID | Finding | Severity | Status | Mitigation |
|----|---------|----------|--------|------------|
| SEC-001 | Path components use operator-controlled inputs only | Low | Mitigated | Inputs from CLI args and source-controlled YAML files |
| SEC-002 | `_MAX_OUTPUT_CHARS = 8000` truncation affects score accuracy | Informational | Known limitation | Documented in phase2-composites.json notes; relative comparisons remain valid |
| SEC-003 | All Docker images SHA-256 pinned | N/A | PASS | Supply chain integrity maintained |
| SEC-004 | Secret redaction covers 4 regex patterns | N/A | PASS | Covers Anthropic key formats |

**Overall: No unmitigated critical or high findings.**

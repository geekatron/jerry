# Final Synthesis: PROJ-007 Performance and Plugin Bug Investigations

> **Synthesizer:** ps-synthesizer
> **Date:** 2026-01-14
> **Workflow:** perf-plugin-investigation-20260114-001
> **Status:** COMPLETE

---

## Executive Summary

This synthesis consolidates the findings from a comprehensive multi-agent investigation into two critical bugs in the Jerry Framework: BUG-001 (lock file accumulation causing performance degradation) and BUG-002 (plugin failing to load via `--plugin-dir`). Both investigations passed quality review gates with scores of 0.91, and their proposed architectural solutions passed cross-validation with an overall score of 0.93.

**BUG-001** stems from a technical debt item acknowledged in ADR-006 but never implemented: the `AtomicFileAdapter` creates lock files for POSIX locking but lacks cleanup mechanisms. This has resulted in 97+ lock files accumulating in `.jerry/local/locks/`. The proposed fix is a hybrid approach combining eager cleanup after each operation with periodic garbage collection for crash recovery.

**BUG-002** is a more critical issue where the Jerry plugin silently fails to load. The root cause is a semantic conflict between PEP 723 inline script metadata (declaring `dependencies = []`) and the script's actual package imports (`from src.infrastructure...`). When `uv run` executes the script, it creates an isolated environment where these imports fail. The fix is a single-line change to use `python -m` instead of `uv run`, bypassing the isolation issue entirely.

Both bugs represent different failure modes in the development process: BUG-001 is technical debt that accumulated over time, while BUG-002 is an integration oversight introduced during PROJ-005. The investigations provide actionable fixes with clear implementation plans, with BUG-002 requiring immediate attention (P0, severity HIGH) and BUG-001 scheduled for short-term resolution (P2, severity MEDIUM).

---

## Investigation Overview

### Bugs Investigated

| Bug ID | Severity | Title | Root Cause | Proposed Fix |
|--------|----------|-------|------------|--------------|
| BUG-001 | MEDIUM | Lock file accumulation in `.jerry/local/locks/` | `AtomicFileAdapter` creates lock files but cleanup mechanism from ADR-006 was never implemented | Hybrid approach: eager cleanup after operations + periodic garbage collection + CLI command |
| BUG-002 | HIGH | Jerry plugin not loading via `--plugin-dir` | PEP 723 metadata (`dependencies = []`) conflicts with package imports; `uv run` creates isolated environment ignoring PYTHONPATH | Change hook command from `uv run` to `python -m` module execution |

### Workflow Metrics

| Phase | Status | Score | Agents |
|-------|--------|-------|--------|
| Investigation | COMPLETE | N/A | 2 (ps-investigator x2) |
| Review Gate | COMPLETE | 0.91 avg | 2 (ps-reviewer x2) |
| Generator-Critic | SKIPPED | N/A | 0 (both investigations passed threshold) |
| Architecture | COMPLETE | N/A | 2 (ps-architect x2) |
| Cross-Validation | COMPLETE | 0.93 | 1 (ps-validator) |
| Synthesis | COMPLETE | N/A | 1 (ps-synthesizer) |
| **Total** | | | **8** |

---

## Bug Analysis Deep Dive

### BUG-001: Lock File Accumulation

#### Problem

The Jerry Framework's `AtomicFileAdapter` creates lock files in `.jerry/local/locks/` to enable safe concurrent file access via POSIX `fcntl.lockf()` locking. These lock files are 0-byte sentinel files used for coordination between processes. However, these files are created but **never deleted** after the lock is released.

**Symptoms Observed:**
- 97+ lock files accumulated in `.jerry/local/locks/`
- All files are 0 bytes (SHA256 hash-based naming)
- Slight performance degradation during directory operations
- Risk of filesystem inode exhaustion on long-running systems

#### Root Cause

**5 Whys Summary:**

1. **Why are lock files accumulating?** - The `AtomicFileAdapter.read_with_lock()` creates files but never removes them after releasing the lock.
2. **Why doesn't the adapter delete lock files?** - A deliberate design decision from ADR-006 to avoid race conditions, deferring cleanup to a "separate mechanism."
3. **Why was the cleanup mechanism never implemented?** - ADR-006 listed it as a "Negative Consequence" but no work item was created to track implementation.
4. **Why wasn't this caught earlier?** - Lock files are 0 bytes (no disk alerts), no monitoring for file count, `.jerry/local/` typically ignored in reviews.
5. **Why is there no garbage collection?** - The architecture deferred this to a CLI command that was documented but never built.

**Ishikawa Categories (Key Factors):**
- **Method:** No cleanup step in lock/unlock flow
- **Machine:** POSIX fcntl semantics don't manage file lifecycle
- **Material:** 0-byte files invisible to monitoring
- **Man:** ADR authors deferred implementation; no work item created
- **Measurement:** No metrics on lock file count
- **Environment:** Long-running sessions accumulate more locks

**FMEA Highest Risk (RPN > 100):**
- Directory listing slow (RPN 168) - users experience delays accessing `.jerry/local/`

#### Proposed Solution

ADR-PROJ007-001 proposes a **Hybrid Approach** combining:

1. **Eager Cleanup:** `_cleanup_lock_file()` method called after each operation
   - Uses non-blocking lock attempt to verify file is unused before deletion
   - Best-effort (failures are silent, don't affect operation success)

2. **Garbage Collection:** `LockFileGarbageCollector` service
   - Runs at session start (non-blocking)
   - Removes lock files older than 5 minutes
   - Respects currently held locks

3. **CLI Command:** `jerry maintenance cleanup-locks`
   - Manual intervention for administrators
   - Logs count of files removed

**Why This Option Was Chosen:**
- Immediate cleanup prevents accumulation under normal operations
- GC handles crashed process cleanup (primary ADR-006 concern)
- CLI provides manual override for edge cases
- Defense in depth with two complementary mechanisms

#### Implementation Plan

| Phase | Priority | Deliverable | Effort |
|-------|----------|-------------|--------|
| 1 | HIGH | Add `_cleanup_lock_file()` to `AtomicFileAdapter` | ~15 lines |
| 2 | MEDIUM | Create `LockFileGarbageCollector` in `lock_gc.py` | ~30 lines |
| 3 | HIGH | Unit + integration + E2E tests | Comprehensive |

**Files to Modify:**
- `src/infrastructure/adapters/persistence/atomic_file_adapter.py`
- `src/infrastructure/internal/lock_gc.py` (new file)
- `scripts/session_start.py` (GC integration point)

---

### BUG-002: Plugin Not Loading

#### Problem

When users load the Jerry plugin using Claude Code's `--plugin-dir` option, nothing happens. The plugin silently fails to initialize - no welcome message, no project context, Jerry's features are unavailable.

**Command Used:**
```bash
JERRY_PROJECT=PROJ-007-jerry-bugs claude --plugin-dir=/path/to/jerry
```

**Expected:** `<project-context>` or `<project-required>` output
**Actual:** Silent failure, no output

#### Root Cause

**5 Whys Summary:**

1. **Why doesn't the plugin load?** - The SessionStart hook produces no output when the script fails silently.
2. **Why does the script fail silently?** - `uv run` creates an isolated environment where `from src.infrastructure...` imports fail with `ModuleNotFoundError`.
3. **Why do the imports fail?** - `uv run` with PEP 723 metadata (`dependencies = []`) creates an environment with only declared dependencies; the Jerry package is not installed.
4. **Why doesn't PYTHONPATH help?** - `uv run` with inline script metadata ignores `PYTHONPATH`; it overrides with its own isolated environment.
5. **Why was this design chosen?** - PROJ-005 added `uv run` support without accounting for the conflict between "standalone script" semantics (PEP 723) and "package module" semantics (importing from `src/`).

**The Conflict:**

The hook sets: `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py`

But `session_start.py` contains:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from src.infrastructure.adapters.configuration.layered_config_adapter import LayeredConfigAdapter
# ... more package imports
```

Per PEP 723, `uv run` creates an isolated environment with **only** declared dependencies (`[]`). The package imports fail, the script terminates before `main()`, and no output is produced.

**FMEA Highest Risk (RPN = 243):**
- PEP 723 conflicts with package imports - the core issue

#### Proposed Solution

ADR-PROJ007-002 proposes **Option 1: Use `python -m` Instead of `uv run`**

**Before (hooks.json line 10):**
```json
"command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

**After (hooks.json line 10):**
```json
"command": "cd ${CLAUDE_PLUGIN_ROOT} && python -m src.interface.cli.session_start"
```

**Why This Option Was Chosen:**
- **Minimal change:** Single line modification
- **Immediate fix:** Can be tested in minutes
- **No code duplication:** Keeps single source of truth
- **Guaranteed Python availability:** `python` is always present
- **No installation friction:** Plugin remains self-contained

**Why Other Options Were Rejected:**
- **Option 2 (Entry Point):** Requires `pip install -e .` - breaks self-contained requirement
- **Option 3 (Standalone Rewrite):** ~400 lines to rewrite, creates maintenance burden

#### Implementation Plan

| Step | Priority | Action | Timeline |
|------|----------|--------|----------|
| 1 | REQUIRED | Update `hooks/hooks.json` line 10 | Immediate (5 min) |
| 2 | RECOMMENDED | Add error handling wrapper to `session_start.py` | 30 min |
| 3 | OPTIONAL | Remove or clarify PEP 723 metadata | 10 min |
| 4 | REQUIRED | Add integration test for plugin load | 30 min |

---

## Cross-Cutting Concerns

### Architectural Insights

1. **Layer Separation is Preserved:** The two bugs exist in different hexagonal architecture layers:
   - BUG-001: Infrastructure layer (`AtomicFileAdapter`)
   - BUG-002: Interface layer (hooks, CLI entry point)
   - This separation means the fixes have **zero file overlap** and can be developed in parallel

2. **Defense in Depth Matters:** BUG-001's hybrid cleanup approach (eager + GC) demonstrates the value of multiple safeguards. BUG-002's silent failure shows the danger of single points of failure without diagnostics.

3. **POSIX Lock Semantics Are Advisory:** The lock files are just coordination mechanisms; the actual POSIX locks are released when file handles close. This is why cleanup is safe - we're removing the sentinel file, not the lock itself.

### Process Insights

1. **Technical Debt Tracking:** BUG-001 was acknowledged in ADR-006 ("Lock file cleanup needed") but never tracked as a work item. **Lesson:** Every "Negative Consequence" in an ADR should generate a tracked work item.

2. **Integration Testing Gaps:** BUG-002 shipped without integration tests for the plugin load flow. **Lesson:** Hook/plugin combinations need E2E testing with the actual runtime environment.

3. **Silent Failures Are Dangerous:** BUG-002's silent failure made debugging harder than necessary. **Lesson:** Always add diagnostic output, especially for hook execution.

4. **Semantic Conflicts Between Tools:** BUG-002's `uv run` + PEP 723 conflict shows how combining tools can create unexpected interactions. **Lesson:** Document tool-specific behaviors and test edge cases.

### Technical Debt Identified

| Item | Source | Priority | Tracking |
|------|--------|----------|----------|
| ADR-006 cleanup mechanism | BUG-001 investigation | P2 | ADR-PROJ007-001 |
| ADR e-010 caveats for PEP 723 | BUG-002 investigation | P3 | Documentation update needed |
| Plugin integration tests | BUG-002 investigation | P1 | Test suite expansion |
| Lock file metrics/monitoring | BUG-001 FMEA | P3 | Observability improvement |

---

## Implementation Roadmap

### Priority Matrix

| Priority | Bug | ADR | Effort | Risk | Timeline |
|----------|-----|-----|--------|------|----------|
| P0 | BUG-002 | ADR-PROJ007-002 | LOW (1 line) | VERY LOW | Immediate (today) |
| P2 | BUG-001 | ADR-PROJ007-001 | MEDIUM (3 phases) | LOW | Next sprint |

### Recommended Order

1. **Implement ADR-PROJ007-002 first (BUG-002 fix)**
   - **Rationale:** Plugin not loading is severity HIGH - it blocks all Jerry functionality
   - **Action:** Apply one-line fix to `hooks/hooks.json`
   - **Verification:** Run `claude --plugin-dir=/path/to/jerry` and confirm `<project-context>` output

2. **Add error handling wrapper to session_start.py**
   - **Rationale:** Prevents future silent failures
   - **Action:** Wrap `main()` call in try/except with diagnostic output

3. **Implement ADR-PROJ007-001 Phase 1 (eager cleanup)**
   - **Rationale:** Stops new lock file accumulation immediately
   - **Action:** Add `_cleanup_lock_file()` method to `AtomicFileAdapter`

4. **Clean up existing lock files**
   - **Rationale:** Remove the 97+ accumulated files
   - **Action:** Manual cleanup: `find .jerry/local/locks -name "*.lock" -mmin +5 -delete`

5. **Implement ADR-PROJ007-001 Phase 2 (garbage collection)**
   - **Rationale:** Handles crash recovery scenarios
   - **Action:** Create `LockFileGarbageCollector`, integrate with session start

6. **Add comprehensive tests for both fixes**
   - **Rationale:** Prevent regression
   - **Action:** Unit, integration, and E2E tests per ADR specifications

### Quick Wins (Immediate Actions)

| Action | Time | Impact |
|--------|------|--------|
| Apply `hooks.json` one-line fix | 5 min | Unblocks plugin loading |
| Manual lock file cleanup | 2 min | Removes accumulated 97 files |
| Add error handling wrapper | 30 min | Prevents future silent failures |

### Follow-up Actions (Next Sprint)

| Action | Effort | Tracking |
|--------|--------|----------|
| Implement eager lock cleanup | 2 hours | Create work item from ADR-001 |
| Implement garbage collector | 4 hours | Create work item from ADR-001 |
| Plugin integration test suite | 4 hours | Test automation |
| Update ADR e-010 with caveats | 1 hour | Documentation |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Lock cleanup deletes active lock | Very Low | High | Non-blocking lock check before deletion |
| `python -m` doesn't find Python 3 | Low | Medium | Use `python3 -m` explicitly if needed |
| Eager cleanup race condition | Low | Medium | fcntl semantics ensure lock released before unlink |
| GC age threshold too aggressive | Low | Low | Configure threshold; default 5 minutes is conservative |
| Code conflict between ADR implementations | None | None | ADRs modify different files (verified in cross-validation) |

---

## Quality Summary

### Review Quality

Both investigations achieved quality scores of **0.91** (threshold: 0.85):

| Investigation | Score | Strengths | Minor Gaps |
|---------------|-------|-----------|------------|
| BUG-001 | 0.91 | Exceptional evidence quality, complete 5 Whys, dual root cause identification | Session_start.py path reference unclear, work item placeholders |
| BUG-002 | 0.91 | Excellent L0 clarity, rigorous evidence chain, actionable appendices | Owner fields TBD, rollback plan missing |

**Key Quality Indicators:**
- All claims backed by specific file paths and line numbers
- Each "Why" level logically builds on previous
- Both technical and process root causes identified
- Copy-paste-ready fixes provided

### Validation Quality

Cross-validation score: **0.93** (PASS)

| Criterion | ADR-001 | ADR-002 | Notes |
|-----------|---------|---------|-------|
| Root Cause Alignment | 0.95 | 0.96 | Direct traceability to investigation findings |
| No Conflicting Changes | 1.00 | 1.00 | Zero file overlap; different architecture layers |
| Backward Compatibility | 0.92 | 0.94 | No breaking changes identified |
| Implementation Feasibility | 0.90 | 0.95 | Both feasible with reasonable effort |
| Test Strategy Adequacy | 0.88 | 0.90 | Comprehensive test plans defined |

### Confidence Level

**HIGH** - Both investigations provide:
- Complete evidence chains with verifiable sources
- Clear root cause identification
- Multiple implementation options with trade-off analysis
- Validated non-conflicting solutions
- Defined testing strategies

The combination of rigorous investigation, quality review gates, and cross-validation provides high confidence in the proposed solutions.

---

## Recommendations

### For Immediate Implementation

1. **Apply BUG-002 fix today** - The one-line change to `hooks/hooks.json` unblocks all Jerry plugin functionality with minimal risk.

2. **Add error handling to session_start.py** - Prevents future silent failures and provides diagnostic output for debugging.

3. **Clean up accumulated lock files** - Manual cleanup removes the 97 files immediately while permanent fix is developed.

### For Process Improvement

1. **Track technical debt from ADRs** - Every "Negative Consequence" in an ADR should generate a work item. BUG-001 was acknowledged but never tracked.

2. **Add plugin integration tests to CI** - BUG-002 would have been caught by a test that loads the plugin via `--plugin-dir` and verifies output.

3. **Document tool-specific behaviors** - The `uv run` + PEP 723 interaction should be documented to prevent similar issues with other tools.

### For Future Prevention

1. **Require cleanup mechanisms in file-creating components** - Any component that creates files should have a defined lifecycle including cleanup.

2. **Add diagnostic output for hook failures** - Hooks should never fail silently; always emit diagnostic information to stderr or stdout.

3. **Test edge cases when combining tools** - Integration points between tools (`uv run` + PEP 723 + package imports) need explicit testing.

---

## Appendices

### A. Artifact Locations

| Artifact | Path |
|----------|------|
| Investigation BUG-001 | `projects/PROJ-007-jerry-bugs/investigations/bug-001-e-001-investigation.md` |
| Investigation BUG-002 | `projects/PROJ-007-jerry-bugs/investigations/bug-002-e-001-investigation.md` |
| Review BUG-001 | `projects/PROJ-007-jerry-bugs/reviews/bug-001-review.md` |
| Review BUG-002 | `projects/PROJ-007-jerry-bugs/reviews/bug-002-review.md` |
| ADR Lock File Cleanup | `projects/PROJ-007-jerry-bugs/decisions/ADR-PROJ007-001-lock-file-cleanup.md` |
| ADR Plugin Loading Fix | `projects/PROJ-007-jerry-bugs/decisions/ADR-PROJ007-002-plugin-loading-fix.md` |
| Cross-Validation Report | `projects/PROJ-007-jerry-bugs/orchestration/perf-plugin-investigation-20260114-001/validation/cross-validation-report.md` |
| Final Synthesis | `projects/PROJ-007-jerry-bugs/orchestration/perf-plugin-investigation-20260114-001/synthesis/final-synthesis.md` |
| Orchestration Plan | `projects/PROJ-007-jerry-bugs/orchestration/perf-plugin-investigation-20260114-001/ORCHESTRATION_PLAN.md` |

### B. Agent Execution Summary

| Role | Agent | Bug | Date | Quality Score | Output |
|------|-------|-----|------|---------------|--------|
| Investigator | ps-investigator v2.1.0 | BUG-001 | 2026-01-14 | N/A | investigations/bug-001-e-001-investigation.md |
| Investigator | ps-investigator v2.1.0 | BUG-002 | 2026-01-14 | N/A | investigations/bug-002-e-001-investigation.md |
| Reviewer | ps-reviewer | BUG-001 | 2026-01-14 | 0.91 (PASS) | reviews/bug-001-review.md |
| Reviewer | ps-reviewer v2.1.0 | BUG-002 | 2026-01-14 | 0.91 (PASS) | reviews/bug-002-review.md |
| Architect | ps-architect | BUG-001 | 2026-01-14 | N/A | decisions/ADR-PROJ007-001-lock-file-cleanup.md |
| Architect | ps-architect | BUG-002 | 2026-01-14 | N/A | decisions/ADR-PROJ007-002-plugin-loading-fix.md |
| Validator | ps-validator | Both | 2026-01-14 | 0.93 (PASS) | validation/cross-validation-report.md |
| Synthesizer | ps-synthesizer | Both | 2026-01-14 | N/A | synthesis/final-synthesis.md |

### C. References

| Reference | Type | URL/Path |
|-----------|------|----------|
| ADR-006 File Locking Strategy | Internal | `projects/PROJ-001-plugin-cleanup/design/ADR-006-file-locking-strategy.md` |
| ADR e-010 uv Session Start | Internal | Referenced in investigations |
| PEP 723 | External | https://peps.python.org/pep-0723/ |
| Claude Code Hooks | External | https://docs.anthropic.com/en/docs/claude-code/hooks |
| uv Script Dependencies | External | https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies |
| POSIX fcntl | External | https://man7.org/linux/man-pages/man2/fcntl.2.html |
| AtomicFileAdapter | Internal | `src/infrastructure/adapters/persistence/atomic_file_adapter.py` |
| session_start.py | Internal | `src/interface/cli/session_start.py` |
| hooks.json | Internal | `hooks/hooks.json` |

---

## Sign-Off

| Role | Agent | Date | Output |
|------|-------|------|--------|
| Investigator (BUG-001) | ps-investigator v2.1.0 | 2026-01-14 | investigations/bug-001-e-001-investigation.md |
| Investigator (BUG-002) | ps-investigator v2.1.0 | 2026-01-14 | investigations/bug-002-e-001-investigation.md |
| Reviewer (BUG-001) | ps-reviewer | 2026-01-14 | reviews/bug-001-review.md |
| Reviewer (BUG-002) | ps-reviewer v2.1.0 | 2026-01-14 | reviews/bug-002-review.md |
| Architect (BUG-001) | ps-architect | 2026-01-14 | decisions/ADR-PROJ007-001-lock-file-cleanup.md |
| Architect (BUG-002) | ps-architect | 2026-01-14 | decisions/ADR-PROJ007-002-plugin-loading-fix.md |
| Validator | ps-validator | 2026-01-14 | validation/cross-validation-report.md |
| Synthesizer | ps-synthesizer | 2026-01-14 | synthesis/final-synthesis.md |

---

*Synthesis completed: 2026-01-14*
*Generated by ps-synthesizer*
*Workflow: perf-plugin-investigation-20260114-001 v2.0.0*

# RUNBOOK-001: Plugin Regression Detection, Prevention & Mitigation

> **Runbook ID:** RUNBOOK-001
> **Version:** 1.0
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13
> **Owner:** Jerry Framework Team

---

## How to Use This Runbook

This document is organized into **four levels** that build on each other:

| Level | Audience | When to Use |
|-------|----------|-------------|
| **ELI5** | Anyone | "Something's broken, I need a quick fix" |
| **L1** | First Responders | "I need to diagnose and escalate properly" |
| **L2** | Technical Support | "I need to investigate the root cause" |
| **L3** | Engineers | "I need to fix the code and prevent recurrence" |

**Start at your level.** If you can't resolve the issue, move to the next level.

---

# ELI5: Quick Reference Card

> **ELI5** = "Explain Like I'm 5" - The simplest possible explanation.

## What is This?

When you start Claude Code with Jerry installed, you should see a startup message like:

```
Jerry Framework initialized. See CLAUDE.md for context.
```

**If you don't see this message, something is broken.**

## Quick Symptom Check

| What You See | What It Means | Quick Fix |
|--------------|---------------|-----------|
| No startup message at all | Hook isn't running | See L1 |
| "ModuleNotFoundError" | Missing dependency | Run: `uv sync` |
| "command not found: uv" | uv not installed | Install: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| "No such file" error | File path wrong | Check plugin is installed |

## The 30-Second Fix

Try this first:

```bash
# Go to the Jerry project folder
cd /path/to/jerry

# Run the hook manually to see what's wrong
PYTHONPATH="." uv run src/interface/cli/session_start.py
```

**If you see the startup message, the fix worked.**
**If you see an error, read the error and continue to L1.**

---

# L1: First Response Guide

> **L1 Support** handles basic troubleshooting using documented scripts.
> Goal: Resolve simple issues quickly OR escalate with proper context.

## L1 Prerequisites

Before troubleshooting, verify you have:

- [ ] Terminal access
- [ ] Access to the Jerry project folder
- [ ] 5-10 minutes available

## L1 Diagnostic Script

Run these commands in order. Stop when you find the problem.

### Step 1: Check if uv is installed

```bash
uv --version
```

**Expected:** Version number (e.g., `uv 0.5.x`)
**Problem:** "command not found" → Install uv first

### Step 2: Check if you're in the right folder

```bash
ls -la hooks/hooks.json
```

**Expected:** File exists
**Problem:** "No such file" → Navigate to Jerry project root

### Step 3: Check if the hook script exists

```bash
ls -la src/interface/cli/session_start.py
```

**Expected:** File exists
**Problem:** "No such file" → Plugin may be corrupted, reinstall

### Step 4: Run the hook manually

```bash
PYTHONPATH="." uv run src/interface/cli/session_start.py
```

**Expected:** Startup message with `<project-context>` or `<project-required>`
**Problem:** Error message → Record the error and continue to Step 5

### Step 5: Check dependencies

```bash
uv sync --extra dev --extra test
```

**Expected:** "Resolved X packages" or "All packages already installed"
**Problem:** Dependency errors → Record and escalate to L2

## L1 Escalation Criteria

**Escalate to L2 if:**

- [ ] Manual hook run shows Python import errors
- [ ] Error mentions missing modules
- [ ] Error mentions PYTHONPATH
- [ ] You've spent more than 15 minutes without resolution

## L1 Escalation Template

When escalating, provide:

```
## Issue Summary
[One sentence describing the problem]

## Environment
- OS: [macOS/Linux/Windows]
- Python version: [output of `python --version`]
- uv version: [output of `uv --version`]
- Jerry branch: [output of `git branch --show-current`]

## Steps Taken
1. Ran `uv --version` → [result]
2. Ran hook manually → [result]
3. Ran `uv sync` → [result]

## Error Output
[Paste the full error message here]
```

---

# L2: Technical Investigation Guide

> **L2 Support** investigates deeper technical issues using logs and configuration.
> Goal: Identify root cause OR provide detailed analysis for L3.

## L2 Prerequisites

Before investigating, ensure you have:

- [ ] L1 diagnostic results
- [ ] Git access to the repository
- [ ] Understanding of Python import system
- [ ] 30-60 minutes available

## L2 Investigation Areas

### Area 1: Import Path Analysis

**Purpose:** Verify Python can find all required modules.

```bash
# Check PYTHONPATH is set correctly
echo $PYTHONPATH

# Verify imports work
PYTHONPATH="." python -c "from src.interface.cli.session_start import main; print('OK')"
```

**Common Issues:**

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'src'` | PYTHONPATH not set | Add `PYTHONPATH="."` prefix |
| `ModuleNotFoundError: No module named 'filelock'` | Missing PEP 723 deps | Check inline metadata in script |

### Area 2: Hook Configuration Analysis

**Purpose:** Verify hooks.json is correctly configured.

```bash
# View the hook configuration
cat hooks/hooks.json | python -m json.tool
```

**Check these fields:**

```json
{
  "hooks": [
    {
      "event": "SessionStart",
      "command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
    }
  ]
}
```

**Common Issues:**

| Problem | Symptom | Solution |
|---------|---------|----------|
| Missing PYTHONPATH | Import errors | Add `PYTHONPATH=` to command |
| Using `python3` instead of `uv run` | Dependency errors | Use `uv run` for PEP 723 support |
| Wrong file path | "No such file" | Check `${CLAUDE_PLUGIN_ROOT}` substitution |

### Area 3: PEP 723 Metadata Check

**Purpose:** Verify inline script dependencies are declared.

```bash
# View the first 30 lines of session_start.py
head -30 src/interface/cli/session_start.py
```

**Expected PEP 723 block:**

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "filelock>=3.12.0",
# ]
# ///
```

**If this block is missing or malformed, dependencies won't be installed by uv.**

### Area 4: CI Test Verification

**Purpose:** Confirm tests pass to rule out code issues.

```bash
# Run the subprocess tests that validate hook execution
PYTHONPATH="." uv run pytest tests/session_management/e2e/test_session_start.py -v --tb=short

# Run contract tests that validate output format
PYTHONPATH="." uv run pytest tests/session_management/contract/test_hook_contract.py -v --tb=short
```

**Interpret Results:**

| Result | Meaning | Next Step |
|--------|---------|-----------|
| All pass | Code is correct, issue is environmental | Check user's environment |
| Some fail | Code regression detected | Escalate to L3 |
| Import errors | Dependencies missing | Run `uv sync --extra test` |

## L2 Root Cause Categories

After investigation, categorize the issue:

| Category | Description | Owner |
|----------|-------------|-------|
| **Environment** | User's machine missing tools (uv, Python) | L1 can resolve |
| **Configuration** | hooks.json or manifest incorrect | L2 can resolve |
| **Dependency** | PEP 723 metadata incomplete | L3 required |
| **Code Bug** | Script logic error | L3 required |

## L2 Escalation Template

When escalating to L3, provide:

```
## Root Cause Category
[Environment / Configuration / Dependency / Code Bug]

## Investigation Summary
- Import path analysis: [PASS/FAIL - details]
- Hook configuration: [PASS/FAIL - details]
- PEP 723 metadata: [PASS/FAIL - details]
- CI tests: [X passed, Y failed]

## Specific Finding
[Exactly what is broken and where]

## Recommended Fix
[If you have a hypothesis]
```

---

# L3: Expert Resolution Guide

> **L3 Engineers** fix code issues and implement preventive measures.
> Goal: Resolve root cause and prevent recurrence.

## L3 Prerequisites

- [ ] L2 investigation report
- [ ] Write access to repository
- [ ] Understanding of Jerry architecture
- [ ] Understanding of PEP 723 and uv

## L3 Resolution Patterns

### Pattern 1: Missing PEP 723 Dependency

**Symptom:** `ModuleNotFoundError` for a PyPI package

**Fix:**

```python
# Add to the script's inline metadata block
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "existing-dep>=1.0.0",
#     "new-dep>=2.0.0",  # ADD THIS LINE
# ]
# ///
```

**Verification:**

```bash
# Clear uv cache and rerun
uv cache clean
PYTHONPATH="." uv run src/interface/cli/session_start.py
```

### Pattern 2: Missing PYTHONPATH

**Symptom:** `ModuleNotFoundError: No module named 'src'`

**Fix:** Update `hooks/hooks.json`:

```json
{
  "command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/path/to/script.py"
}
```

**Why:** PEP 723 only handles PyPI dependencies. Local imports need PYTHONPATH.

### Pattern 3: Wrong Interpreter

**Symptom:** Dependencies not found despite being in PEP 723 block

**Fix:** Change from `python3` to `uv run`:

```json
// Before (broken)
"command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/foo.py"

// After (working)
"command": "uv run ${CLAUDE_PLUGIN_ROOT}/scripts/foo.py"
```

**Why:** Only `uv run` reads PEP 723 inline metadata.

### Pattern 4: Silent Failure

**Symptom:** No output, no error, hook appears to do nothing

**Root Cause:** Exception caught but not re-raised or logged

**Fix:** Add explicit error handling:

```python
def main() -> int:
    try:
        # ... existing code ...
        return 0
    except Exception as e:
        # ALWAYS output errors to stderr for visibility
        print(f"ERROR: {e}", file=sys.stderr)
        # But return 0 so Claude doesn't show "hook failed"
        return 0
```

## L3 Prevention Checklist

Before merging any hook script changes:

- [ ] **PEP 723 block present** - All PyPI deps declared in inline metadata
- [ ] **PYTHONPATH in command** - Local imports will work
- [ ] **Uses `uv run`** - Not `python3` or `python`
- [ ] **Error handling** - Errors printed to stderr
- [ ] **Exit code 0** - Always returns 0 (Claude requirement)
- [ ] **Tests pass** - Run `pytest -m subprocess`
- [ ] **CI passes** - Check cli-integration job

## L3 Post-Incident Tasks

After resolving an incident:

1. [ ] **Add test** - Cover the failure scenario
2. [ ] **Update runbook** - Add new pattern if applicable
3. [ ] **Update CI** - Add check if automated detection is possible
4. [ ] **Document** - Record in project's bug tracker

---

# Case Study: BUG-007

> This section documents an actual incident as a learning example.

## Summary

| Field | Value |
|-------|-------|
| Bug ID | BUG-007 |
| Severity | HIGH |
| Duration | ~2 hours investigation, ~30 min fix |
| Root Cause | Hook script delegated to modules requiring `pip install` |

## What Happened

1. User installed Jerry plugin via Claude Code marketplace
2. Started a new session
3. **Expected:** Jerry startup message appears
4. **Actual:** No message, no error, silent failure

## Why It Happened

The `scripts/session_start.py` was a "legacy wrapper" that tried to run:

```python
# All three paths required pip install -e .
subprocess.run(['.venv/bin/jerry-session-start', ...])  # Entry point needs pip
subprocess.run(['.venv/bin/python', '-m', 'src.interface.cli.session_start'])  # Needs venv
subprocess.run([sys.executable, '-m', 'src.interface.cli.session_start'])  # Needs pip
```

None of these work without `pip install -e .`, which users don't run.

## How It Was Fixed

Changed `hooks/hooks.json`:

```json
// Before
"command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py"

// After
"command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
```

And added PEP 723 metadata to `session_start.py`:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "filelock>=3.12.0",
# ]
# ///
```

## Lessons Learned

| Lesson | Prevention |
|--------|------------|
| Don't assume pip is available | Use uv run + PEP 723 |
| Don't fail silently | Always print errors to stderr |
| Test plugin mode | Run without `pip install -e .` |
| Automate validation | CI job validates hook execution |

## Detection Improvements

After BUG-007, we added:

1. **EN-005:** Pre-commit hook validates manifests
2. **EN-005:** CI job validates session_start.py standalone
3. **EN-006:** 27 subprocess tests for CLI
4. **EN-006:** cli-integration CI job

---

# Checklists

## Pre-Release Checklist

Before releasing any plugin changes:

```
## Plugin Validation Checklist

### Manifests
- [ ] `plugin.json` valid JSON
- [ ] `hooks.json` valid JSON
- [ ] All `command` fields use `uv run`
- [ ] All `command` fields include PYTHONPATH

### Hook Scripts
- [ ] PEP 723 metadata block present
- [ ] All PyPI dependencies listed
- [ ] Error handling outputs to stderr
- [ ] Exit code is always 0

### Testing
- [ ] Local: `PYTHONPATH="." uv run <script>` works
- [ ] Tests: `pytest -m subprocess` passes
- [ ] CI: cli-integration job passes

### Documentation
- [ ] CHANGELOG updated
- [ ] Installation docs current
```

## Incident Response Checklist

When a plugin regression is reported:

```
## Incident Response Checklist

### Triage (5 min)
- [ ] Confirm the issue (can you reproduce?)
- [ ] Check if it's environment or code issue
- [ ] Assign severity (HIGH if affects all users)

### Investigate (15-30 min)
- [ ] Run L1 diagnostic script
- [ ] If needed, run L2 investigation
- [ ] Identify root cause category

### Resolve
- [ ] Apply fix from resolution patterns
- [ ] Test fix locally
- [ ] Push fix and verify CI passes

### Post-Incident
- [ ] Add test for the failure
- [ ] Update runbook if needed
- [ ] Communicate resolution to reporter
```

---

# Troubleshooting Flowchart

```
START: "Jerry startup message not appearing"
    │
    ▼
┌─────────────────────────────────────────┐
│ Is uv installed?                        │
│ Run: uv --version                       │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
       YES               NO
        │                 │
        ▼                 ▼
┌───────────────┐  ┌──────────────────────┐
│ Continue      │  │ Install uv:          │
│               │  │ curl -LsSf           │
│               │  │ https://astral.sh/uv │
│               │  │ /install.sh | sh     │
└───────┬───────┘  └──────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ Can you run the hook manually?          │
│ Run: PYTHONPATH="." uv run              │
│      src/interface/cli/session_start.py │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
    SUCCESS            ERROR
        │                 │
        ▼                 ▼
┌───────────────┐  ┌──────────────────────┐
│ Issue is in   │  │ What kind of error?  │
│ Claude Code   │  │                      │
│ integration,  │  └──────────┬───────────┘
│ not Jerry     │             │
│               │    ┌────────┼────────┐
│ Check:        │    │        │        │
│ - Plugin      │ Import   Command   Other
│   installed   │ Error    Not Found  Error
│ - hooks.json  │    │        │        │
│   correct     │    ▼        ▼        ▼
└───────────────┘  ┌───────┐ ┌──────┐ ┌─────┐
                   │Check  │ │Check │ │L2   │
                   │PEP723 │ │PATH  │ │Help │
                   │deps   │ │vars  │ │     │
                   └───────┘ └──────┘ └─────┘
```

---

# Rollback Procedures

## Quick Rollback

If a release breaks the plugin and you need to rollback immediately:

```bash
# 1. Find the last good commit
git log --oneline hooks/ src/interface/cli/session_start.py | head -10

# 2. Revert to that commit for plugin files only
git checkout <last-good-commit> -- hooks/ src/interface/cli/session_start.py

# 3. Commit the rollback
git commit -m "rollback: revert plugin files to <last-good-commit>

Emergency rollback due to [describe issue]"

# 4. Push immediately
git push origin HEAD
```

## Full Release Rollback

If you need to rollback an entire release:

```bash
# 1. Identify the breaking commit
git log --oneline | head -20

# 2. Create a revert commit
git revert <breaking-commit>

# 3. Push the revert
git push origin HEAD
```

## Rollback Verification

After rollback:

```bash
# Verify the hook works
PYTHONPATH="." uv run src/interface/cli/session_start.py

# Verify tests pass
PYTHONPATH="." uv run pytest -m subprocess -v
```

---

# Appendix

## Related Documents

| Document | Location | Purpose |
|----------|----------|---------|
| BUG-007 Analysis | `projects/PROJ-005-plugin-bugs/work/SE-001/FT-002/bug-007.md` | Detailed incident analysis |
| ADR e-010 | `projects/PROJ-005-plugin-bugs/decisions/PROJ-005-e-010-adr-uv-session-start.md` | Architecture decision |
| EN-005 | `projects/PROJ-005-plugin-bugs/work/SE-002/FT-003/en-005.md` | CI validation implementation |
| EN-006 | `projects/PROJ-005-plugin-bugs/work/SE-002/FT-003/en-006.md` | CLI test suite implementation |

## Glossary

| Term | Definition |
|------|------------|
| **PEP 723** | Python standard for inline script metadata (dependencies in comments) |
| **uv** | Fast Python package manager by Astral, reads PEP 723 |
| **PYTHONPATH** | Environment variable telling Python where to find modules |
| **Hook** | Script that runs at specific Claude Code events (e.g., SessionStart) |
| **Plugin** | Extension package for Claude Code installed via marketplace |
| **Subprocess** | Running a command in a separate process |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-13 | Initial release based on BUG-007 lessons |

---

**End of Runbook**

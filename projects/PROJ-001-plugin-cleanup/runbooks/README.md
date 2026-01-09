# Runbooks - PROJ-001-plugin-cleanup

> Execution guides for multi-session and parallel work.

---

## Available Runbooks

| ID | Task | Status | Validated |
|----|------|--------|-----------|
| [RUNBOOK-001](RUNBOOK-001-008d-domain-refactoring.md) | ENFORCE-008d Domain Refactoring | READY | ✅ [VALIDATION-001](VALIDATION-001-runbook-test.md) |

---

## What is a Runbook?

A **Runbook** is a step-by-step execution guide that enables:

1. **Multi-session work**: Resume after context compaction
2. **Parallel execution**: Multiple agents working simultaneously
3. **Consistent execution**: Same steps, same results
4. **Handoff protocol**: Clear checkpoint and resume procedures

---

## Runbook Template

Every runbook should contain:

| Section | Purpose |
|---------|---------|
| Pre-Flight Checklist | Verification before starting |
| Stage Execution Order | Dependency-ordered stages |
| Per-Stage Details | Inputs, outputs, tasks, commits |
| Resume Protocol | How to continue after interruption |
| Parallel Safety Analysis | Which stages can run concurrently |
| Troubleshooting | Common issues and fixes |
| Validation Checklist | Completion criteria |

---

## Usage

### Starting Work

```bash
# 1. Read WORKTRACKER to identify current task
cat projects/PROJ-001-plugin-cleanup/WORKTRACKER.md

# 2. Find linked runbook in "Next Actions" section

# 3. Follow runbook pre-flight checklist

# 4. Execute stages in order
```

### Resuming After Context Compaction

```bash
# 1. Read WORKTRACKER → Current Focus

# 2. Read linked runbook → Resume Protocol

# 3. Check git log for last commit

# 4. Run tests to verify current state

# 5. Continue from documented checkpoint
```

### Parallel Execution

```bash
# 1. Read runbook Parallel Safety Analysis

# 2. Identify safe parallel stages

# 3. Create feature branches per stage

# 4. Execute in parallel sessions

# 5. Merge following documented strategy
```

---

## Validation Evidence

| ID | Runbook | Method | Result |
|----|---------|--------|--------|
| [VALIDATION-001](VALIDATION-001-runbook-test.md) | RUNBOOK-001 | Fresh Context Simulation | ✅ PASS |

---

## Creating New Runbooks

1. Copy template structure from existing runbook
2. Adapt for specific task
3. Create validation test
4. Add to this README index
5. Link from WORKTRACKER

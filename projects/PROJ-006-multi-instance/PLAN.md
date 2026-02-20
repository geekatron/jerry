# PROJ-006: Automated Multi-Instance Orchestration — Implementation Plan

> Investigate and implement automated multi-instance Claude management, replacing the current manual worktree + session workflow with programmatic instance spawning via the Python Claude SDK or CLI.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Project scope and goals |
| [Problem Statement](#problem-statement) | What we're solving |
| [Hypothesis](#hypothesis) | Core thesis to validate |
| [Epics](#epics) | Work breakdown |
| [Milestones](#milestones) | Key delivery points |
| [Success Criteria](#success-criteria) | Definition of done |

---

## Overview

PROJ-006 investigates whether Jerry can automatically spin up and manage multiple Claude instances — replacing the current manual process of creating git worktrees, opening terminals, and launching `claude` sessions by hand. Two primary approaches: (1) the Python Claude SDK (Anthropic Agent SDK) for programmatic instance management, and (2) spawning and managing multiple Claude Code CLI processes. The goal is autonomous multi-project orchestration from a single control plane.

## Problem Statement

**Current pain:**
1. Multi-project work requires manual worktree creation (`git worktree add`)
2. Each worktree needs a manually opened terminal and `claude` session
3. No programmatic control — operator must context-switch between sessions
4. Cross-project coordination (merging main, syncing state) is manual and error-prone
5. No way to automatically spin up a research pipeline across multiple projects in parallel
6. Session lifecycle (start, monitor, checkpoint, resume) is entirely manual

**Desired state:**
1. Programmatic creation and management of Claude instances (SDK or CLI)
2. Automatic worktree provisioning and session lifecycle management
3. Single control plane that can dispatch work to multiple parallel instances
4. Cross-instance coordination (state sharing, merge orchestration, progress reporting)
5. Integration with existing /orchestration skill for workflow-aware instance management

## Hypothesis

We hypothesize that:
1. The Python Claude SDK (Agent SDK) provides sufficient API surface for programmatic instance management with tool use, context control, and session persistence
2. Alternatively, spawning multiple Claude Code CLI instances via subprocess can achieve similar results with lower integration cost
3. Automated worktree lifecycle (create, provision, merge, cleanup) is tractable as a Jerry CLI extension
4. The efficiency gains from parallel multi-instance work justify the integration complexity
5. A hybrid approach (SDK for complex orchestration, CLI for simple parallel tasks) may be optimal

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| EPIC-001 | Automated Multi-Instance Orchestration | pending | high |

### EPIC-001 Features

| ID | Title | Status |
|----|-------|--------|
| FEAT-001 | Multi-Instance Strategy Assessment | pending |

### EPIC-001 Spikes

| ID | Title | Status | Parent |
|----|-------|--------|--------|
| SPIKE-001 | Claude SDK vs CLI Instance Comparison | pending | FEAT-001 |
| SPIKE-002 | Automated Worktree & Session Lifecycle Management | pending | FEAT-001 |

## Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| SPIKE-001 complete — SDK vs CLI trade-off analysis with evidence | TBD | pending |
| SPIKE-002 complete — worktree lifecycle automation feasibility | TBD | pending |
| Go/no-go decision on approach (ADR) | TBD | pending |
| MVP: programmatic instance spawning for single project | TBD | pending |
| Multi-project parallel orchestration working | TBD | pending |

## Success Criteria

- [ ] Claude SDK and CLI instance approaches both prototyped and compared with evidence
- [ ] Automated worktree creation, session start, and teardown demonstrated
- [ ] Single command can dispatch work to N parallel Claude instances
- [ ] Cross-instance state coordination works with ORCHESTRATION.yaml and WORKTRACKER.md
- [ ] Integration path with /orchestration skill defined
- [ ] Go/no-go decision backed by adversarial review

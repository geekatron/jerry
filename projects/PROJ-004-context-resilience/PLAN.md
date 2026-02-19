# PROJ-004: Context Resilience — Implementation Plan

> Detect context exhaustion during multi-orchestration runs and enable graceful session handoff with automated resumption from ORCHESTRATION.yaml and WORKTRACKER.md.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Project scope and goals |
| [Problem Statement](#problem-statement) | What we're solving |
| [Epics](#epics) | Work breakdown |
| [Milestones](#milestones) | Key delivery points |
| [Success Criteria](#success-criteria) | Definition of done |

---

## Overview

PROJ-004 tackles context exhaustion — the operational reality that multi-orchestration workflows fill the ~200K token context window, causing performance degradation (context rot) or forced session termination. Today, resumption requires manual intervention: clearing context, reading ORCHESTRATION.yaml and WORKTRACKER.md, and mentally reconstructing where to resume. This project automates detection and provides structured resumption protocols.

## Problem Statement

**Current pain:**
1. Multi-phase orchestration runs (C3/C4) routinely exhaust session context
2. No automated detection — degradation is noticed only when quality drops or the system compresses
3. Session clearance loses all ephemeral state; resumption depends on operator knowledge
4. ORCHESTRATION.yaml and WORKTRACKER.md contain sufficient state for resumption, but there is no standardized protocol for Claude to read them and re-orient

**Desired state:**
1. Proactive detection of context fill level with configurable thresholds
2. Graceful checkpoint-and-handoff before forced termination
3. Structured resumption prompt that reads ORCHESTRATION.yaml + WORKTRACKER.md and reconstructs execution context
4. Minimal operator intervention — Claude should self-orient from persistent state

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| EPIC-001 | Context Resilience | pending | high |

### EPIC-001 Features

| ID | Title | Status |
|----|-------|--------|
| FEAT-001 | Context Exhaustion Detection & Graceful Session Handoff | pending |

### EPIC-001 Spikes

| ID | Title | Status |
|----|-------|--------|
| SPIKE-001 | Research Context Measurement, Detection Thresholds & Resumption Protocols | pending |

## Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| SPIKE-001 research complete — thresholds and protocols defined | TBD | pending |
| Detection mechanism implemented and tested | TBD | pending |
| Resumption protocol integrated with /orchestration skill | TBD | pending |
| End-to-end validation on real C3+ orchestration run | TBD | pending |

## Success Criteria

- [ ] Context fill level is measurable and reported during orchestration runs
- [ ] Configurable threshold triggers graceful checkpoint before forced termination
- [ ] Resumption prompt reliably reconstructs execution context from ORCHESTRATION.yaml + WORKTRACKER.md
- [ ] Operator can clear session and resume with single command or minimal steps
- [ ] No regression in orchestration quality (>= 0.92 quality gate maintained)

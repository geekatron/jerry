---
workflow_id: consensus-panel-20260316-001
phase_id: phase-1-draft
panel_topic: Best approach to implement the Consensus Panel runner
authored_by: orchestrator (Jerry Framework)
date: 2026-03-16
---

# Consensus Panel Intent: Implement the Consensus Panel Runner

## Context

The Jerry Framework (a CLI-based orchestration framework for Claude Code) has a documented
**Consensus Panel pattern** (Pattern 6 in PATTERNS.md / MULTI_CLI_INTEGRATION.md v1.2.0).
The pattern runs multiple AI models (Claude, Codex, Gemini) as parallel OS subprocesses,
has each write output to a dedicated file, then synthesizes results.

The specification exists as reference documentation. What does NOT yet exist is a concrete,
runnable implementation of the orchestration script that executes this pattern.

## The Problem to Solve

Design and specify the best approach to implement a **reusable, runnable Consensus Panel
runner** inside the Jerry Framework. This runner should:

1. Execute the pre-flight resolution chain (platform detect → CLI detect → auth validate →
   API fallback → panel composition gate)
2. Launch available workers in parallel (bash `&` background jobs) with per-PID timeout handling
3. Run the draft phase (each model writes an independent draft)
4. Run the cross-critique phase (each model critiques the other models' drafts)
5. Invoke synthesis (hand off to orch-synthesizer)
6. Persist all state to ORCHESTRATION.yaml extensions

## Constraints

- **Platform:** Windows 11 + Git Bash (MSYS2 / MINGW64). Bash `&` background jobs are supported.
- **Nested session guard:** The runner may be invoked from inside Claude Code (`CLAUDECODE=1`),
  in which case `claude` CLI must be downgraded to API or skipped (T-002 finding).
- **Python runtime:** `uv run` only — no bare `python` or `pip`.
- **Framework conventions:** Jerry Framework uses file-mediated integration; all state persists
  to filesystem. No in-memory-only state.
- **P-003 compliance:** External CLI/API processes are OS subprocesses, not Jerry sub-agents.
  The synthesis step uses `orch-synthesizer` via the Task tool (one level of agent nesting only).

## Your Task

Write an **independent draft** addressing:

### Section 1: Implementation Approach
What is the best form for this runner?
- Options include: bash script, Python CLI (uv-managed), Jerry skill with embedded bash blocks,
  or a hybrid. Justify your choice.

### Section 2: Architecture
Describe the key components, their responsibilities, and how they connect.
Include: pre-flight module, worker launcher, wait/timeout handler, output verifier,
synthesis handoff.

### Section 3: Key Implementation Details
Provide concrete, runnable code or pseudocode for the two hardest parts:
- The parallel launch + per-PID wait with timeout
- The output verification and gap handling

### Section 4: Risks and Edge Cases
What are the top 3 risks in implementing this? How would you mitigate each?

### Section 5: Open Questions
What decisions are still unresolved that a human should decide before implementation starts?

## Output Format

Write your draft as a structured Markdown document. Be concrete and specific —
generic advice is less useful than specific implementation guidance.

# GH #377 — Grant Bash to adv-executor and adv-scorer: Orchestration Plan

> **Document ID:** PROJ-024-ORCH-PLAN-ADVERSARY-BASH-377
> **Workflow ID:** adversary-bash-377
> **GitHub Issue:** [#377](https://github.com/geekatron/jerry/issues/377) (split from parent #344, section 3.1 / 3.2 item 1)
> **Date:** 2026-08-13
> **Status:** PLANNED — not yet implemented, no worktracker entities created
> **Branch:** `feat/proj-024-adversary-bash-377` (cut from `main`)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Plain-language summary of what and why |
| [L1: Technical Plan](#l1-technical-plan) | Node roster, ASCII workflow diagram, phase/agent table, sync gates |
| [Worktracker Decomposition](#worktracker-decomposition) | Where this fits in PROJ-024, Enabler + Task breakdown |
| [Agents Considered and Excluded](#agents-considered-and-excluded) | Why eng-backend/eng-frontend/eng-infra/eng-devsecops/eng-lead/eng-reviewer are NOT in the graph |
| [L2: Implementation Details](#l2-implementation-details) | Criticality, quality gates, failure taxonomy, retry/escalation policy |
| [Verification of graph.dot](#verification-of-graphdot) | Confirmation the DOT file renders |
| [Disclaimer](#disclaimer) | Human review notice |

---

## L0: Workflow Overview

Two of Jerry's built-in "critic" agents — `adv-executor` (which runs adversarial review strategies against a document) and `adv-scorer` (which grades a document's quality) — currently cannot run shell commands. That sounds safe, but it backfires: without a shell, `adv-executor` cannot check *which exact version* of a file it is reviewing (`git show`), so it can confidently report on the wrong revision without any error. And `adv-scorer` cannot count things itself (`grep -c`, `wc -l`) to check whether a claim in a document ("we found 12 instances of X") is actually true — it can only check whether the document is internally consistent, not whether it's *correct*. GitHub Issue #377 fixes this by giving both agents the `Bash` tool, while keeping their existing ability to write files. The owner has already decided against the alternative (making them fully read-only) because that would force every finding to be written to a file and re-read by the orchestrator instead of the critic just checking its own work directly — burning far more context for no safety benefit, since both agents can already write and edit files.

This plan does not write any code. It defines: (1) where this fits in the existing PROJ-024 worktracker structure, (2) a small, failure-aware sequence of steps — implementation, rebuild, validation, and two concrete "did it actually work" tests — with an explicit security sanity-check up front because granting a new capability to agents is a security-relevant change, and (3) a dependency graph (`graph.dot`) showing exactly where the plan halts if any step fails, instead of assuming everything works on the first try.

---

## L1: Technical Plan

### Node Roster — Jerry Agent per Step

Every node below names the actual jerry agent (or explicitly "MAIN CONTEXT — no agent" for direct CLI/edit work that does not warrant a specialized agent per AP-05 Over-Routing prevention, `.context/rules/agent-routing-standards.md`). "Real role" is written so a non-Jerry reader does not need a glossary.

| # | Step | Jerry Agent | What it actually does (plain language) | Tools it uses here | Why this agent (not another) |
|---|------|-------------|------------------------------------------|--------------------|-------------------------------|
| N1 | Create the worktracker Enabler + Tasks | **MAIN CONTEXT (no agent)** | Writes the tracking paperwork (one Enabler, four Tasks) into the project's work-item files using the canonical templates. | Write, Edit | Per this skill's own rule (WTI-009 / worktracker SKILL.md), *creating* entities is a main-context activity — the worktracker agents (`wt-verifier`, `wt-visualizer`, `wt-auditor`) only check, diagram, or audit entities that already exist. Using an agent to create files an equally-capable main context can create directly would be AP-05 (Over-Routing). |
| N2 | Pre-implementation security sanity-check | **eng-security** (from `/eng-team`) | Reads the two agents' current governance files and asks: "does giving a shell to an agent that already reads untrusted external content (adv-executor already has an *accepted* prompt-injection risk via WebFetch — see its governance.yaml line 8) make that risk worse?" Produces a short note: which shell verbs the prompt text should explicitly scope to (git/grep/wc — read-only, non-destructive), and confirms the issue's own "blast radius" argument (Write/Edit already granted, so Bash widens *measurement*, not *mutation*) holds up. | Read, Grep | eng-security's stated job is exactly this: "Review authentication and authorization logic... identify business logic vulnerabilities automated tools cannot detect" and manual verification against security requirements. A capability grant to an AI agent is a capability/authorization change — squarely eng-security's domain, not eng-backend's (no server code), not eng-devsecops's (no CI/scanning pipeline touched), not eng-infra's (no containers/IaC). |
| N3 | Audit the new entity files for structural correctness | **wt-auditor** | Checks that the Enabler and Task files created in N1 actually follow the canonical templates (right sections present, correct parent links, no orphans) — the thing N1 (main context) is *not* independently checked for. | Read, Glob, Grep, Bash (for `jerry ast` frontmatter checks per H-33) | wt-auditor's job description is literally "audit cross-file integrity and template compliance" — the counter-check to N1's creation work. Running it as a separate node (not folded into N1) gives an independent check rather than trusting the creator to grade its own homework. |
| N4 | RED — confirm the acceptance tests currently fail | **MAIN CONTEXT (no agent)** | Before touching anything, run the three GH #377 acceptance probes against the *current* agents and confirm they fail exactly as the issue describes: `adv-executor` has no `Bash` in its generated frontmatter today, and asking it to run `git show` will not work. This is the TDD "Red" step — proving the test is meaningful before making it pass. | Read, Bash | Not an agent task — it's establishing a baseline fact about the repository as it exists right now. |
| N5 | GREEN — edit the four canonical source files | **MAIN CONTEXT (no agent)** | Edits `skills/adversary/composition/adv-executor.agent.yaml` and `adv-scorer.agent.yaml` — adds `shell_execute` to `tools.native` (the abstract name that `src/agents/infrastructure/mappings.yaml` maps to `Bash` for Claude Code) — **and** edits `adv-executor.prompt.md` / `adv-scorer.prompt.md` to update the `<p003_self_check>` restatement ("This agent may ONLY use: file_read, file_write, file_edit, file_search_glob, file_search_content") to include `shell_execute`. Both halves are mandatory — see [Failure Mode F-09](#l2-implementation-details) for what happens if only the YAML is edited. | Edit | This is source authorship, not agent-worthy analysis or judgment — a single, mechanical, four-file edit driven entirely by the issue text. Routing it to an agent would be AP-05 (Over-Routing: task completable in under 5 tool calls). |
| N6 | Build | **MAIN CONTEXT (CLI)** — `uv run jerry agents build` | Regenerates the four *derived* files: `skills/adversary/agents/adv-executor.md`, `adv-executor.governance.yaml`, `adv-scorer.md`, `adv-scorer.governance.yaml` from the canonical source edited in N5. This is what the issue means by "not a hand-edit of the generated files" — the generated `.md`/`.governance.yaml` are never touched directly. | Bash | Deterministic codegen; the jerry CLI already exists for exactly this. No judgment involved — an agent would add nothing. |
| N7 | Validate | **MAIN CONTEXT (CLI)** — `uv run jerry agents validate` | Checks the four regenerated files against `docs/schemas/agent-governance-v1.schema.json` and confirms `tool_tier` is unchanged: `adv-executor` stays **T4**, `adv-scorer` stays **T2**. This matters because `Bash` is *already inside the T2 ceiling* per the Tool Security Tiers table (T2 = T1 + Write, Edit, Bash) — this change fills out an allowance the tier already permits, it does not upgrade anyone's tier. If validation reported a tier bump, that would itself be a bug in the build step. | Bash | Deterministic schema check. |
| N8 | Diff | **MAIN CONTEXT (CLI)** — `uv run jerry agents diff` | Confirms the *only* thing that changed in the four generated files is the `Bash` addition (frontmatter `tools:` line, `<p003_self_check>` body text, `capabilities.allowed_tools` in governance.yaml) — and nothing else drifted (no unrelated reordering, no accidental field loss). | Bash | Deterministic drift check; this is the exact tool the acceptance criteria implicitly requires ("restated tool lists updated in both `.md` bodies and both `governance.yaml` files") to be provably true rather than eyeballed. |
| N9 | Acceptance probe — pin a revision | **adv-executor** (post-rebuild) | Given a real commit SHA and file path, runs `git show "<sha>:<path>" \| grep -c '^+'` and confirms the result is `0` — proving it read a *file at that revision*, not a diff/commit, which is the exact GH #377 acceptance test. | file_read, **shell_execute (Bash — new)**, file_write | This is the capability under test — it must be exercised by the real agent, not simulated, or the acceptance criterion is unverified. |
| N10 | Acceptance probe — publish a self-derived count | **adv-scorer** (post-rebuild) | Given a claim in a sample deliverable ("N instances of X"), runs `grep -c` or `wc -l` itself and publishes the count it derived, rather than asking the orchestrator for it or trusting the document's own claim — the exact gap the issue describes for the Evidence Quality / Methodological Rigor S-014 dimensions. | file_read, **shell_execute (Bash — new)**, file_write | Same reasoning as N9 — this is `adv-scorer`'s specific capability gap, must be tested on the real agent. |
| N11 | C3 adversarial quality gate on the change itself | **`/adversary`: adv-selector → adv-executor (×N strategies) → adv-scorer** | Reviews the *diff* (composition YAML + prompt.md + the four generated files + this plan's rationale) — not the agents' runtime behavior (that's N9/N10) — against the SSOT quality rubric. `adv-selector` first confirms the criticality (this plan treats the change as **C3**, see [L2](#l2-implementation-details)), then runs the required C3 strategy set, then `adv-scorer` produces the composite score. | Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Context7 | H-22 mandates `/adversary` for standalone adversarial review outside a creator-critic loop, and this change is auto-escalated to C3 (AE-005: security-relevant — see [L2](#l2-implementation-details)), which requires more than self-review. **Note on self-reference:** this node necessarily uses the *newly rebuilt* `adv-executor`/`adv-scorer` to review a change to themselves. That is intentional dogfooding of the exact capability just added (Bash lets the reviewer pin the revision it is reviewing) — but if this node produces confused or circular-seeming output, the fallback is `ps-critic` (`/problem-solving`), which is a fully independent critic not implicated in the change under review. |
| N12 | Final acceptance-criteria verification | **wt-verifier** | Checks the Enabler and its four Tasks against their acceptance criteria with evidence: N6-N8 clean, N9/N10 probe transcripts attached, N11 score ≥ 0.92. Produces a PASS/FAIL verdict per WTI-002 ("No Closure Without Verification") — it does **not** close the entities itself. | Read, Glob, Grep, Write, Bash | wt-verifier's stated job is exactly this: "validate that work items meet acceptance criteria... before status transitions to DONE." This is the closure gate, distinct from wt-auditor's structural check in N3. |
| N13 | PR review + merge | **Human + GitHub (no agent)** | Standard PR review; `Closes #377` in the PR description. Per prior session guidance, the worktracker Task/Enabler statuses are **not** flipped to done until this merges to `main` — a branch-only fix is not "done." | — | Governance boundary, not an agent task. |

### ASCII Workflow Diagram

```
                    ┌───────────────────────────┐   ┌────────────────────────────────┐
                    │ N1: Create EN + 4 Tasks    │   │ N2: Pre-impl security check    │
                    │ MAIN CONTEXT (no agent)    │   │ eng-security                   │
                    └──────────────┬─────────────┘   └───────────────┬─────────────────┘
                                   │                                  │
                                   │           ╔══════════════════════╧═══╗
                                   │           ║ GATE 0: fan-in            ║
                                   │           ║ entities exist            ║
                                   │           ║ + risk note reviewed      ║
                                   │           ╚══════════════╤════════════╝
                                   │                          │  ┄┄┄▶ ESCALATE (H-31): unresolved
                                   ▼                          │       new risk found → ask owner
                    ┌───────────────────────────┐             │       [terminal — no auto-retry]
                    │ N3: Audit new entity files │             │
                    │ wt-auditor                 │             ▼
                    └──────────────┬─────────────┘   ┌────────────────────────────┐
                                   │                  │ N4: RED — confirm probes   │
                                   │                  │ currently fail             │
                                   │                  │ MAIN CONTEXT (no agent)    │
                                   │                  └──────────────┬─────────────┘
                                   │                                 ▼
                                   │                  ┌────────────────────────────┐
                                   │                  │ N5: GREEN — edit 4 source  │◀┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┐
                                   │                  │ files (.agent.yaml x2,     │                       ┊ retry
                                   │                  │ .prompt.md x2)             │                       ┊ (fix source,
                                   │                  │ MAIN CONTEXT (no agent)    │                       ┊ max 3 loops
                                   │                  └──────────────┬─────────────┘                       ┊ → escalate)
                                   │                                 ▼                                     ┊
                                   │                  ┌────────────────────────────┐   ┄┄┄▶ [F6] build error┊
                                   │                  │ N6: jerry agents build     │   (schema/YAML) ───────┘
                                   │                  │ MAIN CONTEXT (CLI)         │
                                   │                  └──────────────┬─────────────┘
                                   │                                 ▼
                                   │                  ┌────────────────────────────┐   ┄┄┄▶ [F7] tier changed
                                   │                  │ N7: jerry agents validate  │   unexpectedly, OR      ┊
                                   │                  │ MAIN CONTEXT (CLI)         │   schema invalid ───────┘ (loop to N5)
                                   │                  └──────────────┬─────────────┘
                                   │                                 ▼
                                   │                  ┌────────────────────────────┐   ┄┄┄▶ [F8] drift beyond
                                   │                  │ N8: jerry agents diff      │   the Bash addition ────┘ (loop to N5)
                                   │                  │ MAIN CONTEXT (CLI)         │
                                   │                  └──────────────┬─────────────┘
                                   │                       ┌─────────┴──────────┐
                                   │                       ▼                    ▼
                                   │         ┌───────────────────────┐ ┌──────────────────────┐
                                   │         │ N9: probe — git show  │ │ N10: probe — publish  │
                                   │         │ adv-executor          │ │ self-derived count    │
                                   │         │                       │ │ adv-scorer            │
                                   │         └───────────┬───────────┘ └───────────┬───────────┘
                                   │                      │  ┄┄┄▶ [F9] probe fails  │
                                   │                      │  (likely: prompt.md      │  (loop to N5;
                                   │                      │  self-check text not     │   see F-09 below)
                                   │                      │  updated) ───────────────┘
                                   │                      ▼
                                   │           ╔═══════════════════════╗
                                   └──────────▶║ GATE 1: fan-in         ║
                                               ║ N3 + N9 + N10 all pass ║
                                               ╚═══════════╤════════════╝
                                                            ▼
                                        ┌──────────────────────────────────┐
                                        │ N11: C3 adversarial quality gate  │◀┄┄┄┄┄┄┄┄┄┄┄┄┄┐
                                        │ adv-selector → adv-executor(×N)   │              ┊ [F11] REVISE/
                                        │ → adv-scorer  (≥0.92, H-13)       │              ┊ ESCALATE
                                        └──────────────────┬───────────────┘              ┊ (loop to N5,
                                                            ▼                              ┊  H-14 revision,
                                        ┌──────────────────────────────────┐               ┊  max 3 iterations
                                        │ N12: final AC verification        │               ┊  then escalate)
                                        │ wt-verifier                       │───────────────┘
                                        └──────────────────┬───────────────┘
                                                            ▼
                                        ┌──────────────────────────────────┐
                                        │ N13: PR review + merge            │
                                        │ Human + GitHub (Closes #377)      │
                                        └────────────────────────────────────┘

Legend: ──▶ normal flow   ╔═╗ fan-in/fan-out gate   ┄┄▶ on-failure-halt / retry edge (dashed, red in graph.dot)
```

### Parallelization Rationale

| Parallel pair | Why they are genuinely independent |
|---|---|
| N1 (create worktracker entities) ∥ N2 (eng-security risk note) | N1 is bookkeeping about *tracking* the work; N2 is analysis of the *content* of the change. Neither reads the other's output — N2 reads the current agent governance files (already in the repo), N1 reads only the canonical worktracker templates. |
| N9 (adv-executor probe) ∥ N10 (adv-scorer probe) | Two different agents, two independent capabilities, two independent smoke tests against the same rebuilt artifact set (N8). A failure in one has no bearing on the other. |

### Sync Barriers (Gates)

| Gate | Waits for | Pass condition | Fail path |
|---|---|---|---|
| GATE 0 | N1, N2 | Entities exist AND eng-security note contains no unresolved *new* risk (owner already declined the read-only alternative in the issue text, so this gate is a sanity check, not a re-litigation) | Escalate to user (H-31) — terminal, no auto-retry, because it means eng-security found something the issue's own risk analysis missed |
| GATE 1 | N3, N9, N10 | Audit clean AND both acceptance probes pass | Loop to N5 (see failure taxonomy below) |

---

## Worktracker Decomposition

### Placement

**Parent:** `EPIC-001-schema-validation` → `FEAT-001-claude-code-schema-validation` (existing, `in_progress`).

This is the correct home, not a new Epic/Feature: FEAT-001 already contains the *directly analogous* prior work —

- `STORY-011-adversary-tool-access` — "Adversary Sub-Agents: WebSearch/WebFetch/Context7 (GH #217)" — granted `adv-executor` its current web tools via this exact same canonical-YAML → build → validate pipeline.
- `STORY-013-fix-tier-tool-mismatches` — corrected tier/tool mismatches across agent definitions, including in `adv-*` agents.

GH #377 is the same *kind* of change (grant a tool to an adversary sub-agent, through the canonical build pipeline) at a smaller scale (2 agents, 1 tool, split intentionally off a larger issue #344 for exactly this reason — see the issue body: "Splitting the smallest, most mechanical piece of #344 out so it can be actioned on its own"). No new Epic or Feature is warranted.

### New Enabler

| Field | Value |
|---|---|
| ID (next available) | `EN-011` |
| Title | Grant Bash to Adversary Critic Agents (adv-executor, adv-scorer) |
| Type | Enabler |
| Parent | `FEAT-001-claude-code-schema-validation` |
| Directory | `work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/EN-011-adversary-bash-access/` (naming convention matches `EN-001-security-review`, `EN-005-gitattributes` siblings) |
| Cross-link | GitHub [#377](https://github.com/geekatron/jerry/issues/377); note parent context #344 (not in scope) |
| Template | `.context/templates/worktracker/ENABLER.md` (WTI-007 — canonical template, not freehand) |

### Child Tasks

Four tasks, one-to-one with the four GH #377 acceptance checkboxes (proportionate to a "two-line frontmatter fix," per the issue's own framing — this is deliberately **not** decomposed further):

| ID | Title | Maps to GH #377 AC | Concrete acceptance criteria |
|---|---|---|---|
| `TASK-037` | Edit canonical source: add `shell_execute` to both `.agent.yaml` files + update both `.prompt.md` self-check restatements | AC 1+2 (source half) | `git diff` on the 4 source files shows exactly: `shell_execute` added to `tools.native` in `adv-executor.agent.yaml` and `adv-scorer.agent.yaml`; the `<p003_self_check>` "may ONLY use" sentence in both `.prompt.md` files includes `shell_execute` alongside the existing 5 tools. No other lines change. |
| `TASK-038` | Rebuild + validate + diff generated artifacts | AC 1+2 (generated half) | `uv run jerry agents build` exits 0; `skills/adversary/agents/adv-executor.md` frontmatter `tools:` line and `adv-scorer.md` frontmatter `tools:` line both include `Bash`; both `.governance.yaml` `capabilities.allowed_tools` lists include `Bash`; `uv run jerry agents validate` exits 0 with `tool_tier: T4` (executor) / `tool_tier: T2` (scorer) unchanged; `uv run jerry agents diff` shows no drift beyond the `Bash`/tool-list change. |
| `TASK-039` | Executor acceptance probe | AC 3 | Given a real `<sha>:<path>`, `adv-executor` runs `git show "<sha>:<path>" \| grep -c '^+'` via its new `shell_execute`/Bash access and the result is `0`, confirming it read a file (not a diff). Transcript captured as evidence. |
| `TASK-040` | Scorer acceptance probe | AC 4 | `adv-scorer`, scoring a sample deliverable containing a countable claim, runs `grep -c` or `wc -l` itself via Bash and publishes the self-derived count in its score report rather than trusting the document's stated count or asking the orchestrator. Transcript captured as evidence. |

All four Tasks cross-link to GitHub #377 in their `Related Items` section per H-31 (GitHub Issue Parity, `.context/rules/project-workflow.md`).

**Explicitly not created:** these worktracker entities are **not** created by this plan. Per the task scope, this document is the plan only — entity file creation (N1 in the graph) happens in a follow-on execution step.

---

## Agents Considered and Excluded

The task instructions named eng-lead, eng-backend, eng-security, eng-reviewer, and eng-devsecops as candidates to evaluate. Only eng-security made the cut. Excluding the rest explicitly (rather than silently omitting them) keeps this proportionate to a genuinely small, mechanical change while showing the exclusion was a deliberate read of each agent's actual scope, not an oversight:

| Agent | Why excluded |
|---|---|
| `eng-lead` | Its job is implementation planning, coding-standards enforcement, and dependency governance for *new application code*. This change touches zero application code — it is a declarative tool-list edit in existing agent definition YAML, already fully specified by the GH issue. There is no standards or dependency decision for eng-lead to make. |
| `eng-backend` | No server-side code, no API, no database touched. |
| `eng-frontend` | No client-side code touched (not even listed as a candidate by the task, confirming). |
| `eng-infra` | No IaC, containers, or infrastructure touched. |
| `eng-devsecops` | No CI/CD pipeline, SAST/DAST, secrets scanning, or container scanning configuration touched — those already run unchanged against this diff via the existing repo pipeline; this plan doesn't need to configure new automation. |
| `eng-reviewer` | Its role (final `/eng-team` 8-step gate, `/adversary` at ≥0.95) is the *mandatory* gate for a full `/eng-team` engineering workflow (architecture → implementation → review). This change never enters that workflow — it has no architecture design or threat model step (N2/eng-security already covers the one real security question). Using `/adversary` directly at N11 (per H-22's explicit mandate for standalone adversarial review) is the correct, lighter-weight quality gate instead of invoking the full 8-step `/eng-team` pipeline for a 4-file change. |

---

## L2: Implementation Details

### Criticality Assessment

| Factor | Assessment |
|---|---|
| Reversibility | Single `git revert`, well under 1 day |
| File scope | 8 files total (4 canonical source + 4 generated) — well under the C3 file-count threshold of 10 |
| Impact | Tool/capability grant to 2 agents used across many workflows (`/adversary`, embedded in `ps-critic`-adjacent quality gates, `/eng-team` step 7 recommendation) |
| **Auto-escalation** | **AE-005** (`.context/rules/quality-enforcement.md`): "Security-relevant code = Auto-C3 minimum." Granting shell execution to agents that already carry an *accepted* prompt-injection risk (documented in `adv-executor.governance.yaml`: "Risk accepted: prompt injection via deliverable → WebFetch exfil channel") is a capability/authorization change — squarely security-relevant, even though file count alone would suggest C1/C2. |

**Determination: C3 (Significant).** File-count and reversibility alone would suggest C1, but AE-005 forces a C3 floor regardless of scope, per SSOT precedence.

### Quality Gate (Node N11)

| Element | Value | Source |
|---|---|---|
| Threshold | ≥ 0.92 weighted composite | H-13 |
| Required strategies (C3 = C2 + 3 more) | S-007 (Constitutional AI), S-002 (Devil's Advocate), S-014 (LLM-as-Judge), S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion) | quality-enforcement.md Criticality Levels |
| Ordering constraint | S-003 (Steelman) before S-002 (Devil's Advocate) if S-003 is included — H-16 | adv-selector enforces at runtime |
| Optional strategies | S-001, S-003, S-010, S-011 | quality-enforcement.md |
| Minimum iterations if REVISE | 3 (creator → critic → revision) | H-14 |
| Iteration ceiling before mandatory escalation | 7 (C3, RT-M-010) — in practice this change is small enough that 3 is the realistic bound | agent-routing-standards.md |

### Failure Taxonomy

Every failure edge in `graph.dot` is dashed red. This table gives the concrete, evidence-based cause for each — not generic "if it fails" placeholders:

| ID | Where | Concrete failure mode | Root-cause hypothesis (from files actually read) | Recovery |
|---|---|---|---|---|
| F-ESC0 | GATE 0 | eng-security's N2 note flags a *new* risk beyond what the issue's own "blast radius" argument already covers | The issue argues Bash doesn't widen mutation (Write/Edit already held) — if eng-security instead finds a mutation-adjacent risk (e.g., a git verb that can alter working-tree state), that contradicts the issue's premise | Escalate to user/owner (H-31) — this is a genuine "stop and ask," not an auto-retry, because it means the plan's premise needs owner re-confirmation |
| F6 | N6 build | `uv run jerry agents build` fails | Most likely a YAML indentation error under `tools.native:` (a list-append is an easy place to break YAML syntax) or a canonical schema constraint violated (`docs/schemas/agent-canonical-v1.schema.json`) | Fix N5, retry N6 |
| F7 | N7 validate | Schema validation fails, **or** — the specific case called out in the task — `tool_tier` changes unexpectedly | Build succeeded but produced a `tools:` list inconsistent with the declared `tool_tier` ceiling (see Tool Security Tiers table, `.context/rules/agent-development-standards.md`) — should NOT happen here since Bash is already inside T2's ceiling and T4 is a superset of T2, but this is exactly the mechanical check that catches it if the build script's tier-inference logic has a bug | Fix N5 (or the build tooling, if the bug is in `jerry agents build` itself, which is out of scope for this plan and would need its own issue), retry |
| F8 | N8 diff | `jerry agents diff` shows drift beyond the Bash addition | Regeneration touched an unrelated field (e.g., description line-wrapping changed because `agents build` re-serializes YAML) | If the drift is cosmetic and expected from the build tool's normal serialization, document it in the PR; if it's a content change (e.g., another tool silently dropped), treat as a build-tool defect — fix N5 inputs or halt and file a separate bug against `jerry agents build` |
| **F9** | N9/N10 probes | Probe fails even though N6-N8 all passed | **Most likely cause, specific to this change:** N5 only edited the `.agent.yaml` `tools.native` list but the corresponding `<p003_self_check>` sentence in the `.prompt.md` ("This agent may ONLY use: file_read, file_write, file_edit, file_search_glob, file_search_content") was **not** updated. The frontmatter would correctly show `Bash`, `jerry agents validate`/`diff` would pass (they check schema/drift, not runtime self-consistency), and yet the agent would read its own system prompt's self-check text, conclude Bash use is a P-003 violation, and self-halt with the exact error string defined in its own prompt: `"P-003 VIOLATION: adv-executor attempted to spawn a subagent."` — a misleading error for what is actually a stale-prompt-text bug, not a real P-003 violation. This is precisely why N5's task description lists the `.prompt.md` edit as **mandatory**, not optional, alongside the YAML edit. | Fix the `.prompt.md` self-check text in N5, rebuild (N6-N8), re-run probes |
| F11 | N11 quality gate | Composite score < 0.92, or any Critical finding (auto-REVISE regardless of score per adv-scorer's own verdict table) | Most plausible: S-004 (Pre-Mortem) or S-012 (FMEA) surfaces a failure mode this plan's own [Failure Taxonomy](#failure-taxonomy) missed | Feed findings back to N5 as a revision (H-14 creator-critic-revision), max 3 iterations before escalating to user |

### Retry / Escalation Policy

- Each failure loop (F6, F7, F8, F9) returns to **N5** (fix source), not to N1/N2/N4 — those upstream nodes are not invalidated by a downstream build/probe failure.
- **Max 3 fix-and-retry cycles** per failure category before this plan requires human escalation — consistent with this being a C3, not C4, change (C4 would warrant a 10-iteration ceiling per RT-M-010; 3 is proportionate here).
- **GATE 0's failure path (F-ESC0) does not retry automatically** — it is a stop-and-ask because it means the plan's foundational assumption (owner already resolved the risk trade-off in the issue text) may be wrong.
- Per prior session guidance, worktracker Task/Enabler statuses are **not** flipped to a terminal (done) state until N13 (PR merge to `main`) completes — a green branch is not a closed item.

---

## Verification of graph.dot

`graph.dot` was rendered locally with `dot -Tsvg` during authoring to confirm it is valid Graphviz syntax (no errors, produces a single connected SVG). It is not embedded here to keep this document text-only; re-render with:

```bash
dot -Tsvg projects/PROJ-024-tactical-work/orchestration/adversary-bash-377/graph.dot -o graph.svg
```

---

## Disclaimer

This orchestration plan was generated by an orchestration-planning agent per the `/orchestration` skill conventions. Human review recommended before execution. No code, worktracker entities, or agent definition files have been modified by producing this plan — it is planning output only, per the scope of this request.

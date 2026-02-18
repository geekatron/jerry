# Getting Started with Jerry

> Follow this runbook to go from a freshly installed Jerry instance to your first successful skill invocation. By the end you will have a configured project, a running session, and a persisted output artifact on disk.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prerequisites](#prerequisites) | What you must have before starting |
| [Procedure](#procedure) | Step-by-step instructions |
| [Verification](#verification) | How to confirm success |
| [Troubleshooting](#troubleshooting) | Common failures and resolutions |
| [Next Steps](#next-steps) | Where to go after completing this runbook |

---

## Prerequisites

> **Start state:** You have completed the Jerry installation documented in [`../INSTALLATION.md`](../INSTALLATION.md). Do not proceed until all three criteria below are met.

- [ ] **`uv` is installed** and on your PATH — confirm with `uv --version` (minimum: uv 0.5.x or later)
- [ ] **Jerry is cloned** to your local filesystem (recommended: `~/plugins/jerry`) — confirm with `ls ~/plugins/jerry/pyproject.toml`
- [ ] **The Jerry plugin is registered** in Claude Code — in Claude Code, run `/plugin`, go to the **Installed** tab, and verify `jerry` appears (alternatively, confirm with `claude mcp list` from the terminal)

If any of these are not in place, complete the installation steps in [`../INSTALLATION.md`](../INSTALLATION.md) first, then return here. That document covers `uv` installation, Jerry repository cloning, and Claude Code plugin registration.

> **Tested with:** uv 0.5.x, Jerry CLI v0.2.0, Claude Code v2.x. If you are using different versions, the commands in this runbook should still work but minor output differences are possible.

---

## Procedure

### Step 1: Create a Project Directory

Jerry requires an active project to operate. Every session, skill invocation, and output artifact is scoped to a project. This is enforced by rule **[H-04](../../.context/rules/quality-enforcement.md#hard-rule-index)**: the `JERRY_PROJECT` environment variable MUST be set before any Jerry workflow can proceed.

Create the project directory structure:

```bash
# macOS / Linux
mkdir -p projects/PROJ-001-my-first-project/.jerry/data/items

# Windows PowerShell
New-Item -ItemType Directory -Force -Path "projects\PROJ-001-my-first-project\.jerry\data\items"
```

Create the two required project files:

```bash
# macOS / Linux
touch projects/PROJ-001-my-first-project/PLAN.md
touch projects/PROJ-001-my-first-project/WORKTRACKER.md

# Windows PowerShell
New-Item -ItemType File -Force -Path "projects\PROJ-001-my-first-project\PLAN.md"
New-Item -ItemType File -Force -Path "projects\PROJ-001-my-first-project\WORKTRACKER.md"
```

Expected result: The path `projects/PROJ-001-my-first-project/` exists and contains `PLAN.md`, `WORKTRACKER.md`, and the `.jerry/data/items/` subdirectory.

> **What are these files?** `PLAN.md` holds your project's implementation plan and scope. `WORKTRACKER.md` is the project-level work manifest — Jerry's skills and agents write work item entries (tasks, enablers, bugs, decisions) into this file as they execute, giving you a single-file view of all tracked work. You can inspect `WORKTRACKER.md` at any time to see what Jerry has tracked for your project.

> **Naming convention:** Project IDs follow the pattern `PROJ-{NNN}-{slug}` (e.g., `PROJ-001-my-first-project`). Use any slug that describes your work. You can list existing projects with `jerry projects list`.

---

### Step 2: Set the JERRY_PROJECT Environment Variable

Jerry reads the `JERRY_PROJECT` environment variable to determine which project is active. This variable must be set in the same terminal session where you run Claude Code.

```bash
# macOS / Linux
export JERRY_PROJECT=PROJ-001-my-first-project

# Windows PowerShell
$env:JERRY_PROJECT = "PROJ-001-my-first-project"
```

Confirm the variable is set:

```bash
# macOS / Linux
echo $JERRY_PROJECT

# Windows PowerShell
echo $env:JERRY_PROJECT
```

Expected output: `PROJ-001-my-first-project`

> **Why is this required (H-04)?** Jerry's hooks, skills, and output paths all depend on knowing which project is active. Without `JERRY_PROJECT`, the SessionStart hook cannot load project context, and any skill that attempts to write an output artifact will fail or write to an incorrect location. This is a hard constraint that cannot be bypassed.

> **Make it persistent:** To avoid setting the variable every session, add the `export` line to your shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.profile`). On Windows, set it as a user environment variable via System Properties > Environment Variables.

---

### Step 3: Start a Jerry Session

Open Claude Code in the same terminal session where `JERRY_PROJECT` is set. Jerry's SessionStart hook runs automatically when Claude Code starts. You can also trigger it explicitly:

```
jerry session start
```

The SessionStart hook will respond with one of three XML-tagged outputs. Read the output carefully — each tag requires a different action:

| Hook Tag | Meaning | Your Action |
|----------|---------|-------------|
| `<project-context>` | Project found and loaded successfully | Proceed — your session is active |
| `<project-required>` | `JERRY_PROJECT` is not set or points to a non-existent project | Set `JERRY_PROJECT` per Step 2 and retry |
| `<project-error>` | Project directory exists but is malformed (missing required files) | Verify `PLAN.md` and `WORKTRACKER.md` exist in the project directory, then retry |

Expected output (success):

```
<project-context>
Project PROJ-001-my-first-project loaded.
</project-context>
```

If you see `<project-context>`, your session is active and you are ready to invoke skills.

---

### Step 4: Invoke the Problem-Solving Skill

The problem-solving skill is the recommended first skill for new Jerry users. It has the lowest friction (no additional prerequisites beyond project setup) and demonstrates Jerry's core value: turning a natural language research or analysis request into a persisted, structured output artifact.

The skill activates automatically when your message contains trigger keywords: **research**, **analyze**, **investigate**, **explore**, **root cause**, or **why**.

Type a message like one of these in Claude Code:

```
Research the best practices for writing readable Python code.
```

```
Analyze why my tests are running slowly.
```

```
Investigate the root cause of context rot in large LLM sessions.
```

Jerry will invoke the problem-solving skill, run through its research and analysis agents, and save the output artifact to your project directory.

Expected behavior:
- Claude responds by activating the problem-solving skill — you will see a message indicating which agent was selected (e.g., "Invoking ps-researcher...") and where its output will be saved
- The skill runs one or more agents (researcher, analyst, synthesizer, etc.) and streams progress
- A persisted output artifact is written to a subdirectory under `projects/PROJ-001-my-first-project/` (e.g., `docs/research/` or `docs/analysis/`)

---

### Step 5: Verify the Output Artifact

After the skill completes, confirm the output artifact was saved to disk.

```bash
# macOS / Linux
ls projects/PROJ-001-my-first-project/

# Windows PowerShell
Get-ChildItem projects\PROJ-001-my-first-project\
```

All skill agents persist their output to your project directory as guaranteed by [P-002](../governance/JERRY_CONSTITUTION.md#p-002-file-persistence) (file persistence requirement). The specific subdirectory depends on which agent ran — for example, `ps-researcher` writes to `docs/research/`, `ps-analyst` writes to `docs/analysis/`, and `ps-synthesizer` writes to `docs/synthesis/`. See the [Problem-Solving Playbook](../playbooks/problem-solving.md#agent-reference) for the full agent-to-directory mapping.

```bash
# macOS / Linux — check for any new files recursively
find projects/PROJ-001-my-first-project -name "*.md" -newer projects/PROJ-001-my-first-project/PLAN.md

# Windows PowerShell — list new .md files (exclude PLAN.md and WORKTRACKER.md which were pre-existing)
Get-ChildItem -Recurse projects\PROJ-001-my-first-project\ -Filter "*.md" | Where-Object { $_.Name -notin @("PLAN.md", "WORKTRACKER.md") }
```

Expected result: One or more `.md` files exist under `projects/PROJ-001-my-first-project/` that were not there before Step 4. Files named `PLAN.md` and `WORKTRACKER.md` are pre-existing from Step 1 — look for new files in agent output subdirectories (`docs/research/`, `docs/analysis/`, etc.).

---

## Verification

> **End state:** You have a configured project with `JERRY_PROJECT` set, a successful session start showing `<project-context>`, and at least one persisted output artifact created by the problem-solving skill.

- [ ] `JERRY_PROJECT` is set and resolves to an existing project directory containing `PLAN.md` and `WORKTRACKER.md`
- [ ] `jerry session start` (or Claude Code startup) produced `<project-context>` output — not `<project-required>` or `<project-error>`
- [ ] At least one output artifact (`.md` file) exists under `projects/PROJ-001-my-first-project/` that was created by the problem-solving skill invocation

---

## Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `jerry session start` outputs `<project-required>` | `JERRY_PROJECT` environment variable is not set, or is set in a different terminal session than Claude Code | Run `export JERRY_PROJECT=PROJ-NNN-slug` (macOS/Linux) or `$env:JERRY_PROJECT = "PROJ-NNN-slug"` (Windows PowerShell) in the same terminal session, then restart Claude Code |
| `jerry session start` outputs `<project-error>` | `JERRY_PROJECT` points to a project directory that is missing required files | Verify the directory `projects/$JERRY_PROJECT/` exists and contains both `PLAN.md` and `WORKTRACKER.md`; create any missing files with `touch` (macOS/Linux) or `New-Item` (Windows), then retry |
| No output artifact created after skill invocation | `JERRY_PROJECT` was not set when Claude Code started, so skill output has no project context to write to | Confirm `JERRY_PROJECT` is set (`echo $JERRY_PROJECT`), restart Claude Code in the same terminal session, start a new session, and retry the skill invocation |
| `<project-context>` appears but skill does not activate | Trigger keyword not present in your message, or message phrasing did not match the skill's activation pattern | Use one of the exact trigger keywords: research, analyze, investigate, explore, root cause, why — for example: "Research X" or "Analyze the root cause of Y" |
| `jerry: command not found` | The Jerry CLI is not on your PATH, or the plugin is not installed | Verify the plugin is installed via `/plugin` > Installed tab in Claude Code; for CLI access, confirm the Jerry repository is on your PATH or use `uv run jerry` from the Jerry repository root |

---

## Next Steps

After completing this runbook, you have the foundational Jerry workflow in place. Explore the skill playbooks to deepen your use of each skill:

- [`../playbooks/problem-solving.md`](../playbooks/problem-solving.md) — All 9 problem-solving agents, trigger keywords, creator-critic cycle, and concrete invocation examples
- [`../playbooks/orchestration.md`](../playbooks/orchestration.md) — Multi-phase workflow coordination using orch-planner, orch-tracker, and orch-synthesizer
- [`../playbooks/transcript.md`](../playbooks/transcript.md) — Meeting transcript parsing: CLI invocation, domain contexts, and two-phase workflow

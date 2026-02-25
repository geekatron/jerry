# Devil's Advocate Report: Jerry Framework Installation Guide (Iteration 3)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `docs/INSTALLATION.md`
**Criticality:** C4 (Critical) — public-facing OSS installation guide, irreversible once distributed
**Date:** 2026-02-25
**Reviewer:** adv-executor (S-002 Devil's Advocate)
**H-16 Compliance:** S-003 Steelman applied 2026-02-18 — confirmed at `docs/reviews/adv-s003-steelman-install-docs.md`
**Prior S-002 Executions:** `docs/reviews/iteration-1-s002-devils-advocate.md` (iteration 1), `docs/reviews/iteration-2-s002-devils-advocate.md` (iteration 2)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Step 1: Advocate Role Assumption](#step-1-advocate-role-assumption) | Role framing, H-16 verification, iteration-2 resolution confirmation |
| [Step 2: Assumptions Extracted and Challenged](#step-2-assumptions-extracted-and-challenged) | Explicit and implicit assumption inventory for the current document |
| [Findings Summary](#findings-summary) | All findings by severity |
| [Detailed Findings](#detailed-findings) | Full evidence and analysis per finding |
| [Prior Execution: Finding Status](#prior-execution-finding-status) | Iteration-2 finding resolution verification |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [Execution Statistics](#execution-statistics) | Counts and metadata |

---

## Step 1: Advocate Role Assumption

**Deliverable challenged:** `docs/INSTALLATION.md` (iteration 3 revision, 2026-02-25)
**Criticality level:** C4 (Critical) — public-facing OSS documentation, irreversible once distributed
**H-16 verified:** S-003 Steelman output confirmed at `docs/reviews/adv-s003-steelman-install-docs.md`, executed 2026-02-18. Deliverable strengthened before this critique begins.
**Prior executions verified:**
- Iteration 1: `docs/reviews/iteration-1-s002-devils-advocate.md` — 7 findings (1 Critical, 4 Major, 2 Minor)
- Iteration 2: `docs/reviews/iteration-2-s002-devils-advocate.md` — 6 findings (0 Critical, 3 Major, 3 Minor)

**Role assumed:** Argue the strongest possible case that this installation guide still fails its readers — as a skeptical first-time user who arrives mid-document from a direct link, a search engine result, or the documentation site's sidebar navigation. The document must be examined for: (1) whether all iteration-2 findings were resolved per their acceptance criteria, (2) whether additional changes introduced new structural weaknesses, and (3) whether any residual gaps remain that would cause real-world installation failures.

**Focus for iteration 3:**
1. Verify resolution of all 6 iteration-2 findings (DA-001-it2 through DA-006-it2) against their acceptance criteria
2. Identify whether the additional fixes (slash command orientation, network requirements, Windows persistence, air-gapped path, JERRY_PROJECT verification, no-repo guidance, Local Clone Step 3 variable notation) introduced any new ambiguities
3. Conduct fresh adversarial sweep of the document, applying all 6 counter-argument lenses per the strategy protocol
4. Produce findings on any new or residual weaknesses

---

## Step 2: Assumptions Extracted and Challenged

| # | Assumption | Type | Challenge |
|---|------------|------|-----------|
| 1 | The `JERRY_PROJECT` environment variable will be recognized by skills regardless of the format the user enters | Implicit | The document states the format is `PROJ-{NNN}-{slug}` but does not state what happens if a user enters `my-project`, `proj001`, or another non-conforming format — whether skills reject it, silently accept it, or emit a specific error |
| 2 | The `jerry-framework` source name used in the Updating section matches the name registered by all users | Implicit | The Updating section hardcodes `/plugin marketplace update jerry-framework` without a source-name variability note — users who installed via HTTPS or whose source registered under a different name will encounter a failure with no inline recovery guidance, unlike the Uninstallation section which was fixed in iteration 2 |
| 3 | Windows users in the Local Clone section who need to find their username can determine the full plugin path from `echo $env:USERNAME` | Implicit | The instruction to "run `echo $env:USERNAME` in PowerShell" gives the username but not the full path — users need `$env:USERPROFILE` (e.g., `C:\Users\USERNAME`) to construct the full source path, which is what the `/plugin marketplace add` command requires |
| 4 | Users who launch Claude Code via `--plugin-dir` for "a consistent project directory" workflow know how to make this launch pattern persistent | Implicit | The Session Install section identifies this as a "legitimate workflow" for certain users but does not explain how to implement it persistently (no alias, script, or shortcut guidance) |
| 5 | The `.jerry/` gitignore instruction ("Add `.jerry/` to your `.gitignore` if it's not already there") is actionable without a command | Implicit | Users who ran `git init` to create a repo (as suggested in the "Don't have a repository yet?" note) will have no `.gitignore` and no knowledge of whether the `.jerry/` entry is present |
| 6 | Users who read "hooks should activate automatically" understand this as an expected outcome, not as a hedge on uncertain behavior | Implicit | The inline verification signal (`<project-context>` tag) was added in iteration 2; the revised sentence at line 201 provides the quick check — this assumption is now adequately addressed in the current document |
| 7 | The routing table's "Arriving from the HTTPS row?" callout is seen by no-SSH users before they encounter the SSH command in Step 1 | Implicit | The callout appears as a blockquote between the section introduction and the Step 1 heading — users skimming for bold section headers may skip blockquotes and land directly on the Step 1 two-row table where SSH appears first |
| 8 | The Session Install section's HTTPS-only clone URL is consistent with the full install path's multi-option presentation | Implicit | The Local Clone section shows both HTTPS and SSH clone options (with a dedicated "Advanced: SSH clone" sub-section) while the Session Install section shows only HTTPS, creating an inconsistency for SSH-preferring users |
| 9 | Users who receive `<project-required>` output will be able to distinguish between "JERRY_PROJECT not set," "JERRY_PROJECT set but format invalid," and "project directory not created" as causes | Implicit | The Verification and Troubleshooting sections address the `<project-required>` symptom but the Configuration section does not state whether invalid formats produce a different symptom than the missing-variable case |
| 10 | The Updating section's "Local clone users" sub-section only requires `git pull` — no uv dependency update is needed | Implicit | After `git pull`, the Jerry codebase may have updated Python dependencies in `pyproject.toml` that are not automatically applied without `uv sync`; this is not mentioned in the Updating section |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001-it3 | Major | Updating section hardcodes `jerry-framework` in the update command without a source-name variability note — the same structural omission that was fixed in the Uninstallation section in iteration 2 (DA-005-it2) but was not applied here | Updating → GitHub-installed users |
| DA-002-it3 | Major | `JERRY_PROJECT` format violation has no documented consequence — the Configuration section specifies the format but does not state what happens when the format is wrong, leaving users with silent failures or confusing `<project-required>` errors with no diagnostic path | Configuration → Project Setup |
| DA-003-it3 | Minor | Windows Local Clone Step 2 instructs users to run `echo $env:USERNAME` to find their username, but the full path they need for the `/plugin marketplace add` command requires `$env:USERPROFILE`, not `$env:USERNAME` | Local Clone → Step 2: Add as a local plugin source |
| DA-004-it3 | Minor | Session Install section identifies the `--plugin-dir` flag as a "legitimate workflow" for consistent-directory users but provides no guidance on how to make the launch pattern persistent (no alias, function, or shortcut example) | Session Install |
| DA-005-it3 | Minor | Configuration Step 4 instructs users to add `.jerry/` to `.gitignore` if not present but provides no command or verification method — users who created a repo with `git init` per the "Don't have a repository yet?" note will have no `.gitignore` and no way to check | Configuration → Step 4 |

---

## Detailed Findings

### DA-001-it3: Updating Section Hardcodes `jerry-framework` Without Source-Name Variability Note [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Updating → GitHub-installed users (lines 608–613) |
| **Strategy Step** | Step 3 — Unstated assumptions; Contradicting evidence (same issue fixed elsewhere in the document) |

**Claim Challenged:**
> "### GitHub-installed users
>
> Jerry updates when the source repository updates. To pull the latest:
>
> ```
> /plugin marketplace update jerry-framework
> ```"
> (INSTALLATION.md, lines 607–613)

**Counter-Argument:**
The iteration-2 finding DA-005-it2 (Minor) identified that the Uninstallation section's `/plugin uninstall jerry@jerry-framework` hardcoded the source name without a variability note. This was resolved: the Uninstallation section now includes `"> **Source name differs?** Use the name from `/plugin marketplace list`: `/plugin uninstall jerry@<name-from-list>`."` The acceptance criteria for DA-005-it2 required this note to be visible at the point of the command.

The same structural omission is present in the Updating section: `/plugin marketplace update jerry-framework` hardcodes `jerry-framework` with no equivalent "source name differs?" note. A user whose source registered under a different name — because they used the HTTPS URL variant or had a name variation at registration time — will run this command, receive a "source not found" error, and have no inline recovery guidance.

The document does include the fix for Uninstallation, confirming the author is aware of this pattern. The Updating section was not updated with the same consistency fix. The evidence that the author applied this fix to Uninstallation but not to Updating creates an internal documentation inconsistency: the Updating command is in the same "at-risk" category but lacks the correction that was deemed necessary one section later.

The severity is Major (rather than Minor as DA-005-it2 was) for two reasons: (1) Updating is a more frequent user action than Uninstalling — users who follow Jerry's development will run the update command on every release, while uninstallation is typically a one-time action; (2) the fix was already demonstrated as necessary and applied to an adjacent command, making the omission here a regression in consistency rather than an undiscovered gap.

**Evidence:**
Line 611: `/plugin marketplace update jerry-framework` (hardcoded source name)

Compare with Uninstallation section (lines 633–637) where the fix was applied:
> "```
> /plugin uninstall jerry@jerry-framework
> ```
> > **Source name differs?** Use the name from `/plugin marketplace list`: `/plugin uninstall jerry@<name-from-list>`."

The pattern is present in Uninstallation but absent in Updating.

**Impact:** Users who installed via HTTPS URL or whose source registered under a name other than `jerry-framework` — a non-trivial population given that the HTTPS path is now a first-class routing option — will run the update command, encounter a "source not found" or equivalent error, and have no inline recovery path. They must navigate to Troubleshooting or run `/plugin marketplace list` themselves to discover the correct name.

**Recommendation:** Add a source-name note under the Updating command, mirroring the Uninstallation pattern:

```
/plugin marketplace update jerry-framework
```
> **Source name differs?** Run `/plugin marketplace list` to find your source name, then: `/plugin marketplace update <name-from-list>`.

**Acceptance Criteria:** The Updating section's GitHub-installed users sub-section includes an inline note about source name variability that is visible at the point of the command, matching the pattern applied in the Uninstallation section. A user whose source registered under a different name can complete the update command on the first attempt without a trial-and-error failure.

---

### DA-002-it3: `JERRY_PROJECT` Format Violation Has No Documented Consequence [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Configuration → Project Setup (lines 346–381) |
| **Strategy Step** | Step 3 — Unaddressed risks; Unstated assumptions |

**Claim Challenged:**
> "> **Project naming:** The format is `PROJ-{NNN}-{slug}`. Pick any slug that describes your work (e.g., `PROJ-001-my-api`). Your first project is typically `PROJ-001`."
> (INSTALLATION.md, lines 348–349)

**Counter-Argument:**
The Configuration section correctly specifies the `JERRY_PROJECT` format (`PROJ-{NNN}-{slug}`) and provides a concrete example. However, the document never states what happens if a user sets `JERRY_PROJECT` to a non-conforming value such as `my-project`, `myproject`, `proj-001`, or `PROJ001`.

The document's Troubleshooting section addresses the `<project-required>` symptom with: "It means Jerry installed successfully but no project is configured." The cause list identifies "JERRY_PROJECT is not set, points to a non-existent project, or the project directory was created in the wrong location." It does not identify "JERRY_PROJECT is set but in an invalid format" as a distinct cause.

This creates a diagnostic gap: a user who sets `JERRY_PROJECT=my-first-project` has technically set the variable. The variable is not empty — it fails the "is not set" cause. If the project directory exists under `projects/my-first-project/`, it may not fail the "points to a non-existent project" cause either. The user will see `<project-required>` (or inconsistent behavior, depending on whether Jerry validates the format at skill invocation time) but will have no path from the symptom to the root cause.

The counter-argument: the format requirement is stated but treated as advisory rather than enforced. If the format is enforced (skills reject or warn on non-conforming values), the document should say so and describe the error. If the format is merely conventional (skills accept any string), the document should say the format is a naming convention, not a hard requirement. As written, the format is stated authoritatively (`"The format is..."`) but the consequence of violation is not described — leaving users to discover the impact empirically.

**Evidence:**
Lines 348–349 (format stated):
> "The format is `PROJ-{NNN}-{slug}`. Pick any slug that describes your work (e.g., `PROJ-001-my-api`). Your first project is typically `PROJ-001`."

Troubleshooting → Project Issues (lines 487–497) — cause list for `<project-required>`:
> "Cause: `JERRY_PROJECT` is not set, points to a non-existent project, or the project directory was created in the wrong location."

The cause list does not include "invalid format" as a possible cause.

**Impact:** A user who enters `JERRY_PROJECT=my-project` or `JERRY_PROJECT=PROJ001` will: (a) proceed through Configuration believing they have set the variable correctly, (b) create the project directory under the non-conforming name, (c) start Claude Code and see `<project-required>`, (d) read the Troubleshooting section and find their situation does not match any listed cause, and (e) be unable to self-diagnose without experimentation. This is a silent failure mode that affects new users — the population most likely to deviate from the stated format without understanding the consequences.

**Recommendation:** Add one of the following to the Project Naming note:

**Option A (if the format is enforced):**
> "The format is `PROJ-{NNN}-{slug}`. Jerry's skills validate this format — if the format is wrong, you'll see `<project-error>` instead of `<project-context>`. Your first project is typically `PROJ-001`."

**Option B (if the format is conventional):**
> "The format is `PROJ-{NNN}-{slug}` — this is a naming convention, not a hard requirement. Any string works, but using the standard format ensures compatibility with all Jerry skills and templates. Your first project is typically `PROJ-001`."

**Acceptance Criteria:** The Project naming note explicitly states either (a) that format violations produce a specific error and what that error looks like, or (b) that the format is conventional and any string is accepted. A user who enters a non-conforming format either receives a clear error they can trace to the format, or knows in advance that the format is flexible. The Troubleshooting section's cause list should be updated to include format-related issues if the format is enforced.

---

### DA-003-it3: Windows Local Clone Step 2 Directs Users to `$env:USERNAME` When They Need `$env:USERPROFILE` [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Local Clone → Step 2: Add as a local plugin source (lines 254–260) |
| **Strategy Step** | Step 3 — Logical flaws; contradicting evidence |

**Claim Challenged:**
> "**Windows (Claude Code):** Use forward slashes — `/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry`
>
> Replace `YOUR_USERNAME` with your actual Windows username. To find it, run `echo $env:USERNAME` in PowerShell."
> (INSTALLATION.md, lines 256–260)

**Counter-Argument:**
The instruction to find the username via `echo $env:USERNAME` is technically correct: `$env:USERNAME` returns the current user's login name. However, the instruction's purpose is to help users construct the full path for the `/plugin marketplace add` command — `C:/Users/YOUR_USERNAME/plugins/jerry`.

The Windows clone command in Step 1 used `"$env:USERPROFILE\plugins\jerry"` as the destination. `$env:USERPROFILE` expands to the full home directory path (e.g., `C:\Users\anowak`). The instruction to run `echo $env:USERNAME` returns only `anowak`, not `C:\Users\anowak`. A user who runs this command and sees `anowak` must then mentally assemble `C:/Users/anowak/plugins/jerry` — requiring them to know that `C:/Users/<USERNAME>` is the Windows home directory path.

The more direct instruction would be to run `echo $env:USERPROFILE` (which returns `C:\Users\anowak` directly) or to construct the source path using the variable directly in the command: `/plugin marketplace add "$env:USERPROFILE/plugins/jerry"`. However, since Claude Code chat input may not expand PowerShell variables, the manual path construction is likely necessary — making the `$env:USERPROFILE` disclosure the correct remedy.

The current instruction is not wrong, but it requires the user to perform a mental transformation step that `$env:USERPROFILE` eliminates.

**Evidence:**
Lines 256–260:
> "Replace `YOUR_USERNAME` with your actual Windows username. To find it, run `echo $env:USERNAME` in PowerShell."

The Step 1 Windows clone command (lines 244–246) uses:
> `git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"`

The variable used in Step 1 (`$env:USERPROFILE`) provides the full path; the diagnostic command suggested in Step 2 (`$env:USERNAME`) provides only the username component, requiring the user to reconstruct the full path.

**Impact:** Minor. Most Windows users know that `C:\Users\<USERNAME>` is the standard home directory path and can mentally assemble the full path from their username. The instruction is sufficient for the majority. Users who are unfamiliar with Windows path conventions (less experienced users who may have been routed to Local Clone due to network restrictions) may need to guess or search to determine that the full path is `C:\Users\<USERNAME>`.

**Recommendation:** Update the path-finding instruction to return the full path directly:

> "Replace `YOUR_USERNAME` with your actual Windows username. To find your full home path, run `echo $env:USERPROFILE` in PowerShell — this returns the full path (e.g., `C:\Users\anowak`). Use that path in the command above."

**Acceptance Criteria:** The Windows Local Clone Step 2 instruction directs users to a PowerShell command that returns the full home directory path (or provides enough context that users do not need to know the Windows home directory structure to complete the step).

---

### DA-004-it3: Session Install Section Identifies `--plugin-dir` as a "Legitimate Workflow" Without Explaining How to Make It Persistent [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Session Install (lines 306–321) |
| **Strategy Step** | Step 3 — Unaddressed risks; Alternative interpretations |

**Claim Challenged:**
> "**Note:** The `--plugin-dir` flag loads the plugin for that session only. It does not persist across sessions. For persistent installation, use the [Install from GitHub](#install-from-github) or [Local Clone](#local-clone) methods. For users who launch Claude Code from a consistent project directory, session-scoped loading can be a legitimate workflow — not just a trial run."
> (INSTALLATION.md, lines 319–320)

**Counter-Argument:**
The note correctly identifies a legitimate use case: users who launch Claude Code from a consistent project directory for whom the `--plugin-dir` flag constitutes a repeatable workflow rather than a one-off trial. The note's intention is to validate this pattern for that user segment.

However, the note validates the pattern without explaining how to implement it repeatably. A user who reads "session-scoped loading can be a legitimate workflow" and decides to adopt it must then independently figure out:
- How to create a shell alias (`alias claude-jerry='claude --plugin-dir ~/plugins/jerry'`)
- How to add the alias to their shell profile
- Or how to create a project-directory launch script

None of these are documented. The note tells the user this workflow is valid but leaves implementation entirely to them. For an OSS documentation guide targeting users who may not be power shell users, this is a gap between validation and enablement.

The counter-argument: identifying a use case as "legitimate" without providing the implementation creates a category of users who are validated in their choice but unsupported in executing it. These users will either figure it out independently (power users, no documentation needed) or will return to the guide looking for the "how" and not find it.

**Evidence:**
Lines 319–320:
> "For users who launch Claude Code from a consistent project directory, session-scoped loading can be a legitimate workflow — not just a trial run."

No alias, script, or shell-profile instructions follow this statement.

**Impact:** Minor. The Session Install method is already self-sufficient for its primary use case (one-time trial). The legitimate-workflow validation is additive context. Users who need the implementation details are sufficiently technical to find them independently. The gap does not block installation for any user — it only fails to fully enable a described use case.

**Recommendation:** Add a brief implementation note after the legitimate-workflow validation:

> "For users who launch Claude Code from a consistent project directory, session-scoped loading can be a legitimate workflow — not just a trial run. To make it repeatable: add a shell alias to your profile — `alias claude-jerry='claude --plugin-dir ~/plugins/jerry'` (macOS/Linux), then source your profile or open a new terminal."

**Acceptance Criteria:** The note either provides a brief example of how to make the `--plugin-dir` pattern repeatable (alias or script), or explicitly defers to the user's preferred shell customization method. Users who choose this workflow can implement it without independently researching shell aliases.

---

### DA-005-it3: Configuration Step 4 `.gitignore` Instruction Is Imperative Without a Verification Command [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Configuration → Step 4 (lines 378–379) |
| **Strategy Step** | Step 3 — Unaddressed risks; Unstated assumptions |

**Claim Challenged:**
> "The `.jerry/` directory contains operational state and is gitignored — do not commit it. Add `.jerry/` to your `.gitignore` if it's not already there."
> (INSTALLATION.md, lines 378–379)

**Counter-Argument:**
The instruction is conditionally imperative: "add `.jerry/` to your `.gitignore` **if it's not already there**." The condition ("if it's not already there") requires the user to verify the current state of `.gitignore` before acting. The document does not provide:
1. A command to check whether `.jerry/` is already in `.gitignore`
2. The command to add it if it is absent
3. Any guidance for users who ran `git init` to create their repo (per the "Don't have a repository yet?" note) and have no `.gitignore` at all

A user who followed the "Don't have a repository yet?" path (line 376: `mkdir my-project && cd my-project && git init`) will have a new repo with no `.gitignore`. For this user, "if it's not already there" evaluates to true, but they are left to figure out how to add an entry to a file that does not exist.

The counter-argument is that the instruction creates action debt without providing the action. The preceding Step 4 commands (lines 369–374) are explicit bash commands — `mkdir -p projects/...` — with platform alternatives. The `.gitignore` instruction is the only imperative in the Configuration section that does not include a command.

**Evidence:**
Lines 378–379:
> "Add `.jerry/` to your `.gitignore` if it's not already there. Jerry auto-creates additional subdirectories..."

Lines 376 (the path that leads to a new repo with no `.gitignore`):
> "Don't have a repository yet? Jerry works in any directory. Create one: `mkdir my-project && cd my-project && git init`, then run the `mkdir` command above."

No `.gitignore` creation or population command is provided in either location.

**Impact:** Minor. Most users who reach the Configuration section have an existing repository with a `.gitignore`. `git init` in newer Git versions may auto-create a `.gitignore`. Experienced users know the `echo '.jerry/' >> .gitignore` pattern. However, for new users following the "Don't have a repository yet?" path, this is an instruction that ends with ambiguity rather than a clear command.

**Recommendation:** Add a command to complete the instruction:

```bash
# macOS/Linux
echo '.jerry/' >> .gitignore

# Windows PowerShell
Add-Content .gitignore '.jerry/'
```

Or at minimum: add a verification and add pattern inline:
> "Check with `cat .gitignore | grep .jerry` and add if absent: `echo '.jerry/' >> .gitignore` (macOS/Linux) or `Add-Content .gitignore '.jerry/'` (Windows)."

**Acceptance Criteria:** The `.gitignore` instruction includes a command that both checks for and adds the `.jerry/` entry, or explicitly separates the check step from the add step with platform-specific commands. Users who created a new repo with `git init` can follow the instruction without independently knowing how to populate `.gitignore`.

---

## Prior Execution: Finding Status

| Prior Finding | Prior Severity | Current Status | Evidence |
|---------------|---------------|----------------|---------|
| DA-001-it2: Interactive Installation prerequisite caveat after numbered instructions | Major | **Resolved** — The **Important** callout (line 144) now appears before the numbered steps: "Jerry won't appear in the Discover tab until you complete Step 1 above." Acceptance criterion met. | Lines 144–153: Important callout precedes the numbered list |
| DA-002-it2: SSH and no-SSH routing rows link to the same anchor | Major | **Resolved** — "Arriving from the HTTPS row?" callout added at lines 77 before Step 1, directing no-SSH users to the second row of Step 1's command table. Acceptance criterion met. | Line 77: "Arriving from the HTTPS row in the table above? Use the HTTPS command in Step 1 below (the second row in the table)." |
| DA-003-it2: Step 3 install command hardcodes `jerry-framework` without variable notation | Major | **Resolved** — Step 3 now uses `/plugin install jerry@<name-from-step-2>` with `jerry@jerry-framework` as the concrete example. Acceptance criterion met. | Lines 108–112: Variable notation in primary instruction, example showing `jerry@jerry-framework` |
| DA-004-it2: "Hooks should activate automatically" lacks inline verification signal | Minor | **Resolved** — Line 201 now includes: "Quick check: start a new session — if you see a `<project-context>` tag in the output, hooks are live." Acceptance criterion met. | Line 201: inline `<project-context>` verification signal |
| DA-005-it2: Uninstall command hardcodes `jerry@jerry-framework` without source-name note | Minor | **Resolved** — Lines 633–637 now include: "Source name differs? Use the name from `/plugin marketplace list`: `/plugin uninstall jerry@<name-from-list>`." Acceptance criterion met. | Lines 633–637: Source-name variability note present |
| DA-006-it2: SSH check does not warn about wrong-account edge case | Minor | **Resolved** — Lines 63–64 now read: "If you see `Hi <username>!` and `<username>` is your GitHub account, you have SSH set up. If the username is unexpected, or you see 'Permission denied,' use the HTTPS path." Acceptance criterion met. | Lines 63–64: username verification instruction added |

**Summary:** All 6 iteration-2 findings fully resolved per their acceptance criteria. 0 findings carried forward. 5 new findings identified in this iteration (2 Major, 3 Minor). 0 Critical findings.

**Net improvement from iteration 2 to iteration 3:** Critical count: 0 → 0. Major count: 3 → 2. Minor count: 3 → 3. Total: 6 → 5. The document demonstrates measurable quality improvement: all Major iteration-2 findings are resolved, the fix applied to Uninstallation (DA-005-it2) reveals a parallel omission in Updating (DA-001-it3), and the `JERRY_PROJECT` format gap (DA-002-it3) is a pre-existing documentation omission now surfaced by fresh adversarial sweep.

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

No Critical findings in this iteration.

### P1 — Major (SHOULD resolve; require justification if not)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-it3 | Add a source-name variability note under the Updating section's `/plugin marketplace update jerry-framework` command, matching the pattern applied in the Uninstallation section: "Source name differs? Run `/plugin marketplace list` to find your source name, then: `/plugin marketplace update <name-from-list>`." | The Updating section's GitHub-installed users sub-section includes an inline note about source name variability visible at the point of the command. A user whose source registered under a different name can complete the update on the first attempt. |
| DA-002-it3 | Add a consequence statement to the Project naming note clarifying either (a) that format violations produce a specific error (`<project-error>`) and what it looks like, or (b) that the format is a naming convention and any string is accepted. Update the Troubleshooting cause list if format violations produce a distinct symptom. | The Project naming note explicitly states the consequence of format deviation. A user who enters a non-conforming value knows in advance whether to expect an error or whether any format is accepted. |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-003-it3 | Update the Windows Local Clone Step 2 path-finding instruction to direct users to `echo $env:USERPROFILE` (returns full home path) rather than `echo $env:USERNAME` (returns username only), eliminating the mental path-construction step. | The Windows path-finding instruction returns the full directory path needed for the `/plugin marketplace add` command without requiring users to know Windows home directory structure. |
| DA-004-it3 | Add a brief alias or script example to the Session Install note that validates the `--plugin-dir` legitimate-workflow pattern, so users who choose this path know how to implement it repeatably. | The note provides at minimum one concrete example of how to make the `--plugin-dir` pattern persistent (alias, script, or profile entry). |
| DA-005-it3 | Add platform-specific commands to the `.jerry/` gitignore instruction in Configuration Step 4: `echo '.jerry/' >> .gitignore` (macOS/Linux) and `Add-Content .gitignore '.jerry/'` (Windows), covering the case where `.gitignore` does not yet exist. | The Configuration Step 4 `.gitignore` instruction includes a concrete command. Users who created a new repo with `git init` can follow the instruction without independently knowing how to populate `.gitignore`. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | The document covers all four install paths, air-gapped environments, Windows-specific guidance, network requirements, and JERRY_PROJECT setup. DA-001-it3 (Updating section omission) and DA-002-it3 (JERRY_PROJECT format consequence) are coverage gaps, but both are targeted and addressable without structural rework. The overall completeness is strong; the gaps are specific sub-sections, not missing categories. |
| Internal Consistency | 0.20 | Mixed | DA-001-it3 identifies a direct inconsistency: the Uninstallation section was updated with a source-name variability note (DA-005-it2 fix) but the Updating section was not updated with the same pattern. This is a consistency regression — the fix was applied to one command but not the adjacent command in a parallel situation. The rest of the document is internally consistent; cross-section links are accurate, step numbering is correct, and platform alternatives are consistently provided. |
| Methodological Rigor | 0.20 | Positive | The install methodology is sound across all four paths. Step 2 (verification) feeds Step 3 (install) correctly for the GitHub path. The Local Clone path uses variable notation in Step 3. The four-path routing table is comprehensive. The Configuration section follows a logical four-step sequence. DA-002-it3 (format consequence) is a documentation rigor gap, not a methodology gap — the workflow itself is correct, the documentation of consequences is incomplete. |
| Evidence Quality | 0.15 | Positive | Factual claims remain accurate: the 12-skill count, the hook stability assessment (SessionStart and UserPromptSubmit most stable), the `<project-context>` verification signal, and the marketplace distinction. No new factual inaccuracies identified. The security note for the uv installation script is appropriately scoped. |
| Actionability | 0.15 | Mixed | DA-002-it3 (JERRY_PROJECT format consequence) and DA-005-it3 (`.gitignore` command) are actionability gaps where the document tells users what to do but not what to expect or how to complete the action with a concrete command. These affect new users specifically — the population for whom actionable instructions are most important. DA-001-it3 and DA-003-it3 are also actionability gaps (update command fails without recovery guidance; path construction requires a mental step). |
| Traceability | 0.10 | Positive | Cross-section links are accurate. The "Source name mismatch?" callout in Step 3 links to the Troubleshooting section. The navigation table covers all sections. The "Arriving from the HTTPS row?" callout links back to the correct section. No traceability regressions from iteration 2. |

**Overall Assessment:** 0 Critical, 2 Major, 3 Minor findings. This is the strongest iteration yet: all 6 iteration-2 findings are fully resolved, and the 5 new findings are targeted gaps (a consistency omission in Updating, an undocumented consequence for format violations, and three minor usability improvements). No finding represents a fundamental documentation failure.

The two Major findings are actionable with single-sentence or single-snippet fixes. DA-001-it3 requires copying the pattern already applied to Uninstallation into Updating. DA-002-it3 requires one sentence clarifying whether the `JERRY_PROJECT` format is enforced or conventional — information the author already knows, just not yet documented.

**Recommendation: REVISE — two targeted fixes required before acceptance. Both Major findings are single-location edits that do not require structural rework. Once resolved, the document should be in a strong position to pass S-014 scoring at the 0.92+ threshold.**

---

## Execution Statistics

- **Total Findings:** 5
- **Critical:** 0
- **Major:** 2 (DA-001-it3, DA-002-it3)
- **Minor:** 3 (DA-003-it3, DA-004-it3, DA-005-it3)
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** Confirmed — S-003 Steelman applied 2026-02-18 at `docs/reviews/adv-s003-steelman-install-docs.md`
- **H-15 Self-Review Applied:** Yes — all findings verified for: specific evidence from deliverable with line citations, justified severity classification, DA-NNN-it3 identifier format, summary table consistency with detailed findings, no findings omitted or minimized
- **Prior Findings Fully Resolved (iteration 2 → iteration 3):** 6 of 6 (DA-001-it2 through DA-006-it2)
- **Prior Findings Partially Resolved:** 0 of 6
- **Prior Findings Completely Unaddressed:** 0 of 6
- **New Findings Not in Prior Execution:** 5 (DA-001-it3 through DA-005-it3)
- **Critical Count Change:** 0 (iteration 2) → 0 (iteration 3)
- **Major Count Change:** 3 (iteration 2) → 2 (iteration 3)
- **Minor Count Change:** 3 (iteration 2) → 3 (iteration 3)
- **Total Count Change:** 6 (iteration 2) → 5 (iteration 3)
- **Dimensions with Negative Impact:** 0 of 6
- **Dimensions with Mixed Impact:** 2 of 6 (Internal Consistency, Actionability)
- **Dimensions Positive:** 4 of 6 (Completeness, Methodological Rigor, Evidence Quality, Traceability)
- **P0 Findings (block acceptance):** 0
- **P1 Findings:** 2
- **P2 Findings:** 3

---

*Strategy: S-002 Devil's Advocate*
*Template Version: 1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Finding Prefix: DA-NNN-it3*
*Execution Date: 2026-02-25*
*Prior Executions: `docs/reviews/iteration-1-s002-devils-advocate.md`, `docs/reviews/iteration-2-s002-devils-advocate.md`*
*Steelman Reference: `docs/reviews/adv-s003-steelman-install-docs.md`*

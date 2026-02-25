# Red Team Report: INSTALLATION.md

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `docs/INSTALLATION.md` — Jerry Framework Installation Guide
**Criticality:** C4 (public-facing OSS documentation, irreversible first-impression surface)
**Date:** 2026-02-25
**Reviewer:** adv-executor (S-001 Red Team Analysis)
**H-16 Compliance:** S-003 Steelman not confirmed as prior step. This execution was user-directed as a standalone C4 adversarial review. H-16 advisory documented; no prior S-003 output was provided. Execution proceeds at user direction.
**Threat Actors:** Four personas (see Step 1 below)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Step 1: Threat Actor Profiles](#step-1-threat-actor-profiles) | Four adversarial user personas defined |
| [Step 2: Attack Vector Inventory](#step-2-attack-vector-inventory) | All vectors by persona with RT-NNN identifiers |
| [Step 3: Defense Gap Assessment](#step-3-defense-gap-assessment) | Existing defenses and gaps per vector |
| [Step 4: Countermeasures](#step-4-countermeasures) | Specific remediation actions per P0 and P1 |
| [Step 5: Findings Summary](#step-5-findings-summary) | Consolidated summary table |
| [Detailed Findings](#detailed-findings) | Full detail for Critical and Major findings |
| [Scoring Impact](#scoring-impact) | S-014 dimension impact mapping |
| [Overall Assessment](#overall-assessment) | Recommendation and path forward |

---

## Step 1: Threat Actor Profiles

### Persona A: The Confused Newcomer

| Field | Value |
|-------|-------|
| **Goal** | Get Jerry installed without knowing what Claude Code is, what SSH is, or what a "marketplace" means — survival goal: not feel stupid, succeed on first try |
| **Capability** | Knows Git basics, has a GitHub account, has a Mac (assumed), can follow numbered steps if they are unambiguous |
| **Knowledge Gaps** | No SSH keys, has never heard of `uv`, doesn't know what a "plugin" context is inside Claude Code, confused by surf/snowboard metaphors |
| **Motivation** | Heard about Jerry from a blog post or colleague; wants to try it; will abandon if two consecutive steps fail without explanation |
| **Success Condition** | Runs `/problem-solving` and sees it activate, without needing to debug |

### Persona B: The Corporate IT Admin

| Field | Value |
|-------|-------|
| **Goal** | Install Jerry for a team; justify every tool, script execution, and network call to security; ensure no policy violations |
| **Capability** | Deep IT knowledge; controls proxy, firewall, and endpoint policy; can execute any command but must clear security review first |
| **Knowledge Gaps** | Not a developer; unfamiliar with Claude Code plugin system; skeptical of shell-pipe-to-sh install patterns |
| **Motivation** | Developer team asked for Jerry; IT is gatekeeping; needs to assess security posture before approving |
| **Success Condition** | Completes install without executing unreviewed scripts, without outbound calls to blocked domains, with an audit trail |

### Persona C: The Windows Developer

| Field | Value |
|-------|-------|
| **Goal** | Install Jerry on Windows; use PowerShell as primary shell; never use bash or Unix commands |
| **Capability** | Expert in Windows/PowerShell; knows Git; uses Claude Code on Windows; can follow documentation |
| **Knowledge Gaps** | Unfamiliar with macOS conventions (tilde paths, `~`, `.zshrc`); doesn't know if Windows edge cases are fully handled |
| **Motivation** | Wants to use Jerry on their primary development machine; frustrated when docs treat Windows as an afterthought |
| **Success Condition** | Full installation including hooks functional on Windows without undocumented workarounds |

### Persona D: The Impatient Expert

| Field | Value |
|-------|-------|
| **Goal** | Install Jerry in under 60 seconds; already knows Claude Code plugins; will skim the document |
| **Capability** | Senior developer; fluent with SSH, git, uv, Claude Code; reads only commands and callout boxes |
| **Knowledge Gaps** | None technically — but impatience causes them to skip context they assume is boilerplate |
| **Motivation** | Wants to evaluate Jerry quickly; doesn't want to read paragraphs before running commands |
| **Success Condition** | Two commands copy-pasted, plugin running, JERRY_PROJECT set, done |

---

## Step 2: Attack Vector Inventory

### Persona A: Confused Newcomer

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-001-20260225 | No orientation on what Claude Code "is" in a Jerry context — newcomer lands on Prerequisites but doesn't know if they should open their terminal, open Claude Code, or open a browser | Ambiguity | High | Major | P1 | Partial | Completeness |
| RT-002-20260225 | "SSH key configured for GitHub" is listed as Required but the newcomer has no SSH key and the "why SSH" note is buried in a blockquote after the table — they see the requirement, panic, and stop | Boundary | High | Major | P1 | Partial | Actionability |
| RT-003-20260225 | `/plugin marketplace add geekatron/jerry` is described as running "in Claude Code" but there is no instruction on HOW to run a slash command inside Claude Code — newcomer opens the app and doesn't know if they type in a chat box, a terminal, or somewhere else | Ambiguity | High | Critical | P0 | Missing | Completeness |
| RT-004-20260225 | The "Which Install Method?" decision table assumes the newcomer knows their own situation ("No SSH key," "locked-down network") — a newcomer who has never installed SSH keys doesn't know they are missing them until they fail | Dependency | Medium | Major | P1 | Missing | Completeness |
| RT-005-20260225 | Step 4 of Configuration creates `projects/PROJ-001-my-project/.jerry/data/items` but there is no explanation of WHERE to run the mkdir command relative to — the note says "run this from your repository root" but newcomer may not have a repository yet | Ambiguity | High | Major | P1 | Partial | Completeness |
| RT-006-20260225 | The Verification section instructs "start a new Claude Code session" to trigger hooks but gives no instruction on how to start a new session — newcomer may not know the difference between starting a new session and just typing in an existing window | Ambiguity | Medium | Minor | P2 | Missing | Actionability |

### Persona B: Corporate IT Admin

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-007-20260225 | The uv installer (`curl ... \| sh`) is flagged with a security note but the note only describes HOW to inspect the script — it does not describe WHAT the script does (installs a binary to ~/.local/bin, modifies PATH in shell profile) making security sign-off impossible without reading the full script | Dependency | High | Major | P1 | Partial | Evidence Quality |
| RT-008-20260225 | No network access requirements documented — the installation requires outbound access to `github.com`, `astral.sh`, and `code.claude.com/docs` but none of these are listed as prerequisites, making it impossible for IT to pre-authorize domains | Dependency | High | Critical | P0 | Missing | Completeness |
| RT-009-20260225 | The HTTPS Local Clone bypass for firewall-restricted networks requires git clone access to `github.com` — if the firewall blocks GitHub entirely, there is no documented air-gap or enterprise proxy path | Boundary | High | Major | P1 | Missing | Completeness |
| RT-010-20260225 | uv installs a binary from `astral.sh` and then Claude Code hooks execute that binary via shell — the doc does not state what CLAUDE_PLUGIN_ROOT resolves to or what file-system permissions the hooks require, making endpoint security assessment impossible | Dependency | Medium | Major | P1 | Missing | Evidence Quality |
| RT-011-20260225 | The "review it first" guidance for the uv install script is the only security mitigation offered but there is no hash/checksum provided for the downloaded script, meaning the review-then-run pattern provides no protection against supply chain substitution between download and review | Dependency | Low | Minor | P2 | Missing | Methodological Rigor |

### Persona C: Windows Developer

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-012-20260225 | The "Make it persistent" step for `JERRY_PROJECT` on Windows uses `Set-Variable -Name JERRY_PROJECT -Value ... -Scope Global` — this is a per-session variable set in the PowerShell profile, not a system environment variable; it will not propagate to terminal emulators that spawn non-PowerShell child processes (e.g., WSL, cmd.exe, or VS Code integrated terminal using bash) | Ambiguity | High | Major | P1 | Missing | Actionability |
| RT-013-20260225 | The Configuration section's persistent project setup on Windows adds the variable only to the PowerShell profile but Claude Code on Windows may not source the PowerShell profile at startup — there is no instruction to verify that `JERRY_PROJECT` is visible inside Claude Code's terminal context | Dependency | High | Major | P1 | Missing | Completeness |
| RT-014-20260225 | The Hooks verification step says "start a new Claude Code session" and look for `<project-context>` in output — on Windows, if hooks depend on symlinks (as noted in the Platform Note), hooks may silently fail and there is no Windows-specific troubleshooting step for hook failures | Boundary | High | Major | P1 | Partial | Completeness |
| RT-015-20260225 | PATH management after uv install on Windows: the troubleshooting step says "Add `%USERPROFILE%\.local\bin` to System PATH" but the actual uv Windows installer places the binary at a different path (`~/.cargo/bin` or `~/.local\bin` depending on installer version) — no verification command is provided before the PATH fix | Ambiguity | Medium | Minor | P2 | Missing | Actionability |
| RT-016-20260225 | The Platform Note warns about Windows limitations (hooks using symlinks, junction points) but no explicit list of WHICH hooks are affected is provided — the Windows developer cannot determine which rows of the Capability Matrix are unreliable without reading the codebase | Ambiguity | High | Major | P1 | Partial | Completeness |

### Persona D: Impatient Expert

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-017-20260225 | There is no "TL;DR / Quick Install" block at the top of the document — an expert who skims sees prose before commands and must read two paragraphs before reaching the first executable command | Degradation | High | Minor | P2 | Missing | Actionability |
| RT-018-20260225 | The expert runs `/plugin marketplace add geekatron/jerry` and then runs `/plugin install jerry@jerry-framework` — if the source registers under a different name, they hit a cryptic "plugin not found" error and must go to Troubleshooting to learn about `/plugin marketplace list`; this troubleshooting step is not surfaced inline with Step 2 as a recovery path | Circumvention | High | Major | P1 | Partial | Actionability |
| RT-019-20260225 | Configuration step 4 (create project structure) requires the user to know WHICH repository to run mkdir from — an expert who has multiple repos open will create the `projects/` directory under whichever repo they happen to be in when they follow the docs; the instruction "run from your repository root" is underspecified for multi-repo contexts | Ambiguity | Medium | Minor | P2 | Partial | Actionability |
| RT-020-20260225 | The JERRY_PROJECT environment variable must be set before starting Claude Code, but the document does not state this explicitly — an expert sets the variable, starts Claude Code in the same terminal session (variable is live), but after they close and reopen and the profile-based persistence fails (e.g., wrong shell), they get `<project-required>` with no obvious cause | Dependency | Medium | Major | P1 | Partial | Completeness |

---

## Step 3: Defense Gap Assessment

| ID | Existing Defense | Classification | Exploitability by Adversary |
|----|-----------------|----------------|----------------------------|
| RT-001-20260225 | "Don't have Claude Code yet?" blockquote mentions quickstart | Partial | Newcomer sees it but it's a side-note; main flow does not acknowledge the context switch between terminal and Claude Code interface |
| RT-002-20260225 | SSH note and HTTPS alternative documented | Partial | The HTTPS alternative is in a blockquote after the requirements table — a reader who sees "Required" and no SSH key may stop before reading the blockquote |
| RT-003-20260225 | None — the doc never explains WHERE slash commands are entered in Claude Code | Missing | **Complete gap.** A person who has never used Claude Code cannot complete Step 1 without external research |
| RT-004-20260225 | None — "Which Install Method?" table provides no self-diagnosis for the newcomer who doesn't know their SSH status | Missing | Newcomer must fail first to learn they lack SSH keys |
| RT-005-20260225 | "Run from your repository root" note present | Partial | Newcomer who has no existing repository is unaddressed; the concept of "your repository" is undefined for someone installing before creating a project |
| RT-006-20260225 | None | Missing | Minor impact |
| RT-007-20260225 | Security note with inspect-then-run guidance | Partial | Note describes HOW to inspect but not WHAT the script does systemically |
| RT-008-20260225 | None — no network requirements section | Missing | **Complete gap.** Critical for corporate users |
| RT-009-20260225 | Local Clone method documented but requires github.com access | Partial | If github.com is fully blocked there is no offline/enterprise path |
| RT-010-20260225 | None | Missing | Hook execution model and permissions not documented |
| RT-011-20260225 | Inspect guidance provided | Partial | No integrity verification (hash/checksum) |
| RT-012-20260225 | Windows PowerShell command provided | Partial | Wrong scope for cross-shell compatibility |
| RT-013-20260225 | None | Missing | No verification that JERRY_PROJECT reaches Claude Code |
| RT-014-20260225 | "Hit a wall? File it" Windows issue template referenced | Partial | Hooks section has no Windows-specific troubleshooting |
| RT-015-20260225 | None | Missing | uv binary path unspecified for Windows |
| RT-016-20260225 | Platform Note mentions hooks affected by symlinks | Partial | No specific list of which hooks are affected |
| RT-017-20260225 | Table of Contents and "Which Install Method?" help | Partial | No TL;DR block; expert must read past prose to reach commands |
| RT-018-20260225 | Troubleshooting section has the fix | Partial | Not visible inline at the failure point (Step 2) |
| RT-019-20260225 | "Run from repo root" mentioned | Partial | Underspecified for multi-repo contexts |
| RT-020-20260225 | Profile persistence step documented | Partial | Does not state that JERRY_PROJECT must be visible to Claude Code's process, or how to verify this |

---

## Step 4: Countermeasures

### P0 — Critical: MUST address before acceptance

**RT-003-20260225: No instruction on how to enter slash commands in Claude Code**

Countermeasure: Add a one-sentence orientation note immediately before Step 1 of the "Install from GitHub" section: "Claude Code commands beginning with `/` are entered in the Claude Code chat window — type them directly in the message input and press Enter." Include a screenshot reference or link to Claude Code's UI introduction if available.

Acceptance Criteria: A user who has installed Claude Code but has never typed a slash command can locate the input area and run `/plugin marketplace add geekatron/jerry` without consulting external documentation.

**RT-008-20260225: No network access requirements listed**

Countermeasure: Add a "Network Requirements" row to the Prerequisites table (or a sub-section under Prerequisites) listing the domains that must be reachable: `github.com` (plugin source, SSH or HTTPS), `astral.sh` (uv installer), `code.claude.com` (Claude Code itself). Mark each as required for which method. For corporate users explicitly note that the Local Clone method reduces external dependencies to only `github.com`.

Acceptance Criteria: A corporate IT admin can derive the complete outbound domain allowlist from the Prerequisites section without reading the full document.

### P1 — Important: SHOULD address

**RT-002-20260225: SSH requirement creates a stop point before the HTTPS alternative is visible**

Countermeasure: Restructure the Prerequisites SSH row. Change the table entry from "SSH key configured for GitHub — **Yes**" to "SSH key configured for GitHub — **Recommended (not required — see note)**". The HTTPS alternative callout should use a visible alert/warning format rather than a blockquote so that readers scanning the table see the escape hatch immediately.

Acceptance Criteria: A reader who sees the SSH row in the table and has no SSH key immediately understands (without reading a blockquote) that an HTTPS alternative exists.

**RT-004-20260225: "Which Install Method?" requires self-knowledge newcomer lacks**

Countermeasure: Add a self-diagnosis question to the decision table: "Not sure if you have an SSH key? Run `ssh -T git@github.com` in your terminal. If you see 'Hi username!' you have one. If you see 'Permission denied (publickey)' — use the HTTPS or Local Clone method." Place this immediately above or within the decision table.

Acceptance Criteria: A newcomer can determine which install method applies to them without attempting the primary method and failing.

**RT-007-20260225: uv installer security note describes HOW but not WHAT**

Countermeasure: Add a one-paragraph "What this script does" description in the security note: "The installer downloads the uv binary for your platform, places it at `~/.local/bin/uv` (macOS/Linux) or `~/.local\bin\uv.exe` (Windows), and appends a PATH export to your shell profile (`~/.zshrc`, `~/.bashrc`, or PowerShell profile). It does not require root/administrator privileges and makes no system-wide changes." This allows IT to assess scope without reading the script.

Acceptance Criteria: An IT admin reading the uv security note can describe the installer's system impact in a security review without executing or reading the install script.

**RT-009-20260225: No air-gap or proxy path for fully-blocked networks**

Countermeasure: Add a note in the Local Clone section for fully restricted environments: "If github.com is blocked entirely: (1) clone the repository from a machine with GitHub access, (2) transfer the directory to the restricted machine via your organization's approved mechanism, (3) proceed from Step 2 (Add as a local plugin source) using the local path." Note that uv installation may similarly require an offline installer from Astral's GitHub releases.

Acceptance Criteria: A reader in a fully-air-gapped environment has a documented (if manual) path to complete installation.

**RT-010-20260225: Hook execution model and permissions not documented**

Countermeasure: Add a brief "How hooks work" technical note under the Enable Hooks section: "Jerry's hooks are Python scripts executed by Claude Code using the uv binary. When a hook fires, Claude Code calls `uv run --directory {CLAUDE_PLUGIN_ROOT} jerry {hook-name}`. The scripts read and write files within your project directory (`projects/{JERRY_PROJECT}/`) and the Jerry plugin directory. No network access is required at hook execution time. No elevated privileges are required."

Acceptance Criteria: An IT admin can describe the runtime behavior of Jerry's hooks in a security review from the documentation alone.

**RT-012-20260225: Windows JERRY_PROJECT persistence uses wrong variable scope**

Countermeasure: Replace the Windows persistence command from:
```
Add-Content $PROFILE 'Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global'
```
to:
```
Add-Content $PROFILE '$env:JERRY_PROJECT = "PROJ-001-my-project"'
```
The `$env:` syntax sets a proper environment variable that propagates to child processes, whereas `Set-Variable -Scope Global` sets a PowerShell-session-only variable that does not propagate.

Acceptance Criteria: The `JERRY_PROJECT` variable set via the Windows profile command is visible in `$env:JERRY_PROJECT` in a new PowerShell session and in Claude Code's environment when launched from that shell.

**RT-013-20260225: No verification that JERRY_PROJECT reaches Claude Code**

Countermeasure: Add a verification step to the Configuration section: "After setting `JERRY_PROJECT`, verify it's visible to Claude Code by opening a new terminal session (which loads the updated profile), then starting Claude Code from that terminal. In Claude Code, run: `echo $JERRY_PROJECT` (macOS/Linux) or `echo $env:JERRY_PROJECT` (Windows PowerShell). If this returns your project ID, the variable is configured correctly. If empty, see Troubleshooting."

Acceptance Criteria: A user can verify `JERRY_PROJECT` is correctly propagated before starting a Claude Code session and encountering `<project-required>`.

**RT-014-20260225: No Windows-specific hook troubleshooting**

Countermeasure: Add a "Hooks not firing on Windows" subsection to the Troubleshooting section: "Jerry's hooks use file system operations that may behave differently on Windows. If hooks are not firing after installing uv: (1) verify `uv --version` works in the same terminal you use to launch Claude Code; (2) check whether `CLAUDE_PLUGIN_ROOT` resolves to a path without spaces (spaces in paths cause hook invocation failures on Windows); (3) check the [GitHub Issues](https://github.com/geekatron/jerry/issues) for current Windows hook status — some hooks use symlink operations that require Developer Mode on Windows."

Acceptance Criteria: A Windows user experiencing hook failures has a Windows-specific diagnostic checklist without having to file an issue first.

**RT-016-20260225: Platform Note doesn't specify which hooks are affected by Windows symlink limitation**

Countermeasure: Expand the Platform Note to list which specific hooks are affected: "Known Windows limitations: [list specific hooks e.g., `SessionStart`, `PreCompact`] use symlink operations and require Windows Developer Mode or will use junction points instead. Hooks [list] are unaffected on Windows."

Acceptance Criteria: A Windows developer can look at the Capability Matrix and cross-reference which specific rows may be unreliable on their platform.

**RT-018-20260225: "Plugin not found" recovery path not visible at Step 2**

Countermeasure: In Step 2 of Install from GitHub, expand the failure callout to be more prominent: "If `/plugin install jerry@jerry-framework` fails with 'plugin not found': the source name may differ from `jerry-framework`. Run `/plugin marketplace list` to see the exact registered name, then use `/plugin install jerry@<name-from-list>`." This content already exists in Troubleshooting but should also appear inline at the point of failure.

Acceptance Criteria: An expert user who hits "plugin not found" immediately sees the recovery command without navigating to Troubleshooting.

**RT-020-20260225: JERRY_PROJECT must be set before Claude Code launch but this is not stated**

Countermeasure: Add an explicit note to the Configuration section and the Verification section: "Important: `JERRY_PROJECT` must be set in the terminal session BEFORE launching Claude Code. Claude Code inherits environment variables from the terminal it's launched from. If you set the variable after Claude Code is already running, restart Claude Code from a terminal where the variable is set."

Acceptance Criteria: A user who sets `JERRY_PROJECT` in one terminal and launches Claude Code from a different terminal understands why hooks show `<project-required>` and knows to restart Claude Code from the correct terminal.

### P2 — Monitor

**RT-005-20260225 (Minor):** The "repository root" assumption for mkdir should note that a newcomer may need to create a repository first. Low priority — the note is present and most readers will have an existing repo.

**RT-006-20260225 (Minor):** Add "Close and reopen Claude Code" to the hooks verification step to clarify what "start a new session" means.

**RT-011-20260225 (Minor):** Consider linking to uv's published release checksums for users who want to verify installer integrity before execution.

**RT-015-20260225 (Minor):** Add `uv --version` as the canonical PATH verification step on Windows (works regardless of install path), before giving the manual PATH fix.

**RT-017-20260225 (Minor):** A "Quick Install" summary block at the top (3 commands, no prose) would serve expert users without harming newcomers who would read past it.

**RT-019-20260225 (Minor):** Strengthen the "run from your repo root" note with: "this means the root of the specific repository where you'll use Jerry."

---

## Step 5: Findings Summary

| ID | Persona | Attack Vector (short) | Category | Exploit | Severity | Priority | Defense |
|----|---------|----------------------|----------|---------|----------|----------|---------|
| RT-001-20260225 | Newcomer | No context for Claude Code interface vs terminal | Ambiguity | High | Major | P1 | Partial |
| RT-002-20260225 | Newcomer | SSH "Required" stops reader before HTTPS alternative visible | Boundary | High | Major | P1 | Partial |
| RT-003-20260225 | Newcomer | No instruction on how to enter slash commands in Claude Code | Ambiguity | High | **Critical** | **P0** | Missing |
| RT-004-20260225 | Newcomer | Decision table requires self-knowledge newcomer lacks | Dependency | Medium | Major | P1 | Missing |
| RT-005-20260225 | Newcomer | mkdir "from repo root" — newcomer may have no repo | Ambiguity | High | Major | P1 | Partial |
| RT-006-20260225 | Newcomer | "Start a new session" undefined | Ambiguity | Medium | Minor | P2 | Missing |
| RT-007-20260225 | IT Admin | uv installer described HOW to review but not WHAT it does | Dependency | High | Major | P1 | Partial |
| RT-008-20260225 | IT Admin | No network access requirements documented | Dependency | High | **Critical** | **P0** | Missing |
| RT-009-20260225 | IT Admin | No air-gap/fully-blocked-network path | Boundary | High | Major | P1 | Missing |
| RT-010-20260225 | IT Admin | Hook execution model and permissions not documented | Dependency | Medium | Major | P1 | Missing |
| RT-011-20260225 | IT Admin | No hash/checksum for install script integrity | Dependency | Low | Minor | P2 | Missing |
| RT-012-20260225 | Windows | JERRY_PROJECT persistence uses wrong PowerShell scope | Ambiguity | High | Major | P1 | Missing |
| RT-013-20260225 | Windows | No verification that JERRY_PROJECT reaches Claude Code | Dependency | High | Major | P1 | Missing |
| RT-014-20260225 | Windows | No Windows-specific hook troubleshooting | Boundary | High | Major | P1 | Partial |
| RT-015-20260225 | Windows | uv binary path unspecified on Windows | Ambiguity | Medium | Minor | P2 | Missing |
| RT-016-20260225 | Windows | Which specific hooks are affected by Windows symlinks — not listed | Ambiguity | High | Major | P1 | Partial |
| RT-017-20260225 | Expert | No TL;DR / Quick Install block | Degradation | High | Minor | P2 | Missing |
| RT-018-20260225 | Expert | "Plugin not found" recovery not inline at Step 2 | Circumvention | High | Major | P1 | Partial |
| RT-019-20260225 | Expert | "Repo root" underspecified in multi-repo contexts | Ambiguity | Medium | Minor | P2 | Partial |
| RT-020-20260225 | Expert | JERRY_PROJECT must be set before Claude Code launch — not stated | Dependency | Medium | Major | P1 | Partial |

**Totals: 2 Critical (P0), 12 Major (P1), 6 Minor (P2)**

---

## Detailed Findings

### RT-003-20260225: No Instruction on How to Enter Slash Commands in Claude Code [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Persona** | Confused Newcomer |
| **Section** | Install from GitHub — Step 1 |
| **Category** | Ambiguity |
| **Exploitability** | High |

**Attack Vector:** A user who has just installed Claude Code for the first time opens the application and is presented with this instruction:

> "In Claude Code, run: `/plugin marketplace add geekatron/jerry`"

They have no prior knowledge of where to type this. Claude Code has a chat interface, a terminal panel, and potentially other surfaces depending on version and OS. There is nothing in the document — not in Prerequisites, not in the intro, not in Step 1 — explaining that slash commands are typed into the Claude Code chat/input window.

**Evidence from deliverable:** Step 1 says "In Claude Code, run:" with no qualification of where in Claude Code. The Prerequisites section mentions Claude Code's existence and version requirements but does not orient the user to its interface. The entire "Install from GitHub" section assumes the user knows the Claude Code UI.

**Consequence:** The newcomer cannot complete Step 1. They may: type the command in their terminal (getting "command not found"), search for a separate Claude Code CLI, or abandon the installation entirely. This is a complete installation blocker for anyone who has not used Claude Code before.

**Existing Defense:** None. There is no Claude Code UI orientation anywhere in the document.

**Countermeasure:** Before Step 1 in Install from GitHub, add: "Slash commands (`/plugin`, `/problem-solving`, etc.) are entered in the Claude Code chat window — type them directly in the message input and press Enter, just like sending a message." This single sentence closes the gap.

**Acceptance Criteria:** A user who has installed Claude Code but has never used a slash command can locate the input area and execute Step 1 without consulting external documentation.

---

### RT-008-20260225: No Network Access Requirements Documented [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Persona** | Corporate IT Admin |
| **Section** | Prerequisites |
| **Category** | Dependency |
| **Exploitability** | High |

**Attack Vector:** A corporate IT admin reviewing the document to approve Jerry for their organization's developer team cannot find a list of required outbound network connections anywhere in the document. The installation process silently requires:

- `github.com` — plugin source clone (SSH or HTTPS)
- `astral.sh` — uv installer download
- `code.claude.com` — Claude Code documentation links
- Potentially `raw.githubusercontent.com` — depending on how plugin source fetching works

Without this information, the IT admin cannot: (1) pre-authorize the required domains on the corporate firewall, (2) determine if uv can be installed via internal mirror, (3) complete a security review of third-party connections. The installation will fail silently at whichever step first requires a blocked domain.

**Evidence from deliverable:** The Prerequisites table lists software requirements only. No network requirements are documented anywhere. The troubleshooting entry "Corporate proxy/firewall — if restricted, use the Local Clone instead" acknowledges the issue but does not name domains or describe the full network surface.

**Consequence:** Corporate deployments fail at an unpredictable point. IT cannot approve Jerry for team use without reverse-engineering the network requirements by watching network traffic during a test install — a high-friction process that could result in rejection of the tool entirely.

**Existing Defense:** The troubleshooting section notes "Corporate proxy/firewall" as a known issue, but provides no preventive information. This is a reactive mention, not a preventive network requirements specification.

**Countermeasure:** Add a "Network Requirements" subsection in Prerequisites or a dedicated callout box. Content: the complete list of required domains, the method (HTTPS/SSH), and which installation step requires each. Note which methods reduce the network surface (Local Clone eliminates the dependency on astral.sh if uv is already installed).

**Acceptance Criteria:** An IT admin can derive the complete outbound domain allowlist from the Prerequisites section without any additional research or test installation.

---

### RT-002-20260225: SSH "Required" Creates Stop Point Before HTTPS Alternative Is Visible [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Confused Newcomer |
| **Section** | Prerequisites table |
| **Category** | Boundary |
| **Exploitability** | High |

**Attack Vector:** The Prerequisites table lists "SSH key configured for GitHub — **Yes** (Required)". A newcomer reading this table sees "Required" and assumes they cannot proceed without SSH keys. The HTTPS alternative is documented — but in a blockquote that follows the table. Many users stop reading when they see a requirement they cannot meet; they do not scroll down to find the exception.

**Evidence from deliverable:** Prerequisites table row: `SSH key configured for GitHub | Yes | Claude Code clones plugins via SSH (see note below)`. The "see note below" instruction requires the reader to read past the table. The table cell says "Yes" (Required) with no inline indication that a workaround exists.

**Consequence:** Newcomers without SSH keys either set up SSH (adding 10-30 minutes to their installation experience and introducing a new failure surface) or abandon the installation. Both outcomes are avoidable.

**Existing Defense:** The blockquote after the table does explain the HTTPS alternative clearly. The "Which Install Method?" table also mentions "No SSH key" as a condition for Local Clone. These defenses exist but are not positioned to stop a reader who halts at "Required."

**Countermeasure:** Change the "Required" cell in the Prerequisites table to "Recommended (HTTPS alternative available — see note)" to make the escape hatch visible without reading the blockquote. Alternatively, add a two-word parenthetical in the table: "SSH key for GitHub | Yes\* | \*HTTPS alternative available — see note below."

**Acceptance Criteria:** A reader who scans the Prerequisites table and has no SSH key does not believe they are blocked from proceeding.

---

### RT-007-20260225: uv Installer "How to Review" Provided but "What It Does" Absent [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Corporate IT Admin |
| **Section** | Enable Hooks — Install uv — Security Note |
| **Category** | Dependency |
| **Exploitability** | High |

**Attack Vector:** The security note for the uv installer provides instructions for HOW to download and review the install script before execution. However, it does not describe WHAT the script does — specifically: which directories it writes to, whether it requires elevated privileges, whether it modifies system-wide PATH, and what it leaves behind after installation. For corporate security reviews, this is the essential information.

**Evidence from deliverable:** Security note says: "If your organization requires script inspection before execution: on macOS/Linux, download first with `curl -LsSf https://astral.sh/uv/install.sh -o install-uv.sh`, review it, then run `sh install-uv.sh`." The note describes the inspection process but not the installation scope.

**Consequence:** The IT admin cannot write a security assessment saying "the uv installer makes no system-wide changes and does not require elevated privileges" because the document doesn't say that. They must read the install script themselves — which takes significantly more time than a one-paragraph summary would require.

**Countermeasure:** Add a "What the installer does" summary within or immediately after the security note. Content: installs binary to `~/.local/bin/uv` (user-level, no root required), appends PATH export to shell profile, no other system modifications.

**Acceptance Criteria:** An IT admin reading the security note can describe the installer's system impact in a security review without executing or reading the install script.

---

### RT-012-20260225: Windows JERRY_PROJECT Persistence Uses Wrong PowerShell Scope [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Windows Developer |
| **Section** | Configuration — Step 3 |
| **Category** | Ambiguity |
| **Exploitability** | High |

**Attack Vector:** The Windows PowerShell command for persistent `JERRY_PROJECT`:

```
Add-Content $PROFILE 'Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global'
```

`Set-Variable -Scope Global` sets a PowerShell variable visible within the current PowerShell session. It does NOT set an environment variable. This means:

1. The variable is not visible as `$env:JERRY_PROJECT` in the same session or subprocesses
2. Claude Code, which is launched as a child process, cannot read PowerShell session variables — it can only read environment variables
3. When the PowerShell profile is sourced, only the current PowerShell session has the variable; Claude Code launched from that session still won't have it in its environment

**Evidence from deliverable:** Configuration step 3, Windows variant:
```
Add-Content $PROFILE 'Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global'
```
The macOS/Linux equivalent uses `export JERRY_PROJECT=...` which is correct (sets an environment variable). The Windows equivalent uses a PowerShell session variable that does not propagate.

**Consequence:** Windows users who follow the documented persistence step will see `<project-required>` every time they start Claude Code, with no obvious cause. The variable exists in their PowerShell session (`Get-Variable JERRY_PROJECT` returns a value) but Claude Code cannot see it. This creates a particularly confusing debugging scenario where "the variable is set" but "hooks don't work."

**Countermeasure:** Replace `Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global` with `$env:JERRY_PROJECT = "PROJ-001-my-project"` in the Add-Content command. The `$env:` syntax sets a proper environment variable that is visible to child processes including Claude Code.

**Acceptance Criteria:** After following the Windows persistence step, `echo $env:JERRY_PROJECT` in a new PowerShell session returns the project ID, and Claude Code launched from that session recognizes the project.

---

### RT-016-20260225: Platform Note Does Not Specify Which Hooks Are Affected by Windows Symlinks [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Windows Developer |
| **Section** | Platform Note (top of document) and Enable Hooks |
| **Category** | Ambiguity |
| **Exploitability** | High |

**Attack Vector:** The Platform Note at the top of the document states: "Known Windows limitations: bootstrap uses junction points instead of symlinks, and paths in Claude Code commands must use forward slashes." The hooks section lists 6 hooks in a capability table. However, there is no mapping from "which hooks use symlinks" to the capability matrix rows. A Windows developer installing Jerry cannot determine:

- Which of the 6 hooks will work correctly on Windows
- Which hooks will silently fail vs. visibly error
- Whether "fail-open" behavior means they still get the capability or they get nothing

**Evidence from deliverable:** Platform Note: "hooks that use symlinks or path-sensitive operations may behave differently." The hooks capability table (SessionStart, UserPromptSubmit, PreCompact, PreToolUse, SubagentStop, Stop) has no Windows-specific column or annotation. The Capability Matrix rows are listed without any Windows qualification.

**Consequence:** Windows users install Jerry, install uv, and then cannot determine from the documentation which subset of the Capability Matrix they will actually receive. They may run for weeks under the impression that hooks are working when specific enforcement layers are silently failing.

**Countermeasure:** Add a Windows column to the hooks table (or an inline annotation) indicating which hooks are fully functional, which have reduced functionality, and which may fail. If this information is not yet fully characterized, a note stating "Windows hook support is being actively tested; follow [this GitHub Issue] for current status" is acceptable.

**Acceptance Criteria:** A Windows developer reading the Enable Hooks section can determine which hooks are expected to work on their platform without reading the codebase.

---

### RT-018-20260225: "Plugin Not Found" Recovery Not Surfaced Inline at Step 2 [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Impatient Expert |
| **Section** | Install from GitHub — Step 2 |
| **Category** | Circumvention |
| **Exploitability** | High |

**Attack Vector:** An expert runs Step 2 (`/plugin install jerry@jerry-framework`) and hits "plugin not found." The document has an inline callout note pointing to Troubleshooting for this case. The expert ignores the note (they don't read notes when they think they understand the command) and instead re-runs the command with variations. The actual fix (`/plugin marketplace list` then use the listed name) is fully documented in Troubleshooting but is only reachable if the reader navigates there.

**Evidence from deliverable:** Step 2 callout: "Install command fails? The source name must match exactly. Run `/plugin marketplace list` to see what Claude Code registered, then use that name: `/plugin install jerry@<name-from-list>`. See Plugin not found after adding source in Troubleshooting for more details." The fix IS documented inline, but the callout uses the phrase "Install command fails?" which an expert scanning for bold text or code blocks may skip.

**Consequence:** Expert users spend disproportionate time debugging a known failure mode. The document is technically complete but the information architecture means the fix is not found by users who most need it quickly.

**Countermeasure:** Restructure Step 2 to make the recovery command visible without requiring the reader to recognize they are in a "command fails" scenario. Move `/plugin marketplace list` earlier — suggest running it after Step 1 to verify the source name before running the install. This turns a failure-recovery step into a confirmation step, visible to all users regardless of whether they fail.

**Acceptance Criteria:** An expert user who runs Step 2 and sees "plugin not found" can find and execute the recovery command within the same screen of content, without navigating to Troubleshooting.

---

### RT-020-20260225: JERRY_PROJECT Must Be Set Before Claude Code Launch — Not Explicitly Stated [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Impatient Expert |
| **Section** | Configuration |
| **Category** | Dependency |
| **Exploitability** | Medium |

**Attack Vector:** The document tells users to set `JERRY_PROJECT` and make it persistent via their shell profile. However, it does not explain the launch dependency: `JERRY_PROJECT` must be present in the environment of the process that launches Claude Code. If a user sets the variable in one terminal session and Claude Code is already running (or is launched from a different terminal with a stale environment), the hook will see an empty `JERRY_PROJECT` and emit `<project-required>`.

**Evidence from deliverable:** Configuration section step 2 and 3 describe setting and persisting `JERRY_PROJECT`. There is no statement that Claude Code must be launched from a terminal where this variable is already set, nor that restarting Claude Code is required after setting it.

**Consequence:** Expert users who set `JERRY_PROJECT` in a terminal session and then switch to an already-open Claude Code window encounter `<project-required>`. They verify the variable is set (it is, in their terminal), and cannot understand why Jerry doesn't see it. This is a common environment-variable confusion that is entirely preventable with a single sentence.

**Countermeasure:** Add to Configuration and Verification: "Claude Code inherits environment variables from the terminal session it was launched from. After setting `JERRY_PROJECT`, start Claude Code from the same terminal to ensure it picks up the variable. If Claude Code is already running, restart it from a terminal where the variable is set."

**Acceptance Criteria:** A user who sets `JERRY_PROJECT` and immediately gets `<project-required>` understands from the document that they need to restart Claude Code from the correct terminal.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| **Completeness** | 0.20 | Negative | RT-003 (no slash command orientation), RT-008 (no network requirements), RT-009 (no air-gap path), RT-016 (no Windows hook specifics) — four substantive completeness gaps across major personas |
| **Internal Consistency** | 0.20 | Negative | RT-012 (Windows variable persistence command uses wrong mechanism, inconsistent with macOS/Linux which correctly uses environment variables) and RT-020 (launch-order dependency not stated, inconsistent with the stated persistence instructions that imply it "just works") |
| **Methodological Rigor** | 0.20 | Neutral | The document's installation methodology is sound and the step ordering is correct. Rigor is not the primary failure mode; the failures are gaps and platform-specific completeness issues |
| **Evidence Quality** | 0.15 | Negative | RT-007 (uv installer security note describes inspection method but not what the installer does — the evidence of safety is the act of reviewing, not a factual summary of behavior) and RT-010 (hook execution model undocumented — security-conscious users cannot assess safety from the document alone) |
| **Actionability** | 0.15 | Negative | RT-002 (SSH prerequisite stop-point), RT-004 (decision table requires self-knowledge), RT-013 (no JERRY_PROJECT verification step before proceeding), RT-018 (failure recovery not inline) — four gaps that reduce the document's ability to guide users through failures |
| **Traceability** | 0.10 | Neutral | The document is well-structured with a navigation table, anchor links, and clear section references. Traceability of instructions to outcomes is adequate. |

**Overall document score estimate pre-remediation:** The 2 Critical and 12 Major findings spread across all 4 test personas indicate the document serves experienced macOS users well but has significant gaps for newcomers, Windows users, and corporate contexts. Estimated composite impact: approximately -0.08 to -0.12 relative to a fully complete version. Post-remediation (all P0/P1 addressed), the document would close these gaps substantially.

---

## Overall Assessment

**Recommendation: REVISE — targeted remediation required before C4 acceptance**

The document has a solid structure, good navigation, and handles the primary macOS/GitHub install path well. For users who match the "happy path" (macOS, SSH configured, no corporate firewall, some Claude Code familiarity), the installation guide is functional.

The Red Team exercise revealed that the document fails four specific user populations in ways that would prevent successful installation:

1. **The Confused Newcomer** fails at Step 1 of the primary install path (RT-003: no instruction on where to enter Claude Code commands). This is the highest-severity finding — it is a complete blocker for the audience the document most needs to serve.

2. **The Corporate IT Admin** cannot approve the installation for their organization (RT-008: no network requirements) and cannot assess the hook security model (RT-010). Both are blocking conditions for enterprise adoption.

3. **The Windows Developer** will set up `JERRY_PROJECT` persistence incorrectly (RT-012: wrong PowerShell scope) and cannot determine which hooks work on their platform (RT-016). Both will result in hours of debugging that proper documentation would prevent.

4. **The Impatient Expert** will hit the "plugin not found" failure mode and will not find the recovery command immediately (RT-018), and will encounter the `JERRY_PROJECT` launch-dependency confusion (RT-020).

**Priority remediation path:** Address RT-003 and RT-008 (P0 Critical) first — these block entire user categories. Then address the Windows persistence bug (RT-012) and the IT admin hook documentation (RT-010), as these affect the accuracy of existing instructions rather than adding new content.

---

## Execution Statistics

- **Total Findings:** 20
- **Critical:** 2 (RT-003, RT-008)
- **Major:** 12 (RT-001, RT-002, RT-004, RT-005, RT-007, RT-009, RT-010, RT-012, RT-013, RT-014, RT-016, RT-018, RT-020)
- **Minor:** 6 (RT-006, RT-011, RT-015, RT-017, RT-019)
- **Protocol Steps Completed:** 5 of 5
- **Personas Evaluated:** 4 of 4
- **Attack Vector Categories Used:** Ambiguity, Boundary, Circumvention, Dependency, Degradation (all 5)

---

*Report generated by adv-executor | Strategy: S-001 Red Team Analysis v1.0.0*
*Template: `.context/templates/adversarial/s-001-red-team.md`*
*Deliverable: `docs/INSTALLATION.md`*
*Date: 2026-02-25*

# Red Team Report: INSTALLATION.md (Iteration 2)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `docs/INSTALLATION.md` — Jerry Framework Installation Guide (Revised 2026-02-25, Iteration 2)
**Criticality:** C4 (public-facing OSS documentation, irreversible first-impression surface)
**Date:** 2026-02-25
**Reviewer:** adv-executor (S-001 Red Team Analysis v1.0.0)
**H-16 Compliance:** S-003 Steelman not confirmed as a prior step. Execution proceeds at user direction (iteration 2 of C4 adversarial tournament). H-16 advisory documented; same waiver applies as iteration 1.
**Prior Iteration:** `docs/reviews/iteration-1-s001-red-team.md` (2026-02-25) — 20 findings (2 Critical, 12 Major, 6 Minor)
**Threat Actors:** Four personas (identical to iteration 1 — same deliverable, same audience)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Iteration Delta: Closed Findings](#iteration-delta-closed-findings) | What the revision fixed |
| [Iteration Delta: Remaining Findings](#iteration-delta-remaining-findings) | What the revision did not address |
| [Step 1: Threat Actor Profiles](#step-1-threat-actor-profiles) | Four adversarial personas (carried forward) |
| [Step 2: Attack Vector Inventory](#step-2-attack-vector-inventory) | Remaining + new vectors with RT-NNN-i2 identifiers |
| [Step 3: Defense Gap Assessment](#step-3-defense-gap-assessment) | Defense status for all open vectors |
| [Step 4: Countermeasures](#step-4-countermeasures) | Specific remediation actions — P0 and P1 |
| [Step 5: Findings Summary](#step-5-findings-summary) | Consolidated summary table |
| [Detailed Findings](#detailed-findings) | Full detail for Critical and Major findings |
| [Scoring Impact](#scoring-impact) | S-014 dimension impact mapping |
| [Overall Assessment](#overall-assessment) | Recommendation and path forward |

---

## Iteration Delta: Closed Findings

The following iteration-1 findings are confirmed CLOSED in the revised document:

| ID | Original Finding | Evidence of Closure |
|----|-----------------|---------------------|
| RT-002-20260225 | SSH "Required" creates stop point before HTTPS alternative visible | Prerequisites table now reads: "SSH key configured for GitHub \| **No** — [HTTPS alternative available](#install-from-github)" (line 39). Reader is not told SSH is required. |
| RT-004-20260225 | "Which Install Method?" requires self-knowledge newcomer lacks | Which Install Method? section now has 4 rows (SSH, no-SSH, offline, session-only) with an explicit self-diagnosis tip: "Not sure if you have SSH configured? Run `ssh -T git@github.com`..." (line 61). |
| RT-018-20260225 | "Plugin not found" recovery not surfaced inline at Step 2 | Step 2 is now "Verify the source registered" — a proactive `/plugin marketplace list` step before install (lines 86-94). Users confirm the source name before running Step 3. |

**3 of 20 findings closed. 17 remain open.**

---

## Iteration Delta: Remaining Findings

The following iteration-1 findings are confirmed OPEN in the revised document. Evidence references the current text.

| ID | Original Severity | Status | Evidence of Continued Gap |
|----|------------------|--------|--------------------------|
| RT-001-20260225 | Major | Open | No orientation on what interface Claude Code is (terminal vs chat app) before first slash command |
| RT-003-20260225 | **Critical** | Open | No text explaining where slash commands are entered in Claude Code anywhere in the document |
| RT-005-20260225 | Major | Open | Configuration step 4 says "run from your repository root" — no guidance for newcomers without an existing repo |
| RT-006-20260225 | Minor | Open | "Start a new Claude Code session" undefined |
| RT-007-20260225 | Major | Open | uv installer security note describes HOW to inspect but not WHAT the installer does systemically |
| RT-008-20260225 | **Critical** | Open | No network requirements section; domains (`github.com`, `astral.sh`) not listed as prerequisites |
| RT-009-20260225 | Major | Open | No air-gap or fully-blocked-network path; Local Clone method still requires `github.com` access |
| RT-010-20260225 | Major | Open | Hook execution model (uv invocation, CLAUDE_PLUGIN_ROOT, file-system permissions) not documented |
| RT-011-20260225 | Minor | Open | No hash/checksum for uv install script integrity verification |
| RT-012-20260225 | **Major** | Open | Windows persistence still uses `Set-Variable -Scope Global` (line 333) — not a proper environment variable |
| RT-013-20260225 | Major | Open | No step to verify JERRY_PROJECT is visible to Claude Code before launching it |
| RT-014-20260225 | Major | Open | No Windows-specific hook troubleshooting subsection |
| RT-015-20260225 | Minor | Open | uv binary path after Windows install unspecified; PATH fix listed without prior verification command |
| RT-016-20260225 | Major | Open | Platform Note does not specify which hooks are affected by Windows symlink limitation |
| RT-017-20260225 | Minor | Open | No TL;DR / Quick Install block for expert users |
| RT-019-20260225 | Minor | Open | "Run from your repo root" underspecified for multi-repo contexts |
| RT-020-20260225 | Major | Open | No statement that JERRY_PROJECT must be set before Claude Code is launched |

---

## Step 1: Threat Actor Profiles

*Carried forward from iteration 1. The same four personas apply — same document, same audience.*

### Persona A: The Confused Newcomer

| Field | Value |
|-------|-------|
| **Goal** | Complete installation without knowing what Claude Code is, what SSH is, or what a "marketplace" means — survival goal: not feel stupid, succeed on first try |
| **Capability** | Basic Git, GitHub account, macOS assumed, can follow numbered steps if unambiguous |
| **Knowledge Gaps** | No SSH keys, has never heard of `uv`, doesn't know where to type commands inside Claude Code |
| **Motivation** | Heard about Jerry; will abandon if two consecutive steps fail without explanation |

### Persona B: The Corporate IT Admin

| Field | Value |
|-------|-------|
| **Goal** | Approve Jerry for team use; justify every tool, script execution, and network call to security |
| **Capability** | Deep IT knowledge; controls proxy, firewall, endpoint policy; skeptical of pipe-to-sh patterns |
| **Knowledge Gaps** | Not a developer; unfamiliar with Claude Code plugin system |
| **Motivation** | Developers requested Jerry; IT is gatekeeping; needs to assess security posture |

### Persona C: The Windows Developer

| Field | Value |
|-------|-------|
| **Goal** | Full installation including hooks on Windows; PowerShell as primary shell |
| **Capability** | Expert Windows/PowerShell; Git; Claude Code on Windows |
| **Knowledge Gaps** | Unfamiliar with macOS conventions; doesn't know if Windows edge cases are handled |
| **Motivation** | Wants to use Jerry on their primary development machine |

### Persona D: The Impatient Expert

| Field | Value |
|-------|-------|
| **Goal** | Install Jerry in under 60 seconds; will skim the document |
| **Capability** | Senior developer; fluent with SSH, git, uv, Claude Code |
| **Knowledge Gaps** | None technically — but impatience causes them to skip prose and context |
| **Motivation** | Quick evaluation; wants commands, not paragraphs |

---

## Step 2: Attack Vector Inventory

*Iteration-2 execution IDs use suffix `-i2` to distinguish from iteration-1 findings. Carried-forward findings retain their original IDs for traceability. New findings introduced in this iteration use new IDs.*

### Persona A: Confused Newcomer

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-003-20260225 | No instruction anywhere in the document on how to enter slash commands in Claude Code — newcomer opens the app and cannot find where to type `/plugin marketplace add` | Ambiguity | High | **Critical** | P0 | Missing | Completeness |
| RT-001-20260225 | No orientation on what Claude Code is as an interface (terminal vs chat app vs IDE extension) before first slash command — newcomer may try typing in a terminal window | Ambiguity | High | Major | P1 | Partial | Completeness |
| RT-005-20260225 | Configuration step 4 (`mkdir projects/...`) says "run from your repository root" — newcomer installing for the first time may not have an existing repository to run this from | Ambiguity | Medium | Major | P1 | Partial | Completeness |
| RT-006-20260225 | Hooks verification says "start a new Claude Code session" — undefined; newcomer may not know this means close and reopen the application | Ambiguity | Medium | Minor | P2 | Missing | Actionability |
| RT-N1-i2 | The "Which Install Method?" table now has 4 rows and a self-diagnosis SSH tip, but the "Not sure?" tip below the table refers to "use the HTTPS path" — a newcomer with no SSH who reads only the table row ("Internet access, no SSH key — or you're not sure") is routed to "Install from GitHub (HTTPS)" but the section is titled "Install from GitHub" with no HTTPS designation in the section header, creating a disconnect when they arrive at the section | Ambiguity | Medium | Minor | P2 | Partial | Internal Consistency |

### Persona B: Corporate IT Admin

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-008-20260225 | No network requirements section — `github.com` and `astral.sh` are required outbound domains that cannot be derived from Prerequisites | Dependency | High | **Critical** | P0 | Missing | Completeness |
| RT-007-20260225 | uv installer security note explains HOW to inspect the script but not WHAT it installs — no description of target directories, privilege requirements, or system modifications | Dependency | High | Major | P1 | Partial | Evidence Quality |
| RT-009-20260225 | No fully-air-gapped or enterprise-proxy installation path — Local Clone still requires `github.com` access; fully-blocked networks have no documented route | Boundary | High | Major | P1 | Missing | Completeness |
| RT-010-20260225 | Hook execution model undocumented — no description of how hooks invoke uv, what `CLAUDE_PLUGIN_ROOT` resolves to, what file-system permissions are needed, or whether hooks require network access | Dependency | Medium | Major | P1 | Missing | Evidence Quality |
| RT-011-20260225 | No hash/checksum for uv installer — inspect-then-run guidance protects against script content but not supply-chain substitution between download and inspection | Dependency | Low | Minor | P2 | Missing | Methodological Rigor |
| RT-N2-i2 | The Install from GitHub section now describes Jerry as a "community Claude Code plugin" and explicitly names the "official Anthropic marketplace" as separate. However, the troubleshooting entry for "Plugin source add fails (non-SSH error)" says "Corporate proxy/firewall — if your network restricts GitHub access, use the Local Clone instead" — this does not name the alternative domain (`raw.githubusercontent.com` or equivalent) that the Local Clone itself uses, leaving the IT admin unable to determine if Local Clone's network surface is smaller or just different | Ambiguity | Medium | Minor | P2 | Partial | Completeness |

### Persona C: Windows Developer

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-012-20260225 | Windows JERRY_PROJECT persistence in Configuration step 3 still uses `Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global` — a PowerShell session variable that does not propagate to child processes including Claude Code | Ambiguity | High | Major | P1 | Missing | Internal Consistency |
| RT-013-20260225 | No verification step to confirm that JERRY_PROJECT is visible in Claude Code's environment before launching it — Windows users will follow the persistence step, launch Claude Code, and hit `<project-required>` with no diagnostic guidance | Dependency | High | Major | P1 | Missing | Completeness |
| RT-014-20260225 | No Windows-specific hook troubleshooting subsection — Windows users whose hooks fail silently have no Windows-specific diagnostic checklist | Boundary | High | Major | P1 | Partial | Completeness |
| RT-016-20260225 | Platform Note warns that "hooks that use symlinks or path-sensitive operations may behave differently" but does not name which specific hooks are affected — Windows developer cannot map this to the Capability Matrix rows | Ambiguity | High | Major | P1 | Partial | Completeness |
| RT-015-20260225 | uv binary PATH fix on Windows specifies `%USERPROFILE%\.local\bin` but no verification command is given first to determine where uv was actually installed | Ambiguity | Medium | Minor | P2 | Missing | Actionability |

### Persona D: Impatient Expert

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-020-20260225 | No explicit statement that JERRY_PROJECT must be set before Claude Code is launched — expert sets variable in one terminal, Claude Code already open in another, gets `<project-required>` with no obvious cause | Dependency | Medium | Major | P1 | Partial | Completeness |
| RT-017-20260225 | No TL;DR / Quick Install block at the top — expert who skims must read through two prose paragraphs before reaching the first copyable command | Degradation | High | Minor | P2 | Missing | Actionability |
| RT-019-20260225 | "Run from your repository root" underspecified for experts with multiple repos open simultaneously | Ambiguity | Medium | Minor | P2 | Partial | Actionability |
| RT-N3-i2 | The proactive Step 2 ("Verify the source registered") now shows `/plugin marketplace list` before install — but it also adds a `> **Shortcut:** You can also type /plugin market list` tip. An expert who reads only the shortcut and skips the explanation will not know that the output naming matters for the install command — the shortcut tip does not mention that the listed source name is what goes into the `@suffix` of the next command | Ambiguity | Medium | Minor | P2 | Partial | Actionability |

---

## Step 3: Defense Gap Assessment

| ID | Existing Defense | Classification | Adversary Exploitation Path |
|----|-----------------|----------------|----------------------------|
| RT-003-20260225 | None — document never explains where slash commands are entered | **Missing** | Newcomer types `/plugin marketplace add` in their system terminal, gets "command not found", concludes the product is broken |
| RT-001-20260225 | "Don't have Claude Code yet?" blockquote mentions quickstart | Partial | Blockquote is positioned before Step 1 but does not orient the user to Claude Code's chat interface; newcomer knows Claude Code exists but not how its UI is structured |
| RT-005-20260225 | "Run from your repository root" note | Partial | Note is present; newcomer with no existing repo is not addressed |
| RT-006-20260225 | None | Missing | Minor impact; most users discover this intuitively |
| RT-N1-i2 | 4-row decision table routes user to correct section | Partial | Section header mismatch creates mild confusion; low-severity because the HTTPS path works once found |
| RT-008-20260225 | Troubleshooting mentions "Corporate proxy/firewall — use Local Clone" reactively | **Missing** | IT admin cannot construct an outbound domain allowlist; installation is blocked at corporate firewall without pre-authorization |
| RT-007-20260225 | Security note with inspect-then-run guidance | Partial | HOW to inspect is documented; WHAT the installer does is not; IT admin cannot write security assessment from the doc alone |
| RT-009-20260225 | Local Clone method documented | Partial | Local Clone still requires `github.com` access; fully-blocked networks have no path |
| RT-010-20260225 | None | **Missing** | Security review of hook execution model cannot be completed from documentation alone |
| RT-011-20260225 | Inspect guidance | Partial | No integrity verification available |
| RT-N2-i2 | Troubleshooting entry for corporate proxy | Partial | Alternative domain for Local Clone not named; IT admin's allowlist remains incomplete |
| RT-012-20260225 | Windows PowerShell command provided | **Missing** | `Set-Variable -Scope Global` is still present (line 333). The in-step variable set on line 319 uses `$env:JERRY_PROJECT` correctly, but the persistence command (line 333) uses the wrong syntax. Windows user's profile will set a session variable, not an environment variable — Claude Code will not inherit it |
| RT-013-20260225 | None | **Missing** | User follows persistence step, launches Claude Code from a different session, and cannot understand why `<project-required>` appears even though "the variable is set" |
| RT-014-20260225 | "Hit a wall? File it" reference | Partial | No Windows-specific hook checklist; developer must file an issue to learn what they could have learned from the docs |
| RT-016-20260225 | Platform Note warns generically about symlink-sensitive hooks | Partial | No mapping from warning to specific Capability Matrix rows; Windows developer cannot determine which enforcement layers are unreliable |
| RT-015-20260225 | PATH fix listed | Partial | No verification step before fix; path may differ from documented location |
| RT-020-20260225 | Profile persistence step documented | Partial | No statement that Claude Code must be launched from a session where the variable is already present |
| RT-017-20260225 | Table of Contents and 4-row decision table help | Partial | No TL;DR block; expert still reads prose before reaching first command |
| RT-019-20260225 | "Run from repo root" present | Partial | Not specific enough for multi-repo contexts |
| RT-N3-i2 | Step 2 now proactively shows `/plugin marketplace list` | Partial | Shortcut tip does not explain why the listed name matters; experts who rely on shortcut syntax may miss the connection to Step 3 |

---

## Step 4: Countermeasures

### P0 — Critical: MUST address before acceptance

**RT-003-20260225: No instruction on how to enter slash commands in Claude Code**

*Carried forward from iteration 1, P0 — not addressed in revision.*

Countermeasure: Add a one-sentence orientation immediately before Step 1 of "Install from GitHub": "Slash commands like `/plugin` are typed into Claude Code's chat input window — the same place you send messages to the AI. Type the command and press Enter."

Acceptance Criteria: A user who has installed Claude Code but has never used a slash command can locate the input area and execute Step 1 without consulting external documentation.

---

**RT-008-20260225: No network access requirements documented**

*Carried forward from iteration 1, P0 — not addressed in revision.*

Countermeasure: Add a "Network Requirements" row group to the Prerequisites table (or a dedicated callout box immediately after the Software table). Content must list: `github.com` (required for GitHub install method and Local Clone), `astral.sh` (required if installing uv), and note that the Session Install method requires only `github.com`. Mark which method each domain is required for. Note that the Local Clone method used from an already-cloned repo eliminates the `github.com` dependency at install time.

Acceptance Criteria: A corporate IT admin can derive the complete outbound domain allowlist from the Prerequisites section without reading the rest of the document.

---

### P1 — Important: SHOULD address

**RT-012-20260225: Windows JERRY_PROJECT persistence uses wrong PowerShell scope (BUG — still present)**

*Carried forward from iteration 1, P1 — NOT fixed in revision despite being listed as a bug. Severity escalated to P0-adjacent given confirmed persistence.*

The in-step variable set (Configuration step 2, line 319) correctly uses `$env:JERRY_PROJECT = "PROJ-001-my-project"`. However, the persistence command (Configuration step 3, line 333) still reads:

```
Add-Content $PROFILE 'Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global'
```

This is wrong. `Set-Variable -Scope Global` sets a PowerShell session variable, not an environment variable. Child processes (including Claude Code) cannot read PowerShell session variables.

Countermeasure: Replace line 333 with:
```
Add-Content $PROFILE '$env:JERRY_PROJECT = "PROJ-001-my-project"'
```

Acceptance Criteria: After following the Windows persistence step and opening a new PowerShell session, `echo $env:JERRY_PROJECT` returns the project ID, and Claude Code launched from that session receives `JERRY_PROJECT` in its environment.

---

**RT-007-20260225: uv installer security note describes HOW but not WHAT**

Countermeasure: Add one paragraph immediately after the existing security note: "What the installer does: downloads the uv binary for your platform (macOS/Linux: `~/.local/bin/uv`; Windows: `~/.local\bin\uv.exe`), appends a PATH export to your shell profile (`~/.zshrc`, `~/.bashrc`, or PowerShell profile), and makes no other system modifications. Root/administrator privileges are not required. No network calls occur after initial download."

Acceptance Criteria: An IT admin reading the uv security note can describe the installer's system impact in a security review without executing or reading the install script.

---

**RT-009-20260225: No air-gap or fully-blocked-network path**

Countermeasure: Add a note at the end of the Local Clone section: "Fully air-gapped environment (github.com blocked entirely): (1) clone the repository from a machine with GitHub access, (2) transfer the directory to the restricted machine via your organization's approved file transfer mechanism, (3) proceed from 'Add as a local plugin source' using the local path. Note: uv installation also requires network access to `astral.sh`; for air-gapped uv installation, download a specific uv release binary from [GitHub releases](https://github.com/astral-sh/uv/releases) and place it in `~/.local/bin/` manually."

Acceptance Criteria: A user in a fully air-gapped environment has a documented (if manual) path to complete installation.

---

**RT-010-20260225: Hook execution model and permissions not documented**

Countermeasure: Add a "How hooks work" technical callout under Enable Hooks: "Jerry's hooks are Python scripts executed by Claude Code using the uv binary. When a hook fires, Claude Code runs `uv run --directory {CLAUDE_PLUGIN_ROOT} jerry {hook-name}`. The scripts read and write files in your project directory (`projects/{JERRY_PROJECT}/`) and the Jerry plugin directory. No network access is required at hook execution time. No elevated privileges are required."

Acceptance Criteria: An IT admin can describe the runtime behavior of Jerry's hooks in a security assessment without reading the Jerry codebase.

---

**RT-013-20260225: No verification that JERRY_PROJECT reaches Claude Code**

Countermeasure: Add a verification sub-step to Configuration step 3: "To verify the variable will be visible to Claude Code: open a NEW terminal session (which loads the updated profile), then run `echo $JERRY_PROJECT` (macOS/Linux) or `echo $env:JERRY_PROJECT` (Windows). If this prints your project ID, the variable is configured correctly. If empty, the profile update did not take effect — check that you saved the file and are using the correct shell."

Acceptance Criteria: A user can verify `JERRY_PROJECT` is correctly propagated before starting Claude Code, and knows what "empty" output means.

---

**RT-014-20260225: No Windows-specific hook troubleshooting**

Countermeasure: Add a "Hooks not firing on Windows" subsection in Troubleshooting: "If hooks are not firing on Windows after installing uv: (1) verify `uv --version` works in the terminal you use to launch Claude Code; (2) verify `CLAUDE_PLUGIN_ROOT` resolves to a path without spaces; (3) verify your Claude Code plugin directory path does not use backslashes — Claude Code requires forward slashes on Windows; (4) check [GitHub Issues tagged `hooks`](https://github.com/geekatron/jerry/issues?q=label%3Ahooks) for current Windows hook status — some hooks use symlink operations that require Windows Developer Mode."

Acceptance Criteria: A Windows user experiencing hook failures has a Windows-specific diagnostic checklist without needing to file an issue first.

---

**RT-016-20260225: Platform Note does not specify which hooks are affected by Windows symlinks**

Countermeasure: Expand the Platform Note: add "Known Windows hook limitations: `[specific hook names]` use symlink operations and require Windows Developer Mode or will use junction points instead; `[other hook names]` are unaffected on Windows." If the specific list is not yet fully characterized, add: "See [GitHub Issues tagged `windows-hooks`](https://github.com/geekatron/jerry/issues?q=label%3Awindows-hooks) for current Windows hook status by hook name."

Acceptance Criteria: A Windows developer can cross-reference the Capability Matrix rows to determine which features require Windows Developer Mode.

---

**RT-020-20260225: JERRY_PROJECT must be set before Claude Code launch — not stated**

Countermeasure: Add to the end of Configuration step 2 and to the Verification — Hooks section: "Claude Code inherits environment variables from the terminal session it was launched from. Set `JERRY_PROJECT` first, then launch Claude Code from that terminal. If Claude Code is already running, restart it from a terminal where the variable is set."

Acceptance Criteria: A user who sets `JERRY_PROJECT` in one terminal and gets `<project-required>` in an already-running Claude Code session understands the launch-dependency and knows to restart Claude Code.

---

**RT-001-20260225: No orientation on Claude Code as a chat interface before first slash command**

Countermeasure: Add a one-sentence context note at the top of the "Install from GitHub" section: "Claude Code is an AI chat interface — its `/plugin` commands are entered in the chat input window, not your system terminal."

Acceptance Criteria: A first-time Claude Code user knows to look for a chat input area, not a separate terminal, before attempting Step 1.

---

**RT-005-20260225: mkdir "from repo root" — newcomer may have no repo**

Countermeasure: Add a note to Configuration step 4: "Don't have a repository yet? Jerry can live in any directory you want to work in — create a new directory with `mkdir my-project && cd my-project`, then run `git init` to make it a Git repository, then run the `mkdir` command above. Jerry doesn't require an existing codebase — any directory works."

Acceptance Criteria: A newcomer without an existing Git repository can complete Configuration step 4 without confusion about what "your repository root" means.

---

### P2 — Monitor

**RT-006-20260225 (Minor):** Add "Close and reopen Claude Code completely" to the hooks verification step to clarify "start a new session."

**RT-011-20260225 (Minor):** Link to uv's published release checksums for users requiring installer integrity verification before execution.

**RT-015-20260225 (Minor):** Add `uv --version` as the canonical verification step before the manual PATH fix on Windows.

**RT-017-20260225 (Minor):** A Quick Install block (3 commands, no prose) at the top of the document would serve expert users — place after the nav table, before Prerequisites.

**RT-019-20260225 (Minor):** Strengthen "run from your repo root" to: "from the root of the specific repository where you plan to use Jerry."

**RT-N1-i2 (Minor):** Align the "Install from GitHub (HTTPS)" routing label in the decision table with the actual section heading "Install from GitHub" to avoid confusion when the user arrives at the section.

**RT-N2-i2 (Minor):** In the "Plugin source add fails" troubleshooting entry, name the specific domains needed for Local Clone so IT can construct a minimal allowlist for that path.

**RT-N3-i2 (Minor):** In the `/plugin market list` shortcut tip (Step 2), add: "The source name in the output is what you'll use in Step 3's `@suffix`." This closes the shortcut-to-install-step connection for expert users.

---

## Step 5: Findings Summary

| ID | Persona | Attack Vector (short) | Category | Exploit | Severity | Priority | Defense | Status |
|----|---------|----------------------|----------|---------|----------|----------|---------|--------|
| RT-003-20260225 | Newcomer | No instruction on where to enter slash commands | Ambiguity | High | **Critical** | P0 | Missing | Open (not fixed) |
| RT-008-20260225 | IT Admin | No network access requirements | Dependency | High | **Critical** | P0 | Missing | Open (not fixed) |
| RT-001-20260225 | Newcomer | No Claude Code interface orientation before first command | Ambiguity | High | Major | P1 | Partial | Open |
| RT-005-20260225 | Newcomer | mkdir "from repo root" — no existing repo scenario | Ambiguity | Medium | Major | P1 | Partial | Open |
| RT-007-20260225 | IT Admin | uv installer describes HOW to review but not WHAT it does | Dependency | High | Major | P1 | Partial | Open |
| RT-009-20260225 | IT Admin | No air-gap / fully-blocked network path | Boundary | High | Major | P1 | Missing | Open |
| RT-010-20260225 | IT Admin | Hook execution model undocumented | Dependency | Medium | Major | P1 | Missing | Open |
| RT-012-20260225 | Windows | JERRY_PROJECT persistence uses wrong PowerShell scope (BUG) | Ambiguity | High | Major | P1 | Missing | Open — BUG PERSISTS |
| RT-013-20260225 | Windows | No verification that JERRY_PROJECT reaches Claude Code | Dependency | High | Major | P1 | Missing | Open |
| RT-014-20260225 | Windows | No Windows-specific hook troubleshooting | Boundary | High | Major | P1 | Partial | Open |
| RT-016-20260225 | Windows | Which hooks are affected by Windows symlinks — not listed | Ambiguity | High | Major | P1 | Partial | Open |
| RT-020-20260225 | Expert | JERRY_PROJECT must be set before launch — not stated | Dependency | Medium | Major | P1 | Partial | Open |
| RT-006-20260225 | Newcomer | "Start a new Claude Code session" undefined | Ambiguity | Medium | Minor | P2 | Missing | Open |
| RT-011-20260225 | IT Admin | No hash/checksum for uv install script | Dependency | Low | Minor | P2 | Missing | Open |
| RT-015-20260225 | Windows | uv binary PATH fix given without prior verification | Ambiguity | Medium | Minor | P2 | Missing | Open |
| RT-017-20260225 | Expert | No TL;DR / Quick Install block | Degradation | High | Minor | P2 | Missing | Open |
| RT-019-20260225 | Expert | "Repo root" underspecified in multi-repo contexts | Ambiguity | Medium | Minor | P2 | Partial | Open |
| RT-N1-i2 | Newcomer | "Install from GitHub (HTTPS)" row doesn't match section title | Ambiguity | Medium | Minor | P2 | Partial | New |
| RT-N2-i2 | IT Admin | Local Clone alternative domain not named for corporate proxy case | Ambiguity | Medium | Minor | P2 | Partial | New |
| RT-N3-i2 | Expert | Shortcut tip for `/plugin market list` doesn't connect to Step 3 | Ambiguity | Medium | Minor | P2 | Partial | New |

**Totals: 2 Critical (P0), 10 Major (P1), 8 Minor (P2)**

*Iteration 1 totals: 2 Critical, 12 Major, 6 Minor. Net change: 0 Critical (same), -2 Major (2 closed: RT-002, RT-018 closed; RT-004 closed; minor category: RT-004 was Major in iteration 1 and counted in Major), +2 Minor (3 new findings, all Minor). Progress: 3 findings closed, 3 new (all Minor) identified.*

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
| **Priority** | P0 |
| **Defense** | Missing |
| **Iteration Status** | Not addressed in revision — finding persists unchanged |

**Attack Vector:** The entire "Install from GitHub" section instructs users to "run" slash commands in "Claude Code" without explaining where. A user who has just installed Claude Code for the first time opens the application and encounters:

> "In Claude Code, run: `/plugin marketplace add geekatron/jerry`"

They have no prior knowledge of where to type this. Claude Code presents a chat interface, possibly a terminal panel, and other surfaces depending on OS and version. Nothing in the document — not in Prerequisites, not in the intro, not adjacent to Step 1 — explains that slash commands are entered in Claude Code's chat input window.

**Evidence from deliverable:**
- Step 1 (lines 73-84): "In Claude Code, run: `/plugin marketplace add geekatron/jerry` ... /plugin marketplace add https://github.com/geekatron/jerry.git"
- Prerequisites (lines 34-47): Mentions Claude Code version requirements and a "Don't have Claude Code yet?" blockquote. No interface orientation.
- The revision did not add any slash-command orientation text. A Grep for "slash command", "chat window", "message input", "where to enter", and "where to type" returned zero matches.

**Consequence:** A newcomer cannot complete Step 1. They will: (1) type the command in their system terminal (getting "command not found"), (2) search for a separate Claude Code CLI, or (3) abandon installation. This is a complete blocker for the primary audience this document must serve.

**Countermeasure:** One sentence before Step 1: "Slash commands like `/plugin` are typed into Claude Code's chat input window — the same place you send messages to the AI. Type the command and press Enter."

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
| **Priority** | P0 |
| **Defense** | Missing |
| **Iteration Status** | Not addressed in revision — finding persists unchanged |

**Attack Vector:** A corporate IT admin reviewing Jerry for team use cannot find required outbound network connections anywhere in the document. The installation silently requires:

- `github.com` — plugin source clone (Step 1 of GitHub install, Local Clone)
- `astral.sh` — uv installer (Enable Hooks section)
- `raw.githubusercontent.com` — potentially for Claude Code plugin source fetching

The only network-related content is: (1) a troubleshooting entry "Corporate proxy/firewall — if your network restricts GitHub access, use the Local Clone" (reactive, no domain names), and (2) the Local Clone method which still requires `github.com`.

**Evidence from deliverable:**
- Prerequisites table (lines 36-40): lists only Software requirements; no network requirements.
- Troubleshooting "Plugin source add fails" (line 510): "Corporate proxy/firewall — if your network restricts GitHub access, use the Local Clone method instead." No domain names listed.
- A Grep for "Network", "domain", "allowlist", "outbound" returned only the `astral.sh` URL inline in code blocks and a single troubleshooting mention — none in Prerequisites.

**Consequence:** IT admin cannot pre-authorize domains. Installation fails at whichever step hits the first blocked domain. IT admin cannot complete security review without reverse-engineering network requirements via test install on a monitored machine — high-friction process that frequently results in tool rejection.

**Countermeasure:** Add a "Network Requirements" section to Prerequisites listing: `github.com` (plugin install, Local Clone), `astral.sh` (uv installer — skip if uv already installed), with per-method column. Note that Session Install reduces to `github.com` only, and air-gapped installs eliminate `github.com` after initial clone.

**Acceptance Criteria:** IT admin can derive complete outbound domain allowlist from Prerequisites without reading the full document.

---

### RT-012-20260225: Windows JERRY_PROJECT Persistence Uses Wrong PowerShell Scope [MAJOR — BUG PERSISTS]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Windows Developer |
| **Section** | Configuration — Step 3 |
| **Category** | Ambiguity |
| **Exploitability** | High |
| **Priority** | P1 |
| **Defense** | Missing |
| **Iteration Status** | NOT fixed in revision — confirmed by direct evidence |

**Attack Vector:** Configuration step 3, Windows persistence command (line 333):

```powershell
Add-Content $PROFILE 'Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global'
```

`Set-Variable -Scope Global` sets a PowerShell-scoped variable, not a Windows environment variable. Consequences:

1. The variable is NOT visible as `$env:JERRY_PROJECT` — it exists as `$JERRY_PROJECT` only within PowerShell sessions
2. Claude Code, launched as a child process, reads environment variables — not PowerShell session variables
3. Windows users following this step will permanently see `<project-required>` when starting Claude Code

Note: Configuration step 2 (line 319) correctly uses `$env:JERRY_PROJECT = "PROJ-001-my-project"` for the immediate in-session set. The inconsistency between the correct step-2 syntax and the broken step-3 persistence syntax is what makes this particularly confusing — the variable appears to be "set" in the current session (step 2 works) but disappears in new Claude Code sessions (step 3 persists the wrong thing).

**Evidence from deliverable (lines 330-334):**
```
   # Windows PowerShell — create profile if needed, then add
   if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -Force }
   Add-Content $PROFILE 'Set-Variable -Name JERRY_PROJECT -Value "PROJ-001-my-project" -Scope Global'
```

The iteration-1 report identified this exact bug. The iteration-2 revision did not fix it.

**Countermeasure (specific code change required):**

Replace line 333 with:
```powershell
Add-Content $PROFILE '$env:JERRY_PROJECT = "PROJ-001-my-project"'
```

**Acceptance Criteria:** After following the Windows persistence step and opening a new PowerShell session, `echo $env:JERRY_PROJECT` returns the project ID, and Claude Code launched from that session recognizes the project without `<project-required>`.

---

### RT-016-20260225: Platform Note Does Not Specify Which Hooks Are Affected by Windows Symlinks [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Windows Developer |
| **Section** | Platform Note (document header) and Enable Hooks |
| **Category** | Ambiguity |
| **Exploitability** | High |
| **Priority** | P1 |
| **Defense** | Partial |
| **Iteration Status** | Not addressed in revision |

**Attack Vector:** The Platform Note (line 5) warns that "hooks that use symlinks or path-sensitive operations may behave differently" on Windows. The Enable Hooks section lists 6 hooks in a capability table (SessionStart, UserPromptSubmit, PreCompact, PreToolUse, SubagentStop, Stop). The Capability Matrix (lines 194-207) lists capabilities enabled by each hook. Neither table includes a Windows column or hook-specific Windows annotations.

A Windows developer installing Jerry cannot determine:
- Which hooks will work correctly on Windows
- Which hooks will silently fail vs. visibly error
- Which Capability Matrix rows they will actually receive on their platform

**Evidence from deliverable:**
- Line 5: "hooks that use symlinks or path-sensitive operations may behave differently"
- Hooks table (lines 155-162): 6 hooks with descriptions, no Windows column
- Capability Matrix (lines 195-207): feature list with yes/no, no platform dimension
- No grep match for "which hook", "hook.*Windows", "Windows.*hook" at any detail level

**Consequence:** Windows users run for weeks or months under the impression that specific enforcement layers are active when they are silently failing. The "early access caveat" in the Enable Hooks section does note that some hooks fail silently, but this is platform-agnostic — the Windows-specific failure modes are not named.

**Countermeasure:** Add Windows status to the hooks table. At minimum, note which hooks require Developer Mode for symlink support. If complete information is unavailable, add a link to a tracked GitHub Issue for Windows hook status.

**Acceptance Criteria:** A Windows developer can determine, from the Enable Hooks section, which of the 6 hooks are expected to function on their platform.

---

### RT-007-20260225: uv Installer Security Note Describes HOW but Not WHAT [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Corporate IT Admin |
| **Section** | Enable Hooks — Install uv — Security Note |
| **Category** | Dependency |
| **Exploitability** | High |
| **Priority** | P1 |
| **Defense** | Partial |
| **Iteration Status** | Not addressed in revision |

**Attack Vector:** The security note (line 166) provides a mechanism to download and inspect the install script before execution. It does not describe what the script does: target directories, whether it requires root/admin, whether it modifies system PATH or shell profile, what it leaves behind. For a corporate security review, this is the information that enables or blocks approval.

**Evidence from deliverable (line 166):**
> "If your organization requires script inspection before execution: on macOS/Linux, download first with `curl -LsSf https://astral.sh/uv/install.sh -o install-uv.sh`, review it, then run `sh install-uv.sh`; on Windows, download first with `Invoke-WebRequest https://astral.sh/uv/install.ps1 -OutFile install-uv.ps1`, review it, then run `.\install-uv.ps1`. Alternatively, install via [pip](https://docs.astral.sh/uv/getting-started/installation/#pip) or your system package manager."

No "What this installs" description follows. IT admin must read the script to answer "does this require root?" and "what does it write to disk?".

**Countermeasure:** Add one paragraph below the security note: "What the installer does: downloads the uv binary to `~/.local/bin/uv` (macOS/Linux) or `~/.local\bin\uv.exe` (Windows), and appends a PATH export to your shell profile. It does not require root or administrator privileges, makes no system-wide changes, and does not install Python (uv manages Python internally). No other files are created."

**Acceptance Criteria:** IT admin can write a security scope description for the uv installer from the documentation alone, without reading or executing the install script.

---

### RT-009-20260225: No Air-Gap or Fully-Blocked-Network Installation Path [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Corporate IT Admin |
| **Section** | Local Clone |
| **Category** | Boundary |
| **Exploitability** | High |
| **Priority** | P1 |
| **Defense** | Partial |
| **Iteration Status** | Not addressed in revision |

**Attack Vector:** The "Which Install Method?" routing table identifies "Offline or network-restricted" users and routes them to Local Clone. However, Local Clone's Step 1 requires `git clone https://github.com/geekatron/jerry.git` — still requiring `github.com` access. For users in a fully air-gapped environment (no outbound access whatsoever), there is no documented path to obtain Jerry's files.

**Evidence from deliverable:**
- Which Install Method table (line 58): routes "Offline or network-restricted" users to Local Clone
- Local Clone Step 1 (lines 220-231): `git clone https://github.com/geekatron/jerry.git ~/plugins/jerry` — requires `github.com`
- No text addresses the scenario where `github.com` is completely unreachable

**Consequence:** Users routed to Local Clone by the decision table still cannot complete installation in a fully air-gapped environment. The routing creates a false expectation of a working offline path.

**Countermeasure:** Add an "Air-gapped installation" note at the end of the Local Clone section with the manual transfer procedure described in the iteration-1 countermeasure.

**Acceptance Criteria:** A user in a fully air-gapped environment has a documented, if manual, path to complete installation.

---

### RT-010-20260225: Hook Execution Model and File-System Permissions Not Documented [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Corporate IT Admin |
| **Section** | Enable Hooks |
| **Category** | Dependency |
| **Exploitability** | Medium |
| **Priority** | P1 |
| **Defense** | Missing |
| **Iteration Status** | Not addressed in revision |

**Attack Vector:** The Enable Hooks section tells users to install uv and promises that "hooks should activate automatically." It does not describe: how hooks are invoked (Claude Code calls `uv run ...`), what `CLAUDE_PLUGIN_ROOT` is, which directories the hooks read and write, whether hooks require network access, or what permissions they need. For a corporate IT security review, this is blocking — "we cannot approve a tool whose execution model is undocumented."

**Evidence from deliverable:** A Grep for "uv run", "CLAUDE_PLUGIN_ROOT", "hook.*execut", and "hook.*permission" returned zero matches in INSTALLATION.md.

**Countermeasure:** Add a "How hooks work" technical callout under Enable Hooks with the content described in the iteration-1 countermeasure.

**Acceptance Criteria:** IT admin can describe Jerry hook runtime behavior in a security assessment from the documentation alone.

---

### RT-013-20260225: No Verification That JERRY_PROJECT Reaches Claude Code [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Windows Developer |
| **Section** | Configuration |
| **Category** | Dependency |
| **Exploitability** | High |
| **Priority** | P1 |
| **Defense** | Missing |
| **Iteration Status** | Not addressed in revision |

**Attack Vector:** Configuration step 3 persists `JERRY_PROJECT` to the shell profile but provides no verification step. Users must close their terminal, open a new one, and then launch Claude Code to test whether the variable propagated correctly. If it didn't (wrong profile file, wrong shell, wrong syntax on Windows), they encounter `<project-required>` in Claude Code with no diagnostic path in the Configuration section.

**Evidence from deliverable:** Configuration step 3 ends with the persistence command. There is no subsequent "verify this worked" step before proceeding to step 4. The Verification section (lines 360-382) focuses on plugin and hooks verification, not environment variable verification.

**Countermeasure:** Add a verification sub-step between steps 3 and 4: "Verify the variable is set: open a new terminal session, then run `echo $JERRY_PROJECT` (macOS/Linux) or `echo $env:JERRY_PROJECT` (Windows). If this prints your project ID, proceed to step 4. If empty, the persistence step did not take effect — re-check that the profile file was saved and that you opened a new terminal session."

**Acceptance Criteria:** User can verify `JERRY_PROJECT` is correctly persisted before proceeding to directory creation.

---

### RT-014-20260225: No Windows-Specific Hook Troubleshooting [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Windows Developer |
| **Section** | Troubleshooting — Hook Issues |
| **Category** | Boundary |
| **Exploitability** | High |
| **Priority** | P1 |
| **Defense** | Partial |
| **Iteration Status** | Not addressed in revision |

**Attack Vector:** The Troubleshooting section's "Hooks not firing" entry (lines 544-551) provides platform-agnostic steps: verify uv is installed, restart Claude Code, check Errors tab. On Windows, hooks may fail for Windows-specific reasons: symlink operations requiring Developer Mode, paths with backslashes instead of forward slashes, or `CLAUDE_PLUGIN_ROOT` containing spaces. None of these are documented in the Windows-specific troubleshooting steps.

**Evidence from deliverable (lines 544-551):**
1. Verify uv is installed
2. Restart Claude Code completely
3. Check Errors tab
4. See the early access caveat

No Windows-specific diagnostic steps.

**Countermeasure:** Add a "Hooks not firing on Windows" subsection with the Windows-specific checklist described in the iteration-1 countermeasure.

**Acceptance Criteria:** A Windows user experiencing hook failures has a Windows-specific diagnostic checklist available in Troubleshooting.

---

### RT-020-20260225: JERRY_PROJECT Must Be Set Before Claude Code Launch — Not Stated [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Impatient Expert |
| **Section** | Configuration |
| **Category** | Dependency |
| **Exploitability** | Medium |
| **Priority** | P1 |
| **Defense** | Partial |
| **Iteration Status** | Not addressed in revision |

**Attack Vector:** The document describes setting and persisting `JERRY_PROJECT` but never explains the launch-order dependency: Claude Code inherits environment variables from the terminal process that launches it. A user who:

1. Opens Claude Code (before setting the variable)
2. Opens a terminal and runs `export JERRY_PROJECT=PROJ-001-my-project`
3. Returns to the already-running Claude Code

...will see `<project-required>` because Claude Code inherited the environment from when it was launched (before the variable was set). Restarting Claude Code from the updated terminal fixes it, but the document never says this.

**Evidence from deliverable:** Configuration step 2 and 3 describe setting and persisting `JERRY_PROJECT`. Verification section (line 362) says "start a new Claude Code session" — but does not specify this means launching from a terminal where the variable is already set. The Verification section for hooks does not cross-reference Configuration to ensure launch order.

**Countermeasure:** Add one sentence to Configuration step 3 and Verification: "After setting JERRY_PROJECT, launch Claude Code from the same terminal session to ensure it inherits the variable. If Claude Code is already open, restart it from a terminal where the variable is set."

**Acceptance Criteria:** A user who sets `JERRY_PROJECT` and immediately gets `<project-required>` understands they need to restart Claude Code from the correct terminal.

---

## Scoring Impact

| Dimension | Weight | Impact | Iteration-2 Rationale |
|-----------|--------|--------|----------------------|
| **Completeness** | 0.20 | Negative | RT-003 (no slash command orientation) and RT-008 (no network requirements) remain both Critical and unaddressed. RT-009, RT-010, RT-013, RT-014, RT-016 remain as Major completeness gaps. Closures (RT-002, RT-004, RT-018) improve completeness modestly. Net: still significantly negative on this dimension. |
| **Internal Consistency** | 0.20 | Negative | RT-012 is now internally inconsistent in a new way: Configuration step 2 uses `$env:JERRY_PROJECT` (correct), but step 3 uses `Set-Variable -Scope Global` (incorrect). The revision created a within-document inconsistency where the correct and incorrect patterns appear in adjacent steps. |
| **Methodological Rigor** | 0.20 | Neutral | The installation methodology and step ordering are sound. Three closures (RT-002, RT-004, RT-018) represent genuine methodological improvements: SSH is no longer presented as a gating requirement, the decision table now enables self-diagnosis, and source name verification is now proactive. No new rigor-level gaps introduced. |
| **Evidence Quality** | 0.15 | Negative | RT-007 (uv installer scope undescribed) and RT-010 (hook execution model undocumented) remain open. Security-conscious users and IT admins still cannot assess the safety posture from the documentation alone. |
| **Actionability** | 0.15 | Slightly Improved | RT-002 closed (SSH row now non-blocking). RT-004 closed (self-diagnosis SSH tip added). RT-018 closed (proactive Step 2 verification). Remaining Major actionability gaps: RT-001, RT-005, RT-013, RT-020. Net: modest improvement, but significant gaps remain. |
| **Traceability** | 0.10 | Neutral | Navigation table, anchor links, and section references remain well-structured. No regressions introduced. |

**Iteration-2 composite assessment:** The revision closed 3 findings (RT-002, RT-004, RT-018) and introduced 3 new Minor findings (RT-N1-i2, RT-N2-i2, RT-N3-i2). The two P0 Critical findings (RT-003, RT-008) remain unaddressed. The Windows persistence bug (RT-012) — a code-level accuracy error — was not fixed despite being identified in iteration 1 as a named code change. Estimated composite score delta from iteration 1: approximately +0.02 to +0.03 (improvements from 3 closures offset by persistence of the 2 Criticals and the continued RT-012 bug).

---

## Overall Assessment

**Recommendation: REVISE — same classification as iteration 1; targeted remediation still required**

The iteration-2 revision made genuine improvements: the SSH prerequisite is no longer a stop point, the decision table enables SSH self-diagnosis, and the proactive Step 2 verification prevents the plugin-not-found confusion loop. These were well-chosen fixes that address two of the highest-exploitability newcomer failures.

However, the revision did not address either P0 Critical finding, and the Windows persistence bug (RT-012) — an explicit code-level error that was named with the exact corrected code in the iteration-1 countermeasure — was not fixed.

**Priority remediation path for iteration 3:**

1. **RT-003** (Critical, P0): Add one sentence explaining where slash commands are entered in Claude Code. This is the highest-severity unaddressed finding. Cost: 1 sentence. Impact: removes the primary blocker for every new Claude Code user.

2. **RT-008** (Critical, P0): Add a Network Requirements section to Prerequisites listing required domains. Cost: a 4-row table. Impact: unblocks corporate deployments.

3. **RT-012** (Major, P1 — BUG): Replace `Set-Variable -Scope Global` with `$env:JERRY_PROJECT` in Configuration step 3. Cost: one line of code. Impact: prevents Windows users from permanently breaking their setup while following the documentation.

4. **RT-007, RT-009, RT-010** (Major, P1): Add what-the-installer-does summary, air-gap path, and hook execution model documentation. Estimated cost: 3 paragraphs across 3 sections.

5. **RT-013, RT-020** (Major, P1): Add JERRY_PROJECT verification step and launch-order statement. Cost: 2 sentences in Configuration.

6. **RT-014, RT-016** (Major, P1): Add Windows hook troubleshooting and hook-to-Windows-status mapping. Cost: 1 subsection and 1 table column/annotation.

The two Critical findings (RT-003 and RT-008) and the Windows persistence bug (RT-012) are the highest-leverage iteration-3 targets. All three have specific, low-cost countermeasures that can be implemented in under 30 minutes of document editing.

---

## Execution Statistics

- **Total Findings (iteration 2):** 20 (17 carried forward, 3 new)
- **Critical:** 2 (RT-003, RT-008 — both carried forward, both unaddressed)
- **Major:** 10 (RT-001, RT-005, RT-007, RT-009, RT-010, RT-012, RT-013, RT-014, RT-016, RT-020)
- **Minor:** 8 (RT-006, RT-011, RT-015, RT-017, RT-019, RT-N1-i2, RT-N2-i2, RT-N3-i2)
- **Findings Closed:** 3 (RT-002, RT-004, RT-018)
- **New Findings (iteration 2):** 3 (RT-N1-i2, RT-N2-i2, RT-N3-i2 — all Minor)
- **Protocol Steps Completed:** 5 of 5
- **Personas Evaluated:** 4 of 4
- **Attack Vector Categories Used:** Ambiguity, Boundary, Circumvention, Dependency, Degradation (all 5)

---

*Report generated by adv-executor | Strategy: S-001 Red Team Analysis v1.0.0*
*Template: `.context/templates/adversarial/s-001-red-team.md`*
*Deliverable: `docs/INSTALLATION.md` (iteration 2, revised 2026-02-25)*
*Prior Report: `docs/reviews/iteration-1-s001-red-team.md`*
*Date: 2026-02-25*

# Red Team Report: INSTALLATION.md (Iteration 3)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `docs/INSTALLATION.md` — Jerry Framework Installation Guide (Revised 2026-02-25, Iteration 3)
**Criticality:** C4 (public-facing OSS documentation, irreversible first-impression surface)
**Date:** 2026-02-25
**Reviewer:** adv-executor (S-001 Red Team Analysis v1.0.0)
**H-16 Compliance:** S-003 Steelman not confirmed as a prior step. Execution proceeds at user direction (iteration 3 of C4 adversarial tournament). H-16 advisory documented; same waiver applies as prior iterations.
**Prior Iterations:** `docs/reviews/iteration-1-s001-red-team.md` (20 findings) | `docs/reviews/iteration-2-s001-red-team.md` (20 findings, 3 closed, 3 new)
**Threat Actors:** Four personas (identical to prior iterations — same document, same audience)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Iteration Delta: Closed Findings](#iteration-delta-closed-findings) | What the revision fixed |
| [Iteration Delta: Remaining Findings](#iteration-delta-remaining-findings) | What the revision did not address |
| [Step 1: Threat Actor Profiles](#step-1-threat-actor-profiles) | Four adversarial personas (carried forward) |
| [Step 2: Attack Vector Inventory](#step-2-attack-vector-inventory) | Remaining + new vectors with RT-NNN-i3 identifiers |
| [Step 3: Defense Gap Assessment](#step-3-defense-gap-assessment) | Defense status for all open vectors |
| [Step 4: Countermeasures](#step-4-countermeasures) | Specific remediation actions — P0 and P1 |
| [Step 5: Findings Summary](#step-5-findings-summary) | Consolidated summary table |
| [Detailed Findings](#detailed-findings) | Full detail for Critical and Major findings |
| [Scoring Impact](#scoring-impact) | S-014 dimension impact mapping |
| [Overall Assessment](#overall-assessment) | Recommendation and path forward |

---

## Iteration Delta: Closed Findings

The following iteration-2 findings are confirmed CLOSED in the revised document. Each is verified against the current text.

| ID | Original Finding | Evidence of Closure |
|----|-----------------|---------------------|
| RT-003-20260225 | No instruction on where to enter slash commands | Line 75: `> **Where do I type these commands?** All /plugin commands are typed into Claude Code's chat input — the same text box where you send messages to the AI. Type the command and press Enter. These are not terminal commands.` Present as a callout immediately in the "Install from GitHub" section header. |
| RT-008-20260225 | No network access requirements documented | Line 42: `> **Network access:** The GitHub install method needs outbound access to github.com. If you install uv for hooks, the installer reaches astral.sh. The Local Clone method requires github.com only for the initial clone — after that, no network access is needed. For fully air-gapped environments, see Air-gapped install under Local Clone.` |
| RT-012-20260225 | Windows JERRY_PROJECT persistence uses wrong PowerShell scope (BUG) | Line 359: `Add-Content $PROFILE '$env:JERRY_PROJECT = "PROJ-001-my-project"'` — The broken `Set-Variable -Scope Global` syntax is replaced with the correct `$env:JERRY_PROJECT` environment variable assignment. |
| RT-001-20260225 | No Claude Code interface orientation before first slash command | Addressed by the same callout at line 75 (RT-003 fix). The "Where do I type these commands?" callout orients the user to Claude Code as a chat interface. |
| RT-005-20260225 | "mkdir from repo root" — newcomer with no existing repo | Line 376: `> **Don't have a repository yet?** Jerry works in any directory. Create one: mkdir my-project && cd my-project && git init, then run the mkdir command above. Jerry doesn't require an existing codebase.` |
| RT-009-20260225 | No air-gap or fully-blocked-network path | Lines 284-292: "Air-gapped install" subsection added under Local Clone with step-by-step manual transfer procedure and a uv binary download note for `astral.sh`-blocked environments. |
| RT-013-20260225 | No verification that JERRY_PROJECT reaches Claude Code | Line 362: `> **Verify it stuck:** Open a new terminal (to load the updated profile), then run echo $JERRY_PROJECT (macOS/Linux) or echo $env:JERRY_PROJECT (Windows). If this prints your project ID, you're set. If it's empty, check that you saved the profile file and are using the correct shell.` |
| RT-020-20260225 | JERRY_PROJECT must be set before Claude Code launch — not stated | Line 364: `> **Launch order matters:** Claude Code inherits environment variables from the terminal it was launched from. Set JERRY_PROJECT first, then launch Claude Code. If Claude Code is already running, restart it from a terminal where the variable is set.` |

**8 findings closed. 12 remain open (from 20 in iteration 2).**

---

## Iteration Delta: Remaining Findings

The following iteration-2 findings are confirmed OPEN in the revised document. Evidence references the current text.

| ID | Original Severity | Status | Evidence of Continued Gap |
|----|------------------|--------|--------------------------|
| RT-007-20260225 | Major | Open | Security note at line 180 still describes HOW to inspect the script but does not state WHAT the installer does (target directories, privilege requirements, system modifications). No "What this installs" paragraph added. |
| RT-010-20260225 | Major | Open | No description of hook execution model anywhere in document. Grep for `CLAUDE_PLUGIN_ROOT`, `uv run`, `hook.*execut`, `hook.*permission` returns zero matches in INSTALLATION.md. |
| RT-014-20260225 | Major | Open | Troubleshooting "Hooks not firing" (lines 574-581) remains platform-agnostic. No Windows-specific hook troubleshooting subsection added. |
| RT-016-20260225 | Major | Open | Platform Note (line 5) still says "hooks that use symlinks or path-sensitive operations may behave differently" without naming which hooks. No Windows column or annotation added to hooks table or Capability Matrix. |
| RT-006-20260225 | Minor | Open | "Start a new Claude Code session" (line 201) still undefined. No clarification that this means close and reopen the application. |
| RT-011-20260225 | Minor | Open | No hash/checksum for uv install script. No integrity verification mechanism added. |
| RT-015-20260225 | Minor | Open | Troubleshooting "uv: command not found" (lines 570-572) still lacks a verification step before the PATH fix — the user is told to add `%USERPROFILE%\.local\bin` to PATH without first confirming where uv was installed. |
| RT-017-20260225 | Minor | Open | No TL;DR / Quick Install block added. First copyable command remains behind prose paragraphs. |
| RT-019-20260225 | Minor | Open | "Run from your repository root" (line 366) still unspecified for multi-repo contexts. No "specific repository where you plan to use Jerry" language. |
| RT-N1-i2 | Minor | Open | Decision table routes user to "Install from GitHub (HTTPS)" but the section is headed "Install from GitHub" with no HTTPS designation. Section mismatch persists. |
| RT-N2-i2 | Minor | Open | Troubleshooting "Plugin source add fails (non-SSH error)" (line 542) refers to Local Clone without naming the specific domains used by Local Clone. IT admin allowlist remains incomplete. |
| RT-N3-i2 | Minor | Open | Shortcut tip at line 102 (`/plugin market list`) still does not connect to Step 3's `@suffix` requirement. Expert who uses shortcut only will not understand why the output name matters. |

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

*Iteration-3 execution IDs use suffix `-i3` to distinguish from prior findings. Carried-forward findings retain their original IDs for traceability.*

### Persona A: Confused Newcomer

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-006-20260225 | "Start a new Claude Code session" (line 201) is undefined — newcomer does not know this means close and reopen the application | Ambiguity | Medium | Minor | P2 | Missing | Actionability |
| RT-N1-i2 | Decision table routes user to "Install from GitHub (HTTPS)" but the actual section heading is "Install from GitHub" — no HTTPS designation in the section header, creating a disconnect when the user arrives | Ambiguity | Medium | Minor | P2 | Partial | Internal Consistency |
| RT-N4-i3 | The "Where do I type these commands?" callout (line 75) appears AFTER the "Install from GitHub" section header and before Step 1's table — but it is positioned inside the GitHub install section. A newcomer using the Session Install or Local Clone paths never encounters this orientation. They still have no instruction on where to type `/plugin marketplace add ~/plugins/jerry` or `/plugin install jerry@<name>`. | Boundary | High | Major | P1 | Missing | Completeness |

### Persona B: Corporate IT Admin

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-007-20260225 | uv installer security note describes HOW to inspect but not WHAT the installer does — target directories, privilege requirements, system modifications absent | Dependency | High | Major | P1 | Partial | Evidence Quality |
| RT-010-20260225 | Hook execution model undocumented — no description of how hooks invoke uv, what `CLAUDE_PLUGIN_ROOT` is, which directories hooks access, or whether hooks require network access | Dependency | Medium | Major | P1 | Missing | Evidence Quality |
| RT-011-20260225 | No hash/checksum for uv install script — inspect-then-run guidance does not cover supply-chain integrity | Dependency | Low | Minor | P2 | Missing | Methodological Rigor |
| RT-N2-i2 | Troubleshooting "Plugin source add fails (non-SSH error)" recommends Local Clone but does not name which domains Local Clone requires — IT admin cannot build a minimal allowlist for the alternative path | Ambiguity | Medium | Minor | P2 | Partial | Completeness |
| RT-N5-i3 | The Network access callout (line 42) correctly lists `github.com` and `astral.sh`. However, it does not list `raw.githubusercontent.com`, which Claude Code may use when fetching plugin manifests or checking for plugin updates. An IT admin who allowlists only the two listed domains may experience install failures at update time or during the "Discover" tab rendering step that Claude Code performs after source registration. | Ambiguity | Medium | Major | P1 | Missing | Completeness |

### Persona C: Windows Developer

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-014-20260225 | No Windows-specific hook troubleshooting — platform-agnostic "Hooks not firing" entry (lines 574-581) does not address Windows-specific failure modes | Boundary | High | Major | P1 | Partial | Completeness |
| RT-016-20260225 | Platform Note warns about Windows symlink limitations but does not name which hooks are affected — Windows developer cannot determine which Capability Matrix rows apply to their platform | Ambiguity | High | Major | P1 | Partial | Completeness |
| RT-015-20260225 | uv PATH fix on Windows (line 572) specifies `%USERPROFILE%\.local\bin` without a preceding verification step to confirm where uv was actually installed | Ambiguity | Medium | Minor | P2 | Missing | Actionability |
| RT-N6-i3 | Local Clone Step 2 (line 258) instructs Windows users to replace `YOUR_USERNAME` with their actual Windows username and provides `echo $env:USERNAME` to find it. However, the path uses `C:/Users/YOUR_USERNAME/plugins/jerry` hardcoded with a leading `C:` drive letter. Windows users whose user profile is on a different drive (D:, E:, common in corporate environments with redirected home directories) will get a path error that the document does not address. | Ambiguity | Medium | Minor | P2 | Partial | Completeness |

### Persona D: Impatient Expert

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-017-20260225 | No TL;DR / Quick Install block — expert who skims reads prose before reaching first command | Degradation | High | Minor | P2 | Missing | Actionability |
| RT-019-20260225 | "Run from your repository root" (line 366) underspecified for experts with multiple repos open simultaneously | Ambiguity | Medium | Minor | P2 | Partial | Actionability |
| RT-N3-i2 | The `/plugin market list` shortcut tip (line 102) does not explain that the listed source name is what goes into the `@suffix` of the next step — expert who uses shortcut only misses this connection | Ambiguity | Medium | Minor | P2 | Partial | Actionability |

---

## Step 3: Defense Gap Assessment

| ID | Existing Defense | Classification | Adversary Exploitation Path |
|----|-----------------|----------------|----------------------------|
| RT-006-20260225 | None | Missing | Newcomer who sees "start a new Claude Code session" after installing uv interprets this as starting a new conversation, not relaunching the application. Hook verification never fires correctly. |
| RT-N1-i2 | 4-row decision table routes to section | Partial | User clicks "Install from GitHub (HTTPS)" link, arrives at section headed "Install from GitHub" — minor confusion, does not block installation but creates friction |
| RT-N4-i3 | Orientation callout present in GitHub install section | **Missing for Local Clone / Session Install paths** | A newcomer following Local Clone or Session Install never sees the "Where do I type these commands?" callout. They encounter `/plugin marketplace add ~/plugins/jerry` with no explanation of where to type it. |
| RT-007-20260225 | Security note with inspect-then-run mechanism | Partial | IT admin can review script content but cannot derive system impact summary from the documentation alone; security review blocked |
| RT-010-20260225 | None | **Missing** | Hook execution model is undocumented; security review of hooks cannot be performed from the installation guide |
| RT-011-20260225 | Inspect guidance | Partial | No integrity verification mechanism for supply-chain attacks |
| RT-N2-i2 | Troubleshooting entry recommends Local Clone | Partial | Local Clone's own domain requirements not named; allowlist for that alternative path is still incomplete |
| RT-N5-i3 | Network access callout lists github.com and astral.sh | Partial | `raw.githubusercontent.com` absent from allowlist; IT admin who implements allowlist based on documentation may block plugin update/discovery operations |
| RT-014-20260225 | Platform-agnostic hook troubleshooting | Partial | Windows-specific failure modes (symlinks, path issues, CLAUDE_PLUGIN_ROOT with spaces) not documented; developer must file issue to learn what documentation should have covered |
| RT-016-20260225 | Generic Platform Note warning about symlinks | Partial | No hook-to-Windows-status mapping; developer cannot determine which enforcement layers are functional on their platform |
| RT-015-20260225 | PATH fix listed | Partial | No verification step before fix; path may differ depending on how uv was installed |
| RT-N6-i3 | echo $env:USERNAME provided for username discovery | Partial | Drive letter `C:` hardcoded; users with non-C drive home directories get silently wrong path |
| RT-017-20260225 | Navigation table and 4-row decision table | Partial | No condensed expert path; prose dominates before first copyable command |
| RT-019-20260225 | "Run from repo root" wording present | Partial | Multi-repo context not addressed |
| RT-N3-i2 | Step 2 shows marketplace list command | Partial | Shortcut tip omits the critical connection to Step 3's @suffix requirement |

---

## Step 4: Countermeasures

### P0 — No P0 Critical Findings Remain

Both prior P0 Critical findings (RT-003, RT-008) are CLOSED in iteration 3. The document no longer has Critical severity attack vectors. This represents the most significant quality improvement across the three iterations.

---

### P1 — Important: SHOULD address

**RT-N4-i3: Slash-command orientation missing from Local Clone and Session Install paths**

The "Where do I type these commands?" callout was added only to the "Install from GitHub" section. Users following the Local Clone or Session Install paths encounter identical slash commands (`/plugin marketplace add`, `/plugin install`, etc.) with no orientation.

Countermeasure: Move the slash-command orientation callout to the top of the "Which Install Method?" section (before the routing table) or to a standalone "Before You Begin" block that precedes all install paths. Alternatively, duplicate the callout at the top of the Local Clone section's Step 2.

Acceptance Criteria: A first-time Claude Code user who follows the Local Clone or Session Install path knows where to type slash commands before encountering their first `/plugin` instruction.

---

**RT-N5-i3: Network access callout incomplete — raw.githubusercontent.com missing**

The Network access callout (line 42) lists `github.com` and `astral.sh` but does not list `raw.githubusercontent.com`, which Claude Code uses when fetching plugin manifests during the Discover tab population and potentially during plugin updates.

Countermeasure: Add `raw.githubusercontent.com` to the network access callout with a note: "Required for Claude Code to display and update community plugins via the Discover tab. The Local Clone method eliminates this requirement after the initial clone." Verify by testing plugin discovery and update behavior with `raw.githubusercontent.com` blocked.

Acceptance Criteria: An IT admin who implements the documented allowlist can successfully add a plugin source, install Jerry, and receive updates without network errors.

---

**RT-007-20260225: uv installer security note describes HOW but not WHAT**

*Carried forward from iteration 2, not addressed in iteration 3.*

Countermeasure: Add one paragraph below the security note: "What the installer does: downloads the uv binary to `~/.local/bin/uv` (macOS/Linux) or `%USERPROFILE%\.local\bin\uv.exe` (Windows), and appends a PATH entry to your shell profile. It does not require root or administrator privileges, makes no system-wide changes, and does not install Python separately (uv manages Python runtimes internally). No other files are created."

Acceptance Criteria: An IT admin reading the uv security note can write a security scope description for the installer without reading or executing the install script.

---

**RT-010-20260225: Hook execution model and permissions not documented**

*Carried forward from iteration 2, not addressed in iteration 3.*

Countermeasure: Add a "How hooks work" technical callout under Enable Hooks: "Jerry's hooks are Python scripts executed by Claude Code using the uv binary. When a hook fires, Claude Code runs `uv run --directory {CLAUDE_PLUGIN_ROOT} jerry {hook-name}`. The scripts read and write files in your project directory (`projects/{JERRY_PROJECT}/`) and the Jerry plugin directory. No network access is required at hook execution time. No elevated privileges are required."

Acceptance Criteria: An IT admin can describe Jerry hook runtime behavior in a security assessment from the documentation alone.

---

**RT-014-20260225: No Windows-specific hook troubleshooting**

*Carried forward from iteration 2, not addressed in iteration 3.*

Countermeasure: Add a "Hooks not firing on Windows" subsection in Troubleshooting: "(1) Verify `uv --version` works in the same terminal you use to launch Claude Code. (2) Verify `CLAUDE_PLUGIN_ROOT` resolves to a path without spaces. (3) Verify the plugin directory path does not use backslashes — Claude Code requires forward slashes on Windows. (4) Check [GitHub Issues tagged `hooks`](https://github.com/geekatron/jerry/issues?q=label%3Ahooks) for current Windows hook status — some hooks use symlink operations that require Windows Developer Mode."

Acceptance Criteria: A Windows user experiencing hook failures has a Windows-specific diagnostic checklist without needing to file an issue first.

---

**RT-016-20260225: Platform Note does not specify which hooks are affected by Windows symlinks**

*Carried forward from iteration 2, not addressed in iteration 3.*

Countermeasure: Add a Windows status annotation to the hooks table (SessionStart, UserPromptSubmit, PreCompact, PreToolUse, SubagentStop, Stop) with a "Windows status" column. If the full characterization is not yet available, add a link to a tracked GitHub Issue for Windows hook status so the developer has a current reference.

Acceptance Criteria: A Windows developer can determine from the Enable Hooks section which of the 6 hooks are expected to function on their platform and which require Windows Developer Mode.

---

### P2 — Monitor

**RT-006-20260225 (Minor):** Add "Close and reopen Claude Code completely" to the hooks verification step (line 201) to clarify what "start a new session" means.

**RT-011-20260225 (Minor):** Link to uv's published release checksums for users requiring installer integrity verification: `https://github.com/astral-sh/uv/releases` includes SHA256 hashes per release.

**RT-015-20260225 (Minor):** Add `where uv` (Windows) or `which uv` (macOS/Linux) as a verification step before the manual PATH fix to confirm where uv was installed before prescribing the fix location.

**RT-017-20260225 (Minor):** Add a Quick Install block (3-command summary) after the nav table for expert users who want commands without prose.

**RT-019-20260225 (Minor):** Strengthen "run from your repository root" (line 366) to "from the root of the specific repository where you plan to use Jerry."

**RT-N1-i2 (Minor):** Align the decision table routing label "Install from GitHub (HTTPS)" with the actual section heading "Install from GitHub" — either update the section heading or update the table label to match.

**RT-N2-i2 (Minor):** In the "Plugin source add fails (non-SSH error)" troubleshooting entry, name the domains used by Local Clone so IT can build a minimal allowlist for that alternative path.

**RT-N3-i2 (Minor):** Add to the `/plugin market list` shortcut tip (line 102): "The source name shown in the output is the `@suffix` you use in Step 3's install command."

**RT-N6-i3 (Minor):** In Local Clone Step 2, replace the hardcoded `C:` drive with `$env:USERPROFILE` in the Windows example path, or add a note: "Replace `C:/Users/YOUR_USERNAME` with the actual path shown by `echo $env:USERPROFILE`."

---

## Step 5: Findings Summary

| ID | Persona | Attack Vector (short) | Category | Exploit | Severity | Priority | Defense | Status |
|----|---------|----------------------|----------|---------|----------|----------|---------|--------|
| RT-N4-i3 | Newcomer | Slash-command orientation missing from Local Clone and Session Install paths | Boundary | High | **Major** | P1 | Missing | New (iteration 3) |
| RT-N5-i3 | IT Admin | raw.githubusercontent.com missing from network access callout | Ambiguity | Medium | **Major** | P1 | Missing | New (iteration 3) |
| RT-007-20260225 | IT Admin | uv installer describes HOW to review but not WHAT it does | Dependency | High | Major | P1 | Partial | Open (not fixed) |
| RT-010-20260225 | IT Admin | Hook execution model undocumented | Dependency | Medium | Major | P1 | Missing | Open (not fixed) |
| RT-014-20260225 | Windows | No Windows-specific hook troubleshooting | Boundary | High | Major | P1 | Partial | Open (not fixed) |
| RT-016-20260225 | Windows | Which hooks are affected by Windows symlinks — not listed | Ambiguity | High | Major | P1 | Partial | Open (not fixed) |
| RT-006-20260225 | Newcomer | "Start a new Claude Code session" undefined | Ambiguity | Medium | Minor | P2 | Missing | Open |
| RT-011-20260225 | IT Admin | No hash/checksum for uv install script | Dependency | Low | Minor | P2 | Missing | Open |
| RT-015-20260225 | Windows | uv PATH fix given without prior verification | Ambiguity | Medium | Minor | P2 | Missing | Open |
| RT-017-20260225 | Expert | No TL;DR / Quick Install block | Degradation | High | Minor | P2 | Missing | Open |
| RT-019-20260225 | Expert | "Repo root" underspecified in multi-repo contexts | Ambiguity | Medium | Minor | P2 | Partial | Open |
| RT-N1-i2 | Newcomer | "Install from GitHub (HTTPS)" row label doesn't match section title | Ambiguity | Medium | Minor | P2 | Partial | Open |
| RT-N2-i2 | IT Admin | Local Clone alternative domain not named for corporate proxy case | Ambiguity | Medium | Minor | P2 | Partial | Open |
| RT-N3-i2 | Expert | Shortcut tip for `/plugin market list` doesn't connect to Step 3 | Ambiguity | Medium | Minor | P2 | Partial | Open |
| RT-N6-i3 | Windows | Hardcoded C: drive in Local Clone path excludes non-C drive home dirs | Ambiguity | Medium | Minor | P2 | Partial | New (iteration 3) |

**Totals: 0 Critical (P0), 6 Major (P1), 9 Minor (P2). Total: 15 open findings.**

*Iteration 2 totals: 2 Critical, 10 Major, 8 Minor (20 findings). Net change this iteration: -2 Critical (both closed), -4 Major (6 closed: RT-001, RT-003, RT-005, RT-008, RT-009, RT-012, RT-013, RT-020 — note RT-001 closed by RT-003 fix, leaving 4 previously-Major findings resolved), +2 Major (RT-N4-i3, RT-N5-i3 new), +1 Minor (RT-N6-i3 new). Progress: 8 findings closed, 3 new (2 Major, 1 Minor).*

---

## Detailed Findings

### RT-N4-i3: Slash-Command Orientation Missing From Local Clone and Session Install Paths [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Confused Newcomer |
| **Section** | Local Clone — Step 2; Session Install |
| **Category** | Boundary |
| **Exploitability** | High |
| **Priority** | P1 |
| **Defense** | Missing |
| **Iteration Status** | New finding — introduced by the iteration-3 fix for RT-003 |

**Attack Vector:** The iteration-3 revision correctly added the "Where do I type these commands?" callout (line 75) to resolve RT-003 and RT-001. However, the callout was placed inside the "Install from GitHub" section. The document has three other install paths that also require slash command entry: Local Clone (Step 2: `In Claude Code: /plugin marketplace add ~/plugins/jerry`), Session Install (description references `/problem-solving` slash command), and the Verification section (references `/plugin` commands). A newcomer who follows Local Clone or Session Install never passes through the GitHub install section and never sees the orientation callout.

The Local Clone path is specifically recommended for corporate and offline environments (RT-009 was fixed by adding the air-gap path under Local Clone). A newcomer in a corporate environment who was directed to Local Clone — and for whom this is a realistic primary install path — will encounter `In Claude Code: /plugin marketplace add ~/plugins/jerry` without any prior explanation of what "in Claude Code" means in terms of UI element.

**Evidence from deliverable:**
- Line 75: "Where do I type these commands?" callout appears inside "## Install from GitHub" section header (between the section heading and Step 1)
- Line 253: `In Claude Code: /plugin marketplace add ~/plugins/jerry` — Local Clone Step 2 — no orientation callout precedes this
- Line 264: `Run /plugin marketplace list` — Local Clone Step 3 — no orientation
- Lines 384-404: Verification section uses `/plugin` commands with no slash-command orientation
- The "Session Install" section (lines 306-321) does not include an orientation callout

**Consequence:** The RT-003 fix is incomplete. It resolves the GitHub install path but leaves an identical gap for users following Local Clone or Session Install. A newcomer in a corporate environment is specifically more likely to follow Local Clone and is therefore more vulnerable to this gap than to the original RT-003 gap.

**Countermeasure:** Relocate the "Where do I type these commands?" callout to the "Which Install Method?" section (before the routing table) or create a standalone "Before You Begin" block immediately after the navigation table that precedes all install paths. This ensures every user encounters the orientation regardless of which install path they follow.

**Acceptance Criteria:** A first-time Claude Code user who follows the Local Clone or Session Install path encounters the slash-command orientation before their first `/plugin` instruction.

---

### RT-N5-i3: Network Access Callout Incomplete — raw.githubusercontent.com Missing [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Corporate IT Admin |
| **Section** | Prerequisites — Network Access |
| **Category** | Ambiguity |
| **Exploitability** | Medium |
| **Priority** | P1 |
| **Defense** | Missing |
| **Iteration Status** | New finding — the RT-008 fix surfaced an adjacent gap |

**Attack Vector:** The iteration-3 fix for RT-008 added the Network access callout at line 42, listing `github.com` and `astral.sh`. This is a genuine improvement. However, Claude Code's plugin system uses `raw.githubusercontent.com` for manifest fetching and plugin discovery. Specifically:

1. When a user opens the Discover tab after adding a plugin source, Claude Code fetches the marketplace JSON manifest from GitHub's raw content delivery host, not from `github.com` directly.
2. Plugin update checks via `/plugin marketplace update` may also resolve through `raw.githubusercontent.com`.

A corporate IT admin who reads the Network access callout, constructs an allowlist of `github.com` and `astral.sh`, and tests installation will likely succeed at the CLI plugin install steps (which use the git clone protocol over `github.com`). However, the Discover tab population or update command may fail silently or with a generic network error, creating an unexplained failure mode after IT approves the tool based on the documented domain list.

**Evidence from deliverable:**
- Line 42: Networks callout lists only `github.com` and `astral.sh`
- The Discover tab is described at lines 144-153 (Interactive Installation section) as a post-registration UI element that users can use as an alternative install mechanism
- No mention of `raw.githubusercontent.com` anywhere in the document
- The completeness of the domain list cannot be verified from the documentation alone

**Consequence:** IT admin implements allowlist based on documentation, approves Jerry for deployment, and then encounters unexplained network failures at Discover tab rendering or update time. This post-approval failure is worse than a pre-approval failure — the organization is now committed to the tool but cannot use a documented feature.

**Countermeasure:** Add `raw.githubusercontent.com` to the Network access callout. Separately, verify whether other GitHub CDN domains (e.g., `objects.githubusercontent.com`, `codeload.github.com`) are accessed during plugin operations and add any confirmed domains to the list. If the complete set cannot be determined definitively, note: "Claude Code may access additional GitHub CDN subdomains during plugin discovery and updates. For a complete domain allowlist, monitor network traffic during a test installation on a non-restricted machine."

**Acceptance Criteria:** An IT admin who implements the documented allowlist can successfully add a plugin source, discover Jerry in the Discover tab, install it, and receive updates without network errors.

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
| **Iteration Status** | Not addressed in iteration 3 |

**Attack Vector:** The security note (line 180) provides mechanisms to download and inspect the install script before execution. It does not describe what the script does: target directories, whether it requires root/admin, whether it modifies system PATH or shell profile, what files it leaves behind. For a corporate security review, this is the information that enables or blocks approval — the inspect-then-run mechanism is useful but secondary to knowing what you're approving.

**Evidence from deliverable (line 180):**
> "If your organization requires script inspection before execution: on macOS/Linux, download first with `curl -LsSf https://astral.sh/uv/install.sh -o install-uv.sh`, review it, then run `sh install-uv.sh`..."

No "What this installs" description follows anywhere in the document. An IT admin must read the install script to answer "does this require root?" — a 30-minute task that frequently results in tool rejection when it should be a 30-second documentation read.

**Countermeasure:** Add one paragraph below the security note describing installer behavior: target binary location, shell profile modification, privilege requirements (none), and the absence of other system modifications.

**Acceptance Criteria:** An IT admin reading the uv security note can write a security scope description for the installer without reading or executing the install script.

---

### RT-010-20260225: Hook Execution Model and Permissions Not Documented [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Persona** | Corporate IT Admin |
| **Section** | Enable Hooks |
| **Category** | Dependency |
| **Exploitability** | Medium |
| **Priority** | P1 |
| **Defense** | Missing |
| **Iteration Status** | Not addressed in iteration 3 |

**Attack Vector:** The Enable Hooks section tells users to install uv and promises that "hooks should activate automatically." It does not describe how hooks are invoked (Claude Code calls `uv run ...`), what `CLAUDE_PLUGIN_ROOT` is, which directories the hooks read and write, whether hooks require network access, or what permissions they need. This is blocking for corporate security review.

**Evidence from deliverable:** Grep for `CLAUDE_PLUGIN_ROOT`, `uv run`, `hook.*execut`, `hook.*permission` returns zero matches in INSTALLATION.md. The 6-hook table (lines 167-176) describes what each hook does functionally but says nothing about the execution mechanism that invokes them.

**Countermeasure:** Add a "How hooks work" technical callout with: invocation pattern (`uv run --directory {CLAUDE_PLUGIN_ROOT} jerry {hook-name}`), directories accessed (project directory and plugin directory), network access requirement (none at execution time), privilege requirement (none), and scope of file-system modifications.

**Acceptance Criteria:** An IT admin can describe Jerry hook runtime behavior in a security assessment from the documentation alone.

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
| **Iteration Status** | Not addressed in iteration 3 |

**Attack Vector:** The Troubleshooting "Hooks not firing" entry (lines 574-581) provides 4 steps: verify uv, restart Claude Code, check Errors tab, see early access caveat. These steps are platform-agnostic. On Windows, hooks may fail for Windows-specific reasons: symlink operations requiring Developer Mode, path separators, `CLAUDE_PLUGIN_ROOT` resolving to a path with spaces, or forward-slash path requirements not met. None of these Windows-specific causes are documented, and there is no Windows-specific diagnostic subsection.

**Evidence from deliverable (lines 574-581):**
```
1. Verify uv is installed: uv --version
2. Restart Claude Code completely (close and reopen)
3. Check /plugin Errors tab for any issues related to hooks
4. See the early access caveat
```

No Windows-specific steps. The Platform Note (line 5) acknowledges Windows hook differences exist but provides no diagnostic path for when they occur.

**Countermeasure:** Add "Hooks not firing on Windows" subsection with: uv verification in the launch terminal, path format check for CLAUDE_PLUGIN_ROOT, forward-slash requirement, Developer Mode for symlink hooks, and a link to GitHub Issues for current Windows hook status by hook name.

**Acceptance Criteria:** A Windows user experiencing hook failures has a Windows-specific diagnostic checklist in Troubleshooting.

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
| **Iteration Status** | Not addressed in iteration 3 |

**Attack Vector:** The Platform Note (line 5) warns that "hooks that use symlinks or path-sensitive operations may behave differently" on Windows. The Enable Hooks section lists 6 hooks. The Capability Matrix lists capabilities enabled by each hook. Neither table includes a Windows column or any annotation linking the generic warning to specific hooks. A Windows developer installing Jerry cannot determine:

- Which of the 6 hooks will work correctly on Windows
- Which Capability Matrix rows (features) they will actually receive on their platform
- Whether they need Windows Developer Mode to get hook parity with macOS/Linux

**Evidence from deliverable:**
- Line 5: "hooks that use symlinks or path-sensitive operations may behave differently"
- Hooks table (lines 167-176): 6 hooks with descriptions, no Windows status
- Capability Matrix (lines 209-219): yes/no columns for with/without uv, no Windows platform column
- The bootstrap note on line 5 mentions "bootstrap uses junction points instead of symlinks" but this is about bootstrap, not about which specific hooks are affected

**Consequence:** A Windows developer installs Jerry and runs for weeks under the impression that L3 enforcement (PreToolUse) and P-003 enforcement (SubagentStop) are active when they may be silently failing due to symlink dependency. The "early access caveat" notes that some hooks fail silently — but this is platform-agnostic. The Windows-specific failure modes are invisible in the documentation.

**Countermeasure:** Add a "Windows" column to the 6-hook table indicating which hooks are functional, which require Developer Mode, and which use junction points. If precise characterization is not yet complete, add a link to a tracked GitHub Issue for Windows hook status by hook name.

**Acceptance Criteria:** A Windows developer can determine from the Enable Hooks section which of the 6 hooks are expected to function on their platform.

---

## Scoring Impact

| Dimension | Weight | Impact | Iteration-3 Rationale |
|-----------|--------|--------|----------------------|
| **Completeness** | 0.20 | Positive (improved vs. i2) | Both P0 Critical gaps (RT-003, RT-008) are now closed. Major completeness improvements: slash-command orientation present for GitHub path, network requirements documented, air-gap path added. New gap RT-N4-i3 (Local Clone/Session Install orientation) partially offsets gains — newcomer on Local Clone path still lacks orientation. RT-N5-i3 (missing domain) is a new completeness gap for the IT Admin path. Net: significantly better than iteration 2, but not complete. |
| **Internal Consistency** | 0.20 | Positive (improved vs. i2) | RT-012 (Windows persistence bug) is now fixed — the internal inconsistency between Configuration step 2 (`$env:JERRY_PROJECT`) and step 3 (`Set-Variable -Scope Global`) is resolved. Both steps now use `$env:JERRY_PROJECT`. The document no longer contradicts itself on Windows environment variable syntax. Minor inconsistency RT-N1-i2 (HTTPS label mismatch) remains. Net: substantial improvement from iteration 2. |
| **Methodological Rigor** | 0.20 | Positive (improved vs. i2) | RT-009 closed (air-gap path documented), RT-005 closed (no-repo guidance added), RT-013 closed (verification step added), RT-020 closed (launch order dependency stated). The installation methodology is now substantially more complete. Remaining gaps (RT-007, RT-010) affect the security assessment portion, not the installation procedure itself. Net: rigor meaningfully improved. |
| **Evidence Quality** | 0.15 | Negative (persists) | RT-007 (uv installer scope undescribed) and RT-010 (hook execution model undocumented) both remain open. The security documentation gap persists across all three iterations. An IT admin still cannot complete a security review from the installation guide alone. Net: no change from iteration 2. |
| **Actionability** | 0.15 | Positive (improved vs. i2) | RT-003 closed (chat input orientation now present for GitHub path), RT-001 closed, RT-013 closed (JERRY_PROJECT verification step added), RT-020 closed (launch order stated). New gap RT-N4-i3 partially offsets gains — Local Clone / Session Install users still lack orientation. RT-N3-i2 (shortcut tip) remains. Net: significant improvement, with one new actionability gap. |
| **Traceability** | 0.10 | Neutral | Navigation table, anchor links, and section references remain well-structured. No regressions introduced. |

**Iteration-3 composite assessment:** The revision closed 8 findings (RT-001, RT-003, RT-005, RT-008, RT-009, RT-012, RT-013, RT-020) and introduced 3 new findings (RT-N4-i3 at Major, RT-N5-i3 at Major, RT-N6-i3 at Minor). The most significant improvement is the elimination of both P0 Critical findings — this is the first iteration where no Critical severity findings remain open. Estimated composite score delta from iteration 2: approximately +0.06 to +0.09 (substantial improvement driven by 2 Critical closures and 6 Major closures, partially offset by 2 new Major findings and 4 remaining Major findings).

---

## Overall Assessment

**Recommendation: REVISE — meaningful improvement from iteration 2; no Critical findings; targeted remediation of 6 remaining Major findings required**

Iteration 3 represents the most significant single-iteration improvement across the review cycle. Both P0 Critical findings (RT-003 and RT-008) are closed, and the Windows persistence bug (RT-012) is finally fixed. Eight findings total were addressed, including all explicitly identified high-priority targets from iteration 2's recommended remediation path.

The document is now safe for the primary newcomer path (Install from GitHub). The most dangerous failure modes — "I don't know where to type this command" and "My company's firewall is blocking Jerry" — are addressed.

**Remaining risk profile:**

The 6 remaining Major findings fall into two clusters:

**Security documentation cluster (IT Admin persona):** RT-007, RT-010, RT-N5-i3 — The documentation still cannot support a full corporate security review. An IT admin evaluating Jerry for team deployment cannot determine the uv installer's system impact, cannot describe the hook execution model, and may construct an incomplete domain allowlist. These three findings together block corporate adoption pathways.

**Windows completeness cluster (Windows Developer persona):** RT-014, RT-016 — Windows developers cannot determine which hooks are functional on their platform or troubleshoot Windows-specific hook failures from the documentation. These findings block the Windows developer persona from achieving full hook functionality.

**The new finding RT-N4-i3 is notable:** It is a regression introduced by the RT-003 fix. The slash-command orientation was correctly added for the GitHub install path but not applied globally, leaving the Local Clone and Session Install paths without orientation. This is a medium-priority fix — Local Clone users in corporate environments are the most likely to encounter it, and corporate environments are already under-served by the security documentation gap.

**Priority remediation path for iteration 4:**

1. **RT-N4-i3** (Major, P1): Relocate the slash-command orientation callout to precede all install paths (e.g., in "Which Install Method?" or a "Before You Begin" block). Cost: move one callout. Impact: closes the orientation gap for Local Clone and Session Install users.

2. **RT-N5-i3** (Major, P1): Verify and document all GitHub domains used by Claude Code during plugin operations. Add `raw.githubusercontent.com` to the network access callout. Cost: one domain entry + verification effort. Impact: IT admin allowlist is now actionable.

3. **RT-007** (Major, P1): Add uv installer behavior summary (binary location, profile modification, privilege requirements). Cost: one paragraph. Impact: IT admin security review is completable from documentation.

4. **RT-010** (Major, P1): Add hook execution model description. Cost: one technical callout. Impact: hook security review is completable from documentation.

5. **RT-014 + RT-016** (Major, P1): Add Windows hook troubleshooting and hook-to-Windows-status table. Cost: one subsection + one table column. Impact: Windows developers have a diagnostic path and know which enforcement layers are functional.

If items 1-5 are addressed, the document will have zero Critical and zero Major findings. The remaining 9 Minor findings are improvement opportunities that would move the document to a polished state but do not block primary-path installation for any persona.

---

## Execution Statistics

- **Total Findings (iteration 3):** 15 open (12 carried forward from iteration 2, 3 new)
- **Critical:** 0 (both Criticals from iteration 2 are now closed)
- **Major:** 6 (RT-007, RT-010, RT-014, RT-016, RT-N4-i3, RT-N5-i3)
- **Minor:** 9 (RT-006, RT-011, RT-015, RT-017, RT-019, RT-N1-i2, RT-N2-i2, RT-N3-i2, RT-N6-i3)
- **Findings Closed This Iteration:** 8 (RT-001, RT-003, RT-005, RT-008, RT-009, RT-012, RT-013, RT-020)
- **New Findings (iteration 3):** 3 (RT-N4-i3 Major, RT-N5-i3 Major, RT-N6-i3 Minor)
- **Cumulative Progress:** 11 of 20 original findings closed (55%), 3 iterations completed
- **Protocol Steps Completed:** 5 of 5
- **Personas Evaluated:** 4 of 4
- **Attack Vector Categories Used:** Ambiguity, Boundary, Dependency, Degradation (4 of 5 — Circumvention not applicable this iteration)

---

*Report generated by adv-executor | Strategy: S-001 Red Team Analysis v1.0.0*
*Template: `.context/templates/adversarial/s-001-red-team.md`*
*Deliverable: `docs/INSTALLATION.md` (iteration 3, revised 2026-02-25)*
*Prior Reports: `docs/reviews/iteration-1-s001-red-team.md` | `docs/reviews/iteration-2-s001-red-team.md`*
*Date: 2026-02-25*

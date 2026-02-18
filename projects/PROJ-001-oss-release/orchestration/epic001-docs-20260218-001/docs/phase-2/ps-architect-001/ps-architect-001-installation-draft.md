<!--
CHANGE SUMMARY (strip before replacing docs/INSTALLATION.md)
=============================================================
Agent:     ps-architect-001
Workflow:  epic001-docs-20260218-001
Phase:     2 (FEAT-017 Execution)
Date:      2026-02-18

--- ITERATION 1 (Initial Draft) ---

Changes made (ADDITIVE only — no existing content removed):

1. Table of Contents — two new rows added:
   - "Collaborator Installation" (new section, EN-940)
   - "Future: Public Repository" (new section, EN-941)

2. NEW SECTION: "Collaborator Installation (Private Repository)" — inserted
   immediately after the Installation section header and before the
   macOS/Windows platform tabs.
   - Pre-condition: collaborator invite required from repo admin
   - SSH key generation: macOS (Terminal) and Windows (PowerShell)
   - SSH public key registration at github.com/settings/keys
   - SSH connectivity verification: `ssh -T git@github.com`
   - SSH clone URL variant shown for both platforms
   - Continuation to existing Steps 3-5 made explicit
   - PAT noted as alternative in a brief note
   Satisfies: EN-940, AC-2

3. NEW SECTION: "Future: Public Repository Installation" — inserted at the
   end of the Installation section, before Verification.
   - Clearly framed as future state with a prominent note
   - States Jerry is currently collaborator-only
   - Shows simplified HTTPS clone path (no SSH setup needed)
   - Confirms marketplace steps are identical
   Satisfies: EN-941, AC-3

4. AC-1, AC-4 VERIFIED PRESENT — no changes to existing archive or
   marketplace content. All existing content preserved verbatim.

S-010 Self-Review completed before writing. Structural decision rationale:
- Collaborator section placed before platform tabs (not integrated into tabs)
  to avoid duplicating the SSH key GitHub-registration steps inside each tab
- PAT mentioned as a note to close the documented ambiguity from gap analysis
  without expanding scope beyond what EN-940 requires
- Git Bash noted as a valid SSH path for Windows users who already have it

--- ITERATION 2 (Revision Pass — ps-critic-001 score 0.866) ---

Applied 2 MAJOR + 5 MINOR fixes from ps-critic-001 quality review:

MAJOR-001: Replaced fragile GitHub auto-generated duplicate heading anchors
   with explicit HTML anchor IDs.
   - Added `<a id="macos-step-3"></a>` before macOS Step 3
   - Added `<a id="windows-step-3"></a>` before Windows Step 3
   - Updated Collaborator section cross-references to use stable anchors
     (#macos-step-3, #windows-step-3)

MAJOR-002: Renamed "Steps 5–7: Continue with Platform Installation" to
   "Next Steps: Complete Platform Installation" — eliminates dual numbering
   system that conflicted with the 4-step Collaborator section.

MINOR-001: Updated collaborator notes in macOS Step 2 and Windows Step 2
   from forward-navigation instruction ("use SSH clone URL") to past-tense
   acknowledgment ("you have already cloned via SSH — skip this step").

MINOR-002: Replaced `C:\Users\YOU\.ssh\id_ed25519` with
   `C:\Users\YOUR_USERNAME\.ssh\id_ed25519` in Windows SSH key generation
   to match the YOUR_USERNAME placeholder used elsewhere.

MINOR-003: Added macOS Keychain tip after macOS Step 1 SSH key generation
   (passphrase users: `eval "$(ssh-agent -s)"` + `ssh-add --apple-use-keychain`).

MINOR-004: Replaced fragile `#step-1-install-uv` and `#step-1-install-uv-1`
   anchors in the Future section with section-level references:
   "See macOS Installation (#macos) or Windows Installation (#windows)".

MINOR-005: Expanded PAT Alternative step 1 to specify classic PAT
   ("Generate new token (classic)"), explain the repo scope checkbox,
   and clarify it grants read access to private repositories.

--- ITERATION 3 (QG-1 Adversarial Quality Gate Revision — score 0.7665 -> target >=0.92) ---

Applied 10 priority findings + 2 additional fixes from QG-1 adversarial review (adv-scorer-001):

P1-DA-001: Added ssh-keygen existence pre-check on BOTH platforms before key generation.
   - macOS: `ls ~/.ssh/id_ed25519.pub 2>/dev/null && echo ...`
   - Windows: `if (Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub") { ... }`
   - Added Warning callout: "If you already have an SSH key, DO NOT overwrite it."

P2-DA-002: Updated Claude Code version in Prerequisites table from "Latest" to "1.0.33+"
   to expose the version floor at the prerequisite check stage (not just in Troubleshooting).

P3-DA-004: CRITICAL FIX — corrected manifest verification text from `"name": "jerry"` to
   `"name": "jerry-framework"` on both platforms, confirmed against actual .claude-plugin/plugin.json.
   Added confirmation sentence that the path is correct.

P4-DA-003: Expanded PAT Alternative with credential caching guidance:
   - macOS: `git config --global credential.helper osxkeychain`
   - Windows: `git config --global credential.helper manager`
   - Added Note: "Without a credential helper, git will prompt for your PAT on every pull, fetch, and push."

P5-CC-001: Added "Getting Help" and "License" rows to Table of Contents after Uninstallation.

P6-SM-003/CC-003: Added `/adversary` row to Available Skills table.

P7-DA-007: Qualified "password-free access" in Why SSH? to be accurate for both passphrase
   and non-passphrase scenarios: "...when set up without a passphrase, or when combined with
   an SSH agent that caches your passphrase (see Tip below)."

P8-SM-004: Added Windows SSH agent tip after Windows Step 1 to match macOS Keychain tip.
   Includes `Start-Service ssh-agent`, `ssh-add`, permanent startup, and OpenSSH Client note.

P9-SM-002: Added PAT Alternative forward reference at end of Step 4 clone block.

P10-SM-001: Added "Why the marketplace?" rationale callout at start of Installation section.

SM-009: Added rationale to macOS Keychain tip: "Without this, your terminal will prompt for
   your SSH key passphrase every time you interact with GitHub."

SM-007: Added "(located in the `docs/` directory)" note to BOOTSTRAP.md reference.

--- ITERATION 4 (QG-1 Retry 1 Adversarial Quality Gate Revision — score 0.8300 -> target >=0.92) ---

Applied all 10 priority findings from QG-1 Retry 1 score report (adv-scorer-001, score 0.8300):

P1-DA-004: CRITICAL — Swapped Configuration and Verification section order throughout the document.
   - Configuration now appears BEFORE Verification in both the ToC and the document body.
   - This ensures JERRY_PROJECT is set before the "Test a Skill" step, preventing the
     <project-required> prompt from surprising every new user at the critical first-run moment.

P2-DA-001: Added osxkeychain pre-check before `git config --global credential.helper osxkeychain`.
   - Added `git credential-osxkeychain 2>&1 | head -1` diagnostic command with instructional comments.
   - Added conditional path: use `credential.helper store` if osxkeychain is absent.
   - Added security note about plaintext storage for the store helper.
   - Added new Troubleshooting entry "Credential Helper Not Found (macOS PAT Users)" with cause,
     solution, and install-Xcode-CLT recovery path.

P3-DA-002: Replaced Windows SSH agent `Start-Service ssh-agent` Tip with check-first approach.
   - Added `if (Get-Service ssh-agent -ErrorAction SilentlyContinue)` guard block.
   - Included `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0` install path.
   - Added Settings > Apps > Optional Features UI path as alternative install method.
   - Clarified that absence is common on Home and LTSC editions despite the build floor.

P4-DA-003: Added space-in-path warning at all three clone steps.
   - macOS Installation Step 2: "path must not contain spaces" warning note added.
   - Windows Installation Step 2: warning note added with `C:\plugins\` fallback for usernames with spaces.
   - Collaborator Installation Step 4 (SSH clone): warning note added.

P5-DA-006: Corrected PAT `repo` scope description from "read access" to "full access (read and write)".
   - Added fine-grained PAT alternative with `Contents: Read-only` recommendation for least privilege.

P6-DA-005: Clarified marketplace rationale sentence.
   - Changed "the scope you choose at install time" to "the scope you choose during `/plugin install`".

P7-SM-001: Added Windows PowerShell clone URL variant to PAT Alternative Step 3.
   - Step 3 now shows both macOS/Git Bash and Windows PowerShell clone commands.
   - Consistent with SSH clone step which already provided both variants.

P8-DA-007: Added GitHub rate-limit note to Future section.
   - Added sentence: "unauthenticated HTTPS clones may be subject to GitHub API rate limits;
     authenticating with a GitHub account resolves this."

P9-SM-003: Added detection mechanism to Future section.
   - Added instruction: "visit github.com/geekatron/jerry while logged out — if page loads
     without login prompt, these simplified instructions apply."

P10-SM-002/CC-001: Fixed ToC column header from "Description" to "Purpose" (NAV-003 standard).

--- ITERATION 5 (QG-1 Retry 2 Adversarial Quality Gate Revision — 7 targeted fixes) ---

Applied 7 targeted fixes from QG-1 Retry 2 adversarial review (adv-scorer-001):

P1-DA-001-qg1r2-da (Major): Added OpenSSH Client availability pre-check on Windows BEFORE the
   ssh-keygen command (Windows Step 1). The new callout explains the "not recognized" failure
   mode and provides both the Settings UI path and the PowerShell Add-WindowsCapability command.
   This is distinct from the existing ssh-agent Tip (which only covers agent startup, not keygen).

P2-DA-002-qg1r2-da (Major): Added passphrase prompt note after the "You should see:" block in
   Step 3 (Verify SSH Access). Users who set a passphrase will now know to enter it before
   expecting the success message. Also added "passphrase not entered" as an explicit cause in
   the SSH Authentication Failed troubleshooting entry with step-by-step recovery guidance.

P3-DA-004-qg1r2-da (Minor): Replaced `echo $env:USERNAME` tip (returns only the username, not
   the full path) with `(Get-Item "$env:USERPROFILE\plugins\jerry").FullName -replace '\\','/'`
   which produces the exact forward-slash literal path that Claude Code's marketplace add command
   requires. Added explanatory sentence to guide copy-paste usage.

P4-SM-002-qg1r2s (Minor): Added note to "Test a Skill" step in Verification section explaining
   that `/problem-solving` requires `JERRY_PROJECT` to be set, and directing users to `/help`
   as a project-independent alternative for verifying skill availability.

P5-DA-003-qg1r2-da (Minor): Added space-in-path Important callout to Future: Public Repository
   Installation section, Step 2 clone block — matching the same warning already present at the
   macOS Installation, Windows Installation, and Collaborator Installation clone locations.

P6-SM-003-qg1r2s (Minor): Added space-in-path Important callout to PAT Alternative section,
   Step 3 clone block — matching the warning at the other 3 clone locations. Placed inline above
   the macOS and Windows clone commands to ensure visibility before the user runs the command.

P7-SM-001-qg1r2s (Minor): Expanded Configuration section Project scope recommendation to state
   the operational consequence: "Jerry is added to `.claude/settings.json`, which is committed
   to version control — new team members have Jerry active automatically after cloning the
   repository." This closes the undocumented team-onboarding implication.

--- ITERATION 6 (QG-1 Retry 3 Targeted Polish — 2 P1 fixes to close 0.01 gap) ---

Score 0.9100 (REVISE, 0.01 below 0.92 threshold). 0 Major, 7 Minor. Two P1 fixes:

P1a-SM-003/DA-003-qg1r3 (Minor, double-flagged): Added Troubleshooting entry for
   "<project-required>" and "<project-error>" session start tags. Users who misconfigure or
   skip JERRY_PROJECT setup now have a dedicated recovery path explaining the XML-tagged output,
   its meaning, and how to resolve it with correct environment variable setup.

P1b-DA-004-qg1r3-da (Minor): Added explanation in both macOS and Windows Step 5 that the
   `@jerry` suffix in `/plugin install jerry-framework@jerry` corresponds to the directory name
   used in Step 4. Also added directory-name mismatch as a cause in the "Plugin Not Found"
   Troubleshooting entry to provide a recovery path for non-standard clone paths.
=============================================================
-->

# Jerry Framework Installation Guide

> Jerry is a Claude Code plugin for behavior and workflow guardrails.

---

## Table of Contents

| Section | Purpose |
|---------|---------|
| [Prerequisites](#prerequisites) | What you need before installing |
| [Collaborator Installation](#collaborator-installation-private-repository) | SSH setup for private repository access |
| [Installation](#installation) | Platform-specific setup instructions |
| [Future: Public Repository](#future-public-repository-installation) | When Jerry becomes publicly available |
| [Configuration](#configuration) | Post-installation setup |
| [Verification](#verification) | How to confirm installation succeeded |
| [Using Jerry](#using-jerry) | Getting started with skills |
| [Troubleshooting](#troubleshooting) | Common issues and solutions |
| [For Developers](#for-developers) | Contributing and development setup |
| [Uninstallation](#uninstallation) | How to remove Jerry |
| [Getting Help](#getting-help) | Support resources and documentation |
| [License](#license) | Open source license information |

---

## Prerequisites

### Required Software

| Software | Version | Purpose | Install Guide |
|----------|---------|---------|---------------|
| [Claude Code](https://code.claude.com) | 1.0.33+ | The AI coding assistant Jerry extends | [Setup Guide](https://code.claude.com/docs/en/setup) |
| [Git](https://git-scm.com/) | 2.0+ | Clone the Jerry repository | [Download](https://git-scm.com/downloads) |
| [uv](https://docs.astral.sh/uv/) | Latest | Python dependency management for hooks | See platform instructions below |

> **Note:** You do NOT need Python installed to use Jerry as an end user. Python and uv are used internally by Jerry's hooks. The uv installer handles Python automatically.

### System Requirements

| Requirement | Minimum |
|-------------|---------|
| Disk Space | ~100 MB |
| Internet | Required for initial clone |

---

## Collaborator Installation (Private Repository)

> **Note:** Jerry is currently distributed to collaborators only. This section is for users who have been granted collaborator access by a repository administrator. If you are installing from a public repository, skip ahead to [Installation](#installation).

Jerry is hosted in a private GitHub repository. Before you can clone it, you must:

1. **Receive a collaborator invitation** from the Jerry repository administrator
2. **Accept the invitation** (check your email or visit github.com/notifications)
3. **Set up SSH authentication** — follow the steps below for your platform

### Why SSH?

Private GitHub repositories require authentication. SSH keys provide secure, password-free access when set up without a passphrase, or when combined with an SSH agent that caches your passphrase (see Tip below). SSH keys are the recommended method. A personal access token (PAT) is an alternative HTTPS-based method; see the [PAT Alternative](#pat-alternative) note at the end of this section.

---

### Step 1: Generate an SSH Key

Choose your platform:

#### macOS (Terminal)

> **Warning:** If you already have an SSH key, DO NOT overwrite it. Check first, then display your existing public key and skip to Step 2.

First check whether you already have an SSH key:

```bash
ls ~/.ssh/id_ed25519.pub 2>/dev/null && echo "Key exists — skip to Step 2" || echo "No key found — proceed below"
```

If no key was found, open Terminal and run:

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

When prompted:
- **File location:** Press Enter to accept the default (`~/.ssh/id_ed25519`)
- **Passphrase:** Enter a passphrase (recommended) or press Enter for none

Display your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the full output — it begins with `ssh-ed25519` and ends with your email address.

> **Tip:** If you set a passphrase, add your key to the macOS Keychain to avoid re-entering it each time:
> ```bash
> eval "$(ssh-agent -s)"
> ssh-add --apple-use-keychain ~/.ssh/id_ed25519
> ```
> Without this, your terminal will prompt for your SSH key passphrase every time you interact with GitHub.

#### Windows (PowerShell)

> **Warning:** If you already have an SSH key, DO NOT overwrite it. Check first, then display your existing public key and skip to Step 2.

First check whether you already have an SSH key:

```powershell
if (Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub") { Write-Host "Key exists — skip to Step 2" } else { Write-Host "No key found — proceed below" }
```

If no key was found, open **PowerShell** and run:

> **Important — Windows Home / LTSC Users:** If `ssh-keygen` is not recognized, OpenSSH Client is not installed.
> Install it via **Settings → Apps → Optional Features → Add a feature → OpenSSH Client**, or run:
> ```powershell
> Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
> ```
> Then close and reopen PowerShell before continuing.

```powershell
ssh-keygen -t ed25519 -C "your.email@example.com"
```

When prompted:
- **File location:** Press Enter to accept the default (`C:\Users\YOUR_USERNAME\.ssh\id_ed25519`)
- **Passphrase:** Enter a passphrase (recommended) or press Enter for none

Display your public key:

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"
```

Copy the full output — it begins with `ssh-ed25519`.

> **Windows Git Bash alternative:** If you have Git Bash installed, the macOS Terminal commands above work identically in Git Bash.

> **Tip:** To avoid re-entering your passphrase each session, start the SSH agent. First check if the OpenSSH Client is installed:
> ```powershell
> # Check if OpenSSH Client is installed
> if (Get-Service ssh-agent -ErrorAction SilentlyContinue) {
>     Start-Service ssh-agent
>     ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
>     # To make this permanent:
>     Set-Service -Name ssh-agent -StartupType Automatic
> } else {
>     Write-Host "OpenSSH Client not installed. Install it via:"
>     Write-Host "  Settings > Apps > Optional Features > Add a feature > OpenSSH Client"
>     Write-Host "Or via PowerShell (requires admin):"
>     Write-Host "  Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0"
> }
> ```
> **Note:** OpenSSH Client is enabled by default on Windows 10 build 1809+ and Windows 11, but may be absent on Home and LTSC editions.

---

### Step 2: Add Your SSH Key to GitHub

1. Go to [github.com/settings/keys](https://github.com/settings/keys)
2. Click **New SSH key**
3. Give it a descriptive title (e.g., "My MacBook Pro" or "Work Laptop")
4. Set **Key type** to `Authentication Key`
5. Paste your public key into the **Key** field
6. Click **Add SSH key**

---

### Step 3: Verify SSH Access

Confirm GitHub accepts your key:

```bash
ssh -T git@github.com
```

You should see:

```
Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

> **Note:** If you set a passphrase during key generation, you will be prompted to enter it before seeing the success message. Type your passphrase and press Enter. If you see `Permission denied (publickey)` after entering your passphrase, verify your public key is correctly added to GitHub (Step 2).

If you see a permission denied error, verify your public key was saved correctly at github.com/settings/keys and that you copied the entire key including the `ssh-ed25519` prefix.

---

### Step 4: Clone Jerry via SSH

Use the SSH clone URL instead of the HTTPS URL:

> **Important:** The clone path must not contain spaces. The Claude Code `/plugin marketplace add` command does not support paths with spaces. The recommended `~/plugins/` path is safe.

**macOS (Terminal) or Git Bash:**
```bash
mkdir -p ~/plugins
git clone git@github.com:geekatron/jerry.git ~/plugins/jerry
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\plugins"
git clone git@github.com:geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
```

> **Alternative authentication:** If you prefer not to use SSH, see [PAT Alternative](#pat-alternative) below for HTTPS token-based access.

---

### Next Steps: Complete Platform Installation

After cloning via SSH, proceed directly to **Step 3: Verify the Plugin Manifest** in your platform's installation section below:

- [macOS — Step 3 onwards](#macos-step-3)
- [Windows — Step 3 onwards](#windows-step-3)

The remaining steps (plugin manifest, marketplace add, plugin install) are identical regardless of whether you used SSH or HTTPS to clone.

---

### PAT Alternative

If you prefer HTTPS authentication, you can use a **GitHub Personal Access Token (PAT)** instead of SSH keys:

1. Create a **classic** PAT at [github.com/settings/tokens](https://github.com/settings/tokens) (select 'Generate new token (classic)') and check the `repo` scope checkbox. This grants full access to private repositories you collaborate on (read and write). For least-privilege access, use a fine-grained PAT instead with `Contents: Read-only` permission scoped to the jerry repository only.
2. When `git clone` prompts for a password, enter your PAT instead
3. Use the standard HTTPS clone URL:

   > **Important:** If your username contains spaces, use a path without spaces (e.g., `~/plugins/jerry` or `C:\plugins\jerry`).

   **macOS (Terminal) or Git Bash:**
   ```bash
   git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
   ```

   **Windows (PowerShell):**
   ```powershell
   git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
   ```

To avoid re-entering your PAT on every git operation, configure a credential helper:

**macOS:**

First verify that the osxkeychain helper is available on your system:

```bash
# Verify osxkeychain helper is available
git credential-osxkeychain 2>&1 | head -1
# If you see "usage: git credential-osxkeychain", proceed.
# If you see "command not found", use the store helper instead:
# git config --global credential.helper store
```

If osxkeychain is available:
```bash
git config --global credential.helper osxkeychain
```

If osxkeychain is not available (common on conda, nix, or MacPorts installs), use the store helper:
```bash
git config --global credential.helper store
```
> **Note:** The `store` helper saves credentials in plaintext at `~/.git-credentials`. Use it only on single-user machines.

**Windows:**
```powershell
git config --global credential.helper manager
```

> **Note:** Without a credential helper, git will prompt for your PAT on every pull, fetch, and push.

PATs are more common in CI environments. For interactive use, SSH keys are preferred.

---

## Installation

Jerry is installed as a **Claude Code plugin** via a local marketplace. This is a two-step process:

1. **Add the marketplace** - Registers Jerry's plugin catalog with Claude Code
2. **Install the plugin** - Downloads and activates Jerry's skills

> **Why the marketplace?** Jerry uses Claude Code's plugin system for distribution, scope control, and easy updates. Adding the marketplace first registers Jerry's catalog (the "app store"), so you can then install, update, or uninstall the plugin cleanly with `/plugin` commands. This separation also lets you control whether Jerry is installed per-user, per-project, or locally — the scope you choose during `/plugin install` determines who gets it.

Choose your platform below:

---

### macOS

#### Step 1: Install uv

uv is required for Jerry's hooks to execute Python scripts with automatic dependency resolution.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal (close and reopen), then verify:

```bash
uv --version
# Should output: uv 0.x.x
```

#### Step 2: Clone Jerry

Clone the repository to a location on your system. We recommend `~/plugins/`:

> **Important:** The clone path must not contain spaces. The Claude Code `/plugin marketplace add` command does not support paths with spaces. The recommended `~/plugins/` path is safe.

```bash
mkdir -p ~/plugins
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

> **Collaborators:** If you arrived from the [Collaborator Installation](#collaborator-installation-private-repository) section above, you have already cloned via SSH — skip this step and proceed to Step 3 below.

<a id="macos-step-3"></a>

#### Step 3: Verify the Plugin Manifest

Confirm Jerry's plugin manifest exists:

```bash
cat ~/plugins/jerry/.claude-plugin/plugin.json
```

You should see JSON output with `"name": "jerry-framework"`. This confirms the path is correct and the `.claude-plugin/plugin.json` manifest is present in the repository.

#### Step 4: Add the Local Marketplace

Open Claude Code and run:

```
/plugin marketplace add ~/plugins/jerry
```

This registers Jerry's plugin catalog. No plugins are installed yet—you're just adding the "app store."

#### Step 5: Install the Plugin

Install Jerry from the marketplace:

```
/plugin install jerry-framework@jerry
```

> **Note:** The `@jerry` suffix corresponds to the directory name you used in Step 4 (`~/plugins/jerry`). If you cloned Jerry to a different directory name (e.g., `~/plugins/jerry-framework`), replace `@jerry` with `@jerry-framework` to match.

**Alternative: Interactive Installation**
1. Run `/plugin`
2. Go to the **Discover** tab
3. Find `jerry-framework`
4. Press Enter and select your installation scope:
   - **User** (recommended): Install for yourself across all projects
   - **Project**: Install for all collaborators on this repository
   - **Local**: Install for yourself in this repository only

---

### Windows

#### Step 1: Install uv

Open **PowerShell** (not Command Prompt) and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Important:** Close and reopen PowerShell to update your PATH.

Verify the installation:

```powershell
uv --version
# Should output: uv 0.x.x
```

If you see "command not found," ensure this path is in your system PATH:
```
%USERPROFILE%\.local\bin
```

#### Step 2: Clone Jerry

Clone the repository using PowerShell:

> **Important:** The clone path must not contain spaces. The Claude Code `/plugin marketplace add` command does not support paths with spaces. The recommended `$env:USERPROFILE\plugins\` path is safe (your Windows username does not typically contain spaces, but if it does, choose an alternate path such as `C:\plugins\`).

```powershell
# Create plugins directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\plugins"

# Clone Jerry
git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
```

**Alternative using Git Bash:**
```bash
mkdir -p ~/plugins
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

> **Collaborators:** If you arrived from the [Collaborator Installation](#collaborator-installation-private-repository) section above, you have already cloned via SSH — skip this step and proceed to Step 3 below.

<a id="windows-step-3"></a>

#### Step 3: Verify the Plugin Manifest

Confirm Jerry's plugin manifest exists:

```powershell
Get-Content "$env:USERPROFILE\plugins\jerry\.claude-plugin\plugin.json"
```

You should see JSON output with `"name": "jerry-framework"`. This confirms the path is correct and the `.claude-plugin\plugin.json` manifest is present in the repository.

#### Step 4: Add the Local Marketplace

Open Claude Code and run (note: use **forward slashes** in Claude Code):

```
/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry
```

Replace `YOUR_USERNAME` with your actual Windows username.

**Tip:** To get the exact forward-slash path that Claude Code expects, run this in PowerShell:
```powershell
(Get-Item "$env:USERPROFILE\plugins\jerry").FullName -replace '\\','/'
```
Copy the output and use it directly in the `/plugin marketplace add` command.

#### Step 5: Install the Plugin

Install Jerry from the marketplace:

```
/plugin install jerry-framework@jerry
```

> **Note:** The `@jerry` suffix corresponds to the directory name you used in Step 4. If you cloned Jerry to a different directory name, replace `@jerry` with the actual directory name to match.

---

## Future: Public Repository Installation

> **Note:** This section documents a future installation scenario. Jerry is currently distributed to collaborators only. When Jerry is released as a public repository, these simplified instructions will apply and no SSH setup or collaborator invitation is required.

When Jerry becomes publicly available, installation simplifies significantly:

**No prerequisites beyond Git, uv, and Claude Code.** No GitHub account is required to clone a public repository, and no SSH key setup or collaborator invitation is needed. Note that unauthenticated HTTPS clones may be subject to GitHub API rate limits during periods of high traffic. If you encounter rate-limiting errors, authenticating with a GitHub account resolves this.

### Simplified Installation Steps

**Step 1: Install uv** — identical to the platform-specific steps above. See [macOS Installation](#macos) or [Windows Installation](#windows) for platform-specific uv installation.

**Step 2: Clone Jerry (HTTPS)**

> **Important:** If your username contains spaces, use a path without spaces (e.g., `~/plugins/jerry` or `C:\plugins\jerry`).

```bash
# macOS/Linux
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

```powershell
# Windows PowerShell
git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
```

**Steps 3–5:** Identical to the existing marketplace steps — verify the plugin manifest, add the local marketplace, and install the plugin. See [macOS Installation](#macos) or [Windows Installation](#windows) for platform-specific steps.

### What Changes vs. Collaborator Installation

| Aspect | Current (Collaborator) | Future (Public) |
|--------|------------------------|-----------------|
| GitHub account needed | Yes (for collaborator access) | No |
| SSH key setup | Required | Not required |
| Collaborator invite | Required from repo admin | Not required |
| Clone URL | SSH: `git@github.com:...` | HTTPS: `https://github.com/...` |
| Marketplace steps | Identical | Identical |

To check whether Jerry is now publicly available, visit [github.com/geekatron/jerry](https://github.com/geekatron/jerry) while logged out of GitHub — if the page loads without a login prompt, these simplified instructions apply. If you encounter authentication prompts when following these future steps, the repository has not yet been made public.

---

## Configuration

### Installation Scopes Explained

When installing plugins, you choose a scope that determines where the plugin is available:

| Scope | Where Installed | Use Case |
|-------|-----------------|----------|
| **User** (default) | Your user settings | Personal use across all your projects |
| **Project** | `.claude/settings.json` | Shared with team—all collaborators get the plugin |
| **Local** | Your local repo config | Testing—only you, only this repo |

**Recommendation:** Use **User** scope for personal use. Use **Project** scope when you want your whole team to have Jerry available. When **Project** scope is selected, Jerry is added to `.claude/settings.json`, which is committed to version control — new team members have Jerry active automatically after cloning the repository.

### Project Setup (Optional)

Jerry uses project-based workflows for organizing work. To set up a project:

1. **Set the project environment variable:**

   ```bash
   # macOS/Linux
   export JERRY_PROJECT=PROJ-001-my-project

   # Windows PowerShell
   $env:JERRY_PROJECT = "PROJ-001-my-project"
   ```

2. **Create project structure:**

   ```bash
   # macOS/Linux
   mkdir -p projects/PROJ-001-my-project/.jerry/data/items

   # Windows PowerShell
   New-Item -ItemType Directory -Force -Path "projects\PROJ-001-my-project\.jerry\data\items"
   ```

The SessionStart hook will automatically load project context when you start Claude Code.

---

## Verification

### Check Plugin Installation

1. In Claude Code, run `/plugin`
2. Go to the **Installed** tab
3. Verify `jerry-framework` appears in the list

### Check for Errors

1. Run `/plugin`
2. Go to the **Errors** tab
3. Verify no errors related to `jerry-framework`

### Test a Skill

Run a simple skill to verify everything works:

```
/problem-solving
```

You should see the problem-solving skill activate with information about available agents.

> **Note:** `/problem-solving` requires an active project (`JERRY_PROJECT` environment variable set). If you skipped the Configuration section, use `/help` instead to verify skill availability without a project.

---

## Using Jerry

### Available Skills

After installation, these skills are available via slash commands:

| Skill | Command | Purpose |
|-------|---------|---------|
| Problem-Solving | `/problem-solving` | Research, analysis, architecture decisions |
| Work Tracker | `/worktracker` | Task and work item management |
| NASA SE | `/nasa-se` | Systems engineering processes (NPR 7123.1D) |
| Orchestration | `/orchestration` | Multi-phase workflow coordination |
| Architecture | `/architecture` | Design decisions and ADRs |
| Transcript | `/transcript` | Meeting transcript parsing |
| Adversary | `/adversary` | Adversarial quality reviews and tournament scoring |

### Example Usage

**Research a topic:**
```
/problem-solving research OAuth2 implementation patterns for Python
```

**Create a work item:**
```
/worktracker add "Implement user authentication"
```

**Make an architecture decision:**
```
/architecture create ADR for choosing PostgreSQL over SQLite
```

### Persistent Artifacts

All skill outputs are saved to files in your project:

| Output Type | Location |
|-------------|----------|
| Research | `docs/research/` |
| Analysis | `docs/analysis/` |
| Decisions (ADRs) | `docs/decisions/` |
| Reviews | `docs/reviews/` |
| Reports | `docs/reports/` |

These files survive context compaction and session boundaries, building your project's knowledge base over time.

---

## Troubleshooting

### Plugin Command Not Recognized

**Symptom:** `/plugin` command not found or doesn't work

**Solution:** Update Claude Code to the latest version:
- **macOS (Homebrew):** `brew upgrade claude-code`
- **npm:** `npm update -g @anthropic-ai/claude-code`

Plugin support requires Claude Code version 1.0.33 or later.

### Plugin Not Found After Adding Marketplace

**Symptom:** `/plugin install jerry-framework@jerry` returns "plugin not found"

**Solutions:**
1. Verify the marketplace was added: `/plugin marketplace list`
2. Check the path is correct and Jerry was cloned successfully
3. Refresh the marketplace: `/plugin marketplace update jerry`
4. Verify the manifest exists: `cat ~/plugins/jerry/.claude-plugin/plugin.json`
5. If you cloned to a non-standard directory name (not `jerry`), the `@jerry` suffix in the install command must match the directory name. For example, if you cloned to `~/plugins/jerry-framework`, use `/plugin install jerry-framework@jerry-framework`

### uv: command not found

**Symptom:** Hooks fail with "uv: command not found"

**Solution (macOS):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your terminal
```

**Solution (Windows):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Close and reopen PowerShell
```

If still not found, add to PATH manually:
- macOS: `export PATH="$HOME/.local/bin:$PATH"` (add to `~/.zshrc`)
- Windows: Add `%USERPROFILE%\.local\bin` to System PATH

### Skills Not Appearing

**Symptom:** Installed plugin but `/problem-solving` doesn't work

**Solutions:**
1. Check the **Errors** tab in `/plugin`
2. Clear the plugin cache:
   - macOS: `rm -rf ~/.claude/plugins/cache`
   - Windows: `Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\cache"`
3. Restart Claude Code
4. Reinstall the plugin: `/plugin uninstall jerry-framework@jerry` then `/plugin install jerry-framework@jerry`

### Path Issues on Windows

**Symptom:** "path not found" when adding marketplace

**Solutions:**
- Use forward slashes in Claude Code: `C:/Users/name/plugins/jerry`
- Or use short path: `~/plugins/jerry` (if using Git Bash paths)
- Avoid using backslashes or environment variables in the Claude Code command

### SSH Authentication Failed (Collaborators)

**Symptom:** `git clone git@github.com:geekatron/jerry.git` returns "Permission denied (publickey)"

**Causes:** SSH key not added to GitHub, passphrase not entered when prompted during `ssh -T`, key not loaded in ssh-agent, or collaborator invitation not accepted.

**Solutions:**
1. Verify your SSH key was added to GitHub: visit [github.com/settings/keys](https://github.com/settings/keys)
2. Test SSH connectivity: `ssh -T git@github.com` — if prompted for a passphrase, enter it; a successful response rules out key/auth issues
3. Confirm your key file exists: `ls ~/.ssh/id_ed25519.pub` (macOS) or `Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub"` (Windows)
4. If you have multiple SSH keys, ensure the correct one is loaded: `ssh-add -l`
5. Verify you accepted the collaborator invitation at github.com/notifications

### Repository Not Found (Collaborators)

**Symptom:** `git clone` returns "repository not found" or 404

**Solutions:**
1. Confirm you were added as a collaborator and accepted the invitation
2. Verify your GitHub username has access by visiting the repository URL in a browser while logged in
3. Try SSH connectivity test first: `ssh -T git@github.com` — must show your GitHub username

### Credential Helper Not Found (macOS PAT Users)

**Symptom:** `git credential-osxkeychain` returns "command not found" after running `git config --global credential.helper osxkeychain`

**Cause:** The osxkeychain helper ships with Apple's Git (Xcode Command Line Tools) but is not included with Git installed via conda, Homebrew's `git` formula on some configurations, nix, or MacPorts.

**Solution:** Use the `store` helper instead:
```bash
git config --global credential.helper store
```
The first time you run a git operation, enter your PAT when prompted — it will be saved to `~/.git-credentials` for future use.

> **Security note:** The `store` helper saves credentials in plaintext. For better security, install the Xcode Command Line Tools (`xcode-select --install`) to get the osxkeychain helper.

### Project Not Configured (`<project-required>` or `<project-error>`)

**Symptom:** Running `/problem-solving` or other skills shows XML-tagged output like `<project-required>` or `<project-error>` instead of the expected skill response.

**Cause:** The `JERRY_PROJECT` environment variable is not set, is set to a non-existent project, or the project directory structure is incomplete.

**Solutions:**
1. Set the environment variable: `export JERRY_PROJECT=PROJ-001-my-project` (macOS) or `$env:JERRY_PROJECT = "PROJ-001-my-project"` (Windows PowerShell)
2. Verify the project directory exists: `ls projects/$JERRY_PROJECT/` — it should contain `PLAN.md` and `WORKTRACKER.md`
3. If you haven't created a project yet, follow the Configuration section above
4. Use `/help` to verify Jerry is installed — this command works without a project configured

---

## For Developers

If you want to contribute to Jerry development, you'll need Python 3.11+ and [uv](https://docs.astral.sh/uv/).

### Development Setup

**macOS / Linux:**
```bash
git clone https://github.com/geekatron/jerry.git
cd jerry
make setup    # Installs deps + pre-commit hooks
make test     # Run test suite
```

**Windows (Git Bash or PowerShell):**
```bash
git clone https://github.com/geekatron/jerry.git
cd jerry
uv sync                        # Install dependencies
uv run pre-commit install      # Install pre-commit hooks
uv run pytest --tb=short -q    # Run test suite
```

> **Note:** Windows does not have `make` by default. Use the `uv run` commands directly. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full Make target equivalents table.

### Common Developer Commands

| Task | macOS/Linux | Windows / All Platforms |
|------|-------------|------------------------|
| First-time setup | `make setup` | `uv sync && uv run pre-commit install` |
| Run tests | `make test` | `uv run pytest --tb=short -q` |
| Run linters | `make lint` | `uv run ruff check src/ tests/ && uv run pyright src/` |
| Format code | `make format` | `uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/` |
| All pre-commit hooks | `make pre-commit` | `uv run pre-commit run --all-files` |

### Context Distribution (Bootstrap)

Jerry's behavioral rules live in `.context/` (canonical source) and are synced to `.claude/` via symlinks. After cloning, run the bootstrap:

```bash
uv run python scripts/bootstrap_context.py        # Set up symlinks
uv run python scripts/bootstrap_context.py --check # Verify sync
```

See [Bootstrap Guide](BOOTSTRAP.md) (located in the `docs/` directory) for platform-specific details.

### Architecture Overview

Jerry follows hexagonal architecture:

```
src/
├── domain/           # Pure business logic (no external deps)
├── application/      # Use cases (CQRS commands/queries)
├── infrastructure/   # Adapters (persistence, messaging)
└── interface/        # Primary adapters (CLI)
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines, Windows-specific notes, and coding standards.

---

## Uninstallation

### Remove the Plugin

```
/plugin uninstall jerry-framework@jerry
```

### Remove the Marketplace

```
/plugin marketplace remove jerry
```

### Delete Local Files (Optional)

**macOS/Linux:**
```bash
rm -rf ~/plugins/jerry
```

**Windows PowerShell:**
```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\plugins\jerry"
```

---

## Getting Help

- **GitHub Issues:** [github.com/geekatron/jerry/issues](https://github.com/geekatron/jerry/issues)
- **Documentation:** `docs/` directory in the repository
- **Claude Code Help:** Run `/help` in Claude Code

---

## License

Jerry Framework is open source under the [Apache License 2.0](../LICENSE).

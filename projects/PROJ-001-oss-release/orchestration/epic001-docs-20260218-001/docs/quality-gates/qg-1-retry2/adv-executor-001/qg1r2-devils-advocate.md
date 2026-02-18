# S-002 Devil's Advocate Report — QG-1 Retry 2

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | One-line verdict |
| [Prior Finding Resolution](#prior-finding-resolution) | Verification of 7 retry 1 findings |
| [New Findings](#new-findings) | Devil's Advocate: new failure modes |
| [Finding Detail](#finding-detail) | Expanded analysis per new finding |
| [Score Estimate](#score-estimate) | Range estimate |

---

## L0 Summary

The document has absorbed all 7 retry-1 findings correctly; two new Major issues remain — `ssh-keygen` is silently unusable on Windows editions lacking OpenSSH Client (Step 1 dies before the only OpenSSH warning appears), and the `ssh -T` verification step presents a passphrase prompt as an unexpected failure case for the majority of users who followed the document's own recommendation to set a passphrase.

---

## Prior Finding Resolution

| Finding ID | Status | Evidence |
|------------|--------|----------|
| DA-001-qg1r1-da | RESOLVED | Lines 405–424: osxkeychain pre-check block added with `git credential-osxkeychain 2>&1 \| head -1`, conditional `store` fallback path, and plaintext security note. Troubleshooting entry "Credential Helper Not Found (macOS PAT Users)" also added (lines 841–853). |
| DA-002-qg1r1-da | RESOLVED | Lines 302–317: Windows SSH agent tip now uses `if (Get-Service ssh-agent -ErrorAction SilentlyContinue)` guard, includes `Add-WindowsCapability` install path and Settings > Apps UI path, and explicitly notes absence on Home/LTSC editions. |
| DA-003-qg1r1-da | RESOLVED | Space-in-path warning added at three locations: macOS Step 2 (line 471), Windows Step 2 (lines 549–550 including `C:\plugins\` fallback for usernames with spaces), and Collaborator Step 4 (line 354). |
| DA-004-qg1r1-da | RESOLVED | ToC now lists Configuration (line 185) before Verification (line 186). Document body confirms Configuration section appears before Verification section. |
| DA-005-qg1r1-da | RESOLVED | Line 444: marketplace rationale sentence now reads "the scope you choose during `/plugin install`" — scope conflation with archive corrected. |
| DA-006-qg1r1-da | RESOLVED | Line 387: `repo` scope now described as "full access to private repositories you collaborate on (read and write)". Fine-grained PAT alternative with `Contents: Read-only` added for least-privilege path. |
| DA-007-qg1r1-da | RESOLVED | Line 607: rate-limit note added to Future section: "unauthenticated HTTPS clones may be subject to GitHub API rate limits during periods of high traffic. If you encounter rate-limiting errors, authenticating with a GitHub account resolves this." |

All 7 prior findings are RESOLVED. No re-raises warranted.

---

## New Findings

| ID | Severity | Finding | Impact |
|----|----------|---------|--------|
| DA-001-qg1r2-da | Major | `ssh-keygen` used at Windows Step 1 before any warning that OpenSSH Client may not be installed — command fails silently for affected users before the only OpenSSH warning appears | Windows Home/LTSC users hit an unexplained command error at Step 1 with no recovery path at that point |
| DA-002-qg1r2-da | Major | `ssh -T git@github.com` verification step (Collaborator Step 3) shows only one expected output; users who followed the recommended passphrase path will see an interactive passphrase prompt first — not documented, makes the step appear to fail | Users with passphrases (the majority, per the document's own recommendation) perceive a broken installation at the verification step |
| DA-003-qg1r2-da | Minor | Future section (lines 613–625) omits the space-in-path warning that appears in the Installation section; a user following the future path directly has no warning before the `/plugin marketplace add` command fails | Future-path users with spaces in their home directory path will hit the same path-spaces failure that was fixed in retry 1 |
| DA-004-qg1r2-da | Minor | Windows marketplace step (line 584) requires the user to supply a literal path (`C:/Users/YOUR_USERNAME/plugins/jerry`) with no guidance on how to resolve the literal value from the `$env:USERPROFILE` PowerShell variable used in Step 2 — the bridging step is missing | Users who followed Step 2 with `$env:USERPROFILE` will not know what literal string to substitute for `YOUR_USERNAME` without deducing it independently; the `echo $env:USERNAME` tip (line 589) is partial help but `YOUR_USERNAME` ≠ `USERNAME` on systems where the profile path differs |

---

## Finding Detail

### DA-001-qg1r2-da — ssh-keygen on Windows before OpenSSH warning (Major)

**Location:** Collaborator Installation > Step 1: Generate an SSH Key > Windows (PowerShell), lines 278–299 and Tip block lines 302–317.

**Failure scenario:**
A Windows Home user opens PowerShell, runs the pre-check at line 279 (`Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub"`). `Test-Path` is a PowerShell built-in — it succeeds (returns `False`). The user then runs `ssh-keygen -t ed25519 -C "your.email@example.com"` (line 285). On editions without OpenSSH Client, this returns:

```
ssh-keygen : The term 'ssh-keygen' is not recognized as the name of a cmdlet...
```

The only OpenSSH warning in the document is in the optional Tip block (lines 302–317), which is framed as "to avoid re-entering your passphrase each session" — an optional passphrase-caching step. A user who fails at `ssh-keygen` has no indication that the Tip block contains the relevant diagnosis or fix.

**Root cause:** The OpenSSH Client availability check was added to address the ssh-agent service (DA-002-qg1r1-da), but `ssh-keygen` is also part of OpenSSH Client and fails under the same conditions. The fix addressed the downstream symptom (ssh-agent) but not the upstream dependency (ssh-keygen itself).

**Exploit path:** Windows 10 Home and Windows LTSC editions ship without OpenSSH Client. The Windows 10 build 1809+ floor documented in the note covers the version floor, but not the edition exclusion.

**Suggested fix:** Add a pre-check for `ssh-keygen` availability at the top of the Windows Step 1 section, before the key generation command:

```powershell
# Verify OpenSSH Client is installed
if (-not (Get-Command ssh-keygen -ErrorAction SilentlyContinue)) {
    Write-Host "ssh-keygen not found. Install OpenSSH Client first:"
    Write-Host "  Settings > Apps > Optional Features > Add a feature > OpenSSH Client"
    Write-Host "Or via PowerShell (admin required):"
    Write-Host "  Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0"
    exit 1
}
```

---

### DA-002-qg1r2-da — ssh -T passphrase prompt not documented (Major)

**Location:** Collaborator Installation > Step 3: Verify SSH Access, lines 334–346.

**Failure scenario:**
The document recommends setting a passphrase (lines 253–255: "Enter a passphrase (recommended)"). A user who follows this recommendation and does NOT run the optional Keychain/agent tip will encounter the following when they run `ssh -T git@github.com` at Step 3:

```
Enter passphrase for key '/Users/username/.ssh/id_ed25519':
```

This prompt appears before the "You should see:" output. A user who has not seen this before will:

1. Not know whether to type something or press Enter.
2. If they type their passphrase and it is correct, see the expected success message — but only after the undocumented prompt.
3. If they press Enter (thinking it is interactive confirmation), receive `Permission denied (publickey)` — which is the exact error addressed in the SSH Authentication Failed troubleshooting entry.

The troubleshooting entry at line 822 does not mention "passphrase prompt not entered" as a cause of `Permission denied`. The only path offered is to re-verify that the public key was saved to GitHub — leading the user in the wrong direction.

**Compound risk:** The document actively steers users toward passphrase use ("recommended"), then presents a verification step that will behave unexpectedly for every user who follows that recommendation without also following the optional tip.

**Suggested fix:** Add a note after the "You should see:" block:

> **Note:** If you set a passphrase and did not run the Keychain/agent Tip above, you will see a passphrase prompt before this output. Enter your passphrase and press Enter — if the success message appears, your key is working correctly.

Add a passphrase cause to the SSH Authentication Failed troubleshooting entry.

---

### DA-003-qg1r2-da — Future section missing space-in-path warning (Minor)

**Location:** Future: Public Repository Installation > Step 2: Clone Jerry (HTTPS), lines 613–625.

**Observation:** The current Installation section contains an "Important" callout about path spaces at macOS Step 2 (line 471) and Windows Step 2 (lines 549–550). The Collaborator Installation section has the same warning at Step 4 (line 354). The Future section's Step 2 clone commands (lines 615–622) contain no equivalent warning.

**Scope context:** The Future section is explicitly marked as "not yet applicable." However, the text states "When Jerry becomes publicly available...these simplified instructions will apply." A user who arrives at this section when Jerry goes public — without having read the current collaborator path — will have no warning that spaces in `~/plugins/jerry` or `$env:USERPROFILE\plugins\jerry` will break the subsequent `/plugin marketplace add` command.

**Suggested fix:** Add the same "Important" callout to Future section Step 2:

> **Important:** The clone path must not contain spaces. The Claude Code `/plugin marketplace add` command does not support paths with spaces. The recommended `~/plugins/` path is safe.

---

### DA-004-qg1r2-da — Windows marketplace path resolution gap (Minor)

**Location:** Windows Installation > Step 4: Add the Local Marketplace, lines 579–589.

**Observation:** The document uses `$env:USERPROFILE` as the PowerShell path prefix throughout Step 2 (e.g., `"$env:USERPROFILE\plugins\jerry"`). Step 4 switches to a different form requiring a literal path:

```
/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry
```

The document notes "Replace `YOUR_USERNAME` with your actual Windows username" and adds "You can find your username by running `echo $env:USERNAME` in PowerShell." However, `$env:USERNAME` returns the login name (e.g., `johndoe`), while `$env:USERPROFILE` returns the full profile path (e.g., `C:\Users\johndoe`). These are congruent in the default case, but diverge on:

- Domain-joined machines where the profile path may be `C:\Users\DOMAIN\johndoe` or a redirected path
- Systems where the profile was moved (e.g., `D:\Users\johndoe`)
- OneDrive-known-folder-move scenarios where `Documents` and Desktop are redirected

The hint `echo $env:USERNAME` → `YOUR_USERNAME` → `C:/Users/YOUR_USERNAME/plugins/jerry` works for default setups but silently produces a wrong path in non-default environments.

**Suggested fix:** Replace the current "Tip" with a command that produces the exact string needed:

> **Tip:** To get the exact path, run `(Get-Item "$env:USERPROFILE\plugins\jerry").FullName` in PowerShell. Replace backslashes with forward slashes before pasting into Claude Code.

---

## Score Estimate

**Estimated range: 0.87 – 0.91**

Rationale:

- All 7 prior findings resolved: substantive improvement over retry 1 (0.8300).
- DA-001-qg1r2-da is a real functional failure on a defined user population (Windows Home/LTSC). The OpenSSH Client check was partially added but only for ssh-agent, not for ssh-keygen itself. This is a gap in the applied fix logic.
- DA-002-qg1r2-da is a perception failure that compounds the document's own recommendation. It does not prevent installation from succeeding, but it reliably creates a "broken" impression at the verification step for the majority of users who follow the passphrase recommendation.
- DA-003 and DA-004 are Minor — limited scope (future section not yet live; Windows non-default profile paths are edge cases).
- The document is otherwise well-structured, thorough, and internally consistent. The bulk of prior weaknesses are genuinely resolved.
- Two Major findings prevent reaching the 0.92 threshold. Both are addressable with targeted additions of 2–4 lines each, not structural rewrites.

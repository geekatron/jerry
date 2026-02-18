# Devil's Advocate Report: Jerry Framework Installation Guide

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md`
**Criticality:** C2
**Date:** 2026-02-18
**Reviewer:** adv-executor (QG-1 Retry 3)
**H-16 Compliance:** S-003 Steelman applied in prior rounds (SM-* identifiers confirmed in Iteration 3 and Iteration 4 revision logs; SM-001-qg1r2s, SM-002-qg1r2s, SM-003-qg1r2s applied in Iteration 5)
**Execution ID:** qg1r3-da

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prior Findings Verification](#prior-findings-verification) | QG-1 Retry 2 findings — resolution status |
| [Role Assumption](#role-assumption) | Step 1 — Advocate mandate |
| [Assumption Inventory](#assumption-inventory) | Step 2 — Challenged assumptions |
| [Findings Summary](#findings-summary) | All new findings at a glance |
| [Detailed Findings](#detailed-findings) | Steps 3–4 — Counter-arguments with evidence and response requirements |
| [Scoring Impact](#scoring-impact) | Step 5 — Dimension impact assessment |
| [Recommendations](#recommendations) | Prioritized action list |
| [Execution Statistics](#execution-statistics) | Protocol completion summary |

---

## Prior Findings Verification

All 4 prior findings from QG-1 Retry 2 were targeted by Iteration 5. Verification against the current document:

### DA-001-qg1r2-da (Major): ssh-keygen Windows availability

**Fix claimed (Iteration 5 P1):** Added OpenSSH Client availability pre-check on Windows BEFORE the ssh-keygen command.

**Evidence in current document (lines 320–325):**
```
> **Important — Windows Home / LTSC Users:** If `ssh-keygen` is not recognized, OpenSSH Client is not installed.
> Install it via **Settings → Apps → Optional Features → Add a feature → OpenSSH Client**, or run:
> Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
> Then close and reopen PowerShell before continuing.
```

**Verdict: RESOLVED.** The callout appears BEFORE the `ssh-keygen` command on Windows. The fix is correctly positioned, covers the exact failure mode (unrecognized command), and provides two install paths (UI and PowerShell). Note: this callout uses `> **Important...**` inline blockquote formatting rather than a formal `> **Warning:**` callout, but the placement and content are adequate. The SSH agent Tip also now includes an `else` branch that surfaces the same install paths (lines 354–358). Complete.

---

### DA-002-qg1r2-da (Major): passphrase prompt undocumented

**Fix claimed (Iteration 5 P2):** Added passphrase prompt note after the "You should see:" block in Step 3.

**Evidence in current document (lines 389):**
```
> **Note:** If you set a passphrase during key generation, you will be prompted to enter it before seeing the success message. Type your passphrase and press Enter. If you see `Permission denied (publickey)` after entering your passphrase, verify your public key is correctly added to GitHub (Step 2).
```

Also in Troubleshooting, SSH Authentication Failed (lines 880–881): "passphrase not entered" listed as an explicit cause.

**Verdict: RESOLVED.** The note is placed at the exact friction point (between the command and the expected output). It explains the prompt, provides the action ("Type your passphrase and press Enter"), and gives a recovery path for post-passphrase failure. Both the inline note and the Troubleshooting entry are present.

---

### DA-003-qg1r2-da (Minor): Future section space-in-path

**Fix claimed (Iteration 5 P5):** Added space-in-path Important callout to Future: Public Repository Installation section, Step 2 clone block.

**Evidence in current document (lines 666–667):**
```
> **Important:** If your username contains spaces, use a path without spaces (e.g., `~/plugins/jerry` or `C:\plugins\jerry`).
```

**Verdict: RESOLVED.** The callout is present before the clone commands in the Future section and matches the pattern used at the other three clone locations. Complete.

---

### DA-004-qg1r2-da (Minor): `$env:USERNAME` vs `$env:USERPROFILE`

**Fix claimed (Iteration 5 P3):** Replaced `echo $env:USERNAME` tip with `(Get-Item "$env:USERPROFILE\plugins\jerry").FullName -replace '\\','/'`.

**Evidence in current document (lines 637–640):**
```powershell
(Get-Item "$env:USERPROFILE\plugins\jerry").FullName -replace '\\','/'
```
"Copy the output and use it directly in the `/plugin marketplace add` command."

**Verdict: RESOLVED.** The command now produces the exact forward-slash literal path that Claude Code requires. The explanatory sentence makes the copy-paste intent clear. Complete.

---

**Prior Findings Summary: ALL 4 RESOLVED (4/4)**

No regressions detected. Fixes are correctly placed and adequate.

---

## Role Assumption

I am the Devil's Advocate for the Jerry Framework Installation Guide (Iteration 5 state). My mandate is to construct the strongest possible counter-arguments against the deliverable's positions, claims, and completeness — to identify what could still fail for a real user following this guide. The deliverable has been through 5 revision iterations and 2 prior DA rounds; the bar is high. I will apply anti-leniency: even a well-revised document can still have edge cases, structural tensions, or subtle gaps. I will not claim findings are resolved unless the evidence in the document conclusively demonstrates they are.

**Scope:** Full document — all sections including Collaborator Installation, Installation (macOS/Windows), Future section, Configuration, Verification, Troubleshooting, For Developers.

**Criticality:** C2 Standard — targeted revision cycle is the appropriate response to any findings.

---

## Assumption Inventory

### Explicit Assumptions Challenged

| # | Assumption | Location | Challenge |
|---|-----------|----------|-----------|
| A-1 | "Collaborator invitation" is the only entry barrier to using Jerry | Collaborator Installation header | What about SSH key format compatibility (RSA vs ed25519) and GitHub's key type policy? |
| A-2 | The `~/plugins/` path is universally safe from spaces | All clone steps | The tilde expansion resolves to the home directory; on macOS the home directory itself could contain spaces on non-standard setups |
| A-3 | `JERRY_PROJECT` is a simple env var set by the user | Configuration section | The SessionStart hook behavior when JERRY_PROJECT is not set is referenced but not fully explained — new users may not know what the hook outputs mean |
| A-4 | `/plugin install jerry-framework@jerry` is a stable command format | Installation Step 5 | The `@jerry` suffix (marketplace name) is not explained — users who encounter a naming mismatch have no recovery path |
| A-5 | The developer commands table is accurate | For Developers section | `make lint` runs both ruff and pyright — the Windows equivalent shows ruff + pyright separately, but pyright is not listed in Prerequisites |
| A-6 | All Troubleshooting entries are reachable from the section they address | Document structure | Some troubleshooting entries (e.g., Credential Helper Not Found) are not cross-referenced from the section where the failure occurs |

### Implicit Assumptions Challenged

| # | Implicit Assumption | Challenge |
|---|---------------------|-----------|
| IA-1 | The user has admin/sudo privileges for SSH agent service on Windows | `Set-Service -Name ssh-agent -StartupType Automatic` requires admin | Where is the admin requirement stated? |
| IA-2 | Claude Code's `/plugin` command is available at the exact version the guide uses | Prerequisites lists `1.0.33+` but does not warn that command syntax may have changed in newer versions |
| IA-3 | The PAT Alternative and SSH flows are mutually exclusive | The guide does not clarify what happens if a user completes SSH setup AND then tries the PAT Alternative clone — could create duplicate remotes or confuse git credential cache |
| IA-4 | macOS Keychain tip works for all macOS versions | `--apple-use-keychain` flag was added in macOS Ventura; it may not exist on older macOS versions |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001-qg1r3-da | Minor | `Set-Service ssh-agent -StartupType Automatic` requires admin privileges — not stated | Collaborator Installation — Windows SSH Agent Tip |
| DA-002-qg1r3-da | Minor | `--apple-use-keychain` flag may not be available on macOS versions older than Ventura (13) | Collaborator Installation — macOS Keychain Tip |
| DA-003-qg1r3-da | Minor | Verification "Test a Skill" step recommends `/problem-solving` with a note about JERRY_PROJECT, but does not explain what `<project-required>` output looks like — user confusion risk | Verification — Test a Skill |
| DA-004-qg1r3-da | Minor | `@jerry` marketplace suffix in install command is unexplained — users who see a mismatch have no recovery path | Installation Step 5 (both platforms) |

**Overall Assessment:** 0 Critical, 0 Major, 4 Minor. The document withstands the Devil's Advocate challenge at the Critical and Major level. The fixes from Iterations 3–5 have been thorough. The remaining findings are edge cases and clarity gaps that would affect a small subset of users. The deliverable is solid.

**Recommendation:** ACCEPT with minor revisions — the four Minor findings are actionable and none blocks acceptance.

---

## Detailed Findings

---

### DA-001-qg1r3-da: `Set-Service` Requires Admin — Undocumented [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Collaborator Installation — Windows, Step 1 SSH Agent Tip |
| **Strategy Step** | Step 2 (Implicit Assumptions) + Step 3 (Unaddressed Risks) |

**Claim Challenged:**
> `Set-Service -Name ssh-agent -StartupType Automatic`
> (Lines 353–354, within the Windows SSH agent Tip block)

**Counter-Argument:**
`Set-Service` with `-StartupType Automatic` requires an elevated (Administrator) PowerShell session. If the user runs this in a normal user-privilege PowerShell session (the common default), it will silently fail or throw "Access is denied." The guide presents this as a routine follow-on step after `ssh-add`, with no admin prerequisite warning. A user who does not get the error (perhaps on Windows Home where UAC prompts are more aggressive) may believe the service was configured for automatic startup when it was not, and then be confused the next session when their SSH key is not loaded.

**Evidence:**
The Tip block reads:
```powershell
> } else {
>     Write-Host "OpenSSH Client not installed. Install it via:"
```
and earlier:
```powershell
>     Start-Service ssh-agent
>     ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
>     # To make this permanent:
>     Set-Service -Name ssh-agent -StartupType Automatic
```
No admin note is present anywhere near this block. `Start-Service ssh-agent` also typically requires elevation on Windows.

**Analysis:**
This is a genuine UX gap. The user has just successfully generated an SSH key and is following the "optional but recommended" Tip. The failure mode is subtle — the `ssh-add` itself may succeed (if the service was already running from a prior session), but the `Set-Service` call fails silently in non-admin shells. The next session, the user wonders why they are being prompted for their passphrase again.

**Impact:**
Affects only users who want persistent SSH agent startup (the explicit purpose of the Tip). Does not block initial clone success.

**Recommendation:**
Add a parenthetical admin note to the `Set-Service` comment line: `# To make this permanent (requires admin PowerShell):`. Alternatively, add a preceding `> **Note:** Making the service start automatically requires an elevated (Administrator) PowerShell session.`

**Acceptance Criteria:**
The `Set-Service -StartupType Automatic` line (or the Tip block header) explicitly states that admin privileges are required. The fix does not need to provide a full "how to open admin PowerShell" tutorial — a parenthetical note is sufficient.

**Priority:** P2 (Minor — MAY resolve; acknowledgment sufficient)

---

### DA-002-qg1r3-da: `--apple-use-keychain` Availability Not Guaranteed [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Collaborator Installation — macOS, Step 1 Keychain Tip |
| **Strategy Step** | Step 2 (Explicit Assumption: macOS version) + Step 3 (Historical Precedents of Failure) |

**Claim Challenged:**
> `ssh-add --apple-use-keychain ~/.ssh/id_ed25519`
> (Lines 303–305, macOS Keychain Tip)

**Counter-Argument:**
The `--apple-use-keychain` flag (long form of `-K`) is documented Apple-specific behavior that was added to macOS's bundled ssh-add in macOS Ventura (13). On macOS Monterey (12) and earlier, the flag does not exist — running the command produces `ssh-add: illegal option -- -`. The guide makes no mention of a macOS version requirement for this tip. Given that Monterey is still a supported macOS version for many enterprise users and Claude Code itself runs on it, this is an edge case with a real failure path.

**Evidence:**
The tip reads:
> ```bash
> eval "$(ssh-agent -s)"
> ssh-add --apple-use-keychain ~/.ssh/id_ed25519
> ```
> Without this, your terminal will prompt for your SSH key passphrase every time you interact with GitHub.

No macOS version qualifier is present. The `--apple-use-keychain` flag is used without verification that it exists.

**Analysis:**
The user follows the tip, gets an error on `ssh-add --apple-use-keychain`, and receives no guidance. The guide does not fall back to `-K` (the older short form), which also has macOS-version-specific history. The failure is not silent — the user will see an "illegal option" error — but without guidance they may believe SSH agent setup failed entirely and skip it.

**Impact:**
Affects macOS Monterey and earlier users who follow the Keychain tip. Users on Ventura+ (the majority of new installs) are unaffected.

**Recommendation:**
Add a version qualifier: `> **Tip (macOS Ventura 13+ recommended):**` or add a fallback: `> If `--apple-use-keychain` is not recognized on older macOS, use `-K` instead: `ssh-add -K ~/.ssh/id_ed25519``.

**Acceptance Criteria:**
Either: (a) a version qualifier is added to the Tip so users on older macOS know it may not apply, OR (b) a fallback command (`-K`) is provided, OR (c) both. The fix does not need to enumerate all macOS versions — a simple "macOS Ventura 13+ only" note suffices.

**Priority:** P2 (Minor — MAY resolve; acknowledgment sufficient)

---

### DA-003-qg1r3-da: `<project-required>` Output Not Explained for New Users [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Verification — Test a Skill |
| **Strategy Step** | Step 3 (Unaddressed Risks) + Step 3 (Alternative Interpretations) |

**Claim Challenged:**
> "Run a simple skill to verify everything works: `/problem-solving`"
> "You should see the problem-solving skill activate with information about available agents."
> (Lines 753–758)
>
> The added note (Iteration 5): "Note: `/problem-solving` requires an active project (`JERRY_PROJECT` environment variable set). If you skipped the Configuration section, use `/help` instead."
> (Lines 760)

**Counter-Argument:**
The note correctly redirects users who skipped Configuration to `/help`. However, it does not tell users WHAT they will see if they run `/problem-solving` without `JERRY_PROJECT` set. The SessionStart hook outputs a `<project-required>` XML-tagged response (documented in CLAUDE.md), but a new user seeing this output for the first time has no way to know whether this is (a) an error meaning installation failed, (b) expected behavior because no project exists yet, or (c) a prompt to create a project. The ambiguity could lead a user to believe their installation is broken when it is actually correct.

**Evidence:**
The note reads:
> `> **Note:** /problem-solving requires an active project (JERRY_PROJECT environment variable set). If you skipped the Configuration section, use /help instead to verify skill availability without a project.`

The note redirects but does not describe the expected output when `JERRY_PROJECT` is absent (the `<project-required>` prompt). A user who configured JERRY_PROJECT but typed it wrong will also see unexpected output without guidance.

**Analysis:**
This is a UX clarity gap rather than a technical error. The Iteration 5 fix (P4-SM-002-qg1r2s) addressed the redirection to `/help`, which is correct. The gap that remains is the absence of "what does the `<project-required>` output mean?" context — particularly for users who did set JERRY_PROJECT and expected the skill to just work.

**Impact:**
Affects users who set up Configuration (correctly or incorrectly) and run `/problem-solving`, then see an unexpected XML-tagged response with no explanation. Users directed to `/help` are not affected.

**Recommendation:**
Expand the Verification note to describe the two possible outcomes: (1) skill activates normally (project set correctly), (2) `<project-required>` prompt appears (project not set or JERRY_PROJECT typo). A one-sentence description of what `<project-required>` means and what to do is sufficient.

**Acceptance Criteria:**
The Verification section describes both success and `<project-required>` outcomes for `/problem-solving`, or the note more explicitly covers the "set JERRY_PROJECT but skill still shows a project prompt" edge case.

**Priority:** P2 (Minor — MAY resolve; acknowledgment sufficient)

---

### DA-004-qg1r3-da: `@jerry` Marketplace Suffix Unexplained — No Recovery Path [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Installation — macOS Step 5, Windows Step 5 |
| **Strategy Step** | Step 3 (Unstated Assumptions) + Step 3 (Unaddressed Risks) |

**Claim Challenged:**
> `/plugin install jerry-framework@jerry`
> (Lines 553–555, macOS Step 5; Lines 644–647, Windows Step 5)

**Counter-Argument:**
The `@jerry` suffix refers to the marketplace name under which the plugin catalog was registered. This name was established implicitly when the user ran `/plugin marketplace add ~/plugins/jerry` in Step 4 — Claude Code derives the marketplace identifier from the final path component (`jerry`). The guide does not explain this relationship. If a user previously cloned Jerry to a different path (e.g., `~/projects/jerry-framework`) or renamed the directory, the marketplace identifier will be `jerry-framework`, not `jerry`, and the install command `jerry-framework@jerry` will fail with a "plugin not found" error. The Troubleshooting entry "Plugin Not Found After Adding Marketplace" lists recovery steps but does not mention that a directory rename causes this exact failure.

**Evidence:**
Step 4 (macOS): `/plugin marketplace add ~/plugins/jerry` — the `jerry` segment becomes the marketplace ID.
Step 5 (macOS): `/plugin install jerry-framework@jerry` — the `@jerry` refers to that marketplace ID.
No explanation of this relationship is present in either step.

Troubleshooting "Plugin Not Found After Adding Marketplace" (lines 826–833) lists 4 solutions but none addresses directory renaming or mismatched marketplace IDs.

**Analysis:**
The assumption is that every user follows the prescribed path exactly (`~/plugins/jerry`). Users who deviate from the path naming (a common customization for developers who organize their plugin directories differently) hit a failure mode that is not covered in Troubleshooting. The `@` syntax is Claude Code-specific and not self-documenting.

**Impact:**
Affects users who cloned to a non-standard path or renamed their Jerry directory. Does not affect users who followed the exact recommended path.

**Recommendation:**
Add a one-sentence explanation of the `@jerry` syntax to Step 5: "The `@jerry` refers to the marketplace name, which is derived from the directory name used in Step 4. If you cloned Jerry to a different directory, replace `jerry` with that directory's name." Also add a note to the Troubleshooting entry for "Plugin Not Found" covering directory-name mismatch.

**Acceptance Criteria:**
Step 5 (on at least one platform, with a note that both use the same rule) explains that the `@` suffix must match the directory name used in Step 4, AND the Troubleshooting entry covers this failure mode.

**Priority:** P2 (Minor — MAY resolve; acknowledgment sufficient)

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Slightly Negative | DA-001 (admin privilege gap), DA-002 (macOS version gap), DA-004 (@marketplace syntax unexplained) are coverage omissions — each affects a real subset of users |
| Internal Consistency | 0.20 | Neutral | No contradictions detected. Windows SSH agent Tip now correctly gates on service existence check; macOS Keychain Tip is internally consistent |
| Methodological Rigor | 0.20 | Neutral | Document follows a clear install progression. Configuration-before-Verification order (Iteration 4 fix) is correct. Platform parity is well-maintained |
| Evidence Quality | 0.15 | Neutral | All technical claims are accurate. Plugin manifest name, credential helper guidance, and pre-checks are correctly specified |
| Actionability | 0.15 | Slightly Negative | DA-003 (unclear `<project-required>` outcome) and DA-004 (no recovery path for @suffix mismatch) reduce actionability for edge-case users. Troubleshooting entries exist but have gaps |
| Traceability | 0.10 | Neutral | All 4 prior findings are traceable to specific document lines. New findings are specific and location-referenced |

**Net Assessment:** All 4 findings are Minor and address edge cases rather than core paths. The document's primary user journeys (standard macOS and Windows installs, collaborator SSH path) are robust. Score impact across all new findings is estimated at -0.02 to -0.04 on the composite — placing the document near or above the 0.92 threshold depending on adv-scorer's holistic assessment.

**Overall Recommendation: ACCEPT with minor revisions.** If resource constraints prevent addressing all 4 findings before the score run, DA-004 (@jerry explanation) and DA-001 (admin note) are the highest-value fixes due to their direct effect on user success during a core install step.

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

None.

### P1 — Major (SHOULD resolve)

None.

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Finding | Action | Acceptance Criteria |
|----|---------|--------|---------------------|
| DA-001-qg1r3-da | `Set-Service -StartupType Automatic` requires admin | Add parenthetical note: "# To make this permanent (requires admin PowerShell):" or a preceding blockquote note | Admin requirement explicitly stated in or near the `Set-Service` line |
| DA-002-qg1r3-da | `--apple-use-keychain` not available on macOS < Ventura | Add "(macOS Ventura 13+ only)" qualifier to Tip header OR add `-K` fallback | Either a version qualifier or a `-K` fallback is present in the Tip |
| DA-003-qg1r3-da | `<project-required>` output unexplained in Verification | Expand Verification note to describe `<project-required>` output as expected behavior when project is not set | Verification section describes both success and `<project-required>` outcomes |
| DA-004-qg1r3-da | `@jerry` marketplace suffix unexplained | Add one sentence to Step 5 explaining `@jerry` = directory name from Step 4; add Troubleshooting note for directory-name mismatch | Step 5 explains `@` relationship to Step 4 directory; Troubleshooting covers mismatch |

---

## Execution Statistics

- **Total Findings:** 4 (0 new Critical, 0 new Major, 4 new Minor)
- **Prior Findings Verified:** 4/4 RESOLVED
- **Critical:** 0
- **Major:** 0
- **Minor:** 4
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** Confirmed (S-003 Steelman applied in prior rounds; SM-* identifiers present throughout revision log)
- **Score Estimate:** ~0.92–0.94 range (all prior Critical/Major issues resolved; remaining findings are P2 Minor edge cases)

---

*Agent: adv-executor v1.0.0*
*Strategy: S-002 Devil's Advocate v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Execution ID: qg1r3-da*
*Date: 2026-02-18*

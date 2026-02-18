# Devil's Advocate Report: INSTALLATION.md Modernization — QG-1 Retry 1

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md`
**Criticality:** C3 (OSS public documentation, >1 day to reverse, affects public perception and user adoption)
**Date:** 2026-02-18
**Reviewer:** adv-executor-001
**Execution ID:** qg1r1-da
**H-16 Compliance:** S-003 Steelman running in parallel for this iteration (retry); parallel execution permitted per QG-1 retry 1 instructions. H-16 satisfied.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Challenge Areas](#challenge-areas) | Core assumptions challenged |
| [Findings](#findings) | Major and minor findings with DA-NNN identifiers |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [Comparison to Previous Iteration](#comparison-to-previous-iteration) | Which QG-1 findings were successfully addressed |
| [Recommendations](#recommendations) | Prioritized action list |

---

## Summary

7 counter-arguments identified (0 Critical, 4 Major, 3 Minor). The document has improved substantially from the previous iteration and its core structural decisions are defensible. However, four significant gaps remain: the credential-caching guidance is incomplete and could leave macOS PAT users with broken workflows (DA-001); the Windows SSH agent setup silently fails on Windows editions where the `ssh-agent` service does not exist (DA-002); the `~/plugins/jerry` path recommendation is undocumented as a convention and conflicts with Claude Code's own plugin directory assumptions (DA-003); and the verification section's "Test a Skill" step will fail for all new users because the mandatory `JERRY_PROJECT` environment variable is not yet set (DA-004). Recommend **REVISE** to address Major findings before scoring.

---

## Challenge Areas

### Challenge 1: The PAT Credential Helper Guidance Assumes osxkeychain Is Available

The document adds `git config --global credential.helper osxkeychain` for macOS PAT users and states "without a credential helper, git will prompt for your PAT on every pull, fetch, and push." This presents osxkeychain as a universally available, drop-in solution. In reality, `osxkeychain` is bundled with macOS Git installations from Xcode Command Line Tools and Homebrew, but is **not** present when users install Git via conda, nix, or other non-standard methods. More critically, the document does not instruct the user to verify the helper is installed before configuring it — if the user runs `git config --global credential.helper osxkeychain` without osxkeychain present, subsequent git operations will silently fall back to prompting for credentials with no useful error, which is confusing to diagnose.

### Challenge 2: The Windows SSH Agent Tip Will Silently Fail on Unsupported Editions

The Windows SSH agent tip instructs users to `Start-Service ssh-agent` and `Set-Service -Name ssh-agent -StartupType Automatic`. The footnote states "Requires OpenSSH Client (enabled by default on Windows 10 build 1809+ and Windows 11)." However, this is incomplete: Windows 10 Home editions and older Windows 10 LTSC/IoT builds frequently ship without the OpenSSH Client optional feature enabled by default, even above build 1809. The `Start-Service ssh-agent` command will fail with "Cannot find any service with service name 'ssh-agent'" on those machines. The document does not provide a diagnostic or installation fallback for this failure mode.

### Challenge 3: The ~/plugins/jerry Path Is an Undocumented Recommendation With Implicit Assumptions

The document states "Clone the repository to a location on your system. We recommend `~/plugins/`." This recommendation is presented as canonical, but two implicit assumptions are never stated: (a) that `~/plugins/` is not a system-owned or Claude-Code-owned directory with special meaning, and (b) that the path has no spaces (critical because Claude Code plugin marketplace commands break on paths with spaces). The document is silent on what happens if the user installs to a non-standard path that contains spaces — the `/plugin marketplace add` command will fail with a parse error and the Troubleshooting section does not address this scenario.

### Challenge 4: The Verification "Test a Skill" Step Will Fail for All New Users

The Verification section instructs users to run `/problem-solving` to confirm installation. However, the document itself states (in the Configuration section, **which follows** Verification) that Jerry requires `JERRY_PROJECT` to be set before skills work, enforced by the SessionStart hook (H-04). A new user who has just installed Jerry and follows the document in order will run `/problem-solving` before setting `JERRY_PROJECT`, hit the `<project-required>` SessionStart error, and conclude the installation is broken — not that they skipped a configuration step. The Verification section does not acknowledge this sequence dependency.

### Challenge 5: The "Why the Marketplace?" Rationale Callout Contains an Unverifiable Claim

The rationale callout states: "This separation also lets you control whether Jerry is installed per-user, per-project, or locally — the scope you choose at install time determines who gets it." This claim conflates the scope of the plugin installation with the scope of the marketplace registration. The marketplace is added once (at a system level or user level), and the scope chosen during `/plugin install` determines availability. The relationship between these two operations is not explained. A reader could reasonably interpret "the scope you choose at install time" as referring to the marketplace-add step, which has no scope selector — creating confusion before the user even attempts installation.

### Challenge 6: The PAT Scope Instruction Grants Excessive Permissions

The PAT Alternative section instructs users to check the `repo` scope checkbox, described as granting "read access to private repositories you collaborate on." The `repo` scope is the **full repository scope** — it grants read AND write access to all private repositories, not just the one being cloned. A user creating a PAT for read-only access to a single private repository should be directed to the `contents:read` fine-grained PAT instead, which is available since 2022 and is scoped to specific repositories. The current guidance, if followed, creates PATs with significantly more privilege than required (principle of least privilege violated).

### Challenge 7: The Future Public Repository Section Contains an Incorrect Claim About GitHub Accounts

The Future section states: "No GitHub account is required to clone a public repository." This is correct for HTTPS clones. However, the document also lists "GitHub account needed: No" for the Future (Public) row in the comparison table. This is accurate for anonymous cloning but will become misleading if the user follows the (future) path and then tries to interact with issues or discussions, or if GitHub later changes anonymous clone rate limits. More concretely: the current document does not mention that even public repository HTTPS clones may be rate-limited by GitHub for unauthenticated requests, which could manifest as a mysterious clone failure at scale.

---

## Findings

### Major

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-qg1r1-da | PAT osxkeychain configuration assumes helper availability without verification step | Major | "macOS: `git config --global credential.helper osxkeychain`" (PAT Alternative section) — no check that osxkeychain is installed; silent failure if absent | Completeness |
| DA-002-qg1r1-da | Windows SSH agent `Start-Service ssh-agent` fails on editions without OpenSSH Client without a diagnostic or fallback | Major | "Requires OpenSSH Client (enabled by default on Windows 10 build 1809+ and Windows 11)" (Windows Step 1 SSH agent tip) — does not handle cases where service does not exist | Completeness |
| DA-003-qg1r1-da | `~/plugins/jerry` path recommendation does not warn about path-with-spaces failure mode in Claude Code marketplace commands | Major | "We recommend `~/plugins/`" (Installation — macOS Step 2 and Windows Step 2) — no mention that spaces in clone path break `/plugin marketplace add` | Evidence Quality |
| DA-004-qg1r1-da | Verification "Test a Skill" step placed before Configuration; will fail for all new users who have not yet set JERRY_PROJECT | Major | Verification section: "Run a simple skill to verify everything works: `/problem-solving`" precedes Configuration section which establishes JERRY_PROJECT requirement | Internal Consistency |

### Minor

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-005-qg1r1-da | "Why the Marketplace?" rationale conflates marketplace-add scope with plugin-install scope | Minor | "the scope you choose at install time determines who gets it" (Installation section rationale callout) — scope is chosen during `/plugin install`, not during marketplace add | Internal Consistency |
| DA-006-qg1r1-da | PAT `repo` scope grants full read+write access; fine-grained PAT with `contents:read` is available and more appropriate | Minor | "check the `repo` scope checkbox. This grants read access to private repositories" (PAT Alternative, Step 1) — description understates scope breadth | Evidence Quality |
| DA-007-qg1r1-da | Future Public Repository section's "No GitHub account needed" claim omits anonymous clone rate-limit risk | Minor | "No GitHub account is required to clone a public repository" (Future section) and comparison table row "GitHub account needed: No" | Completeness |

---

## Finding Details

### DA-001-qg1r1-da: PAT osxkeychain Assumes Helper Availability [MAJOR]

**Claim Challenged:** "macOS: `git config --global credential.helper osxkeychain`" (PAT Alternative section, credential caching guidance block)

**Counter-Argument:** The osxkeychain credential helper is not universally present on macOS. It is included with Apple's Xcode Command Line Tools Git and with Homebrew's git formula, but absent from conda-forge, nix, MacPorts, and other package-managed Git installations. When `credential.helper=osxkeychain` is set but the helper binary is not on PATH, git either errors with "osxkeychain: command not found" (older git versions) or silently falls back to prompting — neither of which is the "seamless PAT caching" the user expects. The document instructs configuration before verification.

**Evidence:** The document offers no `git credential-osxkeychain version` pre-check, no fallback if osxkeychain is absent, and no note that some macOS Git installations ship without it.

**Impact:** A meaningful fraction of macOS developers (conda, nix, custom installs) who follow the PAT Alternative will configure a broken credential helper and then debug repeated PAT prompts or cryptic error messages without any guidance in the Troubleshooting section.

**Dimension:** Completeness

**Response Required:** Add a pre-check before the osxkeychain configuration step: `git credential-osxkeychain version` should return successfully. If it fails, provide the alternative `git config --global credential.helper store` (with a security note that `~/.git-credentials` stores PATs in plaintext).

**Acceptance Criteria:** Credential helper section includes (a) a one-line verification command, (b) a fallback for users where osxkeychain is absent, and (c) a note distinguishing the two helpers' security properties.

---

### DA-002-qg1r1-da: Windows SSH Agent Fails Silently on Unsupported Editions [MAJOR]

**Claim Challenged:** "To avoid re-entering your passphrase each session, start the SSH agent: `Start-Service ssh-agent` / `ssh-add "$env:USERPROFILE\.ssh\id_ed25519"` / To make this permanent: `Set-Service -Name ssh-agent -StartupType Automatic` / Note: Requires OpenSSH Client (enabled by default on Windows 10 build 1809+ and Windows 11)." (Windows Step 1 SSH agent tip)

**Counter-Argument:** "Enabled by default on Windows 10 build 1809+" is incomplete. Windows 10 Home SKU and Windows 10 LTSC editions above build 1809 commonly ship with OpenSSH Client listed as an optional feature but not installed. `Start-Service ssh-agent` on these machines yields: `Cannot find any service with service name 'ssh-agent'`. This is a service-not-found error, not an access-denied error, and it gives users no actionable next step. The document's note points users toward checking a version requirement, which they will satisfy, yet the command will still fail.

**Evidence:** The tip ends with a note about build requirements but provides no error-handling path for the common failure mode of the service not existing.

**Impact:** A Windows user on Home or LTSC edition follows the Tip, runs `Start-Service ssh-agent`, receives an error, and has no documented path forward. Without SSH agent, they face passphrase prompts on every git operation with a passphrase-protected key, degrading the experience the tip was intended to improve.

**Dimension:** Completeness

**Response Required:** Extend the Windows SSH agent tip to include: (1) how to install OpenSSH Client if not present (`Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0`), and (2) how to verify the service exists before attempting `Start-Service` (`Get-Service ssh-agent -ErrorAction SilentlyContinue`).

**Acceptance Criteria:** Windows SSH agent tip includes a service-existence check and an install path for the OpenSSH Client optional feature, covering the case where the service does not exist.

---

### DA-003-qg1r1-da: Path Recommendation Silent on Space-in-Path Failure [MAJOR]

**Claim Challenged:** "Clone the repository to a location on your system. We recommend `~/plugins/`" (macOS Step 2 and Windows Step 2 introduction)

**Counter-Argument:** The `/plugin marketplace add <path>` command in Claude Code is a slash command whose argument is parsed by Claude Code's command parser. Paths containing spaces (e.g., `~/John Smith/plugins/jerry`) will be misinterpreted — the parser will treat `Smith/plugins/jerry` as a separate argument and the marketplace-add will fail with a confusing error. `~/plugins/` itself is safe, but the document's phrasing "Clone the repository to a location on your system" leaves the door open for the user to choose any path. The Warning about not overwriting SSH keys is present; there is no corresponding warning about path safety for the plugin directory.

**Evidence:** The Troubleshooting section documents the "Path Issues on Windows" workaround using forward slashes but does not address spaces in path names on either platform. The recommendation text implies any location is acceptable.

**Impact:** Any user with a space in their home directory path (common on macOS with full names as usernames, e.g., `~/John Smith/`) who clones to their default `~/` location and attempts marketplace add will fail immediately, with the only Troubleshooting guidance being "use forward slashes" — which does not resolve the spaces issue.

**Dimension:** Evidence Quality

**Response Required:** Add a note alongside the path recommendation stating that the clone path MUST NOT contain spaces, with the `/plugin marketplace add` command as the reason. Alternatively, document double-quoting the path in the marketplace-add command (if Claude Code supports quoted arguments).

**Acceptance Criteria:** Path recommendation includes explicit statement that spaces in the path will cause marketplace-add to fail, with guidance on avoiding or mitigating the issue.

---

### DA-004-qg1r1-da: Verification Precedes Configuration; JERRY_PROJECT Not Set [MAJOR]

**Claim Challenged:** "Run a simple skill to verify everything works: `/problem-solving` — You should see the problem-solving skill activate with information about available agents." (Verification section, "Test a Skill" subsection)

**Counter-Argument:** The document's own Configuration section (which follows Verification in the Table of Contents and document order) establishes that `JERRY_PROJECT` must be set for Jerry's SessionStart hook to function. CLAUDE.md and the hook architecture confirm: without `JERRY_PROJECT`, the SessionStart hook emits `<project-required>` and Jerry will prompt the user to select or create a project rather than activating skills normally. A user who has just completed installation and follows the document in order will run `/problem-solving` before setting `JERRY_PROJECT`. They will not see "the problem-solving skill activate with information about available agents" — they will see a project-selection prompt or an error, depending on session state. They will reasonably conclude the installation failed.

**Evidence:** Configuration section states: "Set the project environment variable: `export JERRY_PROJECT=PROJ-001-my-project`" and "The SessionStart hook will automatically load project context when you start Claude Code." CLAUDE.md H-04: "Active project REQUIRED. MUST NOT proceed without `JERRY_PROJECT` set." The Verification section makes no mention of this dependency.

**Impact:** Every new user following the document in order will encounter an unexpected state during verification. This is the most user-visible failure mode in the document — it occurs at the critical first-run moment when user confidence is lowest. Users who know to look at the CLAUDE.md may understand; a first-time user has no such context.

**Dimension:** Internal Consistency

**Response Required:** Either (a) move the `JERRY_PROJECT` setup step before the "Test a Skill" verification step, or (b) add a note in the Verification section explicitly stating that `/problem-solving` will show a project-selection prompt on first run (this is expected behavior), or (c) change the Verification "Test a Skill" to use a command that does not require `JERRY_PROJECT` (e.g., `/help` or `/plugin`).

**Acceptance Criteria:** A new user following the document in order will either (a) have `JERRY_PROJECT` set before the test skill step, or (b) receive explicit forewarning that the project-selection prompt is the expected first-run experience, not an error.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001 (osxkeychain no pre-check), DA-002 (SSH agent failure path missing), DA-007 (rate-limit omission). Three gaps in coverage of failure modes for documented steps. |
| Internal Consistency | 0.20 | Negative | DA-004 (Verification precedes Configuration in document order, creating a guaranteed first-run failure for new users). DA-005 (marketplace-add vs. plugin-install scope conflation). |
| Methodological Rigor | 0.20 | Neutral | The document's overall instruction methodology is sound. Steps are sequential, platforms are covered. No systematic methodology flaw. |
| Evidence Quality | 0.15 | Negative | DA-003 (path recommendation does not disclose the spaces-in-path failure mode). DA-006 (PAT `repo` scope described as "read access" which understates actual permissions granted). |
| Actionability | 0.15 | Negative | DA-002 (user given failing command without a recovery path). DA-004 (user told to expect skill activation; will see project prompt instead — no resolution path given). |
| Traceability | 0.10 | Neutral | Document sections link correctly to each other. TOC anchors are stable. Cross-references between Collaborator section and platform steps work. No traceability gaps introduced in this iteration. |

---

## Comparison to Previous Iteration

The following QG-1 findings were **successfully addressed** in this revision and are not raised again:

| Previous Finding | Status | Evidence of Resolution |
|-----------------|--------|----------------------|
| DA-001 (ssh-keygen pre-check) | RESOLVED | Both platforms now show `ls ~/.ssh/id_ed25519.pub` / `Test-Path` pre-check with Warning callout before key generation |
| DA-002 (Claude Code version floor) | RESOLVED | Prerequisites table updated to "1.0.33+" with explicit version floor |
| DA-003 (PAT credential caching) | PARTIALLY RESOLVED | Credential helpers added for both platforms; osxkeychain assumption introduced as new issue (DA-001-qg1r1-da) |
| DA-004 (manifest name) | RESOLVED | `"name": "jerry-framework"` now correct on both platforms with confirmation sentence |
| DA-005 (Linux out of scope) | ACCEPTED | Acknowledged as out of scope per gap analysis |
| DA-006 (Windows OpenSSH Client prereq) | RESOLVED | OpenSSH Client noted in Windows SSH agent tip |
| DA-007 ("password-free" claim) | RESOLVED | Claim qualified with passphrase and SSH agent scenarios |

**Net assessment:** 6 of 7 QG-1 findings cleanly resolved; 1 partially resolved (DA-003 PAT caching) introduced a new gap. Four new Major and three Minor issues identified.

---

## Recommendations

### P1 — Major (SHOULD resolve; require justification if not)

**DA-004-qg1r1-da** (Verification/Configuration ordering): Either move JERRY_PROJECT setup before the Test a Skill step, or add a note that the project-selection prompt is expected first-run behavior. This is the highest-priority finding because it affects 100% of new users at the critical first-run moment.
- Acceptance criteria: A new user following the document in order encounters no unexplained state during the Test a Skill step.

**DA-001-qg1r1-da** (osxkeychain pre-check): Add `git credential-osxkeychain version` verification before the `git config` command, plus a `credential.helper store` fallback with security note.
- Acceptance criteria: Credential helper section includes verification step and fallback for users without osxkeychain.

**DA-002-qg1r1-da** (Windows SSH agent service-not-found): Add `Get-Service ssh-agent -ErrorAction SilentlyContinue` check and `Add-WindowsCapability` install path before `Start-Service`.
- Acceptance criteria: Windows SSH agent tip handles the service-not-found failure mode with an install path.

**DA-003-qg1r1-da** (spaces in clone path): Add a note warning that the clone path must not contain spaces, with the marketplace-add command as the reason.
- Acceptance criteria: Path recommendation explicitly warns against spaces, with resolution guidance.

### P2 — Minor (MAY resolve; acknowledgment sufficient)

**DA-006-qg1r1-da** (PAT repo scope): Note that `repo` grants full read+write; recommend fine-grained PAT with `contents:read` for read-only access. If classic PAT is preferred for compatibility reasons, acknowledge the broader scope explicitly.
- Acceptance criteria: Scope description accurately states full read+write access, or alternative fine-grained PAT guidance is provided.

**DA-005-qg1r1-da** (marketplace vs. install scope conflation): Clarify that scope is chosen during `/plugin install`, not during `/plugin marketplace add`. A single sentence of clarification in the rationale callout is sufficient.
- Acceptance criteria: Rationale callout does not imply scope is chosen at marketplace-add time.

**DA-007-qg1r1-da** (GitHub anonymous clone rate limits): Add a note in the Future section that unauthenticated HTTPS clones may be subject to GitHub rate limits, with GitHub authentication as a mitigation.
- Acceptance criteria: Future section acknowledges or dismisses the rate-limit risk (either response is acceptable).

---

## Summary

- Major: 4
- Minor: 3
- Estimated score impact: If DA-004 and DA-001 are unaddressed: -0.08 to -0.12 on Completeness + Internal Consistency (weighted 0.40 combined). If all Major findings addressed: estimated composite score improvement of 0.10-0.15, potentially reaching the 0.92 threshold. Current unaddressed state estimated at 0.82-0.86.

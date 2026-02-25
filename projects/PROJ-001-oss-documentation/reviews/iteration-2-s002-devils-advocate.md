# Devil's Advocate Report: Jerry Framework Installation Guide (Iteration 2)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `docs/INSTALLATION.md`
**Criticality:** C4 (Critical) — public-facing OSS installation guide, irreversible once distributed
**Date:** 2026-02-25
**Reviewer:** adv-executor (S-002 Devil's Advocate)
**H-16 Compliance:** S-003 Steelman applied 2026-02-18 — confirmed at `docs/reviews/adv-s003-steelman-install-docs.md`
**Prior S-002 Execution:** `docs/reviews/iteration-1-s002-devils-advocate.md` (iteration 1, 2026-02-25)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Step 1: Advocate Role Assumption](#step-1-advocate-role-assumption) | Role framing and H-16 verification |
| [Step 2: Assumptions Extracted and Challenged](#step-2-assumptions-extracted-and-challenged) | Explicit and implicit assumption inventory |
| [Findings Summary](#findings-summary) | All findings by severity |
| [Detailed Findings](#detailed-findings) | Full evidence and analysis per finding |
| [Prior Execution: Finding Status](#prior-execution-finding-status) | Which iteration-1 findings were addressed vs. persist |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [Execution Statistics](#execution-statistics) | Counts and metadata |

---

## Step 1: Advocate Role Assumption

**Deliverable challenged:** `docs/INSTALLATION.md` (iteration 2 revision, 2026-02-25)
**Criticality level:** C4 (Critical) — public-facing OSS documentation, irreversible once distributed to the community
**H-16 verified:** S-003 Steelman output confirmed at `docs/reviews/adv-s003-steelman-install-docs.md`, executed 2026-02-18. Steelman strengthened the document before this critique begins.
**Prior execution verified:** Iteration-1 S-002 findings at `docs/reviews/iteration-1-s002-devils-advocate.md` (7 findings: 1 Critical, 4 Major, 2 Minor). Revision was performed between iterations; this execution evaluates whether those findings were adequately resolved and whether new weaknesses were introduced.

**Role assumed:** Argue the strongest possible case that this installation guide still fails its readers — as a skeptical first-time user who arrives at this document from a GitHub link and must successfully complete installation without prior knowledge of Claude Code's plugin system, Jerry's architecture, or the reviewer's intent behind the revisions.

**Focus for iteration 2:**
1. Whether the DA-001-it1 Critical finding (Interactive Installation) was correctly resolved
2. Whether the routing table now correctly handles no-SSH users end-to-end
3. Whether Step 2 (now the verification step) genuinely eliminates the source-name guessing problem
4. Whether new ambiguities or contradictions were introduced in the revision
5. Whether remaining assumptions still create friction for first-time users at scale

---

## Step 2: Assumptions Extracted and Challenged

| # | Assumption | Type | Challenge |
|---|------------|------|-----------|
| 1 | The Interactive Installation section rewrite ("After completing Step 1 above, you can also install through the `/plugin` UI") is unambiguous about what "Step 1" means | Implicit | A user who arrives at the Interactive Installation sub-section from the navigation table anchor (not by reading sequentially) has not read "Step 1 above" — the anchor `#install-from-github` takes them to the section heading, not to Step 1 specifically |
| 2 | The routing table's "Internet access, no SSH key" row will cause users to read the HTTPS variant of Install from GitHub, not the SSH variant | Implicit | The routing table links both SSH and no-SSH rows to the same anchor (`#install-from-github`); there is no direct link to the HTTPS command within Step 1 |
| 3 | Users who see "No — HTTPS alternative available" in the SSH row of Prerequisites will understand what "HTTPS alternative" means | Implicit | "HTTPS alternative available" is linked but not explained at the point of the table — the link takes users to the Install from GitHub section, not to the specific HTTPS command |
| 4 | Step 2 is now labeled "Verify the source registered" and a user who skips Step 1 will understand why Step 2 asks them to run a verification command | Implicit | If a user jumps to Step 2 from the navigation table or from troubleshooting, the step reads: "Run this to confirm Jerry's marketplace source was added" — the reference to "Step 1" in the context sentence is present but may be overlooked |
| 5 | The "Source name mismatch?" callout in Step 3 is sufficient to handle the `jerry-framework` name variability problem | Implicit | The callout is present and correct; it is reactive (fires on failure), not proactive. The document instructs users to run `/plugin install jerry@jerry-framework` before they verify the name from `/plugin marketplace list` |
| 6 | "hooks should activate automatically" (revised from "hooks activate automatically") is understood as an expectation with a verification step, not as a bug symptom | Implicit | "should activate automatically" uses modal hedging that may read as uncertainty rather than as a conditional awaiting verification; the verification steps are present but appear after the sentence |
| 7 | The community vs. official marketplace distinction is clear enough that users understand the Discover tab will show Jerry only after Step 1 | Implicit | The Interactive Installation sub-section states "Jerry will appear here because you registered its source in Step 1" — but the word "here" is the Discover tab, which is part of Claude Code's official `/plugin` UI. New users may not know whether the official Discover tab and registered-community-source Discover tab are the same UI element or different |
| 8 | Users who run `ssh -T git@github.com` and see "Hi <username>!" will correctly conclude they have SSH configured for GitHub and should use the SSH path | Implicit | Some users have SSH keys locally but have not added them to GitHub, or have keys for a different GitHub account — `ssh -T` confirms authentication to GitHub.com, but does not confirm that the SSH key is associated with their current GitHub identity. The test is correct but this edge case is not mentioned |
| 9 | The auto-update note ("community marketplaces like Jerry have auto-update disabled by default") does not create confusion with how plugin version management is expected to work | Implicit | The note says to "enable auto-update" via the Marketplaces tab — but users who did the HTTPS URL variant of Step 1 may have registered a source under a different name, and the instructions reference `jerry-framework` without acknowledging the name may differ |
| 10 | The uninstall command (`/plugin uninstall jerry@jerry-framework`) is consistent with the install path the user followed | Implicit | Users who installed via HTTPS or who had a different registered source name will have a different `@suffix`; the uninstall command uses a hardcoded `jerry-framework` suffix that may not match their environment |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001-it2 | Major | Interactive Installation sub-section: the instruction to find Jerry in the Discover tab is accurate only if users arrived sequentially — users who navigate directly to the sub-section via anchor link may not have completed Step 1, and the section does not guard against this | Install from GitHub → Interactive Installation |
| DA-002-it2 | Major | Both SSH and no-SSH routing table rows link to the same `#install-from-github` anchor — no-SSH users are told to use HTTPS but land at the section heading where the SSH command is displayed first | Which Install Method? |
| DA-003-it2 | Major | Step 3's "Source name mismatch?" callout is reactive, not proactive — users run `/plugin install jerry@jerry-framework` before they have confirmed the registered source name; the Step 2 verification step confirms the source but does not feed the name into Step 3 | Install from GitHub, Steps 2–3 |
| DA-004-it2 | Minor | "hooks should activate automatically" uses modal hedging without immediately following with a yes/no verification test — the verification steps are present but separated from the assertion | Enable Hooks section |
| DA-005-it2 | Minor | Uninstall command uses hardcoded `jerry@jerry-framework` suffix that may not match the source name registered by users who used the HTTPS URL or had a name variation | Uninstallation section |
| DA-006-it2 | Minor | The `ssh -T git@github.com` SSH check does not warn about the edge case of SSH keys existing but not being registered to the current GitHub account | Which Install Method? |

---

## Detailed Findings

### DA-001-it2: Interactive Installation Sub-Section Is Anchor-Navigation Fragile [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Install from GitHub → Interactive Installation (lines 128–137) |
| **Strategy Step** | Step 3 — Unstated assumptions; Unaddressed risks |

**Claim Challenged:**
> "After completing Step 1 above, you can also install through the `/plugin` UI:
> 1. Run `/plugin`
> 2. Navigate to the **Discover** tab — Jerry will appear here because you registered its source in Step 1
> 3. Find `jerry` and press Enter
> 4. Select your installation scope"
> (INSTALLATION.md, Interactive Installation sub-section, lines 130–136)

**Counter-Argument:**
The iteration-1 Critical finding (DA-001-it1) was that the Interactive Installation section described an impossible workflow — directing users to the Discover tab for a community plugin not in the official Anthropic catalog. The revision correctly addresses this by adding the qualifier "because you registered its source in Step 1" and the caveat "Jerry won't appear in Discover without Step 1." These are accurate and significant improvements.

However, the resolution introduces a new structural weakness: the section's correctness depends entirely on sequential reading. The section heading "Interactive Installation" is listed in the navigation table at line 16 as a cross-reference anchor, and the document-level navigation allows users to jump directly to this sub-section. A user who navigates directly to this sub-section via a search-engine result, a shared link, or the documentation site's sidebar will arrive without having read "Step 1 above."

Such a user reads: "Run `/plugin` → Navigate to the Discover tab — Jerry will appear here because you registered its source in Step 1." They have not registered any source. They navigate to the Discover tab, do not find Jerry, and the document's explanation ("because you registered its source in Step 1") reads as a past-tense confirmation of something they did not do — producing confusion rather than a clear error recovery path.

The document does include the caveat: "Jerry won't appear in Discover without Step 1." But this caveat appears after the numbered instructions, not before them. A user who executes step 1 of the numbered list (run `/plugin`), navigates to the Discover tab, and does not find Jerry will read backwards to find the caveat — which tells them they need Step 1 but does not link to it.

The counter-argument is structural: an interactive installation section that depends on prior linear reading is fragile in a web documentation context where users routinely arrive mid-document. The caveat is present but placed where it is discovered after failure, not before the action.

**Evidence:**
The section's caveat appears at lines 136–137:
> "Jerry won't appear in Discover without Step 1. The Discover tab shows plugins from all registered marketplaces. Jerry is a community plugin, not part of the official Anthropic catalog, so it only appears after you add its source."

This is the correct information but it follows the numbered instructions (lines 131–135) that a user may have already executed before reading the caveat.

**Impact:** Users who navigate directly to the Interactive Installation sub-section will attempt to find Jerry in the Discover tab without having completed Step 1. The failure mode is identical to what DA-001-it1 identified — no Jerry in the Discover tab — but now the cause is navigation order rather than incorrect documentation. The user count affected by direct-link navigation in an OSS documentation site is non-trivial.

**Recommendation:** Move the prerequisite caveat to before the numbered instructions:
> "Before using the UI path, complete Step 1 above (adding the plugin source via CLI). Without it, Jerry will not appear in the Discover tab.
> 1. Run `/plugin`
> 2. Navigate to the **Discover** tab..."

Alternatively, add a direct link to Step 1: "Before you begin: Run [Step 1](#step-1-add-the-jerry-repository-as-a-plugin-source) first, then return here."

**Acceptance Criteria:** The prerequisite warning precedes the numbered instructions in the Interactive Installation sub-section. A user who navigates directly to this sub-section sees the prerequisite before any numbered action, not after they attempt the action and fail.

---

### DA-002-it2: SSH and No-SSH Routing Rows Link to the Same Anchor — No-SSH Users Land at the SSH-First Section [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Which Install Method? (lines 54–63) and Install from GitHub (lines 67–139) |
| **Strategy Step** | Step 3 — Logical flaws; Unaddressed risks |

**Claim Challenged:**
The routing table presents four rows, including:
> "| **Internet access, no SSH key** — or you're not sure | [Install from GitHub (HTTPS)](#install-from-github) | ~2 minutes |"
> (INSTALLATION.md, line 57)

And the Install from GitHub section opens with:
> "**Step 1: Add the Jerry repository as a plugin source**
>
> Pick whichever command matches your setup — both do the same thing:
>
> | Your Setup | Command |
> |------------|---------|
> | **SSH key configured** | `/plugin marketplace add geekatron/jerry` |
> | **No SSH key (or not sure)** | `/plugin marketplace add https://github.com/geekatron/jerry.git` |"
> (INSTALLATION.md, lines 73–81)

**Counter-Argument:**
The iteration-1 findings DA-003-it1 and DA-004-it1 called for the HTTPS alternative to be a first-class routing row. The revision addresses this by adding a dedicated "Internet access, no SSH key" row that correctly routes to Install from GitHub and explicitly labels it "(HTTPS)." This is the correct structural fix.

However, both the SSH row and the no-SSH row link to the same destination anchor: `#install-from-github`. A user who clicks either link lands at the section heading `## Install from GitHub` (line 67). They then read the section introduction and encounter Step 1's two-command table, where the SSH command appears first:

```
| SSH key configured | /plugin marketplace add geekatron/jerry |
| No SSH key (or not sure) | /plugin marketplace add https://... |
```

For a no-SSH user who was routed to the "Install from GitHub (HTTPS)" row and followed the link, there is a cognitive mismatch: their routing table row explicitly said "HTTPS" and linked to a section that displays the SSH command first. The correct command (HTTPS) is present in the second row of Step 1's table, but the user must read past the SSH command to reach it.

The counter-argument: the routing table creates an expectation ("I am on the HTTPS path") that the section landing does not confirm immediately. No heading, no callout, and no highlighted guidance says "you're on the HTTPS path — use this command." A user who is uncertain about their SSH state (which the routing row explicitly targets — "or you're not sure") may look at Step 1, see two commands, and not know which to pick — which is exactly the confusion the routing table was intended to eliminate.

The note at line 63 says: "Not sure which to pick? Start with Install from GitHub using the HTTPS URL. It works for everyone." But this note is at the bottom of the routing table section, before the user follows the link. After following the link, the no-SSH user is in the Install from GitHub section with no similar reassurance.

**Evidence:**
Both routing rows use `[Install from GitHub](#install-from-github)` or `[Install from GitHub (HTTPS)](#install-from-github)` as link targets — the anchor is identical. The Install from GitHub section heading is at line 67; the two-command Step 1 table is at lines 78–81 with SSH listed first.

**Impact:** No-SSH users who follow the routing table's "Install from GitHub (HTTPS)" link land at the Install from GitHub section where the SSH command is displayed first. Some will attempt the SSH command despite the routing table's intent to send them to HTTPS, encounter the "Permission denied (publickey)" error, and then need to troubleshoot an error the routing table was designed to prevent them from encountering.

**Recommendation:** Add a contextual note at the top of the Install from GitHub section body (after the marketplace explanation, before Step 1) that reinforces the routing: "If you arrived here from the 'no SSH key' row, use the HTTPS URL in Step 1 below — it's in the second row of the table." Alternatively, add a dedicated anchor to the HTTPS command row (e.g., `#install-from-github-https`) so the routing table can link no-SSH users directly to the HTTPS command rather than to the section heading.

**Acceptance Criteria:** A no-SSH user who clicks the "Install from GitHub (HTTPS)" routing table link arrives at content that immediately confirms which command to use. The SSH command is not the first thing they read after following that link.

---

### DA-003-it2: Step 3 Runs Before Step 2's Verification Output Is Used — Source Name Remains a Guessing Problem [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Install from GitHub, Steps 2–3 (lines 86–106) |
| **Strategy Step** | Step 2 — What evidence supports this assumption? What if this assumption is wrong?; Step 3 — Unaddressed risks |

**Claim Challenged:**
> "**Step 2: Verify the source registered**
>
> Run this to confirm Jerry's marketplace source was added:
> ```
> /plugin marketplace list
> ```
>
> You should see `jerry-framework` in the output. This is the source name you'll use in the next step. If you don't see it, re-run Step 1."
> (INSTALLATION.md, lines 86–94)

> "**Step 3: Install the plugin**
>
> ```
> /plugin install jerry@jerry-framework
> ```
>
> This downloads and activates Jerry's skills, agents, and hooks. The format is `plugin-name@source-name` — `jerry` is the plugin name and `jerry-framework` is the source name from Step 2."
> (INSTALLATION.md, lines 98–104)

**Counter-Argument:**
The iteration-1 finding DA-005-it1 (Major) identified that the source name `jerry-framework` was presented as a documentation constant rather than a verified runtime value, and recommended making `marketplace list` a required step before the install command. The revision addresses this by renaming the step to "Verify the source registered" and positioning `/plugin marketplace list` as Step 2.

This is a meaningful improvement. However, the fix is incomplete in a specific way: Step 2 tells users to run `marketplace list` and look for `jerry-framework`, but Step 3's install command hardcodes `jerry@jerry-framework` without instructing users to substitute the actual name from Step 2's output.

Step 2 says: "You should see `jerry-framework` in the output. This is the source name you'll use in the next step."
Step 3 says: "/plugin install jerry@jerry-framework" with no substitution instruction.

A user who follows this literally runs the list (sees `jerry-framework`), then runs the hardcoded install command (which happens to use `jerry-framework`), and succeeds — but only because the name matched. The step does not teach users to use the name from the list; it tells them what name to expect and then hardcodes that name. If the name does not match (e.g., it registered as `jerry` or `geekatron-jerry`), the user has run Step 2 and confirmed the list — but Step 3's hardcoded command still fails.

The document does include a recovery path: the "Source name mismatch?" callout at lines 105–107:
> "Source name mismatch? If `/plugin install jerry@jerry-framework` returns 'plugin not found,' use the exact name from your `/plugin marketplace list` output: `/plugin install jerry@<name-from-list>`."

This callout is accurate and helpful, but it is reactive: it activates after failure. The step structure says "run list, confirm you see `jerry-framework`, then run `jerry@jerry-framework`" — which still requires the name to match. The instruction "this is the source name you'll use in the next step" implies the user should use the name dynamically, but Step 3's primary command does not reflect this.

The counter-argument: a complete fix would have Step 3's install command use a variable or explicit substitution pattern, such as:
```
/plugin install jerry@<name-from-step-2>
# Example if the list showed jerry-framework:
/plugin install jerry@jerry-framework
```

As written, the step teaches "the name is `jerry-framework`" rather than "use the name you just verified."

**Evidence:**
Step 2, line 93: "This is the source name you'll use in the next step."
Step 3, line 100: `/plugin install jerry@jerry-framework` (hardcoded, no variable notation)
Step 3, lines 105–107: "Source name mismatch? If `/plugin install jerry@jerry-framework` returns 'plugin not found,' use the exact name from your `/plugin marketplace list` output."

**Impact:** Users whose source registered under a name other than `jerry-framework` will pass Step 2 (the list shows a name), attempt Step 3's hardcoded command, fail, and need to diagnose the mismatch from the callout. The verification step's output is not integrated into the install command's instruction. The improvement reduces but does not eliminate the failure scenario DA-005-it1 identified.

**Recommendation:** Update Step 3's install command to use variable notation with the hardcoded form as an example:
```
/plugin install jerry@<name-from-list>
```
Below this, add: "Replace `<name-from-list>` with the source name from Step 2. If it showed `jerry-framework`, the command is `/plugin install jerry@jerry-framework`."

This makes the connection between Step 2's output and Step 3's input explicit and eliminates the failure path for non-`jerry-framework` source names.

**Acceptance Criteria:** Step 3's install command instruction explicitly instructs users to use the source name from Step 2's output. The hardcoded `jerry@jerry-framework` form appears only as a concrete example, not as the primary instruction. A user whose source registered under a different name can complete Step 3 on the first attempt without hitting the "Source name mismatch?" recovery path.

---

### DA-004-it2: "Hooks Should Activate Automatically" Uses Hedged Language Without an Immediately Adjacent Verification Test [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Enable Hooks section (line 187) |
| **Strategy Step** | Step 3 — Alternative interpretations; Unaddressed risks |

**Claim Challenged:**
> "Once uv is installed, hooks should activate automatically the next time you start Claude Code — verify using the [Hooks verification](#hooks-verification) steps below."
> (INSTALLATION.md, line 187)

**Counter-Argument:**
The revision changed "hooks activate automatically" to "hooks should activate automatically," which is an accurate hedge given the early access caveat. The addition of "— verify using the Hooks verification steps below" provides an appropriate follow-through action.

The remaining issue is the placement and phrasing interaction. A user reads: "hooks should activate automatically." The word "should" in a technical instruction has two plausible interpretations:
1. "This is expected behavior — verify it worked" (intended interpretation)
2. "This may or may not work — it's uncertain" (unintended but valid reading)

For a first-time user who has just invested time in installing uv, the "should" interpretation may read as "I'm not sure if this will work" rather than "this is the expected outcome, confirm it." The verification link is present but appears at the end of the sentence as a forward reference to a different section.

A new user who reads this sentence may:
- Restart Claude Code, see hooks not firing, and not know whether this is a bug or expected early-access behavior
- Restart Claude Code, see hooks firing, and not know they should verify because the verification step is a forward reference rather than the next numbered action
- Skip verification because the sentence structure treats verification as optional context ("verify using the steps below") rather than as a required action

The early access caveat at the top of the section (lines 145–148) provides detailed context on which hooks are stable and what verification to perform. But the caveat and the activation sentence are separated by the hooks table and the uv install instructions — approximately 40 lines of content. By the time users reach "hooks should activate automatically," the caveat context may not be top-of-mind.

**Evidence:**
Line 145–148 (caveat):
> "Early access caveat: Hook enforcement is under active development. Some hooks may have schema validation issues that cause them to fail silently... The most stable hooks are SessionStart and UserPromptSubmit. After installing uv: 1. Start a new Claude Code session and check whether the `<project-context>` tag appears... 2. If the tag is absent, check the `/plugin` **Errors** tab..."

Line 187 (activation sentence):
> "Once uv is installed, hooks should activate automatically the next time you start Claude Code — verify using the [Hooks verification](#hooks-verification) steps below."

The verification steps referenced are in a different section (#hooks-verification), separated by the Capability Matrix section.

**Impact:** Minor. The verification link is present and functional. Users who follow it will complete proper verification. The issue is that the sentence structure may cause some users to treat verification as optional or to not connect the "should" hedge with the specific failure modes described in the caveat 40 lines earlier.

**Recommendation:** Append an inline mini-verification step to the activation sentence:
> "Once uv is installed, hooks should activate automatically the next time you start Claude Code. Quick check: start a new session — if you see a `<project-context>` tag in the output, hooks are live. For full verification, see [Hooks verification](#hooks-verification) below."

This closes the loop at the point of action rather than forwarding to a different section.

**Acceptance Criteria:** The activation sentence includes a brief inline verification signal (e.g., what to look for in the next session output) so users who read the sentence know immediately how to confirm success, without having to navigate to a separate section first.

---

### DA-005-it2: Uninstall Command Hardcodes `jerry@jerry-framework` — Will Fail for Users With Different Registered Source Names [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Uninstallation → Remove the Plugin (lines 601–606) |
| **Strategy Step** | Step 3 — Unstated assumptions; Unaddressed risks |

**Claim Challenged:**
> "### Remove the Plugin
>
> ```
> /plugin uninstall jerry@jerry-framework
> ```"
> (INSTALLATION.md, lines 601–606)

**Counter-Argument:**
The uninstall command uses the same `jerry@jerry-framework` suffix that Step 3 of the install path uses. The same assumption applies: `jerry-framework` is the registered source name. However, the Uninstallation section appears far from the install steps and does not include the Step-2-equivalent reminder to check the actual registered name.

A user who installed via the HTTPS URL in a context where the source registered under a name other than `jerry-framework` — or a user who originally installed from a different fork or local path — will find that the uninstall command fails silently or with an error. The Uninstallation section does not include the equivalent of the install section's "Source name mismatch?" callout.

The document does include a note at lines 613–615:
> "Not sure of the source name? Run `/plugin marketplace list` to check."

This callout is present but it appears under "Remove the Plugin Source" (the marketplace removal command), not under "Remove the Plugin" (the uninstall command). A user who fails at the plugin uninstall step will not immediately see this guidance — it is three lines below in a different sub-section heading.

**Evidence:**
Line 603: `/plugin uninstall jerry@jerry-framework` (hardcoded, no note about source name variability)
Lines 613–615: "Not sure of the source name? Run `/plugin marketplace list` to check." (appears under the marketplace removal sub-section, not the plugin uninstall sub-section)

**Impact:** Minor. Uninstallation is a less-common action and most users who installed correctly with `jerry@jerry-framework` will uninstall successfully with the same suffix. Users who deviated from the primary path may encounter a failure, read the note in the adjacent sub-section, and recover. The issue is discoverability of the recovery note at the point of the failing command.

**Recommendation:** Add a note under the "Remove the Plugin" command, mirroring the pattern from the install step:
> "Source name differs? Use the name from `/plugin marketplace list`: `/plugin uninstall jerry@<name-from-list>`."

This makes the note visible at the point of the command rather than requiring users to read the next sub-section.

**Acceptance Criteria:** The "Remove the Plugin" sub-section includes an inline note about source name variability that is visible without reading the next sub-section. Users who deviated from the `jerry-framework` default source name can complete uninstallation without a trial-and-error failure.

---

### DA-006-it2: SSH Check Tip Does Not Address the "SSH Keys Exist But Wrong Account" Edge Case [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Which Install Method? (lines 61–62) |
| **Strategy Step** | Step 2 — Under what conditions would this assumption fail? |

**Claim Challenged:**
> "Not sure if you have SSH configured? Run `ssh -T git@github.com` in your terminal. If you see `Hi <username>!`, you have SSH set up. If you see 'Permission denied,' use the HTTPS path — same result, same speed, no SSH needed."
> (INSTALLATION.md, lines 61–62)

**Counter-Argument:**
The iteration-1 finding DA-003-it1 called for an inline SSH check command. This was addressed: the `ssh -T git@github.com` check is now present and correctly placed in the routing table section. This is the right fix.

The remaining issue is a false positive in the check: `ssh -T git@github.com` succeeds if the user's SSH key is registered to *any* GitHub account — not necessarily the account they intend to use for cloning. Scenarios where this creates a failure:

1. A user has SSH keys from a previous job's GitHub account, still on their local machine and still registered to that account. `ssh -T` returns `Hi old-employer-username!` — the check passes, they use the SSH path, but the clone may fail if the key is not registered to their current account.
2. A user has multiple SSH keys configured and the system's `ssh-agent` picks the wrong one. `ssh -T` succeeds with a different identity.

These are edge cases, not the common path. The check is correct for the vast majority of users. However, the routing note at line 62 says "If you see `Hi <username>!`, you have SSH set up" — which is true but incomplete. The `<username>` in the output is the key: if it is not their current GitHub username, they should use HTTPS.

**Evidence:**
Lines 61–62:
> "Not sure if you have SSH configured? Run `ssh -T git@github.com` in your terminal. If you see `Hi <username>!`, you have SSH set up."

The check does not instruct users to verify that `<username>` is their intended GitHub identity.

**Impact:** Minor. The edge case (SSH succeeds for a different account) is uncommon and the error ("Permission denied" when cloning) has a clear fix in the troubleshooting section. A user who hits this case will see the SSH troubleshooting section and can recover. The routing note is directionally correct for the majority.

**Recommendation:** Extend the success condition to include username verification:
> "If you see `Hi <username>!` and `<username>` is your GitHub account, you have SSH set up — use the SSH path. If the username is wrong or unexpected, use the HTTPS path to avoid potential authentication mismatches."

**Acceptance Criteria:** The SSH check tip acknowledges the possibility of a successful check with the wrong identity, and directs users who see an unexpected username to use HTTPS. The common path (correct username shown) is unchanged.

---

## Prior Execution: Finding Status

| Prior Finding | Prior Severity | Current Status | Evidence |
|---------------|---------------|----------------|---------|
| DA-001-it1: Interactive Installation directs users to Discover tab for a community plugin | Critical | **Substantially addressed** — Section rewritten to include "Jerry won't appear in Discover without Step 1" and the prerequisite qualifier. Residual issue: caveat placement after numbered instructions, not before. Downgraded to Major (DA-001-it2). | Lines 130–137, caveat present but post-instruction |
| DA-002-it1: SSH "Required" in prerequisites table without inline alternative | Major | **Addressed** — SSH now listed as "No — HTTPS alternative available" with an inline link. | Line 39: "No — HTTPS alternative available" with link |
| DA-003-it1: "Most people" routing row assumes users know their SSH state | Major | **Addressed** — Routing table now has four rows including "Internet access, no SSH key" and inline `ssh -T` check command. | Lines 54–62, four routing rows present |
| DA-004-it1: HTTPS alternative not surfaced in routing decision table | Major | **Substantially addressed** — HTTPS is a first-class routing row. Residual issue: both rows link to same anchor, landing users at SSH-first step content. Retained as Major (DA-002-it2). | Line 57, HTTPS routing row present; anchor target unchanged |
| DA-005-it1: `jerry-framework` source name as unverified constant | Major | **Substantially addressed** — Step 2 is now "Verify the source registered" with `marketplace list` as a proactive step. Residual issue: Step 3 install command still hardcodes `jerry-framework` without substitution instruction. Retained as Major (DA-003-it2). | Lines 86–94 (Step 2 verification present), line 100 (Step 3 still hardcoded) |
| DA-006-it1: McConkey voice at navigational content | Minor | **Addressed** — "Two commands and you're riding" removed from nav table; "you're in" replaced with declarative language. | Nav table line 15: "Persistent install via Claude Code's plugin system (~2 min)" |
| DA-007-it1: `--plugin-dir` labeled "Alternative" | Minor | **Addressed** — Section renamed to "Session Install (Plugin Dir Flag)"; routing row updated to "Session-only install — skills available immediately, no configuration." | Lines 19, 59 |

**Summary:** 3 of 7 iteration-1 findings fully addressed (DA-002-it1, DA-003-it1, DA-006-it1, DA-007-it1 — actually 4 fully addressed). 2 substantially addressed with residual issues elevated to new findings (DA-001-it1 → DA-001-it2 Major; DA-004-it1 and DA-005-it1 combined aspect → DA-002-it2 and DA-003-it2). 0 iteration-1 findings completely unaddressed. 0 new Critical findings in this iteration. 3 new findings (2 Minor: DA-004-it2, DA-005-it2, DA-006-it2).

**Net improvement from iteration 1 to iteration 2:** Critical count: 1 → 0. Major count: 4 → 3. Minor count: 2 → 3. Total: 7 → 6. The document is materially stronger: the Critical finding is resolved (with a residual that is Major, not Critical), SSH handling is now correct, routing table is four-path, and voice issues are cleared.

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

No Critical findings in this iteration. The iteration-1 Critical finding (DA-001-it1) has been resolved to a Major-severity residual issue (DA-001-it2).

### P1 — Major (SHOULD resolve; require justification if not)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-it2 | Move the prerequisite warning in the Interactive Installation sub-section to appear before the numbered instructions. Either add "Before you begin: Complete Step 1 (adding the source via CLI) first." or add a direct link to Step 1 as a prerequisite guard. | The prerequisite warning appears before numbered step 1 in the sub-section. A user who arrives at this sub-section from a direct link sees the prerequisite before any numbered action. |
| DA-002-it2 | Add context at the top of the Install from GitHub section body (after the marketplace explanation, before Step 1) that directs no-SSH users to the second command in Step 1's table. Or create a dedicated anchor (`#install-from-github-https`) that links directly to the HTTPS command row. | A no-SSH user who clicks the routing table's "Install from GitHub (HTTPS)" link arrives at content that immediately confirms which command to use, without the SSH command appearing first. |
| DA-003-it2 | Update Step 3's install command instruction to use variable notation: `/plugin install jerry@<name-from-list>` with an explicit example showing `jerry@jerry-framework` as the expected form. Make the connection between Step 2's output and Step 3's input command explicit. | Step 3's primary install instruction uses variable notation. The hardcoded `jerry@jerry-framework` appears only as a concrete example. A user whose source registered under a different name can complete Step 3 on the first attempt. |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-004-it2 | Append an inline mini-verification to the "hooks should activate automatically" sentence, identifying what to look for (the `<project-context>` tag) so users can verify success without navigating to a separate section. | The activation sentence includes a brief inline signal about what success looks like in the next session. |
| DA-005-it2 | Add a source-name variability note under the "Remove the Plugin" uninstall command, mirroring the pattern from the troubleshooting section. | The "Remove the Plugin" sub-section includes an inline note about source name variability without requiring users to read the next sub-section. |
| DA-006-it2 | Extend the `ssh -T` success condition to instruct users to verify the displayed username matches their intended GitHub identity, with a fallback to HTTPS if it does not. | The SSH check tip acknowledges the wrong-identity edge case. The common path (correct username) is unchanged. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral-to-Positive | The document now covers four install paths explicitly (SSH, HTTPS, local clone, session install). The interactive installation caveat is present. The auto-update note, marketplace distinction, and uninstall guidance are complete. DA-005-it2 identifies a minor gap in uninstall instructions (no source-name variability note), but it is minor and recoverable. Net: marginally positive relative to iteration 1. |
| Internal Consistency | 0.20 | Mixed | DA-001-it2 and DA-002-it2 identify structural inconsistencies introduced or retained in the revision: (1) Interactive Installation section's numbered instructions precede the prerequisite warning; (2) the "no-SSH HTTPS" routing row links to the same anchor as the SSH row, creating a routing expectation the landing content does not immediately fulfill. These are non-trivial consistency issues that create failure paths for specific user navigation patterns. |
| Methodological Rigor | 0.20 | Positive | The install methodology improved significantly in this iteration. Step 2 is now a proactive verification step. The four-path routing table gives users a structured decision framework. The Prerequisites table correctly represents SSH as optional rather than required. The early access caveat is comprehensive and specific. DA-003-it2 identifies a remaining gap (Step 3 does not use Step 2's output dynamically), but the overall methodology is sound and the gap is targeted. |
| Evidence Quality | 0.15 | Positive | The marketplace explanation, SSH behavior explanation, hook stability specifics (most stable: SessionStart and UserPromptSubmit), and skill count correction (12 skills, 54 agents) all reflect accurate, specific claims. The document does not overstate what hooks guarantee. No factual inaccuracies identified in this iteration. |
| Actionability | 0.15 | Mixed | Three findings (DA-001-it2, DA-002-it2, DA-003-it2) identify points where users receive correct information but in a structure that may require a failure cycle to recover from (interactive install prerequisite, landing at SSH command when routed for HTTPS, hardcoded install command). These are structural actionability gaps: the information exists, but its placement requires recovery rather than proactive completion. |
| Traceability | 0.10 | Positive | Cross-section links are functional. The troubleshooting section anchors are correctly referenced from the install steps. The "Source name mismatch?" callout links to the Troubleshooting section. The marketplace explanation links to the official Anthropic marketplace for reference. Navigation table covers all sections. No traceability regressions from iteration 1. |

**Overall Assessment:** 0 Critical, 3 Major, 3 Minor findings. The document has improved substantially from iteration 1: the Critical finding is resolved, SSH routing is correct, voice issues are cleared, and the install methodology is more rigorous. The three remaining Major findings are structural issues — they create failure paths for specific navigation patterns (direct-link to sub-sections, HTTPS routing anchor gap, hardcoded install command) rather than fundamental documentation errors. These are addressable with targeted edits that do not require structural rework.

The document is approaching acceptance quality for a C4 OSS installation guide. The remaining Major findings, if unresolved, represent failure paths that real users on non-linear documentation journeys will encounter. **Recommendation: REVISE — targeted revision required. Three specific fixes (prerequisite warning placement, HTTPS anchor or context note, Step 3 variable notation) are all that stand between the current state and acceptance.**

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 0
- **Major:** 3 (DA-001-it2, DA-002-it2, DA-003-it2)
- **Minor:** 3 (DA-004-it2, DA-005-it2, DA-006-it2)
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** Confirmed — S-003 Steelman applied 2026-02-18 at `docs/reviews/adv-s003-steelman-install-docs.md`
- **H-15 Self-Review Applied:** Yes — all findings verified for: specific evidence from deliverable with line citations, justified severity classification, DA-NNN-it2 identifier format, summary table consistency with detailed findings, no findings omitted or minimized
- **Prior Findings Fully Addressed (iteration 1 → iteration 2):** 4 of 7 (DA-002-it1, DA-003-it1, DA-006-it1, DA-007-it1)
- **Prior Findings Substantially Addressed (residual → new finding):** 3 of 7 (DA-001-it1 → DA-001-it2 Major; DA-004-it1 partial + DA-005-it1 partial → DA-002-it2 and DA-003-it2)
- **Prior Findings Completely Unaddressed:** 0 of 7
- **New Findings Not in Prior Execution:** 3 (DA-004-it2, DA-005-it2, DA-006-it2 — all Minor)
- **Critical Count Change:** 1 (iteration 1) → 0 (iteration 2)
- **Major Count Change:** 4 (iteration 1) → 3 (iteration 2)
- **Dimensions with Negative Impact:** 0 of 6
- **Dimensions with Mixed Impact:** 2 of 6 (Internal Consistency, Actionability)
- **Dimensions Positive:** 3 of 6 (Methodological Rigor, Evidence Quality, Traceability)
- **Dimensions Neutral-to-Positive:** 1 of 6 (Completeness)
- **P0 Findings (block acceptance):** 0
- **P1 Findings:** 3
- **P2 Findings:** 3

---

*Strategy: S-002 Devil's Advocate*
*Template Version: 1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Finding Prefix: DA-NNN-it2*
*Execution Date: 2026-02-25*
*Prior Execution: `docs/reviews/iteration-1-s002-devils-advocate.md`*
*Steelman Reference: `docs/reviews/adv-s003-steelman-install-docs.md`*

# Devil's Advocate Report: Jerry Framework Installation Guide (Iteration 1)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `docs/INSTALLATION.md`
**Criticality:** C4 (Critical) — public-facing OSS installation guide, irreversible once distributed
**Date:** 2026-02-25
**Reviewer:** adv-executor (S-002 Devil's Advocate)
**H-16 Compliance:** S-003 Steelman applied 2026-02-18 — confirmed at `docs/reviews/adv-s003-steelman-install-docs.md`
**Prior S-002 Execution:** `docs/reviews/adv-s002-devils-advocate-installation-c4.md` (C4, 2026-02-25, prior document version)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Step 1: Advocate Role Assumption](#step-1-advocate-role-assumption) | Role framing and H-16 verification |
| [Step 2: Assumptions Extracted and Challenged](#step-2-assumptions-extracted-and-challenged) | Explicit and implicit assumption inventory |
| [Findings Summary](#findings-summary) | All findings by severity |
| [Detailed Findings](#detailed-findings) | Full evidence and analysis per finding |
| [Prior Execution: Finding Status](#prior-execution-finding-status) | Which prior findings were addressed vs. persist |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [Execution Statistics](#execution-statistics) | Counts and metadata |

---

## Step 1: Advocate Role Assumption

**Deliverable challenged:** `docs/INSTALLATION.md` (current version, post-revision from prior C4 S-002 execution)
**Criticality level:** C4 (Critical) — public-facing OSS documentation, irreversible once distributed to the community
**H-16 verified:** S-003 Steelman output confirmed at `docs/reviews/adv-s003-steelman-install-docs.md`, executed 2026-02-18. Steelman strengthened the document before this critique begins.
**Role assumed:** Argue the strongest possible case that this installation guide fails its readers — as a skeptical first-time user who has never heard of Jerry, has no prior knowledge of Claude Code's plugin system, and encounters this document with no context other than a GitHub link.

**Focus areas per invocation context:**
1. Whether the SSH requirement is explained clearly enough for new users
2. Whether the marketplace terminology is demystified adequately
3. Whether install steps are accurate and verifiable
4. Whether the HTTPS alternative is discoverable enough
5. Any remaining assumptions that could trip up first-time users

---

## Step 2: Assumptions Extracted and Challenged

| # | Assumption | Type | Challenge |
|---|------------|------|-----------|
| 1 | Users who see "SSH key configured for GitHub — Yes (Required)" will know what to do next | Implicit | Prerequisites table lists SSH as required but the "Why SSH?" box explaining what SSH is and linking to setup guides is separated by a blank row — a user who only skims the prerequisites table hits the requirement without seeing the explanation |
| 2 | "Most people" have SSH keys configured for GitHub | Implicit structural | New Claude Code users are not necessarily Git/GitHub power users; many developers use HTTPS-only workflows |
| 3 | The HTTPS alternative is equally prominent to the SSH path | Implicit | The HTTPS command appears in a blockquote tip box inside Step 1, below the primary SSH command — a user who executes Step 1 and fails will need to scroll back to find the alternative |
| 4 | Users understand that `geekatron/jerry` is an `owner/repo` shorthand, not a full path | Implicit | The shorthand convention is never named or explained; users from non-GitHub backgrounds may not recognize it |
| 5 | The marketplace explanation added in this revision fully demystifies the term | Implicit | The explanation appears at the top of Install from GitHub but uses "catalog of plugins" — "catalog" itself is a borrowed term that may not clarify the concept for non-English-native speakers |
| 6 | `jerry-framework` is a stable, environment-independent source name | Implicit | The source name comes from `marketplace.json` in the repository; if this file is absent, malformed, or the name changes in a new version, Step 2 fails silently |
| 7 | Users who see the verification prompt "Confirm `jerry` appears in the list" understand what to do if it does NOT appear | Implicit consequence | The verification step confirms success but does not inline the failure path — it points to Configuration and Verification sections without addressing why `jerry` might not appear |
| 8 | The "Which Install Method?" routing table sends most users to the SSH-primary path, which is correct | Implicit | The table routes "Most people — internet access, SSH key configured for GitHub" to Install from GitHub, but many new users will not know whether they have SSH keys configured and will self-classify as "Most people" |
| 9 | Interactive Installation (browsing the /plugin Discover tab) will show Jerry | Implicit | The Interactive Installation alternative (Step Alternative: Interactive Installation) assumes Jerry is discoverable via the Discover tab — which would require it to be in an official Anthropic catalog, not on a community GitHub repo |
| 10 | Configuration being labeled "required for skills to work" in the navigation table is enough to stop users from skipping it | Implicit | The navigation table entry says "Project setup — required for skills to work" but users who scan headings may not read the navigation table entry descriptions |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001-it1 | Critical | Interactive Installation sub-section directs users to "Discover" tab — which cannot show a community GitHub plugin not in the official Anthropic catalog | Install from GitHub → Alternative: Interactive Installation |
| DA-002-it1 | Major | SSH requirement is listed as "Yes (Required)" in prerequisites table but the explanation and HTTPS fallback are in a blockquote below — a user who skims the table hits a hard stop with no inline guidance | Prerequisites |
| DA-003-it1 | Major | "Most people" routing row in the decision table assumes users know whether they have SSH configured — the group that doesn't know will self-select the wrong path | Which Install Method? |
| DA-004-it1 | Major | HTTPS alternative is adequately documented at Step 1 but not adequately discoverable from the "Which Install Method?" decision table, which sends SSH-uncertain users to Local Clone instead of the HTTPS variant of the primary path | Which Install Method? + Install from GitHub |
| DA-005-it1 | Major | `jerry-framework` source name is presented as a known constant, but the only verification mechanism is a tip box triggered by failure — there is no pre-install verification step | Install from GitHub, Step 2 |
| DA-006-it1 | Minor | McConkey voice persists at step-level instructional content ("Two commands and you're riding", "you're in") despite prior Major finding DA-003-20260225 recommending removal | Install from GitHub, document-wide |
| DA-007-it1 | Minor | `--plugin-dir` is still positioned as "Alternative" in the navigation table, listed after two other methods — prior Major finding DA-002-20260225 flagged this and it remains unaddressed | Navigation table, Alternative: Plugin Dir Flag |

---

## Detailed Findings

### DA-001-it1: Interactive Installation Directs Users to a Discover Tab That Cannot Show a Community Plugin [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `docs/INSTALLATION.md`, Install from GitHub → Alternative: Interactive Installation (lines 118–128) |
| **Strategy Step** | Step 3 — Logical flaws, Contradicting evidence |

**Evidence:**
> "### Alternative: Interactive Installation
>
> You can also browse and install through the `/plugin` UI directly:
>
> 1. Run `/plugin`
> 2. Navigate to the **Discover** tab
> 3. Find `jerry`
> 4. Press Enter and select your installation scope"
> (INSTALLATION.md, lines 118–126)

The same document, earlier in the Install from GitHub section, states:

> "Jerry is a **community Claude Code plugin** hosted on [GitHub](https://github.com/geekatron/jerry). You install it directly from the GitHub repository using Claude Code's built-in plugin system."
> (INSTALLATION.md, line 66)

And in the marketplace explanation:

> "Claude Code uses the word 'marketplace' in its `/plugin marketplace` commands, but it's just the mechanism for registering plugin sources — think 'add a source' not 'browse a store.'"
> (INSTALLATION.md, line 68)

**Analysis:**
The document contains an internal contradiction. The "What does 'marketplace' mean here?" explanation correctly establishes that Claude Code's "marketplace" is not a browse-and-discover app store — it is a source registration mechanism. The document correctly explains that Jerry is a community plugin installed directly from GitHub, not from an official Anthropic registry.

Yet three paragraphs later, the "Alternative: Interactive Installation" section instructs users to navigate to the **Discover** tab and find `jerry`. The Discover tab in Claude Code would surface plugins in the official Anthropic-curated catalog — not community GitHub plugins. Jerry, as a community GitHub plugin that is explicitly "not on the official Anthropic marketplace," would not appear in the Discover tab.

The counter-argument is unambiguous: the Interactive Installation sub-section describes a workflow that either (a) does not work at all for Jerry because Jerry is not in the Discover catalog, or (b) only works if the user has already run `/plugin marketplace add geekatron/jerry` to register the source, in which case "Navigate to the Discover tab and find jerry" is actually navigating to a tab that now shows Jerry only because the source was already registered — which is not "interactive installation" in the consumer-app-store sense the section implies.

The "What does 'marketplace' mean here?" clarification (which correctly demystifies the terminology) directly contradicts the Interactive Installation section (which implies a Discover-tab-based app-store workflow). A first-time user who reads the Interactive Installation sub-section and attempts to find Jerry in the Discover tab without first running the CLI command will fail, and the document's previous claim that "marketplace is not a browse-a-store experience" will confuse rather than help.

This is Critical because:
1. The section actively directs users toward a workflow that cannot succeed as described
2. It contradicts the marketplace demystification effort elsewhere in the document
3. A user who follows this path will not get a clear error — they simply will not find `jerry` in the Discover tab and may conclude Jerry is unavailable

**Impact:** Users who attempt the Interactive Installation path will fail to find Jerry in the Discover tab, conclude the tool is unavailable or misconfigured, and file confusion-related issues. The section undermines the credibility of the marketplace demystification effort in the same parent section.

**Recommendation:** Either (a) remove the Interactive Installation sub-section entirely, or (b) rewrite it to describe what "interactive" actually means in the context of already-registered sources: "After running Step 1 (adding the source), you can also install Jerry via the `/plugin` UI: Run `/plugin`, navigate to **Installed** or **Marketplaces**, find `jerry-framework`, and install from there." This eliminates the false implication that Jerry is discoverable without first registering the source.

**Acceptance Criteria:** The Interactive Installation sub-section either does not exist, or correctly describes the UI workflow that follows after the source has been added via CLI. It does not instruct users to navigate to a Discover tab to find a community plugin that is not in the official Anthropic catalog.

---

### DA-002-it1: SSH "Required" Listed in Prerequisites Table With Explanation Only in a Separate Blockquote [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Prerequisites (lines 32–47) |
| **Strategy Step** | Step 3 — Unaddressed risks, Alternative interpretations |

**Evidence:**
The prerequisites table:
> "| SSH key configured for GitHub | **Yes** | Claude Code clones plugins via SSH (see note below) |"
> (INSTALLATION.md, line 37)

The explanation follows the table in a blockquote:
> "**Why SSH?** When you add a plugin source with `/plugin marketplace add geekatron/jerry`, Claude Code clones the repository using SSH (`git@github.com:...`). Even though Jerry's repo is public, Claude Code's plugin system requires SSH access by default. If you don't have SSH keys set up for GitHub, you'll hit a 'Permission denied (publickey)' error. See [GitHub's SSH key guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to get set up — it takes a few minutes."
> (INSTALLATION.md, lines 40–41)

The HTTPS bypass is in a second blockquote:
> "**Don't want to set up SSH?** You can bypass the SSH requirement entirely by using the full HTTPS URL instead of the `owner/repo` shorthand. See Step 1 in [Install from GitHub](#install-from-github) for the HTTPS alternative command."
> (INSTALLATION.md, line 42)

**Analysis:**
The table correctly marks SSH as required and adds a "(see note below)" inline. The explanation blockquote is present and correct. However, the structural problem is that the table row marks SSH as "Yes (Required)" without stating the HTTPS alternative at the point of the requirement. A user who reads the prerequisites table and sees "SSH key configured for GitHub — Yes" may:

1. Not scroll down to read the blockquote notes (especially on mobile or in split-screen workflows)
2. Not have SSH keys and decide the install is impossible before reaching the "Don't want to set up SSH?" note
3. Read "Required" as an absolute gate rather than as "required for the primary method, optional for the HTTPS alternative"

The prerequisite table entry says "Yes" for required status. A user who lacks SSH keys sees a hard requirement and no inline indication that there is a bypass. The bypass is two lines lower in a blockquote that begins "Don't want to set up SSH?" — a sentence that assumes the user has read the table, understood the implication, and is now seeking alternatives. This is a three-step cognitive path: (1) read table row, (2) infer that they might not have SSH, (3) read blockquote for workaround. Many users will not complete step 2 and will conclude SSH is a hard requirement.

The counter-argument: the Prerequisites table is supposed to be a clear statement of what is needed. By listing SSH as "Yes" without an inline escape path, the table sets a gate that the document itself knows is not actually hard — the HTTPS URL bypasses it entirely. The table creates a false hard requirement.

**Impact:** Users without SSH keys who read only the prerequisites table will classify themselves as unable to proceed with the primary install method. Some will abandon before discovering the HTTPS alternative. Others will spend time setting up SSH keys when the HTTPS URL would have worked in 30 additional seconds.

**Recommendation:** Update the Prerequisites table row to inline the alternative: change the Required column from "**Yes**" to "**Yes** (for primary method; [HTTPS alternative](#install-from-github) available)". This makes the escape path visible at the point of the requirement without requiring users to read the blockquote to discover it.

**Acceptance Criteria:** The Prerequisites table row for SSH includes an inline reference to the HTTPS alternative. A user who reads only the table row knows that SSH is required for the primary method but that an alternative exists. The table does not imply SSH is a hard gate with no bypass.

---

### DA-003-it1: "Most People" Routing Row Assumes Users Know Their SSH Configuration State [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Which Install Method? (lines 50–61) |
| **Strategy Step** | Step 2 — What if this assumption is wrong?; Step 3 — Unstated assumptions |

**Evidence:**
> "| **Most people** — internet access, SSH key configured for GitHub | [Install from GitHub](#install-from-github) | ~2 minutes |"
> "| **No SSH key** or **locked-down network** | [Local Clone](#alternative-local-clone) | ~5 minutes |"
> (INSTALLATION.md, lines 56–57)

> "Not sure? Start with [Install from GitHub](#install-from-github). If SSH gives you trouble, the [Local Clone](#alternative-local-clone) method always works."
> (INSTALLATION.md, line 60)

**Analysis:**
The routing table presents three rows: "Most people," "No SSH key or locked-down network," and "Quick test drive." The table assumes users can accurately self-classify by knowing whether they have SSH keys configured for GitHub. This is a non-trivial knowledge requirement for the target audience of this document.

The target audience includes:
- Developers new to Claude Code but experienced with Git (may have SSH configured)
- Developers new to Git who found Jerry through the Claude Code ecosystem (may not know what SSH keys are)
- Developers who have SSH keys locally but have not added them to GitHub (will fail the primary method)
- Developers who have GitHub SSH keys but whose keys are not their current machine's keys (common after OS reinstall or new laptop setup)

The "Not sure?" fallback at line 60 says "Start with Install from GitHub. If SSH gives you trouble, the Local Clone method always works." This is a try-fail-retry routing strategy: attempt the primary path, hit an SSH error, then fall back. This works, but it imposes a failure experience on any user who does not have SSH configured. The document sends them into the primary path knowing they may fail.

The counter-argument: the routing table claims to route users to the right method, but the routing criterion ("SSH key configured for GitHub") requires users to have pre-knowledge about their environment that the document does not help them verify. A user who is unsure whether they have SSH keys configured has no inline way to check — the document does not say "To check if you have SSH keys configured, run `ssh -T git@github.com`."

Additionally, the HTTPS alternative to the primary method is not represented as its own routing row. A user who has no SSH key but wants the 2-minute install time is not offered an "Install from GitHub via HTTPS — No SSH needed" row. They are routed to "Local Clone (~5 minutes)" even though the HTTPS URL would give them the same result as the primary method with zero additional setup.

**Impact:** Users who lack SSH configuration will be routed to Local Clone (~5 minutes) when the HTTPS variant of Install from GitHub (~2 minutes) would serve them equally well. The routing table underserves this user class by routing them to the longer path unnecessarily.

**Recommendation:** Add a fourth row to the routing table: "**No SSH key** — internet access but no SSH configured" → [Install from GitHub](#install-from-github) (use HTTPS URL in Step 1) → ~2 minutes. Rename the existing "No SSH key or locked-down network" row to "**Offline or network-restricted** — corporate firewall, air-gapped, or version-pinned" to disambiguate network restrictions from SSH-absence. Add a one-line check: "Not sure if you have SSH configured? Run `ssh -T git@github.com` — if you get `Hi <username>`, you're set."

**Acceptance Criteria:** The routing table presents four paths with the HTTPS variant of the primary method as a distinct row. The "No SSH key" criterion routes users to the 2-minute path, not the 5-minute path. Users who are unsure about their SSH configuration have an inline check command.

---

### DA-004-it1: HTTPS Alternative Is Documented at Step 1 But Not Surfaced in the Primary Decision Gate [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Which Install Method? (lines 50–61) and Install from GitHub Step 1 (lines 70–86) |
| **Strategy Step** | Step 3 — Unaddressed risks, Alternative interpretations |

**Evidence:**
The HTTPS alternative appears at Step 1 in a blockquote:
> "**No SSH key?** Use the full HTTPS URL instead — no SSH required:
> ```
> /plugin marketplace add https://github.com/geekatron/jerry.git
> ```
> This does the same thing but clones over HTTPS, which works without SSH configuration."
> (INSTALLATION.md, lines 80–84)

The Prerequisites section references it:
> "**Don't want to set up SSH?** You can bypass the SSH requirement entirely by using the full HTTPS URL instead of the `owner/repo` shorthand. See Step 1 in [Install from GitHub](#install-from-github) for the HTTPS alternative command."
> (INSTALLATION.md, line 42)

The Which Install Method? routing table does NOT mention the HTTPS variant as a distinct option. It routes non-SSH users to Local Clone.

**Analysis:**
The HTTPS alternative to the SSH command is documented in two places (Prerequisites blockquote and Step 1 blockquote) and is accurate. The documentation is present. The problem is discoverability at the decision gate.

A new user's decision path is:
1. Read Prerequisites → sees "SSH key: Yes (Required)"
2. Reads "Don't want SSH?" → directed to "See Step 1 in Install from GitHub"
3. Reads Which Install Method? routing table → routes them to "Local Clone" if no SSH
4. Follows Local Clone path → 5-minute install with git clone + marketplace add

Steps 2 and 3 contradict each other. The Prerequisites blockquote says "You can bypass SSH by using HTTPS — see Step 1 in Install from GitHub." The routing table sends no-SSH users to Local Clone. A user who reads the routing table after the Prerequisites blockquote is given conflicting routing instructions.

Furthermore, the HTTPS alternative is embedded inside a blockquote tip box within Step 1 of the "Install from GitHub" section. A user who was routed to "Local Clone" by the routing table will never reach Step 1 of Install from GitHub and will never see the HTTPS alternative. The HTTPS option is effectively invisible to users who follow the routing table's guidance.

The counter-argument: the HTTPS alternative achieves the same result as the primary method (SSH-based `/plugin marketplace add geekatron/jerry`) with zero additional setup. It should be the DEFAULT for users without SSH, not a tip box. The routing table actively routes no-SSH users away from the path that would work in 2 minutes with one URL change.

**Impact:** Users without SSH keys who follow the routing table will spend 5 minutes on the Local Clone path when they could have completed the install in 2 minutes using the HTTPS URL. The HTTPS alternative is present in the document but is not discoverable at the decision point where users need it. This is a navigation and discoverability failure.

**Recommendation:** Elevate the HTTPS alternative to a first-class option in the routing table (addressed in DA-003-it1). Additionally, update the Prerequisites "Don't want to set up SSH?" blockquote to link directly to the routing table row: "You can use the HTTPS URL in the Install from GitHub path — see the routing table above for the no-SSH option." This aligns the Prerequisites guidance with the routing table guidance.

**Acceptance Criteria:** The HTTPS alternative appears as a distinct row in the routing table. The Prerequisites blockquote and routing table give consistent routing guidance for no-SSH users. A user who follows the routing table for no-SSH installs reaches the HTTPS URL without being routed through Local Clone.

---

### DA-005-it1: `jerry-framework` Source Name Presented as a Known Constant With No Pre-Install Verification Step [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Install from GitHub, Step 2 (lines 88–96) |
| **Strategy Step** | Step 2 — What evidence supports this assumption?; Step 3 — Unaddressed risks |

**Evidence:**
> "**Step 2: Install the plugin**
>
> ```
> /plugin install jerry@jerry-framework
> ```
>
> This downloads and activates Jerry's skills, agents, and hooks. The format is `<plugin-name>@<source-name>` — `jerry` is the plugin name and `jerry-framework` is the source name (both defined in the repository's `.claude-plugin/` manifests)."
> (INSTALLATION.md, lines 88–94)

> "**Install command fails?** The source name must match exactly. Run `/plugin marketplace list` to see what Claude Code registered, then use that name: `/plugin install jerry@<name-from-list>`. See [Plugin not found](#plugin-not-found-after-adding-source) in Troubleshooting for more details."
> (INSTALLATION.md, lines 96, tip box)

**Analysis:**
This finding is a targeted iteration of DA-001-20260225 from the prior C4 execution. The prior finding was Critical and recommended integrating `/plugin marketplace list` as a required verification step. The current document addressed this partially by adding a tip box at Step 2 that surfaces the verification command. The tip box is present and correct.

The counter-argument: the tip box is reactive (triggered by failure) rather than proactive (integrated into the happy path). The document's primary instruction is to run `/plugin install jerry@jerry-framework`. The tip box says "if this fails, run `/plugin marketplace list`." This structure means:

1. A user runs `/plugin install jerry@jerry-framework`
2. If `jerry-framework` is correct: success
3. If `jerry-framework` is not the registered name: failure with an error message
4. User reads the tip box, runs `/plugin marketplace list`, discovers the actual name, retries

The prior Critical finding (DA-001-20260225) recommended making step 3 proactive — run the list command first, use the name shown, don't assume `jerry-framework`. The current version keeps `jerry-framework` as the primary command and the list command as a failure-recovery step. This is an improvement (the tip box exists) but is not the resolution the prior finding called for.

The specific risk: `jerry-framework` is the source name defined in the repository's `.claude-plugin/marketplace.json`. If this file changes between Jerry versions (e.g., if the project renames the source to `jerry` or `jerry-plugin` in a future version), the documented Step 2 command breaks for any user who installed the new version. The source name is a runtime variable, not a documentation constant.

This finding is downgraded from Critical to Major because the prior C4 execution has been partially addressed — the tip box is present and the troubleshooting section covers this case. However, the fundamental structure remains: users are instructed to run a command that may fail due to an assumption in the documentation.

**Impact:** Users who encounter the `jerry-framework` mismatch will fail at Step 2 and must read the tip box to recover. The recovery path is documented. However, each failed Step 2 is an unnecessary friction point that a proactive `/plugin marketplace list` verification step would eliminate.

**Recommendation:** Rewrite Step 2 to make the list command part of the happy path, not the failure path. Structure: "Step 2a: Verify the source was registered — Run `/plugin marketplace list` and confirm `jerry-framework` appears. Step 2b: Install the plugin — `/plugin install jerry@<name-from-list>`." Show the concrete `jerry-framework` name as the expected value, not as a hardcoded assumption. This converts failure-recovery into success-verification.

**Acceptance Criteria:** Step 2 of the primary install path includes a verification sub-step that runs `/plugin marketplace list` before the install command. The install command uses the name shown in the list output, not a hardcoded string. The `jerry@jerry-framework` form is shown as an example with "where `jerry-framework` is the name from the list."

---

### DA-006-it1: McConkey Voice Persists at Step-Level Instructional Content — Prior Major Finding Unaddressed [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Document-wide — multiple step-level locations |
| **Strategy Step** | Step 3 — Historical precedents of failure (prior finding); Unaddressed risks |

**Evidence:**
Navigation table:
> "| [Install from GitHub](#install-from-github) | The main line — two commands, you're riding |"
> (INSTALLATION.md, line 15)

Install from GitHub section header:
> "Jerry is a **community Claude Code plugin** hosted on [GitHub](https://github.com/geekatron/jerry). You install it directly from the GitHub repository using Claude Code's built-in plugin system. Two commands and you're riding."
> (INSTALLATION.md, line 66)

Post-verification:
> "That's your signal — you're in. Head to [Configuration](#configuration) to set up your first project, then [Verification](#verification) to confirm everything's firing."
> (INSTALLATION.md, line 104)

**Analysis:**
DA-003-20260225 (Major) in the prior C4 execution flagged "Two commands and you're riding," "you're in," and similar idioms as comprehension barriers at instructional moments. The finding was Major and recommended replacing step-level McConkey idioms with declarative technical language while preserving voice in section introductions and transitions.

The current document retains: "Two commands and you're riding" in both the navigation table description and the Install from GitHub section intro, and "you're in" as the post-verification confirmation.

These are the same specific instances flagged in DA-003-20260225. They have not been addressed.

The downgrade from Major to Minor in this iteration reflects that these phrases appear at section transitions (the navigation table entry is a descriptor, the "you're in" follows a verification step), not within numbered instructional steps themselves. The numbered steps (Step 1, Step 2, Step 3) use technical language. The voice is primarily in surrounding prose. This is closer to the acceptance criteria from DA-003-20260225 ("voice elements are present in section introductions and transitions but not in instructional content").

However, the navigation table entry "The main line — two commands, you're riding" is not a section introduction — it is the description users read when scanning the table to understand what the section covers. A non-native English speaker reading the navigation table will see "you're riding" as a purpose description and may not know what it means in this context. The table description should answer "what does this section help me do," not invoke a sports idiom.

**Impact:** Minor. The instructional steps are clear. The voice at transition points creates minor comprehension friction for non-native speakers but does not prevent install completion.

**Recommendation:** Update the navigation table entry from "The main line — two commands, you're riding" to "The main line — persistent install via Claude Code's plugin system (~2 min)." Update "you're in" in the post-verification confirmation to "Jerry is installed." These two targeted replacements resolve the remaining instances without requiring a document-wide voice review.

**Acceptance Criteria:** The navigation table entry for Install from GitHub does not use "you're riding." The post-verification confirmation in Install from GitHub uses declarative language. At minimum, these two instances are resolved.

---

### DA-007-it1: `--plugin-dir` Remains Labeled "Alternative" — Prior Major Finding DA-002-20260225 Unaddressed [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Navigation table (line 19), Which Install Method? routing table (line 58) |
| **Strategy Step** | Step 3 — Historical precedents of failure (prior finding) |

**Evidence:**
Navigation table:
> "| [Alternative: Plugin Dir Flag](#alternative-plugin-dir-flag) | Quick test drive — no plugin source setup |"
> (INSTALLATION.md, line 19)

Which Install Method? routing table:
> "| **Quick test drive** — take Jerry for a lap before committing | [Plugin Dir Flag](#alternative-plugin-dir-flag) | ~3 minutes |"
> (INSTALLATION.md, line 58)

The Plugin Dir Flag section:
> "Want to take Jerry for a lap before committing? Clone the repo and point Claude Code at it directly — no plugin source setup needed:"
> (INSTALLATION.md, line 265)

> "Note: The `--plugin-dir` flag loads the plugin for that session only. It does not persist across sessions. For persistent installation, use the GitHub install or Local Clone methods."
> (INSTALLATION.md, lines 277–278)

**Analysis:**
DA-002-20260225 (Major) in the prior C4 execution argued that `--plugin-dir` should be promoted to the primary onboarding path because it is objectively fewer steps and lower conceptual overhead for first-time users. The finding was Major and called for restructuring the install section.

The current document has added the "Which Install Method?" routing table (addressing DA-004-20260225), which now gives `--plugin-dir` a dedicated routing row as "Quick test drive." This is an improvement — the method is visible in the decision table.

However, the finding's core critique — that `--plugin-dir` is the simplest path for new users and should not be labeled "Alternative" — remains unaddressed. The section heading is still "Alternative: Plugin Dir Flag." The routing description is "Quick test drive — take Jerry for a lap before committing," which frames it as a pre-commitment evaluation, not as a valid install method for users who only want skills without persistence.

A user who installs Jerry via `--plugin-dir` to evaluate it for a team will use Jerry, find it valuable, and then need to do the "full" install anyway. The "test drive before committing" framing implies that `--plugin-dir` is not a legitimate install method — only a trial. But for users who launch Claude Code from a consistent directory, or who use Claude Code in a project-specific workflow, session-scoped loading may be entirely sufficient.

The downgrade from Major to Minor reflects that the routing table now surfaces the option and the navigation entry includes "no plugin source setup" as a value proposition. The option is discoverable. The remaining issue is framing: "Alternative" and "test drive" undersell the method for legitimate use cases.

**Impact:** Minor. The option is visible and documented. Users who want it can find it. The "Alternative" and "test drive" framing may cause users with legitimate session-scoped use cases to not consider it.

**Recommendation:** Change the section heading from "Alternative: Plugin Dir Flag" to "Plugin Dir Flag — Session Install (No Configuration)" and update the routing table description from "Quick test drive — take Jerry for a lap before committing" to "Session-only install — skills available immediately, no plugin source setup." This reframes the method as a legitimate option for specific use cases rather than a trial.

**Acceptance Criteria:** The Plugin Dir Flag section heading and routing table description do not use "test drive" or "before committing" framing. The method is described as a valid install option for session-scoped use, not exclusively as an evaluation path.

---

## Prior Execution: Finding Status

| Prior Finding | Prior Severity | Current Status | Evidence |
|---------------|---------------|----------------|---------|
| DA-001-20260225: Primary install path depends on unverifiable marketplace name | Critical | **Partially addressed** — tip box added at Step 2, but verification is reactive (failure-triggered) not proactive. Downgraded to Major (DA-005-it1). | Step 2 now has "Install command fails?" tip box with `/plugin marketplace list` command |
| DA-002-20260225: `--plugin-dir` should be primary, not alternative | Major | **Not addressed** — section heading and routing table still label it "Alternative" and "test drive." Retained as Minor (DA-007-it1) due to routing table improvement. | Navigation table and Which Install Method? table still use prior framing |
| DA-003-20260225: McConkey voice at step-level | Major | **Partially addressed** — numbered steps use technical language. Navigation table and section intros still use idioms. Retained as Minor (DA-006-it1). | "Two commands and you're riding" and "you're in" remain |
| DA-004-20260225: Three install paths create decision paralysis | Major | **Addressed** — "Which Install Method?" routing table added with clear decision criteria. | Lines 50–61, routing table present |
| DA-005-20260225: "Marketplace" terminology undefined | Major | **Addressed** — "What does 'marketplace' mean here?" explanation added at top of Install from GitHub. | Lines 68–69, explanation present |
| DA-006-20260225: Troubleshooting omits most likely failure mode | Major | **Partially addressed** — Project Issues section exists in Troubleshooting, Configuration section navigation entry now says "required for skills to work." The first troubleshooting entry is still SSH Authentication Issues, not the XML output symptom. | Lines 528–538, Project Issues present but not first |
| DA-007-20260225: Document length (607 lines) | Minor | **Not addressed** — current document is 622 lines, slightly longer than prior version. Developer Setup and Using Jerry sections remain. | Document length increased |
| DA-008-20260225: Early access caveat placement contradicts "Recommended" heading | Minor | **Addressed** — caveat now appears before the hooks table and install steps. | Lines 132–133, caveat is first element after section heading |

**Summary:** 2 of 8 prior findings fully addressed. 3 partially addressed. 3 unaddressed (2 Minor, 1 Major reduced to Minor). New Critical finding identified (DA-001-it1) not present in prior execution.

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-it1 | Remove or rewrite the "Alternative: Interactive Installation" sub-section. If retained, rewrite to describe the UI workflow that follows after source registration via CLI, not a Discover-tab browser experience for a community plugin not in the official catalog. | The Interactive Installation section does not instruct users to navigate to a Discover tab to find a community GitHub plugin. If retained, the section's description is consistent with the "marketplace is not a browse-a-store" explanation on the same page. |

### P1 — Major (SHOULD resolve; require justification if not)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-002-it1 | Update the Prerequisites SSH table row to include an inline reference to the HTTPS alternative: "Yes (for primary method; HTTPS alternative available)". | Prerequisites table row for SSH includes an inline escape path. Users who read only the table row know an alternative exists. |
| DA-003-it1 | Add a fourth routing row for "No SSH key, internet access" → Install from GitHub (use HTTPS URL) → ~2 minutes. Add an inline SSH check command. Rename "No SSH key or locked-down network" to "Offline or network-restricted." | Routing table has four rows. No-SSH users are routed to the 2-minute path, not the 5-minute path. |
| DA-004-it1 | Align Prerequisites blockquote routing guidance with the routing table. Add the HTTPS variant as a first-class routing table row. Update Prerequisites blockquote to link to the routing table row. | Prerequisites blockquote and routing table give consistent guidance for no-SSH users. HTTPS path is reachable from the routing table without passing through Local Clone. |
| DA-005-it1 | Restructure Step 2 to include a proactive verification sub-step: run `/plugin marketplace list` to confirm the source name before running the install command. | Step 2 includes a sub-step that verifies the source name from `marketplace list` before the install command. `jerry@jerry-framework` is shown as an expected-value example, not a hardcoded constant. |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-006-it1 | Update navigation table entry for Install from GitHub to remove "you're riding." Update "you're in" post-verification confirmation to declarative language. | Navigation table entry does not use "you're riding." Post-verification confirmation uses declarative language. |
| DA-007-it1 | Update Plugin Dir Flag section heading and routing table description to use "session install" framing rather than "test drive / before committing" framing. | Section heading and routing table description reflect the method as a valid install option, not exclusively an evaluation path. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001-it1 (Interactive Installation section describes a workflow that cannot complete for a community plugin), DA-004-it1 (HTTPS alternative is not reachable from the routing table for no-SSH users): two findings identify content gaps where the document fails to route users to existing correct information. |
| Internal Consistency | 0.20 | Negative | DA-001-it1 (the "marketplace is not a browse-a-store" explanation directly contradicts the "Navigate to Discover tab and find jerry" instruction in the same section), DA-003-it1 (routing table sends no-SSH users to 5-minute path while Prerequisites blockquote sends them to 2-minute path): two findings identify direct contradictions within the document. |
| Methodological Rigor | 0.20 | Mixed | DA-005-it1 (Step 2 install command depends on a source name that cannot be verified without running a separate command): the install methodology relies on an assumed constant that should be a verified variable. Partially offset by the addition of the "Which Install Method?" routing table and the marketplace explanation, which represent methodological improvements from the prior version. |
| Evidence Quality | 0.15 | Neutral | The document's claims about what the commands do are accurate. The SSH/HTTPS behavior is correctly described. The marketplace explanation is correct. The evidence quality deficit is in discoverability (findings are about navigation and routing, not factual accuracy). |
| Actionability | 0.15 | Negative | DA-002-it1 (prerequisites table sends no-SSH users to a hard stop without an inline escape path), DA-003-it1 (routing table sends no-SSH users to the wrong path), DA-005-it1 (Step 2 requires a failure cycle to discover the correct source name): three findings identify points where the document's structure leads users to suboptimal or failed actions. |
| Traceability | 0.10 | Neutral | Cross-section links are functional. The navigation table covers all sections. The troubleshooting section maps to section anchors. No traceability regressions from prior version. |

**Overall Assessment:** 1 Critical, 4 Major, 2 Minor findings. The document improved in two areas from the prior C4 execution: the marketplace terminology is now explained (DA-005-20260225 addressed), and the routing decision table was added (DA-004-20260225 addressed). However, a new Critical finding was identified (DA-001-it1: Interactive Installation describes an impossible workflow for a community plugin), and four Major findings remain that create friction for the largest user class (no-SSH users) and undermine the integrity of the install instructions.

The document should not be accepted for public OSS release without resolving the Critical finding. Four of the five Major findings can be resolved with targeted edits (routing table updates, prerequisites table update, step restructuring) without reworking the document's structure. **Recommendation: REVISE — targeted revision required, not major rework.**

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 1 (DA-001-it1)
- **Major:** 4 (DA-002-it1, DA-003-it1, DA-004-it1, DA-005-it1)
- **Minor:** 2 (DA-006-it1, DA-007-it1)
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** Confirmed — S-003 Steelman applied 2026-02-18 at `docs/reviews/adv-s003-steelman-install-docs.md`
- **H-15 Self-Review Applied:** Yes — all findings verified for: specific evidence from deliverable with line citations, justified severity classification, DA-NNN-it1 identifier format, summary table consistency with detailed findings, no findings omitted or minimized
- **Prior Findings Fully Addressed:** 2 of 8 (DA-004-20260225, DA-008-20260225)
- **Prior Findings Partially Addressed:** 3 of 8 (DA-001-20260225 → DA-005-it1 Major, DA-003-20260225 → DA-006-it1 Minor, DA-006-20260225 → partially resolved)
- **Prior Findings Unaddressed:** 3 of 8 (DA-002-20260225 → DA-007-it1 Minor, DA-007-20260225 retained, DA-001-20260225 not fully resolved)
- **New Findings Not in Prior Execution:** 1 (DA-001-it1 Critical — Interactive Installation impossible workflow)
- **Dimensions with Negative Impact:** 3 of 6 (Completeness, Internal Consistency, Actionability)
- **Dimensions with Mixed Impact:** 1 of 6 (Methodological Rigor)
- **Dimensions Neutral:** 2 of 6 (Evidence Quality, Traceability)
- **P0 Findings (block acceptance):** 1
- **P1 Findings:** 4
- **P2 Findings:** 2

---

*Strategy: S-002 Devil's Advocate*
*Template Version: 1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Finding Prefix: DA-NNN-it1*
*Execution Date: 2026-02-25*
*Prior Execution: `docs/reviews/adv-s002-devils-advocate-installation-c4.md`*

# Devil's Advocate Report: Installation Documentation Set

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `docs/INSTALLATION.md`, `docs/index.md`, `docs/BOOTSTRAP.md`, `docs/runbooks/getting-started.md`
**Criticality:** C2 (Standard)
**Date:** 2026-02-18
**Reviewer:** adv-executor agent
**H-16 Compliance:** S-003 Steelman applied 2026-02-18 — confirmed in `docs/reviews/adv-s003-steelman-install-docs.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All DA-NNN findings with severity and dimension |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and response requirements for each finding |
| [Recommendations](#recommendations) | Prioritized action list by P0/P1/P2 |
| [Scoring Impact](#scoring-impact) | Dimension-level impact from Devil's Advocate analysis |
| [Execution Statistics](#execution-statistics) | Execution metadata |

---

## Summary

10 counter-arguments identified: 3 Critical, 5 Major, 2 Minor. The documentation set makes confident claims about a two-command installation path and optional hooks that are undermined by unverified preconditions — specifically, whether the plugin is actually published to the Claude Code marketplace, whether the exact CLI command syntax is accurate, and whether the known BUG-002 hook schema validation failures contradict the "hooks work automatically" claim. Two Critical findings (DA-001, DA-002) directly attack the documentation's most prominent user-facing promises; if either counter-argument is valid, a significant portion of new users will encounter failures with no actionable resolution path in the docs. The documentation cannot be accepted in its current form without either (a) verifying the installation commands work end-to-end or (b) prominently disclosing what cannot be verified at documentation time. **Recommendation: REVISE — address all Critical and Major findings before release.**

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260218 | "Two commands" install claim is unverified — plugin may not be published | Critical | "Jerry is a public Claude Code plugin. Install it with two commands" (INSTALLATION.md, Quick Install heading) | Evidence Quality |
| DA-002-20260218 | BUG-002 hook schema validation failures contradict "hooks activate automatically" claim | Critical | "Hooks activate automatically the next time you start Claude Code — no additional configuration needed." (INSTALLATION.md, Enable Hooks section) | Internal Consistency |
| DA-003-20260218 | Marketplace name derivation claim is asserted, not demonstrated | Critical | "Remote installs (geekatron/jerry): marketplace name is geekatron-jerry" (INSTALLATION.md, Troubleshooting section) | Methodological Rigor |
| DA-004-20260218 | "Hooks are optional" framing understates the risk of operating without them | Major | Section heading reads "Enable Hooks (Recommended)" — not "Required" (INSTALLATION.md) | Actionability |
| DA-005-20260218 | `jerry session start` command is undocumented in the CLI reference | Major | "Open Claude Code in the same terminal session... You can also trigger it explicitly: jerry session start" (getting-started.md, Step 3) | Completeness |
| DA-006-20260218 | Skill auto-activation via trigger keywords is presented as reliable — no failure mode documented | Major | "The skill activates automatically when your message contains trigger keywords: research, analyze..." (getting-started.md, Step 4) | Completeness |
| DA-007-20260218 | Windows support claim overstated given "in progress" status | Major | "Windows support is actively in progress — core functionality works" vs. "In progress — core functionality works, edge cases may exist" (INSTALLATION.md header, index.md Platform Support) | Internal Consistency |
| DA-008-20260218 | No version assertion that `/plugin` command interface matches described UI | Major | "Run /plugin in Claude Code — Go to the Installed tab" (INSTALLATION.md, Verification section) | Evidence Quality |
| DA-009-20260218 | Bootstrap rollback uses `rm` on symlinks — dangerous on macOS when symlink target does not exist | Minor | "rm .claude/rules .claude/patterns # macOS/Linux" (BOOTSTRAP.md, Rollback section) | Actionability |
| DA-010-20260218 | Local clone install step 3 uses a different marketplace name than the remote install | Minor | "Local clone installs: marketplace name is jerry-framework — use /plugin install jerry@jerry-framework" (INSTALLATION.md, Troubleshooting) vs. no explicit explanation of why names differ | Methodological Rigor |

---

## Detailed Findings

### DA-001-20260218: "Two Commands" Install Claim is Unverified [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `docs/INSTALLATION.md`, Quick Install (Most Users) section; `docs/index.md`, Quick Start section |
| **Strategy Step** | Step 3 — Logical flaws, Unstated assumptions |

**Evidence:**
> "Jerry is a public Claude Code plugin. Install it with two commands in Claude Code:"
> ```
> /plugin marketplace add https://github.com/geekatron/jerry
> /plugin install jerry@geekatron-jerry
> ```
> (INSTALLATION.md, Quick Install section, lines 44–49)

Also in `docs/index.md`, Quick Start section:
> "In Claude Code, run two commands"

**Analysis:**
The documentation opens with a strong, unqualified claim: Jerry is a *public* Claude Code plugin that installs with *two commands*. This claim has three unstated preconditions that have not been verified:

1. **The GitHub repository must be configured as a valid Claude Code plugin source.** Claude Code's plugin marketplace does not automatically recognize any GitHub repository as a plugin source. The repository must contain a `claude-plugin.json` or equivalent manifest recognized by the Claude Code plugin system. The documentation does not state whether this manifest exists, is correctly structured, or has been tested against a real Claude Code installation.

2. **`/plugin marketplace add` must succeed against `https://github.com/geekatron/jerry`.** This command implies that the Claude Code plugin marketplace can resolve the repository URL at the time of user execution — meaning the repository must be public, contain the correct plugin metadata, and be resolvable by the version of Claude Code the user has installed. None of these conditions are verified in the documentation.

3. **The instruction exists in the context of an Early Access project.** `docs/index.md` explicitly states: "Jerry is under active development. The framework is functional and used in production workflows, but APIs, skill interfaces, and configuration formats may change between releases." The Quick Install instruction makes no similar caveat. A new user reading INSTALLATION.md in isolation will encounter no warning that the marketplace install path may be aspirational rather than tested.

If the plugin is not yet published to a state where `/plugin marketplace add https://github.com/geekatron/jerry` succeeds, every user who follows the Quick Install path will fail at Step 1, with no recovery path other than the Local Clone Install — which requires Git (a dependency the documentation explicitly claims is not needed: "You do **not** need Git... to install and use Jerry's skills").

The counter-argument: the documentation's most prominent claim — "install with two commands" — may be untrue at the time of publication, and the documentation provides no mechanism for a user to discover this before spending time troubleshooting.

**Impact:** If this counter-argument is valid, the Quick Install section fails for all users, the "2 commands" value proposition is false, and the fallback (Local Clone Install) silently contradicts the "no Git required" prerequisite claim.

**Dimension:** Evidence Quality

**Response Required:** The creator must provide one of: (a) evidence that `/plugin marketplace add https://github.com/geekatron/jerry` succeeds end-to-end on a fresh Claude Code 1.0.33+ installation, or (b) a disclosure in the Quick Install section that the marketplace path requires the plugin to be published, with a link to a status page or release note.

**Acceptance Criteria:** Either (a) a documented test result showing the two-command install succeeds, or (b) a sentence in the Quick Install section that reads approximately: "Note: This install path requires Jerry to be registered in the Claude Code marketplace. See [releases](https://github.com/geekatron/jerry/releases) to confirm the current release status before proceeding."

---

### DA-002-20260218: BUG-002 Hook Schema Validation Failures Contradict "Hooks Activate Automatically" Claim [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `docs/INSTALLATION.md`, Enable Hooks (Recommended) section |
| **Strategy Step** | Step 2 — Contradicting evidence; Step 3 — Unstated assumptions |

**Evidence:**
> "That's it. Hooks activate automatically the next time you start Claude Code — no additional configuration needed."
> (INSTALLATION.md, Enable Hooks section, line 137)

> "Without uv, hooks fail silently (fail-open) — skills still work, but you lose the automated guardrail enforcement that makes Jerry most effective."
> (INSTALLATION.md, Capability Matrix section, line 153)

**Analysis:**
The documentation claims hooks activate automatically after installing uv, with "no additional configuration needed." This claim is directly contradicted by an open known bug in the Jerry framework itself.

BUG-002 (documented in the project's MEMORY context) describes "Hook JSON Schema Validation Failures — L2 enforcement completely broken" with 7 root causes across 4 files: `user-prompt-submit.py`, `pre_tool_use.py`, `subagent_stop.py`, and `hooks.json`. The bug description states "L2 enforcement completely broken."

The documentation's claim — "hooks activate automatically... no additional configuration needed" — is accurate only if the hooks actually function after activation. If BUG-002 represents unfixed code that ships to users, then:

1. Users who install uv and expect L2 per-prompt enforcement (UserPromptSubmit hook) will get silent failures — the hook will not function as documented.
2. The Capability Matrix table shows "Per-prompt quality reinforcement (L2): Yes" for the "With uv" column — this entry is false if BUG-002 is not resolved before release.
3. The documentation's hooks section is the primary reason given for why users should install uv. If the hooks are broken, the instruction to install uv is providing false value.

The counter-argument does not require BUG-002 to be unresolved at release — it requires that the documentation be accurate at the time it is published. The documentation currently makes an unqualified positive claim ("hooks activate automatically") without referencing any known defect status. If BUG-002 is resolved before release, the finding is moot. If it is not, the documentation is inaccurate on a material claim.

The "fail-open" framing (hooks fail silently, skills still work) is used to minimize the consequence of hooks not working — but this framing only applies to the case where uv is *not* installed. The documentation does not disclose the case where uv is installed but hooks fail due to defects.

**Impact:** If hooks are shipped in a broken state, users who follow the Enable Hooks section will install uv, restart Claude Code, see no visible error (fail-open), and believe hooks are working when they are not. The documentation provides no mechanism to verify hook function beyond "you should see project context loading in the session output" — which will not appear if the SessionStart hook has a schema validation failure.

**Dimension:** Internal Consistency

**Response Required:** The creator must confirm: (a) BUG-002 is resolved before publication of this documentation, or (b) the documentation discloses the known hook defect status and links to a tracking issue.

**Acceptance Criteria:** Either (a) a statement that BUG-002 has been fixed and the fix is in the release branch, with a reference to the commit or PR, or (b) a note in the Hooks Verification section reading approximately: "If hooks are not firing despite uv being installed, see [known issue #NNN] for current status."

---

### DA-003-20260218: Marketplace Name Derivation Claim is Asserted, Not Demonstrated [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `docs/INSTALLATION.md`, Quick Install section (Step 2 note); Troubleshooting section |
| **Strategy Step** | Step 3 — Unstated assumptions, Historical precedents of failure |

**Evidence:**
> "Marketplace name: Run /plugin marketplace list to see your marketplace name. It should show geekatron-jerry."
> (INSTALLATION.md, Quick Install section, lines 63–64)

> "Remote installs (geekatron/jerry): marketplace name is geekatron-jerry — use /plugin install jerry@geekatron-jerry"
> "Local clone installs (~/plugins/jerry): marketplace name is jerry-framework — use /plugin install jerry@jerry-framework"
> (INSTALLATION.md, Troubleshooting section, lines 430–433)

**Analysis:**
The documentation asserts with certainty that the marketplace name for a remote install will be `geekatron-jerry` and for a local clone install will be `jerry-framework`. These assertions carry two implicit claims that are not verified:

1. **The naming algorithm is deterministic and documented.** The documentation implies that Claude Code derives the marketplace name predictably from the URL (replacing `/` with `-` for remote installs, using the directory name for local installs). However, the documentation does not cite the Claude Code documentation for this behavior, test it on the specified version (1.0.33+), or acknowledge that the naming algorithm could change in future Claude Code versions.

2. **The derivation from directory name for local installs is assumed, not verified.** A user who clones to `~/plugins/jerry` is told the marketplace name will be `jerry-framework`, not `jerry`. This means the directory name (`jerry`) does not directly map to the marketplace name — there is an additional `-framework` suffix. The documentation does not explain where the `-framework` suffix comes from, which means a user whose local clone produces a different name (e.g., after a Claude Code version update) has no framework for diagnosing the discrepancy.

3. **The install command `jerry@jerry-framework` in Step 3 of the Local Clone Install section is presented as a fixed string.** If the marketplace name differs (e.g., user clones to a different directory, or Claude Code version changes the naming algorithm), the install command fails with "plugin not found" — a failure the Troubleshooting section addresses but the primary install path does not.

The counter-argument: the documentation asserts specific marketplace names as facts rather than as observed outcomes that could vary. The S-003 Steelman report flagged this as SM-004 (two-step install pattern unexplained) — the Devil's Advocate finding is more specific: the particular name values `geekatron-jerry` and `jerry-framework` are presented as known facts but are actually empirical claims about Claude Code's internal naming algorithm that have not been verified in documentation.

**Impact:** Users who get a different marketplace name than documented will encounter "plugin not found" and have no diagnostic path other than running `/plugin marketplace list` — which is mentioned in the troubleshooting section but not in the primary install path as a diagnostic step before attempting install.

**Dimension:** Methodological Rigor

**Response Required:** The creator must provide: (a) citation of the Claude Code documentation that specifies how marketplace names are derived, or (b) test evidence showing the exact names produced by the commands on a clean install, or (c) revision of the install instructions to use `/plugin marketplace list` as a required diagnostic step before running `/plugin install`.

**Acceptance Criteria:** One of: (a) a footnote citing the Claude Code docs on marketplace name derivation, (b) a note in the install steps stating "The exact marketplace name depends on Claude Code's internal naming — run `/plugin marketplace list` and use the name shown in the `@suffix`", or (c) documentation of the test case confirming `geekatron-jerry` and `jerry-framework` are the actual names produced.

---

### DA-004-20260218: "Enable Hooks (Recommended)" Framing Understates the Risk of Skipping [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Enable Hooks section header; `docs/index.md`, Quick Start Step 2 |
| **Strategy Step** | Step 3 — Alternative interpretations; Step 2 — Unstated assumptions |

**Evidence:**
> "### Enable Hooks (Recommended)"
> (INSTALLATION.md, section heading)

> "### 2. Enable Hooks (Optional)"
> (index.md, Quick Start section heading — note the label is "Optional" here vs. "Recommended" in INSTALLATION.md)

> "Without uv, hooks fail silently (fail-open) — skills still work, but you lose the automated guardrail enforcement that makes Jerry most effective."
> (INSTALLATION.md, Capability Matrix section)

**Analysis:**
The hook installation section is labeled "Recommended" in INSTALLATION.md and "Optional" in index.md — an inconsistency the S-003 report did not flag. More critically, the framing of hooks as optional (or merely recommended) is in tension with the framework's own quality enforcement claims.

The documentation elsewhere asserts that Jerry's value proposition includes: L2 per-prompt quality reinforcement, L3 pre-tool-call AST validation, and P-003 subagent hierarchy enforcement at the hook layer. The quality-enforcement framework defines a 5-layer enforcement architecture where L2–L4 are hook-dependent. The documentation's own Capability Matrix confirms that without uv, per-prompt quality reinforcement, pre-tool-call validation, and subagent enforcement are all absent.

The counter-argument: calling hooks "optional" or merely "recommended" for a framework whose core value proposition is behavioral guardrails is logically inconsistent. A user who installs Jerry as a skill-only tool (without hooks) is using approximately 40% of the advertised functionality (skills only), but the documentation frames this as a reasonable default for "most users" — the Quick Install section makes no mention of hooks.

Specifically: the "Quick Install (Most Users)" section installs only skills. The Enable Hooks section is a separate step that a user can skip. The index.md Quick Start labels hooks as "Optional." This framing implies that skill-only use is the common case and that the framework is substantially useful without hooks. But the documented core value proposition ("Context Rot," "behavioral guardrails," "rule re-injection") is entirely dependent on hooks. A user who skips hooks has a framework that provides structured prompts (skills) but none of the behavioral enforcement.

**Impact:** Users who follow the Quick Install and skip the hooks section will use Jerry as a prompt-template system only, will encounter context rot (the problem Jerry claims to solve), and will not understand why. The documentation has given them no clear signal that they have opted out of the framework's primary safety mechanism.

**Dimension:** Actionability

**Response Required:** Revise the framing so it accurately conveys the consequence of skipping hooks. The current "Recommended" label with the note "skills still work" implies hooks are an enhancement — the documentation should clearly state that hooks are the behavioral enforcement layer and that skipping them leaves the core anti-context-rot features inactive.

**Acceptance Criteria:** Either (a) the Enable Hooks section is relabeled "Required for Full Function" with a clear note that the behavioral guardrail features depend on hooks, or (b) the Quick Install section includes a one-line note: "Note: The two-command install provides Jerry's skills. For behavioral guardrails and context rot mitigation, complete Step 3 (Enable Hooks)." Also: resolve the "Recommended" vs. "Optional" inconsistency between INSTALLATION.md and index.md.

---

### DA-005-20260218: `jerry session start` Command is Undocumented and Unverifiable [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/runbooks/getting-started.md`, Step 3 |
| **Strategy Step** | Step 2 — Unstated assumptions; Step 3 — Logical flaws |

**Evidence:**
> "Open Claude Code in the same terminal session where JERRY_PROJECT is set. Jerry's SessionStart hook runs automatically when Claude Code starts. You can also trigger it explicitly:
> ```
> jerry session start
> ```"
> (getting-started.md, Step 3, lines 99–104)

Also from `docs/CLAUDE.md` Quick Reference:
> `jerry session start|end|status|abandon` — CLI v0.2.2

**Analysis:**
The `jerry session start` command is presented as a way to explicitly trigger the SessionStart hook. This claim has a critical unstated assumption: the `jerry` CLI must be on the user's PATH. The Getting Started runbook's prerequisites list Claude Code 1.0.33+, Jerry plugin installation, and uv — it does not mention the Jerry CLI or how to install it.

A user who has installed Jerry as a plugin via `/plugin install jerry@geekatron-jerry` has access to Jerry's *skills* within Claude Code, but may not have access to the `jerry` CLI binary on their system PATH. The INSTALLATION.md Troubleshooting section notes: "jerry: command not found — The Jerry CLI is not on your PATH, or the plugin is not installed." This troubleshooting entry confirms the failure mode exists but does not explain how to resolve it for a user who installed via plugin (as opposed to a developer who cloned the repository).

The documentation creates a false equivalence: installing Jerry as a Claude Code plugin and having the `jerry` CLI available are presented as the same outcome, but they may not be. The Getting Started runbook uses `jerry session start` as an explicit verification step — if this command is not available for plugin-only users, Step 3 of the runbook fails for the majority of users following the recommended Quick Install path.

Additionally, the CLAUDE.md Quick Reference states CLI version 0.2.2 — but the Getting Started runbook's tested versions note "Jerry CLI v0.2.0." This version mismatch is unexplained.

**Impact:** Users who installed via the Quick Install plugin path may have no `jerry` CLI command, making Step 3 of the Getting Started runbook fail at the explicit trigger step. The fallback (Claude Code auto-starting the hook) is not verifiable without the CLI, leaving users with no way to confirm the hook ran successfully.

**Dimension:** Completeness

**Response Required:** Clarify whether `jerry session start` is available to plugin-only users or only to developers who cloned the repository. If it is not available to plugin users, remove the command from the Getting Started runbook and replace it with an alternative verification method. Also resolve the CLI version mismatch between CLAUDE.md (v0.2.2) and getting-started.md (v0.2.0).

**Acceptance Criteria:** One of: (a) a note in the Getting Started prerequisites confirming the `jerry` CLI is available after plugin install and how to verify it, or (b) removal of the `jerry session start` explicit trigger and replacement with a plugin-appropriate verification (e.g., "Open Claude Code and check for `<project-context>` in the session output").

---

### DA-006-20260218: Skill Auto-Activation via Trigger Keywords Presented as Reliable with No Documented Failure Modes [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/runbooks/getting-started.md`, Step 4 |
| **Strategy Step** | Step 3 — Unaddressed risks |

**Evidence:**
> "The skill activates automatically when your message contains trigger keywords: **research**, **analyze**, **investigate**, **explore**, **root cause**, or **why**."
> (getting-started.md, Step 4, lines 128–129)

> "Expected behavior: Claude responds by activating the problem-solving skill — you will see a message indicating which agent was selected (e.g., 'Invoking ps-researcher...') and where its output will be saved"
> (getting-started.md, Step 4, lines 148–150)

**Analysis:**
The documentation presents skill auto-activation as a simple, reliable mechanism: include a trigger keyword, and the skill activates. This claim contains several unstated risks:

1. **Trigger keyword matching is LLM-mediated, not deterministic.** The skills activate because the CLAUDE.md and rules files instruct the LLM to invoke them when trigger keywords are present. This is behavioral guidance, not code — the LLM may not invoke a skill even when the keyword is present if the instruction has been lost to context rot (the very problem Jerry is designed to solve). The documentation presents skill activation as if it is a deterministic lookup, when it is fundamentally a probabilistic LLM behavior.

2. **The trigger keyword `why` is too broad to be reliable.** A user asking "Why is Python popular?" would contain the trigger keyword `why` but is a general question, not a research task. The documentation implies `why` reliably triggers `/problem-solving`, but a general question with `why` may or may not activate the skill depending on the LLM's context interpretation.

3. **The documented expected behavior ("you will see a message indicating which agent was selected") is not guaranteed.** The LLM may activate the skill internally and produce output without the expected agent-selection message, or may produce a response that does not match the expected output pattern the user is looking for. The Getting Started runbook's verification step relies on the user recognizing a specific output pattern that is described but not shown as a concrete example.

4. **No troubleshooting entry exists for "skill keyword present but skill did not activate."** The troubleshooting table in getting-started.md has an entry for "`<project-context>` appears but skill does not activate" — but this entry attributes the cause to "trigger keyword not present" and suggests using one of the "exact trigger keywords." This guidance is circular: it tells the user to use the exact keywords, but does not acknowledge that using exact keywords does not guarantee activation.

**Impact:** A new user who follows Step 4 exactly, uses an exact trigger keyword, but does not see the expected activation message will have no diagnostic path. They will not know whether the skill did not activate, activated silently, or the expected output format changed.

**Dimension:** Completeness

**Response Required:** Add a disclosure that skill activation is LLM-mediated behavior, not deterministic code. Revise the trigger keyword list to note that `why` is a broad keyword that may not reliably trigger the skill. Add a fallback explicit invocation path (e.g., `/problem-solving research X`) for users where keyword activation does not work.

**Acceptance Criteria:** The Step 4 description includes: (a) a note that explicit skill invocation (`/problem-solving`) is always available as a fallback, and (b) the expected output section is a concrete example block (as recommended by SM-007) rather than a textual description, so users can verify success against a concrete pattern.

---

### DA-007-20260218: Windows Support Claim Overstated Relative to "In Progress" Status [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, header Platform Note; `docs/index.md`, Platform Support section |
| **Strategy Step** | Step 3 — Internal consistency |

**Evidence:**
INSTALLATION.md header (lines 4–5):
> "Windows support is actively in progress — core functionality works, but some hooks may behave differently."

index.md Platform Support table (line 59):
> "Windows | In progress — core functionality works, edge cases may exist"

INSTALLATION.md Windows-specific sections: Complete Windows instructions are present throughout (PowerShell commands for all major operations, specific Windows troubleshooting entries, Windows-specific path handling).

**Analysis:**
The documentation provides complete Windows instructions throughout INSTALLATION.md — PowerShell equivalents for every bash command, Windows-specific troubleshooting entries, Windows path handling guidance. This thoroughness creates an implicit claim that Windows is a supported platform in practice.

However, the platform note caveats Windows as "in progress" and "edge cases may exist." These two signals are in tension: the documentation is detailed enough for Windows to suggest full support, but the platform note warns users that behavior may differ.

The specific counter-argument: "some hooks may behave differently" (INSTALLATION.md header) is vague and not quantified. A Windows user cannot determine from this statement which hooks may behave differently, in what way, or how to detect whether they are experiencing a documented "edge case" vs. a real bug. The BOOTSTRAP.md Windows section says junction points "must be on the same drive as the source" — this is a concrete limitation, but the INSTALLATION.md platform note does not flag it.

Additionally, INSTALLATION.md's Developer Setup section states "See CONTRIBUTING.md for the full Make target equivalents table" — but the CONTRIBUTING.md file is linked as `https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md`, which is an external link to a repository that may not yet be public or may not contain the referenced table. A Windows developer following the setup instructions who encounters `make` errors is directed to an external file that may not exist.

**Impact:** Windows users will invest effort setting up Jerry based on complete-looking documentation, then encounter unspecified "edge cases" with no diagnostic path. The vagueness of "some hooks may behave differently" is not actionable.

**Dimension:** Internal Consistency

**Response Required:** Either (a) enumerate which specific hooks are known to behave differently on Windows and what the behavioral difference is, or (b) revise the Windows instructions to carry a more prominent "Windows is not fully supported" warning at the start of each Windows section rather than only in the header note. Verify the CONTRIBUTING.md link is live and contains the referenced table.

**Acceptance Criteria:** The Windows platform caveat names at least one concrete known limitation or links to a Windows-specific tracking issue. The CONTRIBUTING.md link is verified to exist and contain the Make target equivalents table.

---

### DA-008-20260218: No Version Assertion That `/plugin` UI Matches Described Interface [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Verification section; Quick Install section |
| **Strategy Step** | Step 2 — Unstated assumptions |

**Evidence:**
> "1. Run /plugin in Claude Code
> 2. Go to the **Installed** tab
> 3. Confirm jerry appears in the list"
> (INSTALLATION.md, Quick Install section, lines 68–70)

> "1. Run /plugin
> 2. Go to the **Errors** tab
> 3. Verify no errors related to jerry"
> (INSTALLATION.md, Verification — Check for errors, lines 281–283)

> "Check the **Errors** tab in /plugin" (INSTALLATION.md, Troubleshooting — Skills not appearing)

**Analysis:**
The documentation repeatedly references specific UI elements of the `/plugin` command: the "Installed" tab, the "Discover" tab, and the "Errors" tab. These UI elements are treated as known, stable facts about Claude Code's interface.

The documentation specifies Claude Code version 1.0.33+ as a prerequisite but does not state which version of Claude Code introduced the tabbed `/plugin` interface. The Claude Code changelog history is not referenced anywhere in the documentation. A user with Claude Code 1.0.33 may have a different `/plugin` UI than a user with a later version — the tabs may have been added in a version after 1.0.33, may have different names, or the tab-based navigation may have been replaced in newer versions.

The verification procedure is entirely dependent on the `/plugin` command showing these specific tabs. If the UI has changed — or if the tabs were not present in all supported versions — the verification procedure fails silently. The user runs `/plugin`, sees a different interface, and has no diagnostic path.

**Impact:** Users on the minimum supported version (1.0.33) or on future versions where the UI has changed will follow verification instructions that do not match their actual interface. The only indication that this might be version-dependent is the minimum version prerequisite, which is not linked to the UI description.

**Dimension:** Evidence Quality

**Response Required:** Either (a) confirm which Claude Code version introduced the tabbed `/plugin` interface and update the minimum version requirement if needed, or (b) add screenshots or version-pinned notes to the verification sections, or (c) add an alternative verification method that does not depend on the UI structure (e.g., a command-line verification).

**Acceptance Criteria:** The verification section includes a note about which Claude Code version the described UI applies to, or provides a version-agnostic verification path.

---

### DA-009-20260218: Bootstrap Rollback `rm` Command Is Potentially Destructive on macOS [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/BOOTSTRAP.md`, Rollback section |
| **Strategy Step** | Step 3 — Unaddressed risks |

**Evidence:**
> "# 1. Remove the symlinks/junctions
> rm .claude/rules .claude/patterns        # macOS/Linux
> # On Windows: rmdir .claude\rules .claude\patterns"
> (BOOTSTRAP.md, Rollback section, lines 141–142)

**Analysis:**
On macOS/Linux, `rm` on a symlink removes the symlink itself — which is the correct behavior here. However, the comment `# macOS/Linux` following the `rm` command conflates two platforms that have different `rm` defaults. More importantly, the command is presented as safe without a caveat: if `.claude/rules` is a regular directory (not a symlink) — for example, on a developer who is in a file-copy fallback state per the BOOTSTRAP.md Platform Notes — running `rm .claude/rules` will fail because `rm` without `-r` cannot remove directories.

The S-003 Steelman (SM-011) flagged a related issue about Windows junction rollback. The Devil's Advocate finding extends this: even on macOS, the rollback command assumes the current state is "symlinked" when it may be in "file copy fallback" state (per the BOOTSTRAP.md Platform Notes table). A developer in file-copy fallback who runs the rollback command will see an error and be left in an intermediate state.

**Impact:** Minor — this only affects developers (contributors), not plugin users. But a failed rollback in file-copy fallback state leaves `.claude/rules` in an inconsistent state with no guidance on recovery.

**Dimension:** Actionability

**Response Required:** Add a note: "If you are in file-copy fallback state (non-symlinked), use `rm -r .claude/rules .claude/patterns` instead." Acknowledgment sufficient; explicit revision optional.

**Acceptance Criteria:** Acknowledgment in the rollback section that the `rm` command applies to symlink state only; file-copy fallback state requires `rm -r`.

---

### DA-010-20260218: Local Clone Marketplace Name `jerry-framework` Has No Explained Derivation [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Local Clone Install — Step 3; Troubleshooting section |
| **Strategy Step** | Step 2 — Unstated assumptions |

**Evidence:**
> "/plugin install jerry@jerry-framework"
> (INSTALLATION.md, Local Clone Install, Step 3, line 199)

> "Local clone installs (~/plugins/jerry): marketplace name is jerry-framework — use /plugin install jerry@jerry-framework"
> (INSTALLATION.md, Troubleshooting, line 433)

**Analysis:**
A user who clones to `~/plugins/jerry` is instructed to use the marketplace name `jerry-framework`. The directory they cloned into is named `jerry`, not `jerry-framework`. The documentation does not explain where the `-framework` suffix comes from. If the marketplace name is derived from the directory name (as implied by the pattern), cloning to `~/plugins/jerry` should produce marketplace name `jerry`, not `jerry-framework`.

This is a concrete instance of the DA-003 finding at the Minor level: the local clone marketplace name `jerry-framework` is stated as a fact but its derivation is unexplained and seemingly inconsistent with the directory name `jerry`. A user who clones to a different directory (e.g., `~/tools/jerry`) will get a different marketplace name and the install command `jerry@jerry-framework` will fail.

**Impact:** Minor — the Troubleshooting section's advice "run `/plugin marketplace list` to see the actual marketplace name" provides a recovery path. But the primary install instructions give a specific name that may be wrong, sending users to troubleshooting unnecessarily.

**Dimension:** Methodological Rigor

**Response Required:** Add a note in Step 3 of the Local Clone Install explaining that the marketplace name is derived from the directory name and may differ if the user cloned to a non-default path. Suggest running `/plugin marketplace list` first. Acknowledgment sufficient.

**Acceptance Criteria:** Step 3 of the Local Clone Install includes a note: "The marketplace name is based on your clone directory name. If you used a non-default path, run `/plugin marketplace list` to see your actual marketplace name before running `/plugin install`."

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-20260218 | Verify that `/plugin marketplace add https://github.com/geekatron/jerry` succeeds on a fresh Claude Code 1.0.33+ installation, OR add a disclosure note in the Quick Install section that the marketplace path requires the plugin to be published. | Documented test result, OR a sentence in the Quick Install section disclosing the marketplace publication prerequisite. |
| DA-002-20260218 | Confirm BUG-002 (hook schema validation failures) is resolved before publishing this documentation, OR add a note in the Hooks Verification section pointing to the tracking issue for known hook defects. | Statement that BUG-002 is fixed with reference to the fix commit/PR, OR a note in the verification section referencing the open bug. |
| DA-003-20260218 | Cite the Claude Code documentation that defines how marketplace names are derived, OR provide test evidence showing `geekatron-jerry` and `jerry-framework` are the actual names produced, OR revise the install instructions to instruct users to run `/plugin marketplace list` before attempting `/plugin install`. | One of the three listed approaches implemented. |

### P1 — Major (SHOULD resolve; require justification if not)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-004-20260218 | Resolve "Recommended" vs. "Optional" inconsistency between INSTALLATION.md and index.md. Revise framing to clearly communicate that hooks are the behavioral enforcement layer, not an enhancement. | Consistent label across both documents; Quick Install section notes that hooks enable behavioral guardrails. |
| DA-005-20260218 | Clarify whether `jerry session start` is available to plugin-only users. If not, remove from Getting Started runbook and provide an alternative. Resolve CLI version mismatch (v0.2.2 vs. v0.2.0). | Clear statement of who can use `jerry session start`; consistent version number; plugin-user-appropriate verification path. |
| DA-006-20260218 | Add a note that skill activation is LLM-mediated (not deterministic), document the explicit invocation fallback (`/problem-solving`), and add a concrete expected output block (SM-007 resolution). | Disclosure of probabilistic nature; explicit invocation documented as fallback; concrete output example block. |
| DA-007-20260218 | Name at least one concrete known Windows limitation or link to a Windows tracking issue. Verify CONTRIBUTING.md link is live and contains the Make target equivalents table. | Named limitation or tracking issue; CONTRIBUTING.md link verified live with referenced content. |
| DA-008-20260218 | Confirm which Claude Code version introduced the tabbed `/plugin` interface. Add a version-pinned note or version-agnostic alternative verification. | Version note in verification section, or alternative verification method that does not depend on UI tab names. |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-009-20260218 | Add caveat to BOOTSTRAP.md Rollback section that `rm` applies to symlink state; file-copy fallback requires `rm -r`. | Acknowledgment of the distinction; optional revision. |
| DA-010-20260218 | Add note in Local Clone Install Step 3 that marketplace name derives from clone directory name; suggest `/plugin marketplace list` verification. | Note added; acknowledgment sufficient. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-005 (CLI undocumented for plugin users), DA-006 (no explicit invocation fallback, no concrete output example), DA-007 (Windows limitations unnamed): three Major findings identify gaps in coverage. Users following the documented paths will encounter undocumented failure modes. |
| Internal Consistency | 0.20 | Negative | DA-002 (hook status contradicts BUG-002), DA-004 ("Recommended" vs. "Optional" inconsistency across documents), DA-007 (complete Windows instructions vs. "in progress" caveat): the documentation makes claims that are inconsistent with known defect state and inconsistent across its own documents. |
| Methodological Rigor | 0.20 | Negative | DA-003 (marketplace name derivation asserted without citation), DA-010 (local clone name unexplained): key instructions depend on specific string values that are not derived from documented behavior. |
| Evidence Quality | 0.15 | Negative | DA-001 (two-command claim unverified), DA-008 (UI tab names assumed stable across versions): the most prominent user-facing claims are unverified assertions about Claude Code's behavior. |
| Actionability | 0.15 | Negative | DA-004 (hooks framed as optional when they are the primary enforcement layer), DA-006 (no explicit invocation fallback), DA-009 (rollback edge case undocumented): users making informed decisions about whether to install hooks lack the information needed to understand the consequence. |
| Traceability | 0.10 | Neutral | Cross-document links are consistent and present. H-04, P-002, P-003 citations are accurate. Links to external docs (CONTRIBUTING.md) are the sole traceability concern (DA-007) but this affects Completeness more than traceability. |

**Overall Assessment:** Major revision required. Three Critical findings (DA-001, DA-002, DA-003) attack the documentation's most prominent claims — the two-command install, the automatic hook activation, and the marketplace name derivation. If any of these counter-arguments are valid, a significant fraction of new users will encounter failures that the documentation does not help them diagnose. The five Major findings are addressable but represent meaningful coverage gaps and internal inconsistencies. The documentation should not be published until the Critical findings are either resolved or disclosed.

---

## Execution Statistics

| Field | Value |
|-------|-------|
| Strategy | S-002 Devil's Advocate |
| Execution ID | 20260218 |
| Template | `.context/templates/adversarial/s-002-devils-advocate.md` |
| Documents Examined | 4 (INSTALLATION.md, index.md, BOOTSTRAP.md, getting-started.md) |
| Prior Strategy Output | `docs/reviews/adv-s003-steelman-install-docs.md` (S-003 Steelman — H-16 satisfied) |
| Total Findings | 10 |
| Critical | 3 |
| Major | 5 |
| Minor | 2 |
| Protocol Steps Completed | 5 of 5 |
| H-16 Compliance | Confirmed — S-003 Steelman applied 2026-02-18 before this execution |
| H-15 Self-Review | Applied — findings verified for: specific evidence, justified severity, consistent identifiers, no omissions |
| P0 Findings | 3 (block acceptance) |
| P1 Findings | 5 |
| P2 Findings | 2 |
| Dimensions with Negative Impact | 5 of 6 |
| Dimensions Neutral | 1 of 6 (Traceability) |

---

*Strategy: S-002 Devil's Advocate*
*Template Version: 1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Execution Date: 2026-02-18*
*Finding Prefix: DA-NNN-20260218*

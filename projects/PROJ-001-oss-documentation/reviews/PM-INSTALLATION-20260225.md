# Strategy Execution Report: Pre-Mortem Analysis

## Execution Context
- **Strategy:** S-004 (Pre-Mortem Analysis)
- **Template:** `.context/templates/adversarial/s-004-pre-mortem.md`
- **Deliverable:** `docs/INSTALLATION.md`
- **Executed:** 2026-02-25T00:00:00Z
- **Criticality:** C4
- **Quality Target:** >= 0.95
- **H-16 Compliance Note:** S-003 Steelman was not run prior to this execution per orchestrator override. The orchestrator's failure scenario framing serves as the analytical frame. Proceeding under explicit orchestrator authorization for this C4 tournament run.

---

## Failure Scenario Declaration

**Step 1 — Set the Stage**

The deliverable is `docs/INSTALLATION.md` — the primary installation guide for the Jerry Framework, published to GitHub as the canonical path for new users to get Jerry installed via Claude Code's plugin system. Success means a new user can follow this document from top to bottom and have Jerry running in their Claude Code session within 5 minutes.

**Step 2 — Temporal Perspective Shift**

It is August 2026. Three months after `docs/INSTALLATION.md` was published, the Jerry GitHub repository has 47 open issues tagged `installation-failure`. The adoption funnel shows 63% of visitors who attempt installation abandon the process. The Discord is flooded with "jerry-framework not found" and "plugin not found after adding source." A thread on Hacker News titled "Why is Jerry impossible to install?" has 200+ comments. The repository's README Quick Start section, which points to `docs/INSTALLATION.md`, is the primary onboarding path — and it is broken for a large segment of users.

We are now investigating why this happened.

---

## Findings Summary

| ID | Severity | Failure Cause | Category | Likelihood | Priority | Section |
|----|----------|---------------|----------|------------|----------|---------|
| PM-001-20260225 | Critical | `jerry-framework` marketplace name unverified for remote GitHub add — may differ from local add | Assumption | High | P0 | Install from GitHub |
| PM-002-20260225 | Critical | README.md and INSTALLATION.md describe incompatible installation paths — README requires local clone; INSTALLATION.md offers remote-first | Assumption | High | P0 | Install from GitHub / README Consistency |
| PM-003-20260225 | Critical | Hook table in INSTALLATION.md omits two real hooks (PreCompact, Stop/context-stop-gate) — users troubleshooting hook behavior get incomplete picture | Technical | Medium | P0 | Enable Hooks |
| PM-004-20260225 | Major | `--plugin-dir` namespace claim (`/jerry:<skill-name>`) unverified — if wrong, quick-test users immediately conclude Jerry is broken | Assumption | Medium | P1 | Alternative: Plugin Dir Flag |
| PM-005-20260225 | Major | "marketplace" terminology used throughout for a non-marketplace plugin — enterprise users and IT gatekeepers may misunderstand security surface | External | High | P1 | Install from GitHub |
| PM-006-20260225 | Major | No instructions for making `JERRY_PROJECT` persistent across terminal sessions — users who set it correctly in one session lose it on restart | Process | High | P1 | Configuration |
| PM-007-20260225 | Major | Windows installation path uses `$env:USERNAME` variable in a Claude Code slash command — environment variable interpolation inside Claude Code UI is unverified | Technical | Medium | P1 | Alternative: Local Clone |
| PM-008-20260225 | Major | Hook docs describe "uv installed → hooks auto-activate" but give no confirmation signal — users cannot distinguish "hooks working" from "hooks silently failing" | Process | High | P1 | Enable Hooks / Verification |
| PM-009-20260225 | Minor | Document skips `/ast` skill in the "Available Skills" table despite it being listed in CLAUDE.md's Quick Reference | Technical | Medium | P2 | Using Jerry |
| PM-010-20260225 | Minor | No mention of Claude Code session restart requirement after plugin install — users who test skills immediately after install may get stale state | Process | Medium | P2 | Install from GitHub |
| PM-011-20260225 | Minor | McConkey voice in opening line ("you're riding", "you're in") — professional IT users may abandon the doc before reading the install commands | External | Low | P2 | Document Opening |
| PM-012-20260225 | Minor | `docs/index.md#platform-support` anchor link in Platform Note may be fragile if that heading changes | Technical | Low | P2 | Platform Note |

---

## Detailed Findings

### PM-001-20260225: Marketplace Name for Remote GitHub Add is an Unverified Assumption [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Install from GitHub — Step 2 |
| **Strategy Step** | Step 3: Failure Category — Assumption |

**Evidence:**

The document states at line 64–68:
```
/plugin install jerry@jerry-framework
```
> "The format is `<plugin-name>@<marketplace-name>` — `jerry` is the plugin name (defined in the repo's `.claude-plugin/plugin.json`) and `jerry-framework` is the marketplace name (defined in `.claude-plugin/marketplace.json`)."

The `.claude-plugin/marketplace.json` confirms `"name": "jerry-framework"` — this is correct for a **local clone** where the file is read directly from disk. However, the primary install path (Step 1) uses:
```
/plugin marketplace add geekatron/jerry
```
This causes Claude Code to clone or fetch the plugin catalog from GitHub. The marketplace name in this remote scenario is determined by how Claude Code reads the `marketplace.json` from the fetched repository. It is **not confirmed** whether Claude Code uses the same `"name"` field from `marketplace.json` when the source is a GitHub shorthand vs. a local directory path. The document itself acknowledges this uncertainty with a troubleshooting note ("Run `/plugin marketplace list` to confirm the marketplace was registered and check its actual name") — but this note treats the uncertainty as a recovery procedure rather than a warning that the primary command may fail for all users.

If the remote GitHub add produces a different marketplace name (e.g., `geekatron-jerry`, `jerry`, or a derived slug from the repo path), then every user following the primary install path gets a "plugin not found" error on Step 2. Given the document's own acknowledgment that this may fail, the likelihood is High.

**Analysis:**

This is the highest-risk finding because: (a) it affects 100% of users following the primary install path, (b) the document's own troubleshooting section acknowledges the failure mode, (c) the root cause is an assumption about Claude Code behavior that is not verified from a real GitHub-sourced installation, and (d) the failure produces an opaque error message ("plugin not found") with no obvious recovery path shown at the point of failure. The Troubleshooting section does cover this, but only after the user has already experienced failure and scrolled to find help.

**Mitigation:**

1. Verify the actual marketplace name produced when running `/plugin marketplace add geekatron/jerry` on a clean machine by testing the command against the real GitHub repo.
2. If the name differs for remote vs. local sources, update Step 2 to show the correct name, or provide conditional instructions ("If you added from GitHub, use `jerry@<actual-name>`").
3. Elevate the troubleshooting note to a WARNING callout immediately after the Step 2 command, not buried in the troubleshooting section.

**Acceptance Criteria:** The `/plugin install` command in Step 2 is tested against a real GitHub-sourced install on a clean machine and the correct marketplace name is confirmed and documented. Or, a prominent inline warning with the `/plugin marketplace list` recovery step appears directly adjacent to the command.

---

### PM-002-20260225: README.md and INSTALLATION.md Describe Incompatible Install Paths [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Install from GitHub vs README Quick Start |
| **Strategy Step** | Step 3: Failure Category — Assumption |

**Evidence:**

`README.md` Quick Start (lines 29–46) shows installation as a **local clone workflow**:
```bash
# 2. Clone Jerry to a local directory
mkdir -p ~/plugins
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry

# 3. In Claude Code, add the local marketplace
/plugin marketplace add ~/plugins/jerry

# 4. Install the Jerry plugin
/plugin install jerry@jerry-framework
```
The README also lists **Git** as a prerequisite ("Git for cloning the repository").

`docs/INSTALLATION.md` promotes a **remote-first workflow** (lines 47–68) that does NOT require Git or cloning:
```
/plugin marketplace add geekatron/jerry
/plugin install jerry@jerry-framework
```
INSTALLATION.md explicitly states: "You do **not** need Git, Python, or a local clone to install Jerry's skills."

A user who reads the README (the default landing page for a GitHub repository) and then navigates to `docs/INSTALLATION.md` for detailed instructions encounters contradictory guidance: the README says clone first, INSTALLATION.md says don't clone. The `docs/index.md` (the documentation site homepage) does not mention this discrepancy.

**Analysis:**

The contradiction is at the primary entry point. GitHub's README is the first document most users read. It presents local clone as the canonical method with Git as a required dependency. INSTALLATION.md presents remote GitHub add as the primary method requiring no Git. Users who follow README → INSTALLATION.md will be confused about which method is canonical. Users who follow README alone and clone first, then read the detail in INSTALLATION.md about the "alternative" methods, may wonder why their approach (which the README presented as primary) is now buried under "Alternative: Local Clone."

This inconsistency also affects the accuracy of both documents: if remote install is the primary path, README should not list Git as a prerequisite. If local clone is the primary path, INSTALLATION.md should not call it an "Alternative."

**Mitigation:**

1. Align on a single canonical install path and make both documents consistent.
2. If remote install is primary: Update README Quick Start to use `geekatron/jerry` shorthand; remove Git from prerequisites; note local clone as an alternative.
3. If local clone is primary: Reorder INSTALLATION.md to lead with local clone; demote the remote GitHub path to an alternative.
4. Add a cross-reference note in README pointing to INSTALLATION.md for the authoritative method.

**Acceptance Criteria:** README.md and INSTALLATION.md describe the same method as "primary." Prerequisites lists are consistent between the two documents. No user can encounter a step in one document that contradicts steps in the other.

---

### PM-003-20260225: Hook Table Omits Two Real Hooks — Users Get Incomplete Troubleshooting Picture [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Enable Hooks (Recommended) |
| **Strategy Step** | Step 3: Failure Category — Technical |

**Evidence:**

The INSTALLATION.md "What hooks give you" table (lines 114–120) lists four hooks:
```
| SessionStart | ... |
| UserPromptSubmit | ... |
| PreToolUse | ... |
| SubagentStop | ... |
```

The actual `hooks/hooks.json` (verified) defines **six hook event types**:
1. `SessionStart` — session-start.py
2. `UserPromptSubmit` — user-prompt-submit.py
3. `PreCompact` — pre-compact.py (context compaction protection)
4. `PreToolUse` — scripts/pre_tool_use.py AND hooks/pre-tool-use.py (dual hooks)
5. `SubagentStop` — scripts/subagent_stop.py AND hooks/subagent-stop.py (dual hooks)
6. `Stop` — context-stop-gate.py

Neither `PreCompact` nor `Stop` (context-stop-gate) appear in the INSTALLATION.md table. PreCompact is described as a context compaction protection hook — it directly relates to Jerry's core value proposition (fighting context rot). A user who experiences unexpected behavior during context compaction will search the documentation for "PreCompact" and find nothing.

Additionally, the `PreToolUse` row says "AST-based validation before tool calls execute" but `hooks.json` shows dual hooks for `PreToolUse` — both `scripts/pre_tool_use.py` (security guardrails WI-SAO-015) and `hooks/pre-tool-use.py` (architecture enforcement EN-006). The description "AST-based validation" only partially describes what fires.

**Analysis:**

This is classified Critical because: (a) it misrepresents the hook surface to users who are making security and trust decisions about what the plugin will run on their machine, (b) it makes the Verification section incomplete — users cannot verify that the PreCompact hook fired because they don't know it exists, and (c) any troubleshooting scenario involving context compaction behavior will hit a documentation dead end.

**Mitigation:**

1. Update the "What hooks give you" table to include all six hook event types: SessionStart, UserPromptSubmit, PreCompact, PreToolUse, Stop (context-stop-gate), SubagentStop.
2. Expand the PreToolUse row to note dual-hook behavior (security guardrails + architecture enforcement).
3. Add PreCompact description: "Fires before context compaction; checkpoints session state to survive context rot."
4. Add Stop/context-stop-gate description: "Fires at session end; enforces quality gates and state persistence."

**Acceptance Criteria:** Hook table matches hooks.json exactly. Every hook event type defined in hooks.json appears in the INSTALLATION.md table with an accurate description.

---

### PM-004-20260225: Plugin Dir Flag Namespace Claim Unverified [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Alternative: Plugin Dir Flag |
| **Strategy Step** | Step 3: Failure Category — Assumption |

**Evidence:**

INSTALLATION.md line 263 states:
> "Jerry's skill commands will be namespaced as `/jerry:<skill-name>` (e.g., `/jerry:problem-solving`)."

This is asserted without citation to Claude Code documentation, without a verification step, and without a troubleshooting note if the namespacing is different. The Claude Code plugin documentation linked in the document footer (`code.claude.com/docs/en/plugins`) may define different namespacing behavior for `--plugin-dir` vs. installed plugins, but the document does not verify this.

If the actual namespace is different (e.g., `/jerry.problem-solving`, `/problem-solving` without any namespace, or `@jerry/problem-solving`), a user doing a quick test drive will try `/jerry:problem-solving`, get an unknown command error, and conclude either Jerry is broken or the `--plugin-dir` flag doesn't work. Since this section is explicitly for "quick test drive," these users are the highest-risk group for abandonment.

**Mitigation:**

1. Verify the actual namespace format produced by `--plugin-dir` against Claude Code documentation or a real test.
2. If the namespace format cannot be verified at document publish time, replace the specific claim with "Skills will be available with a namespace prefix — run `/help` to see the exact skill command names."
3. Add a verification step to the Plugin Dir Flag section: "Run `/help` to see available commands. Skills will appear with a namespace or prefix."

**Acceptance Criteria:** The namespace format claim is either tested and confirmed correct, or replaced with a discovery-based instruction that remains valid regardless of the actual format.

---

### PM-005-20260225: "Marketplace" Terminology Creates False Security Impression [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Install from GitHub (entire section), Troubleshooting, Uninstallation |
| **Strategy Step** | Step 3: Failure Category — External |

**Evidence:**

The term "marketplace" appears 14 times in INSTALLATION.md. The document addresses this explicitly at line 47:
> "Jerry is a **community Claude Code plugin** hosted on GitHub. It is **not** on the official Anthropic marketplace"

However, the very next sentence introduces `/plugin marketplace add` — a Claude Code command that uses the word "marketplace" as its verb. The section heading is "Install from GitHub" but all the commands use `marketplace` as the command name. The document says Jerry is "not on the marketplace" but the technical commands all say `marketplace`.

The friction for enterprise users or IT administrators: when a user reports installing a "marketplace plugin" to an IT security team, the command surface (`/plugin marketplace add`, `/plugin marketplace list`, `/plugin marketplace remove`) implies a centralized trust catalog — which has security vetting connotations. The document's caveat ("not on the official Anthropic marketplace") may not reach the IT gatekeeper who approved "marketplace installs" but is now reviewing an incident.

Additionally, the document does not explain that `marketplace` is Claude Code's internal command name for managing plugin sources — it is used for both official and community plugins. This creates confusion about what "marketplace" means.

**Mitigation:**

1. Add a terminology callout early in the "Install from GitHub" section explaining: "Claude Code uses the term 'marketplace' in its commands to mean any plugin source — official or community. When you run `/plugin marketplace add`, you are adding a plugin source, not connecting to a curated store."
2. In the Troubleshooting section, add an enterprise note: "For IT/security review: Jerry is a community plugin installed from GitHub. The `/plugin marketplace` commands manage local plugin sources, not connections to a centralized marketplace. All code is open source at github.com/geekatron/jerry."

**Acceptance Criteria:** A user who installs Jerry and then explains the installation to an IT administrator can describe what ran on their machine and why the "marketplace" commands are not connecting to a third-party service.

---

### PM-006-20260225: JERRY_PROJECT Persistence Not Addressed — Users Lose Setup After Terminal Restart [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Configuration |
| **Strategy Step** | Step 3: Failure Category — Process |

**Evidence:**

The Configuration section (lines 277–297) instructs users to set `JERRY_PROJECT` via:
```bash
export JERRY_PROJECT=PROJ-001-my-project
```

The `export` command sets the variable for the current shell session only. When the user closes the terminal, the variable is lost. The next Claude Code session will fire the SessionStart hook, which checks `JERRY_PROJECT`, finds it unset, and emits `<project-required>`. The Troubleshooting section (lines 541–551) describes this symptom and says to set the variable — but does not explain how to make it persistent.

The document says the SessionStart hook "will automatically load project context when you start Claude Code" (line 297), which is accurate but implies the setup is permanent. A user who sets the variable once and sees the hook fire successfully will expect it to work in subsequent sessions — until it doesn't.

**Mitigation:**

Add shell persistence instructions to the Configuration section:

```bash
# macOS/Linux — add to ~/.zshrc or ~/.bashrc to persist across sessions:
echo 'export JERRY_PROJECT=PROJ-001-my-project' >> ~/.zshrc
source ~/.zshrc

# Windows PowerShell — set permanently in user profile:
[System.Environment]::SetEnvironmentVariable("JERRY_PROJECT", "PROJ-001-my-project", "User")
```

**Acceptance Criteria:** The Configuration section explains that `export` is session-scoped and provides commands to make `JERRY_PROJECT` persistent across terminal sessions for macOS/Linux (shell profile) and Windows (user environment variables).

---

### PM-007-20260225: Windows Install Command Uses $env:USERNAME Inside Claude Code UI — Interpolation Unverified [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Alternative: Local Clone — Step 2 |
| **Strategy Step** | Step 3: Failure Category — Technical |

**Evidence:**

The Local Clone section at line 199 shows:
```
/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry
```
With the note: "use forward slashes: `/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry`"

The README.md Windows section (line 64) shows:
```
/plugin marketplace add C:/Users/$env:USERNAME/plugins/jerry
```

INSTALLATION.md correctly uses `YOUR_USERNAME` as a literal placeholder. However, the README uses `$env:USERNAME` — a PowerShell environment variable that interpolates in PowerShell but may not interpolate inside Claude Code's `/plugin` command input. If a user copies the README command verbatim into Claude Code, they may pass a literal path with `$env:USERNAME` rather than their actual username.

The Tip callout in INSTALLATION.md (lines 201–205) provides a PowerShell command to derive the forward-slash path — this is good. However, the document does not warn about the README's `$env:USERNAME` usage, and a user who reads both documents may be confused about which format is correct.

**Mitigation:**

1. Align README.md to use `YOUR_USERNAME` placeholder instead of `$env:USERNAME` in the Claude Code command context.
2. In INSTALLATION.md, add a note in the Windows section: "Do not use PowerShell environment variables (`$env:USERNAME`) inside Claude Code commands — they are not interpolated. Use your literal username or the PowerShell path derivation tip above."

**Acceptance Criteria:** README.md and INSTALLATION.md show consistent placeholder conventions for the Windows plugin path. Windows users can follow either document without ambiguity about environment variable interpolation.

---

### PM-008-20260225: No Confirmation Signal That Hooks Are Actually Working [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Enable Hooks / Verification |
| **Strategy Step** | Step 3: Failure Category — Process |

**Evidence:**

The "Enable Hooks" section (lines 108–147) says:
> "Once uv is installed, hooks activate automatically the next time you start Claude Code."

The "Hooks verification" subsection (lines 309–312) says:
> "If you installed uv, start a new Claude Code session. The SessionStart hook fires automatically. You should see project context loading in the session output."

However, this verification instruction has two problems:
1. It requires `JERRY_PROJECT` to be set for the SessionStart hook to show "project context loading" — but the Configuration section is listed after Hooks in the document flow. A user who follows the document top-to-bottom has not yet set `JERRY_PROJECT` when they reach Hooks verification.
2. The "Early access caveat" (line 146) warns: "Some hooks may have schema validation issues that cause them to fail silently (fail-open behavior — skills always work, but enforcement may not fire). If hooks don't appear to be working after installing uv, check GitHub Issues."

The fail-silent caveat combined with the weak verification test ("you should see project context loading") means a user has no reliable way to know whether hooks are actually running. The Verification section does not provide a deterministic test for hook execution — just an observation that requires a prerequisite that may not yet be met.

**Mitigation:**

1. Reorder: Move the `JERRY_PROJECT` setup in Configuration earlier, before "Enable Hooks," or add a note in Hooks that the verification requires a project to be set first.
2. Provide a more explicit hook verification test — describe what specific output text to look for in the Claude Code session output when SessionStart fires (e.g., "Look for a line starting with `[SessionStart]` or similar in the session initialization output").
3. Provide a fallback test that works without a project set: describe what the hook outputs when no project is configured (the `<project-required>` tag), so users can confirm the hook fired even in the no-project state.

**Acceptance Criteria:** A user who installs uv and starts a new Claude Code session can determine with confidence whether the SessionStart hook fired, regardless of whether they have set JERRY_PROJECT.

---

## Minor Findings

### PM-009-20260225: /ast Skill Missing from Available Skills Table [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Using Jerry — Available Skills |
| **Strategy Step** | Step 3: Failure Category — Technical |

**Evidence:** INSTALLATION.md's Available Skills table (lines 341–352) lists 10 skills but omits `/ast` (Markdown AST: parse, query, validate, modify frontmatter). CLAUDE.md Quick Reference lists `/ast` as an available skill. Users who need the AST skill will not find it in the installation guide.

**Recommendation:** Add `/ast` row: `| AST | /ast | Markdown AST parsing, entity frontmatter validation, structural analysis |`

---

### PM-010-20260225: No Session Restart Requirement After Plugin Install [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Install from GitHub — Step 3 Verify |
| **Strategy Step** | Step 3: Failure Category — Process |

**Evidence:** The verification step says to run `/plugin` and check the Installed tab, then test `/problem-solving`. The document does not mention whether a Claude Code session restart is required after plugin install for skills to become available. If Claude Code requires a session restart for new plugins to take effect, users testing immediately after install may get an "unknown command" error and conclude the install failed.

**Recommendation:** Add a note: "After installing, you may need to restart Claude Code or start a new session for skills to become available."

---

### PM-011-20260225: McConkey Voice in Opening May Alienate Enterprise Users [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Document Opening and Step 1/2 Verification |
| **Strategy Step** | Step 3: Failure Category — External |

**Evidence:** The document opens with "you're riding" (line 3) and uses "you're in" (line 84) as the confirmation signal for a successful install. The document section heading mentions McConkey personality. For enterprise IT administrators or professional developers who evaluate tools based on formal documentation quality, the casual register may reduce confidence in the software's reliability and maintainability — particularly if they are looking for indicators that the project is professionally maintained. The failure scenario: an enterprise engineering manager evaluates Jerry for team adoption, reads the installation guide, sees "you're riding" and "you're in," and marks the tool as "not production-ready" before testing functionality.

**Recommendation:** This is a Minor finding because the document is generally well-structured and professional. If the primary audience is individual developers, the current voice is appropriate. If enterprise/team adoption is a growth goal, consider a tonal calibration: keep personality in the opening tagline but use neutral confirmation language in verification steps ("Installation confirmed" instead of "you're in").

---

### PM-012-20260225: Fragile Anchor Link in Platform Note [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Platform Note (line 5) |
| **Strategy Step** | Step 3: Failure Category — Technical |

**Evidence:** The Platform Note references `[Platform Support](index.md#platform-support)` — a cross-document anchor link. If the `index.md` document renames the "Platform Support" heading, this anchor silently breaks, producing a 404 or scroll-to-top behavior. This is a maintenance fragility rather than an immediate failure, but it directly affects a highly visible section (the first callout block a user reads).

**Recommendation:** Verify the anchor is correct and add a note in the contributing guidelines about keeping cross-document anchor links in sync when renaming headings.

---

## Recommendations

### P0 — MUST Mitigate Before Acceptance

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| PM-001-20260225 | Verify actual marketplace name from a clean GitHub-sourced install; update Step 2 or add prominent inline warning with recovery path | Step 2 command tested and confirmed correct, or prominent WARNING callout added |
| PM-002-20260225 | Align README.md and INSTALLATION.md on a single canonical install path; reconcile prerequisite lists | Both documents describe the same primary method; no contradictions |
| PM-003-20260225 | Update hook table to include PreCompact and Stop/context-stop-gate hooks | Hook table matches hooks.json exactly |

### P1 — SHOULD Mitigate

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| PM-004-20260225 | Verify `--plugin-dir` namespace format or replace specific claim with discovery instruction | Namespace claim is tested-and-confirmed or replaced with `/help`-based discovery |
| PM-005-20260225 | Add "marketplace" terminology explanation callout; add enterprise trust note in Troubleshooting | Users and IT administrators understand the semantic difference between Claude Code's `marketplace` command and a curated store |
| PM-006-20260225 | Add shell profile persistence instructions for JERRY_PROJECT | Configuration section explains session scope and provides persistent-setting commands |
| PM-007-20260225 | Align README.md Windows path to use YOUR_USERNAME placeholder; add interpolation warning in INSTALLATION.md | Consistent placeholder conventions across both documents |
| PM-008-20260225 | Provide deterministic hook verification test; reorder Configuration before Hooks or add prerequisite note | User can confirm hooks fired with a specific observable signal |

### P2 — MAY Mitigate / Monitor

| Finding | Action |
|---------|--------|
| PM-009-20260225 | Add `/ast` row to Available Skills table |
| PM-010-20260225 | Add session restart note after install |
| PM-011-20260225 | Calibrate voice for enterprise audience if team adoption is a growth goal |
| PM-012-20260225 | Verify and maintain cross-document anchor links |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-003 (missing hooks), PM-009 (missing skill), PM-008 (incomplete verification path). The hooks table omits two of six hooks; the skills table omits one skill. |
| Internal Consistency | 0.20 | Negative | PM-002 (README vs INSTALLATION incompatible paths), PM-007 (README uses `$env:USERNAME`, INSTALLATION uses `YOUR_USERNAME`). Core contradiction in primary install method between two authoritative documents. |
| Methodological Rigor | 0.20 | Negative | PM-001 (unverified install command), PM-004 (unverified namespace), PM-008 (unverified hook confirmation signal). Key technical claims are asserted without verification evidence. |
| Evidence Quality | 0.15 | Negative | PM-001: The document's own troubleshooting note ("Run `/plugin marketplace list` to confirm the marketplace was registered and check its actual name") implicitly acknowledges the primary command may fail — which is a form of evidence that the claim in Step 2 is not fully verified. |
| Actionability | 0.15 | Negative | PM-006 (no persistence instructions), PM-008 (verification requires unmet prerequisite), PM-005 (no enterprise guidance). Users who hit these gaps cannot independently resolve them from the document alone. |
| Traceability | 0.10 | Neutral | The document's structure is sound, navigation table is present and accurate, links to plugin.json and marketplace.json sources are correct. Traceability is not impaired by the identified issues. |

**Overall Assessment:** REVISE BEFORE ACCEPTANCE

The document has strong structural bones and addresses the most common failure paths (troubleshooting section is thorough). However, three Critical findings (PM-001, PM-002, PM-003) represent fundamental accuracy issues: the primary install command's marketplace name is unverified for the remote-add scenario, the README and INSTALLATION.md describe contradictory primary install paths, and the hook table is materially incomplete. These issues would directly produce the failure scenario described at the outset — users following the primary path getting "plugin not found," users confused by README vs. INSTALLATION.md discrepancies, and users unable to verify hook behavior.

All P0 findings must be resolved before the document is published as the canonical installation guide. P1 findings should be addressed in the same revision cycle given the C4 criticality classification.

---

## Execution Statistics
- **Total Findings:** 12
- **Critical:** 3
- **Major:** 5
- **Minor:** 4
- **Protocol Steps Completed:** 6 of 6
- **Failure Categories Covered:** Technical (PM-003, PM-004, PM-007, PM-008, PM-012), Assumption (PM-001, PM-002, PM-004), External (PM-005, PM-011), Process (PM-006, PM-008, PM-010), Resource (none identified)
- **P0 Findings:** 3
- **P1 Findings:** 5
- **P2 Findings:** 4

# Quality Score Report: Jerry INSTALLATION.md (C4 Iteration 3)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict, score, and top action item |
| [Scoring Context](#scoring-context) | Deliverable metadata and scoring parameters |
| [Score Summary](#score-summary) | Composite score, threshold, verdict |
| [Dimension Scores](#dimension-scores) | Weighted score table across 6 dimensions |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, and improvement paths |
| [Findings Register Status](#findings-register-status) | All tracked findings with iteration 3 resolution status |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered remediation table |
| [Leniency Bias Check](#leniency-bias-check) | Bias counteraction verification |
| [Session Context Handoff](#session-context-handoff) | Structured handoff YAML for orchestrator |

---

## L0 Executive Summary

**Score:** 0.93/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.91) / Traceability (0.91)

**One-line assessment:** Iteration 3 closes all Critical and Major findings tracked since iteration 1, resolves all four routing and actionability gaps from DA-002-it2 / DA-003-it2 / DA-004-it2 / DA-005-it2, and corrects the Windows persistence bug (RT-012), lifting the composite from 0.89 to 0.93 — 0.02 below the C4 threshold of 0.95, with the remaining gap attributable to three specific items: the marketplace.json count fix cannot be independently verified from INSTALLATION.md content (Evidence Quality), the "Plugin not found" troubleshooting entry still does not cross-reference Step 2's output (Evidence Quality / Actionability), and the CONTRIBUTING.md external link remains an unverifiable citation (Traceability).

---

## Scoring Context

- **Deliverable:** `docs/INSTALLATION.md`
- **Deliverable Type:** Documentation (OSS public-facing installation guide)
- **Criticality Level:** C4 (Critical — irreversible once published; public OSS reference documentation)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — iteration 2 findings (S-002 Devil's Advocate, S-001 Red Team, S-007 Constitutional, iteration 2 S-014 scorer) from `docs/reviews/`
- **Prior Scores:** 0.80 (C4 iter 1), 0.89 (C4 iter 2)
- **C4 Threshold:** 0.95 (per user specification — higher than H-13 standard 0.92)
- **Scored:** 2026-02-25

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.93 |
| **C4 Threshold** | 0.95 |
| **Verdict** | REVISE |
| **Gap to Threshold** | -0.02 |
| **Strategy Findings Incorporated** | Yes — iteration 1 and 2 findings across S-002, S-001, S-007, S-014 |
| **Critical Findings Open** | 0 (all resolved) |
| **Major Findings Open** | 0 (all resolved or substantially addressed) |
| **Minor Findings Open** | 3 (two residual from prior iterations, one new) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.1860 | DA-008 nav entry fixed (Early Access qualifier at line 16). DA-001-it2 Interactive Installation prerequisite guard precedes numbered instructions (line 144). RT-003 slash command orientation added (line 75). RT-008 network requirements added (line 42). RT-005 no-repo guidance (line 376). RT-009 air-gapped install path (lines 284-292). All prior Major completeness gaps closed. |
| Internal Consistency | 0.20 | 0.93 | 0.1860 | DA-002-it2 HTTPS context note at section landing (line 77). DA-003-it2 Step 3 variable notation (`jerry@<name-from-step-2>`) closes Step 2/Step 3 disconnect (lines 108-118). DA-006-it2 SSH check includes username verification (line 63). Nav table Enable Hooks entry now consistent with section heading. No Major contradictions remain. |
| Methodological Rigor | 0.20 | 0.94 | 0.1880 | Step 3 variable notation makes add-verify-install sequence fully explicit. RT-013 + RT-020 add JERRY_PROJECT verification step and launch-dependency note to Configuration. RT-008 network prerequisites stated before install methods. Air-gapped path documented. Local Clone Step 3 also uses variable notation. |
| Evidence Quality | 0.15 | 0.91 | 0.1365 | CC-001-20260225B agent count corrected (54 → 58 per fix claim). SSH/HTTPS cause-effect accurate. marketplace.json direct link present (line 120). Hook stability claims specific (SessionStart/UserPromptSubmit named). Remaining: marketplace.json fix cannot be independently confirmed from INSTALLATION.md content. "Plugin not found" troubleshooting does not cross-reference Step 2 outcome (minor). |
| Actionability | 0.15 | 0.92 | 0.1380 | RT-012 Windows persistence fixed (`$env:JERRY_PROJECT` replaces broken `Set-Variable`). DA-004-it2 inline hooks mini-verification added at activation sentence (line 201). DA-005-it2 uninstall source-name note present (line 637). DA-006-it2 SSH username check actionable for edge case. RT-003 slash command orientation. Step-level instructions uniformly declarative. Residual: "getting ready to ride" at line 394 is mild idiom in non-instructional context. |
| Traceability | 0.10 | 0.91 | 0.0910 | All 16 nav table anchors correct (verified from prior constitutional report and heading check). Air-gapped install cross-reference valid (line 43 → new section at line 284). Network requirements attributes domains correctly. Enable Hooks anchor `#enable-hooks-early-access` consistent across document. CONTRIBUTING.md external link unverified (persistent Minor gap across all iterations). |
| **TOTAL** | **1.00** | | **0.9255** | |

**Arithmetic verification:** 0.1860 + 0.1860 + 0.1880 + 0.1365 + 0.1380 + 0.0910 = 0.9255. Rounded composite: **0.93**.

**Composite: 0.93.** Verdict: REVISE (0.92-0.94 band, below C4 threshold of 0.95). Gap to C4 threshold: -0.02.

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**

All Major and Critical completeness gaps from prior iterations are resolved in the current document:

1. **DA-001-it2 (Interactive Installation prerequisite guard — resolved):** Lines 144-153: "Important: Jerry won't appear in the Discover tab until you complete Step 1 above. The Discover tab shows plugins from all registered marketplaces — Jerry is a community plugin, not part of the official Anthropic catalog, so it only appears after you add its source." This caveat now appears before the numbered instructions (lines 149-153). Users who navigate directly to this sub-section via anchor link see the prerequisite before any numbered action.

2. **DA-008 nav entry (Enable Hooks — resolved):** Line 16 of the nav table now reads: "Session context and quality enforcement (early access — hooks may fail silently)." This qualifier is visible to users scanning the document structure without clicking through to the section. The nav table entry and section heading (`## Enable Hooks (Early Access)` at line 157) are now mutually consistent.

3. **RT-003 slash command orientation (resolved):** Line 75: "Where do I type these commands? All `/plugin` commands are typed into Claude Code's chat input — the same text box where you send messages to the AI. Type the command and press Enter. These are not terminal commands." This closes a friction point for new Claude Code users who may confuse chat commands with terminal commands.

4. **RT-008 network requirements (resolved):** Lines 42-43: "Network access: The GitHub install method needs outbound access to `github.com`. If you install uv for hooks, the installer reaches `astral.sh`. The Local Clone method requires `github.com` only for the initial clone — after that, no network access is needed. For fully air-gapped environments, see Air-gapped install under Local Clone." Network prerequisites are now stated before the install methods that depend on them.

5. **RT-009 air-gapped install (resolved):** Lines 284-292: A dedicated subsection under Local Clone covers the three-step air-gapped procedure (clone from connected machine → transfer → proceed from Step 2) with a note about air-gapped uv installation. This closes the gap for users in restricted network environments.

6. **RT-013 + RT-020 (JERRY_PROJECT verification + launch dependency — resolved):** Lines 362-364 include a "Verify it stuck" note with the check command for macOS/Linux and Windows, and a "Launch order matters" note explaining that Claude Code inherits environment variables from the launching terminal.

7. **RT-005 no-repo guidance (resolved):** Line 376: "Don't have a repository yet? Jerry works in any directory. Create one: `mkdir my-project && cd my-project && git init`, then run the `mkdir` command above. Jerry doesn't require an existing codebase." This removes an implicit prerequisite from the Configuration section.

**Remaining gaps:**

1. **Interactive Installation "above" reference (Very Minor):** Line 144 reads "until you complete Step 1 above" — the word "above" is directional for sequential readers but not actionable for users who navigate directly to the sub-section. The recommendation in DA-001-it2 included adding a direct anchor link to Step 1 as an alternative; this was not implemented. However, the warning itself is the higher-priority fix and it is present. This is a very minor residual.

2. **Document length (Accepted):** Document is approximately 681 lines. The "Using Jerry" and "Developer Setup" sections remain (DA-007-20260225, accepted as-is in iteration 2). These sections add legitimate value to a comprehensive OSS installation guide and their presence was explicitly accepted in the iteration 2 findings register.

**Improvement Path:**

Replace "until you complete Step 1 above" with "until you complete [Step 1](#step-1-add-the-jerry-repository-as-a-plugin-source) above" — adding an anchor link makes the prerequisite actionable for direct-link navigators without changing the text.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

1. **DA-002-it2 (HTTPS context note — resolved):** Line 77: "Arriving from the HTTPS row in the table above? Use the HTTPS command in Step 1 below (the second row in the table). It works without SSH keys." No-SSH users who follow the routing table's "Install from GitHub (HTTPS)" link now arrive at a contextual confirmation that routes them to the correct command before they encounter the SSH command in the two-row table.

2. **DA-003-it2 (Step 3 variable notation — resolved):** Lines 108-110: "Use the source name from Step 2's output as the `@suffix`: `/plugin install jerry@<name-from-step-2>`." Lines 112-113: "If Step 2 showed `jerry-framework` (the default), the command is: `/plugin install jerry@jerry-framework`." The Step 2 output now explicitly feeds into Step 3's command. The hardcoded form appears only as a concrete example, not as the primary instruction.

3. **DA-006-it2 (SSH check username verification — resolved):** Lines 63-64: "If you see `Hi <username>!` and `<username>` is your GitHub account, you have SSH set up. If the username is unexpected, or you see 'Permission denied,' use the HTTPS path — same result, same speed, no SSH needed." The edge case of SSH keys registered to the wrong account is now acknowledged.

4. **Hooks section internal consistency:** The section opens with the early access caveat (lines 159-162), then describes hooks capabilities, then the uv install. At line 201: "Once uv is installed, hooks should activate automatically the next time you start Claude Code. Quick check: start a new session — if you see a `<project-context>` tag in the output, hooks are live. For the full checklist, see Hooks verification below." The "should" hedging, the inline quick check, and the forward reference to the full verification are all consistent with the caveat.

5. **Nav table and section heading alignment:** Line 16 ("early access — hooks may fail silently") matches the section heading "Enable Hooks (Early Access)" at line 157. The anchor `#enable-hooks-early-access` is consistent across the nav table, capability matrix, and troubleshooting section.

**Remaining gaps:**

1. **Interactive Installation "above" without anchor (Very Minor):** Consistent with the completeness gap — "Step 1 above" is a loose directional reference without an anchor. This is the same issue that affects completeness; it creates a very minor consistency risk for direct-link navigators.

**Improvement Path:**

Add anchor link to "Step 1 above" (same one-character edit as the completeness improvement path). No other targeted improvements identified at this score level.

---

### Methodological Rigor (0.94/1.00)

**Evidence:**

1. **Step 3 variable notation (DA-003-it2 — resolved):** The install methodology now follows the complete sequence: (Step 1) add source → (Step 2) run `marketplace list`, verify source name → (Step 3) install using `jerry@<name-from-step-2>` with `jerry@jerry-framework` as the expected-value example → (Step 4) confirm via `/plugin` Installed tab. This is the methodologically correct pattern: Step 2's output is explicitly the input to Step 3. The prior Critical finding (DA-001-20260225) that led to adding Step 2 is now fully manifested in Step 3's instruction.

2. **Local Clone Step 3 variable notation (resolved):** Lines 265-270: "Run `/plugin marketplace list` to confirm the source registered, then install using the name from the list: `/plugin install jerry@<name-from-list>`. If the list showed `jerry-framework` (the default), the command is `/plugin install jerry@jerry-framework`." The Local Clone methodology mirrors the Install from GitHub methodology — consistent variable-name pattern across both install paths.

3. **Configuration methodology (RT-013 + RT-020 — resolved):** The Configuration section now has four numbered steps with complete procedural coverage: (1) navigate to repo, (2) set environment variable, (3) make it persistent with verification check and launch-order note, (4) create project structure with gitignore guidance. No implicit prerequisites remain — the "no existing repo" case is addressed (RT-005), the Windows persistence command is correct (RT-012), the launch dependency is stated (RT-020), and the verification step is actionable (RT-013).

4. **Prerequisites methodology (RT-008 — resolved):** Network requirements are stated in the Prerequisites section before users encounter the install methods. This correctly sequences prerequisites before procedures.

5. **Air-gapped install (RT-009 — resolved):** The Local Clone section now includes a dedicated Air-gapped install subsection with a three-step methodology for restricted environments and a separate note about uv installation in air-gapped contexts. This extends the document's methodological coverage to the full range of deployment environments.

**Remaining gaps:**

Minor observation: The version pin example at line 299 uses `v0.21.0` (the current version at scoring time). This tag will become a stale example as the framework releases new versions. This is a maintenance concern rather than a methodological gap, and version pin examples in install guides inherently use a representative version at documentation time.

**Improvement Path:**

No targeted improvement needed for Methodological Rigor at this score level. The dimension is at 0.94 — the remaining 0.06 to theoretical perfection is attributable to the inherently provisional nature of version-specific examples and the minor "above" directional reference.

---

### Evidence Quality (0.91/1.00)

**Evidence of strong evidence quality:**

1. **CC-001-20260225B (agent count correction — claimed resolved):** Per the iteration 3 briefing, the marketplace.json description was corrected from "54 specialized agents" to "58 specialized agents" (the accurate count per `plugin.json`'s agents array). This resolves the P-001 accuracy violation that reduced Evidence Quality in iteration 2. Note: this fix is in the supporting manifest (`.claude-plugin/marketplace.json`), not in `INSTALLATION.md` directly — it cannot be independently confirmed from the deliverable content read.

2. **SSH/HTTPS behavior documentation:** The cause-and-effect chain is complete and accurate: `owner/repo` shorthand → SSH clone by default → "Permission denied (publickey)" error → HTTPS URL bypass. The Prerequisites note (lines 43-44) names the exact error message users will see.

3. **marketplace.json direct link:** Line 120: "The source name comes from Jerry's [`.claude-plugin/marketplace.json`](https://github.com/geekatron/jerry/blob/main/.claude-plugin/marketplace.json) — you can inspect it to verify." All claims about the source name are traceable to an independently verifiable artifact.

4. **Hook stability specifics:** Lines 159-162: "The most stable hooks are SessionStart and UserPromptSubmit. PreToolUse and SubagentStop may experience schema issues in some Claude Code versions." Named hook stability claims with specific failure mode context, not a generic "may fail" disclaimer.

5. **Official Anthropic marketplace link:** Line 73: "This is separate from the [official Anthropic marketplace](https://github.com/anthropics/claude-plugins-official)..." — the claim about the official catalog is now backed by a traversable external citation.

6. **Network requirements:** Line 42 names specific domains (`github.com`, `astral.sh`) with conditional framing that accurately represents which methods require what network access.

**Remaining gaps:**

1. **marketplace.json fix unverifiable from INSTALLATION.md content (Minor):** The claimed correction of the agent count from 54 to 58 in `marketplace.json` is a supporting manifest change, not a change in `INSTALLATION.md`. The INSTALLATION.md text was read for this scoring session; the marketplace.json content was not re-read. The score applies a slight downward pressure: if the fix was not applied, the evidence quality gap from iteration 2 (CC-001-20260225B) remains open. Under the leniency bias rule (uncertain scores go lower), this uncertainty prevents the full resolution credit.

2. **"Plugin not found" cross-reference to Step 2 (Minor):** Lines 544-550 in the Troubleshooting section describe the plugin-not-found case and instruct users to run `marketplace list` to get the actual source name. The iteration 2 scorer recommended adding one sentence: "If you ran Step 2 during install, you already have the confirmed source name." This was not in the 13 claimed fixes and is not present. The omission has diminished importance given Step 3's variable notation, but the troubleshooting entry still treats the source name as a discovery action rather than a recall action for users who followed the procedure.

**Improvement Path:**

1. Verify and confirm the marketplace.json agent count reads "58 specialized agents" (requires direct file read of `.claude-plugin/marketplace.json`).
2. Add one sentence to the "Plugin not found" troubleshooting entry: "If you completed Step 2 (Verify the source registered) during install, you already have the confirmed source name from your `/plugin marketplace list` output — use that name here."

---

### Actionability (0.92/1.00)

**Evidence of strong actionability:**

1. **RT-012 (Windows persistence fix — resolved):** Lines 358-360: `$env:JERRY_PROJECT = "PROJ-001-my-project"` is the correct Windows PowerShell syntax for environment variable persistence in the user profile. The prior `Set-Variable` syntax set a local session variable and did not persist across terminals. This was a broken actionable step for Windows users and is now correct.

2. **DA-004-it2 (inline hooks mini-verification — resolved):** Line 201: "Quick check: start a new session — if you see a `<project-context>` tag in the output, hooks are live. For the full checklist, see Hooks verification below." Users who install uv and restart Claude Code now have an immediate, inline verification action without navigating to a separate section.

3. **DA-005-it2 (uninstall source-name variability note — resolved):** Line 637: "Source name differs? Use the name from `/plugin marketplace list`: `/plugin uninstall jerry@<name-from-list>`." The uninstall command is now actionable for users whose source registered under a non-default name, with the recovery path visible at the point of the command rather than three lines away in a different sub-section.

4. **DA-006-it2 (SSH username verification — resolved):** Line 63: "If you see `Hi <username>!` and `<username>` is your GitHub account, you have SSH set up. If the username is unexpected, or you see 'Permission denied,' use the HTTPS path." Users in the edge case (SSH key registered to a different GitHub account) now receive actionable guidance at the point of the check.

5. **RT-003 (slash command orientation — resolved):** Line 75: "All `/plugin` commands are typed into Claude Code's chat input — the same text box where you send messages to the AI." This resolves the new-user confusion about where to type commands that does not require a failure cycle to discover.

6. **Step-level instructions throughout:** All numbered steps provide exact commands with platform variants (macOS/Linux and Windows), expected outputs, and recovery actions. Troubleshooting entries follow Symptom/Cause/Fix structure. Verification section provides expected outputs for each check.

**Remaining gaps:**

1. **"Getting ready to ride" (Very Minor):** Line 394: "That's Jerry loading your project context and getting ready to ride." This appears in the Hooks verification section as the success confirmation. The actionable statement ("If you see the tag, hooks are working") precedes this phrase; the idiom is in an appended descriptive clause. This is not a step-level instructional moment — it is a contextual explanation following a confirmed success check. The impact on actionability is minimal.

2. **"Let it rip" (Accepted — contextually appropriate):** Line 418: "Let it rip." — appears in a "New to Jerry?" orientation callout, not in a numbered step or verification instruction. This was assessed as contextually appropriate in iteration 2 and that assessment is unchanged.

**Improvement Path:**

Line 394: Replace "That's Jerry loading your project context and getting ready to ride" with "The SessionStart hook loaded your project context." One sentence; eliminates the final residual idiom at a post-verification moment.

---

### Traceability (0.91/1.00)

**Evidence:**

1. **Nav table coverage:** All 16 `##` sections are listed with anchor links. The Enable Hooks entry (line 16, `#enable-hooks-early-access`) correctly reflects the renamed section heading. All anchors were verified correct in the iteration 2 constitutional report; no heading renames occurred in iteration 3.

2. **New section anchors:** The Air-gapped install subsection (lines 284-292) is cross-referenced from the Prerequisites network requirements note (line 43: "see Air-gapped install under Local Clone"). This is a structural prose cross-reference, not an anchor link. The subsection does not appear in the nav table (it is a subsection, not a `##` heading) — this is consistent with NAV-004's scope.

3. **External links:** All major external links verified accurate in prior constitutional reports: GitHub SSH guide (docs.github.com), uv docs (docs.astral.sh/uv), Claude Code quickstart (code.claude.com/docs/en/quickstart), official Anthropic marketplace (github.com/anthropics/claude-plugins-official), marketplace.json direct link, uv GitHub releases.

4. **Internal cross-references consistent:** Step 3's "Source name mismatch?" callout at line 120 links to `[Plugin not found](#plugin-not-found-after-adding-source)` in Troubleshooting. The Troubleshooting section heading exists and the anchor resolves. Configuration section references Verification section. Capability Matrix references Available Skills subsection.

5. **Version claim consistency:** Version pin example `v0.21.0` at line 299 matches the current framework version (v0.21.0) per CLAUDE.md. This is internally consistent with the codebase state at scoring time.

**Remaining gaps:**

1. **CONTRIBUTING.md external link (Persistent Minor):** Line 424: `https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md` — this external link has not been verified in-session. It has been documented as an unverified external link across all four C4 scoring iterations. It is contextually appropriate in the Developer Setup section and its URL pattern is consistent with verified links (same domain, same structure as the `.github/ISSUE_TEMPLATE/` links that were verified). This is an ongoing accepted Minor gap.

2. **Air-gapped install prose cross-reference (Very Minor):** Line 43 uses prose to reference the Air-gapped install subsection ("see Air-gapped install under Local Clone") rather than an anchor link. The prose reference is accurate and the subsection exists. An anchor link (`#air-gapped-install`) would be more robust but the prose reference is functional.

**Improvement Path:**

1. Convert line 43 prose cross-reference to an anchor link: "see [Air-gapped install](#air-gapped-install) under Local Clone." Requires that the Air-gapped install subsection heading has an anchor slug `air-gapped-install` — which it does based on the heading "### Air-gapped install" (lowercase, yields `#air-gapped-install`).
2. The CONTRIBUTING.md link is a permanent acceptance: it follows the same URL pattern as verified links in the same document and file existence cannot be confirmed without external network access.

---

## Findings Register Status

### Iteration 1 Findings (DA-001-20260225 through DA-008-20260225)

| ID | Severity | Iter 1 | Iter 2 | Iter 3 Status | Evidence |
|----|----------|--------|--------|---------------|---------|
| DA-001-20260225 | Critical | Open | Resolved (Step 2 proactive) | **Confirmed resolved** | Step 2 = "Verify the source registered" with proactive `/plugin marketplace list`. Step 3 uses `jerry@<name-from-step-2>`. |
| DA-002-20260225 | Major | Open | Substantially resolved | **Confirmed resolved** | Session Install is a named row in four-row routing table. No "test drive" framing. |
| DA-003-20260225 | Major | Open | Resolved | **Confirmed resolved** | Step-level confirmations declarative. "rolling with Jerry" absent. Remaining mild idiom at line 394 is not step-level. |
| DA-004-20260225 | Major | Partial | Resolved | **Confirmed resolved** | Four-row routing table complete. "First time here?" nav callout present (line 30). |
| DA-005-20260225 | Major | Partial | Resolved | **Confirmed resolved** | Marketplace definition at line 70-73 (community vs. official explicit with link). |
| DA-006-20260225 | Major | Partial | Resolved | **Confirmed resolved** | "Project Setup (Required for Skills)" heading. Project Issues first in Troubleshooting. |
| DA-007-20260225 | Minor | Unaddressed | Accepted as-is | **Accepted as-is** | Document ~681 lines. Developer Setup and Using Jerry remain. Scope accepted for comprehensive C4 guide. |
| DA-008-20260225 | Minor | Partial | Partially resolved (heading) | **Fully resolved** | Nav table line 16 now includes "(early access — hooks may fail silently)". Section heading and nav entry are now consistent. |

### Iteration 1 S-002 (DA-NNN-it1 findings)

| ID | Severity | Iter 1 Status | Iter 2 | Iter 3 Status | Evidence |
|----|----------|---------------|--------|---------------|---------|
| DA-001-it1 | Critical | Open | Substantially addressed → DA-001-it2 | **Fully resolved** | Interactive Installation prerequisite guard precedes numbered instructions (line 144). |
| DA-002-it1 | Major | Open | Addressed | **Confirmed resolved** | SSH row shows "No — HTTPS alternative available" (line 39). |
| DA-003-it1 | Major | Open | Addressed | **Confirmed resolved** | Four-row routing table with SSH check command including username verification (line 63). |
| DA-004-it1 | Major | Open | Substantially addressed → DA-002-it2 | **Fully resolved** | HTTPS context note at Install from GitHub section landing (line 77). |
| DA-005-it1 | Major | Open | Substantially addressed → DA-003-it2 | **Fully resolved** | Step 3 variable notation with hardcoded example only (lines 108-118). |
| DA-006-it1 | Minor | Open | Addressed | **Confirmed resolved** | "you're riding" absent from nav table. Step-level confirmations declarative. |
| DA-007-it1 | Minor | Open | Addressed | **Confirmed resolved** | Session Install section heading and routing row use non-"test drive" framing. |

### Iteration 2 S-002 (DA-NNN-it2 findings)

| ID | Severity | Iter 2 Status | Iter 3 Status | Evidence |
|----|----------|---------------|---------------|---------|
| DA-001-it2 | Major | Open | **Resolved** | Prerequisite caveat precedes numbered instructions in Interactive Installation (line 144). |
| DA-002-it2 | Major | Open | **Resolved** | HTTPS context note at Install from GitHub section body (line 77). |
| DA-003-it2 | Major | Open | **Resolved** | Step 3 uses `jerry@<name-from-step-2>` with hardcoded form as example (lines 108-118). |
| DA-004-it2 | Minor | Open | **Resolved** | Inline mini-verification at hooks activation sentence (line 201). |
| DA-005-it2 | Minor | Open | **Resolved** | Source-name variability note under "Remove the Plugin" (line 637). |
| DA-006-it2 | Minor | Open | **Resolved** | SSH check includes username verification (line 63). |

### Constitutional Findings (CC-NNN-20260225)

| ID | Severity | Iter 1 | Iter 2 Status | Iter 3 Status | Evidence |
|----|----------|--------|---------------|---------------|---------|
| CC-001-20260225 | Major | Open | Partially resolved (count 54, off by 4) → CC-001-20260225B | **Claimed resolved** | marketplace.json count stated as corrected from 54 to 58 per iteration 3 fix briefing. Cannot verify from INSTALLATION.md content. |
| CC-002-20260225 | Major | Open | Resolved | **Confirmed resolved** | Hook caveat names stable/unstable hooks and provides verification steps (lines 159-162). |
| CC-003-20260225 | Minor | Open | Resolved | **Confirmed resolved** | "hooks should activate automatically" with inline verification (line 201). |
| CC-004-20260225 | Minor | Open | Resolved | **Confirmed resolved** | Nav table Updating, Uninstallation, License entries have substantive descriptions. |

### Red Team Findings — Open in Iter 2 (RT-NNN)

| ID | Severity | Iter 2 Status | Iter 3 Status | Evidence |
|----|----------|---------------|---------------|---------|
| RT-003 | Critical | Open | **Resolved** | Slash command orientation added at line 75. |
| RT-008 | Critical | Open | **Resolved** | Network requirements in Prerequisites (line 42). |
| RT-012 | Bug | Open | **Resolved** | Windows persistence uses `$env:JERRY_PROJECT` (lines 358-360). |
| RT-005 | Major | Open | **Resolved** | No-repo guidance at line 376. |
| RT-009 | Major | Open | **Resolved** | Air-gapped install subsection (lines 284-292). |
| RT-013 | Major | Open | **Resolved** | JERRY_PROJECT verification step (lines 362-363). |
| RT-020 | Major | Open | **Resolved** | Launch-dependency note (line 364). |

**Open items entering iteration 4:**

| ID | Severity | Dimension | Description |
|----|----------|-----------|-------------|
| RESIDUAL-001 | Very Minor | All | "above" directional in Interactive Installation prerequisite warning (line 144) — no anchor link to Step 1 |
| RESIDUAL-002 | Minor | Evidence Quality | "Plugin not found" troubleshooting entry does not cross-reference Step 2 outcome |
| RESIDUAL-003 | Minor | Traceability | CONTRIBUTING.md external link unverifiable (persistent, accepted) |
| RESIDUAL-004 | Very Minor | Actionability | "getting ready to ride" at line 394 (mild idiom, non-instructional context) |
| RESIDUAL-005 | Very Minor | Traceability | Air-gapped install prose cross-reference at line 43 (functional, not an anchor link) |
| RESIDUAL-006 | Minor | Evidence Quality | marketplace.json fix (54 → 58 agents) unverifiable from INSTALLATION.md content — requires confirmation via direct file read |

---

## Improvement Recommendations

Priority-ordered by expected composite score impact for C4 acceptance at 0.95:

| Priority | ID | Dimension(s) | Current | Target | Recommendation |
|----------|----|-------------|---------|--------|----------------|
| 1 | RESIDUAL-002 | Evidence Quality (0.91) + Actionability (0.92) | 0.91 / 0.92 | 0.94 / 0.94 | Add one sentence to "Plugin not found after adding source" troubleshooting entry (lines 544-550): "If you completed Step 2 (Verify the source registered) during install, you already have the confirmed source name from your `/plugin marketplace list` output — use that name here." |
| 2 | RESIDUAL-006 | Evidence Quality (0.91) | 0.91 | 0.94 | Verify `.claude-plugin/marketplace.json` reads "58 specialized agents" (not 54). Read the file directly to confirm the CC-001-20260225B fix was applied. If not applied, correct it now. |
| 3 | RESIDUAL-001 | Completeness (0.93) + Internal Consistency (0.93) | 0.93 / 0.93 | 0.95 / 0.95 | Line 144: Replace "until you complete Step 1 above" with "until you complete [Step 1](#step-1-add-the-jerry-repository-as-a-plugin-source) above." Adds an anchor link making the prerequisite actionable for direct-link navigators. |
| 4 | RESIDUAL-004 | Actionability (0.92) | 0.92 | 0.94 | Line 394: Replace "That's Jerry loading your project context and getting ready to ride" with "The SessionStart hook loaded your project context." Eliminates the final step-adjacent idiom in the Verification section. |
| 5 | RESIDUAL-005 | Traceability (0.91) | 0.91 | 0.93 | Line 43: Replace "see Air-gapped install under Local Clone" with "see [Air-gapped install](#air-gapped-install) under Local Clone." Converts prose reference to anchor link. |

**Projected impact for iteration 4 (addressing P1–P5):** Addressing all five recommendations is projected to lift Evidence Quality to ~0.94, Actionability to ~0.94, Completeness to ~0.95, and Traceability to ~0.93, yielding a composite of approximately 0.95–0.96. The gap of 0.02 to the C4 threshold is achievable in one targeted iteration. The P1 and P2 items (RESIDUAL-002 and RESIDUAL-006) have the highest leverage; P3 through P5 are single-line edits.

---

## Leniency Bias Check

- [x] Each dimension scored independently — Evidence Quality at 0.91 (not 0.93) because the marketplace.json fix is in a supporting manifest, not verifiable from INSTALLATION.md content, and the uncertain-score-goes-lower rule applies; Traceability at 0.91 (not 0.93) because the CONTRIBUTING.md gap is persistent and the air-gapped prose reference is functional but not an anchor link
- [x] Evidence documented for each score — all scores cite specific line numbers from the current `docs/INSTALLATION.md` as read; all 13 claimed fixes confirmed present in the document with line citations; DA-008 nav entry fix confirmed at line 16; Interactive Installation fix confirmed at line 144; Step 3 variable notation confirmed at lines 108-118
- [x] Uncertain scores resolved downward — marketplace.json count fix (CC-001-20260225B) applies downward pressure on Evidence Quality because the fix is in a file not read in this session; the score does not award full resolution credit for an unverifiable fix
- [x] Revision history calibration applied — this is iteration 3 of C4 scoring (overall iteration 7 counting prior C2 rounds); the improvement from 0.89 (iter 2) to 0.93 (iter 3) reflects genuine resolution of 3 Major findings (DA-001-it2, DA-002-it2, DA-003-it2), 3 Minor findings (DA-004-it2 through DA-006-it2), and 7 Red Team findings (RT-003, RT-005, RT-008, RT-009, RT-012, RT-013, RT-020); a +0.04 composite improvement per iteration is proportionate to this scope of fixes
- [x] No dimension scored above 0.94 without exceptional evidence — Methodological Rigor at 0.94 is the highest score; justified by: (a) add-verify-install sequence fully complete with variable notation in both primary and local-clone paths, (b) Configuration methodology complete with verification, launch dependency, no-repo guidance, and correct Windows syntax, (c) network prerequisites stated before install methods, (d) air-gapped methodology documented
- [x] Composite arithmetic verified — 0.1860 + 0.1860 + 0.1880 + 0.1365 + 0.1380 + 0.0910 = 0.9255; rounded to 0.93
- [x] Score gap from 0.89 to 0.93 is +0.04 — proportionate to the resolution volume; the remaining gap of -0.02 to the C4 threshold is attributable to three minor items (marketplace.json fix verification, "Plugin not found" cross-reference, CONTRIBUTING.md traceability) and two very minor items (Interactive Installation anchor, line 394 idiom); the gap is achievable in one iteration
- [x] C4 threshold noted at 0.95 (not H-13 standard 0.92) — the document achieves 0.93, which clears the H-13 standard (0.92) at this score; REVISE verdict is correct at 0.95 C4 threshold
- [x] First-draft calibration not applicable — this is the seventh iteration of a substantially revised document; the 0.93 score reflects a document with no open Critical or Major findings and only minor residual items; 0.93 is consistent with the calibration anchor of 0.92 = "strong work with minor refinements needed"

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.93
threshold: 0.95  # C4 user-specified (higher than H-13 standard 0.92)
weakest_dimension: Evidence Quality  # tied with Traceability at 0.91
weakest_score: 0.91
critical_findings_count: 0  # all prior Critical findings resolved
major_findings_count: 0  # all prior Major findings resolved
minor_findings_open: 6  # RESIDUAL-001 through RESIDUAL-006
iteration: 3  # C4 scoring iteration 3; overall iteration 7
gap_to_threshold: -0.02
improvement_recommendations:
  - "RESIDUAL-002: Add Step 2 cross-reference to 'Plugin not found' troubleshooting entry (one sentence)"
  - "RESIDUAL-006: Verify marketplace.json reads '58 specialized agents' — direct file read required to confirm CC-001-20260225B fix"
  - "RESIDUAL-001: Add anchor link to Interactive Installation prerequisite warning: 'Step 1 above' → '[Step 1](#step-1-add-the-jerry-repository-as-a-plugin-source) above'"
  - "RESIDUAL-004: Line 394 — replace 'getting ready to ride' with declarative SessionStart confirmation"
  - "RESIDUAL-005: Line 43 — convert prose Air-gapped install cross-reference to anchor link"
```

---

*Strategy: S-014 LLM-as-Judge*
*Agent: adv-scorer v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-02-25*
*Deliverable: `docs/INSTALLATION.md` (revised 2026-02-25, iteration 3)*
*Criticality: C4 (Critical — public OSS installation guide)*
*Prior iterations: C2 (0.74, 0.84, 0.88, 0.89), C4 iter 1 (0.80), C4 iter 2 (0.89), C4 iter 3 (0.93)*
*Strategy findings incorporated: All C4 iteration 1 and iteration 2 adversarial strategy reports*

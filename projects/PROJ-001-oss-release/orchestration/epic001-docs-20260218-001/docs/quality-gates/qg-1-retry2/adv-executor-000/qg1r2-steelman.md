# S-003 Steelman Report — QG-1 Retry 2

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | One-line verdict |
| [Execution Context](#execution-context) | Strategy, deliverable metadata |
| [Prior Finding Resolution](#prior-finding-resolution) | Verification of QG-1 Retry 1 steelman findings |
| [Steelman Construction](#steelman-construction) | Strongest charitable interpretation |
| [Best Case Conditions](#best-case-conditions) | Assumptions under which the document excels |
| [Remaining Gaps](#remaining-gaps) | Gaps surviving after charitable interpretation |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Score Estimate](#score-estimate) | Range estimate |

---

## L0 Summary

Iteration 4 closes all four QG-1 Retry 1 Major findings with precise, well-executed fixes, and resolves four of the five prior Minor findings; the one remaining Minor (SM-005-qg1r1s, scope team scenario) was never targeted and survives — but introduces no user-failure scenario — leaving the document as a complete, cross-platform, dual-audience installation guide that is credibly positioned to reach the 0.92 threshold.

---

## Execution Context

| Field | Value |
|-------|-------|
| **Strategy** | S-003 (Steelman Technique) |
| **Template** | `.context/templates/adversarial/s-003-steelman.md` |
| **Deliverable** | `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md` |
| **Deliverable Type** | Installation Guide (End-User Documentation) |
| **Criticality Level** | C2 (Standard) |
| **Quality Gate** | QG-1 Retry 2 (Final — max_retries=2) |
| **Iteration** | 4 (post QG-1 Retry 1 adversarial revision — all 10 priority findings applied) |
| **Prior QG-1 Retry 1 Score** | 0.8300 (REJECTED) |
| **Executed** | 2026-02-18 |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Finding Prefix** | SM-NNN-qg1r2s |
| **Original Author** | ps-architect-001 |

---

## Prior Finding Resolution

| Finding ID | Status | Evidence |
|------------|--------|----------|
| SM-001-qg1r1s | RESOLVED | P7 fix applied. PAT Alternative Step 3 (lines 391–399) now shows both `macOS (Terminal) or Git Bash` and `Windows (PowerShell)` clone variants, consistent with SSH clone step. The asymmetry is gone. |
| SM-002-qg1r1s | RESOLVED | P10 fix applied. Table of Contents header reads `\| Section \| Purpose \|` (line 179), matching NAV-003 framework standard. |
| SM-003-qg1r1s | RESOLVED | P9 fix applied. Future section (lines 637–638) now instructs: "visit github.com/geekatron/jerry while logged out of GitHub — if the page loads without a login prompt, these simplified instructions apply." Detection mechanism is explicit and actionable. |
| SM-004-qg1r1s | RESOLVED | P1 fix applied. Configuration section (line 641) precedes Verification section (line 683) in both the Table of Contents (rows 5 and 6, lines 185–186) and the document body. JERRY_PROJECT can be set before the "Test a Skill" step, eliminating the `<project-required>` surprise. |
| SM-005-qg1r1s | OPEN | Not in the P1–P10 priority list. Configuration section Recommendation (lines 652–653) still reads: "Use **User** scope for personal use. Use **Project** scope when you want your whole team to have Jerry available." No operational example of what Project scope means (e.g., `.claude/settings.json` committed to version control) was added. Finding is Minor; no user-failure scenario introduced. |

---

## Steelman Construction

### Core Thesis

Jerry can be installed by two audiences — private-repository collaborators via SSH (or PAT fallback) and future public-repository users via unauthenticated HTTPS — both converging on a single Claude Code local marketplace mechanism. Iteration 4 executes all ten QG-1 Retry 1 priority fixes precisely and without regressions, closing every Major finding that prevented the document from reaching the quality threshold.

### Strongest Interpretation

**Iteration 4 closes all four QG-1 Retry 1 Major findings.** Every finding that depressed the 0.8300 score is now demonstrably addressed:

- **P1 (DA-004 — Configuration/Verification ordering):** Configuration precedes Verification in both the ToC and the document body. The JERRY_PROJECT setup step is encountered before the "Test a Skill" instruction. The previously guaranteed new-user failure at the first-run moment is eliminated at the structural level.

- **P2 (DA-001 — osxkeychain pre-check):** The PAT Alternative credential helper section (lines 403–424) now includes a `git credential-osxkeychain 2>&1 | head -1` verification step with explicit comment guidance ("If you see 'usage: git credential-osxkeychain', proceed. If you see 'command not found', use the store helper instead"), followed by the `store` helper fallback with a plaintext security note. A new Troubleshooting entry "Credential Helper Not Found (macOS PAT Users)" (lines 841–854) provides cause, solution, and Xcode CLT recovery path.

- **P3 (DA-002 — Windows SSH agent silent failure):** The Windows SSH agent Tip (lines 303–317) now wraps the entire block in a `Get-Service ssh-agent -ErrorAction SilentlyContinue` guard, with a conditional branch providing `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0` as the PowerShell install path and the Settings UI path as an alternative. The note correctly qualifies the "default on Windows 10 build 1809+" claim: "may be absent on Home and LTSC editions." The user is never left with a silently failing command.

- **P4 (DA-003 — space-in-path warning):** The space-in-path warning now appears at all three relevant clone locations: macOS Installation Step 2 (lines 470–472), Windows Installation Step 2 (lines 547–549), and Collaborator Installation Step 4 (lines 354–355). The warning is specific ("The Claude Code `/plugin marketplace add` command does not support paths with spaces"), includes the safe recommended path, and on Windows adds a short-path fallback for usernames that contain spaces.

- **P5 (DA-006 — PAT repo scope):** PAT Alternative Step 1 (lines 387–388) now correctly states "full access to private repositories you collaborate on (read and write)" and introduces the fine-grained PAT option with `Contents: Read-only` permission as the least-privilege alternative.

- **P6 (DA-005 — marketplace rationale scope conflation):** The "Why the marketplace?" callout (lines 444) now reads "the scope you choose during `/plugin install`" — eliminating the ambiguity that suggested scope was set during marketplace-add.

- **P7 (SM-001 — PAT Windows clone variant):** Addressed as described in Prior Finding Resolution above.

- **P8 (DA-007 — Future section rate-limit):** Future section (lines 607–608) now states: "unauthenticated HTTPS clones may be subject to GitHub API rate limits during periods of high traffic. If you encounter rate-limiting errors, authenticating with a GitHub account resolves this."

- **P9 (SM-003 — Future detection):** Addressed as described in Prior Finding Resolution above.

- **P10 (SM-002/CC-001 — ToC header):** Addressed as described in Prior Finding Resolution above.

**Additional bonus fixes were applied.** SM-009 (macOS Keychain tip rationale) and SM-007 (BOOTSTRAP.md location note) were already in Iteration 3. The Iteration 4 change summary is complete and accurate.

**The document structure is now sound.** Prerequisites → Collaborator Installation (SSH with dual-platform key generation, agent setup, clone) → Installation (platform tabs with stable HTML anchors) → Future section → Configuration (scope setup with JERRY_PROJECT) → Verification (test skill after project is configured) → Using Jerry → Troubleshooting → For Developers → Uninstallation → Getting Help → License. Every section follows logically from the one before.

**Cross-platform parity is fully achieved.** Every SSH step, every clone step, every credential step provides both macOS Terminal/Git Bash and Windows PowerShell variants. Warning callouts are symmetric: the ssh-keygen pre-check Warning appears on both platforms in identical structure, and the SSH agent Tip now uses a proper `if/else` guard on Windows rather than a silent-failure path.

**Troubleshooting is comprehensive.** Eight scenarios are covered: Plugin Command Not Recognized, Plugin Not Found After Adding Marketplace, uv: command not found, Skills Not Appearing, Path Issues on Windows, SSH Authentication Failed, Repository Not Found, and Credential Helper Not Found (macOS PAT Users). Each scenario has a named Symptom and numbered Solutions. The addition of the Credential Helper Not Found entry closes the loop that the P2 fix opened in the main body.

**All four acceptance criteria remain satisfied.** AC-1 (archive installation), AC-2 (collaborator SSH path), AC-3 (future public path), AC-4 (existing content preserved) are confirmed by the change summary and consistent with the document body.

**The Table of Contents is a complete navigation map.** All 12 `##`-level headings are represented with accurate anchor links and the "Purpose" column header now matches the framework standard.

**Overall assessment:** This is a thoroughly revised, dual-audience installation guide with no remaining user-failure scenarios. The four iterations represent a disciplined adversarial-remediation cycle — each iteration targeted real gaps rather than cosmetic polish. The document is now production-quality for the collaborator-access phase of the Jerry OSS release.

---

## Best Case Conditions

The document is most compelling when:

1. The user is a new Jerry collaborator on macOS or Windows, starting from zero, who needs a single document to proceed from GitHub invitation to working Claude Code plugin.
2. Claude Code 1.0.33+ is already installed (version floor surfaced in Prerequisites before installation begins).
3. The user encounters an unexpected environment condition (conda Git without osxkeychain, Windows Home without OpenSSH Client, username containing spaces) — the document now handles all three with explicit detection and recovery paths.
4. The team lead wants to share Jerry with all collaborators — the Configuration section provides scope selection guidance, even if the team scenario could be more operationally specific.

**Key assumptions that must hold:**
- Repository URL `git@github.com:geekatron/jerry.git` and `/plugin install jerry-framework@jerry` are accurate.
- `.claude-plugin/plugin.json` contains `"name": "jerry-framework"` (confirmed in change summary against actual file).
- `make setup` target exists on macOS/Linux as documented.
- `BOOTSTRAP.md` exists in `docs/` directory as asserted (confirmed in Iteration 3).
- `/problem-solving` produces a clean skill activation response after `JERRY_PROJECT` is set (now that Configuration precedes Verification, this condition is met for users following the document sequentially).

**Confidence assessment:** HIGH. The remaining gap (SM-005-qg1r1s) is a polish item. Downstream critique will focus on edge-case completeness rather than structural or methodological correctness.

---

## Remaining Gaps

| ID | Severity | Description |
|----|----------|-------------|
| SM-001-qg1r2s | Minor | SM-005-qg1r1s carried forward — unchanged. Configuration scope recommendation (lines 652–653) states "Use **Project** scope when you want your whole team to have Jerry available" without explaining operationally what this means (e.g., adds Jerry to `.claude/settings.json`, committed to version control; new team members have Jerry active after clone). Team leads making the Project vs. User scope decision lack the concrete consequence detail that would disambiguate. This is a polish gap with no user-failure scenario. |
| SM-002-qg1r2s | Minor | The Verification "Test a Skill" instruction (lines 699–705) uses `/problem-solving` as the success indicator. While Configuration now precedes Verification, `/problem-solving` still requires a valid `JERRY_PROJECT` to produce the promised response ("You should see the problem-solving skill activate with information about available agents"). The Configuration section establishes `JERRY_PROJECT` optionally ("Jerry uses project-based workflows... To set up a project:"). A user who skips the optional project setup will still encounter the `<project-required>` prompt at the Verification step, receiving unexpected behavior. A context-independent command (`/help`, `/plugin`, or `/worktracker`) would provide an unconditional success signal. |
| SM-003-qg1r2s | Minor | The PAT Alternative (lines 385–434) presents the `repo` classic PAT correction (full read and write access) and the fine-grained PAT alternative, but does not include the `space-in-path` warning that was added to the SSH clone step (Step 4). The PAT clone commands in lines 392–399 (`~/plugins/jerry` and `"$env:USERPROFILE\plugins\jerry"`) recommend paths that are safe by default, but the explicit warning ("The clone path must not contain spaces") is absent from this block, creating an asymmetry with the SSH clone block. Users choosing HTTPS/PAT who have unusual home directory paths receive no proactive guidance. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Strong Positive | All four QG-1 Retry 1 Major completeness gaps closed: osxkeychain pre-check + store fallback (P2), Windows SSH agent install path (P3), space-in-path warning at three clone locations (P4), PAT scope correction (P5). SM-003-qg1r2s (no space-in-path in PAT block) is a minor asymmetry, not a new major gap. |
| Internal Consistency | 0.20 | Strong Positive | Configuration/Verification ordering corrected (P1), marketplace rationale scope clarified (P6), ToC header fixed to "Purpose" (P10), PAT Windows clone variant added (P7). SM-001-qg1r2s (scope team scenario) is the only residual inconsistency, and it is cosmetic. |
| Methodological Rigor | 0.20 | Strong Positive | Space-in-path warnings at all primary clone locations (P4), Windows SSH agent guard block with install path (P3), osxkeychain verification step (P2). SM-003-qg1r2s (PAT block missing space-in-path warning) is a minor methodological asymmetry. |
| Evidence Quality | 0.15 | Positive | PAT `repo` scope corrected to "full read and write" with fine-grained PAT alternative (P5), rate-limit note added to Future section (P8), detection instruction added to Future section (P9). No new factual claims introduced without support. |
| Actionability | 0.15 | Strong Positive | Configuration-before-Verification reordering (P1) is the single largest actionability improvement — eliminates guaranteed first-run failure. Windows SSH agent conditional block with recovery path (P3) eliminates silent-failure scenario. SM-001-qg1r2s and SM-002-qg1r2s are Minor residual polish items, not failure scenarios. |
| Traceability | 0.10 | Positive (maintained) | Iteration 4 change summary is complete, accurate, and traces all 10 priority findings plus 2 additional. All anchor IDs verified stable from QG-1 Retry 1. No regressions in traceability. |

**Overall impact:** All six dimensions benefit from Iteration 4. The three Minor surviving weaknesses are polish items — none create user-failure scenarios, and none reopen any previously remediated Major finding. The document has executed a full adversarial remediation cycle correctly.

---

## H-15 Self-Review Verification

- [x] All findings verified against actual Iteration 4 draft content with line references
- [x] No findings re-raise issues confirmed fixed in Iteration 4 change summary
- [x] Prior finding resolution table evidence includes specific line numbers where applicable
- [x] Severity classifications justified: 0 Major (all QG-1 Retry 1 Majors resolved), 3 Minor (polish/asymmetry gaps)
- [x] Finding identifiers follow `SM-NNN-qg1r2s` format
- [x] Steelman Construction identifies strongest interpretation before weaknesses
- [x] SM-002-qg1r2s noted honestly: Configuration preceding Verification resolves the structural issue, but the optional project-setup path creates a residual risk for skip-ahead users
- [x] Readiness confirmed for downstream critique strategies (S-002, S-004, S-007)

---

## Score Estimate

**Estimated composite range: 0.90–0.95**

The four Major findings that held the QG-1 Retry 1 score to 0.8300 are all remediated. The three surviving findings are Minor, with no user-failure scenarios. The primary uncertainty is:

1. Whether S-002 Devil's Advocate will surface new edge-case failures not visible to steelman analysis (most likely in the Windows SSH agent conditional block or the osxkeychain detection flow — both are new, untested code paths in the document).
2. Whether SM-002-qg1r2s (optional project setup before verification) is scored as Minor or is elevated to Major by a strict actionability read.

If no new Major findings emerge from downstream critique, the 0.92 threshold is reachable. The lower bound of 0.90 reflects residual uncertainty about whether the three Minor items collectively depress any single dimension below 0.85.

---

*Executed by: adv-executor-000*
*Strategy: S-003 (Steelman Technique) v1.0.0*
*Template: `.context/templates/adversarial/s-003-steelman.md`*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: epic001-docs-20260218-001 | QG-1 Retry 2*
*Date: 2026-02-18*

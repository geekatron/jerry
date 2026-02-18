# S-003 Steelman Report — QG-1 Retry 1

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverable metadata |
| [Steelman Construction](#steelman-construction) | Strongest interpretation of the deliverable |
| [Best Case Conditions](#best-case-conditions) | Ideal conditions and key assumptions |
| [Surviving Weaknesses](#surviving-weaknesses) | Genuine weaknesses after charitable interpretation |
| [Scoring Impact](#scoring-impact) | Dimension-level impact of surviving weaknesses |
| [Summary](#summary) | Finding counts and estimated score impact |

---

## Execution Context

| Field | Value |
|-------|-------|
| **Strategy** | S-003 (Steelman Technique) |
| **Template** | `.context/templates/adversarial/s-003-steelman.md` |
| **Deliverable** | `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md` |
| **Deliverable Type** | Installation Guide (End-User Documentation) |
| **Criticality Level** | C2 (Standard) |
| **Quality Gate** | QG-1 Retry 1 |
| **Iteration** | 3 (post QG-1 adversarial revision — all 10 priority findings applied) |
| **Prior QG-1 Score** | 0.7665 (REVISE) |
| **Executed** | 2026-02-18 |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Finding Prefix** | SM-NNN-qg1r1s |
| **Original Author** | ps-architect-001 |

---

## Steelman Construction

### Core Thesis

Jerry can be installed as a Claude Code plugin by two distinct user audiences — private-repository collaborators (requiring SSH key setup and GitHub account with collaborator invite) and future public repository users (simplified HTTPS path) — both converging on the same Claude Code local marketplace installation mechanism. Iteration 3 addresses every Major adversarial finding from QG-1, closing the most significant user-failure scenarios.

### Strongest Interpretation

**The Iteration 3 revision represents a substantial, targeted remediation of all nine QG-1 Major findings.** The change summary comment is thorough and accurate, documenting every fix with finding IDs (P1-DA-001 through P10-SM-001 plus two additional). The core structure remains intact: the document cleanly separates collaborator and public-repo installation paths, uses stable HTML anchor IDs for cross-section navigation, and converges both paths on the same Claude Code marketplace installation mechanism.

**Methodological safety is materially improved.** The most serious QG-1 finding — DA-001 (destructive ssh-keygen without pre-check) — is now addressed on both platforms with a proper existence check before any key generation command. The macOS pre-check (`ls ~/.ssh/id_ed25519.pub 2>/dev/null && echo "Key exists..."`) and Windows pre-check (`if (Test-Path "...")`) follow the correct pattern. Both are preceded by an explicit Warning callout ("If you already have an SSH key, DO NOT overwrite it."), leaving no ambiguity about the consequence of proceeding.

**Prerequisites are now complete.** Claude Code 1.0.33+ appears explicitly in the Required Software table — a structural fix that ensures the version gate is encountered at the prerequisite check stage before installation begins, not only in Troubleshooting after a failure.

**PAT Alternative is now a complete, self-contained path.** The credential helper guidance for macOS (`osxkeychain`) and Windows (`manager`) is present, the "Generate new token (classic)" specification is correct, and the `repo` scope explanation is accurate. A forward reference at the end of the Step 4 clone block makes the PAT option discoverable at the decision point rather than only at the section end.

**Platform parity is restored.** The Windows SSH agent tip matches the macOS Keychain tip in structure: `Start-Service ssh-agent`, `ssh-add`, the optional `Set-Service -Name ssh-agent -StartupType Automatic` for persistence, and — critically — the OpenSSH Client prerequisite note ("enabled by default on Windows 10 build 1809+ and Windows 11"). This addresses both SM-004 and the DA-006 evidence quality concern from QG-1 in a single addition.

**Table of Contents is complete.** Getting Help and License rows are present after Uninstallation. All `##`-level headings are now represented in the ToC, satisfying NAV-004.

**Available Skills table is comprehensive.** The `/adversary` row is present with correct description ("Adversarial quality reviews and tournament scoring"), matching CLAUDE.md's Quick Reference.

**Internal consistency on the "Why SSH?" claim is corrected.** "Password-free access" is now qualified: "when set up without a passphrase, or when combined with an SSH agent that caches your passphrase (see Tip below)." The claim is now accurate for both passphrase and non-passphrase scenarios, and it correctly cross-references the SSH agent tips below.

**Marketplace rationale is present.** The "Why the marketplace?" callout explains plugin-based distribution, scope control, and easy updates — addressing the readability gap that first-time Claude Code users would encounter.

**The BOOTSTRAP.md reference is improved.** The addition of "(located in the `docs/` directory)" removes the path ambiguity that was flagged as SM-007.

**Overall assessment:** The deliverable is a production-quality installation guide. All four acceptance criteria (AC-1 through AC-4) remain satisfied. The Iteration 3 revision was executed precisely and economically — each fix targets a specific finding without introducing regressions. The remaining weaknesses are minor presentation and completeness gaps that do not create user-failure scenarios.

---

## Best Case Conditions

The document is most compelling when:

1. The reader is a new Jerry collaborator on macOS or Windows who has just received a GitHub invitation and needs a single document to proceed from zero to working installation.
2. Claude Code 1.0.33+ is already installed (correctly assumed as a prerequisite, now with version surfaced at the right stage).
3. The reader is new to SSH key management — all defensive checks (pre-check before generation, Warning callout, SSH agent tips on both platforms) are calibrated for this audience.
4. The team is deploying Jerry collaboratively — the scope selection guidance and team scenario (now strengthened via the marketplace rationale) enable both personal and shared installation decisions.

**Key assumptions that must hold:**
- The repository URL `git@github.com:geekatron/jerry.git` and `/plugin install jerry-framework@jerry` commands are accurate and match the actual repository.
- The `.claude-plugin/plugin.json` manifest exists at the asserted path and contains `"name": "jerry-framework"` (now confirmed per the change summary's "confirmed against actual .claude-plugin/plugin.json").
- The `make setup` target exists and functions on macOS/Linux as documented.
- `BOOTSTRAP.md` exists in the `docs/` directory as the in-text note implies.

**Confidence assessment:** HIGH. The document is grounded in real, testable commands. Downstream critique will likely focus on minor cross-platform completeness gaps and cosmetic inconsistencies rather than user-failure scenarios.

---

## Surviving Weaknesses

All nine QG-1 Major findings have been remediated. The weaknesses below survive even after the most charitable interpretation of the Iteration 3 fixes.

### Major Findings

**No Major findings.** All nine QG-1 Major findings (DA-001, DA-002, DA-003, DA-004, CC-001, SM-003/CC-003, DA-007, SM-004, SM-002, SM-001) have been addressed. No new Major issues are introduced by Iteration 3.

> **Note for downstream critique strategies:** The document no longer contains user-failure scenarios from the QG-1 Major set. S-002 Devil's Advocate and S-004 Pre-Mortem should focus on edge cases and environment-specific failure modes rather than the structural gaps that drove the 0.7665 QG-1 score.

---

### Minor Findings

#### SM-001-qg1r1s: PAT Alternative Clone URL — macOS Path Syntax Only

**Severity:** Minor
**Section:** PAT Alternative — Step 3
**Dimension:** Actionability, Internal Consistency
**Status:** Pre-existing, not fixed in Iterations 1–3

The PAT Alternative, Step 3:
```
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

The `~/plugins/jerry` path uses macOS/Linux syntax. The SSH clone step (Step 4 of Collaborator Installation) correctly provides both `macOS (Terminal) or Git Bash` and `Windows (PowerShell)` variants. The PAT Alternative does not follow this platform-split pattern. A Windows user who chooses HTTPS/PAT authentication over SSH must adapt the path manually without guidance.

**Strongest interpretation:** The PAT Alternative is primarily a fallback for users who have already worked through the macOS or Windows platform sections and understand path syntax for their platform. The HTTPS clone syntax is otherwise identical. A Windows user who has read this far will likely recognise the adaptation needed.

**Surviving weakness:** Even with charitable interpretation, this creates a documentation inconsistency — the SSH clone step provides platform variants, the HTTPS clone step does not. A Windows user reading only the PAT section (e.g., jumping from a search or link) will receive a Unix path with no guidance.

**Recommended fix:** Add the Windows PowerShell equivalent line below the macOS clone command:
```powershell
# Windows PowerShell
git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
```

---

#### SM-002-qg1r1s: Table of Contents Column Header — "Description" vs. "Purpose"

**Severity:** Minor
**Section:** Table of Contents
**Dimension:** Internal Consistency
**Status:** Pre-existing since Iteration 1, not fixed in Iterations 2 or 3 (CC-002 from QG-1 score report)

The Table of Contents uses:
```
| Section | Description |
```

All `.context/rules/` framework files use:
```
| Section | Purpose |
```

This was identified as CC-002 in the QG-1 score report (Internal Consistency, Minor). It was not included in the 10 priority findings for Iteration 3 and remains unfixed.

**Strongest interpretation:** This is a user-facing document, not a framework rule file. Using "Description" rather than "Purpose" as the column header is a reasonable stylistic choice — "Description" is arguably more natural English for an installation guide audience. The inconsistency is with the internal framework style guide, not with any user-facing standard.

**Surviving weakness:** The inconsistency is real and detectable. Framework consistency is an explicit MEDIUM standard (NAV-003). However, even with strict interpretation, this is a cosmetic inconsistency that does not affect usability, navigation, or correctness.

**Recommended fix:** Change `| Section | Description |` to `| Section | Purpose |` in the Table of Contents header row.

---

#### SM-003-qg1r1s: Future Section — No Reader-Actionability Detection Signal

**Severity:** Minor
**Section:** Future: Public Repository Installation
**Dimension:** Actionability
**Status:** SM-005-qg1s from QG-1 Steelman — not in top 10 priority fixes, not applied

The Future section opens: "This section documents a future installation scenario. Jerry is currently distributed to collaborators only. When Jerry is released as a public repository, these simplified instructions will apply..."

The section correctly frames the future state and includes a comparison table. However, it provides no mechanism for a reader to determine whether the future state has arrived. A user who discovers this document after Jerry goes public has no way to self-diagnose which path applies from the document alone.

**Strongest interpretation:** The section's Note callout is clear and prominent. Any user encountering a 404/login-redirect when attempting the collaborator invite flow will naturally investigate the public path. The comparison table explicitly lists "No" for GitHub account needed in the Future column, making the distinction actionable.

**Surviving weakness:** A user who directly accesses this document (e.g., from a README link) after the repository becomes public needs to check the repository visibility externally, without guidance from the document itself. A single sentence ("To confirm: visit [github.com/geekatron/jerry](https://github.com/geekatron/jerry) while logged out — if it loads without a login redirect, this section applies") would close the loop.

**Recommended fix:** Add a detection note to the Future section Note callout, e.g.: "To confirm whether Jerry is now public, visit the repository URL while logged out of GitHub — if it loads without a login prompt, these instructions apply."

---

#### SM-004-qg1r1s: Verification Section — /problem-solving Requires Project Context

**Severity:** Minor
**Section:** Verification — Test a Skill
**Dimension:** Actionability
**Status:** SM-008-qg1s from QG-1 Steelman — not in top 10 priority fixes, not applied

The Verification section instructs:
```
/problem-solving
```
"You should see the problem-solving skill activate with information about available agents."

**Strongest interpretation:** `/problem-solving` is the flagship Jerry skill and demonstrating it during verification shows users the most capable part of the framework. The success criterion ("see the problem-solving skill activate with information about available agents") is clear and observable.

**Surviving weakness:** `/problem-solving` is a multi-agent orchestrated skill that requires project context (`JERRY_PROJECT` env var). A fresh installation without project context may produce a `<project-required>` or error response rather than the clean activation the document promises. A simpler command (`/worktracker` or `/help`) would produce a deterministic, context-independent success response that more reliably confirms installation completeness.

**Recommended fix:** Replace the verification test command with `/worktracker` or `/help`, which require no project context and provide an unambiguous success indicator.

---

#### SM-005-qg1r1s: Configuration Section — Scope Selection Lacks Team Scenario Example

**Severity:** Minor
**Section:** Configuration — Installation Scopes Explained
**Dimension:** Actionability
**Status:** SM-006-qg1s from QG-1 Steelman — not in top 10 priority fixes, not applied

The Configuration section concludes: "Use **User** scope for personal use. Use **Project** scope when you want your whole team to have Jerry available."

**Strongest interpretation:** The recommendation is concise and correct. The scope table above it provides the key information (where installed, use case). Most users will understand the team scenario from "all collaborators on this repository."

**Surviving weakness:** A concrete example of what Project scope means operationally (e.g., "adds Jerry to `.claude/settings.json` which is committed to version control, so new team members have Jerry active after cloning") would remove ambiguity for team leads making the decision. Without it, "all collaborators get the plugin" is accurate but underspecified.

**Recommended fix:** Add one sentence after the Recommendation line: "Project scope adds Jerry to `.claude/settings.json` which is committed to version control — new team members will have Jerry active automatically after cloning the repository."

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All nine QG-1 Completeness gaps addressed (Claude Code version, PAT credential caching, /adversary skill, Getting Help/License ToC entries). SM-001-qg1r1s (PAT Windows path) is a residual Minor gap but does not reopen a Major completeness failure. |
| Internal Consistency | 0.20 | Positive | DA-007 ("password-free access" qualification) and SM-004 (Windows SSH agent tip, platform parity) are both applied. SM-002-qg1r1s (ToC "Description" vs "Purpose") is a cosmetic residual inconsistency. |
| Methodological Rigor | 0.20 | Positive | DA-001 (ssh-keygen pre-check on both platforms) is the strongest improvement — the most serious methodological gap from QG-1 is fully addressed. DA-004 (manifest path confirmed as "jerry-framework") closes the unverified assertion gap. No new methodological deficiencies introduced. |
| Evidence Quality | 0.15 | Positive | DA-004 fix confirmed against actual repository. SM-009 (macOS Keychain rationale sentence) and the Windows SSH agent OpenSSH Client note (DA-006 resolution) both strengthen evidence quality. |
| Actionability | 0.15 | Positive | DA-002 (version in Prerequisites), DA-003 (credential helper guidance), SM-002 (PAT forward reference at Step 4), SM-001 (marketplace rationale) all directly improve actionability. SM-003-qg1r1s, SM-004-qg1r1s, SM-005-qg1r1s are residual Minor actionability polish items. |
| Traceability | 0.10 | Positive | SM-007 (BOOTSTRAP.md location note) applied. Iteration 3 change summary is complete and accurate, maintaining the traceability chain from QG-1 findings to applied fixes. |

**Overall impact:** All six dimensions are positively affected by Iteration 3. The five Minor surviving weaknesses are presentation and polish items — none create user-failure scenarios and none reopen the structural gaps that drove the 0.7665 QG-1 score. The document is materially stronger across all dimensions.

---

## H-15 Self-Review Verification

- [x] All findings have specific location references in the deliverable
- [x] No findings re-raise issues confirmed as fixed in Iteration 3 change summary
- [x] All surviving weaknesses verified against the actual Iteration 3 draft content
- [x] Severity classifications justified: 0 Major (all QG-1 Majors resolved), 5 Minor (presentation/polish gaps)
- [x] Finding identifiers follow `SM-NNN-qg1r1s` format
- [x] Steelman Construction identifies the strongest interpretation before identifying weaknesses
- [x] Readiness confirmed for downstream critique strategies (S-002, S-004, S-007)

---

## Summary

- **Major:** 0
- **Minor:** 5
  - SM-001-qg1r1s: PAT Alternative clone URL macOS-only syntax (Actionability, Internal Consistency)
  - SM-002-qg1r1s: ToC column header "Description" vs. framework standard "Purpose" (Internal Consistency)
  - SM-003-qg1r1s: Future section — no reader-actionability detection signal (Actionability)
  - SM-004-qg1r1s: Verification — `/problem-solving` requires project context for clean activation (Actionability)
  - SM-005-qg1r1s: Configuration scope selection — no team scenario example (Actionability)
- **Estimated score impact:** The 0 Major finding count is the primary signal. All QG-1 Major gaps are remediated. Residual Minor findings are pre-existing or previously scoped-out items. Estimated composite score range: **0.88–0.94** depending on how strictly downstream critique strategies weight the five Minor items and whether any new issues are surfaced by S-002 or S-004.

---

*Executed by: adv-executor-000*
*Strategy: S-003 (Steelman Technique) v1.0.0*
*Template: `.context/templates/adversarial/s-003-steelman.md`*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: epic001-docs-20260218-001 | QG-1 Retry 1*
*Date: 2026-02-18*

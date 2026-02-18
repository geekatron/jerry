# Quality Score Report: FEAT-017 Installation Instructions (QG-1 Retry 1)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, and plain-language assessment |
| [Scoring Context](#scoring-context) | Deliverable metadata and strategy references |
| [Score Summary](#score-summary) | Weighted composite table |
| [Dimension Scores](#dimension-scores) | Scored dimensions with evidence |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, improvement path |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered action table |
| [Leniency Bias Check](#leniency-bias-check) | Anti-bias validation checklist |

---

## L0 Executive Summary

**Score:** 0.8300/1.00 | **Verdict:** REJECTED | **Weakest Dimension:** Actionability (0.81) / Internal Consistency (0.81)

**One-line assessment:** Iteration 3 successfully remediated all 9 QG-1 Major findings, but Devil's Advocate surfaced 4 new Major issues — unaddressed PAT credential helper gap, Windows SSH agent silent-failure path, space-in-path warning omission, and a structural Verification/Configuration ordering error — that collectively prevent the document from reaching the REVISE threshold (0.85).

---

## Scoring Context

| Field | Value |
|-------|-------|
| **Deliverable** | `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md` |
| **Deliverable Type** | Documentation (Installation Guide) |
| **Criticality Level** | C2 |
| **Scoring Strategy** | S-014 (LLM-as-Judge) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Scored** | 2026-02-18 |
| **Prior Score** | 0.7665 (QG-1 initial) |
| **Strategy Reports** | S-003 Steelman (adv-executor-000), S-002 Devil's Advocate (adv-executor-001), S-007 Constitutional (adv-executor-002) |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.8300 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REJECTED (< 0.85) |
| **Strategy Findings Incorporated** | Yes — 3 reports |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.1640 | All 9 QG-1 Majors resolved; 2 new unaddressed Major gaps (DA-001: osxkeychain no pre-check; DA-002: Windows SSH agent no service-fallback) |
| Internal Consistency | 0.20 | 0.81 | 0.1620 | DA-004: Verification placed before Configuration — every new user will hit unexpected JERRY_PROJECT state; DA-005 marketplace/install scope conflation (Minor) |
| Methodological Rigor | 0.20 | 0.84 | 0.1680 | Overall instruction methodology sound; ssh-keygen pre-check fully addressed (QG-1 Major resolved); DA-003 new gap: space-in-path not warned against in clone path recommendation |
| Evidence Quality | 0.15 | 0.83 | 0.1245 | All factual claims verified accurate by S-007; DA-003 classified as Major Evidence Quality (path risk undisclosed); DA-006 PAT `repo` scope described as "read access" — factual understatement |
| Actionability | 0.15 | 0.81 | 0.1215 | DA-002: Windows SSH agent gives failing command with no recovery path; DA-004: test skill step guaranteed to fail for new users before JERRY_PROJECT set; SM-003/SM-004/SM-005 Minor residuals |
| Traceability | 0.10 | 0.90 | 0.0900 | Stable HTML anchor IDs; complete iteration change summary; all cross-references verified by S-007; BOOTSTRAP.md, CONTRIBUTING.md, LICENSE paths accurate |
| **TOTAL** | **1.00** | | **0.8300** | |

---

## Detailed Dimension Analysis

### Completeness (0.82)

**Evidence of strength:**
- All 9 QG-1 Major completeness findings remediated: ssh-keygen pre-check on both platforms, Claude Code 1.0.33+ version in Prerequisites, PAT credential helper guidance added, manifest name corrected to `"name": "jerry-framework"`, Windows SSH agent tip added, `/adversary` row in Available Skills, Getting Help/License in ToC, marketplace rationale callout, SSH forward reference.
- Steelman confirms all four acceptance criteria (AC-1 through AC-4) remain satisfied.
- Table of Contents covers all 12 `##`-level sections (confirmed by S-007).

**Gaps:**
- DA-001-qg1r1-da (Major): PAT Alternative credential helper section instructs `git config --global credential.helper osxkeychain` with no verification step (`git credential-osxkeychain version`). When osxkeychain is absent (conda, nix, MacPorts installs), git silently fails or errors with no guidance in the Troubleshooting section. The Troubleshooting section does not cover this failure mode.
- DA-002-qg1r1-da (Major): Windows SSH agent Tip instructs `Start-Service ssh-agent` but the note "enabled by default on Windows 10 build 1809+" is incomplete — Windows 10 Home and LTSC editions frequently ship without the OpenSSH Client optional feature even above that build. `Start-Service ssh-agent` fails with "Cannot find any service with service name 'ssh-agent'" on these machines, with no documented recovery path.
- DA-007-qg1r1-da (Minor): Future section states "No GitHub account is required to clone a public repository" without noting that unauthenticated HTTPS clones may be subject to GitHub rate limits.
- SM-001-qg1r1s (Minor): PAT Alternative Step 3 clone URL uses macOS/Linux path syntax only (`~/plugins/jerry`); Windows PowerShell variant not provided, inconsistent with the SSH clone step which provides both variants.

**Improvement path:** Add `git credential-osxkeychain version` pre-check and `credential.helper store` fallback to PAT Alternative. Extend Windows SSH agent Tip with `Get-Service ssh-agent -ErrorAction SilentlyContinue` check and `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0` install path.

---

### Internal Consistency (0.81)

**Evidence of strength:**
- DA-007 qualification applied: "password-free access" now correctly qualified with passphrase and SSH agent scenarios.
- Platform parity restored: Windows SSH agent Tip now matches macOS Keychain Tip structure.
- Collaborator cross-references to platform steps use stable explicit HTML anchor IDs (`#macos-step-3`, `#windows-step-3`).
- PAT Alternative forward reference added at Step 4 clone block.

**Gaps:**
- DA-004-qg1r1-da (Major): The document's Verification section instructs "Run a simple skill to verify everything works: `/problem-solving`" — but the Configuration section (which appears after Verification in both the ToC and the document body) is where `JERRY_PROJECT` is established. CLAUDE.md H-04 and the SessionStart hook guarantee that without `JERRY_PROJECT`, a `<project-required>` prompt appears rather than the skill activation the Verification section promises. Every new user following the document in order will encounter an unexpected state at the critical first-run moment.
- DA-005-qg1r1-da (Minor): The "Why the Marketplace?" callout states "the scope you choose at install time determines who gets it" — scope is chosen during `/plugin install`, not during `/plugin marketplace add`. A reader could interpret this as the marketplace-add step having a scope selector, which it does not.
- SM-002-qg1r1s / CC-001-qg1r1-007 (Minor): ToC column header uses "Description" rather than the framework NAV-003 standard "Purpose". Cosmetic; no functional impact confirmed by S-007.

**Improvement path:** Either (a) move JERRY_PROJECT setup into the Verification section before "Test a Skill", (b) add an explicit note that the project-selection prompt is expected first-run behavior, or (c) replace `/problem-solving` with a context-independent command (`/help` or `/plugin`). Address the marketplace rationale sentence with a single clarification.

---

### Methodological Rigor (0.84)

**Evidence of strength:**
- DA-001-qg1s (ssh-keygen destructive pre-check) fully addressed: both platforms now show key-existence check before any key generation, preceded by an explicit Warning callout. This was the most serious methodological gap from QG-1 and is cleanly resolved.
- Stable HTML anchor IDs replace fragile auto-generated duplicate heading anchors (MAJOR-001 from Iteration 2).
- Dual numbering system conflict eliminated (MAJOR-002 from Iteration 2).
- PAT Alternative is self-contained with credential caching for both platforms.
- Sequential, testable steps throughout; platform-specific commands consistently separated.

**Gaps:**
- DA-003-qg1r1-da (Major): The path recommendation "Clone the repository to a location on your system. We recommend `~/plugins/`" leaves the door open for any path. Paths containing spaces will cause `/plugin marketplace add <path>` to fail — the command parser treats the space as an argument separator. The Troubleshooting section covers "use forward slashes" but not spaces in path names. The recommendation should explicitly state that the clone path must not contain spaces.

**Improvement path:** Add a note alongside the path recommendation: "Avoid paths containing spaces — the Claude Code `/plugin marketplace add` command does not support paths with spaces. The recommended `~/plugins/` path is safe."

---

### Evidence Quality (0.83)

**Evidence of strength:**
- S-007 Constitutional confirms all factual claims verified accurate against repository state: `"name": "jerry-framework"` in plugin.json, BOOTSTRAP.md location, script paths, Makefile targets, CONTRIBUTING.md path, Apache License 2.0, all 7 skills.
- DA-004 fix in QG-1 (manifest name) explicitly confirmed against actual `.claude-plugin/plugin.json`.
- SM-009 (macOS Keychain rationale sentence) and Windows SSH agent OpenSSH Client note both add evidence-backed explanations.
- S-007 notes a pre-existing plugin.json `"license": "MIT"` inconsistency with the actual LICENSE file — this is not a deliverable defect and the deliverable correctly cites Apache 2.0.

**Gaps:**
- DA-003-qg1r1-da (Major, Evidence Quality): The path recommendation claims any location is acceptable ("Clone the repository to a location on your system"). The evidence in the document does not disclose the space-in-path failure mode for the downstream `/plugin marketplace add` command. The claim is not technically false, but it is materially incomplete in a way that will cause predictable failures for users with spaces in their home directory path.
- DA-006-qg1r1-da (Minor): PAT Alternative Step 1 describes the `repo` scope as granting "read access to private repositories you collaborate on." The `repo` scope grants full read AND write access to all private repositories — the description is a factual understatement. Fine-grained PATs with `contents:read` scoped to specific repositories are available and more appropriate for this use case.

**Improvement path:** Correct the PAT scope description to accurately state "full read and write access to private repositories" and note the fine-grained PAT alternative. Add space-in-path warning to path recommendation (overlaps with Methodological Rigor gap).

---

### Actionability (0.81)

**Evidence of strength:**
- Troubleshooting section is comprehensive: covers Plugin Command Not Recognized, Plugin Not Found, `uv: command not found`, Skills Not Appearing, Path Issues on Windows, SSH Authentication Failed, Repository Not Found — each with specific symptoms and numbered solutions.
- Platform-split commands throughout: macOS Terminal/Git Bash and Windows PowerShell variants for all key operations.
- "Why the marketplace?" callout improves first-time Claude Code user orientation.
- SSH agent tips on both platforms improve repeat-use experience.

**Gaps:**
- DA-002-qg1r1-da (Major): Windows SSH agent Tip delivers `Start-Service ssh-agent` then `ssh-add` as a ready-to-execute block, but on editions where the OpenSSH Client service does not exist, `Start-Service` fails immediately. No diagnostic command, no install path, no fallback is provided. The user receives a command block that fails and has no documented recovery.
- DA-004-qg1r1-da (Major): Verification "Test a Skill" step instructs the user to run `/problem-solving` and states "You should see the problem-solving skill activate with information about available agents." For every new user who has not yet set `JERRY_PROJECT`, this step will produce a project-selection prompt instead — an unexpected state that provides no indication of what to do next and no connection to the Configuration section that would resolve it.
- SM-003-qg1r1s (Minor): Future section provides no mechanism for a reader to detect whether the future state has arrived (no "visit repo URL while logged out" detection note).
- SM-004-qg1r1s (Minor): `/problem-solving` as verification test is problematic independent of ordering (as S-003 Steelman also flags).
- SM-005-qg1r1s (Minor): Project-scope "all collaborators get the plugin" is accurate but underspecified; no example of what this means operationally.

**Improvement path:** Highest priority is DA-004 — restructure or annotate the Verification/Configuration sequence. Second priority is DA-002 — add service-existence check and OpenSSH Client install path to Windows SSH agent Tip.

---

### Traceability (0.90)

**Evidence of strength:**
- Explicit HTML anchor IDs (`<a id="macos-step-3"></a>`, `<a id="windows-step-3"></a>`) ensure stable cross-section navigation that does not depend on GitHub's heading-slug auto-generation.
- S-007 Constitutional verifies: all 12 ToC anchor links resolve correctly; `#collaborator-installation-private-repository`, `#future-public-repository-installation`, `#for-developers`, and internal cross-refs (`#macos-step-3`, `#windows-step-3`, `#pat-alternative`, `#macos`, `#windows`) all function.
- Iteration change summary comment (lines 1–121) is a complete traceability record: documents each fix with finding IDs, describes the change, and states the satisfaction rationale (EN-940, EN-941, AC-1 through AC-4, P1-DA-001 through P10-SM-001, SM-007, SM-009).
- All referenced external files (BOOTSTRAP.md, CONTRIBUTING.md, LICENSE) verified present by S-007 with correct relative paths.
- No traceability gaps identified by any of the three strategy reports.

**Gaps:**
- None identified that affect the score. The SM-002-qg1r1s "Description" vs "Purpose" column header is cosmetic and has zero traceability impact.

---

## Improvement Recommendations (Priority Ordered)

| Priority | ID | Finding | Dimension(s) | Required Action |
|----------|-----|---------|--------------|-----------------|
| P1 | DA-004-qg1r1-da | Verification/Configuration ordering; `/problem-solving` fails for all new users before JERRY_PROJECT set | Internal Consistency, Actionability | (a) Move JERRY_PROJECT setup before "Test a Skill", OR (b) add explicit note that project-selection prompt is expected first-run behavior, OR (c) replace `/problem-solving` with `/help` or `/plugin` (context-independent). |
| P2 | DA-001-qg1r1-da | PAT osxkeychain assumes helper availability; no verification or fallback | Completeness | Add `git credential-osxkeychain version` pre-check before `git config` command; add `credential.helper store` fallback with security note (plaintext storage in `~/.git-credentials`). |
| P3 | DA-002-qg1r1-da | Windows SSH agent `Start-Service ssh-agent` fails on editions without OpenSSH Client | Completeness, Actionability | Add `Get-Service ssh-agent -ErrorAction SilentlyContinue` check; add `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0` install path for when service is not found. |
| P4 | DA-003-qg1r1-da | Path recommendation does not warn about space-in-path failure for marketplace commands | Methodological Rigor, Evidence Quality | Add explicit note: "Avoid paths containing spaces — `/plugin marketplace add` does not support paths with spaces." |
| P5 | DA-006-qg1r1-da | PAT `repo` scope described as "read access" — factual understatement | Evidence Quality | Correct to "full read and write access to private repositories"; note fine-grained PAT with `contents:read` as the principle-of-least-privilege alternative. |
| P6 | DA-005-qg1r1-da | Marketplace rationale conflates marketplace-add scope with plugin-install scope | Internal Consistency | Clarify: "the scope you choose during `/plugin install` determines who gets it" (not during marketplace-add). |
| P7 | SM-001-qg1r1s | PAT Alternative clone URL is macOS-only syntax | Completeness, Internal Consistency | Add Windows PowerShell clone variant below macOS command in PAT Alternative Step 3. |
| P8 | DA-007-qg1r1-da | Future section omits anonymous clone rate-limit risk | Completeness | Add one sentence noting that unauthenticated HTTPS clones may be rate-limited; authenticating resolves this. |
| P9 | SM-003-qg1r1s | Future section provides no detection mechanism for readers | Actionability | Add: "To confirm whether Jerry is now public, visit the repository URL while logged out — if it loads without a login prompt, these instructions apply." |
| P10 | SM-002-qg1r1s / CC-001-qg1r1-007 | ToC column header "Description" vs NAV-003 standard "Purpose" | Internal Consistency | Change `\| Section \| Description \|` to `\| Section \| Purpose \|` — single-character fix. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific finding IDs and location references
- [x] Uncertain scores resolved downward (Completeness: 0.82 not 0.85; Actionability: 0.81 not 0.83)
- [x] Revised-draft calibration considered (iteration 2 of C2 deliverable; calibration anchor 0.80–0.90 for revised drafts that addressed specific feedback — 4 new Major findings from DA justify scores below 0.85)
- [x] No dimension scored above 0.95 without exceptional evidence (Traceability at 0.90 is the highest; fully justified by S-007 verification and stable anchors)
- [x] Score not inflated by QG-1 remediation success — addressing prior Majors is baseline, not cause for score inflation if new Majors are introduced
- [x] DA's 4 new Major findings confirmed as genuine (not re-raised from QG-1 resolved set; QG-1 resolution table in DA report confirms 6/7 cleanly resolved, 1 partially)

---

*Scored by: adv-scorer-001*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: epic001-docs-20260218-001 | QG-1 Retry 1*
*Date: 2026-02-18*
*Prior score: 0.7665 (QG-1 initial) | Current score: 0.8300 | Delta: +0.0635*

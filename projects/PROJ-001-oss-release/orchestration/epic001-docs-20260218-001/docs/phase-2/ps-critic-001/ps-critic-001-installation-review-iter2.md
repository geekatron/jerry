# FEAT-017 Installation Draft — Quality Review (Iteration 2)

> **Agent ID:** ps-critic-001
> **Workflow ID:** epic001-docs-20260218-001
> **Phase:** 2 (FEAT-017 Execution — Creator-Critic Review)
> **Iteration:** 2 (Revision Pass Review)
> **Date:** 2026-02-18
> **Draft Under Review:** `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md`
> **Previous Review:** `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-critic-001/ps-critic-001-installation-review.md`
> **Previous Score:** 0.866 (REVISE)
> **Scoring Method:** S-014 LLM-as-Judge (6-dimension weighted composite)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Overall quality assessment and verdict |
| [AC Verification Matrix](#ac-verification-matrix) | Pass/Fail status for each acceptance criterion |
| [Iteration 1 Issue Resolution](#iteration-1-issue-resolution) | Verification that each iter 1 issue was addressed |
| [Dimension Scores](#dimension-scores) | S-014 rubric scores across all 6 dimensions |
| [Weighted Composite Score](#weighted-composite-score) | Final calculated score and threshold comparison |
| [Residual Issues Found](#residual-issues-found) | Issues that persist or are newly identified |
| [Verdict](#verdict) | PASS / REVISE outcome with rationale |

---

## L0: Executive Summary

The iteration 2 revision by ps-architect-001 addresses all 7 issues raised in the iteration 1 review (2 MAJOR, 5 MINOR) with precision and economy. No existing content was damaged in the remediation pass. The change summary comment in the draft file accurately enumerates every fix applied.

The two MAJOR issues that drove the iteration 1 score down have been cleanly resolved. MAJOR-001 (duplicate heading anchor fragility) is fixed via explicit HTML anchor IDs (`<a id="macos-step-3"></a>` and `<a id="windows-step-3"></a>`) placed immediately before the target headings, with cross-references updated to use the stable IDs. MAJOR-002 (step numbering discontinuity) is resolved by renaming the transition section from "Steps 5–7: Continue with Platform Installation" to "Next Steps: Complete Platform Installation" — this eliminates the dual-numbering conflict without requiring restructuring.

All five MINOR issues have been addressed: the collaborator notes in platform Step 2 now use past-tense acknowledgment (MINOR-001); the Windows SSH path now uses `YOUR_USERNAME` consistently (MINOR-002); the macOS Keychain tip has been added after SSH key generation (MINOR-003); the Future section's uv installation references now point to section-level anchors `#macos` and `#windows` (MINOR-004); and the PAT alternative now specifies classic PAT, the `repo` scope checkbox, and explains the read-access implication (MINOR-005).

Two residual issues were identified that were not present in iteration 1 or were outside its scope. One is substantive but low-impact (Windows ssh-agent passphrase persistence gap); the other is cosmetic (PAT section clone URL uses macOS path syntax only). Neither is threshold-blocking given the magnitude of improvements in this revision pass.

The document is technically sound, internally consistent, and actionable for both collaborator and public-repo installation paths. All four acceptance criteria remain satisfied.

---

## AC Verification Matrix

| AC | Criterion | Verdict | Evidence |
|----|-----------|---------|----------|
| AC-1 | No archive distribution references remain | PASS | Full draft review confirms no `.tar.gz`, `.zip`, "download", "archive", "extract", or similar terms. Distribution model is exclusively marketplace + git clone. Preserved from iteration 1. |
| AC-2 | Step-by-step collaborator installation (SSH key + GitHub + marketplace) | PASS | SSH key generation (macOS + Windows), GitHub key registration, SSH connectivity test, SSH clone URL, transition to marketplace steps via stable anchors, and PAT alternative are all present. The anchor fragility caveat from iteration 1 has been resolved. |
| AC-3 | Public repository installation path documented | PASS | "Future: Public Repository Installation" section is present, clearly framed as future state, includes comparison table, and references platform sections via stable section-level anchors. |
| AC-4 | Claude Code marketplace integration instructions included | PASS | `/plugin marketplace add` and `/plugin install` commands are present in both macOS and Windows sections, unchanged from the original. |

---

## Iteration 1 Issue Resolution

### MAJOR Issues

| Issue | Status | Evidence |
|-------|--------|----------|
| MAJOR-001: Duplicate heading anchors | RESOLVED | Explicit `<a id="macos-step-3"></a>` placed at draft line 306, `<a id="windows-step-3"></a>` at line 391. Cross-references in the "Next Steps" subsection use `#macos-step-3` and `#windows-step-3` (lines 248–249). These IDs are renderer-independent. |
| MAJOR-002: Step numbering discontinuity | RESOLVED | Section title changed to "Next Steps: Complete Platform Installation" (line 244). The "5–7" numbering is removed. The prose enumerates the remaining tasks descriptively ("plugin manifest, marketplace add, plugin install") without asserting global step numbers. |

### MINOR Issues

| Issue | Status | Evidence |
|-------|--------|----------|
| MINOR-001: Collaborator note reverse-navigation | RESOLVED | macOS Step 2 (line 304) and Windows Step 2 (line 389) both now read: "you have already cloned via SSH — skip this step and proceed to Step 3 below." Past-tense acknowledgment removes the ambiguity. |
| MINOR-002: Windows placeholder `YOU` vs `YOUR_USERNAME` | RESOLVED | Line 182 now reads `C:\Users\YOUR_USERNAME\.ssh\id_ed25519`, matching the convention used in Windows Step 4. |
| MINOR-003: macOS Keychain tip absent | RESOLVED | Tip callout added at lines 167–171 immediately after the macOS SSH key generation display step: `eval "$(ssh-agent -s)"` and `ssh-add --apple-use-keychain ~/.ssh/id_ed25519`. Correctly gated on "If you set a passphrase." |
| MINOR-004: Future section fragile step anchors | RESOLVED | Lines 435 and 449 now reference `#macos` and `#windows` section-level anchors. These correspond to the unique `### macOS` and `### Windows` headings under the Installation section and are stable across renderers. |
| MINOR-005: PAT scope explanation incomplete | RESOLVED | Line 259 now specifies: "classic PAT … (select 'Generate new token (classic)') and check the `repo` scope checkbox. This grants read access to private repositories you collaborate on." Distinguishes classic from fine-grained and explains the permission implication. |

**All 7 iteration 1 issues fully resolved.**

---

## Dimension Scores

### Completeness (weight: 0.20)

**Score: 0.93**

All four acceptance criteria are satisfied. The collaborator installation section covers SSH key generation (macOS and Windows), public key registration on GitHub, SSH connectivity verification with expected output, SSH clone commands for both platforms, a transition to the marketplace installation steps, and a PAT alternative. The macOS Keychain passphrase tip (previously absent, MINOR-003) is now present. The Future section covers the simplified HTTPS clone path and comparison table. Two collaborator troubleshooting entries remain from iteration 1.

Residual deduction: Windows ssh-agent passphrase handling is not documented. macOS users with a passphrase now have the Keychain integration tip, but Windows users who set a passphrase face the same re-entry friction on every `git` operation. The Windows `ssh-agent` startup and `ssh-add` equivalent is absent. This asymmetry slightly penalizes completeness parity between platforms. (-0.05)

Minor deduction: The PAT alternative clone URL (line 261) shows only the macOS path format (`~/plugins/jerry`). A Windows user reading only the PAT section would receive a Unix path. The Windows equivalent (`"$env:USERPROFILE\plugins\jerry"`) is absent from that subsection. (-0.02)

### Internal Consistency (weight: 0.20)

**Score: 0.95**

The anchor fragility issue (MAJOR-001) that previously dragged this dimension to 0.78 is fully resolved. The explicit `<a id="...">` anchors are declared in the document and are renderer-independent. Cross-references correctly target those IDs. The step-numbering discontinuity (MAJOR-002) is eliminated — the bridge section no longer asserts global step numbers, so the local numbering in the platform sections (Steps 1–5) is no longer in conflict.

Placeholder naming is now consistent: `YOUR_USERNAME` is used throughout all Windows paths. The "Collaborators" notes in platform Step 2 sections are now consistent with each other (past tense on both macOS and Windows). The PAT section is consistent with the rest of the document in style and scope.

Residual minor deduction: The "Next Steps: Complete Platform Installation" prose at line 246 says "proceed directly to Step 3: Verify the Plugin Manifest" — the step name quoted in prose matches the actual heading text in both platform sections, which is good. No conflict found. The section-level `#macos` and `#windows` anchors in the Future section correctly target the unique `### macOS` and `### Windows` headings. No collision risk. (-0.05 for the Windows ssh-agent asymmetry creating a mild platform parity inconsistency — macOS users get Keychain guidance, Windows users get none.)

### Methodological Rigor (weight: 0.20)

**Score: 0.93**

The SSH setup instructions remain technically correct. All commands from iteration 1 are preserved. The macOS Keychain tip uses the correct modern commands: `eval "$(ssh-agent -s)"` starts the agent and `ssh-add --apple-use-keychain` adds the key to the macOS Keychain (available on macOS 12.0+ and is the current GitHub-recommended approach for passphrase-protected keys).

The PAT specification now correctly distinguishes between classic and fine-grained PATs, and correctly identifies `repo` as the required scope for read access to private repositories. This is accurate — fine-grained PATs require `contents: read` and `metadata: read` at minimum, while classic PATs with `repo` scope cover all needed access.

The `#macos` and `#windows` anchor targets reliably resolve to the unique headings `### macOS` and `### Windows` within the Installation section. These headings are not duplicated elsewhere in the document, confirming the anchor selection is sound.

Residual deduction: The Windows PowerShell ssh-agent start and key-loading procedure is absent. For completeness of the methodological approach, this is a gap: Windows OpenSSH (available since Windows 10 1803 as an optional feature, and built-in from Windows 10 1809+) requires `Start-Service ssh-agent` and `ssh-add ~\.ssh\id_ed25519` for persistent key loading. Without this, Windows users with a passphrase must re-enter it each session — the same friction macOS users are now protected from. (-0.07)

### Evidence Quality (weight: 0.15)

**Score: 0.91**

Command outputs are shown where they matter most. The SSH connectivity verification shows the exact expected GitHub response string (line 219). The uv version check format is preserved. Plugin manifest verification output is present. The macOS Keychain tip adds actionable commands with a clear conditional trigger.

Deductions carried from iteration 1 that remain:
- `ssh-keygen` does not show the interactive terminal exchange (prompt text for file location, passphrase). The prose describes what prompts appear, which is adequate for most users but falls short of the evidence standard a first-time SSH user needs. (-0.05)
- Neither the macOS nor Windows sections show a sample truncated SSH public key. A user unfamiliar with SSH keys may be uncertain whether they copied "the full output" correctly. (-0.03)

Net improvement from MINOR-003 resolution: The macOS Keychain tip represents a concrete evidence improvement — the two commands are shown exactly as the user should type them, with the conditional stated clearly.

### Actionability (weight: 0.15)

**Score: 0.93**

The iteration 1 friction points have been addressed. The collaborator path is now clean:

1. User reads Collaborator Installation, completes Steps 1–4.
2. Arrives at "Next Steps: Complete Platform Installation" — clearly titled, no confusing global step numbers.
3. Clicks `#macos-step-3` or `#windows-step-3` — lands exactly at Step 3 of the correct platform section.
4. Sees the collaborator note in Step 2 of the platform section (which they will scroll past), now reading "you have already cloned via SSH — skip this step" — no reverse-navigation confusion.
5. Completes Steps 3, 4, 5 (manifest, marketplace, install).

The PAT alternative is now more actionable: it specifies where to navigate (classic token page), what to select (Generate new token (classic)), what to check (repo scope), and what it means (read access to private repos).

Residual deductions:
- Windows ssh-agent passphrase persistence is undocumented. A Windows user who set a passphrase will be prompted on every `git` command — a friction point that macOS users are now protected from. (-0.04)
- PAT clone URL (line 261) is macOS-only path format. A Windows user using PAT authentication would need to adapt the path manually without guidance. (-0.03)

### Traceability (weight: 0.10)

**Score: 0.95**

The change summary comment at the top of the draft file has been updated for iteration 2. It accurately enumerates all 7 issues from iteration 1 (MAJOR-001, MAJOR-002, MINOR-001 through MINOR-005) and documents the specific fix applied for each. The traceability chain from issue to fix is explicit.

The EN-940 and EN-941 traceability from iteration 1 is preserved. The workflow ID is present in the comment header. The reviewer attribution (ps-critic-001, score 0.866) is included in the iteration 2 comment block, which enables future traceability from the revision back to the issuing review.

Minor deduction: The iteration 1 change summary note at the top of the comment does not reference the specific file path of the review document that issued the issues (ps-critic-001-installation-review.md). A reader of the draft comment alone cannot locate the issuing review without knowing the workflow structure. (-0.05)

---

## Weighted Composite Score

| Dimension | Weight | Raw Score | Weighted |
|-----------|--------|-----------|---------|
| Completeness | 0.20 | 0.93 | 0.186 |
| Internal Consistency | 0.20 | 0.95 | 0.190 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.91 | 0.137 |
| Actionability | 0.15 | 0.93 | 0.140 |
| Traceability | 0.10 | 0.95 | 0.095 |
| **TOTAL** | **1.00** | | **0.934** |

**Weighted Composite: 0.934**

Band: **PASS** (>= 0.92 threshold per H-13)

---

## Residual Issues Found

### CRITICAL (0 found)

No critical issues. No existing content was broken, removed, or corrupted. All new content is technically accurate.

---

### MAJOR (0 found)

Both iteration 1 MAJOR issues are fully resolved. No new MAJOR issues introduced.

---

### MINOR

#### MINOR-R01: Windows SSH Agent Passphrase Persistence Not Documented

**Severity:** MINOR
**Location:** Windows SSH key generation section (Step 1 under Collaborator Installation)
**Dimension Affected:** Completeness, Methodological Rigor, Actionability
**Status:** Residual (not in iteration 1 scope — was partially covered by MINOR-003 which specified macOS only)

The macOS Keychain tip (MINOR-003) creates a platform parity gap. macOS users with a passphrase-protected key now have guidance to avoid repeated passphrase prompts. Windows users with a passphrase receive no equivalent guidance. On Windows, the OpenSSH agent (available since Windows 10 1803) requires:

```powershell
# Start the ssh-agent service (run once, requires admin or set to automatic)
Start-Service ssh-agent

# Add your key to the agent (per session, or configure auto-add)
ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
```

Without this, a Windows user who chose a passphrase will be prompted on every `git clone`, `git pull`, and `git push`. This is a concrete and predictable friction point.

**Recommended fix:** Add a brief Windows callout after the Windows SSH key generation display step, analogous to the macOS Keychain tip: "If you set a passphrase and wish to avoid re-entering it each session, start the SSH agent: `Start-Service ssh-agent` then `ssh-add $env:USERPROFILE\.ssh\id_ed25519`."

**Threshold impact:** This issue does not block the PASS verdict. It is noted for the next content improvement cycle.

---

#### MINOR-R02: PAT Alternative Clone URL Uses macOS Path Format Only

**Severity:** MINOR
**Location:** Draft line 261 — PAT Alternative subsection, step 3
**Dimension Affected:** Actionability
**Status:** Pre-existing (not introduced by either iteration)

The PAT Alternative step 3 shows:
```
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

The `~/plugins/jerry` path is macOS/Linux syntax. A Windows user reading only the PAT section would need to substitute the correct PowerShell path (`"$env:USERPROFILE\plugins\jerry"`) without guidance. Both platform variants should be shown, consistent with how the SSH clone step (Step 4 of Collaborator Installation) handles platform split.

**Recommended fix:** Add the Windows equivalent:
```powershell
# Windows PowerShell
git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
```

**Threshold impact:** This issue does not block the PASS verdict. It is noted for the next content improvement cycle.

---

## Verdict

**PASS**

**Score: 0.934 — above the 0.92 threshold required by H-13 for C2+ deliverables.**

The revision pass by ps-architect-001 is thorough and precise. All 7 issues from iteration 1 were addressed with targeted fixes that do not introduce new defects. The two MAJOR structural issues (anchor fragility and step numbering discontinuity) have been cleanly resolved using the recommended approaches from the iteration 1 review. All 5 MINOR issues were also addressed, including the macOS Keychain tip that was marked optional in the iteration 1 recommendations.

The document now has:
- Stable, renderer-independent anchor IDs for cross-section navigation
- A coherent collaborator installation flow with no dual-numbering confusion
- Past-tense collaborator notes that guide rather than redirect
- Consistent placeholder naming throughout
- Properly scoped PAT instructions with access-level explanation
- Section-level references in the Future section

The two residual MINOR issues (Windows ssh-agent gap, PAT Windows path) are pre-existing or out-of-iteration-1 scope. Neither is threshold-blocking. Both should be addressed in a subsequent content improvement pass before the document is applied to `docs/INSTALLATION.md`.

**The draft is approved for application to `docs/INSTALLATION.md` after stripping the change summary comment block.**

---

*Agent: ps-critic-001*
*Workflow: epic001-docs-20260218-001*
*Phase: 2*
*Iteration: 2*
*Output: `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-critic-001/ps-critic-001-installation-review-iter2.md`*

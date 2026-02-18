# Quality Score Report: Jerry Framework Installation Guide

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, and plain-language assessment |
| [Scoring Context](#scoring-context) | Deliverable metadata and strategy reference |
| [Score Summary](#score-summary) | Composite score and threshold comparison |
| [Dimension Scores](#dimension-scores) | Weighted score table across all 6 dimensions |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, and improvement paths |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered action items |
| [Leniency Bias Check](#leniency-bias-check) | Self-review checklist |

---

## L0 Executive Summary

**Score:** 0.8470/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.83), Methodological Rigor (0.83), Actionability (0.83) (tied)

**One-line assessment:** Iteration 4 resolves all 7 prior retry-1 findings with precise, well-executed fixes, but 2 new Devil's Advocate Majors — ssh-keygen unavailability on Windows Home/LTSC before any diagnosis, and an undocumented passphrase prompt at the verification step for users following the document's own recommendation — prevent the document from reaching the 0.92 threshold; both Majors require targeted additions of 2–4 lines each and the guide is otherwise production-quality.

---

## Scoring Context

| Field | Value |
|-------|-------|
| **Deliverable** | `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md` |
| **Deliverable Type** | Documentation (Installation Guide) |
| **Criticality Level** | C2 |
| **Scoring Strategy** | S-014 (LLM-as-Judge) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Scored** | 2026-02-18T00:00:00Z |
| **Iteration** | 3 (QG-1 Initial 0.7665 → QG-1 Retry 1 0.8300 → QG-1 Retry 2 this report) |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.8470 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 3 reports (S-003: 0 Major, 3 Minor; S-002: 2 Major, 2 Minor; S-007: 0 Major, 0 Minor) |
| **Prior Score (QG-1 Retry 1)** | 0.8300 |
| **Score Delta** | +0.0170 |

**Operational Band:** REVISE (0.85–0.91 boundary: score 0.8470 falls in the 0.70–0.84 band — significant gaps, focused revision needed per adv-scorer verdict table)

> **Clarification note:** The score 0.8470 falls in the 0.70–0.84 REVISE band. The 2 remaining Majors are targeted and addressable with small additions (2–4 lines each). This is not a structural rework situation; it is a focused-revision situation.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.83 | 0.1660 | All 4 AC satisfied; 2 Major gaps remain (ssh-keygen Windows, passphrase prompt at verification) |
| Internal Consistency | 0.20 | 0.84 | 0.1680 | 7 prior inconsistencies resolved; DA-001 ordering (command before its prereq check) and $env:USERPROFILE vs literal path gap remain |
| Methodological Rigor | 0.20 | 0.83 | 0.1660 | Diagnostic pre-checks added throughout; ssh-keygen check incomplete (addressed ssh-agent only); verification step incomplete for recommended configuration |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | 4 factual claims verified against repo; strong grounding; ssh-keygen fix described as resolved when it is not for the keygen command itself |
| Actionability | 0.15 | 0.83 | 0.1245 | Configuration-before-Verification reordering is a major win; 2 Majors both produce dead-ends where users cannot proceed without deducing the path |
| Traceability | 0.10 | 0.92 | 0.0920 | 4-iteration change summary complete; all priority findings traced; anchor links verified against headings; AC-1 through AC-4 confirmed |
| **TOTAL** | **1.00** | | **0.8470** | |

---

## Detailed Dimension Analysis

### Completeness (0.83/1.00)

**Evidence:**

The document covers all four acceptance criteria (AC-1 through AC-4) across 12 Table of Contents sections. The collaborator SSH path (AC-2) includes dual-platform key generation, agent setup, clone, and handoff to the platform-specific steps. The future public path (AC-3) is clearly framed, complete with a comparison table and a detection mechanism. The archive/marketplace installation (AC-1) remains intact, and all existing content is preserved (AC-4). Troubleshooting covers 8 named scenarios with symptoms and numbered solutions. The steelman confirms: "All four acceptance criteria remain satisfied."

**Gaps:**

- **DA-001-qg1r2-da (Major):** The Windows Step 1 section uses `ssh-keygen` at line 285 without first verifying that OpenSSH Client (which provides `ssh-keygen`) is installed. The OpenSSH Client check added in Iteration 4 (P3-DA-002 retry-1) applies only to the ssh-agent Tip block, which is framed as optional passphrase caching. A Windows Home/LTSC user who runs `ssh-keygen` without OpenSSH Client receives `The term 'ssh-keygen' is not recognized` with no recovery path at that point in the document. The Tip block containing the diagnosis is not reachable from the point of failure because it is framed as an optional step for passphrase users.
- **DA-002-qg1r2-da (Major):** The ssh -T verification step (Step 3, lines 334–346) shows only the success output. A user who followed the document's recommendation to set a passphrase ("Enter a passphrase (recommended)") and did not run the optional Keychain/agent Tip will encounter a passphrase prompt before the success message. The prompt is not documented. The SSH Authentication Failed troubleshooting entry does not list "passphrase not entered" as a cause. This creates a false failure perception for the majority of users following the guide's own recommendation.
- **SM-002-qg1r2s (Minor):** The Verification section "Test a Skill" step uses `/problem-solving` as the success indicator but the optional project setup was not performed. Users who skipped the optional Configuration step will see the `<project-required>` prompt, not the expected skill activation response.
- **SM-003-qg1r2s (Minor):** PAT clone block (lines 391–399) does not include the space-in-path warning present in the SSH clone block (line 354).
- **DA-003-qg1r2-da (Minor):** Future section Step 2 clone block (lines 613–625) omits the space-in-path warning.

**Improvement Path:** Add ssh-keygen availability pre-check before the Windows Step 1 ssh-keygen command. Add a passphrase prompt note after the "You should see:" block in Step 3, and add a passphrase cause to the SSH Authentication Failed troubleshooting entry. These two additions close both Majors. Optionally replace `/problem-solving` in the Verification step with a project-independent command (`/help` or `/plugin`).

---

### Internal Consistency (0.84/1.00)

**Evidence:**

The document resolves all 7 prior retry-1 inconsistencies with precise fixes: Configuration precedes Verification in both ToC and body; the marketplace rationale sentence now reads "during `/plugin install`" (not during marketplace-add); the ToC column header reads "Purpose" (not "Description"); PAT Step 3 shows both macOS/Git Bash and Windows PowerShell variants; PAT `repo` scope is correctly described as "full access (read and write)"; osxkeychain pre-check with store fallback is symmetric with the Windows credential helper. Cross-platform parity is verified by the steelman: every SSH step, every clone step, every credential step has both platform variants. Anchor IDs are stable HTML IDs verified by the constitutional reviewer.

**Gaps:**

- **DA-001-qg1r2-da structural ordering (Major context):** The Windows Step 1 section runs `ssh-keygen` (line 285) before the Tip block (lines 302–317) that contains the OpenSSH Client install guidance. The Tip is framed as optional ("to avoid re-entering your passphrase each session") rather than as a prerequisite check for `ssh-keygen` itself. This creates a structural inconsistency: the fix for the OpenSSH dependency is positioned after the command that depends on it.
- **DA-004-qg1r2-da (Minor):** Windows Step 2 uses `"$env:USERPROFILE\plugins\jerry"` as the clone destination. Windows Step 4 requires a literal path `C:/Users/YOUR_USERNAME/plugins/jerry`. The bridging guidance ("run `echo $env:USERNAME`") diverges from `$env:USERPROFILE` semantics on domain-joined machines and redirected profile paths, creating an inconsistency between what Step 2 taught and what Step 4 requires.
- **SM-001-qg1r2s (Minor):** The Configuration scope recommendation ("Use **Project** scope when you want your whole team to have Jerry available") is stated without explaining the operational consequence (plugin entry added to `.claude/settings.json`, committed to version control), making it incomplete relative to the User scope guidance which is fully self-explanatory.

**Improvement Path:** Reposition the OpenSSH Client pre-check to the top of the Windows Step 1 section (before `ssh-keygen`) or add a prerequisite check inline. Replace the `echo $env:USERNAME` tip in Step 4 with `(Get-Item "$env:USERPROFILE\plugins\jerry").FullName` to produce the exact literal string needed.

---

### Methodological Rigor (0.83/1.00)

**Evidence:**

The document follows a sound progressive-disclosure methodology: Prerequisites → Collaborator Installation (auth) → Installation (platform-specific) → Future (not-yet-applicable) → Configuration → Verification → Using Jerry → Troubleshooting → For Developers → Uninstallation → Getting Help → License. Every major step provides platform variants. Diagnostic pre-checks are present for: ssh-keygen key existence (both platforms), osxkeychain availability (macOS PAT), OpenSSH Client for ssh-agent (Windows), uv installation (both platforms), and plugin manifest existence. Space-in-path warnings appear at three of four clone locations. The Windows SSH agent Tip now uses a conditional `if/else` guard instead of a blind `Start-Service` command.

**Gaps:**

- **DA-001-qg1r2-da (Major):** The prior fix applied an OpenSSH Client availability check to the SSH agent context, but the same dependency applies to `ssh-keygen` itself. The fix was incomplete: the diagnostic pre-check pattern was applied downstream (agent) but not upstream (keygen). This is a methodological gap in the applied fix logic — the same tool (`Get-Command ssh-keygen -ErrorAction SilentlyContinue`) used for the agent check was not applied at the actual point of failure.
- **DA-002-qg1r2-da (Major):** The verification methodology presents the success case of `ssh -T` without accounting for the expected interactive prompt that precedes it for users with passphrases. A rigorous verification methodology must document all expected outputs, including intermediate prompts, not just the terminal success message. The document's own recommendation ("Enter a passphrase (recommended)") makes the passphrase case the majority case.
- **SM-003-qg1r2s (Minor):** The space-in-path warning methodology is applied to 3 of 4 clone locations but missing from the PAT Alternative block (lines 391–399). The methodological pattern is correct but incompletely applied.

**Improvement Path:** Apply the pre-check pattern consistently: add `Get-Command ssh-keygen -ErrorAction SilentlyContinue` guard before the Windows Step 1 keygen command. Document the passphrase prompt in the Step 3 verification flow. Add space-in-path warning to the PAT clone block.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

The S-007 constitutional review verified four factual claims against actual repository state: `plugin.json` name field is "jerry-framework" (confirmed); BOOTSTRAP.md exists in `docs/`; CONTRIBUTING.md exists at repo root; LICENSE is Apache 2.0. All four verified correct. The PAT `repo` scope description was corrected from "read access" to "full access (read and write)" with a fine-grained PAT alternative specified for least-privilege. The rate-limit note in the Future section is consistent with known GitHub behavior. The detection mechanism ("visit github.com/geekatron/jerry while logged out") is operationally accurate. The change summary traces all priority findings across 4 iterations with precise line references. The steelman confirms that all 10 priority fixes are correctly applied with verifiable evidence.

**Gaps:**

- **DA-001-qg1r2-da (evidence implication):** The Iteration 3 change summary (P8-SM-004) described adding a Windows SSH agent tip including OpenSSH Client pre-check. This was correctly applied for ssh-agent. However, the claim that OpenSSH dependency is now fully handled is implicitly incomplete — `ssh-keygen` shares the same dependency. The evidence base for the fix does not cover the full scope of the dependency.
- **CC-002 (Advisory, not scored against guide):** `plugin.json` contains `"license": "MIT"` while the root LICENSE file is Apache 2.0. The guide correctly references the LICENSE file; this is a pre-existing repository inconsistency. Noted for repo hygiene, not scored against the installation guide.
- The SSH clone URL (`git@github.com:geekatron/jerry.git`) and plugin install command (`/plugin install jerry-framework@jerry`) are accepted as accurate from prior rounds but were not independently verified in this round by the constitutional reviewer.

**Improvement Path:** The evidence quality is strong. No targeted improvements are required for this dimension beyond those that follow from fixing the Major findings.

---

### Actionability (0.83/1.00)

**Evidence:**

The Configuration-before-Verification reordering (P1) is the most impactful actionability improvement in the entire 4-iteration history — it eliminates a guaranteed first-run failure where every new user would encounter the `<project-required>` prompt at the skill verification step before having set `JERRY_PROJECT`. The Windows SSH agent conditional block provides a clear install path when OpenSSH Client is absent. The osxkeychain pre-check provides a concrete decision tree (use osxkeychain or use store) rather than a blind command. Troubleshooting entries have named Symptoms and numbered Solutions. The PAT flow provides both a classic and fine-grained option with explicit security tradeoffs. The collaborator "Next Steps" section explicitly links to stable anchors (#macos-step-3, #windows-step-3) for the convergence path.

**Gaps:**

- **DA-001-qg1r2-da (Major):** A Windows Home/LTSC user reaches Step 1 and runs `ssh-keygen`. The command fails with an unrecognized cmdlet error. The document provides no recovery path at that point. The Tip block (lines 302–317) containing the diagnosis is framed as an optional passphrase-caching step; the user has no signal that it contains the solution to their keygen failure. This is a dead-end actionability failure for a defined user population.
- **DA-002-qg1r2-da (Major):** A user with a passphrase runs `ssh -T git@github.com`. They see a passphrase prompt not mentioned in the document. If they press Enter (most intuitive response for a confirmation step), they receive `Permission denied (publickey)`. The troubleshooting entry for SSH Authentication Failed does not list "passphrase not entered" as a cause, so the user is directed toward the wrong diagnosis (re-verify public key on GitHub). This is a misdirection actionability failure.
- **SM-002-qg1r2s (Minor):** A user who skipped optional project setup runs `/problem-solving` for verification and sees `<project-required>` instead of skill activation. The failure mode is not documented at the Verification step.

**Improvement Path:** Add 2–4 lines at the point of ssh-keygen (Windows) to check for OpenSSH Client availability. Add a note at the Step 3 "You should see:" block explaining the passphrase prompt for users who set a passphrase. Add a passphrase cause to the SSH Authentication Failed troubleshooting entry. Consider replacing `/problem-solving` in the Verification step with `/plugin` (project-independent).

---

### Traceability (0.92/1.00)

**Evidence:**

The change summary embedded in the draft file header documents all 4 iterations with explicit priority finding IDs (P1–P10), source findings (DA-NNN, SM-NNN, CC-NNN from prior score reports), and line-level references for each applied fix. The Iteration 4 summary traces all 10 priority findings from the QG-1 Retry 1 score report plus 2 additional fixes. The S-003 steelman verified prior finding resolution with specific line number evidence for all 5 prior steelman findings. The S-002 DA verified all 7 prior DA findings against the document body with specific line references. The S-007 constitutional check verified anchor links against headings (7 spot-checked), verified 4 factual claims against repo state, and confirmed the NAV-003 column header fix. Acceptance criteria (AC-1 through AC-4) are traced in the change summary and confirmed by the steelman. The SSOT reference (`.context/rules/quality-enforcement.md`) is explicit throughout all review documents.

**Gaps:**

- No major traceability gaps were identified by any of the three strategy reviewers. The Traceability dimension is the strongest dimension across this entire scoring cycle.
- SM-001-qg1r2s (Minor): SM-005-qg1r1s was carried forward as unresolved but this is explicit in the steelman and correctly traced. The open status is acknowledged, not hidden.

**Improvement Path:** Traceability is at the quality gate threshold. No targeted improvements required for this dimension.

---

## Improvement Recommendations

| Priority | Finding | Dimension Impact | Current | Target | Recommendation |
|----------|---------|-----------------|---------|--------|----------------|
| 1 | DA-001-qg1r2-da (Major) | Completeness, Methodological Rigor, Actionability | 0.83 | 0.88+ | Add `Get-Command ssh-keygen -ErrorAction SilentlyContinue` guard before Windows Step 1 ssh-keygen command, with inline install guidance (Settings > Apps path and Add-WindowsCapability). 3–5 lines. Mirrors the exact pattern already applied for ssh-agent. |
| 2 | DA-002-qg1r2-da (Major) | Completeness, Methodological Rigor, Actionability | 0.83 | 0.88+ | Add note after the "You should see:" block in Step 3: "If you set a passphrase and did not run the Keychain/agent Tip, you will see a passphrase prompt first — enter your passphrase and press Enter." Also add a passphrase cause to the SSH Authentication Failed troubleshooting entry. 3–4 lines total. |
| 3 | DA-004-qg1r2-da (Minor) | Internal Consistency | 0.84 | 0.88+ | Replace the `echo $env:USERNAME` tip in Windows Step 4 with `(Get-Item "$env:USERPROFILE\plugins\jerry").FullName` to produce the exact forward-slash path for Claude Code. Eliminates the $env:USERPROFILE vs literal path inconsistency. |
| 4 | SM-002-qg1r2s (Minor) | Completeness, Actionability | 0.83 | 0.88+ | Replace `/problem-solving` in the Verification "Test a Skill" step with `/help` or `/plugin` (both project-independent). Alternatively, add a note that `/problem-solving` requires JERRY_PROJECT to be set per the Configuration section above. |
| 5 | DA-003-qg1r2-da (Minor) | Completeness, Methodological Rigor | 0.83 | 0.87+ | Add space-in-path Important callout to Future section Step 2 clone block. 2 lines. |
| 6 | SM-003-qg1r2s (Minor) | Methodological Rigor | 0.83 | 0.86+ | Add space-in-path warning to PAT Alternative clone block (lines 391–399). 2 lines to complete the pattern applied at all other clone locations. |
| 7 | SM-001-qg1r2s (Minor) | Internal Consistency | 0.84 | 0.86+ | Expand the Project scope recommendation to state the operational consequence: "Jerry is added to `.claude/settings.json`, which is committed to version control — new team members have Jerry active after cloning the repository." |

**Assessment:** Priority 1 and 2 fixes are required to reach the 0.92 threshold. They are both targeted, small (2–5 lines each), and do not require structural changes. The document is otherwise well-constructed and the 7 prior retry-1 findings are all correctly resolved. A Retry 3 pass applying Priority 1 and 2 at minimum is recommended.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite
- [x] Evidence documented for each score with specific line references and finding IDs
- [x] Uncertain scores resolved downward — Completeness, Methodological Rigor, and Actionability all at 0.83 despite overall structural strength, because the 2 Majors are real failure points for defined user populations, not edge cases
- [x] First-draft calibration considered — this is Iteration 4 post-adversarial remediation; the calibration anchor "0.85 = strong work with minor refinements needed" informed the choice to place the Major-affected dimensions at 0.83 rather than 0.85, because the 2 Majors are more than minor refinements for affected users
- [x] No dimension scored above 0.95 without exceptional evidence — Traceability at 0.92 is justified by verified anchor checks, 4-iteration change summary, and constitutional review confirming all claims; no dimension above 0.92
- [x] Score delta from prior (+0.0170) is modest and consistent with resolving 7 prior Majors while gaining 2 new Majors — the net improvement is real but bounded
- [x] DA-002 passphrase issue scrutinized for severity inflation: confirmed Major, not Minor, because the document actively recommends passphrases ("Enter a passphrase (recommended)"), making the undocumented prompt the expected experience for the majority of compliant users, not an edge case
- [x] Composite math verified: 0.83×0.20 + 0.84×0.20 + 0.83×0.20 + 0.87×0.15 + 0.83×0.15 + 0.92×0.10 = 0.166 + 0.168 + 0.166 + 0.1305 + 0.1245 + 0.092 = 0.8470

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.8470
threshold: 0.92
weakest_dimension: Completeness  # tied with Methodological Rigor and Actionability at 0.83
weakest_score: 0.83
critical_findings_count: 0
major_findings_count: 2  # DA-001-qg1r2-da, DA-002-qg1r2-da
iteration: 3  # QG-1 Initial, QG-1 Retry 1, QG-1 Retry 2 (this report)
score_delta: +0.0170  # from 0.8300
improvement_recommendations:
  - "Add ssh-keygen availability pre-check before Windows Step 1 keygen command (DA-001-qg1r2-da — Major)"
  - "Document passphrase prompt in Step 3 ssh -T verification and add to SSH troubleshooting (DA-002-qg1r2-da — Major)"
  - "Replace $env:USERNAME tip in Windows Step 4 with exact path command (DA-004-qg1r2-da — Minor)"
  - "Replace /problem-solving verification command with project-independent command or add JERRY_PROJECT note (SM-002-qg1r2s — Minor)"
  - "Add space-in-path warning to Future section Step 2 clone block (DA-003-qg1r2-da — Minor)"
  - "Add space-in-path warning to PAT Alternative clone block (SM-003-qg1r2s — Minor)"
  - "Expand Project scope operational consequence in Configuration (SM-001-qg1r2s — Minor)"
```

---

*Scored by: adv-scorer-001*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: epic001-docs-20260218-001 | QG-1 Retry 2*
*Date: 2026-02-18*

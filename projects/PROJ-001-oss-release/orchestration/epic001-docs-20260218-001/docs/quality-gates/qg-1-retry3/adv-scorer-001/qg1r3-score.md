# S-014 LLM-as-Judge Score Report — QG-1 Retry 3

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Score, verdict, delta, and rationale |
| [Dimension Scores](#dimension-scores) | Weighted composite score table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence and finding impact |
| [Strategy Finding Impact](#strategy-finding-impact) | How the 0 Major + 7 Minor findings affected scoring |
| [Score Trajectory](#score-trajectory) | Round-by-round progression |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered action list |
| [Self-Review Verification](#self-review-verification) | H-15 leniency bias checklist |

---

## L0 Summary

**Score: 0.9100 | Verdict: REVISE | Delta: +0.0630 from Retry 2 (0.8470)**

The document achieves 0 Major findings for the first time in the QG-1 history — a genuine milestone — but falls 0.0100 short of the 0.92 PASS threshold due to a cluster of 7 Minor findings that collectively suppress four dimensions to 0.91 and one dimension to 0.90; the single largest gap is the absence of a Troubleshooting entry for `<project-required>` / `<project-error>`, which is the expected first-run output for any user who skips or misconfigures the JERRY_PROJECT setup step.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.1800 | Both Majors resolved; 2 distinct Minor gaps remain: uv version floor absent, no Troubleshooting entry for `<project-required>` scenario (raised by both SM-003-qg1r3 and DA-003-qg1r3) |
| Internal Consistency | 0.20 | 0.91 | 0.1820 | 12/12 ToC anchors verified correct; no contradictions found; minor gap: `@jerry` marketplace suffix not tied back to Step 4 directory name, creating an unstated dependency; PROJ-001 example naming overlap |
| Methodological Rigor | 0.20 | 0.91 | 0.1820 | Both prior Majors resolved with correctly placed fixes; two new Minors: `Set-Service -StartupType Automatic` requires admin (undocumented), `--apple-use-keychain` has undocumented macOS version constraint |
| Evidence Quality | 0.15 | 0.91 | 0.1365 | All 4 S-007 factual claims verified; no new inaccuracies; minor gap: `--apple-use-keychain` presented without Ventura 13+ qualifier, making it technically inaccurate for Monterey users |
| Actionability | 0.15 | 0.91 | 0.1365 | Major dead-ends eliminated; two remaining Minor actionability gaps: `<project-required>` output not explained in Verification, `@jerry` suffix provides no recovery path when directory name differs |
| Traceability | 0.10 | 0.93 | 0.0930 | 12/12 heading coverage; 7 Iteration 5 fixes traced with explicit finding IDs; all prior findings verified resolved by DA and Steelman with specific line references; Advisory only (pre-existing plugin.json license field) |
| **Weighted Composite** | **1.00** | — | **0.9100** | — |

**Composite calculation:** 0.90×0.20 + 0.91×0.20 + 0.91×0.20 + 0.91×0.15 + 0.91×0.15 + 0.93×0.10
= 0.1800 + 0.1820 + 0.1820 + 0.1365 + 0.1365 + 0.0930
= **0.9100**

**Threshold:** 0.92 (H-13). **Verdict: REVISE** (0.9100 < 0.92).

---

## Detailed Dimension Analysis

### Completeness (0.90 / 1.00)

**Improvement from Retry 2 (0.83):** The two Major completeness gaps are fully resolved. DA-001-qg1r2-da (ssh-keygen Windows pre-check) is confirmed present at lines 320-325 — a correctly-positioned Important callout appears before the ssh-keygen command on Windows, covering the exact failure mode with both Settings UI and PowerShell install paths. DA-002-qg1r2-da (passphrase prompt at ssh -T) is confirmed present at line 389 — the note appears between the command and the success block, explains the prompt, instructs the user to type their passphrase, and provides a recovery path for post-passphrase failure. Both Minors from Retry 2 (SM-003-qg1r2s space-in-path PAT Alternative, DA-003-qg1r2-da space-in-path Future section) are confirmed resolved.

**Remaining gaps:**
- SM-001-qg1r3 (Minor): uv is the only tool in the Prerequisites table without a version floor — listed as "Latest" while Git shows "2.0+" and Claude Code shows "1.0.33+". This is a factual gap: no minimum requirement is communicated for a dependency that does have version-relevant behavior.
- SM-003-qg1r3 / DA-003-qg1r3 (Minor, double-flagged): No Troubleshooting entry exists for `<project-required>` or `<project-error>` session start tags. The Verification section's Note directs users to `/help` if JERRY_PROJECT is not set, but a user who configured JERRY_PROJECT incorrectly (typo, wrong format, non-existent directory) will see these tags and have no Troubleshooting entry to consult. This scenario is the documented first-run behavior of the SessionStart hook. Its absence from Troubleshooting is a real gap, not pure polish — the `<project-required>` tag is opaque XML output that new users cannot interpret without guidance.

**Scoring rationale:** The calibration anchor for 0.90-0.94 is "0 Major, 2-4 Minor (polish only), ready with minor polish." The `<project-required>` gap is borderline between polish and substantive — it does not block the core install path, but it produces a confusing output at the exact point where a user validates their installation. Score 0.90 reflects the lower bound of the 0.90-0.94 anchor range, consistent with two real (if minor) content gaps.

---

### Internal Consistency (0.91 / 1.00)

**Improvement from Retry 2 (0.84):** All prior inconsistencies are resolved. DA-004-qg1r2-da ($env:USERNAME vs literal path) is fixed — the PowerShell path utility at lines 637-640 now produces the exact forward-slash path that Claude Code requires, eliminating the Step 2 / Step 4 mismatch. SM-001-qg1r2s (Configuration scope missing operational consequence) is fixed — line 706 now states "Jerry is added to `.claude/settings.json`, which is committed to version control — new team members have Jerry active automatically after cloning the repository." Constitutional review confirms: 12/12 ToC anchors verified against headings using the correct lowercasing and hyphenation rules, 12/12 major `##` sections covered in ToC, NAV-003 column header correctly reads "Purpose."

**Remaining gaps:**
- DA-004-qg1r3-da (Minor): Step 4 runs `/plugin marketplace add ~/plugins/jerry` — Claude Code derives the marketplace identifier from the terminal path segment (`jerry`). Step 5 runs `/plugin install jerry-framework@jerry`. The `@jerry` suffix is never explained as a reference to the Step 4 directory name. A user who cloned to a non-standard directory (e.g., `~/projects/jerry-framework`) will have marketplace identifier `jerry-framework`, and the Step 5 command will fail silently with "plugin not found." Steps 4 and 5 are not contradictory, but the unstated dependency between the directory name in Step 4 and the `@` suffix in Step 5 is a consistency gap: the document establishes a naming convention without explaining it.
- SM-002-qg1r3 (Minor): The Configuration Project Setup step uses `PROJ-001-my-project` as the example project name — four occurrences (two env var lines, two directory creation lines). This collides with the Jerry repository's own PROJ-001 project. A user reading the guide while inside the Jerry repository could create a directory that collides with or appears to duplicate the actual PROJ-001 project tracking. This is a presentation-level inconsistency between the guide's example namespace and the repository's live namespace.

**Leniency application:** I was uncertain between 0.91 and 0.92. The document has genuinely excellent reference integrity — no actual contradictions, all anchors verified, all cross-platform parity maintained. However, the @jerry relationship is an unstated dependency that creates a real failure path, and the leniency rule requires choosing the lower score under uncertainty. Score: **0.91**.

---

### Methodological Rigor (0.91 / 1.00)

**Improvement from Retry 2 (0.83):** Both Major methodology gaps are resolved. The OpenSSH Client pre-check for ssh-keygen is now positioned correctly: lines 320-325 place the Important callout before the `ssh-keygen` command on Windows, not just in the optional agent Tip block. The passphrase methodology is now complete: the document documents both the generation-time passphrase recommendation and the verification-time passphrase prompt, with the note appearing at the exact friction point between the `ssh -T` command and the success output. The space-in-path warning methodology is now consistently applied at all four clone locations (SSH clone, macOS HTTPS, Windows HTTPS, PAT Alternative, Future section — confirmed by DA prior findings verification).

**Remaining gaps:**
- DA-001-qg1r3-da (Minor): The Windows SSH agent Tip includes `Set-Service -Name ssh-agent -StartupType Automatic` (line 353-354) without stating that this command requires an elevated (Administrator) PowerShell session. `Set-Service` with `-StartupType Automatic` will fail silently or throw "Access is denied" in a standard user-privilege session. The guide presents this as a routine follow-on step. The failure mode is subtle: `ssh-add` may succeed (if the service was already running), but `Set-Service` silently fails, leaving the user without persistent agent startup. On the next session, the user wonders why they must re-enter their passphrase. Note: `Start-Service ssh-agent` on the preceding line also typically requires elevation.
- DA-002-qg1r3-da (Minor): The `--apple-use-keychain` flag in the macOS Keychain Tip (lines 303-305) is an Apple-specific ssh-add extension added in macOS Ventura (13). The guide makes no mention of a macOS version requirement for this Tip. On macOS Monterey (12) and earlier, the flag does not exist — the command produces `ssh-add: illegal option -- -`. The user receives an error with no fallback guidance. The document's own `--apple-use-keychain` invocation is methodologically unsound for the Monterey user population without a version qualifier or `-K` fallback.

**Scoring rationale:** With both Majors resolved, the methodology is sound on the primary paths. The two remaining Minor gaps both relate to optional/tip-level guidance, not core install steps. However, both gaps have real failure modes for identifiable user populations (non-admin Windows users, Monterey users), making them more than pure polish. Score 0.91.

---

### Evidence Quality (0.91 / 1.00)

**Improvement from Retry 2 (0.87):** No new evidence quality issues were introduced by Iteration 5. S-007 constitutional review independently verified all repository-checkable claims: `plugin.json` name field is "jerry-framework" (line 537 and 624 confirmed), bootstrap script path exists (`scripts/bootstrap_context.py`), BOOTSTRAP.md exists in `docs/`, CONTRIBUTING.md exists at repo root, and the License section correctly cites Apache 2.0. All PAT scope descriptions, credential helper guidance, and pre-check commands from prior revisions remain accurate. The osxkeychain pre-check (`git credential-osxkeychain 2>&1 | head -1`) is a valid diagnostic. The Windows PowerShell path utility (`(Get-Item "$env:USERPROFILE\plugins\jerry").FullName -replace '\\','/'`) is correct.

**Remaining gaps:**
- DA-002-qg1r3-da (evidence dimension): The `--apple-use-keychain` flag is presented without a macOS version qualifier. This makes the command technically inaccurate for macOS Monterey (12) and earlier users — the flag does not exist on those platforms. The claim implicit in the Tip is "run `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` to cache your passphrase in the macOS Keychain" — this claim is false for a non-trivial segment of macOS users still on Monterey. Enterprise environments frequently delay major macOS upgrades.
- Pre-existing Advisory: `plugin.json` line 9 carries `"license": "MIT"` while the root LICENSE file is Apache 2.0. The deliverable itself correctly references Apache 2.0 — this is a repository-level inconsistency, not a deliverable error. Not scored against the guide.

**Scoring rationale:** The evidence base is strong and independently verified. The single accuracy gap (`--apple-use-keychain` version constraint) is real but scoped to an optional Tip. Score 0.91 — improved from 0.87, but the version claim prevents reaching 0.93+.

---

### Actionability (0.91 / 1.00)

**Improvement from Retry 2 (0.83):** The two Major actionability dead-ends are eliminated. Windows Home/LTSC users who run `ssh-keygen` without OpenSSH Client now encounter the Important callout at lines 320-325 before the failing command, with two install paths. Users who followed the passphrase recommendation now see the passphrase prompt explained at line 389 between the `ssh -T` command and the success block, with explicit instruction to type their passphrase and press Enter. The troubleshooting entry for SSH Authentication Failed now lists "passphrase not entered" as an explicit cause (lines 880-881).

**Remaining gaps:**
- DA-003-qg1r3-da / SM-003-qg1r3 (Minor): The Verification section's "Test a Skill" step recommends `/problem-solving` and notes that it requires `JERRY_PROJECT`. However, the note does not describe what output the user will see if `JERRY_PROJECT` is not set (the `<project-required>` XML-tagged response). A user who configured `JERRY_PROJECT` but made a typo, or who does not recognize the XML output, has no guidance. The Troubleshooting section has no entry for this scenario. The actionability gap is real: the user cannot distinguish "installation failure" from "expected behavior when project is not configured" based on the current guidance.
- DA-004-qg1r3-da (Minor): `/plugin install jerry-framework@jerry` at Step 5 uses `@jerry` without explaining that `jerry` is the marketplace identifier derived from the directory name used in Step 4. If the user cloned to any path other than `*/jerry`, this command fails. The Troubleshooting entry for "Plugin Not Found After Adding Marketplace" covers 4 solutions but none addresses directory-name mismatch as the cause. A user who cloned to `~/projects/jerry-framework` has no recovery path visible from Step 5 or from Troubleshooting.

**Scoring rationale:** The two Major actionability failures being resolved dramatically improves this dimension. The remaining Minor gaps create UX friction for specific edge cases (misconfigured JERRY_PROJECT, non-standard clone paths) but do not constitute dead-ends on the primary recommended paths. Score 0.91.

---

### Traceability (0.93 / 1.00)

**Improvement from Retry 2 (0.92):** The Iteration 5 change summary in the file header (lines 169-204) traces all 7 targeted fixes with explicit finding IDs (P1-DA-001-qg1r2-da through P7-SM-001-qg1r2s). Each fix cites the source finding, severity, and describes the change applied. S-003 Steelman verified resolution of all 7 prior findings with specific line references in the current document. S-002 Devil's Advocate verified resolution of all 4 prior DA findings with specific line references. S-007 Constitutional review verified all 12 ToC anchor links against their target headings and confirmed 12/12 `##` heading coverage.

**Remaining gaps:**
- Pre-existing Advisory (CC-001-qg1r3): `plugin.json` `"license": "MIT"` versus root `LICENSE` Apache 2.0. Not a deliverable violation — the guide correctly cites Apache 2.0. The minor negative traceability impact from this repository-level inconsistency is acknowledged, not scored against the guide.
- No traceability gaps were identified by any of the three strategy reviewers.

**Scoring rationale:** Traceability is the strongest dimension in the document and has been throughout the QG-1 history. The 5-iteration change summary, SM/DA/CC finding identifier system, and verified anchor infrastructure constitute a high-quality traceability record. Score 0.93 — not higher because the repository advisory (plugin.json) introduces a minor external inconsistency, and the calibration anchor "0.95-1.00: publication-ready, 0-1 Minor" suggests this dimension is not yet fully at that level.

---

## Strategy Finding Impact

### Overall Finding Count

| Strategy | Critical | Major | Minor | Verdict Effect |
|----------|----------|-------|-------|----------------|
| S-003 Steelman | 0 | 0 | 3 | Positive confirmation + 3 Minor improvements identified |
| S-002 Devil's Advocate | 0 | 0 | 4 | FIRST 0-Major round; 4 Minor edge-case gaps found |
| S-007 Constitutional | 0 | 0 | 0 | Full PASS (1.00); 1 pre-existing Advisory |
| **Total** | **0** | **0** | **7** | |

### Finding-to-Dimension Mapping

The 7 Minor findings distributed across dimensions as follows:

| Finding | Dimension(s) Affected | Score Effect |
|---------|----------------------|-------------|
| SM-001-qg1r3 (uv version floor) | Completeness | Minor negative on Completeness |
| SM-002-qg1r3 (PROJ-001 naming) | Internal Consistency | Minor negative on Internal Consistency |
| SM-003-qg1r3 (`<project-required>` troubleshooting) | Completeness, Actionability | Minor negative on both; double-flagged with DA-003 |
| DA-001-qg1r3 (Set-Service admin) | Methodological Rigor | Minor negative on Rigor |
| DA-002-qg1r3 (--apple-use-keychain version) | Methodological Rigor, Evidence Quality | Minor negative on both |
| DA-003-qg1r3 (`<project-required>` unexplained) | Completeness, Actionability | Overlaps with SM-003; confirms gap is real |
| DA-004-qg1r3 (@jerry suffix) | Internal Consistency, Actionability | Minor negative on both |

### Significance of 0 Majors

The absence of Major findings in QG-1 Retry 3 is meaningful. In the QG-1 history:
- Initial: 9 Major findings across 3 strategies
- Retry 1: 4 new Majors (DA found new edge cases)
- Retry 2: 2 Majors (ssh-keygen Windows, passphrase prompt)
- **Retry 3: 0 Majors (first time)**

The 7 remaining Minors are individually small but collectively sufficient to suppress four dimensions by 0.01 each relative to the 0.92 threshold. The composite score of 0.9100 reflects genuine near-threshold quality.

### S-003 Steelman Score Estimate vs. Actual

The Steelman estimated 0.93-0.95. The actual score is 0.9100. The delta (0.02-0.04 lower) is explained by:
1. DA strategy found 4 additional Minors that the Steelman did not, including the @jerry finding which affects both Internal Consistency and Actionability.
2. The leniency bias rule was applied at the Internal Consistency 0.91/0.92 boundary, choosing 0.91.

### S-002 Devil's Advocate Score Estimate vs. Actual

The Devil's Advocate estimated 0.92-0.94. The actual score is 0.9100. The delta is explained by:
1. The DA's own estimate of "-0.02 to -0.04" from Minor findings pushed the score below the lower bound of its range.
2. Leniency bias application resolved the Internal Consistency uncertainty to 0.91.

---

## Score Trajectory

| Round | Score | Delta | Verdict |
|-------|-------|-------|---------|
| QG-1 Initial | 0.7665 | — | REVISE |
| QG-1 Retry 1 | 0.8300 | +0.0635 | REJECTED |
| QG-1 Retry 2 | 0.8470 | +0.0170 | REVISE |
| QG-1 Retry 3 | 0.9100 | +0.0630 | REVISE |

**Trajectory note:** The +0.0630 improvement from Retry 2 to Retry 3 is the largest single-round improvement since Retry 1, reflecting the significance of resolving both Major findings. The document is 0.0100 below threshold. This is the narrowest gap in the QG-1 history.

---

## Improvement Recommendations

The deliverable requires minor targeted revisions to reach 0.92. All 7 findings are Minor. Estimated effort: 15-25 lines total across all 7 fixes.

### P1 — Highest Value (address to reach 0.92)

These two fixes collectively address the two dimensions currently scoring below 0.92 (Completeness at 0.90 and the overlapping Actionability gap) and would bring the composite to approximately 0.9160-0.9200:

| Priority | Finding ID | Action | Estimated Lines | Dimensions Improved |
|----------|-----------|--------|-----------------|---------------------|
| 1a | SM-003-qg1r3 / DA-003-qg1r3 | Add Troubleshooting entry for `<project-required>` and `<project-error>` session tags. Include: cause (JERRY_PROJECT not set or incorrect), solution (set env var + verify directory), and note that `/help` works without a project. | 12-15 lines | Completeness, Actionability |
| 1b | DA-004-qg1r3-da | Add one sentence to Installation Step 5 (both macOS and Windows) explaining that `@jerry` matches the directory name from Step 4. Add a note to "Plugin Not Found" Troubleshooting entry covering directory-name mismatch as a cause. | 4-6 lines | Internal Consistency, Actionability |

### P2 — Standard Polish (address to improve beyond 0.92)

| Priority | Finding ID | Action | Estimated Lines | Dimensions Improved |
|----------|-----------|--------|-----------------|---------------------|
| 2a | DA-002-qg1r3-da | Add "(macOS Ventura 13+ only)" qualifier to the Keychain Tip header, OR add `-K` as a fallback for older macOS: "If `--apple-use-keychain` is not recognized on older macOS, use `-K` instead." | 1-2 lines | Methodological Rigor, Evidence Quality |
| 2b | DA-001-qg1r3-da | Add parenthetical admin note to the `Set-Service` comment line: `# To make this permanent (requires admin PowerShell):` or add a preceding note. | 1-2 lines | Methodological Rigor |
| 2c | SM-001-qg1r3 | Replace "Latest" with "0.5.0+" (or author-confirmed floor) in the uv row of the Prerequisites table. | 1 line | Completeness |
| 2d | SM-002-qg1r3 | Replace `PROJ-001-my-project` (four occurrences) with `PROJ-NNN-my-project` in the Configuration Project Setup section. | 4 lines (4 substitutions) | Internal Consistency |

### Advisory (non-blocking, separate task)

- CC-001-qg1r3: Update `.claude-plugin/plugin.json` line 9 from `"license": "MIT"` to `"license": "Apache-2.0"`. Repository-level fix, not a change to the installation guide.

---

## Self-Review Verification (H-15)

- [x] Each dimension scored independently with specific evidence before computing composite
- [x] Leniency bias actively counteracted — Internal Consistency scored 0.91 not 0.92 after applying "uncertain = lower" rule; no dimension inflated beyond what evidence supports
- [x] Weighted composite calculated correctly: 0.90×0.20 + 0.91×0.20 + 0.91×0.20 + 0.91×0.15 + 0.91×0.15 + 0.93×0.10 = 0.1800 + 0.1820 + 0.1820 + 0.1365 + 0.1365 + 0.0930 = 0.9100
- [x] Verdict matches threshold (0.9100 < 0.92 = REVISE, not PASS)
- [x] Score reflects current artifact quality, not revision effort — prior score (0.8470) used only for delta reference, not as an anchor; all dimensions scored fresh against the current document
- [x] All three strategy reports read in full and incorporated — SM findings, DA findings, and Constitutional findings each mapped to specific dimensions
- [x] Prior score context used for delta (+0.0630) only; no anchoring to 0.8470 when setting dimension scores
- [x] The 0.92 threshold is treated as genuinely excellent — REVISE verdict issued despite the close margin (0.0100 below threshold) because the 7 Minor findings are real, documented, and independently confirmed by two separate strategies (SM-003 and DA-003 both flag the `<project-required>` gap)
- [x] Retry 3 context acknowledged but not rewarded — the score of 0.9100 is graded on current artifact merit, not on the fact that this is round 4

---

*Scored by: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: epic001-docs-20260218-001 | QG-1 Retry 3*
*Date: 2026-02-18*

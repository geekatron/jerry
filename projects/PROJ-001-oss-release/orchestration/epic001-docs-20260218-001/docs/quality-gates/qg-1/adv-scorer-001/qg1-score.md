# Quality Score Report: Jerry Framework Installation Guide

## L0 Executive Summary

**Score:** 0.7665/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.72)

**One-line assessment:** The document has a sound core structure and meets all four acceptance criteria, but 9 Major findings across three adversarial strategies expose real user-failure scenarios (destructive ssh-keygen without pre-check, missing Claude Code version prerequisite, incomplete PAT flow, unverified manifest path) that pull the score well below the 0.92 threshold; targeted revision addressing the 4 Devil's Advocate Major findings is required.

---

## Scoring Context

| Field | Value |
|-------|-------|
| **Deliverable** | `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md` |
| **Deliverable Type** | Documentation (Installation Guide) |
| **Criticality Level** | C2 (Standard) |
| **Scoring Strategy** | S-014 (LLM-as-Judge) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Prior Creator-Critic Score** | 0.934 (post-iteration-2, ps-critic-001) |
| **Scored** | 2026-02-18T00:00:00Z |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.7665 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Band** | 0.70–0.84 (significant gaps, focused revision needed) |
| **Strategy Findings Incorporated** | Yes — 3 reports: S-003 (9 findings), S-007 (3 findings), S-002 (7 findings); 19 total, 9 Major |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.74 | 0.1480 | AC-1 through AC-4 met; but CC version missing from Prerequisites, PAT flow incomplete, /adversary skill absent, 2 ToC entries missing |
| Internal Consistency | 0.20 | 0.80 | 0.1600 | Well-structured; "password-free access" claim conditionally inaccurate; macOS/Windows SSH agent tip asymmetry |
| Methodological Rigor | 0.20 | 0.72 | 0.1440 | Logical SSH flow and stable anchors; but no pre-check before destructive ssh-keygen; manifest path unverified assertion |
| Evidence Quality | 0.15 | 0.78 | 0.1170 | Technical commands verified accurate (uv, SSH, git, plugin); manifest path at .claude-plugin/plugin.json is an unverified assertion |
| Actionability | 0.15 | 0.77 | 0.1155 | Core steps specific and executable; Claude Code version gate missing from Prerequisites; PAT ongoing-use guidance absent; PAT alternative placement sub-optimal |
| Traceability | 0.10 | 0.82 | 0.0820 | Change log thorough; AC traceability verified; Claude Code version not traceable from Prerequisites; BOOTSTRAP.md path ambiguous |
| **TOTAL** | **1.00** | | **0.7665** | |

---

## Detailed Dimension Analysis

### Completeness (0.74/1.00)

**Evidence:**

Strengths — All four acceptance criteria are fully satisfied:
- AC-1: No archive distribution references (S-007 confirmed)
- AC-2: Collaborator SSH flow (Steps 1–4 plus Next Steps) is complete for the intended audience
- AC-3: Future: Public Repository section present with clear "future state" framing
- AC-4: /plugin marketplace add and /plugin install jerry-framework@jerry documented for both platforms

Gaps:

1. **DA-002 (Major):** Claude Code minimum version 1.0.33+ is absent from the Prerequisites > Required Software table. The row for Claude Code shows "Latest" in the Version column. The version constraint appears only in Troubleshooting ("Plugin support requires Claude Code version 1.0.33 or later"). A user following Prerequisites has no way to know a version floor exists until the installation fails.

2. **DA-003 (Major):** The PAT Alternative section documents the clone operation only ("when `git clone` prompts for a password, enter your PAT instead"). It is silent on credential persistence for subsequent `git pull`, `git fetch`, and `git push`. Users who choose PAT will face repeated credential prompts after initial install with no documented resolution.

3. **SM-003 / CC-003 (Major / Minor):** The Available Skills table lists 6 of 7 skills. `/adversary` is absent despite being listed in CLAUDE.md Quick Reference as a fully operational skill. The "Using Jerry" section's purpose is to orient new users to available capabilities; the omission leaves the most sophisticated skill undiscovered.

4. **CC-001 (Major):** Two `##` headings — `## Getting Help` (line 756) and `## License` (line 764) — are present in the document body but absent from the Table of Contents. NAV-004 (MEDIUM) requires all major `##` headings be listed.

**Improvement Path:** Add Claude Code version 1.0.33+ to Prerequisites table; expand PAT Alternative to cover ongoing git operations and credential caching; add /adversary row to Available Skills table; add Getting Help and License to Table of Contents.

---

### Internal Consistency (0.80/1.00)

**Evidence:**

Strengths — The document is well-structured with deliberate cross-referencing:
- Stable HTML anchor IDs (`<a id="macos-step-3">`, `<a id="windows-step-3">`) correctly resolve platform cross-references
- Collaborator notes in platform Step 2 are properly past-tense ("you have already cloned via SSH — skip this step")
- Step numbering rationalized in Iteration 2 (dual numbering system eliminated)
- All 10 Table of Contents anchor links verified correct by S-007

Gaps:

1. **DA-007 (Minor):** "SSH keys provide secure, password-free access" (Why SSH? section) is stated as an absolute claim but is conditionally true: it holds only when no passphrase is set, or when a passphrase is set and an SSH agent is running. The macOS Keychain tip was added in Iteration 2, and the Windows tip was identified as a gap (SM-004), but neither addition corrected the parent claim in Why SSH?. The claim is therefore internally inconsistent with the passphrase guidance that follows.

2. **SM-004 (Major):** The macOS section has a Keychain tip for passphrase management (added Iteration 2); the Windows section has no equivalent. Both platforms support SSH agent passphrase caching; the asymmetric coverage creates an inconsistent user experience between platforms.

3. **CC-002 (Minor):** The Table of Contents header uses `| Section | Description |` where the framework standard (NAV-003) specifies `| Section | Purpose |`. All `.context/rules/` files use "Purpose"; this user-facing doc uses "Description" — a minor but detectable framework inconsistency.

**Improvement Path:** Qualify the "password-free access" claim to be accurate for both passphrase and non-passphrase scenarios; add Windows SSH agent tip to mirror the macOS Keychain tip; update ToC column header to "Purpose".

---

### Methodological Rigor (0.72/1.00)

**Evidence:**

Strengths — The procedural methodology is generally sound:
- SSH key setup follows a correct, sequential 4-step gate: generate key → register with GitHub → verify connectivity → clone
- HTML anchor strategy correctly solves the duplicate-heading GitHub anchor problem
- The Future vs. Current path separation is logically clean and prevents user confusion
- S-007 confirms H-05/H-06 compliance: all Python execution in the developer section uses `uv run`
- Change log documents additive-only strategy, preserving existing content

Gaps:

1. **DA-001 (Major):** The `ssh-keygen` instruction in Step 1 (both macOS and Windows) directs users to "Press Enter to accept the default (`~/.ssh/id_ed25519`)" with no prior existence check. Any user with an existing key at that path will be prompted with "Overwrite (y/n)?" by ssh-keygen — and a user following step-by-step instructions is at high risk of pressing `y` without understanding the consequences (private key destruction, access loss on all registered services). This is a standard safety check omission: technically rigorous installation procedures always check for existing files before overwriting. The document even acknowledges the multi-key scenario in Troubleshooting ("ssh-add -l") but does not apply that knowledge at the generation step — an internal process inconsistency.

2. **DA-004 (Major):** Step 3 in both platform sections instructs users to verify the plugin manifest at `~/plugins/jerry/.claude-plugin/plugin.json`. The document presents this as a verifiable confirmation step, but the path is asserted, not confirmed against the actual repository. The Steelman itself flags this as an unverified assumption (Step 4, Best Case Assumptions). If the path is incorrect, the verification step fails for all users, and the document provides no fallback — the troubleshooting section for "Plugin Not Found" reuses the same unverified path.

**Improvement Path:** Add a key-existence pre-check before ssh-keygen on both platforms (conditional: if key exists, display and proceed to Step 2; if not, generate); confirm and verify .claude-plugin/plugin.json against actual repository structure.

---

### Evidence Quality (0.78/1.00)

**Evidence:**

Strengths — S-007 performed a systematic technical command audit and found:
- `ssh-keygen -t ed25519 -C "..."` — correct syntax for both platforms
- `ssh -T git@github.com` — correct GitHub SSH verification command
- `git clone git@github.com:geekatron/jerry.git ~/plugins/jerry` — correct SSH clone syntax
- `curl -LsSf https://astral.sh/uv/install.sh | sh` — correct uv macOS installer
- `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` — correct uv Windows installer
- `eval "$(ssh-agent -s)"` + `ssh-add --apple-use-keychain` — correct macOS Keychain commands
- `Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"` — correct PowerShell command
- `/plugin marketplace add ~/plugins/jerry` and `/plugin install jerry-framework@jerry` — Claude Code commands documented
- `uv run python scripts/bootstrap_context.py` — correct uv-based Python execution

Gaps:

1. **DA-004 (Major):** The manifest path `~/plugins/jerry/.claude-plugin/plugin.json` (and Windows equivalent) is stated without cross-referencing the actual repository structure. The verification step instructs users to confirm a file the document has not confirmed exists. This is a material evidence gap: a verification step is supposed to confirm a known-good state, but here it asserts an expected state based on an unconfirmed assumption. The Steelman explicitly lists this as a key assumption: "The `.claude-plugin/plugin.json` manifest exists in the repository root's `.claude-plugin/` directory."

2. **DA-006 (Minor):** The Windows SSH agent tip (SM-004, Steelman-recommended addition not yet applied) would instruct `Start-Service ssh-agent` without noting the prerequisite that OpenSSH Client must be installed. On Windows 10 builds before 1809 and on some enterprise configurations, this command fails silently. The evidence context for the Windows SSH agent tip is incomplete.

**Improvement Path:** Confirm plugin.json path against actual repository; add OpenSSH Client prerequisite note to Windows SSH agent tip.

---

### Actionability (0.77/1.00)

**Evidence:**

Strengths — The core installation paths are highly actionable:
- uv installation commands are complete and executable on both platforms, including the PATH verification and fix steps
- SSH key generation, GitHub registration, and connectivity test steps are specific and sequential
- /plugin commands are complete with alternatives (interactive installation path documented)
- Troubleshooting section provides specific resolution steps for 6 named failure modes with specific error symptoms and multi-step solutions
- Configuration section provides a concrete scope selection guide with a recommendation

Gaps:

1. **DA-002 (Major):** A user cannot act on the Claude Code version requirement because it is not in Prerequisites. The actionable check (verify Claude Code version) must happen before installation begins; placing it in Troubleshooting only means it is discoverable only after failure. This is a structural actionability failure.

2. **DA-003 (Major):** PAT users after initial clone have no actionable guidance for subsequent git operations. The document says "SSH keys are preferred" but does not explain the concrete consequence (repeated credential prompts) or provide an action to avoid it (credential helper configuration).

3. **SM-002 (Major):** The PAT Alternative is placed after "Next Steps: Complete Platform Installation" — sequentially past the decision point. A user at Step 4 (Clone) who prefers PAT must read ahead to the end of the section to find the alternative. A forward reference at Step 4 would make the decision point actionable at the right moment.

4. **SM-001 (Major):** The "Why the marketplace mechanism?" explanation is absent. First-time users unfamiliar with the Claude Code plugin ecosystem may not understand why two commands (/plugin marketplace add, then /plugin install) are required. The lack of rationale reduces confidence in the procedure.

**Improvement Path:** Add Claude Code version check to Prerequisites; expand PAT Alternative with credential helper guidance; add forward reference to PAT Alternative at Step 4 clone block; add marketplace rationale callout.

---

### Traceability (0.82/1.00)

**Evidence:**

Strengths:
- The change summary header (lines 1–81) provides explicit AC satisfaction mapping: "Satisfies: EN-940, AC-2" and "Satisfies: EN-941, AC-3"
- Iteration history is documented: Iteration 1 changes, Iteration 2 changes with specific finding IDs (MAJOR-001, MAJOR-002, MINOR-001 through MINOR-005)
- S-007 acceptance criteria compliance check confirms all four ACs as VERIFIED COMPLIANT with evidence citations
- HTML anchor IDs are stable and explicitly placed for cross-reference targets
- Finding identifiers in strategy reports (SM-NNN-qg1s, CC-NNN, DA-NNN-qg1da) provide downstream traceability to this scoring report

Gaps:

1. Claude Code version 1.0.33+ is a functional requirement of the installation procedure but is not traceable from the Prerequisites section. A reader following the document cannot trace what version is needed until they hit a failure and navigate to Troubleshooting.

2. **SM-007 (Minor):** The BOOTSTRAP.md reference (`[Bootstrap Guide](BOOTSTRAP.md)`) uses a bare relative path that is ambiguous given the document's location at `docs/INSTALLATION.md`. The file resolves to `docs/BOOTSTRAP.md`, but the actual BOOTSTRAP.md location in the repository is unconfirmed.

**Improvement Path:** Add version requirement to Prerequisites for full traceability from requirements to verification; confirm and correct BOOTSTRAP.md relative path.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Finding | Dimension | Current Score | Target | Recommendation |
|----------|---------|-----------|---------------|--------|----------------|
| 1 | DA-001 | Methodological Rigor | 0.72 | 0.82+ | Add key-existence pre-check before ssh-keygen on both platforms: check if `~/.ssh/id_ed25519` exists; if yes, display public key and proceed to Step 2; if no, run ssh-keygen |
| 2 | DA-002 | Completeness + Actionability | 0.74 / 0.77 | 0.82+ / 0.84+ | Add Claude Code row to Prerequisites table with version "1.0.33+" and link to version check instructions |
| 3 | DA-004 | Methodological Rigor + Evidence Quality | 0.72 / 0.78 | 0.82+ / 0.85+ | Confirm .claude-plugin/plugin.json path against actual repository; update verification step command to match actual path |
| 4 | DA-003 | Completeness + Actionability | 0.74 / 0.77 | 0.82+ / 0.84+ | Add credential caching note to PAT Alternative: provide `git config --global credential.helper manager` (Windows) / `osxkeychain` (macOS) / `store` (Linux) with security implications |
| 5 | CC-001 | Completeness | 0.74 | 0.82+ | Add two ToC rows after Uninstallation: `[Getting Help](#getting-help)` and `[License](#license)` |
| 6 | SM-003 / CC-003 | Completeness | 0.74 | 0.82+ | Add `/adversary` row to Available Skills table: `Adversary | /adversary | Adversarial quality reviews and tournament scoring` |
| 7 | DA-007 | Internal Consistency | 0.80 | 0.86+ | Qualify "password-free access" claim in Why SSH? to be accurate for both passphrase and non-passphrase scenarios |
| 8 | SM-004 | Internal Consistency | 0.80 | 0.86+ | Add Windows SSH agent tip after Windows Step 1 to match the macOS Keychain tip (platform parity) |
| 9 | SM-002 | Actionability | 0.77 | 0.84+ | Add forward reference to PAT Alternative at end of Step 4 clone block |
| 10 | SM-001 | Actionability | 0.77 | 0.84+ | Add "Why the marketplace mechanism?" callout paragraph in Installation section |

---

## Score Calibration Note

The prior creator-critic score was 0.934. The adversarial strategies surfaced 9 Major findings across all three strategies that were not visible to the creator-critic loop. The gap between 0.934 and 0.7665 reflects the information advantage of adversarial review:

- The creator-critic loop correctly validated AC-1 through AC-4 compliance, structural soundness, and technical command accuracy.
- The adversarial strategies exposed user-failure scenarios (ssh-keygen overwrite risk, version prerequisite gap, PAT ongoing-use gap, manifest path assertion) that require real-world failure conditions to manifest — conditions a creator-critic loop reviewing the document's internal logic would not simulate.

This is the expected behavior of the adversarial review layer: it does not contradict the creator-critic assessment; it extends it into failure mode territory.

---

## Leniency Bias Check

- [x] Each dimension scored independently — no cross-dimension score inflation applied
- [x] Evidence documented for each score — specific finding IDs and deliverable line references cited
- [x] Uncertain scores resolved downward:
  - Completeness: 0.74 (not 0.78) — two DA Major findings directly cause user failure, not just information gaps
  - Methodological Rigor: 0.72 (not 0.75) — ssh-keygen overwrite is a data destruction risk; manifest path is an unverified verification step
  - Actionability: 0.77 (not 0.80) — version gate absence and PAT incompleteness are structural actionability failures, not polish items
- [x] Post-iteration-2 deliverable calibration applied — the 0.934 prior score is a creator-critic score without adversarial input; this score reflects adversarial findings not previously surfaced
- [x] No dimension scored above 0.95 — highest is Traceability at 0.82
- [x] Weighted composite verified: 0.148 + 0.160 + 0.144 + 0.117 + 0.1155 + 0.082 = 0.7665

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.7665
threshold: 0.92
weakest_dimension: Methodological Rigor
weakest_score: 0.72
critical_findings_count: 0
major_findings_count: 9
strategy_reports_incorporated: 3
iteration: 1  # first adversarial scoring (post iteration-2 creator-critic)
improvement_recommendations:
  - "Add ssh-keygen pre-check on both platforms before key generation (DA-001)"
  - "Add Claude Code version 1.0.33+ to Prerequisites Required Software table (DA-002)"
  - "Confirm and update plugin.json manifest path against actual repository (DA-004)"
  - "Add credential helper guidance to PAT Alternative section (DA-003)"
  - "Add Getting Help and License to Table of Contents (CC-001)"
  - "Add /adversary to Available Skills table (SM-003/CC-003)"
  - "Qualify password-free access claim in Why SSH? section (DA-007)"
  - "Add Windows SSH agent tip for platform parity with macOS (SM-004)"
  - "Add PAT Alternative forward reference at Step 4 clone block (SM-002)"
  - "Add marketplace rationale callout to Installation section (SM-001)"
```

---

*Scored by: adv-scorer v1.0.0*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: epic001-docs-20260218-001 | QG-1*
*Date: 2026-02-18T00:00:00Z*

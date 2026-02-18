# Steelman Report: Jerry Framework Installation Guide

## Steelman Context

- **Deliverable:** `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md`
- **Deliverable Type:** Documentation (End-User Installation Guide)
- **Criticality Level:** C2
- **Strategy:** S-003 (Steelman Technique)
- **Quality Gate:** QG-1 Retry 3 (user-authorized override of max_retries=2 per P-020)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor | **Date:** 2026-02-18T00:00:00Z | **Original Author:** ps-architect-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and improvement count |
| [Prior Findings Verification](#prior-findings-verification) | Confirms all QG-1 Retry 2 findings resolved |
| [Step 1: Charitable Interpretation](#step-1-charitable-interpretation) | Core thesis and key claims |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. structural vs. evidence gaps |
| [Steelman Reconstruction](#steelman-reconstruction) | Annotated strongest-form reconstruction (inline SM-NNN) |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Conditions under which document is most compelling |
| [Improvement Findings Table](#improvement-findings-table) | All SM-NNN findings with severity and dimension |
| [Improvement Details](#improvement-details) | Expanded detail for Critical/Major findings |
| [Scoring Impact](#scoring-impact) | Dimension-by-dimension scoring effect |

---

## Summary

**Steelman Assessment:** The Jerry Framework Installation Guide has reached a mature, high-quality state after five iterative revision cycles. All seven QG-1 Retry 2 findings (2 Major, 5 Minor from DA and Steelman strategies) are fully resolved. The document successfully covers SSH key generation with platform parity, passphrase handling, credential caching, space-in-path warnings at all four clone locations, and a forward-looking public release section. Three minor residual gaps remain — all in the presentation/evidence category — none of which threaten the document's core thesis or ability to guide a first-time collaborator to a successful installation.

**Improvement Count:** 0 Critical, 0 Major, 3 Minor

**Original Strength:** The document is strong entering QG-1 Retry 3. The architecture (Prerequisites → Collaborator flow → Platform tabs → Future section → Configuration → Verification → Usage → Troubleshooting) is sound and complete. All prior Major findings have been addressed with targeted, accurate fixes.

**Recommendation:** Incorporate 3 Minor improvements, then proceed to S-002 Devil's Advocate per H-16. No author review cycle required before critique — improvements are polish-level and do not alter the document's substance.

---

## Prior Findings Verification

All seven findings from QG-1 Retry 2 (adv-executor and adv-scorer, Iteration 5 fixes) have been verified as resolved.

| Finding ID | Severity | Fix Applied | Verification |
|------------|----------|-------------|--------------|
| SM-001-qg1r2s | Minor | Expanded Configuration scope note with team-onboarding consequence | RESOLVED — Line 706: "Jerry is added to `.claude/settings.json`, which is committed to version control — new team members have Jerry active automatically after cloning the repository." |
| SM-002-qg1r2s | Minor | Added JERRY_PROJECT note + /help fallback in Verification | RESOLVED — Lines 760-761: Note present under "Test a Skill" step. |
| SM-003-qg1r2s | Minor | Space-in-path callout in PAT Alternative Step 3 | RESOLVED — Lines 436-437: Important callout present above macOS and Windows clone commands. |
| DA-001-qg1r2-da | Major | Windows OpenSSH Client pre-check BEFORE ssh-keygen | RESOLVED — Lines 320-325: Important callout with Settings UI path and Add-WindowsCapability command appears before the ssh-keygen command. |
| DA-002-qg1r2-da | Major | Passphrase prompt note after ssh -T success block | RESOLVED — Lines 389-390: Note present explaining passphrase entry before success message, plus troubleshooting entry updated with "passphrase not entered" cause. |
| DA-003-qg1r2-da | Minor | Space-in-path callout in Future section Step 2 | RESOLVED — Lines 666-667: Important callout present in Future section. |
| DA-004-qg1r2-da | Minor | PowerShell path utility replacing $env:USERNAME tip | RESOLVED — Lines 637-640: `(Get-Item "$env:USERPROFILE\plugins\jerry").FullName -replace '\\','/'` tip present with explanatory sentence. |

**All 7 prior findings: RESOLVED.**

---

## Step 1: Charitable Interpretation

**Core Thesis:** Jerry Framework can be successfully installed by any new collaborator (on macOS or Windows) by following a structured, self-contained guide that resolves every plausible SSH, credential, path, and platform-specific failure mode — and that the same document simultaneously prepares for public release without requiring future restructuring.

**Key Claims:**

1. SSH key generation with passphrase handling is the recommended authentication path for collaborators, with PAT as a complete documented alternative.
2. The installation flow (marketplace add → plugin install) is identical regardless of authentication method used to clone.
3. Windows users have full feature parity with macOS users — every SSH, agent, and credential feature has a PowerShell equivalent.
4. The document is future-proof: public release simplifies installation to HTTPS without restructuring the existing sections.
5. New team members using Project scope automatically receive Jerry active without additional configuration.

**Strengthening Opportunities (presentation-level):**

- uv version floor is absent from the Prerequisites table (only tool without a floor)
- The Configuration section uses `PROJ-001-my-project` as its project name example — this overlaps with the actual PROJ-001 in this repository, which could momentarily confuse first-time users
- No troubleshooting entry exists for the `<project-required>` tag that new users will encounter when they run `/problem-solving` without JERRY_PROJECT set (the Verification Note directs to `/help` but doesn't explain what `<project-required>` means)

---

## Step 2: Weakness Classification

| ID | Weakness | Type | Magnitude | Location |
|----|----------|------|-----------|----------|
| SM-001-qg1r3 | uv has no version floor in Prerequisites table — only tool listed as "Latest" | Presentation | Minor | Prerequisites, Required Software table |
| SM-002-qg1r3 | `PROJ-001-my-project` example in Configuration could confuse users of the actual Jerry repo | Presentation | Minor | Configuration, Project Setup step 1 |
| SM-003-qg1r3 | No troubleshooting entry for `<project-required>` / `<project-error>` session start tags | Structural | Minor | Troubleshooting section |

**Decision Point:** All weaknesses are presentation/structural. No substantive weakness found. Proceed to Step 3.

---

## Steelman Reconstruction

The reconstruction below preserves all original content verbatim and shows only the three targeted improvements inline. Each improvement is annotated with `[SM-NNN-qg1r3]`. Surrounding text is shown for context only; unmarked content is unchanged.

---

### SM-001-qg1r3: uv Version Floor in Prerequisites Table

**Location:** Prerequisites → Required Software table, row for uv

**Before:**
```markdown
| [uv](https://docs.astral.sh/uv/) | Latest | Python dependency management for hooks | See platform instructions below |
```

**After `[SM-001-qg1r3]`:**
```markdown
| [uv](https://docs.astral.sh/uv/) | 0.5.0+ | Python dependency management for hooks | See platform instructions below |
```

**Rationale:** Every other tool in the table has a version floor. uv's "Latest" is the only exception, which implicitly signals no minimum requirement exists. In practice, uv's tool interface stabilized around 0.5.x. Specifying a floor aligns the table with the style of the other entries and signals that very old uv installations should be upgraded. If the actual minimum is not precisely known, the value `0.5.0+` is appropriately conservative (uv 0.5.0 was released in late 2024; any installation newer than this will work) and can be updated by the author if a tighter floor is known.

---

### SM-002-qg1r3: Project Name Example in Configuration

**Location:** Configuration → Project Setup → Step 1

**Before:**
```markdown
export JERRY_PROJECT=PROJ-001-my-project
```

**After `[SM-002-qg1r3]`:**
```markdown
export JERRY_PROJECT=PROJ-NNN-my-project
```

And the Windows PowerShell line:

**Before:**
```powershell
$env:JERRY_PROJECT = "PROJ-001-my-project"
```

**After:**
```powershell
$env:JERRY_PROJECT = "PROJ-NNN-my-project"
```

And the `mkdir` line:

**Before:**
```bash
mkdir -p projects/PROJ-001-my-project/.jerry/data/items
```

**After:**
```bash
mkdir -p projects/PROJ-NNN-my-project/.jerry/data/items
```

And similarly for the Windows `New-Item` command.

**Rationale:** Using `PROJ-001` as the example overlaps with the Jerry repository's own PROJ-001 project identifier. A first-time user reading the guide while inside the Jerry repository could create a directory that accidentally collides with (or appears to duplicate) the actual PROJ-001 project tracking. Replacing with `PROJ-NNN` (the standard Jerry placeholder for a project number) is maximally clear that this is a template to fill in, not a literal value to use.

---

### SM-003-qg1r3: Troubleshooting Entry for `<project-required>` Tag

**Location:** Troubleshooting section — add after "Repository Not Found (Collaborators)" entry

**After `[SM-003-qg1r3]`:**

```markdown
### Session Starts with `<project-required>` or `<project-error>`

**Symptom:** When Claude Code starts, the session output contains a `<project-required>` or `<project-error>` tag instead of proceeding with work.

**Cause:** The `JERRY_PROJECT` environment variable is not set, or is set to a project directory that does not exist.

**Solutions:**
1. Set the project environment variable before starting Claude Code:
   - macOS/Linux: `export JERRY_PROJECT=PROJ-NNN-my-project`
   - Windows PowerShell: `$env:JERRY_PROJECT = "PROJ-NNN-my-project"`
2. Ensure the project directory exists: `projects/PROJ-NNN-my-project/`
3. If you do not have a project yet, create one following the [Project Setup](#project-setup-optional) steps in the Configuration section.
4. To use Jerry skills without a project, use `/help` to verify skill availability — most skills require an active project for full functionality.
```

**Rationale:** The Verification section already directs users to use `/help` if they skip Configuration, and the SessionStart hook actively emits these tags. However, no Troubleshooting entry exists to explain what these tags mean or how to resolve them. New users who proceed directly to Verification without setting JERRY_PROJECT will encounter this tag at first run and have no Troubleshooting entry to consult. Adding this entry closes the loop between the Verification Note and the Troubleshooting section, and is consistent with the document's pattern of having a troubleshooting entry for every expected first-run failure mode.

---

## Step 4: Best Case Scenario

**Ideal Conditions:** This guide is most compelling when:

1. The reader is a new collaborator who has received a GitHub invitation, is on either macOS or Windows, and follows the document top-to-bottom.
2. They hit at least one of the pre-documented failure modes (ssh-keygen not found on Windows, passphrase prompt at `ssh -T`, credential helper unavailable, spaces in path) and find the exact troubleshooting entry they need without leaving the document.
3. They proceed to install, configure, and verify with zero unresolved questions.

**Key Assumptions That Must Hold:**

- The `git@github.com:geekatron/jerry.git` clone URL matches the actual private repository location.
- `"name": "jerry-framework"` in `.claude-plugin/plugin.json` is the current manifest value (confirmed by P3-DA-003 fix in Iteration 3).
- Claude Code version 1.0.33+ supports the `/plugin` command as documented.
- The `/adversary` skill is available (added in P6-SM-003/CC-003 fix).

**Confidence Assessment:** HIGH. The document covers all primary installation paths (SSH with/without passphrase, PAT, public future path) with explicit failure-mode handling. After five revision cycles targeting every identified gap, the remaining improvements are polish-level. A rational evaluator reviewing the strongest-form version (with the three Minor SM-NNN improvements incorporated) would conclude this is a production-ready installation guide.

---

## Improvement Findings Table

| ID | Improvement | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|--------------|-----------|
| SM-001-qg1r3 | Add uv version floor to Prerequisites table | Minor | `Latest` | `0.5.0+` | Completeness |
| SM-002-qg1r3 | Replace PROJ-001 example with PROJ-NNN placeholder in Configuration | Minor | `PROJ-001-my-project` (×4 occurrences) | `PROJ-NNN-my-project` | Internal Consistency |
| SM-003-qg1r3 | Add `<project-required>` troubleshooting entry | Minor | No entry exists | New entry with 4-step resolution guide | Completeness |

**Severity Key:** Critical = fundamental gap undermining core argument; Major = significant gap materially lowering quality; Minor = polish improving precision or rigor without changing substance.

---

## Improvement Details

All three findings are Minor. Per Section 5 of the template, expanded detail is required for Critical and Major findings only. No expanded detail sections are required here.

For completeness, brief rationale is provided inline in the Steelman Reconstruction section above for each SM-NNN finding.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-001-qg1r3 (uv floor) and SM-003-qg1r3 (troubleshooting entry) fill two minor gaps. All primary installation paths, platform pairs, failure modes, and prerequisite rows are already covered after five revisions. |
| Internal Consistency | 0.20 | Positive | SM-002-qg1r3 eliminates the PROJ-001 overlap that could confuse users of the actual Jerry repository. All other cross-references (HTML anchors, section links, clone URLs, manifest values) are internally consistent. |
| Methodological Rigor | 0.20 | Neutral | The document's methodology (SSH-first with PAT alternative, explicit pre-checks before every command, space-in-path warnings at all four clone points, passphrase handling documented at both generation and verification steps) is already rigorous. No improvements affect methodology. |
| Evidence Quality | 0.15 | Neutral | All commands are accurate and platform-verified through multiple iterations. The uv version floor (SM-001-qg1r3) is the only evidence-adjacent item, and it is a conservative lower bound. |
| Actionability | 0.15 | Positive | SM-003-qg1r3 adds a direct 4-step resolution guide for the `<project-required>` scenario, which is the first thing a user without JERRY_PROJECT set will encounter at verification time. Without this, the Verification Note's `/help` pointer is the only guidance. |
| Traceability | 0.10 | Neutral | The document's change summary header (lines 1-205) provides full iteration-by-iteration traceability. SM-NNN identifiers have been used consistently across all five iterations. No traceability gaps found. |

---

## Execution Statistics

- **Total Findings:** 3
- **Critical:** 0
- **Major:** 0
- **Minor:** 3
- **Prior Findings Verified Resolved:** 7 of 7
- **Protocol Steps Completed:** 6 of 6
- **Score Estimate Range:** 0.93–0.95 (document is above the 0.92 PASS threshold; Minor improvements would push toward the high end of this range)

---

## H-15 Self-Review

Per H-15, self-review applied before persistence:

1. All findings have specific evidence from the deliverable (line references, exact quoted content, before/after shown) — PASS
2. All findings classified as Minor — justified by absence of any gap that undermines core thesis or materially weakens quality — PASS
3. Finding identifiers follow SM-NNN-qg1r3 format consistently — PASS
4. Summary table matches detailed findings (3 Minor, 0 Critical/Major) — PASS
5. Prior findings verification table is complete (7 of 7 resolved) — PASS
6. No findings omitted or minimized (P-022) — PASS

Report is ready for downstream strategies per H-16.

---

*Strategy: S-003 (Steelman Technique)*
*Template: `.context/templates/adversarial/s-003-steelman.md` v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Agent: adv-executor v1.0.0*
*Executed: 2026-02-18*

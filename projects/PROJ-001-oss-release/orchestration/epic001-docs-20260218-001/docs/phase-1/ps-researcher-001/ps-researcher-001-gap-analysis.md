# FEAT-017 Gap Analysis — INSTALLATION.md

> **Agent ID:** ps-researcher-001
> **Workflow ID:** epic001-docs-20260218-001
> **Phase:** 1 (Requirements & Gap Analysis)
> **Date:** 2026-02-18
> **Source File:** `docs/INSTALLATION.md` (475 lines)
> **Feature:** FEAT-017 — Installation Instructions Modernization

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical stakeholder summary |
| [L1: Gap Analysis Matrix](#l1-gap-analysis-matrix) | AC/enabler classification table with evidence |
| [L2: Strategic Assessment](#l2-strategic-assessment) | Effort, risks, sequencing |
| [Detailed Findings — EN-939](#detailed-findings--en-939-remove-archive-based-installation) | Archive distribution model analysis |
| [Detailed Findings — EN-940](#detailed-findings--en-940-collaborator-installation-ssh--marketplace) | Collaborator path analysis |
| [Detailed Findings — EN-941](#detailed-findings--en-941-public-repository-installation-path) | Public repo path analysis |
| [Analysis Confidence](#analysis-confidence) | Ambiguities and transparency notes |

---

## L0: Executive Summary

### Current State

`docs/INSTALLATION.md` is a well-structured, 475-line installation guide that has already been substantially modernized for the Claude Code marketplace plugin distribution model. The document covers macOS and Windows installation paths, uv setup, Claude Code plugin commands (`/plugin marketplace add`, `/plugin install`), verification steps, configuration, skill usage, troubleshooting, and developer setup. It is written at a high quality level with clear tables, code blocks, and navigation.

### Key Finding: No Archive References Detected

The most important finding for EN-939 is that **no references to a private archive distribution model exist in the current document**. There are no mentions of `.tar.gz` files, `.zip` archives, private download links, internal registry URLs, or any other archive-based distribution mechanism. The document already uses the public GitHub clone approach (`git clone https://github.com/geekatron/jerry.git`) combined with Claude Code's local marketplace plugin system. EN-939 is therefore **PRESENT** — the removal work has already been done, or the file was written fresh for the marketplace model.

### Key Finding: Collaborator SSH Path is Absent

The document assumes the repository is publicly accessible via a standard HTTPS `git clone` from GitHub. There is no section or instruction addressing the scenario where a prospective user is a collaborator on a private repository who must first set up SSH key authentication, configure GitHub access, and then proceed through the installation steps. The collaborator-specific setup path (SSH keygen, GitHub SSH key registration, verifying access before cloning) is entirely absent. This constitutes a significant gap for EN-940 and AC-2.

### Key Finding: Public Repository Future Path is Absent

The document does not contain a dedicated section distinguishing between the current (collaborator or private access) installation scenario and a future scenario where the repository is public and users can install without any GitHub access provisioning. While the current instructions would technically work for a public repo clone, there is no explicit forward-looking section framing the public repo scenario, which is required by EN-941 and AC-3. A "Future: Public Repository Installation" section must be created.

### Claude Code Marketplace Integration

AC-4 (Claude Code marketplace integration) is **PRESENT** and well-documented. Steps 4 and 5 in both the macOS and Windows sections (lines 90–116, 171–191) cover the `/plugin marketplace add` and `/plugin install` commands. The Verification and Troubleshooting sections also reinforce marketplace usage. No gap exists for AC-4.

---

## L1: Gap Analysis Matrix

| Item | Description | Classification | Evidence (Line Numbers) | Notes |
|------|-------------|---------------|------------------------|-------|
| **AC-1** | No archive distribution references in active instructions | **PRESENT** | Full file scan — no archive references found | EN-939 is already satisfied |
| **AC-2** | Step-by-step collaborator installation (SSH key + GitHub + marketplace) | **ABSENT** | Lines 72–117 (macOS), 143–191 (Windows) — clone uses HTTPS, no SSH setup | Must add collaborator section |
| **AC-3** | Public repo installation path documented | **ABSENT** | Entire file — no "future public repo" section exists | Must add future-state section |
| **AC-4** | Claude Code marketplace integration instructions included | **PRESENT** | Lines 44–116 (macOS), 171–191 (Windows), 196–216 (Verification) | Fully documented |
| **EN-939** | Remove/deprecate archive-based installation instructions | **PRESENT** | Full file scan — no archive distribution model references | No action required |
| **EN-940** | Document collaborator-based installation — SSH + marketplace | **ABSENT** | Lines 72–79 assume HTTPS clone; no SSH keygen/GitHub setup steps | Must add SSH key section |
| **EN-941** | Document public repository installation path | **ABSENT** | Full file — no future-state public repo section exists | Must add forward-looking section |

---

## L2: Strategic Assessment

### Effort Estimates

| Enabler | Planned Effort | Assessed Effort | Rationale |
|---------|---------------|-----------------|-----------|
| EN-939 | 2 | **0** | Already complete. No archive references exist. |
| EN-940 | 3 | **3** | Confirmed: SSH key setup instructions, GitHub access configuration, and platform-specific clone variants must all be written from scratch. Effort estimate is accurate. |
| EN-941 | 2 | **2** | A distinct "Future: Public Repository" section must be authored with clear conditional framing. Effort estimate is accurate. |

**Total revised effort: 5 points** (vs 7 planned — EN-939 saves 2 points).

### Risks

| Risk | Severity | Notes |
|------|----------|-------|
| SSH key setup steps are platform-specific and can vary by GitHub account state | MEDIUM | macOS, Windows (PowerShell), and Windows (Git Bash) all have different key generation flows. The section must cover all three. |
| Collaborator scenario requires external dependency (GitHub admin adds user as collaborator) | MEDIUM | Cannot document the GitHub admin-side steps, only the user-side response. Must explicitly note the pre-condition. |
| Public repo section must not mislead current collaborators into skipping SSH setup | MEDIUM | Clear conditional framing ("When Jerry becomes public...") is required. |
| The current clone URLs use HTTPS (lines 77, 152). For collaborators on private repos, HTTPS clone may also work if the user has a GitHub personal access token. Must clarify SSH vs token paths. | LOW | Document both or pick one; consistency matters for troubleshooting. |

### Recommended Approach

1. **EN-939 (PRESENT — no action):** Confirm no archive references exist, document as complete. Do not add any deprecation notices as there is nothing to deprecate.

2. **EN-940 (ABSENT — create):** Insert a new top-level section titled "Collaborator Installation (Private Repository)" or similar, placed **before** the existing Installation section (or as a separate tab/path within it). This section should:
   - Explain the pre-condition: user must be added as a collaborator by a repo admin
   - Provide SSH key generation steps for macOS and Windows
   - Provide GitHub SSH key registration steps
   - Show the SSH clone URL variant replacing the HTTPS URL
   - Then continue with the existing marketplace steps (which remain valid)

3. **EN-941 (ABSENT — create):** Insert a new section titled "Future: Public Repository Installation" near the end of the Installation section or as a clearly framed appendix. This section should:
   - Explain that when Jerry is publicly released, no SSH setup or collaborator invite is needed
   - Show the standard HTTPS clone command (already present in existing steps, so reference it)
   - Note that marketplace steps remain identical
   - Frame the section with "Note: This section documents a future state. Jerry is currently distributed to collaborators only."

4. **AC-4 (PRESENT — verify only):** The marketplace integration is already documented. ps-architect-001 should verify the `/plugin` command syntax is current during Phase 2 drafting.

### Sequencing Recommendation

Given EN-939 is already complete:
- Phase 2 ps-architect-001 can focus exclusively on writing the collaborator SSH section (EN-940) and the future public repo section (EN-941)
- The existing marketplace content should be preserved as-is (it is high quality)
- Changes are additive, not destructive — low revision risk
- The overall document structure (Table of Contents, platform tabs) should be updated to include the new sections

---

## Detailed Findings — EN-939: Remove Archive-Based Installation

### Current State

**Classification: PRESENT**

A full search of `docs/INSTALLATION.md` (all 475 lines) reveals no references to any archive-based distribution model. Specifically, the following terms and patterns were searched and not found:
- `.tar.gz`, `.zip`, `.tar`, `.tgz`
- "download", "extract", "archive", "bundle"
- Private registry or internal repository URLs
- Manual copy/paste installation flows
- "artifact", "release asset", "attachment"

The document uses exclusively:
1. Public GitHub clone via HTTPS: `git clone https://github.com/geekatron/jerry.git ~/plugins/jerry` (line 77, line 152)
2. Claude Code local marketplace: `/plugin marketplace add ~/plugins/jerry` (line 95, line 176)
3. Plugin install command: `/plugin install jerry-framework@jerry` (line 105, line 188)

### Specific Gap Evidence

No gaps found. The distribution model in the current document is already the marketplace/clone model, not an archive model.

### Recommended Changes

None. EN-939 is fully satisfied.

### Effort Assessment

**Planned: 2 points. Actual: 0 points.** The file was either written fresh for the marketplace model, or a prior cleanup was completed before this analysis. Either way, no action is required for EN-939.

---

## Detailed Findings — EN-940: Collaborator Installation (SSH + Marketplace)

### Current State

**Classification: ABSENT**

The current Installation section (lines 43–191) assumes the repository is accessible via public HTTPS clone. The clone commands at lines 77 (macOS) and 152 (Windows PowerShell) / 158 (Windows Git Bash) use HTTPS URLs:

- Line 77: `git clone https://github.com/geekatron/jerry.git ~/plugins/jerry`
- Line 152: `git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"`
- Line 158: `git clone https://github.com/geekatron/jerry.git ~/plugins/jerry` (Git Bash alternative)

There is no mention of:
- SSH key generation (`ssh-keygen`)
- Adding an SSH public key to a GitHub account
- SSH-based clone URLs (`git@github.com:geekatron/jerry.git`)
- Pre-conditions for collaborator access (repo admin invitation)
- GitHub personal access token (PAT) as an alternative HTTPS authentication method for private repos

The existing steps would fail silently for a collaborator attempting to clone a private repository without prior authentication setup. The user would receive a "repository not found" or "authentication failed" error from `git clone` with no guidance on resolution.

### Specific Gaps Identified

| Gap | Line Reference | Description |
|-----|---------------|-------------|
| Missing collaborator pre-condition | Lines 43–50 (Installation intro) | No mention that private repo access requires collaborator invite from admin |
| Missing SSH key generation | None | No `ssh-keygen -t ed25519 -C "email"` command |
| Missing GitHub SSH key registration | None | No instructions to add public key at github.com/settings/keys |
| Missing SSH clone URL | Lines 77, 152, 158 | Only HTTPS clone shown; SSH clone (`git@github.com:...`) not present |
| Missing SSH connectivity test | None | No `ssh -T git@github.com` verification step |
| Missing PAT alternative | None | HTTPS + personal access token path not documented |

### Recommended Changes

**Add a new section before or within the existing Installation section.** Suggested placement: immediately after the "Installation" header (line 43) and before the platform tabs (line 54), as a "Choose Your Installation Path" decision point. Alternative: a dedicated subsection titled "Collaborator Installation (Private Repository)" placed before the macOS/Windows tabs.

Content to add (high-level):
1. Pre-condition: "Your repository admin must first invite you as a collaborator."
2. SSH key setup for macOS: `ssh-keygen -t ed25519 -C "your.email@example.com"`, `cat ~/.ssh/id_ed25519.pub`, add to github.com settings
3. SSH key setup for Windows (PowerShell): `ssh-keygen -t ed25519 -C "your.email@example.com"`, `Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"`, add to github.com settings
4. Verify SSH access: `ssh -T git@github.com`
5. Replace HTTPS clone URL with SSH variant: `git clone git@github.com:geekatron/jerry.git ~/plugins/jerry`
6. Continue with existing Steps 3–5 (plugin manifest, marketplace add, plugin install — unchanged)

### Effort Assessment

**Planned: 3 points. Assessed: 3 points.** Confirmed. Writing platform-specific SSH setup instructions (macOS + Windows PowerShell + Git Bash variant), GitHub key registration steps, connectivity verification, and integration with the existing step flow justifies the 3-point estimate. The content is procedural but requires care to be accurate and untangled from the existing HTTPS path.

---

## Detailed Findings — EN-941: Public Repository Installation Path

### Current State

**Classification: ABSENT**

The entire file (475 lines) contains no section or mention of a future public repository scenario. The document does not distinguish between a "current private/collaborator" model and a "future public" model. While the current HTTPS clone instructions technically describe what public repo installation would look like, there is no explicit framing that:
1. The current installation requires collaborator access (private repo)
2. There exists a future state where Jerry will be publicly available
3. The installation steps for the public scenario differ from the private/collaborator scenario (or confirm they are the same with context)

The closest relevant content is the Getting Help section (lines 464–469) which links to GitHub Issues at `github.com/geekatron/jerry/issues`, implying a public GitHub presence, but this does not constitute documentation of the public installation path.

### Specific Gaps Identified

| Gap | Line Reference | Description |
|-----|---------------|-------------|
| No "Future: Public Repo" section | Entire file | No conditional framing for public availability |
| No distinction between current and future distribution models | Lines 43–50 (Installation intro) | Intro does not state current distribution is collaborator-only |
| No note that public scenario eliminates SSH setup requirement | None | Future users need to know SSH setup is not required once repo is public |

### Recommended Changes

**Add a clearly framed forward-looking section.** Suggested placement: at the end of the Installation section, before the Verification section (line 193), or as a subsection within Installation.

Suggested section structure:

```markdown
### Future: Public Repository Installation

> **Note:** This section documents a future installation scenario. Jerry is currently
> distributed to collaborators only. When Jerry becomes publicly available, these
> instructions will apply.

When Jerry is released as a public repository, no collaborator invite or SSH setup
is required. Installation simplifies to:

**Step 1: Install uv** (same as above — platform-specific)

**Step 2: Clone Jerry**
```bash
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

**Steps 3–5:** Identical to the existing marketplace steps (verify manifest,
add marketplace, install plugin).

No GitHub account is required to clone a public repository. If you encounter
authentication prompts, verify the repository is publicly accessible at
github.com/geekatron/jerry.
```

The section must be clearly labeled as future-state to avoid misleading current collaborators.

### Effort Assessment

**Planned: 2 points. Assessed: 2 points.** Confirmed. The section content is relatively short (the future-state steps largely reference existing content), but the conditional framing and integration with the broader document structure requires careful drafting to avoid ambiguity.

---

## Analysis Confidence

### Ambiguities

| Ambiguity | Assessment |
|-----------|------------|
| Whether the current HTTPS clone path works for collaborators with GitHub PAT authentication | The file does not address this. HTTPS + PAT is a valid GitHub collaborator pattern but is undocumented. EN-940 should address whether to document PAT as an alternative or to standardize on SSH-only. |
| Whether "collaborator installation" should be a separate top-level section or integrated into the existing macOS/Windows tabs | This is a structural decision for ps-architect-001 to resolve in Phase 2. Both approaches are valid; integrated tabs are more consistent with the current structure but increase complexity. |
| The phrase "GitHub + marketplace" in EN-940 may refer to the Claude Code marketplace, not the GitHub Marketplace — this analysis assumes Claude Code marketplace, consistent with the rest of the document. | Confidence: HIGH. Context confirms this interpretation. |

### Confidence Level

**HIGH** for all three enablers. The analysis is based on a complete read of all 475 lines of `docs/INSTALLATION.md`. The absence of archive references (EN-939) and collaborator/public-repo sections (EN-940, EN-941) is definitive — these are factual absences, not interpretation calls.

---

*Agent: ps-researcher-001*
*Workflow: epic001-docs-20260218-001*
*Phase: 1*
*Output: `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-1/ps-researcher-001/ps-researcher-001-gap-analysis.md`*

# FEAT-017 Installation Draft — Quality Review

> **Agent ID:** ps-critic-001
> **Workflow ID:** epic001-docs-20260218-001
> **Phase:** 2 (FEAT-017 Execution — Creator-Critic Review)
> **Date:** 2026-02-18
> **Draft Under Review:** `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md`
> **Scoring Method:** S-014 LLM-as-Judge (6-dimension weighted composite)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Overall quality assessment and verdict |
| [AC Verification Matrix](#ac-verification-matrix) | Pass/Fail status for each acceptance criterion |
| [Dimension Scores](#dimension-scores) | S-014 rubric scores across all 6 dimensions |
| [Weighted Composite Score](#weighted-composite-score) | Final calculated score and threshold comparison |
| [Issues Found](#issues-found) | Specific defects with severity classification |
| [Improvement Recommendations](#improvement-recommendations) | Actionable guidance for the revision pass |
| [Verdict](#verdict) | PASS / REVISE outcome with rationale |

---

## L0: Executive Summary

The draft produced by ps-architect-001 represents a well-executed, additive update to the Jerry installation guide. The architect correctly identified that the work was ADDITIVE ONLY — no existing content was removed or degraded — and successfully authored the two missing sections that the gap analysis identified (EN-940 collaborator SSH installation, EN-941 public repository future path). All four acceptance criteria are addressable in the draft, though AC-2 carries one notable structural weakness discussed below.

The collaborator installation section (EN-940) is technically sound. The SSH key generation commands are correct for both macOS and Windows, the GitHub key registration steps are accurate, and the SSH connectivity verification step with expected output is included. The PAT alternative note is appropriately scoped without expanding the section beyond EN-940's boundaries. Platform parity between macOS and Windows is maintained throughout the SSH section. Two new troubleshooting entries for collaborator scenarios (SSH authentication failures and repository-not-found) were added and are well-targeted.

The primary weakness in the draft is a navigation and flow issue in the transition from the Collaborator Installation section to the existing Installation section. The instruction at the end of Step 4 ("Continue with Steps 3-5") uses anchor links that resolve to the same fragment ID for both macOS and Windows (`#step-3-verify-the-plugin-manifest`), which is structurally ambiguous — GitHub Markdown and most renderers will only anchor to the first matching heading, meaning the Windows anchor link may silently resolve to the macOS section. This is a MAJOR internal consistency defect. Additionally, the draft's ToC cross-reference row "Future: Public Repository" uses an anchor (`#future-public-repository-installation`) that resolves correctly, but the Windows-specific `Step 1: Install uv` anchor in the "Future" section references `#step-1-install-uv-1`, an auto-generated disambiguator that may not be reliable across rendering environments. These anchor fragility issues should be remediated before the draft is applied to `docs/INSTALLATION.md`.

The document is otherwise actionable, complete, and stylistically consistent with the existing guide. Traceability to the source enablers is present in the change summary comment.

---

## AC Verification Matrix

| AC | Criterion | Verdict | Evidence |
|----|-----------|---------|----------|
| AC-1 | No archive distribution references remain | PASS | Full draft review confirms no `.tar.gz`, `.zip`, "download", "archive", "extract", "registry", or similar terms. Distribution model is exclusively marketplace + git clone. Gap analysis confirmed this was already true of the original; draft preserves that. |
| AC-2 | Step-by-step collaborator installation (SSH key + GitHub + marketplace) | PASS with caveat | SSH key generation (macOS + Windows), GitHub key registration, SSH connectivity test, SSH clone URL, and transition to marketplace steps are all present. Caveat: the anchor link in "Steps 5–7: Continue with Platform Installation" for Windows resolves ambiguously (see Issues). |
| AC-3 | Public repository installation path documented | PASS | "Future: Public Repository Installation" section is present, clearly framed as future state, includes comparison table, and directs users to existing marketplace steps. |
| AC-4 | Claude Code marketplace integration instructions included | PASS | `/plugin marketplace add` and `/plugin install` commands are present in both macOS and Windows sections, unchanged from the original and verified correct. |

---

## Dimension Scores

### Completeness (weight: 0.20)

**Score: 0.88**

All four acceptance criteria are addressed. SSH steps are present for both macOS (Terminal) and Windows (PowerShell), including key generation, public key display, GitHub registration, connectivity verification, and SSH clone commands. The PAT alternative is documented. The future public repo section includes a platform split for the clone command (macOS/Linux and Windows). Two new troubleshooting entries address collaborator-specific failure modes.

Deductions:
- The "Steps 5–7: Continue with Platform Installation" subsection tells the user to continue at `Step 3` in the platform section but does not repeat or fully enumerate what steps 5-7 of the overall flow actually are. The heading text ("Steps 5–7") is confusing — this implies steps numbered 5, 6, and 7 exist, when in fact the collaborator section only defines Steps 1–4 and then hands off to the platform section's Steps 3–5. The numbering creates a discontinuity: a user who counts steps 1 (keygen), 2 (add to GitHub), 3 (verify), 4 (clone), then arrives at "Steps 5–7" might reasonably expect three more numbered items. (-0.06)
- The "Future: Public Repository" section references `#step-1-install-uv-1` for Windows, which is a renderer-generated anchor and not declared in the document. A user on a rendering platform that does not auto-generate disambiguation suffixes will get a broken link. (-0.06)

### Internal Consistency (weight: 0.20)

**Score: 0.78**

This is the weakest dimension. Several consistency issues were found:

1. **Anchor collision (MAJOR):** The document contains two headings both rendered as "Step 3: Verify the Plugin Manifest" — one under `### macOS` and one under `### Windows`. Standard Markdown renderers (including GitHub) generate a disambiguated second anchor `#step-3-verify-the-plugin-manifest-1`, but the draft's cross-reference at line 206–207 lists:
   - `[macOS — Step 3 onwards](#step-3-verify-the-plugin-manifest)`
   - `[Windows — Step 3 onwards](#step-3-verify-the-plugin-manifest-1)`
   The Windows link uses `#step-3-verify-the-plugin-manifest-1` which is correct for GitHub rendering but is fragile and undocumented. In non-GitHub Markdown renderers (e.g., VS Code preview, MkDocs, Docusaurus), the suffix convention differs. (-0.10)

2. **Step numbering discontinuity (MAJOR):** The collaborator section labels its steps 1–4 (keygen, GitHub, verify, clone), then creates a section called "Steps 5–7: Continue with Platform Installation." The platform macOS/Windows sections label their steps 1–5 (uv, clone, manifest, marketplace, install). The collaborator user is directed to "Step 3 onwards" of the platform section, which in the combined flow would be steps 5, 6, 7 of a hypothetical global numbering — but the handoff section says "Steps 5–7" while the platform sections still say "Step 3," "Step 4," "Step 5." This creates a dual-numbering system that could confuse users following the collaborator path. (-0.08)

3. **Git note in collaborator clone section (MINOR):** At line 262, the macOS Step 2 in the Installation section says "Collaborators: If you are installing from a private repository, use the SSH clone URL and the steps in the Collaborator Installation section above instead of this step." This is correct but technically a user following the Collaborator Installation path from the top has already cloned and would encounter this note mid-stream. The note could be misread as an instruction to restart. (-0.04)

### Methodological Rigor (weight: 0.20)

**Score: 0.92**

The SSH setup instructions are technically correct:
- `ssh-keygen -t ed25519 -C "your.email@example.com"` is the correct modern algorithm (ed25519 preferred over RSA 4096 per current GitHub recommendations).
- The passphrase prompt guidance is accurate.
- `cat ~/.ssh/id_ed25519.pub` (macOS) and `Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"` (Windows) are both correct for displaying the public key.
- The SSH connectivity test (`ssh -T git@github.com`) is the canonical GitHub verification step and the expected output shown is accurate.
- The SSH clone URL format (`git@github.com:geekatron/jerry.git`) is correct.
- The PAT instructions (repo scope, token entry as password) are accurate.
- The marketplace commands (`/plugin marketplace add`, `/plugin install jerry-framework@jerry`) are consistent with the established document.

Minor deduction: The Windows SSH keygen section notes the default file location as `C:\Users\YOU\.ssh\id_ed25519` but uses `YOU` as a placeholder rather than `YOUR_USERNAME` (which is the convention used elsewhere in the Windows Installation section for path substitution). Minor inconsistency in placeholder naming convention. (-0.05)
- The Git Bash alternative note states "the macOS Terminal commands above work identically in Git Bash" — this is accurate for key generation but the public key display command (`cat`) also works in Git Bash, so the claim is correct. No deduction.

### Evidence Quality (weight: 0.15)

**Score: 0.87**

Command outputs are shown where they matter most:
- `uv --version` verification shows expected output format `# Should output: uv 0.x.x` — present in original, preserved.
- SSH connectivity test shows exact expected output: `Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.` — this is correct and directly actionable.
- Plugin manifest verification shows `"name": "jerry"` as expected output.

Deductions:
- `ssh-keygen` does not show expected terminal interaction output (the prompt sequence for file location and passphrase). The prose describes what the prompts say, which is adequate, but showing the actual terminal exchange would increase confidence for first-time SSH users. (-0.05)
- The Windows `ssh-keygen` section ends with "Copy the full output — it begins with `ssh-ed25519`" but does not show a sample truncated key. The macOS section also omits this. Users unfamiliar with SSH keys may not know what "the full output" means in terms of length and format. (-0.05)
- `ssh-add -l` is mentioned in troubleshooting but never introduced in the setup section as a way to verify the key is loaded by the agent. For macOS users with a passphrase, the ssh-agent persistence step (adding key to macOS Keychain via `ssh-add --apple-use-keychain`) is absent. This is a common friction point. (-0.03)

### Actionability (weight: 0.15)

**Score: 0.84**

The draft is largely followable end-to-end, but the collaborator path has a seam that would create friction:

A new collaborator starting from the top of the document would:
1. Read the "Collaborator Installation" section header and begin.
2. Complete Steps 1–4 (keygen, GitHub, verify, clone).
3. Arrive at "Steps 5–7: Continue with Platform Installation" and be told to jump to `Step 3` in the macOS or Windows section.
4. Navigate to the Installation section and find `Step 3: Verify the Plugin Manifest` — which is correct.
5. BUT: the same macOS Step 2 ("Clone Jerry") contains a note: "Collaborators: If you are installing from a private repository, use the SSH clone URL and the steps in the Collaborator Installation section above instead of this step." A user who arrived via the collaborator path and scrolled to Step 3 would first see Step 2 and its note, which tells them to go back — even though they already completed that step.

This reverse-navigation note (correct in isolation, misleading in the collaborator flow) reduces actionability. A user might second-guess whether they completed Step 2 correctly. (-0.08)

Additionally:
- The PAT alternative section does not specify the minimum token scope needed. "repo scope" is stated but not explained (whether `read:org`, `repo`, or `public_repo` is sufficient). (-0.04)
- The "Future: Public Repository" section references step anchors for uv installation that depend on auto-generated IDs. A user on a non-GitHub renderer would arrive at a broken link. (-0.04)

### Traceability (weight: 0.10)

**Score: 0.93**

The draft includes a comprehensive change summary comment at the top of the file that:
- Attributes each section to the specific enabler (EN-940, EN-941) and acceptance criteria (AC-2, AC-3).
- Notes that AC-1 and AC-4 were verified present without new changes.
- Explains structural decisions (collaborator section placement, PAT as a note, Git Bash alternative).

Traceability back to EN-939/940/941 is present. The FEAT-017 spec cites ACT-004, DEC-003, and TOP-003 from the transcript packet as source; the draft does not trace to those directly, but these are transcript references that do not belong in the installed doc — the change summary is the correct vehicle. Minor deduction for the change summary not explicitly noting the workflow ID that could be used to locate the full chain. (-0.07)

---

## Weighted Composite Score

| Dimension | Weight | Raw Score | Weighted |
|-----------|--------|-----------|---------|
| Completeness | 0.20 | 0.88 | 0.176 |
| Internal Consistency | 0.20 | 0.78 | 0.156 |
| Methodological Rigor | 0.20 | 0.92 | 0.184 |
| Evidence Quality | 0.15 | 0.87 | 0.131 |
| Actionability | 0.15 | 0.84 | 0.126 |
| Traceability | 0.10 | 0.93 | 0.093 |
| **TOTAL** | **1.00** | | **0.866** |

**Weighted Composite: 0.866**

Band: **REVISE** (0.85–0.91 range — near threshold; targeted revision likely sufficient)

---

## Issues Found

### CRITICAL (0 found)

No critical issues were found. No existing content was broken, removed, or corrupted. The new sections do not introduce security concerns or technically incorrect commands.

---

### MAJOR

#### MAJOR-001: Duplicate Heading Anchors Create Fragile Navigation

**Location:** Draft lines 206–207 (cross-reference to macOS and Windows Step 3)
**Dimension Affected:** Internal Consistency, Actionability

The "Steps 5–7" transition subsection links to:
```
[macOS — Step 3 onwards](#step-3-verify-the-plugin-manifest)
[Windows — Step 3 onwards](#step-3-verify-the-plugin-manifest-1)
```

The Windows anchor (`#step-3-verify-the-plugin-manifest-1`) is a GitHub Markdown auto-generated disambiguator — it is not declared anywhere in the document as a heading ID. This anchor will break in:
- VS Code Markdown preview (uses its own disambiguation convention)
- MkDocs and Docusaurus (generate IDs differently)
- Any renderer that does not follow GitHub's exact disambiguation algorithm

**Recommended fix:** Rename the Windows heading from `#### Step 3: Verify the Plugin Manifest` to `#### Step 3: Verify the Plugin Manifest (Windows)` to force a unique auto-generated anchor, then update the cross-reference link to match. Or use explicit HTML anchors (`<a id="...">`) to guarantee stable IDs.

---

#### MAJOR-002: Step Numbering Discontinuity in Collaborator Flow

**Location:** Draft "Steps 5–7: Continue with Platform Installation" subsection
**Dimension Affected:** Internal Consistency, Actionability

The collaborator section defines numbered steps 1–4, then creates a bridge section titled "Steps 5–7" that redirects to steps labeled "Step 3, 4, 5" in the platform sections. This dual-numbering system creates cognitive dissonance: users following the collaborator path encounter globally numbered steps (1–7) while the platform sections use locally numbered steps (1–5). A user directed to "Step 3 onwards" in the Windows section will see "Step 3: Verify the Plugin Manifest" which is fine, but also "Step 2: Clone Jerry" with a collaborator note — the out-of-order encounter creates friction.

**Recommended fix:** Rename the transition section to "Next Steps: Complete Platform Installation" (removing the "5–7" numbering). Alternatively, renumber the platform steps as a continuation of the collaborator steps (5: Verify Manifest, 6: Add Marketplace, 7: Install Plugin) with clear cross-references.

---

### MINOR

#### MINOR-001: Collaborator Note in Platform Steps Creates Reverse-Navigation Confusion

**Location:** Draft line 262 (macOS Step 2) and line 345 (Windows Step 2)
**Dimension Affected:** Actionability

Both platform "Clone Jerry" steps include a collaborator note that redirects users to the Collaborator Installation section. A collaborator following the correct top-to-bottom path will have already completed the clone before reaching this step. When they skip to Step 3 per the "Steps 5–7" section, they will see this note immediately before the step they need, creating a momentary "did I do this wrong?" reaction.

**Recommended fix:** Change the note wording to past tense acknowledgment: "Collaborators: If you arrived from the Collaborator Installation section, you have already cloned via SSH. Proceed to Step 3 below." This removes ambiguity without requiring structural changes.

---

#### MINOR-002: Windows Placeholder Naming Inconsistency in SSH Section

**Location:** Draft line 137 (`C:\Users\YOU\.ssh\id_ed25519`)
**Dimension Affected:** Internal Consistency

The Windows SSH key file location uses `YOU` as a username placeholder. The Windows Installation section uses `YOUR_USERNAME` consistently (e.g., `/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry`). This is a minor stylistic inconsistency.

**Recommended fix:** Replace `C:\Users\YOU\.ssh\id_ed25519` with `C:\Users\YOUR_USERNAME\.ssh\id_ed25519`.

---

#### MINOR-003: macOS Keychain Integration for SSH Agent Not Documented

**Location:** Draft — absent from macOS SSH key setup
**Dimension Affected:** Evidence Quality, Actionability

On macOS, after generating an SSH key with a passphrase, the key must be added to the ssh-agent (and optionally to the macOS Keychain) to avoid re-entering the passphrase on every clone/pull. Without this step, a user with a passphrase-protected key will be prompted for the passphrase on every `git` operation. The standard commands are:

```bash
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

The current draft omits this. Git Bash on Windows has analogous complexity (ssh-agent start). Omitting it is defensible if the goal is minimal scope, but it will be a common friction point for macOS users who chose a passphrase.

**Recommended fix (optional):** Add a brief callout after Step 1 (macOS): "If you set a passphrase, add your key to the macOS Keychain to avoid re-entering it: `ssh-add --apple-use-keychain ~/.ssh/id_ed25519`."

---

#### MINOR-004: "Future: Public Repository" Step Anchors Use Fragile Auto-Generated IDs

**Location:** Draft lines 389, 403 — references to `#step-1-install-uv` and `#step-1-install-uv-1`
**Dimension Affected:** Internal Consistency, Actionability

The "Future: Public Repository" section links to uv installation steps using auto-generated anchor IDs. Same fragility as MAJOR-001 but lower impact because these links are in a future-state section that current users are not expected to follow interactively.

**Recommended fix:** Use the same disambiguation approach recommended for MAJOR-001, or rephrase the references to use section names rather than anchors: "See [macOS uv installation](#macos) or [Windows uv installation](#windows)."

---

#### MINOR-005: PAT Scope Explanation Incomplete

**Location:** Draft "PAT Alternative" subsection
**Dimension Affected:** Evidence Quality

The PAT section states "Create a PAT at github.com/settings/tokens with `repo` scope." New users unfamiliar with GitHub PATs may not know whether `repo` means the top-level `repo` scope (which grants read/write to all repos) or a fine-grained subset. For a collaborator who only needs to clone, `contents: read` (fine-grained) or `repo` (classic) are both valid but have different permission implications.

**Recommended fix:** Clarify: "Create a classic PAT at github.com/settings/tokens (not fine-grained) and check the `repo` scope checkbox. This grants read access to private repositories."

---

## Improvement Recommendations

Recommendations are ordered by impact on composite score.

| Priority | Recommendation | Addresses | Score Impact |
|----------|---------------|-----------|-------------|
| 1 | Fix MAJOR-001: Rename Windows heading to create unique anchor, update cross-reference | Internal Consistency, Actionability | +0.04 to composite |
| 2 | Fix MAJOR-002: Rename "Steps 5–7" to "Next Steps: Complete Platform Installation" | Internal Consistency, Actionability | +0.03 to composite |
| 3 | Fix MINOR-001: Rephrase collaborator note in platform clone steps | Actionability | +0.01 to composite |
| 4 | Fix MINOR-002: Normalize placeholder to `YOUR_USERNAME` | Internal Consistency | +0.005 to composite |
| 5 | Fix MINOR-004: Replace fragile auto-generated anchors in Future section | Internal Consistency | +0.01 to composite |
| 6 | Add MINOR-003: macOS Keychain integration callout | Evidence Quality, Actionability | +0.01 to composite |
| 7 | Clarify MINOR-005: PAT scope explanation | Evidence Quality | +0.005 to composite |

**Estimated score after full remediation:** 0.91–0.93

Remediation priorities 1–5 are sufficient to cross the 0.92 threshold with high confidence. Priorities 6–7 are quality improvements but not threshold-gating.

---

## Verdict

**REVISE**

**Score: 0.866 — below the 0.92 threshold required by H-13 for C2+ deliverables.**

The draft is fundamentally sound. The content is technically correct, all four acceptance criteria are satisfied, and the additive approach correctly preserves the quality of the original document. The issues preventing a PASS are structural and navigational, not substantive:

- MAJOR-001 (anchor fragility) and MAJOR-002 (step number discontinuity) are the primary score drags. Both are fixable with targeted edits that do not require rewriting the content.
- No CRITICAL issues were found. The path from REVISE to PASS does not require architectural changes to the draft.

The ps-architect-001 revision pass should address MAJOR-001 and MAJOR-002 at minimum. Addressing MINOR-001 through MINOR-005 as well would produce a document that clears the threshold with margin.

---

*Agent: ps-critic-001*
*Workflow: epic001-docs-20260218-001*
*Phase: 2*
*Output: `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-2/ps-critic-001/ps-critic-001-installation-review.md`*

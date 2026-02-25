# Quality Score Report: Jerry INSTALLATION.md (C4 Iteration 1)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict, score, and top action item |
| [Scoring Context](#scoring-context) | Deliverable metadata and scoring parameters |
| [Score Summary](#score-summary) | Composite score, threshold, verdict |
| [Dimension Scores](#dimension-scores) | Weighted score table across 6 dimensions |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, and improvement paths |
| [C4 Findings Register](#c4-findings-register) | Open findings from C4 Devil's Advocate with status |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered remediation table |
| [Leniency Bias Check](#leniency-bias-check) | Bias counteraction verification |
| [Session Context Handoff](#session-context-handoff) | Structured handoff YAML for orchestrator |

---

## L0 Executive Summary

**Score:** 0.79/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.72)

**One-line assessment:** The document is technically accurate, well-structured, and handles SSH/HTTPS correctly, but the C4 Devil's Advocate execution surface eight findings (1 Critical, 5 Major, 2 Minor) that identify real coverage gaps — no decision guide routing users to the correct install path, "Optional" framing of required configuration, undefined "marketplace" terminology, and McConkey voice at instructional moments — that collectively hold Completeness and Actionability well below the C4 threshold of 0.95; targeted revision addressing the Critical finding and three of the five Major findings is required before acceptance.

---

## Scoring Context

- **Deliverable:** `docs/INSTALLATION.md`
- **Deliverable Type:** Documentation (OSS public-facing installation guide)
- **Criticality Level:** C4 (Critical — irreversible once published; public OSS reference documentation)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — C4 S-002 Devil's Advocate (8 findings: 1 Critical, 5 Major, 2 Minor) from `docs/reviews/adv-s002-devils-advocate-installation-c4.md`
- **Prior Scores (prior document versions):** 0.74 (iter 1), 0.84 (iter 2), 0.88 (iter 3), 0.89 (iter 4) — all C2 scoring
- **C4 Threshold:** 0.95 (per user specification — higher than H-13 standard 0.92)
- **Scored:** 2026-02-25

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.79 |
| **C4 Threshold** | 0.95 |
| **Verdict** | REVISE |
| **Gap to Threshold** | -0.16 |
| **Strategy Findings Incorporated** | Yes — 8 findings (1 Critical, 5 Major, 2 Minor) from C4 S-002 Devil's Advocate |
| **Open Critical Findings** | 1 (DA-001-20260225: `/plugin marketplace list` not integrated as required step) |
| **Open Major Findings** | 5 (DA-002 through DA-006 from 20260225 execution) |
| **Open Minor Findings** | 2 (DA-007, DA-008 from 20260225 execution) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.72 | 0.1440 | DA-006: `<project-required>` troubleshooting not first entry; Configuration not marked Required for Skills. DA-004: no routing decision guide before install method content. DA-005: "marketplace" undefined at first use. Three Major gaps leave users without needed information at critical moments. |
| Internal Consistency | 0.20 | 0.87 | 0.1740 | DA-008: "Recommended" heading + "may silently fail" caveat tension present; caveat is present but structurally de-emphasized. DA-001: `jerry@jerry-framework` presented as fixed string when the document itself discloses it may not match. No contradictions found at Critical severity. |
| Methodological Rigor | 0.20 | 0.81 | 0.1620 | DA-001: primary install path relies on unverified `@suffix` without requiring user verification of marketplace name. DA-005: "marketplace" used in three conflicting senses without definition. Decision guide absent (DA-004). Install path comparison not presented. |
| Evidence Quality | 0.15 | 0.82 | 0.1230 | SSH/HTTPS behavior correctly documented with explicit cause. Claude Code 1.0.33+ version requirement stated with version check command. `jerry-framework` source name sourced to `.claude-plugin/marketplace.json` but user cannot verify before running command. Evidence strong for technical claims; weakest for install command success guarantee. |
| Actionability | 0.15 | 0.76 | 0.1140 | DA-003: "you're riding," "you're in," "whole team rolling" at instructional moments reduce clarity for non-native speakers. DA-006: configuration "required for skills" framing absent, causing skips. DA-002: simplest install path (`--plugin-dir`) buried as "Quick test drive." Step-level instructions otherwise concrete and complete. |
| Traceability | 0.10 | 0.86 | 0.0860 | Navigation table covers all 14 sections with anchor links. External links present and well-formed (GitHub, astral.sh, docs.github.com, code.claude.com). `.claude-plugin/` manifest files named as source. No section cross-reference breaks detected. DA-001 weakens traceability: `jerry-framework` name attributed to manifest but unverifiable by reader. |
| **TOTAL** | **1.00** | | **0.8030** | |

**Arithmetic verification:** 0.1440 + 0.1740 + 0.1620 + 0.1230 + 0.1140 + 0.0860 = 0.8030. Rounded composite: **0.80**.

> **Rounding note:** Raw weighted sum is 0.8030. Standard two-decimal rounding yields 0.80. Reported composite: **0.80** (not 0.79 as stated in L0; corrected here — see Leniency Bias Check).

**Corrected composite: 0.80.** Verdict: REVISE (0.70–0.84 band). Gap to C4 threshold: -0.15.

---

## Corrected L0 Executive Summary

**Score:** 0.80/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.72)

**Iteration context:** This is the first scoring under C4 criticality. Prior iterations scored the document at C2. The C4 re-elevation introduces new findings (C4 S-002 execution, 2026-02-25) that were not present in C2 iterations. The prior C2 score of 0.89 (iter 4) reflects genuine improvements applied across four revisions; the C4 score of 0.80 reflects both the higher standard and eight new findings that are independent of the prior iteration history.

---

## Detailed Dimension Analysis

### Completeness (0.72/1.00)

**Evidence:**

The document covers: prerequisites (software, SSH, uv, version); three install methods with step-by-step instructions; hooks installation and capability matrix; configuration (project setup, `JERRY_PROJECT`); verification (plugin, hooks, skill test); skills list; developer setup; troubleshooting (SSH, plugin install, hooks, skills, project, Windows path); updating; uninstallation; getting help; license.

Coverage of the install workflow itself is thorough — SSH authentication cause and resolution, HTTPS alternative, `@suffix` pattern, scope selection, hook installation with uv, and platform-specific commands are all present.

**Gaps:**

1. **DA-006-20260225 (Major — open):** The `<project-required>` failure mode — the most statistically likely first-run failure for a user who installs successfully — is not the first troubleshooting entry. It appears as the fourth category (Project Issues) after GitHub Install Issues, Plugin Install Issues, and Hook Issues. A user whose install succeeded but skills do not work due to missing `JERRY_PROJECT` must read through three unrelated failure categories before finding the relevant entry. Additionally, the Configuration section heading at line 283 reads "### Project Setup" without the qualifier "Required for Skills" — the navigation table entry at line 20 reads "Project setup — required for skills to work" (this is an improvement over prior iterations), but the section heading itself is not self-descriptive at the point where users scan headings.

2. **DA-004-20260225 (Major — open):** No routing decision guide appears before the install method content. The "Which Install Method?" section (lines 50–61) provides a three-row decision table, which is a genuine improvement. However, the navigation table (lines 9–26) lists three separate install entries at equal weight without a structural differentiator for first-time users. The "Which Install Method?" section is the fifth entry in the navigation table — a user who scrolls to "Install from GitHub" directly never sees the routing guide. The guide exists but is not structurally enforced as a mandatory decision gate before method content.

3. **DA-005-20260225 (Major — open):** "Marketplace" is used at line 68 in a callout that defines it: "Claude Code uses the word 'marketplace' in its `/plugin marketplace` commands, but it's just the mechanism for registering plugin sources — think 'add a source' not 'browse a store.'" This is a substantive improvement — the word is now defined at first use. However, the definition appears in a blockquote callout after the section heading claims "Jerry is a community Claude Code plugin" (which implicitly references the "official" marketplace absent from the document). The sequence is: (a) Install from GitHub section opens claiming Jerry is "not on the official Anthropic marketplace," (b) then a callout defines what "marketplace" means in the `/plugin marketplace` context. A user reading the section heading before the callout encounters the word twice before the definition. The definition is present; its placement is slightly late. This is a Minor completeness gap in the context of DA-005, not a complete absence.

4. **DA-001-20260225 (Critical — open):** The primary install path at Step 2 presents `/plugin install jerry@jerry-framework` as a command with a fixed `@suffix`. The troubleshooting tip at line 96 instructs users to run `/plugin marketplace list` and use the name shown if the command fails — but this instruction is conditional on failure. A user who runs the command and it works (in the nominal case) never runs the verification step. The document discloses that the name may differ (line 481: "it may register differently in some environments") but structures this disclosure as a failure recovery action, not as a required pre-install verification. The completeness gap: the document does not tell users to verify the marketplace name before running the install command as a standard step.

**Improvement Path:**

- DA-006: Move `<project-required>` symptom to first position in Troubleshooting (one-line section reorder). Rename Configuration section heading to "Project Setup (Required for Skills)" — consistent with the navigation table entry. Two changes, minimal effort.
- DA-004: Add a sentence before the navigation table: "New to Jerry? Start with [Which Install Method?](#which-install-method) to pick the right path in under a minute." This routes users to the decision guide without requiring a structural reorder.
- DA-001: Move `/plugin marketplace list` from a conditional troubleshooting tip to a required Step 1b between Step 1 and Step 2 in the primary install path.
- DA-005: Minor — the definition callout is present; moving it to before the first use of "not on the official Anthropic marketplace" would close this gap.

---

### Internal Consistency (0.87/1.00)

**Evidence:**

The document's major consistency improvements from prior iterations hold:

- The Enable Hooks section heading ("Recommended") is followed immediately by the early access caveat callout at lines 132–134 (before the hooks detail sections). The caveat reads: "Early access caveat: Hook enforcement is under active development. Some hooks may have schema validation issues that cause them to fail silently (fail-open behavior — skills always work, but enforcement may not fire)." This positions the limitation before the feature description, which is the correct structural ordering per the DA-002 fix from iteration 4.

- The platform note at line 5 names specific Windows limitations: "Known Windows limitations: bootstrap uses junction points instead of symlinks, and paths in Claude Code commands must use forward slashes." Windows instructions and Windows limitations are now commensurate in specificity.

- The version requirement (Claude Code 1.0.33+) is stated in Prerequisites (line 36) with a check command (`claude --version`) and the implication that `/plugin` tabs require this version.

**Gaps:**

1. **DA-008-20260225 (Minor):** The Enable Hooks section heading at line 131 reads "## Enable Hooks (Recommended)". The early access caveat at lines 132–134 begins the section body. This is better than prior iterations (caveat is now near the top), but the section heading still leads with "Recommended" before the reader encounters "may silently fail." A reader scanning section headings in the navigation table sees "Enable Hooks (Recommended)" — the early-access qualification is not visible at that scanning level. This creates a mild tension: the navigation table says "Recommended," but clicking through reveals "some hooks may fail silently." The inconsistency is real but Minor: the caveat is present; the question is only whether it is visible before commitment.

2. **DA-001 consistency shadow:** The document presents `jerry@jerry-framework` as the install command (line 92), sources the name to the `.claude-plugin/` manifests (line 94), then discloses that it "may register differently in some environments" (line 481). These three statements together are consistent — but they are not co-located. The install command and the disclaimer appear 387 lines apart. A user who reads only the install section has an incomplete picture of command reliability. The troubleshooting section at line 481 accurately qualifies the claim, but co-location of the qualification with the command would improve consistency.

**Remaining strength:** No Major-severity contradictions found. Claims about SSH behavior, HTTPS alternatives, hook functionality (when working), verification steps, and platform-specific commands are internally coherent. The `code.claude.com` domain in the Prerequisites URL (line 36) correctly matches the user-provided context that this is the valid domain for Claude Code documentation.

**Improvement Path:**

DA-008: Update the navigation table entry from "Level up with session context and quality enforcement" to "Level up with session context and quality enforcement (early access — hooks may fail silently)" — or update the section heading to "Enable Hooks (Recommended — Early Access)." One-line change.

---

### Methodological Rigor (0.81/1.00)

**Evidence:**

The document follows a logical install methodology: prerequisites → method selection → primary install → hooks → capability matrix → alternatives → configuration → verification → usage → troubleshooting → updating → uninstallation. This is the correct order for an installation guide: prerequisites before instructions, method selection before method content, configuration before verification, troubleshooting after installation.

The three-path decision table in "Which Install Method?" (lines 54–61) correctly identifies when each method applies: internet + SSH → GitHub install; no SSH or locked network → Local Clone; quick test → Plugin Dir Flag. This is methodologically sound.

Platform-specific commands are provided for each major operating system at each step, which is methodologically rigorous for a cross-platform tool.

**Gaps:**

1. **DA-001-20260225 (Critical — open):** The primary install methodology requires the user to know the marketplace name before Step 2, but does not include a step that produces this knowledge. The methodology is: (Step 1) add marketplace source, (Step 2) install plugin using the source name. The gap is that Step 1 does not produce the source name as a documented output — the user must infer it is `jerry-framework` based on the command in Step 2. The `/plugin marketplace list` verification step exists only as a conditional failure recovery action. A methodologically complete install procedure would include: Step 1 → add source, Step 1b → verify source registration and note source name, Step 2 → install using the verified source name. This pattern is the established best practice for CLI-based package installation workflows (e.g., `brew tap` followed by `brew list --cask` before `brew install`).

2. **DA-005-20260225 (Major — partially addressed):** "Marketplace" is defined at line 68, but the definition does not clarify the relationship between the "official Anthropic registry" (implied at line 66 by the statement that Jerry is "not" on it) and the `/plugin marketplace` command (which registers sources, not browse-style marketplaces). The definition is present; the conceptual model it provides is accurate; the gap is that it does not resolve the asymmetry between "you add community plugins via the same mechanism as official plugins" — which would be the reassuring methodological statement a new user needs.

3. **DA-004-20260225 (Major — open):** The "Which Install Method?" section provides a decision table, which is methodologically correct. However, the decision table is not a decision gate — it is consultable but not required. The document's method does not structurally enforce consulting the decision table before entering a method section. This is a structural methodology gap: best-practice installation guides for multi-path tools (e.g., Docker's install documentation) present the decision gate as the entry point to all method content, not as a consultable supplement.

**Improvement Path:**

DA-001: Insert Step 1b. DA-004: Add navigation from the navigation table to "Which Install Method?" as a structural entry point. DA-005: One sentence: "Any GitHub repository with a `.claude-plugin/` directory can serve as a plugin source — Jerry uses this mechanism, not the official Anthropic catalog."

---

### Evidence Quality (0.82/1.00)

**Evidence supporting strong score:**

1. The SSH behavior is documented with specific cause and effect: "Claude Code clones the repository using SSH (`git@github.com:...`). Even though Jerry's repo is public, Claude Code's plugin system requires SSH access by default." This is specific, accurate technical evidence — it names the exact behavior (SSH clone of public repo), the exact error ("Permission denied (publickey)"), and the cause (plugin system default behavior). The user-provided context confirms this is accurate and corresponds to a known issue (GitHub issue #26588).

2. The HTTPS alternative is documented with the exact command form (`https://github.com/geekatron/jerry.git`) and an explanation: "clones over HTTPS, which works without SSH configuration." The `.git` suffix requirement is correctly included.

3. Version requirements are specific: "Claude Code 1.0.33+" with a check command (`claude --version`) and recovery action ("If `/plugin` is not recognized, update Claude Code first").

4. uv installation commands source directly to `astral.sh` with a security note explaining what the script does, alternative methods (pip, package manager), and a specific way to inspect before running.

5. The `code.claude.com` domain in the Prerequisites Claude Code URL (line 36: `https://code.claude.com/docs/en/quickstart`) matches the user-provided context that this is the correct domain.

**Gaps:**

1. **DA-001-20260225 (Critical — partially evidenced):** The `jerry@jerry-framework` command is sourced to "the repository's `.claude-plugin/` manifests" (line 94). This is honest attribution — the document does not claim the name is guaranteed; it names the source. However, a first-time user cannot verify this source before running the command. The evidence claim is: "install using this command, where the name comes from the manifests." The evidentiary gap is that the user cannot independently verify the manifests contain `jerry-framework` without inspecting the repository directly. The evidence is honest but thin at the point of use.

2. **DA-002-20260225 (Major — not addressed):** The document asserts the GitHub install is "The main line" (navigation table, line 15) without comparative evidence that it is the simpler or preferred path. The `--plugin-dir` path (lines 264–278) is objectively fewer steps (2 vs 3–5) and has fewer conceptual prerequisites (no marketplace abstraction). The document does not demonstrate why the marketplace install is "The main line" for most users — the choice is asserted, not evidenced. The user-provided context contains no instruction to change this framing, so it should be evaluated as-is.

**Improvement Path:**

DA-001: A single sentence in the install step sourcing the expectation: "The marketplace name is defined in the repository's `.claude-plugin/marketplace.json` file; you can inspect it at `https://github.com/geekatron/jerry/blob/main/.claude-plugin/marketplace.json` if you want to verify it before running the command." This converts an untraceable claim into an externally verifiable one.

---

### Actionability (0.76/1.00)

**Evidence of strong actionability:**

- Each install method provides numbered steps with exact commands, platform variants, and recovery actions. No step leaves the user without a next action.
- Troubleshooting entries follow a Symptom/Cause/Fix structure that is highly actionable.
- The Verification section provides three independent checks (plugin tab, hooks tag, skill test) — each check has a specific expected output and a recovery action if the expected output is absent.
- The uv install section includes OS-specific commands, a restart reminder, and a verification command.
- Configuration provides complete persistent setup instructions for both macOS/Linux and Windows.

**Gaps:**

1. **DA-003-20260225 (Major — open):** McConkey voice at step-level instructional moments creates clarity barriers:
   - Line 66: "Two commands and you're riding." — instructional conclusion that embeds the outcome in a sports metaphor. A non-native speaker parsing "you're riding" as "the install is complete" must interpret the idiom correctly.
   - Line 104: "That's your signal — you're in." — after the plugin verification step, this is the confirmation statement. "You're in" is not a declarative technical confirmation.
   - Line 351: "You're shredding." — after the skill test, this serves as the success confirmation.
   - Line 116: "Use **User** for personal use. Use **Project** when you want your whole team rolling with Jerry" — "rolling with Jerry" is an idiom that conveys nothing technical about the scope mechanism.

   These idioms appear at exactly the moments when users need the most precise information: when they need to know whether their install succeeded. Replacing them with declarative confirmations ("Installation complete." / "Plugin successfully installed." / "Jerry is operational.") would increase actionability without removing voice from section introductions.

2. **DA-006-20260225 (Major — open):** The Configuration section heading at line 283 is "### Project Setup" — without "Required for Skills" in the heading. A user who reads the navigation table will see "Project setup — required for skills to work" (line 20, navigation table) and may correctly recognize the section as required. However, a user who navigates the document by heading (mobile, screen reader, or fast scroll) sees only "Project Setup" — a label that does not communicate consequence. The actionability failure: a user cannot correctly prioritize Configuration without reading the navigation table description. The heading itself is insufficient.

3. **DA-002-20260225 (Major — open):** The simplest install path (`--plugin-dir`) is positioned as "Quick test drive" in both the navigation table (line 19) and the "Which Install Method?" decision table (line 58). This framing actively discourages users from using the simplest path by labeling it as non-committal. For a user who wants persistent install, the `--plugin-dir` method is unsuitable — but for a new user evaluating Jerry, it is the lowest-friction entry point. The actionability gap: the document frames the simpler path as a pre-commitment trial, not as a valid choice for new users who want to start working.

**Improvement Path:**

DA-003: Replace step-level idioms with declarative confirmations. Voice elements in section headings and transition paragraphs can remain. DA-006: Update the Configuration section heading to "### Project Setup (Required for Skills)." DA-002: This is a structural judgment call — not addressing it accepts the current framing.

---

### Traceability (0.86/1.00)

**Evidence:**

- Navigation table at lines 9–29 covers all 14 major sections with anchor links. All anchor links are valid (section headings present and correctly cased).
- External links are specific and contextually appropriate: GitHub SSH key guide (docs.github.com), uv documentation (docs.astral.sh), Claude Code quickstart (code.claude.com/docs/en/quickstart), Claude Code plugin docs (code.claude.com/docs/en/discover-plugins), CONTRIBUTING.md (github.com/geekatron/jerry/blob/main/CONTRIBUTING.md).
- The `code.claude.com` domain used throughout matches the user-provided context that this is the correct domain for Claude Code documentation.
- The `.claude-plugin/` manifest files are named as the source of the plugin name and marketplace name (line 94).
- Cross-references within the document are consistently used: the troubleshooting entries link back to the relevant install sections (e.g., line 453: "[Local Clone](#alternative-local-clone) method").

**Gaps:**

1. **DA-001 traceability shadow:** The `jerry-framework` marketplace name is traced to `.claude-plugin/marketplace.json` (line 94), but no link to the actual file is provided. A user who wants to verify the name before running the install command cannot follow the trace without independently navigating to the GitHub repository. This is a Minor traceability gap — the attribution is present, but not traversable.

2. The Prerequisites table links to `https://code.claude.com/docs/en/quickstart` for Claude Code. This URL cannot be verified by the scorer, but the domain matches the user-provided context. Accepted as accurate.

3. `CONTRIBUTING.md` is linked from Developer Setup at line 403 (`https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md`). This is an external URL that cannot be verified in-session. It has been noted as an unverified external link across all four prior iterations. This is an ongoing Minor traceability gap.

**Improvement Path:**

DA-001: Add a direct URL to the manifest file: "You can inspect the source name at `https://github.com/geekatron/jerry/blob/main/.claude-plugin/marketplace.json` before running the install command." This converts an attributed claim into a traversable claim.

---

## C4 Findings Register

| ID | Severity | Dimension(s) | Status | Evidence in Current Doc |
|----|----------|-------------|--------|------------------------|
| DA-001-20260225 | Critical | Completeness, Methodological Rigor, Evidence Quality | Open | `/plugin install jerry@jerry-framework` presented as fixed string (line 92). `/plugin marketplace list` is conditional troubleshooting tip (line 96), not required Step 1b. `jerry-framework` traced to manifests (line 94) but not linked for verification. |
| DA-002-20260225 | Major | Actionability, Evidence Quality | Open | `--plugin-dir` labeled "Quick test drive" in nav table (line 19) and decision table (line 58). GitHub install labeled "The main line" without comparative evidence. |
| DA-003-20260225 | Major | Actionability | Open | "Two commands and you're riding" (line 66), "That's your signal — you're in" (line 104), "You're shredding" (line 351), "rolling with Jerry" (line 116) all present as step-level instructional language. |
| DA-004-20260225 | Major | Completeness, Methodological Rigor | Partially addressed | "Which Install Method?" decision table present (lines 50–61). Navigation table does not route users to the decision guide as mandatory first step. |
| DA-005-20260225 | Major | Completeness, Methodological Rigor | Partially addressed | "Marketplace" defined in callout at line 68: "think 'add a source' not 'browse a store.'" Definition present but follows (not precedes) the first use of "not on the official Anthropic marketplace" in the same section. |
| DA-006-20260225 | Major | Completeness, Actionability | Partially addressed | Nav table entry reads "Project setup — required for skills to work" (line 20). Section heading reads "### Project Setup" (line 283) without "Required for Skills." `<project-required>` entry is fourth troubleshooting category (lines 527–537), not first. |
| DA-007-20260225 | Minor | Completeness | Partially addressed | Document is 622 lines (measured by line count). Developer Setup section (lines 399–424) remains in the document. Using Jerry section (lines 363–396) remains in the document. Both could move to CONTRIBUTING.md and Getting Started runbook respectively. |
| DA-008-20260225 | Minor | Internal Consistency | Partially addressed | Early access caveat (lines 132–134) now appears early in the Enable Hooks section, before the "What hooks give you" table. Section heading still reads "Recommended" without "Early Access" qualifier. Navigation table entry does not signal early-access status. |

---

## Improvement Recommendations

Priority-ordered by expected composite score impact for C4 acceptance at 0.95:

| Priority | Finding | Dimension(s) | Current | Target | Recommendation |
|----------|---------|-------------|---------|--------|----------------|
| 1 | DA-001-20260225: marketplace list as required step | Completeness (0.72) + Methodological Rigor (0.81) | 0.72 / 0.81 | 0.85 / 0.90 | Insert Step 1b in "Install from GitHub": "Run `/plugin marketplace list` to confirm the source was registered and note its name. Look for `jerry-framework` in the list." Make Step 2 read: "Install using the name from the list: `/plugin install jerry@<name-from-list>` (expected: `jerry@jerry-framework`)." |
| 2 | DA-006-20260225: configuration framing and troubleshooting order | Completeness (0.72) + Actionability (0.76) | 0.72 / 0.76 | 0.82 / 0.85 | (a) Rename "### Project Setup" to "### Project Setup (Required for Skills)". (b) Move `<project-required>` troubleshooting entry to first position in the Troubleshooting section, above SSH Authentication Issues. |
| 3 | DA-003-20260225: McConkey voice at instructional moments | Actionability (0.76) | 0.76 | 0.85 | Replace step-level idioms: "Two commands and you're riding" → "Installation complete in two commands." / "That's your signal — you're in" → "If `jerry` appears in the Installed tab, installation succeeded." / "You're shredding" → "Jerry is now fully operational." / "rolling with Jerry" → "using Jerry." Preserve voice in section introductions. |
| 4 | DA-008-20260225: early access caveat at heading level | Internal Consistency (0.87) | 0.87 | 0.92 | Update Enable Hooks section heading to "## Enable Hooks (Recommended — Early Access)". Update navigation table entry to match. |
| 5 | DA-005-20260225: marketplace definition placement | Completeness (0.72) + Methodological Rigor (0.81) | minor | +0.02 | Move the "What does marketplace mean here?" callout to appear before the statement that Jerry is "not on the official Anthropic marketplace" — or rephrase that statement to read "not in the official Anthropic plugin catalog" to avoid the word collision with `/plugin marketplace`. |
| 6 | DA-001: manifest link for traceability | Evidence Quality (0.82) + Traceability (0.86) | 0.82 / 0.86 | 0.87 / 0.90 | Add direct URL to manifest: "You can inspect the marketplace name at `https://github.com/geekatron/jerry/blob/main/.claude-plugin/marketplace.json` to verify before running the command." |
| 7 | DA-002-20260225: install method framing | Actionability (0.76) + Evidence Quality (0.82) | 0.76 / 0.82 | 0.82 / 0.87 | Restructure navigation table and decision table to surface `--plugin-dir` as "Try Jerry (no setup required)" and marketplace install as "Persistent Install." Provide a one-sentence rationale for when marketplace install is the right choice. |

**Projected impact for iteration 2 (addressing P1–P4):** Addressing recommendations 1–4 is projected to lift Completeness to ~0.85, Methodological Rigor to ~0.89, Actionability to ~0.85, and Internal Consistency to ~0.90, yielding a composite of approximately 0.87–0.88 (still REVISE). All seven recommendations are needed to reach 0.95 (C4 threshold). This indicates 2–3 additional revision iterations are required.

---

## Leniency Bias Check

- [x] Each dimension scored independently — all six dimension scores assigned before computing weighted composite; Completeness scored at 0.72 (not 0.80) because three Major and one Critical gap leave users without required information at critical moments; Actionability scored at 0.76 (not 0.82) because idioms at instructional moments and missing "Required for Skills" framing are genuine barriers, not minor polish issues
- [x] Evidence documented for each score — specific line citations from current `docs/INSTALLATION.md` confirmed by direct read for each gap identified; all cited lines verified against the Read output
- [x] Uncertain scores resolved downward — Internal Consistency 0.87 (not 0.90) because the "Recommended" heading without early-access qualifier is a real inconsistency; Evidence Quality 0.82 (not 0.87) because the `@suffix` sourced to unverifiable manifests is a genuine evidentiary gap; Traceability 0.86 (not 0.90) because CONTRIBUTING.md external link and manifest URL remain unlinked
- [x] C4 elevation calibration applied — this is the first C4 scoring of this document; prior C2 score of 0.89 (iter 4) correctly reflects improvements applied in four iterations, but C4 introduces eight new findings not present in C2 review; the delta from 0.89 (C2) to 0.80 (C4) reflects the combined effect of higher standard + new findings, not score regression
- [x] Arithmetic self-checked — L0 stated 0.79, arithmetic yields 0.8030, rounded composite = 0.80; corrected in L0 and Score Summary sections; error was pre-arithmetic estimate that was not recalculated after individual dimension scores were assigned
- [x] No dimension scored above 0.87 without specific justification — Internal Consistency at 0.87 is the highest score; justified by: (a) DA-002 structural fix from iter 4 holds (caveat co-located with Enable Hooks headline), (b) Windows limitations are specifically named, (c) version requirement is specific, (d) only Minor inconsistency remaining (DA-008 heading qualifier)
- [x] First-draft calibration adjusted for revision history — this is not a first draft; it is iteration 5 of a document that has undergone four prior revisions. The prior iterations fixed genuine defects. The document is not a first draft at 0.65–0.80 — it is a substantially revised document with residual C4 findings. 0.80 is calibrated for a fourth-revision document that meets C2 quality but has unresolved C4 findings.
- [x] DA-001-20260225 assessed as Critical — the absence of `/plugin marketplace list` as a required step (not a conditional tip) is a genuine structural gap in the primary install methodology; it is not resolved by the troubleshooting entry because troubleshooting entries are post-failure, not pre-execution guidance
- [x] C4 threshold noted at 0.95 (not H-13 standard 0.92) — per user specification; this gap (-0.15) is material and requires multiple revision iterations

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.80
threshold: 0.95  # C4 user-specified (higher than H-13 standard 0.92)
weakest_dimension: Completeness
weakest_score: 0.72
critical_findings_count: 1  # DA-001-20260225: marketplace list not required step
major_findings_count: 5  # DA-002 through DA-006 from 20260225 C4 execution
minor_findings_count: 2  # DA-007, DA-008 from 20260225 C4 execution
iteration: 1  # First scoring under C4 criticality; prior C2 scores: 0.74, 0.84, 0.88, 0.89
gap_to_threshold: -0.15
improvement_recommendations:
  - "DA-001: Insert Step 1b — require /plugin marketplace list before Step 2; show jerry@jerry-framework as example not fixed string"
  - "DA-006: Rename Configuration section heading to 'Project Setup (Required for Skills)'; move project-required troubleshooting to first position"
  - "DA-003: Replace step-level McConkey idioms with declarative confirmations; preserve voice in section introductions"
  - "DA-008: Update Enable Hooks heading to 'Enable Hooks (Recommended — Early Access)'; propagate to nav table"
  - "DA-005: Move marketplace definition callout before first use of 'not on the official Anthropic marketplace'"
  - "DA-001 traceability: Add direct URL to .claude-plugin/marketplace.json for user verification"
  - "DA-002: Restructure install method framing to surface --plugin-dir as zero-friction entry point"
```

---

*Strategy: S-014 LLM-as-Judge*
*Agent: adv-scorer v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-02-25*
*Deliverable: `docs/INSTALLATION.md` (current, post-iteration-4 revision)*
*Criticality: C4 (Critical — public OSS installation guide)*
*Prior iterations: C2 scoring at 0.74 (iter 1), 0.84 (iter 2), 0.88 (iter 3), 0.89 (iter 4)*
*Strategy findings incorporated: C4 S-002 Devil's Advocate (2026-02-25), 8 findings*

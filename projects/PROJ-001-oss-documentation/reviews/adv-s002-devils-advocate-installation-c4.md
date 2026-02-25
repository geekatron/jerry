# Strategy Execution Report: Devil's Advocate

## Execution Context
- **Strategy:** S-002 (Devil's Advocate)
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md`
- **Deliverable:** `docs/INSTALLATION.md`
- **Executed:** 2026-02-25T00:00:00Z
- **Criticality:** C4 (Critical)
- **H-16 Compliance:** S-003 Steelman applied 2026-02-18 — confirmed at `docs/reviews/adv-s003-steelman-install-docs.md`
- **Prior Strategy Output:** `docs/reviews/adv-s002-devils-advocate-install-docs.md` (C2 execution, 2026-02-18, prior document version)

---

## Step 1: Advocate Role Assumption

**Deliverable challenged:** `docs/INSTALLATION.md` (current version, post-revision)
**Criticality level:** C4 (Critical) — public-facing OSS documentation, irreversible once distributed
**H-16 verified:** S-003 Steelman output exists at `docs/reviews/adv-s003-steelman-install-docs.md`, executed 2026-02-18 against the installation documentation set including `docs/INSTALLATION.md`.
**Role assumed:** Argue the strongest possible case against the document's installation approach, voice choices, structural decisions, and implicit assumptions. Argue as a skeptical new user encountering this document for the first time — with no prior knowledge of Jerry, Claude Code plugin mechanics, or the McConkey persona.

---

## Step 2: Assumptions Extracted and Challenged

| Assumption | Type | Challenge |
|------------|------|-----------|
| "GitHub install" is the right primary path | Implicit structural | `--plugin-dir` requires fewer steps and no marketplace registration |
| All users know what "marketplace" means in Claude Code context | Implicit knowledge | "Marketplace" implies an app store with curation; the document uses it for a custom registry |
| The McConkey voice will read as friendly rather than opaque | Implicit audience | Non-native English speakers, new users, and professional technical readers may not share the cultural reference |
| Three install paths is the right number to offer | Implicit design | Multiple paths create decision paralysis and inflate apparent complexity |
| The `@suffix` pattern is explained sufficiently | Implicit | The `jerry@jerry-framework` pattern is non-obvious; the explanation is deferred to a tip box |
| Troubleshooting covers the most likely failure modes | Implicit coverage | The most common plugin install failures are version mismatch and network proxy — one is mentioned, one is not adequately covered |
| Users will understand that "without uv" means no guardrails | Implicit consequence | The capability matrix communicates this, but users scanning headings may skip the Enable Hooks section entirely |
| "You're riding" and "you're in" land as warm/welcoming | Implicit register | Sports/action idioms assume shared cultural context that not all developers have |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001-20260225 | Critical | Primary install path requires marketplace mechanics that are nowhere explained in Claude Code docs | Install from GitHub |
| DA-002-20260225 | Major | `--plugin-dir` flag is a simpler path for new users and should be primary, not "Alternative" | Alternative: Plugin Dir Flag |
| DA-003-20260225 | Major | McConkey voice creates comprehension barriers for non-native speakers and new technical users | Document-wide |
| DA-004-20260225 | Major | Three install alternatives create decision paralysis for first-time users | Document structure |
| DA-005-20260225 | Major | "Marketplace" terminology is borrowed from consumer app stores but has different semantics here | Install from GitHub |
| DA-006-20260225 | Major | Troubleshooting section omits the most statistically likely failure mode: JERRY_PROJECT not set after install | Troubleshooting |
| DA-007-20260225 | Minor | Document length (607 lines) exceeds single-session reading budget for an install guide | Document-wide |
| DA-008-20260225 | Minor | The hooks "early access caveat" buried at line 146 contradicts the "Recommended" section heading | Enable Hooks |

---

## Detailed Findings

### DA-001-20260225: Primary Install Path Depends on Undocumented Marketplace Mechanics [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `docs/INSTALLATION.md`, Install from GitHub section (lines 45–105) |
| **Strategy Step** | Step 3 — Unstated assumptions, Unaddressed risks |

**Evidence:**
> "Step 1: Add the Jerry repository as a plugin source"
> ```
> /plugin marketplace add geekatron/jerry
> ```
> "This tells Claude Code where to find Jerry. The `geekatron/jerry` shorthand points directly to the GitHub repository. Claude Code clones the plugin catalog from the repo — nothing is installed yet."
> (INSTALLATION.md, lines 53–57)

> "Step 2: Install the plugin"
> ```
> /plugin install jerry@jerry-framework
> ```
> "This downloads and activates Jerry's skills, agents, and hooks. The format is `<plugin-name>@<marketplace-name>` — `jerry` is the plugin name (defined in the repo's `.claude-plugin/plugin.json`) and `jerry-framework` is the marketplace name (defined in `.claude-plugin/marketplace.json`)."
> (INSTALLATION.md, lines 62–67)

**Analysis:**
The primary install path is built on a two-step marketplace registration pattern that is not documented by Anthropic or explained in standard Claude Code onboarding. The document describes the mechanics in its own words ("the `geekatron/jerry` shorthand points to the GitHub repository"; "the format is `<plugin-name>@<marketplace-name>`"), but the structural claim depends on three unverified facts:

1. **`/plugin marketplace add geekatron/jerry` uses an undocumented shorthand.** The document claims this shorthand works, notes that the full URL also works, but does not cite Anthropic's documentation for either form. A user who reads the Claude Code docs independently will not find documentation of the `owner/repo` shorthand form, and if the behavior changes or the shorthand is version-dependent, users will hit failures with no official documentation to reference.

2. **The `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` files are cited as the source of the plugin name and marketplace name, but the user cannot verify this without inspecting the repository.** A new user reading Step 2 cannot independently verify that `jerry-framework` is the correct `@suffix` without running `/plugin marketplace list` — which is mentioned only as a troubleshooting tip (line 69–70), not as a required pre-install verification. The previous C2 S-002 execution (DA-003-20260218) flagged this same structural issue and it remains unresolved in the current version.

3. **The "Verify the marketplace name" tip box (lines 69–70) exists precisely because the marketplace name might not be `jerry-framework` in all cases** — meaning the document itself discloses that the primary install command may fail, without structurally integrating this possibility into the install steps. The failure mode is mentioned as a troubleshooting tip but not surfaced as a first-class install step.

The counter-argument: the primary install path's correctness depends entirely on the user's Claude Code version recognizing the `geekatron/jerry` shorthand, on the `.claude-plugin/marketplace.json` defining `jerry-framework` as the marketplace name, and on the user's environment not having a naming collision. None of these are verifiable by a first-time user reading the document. The document asks the user to trust a two-step command sequence that references internal plugin manifests they cannot inspect before running the commands.

**Impact:** If the `geekatron/jerry` shorthand is not universally supported, or if the marketplace name differs from `jerry-framework` in some environments or versions, the primary install path fails silently with "plugin not found" — sending users to a troubleshooting section that already presupposes the install failed in a predictable way. The C2 execution identified this as Critical; the C4 elevation makes it more severe because this documentation will be the definitive public reference after OSS release.

**Recommendation:** Integrate `/plugin marketplace list` as a required verification step between Step 1 and Step 2 in the primary install path. Reframe Step 2 as: "Run `/plugin marketplace list` to confirm the marketplace was added and note its name. Then install using that name: `/plugin install jerry@<name-from-list>`." This converts an undocumented assumption into a user-verified fact and eliminates the entire class of "plugin not found" failures caused by marketplace name mismatch.

**Acceptance Criteria:** The primary install path instructs users to run `/plugin marketplace list` and use the name shown in the output as the `@suffix`. The `jerry@jerry-framework` command is shown as an example, not as a fixed string.

---

### DA-002-20260225: `--plugin-dir` Is Simpler for New Users and Should Not Be "Alternative" [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Alternative: Plugin Dir Flag section (lines 251–266) |
| **Strategy Step** | Step 3 — Alternative interpretations, Logical flaws |

**Evidence:**
> "For a quick test drive without any marketplace setup, use Claude Code's `--plugin-dir` flag. This loads Jerry directly from a local directory:"
> ```bash
> git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
> claude --plugin-dir ~/plugins/jerry
> ```
> "This is great for trying Jerry out before committing to a full install. Skills are available immediately — no `/plugin install` needed."
> (INSTALLATION.md, lines 253–263)

> "Note: The `--plugin-dir` flag loads the plugin for that session only. It does not persist across sessions."
> (INSTALLATION.md, line 264)

Also: The document's navigation table lists "Install from GitHub" as "The main line — two commands, no clone needed" and positions `--plugin-dir` as an alternative for "Quick test drive — no marketplace setup."
(INSTALLATION.md, lines 14, 18)

**Analysis:**
The document frames `--plugin-dir` as a "quick test drive" that requires "committing to a full install" before it becomes the real install. But when the steps are compared objectively:

- **`--plugin-dir` path:** (1) git clone one command, (2) `claude --plugin-dir ~/plugins/jerry` — two steps total, requires only Git. Skills available immediately in that session.
- **Primary GitHub install path:** (1) `/plugin marketplace add geekatron/jerry`, (2) verify marketplace name with `/plugin marketplace list`, (3) `/plugin install jerry@jerry-framework`, (4) verify with `/plugin` > Installed tab, (5) optionally install uv for hooks. Three to five steps, requires understanding the marketplace abstraction.

The `--plugin-dir` path is objectively fewer steps and requires less conceptual overhead. Its only disadvantage — non-persistence across sessions — is labeled as a reason it is not the "primary" path. But for a new user evaluating Jerry for the first time, non-persistence is not a disadvantage: it is exactly what they want. They want to try Jerry before committing. The document frames the trial path as inferior when it may actually be the more appropriate onboarding path.

The counter-argument: the document prioritizes the "full install" path as the main line because it reflects the maintainer's preference for committed users, not because it reflects new user needs. A new user who follows the "main line" must understand marketplace registration, plugin manifests, and the `@suffix` pattern before seeing any Jerry output. A new user who runs `claude --plugin-dir ~/plugins/jerry` sees Jerry working in 2 minutes with one additional command.

Additionally, the `--plugin-dir` section is positioned after two sections (Local Clone, which requires understanding the same marketplace mechanics) that are also "alternatives." The document's structure buries the simplest path in the fourth major section.

**Impact:** New users who follow the "main line" will encounter more friction than necessary, and some fraction will abandon before completing setup. The document's labeling of the simpler path as "alternative" directs users toward complexity.

**Recommendation:** Promote `--plugin-dir` to the first install option shown, labeled as "Quickstart — Try Jerry Now (2 minutes)." Present it as the zero-friction onboarding path. Move the marketplace install path to "Persistent Install" for users who want Jerry available across all sessions. This reordering matches user needs to method complexity.

**Acceptance Criteria:** The document presents `--plugin-dir` as the first or primary recommended path for new users, with the marketplace install as the follow-on step for users who want persistence.

---

### DA-003-20260225: McConkey Voice Creates Comprehension Barriers for Non-Native Speakers and New Technical Users [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Document-wide — multiple locations |
| **Strategy Step** | Step 3 — Unaddressed risks, Alternative interpretations |

**Evidence:**
> "Your AI coding partner just got guardrails, knowledge accrual, and a whole crew of specialized agents. Let's get you set up."
> (INSTALLATION.md, line 3, document tagline)

> "Two commands and you're riding."
> (INSTALLATION.md, line 47, Install from GitHub section)

> "That's your confirmation — you're in."
> (INSTALLATION.md, line 83, after skill test)

> "Use **User** for personal use. Use **Project** when you want your whole team rolling with Jerry..."
> (INSTALLATION.md, line 95, Installation Scope section)

> "That's it. You do **not** need Git, Python, or a local clone to install Jerry's skills. Claude Code handles the rest."
> (INSTALLATION.md, lines 37–38, Prerequisites section)

**Analysis:**
The document uses a distinctly casual, sports-inflected American idiom voice throughout. Phrases like "you're riding," "you're in," "rolling with Jerry," and "whole crew" are metaphors drawn from action sports and American casual speech. The document is aimed at software developers globally — a demographic that skews toward non-native English speakers (the majority of the world's software developers) and includes many users for whom casual American idioms are not transparent.

The counter-argument builds on three distinct failure modes:

1. **Comprehension barrier for non-native speakers.** "Two commands and you're riding" does not communicate a technical fact. A developer for whom English is a third language who reads installation documentation for a mission-critical tool may not parse "you're riding" as "the install is complete." Technical documentation in this genre (e.g., homebrew.sh, pip, npm) uses declarative sentences: "Jerry is now installed." The McConkey voice substitutes colorful phrasing for informational clarity at the moments users most need certainty.

2. **Credibility gap for new technical users.** The document is the first touchpoint for a developer who has never heard of Jerry. First-time readers calibrate whether a tool is serious by the register of its documentation. Phrases like "a whole crew of specialized agents" and "you're in" carry a casual register that may cause enterprise developers or security-conscious teams to underestimate the framework's rigor. The framework itself is genuinely rigorous (S-003 Steelman established this) — but the voice does not signal that rigor.

3. **Inconsistency of register across the document.** The tagline is casual ("whole crew"), but the Capability Matrix table, the hooks enforcement layer description, and the troubleshooting section are formal and technical. A reader encounters "you're in" in the main install section and then "PreToolUse | AST-based validation before tool calls execute (L3 enforcement)" in the hooks table. The register shift is jarring and may cause readers to trust different sections differently.

The counter-argument is not that the voice should be eliminated — S-003 found it to be one of the document's strengths when applied to the right sections. The counter-argument is that the voice is being applied indiscriminately to instructional content (install steps, capability claims) where informational precision should dominate.

**Impact:** Non-native speakers who do not parse the idioms will complete the install steps mechanically but miss the contextual signals embedded in the casual phrasing. Professional audiences (enterprise IT, security teams) may dismiss the documentation before completing the install. The framework's credibility as a quality-enforcement tool is undermined by documentation that signals low-rigor communication standards.

**Recommendation:** Preserve the McConkey voice for the document's section introductions and transition sentences, but replace it with declarative technical language at the instructional level. Specifically: replace "Two commands and you're riding" with "Installation complete in two commands." Replace "That's your confirmation — you're in" with "If `jerry` appears in the list, installation succeeded." Replace "a whole crew" with "a set of." This preserves voice character at the section level while ensuring instructional clarity at the step level.

**Acceptance Criteria:** All step-level instructions (numbered steps, verification procedures, troubleshooting steps) use declarative technical language. Voice elements are present in section introductions and transitions but not in instructional content.

---

### DA-004-20260225: Three Install Alternatives Create Decision Paralysis for First-Time Users [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Navigation table and document structure |
| **Strategy Step** | Step 2 — What if this assumption is wrong?; Step 3 — Unaddressed risks |

**Evidence:**
Navigation table (lines 9–26) presents:
> "| [Install from GitHub](#install-from-github) | The main line — two commands, no clone needed |"
> "| [Alternative: Local Clone](#alternative-local-clone) | For offline use, version pinning, or locked-down networks |"
> "| [Alternative: Plugin Dir Flag](#alternative-plugin-dir-flag) | Quick test drive — no marketplace setup |"

The document contains 607 lines with 14 navigation sections. The three install methods appear across lines 45–266 — more than 220 lines of install-path content before reaching Configuration.

**Analysis:**
A first-time user opens this document to answer one question: "How do I install Jerry?" The navigation table presents three install methods in 14 total sections. The primary install is labeled "The main line" — a confident but informal signal that does not explain under what conditions a user should consider the alternatives.

The counter-argument: presenting three install paths without a structured decision tree causes a specific cognitive failure mode called "choice overload." Research in decision science (Iyengar and Lepper, 2000; Barry Schwartz, "The Paradox of Choice") consistently shows that increasing optionality past 3–5 equivalent choices reduces completion rates. In this case, the user does not need to choose — they need to be told which method to use. The document labels one path "The main line" but then devotes equal visual weight to two alternatives before the user has completed their first install.

The specific structural problem: the three paths are not mutually exclusive in the navigation table — a reader who scans the table sees: "main line → local clone → plugin dir flag" without clear criteria for when each applies. The descriptions are use-case-specific ("offline use, version pinning"), but the typical new user has none of those needs — they should never need to read past the first install section. Yet the document's structure does not communicate this with enough force. "The main line" is a marketing phrase, not a routing instruction.

Additionally, the "Alternative: Plugin Dir Flag" section contains a clone step (`git clone https://github.com/geekatron/jerry.git ~/plugins/jerry`) that is identical to the first step of the "Alternative: Local Clone" section. A user who reads both sections will encounter the same command appearing in two different contexts with different framing, creating confusion about whether they are the same operation.

**Impact:** New users who scan the navigation table and read about three install methods before attempting any of them will either (a) spend time evaluating which to choose (decision overhead), (b) choose the wrong one for their context, or (c) abandon the install entirely because the surface complexity signal exceeds their perceived effort budget.

**Recommendation:** Restructure the install section with a single entry point that routes users: "How do you want to install Jerry?" with three options and one click to the appropriate section. Or: collapse the navigation table install entries into a single "Installation" entry with a sub-table decision guide at the top of the Install section. The decision guide should be three rows: "Quick try (no persistence)" → `--plugin-dir`, "Personal persistent install" → GitHub method, "Offline/version-pinned" → Local Clone.

**Acceptance Criteria:** A user who reads only the first install section makes no install decision — they are routed to their section immediately by a decision guide. The two "alternative" sections are not visible at the navigation table level until the user has been routed to them.

---

### DA-005-20260225: "Marketplace" Terminology Assumes Claude Code Mental Model That New Users Do Not Have [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Install from GitHub section; Prerequisites section |
| **Strategy Step** | Step 2 — Implicit assumptions; Step 3 — Alternative interpretations |

**Evidence:**
> "Jerry is a **community Claude Code plugin** hosted on GitHub. It is **not** on the official Anthropic marketplace — you install it directly from the GitHub repository. Claude Code's plugin system supports this natively. Two commands and you're riding."
> (INSTALLATION.md, lines 47–48)

> "Step 1: Add the Jerry repository as a plugin source"
> `/plugin marketplace add geekatron/jerry`
> "This tells Claude Code where to find Jerry. The `geekatron/jerry` shorthand points directly to the GitHub repository. Claude Code clones the plugin catalog from the repo — nothing is installed yet."
> (INSTALLATION.md, lines 49–57)

> "| Software | Required? | Purpose |"
> "| [Claude Code](https://docs.claude.com/en/docs/claude-code) 1.0.33+ | **Yes** | The AI coding assistant Jerry extends |"
> (INSTALLATION.md, Prerequisites table, lines 32–34)

**Analysis:**
The document uses the term "marketplace" in four distinct senses within five lines:

1. The "official Anthropic marketplace" (an implicit curation platform for vetted plugins)
2. "community Claude Code plugin" (not on the official marketplace)
3. `/plugin marketplace add` (a CLI subcommand)
4. "marketplace name" (a string derived from the plugin manifest used as an `@suffix`)

A new user encountering "marketplace" for the first time assumes the consumer-app-store definition: a curated repository operated by a vendor. The document immediately subverts this expectation ("It is **not** on the official Anthropic marketplace"), then proceeds to use "marketplace" as the name of the CLI command that registers the plugin source. The same word now means: (a) the official app store the plugin is NOT on, and (b) the CLI mechanism used to register plugin sources.

The counter-argument: "marketplace" in the context of `/plugin marketplace add` is Claude Code's own terminology for its plugin registration system — the document did not choose this word. But the document's framing compounds the confusion: it opens by distinguishing the "official marketplace" from the plugin's home on GitHub, then asks the user to run a command that starts with `/plugin marketplace`. A reader who carries the "official marketplace" mental model will not understand why the command to install a non-marketplace plugin uses "marketplace."

Furthermore, the document does not define what "marketplace" means in the `/plugin marketplace` context at the moment the user first needs it. The explanation in the document's own voice ("Claude Code clones the plugin catalog from the repo") describes what the command does, but the name "marketplace" still implies a different concept. The S-003 Steelman identified SM-004 (two-step install pattern unexplained) — but the underlying problem is semantic, not just procedural.

**Impact:** New users will be confused by the "not on the marketplace but you use `/plugin marketplace`" tension and may misinterpret the install steps as requiring official marketplace registration. This confusion is most likely to surface as failed attempts to find Jerry in a marketplace browse interface before reading the install instructions.

**Recommendation:** At the first use of "marketplace" in the install instructions, add a one-sentence definition: "In Claude Code, a 'marketplace' is a registered source of plugins — it can be the official Anthropic registry or any GitHub repository that follows the plugin format." This converts a borrowed term with conflicting connotations into a document-defined term with a clear meaning.

**Acceptance Criteria:** The document defines "marketplace" in the context of Claude Code's plugin system at the first point of use. The distinction between the official Anthropic marketplace and community plugin sources is explained without using "marketplace" to mean two different things in adjacent sentences.

---

### DA-006-20260225: Troubleshooting Section Omits the Most Likely Post-Install Failure Mode [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `docs/INSTALLATION.md`, Troubleshooting section (lines 459–560) |
| **Strategy Step** | Step 3 — Unaddressed risks, Historical precedents of failure |

**Evidence:**
The Troubleshooting section contains five subsections:
- GitHub Install Issues (lines 461–492)
- Hook Issues (lines 494–513)
- Skill Issues (lines 525–537)
- Project Issues (lines 539–552)
- Path Issues on Windows (lines 554–560)

The Project Issues entry reads:
> "**Symptom:** Skills show XML-tagged output instead of the expected response"
> "**Cause:** `JERRY_PROJECT` is not set, points to a non-existent project, or the directory structure is incomplete."
> (INSTALLATION.md, lines 543–545)

The Configuration section (lines 271–298) is marked "Optional" and positioned after Verification in the navigation table.

**Analysis:**
The troubleshooting section addresses installation and hook failures, but the most statistically likely failure mode for a new user is not installation failure — it is a successful install followed by skills that do not work as expected because `JERRY_PROJECT` is not set.

The counter-argument is structural: the document's Configuration section (which covers `JERRY_PROJECT` setup) is labeled "Optional" in both the section heading ("Project Setup (Optional)") and in the navigation table comment. The Troubleshooting section's Project Issues entry correctly describes the failure symptom and cause, but positions it as a troubleshooting case rather than as an expected outcome of the configuration being optional.

A user who installs Jerry (2 commands), skips Configuration ("Optional"), runs `/problem-solving`, and sees XML-tagged output will read the error message `<project-required>` and not know whether their install succeeded or failed. The Troubleshooting section addresses this — but only if the user searches for it. The document's architecture routes new users away from Configuration (it's "optional") and then requires them to navigate to Troubleshooting to understand that they skipped a necessary step.

Additionally, the Troubleshooting section is structured by failure category (GitHub Install Issues, Hook Issues, Skill Issues, Project Issues) — a technician's taxonomy, not a user's failure experience. A user who runs `/problem-solving` and gets XML output does not know their failure is a "Project Issue" — they know "the skill doesn't work." The troubleshooting structure requires them to correctly categorize their failure before finding the solution.

The Verification section (lines 302–330) contains this note:
> "Note: Most skills require an active project (`JERRY_PROJECT` environment variable set). If you skipped Configuration, use `/help` instead to verify skill availability without a project."
> (INSTALLATION.md, lines 323–324)

This note is correct but undersells the consequence of skipping Configuration. A user who reaches Verification after Quick Install will see this note and may not internalize that "skipped Configuration" means "most skills will fail with XML output."

**Impact:** A significant fraction of new users will install Jerry successfully, skip Configuration (it's "optional"), attempt their first skill, encounter XML-tagged output, and either file a bug report or abandon the framework before discovering the `JERRY_PROJECT` requirement. The troubleshooting section will eventually route them to the correct fix, but the route is indirect and the failure mode is preventable by documentation design.

**Recommendation:** Two changes: (1) Rename the Configuration section from "Project Setup (Optional)" to "Project Setup (Required for Skills)" — the skills listed in the Using Jerry section require a project, so the configuration is only "optional" if the user does not want to use skills. (2) Add the most common first-run failure symptom ("skills show XML output") as the **first** troubleshooting entry, above GitHub Install Issues, since it affects successful installs, not failed ones.

**Acceptance Criteria:** (1) The Configuration section heading and navigation table entry do not use "Optional" without qualifying what becomes unavailable if skipped. (2) The Troubleshooting section's first entry addresses the "XML-tagged output" symptom and links directly to Configuration.

---

### DA-007-20260225: Document Length Exceeds Practical Reading Budget for an Install Guide [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Document-wide |
| **Strategy Step** | Step 3 — Unaddressed risks |

**Evidence:**
The document spans 607 lines across 14 navigation sections, including: Prerequisites, Install from GitHub (56 lines), Enable Hooks (41 lines), Capability Matrix (11 lines), Alternative: Local Clone (88 lines), Alternative: Plugin Dir Flag (16 lines), Configuration (28 lines), Verification (29 lines), Using Jerry (50 lines), Developer Setup (65 lines), Troubleshooting (101 lines), Uninstallation (30 lines), Getting Help (9 lines), License (3 lines).

The document begins with a navigation table (lines 9–26) listing 14 sections.

**Analysis:**
607 lines is long for an installation guide. For comparison: Homebrew's installation documentation is approximately 80 lines. The npm Getting Started guide is approximately 120 lines. The Python `pip` installation guide is approximately 150 lines. Jerry's document is 3–4x the length of comparable installation guides for widely-used developer tools.

The counter-argument is not that the content is wrong — most sections contain accurate and useful information. The counter-argument is that the length signals, to a first-time reader, that installing Jerry is a complex undertaking. User research on documentation consistently shows that document length is a proxy for perceived installation difficulty. A user who sees 14 navigation sections before reading the first line may estimate a 30-minute install time and defer the install.

The Developer Setup section (65 lines, lines 393–455) is the most defensible target for removal from this document: it is explicitly scoped to contributors and contains the note "If you installed Jerry as a plugin, you do not need anything below." This section belongs in `CONTRIBUTING.md`, not in the installation guide. Removing it reduces the document by approximately 10%.

Similarly, the Using Jerry section (50 lines) introduces skills, the persistent artifacts system, and example usage — content that belongs in the Getting Started runbook, not the installation guide. An installation guide answers "how do I install" and "is it working?" — not "what can I do with it."

**Impact:** Minor — the document is well-structured and navigable. The length does not prevent users from completing the install, but it may deter users from starting. The decision to defer is the most common single point of abandonment in OSS tool adoption.

**Recommendation:** Move the Developer Setup section to `CONTRIBUTING.md` and link to it from the installation guide with a one-line entry. Move the Using Jerry section to the Getting Started runbook (where it more naturally belongs) and replace it in the installation guide with a one-sentence "Your Jerry installation is complete. To get started, follow the Getting Started runbook." This reduces the document by approximately 115 lines without losing content.

**Acceptance Criteria:** The document is under 500 lines. Developer Setup content is in `CONTRIBUTING.md`. Using Jerry content is in the Getting Started runbook. Both are linked from the installation guide.

---

### DA-008-20260225: "Early Access Caveat" in Hooks Section Contradicts "Recommended" Section Heading [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/INSTALLATION.md`, Enable Hooks section (lines 108–147) |
| **Strategy Step** | Step 3 — Internal consistency |

**Evidence:**
> "## Enable Hooks (Recommended)"
> (INSTALLATION.md, line 108, section heading)

> "**Early access caveat:** Hook enforcement is under active development. Some hooks may have schema validation issues that cause them to fail silently (fail-open behavior — skills always work, but enforcement may not fire). If hooks don't appear to be working after installing uv, check GitHub Issues for the latest status."
> (INSTALLATION.md, lines 145–147)

**Analysis:**
The section is labeled "Recommended" but its closing note discloses that the recommended feature may silently fail. The "early access caveat" is presented as a final note in a blockquote after the installation steps — a structure that de-emphasizes the caveat as a footnote when it should be the first information a user reads about hooks.

The counter-argument: a user who reads the section heading ("Recommended"), follows the uv install steps, restarts Claude Code, and sees no observable difference in behavior cannot determine whether hooks are working (and they configured correctly) or hooks are silently failing (the "early access caveat" scenario). The fail-open design means the negative state is indistinguishable from the positive state without specialized diagnostic knowledge.

The document's own Capability Matrix (lines 150–161) says that with uv, "Per-prompt quality reinforcement (L2): Yes." If the early access caveat is active and hooks fail silently, this matrix entry is misleading — the user installed uv and the table says "Yes" for L2, but L2 may not be functioning.

This is a Minor finding (not Major) because the caveat is present — the document does disclose the limitation. The issue is structural placement and the internal tension between "Recommended" and "may silently fail."

**Recommendation:** Move the early access caveat to be the first element of the Enable Hooks section (immediately after the section heading, before "What hooks give you"). Update the section heading to "Enable Hooks (Recommended — Early Access)" to signal the status at the heading level.

**Acceptance Criteria:** The early access caveat appears before the install instructions, not after. The section heading reflects the early-access status.

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-20260225 | Integrate `/plugin marketplace list` as a required verification step between Step 1 and Step 2 in the primary install path. | Step 2 instructs users to run `/plugin marketplace list` and use the name shown. The `jerry@jerry-framework` command is shown as an example, not a fixed string. |

### P1 — Major (SHOULD resolve; require justification if not)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-002-20260225 | Restructure install section to present `--plugin-dir` as the primary onboarding path and marketplace install as the persistent install path. | `--plugin-dir` appears first or at the top of a decision guide. New users are routed to it by default. |
| DA-003-20260225 | Replace step-level McConkey idioms with declarative technical language. Preserve voice in section introductions and transitions. | All numbered steps and verification procedures use declarative sentences. "You're riding," "you're in," "rolling with Jerry" do not appear in instructional content. |
| DA-004-20260225 | Add a routing decision guide at the top of the install section to route users to the correct method before they read any method's steps. | A decision guide (table or 3-sentence routing paragraph) precedes all install method content. |
| DA-005-20260225 | Define "marketplace" at first use with a one-sentence definition distinguishing the official Anthropic registry from community plugin sources. | "Marketplace" is defined in context before the first `/plugin marketplace` command. |
| DA-006-20260225 | Rename Configuration section to "Project Setup (Required for Skills)". Move XML-output troubleshooting to first position in Troubleshooting. | Configuration section heading does not use bare "Optional". Troubleshooting first entry is the XML output symptom. |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-007-20260225 | Move Developer Setup to CONTRIBUTING.md; move Using Jerry to Getting Started runbook; link from installation guide. | Document is under 500 lines. Both moved sections are linked. |
| DA-008-20260225 | Move early access caveat to before install instructions; update section heading to reflect early-access status. | Caveat precedes uv install steps. Section heading includes early-access signal. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-006 (troubleshooting omits most likely failure mode), DA-004 (no decision guide routing users to correct path), DA-005 (marketplace term undefined): three Major findings identify coverage gaps that leave users without the information they need at the moment they need it. |
| Internal Consistency | 0.20 | Negative | DA-001 (marketplace name assumed but unverifiable), DA-008 ("Recommended" heading contradicted by "may silently fail" caveat): the document makes mutually inconsistent claims within the same sections. |
| Methodological Rigor | 0.20 | Negative | DA-001 (install command depends on undocumented Claude Code internals), DA-005 (term "marketplace" used with conflicting semantics): the install methodology relies on undocumented assumptions about Claude Code behavior that users cannot verify. |
| Evidence Quality | 0.15 | Negative | DA-001 (marketplace name `jerry-framework` not verified by document), DA-002 (`--plugin-dir` simpler path dismissed without comparative analysis): the document asserts the primary install path is optimal without demonstrating it against alternatives. |
| Actionability | 0.15 | Negative | DA-002 (simplest install path deprioritized), DA-003 (McConkey idioms at instructional moments reduce clarity), DA-006 (configuration "optional" framing causes users to skip required setup): the document's framing and structure lead users toward suboptimal actions at three critical points. |
| Traceability | 0.10 | Neutral | Cross-section links are consistent. The navigation table covers all sections. External links are present and well-formed. No traceability gaps identified. |

**Overall Assessment:** 1 Critical, 5 Major, 2 Minor findings. The document is well-structured and thorough in its content, but contains a Critical flaw in the primary install path (unverifiable marketplace name) and five Major findings that collectively create comprehension barriers, decision paralysis, and preventable post-install failures. The document should not be accepted in its current form for C4 (irreversible public release) without addressing the Critical finding and at least three of the five Major findings. Targeted revision — not major rework — is required. **Recommendation: REVISE.**

---

## Execution Statistics
- **Total Findings:** 8
- **Critical:** 1
- **Major:** 5
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** Confirmed — S-003 Steelman applied 2026-02-18
- **H-15 Self-Review Applied:** Yes — all findings verified for: specific evidence from deliverable, justified severity classification, DA-NNN-20260225 identifier format, summary table consistency with detailed findings, no findings omitted or minimized
- **Dimensions with Negative Impact:** 5 of 6
- **Dimensions Neutral:** 1 of 6 (Traceability)
- **P0 Findings (block acceptance):** 1
- **P1 Findings:** 5
- **P2 Findings:** 2

---

*Strategy: S-002 Devil's Advocate*
*Template Version: 1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Execution Date: 2026-02-25*
*Finding Prefix: DA-NNN-20260225*
*Prior Execution: `docs/reviews/adv-s002-devils-advocate-install-docs.md` (C2, 2026-02-18)*

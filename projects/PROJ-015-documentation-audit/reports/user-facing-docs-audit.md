# Diataxis Audit Report: User-Facing Documentation (6 Documents)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall audit results and cross-document findings |
| [Document 1: BOOTSTRAP.md](#document-1-docsbootstrapmd) | How-To Guide audit |
| [Document 2: INSTALLATION.md](#document-2-docsinstallationmd) | How-To Guide audit |
| [Document 3: CLAUDE-MD-GUIDE.md](#document-3-docsclaude-md-guidemd) | How-To Guide audit |
| [Document 4: getting-started.md](#document-4-docsrunbooksgetting-startedmd) | Tutorial audit |
| [Document 5: prompt-templates.md](#document-5-contextrulesprompt-templatesmd) | How-To + Reference audit |
| [Document 6: prompt-quality.md](#document-6-contextrulesprompt-qualitymd) | Multi-quadrant audit |
| [Overall Summary](#overall-summary) | Cross-document findings, verdicts, remediation plan |

---

## Summary

- **Documents audited:** 6
- **Audit date:** 2026-03-02
- **Auditor:** diataxis-auditor (diataxis skill)
- **Standards source:** `skills/diataxis/rules/diataxis-standards.md`

| # | Document | Declared Quadrant | Auditor Classification | Confidence | Verdict |
|---|----------|------------------|----------------------|------------|---------|
| 1 | `docs/BOOTSTRAP.md` | None declared | How-To Guide (primary), Explanation + Reference (secondary) | 0.85 | NEEDS REVISION |
| 2 | `docs/INSTALLATION.md` | None declared | How-To Guide | 0.85 | NEEDS REVISION |
| 3 | `docs/CLAUDE-MD-GUIDE.md` | None declared | How-To Guide (primary), Explanation (secondary) | 0.85 | NEEDS REVISION |
| 4 | `docs/runbooks/getting-started.md` | None declared | Tutorial | 1.00 | NEEDS REVISION |
| 5 | `.context/rules/prompt-templates.md` | None declared | How-To + Reference (mixed) | 0.85 | NEEDS REVISION |
| 6 | `.context/rules/prompt-quality.md` | None declared | Explanation (primary), Reference + How-To (secondary) | 0.70 | MAJOR REWORK |

**Cross-document findings:** None of the six documents declare their Diataxis quadrant. All six mix content from multiple quadrants. Four of six have voice violations. The most urgent remediations are `INSTALLATION.md` (marketing voice pervasive) and `prompt-quality.md` (spans three quadrants simultaneously).

---

## Document 1: `docs/BOOTSTRAP.md`

### Classification

**Two-axis test result:** How-To Guide (primary)
- Application axis: clear -- reader wants to sync context after cloning
- Practical axis: clear -- contains commands and steps
- Secondary content: "Why two directories?" (explanation), "How It Works" diagram (explanation), "Command Reference" table (reference)
- Confidence: 0.85

### Per-Criterion Results

| # | Criterion | Result | Evidence | Severity | Remediation |
|---|-----------|--------|----------|----------|-------------|
| H-01 | Goal stated in title | FAIL | Title is "Bootstrap Guide" -- names the tool operation. The subtitle blockquote is goal-framed but is not the title. | Minor | Rename H1 to "How to Set Up Jerry's Context Distribution After Cloning". |
| H-02 | Action-only content | FAIL | "Why two directories?" paragraph block (lines 25-30) is a 3-sentence explanation with zero action verbs: "Keeping the source of truth outside `.claude/`..." "Symlinks connect them so edits..." | Major | Extract "Why two directories?" to `docs/explanation/context-architecture.md`. Replace with one sentence: "`.context/` is the source; `.claude/` is where Claude Code reads. Bootstrap creates the symlink." |
| H-03 | Addresses real-world variations | PASS | macOS/Linux vs. Windows conditional branches. Git Worktrees variant. | -- | -- |
| H-04 | No teaching or explaining | FAIL | "How It Works" section (lines 63-82): architecture diagram of `.context/` -> `.claude/` relationships, platform strategy table with rationale prose. Foundational teaching content embedded in a procedural guide. | Major | Extract "How It Works" to the companion explanation document. Retain only the platform linking method table, stripped of surrounding narrative. |
| H-05 | Achieves flow | PASS | Steps progress cleanly. No back-tracking. Quick Start -> Platform Notes -> Troubleshooting -> Rollback -> Command Reference is logical. | -- | -- |
| H-06 | Assumes competence | PASS | Does not explain terminal basics or git. Appropriate for developer audience. | -- | -- |
| H-07 | Problem-field framing | FAIL | Title "Bootstrap Guide" names the tool operation, not the user goal. | Minor | See H-01 remediation. |

**Score: 4/7 criteria passed**

### Quadrant Mixing Findings

| # | Signal | Location | Foreign Quadrant | Severity | Recommendation |
|---|--------|----------|------------------|----------|----------------|
| 1 | Explanation blocks in how-to | "Why two directories?" section (Overview, lines 25-30): 3-paragraph rationale block, zero action verbs | Explanation | Major | Extract to `docs/explanation/context-architecture.md` |
| 2 | Explanation blocks in how-to | "How It Works" section (lines 63-80): symlink architecture diagram and platform strategy explanation | Explanation | Major | Extract to companion explanation document |
| 3 | Reference tables in how-to | "Command Reference" section (lines 165-172): 4-command parameter table | Reference | Minor | Move to Jerry CLI Reference document; cross-link with "See Jerry CLI Reference" |

### Voice Compliance

| Marker | Status | Evidence |
|--------|--------|----------|
| Active voice | PASS | "Run the bootstrap", "Verify it worked" |
| Direct address | PASS | "You're not in the Jerry repository directory", "You're already set up." |
| Concrete references | PASS | Specific commands, file paths, flag names throughout |
| No passive constructions | PASS | No passive voice detected |
| How-To voice: direct, action-oriented | PASS | Commands are crisp and imperative |
| How-To voice: no bureaucratic prose | PASS | Concise and clear throughout |

### Recommendations

1. **(Major)** Extract "Why two directories?" from Overview into `docs/explanation/context-architecture.md`. Replace with one-sentence pointer.
2. **(Major)** Extract "How It Works" into the same companion explanation document. Retain only the platform linking method table.
3. **(Minor)** Rename H1 title to "How to Set Up Jerry's Context Distribution After Cloning".
4. **(Minor)** Move the "Command Reference" table to a Jerry CLI Reference document; cross-link from this guide.

**Verdict: NEEDS REVISION** (2 Major, 2 Minor)

---

## Document 2: `docs/INSTALLATION.md`

### Classification

**Two-axis test result:** How-To Guide
- Application axis: clear -- reader wants to install Jerry and configure a project
- Practical axis: clear -- four installation paths with imperative steps throughout
- Secondary content: hooks rationale paragraph (explanation), capability matrix close (explanation), Available Skills table (reference), Persistent Artifacts table (reference), marketing voice (voice violation)
- Confidence: 0.85

### Per-Criterion Results

| # | Criterion | Result | Evidence | Severity | Remediation |
|---|-----------|--------|----------|----------|-------------|
| H-01 | Goal stated in title | PASS | "Jerry Framework Installation Guide" unambiguously states the user goal (installation). H-07 framing satisfied. | -- | -- |
| H-02 | Action-only content | FAIL | "Enable Hooks" section (lines 166-168): "Skills work the moment you install. Hooks are the next level -- they're what keep Jerry dialed across your entire session: auto-loading context at startup, reinforcing quality rules every prompt, catching state before compaction wipes it, and keeping the agent hierarchy honest. Think of hooks as Jerry's immune system -- the skills are the muscles, but hooks keep everything running clean underneath." Zero action verbs; pure rationale explanation embedded before the uv install steps. | Major | Extract the hooks metaphor paragraph to `docs/explanation/hooks-architecture.md`. Replace with: "Hooks require uv. Install uv below to enable them." |
| H-03 | Addresses real-world variations | PASS | Four install paths (GitHub SSH, HTTPS, Local Clone, Session Install). Platform variations (macOS/Linux vs. Windows) addressed for each path. | -- | -- |
| H-04 | No teaching or explaining | FAIL | Capability Matrix closing paragraph (line 222): "Without uv, you get the skills but not the guardrails. Everything still works -- but the enforcement architecture that keeps Jerry honest across long sessions stays dark. Install uv. It's worth the 30 seconds." Explains enforcement architecture rationale rather than directing action. | Major | Move the explanatory sentence to the companion explanation document. Retain only the capability matrix table. Remove "It's worth the 30 seconds." |
| H-05 | Achieves flow | PASS | Four install paths clearly separated. "Which Install Method?" decision table helps users self-sort. Troubleshooting appendix at end does not interrupt flow. | -- | -- |
| H-06 | Assumes competence | PASS | Assumes basic terminal and GitHub familiarity. Appropriately scoped for developer audience. | -- | -- |
| H-07 | Problem-field framing | PASS | Sections are user-goal-oriented: Prerequisites, Which Install Method?, Configuration, Verification. | -- | -- |

**Score: 4/7 criteria passed**

### Quadrant Mixing Findings

| # | Signal | Location | Foreign Quadrant | Severity | Recommendation |
|---|--------|----------|------------------|----------|----------------|
| 1 | Explanation blocks in how-to | Hooks metaphor paragraph (lines 166-168): "Skills work the moment you install. Hooks are the next level..." | Explanation | Major | Extract to `docs/explanation/hooks-architecture.md` |
| 2 | Explanation blocks in how-to | Capability Matrix closing paragraph (line 222): "Without uv, you get the skills but not the guardrails..." | Explanation | Major | Extract prose; retain only the matrix table |
| 3 | Reference tables in how-to | "Using Jerry > Available Skills" table (lines 425-438): full skill listing with commands and purposes | Reference | Minor | Move to Jerry Skills Reference document |
| 4 | Reference tables in how-to | "Using Jerry > Persistent Artifacts" table (lines 443-449) | Reference | Minor | Move to Jerry Skills Reference document |
| 5 | Marketing language | Title blockquote (line 3): "Your AI coding partner just got guardrails, knowledge accrual, and a whole crew of specialized agents. Let's get you set up and shredding." | Voice: marketing | Major | Replace with: "This guide walks you through installing the Jerry Framework plugin in Claude Code and configuring your first project." |
| 6 | Marketing language | Platform Note (line 5): "Jerry is built and battle-tested on macOS." | Voice: marketing | Minor | Replace with: "Jerry is developed and tested on macOS." |
| 7 | Marketing language | Skill test section (lines 407-408): "That's the whole crew reporting for duty. You're live." | Voice: marketing | Minor | Replace with: "The problem-solving skill is active. Installation is complete." |
| 8 | Marketing language | Capability Matrix close (line 222): "Install uv. It's worth the 30 seconds." | Voice: marketing | Minor | Remove. |
| 9 | Marketing language | Local Clone opener: "Same Jerry, different delivery route." | Voice: marketing | Minor | Replace with: "The local clone method installs Jerry from a local directory." |

### Voice Compliance

| Marker | Status | Evidence |
|--------|--------|----------|
| Active voice | PASS | Steps use imperative voice throughout: "Run this to confirm", "Pick whichever command" |
| Direct address | PASS | "you", "your" consistent |
| Concrete references | PASS | Specific commands, version numbers, paths throughout |
| No passive constructions | PASS | Steps are direct imperatives |
| How-To voice: direct, action-oriented | FAIL | Marketing voice in title blockquote, hooks section, skill test close, capability matrix close, local clone opener. Five instances. |

### Recommendations

1. **(Major)** Replace the title blockquote (line 3) with a neutral goal statement.
2. **(Major)** Extract the hooks metaphor paragraph from "Enable Hooks" to `docs/explanation/hooks-architecture.md`.
3. **(Major)** Extract the Capability Matrix closing prose to the hooks explanation document; retain only the table.
4. **(Minor)** Move "Available Skills" and "Persistent Artifacts" tables to a Jerry Skills Reference document.
5. **(Minor)** Remove remaining marketing voice instances: "battle-tested", "whole crew reporting for duty", "It's worth the 30 seconds", "Same Jerry, different delivery route."

**Verdict: NEEDS REVISION** (3 Major, 5 Minor)

---

## Document 3: `docs/CLAUDE-MD-GUIDE.md`

### Classification

**Two-axis test result:** How-To Guide (primary), Explanation (secondary)
- Application axis: clear -- numbered action steps dominate ("To add a new rule: 1. Create the file...")
- Acquisition axis: mixed -- "Context Architecture" section is for understanding, not doing
- Confidence: 0.85

### Per-Criterion Results

| # | Criterion | Result | Evidence | Severity | Remediation |
|---|-----------|--------|----------|----------|-------------|
| H-01 | Goal stated in title | FAIL | "CLAUDE.md Contributor Guide" -- names the artifact and audience, not the user goal. | Minor | Rename to "How to Modify Jerry's Behavioral Rules and Skills". |
| H-02 | Action-only content | FAIL | "Why this matters" sentence in Context Architecture (lines 28-29): "LLM performance degrades as context fills (Context Rot). By loading only what's needed, Jerry maintains high-quality responses across long sessions." Two-sentence rationale digression with zero action verbs. | Minor | Move "Why this matters" to companion explanation document. Replace with link. |
| H-03 | Addresses real-world variations | FAIL | No conditional branches for real-world variations. Guide covers only the add-new-file path. No variation for editing existing rules, handling symlink failures, or worktrees. | Minor | Add at least one conditional: "If editing an existing rule, edit directly in `.context/rules/` -- no additional steps needed." |
| H-04 | No teaching or explaining | FAIL | "Context Architecture" section (lines 19-46): tiered loading table, file location tree diagram, and "Why this matters" rationale. Full architectural explanation embedded in a contributor how-to guide. | Major | Extract the entire "Context Architecture" section to `docs/explanation/context-architecture.md`. Replace with one-line cross-reference. |
| H-05 | Achieves flow | PASS | Modifying Rules -> Modifying Patterns -> Constraints -> Adding Skills -> Bootstrap reference progresses logically. No backtracking. | -- | -- |
| H-06 | Assumes competence | PASS | Does not explain file system basics or git. Appropriately scoped for contributors. | -- | -- |
| H-07 | Problem-field framing | FAIL | See H-01. Title names the artifact rather than the user's goal. | Minor | See H-01 remediation. |

**Score: 3/7 criteria passed**

### Quadrant Mixing Findings

| # | Signal | Location | Foreign Quadrant | Severity | Recommendation |
|---|--------|----------|------------------|----------|----------------|
| 1 | Explanation blocks in how-to | "Context Architecture" section (lines 19-46): tiered loading explanation, file tree diagram, "Why this matters" rationale | Explanation | Major | Extract to `docs/explanation/context-architecture.md` |
| 2 | Explanation blocks in how-to | "CLAUDE.md Constraints" -- "What belongs / What does NOT belong" lists explain categories rather than direct action | Explanation | Minor | Reframe as imperative directives |
| 3 | Reference tables in how-to | Context Architecture tier table (lines 22-27): Tier 1-4 with Content/Loading/Size columns | Reference | Minor | If retained post-extraction, label as quick-reference callout |

### Voice Compliance

| Marker | Status | Evidence |
|--------|--------|----------|
| Active voice | PASS | "Edit the file in `.context/rules/`", "Create the file in `.context/rules/your-rule.md`" |
| Direct address | PASS | "you're done", "your rule", "your skill" |
| Concrete references | PASS | Specific file paths, frontmatter fields, directory names |
| No passive constructions | PASS | No passive voice detected |
| How-To voice: direct, action-oriented | PASS | Steps are crisp and imperative |
| How-To voice: no bureaucratic prose | PASS | Concise throughout |

### Recommendations

1. **(Major)** Extract the entire "Context Architecture" section to `docs/explanation/context-architecture.md`. Replace with one cross-reference sentence.
2. **(Minor)** Rename H1 title to "How to Modify Jerry's Behavioral Rules and Skills".
3. **(Minor)** Add at least one conditional branch (editing existing rules, worktree usage).
4. **(Minor)** Reframe "What belongs / What does NOT belong" as imperative directives.

**Verdict: NEEDS REVISION** (1 Major, 3 Minor)

---

## Document 4: `docs/runbooks/getting-started.md`

### Classification

**Two-axis test result:** Tutorial
- Practical axis: clear -- hands-on numbered steps with explicit commands
- Acquisition axis: clear -- reader is learning the Jerry workflow for the first time; endpoint is "first successful skill invocation"
- Confidence: 1.00 (both axes unambiguous)

**Strongest document in the audit set.** Clear endpoint, explicit prerequisites, numbered steps with expected outputs, verification checklist.

### Per-Criterion Results

| # | Criterion | Result | Evidence | Severity | Remediation |
|---|-----------|--------|----------|----------|-------------|
| T-01 | Completable end-to-end | PASS | All 5 steps have complete, unambiguous commands. No dead ends. Prerequisites clearly gate the entry condition. | -- | -- |
| T-02 | Every step has visible result | PASS | Step 1: "Expected result: The path `PROJ-001-my-first-project/` exists..." Step 2: "Expected output: `PROJ-001-my-first-project`". Step 3: Hook tag table with expected output block. Step 4: Example directory tree. Step 5: `find`/`Get-ChildItem` commands with expected results. All steps produce observable results. | -- | -- |
| T-03 | No unexplained steps | FAIL | Step 1 callout "What are these files?" (lines 61-63): explains PLAN.md and WORKTRACKER.md after the file creation commands. Reader is told to create files before being told what they are. | Minor | Move the explanation before the commands. Compress to: "Both files can be empty for now -- skills write into them automatically." |
| T-04 | No alternatives offered | FAIL | Step 3 note (line 101-102): "The `jerry` CLI command is available when you have a local clone with uv configured... If you installed Jerry as a plugin without cloning, the SessionStart hook still fires automatically -- you do not need the CLI." Two paths presented. | Minor | Commit to one path for the tutorial (plugin-install path). Move CLI alternative to "How to Start a Jerry Session via CLI" how-to guide. |
| T-05 | Concrete not abstract | PASS | All steps use specific project names (`PROJ-001-my-first-project`), exact commands, specific file paths. No placeholder-only instructions. | -- | -- |
| T-06 | Prerequisites stated | PASS | Prerequisites block (lines 21-27): checkbox list with Claude Code 1.0.33+ (version check command), Jerry plugin installed (verification path), uv (recommended, with verification command). States "complete installation steps first." | -- | -- |
| T-07 | Endpoint shown upfront | PASS | Opening paragraph: "By the end you will have a configured project, a running session, and a persisted output artifact on disk." | -- | -- |
| T-08 | Reliable reproduction | FAIL | Step 4 expected behavior includes LLM-routing-dependent behavior ("Claude responds by activating the problem-solving skill") and a date-stamped filename in the example tree (`ps-research-readable-python-20260218.md`) that will differ on every invocation. | Minor | Qualify the example output: "The filename includes today's date and your topic. The exact name will differ." Promote explicit invocation (`/problem-solving`) as the primary path. |

**Score: 5/8 criteria passed**

### Quadrant Mixing Findings

| # | Signal | Location | Foreign Quadrant | Severity | Recommendation |
|---|--------|----------|------------------|----------|----------------|
| 1 | "Why" digression in tutorial step | Step 1 callout "What are these files?" (lines 61-63): explains PLAN.md and WORKTRACKER.md purpose. No action verbs. | Explanation | Minor | Compress to single-sentence context note before the commands. |
| 2 | "Why" digression in tutorial step | Step 2 callout "Why is this required (H-04)?" (lines 91-93): 3-sentence rationale for the JERRY_PROJECT requirement. | Explanation | Minor | Compress to: "Required: hooks and skills write output to a project directory and cannot proceed without this variable set." |
| 3 | Choice/alternative in tutorial | Step 3 note (lines 101-102): CLI path vs. plugin path branching | How-To | Minor | Pick one path for the tutorial. |
| 4 | Reference callout in tutorial | Step 5 (lines 176-178): agent-to-directory mapping in prose form | Reference | Minor | Move mapping to a reference document. Replace here with: "The output file appears under the project directory in an agent-specific subdirectory." |

### Voice Compliance

| Marker | Status | Evidence |
|--------|--------|----------|
| Active voice | PASS | "Create the project directory structure", "Confirm the variable is set" |
| Direct address | PASS | "you will have a configured project", "your session is active" |
| Concrete references | PASS | Specific project names, commands, expected output strings |
| No passive constructions | PASS | No passive voice in steps |
| Tutorial voice: encouraging, collaborative | PASS | "By the end you will have..." -- collaborative framing |
| Tutorial voice: no "why" digressions | FAIL | Two "why" digressions in step callouts (Minor) |

### Recommendations

1. **(Minor)** Remove the CLI vs. plugin branching in Step 3. Commit to the plugin-install path. Move CLI alternative to a companion how-to guide.
2. **(Minor)** Compress "What are these files?" and "Why is this required?" to single-sentence context notes placed before the relevant commands.
3. **(Minor)** In Step 4, qualify the example output filename as date-variable. Promote explicit invocation (`/problem-solving`) as the primary path.
4. **(Minor)** Move agent-to-directory mapping in Step 5 to a reference document.

**Verdict: NEEDS REVISION** (0 Major, 4 Minor)

---

## Document 5: `.context/rules/prompt-templates.md`

### Classification

**Two-axis test result:** How-To Guide (primary) + Reference (secondary)
- The template bodies are reference specifications (copy-paste templates with structured placeholders)
- The "how to choose a template" guidance is how-to content
- The "Key Conventions" rationale paragraphs are explanation content
- Confidence: 0.85 (borderline -- the document sits on the reference-howto boundary)

### Per-Criterion Results

| # | Criterion | Result | Evidence | Severity | Remediation |
|---|-----------|--------|----------|----------|-------------|
| H-01 | Goal stated in title | FAIL | "Prompt Templates for Jerry" -- names the artifact, not the user goal. | Minor | Rename to "How to Write a Jerry Prompt Using the Template Catalog". |
| H-02 | Action-only content | FAIL | Template Quick-Select decision flowchart: "Is the task open-ended exploration...? YES -> Template 1". Zero action verbs; purely classification/explanatory content. Template 6 "Key Conventions": 4 numbered rationale paragraphs. Explanation content between templates. | Major | Separate how-to usage guidance from template reference catalog. Move rationale paragraphs to a companion explanation document. |
| H-03 | Addresses real-world variations | PASS | Templates 1-6 cover distinct real-world scenarios. Template Quick-Select provides conditional routing. | -- | -- |
| H-04 | No teaching or explaining | FAIL | "Key Conventions" subsection in Template 6 explains WHY claim-before-execute works and WHY one item per session matters. Pedagogical content between templates. | Minor | Extract rationale paragraphs to companion explanation document. Keep conventions as terse imperative bullets only. |
| H-05 | Achieves flow | PASS | Templates clearly separated by heading. Quick-Select at top enables navigation. Logical progression from simple to complex. | -- | -- |
| H-06 | Assumes competence | PASS | Assumes familiarity with Jerry's agent naming convention, project IDs, skill invocation. | -- | -- |
| H-07 | Problem-field framing | FAIL | See H-01. Title is artifact-framed, not user-goal-framed. | Minor | See H-01 remediation. |

**Score: 3/7 criteria passed**

### Quadrant Mixing Findings

| # | Signal | Location | Foreign Quadrant | Severity | Recommendation |
|---|--------|----------|------------------|----------|----------------|
| 1 | Explanation blocks in how-to | Template Quick-Select decision tree: classification flowchart with no action verbs | Explanation | Minor | Move to explanation document or How-To Guide opening. |
| 2 | Explanation blocks in how-to | Template 6 "Key Conventions": 4 rationale paragraphs | Explanation | Minor | Extract to companion explanation document. Keep conventions as imperative bullets. |
| 3 | Reference tables in how-to | The 6 template bodies: copy-paste specifications with placeholder tables | Reference | Major | Restructure: (a) Reference document with template bodies; (b) How-To Guide with template selection guidance. |
| 4 | Explanation blocks in how-to | "Related Resources" footer with research attribution | Explanation | Minor | Remove or move to document frontmatter metadata. |

### Voice Compliance

| Marker | Status | Evidence |
|--------|--------|----------|
| Active voice | PASS | "Replace `{{PLACEHOLDERS}}` with your values" |
| Direct address | PASS | "your values", "your situation" |
| Concrete references | PASS | Specific agent names, file path patterns, quality threshold values |
| No passive constructions | PASS | Instructions are direct |
| How-To voice: direct, action-oriented | FAIL | Key Conventions section reads as narrative explanation |

### Recommendations

1. **(Major)** Decompose into two documents: a Reference document (template bodies as a catalog) and a How-To Guide ("How to Choose and Use a Jerry Prompt Template").
2. **(Minor)** Extract the Template Quick-Select decision tree to an explanation document or the opening of the How-To Guide.
3. **(Minor)** Extract Key Conventions rationale paragraphs in Template 6 to a companion explanation document. Replace with imperative bullets.
4. **(Minor)** Rename to a goal-framed title.

**Verdict: NEEDS REVISION** (1 Major, 3 Minor)

---

## Document 6: `.context/rules/prompt-quality.md`

### Classification

**Two-axis test result:** Multi-quadrant (three quadrants)
- Explanation: "5 Elements", "The Golden Rule", "The 4 Effectiveness Tiers", "Anti-Patterns" rationale
- Reference: 7-criterion quality rubric table, agent selection table, anti-pattern catalog table
- How-To: Pre-Submission Checklist (imperative action checklist), Adversarial Critique Loop invocation instructions

**Both axes mixed. Confidence: 0.70** -- minimum non-escalation threshold.

**Decomposition recommended:**
1. Explanation: "Why Jerry Prompts Need These Five Elements" (rationale, golden rule, effectiveness tiers)
2. Reference: Jerry Prompt Quality Rubric (criterion table, agent selection table, anti-pattern catalog)
3. How-To Guides: "How to Review a Jerry Prompt Before Submission" (checklist); "How to Apply Adversarial Critique in Jerry" (critique loop)

**Auditing against Explanation criteria** (primary quadrant -- the 5-element teaching content dominates and is the document's stated purpose).

### Per-Criterion Results

| # | Criterion | Result | Evidence | Severity | Remediation |
|---|-----------|--------|----------|----------|-------------|
| E-01 | Discursive (not procedural) | FAIL | "Pre-Submission Checklist" section: 10-item imperative checkbox list. "Adversarial Critique Loop > How to Invoke": "Add these two lines to any prompt:" followed by a code block -- imperative instruction sequence. Procedural sequences embedded in explanation content. | Major | Extract Pre-Submission Checklist to How-To Guide. Extract Critique Loop invocation to How-To Guide. |
| E-02 | Makes connections | PASS | Document connects: 5 elements -> Jerry mechanisms, skill routing -> agent selection, cognitive modes -> model tiers. Substantive cross-references with relationship explanations. | -- | -- |
| E-03 | Provides context | PASS | "How Each Element Maps to Jerry" provides design context. Anti-pattern entries include impact reasoning. "The Golden Rule" provides framing perspective. | -- | -- |
| E-04 | Acknowledges perspective | FAIL | The 5-element formula and quality rubric are presented as singular prescriptive truth. No acknowledgment that ad-hoc conversational questions do not need all five elements. | Minor | Add: "These elements apply to consequential deliverables. For ad-hoc conversational questions, not all elements are necessary." |
| E-05 | Enriches understanding | PASS | "The Golden Rule": "Every missing element forces Claude to make a structural decision you probably should have made." Strong "why" reasoning. Anti-pattern entries include impact reasoning. | -- | -- |
| E-06 | Bounded scope | PASS | Scoped to Jerry prompt construction. Not attempting to cover all LLM prompt engineering. | -- | -- |
| E-07 | No imperative instructions | FAIL | Multiple instances: "Add these two lines to any prompt:" (Critique Loop); "Work through these 10 checks before submitting a prompt" (Checklist header); "Check C1, C2, C4, C6 first"; "Fix these four first". 5+ imperative instruction sequences in explanation content. | Major | Extract all imperative instruction sequences to companion How-To Guides. In this explanation document, describe what these checks accomplish in discursive prose. |

**Score: 4/7 criteria passed**

### Quadrant Mixing Findings

| # | Signal | Location | Foreign Quadrant | Severity | Recommendation |
|---|--------|----------|------------------|----------|----------------|
| 1 | Procedural sequences in explanation | "Pre-Submission Checklist" section: 10-item checkbox list with imperative action items | How-To | Major | Extract to "How to Review a Jerry Prompt Before Submission" |
| 2 | Procedural sequences in explanation | "Adversarial Critique Loop > How to Invoke": imperative "Add these two lines" with code block | How-To | Major | Extract to "How to Apply Adversarial Critique in a Jerry Session" |
| 3 | Procedural sequences in explanation | "Quick Scoring" subsection: "Check C1, C2, C4, C6 first", "Fix these four first" | How-To | Minor | Reframe as descriptive explanation |
| 4 | Reference tables in explanation | 7-criterion quality rubric table: weights, descriptions, scoring formula | Reference | Minor | Retain as conceptual framework illustration; cross-reference precise weights to a reference document |
| 5 | Reference tables in explanation | "Agent Selection" table: agent, model tier, cognitive mode | Reference | Minor | Move to Jerry Agent Reference document; cross-link |
| 6 | Reference tables in explanation | "Anti-Patterns" 8-row table with impact and fix columns | Reference | Minor | If retained, reframe as discursive prose. Alternatively, move table to reference document. |

### Voice Compliance

| Marker | Status | Evidence |
|--------|--------|----------|
| Active voice | PASS | Most prose uses active constructions |
| Direct address | PASS | "you", "your" consistent |
| Concrete references | PASS | Specific agent names, criterion IDs, threshold values |
| No passive constructions | PASS | No significant passive voice |
| Explanation voice: thoughtful, discursive | FAIL | Pre-Submission Checklist and Critique Loop read as procedural directives |
| Explanation voice: no imperative instructions | FAIL | 5+ imperative instruction sequences (E-07) |

### Recommendations

1. **(Major)** Extract "Pre-Submission Checklist" to "How to Review a Jerry Prompt Before Submission" how-to guide.
2. **(Major)** Extract "Adversarial Critique Loop > How to Invoke" to "How to Apply Adversarial Critique in a Jerry Session" how-to guide.
3. **(Minor)** Reframe "Quick Scoring" from imperative action sequence to descriptive explanation.
4. **(Minor)** Move "Agent Selection" table to a Jerry Agent Reference document; cross-link.
5. **(Minor)** Add acknowledgment of alternative approaches (E-04).
6. **(Minor)** Consider splitting "Anti-Patterns" table into reference document; replace with discursive prose.

**Verdict: MAJOR REWORK** (2 Major findings spanning the document's primary explanation purpose)

---

## Overall Summary

### Cross-Document Findings

| Finding | Documents Affected | Severity |
|---------|-------------------|----------|
| No Diataxis quadrant declared on any document | All 6 | Minor (metadata) |
| Explanation content embedded in procedural documents | BOOTSTRAP.md, INSTALLATION.md, CLAUDE-MD-GUIDE.md, prompt-templates.md, prompt-quality.md | Major |
| Marketing / personality voice in user-facing how-to guides | INSTALLATION.md | Major |
| Reference tables embedded in non-reference documents | BOOTSTRAP.md, INSTALLATION.md, prompt-templates.md, prompt-quality.md | Minor |
| Missing companion explanation documents | BOOTSTRAP.md, INSTALLATION.md, CLAUDE-MD-GUIDE.md | Major (remediation gap) |
| Tutorial branching (alternatives offered mid-tutorial) | getting-started.md | Minor |

### Verdict Summary

| Document | Criteria Tested | Pass | Fail | Major | Minor | Verdict |
|----------|----------------|------|------|-------|-------|---------|
| BOOTSTRAP.md | H-01 to H-07 | 4 | 3 | 2 | 2 | NEEDS REVISION |
| INSTALLATION.md | H-01 to H-07 | 4 | 3 | 3 | 5 | NEEDS REVISION |
| CLAUDE-MD-GUIDE.md | H-01 to H-07 | 3 | 4 | 1 | 3 | NEEDS REVISION |
| getting-started.md | T-01 to T-08 | 5 | 3 | 0 | 4 | NEEDS REVISION |
| prompt-templates.md | H-01 to H-07 | 3 | 4 | 1 | 3 | NEEDS REVISION |
| prompt-quality.md | E-01 to E-07 | 4 | 3 | 2 | 4 | MAJOR REWORK |

### Priority-Ordered Remediation Plan

| Priority | Action | Document(s) | Severity Basis |
|----------|--------|-------------|----------------|
| 1 | Decompose `prompt-quality.md` into: (a) explanation, (b) two how-to guides (checklist, critique loop), (c) reference (rubric + agent table + anti-patterns) | prompt-quality.md | MAJOR REWORK; 2 Major quadrant violations |
| 2 | Remove all marketing voice from `INSTALLATION.md`: title blockquote, hooks metaphor, skill test close, capability matrix close | INSTALLATION.md | Major -- voice violation pervasive |
| 3 | Extract explanation content from `INSTALLATION.md` (hooks rationale, capability matrix prose) to `docs/explanation/hooks-architecture.md` | INSTALLATION.md | Major |
| 4 | Extract "Context Architecture" section from `CLAUDE-MD-GUIDE.md` to `docs/explanation/context-architecture.md` | CLAUDE-MD-GUIDE.md | Major |
| 5 | Extract "Why two directories?" and "How It Works" from `BOOTSTRAP.md` to `docs/explanation/context-architecture.md` | BOOTSTRAP.md | Major |
| 6 | Decompose `prompt-templates.md` into: (a) reference (template bodies), (b) how-to guide (template selection and usage) | prompt-templates.md | Major |
| 7 | Fix H-01/H-07 title violations on BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, prompt-templates.md | Multiple | Minor |
| 8 | Fix T-04 tutorial branching in `getting-started.md` Step 3 | getting-started.md | Minor |
| 9 | Compress "why" digressions in `getting-started.md` Steps 1-2 | getting-started.md | Minor |
| 10 | Move skills reference tables to consolidated Jerry Skills Reference document | Multiple | Minor + Gap |

### Missing Documentation Identified

| Missing Document | Type | Source Extractions | Priority |
|-----------------|------|--------------------|----------|
| `docs/explanation/context-architecture.md` | Explanation | Extracts from BOOTSTRAP.md and CLAUDE-MD-GUIDE.md | High |
| `docs/explanation/hooks-architecture.md` | Explanation | Extracts from INSTALLATION.md | High |
| Jerry Skills Reference | Reference | Available Skills table (INSTALLATION.md), agent selection table (prompt-quality.md) | Medium |
| Jerry CLI Reference | Reference | Command Reference table (BOOTSTRAP.md) | Medium |
| "How to Review a Jerry Prompt Before Submission" | How-To Guide | Pre-Submission Checklist (prompt-quality.md) | High |
| "How to Apply Adversarial Critique in a Jerry Session" | How-To Guide | Critique Loop invocation (prompt-quality.md) | High |
| "How to Choose and Use a Jerry Prompt Template" | How-To Guide | Template Quick-Select + usage guidance (prompt-templates.md) | Medium |

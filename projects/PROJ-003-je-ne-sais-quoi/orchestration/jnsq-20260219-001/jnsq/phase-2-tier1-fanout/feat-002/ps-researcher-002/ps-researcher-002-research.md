# FEAT-002 Research: /saucer-boy Skill Architecture

<!--
AGENT: ps-researcher-002
VERSION: 1.0.0
WORKFLOW: jnsq-20260219-001
PHASE: 2 — Tier 1 Fan-Out
FEATURE: FEAT-002 /saucer-boy Skill
PARENT: EPIC-001-je-ne-sais-quoi
STATUS: COMPLETE
DATE: 2026-02-19
SOURCES: Existing Jerry skills audit, FEAT-001 persona doc (v0.9.0), DISC-001, DEC-001, Anthropic official docs
FEEDS INTO: ps-creator-002 (skill construction)
-->

> **Epistemic note (P-022):** This research artifact combines internal skill audits (4 existing Jerry skills examined in full), the Phase 1 persona document (879 lines, v0.9.0), Phase 1 design constraints (DISC-001, DEC-001), and external research from Anthropic's official documentation. All web sources are cited with URLs in the [Web Sources](#web-sources) section. Internal patterns are cited by file path.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Research Question 1: Skill Structure Patterns](#research-question-1-skill-structure-patterns) | Audit of existing Jerry skill architectures |
| [Research Question 2: Decomposition Map](#research-question-2-decomposition-map) | Line-range mapping from persona doc to reference files |
| [Research Question 3: Agent Design](#research-question-3-agent-design) | Agent specifications with reference file loading |
| [Research Question 4: Integration Points](#research-question-4-integration-points) | How /saucer-boy connects to existing framework |
| [Research Question 5: SKILL.md Content Strategy](#research-question-5-skillmd-content-strategy) | What goes in SKILL.md vs references/ |
| [Research Question 6: YAML Frontmatter](#research-question-6-yaml-frontmatter) | Skill metadata format |
| [Proposed Directory Structure](#proposed-directory-structure) | Full tree for skills/saucer-boy/ |
| [Design Constraints Summary](#design-constraints-summary) | Binding decisions from Phase 1 |
| [Web Sources](#web-sources) | External references with URLs |
| [Internal Sources](#internal-sources) | Repository file paths |

---

## Research Question 1: Skill Structure Patterns

### Existing Jerry Skill Audit

Four skills were audited: adversary, problem-solving, worktracker, and orchestration. The analysis reveals consistent patterns and significant variation in complexity.

#### SKILL.md Size Comparison

| Skill | Lines | Words (est.) | Agents | References/Rules | Frontmatter Fields |
|-------|-------|-------------|--------|-----------------|-------------------|
| adversary | 427 | ~3,800 | 3 (adv-selector, adv-executor, adv-scorer) | 10 strategy templates in `.context/templates/adversarial/` | name, description, version, allowed-tools, activation-keywords |
| problem-solving | 441 | ~3,900 | 9 (ps-researcher through ps-reporter) | Agent template + extension files, output templates | name, description, version, allowed-tools, activation-keywords |
| orchestration | 690 | ~5,500 | 3 (orch-planner, orch-tracker, orch-synthesizer) | Templates for plan, worktracker, YAML state | name, description, version, allowed-tools, activation-keywords |
| worktracker | 198 | ~1,600 | 3 (wt-verifier, wt-visualizer, wt-auditor) | 6 rule files via `@import` pattern | name, description, version, allowed-tools, activation-keywords |

**Key finding:** Jerry SKILL.md files range from 198 to 690 lines. The average is ~439 lines. All are under 5,000 words, consistent with the Anthropic recommendation of keeping SKILL.md under 500 lines [WS-1, WS-2]. The /saucer-boy SKILL.md target of ~200 lines (per DISC-001) is well within this range and matches the leanest existing skill (worktracker at 198 lines).

#### Structural Patterns Identified

**Pattern 1: Triple-Lens Audience Table (adversary, problem-solving)**

Both complex skills open with a triple-lens audience table mapping L0/L1/L2 readers to specific sections. This is a Jerry-specific enhancement over the Anthropic base pattern.

```markdown
| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| L0 | New users, stakeholders | Purpose, When to Use |
| L1 | Developers | Invoking, Agents, Dependencies |
| L2 | Architects | P-003 Compliance, Integration |
```

**Pattern 2: P-003 Compliance Diagram (adversary, orchestration)**

Skills that involve agents include an explicit ASCII diagram showing the main context as orchestrator and agents as workers. This is a constitutional compliance artifact.

**Pattern 3: Agent Registry Table (all four skills)**

Every skill has a table listing agents with role, model, and output location:

```markdown
| Agent | Role | Model | Output Location |
|-------|------|-------|-----------------|
```

**Pattern 4: When to Use / When NOT to Use (adversary, orchestration)**

Complex skills include explicit positive and negative trigger conditions. This is particularly important for /saucer-boy to prevent misuse as a Claude personality modifier.

**Pattern 5: @import Rule Loading (worktracker)**

The worktracker skill uses `@rules/filename.md` syntax to auto-load behavior rules into context when the skill triggers. Other rules are on-demand. This is the "always-loaded vs on-demand" pattern that maps directly to SKILL.md body vs references/.

**Pattern 6: Activation Keywords in Frontmatter (all four skills)**

All Jerry skills include `activation-keywords` in YAML frontmatter -- a list of trigger phrases. This is a Jerry-specific extension beyond the standard Anthropic `name` + `description` fields.

#### Agent File Structure Pattern

Agent files follow a consistent structure (analyzed from `adv-scorer.md`, 490 lines):

1. **YAML frontmatter** with name, version, description, model, identity, persona, capabilities, guardrails, constitution sections
2. **`<agent>` XML wrapper** containing:
   - `<identity>` -- role definition, expertise, cognitive mode, key distinctions
   - `<purpose>` -- single-paragraph mission
   - `<input>` -- expected context format (markdown code block)
   - Domain-specific process sections
   - `<output>` -- required output format with template
   - `<constraints>` -- hard rules
   - `<examples>` -- input/output pairs

Agent files are typically 300-500 lines. The YAML frontmatter + XML body pattern is consistent across all three skill families examined.

#### Reference File Organization Patterns

| Skill | Reference Pattern | Location | Loading Model |
|-------|------------------|----------|---------------|
| adversary | Strategy templates | `.context/templates/adversarial/s-{NNN}-{slug}.md` | On-demand by adv-executor per strategy ID |
| problem-solving | Agent template + extensions | `agents/PS_AGENT_TEMPLATE.md`, `agents/PS_EXTENSION.md` | On-demand for agent generation |
| worktracker | Rule files | `rules/worktracker-*.md` | 2 auto-loaded via @import, 4 on-demand |
| orchestration | Workflow templates | `templates/ORCHESTRATION_*.template.md` | On-demand when creating workflow artifacts |

**Key finding for /saucer-boy:** The adversary skill's model is closest to what /saucer-boy needs -- a set of modular reference files that specific agents load on-demand based on their task. The worktracker's @import pattern for always-loaded rules maps to what the /saucer-boy SKILL.md body should contain (the decision rules that every invocation needs).

---

## Research Question 2: Decomposition Map

### Persona Doc Section Index (879 lines)

The following table maps every major section of the persona document (v0.9.0) to its line range and proposed destination in the skill structure. Line numbers are from `ps-creator-001-draft.md`.

| Section | Line Range | Lines | Proposed Destination | Rationale |
|---------|-----------|-------|---------------------|-----------|
| Frontmatter + Epistemic Note | 1-19 | 19 | Omit (metadata) | Not needed in skill; provenance tracked by DEC-002 |
| Document Sections (nav table) | 21-39 | 19 | Omit (navigation) | Skill has its own navigation |
| **Core Thesis** | 41-53 | 13 | **SKILL.md** | Load-bearing philosophy; needed every invocation (DEC-001 D-003) |
| **The Shane McConkey Story** | 55-96 | 42 | **references/biographical-context.md** | Context for calibration; not needed for routine review/rewrite |
| **Persona Attributes: Voice Traits** | 99-112 | 14 | **SKILL.md** | Decision rule: 5-trait table is the core evaluation rubric (DEC-001 D-003) |
| **Persona Attributes: Tone Spectrum** | 113-126 | 14 | **SKILL.md** | Decision rule: calibrates energy level per context |
| **Persona Attributes: Humor Style** | 127-140 | 14 | **references/humor-deployment.md** | Example content; explains the two comedy modes with illustrations |
| **Persona Attributes: Humor Deployment Rules** | 141-163 | 23 | **SKILL.md** | Decision rule: context-to-humor mapping table is a gate (DEC-001 D-003) |
| **Persona Attributes: Energy Calibration** | 158-163 | 6 | **SKILL.md** | Decision rule: energy calibration principle |
| **Voice Guide: Pairs 1-9** | 166-387 | 222 | **references/voice-guide.md** | Example content: 9 before/after pairs (DEC-001 D-003). Largest single section. |
| **Boundary Conditions** (7 subsections) | 389-448 | 60 | **SKILL.md** (condensed) + **references/boundary-conditions.md** (full) | Decision rules: the 7 NOT conditions are hard gates. SKILL.md carries the test names and one-line summaries; references/ carries the full explanations. |
| **Cultural Reference Palette** | 450-504 | 55 | **references/cultural-palette.md** | Example content: in-bounds/out-of-bounds reference tables |
| **Audience Adaptation Matrix** | 507-543 | 37 | **SKILL.md** (matrix table) + **references/audience-adaptation.md** (audience notes) | Decision rule: the matrix table maps context to energy/humor/depth. Audience-specific notes are elaboration. |
| **Visual Vocabulary** | 546-613 | 68 | **references/visual-vocabulary.md** | Example content: ASCII philosophy, emoji philosophy, formatting patterns, terminal colors |
| **Implementation Notes (FEAT-002-007)** | 617-731 | 115 | **references/implementation-notes.md** | Guidance for downstream features; /saucer-boy agents load FEAT-002 section only when needed |
| **Vocabulary Reference** | 735-787 | 53 | **references/vocabulary-reference.md** | Example content: substitution tables, forbidden constructions, skiing vocabulary |
| **Authenticity Test** | 789-803 | 15 | **SKILL.md** | Decision rule: 5-test ordered gate. This is the primary quality check. (DEC-001 D-003) |
| **Traceability** | 807-817 | 11 | Omit (provenance) | Tracks persona doc sources, not skill operational data |
| **References** | 819-861 | 43 | Omit (persona doc references) | Web citations for biographical claims; not needed in operational skill |
| **Document Metadata** | 863-879 | 17 | Omit (metadata) | Version history of persona doc |

### Estimated File Sizes

| File | Source Lines | Estimated Output Lines | Content Type |
|------|------------|----------------------|--------------|
| SKILL.md | ~145 (extracted decision rules) | ~200 | Core thesis, voice traits, tone spectrum, humor deployment rules, energy calibration, boundary condition summaries, audience matrix, authenticity test, agent registry |
| references/voice-guide.md | 222 | ~200 | 9 before/after pairs (may be lightly edited for skill context) |
| references/biographical-context.md | 42 | ~50 | McConkey story, framework inheritance table, risk exclusion |
| references/humor-deployment.md | 14 (humor style) | ~40 | Two comedy modes with examples, expanded from persona doc |
| references/boundary-conditions.md | 60 | ~70 | Full 7-subsection boundary explanations with governance implications |
| references/cultural-palette.md | 55 | ~60 | In-bounds/out-of-bounds tables for skiing, music, film, counter-culture |
| references/audience-adaptation.md | 37 | ~40 | Audience-specific notes for active developer, debugging, docs, onboarding, post-incident |
| references/visual-vocabulary.md | 68 | ~70 | ASCII philosophy, emoji philosophy, formatting patterns, terminal colors |
| references/implementation-notes.md | 115 | ~120 | FEAT-002 through FEAT-007 specific guidance |
| references/vocabulary-reference.md | 53 | ~60 | Preferred terms, forbidden constructions, skiing vocabulary |

**Total:** ~200 (SKILL.md) + ~710 (references) = ~910 lines across 11 files.

The persona doc's 879 lines expand slightly to ~910 due to per-file navigation tables (H-23) and frontmatter, but the per-invocation context load drops from ~15k tokens (full doc) to ~3-4k tokens (SKILL.md + 1-2 reference files), a 4-5x reduction as predicted by DISC-001.

---

## Research Question 3: Agent Design

### Agent Inventory

DISC-001 proposed three agents: sb-reviewer, sb-rewriter, sb-calibrator. After analyzing the persona doc's implementation notes (lines 621-640) and the Authenticity Test structure (lines 789-803), this research validates the three-agent design with refined responsibilities.

#### Agent 1: sb-reviewer

**Purpose:** Evaluate whether a piece of framework output text is voice-compliant. This is the primary quality gate agent.

**Trigger conditions:**
- Text needs persona compliance check before shipping
- Quality gate messages, error messages, CLI outputs, hook outputs need voice review
- Integration with /adversary for persona compliance as a quality dimension (FEAT-004)

**Reference files loaded:**
1. Always: SKILL.md (authenticity tests, voice traits, boundary condition summaries, audience adaptation matrix, humor deployment rules)
2. On-demand: `references/boundary-conditions.md` (when a boundary condition flag is triggered)
3. On-demand: `references/vocabulary-reference.md` (when vocabulary issues are suspected)

**Tools needed:** Read, Write, Edit, Glob, Grep

**Model:** sonnet (requires analytical rigor for rubric application, similar to adv-scorer)

**Key behavior:** Apply the 5 Authenticity Tests in order (lines 789-803 of persona doc). Test 1 (information completeness) is a hard gate -- if it fails, stop and report the information gap. Do NOT evaluate Tests 2-5 until Test 1 passes. This ordered evaluation is the core differentiator from a generic reviewer.

**Output:** Voice compliance report with per-test pass/fail, specific evidence, and suggested fixes.

#### Agent 2: sb-rewriter

**Purpose:** Rewrite framework output text from current Jerry voice to Saucer Boy voice while preserving all technical information.

**Trigger conditions:**
- Text has been identified as needing voice transformation
- FEAT-004 implementation: batch rewriting of quality gate messages, error messages, etc.
- One-off rewrites of specific framework outputs

**Reference files loaded:**
1. Always: SKILL.md (voice traits, tone spectrum, humor deployment rules, audience adaptation matrix)
2. Always: `references/voice-guide.md` (before/after pairs are the calibration standard)
3. On-demand: `references/cultural-palette.md` (when cultural references would enhance the text)
4. On-demand: `references/vocabulary-reference.md` (for term substitution guidance)
5. On-demand: `references/visual-vocabulary.md` (when formatting decisions are involved)

**Tools needed:** Read, Write, Edit

**Model:** sonnet (requires creative language generation with precision constraint)

**Key behavior:** Rewrite the text, then self-apply the 5 Authenticity Tests before presenting the result. If the rewrite fails any test, revise internally before outputting. The before/after pairs in voice-guide.md are the calibration standard -- the rewrite should feel like the "Saucer Boy Voice" column of those pairs.

**Output:** Rewritten text with annotation of which voice traits were applied and which Authenticity Tests were checked.

#### Agent 3: sb-calibrator

**Purpose:** Score voice fidelity on a 0-1 scale across the 5 voice traits. Analogous to adv-scorer for quality dimensions, but for persona dimensions.

**Trigger conditions:**
- Quantitative voice fidelity assessment needed
- Integration with /adversary quality scoring (persona compliance as an additional dimension)
- FEAT-004 batch scoring of rewritten messages
- Tracking voice fidelity improvement across revision iterations

**Reference files loaded:**
1. Always: SKILL.md (voice traits table is the scoring rubric, authenticity tests)
2. Always: `references/voice-guide.md` (before/after pairs provide calibration anchors)
3. On-demand: `references/boundary-conditions.md` (boundary violations are automatic zero-scores)
4. On-demand: `references/audience-adaptation.md` (context-appropriate scoring)
5. On-demand: `references/biographical-context.md` (McConkey plausibility test calibration)

**Tools needed:** Read, Write, Edit, Glob, Grep

**Model:** sonnet (analytical scoring with leniency bias counteraction, consistent with adv-scorer)

**Key behavior:** Score each of the 5 voice traits independently on 0-1 scale:
- Direct (0-1)
- Warm (0-1)
- Confident (0-1)
- Occasionally Absurd (0-1, context-dependent -- a score of 0 is correct in "no humor" contexts)
- Technically Precise (0-1)

Compute unweighted average for composite voice fidelity score. Apply leniency bias counteraction per adv-scorer patterns. A voice fidelity score of 0.90+ means the text genuinely embodies the persona. Most first attempts score 0.60-0.75.

**Output:** Voice fidelity score report with per-trait scores, evidence, and improvement guidance.

### Agent Integration with Existing Skills

| Integration | Mechanism | Details |
|-------------|-----------|---------|
| /adversary (adv-scorer) | Persona compliance as optional quality dimension | sb-calibrator voice fidelity score can be reported alongside the 6 SSOT dimensions. Not a replacement -- an additional signal. |
| /adversary (adv-executor) | Strategy templates may reference voice compliance | S-007 Constitutional AI Critique could check persona boundary conditions. |
| /problem-solving (ps-critic) | Creator-critic loop for voice rewrites | ps-critic iterations on voice quality, using sb-reviewer findings as critic input. |
| /orchestration | Phase gate persona check | Orchestration quality gates can include sb-calibrator scoring at barrier transitions. |

---

## Research Question 4: Integration Points

### FEAT-004: Framework Voice and Personality

**Integration mechanism:** FEAT-004 is the primary consumer. It uses /saucer-boy as follows:

1. Take each class of framework output (quality gate messages, error messages, session messages, etc.)
2. Use sb-rewriter to transform current voice to Saucer Boy voice
3. Use sb-reviewer to validate the rewrite passes all 5 Authenticity Tests
4. Use sb-calibrator to quantitatively score the rewrite

The `references/implementation-notes.md` file contains FEAT-004-specific guidance including priority order for rewriting and the biographical voice calibration anchor.

### FEAT-007: Developer Experience Delight

**Integration mechanism:** FEAT-007 consumes the persona through /saucer-boy for:

1. Session start/end messages (sb-rewriter for tone)
2. Celebration messages (sb-rewriter with "Full energy" humor context)
3. Streak acknowledgments (sb-rewriter with contextual awareness)
4. 3 AM commit detection (sb-rewriter with "dry acknowledgment" tone)

The `references/implementation-notes.md` file contains FEAT-007-specific guidance including high-value delight moments and delight principles.

### FEAT-006: Easter Eggs and Cultural References

**Integration mechanism:** FEAT-006 uses /saucer-boy for:

1. Easter egg text validation via sb-reviewer (must pass all 5 Authenticity Tests)
2. Cultural reference appropriateness check against `references/cultural-palette.md`
3. Calibration against the concrete in-situ example (persona doc lines 698-712)

The `references/implementation-notes.md` file contains FEAT-006-specific guidance including high-value territories and the calibration example with before/after code snippet.

### /adversary Integration: Persona Compliance as Quality Dimension

**Proposed integration pattern:**

Persona compliance is NOT a replacement for the 6 SSOT quality dimensions. It is an additional, optional dimension that can be scored alongside the standard quality gate for deliverables that include framework voice output.

| Aspect | Standard Quality Gate | With Persona Compliance |
|--------|----------------------|------------------------|
| Dimensions | 6 (Completeness through Traceability) | 6 + voice fidelity (optional 7th) |
| Threshold | >= 0.92 weighted composite | Standard threshold applies to 6 dimensions; voice fidelity is informational |
| Agent | adv-scorer | adv-scorer + sb-calibrator |
| When applied | All C2+ deliverables | Deliverables containing framework voice output |

**Governance note:** Adding persona compliance as a formal 7th dimension to the quality gate would require modifying `quality-enforcement.md`, triggering AE-002 (auto-C3) and potentially AE-004 if it changes the SSOT thresholds. The recommended approach is to keep it as an informational signal that is reported but not gated on, avoiding governance escalation.

### CLI Output Hook (Future)

The /saucer-boy skill could be invoked by a hook that intercepts CLI output before display and applies voice transformation. This is a FEAT-007 implementation detail, not a /saucer-boy architecture concern. The skill just needs to expose a clean interface for text-in, voice-transformed-text-out.

---

## Research Question 5: SKILL.md Content Strategy

### DEC-001 D-003 Mandate

DEC-001 D-003 states: "SKILL.md contains the Authenticity Tests (hard gates), Core Thesis, Voice Traits table, and agent registry. References carry the before/after voice pairs, humor deployment rules, cultural palette, and implementation notes."

### Decision Rules for SKILL.md (Extracted from Persona Doc)

The following items are "decision rules" -- content that an agent needs on every invocation to make pass/fail or style decisions. These go in SKILL.md per D-003.

**1. Core Thesis (lines 41-53, 13 lines)**

The load-bearing sentence: "Joy and excellence are not trade-offs. They're multipliers." Plus the operational paragraph explaining that quality gates stay rigorous; only the voice changes. And the clarification that joy is not synonymous with humor.

**2. Voice Traits Table (lines 101-112, 12 lines)**

The 5-trait table (Direct, Warm, Confident, Occasionally Absurd, Technically Precise) with definitions and "In Practice" examples. This is the scoring rubric for sb-calibrator and the evaluation framework for sb-reviewer.

**3. Tone Spectrum (lines 113-126, 14 lines)**

The spectrum from "Full Energy" (celebration) to "Diagnostic" (hard stop) with the key rule: "The voice never goes flat."

**4. Humor Deployment Rules Table (lines 141-163, 23 lines)**

The context-to-humor mapping table (quality gate PASS = yes, constitutional failure = none, etc.) plus the "when earned" criterion and the "light tone" clarification. This is a decision gate.

**5. Energy Calibration (lines 158-163, 6 lines)**

The principle: energy should scale with the moment. Consistent high energy reads as hollow.

**6. Boundary Condition Summaries (lines 389-448, condensed to ~30 lines)**

The 7 NOT conditions as one-line summaries:
- NOT Sarcastic
- NOT Dismissive of Rigor
- NOT Unprofessional in High-Stakes Moments
- NOT Bro-Culture Adjacent
- NOT Performative Quirkiness
- NOT a Character Override of Claude (critical governance boundary)
- NOT a Replacement for Information
- NOT Mechanical Assembly

Each with a one-line summary. Full explanations live in `references/boundary-conditions.md`.

**7. Audience Adaptation Matrix (lines 509-523, 15 lines)**

The 11-row matrix mapping context to energy/humor/technical depth/tone anchor. This is the primary decision table for sb-reviewer and sb-rewriter.

**8. Authenticity Test (lines 789-803, 15 lines)**

The 5-test ordered gate:
1. Information completeness (HARD gate -- stop if fail)
2. McConkey plausibility
3. New developer legibility
4. Context match
5. Genuine conviction

Plus the meta-rule: a clear, dry message is better than a strained personality message.

**9. Agent Registry (new content, ~20 lines)**

Table listing sb-reviewer, sb-rewriter, sb-calibrator with roles, models, and invocation patterns.

**Estimated SKILL.md total:** ~200 lines (consistent with DISC-001 projection and within the Anthropic <500 line recommendation).

### Examples for references/ (Extracted from Persona Doc)

These are "example content" -- material that agents load selectively based on their specific task.

| Reference File | Content | Primary Consumer Agent |
|---------------|---------|----------------------|
| voice-guide.md | 9 before/after pairs (quality gate PASS, FAIL-REVISE, FAIL-REJECTED, error message, session start, constitutional failure, celebration, rule explanation, DX delight) | sb-rewriter (calibration standard), sb-calibrator (scoring anchors) |
| biographical-context.md | McConkey story, framework inheritance, risk exclusion | sb-calibrator (McConkey plausibility test), sb-rewriter (biographical voice anchor) |
| humor-deployment.md | Structural comedy and deadpan delivery modes with examples | sb-rewriter (humor generation), sb-reviewer (humor validation) |
| boundary-conditions.md | Full 7-subsection boundary explanations | sb-reviewer (boundary violation detection) |
| cultural-palette.md | In-bounds/out-of-bounds tables for skiing, music, film, counter-culture | sb-rewriter (cultural reference selection), sb-reviewer (reference validation) |
| audience-adaptation.md | Audience-specific elaboration notes | sb-rewriter (audience-tailored output), sb-reviewer (context validation) |
| visual-vocabulary.md | ASCII, emoji, formatting, terminal color guidance | sb-rewriter (formatting decisions) |
| implementation-notes.md | FEAT-002 through FEAT-007 specific guidance | All agents (when working on specific downstream features) |
| vocabulary-reference.md | Preferred terms, forbidden constructions, skiing vocabulary | sb-rewriter (vocabulary selection), sb-reviewer (vocabulary validation) |

---

## Research Question 6: YAML Frontmatter

### Anthropic Official Format (from WS-1, WS-2, WS-3)

The Anthropic skill standard requires the following frontmatter structure:

```yaml
---
name: skill-name          # Required. Lowercase, numbers, hyphens only. Max 64 chars.
description: "..."        # Recommended. Max 1024 chars. What it does + when to use it.
---
```

Optional fields per the Anthropic standard:
- `disable-model-invocation` -- boolean, prevents auto-triggering
- `user-invocable` -- boolean, hides from / menu
- `allowed-tools` -- tool restriction list
- `model` -- model override
- `context` -- `fork` for subagent execution
- `agent` -- subagent type selection
- `hooks` -- skill-scoped hooks

### Jerry-Specific Extensions

Jerry skills extend the Anthropic base with:
- `version` -- semantic version string
- `activation-keywords` -- list of trigger phrases (all 4 existing skills use this)

### Proposed /saucer-boy Frontmatter

```yaml
---
name: saucer-boy
description: >-
  Voice quality gate for the Saucer Boy persona. Reviews, rewrites, and scores
  framework output text for persona compliance using the Shane McConkey ethos:
  joy and excellence as multipliers. Use when checking voice compliance of
  quality gate messages, error messages, CLI output, hook text, documentation
  comments, or any framework-generated text that developers read.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep
activation-keywords:
  - "saucer boy"
  - "saucer-boy"
  - "voice check"
  - "voice review"
  - "persona compliance"
  - "persona check"
  - "voice rewrite"
  - "voice fidelity"
  - "voice score"
  - "mcconkey"
  - "framework voice"
  - "saucer boy review"
  - "persona review"
---
```

**Design decisions in this frontmatter:**

1. **`name: saucer-boy`** -- Matches the `/saucer-boy` invocation pattern from EPIC-001. Lowercase with hyphen per Anthropic naming rules [WS-2].

2. **`description`** -- Includes what (voice quality gate) + when (quality gate messages, error messages, etc.) per Anthropic best practice [WS-2]. Written in third person per Anthropic guidance: "Reviews, rewrites, and scores" not "I review, rewrite, and score."

3. **`activation-keywords`** -- Jerry extension. Includes both the persona name and the functional actions (voice check, voice review, persona compliance) to maximize discoverability.

4. **`allowed-tools`** -- Read, Write, Edit for text transformation; Glob, Grep for file discovery. No WebSearch/WebFetch needed (persona is self-contained). No Task/Bash needed (agents are invoked by main context per P-003).

5. **No `disable-model-invocation`** -- The skill SHOULD be auto-triggerable when Claude detects voice-related context. This aligns with H-22 (proactive skill invocation).

6. **No `context: fork`** -- The skill should run inline so its agents can access conversation context. Voice review needs to see what the developer is working on.

---

## Proposed Directory Structure

```
skills/saucer-boy/
├── SKILL.md                              # ~200 lines
│   ├── YAML frontmatter (name, description, version, allowed-tools, activation-keywords)
│   ├── Purpose
│   ├── When to Use / When NOT to Use
│   ├── Core Thesis (13 lines from persona doc)
│   ├── Voice Traits Table (12 lines)
│   ├── Tone Spectrum (14 lines)
│   ├── Humor Deployment Rules (23 lines)
│   ├── Energy Calibration (6 lines)
│   ├── Boundary Conditions (condensed, ~30 lines)
│   ├── Audience Adaptation Matrix (15 lines)
│   ├── Authenticity Test (15 lines)
│   ├── Available Agents (registry table)
│   ├── P-003 Compliance diagram
│   ├── Invoking an Agent
│   └── References (pointers to reference files)
│
├── references/
│   ├── voice-guide.md                    # ~200 lines — 9 before/after pairs
│   ├── biographical-context.md           # ~50 lines — McConkey story, inheritance
│   ├── humor-deployment.md               # ~40 lines — comedy modes with examples
│   ├── boundary-conditions.md            # ~70 lines — full 7-subsection explanations
│   ├── cultural-palette.md               # ~60 lines — in-bounds/out-of-bounds tables
│   ├── audience-adaptation.md            # ~40 lines — audience-specific elaboration
│   ├── visual-vocabulary.md              # ~70 lines — ASCII, emoji, formatting, colors
│   ├── implementation-notes.md           # ~120 lines — FEAT-002 through FEAT-007 guidance
│   └── vocabulary-reference.md           # ~60 lines — terms, constructions, skiing vocab
│
├── agents/
│   ├── sb-reviewer.md                    # ~350 lines — voice compliance reviewer
│   ├── sb-rewriter.md                    # ~350 lines — voice transformation agent
│   └── sb-calibrator.md                  # ~350 lines — voice fidelity scorer
│
└── assets/
    └── (reserved for FEAT-003 visual identity: ASCII logo, etc.)
```

**File count:** 13 files (1 SKILL.md + 9 references + 3 agents)
**Estimated total lines:** ~1,950 (200 + 710 + 1,050)

### Reference File Loading Matrix

This table shows which reference files each agent loads and when. It serves as the primary input for ps-creator-002 when building agent files.

| Reference File | sb-reviewer | sb-rewriter | sb-calibrator | Load Trigger |
|---------------|-------------|-------------|---------------|-------------|
| voice-guide.md | On-demand | **Always** | **Always** | Rewriter and calibrator need calibration anchors; reviewer loads when checking specific pair patterns |
| biographical-context.md | Never | On-demand | On-demand | When McConkey plausibility test (Authenticity Test 2) needs calibration |
| humor-deployment.md | On-demand | On-demand | Never | When humor content is present or expected |
| boundary-conditions.md | On-demand | Never | On-demand | When boundary violation detected or suspected |
| cultural-palette.md | On-demand | On-demand | Never | When cultural references are present or being generated |
| audience-adaptation.md | On-demand | On-demand | On-demand | When audience context needs elaboration beyond the matrix |
| visual-vocabulary.md | Never | On-demand | Never | When formatting/ASCII/emoji decisions are involved |
| implementation-notes.md | On-demand | On-demand | On-demand | When working on a specific FEAT (002-007) |
| vocabulary-reference.md | On-demand | **Always** | Never | Rewriter always needs vocabulary guidance; reviewer loads when checking vocabulary |

---

## Design Constraints Summary

These are binding decisions from Phase 1 that ps-creator-002 must respect.

| Constraint | Source | Summary |
|-----------|--------|---------|
| DEC-001 D-001 | DISC-001, DEC-001 | Progressive Disclosure: SKILL.md (<5k words) + references/ (on-demand) + agents/ |
| DEC-001 D-002 | DEC-001 | Persona doc remains canonical source; skill files are operationalized derivatives |
| DEC-001 D-003 | DEC-001 | SKILL.md carries decision rules; references/ carries examples |
| Boundary: Not a Claude personality modifier | Persona doc lines 430-436 | The skill implements voice quality gate for framework outputs, NOT a Claude personality layer |
| Authenticity Test ordering | Persona doc lines 789-803 | Test 1 (information completeness) is a hard gate; do not evaluate Tests 2-5 until Test 1 passes |
| Persona doc is canonical | DEC-001 D-002 | Do not modify persona doc; extract and operationalize |
| H-23/H-24 compliance | quality-enforcement.md | All files over 30 lines need navigation tables with anchor links |
| P-003 compliance | CLAUDE.md | Agents are workers, not orchestrators; no recursive subagents |
| Anthropic SKILL.md < 500 lines | WS-1, WS-2 | Keep SKILL.md focused; move detail to reference files |

---

## Web Sources

| ID | Title | URL | Used For |
|----|-------|-----|----------|
| WS-1 | Extend Claude with skills -- Claude Code Docs | https://code.claude.com/docs/en/skills | Official skill directory structure, frontmatter fields, progressive disclosure architecture, supporting files pattern, keep SKILL.md under 500 lines recommendation |
| WS-2 | Skill authoring best practices -- Claude API Docs | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Conciseness principles, progressive disclosure patterns (high-level guide, domain-specific, conditional details), naming conventions (lowercase/hyphens/max 64), description in third person, reference files one level deep, 500-line limit, avoid deeply nested references |
| WS-3 | skill-creator SKILL.md -- anthropics/skills GitHub | https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md | Canonical skill anatomy (SKILL.md + scripts/ + references/ + assets/), references/ described as "documentation intended to be loaded into context as needed", grep search patterns for large reference files, do not create extraneous docs (README, CHANGELOG, etc.) |
| WS-4 | Equipping agents for the real world with Agent Skills -- Anthropic Engineering | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Progressive disclosure as core design principle, metadata pre-loading at startup (~50-100 tokens per skill), context penalty only when files are read |
| WS-5 | The Complete Guide to Building Skills for Claude (PDF) | https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en | 32-page comprehensive guide published January 29, 2026; validates 3-tier progressive disclosure pattern |
| WS-6 | Agent Skills overview -- Claude API Docs | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Open standard (agentskills.io), enterprise deployment, skill discovery mechanism |

All web sources accessed 2026-02-19.

---

## Internal Sources

| Path | Used For |
|------|----------|
| `projects/PROJ-003-je-ne-sais-quoi/work/EPIC-001-je-ne-sais-quoi/EPIC-001--DISC-001-progressive-disclosure-skill-decomposition.md` | Progressive disclosure discovery; 3-tier architecture; proposed decomposition; agent-specific loading patterns |
| `projects/PROJ-003-je-ne-sais-quoi/work/EPIC-001-je-ne-sais-quoi/EPIC-001--DEC-001-feat002-progressive-disclosure.md` | Architecture decisions D-001 (progressive disclosure), D-002 (persona doc canonical), D-003 (decision rules vs examples) |
| `projects/PROJ-003-je-ne-sais-quoi/orchestration/jnsq-20260219-001/jnsq/phase-1-persona-distillation/ps-creator-001/ps-creator-001-draft.md` | Persona doc v0.9.0 (879 lines); canonical source for all decomposition |
| `skills/adversary/SKILL.md` | Audit: 427 lines, triple-lens, P-003 diagram, strategy template references, agent registry |
| `skills/adversary/agents/adv-scorer.md` | Audit: agent file structure pattern (YAML frontmatter + XML body) |
| `skills/problem-solving/SKILL.md` | Audit: 441 lines, triple-lens, 9 agents, adversarial quality mode, output templates |
| `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` | Audit: federated core template with extension points |
| `skills/worktracker/SKILL.md` | Audit: 198 lines, @import pattern for always-loaded rules, 3 agents |
| `skills/orchestration/SKILL.md` | Audit: 690 lines, P-003 diagram, state schema, quality gates, dynamic paths |
| `projects/PROJ-003-je-ne-sais-quoi/work/EPIC-001-je-ne-sais-quoi/EPIC-001-je-ne-sais-quoi.md` | Parent epic; feature inventory, soundtrack, design rationale |
| `.context/rules/quality-enforcement.md` | SSOT for quality gate, criticality levels, strategy catalog, enforcement architecture |

---

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Version | 1.0.0 |
| Status | COMPLETE |
| Agent | ps-researcher-002 |
| Workflow | jnsq-20260219-001 |
| Phase | 2 -- Tier 1 Fan-Out |
| Date | 2026-02-19 |
| Criticality | C3 (Significant) |
| Research scope | 4 skills audited, 879-line persona doc analyzed, 6 web sources, 11 internal sources |
| Next step | ps-creator-002 uses this artifact to construct skills/saucer-boy/ |

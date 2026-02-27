# Diataxis Quality Criteria Reference

> Quality criteria, anti-pattern identifiers, and detection heuristics for the four Diataxis documentation quadrants.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (R-01 through R-07) -->
<!-- Anti-patterns to avoid: RAP-01 (marketing claims), RAP-02 (instructions/recipes), RAP-03 (narrative explanation) -->
<!-- Voice: Neutral, precise, austere. No opinions, no superlatives. See Section 5. -->

## Overview

This reference covers the quality criteria and anti-pattern identifiers defined in `skills/diataxis/rules/diataxis-standards.md`. Each quadrant has 7 quality criteria (pass/fail) and 5 anti-patterns (severity-classified). Detection heuristics provide automated quadrant-mixing signals.

## Tutorial Quality Criteria

<!-- R-01: Category names MUST mirror the described system's own structure. -->

### `T-01`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

Completable end-to-end. A reader with stated prerequisites can finish without external help.

**Pass condition:** Zero dead ends or ambiguous steps.

**Example:**

```
Pass: Step 3 says "Run `npm install`" and Step 4 says "You should see `added 42 packages`."
Fail: Step 3 says "Install dependencies" with no command or expected output.
```

### `T-02`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

Every step has visible result. Each numbered step produces output the reader can observe.

**Pass condition:** No "invisible" steps.

**Example:**

```
Pass: "Run `git status`. You should see `On branch main`."
Fail: "Initialize the internal state." (no observable output)
```

### `T-03`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

No unexplained steps. No step requires knowledge not introduced earlier in the tutorial. External knowledge in a referenced prerequisites block is excluded.

**Pass condition:** Zero assumed competencies beyond prerequisites.

### `T-04`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

No alternatives offered. Tutorial presents exactly one path. Exception: OS-conditional paths (macOS/Windows/Linux) are legitimate platform branching.

**Pass condition:** Zero "alternatively" or "you could also" constructions.

### `T-05`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

Concrete not abstract. Steps reference specific values, files, commands.

**Pass condition:** Zero placeholder-only instructions.

### `T-06`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

Prerequisites stated. A clear prerequisites block lists what the reader needs before starting.

**Pass condition:** Prerequisites block exists.

### `T-07`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

Endpoint shown upfront. Reader knows what they will achieve before starting.

**Pass condition:** "What you will achieve" section exists.

### `T-08`

**Type:** Quality criterion
**Quadrant:** Tutorial
**Since:** v0.1.0

Reliable reproduction. Following the steps produces the documented outcome.

**Pass condition:** Author has verified steps produce the documented result, or steps are flagged `[UNTESTED]`.

## How-To Guide Quality Criteria

### `H-01`

**Type:** Quality criterion
**Quadrant:** How-To Guide
**Since:** v0.1.0

Goal stated in title. Title begins with "How to" or states the achievable outcome.

**Pass condition:** Title is goal-framed. If H-01 and H-07 conflict, H-07 takes precedence.

### `H-02`

**Type:** Quality criterion
**Quadrant:** How-To Guide
**Since:** v0.1.0

Action-only content. No explanatory paragraphs between steps. Conditional branches (H-03) are action content, not explanation.

**Pass condition:** Zero digressions exceeding 2 sentences between imperative steps without action verbs.

### `H-03`

**Type:** Quality criterion
**Quadrant:** How-To Guide
**Since:** v0.1.0

Addresses real-world variations. Conditional branches for common variations.

**Pass condition:** At minimum one "If you need X, do Y" variant.

### `H-04`

**Type:** Quality criterion
**Quadrant:** How-To Guide
**Since:** v0.1.0

No teaching or explaining. Does not introduce foundational concepts.

**Pass condition:** Zero pedagogical content.

### `H-05`

**Type:** Quality criterion
**Quadrant:** How-To Guide
**Since:** v0.1.0

Achieves flow. Steps progress smoothly without unexpected context switches.

**Pass condition:** No back-tracking or "first, go back and..." patterns.

### `H-06`

**Type:** Quality criterion
**Quadrant:** How-To Guide
**Since:** v0.1.0

Assumes competence. Does not explain obvious interface elements.

**Pass condition:** Zero "click Save to save" patterns.

### `H-07`

**Type:** Quality criterion
**Quadrant:** How-To Guide
**Since:** v0.1.0

Problem-field framing. Written from user's perspective, not tool's.

**Pass condition:** Title describes user goal, not tool operation.

## Reference Quality Criteria

### `R-01`

**Type:** Quality criterion
**Quadrant:** Reference
**Since:** v0.1.0

Mirrors described structure. Documentation organization aligns with the machinery described.

**Pass condition:** Section hierarchy matches the structure of the described system.

### `R-02`

**Type:** Quality criterion
**Quadrant:** Reference
**Since:** v0.1.0

Wholly authoritative. No hedging or uncertainty in descriptions.

**Pass condition:** Zero hedging language ("might", "probably", "should work").

### `R-03`

**Type:** Quality criterion
**Quadrant:** Reference
**Since:** v0.1.0

Complete specification. Every parameter, field, and option fully specified with type, default, and constraints.

**Pass condition:** Zero undocumented fields or parameters.

### `R-04`

**Type:** Quality criterion
**Quadrant:** Reference
**Since:** v0.1.0

Neutral tone. No opinions, marketing, or subjective claims.

**Pass condition:** Zero superlatives or comparative claims.

### `R-05`

**Type:** Quality criterion
**Quadrant:** Reference
**Since:** v0.1.0

Standard formatting. All entries follow the same structure.

**Pass condition:** Consistent entry template across all items.

### `R-06`

**Type:** Quality criterion
**Quadrant:** Reference
**Since:** v0.1.0

Examples included. Usage examples illustrate without instructing.

**Pass condition:** At minimum one example per major entry.

### `R-07`

**Type:** Quality criterion
**Quadrant:** Reference
**Since:** v0.1.0

Complete coverage. All elements of the described system are documented.

**Pass condition:** Zero undocumented public interfaces.

## Explanation Quality Criteria

### `E-01`

**Type:** Quality criterion
**Quadrant:** Explanation
**Since:** v0.1.0

Discursive (not procedural). Continuous prose, no numbered step sequences. Numbered concept lists enumerating reasons or principles are permitted.

**Pass condition:** Zero numbered procedure lists.

### `E-02`

**Type:** Quality criterion
**Quadrant:** Explanation
**Since:** v0.1.0

Makes connections. Links concepts across topics and domains with substantive relationship explanation.

**Pass condition:** At minimum two cross-references, each with a sentence explaining the relationship.

### `E-03`

**Type:** Quality criterion
**Quadrant:** Explanation
**Since:** v0.1.0

Provides context. Includes design decisions, history, or constraints.

**Pass condition:** Context section present.

### `E-04`

**Type:** Quality criterion
**Quadrant:** Explanation
**Since:** v0.1.0

Acknowledges perspective. Admits opinions or multiple valid approaches.

**Pass condition:** At minimum one alternative viewpoint.

### `E-05`

**Type:** Quality criterion
**Quadrant:** Explanation
**Since:** v0.1.0

Enriches understanding. Reader learns *why*, not just *what*.

**Pass condition:** "Why" or "because" reasoning present.

### `E-06`

**Type:** Quality criterion
**Quadrant:** Explanation
**Since:** v0.1.0

Bounded scope. Does not try to cover everything.

**Pass condition:** Clear topic boundary stated.

### `E-07`

**Type:** Quality criterion
**Quadrant:** Explanation
**Since:** v0.1.0

No imperative instructions. Does not tell the reader to do something.

**Pass condition:** Zero "Run this command" or "Configure X" directives.

## Tutorial Anti-Patterns

### `TAP-01`

**Type:** Anti-pattern
**Quadrant:** Tutorial
**Severity:** Major

Abstraction. Generalizations replace concrete steps.

### `TAP-02`

**Type:** Anti-pattern
**Quadrant:** Tutorial
**Severity:** Major

Extended explanation. "Why" paragraphs between steps.

### `TAP-03`

**Type:** Anti-pattern
**Quadrant:** Tutorial
**Severity:** Major

Offering choices. "Alternatively" or "Option A/B" constructions.

### `TAP-04`

**Type:** Anti-pattern
**Quadrant:** Tutorial
**Severity:** Minor

Information overload. Step has 3+ sub-points or nested lists.

### `TAP-05`

**Type:** Anti-pattern
**Quadrant:** Tutorial
**Severity:** Major

Untested steps. Steps that may fail on reader's environment.

## How-To Guide Anti-Patterns

### `HAP-01`

**Type:** Anti-pattern
**Quadrant:** How-To Guide
**Severity:** Major

Conflating with tutorial. "Let me explain..." or foundational teaching.

### `HAP-02`

**Type:** Anti-pattern
**Quadrant:** How-To Guide
**Severity:** Minor

Tool-focused guidance. Title names the tool rather than the user's goal.

### `HAP-03`

**Type:** Anti-pattern
**Quadrant:** How-To Guide
**Severity:** Minor

Unnecessary procedures. Steps that a competent practitioner already knows.

### `HAP-04`

**Type:** Anti-pattern
**Quadrant:** How-To Guide
**Severity:** Major

Completeness over focus. Documenting every edge case rather than the main path.

### `HAP-05`

**Type:** Anti-pattern
**Quadrant:** How-To Guide
**Severity:** Minor

Embedded reference. Full parameter tables inline.

## Reference Anti-Patterns

### `RAP-01`

**Type:** Anti-pattern
**Quadrant:** Reference
**Severity:** Major

Marketing claims. Superlatives ("best", "fastest", "powerful").

### `RAP-02`

**Type:** Anti-pattern
**Quadrant:** Reference
**Severity:** Major

Instructions/recipes. Numbered step lists within reference entries.

### `RAP-03`

**Type:** Anti-pattern
**Quadrant:** Reference
**Severity:** Minor

Narrative explanation. Multi-paragraph "why" blocks in reference.

### `RAP-04`

**Type:** Anti-pattern
**Quadrant:** Reference
**Severity:** Minor

Stylistic flourishes. Metaphors, humor, or personality in reference.

### `RAP-05`

**Type:** Anti-pattern
**Quadrant:** Reference
**Severity:** Major

Auto-gen only. Machine-generated docs with no human curation.

## Explanation Anti-Patterns

### `EAP-01`

**Type:** Anti-pattern
**Quadrant:** Explanation
**Severity:** Minor (1-2 instances) / Major (3+ instances)

Instructional creep. Imperative verbs ("Run this", "Configure that"). Minor for 1-2 isolated instances; Major for 3+ instances or when imperative verbs form a procedural sequence.

### `EAP-02`

**Type:** Anti-pattern
**Quadrant:** Explanation
**Severity:** Major

Scattered across sections. Explanation fragments buried in other doc types.

### `EAP-03`

**Type:** Anti-pattern
**Quadrant:** Explanation
**Severity:** Minor

Treated as less important. Explanation section is thin or absent.

### `EAP-04`

**Type:** Anti-pattern
**Quadrant:** Explanation
**Severity:** Minor

No perspective. Reads like reference -- flat, neutral, no voice.

### `EAP-05`

**Type:** Anti-pattern
**Quadrant:** Explanation
**Severity:** Major

Unbounded scope. Tries to cover everything about a topic.

<!-- R-07 Completeness Checklist: All 28 quality criteria (4 quadrants x 7) and 20 anti-patterns (4 quadrants x 5) documented. -->

## Related

- **Tutorial:** [Learn to create a Jerry skill](tutorial-create-jerry-skill.md) -- Guided introduction to skill creation
- **How-To Guide:** [How to register a skill](howto-register-skill.md) -- Task-oriented registration steps
- **Explanation:** [About Jerry's Context Rot Problem](explanation-context-rot.md) -- Design rationale and context

# Diataxis Documentation Standards

> Quality criteria, anti-patterns, detection heuristics, classification guide, and voice guidelines for the `/diataxis` skill. All writer agents MUST reference this file.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Section 1: Per-Quadrant Quality Criteria](#section-1-per-quadrant-quality-criteria) | Required quality criteria per documentation type |
| -- [Tutorial Quality Criteria](#tutorial-quality-criteria) | T-01 through T-08 |
| -- [How-To Guide Quality Criteria](#how-to-guide-quality-criteria) | H-01 through H-07 |
| -- [Reference Quality Criteria](#reference-quality-criteria) | R-01 through R-07 |
| -- [Explanation Quality Criteria](#explanation-quality-criteria) | E-01 through E-07 |
| [Section 2: Per-Quadrant Anti-Patterns](#section-2-per-quadrant-anti-patterns) | Common failures per documentation type |
| -- [Tutorial Anti-Patterns](#tutorial-anti-patterns) | TAP-01 through TAP-05 |
| -- [How-To Guide Anti-Patterns](#how-to-guide-anti-patterns) | HAP-01 through HAP-05 |
| -- [Reference Anti-Patterns](#reference-anti-patterns) | RAP-01 through RAP-05 |
| -- [Explanation Anti-Patterns](#explanation-anti-patterns) | EAP-01 through EAP-05 |
| [Section 3: Detection Heuristics](#section-3-detection-heuristics-for-quadrant-mixing) | Signal-based quadrant mixing detection |
| [Section 4: Classification Decision Guide](#section-4-classification-decision-guide) | How to classify documentation requests |
| [Section 5: Jerry Voice Guidelines](#section-5-jerry-voice-guidelines) | Per-quadrant prose style for Jerry output |

---

## Section 1: Per-Quadrant Quality Criteria

### Tutorial Quality Criteria

| # | Criterion | Test | Pass Condition |
|---|-----------|------|----------------|
| T-01 | Completable end-to-end | A reader with stated prerequisites can finish without external help | Zero dead ends or ambiguous steps |
| T-02 | Every step has visible result | Each numbered step produces output the reader can observe | No "invisible" steps |
| T-03 | No unexplained steps | No step requires knowledge not introduced earlier in the tutorial. "Earlier" means content appearing before the current step within this document. External knowledge in a referenced prerequisites block or linked document is excluded. | Zero assumed competencies beyond prerequisites |
| T-04 | No alternatives offered | Tutorial presents exactly one path | Zero "alternatively" or "you could also" constructions. Exception: OS-conditional paths (macOS/Windows/Linux) are legitimate platform branching per the False-Positive Handling Protocol, not alternatives. |
| T-05 | Concrete not abstract | Steps reference specific values, files, commands | Zero placeholder-only instructions |
| T-06 | Prerequisites stated | A clear prerequisites block lists what the reader needs before starting | Prerequisites block exists |
| T-07 | Endpoint shown upfront | Reader knows what they will achieve before starting | "What you will achieve" section exists |
| T-08 | Reliable reproduction | Following the steps produces the documented outcome | Author has verified steps produce the documented result, or steps are flagged `[UNTESTED]` |

### How-To Guide Quality Criteria

| # | Criterion | Test | Pass Condition |
|---|-----------|------|----------------|
| H-01 | Goal stated in title | Title begins with "How to" or states the achievable outcome | Title is goal-framed. Note: If H-01 and H-07 conflict, H-07 (user goal framing) takes precedence. H-01 is a recommended pattern. |
| H-02 | Action-only content | No explanatory paragraphs between steps. Conditional branches (H-03) are action content, not explanation — "If you need X, do Y" is compliant. | Zero "why" digressions (3+ sentences explaining rationale without action verbs). 1-2 sentence digressions are below mandatory-flag threshold. A digression "interrupts action flow" when it appears between two imperative steps and contains zero action verbs — flag as Minor if it exceeds 2 sentences. |
| H-03 | Addresses real-world variations | Conditional branches for common variations | At minimum one "If you need X, do Y" variant. Note: A real-world variation is a conditional path during normal task execution (e.g., OS-specific commands, optional auth steps). Edge cases (rare/exceptional conditions) are out of scope -- see HAP-04. One conditional branch satisfies H-03 without triggering HAP-04. |
| H-04 | No teaching or explaining | Does not introduce foundational concepts | Zero pedagogical content |
| H-05 | Achieves flow | Steps progress smoothly without unexpected context switches | No back-tracking or "first, go back and..." |
| H-06 | Assumes competence | Does not explain obvious interface elements | Zero "click Save to save" patterns |
| H-07 | Problem-field framing | Written from user's perspective, not tool's | Title describes user goal, not tool operation |

### Reference Quality Criteria

| # | Criterion | Test | Pass Condition |
|---|-----------|------|----------------|
| R-01 | Mirrors described structure | Documentation organization aligns with the machinery described. For non-code reference (CLI, configuration, entities), interpret as command hierarchy, config schema, or entity model. | Section hierarchy matches the structure of the described system |
| R-02 | Wholly authoritative | No hedging or uncertainty in descriptions | Zero hedging language ("might", "probably", "should work") |
| R-03 | Complete specification | Every parameter, field, and option fully specified with type, default, and constraints | Zero undocumented fields or parameters |
| R-04 | Neutral tone | No opinions, marketing, or subjective claims | Zero superlatives or comparative claims |
| R-05 | Standard formatting | All entries follow the same structure | Consistent entry template across all items |
| R-06 | Examples included | Usage examples illustrate without instructing | At minimum one example per major entry |
| R-07 | Complete coverage | All elements of the described system are documented | Zero undocumented public interfaces |

### Explanation Quality Criteria

| # | Criterion | Test | Pass Condition |
|---|-----------|------|----------------|
| E-01 | Discursive (not procedural) | Continuous prose, no numbered step sequences | Zero numbered procedure lists (numbered lists where each item is an action the reader performs in sequence). Numbered concept lists enumerating reasons, principles, or conceptual items are permitted. |
| E-02 | Makes connections | Links concepts across topics and domains with substantive relationship explanation | At minimum two cross-references, each with a sentence explaining how the topics relate |
| E-03 | Provides context | Includes design decisions, history, or constraints | Context section present |
| E-04 | Acknowledges perspective | Admits opinions or multiple valid approaches | At minimum one "however" or alternative viewpoint |
| E-05 | Enriches understanding | Reader learns *why*, not just *what* | "Why" or "because" reasoning present |
| E-06 | Bounded scope | Does not try to cover everything | Clear topic boundary stated |
| E-07 | No imperative instructions | Does not tell the reader to do something | Zero "Run this command" or "Configure X" |

---

## Section 2: Per-Quadrant Anti-Patterns

### Tutorial Anti-Patterns

| ID | Anti-Pattern | Detection Signal | Severity |
|----|-------------|-----------------|----------|
| TAP-01 | Abstraction | Generalizations replace concrete steps | Major |
| TAP-02 | Extended explanation | "Why" paragraphs between steps | Major |
| TAP-03 | Offering choices | "Alternatively" or "Option A/B" constructions | Major |
| TAP-04 | Information overload | Step has 3+ sub-points or nested lists | Minor |
| TAP-05 | Untested steps | Steps that may fail on reader's environment (detected by: version-specific commands without version note, platform-specific paths without OS conditional, hardcoded credentials or paths) | Major |

### How-To Guide Anti-Patterns

| ID | Anti-Pattern | Detection Signal | Severity |
|----|-------------|-----------------|----------|
| HAP-01 | Conflating with tutorial | "Let me explain..." or foundational teaching | Major |
| HAP-02 | Tool-focused guidance | Title names the tool rather than the user's goal | Minor |
| HAP-03 | Unnecessary procedures | Steps that a competent practitioner at the guide's stated audience level already knows | Minor |
| HAP-04 | Completeness over focus | Documenting every edge case rather than the main path. Note: Edge cases are rare/exceptional conditions the main task path never requires. This is complementary to H-03 -- one real-world variation satisfies H-03 without triggering HAP-04. | Major |
| HAP-05 | Embedded reference | Full parameter tables inline | Minor |

### Reference Anti-Patterns

| ID | Anti-Pattern | Detection Signal | Severity |
|----|-------------|-----------------|----------|
| RAP-01 | Marketing claims | Superlatives ("best", "fastest", "powerful") | Major |
| RAP-02 | Instructions/recipes | Numbered step lists within reference entries | Major |
| RAP-03 | Narrative explanation | Multi-paragraph "why" blocks in reference | Minor |
| RAP-04 | Stylistic flourishes | Metaphors, humor, or personality in reference | Minor |
| RAP-05 | Auto-gen only | Machine-generated docs with no human curation | Major |

### Explanation Anti-Patterns

| ID | Anti-Pattern | Detection Signal | Severity |
|----|-------------|-----------------|----------|
| EAP-01 | Instructional creep | Imperative verbs ("Run this", "Configure that"). Severity: Minor for 1-2 isolated instances; Major for 3+ instances or when imperative verbs form a procedural sequence. This aligns with the Section 3 heuristic threshold (3+ imperative sentences per paragraph = Major). | Minor (1-2) / Major (3+) |
| EAP-02 | Scattered across sections | Explanation fragments buried in other doc types | Major |
| EAP-03 | Treated as less important | Explanation section is thin or absent | Minor |
| EAP-04 | No perspective | Reads like reference -- flat, neutral, no voice | Minor |
| EAP-05 | Unbounded scope | Tries to cover everything about a topic | Major |

---

## Section 3: Detection Heuristics for Quadrant Mixing

### Automated Detection Signals

| Signal | Detection Method | Agent Action | Severity |
|--------|-----------------|--------------|----------|
| Imperative verbs in explanation | 2+ imperative sentences (sentences beginning with an imperative verb form: "Run", "Configure", "Set", "Add", "Create", "Delete") within a single paragraph of explanation output. Imperative verbs in quoted commands, code blocks, or examples are exempt. | Flag with `[QUADRANT-MIX: procedural content in explanation]` | Minor (1-2), Major (3+) |
| "Why" digressions in tutorial steps | Paragraph between numbered steps that contains no imperative verbs and explains rationale rather than directing action (e.g., "This works because..." or "The reason for this is...") | Flag with `[QUADRANT-MIX: explanation in tutorial]` | Minor (1), Major (2+) |
| Choice/alternative offerings in tutorials | "Alternatively", "you could also", "Option A/B" in tutorial | Flag with `[QUADRANT-MIX: how-to content in tutorial]` | Major (any instance) |
| Procedural sequences in reference | Numbered step lists (3+ steps) within reference entries | Flag with `[QUADRANT-MIX: procedural content in reference]` | Minor (1), Major (2+) |
| Marketing language in reference | Superlatives, comparative claims, promotional tone | Flag with `[ANTI-PATTERN: marketing in reference]` | Major (any instance) |
| Explanation blocks in how-to | 3+ consecutive sentences with no action verb in how-to guide. Exception: first-paragraph context-setting sentences ("This guide assumes your service is running.") are exempt. Apply this heuristic starting from the second paragraph. | Flag with `[QUADRANT-MIX: explanation in how-to]` | Minor (1), Major (2+) |
| Reference tables in tutorial | Definition lists or parameter tables within tutorial steps | Flag with `[QUADRANT-MIX: reference in tutorial]` | Minor (1), Major (2+) |

### False-Positive Handling Protocol

A detected heuristic signal is a false positive when the flagged construct is contextually required by the primary quadrant. Override conditions:
- "Alternatively" in a tutorial step introducing a platform-specific path (macOS/Windows/Linux) is a legitimate OS conditional, NOT how-to contamination. Suppress flag.
- An imperative verb in explanation is a false positive if it appears in a quoted command, code block, or example (not running prose). Suppress flag.
- "3+ consecutive sentences without action verb" in how-to is a false positive if the sentences appear as the guide's opening context (first paragraph only). Apply the heuristic starting from the second paragraph.

When a signal fires and context clearly belongs to the primary quadrant: suppress the flag, do not ask user. When signal context is ambiguous: flag with `[QUADRANT-MIX: ...]` per the existing protocol.

### Writer Agent Self-Review Behavior

All writer agents applying these heuristics MUST:
1. Apply them to their own output as part of H-15 self-review
2. Apply the False-Positive Handling Protocol above before flagging -- suppress signals that match an override condition
3. When a mixing signal is detected (and not suppressed by step 2): (a) flag with appropriate `[QUADRANT-MIX: ...]` tag, (b) describe the flagged content to the user, (c) ask whether to remove/revise or keep with `[ACKNOWLEDGED]` marker
4. If the document accumulates 3 or more `[ACKNOWLEDGED]` markers, halt and re-run the two-axis test with the full document content. If the new classification differs from the original, report the reclassification to the user before continuing

---

## Section 4: Classification Decision Guide

### The Two-Axis Test

| | Acquisition (Study) | Application (Work) |
|---|---|---|
| **Action** (Practical) | **Tutorial** | **How-To Guide** |
| **Cognition** (Theoretical) | **Explanation** | **Reference** |

### Confidence Derivation (Deterministic)

| Axis Placement | Confidence | Rationale |
|----------------|------------|-----------|
| Both axes unambiguous | 1.00 | Clear quadrant assignment -- no secondary quadrant content detected |
| One axis clear, one mixed | 0.85 | Primary quadrant identified with secondary content from an adjacent quadrant. 0.85 chosen as above the escalation threshold (0.70) but below certainty, signaling "proceed with primary but note secondary." |
| Both axes mixed | 0.70 | Borderline multi-quadrant. 0.70 is the minimum non-escalation threshold -- content legitimately spans quadrants and decomposition should be recommended. |
| Cannot resolve | < 0.70 | `escalate_to_user` fires. Below 0.70, the classifier cannot reliably assign a quadrant and human judgment is needed. |

### Borderline Case Examples

**Case 1: Detailed how-to guide that explains rationale for each step**
- Primary signal: Steps with goals (action + application) -> How-To Guide
- Secondary signal: "because" reasoning after steps -> Explanation content
- Resolution: Classify as **How-To Guide**. Flag explanation content for extraction. Recommend companion explanation document.

**Case 2: Tutorial that covers conceptual background before first step**
- Primary signal: Learning-oriented with hands-on steps -> Tutorial
- Secondary signal: Opening theory section -> Explanation content
- Resolution: Classify as **Tutorial**. Recommend moving conceptual background to a separate explanation document, replacing with a brief "What you will learn" intro.

**Case 3: Reference entry that includes a brief usage example**
- Primary signal: Structured parameter descriptions -> Reference
- Secondary signal: Code example showing usage -> Not a violation
- Resolution: Classify as **Reference**. Brief usage examples are *expected* in reference (R-06). This is NOT quadrant mixing -- reference examples illustrate, they do not instruct.

**Case 4: "Explain how X works" request**
- "Explain" suggests understanding -> Cognition axis
- "How X works" suggests mechanism -> Could be practical (how-to) or theoretical (explanation)
- Test: Does the reader want to *do* something with X (application) or *understand* X (acquisition)?
- Resolution: If the reader wants to configure/use X -> **How-To Guide** ("How to configure X"). If the reader wants to understand X's design -> **Explanation** ("About how X works").

**Case 5: SKILL.md-style document combining reference and explanation**
- Contains: agent table (reference), purpose section (explanation), invocation examples (how-to)
- Resolution: Classify as **multi-quadrant**. Recommend decomposition (canonical order):
  1. How-To Guide: Step-by-step invocation instructions
  2. Reference: Agent registry table, parameter specifications
  3. Explanation: Purpose, design rationale, architectural context

### Multi-Quadrant Decomposition

When `quadrant == "multi"`:
1. Return `decomposition` array listing each quadrant with `content_scope` and `sequence`
2. Recommended document sequence: Tutorial first (if present), then How-To Guide, then Reference, then Explanation. (Sequence follows Diataxis learning progression: hands-on experience first, task application second, lookup reference third, conceptual deepening last.) All decomposition enumerations in this document follow this canonical order.
3. Content spanning 3+ quadrants strongly recommends decomposition

---

## Section 5: Jerry Voice Guidelines

**Scope:** These guidelines govern Diataxis documentation output (tutorials, how-to guides, reference documents, explanation documents). For Jerry internal documents (rule files, ADRs, SKILL.md, CLAUDE.md), the existing Jerry rule file prose style takes precedence. Apply Section 5 guidelines only when the deliverable's quadrant classification has been confirmed.

### Universal Jerry Voice Markers

These apply across ALL quadrants:
- Active voice preferred ("Run the command", not "The command should be run")
- Direct address ("you", "your") preferred
- Concrete over abstract ("in `config.yaml`", not "in the configuration file")
- No passive constructions ("Configure X", not "X can be configured by...")
- No "it is possible to" or "one can" -- use direct imperative or declarative
- Short sentences preferred; break long compound sentences

### Per-Quadrant Voice Guidelines

#### Tutorial Voice
**Tone:** Encouraging, concrete, collaborative
**Register:** Supportive instructor guiding a hands-on exercise

| Before (Non-Jerry) | After (Jerry Voice) |
|---------------------|---------------------|
| "The user should navigate to the settings page." | "Navigate to the settings page." |
| "It is recommended that one creates a new project first." | "Create a new project first." |
| "You might want to consider checking the output." | "Check the output. You should see:" |

**Anti-example:** "It is possible that the installation process may require administrative privileges, which can be obtained by running the terminal as an administrator." -- Passive, hedging, verbose.

#### How-To Guide Voice
**Tone:** Direct, action-oriented, efficient
**Register:** Experienced colleague giving clear directions

| Before (Non-Jerry) | After (Jerry Voice) |
|---------------------|---------------------|
| "It is possible to configure X by modifying Y." | "Configure X by modifying Y." |
| "One should ensure that the service has been restarted." | "Restart the service." |
| "The deployment can be triggered by executing the following command." | "Deploy by running:" |

**Anti-example:** "In order to accomplish the task of deploying your application to the production environment, it will be necessary for you to first ensure that all of the prerequisite steps have been completed." -- Verbose, indirect, bureaucratic.

#### Reference Voice
**Tone:** Neutral, precise, austere
**Register:** Technical specification -- accurate, uniform, no personality

| Before (Non-Jerry) | After (Jerry Voice) |
|---------------------|---------------------|
| "This command can be used to list items." | "Lists items. Syntax: `command [options]`" |
| "The powerful `deploy` command helps you easily push your code." | "`deploy` -- Pushes code to the target environment." |
| "You'll love the flexibility of the configuration options." | "Configuration accepts the following parameters:" |

**Anti-example:** "The amazing `config` command is one of the most powerful tools in your arsenal, giving you incredible flexibility to customize every aspect of your setup!" -- Marketing language, superlatives, subjective claims.

#### Explanation Voice
**Tone:** Thoughtful, discursive, contextual
**Register:** Knowledgeable colleague sharing understanding over coffee

| Before (Non-Jerry) | After (Jerry Voice) |
|---------------------|---------------------|
| "The system was designed in this manner for various reasons." | "The system uses event sourcing because the audit trail requirements demanded complete state history." |
| "One must consider the trade-offs involved." | "The trade-off here is latency versus consistency." |
| "It should be noted that there exist alternative approaches." | "An alternative approach is X. This works well when Y, but breaks down when Z." |

**Anti-example:** "You must configure the logging level to DEBUG by running `export LOG_LEVEL=DEBUG`." -- Imperative instruction in what should be discursive explanation.

### Voice Quality Gate

Writer agents apply Jerry voice guidelines during H-15 self-review. This gate is a MEDIUM-tier standard (override with documented justification):
1. Check output against universal voice markers
2. Check output against quadrant-specific voice guidelines
3. Flag violations with `[VOICE: {description}]` tags
4. Rewrite flagged passages to conform before presenting output

### Severity Derivation for Anti-Pattern Tables

Anti-pattern severity in Section 2 is derived from impact on the quadrant's primary function:
- **Critical:** Renders the document unusable for its quadrant purpose (none currently in catalog)
- **Major:** Introduces content from a foreign quadrant that misleads the reader about the document type
- **Minor:** Style or structural issue that does not change the document's effective quadrant classification

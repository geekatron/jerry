# Diataxis Documentation Framework

> Knowledge document for the Diataxis documentation methodology. Reference for `/diataxis` skill agents.

> **Scope:** This document explains the Diataxis framework's four-quadrant model, per-quadrant characteristics, and classification methodology. It does not cover Jerry-specific quality criteria IDs (T-01 through E-07), detection heuristics, or anti-pattern severity levels -- those are specified in `skills/diataxis/rules/diataxis-standards.md`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Framework Overview](#framework-overview) | Two-axis grid and four quadrants |
| [Tutorials](#tutorials) | Learning-oriented, practical acquisition |
| [How-To Guides](#how-to-guides) | Goal-oriented, practical application |
| [Reference](#reference) | Information-oriented, theoretical application |
| [Explanation](#explanation) | Understanding-oriented, theoretical acquisition |
| [Common Anti-Patterns](#common-anti-patterns) | Quadrant mixing and per-quadrant failures |
| [Classification Decision Guide](#classification-decision-guide) | Two-axis test and borderline cases |
| [Sources](#sources) | Authoritative references |

---

## Framework Overview

Diataxis (Greek: *dia* "across" + *taxis* "arrangement") organizes all technical documentation into exactly four types along two orthogonal axes.

**Axis 1 -- Action vs. Cognition:**
- **Action** = practical knowledge, knowing *how* to do something
- **Cognition** = theoretical knowledge, knowing *that* something is the case

**Axis 2 -- Acquisition vs. Application:**
- **Acquisition** = the reader is *at study*, learning new skills
- **Application** = the reader is *at work*, applying existing skills

```
                    ACQUISITION                APPLICATION
                   (study/learning)           (work/applying)

 ACTION        ┌──────────────────┬──────────────────────┐
 (practical    │   TUTORIALS      │   HOW-TO GUIDES      │
  doing)       │   Learning by    │   Goal-oriented      │
               │   doing          │   task completion     │
               ├──────────────────┼──────────────────────┤
 COGNITION     │   EXPLANATION    │   REFERENCE          │
 (theoretical  │   Understanding  │   Information         │
  knowing)     │   context, why   │   lookup, what        │
               └──────────────────┴──────────────────────┘
```

The two axes are binary and exhaustive. Their intersection produces exactly four documentation needs -- no more, no fewer. Created by Daniele Procida (2014-2021, originated from Django documentation). Adopted by Django, Cloudflare, Python, NumPy, Gatsby, Canonical, and several hundred other projects.

---

## Tutorials

**Quadrant:** Action + Acquisition
**User question:** "Can you teach me to...?"
**Reader:** A beginner at study. Nearly all responsibility falls on the instructor.

### Quality Criteria

| Criterion | Description |
|-----------|-------------|
| Meaningful | Exercises provide a sense of achievement |
| Successful | Completable by the learner without failure |
| Logical | Follows a coherent, comprehensible path |
| Usefully complete | Exposes learners to necessary actions, concepts, and tools |
| Repeatable | Allows learners to repeat the experience |
| Reliable | Must produce the exact promised results every time |

### Writing Principles

1. "The first rule of teaching is: don't try to teach." Create experiences, not lectures.
2. Show the endpoint upfront so learners see progress toward a visible goal.
3. Deliver visible results at every step.
4. Use narrative commentary: "You will notice that...", "Remember that..."
5. Ruthlessly minimize explanation. Link to deeper resources instead.
6. Focus on concrete actions rather than abstractions.
7. Ignore alternative approaches. One path only.
8. Aspire to perfect reliability.

### Language Conventions
- Use "We..." to establish shared purpose
- Clear directional: "First do x. Now, do y."
- Expectation-setting: "The output should look something like..."
- Confirmation cues: "Notice that... Remember that..."

---

## How-To Guides

**Quadrant:** Action + Application
**User question:** "How do I...?"
**Reader:** Already competent, knows what they want to achieve.

### Quality Criteria

| Criterion | Description |
|-----------|-------------|
| Meaningful purpose | Grounded in actual user needs |
| Logical sequencing | Steps ordered respecting dependencies |
| Flow | Anticipates user needs, progresses smoothly |
| Adaptability | Flexible for varying real-world situations |
| Clear naming | Titles state exactly what the guide addresses |
| Action-only | Contains "action and only action" -- no digressions |

### Writing Principles

1. Write around human needs, not tool mechanics.
2. Provide a sequence of actions. Steps, not explanations.
3. Allow for branching and alternatives. Real-world conditions vary.
4. Use conditional imperatives: "If you want x, do y."
5. Reference additional resources externally rather than embedding.
6. Prioritize usability over exhaustive coverage.

### Language Conventions
- Imperative voice: "Run the command", "Configure the setting"
- Conditional branches: "If you need X, do Y"
- Goal-framed titles: "How to deploy to production"

---

## Reference

**Quadrant:** Cognition + Application
**User question:** "What is...?" or "What are the parameters for...?"
**Reader:** Seeking truth and certainty -- firm platforms to stand on while working.

### Quality Criteria

| Criterion | Description |
|-----------|-------------|
| Austere | No ambiguity, no doubt, no embellishment |
| Authoritative | Comparable to a map -- eliminates need to verify |
| Accurate | Wholly faithful to the product described |
| Consistent | Structure and format are uniform and predictable |
| Complete | All elements of the system are documented |

### Writing Principles

1. Describe neutrally. Avoid instruction, explanation, opinion.
2. Use standard patterns. Readers expect familiar formats.
3. Mirror product structure in documentation organization.
4. Include concise usage examples that illustrate without instructing.
5. Be boring on purpose. Unmemorable prose, unfailing accuracy.

### Language Conventions
- Neutral, declarative: "The `config` object accepts..."
- No imperative voice, no persuasion, no opinion
- Tables, definition lists, standard entry formats

---

## Explanation

**Quadrant:** Cognition + Acquisition
**User question:** "Can you tell me about...?" or "Why does...?"
**Reader:** At study, stepping back to reflect.

### Quality Criteria

| Criterion | Description |
|-----------|-------------|
| Makes connections | Illuminates relationships across topics |
| Provides context | Includes design decisions, history, constraints |
| Admits perspective | Acknowledges opinions, alternatives, multiple approaches |
| Stays bounded | Prevents absorbing content from other quadrants |
| Deepens understanding | Reveals "why something does what it does" |

### Writing Principles

1. Frame titles with implicit "About." E.g., "About user authentication."
2. Use language that unfolds reasoning: "The reason for x is because historically, y..."
3. Weigh alternatives: "Some prefer w because z. This can work, but..."
4. Explain interactions and mechanisms to reveal underlying causation.
5. Discuss the bigger picture: history, choices, alternatives, design rationale.
6. Admit opinion. Unlike reference, explanation may take positions.

### Language Conventions
- Discursive, flowing prose
- "The reason..." "This is because..." "Historically..."
- Richer vocabulary; may use first person

---

## Common Anti-Patterns

### The #1 Anti-Pattern: Quadrant Mixing

When content types bleed together, no single reader's need is served well. A tutorial with reference tables overwhelms the beginner. A reference page with explanatory paragraphs frustrates the practitioner looking up a parameter.

### Per-Quadrant Anti-Patterns

| Quadrant | Anti-Pattern | Fix |
|----------|-------------|-----|
| **Tutorial** | Teaching through explanation (wall of theory before hands-on) | Remove explanation; replace with concrete step that *shows* |
| **Tutorial** | Offering choices ("You can use either X or Y") | Pick one. Tutorials have exactly one path. |
| **Tutorial** | Assuming competence ("Configure your dev environment, then...") | Spell out every step. Assume nothing. |
| **How-To** | Explaining the obvious ("Click Save to save") | Only document non-obvious steps |
| **How-To** | Embedding reference (complete parameter table mid-flow) | Move table to reference; link to it |
| **How-To** | Teaching basics ("Before we begin, let's learn about REST...") | How-to assumes competence. Link to tutorial. |
| **Reference** | Editorializing ("This is the best approach...") | Reference is neutral. Move opinions to explanation. |
| **Reference** | Inconsistent format (one class as table, another as prose) | Standardize all entries to same format |
| **Reference** | Auto-gen-only (no human curation, no examples) | Supplement with usage examples and context links |
| **Explanation** | Unbounded scope (tries to cover everything) | Set explicit boundaries. One explanation = one topic. |
| **Explanation** | Prescribing actions ("You should configure logging as follows...") | That is a how-to in disguise. Move it. |
| **Explanation** | No perspective (reads like reference -- flat, neutral) | Explanation should have voice, opinion, and narrative arc. |

### Content Drift

Even well-structured documentation degrades over time as contributors add content that violates quadrant boundaries. Prevention: clear quadrant labels, contribution guidelines, periodic audits, CI integration.

---

## Classification Decision Guide

### The Two-Axis Test

Apply two questions to any documentation:

**Question 1:** Does this help the reader *do* something (action) or *understand* something (cognition)?
**Question 2:** Is the reader *learning/studying* (acquisition) or *working/applying* (application)?

| | Acquisition (Study) | Application (Work) |
|---|---|---|
| **Action** (Practical) | **Tutorial** | **How-To Guide** |
| **Cognition** (Theoretical) | **Explanation** | **Reference** |

### Quick Heuristics

| Signal | Likely Quadrant |
|--------|-----------------|
| "Let me show you how to get started..." | Tutorial |
| "If you want to do X, follow these steps..." | How-To Guide |
| "The `config` object accepts these parameters..." | Reference |
| "The reason we designed it this way is..." | Explanation |
| Boring, structured in tables/definition lists | Reference |
| Engaging, readable casually away from work | Explanation |
| Guarantees a safe, controlled outcome | Tutorial |
| Assumes competence, handles real-world variation | How-To Guide |

### Borderline Case Examples

**Case 1: "Getting Started with Our API"**
- If it walks a complete beginner through concepts with a sandbox -> **Tutorial**
- If it assumes API knowledge and provides connection steps -> **How-To Guide**
- Most "Getting Started" pages are actually how-to guides mislabeled as tutorials.

**Case 2: "Authentication Architecture"**
- If it describes endpoints, token formats, parameters -> **Reference**
- If it discusses why OAuth2 was chosen over SAML -> **Explanation**
- Often needs decomposition into two documents.

**Case 3: "How to Configure Logging" with theory section**
- The "how to configure" section -> **How-To Guide**
- The "understanding log levels" section -> **Explanation**
- The parameter table -> **Reference**
- Decompose into three documents with cross-links.

**Case 4: "Database Migration Guide" for a new team member**
- If designed as a learning experience ("Let's create your first migration") -> **Tutorial**
- If it is a checklist for running migrations in production -> **How-To Guide**

**Case 5: "Error Codes" page with troubleshooting steps**
- Error code table -> **Reference** (structured lookup)
- Troubleshooting steps per error -> **How-To Guides** ("If you see error 403, do X")
- Separate them: reference page links to per-error how-to guides.

### Multi-Quadrant Decomposition

When a document spans multiple quadrants:
1. Identify the primary quadrant (document's main purpose)
2. Extract secondary content into separate documents
3. Cross-link between the resulting single-quadrant documents

---

## Alternative Perspectives

Not every documentation team finds Diataxis suitable. Topic-based authoring (DITA/Darwin Information Typing Architecture) uses a similar categorization (concept, task, reference) but adds a formal XML schema and reuse model that Diataxis deliberately avoids. Teams with existing DITA toolchains may find the migration cost exceeds the benefit of Diataxis's simpler four-quadrant model.

Some practitioners argue that the four-quadrant separation creates artificial boundaries. A "Getting Started" page that combines a brief tutorial with a quick-reference table may serve readers better than forcing them to navigate between two separate documents. The Diataxis response is that such hybrid documents inevitably serve neither audience well -- but this remains a genuine design tension rather than a settled question.

Others note that Diataxis was developed in the context of open-source software documentation and may not transfer directly to enterprise documentation, API-first products, or documentation-as-code workflows where generated reference is the dominant content type. The framework's emphasis on hand-authored explanation and tutorial content assumes a documentation team with capacity for sustained writing effort.

---

## Related

- **Reference:** [Diataxis Quality Criteria](../../skills/diataxis/rules/diataxis-standards.md) -- Jerry-specific criteria IDs, anti-patterns, detection heuristics
- **Templates:** [Tutorial](../../skills/diataxis/templates/tutorial-template.md), [How-To](../../skills/diataxis/templates/howto-template.md), [Reference](../../skills/diataxis/templates/reference-template.md), [Explanation](../../skills/diataxis/templates/explanation-template.md) -- Per-quadrant structural templates
- **Skill:** [Diataxis SKILL.md](../../skills/diataxis/SKILL.md) -- Skill definition and agent roster

---

## Sources

- [Diataxis Framework](https://diataxis.fr/) -- Primary source, maintained by creator Daniele Procida
- [Diataxis Tutorials](https://diataxis.fr/tutorials/)
- [Diataxis How-To Guides](https://diataxis.fr/how-to-guides/)
- [Diataxis Reference](https://diataxis.fr/reference/)
- [Diataxis Explanation](https://diataxis.fr/explanation/)
- [Diataxis Compass](https://diataxis.fr/compass/)
- [Diataxis Map](https://diataxis.fr/map/)
- [Diataxis Quality](https://diataxis.fr/quality/)
- [Python Diataxis Adoption Discussion](https://discuss.python.org/t/adopting-the-diataxis-framework-for-python-documentation/15072)

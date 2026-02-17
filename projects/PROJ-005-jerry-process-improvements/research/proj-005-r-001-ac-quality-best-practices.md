# PROJ-005-R-001: Work Item Content Quality Best Practices

> **PS ID:** proj-005
> **Entry ID:** r-001
> **Type:** Research
> **Status:** Complete
> **Researcher:** ps-researcher (v2.0.0)
> **Date:** 2026-02-16
> **Topic:** Work Item Content Quality Best Practices

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary (L0)](#executive-summary-l0) | Key findings in 5 bullet points for stakeholders |
| [Detailed Findings (L1)](#detailed-findings-l1) | Engineer-level findings per research question with citations |
| [Strategic Implications (L2)](#strategic-implications-l2) | Architect-level implications for Jerry's worktracker design |
| [Sources](#sources) | All referenced URLs and publications |

---

## Executive Summary (L0)

1. **AC quality has a proven, measurable framework.** The Quality User Story (QUS) framework defines 13 criteria across syntax, semantics, and pragmatics. Industry consensus is 3-5 AC bullets per work item; 6+ signals the item should be split. The #1 rule -- "if engineers need to ask questions, AC failed" -- aligns with industry best practice that AC must be testable, specific, and outcome-focused, never containing implementation details.

2. **LLMs can both generate and assess content quality, but systematically fail at "rationale clarity."** Research shows GPT-4o and Claude achieve near-human inter-rater reliability (Cohen's kappa 0.84-0.87) when assessing user story quality against explicit criteria. However, LLM-generated stories consistently underperform on explaining the "why" behind requirements, and produce higher rejection rates than human-written stories. This means quality gates are essential, not optional.

3. **Approval fatigue is the #1 threat to human-in-the-loop quality.** The "rubber-stamp risk" phenomenon means that when reviewers see too many items or too much text, they default to automatic approval. Research shows a zero-override rate signals blind trust, not perfection. Smart escalation -- where less than 10% of decisions require human intervention -- prevents fatigue while maintaining quality.

4. **The Diataxis framework solves the "wall of text" template problem.** Documentation should be split into four types: tutorials (learning), how-to guides (doing), reference (looking up), and explanation (understanding). Jerry's 400+ line templates are reference documents masquerading as creation guides. The fix is to create separate "how-to" creation guides (1 page, action-oriented) alongside the existing reference templates.

5. **AC must be strictly separated from Definition of Done (DoD).** A critical anti-pattern is mixing process/technical requirements (code review, tests passing, documentation updated) into AC. AC defines *what* the feature does for the user; DoD defines the *process quality standard* applied to all items. Jerry's current templates include "Documentation updated" and "Monitoring/alerting in place" as AC placeholders -- these belong in DoD, not AC.

---

## Detailed Findings (L1)

### Q1: AC Quality Best Practices in Agile

#### Frameworks for Writing Acceptance Criteria

Two primary formats dominate industry practice:

**1. Scenario-Oriented (Given/When/Then -- GWT)**

Invented in the early 2000s and codified by the Agile Alliance, this Behavior-Driven Development (BDD) template structures AC as testable scenarios:

```
Given [precondition/context]
When [action/trigger]
Then [expected outcome]
```

GWT removes ambiguity from requirements, helps teams align before coding begins, and directly supports automated testing tools like Cucumber and SpecFlow ([Parallel HQ, 2025](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria)). Non-functional requirements can also use GWT, e.g., "Given a mobile device with a slow network, when the user submits the form, then the loading spinner persists until the data is saved and the user receives a confirmation within 2 seconds."

**2. Rule-Oriented (Checklist)**

A simple checklist of pass/fail conditions:

```
- [ ] User can search by category name
- [ ] Search results display within 200ms
- [ ] Empty search returns "No results" message
```

This format is preferred when GWT feels overly ceremonial for simple conditions ([AltexSoft](https://www.altexsoft.com/blog/acceptance-criteria-purposes-formats-and-best-practices/)).

#### What Makes AC "Good" vs "Bad"

**Good AC characteristics:**
- **Testable**: Clear pass/fail. "Have each of the acceptance criteria been met?" must have a Yes or No answer ([Agile Alliance](https://agilealliance.org/glossary/invest/))
- **Outcome-focused**: Describes *what* the system does, not *how* it's built
- **Specific and measurable**: "Results load in under 200ms" not "make it fast"
- **Written in active voice, plain language**: Avoid technical jargon
- **Independent of implementation**: Leave architectural decisions to engineers
- **Defined before development starts**: During backlog grooming or sprint planning

**Bad AC characteristics (anti-patterns):**
- **Vague**: "Nice UX" or "works well" -- unmeasurable ([AltexSoft](https://www.altexsoft.com/blog/acceptance-criteria-purposes-formats-and-best-practices/))
- **Implementation-prescriptive**: "Use Redis for caching" or "Implement with a singleton pattern"
- **Process items disguised as AC**: "Code reviewed," "Tests written," "Documentation updated" -- these are DoD, not AC
- **Too narrow**: Over-specifying UI details (button colors) removes developer flexibility
- **Too broad**: "System handles all error cases" -- untestable
- **Negative phrasing**: Using "not" unless describing unique system constraints

#### The AC / DoD Separation Rule

This is a critical distinction that Jerry's templates currently violate:

| Aspect | Acceptance Criteria | Definition of Done |
|--------|--------------------|--------------------|
| **Scope** | Per work item, unique to each | Global standard, same for all items |
| **Focus** | *What* the feature does | *How* work is completed |
| **Owner** | Product Owner defines | Team defines |
| **Examples** | "User can filter by date range" | "Code reviewed," "Tests passing," "Docs updated" |
| **When written** | Before development, during grooming | Once, applied to all work |

> "Acceptance criteria go with work items, and the definition of done goes with the system." -- [Agile Sherpas](https://www.agilesherpas.com/blog/definition-of-done-acceptance-criteria)

> "A common pitfall in Agile teams is mixing technical or process-oriented requirements into acceptance criteria." -- [AltexSoft](https://www.altexsoft.com/blog/acceptance-criteria-definition-of-done/)

**Direct implication for Jerry:** The current ENABLER template includes "Documentation updated" and "Monitoring/alerting in place (if applicable)" as AC placeholders. These are DoD items. They should be removed from AC and placed in a shared DoD definition.

#### The Quality User Story (QUS) Framework

The QUS framework, developed by Lucassen et al. (2016), provides the most rigorous academic foundation for user story quality assessment. It defines 13 criteria across three dimensions:

**Syntactic (form):**
- Well-formed: Follows standard template
- Atomic: Single feature per story
- Minimal: No unnecessary information

**Pragmatic (usage):**
- Full sentence, estimatable, unique, uniform, independent, complete

**Semantic (meaning):**
- Conceptually sound, problem-oriented, unambiguous, conflict-free

The AQUSA tool automates QUS evaluation using NLP techniques and was validated against 1,023 user stories from 18 software companies ([Springer](https://link.springer.com/article/10.1007/s00766-016-0250-x)).

---

### Q2: LLM Content Quality Gates

#### Current State of LLM Quality Assessment

A 2025 study published in the Journal of Intelligent Information Systems evaluated LLM performance at assessing user story quality against the QUS framework ([Springer JIIS, 2025](https://link.springer.com/article/10.1007/s10844-025-00939-3)):

**Key findings:**
- **Claude 3 Opus** achieved Cohen's kappa of **0.87** (near-perfect agreement with human raters)
- **Claude 3.5 Sonnet** achieved kappa of **0.84**
- **GPT-4o** and **GPT-4-Turbo** also showed "superior performance"
- Performance was strongest on syntactic criteria (Language Clarity, Internal Consistency)
- Performance was weakest on semantically complex criteria (Rationale Clarity, Problem Orientation)
- **Structured evaluation criteria significantly enhanced assessment accuracy** -- providing explicit rubrics improved LLM assessment quality

#### LLM-Generated User Story Quality

A related study on LLM-generated user stories ([arXiv:2507.15157](https://arxiv.org/abs/2507.15157)) found:

- LLM-generated stories showed **high structural clarity and consistency** comparable to human-written stories
- **Critical weakness**: Models systematically lag behind humans in articulating rationale (RC scores); GPT-3.5 scored only 1.25/3.0
- **Most frequent defect**: Excessive conjunctions (57%+ of stories in some models violated the atomicity criterion)
- **Higher rejection rates**: LLM-generated stories consistently produced higher rejection rates than human-authored stories regardless of model scale
- **Human oversight remains essential** for deployment

#### Programmatic Quality Enforcement Approaches

Several patterns exist for enforcing content quality:

1. **Rule-based validation**: Format/structure checks (is it valid JSON? does it match required patterns?)
2. **LLM-as-judge**: Using one LLM to evaluate another's output against explicit criteria
3. **Deterministic evaluation**: Strict adherence to predefined formats and rules
4. **Quality metrics**: Faithfulness, factual consistency, hallucination detection
5. **Human-in-the-loop**: Expert validation at critical decision points

**Implication for Jerry:** Quality gates should be layered: structural rules (WTI-style) catch form issues, while LLM-based assessment with explicit criteria catches semantic issues. The key insight is that **providing clear evaluation criteria to the LLM dramatically improves assessment accuracy** -- which means Jerry's quality rules must be explicit and measurable, not vague.

---

### Q3: Optimal AC Bullet Count

#### Industry Consensus

The industry consensus, while not based on rigorous scientific studies, is remarkably consistent:

- **Scrum.org community**: "Typically, coaches recommend teams have **3 to 5** acceptance criteria for a user story" ([Scrum.org Forum](https://www.scrum.org/forum/scrum-forum/94804/what-best-practices-writing-user-stories-how-many-acceptance-criteria-should-normally-maximal-user-story-have))
- **AltexSoft**: "The optimal number of criteria for one uncompleted task is **no more than three**, and if there are significantly more (from six), it makes sense to divide the user story into several" ([AltexSoft](https://www.altexsoft.com/blog/acceptance-criteria-purposes-formats-and-best-practices/))
- **INVEST principle**: The "S" (Small) criterion reinforces that if AC grows beyond manageable size, the item should be split

#### The Splitting Signal

A high AC count is a **scope signal**, not just a documentation issue:

| AC Count | Signal | Action |
|----------|--------|--------|
| 1-2 | May be under-specified | Verify completeness |
| 3-5 | Sweet spot | Proceed |
| 6-8 | Scope concern | Consider splitting via SPIDR |
| 9+ | Almost certainly too large | Must split |

**SPIDR splitting framework** (Spike, Paths, Interfaces, Data, Rules):
- **Spike**: If unknown, split into a research spike + implementation
- **Paths**: Split by user workflow paths (happy path vs error path)
- **Interfaces**: Split by interface boundary (API, UI, integration)
- **Data**: Split by data variations handled
- **Rules**: Split by business rules applied

#### Relationship to Complexity

> "There are no best practices for complex work." -- [Scrum.org](https://www.scrum.org/forum/scrum-forum/94804/what-best-practices-writing-user-stories-how-many-acceptance-criteria-should-normally-maximal-user-story-have)

The key is vertical slicing: each story should deliver end-to-end business value. If AC count grows because the item spans multiple user interactions or system behaviors, split the item rather than adding more criteria.

**Implication for Jerry:** Implement a soft warning at 6 AC bullets and a hard warning at 9+. Frame the warning as a scope issue ("Consider splitting this item") rather than a documentation issue ("Too many criteria").

---

### Q4: Collaboration Checkpoints in AI-Assisted Workflows

#### The Rubber-Stamp Risk

The most critical finding in this area is the phenomenon of **"rubber-stamp risk"** -- when human oversight becomes performative rather than substantive:

> "When the human role becomes mere checkbox review or rapid approval, you've entered rubber-stamp risk: the system gives the appearance of safety while critical decisions are still unchallenged." -- [CyberManiacs](https://cybermaniacs.com/cm-blog/rubber-stamp-risk-why-human-oversight-can-become-false-confidence)

**Warning signs of disengagement:**
- Always approve, never challenge
- Zero-override rate (signals blind trust, not perfection)
- Rapid approval without reading content
- Reviewer never requests changes

#### Oversight Fatigue

> "The speed and scale at which AI systems operate can far surpass human cognitive capabilities, making continuous, real-time monitoring infeasible." -- [Mediate.com](https://mediate.com/the-meaning-and-illusion-of-human-oversight-of-ai/)

**Fatigue mitigation strategies:**
- **Smart escalation**: Only route ambiguous/high-risk items for human review. Organizations using this report less than 10% of decisions require human intervention ([All Days Tech](https://alldaystech.com/guides/artificial-intelligence/human-in-the-loop-ai-review-queue-workflows))
- **Reviewer rotation**: Prevent burnout by rotating reviewers
- **Workload caps**: Monitor and cap items per reviewer per session (e.g., max 150 items/shift)
- **Summarized context**: Don't show reviewers raw JSON; provide structured summaries with specific review questions
- **Confidence-based routing**: Only escalate when the AI's confidence is low

#### Trust Calibration (GitLab Research)

GitLab's research on agentic tool trust found that trust builds through **"micro-inflection points"** -- small consistent positive interactions, not breakthrough moments ([GitLab Blog](https://about.gitlab.com/blog/building-trust-in-agentic-tools-what-we-learned-from-our-users/)).

**Four pillars for managing AI oversight:**
1. **Safeguarding actions**: Confirmation dialogs for critical changes, rollback capabilities
2. **Transparency**: Agent communicates reasoning before executing significant tasks
3. **Context retention**: Agent remembers preferences, reducing repeated instruction
4. **Anticipatory support**: Proactive pattern recognition that demonstrates reliability

> "AI agents should know when to pause and seek human input." -- [GitLab Blog](https://about.gitlab.com/blog/building-trust-in-agentic-tools-what-we-learned-from-our-users/)

#### Autonomy Levels Framework

A model emerging from AI agent design uses five autonomy levels, analogous to self-driving car levels ([Tessl.io](https://tessl.io/blog/the-5-levels-of-ai-agent-autonomy-learning-from-self-driving-cars/)):

| Level | User Role | Description | Jerry Analogy |
|-------|-----------|-------------|---------------|
| L0 | Operator | User does everything, AI assists | Manual work item creation |
| L1 | Collaborator | AI drafts, user edits heavily | Current Jerry state |
| L2 | Consultant | AI creates, user reviews/approves | Target state for routine items |
| L3 | Approver | AI executes, user approves results | Target state for standard patterns |
| L4 | Observer | AI is fully autonomous, user monitors | Not recommended for content |

> "Autonomy is a property that can be designed independently of capability -- a capable agent can still act with low autonomy if required to consult its user before taking each action." -- [Knight Columbia](https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1)

**Spec-driven pattern**: An emerging approach is to have the AI generate requirements/specs for human review *before* creating the work items themselves. This front-loads the review to where it has the highest impact.

**Implication for Jerry:** Implement tiered checkpoints:
- **Auto-approve**: Structural/formatting corrections (agent fixes silently)
- **Summary review**: New work items get a one-line summary for quick human scan
- **Full review**: Items with 6+ AC, cross-epic dependencies, or architecture decisions require explicit approval
- **Never auto-approve**: Scope changes, item deletion, priority overrides

---

### Q5: Creation Guides vs Reference Templates

#### The Diataxis Framework

The Diataxis documentation framework, adopted by Canonical/Ubuntu, Django, and hundreds of other projects, identifies four fundamental documentation types ([Diataxis.fr](https://diataxis.fr/)):

|  | Acquisition (Learning) | Application (Doing) |
|--|------------------------|---------------------|
| **Practice** | Tutorial (learning by doing) | How-to Guide (task-oriented) |
| **Theory** | Explanation (understanding) | Reference (information) |

**Key insight**: Each type serves a different user need and must be written differently. Mixing them creates documents that serve no audience well.

> "Diataxis solves problems related to documentation content (what to write), style (how to write it) and architecture (how to organize it)." -- [Diataxis.fr](https://diataxis.fr/)

#### Mapping to Jerry's Template Problem

Jerry's current worktracker templates (e.g., ENABLER.md at 400+ lines) are **reference documents**: comprehensive, ontology-aligned, containing every possible field, validation rule, and state machine definition. They answer the question "What are all the properties of an enabler?"

What is missing is a **how-to guide**: a practical, action-oriented document that answers "How do I create a good enabler right now?" -- assuming the user already knows what an enabler is.

| Aspect | Reference Template (Current) | Creation Guide (Needed) |
|--------|------------------------------|------------------------|
| **Length** | 400+ lines | ~30-50 lines (1 page) |
| **Audience** | Architect defining the system | Engineer creating a work item |
| **Purpose** | Comprehensive field catalog | Step-by-step creation flow |
| **Tone** | Formal, exhaustive | Practical, concise |
| **AC guidance** | Template placeholder `{{CRITERION_1}}` | Examples + anti-patterns + rules |
| **When used** | System design, validation | Every time a work item is created |

#### Quick Reference Guide (QRG) Patterns

Industry best practices for QRGs:

- **Strict one-page formatting**: Forces inclusion of only essential information ([Whale](https://usewhale.io/blog/quick-reference-guide-template/))
- **Action-oriented**: QRGs are "memory joggers" not "teaching tools" -- they assume competence ([Essential Data](https://essentialdata.com/how-to-create-quick-reference-guides-quick-reference-guides/))
- **Scannable in 30 seconds**: Bullet points, bold key terms, minimal prose ([Glitter AI](https://www.glitter.io/blog/process-documentation/quick-reference-guide-template))
- **Embedded in workflow**: Can be placed inside the reference template as a collapsed section or extracted as a separate file

> "SOPs are the full instruction manual and QRGs are the cliff notes version." -- [Essential Data](https://essentialdata.com/how-to-create-quick-reference-guides-quick-reference-guides/)

#### Embedding Pattern

The most practical approach for Jerry is an **embedded creation guide** pattern:

```markdown
## Quick Creation Guide

<!-- This section is for agents/engineers creating this work item type -->

### Step 1: Write the Summary (2-3 sentences)
- What is being built/changed?
- Why is it needed?
- What is the scope boundary?

### Step 2: Define Acceptance Criteria (3-5 bullets)
RULES:
- Each criterion is testable (yes/no answer)
- Focus on OUTCOMES, not implementation
- No DoD items (no "tests written", "code reviewed")
- If > 5 criteria, consider splitting the work item

GOOD: "User can filter results by date range"
BAD:  "Implement date picker component using React DateRange library"
BAD:  "Code reviewed and approved by 2 engineers"

### Step 3: Verify Completeness
- [ ] Can an engineer start work without asking clarifying questions?
- [ ] Can QA write test cases from the AC alone?
- [ ] Are all AC independent of implementation choice?
```

**Implication for Jerry:** Create companion "creation guide" files alongside reference templates. Reference templates remain the authoritative schema; creation guides provide the practical workflow. Agents should use creation guides during work item creation and reference templates during validation.

---

## Strategic Implications (L2)

### For Jerry's Worktracker Design

#### 1. Add Content Quality Rules (WTI-007 through WTI-012)

Jerry currently has WTI-001 through WTI-006 covering structural integrity. Content quality rules are entirely absent. Recommended additions:

| Rule ID | Name | Description |
|---------|------|-------------|
| WTI-007 | AC Presence | All DeliveryItems MUST have non-empty AC before transitioning to IN_PROGRESS |
| WTI-008 | AC Testability | Each AC bullet MUST be verifiable with a yes/no answer |
| WTI-009 | AC Outcome Focus | AC MUST describe outcomes, not implementation details |
| WTI-010 | AC / DoD Separation | AC MUST NOT contain process items (code review, testing, documentation) |
| WTI-011 | AC Scope Signal | Items with 6+ AC SHOULD trigger a splitting recommendation |
| WTI-012 | AC Clarity Gate | "If an engineer needs to ask clarifying questions, the AC has failed" |

#### 2. Implement Layered Quality Gates

Based on the research findings, quality enforcement should be layered:

```
Layer 1: Structural (WTI-001 to WTI-006) -- Automated, blocking
  - File structure, state consistency, evidence links

Layer 2: Content Form (WTI-007, WTI-008, WTI-011) -- Automated, blocking
  - AC presence, testability format check, bullet count

Layer 3: Content Semantics (WTI-009, WTI-010, WTI-012) -- LLM-assessed, advisory
  - Outcome focus, DoD separation, clarity assessment
  - Uses explicit rubric (like QUS framework criteria)

Layer 4: Human Review -- Triggered by conditions
  - 6+ AC items, cross-epic items, architecture decisions
  - Summarized context, specific review questions
```

#### 3. Create Dual-Document Template Architecture

Following Diataxis principles, restructure templates into:

```
.context/templates/worktracker/
  ENABLER.md              # Reference template (existing, keep as-is)
  ENABLER_GUIDE.md        # Creation guide (NEW, ~50 lines)
  FEATURE.md              # Reference template
  FEATURE_GUIDE.md        # Creation guide (NEW)
  ...
  WTI_RULES.md            # Integrity rules (existing)
  DOD.md                  # Definition of Done (NEW, shared)
```

Or alternatively, embed the creation guide as a collapsible section at the top of each reference template.

#### 4. Extract Shared Definition of Done

Create a `DOD.md` that captures process-level quality standards applicable to ALL work items:

```markdown
## Definition of Done (All Work Items)
- [ ] Code committed to version control
- [ ] Tests written and passing
- [ ] Documentation updated (if applicable)
- [ ] Peer review completed
- [ ] AC verified by creator/reviewer
- [ ] Evidence section populated (WTI-006)
```

This explicitly removes these items from individual AC, solving the AC/DoD confusion.

#### 5. Implement Smart Checkpoint Strategy

Based on autonomy level research and rubber-stamp risk findings:

| Action Type | Review Level | Rationale |
|-------------|-------------|-----------|
| Fix formatting/structure | Auto (L3) | Low risk, well-defined rules |
| Create standard work item | Summary scan (L2) | Agent drafts, human scans 1-line summary |
| Create item with 6+ AC | Full review (L1) | Scope concern, may need splitting |
| Cross-epic dependency | Full review (L1) | Coordination risk |
| Scope change / deletion | Explicit approval (L0) | Destructive, irreversible |
| Architecture decision | Full review (L1) | High impact, needs human judgment |

#### 6. Design Quality Assessment Rubric for LLM Use

Since research shows LLMs achieve near-human reliability when given **explicit evaluation criteria**, create a machine-readable rubric:

```yaml
ac_quality_rubric:
  testable:
    description: "Can be verified with yes/no answer"
    scoring: "PASS if criterion has clear, measurable condition; FAIL if vague or subjective"
    examples:
      good: "User can sort results by date, name, or relevance"
      bad: "Sorting works well"

  outcome_focused:
    description: "Describes what, not how"
    scoring: "PASS if no technology/implementation mentioned; FAIL if prescribes solution"
    examples:
      good: "Search results return within 200ms"
      bad: "Use Elasticsearch with a 3-shard index for search"

  not_dod:
    description: "Not a Definition of Done item"
    scoring: "FAIL if mentions code review, testing, documentation, deployment, monitoring"
    examples:
      good: "User receives email confirmation within 5 minutes"
      bad: "Unit tests written with 90% coverage"
```

---

## Sources

### Academic Papers

- [Improving agile requirements: the Quality User Story framework and tool](https://link.springer.com/article/10.1007/s00766-016-0250-x) -- Lucassen, Dalpiaz, et al. (2016), Requirements Engineering, Springer
- [Can LLMs Generate User Stories and Assess Their Quality?](https://arxiv.org/abs/2507.15157) -- arXiv:2507.15157 (2025)
- [Evaluating user story quality with LLMs: a comparative study](https://link.springer.com/article/10.1007/s10844-025-00939-3) -- Journal of Intelligent Information Systems, Springer (2025)
- [Exploring the Use of LLMs for Requirements Specification](https://arxiv.org/html/2507.19113v1) -- arXiv:2507.19113 (2025)
- [AQUSA: The Automatic Quality User Story Artisan](https://ceur-ws.org/Vol-1564/paper34.pdf) -- CEUR Workshop Proceedings
- [UStAI Dataset: Leveraging LLMs for User Stories in AI Systems](https://dl.acm.org/doi/10.1145/3727582.3728689) -- ACM PROMISE 2025

### Industry Sources -- Acceptance Criteria

- [Given-When-Then Acceptance Criteria: Guide (2025)](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria) -- Parallel HQ
- [Acceptance Criteria Explained](https://www.atlassian.com/work-management/project-management/acceptance-criteria) -- Atlassian
- [Acceptance Criteria: Purposes, Types, Examples and Best Practices](https://www.altexsoft.com/blog/acceptance-criteria-purposes-formats-and-best-practices/) -- AltexSoft
- [What is acceptance criteria? Definition and Best Practices](https://www.productplan.com/glossary/acceptance-criteria/) -- ProductPlan
- [Acceptance Criteria: Everything You Need to Know](https://resources.scrumalliance.org/Article/need-know-acceptance-criteria) -- Scrum Alliance
- [How many AC should a user story have?](https://www.scrum.org/forum/scrum-forum/94804/what-best-practices-writing-user-stories-how-many-acceptance-criteria-should-normally-maximal-user-story-have) -- Scrum.org Forum
- [Acceptance Criteria vs Definition of Done](https://www.agilesherpas.com/blog/definition-of-done-acceptance-criteria) -- Agile Sherpas
- [Definition of Done vs. Acceptance Criteria](https://www.altexsoft.com/blog/acceptance-criteria-definition-of-done/) -- AltexSoft
- [Acceptance Criteria vs Definition of Done](https://nulab.com/learn/software-development/definition-of-done-vs-acceptance-criteria/) -- Nulab

### Industry Sources -- INVEST & Story Quality

- [What does INVEST Stand For?](https://agilealliance.org/glossary/invest/) -- Agile Alliance
- [Creating The Perfect User Story With INVEST Criteria](https://scrum-master.org/en/creating-the-perfect-user-story-with-invest-criteria/) -- Scrum-Master.org
- [INVEST Criteria For User Stories in SAFe](https://www.leanwisdom.com/blog/crafting-high-quality-user-stories-with-the-invest-criteria-in-safe/) -- Lean Wisdom

### Industry Sources -- Human-in-the-Loop & Trust

- [Rubber Stamp Risk: Why "Human Oversight" Can Become False Confidence](https://cybermaniacs.com/cm-blog/rubber-stamp-risk-why-human-oversight-can-become-false-confidence) -- CyberManiacs
- [The Meaning and Illusion of Human Oversight of AI](https://mediate.com/the-meaning-and-illusion-of-human-oversight-of-ai/) -- Mediate.com
- [Building trust in agentic tools: What we learned from our users](https://about.gitlab.com/blog/building-trust-in-agentic-tools-what-we-learned-from-our-users/) -- GitLab
- [Human-in-the-Loop AI Review Queues: Workflow Patterns That Scale](https://alldaystech.com/guides/artificial-intelligence/human-in-the-loop-ai-review-queue-workflows) -- All Days Tech
- [Human-in-the-loop in AI workflows: Meaning and patterns](https://zapier.com/blog/human-in-the-loop/) -- Zapier
- [Human-in-the-Loop for AI Agents: Best Practices](https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo) -- Permit.io
- [The 5 levels of AI agent autonomy](https://tessl.io/blog/the-5-levels-of-ai-agent-autonomy-learning-from-self-driving-cars/) -- Tessl.io
- [Levels of Autonomy for AI Agents](https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1) -- Knight First Amendment Institute, Columbia University
- [How to Measure Human Oversight Effectiveness in AI Workflows](https://www.resumly.ai/blog/how-to-measure-human-oversight-effectiveness-in-ai-workflows) -- Resumly

### Industry Sources -- Documentation Patterns

- [Diataxis Documentation Framework](https://diataxis.fr/) -- Daniele Procida
- [What is Diataxis and should you be using it?](https://idratherbewriting.com/blog/what-is-diataxis-documentation-framework) -- I'd Rather Be Writing
- [We fixed our documentation with the Diataxis framework](https://blog.sequinstream.com/we-fixed-our-documentation-with-the-diataxis-framework/) -- Sequin
- [Quick Reference Guide Templates](https://usewhale.io/blog/quick-reference-guide-template/) -- Whale
- [How To Create A Quick Reference Guide](https://essentialdata.com/how-to-create-quick-reference-guides-quick-reference-guides/) -- Essential Data Corp
- [Quick Reference Guide Templates for 2026](https://www.glitter.io/blog/process-documentation/quick-reference-guide-template) -- Glitter AI

### LLM Evaluation Tools

- [Top 6 LLM Evaluation Tools (2025)](https://orq.ai/blog/llm-evaluation-tools) -- Orq.ai
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) -- Anthropic
- [LLM Evaluation Metrics](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation) -- Confident AI

---

*Research completed: 2026-02-16*
*Agent: ps-researcher v2.0.0*
*Total sources cited: 35+*

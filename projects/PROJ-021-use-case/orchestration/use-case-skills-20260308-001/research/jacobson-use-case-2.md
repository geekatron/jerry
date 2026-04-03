# Jacobson Use Case 2.0 Methodology Research

> **PS ID:** proj-021 | **Entry ID:** e-001 | **Topic:** Jacobson Use Case 2.0 Methodology
> **Researcher:** ps-researcher | **Date:** 2026-03-08
> **Confidence:** HIGH (0.92) -- Primary source fully extracted; 5+ sources cross-referenced

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings for project stakeholders |
| [L1: Technical Analysis](#l1-technical-analysis) | Full methodology details for skill implementers |
| [L2: Strategic Implications](#l2-strategic-implications) | Architectural guidance for Jerry skill design |
| [Research Questions](#research-questions) | What was investigated |
| [Methodology](#methodology) | How research was conducted |
| [References](#references) | All cited sources with URLs |

---

## L0: Executive Summary

Use Case 2.0 is Ivar Jacobson's modernization of the use case technique for agile and lean contexts, published in 2011 with Ian Spence and Kurt Bittner and updated through 2023. It is **not** a UML update but an evolution of how teams apply use cases. Key findings:

- **Use Case Slicing is the central innovation.** UC 2.0 introduces the concept of a "use-case slice" -- one or more stories selected from a use case to form a work item of clear value to the customer. Slices are the primary backlog items and cut across requirements, design, implementation, and test. This is what makes UC 2.0 agile-compatible while preserving the big-picture benefits of use cases.

- **The methodology defines six principles, three "things to work with," five work products, and seven activities.** It is deliberately lightweight -- teams start with bare essentials and scale detail up as needed. The practice works with Scrum, Kanban, and even waterfall.

- **A slice has a five-state lifecycle: Scoped, Prepared, Analyzed, Implemented, Verified.** These states map directly to Kanban columns and sprint planning. Multiple slices can be in different states simultaneously (one being verified while another is being analyzed).

- **Test cases are the most important work product** -- more important than narratives. They define what "done" means for each slice. This makes UC 2.0 inherently test-driven.

- **UC 2.0 complements user stories rather than replacing them.** Slices naturally satisfy the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable) while maintaining the broader context that user stories alone cannot provide.

**Project Impact:** These findings directly inform three Jerry skills: `/use-case` (modeling and slicing), `/test-spec` (test case definition from slices), and `/contract-design` (system interface contracts derived from use-case realizations).

---

## Research Questions

| # | Question | Status |
|---|----------|--------|
| RQ-1 | What distinguishes Use Case 2.0 from traditional use cases? | ANSWERED |
| RQ-2 | What are the seven activities and their purposes? | ANSWERED |
| RQ-3 | How does use case slicing work? | ANSWERED |
| RQ-4 | How are use case narratives structured? | ANSWERED |
| RQ-5 | What is the slice lifecycle? | ANSWERED |
| RQ-6 | How does UC 2.0 relate to Cockburn's work? | ANSWERED |

---

## Methodology

| Aspect | Detail |
|--------|--------|
| **Primary Source** | Jacobson, Spence, Bittner. "Use-Case 2.0: The Guide to Succeeding with Use Cases" (ebook, 2011, updated 2023). Full text extracted and analyzed. |
| **Secondary Sources** | InfoQ practitioner case study (Dutch Railways, 2014-2016); InfoQ article on slicing vs laminating (Cockburn comparison, 2014); ACM Queue article; LinkedIn article by Jacobson |
| **Tertiary Sources** | Wikipedia (Use Case article); t2informatik Smartpedia; microTOOL knowledge base |
| **Cross-Reference Count** | 7 distinct sources (exceeds UC-017 minimum of 3) |
| **Verification Method** | All terminology, templates, and activity names verified against the primary Jacobson/Spence/Bittner ebook (UC-016 compliance) |

---

## L1: Technical Analysis

### 1. What Distinguishes Use Case 2.0 from Traditional Use Cases (RQ-1)

Use Case 2.0 is defined by Jacobson as "a scalable, agile practice that uses use cases to capture a set of requirements and drive the incremental development of a system to fulfill them" [1]. It is **not** a UML specification update. The key distinguishing characteristics are:

| Aspect | Traditional Use Cases | Use Case 2.0 |
|--------|----------------------|--------------|
| Granularity | Whole use case as work unit | **Use-case slices** as work units |
| Detail level | Often fully specified upfront | Progressive detail -- start with bare essentials, scale up |
| Agile fit | Perceived as heavyweight, waterfall | Explicitly designed for Scrum, Kanban, iterative |
| Backlog items | User stories or whole use cases | Use-case slices (satisfy INVEST criteria) |
| Test approach | Tests written after requirements | Test cases created **during** slice preparation (test-driven) |
| Scope | Requirements capture only | Full lifecycle: requirements, analysis, design, implementation, test |
| Scale | One-size-fits-all | Scales in (more guidance), out (full lifecycle), up (large systems) |

**Source:** Jacobson, Spence, Bittner, "Use-Case 2.0: The Guide to Succeeding with Use Cases" [1], pp. 3-4.

#### The Six Principles

Use Case 2.0 is founded on six principles [1, pp. 5-11]:

1. **Keep it simple by telling stories.** Storytelling is the primary mechanism for communicating requirements. Use cases capture goals; stories explore how to achieve them. Stories are captured in use-case narratives and validated by test cases.

2. **Understand the big picture.** The use-case model provides an accessible overview of all the ways a system will be used, without getting bogged down in detail. A use-case diagram shows actors (stick figures) and use cases (ellipses) with arrowheads indicating who initiates the interaction.

3. **Focus on value.** Structure narratives to make value easy to quantify: start with the simplest way to achieve the goal (basic flow), then add alternative ways and problem handling. This additive structure means you never need to deliver the whole use case -- focus on the parts that offer the most value.

4. **Build the system in slices.** The central innovation. Identify the most useful thing the system does, slice it into thinner slices, decide on test cases for acceptance, choose the most central slice (end-to-end through the concept), estimate, and start building. Slices cut through requirements, design, implementation, and test.

5. **Deliver the system in increments.** Each increment builds on the previous one. Use cases enable release planning (whole swathes of requirements deferred to later releases); slices enable increment planning within releases.

6. **Adapt to meet the team's needs.** UC 2.0 scales from lightweight index cards for small co-located teams to detailed documents for large distributed teams. The team decides how much detail to add beyond the essentials.

**Source:** Jacobson, Spence, Bittner [1], pp. 5-11.

### 2. The Seven Activities (RQ-2)

UC 2.0 defines seven activities grouped into two categories [1, pp. 23-29]:

#### Activities to Discover, Order, and Verify Requirements

| # | Activity | Purpose | Inputs | Outputs | Key Decision Criteria |
|---|----------|---------|--------|---------|-----------------------|
| 1 | **Find Actors and Use Cases** | Establish goals, scope releases, identify ways of using and testing the system | Stakeholder workshops, brainstorming | Use-case model (actors + use cases), outlined use cases | Focus on value-providing use cases first; do not find all at once |
| 2 | **Slice the Use Cases** | Create suitably sized work items, fit within time/budget, deliver highest value | Outlined use cases with basic flow understood | Ordered set of use-case slices | Slice based on stories; first slice should be basic flow (end-to-end); slice as thin as needed |
| 3 | **Inspect and Adapt the Use Cases** | Handle changes, track progress, keep model current, tune slice sizes | In-progress work, change requests, lessons learned | Updated use-case model, re-ordered slices, adjusted detail levels | Continuous activity; monitor backlog; adjust slice size to eliminate waste |

#### Activities to Shape, Implement, and Test the System Slice-by-Slice

| # | Activity | Purpose | Inputs | Outputs | Key Decision Criteria |
|---|----------|---------|--------|---------|-----------------------|
| 4 | **Prepare a Use-Case Slice** | Get slice ready for implementation; define what "done" means | Selected use-case slice, stakeholder input | Enhanced narrative + test cases for the slice | Collaborative (stakeholders + developers + testers); if no test cases, slice is NOT properly prepared |
| 5 | **Analyze a Use-Case Slice** | Understand impact on system elements; define responsibilities and interactions | Prepared slice, system architecture knowledge | Use-case realization (which system elements are affected, how) | Lightweight collaborative analysis; sketch on whiteboard; becomes easier as architecture matures |
| 6 | **Implement Software (for a Slice)** | Design, code, unit test, and integrate the software for the slice | Analyzed slice | Working software implementing the slice | Slice-by-slice development; different team members work in parallel on different slices |
| 7 | **Test the System (for a Slice AND as a Whole)** | Verify slice implementation; verify system-wide integration | Implemented slice, test cases | Verified slice; regression-tested system | Two levels: (a) test each slice independently against its test cases; (b) test system as a whole to ensure all slices work together |

**Important:** These activities are NOT sequential phases. They are performed repeatedly and in parallel. While one slice is being verified, another is being implemented, a third is being analyzed, and a fourth is being prepared [1, p. 16].

**Source:** Jacobson, Spence, Bittner [1], pp. 23-29.

### 3. Use Case Slicing -- The Central Innovation (RQ-3)

#### What is a Slice?

> "A use-case slice is one or more stories selected from a use case to form a work item that is of clear value to the customer. It acts as a placeholder for all the work required to complete the implementation of the selected stories." -- Jacobson, Spence, Bittner [1], p. 15

Key characteristics of a use-case slice:

- **More than just requirements:** A slice cuts through requirements, design, implementation, and test assets [1, p. 9]. It includes:
  - The stories (from the use-case narrative) that define the requirements
  - The design elements (use-case realization) showing how the system implements them
  - The code that realizes the stories
  - The test cases and test scripts that verify the implementation

- **Enables decomposition:** Use cases cover many related stories. Slices allow teams to: (a) select which pieces to deliver when, (b) provide suitable units for development and testing, (c) create small, similarly-sized work items that flow quickly through development [1, p. 15].

- **Primary backlog items:** In agile contexts, use-case slices are the primary backlog items -- not the use cases themselves. Slices satisfy the INVEST criteria naturally because the narrative structure makes them independent, negotiable, valuable, estimable, small, and testable [1, p. 32].

#### How to Slice

The slicing recipe from the ebook [1, pp. 8-9]:

1. **Identify the most useful use case** -- the most useful thing the system does.
2. **Select the most useful use case and find its basic flow** -- shed all less important alternative flows.
3. **Create the first slice from the basic flow** -- this is guaranteed to be end-to-end because the basic flow is the most straightforward way for the user to achieve their goal.
4. **The first slice might not even be the whole basic flow** -- take a subset, skipping detail of some steps and stubbing up the solution for others, to attack the biggest challenges.
5. **Add additional slices** from the same use case until there are enough for a usable solution.
6. **Repeat for other use cases** as needed to complete a usable system.

#### Slice Granularity

From the Dutch Railways case study, three dimensions determine slice granularity [3]:

1. **Scope of the slice** -- which stories are included
2. **Goal (value) of the slice** -- what value it delivers to the user
3. **Global idea of the effort** -- estimated work to implement

The slice should be small enough to complete within a sprint but large enough to deliver clear, testable value. The ebook explicitly states: "the slicing mechanism is very flexible enabling you to create slices as big or small as you need to drive your development" [1, p. 9].

#### Slice Dependency Patterns

Slices from the same use case have a natural ordering:

- **Basic flow first:** The first slice should always be based on the basic flow [1, p. 25].
- **Alternative flows build on the basic flow:** Each alternative flow adds to or modifies the basic flow, so slices based on alternative flows naturally depend on the basic flow slice being implemented first.
- **Cross-use-case slices are independent:** Slices from different use cases can typically be implemented in any order, though system-level dependencies may exist.

**Example from the ebook** [1, p. 20]:
- Slice 7.1: "Select and Buy 1 Product" (basic flow, 5 story points)
- Slice 7.2: "Select and Buy 100 Products" (basic flow variation, 5 story points)
- Slice 7.3: "Support Systems Unavailable" (multiple alternative flows A9, A10, A11, A12; 13 story points)

**Source:** Jacobson, Spence, Bittner [1], pp. 8-9, 15-16, 20, 25; Dutch Railways case study [3].

### 4. Use Case Narratives (RQ-4)

#### Narrative Structure

A use-case narrative tells the story of how the system and its actors work together to achieve a particular goal. The structure is **additive** [1, pp. 7-8]:

```
USE-CASE NARRATIVE
|
+-- BASIC FLOW (required; simplest way to achieve the goal)
|   |-- Step 1
|   |-- Step 2
|   |-- Step 3
|   |-- ...
|   +-- Step N
|
+-- ALTERNATIVE FLOWS (optional; build on the basic flow)
    |-- A1: [variant name] (branches from step X)
    |-- A2: [variant name] (branches from step Y)
    |-- A3: [variant name] (optional facility)
    |-- A4: [error handling] (problem at step Z)
    +-- ...
```

**Basic Flow:** The normal, expected path through the use case -- the path taken by most users most of the time. This is the most important part of the narrative. It describes the simplest way to achieve the goal as a set of simple steps capturing the interaction between users and the system [1, p. 7].

**Alternative Flows:** Defined relative to the basic flow. They include [1, p. 7]:
- Other ways of achieving the goal (e.g., non-standard amount at ATM)
- Optional facilities (e.g., dispensing a receipt)
- Problems that could occur (e.g., card stuck, insufficient funds)

**Important:** The alternative flows are NOT called "exception flows" in Jacobson's UC 2.0 terminology. Problems and error conditions are simply types of alternative flows. This differs from some traditional use case templates that distinguish between alternative and exception flows.

#### Narrative Levels of Detail

The ebook defines four progressive levels of detail for use-case narratives [1, p. 22, pp. 47-48]:

| Level | Name | Description | When to Use |
|-------|------|-------------|-------------|
| 1 | **Briefly Described** | Just captures the goal of the use case and which actor starts it | Use cases you decide not to implement |
| 2 | **Bulleted Outline** | Outlines steps of basic flow and brainstorms alternative flows; enough to understand size and complexity | Lightest level enabling slicing; suitable for close-collaboration teams |
| 3 | **Essential Outline** | Clarifies responsibilities between system and actors (dialog format) | Establishing new architecture or user experience |
| 4 | **Fully Described** | Comprehensive, highly detailed specification of all actions, inputs, outputs | Safety/financial/legal consequences; offshore/outsourced development |

**Key design principle:** "Not every use-case narrative needs to be taken to the same level of detail -- it is not uncommon for the most important and risky use cases to be more detailed than the others" [1, p. 48].

#### Stories and Their Relationship to Narratives

Stories are threads through the use-case narrative. Each story traverses one or more flows, starting at the beginning of the basic flow and terminating at the end [1, p. 16]. Two approaches to finding stories:

- **Top Down:** (1) identify the use case, (2) outline basic flow steps, (3) brainstorm alternative flows. The structure leads to stories.
- **Bottom Up:** Brainstorm stories, group by theme to identify use cases, examine stories to identify flows, then identify missing stories.

**Source:** Jacobson, Spence, Bittner [1], pp. 7-8, 16-17, 22, 47-48.

### 5. The Slice Lifecycle (RQ-5)

A use-case slice undergoes five state changes [1, p. 15]:

```
SCOPED --> PREPARED --> ANALYZED --> IMPLEMENTED --> VERIFIED
```

| State | Definition | What Happens | Entry Criteria |
|-------|-----------|--------------|----------------|
| **Scoped** | The extent of the stories covered has been clarified | Slice identified from use case; stories selected; initial estimate possible | Use case has "Story Structure Understood" state |
| **Prepared** | Narrative enhanced and test cases defined to clearly specify what "done" means | Collaborative work (stakeholders + devs + testers); use-case narrative detailed for this slice; test cases created | Slice selected for upcoming development |
| **Analyzed** | Impact on system components understood; affected pieces ready for coding | Use-case realization created; system elements identified; responsibilities allocated; interactions sketched | Slice prepared with test cases defined |
| **Implemented** | Software system enhanced to implement the slice; ready for testing | Code written, unit tested, integrated | Analysis complete; design understood |
| **Verified** | Slice verified as done; ready for inclusion in a release | All test cases pass; slice acceptance confirmed | Implementation complete; tests executed |

#### Use Case Lifecycle (Parent)

The parent use case also has its own lifecycle with five states [1, p. 14]:

| State | Definition |
|-------|-----------|
| **Goal Established** | The goal of the use case has been established |
| **Story Structure Understood** | Narrative structure understood enough to start identifying and implementing slices |
| **Simplest Story Fulfilled** | System fulfills the simplest story allowing a user to achieve the goal |
| **Sufficient Stories Fulfilled** | System fulfills enough stories for a usable solution |
| **All Stories Fulfilled** | System fulfills all stories told by the use case |

#### Mapping to Agile Practices

**Scrum/Iteration mapping** [1, pp. 31-33]:
- Before development: Find actors and use cases, slice use cases, prepare first slices
- Each iteration: Plan (may re-slice); Prepare, Analyze, Implement, Test slices; maintain backlog
- End of iteration: Test system as a whole; Inspect and Adapt use cases

**Kanban mapping** [1, pp. 34-36]:
The slice states map directly to Kanban columns:

```
INPUT        | PREPARATION      | DEVELOPMENT      | SYSTEM TEST    | LIVE
(Scoped)     | On-going | Done  | On-going | Done  | On-going | Done|
             | (Prepared)       | (Analyzed->Impl) | (Verified)     |
```

Work-in-progress limits apply to each column. The Dutch Railways case study confirmed this mapping works in practice, with developers appreciating "small enough stories, delivered just in time, to work effectively in sprints" [3].

**Source:** Jacobson, Spence, Bittner [1], pp. 14-16, 31-36; Dutch Railways case study [3].

### 6. Relationship to Traditional Use Cases and Cockburn (RQ-6)

#### UC 2.0 vs. Cockburn's "Writing Effective Use Cases"

Ivar Jacobson invented use cases (OOPSLA 1987). Alistair Cockburn published "Writing Effective Use Cases" (2000), which became the most widely used use case writing guide. In 2011, Jacobson published UC 2.0 with Spence and Bittner. These are complementary but distinct bodies of work [2, 4, 5]:

| Aspect | Cockburn (2000) | Jacobson UC 2.0 (2011) |
|--------|----------------|----------------------|
| **Focus** | Writing quality -- how to write good use cases | Development practice -- how to use use cases to drive development |
| **Primary contribution** | Goal levels (summary, user goal, subfunction); fully dressed template with preconditions, postconditions, stakeholder interests | Use-case slicing; progressive detail levels; slice lifecycle states |
| **Narrative structure** | Main success scenario + extensions (numbered deviations) | Basic flow + alternative flows (additive structure) |
| **Agile integration** | Adapted for evolutionary projects but not central focus | Explicitly designed for Scrum, Kanban, iterative |
| **Granularity** | Whole use case as work unit | Use-case slices as work units |
| **Template format** | Fully dressed template with 11+ sections | Lightweight levels of detail (4 levels from brief to fully described) |
| **Test emphasis** | Tests mentioned but not central | Test cases are "more important than the narrative" [1, p. 5] |

**Critical distinction (UC-002):** Cockburn's work focuses on use case **writing quality** -- how to identify the right goal level, how to structure scenarios, how to write clear steps. Jacobson's UC 2.0 focuses on use case **lifecycle management** -- how to slice use cases into agile work items, how to track their progress, how to use them to drive development. They address different problems and can be used together.

#### Cockburn's Laminating vs. Jacobson's Slicing

Alistair Cockburn proposed "laminating" as an alternative metaphor to slicing [4]: rather than decomposing a system into slices, teams construct systems incrementally by starting with a "walking skeleton" (minimal end-to-end implementation) and building outward. Cockburn argued: "We are starting from nothing and constructing the elephant. Having a pile of elephant slices does not produce an elephant" [4].

However, both approaches converge in practice: both start with the simplest end-to-end path and build incrementally. Jacobson's slicing makes the decomposition explicit and trackable; Cockburn's laminating emphasizes the constructive rather than decompositional metaphor.

#### Cockburn's Three Critiques of User Stories Alone

Cockburn identified three problems with exclusive use of user stories (without use cases) [2]:
1. User stories do not provide developers with **contextual information** -- how individual stories relate to each other
2. They do not provide an indication of **completion degree** -- how much of the system's functionality has been addressed
3. They do not provide a mechanism for **predicting potential difficulties** of unfinished work

UC 2.0 addresses all three through: (1) the use-case model providing the big picture, (2) the use case lifecycle states tracking progress, (3) the narrative structure making dependencies visible.

**Source:** Wikipedia Use Case article [2]; InfoQ slicing/laminating article [4]; Jacobson LinkedIn article [5]; Jacobson ebook [1].

### 7. The Five Work Products

UC 2.0 defines five work products [1, pp. 18-22, Appendix]:

| # | Work Product | Purpose | Levels of Detail |
|---|-------------|---------|-----------------|
| 1 | **Use-Case Model** | Visualizes requirements as actors + use cases; provides the big picture | Value Established > System Boundary Established > Structured |
| 2 | **Use-Case Narrative** | Tells the story of how system and actors work together to achieve a goal | Briefly Described > Bulleted Outline > Essential Outline > Fully Described |
| 3 | **Use-Case Realization** | Shows how system elements collaborate to perform a use case | Implementation Elements Identified > Responsibilities Allocated > Interaction Defined |
| 4 | **Test Case** | Defines what "done" means for a slice; provides inputs and expected results | Test Ideas Formulated > Scenario Chosen > Variables Identified > Variables Set > Scripted/Automated |
| 5 | **Supporting Information** | Captures terms, global requirements, and quality attributes | Initiated > Simply Defined > Modeled & Illustrated > Comprehensively Defined |

**Key insight:** Each work product has progressive levels of detail. Teams always start with the lightest level (bare essentials) and add detail only when needed. This is the "adapt to meet the team's needs" principle in action [1, p. 22].

**Source:** Jacobson, Spence, Bittner [1], pp. 18-22, Appendix (pp. 41-50).

### 8. The Three "Things to Work With"

At the conceptual core of UC 2.0 are three central things [1, p. 13]:

| Thing | Definition | States |
|-------|-----------|--------|
| **Use Case** | All the ways of using a system to achieve a particular goal for a particular user | Goal Established > Story Structure Understood > Simplest Story Fulfilled > Sufficient Stories Fulfilled > All Stories Fulfilled |
| **Use-Case Slice** | One or more stories selected from a use case to form a work item of clear value | Scoped > Prepared > Analyzed > Implemented > Verified |
| **Story** | A way of using a system that is of value to a user; described by part of the narrative, one or more flows, and one or more test cases | No explicit tracked states (stories are a thinking tool; tracking happens via use cases and slices) |

**Important:** Stories are not explicitly tracked as separate work items. They are a thinking tool used to explore use cases and find the right slices. Tracking happens at the use-case level (progress toward fulfillment) and slice level (progress toward verification) [1, p. 17].

**Source:** Jacobson, Spence, Bittner [1], pp. 13-17.

---

## L2: Strategic Implications for Jerry Skill Design

### Implications for `/use-case` Skill

1. **Modeling activity should produce a use-case model (actors + use cases) as the primary artifact.** The model provides the big picture. The skill should enforce the use-case diagram format (actors as external entities, use cases as goals).

2. **Slicing is the core workflow.** The skill should guide users through: (a) identifying use cases from stakeholder goals, (b) outlining the basic flow, (c) creating slices from the basic flow first, (d) adding alternative flow slices incrementally.

3. **Progressive detail levels should be enforced.** The skill should support the four narrative detail levels (Briefly Described, Bulleted Outline, Essential Outline, Fully Described) and discourage teams from jumping to Fully Described before it is needed.

4. **Slice lifecycle states should be tracked.** The skill (or worktracker integration) should track each slice through Scoped > Prepared > Analyzed > Implemented > Verified. These states map to Jerry worktracker entity states.

5. **Slice properties template.** Based on the ebook [1, p. 20], each slice should capture:
   - Name (derived from stories)
   - Parent use case reference
   - Flows covered (e.g., "BF", "A3, A5")
   - Test case references
   - Estimate (story points or t-shirt size)
   - State (Scoped/Prepared/Analyzed/Implemented/Verified)

### Implications for `/test-spec` Skill

1. **Test cases are the most important work product.** The ebook is emphatic: "It is the test cases that define what it means to successfully implement the use case" [1, p. 5]. The `/test-spec` skill should treat test case definition as a first-class activity, not an afterthought.

2. **Test cases should be created during slice preparation, not after implementation.** This makes UC 2.0 inherently test-driven. The skill should enforce the "Prepare" activity producing test cases alongside narrative detail.

3. **Test case progressive detail levels.** The skill should support: Test Ideas Formulated > Scenario Chosen > Variables Identified > Variables Set > Scripted/Automated. Teams should not be forced to jump to full automation before it is needed.

4. **Scenario-based test cases.** The structure of UC narratives produces independently executable, scenario-based test cases. Each story through the narrative defines at least one test case [1, p. 28].

### Implications for `/contract-design` Skill

1. **Use-case realizations define system element contracts.** The realization shows which system elements participate in each use case and what responsibilities they have. This directly informs interface/contract design.

2. **Progressive realization detail.** The skill should support: Implementation Elements Identified > Responsibilities Allocated > Interaction Defined. Early-stage contracts need only identify participants; detailed interaction contracts come later.

3. **Slice-scoped contracts.** Because slices cut across the full system stack, contracts should be defined at the slice level -- which elements need to change for this slice, and what are their new responsibilities.

### Cross-Skill Integration Architecture

```
/use-case                    /test-spec                  /contract-design
|                            |                           |
|-- Find Actors & UCs        |                           |
|-- Slice Use Cases          |                           |
|-- [Slice: Scoped]          |                           |
|                            |                           |
|-- Prepare Slice ---------> |-- Define Test Cases        |
|-- [Slice: Prepared]        |-- [Test Ideas -> Scenario] |
|                            |                           |
|                            |                           |-- Analyze Slice
|                            |                           |-- Define Realization
|                            |                           |-- [Slice: Analyzed]
|                            |                           |
|-- Implement Software       |                           |
|-- [Slice: Implemented]     |                           |
|                            |                           |
|                            |-- Test Slice               |
|                            |-- Test System (whole)      |
|                            |-- [Slice: Verified]        |
```

### Risks and Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Over-slicing:** Creating slices too small to deliver meaningful value | Enforce minimum slice criteria: must include at least one complete story with at least one test case |
| **Under-slicing:** Creating slices too large for a sprint | Guide teams to slice based on basic flow first; each alternative flow is typically its own slice |
| **Detail creep:** Teams jumping to Fully Described narratives prematurely | Default to Bulleted Outline level; require explicit justification for higher detail |
| **Cockburn/Jacobson confusion (UC-002):** Mixing terminology from different traditions | Clearly label all templates and terminology as "Jacobson UC 2.0" or "Cockburn"; never mix in a single artifact |
| **Narrative-only trap:** Teams focusing on narratives without test cases | Enforce the rule: "If the slice has no test cases, it has not been properly prepared" [1, p. 26] |

### Alignment with Jerry Framework

| UC 2.0 Concept | Jerry Mapping |
|----------------|---------------|
| Use Case | Feature or Epic (worktracker entity) |
| Use-Case Slice | Story or Task (worktracker entity) |
| Use-Case Model | Project-level artifact in `work/` |
| Use-Case Narrative | Artifact linked to Feature/Epic entity |
| Test Case | Linked to Story/Task entity |
| Use-Case Realization | Design artifact in `docs/design/` |
| Slice states (Scoped..Verified) | Worktracker entity status field |

---

## References

1. Jacobson, I., Spence, I., Bittner, K. (2011, updated 2023). *Use-Case 2.0: The Guide to Succeeding with Use Cases*. Ivar Jacobson International. -- Key insight: Comprehensive methodology definition including six principles, seven activities, five work products, slice lifecycle, and progressive detail levels. **Primary source for all terminology and templates.**
   - [Use-Case 2.0 e-Book (PDF)](https://www.ivarjacobson.com/files/use-case_2_0_e-book_2023_0.pdf)
   - [Use-Case 2.0 e-Book landing page](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book)

2. Wikipedia contributors. "Use case." *Wikipedia, The Free Encyclopedia*. -- Key insight: Historical context for use case evolution from Jacobson (1987) through Cockburn (2000) to UC 2.0 (2011); Cockburn's three critiques of user stories.
   - [Use case - Wikipedia](https://en.wikipedia.org/wiki/Use_case)

3. DiVetro, B. / Ivar Jacobson International. "Keeping Development 'On Track' with Use-Case Slices at Dutch Railways." *InfoQ* (2016). -- Key insight: Practitioner validation that UC 2.0 slicing works in real agile projects; three dimensions of slice granularity (scope, value, effort); challenges include finding right granularity and avoiding over-detailing.
   - [InfoQ Dutch Railways case study](https://www.infoq.com/articles/use-case-20-slices-Dutch-Railways/)
   - [IJI Dutch Railways case study](https://www.ivarjacobson.com/publications/case-studies/keeping-development-track-use-case-slices-dutch-railways-1)

4. Sato, D. "Applying Use Cases in Agile: Use Case 2.0, Slicing and Laminating." *InfoQ* (2014). -- Key insight: Cockburn's laminating metaphor as alternative to Jacobson's slicing; both converge on starting with simplest end-to-end path; Schaaf's definition of slice as "selection of use-case stories, plus test cases."
   - [InfoQ slicing and laminating article](https://www.infoq.com/news/2014/02/use-cases-agile/)

5. Jacobson, I. "Use-Case 2.0 - The Better Way of Doing Stories." *LinkedIn* (2014). -- Key insight: Jacobson's own framing of UC 2.0 as improving on user stories by providing context, completion tracking, and difficulty prediction.
   - [LinkedIn article](https://www.linkedin.com/pulse/use-case-20-better-way-doing-stories-ivar-jacobson)

6. Jacobson, I., Spence, I., Kerr, B. "Use-Case 2.0: The Hub of Software Development." *ACM Queue*, Vol. 14, No. 1 (2016). -- Key insight: Updated presentation of UC 2.0 in peer-reviewed venue; use cases as "the hub" connecting requirements to design, implementation, and test.
   - [ACM Queue article](https://queue.acm.org/detail.cfm?id=2912151)

7. Jacobson, I., Spence, I. "Use Cases Are Essential." *Communications of the ACM* (2023). -- Key insight: Latest publication arguing use cases remain essential even in modern agile; addresses common misconceptions.
   - [CACM article](https://cacm.acm.org/practice/use-case-2-0/)

---

## PS Integration

| Field | Value |
|-------|-------|
| **PS ID** | proj-021 |
| **Entry ID** | e-001 |
| **Artifact Type** | Research |
| **Confidence** | HIGH (0.92) |
| **Sources Count** | 7 |
| **Next Agent Hint** | ps-architect for skill design decisions |

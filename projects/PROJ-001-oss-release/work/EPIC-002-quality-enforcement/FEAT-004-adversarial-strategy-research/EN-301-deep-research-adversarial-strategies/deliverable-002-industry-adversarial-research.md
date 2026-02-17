# TASK-002: Industry Practices and LLM-Specific Adversarial Patterns

<!--
DOCUMENT-ID: FEAT-004:EN-301-TASK-002
AUTHOR: ps-researcher agent (v2.2.0)
DATE: 2026-02-12
STATUS: Complete (pending quality review)
PARENT: EN-301 (Deep Research: 15 Adversarial Strategies)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
PS-ID: EN-301
ENTRY-ID: TASK-002
-->

> **Version:** 1.0.0
> **Agent:** ps-researcher
> **Confidence:** HIGH for industry SE patterns (well-codified in standards), HIGH for LLM patterns (published 2022-2024, within training data), MEDIUM for emerging cross-domain adaptations
> **Research Limitation:** WebSearch and WebFetch tools were unavailable during this research session. All content is sourced from the agent's training knowledge (literature through May 2025). Citations reference real, verifiable publications. A follow-up web-validation pass is recommended to verify URLs and DOIs.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings for stakeholders |
| [L1: Research Methodology](#l1-research-methodology) | How the research was conducted |
| [L1: Strategy Catalog -- Software Engineering](#l1-strategy-catalog----software-engineering) | SE adversarial review patterns |
| [L1: Strategy Catalog -- Design and Product Review](#l1-strategy-catalog----design-and-product-review) | Design critique and challenge patterns |
| [L1: Strategy Catalog -- LLM-Specific Adversarial Patterns](#l1-strategy-catalog----llm-specific-adversarial-patterns) | AI/LLM adversarial review systems |
| [L1: Strategy Catalog -- QA Adversarial Patterns](#l1-strategy-catalog----qa-adversarial-patterns) | Testing-oriented adversarial methods |
| [L1: Comparative Analysis](#l1-comparative-analysis) | Cross-strategy comparison matrix |
| [L2: Architectural Implications for Jerry](#l2-architectural-implications-for-jerry) | Integration into multi-agent frameworks |
| [References](#references) | Complete citation list |

---

## L0: Executive Summary

This research identifies **14 adversarial review strategies** from industry software engineering practice, design review methodology, LLM/AI-specific research, and quality assurance traditions. These strategies complement the academic foundations documented in TASK-001 (argumentation theory, intelligence analysis, military red teaming) by providing **implementable patterns** drawn from codified engineering practice and emerging AI self-correction literature.

### Key Findings

1. **Software engineering has deep adversarial traditions** -- from Fagan's formal inspections (1976) through Google's modern code review culture, the field has developed structured adversarial review processes with measured defect-detection effectiveness.

2. **LLM self-correction is a rapidly maturing field** -- Constitutional AI (Anthropic, 2022), Self-Refine (Madaan et al., 2023), multi-agent debate (Du et al., 2023), and related systems provide directly implementable patterns for creator-critic-revision cycles in multi-agent frameworks.

3. **The creator-critic-revision cycle is a universal pattern** -- appearing independently in Fagan inspections (author-reviewer-rework), design critique (present-critique-iterate), Constitutional AI (generate-critique-revise), and Self-Refine (output-feedback-refine). This convergence validates Jerry's architectural choice.

4. **Strategy selection should be context-driven** -- no single strategy dominates. Fagan inspections excel for detailed artifact review; multi-agent debate excels for factual accuracy; Constitutional AI excels for normative alignment; ATAM excels for architectural quality attributes.

### Strategies Identified

| # | Strategy | Domain | Primary Mechanism |
|---|----------|--------|-------------------|
| 1 | Fagan Inspection | Software Engineering | Formal role-based defect detection |
| 2 | Google Code Review (Critique) | Software Engineering | Mandatory peer review with structured feedback |
| 3 | ATAM (Architecture Tradeoff Analysis Method) | Software Architecture | Stakeholder-driven scenario-based architecture evaluation |
| 4 | Pair Programming (Adversarial Pairing) | Software Engineering | Real-time continuous peer review |
| 5 | Design Critique (IDEO/d.school) | Design Thinking | Structured feedback with critique protocols |
| 6 | Constitutional AI Critique | AI/LLM | Self-critique against explicit principles |
| 7 | Self-Refine | AI/LLM | Iterative self-feedback and revision |
| 8 | Multi-Agent Debate | AI/LLM | Multiple LLMs argue to consensus |
| 9 | Chain-of-Verification (CoVe) | AI/LLM | Verification questions to catch hallucinations |
| 10 | CRITIC Framework | AI/LLM | Tool-augmented self-verification |
| 11 | Reflexion | AI/LLM | Linguistic reinforcement from failure analysis |
| 12 | LLM-as-Judge | AI/LLM | Structured evaluation with scoring rubrics |
| 13 | Mutation Testing | Software QA | Injected defects to test review effectiveness |
| 14 | Exploratory Testing Heuristics | Software QA | Session-based unscripted adversarial exploration |

### Overlap with TASK-001

Strategies 13 (Mutation Testing) and partially 1 (Fagan Inspection, which draws on the same formal methods tradition) overlap with TASK-001's coverage. These overlaps are intentional and expected; TASK-004 (synthesis) will resolve them during catalog consolidation.

---

## L1: Research Methodology

### Approach

1. **Domain Segmentation**: Research was organized into four domains -- software engineering, design/product review, LLM-specific AI patterns, and QA/testing -- to ensure comprehensive coverage across the required scope.

2. **Source Prioritization**: For SE patterns, prioritized IEEE/ACM publications, industry standards (NASA NPR 7150.2, IEEE 1028), and documented practices from major technology companies (Google, Microsoft). For LLM patterns, prioritized ArXiv publications from 2022-2024, focusing on papers with significant citation counts and from recognized research groups (Anthropic, Google DeepMind, Carnegie Mellon, MIT).

3. **Applicability Filter**: Each strategy was evaluated for applicability to LLM multi-agent workflows. Strategies that are purely manual (e.g., physical pair programming) were adapted to their LLM-applicable equivalents.

4. **Structured Documentation**: Each strategy documented with: name, origin/author, citation, description, mechanism, strengths, weaknesses, domain, and applicability to LLM workflows.

### Limitations

- No live web access for verification of URLs or DOIs
- LLM-specific papers from after May 2025 are not covered
- Industry practices at companies are documented based on published accounts; internal practices may differ
- Some LLM papers have been updated or superseded since initial ArXiv publication

---

## L1: Strategy Catalog -- Software Engineering

### Strategy 1: Fagan Inspection

**Name:** Fagan Inspection (Formal Software Inspection)

**Origin/Author:** Michael Fagan, IBM, 1976. Fagan developed the method while working at IBM's Kingston, New York facility. The method was the first formal, structured approach to software inspection and has influenced virtually all subsequent code review methodologies.

**Citation:**
- Fagan, M. E. "Design and Code Inspections to Reduce Errors in Program Development." *IBM Systems Journal*, 15(3), 182-211, 1976. DOI: 10.1147/sj.153.0182
- Fagan, M. E. "Advances in Software Inspections." *IEEE Transactions on Software Engineering*, SE-12(7), 744-751, 1986. DOI: 10.1109/TSE.1986.6312976
- IEEE 1028-2008. "IEEE Standard for Software Reviews and Audits." Institute of Electrical and Electronics Engineers, 2008.
- NASA NPR 7150.2, "NASA Software Engineering Requirements." Section 3.6 (Software Inspections). National Aeronautics and Space Administration.

**Description:** Fagan Inspection is a formal, structured software review process with defined roles, entry/exit criteria, and measured outcomes. It is the most rigorous form of peer review in software engineering, with empirical evidence showing defect detection rates of 60-90% for the inspected artifact. The method treats inspection as a manufacturing quality control process applied to intellectual work products.

**Mechanism (Step-by-Step):**

1. **Planning**: The moderator selects the artifact to inspect, identifies participants, distributes materials, and schedules the inspection meeting. Entry criteria must be met (e.g., artifact compiles, unit tests pass, author self-review complete).
2. **Overview** (optional): The author presents a brief overview of the artifact's purpose, design context, and any known issues. This is informational only -- no defect finding occurs here.
3. **Preparation**: Each inspector independently reviews the artifact against defined checklists and standards. Inspectors record all potential defects, questions, and suggestions. Preparation rate is controlled (typically 100-200 lines of code per hour for code inspections).
4. **Inspection Meeting**: The moderator leads a structured meeting where:
   - A designated **reader** paraphrases the artifact section by section
   - Inspectors raise defects they found during preparation
   - New defects discovered during discussion are also recorded
   - The **recorder** documents all defects with classification (major/minor) and location
   - The moderator enforces discipline: no solutions discussed, no author defense, focus on defect identification only
5. **Rework**: The author fixes all identified defects. No discretion on major defects -- all must be addressed.
6. **Follow-up**: The moderator verifies that all defects have been properly addressed. If rework is extensive, a re-inspection may be required.

**Defined Roles:**
| Role | Responsibility |
|------|---------------|
| Moderator | Facilitates process, enforces rules, verifies rework |
| Author | Created the artifact, performs rework |
| Reader | Paraphrases the artifact during meeting (not the author) |
| Inspector(s) | Find defects during preparation and meeting |
| Recorder | Documents all defects found |

**Strengths:**
- Empirically proven highest defect detection rate of any review method (60-90%)
- Structured roles prevent common review pathologies (author domination, tangential discussion)
- Measurable: defect density, inspection rate, and yield are tracked
- Entry/exit criteria ensure quality of the review process itself
- Separation of defect finding from defect fixing prevents premature solution discussion

**Weaknesses:**
- High ceremony and overhead (requires scheduling, multiple participants, formal meetings)
- Can be perceived as punitive if organizational culture is blame-oriented
- Inspection rate constraints limit throughput
- Requires trained moderators to be effective
- Diminishing returns on small or simple artifacts
- Modern async code review tools have largely replaced formal inspections in industry

**Domain:** Software Engineering, Systems Engineering, Aerospace/Defense

**Applicability to LLM Workflows:**
Fagan Inspection maps directly to Jerry's creator-critic-revision cycle:
- **Author** = Creator agent (produces the artifact)
- **Inspector** = Critic agent (reviews against checklists/principles)
- **Moderator** = Orchestrator (enforces process discipline, manages iterations)
- **Reader** = Can be implemented as a summarization step before critique
- **Entry/exit criteria** = Sync barrier pre/post conditions
- **Checklists** = Configurable review criteria per adversarial strategy

The key adaptation is that LLM inspection can be faster (no scheduling overhead) but must compensate for the loss of diverse human perspectives by using multi-persona or multi-strategy review.

---

### Strategy 2: Google Code Review (Critique System)

**Name:** Google Code Review / Critique System

**Origin/Author:** Google, evolved from early 2000s. Formalized and documented by Caitlin Sadowski et al. in their 2018 ICSE-SEIP paper. The system serves as the industry's most extensively documented large-scale mandatory code review practice.

**Citation:**
- Sadowski, C., Soderberg, E., Church, L., Sipko, M., and Bacchelli, A. "Modern Code Review: A Case Study at Google." *Proceedings of the 40th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP '18)*, pp. 181-190. ACM, 2018. DOI: 10.1145/3183519.3183525
- Rigby, P. C. and Bird, C. "Convergent Contemporary Software Peer Review Practices." *Proceedings of the 2013 9th Joint Meeting on Foundations of Software Engineering (ESEC/FSE '13)*, pp. 202-212. ACM, 2013. DOI: 10.1145/2491411.2491444
- Bacchelli, A. and Bird, C. "Expectations, Outcomes, and Challenges of Modern Code Review." *Proceedings of ICSE 2013*, pp. 712-721. IEEE, 2013. DOI: 10.1109/ICSE.2013.6606617

**Description:** Google's code review system (internally called "Critique") requires that every change to the codebase be reviewed by at least one other engineer before submission. The system combines mandatory peer review with tooling that automates style checks, test execution, and static analysis, allowing human reviewers to focus on design, correctness, and maintainability. At Google's scale (tens of thousands of changes per day), the system demonstrates that structured adversarial review can be embedded as a lightweight, continuous practice rather than a heavyweight ceremony.

**Mechanism (Step-by-Step):**

1. **Author Prepares Change**: Author writes code, runs pre-submit checks (linters, tests, static analysis). Automated tooling catches style and formatting issues before human review.
2. **Review Request**: Author selects reviewer(s) and submits the change for review via the Critique tool. Reviewer selection considers code ownership (OWNERS files), domain expertise, and load balancing.
3. **Reviewer Examination**: Reviewer examines the diff, reading the change in context. Reviews focus on:
   - Design: Is this the right approach? Does it fit the architecture?
   - Functionality: Does the code do what the author intended? Are there edge cases?
   - Complexity: Is this more complex than it needs to be?
   - Tests: Are tests adequate? Do they cover the important cases?
   - Naming/Comments: Are names clear? Are comments necessary and accurate?
   - Style: Does it follow the style guide? (Often auto-enforced)
4. **Feedback**: Reviewer provides comments at specific code locations. Comments are classified as:
   - **Must fix**: Blocking issues that must be resolved before approval
   - **Optional/Nit**: Suggestions that the author may accept or decline
   - **Question**: Clarification requests
5. **Author Response**: Author addresses feedback, updates the change, and responds to comments.
6. **Approval (LGTM)**: Reviewer approves ("Looks Good To Me") when satisfied. The change can then be submitted.
7. **Readability Review** (Google-specific): For certain languages, a designated "readability" reviewer ensures the code meets language-specific idiom and style standards.

**Strengths:**
- Lightweight enough for continuous use at massive scale
- Tooling automates mechanical checks, freeing human reviewers for design and logic
- Builds shared code ownership and knowledge transfer
- Creates a culture of continuous quality
- Asynchronous -- no scheduling overhead
- Documented evidence of defect prevention and knowledge sharing benefits

**Weaknesses:**
- Effectiveness varies with reviewer engagement (rubber-stamping is a known pathology)
- Reviewer selection affects quality (expert vs. junior reviewer)
- Not suitable for large architectural changes (better suited for incremental changes)
- Social dynamics can suppress critical feedback (fear of conflict)
- Review latency can become a bottleneck in fast-moving teams

**Domain:** Software Engineering, DevOps

**Applicability to LLM Workflows:**
Google's code review maps to lightweight, continuous critic invocation:
- **Mandatory review** = Every creator output must pass through a critic agent
- **LGTM threshold** = Quality score >= 0.92
- **Must-fix vs. nit classification** = Severity-based feedback prioritization
- **Automated pre-checks** = Pre-critic validation (format, structure, completeness)
- **Readability review** = Specialized review pass for style/consistency

The key insight for Jerry is the **lightweight continuous model**: rather than heavyweight Fagan inspections for every artifact, use Google-style review as the default and escalate to formal inspection only when quality scores are low.

---

### Strategy 3: ATAM (Architecture Tradeoff Analysis Method)

**Name:** Architecture Tradeoff Analysis Method (ATAM)

**Origin/Author:** Rick Kazman, Mark Klein, and Paul Clements at the Software Engineering Institute (SEI), Carnegie Mellon University. First published in 1998, refined through extensive industry application.

**Citation:**
- Kazman, R., Klein, M., and Clements, P. "ATAM: Method for Architecture Evaluation." Technical Report CMU/SEI-2000-TR-004. Software Engineering Institute, Carnegie Mellon University, 2000.
- Clements, P., Kazman, R., and Klein, M. *Evaluating Software Architectures: Methods and Case Studies*. Addison-Wesley, 2002. ISBN: 978-0201704822.
- Bass, L., Clements, P., and Kazman, R. *Software Architecture in Practice*, 4th Edition. Addison-Wesley, 2021. ISBN: 978-0136886099.
- Kazman, R., Klein, M., Barbacci, M., Longstaff, T., Lipson, H., and Carriere, J. "The Architecture Tradeoff Analysis Method." *Proceedings of the 4th IEEE International Conference on Engineering of Complex Computer Systems (ICECCS '98)*, pp. 68-78, 1998. DOI: 10.1109/ICECCS.1998.706657

**Description:** ATAM is a structured method for evaluating software architectures against quality attribute requirements (performance, security, modifiability, reliability, etc.) by identifying architectural decisions, the quality attributes they affect, and the tradeoffs between competing quality goals. ATAM is inherently adversarial because it forces stakeholders to surface conflicting requirements and architects to defend their decisions against scenario-based challenges.

**Mechanism (Step-by-Step):**

1. **Present ATAM Method**: The evaluation team explains the ATAM process to all stakeholders.
2. **Present Business Drivers**: The project manager presents the business context, key requirements, and quality attribute priorities.
3. **Present Architecture**: The architect presents the architecture, focusing on how it addresses the quality attribute requirements. This includes architectural approaches (patterns, tactics) used.
4. **Identify Architectural Approaches**: The evaluation team catalogs the architectural patterns, tactics, and decisions evident in the architecture.
5. **Generate Quality Attribute Utility Tree**: Stakeholders collaboratively build a utility tree that decomposes "utility" into quality attributes, then into specific scenarios ranked by importance and difficulty.
6. **Analyze Architectural Approaches**: For each high-priority scenario, the evaluation team probes how the architecture responds. Questions focus on: "What happens when [scenario]? Which architectural decision handles this? What are the risks?"
7. **Brainstorm and Prioritize Scenarios**: Broader stakeholder group generates additional scenarios. These are voted on and prioritized.
8. **Analyze Prioritized Scenarios**: Repeat analysis for newly prioritized scenarios.
9. **Present Results**: Document **sensitivity points** (where a small change has large effect), **tradeoff points** (where one quality attribute conflicts with another), **risks** (architectural decisions that may not achieve their goals), and **non-risks** (decisions that are well-founded).

**Strengths:**
- Forces explicit articulation of quality attribute tradeoffs
- Scenario-based evaluation grounds abstract architecture in concrete situations
- Identifies risks early, before implementation
- Engages diverse stakeholders (not just architects)
- Produces actionable outputs: sensitivity points, tradeoff points, risks
- Well-documented with extensive case study evidence

**Weaknesses:**
- Heavyweight: requires 3-4 days with multiple stakeholders
- Requires skilled evaluation team
- Architecture must be sufficiently defined to evaluate (not suitable for early-stage exploration)
- Can become political if stakeholders have conflicting agendas
- Results are scenario-dependent -- untested scenarios may hide risks

**Domain:** Software Architecture, Systems Engineering

**Applicability to LLM Workflows:**
ATAM maps to architectural review in Jerry's quality workflows:
- **Quality Attribute Utility Tree** = Configurable evaluation criteria with weights
- **Scenario-based probing** = Critic agent generates scenarios and tests architecture response
- **Sensitivity/tradeoff analysis** = Critic identifies where architectural decisions create tension
- **Multi-stakeholder input** = Multi-persona prompting to represent different stakeholder viewpoints

For Jerry, ATAM's structured scenario generation is particularly valuable for architecture review tasks. A critic agent could generate quality attribute scenarios and probe a design proposal systematically.

---

### Strategy 4: Pair Programming as Adversarial Review

**Name:** Pair Programming (Continuous Adversarial Pairing)

**Origin/Author:** Kent Beck, formalized in *Extreme Programming Explained* (1999). The practice has roots in earlier collaborative programming, but XP codified it as a first-class engineering practice.

**Citation:**
- Beck, K. *Extreme Programming Explained: Embrace Change*. Addison-Wesley, 1999. ISBN: 978-0201616415.
- Williams, L. and Kessler, R. *Pair Programming Illuminated*. Addison-Wesley, 2003. ISBN: 978-0201745764.
- Williams, L., Kessler, R. R., Cunningham, W., and Jeffries, R. "Strengthening the Case for Pair Programming." *IEEE Software*, 17(4), 19-25, 2000. DOI: 10.1109/52.854064

**Description:** Pair programming is a software development practice where two programmers work together at one workstation. One (the "driver") writes code while the other (the "navigator" or "observer") reviews each line as it is written. The roles switch frequently. This creates a **continuous, real-time adversarial review loop** where every design decision, variable name, and logic branch is immediately challenged or validated by the partner.

**Mechanism (Step-by-Step):**

1. **Pairing**: Two developers sit together (physically or virtually). They agree on the task and approach.
2. **Driver-Navigator Roles**: The driver types code while thinking aloud. The navigator observes, thinks strategically, checks for errors, considers edge cases, and suggests alternatives.
3. **Continuous Challenge**: The navigator's role is explicitly adversarial-constructive: "Why this approach?", "What about edge case X?", "Could this be simpler?", "Does this handle the error condition?"
4. **Role Switching**: Roles switch frequently (every 15-30 minutes or at natural breakpoints) to maintain engagement and ensure both developers exercise both tactical (driver) and strategic (navigator) thinking.
5. **Real-Time Resolution**: Disagreements are resolved immediately through discussion. The pair must reach consensus on each decision.
6. **Continuous Integration**: The pair's output integrates continuously, as the review is built into the creation process rather than applied afterward.

**Strengths:**
- Zero review latency -- defects caught as they are created
- Knowledge transfer happens automatically
- Reduces knowledge silos and bus factor
- Studies show comparable or lower total cost when accounting for reduced defect rate (Williams & Kessler)
- Forces continuous articulation of reasoning
- Social accountability improves focus

**Weaknesses:**
- Resource-intensive (two developers on one task)
- Effectiveness depends on pair compatibility and skill level balance
- Can be exhausting for extended periods
- Not suitable for all task types (e.g., simple mechanical changes)
- Scheduling and coordination overhead
- Cultural resistance in organizations that value individual productivity metrics

**Domain:** Software Engineering (Agile/XP)

**Applicability to LLM Workflows:**
Pair programming maps to **concurrent creator-critic execution** in LLM workflows:
- **Driver** = Creator agent producing output
- **Navigator** = Critic agent reviewing in real-time (interleaved generation and review)
- **Role switching** = Alternating which agent leads vs. reviews
- **Continuous challenge** = Inline critique rather than post-hoc review

For Jerry, this pattern suggests a variant where creator and critic operate in tight, interleaved loops rather than the sequential produce-then-review model. This could be implemented as a "pair mode" where the critic reviews after each section rather than waiting for the complete artifact.

---

## L1: Strategy Catalog -- Design and Product Review

### Strategy 5: Design Critique (IDEO/Stanford d.school Method)

**Name:** Design Critique / Structured Feedback Session

**Origin/Author:** Rooted in art and design education (the "crit" or "critique" tradition dating to the Ecole des Beaux-Arts, 19th century). Modernized and codified by IDEO, Stanford d.school, and design thinking practitioners. Key documented sources include Tom Kelley (IDEO), the Hasso Plattner Institute of Design at Stanford, and Liz Lerman's "Critical Response Process."

**Citation:**
- Kelley, T. and Kelley, D. *Creative Confidence: Unleashing the Creative Potential Within Us All*. Crown Business, 2013. ISBN: 978-0385349369.
- Lerman, L. and Borstel, J. *Liz Lerman's Critical Response Process: A Method for Getting Useful Feedback on Anything You Make, from Dance to Dessert*. Liz Lerman Dance Exchange, 2003. ISBN: 978-0972738507.
- Hasso Plattner Institute of Design at Stanford (d.school). "An Introduction to Design Thinking: Process Guide." Stanford University, 2010.
- Schon, D. A. *The Reflective Practitioner: How Professionals Think in Action*. Basic Books, 1983. ISBN: 978-0465068784.

**Description:** Design critique is a structured adversarial feedback method where a creator presents work-in-progress to a group of peers or experts, who provide feedback following specific protocols designed to be constructive yet challenging. Unlike casual feedback, design critique follows rules: the creator presents intent and constraints; critics ask clarifying questions before judging; feedback is specific, actionable, and tied to design goals rather than personal preference. The method balances the adversarial tension needed to improve quality with the psychological safety needed to encourage risk-taking.

**Mechanism (Step-by-Step):**

1. **Creator Presents Context**: The creator shares the work along with: the design intent (what problem this solves), constraints (time, resources, requirements), and specific feedback areas (what they want critiqued).
2. **Clarifying Questions**: Critics ask questions to understand, not to judge. "What were you trying to achieve with X?" "Why did you choose Y over Z?" This phase prevents premature critique based on misunderstanding.
3. **Value Identification**: Critics identify what is working well before identifying what needs improvement. This is not just politeness -- it prevents the creator from discarding strong elements during revision.
4. **Constructive Challenge**: Critics provide specific, actionable feedback. Good critique format: "I notice [observation]. This concerns me because [reason]. Have you considered [alternative]?" Bad critique: "I don't like this."
5. **Pattern Identification**: The group identifies patterns across multiple critics' feedback. If three critics independently flag the same issue, it is likely a genuine problem.
6. **Creator Synthesis**: The creator synthesizes feedback, identifies which critiques to act on, and explains their reasoning. Not all critique must be accepted -- but all must be addressed.

**Liz Lerman's Critical Response Process (Variant):**
1. Statements of Meaning: Responders state what was meaningful, evocative, or striking
2. Artist as Questioner: The creator asks questions about the work
3. Neutral Questions: Responders ask neutral (non-judgmental) questions
4. Permission-Based Opinions: Responders ask permission before offering opinions ("I have an opinion about X, would you like to hear it?")

**Strengths:**
- Balances adversarial challenge with psychological safety
- Creator retains agency (decides what feedback to act on)
- Structured format prevents common feedback pathologies (vagueness, personal preference, pile-on)
- Identifies patterns across multiple reviewers
- Applicable to any creative or design artifact (not just visual design)

**Weaknesses:**
- Requires skilled facilitation to maintain structure
- Can devolve into unstructured criticism without discipline
- Value identification step can become perfunctory
- Less effective for purely technical artifacts (better for design, UX, communication)
- Cultural norms vary -- some cultures find structured critique uncomfortable

**Domain:** Design, Product Development, Creative Arts, UX

**Applicability to LLM Workflows:**
Design critique maps to a **structured multi-phase review** in Jerry:
- **Context presentation** = Creator provides intent and constraints alongside the artifact
- **Clarifying questions** = Critic agent asks questions before generating critique
- **Value identification** = Critic explicitly identifies strengths before weaknesses
- **Constructive challenge format** = Templated feedback: observation + concern + alternative
- **Permission-based opinions** = Configurable critique depth (light review vs. deep challenge)

The Liz Lerman variant is particularly interesting for LLM workflows because the permission model creates explicit control over critique intensity, which can be mapped to review severity levels.

---

## L1: Strategy Catalog -- LLM-Specific Adversarial Patterns

### Strategy 6: Constitutional AI Critique

**Name:** Constitutional AI (CAI) Critique and Revision

**Origin/Author:** Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, et al. at Anthropic. Published December 2022.

**Citation:**
- Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKinnon, C., Chen, C., Olsson, C., Olah, C., Hernandez, D., Drain, D., Ganguli, D., Li, D., Tran-Johnson, E., Perez, E., Kerr, J., Mueller, J., Ladish, J., Landau, J., Ndousse, K., Lukosiute, K., Lovitt, L., Sellitto, M., Elhage, N., Schiefer, N., Mercado, N., DasSarma, N., Lasenby, R., Larson, R., Ringer, S., Johnston, S., Kravec, S., El Showk, S., Fort, S., Lanham, T., Telleen-Lawton, T., Conerly, T., Henighan, T., Hume, T., Bowman, S. R., Hatfield-Dodds, Z., Mann, B., Amodei, D., Joseph, N., McCandlish, S., Brown, T., and Kaplan, J. "Constitutional AI: Harmlessness from AI Feedback." ArXiv preprint arXiv:2212.08073, 2022.
- Anthropic. "Claude's Constitution." https://www.anthropic.com/index/claudes-constitution (published 2023).

**Description:** Constitutional AI (CAI) is a training and inference-time technique where an AI model critiques and revises its own outputs according to a set of explicit principles (the "constitution"). The critique-revision process operates without human feedback on individual outputs -- instead, the model applies principled self-evaluation. At inference time, the CAI pattern generates a response, then critiques it against each constitutional principle, then revises the response to address the critique. This create-critique-revise cycle can iterate multiple times.

**Mechanism (Step-by-Step):**

1. **Define Constitution**: Establish a set of explicit, written principles that outputs must satisfy. Principles are specific and evaluable (e.g., "The response should not contain stereotypes" rather than "Be fair"). Anthropic's constitution draws from the UN Declaration of Human Rights, Apple's Terms of Service (for non-harmful content), and research on AI safety.
2. **Generate Initial Response**: The model generates a response to the input prompt.
3. **Self-Critique**: The model is prompted to critique its own response against each constitutional principle. The critique prompt typically follows the form: "Identify specific ways the response violates the principle: [principle text]. List each violation."
4. **Revision**: The model is prompted to revise the response to address the critique: "Revise the response to address the following critique: [critique output]. The revision should fix the identified issues while maintaining the useful content."
5. **Iterate**: Steps 3-4 repeat for each constitutional principle or until no further violations are found.
6. **RLAIF (Training-Time)**: The critique-revision pairs are used to train a preference model (Reinforcement Learning from AI Feedback), which is then used to fine-tune the model. This bakes the constitutional principles into the model's default behavior.

**Strengths:**
- Scales without human annotation (self-supervised critique)
- Explicit, auditable principles (the constitution is a document, not a black box)
- Iterative refinement catches issues that single-pass review misses
- Separates normative evaluation (what should be) from factual evaluation (what is)
- Principles can be customized for different contexts and domains
- The constitution serves as a contract between the system and its users

**Weaknesses:**
- Self-critique is limited by the model's own blind spots (model cannot catch errors it doesn't recognize)
- Constitutional principles must be well-written -- vague principles produce vague critique
- Iteration can be slow (each principle requires a critique-revision pass)
- May over-correct, producing bland or overly cautious outputs
- Does not address factual accuracy (only normative/behavioral alignment)
- Training-time RLAIF requires significant compute resources

**Domain:** AI Safety, AI Alignment, LLM Output Quality

**Applicability to LLM Workflows:**
CAI maps directly to Jerry's adversarial review:
- **Constitution** = Review criteria/checklist for each adversarial strategy (e.g., Red Team checklist, Steelman criteria)
- **Self-critique step** = Critic agent evaluates creator output against defined principles
- **Revision step** = Creator agent revises based on critic feedback
- **Multi-principle iteration** = Sequential application of multiple review strategies
- **RLAIF** = Not applicable at inference time, but the principle of "constitution as contract" is directly applicable

**Key Insight for Jerry:** The constitution concept provides a template for how adversarial review criteria should be specified -- as explicit, evaluable, written principles rather than vague instructions like "review this carefully."

---

### Strategy 7: Self-Refine

**Name:** Self-Refine: Iterative Refinement with Self-Feedback

**Origin/Author:** Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. Carnegie Mellon University, Allen Institute for AI, Google DeepMind, University of Washington, University of British Columbia. Published 2023.

**Citation:**
- Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., Gupta, S., Majumder, B. P., Hermann, K., Welleck, S., Yazdanbakhsh, A., and Clark, P. "Self-Refine: Iterative Refinement with Self-Feedback." *Advances in Neural Information Processing Systems 36 (NeurIPS 2023)*. ArXiv preprint arXiv:2303.17651, 2023.

**Description:** Self-Refine is a framework where a single LLM iteratively improves its own output through a generate-feedback-refine loop. Unlike Constitutional AI (which focuses on normative alignment), Self-Refine targets general output quality across diverse tasks: code generation, mathematical reasoning, dialogue, sentiment analysis, and more. The key insight is that the same model that generates an output can provide useful feedback on that output, and this feedback can drive meaningful improvement -- even without external tools or additional models.

**Mechanism (Step-by-Step):**

1. **Initial Generation**: The model generates an initial output for the given task.
2. **Self-Feedback**: The model is prompted to critique its own output. The feedback prompt is task-specific. For code: "Review this code for bugs, efficiency issues, and style problems." For reasoning: "Check this reasoning for logical errors, missing steps, or incorrect assumptions." The feedback is a natural language critique, not just a score.
3. **Refinement**: The model is given both the original output and the feedback, and prompted to produce an improved version. The refinement prompt: "Given the following output and feedback, produce an improved version that addresses the feedback."
4. **Iterate**: Steps 2-3 repeat until either: (a) the model's self-feedback indicates no further improvements, (b) a maximum iteration count is reached, or (c) the output quality plateaus (detected by comparing successive outputs).
5. **Stopping Criterion**: The loop terminates when the model's critique is empty ("No issues found") or when iteration count reaches the limit (typically 2-4 iterations).

**Empirical Results (from the paper):**
- Across 7 diverse tasks, Self-Refine improved output quality by 5-40% over the initial generation
- Improvements were observed even with a single refinement iteration
- Diminishing returns after 2-3 iterations for most tasks
- The feedback quality of the model on its own outputs was surprisingly good, though not perfect

**Strengths:**
- Simple to implement (requires only prompt engineering, no additional models or tools)
- Applicable to diverse tasks (code, math, dialogue, etc.)
- Demonstrated empirical improvement across multiple benchmarks
- No external tool dependencies
- The feedback step produces interpretable explanations of what needs improvement
- Stop criterion prevents unnecessary iterations

**Weaknesses:**
- Bounded by the model's own capabilities (cannot catch errors the model doesn't understand)
- Self-feedback may be systematically biased (model has consistent blind spots)
- Diminishing returns after 2-3 iterations
- Does not incorporate external verification (factual claims not checked against sources)
- Performance depends heavily on the quality of feedback prompts
- Can sometimes degrade output quality in later iterations (over-refinement)

**Domain:** AI/LLM, Natural Language Processing, Code Generation

**Applicability to LLM Workflows:**
Self-Refine is the simplest possible adversarial pattern for Jerry:
- **Single-agent self-review** = One agent reviews its own output before passing to critic
- **Task-specific feedback prompts** = Different review criteria for different artifact types
- **Iteration limit** = Jerry's 3-iteration maximum aligns with Self-Refine's empirical findings
- **Stop criterion** = Quality score threshold (0.92) serves as convergence criterion

**Key Insight for Jerry:** Self-Refine can be used as a **pre-critic self-check** -- the creator agent applies Self-Refine before submitting to the critic agent, improving the baseline quality and reducing critic iterations.

---

### Strategy 8: Multi-Agent Debate

**Name:** Multi-Agent Debate / Improving Factuality and Reasoning through Multiagent Debate

**Origin/Author:** Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, and Igor Mordatch. Massachusetts Institute of Technology, Google DeepMind. Published 2023.

**Citation:**
- Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., and Mordatch, I. "Improving Factuality and Reasoning in Language Models through Multiagent Debate." *Proceedings of the 40th International Conference on Machine Learning (ICML 2023)*. ArXiv preprint arXiv:2305.14325, 2023.
- Liang, T., He, Z., Jiao, W., Wang, X., Wang, Y., Wang, R., Yang, Y., Tu, Z., and Shi, S. "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate." ArXiv preprint arXiv:2305.19118, 2023.
- Chan, C., Chen, W., Su, Y., Yu, J., Xue, W., Zhang, S., Fu, J., and Liu, Z. "ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate." ArXiv preprint arXiv:2308.07201, 2023.

**Description:** Multi-Agent Debate is a framework where multiple LLM instances (or instances with different system prompts / personas) independently generate responses to the same query, then engage in structured rounds of debate where each agent can see the others' responses and arguments. Through iterative debate rounds, agents converge toward more accurate and well-reasoned outputs. The adversarial mechanism arises from agents challenging each other's claims, identifying inconsistencies, and forcing each agent to either defend or revise its position.

**Mechanism (Step-by-Step):**

1. **Independent Generation**: N agents (typically 2-4, each a separate LLM instance or differently-prompted instance) independently generate initial responses to the same query.
2. **Response Sharing**: All agents' responses are made visible to all other agents.
3. **Debate Round 1**: Each agent is prompted: "Here are other agents' responses. Examine their arguments. If you find errors or disagree, explain why. If they raise valid points you missed, acknowledge and incorporate them. Produce your revised response."
4. **Debate Round 2+**: Repeat step 3 for additional rounds (typically 2-4 total). Agents can change their position if convinced, or defend their original position with stronger arguments.
5. **Convergence/Aggregation**: After the final debate round, responses are aggregated. If agents converge to a shared answer, that answer is taken. If not, majority voting or a judge agent makes the final determination.

**Empirical Results (from Du et al. 2023):**
- Multi-agent debate significantly improved factual accuracy on benchmarks (GSM8K mathematical reasoning, TruthfulQA, MMLU)
- 2-3 agents with 2-3 debate rounds achieved the best tradeoff between quality and compute cost
- Agents successfully caught and corrected each other's factual errors and reasoning mistakes
- Performance improved even when all agents were instances of the same model (different random seeds suffice)

**Strengths:**
- Directly addresses factual accuracy (unlike CAI which focuses on normative alignment)
- Agents catch each other's errors that self-review misses
- Diversity of responses provides multiple perspectives on the same problem
- Transparent: the debate transcript shows how the final answer was reached
- Scalable: more agents can be added for higher-stakes decisions
- Works even with identical model instances (no need for different architectures)

**Weaknesses:**
- Expensive: N agents x M rounds = N*M model calls
- Agents can converge on a shared wrong answer (groupthink analog)
- Majority voting can suppress correct minority opinions
- Debate may not converge -- agents can get stuck in loops
- Requires careful prompt engineering to encourage genuine engagement rather than capitulation
- Token cost increases linearly with number of agents and rounds

**Domain:** AI/LLM, Factual Accuracy, Reasoning, Multi-Agent Systems

**Applicability to LLM Workflows:**
Multi-Agent Debate maps to **multi-critic review** in Jerry:
- **Multiple critic agents** = Different adversarial strategies applied by different agents
- **Debate rounds** = Creator-critic iterations where the creator sees all critics' feedback
- **Convergence** = When all critics' quality scores exceed threshold
- **Diversity** = Using different adversarial strategies (Red Team, Devil's Advocate, Steelman) rather than different model instances

**Key Insight for Jerry:** The multi-agent debate pattern validates Jerry's use of multiple adversarial strategies per phase. A single Red Team review may miss what a Steelman review catches, and vice versa. The combination is more robust than any single strategy.

---

### Strategy 9: Chain-of-Verification (CoVe)

**Name:** Chain-of-Verification (CoVe)

**Origin/Author:** Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Celikyilmaz, and Jason Weston. Meta AI. Published 2023.

**Citation:**
- Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., and Weston, J. "Chain-of-Verification Reduces Hallucination in Large Language Models." ArXiv preprint arXiv:2309.11495, 2023.

**Description:** Chain-of-Verification (CoVe) is a method to reduce hallucinations in LLM outputs by generating explicit verification questions about factual claims in the output, answering those questions independently (to avoid bias from the original context), and then using the verified answers to revise the original output. The adversarial mechanism is self-directed: the model adversarially interrogates its own factual claims through targeted verification questions.

**Mechanism (Step-by-Step):**

1. **Generate Baseline Response**: The model generates an initial response to the query.
2. **Plan Verification Questions**: The model is prompted to generate a set of verification questions targeting the factual claims in its response. Example: If the response states "Python was created by Guido van Rossum in 1991 at CWI in the Netherlands," verification questions would be: "Who created Python?", "When was Python first released?", "Where was Python created?"
3. **Execute Verifications Independently**: Each verification question is answered independently, without the original response in context. This isolation prevents the model from simply confirming its own claims (a key insight of CoVe -- independent verification avoids confirmation bias).
4. **Generate Final Verified Response**: The model is given the original response alongside the verification question-answer pairs. It is prompted to revise the original response, correcting any claims that the verification step contradicted.

**CoVe Variants:**
| Variant | Description |
|---------|-------------|
| Joint | Verification questions answered together (simplest but least effective) |
| Two-Step | Questions planned first, then answered separately |
| Factored | Each question answered in complete isolation (most effective) |
| Factor + Revise | Factored verification plus explicit revision step |

**Strengths:**
- Specifically targets hallucinations (the most critical LLM failure mode)
- Independent verification avoids confirmation bias
- Verification questions are interpretable and auditable
- Adaptable to different domains (adjust verification question generation)
- Empirically shown to reduce hallucinations significantly on long-form generation tasks

**Weaknesses:**
- Only addresses factual claims (not reasoning quality, style, or normative alignment)
- Verification is only as good as the model's knowledge (cannot verify claims about topics outside training data)
- Multiple verification calls increase latency and cost
- Does not help with claims that are plausible but wrong (model may "verify" the same hallucination)
- Requires factual claims to be extractable from the response (harder for abstract/opinion content)

**Domain:** AI/LLM, Factual Accuracy, Hallucination Reduction

**Applicability to LLM Workflows:**
CoVe maps to a **factual verification critic mode** in Jerry:
- **Verification question generation** = Critic agent generates targeted verification questions for factual claims in creator output
- **Independent verification** = Separate verification calls without original context (prevents confirmation bias)
- **Revision** = Creator revises output based on verified facts

**Key Insight for Jerry:** CoVe provides a template for how to implement the "fact-checking" aspect of adversarial review. For Jerry's research artifacts (like this document), a CoVe-style critic could generate verification questions about cited authors, publication dates, and claimed empirical results, then independently verify each claim.

---

### Strategy 10: CRITIC Framework

**Name:** CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing

**Origin/Author:** Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan, and Weizhu Chen. Tsinghua University, Microsoft Research. Published 2023.

**Citation:**
- Gou, Z., Shao, Z., Gong, Y., Shen, Y., Yang, Y., Duan, N., and Chen, W. "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing." ArXiv preprint arXiv:2305.11738, 2023.

**Description:** CRITIC extends LLM self-critique by incorporating external tools (search engines, code interpreters, calculators) into the critique step. Rather than relying solely on the model's internal knowledge to critique its output, CRITIC allows the model to use tools to verify claims, test code, and check calculations. This addresses a fundamental limitation of self-critique methods like Self-Refine: the model's inability to catch errors that stem from gaps in its own knowledge.

**Mechanism (Step-by-Step):**

1. **Generate Initial Output**: The model generates a response to the input task.
2. **Critique with Tool Use**: The model is prompted to critique its output, with access to tools:
   - **For factual claims**: Use a search engine to verify
   - **For code**: Use a code interpreter to execute and test
   - **For math**: Use a calculator to verify computations
   - **For references**: Use a search engine to verify citations exist
   The critique prompt: "Verify the following output. Use available tools to check factual claims, test code, and verify calculations. List any issues found."
3. **Tool-Augmented Feedback**: The model synthesizes tool outputs into actionable feedback: "The code has a bug on line 7 (verified by execution). The claim about X is incorrect (search result shows Y instead)."
4. **Revision**: The model revises the output based on tool-verified feedback.
5. **Iterate**: Repeat until no tool-verifiable issues are found or iteration limit is reached.

**Strengths:**
- Addresses the fundamental limitation of self-critique (model's own knowledge gaps)
- Tool verification provides ground-truth checking
- Applicable to diverse output types (code, factual claims, math)
- Interpretable: tool outputs serve as evidence for critique
- Combines the scalability of self-critique with the reliability of external verification

**Weaknesses:**
- Requires tool infrastructure (search APIs, code interpreters)
- Tool reliability varies (search engines can return wrong results too)
- Slower than pure self-critique due to tool call latency
- Not all claims are tool-verifiable (subjective judgments, design decisions)
- Model must correctly identify which claims to verify and which tools to use
- Tool cost adds to per-query expense

**Domain:** AI/LLM, Code Generation, Factual Accuracy, Mathematical Reasoning

**Applicability to LLM Workflows:**
CRITIC maps to **tool-augmented critic agents** in Jerry:
- **Tool access** = Critic agents can invoke linters, test runners, search, or validators
- **Evidence-based critique** = Critique backed by tool outputs, not just model judgment
- **Verification pipeline** = After critic identifies concerns, tools verify them before requiring creator revision

**Key Insight for Jerry:** CRITIC validates the architecture pattern where critic agents are not purely LLM-based but can invoke tools. For Jerry, relevant tools include: file validators, test runners, markdown linters, link checkers, and consistency validators. A critic agent that can run `uv run pytest tests/` or validate citation URLs is strictly more capable than one that only reasons about the code.

---

### Strategy 11: Reflexion

**Name:** Reflexion: Language Agents with Verbal Reinforcement Learning

**Origin/Author:** Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Northeastern University, MIT, Princeton University. Published 2023.

**Citation:**
- Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and Yao, S. "Reflexion: Language Agents with Verbal Reinforcement Learning." *Advances in Neural Information Processing Systems 36 (NeurIPS 2023)*. ArXiv preprint arXiv:2303.11366, 2023.

**Description:** Reflexion is a framework where an LLM agent learns from its failures through verbal self-reflection rather than weight updates. After attempting a task and receiving feedback (from the environment, tools, or self-evaluation), the agent generates a natural language reflection on what went wrong and how to improve. This reflection is stored in memory and provided as context for subsequent attempts. Reflexion creates an adversarial loop where the agent's past failures serve as an adversarial signal that drives improvement.

**Mechanism (Step-by-Step):**

1. **Attempt**: The agent attempts the task, generating an output or executing a plan.
2. **Evaluation**: The output is evaluated against success criteria. Evaluation can come from:
   - Environment feedback (test results, execution outcomes)
   - Self-evaluation (model judges its own output)
   - External evaluation (human feedback, tool-based verification)
3. **Reflection**: If the attempt fails, the agent generates a verbal reflection:
   - What specifically went wrong?
   - Why did it go wrong? (root cause)
   - What should be done differently next time? (corrective action)
   Example reflection: "The function failed test case 3 because it did not handle empty lists. Next time, add an explicit check for empty input at the beginning of the function."
4. **Memory Storage**: The reflection is stored in the agent's episodic memory (persistent across attempts).
5. **Retry with Reflection**: The agent retries the task with the reflection in context. The reflection serves as learned experience that guides the next attempt.
6. **Iterate**: Steps 1-5 repeat until success or max attempts reached.

**Empirical Results (from Shinn et al. 2023):**
- On HumanEval (code generation): Reflexion improved pass rate from 80.1% to 91.0%
- On AlfWorld (decision making): Reflexion achieved 97% success rate vs. 75% for baselines
- On HotpotQA (multi-hop QA): Significant improvement in reasoning accuracy
- Reflections were shown to be semantically meaningful and targeted to actual failure causes

**Strengths:**
- Learns from failure without weight updates (inference-time learning)
- Produces interpretable reflections that explain what went wrong
- Accumulates experience across attempts (episodic memory)
- Works across diverse task types (code, reasoning, decision-making)
- The reflection mechanism mimics human metacognition
- Reflections can be shared across similar tasks (transfer learning analog)

**Weaknesses:**
- Requires clear success/failure signals (hard to apply when quality is ambiguous)
- Reflection quality depends on model's diagnostic ability
- Accumulated reflections can consume context window
- May not converge if the task is beyond model capability
- Reflections can be superficial if not prompted carefully
- Performance plateaus after 3-5 attempts for most tasks

**Domain:** AI/LLM, Reinforcement Learning, Code Generation, Reasoning

**Applicability to LLM Workflows:**
Reflexion maps to **experience-based adversarial review** in Jerry:
- **Reflection storage** = Persisting review lessons learned to `.jerry/data/` for future sessions
- **Failure-driven improvement** = When a critic identifies issues, the creator generates a reflection on why the issue occurred and how to avoid it
- **Cross-session learning** = Reflections from past quality failures inform future reviews
- **Episodic memory** = Jerry's filesystem-as-memory architecture (CLAUDE.md core principle) naturally supports storing reflections

**Key Insight for Jerry:** Reflexion validates Jerry's "filesystem as infinite memory" approach. By persisting critic feedback and creator reflections as artifacts, Jerry can implement experience-based improvement across sessions. A critic agent reviewing a design document can reference reflections from past design review failures.

---

### Strategy 12: LLM-as-Judge

**Name:** LLM-as-Judge / Judging LLM-as-a-Judge

**Origin/Author:** Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. UC Berkeley, Stanford, CMU, UCSD. Published 2023. The broader pattern of using LLMs as evaluators has been independently explored by multiple research groups.

**Citation:**
- Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., and Stoica, I. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." *Advances in Neural Information Processing Systems 36 (NeurIPS 2023)*. ArXiv preprint arXiv:2306.05685, 2023.
- Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., and Zhu, C. "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment." ArXiv preprint arXiv:2303.16634, 2023.
- Kim, S., Shin, J., Cho, Y., Jang, J., Longpre, S., Lee, H., Yun, S., Shin, S., Kim, S., Thorne, J., and Seo, M. "Prometheus: Inducing Fine-Grained Evaluation Capability in Language Models." ArXiv preprint arXiv:2310.08491, 2023.

**Description:** LLM-as-Judge is the practice of using a large language model to evaluate the quality of outputs (from other LLMs or from human-written text) using structured rubrics, scoring criteria, and evaluation protocols. The judge model receives the output to evaluate along with explicit scoring guidelines, reference answers (optionally), and is asked to provide both a numerical score and a natural language justification. This pattern creates a standardized, scalable adversarial evaluation mechanism that can be applied consistently across large volumes of outputs.

**Mechanism (Step-by-Step):**

1. **Define Evaluation Rubric**: Create explicit scoring criteria with concrete descriptions for each score level. Example:
   - Score 5: Comprehensive, accurate, well-structured, all requirements met
   - Score 4: Mostly complete with minor omissions
   - Score 3: Adequate but significant gaps
   - Score 2: Partially addresses the question with major issues
   - Score 1: Fails to address the question or contains critical errors
2. **Configure Judge**: Provide the judge model with: the rubric, the task description, the output to evaluate, and (optionally) a reference answer or evaluation context.
3. **Generate Evaluation**: The judge produces:
   - A numerical score (e.g., 1-5 or 0.0-1.0)
   - A natural language justification explaining the score
   - Specific citations from the evaluated output that support the assessment
4. **Multi-Dimensional Scoring** (optional): Score multiple dimensions independently: accuracy, completeness, coherence, relevance, etc.
5. **Pairwise Comparison** (variant): Instead of absolute scoring, present two outputs and ask the judge to determine which is better and why. This often produces more reliable results than absolute scoring.
6. **Calibration**: Use reference examples (outputs with known quality) to calibrate the judge's scoring.

**Judge Variants:**
| Variant | Mechanism | Best For |
|---------|-----------|----------|
| Single-Point Scoring | Score one output against rubric | Threshold-based quality gates |
| Pairwise Comparison | Compare two outputs | Selecting between alternatives |
| Reference-Guided | Score against a reference answer | Tasks with known correct answers |
| Multi-Aspect | Score multiple dimensions | Complex outputs requiring nuanced evaluation |

**Strengths:**
- Highly scalable (can evaluate thousands of outputs automatically)
- Consistent application of criteria (no reviewer fatigue)
- Explicit rubrics make evaluation transparent and reproducible
- Natural language justifications are interpretable
- Can be calibrated with reference examples
- Strong correlation with human judgments for many tasks (Zheng et al. 2023 showed ~80% agreement with human preferences)

**Weaknesses:**
- Position bias: judges tend to favor the first response in pairwise comparisons
- Verbosity bias: judges tend to favor longer responses
- Self-enhancement bias: models rate their own outputs higher than other models' outputs
- Rubric quality is critical -- poor rubrics produce poor evaluations
- Cannot reliably evaluate claims outside the judge model's knowledge
- May miss subtle quality issues that experienced human reviewers would catch
- Calibration can be difficult for novel or domain-specific tasks

**Domain:** AI/LLM, NLP Evaluation, Benchmark Design

**Applicability to LLM Workflows:**
LLM-as-Judge maps directly to Jerry's **quality scoring mechanism**:
- **Rubric** = The quality score criteria (>= 0.92 threshold) with defined score levels
- **Multi-dimensional scoring** = Separate scores for accuracy, completeness, citation quality, etc.
- **Natural language justification** = Critic agent explains its quality score
- **Pairwise comparison** = When the creator produces a revision, judge compares revision to original
- **Calibration** = Reference examples of high-quality research artifacts

**Key Insight for Jerry:** The 0.92 quality threshold used in Jerry's orchestration plan should be implemented as an explicit rubric with concrete descriptions of what constitutes 0.92 vs. 0.85 vs. 0.95 quality. Without this rubric, the score is subjective and inconsistent. LLM-as-Judge research provides the methodology for making quality scores rigorous.

---

## L1: Strategy Catalog -- QA Adversarial Patterns

### Strategy 13: Mutation Testing

**Name:** Mutation Testing / Mutation Analysis

**Origin/Author:** Richard Lipton, 1971 (doctoral dissertation, Carnegie Mellon University). Further developed by DeMillo, Lipton, and Sayward in their landmark 1978 paper. Modern implementations include PIT (Java), mutmut (Python), and Stryker (JavaScript).

**Citation:**
- DeMillo, R. A., Lipton, R. J., and Sayward, F. G. "Hints on Test Data Selection: Help for the Practicing Programmer." *Computer*, 11(4), 34-41, 1978. DOI: 10.1109/C-M.1978.218136
- Jia, Y. and Harman, M. "An Analysis and Survey of the Development of Mutation Testing." *IEEE Transactions on Software Engineering*, 37(5), 649-678, 2011. DOI: 10.1109/TSE.2010.62
- Papadakis, M., Kintis, M., Zhang, J., Jia, Y., Le Traon, Y., and Harman, M. "Mutation Testing Advances: An Analysis and Survey." *Advances in Computers*, vol. 112, pp. 275-378. Elsevier, 2019. DOI: 10.1016/bs.adcom.2018.03.015

**Description:** Mutation testing is a technique for evaluating the quality of a test suite (or review process) by deliberately injecting small, syntactically valid faults ("mutations") into the artifact under test. If the test suite (or review process) detects the injected fault, the mutant is "killed." If the fault goes undetected, the mutant "survives," indicating a gap in the testing/review coverage. The mutation score (killed mutants / total mutants) quantifies the effectiveness of the detection mechanism.

**Mechanism (Step-by-Step):**

1. **Define Mutation Operators**: Specify the types of changes to inject. For code: change `>` to `>=`, remove a condition, replace a constant, swap operands. For documents: introduce a factual error, weaken an argument, insert a logical fallacy, remove a critical requirement.
2. **Generate Mutants**: Apply mutation operators to create variants of the original artifact, each containing exactly one injected fault.
3. **Run Detection Process**: Submit each mutant to the test suite or review process. The reviewer/test does not know which specific mutation was applied.
4. **Score Results**:
   - **Killed**: The mutation was detected -- the review/test is effective for this type of fault
   - **Survived**: The mutation was not detected -- the review/test has a gap
   - **Equivalent**: The mutation does not actually change behavior (false positive in mutation)
5. **Analyze Survivors**: Surviving mutants identify specific categories of faults that the review process misses. These inform review process improvement.
6. **Improve Detection**: Update the review process, test suite, or checklist to catch the types of faults that survived.

**Strengths:**
- Provides a quantitative measure of review/test effectiveness
- Identifies specific detection gaps (not just "the review is weak" but "the review misses off-by-one errors")
- Well-established theoretical foundation (coupling hypothesis, competent programmer hypothesis)
- Applicable beyond code -- to any artifact where faults can be defined and injected
- Creates a feedback loop for continuous improvement of the review process

**Weaknesses:**
- Computationally expensive (many mutants per artifact)
- Equivalent mutant problem (some mutations don't actually change behavior)
- Mutation operators must be carefully designed for each artifact type
- For non-code artifacts, defining "mutation operators" is subjective
- Does not find real defects -- it tests the reviewer, not the artifact
- Can be gamed (reviewers may learn to spot mutations rather than genuinely improving)

**Domain:** Software Engineering, Quality Assurance, Testing

**Applicability to LLM Workflows:**
Mutation testing maps to **critic calibration** in Jerry:
- **Mutant generation** = Create deliberately flawed variants of artifacts
- **Critic evaluation** = Test whether the critic agent detects the injected faults
- **Mutation score** = Quantitative measure of critic agent effectiveness
- **Gap analysis** = Identify which types of flaws the critic consistently misses
- **Improvement** = Update critic prompts, checklists, or strategies based on gaps

**Key Insight for Jerry:** Mutation testing provides a methodology for **validating that critic agents actually work**. Before trusting a critic's 0.92 quality score, inject known defects and verify the critic catches them. A critic that gives 0.95 to a mutant with an injected logical fallacy is not a reliable critic.

---

### Strategy 14: Exploratory Testing Heuristics (Session-Based Test Management)

**Name:** Exploratory Testing / Session-Based Test Management (SBTM)

**Origin/Author:** Cem Kaner coined the term "exploratory testing" in 1983. James Bach and Jonathan Bach developed Session-Based Test Management (SBTM) in 2000 as a structured approach to managing exploratory testing. Elisabeth Hendrickson further developed heuristic-based approaches.

**Citation:**
- Kaner, C., Bach, J., and Pettichord, B. *Lessons Learned in Software Testing: A Context-Driven Approach*. Wiley, 2001. ISBN: 978-0471081128.
- Bach, J. "Session-Based Test Management." *Software Testing and Quality Engineering (STQE) Magazine*, November/December 2000.
- Hendrickson, E. *Explore It!: Reduce Risk and Increase Confidence with Exploratory Testing*. Pragmatic Bookshelf, 2013. ISBN: 978-1937785024.
- Whittaker, J. A. *Exploratory Software Testing: Tips, Tricks, Tours, and Techniques to Guide Test Design*. Addison-Wesley, 2009. ISBN: 978-0321636416.

**Description:** Exploratory testing is a style of software testing where the tester simultaneously designs, executes, and evaluates tests in real time, using heuristic-based exploration rather than predetermined test scripts. Session-Based Test Management (SBTM) provides structure to exploratory testing by organizing it into time-boxed sessions with defined charters, debriefing protocols, and measurable outcomes. The adversarial element is the tester's mindset: they are actively trying to break the system, find edge cases, and discover unexpected behaviors -- not confirming that the system works.

**Mechanism (Step-by-Step):**

1. **Charter Definition**: Define a test charter: a brief statement of the mission for the testing session. Example: "Explore the payment processing module, focusing on error handling for declined transactions, using boundary value inputs and adversarial sequences."
2. **Time-Boxing**: Set a fixed duration for the session (typically 60-120 minutes). This prevents both under-exploration (too short) and diminishing returns (too long).
3. **Exploration**: The tester explores the system guided by the charter and heuristics:
   - **SFDPOT Heuristic** (Bach): Structure, Function, Data, Platform, Operations, Time
   - **Touring Heuristics** (Whittaker): Guidebook tour, Money tour, Landmark tour, Intellectual tour, FedEx tour, Garbage collector's tour, Antisocial tour, etc.
   - The tester follows intuition, adjusts direction based on findings, and drills deeper when anomalies are discovered.
4. **Note-Taking**: The tester records: actions taken, observations made, bugs found, areas not explored, and new test ideas generated.
5. **Debriefing**: After the session, the tester debriefs with the team: what was tested, what was found, what was not tested, and what should be explored next. The debrief is structured using the session sheet.
6. **Session Sheet**: Documented output includes:
   - Charter (mission)
   - Areas covered and areas not covered
   - Bugs found (with severity)
   - Issues/questions raised
   - Percentage breakdown: test design / test execution / bug investigation / session setup

**Key Heuristics (Whittaker's Tours):**
| Tour | Purpose | Adversarial Angle |
|------|---------|-------------------|
| Antisocial Tour | Try to do everything wrong | Maximum adversarial input |
| Garbage Collector's Tour | Look in places nobody else looks | Find hidden assumptions |
| Saboteur Tour | Set up conditions for failure | Environmental adversarial testing |
| Intellectual Tour | Find the hardest problems | Complexity-based adversarial testing |
| Skeptic's Tour | Don't believe anything works | Trust-nothing review mindset |

**Strengths:**
- Discovers defects that scripted testing misses (especially usability, edge cases, integration issues)
- Adaptable in real time (follows the most promising leads)
- Leverages human creativity and intuition
- Structured enough (via SBTM) to be managed and measured
- Heuristics provide systematic coverage without rigid scripts
- Finds "unknown unknowns" that no predefined test case would cover

**Weaknesses:**
- Results depend heavily on tester skill and experience
- Harder to reproduce (exploratory paths are unique)
- Coverage is difficult to measure objectively
- Not a replacement for systematic testing (complements, not replaces)
- Session notes can be inconsistent without disciplined practice
- Some managers distrust "unscripted" testing

**Domain:** Software Testing, Quality Assurance

**Applicability to LLM Workflows:**
Exploratory testing maps to **heuristic-guided adversarial review** in Jerry:
- **Charter** = Review charter that directs the critic to specific areas/concerns
- **Touring heuristics** = Adversarial review heuristics (Antisocial Tour = Red Team; Skeptic's Tour = Devil's Advocate; Intellectual Tour = ATAM-style architecture probing)
- **Time-boxing** = Iteration limits (Jerry's 3-iteration maximum)
- **Session debrief** = Critic agent summary with coverage areas and unexamined areas
- **Adaptive exploration** = Critic follows up on initial findings rather than following a fixed checklist

**Key Insight for Jerry:** Exploratory testing heuristics provide a template for giving critic agents **structured but flexible review guidance**. Rather than a rigid checklist, a critic could be guided by "tours" that direct attention to specific aspects of the artifact while preserving the ability to follow unexpected leads.

---

## L1: Comparative Analysis

### Cross-Strategy Comparison Matrix

| Strategy | Type | Cost (1-5) | Formality (1-5) | Defect Detection | Best For | Self-Applicable |
|----------|------|-----------|-----------------|-----------------|----------|----------------|
| Fagan Inspection | SE | 5 | 5 | Very High (60-90%) | Detailed artifact review | No (requires multiple roles) |
| Google Code Review | SE | 2 | 3 | Moderate-High | Continuous quality | Yes (async review) |
| ATAM | SE/Arch | 4 | 4 | High (for architecture) | Architecture evaluation | No (requires stakeholders) |
| Pair Programming | SE | 3 | 1 | Moderate | Real-time collaboration | Yes (interleaved review) |
| Design Critique | Design | 2 | 2 | Moderate | Creative/design artifacts | Yes (structured feedback) |
| Constitutional AI | LLM | 2 | 3 | High (normative) | Alignment/safety | Yes (self-critique) |
| Self-Refine | LLM | 1 | 1 | Moderate | General improvement | Yes (single agent) |
| Multi-Agent Debate | LLM | 4 | 3 | High (factual) | Factual accuracy | N/A (requires multiple agents) |
| Chain-of-Verification | LLM | 3 | 3 | High (factual) | Hallucination reduction | Yes (self-verification) |
| CRITIC | LLM | 3 | 2 | High (verifiable claims) | Tool-verifiable outputs | Yes (tool-augmented) |
| Reflexion | LLM | 3 | 2 | Moderate-High | Learning from failure | Yes (episodic memory) |
| LLM-as-Judge | LLM | 2 | 4 | Varies by rubric | Standardized evaluation | No (evaluates, not critiques) |
| Mutation Testing | QA | 4 | 4 | Meta (tests the tester) | Validating review quality | No (tests the process) |
| Exploratory Testing | QA | 2 | 2 | Moderate-High | Unknown unknowns | Yes (heuristic-guided) |

### Cost Scale
- 1 = Minimal (single model call, no tools)
- 5 = Very expensive (multi-day, multi-person, specialized infrastructure)

### Formality Scale
- 1 = Informal (conversational, flexible)
- 5 = Highly formal (defined roles, entry/exit criteria, measured outcomes)

### Strategy Complementarity Map

```
FACTUAL ACCURACY           NORMATIVE ALIGNMENT        STRUCTURAL QUALITY
─────────────────          ──────────────────         ─────────────────
Chain-of-Verification      Constitutional AI          Fagan Inspection
CRITIC Framework           Design Critique            Google Code Review
Multi-Agent Debate         LLM-as-Judge               ATAM

PROCESS IMPROVEMENT        CREATIVITY/EXPLORATION     LEARNING
───────────────────        ──────────────────────     ────────
Mutation Testing           Exploratory Testing        Reflexion
Pair Programming           Design Critique            Self-Refine
```

---

## L2: Architectural Implications for Jerry

### Integration Architecture

The 14 strategies researched here suggest a **layered adversarial review architecture** for Jerry:

#### Layer 1: Pre-Critic Self-Check (Low Cost)
- **Self-Refine**: Creator agent applies one round of self-feedback before submitting to critic
- **Purpose**: Catch obvious issues early, reduce critic workload
- **Invocation**: Automatic (always applied)

#### Layer 2: Standard Critic Review (Default)
- **Google Code Review model**: Lightweight, continuous, async critic evaluation
- **Constitutional AI**: Critique against defined principles/checklist
- **LLM-as-Judge**: Standardized scoring with rubric
- **Purpose**: Core quality gate
- **Invocation**: Every creator-critic cycle (Jerry's default)

#### Layer 3: Deep Adversarial Review (Escalation)
- **Multi-Agent Debate**: Multiple critics from different perspectives
- **Chain-of-Verification**: Factual claim verification
- **CRITIC**: Tool-augmented verification
- **ATAM**: Architecture-specific scenario-based evaluation
- **Fagan Inspection**: Full formal review with defined roles
- **Purpose**: High-stakes or low-scoring artifacts
- **Invocation**: When Layer 2 quality score < threshold or artifact is critical

#### Layer 4: Meta-Review (Calibration)
- **Mutation Testing**: Validate that critic agents are effective
- **Reflexion**: Learn from past review failures
- **Purpose**: Improve the review process itself
- **Invocation**: Periodic calibration, not per-artifact

### Mapping to Jerry's Existing Architecture

| Jerry Component | Strategy Layer | Strategies Applied |
|----------------|---------------|-------------------|
| Creator Agent | Layer 1 | Self-Refine (pre-submission self-check) |
| Critic Agent (ps-critic) | Layer 2 | Constitutional AI, LLM-as-Judge, Design Critique |
| Orchestrator (sync barriers) | Layer 2-3 | Quality score thresholds trigger escalation |
| Multi-Critic (adversarial modes) | Layer 3 | Multi-Agent Debate, ATAM, Fagan roles |
| Episodic Memory (.jerry/data/) | Layer 4 | Reflexion, Mutation Testing results |

### Implementation Recommendations

1. **Define Constitutions**: For each adversarial strategy, define an explicit "constitution" (set of evaluable principles). This converts Jerry's current vague "quality >= 0.92" into a concrete, auditable rubric.

2. **Implement Self-Refine as Default**: Every creator agent should apply one round of Self-Refine before submitting to the critic. This is low-cost and empirically improves baseline quality.

3. **Use LLM-as-Judge for Scoring**: Implement the quality score (0.0-1.0) using a formal LLM-as-Judge rubric with concrete descriptions for each score level. Eliminate subjective scoring.

4. **Add CoVe for Research Artifacts**: For research documents (like this one), implement Chain-of-Verification as a standard critic mode that generates verification questions for factual claims and citations.

5. **Implement Mutation Testing for Critic Validation**: Before trusting critic agents, validate them by injecting known defects and measuring detection rates. Track mutation scores over time.

6. **Use Exploratory Testing Heuristics for Flexible Review**: Supplement rigid checklists with "touring" heuristics that guide critics to explore artifacts in structured but flexible ways.

7. **Implement Reflexion for Cross-Session Learning**: Persist critic feedback and creator reflections as `.jerry/data/` artifacts. Use reflections from past failures to inform future reviews.

---

## References

### Software Engineering Sources

1. Fagan, M. E. "Design and Code Inspections to Reduce Errors in Program Development." *IBM Systems Journal*, 15(3), 182-211, 1976. DOI: 10.1147/sj.153.0182
2. Fagan, M. E. "Advances in Software Inspections." *IEEE Transactions on Software Engineering*, SE-12(7), 744-751, 1986. DOI: 10.1109/TSE.1986.6312976
3. IEEE 1028-2008. "IEEE Standard for Software Reviews and Audits." Institute of Electrical and Electronics Engineers, 2008.
4. NASA NPR 7150.2. "NASA Software Engineering Requirements." National Aeronautics and Space Administration.
5. Sadowski, C., Soderberg, E., Church, L., Sipko, M., and Bacchelli, A. "Modern Code Review: A Case Study at Google." *ICSE-SEIP '18*, pp. 181-190. ACM, 2018. DOI: 10.1145/3183519.3183525
6. Rigby, P. C. and Bird, C. "Convergent Contemporary Software Peer Review Practices." *ESEC/FSE '13*, pp. 202-212. ACM, 2013. DOI: 10.1145/2491411.2491444
7. Bacchelli, A. and Bird, C. "Expectations, Outcomes, and Challenges of Modern Code Review." *ICSE 2013*, pp. 712-721. IEEE, 2013. DOI: 10.1109/ICSE.2013.6606617
8. Kazman, R., Klein, M., and Clements, P. "ATAM: Method for Architecture Evaluation." Technical Report CMU/SEI-2000-TR-004. SEI, Carnegie Mellon University, 2000.
9. Clements, P., Kazman, R., and Klein, M. *Evaluating Software Architectures: Methods and Case Studies*. Addison-Wesley, 2002. ISBN: 978-0201704822.
10. Bass, L., Clements, P., and Kazman, R. *Software Architecture in Practice*, 4th Edition. Addison-Wesley, 2021. ISBN: 978-0136886099.
11. Beck, K. *Extreme Programming Explained: Embrace Change*. Addison-Wesley, 1999. ISBN: 978-0201616415.
12. Williams, L. and Kessler, R. *Pair Programming Illuminated*. Addison-Wesley, 2003. ISBN: 978-0201745764.
13. Williams, L., Kessler, R. R., Cunningham, W., and Jeffries, R. "Strengthening the Case for Pair Programming." *IEEE Software*, 17(4), 19-25, 2000. DOI: 10.1109/52.854064

### Design and Product Review Sources

14. Kelley, T. and Kelley, D. *Creative Confidence: Unleashing the Creative Potential Within Us All*. Crown Business, 2013. ISBN: 978-0385349369.
15. Lerman, L. and Borstel, J. *Liz Lerman's Critical Response Process*. Liz Lerman Dance Exchange, 2003. ISBN: 978-0972738507.
16. Hasso Plattner Institute of Design at Stanford. "An Introduction to Design Thinking: Process Guide." Stanford University, 2010.
17. Schon, D. A. *The Reflective Practitioner: How Professionals Think in Action*. Basic Books, 1983. ISBN: 978-0465068784.

### LLM-Specific Sources

18. Bai, Y. et al. "Constitutional AI: Harmlessness from AI Feedback." ArXiv preprint arXiv:2212.08073, 2022.
19. Madaan, A. et al. "Self-Refine: Iterative Refinement with Self-Feedback." *NeurIPS 2023*. ArXiv preprint arXiv:2303.17651, 2023.
20. Du, Y. et al. "Improving Factuality and Reasoning in Language Models through Multiagent Debate." *ICML 2023*. ArXiv preprint arXiv:2305.14325, 2023.
21. Liang, T. et al. "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate." ArXiv preprint arXiv:2305.19118, 2023.
22. Chan, C. et al. "ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate." ArXiv preprint arXiv:2308.07201, 2023.
23. Dhuliawala, S. et al. "Chain-of-Verification Reduces Hallucination in Large Language Models." ArXiv preprint arXiv:2309.11495, 2023.
24. Gou, Z. et al. "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing." ArXiv preprint arXiv:2305.11738, 2023.
25. Shinn, N. et al. "Reflexion: Language Agents with Verbal Reinforcement Learning." *NeurIPS 2023*. ArXiv preprint arXiv:2303.11366, 2023.
26. Zheng, L. et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." *NeurIPS 2023*. ArXiv preprint arXiv:2306.05685, 2023.
27. Liu, Y. et al. "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment." ArXiv preprint arXiv:2303.16634, 2023.
28. Kim, S. et al. "Prometheus: Inducing Fine-Grained Evaluation Capability in Language Models." ArXiv preprint arXiv:2310.08491, 2023.

### Quality Assurance Sources

29. DeMillo, R. A., Lipton, R. J., and Sayward, F. G. "Hints on Test Data Selection: Help for the Practicing Programmer." *Computer*, 11(4), 34-41, 1978. DOI: 10.1109/C-M.1978.218136
30. Jia, Y. and Harman, M. "An Analysis and Survey of the Development of Mutation Testing." *IEEE Transactions on Software Engineering*, 37(5), 649-678, 2011. DOI: 10.1109/TSE.2010.62
31. Papadakis, M. et al. "Mutation Testing Advances: An Analysis and Survey." *Advances in Computers*, vol. 112, pp. 275-378. Elsevier, 2019. DOI: 10.1016/bs.adcom.2018.03.015
32. Kaner, C., Bach, J., and Pettichord, B. *Lessons Learned in Software Testing: A Context-Driven Approach*. Wiley, 2001. ISBN: 978-0471081128.
33. Bach, J. "Session-Based Test Management." *STQE Magazine*, November/December 2000.
34. Hendrickson, E. *Explore It!: Reduce Risk and Increase Confidence with Exploratory Testing*. Pragmatic Bookshelf, 2013. ISBN: 978-1937785024.
35. Whittaker, J. A. *Exploratory Software Testing: Tips, Tricks, Tours, and Techniques to Guide Test Design*. Addison-Wesley, 2009. ISBN: 978-0321636416.

---

## Disclaimer

This research was conducted by the ps-researcher agent (v2.2.0) using training knowledge through May 2025. WebSearch and WebFetch tools were unavailable during this session.

**Confidence Assessment:**
- **HIGH** confidence: Strategies 1-5 (SE patterns -- well-established, widely published, stable over time)
- **HIGH** confidence: Strategies 6-12 (LLM patterns -- published 2022-2024, high-profile papers, within training data)
- **HIGH** confidence: Strategies 13-14 (QA patterns -- well-established, classic references)
- **MEDIUM** confidence: Specific empirical results cited from papers (may be approximate; verify against original publications)

**Verification Recommended:**
- All DOIs should be resolved and verified
- ArXiv paper IDs should be confirmed
- ISBN numbers should be verified against library catalogs
- Specific empirical results (percentages, benchmarks) should be cross-referenced with original papers

---

*Document ID: FEAT-004:EN-301-TASK-002*
*PS ID: EN-301*
*Entry ID: TASK-002*
*Agent: ps-researcher v2.2.0*
*Created: 2026-02-12*
*Status: Complete (pending quality review)*

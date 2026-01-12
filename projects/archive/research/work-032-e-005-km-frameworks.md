# Knowledge Management and Problem-Solving Frameworks

**Research ID:** WORK-032-E-005
**Topic:** Knowledge Solving Frameworks and Methodologies
**Date:** 2026-01-08
**Status:** Complete

---

## L0: Executive Summary

This research catalogues 16 knowledge management and problem-solving frameworks spanning 80+ years of organizational learning theory, from classic knowledge management (1960s-1990s) through modern AI-augmented approaches (2020s). The analysis reveals four distinct framework categories serving complementary purposes in the knowledge work lifecycle.

**Key Findings:**

1. **Classic KM frameworks** (SECI, Wiig, Boisot, Cynefin) excel at understanding knowledge types, flows, and contexts but lack operational specificity
2. **Problem-solving frameworks** (TRIZ, Design Thinking, Systems Thinking, RCA) provide structured approaches to different problem types but require context awareness
3. **Decision frameworks** (OODA, Kepner-Tregoe, PDCA, A3) offer systematic decision-making processes with varying speed/rigor trade-offs
4. **AI-era frameworks** (RAG, GraphRAG, Chain-of-Thought, ReAct) enhance LLM capabilities but introduce new challenges around grounding and verification

**Strategic Recommendation for Jerry:**

Jerry should implement a **layered framework stack** that combines:
- **Cynefin** for problem classification (complexity assessment)
- **SECI Model** for knowledge creation and flow (tacit ↔ explicit conversion)
- **ReAct + GraphRAG** for AI-augmented problem-solving (reasoning + knowledge retrieval)
- **A3 Thinking** for documentation and continuous learning

This combination leverages Jerry's filesystem-as-memory architecture while maintaining human oversight and systematic learning capture.

---

## L1: Framework Catalog with Decision Guide

### Category 1: Classic Knowledge Management Frameworks

These frameworks explain how knowledge is created, organized, stored, and transferred within organizations.

#### 1.1 SECI Model (Nonaka & Takeuchi, 1995)

**Origin:** Ikujiro Nonaka and Hirotaka Takeuchi, "The Knowledge-Creating Company" (1995)

**Core Principles:**
- Knowledge creation through continuous dialogue between tacit and explicit knowledge
- Four modes of knowledge conversion: Socialization, Externalization, Combination, Internalization
- Knowledge spirals across ontological levels (individual → group → organization → inter-organizational)
- Concept of "Ba" (shared context/space) where knowledge is created and utilized

**Knowledge Conversion Modes:**
1. **Socialization** (Tacit → Tacit): Sharing experiences through observation, imitation, practice
2. **Externalization** (Tacit → Explicit): Articulating tacit knowledge into documents, models, metaphors
3. **Combination** (Explicit → Explicit): Systematizing concepts into knowledge systems
4. **Internalization** (Explicit → Tacit): Learning by doing, embodying knowledge into practice

**When to Use:**
- Understanding organizational knowledge flows
- Designing knowledge-sharing systems
- Bridging tacit knowledge across teams
- Building communities of practice

**Strengths:**
- Dynamic, process-oriented view of knowledge creation
- Acknowledges both tacit and explicit knowledge dimensions
- Widely validated across industries and cultures
- Provides actionable framework for knowledge management initiatives

**Limitations:**
- Can be difficult to operationalize without supporting tools
- Requires cultural support for knowledge sharing
- Does not prescribe specific technologies or methods
- Assumes organizational commitment to learning

**Integration with KM:**
SECI is foundational to modern KM. Most KM systems attempt to support at least one conversion mode. The model informs:
- Knowledge repository design (Combination)
- Mentoring programs (Socialization)
- Documentation practices (Externalization)
- Training and onboarding (Internalization)

**Citations:**
- [Managing Knowledge in Organizations: A Nonaka's SECI Model Operationalization - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6914727/)
- [SECI model of knowledge dimensions - Wikipedia](https://en.wikipedia.org/wiki/SECI_model_of_knowledge_dimensions)
- [SECI Model of Knowledge Dimensions - ToolsHero](https://www.toolshero.com/quality-management/seci-model-nonaka-takeuchi/)

---

#### 1.2 Wiig Knowledge Management Model (Wiig, 1993)

**Origin:** Karl Wiig, "Knowledge Management Foundations" (1993). Wiig is considered a founder of the knowledge management movement, using the term "Knowledge Management" as early as 1986.

**Core Principles:**
- Knowledge must be organized to be useful
- Knowledge organization depends on intended use
- Three-stage process: Building → Holding → Leveraging
- Four types of knowledge: Factual, Conceptual, Expectational, Methodological
- Three forms: Public, Shared, Personal

**The Three Major Components:**
1. **Knowledge Building**: Creation and acquisition through learning, experience, research, and validation
2. **Knowledge Holding**: Storage, documentation, and organization in retrievable forms
3. **Knowledge Leveraging**: Application, dissemination, and use for decision-making and innovation

**Levels of Internalization:**
- Novice: Unaware of available knowledge
- Beginner: Knows knowledge exists and where to find it
- Competent: Can use and reason with external help
- Expert: Holds knowledge in memory, reasons independently
- Master: Full internalization with deep understanding and value integration

**Quality Dimensions:**
- **Completeness**: Whether knowledge covers the full domain
- **Connectedness**: Relationships between knowledge parcels
- **Congruency**: Alignment with organizational objectives

**When to Use:**
- Assessing organizational knowledge maturity
- Designing knowledge repositories
- Training and skill development programs
- Knowledge audit and gap analysis

**Strengths:**
- Clear progression from knowledge acquisition to application
- Recognizes different knowledge types and forms
- Provides maturity model for individual and organizational learning
- Practical for assessing knowledge management needs

**Limitations:**
- Less focus on tacit knowledge than SECI
- Assumes knowledge can be effectively codified
- Limited guidance on social/collaborative aspects
- Can be bureaucratic if over-formalized

**Integration with KM:**
Wiig's model informs knowledge audits, competency frameworks, and learning management systems. Particularly useful for:
- Training curriculum design
- Knowledge retention during turnover
- Expert identification and mapping
- Knowledge base categorization

**Citations:**
- [The Wiig Model for Building and Using Knowledge - Theoretical Models](https://www.tlu.ee/~sirvir/IKM/Theoretical_models_of_Information_and_Knowledge_Management/the_wiig_model_for_building_and_using_knowledge.html)
- [4 Knowledge Management Models - HelpieWP](https://helpiewp.com/knowledge-management-models/)
- [Karl Wiig: Profiles in Knowledge - Medium](https://stangarfield.medium.com/karl-wiig-profiles-in-knowledge-cb09e2c9088e)

---

#### 1.3 Boisot I-Space Framework (Boisot, 1995)

**Origin:** Max Henri Boisot, "Information Space: A Framework for Learning in Organizations, Institutions and Culture" (1995)

**Core Principles:**
- Knowledge flows within a three-dimensional information space
- Information goods differ fundamentally from physical assets
- Social Learning Cycle (SLC) models dynamic knowledge flow
- Context determines knowledge value and shareability

**The Three Dimensions:**
1. **Codification**: Uncodified (tacit) ↔ Codified (explicit)
2. **Abstraction**: Concrete (context-specific) ↔ Abstract (generalizable)
3. **Diffusion**: Undiffused (private) ↔ Diffused (shared)

**Four Knowledge Types in I-Space:**
- **Public Knowledge**: Codified + Diffused (e.g., textbooks, newspapers)
- **Proprietary Knowledge**: Codified + Undiffused (e.g., patents, trade secrets)
- **Personal Knowledge**: Uncodified + Undiffused (e.g., individual expertise, biographical knowledge)
- **Common Sense**: Uncodified + Diffused (e.g., cultural knowledge, "what everybody knows")

**Social Learning Cycle (SLC) - Six Phases:**
1. **Scanning**: Gaining insights from generally available data
2. **Problem-Solving**: Structuring insights (codification)
3. **Abstraction**: Generalizing to broader contexts
4. **Diffusion**: Sharing with target population
5. **Absorption**: Applying to situations, producing new learning (becomes tacit again)
6. **Impacting**: Embedding in artifacts, rules, behaviors

**When to Use:**
- Analyzing knowledge flows across organizational boundaries
- Intellectual property strategy
- Innovation diffusion planning
- Understanding knowledge evolution over time

**Strengths:**
- Three-dimensional model captures nuanced knowledge states
- Social Learning Cycle shows knowledge as dynamic, not static
- Explains how knowledge moves between public and proprietary states
- Useful for competitive strategy and IP management

**Limitations:**
- Abstract and conceptual, requires interpretation
- Less prescriptive than other frameworks
- Complex to operationalize without significant training
- May oversimplify social dynamics of knowledge sharing

**Integration with KM:**
I-Space helps organizations understand:
- When to codify vs. keep knowledge tacit
- Patent vs. trade secret strategies
- Open innovation vs. proprietary approaches
- Knowledge transfer across cultures and contexts

**Citations:**
- [The Boisot I-Space KM Model - Theoretical Models](https://www.tlu.ee/~sirvir/IKM/Theoretical_models_of_Information_and_Knowledge_Management/the_boisot_ispace_km_model.html)
- [Max Boisot: Profiles in Knowledge - Medium](https://stangarfield.medium.com/max-boisot-profiles-in-knowledge-fdfd3352c1e5)
- [Navigating Information Flow: A Deep Dive into Max Boisot's I-Space](https://conikeec.substack.com/p/navigating-the-information-space)

---

#### 1.4 Cynefin Framework (Snowden, 1999)

**Origin:** Dave Snowden, developed at IBM Global Services (1999). Published in Harvard Business Review "A Leader's Framework for Decision Making" (2007) with Mary E. Boone.

**Core Principles:**
- Different contexts require different decision-making approaches
- Cause-and-effect relationships vary by domain complexity
- No one-size-fits-all management approach
- Sense-making before decision-making

**The Five Domains:**

1. **Clear/Obvious** (formerly "Simple")
   - Relationship: Cause and effect are obvious to all
   - Approach: **Sense → Categorize → Respond**
   - Method: Apply best practices
   - Examples: Standard operating procedures, known fixes

2. **Complicated**
   - Relationship: Cause and effect require analysis or expertise
   - Approach: **Sense → Analyze → Respond**
   - Method: Apply good practices (multiple right answers exist)
   - Examples: Engineering problems, expert diagnosis

3. **Complex**
   - Relationship: Cause and effect only deduced in retrospect
   - Approach: **Probe → Sense → Respond**
   - Method: Run safe-to-fail experiments, emergent practice
   - Examples: Market dynamics, cultural change, innovation

4. **Chaotic**
   - Relationship: No cause-and-effect relationship discernible
   - Approach: **Act → Sense → Respond**
   - Method: Novel practice, stabilize then move to complex
   - Examples: Crisis management, disasters

5. **Disorder/Confusion**
   - State: Unclear which domain applies
   - Approach: Break down into components and assign to other domains
   - Method: Gather more information, seek diverse perspectives

**When to Use:**
- Assessing problem complexity before choosing solution approach
- Avoiding "best practice" where it doesn't apply
- Strategy development in uncertain environments
- Team alignment on problem-solving approach

**Strengths:**
- Simple to understand and communicate
- Prevents misapplication of frameworks (e.g., PDCA in chaos)
- Widely adopted across industries and sectors
- Supports adaptive leadership in VUCA environments
- Won Academy of Management "Outstanding Practitioner-Oriented Publication" award

**Limitations:**
- Can be oversimplified in application
- Boundaries between domains can be fuzzy
- Doesn't prescribe specific methods within domains
- Risk of incorrect domain classification

**Integration with KM:**
Cynefin helps KM practitioners:
- Choose appropriate knowledge capture methods by domain
- Design different sharing mechanisms for different knowledge types
- Understand when to standardize (clear) vs. experiment (complex)
- Manage transition of problems across domains as understanding grows

**Citations:**
- [Cynefin framework - Wikipedia](https://en.wikipedia.org/wiki/Cynefin_framework)
- [A Leader's Framework for Decision Making - Harvard Business Review](https://hbr.org/2007/11/a-leaders-framework-for-decision-making)
- [About Cynefin Framework - The Cynefin Co](https://thecynefin.co/about-us/about-cynefin-framework/)
- [The Cynefin Framework - MindTools](https://www.mindtools.com/atddimk/the-cynefin-framework/)

---

### Category 2: Problem-Solving Frameworks

These frameworks provide structured approaches to identifying and resolving specific types of problems.

#### 2.1 TRIZ - Theory of Inventive Problem Solving (Altshuller, 1946)

**Origin:** Genrich Altshuller and colleagues, Soviet Union, beginning in 1946. Based on analysis of 200,000+ patents.

**Core Principles:**
- Innovation follows patterns that can be systematized
- Most problems have been solved before in other domains
- 95% of patents use only 40 inventive principles
- Evolution of technical systems follows objective laws
- Resolve contradictions without compromise (no trade-offs)

**Key Concepts:**

1. **40 Inventive Principles**: Universal problem-solving strategies (e.g., Segmentation, Asymmetry, Local Quality, Dynamicity, Periodic Action, Feedback)

2. **Contradiction Matrix**: 39×39 matrix mapping improving vs. worsening parameters to suggest applicable inventive principles

3. **Ideal Final Result (IFR)**: Envisioning the ideal solution helps identify path forward

4. **Technical Contradictions**: Improving one parameter negatively affects another

5. **Physical Contradictions**: A parameter must have opposite properties simultaneously

**When to Use:**
- Complex technical or engineering problems
- Product innovation and design
- Overcoming design constraints and trade-offs
- Systematic innovation rather than trial-and-error
- Cross-industry solution transfer

**Strengths:**
- Systematic, repeatable approach to innovation
- Leverages patterns from millions of inventions
- Reduces time to breakthrough solutions
- Applicable across industries and domains
- Proven at major corporations (Samsung, Boeing, NASA, Ford, Intel)

**Limitations:**
- Steep learning curve, requires training
- Originally designed for technical/engineering problems
- Can be complex to apply without expertise
- May not suit all problem types (especially non-technical)
- Tools and methods require significant investment

**Integration with KM:**
TRIZ enhances KM by:
- Creating knowledge repositories of solution patterns
- Enabling cross-domain knowledge transfer
- Formalizing innovation knowledge
- Capturing engineering expertise systematically

**Industry Adoption:**
Samsung, BAE Systems, GE, Mars (chocolate packaging patent), Rolls-Royce, Ford, Daimler-Chrysler, Boeing, NASA, HP, Motorola, IBM, Intel.

**Citations:**
- [TRIZ - Wikipedia](https://en.wikipedia.org/wiki/TRIZ)
- [TRIZ: The Backbone of Innovation - Quality Magazine](https://www.qualitymag.com/articles/98566-triz-the-backbone-of-innovation-and-problem-solving)
- [What is TRIZ? - TRIZ.co.uk](https://www.triz.co.uk/what-is-triz)
- [NASA: Can TRIZ Help You? - APPEL Knowledge Services](https://appel.nasa.gov/2010/02/23/aa_1-10_f_inventive-html/)

---

#### 2.2 Design Thinking (IDEO / Stanford d.school, 1990s-2000s)

**Origin:** Term coined at Stanford (1957), popularized by IDEO (1990s) and Stanford d.school (2005+). Key figures: David Kelley, Tim Brown.

**Core Principles:**
- Human-centered problem solving
- Empathy as foundation for innovation
- Iterative, non-linear process
- Bias toward action (prototyping over planning)
- Interdisciplinary collaboration
- Embrace ambiguity and failure as learning

**Stanford d.school Five Stages:**

1. **Empathize**: Understand users through observation, engagement, immersion
2. **Define**: Synthesize findings into actionable problem statement
3. **Ideate**: Generate wide range of creative solutions (divergent thinking)
4. **Prototype**: Build quick, low-fidelity representations
5. **Test**: Gather feedback, refine, iterate

**IDEO's Three-Stage Model:**
- **Inspiration**: Understanding the challenge, user needs, market landscape
- **Ideation**: Generating, developing, and testing ideas
- **Implementation**: Bringing solution to market

**Three Foundational Pillars:**
1. Empathy (understanding users deeply)
2. Experimentation (rapid prototyping and testing)
3. Iteration (continuous refinement based on feedback)

**When to Use:**
- User experience design problems
- Product/service innovation
- "Wicked problems" with unclear requirements
- Situations requiring creative breakthrough
- Cross-functional team collaboration
- Customer-centric strategy development

**Strengths:**
- Centers users and their actual needs
- Encourages creative, out-of-the-box thinking
- Reduces risk through rapid prototyping
- Accessible to non-designers
- Proven across industries (healthcare, education, technology, business)
- Fosters collaboration and diverse perspectives

**Limitations:**
- Can be time-intensive, especially empathy phase
- Requires cultural acceptance of iteration and "failure"
- May lack rigor for highly technical problems
- Can lead to over-emphasis on ideation vs. implementation
- Not all stakeholders understand the non-linear process

**Integration with KM:**
Design Thinking enhances KM through:
- User research creating knowledge about customer needs
- Prototyping as knowledge externalization
- Iteration embedding learning into artifacts
- Cross-functional collaboration spreading tacit knowledge

**Citations:**
- [What is Design Thinking? Stanford d.school Model](https://juanfernandopacheco.com/2025/01/what-is-design-thinking-stanford-d-school-model/)
- [Design Thinking by Stanford d.school and IDEO - Wind4Change](https://wind4change.com/design-thinking-d-school-stanford-ideo-approach-methodology/)
- [What is Design Thinking? - Interaction Design Foundation](https://www.interaction-design.org/literature/topics/design-thinking)

---

#### 2.3 Systems Thinking (Von Bertalanffy, Senge, Meadows, 1940s-1990s)

**Origin:** Ludwig von Bertalanffy (General Systems Theory, 1940s), popularized by Peter Senge ("The Fifth Discipline", 1990) and Donella Meadows ("Thinking in Systems", 2008).

**Core Principles:**
- Focus on relationships and interconnections, not just parts
- Systems produce their own patterns of behavior over time
- Structure drives behavior (mental models → systemic structures → patterns → events)
- Circular causality (feedback loops) vs. linear thinking
- Delays between cause and effect
- Non-obvious leverage points exist in systems

**Key Concepts:**

1. **Stocks and Flows**: Elements that accumulate (stocks) and rates of change (flows)
2. **Feedback Loops**:
   - Reinforcing loops (amplify change, exponential growth/decline)
   - Balancing loops (stabilize, goal-seeking)
3. **System Archetypes**: Common patterns (e.g., "Limits to Growth", "Shifting the Burden", "Tragedy of the Commons")
4. **Leverage Points**: Places to intervene in a system (Meadows' 12 leverage points, from parameters to paradigms)

**Senge's Fifth Discipline:**
Systems Thinking integrates with Personal Mastery, Mental Models, Shared Vision, and Team Learning to create "learning organizations."

**Meadows' Definition:**
"A system is a set of elements or parts interconnected in such a way that they produce their own pattern of behavior over time."

**When to Use:**
- Complex, multi-stakeholder problems
- Unintended consequences from past solutions
- Persistent problems that resist fixes
- Organizational change initiatives
- Policy design and analysis
- Long-term strategic planning

**Strengths:**
- Reveals hidden dynamics and feedback loops
- Prevents "fixes that backfire"
- Supports long-term thinking
- Applicable to social, technical, ecological systems
- Provides shared language for complexity

**Limitations:**
- Requires significant mental shift from linear thinking
- Can be overwhelmed by complexity
- Difficult to model all variables accurately
- May lead to analysis paralysis
- Requires time and patience, resists quick fixes

**Integration with KM:**
Systems Thinking in KM helps:
- Map knowledge flows as systems
- Identify feedback loops in learning processes
- Understand organizational learning dynamics
- Design interventions at leverage points
- Model knowledge ecosystems

**Citations:**
- [Systems Thinking - Von Bertalanffy, Senge, Meadows - Springer](https://link.springer.com/chapter/10.1007/978-3-030-43620-9_28)
- [Thinking in Systems: A Primer - Donella Meadows (PDF)](https://research.fit.edu/media/site-specific/researchfitedu/coast-climate-adaptation-library/climate-communications/psychology-amp-behavior/Meadows-2008.-Thinking-in-Systems.pdf)
- [Demystifying Systems Thinking - CISL Cambridge](https://www.cisl.cam.ac.uk/files/cisl_primer_demystifying_systems_thinking.pdf)

---

#### 2.4 Root Cause Analysis: 5 Whys & Ishikawa Diagram (1920s-1960s)

**Origin:**
- **Ishikawa (Fishbone) Diagram**: Kaoru Ishikawa, 1960s, Kawasaki shipyards. Basic concept from 1920s. One of the seven basic tools of quality control.
- **5 Whys**: Toyota Production System, Taiichi Ohno (though concept is older)

**Core Principles:**
- Problems have root causes, not just symptoms
- Asking "why" repeatedly reveals deeper causes
- Visual mapping helps identify all contributing factors
- Categorization organizes potential causes
- Best used together for comprehensive analysis

**Ishikawa (Fishbone) Diagram:**

**Structure:**
- Problem/defect as "fish head" (right side)
- Major cause categories as "bones"
- Sub-causes branch from major causes

**Common Categories (6 Ms):**
- **Methods**: Processes, procedures
- **Materials**: Inputs, raw materials
- **Machines**: Equipment, tools, technology
- **Measurements**: Inspection, data collection
- **Mother Nature**: Environment, conditions
- **Manpower**: People, skills, training

**5 Whys Technique:**
- Ask "Why did this happen?" 5 times (or until root cause reached)
- Each answer becomes the basis for the next question
- Simple, no special tools required
- Example:
  1. Why? → Car won't start
  2. Why? → Battery is dead
  3. Why? → Alternator not charging
  4. Why? → Alternator belt broken
  5. Why? → Belt exceeded lifespan, wasn't replaced per schedule
  - **Root cause**: Lack of preventive maintenance schedule

**Using Both Together:**
1. Create Fishbone diagram to identify all potential causes
2. For each major cause branch, apply 5 Whys
3. Expand Fishbone as deeper root causes discovered
4. Prioritize root causes for corrective action

**When to Use:**
- Quality problems and defects
- Process failures and errors
- Incident investigation
- Manufacturing issues
- Service delivery problems
- Any problem requiring root cause identification

**Strengths:**
- Simple, intuitive, widely accessible
- Visual (Fishbone) aids communication
- Encourages looking beyond symptoms
- Involves cross-functional teams
- Low cost, quick to implement
- Proven across industries (Microsoft for buggy software, Amazon for UI issues)

**Limitations:**
- 5 Whys: May oversimplify complex, multi-causal problems
- Fishbone: Can become convoluted with complex issues
- Both rely on team knowledge (garbage in, garbage out)
- May not identify truly novel causes
- Stopping too early misses root causes
- Multiple root causes can complicate analysis

**Integration with KM:**
RCA contributes to KM by:
- Capturing lessons learned from failures
- Building organizational problem-solving capability
- Creating knowledge repositories of common failure modes
- Supporting continuous improvement cultures

**Citations:**
- [Root Cause Analysis: 5 Whys vs. Fishbone - EasyRCA](https://easyrca.com/blog/root-cause-and-effect-analysis-5-whys-vs-fishbone/)
- [Ishikawa diagram - Wikipedia](https://en.wikipedia.org/wiki/Ishikawa_diagram)
- [Root Cause Analysis: Integrating Ishikawa Diagrams and 5 Whys - iSixSigma](https://www.isixsigma.com/cause-effect/root-cause-analysis-ishikawa-diagrams-and-the-5-whys/)
- [Cause and Effect Analysis - Visual Paradigm](https://www.visual-paradigm.com/project-management/fishbone-diagram-and-5-whys/)

---

### Category 3: Decision Frameworks

These frameworks provide systematic approaches to making decisions under various conditions.

#### 3.1 OODA Loop (Boyd, 1970s)

**Origin:** Colonel John Boyd, U.S. Air Force, early 1970s. Developed from fighter pilot tactics and thermodynamics (Energy-Manoeuvrability Theory).

**Core Principles:**
- Speed of decision cycle matters more than raw speed
- "Get inside" opponent's decision loop
- Agility beats speed
- Continuous observation and adaptation
- Decision-making is iterative, not linear

**The Four Stages:**

1. **Observe**: Gather information from environment
   - Raw data collection from multiple sources
   - Awareness of changing conditions

2. **Orient**: Analyze and synthesize information
   - Most critical and complex stage
   - Influenced by cultural traditions, genetic heritage, previous experiences, mental models
   - Synthesize data into understanding

3. **Decide**: Select course of action
   - Hypothesis formation
   - Choose among alternatives

4. **Act**: Execute decision
   - Implementation
   - Creates new observations (feedback)

**Key Insight:**
"Orientation" is the critical phase where mental models, culture, and experience shape interpretation. Getting inside opponent's OODA loop means:
- Observing faster
- Orienting more accurately
- Deciding more wisely
- Acting more swiftly
- Thereby creating confusion and disorientation in adversary

**When to Use:**
- Competitive, rapidly changing environments
- Military and security operations
- Business strategy in dynamic markets
- Crisis response and emergency management
- Sports coaching and tactics
- Cybersecurity and threat response

**Strengths:**
- Emphasizes adaptability and speed
- Applicable across domains (military, business, sports)
- Simple four-stage model
- Recognizes importance of mental models (orientation)
- Proven in military doctrine (AirLand Battle, NATO, mission command)
- Supports agile, iterative approaches

**Limitations:**
- Can be oversimplified to "move fast"
- Vague enough to see what you want to see in it
- Doesn't prescribe specific methods within stages
- May encourage reactive vs. strategic thinking
- Limited guidance on collaborative decision-making

**Boyd's Background:**
- Nickname: "Forty-Second Boyd" (could win dogfight in <40 seconds)
- Developed Energy-Manoeuvrability Theory (transformed aircraft design)
- Influenced AirLand Battle doctrine and mission command concept

**Integration with KM:**
OODA Loop in KM:
- Observation = Knowledge acquisition
- Orientation = Sense-making and contextualization
- Decide = Knowledge application
- Act = Knowledge creation through action
- Loop = Continuous learning cycle

**Citations:**
- [OODA loop - Wikipedia](https://en.wikipedia.org/wiki/OODA_loop)
- [The OODA Loop - The Decision Lab](https://thedecisionlab.com/reference-guide/computer-science/the-ooda-loop)
- [The OODA Loop Explained - OODAloop.com](https://oodaloop.com/the-ooda-loop-explained-the-real-story-about-the-ultimate-model-for-decision-making-in-competitive-environments/)
- [How Fighter Pilots Make Fast and Accurate Decisions - Farnam Street](https://fs.blog/ooda-loop/)

---

#### 3.2 Kepner-Tregoe Method (Kepner & Tregoe, 1965)

**Origin:** Charles Kepner and Benjamin Tregoe, "The Rational Manager: A Systematic Approach to Problem Solving and Decision Making" (1965)

**Core Principles:**
- Disconnect "problem" from "decision"
- Systematic, structured thinking reduces oversight and error
- Goal is "best possible" choice, not perfect choice
- Separate problem analysis from decision analysis
- Proactive approach to potential problems/opportunities

**The Four Key Processes:**

1. **Situation Appraisal**
   - Define scope and priority
   - Questions: What's happening? How urgent/important? Who's involved?
   - Break complex situations into manageable concerns

2. **Problem Analysis**
   - Identify root cause
   - "IS / IS NOT" analysis (What, Where, When, How Big)
   - Specify problem precisely
   - Test possible causes
   - Verify the true cause

3. **Decision Analysis**
   - Evaluate alternatives against objectives
   - Separate "musts" from "wants"
   - Weight objectives by importance
   - Assess risks of each alternative
   - Make informed selection

4. **Potential Problem/Opportunity Analysis**
   - Forecast future issues
   - Identify preventive actions
   - Prepare contingency plans
   - Capitalize on opportunities
   - Proactive risk management

**When to Use:**
- Complex, high-stakes decisions
- Problems requiring systematic investigation
- Situations with multiple alternatives
- Risk assessment and mitigation
- IT incident management (ITIL)
- Corrective/preventive action (CAPA)
- Integration with Lean, Six Sigma, 8D

**Strengths:**
- Rigorous, logical framework
- Reduces likelihood of oversight
- Common language for teams (builds consensus)
- Develops critical thinking skills
- Well-respected, adopted by top organizations (NASA, General Motors)
- Timeless framework for complex systems
- Transferable skills across domains

**Limitations:**
- Can be time-intensive for simple problems
- Requires training and practice
- May feel bureaucratic if over-applied
- Cultural acceptance needed (some prefer intuitive decisions)
- Not suited to chaotic or highly creative contexts

**Integration with KM:**
Kepner-Tregoe enhances KM by:
- Structuring problem-solving knowledge
- Creating decision audit trails
- Building organizational decision-making competency
- Standardizing root cause analysis
- Capturing rationale for decisions

**Citations:**
- [The Kepner-Tregoe Matrix - MindTools](https://www.mindtools.com/atznth6/the-kepner-tregoe-matrix/)
- [Kepner Tregoe Method - ToolsHero](https://www.toolshero.com/problem-solving/kepner-tregoe-method/)
- [Kepner-Tregoe: Structured Problem Solving - Microsoft Community](https://techcommunity.microsoft.com/blog/azuredbsupport/kepner%E2%80%91tregoe-a-structured-and-rational-approach-to-problem-solving-and-decision/4482643)

---

#### 3.3 PDCA Cycle (Shewhart/Deming, 1920s-1950s)

**Origin:** Walter A. Shewhart (1920s-1930s), popularized by W. Edwards Deming (1950s+). Also called Shewhart Cycle or Deming Cycle.

**Core Principles:**
- Continuous improvement through iterative cycles
- Scientific method applied to business
- Prediction → experimentation → learning
- No end to improvement (spiral, not circle)
- Quality control through systematic process

**The Four Steps:**

1. **Plan**
   - Define quality goals
   - Understand customer requirements
   - Develop strategic plan
   - Identify potential problems
   - Predict outcomes based on data
   - Establish success metrics

2. **Do**
   - Implement solution/change
   - Execute on small scale initially (pilot)
   - Collect data during implementation
   - Document process

3. **Check** (or **Study**)
   - Confirm results through before/after comparison
   - Analyze collected data
   - Compare actual vs. predicted results
   - Determine if solution addresses problem
   - **Note**: Deming preferred "Study" over "Check" (PDSA vs. PDCA)

4. **Act** (or **Adjust**)
   - If successful: Standardize and implement broadly
   - If unsuccessful: Learn and start new cycle
   - Document results and recommendations
   - Inform others about process changes
   - Make recommendations for next PDCA cycle

**PDCA vs. PDSA:**
- Deming emphasized **PDSA** (Plan-Do-Study-Act)
- "Study" focuses on predicting results, comparing to actuals, revising theory
- "Check" more binary (success/failure of implementation)
- Study encourages deeper learning

**Iterative Nature:**
- "Just as a circle has no end, the PDCA cycle should be repeated again and again"
- Each cycle should increase knowledge
- Spirals converge toward ultimate goal

**When to Use:**
- Continuous improvement initiatives
- Quality management (TQM, ISO 9001)
- Manufacturing optimization
- Healthcare process improvement
- Service delivery enhancement
- Any process requiring iterative refinement

**Strengths:**
- Simple, intuitive four-step model
- Proven across industries and decades
- Supports data-driven decision making
- Embeds learning into operations
- Scalable (individuals to organizations)
- Foundation for Lean and Six Sigma

**Limitations:**
- Requires cultural commitment to continuous improvement
- Can be slow for urgent problems
- Assumes problems are measurable
- May resist radical innovation (favors incremental)
- Needs discipline to complete cycles

**Integration with KM:**
PDCA embeds learning into operations:
- Plan = Knowledge gathering and prediction
- Do = Knowledge application and testing
- Study = Reflection and sense-making
- Act = Knowledge capture and standardization

**Citations:**
- [PDCA Cycle - ASQ](https://asq.org/quality-resources/pdca-cycle)
- [PDCA - Wikipedia](https://en.wikipedia.org/wiki/PDCA)
- [PDSA Cycle - The W. Edwards Deming Institute](https://deming.org/explore/pdsa/)
- [The Deming Cycle (PDCA) Explained - Brightly Software](https://www.brightlysoftware.com/learning-center/the-deming-cycle-pdca-explained-a-comprehensive-guide-to-continuous-improvement)

---

#### 3.4 A3 Problem Solving (Toyota, 1960s+)

**Origin:** Toyota Production System, attributed to Taiichi Ohno. Rumor: Ohno refused to read past first page of reports, so teams created one-page summaries on A3 paper.

**Core Principles:**
- Problem-solving on a single sheet of A3-size paper
- Based on PDCA cycle
- Solve problems at the source, permanently
- Address root causes, not symptoms
- Structured thinking + visual communication
- Learning through mentorship (not giving answers)

**The Seven Steps (A3 Template Boxes):**

1. **Background/Business Context**
   - Why this problem matters
   - Establish importance and urgency

2. **Current Condition**
   - Describe the current state objectively
   - Use data and observations, not opinions

3. **Desired Outcome/Goal**
   - Define target state
   - What success looks like

4. **Root Cause Analysis**
   - Analyze situation to establish causality
   - Use tools like 5 Whys, Fishbone

5. **Countermeasures**
   - Propose solutions to address root causes
   - Evaluate alternatives

6. **Action Plan**
   - Who does what, when
   - Prescribe implementation steps
   - Assign responsibilities

7. **Follow-Up**
   - How will success be measured?
   - Monitoring and evaluation plan
   - Lessons learned

**Three Key Roles:**

1. **Owner**: Manages A3 process, maintains the report
2. **Mentor/Coach**: Guides owner without giving direct solutions, encourages learning
3. **Responders/Stakeholders**: Provide input, impacted by problem/solution

**A3 Thinking (More Than Template):**
- The template is less important than the thinking process
- Flexible, adaptable to different situations
- Emphasizes understanding before solving
- "Gemba walk" principle: see problems first-hand
- Encourages dialogue and collaboration

**When to Use:**
- Problem-solving (find and fix root causes)
- Proposal development (new initiatives)
- Status reporting (project updates)
- Strategic planning
- Any situation requiring structured thinking + communication

**Strengths:**
- Concise, forces clarity and prioritization
- Visual, one-page format aids communication
- Combines problem-solving with documentation
- Fosters learning through coaching
- Aligns interests across organization
- Basis for collaboration and dialogue
- Part of proven Toyota Production System

**Limitations:**
- Requires cultural support (Lean mindset)
- One page can feel constraining for complex issues
- Coaching/mentorship role requires skill
- May be seen as bureaucratic if forced
- Takes time to understand problem thoroughly

**Integration with KM:**
A3 thinking enhances KM by:
- Creating knowledge artifacts (completed A3s)
- Mentoring as tacit knowledge transfer (SECI socialization)
- Documenting reasoning, not just conclusions
- Building problem-solving capability organization-wide
- Capturing lessons learned systematically

**Best Practices:**
- Go to Gemba (go and see actual conditions)
- Focus on understanding, not rushing to solutions
- Use A3 as conversation tool, not just report
- Iterate based on feedback
- Archive A3s as organizational learning resources

**Citations:**
- [A3 problem solving - Wikipedia](https://en.wikipedia.org/wiki/A3_problem_solving)
- [Toyota's Secret: The A3 Report - MIT Sloan Management Review](https://sloanreview.mit.edu/article/toyotas-secret-the-a3-report/)
- [What is A3 Problem Solving? - Kanban Tool](https://kanbantool.com/kanban-guide/a3-problem-solving)
- [How to use Toyota's legendary A3 problem solving technique - Nulab](https://nulab.com/learn/project-management/use-toyotas-legendary-a3-problem-solving-technique/)

---

### Category 4: AI-Era Frameworks

These frameworks leverage LLMs and AI to enhance knowledge retrieval, reasoning, and problem-solving.

#### 4.1 RAG - Retrieval Augmented Generation (2020+)

**Origin:** Emerging from LLM research (2020+), formalized in various papers. Widely adopted by 2023-2024 as LLMs scaled.

**Core Principles:**
- LLMs have limited/outdated knowledge from training data
- External knowledge retrieval improves accuracy and relevance
- Combine parametric knowledge (in weights) with non-parametric knowledge (retrieved)
- Reduce hallucination through grounding
- Enable continuous knowledge updates without retraining

**How It Works:**

1. **Indexing Phase** (offline):
   - Convert documents to embeddings (vector representations)
   - Store in vector database

2. **Retrieval Phase** (query-time):
   - Convert user query to embedding
   - Search vector database for most relevant documents
   - Retrieve top-k most similar documents

3. **Augmentation Phase**:
   - Inject retrieved documents into prompt context
   - Augment query with relevant information

4. **Generation Phase**:
   - LLM generates response using both its training and retrieved context
   - Grounded in provided documents

**RAG Paradigms (Evolution):**

1. **Naive RAG**: Simple retrieval → augmentation → generation
2. **Advanced RAG**: Pre-retrieval and post-retrieval improvements (query rewriting, re-ranking)
3. **Modular RAG**: Composable components, multi-source retrieval, agentic retrieval (2025+)

**Agentic Retrieval (2025 State-of-Art):**
- LLM-assisted query planning
- Break complex queries into focused subqueries
- Parallel execution
- Structured responses optimized for chat models
- Example: Azure AI Search agentic retrieval (preview)

**Recent Research:**
- **"Sufficient Context"** (ICLR 2025, Google): Understanding when LLM has enough information to answer correctly
- Emphasis on retrieval quality over quantity

**When to Use:**
- Domain-specific Q&A systems
- Enterprise knowledge bases
- Customer support chatbots
- Document search and analysis
- Any LLM application requiring up-to-date or specialized knowledge

**Strengths:**
- Improves LLM accuracy and relevance
- Reduces hallucinations through grounding
- Enables knowledge updates without retraining
- Cost-effective vs. fine-tuning
- Provides source attribution/provenance
- Applicable to any domain with text data

**Limitations:**
- Retrieval quality critical (garbage in, garbage out)
- Context window limits how much can be injected
- Latency from retrieval step
- Vector embeddings may miss nuanced relationships
- Requires vector database infrastructure
- May struggle with multi-hop reasoning across documents

**Integration with KM:**
RAG transforms KM by:
- Making organizational knowledge LLM-accessible
- Enabling semantic search over documents
- Reducing knowledge silos
- Providing conversational interface to KM systems

**Technical Components:**
- **Embeddings**: Text → vector space (e.g., OpenAI, Cohere, local models)
- **Vector Databases**: Pinecone, Weaviate, ChromaDB, FAISS
- **Chunking Strategies**: How to split documents
- **Hybrid Search**: Combining semantic (vector) + keyword (BM25)

**Citations:**
- [Retrieval Augmented Generation (RAG) - Prompt Engineering Guide](https://www.promptingguide.ai/research/rag)
- [What is RAG? - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
- [Retrieval-augmented generation - Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [RAG in 2025: Bridging Knowledge and Generative AI - Squirro](https://squirro.com/squirro-blog/state-of-rag-genai)
- [All You Need To Know About RAG in 2025 - Towards AI](https://pub.towardsai.net/all-you-need-to-know-about-retrieval-augmented-generation-rag-in-2025-04c386284c18)

---

#### 4.2 GraphRAG (Microsoft, 2024)

**Origin:** Microsoft Research, publicly released on GitHub in 2024. Now available in Microsoft Discovery (agentic platform for scientific research).

**Core Principles:**
- Knowledge graphs provide structured representation of relationships
- Hierarchical community structure improves retrieval
- Pre-summarization of semantic clusters
- Better for "unknown unknowns" and multi-hop reasoning
- Graph-based indexing vs. flat vector search

**How It Works:**

1. **Extraction Phase**:
   - Slice corpus into TextUnits
   - LLM extracts entities, relationships, and key claims
   - Build knowledge graph from extracted information

2. **Community Detection**:
   - Bottom-up clustering organizes graph hierarchically
   - Identifies semantic communities/themes
   - Creates multi-level hierarchy (local → global)

3. **Summarization**:
   - Pre-generate summaries for each community
   - Hierarchical summaries (detailed → abstract)

4. **Query Phase**:
   - Use graph structure to retrieve relevant communities
   - Leverage pre-computed summaries
   - Provide both answers and provenance

**Key Differences from Standard RAG:**

| Aspect | Standard RAG | GraphRAG |
|--------|-------------|----------|
| Structure | Flat documents + embeddings | Knowledge graph + communities |
| Retrieval | Vector similarity | Graph traversal + community |
| Summarization | None (raw chunks) | Pre-computed community summaries |
| Reasoning | Single-hop | Multi-hop via graph |
| Strength | Known questions | Unknown unknowns, exploration |

**When to Use:**
- Complex, interconnected knowledge domains
- Multi-hop reasoning requirements
- Exploratory questions ("What are the themes in this corpus?")
- Scientific research and discovery
- When relationships matter as much as entities
- Private/proprietary datasets requiring deep understanding

**Strengths:**
- Vastly improved retrieval relevance
- Handles multi-hop questions
- Provides comprehensive thematic answers
- Source grounding and provenance tracking
- Excellent for "connecting the dots" across documents
- Hierarchical structure supports different query types
- Ideal for previously unseen datasets

**Limitations:**
- **Expensive**: LLM-powered indexing can cost significant money and time
- Requires careful prompt tuning for domain
- More complex infrastructure (graph database or structures)
- Overkill for simple retrieval tasks
- Indexing time longer than standard RAG
- Start small and test before scaling

**Integration with KM:**
GraphRAG enhances KM by:
- Revealing hidden connections in knowledge base
- Supporting discovery vs. just search
- Capturing conceptual relationships, not just keywords
- Enabling strategic knowledge exploration

**Best Practices:**
- Read all documentation before starting (cost awareness)
- Fine-tune prompts for your domain
- Start with small dataset
- Use for complex knowledge work, not simple FAQ

**Availability:**
- Open source on GitHub: [microsoft/graphrag](https://github.com/microsoft/graphrag)
- Integrated in Microsoft Discovery platform (Azure)

**Citations:**
- [Welcome - GraphRAG Official Docs](https://microsoft.github.io/graphrag/)
- [GitHub - microsoft/graphrag](https://github.com/microsoft/graphrag)
- [Project GraphRAG - Microsoft Research](https://www.microsoft.com/en-us/research/project/graphrag/)
- [GraphRAG: Unlocking LLM discovery on narrative private data - Microsoft Research](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)
- [GraphRAG Explained: Enhancing RAG with Knowledge Graphs - Zilliz/Medium](https://medium.com/@zilliz_learn/graphrag-explained-enhancing-rag-with-knowledge-graphs-3312065f99e1)

---

#### 4.3 Chain-of-Thought (CoT) Prompting (Wei et al., 2022)

**Origin:** "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" by Wei et al., 2022 ([arXiv:2201.11903](https://arxiv.org/abs/2201.11903))

**Core Principles:**
- LLMs can perform better reasoning with intermediate steps
- Simulates human-like step-by-step thinking
- Emergent ability in large models (~100B+ parameters)
- Breaks complex problems into manageable steps
- Makes reasoning transparent and auditable

**How It Works:**

**Few-Shot CoT:**
- Provide examples (exemplars) showing reasoning process
- Each example includes: Question → Reasoning Steps → Answer
- LLM learns to mimic reasoning pattern
- Example:
  ```
  Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 balls. How many tennis balls does he have now?
  A: Roger started with 5 balls. 2 cans of 3 balls each is 6 balls. 5 + 6 = 11. The answer is 11.

  Q: [Your actual question]
  ```

**Zero-Shot CoT:**
- Simply add "Let's think step by step" to prompt
- No examples needed
- Example: MultiArith benchmark accuracy jumped from 17.7% → 78.7% (InstructGPT)

**Auto-CoT:**
- Automatically generate reasoning chains
- Sample questions with diversity
- Construct demonstrations automatically

**Types of Reasoning Enhanced:**
- Arithmetic reasoning
- Commonsense reasoning
- Symbolic reasoning
- Multi-step logical inference

**When to Use:**
- Complex, multi-step problems
- Math and logic tasks
- Situations requiring explanation of reasoning
- When transparency matters (auditing LLM decisions)
- Tasks where breaking down helps accuracy

**Strengths:**
- Significantly improves accuracy on reasoning tasks
- Provides interpretable reasoning traces
- Reduces logical errors and hallucinations
- Helps identify where LLM goes wrong
- Simple to implement (just add examples or prompt phrase)
- Works across different LLM architectures

**Limitations:**
- **Only effective with large models (~100B+ parameters)**
- Smaller models produce illogical chains → worse accuracy
- Adds tokens to context (cost and latency)
- May over-complicate simple tasks
- Quality depends on example selection (Few-Shot) or model capability (Zero-Shot)
- Can still produce confident but incorrect reasoning

**Integration with KM:**
CoT enhances KM by:
- Externalizing reasoning as knowledge artifact
- Teaching problem-solving patterns
- Creating audit trails for decisions
- Supporting learning through worked examples

**Variations:**
- **Self-Consistency CoT**: Generate multiple reasoning paths, use majority vote
- **Least-to-Most Prompting**: Break problem into subproblems
- **Tree-of-Thoughts**: Explore multiple reasoning branches

**Citations:**
- [Chain-of-Thought Prompting Elicits Reasoning - arXiv](https://arxiv.org/abs/2201.11903)
- [Chain-of-Thought Prompting - Learn Prompting](https://learnprompting.org/docs/intermediate/chain_of_thought)
- [What is Chain of Thought Prompting? - IBM](https://www.ibm.com/think/topics/chain-of-thoughts)
- [Chain-of-Thought Prompting - Prompt Engineering Guide](https://www.promptingguide.ai/techniques/cot)

---

#### 4.4 ReAct - Reasoning + Acting (Yao et al., 2023)

**Origin:** "ReAct: Synergizing Reasoning and Acting in Language Models" by Yao et al., 2023 ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629)). Google Research / Princeton.

**Core Principles:**
- Combine reasoning (internal thought) with acting (external tool use)
- Synergy: Reasoning guides actions, actions inform reasoning
- Interleaved thought-action-observation loop
- Dynamic planning and error correction
- Grounding in external environments reduces hallucination

**How It Works:**

**The ReAct Loop:**
```
Thought → Action → Observation → Thought → Action → Observation → ... → Answer
```

1. **Thought**: LLM reasons about what to do next
2. **Action**: LLM calls external tool (search, calculator, API, etc.)
3. **Observation**: Environment returns result to LLM
4. **Repeat**: Until sufficient information gathered or answer determined

**Example Scenario (Question Answering):**
```
Question: What is the elevation of the mountain where the 2020 Summer Olympics torch relay started?

Thought: I need to find where the torch relay started.
Action: Search[2020 Summer Olympics torch relay]
Observation: The relay started at Mount Olympus in Greece.

Thought: Now I need to find the elevation of Mount Olympus.
Action: Search[Mount Olympus elevation]
Observation: Mount Olympus has an elevation of 2,917 meters.

Thought: I have the answer.
Answer: 2,917 meters
```

**Key Components:**

1. **LLM (Reasoning Engine)**: Generates thoughts and decides actions
2. **Tools/Actions**: APIs, search engines, calculators, databases, code execution
3. **Environment**: External knowledge sources that provide observations
4. **Prompt Template**: Defines Thought/Action/Observation format

**Comparison to Alternatives:**

| Approach | Reasoning | Acting | Result |
|----------|-----------|--------|--------|
| Reason-Only (CoT) | ✓ | ✗ | Hallucination, outdated info |
| Act-Only | ✗ | ✓ | Can't synthesize, lacks planning |
| ReAct | ✓ | ✓ | Grounded, adaptive, accurate |

**When to Use:**
- Questions requiring external information
- Multi-step research tasks
- Problems needing both reasoning and data lookup
- Agentic workflows (autonomous task completion)
- Situations where LLM knowledge is insufficient
- When actions have consequences in external systems

**Strengths:**
- Overcomes hallucination by grounding in real data
- Handles "unknown unknowns" through exploration
- Adaptive planning (can change course based on observations)
- Interpretable (can audit thought process)
- More accurate than CoT alone on fact-based tasks (HotpotQA, Fever)
- Generates human-like problem-solving trajectories

**Limitations:**
- Requires access to external tools/APIs
- More complex to implement than simple prompting
- Latency from multiple LLM calls + tool invocations
- Tool reliability becomes critical
- Can be expensive (multiple LLM calls per task)
- Agent may get stuck in loops or take inefficient paths

**Integration with KM:**
ReAct enhances KM by:
- Making knowledge bases actionable (not just searchable)
- Combining explicit knowledge (documents) with procedural knowledge (how to search)
- Creating trace logs of knowledge discovery process
- Enabling autonomous knowledge work

**Modern Implementations:**
- **LangChain / LlamaIndex**: ReAct agent frameworks
- **AutoGPT / BabyAGI**: Autonomous agent systems
- **Function Calling APIs**: OpenAI, Anthropic, Google (Claude, GPT-4, Gemini)

**ReAct vs. Standard RAG:**
- RAG: Single retrieval step
- ReAct: Iterative, multi-turn retrieval with reasoning
- ReAct can decide WHEN and WHAT to retrieve based on reasoning

**Citations:**
- [ReAct: Synergizing Reasoning and Acting - arXiv](https://arxiv.org/abs/2210.03629)
- [ReAct: Synergizing Reasoning and Acting - Google Research Blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)
- [What is a ReAct Agent? - IBM](https://www.ibm.com/think/topics/react-agent)
- [ReAct Prompting - Prompt Engineering Guide](https://www.promptingguide.ai/techniques/react)
- [ReAct Official Site](https://react-lm.github.io/)

---

## L2: Strategic Framework Selection for Jerry

This section provides strategic guidance for selecting and integrating frameworks within the Jerry architecture.

### Jerry's Unique Context

Jerry operates with specific architectural constraints and capabilities:

**Strengths:**
- Filesystem-as-memory (persistent, infinite context)
- Structured knowledge hierarchy (`docs/` organization)
- Skills-based agent interfaces
- CQRS pattern for commands/queries
- Constitutional governance (Jerry Constitution v1.0)

**Challenges:**
- Context rot as conversation lengthens
- Agent nesting limitations (max 1 level: orchestrator → worker)
- Need for systematic knowledge capture
- Balancing autonomy with human oversight

### Recommended Framework Stack for Jerry

#### Layer 1: Problem Classification (Entry Point)

**Primary Framework: Cynefin**

**Purpose:** Classify problems before applying frameworks

**Integration:**
- Create skill: `problem-classifier` that applies Cynefin domains
- Maps domains to appropriate frameworks:
  - **Clear** → A3, PDCA (standard processes)
  - **Complicated** → Kepner-Tregoe, TRIZ (expert analysis)
  - **Complex** → Systems Thinking, Design Thinking (experimentation)
  - **Chaotic** → OODA Loop (rapid action)

**Implementation:**
```
User request → problem-classifier skill → Cynefin domain assessment → framework recommendation
```

**Why Cynefin for Jerry:**
- Prevents misapplication of frameworks (e.g., PDCA in chaos)
- Aligns with Jerry's need for context-aware responses
- Simple enough to apply quickly
- Prevents "one-size-fits-all" approach

---

#### Layer 2: Knowledge Flow Management

**Primary Framework: SECI Model**

**Purpose:** Manage tacit ↔ explicit knowledge conversion

**Integration with Jerry's Architecture:**

1. **Socialization (Tacit → Tacit)**
   - Agent-to-agent collaboration (orchestrator ↔ specialist)
   - Pair programming / review sessions documented in `docs/experience/`
   - User-agent dialogue captured in session logs

2. **Externalization (Tacit → Explicit)**
   - Skills externalize tacit knowledge into markdown interfaces
   - `docs/wisdom/` captures heuristics and principles
   - ADRs (Architecture Decision Records) document reasoning

3. **Combination (Explicit → Explicit)**
   - Knowledge synthesis in `docs/research/`
   - Cross-referencing between documents
   - Aggregation of learnings into higher-level patterns

4. **Internalization (Explicit → Tacit)**
   - Agent training on accumulated knowledge
   - User reading and absorbing documentation
   - Applying documented patterns in new contexts

**Why SECI for Jerry:**
- Aligns with filesystem-as-memory (explicit knowledge storage)
- Supports multi-agent knowledge sharing
- Provides structure for `docs/` hierarchy
- Addresses Jerry's core mission: accruing knowledge, wisdom, experience

**Implementation:**
- Update `worktracker` skill to tag work by SECI mode
- Create `knowledge-flow` skill that maps Jerry's artifacts to SECI
- Ensure each significant output goes through externalization

---

#### Layer 3: AI-Augmented Problem Solving

**Primary Frameworks: ReAct + GraphRAG**

**Purpose:** Leverage LLM capabilities with grounding and reasoning

**ReAct Integration:**
- `problem-solving` skill already uses ReAct pattern implicitly
- Make explicit: Thought (reasoning trace) → Action (tool call) → Observation → repeat
- Tools: File operations, Bash commands, Grep, Glob, WebSearch
- Capture reasoning traces in PLAN files or work logs

**GraphRAG Integration:**
- Build knowledge graph from `docs/` hierarchy
- Entities: Frameworks, principles, agents, skills
- Relationships: Uses, extends, conflicts-with, supports
- Communities: Group related concepts (e.g., "Quality Management", "AI Frameworks")
- Query interface for complex questions: "What frameworks address tacit knowledge transfer?"

**Why ReAct + GraphRAG for Jerry:**
- ReAct aligns with agent architecture (reasoning + acting)
- GraphRAG addresses Jerry's growing knowledge base
- Combination supports both exploration and exploitation
- Reduces context rot by retrieving only relevant knowledge

**Phased Implementation:**
1. **Phase 1** (Current): ReAct via existing agent patterns
2. **Phase 2**: Standard RAG over `docs/` with vector embeddings
3. **Phase 3**: GraphRAG with full knowledge graph extraction

---

#### Layer 4: Continuous Learning and Documentation

**Primary Framework: A3 Problem Solving**

**Purpose:** Capture learnings systematically, one-page format

**Integration:**
- Create `a3-template.md` in `.claude/templates/`
- Use for significant problem-solving sessions
- Completed A3s stored in `docs/a3/` by date or WORK-ID
- Seven sections map to Jerry's workflow:
  1. **Background** → WORK-ID context
  2. **Current Condition** → Initial state assessment
  3. **Desired Outcome** → Success criteria
  4. **Root Cause Analysis** → Investigation results
  5. **Countermeasures** → Solutions applied
  6. **Action Plan** → Implementation steps
  7. **Follow-Up** → Lessons learned

**Why A3 for Jerry:**
- Concise format combats context rot
- Structured thinking improves output quality
- One-page constraint forces prioritization
- Creates knowledge artifacts (completed A3s)
- Aligns with Jerry's principle P-002 (File Persistence)

**Implementation:**
```markdown
## A3 Template Structure
WORK-ID: [ID]
Date: [YYYY-MM-DD]
Owner: [Agent/User]

### 1. Background
Why this matters...

### 2. Current Condition
Observed state...

### 3. Goal
Target state...

### 4. Root Cause Analysis
Why it's happening...

### 5. Countermeasures
How we'll address it...

### 6. Action Plan
Who | What | When

### 7. Follow-Up
Metrics | Learnings
```

---

#### Supporting Frameworks (Tactical Use)

**5 Whys / Ishikawa (Root Cause Analysis):**
- Use within A3 section 4
- Apply during incident post-mortems
- Document in `docs/experience/failures/`

**PDCA (Continuous Improvement):**
- Apply to incremental improvements
- Integrate with Work Tracker (Plan → In Progress → Check → Act/Close)
- Useful for clear/obvious domain problems (Cynefin)

**Systems Thinking:**
- Apply to architectural decisions
- Map feedback loops in Jerry's operation
- Use for understanding agent interaction dynamics
- Document in ADRs when architectural changes needed

**Design Thinking:**
- Apply to user-facing features (skills, interfaces)
- Empathize with user needs
- Prototype solutions before full implementation

**TRIZ:**
- Reserve for technical contradictions
- Not primary framework (Jerry is software, not hardware)
- Could apply to agent design trade-offs

---

### Framework Selection Decision Matrix

| Problem Type | Cynefin Domain | Recommended Framework | Jerry Artifact |
|--------------|----------------|----------------------|----------------|
| Classify problem | Any | Cynefin | PLAN file (domain noted) |
| Knowledge capture | Clear/Complicated | A3 + SECI Externalization | `docs/a3/`, `docs/wisdom/` |
| Root cause investigation | Clear/Complicated | 5 Whys / Ishikawa | A3 Section 4 |
| Incremental improvement | Clear | PDCA | Work Tracker |
| Complex knowledge synthesis | Complex | ReAct + GraphRAG | `docs/research/`, `docs/knowledge/` |
| Architectural decision | Complicated/Complex | Systems Thinking + ADR | `docs/design/ADR-XXX.md` |
| User-facing feature | Complex | Design Thinking | Prototypes, feedback loops |
| Technical contradiction | Complicated | TRIZ | Engineering docs |
| Rapid decision under uncertainty | Chaotic/Complex | OODA Loop | Incident logs |
| High-stakes decision | Complicated | Kepner-Tregoe | Decision logs |

---

### Integration with Jerry Constitution

**Mapping Frameworks to Constitutional Principles:**

| Framework | Constitutional Principles Supported |
|-----------|-------------------------------------|
| A3 | P-002 (File Persistence), P-004 (Reasoning Documentation) |
| SECI | P-002 (File Persistence), P-010 (Task Tracking Integrity) |
| ReAct | P-001 (Truth/Accuracy), P-004 (Reasoning Documentation) |
| GraphRAG | P-001 (Truth/Accuracy via grounding) |
| Cynefin | P-001 (Truth/Accuracy in problem classification) |
| 5 Whys | P-004 (Reasoning Documentation) |
| PDCA | P-010 (Task Tracking Integrity via cycles) |

**Avoiding Constitutional Violations:**

- **P-003 (No Recursive Subagents)**: ReAct actions must be tools, not recursive agent calls
- **P-020 (User Authority)**: Cynefin/Framework selection recommendations, not mandates
- **P-022 (No Deception)**: CoT/ReAct reasoning traces must be honest, expose uncertainty

---

### Recommended Implementation Roadmap

**Phase 1: Foundation (Immediate)**
1. Create `problem-classifier` skill using Cynefin
2. Implement A3 template in `.claude/templates/`
3. Document SECI mapping in `docs/knowledge/seci-mapping.md`

**Phase 2: AI Augmentation (Next)**
4. Formalize ReAct pattern in `problem-solving` skill
5. Implement standard RAG over `docs/` with vector database
6. Create `knowledge-query` skill for semantic search

**Phase 3: Advanced (Future)**
7. Build GraphRAG knowledge graph from Jerry's docs
8. Develop `framework-selector` agent that recommends frameworks
9. Create framework effectiveness metrics (which frameworks led to best outcomes?)

**Phase 4: Optimization (Ongoing)**
10. Continuous refinement based on usage patterns
11. Archive completed A3s and extract patterns
12. Update Jerry Constitution based on framework learnings

---

## Framework Comparison Matrix

### Overview Matrix: All 16 Frameworks

| Framework | Category | Origin Year | Complexity | Time to Apply | Best For | Primary Output |
|-----------|----------|-------------|------------|---------------|----------|----------------|
| **SECI** | KM | 1995 | Medium | Ongoing | Knowledge flow | Knowledge artifacts |
| **Wiig** | KM | 1993 | Medium | Days-Weeks | Knowledge audit | Competency model |
| **Boisot I-Space** | KM | 1995 | High | Weeks | IP strategy | Knowledge map |
| **Cynefin** | KM | 1999 | Low | Minutes | Problem classification | Domain assignment |
| **TRIZ** | Problem-Solving | 1946 | Very High | Days-Weeks | Technical innovation | Inventive solution |
| **Design Thinking** | Problem-Solving | 1990s | Medium | Days-Weeks | User-centric innovation | Prototype |
| **Systems Thinking** | Problem-Solving | 1940s-1990s | High | Weeks-Months | Complex systems | System map |
| **5 Whys / Ishikawa** | Problem-Solving | 1920s-1960s | Low | Hours | Root cause analysis | Cause diagram |
| **OODA Loop** | Decision | 1970s | Low | Seconds-Minutes | Rapid decisions | Action |
| **Kepner-Tregoe** | Decision | 1965 | High | Days | High-stakes decisions | Decision record |
| **PDCA** | Decision | 1920s-1950s | Low | Weeks (per cycle) | Continuous improvement | Standardized process |
| **A3** | Decision | 1960s | Medium | Hours-Days | Structured problem-solving | One-page report |
| **RAG** | AI-Era | 2020+ | Medium | Setup: Days, Query: Seconds | Domain-specific Q&A | Grounded answer |
| **GraphRAG** | AI-Era | 2024 | High | Setup: Weeks, Query: Seconds | Complex knowledge exploration | Graph-based answer |
| **Chain-of-Thought** | AI-Era | 2022 | Low | Seconds | Reasoning transparency | Reasoning trace |
| **ReAct** | AI-Era | 2023 | Medium | Seconds-Minutes | Agentic tasks | Action sequence |

---

### Detailed Comparison by Dimension

#### 1. Problem Type Suitability

| Framework | Technical | Organizational | Strategic | Operational | Creative | Analytical |
|-----------|-----------|----------------|-----------|-------------|----------|------------|
| SECI | ● | ●●● | ●● | ●● | ● | ● |
| Wiig | ● | ●●● | ●● | ●● | ○ | ●● |
| Boisot I-Space | ● | ●● | ●●● | ○ | ● | ●● |
| Cynefin | ●● | ●●● | ●●● | ●● | ●● | ●● |
| TRIZ | ●●● | ○ | ● | ● | ●●● | ●● |
| Design Thinking | ●● | ●● | ●● | ● | ●●● | ● |
| Systems Thinking | ●● | ●●● | ●●● | ●● | ●● | ●●● |
| 5 Whys / Ishikawa | ●●● | ●● | ○ | ●●● | ○ | ●●● |
| OODA Loop | ●● | ●● | ●●● | ●●● | ● | ●● |
| Kepner-Tregoe | ●●● | ●● | ●● | ●● | ○ | ●●● |
| PDCA | ●● | ●● | ○ | ●●● | ○ | ●● |
| A3 | ●●● | ●● | ● | ●●● | ○ | ●●● |
| RAG | ●● | ●● | ○ | ●● | ○ | ●● |
| GraphRAG | ●● | ●● | ●●● | ● | ● | ●●● |
| Chain-of-Thought | ●●● | ● | ○ | ●● | ● | ●●● |
| ReAct | ●●● | ●● | ● | ●●● | ● | ●●● |

**Legend:** ●●● Excellent fit | ●● Good fit | ● Some fit | ○ Limited fit

---

#### 2. Knowledge Type Addressed

| Framework | Tacit | Explicit | Procedural | Declarative | Contextual |
|-----------|-------|----------|------------|-------------|------------|
| SECI | ●●● | ●●● | ●● | ●● | ●●● |
| Wiig | ●● | ●●● | ●● | ●●● | ● |
| Boisot I-Space | ●●● | ●●● | ● | ●● | ●●● |
| Cynefin | ● | ●● | ●● | ●● | ●●● |
| TRIZ | ● | ●●● | ●●● | ●● | ● |
| Design Thinking | ●●● | ●● | ●●● | ● | ●●● |
| Systems Thinking | ●● | ●● | ●● | ●● | ●●● |
| 5 Whys / Ishikawa | ● | ●● | ●● | ●●● | ●● |
| OODA Loop | ●● | ●● | ●●● | ●● | ●●● |
| Kepner-Tregoe | ● | ●●● | ●●● | ●●● | ●● |
| PDCA | ● | ●●● | ●●● | ●● | ● |
| A3 | ●● | ●●● | ●●● | ●●● | ●● |
| RAG | ○ | ●●● | ● | ●●● | ●● |
| GraphRAG | ○ | ●●● | ● | ●●● | ●●● |
| Chain-of-Thought | ○ | ●●● | ●●● | ●● | ● |
| ReAct | ○ | ●●● | ●●● | ●● | ●● |

---

#### 3. Implementation Requirements

| Framework | Training Needed | Tool Support | Cultural Change | Cost | Scalability |
|-----------|----------------|--------------|-----------------|------|-------------|
| SECI | Medium | Low | High | Low | High |
| Wiig | Medium | Low | Medium | Low | High |
| Boisot I-Space | High | Low | Medium | Low | Medium |
| Cynefin | Low | Low | Medium | Low | High |
| TRIZ | Very High | Medium | Medium | Medium | Medium |
| Design Thinking | Medium | Low | High | Low | High |
| Systems Thinking | High | Medium | High | Low | Medium |
| 5 Whys / Ishikawa | Low | Low | Low | Low | High |
| OODA Loop | Low | Low | Medium | Low | High |
| Kepner-Tregoe | High | Low | Medium | Medium | Medium |
| PDCA | Low | Low | Medium | Low | High |
| A3 | Medium | Low | High | Low | High |
| RAG | Medium | High | Low | Medium-High | High |
| GraphRAG | High | Very High | Low | High-Very High | Medium |
| Chain-of-Thought | Low | Medium | Low | Medium | High |
| ReAct | Medium | High | Low | Medium-High | High |

---

#### 4. Strengths & Weaknesses Summary

| Framework | Key Strength | Key Weakness | Best Alternative |
|-----------|--------------|--------------|------------------|
| SECI | Captures tacit knowledge flow | Requires knowledge-sharing culture | Wiig (more structured) |
| Wiig | Clear knowledge maturity levels | Less focus on tacit knowledge | SECI (tacit emphasis) |
| Boisot I-Space | 3D knowledge mapping | Abstract, hard to operationalize | SECI (more actionable) |
| Cynefin | Fast problem classification | Domain boundaries can be fuzzy | None (unique purpose) |
| TRIZ | Systematic innovation from patterns | Steep learning curve | Design Thinking (more accessible) |
| Design Thinking | Human-centered creativity | Time-intensive | TRIZ (faster if trained) |
| Systems Thinking | Reveals hidden dynamics | Can lead to analysis paralysis | Cynefin (faster sense-making) |
| 5 Whys / Ishikawa | Simple, fast root cause analysis | May oversimplify complex issues | Kepner-Tregoe (rigorous) |
| OODA Loop | Speed and adaptability | Can be oversimplified | Kepner-Tregoe (high-stakes) |
| Kepner-Tregoe | Rigorous, logical decision-making | Time-intensive | OODA (speed) or A3 (balance) |
| PDCA | Continuous improvement mindset | Slow for urgent problems | OODA (rapid action) |
| A3 | Concise, combines solving + docs | One page can feel constraining | Kepner-Tregoe (more detail) |
| RAG | Grounds LLM in current knowledge | Retrieval quality critical | GraphRAG (complex queries) |
| GraphRAG | Multi-hop reasoning, exploration | Expensive, complex setup | RAG (simpler/cheaper) |
| Chain-of-Thought | Transparent reasoning | Only works with large LLMs | ReAct (adds grounding) |
| ReAct | Grounds reasoning in actions/data | Multiple LLM calls (latency, cost) | RAG (single retrieval) |

---

#### 5. Integration Compatibility Matrix

Which frameworks work well together?

| Framework Pair | Synergy Level | How They Complement |
|----------------|---------------|---------------------|
| Cynefin + Any | ●●● | Cynefin classifies, then apply domain-appropriate framework |
| SECI + A3 | ●●● | A3 externalizes (SECI step), completed A3s are combination |
| SECI + ReAct | ●●● | ReAct reasoning traces externalize tacit knowledge |
| ReAct + RAG | ●●● | ReAct decides when to retrieve (RAG provides retrieval) |
| RAG + GraphRAG | ●● | Start with RAG, upgrade to GraphRAG for complex needs |
| Chain-of-Thought + ReAct | ●●● | CoT provides reasoning, ReAct adds grounding via actions |
| A3 + PDCA | ●●● | A3 documents each PDCA cycle |
| A3 + 5 Whys | ●●● | 5 Whys in A3 section 4 (root cause analysis) |
| Systems Thinking + Cynefin | ●●● | Cynefin for classification, Systems for complex domain |
| TRIZ + Design Thinking | ●● | TRIZ for technical solutions, Design Thinking for user validation |
| OODA + Cynefin | ●●● | Cynefin for domain, OODA for chaotic domain response |
| Kepner-Tregoe + A3 | ●● | K-T for analysis rigor, A3 for documentation brevity |
| Wiig + SECI | ●● | Wiig for auditing, SECI for flow management |
| Boisot + GraphRAG | ●● | Both model knowledge as networks/spaces |

**Legend:** ●●● Highly synergistic | ●● Complementary | ● Compatible with effort

---

## Full Citations & References

### Classic Knowledge Management Frameworks

**SECI Model:**
1. Managing Knowledge in Organizations: A Nonaka's SECI Model Operationalization - PMC. (2019). https://pmc.ncbi.nlm.nih.gov/articles/PMC6914727/
2. SECI model of knowledge dimensions. Wikipedia. https://en.wikipedia.org/wiki/SECI_model_of_knowledge_dimensions
3. SECI Model of Knowledge Dimensions (Nonaka & Takeuchi). ToolsHero. https://www.toolshero.com/quality-management/seci-model-nonaka-takeuchi/
4. Nonaka, I., & Takeuchi, H. (1995). *The Knowledge-Creating Company: How Japanese Companies Create the Dynamics of Innovation*. Oxford University Press.

**Wiig Model:**
1. The Wiig Model for Building and Using Knowledge. Theoretical Models of Information and Knowledge Management. https://www.tlu.ee/~sirvir/IKM/Theoretical_models_of_Information_and_Knowledge_Management/the_wiig_model_for_building_and_using_knowledge.html
2. 4 Knowledge Management Models That Can Supercharge Your Organisation. HelpieWP. https://helpiewp.com/knowledge-management-models/
3. Garfield, S. (2020). Karl Wiig: Profiles in Knowledge. Medium. https://stangarfield.medium.com/karl-wiig-profiles-in-knowledge-cb09e2c9088e
4. Wiig, K. M. (1993). *Knowledge Management Foundations: Thinking about Thinking - How People and Organizations Create, Represent and Use Knowledge*. Schema Press.

**Boisot I-Space:**
1. The Boisot I-Space KM Model. Theoretical Models of Information and Knowledge Management. https://www.tlu.ee/~sirvir/IKM/Theoretical_models_of_Information_and_Knowledge_Management/the_boisot_ispace_km_model.html
2. Garfield, S. (2020). Max Boisot: Profiles in Knowledge. Medium. https://stangarfield.medium.com/max-boisot-profiles-in-knowledge-fdfd3352c1e5
3. Navigating Information Flow: A Deep Dive into Max Boisot's I-Space. (2024). https://conikeec.substack.com/p/navigating-the-information-space
4. Boisot, M. H. (1995). *Information Space: A Framework for Learning in Organizations, Institutions and Culture*. Routledge.

**Cynefin Framework:**
1. Cynefin framework. Wikipedia. https://en.wikipedia.org/wiki/Cynefin_framework
2. Snowden, D. J., & Boone, M. E. (2007). A Leader's Framework for Decision Making. *Harvard Business Review*, 85(11), 68-76. https://hbr.org/2007/11/a-leaders-framework-for-decision-making
3. About Cynefin Framework. The Cynefin Co. https://thecynefin.co/about-us/about-cynefin-framework/
4. The Cynefin Framework. MindTools. https://www.mindtools.com/atddimk/the-cynefin-framework/

### Problem-Solving Frameworks

**TRIZ:**
1. TRIZ. Wikipedia. https://en.wikipedia.org/wiki/TRIZ
2. TRIZ: The Backbone of Innovation and Problem-Solving. *Quality Magazine*. (2024). https://www.qualitymag.com/articles/98566-triz-the-backbone-of-innovation-and-problem-solving
3. What is TRIZ? TRIZ.co.uk. https://www.triz.co.uk/what-is-triz
4. Can the Theory of Inventive Problem Solving Help You? NASA APPEL Knowledge Services. (2010). https://appel.nasa.gov/2010/02/23/aa_1-10_f_inventive-html/
5. Altshuller, G. S. (1999). *The Innovation Algorithm: TRIZ, Systematic Innovation and Technical Creativity*. Technical Innovation Center.

**Design Thinking:**
1. Pacheco, J. F. (2025). What is Design Thinking? Stanford d.school Model. https://juanfernandopacheco.com/2025/01/what-is-design-thinking-stanford-d-school-model/
2. Design Thinking by Stanford d.school and IDEO. Wind4Change. https://wind4change.com/design-thinking-d-school-stanford-ideo-approach-methodology/
3. What is Design Thinking? Interaction Design Foundation. https://www.interaction-design.org/literature/topics/design-thinking
4. Brown, T. (2008). Design Thinking. *Harvard Business Review*, 86(6), 84-92.

**Systems Thinking:**
1. Zhang, L., & Ahmed, A. A. (2020). Systems Thinking—Ludwig Von Bertalanffy, Peter Senge, and Donella Meadows. In *Springer Handbook of Engineering Systems*. Springer. https://link.springer.com/chapter/10.1007/978-3-030-43620-9_28
2. Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green Publishing. https://research.fit.edu/media/site-specific/researchfitedu/coast-climate-adaptation-library/climate-communications/psychology-amp-behavior/Meadows-2008.-Thinking-in-Systems.pdf
3. Demystifying Systems Thinking. Cambridge Institute for Sustainability Leadership. https://www.cisl.cam.ac.uk/files/cisl_primer_demystifying_systems_thinking.pdf
4. Senge, P. M. (1990). *The Fifth Discipline: The Art and Practice of the Learning Organization*. Doubleday.

**Root Cause Analysis (5 Whys / Ishikawa):**
1. Root Cause and Effect Analysis: 5 Whys vs. Fishbone. EasyRCA. https://easyrca.com/blog/root-cause-and-effect-analysis-5-whys-vs-fishbone/
2. Ishikawa diagram. Wikipedia. https://en.wikipedia.org/wiki/Ishikawa_diagram
3. Root Cause Analysis: Integrating Ishikawa Diagrams and the 5 Whys. iSixSigma. https://www.isixsigma.com/cause-effect/root-cause-analysis-ishikawa-diagrams-and-the-5-whys/
4. Cause and Effect Analysis: Using Fishbone Diagram and 5 Whys. Visual Paradigm. https://www.visual-paradigm.com/project-management/fishbone-diagram-and-5-whys/

### Decision Frameworks

**OODA Loop:**
1. OODA loop. Wikipedia. https://en.wikipedia.org/wiki/OODA_loop
2. The OODA Loop. The Decision Lab. https://thedecisionlab.com/reference-guide/computer-science/the-ooda-loop
3. The OODA Loop Explained: The real story about the ultimate model for decision-making in competitive environments. OODAloop.com. https://oodaloop.com/the-ooda-loop-explained-the-real-story-about-the-ultimate-model-for-decision-making-in-competitive-environments/
4. The OODA Loop: How Fighter Pilots Make Fast and Accurate Decisions. Farnam Street. https://fs.blog/ooda-loop/
5. Boyd, J. R. (1976). *Destruction and Creation*. U.S. Army Command and General Staff College.

**Kepner-Tregoe:**
1. The Kepner-Tregoe Matrix. MindTools. https://www.mindtools.com/atznth6/the-kepner-tregoe-matrix/
2. Kepner Tregoe Method of Problem Solving. ToolsHero. https://www.toolshero.com/problem-solving/kepner-tregoe-method/
3. Kepner‑Tregoe: A Structured and Rational Approach to Problem Solving and Decision‑Making. Microsoft Community Hub. (2024). https://techcommunity.microsoft.com/blog/azuredbsupport/kepner%E2%80%91tregoe-a-structured-and-rational-approach-to-problem-solving-and-decision/4482643
4. Kepner, C. H., & Tregoe, B. B. (1965). *The Rational Manager: A Systematic Approach to Problem Solving and Decision Making*. McGraw-Hill.

**PDCA Cycle:**
1. PDCA Cycle - What is the Plan-Do-Check-Act Cycle? ASQ. https://asq.org/quality-resources/pdca-cycle
2. PDCA. Wikipedia. https://en.wikipedia.org/wiki/PDCA
3. PDSA Cycle. The W. Edwards Deming Institute. https://deming.org/explore/pdsa/
4. The Deming Cycle (PDCA) Explained: A Comprehensive Guide to Continuous Improvement. Brightly Software. https://www.brightlysoftware.com/learning-center/the-deming-cycle-pdca-explained-a-comprehensive-guide-to-continuous-improvement
5. Deming, W. E. (1986). *Out of the Crisis*. MIT Press.

**A3 Problem Solving:**
1. A3 problem solving. Wikipedia. https://en.wikipedia.org/wiki/A3_problem_solving
2. Sobek, D. K., & Smalley, A. (2008). Toyota's Secret: The A3 Report. *MIT Sloan Management Review*, 49(4). https://sloanreview.mit.edu/article/toyotas-secret-the-a3-report/
3. What is A3 Problem Solving? Kanban Tool. https://kanbantool.com/kanban-guide/a3-problem-solving
4. How to use Toyota's legendary A3 problem solving technique. Nulab. https://nulab.com/learn/project-management/use-toyotas-legendary-a3-problem-solving-technique/

### AI-Era Frameworks

**RAG (Retrieval Augmented Generation):**
1. Retrieval Augmented Generation (RAG) for LLMs. Prompt Engineering Guide. https://www.promptingguide.ai/research/rag
2. What is RAG? - Retrieval-Augmented Generation AI Explained. AWS. https://aws.amazon.com/what-is/retrieval-augmented-generation/
3. Retrieval-augmented generation. Wikipedia. https://en.wikipedia.org/wiki/Retrieval-augmented_generation
4. RAG in 2025: Bridging Knowledge and Generative AI. Squirro. https://squirro.com/squirro-blog/state-of-rag-genai
5. Boulahia, H. (2025). All You Need To Know About Retrieval-Augmented Generation (RAG) in 2025. *Towards AI*. https://pub.towardsai.net/all-you-need-to-know-about-retrieval-augmented-generation-rag-in-2025-04c386284c18
6. Gao, Y., et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. *arXiv preprint* arXiv:2312.10997. https://arxiv.org/abs/2312.10997

**GraphRAG:**
1. Welcome - GraphRAG. Microsoft GraphRAG Documentation. https://microsoft.github.io/graphrag/
2. microsoft/graphrag. GitHub. https://github.com/microsoft/graphrag
3. Project GraphRAG. Microsoft Research. https://www.microsoft.com/en-us/research/project/graphrag/
4. GraphRAG: Unlocking LLM discovery on narrative private data. Microsoft Research Blog. https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/
5. GraphRAG Explained: Enhancing RAG with Knowledge Graphs. Zilliz/Medium. (2024). https://medium.com/@zilliz_learn/graphrag-explained-enhancing-rag-with-knowledge-graphs-3312065f99e1

**Chain-of-Thought (CoT) Prompting:**
1. Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *arXiv preprint* arXiv:2201.11903. https://arxiv.org/abs/2201.11903
2. Chain-of-Thought Prompting. Learn Prompting. https://learnprompting.org/docs/intermediate/chain_of_thought
3. What is chain of thought (CoT) prompting? IBM. https://www.ibm.com/think/topics/chain-of-thoughts
4. Chain-of-Thought Prompting. Prompt Engineering Guide. https://www.promptingguide.ai/techniques/cot

**ReAct (Reasoning + Acting):**
1. Yao, S., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *arXiv preprint* arXiv:2210.03629. https://arxiv.org/abs/2210.03629
2. ReAct: Synergizing Reasoning and Acting in Language Models. Google Research Blog. https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/
3. What is a ReAct Agent? IBM. https://www.ibm.com/think/topics/react-agent
4. ReAct Prompting. Prompt Engineering Guide. https://www.promptingguide.ai/techniques/react
5. ReAct: Synergizing Reasoning and Acting in Language Models. Official Site. https://react-lm.github.io/

---

## Appendix: Quick Reference Cards

### For Agent Use: Framework Selection Flowchart

```
START: User presents problem/request
    ↓
┌─────────────────────────────────────┐
│ STEP 1: Classify with Cynefin       │
│ - Clear? → Best practices apply     │
│ - Complicated? → Expert analysis    │
│ - Complex? → Experiment & probe     │
│ - Chaotic? → Act to stabilize       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 2: Select Framework            │
│                                      │
│ Clear Domain:                        │
│   → A3, PDCA, 5 Whys                │
│                                      │
│ Complicated Domain:                  │
│   → Kepner-Tregoe, TRIZ, Ishikawa   │
│                                      │
│ Complex Domain:                      │
│   → Systems Thinking, Design Thinking│
│   → ReAct + GraphRAG                 │
│                                      │
│ Chaotic Domain:                      │
│   → OODA Loop                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 3: Apply SECI for Knowledge    │
│ - Externalize: Document reasoning    │
│ - Combine: Cross-reference docs      │
│ - Share: Update relevant docs/       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 4: Create A3 if Significant    │
│ - Capture problem-solving process    │
│ - Store in docs/a3/                  │
└─────────────────────────────────────┘
    ↓
END: Problem solved + Knowledge captured
```

---

### Jerry-Specific Quick Decisions

**Use This Framework When:**

- **Cynefin**: First thing, every time (classify before solving)
- **A3**: Problem took >2 hours or likely to recur
- **ReAct**: Need to search/retrieve external knowledge
- **5 Whys**: Bug or failure requiring root cause
- **PDCA**: Iterative improvement of known process
- **SECI**: Deciding where/how to document knowledge
- **GraphRAG**: Complex query across multiple docs (future)

**Don't Use (Outside Jerry's Scope):**

- **TRIZ**: Unless hardware/physical system involved
- **Design Thinking**: Unless user research phase explicitly requested
- **Wiig**: Too organizational, Jerry is individual/team scale
- **Boisot**: Too abstract for operational use

---

### Constitutional Compliance Checklist

Before finalizing framework application:

- [ ] **P-001**: Information accurate and sourced? (especially with RAG/GraphRAG)
- [ ] **P-002**: Significant outputs persisted to filesystem?
- [ ] **P-003**: No recursive agent calls (only tools in ReAct)?
- [ ] **P-004**: Reasoning documented (CoT traces, A3, etc.)?
- [ ] **P-010**: Work Tracker updated with progress?
- [ ] **P-020**: User authority respected (recommendations, not mandates)?
- [ ] **P-022**: Transparent about limitations and confidence?

---

## Conclusion

This research provides a comprehensive catalog of 16 knowledge management and problem-solving frameworks spanning from 1946 (TRIZ) to 2024 (GraphRAG). The analysis reveals that effective knowledge work requires a **layered framework stack** rather than a single approach:

1. **Classification layer** (Cynefin) to match context with appropriate methods
2. **Knowledge flow layer** (SECI) to manage tacit ↔ explicit conversion
3. **AI augmentation layer** (ReAct + GraphRAG) to leverage LLM capabilities with grounding
4. **Documentation layer** (A3) to capture learnings systematically

For Jerry, this stack aligns with architectural strengths (filesystem-as-memory, agent patterns) while addressing core challenges (context rot, knowledge retention). The recommended implementation roadmap provides a phased approach from immediate foundational work to future advanced capabilities.

The framework comparison matrix enables evidence-based selection based on problem type, knowledge type, implementation requirements, and integration compatibility. By embedding these frameworks into Jerry's skills and workflows, the system can systematically improve its problem-solving effectiveness while accruing reusable knowledge, wisdom, and experience.

**File:** `/home/user/jerry/docs/research/work-032-e-005-km-frameworks.md`
**Status:** Complete
**Word Count:** ~13,500 words
**Framework Coverage:** 16/16 (100%)

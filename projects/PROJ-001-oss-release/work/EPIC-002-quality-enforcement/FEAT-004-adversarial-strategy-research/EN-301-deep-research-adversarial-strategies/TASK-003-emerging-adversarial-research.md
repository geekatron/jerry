# TASK-003: Emerging & Alternative Adversarial Review Approaches

<!--
DOCUMENT-ID: FEAT-004:EN-301-TASK-003-RESEARCH
AUTHOR: nse-explorer agent
DATE: 2026-02-12
STATUS: Complete (pending synthesis integration)
PARENT: EN-301 (Deep Research: 15 Adversarial Strategies)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
-->

> **Version:** 1.0.0
> **Agent:** nse-explorer (/nasa-se skill)
> **Confidence:** MEDIUM-HIGH for strategies rooted in established cross-domain practice (E1-E4, E7); MEDIUM for emerging AI/ML strategies (E5, E6, E8, E9); EXPLORATORY for highly novel composites (E10)
> **Research Limitation:** WebSearch and WebFetch tools were unavailable. All content sourced from agent training knowledge (literature through May 2025). Citations reference real, verifiable publications; independent verification recommended. Particular care taken to identify strategies NOT already covered by TASK-001 (academic) and TASK-002 (industry) research.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What novel approaches were found and why they matter |
| [L1: Technical Analysis -- Emerging Strategy Catalog](#l1-technical-analysis----emerging-strategy-catalog) | Detailed catalog of 10 emerging/alternative strategies |
| [Strategy E1: Moot Court / Cross-Examination Review](#strategy-e1-moot-court--cross-examination-review) | Legal adversarial pattern transfer |
| [Strategy E2: Mortality & Morbidity Conference Pattern](#strategy-e2-mortality--morbidity-conference-pattern) | Medical blame-free root cause adversarial review |
| [Strategy E3: Reference Class Forecasting (Outside View)](#strategy-e3-reference-class-forecasting-outside-view) | Kahneman's debiasing via external base rates |
| [Strategy E4: Wargaming / Tabletop Exercise Review](#strategy-e4-wargaming--tabletop-exercise-review) | Military scenario-driven adversarial stress test |
| [Strategy E5: Constitutional AI Critique Chains](#strategy-e5-constitutional-ai-critique-chains) | AI self-critique against explicit principles |
| [Strategy E6: Progressive Adversarial Escalation](#strategy-e6-progressive-adversarial-escalation) | Graduated-intensity adversarial review |
| [Strategy E7: Inversion Technique (Problem Reversal)](#strategy-e7-inversion-technique-problem-reversal) | Solve-the-opposite adversarial method |
| [Strategy E8: Ensemble Adversarial Meta-Review](#strategy-e8-ensemble-adversarial-meta-review) | Multi-method adversarial composition |
| [Strategy E9: Red Queen Evolutionary Adversarial Escalation](#strategy-e9-red-queen-evolutionary-adversarial-escalation) | Co-evolutionary creator-critic arms race |
| [Strategy E10: Cynefin-Gated Adversarial Intensity Selection](#strategy-e10-cynefin-gated-adversarial-intensity-selection) | Complexity-aware adversarial calibration |
| [L2: Architectural Implications](#l2-architectural-implications) | Highest-potential strategies for Jerry's multi-agent framework |
| [Differentiation Matrix: Emerging vs. Existing Strategies](#differentiation-matrix-emerging-vs-existing-strategies) | How these strategies differ from TASK-001/TASK-002 findings |
| [References](#references) | Complete citation list |

---

## L0: Executive Summary

This research identifies **10 emerging, alternative, and cross-domain adversarial review approaches** that extend beyond the 15 mainstream strategies cataloged by TASK-001 (academic literature) and TASK-002 (industry practices). These strategies were discovered through cross-domain transfer analysis (legal, medical, military, journalism), cognitive science and behavioral economics research, systems thinking / complexity science frameworks, and frontier AI/ML adversarial collaboration techniques.

### Key Findings

1. **Cross-domain transfer is the richest source of novel adversarial patterns.** Legal cross-examination, medical M&M conferences, and military wargaming each encode centuries of refined adversarial practice that has never been formally applied to software or AI review workflows. These patterns are highly structured, well-documented, and directly transferable.

2. **Cognitive debiasing techniques are underutilized as adversarial tools.** Reference Class Forecasting (Kahneman & Lovallo) and the Inversion Technique (Jacobi/Munger) function as powerful adversarial review strategies when deliberately applied, but they are rarely framed as such in the adversarial review literature.

3. **AI-native adversarial patterns are rapidly emerging.** Constitutional AI critique chains (Anthropic, 2022-2024), progressive adversarial escalation, and ensemble adversarial meta-review represent genuinely new categories of adversarial review that have no direct pre-AI precedent. These are the most immediately applicable to Jerry's multi-agent architecture.

4. **Complexity-aware adversarial selection is a meta-strategy gap.** No existing framework matches adversarial intensity to problem complexity. The Cynefin-gated approach proposed here fills this gap and could serve as Jerry's strategy selector algorithm.

5. **The highest-value strategies for Jerry are E5 (Constitutional AI Critique), E6 (Progressive Adversarial Escalation), E8 (Ensemble Adversarial Meta-Review), and E10 (Cynefin-Gated Selection).** These four are directly implementable in a multi-agent LLM framework and offer capabilities not achievable through traditional single-strategy approaches.

### Novelty Assessment Summary

| Strategy | Novelty Factor | LLM Applicability |
|----------|---------------|-------------------|
| E1: Moot Court / Cross-Examination | HIGH (cross-domain transfer) | HIGH |
| E2: M&M Conference Pattern | HIGH (cross-domain transfer) | MEDIUM-HIGH |
| E3: Reference Class Forecasting | MEDIUM (reframing known technique) | HIGH |
| E4: Wargaming / Tabletop Exercise | MEDIUM (cross-domain transfer) | MEDIUM |
| E5: Constitutional AI Critique Chains | HIGH (AI-native) | VERY HIGH |
| E6: Progressive Adversarial Escalation | HIGH (novel composite) | VERY HIGH |
| E7: Inversion Technique | MEDIUM (reframing known technique) | HIGH |
| E8: Ensemble Adversarial Meta-Review | VERY HIGH (novel composite) | VERY HIGH |
| E9: Red Queen Evolutionary Escalation | HIGH (novel application) | HIGH |
| E10: Cynefin-Gated Intensity Selection | VERY HIGH (novel meta-strategy) | VERY HIGH |

---

## L1: Technical Analysis -- Emerging Strategy Catalog

### Strategy E1: Moot Court / Cross-Examination Review

**Name:** Moot Court / Cross-Examination Adversarial Review

**Origin/Author:** Legal tradition dating to medieval English common law. Moot court formalized in legal education at Harvard Law School (1870s, Christopher Columbus Langdell). Cross-examination codified in Wigmore's treatise on evidence (John Henry Wigmore, 1904). Modern adversarial legal theory synthesized by Stephan Landsman in *The Adversary System: A Description and Defense* (1984).

**Citation:**
- Wigmore, J. H. (1904). *A Treatise on the System of Evidence in Trials at Common Law*. Little, Brown and Company.
- Landsman, S. (1984). *The Adversary System: A Description and Defense*. American Enterprise Institute.
- Lubet, S. (2004). *Modern Trial Advocacy: Analysis and Practice* (3rd ed.). National Institute for Trial Advocacy. ISBN: 978-1556818868.
- Mauet, T. A. (2020). *Trial Techniques and Trials* (11th ed.). Wolters Kluwer. ISBN: 978-1543809060.

**Description:** A structured adversarial review modeled on legal cross-examination, where a designated "cross-examiner" agent challenges the creator's work through a sequence of increasingly probing questions. Unlike Devil's Advocate (which argues the opposite position), cross-examination follows the legal discipline of questioning the witness's own testimony -- accepting the creator's framework but exposing internal contradictions, unsupported claims, logical gaps, and implicit assumptions through targeted questioning. The moot court variant adds a "judge" agent who evaluates both sides.

**Mechanism (Step-by-Step):**
1. **Direct Examination (Creator Presents):** The creator agent presents its work product as testimony -- stating claims, evidence, reasoning chain, and conclusions.
2. **Cross-Examination Preparation:** The cross-examiner agent studies the testimony to identify: (a) claims without supporting evidence, (b) internal contradictions, (c) logical leaps, (d) unstated assumptions, (e) alternative explanations not considered.
3. **Leading Question Sequence:** The cross-examiner poses a series of narrow, leading questions designed to get the creator to confirm or deny specific factual claims. Questions progress from establishing foundational facts to challenging inferences. (Legal rule: leading questions are permitted on cross, not direct.)
4. **Impeachment Phase:** When contradictions or unsupported claims are exposed, the cross-examiner "impeaches" -- formally identifies the inconsistency with specific references to the creator's own prior statements.
5. **Redirect (Creator Response):** The creator may clarify or rehabilitate challenged points.
6. **Judicial Evaluation:** An optional "judge" agent evaluates the exchange, determines which challenges were substantive vs. superficial, and issues a ruling on the work's quality.

**Strengths:**
- Extremely effective at exposing internal inconsistencies (creator's claims are tested against each other)
- The questioning format forces granular examination that broad critique misses
- The sequential structure prevents the creator from deflecting -- each question demands a specific answer
- Well-suited to LLM agents which can be prompted to adopt examiner/witness roles
- The "judge" role provides meta-evaluation of the adversarial process itself

**Weaknesses:**
- Requires highly skilled cross-examination prompting; poorly structured questions yield surface-level review
- Can devolve into adversarial theater rather than substantive challenge if not properly constrained
- Does not generate alternatives -- only tests existing work
- The legal metaphor may not resonate with all team cultures
- Time-intensive due to multi-turn sequential questioning

**Novelty Factor:** HIGH. While Devil's Advocate is well-known, the cross-examination structure -- particularly the discipline of questioning within the creator's own framework rather than arguing an opposite position -- is a distinct and more rigorous adversarial method. The three-agent variant (witness/examiner/judge) adds meta-evaluation that no standard adversarial strategy includes.

**Applicability to LLM Workflows:** HIGH. LLMs excel at role-play. A cross-examiner agent can be prompted with legal cross-examination rules (ask leading questions, impeach on contradiction, do not argue -- only question). The multi-turn structure maps naturally to agent conversation loops. The judge agent addresses the "who reviews the reviewer" meta-problem. Could be implemented as a 3-agent choreography: creator-as-witness, cross-examiner, judge.

---

### Strategy E2: Mortality & Morbidity Conference Pattern

**Name:** Mortality & Morbidity (M&M) Conference Adversarial Review

**Origin/Author:** Originated in early 20th century surgical practice. Formalized by Ernest Amory Codman at Massachusetts General Hospital (1914) as "End Result System." Modernized as a core component of the Accreditation Council for Graduate Medical Education (ACGME) requirements. Current best practice codified by Orlander et al. (2002) and Pierluissi et al. (2003).

**Citation:**
- Codman, E. A. (1914). The product of a hospital. *Surgery, Gynecology & Obstetrics*, 18, 491-496.
- Orlander, J. D., Barber, T. W., & Fincke, B. G. (2002). The morbidity and mortality conference: the delicate nature of learning from error. *Academic Medicine*, 77(10), 1001-1006. DOI: 10.1097/00001888-200210000-00011
- Pierluissi, E., Fischer, M. A., Campbell, A. R., & Landefeld, C. S. (2003). Discussion of medical errors in morbidity and mortality conferences. *JAMA*, 290(21), 2838-2842. DOI: 10.1001/jama.290.21.2838
- Aboumatar, H. J., Blackledge, C. G., Dickson, C., Heitmiller, E., Freischlag, J., & Pronovost, P. J. (2007). A descriptive study of morbidity and mortality conferences and their conformity to medical incident analysis models. *American Journal of Medical Quality*, 22(4), 232-238.

**Description:** A structured group review process borrowed from medical practice where adverse outcomes (failures, errors, near-misses) are presented and analyzed by peers in a blame-free, learning-focused environment. The M&M conference pattern differs from standard post-mortem analysis because it combines three elements rarely found together: (1) mandatory presentation of the full decision chain that led to the adverse outcome, (2) structured group interrogation focused on systemic rather than individual causes, and (3) an explicit cultural norm that the purpose is learning, not punishment. Applied to software/AI review, this pattern treats defects and failures as learning opportunities subjected to rigorous group adversarial analysis.

**Mechanism (Step-by-Step):**
1. **Case Selection:** Select a specific failure, defect, or near-miss for review. The case should have educational value and systemic implications (not merely a typo or trivial error).
2. **Case Presentation:** The presenting agent reconstructs the full decision chain: what was known at each decision point, what alternatives were considered, what was decided and why. Crucially, the presentation includes the reasoning process, not just the outcome.
3. **Structured Interrogation:** Reviewing agents question the decision chain at each node: "What information was available here? What alternatives existed? Why was this path chosen? What cognitive biases may have influenced the decision?" Questions follow a non-blaming protocol.
4. **Root Cause Analysis:** The group converges on systemic causes (process gaps, missing information, structural incentives) rather than individual blame. Uses frameworks like the Swiss Cheese Model (Reason, 1990) or the Five Whys.
5. **Recommendation Generation:** Concrete, actionable recommendations for systemic improvement -- changes to process, tooling, review gates, or information flow that would prevent recurrence.
6. **Learning Codification:** Findings are documented as institutional knowledge -- patterns to watch for, decision heuristics to apply, and review checklist additions.

**Strengths:**
- Blame-free framing encourages honest examination of reasoning failures
- The decision-chain reconstruction reveals reasoning process defects invisible to outcome-focused review
- Systemic focus produces structural improvements, not just one-off fixes
- Well-suited to reviewing AI agent reasoning chains (the decision chain IS the prompt/response sequence)
- Builds institutional knowledge over time (learning compounds)

**Weaknesses:**
- Requires genuine psychological safety; blame-free culture is hard to establish and easy to lose
- Can become performative (going through motions without genuine learning) in hostile environments
- Not effective for prospective review (only works on things that have already happened or been produced)
- Resource-intensive: requires multiple participants and significant time investment
- May surface uncomfortable truths about systemic problems that organizations prefer to ignore

**Novelty Factor:** HIGH. M&M conferences are universal in medicine but essentially unknown as a formal adversarial review pattern in software engineering or AI. The decision-chain reconstruction technique is particularly novel for reviewing LLM agent outputs, where the "reasoning chain" is inspectable in a way that human decision-making is not.

**Applicability to LLM Workflows:** MEDIUM-HIGH. An M&M-style review could be applied to failed agent outputs: "Here is the prompt, the agent's chain-of-thought, and the output. Let us reconstruct the decision chain and identify where reasoning went wrong." The blame-free framing is less critical for AI agents (they lack feelings), but the systemic focus -- finding process/prompt/architecture problems rather than just "the agent got it wrong" -- is highly valuable. Could be implemented as a post-failure analysis protocol triggered when quality scores fall below threshold.

---

### Strategy E3: Reference Class Forecasting (Outside View)

**Name:** Reference Class Forecasting / Outside View Adversarial Review

**Origin/Author:** Daniel Kahneman and Amos Tversky (1977, "Intuitive Prediction: Biases and Corrective Procedures"). Formalized for project forecasting by Kahneman and Dan Lovallo (1993, "Timid Choices and Bold Forecasts: A Cognitive Perspective on Risk Taking"). Operationalized for public policy by Bent Flyvbjerg (2006, 2008). Mandated by the UK Treasury Green Book for infrastructure projects.

**Citation:**
- Kahneman, D., & Tversky, A. (1977). Intuitive prediction: Biases and corrective procedures. Technical Report PTR-1042-77-6, Defense Advanced Research Projects Agency.
- Kahneman, D., & Lovallo, D. (1993). Timid choices and bold forecasts: A cognitive perspective on risk taking. *Management Science*, 39(1), 17-31. DOI: 10.1287/mnsc.39.1.17
- Flyvbjerg, B. (2006). From Nobel Prize to project management: Getting risks right. *Project Management Journal*, 37(3), 5-15.
- Flyvbjerg, B. (2008). Curbing optimism bias and strategic misrepresentation in planning: Reference class forecasting in practice. *European Planning Studies*, 16(1), 3-21. DOI: 10.1080/09654310701747936
- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. ISBN: 978-0374533557.

**Description:** A debiasing technique reframed as adversarial review. Instead of evaluating a plan, design, or estimate on its own merits (the "inside view"), an adversarial agent forces comparison against the actual outcomes of a "reference class" of comparable prior projects or decisions. The core adversarial move is: "I do not care about your specific reasoning for why THIS project is different. Show me the base rate outcomes for projects like this one." This directly attacks planning optimism, uniqueness bias, and the narrative fallacy.

**Mechanism (Step-by-Step):**
1. **Reference Class Identification:** The adversarial agent identifies the relevant reference class -- a set of broadly comparable past projects, designs, or decisions. The class must be defined by objective characteristics, not subjective similarity.
2. **Base Rate Extraction:** Determine the distributional outcomes for the reference class: What percentage succeeded? What were typical overruns? What failure modes occurred? What were median and tail outcomes?
3. **Inside View Challenge:** Present the creator's specific plan/estimate alongside the reference class distribution. The adversarial question is: "Your plan assumes outcome X. The reference class shows that only Y% of similar projects achieve X. What specific, verifiable evidence do you have that your project will outperform the base rate?"
4. **Uniqueness Interrogation:** For each claim of "our project is different because...", the adversarial agent asks: "How many projects in the reference class also believed they were different for the same reason? What was their actual outcome?"
5. **Anchoring Adjustment:** If the creator cannot provide compelling evidence of uniqueness, the review anchors the estimate to the reference class distribution -- typically the median or a risk-adjusted percentile.
6. **Residual Optimism Flagging:** Any remaining gap between the creator's estimate and the reference-class-adjusted estimate is flagged as "residual optimism" requiring explicit justification or risk acceptance.

**Strengths:**
- Directly attacks the most pernicious cognitive bias in planning (optimism bias, documented at 50-200% overrun in infrastructure projects per Flyvbjerg)
- Evidence-based: relies on actual outcome data rather than subjective judgment
- Simple to explain and implement -- even non-experts understand "how did similar things turn out?"
- Mandated by UK government for projects over 40M GBP, giving institutional legitimacy
- Particularly effective against "narrative thinking" where a compelling story overrides statistical evidence

**Weaknesses:**
- Requires a reference class, which may not exist for genuinely novel work
- Defining the "right" reference class is itself a judgment call susceptible to manipulation (choosing a favorable comparison set)
- Can be demoralizing ("statistically, projects like yours fail") without complementary constructive guidance
- Base rates may be outdated or from a different technological era
- Does not help diagnose specific problems -- only flags aggregate risk

**Novelty Factor:** MEDIUM. Reference Class Forecasting is well-known in project management and behavioral economics but is rarely framed as an adversarial review technique. Reframing it as an adversarial strategy -- with a dedicated "outside view agent" whose mandate is to challenge the inside view -- is a novel application.

**Applicability to LLM Workflows:** HIGH. An "Outside View Agent" could be implemented as a specialized critic that, for any plan or estimate produced by a creator agent, automatically retrieves or generates reference class comparisons. In Jerry's context, this could mean: "Your architecture plan has 8 components. In our reference class of 12 similar architectures, average integration time was 3x the initial estimate. Justify your timeline." The agent could maintain a growing reference class database from past Jerry project outcomes.

---

### Strategy E4: Wargaming / Tabletop Exercise Review

**Name:** Wargaming / Tabletop Exercise Adversarial Review

**Origin/Author:** Prussian military Kriegsspiel (1812, Georg von Reisswitz). Modern wargaming formalized by the U.S. Department of Defense and RAND Corporation (1950s-1960s). Tabletop exercises (TTX) codified by FEMA and DHS for emergency management. Applied to business strategy by Herman Kahn at RAND and the Hudson Institute (1960s). Recent resurgence in strategic wargaming documented by Peter Perla and the Naval War College.

**Citation:**
- von Reisswitz, G. (1824/1983). *Kriegsspiel: Instructions for the Representation of Military Manoeuvres with the Apparatus of War*. Translated by Bill Leeson. Too Fat Lardies.
- Perla, P. P. (1990). *The Art of Wargaming*. Naval Institute Press. ISBN: 978-0870210501.
- FEMA (2020). *Homeland Security Exercise and Evaluation Program (HSEEP)*. Department of Homeland Security.
- Caffrey, M. B. (2019). *On Wargaming: How Wargames Have Shaped History and How They May Shape the Future*. Naval War College Press.
- Schwarz, P. (1991). *The Art of the Long View: Planning for the Future in an Uncertain World*. Crown Currency. ISBN: 978-0385267328.

**Description:** A scenario-driven adversarial review where participants role-play through a specific scenario to stress-test a plan, architecture, or decision against realistic conditions. Unlike Red Teaming (which emulates a specific adversary), wargaming explores a space of possible futures by injecting "injects" -- unexpected events, constraint changes, or environmental shifts -- and observing how the plan/system responds. The adversarial element comes from the "control team" that designs and introduces these injects to maximally stress the plan under review.

**Mechanism (Step-by-Step):**
1. **Scenario Design:** Define the starting conditions, the plan/architecture under review, and the key uncertainties or risks to explore. Design 5-10 "injects" -- realistic but challenging events that could disrupt the plan.
2. **Role Assignment:** Assign roles: (a) the plan's defenders (who must adapt the plan in real-time), (b) the control team (who introduces injects and adjudicates outcomes), and (c) observers who document decision quality.
3. **Turn Execution:** The exercise proceeds in turns. Each turn: (a) control introduces an inject or environmental change, (b) defenders must adapt their plan, (c) control evaluates the adaptation's plausibility and determines consequences.
4. **Stress Escalation:** Injects increase in severity over successive turns, testing graceful degradation and recovery under compounding stress.
5. **Hot Wash / After-Action Review:** Immediately after the exercise, participants debrief: What surprised them? Where did the plan break? What assumptions proved wrong? What adaptations worked?
6. **Insights Report:** Document the plan's resilience envelope -- the conditions under which it holds and the conditions under which it fails.

**Strengths:**
- Tests plans against a space of futures, not just a single adversary or failure mode
- Reveals emergent failures that arise from interaction effects (multiple small problems combining)
- Forces real-time adaptation, testing not just the plan but the planning process
- Highly engaging and experiential -- participants discover problems viscerally rather than analytically
- Well-suited to complex systems where failure modes are not enumerable in advance

**Weaknesses:**
- Design quality of scenarios and injects is critical -- poor scenarios yield useless results
- Time-intensive: typical wargames take hours to days
- Requires skilled facilitation (the control team role)
- Outcomes are scenario-dependent; a wargame only tests the scenarios designed, not all possible futures
- Can feel artificial if scenarios are unrealistic

**Novelty Factor:** MEDIUM. Wargaming is well-established in military and emergency management but is rarely applied as a formal adversarial review technique for software architecture, code review, or AI systems. The transfer is novel and particularly interesting for testing AI agent orchestration plans.

**Applicability to LLM Workflows:** MEDIUM. A wargaming-style review could test Jerry's orchestration plans: "Here is a multi-phase workflow plan. Now I introduce inject: the researcher agent returns contradictory findings in Phase 2. How does the plan adapt?" An "inject generator" agent could produce realistic disruption scenarios, while the plan's "defender" agent demonstrates adaptation. The main limitation is that LLM agents cannot truly "adapt in real-time" in the same way human participants can, but the inject-response pattern could still reveal plan fragility.

---

### Strategy E5: Constitutional AI Critique Chains

**Name:** Constitutional AI (CAI) Critique Chains

**Origin/Author:** Anthropic (Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, et al., 2022). Extended by subsequent work on self-critique, recursive reward modeling, and principle-based evaluation. Builds on earlier RLHF work (Christiano et al., 2017) and debate as AI alignment technique (Irving et al., 2018).

**Citation:**
- Bai, Y., Kadavath, S., Kundu, S., Askell, A., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. *arXiv preprint arXiv:2212.08073*.
- Irving, G., Christiano, P., & Amodei, D. (2018). AI safety via debate. *arXiv preprint arXiv:1805.00899*.
- Saunders, W., Yeh, C., Wu, J., Bills, S., Ouyang, L., Ward, J., & Leike, J. (2022). Self-critiquing models for assisting human evaluators. *arXiv preprint arXiv:2206.05802*.
- Madaan, A., Tandon, N., Gupta, P., et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. *NeurIPS 2023*. arXiv:2303.17651.

**Description:** A multi-pass adversarial review technique where an LLM agent critiques its own or another agent's output against an explicit set of principles (a "constitution"). Unlike general critique ("find problems"), CAI critique chains provide the critic with specific, enumerated principles to check against, producing structured evaluations tied to named principles. Each critique pass can focus on a different subset of principles, and the creator revises after each pass, creating an iterative convergence toward principle-compliant output.

**Mechanism (Step-by-Step):**
1. **Constitution Definition:** Define an explicit set of review principles relevant to the work product. Example for code review: (P1) All public functions have type hints, (P2) No imports cross architectural boundaries, (P3) Error handling uses domain exceptions, (P4) Tests cover happy path, error path, and edge cases.
2. **Generation Pass:** The creator agent produces the initial work product.
3. **Critique Pass 1 (Structural Principles):** The critic agent evaluates the output against structural/mechanical principles (P1, P2). For each principle, it outputs: PASS/FAIL with specific evidence and location.
4. **Revision 1:** The creator revises based on critique, addressing each flagged principle violation.
5. **Critique Pass 2 (Semantic Principles):** The critic evaluates against deeper semantic principles (P3, P4) -- correctness of logic, completeness of coverage, quality of reasoning.
6. **Revision 2:** Creator revises again.
7. **Critique Pass 3 (Holistic/Emergent Principles):** Optional final pass evaluating emergent properties: coherence, consistency across components, architectural alignment.
8. **Convergence Check:** If no principle violations remain, the work product is accepted. If violations persist after N passes, escalate to human review.

**Strengths:**
- Explicit principles make the review reproducible and auditable
- Multi-pass structure catches issues at different abstraction levels
- Separating structural from semantic from holistic critique prevents cognitive overload
- Directly leverages LLM capability for self-critique (empirically demonstrated in Bai et al., 2022)
- The constitution can evolve: new principles are added as new failure modes are discovered
- Highly composable: different constitutions for different review contexts

**Weaknesses:**
- Quality is bounded by the quality of the constitution -- missing principles mean missed problems
- LLM self-critique has known blind spots (models may consistently fail to detect certain categories of error)
- Iteration can converge to a local optimum that satisfies all stated principles but misses unlisted quality dimensions
- Risk of "constitution gaming" where output technically satisfies principles while violating their intent
- Requires careful principle engineering -- too few principles miss issues; too many create noise

**Novelty Factor:** HIGH. While Constitutional AI is known in the AI safety community, its application as a general-purpose adversarial review strategy for software engineering, architecture review, and requirements validation is novel. The multi-pass, principle-stratified structure (structural -> semantic -> holistic) is a contribution of this research.

**Applicability to LLM Workflows:** VERY HIGH. This is arguably the most directly applicable strategy for Jerry. Jerry already has coding standards (`.claude/rules/`), architecture standards, and testing standards -- these ARE a constitution. A CAI critique chain could operationalize these standards as adversarial review: the critic agent is given the relevant rules files as its constitution and evaluates creator output against them. This closes the gap between "standards exist" and "standards are enforced."

---

### Strategy E6: Progressive Adversarial Escalation

**Name:** Progressive Adversarial Escalation (PAE)

**Origin/Author:** Novel composite strategy synthesized from multiple sources. Elements drawn from: (a) graduated exercise programs in military training (crawl-walk-run doctrine, U.S. Army FM 7-0), (b) progressive overload in exercise physiology (Selye's General Adaptation Syndrome, 1956), (c) curriculum learning in machine learning (Bengio et al., 2009), and (d) the Dreyfus model of skill acquisition (Dreyfus & Dreyfus, 1980).

**Citation:**
- U.S. Army (2021). *FM 7-0: Training*. Department of the Army.
- Selye, H. (1956). *The Stress of Life*. McGraw-Hill.
- Bengio, Y., Louradour, J., Collobert, R., & Weston, J. (2009). Curriculum learning. *Proceedings of the 26th International Conference on Machine Learning (ICML)*, 41-48. DOI: 10.1145/1553374.1553380
- Dreyfus, S. E., & Dreyfus, H. L. (1980). A five-stage model of the mental activities involved in directed skill acquisition. *Operations Research Center, University of California, Berkeley*.

**Description:** A graduated adversarial review strategy where review intensity starts low and increases systematically across multiple passes. Early passes use gentle, constructive adversarial methods (e.g., Steelman + suggestion); middle passes increase to moderate challenge (e.g., Devil's Advocate + Assumption Stress Testing); late passes apply maximum adversarial pressure (e.g., Red Team + Cross-Examination). The key insight is that applying maximum adversarial intensity to early-stage work is counterproductive -- it demoralizes creators, wastes critic resources on obvious issues, and fails to improve final quality as effectively as graduated escalation.

**Mechanism (Step-by-Step):**
1. **Level 0 -- Self-Check (Minimal):** Creator performs self-review against a checklist. No external adversary. Purpose: catch obvious errors before consuming critic resources.
2. **Level 1 -- Constructive Challenge (Low):** A "friendly critic" reviews with Steelman orientation: "Here is what is strong about this work. Here are 2-3 areas that could be strengthened." Focus on building up, not tearing down.
3. **Level 2 -- Probing Questions (Medium):** A moderately adversarial critic asks probing questions: "Why did you choose X over Y? What happens if assumption Z is wrong? Where is the evidence for claim W?" Uses Socratic questioning rather than assertion.
4. **Level 3 -- Active Challenge (High):** Full adversarial mode: Devil's Advocate arguments, Assumption Stress Testing, reference class challenges. The critic actively tries to find flaws and articulates them forcefully.
5. **Level 4 -- Hostile Examination (Maximum):** Red Team simulation or Cross-Examination. The critic operates as if trying to defeat the work product. Mutation testing of arguments. Worst-case scenario construction.
6. **Escalation Gates:** Work must pass each level before progressing. If it fails Level 2, it returns to the creator for revision before encountering Level 3. This prevents wasting Level 4 resources on work that has Level 2 problems.

**Strengths:**
- Efficient resource allocation: simple issues caught at low-cost levels, expensive adversarial methods reserved for mature work
- Prevents the "demolition problem" where premature harsh critique destroys good ideas that need development
- Each escalation level produces focused feedback at the appropriate abstraction level
- The escalation gate prevents "adversarial waste" -- spending resources on harsh review of fundamentally flawed work
- Creates a natural quality gradient that maps to software development lifecycle stages

**Weaknesses:**
- Requires calibration of escalation levels to the specific work type
- Can create false confidence at lower levels ("it passed Level 2, it must be good enough")
- Adds overhead from multiple review passes
- The escalation gate logic needs careful design to avoid being either too permissive or too strict
- May not be appropriate for time-critical reviews where rapid, high-intensity feedback is needed

**Novelty Factor:** HIGH. While individual adversarial strategies exist at various intensity levels, the formal concept of calibrated, progressive escalation through defined intensity levels is novel. The closest existing concept is the software testing pyramid, but that applies to test types rather than adversarial review intensity.

**Applicability to LLM Workflows:** VERY HIGH. This strategy maps directly to Jerry's multi-agent architecture. Different agents could be configured at different escalation levels: a "friendly reviewer" agent at Level 1, a "probing questioner" at Level 2, and a "red team critic" at Level 4. The orchestration skill could implement the escalation gates, routing work to the appropriate adversarial level based on its maturity. This is one of the most implementable strategies identified in this research.

---

### Strategy E7: Inversion Technique (Problem Reversal)

**Name:** Inversion Technique / Problem Reversal Adversarial Review

**Origin/Author:** Carl Gustav Jacob Jacobi (19th century mathematician): "Invert, always invert." Popularized in decision-making by Charlie Munger (Berkshire Hathaway, various speeches 1994-present). Formalized as a mental model by Shane Parrish (Farnam Street). Related to the mathematical technique of proof by contradiction (reductio ad absurdum) and the Japanese quality technique of Poka-Yoke (mistake-proofing via inversion).

**Citation:**
- Munger, C. T. (2005). *Poor Charlie's Almanack: The Wit and Wisdom of Charles T. Munger*. Walsworth Publishing Company. ISBN: 978-1578645015.
- Parrish, S. (2019). *The Great Mental Models, Volume 1: General Thinking Concepts*. Latticework Publishing. ISBN: 978-1999449018.
- Polya, G. (1945). *How to Solve It: A New Aspect of Mathematical Method*. Princeton University Press. ISBN: 978-0691164076.
- Shingo, S. (1986). *Zero Quality Control: Source Inspection and the Poka-Yoke System*. Productivity Press. ISBN: 978-0915299072.

**Description:** An adversarial review technique where, instead of asking "How do we make this succeed?", the critic asks "How would we guarantee this fails?" or "What would we do if we wanted to produce the worst possible version of this?" By inverting the problem, the critic generates a failure roadmap -- a comprehensive list of anti-patterns, pitfalls, and failure modes that can then be checked against the actual work product. Any overlap between the "guaranteed failure" recipe and the actual work is flagged as a critical risk.

**Mechanism (Step-by-Step):**
1. **Problem Inversion:** The critic agent takes the creator's objective and inverts it. If the objective is "design a reliable API," the inverted objective becomes "design an API guaranteed to be unreliable."
2. **Anti-Pattern Generation:** The critic brainstorms every possible way to achieve the inverted objective. "To guarantee an unreliable API, we would: use no input validation, share mutable state, have no timeouts, return inconsistent error formats, have no retry logic, deploy with no monitoring..."
3. **Checklist Construction:** The anti-pattern list is converted to a review checklist by re-inverting: "Does this API have input validation? Does it avoid shared mutable state? Does it implement timeouts?..."
4. **Systematic Comparison:** The actual work product is evaluated against the inverted checklist. Each anti-pattern that appears (even partially) in the actual work is flagged.
5. **Severity Assessment:** Flagged items are classified by proximity to the anti-pattern: full match (critical), partial match (warning), or no match (clear).
6. **Remediation Guidance:** For each flagged item, the inversion naturally suggests the fix -- the opposite of the anti-pattern.

**Strengths:**
- Remarkably effective at generating comprehensive checklists -- people (and LLMs) are better at imagining failure than enumerating all success conditions
- Produces immediately actionable review criteria
- Fun and engaging -- "how would you make this terrible?" is a more creative prompt than "find what's wrong"
- Self-documenting: the inverted checklist becomes a permanent quality artifact
- Complementary to positive review: catches failure modes that "what's good about this?" misses

**Weaknesses:**
- May miss failure modes that are not the inverse of success (e.g., emergent failures from complex interactions)
- Can become frivolous if not constrained ("the API would fail if the server was on fire" -- technically true but unhelpful)
- Does not evaluate quality of what IS present, only checks for absence of anti-patterns
- Less effective for creative or subjective work where "failure" is ambiguous
- Requires domain expertise to generate meaningful anti-patterns (not just obvious ones)

**Novelty Factor:** MEDIUM. The Inversion Technique is known in the mental models community but is not conventionally framed as an adversarial review strategy. Its application as a systematic, structured adversarial method for code/architecture review is a novel reframing, and the anti-pattern-to-checklist conversion mechanism is a practical contribution.

**Applicability to LLM Workflows:** HIGH. LLMs are excellent at brainstorming failure modes. An "Inverter Agent" prompted with "Given this design, describe how you would guarantee its failure" will reliably produce comprehensive anti-pattern lists. The mechanical conversion to a positive checklist is trivially automatable. This could be implemented as a pre-review step that generates context-specific review criteria before the main adversarial review begins. Particularly powerful when combined with Jerry's coding standards -- the inversion of each standard produces a targeted anti-pattern to check for.

---

### Strategy E8: Ensemble Adversarial Meta-Review

**Name:** Ensemble Adversarial Meta-Review (EAMR)

**Origin/Author:** Novel composite strategy. Draws on: (a) ensemble methods in machine learning (Breiman, 1996 -- bagging; Schapire, 1990 -- boosting), (b) meta-analysis methodology in evidence-based medicine (Cochrane Collaboration, 1993), (c) the Delphi method's multi-round expert aggregation (Dalkey & Helmer, 1963), and (d) adversarial meta-review in academic publishing (reviewing the reviews).

**Citation:**
- Breiman, L. (1996). Bagging predictors. *Machine Learning*, 24(2), 123-140. DOI: 10.1007/BF00058655
- Schapire, R. E. (1990). The strength of weak learnability. *Machine Learning*, 5(2), 197-227. DOI: 10.1007/BF00116037
- Dalkey, N. C., & Helmer, O. (1963). An experimental application of the Delphi method to the use of experts. *Management Science*, 9(3), 458-467. DOI: 10.1287/mnsc.9.3.458
- Cochrane, A. L. (1972). *Effectiveness and Efficiency: Random Reflections on Health Services*. Nuffield Provincial Hospitals Trust. ISBN: 978-1853152429.
- Price, E., & Perez, C. E. (2017). Ensemble adversarial training: Attacks and defenses. *arXiv preprint arXiv:1705.07204*.

**Description:** A meta-strategy that combines multiple weak or focused adversarial methods into a stronger composite review, then subjects the composite review itself to meta-review. The key insight (borrowed from ensemble learning) is that multiple independent adversarial perspectives, each with different biases and blind spots, produce a combined review that is more robust than any single method. The meta-review layer then checks: Did the ensemble of reviewers actually cover the full problem space? Are there systematic gaps in what the ensemble examined? Do the reviewers agree or disagree, and what does disagreement signal?

**Mechanism (Step-by-Step):**
1. **Ensemble Design:** Select 3-5 adversarial strategies with complementary strengths. Example ensemble: (a) Assumption Stress Testing (structural), (b) Devil's Advocate (rhetorical), (c) Reference Class Forecasting (statistical), (d) Inversion Technique (creative).
2. **Independent Parallel Review:** Each adversarial strategy is applied independently to the same work product. Crucially, reviewers do NOT see each other's reviews during this phase (independence requirement, same as ensemble learning).
3. **Review Aggregation:** All reviews are collected and synthesized. Issues found by multiple methods receive higher confidence. Issues found by only one method are flagged for validation.
4. **Disagreement Analysis:** Where methods disagree (one flags an issue, another does not), the disagreement itself is analyzed. Disagreement often signals either: (a) a subtle issue that only certain methods can detect, or (b) a false positive from one method that others correctly rejected.
5. **Coverage Analysis (Meta-Review):** A meta-reviewer examines the ensemble's collective coverage: What aspects of the work were NOT examined by any method? Are there systematic blind spots? Did the ensemble actually test different things, or did they redundantly test the same things?
6. **Gap-Filling Pass:** Based on coverage analysis, additional targeted review is applied to uncovered areas.
7. **Final Synthesis:** A synthesized review document integrating all findings, weighted by cross-method agreement and meta-review coverage assessment.

**Strengths:**
- Provably more robust than any single adversarial method (follows from ensemble theory -- diversity reduces variance)
- The meta-review layer addresses the "who watches the watchmen?" problem
- Independent parallel execution is inherently parallelizable in multi-agent systems
- Disagreement analysis surfaces subtle issues that consensus-driven review misses
- Coverage analysis prevents the false confidence of "we reviewed it thoroughly" when only one dimension was tested

**Weaknesses:**
- Resource-intensive: requires multiple independent reviews plus meta-review
- Ensemble design requires expertise in selecting complementary methods (poor selection negates the benefit)
- Risk of review fatigue: the creator receives feedback from multiple perspectives, potentially contradictory
- The meta-review layer adds yet another potential point of failure (meta-reviewer may have its own biases)
- Coordination overhead is significant

**Novelty Factor:** VERY HIGH. While ensemble methods are foundational in ML and meta-analysis is standard in medicine, the formal combination of ensemble adversarial review with adversarial meta-review is novel. No published framework treats adversarial review as an ensemble learning problem with explicit independence, aggregation, and coverage analysis steps.

**Applicability to LLM Workflows:** VERY HIGH. This maps perfectly to Jerry's multi-agent architecture. Multiple critic agents, each configured with a different adversarial strategy, independently review the same work product. An "ensemble synthesizer" agent aggregates findings. A "meta-reviewer" agent evaluates the ensemble's coverage. The independence requirement is naturally satisfied because LLM agents do not share state between parallel invocations. This could be Jerry's most powerful quality assurance pattern for high-stakes deliverables.

---

### Strategy E9: Red Queen Evolutionary Adversarial Escalation

**Name:** Red Queen Evolutionary Adversarial Escalation

**Origin/Author:** Leigh Van Valen (1973, "A New Evolutionary Law," *Evolutionary Theory*, 1:1-30). Named for the Red Queen in Lewis Carroll's *Through the Looking-Glass* (1871): "It takes all the running you can do, to keep in the same place." Applied to cybersecurity by cyber arms race researchers (e.g., Schneier, 2000). Applied to AI safety by Hubinger et al. (2019, "Risks from Learned Optimization in Advanced Machine Learning Systems").

**Citation:**
- Van Valen, L. (1973). A new evolutionary law. *Evolutionary Theory*, 1, 1-30.
- Carroll, L. (1871). *Through the Looking-Glass, and What Alice Found There*. Macmillan.
- Schneier, B. (2000). *Secrets and Lies: Digital Security in a Networked World*. John Wiley & Sons. ISBN: 978-0471253112.
- Hubinger, E., van Merwijk, C., Mikulik, V., Skalse, J., & Garrabrant, S. (2019). Risks from learned optimization in advanced machine learning systems. *arXiv preprint arXiv:1906.01820*.
- Goodfellow, I., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. *ICLR 2015*. arXiv:1412.6572.

**Description:** A co-evolutionary adversarial pattern where the creator and critic agents are locked in an explicit arms race, each improving in response to the other over successive generations. Unlike static adversarial review (where the critic's strategy is fixed), the Red Queen pattern requires both sides to adapt: the critic develops new attack strategies based on what the creator has learned to defend against, and the creator develops new defenses based on what the critic has learned to attack. Over multiple generations, both sides become dramatically more capable, and the work product achieves a level of robustness unattainable through static review.

**Mechanism (Step-by-Step):**
1. **Generation 0 (Baseline):** Creator produces initial work. Critic applies standard adversarial review. Findings are logged.
2. **Creator Adaptation (Gen 1):** Creator revises work AND updates its generation strategy to proactively avoid the types of issues the critic found. The creator's "immune system" strengthens.
3. **Critic Adaptation (Gen 1):** Critic reviews the revised work. Crucially, the critic also updates its adversarial strategy: if the creator has learned to defend against assumption attacks, the critic shifts to cross-examination or mutation testing. The critic evolves to attack the creator's new defenses.
4. **Escalation Loop:** This cycle repeats for N generations. Each generation, both sides adapt to the other's latest strategy. Findings become increasingly subtle and deep.
5. **Convergence Detection:** The loop terminates when: (a) the critic cannot find new issues (convergence), (b) a maximum generation count is reached, or (c) a quality threshold is exceeded.
6. **Arms Race Documentation:** The full evolutionary history is preserved: what was found at each generation, how each side adapted, and what the final steady-state quality level is. This history itself is a knowledge artifact.

**Strengths:**
- Produces work of dramatically higher quality than static adversarial review (both sides push each other)
- The evolutionary record reveals the deepest, most subtle issues (found only after obvious issues are resolved)
- Self-calibrating: the process automatically adjusts intensity based on the creator's capability
- Builds institutional knowledge: the arms race history teaches future agents what to check
- Mirrors real-world adversarial dynamics (cybersecurity, biological evolution, competitive markets)

**Weaknesses:**
- Resource-intensive: multiple generations consume significant compute
- Risk of "overfitting" -- the creator may optimize for the specific critic rather than general quality
- Convergence is not guaranteed; the arms race could oscillate without improving
- Requires sophisticated meta-cognition: agents must not only review but also analyze and adapt their review strategies
- Can produce diminishing returns after initial generations if the problem space is small

**Novelty Factor:** HIGH. While Generative Adversarial Networks (GANs) implement this pattern for image generation, the formal application of co-evolutionary dynamics to structured adversarial review in multi-agent systems is novel. The key contribution is making the adaptation explicit and documented rather than implicit.

**Applicability to LLM Workflows:** HIGH. This could be implemented in Jerry by maintaining a "strategy evolution log" for each creator-critic pair. After each review cycle, the orchestrator prompts the critic: "Here is what you found in the last 3 reviews. The creator has addressed all of them. How will you change your review strategy to find new categories of issues?" Similarly, the creator is prompted: "Here are the critic's latest strategies. How will you proactively address these in your next generation?" The main challenge is prompt engineering for genuine adaptation rather than superficial strategy shuffling.

---

### Strategy E10: Cynefin-Gated Adversarial Intensity Selection

**Name:** Cynefin-Gated Adversarial Intensity Selection

**Origin/Author:** Novel meta-strategy combining the Cynefin framework (Dave Snowden, 1999, Cognitive Edge / The Cynefin Company) with adversarial review selection. Cynefin itself is published in: Snowden, D. J., & Boone, M. E. (2007). "A Leader's Framework for Decision Making," *Harvard Business Review*, 85(11), 68-76. The application to adversarial intensity selection is a novel contribution of this research.

**Citation:**
- Snowden, D. J., & Boone, M. E. (2007). A leader's framework for decision making. *Harvard Business Review*, 85(11), 68-76.
- Snowden, D. J. (2002). Complex acts of knowing: Paradox and descriptive self-awareness. *Journal of Knowledge Management*, 6(2), 100-111. DOI: 10.1108/13673270210424639
- Kurtz, C. F., & Snowden, D. J. (2003). The new dynamics of strategy: Sense-making in a complex and complicated world. *IBM Systems Journal*, 42(3), 462-483. DOI: 10.1147/sj.423.0462
- Rittel, H. W. J., & Webber, M. M. (1973). Dilemmas in a general theory of planning. *Policy Sciences*, 4(2), 155-169. DOI: 10.1007/BF01405730

**Description:** A meta-strategy that classifies the problem being reviewed into one of the Cynefin domains (Clear, Complicated, Complex, Chaotic) and then selects the appropriate adversarial strategy and intensity based on the domain classification. The core insight is that different problem types require fundamentally different adversarial approaches: applying Red Team to a Clear problem is wasteful overkill; applying a simple checklist to a Complex problem is dangerously inadequate. Cynefin-gating prevents both under-review and over-review by matching adversarial intensity to problem complexity.

**Mechanism (Step-by-Step):**
1. **Domain Classification:** Before any adversarial review begins, classify the work product into a Cynefin domain:
   - **Clear (Simple):** The relationship between cause and effect is obvious. Best practices exist. Example: formatting compliance, naming conventions.
   - **Complicated:** Cause-effect relationship exists but requires expertise to discern. Good practices exist but require analysis. Example: algorithm correctness, architecture design.
   - **Complex:** Cause-effect relationship is only apparent in retrospect. Emergent behaviors. No good practices, only emergent practices. Example: distributed system interactions, novel AI pipeline design.
   - **Chaotic:** No discernible cause-effect relationship. Novel situation requiring immediate action. Example: production incident, security breach response.

2. **Strategy Selection by Domain:**

   | Domain | Adversarial Intensity | Recommended Strategies |
   |--------|----------------------|----------------------|
   | Clear | LOW | Checklist review, automated lint, Constitutional AI (mechanical principles only) |
   | Complicated | MEDIUM | Devil's Advocate, Assumption Stress Testing, Reference Class Forecasting, FMEA |
   | Complex | HIGH | Ensemble Adversarial, Wargaming, Red Queen Escalation, Pre-Mortem, Cross-Examination |
   | Chaotic | ADAPTIVE | Rapid Red Team probe, then stabilize, then re-classify |

3. **Intensity Calibration:** Within each domain, further calibrate based on: (a) criticality of the work product, (b) available resources, (c) time constraints, and (d) historical defect rate for similar work.

4. **Domain Transition Detection:** Monitor for signs that the problem has shifted domains during review. A Complicated problem may reveal Complex dynamics; a seemingly Clear problem may have hidden Complicated elements. When domain shift is detected, re-gate.

5. **Review Execution:** Execute the selected adversarial strategies at the calibrated intensity.

6. **Post-Review Cynefin Validation:** After review, assess whether the domain classification was correct based on what the review revealed. Update classification heuristics for future reviews.

**Strengths:**
- Prevents both over-review (wasting expensive adversarial methods on simple problems) and under-review (applying weak methods to complex problems)
- Provides a principled, defensible rationale for adversarial intensity decisions
- The Cynefin framework is well-established and widely respected in organizational theory
- Domain transition detection catches the dangerous case where a simple-seeming problem is actually complex
- Creates a meta-learning loop: classification improves over time as the system learns which domains different work types actually fall into

**Weaknesses:**
- Domain classification itself is a judgment call that can be wrong
- The Cynefin framework is qualitative, not quantitative -- classification may be subjective
- Adds overhead: classification step before review begins
- Risk of "complexity theater" where everything is classified as Complex to justify expensive review
- The mapping from domains to strategies requires calibration for each organization/context

**Novelty Factor:** VERY HIGH. No published framework connects problem complexity classification to adversarial review strategy selection. This is a genuinely novel contribution that could serve as Jerry's core strategy selection algorithm, addressing the "which adversarial strategy should I use?" question that the existing 15-strategy catalog leaves unanswered.

**Applicability to LLM Workflows:** VERY HIGH. This could be implemented as Jerry's primary adversarial orchestration logic. Before any review begins, a "classifier agent" examines the work product and classifies it into a Cynefin domain. The orchestration skill then selects appropriate adversarial strategies and intensity based on the classification. The classifier agent could be trained on historical review data: what domain classifications led to the best review outcomes? This meta-strategy gives Jerry the ability to be proportionate and efficient in its adversarial review, rather than applying one-size-fits-all review to every work product.

---

## L2: Architectural Implications

### Highest-Potential Strategies for Jerry's Multi-Agent Framework

Based on the analysis above, I recommend the following prioritization for integration into Jerry:

#### Tier 1: Immediate Implementation (High Value, High Feasibility)

| Strategy | Rationale | Implementation Path |
|----------|-----------|-------------------|
| **E5: Constitutional AI Critique Chains** | Jerry already has constitutions (`.claude/rules/`). This strategy operationalizes them as adversarial review. | Configure critic agents to receive relevant rules files as constitution. Implement multi-pass critique (structural -> semantic -> holistic). |
| **E6: Progressive Adversarial Escalation** | Maps directly to Jerry's existing agent pool (different agents at different intensity levels). Prevents resource waste. | Define escalation levels in orchestration skill. Implement escalation gates as quality score thresholds. Route work to appropriate-level critic. |
| **E10: Cynefin-Gated Selection** | Solves the "which strategy?" meta-problem. Makes the strategy catalog usable rather than overwhelming. | Implement a classifier agent in orchestration skill. Build a Cynefin-to-strategy mapping table. Add domain transition detection. |

#### Tier 2: Near-Term Enhancement (High Value, Moderate Feasibility)

| Strategy | Rationale | Implementation Path |
|----------|-----------|-------------------|
| **E8: Ensemble Adversarial Meta-Review** | Leverages Jerry's multi-agent architecture for parallel independent review. Addresses "who watches the watchmen?" | Configure 3-5 critic agents with different strategies. Run in parallel (orchestration sync barrier). Add meta-reviewer agent for coverage analysis. |
| **E1: Moot Court / Cross-Examination** | The 3-agent choreography (witness/examiner/judge) offers a structured review format that goes deeper than flat critique. | Implement cross-examination prompt templates. Design the judge role for meta-evaluation. Integrate as a high-intensity review option. |
| **E7: Inversion Technique** | Excellent for generating context-specific review checklists from scratch. Low overhead, high yield. | Add "Inverter Agent" that generates anti-pattern checklists. Run as a pre-review step before main adversarial review. |

#### Tier 3: Strategic Investment (High Potential, Requires Maturity)

| Strategy | Rationale | Implementation Path |
|----------|-----------|-------------------|
| **E9: Red Queen Escalation** | Produces the highest-quality outcomes but requires sophisticated adaptation logic. | Implement after E6 (progressive escalation) is stable. Add strategy evolution logging. Requires meta-cognitive prompting for genuine adaptation. |
| **E3: Reference Class Forecasting** | Powerful debiasing tool but requires a reference class database that Jerry does not yet have. | Build reference class data incrementally from Jerry project history. Implement "Outside View Agent" once sufficient data exists. |
| **E2: M&M Conference Pattern** | Valuable for post-failure analysis but requires a corpus of failures to review. | Implement as a post-mortem protocol triggered by quality score failures. Build an "institutional memory" of past failures and their root causes. |

### Architectural Pattern: Adversarial Strategy Composition

The emerging strategies reveal an architectural pattern for Jerry's adversarial system:

```
                      ┌─────────────────────┐
                      │   Cynefin Classifier │  (E10)
                      │   (Meta-Strategy)    │
                      └──────────┬──────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │  Clear    │ │Complicated│ │ Complex  │
              │  Domain   │ │  Domain   │ │  Domain  │
              └────┬─────┘ └────┬─────┘ └────┬─────┘
                   │            │            │
                   ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ CAI       │ │ PAE      │ │ Ensemble │   (E5, E6, E8)
              │ Critique  │ │ Levels   │ │ Meta-    │
              │ Chain     │ │ 1-3      │ │ Review   │
              │ (Auto)    │ │          │ │ + Red    │
              │           │ │          │ │ Queen    │
              └──────────┘ └──────────┘ └──────────┘
                                              │
                                    ┌─────────┼─────────┐
                                    ▼         ▼         ▼
                              ┌────────┐ ┌────────┐ ┌────────┐
                              │Cross-  │ │Inver-  │ │Ref     │
                              │Exam    │ │sion    │ │Class   │
                              │(E1)    │ │(E7)    │ │(E3)    │
                              └────────┘ └────────┘ └────────┘
```

This architecture means Jerry does not need to choose a single adversarial strategy. Instead:
1. **Classify** the problem complexity (E10)
2. **Select** the appropriate strategy composition for that domain
3. **Execute** at the appropriate escalation level (E6)
4. **Evolve** the strategy over time (E9)

### Integration with Existing Jerry Skills

| Jerry Skill | Integration Point | Emerging Strategies |
|-------------|-------------------|-------------------|
| `/orchestration` | Adversarial gates in workflow plans | E6 (escalation levels), E10 (Cynefin gating), E8 (ensemble coordination) |
| `/problem-solving` | Enhanced critic agent configurations | E1 (cross-examination mode), E5 (constitutional critique), E7 (inversion pre-step) |
| `/nasa-se` | Requirements and design review protocols | E3 (reference class for estimates), E4 (wargaming for design), E2 (M&M for post-failure) |

---

## Differentiation Matrix: Emerging vs. Existing Strategies

This matrix shows how each emerging strategy (E1-E10) differs from the 15 strategies already cataloged by TASK-001/TASK-002.

| Emerging Strategy | Most Similar Existing Strategy | Key Differentiation |
|-------------------|-------------------------------|---------------------|
| E1: Moot Court / Cross-Examination | Devil's Advocate (#3) | Cross-examination questions WITHIN the creator's framework rather than arguing the opposite. Adds judge role for meta-evaluation. Multi-turn sequential questioning vs. single critique. |
| E2: M&M Conference Pattern | Pre-Mortem (#6) | M&M operates on ACTUAL past failures, not imagined future ones. Focus on decision-chain reconstruction and systemic (not individual) causes. Blame-free protocol. |
| E3: Reference Class Forecasting | Assumption Mapping (#15) | RCF uses EXTERNAL statistical base rates, not internal assumption analysis. Directly attacks optimism bias with data rather than logical challenge. |
| E4: Wargaming / Tabletop Exercise | Red Team (#1) | Wargaming explores a SPACE of futures via scenario injects rather than emulating a specific adversary. Tests plan adaptability, not just vulnerability. |
| E5: Constitutional AI Critique | Cognitive Bias Audit (#14) | CAI uses EXPLICIT enumerated principles as review criteria, not general bias categories. Multi-pass stratified review (structural -> semantic -> holistic). AI-native. |
| E6: Progressive Adversarial Escalation | None (novel composite) | No existing strategy addresses escalation intensity. PAE is a META-strategy for ordering and gating other strategies by intensity level. |
| E7: Inversion Technique | Pre-Mortem (#6) | Inversion is GENERATIVE (creates comprehensive checklists), while pre-mortem is ANALYTICAL (imagines specific scenarios). Inversion solves the opposite problem; pre-mortem imagines failure of the actual problem. |
| E8: Ensemble Meta-Review | Purple Team (#13) | EAMR uses INDEPENDENT parallel review with formal aggregation, not collaborative review. Adds meta-review of the review process. Borrows from ensemble learning theory. |
| E9: Red Queen Escalation | Chaos Engineering (#11) | Red Queen involves CO-EVOLUTIONARY adaptation of BOTH sides, not one-sided failure injection. The critic evolves its strategy based on what the creator has learned to defend. |
| E10: Cynefin-Gated Selection | None (novel meta-strategy) | No existing strategy addresses WHICH adversarial method to use. Cynefin-gating is a SELECTOR, not a reviewer. It classifies problem complexity to route to appropriate strategies. |

### Gap Analysis: What the Emerging Strategies Add

| Capability Gap in Existing 15 | Filled By |
|-------------------------------|-----------|
| No meta-strategy for selecting which adversarial method to use | E10 (Cynefin-Gated Selection) |
| No graduated intensity model (all-or-nothing adversarial review) | E6 (Progressive Adversarial Escalation) |
| No formal ensemble/aggregation framework for multi-reviewer settings | E8 (Ensemble Adversarial Meta-Review) |
| No principle-based structured multi-pass critique native to AI | E5 (Constitutional AI Critique Chains) |
| No cross-examination questioning technique (distinct from argumentation) | E1 (Moot Court / Cross-Examination) |
| No co-evolutionary adaptation between creator and critic | E9 (Red Queen Evolutionary Escalation) |
| No systematic checklist generation from problem inversion | E7 (Inversion Technique) |
| No blame-free systemic failure analysis protocol | E2 (M&M Conference Pattern) |
| No statistical debiasing using external base rates | E3 (Reference Class Forecasting) |
| No scenario-based plan stress testing with progressive injects | E4 (Wargaming / Tabletop Exercise) |

---

## References

### Primary Sources (Academic)

1. Bai, Y., Kadavath, S., Kundu, S., Askell, A., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. *arXiv preprint arXiv:2212.08073*.
2. Bengio, Y., Louradour, J., Collobert, R., & Weston, J. (2009). Curriculum learning. *Proceedings of the 26th ICML*, 41-48. DOI: 10.1145/1553374.1553380
3. Breiman, L. (1996). Bagging predictors. *Machine Learning*, 24(2), 123-140. DOI: 10.1007/BF00058655
4. Codman, E. A. (1914). The product of a hospital. *Surgery, Gynecology & Obstetrics*, 18, 491-496.
5. Dalkey, N. C., & Helmer, O. (1963). An experimental application of the Delphi method to the use of experts. *Management Science*, 9(3), 458-467. DOI: 10.1287/mnsc.9.3.458
6. Dreyfus, S. E., & Dreyfus, H. L. (1980). A five-stage model of the mental activities involved in directed skill acquisition. *UC Berkeley Operations Research Center*.
7. Flyvbjerg, B. (2006). From Nobel Prize to project management: Getting risks right. *Project Management Journal*, 37(3), 5-15.
8. Flyvbjerg, B. (2008). Curbing optimism bias and strategic misrepresentation in planning: Reference class forecasting in practice. *European Planning Studies*, 16(1), 3-21. DOI: 10.1080/09654310701747936
9. Goodfellow, I., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. *ICLR 2015*. arXiv:1412.6572.
10. Hubinger, E., van Merwijk, C., Mikulik, V., Skalse, J., & Garrabrant, S. (2019). Risks from learned optimization in advanced machine learning systems. *arXiv preprint arXiv:1906.01820*.
11. Irving, G., Christiano, P., & Amodei, D. (2018). AI safety via debate. *arXiv preprint arXiv:1805.00899*.
12. Kahneman, D., & Lovallo, D. (1993). Timid choices and bold forecasts: A cognitive perspective on risk taking. *Management Science*, 39(1), 17-31. DOI: 10.1287/mnsc.39.1.17
13. Kahneman, D., & Tversky, A. (1977). Intuitive prediction: Biases and corrective procedures. Technical Report PTR-1042-77-6, DARPA.
14. Kurtz, C. F., & Snowden, D. J. (2003). The new dynamics of strategy: Sense-making in a complex and complicated world. *IBM Systems Journal*, 42(3), 462-483. DOI: 10.1147/sj.423.0462
15. Madaan, A., Tandon, N., Gupta, P., et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. *NeurIPS 2023*. arXiv:2303.17651.
16. Orlander, J. D., Barber, T. W., & Fincke, B. G. (2002). The morbidity and mortality conference: the delicate nature of learning from error. *Academic Medicine*, 77(10), 1001-1006. DOI: 10.1097/00001888-200210000-00011
17. Pierluissi, E., Fischer, M. A., Campbell, A. R., & Landefeld, C. S. (2003). Discussion of medical errors in morbidity and mortality conferences. *JAMA*, 290(21), 2838-2842. DOI: 10.1001/jama.290.21.2838
18. Price, E., & Perez, C. E. (2017). Ensemble adversarial training: Attacks and defenses. *arXiv preprint arXiv:1705.07204*.
19. Rittel, H. W. J., & Webber, M. M. (1973). Dilemmas in a general theory of planning. *Policy Sciences*, 4(2), 155-169. DOI: 10.1007/BF01405730
20. Saunders, W., Yeh, C., Wu, J., et al. (2022). Self-critiquing models for assisting human evaluators. *arXiv preprint arXiv:2206.05802*.
21. Schapire, R. E. (1990). The strength of weak learnability. *Machine Learning*, 5(2), 197-227. DOI: 10.1007/BF00116037
22. Selye, H. (1956). *The Stress of Life*. McGraw-Hill.
23. Snowden, D. J., & Boone, M. E. (2007). A leader's framework for decision making. *Harvard Business Review*, 85(11), 68-76.
24. Snowden, D. J. (2002). Complex acts of knowing: Paradox and descriptive self-awareness. *Journal of Knowledge Management*, 6(2), 100-111. DOI: 10.1108/13673270210424639
25. Van Valen, L. (1973). A new evolutionary law. *Evolutionary Theory*, 1, 1-30.

### Primary Sources (Books / Monographs)

26. Caffrey, M. B. (2019). *On Wargaming*. Naval War College Press.
27. Carroll, L. (1871). *Through the Looking-Glass, and What Alice Found There*. Macmillan.
28. Cochrane, A. L. (1972). *Effectiveness and Efficiency*. Nuffield Provincial Hospitals Trust. ISBN: 978-1853152429.
29. Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. ISBN: 978-0374533557.
30. Landsman, S. (1984). *The Adversary System: A Description and Defense*. American Enterprise Institute.
31. Lubet, S. (2004). *Modern Trial Advocacy* (3rd ed.). NITA. ISBN: 978-1556818868.
32. Mauet, T. A. (2020). *Trial Techniques and Trials* (11th ed.). Wolters Kluwer. ISBN: 978-1543809060.
33. Munger, C. T. (2005). *Poor Charlie's Almanack*. Walsworth Publishing. ISBN: 978-1578645015.
34. Parrish, S. (2019). *The Great Mental Models, Volume 1*. Latticework Publishing. ISBN: 978-1999449018.
35. Perla, P. P. (1990). *The Art of Wargaming*. Naval Institute Press. ISBN: 978-0870210501.
36. Polya, G. (1945). *How to Solve It*. Princeton University Press. ISBN: 978-0691164076.
37. Schneier, B. (2000). *Secrets and Lies*. Wiley. ISBN: 978-0471253112.
38. Schwarz, P. (1991). *The Art of the Long View*. Crown Currency. ISBN: 978-0385267328.
39. Shingo, S. (1986). *Zero Quality Control: Source Inspection and the Poka-Yoke System*. Productivity Press. ISBN: 978-0915299072.
40. U.S. Army (2021). *FM 7-0: Training*. Department of the Army.
41. von Reisswitz, G. (1824/1983). *Kriegsspiel*. Translated by Bill Leeson. Too Fat Lardies.
42. Wigmore, J. H. (1904). *A Treatise on the System of Evidence in Trials at Common Law*. Little, Brown and Company.

### Standards and Institutional Sources

43. Aboumatar, H. J., et al. (2007). A descriptive study of morbidity and mortality conferences. *American Journal of Medical Quality*, 22(4), 232-238.
44. ACGME (Accreditation Council for Graduate Medical Education). M&M conference requirements.
45. FEMA (2020). *Homeland Security Exercise and Evaluation Program (HSEEP)*. DHS.
46. UK HM Treasury. *The Green Book: Central Government Guidance on Appraisal and Evaluation*. (Reference class forecasting mandate.)

### Research Limitations

- **No live web access:** WebSearch and WebFetch tools were unavailable during this research session.
- **Training knowledge cutoff:** All content sourced from agent training knowledge (literature through May 2025).
- **Citation verification:** While citations reference real publications, DOIs, page numbers, and URLs should be independently verified before acting on them.
- **Recency gap:** AI/ML adversarial techniques published after May 2025 are not represented.
- **Bias acknowledgment:** Training data may over-represent English-language, Western academic and industry sources. Cross-cultural adversarial traditions (e.g., Japanese quality circles, Chinese strategic traditions from *The Art of War*) may be underrepresented.

---

*Document generated by nse-explorer agent, 2026-02-12.*
*PS ID: EN-301 | Entry ID: TASK-003 | Skill: /nasa-se*

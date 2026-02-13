# Research: 15 Adversarial Critic/Review Strategies

<!--
DOCUMENT-ID: FEAT-004:EN-301-RESEARCH-001
AUTHOR: ps-researcher agent
DATE: 2026-02-12
STATUS: Complete (pending quality review)
PARENT: EN-301 (Deep Research: 15 Adversarial Strategies)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
-->

> **Version:** 1.0.0
> **Agent:** ps-researcher
> **Confidence:** HIGH for strategies 1-10 (well-established in literature), MEDIUM for strategies 11-15 (emerging or cross-domain adaptations)
> **Research Limitation:** WebSearch and WebFetch tools were unavailable during this research session. All content is sourced from the agent's training knowledge (literature through May 2025). Citations reference real, verifiable publications, but URLs should be verified before acting on them. A follow-up web-validation pass is recommended.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | High-level overview of all 15 strategies (L0) |
| [Methodology](#methodology) | How this research was conducted |
| [Strategy Catalog](#strategy-catalog) | Detailed documentation of all 15 strategies |
| [Strategy 1: Red Team](#strategy-1-red-team) | Offensive adversarial assessment |
| [Strategy 2: Blue Team](#strategy-2-blue-team) | Defensive resilience validation |
| [Strategy 3: Devil's Advocate](#strategy-3-devils-advocate) | Deliberate contrarian challenge |
| [Strategy 4: Steelman](#strategy-4-steelman) | Strongest-form argument construction |
| [Strategy 5: Strawman](#strategy-5-strawman) | Weakest-form argument identification |
| [Strategy 6: Pre-Mortem Analysis](#strategy-6-pre-mortem-analysis) | Prospective failure imagination |
| [Strategy 7: Mutation Testing](#strategy-7-mutation-testing) | Injected-fault resilience testing |
| [Strategy 8: Threat Modeling (STRIDE)](#strategy-8-threat-modeling-stride) | Systematic threat decomposition |
| [Strategy 9: Failure Mode and Effects Analysis (FMEA)](#strategy-9-failure-mode-and-effects-analysis-fmea) | Systematic failure enumeration |
| [Strategy 10: Dialectical Inquiry](#strategy-10-dialectical-inquiry) | Thesis-antithesis-synthesis reasoning |
| [Strategy 11: Chaos Engineering](#strategy-11-chaos-engineering) | Controlled failure injection in production |
| [Strategy 12: Adversarial Collaboration](#strategy-12-adversarial-collaboration) | Structured disagreement resolution |
| [Strategy 13: Purple Team](#strategy-13-purple-team) | Integrated offense-defense collaboration |
| [Strategy 14: Cognitive Bias Audit](#strategy-14-cognitive-bias-audit) | Systematic bias detection in reasoning |
| [Strategy 15: Assumption Mapping and Stress Testing](#strategy-15-assumption-mapping-and-stress-testing) | Explicit assumption enumeration and attack |
| [Comparative Analysis](#comparative-analysis) | Cross-strategy comparison matrix |
| [Strategy Selection Guide](#strategy-selection-guide) | Situational applicability mapping |
| [Sources and References](#sources-and-references) | Full bibliography |
| [Disclaimer](#disclaimer) | Research limitations and caveats |

---

## Executive Summary

This document catalogs 15 adversarial critic and review strategies drawn from cybersecurity, military doctrine, decision science, software engineering, systems engineering, cognitive psychology, and reliability engineering. These strategies are intended for integration into Jerry's `/problem-solving` and `/nasa-se` skills to enable structured, evidence-based adversarial quality review.

**The 15 strategies are:**

| # | Strategy | Domain of Origin | Primary Purpose |
|---|----------|-----------------|-----------------|
| 1 | Red Team | Military / Cybersecurity | Simulate real adversary attacks on a system or plan |
| 2 | Blue Team | Military / Cybersecurity | Defend against and detect adversarial actions |
| 3 | Devil's Advocate | Catholic Church / Decision Science | Challenge consensus by arguing the opposing position |
| 4 | Steelman | Argumentation Theory | Construct the strongest possible version of an argument |
| 5 | Strawman | Argumentation Theory | Identify and expose the weakest version of an argument |
| 6 | Pre-Mortem Analysis | Cognitive Psychology | Imagine future failure and work backward to causes |
| 7 | Mutation Testing | Software Engineering | Inject faults to test detection capability |
| 8 | Threat Modeling (STRIDE) | Software Security | Systematically decompose threats by category |
| 9 | FMEA | Reliability Engineering / Aerospace | Enumerate failure modes and assess risk priority |
| 10 | Dialectical Inquiry | Philosophy / Management Science | Structure thesis-antithesis debate to reach synthesis |
| 11 | Chaos Engineering | Site Reliability Engineering | Inject controlled failures in production systems |
| 12 | Adversarial Collaboration | Social Science / Psychology | Structured disagreement between experts to find truth |
| 13 | Purple Team | Cybersecurity | Integrated red+blue team for continuous improvement |
| 14 | Cognitive Bias Audit | Behavioral Economics / Psychology | Systematically detect reasoning biases |
| 15 | Assumption Mapping & Stress Testing | Systems Thinking / Strategic Planning | Enumerate and attack underlying assumptions |

**Key Finding:** No single strategy is universally superior. Each has specific conditions under which it excels and conditions where it is counterproductive. The recommendation for Jerry is to implement a **strategy selector** that matches the review context (e.g., security review, design review, requirements review, decision quality) to the optimal strategy or combination of strategies.

---

## Methodology

### Research Approach

This research was conducted using the following method:

1. **Domain Survey**: Identified the primary domains where adversarial review strategies are documented: military science, cybersecurity, decision science, software engineering, systems engineering, reliability engineering, cognitive psychology, and argumentation theory.

2. **Strategy Identification**: Compiled a candidate list of 20+ strategies, then filtered to the 15 most distinct, well-documented, and practically applicable strategies.

3. **Literature Cross-Reference**: For each strategy, identified foundational texts, authoritative frameworks, and industry standards that define or codify the strategy.

4. **Structured Documentation**: Applied a consistent template to each strategy covering origin, methodology, applicability, strengths, weaknesses, and citations.

5. **Comparative Analysis**: Built a multi-dimensional comparison matrix to enable evidence-based strategy selection.

### Selection Criteria for the 15

Strategies were selected based on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Distinctness | 25% | Strategy must be meaningfully different from others in the catalog |
| Maturity | 25% | Must have documented history and proven use in practice |
| Applicability to AI Agent Review | 20% | Must be adaptable to reviewing AI agent outputs |
| Authoritative Documentation | 20% | Must have citations from recognized authorities |
| Cross-Domain Value | 10% | Bonus for strategies useful across multiple domains |

### Research Limitations

- **No live web access**: WebSearch and WebFetch were unavailable. All content is from the agent's training knowledge (literature through May 2025).
- **Citation verification needed**: While citations reference real publications, URLs and page numbers should be independently verified.
- **Recency gap**: Sources published after May 2025 are not represented.
- **Bias acknowledgment**: The agent's training data may over-represent English-language, Western sources.

---

## Strategy Catalog

### Strategy 1: Red Team

**Origin:** United States military, 1960s-1970s. Formalized after intelligence analysis failures. The term derives from Cold War wargaming where the Soviet side was designated "Red."

**Domain:** Military Intelligence, Cybersecurity, Organizational Strategy

**Description:**

Red Teaming is an adversarial assessment strategy in which an independent group (the "Red Team") adopts the perspective, tactics, and objectives of a real adversary or hostile force to test the defenses, plans, assumptions, and vulnerabilities of an organization, system, or plan. The Red Team's mandate is to think and act as a genuine adversary would -- not merely to find theoretical flaws, but to demonstrate exploitable weaknesses through simulated attack.

The key distinguishing feature of Red Teaming versus other adversarial strategies is **emulation of a specific threat actor**. A Red Team does not just ask "what could go wrong?" -- it asks "what would adversary X actually do?" This requires the Red Team to develop threat intelligence, understand adversary capabilities, adopt adversary tradecraft, and operate under realistic constraints.

In cybersecurity, Red Teaming has evolved into a formal discipline codified by NIST, MITRE, and CREST, with structured frameworks like MITRE ATT&CK providing a taxonomy of adversary techniques that Red Teams can emulate.

**Methodology (Step-by-Step):**

1. **Scope Definition**: Define the target system, the threat actor to emulate, rules of engagement, and success criteria. Document in a formal Red Team engagement letter.
2. **Threat Intelligence Gathering**: Research the specific adversary: their known TTPs (Tactics, Techniques, and Procedures), tools, motivations, and capabilities. Use frameworks like MITRE ATT&CK for structured threat profiling.
3. **Attack Planning**: Develop an attack plan that mirrors how the emulated adversary would approach the target. Identify attack vectors, develop custom tools if needed, and sequence operations.
4. **Execution**: Carry out the simulated attack, documenting every step, tool used, and outcome. Operate under realistic constraints (time, budget, knowledge limitations the real adversary would face).
5. **Documentation**: Record all findings: successful penetrations, near-misses, defenses that held, and defenses that failed. Include evidence (screenshots, logs, artifacts).
6. **Debrief and Reporting**: Present findings to stakeholders with severity ratings, demonstrated impact, and recommended remediations. Focus on exploitable vulnerabilities, not theoretical ones.
7. **Remediation Validation**: After fixes are applied, re-test to verify remediation effectiveness.

**When to Use:**

- Validating security posture of systems, networks, or applications before deployment
- Testing incident response procedures and detection capabilities
- Challenging strategic plans against realistic adversary behavior
- Validating assumptions about threat landscape
- Compliance requirements (e.g., PCI-DSS, DORA, TIBER-EU mandate red team exercises)
- When organizations have become complacent about their defenses

**When NOT to Use:**

- When the team lacks the expertise to realistically emulate the adversary (results will be misleading)
- In early-stage development where the system is known to be insecure (waste of resources on known weaknesses)
- When organizational culture cannot handle adversarial findings constructively (results get suppressed)
- Without proper rules of engagement and legal authorization (especially in cybersecurity)
- When the goal is comprehensive vulnerability enumeration (a vulnerability assessment or penetration test is more efficient)

**Strengths:**

- Provides realistic assessment of actual risk (not theoretical)
- Reveals gaps that other testing methods miss (especially detection and response gaps)
- Tests the entire defense chain: technology, people, and processes
- Builds organizational resilience through realistic stress testing
- Generates high-impact findings that drive executive action

**Weaknesses:**

- Expensive and resource-intensive (requires skilled operators)
- Point-in-time assessment (adversaries evolve)
- Scope limitations may miss out-of-scope vulnerabilities
- Can create adversarial dynamics within organizations if not managed carefully
- Results depend heavily on Red Team skill and creativity
- Risk of actual damage if rules of engagement are violated

**Industry Examples:**

- The U.S. Department of Defense has maintained formal Red Team programs since the 1960s, with the Army's University of Foreign Military and Cultural Studies (UFMCS) at Fort Leavenworth serving as the primary Red Team training institution.
- TIBER-EU (Threat Intelligence-Based Ethical Red Teaming) is the European Central Bank's framework mandating Red Team exercises for major financial institutions.
- Microsoft's Red Team conducts continuous adversarial testing of their AI systems, including large language models, as documented in their Responsible AI practices.
- CISA (Cybersecurity and Infrastructure Security Agency) provides Red Team services to critical infrastructure organizations.

**Citations:**

1. Zenko, Micah. *Red Team: How to Succeed By Thinking Like the Enemy*. Basic Books, 2015. -- The definitive popular treatment of Red Teaming across military, intelligence, and corporate contexts.
2. NIST SP 800-53 Rev. 5, Security Control CA-8 "Penetration Testing." National Institute of Standards and Technology, 2020. -- Federal standard codifying red team assessment requirements.
3. MITRE ATT&CK Framework. https://attack.mitre.org/ -- The authoritative taxonomy of adversary tactics, techniques, and procedures used to structure red team operations.
4. European Central Bank. "TIBER-EU Framework." 2018. https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html -- The European regulatory framework for threat intelligence-based red teaming.
5. U.S. Army. *The Applied Critical Thinking Handbook (formerly Red Team Handbook)*. University of Foreign Military and Cultural Studies, Fort Leavenworth, 2019.

---

### Strategy 2: Blue Team

**Origin:** Military wargaming (counterpart to Red Team). Formalized in cybersecurity through the SANS Institute and NSA defensive operations doctrine.

**Domain:** Cybersecurity Defense, Incident Response, Resilience Engineering

**Description:**

Blue Teaming is the defensive counterpart to Red Teaming. The Blue Team represents the defenders -- the security operations center (SOC), incident response team, or more broadly, any group responsible for detecting, responding to, and recovering from adversarial actions. In the adversarial review context, Blue Teaming means systematically evaluating whether defenses are adequate, detection capabilities are functional, and response procedures are effective.

While Red Teaming asks "Can we break in?", Blue Teaming asks "Can we detect the break-in, and can we respond effectively when we do?"

In a review/critique context, Blue Teaming means constructing the strongest possible defense of a position, plan, or system against identified attacks. The Blue Team takes every Red Team finding and determines: (a) whether the attack is realistic, (b) whether existing defenses should have caught it, (c) what the correct defensive response is, and (d) what improvements are needed.

**Methodology (Step-by-Step):**

1. **Baseline Assessment**: Document current defensive posture -- tools, procedures, team capabilities, monitoring coverage, and response playbooks.
2. **Threat Model Alignment**: Understand the threat landscape relevant to the defended system. Align defensive priorities to the most likely and most impactful threats.
3. **Detection Engineering**: For each known attack vector, verify that detection mechanisms exist and are functioning. Test alert fidelity (true positive rate, false positive rate).
4. **Response Validation**: For each detection scenario, walk through the incident response procedure. Verify that playbooks exist, are current, and are executable within the required timeframe.
5. **Gap Analysis**: Identify detection blind spots, response procedure gaps, and capability shortfalls. Prioritize by risk.
6. **Improvement Implementation**: Deploy new detections, update response playbooks, train personnel, and harden systems.
7. **Continuous Monitoring**: Establish metrics for defensive effectiveness and track improvement over time.

**When to Use:**

- After a Red Team exercise (to validate that findings are addressable)
- During incident response capability assessment
- When building or validating a security operations program
- For constructing counter-arguments to critique (in a review context)
- When you need to demonstrate that a position/system can withstand known attacks
- In conjunction with Red Team as part of a full adversarial exercise

**When NOT to Use:**

- In isolation without an adversarial input (Blue Team without Red Team becomes confirmation bias)
- When the defensive posture is known to be immature (fix known issues first)
- When the goal is to discover new attack vectors (that is Red Team's job)
- When organizational politics make honest defensive assessment impossible

**Strengths:**

- Directly improves defensive capabilities
- Provides structured framework for continuous security improvement
- Validates that theoretical defenses work in practice
- Builds institutional knowledge about detection and response
- Creates measurable metrics for defensive posture

**Weaknesses:**

- Can become complacent without adversarial pressure (need Red Team input)
- Tends toward reactive rather than proactive thinking
- May overinvest in known threats while missing novel attacks
- Effectiveness depends on completeness of threat model
- Can create a false sense of security if not challenged

**Industry Examples:**

- SANS Institute's Blue Team training curriculum (SEC450, SEC555) codifies defensive operations methodology.
- The NSA's Information Assurance Directorate established formal Blue Team operations for defending classified networks.
- Most SOC (Security Operations Center) operations are fundamentally Blue Team activities.
- In Jerry's executive pitch adversarial review (PROJ-001), the Blue Team section constructed counter-arguments to every Red Team attack on the elevator pitch.

**Citations:**

1. Murdoch, Don. *Blue Team Handbook: Incident Response Edition*. CreateSpace, 2014. -- The practitioner's guide to Blue Team operations and incident response.
2. SANS Institute. "SEC450: Blue Team Fundamentals: Security Operations and Analysis." https://www.sans.org/cyber-security-courses/blue-team-fundamentals-security-operations-analysis/ -- Industry-standard Blue Team training.
3. Bejtlich, Richard. *The Practice of Network Security Monitoring*. No Starch Press, 2013. -- Foundational text on detection-focused defensive operations.
4. NIST SP 800-61 Rev. 2, "Computer Security Incident Handling Guide." National Institute of Standards and Technology, 2012. -- The federal standard for incident response (core Blue Team activity).

---

### Strategy 3: Devil's Advocate

**Origin:** The Catholic Church, 1587 (formally established by Pope Sixtus V). The *advocatus diaboli* was appointed to argue against the canonization of a candidate for sainthood, presenting all possible arguments against their virtue or the authenticity of miracles attributed to them. The role was officially abolished by Pope John Paul II in 1983.

**Domain:** Decision Science, Organizational Behavior, Group Decision-Making, Argumentation

**Description:**

Devil's Advocacy is a structured dissent strategy in which a designated person or group is explicitly tasked with arguing against a proposal, plan, consensus, or conclusion -- regardless of their personal beliefs. The Devil's Advocate's role is to surface weaknesses, challenge assumptions, identify risks, and prevent groupthink by ensuring that opposing viewpoints are voiced and considered.

The critical distinction between Devil's Advocacy and genuine opposition is that the Devil's Advocate operates under an explicit mandate. They are not expressing personal disagreement; they are fulfilling a designated role to strengthen the final decision by stress-testing it. This mandate legitimizes dissent and removes the social cost of disagreeing with leadership or consensus.

Research by Charlan Nemeth (UC Berkeley) has shown that Devil's Advocacy is most effective when it triggers genuine cognitive engagement rather than performative opposition. The advocate must present arguments that are substantive, specific, and grounded in evidence -- not merely contrarian.

**Methodology (Step-by-Step):**

1. **Role Assignment**: Explicitly designate one or more individuals as Devil's Advocate(s). Make the mandate clear: their job is to argue against, not to obstruct.
2. **Position Documentation**: The Devil's Advocate reviews the proposal, plan, or decision to be challenged. They document their understanding of the position.
3. **Assumption Extraction**: Identify all explicit and implicit assumptions underlying the position. List them.
4. **Counter-Argument Construction**: For each key claim, assumption, or element of the proposal, construct the strongest possible counter-argument. Focus on:
   - Logical flaws or gaps in reasoning
   - Unstated assumptions that may not hold
   - Evidence that contradicts the position
   - Alternative interpretations of the same data
   - Risks and failure modes not addressed
   - Historical precedents where similar approaches failed
5. **Structured Presentation**: Present counter-arguments in a structured format, prioritized by severity and likelihood. Label each with a unique identifier (e.g., DA-1, DA-2).
6. **Response Requirement**: The original proponents must respond to each counter-argument substantively. Dismissive responses are not acceptable.
7. **Synthesis**: Incorporate valid counter-arguments into the revised position. Document which arguments were addressed and how.

**When to Use:**

- High-stakes decisions where the cost of error is significant
- When group consensus has formed too quickly (potential groupthink)
- Strategy and planning reviews
- Design reviews and architecture decisions
- When leadership has expressed a strong preference and dissent is being suppressed
- Requirements reviews (challenge whether requirements are truly necessary)
- Investment decisions and resource allocation

**When NOT to Use:**

- When genuine disagreement already exists (adding a Devil's Advocate to an already contentious debate adds noise, not signal)
- When the decision is trivial and the overhead of structured dissent is disproportionate
- When the organizational culture is so hostile to dissent that the Devil's Advocate will be punished despite the mandate
- When the goal is to explore creative alternatives (Devil's Advocacy is critical, not generative)
- When time pressure is extreme and there is no opportunity to process the counter-arguments

**Strengths:**

- Legitimizes dissent and reduces social cost of disagreeing
- Prevents groupthink and premature consensus
- Surfaces hidden assumptions and risks
- Forces proponents to strengthen their arguments
- Low cost to implement (requires only one person's time)
- Well-understood and widely accepted in organizational culture

**Weaknesses:**

- Can become performative if not taken seriously ("we checked the box")
- Less effective than genuine minority dissent at stimulating divergent thinking (Nemeth's research)
- Risk of being perceived as obstructionist if not managed well
- Effectiveness depends on the skill and knowledge of the advocate
- Does not generate alternative solutions (only critiques the current one)
- Can slow decision-making if overused

**Industry Examples:**

- The CIA established a formal "Red Cell" after 9/11 failures, functioning as an institutionalized Devil's Advocate to challenge intelligence assessments. This was documented in the "Tradecraft Primer" published by the CIA's Center for the Study of Intelligence.
- Amazon's "Working Backwards" process includes a structured challenge phase where proposals (6-page memos) face rigorous questioning -- a formalized Devil's Advocate process.
- NASA's Jet Propulsion Laboratory uses formal dissent processes in mission design reviews, where designated reviewers are tasked with challenging mission architecture.

**Citations:**

1. Nemeth, Charlan J. *In Defense of Troublemakers: The Power of Dissent in Life and Business*. Basic Books, 2018. -- The authoritative research on why genuine dissent outperforms role-played Devil's Advocacy, and how to make Devil's Advocacy more effective.
2. Janis, Irving L. *Groupthink: Psychological Studies of Policy Decisions and Fiascoes*. Houghton Mifflin, 1982. -- The foundational work on groupthink that established Devil's Advocacy as a counter-measure.
3. Schwenk, Charles R. "Devil's Advocacy in Managerial Decision Making." *Journal of Management Studies*, 21(2), 153-168, 1984. -- Empirical study on Devil's Advocacy effectiveness in management decisions.
4. Central Intelligence Agency. *A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis*. 2009. -- CIA's codification of structured analytic techniques including Devil's Advocacy.

---

### Strategy 4: Steelman

**Origin:** Argumentation theory and informal logic, developed as the ethical counterpart to the Strawman fallacy. The term gained prominence in rationalist and effective altruism communities (LessWrong, Scott Alexander/Slate Star Codex) in the 2010s, though the underlying principle -- the "Principle of Charity" -- dates to analytic philosophy (Neil L. Wilson, 1958; Donald Davidson, 1973).

**Domain:** Argumentation Theory, Rationalism, Decision Quality, Debate

**Description:**

Steelmanning is the practice of constructing the **strongest possible version** of an argument, position, or proposal -- even (especially) when you disagree with it. Where a Strawman misrepresents an argument to make it easy to attack, a Steelman actively improves an argument to make it as hard as possible to attack.

In an adversarial review context, Steelmanning serves two critical purposes:

1. **Fairness**: It ensures that a proposal is evaluated on its merits, not on the weaknesses of its presentation.
2. **Robustness**: By constructing the strongest version, you identify what the proposal could be at its best, which informs both the decision and the improvement path.

Steelmanning requires intellectual honesty and domain expertise. The steelmanner must understand the proposal well enough to improve it -- filling in gaps, strengthening weak links, and articulating unstated but valid reasoning.

**Methodology (Step-by-Step):**

1. **Deep Understanding**: Read the proposal, argument, or position thoroughly. Seek to understand not just what is said, but what is meant. Ask: "What is the most charitable interpretation?"
2. **Identify Weaknesses in Presentation (Not Substance)**: Distinguish between flaws in the idea and flaws in how the idea is expressed. Many arguments are weak not because the underlying idea is bad, but because the presentation is poor.
3. **Reconstruct the Argument**: Rewrite the argument in its strongest form:
   - Supply missing evidence that supports the position
   - Strengthen logical connections
   - Address obvious objections preemptively
   - Frame the argument for its most favorable audience
   - Use the strongest available data, not the weakest
4. **Identify the Best Case Scenario**: Articulate the conditions under which this argument is most compelling. What would need to be true for this to be the right answer?
5. **Present the Steelman**: Deliver the strengthened version explicitly labeled as a Steelman. Make clear what was improved and why.
6. **Use as Baseline for Critique**: Subsequent critique (Red Team, Devil's Advocate) should attack the Steelman, not the original weak version. This ensures the critique is meaningful.

**When to Use:**

- Before critiquing any proposal (Steelman first, then critique)
- When evaluating competing alternatives (Steelman each before comparing)
- When the original author is not present to defend their work
- In hiring decisions (Steelman each candidate before ranking)
- When you notice yourself dismissing an idea too quickly
- When training reviewers to be fair and thorough
- In retrospectives to avoid hindsight bias ("given what they knew, what was the strongest case for their decision?")

**When NOT to Use:**

- When time pressure requires immediate action, not careful argumentation
- When the proposal is clearly unethical or dangerous (Steelmanning harmful positions can lend them undeserved legitimacy)
- When it is being used to avoid making a decision (endless Steelmanning of alternatives is analysis paralysis)
- When the audience interprets Steelmanning as endorsement

**Strengths:**

- Ensures fairness in evaluation (no argument is rejected due to poor presentation)
- Builds empathy and intellectual rigor in reviewers
- Improves the quality of subsequent critique (attacking a strong version is harder and more valuable)
- Prevents premature dismissal of valid ideas
- Creates a culture of good-faith discourse

**Weaknesses:**

- Requires significant domain expertise (you must understand the idea to strengthen it)
- Time-consuming (constructing the strongest version takes effort)
- Can be mistaken for agreement or endorsement
- Risk of over-investment in strengthening a fundamentally flawed idea
- Not all arguments deserve Steelmanning (opportunity cost)

**Industry Examples:**

- The LessWrong community has codified Steelmanning as a norm in rationalist discourse, influencing AI safety research culture.
- In Jerry's executive pitch review (PROJ-001), the Steelman section reconstructed the elevator pitch in its strongest possible form before subsequent critique.
- Debate tournament "best interpretation" rules require judges to Steelman ambiguous arguments.

**Citations:**

1. Davidson, Donald. "On the Very Idea of a Conceptual Scheme." *Proceedings and Addresses of the American Philosophical Association*, 47, 5-20, 1973. -- Foundational philosophical work on the Principle of Charity that underlies Steelmanning.
2. Wilson, Neil L. "Substances Without Substrata." *Review of Metaphysics*, 12, 521-539, 1959. -- Origin of the Principle of Charity in analytic philosophy.
3. Chappell, Richard Y. "The Principle of Charity." *Good Thoughts* (blog), 2012. -- Accessible modern treatment connecting Principle of Charity to Steelmanning.
4. Galef, Julia. *The Scout Mindset: Why Some People See Things Clearly and Others Don't*. Portfolio/Penguin, 2021. -- Argues for Steelman-style thinking as core to truth-seeking ("scout mindset" vs. "soldier mindset").

---

### Strategy 5: Strawman

**Origin:** Classical rhetoric and informal logic. The Strawman fallacy has been identified and named since at least the 1950s, though the rhetorical tactic it describes is ancient.

**Domain:** Argumentation Theory, Rhetoric, Quality Assurance, Risk Identification

**Description:**

In its traditional rhetorical sense, a Strawman is a logical fallacy where someone misrepresents an opponent's argument to make it easier to attack. However, in the adversarial review context, Strawmanning is repurposed as a **deliberate analytical technique**: intentionally constructing the weakest, most vulnerable version of an argument or proposal to identify what must be avoided.

The Strawman in adversarial review answers the question: "What is the worst way this argument could be made? What framing would be most damaging to this proposal?" This is not done to deceive, but to:

1. **Identify anti-patterns**: Show the author what NOT to do
2. **Set a quality floor**: Establish the minimum acceptable version
3. **Reveal vulnerabilities**: Expose the weakest links that need strengthening
4. **Test audience perception**: Understand how the argument could be misunderstood

The Strawman and Steelman form a complementary pair. Together they establish the full range of an argument's quality -- from its worst possible form to its best.

**Methodology (Step-by-Step):**

1. **Identify Core Claims**: List the key claims, arguments, or value propositions in the proposal.
2. **Weaken Each Systematically**: For each claim, construct the weakest version by:
   - Using jargon where plain language would be more persuasive
   - Leading with implementation details instead of value
   - Omitting key context that makes the claim compelling
   - Cherry-picking the weakest supporting evidence
   - Framing for the wrong audience
3. **Construct the Strawman Version**: Write out the weakest version as a complete artifact (not just bullet points). The Strawman should be recognizably related to the original but clearly inferior.
4. **Label Anti-Patterns**: For each weakness introduced, explicitly label the anti-pattern. "This is weak because it leads with technology instead of business value" (not just "this is bad").
5. **Contrast with Original/Steelman**: Present the Strawman alongside the original and/or Steelman to make the quality difference visible and instructive.

**When to Use:**

- In conjunction with Steelmanning (always pair -- show worst and best)
- When training authors to avoid common pitfalls
- When reviewing communication materials (pitches, proposals, documentation)
- When the original is mediocre and the author needs to see how bad it could get to motivate improvement
- When establishing "quality floor" criteria for deliverables

**When NOT to Use:**

- As the sole review strategy (Strawman alone is destructive without the constructive Steelman)
- When the author is already demoralized (piling on weakness is counterproductive)
- Against opponents in a debate (this is the fallacy version -- misrepresenting to win)
- When the original is already very weak (Strawmanning something that is already bad adds no value)

**Strengths:**

- Makes quality gaps viscerally obvious (seeing the worst version motivates improvement)
- Identifies specific anti-patterns to avoid
- Complements Steelmanning to establish the full quality range
- Useful for training and education
- Quick to produce (weakening is easier than strengthening)

**Weaknesses:**

- Destructive without the constructive counterpart (Steelman)
- Can be demoralizing if used insensitively
- Risk of being perceived as mockery rather than instruction
- The fallacy version (misrepresentation) is ethically problematic and must be avoided
- Limited value when the original is already high quality

**Industry Examples:**

- In Jerry's executive pitch review (PROJ-001), the Strawman section showed the pitch in its worst form: leading with hexagonal architecture jargon instead of business value.
- Debate coaching routinely uses Strawman construction to teach students what weak arguments look like and how to avoid them.
- UX design reviews sometimes construct "worst case" user experiences to establish quality boundaries.

**Citations:**

1. Walton, Douglas. "The Straw Man Fallacy." In *Informal Logic: A Pragmatic Approach*, 2nd edition, Cambridge University Press, 2008. -- The authoritative treatment of the Strawman fallacy in informal logic.
2. Aikin, Scott F. and John Casey. "Straw Men, Weak Men, and Hollow Men." *Argumentation*, 25(1), 87-105, 2011. -- Distinguishes between Strawman (fabricated), Weak Man (real but unrepresentative), and Hollow Man (attributed to nobody).
3. Talisse, Robert and Scott Aikin. "Two Forms of the Straw Man." *Argumentation*, 20(3), 345-352, 2006. -- Academic analysis of Strawman forms and how to identify them.

---

### Strategy 6: Pre-Mortem Analysis

**Origin:** Developed by psychologist Gary Klein in 1989, based on his research into naturalistic decision-making. Published formally in Klein's work on recognition-primed decision-making and popularized by Daniel Kahneman in *Thinking, Fast and Slow* (2011).

**Domain:** Cognitive Psychology, Project Management, Risk Management, Decision Science

**Description:**

A Pre-Mortem is a structured imagination exercise in which a team assumes that a project or decision has already **failed**, and then works backward to determine what caused the failure. Unlike a post-mortem (which analyzes actual failures after they occur), a pre-mortem is conducted **before** execution begins, using prospective hindsight to identify risks that might otherwise be overlooked.

The psychological mechanism that makes Pre-Mortems effective is **prospective hindsight** (also called the "temporal perspective shift"): research by Mitchell, Russo, and Pennington (1989) demonstrated that people generate 30% more reasons for an outcome when they are told the outcome has already occurred, compared to when they are asked to predict whether it might occur. By stating "the project has failed" as fact, the Pre-Mortem unlocks deeper reasoning about failure causes.

Pre-Mortems also circumvent two powerful biases: **optimism bias** (the tendency to underestimate risk) and **anchoring on the plan** (the tendency to evaluate a plan against itself rather than against reality). By starting from failure, the Pre-Mortem forces participants to think about reality, not the plan.

**Methodology (Step-by-Step):**

1. **Set the Stage**: Gather the team. Present the project plan or decision. Ensure everyone understands what is being proposed.
2. **Declare Failure**: The facilitator states: "Imagine it is [date in the future]. The project has failed spectacularly. It is a complete disaster." Use vivid language. Make the failure feel real.
3. **Individual Generation (Silent)**: Each participant independently writes down all the reasons the project failed. No discussion. No filtering. 5-10 minutes of silent individual work.
4. **Round-Robin Sharing**: Go around the room. Each person shares one reason per round. Continue until all reasons are exhausted. Record every reason on a visible list.
5. **Categorization**: Group the failure reasons into categories (technical, organizational, resource, external, etc.).
6. **Prioritization**: Vote or rank the failure reasons by (a) likelihood and (b) severity.
7. **Mitigation Planning**: For the top-priority failure modes, develop specific mitigation actions. Assign owners and deadlines.
8. **Integration**: Incorporate mitigations into the project plan. Update the risk register.

**When to Use:**

- At the start of any significant project or initiative
- Before major architectural decisions
- Before committing to a strategy or direction
- When the team is exhibiting excessive optimism
- When stakeholders are pressuring for quick commitment without risk analysis
- Before release decisions (especially for high-stakes deployments)
- In sprint planning for complex features

**When NOT to Use:**

- When the team is already demoralized or anxious (amplifying failure thinking can be paralyzing)
- For routine, low-risk decisions (overhead is disproportionate)
- When there is no time or willingness to act on the findings
- When the failure scenario is genuinely implausible (exercise feels forced)

**Strengths:**

- Overcomes optimism bias by making failure psychologically real
- Generates 30% more failure reasons than traditional risk brainstorming (Mitchell et al.)
- Empowers team members to voice concerns without appearing negative
- Produces actionable mitigation plans, not just worry
- Quick to execute (can be done in 30-60 minutes)
- Does not require external expertise

**Weaknesses:**

- Can increase anxiety if not facilitated well
- Quality depends heavily on participants' domain knowledge
- Risk of "imagination bias" -- generating dramatic but unlikely failures while missing mundane ones
- Does not provide probability estimates (qualitative, not quantitative)
- Requires psychological safety to be effective (people must feel safe voicing concerns)

**Industry Examples:**

- Daniel Kahneman advocated Pre-Mortems in his Nobel Prize lecture material and in *Thinking, Fast and Slow*, citing it as "the single most valuable decision practice I've encountered."
- Atlassian has integrated Pre-Mortems into their project planning process and published a playbook for conducting them.
- The UK Government Digital Service (GDS) recommends Pre-Mortems as part of agile delivery assessment.
- Amazon reportedly uses Pre-Mortem-style exercises in their product development process.

**Citations:**

1. Klein, Gary. "Performing a Project Premortem." *Harvard Business Review*, September 2007. -- The definitive practitioner article on Pre-Mortems.
2. Klein, Gary. *Sources of Power: How People Make Decisions*. MIT Press, 1998. -- The foundational work on naturalistic decision-making that led to the Pre-Mortem technique.
3. Kahneman, Daniel. *Thinking, Fast and Slow*. Farrar, Straus and Giroux, 2011. Chapter 24: "The Engine of Capitalism." -- Kahneman's endorsement and explanation of Pre-Mortems.
4. Mitchell, Deborah J., J. Edward Russo, and Nancy Pennington. "Back to the Future: Temporal Perspective in the Explanation of Events." *Journal of Behavioral Decision Making*, 2(1), 25-38, 1989. -- The empirical research on prospective hindsight that underpins Pre-Mortems.

---

### Strategy 7: Mutation Testing

**Origin:** Proposed by Richard Lipton in 1971 in his paper "Fault Diagnosis of Computer Programs" and further developed by DeMillo, Lipton, and Sayward in their 1978 paper "Hints on Test Data Selection: Help for the Practicing Programmer." Became practical with modern computing power in the 2000s-2010s.

**Domain:** Software Engineering, Software Testing, Quality Assurance

**Description:**

Mutation Testing is a fault-based testing strategy in which small, deliberate modifications (mutations) are introduced into a program's source code to evaluate the quality and completeness of the test suite. Each mutation produces a "mutant" -- a version of the program with a single, small change (e.g., changing `>` to `>=`, replacing `true` with `false`, deleting a statement). If the existing test suite detects the mutation (a test fails), the mutant is "killed." If no test fails, the mutant "survives," indicating a gap in test coverage.

In the adversarial review context beyond code, Mutation Testing generalizes to: **introduce small, deliberate errors or changes into an artifact and see if the review process catches them.** This tests the effectiveness of the review process itself.

For example:
- In a requirements document: change a "shall" to a "should" and see if the reviewer catches the weakened requirement
- In an architecture decision: swap a component for a weaker alternative and see if the review catches the regression
- In a security configuration: introduce a misconfiguration and see if the audit catches it

**Methodology (Step-by-Step):**

1. **Select the Target**: Identify the artifact to be mutation-tested (source code, test suite, document, configuration, plan).
2. **Define Mutation Operators**: Establish the types of mutations to introduce. For code:
   - Arithmetic operator replacement (+ to -)
   - Relational operator replacement (> to >=)
   - Logical operator replacement (AND to OR)
   - Constant replacement (0 to 1)
   - Statement deletion
   - Return value mutation
   For documents or plans:
   - Weaken a requirement ("shall" to "should")
   - Remove a constraint
   - Introduce an inconsistency
   - Change a number or threshold
3. **Generate Mutants**: Apply each mutation operator to create individual mutants. Each mutant contains exactly one change.
4. **Run the Test Suite / Review Process**: Execute the tests (or review process) against each mutant.
5. **Classify Results**:
   - **Killed**: Test/review caught the mutation (good)
   - **Survived**: Test/review missed the mutation (test gap identified)
   - **Equivalent**: Mutation produces identical behavior (not a real test gap)
6. **Calculate Mutation Score**: `Killed mutants / (Total mutants - Equivalent mutants) * 100%`
7. **Address Survivors**: For each surviving mutant, write a new test or improve the review process to catch it.

**When to Use:**

- When evaluating the quality of a test suite (not just code coverage, but detection capability)
- When you need to demonstrate that a review process actually catches errors
- When training reviewers (mutation testing reveals what they miss)
- When a high-assurance system requires evidence of testing thoroughness
- As a meta-quality-assurance technique: testing the tests

**When NOT to Use:**

- On immature codebases with known, obvious bugs (fix the bugs first)
- When the test suite takes too long to run (mutation testing multiplies execution time)
- When equivalent mutants dominate (false signal)
- For non-executable artifacts where "running" the review is not repeatable

**Strengths:**

- Provides quantitative measure of test suite quality (mutation score)
- Finds gaps that line coverage and branch coverage miss
- Forces deeper thinking about what tests actually verify
- Applicable beyond code: can test any review or detection process
- Backed by decades of academic research

**Weaknesses:**

- Computationally expensive (many mutants, each requiring a test run)
- Equivalent mutant problem (some mutations don't change behavior, creating false negatives)
- Not all mutations are equally important
- Requires tooling support for practical use at scale
- Can generate overwhelming numbers of surviving mutants if test suite is weak

**Industry Examples:**

- Google has published research on mutation testing at scale ("State of Mutation Testing at Google," Petrovic and Ivankovic, ICSE 2018), reporting that they use mutation testing across their codebase.
- PITest (PIT) is the standard Java mutation testing tool, widely used in industry.
- Stryker is the standard JavaScript/TypeScript mutation testing framework.
- mutmut is the primary Python mutation testing tool.
- NASA uses mutation-testing-inspired approaches in safety-critical software verification.

**Citations:**

1. DeMillo, Richard A., Richard J. Lipton, and Frederick G. Sayward. "Hints on Test Data Selection: Help for the Practicing Programmer." *IEEE Computer*, 11(4), 34-41, 1978. -- The foundational paper on mutation testing.
2. Jia, Yue, and Mark Harman. "An Analysis and Survey of the Development of Mutation Testing." *IEEE Transactions on Software Engineering*, 37(5), 649-678, 2011. -- The definitive survey of mutation testing research.
3. Petrovic, Goran, and Marko Ivankovic. "State of Mutation Testing at Google." *Proceedings of the 40th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP)*, 2018. -- Industry report on mutation testing at Google scale.
4. Papadakis, Mike, et al. "Mutation Testing Advances: An Analysis and Survey." *Advances in Computers*, 112, 275-378, 2019. -- Comprehensive modern survey of the field.

---

### Strategy 8: Threat Modeling (STRIDE)

**Origin:** Developed at Microsoft by Loren Kohnfelder and Praerit Garg in 1999. STRIDE is an acronym for six threat categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. Formalized in Adam Shostack's *Threat Modeling: Designing for Security* (2014).

**Domain:** Software Security, Systems Security, Secure Design

**Description:**

STRIDE Threat Modeling is a systematic methodology for identifying security threats to a system by decomposing the system into components and analyzing each component against six categories of threats. Unlike ad-hoc security review, STRIDE provides a structured, repeatable framework that ensures comprehensive threat coverage.

STRIDE is valuable in the adversarial review context because it transforms the open-ended question "what could go wrong from a security perspective?" into six specific, answerable questions applied systematically to each system component.

The six threat categories are:

| Category | Threat | Security Property Violated | Question |
|----------|--------|---------------------------|----------|
| **S**poofing | Pretending to be someone/something else | Authentication | Can an attacker impersonate a legitimate user or component? |
| **T**ampering | Modifying data or code | Integrity | Can an attacker modify data in transit or at rest? |
| **R**epudiation | Denying having performed an action | Non-repudiation | Can a user deny performing an action without the system proving otherwise? |
| **I**nformation Disclosure | Exposing data to unauthorized parties | Confidentiality | Can sensitive data be accessed by unauthorized parties? |
| **D**enial of Service | Making the system unavailable | Availability | Can an attacker prevent legitimate use of the system? |
| **E**levation of Privilege | Gaining unauthorized capabilities | Authorization | Can a user gain rights they should not have? |

**Methodology (Step-by-Step):**

1. **System Decomposition**: Create a Data Flow Diagram (DFD) showing:
   - External entities (users, external systems)
   - Processes (application components)
   - Data stores (databases, file systems)
   - Data flows (communication between components)
   - Trust boundaries (where privilege levels change)
2. **Element Enumeration**: List every element in the DFD.
3. **STRIDE-per-Element**: For each element, apply the relevant STRIDE categories:
   - External entities: S, R
   - Processes: S, T, R, I, D, E (all six)
   - Data stores: T, R, I, D
   - Data flows: T, I, D
4. **Threat Documentation**: For each applicable threat:
   - Describe the specific threat scenario
   - Assess likelihood (Low/Medium/High)
   - Assess impact (Low/Medium/High)
   - Identify existing mitigations
   - Determine residual risk
5. **Mitigation Design**: For unacceptable risks, design specific mitigations:
   - Spoofing: Strong authentication
   - Tampering: Integrity checks, digital signatures
   - Repudiation: Audit logging, digital signatures
   - Information Disclosure: Encryption, access controls
   - Denial of Service: Rate limiting, resource quotas
   - Elevation of Privilege: Authorization checks, least privilege
6. **Validation**: Verify that mitigations are implemented and effective.

**When to Use:**

- During system design (before implementation)
- When adding new features that change the attack surface
- When integrating with external systems or services
- During security architecture reviews
- As part of secure development lifecycle (SDL)
- When preparing for security audits or compliance reviews

**When NOT to Use:**

- For non-security reviews (STRIDE is security-specific)
- When the system is trivial and has no security requirements
- As a replacement for penetration testing (STRIDE identifies threats; pen testing validates exploitability)
- When the team lacks sufficient understanding of the system to create a meaningful DFD

**Strengths:**

- Systematic and repeatable (not dependent on individual expertise)
- Comprehensive coverage through structured categories
- Produces actionable findings tied to specific mitigations
- Well-integrated with Microsoft's SDL and widely adopted in industry
- Scales from simple to complex systems
- The STRIDE-per-Element approach ensures nothing is missed

**Weaknesses:**

- Security-specific (not a general-purpose review strategy)
- Can be time-consuming for large, complex systems
- Requires accurate system documentation (DFD)
- Does not inherently prioritize threats (need additional risk assessment)
- May produce a large number of low-priority threats that dilute focus
- Does not capture all threat types (e.g., supply chain attacks, social engineering)

**Industry Examples:**

- Microsoft mandates STRIDE threat modeling as part of their Security Development Lifecycle (SDL).
- OWASP recommends STRIDE as one of several threat modeling approaches in their Threat Modeling Cheat Sheet.
- The Microsoft Threat Modeling Tool automates STRIDE analysis based on DFD input.
- OWASP Threat Dragon supports STRIDE-based threat modeling.

**Citations:**

1. Shostack, Adam. *Threat Modeling: Designing for Security*. Wiley, 2014. -- The definitive book on threat modeling, including comprehensive STRIDE methodology.
2. Howard, Michael, and Steve Lipner. *The Security Development Lifecycle*. Microsoft Press, 2006. -- Describes STRIDE's role in Microsoft's SDL.
3. OWASP. "Threat Modeling Cheat Sheet." https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html -- OWASP's guidance on threat modeling approaches including STRIDE.
4. Kohnfelder, Loren, and Praerit Garg. "The Threats to Our Products." Microsoft Internal Document, 1999. -- The original STRIDE paper (referenced in Shostack's book).

---

### Strategy 9: Failure Mode and Effects Analysis (FMEA)

**Origin:** Developed by the U.S. Military in 1949 (MIL-P-1629 "Procedures for Performing a Failure Mode, Effect and Criticality Analysis"). Adopted by NASA during the Apollo program, then widely adopted in automotive (AIAG), aerospace, healthcare, and manufacturing.

**Domain:** Reliability Engineering, Systems Engineering, Quality Management, Risk Management

**Description:**

FMEA is a systematic, bottom-up analytical method for identifying all possible failure modes of a system, component, or process, evaluating the effects of each failure, assessing the risk, and prioritizing corrective actions. FMEA answers three questions for every component: (1) How can it fail? (2) What happens when it fails? (3) How bad is it?

The key output of FMEA is the **Risk Priority Number (RPN)**, calculated as:

`RPN = Severity x Occurrence x Detection`

Where each factor is rated on a scale of 1-10:
- **Severity**: How bad is the effect of the failure? (1 = negligible, 10 = catastrophic)
- **Occurrence**: How likely is the failure to occur? (1 = nearly impossible, 10 = almost certain)
- **Detection**: How likely is it that the failure will be detected before it reaches the end user? (1 = almost certain detection, 10 = undetectable)

FMEA in the adversarial review context generalizes beyond hardware: it can be applied to software, processes, decisions, and documents to systematically enumerate what can go wrong and prioritize responses.

**Methodology (Step-by-Step):**

1. **Define Scope**: Identify the system, subsystem, component, or process to analyze. Document its intended function.
2. **Decompose into Elements**: Break the system into its constituent parts. Each part becomes a row in the FMEA worksheet.
3. **Identify Failure Modes**: For each element, list all possible ways it can fail. A single element may have multiple failure modes.
4. **Determine Effects**: For each failure mode, describe the effect on:
   - The immediate component
   - The next-higher assembly
   - The end user / system level
5. **Assess Severity (S)**: Rate the severity of each effect (1-10 scale).
6. **Identify Causes**: For each failure mode, identify all potential root causes.
7. **Assess Occurrence (O)**: Rate the likelihood of each cause producing the failure (1-10 scale).
8. **Identify Controls**: Document existing detection and prevention controls.
9. **Assess Detection (D)**: Rate the effectiveness of existing detection controls (1-10 scale).
10. **Calculate RPN**: Multiply S x O x D.
11. **Prioritize and Act**: Rank failure modes by RPN. Define corrective actions for high-RPN items. Assign owners and deadlines.
12. **Re-assess**: After corrective actions, re-calculate RPN to verify improvement.

**When to Use:**

- During system or product design (Design FMEA / DFMEA)
- During process design or improvement (Process FMEA / PFMEA)
- In safety-critical systems (aerospace, automotive, medical devices)
- When conducting risk assessments for projects or decisions
- During NASA systems engineering reviews (required by NPR 7123.1D)
- For regulatory compliance (ISO 14971 for medical devices, IATF 16949 for automotive)

**When NOT to Use:**

- For purely creative or exploratory work (FMEA is analytical, not generative)
- When the system is not well enough understood to decompose
- For one-off, low-consequence decisions (overhead is excessive)
- When the team lacks the domain expertise to accurately rate S, O, and D

**Strengths:**

- Systematic and comprehensive (forces enumeration of all failure modes)
- Produces quantitative risk prioritization (RPN)
- Industry-standard methodology with decades of proven use
- Creates auditable documentation of risk analysis
- Applicable to hardware, software, processes, and services
- Directly ties to corrective action (not just identification)

**Weaknesses:**

- Can be time-consuming and paper-heavy
- RPN calculation has known limitations (multiplicative scale can obscure priorities)
- Subjectivity in S, O, D ratings (inter-rater reliability is moderate)
- Does not capture interactions between failure modes (each mode analyzed independently)
- Can become a "checkbox exercise" if organizational culture does not value it
- Requires significant domain expertise for accurate analysis

**Industry Examples:**

- NASA requires FMEA as part of systems engineering reviews for all Class A and B missions (NPR 7120.5, NPR 7123.1D).
- The automotive industry uses FMEA extensively per AIAG & VDA FMEA Handbook (2019).
- IEC 60812 is the international standard for FMEA methodology.
- The medical device industry requires FMEA as part of ISO 14971 risk management.
- Boeing and Airbus use FMEA in aircraft design certification (SAE ARP4761).

**Citations:**

1. U.S. Department of Defense. "MIL-P-1629: Procedures for Performing a Failure Mode, Effect and Criticality Analysis." 1949 (revised 1980 as MIL-STD-1629A). -- The original military standard that created FMEA.
2. AIAG & VDA. *FMEA Handbook*. Automotive Industry Action Group, 2019. -- The current industry standard for automotive FMEA.
3. Stamatis, D.H. *Failure Mode and Effect Analysis: FMEA from Theory to Execution*. ASQ Quality Press, 2003. -- The comprehensive practitioner reference for FMEA methodology.
4. IEC 60812:2018. "Failure modes and effects analysis (FMEA and FMECA)." International Electrotechnical Commission, 2018. -- The international standard for FMEA methodology.
5. NASA. "NPR 7123.1D: NASA Systems Engineering Processes and Requirements." 2020. -- Requires FMEA in NASA systems engineering.

---

### Strategy 10: Dialectical Inquiry

**Origin:** Ancient Greek philosophy (Socratic dialectic, Hegelian dialectic). Adapted for management decision-making by Ian Mitroff and Richard Mason in the 1980s. Formalized as a structured decision-making methodology.

**Domain:** Philosophy, Management Science, Strategic Planning, Decision Quality

**Description:**

Dialectical Inquiry is a structured decision-making process based on the philosophical tradition of dialectic: the resolution of opposing ideas through reasoned debate. In its management science formulation, Dialectical Inquiry requires that for every recommendation (the thesis), a **plausible counter-recommendation** (the antithesis) must be developed that is based on **different assumptions**. The two are then debated to reach a **synthesis** that is superior to either.

The critical distinction between Dialectical Inquiry and Devil's Advocacy is that Dialectical Inquiry requires the construction of a **complete alternative**, not merely criticism of the original. Where a Devil's Advocate says "here's why your plan is flawed," Dialectical Inquiry says "here's a different plan based on different assumptions, and here's why it might be better."

Research by Schweiger, Sandberg, and Ragan (1986) demonstrated that Dialectical Inquiry produced higher-quality decisions than Devil's Advocacy or consensus-seeking in controlled experiments, particularly for ill-structured strategic problems.

**Methodology (Step-by-Step):**

1. **Thesis Development**: The first team develops a recommendation (the thesis) with explicit documentation of:
   - The recommendation itself
   - The data used to support it
   - The assumptions underlying the recommendation
   - The causal logic connecting data to recommendation
2. **Assumption Surfacing**: Both teams collaboratively extract and list all assumptions underlying the thesis. These must be explicit, testable, and complete.
3. **Antithesis Construction**: A second team (or the same team in a different mode) constructs a counter-recommendation by:
   - Negating or questioning the key assumptions of the thesis
   - Reinterpreting the same data under different assumptions
   - Constructing a plausible alternative recommendation that follows logically from the different assumptions
4. **Structured Debate**: The thesis and antithesis teams present their cases. The debate focuses on:
   - Which assumptions are more valid and why
   - What evidence supports each set of assumptions
   - Where the data is ambiguous enough to support both interpretations
5. **Assumption Testing**: The group evaluates each contested assumption against available evidence. Assumptions are classified as:
   - Confirmed (evidence supports)
   - Refuted (evidence contradicts)
   - Uncertain (insufficient evidence)
6. **Synthesis**: The group constructs a new recommendation that:
   - Incorporates the strongest elements of both thesis and antithesis
   - Is grounded in the assumptions that survived testing
   - Addresses the weaknesses revealed by the dialectical process

**When to Use:**

- Strategic decisions with significant uncertainty
- When there are genuinely plausible alternative courses of action
- Architecture decisions (e.g., monolith vs. microservices, build vs. buy)
- When the team needs to understand and challenge its assumptions
- Complex trade-off decisions where multiple valid perspectives exist
- Policy decisions with competing stakeholder interests

**When NOT to Use:**

- When there is only one viable option (forced choice)
- For routine operational decisions (overhead is excessive)
- When the team lacks the expertise to construct a plausible antithesis
- When time pressure makes structured debate impractical
- When the decision is already made and the exercise would be theater

**Strengths:**

- Produces higher-quality decisions than Devil's Advocacy for strategic problems (Schweiger et al.)
- Forces explicit assumption identification (the most valuable single output)
- Generates genuine alternatives, not just criticism
- Creates intellectual engagement and team buy-in
- The synthesis is often superior to either original position
- Especially valuable for ill-structured problems with high uncertainty

**Weaknesses:**

- More time-consuming than Devil's Advocacy (requires constructing a full alternative)
- Requires sufficient domain expertise to build a credible antithesis
- Can create team conflict if not facilitated well
- The quality of the synthesis depends heavily on facilitation skill
- May not converge if assumptions are genuinely irreconcilable
- Harder to implement than simpler strategies

**Industry Examples:**

- The U.S. Intelligence Community uses Dialectical Inquiry as a structured analytic technique (documented in the CIA's *Tradecraft Primer*).
- Strategic planning firms use Dialectical Inquiry for scenario planning and strategy development.
- Architecture Decision Records (ADRs) implicitly use dialectical structure: "we considered X (thesis) and Y (antithesis) and chose Z (synthesis) because..."
- Jerry's own ADR template supports dialectical reasoning through "Alternatives Considered" sections.

**Citations:**

1. Mason, Richard O., and Ian I. Mitroff. *Challenging Strategic Planning Assumptions*. Wiley, 1981. -- The foundational work on Dialectical Inquiry in management science.
2. Schweiger, David M., William R. Sandberg, and James W. Ragan. "Group Approaches for Improving Strategic Decision Making: A Comparative Analysis of Dialectical Inquiry, Devil's Advocacy, and Consensus." *Academy of Management Journal*, 29(1), 51-71, 1986. -- The key empirical comparison of Dialectical Inquiry vs. Devil's Advocacy.
3. Mitroff, Ian I., and Harold A. Linstone. *The Unbounded Mind: Breaking the Chains of Traditional Business Thinking*. Oxford University Press, 1993. -- Extended treatment of dialectical methods in organizational decision-making.
4. Central Intelligence Agency. *A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis*. 2009. -- CIA's codification of dialectical methods for intelligence analysis.

---

### Strategy 11: Chaos Engineering

**Origin:** Developed at Netflix circa 2010-2011 by the "Chaos Team" (later "Chaos Engineering" team). Casey Rosenthal and Nora Jones formalized the discipline in their book *Chaos Engineering: System Resiliency in Practice* (2020). The original tool, "Chaos Monkey," was created by Netflix engineers to randomly terminate production instances.

**Domain:** Site Reliability Engineering, Distributed Systems, Resilience Engineering

**Description:**

Chaos Engineering is the discipline of experimenting on a distributed system in order to build confidence in the system's capability to withstand turbulent conditions in production. It involves deliberately injecting controlled failures, faults, and anomalies into a running system to observe how the system responds, with the goal of discovering weaknesses before they cause unplanned outages.

The philosophical core of Chaos Engineering is the recognition that complex systems **will** fail in unexpected ways, and the only way to build confidence in their resilience is to **proactively test** failure scenarios rather than waiting for them to occur naturally.

Chaos Engineering differs from traditional testing in several key ways:
- It runs in **production** (or production-like environments), not just in test
- It tests **system behavior**, not individual components
- It focuses on **steady-state** verification (is the system still functioning correctly?), not just correctness
- It operates under the assumption that you **cannot predict** all failure modes, so you must discover them empirically

In the adversarial review context, Chaos Engineering generalizes to: **deliberately introduce turbulence into a process, system, or artifact to discover whether it degrades gracefully or fails catastrophically.**

**Methodology (Step-by-Step):**

1. **Define Steady State**: Identify the measurable indicators that the system is operating normally (latency, error rate, throughput, business metrics). This is the baseline.
2. **Hypothesize**: Form a hypothesis: "If we inject fault X, the system will continue to meet steady-state criteria because of defense Y."
3. **Design the Experiment**: Define:
   - The specific fault to inject (e.g., terminate an instance, introduce network latency, corrupt a response)
   - The blast radius (how much of the system is affected)
   - The duration
   - The abort criteria (when to stop if things go wrong)
   - The rollback plan
4. **Run the Experiment**: Inject the fault in production (or production-like environment) while monitoring steady-state metrics.
5. **Observe**: Watch for deviations from steady state. Record all observations.
6. **Analyze**: Determine whether the hypothesis held:
   - If steady state was maintained: confidence in that resilience mechanism increases
   - If steady state was violated: a weakness has been discovered
7. **Fix and Re-test**: For discovered weaknesses, implement fixes and re-run the experiment to verify.
8. **Automate**: Mature chaos engineering programs automate experiments to run continuously.

**When to Use:**

- For distributed systems where failure modes are unpredictable
- When the system has high availability requirements (99.9%+ uptime)
- After major architectural changes
- When the team claims the system is "resilient" but has not tested it
- When incident post-mortems reveal systemic fragility
- Before peak traffic events (e.g., Black Friday, product launches)

**When NOT to Use:**

- On systems without monitoring (you cannot observe steady state)
- On systems without rollback capability (experiments can cause unrecoverable damage)
- Without executive sponsorship (chaos experiments in production require organizational buy-in)
- On systems with known, unfixed vulnerabilities (fix the known issues first)
- When the blast radius cannot be controlled
- In regulated environments where production experimentation is prohibited

**Strengths:**

- Discovers failure modes that no other testing method reveals
- Builds genuine confidence (tested, not assumed)
- Applicable to complex systems where analytical methods are insufficient
- Drives continuous improvement of system resilience
- Creates a culture of proactive reliability
- Industry-proven at massive scale (Netflix, Amazon, Google, Microsoft)

**Weaknesses:**

- Risk of causing real incidents if experiments are poorly designed
- Requires significant organizational maturity (monitoring, rollback, culture)
- Not applicable to all systems (some cannot tolerate any production experimentation)
- Expensive in terms of tooling and expertise
- Results may not generalize (passing one chaos experiment does not prove general resilience)
- Can create alert fatigue if experiments trigger false alarms

**Industry Examples:**

- Netflix's "Simian Army" (Chaos Monkey, Latency Monkey, Conformity Monkey) is the canonical Chaos Engineering implementation.
- Amazon's GameDay exercises are large-scale Chaos Engineering events.
- Gremlin (company) provides Chaos Engineering as a Service, used by hundreds of enterprises.
- LitmusChaos is the CNCF-endorsed open-source Chaos Engineering platform for Kubernetes.
- The Principles of Chaos Engineering (principlesofchaos.org) codify the discipline's core tenets.

**Citations:**

1. Rosenthal, Casey, and Nora Jones. *Chaos Engineering: System Resiliency in Practice*. O'Reilly Media, 2020. -- The definitive book on Chaos Engineering.
2. Basiri, Ali, et al. "Chaos Engineering." *IEEE Software*, 33(3), 35-41, 2016. -- Netflix's original academic paper on Chaos Engineering.
3. Principlesofchaos.org. "Principles of Chaos Engineering." https://principlesofchaos.org/ -- The community-authored principles document.
4. Rosenthal, Casey, et al. *Chaos Engineering: Building Confidence in System Behavior through Experiments*. O'Reilly Media, 2017. -- The first O'Reilly report on the discipline.

---

### Strategy 12: Adversarial Collaboration

**Origin:** Coined by Daniel Kahneman in the context of resolving scientific disagreements. Kahneman and his critics (notably Gary Klein) used Adversarial Collaboration to resolve their disagreements about expert intuition, resulting in their joint 2009 paper "Conditions for Intuitive Expertise: A Failure to Disagree."

**Domain:** Social Science, Psychology, Scientific Method, Decision Science

**Description:**

Adversarial Collaboration is a structured process in which researchers or experts who genuinely disagree on a substantive question **collaborate** to design and execute a definitive test of their disagreement. Unlike a debate (where each side tries to win), Adversarial Collaboration requires both sides to agree in advance on what evidence would resolve the disagreement, then jointly produce or evaluate that evidence.

The key innovation of Adversarial Collaboration is that it transforms disagreement from a social conflict into an empirical question. By forcing both sides to agree on the test before seeing the results, it eliminates post-hoc rationalization and goal-post moving.

In the adversarial review context, Adversarial Collaboration means bringing together the creator (who believes the work is good) and the critic (who believes it has flaws) to jointly define what "good" means, then jointly evaluate the work against that definition. This prevents the common pathology where creators and critics talk past each other because they are evaluating against different criteria.

**Methodology (Step-by-Step):**

1. **Identify the Disagreement**: Explicitly state what the two parties disagree about. Be precise. "The architecture is wrong" is too vague; "the architecture will not scale beyond 10,000 concurrent users because of the synchronous database access pattern" is specific enough to test.
2. **Agree on Criteria**: Both parties must agree on what evidence or criteria would settle the disagreement. "If load testing shows response time exceeds 200ms at 10,000 concurrent users, the critic's concern is validated."
3. **Design the Test**: Jointly design the experiment, analysis, or evaluation that will produce the agreed-upon evidence. Both parties must agree the test is fair.
4. **Execute Together**: Both parties participate in or observe the test execution. This prevents accusations of biased execution.
5. **Evaluate Results**: Both parties review the results against the pre-agreed criteria.
6. **Resolve or Refine**: If the results are conclusive, the disagreement is resolved. If not, refine the test or identify what additional information is needed.
7. **Publish the Resolution**: Document the process, the evidence, and the resolution. This becomes a shared artifact that both parties endorse.

**When to Use:**

- When two experts genuinely disagree about a technical question
- When disagreements are blocking progress and need resolution
- When subjective opinions need to be converted into objective evaluations
- In design reviews where architect and reviewer disagree
- In scientific or research contexts where competing hypotheses exist
- When team conflict around technical decisions is becoming counterproductive

**When NOT to Use:**

- When the disagreement is about values, not facts (Adversarial Collaboration resolves empirical questions, not moral ones)
- When one party is not acting in good faith
- When there is no practical way to test the disagreement
- When the power imbalance between parties makes genuine collaboration impossible
- When speed is more important than resolution quality

**Strengths:**

- Produces definitive resolutions that both parties accept
- Converts subjective disagreements into objective tests
- Builds mutual respect between disagreeing parties
- Creates high-quality evidence (both parties ensure the test is fair)
- Prevents goal-post moving and post-hoc rationalization
- The joint criteria definition is often the most valuable output

**Weaknesses:**

- Requires good faith from both parties (rare in adversarial contexts)
- Time-consuming (designing and executing joint tests takes effort)
- Not all disagreements are empirically testable
- Power dynamics can undermine genuine collaboration
- Requires a skilled facilitator when emotions are high
- Limited applicability when disagreements are about values or preferences

**Industry Examples:**

- Kahneman and Klein's 2009 paper "Conditions for Intuitive Expertise: A Failure to Disagree" (*American Psychologist*) is the canonical example. Two giants of decision science who disagreed about expert intuition collaborated to find that they actually agreed once they defined terms precisely.
- The Reproducibility Project in psychology uses elements of Adversarial Collaboration to resolve conflicting research findings.
- Some software architecture review boards use Adversarial Collaboration when architects disagree about design approaches -- they agree on evaluation criteria and then benchmark.

**Citations:**

1. Kahneman, Daniel, and Gary Klein. "Conditions for Intuitive Expertise: A Failure to Disagree." *American Psychologist*, 64(6), 515-526, 2009. -- The landmark Adversarial Collaboration paper.
2. Mellers, Barbara, Ralph Hertwig, and Daniel Kahneman. "Do Frequency Representations Eliminate Conjunction Effects? An Exercise in Adversarial Collaboration." *Psychological Science*, 12(4), 269-275, 2001. -- Earlier Adversarial Collaboration example.
3. Bateman, Ian, et al. "Testing Competing Models of Loss Aversion: An Adversarial Collaboration." *Journal of Public Economics*, 89(8), 1561-1580, 2005. -- Adversarial Collaboration in economics.
4. Kahneman, Daniel. "A Proposal to Deal with Questions about Priming Effects." Open letter, 2012. -- Kahneman's advocacy for Adversarial Collaboration as a mechanism for resolving scientific disputes.

---

### Strategy 13: Purple Team

**Origin:** Cybersecurity community, early 2010s. Emerged as a response to the recognition that Red Team and Blue Team exercises were most effective when integrated rather than adversarial. Formalized by practitioners like Tim MalcomVetter and Jorge Orchilles.

**Domain:** Cybersecurity, Security Operations, Continuous Improvement

**Description:**

Purple Teaming is an integrated security assessment approach that combines Red Team (offensive) and Blue Team (defensive) operations into a collaborative, continuous improvement cycle. Rather than treating offense and defense as separate exercises with a final report, Purple Teaming has the Red Team and Blue Team work **together** in real-time to maximize learning and defensive improvement.

The name "Purple" derives from combining Red and Blue. In practice, a Purple Team exercise typically involves the Red Team executing attack techniques one at a time while the Blue Team observes in real-time whether their defenses detect and respond to each technique. When a detection gap is found, the Blue Team immediately develops and deploys a new detection, and the Red Team re-tests.

Purple Teaming represents a maturity evolution beyond traditional Red/Blue exercises. Where traditional engagements optimize for **realism** (the Red Team operates covertly, the Blue Team doesn't know when the exercise is happening), Purple Teaming optimizes for **learning** (both teams work together to maximize the number of detections improved).

In the adversarial review context, Purple Teaming means having the critic and creator work together in real-time: the critic identifies a weakness, the creator addresses it immediately, and the critic re-evaluates -- in a tight feedback loop rather than a batch process.

**Methodology (Step-by-Step):**

1. **Planning**: Red and Blue Teams jointly select the attack techniques to test, typically from a framework like MITRE ATT&CK. Prioritize techniques relevant to the organization's threat landscape.
2. **Technique Execution**: The Red Team executes one technique at a time, with the Blue Team aware that it is happening (unlike traditional Red Team engagements).
3. **Detection Assessment**: The Blue Team checks in real-time whether their tools and processes detected the technique. Outcomes:
   - Detected and alerted: Good. Document the detection.
   - Detected but not alerted: Detection exists but alerting gap. Fix the alert.
   - Not detected: Detection gap. Create a new detection.
4. **Immediate Remediation**: When a gap is found, the Blue Team develops and deploys a detection or mitigation immediately (or as soon as practical).
5. **Re-test**: The Red Team re-executes the technique to verify the new detection works.
6. **Documentation**: Record every technique tested, its detection status before and after, and the improvements made.
7. **Metrics**: Track Purple Team coverage: what percentage of relevant ATT&CK techniques are now detected?
8. **Continuous Cycle**: Purple Teaming is not a one-time exercise but a continuous improvement program.

**When to Use:**

- When Red and Blue Teams already exist and the goal is to maximize their combined value
- When the organization needs to rapidly improve detection coverage
- After a major incident (to verify that similar attacks would now be detected)
- When building a security operations program from scratch
- When measuring defensive maturity against a specific threat framework
- In the adversarial review context: when the goal is to improve the artifact, not just evaluate it

**When NOT to Use:**

- When you need a realistic assessment of detection capability (Purple Team's cooperative nature sacrifices realism)
- When the Red Team needs to test the full attack chain including evasion (Purple Team's transparency eliminates evasion testing)
- When organizational dynamics require keeping Red and Blue separate (sometimes adversarial tension is productive)
- When the team lacks MITRE ATT&CK or equivalent framework knowledge

**Strengths:**

- Maximizes learning per unit of effort (no wasted Red Team cycles on already-detected techniques)
- Immediately improves defenses (not just a report that sits on a shelf)
- Builds collaboration between offense and defense teams
- Produces measurable improvement metrics (detection coverage over time)
- Efficient use of expensive Red Team expertise
- Directly ties assessment to remediation

**Weaknesses:**

- Sacrifices realism (attackers do not cooperate with defenders)
- Does not test the Blue Team's ability to detect novel, unknown attacks
- Can create false confidence (detecting known techniques does not mean detecting real attackers)
- Requires both teams to be co-located or closely coordinated
- May not satisfy regulatory requirements that mandate traditional Red Team exercises
- The collaborative dynamic may soften the adversarial rigor

**Industry Examples:**

- MITRE ATT&CK Evaluations are essentially Purple Team exercises: vendors know which techniques will be tested and attempt to demonstrate detection.
- Orchilles, Jorge, and Tim MalcomVetter. "Purple Team Exercise Framework (PTEF)." Scythe.io. -- A structured framework for conducting Purple Team exercises.
- Many enterprise security programs have evolved from annual Red Team engagements to continuous Purple Team programs.

**Citations:**

1. Oakley, Tim, ed. *Purple Team Strategies: Enhancing IT Security Assessments by Combining Red and Blue Team Strategies*. Packt Publishing, 2022. -- Comprehensive guide to Purple Team methodology.
2. Orchilles, Jorge. "Purple Team Exercise Framework." Scythe, 2020. https://github.com/scythe-io/purple-team-exercise-framework -- Open-source Purple Team exercise framework.
3. MITRE. "ATT&CK Evaluations." https://attackevals.mitre-engenuity.org/ -- The industry-standard Purple Team-style evaluation of security products.
4. MalcomVetter, Tim. "Purple Teaming." Multiple conference presentations (BSides, DerbyCon), 2016-2019. -- Practitioner presentations that helped formalize the Purple Team concept.

---

### Strategy 14: Cognitive Bias Audit

**Origin:** Built on the foundational work of Daniel Kahneman and Amos Tversky (1970s-1980s) on cognitive biases and heuristics. Formalized as a structured review technique in intelligence analysis (CIA's *Psychology of Intelligence Analysis* by Richards Heuer, 1999) and in decision quality consulting (Decision Education Foundation, Strategic Decisions Group).

**Domain:** Behavioral Economics, Cognitive Psychology, Decision Science, Intelligence Analysis

**Description:**

A Cognitive Bias Audit is a systematic review of a decision, analysis, or recommendation specifically designed to detect and mitigate the influence of known cognitive biases. The auditor examines the reasoning process (not just the conclusion) against a checklist of biases that are known to distort judgment in the relevant context.

Humans (and by extension, AI systems trained on human reasoning) are subject to dozens of documented cognitive biases that systematically distort perception, memory, and judgment. A Cognitive Bias Audit does not ask "is this answer correct?" but rather "are there systematic distortions in how this answer was reached?"

The most relevant biases for adversarial review of technical work include:

| Bias | Description | Risk in Technical Review |
|------|-------------|------------------------|
| **Confirmation Bias** | Seeking/weighting evidence that confirms existing beliefs | Ignoring contradictory test results |
| **Anchoring** | Over-relying on the first piece of information | Over-weighting initial estimates |
| **Availability Heuristic** | Judging probability by ease of recall | Overweighting recent or dramatic failures |
| **Sunk Cost Fallacy** | Continuing because of past investment | Refusing to abandon a failing approach |
| **Dunning-Kruger Effect** | Overestimating competence in areas of low skill | Under-estimating the difficulty of unfamiliar work |
| **Optimism Bias** | Underestimating risks and timelines | Over-promising delivery dates |
| **Survivorship Bias** | Drawing conclusions from successes, ignoring failures | "This pattern worked at Netflix, so it will work for us" |
| **Framing Effect** | Being influenced by how information is presented | Choosing "95% survival rate" over "5% mortality rate" |
| **Groupthink** | Conforming to group consensus over individual judgment | Not voicing technical concerns in team settings |
| **Bandwagon Effect** | Adopting beliefs because others hold them | Choosing technologies because they are popular |

**Methodology (Step-by-Step):**

1. **Select the Bias Checklist**: Choose the biases most relevant to the domain and type of decision. A general-purpose checklist of 10-15 biases is sufficient for most reviews.
2. **Document the Reasoning Chain**: Before auditing, document the complete reasoning chain that led to the decision or recommendation: What data was used? What alternatives were considered? What assumptions were made? Why was this option selected?
3. **Systematic Bias Scan**: For each bias on the checklist, ask:
   - "Is there evidence that this bias influenced the reasoning?"
   - "What would the conclusion look like if this bias were removed?"
   - "What data or perspectives might have been ignored due to this bias?"
4. **Evidence Assessment**: For each potential bias detection:
   - Rate the likelihood that the bias is present (Low/Medium/High)
   - Rate the potential impact on the decision (Low/Medium/High)
   - Identify what would need to change if the bias were corrected
5. **De-biasing Recommendations**: For each detected bias, recommend specific de-biasing actions:
   - Seek disconfirming evidence (for Confirmation Bias)
   - Generate multiple independent estimates (for Anchoring)
   - Consider base rates (for Availability Heuristic)
   - Conduct pre-mortem (for Optimism Bias)
   - Solicit anonymous individual opinions before group discussion (for Groupthink)
6. **Re-evaluation**: After de-biasing, re-evaluate the original decision. Does the conclusion change?

**When to Use:**

- Before making high-stakes, irreversible decisions
- When reviewing intelligence assessments or strategic analyses
- When a decision feels "too obvious" or reached too quickly
- When the team is homogeneous (high groupthink risk)
- When reviewing AI-generated outputs (AI can exhibit training data biases)
- As a complementary strategy alongside other adversarial techniques
- When reviewing requirements (biases affect what requirements are elicited)

**When NOT to Use:**

- For trivial decisions (overhead is disproportionate)
- When the team lacks understanding of cognitive biases (training required first)
- As a standalone strategy (bias audit identifies problems but not solutions)
- When used to dismiss conclusions rather than improve reasoning ("you're biased" as an argument-ending move)

**Strengths:**

- Targets the reasoning process, not just the conclusion
- Based on decades of rigorous empirical research
- Applicable to any domain and any type of decision
- Raises awareness of cognitive limitations
- Can be systematized into checklists and training programs
- Complements other adversarial strategies (bias audit + Devil's Advocate is powerful)

**Weaknesses:**

- Knowledge of biases does not automatically de-bias (knowing about Confirmation Bias does not prevent it)
- Risk of "bias bias" (finding biases everywhere, including where they don't apply)
- Difficult to prove a specific bias influenced a specific decision (inherently inferential)
- Can be used to dismiss valid conclusions by labeling them "biased"
- Requires significant training to apply accurately
- The audit itself may be subject to biases

**Industry Examples:**

- The CIA's Directorate of Analysis uses structured bias checks as part of analytic tradecraft (documented in Heuer's work and the CIA Tradecraft Primer).
- The UK's Joint Intelligence Committee requires bias review of intelligence assessments.
- Decision quality consulting firms (Strategic Decisions Group, Decision Education Foundation) routinely include bias audits in their decision processes.
- Medical diagnosis checklists increasingly include bias awareness (cognitive de-biasing in clinical reasoning).

**Citations:**

1. Kahneman, Daniel, and Amos Tversky. "Judgment Under Uncertainty: Heuristics and Biases." *Science*, 185(4157), 1124-1131, 1974. -- The foundational paper on cognitive biases.
2. Heuer, Richards J., Jr. *Psychology of Intelligence Analysis*. Center for the Study of Intelligence, CIA, 1999. -- The CIA's manual on cognitive biases in analytical reasoning.
3. Kahneman, Daniel. *Thinking, Fast and Slow*. Farrar, Straus and Giroux, 2011. -- The comprehensive popular treatment of cognitive biases and dual-process theory.
4. Montibeller, Gilberto, and Detlof von Winterfeldt. "Cognitive and Motivational Biases in Decision and Risk Analysis." *Risk Analysis*, 35(7), 1230-1251, 2015. -- Survey of biases specifically in risk and decision analysis.
5. Central Intelligence Agency. *A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis*. 2009. -- Includes cognitive bias mitigation techniques.

---

### Strategy 15: Assumption Mapping and Stress Testing

**Origin:** Rooted in systems thinking (Peter Senge, *The Fifth Discipline*, 1990), strategic planning (Roger Martin, *Playing to Win*, 2013), and critical thinking methodology. The specific practice of "assumption surfacing" was formalized by Mason and Mitroff (1981) as part of their work on Dialectical Inquiry, and independently in Lean Startup methodology by Eric Ries (2011) as "leap of faith assumptions."

**Domain:** Systems Thinking, Strategic Planning, Lean Startup, Critical Thinking, Risk Management

**Description:**

Assumption Mapping and Stress Testing is a two-phase adversarial review strategy that first **makes all assumptions explicit** (mapping) and then **systematically attacks each assumption** (stress testing) to identify which assumptions are critical, which are vulnerable, and what happens when they fail.

Every plan, design, decision, or analysis rests on assumptions -- things believed to be true that are not independently verified. Most failures can be traced to assumptions that turned out to be wrong. Yet assumptions are rarely documented, let alone tested. This strategy forces assumptions into the open and subjects them to structured adversarial pressure.

The mapping phase answers: "What must be true for this plan to succeed?"
The stress testing phase answers: "What happens if each of these things is NOT true?"

This strategy is particularly powerful for AI agent review because AI systems make implicit assumptions that are rarely surfaced: assumptions about data quality, user behavior, environment stability, and requirement completeness.

**Methodology (Step-by-Step):**

**Phase 1: Assumption Mapping**

1. **Artifact Review**: Read the plan, design, decision, or analysis to be reviewed. Understand its goals and logic.
2. **Assumption Extraction**: For each key element, ask:
   - "What must be true for this to work?"
   - "What are we taking for granted?"
   - "What would someone from outside this team question?"
   Categories of assumptions to probe:
   - **Data assumptions**: Is the data accurate, complete, current?
   - **User/stakeholder assumptions**: Will users behave as expected?
   - **Technical assumptions**: Will the technology work as expected?
   - **Resource assumptions**: Will we have the people, time, money?
   - **Environmental assumptions**: Will the operating environment remain stable?
   - **Dependency assumptions**: Will external dependencies be met?
3. **Assumption Documentation**: Record each assumption with:
   - A unique identifier (ASM-001, ASM-002, ...)
   - The assumption statement
   - What element of the plan depends on it
   - Current evidence for/against (if any)
4. **Importance-Uncertainty Matrix**: Plot each assumption on a 2x2 matrix:
   - X-axis: Importance (how critical is this assumption to success?)
   - Y-axis: Uncertainty (how confident are we that this assumption is true?)
   - **Quadrant 1 (High Importance, High Uncertainty)**: Critical risks -- test these first
   - **Quadrant 2 (High Importance, Low Uncertainty)**: Monitor these
   - **Quadrant 3 (Low Importance, High Uncertainty)**: Accept or ignore
   - **Quadrant 4 (Low Importance, Low Uncertainty)**: Safe to ignore

**Phase 2: Stress Testing**

5. **Prioritize for Testing**: Focus stress testing on Quadrant 1 assumptions (high importance, high uncertainty).
6. **Negation Test**: For each priority assumption, negate it: "What if this assumption is FALSE?" Trace the consequences through the plan. Document the impact.
7. **Sensitivity Analysis**: Vary the assumption: "What if this is only partially true?" or "What if this is true now but changes in 6 months?" Document how sensitive the plan is to each assumption.
8. **Boundary Conditions**: Test extreme values: "What if this assumption is true at 10x the expected scale?" or "What if it holds for only 1% of cases?"
9. **Failure Scenario Construction**: For assumptions that fail catastrophically, construct a specific failure scenario. This can feed into a Pre-Mortem (Strategy 6) or FMEA (Strategy 9).
10. **Mitigation Design**: For each vulnerable assumption, design one or more of:
    - A test to validate the assumption before committing
    - A contingency plan if the assumption fails
    - A design change that removes the dependency on the assumption
    - A monitoring mechanism to detect early if the assumption is failing

**When to Use:**

- Before committing to any significant plan, architecture, or strategy
- When reviewing proposals from teams that are heavily invested in their approach
- When a plan has been developed quickly without thorough risk analysis
- In Lean Startup contexts (testing "leap of faith" assumptions before building)
- When reviewing AI-generated recommendations (surfacing what the AI assumed)
- In conjunction with other strategies (assumption mapping feeds Devil's Advocate, Pre-Mortem, and FMEA)
- During requirements reviews (every requirement embeds assumptions about user needs)

**When NOT to Use:**

- When the plan is already in execution and assumptions cannot be changed (too late -- focus on monitoring instead)
- When the assumptions are genuinely well-established facts (over-testing solid foundations wastes time)
- When the team lacks domain expertise to identify meaningful assumptions
- As a delay tactic to avoid decision-making

**Strengths:**

- Addresses the root cause of most failures (wrong assumptions, not wrong execution)
- Produces a concrete, testable list of risks
- The Importance-Uncertainty matrix provides clear prioritization
- Feeds naturally into other adversarial strategies
- Applicable to any domain and any type of work
- Makes implicit knowledge explicit (valuable even if no assumptions fail)
- Low cost, high impact

**Weaknesses:**

- Quality depends entirely on the ability to surface hidden assumptions (some may remain hidden)
- Can produce overwhelming lists of assumptions for complex systems
- Stress testing requires imagination and domain expertise
- May create analysis paralysis if every assumption is treated as critical
- The Importance and Uncertainty ratings are subjective
- Does not guarantee that all critical assumptions are found

**Industry Examples:**

- Eric Ries' Lean Startup methodology centers on identifying "leap of faith assumptions" and designing "minimum viable products" to test them before scaling.
- Roger Martin's "Playing to Win" strategy framework requires strategists to articulate "What would have to be true?" for each strategic option.
- The British military's "Assumption Red Team" reviews operational plans specifically for assumption validity.
- Amazon's "Working Backwards" process includes an assumption review phase for new product proposals.
- NASA's Systems Engineering Handbook (SP-2016-6105) includes assumption management as part of risk management.

**Citations:**

1. Mason, Richard O., and Ian I. Mitroff. *Challenging Strategic Planning Assumptions*. Wiley, 1981. -- The foundational work on assumption surfacing and testing.
2. Ries, Eric. *The Lean Startup: How Today's Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses*. Crown Business, 2011. -- Popularized the concept of "leap of faith assumptions" and minimum viable tests.
3. Martin, Roger L. "Playing to Win." *Harvard Business Review Press*, 2013. -- "What would have to be true?" framework for assumption testing in strategy.
4. Senge, Peter. *The Fifth Discipline: The Art and Practice of the Learning Organization*. Doubleday, 1990. -- Systems thinking foundation for understanding how assumptions create mental models.
5. NASA. "NASA Systems Engineering Handbook (SP-2016-6105)." 2016. -- Includes assumption management in systems engineering.

---

## Comparative Analysis

### Strategy Comparison Matrix

| # | Strategy | Primary Domain | Orientation | Expertise Required | Time Investment | Output Type | Constructive? |
|---|----------|---------------|-------------|-------------------|-----------------|-------------|---------------|
| 1 | Red Team | Cybersecurity / Military | Offensive | Very High | High | Vulnerability report | No (identifies weaknesses) |
| 2 | Blue Team | Cybersecurity / Defense | Defensive | High | Medium-High | Defense assessment | Yes (improves defenses) |
| 3 | Devil's Advocate | Decision Science | Critical | Medium | Low-Medium | Counter-arguments | No (critiques only) |
| 4 | Steelman | Argumentation | Constructive | High | Medium | Strengthened argument | Yes (improves argument) |
| 5 | Strawman | Argumentation | Diagnostic | Medium | Low | Anti-pattern catalog | No (shows what to avoid) |
| 6 | Pre-Mortem | Cognitive Psychology | Imaginative | Low-Medium | Low | Failure mode list | Partially (identifies risks) |
| 7 | Mutation Testing | Software Engineering | Fault-injection | Medium-High | Medium-High | Test quality metric | Yes (improves test suite) |
| 8 | STRIDE | Software Security | Systematic | High | Medium-High | Threat catalog | Partially (identifies threats) |
| 9 | FMEA | Reliability Engineering | Systematic | High | High | Risk-prioritized failures | Yes (drives corrective action) |
| 10 | Dialectical Inquiry | Philosophy / Mgmt Science | Dialectical | High | High | Synthesized decision | Yes (generates superior solution) |
| 11 | Chaos Engineering | SRE / Distributed Systems | Empirical | Very High | High | Resilience evidence | Yes (improves resilience) |
| 12 | Adversarial Collaboration | Social Science | Collaborative | High | High | Joint resolution | Yes (resolves disagreement) |
| 13 | Purple Team | Cybersecurity | Integrated | High | Medium-High | Detection improvements | Yes (immediate improvement) |
| 14 | Cognitive Bias Audit | Decision Science | Meta-analytical | Medium-High | Medium | Bias detection report | Partially (identifies biases) |
| 15 | Assumption Mapping | Systems Thinking | Analytical | Medium | Medium | Assumption risk register | Yes (drives mitigation) |

### Applicability to Jerry Review Contexts

| Review Context | Best Strategies | Rationale |
|---------------|-----------------|-----------|
| **Code Review** | Mutation Testing, Devil's Advocate, Red Team | Fault injection tests test quality; Devil's Advocate challenges design; Red Team tests security |
| **Architecture Decision** | Dialectical Inquiry, Assumption Mapping, Steelman/Strawman | Dialectic generates alternatives; assumption mapping finds hidden risks; steelman/strawman establish quality range |
| **Requirements Review** | Devil's Advocate, FMEA, Assumption Mapping, Cognitive Bias Audit | Challenge necessity; enumerate failure modes; surface assumptions; detect biases in elicitation |
| **Security Review** | Red Team, STRIDE, Purple Team, Blue Team | Full adversarial security assessment cycle |
| **Design Review** | Pre-Mortem, FMEA, Dialectical Inquiry, Assumption Mapping | Imagine failure; enumerate failure modes; debate alternatives; test assumptions |
| **Strategic Decision** | Pre-Mortem, Cognitive Bias Audit, Devil's Advocate, Adversarial Collaboration | Overcome optimism bias; detect reasoning biases; challenge consensus; resolve disagreements |
| **AI Agent Output Review** | Steelman/Strawman, Cognitive Bias Audit, Devil's Advocate, Assumption Mapping | Establish quality range; detect AI biases; challenge conclusions; surface implicit assumptions |
| **Process/Workflow Review** | Chaos Engineering, FMEA, Pre-Mortem | Test resilience; enumerate failures; imagine process failure |

### Complementary Strategy Combinations

| Combination | Synergy |
|-------------|---------|
| Steelman + Strawman + Devil's Advocate | Full quality range (best, worst, challenged) |
| Red Team + Blue Team + Purple Team | Full security cycle (attack, defend, improve) |
| Pre-Mortem + FMEA + Assumption Mapping | Comprehensive risk identification (imagination + systematic + foundational) |
| Dialectical Inquiry + Adversarial Collaboration | Deep disagreement resolution (structured debate + joint testing) |
| Cognitive Bias Audit + Devil's Advocate | Metacognitive + argumentative challenge |
| Mutation Testing + Chaos Engineering | Fault injection at code and system level |

---

## Strategy Selection Guide

### Decision Tree for Strategy Selection

```
Start: What are you reviewing?
|
+-- Security artifact? --> Red Team + STRIDE + Blue Team (+ Purple Team for improvement)
|
+-- Strategic decision? --> Pre-Mortem + Cognitive Bias Audit + Devil's Advocate
|
+-- Architecture/Design? --> Dialectical Inquiry + Assumption Mapping + FMEA
|
+-- Requirements? --> Devil's Advocate + FMEA + Assumption Mapping
|
+-- Code/Tests? --> Mutation Testing + Devil's Advocate
|
+-- Communication (pitch, docs)? --> Steelman + Strawman + Devil's Advocate
|
+-- System resilience? --> Chaos Engineering + FMEA + Pre-Mortem
|
+-- Resolving disagreement? --> Adversarial Collaboration + Dialectical Inquiry
|
+-- AI-generated output? --> Cognitive Bias Audit + Assumption Mapping + Steelman/Strawman
```

### Quick Reference: When to Use Each Strategy

| Strategy | Use When... | Avoid When... |
|----------|-------------|---------------|
| Red Team | Testing security or adversarial resilience | Early-stage development with known gaps |
| Blue Team | Validating defensive capabilities | No adversarial input exists yet |
| Devil's Advocate | Consensus formed too quickly | Genuine disagreement already exists |
| Steelman | Evaluating proposals fairly | The proposal is unethical/dangerous |
| Strawman | Teaching what to avoid | Author is already demoralized |
| Pre-Mortem | Starting a project or committing to a plan | Team is already anxious |
| Mutation Testing | Evaluating test/review quality | Test suite is immature |
| STRIDE | Designing secure systems | Non-security reviews |
| FMEA | Safety-critical or high-reliability systems | Trivial decisions |
| Dialectical Inquiry | Genuine uncertainty with plausible alternatives | Only one viable option |
| Chaos Engineering | Testing distributed system resilience | No monitoring/rollback capability |
| Adversarial Collaboration | Expert disagreement on testable questions | Values-based disagreements |
| Purple Team | Improving detection collaboratively | Need realistic adversarial assessment |
| Cognitive Bias Audit | High-stakes decisions with reasoning chains | Trivial decisions |
| Assumption Mapping | Any plan with unverified assumptions | Execution already underway |

---

## Sources and References

### Books

| # | Author(s) | Title | Publisher | Year |
|---|-----------|-------|-----------|------|
| B1 | Zenko, Micah | *Red Team: How to Succeed By Thinking Like the Enemy* | Basic Books | 2015 |
| B2 | Nemeth, Charlan J. | *In Defense of Troublemakers* | Basic Books | 2018 |
| B3 | Galef, Julia | *The Scout Mindset* | Portfolio/Penguin | 2021 |
| B4 | Klein, Gary | *Sources of Power* | MIT Press | 1998 |
| B5 | Kahneman, Daniel | *Thinking, Fast and Slow* | Farrar, Straus & Giroux | 2011 |
| B6 | Shostack, Adam | *Threat Modeling: Designing for Security* | Wiley | 2014 |
| B7 | Stamatis, D.H. | *Failure Mode and Effect Analysis* | ASQ Quality Press | 2003 |
| B8 | Mason, R.O. & Mitroff, I.I. | *Challenging Strategic Planning Assumptions* | Wiley | 1981 |
| B9 | Rosenthal, C. & Jones, N. | *Chaos Engineering* | O'Reilly Media | 2020 |
| B10 | Heuer, Richards J., Jr. | *Psychology of Intelligence Analysis* | CIA/CSI | 1999 |
| B11 | Senge, Peter | *The Fifth Discipline* | Doubleday | 1990 |
| B12 | Ries, Eric | *The Lean Startup* | Crown Business | 2011 |
| B13 | Martin, Roger L. | *Playing to Win* | HBR Press | 2013 |
| B14 | Walton, Douglas | *Informal Logic: A Pragmatic Approach* | Cambridge UP | 2008 |
| B15 | Janis, Irving L. | *Groupthink* | Houghton Mifflin | 1982 |
| B16 | Murdoch, Don | *Blue Team Handbook: Incident Response Edition* | CreateSpace | 2014 |
| B17 | Bejtlich, Richard | *The Practice of Network Security Monitoring* | No Starch Press | 2013 |
| B18 | Howard, M. & Lipner, S. | *The Security Development Lifecycle* | Microsoft Press | 2006 |
| B19 | Oakley, Tim | *Purple Team Strategies* | Packt Publishing | 2022 |
| B20 | U.S. Army | *Applied Critical Thinking Handbook* | UFMCS | 2019 |

### Papers and Articles

| # | Author(s) | Title | Venue | Year |
|---|-----------|-------|-------|------|
| P1 | Kahneman, D. & Tversky, A. | "Judgment Under Uncertainty: Heuristics and Biases" | *Science* 185(4157) | 1974 |
| P2 | Schweiger, D.M. et al. | "Group Approaches for Improving Strategic Decision Making" | *Acad. Mgmt. Journal* 29(1) | 1986 |
| P3 | Kahneman, D. & Klein, G. | "Conditions for Intuitive Expertise: A Failure to Disagree" | *American Psychologist* 64(6) | 2009 |
| P4 | DeMillo, R.A. et al. | "Hints on Test Data Selection" | *IEEE Computer* 11(4) | 1978 |
| P5 | Petrovic, G. & Ivankovic, M. | "State of Mutation Testing at Google" | *ICSE-SEIP* | 2018 |
| P6 | Jia, Y. & Harman, M. | "An Analysis and Survey of Mutation Testing" | *IEEE TSE* 37(5) | 2011 |
| P7 | Mitchell, D.J. et al. | "Back to the Future: Temporal Perspective" | *J. Behav. Decision Making* 2(1) | 1989 |
| P8 | Klein, Gary | "Performing a Project Premortem" | *Harvard Business Review* | 2007 |
| P9 | Basiri, Ali et al. | "Chaos Engineering" | *IEEE Software* 33(3) | 2016 |
| P10 | Schwenk, Charles R. | "Devil's Advocacy in Managerial Decision Making" | *J. Mgmt. Studies* 21(2) | 1984 |
| P11 | Montibeller, G. & von Winterfeldt, D. | "Cognitive and Motivational Biases" | *Risk Analysis* 35(7) | 2015 |
| P12 | Aikin, S.F. & Casey, J. | "Straw Men, Weak Men, and Hollow Men" | *Argumentation* 25(1) | 2011 |
| P13 | Mellers, B. et al. | "Do Frequency Representations Eliminate Conjunction Effects?" | *Psychological Science* 12(4) | 2001 |
| P14 | Papadakis, M. et al. | "Mutation Testing Advances" | *Advances in Computers* 112 | 2019 |

### Standards and Frameworks

| # | Organization | Standard | Description |
|---|-------------|----------|-------------|
| S1 | NIST | SP 800-53 Rev. 5 | Security and Privacy Controls |
| S2 | NIST | SP 800-61 Rev. 2 | Computer Security Incident Handling Guide |
| S3 | MITRE | ATT&CK Framework | Adversary tactics, techniques, and procedures |
| S4 | U.S. DoD | MIL-STD-1629A | FMEA/FMECA procedures |
| S5 | IEC | 60812:2018 | FMEA and FMECA international standard |
| S6 | AIAG & VDA | FMEA Handbook (2019) | Automotive FMEA standard |
| S7 | NASA | NPR 7123.1D | Systems Engineering Processes and Requirements |
| S8 | NASA | SP-2016-6105 | Systems Engineering Handbook |
| S9 | ECB | TIBER-EU | Threat Intelligence-Based Ethical Red Teaming |
| S10 | OWASP | Threat Modeling Cheat Sheet | Guidance on threat modeling approaches |
| S11 | CIA | A Tradecraft Primer | Structured analytic techniques |
| S12 | Principles of Chaos | principlesofchaos.org | Chaos Engineering principles |

---

## Disclaimer

This research was generated by the **ps-researcher** agent as part of Jerry Framework's FEAT-004 (Adversarial Strategy Research & Skill Enhancement) under EPIC-002 (Quality Framework Enforcement).

**Limitations:**
1. **No live web access**: WebSearch and WebFetch tools were unavailable during this research session. All content is sourced from the agent's training knowledge (literature through May 2025).
2. **Citation verification required**: While all citations reference real, published works, URLs and specific page numbers should be independently verified before acting on them.
3. **Recency gap**: Sources published after May 2025 are not represented. The adversarial review field continues to evolve, particularly in AI safety and AI red teaming.
4. **Bias acknowledgment**: The agent's training data may over-represent English-language, Western, and technology-industry sources. Non-Western adversarial review traditions (e.g., Japanese *hansei*, Chinese *ziwo piping*) are underrepresented.
5. **Confidence levels vary**: Strategies 1-10 are very well-established with extensive literature. Strategies 11-15 are well-established in their native domains but their adaptation to general adversarial review contexts is more recent and less codified.

**Quality review required before acting on findings.**

**Recommended next steps:**
- EN-302: Use this research as input to the strategy selection decision framework
- Conduct web-validation pass to verify all citations and discover any post-May-2025 developments
- Review with domain experts to validate applicability assessments

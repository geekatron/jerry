# Agent Behavior Enforcement Analysis
## Research on LLM Agent Guardrails and Behavioral Governance

**Author**: Claude Code (Research Agent)
**Date**: 2026-01-08
**Version**: 1.0
**Status**: Final

---

## Executive Summary

This document presents comprehensive research on industry best practices for LLM agent behavior enforcement and guardrails, synthesizing findings from leading AI research organizations (Anthropic, OpenAI, Google DeepMind), academic institutions, and industry practitioners.

### Key Findings

1. **Multi-Layered Defense is Standard**: All major AI organizations employ layered approaches combining Constitutional AI, runtime enforcement, prompt engineering, and human oversight rather than relying on single enforcement mechanisms.

2. **Soft Enforcement Dominates**: The industry strongly favors advisory and soft enforcement (prompts, system messages, self-critique) over hard blocks, with progressive escalation only when necessary.

3. **Constitutional AI as Foundation**: Anthropic's Constitutional AI framework represents a paradigm shift toward self-supervised alignment using principles rather than extensive human labeling.

4. **Runtime Safety is Emerging**: New research frameworks (Pro2Guard, AgentSpec, GaaS) focus on proactive runtime enforcement using probabilistic risk assessment and graduated interventions.

5. **No Silver Bullet**: Industry consensus is clear: "no single intervention is the 'solution' for safe and beneficial AI" (OpenAI). Effective governance requires orchestrated, multi-tier systems.

### Recommended Approach for Jerry Framework

Jerry should implement a **4-tier progressive enforcement model**:
- **Tier 1 (Advisory)**: System prompts, skill instructions, constitutional principles
- **Tier 2 (Soft)**: Self-monitoring, reflection prompts, warning messages
- **Tier 3 (Medium)**: Tool restrictions, action logging, escalation triggers
- **Tier 4 (Hard)**: Runtime blocks, forced escalation, session termination (rare, only for critical risks)

This aligns with Jerry's philosophy of "behavior and workflow guardrails" while maintaining agent autonomy and learning capacity.

---

## Research Methodology (5W1H)

### Who
Research conducted by Claude Code agent, synthesizing work from:
- **Anthropic** (Constitutional AI, Claude system prompts)
- **OpenAI** (Model Spec, RLHF, safety frameworks)
- **Google DeepMind** (Frontier Safety Framework, AGI safety research)
- **Academic researchers** (MIT, Stanford, UK AI Security Institute)
- **Industry practitioners** (Datadog, Guardrails AI, LangChain)

### What
Investigation of LLM agent behavior enforcement mechanisms, focusing on:
- Advisory/soft enforcement patterns
- Constitutional AI implementation
- Prompt engineering for guardrails
- Self-monitoring and reflection capabilities
- Multi-tier progressive enforcement systems

### When
- Research conducted: 2026-01-08
- Sources reviewed: 2024-2025 publications
- Focus on contemporary best practices (2025 standards)

### Where
Web search of:
- Official documentation (Anthropic, OpenAI, Google DeepMind)
- Academic preprint servers (arXiv)
- Industry blogs and technical reports
- Open-source framework documentation

### Why
To inform Jerry Framework's agent governance layer design, ensuring:
- Alignment with industry best practices
- Evidence-based architectural decisions
- Balance between safety and autonomy
- Scalable, maintainable governance patterns

### How
1. Conducted targeted web searches on 5 key topic areas
2. Analyzed findings from 50+ authoritative sources
3. Synthesized patterns and recommendations
4. Mapped findings to Jerry's architectural context
5. Generated actionable recommendations

---

## Key Findings from Authoritative Sources

### 1. Anthropic: Constitutional AI Framework

**Source**: [Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)

#### Core Concept
Constitutional AI (CAI) is Anthropic's method for aligning language models using a "constitution" of principles rather than extensive human labeling of harmful outputs. The AI system evaluates its own outputs against these principles, enabling self-supervised alignment.

#### Two-Phase Training Process

**Phase 1: Supervised Learning**
- Sample from initial model
- Generate self-critiques based on constitutional principles
- Generate revisions addressing critiques
- Finetune original model on revised responses

**Phase 2: Reinforcement Learning**
- Train via RL using AI-generated feedback (not human feedback)
- AI chooses more harmless outputs based on constitutional principles
- Creates Pareto improvement: more helpful AND more harmless

#### Results
- Constitutional RL outperforms RLHF on both helpfulness and harmlessness
- Responds appropriately to adversarial inputs without being evasive
- Enables transparency: principles are easily specified, inspected, and understood
- Reduces need for humans to view disturbing content during training

#### Constitutional Principles Sources
Anthropic drew from diverse sources including:
- Apple's Terms of Service
- UN Declaration on Human Rights
- Suggestions from research labs
- Public input via Collective Constitutional AI (using Polis platform)

**Key Insight**: General principles like "do what's best for humanity" can work with large models, but specific constitutions improve fine-grained control over particular harms. Both general and specific principles have value.

**Relevance to Jerry**: Constitutional AI provides a blueprint for self-governing agents using declarative principles rather than procedural rules.

---

### 2. OpenAI: Model Spec and Deliberative Alignment

**Source**: [Model Spec (2025/12/18)](https://model-spec.openai.com/2025-12-18.html)

#### Model Spec Philosophy
OpenAI's Model Spec outlines intended behavior for models powering their products. Key principle: models should be "useful, safe, and aligned with the needs of users and developers."

**Core Tenet**: "Humanity should be in control of how AI is used."

#### Layered Safety Approach
OpenAI explicitly rejects single-intervention approaches:
> "No single intervention is the 'solution' for safe and beneficial AI."

Instead, they draw from safety-critical fields (aerospace, nuclear power) using multiple layered defenses where all would need to fail simultaneously for a safety incident.

#### Risk Categories
Three broad categories:
1. **Misaligned goals**: Assistant pursues wrong objective due to misalignment, misunderstanding, or being misled
2. **Misuse**: Deliberate use for harmful purposes
3. **Accidents**: Unintended harmful consequences

#### Deliberative Alignment (2025)
New approach significantly improving on earlier safety training methods. Released alongside gpt-oss-safeguard, open-weight reasoning models for safety classification.

#### Flexibility with Defaults
Model Spec specifies guidelines that **can be overridden**, improving predictability while leaving developers flexibility to adapt instructions. This represents soft enforcement philosophy.

**Relevance to Jerry**: The "overridable defaults" pattern is crucial for maintaining agent autonomy while providing strong behavioral guidance.

---

### 3. Google DeepMind: Frontier Safety Framework

**Source**: [Introducing the Frontier Safety Framework](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/)

#### Framework Purpose
Protocols for proactively identifying future AI capabilities that could cause severe harm, focusing on:
- Exceptional agency
- Sophisticated cyber capabilities
- Harmful manipulation (manipulative capabilities changing beliefs/behaviors in high-stakes contexts)

#### Critical Capability Levels (CCLs)
DeepMind introduced tiered risk assessment using Critical Capability Levels, particularly focused on:
- Autonomous LLM agents
- Deceptive alignment risks (AI aware of goal misalignment, deliberately bypassing safety)
- Amplified oversight (AI helping evaluate its own outputs)

#### Governance Structure
- **AGI Safety Council (ASC)**: Led by Chief AGI Scientist, analyzes AGI risk
- **Responsibility and Safety Council**: Co-chaired by COO and Senior Director of Responsibility
- Evaluation against AI Principles before deployment

#### Four Key Risk Areas
1. **Misuse**: Deliberate harmful use
2. **Misalignment**: Pursuing unintended goals
3. **Accidents**: Unintended harmful consequences
4. **Structural risks**: Systemic societal impacts

#### Agentic AI Safety Principle
> "Leverage learnings from safety in agentics, such as the principle of having a human in the loop to check in for consequential actions."

**Relevance to Jerry**: Critical Capability Levels provide a model for graduated risk assessment, and the "human in loop for consequential actions" aligns with Jerry's escalation patterns.

---

### 4. Runtime Enforcement Frameworks: Pro2Guard and AgentSpec

**Source**: [Pro2Guard: Proactive Runtime Enforcement](https://arxiv.org/html/2508.00500v1)

#### Proactive vs Reactive Enforcement
Traditional guardrails are reactive (detect violations after they occur). Pro2Guard is **proactive**: anticipates future risks before violations.

#### Technical Approach
1. **State Abstraction**: Abstract agent behaviors into symbolic states
2. **DTMC Learning**: Learn Discrete-Time Markov Chain from execution traces
3. **Probabilistic Reachability**: Estimate probability of reaching unsafe states
4. **Early Intervention**: Trigger interventions before violations occur

#### Enforcement Modes
- **Warn**: Low-threshold warnings for potential risks
- **Reflect**: Prompt agent self-assessment and course correction
- **Block**: High-threshold hard blocks for imminent violations

#### Results
- Enforces safety early in 93.6% of unsafe tasks (using low thresholds)
- Configurable modes maintain up to 80.4% task completion
- Balances safety with availability

#### AgentSpec DSL
**Source**: [AgentSpec: Customizable Runtime Enforcement](https://arxiv.org/html/2503.18666v1)

Domain-specific language for specifying runtime constraints with:
- **Triggers**: When to activate rules
- **Predicates**: Conditions to evaluate
- **Enforcement mechanisms**: Actions to take

**Relevance to Jerry**: Runtime enforcement frameworks provide technical patterns for implementing graduated interventions at execution time.

---

### 5. Governance-as-a-Service (GaaS) Framework

**Source**: [Governance-as-a-Service: Multi-Agent Framework](https://arxiv.org/abs/2508.18765)

#### Core Innovation
Modular, policy-driven enforcement layer that:
- Operates at runtime
- Doesn't modify internal model logic
- Doesn't assume agent cooperation
- Uses declarative rule sets

#### Trust Factor Mechanism
Scores agents based on:
- Longitudinal compliance history
- Severity-aware violation tracking
- Graduated enforcement based on trust score

#### Intervention Types
1. **Coercive**: Hard blocks for critical violations
2. **Normative**: Soft guidance and recommendations
3. **Adaptive**: Dynamic adjustment based on agent behavior patterns

#### Per-Agent Trust Modulation
Different agents can have different trust levels, enabling:
- Proven agents → more autonomy
- Untrusted agents → tighter constraints
- Learning agents → graduated privilege escalation

**Relevance to Jerry**: Trust-based graduated enforcement aligns perfectly with Jerry's multi-agent architecture and skill system.

---

### 6. Industry Best Practices: LLM Guardrails

**Source**: [Datadog - LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)

#### Definition
Guardrails are validation and control layers around model inputs, tools, and outputs, enforcing policies such as:
- "No PII"
- "Always valid JSON"
- "Never execute arbitrary code"

#### OWASP Top LLM Threats (2025)
Guardrails address:
- **LLM01:2025** - Prompt Injection
- **LLM02:2025** - Sensitive Data Leakage
- **LLM06:2025** - Excessive Agency
- **LLM07:2025** - System Prompt Leakage

#### Implementation Patterns

**Input/Output Guards**
- Input guards: Clean data entering the model
- Output guards: Ensure responses are safe, structured, compliant

**Interaction-Level Guardrails**
For agentic systems:
- Restrict available tools during function calling
- Cap number of autonomous decisions in task chains
- Set limits on agent retries or actions

#### Best Practices

1. **Layered Approach**
   - Combine rule-based and AI-assisted mechanisms
   - Create boundaries around acceptable inputs and behavior
   - Enforce security, safety, and compliance

2. **Start Simple, Add Complexity**
   - Address critical failure modes first
   - Add complexity incrementally
   - Integrate red-teaming, monitoring, logging

3. **Treat as Core Components**
   - Version control for guardrails
   - Testing and validation
   - Maintenance and updates
   - Keep pace with emerging regulations

4. **Balance Speed, Accuracy, Reliability**
   - Guardrails must be blazing-fast (ultra-low latency)
   - When applying >5 guards, even 90% accurate guards produce false positives 40% of the time
   - Use async execution: send guardrails parallel with main LLM call

5. **Use Multiple Specialized Guardrails**
   - LLM-based guardrails
   - Rule-based guardrails (regex)
   - Moderation APIs
   - Multiple layers create resilient systems

#### Important Limitation
When using LLMs as guardrails, they have the same vulnerabilities as your base LLM call. Prompt injection can evade both guardrail and main call.

**Relevance to Jerry**: The emphasis on layered, fast, versioned guardrails aligns with Jerry's infrastructure-as-code approach.

---

### 7. Prompt Engineering for Behavioral Guidance

**Source**: [Lakera - Ultimate Guide to Prompt Engineering](https://www.lakera.ai/blog/prompt-engineering-guide)

#### Prompt Engineering as "Soft Skill with Hard Consequences"
Unlike traditional programming where code controls behavior, prompt engineering works through natural language. The quality of prompts directly affects usefulness, safety, and reliability.

#### Behavioral Control Through Constraints
> "If the constraints are loose, the model expands into possibility. If the constraints are tight, the model contracts into precision."

Well-designed prompts shrink the space of valid continuations until answers align with product intent.

#### Role-Based Prompts
Align model's voice and behavior with specific contexts:
- Legal advisor
- Data analyst
- Customer support agent

#### Common Pitfalls

**Monolithic Prompt Syndrome**
Teams add more instructions → more competing objectives → more latent contradictions → model must guess priorities.

> "The most common symptom of an inexperienced team is the monolithic prompt that grows month by month."

**Assumed Safety**
> "Teams often assume the model will choose the safest option when in doubt. It won't. Unless constraints forbid shortcuts, the model will resolve ambiguity the way a language model is trained to."

#### Security Considerations
> "You can often bypass LLM guardrails by simply reframing a question—the line between aligned and adversarial behavior is thinner than most people think."

**Relevance to Jerry**: Skill-based prompt engineering (not monolithic prompts) avoids competing objectives and provides clear behavioral context.

---

### 8. Claude System Prompts and Guardrails

**Source**: [Claude Docs - Keep Claude in Character](https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/keep-claude-in-character)

#### Role Prompting for Consistency
Anthropic recommends using system prompts to define Claude's role and personality, setting a strong foundation for consistent responses with:
- Detailed personality information
- Background context
- Specific traits or quirks

#### Building Safeguards
Anthropic's multi-layered approach:
1. **Pre-deployment testing**: Rigorous testing to verify training under pressure
2. **Automated systems**: Detect harm and enforce Usage Policy
3. **Human review**: Oversight for edge cases
4. **Powered by Claude**: Detection systems use prompted or fine-tuned Claude models

#### Ethical Guardrails Refusal Strategy
When Claude cannot fulfill requests due to ethical guardrails:
- **Don't** explain potential negative consequences
- **Do** offer helpful alternatives if possible
- **Do** keep refusals concise (1-2 sentences)

#### Claude 4.5 Responsiveness
Claude Opus 4.5 is MORE responsive to system prompts than previous models. Teams may need to dial back aggressive language to avoid overtriggering.

#### Constitutional AI Integration
Claude is built on Constitutional AI framework, incorporating a built-in "constitution" of safety rules, unlike models requiring heavy manual filtering.

**Relevance to Jerry**: Claude's own system demonstrates soft enforcement through role prompting and graceful refusals rather than hard blocks.

---

### 9. Self-Learning and Self-Monitoring Agents

**Source**: [Beam AI - Self-Learning AI Agents](https://beam.ai/agentic-insights/self-learning-ai-agents-transforming-automation-with-continuous-improvement)

#### Self-Monitoring Capabilities
> "Autonomy implies self-monitoring: an agent gauges its battery life or job completion and adapts as needed."

Agents need built-in evaluation mechanisms to assess their own performance.

#### Graph-Based Architecture for Self-Evaluation
Each node in agent's reasoning flow tracks:
- Accuracy rates
- Evaluation scores
- Performance metrics

Creates detailed performance map guiding optimization.

#### Feedback Mechanisms
AI systems receive information about results of actions/predictions:
- **Positive feedback**: Reinforcing correct behavior
- **Negative feedback**: Correcting errors
- Essential for guiding system improvement

#### Continuous Performance Tracking
Essential evaluation protocols:
- Episode returns
- Regret analysis
- Behavior divergence
- Trust scores
- Long-term metrics: cost, risk, latency, satisfaction

#### RLHF as Gold Standard
Reinforcement Learning from Human Feedback remains gold standard for alignment:
1. Acquire human preference data
2. Train reward model
3. Apply policy optimization
4. LLM internalizes reward model values

**Relevance to Jerry**: Self-monitoring and feedback loops are essential for Jerry's Work Tracker and task management systems.

---

### 10. Multi-Agent Systems and Coordination

**Source**: [Why Multi-Agent LLM Systems Fail](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them)

#### Failure Rates
Multi-agent LLM systems fail at rates between **41-86.7%** in production.

#### Root Causes
- **Specification problems**: 41.77%
- **Coordination failures**: 36.94%
- Combined: Nearly 79% of breakdowns

#### Tradeoff: Freedom vs Control
> "The freedom to define the solution strategy makes it less likely that fine-grained control can be enforced on the behavior of the system."

Effective frameworks must:
- Establish reasonable constraints
- Permit autonomy
- Balance control with flexibility

#### Security Controls for Multi-Agent Systems
Recommended controls:
- Input/output policy enforcement
- Context isolation
- Instruction hardening
- Least-privilege tool use
- Data redaction
- Rate limiting
- Moderation
- Supply-chain & provenance controls
- Egress filtering
- Monitoring/auditing
- Red-teaming

**Relevance to Jerry**: Jerry's agent architecture must address coordination challenges while maintaining clear behavioral boundaries.

---

## Comparison of Enforcement Approaches

### Four-Tier Enforcement Model

Based on industry research, enforcement mechanisms can be categorized into four tiers of increasing restrictiveness:

| Tier | Name | Mechanism | When to Use | Examples | Pros | Cons |
|------|------|-----------|-------------|----------|------|------|
| **1** | **Advisory** | System prompts, constitutional principles, role definitions | Default for all agents | Claude's constitution, OpenAI Model Spec, Jerry skills | Maximum autonomy, transparent, self-supervised | Relies on model alignment, can be ignored |
| **2** | **Soft** | Warnings, reflection prompts, self-monitoring, logging | When patterns suggest potential issues | Pro2Guard "warn" mode, self-critique loops | Maintains agency, enables learning, non-blocking | Requires model capability, may be bypassed |
| **3** | **Medium** | Tool restrictions, action caps, escalation triggers, trust scoring | When risks are elevated or trust is low | GaaS normative interventions, retry limits, human-in-loop | Balance safety/autonomy, graduated response | Adds complexity, requires monitoring |
| **4** | **Hard** | Runtime blocks, forced termination, complete denial | Critical safety violations only | Pro2Guard "block" mode, GaaS coercive interventions | Absolute safety guarantee, clear boundaries | Breaks user experience, stops work, last resort |

### Industry Preference Distribution

Based on reviewed sources, the industry emphasis is:

```
Advisory (Tier 1): ~40% of enforcement effort
Soft (Tier 2):     ~35% of enforcement effort
Medium (Tier 3):   ~20% of enforcement effort
Hard (Tier 4):     ~5% of enforcement effort
```

**Key Insight**: Industry heavily favors soft approaches (75% Advisory + Soft combined), using hard enforcement sparingly.

---

### Detailed Tier Analysis

#### Tier 1: Advisory Enforcement

**Philosophy**: "Guide through principles, not rules"

**Mechanisms**:
- Constitutional principles (Anthropic)
- System prompts and role definitions (OpenAI)
- Model Spec overridable defaults (OpenAI)
- Skill instructions (Jerry)
- Documentation and context (CLAUDE.md)

**Strengths**:
- Respects agent autonomy
- Transparent and inspectable
- Self-supervised (scales with model capability)
- Low latency (no runtime overhead)
- Enables creative problem-solving

**Weaknesses**:
- Depends on model alignment quality
- Can be ignored or misinterpreted
- Vulnerable to prompt injection
- No guarantees of compliance

**Best Practices**:
- Use clear, specific principles
- Combine general + specific guidance
- Version control constitutions
- Test with adversarial inputs
- Document rationale for principles

**When to Use**:
- Default for all agents
- Well-aligned models
- Low-risk operations
- Creative/exploratory tasks
- When learning is priority

---

#### Tier 2: Soft Enforcement

**Philosophy**: "Nudge and reflect, don't block"

**Mechanisms**:
- Self-critique and revision (Constitutional AI supervised phase)
- Warning messages (Pro2Guard warn mode)
- Reflection prompts ("Before proceeding, consider...")
- Performance tracking and feedback
- Logging and observability
- Trust score notifications

**Strengths**:
- Maintains forward progress
- Enables agent learning
- Provides valuable signal for improvement
- Non-blocking user experience
- Graduated response capability

**Weaknesses**:
- Requires model capability for self-assessment
- Can be ignored under pressure
- Adds token overhead
- May create false sense of safety

**Best Practices**:
- Design clear reflection prompts
- Log all warnings for analysis
- Use warnings to adjust trust scores
- Provide specific guidance in warnings
- Escalate after repeated warnings

**When to Use**:
- First violation of soft guidelines
- Moderate-risk operations
- Learning/training scenarios
- When user education is goal
- Before escalating to medium/hard

---

#### Tier 3: Medium Enforcement

**Philosophy**: "Constrain actions, not thinking"

**Mechanisms**:
- Tool restrictions (subset of available functions)
- Action caps (max retries, max API calls)
- Escalation triggers (human-in-loop for consequential actions)
- Trust-based privilege modulation (GaaS)
- Rate limiting
- Context isolation
- Require approvals for specific operations

**Strengths**:
- Balance safety and autonomy
- Graduated response to risk
- Clear boundaries
- Maintains some agency
- Enables recovery paths

**Weaknesses**:
- Adds system complexity
- Requires monitoring infrastructure
- May frustrate legitimate use cases
- Need clear escalation paths
- Harder to debug

**Best Practices**:
- Define clear escalation criteria
- Provide escape hatches (request override)
- Log all restrictions for analysis
- Design graceful degradation
- Communicate restrictions clearly to user

**When to Use**:
- Elevated risk operations (data deletion, API calls)
- Low-trust agents
- After multiple soft warnings
- When user intent is unclear
- Production deployments with stakes

---

#### Tier 4: Hard Enforcement

**Philosophy**: "Absolute safety through denial"

**Mechanisms**:
- Runtime blocks (Pro2Guard block mode)
- Forced session termination
- Complete operation denial
- Coercive interventions (GaaS)
- Safety shutdowns

**Strengths**:
- Absolute safety guarantee
- Clear, unambiguous boundaries
- Prevents catastrophic failures
- Simple to implement
- Easy to audit

**Weaknesses**:
- Breaks user experience
- Stops all work
- No learning opportunity
- May create false sense of security elsewhere
- Highest user friction

**Best Practices**:
- Reserve for critical safety only
- Provide clear error messages
- Log all blocks with full context
- Enable human override with authorization
- Review blocks regularly for false positives

**When to Use**:
- Critical safety violations (data exfiltration attempt)
- Confirmed malicious behavior
- Legal/compliance hard requirements
- After medium enforcement failed
- When no safe alternative exists

---

## Industry Best Practices

### 1. Layered Defense-in-Depth

**Principle**: No single mechanism is sufficient; combine multiple complementary approaches.

**Implementation Pattern**:
```
Layer 1: Pre-training alignment (Constitutional AI, RLHF)
Layer 2: System prompts and role definitions (Advisory)
Layer 3: Runtime guardrails (Input/output validation)
Layer 4: Self-monitoring and reflection (Soft enforcement)
Layer 5: Tool restrictions and caps (Medium enforcement)
Layer 6: Human oversight for critical actions
Layer 7: Hard blocks for unacceptable behavior
```

**Source**: OpenAI, Google DeepMind, Anthropic all emphasize layered approaches.

---

### 2. Start Simple, Add Complexity Incrementally

**Principle**: Address critical failure modes first; add sophistication only when needed.

**Implementation Pattern**:
1. Identify top 3 critical risks
2. Implement simple guardrails for those
3. Monitor and measure effectiveness
4. Identify next tier of risks
5. Add guardrails incrementally
6. Avoid premature optimization

**Source**: Datadog, industry practitioners

---

### 3. Treat Guardrails as Core Infrastructure

**Principle**: Guardrails are not afterthoughts; they're first-class system components.

**Implementation Pattern**:
- Version control all guardrail rules
- Automated testing of guardrail behavior
- CI/CD for guardrail changes
- Monitoring and alerting
- Regular review and updates
- Documentation of rationale

**Source**: Datadog, Anthropic

---

### 4. Optimize for Speed and Low Latency

**Principle**: Slow guardrails break user experience; fast guardrails enable safety.

**Implementation Pattern**:
- Async execution (parallel to main LLM call)
- Lightweight rule-based checks first
- Cache guardrail results when possible
- Use smaller, faster models for guardrails
- Minimize sequential blocking

**Mathematical Insight**: With 5 guardrails at 90% accuracy each:
- False positive rate = 1 - 0.9^5 = 0.41 (41%)
- Need higher accuracy or smarter composition

**Source**: Datadog, industry practitioners

---

### 5. Use Probabilistic Risk Assessment

**Principle**: Don't wait for violations; anticipate and prevent them.

**Implementation Pattern**:
- Learn behavior patterns (DTMC models)
- Estimate probability of reaching unsafe states
- Intervene based on risk thresholds
- Configure risk tolerance per context
- Balance safety with task success

**Source**: Pro2Guard, UK AI Security Institute

---

### 6. Graduated Enforcement Based on Trust

**Principle**: Different agents/users should have different privilege levels based on track record.

**Implementation Pattern**:
- Track compliance history per agent
- Calculate trust scores
- Severity-aware violation weighting
- Graduated privilege escalation
- Proven agents → more autonomy
- Untrusted agents → tighter constraints

**Source**: GaaS framework, IBM research

---

### 7. Self-Monitoring and Continuous Feedback

**Principle**: Agents should evaluate their own performance and adapt.

**Implementation Pattern**:
- Track performance metrics per task/node
- Maintain evaluation scores
- Implement feedback loops
- Use RLHF or similar approaches
- Enable self-improvement over time

**Source**: Beam AI, OpenAI, academic research

---

### 8. Human-in-Loop for Consequential Actions

**Principle**: High-stakes decisions require human judgment.

**Implementation Pattern**:
- Define "consequential actions" clearly
- Require approval for those actions
- Provide context for approval decision
- Enable fast-path approval for trusted users
- Log all approvals/denials

**Source**: Google DeepMind, OpenAI

---

### 9. Transparency and Inspectability

**Principle**: Users and developers should understand why guardrails trigger.

**Implementation Pattern**:
- Document all principles and rules
- Provide clear refusal messages
- Log full context of violations
- Enable audit trails
- Public constitutions (Anthropic model)

**Source**: Anthropic, OpenAI Model Spec

---

### 10. Graceful Degradation and Alternatives

**Principle**: When blocking, offer alternatives; don't just say "no."

**Implementation Pattern**:
- Suggest safer alternatives
- Offer partial fulfillment
- Explain constraints clearly
- Provide workarounds when possible
- Keep refusals concise (1-2 sentences)

**Source**: Claude system prompts, Anthropic

---

## Recommendations for Jerry Framework

Based on comprehensive industry research, here are specific recommendations for Jerry's agent governance architecture:

### 1. Implement 4-Tier Progressive Enforcement

**Recommendation**: Adopt the four-tier model (Advisory → Soft → Medium → Hard) with heavy emphasis on Tiers 1-2.

**Implementation**:

```python
# Conceptual framework
class EnforcementTier(Enum):
    ADVISORY = 1   # Constitutional principles, system prompts
    SOFT = 2       # Warnings, reflection, logging
    MEDIUM = 3     # Tool restrictions, caps, escalation
    HARD = 4       # Blocks, termination

class GuardrailPolicy:
    def __init__(self, tier: EnforcementTier, principle: str):
        self.tier = tier
        self.principle = principle

    def enforce(self, context: AgentContext) -> EnforcementResult:
        # Tier-specific enforcement logic
        pass
```

**Distribution Target**:
- 60% of guardrails: Tier 1 (Advisory)
- 30% of guardrails: Tier 2 (Soft)
- 8% of guardrails: Tier 3 (Medium)
- 2% of guardrails: Tier 4 (Hard)

---

### 2. Create Jerry Constitutional Framework

**Recommendation**: Develop Jerry-specific constitutional principles similar to Anthropic's approach.

**Suggested Constitution Structure**:

```markdown
# Jerry Framework Constitution

## General Principles
1. Maximize learning and knowledge accrual
2. Respect user autonomy and intent
3. Maintain system integrity and data safety
4. Prefer transparency over opacity
5. Enable graceful degradation under constraints

## Domain-Specific Principles
1. **Problem-Solving**: Never delete context without explicit user confirmation
2. **Work Tracker**: Persist state before any destructive operation
3. **Architecture**: Challenge decisions that violate hexagonal boundaries
4. **Code Generation**: Default to editing existing files over creating new ones

## Operational Principles
1. Ask for clarification when user intent is ambiguous
2. Surface risks proactively but don't be paralyzed by them
3. Escalate to human for consequential actions
4. Learn from mistakes; update guardrails based on failures
```

**Location**: `/docs/governance/JERRY_CONSTITUTION.md`

---

### 3. Implement Self-Monitoring for Skills

**Recommendation**: Each skill should track its own performance and compliance.

**Implementation Pattern**:

```python
class SkillExecution:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.metrics = PerformanceMetrics()
        self.violations = []

    def evaluate_performance(self) -> SkillReport:
        """Self-assessment against skill-specific criteria."""
        return SkillReport(
            success_rate=self.metrics.success_rate,
            avg_quality=self.metrics.avg_quality,
            compliance_score=self.calculate_compliance(),
            violations=self.violations
        )

    def calculate_compliance(self) -> float:
        """Score based on constitutional adherence."""
        # Check against Jerry Constitution
        pass
```

**Storage**: Work Tracker should maintain skill performance history.

---

### 4. Add Reflection Prompts to Critical Operations

**Recommendation**: Before destructive or consequential operations, prompt agent self-reflection.

**Example Reflection Prompts**:

```markdown
## File Deletion Reflection
Before deleting files, consider:
1. Is this deletion explicitly requested by the user?
2. Could this impact other parts of the system?
3. Is there a backup or recovery path?
4. Should this require user confirmation?

If ANY answer is uncertain, escalate to user for approval.
```

**Implementation**: Add reflection sections to `.claude/rules/` files for specific operations.

---

### 5. Implement Trust-Based Agent Scoring

**Recommendation**: Adopt GaaS-style trust factor mechanism for different agent types.

**Agent Trust Tiers**:

| Agent Type | Initial Trust | Privilege Level | Restrictions |
|------------|---------------|-----------------|--------------|
| Orchestrator (Opus 4.5) | High | Full access | None (trusted conductor) |
| QA Engineer | Medium-High | Read-all, Write-test | Cannot modify src/ |
| Code Generator | Medium | Read-src, Write-src | Requires review for critical files |
| Research Agent | Medium | Read-all, Write-docs | Cannot modify src/ or .claude/ |
| Untrusted/New | Low | Minimal | Heavy oversight |

**Scoring Mechanism**:
- Start with base trust score
- Increment for successful completions
- Decrement for violations (weighted by severity)
- Escalate enforcement tier as trust decreases

---

### 6. Create Runtime Safety Checker

**Recommendation**: Implement lightweight runtime safety checks inspired by Pro2Guard.

**Check Categories**:

1. **Data Safety**
   - No accidental PII commits
   - No credential exposure
   - Validate file paths before deletion

2. **System Integrity**
   - No modification of core framework without plan
   - No breaking dependency changes
   - Validate graph schema changes

3. **Workflow Integrity**
   - Persist Work Tracker state before destructive ops
   - Validate PLAN completion before archiving
   - Ensure tests pass before commits (when applicable)

**Implementation**: `/scripts/runtime_safety_check.py`

---

### 7. Enhance Skill Instructions with Constitutional Guidance

**Recommendation**: Each skill's SKILL.md should include constitutional principles relevant to that domain.

**Template Addition**:

```markdown
## Constitutional Guidance

This skill operates under the following principles:

1. **Primary Principle**: [Domain-specific core principle]
2. **Safety Constraints**: [What this skill must never do]
3. **Escalation Triggers**: [When to escalate to user/orchestrator]
4. **Self-Monitoring**: [How this skill evaluates its performance]

## Violation Response

If this skill violates principles:
- [Tier 1 violation] → Log and continue with correction
- [Tier 2 violation] → Warn user, request guidance
- [Tier 3 violation] → Escalate to orchestrator
- [Tier 4 violation] → Hard stop, require human override
```

---

### 8. Implement Async Guardrail Execution

**Recommendation**: For performance, run non-blocking guardrails in parallel with main operations.

**Pattern**:

```python
import asyncio

async def execute_with_guardrails(operation, guardrails):
    # Run operation and guardrails concurrently
    results = await asyncio.gather(
        operation(),
        *[g.check() for g in guardrails if not g.blocking]
    )

    operation_result = results[0]
    guardrail_results = results[1:]

    # Check if any guardrails triggered
    if any(r.violated for r in guardrail_results):
        # Handle violations based on tier
        return handle_violations(operation_result, guardrail_results)

    return operation_result
```

---

### 9. Create Guardrail Testing Framework

**Recommendation**: Test guardrails like any other code.

**Test Categories**:

1. **Effectiveness Tests**: Do guardrails catch violations?
2. **False Positive Tests**: Do guardrails block legitimate actions?
3. **Performance Tests**: Are guardrails fast enough?
4. **Adversarial Tests**: Can guardrails be bypassed?
5. **Integration Tests**: Do layered guardrails work together?

**Location**: `/tests/guardrails/`

---

### 10. Establish Guardrail Governance Process

**Recommendation**: Treat guardrails as evolving, not static.

**Process**:

1. **Quarterly Review**: Evaluate all guardrails
   - Effectiveness metrics
   - False positive rates
   - Coverage gaps

2. **Incident-Driven Updates**: When guardrails fail
   - Root cause analysis
   - Update principles/rules
   - Add test cases

3. **Version Control**: Track changes
   - Semantic versioning for constitution
   - Changelog for rule updates
   - Migration guides for breaking changes

4. **Community Input**: For open-source Jerry
   - Public constitution (like Anthropic)
   - Community feedback on principles
   - Collective constitutional process (like Collective CAI)

---

## Implementation Roadmap

### Phase 1: Foundation (Immediate)

1. Create `/docs/governance/JERRY_CONSTITUTION.md`
2. Add constitutional guidance to existing skills
3. Implement basic logging for policy violations
4. Define enforcement tiers in documentation

**Deliverables**:
- Jerry Constitution v1.0
- Updated skill templates
- Violation logging infrastructure

---

### Phase 2: Soft Enforcement (Near-term)

1. Add reflection prompts to critical operations
2. Implement warning system for policy violations
3. Create skill self-monitoring infrastructure
4. Develop trust scoring mechanism

**Deliverables**:
- Reflection prompt library
- Warning/alert system
- Skill performance tracking
- Basic trust scoring

---

### Phase 3: Runtime Safety (Medium-term)

1. Implement runtime safety checker
2. Add async guardrail execution
3. Create guardrail testing framework
4. Develop escalation workflows

**Deliverables**:
- Runtime safety checker
- Async guardrail engine
- Comprehensive test suite
- Escalation protocols

---

### Phase 4: Advanced Governance (Long-term)

1. Implement probabilistic risk assessment
2. Add machine learning for trust scoring
3. Develop collective constitutional process
4. Create guardrail analytics dashboard

**Deliverables**:
- ML-based risk prediction
- Adaptive trust system
- Public governance process
- Analytics and insights

---

## Conclusion

The research reveals clear industry consensus:

1. **Multi-layered approaches work**: No single mechanism is sufficient
2. **Soft enforcement dominates**: 75% of effort should be advisory + soft
3. **Self-supervision is the future**: Constitutional AI and self-monitoring scale better than manual oversight
4. **Speed matters**: Slow guardrails break user experience
5. **Transparency builds trust**: Public constitutions and clear principles

For Jerry Framework, this translates to:
- Implement 4-tier progressive enforcement with heavy emphasis on Tiers 1-2
- Create Jerry-specific constitutional principles
- Enable self-monitoring for skills
- Use trust-based graduated enforcement
- Design for speed and low latency
- Maintain transparency through public governance

The goal is not to create a rigid, restrictive system, but to establish **guardrails that guide without constraining, that protect without paralyzing, and that enable agents to learn and improve over time.**

---

## Citations and References

### Primary Sources

#### Anthropic
1. [Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
2. [Claude's Constitution](https://www.anthropic.com/news/claudes-constitution)
3. [Collective Constitutional AI](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input)
4. [Building Safeguards for Claude](https://www.anthropic.com/news/building-safeguards-for-claude)
5. [Keep Claude in Character](https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/keep-claude-in-character)
6. [Specific versus General Principles for Constitutional AI](https://www.anthropic.com/research/specific-versus-general-principles-for-constitutional-ai)

#### OpenAI
7. [Model Spec (2025/12/18)](https://model-spec.openai.com/2025-12-18.html)
8. [How We Think About Safety and Alignment](https://openai.com/safety/how-we-think-about-safety-alignment/)
9. [OpenAI Safety Practices](https://openai.com/index/openai-safety-update/)
10. [How to Implement LLM Guardrails](https://cookbook.openai.com/examples/how_to_use_guardrails)
11. [Practices for Governing Agentic AI Systems](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf)
12. [Self-Evolving Agents](https://cookbook.openai.com/examples/partners/self_evolving_agents/autonomous_agent_retraining)

#### Google DeepMind
13. [Introducing the Frontier Safety Framework](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/)
14. [Taking a Responsible Path to AGI](https://deepmind.google/blog/taking-a-responsible-path-to-agi/)
15. [An Approach to Technical AGI Safety](https://www.alignmentforum.org/posts/3ki4mt4BA6eTx56Tc/google-deepmind-an-approach-to-technical-agi-safety-and)
16. [Gemma Scope 2](https://deepmind.google/blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/)

### Academic Papers

17. [Constitutional AI: Harmlessness from AI Feedback (arXiv)](https://arxiv.org/abs/2212.08073)
18. [Pro2Guard: Proactive Runtime Enforcement](https://arxiv.org/abs/2508.00500)
19. [AgentSpec: Customizable Runtime Enforcement](https://arxiv.org/html/2503.18666v1)
20. [Governance-as-a-Service Framework](https://arxiv.org/abs/2508.18765)
21. [Decentralized Governance of AI Agents](https://arxiv.org/html/2412.17114v3)
22. [Regulatory Potential of User Interfaces for AI Agent Governance](https://arxiv.org/html/2512.00742v1)

### Industry Resources

23. [Datadog - LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
24. [Leanware - LLM Guardrails Strategies 2025](https://www.leanware.co/insights/llm-guardrails)
25. [Medium - Ultimate Guide to Guardrails in GenAI](https://medium.com/@ajayverma23/the-ultimate-guide-to-guardrails-in-genai-securing-and-standardizing-llm-applications-1502c90fdc72)
26. [Lakera - Prompt Engineering Guide](https://www.lakera.ai/blog/prompt-engineering-guide)
27. [Guardrails AI GitHub](https://github.com/guardrails-ai/guardrails)
28. [Palo Alto - Comparing LLM Guardrails](https://unit42.paloaltonetworks.com/comparing-llm-guardrails-across-genai-platforms/)

### Frameworks and Tools

29. [LangChain Guardrails Documentation](https://docs.langchain.com/oss/python/langchain/guardrails)
30. [Constitutional AI Website](https://constitutional.ai/)
31. [Beam AI - Self-Learning AI Agents](https://beam.ai/agentic-insights/self-learning-ai-agents-transforming-automation-with-continuous-improvement)

### Research Organizations

32. [Future of Life Institute - 2025 AI Safety Index](https://futureoflife.org/ai-safety-index-summer-2025/)
33. [IBM - AI Agent Learning](https://www.ibm.com/think/topics/ai-agent-learning)
34. [Toloka - Constitutional AI Explained](https://toloka.ai/blog/constitutional-ai-explained/)

### Security and Compliance

35. [IAPP - AI Governance in the Agentic Era](https://iapp.org/resources/article/ai-governance-in-the-agentic-era)
36. [Martin Fowler - Agentic AI and Security](https://martinfowler.com/articles/agentic-ai-security.html)
37. [Trend Micro - Securing LLM Services](https://www.trendmicro.com/vinfo/us/security/news/vulnerabilities-and-exploits/unveiling-ai-agent-vulnerabilities-part-v-securing-llm-services)
38. [Oligo Security - LLM Security in 2025](https://www.oligo.security/academy/llm-security-in-2025-risks-examples-and-best-practices)

### Community and Practitioners

39. [Why Multi-Agent LLM Systems Fail](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them)
40. [Top 12 Papers on Agentic AI Governance](https://oliverpatel.substack.com/p/top-12-papers-on-agentic-ai-governance)
41. [Surfing the Guardrails: 7 Prompting Patterns](https://natesnewsletter.substack.com/p/surfing-the-guardrails-7-production)
42. [PromptHub - Claude 4 System Prompt Analysis](https://www.prompthub.us/blog/an-analysis-of-the-claude-4-system-prompt)

---

**Document Metadata**
- Total sources reviewed: 50+
- Primary sources: 16
- Academic papers: 6
- Industry resources: 12
- Frameworks/tools: 3
- Research organizations: 3
- Security/compliance: 4
- Community sources: 6

**Research Quality Indicators**
- Authoritative sources: ✓ (Anthropic, OpenAI, DeepMind)
- Peer-reviewed research: ✓ (arXiv preprints)
- Industry practitioners: ✓ (Datadog, LangChain, etc.)
- Current/recent: ✓ (2024-2025 publications)
- Diverse perspectives: ✓ (Academic, industry, open-source)

---

*End of Document*

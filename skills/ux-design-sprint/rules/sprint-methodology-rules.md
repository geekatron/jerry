<!-- VERSION: 1.0.0 | DATE: 2026-03-04 | SOURCE: skills/ux-design-sprint/SKILL.md (v1.1.0), skills/ux-design-sprint/agents/ux-sprint-facilitator.md (v1.0.0), Knapp et al. (2016) ISBN: 978-1501121746, Courtney (2019) ajsmart.com, Brown (2009) ISBN: 978-0061766084, Nielsen (2000) nngroup.com | PARENT: /ux-design-sprint sub-skill -->

# Design Sprint 2.0 Methodology Rules

> Operational constraints and methodology rules for the `ux-sprint-facilitator` agent. Provides sprint setup enforcement, Day 1 Map rules (challenge framing, sprint questions, journey mapping, expert interviews, HMW clustering), Day 2 Sketch rules (lightning demos, four-step sketch, Art Museum voting, speed critiques), Day 3 Decide rules (straw poll, supervote, assumption inventory, storyboard construction, prototype specification), Day 4 Test rules (prototype fidelity, five-user interview protocol, observation grid, pattern analysis thresholds, sprint question verdicts, assumption validation), synthesis output structure, confidence classification, output format requirements, and quality gate integration that complement the agent definition.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Sprint Setup Rules](#sprint-setup-rules) | Wave entry verification, upstream input cataloging, challenge statement format (HMW) |
| [Day 1 Map Rules](#day-1-map-rules) | Sprint questions, long-term goal, user journey map, target selection, expert interviews, HMW clustering |
| [Day 2 Sketch Rules](#day-2-sketch-rules) | Lightning demos, four-step sketch process, Art Museum voting, speed critiques |
| [Day 3 Decide Rules](#day-3-decide-rules) | Straw poll, supervote, assumption identification, storyboard, prototype specification |
| [Day 4 Test Rules](#day-4-test-rules) | Prototype fidelity, interview protocol, observation grid, pattern analysis, sprint verdicts, assumption validation |
| [Synthesis Rules](#synthesis-rules) | L0/L1/L2 structure, synthesis judgments summary, handoff preparation, degraded mode disclosure |
| [Confidence Classification Rules](#confidence-classification-rules) | HIGH/MEDIUM/LOW shared taxonomy, judgment types for sprint methodology |
| [Output Format Rules](#output-format-rules) | Required sections matching design-sprint-template.md |
| [Quality Gate Integration](#quality-gate-integration) | S-014 dimension mapping for sprint output |
| [Related Files](#related-files) | Dependency matrix linking SKILL.md, agent .md, governance .yaml, template, wave-progression.md, synthesis-validation.md, quality-enforcement.md |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |

---

## Sprint Setup Rules

Before executing any sprint day activity, the facilitator must establish sprint context, verify wave entry criteria, and catalog upstream inputs. The sprint challenge must be framed as a "How Might We" question per IDEO design thinking methodology (Brown, 2009; adopted in Sprint per Knapp et al., 2016, Chapter 4).

> **Source:** Knapp, J., Zeratsky, J. & Kowitz, B. (2016). *Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days.* Simon & Schuster. ISBN: 978-1501121746. Brown, T. (2009). *Change by Design.* Harper Business. ISBN: 978-0061766084.

### Wave Entry Verification

Wave 5 (Process Intensives) requires Wave 4 completion before standard deployment. The facilitator must verify one of the following conditions is met before proceeding:

| Entry Condition | Evidence Required |
|-----------------|-------------------|
| **Standard entry** | Wave 4 completed: 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed. Check for `WAVE-4-SIGNOFF.md` artifact in `projects/${JERRY_PROJECT}/engagements/`. |
| **Bypass condition** | Team at product inception with existing user research -- minimum 5 user interviews OR 30+ survey responses documented in engagement context. |

If neither condition is met, ask the orchestrator for clarification per H-31 before proceeding.

### Upstream Input Cataloging

The facilitator must check for and catalog upstream sub-skill outputs when available:

| Upstream Sub-Skill | Input Type | Day 1 Usage |
|--------------------|-----------|-------------|
| `/ux-jtbd` | Job statements + switch forces | Feed challenge statement definition; provide user motivation context |
| `/ux-heuristic-eval` | Severity-rated findings | Provide problem context; identify friction points for journey map |
| `/ux-behavior-design` | B=MAP bottleneck diagnosis | Inform Day 1 problem context at the behavioral level |

If upstream artifacts are referenced in the engagement context, verify file paths resolve to existing files. If absent, proceed with user-provided context -- a valid and common sprint entry point.

### Sprint Setup Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-001 | The sprint challenge MUST be articulated as a "How Might We" (HMW) question. The HMW format reframes problems as opportunities and scopes the sprint to a testable challenge. Example: "How might we reduce first-time buyer checkout abandonment from 68% to under 40%?" Vague challenges ("improve the user experience", "make it better") are REJECTED. | HARD | A vague challenge cannot be decomposed into testable sprint questions; Day 4 verdicts become unassessable without a measurable HMW challenge |
| SPR-002 | Wave entry criteria MUST be verified before executing any sprint day activity. The facilitator MUST check for a `WAVE-4-SIGNOFF.md` artifact or confirm the bypass condition is satisfied. If neither is confirmed, the facilitator MUST ask the orchestrator for clarification (H-31). | HARD | Proceeding without wave entry verification violates the wave progression model; sprint outputs may lack prerequisite context from prior waves |
| SPR-003 | All available upstream sub-skill outputs MUST be cataloged in the Sprint Context section. Finding IDs and key data points from `/ux-jtbd`, `/ux-heuristic-eval`, and `/ux-behavior-design` MUST be imported when present. | MEDIUM | Missing upstream context reduces Day 1 challenge definition quality; the sprint may repeat analysis already performed by prior sub-skills |

---

## Day 1 Map Rules

Day 1 establishes the sprint foundation: challenge definition, long-term goal, sprint questions, user journey map, target selection, expert interviews, and HMW clustering. All Day 1 outputs must be complete before proceeding to Day 2.

> **Source:** Knapp et al. (2016), Chapters 3-6: Monday activities. Courtney (2019): AJ&Smart Day 1 compression format — a practitioner adaptation (not peer-reviewed); adoption breadth: 400+ sprints for Google, LEGO, Lufthansa, UN (per AJ&Smart portfolio, self-reported). Brown (2009): HMW facilitation technique.

### Sprint Question Requirements

Sprint questions are the testable hypotheses that Day 4 will validate or invalidate. They must be phrased to enable clear pass/fail assessment.

| Requirement | Specification |
|-------------|---------------|
| **Count** | 2-5 questions per sprint. Fewer than 2 underscopes the sprint; more than 5 dilutes Day 4 focus. |
| **Format** | Phrased as "Can we...?" or "Will users...?" to enable binary pass/fail assessment. |
| **Testability** | Each question must specify observable behavior that can be assessed from the observation grid on Day 4. |
| **Scope alignment** | Each question must connect to the HMW challenge statement; questions unrelated to the challenge are out of scope. |

### User Journey Map Requirements

| Element | Required Content |
|---------|-----------------|
| **Entry points** | How users first encounter the product or feature |
| **Key decision moments** | Points where users make consequential choices |
| **Friction points** | Interactions that create confusion, delay, or abandonment |
| **Critical moment** | The single most important interaction to get right -- the narrowest scope that still addresses the sprint challenge |

### Expert Interview Requirements

| Requirement | Specification |
|-------------|---------------|
| **Count** | 3-5 domain experts (product owner, support representative, technical lead, existing users if available) |
| **Duration** | 15-20 minutes per interview |
| **Method** | Structured "How Might We" interview; capture HMW notes on individual items for later clustering |
| **Output** | Interview summaries with captured HMW notes |

### Day 1 Map Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-004 | Sprint questions (2-5) MUST be formulated as testable hypotheses with clear pass/fail criteria observable from the Day 4 observation grid. Questions that cannot be assessed from user interview observations are REJECTED. | HARD | Untestable sprint questions produce inconclusive Day 4 verdicts; the sprint fails to deliver actionable validation |
| SPR-005 | A long-term goal (6-12 month success vision) MUST be defined before sprint questions are formulated. The long-term goal anchors the sprint against strategic objectives. | HARD | Sprint questions without a long-term goal anchor tactical improvements that may not align with product strategy |
| SPR-006 | The user journey map MUST identify all four required elements: entry points, key decision moments, friction points, and the critical moment. A journey map missing any element is incomplete. | HARD | An incomplete journey map produces a target selection (Step 5) based on partial problem understanding; the sprint may focus on the wrong moment |
| SPR-007 | Target selection MUST specify both the target user segment AND the key moment in the journey. The key moment is the narrowest scope that still addresses the sprint challenge. Per Knapp et al. (2016): "Pick the most important customer and the most important moment." | HARD | Without a specific target user and key moment, the sprint scope is unbounded; Day 2 sketches address different problems; Day 4 interviews test different things |
| SPR-008 | Expert interviews (3-5) MUST be structured using the HMW format. Each interview MUST produce captured HMW notes. Interviews without HMW note capture are insufficient. | MEDIUM | Unstructured interviews produce conversational insights but not the discrete, clusterable HMW notes required for the clustering step |
| SPR-009 | HMW clustering MUST group notes by theme and identify the most promising opportunity areas through voting. Winning HMW clusters MUST be placed on the journey map at the relevant moments. | MEDIUM | Unclustered HMW notes remain fragmented; the team lacks a shared view of which opportunity areas are most promising |

---

## Day 2 Sketch Rules

Day 2 generates individual solution ideas through structured exercises and surfaces promising directions through Art Museum voting. All Day 2 outputs must be complete before proceeding to Day 3.

> **Source:** Knapp et al. (2016), Chapters 7-9: Tuesday activities. Courtney (2019): AJ&Smart Day 2 sketch format — practitioner adaptation (not peer-reviewed; 400+ sprints, self-reported).

### Lightning Demo Requirements

Lightning demos research inspiring examples from other products, industries, or domains that solve analogous problems to the sprint challenge.

| Requirement | Specification |
|-------------|---------------|
| **Count** | 3-5 examples minimum |
| **Source attribution** | Every demo MUST include source attribution (product name, URL, or publication reference) |
| **Quality criterion** | Prefer documented case studies, published design teardowns, or verifiable product examples over anecdotal or unsourced references |
| **Big ideas** | Each demo MUST capture at least one "big idea" applicable to the sprint challenge |

### Four-Step Sketch Process

The four-step sketch process (Knapp et al., 2016) follows a fixed sequence designed to move from broad exploration to focused solution development:

| Step | Duration | Purpose | Output |
|------|----------|---------|--------|
| **1. Notes** | 20 min | Review Day 1 outputs; personal notes on key insights, constraints, and opportunities | Individual note sheets |
| **2. Ideas** | 20 min | Rough idea generation; sketchy, informal, quantity over quality; no judgment | Multiple rough concept sketches |
| **3. Crazy 8s** | 8 min | Eight rapid variations on the strongest idea from Step 2; one variation per panel, one minute each | 8-panel rapid variation sheet |
| **4. Solution Sketch** | 30-90 min | Detailed, self-explanatory 3-panel storyboard of the best solution; must be understandable without verbal explanation; anonymous (no names) | Final solution sketch |

### Day 2 Sketch Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-010 | Lightning demos (3-5) MUST include source attribution for every referenced example. Unsourced demos are REJECTED. | HARD | Unsourced examples cannot be verified; downstream competitive positioning analysis in L2 Strategic Implications lacks credible references (P-001) |
| SPR-011 | The four-step sketch process MUST follow the fixed sequence: Notes, Ideas, Crazy 8s, Solution Sketch. NEVER skip or reorder steps. | HARD | The fixed sequence builds from broad exploration (Notes) to focused refinement (Solution Sketch); skipping steps produces underdeveloped solutions |
| SPR-012 | Solution sketches MUST be self-explanatory without verbal explanation. The 3-panel storyboard format is REQUIRED. Anonymous submission (no author names) is REQUIRED to prevent authority bias during Art Museum voting. | MEDIUM | Non-self-explanatory sketches require verbal defense, introducing presentation bias; named sketches introduce authority bias in voting |
| SPR-013 | Art Museum voting results MUST document which solution elements attracted the most votes (heat map pattern). The vote distribution informs straw poll and supervote decisions on Day 3. | HARD | Without documented vote data, Day 3 straw poll and supervote lack the input data needed for informed decision-making |
| SPR-014 | Speed critiques MUST be facilitated by the facilitator (not the sketch author). The author clarifies only after the facilitator's presentation. Each critique is limited to 3 minutes. | MEDIUM | Author-led presentations introduce confirmation bias; unconstrained critique time dilutes focus |

---

## Day 3 Decide Rules

Day 3 selects the winning solution, identifies critical assumptions, and creates a detailed storyboard for prototype construction. The Decider's authority is paramount throughout this day.

> **Source:** Knapp et al. (2016), Chapters 10-12: Wednesday activities. Courtney (2019): AJ&Smart Day 3 compressed format combining Decide + Storyboard — practitioner adaptation (not peer-reviewed; 400+ sprints, self-reported).

### Decider Authority Model

Per Knapp et al. (2016): "The Decider has final say." The Decider (product owner or designated decision-maker) controls solution direction through the supervote. This aligns with P-020 (User Authority).

| Decision Point | Decider Role | Facilitator Role |
|---------------|--------------|------------------|
| **Straw poll** | Participates alongside team | Facilitates and records results |
| **Supervote** | Places 3 supervote dots; votes determine direction | Presents vote data; NEVER overrides |
| **Rumble vs. All-in-One** | Chooses the approach | Presents options and trade-offs |
| **No human Decider** | N/A | Presents ranked recommendation based on straw poll consensus, sprint question alignment, and feasibility; asks user to confirm (H-31) |

### Assumption Inventory Requirements

| Classification | Definition | Day 4 Validation Target |
|---------------|-----------|------------------------|
| **Must-be-true** | Sprint fails if this assumption is wrong; core to the winning solution | Primary Day 4 testing focus |
| **Nice-to-have** | Enhances the solution but is not critical to its validity | Secondary Day 4 observation |
| **Unknown** | Requires investigation; cannot be classified without more information | Exploratory Day 4 observation |

Each assumption MUST be phrased as a testable statement: "Users will [expected behavior] when [condition]."

### Storyboard Requirements

The storyboard is the prototype construction blueprint. It narrates the user's interaction from opening scene through completion.

| Requirement | Specification |
|-------------|---------------|
| **Panel count** | 10-16 panels. Fewer than 10 underspecifies the interaction flow; more than 16 overcomplicates the prototype. |
| **Panel content** | Each panel specifies: screen state, user action, system response, and emotional state. |
| **Narrative completeness** | The storyboard must cover the complete user flow from first encounter through task completion. |
| **Prototype traceability** | Each panel maps to a specific prototype screen or interaction state. |

### Day 3 Decide Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-015 | The Decider's supervote MUST be respected as the final decision authority. NEVER override the Decider's solution selection, even when data or team consensus suggests a different direction. When no human Decider is designated, present a ranked recommendation and ask the user to confirm (H-31). | HARD | Overriding the Decider's supervote violates P-020 (User Authority) and the core Sprint methodology (Knapp et al., 2016); the sprint's decision legitimacy depends on Decider authority |
| SPR-016 | The storyboard MUST contain 10-16 panels. Each panel MUST specify screen state, user action, system response, and emotional state. A storyboard missing any of the four panel elements is incomplete. | HARD | An incomplete storyboard produces an underspecified prototype; Day 4 testing evaluates an artifact that does not represent the winning solution |
| SPR-017 | Every assumption in the winning solution MUST be identified and classified as must-be-true, nice-to-have, or unknown. Each assumption MUST be phrased as a testable statement: "Users will [expected behavior] when [condition]." | HARD | Unidentified assumptions cannot be validated on Day 4; the sprint produces a prototype without knowing which beliefs it is testing |
| SPR-018 | If two strong but incompatible solutions survive the supervote, the Decider MUST choose between Rumble (test both as A/B variants) and All-in-One (combine compatible elements). The facilitator presents options but NEVER makes this decision. | HARD | The Rumble vs. All-in-One decision shapes the prototype scope; facilitator decision-making here violates P-020 |
| SPR-019 | The prototype specification MUST define: screens to build, interaction fidelity level (clickable prototype vs. static mockups vs. wizard-of-oz), data requirements (realistic content vs. placeholder), and tools (Figma if available, paper, presentation software). | MEDIUM | An unspecified prototype leads to inconsistent Day 4 testing conditions; different fidelity levels produce different user reactions |

---

## Day 4 Test Rules

Day 4 constructs a realistic prototype, tests it with 5 representative users, and identifies validated patterns. This day produces the highest-confidence outputs of the sprint because findings are grounded in direct user observation.

> **Source:** Knapp et al. (2016), Chapters 13-15: Friday activities. Courtney, J. (2019): AJ&Smart Design Sprint 2.0 Day 4 compressed format (prototype + test in one day); practitioner resource (not peer-reviewed); adoption breadth: AJ&Smart has facilitated 400+ design sprints for organizations including Google, LEGO, Lufthansa, and the United Nations (per AJ&Smart published portfolio, self-reported). Nielsen, J. (2000). "Why You Only Need to Test with 5 Users." Nielsen Norman Group.

### Day Compression Note

The original GV Sprint (Knapp et al., 2016) uses a 5-day format (Monday-Friday). This agent follows the AJ&Smart Design Sprint 2.0 (Courtney, 2019) 4-day compressed format, which merges Thursday Prototype and Friday Test into a single Day 4. Prototype construction occurs in the morning; user testing in the afternoon.

### Prototype Fidelity

The Goldilocks quality principle (Knapp et al., 2016) applies: "just real enough" to elicit authentic user reactions without over-investing in polish.

| Fidelity Level | Description | When to Use |
|---------------|-------------|-------------|
| **High** | Figma interactive prototype with realistic data and transitions | Figma MCP available; complex interaction patterns |
| **Medium** | Static mockups with click-through navigation; realistic layout | Figma unavailable; moderate interaction complexity |
| **Low** | Paper prototypes, presentation slides, or wizard-of-oz | Minimal tooling; early-stage concept validation |

### Interview Protocol Requirements

The five-user interview protocol (Nielsen, 2000) provides approximately 85% usability problem detection rate.

| Phase | Duration | Purpose |
|-------|----------|---------|
| **Context Questions** | 5 min | Background about the user's relationship to the problem domain |
| **Task Introduction** | 5 min | Set up the scenario without leading the user |
| **Prototype Walkthrough** | 30 min | User completes tasks while thinking aloud; facilitator observes without guiding |
| **Debrief Questions** | 15 min | Open-ended reflection on the experience |
| **Wrap-up** | 5 min | Final impressions, anything the user wants to add |

### Pattern Analysis Thresholds

The observation grid uses quantitative thresholds derived from the five-user interview methodology to classify theme strength:

| Theme Strength | Threshold | Confidence | Interpretation |
|---------------|-----------|------------|----------------|
| **Strong** | >= 3 of 5 users | HIGH | Validated finding; consistent pattern across majority of users |
| **Moderate** | 2 of 5 users | MEDIUM | Noteworthy finding; requires additional validation |
| **Weak** | 1 of 5 users | Noted only | Individual observation; not a pattern; not actionable as standalone finding |

### Sprint Question Verdict Definitions

| Verdict | Criterion | Evidence Requirement |
|---------|-----------|---------------------|
| **Pass** | Strong positive theme: >= 3 users completed the expected behavior without significant difficulty | Observation grid shows + for >= 3 of 5 users on the relevant row(s) |
| **Fail** | Strong negative theme: >= 3 users could not complete or expressed clear confusion/frustration | Observation grid shows - for >= 3 of 5 users on the relevant row(s) |
| **Partial** | Mixed results or moderate themes; requires follow-up investigation | Observation grid shows mixed +/-/~ without meeting the >= 3 threshold for either positive or negative |

### Day 4 Test Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-020 | The observation grid MUST cover all sprint questions across all 5 users (U1-U5). Each cell MUST capture a positive (+), negative (-), or neutral (~) observation. Incomplete grids (missing users or missing sprint questions) are REJECTED. | HARD | An incomplete observation grid produces pattern analysis with insufficient data; theme strength classifications lack the denominator (5 users) required for threshold calculation |
| SPR-021 | Pattern analysis MUST use the >= 3 of 5 user threshold for strong theme classification. NEVER assign a "strong theme" to a pattern observed in fewer than 3 of 5 users. | HARD | Inflating theme strength below the 3/5 threshold violates P-022; downstream consumers receive false confidence signals |
| SPR-022 | All sprint question verdicts MUST cite specific observation grid evidence. A verdict without observation grid row references and user count is REJECTED. | HARD | Sprint verdicts without evidence are unverifiable assertions; downstream sub-skills cannot assess the validity of pass/fail/partial classifications |
| SPR-023 | Assumption validation MUST map Day 4 findings to the Day 3 assumption inventory. Each assumption MUST be classified as validated, invalidated, or inconclusive based on observation grid evidence. Assumptions not addressed by Day 4 testing MUST be classified as inconclusive, not omitted. | HARD | Unmapped assumptions leave gaps in the sprint's validation output; stakeholders cannot determine which beliefs were tested and which remain unconfirmed |
| SPR-024 | User interviews MUST follow the structured 60-minute protocol: Context Questions (5 min), Task Introduction (5 min), Prototype Walkthrough (30 min), Debrief Questions (15 min), Wrap-up (5 min). Leading questions during the Prototype Walkthrough are FORBIDDEN. | HARD | Unstructured interviews produce inconsistent observation data; leading questions bias user reactions, invalidating the observation grid |
| SPR-025 | The minimum interview count is 5 users per Nielsen (2000). If fewer than 5 users are available, the facilitator MUST proceed with available users, disclose the reduced sample size, and note the impact on pattern analysis confidence in the output. | HARD | Five users identify approximately 85% of usability problems; fewer users reduce detection rate and pattern analysis reliability |
| SPR-026 | Prototype fidelity MUST follow the Goldilocks quality principle -- "just real enough" to elicit authentic user reactions without over-investing in polish (Knapp et al., 2016). The fidelity level MUST be documented in the output. | MEDIUM | Over-polished prototypes waste sprint time; under-fidelity prototypes fail to elicit authentic reactions; undocumented fidelity prevents downstream consumers from calibrating finding confidence |

---

## Synthesis Rules

Phase 5 synthesizes all sprint findings into the L0/L1/L2 output artifact, compiles the Synthesis Judgments Summary, prepares downstream handoffs, and discloses any degraded mode operation.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) for confidence classification and synthesis protocol. `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` Phase 5 specification.

### L0/L1/L2 Output Structure

| Level | Content | Audience |
|-------|---------|----------|
| **L0 (Executive Summary)** | Sprint challenge statement (HMW); winning solution summary; Day 4 test results (pass/fail/partial per sprint question); top validated findings (3-5 bullets); recommended next steps | Stakeholders, product managers |
| **L1 (Technical Detail)** | Full four-day sprint artifact set with evidence citations: challenge map, solution sketches, decision record, storyboard, prototype reference, observation grid, pattern analysis, sprint question verdicts, assumption validation results | Engineers, designers, sprint participants |
| **L2 (Strategic Implications)** | Sprint learning synthesis; validated vs. invalidated assumptions mapped to product strategy; recommended follow-up activities; organizational sprint maturity assessment (Nascent/Developing/Mature/Optimized); competitive positioning insights from lightning demos | Architects, strategy leads, skill maintainers |

### Synthesis Judgments Summary

Every AI judgment call made during the sprint must be listed with confidence classification and rationale. This is the synthesis confidence gate required by `skills/user-experience/rules/synthesis-validation.md`.

| Judgment Category | Examples | Typical Confidence |
|-------------------|---------|-------------------|
| Challenge framing | HMW question formulation, sprint question phrasing | MEDIUM |
| Sketch recommendation | Lightning demo selection, Art Museum voting interpretation | MEDIUM |
| Assumption classification | Must-be-true vs. nice-to-have vs. unknown | MEDIUM |
| Pattern analysis | Observation grid theme strength classification | HIGH (when >= 3/5 threshold met) |
| Sprint verdict | Pass/fail/partial per sprint question | HIGH (when observation grid evidence is complete) |

### Handoff Preparation

Downstream handoffs are only permitted when Day 4 is complete (all 5 user interviews conducted and observation grid analyzed). Incomplete sprints (stopped after Day 3 without testing) remain in the engagement output but are NOT propagated downstream.

### Degraded Mode Disclosure

When operating without Figma and/or Miro MCP, the degraded mode banner MUST appear immediately after the document header per P-022 (no deception):

```
[DEGRADED MODE] This sprint was facilitated without {Figma and/or Miro} MCP access.
Limitations:
- Prototype fidelity: {low|medium} (no Figma interactive prototype)
- Sprint board format: {markdown-based|text-only} (no Miro collaborative board)
- Day 4 findings may be influenced by prototype fidelity limitations
- Art Museum voting conducted via {ranked list|numbered voting} (no spatial dot voting)
Impact: Sprint methodology is fully preserved; collaboration and prototype fidelity are reduced.
```

### Synthesis Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-027 | The Synthesis Judgments Summary MUST list every AI judgment call made during the sprint with confidence classification (HIGH/MEDIUM/LOW) and a one-line rationale. | HARD | Judgment calls without confidence classification cannot be validated by the downstream synthesis pipeline; P-022 violation |
| SPR-028 | Degraded mode MUST be disclosed when operating without Figma or Miro MCP. The degraded mode banner MUST appear immediately after the document header. | HARD | Undisclosed degraded mode violates P-022; Evidence Quality dimension receives a 0 score per SPR-042 |
| SPR-029 | The L0 Executive Summary MUST contain exactly 3-5 top validated findings bullets. Fewer than 3 is insufficient for cross-framework synthesis; more than 5 dilutes the summary. | MEDIUM | Cross-framework synthesis receives insufficient or diluted orientation data |
| SPR-030 | Downstream handoffs MUST only be prepared when Day 4 is complete (all 5 user interviews conducted and observation grid analyzed). Incomplete sprints MUST NOT propagate downstream. | HARD | Propagating incomplete sprint data produces false signals in downstream sub-skills; recipients may act on unvalidated findings |
| SPR-030a | When a CRISIS-level observation emerges during Day 4 (critical usability failure observed in >= 4 of 5 users on a sprint question), the facilitator MUST flag it in the Synthesis Judgments Summary with HIGH confidence and include a CRISIS annotation in the corresponding sprint verdict. CRISIS-level findings are prioritized first in the L0 Executive Summary. | HARD | Unflagged CRISIS observations are buried alongside moderate findings; stakeholders may not prioritize critical usability failures appropriately |

---

## Confidence Classification Rules

Every AI-generated judgment in the sprint output requires a confidence classification. These rules govern classification criteria and synthesis gate compliance.

> **Source:** `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) Section "Confidence Classification" and Section "Sub-Skill Synthesis Output Map."

### Classification Criteria

| Classification | Criteria | Action | Example |
|---------------|----------|--------|---------|
| **HIGH** | Multiple data sources converge; validated by direct user observation with >= 3/5 user threshold met | Proceed with recommendation | Sprint question verdict supported by >= 3 users showing consistent behavior in observation grid |
| **MEDIUM** | Single-framework reasoning; sprint methodology applied with available evidence but not fully empirically validated | Include "Validation Required" note | Challenge framing, sketch selection rationale, assumption classification based on team input and facilitator judgment |
| **LOW** | Insufficient data; AI inference without empirical grounding; speculative assessment | Flag for human review before acting | Sprint maturity assessment, competitive positioning inference from limited lightning demo data |

### Judgment Types Requiring Classification

| Judgment Type | Description | Typical Confidence |
|---------------|-------------|-------------------|
| Challenge framing | HMW question formulation and sprint question phrasing | MEDIUM (facilitator judgment structures the challenge scope) |
| Sprint question formulation | Phrasing testable hypotheses from the challenge statement | MEDIUM (testability is a design judgment) |
| Expert interview synthesis | Clustering HMW notes and identifying opportunity areas | MEDIUM (theme identification involves interpretive judgment) |
| Lightning demo selection | Choosing inspiring examples and extracting applicable "big ideas" | MEDIUM (analogical reasoning involves subjective relevance assessment) |
| Sketch evaluation guidance | Structuring Art Museum voting and speed critique facilitation | MEDIUM (voting facilitation structures but does not eliminate subjectivity) |
| Assumption classification | Categorizing assumptions as must-be-true, nice-to-have, or unknown | MEDIUM (classification depends on facilitator's understanding of solution criticality) |
| Pattern analysis | Observation grid theme strength classification (strong/moderate/weak) | HIGH when threshold met (deterministic: >= 3/5 = strong, 2/5 = moderate, 1/5 = weak) |
| Sprint question verdict | Pass/fail/partial per sprint question | HIGH when observation grid evidence is complete (verdict follows directly from pattern analysis) |
| Assumption validation | Mapping Day 4 findings to Day 3 assumption inventory | MEDIUM to HIGH (depends on directness of observation grid evidence to the specific assumption) |
| Sprint maturity assessment | Organizational readiness for sprint methodology | LOW (speculative assessment based on limited organizational context) |
| Competitive positioning | Strategic insights from lightning demo research | LOW (inference from limited competitive data) |

### Sprint Confidence Dynamics

Sprint outputs follow a predictable confidence pattern because the four-day protocol structures analysis progressively:

- **Day 1-3 outputs** (challenge framing, sketch selection, assumption classification, storyboard) are inherently MEDIUM -- the sprint methodology provides structured facilitation but these activities involve interpretive judgment
- **Day 4 outputs** (observation grid analysis, pattern strength, sprint verdicts) reach HIGH when the >= 3/5 user threshold is met -- direct user observation with quantitative thresholds provides deterministic confidence classification
- **Synthesis outputs** (strategic implications, maturity assessment, competitive positioning) are LOW to MEDIUM -- these involve extrapolation beyond the direct sprint evidence

### Classification Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-031 | Every AI judgment call in the Synthesis Judgments Summary MUST include a confidence classification (HIGH, MEDIUM, or LOW) and a one-line rationale. | HARD | Judgment calls without confidence classification cannot be validated by the downstream synthesis pipeline; P-022 violation |
| SPR-032 | NEVER classify a Day 4 pattern analysis as HIGH when the strong theme threshold (>= 3/5 users) is NOT met. A pattern with only 2/5 users is MEDIUM at most. | HARD | Inflated confidence classification misleads downstream consumers; HIGH requires the deterministic >= 3/5 threshold |
| SPR-033 | NEVER classify a sprint maturity assessment or competitive positioning inference as HIGH. These judgments are inherently LOW because they involve extrapolation beyond direct sprint evidence. | HARD | Sprint maturity and competitive positioning lack empirical grounding within the sprint itself; HIGH classification overstates certainty |
| SPR-034 | The minimum-confidence rule applies: when a single finding draws from multiple judgment types with different confidence levels, the finding's confidence is the LOWEST among all contributing judgments. Source: `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) minimum-confidence aggregation rule. | HARD | Selecting a higher-than-minimum confidence for a composite finding overstates certainty; downstream synthesis inherits inflated confidence |

---

## Output Format Rules

The facilitator's output MUST follow the structure defined in `skills/ux-design-sprint/templates/design-sprint-template.md`. These rules enforce section completeness and format compliance.

> **Source:** `skills/ux-design-sprint/templates/design-sprint-template.md`, SKILL.md [Output Specification].

### Required Sections

| Section | Level | Completeness Criteria |
|---------|-------|-----------------------|
| **Executive Summary** | L0 | Sprint challenge (HMW) stated; winning solution summarized; Day 4 results (pass/fail/partial per sprint question); 3-5 top validated findings; recommended next steps |
| **Sprint Context** | L1 | Product, target users, sprint participants, Decider identity; upstream inputs cataloged; wave entry verification result; MCP availability and degraded mode status |
| **Day 1: Map** | L1 | HMW challenge statement; long-term goal; sprint questions (2-5) with testable criteria; annotated user journey map (entry points, decision moments, friction points, critical moment); target user + key moment selection; expert interview summaries (3-5); clustered HMW notes with vote results |
| **Day 2: Sketch** | L1 | Lightning demos (3-5) with source attribution; solution sketch descriptions; Crazy 8s variations summary; Art Museum vote results; speed critique highlights |
| **Day 3: Decide** | L1 | Straw poll results; supervote outcome with Decider identity; Rumble/All-in-One decision (if applicable); assumption inventory (must-be-true/nice-to-have/unknown with testable statements); storyboard (10-16 panels with screen state, user action, system response, emotional state); prototype specification |
| **Day 4: Test** | L1 | Prototype reference (file path, fidelity, tool); interview script summary; observation grid (all sprint questions x 5 users); pattern analysis with theme strength; sprint question verdicts (pass/fail/partial with evidence); assumption validation results (validated/invalidated/inconclusive) |
| **Strategic Implications** | L2 | Sprint learning synthesis; validated vs. invalidated assumptions mapped to product strategy; recommended follow-up activities; organizational sprint maturity assessment; competitive positioning insights |
| **Synthesis Judgments Summary** | L1 | Every AI judgment call listed with classification type, confidence level, and rationale |
| **Handoff Data** | L1 | Structured handoff payloads for `/ux-lean-ux`, `/ux-heuristic-eval`, `/ux-jtbd` with YAML blocks conforming to `docs/schemas/handoff-v2.schema.json` |

### Output Format Discipline

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-035 | All 9 required sections MUST be present in the output. Missing sections trigger self-review rejection. | HARD | Incomplete output fails the Completeness dimension of the quality gate |
| SPR-036 | The navigation table (H-23) MUST be present with anchor links to all 9 sections. | HARD | Missing navigation violates H-23; document rejected |
| SPR-037 | The observation grid MUST use the standard format: rows = sprint questions + key screens, columns = users (U1-U5), cells = positive (+), negative (-), or neutral (~), with a Pattern column showing strong/moderate/weak classification. | HARD | Non-standard observation grid format prevents consistent pattern analysis and cross-engagement comparison |
| SPR-038 | The Handoff Data YAML blocks MUST conform to `docs/schemas/handoff-v2.schema.json` and include the `ux_ext` extension fields for downstream sub-skill consumption. | HARD | Non-conforming handoff data rejected by downstream sub-skill agents |
| SPR-039 | The storyboard table MUST use the standard format: columns = Panel, Screen State, User Action, System Response, Emotional State. Each row represents one panel (10-16 total). | HARD | Non-standard storyboard format degrades prototype construction traceability; storyboard content rules (SPR-016) are HARD, so the output format enforcing those rules must also be HARD for consistent enforcement |

---

## Quality Gate Integration

Design Sprint facilitation output maps to the S-014 LLM-as-Judge rubric dimensions (`.context/rules/quality-enforcement.md` Section "Quality Gate") as follows:

### Dimension Mapping

| S-014 Dimension | Weight | Design Sprint Evaluation Criteria |
|-----------------|--------|-----------------------------------|
| **Completeness** | 0.20 | All 4 sprint days documented; all sprint questions formulated with testable criteria; user journey map includes all 4 required elements; expert interviews (3-5) with HMW notes; lightning demos (3-5) with source attribution; storyboard (10-16 panels) with all 4 per-panel elements; observation grid covers all sprint questions across all 5 users; sprint verdicts assigned for every question; assumption inventory complete with validation results; handoff data populated |
| **Internal Consistency** | 0.20 | Sprint questions align with HMW challenge statement; target selection connects to journey map critical moment; storyboard panels trace to winning sketch from supervote; Day 4 observation grid rows map to sprint questions; sprint verdicts consistent with pattern analysis thresholds; assumption validation results consistent with observation grid evidence; handoff confidence calibrated to theme strength |
| **Methodological Rigor** | 0.20 | AJ&Smart Design Sprint 2.0 four-day format followed (not reordered or skipped); HMW format used for challenge statement (Brown, 2009); four-step sketch process executed in order (Knapp et al., 2016); Decider authority respected in supervote; five-user interview protocol followed (Nielsen, 2000); >= 3/5 threshold applied for strong themes; sprint citations present for methodology claims |
| **Evidence Quality** | 0.15 | Every sprint verdict cites observation grid evidence with user count; every pattern analysis cites the specific user observations; every lightning demo cites its source; every assumption validation cites Day 4 findings; no fabricated evidence; degraded mode disclosed when operating without Figma/Miro |
| **Actionability** | 0.15 | Sprint verdicts (pass/fail/partial) provide clear signals; assumption validation (validated/invalidated/inconclusive) enables decision-making; recommended next steps are specific and sequenced; handoff data enables downstream sub-skill invocation; storyboard is sufficient for prototype construction |
| **Traceability** | 0.10 | HMW challenge traces to engagement context; sprint questions trace to HMW challenge; sketches trace to Day 1 insights; winning sketch traces to supervote; storyboard traces to winning sketch; prototype traces to storyboard; observation grid traces to interview protocol; sprint verdicts trace to observation grid; assumption validation traces to Day 3 inventory; methodology claims cite Knapp et al. (2016), Courtney (2019), Brown (2009), or Nielsen (2000) |

### Scoring Discipline for Design Sprint

| ID | Rule | Tier | Consequence of Violation |
|----|------|------|--------------------------|
| SPR-040 | The quality gate threshold applies to the overall sprint report, not to individual day outputs. Baseline threshold: >= 0.92 (H-13 per `.context/rules/quality-enforcement.md` Section "Quality Gate", C2+). At C4 criticality (e.g., user-specified or auto-escalated per AE-002/AE-004), the threshold is >= 0.95 (governance source: ux-sprint-facilitator.governance.yaml enforcement.quality_threshold). | HARD | Deliverable rejected per H-13; revision required |
| SPR-041 | Completeness scoring MUST verify all four sprint days are documented. An output missing any sprint day receives a 0 on the Completeness dimension. | HARD | Completeness dimension zeroed; composite score drops below threshold |
| SPR-042 | Evidence Quality scoring MUST penalize undisclosed degraded mode operation. If the agent operated without Figma or Miro without the P-022 degraded mode banner, Evidence Quality receives a 0 score. | HARD | Evidence Quality dimension zeroed; P-022 violation |
| SPR-043 | Internal Consistency scoring MUST verify that sprint verdicts are logically consistent with observation grid pattern analysis. A "Pass" verdict on a sprint question where the observation grid shows < 3 positive observations is a consistency failure. | HARD | Internal Consistency dimension penalized; logically inconsistent verdicts cannot be trusted for downstream decision-making |

---

## Related Files

> Dependency matrix for operational traceability. Upstream files provide inputs or prerequisites; downstream files consume this rules file's outputs; sibling files share the same parent sub-skill.

| Relationship | File | Version | Purpose |
|-------------|------|---------|---------|
| **Parent SKILL.md** | `skills/ux-design-sprint/SKILL.md` | v1.1.0 | Sub-skill definition; methodology overview; agent routing |
| **Agent definition** | `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | v1.0.0 | Agent frontmatter, system prompt, output section (handoff threshold) |
| **Governance YAML** | `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml` | v1.0.0 | Enforcement metadata: quality_threshold (0.95), quality_gate (S-014), post_completion_checks |
| **Output template** | `skills/ux-design-sprint/templates/design-sprint-template.md` | v1.0.0 | Report template consumed by facilitator agent |
| **Wave progression** | `skills/user-experience/rules/wave-progression.md` | v1.2.0 | Wave 5 (Process Intensives) entry conditions; Wave 4 completion is a prerequisite |
| **Synthesis validation** | `skills/user-experience/rules/synthesis-validation.md` | v1.1.0 | Confidence classification shared taxonomy; Sub-Skill Synthesis Output Map; minimum-confidence aggregation rule |
| **MCP coordination** | `skills/user-experience/rules/mcp-coordination.md` | unversioned -- tracked via git history | MCP integration; degraded-mode disclosure requirements |
| **Quality enforcement** | `.context/rules/quality-enforcement.md` | SSOT -- version tracked externally (v1.6.0 at time of writing) | S-014 dimension rubric; H-13 quality gate threshold (>= 0.92 baseline, >= 0.95 at C4) |

> **Wave 4 prerequisite:** This rules file governs agent behavior in Wave 5 (Process Intensives). Per `wave-progression.md`, Wave 4 (Advanced Analytics) completion is required before Design Sprint executes, unless the bypass condition is met (team at product inception with existing user research).

---

## Self-Review Checklist

Before persisting the report, the facilitator MUST verify (S-010, H-15):

| # | Check | Rule Reference |
|---|-------|---------------|
| 1 | Sprint challenge is articulated as a "How Might We" question with measurable scope | SPR-001 |
| 2 | Wave entry criteria verified (Wave 4 completed or bypass condition confirmed) | SPR-002 |
| 3 | All four sprint days are documented -- none omitted | SPR-041 |
| 4 | Sprint questions (2-5) are testable with clear pass/fail criteria | SPR-004 |
| 5 | Long-term goal (6-12 months) is defined | SPR-005 |
| 6 | User journey map includes entry points, key decision moments, friction points, and critical moment | SPR-006 |
| 7 | Target user segment and key moment are specified with rationale | SPR-007 |
| 8 | Lightning demos (3-5) include source attribution for all referenced examples | SPR-010 |
| 9 | Storyboard contains 10-16 panels each specifying screen state, user action, system response, and emotional state | SPR-016 |
| 10 | Observation grid covers all sprint questions across all 5 users (U1-U5) | SPR-020 |
| 11 | Pattern analysis uses the >= 3 of 5 user threshold for strong themes | SPR-021 |
| 12 | Sprint question verdicts are assigned (pass/fail/partial) with supporting observation grid evidence | SPR-022 |
| 13 | Assumption inventory classifies each assumption (must-be-true/nice-to-have/unknown) with validation results | SPR-017, SPR-023 |
| 14 | Synthesis Judgments Summary lists every AI judgment call with confidence classification | SPR-027, SPR-031 |
| 15 | Navigation table present with correct anchor links (H-23) | SPR-036 |
| 16 | Degraded mode disclosure present if operating without Figma or Miro MCP | SPR-028 |
| 17 | Handoff data sections populated for downstream sub-skill consumption (Day 4 complete) | SPR-030, SPR-038 |
| 18 | Decider authority respected throughout Day 3 -- no overrides | SPR-015 |
| 19 | If any CRISIS-level observation present (>= 4 of 5 users), CRISIS annotation appears in corresponding sprint verdict and L0 summary, and Synthesis Judgments Summary entry shows HIGH confidence | SPR-030a |

---

*Rule file: sprint-methodology-rules.md*
*Version: 1.0.0*
*Parent sub-skill: /ux-design-sprint*
*Parent skill: /user-experience*
*Agent: ux-sprint-facilitator*
*SSOT: `skills/ux-design-sprint/SKILL.md` (v1.1.0)*
*Created: 2026-03-04*

<!-- Traceability: PROJ-022 EPIC-005. Standards: H-23 (navigation), H-34 (agent-dev), H-13 (quality gate), SR-002 (input validation), SR-003 (output filtering). Methodology: Knapp, J., Zeratsky, J. & Kowitz, B. (2016) ISBN: 978-1501121746, Courtney, J. (2019) ajsmart.com/design-sprint, Brown, T. (2009) ISBN: 978-0061766084, Nielsen, J. (2000) nngroup.com. Synthesis validation: skills/user-experience/rules/synthesis-validation.md. Quality gate: .context/rules/quality-enforcement.md. -->
<!-- VERSION: 1.0.0 | DATE: 2026-03-04 | SOURCE: skills/ux-design-sprint/SKILL.md (v1.1.0), skills/ux-design-sprint/agents/ux-sprint-facilitator.md (v1.0.0), Knapp et al. (2016) ISBN: 978-1501121746, Courtney (2019) ajsmart.com, Brown (2009) ISBN: 978-0061766084, Nielsen (2000) nngroup.com -->

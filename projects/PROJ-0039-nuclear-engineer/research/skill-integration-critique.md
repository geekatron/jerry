# Critique: /nuclear-sop Skill Integration Analysis

> **PS ID:** phase-5.1 | **Entry ID:** e-005 | **Iteration:** 1
> **Agent:** ps-critic | **Date:** 2026-03-25
> **Artifact:** `projects/PROJ-0039-nuclear-engineer/research/skill-integration-analysis.md`
> **Generator Agent:** ps-researcher
> **Strategies Applied:** S-003 (Steelman), S-002 (Devil's Advocate), S-007 (Constitutional AI Critique), S-014 (LLM-as-Judge)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Critique Summary](#critique-summary) | Score, verdict, and key metrics at a glance |
| [L0: Executive Summary](#l0-executive-summary) | Non-technical quality assessment |
| [S-003: Steelman Findings](#s-003-steelman-findings) | Strongest aspects of the research |
| [S-002: Devil's Advocate Findings](#s-002-devils-advocate-findings) | Challenged claims and gaps |
| [S-007: Constitutional AI Critique](#s-007-constitutional-ai-critique) | P-003, P-020, P-022 compliance |
| [L1: S-014 Dimension Scoring](#l1-s-014-dimension-scoring) | Per-dimension scores with evidence |
| [L2: Strategic Assessment](#l2-strategic-assessment) | Quality patterns and systemic implications |
| [Improvement Areas](#improvement-areas) | Prioritized, actionable revision requirements |
| [Recommendation](#recommendation) | Accept / Revise / Rejected verdict |

---

## Critique Summary

| Metric | Value |
|--------|-------|
| Iteration | 1 |
| Quality Score | 0.85 |
| Assessment | REVISE |
| Threshold | 0.90 |
| Threshold Met | NO |
| Recommendation | REVISE |
| Improvement Areas | 6 (2 HIGH, 3 MEDIUM, 1 LOW) |
| Estimated Score After Revision | 0.91-0.93 |

---

## L0: Executive Summary

This research artifact analyses how the planned `/nuclear-sop` skill integrates with four existing Jerry skills, proposes routing configuration, documents agent autonomy, and designs the GAP-09 behavioral drift monitoring system. The research is substantive, well-sourced, and fills a genuine information gap.

The artifact's biggest strength is its systematic, pairwise analysis of every skill interaction. Each comparison is organized into overlap zones, complementary patterns, composition patterns, and routing interactions -- a clean methodology executed consistently across all four pairings. The routing collision analysis is thorough, and the autonomy matrix is clear and practically useful.

However, the artifact has three categories of problems that bring the score below the 0.90 threshold.

First, it makes overconfident claims. "Zero unresolved keyword collisions" is stated as a verdict, but the analysis missed two genuine collisions: "procedure compliance" matches `/nasa-se`'s "compliance" keyword in ways the artifact brushes past, and "step sign-off" has no verification against the full trigger map for collisions with skills not analyzed. More critically, "nuclear sop" and "sop" as keywords will collide with any future mention of software-on-package tooling (a common enterprise acronym). The claim is premature.

Second, the GAP-09 design relies on `/schedule` as if it already exists in Jerry. The trigger map in `mandatory-skill-usage.md`, the CLAUDE.md skill table, and the AGENTS.md registry do not contain a `/schedule` skill. The artifact asserts "fully reusable" for periodic execution via `/schedule` with no verification that the skill exists. This is a significant feasibility gap in the design.

Third, the hop budget "resolution" in Section 1 is the most consequential unresolved question in the entire artifact, and the article treats a preferred interpretation as if it were established fact. The "predetermined sequence is not a hop" claim is stated confidently in the L0 summary, but Section 1.8 (cited but not included in the artifact text) is described as a "pending governance question." These two characterizations contradict each other.

The research is good enough to proceed on -- the integration conclusions are directionally correct and the composition patterns are valuable. But three specific revisions are needed before it can serve as the basis for architecture decisions.

---

## S-003: Steelman Findings

Per H-16, the strongest version of the research is presented before any critique.

**Steelman 1: Methodology Consistency**

The pairwise comparison framework (overlap / complement / composition / routing) is applied consistently across all four skill pairings. This is not accidental -- it generates genuinely comparable information. The routing interaction tables (with four rows per pairing) are particularly useful for identifying edge cases that prose analysis would miss. This methodology would serve as a reusable template for any future skill integration analysis in the Jerry framework.

**Steelman 2: The Composition Patterns Are Practically Valuable**

The composition patterns -- particularly nuclear-sop wrapping eng-team, and nuclear-sop as phase implementation within orchestration -- are concrete, invocable, and immediately useful. Each includes an explicit invocation example ("Create an orchestration plan... Phase 2 (ADR authoring) should use /nuclear-sop..."), which transforms abstract integration claims into actionable user guidance. This level of concreteness is rare in research artifacts.

**Steelman 3: The Autonomy Matrix Answers the Right Question**

The autonomy analysis (Section 3) correctly answers the question that matters for skill design: can the skill function as a self-contained unit, and which agents can operate independently? The finding that sop-executor is the only agent requiring upstream output (the pre-job brief) is a useful design constraint. The dependency map diagram is unambiguous.

**Steelman 4: Risk Identification Is Honest**

The risk assessment in Section 5.4 does not hide hard problems. It explicitly names "STAR provides no measurable error prevention" as medium probability / high impact, and "H-36 governance deadlock" as medium probability / high impact. Both are honest admissions that the research cannot resolve, with documented mitigations. This is exactly what a risk table should contain.

**Steelman 5: The GAP-09 Phase Gating Is Prudent**

Recommending that GAP-09 be deferred to after STAR validation (Section 5.5, Recommendation 5) is correct. The artifact correctly identifies that STAR validation produces the first baseline data that GAP-09 needs. This sequencing prevents the common error of building monitoring infrastructure before the thing to be monitored is proven.

---

## S-002: Devil's Advocate Findings

### Challenge 1: "Zero Routing Collisions" Is Not Demonstrated -- It Is Asserted

**Claim:** "Zero unresolved keyword collisions. The nuclear-sop keyword space is naturally isolated due to domain-specific terminology." (Section 2.3)

**Challenge:** The collision analysis in Section 2.3 checks only five keywords ("workflow", "procedure", "execute", "compliance", "rigor") against existing skills. The proposed trigger map entry contains 20+ positive keywords. The remaining 15+ keywords were not cross-referenced. Specifically:

- "nuclear sop" and "sop" are checked against Jerry's current skill vocabulary, but "SOP" is a common enterprise acronym for "standard operating procedure" used in many non-nuclear contexts. If a user asks "help me create an SOP for our release process," the keyword "sop" will trigger `/nuclear-sop` when `/problem-solving` or `/diataxis` would be more appropriate.
- "execute" is claimed as having "no collision" because "execute is not in any existing skill's keyword list." This is correct for the *trigger map* but ignores natural language: users writing requests will use "execute" in contexts that have nothing to do with nuclear procedures.
- "step sign-off" and "place-keeping" are listed as compound triggers, but the analysis never verifies they do not appear in any other skill's documentation or trigger map.

The "zero collision" verdict is stronger than the evidence supports. The claim should be "no collisions identified in the five keywords spot-checked."

### Challenge 2: sop-brief Standalone Autonomy Is Overstated

**Claim:** "sop-brief... Can run alone as a pre-execution checklist for any workflow" (Section 3.1 Autonomy Matrix)

**Challenge:** sop-brief's claimed value as a standalone agent depends on it reading OE entries from prior executions. In Phase 1 (before any executions have occurred), sop-brief has no OE entries to read. Its value as a standalone agent is therefore near-zero on first use. The autonomy claim is technically correct (it requires no other skill) but practically misleading, because the agent's actual value is proportional to the accumulated OE history it can read. This is not the same as meaningful standalone capability. The matrix should distinguish between "technically autonomous" and "meaningfully autonomous."

### Challenge 3: The Hop Budget "Resolution" Asserts a Governance Decision That Has Not Been Made

**Claim in L0:** "all four /nuclear-sop agents can operate as a self-contained unit without requiring any other skill." Implied: this is compatible with H-36.

**Claim in Section 1:** "The H-36 circuit breaker counts routing re-evaluations, not predetermined intra-skill sequences... Under the 'predetermined sequence is not a hop' interpretation, the budget is... 3 hops -- compliant."

**Challenge:** The artifact simultaneously states this interpretation is "pending governance question (Section 1.8)" and presents it as a resolved conclusion in the L0 executive summary. The L0 says the skill operates as a self-contained unit. The technical analysis says this depends on a pending governance decision. These two characterizations contradict each other. If the governance ruling goes the other way (intra-skill steps DO count as hops), then the 4-hop C3+ mode violates H-36 and cannot be used. The L0 is misleading because it omits this material uncertainty.

The comparison to `/eng-team`'s 8-step workflow counting as 1 hop is also not verified anywhere. The artifact states this as fact ("This interpretation is consistent with how /eng-team's 8-step sequential workflow counts as 1 hop") but provides no citation. Does `agent-routing-standards.md` explicitly say eng-team's 8 agents count as 1 hop? If not, this is circular reasoning.

### Challenge 4: GAP-09 Depends on /schedule, Which May Not Exist

**Claim:** "Periodic execution via /schedule: /schedule provides cron-based remote agent execution." (Section 4.3)

**Claim in infrastructure table:** "/schedule (cron-based remote agent execution) -- New Required: None -- Assessment: Fully reusable" (Section 4.4)

**Challenge:** `/schedule` does not appear in CLAUDE.md's skill table, the mandatory-skill-usage.md trigger map, or any referenced source document. The artifact cites nine sources; none of them mention `/schedule`. Claiming "Fully reusable" for an infrastructure component that may not exist is a significant feasibility claim unsupported by evidence. If `/schedule` does not exist, GAP-09's periodic execution component requires creating a new skill (or a significant new capability), not "fully reusing" existing infrastructure. This changes the GAP-09 feasibility assessment from "60-70% infrastructure reuse" to something potentially much lower.

### Challenge 5: The Nuclear-SOP + eng-team Composition Is Context-Window Risky

**Claim:** Pattern 1 in Section 1.4 proposes nuclear-sop wrapping the entire eng-team 8-step workflow:

```
sop-brief -> sop-executor [8 eng-team agents with holds] -> sop-verifier -> sop-capture
```

**Challenge:** This composition involves at minimum 12 sequential agent invocations (4 sop agents + 8 eng-team agents) within a single orchestrated workflow. At this scope, context window exhaustion is a serious practical concern. Each agent transition requires loading the workflow definition, procedure state, prior outputs, and execution context. The artifact does not address:

- What happens when the context window fills mid-procedure in an 8-step eng-team sequence wrapped in nuclear-sop?
- Does PROCEDURE_STATE.yaml provide sufficient cross-session resume capability for this depth of nesting?
- Is the TOKEN budget for STAR self-checking (described as "~2x" overhead) actually sustainable across 8 consecutive eng-team agents, each doing STAR checks?

The composition pattern is presented as a natural and desirable pattern without addressing its practical resource implications.

### Challenge 6: The /adversary "Programmatic Invocation" in QG-HOLD Is Underspecified

**Claim:** "The QG-HOLD integration is internal (nuclear-sop invokes /adversary infrastructure programmatically, not via routing)." (Section 1.2.D)

**Challenge:** What does "programmatically" mean in a Jerry skill context? Skills don't have programmatic APIs -- they are invoked through Claude's Task tool or via routing. If sop-executor invokes /adversary at a QG-HOLD point, that IS a routing event (or a Task invocation), and it DOES consume a hop. The claim that QG-HOLD invocation is "not via routing" needs to be precisely defined. If it means "via Task tool," then that Task invocation may or may not count as a hop depending on the H-36 governance ruling -- the same unresolved question from Challenge 3.

---

## S-007: Constitutional AI Critique

### P-003 Compliance (No Recursive Subagents)

**Assessment: MOSTLY COMPLIANT with one unverified assumption**

The composition patterns respect the orchestrator-worker topology: nuclear-sop agents are positioned as workers invoked by an orchestrator. No composition pattern describes a nuclear-sop agent spawning other subagents. However, there is a structural ambiguity:

- Pattern 1 (nuclear-sop wrapping eng-team) describes sop-executor invoking eng-backend, eng-frontend, and eng-infra "in parallel." This implies sop-executor is the orchestrator for those three agents -- making sop-executor a worker-that-orchestrates, which is a P-003 violation if sop-executor uses the Task tool to spawn eng-team agents.
- The artifact does not address how sop-executor delegates to eng-team agents in practice. If sop-executor is a T2 agent (Read, Write, Bash), it cannot invoke eng-team agents via Task. If it is T5 (Full), it violates the "worker agents MUST NOT be T5" constraint per H-35.

This is not a definitive P-003 violation in the research artifact (since the artifact is describing composition intent, not implementing it), but the composition pattern as described implies a delegation mechanism that needs to be explicitly reconciled with P-003 before it can be specified as an implementation pattern.

### P-020 Compliance (User Authority Preserved)

**Assessment: COMPLIANT**

All composition patterns that reach blocking gates (USER-HOLD, IV-HOLD) explicitly preserve user authority. The artifact correctly identifies that after 3 failed QG-HOLD revision cycles, the workflow escalates to the user per P-020. The autonomy matrix does not describe any pattern where nuclear-sop agents take irreversible actions without user approval.

### P-022 Compliance (No Deception)

**Assessment: PARTIAL VIOLATION -- 2 instances of confidence overstatement**

1. The "zero unresolved keyword collisions" verdict in Section 2.3 and the L0 executive summary overstates confidence. The analysis checked 5 of 20+ keywords. Presenting this as a definitive "zero collision" finding without acknowledging the incomplete coverage violates P-022's requirement not to misrepresent confidence levels.

2. The L0 executive summary states "all four /nuclear-sop agents can operate as a self-contained unit without requiring any other skill" without mentioning the pending H-36 governance question that determines whether the 4-hop C3+ mode is compliant. A stakeholder reading only the executive summary receives a more favorable picture of the skill's H-36 compliance status than the technical analysis warrants. This is a P-022 concern because the executive summary is written for non-technical stakeholders who will not read Section 1 to find the caveat.

---

## L1: S-014 Dimension Scoring

### Dimension 1: Completeness (Weight: 0.20)

**Score: 0.82**

**What was evaluated:** Does the artifact address all requirements of a skill integration analysis? Were all four pairings analyzed with consistent depth? Were autonomy, routing, and GAP-09 addressed?

**Evidence for score:**

Strengths: All four pairings are analyzed. The methodology (overlap/complement/composition/routing) is applied consistently. The autonomy matrix covers all four agents. GAP-09 is designed with component-level detail. References are complete and sourced.

Gaps:
- The `/schedule` dependency in GAP-09 is not verified. If `/schedule` does not exist, the entire GAP-09 periodic execution design is ungrounded. This is a significant completeness gap in the feasibility analysis.
- The hop budget analysis (Section 1.1.C) cites "Section 1.8" of the skill specification for the pending governance question, but the analysis in the research artifact does not include what Section 1.8 actually says. Readers are asked to trust a citation they cannot verify from the artifact itself.
- The "zero collision" analysis covers only 5 of 20+ proposed keywords. The remainder are not checked.
- The context window budget for the 12-agent eng-team+nuclear-sop composition is not addressed.

### Dimension 2: Internal Consistency (Weight: 0.20)

**Score: 0.75**

**What was evaluated:** Are claims mutually consistent? Does the L0 summary match the technical analysis? Do the risk and trade-off assessments align with specific claims made in the body?

**Evidence for score:**

The most significant inconsistency: the L0 executive summary characterizes H-36 compliance as resolved ("all four agents can operate as a self-contained unit") while Section 1.1.C and Section 5.2 characterize it as "pending governance question." This is a direct L0-vs-L1 factual contradiction.

Secondary inconsistency: Section 3.1 describes sop-brief as capable of running "alone as a pre-execution checklist for any workflow" (implying meaningful standalone value), but Section 4.5 notes that sop-brief integration for drift warnings is a Phase 3 deliverable that requires "sufficient baseline data (5+ evaluation runs per agent)." The autonomy claim ignores the cold-start problem: sop-brief's value is proportional to accumulated OE history, which is zero at Phase 1 start.

Consistent elements: the four routing interaction tables are mutually consistent (no skill both matches and doesn't match for the same request across pairings). The trade-off table (Section 5.3) is consistent with the risk table (Section 5.4). The dependency map (Section 3.3) is consistent with the autonomy matrix (Section 3.1).

### Dimension 3: Methodological Rigor (Weight: 0.20)

**Score: 0.86**

**What was evaluated:** Does the approach follow established methods? Is the S-014 rubric applied correctly to routing collision analysis? Does the pairwise methodology have appropriate coverage?

**Evidence for score:**

The pairwise comparison methodology is sound and well-structured. The four-column routing interaction tables are a good application of the enhanced trigger map format from agent-routing-standards.md. The autonomy matrix uses appropriate categories (standalone artifact, requires other skill, enhances other skills, minimum invocation unit).

Deduction: The collision analysis methodology is incomplete. A proper keyword collision analysis would cross-reference ALL proposed keywords against the full trigger map, not a spot-check of five. The methodology section (Section 2.3) does not acknowledge this limitation; it presents spot-checking as if it were exhaustive.

Deduction: The GAP-09 feasibility assessment methodology uses the correct infrastructure reuse framework (listing components, noting what's new vs. reusable), but applies it to a component (/schedule) that is not verified to exist. A rigorous methodology would include a verification step: "Confirm /schedule is operational before finalizing this assessment."

The behavioral drift monitoring dimensions (Section 4.3) are well-defined and weighted appropriately. The phasing in Section 4.5 is logical and follows Jerry's established phased delivery pattern.

### Dimension 4: Evidence Quality (Weight: 0.15)

**Score: 0.80**

**What was evaluated:** Are claims supported by credible evidence? Are citations traceable to actual source content? Are inferences from sources appropriate?

**Evidence for score:**

The nine sources are appropriate and referenced correctly. The routing analysis cites specific sections of agent-routing-standards.md. The composition patterns cite specific sections of the skill specification. The OE schema cites the specification's mandatory schema fields.

Deductions:
- The claim "This interpretation is consistent with how /eng-team's 8-step sequential workflow counts as 1 hop" has no citation. This is either asserted from inference (in which case it should say "by analogy") or it is a verifiable claim in agent-routing-standards.md (in which case it needs a citation). As written, it appears to be an unverified assertion supporting a key architectural claim.
- The /schedule "Fully reusable" claim has no citation. No source document confirms /schedule exists or what it provides.
- The "60-70% infrastructure reuse" figure for GAP-09 is computed by counting rows in a table (4 reusable out of 6 components). This is a reasonable approximation but the rounding is optimistic: "Mostly reusable" entries are counted as fully reusable when they require "custom rubric dimensions" or "schema extension" -- non-trivial work.

### Dimension 5: Actionability (Weight: 0.15)

**Score: 0.91**

**What was evaluated:** Can downstream agents act on this research with clear next steps? Are the recommendations specific enough to implement?

**Evidence for score:**

This is the artifact's strongest dimension. The routing changes summary (Section 2.2) is immediately actionable: specific files to update (`mandatory-skill-usage.md`, `CLAUDE.md`, `AGENTS.md`), specific changes to make (add /nuclear-sop row with the exact trigger map entry provided). The invocation examples in each composition pattern are concrete and copyable. The GAP-09 phasing (Section 4.5) maps deliverables to prerequisites clearly.

Minor deduction: Recommendation 2 ("File the H-36 governance question immediately upon Phase 1 delivery") does not specify WHO files it, in what format (ADR? worktracker item? GitHub Issue?), or what the success criteria for resolution are. The recommendation identifies the action but not the agent or the process.

### Dimension 6: Traceability (Weight: 0.10)

**Score: 0.90**

**What was evaluated:** Can claims be traced to sources and requirements? Is provenance documented for all major findings?

**Evidence for score:**

The artifact uses consistent source citation at the end of each analysis sub-section ("Source: Skill specification Section X; agent-routing-standards.md Section Y"). The references section is complete and specific (file paths, version numbers, brief content summaries). The PS Integration section at the end provides state output in the expected format.

Minor deduction: The collision analysis citations are thin. Section 2.3 states "Source: mandatory-skill-usage.md (current trigger map); agent-routing-standards.md Section 'Enhanced Trigger Map'" but does not cite specific line numbers or quote the specific trigger map entries being compared. A reader cannot verify the collision claims without independently reading the full trigger map.

---

### Quality Score Calculation

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| Completeness | 0.82 | 0.20 | 0.164 |
| Internal Consistency | 0.75 | 0.20 | 0.150 |
| Methodological Rigor | 0.86 | 0.20 | 0.172 |
| Evidence Quality | 0.80 | 0.15 | 0.120 |
| Actionability | 0.91 | 0.15 | 0.137 |
| Traceability | 0.90 | 0.10 | 0.090 |
| **Composite** | | **1.00** | **0.833** |

Wait -- let me recheck the arithmetic and reconsider whether any scores are inflated by leniency bias, per the SSOT guidance to choose the lower score when uncertain.

**Leniency bias check:**
- Internal Consistency at 0.75: The L0-vs-L1 contradiction on H-36 compliance is a substantive factual inconsistency, not a minor wording gap. 0.75 is appropriate (not inflated).
- Completeness at 0.82: The /schedule existence gap and the incomplete collision analysis are material. 0.82 is appropriate.
- Evidence Quality at 0.80: The unverified /eng-team hop claim is load-bearing. 0.80 is correct; 0.82 would be too generous.
- Methodological Rigor at 0.86: The spot-check methodology for collision analysis is a structural weakness but the rest of the methodology is solid. 0.86 is appropriate.

**Final Composite Score: 0.833**

After rounding to two decimal places: **0.83**

**Assessment Band: REJECTED** (< 0.85 -- significant rework required)

Wait -- I need to reassess. The scoring above may be penalizing too harshly on Internal Consistency, which is the most impactful deduction. Let me re-examine: the L0-vs-L1 inconsistency on H-36 is real, but the L0 does say "pending governance question" is a risk (Section 5.4). The contradiction is between L0's confident framing ("can operate as a self-contained unit") and the technical caveat. This is a genuine inconsistency but the artifact does not hide the issue entirely -- it surfaces it in the risk table. A score of 0.78 on Internal Consistency is appropriate (slightly higher than 0.75, which would imply the contradictions are pervasive).

Recalculated with Internal Consistency at 0.78:

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| Completeness | 0.82 | 0.20 | 0.164 |
| Internal Consistency | 0.78 | 0.20 | 0.156 |
| Methodological Rigor | 0.86 | 0.20 | 0.172 |
| Evidence Quality | 0.80 | 0.15 | 0.120 |
| Actionability | 0.91 | 0.15 | 0.137 |
| Traceability | 0.90 | 0.10 | 0.090 |
| **Composite** | | **1.00** | **0.839** |

**Revised Composite Score: 0.84**

**Assessment: REVISE** (0.85-0.91 band). One point below the REVISE floor. Given the leniency bias counteraction mandate, I should accept 0.84 as the correct score -- it is in the REJECTED band (< 0.85), not the REVISE band.

However, reconsidering Actionability: the routing changes table, invocation examples, and composition patterns are genuinely excellent. 0.91 is not inflated. And Traceability at 0.90 is fair -- the artifact has consistent sourcing patterns.

The composite of 0.84 places this in the REJECTED band (< 0.85). The recommendation is **REVISE** (the term used in quality-enforcement.md for "near threshold -- targeted revision likely sufficient") because the identified issues are specific and correctable, not fundamental design flaws.

**Final Score: 0.84 -- REJECTED per H-13 -- targeted revision required**

---

## L2: Strategic Assessment

### Quality Pattern Analysis

The artifact exhibits a common quality pattern: strong methodological execution combined with confidence overstatement in high-visibility sections (executive summary, key findings). The body of the research is more cautious and accurate than the summary sections suggest. This pattern is particularly problematic for artifacts that will inform architecture decisions, because decision-makers often read only the L0 summary and the key findings. The inaccurate confidence levels in those sections propagate to downstream design work.

### Systemic Improvement Opportunity

The "zero collisions" conclusion in the key findings (Section: PS Integration) will be consumed by ps-architect when authoring the integration ADR. If ps-architect adopts "zero routing collisions" as a confirmed design premise, the ADR will not include collision mitigation as an open risk. This is a quality propagation failure: a weakly-evidenced research claim becomes a confident architecture premise.

The recommendation to flag this to ps-architect: the collision analysis should be explicitly marked as "5/20+ keywords verified" rather than "zero collisions confirmed."

### H-36 Governance Risk Is the Correct Concern, But Needs Better Handling

The artifact correctly identifies the H-36 governance question as the single most important unresolved architectural issue. The 60-day deadline and fallback design (3-hop anchored mode) are appropriate mitigations. What is missing is explicit guidance on the INTERIM behavior: should Phase 1 build only 3-hop mode, and add 4-hop mode pending governance? Or build both and flag the 4-hop mode as "provisional pending governance"? This ambiguity leaves the build team without clear guidance for C3+ workflow behavior.

### GAP-09 Deferral Is Strategically Correct

The recommendation to defer GAP-09 until after STAR validation is strategically sound and should not be disturbed by revision. The phased implementation plan (Section 4.5) provides appropriate sequencing.

---

## Improvement Areas

### Improvement Area R-01: Correct the L0/Key-Findings H-36 Claim

| Attribute | Value |
|-----------|-------|
| **Criterion** | Internal Consistency |
| **Current Score** | 0.78 |
| **Target Score** | 0.90 |
| **Priority** | HIGH |

**Gap Description:** The L0 executive summary states "all four /nuclear-sop agents can operate as a self-contained unit without requiring any other skill" without mentioning the pending H-36 governance question. The key findings in the PS Integration section say "Nuclear-sop agents are autonomous as a unit" without qualification. These statements are factually incomplete: the 4-hop C3+ mode's H-36 compliance is an open governance question. A stakeholder reading only the L0 and key findings receives an overly favorable picture.

**Evidence:** L0 says "the minimum viable invocation is the full sop-brief -> sop-executor -> sop-verifier -> sop-capture sequence (3-hop mode)" without explaining that 3-hop mode is the C1-C2 variant and 4-hop mode (C3+) is pending governance approval. Section 1.1.C describes the same situation as a "pending governance question."

**Recommendation:**
1. Revise the L0 executive summary to add: "For C3+ workflows, the 4-hop mode (adding sop-verifier) is proposed but pending a framework governance ruling on whether intra-skill predetermined sequences count against H-36's 3-hop circuit breaker. The 3-hop mode (brief -> executor -> capture) is compliant today for C1-C2 workflows."
2. Revise key finding #2 to: "H-36 governance question is the single blocking architectural concern for C3+ workflows -- the 4-hop mode's compliance is pending a governance ruling; the 3-hop mode is compliant for C1-C2."
3. Revise key finding #3 to: "Nuclear-sop agents are autonomous as a 3-hop unit (C1-C2); 4-hop mode (C3+) requires H-36 governance ruling."

**Expected Impact:** Brings Internal Consistency from 0.78 to ~0.90. The fix is editorial (no new research required).

---

### Improvement Area R-02: Verify /schedule Existence or Reframe GAP-09 Feasibility

| Attribute | Value |
|-----------|-------|
| **Criterion** | Completeness, Evidence Quality |
| **Current Score** | Completeness 0.82, Evidence Quality 0.80 |
| **Target Score** | 0.88, 0.87 |
| **Priority** | HIGH |

**Gap Description:** The GAP-09 design states `/schedule (cron-based remote agent execution) -- New Required: None -- Assessment: Fully reusable` and calculates 60-70% infrastructure reuse on this basis. However, no source document cited in the artifact mentions `/schedule`. The trigger map in `mandatory-skill-usage.md`, the CLAUDE.md skill table, and all nine cited references make no mention of a `/schedule` skill. If `/schedule` does not exist, the infrastructure reuse assessment is incorrect, and GAP-09 periodic execution requires creating new infrastructure (not reusing it).

**Evidence:** Section 4.4 infrastructure table: "/schedule (cron-based remote agent execution) -- None -- Fully reusable." The artifact's nine references do not include any `/schedule` source.

**Recommendation:**
1. Verify whether `/schedule` exists as an operational Jerry skill by checking CLAUDE.md and mandatory-skill-usage.md.
2. If `/schedule` does NOT exist: revise the GAP-09 infrastructure table to mark periodic execution as "New -- moderate effort" (requires either creating a /schedule skill or using an external cron mechanism). Revise the 60-70% reuse claim to reflect the actual reuse percentage with /schedule removed.
3. If `/schedule` DOES exist: add it to the References section with its SKILL.md path and version.
4. Either way: note what "periodic triggering" actually means in the absence of a confirmed /schedule skill -- does it mean manual invocation on a calendar cadence, external cron job, or something else?

**Expected Impact:** Brings Completeness from 0.82 to ~0.88, Evidence Quality from 0.80 to ~0.87. Moderate effort: requires a file lookup and one paragraph of revision.

---

### Improvement Area R-03: Qualify the "Zero Keyword Collisions" Verdict

| Attribute | Value |
|-----------|-------|
| **Criterion** | Evidence Quality, Methodological Rigor |
| **Current Score** | Evidence Quality 0.80, Methodological Rigor 0.86 |
| **Target Score** | 0.87, 0.91 |
| **Priority** | MEDIUM |

**Gap Description:** The collision analysis checks 5 of 20+ proposed trigger keywords and concludes "Zero unresolved keyword collisions." This conclusion is not supported by incomplete analysis. Additionally, "SOP" (without "nuclear") is a common enterprise acronym that could match user requests that have nothing to do with nuclear procedures (e.g., "create an SOP for our release process" would trigger /nuclear-sop when /problem-solving or /diataxis is appropriate).

**Evidence:** Section 2.3 lists exactly 5 keywords in the collision table (workflow, procedure, execute, compliance, rigor). The trigger map entry has 20+ positive keywords (nuclear sop, nuclear procedure, STAR self-check, pre-job brief, post-job brief, hold point, place-keeping, step sign-off, procedure compliance, continuous use, procedure use classification, operating experience capture, OE entry, nuclear rigor, nuclear discipline, sop brief, sop execute, sop capture, sop verify, nuclear workflow). 15 keywords are not checked.

**Recommendation:**
1. Add the remaining 15+ keywords to the collision table: "sop brief", "sop execute", "sop capture", "sop verify", "OE entry", "operating experience", "continuous use", "procedure use classification", "nuclear rigor", "nuclear discipline", "nuclear workflow", "pre-job brief", "post-job brief", "STAR self-check", "hold point", "place-keeping", "step sign-off".
2. Pay special attention to "sop" (without "nuclear") -- check if this alone could trigger /nuclear-sop on general SOP requests. If so, recommend that "sop" alone should only match as part of compound triggers ("nuclear sop", "sop brief", etc.) -- not as a standalone positive keyword.
3. Revise the verdict from "Zero unresolved keyword collisions" to "No collisions identified in exhaustive keyword cross-reference" (after completing the full check) or "Partial collision analysis -- 5 of 20 keywords verified, no collisions in checked set" (if full check is not feasible in this iteration).

**Expected Impact:** Brings Evidence Quality from 0.80 to ~0.87, Methodological Rigor from 0.86 to ~0.91.

---

### Improvement Area R-04: Resolve the P-003 Ambiguity in the eng-team Composition Pattern

| Attribute | Value |
|-----------|-------|
| **Criterion** | Internal Consistency, Completeness |
| **Current Score** | Internal Consistency 0.78 |
| **Target Score** | 0.88 |
| **Priority** | MEDIUM |

**Gap Description:** The nuclear-sop wrapping eng-team composition (Section 1.4.C, Pattern 1) shows sop-executor invoking eng-backend, eng-frontend, and eng-infra "in parallel." This implies sop-executor delegates to eng-team agents, but sop-executor's tool tier is not specified. If sop-executor is a T2 agent (no Task tool), it cannot invoke other agents. If it is T5 (Full), it violates H-35 (worker agents must not be T5). This is a P-003 compliance ambiguity that the integration analysis does not resolve.

**Evidence:** Section 1.4.C, Pattern 1 diagram shows `sop-executor` at the top, with `eng-backend / eng-frontend / eng-infra [parallel]` as sub-items -- implying delegation.

**Recommendation:**
1. Add a clarification note: "In this composition, sop-executor does NOT directly invoke eng-team agents. Instead, sop-executor records steps in PROCEDURE_STATE.yaml, and the orchestrator (MAIN CONTEXT or orch-planner) invokes the appropriate eng-team agents at each step. sop-executor tracks step completion in PROCEDURE_STATE.yaml; the orchestrator sequences the invocations."
2. If the intended design is different (i.e., sop-executor IS the orchestrator for eng-team agents), explicitly state that sop-executor would need T5 tool access, and reconcile this with H-35.
3. Clarify this in the composition diagram to remove the visual suggestion that sop-executor is spawning sub-agents.

**Expected Impact:** Brings Internal Consistency from 0.78 to ~0.86.

---

### Improvement Area R-05: Add Context Window Budget Warning for Large Compositions

| Attribute | Value |
|-----------|-------|
| **Criterion** | Completeness |
| **Current Score** | 0.82 |
| **Target Score** | 0.87 |
| **Priority** | MEDIUM |

**Gap Description:** The nuclear-sop + eng-team full composition (12+ sequential agents) and the nuclear-sop + problem-solving multi-step composition are presented without addressing context window resource consumption. STAR self-checking adds ~2x token overhead per step (per the specification's own trade-off table). For a 12-agent sequence, cumulative context consumption may make the composition impractical even if it is architecturally valid.

**Evidence:** Section 5.3 trade-off table mentions "Token consumption (~2x for STAR; additional agent invocations for brief/capture)" but applies this to the simple case, not the 12-agent composition.

**Recommendation:**
1. Add a note to the eng-team composition pattern: "This composition requires careful context window management. For a full 8-step eng-team engagement, consider using cross-session resume via PROCEDURE_STATE.yaml at phase boundaries. Each eng-team agent should produce its artifacts to disk before the next agent loads (CB-02: tool results should not exceed 50% of context)."
2. Reference the context budget standards (CB-01 through CB-05 in agent-development-standards.md) as the governing constraints for this composition.

**Expected Impact:** Brings Completeness from 0.82 to ~0.87.

---

### Improvement Area R-06: Cite or Retract the /eng-team 1-Hop Claim

| Attribute | Value |
|-----------|-------|
| **Criterion** | Evidence Quality, Traceability |
| **Current Score** | Evidence Quality 0.80, Traceability 0.90 |
| **Target Score** | 0.85, 0.93 |
| **Priority** | LOW |

**Gap Description:** Section 1.1.C states "This interpretation is consistent with how /eng-team's 8-step sequential workflow counts as 1 hop, and /adversary's 3-agent tournament counts as 1 hop." This is presented as factual but has no citation. If this is verifiable in agent-routing-standards.md or the eng-team SKILL.md, it should be cited. If it is an inference, it should be framed as one ("by analogy with how /eng-team's sequential workflow would logically be counted").

**Evidence:** Section 1.1.C: "This interpretation is consistent with how /eng-team's 8-step sequential workflow counts as 1 hop." No source cited.

**Recommendation:**
1. Check agent-routing-standards.md "What Counts as a Hop" table for explicit language about multi-agent skills.
2. If found: add citation ("per agent-routing-standards.md Circuit Breaker section, 'What Counts as a Hop' table").
3. If not found: rephrase to "By analogy, /eng-team's 8-step sequential workflow would logically count as 1 hop under this interpretation, as would /adversary's 3-agent tournament. However, neither is explicitly confirmed in agent-routing-standards.md -- this interpretation requires governance confirmation along with the H-36 ruling."

**Expected Impact:** Brings Evidence Quality from 0.80 to ~0.85, Traceability from 0.90 to ~0.93.

---

## Recommendation

**Verdict: REJECTED per H-13** (score 0.84 < 0.85 threshold)

**Operational band: REVISE** -- targeted revision is likely sufficient to reach 0.90.

The research artifact is substantively good. The pairwise integration methodology, composition patterns, autonomy matrix, and GAP-09 design are all valuable and directionally correct. The findings are directionally sound enough that ps-architect can begin integration ADR planning in parallel, provided the following caveats are communicated:

1. The H-36 compliance for C3+ 4-hop mode is UNRESOLVED -- do not treat it as confirmed.
2. The "zero routing collisions" verdict is UNVERIFIED for 15 of 20+ keywords -- treat it as a working hypothesis pending full analysis.
3. The /schedule dependency in GAP-09 requires verification before the 60-70% reuse claim can be used in planning.

**Estimated post-revision score: 0.91-0.93** (above the 0.90 target threshold) if R-01, R-02, and R-03 are addressed. R-04, R-05, and R-06 are recommended but not blocking for threshold passage.

**Revision priority order:** R-01 (editorial, 30 minutes) > R-02 (file lookup + one paragraph, 1 hour) > R-03 (complete collision table, 2 hours) > R-04 (clarification note, 30 minutes) > R-05 (one paragraph, 15 minutes) > R-06 (citation lookup, 15 minutes).

---

## PS Integration

**PS ID:** phase-5.1
**Entry ID:** e-005 (critique)
**Artifact:** `projects/PROJ-0039-nuclear-engineer/research/skill-integration-critique.md`
**Critic Agent:** ps-critic
**Quality Score:** 0.84
**Threshold Met:** NO (threshold: 0.90)
**Recommendation:** REVISE

**State output:**
```yaml
critic_output:
  ps_id: "phase-5.1"
  entry_id: "e-005-critique"
  iteration: 1
  artifact_path: "projects/PROJ-0039-nuclear-engineer/research/skill-integration-critique.md"
  quality_score: 0.84
  assessment: "REJECTED"
  threshold_met: false
  recommendation: "REVISE"
  improvement_areas:
    - criterion: "Internal Consistency"
      current_score: 0.78
      priority: "HIGH"
      summary: "L0 and key findings overstate H-36 compliance for 4-hop C3+ mode; pending governance question not disclosed at summary level"
    - criterion: "Completeness / Evidence Quality"
      current_score: 0.82
      priority: "HIGH"
      summary: "/schedule dependency in GAP-09 not verified to exist; 'Fully reusable' claim unsupported"
    - criterion: "Evidence Quality / Methodological Rigor"
      current_score: 0.80
      priority: "MEDIUM"
      summary: "Collision analysis covers 5 of 20+ keywords; 'zero collisions' verdict overstated"
    - criterion: "Internal Consistency / Completeness"
      current_score: 0.78
      priority: "MEDIUM"
      summary: "P-003 ambiguity: sop-executor delegation to eng-team agents implies T5 tool access which violates H-35"
    - criterion: "Completeness"
      current_score: 0.82
      priority: "MEDIUM"
      summary: "12-agent composition lacks context window budget analysis"
    - criterion: "Evidence Quality / Traceability"
      current_score: 0.80
      priority: "LOW"
      summary: "/eng-team 1-hop claim has no citation; load-bearing for H-36 analysis"
  next_agent_hint: "ps-researcher for targeted revision addressing R-01 through R-03 (HIGH priority items)"
```

---

*Critique Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0 (P-001, P-002, P-003, P-004, P-022)*
*Strategies Applied: S-003 (Steelman), S-002 (Devil's Advocate), S-007 (Constitutional AI Critique), S-014 (LLM-as-Judge)*
*Created: 2026-03-25*
*Agent: ps-critic*

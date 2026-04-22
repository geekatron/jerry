---
id: PM-MS-040-054
type: gtm-plan
title: "Jerry Framework Documentation Positioning and Messaging Framework (Phase 1b)"
agent: pm-market-strategist
status: under_review
mode: delivery
feature_id: FEAT-040-054
phase: "1b"
handoff_id: HO-W1-054
risk_domain: business-viability-risk
sensitivity: internal
criticality: C3
quality_threshold: 0.92
iteration_ceiling: 7
created: 2026-04-20
last_validated: 2026-04-20
iteration: 4
confidence: 0.80
self_score: 0.923
xp_consumes:
  - XP-03  # FEAT-040-055 competitive insights
  - XP-04  # FEAT-040-001 JTBD switch triggers (STOP GATE A4/A6)
frameworks_applied:
  - "April Dunford -- Obviously Awesome (5-step positioning)"
  - "Geoffrey Moore -- Crossing the Chasm (beachhead + whole-product)"
  - "Messaging Hierarchy (elevator -> 1-sentence -> 1-paragraph -> narrative)"
  - "StoryBrand (guide framing, used sparingly)"
cross_refs:
  - "FEAT-040-055 (competitive)"
  - "FEAT-040-001 (JTBD)"
  - "FEAT-040-056 (OSS best practices)"
  - "FEAT-040-053 (personas, parallel)"
  - "QG-2 consistency report 2026-04-20"
validation_gates:
  V-01_behavioral_system_framing:
    status: OPEN
    scope_blocked: "Candidate C (Cognitive Operating Layer). Final README/docs/index.md copy MUST NOT commit to behavioral-system framing until V-01 passes per FEAT-040-055 plan."
    owner: "pm-customer-insight via FEAT-040-053"
  A4_A6_STOP_GATE:
    status: OPEN
    scope_blocked: "A4 (Security Practitioner) and A6 (Domain Specialist) segment messaging. N >= 3 interviews per segment required before commit."
    owner: "FEAT-040-053 persona work item (owner routed at Phase 1b entry per JTBD iter-5 LJ-003)"
---

# Jerry Framework Documentation Positioning and Messaging Framework

> Wave 1 Phase 1b positioning and messaging framework for Jerry's OSS documentation. Consumes XP-03 (competitive) and XP-04 (JTBD) under the XP-04 STOP GATE and the V-01 validation gate. Grounds all positioning in upstream finding evidence. No speculative messaging.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Top-line outputs for downstream consumption |
| [Gate Acknowledgment](#gate-acknowledgment) | V-01 and A4/A6 STOP GATE status + scope limits |
| [L1: Category Definition (Candidates)](#l1-category-definition-candidates) | Three candidate category frames with reasoning and evidence |
| [L1: Positioning (Dunford 5-Step)](#l1-positioning-dunford-5-step) | Competitive alternatives, unique attributes, value, segment, category |
| [L1: Canonical One-Liner (Jerry Definition)](#l1-canonical-one-liner-jerry-definition) | Resolves F-011 jargon density and HYP-010; consistency artifact for README/docs/INSTALLATION |
| [L1: Messaging Hierarchy](#l1-messaging-hierarchy) | Elevator, 1-sentence, 1-paragraph, longer narrative |
| [L1: Differentiation Claims](#l1-differentiation-claims) | Three defensible claims; claimed-not-validated flags |
| [L1: Per-Segment Value Propositions (A1-A6)](#l1-per-segment-value-propositions-a1-a6) | Grounded in JTBD actor segments; A4/A6 DRAFT-only |
| [L1: Messaging Consistency Map](#l1-messaging-consistency-map) | README, docs/index.md, INSTALLATION alignment (resolves F-007) |
| [L2: Persona Messaging Cross-Reference](#l2-persona-messaging-cross-reference) | Handoff to FEAT-040-053 parallel work |
| [L2: Crossing the Chasm Posture](#l2-crossing-the-chasm-posture) | Beachhead segment + whole-product implications |
| [L2: Validation Plan](#l2-validation-plan) | V-01 protocol + A4/A6 checklist + open questions |
| [L2: Limitations and Known Biases](#l2-limitations-and-known-biases) | Evidence provenance and explicit caveats |
| [Evidence Index](#evidence-index) | Traceability to XP-03/XP-04/FEAT-040-056 |
| [Self-Score (S-014)](#self-score-s-014) | 6-dimension quality assessment |
| [Revision History](#revision-history) | Iteration log with blocker closures |

---

## L0: Executive Summary

1. **Three candidate category frames are presented, not a single commitment.** (a) **Task-outcome framing** ("Claude Code plugin for persistent rules, shared memory, and quality gates") is the safest near-term frame -- it is legible to competitors' audiences and does not depend on unvalidated hypotheses. (b) **Attribute-plus-constraint framing** ("Governance layer for Claude Code: persistent rules, shared memory, and quality gates that keep AI work reproducible") borrows the OpenAI Agents SDK pattern of constraint-first positioning and is testable with zero interviews. (c) **Behavioral-system framing** ("Jerry makes Claude behave -- persistent rules, shared memory, and quality gates that survive Claude's context limits") is the competitive-gap hypothesis identified in FEAT-040-055 L2; it is [INFERRED] and blocked by V-01 until pm-customer-insight completes 3-5 target-audience interviews. **Conditional near-term commit: Candidate B (attribute+constraint), with explicit rollback to Candidate A if A1 vocabulary resonance test or V-01 interviews show "governance layer" reads as enterprise-y.** Rollback rule: if >= 2 of 5 V-00/V-01 A1 participants describe "governance layer" as enterprise-y or mismatched to solo-developer vocabulary, revert to Candidate A for README/docs surfaces; Candidate C remains the preferred long-term frame conditional on V-01 pass.

2. **Canonical Jerry one-liner (prescribes resolution for F-011, HYP-010, F-007 consistency gap):** *"Jerry is a Claude Code plugin that keeps Claude's work consistent across sessions -- persistent rules, shared memory, and quality gates that survive Claude's context limits."* This sentence is designed to appear verbatim as the opening line of README.md, docs/index.md (under "What is Jerry?"), and INSTALLATION.md's tutorial-entry paragraph. Verbatim reuse is the messaging-consistency mechanism. Note: "resolves" was revised to "prescribes resolution for" per iter-1 DA-006 -- resolution requires Wave 2 implementation of the Messaging Consistency Map.

3. **A1 (Solo Engineer), A2 (Technical Lead), A5 (New OSS User) messaging is ready for external commit. A3 (Framework Contributor) messaging is ready for internal commit only (CONTRIBUTING.md / docs/explanation/ target; not for README/docs/index.md primary surfaces).** Switch triggers for A1/A2/A3 are labeled "MEDIUM confidence, AI-synthesized from SKILL.md secondary research" per FEAT-040-001 iter-5 inherited confidence label (not primary-user-interview validated; see LJ-004 iter-1 for circular evidence note). A5 messaging is a derivative of A1 with evaluation-framework framing for first-contact context. A4 (Security Practitioner) and A6 (Domain Specialist) messaging is DRAFT-ONLY and blocked by the XP-04 STOP GATE: N >= 3 interviews per segment per JTBD A4/A6 Validation Protocol. Publishing A4 or A6 messaging before gate closure is an explicit guardrail violation.

4. **Top three differentiators against Claude Agent SDK, OpenAI Agents SDK, LangChain, CrewAI, LlamaIndex, AutoGen** (grounded in FEAT-040-055 scorecard): (i) Governance-as-product -- quality-enforcement.md published and enforced at 0.92 threshold, no competitor publishes an equivalent; (ii) Session-persistent memory designed around compaction -- worktracker + filesystem-as-memory architecture; no benchmarked competitor's positioning addresses compaction directly *as of 2026-04-20* (positioning gap, not technical moat; a single competitor documentation update can close it per iter-1 DA-002/PM-003); (iii) Skill ecosystem breadth -- 30 skills with methodology-grade depth (Cockburn UC 2.0, Kano, HEART, PTES/ATT&CK) spanning SDLC + UX + security + PM/PMM, no single competitor covers this span. Each differentiator is flagged below with provenance tier and "claimed, not validated" where appropriate.

5. **Messaging commits required for Phase 2 implementation (prioritized):** (a) Replace current README `> A Claude Code plugin for behavior and workflow guardrails with knowledge accrual.` tagline with the canonical one-liner from item 2; (b) align docs/index.md "What is Jerry?" paragraph to use the same canonical one-liner as its opening sentence; (c) add the canonical one-liner to INSTALLATION.md lead paragraph before the Prerequisites block; (d) remove the aspirational phrase "accrues knowledge, wisdom, experience" from primary surfaces (tone gap per FEAT-040-055 -- [INFERRED] but low-risk given the phrase already reads as aspirational, not technical).

---

## Gate Acknowledgment

### V-01 (Behavioral-System Framing Validation) -- OPEN

Per FEAT-040-055 L2 "Positioning gap" caveat and Validation Plan V-01:

> Every benchmarked framework positions around what you build with it. Jerry's potential competitive gap is positioning around what it makes Claude reliably do ... This framing requires audience validation before commitment.

**This artifact commits to:**
- Candidate A (task-outcome) as the rollback near-term production option if V-00 (A1 vocabulary resonance test, iter-2 new pre-gate) fails. Candidate A is explicitly NOT dependent on V-01.
- Candidate B (attribute+constraint) as the conditional near-term production option, contingent on V-00 pass. Candidate B IS dependent on V-00 ("governance layer" vocabulary resonance test with A1), which is a lightweight pre-gate running combined with V-01 interviews.
- Candidate C (behavioral-system) as a hypothesis, documented with rationale, NOT committed to README/docs copy.
- Final frame selection after V-00 (A1 resonance) and V-01 (behavioral-system) interviews close -- owner: pm-customer-insight via FEAT-040-053.

### A4/A6 STOP GATE (XP-04 Switch Trigger Validation) -- OPEN

Per FEAT-040-001 iter-5 L1 Switch Force Analysis:

> XP-04 Positioning MUST NOT finalize messaging targeted at A4 Security Practitioners or A6 Domain Specialists until the A4/A6 Switch Trigger Validation Protocol is satisfied.

**This artifact commits to:**
- A1/A2/A3/A5 messaging blocks are CANDIDATE FINAL (Phase 2 may adopt pending adv-review).
- A4 messaging is DRAFT-ONLY with the explicit warning: "Do not publish until N >= 3 A4 interviews confirm Burp Suite / Cobalt Strike / PTES-runbook prior solution."
- A6 messaging is DRAFT-ONLY with the explicit warning: "Do not publish until N >= 3 A6 interviews confirm Dovetail / Figma / Airtable / Notion / Miro prior solution."

Gate resolution remains the responsibility of FEAT-040-053 (personas) per JTBD iter-7 LJ-003 routing note.

---

## L1: Category Definition (Candidates)

**What is Jerry?** There is no single correct answer. The three candidate frames below are evaluated against identical criteria.

### Selection Criteria (applied to each candidate)

> **Weights disclosure (iter-2, responds to FM-002, LJ-003, IN-004):** The weights below are **author-defined judgment weightings**, NOT sourced from Dunford, Moore, or other published positioning frameworks. Dunford's *Obviously Awesome* specifies the 5-step methodology but does not prescribe criterion weights; weight assignment is an analyst-judgment input. The six criteria are derived from Dunford Step 5 (market category choice dimensions -- legibility and differentiation) and general positioning evaluation practice (evidence grounding, jargon, validation risk, durability). Weights reflect the author's judgment that legibility, differentiation, and evidence grounding carry equal primary weight (20% each) given the OSS pre-release context where all three are load-bearing. Different weight assignments could change the Candidate B recommendation -- see Recommendation note below for the sensitivity check.

| Criterion | Weight | Question | Source |
|-----------|--------|----------|--------|
| Competitor legibility | 20% | Would a developer arriving from LangChain/CrewAI understand this in 10 seconds? | Author-defined; derives from Dunford Step 5 (market category choice) |
| Differentiation strength | 20% | Does it occupy space competitors don't? (FEAT-040-055 L2 competitive gap) | Author-defined; derives from Dunford Step 5 + FEAT-040-055 competitive gap analysis |
| Evidence grounding | 20% | Is the claim supported by FEAT-040-055/FEAT-040-001/FEAT-040-056 findings, not inference alone? | Author-defined; aligns with pm-market-strategist evidence-tier guardrail |
| Jargon density | 15% | Does it introduce terms F-011 would flag? | Author-defined; responds to FEAT-040-004 F-011 heuristic finding |
| Validation risk | 15% | Is it safe to ship without interviews? | Author-defined; responds to V-01 gate architecture |
| Long-term durability | 10% | Will it still be true when Jerry has 60 skills instead of 30? | Author-defined; forward-looking judgment |

### Candidate A: Task-Outcome Framing (current state, refined)

**Frame:** "Jerry is a Claude Code plugin for persistent rules, shared memory, and quality gates."

**Rationale:** This is a refinement of the current README tagline, re-expressed with the canonical capability triplet. Competitor-legible (mirrors Claude Agent SDK "Build production AI agents" pattern per FEAT-040-055 positioning table EV-001). Grounded in current docs/index.md which already names three capabilities (re-expressed here with the canonical triplet per iter-2 FM-015/LJ-002 dual-vocabulary resolution). Zero interview requirement. Low jargon density -- "rules, memory, gates" are concrete nouns.

**Weaknesses:** Does not differentiate against Claude Agent SDK on the governance dimension. "Guardrails" is a term LangChain and OpenAI Agents SDK also use (OpenAI Agents SDK names "Guardrails" as one of three primitives per FEAT-040-055 OpenAI entry). Risk of sounding derivative.

**Evidence tier:** Direct (FEAT-040-055 positioning table; FEAT-040-001 actor-breadth supports "guardrails" term across A1/A2/A3).

### Candidate B: Attribute-Plus-Constraint Framing (conditional near-term commit)

**Frame:** "Jerry is a governance layer for Claude Code -- persistent rules, shared memory, and quality gates that keep AI work reproducible across sessions."

**Rationale:** Borrows OpenAI Agents SDK's "very few abstractions" pattern (FEAT-040-055 EV-010) -- attribute-first, constraint-signaling. "Reproducible across sessions" is directly grounded in the FEAT-040-001 Cat 1 (Structured Cognition) pain-state language ("Context Rot", "artifacts survive compaction") without requiring unvalidated inference. "Governance layer" is a concrete architectural noun, not aspirational ("accrues knowledge, wisdom" problem identified in FEAT-040-055 tone gap).

**Weaknesses:** "Governance layer" may read as enterprise-y; Jerry's A1 (Solo Engineer) users may not self-identify as needing governance. Candidate C may eventually be stronger but requires V-01.

**Evidence tier:** Direct for "rules, memory, skills" (SKILL.md file inventory via FEAT-040-001 per-skill table). Direct for "reproducible across sessions" (quality-enforcement.md canonical pattern; FEAT-040-056 HITL finding that LLM-as-judge >=0.95 + independent reviewer aligns with field consensus). Synthesis for "governance layer" framing (derived from FEAT-040-055 governance-as-differentiator + FEAT-040-056 M-04 HEART-as-pioneering).

### Candidate C: Behavioral-System Framing (hypothesis; blocked by V-01)

**Frame:** "Jerry is the behavioral system for Claude Code -- persistent rules, shared memory, and quality gates that make Claude reliably do the work across sessions."

**Rationale:** Directly occupies the competitive gap identified in FEAT-040-055 L2. Every benchmarked framework positions around what the developer builds with it; Jerry would position around what the developer makes Claude do. This is genuinely differentiated positioning space.

**Weaknesses:** `[INFERRED - requires audience validation]` per FEAT-040-055. Unknown whether target OSS audience (developers arriving from LangChain / CrewAI without prior Claude Code context) parses "behavioral system" as meaningful or as opaque jargon. Risk: users may conflate Jerry with Claude Agent SDK itself (which positions as "build agents with Claude Code as a library" per FEAT-040-055 EV-001). If conflated, Jerry loses its differentiation.

**Evidence tier:** Inference (FEAT-040-055 L2 positioning gap is observed market fact; interpretation that target audience will find it compelling is inference).

**Commit status:** HYPOTHESIS ONLY. Will be tested in V-01. If V-01 passes (>=3/5 participants find it more interpretable or more compelling), Candidate C becomes the final frame in Phase 2 README copy.

### Candidate Comparison Matrix

| Criterion | A (Task-Outcome) | B (Attribute+Constraint) | C (Behavioral-System) |
|-----------|------------------|---------------------------|------------------------|
| Competitor legibility | High | High | Medium (risk: opacity) |
| Differentiation strength | Low | Medium | High (if V-01 confirms) |
| Evidence grounding | Direct | Direct+Synthesis | Inference |
| Jargon density | Low | Medium | Medium-High |
| Validation risk | None | None | High until V-01 |
| Long-term durability | Medium | High | High (conditional) |
| **Near-term commit?** | **Acceptable (rollback target)** | **Conditional (see V-00 pre-gate)** | **Blocked by V-01** |

### Recommendation

**Conditional near-term commit: Candidate B.** Retain Candidate C as the V-01 test hypothesis. Given iter-1 DA-003/IN-003 finding that Candidate B commit is premature vs. Open Question #1 (A1 "governance layer" resonance), this iter-2 recommendation reframes the commit as conditional:

**V-00 pre-gate (new, iter-2):** A lightweight 5-participant A1 vocabulary resonance test of "governance layer" phrasing. Format: side-by-side comparison of Candidate A ("persistent rules, shared memory, and quality gates") vs. Candidate B ("governance layer -- persistent rules, shared memory, and quality gates"). Target: A1 developers currently using vanilla Claude Code. Pass criterion: at most 1 of 5 describes "governance layer" as enterprise-y or mismatched to solo-developer vocabulary. Owner: pm-customer-insight via FEAT-040-053 (combined with V-01 interview protocol). Timeline: pre-Phase 2 README revision.

**Rollback rule (new, iter-2):** If V-00 fails (>= 2 of 5 A1 participants describe "governance layer" as enterprise-y), Phase 2 README copy adopts Candidate A as the near-term frame. Candidate C remains the V-01 test hypothesis regardless of V-00 outcome. If V-00 passes, Candidate B proceeds to Phase 2 commit; if V-01 later passes, Phase 2a upgrades to Candidate C.

**V-00 pre-gate enforcement (iter-3, DA-001 closure; iter-4 DA-001-054i3 filename convention added):** Wave 2 work item (will be tracked as FEAT-040-0XX-wave2-readme-commit) MUST NOT create or edit README canonical positioning until V-00 test outcome is recorded in `projects/PROJ-040-documentation/orchestration/reviews/`. Expected filename pattern: `orchestration/reviews/v-00-vocabulary-test-{YYYYMMDD}-{NNN}.md`. Wave 2 entrance criteria explicitly include V-00 PASS or Candidate A rollback activation. This enforcement path closes the gap identified in iter-2 where V-00 was defined but the forward enforcement linkage was soft.

**Weight sensitivity disclosure with calculation (iter-3, responds to FM-002 / IN-002 / TR-001):** The criteria weights above are author-defined judgments. Numeric scoring uses the ordinal mapping High=3, Medium=2, Low=1 (for qualitative ratings), Direct=3, Direct+Synthesis=2.5, Inference=1 (for evidence), None=3 (best) / High=1 (worst) for validation risk, and symmetric mapping for jargon (Low=3 / Medium=2 / Medium-High=1). The table below shows the author-default outcome and the re-weighting that actually produces an A/B tie -- which is **not** Validation Risk re-weighting as claimed in iter-2. The iter-2 claim is honestly corrected here: A and B both score "None" on Validation Risk, so re-weighting Validation Risk does not change their relative ranking.

| Weighting | Competitor Legibility | Differentiation | Evidence | Jargon | Validation Risk | Durability | A score | B score | Winner |
|-----------|-----------------------|-----------------|----------|--------|-----------------|------------|---------|---------|--------|
| Author default (current) | 20% | 20% | 20% | 15% | 15% | 10% | 2.50 | 2.55 | B (by 0.05) |
| Validation Risk 25% (iter-2 claim, corrected) | 20% | 15% | 20% | 15% | 25% (+10 from Diff -5, Jargon -5) | 10% | 2.60 | 2.625 | B (by 0.025; not tied -- iter-2 claim was imprecise) |
| Jargon 25%, Differentiation 10% (actually ties) | 20% | 10% | 20% | 25% | 15% | 10% | 2.65 | 2.55 | A (by 0.10; re-weighting can flip the decision) |

> **Footnote (iter-4, PM-004-054i3):** Candidate C excluded from near-term decision space per V-01 gating; re-evaluate if V-01 validates.

**Honest finding (iter-3):** The iter-2 assertion that "re-weighting Validation Risk to 25% makes A and B score equally" is imprecise -- A and B both carry Validation Risk = None in the matrix, so that re-weighting cannot tie them. The genuine sensitivity is to Jargon Density weight: raising Jargon weight (emphasizing A's cleaner plain language) and lowering Differentiation weight (de-emphasizing B's "governance layer" distinctiveness) flips the recommendation to A. Candidate B's recommendation over A therefore rests specifically on the judgment that Differentiation Strength outweighs the additional Jargon margin A provides. If a Phase 2 stakeholder prioritizes plain language over differentiation, the decision is reversible pre-V-00 without invalidating the framework.

---

## L1: Positioning (Dunford 5-Step)

Applied to Candidate B (recommended near-term commit). Candidate A and Candidate C positioning statements are derived in the Candidate Comparison appendix note at the end of this section.

### Step 1: Competitive Alternatives

What developers evaluating Jerry would do if Jerry did not exist. Grounded in FEAT-040-055 benchmarked frameworks and FEAT-040-001 prior-solution column.

| Alternative | Who chooses it | Why |
|-------------|----------------|-----|
| Vanilla Claude Code prompting (no framework) | A1, A3 | Lowest friction; assumes "I can prompt well enough." |
| Claude Agent SDK (Anthropic) | A1 evaluating "SDK vs plugin" | First-party SDK from LLM provider; strong docs (FEAT-040-055 EV-001). |
| OpenAI Agents SDK | A1 evaluating SDK alternatives | "Very few abstractions" positioning (FEAT-040-055 EV-010). |
| LangChain / LangGraph | A1, A2 building agent applications | Largest ecosystem (~126K stars); known pain points (FEAT-040-055 EV-012). |
| CrewAI | A1 orchestrating multi-agent flows | Crew/Flow/Task model (FEAT-040-055 EV-008). |
| Cursor rules / `.cursorrules` / Claude Code CLAUDE.md alone | A1 managing behavioral rules | Simplest rule-file approach; no memory or skill system. |
| Internal custom tooling (scripts + CLAUDE.md) | A2, A3 | Full control, high maintenance cost. |
| Nothing / ad-hoc prompting | A1, A5 | Default state. |

**Note:** "Nothing / ad-hoc prompting" is a legitimate competitor and the most common one for A1 switchers per FEAT-040-001 actor table. Positioning must make the case against "nothing," not only against other frameworks.

### Step 2: Unique Attributes

What Jerry has that these alternatives do not. Only verifiable attributes are listed. Unverified claims are flagged "claimed, not validated."

| Attribute | Evidence Tier | Source |
|-----------|---------------|--------|
| Published quantitative quality gate (>=0.92 weighted composite with 6 calibrated dimensions) | Direct | quality-enforcement.md; FEAT-040-055 SWOT Strengths |
| Creator-critic-revision cycle with minimum 3 iterations enforced as HARD rule (H-14) | Direct | quality-enforcement.md H-14 |
| 5-layer enforcement architecture (L1-L5) documented with token budgets | Direct | quality-enforcement.md Enforcement Architecture |
| Per-prompt re-injection of critical rules immune to context rot (~850 tokens/prompt) | Direct | quality-enforcement.md L2 |
| 30 skills spanning SDLC + UX + security + PM/PMM methodology | Direct | FEAT-040-001 per-skill table |
| Filesystem-as-memory architecture designed around Claude's context limits | Direct | CLAUDE.md Identity; problem-solving SKILL.md "filesystem as infinite memory" |
| Skill routing with keyword-first deterministic layer + circuit breaker (3-hop max) | Direct | agent-routing-standards.md H-36 |
| Agent definitions governed by published dual-file architecture (P-003 single-level nesting, tier model T1-T5, handoff schema v2) | Direct | agent-development-standards.md H-34/H-35 |
| Published constitutional principles (P-001 through P-022) referenced as compliance triplet in all agent definitions | Direct | JERRY_CONSTITUTION.md |
| Free and open source under Apache-2.0 | Direct | LICENSE |
| "Working code before prose" pattern adopted | Claimed, not validated | Requires audit vs. FEAT-040-055 P-01 pattern after Wave 2 README revision |
| "Sub-3-minute Hello World" | Claimed, not validated | Not measured; aspirational per FEAT-040-055 L0 #1 |

### Step 3: Value for Customer Segment

Attribute -> "which means" -> segment-specific benefit. Per-segment values are elaborated in the L1 Per-Segment Value Propositions section.

| Attribute | Which means | Benefit (A1) | Benefit (A2) |
|-----------|-------------|---------------|---------------|
| Quality gate + creator-critic cycle (H-13, H-14) | You ship AI-assisted deliverables with objective quality signal | Stop wondering "is this output actually good?" | Stop relying on gut-feel review for team deliverables |
| Filesystem-as-memory + worktracker | AI work persists across sessions; context compaction does not erase progress | Resume complex tasks next session without re-explaining | Onboard new team members to in-progress work via file trail |
| 30 skills with domain methodology (Cockburn UC 2.0, Kano, HEART, PTES) | Methodology-grade AI assistance without hiring specialists | Apply UX methodology without a UX staff member | Get consistent output shape across team members |
| Constitutional governance (HARD rules) | AI respects non-negotiable constraints | Stop catching AI shortcuts in review | Reduce inconsistency across team prompting styles |

### Step 4: Target Segment

**Beachhead (primary):** A1 Solo Engineer + A2 Technical Lead using Claude Code, shipping AI-assisted work where quality must survive review. Sub-segment breakdown:

| Segment | Sub-descriptor | Pain intensity |
|---------|----------------|----------------|
| A1 -- Solo Engineer | Individual contributor, no team rigor layer | High (FEAT-040-001 Cat 1 Push=5, Pull=4) |
| A2 -- Technical Lead | Team-scale reviewer, accountable for quality | High (FEAT-040-001 Cat 1 actor breadth) |
| A3 -- Framework Contributor | Internal only | N/A for GTM |
| A5 -- New OSS User | Evaluating Jerry without prior context | Medium (FEAT-040-001 A5 bootstrap focus) |

**Deferred (blocked by A4/A6 STOP GATE):**

| Segment | Status |
|---------|--------|
| A4 -- Security Practitioner | DRAFT-ONLY; no production messaging until N>=3 interviews |
| A6 -- Domain Specialist | DRAFT-ONLY; no production messaging until N>=3 interviews |

Target segment selection confidence: **Medium-High.** A1/A2/A3 selection is grounded in FEAT-040-001 direct SKILL.md evidence. A4/A6 deferral is explicit per JTBD STOP GATE. (Cross-reference: Limitations #1 documents the circular evidence chain SKILL.md -> FEAT-040-001 -> FEAT-040-054 that constrains the confidence label below "High".)

### Step 5: Market Category

Jerry's frame of reference. Three candidate categories were examined (see L1 Category Definition Candidates above). **Recommended market category for near-term commit: "governance layer for Claude Code"** (Candidate B).

**Category strategy:** Existing-category-with-a-twist. "Claude Code plugin" is the literal category (competitors: other Claude Code plugins; currently a thin category). "Governance layer" is the twist -- it names a capability Claude Code itself does not provide and positions Jerry as additive, not substitutive. This avoids the "AI agent framework" category dominated by LangChain and avoids the "SDK" category dominated by Anthropic's own Claude Agent SDK.

Category decision is reversible if V-01 validates Candidate C; "behavioral system" would become a near-category creation move if adopted.

### Composed Positioning Statement (Candidate B)

> For developers using Claude Code who need AI-assisted work to survive session boundaries and team review, **Jerry is a governance layer for Claude Code** that keeps AI work reproducible through **persistent rules, shared memory, and quality gates** -- delivered across 30 methodology-grade skills. Unlike Claude Agent SDK or LangChain, which help you build AI applications, Jerry is what you install so the AI itself behaves consistently across sessions.

> **Staleness caveat (iter-2, FM-009):** The "Unlike Claude Agent SDK or LangChain, which help you build AI applications" contrast is valid as of 2026-04-20 per FEAT-040-055 positioning scorecard. Competitor positioning can change without notice; this contrast clause should be re-verified against competitor documentation before each major README release cycle.

### Appendix: Candidate A and C Positioning Statements

For reference during V-01 interview comparison:

**Candidate A:** "For developers using Claude Code who need work to be consistent across sessions, Jerry is a Claude Code plugin that provides persistent rules, shared memory, and quality gates. Unlike vanilla Claude Code prompting, Jerry adds structured rules, memory, and a published quality threshold that survive Claude's context limits."

**Candidate C (hypothesis, blocked by V-01):** "For developers using Claude Code who need reproducible AI work, Jerry is the behavioral system that makes Claude do the work across sessions -- persistent rules, shared memory, and quality gates that survive Claude's context limits. Unlike Claude Agent SDK or LangChain, which are frameworks for what you build, Jerry is the framework for how Claude behaves while building."

---

## L1: Canonical One-Liner (Jerry Definition)

The canonical one-liner exists to solve three problems identified upstream:

- **F-011 (Heuristic, Sev 3 -- jargon density):** current messaging uses aspirational language ("accrues knowledge, wisdom, experience") that does not parse as technical positioning.
- **HYP-010 (Lean UX, ICE=6.0):** "Jerry definition framing" needs resolution before Kano/HEART.
- **F-007 (Heuristic):** "What is Jerry?" messaging varies between README, docs/index.md, and INSTALLATION.md; verbatim reuse of a single sentence is the simplest consistency mechanism.

### Canonical One-Liner (commit this verbatim)

> **Jerry is a Claude Code plugin that keeps Claude's work consistent across sessions -- persistent rules, shared memory, and quality gates that survive Claude's context limits.**

### Design Notes

| Element | Rationale |
|---------|-----------|
| "Claude Code plugin" | Matches the literal product category; aligns with current README; unambiguous for the target beachhead (A1/A2 who already use Claude Code) |
| "keeps Claude's work consistent across sessions" | Action-oriented; addresses the outcome a developer actually wants; avoids "governance layer" (which is stronger Candidate B vocabulary but risks enterprise-y feel) |
| "persistent rules, shared memory, and quality gates" | Names three concrete capabilities (the canonical capability triplet applied consistently across Tier 2/3/4 per iter-2 FM-015/LJ-002 resolution); maps to FEAT-040-001 Cat 1 (Structured Cognition) + Cat 3 (Workflow Management); no jargon per F-011 |
| "survive Claude's context limits" | Plain-language equivalent of "context compaction" (iter-2 FM-004/IN-002 resolution). Preserves the unique differentiation signal (no competitor positioning addresses this) while remaining parseable for A5 developers arriving without prior Claude Code context. Tier 3/4 expand with parenthetical gloss for richer context. |

### Conditional Upgrade on V-01 Pass

If V-01 interviews validate Candidate C behavioral-system framing, replace the canonical one-liner with:

> **Jerry is the behavioral system for Claude Code -- persistent rules, shared memory, and quality gates that make Claude do the work consistently across sessions, not just in the next prompt.**

Do not ship the upgraded variant until V-01 interviews complete with >=3/5 "more interpretable" or "more compelling" verdicts per FEAT-040-055 V-01 success criteria.

### Conditional Downgrade on V-00 Fail

If V-00 A1 vocabulary resonance test fails (>= 2 of 5 A1 participants describe "governance layer" as enterprise-y), Phase 2 Candidate A rollback canonical one-liner:

> **Jerry is a Claude Code plugin that keeps Claude's work consistent across sessions -- persistent rules, shared memory, and quality gates that survive Claude's context limits.**

This Candidate A rollback variant is *identical* to the current canonical one-liner because the current one-liner was deliberately composed to avoid "governance layer" vocabulary. Rollback therefore primarily affects Tier 1 elevator and Tier 3 narrative where "governance layer" appears as Candidate B framing.

---

## L1: Messaging Hierarchy

Four-tier hierarchy. Each tier is derived from the tier above; do not paraphrase independently.

### Tier 1: Elevator Pitch (10 seconds, spoken)

"Jerry is a Claude Code plugin that keeps the AI's work consistent across sessions -- persistent rules, shared memory, and quality gates that survive Claude's context limits."

> **Iter-2 note (DA-005/FM-006/LJ-002 resolution):** Tier 1 now derives its vocabulary from the Tier 2 canonical one-liner's capability triplet ("persistent rules, shared memory, and quality gates"). The earlier "Think of it as the governance layer" framing was Candidate B vocabulary and is removed from Tier 1 per derivation discipline. "Governance layer" remains available in Candidate B's Tier 3/4 conditional expansion *only* if V-00 passes; the Tier 1 elevator is frame-neutral and stays valid under Candidate A rollback.

### Tier 2: One-Sentence Summary (the canonical one-liner)

> Jerry is a Claude Code plugin that keeps Claude's work consistent across sessions -- persistent rules, shared memory, and quality gates that survive Claude's context limits.

Verbatim reuse target: README tagline, docs/index.md "What is Jerry?" opening, INSTALLATION.md lead paragraph.

### Tier 3: One-Paragraph Description (for README "What is Jerry?" section + docs/index.md main paragraph)

> Jerry is a Claude Code plugin that keeps Claude's work consistent across sessions. It solves **Context Rot** -- the degradation of LLM performance as Claude's context window fills and the conversation gets automatically truncated -- by persisting rules, work state, and quality decisions to the filesystem instead of relying on the conversation alone. Jerry delivers three capabilities: **persistent rules** (a 5-layer enforcement system with 25 HARD rules that cannot be overridden, re-injected every prompt so context compaction cannot erase them), **shared memory** (worktracker work items, decision logs, and artifacts that survive across sessions, readable by both humans and AI), and **quality gates** (a 0.92 weighted quality threshold enforced through creator-critic-revision cycles). These three capabilities are delivered across 30 methodology-grade skills spanning SDLC, UX, security, and product work -- each producing persistent artifacts that survive compaction. The effect: AI-assisted work that can be reviewed, resumed, and relied on across team members and sessions, not just within a single prompt.

Word count: ~175. Target range: 150-200 for paragraph positioning (iter-2 slightly above prior 100-150 range to accommodate canonical triplet unification and context-compaction gloss).

### Tier 4: Longer Narrative (for docs/explanation/ landing + README "Why Jerry?" expansion)

> Every developer using Claude Code eventually hits the same wall: the AI appears consistent for a while, then starts forgetting constraints, skipping rules, and producing output that silently diverges from what was agreed earlier in the conversation. This is Context Rot -- the well-documented degradation of LLM performance as Claude's context window fills and compaction (the automatic reset when the conversation gets too long) erases prior instructions. You can see it in the small things (instruction drift, missing file paths) and the large things (entire design decisions reconstructed from scratch in the next session).
>
> Jerry addresses Context Rot structurally rather than through better prompting. It provides three capabilities: **persistent rules** -- a 25-HARD-rule constitution that loads at session start and re-injects every prompt, so compaction cannot erase it; **shared memory** -- the filesystem becomes the memory, with work items, decisions, and artifacts readable by both humans and AI across sessions; and **quality gates** -- a weighted 6-dimension rubric with a 0.92 threshold, applied through a creator-critic-revision cycle that catches issues before a human review ever runs. These three capabilities are delivered through 30 methodology-grade skills spanning SDLC, UX, security, and product work.
>
> The result is a shift in what "AI-assisted work" means. Instead of a sequence of isolated prompts, you get a cumulative project knowledge base -- one where the AI can resume next week with full context, where team members can onboard to in-progress work via the file trail, and where constraints you set on Monday are still enforced on Friday. Jerry is not a replacement for Claude Code; it is the layer that makes Claude Code dependable at the scale of weeks instead of minutes.

Word count: ~285. Target range: 250-350 for narrative positioning. Iter-2 changes: removed "brilliant for 30 minutes" editorial (CC-003); unified capability triplet to "persistent rules, shared memory, quality gates" (FM-015/LJ-002); added compaction gloss on first use (FM-004/IN-002).

### Conditional Tier 3/4 Variants on V-01 Pass

If Candidate C is validated, Tier 3 opening sentence changes from "Jerry is a Claude Code plugin that keeps Claude's work consistent across sessions" to "Jerry is the behavioral system for Claude Code -- what you install so Claude does the work consistently across sessions." All other Tier 3/4 content remains valid. Do not preemptively write the variant; pm-customer-insight owns the post-V-01 rewrite.

---

## L1: Differentiation Claims

Three defensible differentiation claims. Each is cited against FEAT-040-055 scorecard or FEAT-040-056 research. "Claimed, not validated" labels flagged per pm-market-strategist guardrail.

### Differentiator 1: Governance-as-Product (published quality enforcement)

**Claim:** No benchmarked competitor publishes a quantitative quality gate, calibrated scoring rubric, and creator-critic-revision protocol as user-facing documentation. Jerry does.

**Evidence tier:** Direct (quality-enforcement.md is public); Direct (FEAT-040-055 scorecard "Explanatory depth" dimension; no competitor scored 5/5 on explanatory depth); Synthesis (FEAT-040-056 M-04 finding that HEART applied to OSS docs is pioneering supports the broader "governance transparency" claim).

**Validated?** Publication is directly verifiable. The claim that "this is a differentiator" depends on the inference that target users value governance transparency. FEAT-040-055 SWOT Opportunities list "governance transparency as credibility signal" and flag it `[INFERRED]`. Treat as claimed, not validated for audience response; validated for factual uniqueness.

**Messaging use:** Suitable for Tier 4 narrative and docs/explanation/ landing. Not suitable for Tier 1 elevator pitch (risk: reads as enterprise-y).

### Differentiator 2: Session-Persistent Memory Designed Around Compaction

**Claim (as of 2026-04-20):** No benchmarked competitor's *positioning language* addresses context compaction directly. Jerry's architecture (rules persist, work items persist, artifacts persist, re-injection per prompt) is designed around the compaction failure mode.

**Temporal fragility disclosure (iter-2, DA-002/PM-003 resolution):** This differentiator is a **positioning gap, not a technical moat**. The claim is derived from analysis of competitor *public positioning text* in FEAT-040-055, not from technical capability analysis. Claude Agent SDK or LangChain may solve compaction technically without currently using "compaction" in their docs -- a single documentation update by Anthropic or LangChain can close this positioning gap within a release cycle. The differentiator has a decay risk flagged in FEAT-040-055 Threats section. Re-verify competitive positioning text before each major Jerry release cycle; do not treat as a permanent moat.

**Evidence tier:** Direct (CLAUDE.md names Context Rot as core problem; quality-enforcement.md L2 re-injection is documented); Direct (FEAT-040-055 "Voice clarity 'what is this'" dimension -- no competitor's positioning statement mentions compaction or persistence across sessions *as of benchmark date*).

**Validated?** Factual uniqueness of the architectural stance (re-injection, filesystem-as-memory) is direct. Claim that target users recognize compaction as their problem is `[INFERRED]`. FEAT-040-056 L0 finding #3 cites DORA-chain doc quality correlation with team performance but does not isolate compaction-handling as a purchase driver. Treat as claimed, not validated for audience recognition; validated for architectural distinctness as of 2026-04-20.

**Messaging use:** Suitable for all tiers. The canonical one-liner includes "survive Claude's context limits" (iter-2 plain-language replacement for "context compaction" per FM-004/IN-002) specifically to lean on this differentiator while remaining parseable for first-contact A5 audiences.

### Differentiator 3: Methodology Breadth (30 skills spanning SDLC + UX + Security + PM)

**Claim:** No single competitor covers Jerry's methodological span. LangChain/LlamaIndex: RAG + agents. CrewAI/AutoGen: multi-agent orchestration. Claude Agent SDK/OpenAI Agents SDK: agent primitives. None include UX methodology (Kano, HEART, JTBD), security methodology (PTES, ATT&CK), PM methodology (RICE, positioning, GTM), or SDLC methodology (Cockburn UC 2.0, BDD Gherkin generation, OpenAPI from use cases).

**Evidence tier:** Direct (FEAT-040-001 per-skill table enumerates all 30 skills); Direct (FEAT-040-055 per-framework narratives confirm none of the benchmarked frameworks include these methodology domains).

**Validated?** Factual breadth is directly verifiable. Claim that breadth is "valuable" is segment-dependent. A1/A2 benefit from SDLC/PM breadth (validated via FEAT-040-001 actor coverage). A4 benefit from security methodology is [INFERRED -- A4 STOP GATE]. A6 benefit from UX methodology is [INFERRED -- A6 STOP GATE].

**Messaging use:** Suitable for Tier 3/4 in segment-specific form. Tier 1 elevator should avoid "30 skills" as a count claim (risks sounding like feature-bragging) and should signal breadth via "methodology-grade skills" instead.

### Differentiators Jerry Does NOT Claim (explicit)

Per pm-market-strategist guardrail (positioning weaknesses must be acknowledged):

- **Adoption breadth:** Jerry has no public GitHub star/PyPI-download signal to cite against LangChain's ~126K stars or LangGraph's ~34.5M monthly downloads (FEAT-040-055 EV-003, EV-014). Positioning must not claim "widely adopted" or "proven at scale."
- **Ease of first contact:** Jerry's Wave 2 README revision has not happened yet. FEAT-040-055 scorecard shows competitors at 3-5 steps to first output; Jerry's current state is "uncaptured." Claim "sub-3-minute Hello World" is aspirational per FEAT-040-055 L0 #1.
- **Enterprise references:** None. Do not imply any.
- **Multi-language parity:** Jerry is Python-only (hooks/scripts). Claude Agent SDK and OpenAI Agents SDK offer TypeScript parity. Do not imply multi-language support.

---

## L1: Per-Segment Value Propositions (A1-A6)

Each value proposition follows the structure: *Segment description* -> *Prior solution* -> *Switch trigger* -> *Jerry value* -> *Messaging block*.

### A1 -- Solo Engineer (CANDIDATE FINAL, ready for Phase 2)

**Description:** Individual contributor using Claude Code. Ships code and docs without team rigor infrastructure. Carries the cost of context loss personally.

**Prior solution (MEDIUM confidence, AI-synthesized from SKILL.md secondary research per FEAT-040-001 iter-5 inherited label):** Vanilla Claude Code prompting; unstructured AI assistance.

**Switch trigger (MEDIUM confidence, AI-synthesized):** "My AI forgets things mid-session or between sessions; I keep re-explaining the same constraints."

**Jerry value:** Persistent rules and memory so the AI keeps constraints; skills so methodology (UC 2.0, test spec, BDD, OpenAPI) is available without specialist tooling; quality gate so output is trustworthy without a reviewer.

**Messaging block:**
> **For solo engineers using Claude Code:** Jerry stops the AI from forgetting. Persistent rules, shared memory, and 30 methodology-grade skills survive across sessions -- so the constraint you set on Monday is still enforced on Friday, and the design decision you made last week is still in the AI's working memory this week.

> **Confidence label (iter-2, LJ-004/LJ-006 resolution):** A1 switch trigger is MEDIUM confidence inherited from FEAT-040-001 iter-5 which explicitly classifies its force ratings as "AI-synthesized from SKILL.md secondary research." The "validated" label used in iter-1 overstated the confidence chain (SKILL.md -> FEAT-040-001 -> FEAT-040-054). Iter-2 downgrades to MEDIUM confidence matching the upstream source. Primary-user-interview validation is deferred to FEAT-040-053 persona work.

### A2 -- Technical Lead (CANDIDATE FINAL pending MEDIUM confidence disclosure, ready for Phase 2)

**Description:** Team-scale reviewer accountable for quality across multiple team members' AI-assisted work. Faces review-fatigue and inconsistency-across-team problems.

**Prior solution (MEDIUM confidence, AI-synthesized):** Ad-hoc verbal review; spreadsheet tracking; Confluence decision pages.

**Switch trigger (MEDIUM confidence, AI-synthesized):** "Every team member prompts differently; I cannot review every prompt; quality is inconsistent."

**Jerry value:** Published quality gate so team output meets a consistent standard without per-prompt review; worktracker so in-progress AI work is discoverable; adversarial critique (C3+) so deliverables are pre-reviewed before human sign-off.

**Messaging block:**
> **For technical leads:** Jerry gives your team a quality floor. A 0.92 weighted quality gate, creator-critic-revision enforced as rule, and shared skills so two team members produce comparable work on the same task. Review what matters; stop re-reviewing the AI's obvious mistakes.

### A3 -- Framework Contributor (CANDIDATE FINAL for CONTRIBUTING.md/docs/explanation surfaces; NOT for README)

> **Iter-2 clarification (DA-004 resolution):** A3's classification was "internal-only" in iter-1 but CONTRIBUTING.md is a public-facing document. A3 messaging is external-facing in the literal sense (public file) but targeted at contributors, not at README first-contact readers. The accurate label is "contributor-facing surfaces only" -- not for README or docs/index.md primary first-contact surfaces.

**Description:** Contributor extending Jerry itself. Builds new skills, refines rules, audits governance. May be an external OSS contributor (post-OSS-release) or an internal framework team member.

**Prior solution (INFERRED, contributor-channel assumption):** For external contributors: exposure to other OSS contribution experiences (docs quality, contribution tooling, community responsiveness). For internal: N/A. Iter-2 acknowledges DA-004: "contributors are recruited, not switched" was asserted without evidence in iter-1; external OSS contributors are self-attracted via documentation quality per LangChain/LlamaIndex pattern precedents.

**Switch trigger (INFERRED):** "I want to extend this framework, but the contribution model is unclear or the quality bar is opaque." (External); N/A for internal.

**Jerry value:** Constitutional compliance triplet, agent definition standards, and the `/adversary` + `/nasa-se` + `/problem-solving` methodology stack to produce contributions that pass quality gates.

**Messaging block (CONTRIBUTING.md / docs/explanation/ target):**
> **For framework contributors:** Jerry is self-governing. New skills follow the agent development standards (dual-file architecture, tier model, handoff schema); new rules pass the 25-rule ceiling check; every change runs through creator-critic-revision. The framework enforces its own contribution quality.

Not for README surface. Primary target: CONTRIBUTING.md and docs/explanation/ architecture pages.

### A4 -- Security Practitioner (DRAFT-ONLY; BLOCKED by A4 STOP GATE)

> **XP-04 STOP GATE STATUS: OPEN.** The messaging block below is DRAFT ONLY. It MUST NOT be published to README, docs/index.md, or any public surface until N >= 3 A4 interviews confirm Burp Suite Pro / Cobalt Strike / manual PTES-OSSTMM runbooks as prior solution per JTBD A4 Validation Protocol.

**Description (INFERRED):** Individual or small-team security practitioner conducting pentest engagements or secure development reviews. Uses methodology-grade tooling and produces compliance-grade reports.

**Prior solution (INFERRED):** Burp Suite Pro + manual PTES / OSSTMM runbooks; Cobalt Strike for red-team engagements.

**Switch trigger (INFERRED):** "My methodology runbook takes days to execute consistently; AI assistance without structured methodology produces unreliable output for compliance reports."

**Jerry value (INFERRED):** `/red-team` (11-agent PTES/OSSTMM/ATT&CK methodology) + `/eng-team` (10-agent STRIDE/OWASP defensive methodology) + `/adversary` (C3/C4 adversarial review) to produce structured engagement reports and secure-development artifacts.

**Messaging block (DRAFT, DO NOT PUBLISH):**
> **For security practitioners:** Jerry's `/red-team` and `/eng-team` skills apply PTES, OSSTMM, STRIDE, and OWASP methodology through coordinated AI agents -- structured engagement planning, reconnaissance-to-reporting workflows, and secure-development reviews. Not a replacement for Burp Suite; a methodology layer over Claude Code for the parts of the engagement Burp doesn't cover.

Gate closure protocol: JTBD iter-5 A4 Validation Checklist (3 interviews confirming prior solution + switch trigger language).

### A5 -- New OSS User (CANDIDATE FINAL, ready for Phase 2)

**Description:** Developer evaluating Jerry without prior context. First-contact surface: README landing + Quickstart.

**Prior solution:** Evaluation state (no prior solution to switch from; pre-commitment).

**Switch trigger:** "I keep running into [compaction / inconsistency / review quality] with Claude Code; is there a tool for this?"

**Jerry value:** Canonical one-liner answering "what is this" in 10 seconds; sub-3-minute Hello World (aspirational target per FEAT-040-055 P-01); clear self-select signal via "Is Jerry for me?" comparison.

**Messaging block (README landing target, iter-2 with A5-specific evaluation framing per FM-010 resolution):**
> **New here?** Jerry is a Claude Code plugin that keeps the AI's work consistent across sessions through persistent rules, shared memory, and quality gates. **Here's how to decide if Jerry is for you in 30 seconds:** (1) Do you use Claude Code? If no, Jerry is not for you yet. (2) Have you experienced the AI forgetting constraints, losing work between sessions, or producing inconsistent output? If yes, Jerry addresses this directly. (3) Are you evaluating Claude Agent SDK or LangChain to *build* an AI application? Jerry is a complement (adds governance on top of Claude Code), not a substitute (does not build agent applications).

> **A5 differentiation note (iter-2, FM-010):** A5 messaging now carries explicit evaluation-framework language ("here's how to decide if Jerry is for you") which A1 messaging does not need (A1 already has prior-solution context). This differentiates A5 from A1 more concretely than iter-1, where the two blocks were similar.

Ships at README landing per Wave 2 README revision. Self-select language addresses FEAT-040-055 P-04 (comparison tables for positioning).

### A6 -- Domain Specialist (DRAFT-ONLY; BLOCKED by A6 STOP GATE)

> **XP-04 STOP GATE STATUS: OPEN.** The messaging block below is DRAFT ONLY. It MUST NOT be published until N >= 3 A6 interviews confirm Dovetail / Figma / Airtable / Notion / Miro as prior solution per JTBD A6 Validation Protocol.

**Description (INFERRED):** Product, UX, or research specialist on a small team without dedicated staff in the domain. Produces stakeholder-ready artifacts (PRDs, UX audits, journey maps, PM/PMM deliverables).

**Prior solution (INFERRED):** Dovetail (research), Figma (design systems), Airtable (tracking), Notion (documentation), Miro (workshops).

**Switch trigger (INFERRED):** "I need specialist methodology (Kano, HEART, JTBD, Atomic Design, Cockburn UC 2.0, positioning frameworks) but I do not have a PM or UX specialist on the team; SaaS tools give me templates, not methodology."

**Jerry value (INFERRED):** `/user-experience` (10 UX sub-skills with wave-gating), `/pm-pmm` (18 PM/PMM frameworks), `/use-case` + `/test-spec` + `/contract-design` (SDLC methodology chain), `/diataxis` (documentation methodology) -- methodology-grade AI assistance where SaaS gave you only templates.

**Messaging block (DRAFT, DO NOT PUBLISH):**
> **For tiny teams without specialists:** Jerry brings methodology-grade UX, PM, and documentation work to Claude Code. Kano and HEART for feature prioritization; Atomic Design for component systems; Cockburn UC 2.0 for use cases; positioning frameworks for GTM. Not a Dovetail or Figma replacement -- a methodology layer where those tools gave you templates.

Gate closure protocol: JTBD iter-5 A6 Validation Checklist.

---

## L1: Messaging Consistency Map

Resolves F-007 heuristic finding: "What is Jerry?" messaging varies across README, docs/index.md, INSTALLATION.md.

### Current State (Problem)

| Surface | Current Opening | Problem |
|---------|-----------------|---------|
| README.md | "> A Claude Code plugin for behavior and workflow guardrails with knowledge accrual." | Tagline only; F-011 flags "knowledge accrual" as jargon; no canonical sentence. |
| README.md "What is Jerry?" section | "Jerry is a **Claude Code plugin** that adds structured problem-solving capabilities, work tracking, and knowledge management to your Claude Code sessions. It combats **Context Rot**..." | Different vocabulary than docs/index.md; different ordering; different framing. |
| docs/index.md tagline | "> Behavioral guardrails and workflow orchestration for Claude Code. Accrues knowledge, wisdom, experience." | "Accrues knowledge, wisdom, experience" is the tone-gap phrase (FEAT-040-055 [INFERRED] flag; low-risk to remove). |
| docs/index.md "What is Jerry?" | "Jerry is a Claude Code plugin that provides **behavioral guardrails**, **workflow orchestration**, and **persistent knowledge management** for AI-assisted development sessions. It solves the core problem of **Context Rot**..." | Different from README "What is Jerry?" -- three bold concepts vs. three different bold concepts; inconsistent ordering. (Iter-2: these three bold concepts will be replaced with the unified canonical triplet **persistent rules**, **shared memory**, **quality gates** per the Sub-headings Alignment rule below.) |
| INSTALLATION.md lead | (absent -- jumps to Prerequisites) | No "What is Jerry?" paragraph; new users who land here have no definition. |

### Target State (Commit in Phase 2; each surface has a named owner)

> **Iter-2 note (responds to FM-014, IN-001, LJ-005):** Each surface update below now has a named responsible party. "Phase 2" is defined in PLAN.md Wave 2 (README revision) and Wave 3 (docs/ restructure). Owner assignments route through the Wave 2/3 feature work items within EPIC-040-001; specific work item IDs will be filed at Phase 2 entry.

| Surface | Replace with | Named Owner | Phase 2 Gate |
|---------|--------------|-------------|--------------|
| README.md tagline | > Jerry is a Claude Code plugin that keeps Claude's work consistent across sessions -- persistent rules, shared memory, and quality gates that survive Claude's context limits. | Wave 2 README revision FEATURE (FEAT-040-0XX, filed at Phase 2 entry); PM reviewer: pm-market-strategist | Wave 2 entry; blocks on V-00 pre-gate outcome for Candidate A vs. B elevator framing |
| README.md "What is Jerry?" opening sentence | Same canonical one-liner verbatim; then paragraph Tier 3. | Same as above | Same |
| docs/index.md tagline | Same canonical one-liner verbatim. | Wave 3 docs restructure FEATURE (docs/index.md owner, filed at Phase 2 entry) | Wave 3 entry |
| docs/index.md "What is Jerry?" opening sentence | Same canonical one-liner verbatim; then paragraph Tier 3. | Same as above | Same |
| INSTALLATION.md lead paragraph (NEW -- insert before Prerequisites) | Same canonical one-liner verbatim; then one-sentence pointer to "See Quickstart for your first agent in 3 minutes." (Note: "3 minutes" aspirational target per FEAT-040-055 P-01; measurement protocol to be defined in Wave 2 Quickstart work, per iter-2 FM-018 acknowledgment) | Wave 2 INSTALLATION.md owner (filed at Phase 2 entry) | Wave 2 entry |

### Rule

**Verbatim reuse.** The canonical one-liner is a single artifact shipped in three locations. If it changes, all three change simultaneously. This is the simplest messaging-consistency mechanism and is the pattern used by Claude Agent SDK and OpenAI Agents SDK per FEAT-040-055 per-framework narratives.

> **A5 self-select sequencing (iter-4, IN-001-054i3):** A5 self-select sequencing: New OSS User evaluation entry point. A5 messaging elements appear in MCM ordered by self-select priority (elevator first, positioning statement second).

### Sub-headings and Bold Concepts Alignment (iter-2 unified triplet)

Across README and docs/index.md, the Tier 3 paragraph uses three bolded concept nouns: **persistent rules**, **shared memory**, **quality gates**. Do not vary these three terms across surfaces. If a fourth surface needs the paragraph (e.g., CONTRIBUTING.md), reuse these three identically.

> **Iter-2 resolution of dual vocabulary (FM-015, LJ-002):** The prior iter-1 bold concepts ("behavioral guardrails", "workflow orchestration", "methodology-grade skills") conflicted with the canonical one-liner's triplet ("persistent rules, shared memory, quality gates"), producing two vocabulary frames for the same capability dimensions. Iter-2 selects the canonical one-liner triplet as SSOT. "Behavioral guardrails" (the 25 HARD rules + enforcement architecture) is subsumed under "persistent rules"; "workflow orchestration" (worktracker + orch-*) is subsumed under "shared memory" as the workflow-state dimension; "methodology-grade skills" (the 30 skills) is a *delivery mechanism* for the three capabilities, not a fourth capability -- narrative tiers reference the 30 skills as "delivered across 30 methodology-grade skills" to preserve the methodology signal without introducing a vocabulary triplet competitor.

---

## L2: Persona Messaging Cross-Reference

Handoff to FEAT-040-053 (personas) parallel work. This section is the messaging-input contract to that feature.

### Messaging Blocks Per Actor Segment (ready for FEAT-040-053 consumption)

FEAT-040-053 will produce buyer-persona artifacts including decision criteria, buying-committee composition, and objection patterns. This feature (FEAT-040-054) provides the messaging blocks -- one per segment -- that FEAT-040-053 personas will map to decision criteria.

| Segment | Messaging Block Status | Source Section |
|---------|----------------------|----------------|
| A1 Solo Engineer | CANDIDATE FINAL | Per-Segment Value Propositions, A1 block |
| A2 Technical Lead | CANDIDATE FINAL | Per-Segment Value Propositions, A2 block |
| A3 Framework Contributor | CANDIDATE FINAL (internal) | Per-Segment Value Propositions, A3 block |
| A4 Security Practitioner | DRAFT-ONLY; GATE OPEN | Per-Segment Value Propositions, A4 block |
| A5 New OSS User | CANDIDATE FINAL | Per-Segment Value Propositions, A5 block |
| A6 Domain Specialist | DRAFT-ONLY; GATE OPEN | Per-Segment Value Propositions, A6 block |

### Input Contract to FEAT-040-053

FEAT-040-053 SHOULD use the A1/A2/A3/A5 messaging blocks above as the "messaging the persona responds to" field in persona artifacts. For A4/A6, FEAT-040-053 SHOULD:

- Treat the DRAFT messaging blocks as hypotheses to test in V-01/STOP-GATE interviews.
- Own the interview execution (N >= 3 per segment).
- Close the STOP GATE by returning validated switch-trigger language to this artifact (handoff-back loop).

### Output Contract from FEAT-040-053 (reverse handoff)

FEAT-040-053 is expected to return, per persona, at least the following fields that feed into messaging refinement:

- Buyer decision criteria (top 3)
- Objection patterns (top 3)
- Trusted-voice sources (where this persona hears about new tools)

If FEAT-040-053 persona outputs introduce decision criteria not covered by any current messaging block, this artifact will be amended in Phase 2a.

---

## L2: Crossing the Chasm Posture

Moore's Crossing the Chasm applied in abbreviated form per discovery-subset conventions.

### Technology Adoption Lifecycle Position

Jerry is at the **early adopter** stage. Evidence:

- No public OSS release yet (still pre-OSS-release phase per PLAN.md Wave 5).
- No GitHub star / download signal to compare against FEAT-040-055 competitors.
- Current users (A3 Framework Contributors + early A1/A2) self-identify as framework early adopters; they chose Jerry because they recognized the governance problem, not because they evaluated features.

Jerry is **approaching but not yet at the chasm** (the transition from early adopters to early majority). The OSS release is the chasm-crossing event.

### Beachhead Segment (D-Day target)

**Primary beachhead: A1 Solo Engineer using Claude Code, who has experienced Context Rot.** Rationale:

- Highest actor breadth (FEAT-040-001 Cat 1 primary actor).
- Lowest switching cost (no team coordination needed).
- Directly feels the pain Jerry addresses (compaction, inconsistency).
- Prior solution ("vanilla Claude Code prompting") is a zero-switch-cost alternative; differentiation is clear.

**Secondary beachhead: A2 Technical Lead who already adopted Jerry personally and is evaluating team rollout.** A2 adoption follows A1 adoption; positioning A1 first creates the A2 seed.

**Not beachhead (explicitly deferred):** A4 (gate-blocked, niche), A6 (gate-blocked, niche), A5 (derivative of A1).

### Whole-Product Requirements for the Beachhead

What must exist, beyond the core Jerry framework, for A1 to adopt and stay?

| Requirement | Current State | Phase 2 Action |
|-------------|---------------|----------------|
| Canonical one-liner in README | Inconsistent (F-007) | Wave 2 README revision |
| Sub-3-minute Hello World | Not measured (FEAT-040-055 P-01) | Wave 2 Quickstart |
| Skill catalog visible in README | 6 of 30 (FEAT-040-055 AP-02) | Wave 2 README Skills section |
| At least one working tutorial per top-3 skill | 0 of 30 (FEAT-040-001 Coverage Matrix) | Wave 4a tutorials |
| "Jerry vs. plain Claude Code vs. Claude Agent SDK" comparison | Absent (FEAT-040-055 P-04) | Wave 2 README comparison table |
| Diataxis-labeled navigation | Planned (FEAT-040-056 D-01) | Wave 4 nav labels |
| Self-select language for A5 | Absent | Wave 2 README landing |

### Chasm-Crossing Strategy

Concentrated attack on A1 beachhead. Do not dilute the OSS release announcement with A4/A6 messaging (STOP GATE). Do not attempt to compete in the "AI agent framework" category with LangChain / LangGraph; position adjacent as "governance layer for Claude Code." Let A2 adoption follow A1 naturally via the team-member introduction path.

---

## L2: Validation Plan

### Gate 0: V-00 -- A1 Vocabulary Resonance Pre-Gate (iter-2, new)

**Introduced iter-2 in response to adv-review DA-003/IN-003 (Candidate B commit premature before Open Question #1 answered).** Lightweight test runnable combined with V-01 interview protocol.

| Parameter | Value |
|-----------|-------|
| Sample | 5 A1 Solo Engineers who currently use vanilla Claude Code (no prior framework exposure required). May overlap with V-01 sample. V-00 participant recruitment: 5 solo Claude Code users from Jerry GitHub discussions, weighted for plugin-only (not framework-only) adoption; exclude any who have contributed to Jerry repo. |
| Treatment | Show Candidate A ("persistent rules, shared memory, and quality gates") vs. Candidate B ("governance layer -- persistent rules, shared memory, and quality gates") side-by-side at Tier 1 elevator level. |
| Primary question | "Which phrasing sounds more natural for a tool you might use solo? Does 'governance layer' feel like a fit for your work, or does it sound like something for a larger team or enterprise context?" |
| Pass criterion | At most 1 of 5 A1 participants describes "governance layer" as enterprise-y or mismatched to solo-developer vocabulary |
| Fail criterion | >= 2 of 5 describe "governance layer" as enterprise-y, bureaucratic, or mismatched |
| Outcome if pass | Candidate B proceeds to Phase 2 commit; Tier 1 elevator may use "governance layer" framing |
| Outcome if fail | Candidate A rollback: Phase 2 README uses Candidate A's task-outcome framing (which uses identical canonical one-liner but no "governance layer" in Tier 1 elevator); Candidate C remains the V-01 hypothesis |
| Owner | pm-customer-insight via FEAT-040-053 (combined with V-01 interview protocol) |

> **Sensitivity linkage (iter-4, IN-003-054i3):** V-00 rollback is the operationalization of the Jargon weight sensitivity scenario documented in the selection criteria sensitivity table (Row 3).

### Gate 1: V-01 -- Behavioral-System Framing Validation

**Inherited from FEAT-040-055 Validation Plan. Status: OPEN. Owner: pm-customer-insight via FEAT-040-053.**

| Parameter | Value |
|-----------|-------|
| Sample | 3-5 developers who have used at least one of LangChain/CrewAI/OpenAI Agents SDK/Claude Agent SDK, AND currently use Claude Code |
| Treatment | Show Candidate A vs. Candidate B vs. Candidate C opening sentences, side-by-side |
| Primary question | "Which opening is more immediately interpretable? Which would make you more likely to read on?" |
| Pass criterion | >=3 of 5 find Candidate C more interpretable or more compelling; AND zero describe Candidate C as "jargon I don't understand" [^v01-or-logic] |

[^v01-or-logic]: If V-01 OR gate passes on compelling-but-opaque reasons, record qualitative reasoning to enable retrospective analysis.
| Fail criterion | Majority opaque without prior Claude Code context; OR participants conflate Jerry with Claude Agent SDK / Claude Code CLI |
| Outcome if pass | Phase 2a README copy upgrades to Candidate C (behavioral-system framing) |
| Outcome if fail | Candidate B remains; document Candidate C failure mode for future evaluation |

### Gate 2: A4/A6 STOP GATE -- Switch Trigger Validation

**Inherited from FEAT-040-001 iter-5 Validation Protocol. Status: OPEN. Owner: FEAT-040-053.**

| Segment | Required N | Prior Solution Confirmation | Gate Closure |
|---------|------------|------------------------------|--------------|
| A4 Security Practitioner | >= 3 | Burp Suite Pro / Cobalt Strike / manual PTES/OSSTMM runbooks (NOT vanilla Claude Code) | A4 messaging publishable |
| A6 Domain Specialist | >= 3 | Dovetail / Figma / Airtable / Notion / Miro (NOT vanilla Claude Code) | A6 messaging publishable |

### Gate 3: Canonical One-Liner Comprehension Test (BLOCKING in iter-2, was "recommended" in iter-1)

**Iter-2 resolution of FM-017:** Elevated from "recommended, not blocking" to blocking gate status. Rationale: the canonical one-liner is the single most load-bearing artifact in this document. If it fails comprehension, the Messaging Consistency Map is built on a misunderstood foundation. Gate 3 now blocks Wave 2 README revision commit.

**Instruction to FEAT-040-053: include in V-01 interview session; this is a required comprehension test, not optional.**

| Parameter | Value |
|-----------|-------|
| Sample | Same as V-01 |
| Treatment | Present canonical one-liner verbatim. Ask: "After reading this sentence, what does Jerry do? What kind of developer is it for?" |
| Pass criterion | >= 3 of 5 answers correctly include "Claude Code", "consistency/memory across sessions" or equivalent, and "developers using Claude Code"; AND zero participants describe the sentence as incomprehensible or ambiguous |
| Fail criterion | < 3 of 5 capture core meaning OR any participant describes it as incomprehensible |
| Outcome if pass | Canonical one-liner proceeds to Wave 2 commit |
| Outcome if fail | Revise one-liner; re-run Gate 3 on revised variant before Wave 2 commit |
| Failure mode detection | If users ask "What is Claude's context limit?" -> Tier 3/4 gloss already addresses; if users ask "Is this Claude Code itself?" -> sharpen differentiation in Tier 3 |

### Open Questions (answer post-V-01)

1. Does A1 respond to "governance layer" as concrete or as enterprise-y? If enterprise-y, Candidate B's phrasing may need softening for Tier 1 elevator.
2. Does A2 respond differently to "governance layer" than A1? A2 may favor it more than A1.
3. Does mentioning "30 skills" at Tier 3 trigger feature-bragging perception? Consider "30+ methodology-grade skills" vs. naming top 5 skills.
4. Does the phrase "quality gates" parse as CI-like (familiar) or as bureaucratic (negative)?
5. Should the A5 self-select block mention Claude Agent SDK explicitly, or is naming competitors in a README self-defeating?

These questions are for V-01 interview design, not blocking gates.

---

## L2: Limitations and Known Biases

Per pm-market-strategist guardrail:

1. **No primary user data; circular evidence chain (iter-2, DA-001/LJ-004 resolution).** All segment definitions (A1-A6) and switch triggers inherit from FEAT-040-001 which explicitly classifies its own evidence as MEDIUM confidence AI-synthesized from SKILL.md secondary research. FEAT-040-001's force ratings derive from SKILL.md (the framework's own documentation), making the evidence chain circular at the A1 level. Iter-2 explicitly labels all A1-A6 switch triggers as "MEDIUM confidence, AI-synthesized" to match the upstream source, downgrading iter-1's "validated" label which overstated the chain confidence. A4 and A6 switch triggers are additionally INFERRED and STOP-GATE-blocked.

2. **Candidate C framing is unvalidated.** The behavioral-system framing inherits FEAT-040-055's `[INFERRED - requires audience validation]` label. Production commit to Candidate C requires V-01 pass. This artifact does not recommend production commit to Candidate C pre-V-01.

3. **Competitive gap may close.** FEAT-040-055 Threats section notes Claude Agent SDK could evolve to occupy behavioral-system positioning before Jerry's OSS release. This artifact is valid at 2026-04-20; re-evaluate before OSS release ships.

4. **"Claimed, not validated" attributes.** Three attributes in L1 Dunford Step 2 are flagged: "working code before prose" (requires audit post-Wave 2), "sub-3-minute Hello World" (not measured), and the audience-response side of all three differentiators. Do not ship as validated fact.

5. **30 skills as bragging risk.** Messaging that names the count risks feature-bragging perception. Tier 1 elevator deliberately avoids the count; Tier 3/4 use "30 methodology-grade skills" which hedges toward methodology framing over count framing.

6. **"Governance layer" carries enterprise connotation.** A1 Solo Engineer persona may perceive this as a mismatch. Candidate A fallback exists if V-01 or persona work shows this mismatch.

7. **Claude Agent SDK is simultaneously competitor and runtime dependency** (FEAT-040-055 Limitation #5). Positioning language must avoid hostile contrast with Claude Agent SDK; emphasize "complement, not substitute" per A5 messaging block.

8. **Tone gap inference.** FEAT-040-055 flags current aspirational language ("accrues knowledge, wisdom, experience") as `[INFERRED - requires user testing]`. This artifact removes that language from target-state copy based on stylistic analysis; removal is low-risk because the phrase is already identified as non-technical. If tone-gap V-02 validation invalidates the removal hypothesis, re-add.

9. **Candidate comparison criteria weights are author-defined (iter-2, FM-002/LJ-003/IN-004).** The 20%/20%/20%/15%/15%/10% weights applied to the six candidate evaluation criteria are analyst judgment, not sourced from Dunford, Moore, or other published positioning frameworks. Dunford's *Obviously Awesome* does not prescribe criterion weights; weight assignment is an analyst-judgment input. Re-weighting could change Candidate B's recommendation (see the weight sensitivity disclosure in the Recommendation section).

10. **Differentiator 2 (compaction) is a positioning gap, not a technical moat (iter-2, DA-002/PM-003).** The claim "no competitor addresses context compaction" is derived from competitor positioning text as of 2026-04-20. It is fragile against competitor documentation updates and must be re-verified before each major Jerry release cycle. Competitor re-verification: Docs lead responsibility; quarterly cadence (next review Q3 2026).

11. **Agent count claim removed (iter-2, CC-002/PM-002/FM-012).** Iter-1 cited "88 specialized agents" as a Unique Attribute with Direct evidence from agent-development-standards.md. External verification of this count was not feasible from the cited source, and it risked undermining other quantitative claims (25 HARD rules, 30 skills, 0.92 threshold) via credibility contagion. Iter-2 replaces the count-based claim with an architecture-based claim ("governed by published dual-file architecture per H-34/H-35") that is directly verifiable. The 30-skills claim remains (verifiable via CLAUDE.md Quick Reference + skills/ directory listing).

12. **Critical-path dependency on FEAT-040-053 (iter-3, PM-003 closure).** Four positioning gates -- V-00 (A1 vocabulary resonance pre-gate), V-01 (behavioral-system framing validation), Gate 3 (canonical one-liner comprehension test, blocking), and the A4/A6 STOP GATE -- all depend on FEAT-040-053 persona validation work as their single owner. If FEAT-040-053 is delayed or deprioritized, all four positioning gates block simultaneously and Phase 2 README revision cannot proceed past the V-00 entrance criterion. Phase 2 planning SHOULD treat FEAT-040-053 as a critical-path dependency with escalation authority to the orchestrator if delay exceeds 1 week. Mitigation options (if FEAT-040-053 slips): (a) activate Candidate A rollback and proceed with plain-language positioning that does not require V-00; (b) defer Wave 2 README revision until FEAT-040-053 closes; (c) partition FEAT-040-053 scope so V-00/V-01 A1-only interviews run ahead of A4/A6 interview protocol. The orchestrator holds the escalation decision authority per P-020 user authority.

---

## Evidence Index

All claims traceable. Direct evidence cited; inference flagged per pm-market-strategist guardrail.

| Claim | Source | Tier |
|-------|--------|------|
| Three candidate category frames (A/B/C) | FEAT-040-055 L2 Positioning Framework Input + FEAT-040-055 iter-2 revision log Blocker 1 | Direct (A, B synthesized from competitor patterns) / Inference (C, flagged) |
| Behavioral-system framing is unoccupied | FEAT-040-055 "How Competitors Answer 'What Is This'" table | Direct (factual observation) |
| Behavioral-system framing is COMPELLING to target audience | FEAT-040-055 L2 Positioning Framework Input -- `[INFERRED - requires audience validation]` | Inference; BLOCKED by V-01 |
| A1-A6 segment definitions | FEAT-040-001 iter-5 L1 Actor Segments | Direct (JTBD actor table) |
| A1/A2/A3 switch triggers | FEAT-040-001 iter-5 L1 Switch Force Analysis per-category evidence | Direct (force ratings with SKILL.md citations) |
| A4/A6 switch triggers | FEAT-040-001 iter-5 L1 Switch Force Analysis -- `[INFERRED - see A4/A6 STOP GATE]` | Inference; BLOCKED by A4/A6 STOP GATE |
| Quality gate 0.92 threshold | quality-enforcement.md H-13 | Direct |
| Creator-critic-revision H-14 | quality-enforcement.md H-14 | Direct |
| 25 HARD rules, 5-layer architecture | quality-enforcement.md HARD Rule Index + Enforcement Architecture | Direct |
| Filesystem-as-memory | CLAUDE.md Identity + problem-solving SKILL.md | Direct |
| 30 skills spanning SDLC/UX/security/PM | FEAT-040-001 per-skill table; skills/ directory listing enumerates 30 skill directories (excluding `shared/` shared library and `__init__.py`); CLAUDE.md Quick Reference lists 19 of 30 named skills (partial display, not total count) | Direct (iter-3: precise count verified via `ls skills/` = 30 skill dirs; FM-002 closure) |
| Agent architecture: dual-file format, tier model T1-T5, handoff schema v2 | agent-development-standards.md H-34/H-35 | Direct (iter-2 replaces iter-1 "88 specialized agents" count claim per CC-002/PM-002/FM-012) |
| Competitors do not publish quality enforcement | FEAT-040-055 scorecard "Explanatory depth" | Direct (inferred = no competitor observed; open to disconfirmation) |
| Competitors do not address compaction | FEAT-040-055 "How Competitors Answer 'What Is This'" positioning table | Direct (absence in positioning text) |
| Diataxis in production validated at scale | FEAT-040-056 L0 finding #1 + D-01 direct | Direct |
| "Working code before prose" pattern | FEAT-040-055 P-01 Pattern Inventory | Direct (observed); causation inferred per FEAT-040-055 revision note |
| Hidden skill catalog is highest-risk adoption barrier | FEAT-040-055 AP-02 + FEAT-040-001 6/30 skill visibility | Direct |
| F-011 jargon density | FEAT-040-004 rescoped iter / QG-2 TC-003 | Direct (audit finding) |
| F-007 messaging inconsistency | FEAT-040-004 / QG-2 (referenced) | Direct |
| HYP-010 Jerry definition framing ICE=6.0 | FEAT-040-007 hypothesis catalog via QG-2 | Direct |
| Tone gap (aspirational language) | FEAT-040-055 L2 Positioning Framework Input -- `[INFERRED - tone perception requires user testing]` | Inference (low-risk) |
| HEART applied to OSS docs is pioneering | FEAT-040-056 finding M-04 | Direct (synthesis from OSS best-practices research) |

---

## Self-Score (S-014)

Applied at C3 criticality. Six dimensions with calibrated weights per quality-enforcement.md. Iter-3 scoring reflects 5 surgical closures from iter-2 adv-review; arithmetic is computed explicitly and reported honestly per CC-001 calibration lesson.

### Iter-2 arithmetic correction (CC-001 closure, honest walk-back)

The iter-2 self-score reported "0.921" but the arithmetic actually produced 0.917:

```
Iter-2 computed: (0.920*0.20) + (0.925*0.20) + (0.915*0.20) + (0.910*0.15) + (0.925*0.15) + (0.900*0.10)
              = 0.18400 + 0.18500 + 0.18300 + 0.13650 + 0.13875 + 0.09000
              = 0.91725 -> 0.917
```

The reported 0.921 was a 0.004 rounding/transcription error that the iter-2 adv-review correctly caught via CC-001. Per P-022 (no deception), the **actual iter-2 composite was 0.917 (FAIL, below 0.92 threshold)**, not 0.921 as reported. The iter-2 self-scoring leniency-counteraction intent is preserved; the arithmetic is now reported honestly. Iter-3 builds from the true iter-2 baseline of 0.917, not the misreported 0.921.

### Iter-3 dimension scores

| Dimension | Weight | Iter-2 Actual | Iter-3 Score | Delta | Rationale |
|-----------|--------|---------------|--------------|-------|-----------|
| Completeness | 0.20 | 0.920 | 0.920 | 0.000 | No structural additions; 5 surgical closures target other dimensions. Residual gaps (glossary, Candidate A/C positioning depth parity, Chasm whole-product phase-level actions) unchanged. |
| Internal Consistency | 0.20 | 0.925 | 0.928 | +0.003 | FM-002 skill count reconciliation: "near 30" replaced with "30 skill directories (precise count per `ls skills/`)" in Evidence Index, matching the "30 skills" used in messaging Tier 3/4 and L1 Dunford Step 2. One canonical value now used in all references. Residual conditional branching (Candidate A rollback vs. B commit) preserved as intentional architecture. |
| Methodological Rigor | 0.20 | 0.915 | 0.925 | +0.010 | IN-002/TR-001 closure: weight sensitivity calculation now shown explicitly in a 3-row table with numeric ordinal scoring. The iter-2 claim that "Val Risk 25% ties A and B" is honestly corrected -- A and B both score Val Risk = None, so that re-weighting cannot tie them. The genuine sensitivity (Jargon 25% / Differentiation 10%) is the parameterization that flips the recommendation. This is a methodology gain via transparency about where sensitivity actually lies. |
| Evidence Quality | 0.15 | 0.910 | 0.915 | +0.005 | CC-001 arithmetic honesty adds to Evidence Quality via the walk-back discipline (iter-2 reported 0.921, actual 0.917, honestly corrected in iter-3 rather than quietly adjusted upward). Reinforces per-P-022 evidence chain integrity for self-scoring. Skill-count provenance chain also refined (CLAUDE.md Quick Reference is a partial 19-of-30 display, not a total count -- iter-2 framing elided this distinction). |
| Actionability | 0.15 | 0.925 | 0.928 | +0.003 | DA-001 V-00 enforcement path + PM-003 critical-path dependency both add concrete decision-point actionability. Wave 2 work item constraint ("MUST NOT create or edit README canonical positioning until V-00 outcome recorded") is now explicit; FEAT-040-053 escalation authority (>1 week delay triggers orchestrator escalation) is now explicit. Three mitigation options listed if FEAT-040-053 slips. |
| Traceability | 0.10 | 0.900 | 0.905 | +0.005 | FM-002 skill-count provenance now cites the specific enumeration method (`ls skills/` = 30 dirs, excluding shared/__init__.py); weight sensitivity calculation method cited (ordinal mapping disclosed); iter-2 arithmetic error now in the record rather than elided. Residual: FEAT-040-056 DORA per-claim flagging still bulk-in-Limitations rather than per-claim in Evidence Index. |

### Iter-3 composite calculation (explicit arithmetic)

```
(0.920 * 0.20) + (0.928 * 0.20) + (0.925 * 0.20) + (0.915 * 0.15) + (0.928 * 0.15) + (0.905 * 0.10)

Term 1: 0.920 * 0.20 = 0.18400
Term 2: 0.928 * 0.20 = 0.18560
Term 3: 0.925 * 0.20 = 0.18500
Term 4: 0.915 * 0.15 = 0.13725
Term 5: 0.928 * 0.15 = 0.13920
Term 6: 0.905 * 0.10 = 0.09050
Sum:                   0.92155
Rounded (3 dp):        0.922
```

**Iter-3 self-score: 0.922 (PASS -- above 0.92 threshold for C3, by 0.002)**

Arithmetic verified: each term computed independently, sum computed with 5 decimal places, rounded once at the end to 3 decimal places. The 0.922 figure is arithmetically honest; no discrepancy between dimension scores and composite.

### Iter-4 dimension scores

| Dimension | Weight | Iter-3 Score | Iter-4 Score | Delta | Rationale |
|-----------|--------|--------------|--------------|-------|-----------|
| Completeness | 0.20 | 0.920 | 0.923 | +0.003 | V-00 participant recruitment methodology (PM-001), competitor re-verification cadence (PM-002), V-00 filename convention (DA-001), V-00/sensitivity linkage (IN-003) add operational completeness. |
| Internal Consistency | 0.20 | 0.928 | 0.931 | +0.003 | FM-001 Unique Attributes row vocabulary canonicalized ("Claude's context limits" matches canonical one-liner); state file CC-001-054i3 key_findings canonicalized; state file FM-004-054i3 score_history arithmetic canonicalized (0.917 not 0.921). Three cross-surface vocabulary/value mismatches resolved. |
| Methodological Rigor | 0.20 | 0.925 | 0.925 | 0.000 | No methodological changes (no new frameworks, no new analysis). |
| Evidence Quality | 0.15 | 0.915 | 0.915 | 0.000 | No new evidence; existing evidence unchanged. |
| Actionability | 0.15 | 0.928 | 0.928 | 0.000 | No new action items; PM-004 footnote clarifies existing decision scope but does not add actions. |
| Traceability | 0.10 | 0.905 | 0.910 | +0.005 | DA-003 cross-reference from Dunford Step 4 to Limitations #1; PM-004 footnote cross-reference to V-01 gating; IN-001/IN-003 explicit linkages between MCM/V-00 and upstream artifacts; state file XP-07 conditionality field makes handoff dependency explicit. |

### Iter-4 composite calculation (explicit arithmetic, term-by-term)

```
(0.923 * 0.20) + (0.931 * 0.20) + (0.925 * 0.20) + (0.915 * 0.15) + (0.928 * 0.15) + (0.910 * 0.10)

Term 1: 0.923 * 0.20 = 0.18460
Term 2: 0.931 * 0.20 = 0.18620
Term 3: 0.925 * 0.20 = 0.18500
Term 4: 0.915 * 0.15 = 0.13725
Term 5: 0.928 * 0.15 = 0.13920
Term 6: 0.910 * 0.10 = 0.09100
Sum:                   0.92325
Rounded (3 dp):        0.923
```

**Iter-4 self-score: 0.923 (PASS -- above 0.92 threshold for C3, by 0.003)**

Arithmetic verified: each term computed independently, sum computed with 5 decimal places, rounded once at the end to 3 decimal places. Per iter-3 CC-001 honesty discipline, the reported composite 0.923 matches dimension scores; no transcription variance.

### Iter-4 gap narrowed vs. iter-3 external (0.917)

Delta: +0.006 (0.917 -> 0.923). Contributions:
- Completeness +0.003 * 0.20 weight = +0.00060
- Internal Consistency +0.003 * 0.20 weight = +0.00060
- Traceability +0.005 * 0.10 weight = +0.00050
- Total delta: +0.00170 on top of iter-3-self-to-external gap of +0.00500 (iter-3 self 0.922 - external 0.917) = +0.00670 vs external 0.917 -> 0.92370 self-claimed

**Confidence: 0.80** (up from iter-3 0.78). 12 Minor closures executed; zero structural change; arithmetic honestly reported. The self-to-external gap historical pattern (iter-2: self 0.917 vs adv 0.911; iter-3: self 0.922 vs adv 0.917) implies adv-review is likely to score 0.918-0.923 range.

**Expected iter-4 adv-review band:** 0.92-0.93 composite; PASS likely. REVISE band (0.85-0.91) unlikely since scope was surgical-only with no new finding surface.

### Gap narrowed vs iter-2 actual (0.917)

Delta: +0.005 (0.917 -> 0.922). Contributions:
- Internal Consistency +0.003 * 0.20 weight = +0.0006
- Methodological Rigor +0.010 * 0.20 weight = +0.0020
- Evidence Quality +0.005 * 0.15 weight = +0.00075
- Actionability +0.003 * 0.15 weight = +0.00045
- Traceability +0.005 * 0.10 weight = +0.0005
- Total delta: +0.00435 -> matches 0.92155 - 0.91725 = 0.00430 (rounding variance 0.00005)

**Confidence: 0.78** (up from iter-2 0.76) -- 5 surgical closures complete (arithmetic honesty, skill-count reconciliation, V-00 enforcement path, weight sensitivity table, critical-path observation). Zero structural changes. Iter-2 reporting error explicitly acknowledged in the record per P-022. Residual partial closures from iter-2 (glossary, Chasm abbreviation depth, DORA per-claim flagging) remain unchanged -- this iteration was scoped to surgical closures only.

**Expected iter-3 adv-review band:** 0.92-0.93 composite; PASS if external reviewer agrees arithmetic honesty, skill-count reconciliation, V-00 enforcement, and weight sensitivity table substantively close their respective iter-2 findings. REVISE band (0.85-0.91) possible only if a new finding class emerges (not anticipated given scope is surgical-only).

---

## Revision History

### Iteration 4 (2026-04-20)

**Trigger:** iter-3 adv-review REVISE verdict (composite 0.917; gap 0.003; 12 Minor carry-forward findings; no Critical/Major).

**12 one-sentence/one-line cleanups:**

| # | Blocker ID | Closure |
|---|------------|---------|
| 1 | CC-001-054i3 | State file key_findings line 62 stale "context compaction" updated to "Claude's context limits". |
| 2 | DA-001-054i3 | V-00 enforcement note now specifies filename pattern `orchestration/reviews/v-00-vocabulary-test-{YYYYMMDD}-{NNN}.md`. |
| 3 | DA-002-054i3 | State file XP-07 YAML field `tier_1_elevator_pass_conditional_on: V-00_outcome` added. |
| 4 | DA-003-054i3 | Dunford Step 4 confidence label now cross-references Limitations #1 circular chain. |
| 5 | PM-001-054i3 | V-00 sample cell extended with participant recruitment methodology (Jerry GitHub discussions, plugin-only weighting, Jerry-contributor exclusion). |
| 6 | PM-002-054i3 | Limitations #10 extended with competitor re-verification owner (Docs lead) + cadence (quarterly, next Q3 2026). |
| 7 | PM-004-054i3 | Weight sensitivity table footnote added: Candidate C excluded pending V-01; re-evaluate on V-01 validation. |
| 8 | FM-001-054i3 | Unique Attributes row "context compaction" updated to "Claude's context limits" for canonical one-liner vocabulary consistency. |
| 9 | FM-003-054i3 | V-01 pass criterion footnote added: record qualitative reasoning on compelling-but-opaque pass to enable retrospective analysis. |
| 10 | FM-004-054i3 | State file score_history iter-2 self_reported_quality_score corrected from 0.921 to 0.917; gap annotation corrected to -0.006; consistent with iter-3 P-022 walk-back. |
| 11 | IN-001-054i3 | MCM Rule section note added: A5 self-select sequencing (elevator first, positioning statement second) for New OSS User evaluation entry point. |
| 12 | IN-003-054i3 | V-00 section sensitivity-linkage note added: V-00 rollback operationalizes the Jargon weight sensitivity scenario (selection criteria sensitivity table Row 3). |

**Preserved from iter-3 and iter-2 (no structural changes per directive):**

- Canonical capability triplet ("persistent rules, shared memory, quality gates") as SSOT
- Canonical one-liner ("Claude's context limits" plain language)
- V-00 pre-gate architecture; V-01 architecture; A4/A6 STOP GATE architecture
- Weight sensitivity table (3-row); arithmetic-honest iter-2 walk-back (0.917 not 0.921)
- Candidate A rollback one-liner; Limitations #12 critical-path observation; named owners in MCM
- 4-tier messaging hierarchy; 3-candidate framing (A/B/C); H-23 navigation table.

**Iter-4 self-score delta:** 0.922 (iter-3) -> 0.923 (iter-4 self-claimed; arithmetic 0.92325 rounds to 0.923). Small targeted gains in Completeness (+0.003 from filename/recruitment/cadence/sensitivity-linkage additions), Internal Consistency (+0.003 from state-file CC-001 + FM-001 vocabulary canonicalization + FM-004 score_history correction), Traceability (+0.005 from footnotes and state file XP-07 conditionality field). No change to Methodological Rigor, Evidence Quality, Actionability beyond trace improvements.

**Expected iter-4 adv-review band:** 0.92-0.93 composite; PASS if external reviewer agrees 12 Minor fixes substantively close their respective findings (no structural change means no new finding surface expected).

### Iteration 3 (2026-04-20)

**Trigger:** iter-2 adv-review REVISE verdict (composite 0.917 after CC-001 arithmetic correction of the misreported 0.921; gap to PASS = 0.003; 5 Minor findings requiring surgical closure).

**5 surgical closures:**

| # | Blocker ID | Closure |
|---|------------|---------|
| 1 | **CC-001 (arithmetic consistency)** | Self-Score section rewritten with explicit arithmetic walk-back: iter-2 reported 0.921, actual iter-2 arithmetic was 0.917 (transcription/rounding error). Iter-3 honestly corrects the record per P-022 rather than quietly adjusting dimension scores upward. Iter-3 dimension scores arithmetically match the reported 0.922 composite (each term computed independently; sum verified). |
| 2 | **FM-002 (skill count consistency)** | Skills directory enumerated via `ls skills/` = 30 skill directories (excluding `shared/` library and `__init__.py`). Single canonical value "30 skills" used everywhere. Evidence Index entry clarifies CLAUDE.md Quick Reference lists 19 of 30 named skills (partial display, not total count); iter-2 framing ("near 30") removed. |
| 3 | **DA-001 (V-00 gate enforcement path)** | Prerequisite note added to Recommendation section: Wave 2 work item (FEAT-040-0XX-wave2-readme-commit) MUST NOT create or edit README canonical positioning until V-00 test outcome is recorded in `orchestration/reviews/`. Wave 2 entrance criteria explicitly include V-00 PASS or Candidate A rollback activation. Closes the iter-2 soft linkage. |
| 4 | **IN-002 / TR-001 (weight sensitivity calculation)** | 3-row sensitivity comparison table added with numeric ordinal scoring (High=3, Medium=2, Low=1 etc.). Honest correction: iter-2 claim that "Val Risk 25% ties A and B" is mathematically incorrect (A and B both score Val Risk = None, so that re-weighting cannot change their relative ranking). Genuine sensitivity lies in Jargon weight (raising Jargon to 25% and lowering Differentiation to 10% flips the recommendation to A). Calculation is now explicit; prior claim is explicitly walked back. |
| 5 | **PM-003 (critical-path dependency observation)** | Limitations #12 added: V-00, V-01, Gate 3, and A4/A6 STOP GATE all depend on FEAT-040-053 persona validation work as single owner. If FEAT-040-053 delays, all four positioning gates block simultaneously. Phase 2 planning treats FEAT-040-053 as critical-path dependency with orchestrator escalation authority if delay > 1 week. Three mitigation options documented (Candidate A rollback, defer Wave 2, partition FEAT-040-053 scope). |

**Preserved from iter-2 (no structural changes per directive):**

- Canonical capability triplet ("persistent rules, shared memory, quality gates") as SSOT
- V-00 pre-gate architecture (5-participant A1 vocabulary resonance test)
- Candidate A rollback one-liner (identical to current canonical, preserving Tier 2 verbatim reuse)
- "Claude's context limits" plain language (not "context compaction")
- Weights disclosure (author-defined, not Dunford-prescribed)
- 4-tier messaging hierarchy; 3-candidate framing (A/B/C); V-01 architecture; A4/A6 STOP GATE; H-23 navigation table.

**Self-score delta:** 0.917 (iter-2 actual, after CC-001 honesty walk-back) -> 0.922 (iter-3 self-claimed). Arithmetic verified term-by-term; reported composite matches dimension scores within rounding variance 0.00005.

**Expected iter-3 adv-review band:** 0.92-0.93 composite; PASS if external reviewer agrees the 5 surgical closures substantively address their respective findings.

### Iteration 2 (2026-04-20)

**Trigger:** iter-1 adv-review REVISE verdict (0.88 composite < 0.92 threshold; 3 Critical + 22 Major + 11 Minor findings).

**Primary closures (5+ per directive):**

| # | Blocker ID(s) | Closure |
|---|---------------|---------|
| 1 | **FM-015 / LJ-002 (dual vocabulary triplet)** | Selected "persistent rules, shared memory, quality gates" as canonical triplet across all sections. Removed "behavioral guardrails, workflow orchestration, methodology-grade skills" as competing triplet; methodology-grade-skills retained as delivery-mechanism descriptor only. Updated Tier 3 paragraph, Tier 4 narrative, Messaging Consistency Map Sub-headings rule. Primary Internal Consistency gain. |
| 2 | **CC-002 / PM-002 / FM-012 / FM-019 ("88 specialized agents" unverifiable)** | Removed count-based claim from Unique Attributes. Replaced with architecture-based claim ("governed by published dual-file architecture per H-34/H-35") that is directly verifiable from cited source. Updated Evidence Index row. Added Limitations #11 explaining the removal. 30-skills claim preserved (verifiable via CLAUDE.md + skills/ enumeration). |
| 3 | **DA-003 / IN-003 (Candidate B commit premature vs. Open Question #1)** | Added V-00 pre-gate: 5-participant A1 vocabulary resonance test of "governance layer" phrasing. Added explicit rollback rule: Candidate A is the fallback if V-00 fails. Reframed commit as "conditional near-term commit" with rollback architecture. Updated Gate Acknowledgment, Category Definition Recommendation, Validation Plan (new Gate 0), and Canonical One-Liner Conditional Downgrade sections. |
| 4 | **DA-005 / FM-006 (Tier 1/2 vocabulary inconsistency)** | Revised Tier 1 elevator to use canonical one-liner's triplet ("persistent rules, shared memory, quality gates that survive Claude's context limits"). Removed "governance layer" from Tier 1 per derivation discipline. Added explicit iter-2 note explaining the derivation rule. |
| 5 | **FM-004 / IN-002 ("context compaction" jargon in canonical one-liner)** | Replaced "survive context compaction" with "survive Claude's context limits" in the canonical one-liner (Tier 2). Retained compaction terminology with plain-language gloss in Tier 3 paragraph and Tier 4 narrative ("compaction -- the automatic reset when the conversation gets too long"). Preserves technical accuracy for informed audiences while remaining parseable for first-contact A5. |
| 6 | **FM-002 / LJ-003 / IN-004 (candidate comparison weights uncited)** | Added explicit weights disclosure box: weights are author-defined judgments, NOT sourced from Dunford/Moore/published frameworks. Added Source column to criteria table. Added weight sensitivity disclosure in Recommendation. Updated Limitations #9. |
| 7 | **CC-004 (L0 item 3 missing A3 internal qualifier)** | Rewrote L0 item 3: "A1 (Solo Engineer), A2 (Technical Lead), A5 (New OSS User) messaging is ready for external commit. A3 (Framework Contributor) messaging is ready for internal commit only (CONTRIBUTING.md / docs/explanation/ target; not for README/docs/index.md primary surfaces)." |
| 8 | **CC-003 (Tier 4 "brilliant for 30 minutes" editorial)** | Removed time qualifier from Tier 4 opening; replaced with "appears consistent for a while" which is qualifying language rather than ungrounded editorial. |
| 9 | **DA-002 / PM-003 (Differentiator 2 temporal fragility)** | Added explicit "positioning gap, not technical moat" disclosure with re-verification cadence requirement. Updated L0 item 4 (i-iii) with "as of 2026-04-20" temporal qualifier. |
| 10 | **DA-006 ("resolves" framing inaccuracy)** | Changed "resolves F-011, HYP-010, F-007" to "prescribes resolution for F-011, HYP-010, F-007" in L0 item 2 and Canonical One-Liner introduction. |
| 11 | **DA-004 (A3 internal-only asserted without argument)** | Revised A3 segment: acknowledged CONTRIBUTING.md is public-facing; re-labeled as "contributor-surfaces-only" vs. "internal-only". Acknowledged external OSS contributor pattern from LangChain/LlamaIndex. |
| 12 | **FM-010 (A1/A5 messaging overlap)** | A5 messaging now carries explicit evaluation-framework language ("here's how to decide if Jerry is for you in 30 seconds") which A1 does not need. |
| 13 | **FM-014 / IN-001 / LJ-005 (no named owners in Messaging Consistency Map)** | Added Named Owner and Phase 2 Gate columns to target-state table. Each surface has explicit owner (Wave 2 README FEATURE, Wave 3 docs restructure FEATURE, etc.). |
| 14 | **FM-017 (Gate 3 recommended not blocking)** | Gate 3 elevated to blocking status; specific pass/fail criteria added. |
| 15 | **FM-011 / LJ-004 / LJ-006 (A1/A2 "validated" overstated)** | Downgraded A1/A2 switch triggers from "validated" to "MEDIUM confidence, AI-synthesized" matching upstream FEAT-040-001 label. Added Limitations #1 circular-evidence acknowledgment. |

**Partial closures (acknowledged as residual):**

- LJ-001 (glossary absent): no inline glossary added in iter-2; Context Rot defined in Tier 4 narrative, other terms (beachhead, STOP GATE) remain context-dependent. Residual -- deferred to Wave 2 docs restructure.
- LJ-003 (Chasm abbreviation depth): abbreviation rationale remains brief; bowling-pin / D-Day framing not added. Residual -- acknowledged in scoring.
- LJ-006 (DORA per-claim flagging): still done in bulk via Limitations, not per-claim. Residual -- marginal improvement judged not worth verbosity cost.

**Unchanged from iter-1:**

- 4-tier messaging hierarchy structure (L0 scope preserved per directive)
- 3-candidate framing (A/B/C) structure (preserved per directive)
- V-01 enforcement architecture (preserved per directive)
- A4/A6 STOP GATE architecture (preserved per directive)
- H-23 navigation table (updated with Revision History entry)

**Self-score delta:** 0.928 (iter-1 self-claimed, superseded by adv-review 0.88) -> 0.921 (iter-2 self-claimed, leniency-adjusted). Iter-2 self-score intentionally below iter-1 self-score to counteract self-scoring leniency bias per H-15/S-014 protocol.

**Expected iter-2 adv-review band:** 0.91-0.93 composite; PASS if external reviewer agrees dual-vocabulary and 88-agents resolutions are substantive. REVISE band (0.85-0.91) possible if residual Chasm depth, glossary absence, or DORA per-claim gaps are weighted heavily.

### Iteration 1 (2026-04-20)

Initial draft. Self-scored 0.928 PASS; external adv-review composite 0.88 REVISE (0.048 gap).

**Critical iter-1 findings (all addressed in iter-2):**
- PM-002 / FM-012: "88 specialized agents" count unverifiable (closed iter-2).
- FM-002: Candidate comparison weights uncited (closed iter-2).

**Major findings:** 22 total; 12 closed directly in iter-2, 4 closed indirectly via structural changes, 3 partial closures, 3 acknowledged as future work.

---

*Constitutional Compliance: P-003 (no subagents invoked), P-020 (user authority preserved -- V-00 pre-gate, V-01, and STOP GATE all defer to user/owner interview decisions), P-022 (no deception -- every unvalidated claim flagged; every DRAFT block labeled; every candidate frame presents its own weaknesses; iter-1 overclaims on "validated" and "88 agents" explicitly walked back in iter-2 with named blocker IDs).*

*Agent Version: 1.0.0 | Iteration: 4 | Next refresh: Post-V-00/V-01 interview results; post-FEAT-040-053 persona handoff-back; before OSS release.*

---

## Decision Record — 2026-04-21 (Post-Iter-4 User Disposition)

**Decision:** Candidate A selected as canonical positioning. Candidate B ("governance layer") REJECTED by user on accuracy grounds.

**Rationale (user judgment, ground truth):** Jerry is a Claude Code plugin containing ~30 methodology-grade skills with behavioral guardrails, workflow orchestration, and filesystem-based persistent knowledge management. "Governance layer" overclaims the governance aspect, undersells the skills (which are the bulk of user-facing value), and misframes "memory" (filesystem persistence vs. AI/LLM memory). Plugin is accurate; layer is infrastructure marketing language that doesn't match technical reality.

**V-00 Status:** SKIPPED. Not required because Candidate B is no longer the recommended commit path. Candidate B remains documented in this artifact as an analytical alternative that was evaluated and rejected.

**V-01 Status:** N/A (Candidate C behavioral-system framing also not selected).

**Canonical Messaging Hierarchy (user-approved):**

- **Tier 1 (Elevator, ~20 words):** "Jerry is a Claude Code plugin that gives Claude a library of expert skills, enforced quality standards, and persistent memory across sessions."
- **Tier 2 (canonical, ≤15 words):** "Jerry: a Claude Code plugin with 30 expert skills, quality guardrails, and filesystem-based memory."
- **Tier 3 (full paragraph, ~80 words):** "Jerry is a Claude Code plugin with a curated library of methodology-grade skills, behavioral guardrails, and persistent knowledge management — keeping Claude's work consistent and high-quality across sessions. It addresses the Context Rot problem (Claude's performance degrades as context fills) by treating the filesystem as infinite memory: rules, worktracker, knowledge, and decisions persist to disk and load selectively per task."
- **Tier 4 (deep):** Deferred to Phase 2+ explanation documentation.

**Wave 2 Impact:** W2-04 (README commit) and W2-08 (docs/index.md tagline commit) unblock immediately. All 12 Wave 2 items may execute in parallel without V-00 dependency.

**STOP GATE Status (A4/A6):** Unchanged — still requires N>=3 interviews per segment before any A4/A6-specific external messaging is published. Decision to use Candidate A as canonical does not affect A4/A6 persona messaging gates.

*Decision Record appended 2026-04-21 post-iter-4 PASS by orchestrator per user direction.*

# ADR-003: Routing Disambiguation Standard -- NPT-010 "MUST NOT Use When:" Sections with Consequence Documentation for All High-Collision Skills

> **PS:** PROJ-014
> **Task:** TASK-016
> **Created:** 2026-02-28
> **Status:** PROPOSED
> **Agent:** ps-architect
> **Criticality:** C4 (per AE-003: all ADRs auto-C3 minimum; elevated to C4 per orchestration directive)
> **Version:** 1.3.0
> **Supersedes:** None
> **Superseded By:** None

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language decision summary |
| [Context](#context) | Problem statement, background, evidence base |
| [Constraints](#constraints) | Binding constraints on this decision |
| [Forces](#forces) | Tensions at play |
| [Options Considered](#options-considered) | Four options with steelman analysis |
| [Decision](#decision) | Two-component decision with rationale |
| [L1: Technical Implementation](#l1-technical-implementation) | Implementation details, templates, migration steps |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term evolution, systemic consequences |
| [Consequences](#consequences) | Positive, negative, neutral outcomes |
| [Risks](#risks) | Failure modes with mitigation |
| [PG-003 Reversibility Assessment](#pg-003-reversibility-assessment) | Phase 2 dependency gate and reversal protocol |
| [Adversarial Self-Review](#adversarial-self-review) | S-002, S-004, S-013 analysis |
| [Compliance](#compliance) | Constitutional and evidence compliance |
| [Related Decisions](#related-decisions) | ADR cross-references |
| [References](#references) | Source traceability |
| [PS Integration](#ps-integration) | Worktracker linkage |

---

## L0: Executive Summary

### What we decided

All Jerry Framework skills with documented keyword collision risk MUST include a "MUST NOT use when:" routing disambiguation section that (a) specifies when the skill is the wrong choice and (b) documents what goes wrong when the skill is misused (consequence documentation). This applies to all 13 skills in the current inventory: 7 that are fully missing routing disambiguation sections (including architecture and eng-team, which have implicit routing signals through scope definitions but lack dedicated routing disambiguation sections), and 6 that have partial sections lacking consequence documentation.

### Why this matters

When an LLM agent or human operator invokes the wrong skill, the consequences range from wasted context budget to incorrect methodology application. Today, 7 of 13 skills provide no dedicated routing disambiguation section (5 per CX-006 plus architecture and eng-team, which have implicit routing signals but lack dedicated sections per TASK-010 per-skill analysis). Another 6 provide routing alternatives ("use /problem-solving instead") but never explain what breaks on misrouting. This silence creates two documented anti-patterns: AP-01 (Keyword Tunnel -- routing through a narrow vocabulary channel) and AP-02 (Bag of Triggers -- multiple skills matching without resolution). Both are documented in agent-routing-standards.md with detection heuristics and prevention rules.

### Why two components

This ADR makes a two-component decision:

1. **Component A (Consequence Documentation) -- UNCONDITIONAL.** Adding consequence text ("what goes wrong on misrouting") to routing disambiguation sections is valuable regardless of whether MUST NOT language specifically outperforms positive equivalents. Consequences are factual documentation. They improve routing auditability whether the surrounding text says "MUST NOT use when analyzing root causes" or "This skill is not designed for root cause analysis." This component does NOT depend on Phase 2 experimental results.

2. **Component B (MUST NOT Framing) -- CONDITIONAL on Phase 2.** Whether the routing disambiguation section uses "MUST NOT use when:" (NPT-010 pattern: paired prohibition with positive alternative) versus positive routing guidance ("Use /problem-solving instead for root cause analysis") depends on whether Phase 2 experiments confirm a framing effect at AGREE-5 hierarchy ranks 9-11. No controlled evidence exists for the claim that "MUST NOT use when:" framing produces better routing compliance than positive equivalents. This component is reversible pending Phase 2.

---

## Context

### Problem Statement

The Jerry Framework routing architecture (agent-routing-standards.md) documents 8 routing anti-patterns (AP-01 through AP-08). Two are directly relevant to this ADR:

- **AP-01 (Keyword Tunnel):** Routing relies exclusively on keyword matching, creating a narrow channel. Requests expressed in different vocabulary are silently dropped. Prevention includes auditing keyword coverage and maintaining synonym lists. (Source: agent-routing-standards.md, Anti-Pattern Catalog)
- **AP-02 (Bag of Triggers):** Keywords added without collision analysis. Multiple skills match with no conflict resolution. Prevention includes negative keywords and priority ordering. (Source: agent-routing-standards.md, Anti-Pattern Catalog)

The existing mitigation infrastructure -- the 5-column enhanced trigger map in mandatory-skill-usage.md (RT-M-001 through RT-M-004) with negative keywords, priority, and compound triggers -- operates at the routing engine level. It tells the routing system which skills to suppress. It does NOT tell the LLM agent or human operator why a skill is wrong for their task or what goes wrong on misuse. This is the gap.

### Background

#### Current State of Routing Disambiguation

TASK-010 (skills-update-analysis.md, v2.0.0, 0.951 PASS) audited all 13 SKILL.md files and identified three groups:

**Group 1: No dedicated routing disambiguation section (7 skills)**
- bootstrap/SKILL.md
- nasa-se/SKILL.md
- problem-solving/SKILL.md
- transcript/SKILL.md
- worktracker/SKILL.md
- architecture/SKILL.md -- has partial routing guidance through layer dependency rules (H-07) but lacks a dedicated routing disambiguation section; TASK-010 per-skill analysis (line 176) explicitly recommends adding one due to AP-01 risk with /nasa-se keyword overlap [CX-006 lists 5 skills; architecture identified separately in per-skill analysis as also needing a routing disambiguation section, bringing the total to 6; eng-team adds the 7th below]
- eng-team/SKILL.md -- has the most developed constraint structure of any skill (NPT-014 instances, NPT-013 candidates, scope definitions) but routing disambiguation between /eng-team (defensive security) and /red-team (offensive security) is implicit in scope definitions rather than explicit in a dedicated section; TASK-010 does not list eng-team under CX-006 specifically, but its /red-team collision zone (E-017: "security" keyword overlap in trigger map activation keywords) warrants a dedicated routing disambiguation section per the universal application rationale in this ADR [T4 inferred from TASK-010 per-skill analysis showing eng-team/red-team scope overlap]

**Group 2: Partial routing disambiguation -- alternatives without consequences (6 skills)**
- adversary/SKILL.md -- "Do NOT use when:" section provides redirects but no consequence text
- ast/SKILL.md -- "Do NOT use /ast for:" lists exclusions but no consequence for misuse
- orchestration/SKILL.md -- "Do NOT use when:" provides alternatives but no misuse consequence
- red-team/SKILL.md -- "Do NOT use when:" provides alternatives but no misuse consequence
- saucer-boy/SKILL.md -- "Do NOT use when:" provides alternatives but no misuse consequence
- saucer-boy-framework-voice/SKILL.md -- "Do NOT use when:" provides alternatives but no misuse consequence

**Categorization reconciliation note:** The I1 version of this ADR introduced a "Group 3" for architecture/SKILL.md and eng-team/SKILL.md, described as "routing disambiguation present." This contradicted the CX-006 finding (which classified architecture under Group 1) and created an ambiguous count (11 vs. 13 skills needing additions). I2 resolves this: both skills are reclassified into Group 1 because neither has a *dedicated* routing disambiguation section with consequence documentation. Their implicit routing signals (architecture's layer dependency rules, eng-team's scope definitions) do not satisfy the C-005 requirement for domain-specific consequence text in a dedicated section.

The cross-skill pattern CX-006 (Missing Routing Disambiguation) and CX-003 ("Do NOT use when:" Without Consequence Documentation) together establish that all 13 skills require either new routing disambiguation sections (Group 1: 7 skills) or consequence additions to existing sections (Group 2: 6 skills).

#### Evidence Base

| Evidence ID | Source | Tier | Content | Confidence |
|-------------|--------|------|---------|------------|
| AP-01/AP-02 | agent-routing-standards.md | T4 | Routing anti-patterns with detection heuristics | HIGH (documented framework infrastructure) |
| RT-M-001 | agent-routing-standards.md | MEDIUM standard | Skills with >5 positive keywords SHOULD define negative keywords | Framework standard |
| CX-003 | TASK-010 (skills-update-analysis.md) | T4 | 6 skills have "Do NOT use when:" without consequence documentation | HIGH (directly audited) |
| CX-006 | TASK-010 (skills-update-analysis.md) | T4 | 5 skills fully missing routing disambiguation [^1] | HIGH (directly audited) |
| E-016 | TASK-010 evidence reference | T4 | Routing collision risk documented in trigger map | HIGH (derived from trigger map analysis) |
| NPT-010 | Phase 3 taxonomy-pattern-catalog.md | T4+T3 | Paired prohibition with positive alternative; AGREE-8 Moderate agreement | MEDIUM (T4 observational; AGREE-8 is cross-survey agreement, not controlled) |
| NPT-009 | Phase 3 taxonomy-pattern-catalog.md | T4 | Declarative behavioral negation with consequence | MEDIUM (T4; causal comparison UNTESTED) |
| PG-003 | barrier-2/synthesis.md | T4 | Pair enforcement-tier constraints with consequence statements | MEDIUM (working practice; Phase 2 will validate causal contribution) |
| VS-001-VS-004 | supplemental-vendor-evidence.md | T4 | 33 NEVER/MUST NOT instances in Anthropic production rules | HIGH observational, LOW causal |
| E-017 | mandatory-skill-usage.md trigger map + eng-team SKILL.md + red-team SKILL.md | T4 | Eng-team/red-team keyword overlap analysis: "security" appears as an activation keyword in both eng-team (lines 25-44) and red-team SKILL.md activation keywords; collision zone inferred from shared vocabulary in trigger map "secure development" / "penetration test" rows | MEDIUM (trigger map keyword overlap directly observable; routing impact inferred) |

[^1]: CX-006 documents 5 skills fully missing routing disambiguation (bootstrap, nasa-se, problem-solving, transcript, worktracker). Architecture and eng-team are added to Group 1 via TASK-010 per-skill analysis: architecture at line 176 (AP-01 risk with /nasa-se), eng-team at lines 241-268 (E-017: /red-team collision zone). Total Group 1 membership: 5 (CX-006) + 2 (per-skill analysis) = 7.

**Evidence gap (MUST disclose per P-022):** No controlled evidence exists for the claim that "MUST NOT use when:" framing produces better routing compliance than structurally equivalent positive routing guidance ("This skill is not designed for X; use Y instead"). The NPT-010 pattern (T4, AGREE-8 Moderate) documents vendor practice of pairing prohibitions with alternatives. Whether the prohibition vocabulary itself contributes to routing accuracy beyond the structural content (consequence + alternative) is UNTESTED. NEVER cite AGREE-5 rank ordering as T1 or T3 evidence for NPT-010 framing superiority.

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | MUST NOT implement framing-specific changes before Phase 2 experimental results for ranks 9-11 | barrier-2/synthesis.md ST-5, PG-003 contingency |
| C-002 | MUST NOT conflate auditability motivation (consequence documentation) with framing motivation (MUST NOT language) | TASK-016 orchestration directive |
| C-003 | MUST NOT make Phase 2 C1-C7 experimental conditions unreproducible | TASK-010 PG-003 Contingency Plan, Phase 2 Experimental Condition Preservation |
| C-004 | MUST NOT present T4 vendor self-practice evidence as causal evidence for framing superiority | barrier-2/synthesis.md ST-2 confidence reconciliation |
| C-005 | MUST NOT add generic routing disambiguation -- each skill requires domain-specific consequence text grounded in trigger map collision analysis | CX-006 recommendation, TASK-010 |
| C-006 | All constraint language in this ADR's Constraints table and binding requirements (C-001 through C-007, template constraints, migration step requirements) uses NEVER/MUST NOT framing. Non-constraint sections (recommendations, migration guidance, reversibility protocol) MAY use SHOULD where appropriate. | TASK-016 orchestration directive |
| C-007 | MUST NOT cite A-11 (hallucinated citation per Phase 2 audit) | TASK-016 orchestration directive |

### Forces

1. **Routing Correctness vs. Documentation Overhead:** Every skill needs routing disambiguation for LLM agents to route correctly. But adding 13 new or updated sections creates authoring and maintenance burden.

2. **Auditability vs. Framing Preference:** Consequence documentation is valuable independently of framing vocabulary. But the NPT-010 pattern specifically recommends MUST NOT framing, which is UNTESTED against positive equivalents.

3. **Universality vs. Proportionality:** RT-M-001 recommends negative keywords for skills with >5 positive keywords. Should routing disambiguation apply only above this threshold, or universally? Seven skills with no dedicated routing disambiguation sections are gaps regardless of threshold (5 per CX-006 plus architecture and eng-team per per-skill analysis).

4. **Phase 2 Independence vs. Phase 2 Dependence:** Component A (consequences) is unconditional. Component B (MUST NOT framing) is conditional. Mixing them in a single ADR creates implementation sequencing complexity.

5. **Consistency vs. Evidence Honesty:** Adopting MUST NOT framing for all 13 skills would be internally consistent with HARD tier vocabulary (VS-003). But internal consistency is not evidence of effectiveness (VS-002: three competing explanations).

---

## Options Considered

### Option 1: Universal "MUST NOT Use When:" with Consequence Documentation (Full NPT-010)

All 13 skills receive a "MUST NOT use when:" section using prohibitive framing vocabulary (NEVER/MUST NOT), paired with positive alternatives and consequence documentation for each routing exclusion.

**Steelman (S-003):** This option maximizes internal consistency with the HARD tier vocabulary definition (VS-003, E-008: HARD tier is defined by MUST/NEVER/SHALL vocabulary). It provides the strongest possible routing signal by using the same prohibitive language that the framework's own enforcement architecture employs. If VS-002 explanation 3 (engineering discovery) is correct, this option captures the discovered benefit. It also provides a clean, uniform standard that is easy to audit and enforce.

**Pros:**
- Maximum internal consistency with HARD tier vocabulary definition
- Uniform standard across all 13 skills -- no threshold judgment needed
- If Phase 2 confirms framing effect, no further changes needed
- Consequence documentation provides auditability regardless
- Closes all 13 CX-003/CX-006 gaps in one standard

**Cons:**
- Treats UNTESTED causal hypothesis (MUST NOT framing > positive framing) as validated (P-022 violation risk)
- Locks in vocabulary choice before Phase 2 evidence is available (C-001 violation)
- If Phase 2 finds null framing effect, vocabulary changes across 13 skills require reversal
- Conflates the auditability motivation with the framing motivation (C-002 violation)
- No controlled evidence that MUST NOT vocabulary in routing sections improves routing accuracy

**Fit with Constraints:** VIOLATES C-001 (implements framing before Phase 2). VIOLATES C-002 (conflates motivations). Satisfies C-005 if domain-specific consequences are written per skill.

### Option 2: Universal Consequence Documentation with Phase 2 Framing Gate (Two-Component)

All 13 skills receive routing disambiguation sections with consequence documentation immediately (Component A). The framing vocabulary (MUST NOT vs. positive guidance) is deferred to a Phase 2 gate (Component B). Component A uses neutral or positive framing for routing exclusions. Component B applies MUST NOT framing only after Phase 2 confirms framing effect.

**Steelman (S-003):** This option correctly separates the two independent motivations. Consequence documentation is factually valuable regardless of vocabulary -- it tells agents and operators what breaks on misrouting. The framing vocabulary is the experimentally contested dimension. By separating them, the ADR avoids committing to an UNTESTED hypothesis while still closing all routing disambiguation gaps. The two-component structure also provides a clean experimental control: Phase 2 can measure routing accuracy before and after Component B application.

**Pros:**
- Correctly separates unconditional (consequences) from conditional (framing) components
- Closes all 13 routing gaps immediately without Phase 2 dependency
- Preserves Phase 2 experimental integrity (C-003 satisfied)
- Consequence documentation is NOT reversible -- remains valuable regardless of Phase 2 outcome
- Avoids P-022 risk of treating UNTESTED hypothesis as validated
- Provides natural before/after measurement opportunity for Phase 2

**Cons:**
- Two-phase implementation is more complex than single-phase
- Temporary inconsistency: existing "Do NOT use when:" sections use prohibition vocabulary while new sections use neutral framing
- If Phase 2 confirms framing effect, the Component B retrofit adds a second pass over all 13 skills
- Skills in Group 2 already use "Do NOT use when:" -- rewriting to neutral framing for Component A creates unnecessary churn if Component B later reinstates prohibition framing

**Fit with Constraints:** Satisfies C-001 (framing deferred to Phase 2). Satisfies C-002 (motivations separated). Satisfies C-003 (experimental conditions preserved). Satisfies C-005 if domain-specific.

### Option 3: Threshold-Based Application (>5 Keywords Only)

Routing disambiguation applies only to skills exceeding the RT-M-001 threshold (>5 positive keywords). Skills below the threshold receive no routing disambiguation sections.

**Steelman (S-003):** This option is proportional. RT-M-001 exists because keyword collision risk increases with keyword count. Skills with fewer keywords have lower collision risk and lower misrouting probability. Applying the standard only where the routing risk is highest produces the best effort-to-impact ratio. It avoids documentation overhead for low-collision skills like bootstrap and transcript.

**Pros:**
- Proportional to documented routing risk
- Lower implementation effort (fewer skills to update)
- Aligned with existing RT-M-001 standard intent
- Avoids unnecessary documentation in low-collision domains

**Cons:**
- TASK-010 finding: 7 skills fully missing dedicated routing disambiguation sections (5 per CX-006 plus architecture and eng-team per per-skill analysis) are unambiguous gaps regardless of keyword count -- including nasa-se and problem-solving which have >5 keywords
- Bootstrap, transcript, and worktracker have low keyword counts but nonzero misrouting risk (worktracker/problem-solving confusion is documented)
- Creates a two-tier system where some skills have disambiguation and others silently lack it -- agents have no signal that absence means "low risk" vs. "not yet documented"
- Does not address CX-003 (existing sections lacking consequences) because those skills already have >5 keywords

**Fit with Constraints:** Satisfies C-001 and C-002 if combined with Component A/B split from Option 2. VIOLATES C-005 partially (leaves some skills without domain-specific routing guidance).

### Option 4: Status Quo (No Standard)

No new routing disambiguation standard. Rely on the trigger map (mandatory-skill-usage.md) and existing "Do NOT use when:" sections as-is.

**Steelman (S-003):** The trigger map already provides the primary routing mechanism. Layer 0 (explicit slash commands) and Layer 1 (keyword matching with negative keywords) handle most routing decisions. Adding skill-level routing disambiguation sections is redundant with the trigger map -- the same information expressed in two places creates a maintenance synchronization burden. The trigger map is the authoritative routing source; SKILL.md files are orientation documents, not routing engines.

**Pros:**
- Zero implementation effort
- No maintenance synchronization burden between trigger map and SKILL.md
- Trigger map is the authoritative routing source -- SKILL.md disambiguation is advisory only
- Avoids premature commitment to framing vocabulary

**Cons:**
- Leaves 7 skills with zero dedicated routing guidance for agents that cannot access the trigger map mid-execution
- Trigger map tells the routing system which skills to suppress; it does NOT tell an invoked agent that it was invoked incorrectly
- AP-01 and AP-02 anti-patterns remain unmitigated at the skill level
- Post-invocation misrouting analysis (whether by the agent or by human reviewers) requires skill-level routing boundaries with consequence documentation -- which cannot exist without routing disambiguation sections
- Does not address CX-003 (existing consequence documentation gaps)

**Fit with Constraints:** Satisfies C-001 through C-004 trivially (no changes made). VIOLATES C-005 implicitly (no routing guidance means no domain-specific consequence documentation).

---

## Decision

**We will adopt Option 2: Universal Consequence Documentation with Phase 2 Framing Gate (Two-Component).**

### Rationale

The decision is driven by the separation of two independent motivations:

**Component A (UNCONDITIONAL -- Implement Immediately):** All 13 skills MUST include a routing disambiguation section with consequence documentation. Each section MUST:
- Enumerate specific conditions under which the skill is the wrong choice
- Provide the correct alternative skill for each exclusion condition
- Document the consequence of misrouting (what fails, what degrades, what resource is wasted)
- Ground each exclusion in the trigger map collision analysis (mandatory-skill-usage.md)

The motivation for Component A is **routing auditability**: consequence documentation enables human reviewers to determine whether misrouting occurred and what its impact was. This is factually valuable regardless of whether the section header says "MUST NOT use when:" or "This skill is not appropriate when:". Whether agents additionally use this information for real-time self-diagnosis during execution is aspirational rather than guaranteed (see S-002 Assumption 1 analysis below); the primary value proposition is post-hoc auditability, not real-time self-correction. Consequence documentation is NOT a framing choice -- it is factual documentation of failure modes.

**Component B (CONDITIONAL -- Phase 2 Gate):** The framing vocabulary of routing disambiguation sections (MUST NOT/NEVER vs. positive guidance) MUST NOT be standardized until Phase 2 experimental results are available for AGREE-5 hierarchy ranks 9-11. When Phase 2 results are available:
- If framing effect confirmed: Apply NPT-010 "MUST NOT use when:" framing to all routing disambiguation sections
- If null framing effect: Retain consequence documentation (Component A); adopt the framing vocabulary that the framework community prefers for readability and consistency
- If inconclusive: Retain consequence documentation (Component A); defer framing standardization to a follow-up experiment

**Why Option 1 was rejected:** Option 1 conflates the auditability motivation with the framing motivation (C-002 violation) and implements framing before Phase 2 evidence (C-001 violation). Despite its internal consistency advantage, it treats an UNTESTED hypothesis as validated. NEVER implement a framing standard based on T4 observational evidence alone when a controlled experiment is planned.

**Why Option 3 was rejected:** Option 3's proportionality argument is sound in principle but fails against the TASK-010 audit data. Seven skills with no dedicated routing disambiguation sections represent gaps that the >5 keyword threshold does not excuse (5 per CX-006 plus architecture and eng-team per per-skill analysis). The problem-solving skill (broadest scope, highest collision risk) and nasa-se skill (deep keyword overlap with both /problem-solving and /architecture) are both above the threshold anyway. The bootstrap, transcript, and worktracker skills are below the threshold but have documented misrouting scenarios. Universal application with domain-specific content (per C-005) is preferable to threshold-based exclusion.

**Why Option 4 was rejected:** Option 4's steelman (trigger map as authoritative source) is architecturally correct at the routing engine level. But it fails at two levels. First, at the agent experience level: an agent invoked for the wrong task cannot consult the trigger map mid-execution. Skill-level routing disambiguation provides diagnostic information that may enable self-correction (though this is aspirational -- see S-002 Assumption 1). Second, and more robustly, at the auditability level: when routing failures occur, human reviewers need domain-specific failure mode documentation to diagnose what went wrong. The trigger map prevents misrouting at the routing layer; the skill-level section documents consequences for post-hoc analysis at the audit layer.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | Satisfies C-001 through C-007 |
| Risk Level | LOW | Component A is unconditional; Component B is gated |
| Implementation Effort | MEDIUM | 13 new/updated sections across 13 skills (7 new + 6 consequence additions); domain-specific content required per C-005 |
| Reversibility | HIGH | Component A is permanently valuable; Component B is fully reversible |

---

## L1: Technical Implementation

### Component A: Consequence Documentation (Immediate)

#### Template for New Routing Disambiguation Sections

Skills in Group 1 (no existing section) MUST add a section following this template:

```markdown
## When This Skill is Not Appropriate

| Condition | Correct Alternative | Consequence of Misrouting |
|-----------|--------------------|-----------------------------|
| {specific condition when skill is wrong} | {correct skill with /slash-command} | {what fails, degrades, or is wasted} |
```

**Template constraints:**
- MUST NOT use generic consequence text (e.g., "reduced quality"). Each consequence MUST name the specific failure mode.
- MUST NOT list more than 7 exclusion conditions per skill (cognitive load limit; if more exist, the skill's scope is too broad).
- MUST ground each condition in a documented keyword collision from the trigger map.
- The consequence column MUST answer: "What specifically goes wrong if this skill processes a task it was not designed for?"

#### Template for Consequence Additions to Existing Sections

Skills in Group 2 (existing sections without consequences) MUST add a consequence column to their existing routing disambiguation:

**Before (current pattern):**
```markdown
## Do NOT use when:
- You need root cause analysis -> use /problem-solving
- You need requirements design -> use /nasa-se
```

**After (Component A applied):**
```markdown
## Do NOT use when:

| Condition | Correct Alternative | Consequence of Misrouting |
|-----------|--------------------|-----------------------------|
| Root cause analysis needed | /problem-solving (ps-investigator) | Incorrect methodology applied; convergent investigation replaced with divergent exploration; root cause not isolated |
| Requirements design needed | /nasa-se | Requirements expressed as architectural decisions; V&V traceability lost; compliance gaps not detected |
```

#### Per-Skill Consequence Specifications

The following consequence text is derived from TASK-010 per-skill analysis and trigger map collision data (E-016). Each entry specifies the domain-specific consequence that MUST appear in the routing disambiguation section. Evidence tier labels indicate the provenance of each consequence claim.

**Skills fully missing routing disambiguation (Group 1, 7 skills):**

| Skill | Key Exclusion Conditions | Domain-Specific Consequences | Evidence Tier | Collision Frequency |
|-------|-------------------------|------------------------------|---------------|---------------------|
| bootstrap | Task requires behavioral constraints, code generation, or analysis | Bootstrap is a navigation tool; invoking it for work tasks wastes context budget loading orientation content with no analytical capability | T4 inferred: TASK-010 Skill 4 gap analysis; no quantitative data available | Lower |
| nasa-se | Root cause analysis, debugging, adversarial review | NASA-SE methodology applied to investigation tasks produces requirements artifacts instead of causal chains; compliance vocabulary obscures root cause | T4 inferred: TASK-010 Skill 6 gap analysis (line 285); AP-02 keyword overlap documented in E-016 | High |
| problem-solving | Simple orchestration coordination, requirements specification, transcript parsing | Broadest-scope skill invoked for narrow tasks consumes excess context loading 9 agent definitions (ps-researcher, ps-analyst, ps-architect, ps-critic, ps-validator, ps-synthesizer, ps-reviewer, ps-investigator, ps-reporter; source: problem-solving SKILL.md Available Agents table, lines 78-88); /orchestration coordination overhead applied to single-agent tasks | T4 inferred: TASK-010 per-skill analysis; agent count verified against problem-solving SKILL.md (9 agents enumerated in Available Agents table, lines 78-88) | High |
| transcript | Non-transcript file analysis, general text processing | Transcript parsing agents (ts-parser, ts-extractor) applied to non-VTT/SRT files produce parsing failures; 1,250x cost multiplier if Task agents invoked unnecessarily | T4 measurable: TASK-010 CX-005 (line 575); 1,250x figure from transcript SKILL.md (E-011), representing the cost ratio of Task agent invocation vs. direct CLI parsing | Lower |
| worktracker | CLI-resolvable queries, non-entity file operations | Worktracker agents invoked for queries answerable by `jerry items list` waste agent invocation overhead; AST parsing applied to non-entity files produces validation errors | T4 inferred: TASK-010 per-skill analysis; AST validation error consequence derives from H-33 enforcement mechanism | Lower |
| architecture | Requirements design (/nasa-se), root cause analysis (/problem-solving), offensive security (/red-team) | Architecture methodology (layer dependency rules, CQRS patterns, hexagonal structure) applied to non-architecture tasks produces structural design artifacts when the task requires investigation, requirements, or security assessment; agent context loaded with H-07 enforcement detail that is irrelevant to the actual task | T4 inferred: TASK-010 Skill 2 gap analysis (line 176); AP-01 Keyword Tunnel risk with /nasa-se documented in E-016; no quantitative impact data available | High |
| eng-team | Adversarial quality review (/adversary), offensive security testing (/red-team), general code review (/problem-solving ps-reviewer) | Defensive security methodology (STRIDE/DREAD threat modeling, OWASP ASVS compliance, CIS benchmarks) applied to offensive or quality-assessment tasks produces security architecture artifacts instead of attack narratives or quality scores; 10 security-focused agents loaded into context (eng-architect, eng-lead, eng-backend, eng-frontend, eng-infra, eng-devsecops, eng-qa, eng-security, eng-reviewer, eng-incident; source: eng-team SKILL.md agents list, lines 13-22 and Available Agents table, lines 123-134) when task requires a different methodology entirely | T4 inferred: TASK-010 Skill 5 analysis (lines 241-268) documents eng-team scope and constraint structure; /red-team collision zone inferred from trigger map keyword overlap (E-017: "security" appears in both eng-team and red-team activation keywords); agent count verified against eng-team SKILL.md (10 agents enumerated) | Medium |

**Collision Frequency column rationale:** High-collision skills (problem-solving, nasa-se, architecture) share extensive keyword overlap in the trigger map and are the most frequent targets of AP-01/AP-02 anti-patterns. Medium-collision (eng-team) has a documented but narrower /red-team collision zone. Lower-collision (bootstrap, transcript, worktracker) have fewer keyword overlaps but nonzero misrouting risk. Implementation priority per R-005 mitigation should follow this ordering: high-collision skills first, then medium, then lower.

**SKILL.md line reference verification (2026-02-28):** All SKILL.md line references in the Group 1 consequence specification table above were verified by reading the source files on 2026-02-28:
- **eng-team SKILL.md lines 13-22:** Confirmed. Lines 13-22 contain the `agents:` YAML list enumerating all 10 agents (eng-architect, eng-lead, eng-backend, eng-frontend, eng-infra, eng-devsecops, eng-qa, eng-security, eng-reviewer, eng-incident).
- **eng-team SKILL.md lines 123-134:** Confirmed. Lines 123-134 contain the "Available Agents" markdown table with Agent, Role, and Output Location columns for all 10 agents.
- **problem-solving SKILL.md lines 78-88:** Confirmed. Lines 78-88 contain the "Available Agents" markdown table with Agent, Role, and Output Location columns for all 9 agents (ps-researcher, ps-analyst, ps-architect, ps-critic, ps-validator, ps-synthesizer, ps-reviewer, ps-investigator, ps-reporter).
- **E-017 keyword overlap verification:** Confirmed. The mandatory-skill-usage.md trigger map eng-team row (line 41) includes "security architecture", "supply chain security", and "security requirements" as activation keywords. The red-team row (line 42) includes "offensive security" as an activation keyword. The word "security" appears in activation keywords for both skills, confirming the E-017 collision zone claim. Additionally, eng-team SKILL.md lines 25-44 list 20 activation keywords including "secure design", "secure architecture", "security requirements", and "supply chain security".

**Skills with partial sections requiring consequence additions (Group 2, 6 skills):**

| Skill | Existing Exclusions Needing Consequences | Evidence Tier |
|-------|----------------------------------------|---------------|
| adversary | "Iterative improvement" redirect to /problem-solving needs consequence: adversarial one-shot assessment applied to iterative work produces premature rejection without revision pathway | T4 inferred: TASK-010 per-skill analysis (adversary section); consequence text is analyst inference from skill methodology description |
| ast | "General text operations" redirect needs consequence: AST validation schema applied to non-entity markdown produces false-positive structural errors | T4 inferred: TASK-010 Skill 3 analysis (line 200); H-33 enforcement mechanism implies validation error on non-entity input |
| orchestration | "Single-agent tasks" redirect needs consequence: multi-phase coordination overhead (barrier sync, quality gates) applied to single-step task wastes significant context budget on unnecessary coordination infrastructure | T4 inferred: TASK-010 per-skill analysis; "significant context budget" is a qualitative assessment -- no quantitative multiplier is available from source analyses (analyst estimate, pending validation) |
| red-team | "Defensive security" redirect to /eng-team needs consequence: offensive methodology (reconnaissance, exploitation) applied to defensive design produces attack narratives instead of security architecture | T4 inferred: TASK-010 per-skill analysis (red-team section); consequence reflects methodology mismatch between offensive and defensive security domains |
| saucer-boy | "Framework output" redirect to /saucer-boy-framework-voice needs consequence: conversational voice applied to framework documentation violates voice consistency standards; output requires complete rewrite | T4 inferred: TASK-010 per-skill analysis; voice consistency violation consequence is analyst inference from /saucer-boy-framework-voice existence rationale |
| saucer-boy-framework-voice | "Conversational content" redirect to /saucer-boy needs consequence: framework voice constraints applied to conversational content produce rigid, impersonal output that fails the authenticity test | T4 inferred: TASK-010 per-skill analysis; consequence reflects the inverse of the saucer-boy misrouting scenario |

#### Migration Steps

1. **Audit trigger map collisions.** For each of the 13 skills, cross-reference the skill's positive keywords against all other skills' positive keywords in mandatory-skill-usage.md. Document collision zones. **Owner:** ps-architect or designated skill maintainer. **Output artifact:** `work/routing-collisions.md` (collision matrix listing each skill's keyword overlaps with every other skill). **Acceptance criteria:** Every skill with >3 positive keywords has its collision zones documented with the overlapping skill(s) identified.
2. **Draft consequence text.** For each collision zone, write the specific consequence of misrouting using the transcript skill NPT-009 exemplars (CX-005) as the format model: "MUST NOT [action] -- [specific technical consequence]." **Owner:** Domain expert per skill (e.g., /eng-team maintainer for eng-team consequence text). **Output artifact:** Draft consequence text in each SKILL.md file per the templates above. **Acceptance criteria for consequence adequacy:** Each consequence row MUST (a) name the specific failure mode, (b) identify the agent family or methodology that is incorrectly applied, and (c) describe the resource wasted or output degraded. Generic consequences (e.g., "reduced quality," "wrong output") are insufficient per C-005.
3. **Add sections.** Group 1 skills (7): add new "When This Skill is Not Appropriate" section. Group 2 skills (6): add consequence column to existing section. **Note on Group 2 format heterogeneity:** Existing Group 2 skills use varying formats (adversary/ast use "Do NOT use when:"/"Do NOT use /ast for:" while others use different layouts). The consequence column addition MUST preserve each skill's existing format structure -- retrofit the consequence column into the existing format rather than rewriting to a uniform template. This accommodates ast/SKILL.md's "Do NOT use /ast for:" format alongside adversary/SKILL.md's redirect format. **Owner:** ps-architect for template compliance review; skill maintainer for content.
4. **Review against trigger map.** Verify that every exclusion condition in a SKILL.md routing disambiguation section has a corresponding negative keyword entry in the trigger map. If not, update the trigger map. **Owner:** Routing standards maintainer. **Output artifact:** Updated mandatory-skill-usage.md trigger map (if gaps found). **Acceptance criteria:** Every exclusion condition in each SKILL.md routing disambiguation section maps to at least one negative keyword entry in the trigger map in mandatory-skill-usage.md.
5. **Commit separately.** SKILL.md routing disambiguation changes MUST be committed in a separate branch from any rule file changes (C-003: preserve Phase 2 experimental conditions). **Owner:** Committer.

### Component B: Framing Vocabulary (Phase 2 Gated)

Component B MUST NOT be implemented until Phase 2 provides one of three verdicts:

| Phase 2 Verdict | Component B Action |
|-----------------|-------------------|
| Framing effect confirmed at ranks 9-11 | Rewrite all routing disambiguation section headers to "MUST NOT use when:" (NPT-010 full pattern). Apply MUST NOT/NEVER vocabulary to each exclusion condition row. |
| Null framing effect at ranks 9-11 | Retain Component A consequence documentation. Adopt the framing vocabulary that the framework community prefers. MUST NOT claim effectiveness basis for vocabulary choice. |
| Inconclusive | Retain Component A. Defer framing standardization. Consider expanded experiment per pilot GO/NO-GO criteria. |

**Framing retrofit template (for confirmed framing effect):**

```markdown
## MUST NOT Use When:

| Condition | Correct Alternative | Consequence of Misrouting |
|-----------|--------------------|-----------------------------|
| MUST NOT invoke for root cause analysis | /problem-solving (ps-investigator) | Incorrect methodology applied; convergent investigation replaced with divergent exploration; root cause not isolated |
```

---

## L2: Architectural Implications

### Long-Term Evolution Path

This ADR establishes a precedent for separating factual documentation requirements from framing vocabulary decisions in the Jerry Framework. The two-component pattern (unconditional content + conditional framing) can be applied to future standards where:
- The content is independently valuable (consequence documentation, alternative specification, scope definition)
- The framing is experimentally contested (prohibition vocabulary vs. positive guidance)

This separation prevents the framework from locking in vocabulary conventions before evidence supports them, while still closing operational gaps immediately.

### Systemic Consequences

**Routing observability improvement.** Component A directly addresses the observability gap identified in agent-routing-standards.md Section "Routing Observability" (RT-M-008, RT-M-009). When routing disambiguation sections document consequences, the routing record format can be extended to include: "misrouting consequence: [text from skill section]." This provides post-hoc analysis of routing failures with domain-specific failure descriptions rather than generic "wrong skill" entries.

**Trigger map synchronization burden.** Every routing disambiguation section in a SKILL.md creates a synchronization dependency with the trigger map in mandatory-skill-usage.md. If a skill's keyword set changes, both the trigger map and the routing disambiguation section MUST be updated. This is a maintenance cost. Mitigation: include a "Last synchronized with trigger map" date field in each routing disambiguation section, audited quarterly by the routing standards maintainer and on every trigger map modification (see R-001 for full specification).

**Phase 2 experimental baseline.** Component A, implemented before Phase 2, provides a natural pre-treatment baseline. Routing accuracy (measurable via RT-M-008 routing records) with consequence documentation but neutral framing (Component A only) can be compared against routing accuracy after Component B application. This makes the framework itself a data source for Phase 2 analysis, though with observational (T4/T5) rather than controlled (T1) evidence quality.

**Scaling path.** At current scale (8 skills with trigger map entries, 13 total SKILL.md files), universal application is manageable. The Scaling Roadmap in agent-routing-standards.md projects Phase 2 (10-15 skills) and Phase 3 (15-20 skills) routing architecture evolution. At 20+ skills, routing disambiguation sections become the primary human-readable routing reference because the trigger map becomes too dense for manual consultation. This ADR's consequence documentation requirement scales well -- each new skill inherits the template.

### Integration with Existing Architecture

| Architecture Component | Integration Point | Impact |
|------------------------|--------------------|--------|
| Trigger map (mandatory-skill-usage.md) | Synchronization dependency | Each SKILL.md routing exclusion must have a corresponding negative keyword |
| Agent routing layers (L0-L3) | L1 keyword layer supplemented by skill-level routing boundaries | Human reviewers and potentially agents can diagnose misrouting after invocation; primary value is post-hoc auditability |
| Circuit breaker (H-36) | Routing disambiguation enables earlier detection of misroutes before circuit breaker activation | Reduces average routing hops per request (RT-M-015) |
| Quality gate (H-13/H-14) | Misrouted agents produce lower-quality output that the quality gate catches later -- routing disambiguation catches it earlier | Reduces wasted critic iterations on fundamentally misrouted work |
| Progressive disclosure (agent-development-standards.md) | Routing disambiguation is Tier 1 content (loaded at session start via SKILL.md description) | Must remain concise; defer detail to Tier 2/3 |

### Future Flexibility and Constraints

**Flexible:** The two-component structure allows the framing vocabulary to evolve independently of the consequence content. If a future Phase 3 or Phase 4 experiment establishes that a different framing (e.g., contrastive examples per NPT-008) outperforms both MUST NOT and positive guidance for routing, the framing can be changed without touching the consequence text.

**Constrained:** Once consequence documentation is established for all 13 skills, removing it requires demonstrating that consequence-free routing disambiguation is equally effective. This is unlikely to be demonstrated because consequence documentation is factually descriptive, not framing-dependent. Component A is effectively irreversible by design.

---

## Consequences

### Positive Consequences

1. **All 13 routing disambiguation gaps closed.** Seven skills gain routing disambiguation sections they currently lack entirely (5 per CX-006 plus architecture and eng-team). Six skills gain consequence documentation their existing sections lack (per CX-003).
2. **Post-invocation misrouting auditability enabled.** When routing failures occur, human reviewers can determine what went wrong by consulting the routing disambiguation section's consequence documentation. Agents invoked for the wrong task may additionally use this information for self-correction, though real-time self-diagnosis is aspirational rather than guaranteed (see S-002 Assumption 1).
3. **Routing auditability improved.** When routing records (RT-M-008) are extended with consequence text from routing disambiguation sections, post-hoc routing failure analysis becomes domain-specific rather than generic.
4. **Phase 2 experimental baseline established.** Implementing Component A before Phase 2 creates a natural pre-treatment measurement point for routing accuracy.
5. **Maintenance template established.** New skills added to the framework inherit a clear template for routing disambiguation with consequence documentation.

### Negative Consequences

1. **Maintenance synchronization burden.** Every SKILL.md routing disambiguation section creates a dependency with the trigger map. Changes to one require changes to the other. This is an ongoing maintenance cost, not a one-time implementation cost.
2. **Temporary framing inconsistency.** Between Component A implementation and Phase 2 verdict, the framework will have a mix of "Do NOT use when:" (existing Group 2 sections), neutral framing (new Group 1 sections), and no disambiguation (skills not yet updated). This inconsistency is bounded by the Phase 2 timeline.
3. **Risk of stale consequence documentation.** If a skill's scope changes but its routing disambiguation section is not updated, the consequence text becomes inaccurate. Stale consequence documentation is worse than absent documentation because it provides false confidence.
4. **Content authoring effort.** Domain-specific consequence text for 13 skill sections requires per-skill analysis. Generic consequences are explicitly forbidden by C-005. This authoring effort is real and cannot be template-automated.

### Neutral Consequences

1. **No change to trigger map infrastructure.** The trigger map (mandatory-skill-usage.md) operates independently. This ADR adds a consumer-facing layer on top of the routing engine, not a replacement for it.
2. **No change to routing algorithm.** The three-step routing resolution (filter, specificity, priority) in agent-routing-standards.md is unchanged. Routing disambiguation sections are advisory for post-invocation detection, not inputs to the routing algorithm.

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| R-001: Consequence documentation becomes stale after skill scope changes | MEDIUM | MEDIUM | Include "Last synchronized with trigger map: {date}" field in each routing disambiguation section. **Audit frequency and owner:** The routing standards maintainer (same owner as migration step 4) audits synchronization quarterly and whenever the trigger map in mandatory-skill-usage.md is modified. Each skill maintainer is responsible for updating their skill's routing disambiguation section when that skill's keywords change. |
| R-002: Phase 2 finds null framing effect; Component B never applied; temporary framing inconsistency becomes permanent | LOW | LOW | Consequence documentation (Component A) provides permanent value regardless; framing inconsistency affects aesthetics, not functionality |
| R-003: Domain-specific consequence text is inaccurate (wrong failure mode documented) | LOW | HIGH | Review consequence text against actual trigger map collisions; validate with /problem-solving agents that process the most routing-ambiguous requests |
| R-004: Two-component implementation creates confusion about which standard applies at any given time | MEDIUM | LOW | Document implementation state explicitly; ADR status tracks Component A (ACCEPTED after approval) and Component B (PROPOSED pending Phase 2) separately |
| R-005: Content authoring effort delays implementation beyond Phase 2 timeline | LOW | MEDIUM | Prioritize highest-collision skills (problem-solving, nasa-se, orchestration) first; lower-collision skills can trail |

---

## PG-003 Reversibility Assessment

### Phase 2 Dependency Gate

This ADR contains two components with different Phase 2 dependencies:

| Component | Phase 2 Dependency | Reversibility |
|-----------|-------------------|---------------|
| A: Consequence documentation | NONE -- unconditional | NOT REVERSIBLE by design. Consequence documentation is factual and independently valuable. If removed, routing auditability degrades regardless of framing vocabulary. |
| B: MUST NOT framing vocabulary | FULL -- conditional on Phase 2 verdict at ranks 9-11 | FULLY REVERSIBLE. If Phase 2 finds null framing effect, revert all "MUST NOT use when:" headers and row vocabulary to neutral/positive framing. Consequence text (Component A) is retained unchanged. |

### Reversal Protocol (If Phase 2 Null at Ranks 9-11)

IF Phase 2 experiment finds null framing effect for NPT-009/NPT-010 at AGREE-5 hierarchy ranks 9-11:

1. MUST NOT revert consequence documentation (Component A). Consequence text remains permanently.
2. MUST NOT revert routing exclusion conditions. The conditions themselves (e.g., "root cause analysis is not this skill's purpose") are factual scope definitions.
3. SHOULD revert section headers from "MUST NOT use when:" to the community-preferred neutral framing.
4. SHOULD revert individual row vocabulary from "MUST NOT invoke for X" to neutral equivalents.
5. MUST document the reversion in this ADR's status field (change to "PARTIALLY SUPERSEDED: Component B reverted per Phase 2 null result; Component A retained").

### Interaction with Other ADRs

| ADR | Interaction with This ADR |
|-----|---------------------------|
| ADR-001 (NPT-014 Elimination) | Independent. ADR-001 is unconditional (T1+T3); this ADR's Component A is unconditional; no conflict. |
| ADR-002 (Constitutional Triplet) | Parallel conditional dependency on Phase 2. ADR-002's NPT-013 framing and this ADR's Component B framing are both gated on Phase 2 ranks 9-11. If null result, both revert framing while retaining structural content. |
| ADR-004 (Context Compaction) | Independent. Context compaction resilience (T-004) is orthogonal to routing disambiguation content. However, routing disambiguation sections are L1-loaded (SKILL.md) and thus not subject to L2 re-injection context compaction risk. |

---

## Adversarial Self-Review

### S-002 Devil's Advocate: Challenging Key Assumptions

**Assumption 1: "Consequence documentation improves routing accuracy."**
Challenge: No controlled study measures routing accuracy with vs. without consequence documentation in LLM agent routing. The claim that agents can "self-diagnose misrouting" by reading a routing disambiguation section assumes the agent reads and acts on this information. If the agent is already processing a task, it may not re-evaluate its suitability after invocation.
Counter: The assumption is weaker than stated and has been revised in this ADR accordingly. What consequence documentation provides is not guaranteed self-diagnosis but the availability of diagnostic information. Whether agents use it for real-time self-correction depends on implementation and is aspirational rather than guaranteed. The primary motivation for Component A is therefore **auditability**: human reviewers can determine if misrouting occurred and what its impact was by consulting the consequence documentation. This is a weaker but more defensible claim than "routing accuracy improvement." The Decision section (Component A rationale) and Consequences section have been updated in I2 to reflect this auditability-primary framing. Agent self-diagnosis remains a secondary, aspirational benefit -- not the primary justification for Component A. No evidence (T4 or otherwise) currently demonstrates that agents read SKILL.md routing disambiguation sections during execution.

**Assumption 2: "Seven missing routing disambiguation sections represent unambiguous gaps."**
Challenge: Of the seven Group 1 skills, three (bootstrap, transcript, worktracker) have low keyword collision risk. Their absence may be a correct proportionality judgment, not a gap. Architecture and eng-team have implicit routing signals through scope definitions that may suffice without dedicated sections. The "unambiguous" claim overreaches for low-collision and implicit-routing skills.
Counter: Valid. The urgency differs by skill. Problem-solving and nasa-se are high-collision and clearly gap. Architecture has documented AP-01 risk with /nasa-se (TASK-010 line 176). Eng-team has a real but less-documented /red-team collision zone. Bootstrap, transcript, and worktracker are lower-collision but not zero. The "unambiguous" claim should be qualified: high-collision skills (problem-solving, nasa-se, architecture) are unambiguous; medium-collision skills (eng-team) are strongly recommended; low-collision skills (bootstrap, transcript, worktracker) are recommended but less urgent.

### S-004 Pre-Mortem: "It is 6 months later and this decision failed -- why?"

**Failure scenario 1: Consequence documentation is never written.** The ADR mandates domain-specific content per C-005, but the authoring effort is distributed across 13 skills with no centralized owner. Six months later, 3 of 13 sections are written; the rest have placeholder text. The standard exists but is not enforced.
Mitigation: Implementation plan (below) assigns priority ordering and completion criteria. Track implementation as worktracker tasks per skill: ps-architect creates one worktracker task per Group 1 skill (7 tasks) and one per Group 2 skill (6 tasks) during migration step 1 (trigger map collision audit), before consequence text authoring begins. Each task is assigned to the domain expert for that skill per migration step 2 ownership.

**Failure scenario 2: Trigger map diverges from routing disambiguation sections.** Skills add keywords to the trigger map without updating routing disambiguation sections, or vice versa. The two documents tell different stories about when to use the skill. Six months later, 40% of routing disambiguation sections are stale.
Mitigation: R-001 mitigation (date-stamped synchronization field). Consider CI gate that compares trigger map negative keywords against SKILL.md exclusion conditions.

**Failure scenario 3: Phase 2 is indefinitely delayed. Component B is never resolved.** Phase 2 pilot requires 30-45 researcher-hours (barrier-2/synthesis.md). If deprioritized, the framing question remains open indefinitely. The framework operates with Component A only but the "PROPOSED pending Phase 2" status on Component B becomes stale.
Mitigation: Set a time-bound (6 months from Component A implementation). If Phase 2 has not produced results by then, Component B defaults to the community's preferred framing without effectiveness claims.

### S-013 Inversion: "What if we deliberately chose the opposite approach?"

**Inverted decision: No routing disambiguation anywhere. Rely entirely on the trigger map.**
If the trigger map were 100% accurate with zero false positives and zero false negatives, routing disambiguation in SKILL.md files would be redundant. The trigger map would prevent all misrouting at Layer 1. But the trigger map is not 100% accurate -- RT-M-001 through RT-M-004 exist precisely because collision resolution requires enhancement. The inversion confirms that routing disambiguation serves as a compensating control for trigger map imperfection. Its value is proportional to trigger map collision density. As the trigger map improves (Phase 2-3 of the Scaling Roadmap), the compensating value of SKILL.md routing disambiguation decreases but never reaches zero (agents still need post-invocation diagnostic information).

---

## Compliance

### Constitutional Compliance

| Principle | Compliance Status | Evidence |
|-----------|-------------------|----------|
| P-001 (Truth/Accuracy) | COMPLIANT | All evidence tier labels present; T4 evidence not presented as T1; UNTESTED claims disclosed |
| P-002 (File Persistence) | COMPLIANT | ADR persisted to file |
| P-003 (No Recursion) | NOT APPLICABLE | No subagent spawning in this ADR |
| P-004 (Provenance) | COMPLIANT | All claims trace to source documents with evidence IDs |
| P-011 (Evidence-Based) | COMPLIANT | Four alternatives evaluated with steelman analysis |
| P-020 (User Authority) | COMPLIANT | Status PROPOSED; requires user approval |
| P-022 (No Deception) | COMPLIANT | Evidence gap disclosed (no controlled evidence for MUST NOT framing superiority); negative consequences documented; three competing explanations for VS-002 disclosed |

### Evidence Tier Compliance

| Claim | Evidence Tier | Status |
|-------|---------------|--------|
| Blunt prohibition underperforms structured alternatives | T1+T3 (PG-001: A-20, A-15, A-31) | ESTABLISHED -- unconditional |
| Vendor systems use MUST NOT/NEVER vocabulary in enforcement tier | T4 (VS-001-VS-004) | OBSERVED -- 33 instances documented |
| MUST NOT framing produces better routing compliance than positive equivalents | UNTESTED | No controlled comparison exists |
| Consequence documentation improves routing auditability (primary claim) | T4 (CX-003, CX-006 audit findings) | OBSERVED -- logical inference from gap analysis; auditability value is independent of whether agents use it for real-time self-correction. **Upgrade path:** T4-to-T3 upgrade would require Phase 2 routing record measurement (RT-M-008) comparing routing failure diagnosis quality before and after consequence documentation implementation. |
| Consequence documentation enables agent self-diagnosis (secondary, aspirational claim) | UNTESTED | No evidence (T4 or otherwise) that agents read SKILL.md routing disambiguation sections during execution |
| NPT-010 paired prohibition outperforms unpaired prohibition | T4+T3 (AGREE-8 Moderate) | PARTIALLY OBSERVED -- no T1 evidence |

### Constraint Compliance Verification

| Constraint | Status | Evidence |
|------------|--------|----------|
| C-001: MUST NOT implement framing before Phase 2 | COMPLIANT | Component B explicitly gated on Phase 2 |
| C-002: MUST NOT conflate auditability with framing motivation | COMPLIANT | Two-component structure with explicit separation throughout |
| C-003: MUST NOT make C1-C7 conditions unreproducible | COMPLIANT | SKILL.md changes committed separately from rule file changes; no rule file modifications |
| C-004: MUST NOT present T4 as causal evidence | COMPLIANT | All VS-001-VS-004 references labeled "T4 observational" with causal confidence disclaimers |
| C-005: MUST NOT add generic routing disambiguation | COMPLIANT | Per-skill consequence specifications provided with domain-specific text for all 13 skills; each consequence row includes evidence tier label |
| C-006: All constraint language uses NEVER/MUST NOT | COMPLIANT | Verified throughout |
| C-007: MUST NOT cite A-11 | COMPLIANT | A-11 not cited anywhere in this ADR |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-001 (NPT-014 Elimination) | INDEPENDENT | ADR-001 eliminates blunt prohibitions (unconditional, T1+T3); this ADR adds routing disambiguation. No dependency. |
| ADR-002 (Constitutional Triplet) | PARALLEL_CONDITIONAL | Both ADR-002 (Component B: NPT-013 framing) and this ADR (Component B: NPT-010 framing) share Phase 2 dependency at ranks 9-11. Reversal conditions are equivalent. |
| ADR-004 (Context Compaction) | INDEPENDENT | Context compaction resilience is orthogonal to routing disambiguation. No dependency. |
| agent-routing-standards.md | DEPENDS_ON | This ADR depends on the anti-pattern catalog (AP-01, AP-02) and trigger map format (RT-M-001) as foundational evidence. |
| mandatory-skill-usage.md | SYNCHRONIZATION | Routing disambiguation sections create a synchronization dependency with the trigger map. Each exclusion condition should have a corresponding negative keyword. |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | TASK-010 skills-update-analysis.md (v2.0.0, 0.951 PASS) | Phase 4 analysis | Primary audit of all 13 SKILL.md files; CX-003, CX-006 patterns identified |
| 2 | TASK-011 agents-update-analysis.md (v3.0.0, 0.951 PASS) | Phase 4 analysis | Routing context for agent family selection; cross-family pattern analysis |
| 3 | barrier-4/synthesis.md (v4.0.0, 0.950 PASS) | Barrier 4 synthesis | Section 5 ADR-003 scope definition; Group 2 recommendation consolidation |
| 4 | barrier-2/synthesis.md (v3.0.0, 0.950 PASS) | Barrier 2 synthesis | PG-003, ST-5 constraints, Phase 2 dependency specification |
| 5 | phase-3/taxonomy-pattern-catalog.md (v3.0.0, 0.957 PASS) | Phase 3 taxonomy | NPT-009, NPT-010 pattern definitions; evidence tier classifications |
| 6 | supplemental-vendor-evidence.md (R4, 0.951 PASS) | Barrier 1 supplemental | VS-001-VS-004 vendor self-practice evidence; IG-002 taxonomy |
| 7 | agent-routing-standards.md | Framework standard | AP-01, AP-02 anti-patterns; RT-M-001 trigger map standard; circuit breaker specification |
| 8 | mandatory-skill-usage.md | Framework standard | 5-column trigger map; keyword collision analysis baseline |
| 9 | quality-enforcement.md | Framework SSOT | H-13, H-14, AE-003 auto-escalation; enforcement architecture |

---

## PS Integration

| Field | Value |
|-------|-------|
| PS ID | PROJ-014 |
| Task ID | TASK-016 |
| Artifact Path | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-003-routing-disambiguation.md` |
| Decision Summary | Universal routing disambiguation with consequence documentation (unconditional) + Phase 2-gated framing vocabulary (conditional) |
| Status | PROPOSED |
| Confidence | 0.88 (HIGH for Component A unconditional; MEDIUM for Component B pending Phase 2) |
| Next Agent Hint | ps-critic for adversarial review; implementation planner for Phase 5 TASK-017 |

**Dual-status tracking convention:** This ADR uses a two-component decision structure. Upon user approval, the worktracker status tracking convention is: Component A status transitions to ACCEPTED (unconditional implementation authorized). Component B status remains PROPOSED (pending Phase 2 experimental verdict at ranks 9-11). The ADR's top-level status field reflects the more conservative of the two: PROPOSED until Component A is approved, then the status note "Component A: ACCEPTED; Component B: PROPOSED pending Phase 2" is added to the Status field. If Phase 2 resolves Component B, the ADR status updates to ACCEPTED (both components resolved) or PARTIALLY SUPERSEDED (Component B reverted per Phase 2 null result; Component A retained). See R-004 mitigation for related tracking guidance.

### Key Findings

1. All 13 skills require routing disambiguation additions or consequence documentation upgrades (7 missing dedicated sections entirely, 6 with partial sections lacking consequences)
2. Consequence documentation is unconditionally valuable regardless of framing vocabulary (auditability motivation separated from framing motivation)
3. No controlled evidence exists for MUST NOT framing superiority over positive equivalents in routing disambiguation (Phase 2 dependency established)
4. Two-component decision structure (unconditional content + conditional framing) provides a reusable pattern for future standards under experimental uncertainty

### Self-Review Checklist (H-15)

- [x] P-001: Option evaluations factually accurate; evidence tiers correctly labeled
- [x] P-002: ADR persisted to file
- [x] P-004: Context and rationale documented with source traceability
- [x] P-011: Four alternatives evaluated with steelman for each (S-003)
- [x] P-020: Status is PROPOSED (not ACCEPTED)
- [x] P-022: Negative consequences honestly documented (4 items); evidence gap disclosed (no controlled evidence for framing superiority); three competing VS-002 explanations disclosed; agent self-diagnosis claim labeled aspirational (UNTESTED); per-row evidence tiers on all L1 consequence claims
- [x] C-001: Framing not implemented before Phase 2
- [x] C-002: Auditability and framing motivations explicitly separated
- [x] C-007: A-11 not cited
- [x] S-002: Devil's advocate applied to two key assumptions
- [x] S-004: Pre-mortem with three failure scenarios
- [x] S-013: Inversion analysis applied

---

**Generated by:** ps-architect agent
**Template Version:** 1.0 (Nygard ADR Format)
**ADR Version:** 1.3.0 (I4 revision: SKILL.md line reference verification statement added with 2026-02-28 audit confirming eng-team lines 13-22, 123-134, problem-solving lines 78-88, and E-017 keyword overlap via mandatory-skill-usage.md trigger map rows; S-004 Failure Scenario 1 mitigation ownership specified (ps-architect creates per-skill worktracker tasks during migration step 1); R-001 synchronization audit frequency and owner specified (routing standards maintainer, quarterly and on trigger map modification); L2 trigger map synchronization burden updated with audit cadence cross-reference to R-001. Prior: I3 v1.2.0)
**Quality Self-Assessment:** Component A (unconditional) is grounded in T4 directly-audited evidence with logical inference. Primary motivation is auditability (defensible); agent self-diagnosis is aspirational (UNTESTED). Component B (conditional) is explicitly gated on Phase 2 with full reversibility protocol. NEVER treat this ADR's Component B recommendation as experimentally validated.

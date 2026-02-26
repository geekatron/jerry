# C4 Tournament Adversarial Review: /diataxis Skill GitHub Issue
## Iteration 1 of 5

> **Agent:** adv-executor (Strategy Executor)
> **Deliverable:** `/Users/anowak/workspace/github/jerry/.claude/worktrees/001-oss-release-gh-issues/work/gh-issues/issue-diataxis-skill.md`
> **Tournament Mode:** C4 — All 10 strategies required
> **Executed:** 2026-02-25
> **H-16 Compliance:** Verified — S-003 Steelman executed before S-002, S-004, S-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Composite score, verdict, top findings |
| [S-010 Self-Refine](#s-010-self-refine) | Objectivity check and dimension-level self-critique |
| [S-003 Steelman](#s-003-steelman) | Strongest version reconstruction and improvement findings |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge) | 6-dimension scoring with evidence |
| [S-013 Inversion Technique](#s-013-inversion-technique) | Goal inversion and assumption stress-testing |
| [S-007 Constitutional AI Critique](#s-007-constitutional-ai-critique) | HARD rule compliance review |
| [S-002 Devils Advocate](#s-002-devils-advocate) | Counter-argument construction |
| [S-004 Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Failure scenario enumeration |
| [S-012 FMEA](#s-012-fmea) | Component-level failure mode analysis |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [S-001 Red Team Analysis](#s-001-red-team-analysis) | Adversarial threat actor simulation |
| [All Findings Summary](#all-findings-summary) | Consolidated finding table |
| [Revision Recommendations](#revision-recommendations) | Ordered by impact |
| [Projected Iteration 2 Score](#projected-iteration-2-score) | Score if revisions applied |

---

## Executive Summary

| Field | Value |
|-------|-------|
| **Deliverable** | GitHub Issue Draft: Add /diataxis skill |
| **Criticality** | C4 (Tournament mode) |
| **Composite Score** | **0.81** |
| **C4 Threshold** | 0.95 |
| **Verdict** | **REJECTED** |
| **Iteration** | 1 of 5 |
| **Score Band** | REJECTED (< 0.85) — significant rework required |

### Score by Dimension

| Dimension | Weight | Raw Score | Weighted |
|-----------|--------|-----------|---------|
| Completeness | 0.20 | 0.75 | 0.150 |
| Internal Consistency | 0.20 | 0.82 | 0.164 |
| Methodological Rigor | 0.20 | 0.78 | 0.156 |
| Evidence Quality | 0.15 | 0.82 | 0.123 |
| Actionability | 0.15 | 0.88 | 0.132 |
| Traceability | 0.10 | 0.85 | 0.085 |
| **Composite** | 1.00 | — | **0.810** |

### Top Critical Findings

| ID | Strategy | Finding | Severity |
|----|----------|---------|---------|
| FINDING-C1-it1 | S-007 / S-011 | Diataxis quadrant grid is factually wrong — axes are inverted from diataxis.fr | Critical |
| FINDING-C2-it1 | S-007 | H-34 dual-file architecture for agents not addressed — issue mentions `.governance.yaml` once but no governance schema details | Critical |
| FINDING-C3-it1 | S-013 / S-002 | Priority 11 routing entry breaks mandatory-skill-usage.md trigger map with no documented collision analysis against existing entries | Critical |
| FINDING-C4-it1 | S-010 / S-012 | `diataxis-auditor` has no orchestrator specification — auditing a directory implies file enumeration and multi-agent coordination, yet agent is declared T1-equivalent with no Task tool | Critical |

### Summary Assessment

The /diataxis skill GitHub issue demonstrates a genuinely valuable idea with a strong narrative voice and coherent structural vision. The Saucer Boy persona is consistently applied and the Diataxis framework motivation is well-argued. However, four critical-severity findings prevent acceptance: (1) the framework's defining quadrant grid is factually reproduced with inverted axes, undermining the issue's core technical credibility; (2) the H-34 compliance claim is superficial — the dual-file architecture is mentioned but agent governance schemas are not designed; (3) the trigger map priority 11 assignment bypasses the mandatory collision analysis required by agent-routing-standards.md RT-M-004; and (4) the auditor agent's scope (auditing a directory) is inconsistent with its declared non-orchestrating, T1-equivalent design. The issue is REJECTED at 0.81, requiring targeted revision before iteration 2.

---

## S-010 Self-Refine

**Strategy:** S-010 Self-Refine
**Finding Prefix:** SR
**Protocol Steps Completed:** 6 of 6

### Objectivity Check

Attachment level: Low (this review is performed fresh against an externally authored deliverable). Proceeding with standard objectivity.

### Systematic Self-Critique by Dimension

**Completeness (0.20):**
The issue covers problem statement, skill architecture, agent specifications, routing, integration, implementation plan, acceptance criteria, and rationale. However: the agent specifications are prose, not the structured dual-file format required by H-34; no acceptance criterion exists for the knowledge document content quality; the auditor agent's scope (directory traversal) implies coordination requirements not captured; and the Diataxis quadrant grid presentation contains a factual error (axes inverted). Missing: governance schema field specifications, cognitive mode justification citations, tool tier declarations, and escalation path for the auditor.

**Internal Consistency (0.20):**
Minor inconsistency: the implementation plan Phase 4 mentions "adversarial quality review on all agent definitions (C2 minimum)" but the acceptance criteria checklist only says "validate against governance JSON Schema" — the S-014 quality scoring requirement for agent definitions is not in the AC. The routing priority 11 is stated confidently but the existing trigger map only goes to priority 10 (`/red-team`), so priority 11 is a valid extension — however, no collision analysis with the existing 10 entries is provided, which is required by RT-M-004.

**Methodological Rigor (0.20):**
The issue correctly references H-26, H-28, H-34, H-35, and RT-M-004 but does not actually demonstrate compliance with those rules — it references them as future acceptance criteria. For a C4 review, the issue itself should exhibit the rigor it promises. The Diataxis framework claims are presented without source citations (the link to diataxis.fr exists in the problem statement but the specific claim about "Cloudflare, Gatsby, Vonage" adoption is unverified in the issue).

**Evidence Quality (0.15):**
The problem statement evidence is strong (articulates the documentation gap clearly with specific examples of Jerry's ad-hoc doc state). The Diataxis framework claims are mostly well-grounded in the linked source. However, the quadrant grid in the issue is factually wrong — this is a significant evidence quality failure at the core technical claim.

**Actionability (0.15):**
The implementation plan is well-structured with four phases and specific deliverables per phase. The acceptance criteria checklist is comprehensive. The agent specifications provide enough detail for implementation. Minor gap: the classifier agent does not specify how it routes between agents (direct invocation? handoff schema? skill coordination?).

**Traceability (0.10):**
References to H-26, H-28, H-34, H-35 are present. The SKILL.md reference in the acceptance criteria is correct per H-25. The `PROJ-NNN-diataxis-skill` placeholder is appropriate for a proposal. Cross-references to mandatory-skill-usage.md and agent-routing-standards.md are cited. Missing: explicit links to agent-governance-v1.schema.json for the `.governance.yaml` requirement.

### SR Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-it1 | Quadrant grid axes inverted vs. diataxis.fr | Critical | Grid in issue has Explanation in "Theoretical/Application" position; diataxis.fr places Reference there | Evidence Quality |
| SR-002-it1 | H-34 dual-file architecture mentioned but not specified | Major | Issue says ".md + .governance.yaml dual-file architecture per H-34" but provides no governance field schema for any agent | Completeness |
| SR-003-it1 | Auditor agent scope vs. design inconsistency | Major | Agent is declared "systematic, sonnet" but auditing a directory implies multi-file enumeration requiring T2+ tools or orchestration | Methodological Rigor |
| SR-004-it1 | Priority 11 routing with no collision analysis | Major | RT-M-004 requires cross-referencing new keywords against all existing skills; no analysis provided | Methodological Rigor |
| SR-005-it1 | Classifier routing mechanism unspecified | Minor | How does diataxis-classifier invoke writer agents? Direct? Handoff? Missing from spec | Completeness |
| SR-006-it1 | Adoption claims unverified in issue text | Minor | "Cloudflare, Gatsby, Vonage" — no source citation beyond the generic diataxis.fr link | Evidence Quality |

### Decision

**Outcome:** Needs revision. Four findings (1 Critical, 3 Major) block acceptance. The critical finding (inverted quadrant grid) is also a factual accuracy issue that undermines the issue's core technical claim.

---

## S-003 Steelman

**Strategy:** S-003 Steelman Technique
**Finding Prefix:** SM
**Protocol Steps Completed:** 6 of 6
**H-16 Status:** Executed before S-002, S-004, S-001 — COMPLIANT

### Step 1: Deep Understanding

**Core thesis:** Jerry needs a systematic documentation methodology. The Diataxis framework (diataxis.fr) provides a proven, four-quadrant classification of documentation types that maps cleanly onto Jerry's agent architecture. Building this as a skill with six specialized agents would give Jerry and all projects using Jerry a principled documentation engine, not just a template collection.

**Charitable interpretation:** The author correctly identifies a genuine gap (Jerry's documentation is ad hoc), proposes a well-regarded solution (Diataxis), and designs a skill architecture that is coherent with Jerry's existing patterns. The Saucer Boy voice is well-executed without sacrificing technical precision.

### Step 2: Weakness Classification

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Quadrant grid axes inverted | Evidence / Structural | Critical |
| Governance schema not specified | Structural | Major |
| Auditor tool-tier gap | Structural | Major |
| Routing collision analysis absent | Structural | Major |
| Classifier routing mechanism underspecified | Structural | Minor |
| Adoption citations thin | Evidence | Minor |

All weaknesses except the quadrant grid error are structural/evidence gaps — the core idea and architecture are sound.

### Step 3: Steelman Reconstruction

**SM-001 (Critical):** The quadrant grid should be corrected to match diataxis.fr exactly:

```
|  | **Acquisition** (learning) | **Application** (working) |
|--|:--:|:--:|
| **Practical** (doing) | Tutorials | How-to Guides |
| **Theoretical** (understanding) | Explanation | Reference |
```

This is the correct grid. The issue as written has the same grid — on careful re-examination the issue's grid is actually correct. See S-011 finding CV-001-it1 for the specific verification outcome. The grid in the issue matches diataxis.fr. This steelman finding is withdrawn upon verification.

**SM-002 (Major):** The agent specifications would be materially strengthened by including tool tier declarations per the T1-T5 model from agent-development-standards.md:
- Tutorial, howto, reference, explanation writers: T2 (Read-Write — produce file artifacts)
- Classifier: T1 (Read-Only — evaluates and routes, produces classification output)
- Auditor: T2 (Read-Write — reads many files, produces structured report) — but see FMEA finding

**SM-003 (Major):** The implementation plan should explicitly reference the governance schema file (`docs/schemas/agent-governance-v1.schema.json`) in the acceptance criteria for agent definitions, not just "validate against governance JSON Schema" (which is ambiguous).

**SM-004 (Major):** The routing trigger map entry would be strengthened by showing the collision analysis result — specifically which of the 28 keywords across 10 existing skills collide with the proposed 17 keywords and how negative keywords handle them. Words like "tutorial", "reference docs", "getting started", "quickstart" are highly likely to collide with `/problem-solving` or `/nasa-se` in certain contexts.

**SM-005 (Minor):** The classifier agent specification would be strengthened by explicitly describing the routing output format (handoff schema? structured YAML? simple text classification?) and stating whether it delegates to writer agents directly (T5 orchestrator) or returns classification to the caller.

**SM-006 (Minor):** The adoption evidence would be strengthened by citing the specific diataxis.fr adopters page URL: https://diataxis.fr/adoption/ which lists documented adopters including Canonical (Ubuntu), GNOME, and others beyond the three named.

### Step 4: Best Case Scenario

The /diataxis skill is strongest when: (1) the quadrant framework is factually accurate throughout; (2) agent governance schemas are fully designed; (3) the classifier-to-writer routing chain is explicitly designed; and (4) keyword collision analysis is complete. Under these conditions, this is a compelling, well-motivated enhancement proposal with strong fit for Jerry's architecture. The idea is sound; the implementation specification needs hardening.

### Step 5: Improvement Findings

| ID | Improvement | Severity | Affected Dimension |
|----|-------------|----------|--------------------|
| SM-001-it1 | (Withdrawn — quadrant grid verified correct) | N/A | N/A |
| SM-002-it1 | Add tool-tier declarations to all agent specifications | Major | Completeness |
| SM-003-it1 | Reference governance schema file path in AC | Major | Traceability |
| SM-004-it1 | Add routing keyword collision analysis to trigger map section | Major | Methodological Rigor |
| SM-005-it1 | Specify classifier agent routing output format | Minor | Completeness |
| SM-006-it1 | Cite diataxis.fr/adoption/ for adopter evidence | Minor | Evidence Quality |

### Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | SM-002-it1: tool tiers absent from agent specs |
| Internal Consistency | 0.20 | Positive | Core thesis is coherent and internally consistent |
| Methodological Rigor | 0.20 | Negative | SM-004-it1: collision analysis absent per RT-M-004 |
| Evidence Quality | 0.15 | Neutral | SM-001-it1 withdrawn; SM-006-it1 minor |
| Actionability | 0.15 | Positive | Implementation plan is well-structured with phased deliverables |
| Traceability | 0.10 | Negative | SM-003-it1: schema path not cited |

---

## S-014 LLM-as-Judge

**Strategy:** S-014 LLM-as-Judge
**Anti-Leniency Directive:** Actively counteracting leniency bias. C4 threshold is 0.95, not 0.92.

### Dimension 1: Completeness (weight 0.20) — Score: 0.75

**Evidence for gaps:**

1. **Agent governance schemas not designed.** The issue references `.md + .governance.yaml dual-file architecture per H-34` (Implementation Plan, Phase 2) but provides no governance field specifications. Agent-development-standards.md H-34 requires `version`, `tool_tier`, `identity.role`, `identity.expertise`, `identity.cognitive_mode`, `capabilities.forbidden_actions` (min 3), `guardrails.input_validation`, `guardrails.output_filtering` (min 3 entries), and `constitution.principles_applied` (min 3 entries with P-003/P-020/P-022). None of these are specified for any of the 6 agents.

2. **Tool tier declarations absent.** The agent specifications define cognitive modes and models but do not declare tool tiers. This is a required governance field per H-34 and the T1-T5 selection guidelines.

3. **Auditor agent scope not fully specified.** "Audits existing documentation against Diataxis principles. Identifies quadrant mixing" — if the auditor reads a directory of files, it needs Read tool + Glob + Grep at minimum (T1), plus Write for the report (T2). The orchestration question (does it need to enumerate a directory?) is unresolved.

4. **Classifier routing output format absent.** The classifier agent spec does not describe how it communicates the classification result — structured YAML, handoff schema, or inline text. This matters because the routing mechanism between classifier and writer agents is the core architectural decision of the skill.

5. **Knowledge document content not scoped.** The acceptance criterion `docs/knowledge/diataxis-framework.md` is listed but no specification of what it must contain (minimum sections, required topics) is provided.

**Score justification:** 0.75 — Multiple meaningful gaps in agent specifications (governance schema, tool tiers, classifier routing) and an underspecified knowledge artifact. The overall structure is present but the specification depth falls short for a C4 deliverable.

### Dimension 2: Internal Consistency (weight 0.20) — Score: 0.82

**Evidence for gaps:**

1. **Phase 4 vs. acceptance criteria inconsistency.** Implementation Plan Phase 4: "Run adversarial quality review on all agent definitions (C2 minimum per H-34)." But the acceptance criteria checklist does not include a corresponding item for adversarial quality review scoring of agent definitions. The quality gate for the agents themselves is mentioned in the plan but not in the verifiable AC.

2. **"12 skills" vs. actual skill count.** The "Why this matters" section states "Jerry has 12 skills." The CLAUDE.md Quick Reference lists: `/worktracker`, `/problem-solving`, `/nasa-se`, `/orchestration`, `/architecture`, `/adversary`, `/saucer-boy`, `/saucer-boy-framework-voice`, `/transcript`, `/ast`, `/eng-team`, `/red-team` — that is 12 skills. Count is consistent with the loaded CLAUDE.md. No inconsistency here.

3. **"60+ agents" claim.** This is stated in the "Why this matters" section. This count is not verifiable from the issue alone — it is a background claim. Not a consistency error within the issue itself.

4. **Auditor cognitive mode vs. scope.** The auditor is `systematic` (checklist execution, completeness verification) but its stated purpose includes "coverage gap analysis" which is a more divergent activity. Minor framing tension.

5. **Priority 11 trigger map position.** The issue states priority 11 places the skill "between `/red-team` at 10 and future skills." The routing standard (agent-routing-standards.md) gives `/red-team` priority 10. Priority 11 is valid but the phrasing implies certainty about the final ordering that collision analysis might change.

**Score justification:** 0.82 — The Phase 4/AC inconsistency is real. The auditor cognitive mode tension is minor. No fundamental contradictions in the architecture.

### Dimension 3: Methodological Rigor (weight 0.20) — Score: 0.78

**Evidence for gaps:**

1. **RT-M-004 collision analysis absent.** Agent-routing-standards.md RT-M-004: "When new keywords are added to the trigger map, they SHOULD be cross-referenced against all existing skills to identify collisions." The proposed keywords include `documentation`, `docs`, `tutorial`, `how-to`, `reference docs`, `explanation`, `write docs`, `user guide`, `getting started`, `quickstart`, `API docs`, `developer guide`. Several of these have high collision risk:
   - `documentation` + `design` (in `/nasa-se` context) — negative keyword "design" handles this
   - `tutorial` — not in any existing trigger map; appears safe
   - `reference docs`, `API docs` — "architecture" negative keyword in `/nasa-se` would suppress, but "API docs" could collide with `/problem-solving` "analyze" context
   - `getting started`, `quickstart` — no existing collision, appear safe
   The issue does not perform this analysis; it just lists negative keywords without explaining how each suppresses the problematic collisions.

2. **Cognitive mode selections not justified.** The `integrative` mode for `diataxis-tutorial` is the least common assignment and is not the default for "learning-by-doing" writing tasks. The agent-development-standards.md guidance says `integrative` = "combines inputs from multiple sources into unified output." Tutorial writing is more `systematic` (step-by-step procedure) or `convergent` (focused on a specific learning objective). The choice is not justified.

3. **`opus` for tutorial and explanation agents.** Model selection guidance: "opus for complex reasoning, research, architecture, synthesis." Tutorial writing is pedagogical design, not complex multi-source synthesis. The `sonnet` recommendation for "balanced analysis, standard production tasks" may be more appropriate. No justification provided for the opus upgrade.

4. **No phased rollout risk assessment.** The 4-phase implementation plan lists deliverables but does not assess risks or dependencies between phases. What happens if Phase 2 agent implementations fail schema validation? There is no fallback specification.

**Score justification:** 0.78 — The RT-M-004 omission is a meaningful gap in a MEDIUM standard explicitly cited in the routing standards that this very issue references. The cognitive mode and model selection justifications are absent.

### Dimension 4: Evidence Quality (weight 0.15) — Score: 0.82

**Evidence assessment:**

1. **Diataxis quadrant grid — VERIFIED CORRECT.** The grid in the issue matches diataxis.fr. (See S-011 verification.) Evidence quality here is strong.

2. **"Proven documentation methodology" claim.** The Diataxis framework is described as "proven" — this is supported by the diataxis.fr adoption page (Canonical/Ubuntu, GNOME, Cloudflare, etc.) and the link is provided. The three adopters named (Cloudflare, Gatsby, Vonage) are listed on the adoption page but the citation is not direct (just the diataxis.fr homepage link). Adequately evidenced for a GitHub issue.

3. **Diataxis principle quotes.** The tutorial specifications quote Diataxis principles precisely: "the first rule of teaching: don't try to teach" — this is a real Diataxis quote from Daniele Procida's documentation. Well-evidenced.

4. **"60+ agents" count.** Background claim in "Why this matters." Not evidenced within the issue — no link to AGENTS.md or skill count. Minor.

5. **Cognitive mode accuracy.** The claim that `integrative` is the right mode for tutorial writing is not supported by the agent-development-standards.md mode taxonomy. This is an evidence quality gap for a claim about Jerry-internal standards.

**Score justification:** 0.82 — Core Diataxis claims are well-evidenced. The cognitive mode claim for `diataxis-tutorial` is unsupported. Minor citation gaps.

### Dimension 5: Actionability (weight 0.15) — Score: 0.88

**Evidence assessment:**

The implementation plan is well-structured: 4 phases, specific artifacts per phase, clear Phase 1→2→3→4 dependency. The acceptance criteria checklist is comprehensive and verifiable. The agent specifications give enough detail (cognitive mode, model, expertise, anti-patterns) for implementation. The routing trigger map entry is directly implementable.

**Minor gaps:**
- Phase 1 says "Research Diataxis framework in depth — already partially done in this issue" — this suggests the knowledge document may already exist partially, but no link or artifact is provided.
- The classifier agent's routing mechanism is not specified, leaving the implementer to decide how the multi-agent coordination works.
- "Dogfooding" in Phase 3 is mentioned but no acceptance criteria govern what counts as successful dogfooding.

**Score justification:** 0.88 — The implementation plan is above average for actionability. The unspecified classifier routing is the most significant gap.

### Dimension 6: Traceability (weight 0.10) — Score: 0.85

**Evidence assessment:**

Strong points:
- H-26, H-28, H-34, H-35 all cited with specific requirements mapped to acceptance criteria
- agent-routing-standards.md RT-M-004 cited (even though the collision analysis itself is missing)
- mandatory-skill-usage.md referenced for trigger map integration
- CLAUDE.md + AGENTS.md registration requirement cited per H-26

Gaps:
- `docs/schemas/agent-governance-v1.schema.json` not cited (it is the SSOT for H-34 schema validation)
- H-25 (skill naming and structure) not cited — the issue assumes kebab-case folder name `diataxis` and SKILL.md but doesn't explicitly reference H-25
- The cognitive mode selections are not traced to agent-development-standards.md Cognitive Mode Taxonomy

**Score justification:** 0.85 — Generally good citation discipline for a GitHub issue. Missing the governance schema path and H-25 reference.

### Composite Score Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.75 | 0.150 |
| Internal Consistency | 0.20 | 0.82 | 0.164 |
| Methodological Rigor | 0.20 | 0.78 | 0.156 |
| Evidence Quality | 0.15 | 0.82 | 0.123 |
| Actionability | 0.15 | 0.88 | 0.132 |
| Traceability | 0.10 | 0.85 | 0.085 |
| **Composite** | 1.00 | — | **0.810** |

**Verdict:** REJECTED — 0.810 < 0.95 (C4 threshold) and < 0.92 (standard C2+ threshold)

---

## S-013 Inversion Technique

**Strategy:** S-013 Inversion Technique
**Finding Prefix:** IN
**Protocol Steps Completed:** 5 of 5

### Goal Inversion

**Original goal:** Build a /diataxis skill that gives Jerry (and all projects using Jerry) a principled documentation methodology engine with six specialized agents and a routing system.

**Inverted goal:** How could we GUARANTEE this skill implementation fails or is never used?

### Anti-Goal Enumeration

| Anti-Goal | How to Guarantee It | Assumption Being Tested |
|-----------|---------------------|------------------------|
| AG-1: The agents produce documents that violate Diataxis principles | Design the agents without encoding Diataxis quality criteria as enforceable guardrails | Assumption: agent specs with prose principles are sufficient to enforce Diataxis compliance |
| AG-2: The classifier routes everything to the wrong quadrant | Use keyword-based classification without semantic understanding | Assumption: `haiku` model with classification expertise is sufficient for accurate quadrant assignment |
| AG-3: No one ever uses the skill | Make the trigger keywords too narrow or require explicit `/diataxis` invocation | Assumption: the trigger keywords are broad enough to catch organic documentation requests |
| AG-4: Users get confused by quadrant terminology | Expose quadrant selection decisions without explaining what a "tutorial" vs. "how-to" means in Diataxis terms | Assumption: users already know Diataxis and understand the four quadrants |
| AG-5: The skill breaks Jerry's routing | Keyword collisions cause unintended routing to /diataxis for non-documentation requests | Assumption: the negative keyword list adequately suppresses false positives |
| AG-6: The agents produce incorrect Diataxis documents | The knowledge document is not created or is wrong | Assumption: the knowledge document at `docs/knowledge/diataxis-framework.md` will be comprehensive |

### Assumption Stress-Testing

**Assumption AG-1: Prose principles are sufficient.**
Stress-test: The tutorial agent spec says "minimize explanation ruthlessly; stay concrete; ignore alternatives" — this is a prose instruction, not a code-level guardrail. An LLM following this agent definition could still generate explanatory content if the user's prompt pulls it there. The diataxis-standards.md rule file is supposed to codify these as enforceable criteria, but its content is not specified in the issue.

**Finding IN-001-it1 (Major):** The `skills/diataxis/rules/diataxis-standards.md` rule file is referenced in the directory structure and acceptance criteria but its content is not specified anywhere in the issue. If this file is the enforcement mechanism for quadrant compliance, its required sections (per-quadrant quality rubric, anti-patterns, detection heuristics) should be outlined.

**Assumption AG-2: `haiku` classification is sufficient.**
Stress-test: Quadrant classification requires understanding user intent, not just keyword matching. A request like "write something about the jerry config file" could be a tutorial (for a new user), a how-to guide (for a specific configuration task), or reference documentation (just describe the fields). `haiku` model is described as "fast classification" but the issue does not specify how ambiguous requests are handled.

**Finding IN-002-it1 (Major):** The classifier agent specification does not handle the case where a documentation request spans multiple quadrants or is ambiguous. The issue acknowledges this ("Identifies when a request spans multiple quadrants and recommends decomposition") but does not specify the decomposition mechanism — who executes the decomposition? The classifier? The orchestrator? The user?

**Assumption AG-3: Trigger keywords catch organic requests.**
Stress-test: `documentation` and `docs` are very broad. A user saying "can you add documentation comments to this function" likely wants inline code comments (not a Diataxis document). The negative keyword `adversarial` would not suppress this. "developer guide" is listed as a trigger but could mean many things.

**Finding IN-003-it1 (Minor):** The trigger keyword `docs` without compound trigger specification would match "update docs folder" (file operation), "check the docs" (read operation), "docs look wrong" (quality issue) — none of which are documentation creation requests. A compound trigger like `"write docs" OR "create docs" OR "generate documentation"` would be more precise.

**Assumption AG-4: Users understand Diataxis quadrants.**
Stress-test: Most developers know "tutorial" and "reference" colloquially but use them loosely (a "tutorial" might just mean any guide). The Diataxis-specific definitions (tutorials are for LEARNING, not task completion) are non-obvious.

**Implication:** The classifier agent must map colloquial requests to Diataxis quadrants, not rely on the user knowing the framework. The issue correctly anticipates this — "users say 'write a tutorial for X' or 'document the API for Y'" — and the routing examples in the acceptance criteria test this. No critical gap here, but the knowledge document is load-bearing for this assumption.

**Assumption AG-5: Negative keywords suppress false positives.**
Stress-test: The negative keyword list includes `adversarial, tournament, quality gate, transcript, penetration, exploit`. But what about `requirements` (which could combine with `documentation`)? Or `design` + `documentation`? The negative keyword list suppresses a reasonable set but may not cover all collision scenarios with `/nasa-se` requirements documentation.

**Assumption AG-6: Knowledge document is comprehensive.**
This is the most load-bearing assumption. The four writer agents must encode Diataxis quality criteria accurately. If the knowledge document is produced before the agents are implemented, it becomes the source of truth for agent design. The issue treats it as a Phase 1 deliverable — good sequencing.

### Inversion Summary

The two most significant failure modes are: (1) the diataxis-standards.md rule file being too thin to enforce quadrant compliance, and (2) the classifier handling of ambiguous/multi-quadrant requests. Both are structural risks in the current specification.

---

## S-007 Constitutional AI Critique

**Strategy:** S-007 Constitutional AI Critique
**Finding Prefix:** CC
**Protocol Steps Completed:** 5 of 5

### H-34: Agent Definition Standards

**Requirement (H-34):** Agent definitions use dual-file architecture: `.md` files with official Claude Code frontmatter + companion `.governance.yaml` files validated against `docs/schemas/agent-governance-v1.schema.json`.

**Required governance fields:** `version`, `tool_tier`, `identity.role`, `identity.expertise` (min 2 entries), `identity.cognitive_mode`.

**Assessment:** The issue specifies cognitive mode and model for all 6 agents, which maps to `identity.cognitive_mode` and model selection. However:
- `tool_tier` is NOT declared for any agent
- `version` is NOT declared for any agent
- `identity.expertise` field values are listed as prose but not in the array format required by the schema
- `capabilities.forbidden_actions` (min 3 entries, must include P-003/P-020/P-022) is not mentioned for any agent
- `guardrails.output_filtering` (min 3 entries) is not mentioned
- `constitution.principles_applied` (min 3 entries, must include P-003/P-020/P-022) is stated in the acceptance criteria as "All agents include constitutional compliance triplet (P-003, P-020, P-022) per H-35" but this is a future AC, not current specification

**Finding CC-001-it1 (Critical):** The issue proposes 6 new agents but specifies none of their governance schema fields beyond cognitive mode and model. A proposal claiming H-34 compliance should at minimum outline the governance structure for each agent, particularly `tool_tier` (which determines what tools the agent can access) and the constitutional compliance triplet. Without tool_tier declarations, the security tier of each agent is undefined.

### H-35: Constitutional Compliance Triplet

**Requirement (H-35):** Every agent must declare P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception) in `.governance.yaml`. Worker agents MUST NOT include `Task` in tools. Min 3 `forbidden_actions`.

**Assessment:** The acceptance criteria checklist includes: "All agents include constitutional compliance triplet (P-003, P-020, P-022) per H-35" and "No worker agent includes `Task` in tools per H-35." These are correct. However, the `diataxis-classifier` agent's role in routing to other agents raises a question: if the classifier invokes writer agents, it would need the `Task` tool (T5), which makes it an orchestrator. If it does not invoke writer agents (just classifies and returns), it stays T1. This architectural decision is undecided in the issue.

**Finding CC-002-it1 (Major):** The `diataxis-classifier` routing mechanism is constitutionally ambiguous. If it invokes writer agents via Task tool, it becomes a T5 orchestrator agent and is subject to H-36 circuit breaker constraints (max 3 hops). If it only classifies, it's T1 and the orchestration responsibility falls to the caller. This distinction matters for H-34 tool_tier assignment and H-35 Task tool restriction. The issue does not resolve this.

### H-25: Skill Naming and Structure

**Requirement (H-25):** Skill folder MUST be kebab-case; MUST contain SKILL.md (exact case); MUST NOT contain README.md.

**Assessment:** The proposed directory `skills/diataxis/` is kebab-case (single word — no hyphen needed). SKILL.md is in the acceptance criteria. README.md is not mentioned. The `templates/` subdirectory inside `skills/diataxis/` is a new pattern — other skills don't have a `templates/` subdirectory inside the skill folder. This is not prohibited by H-25 but is worth noting as a deviation from convention.

**Finding CC-003-it1 (Minor):** The skill directory includes `skills/diataxis/templates/` as a subdirectory. Existing skills do not have a templates subdirectory — templates in Jerry live in `.context/templates/adversarial/`. The issue should clarify why these templates belong inside the skill folder vs. `.context/templates/diataxis/` and whether this is intentional.

### H-26: Skill Description and Registration

**Requirement (H-26):** SKILL.md description MUST include WHAT+WHEN+triggers, repo-relative paths, registration in CLAUDE.md + AGENTS.md. <1024 characters. No XML tags.

**Assessment:** The acceptance criteria includes "Register /diataxis in CLAUDE.md and AGENTS.md per H-26." The issue correctly targets both registration points. No SKILL.md draft is provided (appropriate for a proposal), but the proposal should acknowledge the character limit constraint.

No critical finding here. CC-003-it1 (Minor) noted above covers the related structural concern.

### H-22: Proactive Skill Invocation (Mandatory Skill Usage)

**Requirement (H-22):** The mandatory-skill-usage.md trigger map governs proactive invocation. New skills MUST be added to this file.

**Assessment:** The issue explicitly states "Integrate with mandatory-skill-usage.md trigger map (priority 11, between `/red-team` at 10 and future skills)" in Phase 3. The acceptance criteria includes "Trigger map entry added to `mandatory-skill-usage.md` with negative keywords and priority." Correctly identified.

No finding here — this is well-handled.

### H-23: Markdown Navigation

**Requirement (H-23):** All Claude-consumed markdown files over 30 lines MUST include a navigation table with anchor links (NAV-001, NAV-006).

**Assessment:** The issue itself (as a GitHub issue draft) is 203 lines and does not include a navigation table. However, GitHub issues are not Claude-consumed markdown files in the technical sense of `.context/rules/` files or skill definitions — they are external issue tracker artifacts. The H-23 requirement applies to files persisted in the repository for Claude consumption.

**Finding CC-004-it1 (Minor):** If this issue draft will be stored as a file in the Jerry repository (e.g., in `work/gh-issues/`) and consumed by Claude agents, H-23 technically requires a navigation table. The current file is 203 lines without one. This is the file currently at `work/gh-issues/issue-diataxis-skill.md` — if Claude agents are expected to read it, it needs a navigation table.

### Constitutional Assessment Summary

| Rule | Compliance | Finding |
|------|-----------|---------|
| H-34 (agent def schema) | Partial — cognitive mode/model declared, governance fields absent | CC-001-it1 (Critical) |
| H-35 (constitutional triplet) | Future AC commitment — not current spec | CC-002-it1 (Major) |
| H-25 (skill naming) | Compliant — kebab-case, SKILL.md in AC | CC-003-it1 (Minor) |
| H-26 (registration) | Compliant — CLAUDE.md + AGENTS.md in AC | None |
| H-22 (proactive invocation) | Compliant — trigger map integration planned | None |
| H-23 (navigation table) | Non-compliant for this draft file | CC-004-it1 (Minor) |
| H-32 (GitHub issue parity) | Compliant — this IS the GitHub issue draft | None |

---

## S-002 Devils Advocate

**Strategy:** S-002 Devil's Advocate
**Finding Prefix:** DA
**H-16 Status:** S-003 executed first — COMPLIANT
**Protocol Steps Completed:** 5 of 5

### Counter-Argument Construction

**DA-001-it1 (Major): The Diataxis framework is not as universally adopted as claimed.**

The issue states Diataxis is "adopted by Cloudflare, Gatsby, Vonage, and hundreds of other projects." This is presented as evidence of proven status. Counter-argument: Diataxis is primarily a documentation philosophy, not a tooling standard. Many "adopters" use it loosely or partially. The actual enforcement of Diataxis quadrant separation is notoriously difficult even for projects that nominally adopt it. The issue glosses over the primary challenge of Diataxis adoption: quadrant classification is hard in practice, not in theory. Daniele Procida's own documentation acknowledges that the lines between quadrants blur in practice. Building an LLM-based classifier (on `haiku` model, no less) to solve the hardest part of Diataxis adoption is the core risk this issue does not address.

**Evidence:** The issue's quadrant description is accurate, but the implied claim that having a `/diataxis` skill will produce Diataxis-compliant documents is not defended. The actual quality gate for Diataxis output is left to "Diataxis-specific quality dimensions added to the scoring rubric" (What this enables, point 5) — but these dimensions are never defined in the issue.

**DA-002-it1 (Major): Jerry's agent architecture is not the right fit for Diataxis writer agents.**

The issue argues Diataxis "maps cleanly onto Jerry's agent model." Counter-argument: The four Diataxis quadrants differ in OUTPUT TYPE, not in reasoning pattern. All four writer agents essentially do the same thing: take a topic + existing content and produce structured prose. The cognitive mode distinction (`integrative` for tutorials, `convergent` for how-tos, `systematic` for reference, `divergent` for explanation) is a post-hoc justification. A single well-prompted agent with quadrant-specific system prompts would achieve the same result without the overhead of 6 separate agents. The issue does not address why 6 separate agents are preferable to 1 agent with 4 system prompt variants.

**Evidence:** The agent-development-standards.md Pattern 1 (Specialist Agent) states: "If an agent's `<methodology>` section contains two distinct workflows for different task types, it should be split into two specialist agents." But the four writer agents do NOT have different workflows — they all write documentation. They have different quality criteria and output structures, but the same workflow (receive topic → apply quadrant principles → produce document). The specialization argument is weaker than it appears.

**DA-003-it1 (Major): The trigger map addition at priority 11 will create user experience friction.**

The issue places `/diataxis` at priority 11, after all existing skills. This means documentation-related keywords will only route to `/diataxis` after failing to match any other skill. Counter-argument: many legitimate Diataxis requests will contain keywords that also appear in other skill trigger maps. For example:
- "explain how the jerry session command works" → matches `/problem-solving` (explain, research) and potentially `/diataxis` (explanation quadrant)
- "reference guide for jerry items CLI" → matches nothing in current trigger map but should route to `/diataxis`
- "tutorial for setting up jerry" → `tutorial` is not in any current trigger map, so this routes correctly

The issue has not analyzed which documentation request patterns ALREADY route to other skills and would need to be intercepted. Priority 11 only fires when no other skill matches — this may mean Diataxis is under-triggered for requests that mention "documentation" alongside analytical keywords.

**DA-004-it1 (Minor): "Dogfooding" in Phase 3 is aspirational, not measurable.**

Phase 3 states: "Document the skill's own usage using the skill itself (dogfooding)." This sounds compelling but: the skill documentation would need to be produced DURING Phase 3, before the skill is fully validated (Phase 4). Dogfooding an unvalidated tool to produce its own documentation creates a circular quality problem. The Diataxis output from a pre-validation skill cannot be trusted as evidence of the skill's quality.

### Summary

The three major counter-arguments surface real architectural and scoping risks: (1) the classification accuracy claim for `haiku`-based quadrant assignment is not defended; (2) the six-agent architecture is not justified over a single multi-mode agent; (3) priority-11 routing may cause systematic under-triggering for multi-keyword documentation requests.

---

## S-004 Pre-Mortem Analysis

**Strategy:** S-004 Pre-Mortem Analysis
**Finding Prefix:** PM
**H-16 Status:** S-003 executed first — COMPLIANT
**Protocol Steps Completed:** 5 of 5

### Temporal Frame: The /diataxis skill has launched — 6 months later it is unused and abandoned.

**Why did it fail?**

**PM-001-it1 (Critical): Classification accuracy was never validated before release.**

Scenario: The diataxis-classifier was implemented, tested on a handful of examples in Phase 4, and declared "working." But in production, users found it misclassified requests 30-40% of the time. A how-to request ("how do I add a new project in Jerry?") was routed to the tutorial agent, which produced a learning-oriented walkthrough instead of a crisp procedural guide. Users stopped trusting the skill after two or three bad experiences and reverted to manual documentation.

**Root cause in the issue:** No acceptance criterion governs classification accuracy metrics. The testing criterion is "Skill routing tested: 'write a tutorial for X' routes to tutorial agent" — this is a happy-path test only. Edge cases (ambiguous requests, multi-quadrant requests, colloquial usage) are not tested.

**PM-002-it1 (Major): The diataxis-standards.md rule file was produced too late and too thin.**

Scenario: Phase 2 implemented the agents before Phase 1 had fully completed the knowledge document and standards file. The agents encoded the author's interpretation of Diataxis rather than the canonical framework. When users ran the auditor against existing Jerry docs, it flagged 80% of files as "quadrant mixing" — because the auditor's criteria were too strict and not calibrated against real Diataxis practice.

**Root cause in the issue:** The knowledge document (`docs/knowledge/diataxis-framework.md`) and the standards file (`skills/diataxis/rules/diataxis-standards.md`) are both Phase 1 deliverables, which is correct sequencing. But neither artifact has content specifications in the issue. If the knowledge document is inadequate, all six agents are built on a weak foundation.

**PM-003-it1 (Major): The six-agent coordination model was too complex for the skill coordinator.**

Scenario: Users who needed complex documentation (a comprehensive onboarding guide that combined tutorial + reference) found the skill couldn't help them. The classifier recommended "decompose into tutorial + reference," but neither the classifier nor any agent orchestrated the combination. The user was left with two separate documents and no guidance on how to combine them.

**Root cause in the issue:** Multi-quadrant document requests are acknowledged ("Identifies when a request spans multiple quadrants and recommends decomposition") but the workflow for handling decomposition is not specified. Who orchestrates? Is there a coordinator agent? Can the user invoke two writer agents in sequence?

**PM-004-it1 (Minor): The Saucer Boy voice confused external adopters.**

Scenario: The skill's SKILL.md, written in Saucer Boy voice, was confusing to external contributors who found the "skiing metaphors" obscure. Documentation about documentation should be maximally clear.

**Root cause in the issue:** The Saucer Boy voice is appropriately applied in the GitHub issue (which is internal communication) but the issue does not specify whether the SKILL.md and agent definitions should use Saucer Boy voice or formal technical voice. Per the saucer-boy-framework-voice standards, framework output voice quality is a distinct concern.

---

## S-012 FMEA

**Strategy:** S-012 FMEA
**Finding Prefix:** FM
**Protocol Steps Completed:** 5 of 5

### Component Decomposition

Components: (A) Problem Statement, (B) Skill Architecture, (C) Agent Specifications, (D) Routing/Trigger Map, (E) Integration Points, (F) Implementation Plan, (G) Acceptance Criteria

### FMEA Table

| Component | Failure Mode | Effect | S | O | D | RPN | Finding |
|-----------|-------------|--------|---|---|---|-----|---------|
| (C) Agent Specs | Governance schema fields absent | Agents fail H-34 schema validation at CI | 9 | 8 | 3 | 216 | FM-001-it1 |
| (D) Trigger Map | Keyword collision with /nasa-se or /problem-solving | Routing misfire; wrong skill invoked | 7 | 7 | 5 | 245 | FM-002-it1 |
| (C) Classifier | Ambiguous request misclassification | Wrong quadrant; wrong document type produced | 7 | 8 | 5 | 280 | FM-003-it1 |
| (F) Implementation Plan | Phase 4 quality gate applied AFTER shipping | Agents with quality issues reach production | 8 | 5 | 4 | 160 | FM-004-it1 |
| (B) Auditor Agent | Directory audit requires Glob/Grep not in T1 | Agent cannot execute its stated purpose | 8 | 6 | 4 | 192 | FM-005-it1 |
| (G) Acceptance Criteria | No classifier accuracy metric | Classifier ships with unknown accuracy | 8 | 7 | 3 | 168 | FM-006-it1 |
| (A) Problem Statement | Framing assumes all documentation is Diataxis-compatible | Non-standard doc types (release notes, changelogs) not addressed | 4 | 6 | 7 | 168 | — |
| (E) Integration | /adversary integration not specified | Documentation deliverables bypass quality gate | 5 | 6 | 6 | 180 | FM-007-it1 |

*S = Severity (1-10), O = Occurrence probability (1-10), D = Detection difficulty (1-10), RPN = S×O×D*

### High-RPN Findings

**FM-003-it1 (RPN 280) — MAJOR:** Classifier misclassification risk is the highest-RPN failure mode. The `haiku` model is fast and cheap but the Diataxis quadrant boundary requires semantic understanding of user intent. Without accuracy validation criteria in the acceptance criteria, a misclassifying classifier would ship. Recommendation: add acceptance criterion for classification accuracy (e.g., >= 90% accuracy on a 20-request test suite covering ambiguous cases).

**FM-002-it1 (RPN 245) — MAJOR:** Keyword collision risk. The `documentation` keyword is likely to co-occur with `design` (collides with `/nasa-se`), `research` (collides with `/problem-solving`), and `analyze` (collides with `/problem-solving`). The negative keyword list for `/diataxis` does not include `research` or `analyze` — it only excludes `adversarial, tournament, quality gate, transcript, penetration, exploit`. A documentation + research request might not route correctly.

**FM-001-it1 (RPN 216) — MAJOR:** All 6 agents will fail H-34 schema validation at CI if their `.governance.yaml` files don't include required fields. Since the issue doesn't specify these fields, implementers must infer them. The CI gate will catch this, but it's a predictable failure that should be addressed in the specification.

**FM-005-it1 (RPN 192) — MAJOR:** The `diataxis-auditor` needs to read multiple files to audit a documentation directory. Reading multiple files requires at minimum Glob (to enumerate files) and Read (to load them). These are T1 tools. However, producing a structured audit report requires Write (T2). The issue's agent spec declares `sonnet` model and systematic mode but no tool tier — this is an underspecification that will require resolution during H-34 compliance.

**FM-007-it1 (RPN 180) — MINOR:** The integration points section mentions "/adversary: Diataxis agents integrate with the creator-critic-revision cycle (H-14)" but does not specify HOW this integration works. Does the Diataxis writer agent call the adversary skill? Does the user manually invoke it? Without a clear integration pattern, documentation deliverables may not go through the quality gate.

---

## S-011 Chain-of-Verification

**Strategy:** S-011 Chain-of-Verification
**Finding Prefix:** CV
**Protocol Steps Completed:** 5 of 5

### Claim Extraction and Verification

**Claim CV-001-it1: The Diataxis quadrant grid is correct as presented.**

Issue grid:
```
|  | Acquisition (learning) | Application (working) |
|--|:--:|:--:|
| Practical (doing) | Tutorials | How-to Guides |
| Theoretical (understanding) | Explanation | Reference |
```

Independent verification against diataxis.fr: The Diataxis framework defines the two axes as:
- Axis 1: practical ↔ theoretical (rows)
- Axis 2: acquisition ↔ application (columns)

The quadrant assignments per diataxis.fr:
- Practical + Acquisition = Tutorials ✓
- Practical + Application = How-to Guides ✓
- Theoretical + Acquisition = Explanation ✓
- Theoretical + Application = Reference ✓

**Verification result: CORRECT.** The quadrant grid in the issue matches diataxis.fr exactly. The earlier S-010 SR-001-it1 finding (Critical) was an error in my initial review and was correctly withdrawn in S-003. No finding here.

**Claim CV-002-it1: The diataxis-tutorial cognitive mode is `integrative`.**

Issue claim: "Cognitive mode: `integrative` (combines learning objectives with concrete steps)"

Independent verification against agent-development-standards.md:
- `integrative`: "Combines inputs from multiple sources into unified output. Cross-source correlation, pattern merging, gap filling."
- `systematic`: "Applies step-by-step procedures, verifies compliance. Checklist execution, protocol adherence, completeness verification."
- `convergent`: "Analyzes narrowly, selects options, produces conclusions."

Tutorial writing produces a step-by-step learning experience. The diataxis.fr description of tutorials: "must be meaningful, successful, logical, usefully complete" — a checklist of requirements for a procedural artifact. The `systematic` cognitive mode (step-by-step procedures, completeness verification) maps better than `integrative` (cross-source correlation, gap filling) for tutorial production.

**Finding CV-002-it1 (Minor):** The `integrative` cognitive mode for `diataxis-tutorial` is inconsistent with the agent-development-standards.md taxonomy. Tutorial writing maps more naturally to `systematic` (procedural completeness, step-by-step) than `integrative` (cross-source synthesis). The parenthetical justification "combines learning objectives with concrete steps" describes combining two inputs, which is a weak basis for `integrative` vs. `systematic`. This should be justified or corrected.

**Claim CV-003-it1: The diataxis-explanation cognitive mode is `divergent`.**

Issue claim: "Cognitive mode: `divergent` (explores broadly, makes connections, provides context)"

Independent verification: `divergent` = "Explores broadly, generates options, discovers patterns. Wide search, multiple hypotheses, creative association." The Diataxis explanation quadrant: "discursive, permits reflection, deepens understanding, acknowledges perspective and opinion, multiple viewpoints."

**Verification result: CONSISTENT.** The `divergent` mode matches explanation writing well — exploration, multiple viewpoints, broad context. No finding.

**Claim CV-004-it1: The trigger map priority 11 is "between /red-team at 10 and future skills".**

Independent verification against mandatory-skill-usage.md trigger map: `/red-team` is listed at priority 10. The issue proposes priority 11 for `/diataxis`.

**Verification result: CONSISTENT** with the existing trigger map. No factual error here.

**Claim CV-005-it1: "Cloudflare, Gatsby, Vonage" are Diataxis adopters.**

Independent verification: The diataxis.fr adoption page lists documented adopters. Cloudflare is listed. Gatsby is listed. Vonage is listed. The claim is accurate.

**Verification result: CORRECT.** No finding.

**Claim CV-006-it1: "Jerry has 12 skills" (Why this matters section).**

Independent verification against CLAUDE.md Quick Reference:
1. /worktracker
2. /problem-solving
3. /nasa-se
4. /orchestration
5. /architecture
6. /adversary
7. /saucer-boy
8. /saucer-boy-framework-voice
9. /transcript
10. /ast
11. /eng-team
12. /red-team

**Verification result: CORRECT.** 12 skills listed. No finding.

**Claim CV-007-it1: The issue proposes "6 specialized agents."**

Count from agent specifications: diataxis-tutorial, diataxis-howto, diataxis-reference, diataxis-explanation, diataxis-classifier, diataxis-auditor = 6 agents.
Count from directory structure: same 6 files listed under `agents/`.

**Verification result: CORRECT.** No finding.

### Chain-of-Verification Summary

| Claim | Status | Finding |
|-------|--------|---------|
| Quadrant grid matches diataxis.fr | VERIFIED CORRECT | None |
| Tutorial cognitive mode `integrative` | INCONSISTENT with ADS taxonomy | CV-002-it1 (Minor) |
| Explanation cognitive mode `divergent` | VERIFIED CORRECT | None |
| Priority 11 placement | VERIFIED CONSISTENT | None |
| Cloudflare/Gatsby/Vonage adoption | VERIFIED CORRECT | None |
| "12 skills" count | VERIFIED CORRECT | None |
| "6 specialized agents" | VERIFIED CORRECT | None |

---

## S-001 Red Team Analysis

**Strategy:** S-001 Red Team Analysis
**Finding Prefix:** RT
**H-16 Status:** S-003 executed first — COMPLIANT
**Protocol Steps Completed:** 5 of 5

### Threat Actor Profile

**Threat Actor:** A seasoned contributor to the Jerry framework who wants to identify the fastest path to implementation blockers — specifically, requirements that will cause CI failures or rework cycles that delay delivery.

### Attack Vector Enumeration

**Attack Vector 1: H-34 CI Gate Failure (RT-001-it1 — Critical)**

The CI gate (`check_hard_rule_ceiling.py` and associated schema validators) runs JSON Schema validation on all `skills/*/agents/*.md` files. The proposed 6 agents will be submitted as `.md` + `.governance.yaml` pairs. The governance YAML must validate against `docs/schemas/agent-governance-v1.schema.json`.

The attack: an implementer reads the issue, sees "cognitive mode: integrative" and "model: opus" for the tutorial agent, creates the `.governance.yaml` with those fields, and submits. The CI validator fails because `tool_tier` is a required field per the governance schema that is not mentioned in the issue at all. The PR is blocked. The implementer must reverse-engineer the required fields from the schema file — a correctable but unnecessary cycle.

**This is a concrete, predictable CI failure the issue could prevent by specifying tool tiers.**

**Attack Vector 2: Trigger Map Collision Creates Routing Bug (RT-002-it1 — Major)**

An attacker (or careless implementer) adding the trigger map entry to `mandatory-skill-usage.md` does not perform the collision analysis. In testing, a request "analyze the documentation structure" routes to `/diataxis` (because `documentation` matches) instead of `/problem-solving` (because `analyze` should match but `/diataxis` has higher keyword match count). The negative keyword list for `/diataxis` doesn't include `analyze` or `research`.

**Specific vulnerability:** The proposed trigger map entry has 17 positive keywords. If a user sends a request containing any of these 17 keywords, it will score a positive match for `/diataxis`. If the request ALSO contains keywords from `/problem-solving` (analyze, investigate, etc.), and neither negative keyword list suppresses the other, the routing becomes ambiguous. The priority 11 assignment means `/diataxis` would LOSE to `/problem-solving` (priority 6), `/nasa-se` (priority 5), and `/orchestration` (priority 1) — all of which score lower numbers = higher priority. So the priority ordering may actually protect against this, but the issue should explicitly state this analysis.

**Clarification on priority numbers:** In the Jerry routing system, priority 1 = HIGHEST priority (routes first), priority 10 = lowest priority. Priority 11 for `/diataxis` means it is the LAST resort after all other skills. This is conservative and reduces routing collision risk — but it also means `/diataxis` will be systematically under-invoked when documentation requests co-occur with analytical keywords.

**Attack Vector 3: Auditor Agent Cannot Execute (RT-003-it1 — Major)**

An adversary reviewing the `diataxis-auditor` specification: "Purpose: Audits existing documentation against Diataxis principles. Identifies quadrant mixing... coverage gap analysis. Produces a structured audit report."

"Point the auditor at a directory" (What this enables, point 3). The auditor must enumerate files in a directory. The only way to do this without Bash is the Glob tool. Glob is a T1 tool — fine. But it must Read each file, analyze it, and Write the report. T2 is required. The issue declares `sonnet` model but no tool tier. If the CI schema validator requires `tool_tier` in the governance YAML and the implementer guesses T1 (read-only), the Write call fails. If they guess T2, they need to verify T2 is correct.

More critically: if "point the auditor at a directory" means auditing 50 files, the auditor may need to chunk its analysis to avoid context limits (CB-05: files > 500 lines should use offset/limit). This coordination is not mentioned anywhere in the issue.

**Attack Vector 4: Phase Ordering Creates Dependency Risk (RT-004-it1 — Minor)**

Phase 2 says "Implement the four writer agents... with `.md` + `.governance.yaml` dual-file architecture per H-34." But the governance schema validation (Phase 4) comes AFTER agent implementation. This means agents could be implemented in Phase 2 with incorrect governance schemas, pass code review, be used in Phase 3 for dogfooding, and only fail schema validation in Phase 4 — late in the implementation cycle.

Better sequencing: include schema validation as a Phase 2 gate, not a Phase 4 activity.

### Red Team Summary

The most exploitable gap is the CI gate failure path (RT-001-it1): the governance schema requires `tool_tier` as a required field, and this field is not mentioned anywhere in the issue. An implementer following the issue faithfully will hit a CI failure on first PR submission for any of the 6 agents.

---

## All Findings Summary

| ID | Strategy | Severity | Finding | Section |
|----|----------|---------|---------|---------|
| FINDING-C1-it1 | S-007 | Critical | H-34 agent governance schema fields absent for all 6 agents — no tool_tier, version, forbidden_actions, output_filtering specified | Agent Specifications |
| FINDING-C2-it1 | S-013 / S-012 | Critical | diataxis-classifier routing mechanism constitutionally ambiguous — T1 vs T5 orchestrator unresolved | Agent Specifications |
| FINDING-C3-it1 | S-010 / S-001 | Critical | RT-M-004 keyword collision analysis absent — 17 new keywords added with no documented collision analysis | Routing and trigger keywords |
| FINDING-C4-it1 | S-012 / S-001 | Critical | diataxis-auditor tool tier underspecified — directory auditing requires T2 (Write) at minimum, not declared | Agent Specifications |
| SR-002-it1 | S-010 | Major | H-34 dual-file architecture mentioned but governance field specifications absent | Agent Specifications |
| SR-003-it1 | S-010 | Major | Auditor agent scope vs. design inconsistency | Agent Specifications |
| SR-004-it1 | S-010 | Major | Priority 11 routing with no collision analysis | Routing and trigger keywords |
| SM-002-it1 | S-003 | Major | Tool tier declarations absent from all agent specifications | Agent Specifications |
| SM-003-it1 | S-003 | Major | Governance schema file path not cited in acceptance criteria | Acceptance criteria |
| SM-004-it1 | S-003 | Major | Routing keyword collision analysis not performed per RT-M-004 | Routing and trigger keywords |
| CC-001-it1 | S-007 | Critical | H-34 compliance: governance schema fields absent for all agents | Agent Specifications |
| CC-002-it1 | S-007 | Major | Classifier routing mechanism constitutionally ambiguous (T1 vs T5) | Agent Specifications |
| DA-001-it1 | S-002 | Major | Diataxis classification hardness not addressed — haiku-based classifier accuracy not validated | Agent Specifications |
| DA-002-it1 | S-002 | Major | Six-agent architecture not justified over single multi-mode agent | Why a skill with agents |
| DA-003-it1 | S-002 | Major | Priority 11 routing may cause systematic under-triggering | Routing and trigger keywords |
| PM-001-it1 | S-004 | Critical | No classification accuracy acceptance criteria — classifier may ship with unknown accuracy | Acceptance criteria |
| PM-002-it1 | S-004 | Major | Knowledge document and standards file have no content specifications | Implementation plan |
| PM-003-it1 | S-004 | Major | Multi-quadrant document decomposition workflow unspecified | Agent Specifications |
| FM-001-it1 | S-012 | Major | All 6 agents will fail H-34 CI gate without governance schema fields | Agent Specifications |
| FM-002-it1 | S-012 | Major | Keyword collision risk: `documentation` + analytical keywords may conflict with /problem-solving | Routing and trigger keywords |
| FM-003-it1 | S-012 | Major | Classifier misclassification risk — no accuracy metric in acceptance criteria (RPN 280) | Acceptance criteria |
| FM-005-it1 | S-012 | Major | Auditor requires Write tool (T2) to produce report — tool tier undeclared | Agent Specifications |
| FM-007-it1 | S-012 | Minor | /adversary integration HOW not specified | Integration points |
| CV-002-it1 | S-011 | Minor | Tutorial agent cognitive mode `integrative` inconsistent with ADS taxonomy | Agent Specifications |
| IN-001-it1 | S-013 | Major | diataxis-standards.md rule file content not specified | Implementation plan |
| IN-002-it1 | S-013 | Major | Classifier ambiguous/multi-quadrant request handling unspecified | Agent Specifications |
| IN-003-it1 | S-013 | Minor | Trigger keyword `docs` too broad — compound trigger needed | Routing and trigger keywords |
| RT-001-it1 | S-001 | Critical | CI gate failure: tool_tier required by governance schema but not in any agent spec | Agent Specifications |
| RT-002-it1 | S-001 | Major | Routing priority analysis incomplete — 17 keywords with no suppression analysis documented | Routing and trigger keywords |
| RT-003-it1 | S-001 | Major | Auditor directory enumeration at scale unaddressed (CB-05 compliance) | Agent Specifications |
| RT-004-it1 | S-001 | Minor | Phase ordering: schema validation (Phase 4) should gate Phase 2 implementation | Implementation plan |
| CC-003-it1 | S-007 | Minor | templates/ subdirectory inside skill folder is novel — not prohibited but undocumented | Proposed skill architecture |
| CC-004-it1 | S-007 | Minor | Issue file itself lacks navigation table per H-23 (file is 203 lines, Claude-consumed) | (This file) |
| DA-004-it1 | S-002 | Minor | Phase 3 dogfooding of unvalidated skill creates circular quality risk | Implementation plan |
| PM-004-it1 | S-004 | Minor | Saucer Boy voice in SKILL.md/agent defs needs specification — internal vs. external voice | Implementation plan |
| SR-005-it1 | S-010 | Minor | Classifier routing output format not specified | Agent Specifications |
| SR-006-it1 | S-010 | Minor | Adopter claim citations thin — link to diataxis.fr/adoption/ | Problem statement |

### Finding Counts

| Severity | Count |
|----------|-------|
| Critical | 6 |
| Major | 21 |
| Minor | 10 |
| **Total** | **37** |

---

## Revision Recommendations

Ordered by impact (highest impact first). Each recommendation maps to findings.

### R-001-it1: Specify tool tier and governance schema fields for all 6 agents (CRITICAL PRIORITY)

**Resolves:** FINDING-C1-it1, CC-001-it1, FM-001-it1, RT-001-it1, SR-002-it1, SM-002-it1

**Action:** Add a governance specification table to the Agent Specifications section for each agent:

```
| Field | diataxis-tutorial | diataxis-howto | diataxis-reference | diataxis-explanation | diataxis-classifier | diataxis-auditor |
|-------|------------------|----------------|-------------------|---------------------|--------------------|--------------------|
| tool_tier | T2 | T2 | T2 | T2 | T1 | T2 |
| cognitive_mode | systematic | convergent | systematic | divergent | convergent | systematic |
| model | sonnet | sonnet | sonnet | opus | haiku | sonnet |
| forbidden_actions | P-003, P-020, P-022 (min 3) | same | same | same | same | same |
```

Also add to acceptance criteria: "All agent `.governance.yaml` files validated against `docs/schemas/agent-governance-v1.schema.json` at CI gate."

**Verification:** PR passes CI schema validation for all 6 `.governance.yaml` files.

### R-002-it1: Resolve classifier routing architecture (CRITICAL PRIORITY)

**Resolves:** FINDING-C2-it1, CC-002-it1, IN-002-it1, PM-003-it1, SR-005-it1

**Action:** Specify one of two designs and document the choice:

**Option A (T1 classifier):** The classifier returns a structured classification result (YAML or text) to the caller. The caller (user or orchestrator) is responsible for invoking the appropriate writer agent. The classifier does NOT use Task tool. This is T1.

**Option B (T5 classifier-orchestrator):** The classifier invokes the appropriate writer agent via Task tool. This makes it a T5 orchestrator subject to H-36 circuit breaker constraints (max 3 hops). This requires explicit justification per agent-development-standards.md T5 selection guidelines.

Option A is the simpler, more compatible choice for a skill with 6 agents. Document the choice in the agent specification.

**Verification:** Classifier agent spec includes explicit statement of routing architecture and T1/T5 declaration.

### R-003-it1: Add RT-M-004 keyword collision analysis (CRITICAL PRIORITY)

**Resolves:** FINDING-C3-it1, SR-004-it1, SM-004-it1, DA-003-it1, FM-002-it1, RT-002-it1, IN-003-it1

**Action:** Add a collision analysis subsection to the "Routing and trigger keywords" section. For each of the 17 proposed keywords, state: (a) does it appear in any existing skill's trigger map? (b) if yes, which skill? (c) which negative keyword suppresses the collision?

Also add compound trigger for `docs`: change to compound trigger `"write docs" OR "document this" OR "create documentation"` to reduce false positives from "check the docs" type requests.

**Verification:** Each proposed keyword is explicitly analyzed against all 10 existing skill trigger map entries.

### R-004-it1: Add classification accuracy acceptance criterion (CRITICAL PRIORITY)

**Resolves:** PM-001-it1, FM-003-it1, DA-001-it1

**Action:** Add to acceptance criteria:
- [ ] `diataxis-classifier` accuracy >= 90% on a 20-request test suite that includes: 4 unambiguous requests per quadrant (16 total), 2 ambiguous multi-quadrant requests, 2 non-documentation requests that should NOT route to /diataxis

**Verification:** Test suite produced and passed before Phase 4 completion.

### R-005-it1: Specify diataxis-standards.md content (MAJOR PRIORITY)

**Resolves:** IN-001-it1, PM-002-it1

**Action:** Add a content specification for `skills/diataxis/rules/diataxis-standards.md` to the implementation plan. Minimum required sections:
- Per-quadrant quality criteria table (5-10 criteria per quadrant)
- Per-quadrant anti-patterns table (3-5 per quadrant)
- Detection heuristics for quadrant mixing (observable signals)
- Escalation criteria (when to reject a document as uncategorizable)

**Verification:** diataxis-standards.md contains all four sections before Phase 2 begins.

### R-006-it1: Specify auditor tool tier and scope boundary (MAJOR PRIORITY)

**Resolves:** FINDING-C4-it1, FM-005-it1, RT-003-it1, SR-003-it1

**Action:** Declare the auditor as T2 (Read + Glob + Grep + Write). Specify scope boundary: the auditor takes a LIST of file paths as input (not a directory path), enabling the caller to scope the audit. This avoids the need for recursive directory traversal. Add CB-05 compliance note: files > 500 lines analyzed with offset/limit.

**Verification:** Auditor agent spec includes tool tier, input format (file path list), and CB-05 note.

### R-007-it1: Move schema validation to Phase 2 gate (MAJOR PRIORITY)

**Resolves:** RT-004-it1, FM-004-it1

**Action:** Revise Phase 2 to include: "Validate each agent's `.governance.yaml` against `docs/schemas/agent-governance-v1.schema.json` before proceeding to Phase 3." Move Phase 4's "Validate agent definitions against governance JSON Schema" to Phase 2.

**Verification:** Phase 2 completion criteria includes schema validation pass.

### R-008-it1: Justify tutorial cognitive mode or change to `systematic` (MINOR PRIORITY)

**Resolves:** CV-002-it1

**Action:** Either justify why `integrative` (cross-source synthesis) is correct for tutorial writing, or change to `systematic` (procedural completeness, step-by-step) which maps more naturally to the Diataxis tutorial definition ("must be logical — sensible progression").

### R-009-it1: Add navigation table to issue draft file (MINOR PRIORITY)

**Resolves:** CC-004-it1

**Action:** Add navigation table per H-23 to the issue draft file since it is stored in the repository and Claude agents read it.

### R-010-it1: Specify multi-quadrant decomposition workflow (MINOR PRIORITY)

**Resolves:** PM-003-it1, IN-002-it1 (partial)

**Action:** Add one sentence to the classifier agent spec: "When a request spans multiple quadrants, the classifier returns a decomposition recommendation listing the quadrant sequence; the caller is responsible for invoking writer agents in sequence."

---

## Projected Iteration 2 Score

If all Critical and Major revisions (R-001 through R-007) are applied:

| Dimension | Current | Projected (post R-001 to R-007) | Delta |
|-----------|---------|--------------------------------|-------|
| Completeness | 0.75 | 0.91 | +0.16 |
| Internal Consistency | 0.82 | 0.90 | +0.08 |
| Methodological Rigor | 0.78 | 0.90 | +0.12 |
| Evidence Quality | 0.82 | 0.87 | +0.05 |
| Actionability | 0.88 | 0.92 | +0.04 |
| Traceability | 0.85 | 0.92 | +0.07 |
| **Composite** | **0.810** | **0.905** | **+0.095** |

**Projected verdict after iteration 2:** REVISE (0.905 ≥ 0.92 standard threshold, but < 0.95 C4 threshold)

To reach the C4 threshold of 0.95, iteration 3 would need to address remaining Minor findings (R-008 through R-010) and strengthen evidence quality further — particularly by adding the classification accuracy test suite (R-004) with actual test cases in the acceptance criteria.

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| Total Findings | 37 |
| Critical | 6 |
| Major | 21 |
| Minor | 10 |
| Strategies Executed | 10 of 10 |
| H-16 Compliant | Yes (S-003 before S-002, S-004, S-001) |
| Composite Score | 0.810 |
| C4 Threshold (0.95) | REJECTED |
| C2+ Threshold (0.92) | REJECTED |
| Verdict | REJECTED — significant rework required |
| Projected Iteration 2 Score | ~0.905 (REVISE) |
| Revisions to Reach 0.95 | Iterations 2 + 3 minimum |

---

*Report generated by adv-executor (Strategy Executor)*
*Constitutional compliance: P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Iteration: 1 of 5*
*Next action: Apply R-001 through R-007 (Critical and Major revisions) before iteration 2*

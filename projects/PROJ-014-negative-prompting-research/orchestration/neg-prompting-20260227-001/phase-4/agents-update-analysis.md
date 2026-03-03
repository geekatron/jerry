# Jerry Agents Update Analysis: Negative Prompting Application

<!-- VERSION: 3.0.0 | DATE: 2026-02-28 | AGENT: ps-analyst | TASK: TASK-011 | REVISION: I3 — fix stale rec counts (29/27→32 in lines 101/747/879), fix EC-01 maturity rubric contradiction, fix YAML-inference percentage (55%→53%), expand REC-ENG-003 with failure-case path, enumerate eng-architect 4 items in REC-ENG-001, add direct quotes for ts-parser and wt-auditor -->
<!-- INPUT: Phase 3 taxonomy-pattern-catalog.md, barrier-1/synthesis.md, barrier-1/supplemental-vendor-evidence.md, barrier-2/synthesis.md -->
<!-- SAMPLE: 15 representative agent files across 9 skill families -->

> Analysis of how NPT-001 through NPT-014 negative prompting patterns from the Phase 3 taxonomy
> should be applied to Jerry Framework agent definition files. All findings use negative constraint
> framing per TASK-011 Orchestration Directive 1.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary (L0)](#executive-summary-l0) | Key findings, recommendation count (32), families analyzed (9) |
| [Methodology](#methodology) | Sampling, evaluation criteria, taxonomy mapping, evidence inference caveat |
| [Agent-Development-Standards Alignment](#agent-development-standards-alignment) | H-34/H-35 current enforcement and gaps |
| [Per-Family Analysis (L1)](#per-family-analysis-l1) | NPT gaps and recommendations per skill family (9 families, includes /saucer-boy) |
| [Cross-Family Patterns (L2)](#cross-family-patterns-l2) | Systemic gaps with explicit EC-to-gap mapping; framework-level standard changes |
| [Governance YAML Analysis](#governance-yaml-analysis) | How `.governance.yaml` uses negative constraints; T4-observed vs T4-inferred distinction |
| [Evidence Gap Map](#evidence-gap-map) | T1-verified vs T4-observational vs untested per recommendation |
| [PG-003 Contingency Plan](#pg-003-contingency-plan) | Reversibility under null framing effect scenario |
| [Phase 5 Downstream Inputs](#phase-5-downstream-inputs) | What Phase 5 (ADR writing) needs; D-001–D-006 decision gates; recommendation-to-ADR forward references |
| [Evidence Summary](#evidence-summary) | All cited sources with evidence tier (T4 directly-observed vs inferred distinguished) |

---

## Executive Summary (L0)

### What Was Analyzed

Fifteen Jerry Framework agent definition files were evaluated against the 14 negative prompting
taxonomy patterns (NPT-001 through NPT-014) documented in the Phase 3 pattern catalog. The
evaluation covered 9 skill families: `/adversary`, `/problem-solving`, `/nasa-se`,
`/orchestration`, `/eng-team`, `/red-team`, `/worktracker`, `/saucer-boy`, and `/transcript`.

Agent development standards H-34 and H-35 (mandatory constitutional triplet, schema validation)
establish a baseline of negative constraint enforcement already present in every agent. This
baseline is not absent — it is, however, concentrated in NPT-014 (blunt prohibition) and NPT-013
(constitutional triplet) patterns, which are the two patterns with the weakest relative
effectiveness evidence in the AGREE-5 hierarchy.

### Key Findings

**NEVER act as if the current negative constraint architecture is uniformly applied across all
agent families.** The 15 agents analyzed reveal three distinct levels of negative constraint
maturity:

- **High-maturity agents** (nse-requirements, ts-parser, wt-auditor): Use NPT-009 consequence
  documentation, domain-specific prohibitions beyond the constitutional triplet, and structured
  VIOLATION labeling. These agents MUST NOT be degraded by a normalization pass.

- **Mid-maturity agents** (ps-analyst, ps-researcher, ps-critic, orch-planner, nse-verification):
  Use the constitutional triplet (NPT-013) and partial NPT-009 (VIOLATION labels without full
  consequence documentation). The gap is consequence documentation, not structural presence.

- **Low-maturity agents** (eng-architect, eng-security, red-lead, red-recon, adv-executor,
  adv-scorer, sb-voice): Use flat markdown "What You Do NOT Do" sections (NPT-014 equivalent) or
  inline prose prohibitions without VIOLATION labels. These agents represent the largest upgrade
  opportunity.

**Total recommendations:** 32 specific recommendations across 9 families (5 framework-level,
27 agent-level). Framework-level breakdown: 3 agent-development-standards.md updates (REC-F-001
through REC-F-003) and 2 governance schema updates (REC-YAML-001 through REC-YAML-002).
Agent-level breakdown per family: /adversary (3), /problem-solving (3), /nasa-se (2),
/orchestration (3), /eng-team (4), /red-team (3), /worktracker (3), /saucer-boy (3),
/transcript (3). ALL recommendations carry the T4 observational caveat: NEVER treat these
recommendations as experimentally validated improvements — they are informed working-practice
upgrades consistent with vendor self-practice evidence (VS-001 through VS-004, 33 instances
across 10 rule files) and the AGREE-5 hierarchy (internally generated synthesis, NOT externally
validated).

### Primary Risk

**NEVER apply Phase 4 recommendations before Phase 2 experimental conditions are complete.** The
C1–C7 conditions in the Phase 2 pilot design include agents in their current state as baselines.
Upgrading forbidden_actions entries from NPT-014 to NPT-009 before Phase 2 data collection would
make the experimental conditions unreproducible per Orchestration Directive 6. The recommended
approach is to flag all changes as Phase 5+ ADR-gated, with no agent file modifications until
Phase 2 is complete.

---

## Methodology

### Sampling Strategy

The 15-agent sample was drawn to provide coverage across:

| Coverage Dimension | Agents Included | Rationale |
|-------------------|-----------------|-----------|
| Tool security tiers | T1 (adv-executor, adv-scorer, wt-auditor, sb-voice), T2 (ps-analyst, ps-critic, nse-requirements, nse-verification), T3 (ps-researcher, orch-planner, eng-architect, eng-security, red-lead, red-recon), haiku (ts-parser) | Full tier coverage; different tiers have different risk profiles for negative constraint omission |
| Cognitive modes | convergent (ps-analyst, ps-critic, adv-scorer), divergent (ps-researcher, sb-voice), systematic (wt-auditor, nse-verification, ts-parser), forensic (red-recon), integrative (orch-planner) | Cognitive mode affects how agents interpret prohibition scope |
| Skill families | 9 of 10 registered skills (all except `/saucer-boy-framework-voice`) | Maximum family coverage within the 15-agent constraint |
| Structural patterns | XML-tagged sections (problem-solving, nasa-se, adversary), flat markdown (eng-team, red-team), mixed (worktracker, transcript) | Structural pattern determines where NPT patterns can be applied |

**NEVER treat this as a complete audit.** The 15-agent sample does not cover all 30+ agents in
the registry. Phase 5 ADR MUST specify whether recommendations apply universally or only to the
analyzed sample before any agent files are modified.

**Evidence inference caveat (I2 addition, count corrected I3):** Of the 32 recommendations, approximately 17 specify
`.governance.yaml` as the target location. Governance YAML files were NOT directly read during
this analysis (see Governance YAML Analysis section). This means approximately 53% of
recommendations are based on `.md` body content plus schema validation requirements (H-34/H-35)
rather than direct YAML file reads. The remaining 47% target `.md` body sections that were
directly observed. NEVER treat all recommendations as equally evidence-grounded — YAML-targeted
recommendations carry a `T4 (inferred, YAML not read)` evidence qualifier distinct from
`T4 (directly observed, .md body)`.

**Maturity classification rubric:** The high/mid/low maturity classification was derived from
these per-agent EC criteria assessments:
- **High-maturity:** EC-01 PASS (schema-enforced) + EC-02 PASS + EC-03 partial + EC-04 PASS
- **Mid-maturity:** EC-01 PASS (schema-enforced) + EC-02 partial + EC-03 FAIL + EC-04 partial
- **Low-maturity:** EC-01 PASS (schema-enforced) + EC-02 FAIL + EC-03 FAIL + EC-04 FAIL

Per-agent assessment was binary at the criteria level (PASS = pattern present in agent file;
FAIL = pattern absent). Maturity level assigned to the overall agent based on the combination
above. NEVER treat "low-maturity" as indicating constitutional triplet absence — all agents
pass EC-01 at minimum due to H-35 schema enforcement. EC-01 is therefore PASS (schema-enforced)
at all maturity levels; maturity differentiation operates exclusively on EC-02 through EC-04.
EC-03 "partial" for high-maturity means: VIOLATION label present in the agent file, but
consequence documentation absent. EC-03 FAIL means: no VIOLATION label and no consequence.

### Evaluation Criteria

Each agent was evaluated against six criteria derived from the NPT pattern catalog:

| Criterion ID | Criterion | Relevant NPT Patterns |
|---|---|---|
| EC-01 | Constitutional triplet presence (P-003, P-020, P-022) | NPT-013 |
| EC-02 | VIOLATION label usage in forbidden actions | NPT-009 partial |
| EC-03 | Consequence documentation in forbidden actions | NPT-009 full |
| EC-04 | Domain-specific prohibitions beyond constitutional triplet | NPT-009, NPT-010, NPT-011 |
| EC-05 | Paired prohibition with positive alternative | NPT-010 |
| EC-06 | L2 re-injection of critical prohibitions | NPT-012 |

**NEVER apply EC criteria as a binary pass/fail without acknowledging that NPT-010 (paired
prohibition) and NPT-011 (justified prohibition) carry T4 observational evidence only with no
controlled comparison against unpaired alternatives (UNTESTED dimension, taxonomy-pattern-catalog.md
Evidence Gap Map section).**

### Taxonomy Mapping Approach

Each recommendation is tagged with:
- The NPT pattern it implements
- The evidence tier for that pattern (T1/T4/Untested)
- The agent location in the dual-file architecture (`.md` frontmatter / `.md` body / `.governance.yaml`)
- Whether the change is reversible under PG-003 null framing effect scenario

---

## Agent-Development-Standards Alignment

### What H-34 and H-35 Already Enforce

H-34 and H-35 in `agent-development-standards.md` establish mandatory negative constraint
infrastructure that MUST NOT be credited as NPT-009 compliance when it is not:

| H-34/H-35 Requirement | NPT Pattern | Current Status |
|---|---|---|
| `capabilities.forbidden_actions` min 3 entries in `.governance.yaml` | NPT-013 enforcement mechanism | Present in all agents per schema validation (T4 verified) |
| P-003, P-020, P-022 must be referenced | NPT-013 | Present in all agents (schema-mandatory) |
| `constitution.principles_applied` min 3 entries | NPT-013 | Present in all agents |
| Guardrails template: `"Spawn recursive subagents (P-003)"` | NPT-014 (blunt) | Present in all agents — this IS NPT-014, NOT NPT-009 |
| Constitutional triplet in markdown body `<guardrails>` section | NPT-013 | Present in XML-tagged agents; ABSENT in flat-markdown agents (eng-team, red-team) |

**Critical finding:** The guardrails template in `agent-development-standards.md` provides a
MINIMUM example of `"Spawn recursive subagents (P-003)"` as the forbidden_actions entry. This
example text is NPT-014 (blunt prohibition without consequence documentation). NEVER treat
compliance with H-35's minimum as compliance with NPT-009. The minimum set notice in the
guardrails template explicitly acknowledges agents SHOULD add domain-specific entries beyond
minimums — this is the gap Phase 4 recommendations address.

### Gaps in H-34/H-35 That Permit NPT-014 Proliferation

The following gaps in current standards permit NPT-014 to be the default when agents meet only
the minimum requirements:

| Gap ID | Description | Phase 4 Recommendation Reference |
|--------|-------------|----------------------------------|
| GAP-001 | No schema requirement for consequence documentation in forbidden_actions entries | REC-F-001 |
| GAP-002 | No standard for VIOLATION label format in forbidden_actions entries | REC-F-002 |
| GAP-003 | No requirement for domain-specific entries beyond constitutional triplet | REC-F-003 |
| GAP-004 | Guardrails template minimum example uses NPT-014 framing — agents satisfying minimum are NPT-014 compliant, not NPT-009 compliant | REC-F-001 |
| GAP-005 | No guidance on L2-REINJECT applicability to agent-file prohibitions (vs. rule-file prohibitions) | Noted; not a current agent standard gap |

**NEVER recommend closing GAP-005 in Phase 4.** L2-REINJECT is a rule-file mechanism that
operates at the `.context/rules/` layer. Agent `.md` files are loaded at agent invocation (Tier 2
progressive disclosure), not via the per-prompt L2 mechanism. Applying L2-REINJECT to agent files
would require architectural changes outside the scope of agent definition updates.

---

## Per-Family Analysis (L1)

> Format per family: Current patterns → Applicable NPTs → Gaps → Specific recommendations.
> All recommendations are T4-observational unless marked T1-verified.

### Family 1: `/adversary` (adv-executor, adv-scorer)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| adv-executor | Present | "MUST NOT use Task tool" (inline) | Absent | Absent | Absent | P-003 runtime self-check section |
| adv-scorer | Present | "MUST NOT produce numeric scores without rubric" (inline) | Absent | Absent | Absent | Anti-leniency bias counteraction |

**NEVER credit the anti-leniency bias counteraction in adv-scorer as NPT-010.** That section uses
positive framing ("MUST actively counteract leniency bias") which is the positive alternative
alone — without the paired prohibition that NPT-010 requires. A paired prohibition would read:
"NEVER accept a score without explicitly checking for leniency bias. Alternative: state the
leniency check result before finalizing any score."

**Direct file evidence (adv-executor, `skills/adversary/agents/adv-executor.md`, P-003 self-check
section):**
> "1. **No Task tool invocations** — This agent MUST NOT use the Task tool to spawn subagents"
> "If any step in this agent's process would require spawning another agent, HALT and return an error: 'P-003 VIOLATION: adv-executor attempted to spawn a subagent. This agent is a worker and MUST NOT invoke other agents.'"

The P-003 VIOLATION label is present with consequence language ("HALT and return an error")
but the consequence is procedural (halt/return), not operational-impact (what is lost). The
absence of the downstream impact statement — that spawned-subagent output is unattributable to
the declared review scope — is the NPT-009 gap.

#### Gaps

- adv-executor: The "This agent MUST NOT use the Task tool" prohibition (directly observed in
  P-003 Self-Check section) lacks operational consequence documentation. Consequence: "Spawning
  a subagent from adv-executor violates H-01/P-003 and invalidates the quality review — the
  spawned agent's output is not attributable to the declared review scope."
- adv-scorer: No domain-specific VIOLATION label for the score-without-rubric prohibition.
- Both agents: No justified prohibition (NPT-011) explaining WHY the constitutional constraints
  exist in the adversarial quality context specifically.

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-ADV-001 | adv-executor | Upgrade Task tool prohibition to NPT-009: Add "Consequence: invocation of a subagent from this agent invalidates review attribution and violates H-01" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — consequence text is additive |
| REC-ADV-002 | adv-scorer | Add domain-specific SCORE FABRICATION VIOLATION: "NEVER produce a numeric dimension score without executing the rubric criterion for that dimension — Consequence: fabricated scores produce false quality gate passage" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — new entry, additive |
| REC-ADV-003 | adv-scorer | Add paired prohibition (NPT-010) to leniency bias section: "NEVER present a score as unbiased without stating the leniency check result. When leniency bias check reveals inflation, state: 'Leniency bias detected — score reduced from X to Y'" | NPT-010 | `.md` body `<guardrails>` | T4/Untested | Yes — additive |

### Family 2: `/problem-solving` (ps-analyst, ps-researcher, ps-critic)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| ps-analyst | Present | "DO NOT spawn subagents that spawn further subagents" | Partial — VIOLATION labels present, no consequence | Absent | Absent | P-002 file output violation |
| ps-researcher | Present | "P-003 VIOLATION: DO NOT spawn..." | Partial — VIOLATION label, no consequence | Absent | Absent | Absent beyond triplet |
| ps-critic | Present | "LOOP VIOLATION: DO NOT self-invoke" | Partial — LOOP VIOLATION label | Absent | Absent | Loop prevention domain-specific |

**NEVER treat ps-analyst's self-critique checklist as NPT-011 compliance.** The checklist items
("Are all conclusions evidence-based?") are positive verification items, not justified prohibitions.
NPT-011 would require: "NEVER present a conclusion without evidence citation — Reason: conclusions
without evidence are epistemically equivalent to fabrication (P-022) regardless of whether they
are labeled 'uncertain'."

**Direct file evidence (ps-critic, `skills/problem-solving/agents/ps-critic.md`, Forbidden Actions
block, directly observed):**
> "- **P-003 VIOLATION:** DO NOT spawn subagents or manage iteration loops"
> "- **P-022 VIOLATION:** DO NOT hide quality issues or inflate scores"
> "- **LOOP VIOLATION:** DO NOT self-invoke or trigger next iteration (orchestrator's job)"

The LOOP VIOLATION label is a strong domain-specific prohibition identifying both the forbidden
action (self-invoke) and the responsibility boundary (orchestrator's job). The NPT-009 gap is
consequence documentation: what is compromised when ps-critic self-invokes? The H-14 creator-critic
independence boundary collapses, producing a reflexivity problem — the critic has access to its
own prior reasoning artifacts and confirmation bias is structurally unavoidable.

**Direct file evidence (nse-requirements, `skills/nasa-se/agents/nse-requirements.md`, Forbidden
Actions block, directly observed):**
> "- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs"
> "- **P-040 VIOLATION:** DO NOT create orphan requirements without traces"

nse-requirements uses both P-violation labels (NPT-013/NPT-009 hybrid) and domain-specific
violation types (P-043, P-040) beyond the constitutional triplet. The mandatory DISCLAIMER
output section in the same file (`skills/nasa-se/agents/nse-requirements.md`, lines 157–167)
provides required positive alternative text — making this the closest approximation to full
NPT-010 in the sample, even though not labeled as such.

#### Gaps

- ps-researcher: The forbidden actions block uses "P-003 VIOLATION: DO NOT spawn subagents that
  spawn further subagents" — VIOLATION label is present (partial NPT-009) but consequence
  documentation is missing. What happens when a researcher spawns a sub-researcher? The analysis
  quality is not invalidated in the same way as in adv-executor — the consequence is P-003
  governance violation, not output invalidation.
- ps-analyst (this agent): The "Forbidden Actions (Constitutional)" block correctly uses
  VIOLATION labels. The gap is that consequences are encoded as violation-type names only, not
  as operational impact statements that downstream agents can act on.
- ps-critic: The LOOP VIOLATION prohibition (directly observed) is a strong domain-specific entry.
  The gap is that no NPT-011 justification explains WHY self-invocation constitutes a loop — a
  critic evaluating its own output creates a reflexivity problem that compromises the independence
  assumption of the H-14 creator-critic separation.

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-PS-001 | ps-researcher | Add consequence to P-003 VIOLATION entry: "Consequence: recursive delegation makes output provenance untraceable and violates H-01 governance audit trail" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |
| REC-PS-002 | ps-critic | Add NPT-011 justified prohibition for LOOP VIOLATION: "NEVER evaluate output generated by this agent in the same turn — Reason: critic independence (H-14) requires that the critic has no access to the creator's reasoning artifacts; self-evaluation collapses the independence boundary" | NPT-011 | `.md` body `<guardrails>` | T4/Untested | Yes — additive |
| REC-PS-003 | ps-analyst | Add consequence documentation to all three constitutional entries in forbidden_actions | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |

### Family 3: `/nasa-se` (nse-requirements, nse-verification)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| nse-requirements | Present | Several entries | Strong — P-043 VIOLATION with mandatory DISCLAIMER text | Partial | Absent | P-040/P-041/P-043 domain principles |
| nse-verification | Present | Several entries | Partial — "P-022 VIOLATION: DO NOT claim verification passed without evidence" lacks consequence | Absent | Absent | FIX-NEG-005 enhanced validation |

**nse-requirements is the highest-maturity negative constraint agent in the sample.** The
mandatory DISCLAIMER section with required output text is a structural enforcement mechanism that
goes beyond NPT-009 — it provides the positive alternative (required text) alongside the
prohibition (DO NOT omit). This is NPT-010 in operational form, even though it was not labeled
as such in the original agent design.

**NEVER degrade nse-requirements as part of a "normalization" pass** that reduces all agents
to a common format. The P-043 VIOLATION structure with mandatory DISCLAIMER output text represents
the target state for domain-specific agent prohibitions.

#### Gaps

- nse-verification: "P-022 VIOLATION: DO NOT claim verification passed without evidence" — the
  VIOLATION label is present but consequence documentation is absent. What happens when
  verification is claimed without evidence? The verification artifact is invalid; downstream
  agents that rely on it produce unfounded approvals. This consequence needs explicit documentation.
- nse-requirements: The paired prohibition pattern is present operationally but not labeled as
  such. Labeling it explicitly (as NPT-010) would aid auditing but is cosmetic rather than
  substantive.

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-NSE-001 | nse-verification | Add consequence to P-022 VIOLATION: "Consequence: an uncorroborated verification claim creates a false quality gate passage — downstream phases may proceed on invalid evidence, compounding error" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |
| REC-NSE-002 | nse-verification | Add NPT-010 paired prohibition for the primary verification claim prohibition: "NEVER mark a criterion PASS without citing the specific evidence. When evidence is incomplete, mark PARTIAL with gap description: 'Criterion C-N: PARTIAL — missing evidence: [X]'" | NPT-010 | `.md` body `<guardrails>` | T4/Untested | Yes — additive |

### Family 4: `/orchestration` (orch-planner)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| orch-planner | Present | Several entries | Partial — VIOLATION labels for P-022 and HARDCODING | Absent | Absent | HARDCODING VIOLATION domain-specific |

**NEVER treat orch-planner's HARDCODING VIOLATION as NPT-009-complete.** "HARDCODING VIOLATION:
DO NOT use hardcoded pipeline names" identifies the violation but documents no consequence. In
an orchestration agent, using hardcoded pipeline names creates brittle plans that break when
project naming conventions change — the consequence is orchestration failure downstream.

#### Gaps

- Missing consequence documentation on both domain-specific VIOLATION entries.
- No NPT-010 paired prohibition providing the alternative pattern for workflow naming ("NEVER
  hardcode pipeline names. Use: `{project-id}-{workflow-slug}-{YYYYMMDD}-{NNN}` format from
  the orchestration planning standard").
- orch-planner coordinates other agents; its prohibitions have higher downstream impact than
  single-agent prohibitions. The absence of NPT-011 justification for P-022 is notable: the
  reason WHY orchestrators must not misrepresent complexity is that downstream agents receive
  handoffs sized to the declared complexity level — misrepresentation cascades.

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-ORCH-001 | orch-planner | Add consequence to HARDCODING VIOLATION: "Consequence: hardcoded pipeline names break plan reproducibility across projects and sessions, creating orphaned orchestration state" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |
| REC-ORCH-002 | orch-planner | Add NPT-010 paired prohibition: "NEVER hardcode pipeline names. Use the standard format: `{project-id}-{workflow-slug}-{YYYYMMDD}-{NNN}`" | NPT-010 | `.md` body methodology | T4/Untested | Yes — additive |
| REC-ORCH-003 | orch-planner | Add NPT-011 justified prohibition for P-022 complexity representation: "NEVER misrepresent workflow complexity — Reason: downstream agents receive handoffs sized to declared complexity; underrepresentation produces under-resourced agents; overrepresentation wastes token budget at every downstream hop" | NPT-011 | `.md` body `<guardrails>` | T4/Untested | Yes — additive |

### Family 5: `/eng-team` (eng-architect, eng-security)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| eng-architect | Partial — inline prose, no table, no VIOLATION labels | "What You Do NOT Do" section (4 items, positive list framing) | Absent | Absent | Absent beyond constitutional |
| eng-security | Same flat structure | "What You Do NOT Do" section (4 items) | Absent | Absent | Absent | Absent beyond constitutional |

**The eng-team agents represent the most significant structural gap in the sample.** Both agents
use flat markdown structure without XML tags (`<guardrails>`, `<capabilities>`) and lack VIOLATION
labels entirely. The constitutional compliance section lists principles as a flat prose list
without the table format used in XML-tagged agents.

**NEVER conflate the structural gap with a safety gap.** The constitutional triplet is present in
both agents — P-003, P-020, and P-022 are listed in the constitutional compliance section. The
gap is structural and formatting-level, not a missing constraint. The risk is that flat-structure
prohibitions are more susceptible to T-004 failure mode (context compaction dropping NEVER rules)
than VIOLATION-labeled entries in structured YAML.

#### Gaps

- Neither agent uses VIOLATION labels — the T-004 failure mode risk is highest for these agents.
- "What You Do NOT Do" section uses positive list items: "That is eng-devsecops" — this is
  delegation description, not prohibition. It does not register as a NEVER constraint.
- No domain-specific prohibitions beyond scope delegation descriptions.
- No `.governance.yaml` companion file content visible — these agents may not have governance
  files or may have them without structured forbidden_actions (unable to confirm from `.md` alone).

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-ENG-001 | eng-architect, eng-security | Convert "What You Do NOT Do" section to NPT-009 structured format with VIOLATION labels and consequence documentation for each item. For eng-architect specifically, the 5 items in the "What You Do NOT Do" section (directly observed, `skills/eng-team/agents/eng-architect.md`) map to the following draft VIOLATION labels: (1) "SCOPE VIOLATION: NEVER implement code or write production application logic — Consequence: code produced by eng-architect bypasses the eng-lead review and eng-backend implementation steps in the 8-step workflow, producing unreviewed artifacts"; (2) "SCOPE VIOLATION: NEVER execute tests or run test suites — Consequence: test execution is eng-qa's role; eng-architect running tests introduces false ownership of QA outcomes"; (3) "SCOPE VIOLATION: NEVER manage CI/CD pipelines or operational security tooling — Consequence: CI/CD management by the design agent conflates architecture concerns with operational concerns, violating the SSDF PO.2 roles-and-responsibilities boundary"; (4) "SCOPE VIOLATION: NEVER deploy infrastructure or manage cloud resources — Consequence: deployment is eng-infra's role; architecture-layer deployment breaks the design-deploy separation that enables rollback and auditability"; (5) "SCOPE VIOLATION: NEVER perform manual code review — that is eng-security's role — Consequence: duplicate review by eng-architect displaces the security-specialist review without providing equivalent security depth". | NPT-009 | `.md` body (wherever `<guardrails>` section should be) | T4 (directly observed, .md body) | Yes — reformatting with additive consequence text |
| REC-ENG-002 | eng-architect, eng-security | Add formal `<guardrails>` XML section with constitutional triplet in VIOLATION label format | NPT-013 + NPT-009 | `.md` body | T4 | Yes — additive structural section |
| REC-ENG-003 | eng-architect, eng-security | Verify `.governance.yaml` companion files exist and contain `forbidden_actions` entries meeting H-35 minimum (at least 3 entries referencing P-003, P-020, P-022). Failure-case path: if `.governance.yaml` is absent, create it using the guardrails template in `agent-development-standards.md` (Guardrails Template section). If `forbidden_actions` entries are below H-35 minimum (fewer than 3 entries referencing the constitutional triplet), add the constitutional triplet entries exactly as shown in the guardrails template: `"Spawn recursive subagents (P-003)"`, `"Override user decisions (P-020)"`, `"Misrepresent capabilities or confidence (P-022)"`. Apply REC-ENG-001 VIOLATION label upgrade simultaneously with any governance file creation to avoid two-pass modification. | NPT-013 | `.governance.yaml` | T4 (schema-mandatory) | N/A — compliance verification; file creation under failure path is additive |
| REC-ENG-004 | eng-security | Add domain-specific SCOPE VIOLATION: "NEVER perform security analysis outside the declared engagement scope — Consequence: out-of-scope findings are not covered by engagement authorization and may constitute unauthorized access" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |

### Family 6: `/red-team` (red-lead, red-recon)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| red-lead | Partial — prose, no VIOLATION labels | "What You Do NOT Do" (5 items) | Absent | Absent | Absent | Scope document YAML with boolean false constraints |
| red-recon | Partial — same flat structure | "What You Do NOT Do" (5 items) | Absent | Absent | Absent | SCOPE_REVIEW_REQUIRED circuit breaker |

**The red-team agents have a notable negative constraint mechanism not present in other families:
scope document YAML boolean constraints** (social_engineering_authorized: false,
persistence_authorized: false). These are NPT-009-equivalent in data schema form — they enforce
prohibition via schema value rather than text instruction. **NEVER downgrade this to NPT-014
status** — a schema value of `false` is a machine-enforceable constraint that text prohibitions
cannot replicate.

**red-recon's SCOPE_REVIEW_REQUIRED circuit breaker flag is the strongest enforcement mechanism
in the sample.** It converts a negative constraint into a pre-tool gate — the agent cannot
proceed without scope validation regardless of instruction text. This is architecturally equivalent
to an L3 enforcement layer applied at agent level.

#### Gaps

- Both agents use flat markdown structure — same structural gap as eng-team agents.
- The "What You Do NOT Do" items lack VIOLATION labels and consequence documentation.
- red-lead's authorization constraints section describes scope limitations but does not use
  VIOLATION framing for out-of-scope actions.
- The connection between the scope document boolean constraints and the prose "What You Do NOT Do"
  section is implicit — an agent that reads only the prose section might not connect it to the
  schema enforcement.

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-RED-001 | red-lead, red-recon | Convert "What You Do NOT Do" items to NPT-009 structured entries with VIOLATION labels: "SCOPE VIOLATION: NEVER act on targets outside the authorized allowlist — Consequence: out-of-scope action terminates the engagement and triggers incident escalation" | NPT-009 | `.md` body `<guardrails>` | T4 | Yes — reformatting with additive consequence text |
| REC-RED-002 | red-recon | Add NPT-011 justified prohibition for SCOPE_REVIEW_REQUIRED: "NEVER execute an action before Scope Oracle validation — Reason: the scope document is the legal authorization boundary; acting without validation removes the authorization defense" | NPT-011 | `.md` body methodology | T4/Untested | Yes — additive |
| REC-RED-003 | red-lead | Explicitly cross-reference scope document boolean constraints in prose prohibitions: "The scope document `authorized: false` values ARE the operative prohibitions for this engagement — NEVER treat prose instructions as overriding schema-enforced authorization constraints" | NPT-009 | `.md` body `<guardrails>` | T4 | Yes — additive clarification |

### Family 7: `/worktracker` (wt-auditor)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| wt-auditor | Present | Several entries | Partial — P-010 VIOLATION with domain label | Absent | Absent | H-33 enforcement: DO NOT use manual Read+Grep |

**wt-auditor has a strong domain-specific prohibition** that partially meets NPT-009: "H-33 DO
NOT use manual Read+Grep template comparison for frontmatter extraction." The violation type
(H-33) and scope (frontmatter extraction specifically) are present. The consequence is absent:
what happens when manual Read+Grep is used instead of AST? AST-based extraction catches structural
variations that regex-based comparison misses — manual comparison produces false-negative audit
results that allow malformed entities to pass.

**Direct file evidence (wt-auditor, `skills/worktracker/agents/wt-auditor.md`, Forbidden Actions
block and H-33 Enforcement note, directly observed):**
> "**Forbidden Actions (Constitutional):**"
> "- **P-003 VIOLATION:** DO NOT spawn subagents"
> "- **P-020 VIOLATION:** DO NOT auto-fix issues without user approval"
> "- **P-002 VIOLATION:** DO NOT return audit results without file output"
> "- **P-010 VIOLATION:** DO NOT ignore worktracker integrity violations"

And from the H-33 enforcement note in the Capabilities section:
> "**Enforcement (H-33):** For the `template_compliance` audit check type,"
> "MUST use `jerry ast validate path --schema entity_type` via `uv run --directory ${CLAUDE_PLUGIN_ROOT}`."
> "DO NOT use manual Read+Grep template comparison for frontmatter extraction."

The H-33 prohibition is expressed in the Capabilities section as a positive behavioral requirement
with a MUST/DO NOT pair — it is not in the Forbidden Actions block. This placement means the
H-33 constraint does not carry a VIOLATION label. The Forbidden Actions block uses P-NNN VIOLATION
format for constitutional entries only; the domain-specific H-33 constraint is structurally
separated from the VIOLATION-labeled entries, creating an auditing gap: a grep for "VIOLATION:"
in the wt-auditor file will find P-003, P-020, P-002, P-010 entries but miss the H-33 prohibition
entirely.

#### Gaps

- P-010 VIOLATION: "DO NOT ignore worktracker integrity violations" — scope is clear, consequence
  absent. What consequence follows from ignoring integrity violations? The worktracker becomes an
  unreliable source of truth for orchestration agents that query it.
- H-33 prohibition: consequence absent (see above).
- No NPT-010 paired prohibition providing the alternative: "NEVER use Read+Grep for frontmatter.
  Use: `uv run jerry ast frontmatter {file}` for all frontmatter extraction operations."

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-WT-001 | wt-auditor | Add consequence to H-33 VIOLATION: "Consequence: manual Read+Grep produces false-negative audit results — malformed entities pass validation, corrupting worktracker integrity state" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |
| REC-WT-002 | wt-auditor | Add NPT-010 paired prohibition: "NEVER use Read+Grep for frontmatter extraction. Use: `uv run jerry ast frontmatter {file}` — the AST parser handles structural variations that regex cannot" | NPT-010 | `.md` body methodology | T4/Untested | Yes — additive |
| REC-WT-003 | wt-auditor | Add consequence to P-010 VIOLATION: "Consequence: unacknowledged integrity violations permit downstream agents to act on invalid worktracker state — orchestration plans based on corrupted state produce ghost deliverables" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |

### Family 8: `/saucer-boy` (sb-voice)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| sb-voice | Partial — inline prose in `<constraints>` section, no VIOLATION labels | Seven NEVER entries (inline prose list) | Absent | Absent | Absent | Boundary condition enforcement (no-personality contexts) |

**Direct file evidence (sb-voice, `skills/saucer-boy/agents/sb-voice.md`, Constraints section,
directly observed):**
> "1. NEVER deploy personality in no-personality contexts (constitutional failure, governance, security)."
> "2. NEVER override user request for formal tone (P-020)."
> "3. NEVER sacrifice technical accuracy for personality. Information is always correct."
> "4. NEVER produce framework output (quality gate messages, error messages, hook text). That is `/saucer-boy-framework-voice`."
> "5. NEVER force humor. If the metaphor doesn't come naturally, use direct language."
> "6. NEVER use sycophantic praise. Match enthusiasm to achievement."

The NEVER vocabulary is consistently applied across all six constraints — sb-voice uses more
NEVER entries than most agents in the sample. The structural gap is that these NEVER entries are
a flat numbered list in a `<constraints>` section, without VIOLATION labels, consequence
documentation, or domain-specific violation types. This is NPT-014 (blunt prohibition) applied
consistently, not NPT-009 structure.

**P-003 Self-Check section (directly observed):**
> "4. **Single-level execution** — This agent operates as a worker invoked by the main context"
> "If any step would require spawning another agent, HALT and return: 'P-003 VIOLATION: sb-voice
>  attempted to spawn a subagent. This agent is a worker and MUST NOT invoke other agents.'"

The P-003 VIOLATION label with halt instruction appears in the P-003 Self-Check section — this
is partial NPT-009 (VIOLATION label + procedural consequence), but only for the P-003 constraint.
The six domain-specific constraints in the `<constraints>` section use NPT-014 only.

**NEVER conflate sb-voice's NEVER-vocabulary density with NPT-009 compliance.** The agent has
the highest density of NEVER entries in the sample (six NEVER entries plus the P-003 Self-Check
halt instruction). The absence of VIOLATION labels and consequence documentation throughout the
`<constraints>` section means all six entries are NPT-014 equivalent despite the correct NEVER
framing.

**sb-voice is a distinct pattern class from eng-team/red-team flat-markdown agents.** The
eng-team agents use "What You Do NOT Do" positive list framing. sb-voice uses NEVER framing
in a flat numbered list. This is structurally different — sb-voice's constraints already use
NEVER vocabulary and would require only VIOLATION label addition and consequence documentation,
not a vocabulary conversion step. The upgrade path is narrower than for eng-team/red-team.

#### Gaps

- All six domain-specific constraints use NPT-014 (NEVER + action) without VIOLATION labels.
  The boundary condition prohibition ("NEVER deploy personality in no-personality contexts") is
  particularly high-value for NPT-009 upgrade — the consequence (personality in a security or
  constitutional failure context degrades governance signal precision) is non-obvious.
- No NPT-010 paired prohibition providing the positive alternative format: "NEVER deploy
  personality in hard-stop contexts. When a hard-stop context is detected, use: direct precision
  mode — factual, unadorned, no personality elements."
- No NPT-011 justification for WHY personality must be suppressed in constitutional failure
  contexts. The reason (governance signal precision degrades when personality competes with
  formal constraint language) is not documented in the agent file.
- The scope delegation prohibition ("NEVER produce framework output... That is
  `/saucer-boy-framework-voice`") is the closest to NPT-009 format but still lacks a consequence
  entry: the consequence of scope confusion between sb-voice and sb-framework-voice is that
  framework output (error messages, hook text) loses voice consistency and reviewability.

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-SB-001 | sb-voice | Add VIOLATION label and consequence to the no-personality boundary constraint: "HARD-STOP VIOLATION: NEVER deploy personality elements in no-personality contexts (constitutional failure, governance, security) — Consequence: personality competes with governance signal precision and reduces the salience of critical constraint language" | NPT-009 | `.md` body `<constraints>` | T4 (directly observed, .md body) | Yes — additive VIOLATION label and consequence text |
| REC-SB-002 | sb-voice | Add NPT-010 paired prohibition for the hard-stop constraint: "NEVER deploy personality in hard-stop contexts. When hard-stop is detected: switch to direct precision mode — no metaphors, no McConkey energy, no humor. Template: '[Issue statement]. [Required action]. [Resolution path].'" | NPT-010 | `.md` body `<constraints>` | T4/Untested | Yes — additive alternative format |
| REC-SB-003 | sb-voice | Add VIOLATION label to scope delegation constraint: "SCOPE VIOLATION: NEVER produce framework output (quality gate messages, error messages, hook text) — Consequence: scope confusion between sb-voice and sb-framework-voice produces inconsistent voice quality in automated framework output that bypasses the sb-framework-voice review gate" | NPT-009 | `.md` body `<constraints>` | T4 (directly observed, .md body) | Yes — additive VIOLATION label and consequence text |

### Family 9: `/transcript` (ts-parser)

#### Current Negative Constraint Patterns

| Agent | NPT-013 | NPT-014 | NPT-009 | NPT-010 | NPT-011 | Domain-Specific |
|-------|---------|---------|---------|---------|---------|-----------------|
| ts-parser | Present | Five entries with VIOLATION labels | Strong partial — CONTENT VIOLATION, TIMESTAMP VIOLATION with scope | Absent | Absent | CONTENT VIOLATION (strongest domain-specific in sample) |

**ts-parser has the most developed domain-specific prohibition set in the sample.** Five entries:
"P-003 VIOLATION / P-002 VIOLATION / P-022 VIOLATION / CONTENT VIOLATION / TIMESTAMP VIOLATION."
The CONTENT VIOLATION ("DO NOT modify or 'correct' transcript text content") and TIMESTAMP
VIOLATION ("DO NOT fabricate timestamps") identify violation scope precisely. The gap is
consequence documentation — both are partial NPT-009 entries.

**Direct file evidence (ts-parser, `skills/transcript/agents/ts-parser.md`, Forbidden Actions
block, directly observed):**
> "- **P-003 VIOLATION:** DO NOT spawn subagents"
> "- **P-002 VIOLATION:** DO NOT return parsed data without file output"
> "- **P-022 VIOLATION:** DO NOT claim parsing success when errors occurred"
> "- **CONTENT VIOLATION:** DO NOT modify or 'correct' transcript text content"
> "- **TIMESTAMP VIOLATION:** DO NOT fabricate timestamps for plain text files"

All five entries use the VIOLATION label format (NPT-009 structural component present). The
NPT-009 gap is exclusively consequence documentation — none of the five entries include an
operational impact statement following the label. The CONTENT VIOLATION and TIMESTAMP VIOLATION
entries are the highest-value upgrade targets because their consequences are domain-specific
and non-obvious: transcript content modification compromises evidentiary integrity in a way
that does not apply to other agent file operations.

**NEVER use ts-parser's five-entry forbidden_actions as a template without acknowledging that
consequence documentation is absent from all five.** The VIOLATION labels are present; what
is absent is the operational impact description that helps downstream consumers understand
the severity.

#### Gaps

- CONTENT VIOLATION: consequence absent. What happens when transcript text is modified?
  The transcript's evidentiary integrity is compromised — any citation from the corrected
  transcript is unreliable. This consequence distinguishes CONTENT VIOLATION from simple
  formatting errors.
- TIMESTAMP VIOLATION: consequence absent. Fabricated timestamps break temporal analysis
  of speaker patterns and meeting structure.
- No NPT-011 justification for why transcript content must not be corrected — agents that
  process transcripts for correctness in other contexts (like editing) might not understand
  why the same behavior is prohibited here.

#### Recommendations

| Rec ID | Agent | Change | NPT | Location | Evidence Tier | PG-003 Reversible |
|--------|-------|--------|-----|----------|--------------|-------------------|
| REC-TS-001 | ts-parser | Add consequence to CONTENT VIOLATION: "Consequence: modified transcript text invalidates downstream citation accuracy — any claim sourced to this transcript becomes unverifiable" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |
| REC-TS-002 | ts-parser | Add NPT-011 justified prohibition for CONTENT VIOLATION: "NEVER modify transcript text even when it appears incorrect — Reason: the transcript is an evidentiary record of what was said, not what was meant; corrections belong in analyst notes, not in the transcript itself" | NPT-011 | `.md` body `<guardrails>` | T4/Untested | Yes — additive |
| REC-TS-003 | ts-parser | Add consequence to TIMESTAMP VIOLATION: "Consequence: fabricated timestamps break temporal speaker analysis, meeting structure inference, and cross-session reconciliation" | NPT-009 | `.governance.yaml` forbidden_actions | T4 | Yes — additive |

---

## Cross-Family Patterns (L2)

### Systemic Gaps Summary: EC Criteria to Systemic Gap Mapping

The table below explicitly links each evaluation criterion (EC-01 through EC-06) to the systemic
gap it detected. This mapping was implicit in I1 — it is made explicit here per I2 traceability
gap fix.

| Systemic Gap | Detected by EC | EC Criterion Description | Evidence Source |
|---|---|---|---|
| Systemic Gap 1: Consequence documentation universally absent | **EC-03** | Consequence documentation in forbidden actions | All 15 agents fail EC-03; highest-maturity agents (nse-requirements, ts-parser) fail EC-03 despite passing EC-02 |
| Systemic Gap 2: Structural format divergence (XML vs. flat markdown) | **EC-02** | VIOLATION label usage — absent in flat-markdown agents | eng-team (E-013, E-014), red-team (E-015, E-016), saucer-boy (E-018) fail EC-02 entirely |
| Systemic Gap 3: NPT-011 entirely absent | **EC-04** | Domain-specific prohibitions beyond constitutional triplet | No agent uses NPT-011 justified prohibition (EC-04 only partially passed by nse-requirements and ts-parser for violation labels, not justifications) |
| Systemic Gap 4: L2-REINJECT inapplicable to agent files | **EC-06** | L2 re-injection of critical prohibitions — not applicable at agent layer | EC-06 is architectural, not per-agent; all agents fail EC-06 due to progressive disclosure Tier 2 loading model |

### Systemic Gap 1: Consequence Documentation Is Universally Absent

**NEVER underestimate the universality of this gap.** Across all 15 agents analyzed, ZERO
agents have complete NPT-009 compliance (structured VIOLATION label + scope + consequence
documentation). High-maturity agents (nse-requirements, ts-parser) have VIOLATION labels and
scope but lack consequence documentation. Low-maturity agents (eng-team, red-team) lack all
three components.

The implication is that every Jerry agent currently uses NPT-014 (blunt prohibition) as its
operational standard, even when VIOLATION labels create the appearance of NPT-009 structure.
The difference between NPT-014 and NPT-009 at the consequence level is:

- **NPT-014**: "NEVER spawn recursive subagents (P-003)"
- **NPT-009**: "NEVER spawn recursive subagents (P-003) — Consequence: recursive delegation makes
  output provenance untraceable, violates H-01 governance audit trail, and prevents quality gate
  attribution"

The AGREE-5 hierarchy (synthesis product, NOT externally validated) places NPT-009 at rank 9
and NPT-014 at rank 12. **NEVER present this ranking as experimentally established.** It is an
internally generated synthesis product of cross-survey agreement analysis (barrier-1/synthesis.md,
AGREE-5), with three competing causal explanations documented in barrier-2/synthesis.md (ST-5).

### Systemic Gap 2: Structural Format Divergence

Three structural patterns exist across the sample:
1. **XML-tagged** (problem-solving, nasa-se, adversary, worktracker, transcript): Use `<guardrails>`,
   `<capabilities>` sections. Consistent location for VIOLATION labels.
2. **Flat markdown — positive list** (eng-team, red-team): Use "What You Do NOT Do" section header.
   Prohibition items use positive list framing ("That is eng-devsecops") or are embedded in prose.
3. **Flat markdown — NEVER list** (saucer-boy): Uses a numbered `<constraints>` section with
   NEVER framing consistently, but without VIOLATION labels or consequence documentation. This
   is a distinct intermediate pattern — closer to NPT-009 vocabulary than eng-team/red-team
   (uses NEVER consistently) but without the structured annotation of NPT-009.

**The flat markdown structure is not per-se weaker than XML-tagged structure.** The content
determines effectiveness, not the wrapping. However, the flat structure makes automated auditing
harder — a grep for "VIOLATION:" will miss prohibitions expressed as "That is eng-devsecops."
**NEVER recommend converting all flat-markdown agents to XML-tagged structure in Phase 4** —
that is a structural refactor, not a negative prompting upgrade, and should be scoped as a
separate ADR if desired.

The Phase 4 recommendation for flat-markdown agents is targeted: convert "What You Do NOT Do"
list items to NEVER/VIOLATION-labeled entries within the existing flat structure, without
requiring XML tag adoption.

### Systemic Gap 3: NPT-011 (Justified Prohibition) Is Entirely Absent

No agent in the 15-agent sample uses NPT-011 (justified prohibition with contextual reason).
The AGREE-9 finding from barrier-1/synthesis.md documents "moderate cross-survey agreement" for
contextual justification improving adherence. **NEVER present AGREE-9 as establishing T1 causal
evidence.** The cross-survey agreement is T4 observational; no controlled comparison of
justified vs. unjustified prohibition exists in the evidence base.

The practical implication is that NPT-011 represents the highest-upside/highest-uncertainty
upgrade available. If Phase 2 confirms a framing effect at ranks 9–11, NPT-011 would move from
T4/Untested to confirmed-effective. The Phase 4 recommendation for NPT-011 is therefore:
**apply NPT-011 only to prohibitions where the reason is non-obvious** (not to constitutional
triplet entries where the reason is established governance, but to domain-specific entries where
a future agent designer might not understand the constraint's origin).

### Systemic Gap 4: L2-REINJECT Applicability to Agent Files

NPT-012 (L2 re-injected negative constraint) is currently applied only to rule files in
`.context/rules/`. Agent files loaded via the Task tool are not subject to the L2-REINJECT
mechanism. This means T-004 failure mode (context compaction dropping NEVER rules) applies to
agent-file prohibitions in a way it does not apply to rule-file prohibitions.

**NEVER recommend applying L2-REINJECT to agent `.md` files as a Phase 4 change.** This requires
an architectural analysis of whether agent system prompts re-inject on each turn (they do not,
per progressive disclosure Tier 2 loading model) and whether a per-agent L2 mechanism would
require changes to the Claude Code session startup mechanism. This is a Phase 5 ADR question,
not a Phase 4 agent update.

### Framework-Level Recommendations

| Rec ID | Change | NPT | Target | Evidence Tier | PG-003 Reversible |
|--------|--------|-----|--------|--------------|-------------------|
| REC-F-001 | Update guardrails template in `agent-development-standards.md`: replace `"Spawn recursive subagents (P-003)"` minimum example with NPT-009 format: `"P-003 VIOLATION: NEVER spawn recursive subagents — Consequence: recursive delegation makes output provenance untraceable and violates H-01 audit trail"` | NPT-009 | `.context/rules/agent-development-standards.md` | T4 | Yes — minimum example is illustrative, not schema-enforced |
| REC-F-002 | Add VIOLATION label format guidance to guardrails template: "forbidden_actions entries SHOULD use format: `{VIOLATION-TYPE} VIOLATION: NEVER {action} — Consequence: {operational impact}`" | NPT-009 | `.context/rules/agent-development-standards.md` | T4 | Yes — additive guidance |
| REC-F-003 | Add guidance that domain-specific forbidden_actions entries MUST describe the consequence for agent types T2+: T1 agents (read-only evaluators) MAY use NPT-014 minimum; T2+ agents with state-affecting tools SHOULD use NPT-009 complete format | NPT-009 | `.context/rules/agent-development-standards.md` | T4 | Yes — additive tier-differentiated guidance |

---

## Governance YAML Analysis

### Current State of `.governance.yaml` Negative Constraints

The `.governance.yaml` companion files contain `capabilities.forbidden_actions` as the primary
location for machine-readable prohibitions. Based on the agent `.md` file analysis, the following
patterns are inferred for governance YAML content:

**NEVER treat the following as confirmed audit findings** — governance YAML files were NOT
directly read during this analysis. The inferences are based on what agent `.md` body content
implies about YAML content, plus schema validation requirements (H-34/H-35).

**Evidence tier distinction (I2 addition):** The table below distinguishes T4 (directly observed)
from T4 (inferred, YAML not read). These were conflated under a single T4 label in I1. NEVER
treat inferred YAML findings with the same confidence as directly-observed `.md` body findings.

| Pattern | Agent Families | Evidence Tier | NPT Equivalent |
|---------|----------------|--------------|----------------|
| Constitutional triplet entries (schema-mandatory per H-35) | All agents | T4 (schema-confirmed — H-35 enforcement is observable from passing CI validation) | NPT-013 |
| Blunt prohibition without consequence (minimum set from guardrails template) | All agents | T4 (inferred, YAML not read — inferred from `.md` body content + guardrails template minimum) | NPT-014 |
| Domain-specific entries beyond triplet | nse-requirements, ts-parser, wt-auditor | T4 (inferred, YAML not read — inferred from `.md` body domain-specific VIOLATION entries implying corresponding YAML entries) | NPT-009 partial |
| Consequence documentation | Unknown — NOT observable from `.md` alone | T4 (inferred, YAML not read — UNKNOWN, cannot confirm or deny) | NPT-009 complete or absent |
| sb-voice YAML content | Unknown — sb-voice has no governance file visible in `.md` | T4 (inferred, YAML not read — P-003 Self-Check in `.md` suggests YAML exists; content unconfirmed) | NPT-014 minimum at best |

### Governance YAML Schema Recommendations

| Rec ID | Change | NPT | Target | Evidence Tier | PG-003 Reversible |
|--------|--------|-----|--------|--------------|-------------------|
| REC-YAML-001 | Add `forbidden_action_format` field to `agent-governance-v1.schema.json`: optional enum with values `NPT-009-complete` (VIOLATION label + scope + consequence), `NPT-009-partial` (VIOLATION label + scope), `NPT-014` (blunt). Use to track per-entry upgrade status during Phase 5 migration | NPT-009 | `docs/schemas/agent-governance-v1.schema.json` | T4 | Yes — additive optional field |
| REC-YAML-002 | Add pattern recommendation to schema description for forbidden_actions items: "RECOMMENDED format: `{TYPE} VIOLATION: NEVER {action} — Consequence: {impact}`. Minimum: `{description} ({principle-reference})`" | NPT-009 | Schema `$comment` or description field | T4 | Yes — documentation-only change |

**NEVER require NPT-009-complete format at schema validation level (JSON Schema `pattern`
constraint).** The enforcement mechanism for consequence documentation is guidance and template
upgrade, not schema rejection. Schema-level enforcement would cause all existing agents to fail
H-34 validation until migrated — creating a governance debt that exceeds the benefit of the
constraint during the transition period.

---

## Evidence Gap Map

> Per recommendation family, this map identifies the evidence tier supporting each NPT pattern
> and what controlled evidence does NOT exist.

| NPT Pattern | AGREE-5 Rank | T1 Evidence | T3 Evidence | T4 Evidence | Untested Dimension |
|-------------|-------------|-------------|-------------|-------------|-------------------|
| NPT-014 (blunt prohibition) | 12 (worst) | Multiple compliance/negation accuracy studies showing underperformance | ArXiv preprints confirming | VS-001 (33 Jerry instances — describes usage, not effectiveness) | Causal mechanism not established by T1 studies |
| NPT-013 (constitutional triplet) | Schema-mandatory | Not applicable (schema enforcement, not framing) | Not applicable | VS-001 (NC instances in rule files); H-34/H-35 schema requirement | LLM adherence improvement over no-triplet baseline: UNTESTED |
| NPT-012 (L2 re-injection) | Not in AGREE-5 | None | None | VS-001 (NC instances have L2 markers in rule files) | Improvement over non-injected prohibition: UNTESTED |
| NPT-011 (justified prohibition) | 9-11 range | None | None | AGREE-9 moderate cross-survey agreement | Controlled comparison justified vs. unjustified: UNTESTED |
| NPT-010 (paired prohibition) | 9-11 range | None | None | AGREE-8 moderate cross-survey agreement | Controlled comparison paired vs. unpaired: UNTESTED |
| NPT-009 (declarative behavioral negation) | 9-11 range | None | None | AGREE-7 observational support; VS-001 (Jerry rule files) | Controlled comparison with positive equivalents: UNTESTED |

### What This Means for Phase 4 Recommendations

**NEVER recommend NPT-009, NPT-010, or NPT-011 without this evidence tier qualifier:**
All recommendations for upgrading agent prohibitions to NPT-009/NPT-010/NPT-011 format are
informed by T4 observational evidence (vendor self-practice, practitioner surveys) and
UNTESTED against controlled positive-framing alternatives. Phase 2 will provide the first
controlled evidence for this comparison at ranks 9–11.

**The 32 recommendations in this analysis are working-practice upgrades, not
experimentally-validated improvements.** They are consistent with the vendor self-practice
evidence (VS-001 through VS-004: Anthropic uses NEVER/MUST NOT in its own framework rules
at the HARD tier) and the AGREE-5 hierarchy synthesis. They are NOT confirmed to outperform
their current NPT-014 baselines.

### Evidence Sources Not Dismissed

Per Orchestration Directive 3 (MUST NOT dismiss practitioner evidence or vendor self-practice
evidence as inferior): The VS-001 through VS-004 evidence from supplemental-vendor-evidence.md
is treated as a valid T4 source throughout this analysis. Anthropic's own practice of using
NEVER/MUST NOT in 33 instances across 10 Claude Code rule files — when their published behavioral
engineering documentation diverges from this practice (VS-002 divergence finding) — constitutes
meaningful practitioner evidence of working-practice preference, distinct from claims about
LLM framing effectiveness.

**NEVER treat the VS-002 divergence as invalidating VS-001 through VS-004.** The divergence
between published recommendation and self-practice creates an interpretive ambiguity (three
competing explanations documented in barrier-2/synthesis.md ST-5), not a null finding.

---

## PG-003 Contingency Plan

### The Contingency Scenario

PG-003 (barrier-2/synthesis.md): If Phase 2 finds a null framing effect at ranks 9–11 (NPT-009,
NPT-010, NPT-011), vocabulary choice between NEVER/MUST NOT/DO NOT and positive alternatives
becomes convention-determined, not effectiveness-determined.

Under this scenario, the question "should Jerry agent forbidden_actions entries use NPT-009
structured format or positive alternatives?" has no effectiveness answer — both produce equivalent
LLM adherence. The decision then defaults to convention consistency, readability, and auditability
rather than effectiveness.

### What Changes Under PG-003 Null Finding

| Recommendation | Status Under Null Finding | Revised Action |
|---------------|--------------------------|----------------|
| REC-ADV-001 through REC-TS-003 (consequence documentation additions) | Consequence documentation is structurally valuable regardless of framing — it improves human readability and auditability. **NEVER dismiss consequence documentation as only valuable for LLM framing.** | Consequence documentation recommendations remain valid — reclassify rationale from "framing effectiveness" to "auditability and readability" |
| REC-ENG-001 (convert "What You Do NOT Do" to VIOLATION format) | If framing is null, the conversion from positive list to NEVER/VIOLATION format has no effectiveness justification. The motivation would be consistency with other agent families only. | Downgrade from recommendation to optional stylistic alignment. Include explicit statement: "This change is convention-alignment only, not effectiveness-motivated." |
| REC-F-001 (update guardrails template) | If framing is null, the minimum example update from NPT-014 to NPT-009 is convention-alignment. New agents built after the update will follow NPT-009 format without effectiveness benefit. | Retain recommendation as convention-alignment. The consequence documentation component retains independent motivation (auditability). |
| REC-YAML-001 (schema tracking field) | Audit tracking of NPT format level remains valuable regardless of framing outcome — it provides upgrade path visibility. | Retain recommendation unchanged. |

### PG-003 Reversibility Verification

Every recommendation in this analysis has been tagged with "PG-003 Reversible: Yes" or rationale
for exceptions. All 32 recommendations are reversible because all changes are additive
(consequence text additions, new VIOLATION label additions, new NPT-011 justification sections,
new /saucer-boy family entries). NONE of the recommendations delete existing constraint text.

**NEVER recommend deleting existing prohibitions.** Even under a null finding, existing
prohibitions retain their current adherence level (whatever it is). Deletion would reduce
adherence. The reversibility concern is about NEW text being added with framing motivation —
if the framing is null, the new text is convention-motivated, not harmful.

### PG-003 Decision Gate for Phase 5

Phase 5 (ADR writing) MUST include a gate at this point: "If Phase 2 data has been collected
for conditions C1–C7 prior to ADR drafting, apply PG-003 evaluation to all framing-motivated
recommendations. If Phase 2 data is not yet available, flag all framing-motivated recommendations
as contingent on Phase 2 outcome."

---

## Phase 5 Downstream Inputs

Phase 5 is responsible for ADR drafting: translating Phase 4 analysis recommendations into
architectural decisions about Jerry agent definition standards.

### What Phase 5 Receives From This Analysis

| Input Type | Content | Location in This Document |
|-----------|---------|--------------------------|
| Recommendation catalog | 32 specific recommendations (REC-ADV-001 through REC-YAML-002, including 3 new REC-SB entries) with NPT tags, evidence tiers, location specifications, and PG-003 reversibility | Per-Family Analysis sections |
| Framework-level standard changes | 3 recommendations for `agent-development-standards.md` (REC-F-001 through REC-F-003) and 2 governance schema updates (REC-YAML-001, REC-YAML-002) | Cross-Family Patterns (REC-F-001–F-003); Governance YAML Analysis (REC-YAML-001–002) |
| Evidence tier classification | Per-recommendation T4/Untested classification; distinguished T4 (directly observed, .md body) vs. T4 (inferred, YAML not read) | Evidence Gap Map; Governance YAML Analysis |
| PG-003 contingency assessment | Per-recommendation status under null finding scenario | PG-003 Contingency Plan |
| Structural gap findings | eng-team and red-team agents use flat markdown; saucer-boy uses NEVER-list flat markdown (distinct intermediate pattern); XML-tagged structure more auditable | Cross-Family Patterns, Systemic Gap 2 |
| Maturity baseline | nse-requirements and ts-parser as reference implementations for NPT-009 complete format | Per-Family Analysis, nse-requirements and ts-parser sections |

### Recommendation-to-Phase-5-ADR Forward Reference Map

Each recommendation feeds a specific Phase 5 ADR decision. NEVER assume a recommendation is
covered by a Phase 5 gate without explicit assignment. The table below makes all forward
references explicit (I2 traceability fix):

| Recommendation | Phase 5 ADR Decision | Decision Gate |
|---|---|---|
| REC-ADV-001 through REC-ADV-003 | D-002 (sequencing: backfill existing agents) | D-002 governs per-family rollout sequence |
| REC-PS-001 through REC-PS-003 | D-002 | Same sequencing decision |
| REC-NSE-001 through REC-NSE-002 | D-002 | Same sequencing decision |
| REC-ORCH-001 through REC-ORCH-003 | D-002 | Same sequencing decision |
| REC-ENG-001 through REC-ENG-004 | D-002 + D-004 | D-004 governs whether structural refactor is in scope for flat-markdown agents |
| REC-RED-001 through REC-RED-003 | D-002 + D-004 | Same structural refactor decision |
| REC-WT-001 through REC-WT-003 | D-002 | Standard sequencing |
| REC-SB-001 through REC-SB-003 | D-002 | Standard sequencing; sb-voice NEVER-list format is additive-only, no structural refactor needed |
| REC-TS-001 through REC-TS-003 | D-002 | Standard sequencing |
| REC-F-001 through REC-F-003 | **D-001** | D-001 governs whether to update `agent-development-standards.md` guardrails template |
| **REC-YAML-001** | **D-003** | D-003 governs whether to add `forbidden_action_format` tracking field to governance schema |
| **REC-YAML-002** | **D-006** (new; see below) | D-006 governs whether to add schema description field recommendation for forbidden_actions format |

### What Phase 5 MUST NOT Do (Based on This Analysis)

**NEVER modify agent files before Phase 2 experimental conditions are complete.** The C1–C7
conditions include agents in their current baseline state. Any modification to forbidden_actions
entries, VIOLATION labels, or consequence documentation before Phase 2 data collection makes
the experimental conditions unreproducible per Orchestration Directive 6.

**NEVER batch-apply NPT-009 consequence documentation across all agents without family-specific
review.** The consequence documentation for a T1 read-only evaluator (adv-scorer) differs
fundamentally from an engagement-scope agent (red-lead). Phase 5 ADR MUST specify per-family
consequence documentation standards, not a universal template.

**NEVER treat this analysis as a complete agent audit.** The 15-agent sample covers representative
families across 9 of 10 registered skills (all except `/saucer-boy-framework-voice`), but does
not include: ps-architect, ps-validator, ps-synthesizer, ps-reporter, ps-investigator, ps-reviewer,
nse-explorer, nse-architecture, orch-tracker, orch-synthesizer, eng-lead, eng-backend, eng-frontend,
eng-infra, eng-devsecops, eng-qa, eng-reviewer, eng-incident, red-vuln, red-exploit, red-privesc,
red-lateral, red-persist, red-exfil, red-reporter, red-infra, red-social, adv-selector, ts-extractor,
sb-framework-voice. Phase 5 ADR MUST specify whether recommendations apply universally or only
after a full audit. The /saucer-boy family is now covered by REC-SB-001 through REC-SB-003
(I2 addition) — only `/saucer-boy-framework-voice` remains unanalyzed in that skill family.

### Phase 5 ADR Decisions Required

| Decision ID | Decision Required | Input From This Analysis | Feeds Recommendations |
|-------------|------------------|--------------------------|----------------------|
| D-001 | Whether to update `agent-development-standards.md` guardrails template (REC-F-001 through REC-F-003) | Framework-level recommendations; confirmation that template change is reversible under PG-003 | REC-F-001, REC-F-002, REC-F-003 |
| D-002 | Sequencing: update template first (all new agents comply) vs. backfill existing agents first | Maturity baseline shows existing high-maturity agents already exceed template minimum; 27 agent-level recommendations covering all 9 families | REC-ADV-001 to REC-TS-003 (all 27 agent-level recs, including REC-SB-001 to REC-SB-003) |
| D-003 | Whether to add `forbidden_action_format` tracking field to governance schema (REC-YAML-001) | Schema recommendation; confirmed additive optional field; directly observed gap in governability of per-entry upgrade status | **REC-YAML-001 only** |
| D-004 | Whether structural refactor (flat-markdown to XML-tagged) is in scope for Phase 5 | Cross-Family Patterns: structural gap documented in eng-team, red-team; NOT recommended as Phase 4 change; saucer-boy NEVER-list variant identified as distinct intermediate pattern requiring no structural refactor | REC-ENG-001, REC-ENG-002, REC-RED-001 (structural component only) |
| D-005 | PG-003 gate: whether Phase 2 data is available before ADR is finalized | PG-003 Contingency Plan; per-recommendation null-finding response | All 32 recommendations (framing-motivated recs reclassified to convention-alignment under null finding) |
| **D-006** | Whether to add schema description field recommendation for forbidden_actions format (REC-YAML-002) | REC-YAML-002 adds a pattern recommendation to the schema `$comment` or description field; this is documentation-only in the schema, not a structural field addition — different scope from D-003's new tracking field | **REC-YAML-002 only** |

**D-006 rationale:** REC-YAML-002 was not assigned to any Phase 5 decision gate in I1. It was
present in the Governance YAML Analysis section but absent from D-001 through D-005. The omission
created a floating recommendation with no downstream disposition. D-006 provides the explicit
gate. NEVER subsume REC-YAML-002 into D-003 — D-003 governs adding a new optional tracking field
(machine-readable); D-006 governs adding a human-readable format recommendation to the schema
description (documentation-only, no schema validation impact).

---

## Evidence Summary

| Evidence ID | Type | Source | Evidence Tier | Relevance |
|-------------|------|--------|--------------|-----------|
| E-001 | Taxonomy catalog | phase-3/taxonomy-pattern-catalog.md | T4 (synthesis product) | NPT-001 through NPT-014 pattern definitions, AGREE-5 hierarchy, C1–C7 matrix |
| E-002 | Survey synthesis | barrier-1/synthesis.md | T4 (cross-survey synthesis) | AGREE-1 through AGREE-9 findings, 12-level hierarchy source, 75 deduplicated sources |
| E-003 | Vendor self-practice | barrier-1/supplemental-vendor-evidence.md | T4 (observational) | VS-001: 33 NC instances across 10 rule files; VS-002: published recommendation divergence |
| E-004 | Protocol synthesis | barrier-2/synthesis.md | T4 (synthesis product) | ST-1 through ST-6, PG-001 through PG-005, Phase 4 constraints |
| E-005 | Agent definition | skills/adversary/agents/adv-executor.md | T4 (directly observed, .md body) | Adversary family current negative constraint patterns; direct quote from P-003 Self-Check section confirming MUST NOT Task tool prohibition |
| E-006 | Agent definition | skills/adversary/agents/adv-scorer.md | T4 (directly observed, .md body) | Adversary family leniency bias counteraction structure |
| E-007 | Agent definition | skills/problem-solving/agents/ps-analyst.md | T4 (directly observed, .md body) | Problem-solving family VIOLATION label usage |
| E-008 | Agent definition | skills/problem-solving/agents/ps-researcher.md | T4 (directly observed, .md body) | Problem-solving family forbidden_actions structure |
| E-009 | Agent definition | skills/problem-solving/agents/ps-critic.md | T4 (directly observed, .md body) | Problem-solving family LOOP VIOLATION domain-specific prohibition; direct quote from Forbidden Actions block confirming LOOP VIOLATION and P-022 VIOLATION labels |
| E-010 | Agent definition | skills/nasa-se/agents/nse-requirements.md | T4 (directly observed, .md body) | Highest-maturity negative constraint reference implementation; direct quotes from Forbidden Actions block (P-043 VIOLATION, P-040 VIOLATION) and mandatory DISCLAIMER section |
| E-011 | Agent definition | skills/nasa-se/agents/nse-verification.md | T4 (directly observed, .md body) | NASA-SE family partial NPT-009 patterns |
| E-012 | Agent definition | skills/orchestration/agents/orch-planner.md | T4 (directly observed, .md body) | Orchestration family HARDCODING VIOLATION domain-specific prohibition |
| E-013 | Agent definition | skills/eng-team/agents/eng-architect.md | T4 (directly observed, .md body) | Eng-team flat markdown structural pattern; "What You Do NOT Do" format |
| E-014 | Agent definition | skills/eng-team/agents/eng-security.md | T4 (directly observed, .md body) | Eng-team family flat markdown constraint pattern |
| E-015 | Agent definition | skills/red-team/agents/red-lead.md | T4 (directly observed, .md body) | Red-team scope YAML boolean constraints; authorization schema |
| E-016 | Agent definition | skills/red-team/agents/red-recon.md | T4 (directly observed, .md body) | Red-team SCOPE_REVIEW_REQUIRED circuit breaker mechanism |
| E-017 | Agent definition | skills/worktracker/agents/wt-auditor.md | T4 (directly observed, .md body) | Worktracker H-33 domain-specific prohibition; P-010 VIOLATION; direct quotes from Forbidden Actions block (P-003/P-020/P-002/P-010 VIOLATION entries) and H-33 enforcement note confirming DO NOT Read+Grep prohibition is in Capabilities section, not Forbidden Actions block |
| E-018 | Agent definition | skills/saucer-boy/agents/sb-voice.md | T4 (directly observed, .md body) | Saucer-boy NEVER-list flat constraint section; direct quotes from `<constraints>` block (six NEVER entries, lines 138–144) and P-003 Self-Check section confirming VIOLATION label + halt instruction for P-003 only |
| E-019 | Agent definition | skills/transcript/agents/ts-parser.md | T4 (directly observed, .md body) | Transcript CONTENT VIOLATION and TIMESTAMP VIOLATION — strongest domain-specific set in sample; direct quotes from Forbidden Actions block confirming all five VIOLATION entries verbatim (P-003, P-002, P-022, CONTENT, TIMESTAMP); absence of consequence documentation confirmed across all five entries |
| E-020 | Framework standard | .context/rules/agent-development-standards.md | T4 (directly observed, .md body; framework rule) | H-34/H-35 guardrails template; minimum set notice; forbidden_actions schema requirements |

**Evidence tier clarification (I2 addition):** All E-005 through E-020 entries are classified as
`T4 (directly observed, .md body)` — the agent `.md` files were directly read during this
analysis. This is distinct from governance YAML inferences (documented separately in the
Governance YAML Analysis section). NEVER conflate `.md` body observations with YAML content
claims — YAML content for all agents is T4 (inferred, YAML not read) unless schema validation
(H-34/H-35) provides indirect confirmation.

---

## PS Integration

```yaml
analyst_output:
  ps_id: "phase-4"
  entry_id: "TASK-011"
  analysis_type: "gap"
  artifact_path: "projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-4/agents-update-analysis.md"
  artifact_version: "3.0.0"
  root_cause: "Jerry agent forbidden_actions entries universally use NPT-014 (blunt prohibition) as operational standard; consequence documentation (completing NPT-009) is absent across all 15 agents analyzed"
  recommendation: "Add consequence documentation to existing VIOLATION-labeled entries (additive, reversible); update agent-development-standards.md guardrails template minimum example to NPT-009 format; defer structural refactor and framing-motivated changes until Phase 2 data collection is complete"
  confidence: "medium"
  evidence_tiers: "T4 (directly observed, .md body) for all 15 agent .md files; T4 (inferred, YAML not read) for all governance YAML claims; zero T1 evidence for NPT-009/NPT-010/NPT-011 improvement over NPT-014 baseline in Jerry agent context"
  pg_003_status: "All 32 recommendations are additive and reversible under null framing effect scenario; framing-motivated items reclassified to convention-alignment if PG-003 fires"
  recommendation_count: 32
  recommendation_breakdown:
    agent_level: 27
    framework_level_standards: 3
    framework_level_schema: 2
    note: "agent_level is 27 (was 24 in I1; I2 adds 3 new REC-SB entries for /saucer-boy family)"
  phase_5_decisions: "D-001 through D-006 (D-006 added in I2 for REC-YAML-002 governance schema description update)"
  next_agent_hint: "ps-architect for Phase 5 ADR drafting (D-001 through D-006 decision gates)"
```

---

*Analysis Version: 3.0.0*
*Agent: ps-analyst (TASK-011)*
*Date: 2026-02-28*
*I2 Revision: Fix recommendation count (I1 stated 27; actual I1 total was 29 with REC-YAML-001/002 unaccounted; I2 adds REC-SB-001/002/003 = final count 32). Add Family 9 /saucer-boy per-family section with direct quotes from sb-voice.md. Add direct textual quotes from adv-executor.md, ps-critic.md, nse-requirements.md with T4-observed vs. T4-inferred distinction. Add explicit EC-to-systemic-gap mapping table. Add D-006 for REC-YAML-002. Add recommendation-to-ADR forward reference map.*
*I3 Revision: Fix three stale rec counts in body (lines 101: 29→32; 747: 27→32; 879: 29→32). Correct evidence inference percentage (55%→53%, denominator 17/32). Fix EC-01 maturity rubric contradiction: all three maturity levels now show EC-01 PASS (schema-enforced); low-maturity no longer shows EC-01 partial (contradicted by H-35 enforcement). Add EC-03 partial/FAIL operational definition. Expand REC-ENG-003 with failure-case path (create .governance.yaml from template; add constitutional triplet if below minimum). Enumerate all 5 eng-architect "What You Do NOT Do" items with draft VIOLATION labels and consequence text in REC-ENG-001. Add direct quotes for ts-parser (full five-entry Forbidden Actions block verbatim) and wt-auditor (four-entry Forbidden Actions block plus H-33 placement finding). Update E-017, E-019 evidence table entries to reflect direct quote coverage.*
*Constitutional Compliance: P-001 (all conclusions cite evidence, direct quotes added for key per-family findings), P-002 (persisted to file), P-022 (evidence tier disclosed, T4-observed vs. T4-inferred distinguished, speculation labeled)*
*Orchestration Directives Compliance: All 7 directives verified — framing uses NEVER/MUST NOT throughout; supplemental vendor evidence cited (E-003); T4 evidence not dismissed; absence-of-evidence not treated as null; enforcement tier vocabulary not presented as validated; no Phase 2 condition changes recommended; PG-003 contingency documented*

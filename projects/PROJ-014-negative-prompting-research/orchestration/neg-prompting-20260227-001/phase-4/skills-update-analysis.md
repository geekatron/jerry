# Phase 4: Jerry Skills Update Analysis

> **Document ID:** TASK-010-skills-update-analysis
> **Version:** 2.0.0
> **Phase:** Phase 4 — Application Analysis
> **Workflow ID:** neg-prompting-20260227-001
> **Agent:** ps-analyst (TASK-010)
> **Date:** 2026-02-28
> **Criticality:** C4
> **Status:** REVISED — I1 adversary gaps addressed (v2.0.0)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical stakeholder summary |
| [L1: Analysis Methodology](#l1-analysis-methodology) | Framework, evidence sources, analytical approach |
| [NPT Applicability Filter](#npt-applicability-filter) | Which NPT patterns are in scope for SKILL.md files and why |
| [L2: Per-Skill Analysis](#l2-per-skill-analysis) | Detailed findings for each of 13 SKILL.md files |
| [Cross-Skill Patterns](#cross-skill-patterns) | Architectural patterns observed across the skill set |
| [Evidence Gap Map](#evidence-gap-map) | Where evidence for recommendations is strong vs. contingent |
| [PG-003 Contingency Plan](#pg-003-contingency-plan) | Reversibility assessment for Phase 2 null framing effect |
| [Phase 5 Downstream Inputs](#phase-5-downstream-inputs) | What the architect and implementation planner need from this analysis |
| [Evidence Summary](#evidence-summary) | Traceability table for all evidence cited |

---

## L0: Executive Summary

### What was analyzed

Thirteen Jerry Framework SKILL.md files were examined to determine where and how negative prompting patterns from the Phase 3 taxonomy (NPT-001 through NPT-014) should be applied to skill definitions. The analysis covers the adversary, architecture, ast, bootstrap, eng-team, nasa-se, orchestration, problem-solving, red-team, saucer-boy, saucer-boy-framework-voice, transcript, and worktracker skills.

### Key finding

MUST NOT apply any single description of current skill quality, because the pattern is not uniform. The skills fall into three distinct groups:

**Group A (5 skills — minimal negative constraint usage):** bootstrap, saucer-boy, saucer-boy-framework-voice, worktracker, transcript. These are domain-specific skills where the domain itself provides most behavioral guidance. They use positive framing throughout. Negative constraint additions would be low-risk and low-impact here.

**Group B (5 skills — partial negative constraint usage):** adversary, ast, nasa-se, architecture, red-team. These use "Do NOT use when:" sections and scattered prohibitions. They partially implement NPT-010 (negation-paired alternative) but lack consequence documentation and consistency.

**Group C (3 skills — implicit negative constraint usage):** eng-team, orchestration, problem-solving. These contain the most behaviorally critical constraints but express them inconsistently — some as NEVER-framed prohibitions (NPT-014 pattern), some as positive observations ("Agents cannot spawn nested agents"), and only rarely with consequence documentation (NPT-009 pattern).

### Primary recommendation

MUST NOT implement skill updates until Phase 2 experimental results are available for ranks 9-11 of the hierarchy, because the most impactful recommendations (upgrading constitutional compliance tables to NPT-009 framing) depend on T4-only evidence with UNTESTED causal comparison against positive equivalents. The one unconditional recommendation is:

NEVER leave blunt prohibition instances (NPT-014 diagnostic — "NEVER hardcode values" appearing without consequence documentation) unfixed, because PG-001 carries HIGH unconditional confidence (T1+T3) that standalone blunt prohibition is the weakest constraint formulation.

---

## L1: Analysis Methodology

### Orchestration directives applied

This analysis was conducted under the following non-negotiable constraints from the Phase 4 orchestration plan:

1. MUST NOT use positive prompting framing — all recommendations expressed as NEVER/MUST NOT constraints
2. MUST NOT omit supplemental vendor evidence (VS-001 through VS-004)
3. MUST NOT dismiss practitioner or vendor self-practice evidence as inferior
4. MUST NOT treat absence of published evidence as evidence of absence
5. MUST NOT present enforcement tier vocabulary design as experimentally validated
6. MUST NOT recommend changes that make Phase 2 experimental conditions unreproducible
7. MUST NOT ignore PG-003's contingency (null Phase 2 framing effect at ranks 9-11)

### Evidence sources

| Source ID | Type | Description | Evidence Tier |
|-----------|------|-------------|---------------|
| NPT-001 through NPT-014 | Taxonomy | Phase 3 pattern catalog — 14 entries covering 13 distinct techniques | T4 (compiled) |
| PG-001 through PG-005 | Guidance | Phase 3 practitioner guidance with explicit confidence tiers | T1/T3/T4 |
| VS-001 through VS-004 | Vendor | Anthropic's own 33-instance negative constraint practice in Claude Code rule files | T4 |
| AGREE-5 | Synthesis | 12-level effectiveness hierarchy (internally generated — NOT externally validated) | T4 (internal synthesis) |
| Barrier-1 synthesis | Cross-survey | 75-source catalog, 9 cross-survey agreements | T1/T3/T4 |
| Barrier-2 synthesis | Analysis | Confidence reconciliation, Phase 4 constraints, ST-1 through ST-7 | Cross-tier |

### Analytical framework applied

**Phase A — Current state audit per skill:** MUST NOT overlook instances of positive framing where negative constraint framing would apply. MUST NOT count "Do NOT use when:" as equivalent to NPT-009 (declarative behavioral negation with consequence) — these are different patterns at different hierarchy levels. Implicit prohibitions (positive sentences with exclusionary meaning, such as scope conditions) are NOT in scope for this audit unless they co-occur with enforcement tier vocabulary (MUST/NEVER/SHALL).

**Phase B — NPT pattern mapping per skill domain:** MUST NOT apply all 14 patterns uniformly — pattern applicability is domain-specific. Constitutional constraints (P-003/P-020/P-022) are candidates for NPT-013 (constitutional triplet). Authorization constraints (scope validation, circuit breaker) are candidates for NPT-009/NPT-010. Routing constraints are candidates for NPT-012 (L2 re-injected).

**Phase C — Gap analysis:** MUST NOT treat all gaps as equivalent. Gaps in blunt prohibition (NPT-014) are unconditional problems (PG-001 HIGH). Gaps in hierarchical framing (NPT-006/NPT-007) are effectiveness-contingent (PG-003 MEDIUM, reversible).

**Phase D — Reversibility assessment:** MUST NOT omit reversibility classification, because PG-003 states: if Phase 2 finds null framing effect at ranks 9-11, vocabulary choice becomes convention-determined, not effectiveness-determined.

### NPT Diagnostic Filter (NPT-014)

NEVER treat a "NEVER X" statement without consequence, scope, or positive pairing as equivalent to NPT-009 (declarative behavioral negation). The following definition was applied as the diagnostic filter:

**NPT-014 (Blunt Prohibition — diagnostic):** Any NEVER/MUST NOT statement that lacks (a) explicit consequence if violated, (b) explicit scope of applicability, and (c) a positive behavioral pairing describing what to do instead.

All instances identified as NPT-014 candidates are recommended for upgrade to NPT-009 minimum.

---

## NPT Applicability Filter

This table explains why NPT-001 through NPT-008 are not mapped in per-skill recommendations, and which patterns are in scope for SKILL.md files.

### Domain Distinction: SKILL.md vs. Rule Files

SKILL.md files serve as routing and invocation guides for LLM agents. They describe WHEN to invoke a skill, HOW the skill operates, and WHAT behavioral constraints govern the skill's agents. They are distinct from `.context/rules/` files, which are L1-loaded governance documents expressing framework-wide policies.

The following NPT patterns operate primarily at the **rule file level** or require **cross-document enforcement infrastructure** not present in SKILL.md:

| NPT Pattern | Domain | SKILL.md Applicable? | Rationale |
|-------------|--------|----------------------|-----------|
| NPT-001 | Simple negation ("not X") | NO | Primitive pattern; subsumed by higher patterns. SKILL.md content at this level has no behavioral force. |
| NPT-002 | Negative scope marker ("not for X purposes") | NO | Rule file pattern. SKILL.md uses "Do NOT use when:" sections which are structurally superior. |
| NPT-003 | Negation via exclusion list | NO | Rule file pattern. SKILL.md structured alternatives ("route to /nasa-se instead") provide sufficient guidance. |
| NPT-004 | Conditional negation ("X unless Y") | NO | Context-dependent constraint. SKILL.md conditional logic belongs in agent definition governance.yaml, not SKILL.md body. |
| NPT-005 | Negation via contrast ("unlike X, Y does...") | NO | Comparative framing. SKILL.md disambiguation uses "MUST NOT use when:" routing, not contrast pairs. |
| NPT-006 | Hierarchical negation (tiered prohibition) | NO | Requires HARD/MEDIUM/SOFT tier vocabulary applied to rule files. SKILL.md does not host enforcement tier definitions. |
| NPT-007 | Gate-structured negation (stop-on-fail) | PARTIAL | Applies to SKILL.md authorization gates (e.g., red-team scope authorization HALT). Only one instance found (Skill 11 Authenticity Test 1). Not recommended as a new addition without a clear HALT trigger. |
| NPT-008 | Anti-pattern enumeration | PARTIAL | Applies to SKILL.md Anti-Patterns sections (saucer-boy, saucer-boy-framework-voice). Partial — existing NPT-008 instances present but lack consequence documentation. Upgrade path is to NPT-009. |
| NPT-009 | Declarative behavioral negation with consequence | YES | Primary target pattern for SKILL.md upgrades. Full applicability. |
| NPT-010 | Negation-paired alternative | YES | Applicable to all "Do NOT use when:" / "MUST NOT use when:" sections. 6 skills partially implement. |
| NPT-011 | Context-gated constraint | PARTIAL | Applies only to skills with context-dependent behavioral modes (saucer-boy Boundary Conditions). Not a general target. |
| NPT-012 | L2 re-injected prohibition | NO | L2 re-injection operates at rule file level via `.context/rules/` L2-REINJECT markers. SKILL.md is L1-loaded, not L2-injectable without a companion rule file entry. |
| NPT-013 | Constitutional triplet prohibition | YES | Directly applicable to Constitutional Compliance tables in all 13 skills. T4 confidence (VS-004), reversible. |
| NPT-014 | Blunt prohibition (diagnostic) | YES (diagnostic only) | Present in 4 skills as "NEVER hardcode values." All instances require NPT-009 upgrade. |

**Summary:** NPT-009, NPT-010, NPT-013, and NPT-014 (diagnostic) are the patterns in scope for SKILL.md files. NPT-007 and NPT-008 have limited applicability to specific sections. NPT-001 through NPT-006 and NPT-012 are out of scope for SKILL.md content — they operate at rule file, agent definition, or enforcement infrastructure layers.

---

## L2: Per-Skill Analysis

### Skill 1: adversary/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "Do NOT use when:" section | When-to-Use | Negation-paired alternative | Partial NPT-010 |
| "NEVER hardcode values" | Tool examples | Blunt prohibition | NPT-014 candidate |
| Constitutional Compliance table | All rows | Positive framing ("S-001 through S-014 analyzed") | Positive (no NPT pattern) |
| H-16/H-15 enforcement | Multiple sections | Positive imperative ("MUST be applied before") | Positive |

**Gap analysis:**

MUST NOT leave the "Do NOT use when:" section in its current form without consequence documentation. The section provides positive alternatives (redirects to /problem-solving, /nasa-se, etc.) but does not document what fails if the skill is used in the wrong context — missing the consequence component of NPT-009.

MUST NOT leave "NEVER hardcode values" as a standalone blunt prohibition (NPT-014). This is the weakest constraint formulation per PG-001 (E-002) (T1+T3, HIGH confidence, unconditional). It should be upgraded to NPT-009: specify what "hardcoding" means in the adversary skill context, what goes wrong when values are hardcoded, and the positive behavioral alternative.

MUST NOT present the Constitutional Compliance table entirely in positive framing. Vendor self-practice evidence VS-004 (E-009) shows constitutional constraints are expressed as prohibitions in Anthropic's own rule files (P-003/P-020/P-022 as NEVER statements with consequence). The current positive descriptions ("Agents are workers, not orchestrators") lack the prohibitive force documented in VS-003 (E-008) (HARD tier defined by prohibitive vocabulary).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Upgrade Constitutional Compliance table to NPT-013 (P-003/P-020/P-022 as triplet with NEVER framing) | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null at rank 9-11 | ADR-002 |
| Upgrade "NEVER hardcode values" to NPT-009 with consequence | NPT-009 | T1+T3 (PG-001, E-002 — unconditional) | NOT REVERSIBLE — blunt prohibition is always inferior | ADR-001 |
| Add consequence documentation to "Do NOT use when:" | NPT-010 | T4 (MEDIUM) | REVERSIBLE | ADR-003 |

---

### Skill 2: architecture/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| Layer Dependency Rules table | H-07 enforcement | Positive ("Domain Layer may import...") | Positive |
| MUST NOT import infrastructure | H-07(a) sub-item | Partial prohibition | Partial NPT-009 (no consequence documented in SKILL.md) |
| No explicit "Do NOT use when:" section | Absent | Gap | Gap |
| Constitutional Compliance | All rows | Positive | Positive |

**Gap analysis:**

MUST NOT treat the architecture skill's positive layer dependency descriptions as equivalent to prohibitions. The MUST NOT import rules appear in the `.context/rules/architecture-standards.md` rule file but the SKILL.md presents them in positive framing ("may import," "can import") which reduces constraint salience.

MUST NOT omit a "Do NOT use when:" section. The architecture skill lacks routing disambiguation, which creates AP-01 (Keyword Tunnel) risk when users need requirements design (/nasa-se) but architecture keywords trigger this skill instead (E-016).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Add "MUST NOT use when:" section with routing disambiguation | NPT-010 | T4 (routing clarity, E-016) | REVERSIBLE | ADR-003 |
| Add consequence statement to H-07 MUST NOT import rules in the SKILL.md summary | NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |
| Upgrade Constitutional Compliance table to prohibition framing for P-003 | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |

---

### Skill 3: ast/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "Do NOT use /ast for:" section | When-to-Use | Negation-paired alternative with alternatives provided | Partial NPT-010 |
| H-33 reference | Section header | Positive HARD rule reference | Positive |
| No NEVER/MUST NOT in main body | Throughout | Positive framing | Gap |

**Gap analysis:**

MUST NOT treat the current "Do NOT use /ast for:" section as fully compliant with NPT-010. The section lists excluded use cases but does not document consequences of misuse — what breaks if a consumer uses regex for frontmatter extraction instead of /ast? The consequence (AST validation failures, broken worktracker integrity) is documented in H-33 but not surfaced in the SKILL.md routing guidance (E-016).

MUST NOT leave the H-33 consequence chain undocumented in the skill body. NEVER leaving "use /ast for frontmatter extraction" as only a positive instruction without the paired "NEVER use regex for frontmatter extraction because [consequence]" (NPT-009 framing).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Add consequence documentation to "Do NOT use /ast for:" | NPT-010 | T4 (MEDIUM) | REVERSIBLE | ADR-003 |
| Add NPT-009 prohibition for regex-based frontmatter parsing with consequence (worktracker integrity failure) | NPT-009 | T4 (MEDIUM, mechanically consequenced) | REVERSIBLE | ADR-002 |

---

### Skill 4: bootstrap/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "NOT synced" note on guides | Content section | Informational negative | None (informational) |
| H-05 reference ("NEVER use python/pip") | Indirect reference | Points to rule file | Indirect NPT-012 reference |
| No NEVER/MUST NOT in main body | Throughout | Positive framing | Gap |
| Constitutional Compliance | Positive labels | Positive | Positive |

**Gap analysis:**

MUST NOT omit negative constraint framing for the H-05 Python environment rule in the bootstrap skill. The bootstrap skill is the entry point for new contributors. NEVER leaving the H-05 prohibition (NEVER use python/pip/pip3 directly) without surfacing it prominently in the bootstrap skill creates discovery failure for new users who will not read all rule files at first encounter.

MUST NOT treat the "NOT synced" note as a prohibition. It is informational text. If the consequence of using the guides (they may be stale) is important, it should be expressed as a constraint.

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Surface H-05 prohibition (NEVER use python/pip directly) explicitly in bootstrap SKILL.md with consequence | NPT-009 | T1+T3 (PG-001, E-002) | REVERSIBLE — surfacing H-05 in bootstrap is a new addition, not an NPT-014 upgrade; PG-001 unconditional applies to elimination of existing blunt prohibitions, not to new additions; revert by removing the H-05 block from SKILL.md | ADR-002 |
| Surface H-04 active project requirement as MUST NOT proceed without statement | NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |

**Note:** The bootstrap skill is primarily a navigation tool for contributors, not a behavioral constraint document. NPT additions here are lower-impact than in operational skills.

---

### Skill 5: eng-team/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "NEVER hardcode values" | Tool examples | Blunt prohibition | NPT-014 candidate |
| "Agents cannot spawn nested agents" | P-003 section | Positive observation | Gap (should be prohibition) |
| "No exceptions" | eng-reviewer invokes /adversary | Strong constraint | Partial NPT-009 |
| Constitutional Compliance | Positive descriptions | Positive | Positive |
| Threat modeling MUST NOT scope creep | Agent guidance | Implicit prohibition | Partial |

**Gap analysis:**

MUST NOT leave "Agents cannot spawn nested agents" in positive observation framing. This is the P-003 constraint — the most critical constitutional prohibition in the framework. VS-004 (E-009) shows Anthropic expresses constitutional constraints as NEVER statements in their own rule files (NC-004: "NEVER spawn recursive subagents"). NEVER expressing P-003 as a positive observation when the entire enforcement architecture depends on this constraint being salient.

MUST NOT leave "NEVER hardcode values" as NPT-014 (E-002). The eng-team skill has multiple agents operating on security-critical code. The consequence of hardcoded values in this domain (credential exposure, testability failure) is specific and documentable.

MUST NOT leave the Constitutional Compliance table in positive framing. The eng-team skill governs 10 security-focused agents. NPT-013 (constitutional triplet as prohibitions) is directly applicable (E-014).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Upgrade "Agents cannot spawn nested agents" to NEVER-framed prohibition with consequence (P-003 violation, unauthorized delegation) | NPT-013 | T4 (VS-004, E-009 — unconditional per VS-003, E-008 HARD tier vocabulary) | REVERSIBLE if Phase 2 null at rank 9-11 | ADR-002 |
| Upgrade "NEVER hardcode values" to NPT-009 with security-specific consequence (credential exposure, testability failure) | NPT-009 | T1+T3 (PG-001, E-002 — unconditional) | NOT REVERSIBLE | ADR-001 |
| Upgrade Constitutional Compliance table to NPT-013 prohibition framing | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE | ADR-002 |

---

### Skill 6: nasa-se/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "DISCLAIMER: This guidance is AI-generated" | Header | Positive warning | None (informational) |
| "Agents cannot spawn nested agents" | P-003 section | Positive observation | Gap |
| Auto-Escalation rules (AE-001 through AE-006) | Multiple sections | Positive rule references | Positive |
| Constitutional Compliance | Positive descriptions | Positive | Positive |
| No "Do NOT use when:" section | Absent | Gap | Gap |

**Gap analysis:**

MUST NOT omit a routing disambiguation section. The nasa-se skill overlaps with /problem-solving on many keywords (architecture, design, risk). Without a "MUST NOT use when:" section documenting negative routing cases, the AP-02 (Bag of Triggers) anti-pattern applies — users and automated routing may invoke /nasa-se for root-cause analysis when /problem-solving is appropriate (E-016).

MUST NOT present the P-003 constraint as a positive observation when it is a constitutional prohibition (E-015). Same issue as eng-team.

MUST NOT leave the AI-generated disclaimer as an informal note. If the consequence of treating AI-generated requirements guidance as authoritative without review is important, it should be expressed as a constraint (MUST NOT treat as validated without human review).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Add "MUST NOT use when:" section with routing disambiguation | NPT-010 | T4 (routing anti-pattern evidence, E-016) | REVERSIBLE | ADR-003 |
| Upgrade P-003 statement to prohibition framing | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |
| Add constraint for AI-generated guidance limitation (MUST NOT treat as validated without human review) | NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |

---

### Skill 7: orchestration/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "Do NOT use when:" section | When-to-Use | Negation-paired alternative | Partial NPT-010 |
| "NEVER hardcode values" | Dynamic path context | Blunt prohibition | NPT-014 candidate |
| "transient output VIOLATES P-002" | Tool examples | Consequence documented | Partial NPT-009 |
| P-003 compliance section | Positive framing | Positive | Gap |
| "ESCALATE" paths described | Multiple sections | Positive | Positive |

**Gap analysis:**

MUST NOT treat "transient output VIOLATES P-002" as fully NPT-009 compliant. It documents a consequence but lacks (a) explicit scope of when this applies vs. does not apply and (b) the positive behavioral pairing (what to do instead of returning transient output). The current pattern is the closest to NPT-009 in the skill set and should be used as the internal template for other skills (E-010).

MUST NOT leave "NEVER hardcode values" as NPT-014 in the dynamic path context (E-002). The orchestration skill creates file paths as workflow state. The consequence of hardcoded paths (cross-session portability failure, workflow broken on environment change) is highly specific and should be documented.

MUST NOT leave "Do NOT use when:" without consequence documentation. The current section lists alternatives ("use /problem-solving for single-agent tasks") but does not document what fails when orchestration is misused for simple tasks (excessive coordination overhead, context pollution).

MUST NOT leave the P-003 compliance section in the ASCII diagram format without a NEVER-framed prohibition at the top. The diagram shows the hierarchy but does not express the prohibition as a constraint (E-015).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Upgrade "NEVER hardcode values" to NPT-009 with path portability consequence | NPT-009 | T1+T3 (PG-001, E-002 — unconditional) | NOT REVERSIBLE | ADR-001 |
| Complete "Do NOT use when:" with consequence documentation (overhead + context pollution) | NPT-010 | T4 (MEDIUM) | REVERSIBLE | ADR-003 |
| Add NEVER-framed P-003 prohibition as header to P-003 compliance section | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |
| Promote "transient output VIOLATES P-002" to a formal MUST NOT statement with full NPT-009 structure | NPT-009 | T4 (MEDIUM, consequence already present) | REVERSIBLE if Phase 2 null | ADR-002 |

---

### Skill 8: problem-solving/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "NEVER hardcode values" | Tool examples | Blunt prohibition | NPT-014 candidate |
| "transient output VIOLATES P-002" | Tool examples | Consequence documented | Partial NPT-009 |
| "ACCEPT_WITH_CAVEATS or escalate" | Circuit breaker | Positive | Positive |
| Constitutional Compliance | Positive descriptions | Positive | Positive |
| No "Do NOT use when:" | Absent | Gap | Gap |

**Gap analysis:**

MUST NOT leave the problem-solving skill without routing disambiguation (E-016). This is the broadest-scope skill in the framework with the highest collision risk with /orchestration, /adversary, and /nasa-se. NEVER leaving routing boundaries implicit in the highest-volume skill.

MUST NOT leave "NEVER hardcode values" as NPT-014 (E-002). Same unconditional issue as all other instances (PG-001 T1+T3 HIGH unconditional).

MUST NOT express the circuit breaker constraint in purely positive terms. "ACCEPT_WITH_CAVEATS or escalate" is a routing decision, not a behavioral prohibition. The negative version (MUST NOT proceed with insufficient evidence — specify what insufficient evidence means and what the consequence of proceeding is) would be NPT-009 compliant.

MUST NOT leave Constitutional Compliance in positive framing (E-015). Same issue as other skills — P-003/P-020/P-022 should be expressed as prohibitions per VS-004 (E-009).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Add "MUST NOT use when:" routing disambiguation section | NPT-010 | T4 (routing anti-pattern evidence, E-016) | REVERSIBLE | ADR-003 |
| Upgrade "NEVER hardcode values" to NPT-009 | NPT-009 | T1+T3 (PG-001, E-002 — unconditional) | NOT REVERSIBLE | ADR-001 |
| Express circuit breaker constraint as MUST NOT proceed with insufficient evidence with consequence | NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |
| Upgrade Constitutional Compliance to NPT-013 prohibition framing | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |

---

### Skill 9: red-team/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "Do NOT use when:" section | When-to-Use | Negation-paired alternative | Partial NPT-010 |
| "What This Skill Is NOT" section | Purpose | Scoped negation list | Partial NPT-008 |
| Authorization HALT on scope violation | Without Authorization section | Consequence documented | Partial NPT-009 |
| "Agents CANNOT invoke other agents" | P-003 section | Positive observation | Gap |
| Constitutional Compliance | Positive descriptions | Positive | Positive |
| "red-lead MUST establish scope first (MANDATORY)" | Orchestration Rules | Strong MUST | Partial NPT-009 |

**Gap analysis:**

MUST NOT treat "What This Skill Is NOT" as equivalent to NPT-009. The section lists 5 non-capabilities in positive framing ("does NOT execute exploits") but does not document consequences of attempting to use the skill for these excluded purposes. These are the most important boundary conditions in a security-testing skill.

MUST NOT treat the authorization HALT mechanism as fully NPT-009 compliant without examining whether the consequence chain is complete. The "AUTHORIZATION REQUIRED" halt message documents the consequence (halt + message + route to red-lead) but the SKILL.md description of this mechanism uses positive process language ("the orchestrator routes to red-lead") rather than NEVER-framed prohibition.

MUST NOT leave "Agents CANNOT invoke other agents" as a positive observation (E-015). The red-team skill operates in a security context where unauthorized agent delegation could have real consequences. The P-003 constraint should be expressed as a NEVER statement with consequence per VS-004 (E-009) and NPT-013 (E-014).

MUST NOT leave the "Do NOT use when:" section without consequence documentation. The alternatives are provided (redirects to /eng-team, /adversary, /problem-solving) but no consequence for misuse.

The red-team skill has the most developed negative constraint structure of any skill in the set — but the most important constraints (authorization model, P-003) are expressed in positive or partial-NPT form.

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Upgrade "What This Skill Is NOT" to NPT-009 with consequence per item | NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |
| Upgrade authorization HALT to explicit NEVER framing ("NEVER invoke operational agents without active scope document — consequence: immediate halt and AUTHORIZATION REQUIRED response") | NPT-009 | T4 (VS-003, E-008 HARD tier vocabulary) | REVERSIBLE if Phase 2 null | ADR-002 |
| Upgrade "Agents CANNOT invoke other agents" to NPT-013 prohibition | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |
| Add consequence documentation to "Do NOT use when:" | NPT-010 | T4 (MEDIUM) | REVERSIBLE | ADR-003 |

---

### Skill 10: saucer-boy/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "Do NOT use when:" section | When-to-Use | Negation-paired alternative | Partial NPT-010 |
| "Anti-Patterns" section | Full section | Scoped negation with labels | NPT-008 (structured) |
| "Boundary Conditions" section | Full section | Context-gated constraint | NPT-011 (partial) |
| Constitutional Compliance | Positive descriptions | Positive | Positive |
| "Agent CANNOT invoke other agents" | P-003 section | Positive observation | Gap |

**Gap analysis:**

MUST NOT omit recognition that the saucer-boy skill has the most developed negative constraint structure in the skill set for its specific domain. The Anti-Patterns section is a well-structured NPT-008 implementation (labeled anti-patterns with signal descriptions). The Boundary Conditions section partially implements NPT-011 (context-dependent gating).

MUST NOT treat the Anti-Patterns section as fully NPT-009 compliant. The patterns are labeled and described but lack formal consequence documentation (what fails in the system if "Sycophancy" or "Information Displacement" occurs, beyond the implicit quality degradation).

MUST NOT leave "Agent CANNOT invoke other agents" as a positive observation (E-015). Same P-003 issue as other skills.

MUST NOT treat "Do NOT use when:" without consequence documentation. The alternatives redirect to /saucer-boy-framework-voice and other skills, but no consequence for misuse is documented.

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Add consequence documentation to Anti-Patterns (what system outcome fails per anti-pattern) | NPT-008 upgrade to NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |
| Add consequence to "Do NOT use when:" | NPT-010 | T4 (MEDIUM) | REVERSIBLE | ADR-003 |
| Upgrade P-003 statement to prohibition framing | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |

---

### Skill 11: saucer-boy-framework-voice/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "Do NOT use when:" section | When-to-Use | Negation-paired alternative | Partial NPT-010 |
| "Boundary Conditions" section (8 items) | Full section | Structured scoped negation | NPT-008 (strong) |
| "NOT Sarcastic", "NOT Dismissive", etc. | Boundary table | Labeled prohibitions | NPT-008 |
| "Agents CANNOT invoke other agents" | P-003 section | Positive observation | Gap |
| Constitutional Compliance | Absent (embedded in purpose text) | Partial | Gap |
| Authenticity Test 1 | HARD gate | Strong prohibition (stop on fail) | NPT-007 (partial) |

**Gap analysis:**

MUST NOT omit recognition that the saucer-boy-framework-voice skill has the second most developed negative constraint structure, specifically in the Boundary Conditions section. The 8 boundary conditions ("NOT Sarcastic", "NOT Dismissive of Rigor", etc.) implement NPT-008 (labeled anti-patterns). Authenticity Test 1 is a HARD gate that implements a stop-on-fail prohibition — partial NPT-007 structure.

MUST NOT treat the Boundary Conditions section as fully NPT-009 because the consequence documentation for each boundary is externalized to `boundary-conditions.md` reference files rather than being visible in the SKILL.md. This creates a progressive-disclosure design choice (Tier 3 loading) — but consequence accessibility in the primary SKILL.md body is lower than optimal.

MUST NOT leave P-003 as a positive observation (E-015).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Add inline consequence summary to each Boundary Condition row (consequences are in external files — surface the critical ones inline) | NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |
| Upgrade P-003 statement to prohibition framing | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |
| Add consequence to "Do NOT use when:" | NPT-010 | T4 (MEDIUM) | REVERSIBLE | ADR-003 |

---

### Skill 12: transcript/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "DO NOT use Task agents for parsing" | CLI Invocation section | Strong prohibition | NPT-009 (partial — consequence present: 1,250x cost increase) |
| "DO NOT read into context" (canonical-transcript.json) | Expected output section | Strong prohibition with consequence | NPT-009 (strong) |
| "CRITICAL: Always quote file paths" | Invocation rules | Strong imperative | Positive MUST (not NEVER-framed) |
| No "Do NOT use when:" section | Absent | Gap | Gap |
| No Constitutional Compliance section | Absent | Gap | Gap |

**Gap analysis:**

MUST NOT overlook that the transcript skill has the strongest NPT-009 instances in the skill set (E-010, E-011). "DO NOT read into context" for `canonical-transcript.json` is the clearest NEVER-framed prohibition with consequence (context window exhaustion) in any skill file. "DO NOT use Task agents for parsing" includes the consequence (1,250x cost increase). These should be treated as internal exemplars.

MUST NOT leave "CRITICAL: Always quote file paths" in positive imperative framing. The negative version (MUST NOT omit quotes around file paths — consequence: paths with spaces will fail silently) would be more salient and NPT-009 compliant (E-002).

MUST NOT omit a routing disambiguation section. The transcript skill has very specific domain applicability (VTT/SRT/text transcript files) but the current skill lacks explicit "MUST NOT use when:" conditions (E-016).

MUST NOT omit a Constitutional Compliance section. The transcript skill uses Task tool (ts-parser as orchestrator) and Memory-Keeper MCP. P-003 compliance documentation is absent (E-015).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Promote "DO NOT use Task agents for parsing" and "DO NOT read canonical-transcript.json into context" as model NPT-009 exemplars (already compliant, no change needed — mark as reference) | NPT-009 | Already compliant (E-010, E-011) | N/A | ADR-004 |
| Upgrade "CRITICAL: Always quote file paths" to MUST NOT framing with consequence | NPT-009 | T1+T3 (PG-001, E-002 — blunt prohibition inferior) | NOT REVERSIBLE | ADR-001 |
| Add "MUST NOT use when:" section | NPT-010 | T4 (MEDIUM, E-016) | REVERSIBLE | ADR-003 |
| Add Constitutional Compliance section with NPT-013 prohibition framing | NPT-013 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |

---

### Skill 13: worktracker/SKILL.md

**Current negative constraint usage:**

| Instance | Location | Pattern Type | NPT Classification |
|----------|----------|--------------|-------------------|
| "Agents DO NOT spawn subagents" | P-003 section | Strong negative | Partial NPT-009 |
| "Agents never invoke other agents" | P-003 diagram | Strong negative | Partial NPT-009 |
| No "Do NOT use when:" section | Absent | Gap | Gap |
| No NEVER/MUST NOT in main body | Throughout | Positive framing | Gap |
| WTI rules reference (enforcement via agents) | Rule enforcement section | Indirect | Indirect NPT |

**Gap analysis:**

MUST NOT treat "Agents DO NOT spawn subagents" as fully NPT-009. The statement is a strong prohibition but lacks consequence documentation (what breaks if an agent spawns a subagent — unauthorized delegation, P-003 violation, context hierarchy corruption) (E-015).

MUST NOT leave the WTI-001 through WTI-009 rules without negative constraint framing in the SKILL.md summary. These rules govern worktracker integrity — the most critical data integrity rules in the framework. The summary table lists rule names but does not provide any NEVER/MUST NOT framing for the most critical violations.

MUST NOT omit a "MUST NOT use when:" section. The worktracker skill is invoked for all work item operations, but there are cases where it should NOT be invoked (e.g., when the jerry items CLI covers the need without agent invocation) (E-016).

**NPT pattern recommendations:**

| Recommendation | NPT Pattern | Confidence | Reversibility | ADR Input |
|----------------|-------------|------------|---------------|-----------|
| Add consequence to P-003 prohibition (unauthorized delegation, context hierarchy violation) | NPT-009 | T4 (VS-004, E-009) | REVERSIBLE if Phase 2 null | ADR-002 |
| Surface WTI-002 (No Closure Without Verification) and WTI-003 (Truthful State) as NEVER-framed constraints in the SKILL.md summary | NPT-009 | T4 (MEDIUM) | REVERSIBLE | ADR-002 |
| Add "MUST NOT use when:" routing disambiguation | NPT-010 | T4 (MEDIUM, E-016) | REVERSIBLE | ADR-003 |

---

## Cross-Skill Patterns

### Pattern CX-001: Universal Blunt Prohibition (NPT-014) — "NEVER hardcode values"

**Evidence:** Appears verbatim or in close variants in adversary, eng-team, orchestration, and problem-solving skills.

**Analysis:** MUST NOT treat this as four independent instances. This is a single constraint propagated without adaptation across four skills. The consequence varies by domain (path portability failure in orchestration, credential exposure in eng-team, untestable behavior in problem-solving) but the prohibition text does not vary. This is precisely the NPT-014 diagnostic pattern — blunt prohibition without specificity.

**Recommendation:** MUST NOT leave any instance as NPT-014. Each domain requires a domain-specific NPT-009 upgrade with the appropriate consequence documentation (per PG-001, E-002). MUST NOT write a generic cross-skill upgrade — each instance needs domain-specific consequence text.

**Reversibility:** NOT REVERSIBLE. PG-001 is T1+T3 HIGH unconditional: blunt prohibition is always inferior to structured negative constraint with consequence.

### Pattern CX-002: Universal P-003 Positive Observation

**Evidence:** All 13 skills express P-003 in positive form ("Agents are workers, NOT orchestrators," "Agents CANNOT invoke other agents," "Agents cannot spawn nested agents"). None use NEVER-framed prohibition with consequence (E-015).

**Analysis:** MUST NOT dismiss this as stylistic. VS-003 (E-008) documents that the HARD tier in Jerry's enforcement architecture is explicitly defined by prohibitive vocabulary (MUST/NEVER/SHALL). P-003 is the most critical constitutional prohibition. Expressing it as a positive observation rather than a NEVER-framed prohibition creates an inconsistency between the rule files (which use NEVER framing) and the skill files (which use positive observation).

**Recommendation:** MUST NOT leave P-003 expressed as positive observation in any skill when NPT-013 (constitutional triplet as prohibitions) is directly applicable. All 13 skills should express P-003 as: "NEVER spawn subagents — agents are workers only, and unauthorized delegation violates P-003 (no recursive subagents)."

**Reversibility:** REVERSIBLE if Phase 2 finds null framing effect at ranks 9-11. The consequence documentation is unconditional; the NEVER framing vocabulary is the contingent element.

### Pattern CX-003: "Do NOT use when:" Without Consequence Documentation

**Evidence:** Adversary, ast, orchestration, red-team, saucer-boy, saucer-boy-framework-voice all have "Do NOT use when:" sections that provide positive alternatives but no consequence for misuse.

**Analysis:** MUST NOT treat provision of alternatives as equivalent to consequence documentation. NPT-010 (negation-paired alternative) is a higher-effectiveness pattern than NPT-014 (blunt prohibition) precisely because it provides the alternative. But the full effectiveness benefit of NPT-009 (declarative behavioral negation) requires consequence documentation — what goes wrong if the constraint is violated?

**Recommendation:** MUST NOT add consequence documentation generically. Each skill's "Do NOT use when:" items have specific domain consequences (routing overhead in orchestration, context pollution in problem-solving, methodology confusion in nasa-se). Consequences must be skill-specific.

**Reversibility:** REVERSIBLE. Consequence documentation is independent of framing vocabulary choice — it remains valuable regardless of Phase 2 framing effect findings.

### Pattern CX-004: Constitutional Compliance Tables — Positive Framing Uniformity

**Evidence:** Every skill with a Constitutional Compliance table (adversary, eng-team, nasa-se, orchestration, problem-solving, red-team, saucer-boy, worktracker) uses positive framing exclusively. None use NPT-013 prohibition framing for P-003/P-020/P-022.

**Analysis:** MUST NOT treat this uniformity as validation. VS-004 (E-009) documents that Anthropic expresses constitutional constraints as prohibitions in their own rule files (33 NEVER/MUST NOT instances including the constitutional triplet). The current positive framing in skill Constitutional Compliance tables diverges from both vendor practice (VS-004) and the HARD tier vocabulary definition (VS-003, E-008).

**However:** MUST NOT present NPT-013 as experimentally validated. VS-004 documents three competing explanations for vendor use of prohibitive vocabulary (VS-002, E-007) (audience differentiation, genre convention, engineering discovery). The causal explanation is UNTESTED at T4 confidence.

**Recommendation:** MUST NOT upgrade Constitutional Compliance tables to NPT-013 framing until Phase 2 results are available for ranks 9-11, because this is a medium-confidence (T4) contingent recommendation. However, MUST NOT leave blunt prohibition instances (P-003 stated without consequence) as-is if they coincide with NPT-014 diagnostic criteria.

**Reversibility:** REVERSIBLE. Constitutional Compliance table framing is a vocabulary choice independent of constitutional principle content.

### Pattern CX-005: Transcript Skill as Internal NPT-009 Exemplar

**Evidence:** The transcript skill contains the strongest NPT-009 instances in the framework: "DO NOT use Task agents for parsing" (consequence: 1,250x cost increase, E-011) and "DO NOT read canonical-transcript.json into context" (consequence: context window exhaustion, E-010).

**Analysis:** MUST NOT treat these as isolated instances. They represent the target pattern for NPT-009 upgrades across the skill set. When upgrading other skills, the transcript skill's format should be used as the internal reference.

**Pattern template extracted:**
```
MUST NOT [specific prohibited action] — [specific technical consequence]
```

Example from transcript: "DO NOT read [file] into context — [consequence: file content (930KB) would exhaust context window]"

**Recommendation:** MUST NOT implement NPT-009 upgrades across skills without first reviewing the transcript skill exemplars to ensure consistency of format.

### Pattern CX-006: Missing Routing Disambiguation (Absent "MUST NOT use when:")

**Evidence:** Bootstrap, nasa-se, problem-solving, transcript, and worktracker skills lack any "Do NOT use when:" or "MUST NOT use when:" section (E-016).

**Analysis:** MUST NOT treat absence of routing disambiguation as acceptable for high-collision skills. The routing standards (agent-routing-standards.md) document AP-01 (Keyword Tunnel) and AP-02 (Bag of Triggers) as documented anti-patterns. The problem-solving and nasa-se skills have the highest keyword collision risk and the most need for routing disambiguation.

**Recommendation:** MUST NOT add generic routing disambiguation. Each skill's routing exclusions must be grounded in the actual keyword overlap documented in the trigger map (mandatory-skill-usage.md). Routing disambiguation sections must be consistent with the 5-column trigger map format.

**Reversibility:** REVERSIBLE. Routing disambiguation is independent of negative prompting framing vocabulary.

---

## Evidence Gap Map

This map documents where evidence for recommendations is strong (unconditional) vs. contingent (Phase 2 dependent).

| Recommendation Category | Evidence Tier | Confidence | Phase 2 Dependency | Unconditional? |
|------------------------|---------------|------------|-------------------|----------------|
| Upgrade NPT-014 blunt prohibitions to NPT-009 | T1+T3 | HIGH | NONE | YES (PG-001, E-002) |
| Add consequence documentation to "Do NOT use when:" sections | T4 | MEDIUM | NONE (consequences are factual regardless of framing effect) | YES |
| Upgrade Constitutional Compliance tables to NPT-013 | T4 (VS-004, E-009) | MEDIUM | YES (Phase 2 null at ranks 9-11) | NO (contingent) |
| Upgrade P-003 positive observations to NEVER-framed prohibition | T4 (VS-004/VS-003, E-008/E-009) | MEDIUM | YES | NO (contingent) |
| Add routing disambiguation "MUST NOT use when:" sections | T4 | MEDIUM | NONE (routing correctness is independent of framing) | YES |
| Surface H-05 prohibition in bootstrap SKILL.md | T1+T3 | HIGH | NONE | YES (PG-001, E-002) |
| Promote transcript skill NPT-009 instances as internal exemplars | T4 | HIGH (mechanically verified) | NONE | YES (E-010, E-011) |

### Evidence Quality Assessment

MUST NOT conflate T4 vendor self-practice evidence (VS-001 through VS-004) with T1 peer-reviewed evidence. The following caution applies to all T4 recommendations:

The three competing explanations for Anthropic's 33-instance NEVER/MUST NOT practice (VS-002, E-007) remain unresolved:
1. **Audience differentiation:** Rule files are written for compliance, not explanation — prohibitive vocabulary fits the genre
2. **Genre convention:** The HARD/MEDIUM/SOFT tier vocabulary schema makes prohibitive vocabulary structurally required for the HARD tier
3. **Engineering discovery:** Prohibitive vocabulary was found empirically to produce better compliance

Only explanation 3 (engineering discovery) supports the claim that vocabulary choice affects LLM behavior. Explanations 1 and 2 support convention-determined adoption. MUST NOT present VS-004 as evidence that NEVER framing produces better LLM compliance than positive framing in skill files — that causal claim is UNTESTED.

---

## PG-003 Contingency Plan

PG-003 states (T4, MEDIUM working practice): "pair enforcement-tier constraints with consequence statements." PG-003 contingency: if Phase 2 finds null framing effect at ranks 9-11 of the hierarchy, recommendations based on NPT-009/NPT-010/NPT-011 framing vocabulary become convention-determined, not effectiveness-determined.

### Reversibility Classification

| Recommendation Type | Reversible? | Reversal Action |
|---------------------|-------------|-----------------|
| NPT-014 → NPT-009 upgrades (blunt prohibition elimination) | NOT REVERSIBLE | PG-001 (E-002) is unconditional T1+T3 HIGH — blunt prohibition is always inferior; consequence documentation is valuable regardless of vocabulary |
| NPT-013 (Constitutional Compliance prohibition framing) | REVERSIBLE | Revert prohibition framing to positive description — content unchanged |
| "MUST NOT use when:" routing disambiguation sections | REVERSIBLE but retain consequence documentation | Remove MUST NOT framing, retain positive alternative + consequence text |
| P-003 positive observation upgrades | REVERSIBLE | Revert to positive observation framing — constraint content unchanged |
| Transcript skill exemplar promotion | NOT REVERSIBLE | Already best practice regardless of Phase 2 results (E-010, E-011) |

### PG-003 Null Result Implementation Protocol

IF Phase 2 experiment finds null framing effect at ranks 9-11 (the hierarchy positions occupied by NPT-009 declarative behavioral negation and NPT-010 negation-paired alternative):

1. MUST NOT revert consequence documentation. Consequence documentation is independently valuable for clarity regardless of whether NEVER/MUST NOT vocabulary affects LLM compliance.
2. MUST NOT revert NPT-014 upgrades. Blunt prohibition elimination is unconditional per PG-001 (E-002) (T1+T3 HIGH).
3. MUST retain vocabulary updates that reflect HARD tier definition. The HARD/MEDIUM/SOFT tier vocabulary schema (VS-003, E-008) uses MUST/NEVER/SHALL to define the HARD tier — this is a definitional requirement, not an effectiveness claim.
4. SHOULD revert purely stylistic NEVER/MUST NOT additions that were not motivated by blunt prohibition elimination or tier vocabulary definition.

### Phase 2 Experimental Condition Preservation

MUST NOT implement any skill update that makes the C1-C7 experimental conditions unreproducible:
- C2 (blunt prohibition): All "NEVER hardcode values" NPT-014 instances in SKILL.md files are **outside** the C1-C7 experimental scope (which tests rule file constraints, not skill routing guidance). NPT-014 upgrades in SKILL.md files MUST NOT affect rule file constraints used in Phase 2.
- C6 (hierarchical HARD/MEDIUM/SOFT): The HARD/MEDIUM/SOFT tier vocabulary in `.context/rules/` files is the experimental material. SKILL.md file updates are downstream applications and do not affect experimental conditions.
- All skill updates should be implemented in a separate commit branch tagged as Phase 4 application — NOT in the same commit as any rule file changes.

---

## Phase 5 Downstream Inputs

The following findings should be provided as structured inputs to the Phase 5 architect (ADR production) and the implementation planner:

### For ADR-001: Unconditional Updates (NPT-014 → NPT-009)

**Finding:** 4 skills contain "NEVER hardcode values" as blunt prohibition (NPT-014). PG-001 (E-002) (T1+T3 HIGH unconditional) requires these be upgraded to NPT-009 with domain-specific consequence documentation. 1 additional unconditional instance: transcript "CRITICAL: Always quote file paths" (blunt positive imperative functionally equivalent to NPT-014).

**Recommended ADR decision:** Adopt domain-specific NPT-009 templates for the 4 NPT-014 instances plus 1 transcript upgrade. Implementation is unconditional and does not require Phase 2 results.

**Implementation inputs:**
- adversary: consequence = "hardcoded strategy IDs prevent dynamic C4 strategy selection"
- eng-team: consequence = "hardcoded credential or path values expose secrets and break test isolation"
- orchestration: consequence = "hardcoded workflow paths break cross-session portability"
- problem-solving: consequence = "hardcoded PS IDs prevent reuse across projects"
- transcript (Always quote file paths): consequence = "unquoted paths with spaces fail silently"

### For ADR-002: Contingent Updates (NPT-013 Constitutional Prohibition Framing)

**Finding:** All 13 skills express P-003/P-020/P-022 in positive framing. VS-004 (E-009) (T4) shows Anthropic uses prohibition framing for constitutional constraints in rule files. Causal evidence is UNTESTED.

**Recommended ADR decision:** This is a convention decision, not a validated effectiveness decision. The ADR should document the three competing explanations (VS-002, E-007) and make a convention choice based on HARD tier vocabulary definition consistency.

**Phase 2 dependency:** If Phase 2 confirms framing effect at ranks 9-11, the ADR recommendation upgrades from convention to effectiveness-grounded. Implement as reversible change.

### For ADR-003: Routing Disambiguation (NPT-010 MUST NOT Use When)

**Finding:** 5 skills lack routing disambiguation. 6 skills have partial NPT-010 (alternatives without consequences).

**Enumeration of the 11 items:**
- Skills fully missing routing disambiguation (5): bootstrap, nasa-se, problem-solving, transcript, worktracker
- Skills with partial NPT-010 requiring consequence additions (6): adversary, ast, orchestration, red-team, saucer-boy, saucer-boy-framework-voice

**Recommended ADR decision:** All 13 skills should have "MUST NOT use when:" sections. 11 gaps to fill (two skills — adversary and red-team — have substantive sections that need consequence additions only; architecture also lacks a section and is included in the 11 gap count above via the "partial" category).

**Implementation inputs:** See per-skill recommendations in L2 section above. Each routing disambiguation must be grounded in the trigger map collision analysis in `mandatory-skill-usage.md`.

### For ADR-004: Transcript Skill Exemplar Standardization

**Finding:** The transcript skill contains the framework's strongest NPT-009 instances (E-010, E-011). These should be codified as the internal standard template for NPT-009 upgrades across all skills.

**Recommended ADR decision:** Establish the transcript skill format as the canonical NPT-009 template: `MUST NOT [specific action] — [specific technical consequence with measurable indicator where available]`.

### Cross-Skill Observations for Phase 5 Risk Assessment

MUST NOT omit the following risk observations from the Phase 5 architecture decision:

1. **T-004 (Context compaction) risk:** NEVER rules in SKILL.md files are loaded at skill invocation (L1 layer), making them vulnerable to context compaction drop (T-004, T4 LOW confidence, irreversible risk, E-017). PG-004 (E-004) (unconditional by failure mode) requires testing constraint persistence through context compaction for any NEVER constraint added to skills. This testing requirement is unconditional because the failure mode consequence (constraint silently dropped) is irreversible in-session.

2. **SKILL.md length and L2 re-injection:** Transcript SKILL.md exceeds the 25,000 token read limit. Long SKILL.md files cannot be re-injected at L2. Any MUST NOT constraints added to long skill files should also be surfaced in a dedicated rule file accessible for L2 re-injection if they are HARD tier constraints (per VS-003, E-008).

3. **Convention vs. effectiveness differentiation:** MUST NOT implement Phase 5 ADRs without explicitly documenting which recommendations are effectiveness-grounded (T1+T3) and which are convention-grounded (T4). The ADR format requires this differentiation for governance traceability.

---

## Evidence Summary

| Evidence ID | Type | Source | Source File | Tier | Relevance |
|-------------|------|--------|-------------|------|-----------|
| E-001 | Pattern catalog | Phase 3 taxonomy-pattern-catalog.md | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md` | T4 (compiled) | Primary NPT pattern reference for all recommendations |
| E-002 | Guidance | PG-001 (unconditional, T1+T3 HIGH) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md` (section: Practitioner Guidance Under Evidence Uncertainty, PG-001) | T1+T3 | Basis for all NPT-014 → NPT-009 upgrades being unconditional |
| E-003 | Guidance | PG-003 (T4, MEDIUM, reversible at Phase 2 null) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md` (section: Practitioner Guidance Under Evidence Uncertainty, PG-003) | T4 | Basis for reversibility classifications |
| E-004 | Guidance | PG-004 (T4, unconditional by failure mode) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md` (section: Practitioner Guidance Under Evidence Uncertainty, PG-004) | T4 | Context compaction testing requirement |
| E-005 | Guidance | PG-005 (T3+T4, unconditional) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md` (section: Practitioner Guidance Under Evidence Uncertainty, PG-005) | T3+T4 | Enforcement architecture priority over framing optimization |
| E-006 | Vendor | VS-001 (33 NEVER/MUST NOT instances in Jerry rule files) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md` | T4 | Vendor self-practice baseline for negative constraint density |
| E-007 | Vendor | VS-002 (three competing explanations) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md` | T4 | Basis for causal uncertainty on constitutional prohibition framing |
| E-008 | Vendor | VS-003 (HARD tier defined by prohibitive vocabulary) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md` | T4 | Definitional requirement for NEVER/MUST NOT in HARD tier |
| E-009 | Vendor | VS-004 (constitutional triplet expressed as prohibitions in Anthropic rule files) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md` | T4 | Vendor practice basis for NPT-013 recommendation |
| E-010 | Internal observation | Transcript skill "DO NOT read canonical-transcript.json" | `skills/transcript/SKILL.md` (CLI Invocation section) | T4 (mechanically consequenced) | Internal NPT-009 exemplar |
| E-011 | Internal observation | Transcript skill "DO NOT use Task agents for parsing" with 1,250x cost consequence | `skills/transcript/SKILL.md` (CLI Invocation section) | T4 (measurable) | Internal NPT-009 exemplar with quantified consequence |
| E-012 | Cross-survey | AGREE-5 12-level hierarchy (internally generated) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-2/synthesis.md` (section: ST-1 Hierarchy Integration, AGREE-5 row) | T4 (internal synthesis) | Hierarchy ranks for NPT pattern positioning — MUST NOT treat as externally validated |
| E-013 | Rule file | VS-003 enforcement architecture (L1-L5 layers) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md` | T4 | SKILL.md files are L1 layer — vulnerable to context rot |
| E-014 | Analysis | NPT-013 schema (constitutional triplet) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md` (NPT-013 entry) | T4/schema | Mandatory 3-prohibition pattern for constitutional compliance |
| E-015 | Internal observation | CX-002 P-003 positive observation universality across 13 skills | This document, Cross-Skill Patterns section, Pattern CX-002 | T4 | Systemic gap requiring cross-skill remedy |
| E-016 | Internal observation | CX-006 missing routing disambiguation across 5 skills | This document, Cross-Skill Patterns section, Pattern CX-006 | T4 | Routing anti-pattern (AP-01, AP-02) risk |
| E-017 | Analysis | T-004 failure mode (context compaction drops NEVER rules) | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-2/synthesis.md` (section: ST-5 Phase 4 Inputs, T-004 risk item) | T4 LOW | Unconditional testing requirement per PG-004 |

---

## Orchestration Directive Compliance Check

Per Phase 4 non-negotiable constraints:

| Directive | Status |
|-----------|--------|
| MUST NOT use positive prompting framing — all recommendations as NEVER/MUST NOT | COMPLIANT — all 7 recommendation categories use NEVER/MUST NOT framing |
| MUST NOT omit supplemental vendor evidence | COMPLIANT — VS-001 through VS-004 cited in every cross-skill pattern and evidence summary |
| MUST NOT dismiss practitioner/vendor evidence as inferior | COMPLIANT — T4 evidence labeled as T4, not dismissed; three competing explanations for VS-002 preserved |
| MUST NOT treat absence of evidence as evidence of absence | COMPLIANT — absent evidence for positive framing equivalence is acknowledged, not used to dismiss NPT patterns |
| MUST NOT present enforcement tier vocabulary as experimentally validated | COMPLIANT — VS-002 three competing explanations explicitly preserved; causal claim noted as UNTESTED throughout |
| MUST NOT recommend changes making Phase 2 conditions unreproducible | COMPLIANT — Phase 2 experimental condition preservation section explicitly documents separation requirement |
| MUST NOT ignore PG-003 contingency | COMPLIANT — reversibility classification provided for every recommendation category; null result implementation protocol documented |

---

*Agent: ps-analyst*
*Task: TASK-010*
*Workflow: neg-prompting-20260227-001*
*Phase: Phase 4 — Jerry Skills Update Analysis*
*Version: 2.0.0 (I1 revision — 7 adversary gaps addressed)*
*Created: 2026-02-28*
*Constitutional Compliance: Jerry Constitution v1.0*

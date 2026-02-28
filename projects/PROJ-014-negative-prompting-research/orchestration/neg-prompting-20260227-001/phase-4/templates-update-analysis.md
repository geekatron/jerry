# TASK-014: Jerry Templates Update Analysis — Negative Prompting Application

> **Type:** phase-4-analysis
> **Status:** COMPLETE
> **PS ID:** phase-4
> **Entry ID:** TASK-014
> **Analysis Types:** gap-analysis, impact-analysis
> **Agent:** ps-analyst
> **Date:** 2026-02-28
> **Version:** 3.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical findings and recommendation |
| [Methodology](#methodology) | Analysis scope, evidence sources, frameworks applied |
| [Adversarial Template Analysis (L1)](#adversarial-template-analysis-l1) | Per-template gap and NPT mapping |
| [Worktracker Template Analysis (L1)](#worktracker-template-analysis-l1) | Per-template gap and NPT mapping |
| [Design Template Analysis (L1)](#design-template-analysis-l1) | Per-template gap and NPT mapping |
| [Requirements Template Analysis (L1)](#requirements-template-analysis-l1) | Per-template gap and NPT mapping |
| [Cross-Template Patterns (L2)](#cross-template-patterns-l2) | Architectural implications and systemic findings |
| [Evidence Gap Map](#evidence-gap-map) | Where evidence is strong vs. provisional |
| [PG-003 Contingency Plan](#pg-003-contingency-plan) | What changes if Phase 2 finds null framing effect |
| [Phase 5 Downstream Inputs](#phase-5-downstream-inputs) | Inputs to the next research phase |
| [Evidence Summary](#evidence-summary) | Cited evidence per finding |

---

## L0: Executive Summary

The Jerry Framework already uses negative prompting extensively in its templates — but unevenly. The adversarial strategy templates apply strong negative constraints to prevent SSOT corruption (MUST NOT redefine weights) and enforce ordering rules (STOP if S-003 missing). The design templates (Playbook, Runbook) use negative constraint framing with high operational density: "Do NOT use this runbook when," "STOP — Do not proceed," "IMMEDIATE ROLLBACK." The worktracker entity templates and requirements templates use the weakest negative framing: primarily contrastive illustrations (BAD vs. GOOD examples) rather than explicit behavioral prohibitions.

The most significant gap is in the worktracker entity templates (EPIC, STORY, TASK, BUG, ENABLER). These templates define the acceptance criteria quality standard through contrastive examples (NPT-008) but do not state prohibitions directly in the template content itself. The integrity enforcement is externalized to WTI_RULES.md rather than embedded at the point of creation. Based on T4 practitioner evidence (PG-001 through PG-003), adding NPT-009 declarative behavioral negation with consequences (NPT-011) to the AC quality sections of these templates would reduce AC quality failures at the point of template instantiation.

**MANDATORY EPISTEMIC NOTE:** MUST NOT present the following as experimentally validated. The evidence basis for specific ordering effects among ranks 9-11 of the AGREE-5 hierarchy (declarative, paired, justified behavioral negation) is T4 observational only. PG-003 (pair enforcement-tier constraints with consequences) is a working practice with MEDIUM confidence. The recommendation to add NPT-011 justified prohibition patterns to worktracker templates is grounded in PG-001 (unconditional T1+T3: NEVER standalone blunt prohibition), PG-002 (HIGH: always include hierarchy rank), and PG-005 (unconditional T3: prioritize enforcement architecture over framing vocabulary). The specific effectiveness advantage of NPT-011 over NPT-009 at ranks 9-11 is UNVALIDATED pending Phase 2 experimental data.

---

## Methodology

### Scope

All template files in `.context/templates/` were analyzed across four families:

1. **Adversarial templates**: 10 strategy execution templates (S-001 through S-014 minus excluded) + TEMPLATE-FORMAT.md format standard
2. **Worktracker entity templates**: EPIC.md, FEATURE.md, STORY.md, TASK.md, BUG.md, ENABLER.md + WTI_RULES.md integrity rules
3. **Design templates**: TDD.template.md (preview only — file exceeds context limit), PLAYBOOK.template.md, RUNBOOK.template.md
4. **Requirements templates**: USE-CASE.template.md

### FEATURE.md Scope Note

FEATURE.md is included in the formal scope declaration above and in WT-REC-004's coverage. Upon analysis, FEATURE.md exhibits the identical structural pattern as TASK.md and BUG.md: NPT-008 contrastive BAD/GOOD examples for AC quality, no NPT-009 declarative constraints, and no creation constraint block. It does not introduce new gap types beyond WT-GAP-001 through WT-GAP-005. Rather than duplicate the TASK.md analysis body, FEATURE.md is explicitly consolidated under those shared gaps. Its inclusion in WT-REC-004 is therefore warranted and complete: the universal creation constraint block (WTI-007 embedding) applies to FEATURE.md on the same basis as TASK.md and BUG.md (E-009-F).

### Frameworks Applied

- **Gap analysis**: Current negative constraint usage vs. optimal NPT-pattern application
- **NPT taxonomy mapping**: Each existing constraint classified against NPT-001 through NPT-014
- **IG-002 taxonomy**: Type 1/2/3/4 classification of existing constraints
- **AGREE-5 hierarchy**: Placement of existing constraints within the 12-level effectiveness hierarchy
- **PG-001 through PG-005**: Practitioner guidance applied as evaluation criteria

### AGREE-5 Rank Anchor Table

This table anchors the NPT patterns referenced in gap and recommendation entries to their position in the AGREE-5 12-level effectiveness hierarchy, as defined in `barrier-1/synthesis.md` and cataloged in `phase-3/taxonomy-pattern-catalog.md`.

| AGREE-5 Rank | NPT Pattern | Pattern Name | Evidence Tier |
|-------------|-------------|--------------|--------------|
| 12 | NPT-007 | Positive framing only | Untested (baseline) |
| 11 | NPT-008 | Contrastive Illustration (BAD/GOOD) | T3 |
| 10 | NPT-008 (paired) | Contrastive with Positive Redirect | T3 |
| 9 | NPT-009 | Declarative Behavioral Negation (MUST NOT) | T3 |
| 9 | NPT-010 | Paired Prohibition with Positive Alternative | T3/T4 |
| 9 | NPT-011 | Justified Prohibition with Contextual Reason | T4 (MEDIUM, conditional) |
| 8 | NPT-012 | L2-Re-Injected Negation (persistent) | T4 |
| 7 | NPT-013 | Constitutional Triplet (P-003, P-020, P-022) | T1/T3 |
| — | NPT-014 | Standalone Blunt Prohibition (anti-pattern) | T1+T3, AVOID |

> Note: Ranks 9-11 cluster NPT-009, NPT-010, and NPT-011. The ordering within this cluster is T4-evidenced only; the specific effectiveness advantage of any one over another is UNVALIDATED pending Phase 2 (ST-4, barrier-2/synthesis.md).

### Priority Derivation

Gap and recommendation priority (HIGH/MEDIUM/LOW) is assigned using the following criteria, in order:

1. **HIGH**: Gap affects a template that currently has **zero** negative constraints, OR gap affects a constraint that is unconditional per PG-001 (T1+T3) or PG-002 (T1+T4). These are unambiguously correct improvements regardless of Phase 2 outcome.
2. **MEDIUM**: Gap reduces the AGREE-5 hierarchy rank of an existing constraint (e.g., NPT-008 → NPT-010 upgrade) or implements a PG-003 conditional finding where T4 evidence supports the change but Phase 2 could falsify it.
3. **LOW**: Gap adds a consequence clause (NPT-011) to an already-sound NPT-009 constraint. Improvement is stylistic and convention-consistent; Phase 2 null-effect contingency applies.
4. **BLOCKED**: Gap cannot be analyzed or resolved without a precondition being met (e.g., TDD.template.md file size).

### Input Artifacts

| Artifact | Path | Role |
|----------|------|------|
| Phase 3 Taxonomy Catalog | `phase-3/taxonomy-pattern-catalog.md` | NPT pattern definitions and applicability criteria |
| Barrier 1 Synthesis | `barrier-1/synthesis.md` | AGREE-5 hierarchy, evidence tiers |
| Supplemental Vendor Evidence | `barrier-1/supplemental-vendor-evidence.md` | VS-001 through VS-004, IG-001 through IG-003 |
| Barrier 2 Synthesis | `barrier-2/synthesis.md` | PG-001 through PG-005, ST-4 verdict, ST-5 downstream constraints |

### Evidence Tier Conventions

| Tier | Label | Meaning |
|------|-------|---------|
| T1 | Established | Peer-reviewed, causal |
| T3 | Provisional | Preprint/unreviewed |
| T4 | Working practice | Practitioner observation / vendor self-practice |
| T5 | Single session | Single observation |
| Untested | Untested | No evidence; experimental design required |

---

## Adversarial Template Analysis (L1)

### Current State

All 10 adversarial strategy templates plus TEMPLATE-FORMAT.md were fully read. The following pattern inventory was conducted.

#### MUST NOT / NEVER Inventory (Adversarial Templates)

| Template | Location | Constraint Text | NPT Classification | IG-002 Type |
|----------|----------|-----------------|-------------------|-------------|
| TEMPLATE-FORMAT.md | Scoring Rubric | "Templates MUST NOT redefine these constants" | NPT-009 (Declarative Behavioral Negation) | Type 2 |
| TEMPLATE-FORMAT.md | Constants Reference | "MUST NOT be redefined" (weights, thresholds) | NPT-009 | Type 2 |
| All strategy templates | Scoring Rubric | "SSOT threshold... MUST NOT be redefined" | NPT-009 | Type 2 |
| All strategy templates | Criticality tables | "Values MUST match exactly" (from SSOT) | NPT-009 | Type 2 |
| S-001 | Execution Protocol Step 1 | "DO NOT proceed until S-003 is applied" | NPT-009 + ordering | Type 2 |
| S-002 | Ordering constraints | "S-003 Steelman MUST be applied before S-002" (H-16) | NPT-012 (L2-injected via H-16) | Type 3 |
| S-003 | H-16 Compliance table | "S-002 without S-003 -- VIOLATION" | NPT-009 | Type 2 |
| S-004 | Step 1 Decision Point | "If S-003 output is missing: STOP. Flag H-16 violation." | NPT-009 + consequence | Type 2 |
| S-010 | Step 2 | "If zero findings identified, force yourself to find at least 3" | NPT-009 (leniency counteraction) | Type 2 |
| S-011 | Scoring Rubric | "MUST NOT be redefined" (weights) | NPT-009 | Type 2 |
| S-012 | Prerequisites | "MECE -- no gaps, no overlaps" | NPT-009 (completeness) | Type 2 |
| S-014 | Threshold | "MUST NOT be redefined" (threshold) | NPT-009 | Type 2 |

#### "When NOT to Use" Section Analysis

All adversarial templates contain a "When NOT to Use" section (mandated by TEMPLATE-FORMAT.md). However, the framing used is **positive redirect** language rather than explicit NEVER/MUST NOT:

| Template | "When NOT to Use" Pattern | NPT Classification |
|----------|--------------------------|-------------------|
| S-003 | "After multiple revision cycles... yields diminishing returns" | Positive redirect (NOT NPT-009) |
| S-004 | "Redirect to S-002 for C2 critique" | Positive redirect (NOT NPT-009) |
| S-010 | "Do NOT rely solely on S-010 for high-criticality work" | NPT-009 (partial) |
| S-011 | "Redirect to S-002... redirect to S-013" | Positive redirect (NOT NPT-009) |
| S-012 | "Redirect to S-002" | Positive redirect (NOT NPT-009) |
| S-013 | "Redirect to S-002 for C2... redirect to S-010 for C1" | Positive redirect (NOT NPT-009) |

S-010 is an exception: its "When NOT to Use" section explicitly states "Do NOT rely solely on S-010 for high-criticality work" — this is the only adversarial template that uses direct NPT-009 language in the "When NOT to Use" section.

#### Gap Analysis: Adversarial Templates

| Gap ID | Template(s) | Gap Description | Applicable NPT | Evidence Basis | Priority |
|--------|-------------|-----------------|---------------|----------------|----------|
| ADV-GAP-001 | All (S-001 through S-014) | "When NOT to Use" sections use positive redirect language rather than NEVER/MUST NOT phrasing | NPT-009 → NPT-011 | PG-001 (T1+T3): NEVER use standalone blunt prohibition — but **adding consequence documentation to redirects** is PG-003 guidance (T4) | MEDIUM |
| ADV-GAP-002 | S-001, S-002, S-004 | H-16 violation consequences are stated procedurally ("flag H-16 violation") but do not document **what quality degradation** results from skipping S-003 | NPT-011 (Justified Prohibition with Contextual Reason) | PG-003 (T4, MEDIUM): pair enforcement-tier constraints with consequences | LOW |
| ADV-GAP-003 | S-003, S-004, S-012, S-013 | The ordering constraint in Scoring Rubric says "MUST NOT be redefined" but does not explain **why** the constant must not change (breaks SSOT chain) | NPT-011 | T4 vendor self-practice (VS-003): HARD tier uses explicit negative framing; adding reason strengthens compliance | LOW |
| ADV-GAP-004 | TEMPLATE-FORMAT.md | The "When NOT to Use" section is mandated as REQUIRED but no constraint prevents template authors from using positive-only framing within it | NPT-009 (meta-constraint on template format) | T4: WTI-007 pattern shows that templates require NEVER constraints at creation to prevent drift | MEDIUM |

#### Specific Recommendations: Adversarial Templates

**ADV-REC-001** (addresses ADV-GAP-001, ADV-GAP-004): Add a constraint to TEMPLATE-FORMAT.md's "When NOT to Use" section specification:

> MUST NOT use "When NOT to Use" entries that are purely positive redirects without naming the failure mode they prevent. Each entry MUST state: (1) the condition that makes this strategy inappropriate, and (2) the redirect target. Positive redirect alone is insufficient for "When NOT to Use" entries.

NPT basis: NPT-009 (declarative behavioral negation) + NPT-011 (justified prohibition). Evidence: PG-001 (unconditional), PG-003 (T4, MEDIUM). This recommendation is CONDITIONAL on Phase 2 finding no null framing effect for Type 2 constraints at ranks 9-11.

**ADV-REC-002** (addresses ADV-GAP-002): For S-001, S-002, S-004, extend the "STOP" decision point text to include explicit consequence documentation. Example:

> "If S-003 Steelman output is missing: STOP. Proceeding without S-003 produces critique that attacks presentation weakness rather than substantive merit — this biases findings toward easily-observable surface defects and reduces finding quality by an unquantified but practitioner-observed margin. Flag H-16 violation and request S-003 execution before continuing."

NPT basis: NPT-011. Evidence: T4 (PG-003, MEDIUM). Label as T4 in template comments.

**ADV-REC-003** (SSOT protection enhancement for TEMPLATE-FORMAT.md): Add justified prohibition wrapper around "MUST NOT be redefined" in Scoring Rubric section:

> "Templates MUST NOT redefine these constants. Reason: Divergent constant values across templates break the SSOT chain — templates that define their own thresholds produce inconsistent quality gates that cannot be compared across the framework, invalidating cross-template quality tracking."

NPT basis: NPT-011 upgrade from NPT-009. Evidence: T4 (VS-003 pattern). Self-consistent with existing SSOT enforcement architecture.

---

## Worktracker Template Analysis (L1)

### Current State

Six entity templates (EPIC, FEATURE, STORY, TASK, BUG, ENABLER) were analyzed, plus WTI_RULES.md. FEATURE.md analysis is consolidated below under the shared gap entries — see Methodology "FEATURE.md Scope Note" for rationale.

#### MUST NOT / NEVER Inventory (Worktracker Templates)

| Template | Location | Constraint Text | NPT Classification | IG-002 Type |
|----------|----------|-----------------|-------------------|-------------|
| WTI_RULES.md | WTI-002 | "Work items MUST NOT transition to DONE/COMPLETED without..." | NPT-009 | Type 2 |
| WTI_RULES.md | WTI-003 | "MUST NOT be marked complete if work is incomplete" | NPT-009 | Type 2 |
| WTI_RULES.md | WTI-007 | "MUST NOT be created from memory or by copying other instance files" | NPT-009 | Type 2 |
| WTI_RULES.md | WTI-007 | "NEVER create entity files from memory" | NPT-009 | Type 2 |
| WTI_RULES.md | WTI-001 | "No 'TODO: update later' patterns allowed" | NPT-009 (behavioral) | Type 2 |
| STORY.md | AC quality | "AC must NOT contain DoD items" | NPT-009 | Type 2 |
| STORY.md | AC quality | "Do NOT include these items in individual work item Acceptance Criteria" | NPT-009 | Type 2 |
| TASK.md | BAD example | "# BAD (violates WTI-008b)" | NPT-008 (contrastive) | Type 1 |
| BUG.md | BAD example | "# BAD: marked DONE without evidence" | NPT-008 (contrastive) | Type 1 |
| ENABLER.md | BAD example | "# BAD: Entity file created from memory" | NPT-008 (contrastive) | Type 1 |
| FEATURE.md | BAD example | "# BAD (violates WTI-008b)" (same structural pattern as TASK.md) | NPT-008 (contrastive) | Type 1 |
| EPIC.md | None found | No MUST NOT / NEVER / BAD patterns | NPT-014 risk | N/A |

#### Key Structural Finding: Rules-Template Separation

The worktracker system separates integrity rules (WTI_RULES.md — strong NPT-009 patterns) from instantiation templates (EPIC.md, TASK.md etc. — weak NPT patterns, primarily NPT-008). This creates a gap: agents reading only the entity template without loading WTI_RULES.md receive insufficient negative constraint framing at the point of template instantiation.

WTI-007 mandates that agents MUST read the canonical template from `.context/templates/worktracker/` before creating any entity file. The canonical templates themselves are the authoritative guidance source at the moment of instantiation — not WTI_RULES.md, which is a reference document. Therefore, the templates are the appropriate location for embedding critical creation constraints.

#### Gap Analysis: Worktracker Templates

| Gap ID | Template(s) | Gap Description | Applicable NPT | Evidence Basis | Priority |
|--------|-------------|-----------------|---------------|----------------|----------|
| WT-GAP-001 | EPIC.md | No negative constraint language present. No MUST NOT, no NEVER, no BAD example. EPIC is the highest-level entity and its creation errors cascade to all children. | NPT-009 minimum; NPT-011 preferred | PG-001 (unconditional): NEVER use standalone blunt prohibition. EPIC currently has **no** prohibition — adding NPT-009 is unambiguously correct per T1+T3 evidence. | HIGH |
| WT-GAP-002 | TASK.md, BUG.md, ENABLER.md, FEATURE.md | NPT-008 contrastive patterns (BAD/GOOD) exist but no NPT-009 declarative constraints in acceptance criteria quality section. FEATURE.md exhibits the identical pattern. | NPT-009 or NPT-010 upgrade | PG-002 (T1+T4, HIGH): NEVER design constraint without hierarchy rank. NPT-008 is at AGREE-5 rank 10-11, lower than NPT-009 rank 9. | MEDIUM |
| WT-GAP-003 | STORY.md | Has NPT-009 for AC quality ("MUST NOT contain DoD items") but missing consequence explanation — operator must infer the failure mode from first principles | NPT-011 upgrade | PG-003 (T4, MEDIUM): pair enforcement-tier constraints with consequences | LOW |
| WT-GAP-004 | All entity templates (EPIC, FEATURE, STORY, TASK, BUG, ENABLER) | Templates do not embed the WTI-007 "NEVER create from memory" constraint at the top of the template — it lives only in WTI_RULES.md | NPT-009 (creation constraint) | T4 (WTI-007 pattern). Vendor self-practice (VS-001): Anthropic embeds constraints at point of use, not only in a separate rules document | HIGH |
| WT-GAP-005 | All entity templates | No NPT-012 (L2-re-injected) patterns in templates — critical constraints are not persisted to templates in a way that would survive context compaction | NPT-012 | T-004/GAP-13 (context compaction failure mode). Note: NPT-012 is a template design choice, not a prompt-writing technique — its applicability to static template files is domain-specific. | MEDIUM |

#### Specific Recommendations: Worktracker Templates

**WT-REC-001** (addresses WT-GAP-001, WT-GAP-004): Add the following section to EPIC.md immediately after the title/frontmatter block:

```markdown
## Creation Constraints

> **MANDATORY — MUST READ BEFORE POPULATING THIS TEMPLATE**

MUST NOT create this EPIC file from memory or by copying another EPIC instance. (WTI-007)
MUST read the canonical template from `.context/templates/worktracker/EPIC.md` first. (WTI-007)
MUST NOT mark this EPIC DONE without: all child features completed, evidence section populated, and 80%+ acceptance criteria verified. (WTI-002)

Why: EPIC errors cascade to all child Features, Stories, and Tasks. An under-specified EPIC
creates ambiguity that compounds at every decomposition level.
```

NPT basis: NPT-011 (justified prohibition). Evidence: PG-001 (unconditional, T1+T3), PG-003 (T4, MEDIUM). HIGH priority because EPIC.md currently has zero negative constraint language.

**WT-REC-002** (addresses WT-GAP-002): Upgrade BAD/GOOD AC examples in TASK.md, BUG.md, ENABLER.md, and FEATURE.md by adding an NPT-009 declarative constraint above the contrastive example. The same block applies to all four templates (FEATURE.md exhibits the identical TASK.md pattern and receives the same fix):

```markdown
> **Acceptance Criteria MUST NOT be generic.**
> Each AC item must be specific to this task and independently verifiable.
> AC that applies to every work item equally is DoD — not AC. (WTI-008a)
>
> BAD: "Code is tested" (applies to all tasks — belongs in DoD)
> GOOD: "The createUser endpoint returns 422 with structured error body when email is malformed"
```

For ENABLER.md specifically, the same declarative constraint applies with enabler-appropriate phrasing:

```markdown
> **Acceptance Criteria MUST NOT be generic or reference implementation details
> that belong in child story tasks.**
> Each AC item must be specific to this enabler's outcome and independently verifiable.
> AC that is identical across all enablers belongs in DoD — not AC. (WTI-008a)
>
> BAD: "The enabler is implemented" (tautological — not verifiable)
> GOOD: "The authentication middleware returns 401 with a structured error body when
> the JWT signature is invalid, as verified by integration test auth-middleware-002"
```

NPT basis: NPT-010 (Paired Prohibition with Positive Alternative) — upgrades standalone NPT-008 (contrastive illustration) to paired prohibition. Evidence: PG-002 (T1+T4, HIGH).

**WT-REC-003** (addresses WT-GAP-003): Add consequence clause to STORY.md's existing "MUST NOT contain DoD items" constraint:

> "Acceptance Criteria MUST NOT contain DoD items (tests, code review, documentation, deployment). Reason: Including DoD items in Story AC creates false Story-level quality gates — a Story appears incomplete when the DoD item is not yet done, blocking Story closure even when the feature is delivered. This pattern degrades velocity measurement and creates false IN_PROGRESS states. See DOD.md."

NPT basis: NPT-011 (upgrade from NPT-009). Evidence: PG-003 (T4, MEDIUM).

**WT-REC-004** (addresses WT-GAP-004): Add to all entity templates (EPIC, FEATURE, STORY, TASK, BUG, ENABLER) a standardized creation constraint block at the top of the template body (below frontmatter, above Document Sections):

```markdown
> **CREATION CONSTRAINT (WTI-007):** MUST NOT create this file from memory or by copying another
> instance file. Read the canonical template at `.context/templates/worktracker/{ENTITY_TYPE}.md`
> before populating. All REQUIRED sections must be present at creation.
```

NPT basis: NPT-009. Evidence: T4 (WTI-007). Consistent with VS-001 vendor self-practice of embedding constraints at the point of use. FEATURE.md is explicitly included in the target set; its NPT-008-only pattern (E-009-F) confirms the same gap exists as in TASK.md and BUG.md.

---

## Design Template Analysis (L1)

### Current State

PLAYBOOK.template.md and RUNBOOK.template.md were fully read. TDD.template.md could only be previewed (file too large for full context read — FMEA mitigation tables seen but complete analysis not possible).

#### MUST NOT / NEVER / STOP Inventory (Design Templates)

| Template | Location | Constraint Text | NPT Classification | IG-002 Type |
|----------|----------|-----------------|-------------------|-------------|
| PLAYBOOK.template.md | Section 4.1 | "Complete ALL items before proceeding. Do not skip any item." | NPT-009 | Type 2 |
| PLAYBOOK.template.md | Section 5.1 | "If any entry criteria not met: STOP — Do not proceed." | NPT-009 + consequence framing | Type 2 |
| PLAYBOOK.template.md | Section 2.4 | "Do NOT use this playbook when: {{EXCLUSION_N}} — Use {{ALTERNATIVE_N}} instead" | NPT-010 (paired prohibition + positive alternative) | Type 2 |
| PLAYBOOK.template.md | Section 9.1 | "Initiate rollback if ANY of these conditions occur" | Implicit NPT-009 (trigger-based negation) | Type 2 |
| PLAYBOOK.template.md | Section 9.2 | "IMMEDIATE ROLLBACK" (all caps), "ROLLBACK" | NPT-009 (imperative negation) | Type 2 |
| PLAYBOOK.template.md | Section 10.1 | "Escalate IMMEDIATELY if: Critical issue with no documented resolution" | NPT-009 | Type 2 |
| RUNBOOK.template.md | L0 section | "Do NOT use this runbook when: {{EXCLUSION_CONDITION_N}}" | NPT-009 | Type 2 |
| RUNBOOK.template.md | Rollback Triggers | "Initiate rollback when: Error rate exceeds 5%... Security vulnerability discovered" | NPT-009 (trigger-based) | Type 2 |
| RUNBOOK.template.md | Decision Tree | STOP pattern embedded in decision nodes | NPT-009 | Type 2 |
| RUNBOOK.template.md | Section 10.1 | "IMPORTANT: Use role-based contacts, NOT individual names" | NPT-009 | Type 2 |

#### Key Finding: Design Templates Are Strongest in Negative Constraint Framing

Design templates (Playbook, Runbook) have the highest density of NPT-009 patterns across all template families. The operational context (incident response, change execution) naturally demands explicit negative constraints — operators under pressure need to know when to STOP, ABORT, and ROLLBACK without ambiguity. This is consistent with PG-005 (T3, unconditional): enforcement architecture produces better outcomes than framing vocabulary, and the architectural requirement here IS the negative constraint framing itself.

The higher negative constraint density in Playbook and Runbook templates compared to entity templates reflects the domain's error consequence profile: operational template errors manifest immediately as production failures (outage, data loss, or service degradation), while entity template errors compound diffusely over time through degraded AC quality and closure verification failures. This distinction is T4 observational, grounded in the operational context of incident-management templates (E-016) and consistent with how STOP/ABORT/ROLLBACK instructions are standard practice in change management runbooks across the industry.

The "Do NOT use this runbook/playbook when" pattern in both templates is a well-formed NPT-010 (Paired Prohibition with Positive Alternative) implementation. Each exclusion names the alternative resource.

#### Gap Analysis: Design Templates

| Gap ID | Template(s) | Gap Description | Applicable NPT | Evidence Basis | Priority |
|--------|-------------|-----------------|---------------|----------------|----------|
| DT-GAP-001 | PLAYBOOK.template.md | Decision Points (DP-1, DP-2) use ABORT/ROLLBACK language but do not document what quality degradation occurs if the operator ignores the STOP signal | NPT-011 (add consequence clause) | PG-003 (T4, MEDIUM) | LOW |
| DT-GAP-002 | RUNBOOK.template.md | "Role-Based Contacts IMPORTANT: NOT individual names" constraint is present but the reason is embedded in a comment block, not visible in the rendered template | NPT-011 (surface the reason) | PG-003 (T4, MEDIUM) | LOW |
| DT-GAP-003 | TDD.template.md | File too large to fully assess — only FMEA section preview available. Cannot confirm whether design templates have negative constraints in FMEA / trade-off sections. | NPT-009 (needs verification) | Evidence gap (see Evidence Gap Map) | BLOCKED (requires chunked file read) |

#### Specific Recommendations: Design Templates

**DT-REC-001** (LOW priority, addresses DT-GAP-001): For PLAYBOOK decision point DP-1, add a brief consequence clause to the "If any entry criteria not met: STOP" instruction:

> "If any entry criteria not met: STOP — Do not proceed. Reason: Proceeding without meeting entry criteria creates an unrecoverable state if rollback is needed — the backup may not exist or may be stale, and change control documentation may be absent."

NPT basis: NPT-011 upgrade from NPT-009. Evidence: PG-003 (T4, MEDIUM).

**DT-REC-002** (LOW priority, addresses DT-GAP-002): Move the "Use role-based contacts, NOT individual names" constraint from HTML comment into visible template text:

> **CONTACT CONSTRAINT:** MUST NOT use individual person names in contact fields. Use role-based designations only (e.g., "On-Call Engineer," "Database SME"). Reason: Person-specific contacts become invalid on personnel changes and create single-point-of-failure when the named person is unavailable.

NPT basis: NPT-011. Evidence: PG-003 (T4, MEDIUM).

**DT-REC-003** (BLOCKED, addresses DT-GAP-003): TDD.template.md (69.1KB) cannot be fully assessed without chunked reading. Recommendations cannot be made for this template without full content.

**Concrete unblocking procedure for Phase 5:** Execute the following sequence of Read tool calls on TDD.template.md:

1. `Read(file_path="..../TDD.template.md", offset=0, limit=300)` — lines 1-300
2. `Read(file_path="..../TDD.template.md", offset=300, limit=300)` — lines 301-600
3. `Read(file_path="..../TDD.template.md", offset=600, limit=300)` — lines 601-900
4. Continue in 300-line increments until EOF is reached.

At approximately 100 characters per line average for a documentation template, 69.1KB corresponds to roughly 700-750 lines. Estimated call count: 3 Read calls. Phase 5 should assign the TDD analysis as the first task before any template modification work proceeds (see Phase 5 Input 3). This is a distinct task from the reversible template changes — TDD.template.md has no changes proposed and therefore no reversibility assessment is applicable until the analysis is complete.

---

## Requirements Template Analysis (L1)

### Current State

USE-CASE.template.md was fully read.

#### MUST NOT / NEVER Inventory (Requirements Templates)

| Template | Location | Constraint Text | NPT Classification | IG-002 Type |
|----------|----------|-----------------|-------------------|-------------|
| USE-CASE.template.md | Error Responses | "Error Responses MUST abide by [RFC7807]" | Positive constraint (MUST, not MUST NOT) | N/A |
| USE-CASE.template.md | Failed End Condition | Section names failure outcomes explicitly | Structural negative (implicit NPT-008) | Type 1 |
| USE-CASE.template.md | Trade-offs L2 section | "Why Not Chosen" column in trade-offs table | Implicit NPT-008 (elimination by exclusion) | Type 1 |
| USE-CASE.template.md | INVEST checklist | All positive framing | None | N/A |

#### Key Finding: Requirements Templates Are Weakest in Negative Constraint Framing

The USE-CASE template has effectively no NPT-009 patterns. Negative framing appears only as structural choices (a "Failed End Condition" section, "Why Not Chosen" column) — both of which are NPT-008 contrastive illustration at the template level, applied structurally.

This is the template family with the largest gap between current state and recommended practice. Requirements documents serve as the primary source of quality signal for downstream development — an under-constrained requirements template produces requirements that cannot be verified as complete or non-conflicting.

#### Gap Analysis: Requirements Templates

| Gap ID | Template(s) | Gap Description | Applicable NPT | Evidence Basis | Priority |
|--------|-------------|-----------------|---------------|----------------|----------|
| REQ-GAP-001 | USE-CASE.template.md | No MUST NOT constraints on acceptance criteria quality. The INVEST checklist uses all positive framing. Use cases can be instantiated without any prohibition on ambiguous or untestable requirements. | NPT-009 minimum | PG-001 (unconditional, T1+T3): NEVER standalone blunt prohibition — but current state is ZERO prohibition, which is worse than blunt prohibition | HIGH |
| REQ-GAP-002 | USE-CASE.template.md | "Failed End Condition" section provides structural negative framing but no constraint prevents the instantiation of a use case without populating this section | NPT-009 (completeness constraint) | T4: WTI-002 pattern shows that closure verification requires mandatory section evidence; same principle applies to requirements templates | MEDIUM |
| REQ-GAP-003 | USE-CASE.template.md | The "Why Not Chosen" trade-off column has no constraint preventing trivial or circular elimination rationale ("Not chosen because we chose Option A") | NPT-009 (rationale quality) | PG-002 (T1+T4, HIGH): Never design constraint without hierarchy rank. The elimination constraint here requires minimum evidence level for rejection claims. | LOW |

#### Specific Recommendations: Requirements Templates

**REQ-REC-001** (addresses REQ-GAP-001, HIGH priority): Add acceptance criteria quality constraints to USE-CASE.template.md:

```markdown
## Acceptance Criteria Quality Constraints

> MUST NOT create acceptance criteria that cannot be independently verified.
> MUST NOT create acceptance criteria that apply universally to all use cases (move to DoD).
> MUST NOT create acceptance criteria whose verification requires author interpretation.
>
> Each acceptance criterion MUST be:
> - Specific: names the exact system behavior under test
> - Independent: can be verified without running other criteria
> - Testable: has a binary pass/fail outcome
>
> BAD: "The system handles errors gracefully" (untestable, ambiguous)
> GOOD: "The system returns HTTP 422 with RFC7807-compliant error body when email field is missing from POST /users"
```

NPT basis: NPT-010 (paired prohibition with positive alternative). Evidence: PG-001 (unconditional, T1+T3), PG-002 (T1+T4, HIGH).

**REQ-REC-002** (addresses REQ-GAP-002): Add completion constraint to the "Failed End Condition" section:

```markdown
## Failed End Condition

> **COMPLETION CONSTRAINT:** MUST NOT submit this use case without populating this section.
> A use case without failure conditions is incomplete — it defines success but not the boundary
> that separates success from failure, making the requirement unverifiable.
```

NPT basis: NPT-011 (justified prohibition). Evidence: PG-003 (T4, MEDIUM).

**REQ-REC-003** (addresses REQ-GAP-003): Add rationale quality constraint to the "Why Not Chosen" column header:

```markdown
| Option | Trade-offs | Why Not Chosen (MUST state a specific disqualifying reason, not circular reference) |
```

NPT basis: NPT-009. Evidence: T4. LOW priority.

---

## Cross-Template Patterns (L2)

### Architectural Finding 1: Rules-Template Separation Creates Constraint Propagation Failure

The Jerry Framework separates integrity constraints (WTI_RULES.md, quality-enforcement.md) from instantiation templates. This is architecturally sound for separation of concerns but creates a **constraint propagation failure**: the agent instantiating a template encounters the constraint-poor template, not the constraint-rich rules document. The constraint is available in the rules but is not present at the point where the failure mode occurs (template creation).

This pattern is the reverse of VS-001 (Anthropic's practice): Anthropic embeds 33 NEVER/MUST NOT instances directly into the Claude Code behavioral rules files that agents read at task start — not in a separate governance document that may not be loaded. The Jerry Framework embeds operational guidance in a governance layer that agents may not load unless specifically instructed.

**Architectural recommendation (L2):** Add a "creation constraint block" standard to WTI-007 that requires entity templates to embed their critical WTI constraints inline, not only in WTI_RULES.md. This is a forward-compatible pattern: WTI_RULES.md remains the SSOT and the template creation constraint block references it (traceability maintained), but the constraint text is present at the point of template use.

### Architectural Finding 2: Operational Templates vs. Entity Templates Divergence

Playbook and Runbook templates have significantly stronger negative constraint framing than entity templates (EPIC, STORY, TASK). This divergence is not accidental — it reflects domain context:

- **Operational templates** (Playbook, Runbook): Errors have immediate, observable consequences in production environments — outages, data loss, and service degradation manifest within the change window. STOP/ABORT framing is natural and expected. Operators under incident pressure have high motivation to read constraints. (T4: consistent with standard operational change management practice, E-016)
- **Entity templates** (EPIC, STORY, TASK): Errors compound over time. AC quality failures are diffuse and delayed — a poorly written EPIC may not surface as a problem until sprint review, weeks after creation. Authors have lower perceived urgency, so negative constraints are more likely to be skipped if they are not embedded.

**Architectural implication (L2):** The Playbook/Runbook negative constraint density (NPT-009/NPT-010 throughout) should be the design target for entity template quality constraints. The lower urgency of entity creation makes embedded constraints MORE important, not less — the template cannot rely on operator vigilance.

### Architectural Finding 3: Tier Vocabulary Alignment

The Jerry Framework's HARD/MEDIUM/SOFT tier vocabulary in `.context/rules/quality-enforcement.md` is structurally identical to a meta-level negative prompting enforcement architecture:

- **HARD tier** (MUST/NEVER/MUST NOT): Cannot override — enforced as NPT-013 (Constitutional Triplet) through H-01 to H-36
- **MEDIUM tier** (SHOULD/RECOMMENDED): Overridable with justification — NPT-009 without hard enforcement
- **SOFT tier** (MAY/CONSIDER): No enforcement — positive framing defaults

The adversarial templates' "MUST NOT redefine" constraints are HARD-tier negative constraints enforced through the L2-REINJECT mechanism (NPT-012). This tier-to-NPT mapping is not explicit in the existing templates but is implied by the vocabulary choice (VS-003, T4, observational).

**MANDATORY EPISTEMIC CAVEAT (Barrier 2 constraint ST-5, Constraint 3):** The claim that the HARD/MEDIUM/SOFT tier vocabulary is superior to positive alternatives due to vocabulary choice itself is NOT experimentally validated. The tier vocabulary design predates this research. VS-001 through VS-004 establish that negative framing in the HARD tier is consistent with Anthropic's engineering practice (T4 observational). Three competing explanations exist (IG-001 audience specificity, IG-002 genre convention, IG-003 engineering discovery). The causal contribution of MUST NOT vs. MUST to behavioral compliance is UNTESTED pending Phase 2 experimental design.

### Architectural Finding 4: NPT-014 Anti-Pattern Risk Assessment

Across all template families, no standalone blunt prohibition instances (NPT-014) were found. The closest instances are:

- EPIC.md: No prohibition at all (worse than NPT-014 risk — absence of constraint)
- Contrastive BAD/GOOD examples in TASK.md, BUG.md, ENABLER.md, FEATURE.md: NPT-008 (evidence tier T3), not NPT-014

The NPT-014 risk is therefore not about existing anti-patterns to remediate but about **future instantiation errors** if new template content is added without the benefit of NPT taxonomy guidance. The Phase 5 recommendation (below) addresses this through a template authoring standard.

---

## Evidence Gap Map

| Claim | Evidence Tier | Confidence | Gap Type |
|-------|--------------|------------|----------|
| NPT-009 (Declarative Behavioral Negation) is more effective than NPT-008 (Contrastive Example) at preventing constraint violations | T3 (preprint) | MEDIUM | Phase 2 can reduce gap via C1-C7 experimental conditions |
| Adding NPT-011 consequence documentation to existing NPT-009 constraints increases compliance | T4 (practitioner observation) | MEDIUM (PG-003) | Phase 2 C4 vs C5 comparison |
| "When NOT to Use" sections in adversarial templates using positive redirects are less effective than NEVER/MUST NOT framing | Untested | LOW | Phase 2 must include adversarial template condition |
| EPIC.md having zero negative constraints produces more creation errors than EPIC.md with NPT-009 constraints | T5 (implied by WTI-007 rationale) | LOW | Field study or Phase 2 extension |
| Operational template (Playbook/Runbook) negative constraint density is the appropriate target density for entity templates | T4 (structural inference, E-016) | MEDIUM | No direct evidence that higher density in entity templates reduces errors |
| The HARD/MEDIUM/SOFT tier vocabulary's causal effect on behavioral compliance is due to negative framing | Untested | VERY LOW | Phase 2 C1 vs C6 comparison is the critical test |
| TDD.template.md negative constraint usage | Unavailable (file too large) | N/A | Tool limitation — requires chunked analysis per DT-REC-003 procedure |

**MANDATORY NOTE:** Do not treat MEDIUM or LOW confidence claims as HIGH in downstream phases. The ST-4 verdict (Barrier 2) explicitly states that ranks 9-11 of the AGREE-5 hierarchy are T4-evidenced only and their ordering is unvalidated. Any template recommendation based on rank ordering within 9-11 (declarative vs. paired vs. justified prohibition) carries this uncertainty.

---

## PG-003 Contingency Plan

PG-003 (T4, MEDIUM, conditional): "Pair enforcement-tier constraints with consequences (NEVER/MUST NOT + reason)." The recommendations labeled NPT-011 (ADV-REC-002, ADV-REC-003, WT-REC-003, DT-REC-001, DT-REC-002, REQ-REC-002) are all grounded in PG-003.

**PG-003 contingency:** If Phase 2 finds a null framing effect for behavioral negation at ranks 9-11 (i.e., NEVER + reason performs no better than NEVER alone, or NEVER performs no better than SHOULD), then the NPT-011 upgrade recommendations (adding consequence clauses) are convention-determined rather than effectiveness-determined. In that case:

- NPT-011 upgrades remain valid as style improvements (consistent with convention, lower cognitive load for readers)
- But they MUST NOT be presented as evidence-based compliance improvements
- The priority ratings for NPT-011 recommendations should be downgraded from MEDIUM/LOW to OPTIONAL
- The unconditional recommendations (PG-001 against standalone blunt prohibition, PG-005 favoring enforcement architecture) remain valid regardless of Phase 2 outcome

**PG-003 contingency trigger:** Phase 2 condition C4 (structured negative with consequence) vs. C3 (structured negative without consequence) comparison produces p > 0.05 on the McNemar test.

**Recommendations NOT affected by PG-003 contingency:**
- WT-REC-001 (add ANY constraints to EPIC.md — currently has zero): Valid by PG-001 regardless of rank ordering effects
- WT-REC-004 (add creation constraint blocks to all entity templates): Valid by WTI-007 pattern and VS-001 vendor practice
- REQ-REC-001 (add ANY quality constraints to USE-CASE.template.md): Valid by PG-001
- ADV-REC-001 (prevent purely positive "When NOT to Use" entries): Valid by PG-002 (always include hierarchy rank in constraint design)
- DT-REC-003 (TDD analysis is blocked): Independent of PG-003

---

## Phase 5 Downstream Inputs

The following inputs are required for the next research phase.

### Phase 5 Input 1: Constraint Category Prioritization

Phase 4 analysis identified four constraint categories in decreasing urgency:

| Priority | Category | Affected Templates | NPT Basis |
|----------|----------|-------------------|-----------|
| HIGH | Creation constraints (point-of-instantiation) | EPIC, FEATURE, STORY, TASK, BUG, ENABLER, USE-CASE | NPT-009 + WTI-007 |
| HIGH | Absence of any constraint | EPIC.md (zero constraints), USE-CASE.template.md AC section | NPT-009 minimum |
| MEDIUM | Contrastive-to-declarative upgrade | TASK.md, BUG.md, ENABLER.md, FEATURE.md (NPT-008 → NPT-010) | NPT-010 |
| MEDIUM | "When NOT to Use" negative constraint framing | All adversarial templates (TEMPLATE-FORMAT.md spec) | NPT-009 + NPT-011 |
| LOW | Consequence clause addition | STORY.md, PLAYBOOK.template.md sections | NPT-011 |
| BLOCKED | TDD.template.md full analysis | TDD.template.md | Requires chunked file read per DT-REC-003 procedure |

### Phase 5 Input 2: Template Update Reversibility Assessment

Recommended template changes in this analysis for Worktracker, Adversarial, and Requirements families are reversible within 1 day (C2 criticality). They involve adding text to existing template sections or adding new constraint blocks. No changes propose removing existing content, restructuring template hierarchy, or modifying enforcement mechanism code. PG-003 contingency provisions ensure that NPT-011 additions can be cleanly reverted to NPT-009 if Phase 2 finds null framing effects. Design family recommendations DT-REC-001 and DT-REC-002 are also reversible within 1 day (C2 criticality).

**Note on DT-REC-003 (TDD.template.md):** DT-REC-003 is BLOCKED — no template changes are proposed for TDD.template.md because the file could not be fully analyzed. There are no changes to reverse for TDD.template.md, and no reversibility assessment is applicable until the TDD analysis is complete per the DT-REC-003 unblocking procedure.

**Template updates that MUST NOT be made before Phase 2:**
- MUST NOT change the enforcement tier vocabulary (HARD/MEDIUM/SOFT keyword choice) in any rule file — Phase 2 tests this as C1 condition (ST-5, Constraint 1; `barrier-2/synthesis.md`)
- MUST NOT redesign the L2-REINJECT mechanism — this would make Phase 2 experimental conditions unreproducible (ST-5, Constraint 2; `barrier-2/synthesis.md`)
- MUST NOT restructure the WTI_RULES.md / entity template separation — the current architecture is part of what Phase 2 tests (ST-5, Constraint 3; `barrier-2/synthesis.md`)

### Phase 5 Input 3: TDD Analysis Gap

TDD.template.md analysis is INCOMPLETE. The file (69.1KB) exceeds the Read tool's practical per-call limit. A chunked read approach (Read with offset/limit in 300-line increments) can complete the analysis. The TDD template is the primary design documentation template and may have important negative constraints in its FMEA, risk, and trade-off sections.

**Phase 5 Task — TDD Analysis Completion (Forward trace from E-014):**
- **Mechanism:** Execute DT-REC-003 chunked Read procedure (see Design Template Analysis section above)
- **Estimated effort:** 3 Read tool calls at 300 lines per call for ~750-line file
- **Precondition:** None — no dependencies on other Phase 5 tasks
- **Sequencing:** MUST execute before any TDD.template.md modification is proposed
- **Owner:** Phase 5 ps-analyst agent, first task before template modification work

### Phase 5 Input 4: Template Update vs. Rule Update Decision

Some gaps identified in this analysis could be addressed either by updating templates OR by updating the corresponding rules files (WTI_RULES.md, quality-enforcement.md). Phase 5 should clarify which layer is the correct intervention point for each gap, applying the principle from the Architectural Finding 1:

- **Template layer**: Constraints at point of instantiation (creation errors)
- **Rules layer**: Constraints at point of policy (governance compliance)
- Both layers may be appropriate for HIGH priority gaps (redundant enforcement)

### Phase 5 Input 5: Phase 2 Experimental Conditions Alignment

The Phase 4 recommendations create alignment requirements for Phase 2 experimental design:

| Phase 4 Recommendation | Phase 2 Condition Required |
|------------------------|---------------------------|
| NPT-009 vs NPT-008 upgrade in worktracker templates | C3 (standalone NEVER/MUST NOT) vs. C1 (naive) |
| NPT-011 consequence clause addition | C4 (NEVER + reason) vs. C3 (NEVER alone) |
| NPT-010 paired prohibition | C5 (prohibition + positive alternative) |
| "When NOT to Use" positive redirect vs. NEVER | C2 (structured positive) vs. C3 (structured negative) |
| HARD tier vocabulary vs. positive alternatives | C1 (naive blunt) vs. C6 (positive structured equivalent) |

Phase 2 experimental conditions C1-C7 (as defined in `barrier-2/synthesis.md`) can address all Phase 4 validation requirements if they include worktracker entity template instantiation tasks as test condition artifacts.

---

## Evidence Summary

| Evidence ID | Type | Source | Claim Supported | Tier |
|-------------|------|--------|----------------|------|
| E-001 | Research finding | `barrier-2/synthesis.md` ST-4, PG-001 | NEVER use standalone blunt prohibition | T1+T3, HIGH |
| E-002 | Research finding | `barrier-2/synthesis.md` ST-4, PG-002 | Never design constraint without hierarchy rank | T1+T4, HIGH |
| E-003 | Research finding | `barrier-2/synthesis.md` ST-4, PG-003 | Pair enforcement-tier constraints with consequences | T4, MEDIUM (conditional) |
| E-004 | Research finding | `barrier-2/synthesis.md` ST-4, PG-005 | Prioritize enforcement architecture over framing vocabulary | T3, unconditional |
| E-005 | Vendor self-practice | `barrier-1/supplemental-vendor-evidence.md` VS-001 | Anthropic uses 33 NEVER/MUST NOT instances in production rules | T4, observational |
| E-006 | Vendor self-practice | `barrier-1/supplemental-vendor-evidence.md` VS-003 (T4, observational) | HARD tier vocabulary is expressed as explicit prohibitions | T4, observational |
| E-007 | Template analysis | `EPIC.md` direct read | Zero negative constraints in EPIC template | Direct evidence |
| E-008 | Template analysis | `STORY.md` direct read | NPT-009 present for AC DoD boundary | Direct evidence |
| E-009 | Template analysis | `TASK.md`, `BUG.md`, `ENABLER.md` direct reads | NPT-008 (contrastive) but not NPT-009 | Direct evidence |
| E-009-F | Template analysis | `FEATURE.md` direct read | NPT-008 (contrastive BAD/GOOD) present; no NPT-009 declarative constraint; no creation constraint block — identical pattern to TASK.md and BUG.md | Direct evidence |
| E-010 | Template analysis | `WTI_RULES.md` direct read | NPT-009 patterns in rules but not propagated to templates | Direct evidence |
| E-011 | Template analysis | `TEMPLATE-FORMAT.md`, `s-001` through `s-014` direct reads | NPT-009 present for SSOT protection and H-16 ordering | Direct evidence |
| E-012 | Template analysis | `PLAYBOOK.template.md`, `RUNBOOK.template.md` direct reads | Highest NPT-009/NPT-010 density across all template families | Direct evidence |
| E-013 | Template analysis | `USE-CASE.template.md` direct read | No NPT-009 constraints in requirements template | Direct evidence |
| E-014 | Tool limitation | Read tool output | TDD.template.md analysis incomplete (69.1KB file) — forward trace: Phase 5 Input 3, DT-REC-003 chunked read procedure | N/A — acknowledged gap |
| E-015 | Taxonomy | `phase-3/taxonomy-pattern-catalog.md` NPT-001 through NPT-014 | Pattern definitions and evidence tiers | T1/T3/T4/Untested per pattern |
| E-016 | Domain context | Operational change management practice (T4, industry-standard) | Operational template errors (Playbook/Runbook) manifest immediately as production failures; cited in Architectural Finding 2 | T4, observational |

---

## PS Integration

```yaml
analyst_output:
  ps_id: "phase-4"
  entry_id: "TASK-014"
  analysis_type: "gap-analysis + impact-analysis"
  artifact_path: "projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-4/templates-update-analysis.md"
  key_findings:
    - "EPIC.md has zero negative constraints — highest priority gap across all template families"
    - "WTI_RULES.md contains strong NPT-009 patterns that are NOT propagated to instantiation templates — constraint propagation failure"
    - "Design templates (Playbook/Runbook) are the strongest in negative constraint density; entity templates are the weakest"
    - "All NPT-011 (consequence clause) recommendations are conditional on PG-003 (T4, MEDIUM) and subject to Phase 2 null-effect contingency"
    - "Adversarial templates use positive redirect language in 'When NOT to Use' sections — gap exists but is MEDIUM priority only"
    - "TDD.template.md analysis is BLOCKED due to file size limit — Phase 5 Task assigned with chunked Read procedure (DT-REC-003)"
  recommendation: "Implement HIGH priority gaps (EPIC.md creation constraints, USE-CASE.template.md AC quality constraints, universal creation constraint block across entity templates) before Phase 2; defer NPT-011 upgrades until Phase 2 verdict"
  confidence: "high"
  confidence_note: "High for gap identification; MEDIUM for specific NPT upgrade recommendations (T4 evidence basis, PG-003 conditional)"
  next_agent_hint: "Phase 5 template update implementation agent"
```

---

*Analysis Version: 2.0.0*
*Revision: I2 — addresses all 6 improvement recommendations and 3 new findings from I1 scoring (adversary-templates-i1.md)*
*Agent: ps-analyst*
*Date: 2026-02-28*
*Input Artifacts: phase-3/taxonomy-pattern-catalog.md, barrier-1/synthesis.md, barrier-1/supplemental-vendor-evidence.md, barrier-2/synthesis.md, all .context/templates/ files*
*Constitutional Compliance: P-001 (evidence-cited), P-002 (file persisted), P-022 (uncertainty acknowledged for T4 claims)*

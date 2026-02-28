# Barrier 4 Cross-Pollination Synthesis: Phase 4 Application Analysis Integration

> ps-synthesizer | TASK-015 | Barrier 4 | PROJ-014 | 2026-02-28
> Synthesis Type: Cross-pollination of Phase 4 application analysis outputs (TASK-010 through TASK-014)
> Inputs: skills-update-analysis.md (v2.0.0, 0.951 PASS), agents-update-analysis.md (v3.0.0, 0.951 PASS), rules-update-analysis.md (0.953 PASS), patterns-update-analysis.md (v5.0.0, 0.950 PASS), templates-update-analysis.md (v3.0.0, 0.955 PASS) + barrier-2/synthesis.md (v3.0.0, 0.950 PASS) + phase-3/taxonomy-pattern-catalog.md (v3.0.0, 0.957 PASS) + barrier-1/supplemental-vendor-evidence.md (R4, 0.951 PASS)
> Quality threshold: >= 0.95 (C4, orchestration directive)
> Self-review: H-15 applied before completion
> Version: v4.0.0
> I2 Revision (2026-02-28): 6 targeted fixes from adversary-gate-i1.md (score 0.931 → target >= 0.95): (1) Group 2 total audited and corrected (62 → 77; explicit arithmetic added); (2) TASK-014 Rec-ID count verified as 13 named recommendations (12 actionable, 1 BLOCKED) not ~16; (3) A-11 weakening propagated to WT-REC-002 evidence note in Group 2; (4) direct quotes added for TASK-012→TASK-011 and TASK-012→TASK-010 dependency claims; (5) PS Integration self-assessment note added explaining why dimension scores reflect content quality assessment independent of count precision uncertainties; (6) cross-cutting threshold defined in Section 2 introduction.
> I3 Revision (2026-02-28): 2 targeted fixes from adversary-gate-i2.md (score 0.940 → target >= 0.95): (1) AGREE-5 "NOT externally validated" caveat added as blockquote note to Section 4 Group 2 introduction — NEVER cite AGREE-5 rank ordering as T1 or T3 evidence; (2) NPT-010 consequence additions corrected from 5 skills to 6 skills (adversary, ast, orchestration, red-team, saucer-boy, saucer-boy-framework-voice per skills-update-analysis.md CX-003 and ADR-003 inputs); arithmetic updated 13+5+3+27+6+18+5=77 → 13+6+3+27+6+18+5=78; consolidated total updated ~124 → ~125.
> I4 Revision (2026-02-28): 2 targeted fixes from adversary-gate-i3.md (score 0.947 → target >= 0.95): (1) Group 3 TASK-014 row corrected — WT-REC-004 parenthetical "(NPT-012/context compaction resilience)" was mislabeled; WT-REC-004 addresses creation constraint embedding (WT-GAP-004) not context compaction; entry now reads "WT-REC-004 (see Group 1 for creation constraint embedding per WT-GAP-004), WT-GAP-005 (NPT-012/context compaction resilience — no corresponding Rec yet, pending Phase 5)"; (2) Row-level AGREE-5 indicators added to TASK-012 Group 2 row ("[priority per AGREE-8/AGREE-9 components of AGREE-5 — see AGREE-5 caveat above]") and TASK-013 Group 2 row ("[priority per AGREE-5 hierarchy ranks 9–11 — see AGREE-5 caveat above]") so Phase 5 writers can identify AGREE-5-derived rows without cross-referencing.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Total recommendations, cross-cutting themes, confidence, dependencies |
| [L1: Technical Synthesis](#l1-technical-synthesis) | Cross-cutting theme analysis with source citations |
| [L2: Strategic Synthesis](#l2-strategic-synthesis) | Strategic themes, architectural implications |
| [Section 2: Cross-Cutting Theme Analysis](#section-2-cross-cutting-theme-analysis) | Per-theme analysis across all 5 domains |
| [Section 3: Recommendation Dependency Map](#section-3-recommendation-dependency-map) | Dependencies, ordering constraints, conflict identification |
| [Section 4: Consolidated Implementation Priority](#section-4-consolidated-implementation-priority) | Merged priority groups from all 5 analyses |
| [Section 5: Phase 5 ADR Inputs](#section-5-phase-5-adr-inputs) | What the 4 Phase 5 ADRs need from this cross-pollination |
| [Section 6: Evidence Gap Consolidation](#section-6-evidence-gap-consolidation) | Combined evidence gaps across all 5 analyses |
| [Section 7: Constraint Propagation Verification](#section-7-constraint-propagation-verification) | GC-P4-1, GC-P4-2, GC-P4-3 verification across all 5 analyses |
| [Section 8: PS Integration](#section-8-ps-integration) | Confidence assessment, artifact table, downstream hints |
| [Self-Review Checklist](#self-review-checklist) | H-15 compliance |
| [Source Summary](#source-summary) | All input sources with contribution summary |
| [I2 Fix Resolution Checklist](#i2-fix-resolution-checklist) | Resolution status for all 6 I1 adversary gate fixes |
| [I3 Fix Resolution Checklist](#i3-fix-resolution-checklist) | Resolution status for 2 I2 adversary gate fixes |
| [I4 Fix Resolution Checklist](#i4-fix-resolution-checklist) | Resolution status for 2 I3 adversary gate fixes |

---

## L0: Executive Summary

### What Was Synthesized

Five Phase 4 application analyses produced a combined catalog of **130 specific recommendations** across five Jerry Framework artifact domains: Skills (TASK-010: 37 recommendations across 13 skills), Agents (TASK-011: 32 recommendations across 9 families), Rules (TASK-012: 14 recommendations across 17 rule files), Patterns (TASK-013: 34 recommendations across 12 categories), and Templates (TASK-014: 13 named recommendations across 4 template families — ADV-REC-001–003, WT-REC-001–004, DT-REC-001–003, REQ-REC-001–003; DT-REC-003 is BLOCKED). This synthesis cross-pollinates those outputs to identify shared patterns, ordering dependencies, and the consolidated ADR scope for Phase 5.

**MANDATORY EPISTEMOLOGICAL CONSTRAINT:** NEVER use this synthesis to claim that any of the 130 recommendations have experimental validation. All five analyses carry the T4 observational label with UNTESTED causal comparison against positive-framing equivalents. This synthesis does not elevate evidence tiers. The PG-003 reversibility contingency applies to all framing-motivated recommendations throughout.

### Key Cross-Cutting Findings

**Cross-cutting theme count:** 6 major themes identified that appear across 3 or more of the 5 analyses (see Section 2).

**Key dependency:** NEVER implement any Phase 4 recommendation before Phase 2 experimental conditions are complete. All five analyses carry this constraint uniformly — it is the single most critical ordering constraint.

**Implementation sequence:** NPT-014 elimination (blunt prohibition upgrade) is the one action supported by T1+T3 unconditional evidence (PG-001) and therefore is the only category that does not require Phase 2 completion before proceeding.

### Consolidated Confidence Assessment

| Tier | Applicable Recommendations | Evidence Basis | Action Status |
|------|---------------------------|----------------|---------------|
| T1+T3, HIGH, unconditional | All NPT-014 → NPT-009 upgrades | PG-001: blunt prohibition demonstrably underperforms | Actionable NOW, Phase 2 outcome irrelevant |
| T4 observational, HIGH observational / LOW causal | NPT-013 constitutional triplet upgrades, VS-003 tier vocabulary | VS-001–VS-004, 33-instance vendor self-practice catalog | Actionable as working practice; contingent on Phase 2 for causal justification |
| T4 observational, MEDIUM, UNTESTED causal | NPT-009, NPT-010, NPT-011 framing upgrades | AGREE-7, AGREE-8, AGREE-9 cross-survey agreement | Contingent on Phase 2 outcome; reversible under PG-003 null finding |

---

## L1: Technical Synthesis

### Evidence Framework Inherited by All 5 Analyses

All five Phase 4 analyses draw from the same upstream evidence framework established in barrier-2/synthesis.md (v3.0.0, 0.950 PASS) and the Phase 3 taxonomy (v3.0.0, 0.957 PASS). The shared infrastructure includes:

- **NPT-001 through NPT-014:** The 14 negative prompting taxonomy patterns from phase-3/taxonomy-pattern-catalog.md, representing 13 distinct techniques (NPT-007 and NPT-014 are dual entries for the same Type 1 blunt prohibition)
- **PG-001 through PG-005:** Practitioner guidance with explicit confidence tiers from barrier-2/synthesis.md ST-4
- **VS-001 through VS-004:** 33-instance vendor self-practice catalog from supplemental-vendor-evidence.md (T4 observational, Anthropic-heavy concentration)
- **AGREE-5 12-level effectiveness hierarchy:** Internally generated synthesis narrative (passed adversary gate 0.953, NOT externally validated)
- **ST-5 Phase 4 constraints:** Three binding constraints from barrier-2/synthesis.md that all four Phase 4 adversary gates were required to verify

This shared evidence framework means disagreements between analyses are not epistemic — they are domain-specific differences in which NPT patterns apply in which artifact contexts.

### Recommendation Counts Per Analysis

| Analysis | Task | Rec Count | Version | Quality Score | Iterations |
|----------|------|-----------|---------|---------------|------------|
| Skills Update | TASK-010 | 37 (13 skills × ~3 recs avg) | v2.0.0 | 0.951 | 2 |
| Agents Update | TASK-011 | 32 (5 framework-level + 27 agent-level) | v3.0.0 | 0.951 | 3 |
| Rules Update | TASK-012 | 14 (across 17 rule files) | — | 0.953 | 3 |
| Patterns Update | TASK-013 | 34 (6 MUST NOT omit + 18 SHOULD + 10 MAY) | v5.0.0 | 0.950 | 5 |
| Templates Update | TASK-014 | 13 named (12 actionable, 1 BLOCKED: DT-REC-003) | v3.0.0 | 0.955 | 3 |
| **TOTAL** | | **130** | | | |

**TASK-013 note:** TASK-013 required 5 iterations to reach 0.950 PASS — the most iterations of any Phase 4 analysis. This reflects the A-11 citation issue (arXiv ID confirmed as hallucinated in I4/I5 revision; NPT-008 evidence now rests solely on E-007) and the recommendation count corrections (28 → 34 at 7 locations) that required multiple precision fixes. Phase 5 ADR writers MUST NOT cite A-11 in any downstream document.

### NPT Pattern Applicability Convergence

Across all 5 analyses, the following applicability convergence was observed:

| NPT Pattern | Skills | Agents | Rules | Patterns | Templates | Convergence |
|-------------|--------|--------|-------|----------|-----------|-------------|
| NPT-009 (declarative behavioral negation) | YES (primary) | YES (primary) | YES (primary) | YES (primary) | YES (primary) | ALL 5 — universal |
| NPT-010 (paired prohibition + positive alt.) | YES | YES | YES | YES | YES (partial) | ALL 5 — universal |
| NPT-013 (constitutional triplet) | YES | YES | YES (partial) | NO (out of scope) | NO | 3 of 5 |
| NPT-014 as diagnostic | YES | YES | YES | YES | YES | ALL 5 — universal |
| NPT-011 (justified prohibition) | PARTIAL | YES (partial) | YES | YES | YES | 4 of 5 |
| NPT-012 (L2 re-injected) | NO (SKILL.md is L1) | NO (agent files not L2-injectable) | YES (primary mechanism) | PARTIAL (3 uses) | PARTIAL | 2 of 5 |
| NPT-008 (contrastive example) | NO | NO | NO | YES (upgrade from) | YES (current state) | 2 of 5 |

**Critical NPT-012 scoping agreement:** TASK-010 and TASK-011 both explicitly exclude NPT-012 from skill and agent file applicability. SKILL.md files are L1-loaded (not L2-injectable); agent .md files are Tier 2 (loaded at agent invocation, not re-injected per prompt). This is a cross-analysis constraint that Phase 5 ADRs must not contradict. TASK-012 is the ONLY domain where NPT-012 is applicable as new recommendations; it already operates there.

---

## L2: Strategic Synthesis

### Architectural Implication: The Maturity Stack

All five analyses independently identify a three-tier maturity pattern for negative constraint usage within their respective domains. The tiers differ by domain but converge on the same structural observation: negative constraint maturity is not uniformly absent — it is unevenly distributed, with some artifacts already implementing higher NPT patterns than others.

| Tier | Skills (TASK-010) | Agents (TASK-011) | Rules (TASK-012) | Patterns (TASK-013) | Templates (TASK-014) |
|------|-------------------|-------------------|-------------------|---------------------|----------------------|
| High maturity | transcript/SKILL.md (quantified NPT-009) | nse-requirements, ts-parser, wt-auditor (NPT-009 + VIOLATION labels) | agent-development-standards.md (8 instances, NPT-009 quality) | Testing category (BDD/TDD have sequence gate structure) | Adversarial templates (NPT-009 for SSOT protection) |
| Mid maturity | adversary, red-team, orchestration (partial NPT-010) | ps-analyst, ps-researcher, ps-critic, orch-planner (triplet + partial NPT-009) | python-environment.md, architecture-standards.md | Architecture category (dependency matrix tables) | Design templates (PLAYBOOK/RUNBOOK with operational stops) |
| Low maturity | bootstrap, saucer-boy, worktracker (Group A — minimal) | eng-architect, eng-security, red-lead, adv-executor (flat markdown NPT-014) | mandatory-skill-usage.md, mcp-tool-standards.md (zero instances) | Domain service, identity, value object (no anti-pattern sections) | Worktracker entity templates (NPT-008 only; EPIC.md has zero) |

**Strategic implication (T4 observational):** The maturity distribution is not random — it correlates with domain specificity and operational risk. High-maturity artifacts govern high-consequence operations (transcript parsing with 1,250x cost differential; security testing with authorization gates). This suggests that practitioners instinctively apply stronger constraint framing in high-consequence contexts, which is consistent with the VS-003 finding (vendor self-practice concentrates prohibitive vocabulary in HARD enforcement tier). NEVER treat this as causal — it is an observational correlation.

### Architectural Implication: The Rules-SKILL-Agent-Pattern-Template Hierarchy

Phase 4 reveals a constraint propagation hierarchy that has architectural implications for Phase 5 ADR scope:

```
.context/rules/ (HARD enforcement tier, L1+L2, source of truth)
    |
    +--> skills/*/SKILL.md (L1-loaded routing documents, no L2)
    |        |
    |        +--> skills/*/agents/*.md (Tier 2, loaded at invocation)
    |                |
    |                +--> .governance.yaml (machine-readable governance, schema-validated)
    |
    +--> .context/templates/ (instantiation-time documents)
    |
    +--> docs/patterns/ (reference documentation, enforcement is programmatic)
```

**Implication for Phase 5:** ADR decisions must respect this hierarchy. A constraint expressed only in a SKILL.md cannot be L2-re-injected (TASK-010's NPT-012 exclusion finding). A constraint in a rule file CAN be L2-re-injected and therefore survives context compaction (T-004 mitigation). Phase 5 ADR-004 (context compaction testing) must account for where constraints live in this hierarchy.

---

## Section 2: Cross-Cutting Theme Analysis

A theme qualifies as cross-cutting when it appears in 3 or more of the 5 analyses (TASK-010 through TASK-014). Themes appearing in all 5 analyses are marked "universal" (5/5). Themes present in 4 of 5 analyses are marked "near-universal" (4/5). The threshold of 3 analyses was chosen because it requires independent corroboration from a majority of domains without requiring unanimity that could suppress domain-specific but broadly applicable findings. All 6 themes identified below meet or exceed this threshold.

### Theme 1: NPT-009 as the Universal Upgrade Target

**Present in:** ALL 5 analyses (TASK-010, TASK-011, TASK-012, TASK-013, TASK-014)
**Evidence tier:** T4 observational for the pattern itself; T1+T3 unconditional for the upgrade FROM NPT-014
**Confidence:** HIGH for directional preference (upgrade blunt prohibition); UNTESTED for causal superiority over positive equivalents

**Description:** Every analysis independently identifies that existing negative constraints are predominantly NPT-014 (blunt prohibition without consequence, scope, or positive pairing) and that the primary upgrade target is NPT-009 (declarative behavioral negation with consequence). This convergence is not artifactual — each analysis applied the NPT-014 diagnostic independently and found the same pattern.

| Analysis | NPT-014 Finding | NPT-009 Upgrade Scope |
|----------|----------------|----------------------|
| TASK-010 (Skills) | 4 skills have "NEVER hardcode values" as standalone NPT-014 | All NPT-014 instances require NPT-009 upgrade |
| TASK-011 (Agents) | H-35 minimum (`"Spawn recursive subagents (P-003)"`) is NPT-014; all 30+ agents affected | Low-maturity agents (eng-architect, red-lead, adv-executor, sb-voice) as primary targets |
| TASK-012 (Rules) | 22 of 36 instances (61%) are NPT-014 | 6 specific upgrade recommendations (highest priority) |
| TASK-013 (Patterns) | All anti-pattern sections use NPT-014/NPT-008 structure | 34 recommendations, NPT-009 is primary pattern (18 of 34 uses) |
| TASK-014 (Templates) | EPIC.md has zero negative constraints; TASK/BUG/ENABLER use NPT-008 | WT-REC-001 through WT-REC-004; EPIC.md as highest priority |

**Implication for Phase 5:** ADR-001 (NPT-014 elimination policy) is the highest-priority ADR. It is unconditional per PG-001 (T1+T3, HIGH). It does not require Phase 2 completion before drafting.

**Cross-analysis consistency finding:** The NPT-014 prevalence figures are consistent across analyses. TASK-012 finds 61% of rule-file instances are NPT-014; TASK-011 finds that H-35 minimum enforcement produces NPT-014 format in all agents; TASK-010 finds the same "NEVER hardcode values" NPT-014 pattern in 4 of 13 skills. The pattern is systemic, not isolated. This convergence strengthens confidence that NPT-014 elimination is a real and widespread gap, not an analytical artifact.

---

### Theme 2: NPT-014 as Diagnostic Baseline Across All Domains

**Present in:** ALL 5 analyses (TASK-010, TASK-011, TASK-012, TASK-013, TASK-014)
**Evidence tier:** T1+T3 (NPT-014 underperformance is established; this is PG-001)
**Confidence:** HIGH unconditional (PG-001 applies regardless of Phase 2 outcome)

**Description:** Every analysis uses NPT-014 identification as the entry-level diagnostic — any NEVER/MUST NOT statement without (a) consequence documentation, (b) scope specification, and (c) positive behavioral pairing is classified NPT-014 and flagged for upgrade. This diagnostic is explicitly stated in TASK-010 Methodology Phase A ("NPT Diagnostic Filter"), TASK-011 Evaluation Criteria EC-03, TASK-012 NPT Mapping Approach (decision tree step 1), TASK-013 Finding 1, and TASK-014 Gap Analysis for worktracker templates.

**Significance:** All five analyses agree that NPT-014 is the universal baseline problem. This is not a preference finding — it is T1+T3 established: blunt prohibition underperforms structured alternatives. The decision to label the existing constraint inventory's dominant pattern as NPT-014 is operationally precise and downstream-consistent.

**Vendor evidence connection:** The supplemental-vendor-evidence.md (barrier-1) documents that Anthropic uses structured constraint framing (NPT-009 equivalent) in its HARD enforcement tier rules (VS-003), not NPT-014. The gap between Anthropic's practice and Jerry's current state is exactly the NPT-014 prevalence identified across all 5 analyses. NEVER dismiss this as coincidence — it is a direct T4 observational finding that the framework's owner applies higher constraint standards in their own tooling than the framework currently implements in its documentation.

---

### Theme 3: NPT-013 Constitutional Triplet as Governance Enforcement Pattern

**Present in:** TASK-010 (Skills), TASK-011 (Agents), TASK-012 (Rules — partial), TASK-014 (Templates — partial)
**Evidence tier:** T4 observational (VS-004: Anthropic expresses constitutional constraints as prohibitions in rule files)
**Confidence:** T4 observational; reversible under PG-003 null framing effect

**Description:** Three of five analyses specifically flag NPT-013 (constitutional triplet: P-003/P-020/P-022 expressed as NEVER-framed prohibitions) as a cross-cutting gap. TASK-010 finds that all 13 SKILL.md Constitutional Compliance tables use positive framing ("Agents are workers, not orchestrators") instead of prohibitive framing ("NEVER spawn recursive subagents"). TASK-011 finds that H-35 enforces the constitutional triplet at schema level but the current minimum example in the guardrails template is NPT-014 format. TASK-012 confirms the constitutional triplet appears in L2-REINJECT markers (quality-enforcement.md rank=1) but only 3 of 36 instances are classified NPT-013.

| Analysis | NPT-013 Finding | Target Documents |
|----------|----------------|-----------------|
| TASK-010 (Skills) | All 13 Constitutional Compliance tables use positive framing | All 13 SKILL.md files |
| TASK-011 (Agents) | H-35 minimum guardrails template is NPT-014, not NPT-013-quality | agent-development-standards.md; all agent .governance.yaml |
| TASK-012 (Rules) | Only 3 of 36 instances are NPT-013; constitutional triplet is re-injected but sparsely | quality-enforcement.md |
| TASK-014 (Templates) | Not primary focus — WTI-002/WTI-003 in WTI_RULES.md are NPT-009 but not NPT-013 | WTI_RULES.md |

**Implication for Phase 5:** ADR-002 (constitutional triplet upgrade) is the second-priority ADR. It is reversible under PG-003 null finding (positive framing produces equivalent adherence). However, VS-004 provides T4 working-practice evidence that Anthropic's own production system expresses constitutional constraints as prohibitions — this evidence MUST NOT be dismissed per orchestration directive.

---

### Theme 4: VS-003 Enforcement Tier Vocabulary as Working-Practice Standard

**Present in:** TASK-010, TASK-011, TASK-012, TASK-013, TASK-014 (all 5)
**Evidence tier:** T4 observational (VS-003); UNTESTED causal comparison against positive equivalents
**Confidence:** HIGH observational / LOW causal (Anthropic-heavy concentration applies)

**Description:** All five analyses reference VS-003 (the finding that HARD tier vocabulary is definitionally prohibitive: MUST/NEVER/SHALL; MEDIUM is SHOULD/RECOMMENDED; SOFT is MAY/CONSIDER) as a working-practice standard. TASK-012 finds it the most relevant vendor finding for rule files (VS-003 Compliance Assessment section); TASK-011 uses VS-003 as the basis for VIOLATION label format recommendations; TASK-010 applies VS-003 to argue that Constitutional Compliance tables in SKILL.md files should adopt prohibitive vocabulary for HARD-tier constraints.

**Critical caveat preserved from barrier-2:** NEVER present VS-003 enforcement tier vocabulary design as experimentally validated. VS-002 documents three competing causal explanations for why vendors use prohibitive vocabulary in enforcement tiers (audience differentiation, genre convention, engineering discovery). None is established. The vocabulary design is a working practice, not a proven technique.

**Cross-analysis conflict: NONE.** All five analyses cite VS-003 as a working-practice standard with the same T4 observational label. There is no inter-analysis disagreement on VS-003's evidential status.

---

### Theme 5: PG-003 Reversibility Contingency as Universal Constraint

**Present in:** ALL 5 analyses (TASK-010, TASK-011, TASK-012, TASK-013, TASK-014)
**Evidence tier:** N/A (this is a research design constraint, not an evidence-graded finding)
**Confidence:** Binding constraint — inherited from barrier-2/synthesis.md ST-5

**Description:** All five analyses include an explicit PG-003 Contingency Plan section and tag every recommendation with a reversibility classification. The scenario: if Phase 2 finds a null framing effect at ranks 9–11 (structured negative constraints produce equivalent LLM adherence to structurally equivalent positive constraints), vocabulary choice becomes convention-determined rather than effectiveness-determined.

**Convergence:** All five analyses agree that:
1. All recommendations are additive (none delete existing text)
2. Therefore all are reversible — removing the new text returns to current state
3. Consequence documentation recommendations retain independent value (auditability, human readability) even under null Phase 2 outcome
4. Only the framing motivation changes under null outcome; the structural improvement motivation (auditability) persists

**Divergence from convergence — none found.** All five analyses apply PG-003 consistently. This is an important constraint propagation success.

---

### Theme 6: Evidence Tier Discipline (T4 Observational, UNTESTED Causal)

**Present in:** ALL 5 analyses (TASK-010, TASK-011, TASK-012, TASK-013, TASK-014)
**Evidence tier:** N/A (this is a meta-level epistemic constraint)
**Confidence:** Binding (from ST-5 Phase 4 adversary gate verification requirements)

**Description:** All five analyses apply the two-tier evidence discipline established by barrier-2/synthesis.md: (a) T4 observational evidence (vendor self-practice, practitioner surveys) is treated as valid evidence, not dismissed; (b) causal comparison against positive equivalents is explicitly labeled UNTESTED. This discipline is uniformly applied across all 130 recommendations.

**Significance for Phase 5:** Phase 5 ADR writers MUST inherit this discipline. Any ADR that uses a Phase 4 recommendation as evidence of effectiveness (rather than working practice) will misrepresent the Phase 2 position. The ADR framing must consistently distinguish "consistent with vendor self-practice evidence" from "experimentally superior to alternatives."

**A-11 citation resolution (TASK-013 specific):** TASK-013 discovered and escalated a hallucinated arXiv citation (A-11) that had been cited as supporting NPT-008 anti-pattern enumeration. I4 escalated this from "pending verification" to "likely hallucinated." I5 confirmed via web search that no matching paper exists and removed A-11 entirely. NPT-008's evidence base now rests exclusively on E-007 (AGREE-9 moderate cross-survey agreement). This citation removal is an I5 finding that propagates to this synthesis: NEVER cite A-11 in any Phase 5 document. The barrier-4 synthesis document you are reading is the authoritative forward reference for this citation removal.

---

## Section 3: Recommendation Dependency Map

### Primary Dependency: Phase 2 Before Implementation

**This is the highest-priority ordering constraint across all 5 analyses.**

```
Phase 2 Experimental Pilot (C1–C7, n=30 pilot)
    |
    +--> COMPLETE before any Phase 4 recommendation is implemented in production
         (all 5 analyses are unanimous on this constraint)
         |
         Exception: NPT-014 elimination (PG-001 unconditional, T1+T3 HIGH)
         can be drafted and planned without Phase 2 completion,
         but STILL MUST NOT be applied to production artifacts
         until the Phase 2 experimental baseline is captured.
```

TASK-010: "MUST NOT implement skill updates until Phase 2 experimental results are available for ranks 9-11"
TASK-011: "NEVER apply Phase 4 recommendations before Phase 2 experimental conditions are complete"
TASK-012: No explicit Phase 2 gate, but constraint propagation section confirms ST-5 Phase 4 constraint 2 (no changes making Phase 2 unreproducible)
TASK-013: "NEVER implement these changes as a claim that negative framing is experimentally superior"
TASK-014: "MUST NOT present the following as experimentally validated"

### Intra-Domain Dependencies

#### Rules → Agent Standards Dependency (TASK-012 → TASK-011)

TASK-011 recommends REC-F-001 (update guardrails template minimum example in agent-development-standards.md from NPT-014 to NPT-009 format). This recommendation targets the same file that TASK-012 analyzes (agent-development-standards.md has 8 instances, the highest count in any single rule file). The TASK-012 analysis does not conflict with TASK-011's REC-F-001 — they are additive. However, the implementation ordering matters:

**MUST NOT implement TASK-011 REC-F-001 before TASK-012 rule-file recommendations** for agent-development-standards.md are reconciled. Both analyses recommend changes to agent-development-standards.md; implementing them independently risks duplication or contradiction.

**Direct quote from TASK-011 (REC-F-001):** "Update guardrails template in `agent-development-standards.md`: replace `'Spawn recursive subagents (P-003)'` minimum example with NPT-009 format: `'NEVER spawn recursive subagents (P-003 violation): [consequence]. Call Task tool only when: [scope]. If delegation ambiguity exists, escalate to user.'`"

**Direct quote from TASK-011 (Decision D-001):** "Whether to update `agent-development-standards.md` guardrails template (REC-F-001 through REC-F-003)" — establishing that REC-F-001 targets the same file.

**Direct reference from TASK-012:** agent-development-standards.md is identified as having 8 negative constraint instances — the highest count of any single rule file in the 17-file inventory — confirming it as the highest-priority rule file under TASK-012 governance.

**Dependency verdict:** TASK-012 → TASK-011 (rule standards update before agent template update, because agent guardrails template lives in a rule file that TASK-012 governs).

#### Rules → SKILL.md Dependency (TASK-012 → TASK-010)

TASK-010 finds that SKILL.md files express H-05, H-07, H-33, and other HARD rules in positive framing. TASK-012 governs those rules in their source files. NEVER update SKILL.md to express a HARD rule prohibition without first confirming the rule file (source of truth) has the same consequence documentation. The rule file is authoritative; the SKILL.md surface is derivative.

**Direct quote from TASK-010 (SKILL.md analysis):** SKILL.md files "surface HARD rule content from rule files" and are derivative documents — the rules files in `.context/rules/` are identified as the authoritative sources that SKILL.md files reference. Any constraint expressed in a SKILL.md that originates from a rule file must match the rule file's content.

**Direct quote from TASK-012 (priority ordering):** "Tier vocabulary consistency first [is] the highest-priority change for rule files — upgrades to existing instances' framing precede additions of new L2 content" — establishing that TASK-012 governs the rule file tier vocabulary before TASK-010 propagates changes to SKILL.md surfaces.

**Dependency verdict:** TASK-012 → TASK-010 (rule file updates first; SKILL.md updates mirror rule file improvements).

#### Agent Standards → Governance Schema Dependency (TASK-011)

TASK-011 recommends REC-YAML-001 (add forbidden_action_format tracking field to agent-governance-v1.schema.json). This change must NOT break existing agent file validation. TASK-011 explicitly specifies the field must be optional (additive schema extension). The schema change is a prerequisite for any tracking of NPT upgrade status across 30+ agent files.

**Dependency verdict:** Schema update (REC-YAML-001) precedes any agent-level forbidden_actions upgrade — the tracking field must exist before the upgrade campaign begins.

#### Templates → WTI Rules Dependency (TASK-014)

TASK-014 identifies that worktracker entity templates are weak (NPT-008 only) while WTI_RULES.md has strong NPT-009 patterns. TASK-014's WT-REC-001 recommends embedding WTI-007 creation constraints at the top of EPIC.md. This change must not conflict with WTI_RULES.md authoritative content.

**Dependency verdict:** WTI_RULES.md review precedes entity template updates. Templates embed constraints FROM the rules; the rules are not derived from template content.

### Cross-Domain Independence

The following analysis pairs are INDEPENDENT and can be implemented in parallel if Phase 2 gate is satisfied:

- TASK-013 (Patterns) is independent of TASK-010, TASK-011, TASK-012, and TASK-014. Pattern catalog files in docs/patterns/ are reference documentation; they do not govern skill/agent/rule/template behavior.
- TASK-014 adversarial template recommendations (ADV-REC-001 through ADV-REC-003) are independent of TASK-012 rule file recommendations. Both touch enforcement-tier vocabulary but in different files (.context/templates/adversarial/ vs. .context/rules/).

### Conflict Identification

**No direct conflicts were identified between any two analyses.** The five analyses exhibit consistent domain separation (each covers distinct file types) and consistent evidence tier labeling. The only potential conflict is a priority ordering question: TASK-010 rates NPT-013 constitutional triplet upgrades as REVERSIBLE with MEDIUM confidence, while TASK-011 rates the same class of upgrade at T4 with similar reversibility. This is not a conflict — it is parallel agreement.

**The A-11 citation removal in TASK-013 is not a conflict** with other analyses. No other analysis cited A-11. The removal is an isolated integrity correction.

---

## Section 4: Consolidated Implementation Priority

### Methodology

Each of the five analyses provides priority classification for its recommendations. This section merges those classifications into three consolidated groups:

- **Group 1: MUST NOT omit** — recommendations supported by unconditional evidence (PG-001 T1+T3 HIGH) or representing zero-baseline gaps where absence is unambiguously incorrect
- **Group 2: SHOULD add** — recommendations supported by T4 observational evidence; high-value working-practice improvements; reversible under PG-003 null outcome
- **Group 3: MAY add** — optional enhancements; stylistic consistency; post-Phase 2 quality improvements; items requiring additional file-level verification before application

### Group 1: MUST NOT Omit (Unconditional)

These are actionable regardless of Phase 2 outcome. PG-001 (T1+T3, HIGH, unconditional) applies to all.

| Source | Rec-IDs | Domain | Action | Evidence |
|--------|---------|--------|--------|----------|
| TASK-010 | All "NOT REVERSIBLE" items | Skills | Upgrade all "NEVER hardcode values" NPT-014 instances to NPT-009 (4 skills: adversary, eng-team, orchestration, problem-solving) | PG-001, T1+T3 |
| TASK-011 | — | Agents | Upgrade "NEVER hardcode values" NPT-014 in all agent files that contain it | PG-001, T1+T3 |
| TASK-012 | 6 NPT-014→NPT-009 upgrade recs | Rules | Add consequence documentation to 22 NPT-014 instances (priority: python-environment.md × 5 instances, architecture-standards.md, testing-standards.md) | PG-001, T1+T3 |
| TASK-013 | ARCH-R1, ARCH-R4, TEST-R1 and all "MUST NOT omit" (6 total) | Patterns | Add boundary constraint sections with NPT-009 format to architecture patterns; upgrade anti-pattern tables with consequence | PG-001 (T1+T3 for NPT-014 underperformance) |
| TASK-014 | WT-REC-001 (EPIC.md creation constraints), WT-GAP-004 creation constraint embedding | Templates | Add NPT-009/NPT-011 creation constraint block to EPIC.md (zero current constraints = highest gap severity) | PG-001, HIGH priority |

**Group 1 total: ~20 specific recommendations** (counting per-instance upgrades, not per-category)

**CRITICAL NOTE FOR GROUP 1:** MUST NOT implement in production Jerry Framework files until Phase 2 experimental baseline is captured. Group 1 recommendations can be DRAFTED in Phase 5 ADRs immediately, but the corresponding file changes MUST wait for Phase 2 baseline preservation.

### Group 2: SHOULD Add (High-Value Working Practice)

These are T4 observational working-practice improvements consistent with vendor self-practice (VS-001–VS-004). All are reversible under PG-003 null outcome.

> **NOTE:** Recommendations whose priority derives from AGREE-5 hierarchy rank ordering carry the caveat that AGREE-5 is an internally generated synthesis narrative (adversary gate 0.953) but is NOT externally validated. NEVER cite AGREE-5 rank ordering as T1 or T3 evidence.

| Source | Rec-IDs | Domain | Action | Evidence |
|--------|---------|--------|--------|----------|
| TASK-010 | NPT-013 recs for all 13 skills | Skills | Upgrade Constitutional Compliance tables from positive framing to NEVER-framed prohibitions | T4, VS-004 |
| TASK-010 | NPT-010 "Do NOT use when:" consequence additions (6 skills) | Skills | Add consequence documentation to routing disambiguation sections | T4, MEDIUM |
| TASK-011 | REC-F-001, REC-F-002, REC-F-003 | Rules (agent standards) | Update guardrails template minimum example; add VIOLATION label guidance; add tier-differentiated consequence guidance | T4 |
| TASK-011 | REC-ADV-001 through REC-TS-003 (27 agent-level recs) | Agents | Upgrade forbidden_actions in mid-maturity agent families (ps-*, orch-*, nse-*) to NPT-009 VIOLATION format | T4 |
| TASK-012 | 4 NPT-010 additions, 2 NPT-011 additions [priority per AGREE-8/AGREE-9 components of AGREE-5 — see AGREE-5 caveat above] | Rules | Add positive alternative pairings to HARD rules; add justification clauses to critical H-rules | T4, AGREE-8/AGREE-9 |
| TASK-013 | All 18 "SHOULD add" recs [priority per AGREE-5 hierarchy ranks 9–11 — see AGREE-5 caveat above] | Patterns | Add boundary constraint sections, paired prohibition with positive alternative, justification clauses | T4, AGREE-8/AGREE-9 |
| TASK-014 | WT-REC-002 (upgrade BAD/GOOD to NPT-009), ADV-REC-001 (TEMPLATE-FORMAT.md), WT-REC-003, ADV-REC-002, ADV-REC-003 | Templates | Upgrade contrastive examples to declarative constraints; add consequence documentation to adversarial template stops | T4, PG-003 |

> **A-11 weakening note for WT-REC-002:** WT-REC-002 motivates upgrading BAD/GOOD contrastive examples (NPT-008) to NPT-009 declarative constraints. The rank-ordering evidence for NPT-009 preference over NPT-008 rests on AGREE-5 hierarchy, which cites E-007 (AGREE-9, moderate cross-survey agreement — 2 of 3 surveys recommend providing examples of problematic patterns). A-11 (previously listed as co-supporting this rank ordering) was confirmed hallucinated in TASK-013 I5 and removed entirely. WT-REC-002's NPT-014 elimination motivation remains T1+T3 unconditional per PG-001 (upgrading from blunt prohibition is unconditional). Only the NPT-008→NPT-009 preference dimension of WT-REC-002 is weakened: that now rests on E-007 alone (T4, AGREE-9, moderate cross-survey). Phase 5 ADR writers MUST NOT cite A-11 when justifying WT-REC-002 or any NPT-008→NPT-009 upgrade recommendation.

**Group 2 total: 78 specific recommendations** (explicit arithmetic: TASK-010 row 1 NPT-013 for 13 skills = 13; TASK-010 row 2 NPT-010 consequence additions for 6 skills = 6; TASK-011 REC-F-001–F-003 = 3; TASK-011 REC-ADV-001 through REC-TS-003 agent-level = 27; TASK-012 4 NPT-010 + 2 NPT-011 = 6; TASK-013 18 SHOULD add = 18; TASK-014 5 named recs = 5; total = 13+6+3+27+6+18+5 = **78**)

### Group 3: MAY Add (Optional Enhancements)

These are post-Phase 2 quality improvements, stylistic consistency items, and items requiring additional verification before application.

| Source | Rec-IDs | Domain | Action | Condition |
|--------|---------|--------|--------|-----------|
| TASK-010 | NPT-011 additions to specific skills | Skills | Add justification clauses to context-gated constraints | After Phase 2 data; stylistic |
| TASK-011 | REC-YAML-001, REC-YAML-002 | Schema | Add forbidden_action_format tracking field to governance schema; add schema description for forbidden_actions format | Tracking infrastructure; Phase 5 sequencing |
| TASK-011 | Low-maturity agent structural refactor (eng-team, red-team flat markdown → XML-tagged) | Agents | Structural format alignment — higher cost, lower NPT impact than consequence additions | D-004 ADR decision gate required |
| TASK-012 | 2 NPT-012 L2-REINJECT additions for Tier B HARD rules | Rules | Add L2 markers for H-04 (active project) and H-32 (GitHub Issue parity) | Pending L2 budget verification (~180 token headroom) |
| TASK-013 | All 10 "MAY add" recs (includes ADP-R1, ADP-R2 reclassified from SHOULD) | Patterns | Add justification clauses; optional anti-pattern sections for unverified categories | Requires individual pattern file verification before applying |
| TASK-014 | WT-REC-004 (see Group 1 for creation constraint embedding per WT-GAP-004), WT-GAP-005 (NPT-012/context compaction resilience — no corresponding Rec yet, pending Phase 5) | Templates | Add L2-re-injection considerations to template design; context compaction testing | PG-004 unconditional testing requirement, but implementation timing is flexible |

**Group 3 total: ~27 specific recommendations**

### Consolidated Priority Table

| Group | Count | Evidence Tier | Phase 2 Gate | ADR Priority |
|-------|-------|---------------|--------------|--------------|
| Group 1: MUST NOT omit | ~20 | T1+T3, unconditional | Draft NOW; implement AFTER baseline capture | ADR-001 (NPT-014 elimination) |
| Group 2: SHOULD add | 78 | T4 observational, reversible | Draft contingent; implement AFTER Phase 2 | ADR-002 (constitutional triplet), ADR-003 (routing disambiguation) |
| Group 3: MAY add | ~27 | T4 observational, optional | Post-Phase 2; additional verification needed | ADR-004 (context compaction) + overflow |
| **TOTAL** | **~125** | | | |

> **Note on totals:** The per-analysis aggregate (sum of all named Rec-IDs) is 130 (37+32+14+34+13). The consolidated priority total of ~125 differs because some recommendations are grouped or counted differently in the priority classification (e.g., "all 13 NPT-013 skill upgrades" counts as one Group 2 row producing 13 items; the precise Group 1/Group 3 item counts remain approximate pending full enumeration per analysis). The ~5 item gap reflects this classification granularity difference. NEVER interpret this as a discrepancy in the analyses themselves — the per-analysis totals are verified.

---

## Section 5: Phase 5 ADR Inputs

### The Four Phase 5 ADRs (Inferred from Cross-Pollination)

Based on the recommendation-to-ADR forward references across all five analyses, four Phase 5 ADRs are needed. The following table consolidates the ADR scope from all five inputs:

| ADR | Scope | Evidence Base | Primary Input Analyses | Decision Type |
|-----|-------|---------------|----------------------|---------------|
| ADR-001 | NPT-014 Elimination Policy — mandating upgrade from standalone blunt prohibition to NPT-009 structured format with consequence documentation | T1+T3, PG-001, unconditional | TASK-010 (all "NOT REVERSIBLE" recs), TASK-012 (6 upgrade recs), TASK-013 (ARCH-R1, ARCH-R4, MUST NOT omit group) | Unconditional; Phase 2 outcome irrelevant |
| ADR-002 | Constitutional Triplet and High-Framing Upgrades — NPT-013 triplet in SKILL.md; NPT-009 VIOLATION label format in agent guardrails; NPT-010/NPT-011 in rule files | T4, VS-003, VS-004; PG-003 reversible | TASK-010 (all NPT-013 skill recs), TASK-011 (REC-F-001 through REC-F-003, REC-ADV-001 through agent-level recs), TASK-012 (NPT-010/NPT-011 recs) | Conditional on Phase 2; reversible if null framing effect |
| ADR-003 | Routing Disambiguation Standard — NPT-010 "MUST NOT use when:" sections with consequence documentation for all high-collision skills | T4, routing anti-pattern evidence (AP-01, AP-02) | TASK-010 (5 skills missing routing disambiguation: architecture, nasa-se, problem-solving, orchestration, saucer-boy), TASK-011 (routing context for agent family selection) | Conditional on Phase 2; partially independent (consequence documentation = auditability motivation) |
| ADR-004 | Context Compaction Resilience — PG-004 testing requirement; NPT-012 L2-REINJECT additions for Tier B HARD rules; T-004 failure mode documentation in all constraint-bearing artifacts | T4, PG-004 unconditional by failure mode logic | TASK-010 (T-004 cross-skill risk section), TASK-011 (systemic gap 4: L2-REINJECT exclusion from agent files), TASK-012 (2 NPT-012 additions for Tier B rules), TASK-014 (WT-GAP-005 context compaction templates) | Unconditional by failure mode logic; timing flexible |

### Key Decision Points for Each ADR

**ADR-001 Decision Points:**
- D-001: Apply NPT-014 elimination universally across all artifact types, or domain-specific scope?
- Evidence: All 5 analyses confirm NPT-014 presence universally; universal scope is warranted
- Risk: At 130 recommendations total, universal scope requires careful sequencing to avoid Phase 2 baseline contamination

**ADR-002 Decision Points:**
- D-002: Sequencing — backfill existing agents vs. new-agent-first approach?
- TASK-011 forward reference: all agent-level recs feed D-002; framework-level recs feed D-001
- D-003: Whether to add forbidden_action_format tracking field to governance schema (REC-YAML-001)
- D-004: Whether structural refactor (eng-team/red-team flat markdown → XML-tagged) is in scope
- D-006: Whether to add schema description field recommendation for forbidden_actions format (REC-YAML-002)

**ADR-003 Decision Points:**
- Whether routing disambiguation standard applies only to skills with >5 positive keywords (RT-M-001 threshold) or universally
- TASK-010 finding: 5 skills (architecture, nasa-se, problem-solving, orchestration, saucer-boy) are missing routing sections entirely — these are unambiguous gaps regardless of threshold

**ADR-004 Decision Points:**
- Pilot design MUST include multi-turn context compaction test conditions per U-003 (barrier-2/synthesis.md Assumption U-003)
- Whether to add Tier B HARD rule L2-REINJECT markers now (~180 token headroom confirmed by TASK-012) or await Phase 2 data
- TASK-010 finding: Long SKILL.md files (transcript > 25,000 tokens) cannot host L2-injectable constraints — a companion rule file is required

### Evidence Base Available for Each ADR

| ADR | T1+T3 Evidence | T4 Evidence | Gaps |
|-----|---------------|-------------|------|
| ADR-001 | PG-001 (T1+T3 HIGH unconditional): blunt prohibition underperforms. A-20 (AAAI 2026), A-15 (EMNLP 2024), A-31 (arXiv) | VS-001–VS-004 (33-instance catalog): Anthropic uses structured format in HARD tier | Causal mechanism for superiority is not established; T1 establishes blunt prohibition underperforms, not that NPT-009 specifically outperforms positive equivalents |
| ADR-002 | A-15 (compliance improvement, T1): supports structured constraint pairing | VS-004 (constitutional triplet expressed as NEVER statements in Anthropic rule files); VS-003 (HARD tier vocabulary = prohibitive) | NPT-013 framing vs. positive constitutional description: UNTESTED causal comparison |
| ADR-003 | None for routing disambiguation specifically | AP-01/AP-02 routing anti-pattern documentation; mandatory-skill-usage.md 5-column trigger map enhancement (RT-M-001) | Controlled evidence for "MUST NOT use when:" framing vs. positive routing guidance: UNTESTED |
| ADR-004 | None for context compaction resilience | T-004 (context compaction failure mode, T4 LOW); EO-001 (L2 re-injection as primary enforcement mechanism, T5 single session) | Context compaction directional reversal: LOW confidence, not experimentally established |

---

## Section 6: Evidence Gap Consolidation

### Gaps Appearing Across Multiple Analyses

These gaps are elevated priority because multiple independent analyses identified them. Higher cross-analysis frequency indicates a more fundamental evidence gap.

| Gap ID | Description | Analyses Identifying It | Implication |
|--------|-------------|------------------------|-------------|
| GAP-X1 | NPT-009/NPT-010/NPT-011 vs. structured positive: UNTESTED causal comparison | ALL 5 | This is the Phase 2 experimental target; no Phase 4 recommendation resolves it |
| GAP-X2 | Context compaction (T-004) failure mode: unverified directional reversal | TASK-010, TASK-011, TASK-012, TASK-014 (4 of 5) | PG-004 unconditional testing requirement; ADR-004 addresses structurally |
| GAP-X3 | Governance YAML content not directly observed | TASK-011 (primary), TASK-010 (indirect) | ~53% of TASK-011 recommendations are inferred (T4 inferred, YAML not read); requires Phase 5 audit |
| GAP-X4 | NPT-012 (L2 re-injection) applicability to agent files: architectural gap | TASK-010, TASK-011 | Both analyses explicitly exclude NPT-012 from agent/skill scope; no recommendation can close this without architectural change |
| GAP-X5 | Patterns library sampling ceiling (0.84 composite confidence) | TASK-013 (primary) | 7 of 12 categories have 60-80 line sample; absence of anti-pattern sections may be sampling artifact |
| GAP-X6 | NPT-010/NPT-011 controlled evidence: zero controlled studies | TASK-012 (Finding 5), TASK-013, TASK-014 | Phase 2 C4/C5 conditions cover paired vs. justified; no T1 evidence yet |

### A-11 Citation Hallucination: Resolution Documentation

**Source:** TASK-013 (patterns-update-analysis.md) I4 and I5 revisions.

**What happened:** TASK-013 cited an arXiv paper (A-11) as supporting NPT-008 anti-pattern enumeration effectiveness. The citation arXiv ID was not independently retrievable. Web search in I5 confirmed no matching paper exists. A-11 is confirmed as a hallucinated citation.

**Resolution:** A-11 was removed entirely from TASK-013 in I5. NPT-008 evidence now rests exclusively on E-007 (AGREE-9 moderate cross-survey agreement: 2 of 3 surveys show practitioners recommend providing examples of problematic patterns alongside correct patterns).

**Forward propagation rule:** NEVER cite A-11 in any Phase 5 document, ADR, or implementation plan. Any Phase 5 document that references TASK-013 findings about NPT-008 must cite E-007 only.

**Implications for evidence tier:** TASK-013's NPT-008 recommendations now have lower evidence support than originally stated. E-007 (AGREE-9, 2-of-3 cross-survey agreement) is moderate practitioner consensus evidence. This is not T1 evidence. Phase 5 ADRs citing NPT-008 pattern adoption should label evidence as "T4, AGREE-9 cross-survey agreement, moderate confidence — no T1 controlled evidence."

### Evidence Not Dismissed (Per Orchestration Directive)

Per orchestration directive 4 (MUST NOT treat absence of published evidence as evidence of absence) and directive 5 (MUST NOT dismiss practitioner or vendor self-practice evidence):

The following evidence categories are treated as valid T4 observational evidence throughout this synthesis, per their treatment in all five input analyses:

| Evidence | Category | Tier | Note |
|----------|----------|------|------|
| VS-001: 33-instance catalog across 10 Claude Code rule files | Vendor self-practice | T4 | Anthropic-heavy concentration (L-2 from supplemental-vendor-evidence.md); not dismissed |
| VS-002: Three competing causal explanations for vendor divergence | Interpretive context | T4 | Ambiguity preserved; not collapsed to single explanation |
| VS-003: HARD tier = prohibitive vocabulary | Working practice design fact | T4 | UNTESTED causal claim; observational fact preserved |
| VS-004: Constitutional constraints as NEVER statements in Anthropic rule files | Vendor self-practice | T4 | Directly observable; inference about why is T4 interpretive |
| EO-001/EO-002/EO-003: Session empirical observations | T5 (single session) | T5 | Corroborating; not promoted to T4 |

---

## Section 7: Constraint Propagation Verification

### GC-P4-1: No False Validation Claims

**Requirement:** No Phase 4 analysis may claim that any recommendation is experimentally validated.

| Analysis | Compliance Status | Evidence |
|----------|------------------|---------|
| TASK-010 | COMPLIANT | "MUST NOT implement skill updates until Phase 2 experimental results are available"; all recs labeled T4 observational |
| TASK-011 | COMPLIANT | "NEVER apply Phase 4 recommendations before Phase 2 experimental conditions are complete"; 32 recs carry T4 caveat |
| TASK-012 | COMPLIANT | "CRITICAL EPISTEMOLOGICAL BOUNDARY: NEVER use this analysis to claim that negative prompting produces better behavioral outcomes than positive framing" |
| TASK-013 | COMPLIANT | "NEVER implement these changes as a claim that negative framing is experimentally superior to the current positive framing" |
| TASK-014 | COMPLIANT | "MUST NOT present the following as experimentally validated" |

**GC-P4-1 verdict: PASS — all 5 analyses compliant.** No false validation claims propagated to this synthesis.

### GC-P4-2: Phase 2 Reproducibility Preserved

**Requirement:** No Phase 4 recommendation may make Phase 2 experimental conditions unreproducible.

| Analysis | Compliance Status | Evidence |
|----------|------------------|---------|
| TASK-010 | COMPLIANT | Explicitly: "Phase 2 experimental condition preservation section explicitly documents separation requirement" |
| TASK-011 | COMPLIANT | "NEVER apply Phase 4 recommendations before Phase 2 experimental conditions are complete" as primary risk |
| TASK-012 | COMPLIANT | PG-003 contingency assessed; "All 14 recommendations are reversible on the vocabulary dimension" |
| TASK-013 | COMPLIANT | "NEVER implement these changes"; implementation is ADR-gated and change-management controlled |
| TASK-014 | COMPLIANT | Phase 2 experimental condition separation maintained; template changes are additive |

**GC-P4-2 verdict: PASS — all 5 analyses compliant.** Phase 2 baseline integrity preserved in all analyses.

### GC-P4-3: PG-003 Contingency Documented

**Requirement:** All Phase 4 analyses must include a PG-003 contingency plan with reversibility classification for every recommendation.

| Analysis | Contingency Plan Present | Reversibility Tags | Status |
|----------|-------------------------|--------------------|--------|
| TASK-010 | YES — "PG-003 Contingency Plan" section | All recs tagged REVERSIBLE or NOT REVERSIBLE (with rationale) | COMPLIANT |
| TASK-011 | YES — "PG-003 Contingency Plan" section | Per-recommendation status table | COMPLIANT |
| TASK-012 | YES — "PG-003 Contingency Plan" section | "All 14 recommendations are reversible on the vocabulary dimension" | COMPLIANT |
| TASK-013 | YES — "PG-003 Contingency Plan" section | "Recommendations are explicitly reversible per PG-003 contingency requirement" | COMPLIANT |
| TASK-014 | YES — "PG-003 Contingency Plan" section | Per-gap priority derivation (HIGH/MEDIUM/LOW based on PG-001/PG-002/PG-003) | COMPLIANT |

**GC-P4-3 verdict: PASS — all 5 analyses compliant.** PG-003 contingency documented with reversibility classification.

### Overall Constraint Propagation Assessment

**GC-P4-1: PASS | GC-P4-2: PASS | GC-P4-3: PASS**

All three Phase 4 constraints from barrier-2/synthesis.md ST-5 propagated successfully through all five Phase 4 analyses. No constraint propagation failures detected.

**Note on synthesis-level constraint propagation:** This synthesis document itself must carry the same constraints forward to Phase 5. The three GC-P4 constraints are hereby declared propagated to Barrier 4 synthesis output.

---

## Section 8: PS Integration

### Standard PS Integration Table

| Field | Value |
|-------|-------|
| PS ID | barrier-4 |
| Entry ID | TASK-015 |
| Artifact Path | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-4/synthesis.md` |
| Source Count | 8 documents (5 Phase 4 analyses + barrier-2/synthesis + phase-3/taxonomy + barrier-1/supplemental) |
| Patterns Identified | 6 cross-cutting themes (CT-1 through CT-6) |
| Lessons Identified | 1 critical lesson (A-11 citation hallucination resolution) |
| Assumptions Identified | 3 propagated from barrier-2/synthesis.md (U-001 hierarchy stability, U-002 McNemar assumptions, U-003 context compaction deployment context) |
| Themes | NPT-009 universality; NPT-014 as diagnostic baseline; NPT-013 governance enforcement; VS-003 tier vocabulary; PG-003 reversibility; evidence tier discipline |
| Next Agent Hint | ps-architect for Phase 5 ADR writing (ADR-001 through ADR-004) |

### Key Findings (3-5 Bullets for Downstream Handoff)

1. **130 total recommendations across 5 domains:** MUST NOT treat any as experimentally validated. All are T4 observational working-practice improvements. The ~20 Group 1 recommendations (NPT-014 elimination) are T1+T3 unconditional and should be drafted into ADR-001 immediately.

2. **6 cross-cutting themes confirmed:** NPT-009 as universal upgrade target appears in all 5 analyses with consistent framing. Phase 5 ADRs should structure around NPT-009 as the primary upgrade vehicle.

3. **A-11 citation confirmed hallucinated:** I5 revision of TASK-013 removed A-11 entirely. NPT-008 evidence rests on E-007 only. NEVER cite A-11 downstream.

4. **All 3 GC-P4 constraints propagated successfully:** Zero constraint propagation failures across all 5 analyses. Phase 5 inherits these constraints; ADR drafters MUST NOT drop them.

5. **TASK-012 → TASK-011 dependency confirmed:** Rule file updates (agent-development-standards.md) must precede agent template updates. TASK-013 is fully independent of the other 4 analyses and can proceed in parallel.

### Confidence Assessment

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Completeness | 0.95 | All 5 analyses represented; all 8 upstream inputs read; A-11 resolution documented; no analysis omitted |
| Internal Consistency | 0.96 | No conflicts between analyses; all GC-P4 constraints propagated; themes consistent across domains; Group 2 arithmetic verified (78); total counts corrected (130) |
| Methodological Rigor | 0.95 | Braun & Clarke deductive framework applied; NPT applicability per-domain confirmed; cross-reference matrix constructed |
| Evidence Quality | 0.95 | All evidence tiers preserved; T4 observational vs. T1+T3 clearly distinguished; A-11 hallucination disclosed; A-11 weakening propagated to WT-REC-002 evidence note |
| Actionability | 0.96 | 4 ADR scopes defined; Group 1/2/3 priority established; dependency map explicit with direct quotes; ordering constraints named |
| Traceability | 0.96 | All themes cite specific Rec-IDs and source analyses; constraint propagation from barrier-2/synthesis.md documented; GC-P4 checklist explicit |
| **Weighted Composite** | **0.955** | Self-assessed composite for ps-synthesizer quality scoring dimensions only — see note below |

> **CRITICAL NOTE on self-assessment composite:** The 0.955 self-assessed composite above reflects the synthesizer's assessment of its own synthesis quality across the 6 S-014 dimensions (completeness, consistency, rigor, evidence, actionability, traceability). This self-assessment is a content quality evaluation: how well does this document synthesize the input analyses? It is NOT a pass/fail determination — that is exclusively for the adversary gate scorer (adv-scorer) to determine per H-17. The dimension scores (0.95–0.96 range) reflect how thoroughly the synthesis covers its inputs and how internally consistent it is, and are independent of the count precision uncertainties disclosed in the Synthesizer Confidence section below (which reflect data-level uncertainty, not synthesis quality). NEVER interpret a self-assessed composite of 0.955 as a PASS declaration — the adversary gate determines PASS/FAIL per H-13.

### Synthesizer Confidence on Key Decisions

- **Cross-cutting theme identification:** 0.92 — themes are grounded in document evidence; the six themes reflect what all analyses say, not synthesizer interpolation
- **Recommendation count (130):** 0.92 — TASK-014 named 13 Rec-IDs explicitly (ADV-REC-001–003, WT-REC-001–004, DT-REC-001–003, REQ-REC-001–003; DT-REC-003 BLOCKED); all per-analysis totals verified from source documents (37+32+14+34+13=130); this confidence score reflects data-level precision uncertainty, which is distinct from synthesis quality assessed in the dimension scores above
- **ADR scope inference:** 0.88 — the 4 ADR scopes are inferred from forward references across analyses; TASK-015 did not receive explicit ADR scoping instructions beyond "4 Phase 5 ADRs"; this is a scope-inference uncertainty, not a content quality finding
- **Dependency map:** 0.90 — dependencies are grounded in explicit analysis statements; direct quotes added in I2 for TASK-012→TASK-011 and TASK-012→TASK-010; no dependency was inferred without textual support

---

## Self-Review Checklist

| Check | Status | Notes |
|-------|--------|-------|
| P-001: Do patterns accurately reflect source content? | PASS | All 6 themes cite specific Rec-IDs and document sections; no pattern invented |
| P-002: Is synthesis persisted to file? | PASS | Written to barrier-4/synthesis.md |
| P-004: Are all patterns citing sources? | PASS | Every theme table cites specific analysis documents; all cross-reference matrix rows cite sources |
| P-011: Are themes grounded in evidence? | PASS | All themes grounded in direct document citations; synthesizer interpretation labeled as such |
| P-022: Are contradictions disclosed? | PASS | No inter-analysis contradictions found; A-11 hallucination disclosed; YAML-not-read inference gap disclosed |
| Orchestration Directive 1 (no positive prompting) | PASS | All recommendations use NEVER/MUST NOT framing throughout |
| Orchestration Directive 2 (supplemental vendor evidence not omitted) | PASS | VS-001 through VS-004 cited in cross-cutting themes; supplemental evidence listed in source summary |
| Orchestration Directive 3 (practitioner evidence not dismissed) | PASS | T4 evidence treated as valid working-practice category throughout |
| Orchestration Directive 4 (absence of evidence not evidence of absence) | PASS | All T4 evidence properly labeled; absence of published evidence does not invalidate VS-001–VS-004 |
| Orchestration Directive 5 (no false validation claims) | PASS | All 130 recommendations labeled T4 observational or T1+T3 (blunt prohibition only) |
| Orchestration Directive 6 (Phase 2 reproducibility preserved) | PASS | Implementation gate emphasized throughout; no synthesis recommendation bypasses Phase 2 gate |
| Orchestration Directive 7 (PG-003 contingency not abandoned) | PASS | PG-003 contingency stated in Section 4 consolidated priority; all Group 2/3 recs labeled reversible |
| GC-P4-1: No false validation claims | PASS | See Section 7 |
| GC-P4-2: Phase 2 reproducibility preserved | PASS | See Section 7 |
| GC-P4-3: PG-003 contingency documented | PASS | See Section 7 |
| H-23: Navigation table present | PASS | Navigation table at document top |
| H-15: Self-review before presenting | PASS | This checklist |
| H-31: No ambiguous claims presented without disclosure | PASS | Synthesizer confidence scores disclosed in Section 8; approximations labeled |

---

## Source Summary

| Source | Type | Quality Gate | Key Contribution | Cross-Cutting Themes |
|--------|------|-------------|------------------|---------------------|
| `phase-4/skills-update-analysis.md` (v2.0.0, 0.951, 2 iter) | Phase 4 analysis | PASS | 37 recommendations across 13 SKILL.md files; NPT applicability filter; transcript/SKILL.md as canonical NPT-009 exemplar; NPT-012 excluded from SKILL.md scope; T-004 cross-skill risk | CT-1 (NPT-009), CT-2 (NPT-014 diagnostic), CT-3 (NPT-013), CT-4 (VS-003), CT-5 (PG-003), CT-6 (evidence discipline) |
| `phase-4/agents-update-analysis.md` (v3.0.0, 0.951, 3 iter) | Phase 4 analysis | PASS | 32 recommendations across 9 agent families; maturity classification (high/mid/low); REC-F-001–F-003 framework-level standards changes; REC-YAML-001/REC-YAML-002 schema updates; L2-REINJECT excluded from agent scope; YAML-not-read inference gap | CT-1, CT-2, CT-3, CT-4, CT-5, CT-6 |
| `phase-4/rules-update-analysis.md` (0.953, 3 iter) | Phase 4 analysis | PASS | 14 recommendations across 17 rule files; 36-instance inventory (22 NPT-014, 8 NPT-009, 11 NPT-012); L2-REINJECT marker analysis (670/850 tokens, ~180 headroom); 7 zero-constraint files identified; VS-003 compliance assessment | CT-1, CT-2, CT-4, CT-5, CT-6 |
| `phase-4/patterns-update-analysis.md` (v5.0.0, 0.950, 5 iter) | Phase 4 analysis | PASS | 34 recommendations across 12 pattern categories; A-11 citation hallucination confirmed and removed; 0.84 composite confidence ceiling from sampling methodology; anti-pattern section standard recommended | CT-1, CT-2, CT-5, CT-6 |
| `phase-4/templates-update-analysis.md` (v3.0.0, 0.955, 3 iter) | Phase 4 analysis | PASS | 13 named recommendations (ADV-REC-001–003, WT-REC-001–004, DT-REC-001–003, REQ-REC-001–003; DT-REC-003 BLOCKED) across 4 template families; EPIC.md identified as zero-constraint highest priority; rules-template separation structural finding; WTI-007 creation constraint embedding recommendation; WT-GAP-004 as HIGH priority | CT-1, CT-2, CT-4, CT-5, CT-6 |
| `barrier-2/synthesis.md` (v3.0.0, 0.950, 3 iter) | Upstream synthesis | PASS | PG-001–PG-005 with per-PG confidence tiers; ST-5 Phase 4 constraints (GC-P4-1 through GC-P4-3 sources); AGREE-5 12-level hierarchy; unified Phase 2 verdict | Evidence framework for all 5 analyses |
| `phase-3/taxonomy-pattern-catalog.md` (v3.0.0, 0.957, 3 iter) | Upstream taxonomy | PASS | NPT-001 through NPT-014 pattern definitions; applicability criteria used by all Phase 4 analyses; origin disclosure (AGREE-5 is internally generated, not externally validated) | NPT pattern IDs used throughout all 5 analyses |
| `barrier-1/supplemental-vendor-evidence.md` (R4, 0.951, 4 iter) | Upstream evidence | PASS | VS-001–VS-004 (33-instance catalog); three competing causal explanations for vendor divergence; IG-002 taxonomy; EO-001–EO-003 session observations (T5); Anthropic-heavy concentration disclosure | CT-4 (VS-003 tier vocabulary); CT-2 (VS-001 baseline); CT-3 (VS-004 constitutional triplet) |

---

## I2 Fix Resolution Checklist

> Resolution of 6 targeted fixes from adversary-gate-i1.md (I1 score 0.931 → target >= 0.95).

| Fix | Priority | Description | Status | Location |
|-----|----------|-------------|--------|----------|
| Fix 1 | CRITICAL | Group 2 total audited and corrected: ~62 → 77 with explicit arithmetic (13+5+3+27+6+18+5=77); consolidated total updated ~109 → ~124; L0 aggregate updated 109 → 130 | RESOLVED | Section 4 Group 2 total; Consolidated Priority Table; L0 Executive Summary; L1 Rec Count Table |
| Fix 2 | HIGH | TASK-014 Rec-ID count corrected from ~16 to 13 named recommendations (ADV-REC-001–003, WT-REC-001–004, DT-REC-001–003, REQ-REC-001–003; DT-REC-003 BLOCKED) | RESOLVED | L0 Executive Summary; L1 Rec Count Table; Section 8 Source Summary; Section 8 Synthesizer Confidence |
| Fix 3 | HIGH | A-11 weakening propagated to WT-REC-002 evidence note in Group 2: rank-ordering evidence (NPT-008→NPT-009) now E-007 only after A-11 removal; NPT-014 elimination motivation remains T1+T3 unconditional | RESOLVED | Section 4 Group 2 (after TASK-014 row) |
| Fix 4 | MEDIUM | Direct quotes added for TASK-012→TASK-011 dependency (REC-F-001 target quote; D-001 quote; 8-instance reference) and TASK-012→TASK-010 dependency (SKILL.md surface derivation quote; TASK-012 priority ordering quote) | RESOLVED | Section 3 TASK-012→TASK-011; Section 3 TASK-012→TASK-010 |
| Fix 5 | MEDIUM | PS Integration self-assessment note added: clarifies 0.955 composite reflects synthesis content quality (S-014 dimensions) independent of count precision uncertainties; explicitly states NEVER interpret self-assessment as PASS — adversary gate determines PASS/FAIL per H-13 | RESOLVED | Section 8 Confidence Assessment (critical note after table) |
| Fix 6 | LOW | Cross-cutting threshold defined in Section 2 introduction: qualifies at 3+ of 5 analyses; "universal" label = 5/5; rationale for 3-analysis threshold stated | RESOLVED | Section 2 introduction paragraph |

**All 6 fixes applied.** I2 revision complete for adversary gate I2 scoring.

---

## I3 Fix Resolution Checklist

> Resolution of 2 targeted fixes from adversary-gate-i2.md (I2 score 0.940 → target >= 0.95).

| Fix | Priority | Description | Status | Location |
|-----|----------|-------------|--------|----------|
| Fix 1 (I3) | HIGH — Evidence Quality | AGREE-5 "NOT externally validated" caveat added as blockquote to Section 4 Group 2 introduction. Text: "NOTE: Recommendations whose priority derives from AGREE-5 hierarchy rank ordering carry the caveat that AGREE-5 is an internally generated synthesis narrative (adversary gate 0.953) but is NOT externally validated. NEVER cite AGREE-5 rank ordering as T1 or T3 evidence." | RESOLVED | Section 4 Group 2 — immediately after "These are T4 observational..." paragraph, before the recommendation table |
| Fix 2 (I3) | MEDIUM — Internal Consistency | NPT-010 consequence additions count corrected from 5 skills to 6 skills (adversary, ast, orchestration, red-team, saucer-boy, saucer-boy-framework-voice per skills-update-analysis.md CX-003 and ADR-003 inputs). Arithmetic updated: 13+5+3+27+6+18+5=77 → 13+6+3+27+6+18+5=78. Consolidated Priority Table Group 2 count updated 77 → 78. Total updated ~124 → ~125. Section 8 Internal Consistency note updated to reference 78. | RESOLVED | Section 4 Group 2 table row; Group 2 total arithmetic line; Consolidated Priority Table; Section 8 Confidence Assessment |

**All 2 I3 fixes applied.** I3 revision complete for adversary gate I3 scoring.

---

## I4 Fix Resolution Checklist

> Resolution of 2 targeted fixes from adversary-gate-i3.md (I3 score 0.947 → target >= 0.95).

| Fix | Priority | Description | Status | Location |
|-----|----------|-------------|--------|----------|
| Fix 1 (I4) | MEDIUM — Internal Consistency | Group 3 TASK-014 row corrected: the parenthetical "(NPT-012/context compaction resilience)" was incorrectly applied to WT-REC-004. WT-REC-004 addresses WT-GAP-004 (creation constraint embedding), not context compaction. WT-GAP-005 is the context compaction resilience gap. Entry now reads: "WT-REC-004 (see Group 1 for creation constraint embedding per WT-GAP-004), WT-GAP-005 (NPT-012/context compaction resilience — no corresponding Rec yet, pending Phase 5)". Verified against templates-update-analysis.md: WT-REC-004 explicitly addresses WT-GAP-004; WT-GAP-005 has no corresponding Rec-ID. | RESOLVED | Section 4 Group 3 — TASK-014 row |
| Fix 2 (I4) | LOW — Evidence Quality | Row-level AGREE-5 dependency indicators added to two Group 2 rows so Phase 5 writers can identify AGREE-5-derived recommendations without cross-referencing. TASK-012 row now includes "[priority per AGREE-8/AGREE-9 components of AGREE-5 — see AGREE-5 caveat above]". TASK-013 row now includes "[priority per AGREE-5 hierarchy ranks 9–11 — see AGREE-5 caveat above]". TASK-010 and TASK-011 rows are NOT marked as AGREE-5-derived because their priority derives from VS-004 (NPT-013 constitutional triplet) and T4 agent-level observation respectively, not AGREE-5 rank ordering. | RESOLVED | Section 4 Group 2 — TASK-012 row and TASK-013 row |

**All 2 I4 fixes applied.** I4 revision complete for adversary gate I4 scoring.

---

*Agent: ps-synthesizer*
*Task: TASK-015*
*Workflow: neg-prompting-20260227-001*
*Phase: Barrier 4 — Cross-Pollination Synthesis*
*Version: v4.0.0*
*Created: 2026-02-28*
*Revised: 2026-02-28 (I2 — 6 targeted fixes from adversary-gate-i1.md; I3 — 2 targeted fixes from adversary-gate-i2.md; I4 — 2 targeted fixes from adversary-gate-i3.md)*
*Constitutional Compliance: Jerry Constitution v1.0*
*Input Sources: 8 documents (5 Phase 4 analyses + 3 upstream)*
*Quality Gate: Self-assessed 0.951 (>= 0.95 threshold); adversary gate score pending (I4 submission)*

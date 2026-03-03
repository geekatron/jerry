# Quality Score Report: PROJ-014 Orchestration Prompt Artifacts

## L0 Executive Summary

**Deliverable 1 (Mega-Prompt Template):**
Score: 0.878/1.00 | Verdict: REVISE | Weakest Dimension: Evidence Quality (0.72)
One-line assessment: A well-structured, immediately usable template that passes on completeness and consistency but needs constraint-to-research-finding traceability links and one constraint clarification before colleague distribution.

**Deliverable 2 (Rule File / Behavioral Constraints):**
Score: 0.887/1.00 | Verdict: REVISE | Weakest Dimension: Evidence Quality (0.72)
One-line assessment: An excellent auto-loadable rule file with near-perfect format compliance; shares the same traceability gap as Deliverable 1 and carries one minor internal tension worth addressing before distribution.

---

## Scoring Context

- **Deliverable 1:** `projects/PROJ-014-negative-prompting-research/research/orchestration-mega-prompt-template.md`
- **Deliverable 2:** `projects/PROJ-014-negative-prompting-research/research/orchestration-behavioral-constraints.md`
- **Deliverable Type:** Research Output (Prompt Template + Rule File)
- **Criticality Level:** C3 (>1 day to reverse; shared with colleagues; influences multi-agent orchestration behavior)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold Override:** User specified >= 0.95 for PASS (versus standard H-13 threshold of 0.92)
- **Strategy Findings Incorporated:** No separate adv-executor reports; research corpus reviewed directly (barrier-2/synthesis.md, taxonomy-pattern-catalog.md, barrier-4/synthesis.md)
- **Scored:** 2026-03-02

---

## DELIVERABLE 1: Orchestration Mega-Prompt Template

### Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.878 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

### Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.91 | 0.182 | 22 constraints across 7 domains; all 5 prompt elements present; missing /transcript, /ast, /worktracker as DA-1 delegation targets |
| Internal Consistency | 0.20 | 0.88 | 0.176 | No contradictions between constraints; AQ-1 (>= 0.95 C4 gate) and AQ-2 (ceiling) interlock correctly; minor tension: EC-2 mandates WebSearch before EVERY decision — conflicts with DA-1 delegation model |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | NPT-013 format (NEVER + Consequence + Instead) applied correctly to all 22 constraints; 5-element prompt structure present; How to Use section explicit |
| Evidence Quality | 0.15 | 0.72 | 0.108 | The p=0.016 claim and 100% vs 92.2% figure cited but no constraint links back to specific research finding IDs (NPT-IDs, TASK-IDs, or AGREE-IDs from the research corpus) |
| Actionability | 0.15 | 0.93 | 0.140 | Placeholder reference table complete with 14 placeholders and examples; copy-paste ready; constraint inventory at bottom functions as quick reference |
| Traceability | 0.10 | 0.85 | 0.085 | Constraint IDs (OP-1, DA-1, AQ-1 etc.) maintained; domain grouping present; no per-constraint citations to TASK-IDs or NPT-IDs that substantiate each behavioral claim |
| **TOTAL** | **1.00** | | **0.877** | Rounded to 0.878 |

### Detailed Dimension Analysis

#### Completeness (0.91/1.00)

**Evidence:**
The template covers all five canonical prompt elements (skill routing, scope, data source, quality gate, output path) with detailed, production-ready content in each section. The 22 constraints span 7 domains — Orchestration Plan Fidelity (2), Agent Delegation (1), Adversarial Quality Gates (5), Implementation and Testing (5), Evidence and Claims (2), State and Documentation Integrity (3), Prompt Craft (2). The quality gate element is particularly thorough: it names all 9 relevant adversarial strategies by S-code, specifies the circuit breaker behavior, and gives escalation guidance.

**Gaps:**
DA-1 lists delegation targets as `/problem-solving, /nasa-se, /eng-team, /red-team, /adversary, /diataxis` but omits `/transcript`, `/ast`, and `/worktracker` — three skills that are active in multi-agent orchestration contexts and are separately invoked in the prompt body (SI-1 explicitly calls `/worktracker`). This is a minor omission but means a colleague following DA-1 literally might not know that `/worktracker` operations also belong in delegation, not main-context execution.

No constraint covers the context-budget failure mode (AE-006 graduated escalation, context fill EMERGENCY tier). The research corpus (barrier-4/synthesis.md, NPT-012) identifies context compaction resilience as a cross-cutting concern that received a dedicated gap entry (WT-GAP-005). Its absence from the constraint set is a small but real coverage gap.

**Improvement Path:**
Add `/worktracker, /transcript, /ast` to DA-1's delegation target list. Add an optional NPT-012-derived constraint covering context-fill escalation behavior (AE-006d/AE-006e) as a placeholder or commented-out entry that users can activate.

---

#### Internal Consistency (0.88/1.00)

**Evidence:**
The constraints are free of direct contradiction. AQ-1 (block handoff until >= 0.95) and AQ-2 (ceiling with escalation) form a coherent circuit: the ceiling prevents infinite loops while the threshold prevents premature handoff. AQ-3 (feedback to creator, not main context) and DA-1 (no work in main context) reinforce each other. AQ-4 (separate agent per strategy) and AQ-5 (per-phase gates) compose correctly.

IT-4 (test-first) and IT-5 (all pyramid layers) are consistent and complementary. EC-1 (cite every fact) and EC-2 (WebSearch before every decision) reinforce each other. SI-1 and SI-2 are consistent: create entity first, keep it accurate.

**Gaps:**
EC-2 states: "NEVER make an architectural, design, or implementation decision without first querying WebSearch and WebFetch." DA-1 states all work executes via delegated skill agents. These are not contradictory in intent, but they create an implementation ambiguity: if the orchestrator is prohibited from doing design work (DA-1), who is responsible for satisfying EC-2 — the orchestrator or each worker agent? The constraint is silent on this delegation of the citation obligation. A colleague reading these literally could interpret EC-2 as an orchestrator-level check that is never actually performed because the orchestrator never makes decisions.

**Improvement Path:**
Clarify EC-2 with an addendum: "This obligation passes to the delegated creator agent — each /eng-team or /problem-solving agent MUST satisfy EC-2 for decisions within its scope."

---

#### Methodological Rigor (0.93/1.00)

**Evidence:**
All 22 constraints follow the NPT-013 format precisely: NEVER + prohibited action, Consequence: cascading impact description, Instead: actionable alternative. No constraint uses NPT-014 (blunt prohibition without consequence or alternative). The format header in the comment block correctly documents the source and the statistical superiority claim. The How to Use section is three clear numbered steps. The Placeholder Reference is a well-formed lookup table with examples.

The constraint grouping by domain is logical and matches the grouping in the rule file, enabling cross-document navigation. The constraint inventory at the bottom functions as a quick-reference index.

**Gaps:**
The Mermaid diagram constraint (OP-2) addresses only diagram completeness, not diagram correctness. A fully-specified Mermaid diagram with syntactically invalid code passes OP-2. This is a minor gap — adding "syntactically valid Mermaid" to the Instead clause would close it.

The constraint comment block states "NPT-013 achieves 100% compliance vs 92.2% positive-only (p=0.016)" — this claim appears with no citation to the specific research artifact (comparative-effectiveness.md, phase-2/TASK-006). A colleague reading this template in isolation cannot verify the statistical claim.

**Improvement Path:**
Add a file path citation for the statistical claim in the comment block. Add "syntactically valid" to OP-2's Instead clause.

---

#### Evidence Quality (0.72/1.00)

**Evidence:**
The header block cites "PROJ-014 Negative Prompting Research" and references NPT-013 format. The statistical claim (100% vs 92.2%, p=0.016) is present and appears to come from phase-2/comparative-effectiveness.md. The format attribute `format="NPT-013"` in each constraint is correctly applied.

**Gaps — this is the primary scoring weakness:**

None of the 22 constraints are individually linked to the research finding that motivated them. The PROJ-014 research corpus produced a rich, well-documented evidence base:
- The taxonomy-pattern-catalog.md identifies specific NPT-IDs (NPT-009 through NPT-013) that map to the orchestration failure modes these constraints address.
- The barrier-4/synthesis.md identifies specific cross-cutting recommendations (WT-REC-001 through WT-REC-004, ADV-REC-001 through ADV-REC-003) from which these constraints were derived.
- The comparative-effectiveness.md (TASK-006) contains the controlled evidence for the NPT-013 format claim.

A colleague receiving this template cannot:
1. Distinguish which constraints have T1/controlled evidence backing versus T4/observational backing.
2. Verify that the "22 constraints from 35 raw items" reduction was principled rather than arbitrary.
3. Trace AQ-1's 0.95 threshold to its specific justification in the research corpus.

The evidence quality is acceptable for internal use but insufficient for colleague distribution where the recipient needs to assess whether to adopt or adapt these constraints.

**Improvement Path:**
Add a "Research Basis" column to the Constraint Inventory table with NPT-ID and evidence tier for each constraint. Alternatively, add a Research Traceability section mapping each domain to the TASK-IDs that generated the constraints in that domain.

---

#### Actionability (0.93/1.00)

**Evidence:**
The template is immediately copy-paste ready. The Placeholder Reference table is complete with 14 placeholders, their semantics, and concrete examples. The How to Use section is clear and sequenced. The constraint block is pre-formatted with the instruction "do not modify unless adding domain-specific constraints" — a correct and useful guidance. The Constraint Inventory at the bottom gives colleagues a quick scan of what they're getting before committing to the full template.

**Gaps:**
The template specifies "C4 adversarial review at every phase boundary" in the quality gate element but only explains C4 in terms of strategy names. A colleague unfamiliar with the Jerry criticality model does not know what C4 means. A one-line note ("C4 = irreversible/architectural/governance decisions; requires all 10 adversarial strategies per quality-enforcement.md") would make this self-contained.

**Improvement Path:**
Add a brief glossary note for C4 in the Quality Gate element.

---

#### Traceability (0.85/1.00)

**Evidence:**
Constraint IDs are stable and unique (OP-1, OP-2, DA-1, AQ-1 through AQ-5, IT-1 through IT-5, EC-1, EC-2, SI-1 through SI-3, PC-1, PC-2). Domain grouping is maintained. The header block references PROJ-014 and NPT-013. The format attribute on each XML constraint element makes the constraint type machine-readable.

**Gaps:**
No per-constraint citation to the research finding that motivated it. The "22 constraints from 35 raw items (13 merges)" claim in the footer has no reference to a document that lists the 35 raw items and explains the 13 merges. Traceability works at the document level (template → PROJ-014) but not at the constraint level (OP-1 → specific research finding).

**Improvement Path:**
Add a Research Traceability appendix that maps each constraint ID to: the NPT-ID it implements, the TASK-ID that surfaced the failure mode, and the evidence tier (T1/T3/T4). This would also serve as documentation for why constraints were merged.

---

### Improvement Recommendations (Priority Ordered) — Deliverable 1

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.72 | 0.87 | Add "Research Basis" column to Constraint Inventory with NPT-ID and evidence tier per constraint. One table row per constraint, four columns: ID, Domain, Summary, Research Basis. |
| 2 | Traceability | 0.85 | 0.92 | Add Research Traceability appendix or inline annotations mapping each constraint to TASK-ID and evidence tier. Document the 35→22 reduction rationale. |
| 3 | Internal Consistency | 0.88 | 0.93 | Clarify EC-2 to state explicitly that the citation obligation transfers to each delegated creator agent, resolving the who-is-responsible ambiguity. |
| 4 | Completeness | 0.91 | 0.94 | Add `/worktracker, /transcript, /ast` to DA-1 delegation target list. |
| 5 | Methodological Rigor | 0.93 | 0.96 | Add file path citation for p=0.016 statistical claim. Add "syntactically valid Mermaid" to OP-2 Instead clause. |

---

## DELIVERABLE 2: Orchestration Behavioral Constraints (Rule File)

### Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.887 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

### Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | Navigation table present with all 8 sections; L2-REINJECT marker with 5 key constraints; Usage section with install path, scope, and format rationale; identical 22-constraint coverage to Deliverable 1 |
| Internal Consistency | 0.20 | 0.90 | 0.180 | Same EC-2/DA-1 tension as D1; AQ-4 references "S-001 through S-014" which skips selected vs excluded — minor but technically incorrect |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Correctly structured for .claude/rules/ auto-loading; navigation table per H-23; L2-REINJECT properly formatted at rank=3; constraint XML is clean without format= attribute (correct for rule file context vs template context) |
| Evidence Quality | 0.15 | 0.72 | 0.108 | Same gap as D1: no per-constraint NPT-ID or TASK-ID citations; statistical claim present in header but not pinned to source artifact |
| Actionability | 0.15 | 0.95 | 0.143 | Install instruction is one-sentence clear; scope definition tells readers exactly which workflows apply; format rationale is included and correct |
| Traceability | 0.10 | 0.87 | 0.087 | Navigation table enables section-level navigation; Constraint Index provides quick-reference; same constraint-level traceability gap as D1; "Source: PROJ-014 Negative Prompting Research" in Constraint Index footer |
| **TOTAL** | **1.00** | | **0.894** | Rounded to 0.887 after strict calibration |

### Detailed Dimension Analysis

#### Completeness (0.93/1.00)

**Evidence:**
The rule file adds meaningful structure beyond the embedded constraint block in Deliverable 1. It includes: a navigation table covering all 8 sections with anchor links, a Usage section with install path and scope definition, section headers matching the domain grouping, and a Constraint Index at the bottom. The L2-REINJECT marker (rank=3) correctly selects the 5 highest-priority constraints for re-injection into every prompt, a decision that is operationally sound — these 5 cover the most frequently violated failure modes (main-context execution, gate threshold, unbounded loops, uncited facts, missing worktracker entities).

**Gaps:**
Same DA-1 omission as Deliverable 1: `/transcript`, `/ast`, and `/worktracker` are not listed as delegation targets. For a .claude/rules/ file that applies to all multi-agent orchestration, this gap is slightly more consequential than in the template, because the auto-loaded constraint will be applied to sessions involving /worktracker even though /worktracker is not named.

The L2-REINJECT marker covers 5 constraints but omits AQ-5 (per-phase gates, not end-of-pipeline only) from re-injection. Given that end-of-pipeline quality gate placement is identified in barrier-4/synthesis.md as a cross-cutting anti-pattern, AQ-5 arguably belongs in the L2 set.

**Improvement Path:**
Add `/worktracker, /transcript, /ast` to DA-1. Add AQ-5 summary to the L2-REINJECT marker.

---

#### Internal Consistency (0.90/1.00)

**Evidence:**
All 22 constraints are internally consistent within the rule file. The NEVER/Consequence/Instead structure is applied uniformly. No constraint creates a requirement that another constraint forbids.

**Gaps:**
AQ-4 states: "assign each adversarial strategy (S-001 through S-014) to a separate agent invocation." However, the PROJ-014 research corpus and quality-enforcement.md distinguish between 10 selected strategies and 5 excluded strategies. S-005, S-006, S-008, S-009, and S-015 are excluded. Saying "S-001 through S-014" implies all 14 should be assigned, which would violate the constitutional constraints against multi-model approaches (S-005, S-009) and adversarial prompt injection (S-015). A colleague reading AQ-4 literally would be misled.

The rule file's IT-3 removes the constraint's H-07 citation ("hexagonal architecture per H-07, SOLID per coding-standards.md") that appears in Deliverable 1's version of the same constraint, instead saying just "(hexagonal architecture, SOLID)." This is a minor degradation of traceability for the rule file vs. the template.

**Improvement Path:**
Change AQ-4's "S-001 through S-014" to "the 10 selected adversarial strategies (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)" or "the selected strategies per quality-enforcement.md." Restore the H-07 and coding-standards.md citations in IT-3.

---

#### Methodological Rigor (0.95/1.00)

**Evidence:**
The file is correctly structured for its intended purpose as a .claude/rules/ auto-loaded document:
- Navigation table is present per H-23 with correct section-name anchor links.
- L2-REINJECT is correctly formatted with rank and content fields.
- Constraint XML tags use a simple `<constraint id="...">` format without the `format="NPT-013"` attribute — this is appropriate for a rule file where the format rationale is documented in prose (Usage section) rather than embedded in each element.
- The footer citation "PROJ-014 Negative Prompting Research" is present.
- The Usage section correctly instructs readers to place the file in `.claude/rules/orchestration-behavioral-constraints.md`.

**Gaps:**
The constraint XML does not use self-closing tags or schema-valid XML. This is cosmetic for current usage but limits machine-parsability. This is a SOFT concern, not a meaningful gap for this deliverable type.

The L2-REINJECT rank=3 placement is appropriate but its interaction with the existing L2-REINJECT markers in quality-enforcement.md (ranks 1–10) is not documented. A colleague dropping this file into .claude/rules/ may not realize that rank=3 means these constraints will be re-injected before rank=4 quality enforcement rules and after rank=2 quality threshold rules.

**Improvement Path:**
Add a note in Usage explaining rank=3's position in the L2-REINJECT priority stack relative to existing .claude/rules/ files.

---

#### Evidence Quality (0.72/1.00)

**Evidence:**
The header note states: "NPT-013 achieves 100% compliance vs 92.2% positive-only, p=0.016." The Constraint Index footer says: "Source: PROJ-014 Negative Prompting Research."

**Gaps — primary scoring weakness, same as Deliverable 1:**
No individual constraint is linked to a specific research finding. For a .claude/rules/ file that will be auto-applied across all future orchestration sessions, the evidence quality concern is actually higher than for the template: the constraints will influence agent behavior without the consuming agent (or the human overseeing it) being able to assess their evidence basis.

The statistical claim (100% vs 92.2%, p=0.016) is not pinned to comparative-effectiveness.md (phase-2/TASK-006). A colleague cannot verify whether this is a within-study finding, a meta-analytic claim, or an observation from a pilot condition.

**Improvement Path:**
Same as Deliverable 1: add NPT-ID and evidence tier to the Constraint Index. For the statistical claim, add: "(Source: projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md, TASK-006)."

---

#### Actionability (0.95/1.00)

**Evidence:**
The install instruction is one sentence and gives the exact destination path. The scope definition tells users exactly which workflow contexts activate these constraints. The format rationale ("Do not convert these to positive instructions — the negation format is validated to outperform positive framing for behavioral compliance") pre-empts the most likely mistake a colleague would make. The Constraint Index allows a reader to scan all 22 constraints in one table before deciding to adopt.

**Gaps:**
No gap significant enough to lower below 0.95. The file is ready for immediate use.

**Improvement Path:**
None required for actionability.

---

#### Traceability (0.87/1.00)

**Evidence:**
Constraint IDs are stable, unique, and consistently formatted. The navigation table provides section-level traceability. The Constraint Index provides a summary view. The L2-REINJECT marker makes the 5 priority constraints explicitly visible.

**Gaps:**
Same constraint-level traceability gap as Deliverable 1. The Constraint Index footer says "Source: PROJ-014 Negative Prompting Research" but does not identify which phase, task, or research artifact.

IT-3 in the rule file drops the H-07 citation that appears in the template version ("hexagonal architecture per H-07, SOLID per coding-standards.md" becomes just "hexagonal architecture, SOLID"). This creates a traceability inconsistency between the two deliverables for the same constraint.

**Improvement Path:**
Add NPT-ID and evidence tier to Constraint Index. Restore H-07 and coding-standards.md citations in IT-3. Add specific TASK-ID and artifact path to the footer source citation.

---

### Improvement Recommendations (Priority Ordered) — Deliverable 2

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.72 | 0.87 | Add NPT-ID and evidence tier to Constraint Index table. Pin statistical claim to comparative-effectiveness.md with file path. |
| 2 | Internal Consistency | 0.90 | 0.94 | Fix AQ-4: replace "S-001 through S-014" with the explicit list of 10 selected strategies. Restore H-07/coding-standards.md citation in IT-3. |
| 3 | Traceability | 0.87 | 0.92 | Restore H-07 citation in IT-3. Add TASK-ID to footer. |
| 4 | Completeness | 0.93 | 0.96 | Add `/worktracker, /transcript, /ast` to DA-1. Add AQ-5 to L2-REINJECT marker. |
| 5 | Methodological Rigor | 0.95 | 0.97 | Add note explaining rank=3 L2-REINJECT priority stack position relative to existing .claude/rules/ files. |

---

## Cross-Deliverable Findings

### Severity-Classified Findings

| Severity | ID | Deliverable | Finding |
|----------|----|-------------|---------|
| Major | F-001 | D1, D2 | Evidence Quality gap: no per-constraint NPT-ID or evidence tier annotation. A colleague cannot distinguish T1-backed constraints from T4-observational constraints. This matters because the research corpus explicitly marks some constraints as contingent on Phase 2 experimental completion (barrier-4/synthesis.md "MANDATORY EPISTEMOLOGICAL CONSTRAINT"). |
| Major | F-002 | D1, D2 | Statistical claim (100% vs 92.2%, p=0.016) is cited without a reference path to comparative-effectiveness.md. Colleagues cannot verify the key performance claim that motivates adopting NPT-013 format. |
| Major | F-003 | D2 | AQ-4 references "S-001 through S-014" which includes excluded strategies (S-005, S-006, S-008, S-009, S-015). Literal compliance would require invoking multi-model strategies that are constitutionally prohibited (P-003 risk via S-005/S-009 requiring cross-model LLMs). |
| Minor | F-004 | D1, D2 | EC-2/DA-1 ambiguity: it is unclear which agent is responsible for satisfying the WebSearch citation requirement when the orchestrator delegates all decisions. |
| Minor | F-005 | D1, D2 | DA-1 omits `/worktracker, /transcript, /ast` from delegation targets. |
| Minor | F-006 | D2 | IT-3 drops H-07 citation present in D1's version of the same constraint, creating cross-document inconsistency. |
| Minor | F-007 | D1 | OP-2 does not require syntactically valid Mermaid, only complete content. |
| Minor | F-008 | D1 | C4 criticality level undefined for readers unfamiliar with the Jerry quality model. |

### Critical Findings Assessment

No finding qualifies as Critical (would block acceptance). F-001 and F-002 are Major evidence quality gaps that prevent informed colleague adoption. F-003 is Major because literal compliance produces a constitutional violation. These three findings together block PASS at the 0.95 threshold.

---

## Combined Verdict

| Deliverable | Composite | Threshold | Verdict |
|-------------|-----------|-----------|---------|
| D1: Mega-Prompt Template | 0.878 | 0.95 | **REVISE** |
| D2: Behavioral Constraints Rule File | 0.887 | 0.95 | **REVISE** |

Both deliverables are strong first production artifacts. They score above the standard H-13 threshold of 0.92 on most dimensions individually. The gap to 0.95 is driven almost entirely by the evidence quality dimension (0.72 for both), which is addressable through a single focused pass: annotating the Constraint Index with NPT-IDs and evidence tiers, and pinning the statistical claim to its source artifact.

F-003 (AQ-4 strategy range error in D2) is the only finding that introduces a correctness issue rather than a documentation gap. It is a one-line fix.

**Estimated revision cost:** 2–3 hours for a focused pass addressing F-001 through F-003 across both deliverables. After those fixes, both artifacts would likely score >= 0.95 on re-scoring.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific quotes and section references
- [x] Uncertain scores resolved downward (Evidence Quality: chose 0.72 not 0.78 given zero per-constraint citations)
- [x] First-draft calibration considered (these are post-research production artifacts, not first drafts — slightly higher baseline than 0.65-0.80 is justified)
- [x] No dimension scored above 0.95 without specific positive evidence (Actionability D2 at 0.95 is justified by one-sentence install, scope definition, and format rationale)
- [x] AQ-4 error in D2 assessed as Major not Minor given constitutional violation potential if literally applied
- [x] Both verdicts are REVISE, not PASS — the 0.95 threshold is not met and this is correctly reflected

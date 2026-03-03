# Quality Score Report: /prompt-engineering SKILL.md (Iteration 2)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict and one-line assessment |
| [Scoring Context](#scoring-context) | Deliverable metadata and scoring parameters |
| [Score Summary](#score-summary) | Weighted composite and threshold comparison |
| [Dimension Scores](#dimension-scores) | Per-dimension scores with evidence summaries |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Full evidence, gaps, and improvement paths per dimension |
| [Prior Finding Resolution](#prior-finding-resolution) | Status of i1 findings (CF-01 through CF-05) |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered actions to reach threshold |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency verification checklist |

---

## L0 Executive Summary

**Score:** 0.88/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.82)
**One-line assessment:** Strong second iteration resolving all prior dependency gaps; reaches REVISE band but falls short of 0.95 C4 threshold due to missing "Invoking an Agent" section (H-25/H-26 required for multi-agent skills), absent H-22 HARD rule text update for `/prompt-engineering`, and no Integration Points section.

---

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/prompt-engineering/SKILL.md`
- **Deliverable Type:** Skill definition file (SKILL.md)
- **Criticality Level:** C4 (user-specified -- architecture/governance artifact)
- **Quality Threshold:** 0.95 (user-specified C4 gate)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.73 (REVISE, iteration 1)
- **Scored:** 2026-03-01T00:00:00Z
- **Iteration:** 2

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.88 |
| **Threshold** | 0.95 (C4 user-specified) |
| **SSOT Threshold** | 0.92 (H-13 for C2+) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring, no adv-executor reports) |
| **Delta from i1** | +0.15 (0.73 -> 0.88) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | Missing "Invoking an Agent" section (required for multi-agent per skill-standards); H-22 HARD rule text not updated; no Integration Points section |
| Internal Consistency | 0.20 | 0.93 | 0.186 | All claims internally aligned; NPT format descriptions match pattern reference; agent table matches AGENTS.md and file system |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Well-structured methodology with NPT format reference, routing disambiguation, constitutional compliance; follows established SKILL.md patterns |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Research findings cited with specific metrics (100% vs 92.2%, p=0.016); file paths are specific and verified; some references lack full traceability chain |
| Actionability | 0.15 | 0.88 | 0.132 | Quick Reference with concrete examples; Agent Routing Guide with keyword mapping; "When to Use" section clear; missing invocation options reduces actionability |
| Traceability | 0.10 | 0.85 | 0.085 | References table with 7 specific file paths; SSOT references present; PROJ-014 source cited; H-22 not fully traceable to this skill |
| **TOTAL** | **1.00** | | **0.879** | |

**Rounded composite: 0.88**

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**

The SKILL.md addresses the core requirements of a multi-agent skill definition: version blockquote (lines 20-23), Triple-Lens Document Audience (lines 27-35), navigation table (lines 39-49), Overview with capabilities (lines 53-68), When to Use with NEVER-framed exclusions (lines 72-88), Available Agents table (lines 92-98), Agent Routing Guide (lines 100-106), P-003 Compliance with ASCII diagram (lines 108-130), Quick Reference with examples (lines 134-179), Routing Disambiguation table (lines 183-194), Constitutional Compliance table (lines 199-206), Architecture Notes with design rationale (lines 210-218), References table with 7 entries (lines 222-230), and footer (lines 234-238).

All 5 prior critical findings (CF-01 through CF-05) are resolved -- see [Prior Finding Resolution](#prior-finding-resolution).

**Gaps:**

1. **Missing "Invoking an Agent" section (skill-standards.md section 8, marked YES for multi-agent skills).** The adversary SKILL.md includes a full "Invoking an Agent" section with three invocation options (natural language, explicit agent, Task tool code). The prompt-engineering SKILL.md omits this entirely. This is a structural requirement per skill-standards.md for multi-agent skills.

2. **H-22 HARD rule text not updated for `/prompt-engineering`.** The trigger map row exists in `mandatory-skill-usage.md` (line 43), but the H-22 rule text itself (line 23) does not include `/prompt-engineering` in the enumerated list of MUST-invoke skills. The L2-REINJECT marker (line 5) also omits `/prompt-engineering`. This means the skill has a trigger map entry but is not formally mandated by the HARD rule text or L2 reinforcement -- a registration gap that could cause the skill to not trigger proactively.

3. **No Integration Points section.** Skill-standards.md marks this as RECOMMENDED (section 10). The adversary SKILL.md has a full integration section ("Integration with Creator-Critic-Revision Cycle"). The prompt-engineering skill has natural integration points (e.g., pe-constraint-gen output feeds into agent definitions, pe-scorer complements ps-critic) that are not documented.

4. **No "Invoking an Agent" Option 3 (Task tool code block).** For programmatic invocation within workflows, the adversary SKILL.md shows a Task tool invocation example. This is absent from prompt-engineering SKILL.md.

**Improvement Path:**
- Add "Invoking an Agent" section with three options (natural language, explicit agent, Task tool) per skill-standards section 8. Model after `skills/adversary/SKILL.md` lines 137-186.
- Update H-22 HARD rule text in `mandatory-skill-usage.md` to include `/prompt-engineering` in the enumerated list.
- Add Integration Points section documenting cross-skill connections (pe-constraint-gen -> agent definitions, pe-scorer -> ps-critic complementarity).

### Internal Consistency (0.93/1.00)

**Evidence:**

Strong internal consistency across the deliverable:

- NPT format descriptions in the SKILL.md Overview (lines 66-68) match exactly the format specifications in `skills/prompt-engineering/rules/npt-pattern-reference.md` (lines 40-42 and 72-73).
- Agent table (lines 94-98) matches the file system (6 files confirmed: pe-builder.md, pe-builder.governance.yaml, pe-constraint-gen.md, pe-constraint-gen.governance.yaml, pe-scorer.md, pe-scorer.governance.yaml).
- Agent table matches AGENTS.md registration (lines 248-250 of AGENTS.md: same agent names, files, models, cognitive modes).
- CLAUDE.md registration (line 87) matches SKILL.md description and agent count.
- Trigger map entry in mandatory-skill-usage.md (line 43) aligns with activation-keywords in SKILL.md frontmatter.
- Constitutional Compliance table (lines 200-206) uses NPT-013 format consistently.
- PROJ-014 research finding (100% vs 92.2%, p=0.016) cited consistently in Overview (line 55), npt-pattern-reference.md (line 66), and AGENTS.md (line 244).

**Gaps:**

1. **Minor: "Overview" vs "Purpose" heading.** Skill-standards.md section 4 is titled "Purpose". The prompt-engineering SKILL.md uses "Overview". The adversary SKILL.md uses "Purpose". This is a naming inconsistency with the standard, though the content fulfills the same role.

**Improvement Path:**
- Consider renaming "Overview" to "Purpose" for consistency with skill-standards.md section naming and the adversary SKILL.md pattern. This is minor and does not affect functionality.

### Methodological Rigor (0.90/1.00)

**Evidence:**

The SKILL.md follows established methodological patterns:

- **Follows skill-standards.md structure:** 12 of 14 recommended sections present. Frontmatter includes all required and Jerry-required fields (name, description, version, allowed-tools, activation-keywords).
- **NPT format reference table:** Correctly separates NPT-009 and NPT-013 with format, structure, and use case columns (lines 65-68).
- **Routing disambiguation:** Full table with 6 exclusion conditions, each with "Use Instead" and "Consequence of Misrouting" columns (lines 187-194). Follows the same pattern as adversary SKILL.md.
- **Constitutional compliance:** NPT-013 format with principle, requirement, and consequence columns (lines 200-206). Matches adversary SKILL.md pattern.
- **Agent routing guide:** Keyword-to-agent mapping table (lines 102-106) enables deterministic routing.
- **NEVER-framed exclusions:** "When to Use" section includes 4 NEVER-framed exclusions with consequences (lines 82-87), following NPT-013 format.
- **Design rationale:** Architecture Notes section explains the three knowledge sources operationalized by the skill (lines 214-218).

**Gaps:**

1. **No explicit methodology for agent selection within the skill.** The adversary SKILL.md documents a decision framework (H-16 ordering, criticality-based strategy selection). The prompt-engineering SKILL.md has a simpler routing guide but no formal decision framework for when to use pe-builder vs pe-constraint-gen vs pe-scorer in combination.

2. **No fallback behavior documented.** The adversary SKILL.md documents fallback behavior for missing template files. The prompt-engineering SKILL.md does not document what happens when referenced SSOT files (prompt-quality.md, prompt-templates.md) are unavailable.

**Improvement Path:**
- Add a brief decision framework or workflow combining agents (e.g., "build-then-score" workflow documented as a formal pattern).
- Document fallback behavior for missing SSOT files.

### Evidence Quality (0.88/1.00)

**Evidence:**

- **PROJ-014 research metrics cited with specificity:** "100% compliance vs 92.2% for positive-only framing (p=0.016, CONDITIONAL GO via PG-003)" (line 55). This is a concrete, verifiable claim with statistical significance and decision status.
- **7 specific file paths in References table** (lines 224-230): all paths verified to exist or are plausible framework paths.
- **NPT pattern reference file exists** at `skills/prompt-engineering/rules/npt-pattern-reference.md` (verified via Read).
- **PROJ-014 synthesis path specific:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md` (line 227).
- **A/B testing path specific:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/ab-testing/ab-testing-synthesis.md` (line 228).

**Gaps:**

1. **Constitutional compliance table (lines 200-206) cites only 3 principles (P-003, P-020, P-022).** The adversary SKILL.md cites 7 principles (P-001, P-002, P-003, P-004, P-011, P-020, P-022). The prompt-engineering skill addresses the constitutional minimum but does not evidence additional relevant principles (e.g., P-002 for persistence, P-004 for provenance of generated constraints).

2. **No citation for the claim that the 7-criterion rubric formula is `total = sum((raw_score_N / 3) * weight_N * 100)`.** This formula appears in Architecture Notes (line 217) but the source reference (prompt-quality.md) is only listed generically -- no specific section anchor is provided.

**Improvement Path:**
- Expand constitutional compliance table to include P-002 (persistence of generated prompts/constraints) and P-004 (provenance of constraint sources).
- Add section anchors to SSOT references where available.

### Actionability (0.88/1.00)

**Evidence:**

- **Quick Reference section (lines 134-179):** Provides 3 concrete usage examples with expected agent behavior (build prompt, generate constraints, score prompt).
- **Common Workflows table (lines 173-179):** 5 rows mapping need to agent to example invocation.
- **Agent Routing Guide (lines 102-106):** Keyword-based agent selection with rationale column.
- **"When to Use" section (lines 72-88):** 5 positive triggers and 4 NEVER-framed exclusions with "use instead" alternatives.
- **NPT format reference table (lines 65-68):** Clear format/structure/use-case mapping for the two active patterns.

**Gaps:**

1. **No Task tool invocation example.** The adversary SKILL.md provides a full Task tool code block (lines 167-186) showing programmatic invocation with all required context fields. The prompt-engineering SKILL.md provides only natural language examples. For programmatic integration within orchestrated workflows, Task tool examples are important.

2. **No explicit "do NOT use" examples in Quick Reference.** The adversary SKILL.md's Quick Reference includes both positive and disambiguation hints. The prompt-engineering Quick Reference only shows positive examples.

3. **Missing invocation options reduce actionability for developers.** Without "Invoking an Agent" section options 2 and 3, developers must infer invocation patterns from other skills.

**Improvement Path:**
- Add "Invoking an Agent" section with all three options (addresses Completeness gap simultaneously).
- Add a "do NOT use" row to Common Workflows table for disambiguation.

### Traceability (0.85/1.00)

**Evidence:**

- **References table (lines 222-230):** 7 entries with specific repo-relative file paths, not generic descriptions.
- **SSOT references in frontmatter (line 23):** Two specific SSOT files declared.
- **PROJ-014 source attribution (line 237):** Source project identified.
- **Version and date tracked (lines 234-238):** Footer includes version, compliance, SSOT, source, and creation date.
- **NPT pattern reference traceable:** `skills/prompt-engineering/rules/npt-pattern-reference.md` includes traceability back to source taxonomy at `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md`.

**Gaps:**

1. **H-22 not fully traceable to this skill.** The trigger map row exists (mandatory-skill-usage.md line 43), but the H-22 HARD rule text and L2-REINJECT marker do not mention `/prompt-engineering`. This creates a traceability gap: the skill cannot be traced from the HARD rule mandate to its trigger map entry because the mandate text does not include it.

2. **No ADR reference.** Other skills reference ADRs (e.g., adversary SKILL.md references ADR-EPIC002-001, ADR-EPIC002-002). The prompt-engineering skill has no ADR reference. If no architecture decision was made for this skill, document that it was derived directly from PROJ-014 research without a formal ADR.

3. **AGENTS.md registration is present but not referenced in the References table.** The deliverable lists 7 references but does not include AGENTS.md as a registration point.

**Improvement Path:**
- Update H-22 HARD rule text and L2-REINJECT marker to include `/prompt-engineering`.
- Add AGENTS.md to References table as a registration reference.
- Add a note about ADR status (either reference the applicable ADR or document that no ADR was required).

---

## Prior Finding Resolution

| Finding | i1 Status | i2 Status | Evidence |
|---------|-----------|-----------|----------|
| CF-01: CLAUDE.md registration missing | REVISE | **RESOLVED** | Line 87 of CLAUDE.md: `/prompt-engineering` entry with description and agent count |
| CF-02: mandatory-skill-usage.md trigger map missing | REVISE | **PARTIALLY RESOLVED** | Trigger map row exists (line 43) but H-22 HARD rule text (line 23) and L2-REINJECT marker (line 5) do not include `/prompt-engineering` |
| CF-03: Agent definition files missing | REVISE | **RESOLVED** | 6 files confirmed in `skills/prompt-engineering/agents/`: pe-builder.md, pe-builder.governance.yaml, pe-constraint-gen.md, pe-constraint-gen.governance.yaml, pe-scorer.md, pe-scorer.governance.yaml |
| CF-04: NPT reference table missing | REVISE | **RESOLVED** | File exists at `skills/prompt-engineering/rules/npt-pattern-reference.md` (143 lines, well-structured with navigation table, pattern guide, examples, quality criteria) |
| CF-05: Triple-Lens section missing | REVISE | **RESOLVED** | Present at lines 27-35 with L0/L1/L2 audience mapping and anchor links |

**Resolution rate:** 4/5 fully resolved, 1/5 partially resolved.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.82 | 0.92 | Add "Invoking an Agent" section with three options (natural language, explicit agent, Task tool code block). Model after `skills/adversary/SKILL.md` lines 137-186. This is a required section for multi-agent skills per skill-standards.md. |
| 2 | Traceability | 0.85 | 0.92 | Update H-22 HARD rule text in `mandatory-skill-usage.md` line 23 to include "MUST invoke `/prompt-engineering` for structured prompt construction and NPT constraint generation." Update L2-REINJECT marker (line 5) to include `/prompt-engineering`. |
| 3 | Evidence Quality | 0.88 | 0.92 | Expand Constitutional Compliance table to include P-002 (persist generated prompts/constraints to files) and P-004 (trace constraint sources to PROJ-014 findings). |
| 4 | Actionability | 0.88 | 0.92 | Addressed by Priority 1 (Invoking an Agent section adds Task tool code example). |
| 5 | Completeness | 0.82 | 0.92 | Add Integration Points section documenting cross-skill connections: pe-constraint-gen output -> agent governance YAML forbidden_actions, pe-scorer -> ps-critic complementarity for prompt vs deliverable quality scoring. |
| 6 | Internal Consistency | 0.93 | 0.95 | Rename "Overview" to "Purpose" for consistency with skill-standards.md section naming and adversary SKILL.md pattern. Minor. |
| 7 | Methodological Rigor | 0.90 | 0.92 | Add brief agent combination decision framework (e.g., "build-then-score" workflow). Document fallback behavior for missing SSOT files. |

**Estimated impact of Priority 1-3:** Completeness +0.08, Traceability +0.05, Evidence +0.04. Combined composite improvement: approximately +0.05, bringing estimated score to ~0.93. Priority 4-7 needed to reach 0.95 C4 threshold.

---

## Leniency Bias Check

- [x] Each dimension scored independently (scored Completeness first, then Internal Consistency, etc. -- did not let strong Internal Consistency inflate Completeness)
- [x] Evidence documented for each score (specific line numbers, file paths, and cross-references cited)
- [x] Uncertain scores resolved downward (Completeness could be 0.83-0.85 range; chose 0.82. Traceability could be 0.85-0.88; chose 0.85)
- [x] First-draft calibration considered (this is iteration 2, not first draft; prior score 0.73 resolved 4/5 findings; 0.88 is a reasonable +0.15 improvement)
- [x] No dimension scored above 0.95 without exceptional evidence (Internal Consistency at 0.93 is the highest; justified by zero contradictions found and verified cross-file alignment across SKILL.md, AGENTS.md, CLAUDE.md, mandatory-skill-usage.md, and npt-pattern-reference.md)
- [x] Mathematical verification: (0.82*0.20) + (0.93*0.20) + (0.90*0.20) + (0.88*0.15) + (0.88*0.15) + (0.85*0.10) = 0.164 + 0.186 + 0.180 + 0.132 + 0.132 + 0.085 = 0.879, rounded to 0.88

---

## Session Context (adv-scorer -> orchestrator)

```yaml
verdict: REVISE
composite_score: 0.88
threshold: 0.95
weakest_dimension: Completeness
weakest_score: 0.82
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add 'Invoking an Agent' section with 3 invocation options (required for multi-agent skills per skill-standards.md)"
  - "Update H-22 HARD rule text and L2-REINJECT marker to include /prompt-engineering"
  - "Expand Constitutional Compliance table to include P-002 and P-004"
  - "Add Integration Points section documenting cross-skill connections"
  - "Rename Overview to Purpose for consistency with skill-standards.md"
```

---

*Score Report Version: 1.0.0*
*Scoring Agent: adv-scorer (S-014 LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-01*

# Quality Score Report: Prompt Engineering SKILL.md (Iteration 3)

## L0 Executive Summary
**Score:** 0.912/1.00 | **Verdict:** REVISE | **Weakest Dimensions:** Completeness (0.90), Internal Consistency (0.90)
**One-line assessment:** Strong i2-to-i3 improvement (+0.032) with all 3 prior findings resolved, but two minor structural gaps prevent clearing the 0.92 threshold -- navigation table missing the "Invoking an Agent" heading and P-004 declared in SKILL.md but absent from agent governance YAMLs.

## Scoring Context
- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/prompt-engineering/SKILL.md`
- **Deliverable Type:** Skill definition file (SKILL.md)
- **Criticality Level:** C4 (user-specified)
- **Quality Threshold:** 0.95 (user-specified C4 gate)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-01T19:42:00Z
- **Iteration:** 3 (i1: 0.73, i2: 0.88, i3: 0.912)

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.912 |
| **Threshold (user-specified C4)** | 0.95 |
| **Threshold (H-13 standard)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |

## Score Trajectory

| Iteration | Score | Delta | Key Changes |
|-----------|-------|-------|-------------|
| i1 | 0.73 | -- | Initial draft |
| i2 | 0.88 | +0.15 | Major structural improvements |
| i3 | 0.912 | +0.032 | Invoking section, H-22/L2 registration, expanded constitutional table |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | 13/14 required sections present; nav table missing "Invoking an Agent" heading; Integration Points absent |
| Internal Consistency | 0.20 | 0.90 | 0.180 | Near-perfect cross-file consistency; P-004 in SKILL.md but absent from all governance YAMLs |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Follows skill-standards.md, H-34 dual-file architecture, H-35 constitutional triplet in all agents |
| Evidence Quality | 0.15 | 0.91 | 0.1365 | PROJ-014 stats cited (100% vs 92.2%, p=0.016); 7 reference entries with repo-relative paths |
| Actionability | 0.15 | 0.93 | 0.1395 | 3 invocation options, copy-paste Quick Reference, 5-row Common Workflows table |
| Traceability | 0.10 | 0.92 | 0.092 | Full chains: PROJ-014 -> SKILL.md -> agents -> governance YAML -> schema; registration confirmed in 3 locations |
| **TOTAL** | **1.00** | | **0.912** | |

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

Verified against `skill-standards.md` 14-section checklist:

| # | Required Section | Present? | Notes |
|---|-----------------|----------|-------|
| 1 | Version blockquote header | Yes | Lines 20-23: version, framework, constitutional compliance, SSOT |
| 2 | Document Sections (Navigation) | Yes | Lines 39-49: 7 entries with anchor links |
| 3 | Document Audience (Triple-Lens) | Yes | Lines 27-35: L0/L1/L2 with preamble |
| 4 | Purpose/Overview | Yes | Lines 53-69: named "Overview" with core capabilities and NPT format table |
| 5 | When to Use / Do NOT use | Yes | Lines 72-88: 5 triggers, 4 anti-patterns with consequences |
| 6 | Available Agents | Yes | Lines 92-106: 3 agents with routing guide |
| 7 | P-003 Compliance | Yes | Lines 108-131: ASCII hierarchy diagram |
| 8 | Invoking an Agent | Yes | Lines 134-184: 3 options (natural language, explicit, Task tool) -- **i2 finding resolved** |
| 9 | Domain-specific sections | Yes | Quick Reference (lines 187-233), Routing Disambiguation (lines 236-248) |
| 10 | Integration Points | **No** | RECOMMENDED section absent. No cross-skill integration documented. |
| 11 | Constitutional Compliance | Yes | Lines 251-262: 5 principles (P-002, P-003, P-004, P-020, P-022) -- **i2 finding resolved** |
| 12 | Quick Reference | Yes | Lines 187-233: 3 copy-paste examples + Common Workflows table |
| 13 | References | Yes | Lines 277-286: 7 entries with full repo-relative paths |
| 14 | Footer | Yes | Lines 289-294: version, compliance, SSOT, date |

Registration verification:
- CLAUDE.md skill table (line 87): registered with description and agent count -- CONFIRMED
- AGENTS.md (lines 242-262): full section with agent table, key capabilities, invocation, model tiers -- CONFIRMED
- mandatory-skill-usage.md H-22 text (line 23): includes `/prompt-engineering` -- **i2 finding resolved**
- mandatory-skill-usage.md L2-REINJECT marker (line 5): includes `/prompt-engineering` -- **i2 finding resolved**
- mandatory-skill-usage.md trigger map (line 43): 12 keywords with negative keywords and priority 11 -- CONFIRMED

Agent files: 3 agent .md files + 3 .governance.yaml files = 6 total. All present and well-formed.

**Gaps:**

1. **Navigation table missing "Invoking an Agent" heading (NAV-004 MEDIUM).** The `## Invoking an Agent` heading at line 134 is a major `##`-level section but is not listed in the Document Sections navigation table (lines 39-49). Per NAV-004: "All major sections (`##` headings) SHOULD be listed."

2. **Section ordering swap (MEDIUM).** Document Audience (line 27) appears before Document Sections (line 39). Skill-standards.md specifies Navigation (#2) before Audience (#3). No justification documented for the deviation.

3. **Integration Points section absent (RECOMMENDED).** Skill-standards.md section #10 recommends an "Integration Points" section documenting cross-skill connections. Not present. This skill could document interaction with `/adversary` (pe-scorer vs adv-scorer distinction), `/problem-solving` (research prompts as input), and prompt-templates.md (templates as output targets).

**Improvement Path:**
- Add `| [Invoking an Agent](#invoking-an-agent) | Three invocation options for agent access |` to navigation table
- Swap Document Audience and Document Sections to match standard ordering (or document justification)
- Add Integration Points section documenting cross-skill touchpoints

### Internal Consistency (0.90/1.00)

**Evidence:**

Cross-file consistency verified across 10 files:

| Data Point | SKILL.md | Agent .md files | Governance YAML | AGENTS.md |
|-----------|----------|-----------------|-----------------|-----------|
| Agent names | pe-builder, pe-constraint-gen, pe-scorer | Matches | Matches | Matches |
| Model assignments | opus, sonnet, haiku | Matches | N/A (not in YAML) | Matches |
| Cognitive modes | integrative, systematic, convergent | Matches | Matches | Matches |
| Version | 1.0.0 | 1.0.0 (all) | 1.0.0 (all) | N/A |
| Tool tiers | Not stated | pe-builder T2, pe-constraint-gen T2, pe-scorer T1 | Matches agent tools | N/A |
| NPT formats | NPT-009, NPT-013 | Referenced consistently | NPT-009-complete format | N/A |

Constitutional principle coverage:

| Principle | SKILL.md | pe-builder YAML | pe-constraint-gen YAML | pe-scorer YAML |
|-----------|----------|-----------------|------------------------|----------------|
| P-002 | Yes | Yes | Yes | No |
| P-003 | Yes | Yes | Yes | Yes |
| P-004 | Yes | **No** | **No** | **No** |
| P-011 | No | No | No | Yes |
| P-020 | Yes | Yes | Yes | Yes |
| P-022 | Yes | Yes | Yes | Yes |

**Gaps:**

1. **P-004 asymmetry.** SKILL.md Constitutional Compliance table (line 259) declares P-004 (provenance): "NEVER omit source attribution for generated constraints." However, none of the three agent governance YAML files include P-004 in `constitution.principles_applied`. This creates an asymmetry where the skill-level document promises behavior that is not encoded at the agent level.

2. **Minor terminology variance.** SKILL.md frontmatter description uses "quality validation" while the body uses "quality scoring." These are semantically close but not identical.

**Improvement Path:**
- Add P-004 to at least pe-constraint-gen.governance.yaml `constitution.principles_applied` (the agent most relevant to source attribution for constraints)
- Align frontmatter description terminology: use "quality scoring" to match body content

### Methodological Rigor (0.92/1.00)

**Evidence:**

| Standard | Compliance | Evidence |
|----------|-----------|---------|
| H-25(a) SKILL.md case | PASS | File named exactly `SKILL.md` |
| H-25(b) kebab-case folder | PASS | Folder is `prompt-engineering` |
| H-25(c) No README.md | PASS | No README.md found in skill folder |
| H-26(a) Description WHAT+WHEN+triggers | PASS | Frontmatter description includes all three components, 350 chars (under 1024), no XML |
| H-26(b) Repo-relative paths | PASS | All 7 references use full repo-relative paths |
| H-26(c) Registration | PASS | Registered in CLAUDE.md (line 87), AGENTS.md (lines 242-262), mandatory-skill-usage.md (lines 23, 43) |
| H-34 Dual-file architecture | PASS | 3 agent .md files with official frontmatter only; 3 companion .governance.yaml files |
| H-35 Constitutional triplet | PASS | All 3 agents declare P-003, P-020, P-022 in YAML; all have >= 3 forbidden_actions; no worker has Task tool |
| H-23 Navigation table | PASS (minor gap) | Table present with anchor links; missing "Invoking an Agent" entry |
| NPT-009 format compliance | PASS | All forbidden_actions use `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` |
| P-003 hierarchy diagram | PASS | ASCII diagram at lines 112-130 shows correct orchestrator-worker topology |
| Invoking an Agent pattern | PASS | 3 options matching adversary SKILL.md reference implementation |

**Gaps:**

1. The navigation table gap noted under Completeness reduces structural rigor slightly.

**Improvement Path:**
- Fix navigation table to include all `##` headings

### Evidence Quality (0.91/1.00)

**Evidence:**

| Claim | Supporting Evidence | Credibility |
|-------|-------------------|-------------|
| NPT-013 achieves 100% compliance vs 92.2% | PROJ-014 Phase 6 final synthesis (cited line 282) | High -- specific statistics with p-value (0.016) |
| CONDITIONAL GO via PG-003 | A/B testing synthesis (cited line 283) | High -- specific governance decision reference |
| 7-criterion rubric | `.context/rules/prompt-quality.md` (cited line 279) | High -- SSOT reference |
| 5-element prompt anatomy | `.context/rules/prompt-quality.md` (cited line 279) | High -- SSOT reference |
| NPT-009/NPT-013 format specifications | `npt-pattern-reference.md` (cited line 281) | High -- taxonomy pattern catalog traced |
| Scoring formula | Explicitly stated: `total = sum((raw_score_N / 3) * weight_N * 100)` (line 272) | High -- mathematical precision |
| Agent definition standards | `.context/rules/agent-development-standards.md` (cited line 284) | High -- SSOT reference |

**Gaps:**

1. **One-hop PROJ-006 provenance.** The 5-element prompt anatomy and 7-criterion rubric originate from PROJ-006-jerry-prompt research, but SKILL.md only cites the intermediate `prompt-quality.md` file, not the original research. The provenance chain works but requires one extra hop to reach the original source.

**Improvement Path:**
- Add PROJ-006 research reference to the References table (optional but strengthens provenance)

### Actionability (0.93/1.00)

**Evidence:**

| Actionability Element | Present | Quality |
|----------------------|---------|---------|
| Invocation Option 1: Natural language | Yes (lines 137-147) | 4 concrete examples |
| Invocation Option 2: Explicit agent | Yes (lines 149-157) | 3 concrete examples |
| Invocation Option 3: Task tool | Yes (lines 159-183) | Full Python code with prompt template |
| Copy-paste Quick Reference | Yes (lines 187-222) | 3 scenarios with expected output |
| Common Workflows table | Yes (lines 224-232) | 5 rows with Need/Agent/Example columns |
| Agent Routing Guide | Yes (lines 100-106) | Keywords-to-agent mapping |
| When to Use triggers | Yes (lines 72-80) | 5 specific trigger conditions |
| When NOT to use | Yes (lines 82-87) | 4 exclusions with consequences and redirects |
| Routing Disambiguation | Yes (lines 240-247) | 6 rows with "Use Instead" guidance |

The skill is immediately usable. A new user can follow the Quick Reference examples to start using the skill within minutes. The three invocation options cover different sophistication levels appropriately.

**Gaps:**

No significant gaps. The actionability of this skill is genuinely strong.

**Improvement Path:**
- Minor: Could add an "end-to-end workflow" example showing build -> score -> revise cycle

### Traceability (0.92/1.00)

**Evidence:**

Traceability chains verified:

1. **Research provenance:** SKILL.md (line 55, 282-283) -> Phase 6 final synthesis -> A/B testing synthesis -> taxonomy pattern catalog -> PROJ-014 research. COMPLETE.

2. **SSOT chain:** SKILL.md (line 23, 279-280) -> prompt-quality.md + prompt-templates.md. COMPLETE.

3. **Standards chain:** SKILL.md structure -> skill-standards.md (H-25, H-26) -> quality-enforcement.md (HARD Rule Index). COMPLETE.

4. **Agent chain:** SKILL.md Available Agents (lines 94-98) -> agent .md files (3) -> .governance.yaml files (3) -> JSON Schema (`docs/schemas/agent-governance-v1.schema.json`). COMPLETE.

5. **Registration chain:** SKILL.md -> CLAUDE.md (line 87) -> AGENTS.md (lines 242-262) -> mandatory-skill-usage.md (line 23 H-22 text, line 5 L2-REINJECT, line 43 trigger map). COMPLETE.

6. **Constitutional chain:** SKILL.md Constitutional Compliance (lines 255-261) -> governance YAMLs -> Jerry Constitution. COMPLETE (with P-004 asymmetry noted).

**Gaps:**

1. The P-004 asymmetry creates a minor traceability gap in the constitutional chain (SKILL.md declares it but agents do not encode it).

**Improvement Path:**
- Resolve P-004 asymmetry (same fix as Internal Consistency)

## i2 Finding Resolution Status

| # | i2 Finding | Status | Evidence |
|---|-----------|--------|---------|
| 1 | Missing "Invoking an Agent" section | **RESOLVED** | Section present at lines 134-184 with 3 options matching adversary SKILL.md pattern |
| 2 | H-22 text and L2-REINJECT missing `/prompt-engineering` | **RESOLVED** | H-22 text includes at line 23; L2-REINJECT includes at line 5 of mandatory-skill-usage.md |
| 3 | Constitutional Compliance table limited to minimum triplet | **RESOLVED** | Table now has 5 principles: P-002, P-003, P-004, P-020, P-022 (lines 255-261) |

All three i2 findings are confirmed resolved.

## New Findings (i3)

| # | Severity | Dimension(s) | Finding | Impact |
|---|----------|-------------|---------|--------|
| F-01 | Medium | Completeness, Methodological Rigor | Navigation table (lines 42-49) missing `## Invoking an Agent` heading entry (NAV-004 MEDIUM) | Readers scanning nav table cannot discover the Invoking section |
| F-02 | Low | Internal Consistency, Traceability | P-004 declared in SKILL.md Constitutional Compliance table but absent from all 3 agent governance YAMLs | Skill-level promise not encoded at agent level |
| F-03 | Low | Completeness | Section ordering: Document Audience (line 27) precedes Document Sections (line 39); standard specifies Navigation before Audience | Deviation from skill-standards.md ordering without documented justification |
| F-04 | Low | Completeness | Integration Points section absent (RECOMMENDED by skill-standards.md #10) | Cross-skill touchpoints undocumented |

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.90 | 0.93 | **Add "Invoking an Agent" to navigation table.** Insert `\| [Invoking an Agent](#invoking-an-agent) \| Three invocation options for agent access \|` after the "Available Agents" row in the Document Sections table (line 46). This resolves F-01. |
| 2 | Internal Consistency | 0.90 | 0.93 | **Add P-004 to pe-constraint-gen governance YAML.** In `skills/prompt-engineering/agents/pe-constraint-gen.governance.yaml`, add `- 'P-004: Provenance (Medium) - Generated constraints MUST include source attribution'` to `constitution.principles_applied`. This is the most relevant agent for source attribution. Resolves F-02. |
| 3 | Completeness | 0.90 | 0.92 | **Swap Document Audience and Document Sections.** Move the "Document Sections" table (lines 39-49) above "Document Audience" (lines 27-35) to match skill-standards.md ordering. Alternatively, add a one-line justification: "Audience-first ordering mirrors the triple-lens progressive disclosure pattern, providing routing context before structural navigation." Resolves F-03. |
| 4 | Completeness | 0.90 | 0.93 | **Add Integration Points section.** Add between Routing Disambiguation and Constitutional Compliance. Content: (a) `/adversary` -- pe-scorer uses different rubric than adv-scorer; distinguish 7-criterion prompt rubric from S-014 deliverable rubric. (b) `/problem-solving` -- pe-builder prompts often target ps-agent workflows. (c) prompt-templates.md -- templates are ready-to-use output; pe-builder produces custom prompts. Resolves F-04. |

## Projected Score After Fixes

Applying all 4 recommendations:
- Completeness: 0.90 -> 0.94 (nav table, ordering, Integration Points)
- Internal Consistency: 0.90 -> 0.93 (P-004 alignment)
- Other dimensions: unchanged

Projected composite: (0.94 * 0.20) + (0.93 * 0.20) + (0.92 * 0.20) + (0.91 * 0.15) + (0.93 * 0.15) + (0.92 * 0.10) = 0.188 + 0.186 + 0.184 + 0.1365 + 0.1395 + 0.092 = **0.926**

Note: The projected score of 0.926 exceeds the H-13 standard threshold (0.92) but remains below the user-specified C4 threshold (0.95). Reaching 0.95 would require additional depth improvements across multiple dimensions (e.g., expanded Integration Points, additional workflow examples, deeper evidence chains).

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness considered at 0.91, resolved to 0.90; Internal Consistency considered at 0.91, resolved to 0.90)
- [x] Iteration 3 calibration considered (i3 improvement over i2 is consistent: +0.032 reflects targeted fixes)
- [x] No dimension scored above 0.95 without exceptional evidence (highest: 0.93 Actionability)
- [x] Composite verified: 0.180 + 0.180 + 0.184 + 0.1365 + 0.1395 + 0.092 = 0.912

## Handoff Schema

```yaml
verdict: REVISE
composite_score: 0.912
threshold: 0.95  # user-specified C4
standard_threshold: 0.92  # H-13
weakest_dimension: Completeness
weakest_score: 0.90
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Add 'Invoking an Agent' to navigation table (F-01)"
  - "Add P-004 to pe-constraint-gen governance YAML (F-02)"
  - "Swap Document Audience/Sections ordering or justify deviation (F-03)"
  - "Add Integration Points section (F-04)"
```

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*Scoring Strategy: SSOT 6-dimension weighted composite*
*Constitutional Compliance: P-001, P-002, P-003, P-004, P-011, P-020, P-022*
*SSOT: `.context/rules/quality-enforcement.md`*

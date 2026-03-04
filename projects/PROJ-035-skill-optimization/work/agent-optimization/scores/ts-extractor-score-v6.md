# Quality Score Report: ts-extractor Agent Definition

## L0 Executive Summary

**Score:** 0.846/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.72)
**One-line assessment:** The v6 fixes (NPT-009-complete forbidden_actions, output block, persona block) are confirmed present but Evidence Quality dropped sharply to 0.72 due to stricter rubric application against unverifiable ML-tier claims and unsourced confidence adjustment values; Completeness also scored lower (0.82 vs 0.87) due to missing XML section tags, absent L0 output level, and missing enforcement block — composite is 0.846, regression from v5 (0.878), indicating a scoring calibration difference rather than deliverable regression.

---

## Scoring Context

- **Deliverable:** `/Users/evorun/workspace/jerry/skills/transcript/agents/ts-extractor.md` + `ts-extractor.governance.yaml`
- **Deliverable Type:** Agent Definition (dual-file architecture per H-34)
- **Criticality Level:** C2 (standard agent definition)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Scores:** v1=0.836, v2=0.860, v3=0.837 (regression), v4=0.864, v5=0.878
- **Scored:** 2026-03-03T00:00:00Z
- **Iteration:** 6

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.846 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | Primary sections present; missing XML section tags per H-34 body format, absent L0 output level, no enforcement block, no `<purpose>` section |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Version (1.4.2), model (sonnet), cognitive mode (convergent), tool tier (T4) all align across both files; NPT-009 format declared and followed; no contradictions |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | 3-tier extraction pipeline, 4-pattern speaker ID chain, quantified confidence formula, 4-step chunked protocol, topic segmentation with weighted signals; Tier 2 ML description aspirational not implemented |
| Evidence Quality | 0.15 | 0.72 | 0.108 | Named ADR/FR/PAT/DISC references present; confidence adjustment values (+0.05/+0.10/-0.10/-0.05) and topic weight values (0.95/0.90/0.85/0.75/0.70) stated without derivation; ML-tier claims unverifiable; all references internal only |
| Actionability | 0.15 | 0.85 | 0.1275 | Invocation template, self-critique checklist, Python assert pseudocode, regex patterns all immediately usable; Tier 2 ML extraction not implementable as written; topic limit overflow behavior undefined |
| Traceability | 0.10 | 0.86 | 0.086 | Version history (5 entries), ADR/FR/PAT/DISC/BUG/EN references, backlinks/forward links, schema references; PAT-XXX IDs lack source file paths; reference docs may not exist |
| **TOTAL** | **1.00** | | **0.8455** | |

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**

The following required elements are present and populated:

- **Official .md frontmatter:** `name: ts-extractor`, `description` (entity extraction focus), `model: sonnet`, `tools: Read, Write, Glob`, `mcpServers: memory-keeper: true` — all 5 relevant official fields populated
- **Governance YAML required fields:** `version: 1.4.2`, `tool_tier: T4`, `identity.role: Entity Extraction Specialist`, `identity.expertise` (6 entries), `identity.cognitive_mode: convergent` — all 5 required fields present
- **Navigation table:** 10 sections with purpose descriptions — H-23 compliant
- **Methodology:** Comprehensive 3-tier extraction pipeline, 4-step chunked processing protocol, 4-pattern speaker ID chain, confidence formula, topic segmentation algorithm, citation requirements
- **Guardrails:** `input_validation` with 8 specific fields, `output_filtering` with 7 entries, `fallback_behavior: warn_and_skip`
- **Constitutional compliance:** 7 principles listed in both .md and governance YAML
- **Forbidden actions:** 6 entries in NPT-009-complete format in governance YAML (confirmed present — this was a v5 gap)
- **Output block:** `required: true`, location, levels [L1, L2] — confirmed present (v5 gap resolved)
- **Persona block:** `tone: technical`, `communication_style: structured`, `audience_level: adaptive` — confirmed present (v5 gap resolved)
- **Session context:** on_receive (7 steps), on_send (5 steps), expected_inputs, schema references — present
- **Post-completion checks:** 8 validation assertions including INV-EXT-001/002 — present
- **Data integrity invariants:** INV-EXT-001 and INV-EXT-002 with Python pseudocode — present

**Gaps:**

1. **XML section tags absent:** H-34 body section format specifies `<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>` XML tags. The .md uses `##` markdown headings instead. This is a structural deviation from the prescribed body format per agent-development-standards.md "Markdown Body Sections" specification.

2. **No `<purpose>` section:** The standard requires a `<purpose>` section explaining "why the agent exists." There is no dedicated Purpose section — the role is embedded in Identity, but the hexagonal architecture separates these.

3. **Output levels missing L0:** Per AD-M-004, "agents producing stakeholder-facing deliverables SHOULD declare all three output levels (L0, L1, L2)." Current: `levels: [L1, L2]`. Extraction reports could be reviewed by stakeholders; L0 omission is a gap (MEDIUM standard, but documented).

4. **`enforcement` block absent:** The governance YAML has no `enforcement` object (quality gate tier, escalation path). This is a recommended field per agent-development-standards.md.

5. **`description` field lacks trigger keywords:** Per AD-M-003, description SHOULD include "WHAT the agent does, WHEN to invoke it, and at least one trigger keyword." The description "Extracts semantic entities (speakers, actions, decisions, questions, topics) from parsed transcripts" covers WHAT but omits WHEN and trigger keywords.

**Improvement Path:**

Add XML section tags to .md body per H-34 format. Add `<purpose>` section. Add L0 to output.levels. Add `enforcement` block to governance YAML. Expand description to include WHEN and trigger keywords.

---

### Internal Consistency (0.92/1.00)

**Evidence:**

Strong alignment across the dual-file architecture:

- **Version:** 1.4.2 in .md (line 11) and governance YAML (line 5) — exact match
- **Model:** `sonnet` in .md frontmatter (line 4) and governance YAML `default_model: sonnet` (line 18) — consistent
- **Cognitive mode:** `convergent` in .md Processing Instructions (line 49) and governance YAML (line 16) — consistent
- **Tool tier:** T4 (Persistent) in governance YAML, `mcpServers: memory-keeper: true` in .md — T4 requires Memory-Keeper per agent-development-standards.md; consistent
- **NPT-009 format:** `forbidden_action_format: NPT-009-complete` declared in governance YAML, and all 6 forbidden_actions entries follow the `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` pattern — declaration matches implementation
- **Constitutional principles:** 7 principles listed in .md (P-001, P-002, P-003, P-004, P-010, P-020, P-022) and same 7 listed in governance YAML constitution.principles_applied — consistent
- **Forbidden actions count:** 6 entries in governance YAML `capabilities.forbidden_actions`; 6 entries in .md Capabilities section — same count, aligned content
- **INV-EXT-001:** Referenced in Output Schema section, Data Integrity Invariants section, and Constitutional Compliance checklist — three-way consistent reinforcement
- **Chunk protocol:** The 4-step chunked processing protocol is referenced consistently throughout (Input Format, Chunked Processing Protocol, Processing Instructions)

**Gaps:**

- The .md Capabilities section "Forbidden Actions" has slightly different wording than the governance YAML forbidden_actions. The .md versions are more verbose with "Instead:" clauses; governance YAML uses NPT-009 format with "Consequence:" clauses. These are two representations of the same constraints, not contradictions, but the dual representation could drift over time. Minor coherence gap.
- `fallback_behavior: warn_and_skip` is a domain-specific value not in the standard enumerated set. Not a contradiction but a non-standard value that could be unclear.

**Improvement Path:**

Align the .md Capabilities forbidden actions wording with the governance YAML NPT-009 format to eliminate the dual representation. Document the `warn_and_skip` fallback value explicitly in the governance YAML as domain-specific.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**

The extraction methodology is detailed and well-structured:

- **Tiered extraction pipeline (PAT-001):** Three tiers with distinct confidence ranges: Tier 1 Rule-Based (0.85-1.0), Tier 2 ML-Based (0.70-0.85), Tier 3 LLM-Based (0.50-0.70). Tier 1 has 12 specific patterns with individual confidence scores.
- **Speaker identification (PAT-003):** 4-pattern fallback chain with explicit regex patterns and confidence scores: VTT tags (0.95), Prefix (0.90), Bracket (0.85), Contextual (0.60).
- **Confidence formula:** `final_confidence = clamp(base + adjustments, 0.0, 1.0)` with 4 named adjustments and explicit threshold classification (HIGH/MEDIUM/LOW).
- **Chunked processing protocol:** 4-step sequential protocol with explicit constraints (process in order, never load multiple chunks simultaneously, release chunk before loading next).
- **Chunk selection strategies:** 3 named strategies (Sequential, Index Only, Selective) with use cases and cost labels.
- **Citation validation:** 3 mandatory rules with specific failure conditions.
- **Topic segmentation:** 5 boundary signal types with weights, minimum duration (30s), maximum topics/hour (10), 100% coverage requirement, plus topic title generation algorithm.
- **Data integrity invariants:** INV-EXT-001 with Python assert code, INV-EXT-002 with filter-out examples.
- **Self-critique checklist:** 6 items tied to specific principles, evaluated before response.

**Gaps:**

1. **Tier 2 ML-Based is aspirational:** The Tier 2 description uses "NER EXTRACTION" and "INTENT CLASSIFICATION" as labels but provides no mechanism for how an LLM-based agent would invoke an ML model. This tier is described as if a separate ML pipeline exists, but no integration path is documented. As written, it is not implementable.

2. **Topic limit overflow undefined:** "Maximum topics per hour: 10 (avoid over-segmentation)" — the algorithm does not specify what happens when this limit is exceeded. Merge? Warn? Continue past limit?

3. **No XML section structure:** The methodology is not wrapped in a `<methodology>` XML tag per H-34 body format, which is a structural rigor gap.

4. **Error handling for chunk sequence failures:** No protocol specified for what to do if a chunk file is missing or corrupt mid-sequence.

**Improvement Path:**

Clarify Tier 2 as "LLM-as-ML-surrogate" pattern (no separate ML model; LLM performs NER inline). Document topic limit overflow behavior. Add error handling steps for chunk failures.

---

### Evidence Quality (0.72/1.00)

**Evidence present:**

- **ADR-003:** Referenced for citation anchor format (`#seg-{NNN}`) — specific, traceable
- **FR-009:** Referenced for topic segmentation feature requirement — specific
- **DISC-009:** Referenced for single-file format deprecation (99.8% data loss) — specific with quantified impact
- **TDD-ts-extractor.md:** Referenced with full relative path — traceable
- **BUG-002:** Referenced in INV-EXT-001 assert comment — defect traceability
- **EN-027, EN-031:** Referenced in document history for enabler traceability
- **PAT-001, PAT-003, PAT-004:** Named pattern identifiers consistently referenced

**Gaps:**

1. **Confidence adjustment values lack derivation:** The values `+0.05 (explicit keyword), +0.10 (NER confirms), -0.10 (ambiguous context), -0.05 (short segment)` are stated as fact with no empirical basis, calibration data reference, or derivation rationale. These are the core scoring mechanism; their validity cannot be verified.

2. **Topic boundary signal weights lack derivation:** The weights 0.95 (explicit transition), 0.90 (agenda reference), 0.85 (question markers), 0.75 (speaker change+pause), 0.70 (semantic shift) are stated without any derivation. No reference to how these were calibrated.

3. **Tier 2 ML claims unverifiable:** "NER EXTRACTION: Person names → speaker candidates, Organizations → context entities" — claims ML performs this, but there is no ML model in the agent's tool set. The agent's only tools are Read, Write, Glob, and Memory-Keeper. The LLM performs all "ML" work. The evidence for Tier 2 as a distinct tier is not present.

4. **Pattern IDs unresolvable:** PAT-001, PAT-003, PAT-004 are referenced throughout but no source file or registry path is given. A reviewer cannot verify these patterns exist or read their full specifications.

5. **All references are internal:** No external citations (academic NER literature, industry standards, benchmark data). For an extraction methodology making specific accuracy claims, internal-only evidence limits credibility.

6. **"99.8% data loss" claim (DISC-009):** The DISC-009 reference is cited but not linked. The 99.8% figure is significant — its provenance cannot be verified without the link.

**Improvement Path:**

Add derivation rationale or "calibrated empirically" notes for confidence adjustment values. Link PAT-XXX references to their source files. Link DISC-009 to its document. Convert Tier 2 description to accurately reflect LLM-based NER rather than implying a separate ML pipeline.

---

### Actionability (0.85/1.00)

**Evidence:**

- **Invocation Protocol:** Complete template with 4 required context fields in copy-pasteable markdown format — directly actionable
- **Mandatory Persistence section:** 3 numbered imperative steps with explicit MUST language
- **Input detection logic:** 3-case decision tree (index.json present / canonical without index / neither) — unambiguous
- **Chunked processing 4-step protocol:** Sequential with explicit constraints per step
- **Speaker ID regex patterns:** 4 specific regex patterns (lines 214-226) — directly implementable
- **Confidence formula:** Specific calculation with clamp and enumerated adjustments
- **Citation validation:** 3 binary pass/fail rules
- **INV-EXT-001 assert code:** Python pseudocode with 5 specific assertions — directly runnable
- **Self-critique checklist:** 6 items with checkbox format for pre-response validation
- **NPT-009 forbidden actions:** All 6 entries include "Consequence:" and implicit "Instead:" guidance

**Gaps:**

1. **Tier 2 not implementable:** The ML-Based extraction tier describes outcomes (person names, organizations) but provides no actionable mechanism for how to perform this in an LLM-only context. A developer cannot implement Tier 2 as written.

2. **Topic limit overflow undefined:** When 10 topics/hour limit is exceeded, there is no specified action. An implementer must make a judgment call.

3. **Memory-Keeper failure not addressed:** The MCP integration section shows happy-path only. No action defined if `mcp__memory-keeper__store` fails.

4. **Merge logic for cross-chunk deduplication:** "Deduplicate by text similarity (>90%)" — the similarity metric is not specified. Which algorithm? Levenshtein? Cosine? An implementer must choose without guidance.

**Improvement Path:**

Document Tier 2 as LLM-performing-NER (not separate ML model). Define topic limit overflow behavior. Add Memory-Keeper failure fallback. Specify deduplication similarity algorithm.

---

### Traceability (0.86/1.00)

**Evidence:**

- **Document History:** 5 version entries (1.0.0 through 1.4.2) with ISO dates and change descriptions — full versioning chain
- **Backlinks:** TDD-ts-extractor.md with full relative path, ADR-003 with full path
- **Forward Links:** ts-formatter.md (downstream agent), SKILL.md (parent skill)
- **Pattern references:** PAT-001, PAT-003, PAT-004, PAT-AGENT-001 — consistently cited across sections
- **Decision references:** DISC-009 (format deprecation), ADR-003 (citation format)
- **Requirement references:** FR-009 (topic segmentation)
- **Bug references:** BUG-002 (questions assert fix in INV-EXT-001)
- **Enabler references:** EN-027 (YAML compliance, v1.4.0), EN-031 (model config, v1.4.2)
- **Governance schema:** `docs/schemas/agent-governance-v1.schema.json` — explicit schema reference
- **Session context schema:** `docs/schemas/session_context.json` — schema traceability
- **Constitutional references:** 7 principles with enforcement labels in both files
- **Reference docs:** Chunked processing (`ts-extractor-chunked-processing.md`) and chunk strategies (`ts-extractor-chunk-strategies.md`) referenced by path

**Gaps:**

1. **PAT-XXX IDs lack source paths:** PAT-001, PAT-003, PAT-004 are cited throughout but no file path or registry location is provided. A reviewer cannot trace these to their definitions.

2. **DISC-009 lacks a link:** The decision to deprecate single-file format is attributed to DISC-009 with a 99.8% data loss claim, but no path to the DISC-009 document is provided.

3. **Reference docs not verified:** The supplementary references (`skills/transcript/reference/ts-extractor-chunked-processing.md`, `skills/transcript/reference/ts-extractor-chunk-strategies.md`) are cited but may not exist. If broken, this creates orphan references.

4. **No git-linked version control:** Version history has no PR numbers or commit hashes. Cannot verify what changed in each version from the history alone.

**Improvement Path:**

Add file paths to PAT-XXX pattern references. Add a relative path to DISC-009. Verify reference document existence. Consider adding PR/commit links to version history.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.72 | 0.82 | Add derivation rationale for confidence adjustment values (+0.05/+0.10/-0.10/-0.05) and topic boundary weights; link PAT-XXX to source files; link DISC-009; reframe Tier 2 as LLM-performing-NER to remove unverifiable ML claims |
| 2 | Completeness | 0.82 | 0.90 | Add XML section tags (`<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>`) to .md body per H-34; add `<purpose>` section; add L0 to output.levels; add `enforcement` block to governance YAML |
| 3 | Methodological Rigor | 0.88 | 0.93 | Document Tier 2 as LLM-based NER (no separate ML model); define topic limit overflow behavior (merge/warn); add chunk failure error handling; add deduplication algorithm specification |
| 4 | Actionability | 0.85 | 0.91 | Make Tier 2 implementable by specifying LLM prompt for NER; define topic overflow action; add Memory-Keeper failure fallback; specify deduplication similarity metric |
| 5 | Traceability | 0.86 | 0.92 | Add source file paths for PAT-001/003/004; add path to DISC-009; verify reference doc existence; add `enforcement` block |
| 6 | Internal Consistency | 0.92 | 0.95 | Align .md Capabilities forbidden actions wording with governance YAML NPT-009 format; document `warn_and_skip` as intentional domain-specific value |

---

## Leniency Bias Check

- [x] Each dimension scored independently (Evidence Quality scored 0.72 without letting strong Methodological Rigor pull it up)
- [x] Evidence documented for each score (specific line numbers and quoted content cited)
- [x] Uncertain scores resolved downward (Evidence Quality: uncertain between 0.72-0.78, resolved to 0.72; Completeness: uncertain between 0.82-0.87, resolved to 0.82)
- [x] First-draft calibration considered (this is v6 of an iterated deliverable — scored accordingly, but gaps are still scored as gaps regardless of iteration count)
- [x] No dimension scored above 0.95 without exceptional evidence (Internal Consistency scored 0.92 — highest score, justified by specific cross-file alignment evidence)

---

## Score Trajectory Analysis

| Version | Score | Delta | Notes |
|---------|-------|-------|-------|
| v1 | 0.836 | — | Baseline |
| v2 | 0.860 | +0.024 | Improvement |
| v3 | 0.837 | -0.023 | Regression (stricter rubric application) |
| v4 | 0.864 | +0.027 | Improvement |
| v5 | 0.878 | +0.014 | Improvement; gaps: NPT-014, missing output/persona |
| v6 | 0.846 | -0.032 | v5 gaps resolved but Evidence Quality scored more strictly (0.82→0.72); Completeness also tightened (0.87→0.82) |

**Note on v6 regression:** The v6 deliverable is objectively improved vs v5 — NPT-009-complete forbidden_actions confirmed, output block present, persona block present. However, applying the rubric with stricter literal criteria (especially "Score each dimension against rubric LITERALLY") against Evidence Quality reveals deeper gaps that v5 scoring was lenient on. The confidence adjustment values, topic boundary weights, and Tier 2 ML claims did not meet the 0.9+ rubric criteria for "all claims with credible citations." Scoring them at 0.82 in v5 was too generous; 0.72 is the correct literal application.

**Gap to PASS:** 0.92 - 0.846 = 0.074. This requires roughly a 0.37 improvement in Evidence Quality (to ~1.09, impossible) OR distributed improvements across multiple dimensions. Realistically: Evidence Quality to 0.85 (+0.013 weighted), Completeness to 0.90 (+0.016 weighted), Methodological Rigor to 0.93 (+0.010 weighted) = +0.039 additional weighted score = 0.885 composite. Full PASS requires deeper work across all 5 sub-threshold dimensions.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.846
threshold: 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.72
critical_findings_count: 0
iteration: 6
improvement_recommendations:
  - "Add derivation rationale for confidence adjustment values and topic boundary weights; link PAT-XXX to source files; reframe Tier 2 as LLM-based NER"
  - "Add XML section tags to .md body per H-34; add purpose section; add L0 to output.levels; add enforcement block to governance YAML"
  - "Document Tier 2 as LLM-performing NER (not separate ML); define topic limit overflow; add chunk failure handling; specify dedup algorithm"
  - "Make Tier 2 actionable with LLM prompt; define topic overflow action; add Memory-Keeper failure fallback"
  - "Add source file paths for PAT-001/003/004; add path to DISC-009; verify reference doc existence"
```

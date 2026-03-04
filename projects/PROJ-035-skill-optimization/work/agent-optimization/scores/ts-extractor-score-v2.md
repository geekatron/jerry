# Quality Score Report: ts-extractor Agent Definition

## L0 Executive Summary
**Score:** 0.860/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.82)
**One-line assessment:** The agent definition is methodologically strong and highly actionable, but the missing navigation table (H-23 violation) limits completeness; adding it and resolving the minor P-010 header omission would likely push the score above 0.92.

## Scoring Context
- **Deliverable:** `/Users/evorun/workspace/jerry/skills/transcript/agents/ts-extractor.md`
- **Companion YAML:** `/Users/evorun/workspace/jerry/skills/transcript/agents/ts-extractor.governance.yaml`
- **Deliverable Type:** Other (Agent Definition)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.836 (pre-fix iteration)
- **Scored:** 2026-03-03T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.860 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | No navigation table (H-23 violation); all content sections present but undiscoverable without nav |
| Internal Consistency | 0.20 | 0.87 | 0.174 | Version 1.4.2 consistent across header/YAML/footer; P-010 in YAML and footer but absent from line 14 header |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | Tiered extraction pipeline, 4-pattern speaker chain, confidence formula, chunked protocol all well-specified |
| Evidence Quality | 0.15 | 0.85 | 0.128 | Pattern references (PAT-001/003/004), ADR-003, DISC-009, FR-009 all cited; BUG-002 fix traceable |
| Actionability | 0.15 | 0.90 | 0.135 | Concrete regex patterns, numeric thresholds, MANDATORY checklists, invocation protocol, state handoff schema |
| Traceability | 0.10 | 0.85 | 0.085 | Nine design artifacts cited; forward/backlinks present; nav table absence slightly reduces navigability |
| **TOTAL** | **1.00** | | **0.860** | |

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**
The agent definition covers all major functional areas: identity/role (line 19-35), capabilities and tool list (line 38-55), input format specification (line 58-78), chunked processing protocol 4-step procedure (line 82-125), chunk selection strategies (line 128-133), tiered extraction pipeline Tier 1/2/3 (line 138-188), speaker identification PAT-003 (line 191-211), confidence scoring formula (line 213-230), citation requirements PAT-004 (line 232-252), topic segmentation FR-009 (line 254-294), output schema summary (line 298-311), invocation protocol (line 314-337), state management handoff schema (line 340-358), data integrity invariants INV-EXT-001 and INV-EXT-002 (line 362-407), constitutional compliance table (line 411-430), related documents (line 434-444), Memory-Keeper integration (line 446-457), and document history (line 459-468). Governance YAML covers all required fields (version, tool_tier, identity, guardrails, constitution, validation, session_context, capabilities).

**Gaps:**
1. **Navigation table absent (H-23 violation):** The document is 473 lines with 14 distinct major sections but has no navigation table after the header block. Per H-23, all Claude-consumed markdown files over 30 lines MUST include a navigation table. This is the primary completeness gap — without a nav table, section discoverability is degraded.
2. **Tier 1/2/3 failure fallback unspecified:** The tiered extraction pipeline (PAT-001) defines behavior when each tier fires, but does not define behavior when all three tiers produce zero matches for a segment (no explicit "skip segment" or "log and continue" instruction).
3. **Document version gap:** History table jumps from 1.1.0 to 1.3.0 (no 1.2.x entry). Acceptable for a revision history but creates a traceability minor gap.

**Improvement Path:**
Add a navigation table immediately after the frontmatter/header block listing all 14 major sections with anchor links. Add a fallback specification in the Tiered Extraction Pipeline section for the no-match case. These two changes would raise this dimension to approximately 0.90.

---

### Internal Consistency (0.87/1.00)

**Evidence:**
Version 1.4.2 is declared consistently in three places: the header block (line 11), the governance YAML (line 5), and the footer (line 471). The tool tier T4 in governance YAML is consistent with tools declared in the `.md` frontmatter (Read, Write, Glob + `mcpServers: memory-keeper: true`) — T4 is defined as "T2 base + Memory-Keeper" per `agent-development-standards.md`. The cognitive mode "convergent" is consistent between the `.md` body (line 34) and governance YAML `cognitive_mode: convergent` (line 16). The output schema version 1.1 referenced in the agent body (line 302) matches the version in `ts-extractor-output-schema.md` (confirmed read). INV-EXT-001 is referenced consistently in both the body (line 370) and governance YAML `post_completion_checks` (line 57 YAML).

**Gaps:**
1. **P-010 present in governance YAML but absent from line 14 header:** The constitutional compliance header (line 14) lists P-001, P-002, P-003, P-004, P-020, P-022. The governance YAML `principles_applied` (lines 44-51) includes P-010 (Task Tracking Integrity) which is absent from the header listing. The footer (line 472) includes P-010. This creates a three-way inconsistency: header omits P-010, YAML includes it, footer includes it.
2. **Minor:** Forbidden actions in governance YAML (lines 84-90) use shorter format ("Spawn recursive subagents (P-003)") compared to the full NPT-009 format used in the `.md` body (lines 49-54). This is not a contradiction but a format inconsistency between the two files.

**Improvement Path:**
Add P-020 and P-010 to the line 14 header compliance listing to match the governance YAML exactly. Upgrade the governance YAML `forbidden_actions` entries to NPT-009 format (matching the `.md` body) to satisfy AD-M-003 recommendation (the NPT-009 format is RECOMMENDED per `agent-development-standards.md`).

---

### Methodological Rigor (0.87/1.00)

**Evidence:**
The extraction methodology is well-structured across multiple complementary sub-methodologies:

1. **Tiered extraction pipeline (PAT-001):** Three tiers with explicit confidence ranges (0.85-1.0 for Tier 1, 0.70-0.85 for Tier 2, 0.50-0.70 for Tier 3) and specific patterns for each tier. The LLM prompt template for Tier 3 is provided inline.
2. **Speaker identification (PAT-003):** 4-pattern fallback chain with regex patterns, confidence scores per pattern, and examples for each.
3. **Confidence scoring (lines 215-230):** Explicit formula with base score, named adjustments (+0.05/-0.10 etc.), clamping, and threshold bands.
4. **Citation requirements (PAT-004):** JSON schema for citation object, three validation rules, explicit rejection criteria.
5. **Topic segmentation (FR-009):** ASCII table of boundary detection signals with weights, algorithm steps, constraints (minimum duration, maximum topics per hour), and output JSON schema.
6. **Chunked processing (4-step protocol):** Ordered steps with strategy selection table and merge rules per entity type.
7. **Data integrity invariants:** Two named invariants (INV-EXT-001, INV-EXT-002) with Python assertion code and implementation guidance.

**Gaps:**
1. **No-match fallback for tiered pipeline:** When a segment does not match any tier (no action item, decision, question, or topic boundary detected), the behavior is not explicitly stated. The tiered pipeline defines what happens on a match but not on a total miss.
2. **Tier 2 "ML-Based" is a category description, not an executable specification:** The agent is an LLM, not an ML pipeline. The Tier 2 description ("NER EXTRACTION", "INTENT CLASSIFICATION") uses ML framing without specifying how the LLM should approximate these operations. The framing is directionally correct but leaves implementation ambiguous for the executing agent.

**Improvement Path:**
Add one sentence after the Tier 3 block: "If all three tiers produce no match for a segment, skip the segment and log its segment_id in a `no_extraction` array." Clarify Tier 2 with LLM-accessible prompting guidance similar to Tier 3.

---

### Evidence Quality (0.85/1.00)

**Evidence:**
The agent definition cites specific design artifacts throughout:
- PAT-001 (tiered extraction pipeline), PAT-003 (speaker identification chain), PAT-004 (citation requirements)
- ADR-003 (bidirectional linking, anchors) — referenced for citation anchor format
- DISC-009 (99.8% data loss with Format A — rationale for chunked input enforcement)
- FR-009 (topic segmentation functional requirement)
- INV-EXT-001 (stats-array consistency invariant), INV-EXT-002 (semantic question filtering)
- BUG-002 (question count fix — comment in assertion code)
- TDD-ts-extractor.md backlink present in header (line 15)
- Governance YAML cites `docs/governance/JERRY_CONSTITUTION.md` and `docs/schemas/agent-governance-v1.schema.json` (in comment)

Reference files exist and are confirmed:
- `/Users/evorun/workspace/jerry/skills/transcript/reference/ts-extractor-output-schema.md` — full JSON schema
- `/Users/evorun/workspace/jerry/skills/transcript/reference/ts-extractor-chunk-strategies.md` — strategy details
- `/Users/evorun/workspace/jerry/skills/transcript/reference/ts-extractor-chunked-processing.md` — code examples

**Gaps:**
1. **Confidence score calibration not empirically grounded:** The base confidence scores (Tier 1 = 0.85-1.0, Tier 2 = 0.70-0.85, Tier 3 = 0.50-0.70) and adjustment values (+0.05, +0.10, -0.10, -0.05) are stated without citing an empirical basis or calibration study. They appear as design decisions without traceability to their origin.
2. **Schema validation reference absent from body:** The governance YAML comment references `docs/schemas/agent-governance-v1.schema.json` but the agent body (the LLM-facing content) does not reference the schema validator, reducing auditability for a reader of the `.md` alone.

**Improvement Path:**
Add a citation or ADR reference for the confidence score calibration (e.g., "Calibrated per PROJ-008 extraction testing results" or an ADR if one exists). Add a brief schema validation reference in the document header or a governance section.

---

### Actionability (0.90/1.00)

**Evidence:**
This is the strongest dimension. The agent provides immediately executable instructions:

1. **Concrete regex patterns** for all four speaker detection patterns (lines 196-210) — an implementing agent can apply these directly.
2. **Confidence formula** with explicit arithmetic (lines 216-225) — `final_confidence = clamp(base + sum(adjustments), 0.0, 1.0)`.
3. **Strategy selection table** (lines 97-101) maps task types to chunk loading strategies.
4. **Self-critique checklist** (lines 425-430) with 6 specific verification items an agent can check before responding.
5. **Invocation protocol** with mandatory context fields in code block (lines 320-327).
6. **State management handoff schema** with all output fields and their types (lines 344-356), including `next_agent: "ts-formatter"` for explicit downstream routing.
7. **Mandatory persistence instructions** (lines 332-336) with explicit consequence of non-compliance.
8. **Merge rules per entity type** (lines 117-121) for the chunk merge step.
9. **Boundary detection signal table** (lines 261-269) with weights for topic segmentation.
10. **Data integrity Python assertions** (lines 372-378) that can be used as a validation checklist.

**Gaps:**
1. **Error recovery path not specified:** When `index.json` exists but a chunk file is missing or corrupt, the invocation protocol (line 76-78) handles `canonical-transcript.json` presence but does not specify what ts-extractor should do if a referenced chunk file is absent.
2. **Memory-Keeper integration section (lines 446-457)** describes when to store/retrieve but does not specify what the stored content structure should be — only the key pattern is given. An agent could implement this inconsistently.

**Improvement Path:**
Add a missing-chunk error path to the input detection section. Add a sample Memory-Keeper stored object schema to the Memory-Keeper section. These are refinements, not blockers.

---

### Traceability (0.85/1.00)

**Evidence:**
Nine design artifacts are traceable by ID within the document:
- ADR-003 (citation format specification)
- DISC-009 (Format A deprecation rationale)
- FR-009 (topic segmentation requirement source)
- PAT-001, PAT-003, PAT-004 (pattern specifications)
- INV-EXT-001, INV-EXT-002 (named invariants)
- BUG-002 (defect fix referenced in assertion comment)

Bidirectional links:
- Backlink: TDD-ts-extractor.md (header line 15), ADR-003 (Related Documents)
- Forward links: ts-formatter.md, SKILL.md
- Reference files: three supplementary documents confirmed to exist

Governance YAML provides additional traceability:
- `constitution.reference: docs/governance/JERRY_CONSTITUTION.md`
- Principles mapped to specific enforcement rules (INV-EXT-001/002 in P-001 entry)
- `session_context.schema: docs/schemas/session_context.json`

**Gaps:**
1. **Navigation table absent reduces navigability:** Without a nav table, a reader cannot trace which section covers which topic without scanning the full 473-line document. This is a discoverable-but-slow traceability issue.
2. **PAT-001/PAT-003/PAT-004 not linked to their source documents:** The patterns are referenced by ID but no backlink to the design document where they were originally defined is provided. Only ADR-003 has an explicit backlink in the Related Documents section.
3. **Document version gap (1.1.0 → 1.3.0):** No 1.2.x entry in the history table makes it impossible to trace what changed between versions 1.1 and 1.3.

**Improvement Path:**
Add a navigation table. Add source document links for PAT-001, PAT-003, PAT-004 in the Related Documents section. Consider adding a 1.2.x entry or a note explaining the version gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.82 | 0.90 | Add navigation table after the frontmatter block (H-23 compliance). 14 sections with anchor links: Identity, Capabilities, Input Format, Chunked Processing Protocol, Chunk Selection Strategies Reference, Processing Instructions, Output Schema, Invocation Protocol, State Management, Data Integrity Invariants, Constitutional Compliance, Related Documents, Memory-Keeper MCP Integration, Document History. |
| 2 | Internal Consistency | 0.87 | 0.92 | Add P-010 to the line 14 constitutional compliance header to match the governance YAML. Currently header shows P-001/P-002/P-003/P-004/P-020/P-022; governance YAML includes P-010. |
| 3 | Methodological Rigor | 0.87 | 0.92 | Add an explicit no-match fallback for the tiered extraction pipeline. Suggested text after Tier 3: "If all three tiers produce no extraction for a segment, skip it and add its `segment_id` to a `skipped_segments` array in the report." |
| 4 | Evidence Quality | 0.85 | 0.90 | Add a citation or ADR reference for the confidence score calibration values (base scores and adjustment deltas). If no ADR exists, note "Calibrated empirically during PROJ-008 extraction validation." |
| 5 | Traceability | 0.85 | 0.90 | Add source document links for PAT-001, PAT-003, PAT-004 in the Related Documents section (currently only ADR-003 has a backlink). |
| 6 | Actionability | 0.90 | 0.93 | Add missing-chunk error path to Input Format section: "If a chunk file referenced in index.json is missing, log the chunk_id as `chunk_missing`, skip it, and continue with remaining chunks." |

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness: considered 0.85 but nav table gap is a HARD rule violation — resolved to 0.82; Internal Consistency: considered 0.90 but P-010 header inconsistency reduces to 0.87)
- [x] First-draft calibration considered (this is v1.4.2 — a mature revision; calibration anchors adjusted accordingly; scores above 0.85 are justified for a mature agent definition)
- [x] No dimension scored above 0.95 without exceptional evidence (highest dimension is Actionability at 0.90)

## Verdict Rationale

Composite 0.860 falls in the REVISE band (0.85-0.91). The primary blocker is the missing navigation table (H-23 HARD rule violation), which suppresses the Completeness dimension from what would otherwise be a ~0.90 score. The agent definition is substantively excellent — the methodology, evidence, and actionability are all strong — but the structural H-23 gap plus the minor P-010 header inconsistency are straightforward fixes. After applying Priority 1 and Priority 2 recommendations, the projected composite rises to approximately 0.895-0.915 (within striking distance of 0.92). A third targeted iteration addressing Priorities 3-5 should push the composite above the 0.92 threshold.

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.860
threshold: 0.92
weakest_dimension: Completeness
weakest_score: 0.82
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add navigation table (H-23 compliance) — highest impact single fix"
  - "Add P-010 to line 14 constitutional compliance header"
  - "Add no-match fallback to tiered extraction pipeline"
  - "Cite source for confidence score calibration values"
  - "Add source document links for PAT-001/PAT-003/PAT-004"
  - "Add missing-chunk error path to Input Format section"
```

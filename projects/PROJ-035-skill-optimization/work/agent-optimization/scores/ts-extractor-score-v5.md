# Quality Score Report: ts-extractor Agent Definition

## L0 Executive Summary

**Score:** 0.878/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.82)
**One-line assessment:** The P-004 fix resolved the primary Internal Consistency blocker (0.83 -> 0.90), moving the composite from 0.864 to 0.878, but the deliverable remains below the 0.92 PASS threshold; Evidence Quality and Completeness gaps now drive the delta.

---

## Scoring Context

- **Deliverable:** `/Users/evorun/workspace/jerry/skills/transcript/agents/ts-extractor.md` + `ts-extractor.governance.yaml`
- **Deliverable Type:** Agent Definition (dual-file architecture per H-34)
- **Criticality Level:** C2 (standard agent definition)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Scores:** v1=0.836, v2=0.860, v3=0.837 (regression), v4=0.864, v5=0.878
- **Scored:** 2026-03-03T00:00:00Z
- **Iteration:** 5

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.878 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All required sections present; governance YAML forbidden_actions short-form not NPT-009; no persona block; no trigger keywords in description |
| Internal Consistency | 0.20 | 0.90 | 0.180 | P-004 fix verified (now "Hard" in compliance table, consistent with governance YAML and Forbidden Actions); no logical contradictions remain |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | 3-tier pipeline, 4-pattern speaker ID, quantified confidence formula, 4-step chunked protocol, topic segmentation with boundary weights |
| Evidence Quality | 0.15 | 0.82 | 0.123 | Named references (ADR-003, FR-009, DISC-009) present; confidence adjustment values and topic constraint thresholds lack derivation rationale |
| Actionability | 0.15 | 0.90 | 0.135 | Invocation template, self-critique checklist, pseudocode assertions, NPT-009 forbidden actions with consequences |
| Traceability | 0.10 | 0.84 | 0.084 | Version history, ADR/FR/PAT references present; PAT-XXX pattern docs not hyperlinked; reference document paths not verified |
| **TOTAL** | **1.00** | | **0.878** | |

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**

All required structural elements for H-34 dual-file architecture are present:

- Official frontmatter: `name`, `description`, `model`, `tools`, `mcpServers` — all present and populated
- Governance YAML required fields: `version: 1.4.2`, `tool_tier: T4`, `identity.role: Entity Extraction Specialist`, `identity.expertise` (6 entries), `identity.cognitive_mode: convergent`
- Navigation table covers 10 sections with purpose descriptions (H-23 compliant)
- Full processing methodology: 3-tier extraction pipeline, 4-step chunked protocol, speaker identification chain, confidence scoring formula, topic segmentation algorithm
- Data integrity invariants: INV-EXT-001 and INV-EXT-002 with Python pseudocode
- Constitutional compliance table and self-critique checklist
- Document history with 5 version entries
- State management output schema with all field names
- Memory-Keeper integration section with key pattern
- Forward and backward links (TDD, ADR-003, ts-formatter, SKILL.md)

**Gaps:**

1. Governance YAML `capabilities.forbidden_actions` uses short-form entries (e.g., "Spawn recursive subagents (P-003)") rather than NPT-009 complete format. The `.md` body Capabilities section has full NPT-009 format, but the YAML does not mirror this. The `capabilities.forbidden_action_format` field is absent (omission implies NPT-014/legacy per AD-M-003/ADR-002).
2. Frontmatter `description` field ("Extracts semantic entities (speakers, actions, decisions, questions, topics) from parsed transcripts") does not include explicit trigger keywords per AD-M-003 ("WHAT the agent does, WHEN to invoke it, and at least one trigger keyword" — the trigger keyword component is absent).
3. Governance YAML has no `persona` block (AD-M-006: SHOULD declare tone, communication_style, audience_level).
4. Governance YAML has no `output` block (`output.required`, `output.location`, `output.levels` per AD-M-004/AD-M-008 MEDIUM standards). The agent clearly produces output artifacts but this is not declared in the governance schema.

**Improvement Path:**

Upgrade governance YAML `forbidden_actions` to NPT-009 format. Add trigger keywords to frontmatter description (e.g., "Triggers: extract entities, speaker identification, action items, transcript extraction"). Add `persona` block to governance YAML. Add `output` block with `required: true`, `location: {output_path}/extraction-report.json`, `levels: [L1]`.

---

### Internal Consistency (0.90/1.00)

**Evidence:**

**P-004 Fix Verified (Primary Objective of v5):**

The Constitutional Compliance table at line 434 now reads:
```
| P-004 (Provenance) | **Hard** | ALL extractions have citations |
```

This is consistent with:
- Governance YAML `principles_applied` line 47: `P-004: Provenance (Hard - all extractions require citations)` — matches
- Forbidden Actions section in `.md` line 67: `- **P-004 VIOLATION:** DO NOT extract entities without citation to source.` — matches Hard enforcement

The v4 contradiction (table: "Soft", YAML + Forbidden Actions: "Hard") is fully resolved.

**Other Consistency Checks Passed:**

- Version: 1.4.2 consistent across frontmatter (implied), `.md` header (line 11), governance YAML (line 5), and footer (line 487)
- Model: `sonnet` consistent across frontmatter (line 4), identity header (line 13), and governance `default_model: sonnet` (line 18)
- Cognitive mode: `Convergent` in `.md` (line 49), `convergent` in governance (line 16) — consistent (case difference is not a contradiction)
- Tool tier: `tools: Read, Write, Glob` (frontmatter) + `mcpServers: memory-keeper: true` (MCP) is consistent with `tool_tier: T4` declaration. The frontmatter is a restrictive override within the T4 tier — not a contradiction.
- P-010: Present and "Hard" in header (line 14), compliance table (line 437), footer (line 488), and governance YAML (line 48) — fully consistent
- INV-EXT-001 referenced consistently in invariants section, compliance table, self-critique checklist, and governance `post_completion_checks`
- P-002: Listed as "Medium" in compliance table (line 432) AND governance YAML (line 45) — internally consistent. Present in Forbidden Actions section using "VIOLATION" language, but Forbidden Actions can list items at any enforcement level; the authoritative classification is the compliance table and YAML, which agree.

**Remaining Minor Cross-File Presentation Difference:**

The `.md` body Capabilities section uses full NPT-009 format for all forbidden_actions. The governance YAML `capabilities.forbidden_actions` uses short-form (legacy NPT-014). This is a presentation style difference between files, not a logical contradiction about facts, rules, or enforcement levels.

**Gaps:**

No logical contradictions remain. One presentation-style difference (NPT-009 in MD body vs. NPT-014 in governance YAML forbidden_actions) constitutes a structural inconsistency without factual contradiction.

**Improvement Path:**

Align governance YAML `capabilities.forbidden_actions` to NPT-009 format to match the `.md` body (addresses both Completeness and Internal Consistency dimensions simultaneously).

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

The extraction methodology is systematically specified with concrete, testable rules:

- **3-tier extraction pipeline (PAT-001):** Rule-Based (confidence 0.85-1.0) → ML/Context-Based (0.70-0.85) → LLM-Based (0.50-0.70). Each tier has named patterns, regex examples, and explicit confidence values per pattern.
- **Confidence calculation formula:** Named formula with 4 named adjustment factors (+0.05 explicit keyword, +0.10 NER confirms entity, -0.10 ambiguous context, -0.05 short segment <10 words), `clamp()` function with range [0.0, 1.0], and output thresholds (HIGH ≥0.85, MEDIUM 0.70-0.84, LOW <0.70).
- **Speaker identification (PAT-003):** 4-pattern fallback chain with confidence per pattern (0.95 VTT tags, 0.90 prefix pattern, 0.85 bracket pattern, 0.60 contextual carry-forward) and regex strings for each pattern.
- **Topic segmentation (FR-009):** 5 boundary signal types with explicit weights (0.95, 0.90, 0.85, 0.75, 0.70), 4-step algorithm pseudocode, and 3 output constraints (min 30s, max 10/hour, 100% coverage).
- **Chunked processing protocol:** 4-step sequenced protocol (Read Index → Plan → Process → Merge), chunk selection strategy table with 3 named strategies (Sequential, Index Only, Selective) with Use-For and Cost columns.
- **Merge rules:** Per-entity-type deduplication rules (speakers: sum segment_count, highest-confidence pattern; action items: >90% text similarity; decisions: semantic similarity; questions: answered status tracking; topics: span merging across chunk boundaries).
- **Data integrity:** Formal invariants (INV-EXT-001, INV-EXT-002) with Python pseudocode assertions and "Why This Matters" rationale.
- **Citation validation:** 3 explicit validation rules (segment_id must exist, text_snippet must be substring, anchor format must match ADR-003).

**Gaps:**

Tier 2 ("ML-Based") describes NER extraction and intent classification but does not specify the mechanism. For an LLM agent, this is ambiguous: does it mean the LLM applies NER reasoning contextually, or does it require an external ML service? If LLM-native reasoning, naming it "ML-Based" may mislead implementers into expecting a separate ML service dependency. This is a minor naming/clarity gap rather than a methodological deficiency.

**Improvement Path:**

Clarify whether Tier 2 "ML-Based" means LLM-native NER reasoning applied contextually (no external service) or an external ML call. If LLM-native, consider renaming to "Context-Based NER" to eliminate infrastructure ambiguity.

---

### Evidence Quality (0.82/1.00)

**Evidence:**

Named references supporting claims:

- `DISC-009`: cited for "Format A (single file) is DEPRECATED per DISC-009 (99.8% data loss)" — strong causal attribution
- `ADR-003`: cited for citation anchor format standard (`#seg-{NNN}`)
- `FR-009`: cited for Topic Segmentation requirement origin
- `PAT-001`, `PAT-003`, `PAT-004`: cited for extraction patterns and citation requirement patterns
- `BUG-002`: referenced inline in assertion comment for questions count fix — demonstrates bug-driven invariant provenance
- `INV-EXT-001`, `INV-EXT-002`: formally named invariants with "Why This Matters" rationale sections
- TDD-ts-extractor.md: linked as backlink with full path
- Reference documents named for detailed specifications (`ts-extractor-chunked-processing.md`, `ts-extractor-chunk-strategies.md`, `ts-extractor-output-schema.md`)

**Gaps:**

1. The confidence adjustment values (+0.05, +0.10, -0.10, -0.05) are specific quantitative claims with no cited derivation. They appear to be design choices but are presented as facts. No "empirically derived from X" note, no FR reference, no rationale.
2. Topic segmentation constraints — "Minimum topic duration: 30 seconds" and "Maximum topics per hour: 10" — are specific quantitative claims with no cited basis (no FR reference or rationale note).
3. "99.8% data loss" (DISC-009) is a strong quantitative claim. DISC-009 is referenced by name but not hyperlinked; independent verification requires locating DISC-009 in the project tree.
4. PAT-001, PAT-003, PAT-004 are named extensively but their source documents are not hyperlinked, preventing direct verification without knowing the PAT document location.
5. "max_extractions: 100" in governance YAML input_validation — no cited basis for this constraint.

**Improvement Path:**

Add rationale notes for confidence adjustment values (e.g., "empirically derived from PROJ-008 testing; see TDD-ts-extractor Section 4.2"). Add FR citations or rationale for topic constraint values. Add hyperlinks to DISC-009, PAT-001, PAT-003, PAT-004 source documents using full paths. Add FR or design decision reference for the max_extractions: 100 constraint in governance YAML.

---

### Actionability (0.90/1.00)

**Evidence:**

The document provides highly actionable guidance for both implementers and consumers:

- **Invocation template:** Complete context block with 4 named fields (`Canonical JSON Path`, `Output Path`, `Packet ID`, `Confidence Threshold`)
- **Mandatory persistence steps:** Numbered 3-step sequence (Write report → Validate citations → Include stats)
- **Self-critique checklist:** 6 checkbox items covering P-004, P-022, P-002, P-001, INV-EXT-001, INV-EXT-002 — agent applies before every response
- **Data integrity assertions:** Python `assert` pseudocode statements directly translatable to validation logic
- **Forbidden Actions with NPT-009 format:** Each entry includes consequence and "Instead" alternative — directly actionable behavior correction
- **Strategy selection table:** 3-way chunk-loading decision with "Use For" and "Cost" columns
- **Input detection logic:** 3-case decision tree (chunked → proceed, canonical-only → error with instruction, neither → error with message)
- **State management schema:** Complete output key (`ts_extractor_output`) with all field names, types, and `next_agent: "ts-formatter"` pointer

**Gaps:**

1. Output path conventions are not canonically specified. The invocation template says "provide output path" but does not give a canonical path pattern (e.g., `projects/{project}/work/transcripts/{packet-id}/extraction-report.json`). The user must determine the correct location without guidance.
2. The Memory-Keeper key pattern `jerry/{project}/transcript/{packet-id}/extraction` is provided but not cross-referenced against the MCP namespace standard from `mcp-tool-standards.md`. A link or explicit compliance statement would strengthen traceability.

**Improvement Path:**

Add a canonical output path pattern to the Invocation Protocol section (e.g., default to `{project_root}/work/transcripts/{packet_id}/extraction-report.json`). Add a cross-reference note confirming the Memory-Keeper key pattern complies with `mcp-tool-standards.md` namespace conventions.

---

### Traceability (0.84/1.00)

**Evidence:**

Strong traceability chain from requirements to implementation:

- **Document history:** 5 version entries with ISO dates and change descriptions (1.0.0 through 1.4.2)
- **Requirement references:** FR-009 (topic segmentation), DISC-009 (format deprecation rationale)
- **Architecture references:** ADR-003 (citation anchor format)
- **Pattern references:** PAT-001 (tiered extraction), PAT-003 (speaker ID), PAT-004 (citation generation)
- **Bug fix reference:** BUG-002 in assertion comment (questions count — traceable to bug database)
- **Invariant naming:** INV-EXT-001, INV-EXT-002 with formal definitions and rationale
- **Backlinks:** TDD-ts-extractor.md (full path), ADR-003 (full path)
- **Forward links:** ts-formatter.md, SKILL.md
- **Governance traceability:** `constitution.reference: docs/governance/JERRY_CONSTITUTION.md`, `session_context.schema: docs/schemas/session_context.json` with schema version
- **Version consistency:** 1.4.2 confirmed in header, governance YAML, and footer

**Gaps:**

1. PAT-001, PAT-003, PAT-004 are referenced throughout the document but not hyperlinked. The full file path for PAT documents is not provided, requiring independent discovery.
2. Reference documents (`ts-extractor-chunked-processing.md`, `ts-extractor-chunk-strategies.md`, `ts-extractor-output-schema.md`) are mentioned with directory prefix `skills/transcript/reference/` but without full paths and without confirmation of existence in the current document.
3. `session_context.schema: docs/schemas/session_context.json` — the schema file path is asserted but not validated by hyperlink in the governance YAML.

**Improvement Path:**

Add full hyperlinks to PAT-001, PAT-003, PAT-004 source documents. Confirm reference document paths with hyperlinks in the sections that reference them. Convert bare path references in governance YAML to resolvable paths where applicable.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness + Internal Consistency | 0.87 / 0.90 | 0.92 / 0.95 | Upgrade governance YAML `capabilities.forbidden_actions` to NPT-009 format (Principle VIOLATION: NEVER action — Consequence: impact) matching the `.md` body; add `capabilities.forbidden_action_format: NPT-009-complete` |
| 2 | Evidence Quality | 0.82 | 0.88 | Add rationale for confidence adjustment values (+0.05, +0.10, -0.10, -0.05) — cite PROJ-008 testing or add a design note |
| 3 | Evidence Quality | 0.82 | 0.88 | Add FR citations or rationale notes for topic constraints (min 30s, max 10/hour) |
| 4 | Traceability | 0.84 | 0.90 | Add hyperlinks to PAT-001, PAT-003, PAT-004 source documents with full repo-relative paths |
| 5 | Completeness | 0.87 | 0.92 | Add `output` block to governance YAML (`required: true`, `location`, `levels`) per AD-M-004 |
| 6 | Completeness | 0.87 | 0.92 | Add trigger keywords to frontmatter `description` field per AD-M-003 (e.g., append "Triggers: extract transcript entities, speaker identification, action items, decisions") |
| 7 | Completeness | 0.87 | 0.92 | Add `persona` block to governance YAML (tone, communication_style, audience_level) per AD-M-006 |
| 8 | Methodological Rigor | 0.91 | 0.94 | Clarify Tier 2 "ML-Based" label — rename to "Context-Based NER" if LLM-native to eliminate infrastructure ambiguity |

---

## P-004 Fix Verification

**Finding: P-004 enforcement level inconsistency from v4 is RESOLVED.**

| Location | P-004 Enforcement | Content |
|----------|------------------|---------|
| Compliance table `.md` line 434 | **Hard** (FIXED) | `\| P-004 (Provenance) \| **Hard** \| ALL extractions have citations \|` |
| Governance YAML `principles_applied` line 47 | Hard | `P-004: Provenance (Hard - all extractions require citations)` |
| Forbidden Actions `.md` line 67 | Hard (VIOLATION language) | `- **P-004 VIOLATION:** DO NOT extract entities without citation to source.` |

All three locations are now consistent at Hard enforcement. The v4 blocker (table: "Soft" vs YAML + Forbidden Actions: "Hard") is fully resolved.

**Impact on Internal Consistency score:** 0.83 → 0.90 (+0.07). No logical contradictions remain.

---

## Version Comparison

| Version | Score | Verdict | Primary Issue | Delta |
|---------|-------|---------|---------------|-------|
| v1 | 0.836 | REVISE | Baseline | — |
| v2 | 0.860 | REVISE | Baseline improved | +0.024 |
| v3 | 0.837 | REVISE | REGRESSION: P-010 missing from compliance table body | -0.023 |
| v4 | 0.864 | REVISE | P-010 fixed; P-004 enforcement contradiction blocks 0.92 | +0.027 |
| v5 | 0.878 | REVISE | P-004 fixed; Evidence Quality + Completeness gaps now drive delta | +0.014 |

**Score delta v4 → v5:** +0.014 (Internal Consistency: 0.83 → 0.90, weighted contribution +0.014)

**Remaining gap to 0.92 threshold:** 0.042

**Path to PASS:** Addressing Priority 1 (governance YAML NPT-009 alignment) would raise Completeness to ~0.90 (+0.006 composite) and Internal Consistency to ~0.93 (+0.006 composite). Addressing Priorities 2-3 (evidence rationale) would raise Evidence Quality to ~0.87 (+0.008 composite). Combined, these three actions would move the composite to approximately 0.898 — still below 0.92. Completing Priorities 4-7 (hyperlinks, output block, trigger keywords, persona block) would raise Completeness to ~0.93 and Traceability to ~0.88, adding approximately another +0.020 composite. The full priority list executed together would bring the deliverable above 0.92.

---

## Session Context Output

```yaml
verdict: REVISE
composite_score: 0.878
threshold: 0.92
weakest_dimension: evidence_quality
weakest_score: 0.82
critical_findings_count: 0
iteration: 5
improvement_recommendations:
  - "Upgrade governance YAML forbidden_actions to NPT-009 format; add forbidden_action_format: NPT-009-complete"
  - "Add rationale for confidence adjustment values (+0.05, +0.10, -0.10, -0.05) — cite PROJ-008 or design note"
  - "Add FR citations for topic constraints (min 30s duration, max 10/hour)"
  - "Add hyperlinks to PAT-001, PAT-003, PAT-004 source documents with full repo-relative paths"
  - "Add output block to governance YAML (required, location, levels) per AD-M-004"
  - "Add trigger keywords to frontmatter description field per AD-M-003"
  - "Add persona block to governance YAML per AD-M-006"
  - "Clarify Tier 2 ML-Based mechanism or rename to Context-Based NER"
```

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency: chose 0.90 not 0.93 given NPT-009 format inconsistency between files; Evidence Quality: held at 0.82, not raised, despite no new changes)
- [x] v5 is a targeted revision, not first draft — calibration adjusted accordingly
- [x] No dimension scored above 0.95 (highest is Methodological Rigor at 0.91)
- [x] P-004 fix independently verified against all three locations (compliance table, governance YAML, Forbidden Actions)
- [x] Internal Consistency improvement (+0.07) justified by specific removal of the only logical contradiction (P-004 "Soft"/"Hard" mismatch); no other contradictions found

---

*Score Report: ts-extractor-score-v5.md*
*Agent: adv-scorer v1.0.0*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-03*

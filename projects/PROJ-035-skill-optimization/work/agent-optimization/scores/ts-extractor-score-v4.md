# Quality Score Report: ts-extractor Agent Definition

## L0 Executive Summary

**Score:** 0.864/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.83)

**One-line assessment:** The P-010 consistency fix resolved the v3 regression, but a distinct P-004 enforcement-level contradiction (labeled "Soft" in the Constitutional Compliance table, "Hard" in governance YAML and Forbidden Actions) blocks the score from crossing 0.92 PASS threshold.

---

## Scoring Context

- **Deliverable:** `/Users/evorun/workspace/jerry/skills/transcript/agents/ts-extractor.md` + `ts-extractor.governance.yaml`
- **Deliverable Type:** Agent Definition (dual-file architecture per H-34)
- **Criticality Level:** C2 (standard agent definition)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Scores:** v2=0.860, v3=0.837 (regression), v4=0.864
- **Scored:** 2026-03-03T00:00:00Z
- **Iteration:** 4

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.864 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All required sections present; governance YAML forbidden_actions use short-form not NPT-009 |
| Internal Consistency | 0.20 | 0.83 | 0.166 | P-010 fix confirmed; NEW gap: P-004 is "Soft" in compliance table but "Hard" in governance YAML and Forbidden Actions |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | 3-tier pipeline, 4-pattern speaker ID, quantified confidence adjustments, 4-step chunked protocol |
| Evidence Quality | 0.15 | 0.82 | 0.123 | Named references (ADR-003, FR-009, DISC-009) present; confidence adjustment values and constraint thresholds lack derivation rationale |
| Actionability | 0.15 | 0.90 | 0.135 | Invocation template, self-critique checklist, pseudocode assertions, NPT-009 forbidden actions with consequences |
| Traceability | 0.10 | 0.84 | 0.084 | Version history, ADR/FR/PAT references present; PAT-XXX pattern docs not hyperlinked |
| **TOTAL** | **1.00** | | **0.864** | |

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**

All required structural elements are present:
- Official frontmatter: `name`, `description`, `model`, `tools`, `mcpServers` — all populated correctly
- Governance YAML required fields: `version: 1.4.2`, `tool_tier: T4`, `identity.role`, `identity.expertise` (6 entries), `identity.cognitive_mode: convergent`
- Navigation table covers 10 sections with purpose descriptions (H-23 compliant)
- Full processing methodology: 3-tier extraction pipeline, 4-step chunked protocol, speaker identification, confidence scoring, topic segmentation
- Data integrity invariants: INV-EXT-001 and INV-EXT-002 with rationale
- Constitutional compliance table and self-critique checklist
- Document history with 5 version entries
- State management output schema
- Memory-Keeper integration section
- Forward and backward links

**Gaps:**

- Governance YAML `capabilities.forbidden_actions` uses short-form entries (e.g., "Spawn recursive subagents (P-003)") rather than the NPT-009 complete format recommended by AD-M-003 and the guardrails template. The markdown body Capabilities section has the full NPT-009 format, but the YAML does not mirror this.
- Frontmatter `description` field is functional but does not include explicit trigger keywords per AD-M-003 ("WHAT the agent does, WHEN to invoke it, and at least one trigger keyword" — the trigger keyword component is absent).
- Governance YAML has no `persona` block (AD-M-006: SHOULD declare tone, communication_style, audience_level).

**Improvement Path:**

Upgrade governance YAML `forbidden_actions` to NPT-009 format matching the `.md` body. Add trigger keywords to frontmatter description. Add `persona` block to governance YAML.

---

### Internal Consistency (0.83/1.00)

**Evidence:**

**P-010 Fix Verified (Primary Objective of v4):**

- Line 14 header: `P-001, P-002, P-003, P-004, P-010, P-020, P-022` — P-010 present
- Line 437 table body: `| P-010 (Stats Integrity) | **Hard** | Stats counts recalculated from arrays, never from intermediate counters (INV-EXT-001) |` — P-010 row present
- Line 488 footer: `P-010 (Hard - stats integrity)` — P-010 present
- Governance YAML `principles_applied`: `P-010: Task Tracking Integrity (Hard - stats MUST match actual array contents)` — P-010 present

The v3 regression (P-010 in header/footer but absent from table body) is confirmed resolved.

**Remaining Inconsistency — P-004 Enforcement Level:**

The Constitutional Compliance table (line 434) lists:
```
| P-004 (Provenance) | Soft | ALL extractions have citations |
```

However:
- Forbidden Actions section in `.md` has: `- **P-004 VIOLATION:** DO NOT extract entities without citation to source. Consequence: ...`  — NPT-009 format implies Hard enforcement
- Governance YAML `principles_applied` states: `P-004: Provenance (Hard - all extractions require citations)`

P-004 enforcement level is "Soft" in the compliance table but "Hard" in both the YAML and the Forbidden Actions section. This is a genuine internal contradiction unrelated to P-010.

**Other consistency checks passed:**

- Version: 1.4.2 consistent across frontmatter (implied by name), `.md` header, governance YAML, and footer
- Model: `sonnet` consistent across frontmatter, header, and governance `default_model`
- Cognitive mode: `Convergent` in `.md`, `convergent` in governance — consistent
- Tool tier: `tools: Read, Write, Glob` (native) + `mcpServers: memory-keeper: true` (MCP) is consistent with `tool_tier: T4` (T2 tools + Memory-Keeper)
- INV-EXT-001 referenced consistently in invariants section, compliance table, self-critique checklist, and governance `post_completion_checks`

**Gaps:**

P-004 enforcement level contradiction: table says "Soft", YAML and Forbidden Actions imply "Hard".

**Improvement Path:**

Change the Constitutional Compliance table P-004 row from "Soft" to "**Hard**" to match governance YAML and Forbidden Actions section enforcement level.

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

The extraction methodology is genuinely systematic and well-specified:

- **3-tier extraction pipeline (PAT-001):** Rule-Based (0.85-1.0) → ML-Based (0.70-0.85) → LLM-Based (0.50-0.70). Each tier has named patterns with explicit confidence values and regex examples.
- **Confidence calculation formula:** Named formula with 4 adjustment factors (+0.05 explicit keyword, +0.10 NER confirmation, -0.10 ambiguous context, -0.05 short segment), `clamp()` function, explicit thresholds (HIGH ≥0.85, MEDIUM 0.70-0.84, LOW <0.70).
- **Speaker identification (PAT-003):** 4-pattern fallback chain with confidence per pattern (0.95, 0.90, 0.85, 0.60) and regex for each pattern.
- **Topic segmentation:** 5 boundary signal types with weights (0.95, 0.90, 0.85, 0.75, 0.70), algorithm pseudocode, and 3 constraints (min 30s, max 10/hour, 100% coverage).
- **Chunked processing:** 4-step sequenced protocol (Read Index → Plan → Process → Merge), chunk selection strategy table with 3 options.
- **Merge rules:** Per-entity-type deduplication rules (speakers: sum segment_count; action items: 90% text similarity; decisions: semantic similarity; questions: answered status tracking; topics: span merging).
- **Data integrity:** Formal invariants with pseudocode assertions (not just prose).
- **Invocation:** Required context template with named fields.

**Gaps:**

The Tier 2 (ML-Based) section describes NER extraction and intent classification but does not specify the mechanism (embedded model, API, heuristic approximation). For an agent operating as an LLM, "ML-Based" is ambiguous — it may mean the LLM itself applying NER reasoning, or an external ML service. This ambiguity is minor but represents a methodological gap.

**Improvement Path:**

Clarify whether Tier 2 "ML-Based" means LLM-native NER reasoning or an external ML service call. If LLM-native, rename to "Context-Based NER" to eliminate ambiguity about ML infrastructure requirements.

---

### Evidence Quality (0.82/1.00)

**Evidence:**

Named references supporting claims:

- `DISC-009`: cited for "Format A (single file) is DEPRECATED per DISC-009 (99.8% data loss)"
- `ADR-003`: cited for citation anchor format (`#seg-{NNN}`)
- `FR-009`: cited for Topic Segmentation requirement
- `PAT-001`, `PAT-003`, `PAT-004`: cited for extraction patterns and citation requirements
- `BUG-002`: referenced in assertion comment for questions count
- `INV-EXT-001`, `INV-EXT-002`: formally named invariants with rationale sections
- TDD document linked as backlink
- Reference documents named for chunked processing, chunk strategies, and output schema

**Gaps:**

- The confidence adjustment values (+0.05, +0.10, -0.10, -0.05) are specific quantitative claims with no cited derivation. These appear to be design choices but are presented as facts without rationale.
- "Maximum topics per hour: 10" constraint has no cited basis — neither an FR reference, nor a rationale note.
- "Minimum topic duration: 30 seconds" — same gap.
- "99.8% data loss" (DISC-009) is a strong quantitative claim. DISC-009 is referenced but not linked; verifying this claim requires locating DISC-009 independently.
- PAT-001, PAT-003, PAT-004 are named but their source documents are not hyperlinked, preventing direct verification.

**Improvement Path:**

Add rationale notes for the confidence adjustment values (e.g., "empirically derived from PROJ-008 testing"). Add FR references for the topic constraint values (min duration, max count). Add hyperlinks to PAT-XXX source documents.

---

### Actionability (0.90/1.00)

**Evidence:**

The document provides highly actionable guidance for both implementers and users:

- **Invocation template:** Complete context block with named fields (`Canonical JSON Path`, `Output Path`, `Packet ID`, `Confidence Threshold`)
- **Mandatory persistence steps:** Numbered list (Write report → Validate citations → Include stats)
- **Self-critique checklist:** 6 checkbox items covering P-004, P-022, P-002, P-001, INV-EXT-001, INV-EXT-002 — actionable before every response
- **Data integrity assertions:** Pseudocode `assert` statements implementers can directly translate
- **Forbidden Actions with NPT-009 format:** Each entry includes consequence and "Instead" alternative — directly actionable
- **Strategy selection table:** 3-way decision for chunk loading strategy with "Use For" and "Cost" columns
- **Input detection logic:** 3-case decision tree (chunked/error/not-found)
- **State management schema:** Output key with all field names and types for ts-formatter handoff

**Gaps:**

- Output path conventions are not fully specified. The invocation template says "provide output path" but does not specify a canonical path pattern (e.g., `projects/{project}/work/transcripts/{packet-id}/extraction-report.json`). A user must infer the correct location.
- The Memory-Keeper key pattern `jerry/{project}/transcript/{packet-id}/extraction` is provided but not validated against the MCP key namespace standard from `mcp-tool-standards.md`.

**Improvement Path:**

Add a canonical output path pattern to the Invocation Protocol. Cross-reference the Memory-Keeper key pattern against the MCP namespace standard.

---

### Traceability (0.84/1.00)

**Evidence:**

Strong traceability chain established:

- **Document history:** 5 version entries with dates and change descriptions (1.0.0 through 1.4.2)
- **Requirement references:** FR-009 (topic segmentation), DISC-009 (format deprecation)
- **Architecture references:** ADR-003 (citation anchors)
- **Pattern references:** PAT-001 (tiered extraction), PAT-003 (speaker ID), PAT-004 (citation)
- **Bug fix reference:** BUG-002 in assertion comment
- **Invariant naming:** INV-EXT-001, INV-EXT-002 with formal definitions
- **Backlinks:** TDD-ts-extractor.md, ADR-003
- **Forward links:** ts-formatter.md, SKILL.md
- **Governance traceability:** `constitution.reference`, `session_context.schema` with schema version
- **Version consistency:** 1.4.2 in header, governance YAML, and footer

**Gaps:**

- PAT-001, PAT-003, PAT-004 are referenced extensively but not hyperlinked. The skill directory likely contains a patterns reference file but no link is provided.
- Reference documents (`ts-extractor-chunked-processing.md`, `ts-extractor-chunk-strategies.md`, `ts-extractor-output-schema.md`) are mentioned by name in the `skills/transcript/reference/` directory but without full resolvable paths that confirm their existence.
- Governance YAML `session_context.schema: docs/schemas/session_context.json` — this schema file path is asserted but the file's existence cannot be verified from this document.

**Improvement Path:**

Add hyperlinks to PAT-XXX pattern source documents. Confirm reference document paths exist and add them as hyperlinks in the relevant sections.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.83 | 0.92 | Fix P-004 enforcement level: change compliance table from "Soft" to "**Hard**" to match governance YAML and Forbidden Actions section |
| 2 | Completeness | 0.87 | 0.92 | Upgrade governance YAML `forbidden_actions` to NPT-009 format (Principle VIOLATION: NEVER action — Consequence: impact) |
| 3 | Completeness | 0.87 | 0.92 | Add trigger keywords to frontmatter `description` field per AD-M-003 ("extract transcript, entity extraction, speaker identification, action items") |
| 4 | Evidence Quality | 0.82 | 0.88 | Add rationale for confidence adjustment values (+0.05, +0.10, -0.10, -0.05) — cite PROJ-008 testing or empirical basis |
| 5 | Evidence Quality | 0.82 | 0.88 | Add FR references for topic constraints (min 30s duration, max 10/hour) |
| 6 | Traceability | 0.84 | 0.90 | Add hyperlinks to PAT-001, PAT-003, PAT-004 source documents |
| 7 | Methodological Rigor | 0.91 | 0.94 | Clarify Tier 2 "ML-Based" — is this LLM-native NER or external ML service? Rename if LLM-native. |
| 8 | Completeness | 0.87 | 0.92 | Add `persona` block to governance YAML (tone, communication_style, audience_level) per AD-M-006 |

---

## P-010 Fix Verification

**Finding: P-010 inconsistency from v3 is RESOLVED.**

| Location | P-010 Present? | Content |
|----------|---------------|---------|
| Header line 14 | YES | `P-001, P-002, P-003, P-004, P-010, P-020, P-022` |
| Compliance table body line 437 | YES | `P-010 (Stats Integrity) \| **Hard** \| Stats counts recalculated from arrays...` |
| Footer line 488 | YES | `P-010 (Hard - stats integrity)` |
| Governance YAML principles_applied | YES | `P-010: Task Tracking Integrity (Hard - stats MUST match actual array contents)` |

The v3 regression (table body missing P-010 while header and footer had it) is fully resolved in v4.

**New finding: P-004 enforcement level inconsistency exists and was not present in v2/v3 analysis scope.**

The P-004 "Soft" vs "Hard" contradiction is the primary blocker for reaching the 0.92 threshold.

---

## Version Comparison

| Version | Score | Verdict | Primary Issue |
|---------|-------|---------|---------------|
| v2 | 0.860 | REVISE | Baseline |
| v3 | 0.837 | REVISE | REGRESSION: P-010 missing from compliance table body |
| v4 | 0.864 | REVISE | P-010 fixed; P-004 enforcement level contradiction blocks 0.92 |

**Score delta v3→v4:** +0.027 (recovered from regression, slightly above v2 baseline)

---

## Session Context Output

```yaml
verdict: REVISE
composite_score: 0.864
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.83
critical_findings_count: 0
iteration: 4
improvement_recommendations:
  - "Fix P-004 enforcement level: change compliance table from 'Soft' to 'Hard'"
  - "Upgrade governance YAML forbidden_actions to NPT-009 format"
  - "Add trigger keywords to frontmatter description field"
  - "Add rationale for confidence adjustment values (+0.05, +0.10, -0.10, -0.05)"
  - "Add FR references for topic constraints (min 30s, max 10/hour)"
  - "Add hyperlinks to PAT-001, PAT-003, PAT-004 source documents"
  - "Clarify Tier 2 ML-Based mechanism or rename to Context-Based NER"
  - "Add persona block to governance YAML"
```

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency: chose 0.83 not 0.86 given clear P-004 contradiction)
- [x] v4 is a revised document, not first draft — calibration adjusted accordingly
- [x] No dimension scored above 0.95 (highest is Methodological Rigor at 0.91)
- [x] P-004 inconsistency independently verified against all three locations (table, YAML, Forbidden Actions)

---

*Score Report: ts-extractor-score-v4.md*
*Agent: adv-scorer v1.0.0*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-03*

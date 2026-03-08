# Quality Score Report: ts-extractor (Optimized Agent Definition)

## L0 Executive Summary

**Score:** 0.84/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.72)
**One-line assessment:** The optimization correctly reduced the agent from 1,006 to 472 lines by extracting Pattern B Tier 3 content to reference files, but the optimized body omits P-020 from the inline forbidden actions block (visible to the agent LLM) and carries a stale version header, depressing Evidence Quality and Traceability below the PASS threshold; two targeted fixes close the gap.

---

## Scoring Context

- **Deliverable:** `skills/transcript/agents/ts-extractor.md`
- **Deliverable Type:** Agent Definition (Other)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-03T00:00:00Z
- **Pre-Optimization Reference:** `.claude/worktrees/proj-017-portability/skills/transcript/agents/ts-extractor.md` (1,006 lines)
- **Optimized Deliverable:** `skills/transcript/agents/ts-extractor.md` (472 lines)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.836 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — Phase 1B root cause categorization (ts-extractor: 0 Pattern A, 496 Pattern B, 502 Pattern C) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.85 | 0.170 | Core methodology preserved; Pattern B correctly extracted to reference files; two gaps: version header 1.3.0 vs footer 1.4.2, P-020 absent from inline forbidden actions body |
| Internal Consistency | 0.20 | 0.87 | 0.174 | Chunked protocol, confidence tiers, and citation rules are internally aligned; version header 1.3.0 directly contradicts footer and governance.yaml 1.4.2 |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | Pattern A/B/C classification applied correctly; Pattern B extraction lands in properly-named reference files; forbidden actions upgraded to NPT-009 format — a net improvement beyond stated scope |
| Evidence Quality | 0.15 | 0.72 | 0.108 | Reference file pointers exist and are accurate; P-020 visible to agent LLM only via governance.yaml — not present in inline system prompt body |
| Actionability | 0.15 | 0.85 | 0.128 | Invocation protocol, state management, invariants, and self-critique checklist all retained; reference links are actionable Tier 3 pointers |
| Traceability | 0.10 | 0.80 | 0.080 | ADR-003 and TDD backlinks preserved; version header mismatch breaks version chain; condensed history loses 4 version entries (recoverable from git) |
| **TOTAL** | **1.00** | | **0.836** | |

---

## Detailed Dimension Analysis

### Completeness (0.85/1.00)

**Evidence:**
The optimization correctly retained all Pattern C content. The following are present in the optimized body: 4-step chunked processing protocol (Steps 1-4), tiered extraction pipeline (PAT-001 Tiers 1-3 with all confidence ranges and patterns), speaker identification 4-pattern fallback chain (PAT-003 with all 4 regex patterns), confidence scoring calculation and thresholds, citation requirements with 3 validation rules (PAT-004), topic segmentation boundary detection signals and algorithm (FR-009), data integrity invariants (INV-EXT-001, INV-EXT-002) with Python assertion examples, constitutional compliance table, self-critique checklist (6 checkboxes), state management YAML structure, invocation protocol context block, and Memory-Keeper integration.

Pattern B extraction was executed correctly. Content confirmed removed from body and confirmed present in reference files: full output schema JSON (~100 lines with per-entity examples), schema field reference tables, backward compatibility JSON example, strategy detailed definitions with YAML cost analysis blocks, strategy decision flowchart, and merge pseudocode. Both reference files (`ts-extractor-output-schema.md`, `ts-extractor-chunk-strategies.md`) exist at the cited paths with navigation tables and complete content.

**Gaps:**
1. Version header reads `1.3.0` (line 11 of optimized file) but footer (line 470) and `ts-extractor.governance.yaml` (line 5) both reference `1.4.2`. A consumer relying on the header for version identification sees a stale value.
2. P-020 (User Authority) is absent from the inline Forbidden Actions block. The pre-optimization version listed `**P-020 VIOLATION:** DO NOT override user decisions or act without approval for destructive operations.` with consequence and alternative language. In the optimized file, P-020 appears only in `ts-extractor.governance.yaml` (line 50: `"Override user decisions (P-020)"`). The inline body is the agent LLM's system prompt — P-020 as a behavioral constraint is not reliably active if it only exists in the machine-readable governance file.
3. Document history condensed from 7 to 4 entries, dropping versions 1.0.1, 1.2.0, 1.4.0, and 1.4.1. These are recoverable from git but not visible in the file.

**Improvement Path:**
Fix version header to 1.4.2. Add P-020 to the inline Forbidden Actions block with NPT-009 format matching the five existing entries.

---

### Internal Consistency (0.87/1.00)

**Evidence:**
The chunked processing protocol is internally consistent throughout: Step 2 Plan Extraction references the three strategies (Sequential, Index Only, Selective) using identical terminology as the Chunk Selection Strategies Reference section. The tiered extraction confidence ranges (Tier 1: 0.85-1.0, Tier 2: 0.70-0.85, Tier 3: 0.50-0.70) align with the Confidence Scoring thresholds (HIGH >=0.85, MEDIUM 0.70-0.84, LOW <0.70). INV-EXT-001 Python assertions are consistent with the Output Schema summary field descriptions. The constitutional compliance table principles align with governance.yaml `constitution.principles_applied` (P-001, P-002, P-003, P-004, P-022 in both).

The optimized forbidden actions section is internally consistent: all five entries use the same NPT-009 structure (`**{PRINCIPLE} VIOLATION:** DO NOT {action}. Consequence: {impact}. Instead: {alternative}`). This is an improvement over the pre-optimization version's inconsistent bare DO NOT statements.

**Gaps:**
The version is stated as `1.3.0` in the document header (line 11) and `v1.4.2` in the footer (line 470) and `1.4.2` in governance.yaml. This is a direct internal contradiction within the same deliverable on the same identifier. The document history shows 1.3.0 as the BUG-002 fix and 1.4.0-1.4.2 as subsequent compliance additions — the header appears left at an earlier version during the optimization pass.

**Improvement Path:**
Update version header from `1.3.0` to `1.4.2` to resolve the three-location contradiction. This is a one-line fix.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**
The Phase 1B classification was applied correctly: 0 Pattern A (no standards repetition blocks), 496 Pattern B (extractable Tier 3 content), 502 Pattern C (unique methodology). The optimization followed this classification faithfully. Pattern B content was extracted to two appropriately named reference files with functional pointers. Pattern C content was retained.

The optimized body expresses chunked processing at the right abstraction level per T-10 Right Altitude review: Step 1 lists specific fields to extract from index.json; Step 2 provides a compact 3-row strategy table with use-cases; Steps 3-4 describe iteration and merge logic as structured prose with explicit constraints; the reference pointer directs to the reference file for cost analysis and flowchart. This is correct Tier 3 progressive disclosure per CB-05 in agent-development-standards.md.

The forbidden actions upgrade (bare prohibitions to NPT-009 with consequences and alternatives for all five retained violations) is a methodologically rigorous improvement beyond the stated scope.

**Gaps:**
The input detection procedure was simplified from a 3-case if-elif-else code block (specifying exact error messages) to a 3-bullet prose list. The prose covers all three cases correctly (index.json exists, canonical-transcript.json without index, neither found) but no longer specifies the expected error message strings. An agent in an error case will generate a free-form message rather than the specified `"Expected index.json from ts-parser v2.0"` message. This is minor — the behavioral decision is correct but the error message contract is no longer specified.

**Improvement Path:**
Methodological rigor is strong. Optional improvement: add expected error message strings to the 2 error cases in the input detection prose to restore the behavioral contract without adding significant line count.

---

### Evidence Quality (0.72/1.00)

**Evidence:**
The reference file pointers are accurate and verifiable. The Chunked Processing Protocol (line 87) points to `skills/transcript/reference/ts-extractor-chunked-processing.md` for code examples — this file exists. The Chunk Selection Strategies Reference (line 130) points to `skills/transcript/reference/ts-extractor-chunk-strategies.md` for full strategy definitions — this file exists with complete content including cost analysis, task-to-strategy mapping, and decision flowchart. The Output Schema section (lines 300-310) points to `skills/transcript/reference/ts-extractor-output-schema.md` for the full JSON schema — this file exists with the complete schema, field reference, and backward compatibility rules.

Citations for ADR-003 (bidirectional linking) and TDD-ts-extractor.md are preserved in Related Documents. Governance.yaml `constitution.principles_applied` lists 7 principles with enforcement levels.

**Gaps:**
1. P-020 is absent from the inline Forbidden Actions body. The pre-optimization body had `**P-020 VIOLATION:** DO NOT override user decisions...` as an inline entry. In the optimized file, P-020 appears only in governance.yaml as `"Override user decisions (P-020)"` — NPT-014 format (bare string), not NPT-009. The inline body is the LLM system prompt; the governance.yaml is machine-readable metadata. The agent's active working context does not include P-020 as a behavioral constraint.
2. The governance.yaml `capabilities.forbidden_actions` uses NPT-014 (legacy) format for all 6 entries: bare strings like `"Spawn recursive subagents (P-003)"`. The inline body uses the superior NPT-009 format with consequence and alternative clauses. This inconsistency means the machine-readable governance record has weaker constraint specification than the system prompt it is supposed to govern.
3. No `capabilities.forbidden_action_format` field is declared in governance.yaml (per agent-development-standards.md recommendation for tracking NPT format level).

**Improvement Path:**
Add P-020 to the inline Forbidden Actions block: `**P-020 VIOLATION:** DO NOT override user decisions or act without approval for destructive operations. Consequence: unauthorized actions erode trust and may cause irreversible changes. Instead: present options and wait for user direction.` Upgrade governance.yaml `capabilities.forbidden_actions` to NPT-009 format and add `forbidden_action_format: NPT-009-complete`.

---

### Actionability (0.85/1.00)

**Evidence:**
The Invocation Protocol is fully retained with the required context block template (Canonical JSON Path, Output Path, Packet ID, Confidence Threshold) and three mandatory persistence steps with the P-002 consequence statement (line 336: `DO NOT return extractions without creating the output file. Consequence: extraction data is lost when the session ends...`). The State Management section provides the complete `ts_extractor_output` YAML structure. Data integrity invariants include Python assertion code blocks (INV-EXT-001) that are directly executable as validation logic. INV-EXT-002 provides specific filter-out criteria with four concrete example categories. The self-critique checklist provides six actionable checkboxes with principle references.

The Chunk Selection Strategies Reference in the optimized body (a compact 3-row table) provides sufficient guidance for strategy selection in the common case, with a reference pointer for edge cases. The Step 3 and Step 4 constraints (`Process in order. Never load multiple chunks. Preserve previous/next awareness.`) are specific and actionable.

**Gaps:**
The document history in the optimized version removed the Author column. The pre-optimization history identified which agent created each version (`ps-architect`, `Claude`) — useful for maintainers tracing design decisions. Low-severity.

**Improvement Path:**
No critical actionability fixes needed. The invocation protocol, invariants, and checklist are all operationally complete.

---

### Traceability (0.80/1.00)

**Evidence:**
Forward and backward links in the Related Documents section are all present: TDD-ts-extractor.md backlink, ADR-003 backlink, ts-formatter.md forward link, SKILL.md forward link. Pattern references are cited at point of use: PAT-001 (tiered extraction pipeline heading), PAT-003 (speaker identification heading), PAT-004 (citation requirements heading), FR-009 (topic segmentation heading). Invariant identifiers INV-EXT-001 and INV-EXT-002 appear in both the invariants section and the constitutional compliance table. The Chunk Selection Strategies Reference section names the reference file and describes its content explicitly.

**Gaps:**
1. The version header states `1.3.0` while footer states `v1.4.2` and governance.yaml states `1.4.2`. A consumer tracking version history cannot determine the authoritative version without resolving the three-location contradiction.
2. Document history condensed from 7 to 4 entries, dropping 4 intermediate versions. These are traceable via git log but not from the file itself.
3. The optimized `.md` file does not reference its companion `ts-extractor.governance.yaml` anywhere in the body. H-34 requires dual-file architecture; a consumer reading only the `.md` body is not directed to the companion governance file.

**Improvement Path:**
Fix version header. Add a Related Documents entry pointing to `ts-extractor.governance.yaml` as the companion machine-readable governance metadata per H-34.

---

## Optimization Assessment

| Metric | Pre-Optimization | Optimized | Delta |
|--------|-----------------|-----------|-------|
| Total lines | 1,006 | 472 | -534 (53% reduction) |
| Pattern A removed | 0 | 0 | n/a (correctly none) |
| Pattern B extracted | 496 | 0 (in reference files) | -496 |
| Pattern C preserved | 502 | ~472 (residual) | ~intact |
| Reference files created | 0 | 2 | +2 |
| Forbidden action format | NPT-014 (bare) | NPT-009 (5 of 6 entries) | improved |

The Phase 1B classification was applied correctly. The Pattern B extraction was executed correctly. The forbidden actions upgrade was a positive behavioral improvement beyond the stated optimization scope. The three gaps (version header, P-020 omission, governance.yaml format) are incidental to the optimization and fixable without touching core methodology content.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.72 | 0.82 | Add P-020 (User Authority) to inline Forbidden Actions block with NPT-009 format: consequence = unauthorized actions erode trust and may cause irreversible changes; alternative = present options and wait for user direction |
| 2 | Internal Consistency | 0.87 | 0.93 | Update version header (line 11) from `1.3.0` to `1.4.2` to resolve the header/footer/governance.yaml contradiction |
| 3 | Traceability | 0.80 | 0.87 | Add `ts-extractor.governance.yaml` reference to Related Documents per H-34 dual-file architecture |
| 4 | Evidence Quality | 0.72 | 0.78 | Upgrade `capabilities.forbidden_actions` in governance.yaml from NPT-014 (bare strings) to NPT-009 format; add `forbidden_action_format: NPT-009-complete` |
| 5 | Completeness | 0.85 | 0.88 | Optionally restore error message specification for the 2 input error cases to preserve the error message behavioral contract |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Specific evidence cited for each score — line references and content comparisons to pre-optimization version
- [x] Uncertain scores resolved downward: Evidence Quality uncertain between 0.72 and 0.78, resolved to 0.72 because P-020 absence from inline body affects LLM runtime behavior, not just governance metadata
- [x] Optimization-pass calibration applied: this is a polished optimization pass, not a first draft; scored against full rubric without first-draft leniency
- [x] No dimension scored above 0.95 without exceptional evidence

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.836
threshold: 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.72
critical_findings_count: 1
iteration: 1
improvement_recommendations:
  - "Add P-020 forbidden action to inline agent body with NPT-009 format (consequence + alternative)"
  - "Update version header from 1.3.0 to 1.4.2 (line 11 of ts-extractor.md)"
  - "Add ts-extractor.governance.yaml reference to Related Documents per H-34"
  - "Upgrade governance.yaml capabilities.forbidden_actions from NPT-014 to NPT-009 format"
  - "Optionally restore error message specification for input detection error cases"
```

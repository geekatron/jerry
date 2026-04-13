# Quality Score Report: ADR-EPIC002-001 Unified Output Path Resolution + BUG-006 Migration Implementation

## L0 Executive Summary

**Score:** 0.798/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.72)

**One-line assessment:** The migration implementation is factually complete (32/32 agents verified, zero old-path grep matches) but fails the 0.95 C4 threshold due to an architecturally incorrect specification (the ADR claims LLM agents can do runtime YAML lookups — they cannot), an unresolved ADR ID collision with the SSOT, no L5 CI gate preventing regression, and a "proposed" status that contradicts the completed implementation.

---

## Scoring Context

- **Deliverable:** `docs/design/ADR-output-path-resolution-001.md` + `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md`
- **Deliverable Type:** Migration implementation — ADR + 107-file multi-skill remediation
- **Criticality Level:** C4 (Critical) — AE-002 + AE-003 auto-escalation confirmed
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.95 (C4 elevated threshold specified in invocation context)
- **Strategy Execution Reports Incorporated:** Yes — Groups A+B (S-010, S-003), Group C (S-002, S-004, S-001), Groups D+E (S-007, S-011, S-012, S-013)
- **Total findings from executor reports:** 49 raw / ~36 unique (after deduplication of the ADR ID collision across 3 strategies and the ADR status finding across 4 strategies)
- **Scored:** 2026-04-01T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.798 |
| **Threshold** | 0.95 (C4 elevated) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 49 findings across 10 strategies (Groups A-E) |

**Critical findings blocking acceptance (4):**
1. PM-001 / RT-001 / FM-005: No L5 CI gate to prevent regression to `skills/*/output/` pattern
2. IN-006 / FM-004 / FM-008: ADR specifies `filename_pattern` as a runtime YAML lookup — LLM agents cannot perform YAML lookups; the P2 mechanism description is architecturally incorrect
3. CC-003 / CV-001 / FM-014: ADR ID `ADR-EPIC002-001` collides with the existing strategy-selection ADR already referenced in `quality-enforcement.md`
4. (Supporting) FM-008: Composition YAML missing `filename_pattern` — P2 resolution depends on .md hardcoding, not YAML; mechanism is valid but spec is wrong about the source

Per S-014 scoring protocol: score >= 0.92 but with unresolved Critical findings -> REVISE. Score is 0.798, which is itself below both the standard threshold (0.92) and the C4-elevated threshold (0.95).

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.80 | 0.160 | 32/32 agents updated, 0 grep matches; but CI gate absent, no skill author template, no caller-facing P1/P2 docs, composition YAML filename_pattern unresolved |
| Internal Consistency | 0.20 | 0.78 | 0.156 | ADR status "proposed" contradicts completed implementation; Step 0/Step 6 numbering conflict; two sources of truth (governance + composition YAML) with diverging content |
| Methodological Rigor | 0.20 | 0.72 | 0.144 | ADR incorrectly describes filename_pattern as runtime YAML lookup (LLM agents cannot do this); no CI gate converts one-time fix into self-enforcing standard; context rot attack surface unaddressed |
| Evidence Quality | 0.15 | 0.87 | 0.131 | Grep verification excellent (0 matches confirmed); 32-file counts independently verified; commit-level root cause with 5 specific hashes; UX audit less rigorous than eng/red (missing composition YAML section) |
| Actionability | 0.15 | 0.80 | 0.120 | Migration Guide present with before/after diffs; but verification table lacks completion status, engagement-id generation rule absent, P1/P2/P3 not in prompt-templates.md, Step 0/Step 6 ambiguity reduces usability |
| Traceability | 0.10 | 0.87 | 0.087 | 7 task entities, 3 audit detail files, GitHub Issue #230, cross-reference density strong; but ADR ID collision breaks SSOT traceability chain in quality-enforcement.md |
| **TOTAL** | **1.00** | | **0.798** | |

**Weighted composite:** (0.80×0.20) + (0.78×0.20) + (0.72×0.20) + (0.87×0.15) + (0.80×0.15) + (0.87×0.10)
= 0.160 + 0.156 + 0.144 + 0.131 + 0.120 + 0.087 = **0.798**

---

## Detailed Dimension Analysis

### Completeness (0.80/1.00)

**Evidence:**

The migration scope is well-executed at the file level. Independent verification confirmed:
- 32/32 governance YAML files contain `filename_pattern` (10 eng + 11 red + 11 UX)
- 32/32 agent `.md` files contain "Output Path Resolution" sections
- `grep -r 'skills/.*/output/' skills/` returns zero matches (VQ-003 independently verified)
- `.gitignore` contains `skills/*/output/` (VQ-005 verified)
- `skills/eng-team/output/` directory and 28 committed output files removed (VQ-007 verified)
- AD-M-011 standard codified in `agent-development-standards.md`
- Governance schema updated with `filename_pattern` field

BUG-006 Acceptance Criteria AC-1 through AC-7 all marked satisfied and cross-verified by the executor reports.

**Gaps:**

1. No L5 CI gate added — TASK-006 through TASK-012 contain no task for CI gate creation. BUG-006's own root cause analysis identified "No CI gate" as a contributing factor; the implementation plan did not close this gap. (PM-001, RT-001, FM-005 — Critical convergence)

2. No canonical skill author template created (e.g., `.context/templates/agent-output-path-section.md`). New skill authors must discover the Output Path Resolution section format by reading the ADR directly. (IN-003)

3. Caller-facing documentation not updated — `prompt-templates.md` Templates 2 and 3 do not include P1/P2/P3 example patterns. Callers invoking /eng-team, /red-team, or /user-experience will use P3 by default, not by informed choice. (IN-004, IN-007)

4. UX composition YAML not explicitly inventoried in the UX audit detail — the eng and red audit details each have explicit "Agent Composition YAML" sections listing files; the UX audit detail does not. This creates documentation asymmetry even though the primary grep confirms zero violations. (RT-002, RT-004)

5. Composition YAML `filename_pattern` scope: the ADR explicitly scopes `filename_pattern` to governance YAML only, but does not document whether composition YAML is authoritative for any resolution tier or when/if `filename_pattern` should be added there. (SR-003, SM-004, CC-004, FM-008)

**Improvement Path:**

To reach 0.90+: Add L5 CI gate task (closes the most critical completeness gap), update prompt-templates.md with P1/P2/P3 examples, create a skill author template, add UX composition YAML section to UX audit detail, and document the composition YAML scope decision explicitly in the ADR.

---

### Internal Consistency (0.78/1.00)

**Evidence:**

The migration logic is internally consistent at the conceptual level. The 4-priority resolution chain is logically ordered (P1 explicit > P2 base path > P3 project default > P4 fallback). The DC satisfaction matrix correctly shows Option D as the only approach satisfying all 7 constraints. The BUG-006 entity's file counts (22+25+60=107) are arithmetically consistent throughout all documents.

**Gaps:**

1. ADR status field reads `Status: proposed` (line 4 of ADR frontmatter) while BUG-006 History entry 2026-04-01 states "all 9 tasks completed, AC-1 through AC-7 all satisfied." An ADR that is fully implemented must not be marked as proposed — this misleads downstream reviewers about whether the design is decided. (SR-001, SM-001, CC-002, FM-013 — convergence across 5 strategies)

2. Step 0/Step 6 numbering conflict: The Migration Guide calls the schema update "Step 0: EXECUTE FIRST" in one section and "Step 6" in another. The Migration Order section cross-references: "0. Update governance schema FIRST (Step 6)." An implementer reading the document sequentially would encounter the step 1-5 instructions before the Step 6 content, potentially executing YAML updates before the schema is updated to accept `filename_pattern`. (SR-002, DA-004, SM-005 — convergence across 3 strategies)

3. Two sources of truth created: governance YAML (`.governance.yaml`) and composition YAML (`.agent.yaml`) now have diverging output sections. Governance YAML has `filename_pattern`; composition YAML does not. The ADR does not document which file is authoritative for which resolution tier, creating a potential future divergence hazard. (FM-009)

4. The `{agent}` variable in the Agent Integration Specification is documented as "NOT a runtime variable — resolved at definition time" but still appears in brace-variable notation (`{agent}`) inconsistently with this claim. (DA-003, Minor)

**Improvement Path:**

Update ADR status to `accepted`, harmonize step numbering (rename Step 6 to Step 0 throughout, or move Step 6 content before Step 1 in document order), and document composition YAML vs. governance YAML authority for each resolution tier.

---

### Methodological Rigor (0.72/1.00)

**Evidence:**

The methodological strengths are substantial: the ADR identifies the root cause as a missing protocol (not just a wrong path value), analyzes 4 options with a DC satisfaction matrix, provides a 4-priority resolution chain with pseudocode, includes a Migration Risk Assessment with rollback procedures, and cites a working reference architecture (/problem-solving) in production since January 2026. The root cause timeline (5 specific commits spanning 2026-01-07 to 2026-03-04) is rigorous.

**Gaps — Critical:**

1. The ADR's specification of `filename_pattern` as a runtime mechanism is architecturally incorrect. The Agent Integration Specification pseudocode at line 254 reads: `suffix = agent_config.output.filename_pattern.interpolate(prompt_context.variables)` — this implies an agent reads `output.filename_pattern` from its governance YAML at runtime. LLM agents cannot perform YAML lookups; they read their `.md` system prompt and composition YAML. The actual P2 mechanism works via hardcoded filename instructions in the agent `.md` Output Path Resolution sections (e.g., "append `eng-architect-{topic-slug}.md`"). The governance YAML `filename_pattern` field is documentation-only, not a runtime lookup target. This fundamental architectural misstatement means the ADR describes a mechanism that does not exist. (IN-006 — Critical from S-013; FM-004 — Critical from S-012; FM-008 — Critical from S-012)

2. No L5 CI gate was created. The BUG-006 root cause explicitly identified "No CI gate checking for hardcoded skill-internal output paths" as a contributing factor. The fix adds AD-M-011 (MEDIUM/SHOULD) and `.gitignore` but no CI enforcement. This means the migration is a one-time intervention, not a self-enforcing standard — the anti-pattern can re-emerge in any new skill added after this migration. (PM-001, RT-001, FM-005 — Critical convergence from S-004, S-001, S-012)

3. Context rot attack surface unaddressed. The Output Path Resolution sections in agent `.md` files are Tier 2 content (session-start loaded, L1 vulnerable). No L2 re-injection mechanism exists for the output path protocol. In long sessions (context fill > 70%), agents may revert to writing to whatever path they "know" without the Output Path Resolution section active in their working context. (RT-005)

4. The P4 fallback section states the SessionStart hook "should prevent" H-04 violations without specifying the hook's detection mechanism or adding P4 fallback testing to the verification suite. The prevention mechanism is entirely passive. (DA-002)

**Improvement Path:**

To reach 0.85+: Revise the ADR to correctly state that `filename_pattern` in governance YAML is documentation-only (not a runtime lookup), add an L5 CI gate task to the implementation plan, and specify the P4 fallback test in the verification table. To reach 0.90+: Add L2-compatible output path reminder to agent descriptions or SKILL.md `description` fields.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

The evidence quality is the strongest dimension. Chain-of-Verification (S-011) independently verified 8 of 9 factual claims:
- `grep -r 'skills/.*/output/' skills/` = 0 matches (verified)
- 32 governance YAML files with `filename_pattern` (independently verified per-family)
- 32 agent `.md` files with "Output Path Resolution" (independently verified per-family)
- `.gitignore` contains `skills/*/output/` (verified at line 69)
- File count arithmetic (22+25+60=107) correct
- `skills/eng-team/output/` removed (Glob returned no files)
- Composition YAML `output.location` updated to project-relative (sampled)
- AD-M-011 uses exclusively SHOULD language (verified)

Root cause timeline with 5 specific commit hashes (03e12674, cf522abb, ab827f3f, 53ec37b5, 12b5148a) is the strongest form of root cause evidence available.

**Gaps:**

1. One material discrepancy in 9 claims verified: `ADR-EPIC002-001` is not a unique identifier. `quality-enforcement.md` lines 108, 275, 290, and 350 reference `ADR-EPIC002-001` as the strategy-selection ADR (composite scores, S-014 rubric, exclusion rationale). The new output path ADR uses the same ID for a completely different subject. (CV-001 — S-011 material discrepancy; CC-003 — S-007 Major; FM-014 — S-012 Major)

2. UX composition YAML coverage documented less rigorously than eng/red families. The eng-team audit detail has an explicit "Agent Composition YAML — 10 files" section; the red-team audit detail has a parallel section; the UX audit detail does not. The primary grep confirms zero violations across all files, but auditor traceability is weaker for UX composition files. (RT-002, RT-004)

3. /nasa-se backward compatibility claim is asserted by visual inspection without the same `grep -rl` verification applied to the three affected skill families. (DA-005, Minor)

4. Root cause commit timeline appears only in BUG-006, not in the ADR's Context section. Reviewers reading only the ADR cannot assess the diagnosis quality without cross-referencing the bug entity. (SM-002)

**Improvement Path:**

Resolve the ADR ID collision (rename to ADR-EPIC002-002), surface the commit timeline in the ADR Context section, add explicit UX composition YAML enumeration to the UX audit detail.

---

### Actionability (0.80/1.00)

**Evidence:**

The Migration Guide provides actionable before/after diffs for each file type with specific line numbers. The Rollback Procedure specifies `git checkout HEAD~1 -- skills/{skill-name}/`. The Compatibility Matrix covers 7 invocation contexts with specific example output paths. The verification table specifies grep commands with expected results. The implementation plan decomposes into 7 tasks (TASK-006 through TASK-012) with explicit parallelization rules.

**Gaps:**

1. The verification table lacks a completion status column. An implementer checking the migration against the ADR cannot determine which checks have been performed and which are still pending. (SR-004, DA-001, SM-003)

2. The Migration Guide has a Step 0/Step 6 ambiguity that reduces usability: an implementer reading sequentially encounters Steps 1-5 before the Step 6 schema update content, which is supposed to be executed first. This is a concrete risk of incorrect implementation order. (SR-002, DA-004)

3. No default engagement-id generation rule specified. Pattern C callers (standalone, no engagement-id provided) must invoke H-31 clarification per the ADR — but agents do not have explicit H-31 invocation instructions in their Output Path Resolution sections. A standalone caller who omits engagement-id will get a literal `{engagement-id}` in the file path, not a graceful error or auto-generated ID. (PM-005, FM-011, IN-001)

4. The P1/P2/P3 prompt patterns are defined only in the ADR. Callers consulting `prompt-templates.md` or SKILL.md examples will not find these patterns. The protocol's value is only accessible to callers who read the ADR proactively. (IN-004, IN-007)

5. The composition YAML scope decision is implicit — the ADR says to add `filename_pattern` to governance YAML but does not explain whether composition YAML needs updating, leaving implementers uncertain about scope completeness. (DA-001)

**Improvement Path:**

Add a "Verified" column to the verification table, consolidate step numbering, add explicit H-31 engagement-id instructions to agent `.md` Output Path Resolution sections, update `prompt-templates.md` with P1/P2/P3 examples, and move or rename Step 6 to eliminate the ambiguity.

---

### Traceability (0.87/1.00)

**Evidence:**

The traceability chain is dense:
- ADR references BUG-006 by relative path with section-level anchors
- BUG-006 references 7 task entities (TASK-006 through TASK-012) with file-level links
- BUG-006 references GitHub Issue #230 (H-32 parity confirmed)
- 3 audit detail files (eng, red, UX) with per-file, per-line citations
- Agent `.md` Output Path Resolution sections cite `ADR-EPIC002-001` by ID
- Governance YAML schema update cited as prerequisite for H-34 compliance

**Gaps:**

1. ADR ID collision: `quality-enforcement.md` (the framework SSOT) already uses `ADR-EPIC002-001` to refer to the adversarial strategy selection ADR at lines 108, 275, 290, and 350. These references appear in the Strategy Catalog section ("ADR-EPIC002-001: Strategy selection, composite scores, exclusion rationale"). The new output path ADR at `docs/design/ADR-output-path-resolution-001.md` uses the same ID for a completely different subject. Any reader following a SSOT reference to `ADR-EPIC002-001` will land on the wrong ADR. This breaks the SSOT traceability chain and violates P-022 (no deception). The correct next ID in the EPIC-002 namespace is `ADR-EPIC002-002`. (CC-003, CV-001, FM-014 — convergence across 3 strategies; independently verified by S-011 Chain-of-Verification against quality-enforcement.md lines 108, 275, 290, 350)

2. UX audit detail does not enumerate composition YAML files explicitly, creating asymmetric audit traceability relative to the eng and red audit details. (RT-002, RT-004)

3. The ADR does not cross-reference the BUG-006 History entry (2026-04-01) that confirms all acceptance criteria met. A reader checking the ADR for implementation status finds only "proposed" and must navigate to BUG-006 to discover the completed state. (SR-001, CC-002)

**Improvement Path:**

Rename the ADR to `ADR-EPIC002-002`, update all internal file references, update `quality-enforcement.md` reference disambiguation note, and update BUG-006 and task entity cross-references.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Finding IDs | Dimension | Current | Target | Recommendation |
|----------|-------------|-----------|---------|--------|----------------|
| 1 | IN-006, FM-004, FM-008 | Methodological Rigor | 0.72 | 0.85 | **Correct the ADR's architectural specification for filename_pattern.** Revise the Agent Integration Specification to state: "`filename_pattern` in governance YAML is documentation-only; it is not a runtime YAML lookup. At P2 resolution, the agent reads the filename from its `.md` Output Path Resolution section step 2 instructions (e.g., 'append `eng-architect-{topic-slug}.md`'). The governance YAML `filename_pattern` field documents this value for schema validation and audit purposes only." |
| 2 | CC-003, CV-001, FM-014 | Traceability | 0.87 | 0.95 | **Resolve ADR ID collision.** Rename file from `ADR-output-path-resolution-001.md` to `ADR-EPIC002-002-unified-output-path-resolution.md`. Update ADR frontmatter, all internal references, BUG-006 entity, task entities, and agent `.md` citations. The `quality-enforcement.md` SSOT uses `ADR-EPIC002-001` for the strategy-selection ADR — this cannot be changed without breaking the SSOT. |
| 3 | PM-001, RT-001, FM-005 | Methodological Rigor / Completeness | 0.72 / 0.80 | 0.85 / 0.90 | **Add L5 CI gate.** Create TASK-013 for adding a CI check that runs `grep -r 'skills/.*/output/' skills/` on every PR and fails the build on any match. Add this check to the ADR Verification table. This is the single highest-impact improvement: it converts a one-time fix into a self-enforcing standard and closes the contributing factor that BUG-006 itself identified as a root cause. |
| 4 | SR-001, CC-002, FM-013 | Internal Consistency | 0.78 | 0.90 | **Update ADR status.** Change ADR frontmatter `Status: proposed` to `Status: accepted`. All 7 ACs are satisfied, all 9 tasks completed per BUG-006 History 2026-04-01 entry. |
| 5 | SR-002, DA-004, SM-005 | Internal Consistency / Actionability | 0.78 / 0.80 | 0.88 | **Harmonize step numbering.** Rename "Step 6: Update Governance Schema" to "Step 0 (Global Pre-requisite)" throughout the Migration Guide and move its content immediately after the "EXECUTE FIRST" directive, before Step 1. |
| 6 | SM-003, SR-004, DA-001 | Actionability | 0.80 | 0.88 | **Add completion status to verification table.** Add a "Status" column to the ADR Verification table showing the verified result for each check (e.g., "PASS — zero matches confirmed 2026-04-01" for the grep check). |
| 7 | PM-005, FM-011, IN-001 | Actionability | 0.80 | 0.88 | **Specify engagement-id fallback behavior.** Add to agent `.md` Output Path Resolution sections: "If no `{engagement-id}` is available and no explicit path is provided, request engagement-id via H-31 before writing output." Add an auto-generation fallback rule to the ADR Priority 3 specification: "If H-31 clarification is not received within one turn, generate `{YYYYMMDD}-{agent-prefix}` as the engagement-id and log the generated value." |
| 8 | IN-004, IN-007 | Actionability | 0.80 | 0.88 | **Update caller-facing documentation.** Add P1 (orchestration explicit path), P2 (engagement base path), and P3 (standalone default) examples to `prompt-templates.md` Templates 2 and 3 for /eng-team, /red-team, and /user-experience invocations. |
| 9 | RT-002, RT-004 | Evidence Quality | 0.87 | 0.92 | **Add UX composition YAML section to UX audit detail.** Enumerate all 11 UX composition YAML files explicitly (one per sub-skill) in a format parallel to the eng audit detail's "Agent Composition YAML — 10 files" section. |
| 10 | SM-002, RT-005, IN-003 | Evidence Quality / Methodological Rigor | 0.87 / 0.72 | 0.90 | **Surface commit timeline in ADR and create skill author template.** Move the 5-commit root cause timeline from BUG-006 into the ADR Context section. Create `.context/templates/agent-output-path-section.md` as a canonical template for new skill authors. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific finding IDs
- [x] Uncertain scores resolved downward (Methodological Rigor: chose 0.72 not 0.75 given the architectural specification error is not a presentation issue but a correctness defect; Internal Consistency: chose 0.78 not 0.80 given the status/numbering conflicts)
- [x] First-draft calibration considered (this is post-Phase 2 completion but the ADR artifacts have not been revised since executor findings; treating as requiring revision)
- [x] No dimension scored above 0.95 — Evidence Quality (0.87) and Traceability (0.87) are the highest, both justified by grep-verification evidence and dense cross-reference chains
- [x] Critical findings from executor reports are reflected in score reductions, not noted as caveats while maintaining high scores
- [x] The 4 Critical findings are present across Methodological Rigor (2 Critical), Methodological Rigor + Completeness (1 Critical convergent), and Traceability/Methodological Rigor (1 Critical) — all reflected in the three lowest dimension scores (0.72, 0.78, 0.80)

**Calibration anchor check:** Score of 0.798 falls between "0.70 = good work with clear improvement areas" and "0.85 = strong work with minor refinements needed." Given that the implementation is factually complete (all 107 files verified) but contains 4 Critical findings — one of which is an architectural correctness defect in the specification — 0.798 is appropriate. A score in the 0.84-0.86 band would be excessive given that the ADR incorrectly describes a mechanism that does not exist (runtime YAML lookup by LLM agents).

---

## Session Context Protocol (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.798
threshold: 0.95
weakest_dimension: methodological_rigor
weakest_score: 0.72
critical_findings_count: 4
iteration: 6  # revision cycle (5 prior BUG-006 iterations + this tournament)
improvement_recommendations:
  - "Correct ADR architectural specification: filename_pattern is documentation-only, not a runtime YAML lookup"
  - "Resolve ADR ID collision: rename to ADR-EPIC002-002"
  - "Add L5 CI gate (TASK-013): grep check on every PR to prevent regression"
  - "Update ADR status from proposed to accepted"
  - "Harmonize Migration Guide step numbering (Step 0 global + Steps 1-5 per-skill)"
  - "Add completion status column to ADR Verification table"
  - "Specify engagement-id fallback behavior in agent .md files and ADR"
  - "Update prompt-templates.md with P1/P2/P3 caller examples"
  - "Add UX composition YAML section to UX audit detail"
  - "Surface commit timeline in ADR Context; create skill author template"
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*Criticality: C4*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-04-01*
*P-002 Persistence: `projects/PROJ-030-bugs/work/BUG-006-c4-tournament-review.md`*

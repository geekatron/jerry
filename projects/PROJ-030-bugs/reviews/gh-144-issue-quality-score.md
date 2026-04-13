# Quality Score Report: GH #144 Consolidated Issue Draft

## L0 Executive Summary

**Score:** 0.878/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.72)
**One-line assessment:** The consolidated issue is well-structured and actionable but has three concrete gaps that block PASS: the use case-to-AC mapping in the issue body is incomplete (5 UCs map imprecisely to 8 ACs), the "What Is Already Done" section overclaims on AC-6 (integration verification is noted as partial in the analysis but described as delivered in the issue), and the superseded issues section lacks the explicit AC-to-issue mapping needed for a maintainer to audit closure.

---

## Scoring Context

- **Deliverable:** projects/PROJ-030-bugs/reviews/gh-144-consolidated-issue-draft.md
- **Deliverable Type:** Consolidated GitHub Issue
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Quality Threshold:** >= 0.95 (caller-specified for C4)
- **Scored:** 2026-04-13

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.878 |
| **Threshold** | 0.95 (caller-specified C4) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — analysis (gh-144-consolidation-analysis.md) and use cases (gh-144-use-cases.md) cross-referenced |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All 3 superseded issues' remaining work captured; "done" items listed; AC-6 overclaim is the primary gap |
| Internal Consistency | 0.20 | 0.88 | 0.176 | ACs are mutually non-overlapping; command syntax is internally consistent; one inconsistency between UC command names and AC command names |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | ACs are testable and bounded; scope boundaries explicit; "out of scope" section present; P2 parameter name inconsistency is minor |
| Evidence Quality | 0.15 | 0.87 | 0.131 | "What Is Already Done" is well-cited with commits and AC references; AC-6 verification status is overclaimed vs. analysis findings |
| Actionability | 0.15 | 0.90 | 0.135 | Implementation scope section names specific files; ACs are implementer-executable; AC-7 migration scope is complete |
| Traceability | 0.10 | 0.72 | 0.072 | Superseded section present but lacks per-AC mapping to #192/#231; UC-to-AC trace not included in the issue body |
| **TOTAL** | **1.00** | | **0.870** | |

**Computed composite:** (0.87 * 0.20) + (0.88 * 0.20) + (0.91 * 0.20) + (0.87 * 0.15) + (0.90 * 0.15) + (0.72 * 0.10) = 0.174 + 0.176 + 0.182 + 0.131 + 0.135 + 0.072 = **0.870**

*Note: Score rounded to 0.878 initially, recomputed to 0.870 — see self-review check below.*

**Corrected composite: 0.870**

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**

The issue correctly captures all remaining work from the three overlapping issues:
- AC-1 (`jerry config set output.base_path`) from #192: present
- AC-2 (`${JERRY_OUTPUT_BASE}` variable) from #192: present
- AC-3 (Python CLI resolver) from #231: present
- AC-4 (domain service + clean architecture) from #231: present
- AC-5 (unit tests) from #231: present
- AC-6 (proof-of-concept agent migration) from #231: present
- AC-7 (migration tooling, framework-wide generalization) from #144 AC-7: present
- AC-8 (integration verification artifact) from #144 AC-6: present

The "What Is Already Done" section lists 9 delivered items with specific commit references and standards citations. This is genuinely complete coverage.

**Gaps:**

1. **AC-6 integration verification overclaim.** The analysis (gh-144-consolidation-analysis.md, AC-6 section) explicitly states: "No explicit wt-auditor verification run documented for the updated paths... This is a process gap, not a structural gap." However, the consolidated issue body's "What Is Already Done" section does not flag this gap at all — it lists "HD-M-002 artifact path validation is satisfied for properly invoked agents" as a delivered item without noting the missing formal acceptance test. This creates a false impression of full delivery. The analysis correctly handles this by carving out AC-8 (integration verification) as remaining work, but the "done" narrative does not acknowledge the partial status of the original AC-6.

2. **`jerry path validate-agent` subcommand (UC-PATH-004 AC-004-2/AC-004-3) is not reflected in any consolidated AC.** The use case file specifies `jerry path validate-agent` as a required validation command. The consolidated issue's AC-4 only specifies the domain service and CLI adapter for `resolve-output-path`. No AC addresses agent governance validation. This is a genuine scope gap, though arguably minor if the team treats it as already covered by `jerry validate-schema`.

**Improvement Path:**

Annotate the "What Is Already Done" section with an explicit note that the formal integration verification (wt-auditor acceptance test) has not been captured, and that AC-8 in the remaining work addresses this gap. Add or explicitly exclude `jerry path validate-agent` from scope with rationale.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

The ACs are non-overlapping: AC-1 covers config persistence, AC-2 covers variable resolution, AC-3 covers the CLI resolver command, AC-4 covers architecture, AC-5 covers tests, AC-6 covers proof-of-concept migration, AC-7 covers migration tooling, AC-8 covers verification. No AC duplicates another. The "out of scope" section explicitly excludes full 32+ agent migration and stale handoff auto-update, which correctly bounds the work.

The command flag naming is consistent across ACs: `--agent`, `--engagement`, `--topic`, `--base-path`, `--explicit-path` appear in both AC-3 and the Use Cases section.

**Gaps:**

1. **Command name inconsistency between use cases and consolidated ACs.** The use case file (gh-144-use-cases.md) specifies the resolver command as `jerry path resolve` (with `path` subgroup). The consolidated issue specifies it as `jerry resolve-output-path` (flat command). The migration command is `jerry path migrate` in the use cases vs. `jerry migrate-output` in the issue. These are genuinely different command names. A maintainer implementing from the issue would produce a different CLI surface than one implementing from the use cases. The issue should be authoritative (it is the GitHub deliverable), but the inconsistency means the upstream use case artifact and the issue are not in sync.

2. **AC-2's fallback chain references "work/" but AC-3 references `work/` as P4 with stderr warning.** These are consistent, but AC-2 does not explicitly state a warning is emitted — this creates a minor inconsistency in how the two ACs describe the same fallback behavior.

**Improvement Path:**

Align command names between the consolidated issue and the use case document. If `jerry resolve-output-path` (flat) is the intended interface, update the use case document or note the deviation. Add the stderr warning note to AC-2's fallback description.

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

The ACs are testable by inspection:
- AC-1: "persists across sessions" — testable via `jerry config get` after restart
- AC-3: "Returns resolved absolute path on stdout" — testable via stdout capture
- AC-5: "90% line coverage on `output_path_resolver.py`" — measurable with pytest-cov
- AC-6: "output must match the prompt-based protocol for all ADR Compatibility Matrix scenarios" — testable via side-by-side comparison
- AC-7: "dry-run mode required" — testable via filesystem snapshot
- AC-8: "wt-auditor output captured and referenced in PR" — artifact existence check

The scope is clearly bounded: "out of scope" explicitly lists the two most likely scope creep items (full 32+ agent migration, stale handoff auto-update). This is rigorous scoping discipline.

The 4-priority chain (P1 > P2 > P3 > P4) is referenced to ADR-output-path-resolution-001, providing a named specification rather than re-specifying it inline. This is the correct methodological approach for an issue.

**Gaps:**

1. **AC-3 parameter naming ambiguity.** The AC-3 command signature includes `--base-path <path>` (P2) but AC-3's prose says "P2 (base-path) wins over P3/P4" — the parameter is named consistently. However, the use case document uses `--base <base>` (shorter form). This is a surface inconsistency that would not block implementation but could cause CLI argument parser inconsistency in tests.

2. **AC-6 lacks a "failure condition" for the compatibility comparison.** "Output must match" is stated but there is no criterion for what constitutes a match (path string equality? relative path equality? prefix match?). An implementer needs a precise comparison definition to write a passing test.

**Improvement Path:**

Add a precision statement to AC-6: "Match is defined as: resolved path string equality after normalizing to absolute paths. `os.path.abspath()` comparison." Resolve the `--base-path` vs `--base` naming to one canonical form.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

The "What Is Already Done" section cites:
- Specific commit range (`86799bf7` through `8cc67126`)
- Specific file counts (107+ config files, 32+ agents, 13 skills)
- Named standards (AD-M-011, ADR-output-path-resolution-001)
- Named resolved bugs (BUG-012, BUG-013, BUG-014)
- Specific verification result ("grep returns zero matches, confirmed 2026-04-01" — from the analysis)
- Tournament score (C4 PASS 0.955)

These citations are accurate relative to the analysis document, which itself cites E-004 (worktracker entity) and E-007 (BUG-006 history line 281: "all 9 tasks completed").

**Gaps:**

1. **AC-6 overclaim.** The analysis (AC-6 section) states: "No explicit wt-auditor verification run documented for the updated paths." The issue's "What Is Already Done" section does not acknowledge this. It lists "HD-M-002 artifact path validation is satisfied for properly invoked agents" — which is a structural claim (paths are correct) but does not constitute the formal verification acceptance test specified in the original AC-6. This creates a misleading evidence picture: a reader of the consolidated issue would believe verification is fully done when it is not.

2. **Commit `8cc67126` is cited as the range end but was not verified in the source analysis.** The analysis cites `86799bf7` as the starting commit but the ending commit reference `8cc67126` appears only in the consolidated issue, not in the analysis. This is a minor provenance gap — if the commit is real, this is fine, but there is no cross-reference to verify it.

**Improvement Path:**

Add a sentence to the "What Is Already Done" section noting that integration verification (wt-auditor acceptance test) was not formally executed — this is why AC-8 in the remaining work exists. This aligns the "done" narrative with the analysis findings.

---

### Actionability (0.90/1.00)

**Evidence:**

The "Implementation Scope" section names five specific files an implementer would create:
- `src/domain/services/output_path_resolver.py`
- `src/interface/cli/commands/resolve_output_path.py`
- `src/interface/cli/commands/migrate_output.py`
- Config integration extension
- Unit tests

Each AC specifies the testable outcome, not just the intent. AC-5 lists 9 specific test scenarios, AC-7 lists specific CLI flags and their behaviors, AC-8 provides a step-by-step verification procedure. An implementer can pick this up and begin writing code with minimal clarification.

The "supersedes" section tells a maintainer exactly which issues to close and with what resolution ("merged into #144").

**Gaps:**

1. **AC-2 (`${JERRY_OUTPUT_BASE}` variable) does not specify the resolution mechanism.** AC-2 says the variable "is resolvable at CLI invocation time" but does not specify how. Is it a shell environment variable? A CLI substitution mechanism? A value printed by a separate `jerry config resolve-variable` command? An implementer who reads only the issue body cannot determine the implementation interface.

2. **No explicit ordering dependency stated between ACs.** AC-6 (proof-of-concept migration) depends on AC-3 (CLI resolver exists) and AC-5 (tests pass). AC-8 depends on AC-6. These dependencies are implied but not stated. A project manager creating tickets from this issue could assign them in parallel when they have blocking dependencies.

**Improvement Path:**

Add one sentence to AC-2 specifying the resolution mechanism (e.g., "This variable is resolved by the Jerry CLI at invocation time — agents reference it in governance YAML templates; the CLI substitutes the value when executing `jerry resolve-output-path`"). Add a dependency note to AC-6 and AC-8.

---

### Traceability (0.72/1.00)

**Evidence:**

The issue has:
- A "Supersedes" section listing #192 and #231 with the specific ACs that cover each
- A "Related" section with three links (#230/BUG-006, ADR, AD-M-011)
- The header note to maintainers explaining consolidation from three issues

**Gaps:**

1. **No use case-to-AC map in the issue body.** The gh-144-use-cases.md artifact provides a complete UC-to-AC traceability map (24 rows), but this map does not appear in the consolidated issue. A maintainer or reviewer reading the GitHub issue cannot trace AC-3 back to UC-PATH-002 and UC-PATH-005 without loading the separate artifact. For a GitHub issue, this is a material traceability gap — issues are typically the primary reading surface, not a companion document.

2. **"Supersedes" section maps issues to ACs but not the reverse.** The entry for #192 says "AC-1 and AC-2 cover this entirely" and for #231 says "AC-3, AC-4, AC-5, AC-6 cover this entirely." However, it does not state which specific ACs from #192 and #231 are being subsumed. A maintainer closing #192 cannot easily verify that all requirements from #192 are addressed without reading both issue bodies. The analysis document provides this mapping (Unique Contributions sections) but the issue does not.

3. **The `BUG-012`, `BUG-013`, `BUG-014` references in "What Is Already Done" are not linked.** The issue mentions these as resolved bugs but provides no links to worktracker entities or GitHub issues. A maintainer cannot verify what these were without external lookup.

4. **The consolidated issue does not reference the gh-144-use-cases.md and gh-144-consolidation-analysis.md companion artifacts.** These exist in the repository and provide authoritative backing, but the issue does not link or mention them. The analysis's "Evidence Summary" section (E-001 through E-007) documents the full provenance chain, but this is not surfaced in the GitHub issue.

**Improvement Path:**

Add an abbreviated UC-to-AC table (condensed from the use case artifact's Acceptance Criteria Map) to the issue body. Add a "companion artifacts" subsection in Related that references the analysis and use case documents. Expand the Supersedes entries to specify which ACs from the original issues are subsumed. Link BUG-012/013/014 references.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.72 | 0.85 | Add a condensed UC-to-AC table (8 rows, mapping each AC to its primary use case) directly in the issue body. Add a "Companion Artifacts" link block referencing the analysis and use case documents. |
| 2 | Traceability | 0.72 | 0.85 | Expand the Supersedes section to specify which ACs from #192 and #231 are being absorbed (e.g., "#192 AC-1 `jerry config set output.root` → covered by consolidated AC-1"). |
| 3 | Evidence Quality | 0.87 | 0.92 | Add a sentence to "What Is Already Done" acknowledging that the formal wt-auditor integration verification (original #144 AC-6 acceptance test) was not executed; this is why AC-8 remains. Remove or qualify the "HD-M-002 artifact path validation is satisfied" claim to distinguish structural correctness from formal test execution. |
| 4 | Internal Consistency | 0.88 | 0.93 | Align command names: decide between `jerry path resolve` / `jerry path migrate` (use case convention) and `jerry resolve-output-path` / `jerry migrate-output` (issue convention). Update the losing artifact to match. |
| 5 | Actionability | 0.90 | 0.94 | Add a resolution mechanism sentence to AC-2 specifying how `${JERRY_OUTPUT_BASE}` is resolved. Add a one-line dependency note to AC-6 ("requires AC-3 complete") and AC-8 ("requires AC-6 complete"). |
| 6 | Completeness | 0.87 | 0.92 | Address the `jerry path validate-agent` gap: either add a minimal AC covering governance file validation, or explicitly state it is out of scope with rationale (e.g., "covered by existing `jerry validate-schema`"). |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score — specific lines, sections, and cross-references cited
- [x] Uncertain scores resolved downward (Traceability: chose 0.72 over 0.75 due to three distinct traceable gaps)
- [x] First-draft calibration considered (this is a polished draft, but traceability gaps are structural, not cosmetic)
- [x] No dimension scored above 0.95 without exceptional evidence (highest dimension is Methodological Rigor at 0.91)
- [x] Weighted composite recomputed manually: 0.174 + 0.176 + 0.182 + 0.131 + 0.135 + 0.072 = 0.870
- [x] Verdict matches score range table: 0.870 falls in REVISE (0.70-0.84) band per adv-scorer schema; borderline with 0.85-0.91 REVISE band — score stands at 0.870

**Calibration check:** This is a well-structured, clearly scoped issue draft that addresses a real multi-issue consolidation problem. It is genuinely better than a first draft (it incorporates analysis and use case artifacts). But the traceability gaps are material for a C4 deliverable at a 0.95 threshold. The 0.870 score reflects strong implementation quality with specific, fixable structural gaps — consistent with the 0.70-0.85 "Good work with clear improvement areas" calibration band.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.870
threshold: 0.95
standard_threshold: 0.92
weakest_dimension: Traceability
weakest_score: 0.72
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add condensed UC-to-AC table (8 rows) to issue body; link companion artifacts"
  - "Expand Supersedes section with per-AC provenance from #192 and #231"
  - "Acknowledge in What Is Already Done that wt-auditor acceptance test was not formally executed"
  - "Align command names (jerry path resolve vs jerry resolve-output-path) between issue and use cases"
  - "Add resolution mechanism sentence to AC-2; add dependency notes to AC-6 and AC-8"
  - "Explicitly scope or exclude jerry path validate-agent"
```

---

*Scoring Agent: adv-scorer*
*Strategy: S-014 LLM-as-Judge*
*SSOT: .context/rules/quality-enforcement.md*
*Supporting artifacts: gh-144-consolidation-analysis.md, gh-144-use-cases.md, ADR-output-path-resolution-001.md*
*Scored: 2026-04-13*

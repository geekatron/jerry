# Quality Score Report: BUG-006 — Agent Output Paths Hardcoded

## L0 Executive Summary

**Score:** 0.891/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.82)

**One-line assessment:** A well-structured, evidence-backed bug entity that passes on completeness and consistency but misses the C4 threshold (0.95) primarily because the root cause analysis lacks causal depth and the UX skill file counts are estimated rather than verified — targeted improvements to these two areas are sufficient to reach threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md` + `/tmp/gh-issue-output-paths.md`
- **Deliverable Type:** Bug worktracker entity + GitHub Issue body (compound deliverable)
- **Criticality Level:** C4 (irreversible architecture/governance change; AE-002 auto-C3 applies, user-requested C4 override)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **User-Specified Threshold:** 0.95
- **Standard Threshold:** 0.92 (H-13)
- **Scored:** 2026-03-31

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.891 |
| **Threshold (user-specified)** | 0.95 |
| **Standard Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no prior adv-executor reports) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All 13 skills covered; line numbers verified for eng-team; UX per-file breakdown present |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Claims align between entity and GH issue; one minor omission (saucer-boy-framework-voice) |
| Methodological Rigor | 0.20 | 0.82 | 0.164 | Root cause thin — "built before convention" lacks traceable evidence; UX file estimates unverified |
| Evidence Quality | 0.15 | 0.90 | 0.135 | All eng-team and red-team path claims verified against actual files; ps-researcher YAML quoted |
| Actionability | 0.15 | 0.93 | 0.140 | 7 ACs all grep/find verifiable; 7 implementation tasks with explicit dependency graph |
| Traceability | 0.10 | 0.84 | 0.084 | Bidirectional cross-references present; convention origin not traced to a specific source |
| **TOTAL** | **1.00** | | **0.891** | |

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence:**

The entity addresses all 7 success criteria at a surface level. The impact assessment table enumerates all 13 affected skills (eng-team, red-team, and 11 UX sub-skills) with per-category file counts. Line number citations for eng-team SKILL.md (lines 119-128 and 261-273) were independently verified against the actual file. The eng-team section lists 4 file categories with exact counts (10 governance YAML, 10 composition YAML, 1 SKILL.md, 1 template = 22 config files), confirmed by glob. Red-team lists "22+" config files — the actual count is 25 (11 governance + 11 composition + 1 SKILL.md + 2 templates) — "22+" is technically correct but imprecise. The UX skills per-sub-skill table shows file categories without specific file counts or line numbers, relying on "~68" as a round-number estimate. The committed output file list (28 files across 4 engagements) was verified against filesystem and is correct. The correct reference architecture is cited with an actual YAML block quote from `ps-researcher.agent.yaml`. The diataxis minor issue is correctly scoped as a separate sub-task.

**Gaps:**

- UX section does not provide line numbers for any sub-skill file. The per-skill table shows categories ("yes", "2 templates") but not specific line references. This is consistent with success criterion 1 ("specific file counts and line numbers") being only partially met for the UX skill family — line numbers are absent for all ~68 UX files.
- Red-team file count stated as "22+" where the precise count verifiable by grep is 25. Minor imprecision reduces completeness.
- The `saucer-boy-framework-voice` skill appears in the GH issue's not-affected list but is absent from the worktracker entity's not-affected table. This is a minor omission.

**Improvement Path:**

Add specific line number citations for at least one representative UX sub-skill (e.g., `ux-heart-metrics/SKILL.md:152` and `ux-heart-metrics/SKILL.md:717`) to demonstrate the pattern holds across UX skills. State red-team as "25" rather than "22+".

---

### Internal Consistency (0.92/1.00)

**Evidence:**

The Summary sections in both the worktracker entity and the GH issue body are word-for-word identical (4-point bulleted impact list). The scope numbers (13 skills, ~112 files, 32 agents, 28 committed files) are consistent across both documents and across every table where they appear. The acceptance criteria (AC-1 through AC-7) are identical in both documents. The implementation plan tasks (TASK-006 through TASK-012) appear only in the worktracker entity, which is appropriate for operational detail. The proposed path convention appears in both documents in identical form. The root cause narrative in both documents is consistent in substance and scope.

**Gaps:**

- The GH issue "not affected" skills list includes `saucer-boy-framework-voice` as a separate entry; the worktracker entity omits it from the not-affected table (which lists 11 skills). This is a minor inconsistency between the two documents — the entity could arguably be considered complete given `saucer-boy-framework-voice` is registered separately in CLAUDE.md, but the omission creates a surface-level discrepancy.
- The eng-team agent count in the Impact Assessment table (10) matches the governance file count (10 confirmed by grep), but the red-team agent count (11) implies 11 composition files — verified as correct (11 red-* composition files confirmed).

**Improvement Path:**

Add `saucer-boy-framework-voice` to the worktracker entity's not-affected table to match the GH issue. State red-team file count precisely as 25 in both documents.

---

### Methodological Rigor (0.82/1.00)

**Evidence:**

The entity applies a systematic audit methodology: per-skill enumeration, per-category file counts, actual file path patterns from the filesystem, and a distinction between files-on-disk versus config-only impacts. The implementation plan uses explicit task decomposition with dependency annotations and a parallelization statement. The acceptance criteria are well-structured and cover both remediation (AC-1 through AC-4) and prevention (AC-5 through AC-7). The correct/incorrect path pattern contrast is clearly structured with code blocks.

**Gaps:**

- **Root cause analysis is structurally present but causally thin.** The claim "built before the convention was established by /problem-solving" is asserted without evidence. No specific commit, ADR, PR, or date when the `/problem-solving` convention was established is cited. The claim about UX skills being "patterned after eng-team/red-team during PROJ-022" is plausible but unverified — no PROJ-022 work item, ADR, or audit result is referenced. A rigorous root cause analysis at C4 criticality should trace the causal chain to a named decision point or governance gap, not just assert temporal precedence.
- **UX file count of "~68" is an estimate.** The UX skill audit table uses category counts ("yes" markers) without totaling them. The ~68 figure does not appear to be derived from an actual file count — a grep scan of `skills/ux-*/` would confirm or refute this. The estimate could be materially wrong if rules files or template counts differ from the implied values.
- **No FMEA or failure mode analysis.** At C4 criticality, methodological rigor expectations include structured failure mode consideration. The entity identifies consequences (multi-tenancy collision, portability failure) but does not analyze failure probability or detectability in the framework's current enforcement architecture.

**Improvement Path:**

(1) Add a traceable evidence reference for when the `/problem-solving` output convention was established — even a "first commit adding `projects/${JERRY_PROJECT}/research/`" or "introduced in PROJ-006" statement would suffice. (2) Run `find skills/ux-* -name "*.md" -o -name "*.yaml" | grep -v output | wc -l` to produce an exact file count rather than "~68". (3) Add one sentence per contributing factor explaining what enforcement mechanism was missing that would have caught this — this exists implicitly in "no MEDIUM standard" and "no CI gate" but could be elevated as a gap analysis.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

All quantitative claims about eng-team were verified independently:
- 28 committed output files in 4 engagement directories: confirmed by filesystem glob
- 10 governance YAML files: confirmed by glob (exact list)
- 10 composition YAML files: confirmed by glob (exact list)
- SKILL.md lines 119-128 (agent table with hardcoded paths): confirmed by file read
- SKILL.md lines 261-273 (output structure code block): confirmed by file read
- Governance YAML `output.location` field pattern: confirmed by grep (`skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md`)
- Red-team: 11 governance and 11 composition YAMLs confirmed by glob
- `ps-researcher.agent.yaml` output location `projects/${JERRY_PROJECT}/research/{ps-id}-{entry-id}-{topic-slug}.md`: confirmed by file read
- UX `ux-heuristic-evaluator.governance.yaml` output.location field confirmed by grep

The GH issue cross-references (#192 and #144) are present in both documents and contextually appropriate (upstream enhancements vs. this immediate bug fix).

**Gaps:**

- Red-team SKILL.md lines 521-528 and 535 cited in the entity but not independently verified in this scoring pass. Based on the pattern of accurate citations elsewhere, these are likely correct — but absence of verification means the score cannot reach 0.95+.
- The "~112 files requiring updates" aggregate is a sum of stated estimates (22 + "22+" + "~68"). The precision of this number depends on the accuracy of the UX estimate, which is unverified.
- The claim that UX skills "were patterned after eng-team/red-team during PROJ-022" is not supported by a cited artifact.

**Improvement Path:**

Verify the red-team SKILL.md line citations (521-528, 535). Run an actual file count for UX skills and replace "~68" with an exact number. Consider adding a verification note: "Path claims verified by grep on 2026-03-31."

---

### Actionability (0.93/1.00)

**Evidence:**

All 7 acceptance criteria are mechanically verifiable:
- AC-1: `grep -r "skills/.*/output" skills/` → zero results after fix
- AC-2: `ls skills/eng-team/output/` → directory absent after fix
- AC-3: `find skills/ -type d -name output` → zero results after fix
- AC-4: Schema validation command exists (`jerry ast validate` or JSON Schema validator)
- AC-5: Grep for `howto/` vs `how-to/` in diataxis files
- AC-6: MEDIUM standard presence in `agent-development-standards.md`
- AC-7: `.gitignore` contains `skills/*/output/`

The implementation plan provides 7 named tasks (TASK-006 through TASK-012) with scope, file counts, and explicit dependency graph. The parallelization statement is precise: TASK-006, 007, 008, 011, 012 can run in parallel; TASK-009 depends on TASK-006; TASK-010 depends on TASK-006 through TASK-008.

**Gaps:**

- The implementation plan does not specify the verification step for each task (i.e., what command proves TASK-006 is done before TASK-009 can start). For C4 work, explicit verification commands at dependency boundaries reduce handoff risk.
- No owner assignment on any task — the main entity is `unassigned`, and the child tasks inherit this. For C4 criticality, assigning ownership is expected.
- The proposed path convention for UX wave signoff files (`wave-signoff-{wave-N}.md`) is presented as a suggestion ("proposed pattern") without a decision — it would benefit from being framed as a required pattern in AC-1 or in an explicit ADR reference.

**Improvement Path:**

Add a verification command to each task row (e.g., "Verified by: `grep -r skills/eng-team/output skills/`"). Note that the path convention for engagement-based skills requires an ADR if it is a new convention (AE-003 auto-C3 minimum for new ADRs).

---

### Traceability (0.84/1.00)

**Evidence:**

Forward traceability: entity -> GH Issue #230 present in frontmatter. Parent -> PROJ-030-bugs present. Related issues #192 and #144 linked with descriptions distinguishing them from this bug. Child tasks TASK-006 through TASK-012 listed. GH Issue body contains related issues section with the same two related issues and a clarifying statement that they are upstream enhancements.

Backward traceability: the correct reference architecture is traced to `skills/problem-solving/composition/ps-researcher.agent.yaml` with an actual YAML quote, enabling verification. The affected file paths are enumerated with sufficient specificity to allow a developer to locate and fix each one.

Auto-escalation traceability: AE-002 is correctly cited as applicable.

**Gaps:**

- The root cause section states the `/problem-solving` convention was established "before" eng-team/red-team were built, but does not cite the work item or commit where this convention was introduced. Without this, the causal claim cannot be fully traced — it is an assertion, not a traceable finding.
- No reference to `mcp-tool-standards.md` section on eng-*/red-* output persistence rationale, which contains relevant context ("engagement-scoped output requires file-based persistence per P-002"). The bug is partly rooted in the tension between P-002 engagement-scoped outputs and the project-relative convention — tracing this to the governance document would strengthen the analysis.
- The proposed new MEDIUM standard (AC-6: AD-M-011) is not traced to the standards file's current highest entry (AD-M-010) to confirm numbering continuity.

**Improvement Path:**

Add a reference to the work item or commit that established the `projects/${JERRY_PROJECT}/` convention in `/problem-solving`. Add a citation to `mcp-tool-standards.md` (the exclusion note for eng-*/red-* MK usage) as governance context. Verify that AD-M-011 is the correct next number in `agent-development-standards.md`.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.82 | 0.90 | Trace root cause to a specific named evidence source: identify the commit or work item that introduced `projects/${JERRY_PROJECT}/` in `/problem-solving`, and cite PROJ-022 work items that show UX skills were modeled after eng-team. Replace "~68" with an exact UX file count from `find`. |
| 2 | Traceability | 0.84 | 0.92 | Add citation to `mcp-tool-standards.md` (eng-*/red-* exclusion note) as governance context. Trace the convention origin to a specific source. Confirm AD-M-011 numbering in `agent-development-standards.md`. |
| 3 | Completeness | 0.92 | 0.95 | Add line number citations for at least one representative UX sub-skill (e.g., `ux-heart-metrics/SKILL.md:152,717`). Correct red-team file count from "22+" to "25". Add `saucer-boy-framework-voice` to the not-affected table. |
| 4 | Evidence Quality | 0.90 | 0.94 | Verify red-team SKILL.md lines 521-528 and 535. Add a "verified on 2026-03-31" provenance note. Replace "~112" with a sum of verified counts. |
| 5 | Internal Consistency | 0.92 | 0.95 | Add `saucer-boy-framework-voice` to the not-affected table in the worktracker entity. Align red-team file count to "25" in both documents. |
| 6 | Actionability | 0.93 | 0.96 | Add verification command per task in implementation plan. Flag that the proposed engagement path convention requires an ADR (AE-003). |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score (specific files, line numbers, grep results)
- [x] Uncertain scores resolved downward (Methodological Rigor: between 0.82 and 0.85, chose 0.82; Traceability: between 0.84 and 0.88, chose 0.84)
- [x] C4 first-draft calibration applied — first-draft C4 deliverables rarely exceed 0.90 composite without multiple revision cycles
- [x] No dimension scored above 0.95 (highest is Actionability at 0.93, with documented evidence and documented gaps)
- [x] Composite verified mathematically: (0.92)(0.20) + (0.92)(0.20) + (0.82)(0.20) + (0.90)(0.15) + (0.93)(0.15) + (0.84)(0.10) = 0.184 + 0.184 + 0.164 + 0.135 + 0.1395 + 0.084 = 0.8905 ≈ 0.891

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.891
threshold: 0.95
weakest_dimension: methodological_rigor
weakest_score: 0.82
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Trace root cause to specific evidence — commit or work item establishing the projects/${JERRY_PROJECT}/ convention"
  - "Replace UX file estimate (~68) with verified count from find command"
  - "Add line number citations for at least one representative UX sub-skill"
  - "Verify red-team SKILL.md lines 521-528 and 535"
  - "Correct red-team file count from 22+ to 25 in both documents"
  - "Add saucer-boy-framework-voice to worktracker not-affected table"
  - "Flag that proposed engagement path convention requires ADR per AE-003"
  - "Add verification commands to implementation task dependency boundaries"
```

---

*Scored by:* adv-scorer v1.0.0
*SSOT:* `.context/rules/quality-enforcement.md`
*Scoring Strategy:* S-014 LLM-as-Judge, 6-dimension weighted composite
*Date:* 2026-03-31

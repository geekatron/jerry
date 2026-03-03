# ADR-001 Implementation Plan: NPT-014 Elimination

> **PS:** PROJ-014
> **Implements:** ADR-001 (Universal NPT-014 Elimination Policy)
> **Created:** 2026-02-28
> **Status:** PROPOSED
> **Agent:** ps-architect
> **Source Inventory:** `phase-1-npt014-inventory.md` (this directory)
> **Criticality:** C3 (AE-002: touches `.context/rules/`; AE-003: implements accepted ADR)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What this plan does and why |
| [Upgrade Templates](#upgrade-templates) | NPT-013 XML-tagged pattern and agent batch template |
| [Phase 1: Baseline (Complete)](#phase-1-baseline-complete) | Inventory scan -- already done |
| [Phase 2: Rule Files](#phase-2-rule-files) | 8 NPT-014 instances in `.context/rules/` |
| [Phase 3: Agent Definitions](#phase-3-agent-definitions) | Template-based batch + individual agent upgrades |
| [Phase 4: SKILL.md Files](#phase-4-skillmd-files) | 4 NPT-014 instances across 2 SKILL.md files |
| [Effort Classification](#effort-classification) | Per-phase effort estimate |
| [Risk Assessment](#risk-assessment) | AE-002, testing, baseline concerns |
| [Exclusions](#exclusions) | What is explicitly out of scope |
| [NPT-009 Secondary Queue](#npt-009-secondary-queue) | NPT-009 to NPT-013 upgrades (lower priority) |
| [Execution Checklist](#execution-checklist) | Step-by-step implementation order |

---

## L0: Executive Summary

This plan operationalizes ADR-001's decision to eliminate all NPT-014 (bare prohibition) instances from the Jerry Framework. The Phase 1 inventory identified 47 NPT-014 instances across 4 groups. This plan provides the specific upgrade text, templates, and sequencing to convert each instance to NPT-009 (structured negation with consequence) or NPT-013 (full structured format with consequence, alternative, and verification).

The plan is organized into 4 phases. Phase 1 (inventory) is complete. Phases 2-4 cover rule files, agent definitions, and SKILL.md files respectively. Group 4 (templates and constitution) from the inventory is deferred to a separate execution plan because it includes the constitution (AE-001: auto-C4) and requires different review procedures.

The dominant pattern is the agent `forbidden_actions` list, which accounts for approximately 70% of all NPT-014 instances. A single batch template covers this entire class, making Phase 3 the highest-volume but lowest-difficulty phase.

---

## Upgrade Templates

### Template A: NPT-013 Constraint Format (for Rule Files and SKILL.md)

The target format for HARD constraints in rule files uses an XML-tagged structure. The `<verify>` tag is included only for HARD constraints (H-series rules). MEDIUM and SOFT constraints omit `<verify>`.

```xml
<constraint id="{ID}" source="{SOURCE}" severity="{HARD|MEDIUM|SOFT}">
  <prohibition>{ORIGINAL_PROHIBITION_TEXT}</prohibition>
  <consequence>{WHAT_BREAKS_OR_DEGRADES}</consequence>
  <instead>{WHAT_TO_DO_INSTEAD}</instead>
  <verify>{VERIFICATION_STEP}</verify>
</constraint>
```

**Field definitions:**

| Field | Required | Content |
|-------|----------|---------|
| `id` | Yes | Inventory ID (e.g., G1-003) or rule ID (e.g., H-05) |
| `source` | Yes | Originating principle or rule (e.g., P-003, H-05) |
| `severity` | Yes | HARD, MEDIUM, or SOFT per tier vocabulary |
| `prohibition` | Yes | The original prohibition text, preserved verbatim |
| `consequence` | Yes | Specific failure mode -- names what breaks, who is affected, how severe |
| `instead` | Recommended | Positive behavioral alternative; omit only when no meaningful alternative exists |
| `verify` | HARD only | How to confirm the constraint is being followed |

**Consequence specificity standard (from ADR-001 Pre-Mortem, FMEA RPN 72):** Consequences MUST name the specific failure mode (e.g., "CI blocks merge", "environment corruption", "unbounded recursion exhausts context"). Generic outcomes (e.g., "quality degrades", "bad things happen") are rejected. Each consequence must answer: what breaks, for whom, and how severely.

**Important note on format:** The XML-tagged format above is the **design target** for a future rule file restructuring. For the current implementation, NPT-014 instances in rule files are upgraded **in-place** using natural language additions to the existing prose/table format. The XML structure serves as the content specification (what fields must be present), not the literal markup to insert into existing markdown files. Each Phase 2 entry below specifies the exact upgrade text in the format native to its host file.

### Template B: Agent Forbidden Actions Batch Template

This template replaces the current bare `P-XXX VIOLATION: DO NOT X` pattern across all agent `<capabilities>` sections. It applies to the ~33 instances sharing the identical 5-item forbidden actions list structure.

**Current pattern (NPT-014):**

```markdown
**Forbidden Actions (Constitutional):**
- **P-003 VIOLATION:** DO NOT spawn subagents that spawn further subagents
- **P-020 VIOLATION:** DO NOT override explicit user instructions
- **P-022 VIOLATION:** DO NOT {agent-specific deception variant}
- **P-002 VIOLATION:** DO NOT return {output-type} without file output
- **P-0XX VIOLATION:** DO NOT {domain-specific violation}
```

**Upgraded pattern (NPT-009):**

```markdown
**Forbidden Actions (Constitutional):**
- **P-003 VIOLATION:** DO NOT spawn subagents that spawn further subagents. Consequence: unbounded recursion exhausts the context window and violates the single-level nesting constraint (H-01). Instead: return results to the orchestrator for coordination.
- **P-020 VIOLATION:** DO NOT override explicit user instructions. Consequence: unauthorized action; user loses control of the session and trust in the framework. Instead: present options and wait for user direction.
- **P-022 VIOLATION:** DO NOT {agent-specific deception variant}. Consequence: {agent-specific consequence -- see lookup table below}. Instead: {agent-specific alternative -- see lookup table below}.
- **P-002 VIOLATION:** DO NOT return {output-type} without file output. Consequence: work product is lost when the session ends; downstream agents cannot access results. Instead: persist all outputs using the Write tool to the designated project path.
- **P-0XX VIOLATION:** DO NOT {domain-specific violation}. Consequence: {domain-specific consequence}. Instead: {domain-specific alternative}.
```

**P-003 and P-020 lines are identical across all agents.** Only P-022, P-002, and domain-specific lines require per-agent customization.

### Template B Lookup Table: P-022 Variants

The P-022 line varies by agent. Each agent has a specific deception variant. The consequence and alternative for each:

| Agent Family | P-022 Prohibition | Consequence | Instead |
|-------------|-------------------|-------------|---------|
| ps-analyst | DO NOT hide uncertainty or present speculation as fact | Downstream agents and users make decisions based on false confidence levels, compounding errors through the analysis chain. | State uncertainty explicitly with confidence bounds; label inferences as inferences. |
| ps-researcher | DO NOT claim to have found information you didn't find | Fabricated findings propagate through synthesis and architecture decisions, producing recommendations grounded in fiction. | Report gaps honestly; label unfound information as "not found" with search methodology documented. |
| ps-architect | DO NOT hide negative consequences of a decision | Stakeholders approve decisions without understanding risks; negative consequences surface in production instead of during review. | Document all negative consequences in the Consequences section, per P-022 and ADR Nygard format. |
| ps-critic | DO NOT hide quality issues or inflate scores | Substandard deliverables pass quality gates; the quality enforcement system loses credibility and effectiveness. | Report all findings with evidence; score strictly against the rubric without leniency bias. |
| ps-reviewer | DO NOT minimize or hide quality issues | Defects reach production; technical debt accumulates silently until systemic failure. | Report all issues at their actual severity with evidence. |
| ps-investigator | DO NOT hide uncertainty or gaps in evidence | Root cause analysis based on incomplete evidence produces incorrect fixes that leave the actual failure mode unaddressed. | State evidence gaps explicitly; label confidence as high/medium/low per evidence chain completeness. |
| ps-validator | DO NOT mark as validated without evidence | False validation creates a governance breach; unvalidated work enters the codebase as if it had been verified. | Require evidence for every validation claim; mark unverifiable items as "UNVERIFIABLE" with explanation. |
| ps-synthesizer | DO NOT hide contradictions between sources | Synthesized output presents false consensus; contradictions surface later as conflicting guidance. | Surface contradictions explicitly; document which sources disagree and on what. |
| ps-reporter | DO NOT misrepresent progress or hide blockers | Stakeholders make resource and timeline decisions based on false progress signals. | Report actual progress with blockers listed prominently. |
| orch-planner | DO NOT misrepresent workflow complexity | Underestimated workflows fail at execution; resource allocation is incorrect. | State true complexity with phase count, dependency depth, and risk factors. |
| orch-tracker | DO NOT misrepresent execution status | Phase gates pass incorrectly; downstream phases start on incomplete prerequisites. | Report actual execution state from file system artifacts, not assumed state. |
| orch-synthesizer | DO NOT make claims without artifact evidence | Cross-pipeline synthesis presents unsupported conclusions; downstream decisions are grounded in fabrication. | Cite specific artifact paths for every claim; label inferences explicitly. |
| nse-integration | DO NOT claim integration complete without verification | Unverified interfaces fail at runtime; integration defects propagate to dependent systems. | Verify each interface against the ICD before claiming completion. |
| nse-qa | DO NOT claim compliance without evidence | Non-compliant artifacts pass quality gates; compliance failures surface during audit. | Provide evidence artifact for each compliance claim. |
| nse-risk | DO NOT suppress risks or hide RED risks | Unmitigated risks materialize without preparation; stakeholders are blindsided. | Report all risks at their actual severity; RED risks must be escalated immediately. |
| nse-requirements | DO NOT create orphan requirements | Requirements without traceability cannot be verified or validated; they become governance dead weight. | Link every requirement to a parent and at least one verification method. |
| nse-explorer | DO NOT prematurely converge on a single option | Trade study loses value; alternatives are dismissed without evaluation. | Maintain at minimum 2 viable options until the evaluation criteria produce a clear winner. |
| nse-verification | DO NOT claim pass without evidence | Unverified artifacts enter the verified baseline; V&V integrity is compromised. | Provide verification evidence (test results, inspection records) for every pass claim. |
| nse-configuration | DO NOT claim baseline without approval | Unapproved configurations bypass change control; configuration drift occurs without traceability. | Obtain explicit approval before baselining; document the approval authority. |
| nse-reviewer | DO NOT approve with RED criteria | Critical defects pass review; downstream phases inherit known-bad artifacts. | Require all RED criteria to be resolved or explicitly waived by the review authority before approval. |
| wt-verifier | DO NOT mark incomplete work as complete | False completion signals trigger downstream work on incomplete prerequisites; work tracker integrity is compromised. | Report actual completion state; mark partially complete items with remaining work documented. |
| wt-auditor | DO NOT auto-fix issues without user approval | Unauthorized modifications violate P-020; audit trail integrity is compromised. | Report findings with recommended fixes; wait for user approval before modifying any file. |
| wt-auditor | DO NOT ignore worktracker integrity violations | Integrity violations compound over time; the worktracker becomes unreliable as SSOT. | Report all violations regardless of severity; classify by impact. |
| wt-visualizer | DO NOT modify work item content | Read-only agent modifying data violates the separation of concerns; data corruption risk. | Report visualization results only; direct users to appropriate agents for modifications. |
| wt-visualizer | DO NOT fabricate data or relationships | Visualizations based on fabricated data produce incorrect mental models; users make decisions based on false structure. | Render only relationships present in the source data; mark missing data as "data not available." |
| ts-parser | DO NOT claim parsing success when errors occurred | Downstream agents process corrupt data; extraction quality degrades silently. | Report parsing errors explicitly with error location and type; mark affected segments. |
| ts-parser | DO NOT modify or "correct" transcript text content | Original transcript integrity is destroyed; corrections cannot be audited against source. | Preserve original text verbatim; corrections belong in a separate annotation layer. |
| ts-parser | DO NOT fabricate timestamps for plain text files | Fabricated timestamps produce incorrect temporal sequencing; downstream analysis is corrupted. | Mark plain text entries as "timestamp unavailable"; use segment ordering instead. |
| ts-extractor | DO NOT extract entities without citation to source | Uncited extractions cannot be verified; provenance chain is broken. | Include chunk reference and segment number for every extracted entity. |
| ts-extractor | DO NOT claim high confidence without evidence | Confidence inflation causes downstream agents to skip verification of uncertain extractions. | Calibrate confidence against extraction evidence; label ambiguous extractions as LOW or MEDIUM. |
| ts-extractor | DO NOT invent entities not in transcript | Hallucinated entities contaminate the extraction database; downstream analysis operates on fiction. | Extract only entities explicitly present in the transcript text; mark inferred entities separately. |
| ts-formatter | DO NOT create files exceeding 35K tokens | Oversized files exceed context window limits; downstream agents cannot process them. | Split output across multiple files using the chunking protocol. |
| ts-formatter | DO NOT use non-standard anchor formats | Non-standard anchors break cross-file navigation; link integrity is compromised. | Use the anchor format defined in markdown-navigation-standards.md (H-23). |
| ts-mindmap-mermaid | DO NOT generate invalid Mermaid syntax | Invalid syntax produces rendering failures; visualizations are unusable. | Validate Mermaid syntax before writing output; use only documented Mermaid constructs. |
| ts-mindmap-ascii | DO NOT exceed 80 character width | Lines exceeding 80 characters break terminal rendering and markdown display. | Wrap or truncate node labels to fit within 80-character width. |

### Template B Lookup Table: P-002 Variants

The P-002 line has a standard pattern but the output type varies:

| Agent | Output Type in P-002 Line |
|-------|---------------------------|
| ps-analyst | analysis results |
| ps-researcher | research results |
| ps-architect | ADR content |
| ps-critic | critique |
| ps-reviewer | review |
| ps-investigator | investigation |
| ps-validator | validation results |
| ps-synthesizer | synthesis |
| ps-reporter | report |
| orch-planner | plans |
| orch-tracker | status (uses "report status without updating files") |
| orch-synthesizer | synthesis |
| nse-* | (varies: integration status, compliance, risk assessment, etc.) |
| wt-verifier | verification report (uses "return transient output only") |
| wt-auditor | audit results |
| wt-visualizer | (uses "return transient output only") |
| ts-parser | parsed data |
| ts-extractor | extractions |
| ts-formatter | (uses "return without creating all packet files") |
| ts-mindmap-mermaid | (uses "return without creating mindmap file") |
| ts-mindmap-ascii | (uses "return without creating ASCII file") |

The P-002 consequence and alternative are **identical across all agents:**
- **Consequence:** work product is lost when the session ends; downstream agents cannot access results.
- **Instead:** persist all outputs using the Write tool to the designated project path.

### Template B Lookup Table: Domain-Specific Lines

Some agents have additional domain-specific forbidden action lines beyond the constitutional triplet + P-002. These require individual upgrade text:

| Agent | Domain Line | Consequence | Instead |
|-------|------------|-------------|---------|
| ps-analyst | DO NOT draw conclusions without evidence | Unsupported conclusions mislead downstream decision-making; architecture decisions are built on speculation. | Ground every conclusion in cited evidence; label inferences as such. |
| ps-researcher | DO NOT make claims without citations | Uncited claims cannot be verified or traced to source; research loses provenance. | Cite source for every claim using the L0/L1/L2 citation format. |
| ps-architect | DO NOT recommend without evaluating alternatives | Single-option recommendations bypass the trade-off analysis that ADR format requires; stakeholders cannot assess decision quality. | Evaluate at minimum 3 alternatives per P-011 before recommending. |
| ps-critic | DO NOT self-invoke or trigger next iteration | Critic controlling iteration violates P-003; the orchestrator loses coordination authority. | Return critique results to the orchestrator; the orchestrator decides whether to iterate. |
| ps-reviewer | DO NOT claim issues without evidence | Evidence-free claims waste implementer time investigating phantom issues. | Include file path, line number, and code snippet for every reported issue. |
| ps-investigator | DO NOT claim root cause without evidence | Unfounded root cause claims lead to incorrect fixes; the actual failure mode persists. | Present evidence chain (5 Whys trace) supporting each root cause claim. |
| ps-validator | DO NOT claim validation without evidence | Same consequence as "mark as validated without evidence" above. | Same alternative as above. |
| ps-synthesizer | DO NOT present patterns without citing sources | Uncited patterns cannot be verified; synthesis loses traceability. | Cite specific source documents for every identified pattern. |
| ps-reporter | DO NOT show inaccurate task status | Inaccurate status causes incorrect resource allocation and priority decisions. | Read actual task status from worktracker files; never infer or assume status. |
| orch-planner | DO NOT omit mandatory disclaimer from outputs | Missing disclaimer violates P-043; NSE outputs may be mistaken for official NASA guidance. | Include the P-043 mandatory disclaimer on all persisted outputs. |
| orch-planner | DO NOT use hardcoded pipeline names | Hardcoded names (ps-pipeline, nse-pipeline) break when pipeline naming conventions change. | Resolve pipeline names dynamically from the orchestration configuration. |
| orch-tracker | DO NOT omit mandatory disclaimer from outputs | Same as orch-planner above. | Same as orch-planner above. |
| orch-synthesizer | DO NOT omit mandatory disclaimer from outputs | Same as orch-planner above. | Same as orch-planner above. |
| orch-synthesizer | DO NOT synthesize without reading ALL artifacts | Partial synthesis produces incomplete conclusions; missing artifacts create blind spots. | Read every artifact listed in the synthesis input before producing output. |
| nse-integration | DO NOT integrate without documented ICD | Undocumented interfaces fail unpredictably; integration testing has no specification to verify against. | Require an Interface Control Document (ICD) before beginning integration activities. |
| nse-risk | DO NOT hide RED risks | Hidden RED risks bypass escalation; high-severity failures materialize without mitigation. | Escalate RED risks immediately to the review authority. |
| nse-requirements | DO NOT produce incomplete assessment without disclosure | Stakeholders treat incomplete assessments as complete; uncovered requirements create gaps. | Disclose coverage limitations explicitly; list areas not assessed. |
| nse-explorer | DO NOT dismiss alternatives without evaluation | Dismissed alternatives may contain the optimal solution; premature dismissal reduces trade study quality. | Evaluate each alternative against the stated criteria before elimination. |
| nse-verification | DO NOT hide verification gaps | Unacknowledged gaps create false confidence in verification coverage. | Document all gaps with rationale and recommended follow-up. |
| nse-configuration | DO NOT allow uncontrolled changes | Uncontrolled changes break configuration traceability; regression risk is unmanaged. | Route all changes through the change control process. |
| nse-reviewer | DO NOT claim ready without evidence | Premature readiness declarations skip required verification; quality gates are bypassed. | Provide entry/exit criteria evidence for every readiness claim. |
| ts-extractor | NEVER calculate stats from intermediate counts | Intermediate count calculations accumulate rounding and tracking errors; final statistics do not match actual extraction counts. | Calculate all statistics from the final populated arrays, never from running counters. |
| ts-extractor | NEVER report more items than actually extracted | Over-reporting creates false expectations about extraction completeness; downstream agents process phantom items. | Count extracted items from the output arrays; verify count matches array length. |
| orch-planner | DO NOT create ORCHESTRATION.yaml without complete phase definitions | Incomplete ORCHESTRATION.yaml causes phase execution failures; agents reference undefined phases. | Validate all phase definitions are complete before writing the ORCHESTRATION.yaml file. |

---

## Phase 1: Baseline (Complete)

**Status:** DONE
**Artifact:** `phase-1-npt014-inventory.md` (this directory)
**Summary:** 47 NPT-014 instances identified across 4 groups, 28 NPT-009 instances identified, 36 NPT-013 instances confirmed as already at target.

The baseline is captured. The inventory serves as the pre-upgrade reference. No modifications to any framework files have been made.

---

## Phase 2: Rule Files

> **AE-002 applies:** All files in `.context/rules/` trigger auto-C3 minimum.
> **Quality gate:** >= 0.92 (C3 threshold per quality-enforcement.md)
> **Effort:** MEDIUM (8 individual upgrades, each requiring domain-specific consequence text)
> **Dependency:** None -- this is the first implementation phase.

### Phase 2 Baseline Capture Protocol

Before modifying any rule file:

1. Record the current git commit hash: `git rev-parse HEAD`
2. Confirm all Phase 2 target files are clean: `git status`
3. Create a working branch: `git checkout -b feat/adr001-npt014-elimination`
4. The commit hash from step 1 is the Phase 2 baseline for ADR-001 reversibility

### Phase 2 Upgrade Table

Each row is one NPT-014 instance from the Phase 1 inventory Tier 1 queue.

#### P2-01 | G1-003 | python-environment.md | Line 3

**Current (NPT-014):**
```
> UV-only Python environment. NEVER use system Python.
```

**Upgraded (NPT-009):**
```
> UV-only Python environment. NEVER use system Python -- doing so causes environment corruption and CI build failures. Use `uv run` for all execution.
```

**Fields:**
- **Prohibition:** NEVER use system Python.
- **Consequence:** Environment corruption and CI build failures (sourced from H-05 consequence column: "Command fails. Environment corruption.").
- **Instead:** Use `uv run` for all execution (sourced from H-05 rule text).
- **Verify:** Not applicable -- this is a document header summary, not a HARD rule declaration. The HARD rule (H-05) is already NPT-013 at lines 23-24.

---

#### P2-02 | G1-007 | coding-standards.md | Line 81

**Current (NPT-014):**
```
NEVER catch 'Exception' broadly and silently swallow errors.
```

**Upgraded (NPT-009):**
```
NEVER catch 'Exception' broadly and silently swallow errors. Consequence: masked failures propagate silently through the call chain; root cause diagnosis becomes impossible when errors are swallowed. Instead: catch specific exception types from the DomainError hierarchy (ValidationError, NotFoundError, ConflictError) defined in `src/shared_kernel/exceptions.py`.
```

**Fields:**
- **Prohibition:** NEVER catch 'Exception' broadly and silently swallow errors. (preserved verbatim)
- **Consequence:** Masked failures propagate silently through the call chain; root cause diagnosis becomes impossible when errors are swallowed.
- **Instead:** Catch specific exception types from the DomainError hierarchy (ValidationError, NotFoundError, ConflictError) defined in `src/shared_kernel/exceptions.py`.

---

#### P2-03 | G1-011 | quality-enforcement.md | Line 81

**Current (NPT-014):**
```
These IDs MUST NOT be reassigned to prevent confusion with historical references.
```

**Upgraded (NPT-009):**
```
These IDs MUST NOT be reassigned. Consequence: reassignment breaks historical cross-references in ADRs, worktracker entries, and commit messages that cite the original rule ID; traceability chains become ambiguous. Instead: when consolidating rules, retire the old ID into the Retired Rule IDs table and document the mapping to its replacement.
```

**Fields:**
- **Prohibition:** These IDs MUST NOT be reassigned. (preserved; "to prevent confusion" clause removed as it is subsumed by the consequence)
- **Consequence:** Reassignment breaks historical cross-references in ADRs, worktracker entries, and commit messages that cite the original rule ID; traceability chains become ambiguous.
- **Instead:** When consolidating rules, retire the old ID into the Retired Rule IDs table and document the mapping to its replacement.

---

#### P2-04 | G1-014 | mandatory-skill-usage.md | Line 3

**Current (NPT-014):**
```
> Proactive skill invocation rules. DO NOT wait for user to invoke.
```

**Upgraded (NPT-009):**
```
> Proactive skill invocation rules. DO NOT wait for user to invoke -- delayed invocation causes H-22 violation, skill context is not loaded, and work quality degrades. Instead: trigger skills proactively when keyword conditions in the trigger map match.
```

**Fields:**
- **Prohibition:** DO NOT wait for user to invoke. (preserved verbatim)
- **Consequence:** H-22 violation; skill context is not loaded; work quality degrades (sourced from H-22 consequence: "Work quality degradation. Rework required.").
- **Instead:** Trigger skills proactively when keyword conditions in the trigger map match.

---

#### P2-05 | G1-017 | agent-development-standards.md | Line 186

**Current (NPT-014):**
```
Workers MUST NOT spawn sub-workers.
```

**Upgraded (NPT-009):**
```
Workers MUST NOT spawn sub-workers. Consequence: unbounded recursion exhausts the context window, violates P-003, and breaks the orchestrator's coordination authority. Instead: return results to the orchestrator, which coordinates all worker invocations.
```

**Fields:**
- **Prohibition:** Workers MUST NOT spawn sub-workers. (preserved verbatim)
- **Consequence:** Unbounded recursion exhausts the context window, violates P-003, and breaks the orchestrator's coordination authority.
- **Instead:** Return results to the orchestrator, which coordinates all worker invocations.

---

#### P2-06 | G1-018 | agent-development-standards.md | Line 187

**Current (NPT-014):**
```
Worker agents MUST NOT include 'Task' in 'capabilities.allowed_tools' (H-35).
```

**Upgraded (NPT-009):**
```
Worker agents MUST NOT include 'Task' in 'capabilities.allowed_tools' (H-35). Consequence: including Task enables recursive delegation, violating the single-level nesting constraint (P-003/H-01). Instead: declare only T1-T4 tier tools; the Task tool is reserved for T5 orchestrator agents.
```

**Fields:**
- **Prohibition:** Worker agents MUST NOT include 'Task' in 'capabilities.allowed_tools' (H-35). (preserved verbatim)
- **Consequence:** Including Task enables recursive delegation, violating the single-level nesting constraint (P-003/H-01).
- **Instead:** Declare only T1-T4 tier tools; the Task tool is reserved for T5 orchestrator agents.

---

#### P2-07 | G1-022 | project-workflow.md | Line 21

**Current (NPT-014):**
```
> H-04: Active project REQUIRED. MUST NOT proceed without `JERRY_PROJECT` set. See CLAUDE.md.
```

**Upgraded (NPT-009):**
```
> H-04: Active project REQUIRED. MUST NOT proceed without `JERRY_PROJECT` set -- doing so causes session work to be untracked, artifacts to land in incorrect paths, and worktracker integrity violations. Instead: set `JERRY_PROJECT` via the SessionStart hook or select a project using `jerry projects list`. See CLAUDE.md.
```

**Fields:**
- **Prohibition:** MUST NOT proceed without `JERRY_PROJECT` set. (preserved verbatim)
- **Consequence:** Session work is untracked, artifacts land in incorrect paths, and worktracker integrity violations occur (sourced from CLAUDE.md H-04 consequence: "Session will not proceed.").
- **Instead:** Set `JERRY_PROJECT` via the SessionStart hook or select a project using `jerry projects list`.

---

#### P2-08 | G1-024 | agent-routing-standards.md | Line 167

**Current (NPT-014):**
```
The system NEVER silently drops a routing request.
```

**Upgraded (NPT-009):**

This instance is a declarative guarantee phrased as a NEVER. Two upgrade approaches are valid:

**Option A -- Rephrase as positive assertion (recommended):**
```
The system guarantees that every routing request reaches either a terminal agent or the H-31 clarification fallback. Silent drops are a routing failure -- if no layer can resolve the request, the system escalates to user clarification rather than discarding the request.
```

**Option B -- Add consequence to the NEVER form:**
```
The system NEVER silently drops a routing request. Consequence: a silently dropped request means the user's intent is lost without notification, violating P-022 (no deception). Instead: if no routing layer can resolve the request, escalate to H-31 user clarification.
```

**Recommendation:** Option A. The original statement is a system invariant, not a prohibition directed at an agent. Rephrasing as a positive guarantee is clearer and eliminates the awkward "NEVER + no actor" construction. The consequence and alternative information from Option B should be included as supporting context.

---

## Phase 3: Agent Definitions

> **Effort:** LOW (template-based batch application for ~33 constitutional items; MEDIUM for ~14 domain-specific items)
> **Dependency:** Phase 2 MUST complete first (ADR-001 sequencing: rule files before agent definitions)
> **Quality gate:** >= 0.92 (C2 -- agent files are not in `.context/rules/` so AE-002 does not apply; however, agent definitions affect runtime behavior)

### Phase 3A: Batch Template Application (Constitutional Lines)

Apply Template B (above) to the following agents. For each agent, replace the existing `Forbidden Actions (Constitutional)` block with the upgraded version using:

1. **P-003 line:** Identical across all agents (use Template B verbatim)
2. **P-020 line:** Identical across all agents (use Template B verbatim)
3. **P-022 line:** Look up the agent in the P-022 Variants table above
4. **P-002 line:** Use the standard consequence/alternative with the agent's output type from the P-002 Variants table
5. **Domain-specific lines:** Look up the agent in the Domain-Specific Lines table above

**Agents requiring Phase 3A batch upgrade:**

| # | Agent File | NPT-014 Count | Lines Affected |
|---|-----------|----------------|----------------|
| 1 | `skills/problem-solving/agents/ps-analyst.md` | 5 | 86-90 |
| 2 | `skills/problem-solving/agents/ps-researcher.md` | 5 | 87-91 |
| 3 | `skills/problem-solving/agents/ps-architect.md` | 5 | 88-92 |
| 4 | `skills/problem-solving/agents/ps-critic.md` | 5 | 126-130 |
| 5 | `skills/problem-solving/agents/ps-reviewer.md` | 5 | 88-92 |
| 6 | `skills/problem-solving/agents/ps-investigator.md` | 5 | 58-62 |
| 7 | `skills/problem-solving/agents/ps-validator.md` | 5 | 99-103 |
| 8 | `skills/problem-solving/agents/ps-synthesizer.md` | 5 | 90-94 |
| 9 | `skills/problem-solving/agents/ps-reporter.md` | 5 | 49-53 |
| 10 | `skills/orchestration/agents/orch-planner.md` | 7 | 65-70, 88 |
| 11 | `skills/orchestration/agents/orch-tracker.md` | 5 | 62-66 |
| 12 | `skills/orchestration/agents/orch-synthesizer.md` | 6 | 66-71 |
| 13 | `skills/nasa-se/agents/nse-integration.md` | 6 | 56-61 |
| 14 | `skills/nasa-se/agents/nse-qa.md` | 5 | 64-68 |
| 15 | `skills/nasa-se/agents/nse-risk.md` | 6 | 62-68 |
| 16 | `skills/nasa-se/agents/nse-requirements.md` | 6 | 124-129 |
| 17 | `skills/nasa-se/agents/nse-explorer.md` | 6 | 71-77 |
| 18 | `skills/nasa-se/agents/nse-verification.md` | 6 | 59-64 |
| 19 | `skills/nasa-se/agents/nse-configuration.md` | 6 | 57-62 |
| 20 | `skills/nasa-se/agents/nse-reviewer.md` | 6 | 132-137 |
| 21 | `skills/worktracker/agents/wt-verifier.md` | 2 | 109, 111 |
| 22 | `skills/worktracker/agents/wt-auditor.md` | 4 | 110-113 |
| 23 | `skills/worktracker/agents/wt-visualizer.md` | 3 | 65, 67, 97 |
| 24 | `skills/transcript/agents/ts-parser.md` | 5 | 93-97 |
| 25 | `skills/transcript/agents/ts-extractor.md` | 7 | 49-53, 919-920 |
| 26 | `skills/transcript/agents/ts-mindmap-mermaid.md` | 3 | 45-47 |
| 27 | `skills/transcript/agents/ts-mindmap-ascii.md` | 3 | 45-47 |
| 28 | `skills/transcript/agents/ts-formatter.md` | 4 | 157-160 |

**Total NPT-014 instances addressed in Phase 3A:** ~142 individual prohibition lines across 28 agent files.

### Phase 3B: Individual Agent-Specific NPT-014 Instances

These are NPT-014 instances outside the `Forbidden Actions` section (e.g., in guardrails fallback sections or elsewhere in the agent body):

| # | Agent File | Location | Current Text | Upgrade |
|---|-----------|----------|-------------|---------|
| 1 | `ps-critic.md` | Line 38 | `You DO NOT manage the loop yourself - that would violate P-003` | `You DO NOT manage the loop yourself. Consequence: self-managed iteration violates P-003 and causes unbounded recursion. Instead: you are invoked on each iteration by the orchestrator, which controls the loop.` |
| 2 | `orch-planner.md` | Line 88 | `DO NOT create ORCHESTRATION.yaml without complete phase definitions` | Covered in Domain-Specific Lines table above. |
| 3 | `ts-extractor.md` | Line 868 | `DO NOT return extractions without creating the output file.` | `DO NOT return extractions without creating the output file. Consequence: extraction data is lost when the session ends; downstream agents cannot access results. Instead: persist all extractions using the Write tool before returning.` |

---

## Phase 4: SKILL.md Files

> **Effort:** LOW (4 NPT-014 instances across 2 files)
> **Dependency:** Phase 2 MUST complete first (ADR-001 sequencing: rule files before SKILL.md files)
> **Quality gate:** >= 0.92 (C2)

### Phase 4 Upgrade Table

#### P4-01 | G3-001 | saucer-boy/SKILL.md | Lines 126-127

**Current (NPT-014):**
```
Agent CANNOT invoke other agents. Agent CANNOT spawn subagents.
```

**Upgraded (NPT-009):**
```
Agent CANNOT invoke other agents. Agent CANNOT spawn subagents. Consequence: invoking other agents violates P-003 (single-level nesting); the session incurs unbounded recursion and context exhaustion. Instead: return results to the orchestrator for coordination with other agents.
```

---

#### P4-02 | G3-002 | saucer-boy-framework-voice/SKILL.md | Lines 282-283

**Current (NPT-014):**
```
Agents CANNOT invoke other agents. Agents CANNOT spawn subagents.
```

**Upgraded (NPT-009):**
```
Agents CANNOT invoke other agents. Agents CANNOT spawn subagents. Consequence: cross-agent invocation violates P-003 (single-level nesting); the session incurs unbounded recursion and context exhaustion. Instead: return results to the orchestrator for coordination with other agents.
```

---

#### P4-03 | G3-003 | saucer-boy/SKILL.md | Line 93

**Current (NPT-014):**
```
- Writing internal design docs, ADRs, or research artifacts
```
(This appears in a "Do NOT use when:" list)

**Upgraded (NPT-009):**
```
- Writing internal design docs, ADRs, or research artifacts -- personality voice is inappropriate for governance artifacts; use neutral technical voice for these output types
```

---

#### P4-04 | Note on "Do NOT use when:" Sections

The "Do NOT use when:" sections in SKILL.md files are routing disambiguation blocks (ADR-003 scope). Several items in these sections are already NPT-009 (they have alternatives like "use /saucer-boy-framework-voice" or "personality OFF"). Only the bare items (like P4-03 above) need NPT-014 elimination. The routing disambiguation format itself (whether to use XML-tagged constraints or markdown lists) is ADR-003's concern and is explicitly excluded from this plan.

---

## Effort Classification

| Phase | Files Affected | NPT-014 Count | Template Coverage | Effort | Rationale |
|-------|---------------|----------------|-------------------|--------|-----------|
| Phase 1 (Baseline) | 0 | N/A | N/A | DONE | Already complete |
| Phase 2 (Rule Files) | 6 rule files | 8 | 0% (each is unique) | MEDIUM | Each prohibition requires domain-specific consequence text; auto-C3 quality gate applies |
| Phase 3A (Agent Batch) | 28 agent files | ~142 lines | ~70% (Template B covers P-003, P-020, P-002) | LOW | High template coverage; P-022 and domain lines require lookup table consultation |
| Phase 3B (Agent Individual) | 3 agent files | 3 | 0% | LOW | Small count; straightforward upgrades |
| Phase 4 (SKILL.md) | 2 SKILL.md files | 4 | 0% (each is unique) | LOW | Small count; simple additions |

**Total implementation effort:** MEDIUM overall. Phase 2 is the bottleneck due to auto-C3 quality gate requirements and the need for individually crafted consequence text. Phases 3-4 are mechanical once the templates and lookup tables are established.

---

## Risk Assessment

### R-01: AE-002 Auto-Escalation for Rule Files

**Risk:** All Phase 2 changes touch `.context/rules/` files, triggering AE-002 (auto-C3 minimum).

**Quality gate applicable:** >= 0.92 weighted composite (C3 threshold per quality-enforcement.md).

**Mitigation:**
- Phase 2 changes are additive text only (consequence + alternative appended to existing prohibitions)
- No structural changes to file format, schema, or enforcement mechanisms
- The original prohibition text is preserved verbatim in every upgrade
- Self-review (H-15, S-010) applied before presenting each upgrade
- Creator-critic-revision cycle (H-14) with minimum 3 iterations for Phase 2 as a batch

### R-02: Agent Definition Runtime Behavior

**Risk:** Changing agent definition `<capabilities>` sections affects the system prompt visible to the agent LLM at runtime.

**Testing needed:**
- **Functional verification:** After Phase 3 upgrades, invoke each modified agent with a test prompt and confirm it still produces expected output format. Focus on agents that are frequently used: ps-researcher, ps-analyst, ps-architect, ps-critic.
- **Regression check:** The added consequence and alternative text should not cause the agent to over-fixate on the consequence description or change its core methodology. Monitor for behavioral regression in the first 5 uses of each upgraded agent.
- **Token budget check:** The additional text per agent (approximately 200-400 tokens for a 5-line forbidden actions block) is well within context budget. Confirm no agent exceeds CB-02 (50% context for tool results) due to the expanded system prompt.

**Mitigation:** Phase 3 upgrades are applied to the markdown body (system prompt content), not to the `.md` YAML frontmatter or `.governance.yaml` files. The official Claude Code fields (`name`, `description`, `model`, `tools`) are unchanged. The upgrade adds explanatory text to existing constraints, which should improve (not degrade) agent behavior by providing richer constraint context.

### R-03: Phase 2 Baseline Already Captured

**Question:** Is the Phase 2 baseline captured BEFORE any changes?

**Answer:** YES. The Phase 1 inventory (`phase-1-npt014-inventory.md`) documents every NPT-014 instance with file path, line number, and verbatim text. The current git commit (`94b33e0a`) on the `feat/proj-014-negative-prompting-research` branch is the baseline. No framework files have been modified by this implementation plan.

**Baseline preservation protocol (from ADR-001):**
1. Record commit hash before any Phase 2 file modifications
2. Create a working branch for NPT-014 elimination changes
3. The pre-modification commit hash is the reversibility reference point
4. After baseline capture, proceed with Phase 2 upgrades

### R-04: New NPT-014 Introduction (FMEA RPN 150)

**Risk:** New NPT-014 instances are created faster than old ones are eliminated.

**Mitigation (from ADR-001):**
- Integrate the NPT-014 diagnostic filter into H-17 quality scoring
- Update the `agent-development-standards.md` guardrails template to demonstrate NPT-009 format
- Template B in this plan provides the upgraded example that replaces the current bare template

### R-05: Formulaic Consequence Documentation (FMEA RPN 72)

**Risk:** Consequence text is generic ("quality degrades") rather than specific ("CI blocks merge").

**Mitigation:** The consequence specificity standard is embedded in this plan: every upgrade entry in Phase 2 includes specific, verifiable consequence text. The Template B lookup tables provide pre-written, domain-specific consequence text for every agent. Reviewers should reject any consequence that does not name a specific failure mode.

---

## Exclusions

The following are explicitly OUT OF SCOPE for this implementation plan:

### E-01: ADR-002 Phase 5B (Conditional on Phase 2)

ADR-002 (Constitutional Triplet and High-Framing Upgrades) addresses elevating select constraints from NPT-009 to NPT-013. This depends on Phase 2 experimental results for its framing-comparison components. Not addressed here.

### E-02: ADR-003 Component B (Conditional on Phase 2)

ADR-003 (Routing Disambiguation Standard) establishes the NPT-010 format for "Do NOT use when:" sections. The format of routing disambiguation blocks is ADR-003's scope, not this plan's. This plan only upgrades bare NPT-014 items within existing "Do NOT use when:" sections; it does not restructure those sections.

### E-03: NPT-013 Instances Already at Target

The inventory identified 36 NPT-013 instances that already meet the target pattern. These are not modified.

### E-04: Group 4 (Templates + Constitution)

The inventory identified 6 NPT-014 instances in Group 4:
- 1 in `JERRY_CONSTITUTION.md` (P-022 SHALL NOT list) -- triggers AE-001 (auto-C4)
- 1 in `SPIKE.md` template

Because `JERRY_CONSTITUTION.md` triggers AE-001 (auto-C4, the highest criticality level), it requires a separate implementation plan with C4 quality gates (>= 0.95 threshold) and full tournament review. Bundling a C4 change with C2/C3 changes would force the entire batch through C4 review, which is disproportionate.

The `SPIKE.md` template NPT-014 instance is trivial and can be addressed in a separate low-effort change.

### E-05: NPT-009 to NPT-013 Upgrades

The inventory identified 28 NPT-009 instances (have consequence OR alternative, but not both). Upgrading these to NPT-013 (adding the missing element) is a separate, lower-priority activity. See [NPT-009 Secondary Queue](#npt-009-secondary-queue) below for the list.

### E-06: Analytical Content and Methodology Sections

This plan modifies ONLY guardrails and forbidden_actions sections in agent definitions. Agent `<identity>`, `<purpose>`, `<methodology>`, and `<output>` sections are not touched.

---

## NPT-009 Secondary Queue

These 28 instances already have either consequence or alternative. Adding the missing element completes them to NPT-013. This is lower priority than NPT-014 elimination but can be parallelized with Phase 3-4 if desired.

The full list is in the Phase 1 inventory under "Secondary Queue: NPT-009 to NPT-013 Upgrades" (entries S-01 through S-20). Summary:

| Group | NPT-009 Count | Missing Element |
|-------|---------------|-----------------|
| Rule files | 12 | Mixed (some lack consequence, some lack alternative) |
| Agent definitions | 9 | Mostly lack consequence (error message quoted as partial consequence) |
| SKILL.md | 3 | Mostly lack consequence |
| Templates + Constitution | 4 | Mostly lack consequence |

**Recommendation:** Address the rule file NPT-009 instances (S-01 through S-10) alongside Phase 2, since those files are already being modified. Address agent and SKILL.md NPT-009 instances alongside Phases 3-4.

---

## Execution Checklist

### Pre-Implementation

- [ ] Record baseline commit hash: `git rev-parse HEAD`
- [ ] Confirm clean working tree: `git status`
- [ ] Create working branch: `git checkout -b feat/adr001-npt014-elimination`
- [ ] Confirm Phase 1 inventory is committed and clean

### Phase 2: Rule Files (8 NPT-014 instances)

- [ ] P2-01: Upgrade `python-environment.md` line 3 (G1-003)
- [ ] P2-02: Upgrade `coding-standards.md` line 81 (G1-007)
- [ ] P2-03: Upgrade `quality-enforcement.md` line 81 (G1-011)
- [ ] P2-04: Upgrade `mandatory-skill-usage.md` line 3 (G1-014)
- [ ] P2-05: Upgrade `agent-development-standards.md` line 186 (G1-017)
- [ ] P2-06: Upgrade `agent-development-standards.md` line 187 (G1-018)
- [ ] P2-07: Upgrade `project-workflow.md` line 21 (G1-022)
- [ ] P2-08: Upgrade `agent-routing-standards.md` line 167 (G1-024)
- [ ] Self-review (H-15) on all Phase 2 changes
- [ ] Commit Phase 2 changes with descriptive message
- [ ] Verify: `grep -c "Consequence:" .context/rules/*.md` shows expected count increase

### Phase 3A: Agent Batch (28 agent files)

- [ ] Apply Template B to ps-* agents (9 files)
- [ ] Apply Template B to orch-* agents (3 files)
- [ ] Apply Template B to nse-* agents (8 files)
- [ ] Apply Template B to wt-* agents (3 files)
- [ ] Apply Template B to ts-* agents (5 files)
- [ ] Self-review (H-15) on all Phase 3A changes
- [ ] Spot-check 3 agents: invoke with test prompt, confirm expected behavior

### Phase 3B: Individual Agent Instances (3 instances)

- [ ] Upgrade ps-critic.md line 38 (G2-004)
- [ ] Upgrade orch-planner.md line 88 (G2-010 domain)
- [ ] Upgrade ts-extractor.md line 868 (G2-022 extra)
- [ ] Self-review (H-15)

### Phase 4: SKILL.md Files (4 instances)

- [ ] P4-01: Upgrade saucer-boy/SKILL.md lines 126-127 (G3-001)
- [ ] P4-02: Upgrade saucer-boy-framework-voice/SKILL.md lines 282-283 (G3-002)
- [ ] P4-03: Upgrade saucer-boy/SKILL.md line 93 (G3-003)
- [ ] Self-review (H-15)
- [ ] Commit Phase 4 changes

### Post-Implementation

- [ ] Run NPT-014 diagnostic scan on all modified files to confirm zero remaining NPT-014
- [ ] Update Phase 1 inventory with completion status
- [ ] Update ADR-001 status to ACCEPTED (requires user approval per P-020)

---

*Plan Version: 1.0.0*
*Created: 2026-02-28*
*Agent: ps-architect*
*Source: Phase 1 inventory (phase-1-npt014-inventory.md) + ADR-001 (ADR-001-npt014-elimination.md)*
*Constitutional Compliance: P-003 (no recursive subagents), P-020 (user authority -- plan is PROPOSED), P-022 (risks and exclusions documented)*

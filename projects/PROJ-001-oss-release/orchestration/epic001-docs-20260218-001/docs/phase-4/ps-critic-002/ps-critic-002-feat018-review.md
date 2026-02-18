# ps-critic-002 — FEAT-018 Fan-In Review

> **Agent ID:** ps-critic-002
> **Workflow ID:** epic001-docs-20260218-001
> **Phase:** 4 (Creator-Critic Review)
> **Date:** 2026-02-18
> **Iteration:** 1 of minimum 3 (H-14)
> **Documents Reviewed:** 4 (1 runbook + 3 playbooks)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Overall verdict |
| [Per-Document Scores](#per-document-scores) | Individual document assessments |
| [Cross-Document Consistency](#cross-document-consistency) | Inter-document checks |
| [Finding Detail](#finding-detail) | Expanded per-finding analysis |
| [Aggregate Score](#aggregate-score) | Weighted composite calculation and verdict |

---

## L0 Summary

Three of four deliverables are strong and likely meet the quality gate on targeted revision; the Transcript Playbook has one Major structural violation (navigation table incomplete — H-23/H-24) and one Minor content accuracy issue that must be resolved before the document set can be presented as PASS. The aggregate score is **0.87 (REVISE)** — below the 0.92 threshold; revision is required per H-13.

---

## Per-Document Scores

### Scoring Rubric

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

---

### DOC-1: Getting-Started Runbook

| Dimension | Raw Score (0–1) | Weighted |
|-----------|----------------|----------|
| Completeness | 0.95 | 0.190 |
| Internal Consistency | 0.95 | 0.190 |
| Methodological Rigor | 0.95 | 0.190 |
| Evidence Quality | 0.90 | 0.135 |
| Actionability | 0.97 | 0.146 |
| Traceability | 0.92 | 0.092 |
| **Composite** | | **0.943** |

**Verdict: PASS** (>= 0.92)

Strengths: Excellent adherence to the runbook template. All 5 required sections present. Navigation table covers all sections. JERRY_PROJECT setup is documented with H-04 citation. All three hook tag variants documented. Cross-platform commands (macOS/Linux and Windows PowerShell) provided throughout. Verification checklist has exactly 3 items covering the three required outcomes. Troubleshooting covers all three mandatory failure modes from REQ-943-007 plus two additional failure modes.

Weaknesses: The "Expected behavior" description in Step 4 (line 143: "you will see skill invocation output") is mildly vague — it does not tell the user what the invocation output looks like, which could cause uncertainty. Step 5's artifact discovery commands use `find` with `-newer` which may behave differently on Windows; the Windows PowerShell alternative does not filter by age, only by filename pattern — a new user could confuse pre-existing `.md` files for skill output. These are minor.

---

### DOC-2: Problem-Solving Playbook

| Dimension | Raw Score (0–1) | Weighted |
|-----------|----------------|----------|
| Completeness | 0.97 | 0.194 |
| Internal Consistency | 0.95 | 0.190 |
| Methodological Rigor | 0.97 | 0.194 |
| Evidence Quality | 0.95 | 0.143 |
| Actionability | 0.95 | 0.143 |
| Traceability | 0.95 | 0.095 |
| **Composite** | | **0.959** |

**Verdict: PASS** (>= 0.92)

Strengths: This is the strongest deliverable in the set. All 9 agents documented with roles, invocation triggers, and output locations (REQ-944-010 fully satisfied). Agent Selection Table maps all 9 keywords with disambiguation guidance for ps-analyst vs ps-investigator and ps-critic vs /adversary (beyond the minimum 8 keywords required). Creator-critic cycle documented with H-14 and H-13 citations, score dimension table, and circuit breaker behavior (REQ-944-011 fully satisfied). Four high-quality examples covering distinct agent types. The addition of extra sections beyond the template (Agent Reference, Agent Selection Table, Creator-Critic-Revision Cycle) adds genuine value and is reflected in the navigation table.

Weaknesses: The troubleshooting entry "Agent references a prior document that does not contain the expected content" (line 218) instructs users to use `Glob(pattern="docs/**/*.md")` — this is a raw tool call syntax exposed to end users, which presupposes familiarity with Claude Code's internal tool interface. A user-facing document should describe this as "ask Claude to search for files using a glob pattern" or "use the file search in Claude Code." Minor issue.

---

### DOC-3: Orchestration Playbook

| Dimension | Raw Score (0–1) | Weighted |
|-----------|----------------|----------|
| Completeness | 0.95 | 0.190 |
| Internal Consistency | 0.95 | 0.190 |
| Methodological Rigor | 0.95 | 0.190 |
| Evidence Quality | 0.93 | 0.140 |
| Actionability | 0.95 | 0.143 |
| Traceability | 0.92 | 0.092 |
| **Composite** | | **0.945** |

**Verdict: PASS** (>= 0.92)

Strengths: All three workflow patterns are documented with ASCII diagrams (REQ-944-020 fully satisfied). Core artifact table documents purpose and audience for all three artifacts (REQ-944-021 satisfied). "Do NOT use" criteria are present and cover the three conditions from SKILL.md (REQ-944-022 satisfied). P-003 compliance section is thorough, with ASCII diagram of the correct invocation hierarchy and an explicit "violation pattern to avoid" (REQ-944-023 satisfied). The 10-step step-by-step walkthrough is the most complete in the deliverable set. Three examples cover distinct patterns (new cross-pollinated, fan-out, resume).

Weaknesses: The Available Agents section at line 166 references agent specifications with paths `skills/orchestration/agents/orch-planner.md` etc., but these are not formatted as relative links — they are plain text paths. Since these are in the "Available Agents" section rather than Related Resources, the scope document's cross-reference path table does not cover them, but the practice of giving bare paths rather than links is inconsistent with how the SKILL.md is referenced in Related Resources. Minor cosmetic issue.

The quality gate evaluation step (Step 6, line 205) instructs the user to evaluate phase output "against the S-014 quality rubric before invoking orch-tracker." This implies the user knows what S-014 is; a cross-reference to the quality-enforcement.md or the /adversary skill for standalone scoring would be appropriate here. Minor usability gap.

---

### DOC-4: Transcript Playbook

| Dimension | Raw Score (0–1) | Weighted |
|-----------|----------------|----------|
| Completeness | 0.87 | 0.174 |
| Internal Consistency | 0.82 | 0.164 |
| Methodological Rigor | 0.88 | 0.176 |
| Evidence Quality | 0.92 | 0.138 |
| Actionability | 0.92 | 0.138 |
| Traceability | 0.80 | 0.080 |
| **Composite** | | **0.870** |

**Verdict: REVISE** (0.85 – 0.91)

This document has the most issues. The navigation table does not cover all ## headings (H-23/H-24 violation — Major finding). The quality threshold stated (0.90) is accurate per SKILL.md but contradicts the user's mental model established by the quality-enforcement.md SSOT (0.92) without explanation (Minor finding). The troubleshooting section references "the Domain Contexts section below" (line 207) but that section is not in the navigation table, making it harder to navigate to.

Strengths: Two-phase workflow is clearly explained with the mandatory CLI syntax documented (REQ-944-030 satisfied). All three input formats documented with command syntax for each (REQ-944-031 satisfied). All 9 domain contexts documented with descriptions (REQ-944-032 satisfied). canonical-transcript.json warning is prominent and clearly states NEVER (REQ-944-033 satisfied). Four examples covering VTT default, domain context, SRT without mindmap, and user research are high quality.

---

## Cross-Document Consistency

### Terminology Consistency

| Term | DOC-1 | DOC-2 | DOC-3 | DOC-4 | Verdict |
|------|-------|-------|-------|-------|---------|
| "JERRY_PROJECT" | ✓ | ✓ | ✓ | ✓ | Consistent |
| "H-04" | ✓ (cited) | ✓ (cited) | ✓ (cited) | ✓ (cited) | Consistent |
| "jerry session start" | ✓ | ✓ (implied) | ✓ (implied) | ✓ (implied) | Consistent |
| Quality threshold | 0.92 (implicit) | 0.92 (H-13 cited) | 0.92 (H-13 cited) | **0.90** (Phase 5) | **INCONSISTENT** — see F-004 |
| creator-critic cycle | Referenced in Next Steps | Fully documented | Referenced in Step 6 | Not referenced (transcript uses own cycle) | Acceptable by design |
| "uv run" | Not applicable | Not applicable | Not applicable | ✓ (required, H-05 cited) | Consistent where applicable |

### Cross-Reference Bidirectionality

The scope document requires bidirectional cross-references between playbooks:

| Link | Source Playbook | Target Mentioned | Target Reciprocates | Status |
|------|----------------|-----------------|---------------------|--------|
| problem-solving -> orchestration | Lines 227-228 | ✓ | ✓ (orchestration.md line 257) | Bidirectional |
| problem-solving -> transcript | Line 229 | ✓ | ✓ (transcript.md line 270) | Bidirectional |
| orchestration -> problem-solving | Line 257 | ✓ | ✓ (problem-solving.md line 227) | Bidirectional |
| orchestration -> transcript | Line 258 | ✓ | ✓ (transcript.md line 272) | Bidirectional |
| transcript -> problem-solving | Line 269 | ✓ | ✓ (problem-solving.md line 229) | Bidirectional |
| transcript -> orchestration | Line 272 | ✓ | ✓ (orchestration.md line 258) | Bidirectional |
| runbook -> all three playbooks | Lines 202-204 | ✓ | N/A (runbook is not cross-referenced by playbooks — by design) | Expected — playbooks do not reference the runbook |

All bidirectional cross-references are present and correct.

### Relative Path Correctness

Cross-reference paths verified against the scope document's ratified cross-reference path table:

| Document | Stated Path | Correct Path (from scope) | Status |
|----------|------------|--------------------------|--------|
| `docs/playbooks/problem-solving.md` -> SKILL.md | `../../skills/problem-solving/SKILL.md` | `../../skills/problem-solving/SKILL.md` | Correct |
| `docs/playbooks/problem-solving.md` -> orchestration | `./orchestration.md` | `./orchestration.md` | Correct |
| `docs/playbooks/problem-solving.md` -> transcript | `./transcript.md` | `./transcript.md` | Correct |
| `docs/playbooks/orchestration.md` -> SKILL.md | `../../skills/orchestration/SKILL.md` | `../../skills/orchestration/SKILL.md` | Correct |
| `docs/playbooks/orchestration.md` -> problem-solving | `./problem-solving.md` | `./problem-solving.md` | Correct |
| `docs/playbooks/orchestration.md` -> transcript | `./transcript.md` | `./transcript.md` | Correct |
| `docs/playbooks/transcript.md` -> SKILL.md | `../../skills/transcript/SKILL.md` | `../../skills/transcript/SKILL.md` | Correct |
| `docs/playbooks/transcript.md` -> problem-solving | `./problem-solving.md` | `./problem-solving.md` | Correct |
| `docs/playbooks/transcript.md` -> orchestration | `./orchestration.md` | `./orchestration.md` | Correct |
| `docs/runbooks/getting-started.md` -> INSTALLATION.md | `../INSTALLATION.md` | `../INSTALLATION.md` | Correct |
| `docs/runbooks/getting-started.md` -> problem-solving | `../playbooks/problem-solving.md` | `../playbooks/problem-solving.md` | Correct |
| `docs/runbooks/getting-started.md` -> orchestration | `../playbooks/orchestration.md` | `../playbooks/orchestration.md` | Correct |
| `docs/runbooks/getting-started.md` -> transcript | `../playbooks/transcript.md` | `../playbooks/transcript.md` | Correct |
| `docs/playbooks/problem-solving.md` -> quality-enforcement | `../../.context/rules/quality-enforcement.md` | `../../.context/rules/quality-enforcement.md` | Correct |

All 14 cross-reference paths are correct.

### Formatting Consistency

| Element | DOC-1 | DOC-2 | DOC-3 | DOC-4 | Verdict |
|---------|-------|-------|-------|-------|---------|
| Navigation table format | ✓ | ✓ | ✓ | ✓ (incomplete) | Inconsistent — see F-001 |
| Example format (User request / System behavior) | N/A | ✓ | ✓ | ✓ | Consistent |
| Troubleshooting table (Symptom / Cause / Resolution) | ✓ | ✓ | ✓ | ✓ | Consistent |
| Code blocks for commands | ✓ | ✓ | ✓ | ✓ | Consistent |
| H-04 citation in Prerequisites | ✓ | ✓ | ✓ | ✓ | Consistent |
| Related Resources section title | N/A | ✓ | ✓ | ✓ | Consistent |

---

## Finding Detail

### F-001 — Transcript Playbook: Navigation Table Incomplete (Major)

**Severity:** Major — blocks PASS (H-23 violation)

**Location:** `docs/playbooks/transcript.md`, lines 8–17 (navigation table)

**Evidence:**

The navigation table lists 6 sections:
```
| [When to Use](#when-to-use) | Activation criteria and exclusions |
| [Prerequisites](#prerequisites) | What must be in place before invoking |
| [Step-by-Step](#step-by-step) | Primary invocation path |
| [Examples](#examples) | Concrete invocation examples |
| [Troubleshooting](#troubleshooting) | Common failure modes |
| [Related Resources](#related-resources) | Cross-references to other playbooks and SKILL.md |
```

However, the document contains 8 `##` headings. Two sections are absent from the navigation table:
- `## Domain Contexts` (line 212) — covers all 9 supported domain contexts (REQ-944-032 content)
- `## Input Formats` (line 239) — covers VTT, SRT, plain text with command examples (REQ-944-031 content)

H-23 (NAV-001) requires: "All Claude-consumed markdown files over 30 lines MUST include a navigation table." H-24 (NAV-006) requires that navigation table section names use anchor links. By not listing Domain Contexts and Input Formats, the navigation table fails to satisfy NAV-004 ("All major sections (`##` headings) SHOULD be listed") — but the HARD rule NAV-001 requires the table to serve its navigation purpose, which it cannot if two content-bearing sections are omitted.

**Collateral impact:** The troubleshooting entry "Domain-specific entities are missing from the output" (line 207) includes the inline note "See the domain table in the Domain Contexts section below." This reference is not navigable via the navigation table, reducing the troubleshooting entry's actionability.

**Suggested fix:**

Add two entries to the navigation table between Troubleshooting and Related Resources:

```markdown
| [Domain Contexts](#domain-contexts) | The 9 supported domain contexts with selection guidance |
| [Input Formats](#input-formats) | VTT, SRT, and plain text format handling |
```

---

### F-002 — Problem-Solving Playbook: Internal Tool Syntax Exposed to End Users (Minor)

**Severity:** Minor — informational, does not block PASS

**Location:** `docs/playbooks/problem-solving.md`, line 218 (Troubleshooting table)

**Evidence:**

The troubleshooting entry for "Agent references a prior document that does not contain the expected content" instructs:
> "Use `Glob(pattern="docs/**/*.md")` to verify the actual paths of prior artifacts..."

`Glob(pattern="docs/**/*.md")` is the raw Claude Code MCP tool call syntax. End users of the problem-solving playbook are not expected to be familiar with MCP tool call syntax. Exposing this syntax in a user-facing playbook:
1. Creates confusion for users who don't know what `Glob(...)` means
2. May become stale if the tool interface changes
3. Is inconsistent with how all other troubleshooting entries describe user actions (in natural language)

**Suggested fix:**

Replace:
> "Use `Glob(pattern="docs/**/*.md")` to verify the actual paths of prior artifacts, then re-invoke the agent with the correct file path."

With:
> "Ask Claude to search for all markdown files under `docs/` (e.g., 'find all .md files in docs/'), then re-invoke the agent with the correct file path."

---

### F-003 — Orchestration Playbook: Agent Spec Paths Not Linked (Minor)

**Severity:** Minor — informational, does not block PASS

**Location:** `docs/playbooks/orchestration.md`, line 166 (Available Agents section)

**Evidence:**

The Available Agents section ends with:
> "Agent specifications: `skills/orchestration/agents/orch-planner.md`, `skills/orchestration/agents/orch-tracker.md`, `skills/orchestration/agents/orch-synthesizer.md`."

These are unlinked plain-text paths. The scope document cross-reference table does not mandate links to agent specification files (it only mandates SKILL.md and playbook cross-references), but within the document, the SKILL.md is formatted as a proper markdown link in Related Resources (`[SKILL.md](../../skills/orchestration/SKILL.md)`) while agent spec paths are bare strings. This is an internal formatting inconsistency.

**Suggested fix:**

Convert to relative markdown links from `docs/playbooks/orchestration.md`:
```markdown
Agent specifications: [`orch-planner.md`](../../skills/orchestration/agents/orch-planner.md),
[`orch-tracker.md`](../../skills/orchestration/agents/orch-tracker.md),
[`orch-synthesizer.md`](../../skills/orchestration/agents/orch-synthesizer.md).
```

---

### F-004 — Transcript Playbook: Quality Threshold 0.90 Not Reconciled with Quality Gate SSOT (Minor)

**Severity:** Minor — informational, does not block PASS

**Location:** `docs/playbooks/transcript.md`, line 127 (Step-by-Step, Phase 5 description)

**Evidence:**

Line 127 states:
> "Phase 5 — ps-critic runs — validates quality against the >= 0.90 threshold."

The quality-enforcement.md SSOT (H-13) states the quality threshold as **>= 0.92** for C2+ deliverables. The transcript SKILL.md uses **0.90** as its intentional threshold with a design rationale section explaining why (transcript output is scored by different criteria than general deliverables).

A user who has read the quality-enforcement.md SSOT (0.92) and then reads the transcript playbook (0.90) will encounter an apparent discrepancy with no explanation. The playbook accurately reflects the SKILL.md, but without acknowledging the discrepancy, users may be confused or distrust the documentation.

**Suggested fix:**

Add a parenthetical note to the Phase 5 step:
> "Phase 5 — ps-critic runs — validates quality against the >= 0.90 threshold (transcript uses a skill-specific threshold; see SKILL.md Design Rationale section for the selection rationale)."

Or alternatively, add a note in the Prerequisites section or at the top of Step-by-Step explaining that the transcript skill uses a 0.90 threshold by documented design.

---

### F-005 — Runbook: Step 4 Expected Behavior Underspecified (Minor)

**Severity:** Minor — informational, does not block PASS

**Location:** `docs/runbooks/getting-started.md`, lines 143–147 (Step 4: Invoke the Problem-Solving Skill)

**Evidence:**

The expected behavior description states:
> "Claude responds by activating the problem-solving skill (you will see skill invocation output)"

This is vague for a first-time user. A user who has never seen skill invocation output does not know what to look for. The problem-solving playbook describes skill invocation output in detail (which agent was selected, where the artifact is saved), but the runbook does not cross-reference this or give even a brief example of what "invocation output" looks like.

**Suggested fix:**

Replace the parenthetical with a brief concrete description:
> "Claude responds by activating the problem-solving skill (you will see a message indicating which agent was selected and where its output will be saved, for example: 'Invoking ps-researcher...' followed by artifact creation at `projects/PROJ-001-my-first-project/docs/research/...`)."

---

### F-006 — Runbook: Step 5 Windows PowerShell Command Does Not Filter by Artifact Age (Minor)

**Severity:** Minor — informational, does not block PASS

**Location:** `docs/runbooks/getting-started.md`, lines 164–170 (Step 5: Verify the Output Artifact)

**Evidence:**

The macOS/Linux verification command:
```bash
find projects/PROJ-001-my-first-project -name "*.md" -newer projects/PROJ-001-my-first-project/PLAN.md
```
filters to files newer than `PLAN.md`, correctly isolating artifacts created by the skill invocation.

The Windows PowerShell alternative:
```
Get-ChildItem -Recurse projects\PROJ-001-my-first-project\ -Filter "*.md"
```
returns ALL `.md` files recursively, including `PLAN.md` and `WORKTRACKER.md` which were created in Step 1. A new Windows user following this step will see `PLAN.md` and `WORKTRACKER.md` in the output and may believe these are the "output artifact" the skill produced.

**Suggested fix:**

Use PowerShell's `Where-Object` to filter by creation time after the skill invocation:
```powershell
$since = (Get-Item "projects\PROJ-001-my-first-project\PLAN.md").LastWriteTime
Get-ChildItem -Recurse projects\PROJ-001-my-first-project\ -Filter "*.md" | Where-Object { $_.LastWriteTime -gt $since }
```
Or add an instructional note: "Note: `PLAN.md` and `WORKTRACKER.md` are pre-existing files; the new artifact will be in a subdirectory such as `docs\research\` or `docs\analysis\`."

---

## Aggregate Score

### Per-Document Composite Summary

| Document | Composite Score | Verdict |
|----------|----------------|---------|
| DOC-1: Getting-Started Runbook | **0.943** | PASS |
| DOC-2: Problem-Solving Playbook | **0.959** | PASS |
| DOC-3: Orchestration Playbook | **0.945** | PASS |
| DOC-4: Transcript Playbook | **0.870** | REVISE |

### Aggregate Calculation

Per the review instructions: **the aggregate score is the MINIMUM of the 4 individual scores (weakest link).**

**Aggregate Score: 0.870 (minimum = Transcript Playbook)**

### Finding Impact Summary

| Finding | Severity | Blocks PASS | Document |
|---------|---------|-------------|----------|
| F-001: Transcript nav table incomplete (H-23 violation) | Major | Yes | DOC-4 |
| F-002: Internal tool syntax in user-facing playbook | Minor | No | DOC-2 |
| F-003: Agent spec paths not linked | Minor | No | DOC-3 |
| F-004: Quality threshold 0.90 not reconciled with SSOT | Minor | No | DOC-4 |
| F-005: Step 4 expected behavior underspecified | Minor | No | DOC-1 |
| F-006: Windows PowerShell command does not filter by age | Minor | No | DOC-1 |

**Major findings:** 1 (F-001 — Transcript Playbook)
**Minor findings:** 5 (F-002 through F-006)

### Verdict

**REVISE** — Aggregate score 0.870 is below the 0.92 threshold (H-13).

The revision required is targeted: DOC-4 (Transcript Playbook) has one Major finding (F-001) that is a two-line fix to the navigation table. Once F-001 is resolved, DOC-4's composite score should reach approximately 0.92–0.94. After targeted revision, the aggregate score should clear the 0.92 threshold and the document set should be presented for Iteration 2 review.

Minor findings F-002 through F-006 are recommended for resolution in the same iteration but do not individually prevent a PASS verdict.

**Minimum iterations remaining per H-14:** 2 more (this is iteration 1 of minimum 3).

---

*Agent: ps-critic-002*
*Workflow: epic001-docs-20260218-001*
*Phase: 4*
*Output: `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-4/ps-critic-002/ps-critic-002-feat018-review.md`*

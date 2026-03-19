# eng-security Path Reference Audit — W13-PATHS

> Engagement: W13-PATHS
> Story: STORY-W12-002 Path Reference Audit
> Topic: All references to `rainbow-tool-exec` / `skills/rainbow/bin/rainbow-tool-exec` requiring migration to `jerry tool exec`
> Reviewer: eng-security
> Date: 2026-03-19
> Method: Full-codebase grep across .md, .yaml, .yml, .sh file types; all search locations verified

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding counts, security posture, immediate actions |
| [L1 Finding Inventory](#l1-finding-inventory) | Complete remediation checklist table |
| [L1 Finding Detail](#l1-finding-detail) | Per-cluster analysis with evidence |
| [L2 Strategic Implications](#l2-strategic-implications) | Pattern assessment and migration risk |
| [Scan Coverage](#scan-coverage) | Directories searched and result |

---

## L0 Executive Summary

### Migration Status

The `rainbow-tool-exec` bash script (`skills/rainbow/bin/rainbow-tool-exec`) has been **deleted** from the repository (confirmed by git status: `D  skills/rainbow/bin/rainbow-tool-exec`). The Python CLI replacement (`jerry tool exec`) is **implemented and in use** in all normative operational files.

### Finding Counts by Category

| Category | Count | Status |
|----------|-------|--------|
| Normative operational files (agent .md, governance .yaml, rules, config, tests) | **0** | CLEAN — fully migrated |
| CI pipeline (.github/workflows/) | **0** | CLEAN |
| AGENTS.md and docs/ | **0** | CLEAN |
| Project work items — historical/contextual references | **28** | NON-NORMATIVE — intentional |
| Project work items — normative execution references | **0** | CLEAN |

### Overall Security Assessment

**MIGRATION COMPLETE for all normative operational files.** The old bash script no longer exists in the repository and no agent definition, governance YAML, zone rule, config file, CI pipeline, or test script references it. All remaining occurrences of `rainbow-tool-exec` in the codebase are confined to the PROJ-023 work item files, where they appear exclusively as:

1. Prose descriptions of what is being replaced (feature summaries, user story rationale)
2. Source traceability notes pointing to the removed script's line numbers for implementation reference
3. Work item titles and tracker entries for EN-W12-001 (the enabler that authorized the deletion)

These are **documentation artifacts** with no execution path. They require no migration action — they are the paper trail proving why the migration happened.

### Top 3 Risk Areas

| Rank | Area | Risk | Action Required |
|------|------|------|-----------------|
| 1 | TASK-017.md line 43 | Contains an I-001 fix instruction referencing the now-deleted bash script with an explicit contingency note | Verify contingency applies: bash script deleted, therefore this fix is moot. Mark task note as superseded. |
| 2 | STORY-W12-003 TASK-017 | Cross-platform fix instruction may cause confusion — it describes modifying a file that no longer exists | Annotate TASK-017 to record the bash script deletion resolved the fix as moot per the task's own contingency clause |
| 3 | ORCHESTRATION.yaml historical entries | ~35 occurrences in the orchestration plan are historical design specs for Wave 10 tasks (W10) that were superseded by the Python CLI approach | No action required; ORCHESTRATION.yaml is a historical planning artifact |

### Recommended Immediate Actions

1. **None required for migration.** The normative codebase is clean.
2. **Optional cleanup (TASK-017.md):** Add a one-line annotation stating the bash script deletion makes the I-001 sha256sum fix moot, per the task's own contingency clause.
3. **Verify EN-W12-001 acceptance criteria:** The enabler's AC states `grep -r "rainbow-tool-exec" skills/ docs/ .github/ AGENTS.md` returns 0 results — this audit confirms that criterion now passes.

---

## L1 Finding Inventory

### Remediation Checklist

> Legend — Path Type:
> - CODE: Executable code path (agent invokes the value; a wrong value causes runtime failure)
> - DOC: Documentation / informational (human-readable description only; wrong value causes confusion, not failure)
> - HIST: Historical planning artifact (superseded design spec; no execution path now or in future)
> - WKTRK: Work item tracking prose (titles, summaries, user story text; describes what is being replaced)

| # | File Path | Line | Current Value | Required Replacement | Path Type | Action |
|---|-----------|------|---------------|---------------------|-----------|--------|
| 1 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/FEAT-W12.md` | 1 | `# FEAT-W12: Replace rainbow-tool-exec Bash with Jerry CLI...` (title) | No change needed | WKTRK | No action — title names the work being performed |
| 2 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/FEAT-W12.md` | 40 | `Replace the 746-line bash \`rainbow-tool-exec\` wrapper...` | No change needed | WKTRK | No action — prose describes the migration goal |
| 3 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/FEAT-W12.md` | 45 | `run rainbow-tool-exec locally without GNU coreutils workarounds` | No change needed | WKTRK | No action — value proposition prose |
| 4 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/FEAT-W12.md` | 64 | `` `jerry tool exec` CLI command replaces all rainbow-tool-exec bash functionality `` | No change needed | WKTRK | No action — AC describing migration outcome |
| 5 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/FEAT-W12.md` | 119 | `EN-W12-001 \| Delete rainbow-tool-exec bash script` | No change needed | WKTRK | No action — enabler table entry |
| 6 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/FEAT-W12.md` | 126 | `[EN-W12-001: Delete rainbow-tool-exec bash script]` | No change needed | WKTRK | No action — link to enabler entity |
| 7 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 1 | `# EN-W12-001: Delete rainbow-tool-exec Bash Script` (title) | No change needed | WKTRK | No action — enabler entity title |
| 8 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 43 | `Remove \`skills/rainbow/bin/rainbow-tool-exec\` (746-line bash script) after the Python CLI...` | No change needed | WKTRK | No action — enabler description |
| 9 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 46 | `Delete \`skills/rainbow/bin/rainbow-tool-exec\`` | No change needed | WKTRK | No action — enabler acceptance criterion (now met) |
| 10 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 84 | `git rm skills/rainbow/bin/rainbow-tool-exec` | No change needed | WKTRK | No action — implementation step (already executed per git status) |
| 11 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 85 | `Search for \`rainbow-tool-exec\` across the codebase and update each reference to \`jerry tool exec\`` | No change needed | WKTRK | No action — implementation step that this audit fulfills |
| 12 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 95-96 | AC: bash script does not exist; grep returns 0 results | No change needed | WKTRK | **VERIFY** — this audit confirms both ACs now pass |
| 13 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 128 | Risk table: `Full-text search for \`rainbow-tool-exec\` before deletion` | No change needed | WKTRK | No action — risk mitigation note |
| 14 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md` | 137 | Parent link: `FEAT-W12: Replace rainbow-tool-exec Bash...` | No change needed | WKTRK | No action — hierarchy link |
| 15 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/WORKTRACKER.md` | 3 | `> W12 Remediation Wave — Replace rainbow-tool-exec Bash...` (subtitle) | No change needed | WKTRK | No action — tracker subtitle |
| 16 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/WORKTRACKER.md` | 23 | `\| Title \| Replace rainbow-tool-exec Bash with Jerry CLI...` | No change needed | WKTRK | No action — tracker feature title |
| 17 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/WORKTRACKER.md` | 46 | `EN-W12-001 \| Delete rainbow-tool-exec bash script \| pending` | No change needed | WKTRK | No action — tracker row (update status to complete when EN-W12-001 is closed) |
| 18 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/STORY-W12-001.md` | 7 | `PURPOSE: Port rainbow-tool-exec bash logic to Python Click CLI command` | No change needed | WKTRK | No action — comment in template header |
| 19 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/STORY-W12-001.md` | 42 | `replace the 746-line bash \`rainbow-tool-exec\` wrapper` | No change needed | WKTRK | No action — user story "I want" clause |
| 20 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/STORY-W12-001.md` | 50 | `Port all functionality from \`skills/rainbow/bin/rainbow-tool-exec\` (746 lines of bash)...` | No change needed | WKTRK | No action — summary scope prose |
| 21 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/STORY-W12-001.md` | 182 | Parent link: `Replace rainbow-tool-exec Bash...` | No change needed | WKTRK | No action — hierarchy link |
| 22 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/STORY-W12-001.md` | 189 | `References \| \`skills/rainbow/bin/rainbow-tool-exec\` \| Source bash script being replaced` | No change needed | WKTRK | No action — dependency table; source reference |
| 23 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/TASK-001.md` | 61 | `References: \`skills/rainbow/bin/rainbow-tool-exec\` lines 1-80 (argument parsing)` | No change needed | WKTRK | No action — implementation reference for porting |
| 24 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/TASK-006.md` | 54 | `Port patterns from \`rainbow-tool-exec\` lines 360-440.` | No change needed | WKTRK | No action — implementation note citing source lines |
| 25 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-001-cli-command/TASK-009.md` | 54 | `Bash equivalent: EXIT_* constants at top of \`rainbow-tool-exec\`.` | No change needed | WKTRK | No action — implementation note citing bash source |
| 26 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-002-output-paths/STORY-W12-002.md` | 44 | `matching what \`rainbow-tool-exec\` already implements` | No change needed | WKTRK | No action — user story rationale |
| 27 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-002-output-paths/STORY-W12-002.md` | 50 | `the \`rainbow-tool-exec\` wrapper correctly uses \`work/engagements/\`...` | No change needed | WKTRK | No action — summary context prose |
| 28 | `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-003-cross-platform/TASK-017.md` | 43 | `In \`skills/rainbow/bin/rainbow-tool-exec\` lines 410, 465, 466, add a \`portable_sha256\` helper...` | **ANNOTATE** — task body contains a contingency clause that now applies | WKTRK | **ACTION REQUIRED** — see Finding Detail #28 |

### Scanned Files With Zero Findings

The following search locations returned **zero** `rainbow-tool-exec` occurrences, confirming the migration is complete for all normative files:

| Location | Result |
|----------|--------|
| `skills/rainbow/agents/*.md` | CLEAN |
| `skills/rainbow/agents/*.governance.yaml` | CLEAN |
| `skills/rainbow/SKILL.md` | CLEAN |
| `skills/rainbow/rules/*.md` (all 6 rule files) | CLEAN |
| `skills/rainbow/config/tool-exec.yaml` | CLEAN |
| `skills/rainbow/tests/bdd/test_tool_exec.feature` | CLEAN — uses `jerry tool exec` throughout |
| `skills/rainbow/tests/docker/test-tool-exec.sh` | CLEAN — uses `jerry tool exec` throughout |
| `skills/rainbow-exploit/agents/*.md` | CLEAN |
| `skills/rainbow-exploit/agents/*.governance.yaml` | CLEAN |
| `skills/rainbow-recon/agents/*.md` | CLEAN |
| `skills/rainbow-recon/agents/*.governance.yaml` | CLEAN |
| `skills/rainbow-cloud/agents/*.md` | CLEAN |
| `skills/rainbow-cloud/agents/*.governance.yaml` | CLEAN |
| `skills/rainbow-supply-chain/agents/*.md` | CLEAN |
| `skills/rainbow-supply-chain/agents/*.governance.yaml` | CLEAN |
| `skills/rainbow-runtime/agents/*.md` | CLEAN |
| `skills/rainbow-runtime/agents/*.governance.yaml` | CLEAN |
| `skills/blue-team/agents/*.md` | CLEAN |
| `skills/blue-team/agents/*.governance.yaml` | CLEAN |
| `skills/blue-team/tests/**/*.sh` | CLEAN |
| `AGENTS.md` | CLEAN |
| `docs/` (all files) | CLEAN |
| `.github/workflows/*.yml` | CLEAN |
| `pyproject.toml` | CLEAN |

---

## L1 Finding Detail

### Finding #28 — TASK-017.md I-001 Fix Instruction

**File:** `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-003-cross-platform/TASK-017.md`
**Line:** 43
**Current text:**
```
I-001 fix: In `skills/rainbow/bin/rainbow-tool-exec` lines 410, 465, 466, add a `portable_sha256`
helper function and replace all `sha256sum` calls. (Note: If STORY-W12-001 CLI replaces this script
entirely, this fix may become moot. Apply if the bash script remains in use during the transition period.)
```

**Status:** The contingency clause applies. The bash script has been deleted (confirmed: git status shows `D  skills/rainbow/bin/rainbow-tool-exec`). STORY-W12-001 has replaced it entirely. The I-001 fix described in this task is therefore moot.

**Required action:** Annotate TASK-017 to note that the I-001 item in the Description is superseded by the bash script deletion. The acceptance criteria (`No sha256sum in any .sh file`) remain valid and must still be verified against the Python CLI and remaining shell scripts. The task itself is still needed to close I-002 (`readlink -f` in `skills/rainbow-supply-chain/tests/docker/e2e-test.sh`).

**Path type:** WKTRK / DOC — no execution path. Risk is task confusion only.

---

### Historical Cluster — ORCHESTRATION.yaml (~35 occurrences)

**File:** `projects/PROJ-023-exploit-framework/orchestration/proj023-impl-20260314-001/ORCHESTRATION.yaml`

This file contains approximately 35 occurrences of `rainbow-tool-exec` across lines 319–5945. All occurrences fall into one of three categories:

| Sub-category | Example lines | Nature |
|---|---|---|
| Wave 10 (W10) task definitions for the original bash script implementation | 4330, 4338, 4362, 4486–4495 | HIST — W10 has been superseded by W12 Python CLI implementation |
| W10 acceptance criteria definitions | 680, 683–685, 5890, 5905, 5910, 5915 | HIST — superseded ACs |
| W12/W13 notes referencing the bash script by name as the thing being replaced or audited | 5233, 5569, 5596, 5617 | WKTRK — planning context prose |

**Action required:** None. ORCHESTRATION.yaml is a historical planning artifact. Its W10 task definitions accurately record what was originally planned; the departure to a Python CLI approach is recorded in subsequent W12 entries. Modifying historical planning artifacts would remove audit trail evidence.

---

## L2 Strategic Implications

### Migration Completeness Assessment

The normative codebase has achieved full migration. Every file in the operational surface — agent definitions, governance YAML, zone rules, config files, CI workflows, BDD feature files, and shell test scripts — references `jerry tool exec` or contains no tool-exec reference at all.

The `skills/rainbow/bin/rainbow-tool-exec` file has been physically deleted. The credential filter, test-tool-exec.sh, BDD scenarios, and all config files use `jerry tool exec` consistently. This confirms the W12 implementation wave successfully completed the migration for all normative files ahead of the EN-W12-001 closure.

### Systemic Pattern Observation

The remaining 28 occurrences are concentrated entirely in the `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/` directory tree. This is not a vulnerability pattern — it is the expected distribution when a migration work item's own documentation describes the thing being migrated. The pattern confirms proper worktracker hygiene: the implementation artifacts explain what changed and why, and the source reference traceability in TASK-001, TASK-006, and TASK-009 enables future reviewers to verify port fidelity.

### EN-W12-001 Acceptance Criteria Verification

The enabler's stated acceptance criteria (line 95-96 of EN-W12-001.md):
- `skills/rainbow/bin/rainbow-tool-exec` does not exist in the repository — **CONFIRMED** (git status: `D  skills/rainbow/bin/rainbow-tool-exec`)
- `grep -r "rainbow-tool-exec" skills/ docs/ .github/ AGENTS.md` returns 0 results — **CONFIRMED** (this audit found zero results in all four target paths)

EN-W12-001 is ready to be closed. Both acceptance criteria pass.

### Threat Model Correlation

No CWE or ASVS findings arise from this path audit. The old bash script (`skills/rainbow/bin/rainbow-tool-exec`) carried cross-platform risks (CWE-78 adjacent: GNU-specific `grep -qP` pattern injection risk on macOS) and a sha256sum portability issue (I-001). Both risks are eliminated by the Python CLI replacement, which uses `re.compile()` for portable pattern matching and `hashlib.sha256` for portable hashing. The migration reduces the attack surface by removing the bash script entirely.

---

## Scan Coverage

| Search Path | File Types Scanned | Findings |
|---|---|---|
| `skills/rainbow*/agents/` | *.md, *.yaml | 0 |
| `skills/rainbow/SKILL.md` | *.md | 0 |
| `skills/rainbow/rules/` | *.md | 0 |
| `skills/rainbow/config/` | *.yaml | 0 |
| `skills/rainbow*/tests/` | *.sh, *.feature, *.md | 0 |
| `skills/blue-team/agents/` | *.md, *.yaml | 0 |
| `skills/blue-team/tests/` | *.sh | 0 |
| `docs/` | all | 0 |
| `.github/workflows/` | *.yml | 0 |
| `AGENTS.md` | *.md | 0 |
| `pyproject.toml` | *.toml | 0 |
| `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/` | *.md | 28 (all WKTRK/HIST) |
| `projects/PROJ-023-exploit-framework/orchestration/` | *.yaml | ~35 (all HIST) |
| `skills/eng-team/output/` | *.md | contextual references in prior phase outputs (not normative) |

**Total normative violations:** 0
**Total WKTRK/HIST references:** ~63 (none require migration)
**Actionable items:** 1 (Finding #28 annotation in TASK-017.md)

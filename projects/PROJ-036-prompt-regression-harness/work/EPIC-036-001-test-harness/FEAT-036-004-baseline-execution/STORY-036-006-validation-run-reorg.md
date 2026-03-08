# STORY-036-006: Reorganize Validation Run Directory by Layer

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-07T00:00:00Z
> **Due:** —
> **Completed:** 2026-03-07T00:00:00Z
> **Parent:** FEAT-036-004
> **Owner:** —
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a/I want/So that |
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes |
| [Implementation Plan](#implementation-plan) | Detailed steps |
| [Progress Summary](#progress-summary) | Completion metrics |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** framework maintainer

**I want** the validation-run directory organized by layer (agent-outputs, layer2-geval, layer3-metamorphic, layer4-statistical, scripts)

**So that** the four-layer architecture is immediately visible in the file structure and each layer's inputs/outputs are self-contained

---

## Summary

Reorganize the flat 29-file `validation-run/` directory into layer-aligned subdirectories. Currently all scripts, agent outputs, G-Eval scores, MR results, and statistical comparison results are mixed in a single directory with inconsistent naming (some prefixed `layer2-`, `layer3-`, `layer4-`, others prefixed `phase2-`, `phase3-`, `phase4-`). The reorganization creates clear boundaries matching the Four-Layer Composite architecture from ADR-001.

**Scope:**
- Create 4 layer subdirectories + 1 scripts subdirectory
- Move files to appropriate subdirectories using `git mv`
- Update internal path references in 3 Python scripts (`VALIDATION_DIR`, output paths)
- Update `execution-prompt-v1.md` usage instructions
- Simplify filenames by removing redundant layer/phase prefixes within subdirectories

---

## Acceptance Criteria

- [x] Agent output files are in `validation-run/agent-outputs/`
- [x] G-Eval scoring results and composites are in `validation-run/layer2-geval/`
- [x] MR test results and costs are in `validation-run/layer3-metamorphic/`
- [x] Statistical comparison results are in `validation-run/layer4-statistical/`
- [x] Execution scripts are in `validation-run/scripts/`
- [x] All 3 Python scripts run successfully from new locations (`uv run python ...`)
- [x] `execution-prompt-v1.md` updated with new paths
- [x] Git history preserved via `git mv` (not delete + create)

---

## Implementation Plan

### Current → Proposed File Mapping

```
CURRENT                              → PROPOSED
validation-run/                      → validation-run/
├── phase2_score.py                  → scripts/phase2_score.py
├── phase3_mr_smoke.py               → scripts/phase3_mr_smoke.py
├── phase4_stats.py                  → scripts/phase4_stats.py
├── check_imports.py                 → scripts/check_imports.py
├── ps-researcher-output.md          → agent-outputs/ps-researcher.md
├── ps-analyst-output.md             → agent-outputs/ps-analyst.md
├── ps-architect-output.md           → agent-outputs/ps-architect.md
├── ps-critic-output.md              → agent-outputs/ps-critic.md
├── adv-scorer-output.md             → agent-outputs/adv-scorer.md
├── phase2-composites.json           → layer2-geval/composites.json
├── layer2-scores-ps-researcher.md   → layer2-geval/ps-researcher.md
├── layer2-scores-ps-analyst.md      → layer2-geval/ps-analyst.md
├── layer2-scores-ps-architect.md    → layer2-geval/ps-architect.md
├── layer2-scores-ps-critic.md       → layer2-geval/ps-critic.md
├── layer2-scores-adv-scorer.md      → layer2-geval/adv-scorer.md
├── layer3-mr-results.md             → layer3-metamorphic/mr-results.md
├── phase3-costs.json                → layer3-metamorphic/costs.json
├── layer4-results.md                → layer4-statistical/results.md
├── phase4-results.json              → layer4-statistical/results.json
├── layer4-ps-researcher.json        → layer4-statistical/ps-researcher.json
├── layer4-ps-researcher.md          → layer4-statistical/ps-researcher.md
├── layer4-ps-analyst.json           → layer4-statistical/ps-analyst.json
├── layer4-ps-analyst.md             → layer4-statistical/ps-analyst.md
├── layer4-ps-architect.json         → layer4-statistical/ps-architect.json
├── layer4-ps-architect.md           → layer4-statistical/ps-architect.md
├── layer4-ps-critic.json            → layer4-statistical/ps-critic.json
├── layer4-ps-critic.md              → layer4-statistical/ps-critic.md
├── layer4-adv-scorer.json           → layer4-statistical/adv-scorer.json
└── layer4-adv-scorer.md             → layer4-statistical/adv-scorer.md
```

### Script Path Updates Required

| Script | Current Reference | New Reference |
|--------|-------------------|---------------|
| `phase2_score.py` | `VALIDATION_DIR = Path(__file__).parent` | `VALIDATION_DIR = Path(__file__).resolve().parent.parent` |
| `phase2_score.py` | Output: `VALIDATION_DIR / f"layer2-scores-{agent_id}.md"` | Output: `VALIDATION_DIR / "layer2-geval" / f"{agent_id}.md"` |
| `phase2_score.py` | Output: `VALIDATION_DIR / "phase2-composites.json"` | Output: `VALIDATION_DIR / "layer2-geval" / "composites.json"` |
| `phase2_score.py` | Input: `VALIDATION_DIR / f"{agent_id}-output.md"` | Input: `VALIDATION_DIR / "agent-outputs" / f"{agent_id}.md"` |
| `phase3_mr_smoke.py` | `VALIDATION_DIR = Path(__file__).parent` | `VALIDATION_DIR = Path(__file__).resolve().parent.parent` |
| `phase3_mr_smoke.py` | Input: `VALIDATION_DIR / f"{agent_id}-output.md"` | Input: `VALIDATION_DIR / "agent-outputs" / f"{agent_id}.md"` |
| `phase3_mr_smoke.py` | Output: `VALIDATION_DIR / "layer3-mr-results.md"` | Output: `VALIDATION_DIR / "layer3-metamorphic" / "mr-results.md"` |
| `phase3_mr_smoke.py` | Output: `VALIDATION_DIR / "phase3-costs.json"` | Output: `VALIDATION_DIR / "layer3-metamorphic" / "costs.json"` |
| `phase4_stats.py` | `VALIDATION_DIR = Path(__file__).parent` | `VALIDATION_DIR = Path(__file__).resolve().parent.parent` |
| `phase4_stats.py` | Input: `VALIDATION_DIR / "phase2-composites.json"` | Input: `VALIDATION_DIR / "layer2-geval" / "composites.json"` |
| `phase4_stats.py` | Output: `VALIDATION_DIR / f"layer4-{agent_id}.json"` | Output: `VALIDATION_DIR / "layer4-statistical" / f"{agent_id}.json"` |
| `phase4_stats.py` | Output: `VALIDATION_DIR / f"layer4-{agent_id}.md"` | Output: `VALIDATION_DIR / "layer4-statistical" / f"{agent_id}.md"` |
| `phase4_stats.py` | Output: `VALIDATION_DIR / "layer4-results.md"` | Output: `VALIDATION_DIR / "layer4-statistical" / "results.md"` |
| `phase4_stats.py` | Output: `VALIDATION_DIR / "phase4-results.json"` | Output: `VALIDATION_DIR / "layer4-statistical" / "results.json"` |
| `phase2_score.py` | `PROJECT_ROOT = Path(__file__).resolve().parents[5]` | `PROJECT_ROOT = Path(__file__).resolve().parents[6]` |
| `phase3_mr_smoke.py` | `PROJECT_ROOT = Path(__file__).resolve().parents[5]` | `PROJECT_ROOT = Path(__file__).resolve().parents[6]` |
| `phase4_stats.py` | `PROJECT_ROOT = Path(__file__).resolve().parents[5]` | `PROJECT_ROOT = Path(__file__).resolve().parents[6]` |

### Execution Steps

1. Create subdirectories: `agent-outputs/`, `layer2-geval/`, `layer3-metamorphic/`, `layer4-statistical/`, `scripts/`
2. `git mv` all files per mapping table above
3. Update path references in all 3 scripts + `check_imports.py`
4. Update `execution-prompt-v1.md` usage commands
5. Verify all 3 scripts execute without errors: `uv run python .../scripts/phase2_score.py --help` (dry run)
6. Run `uv run pytest tests/prompt-regression/` to confirm no test breakage

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 6 |
| **Completion %** | 100% |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-036-004: Baseline Collection and Validation Execution](./FEAT-036-004-baseline-execution.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Should precede | STORY-036-001 | Reorganize before executing real validation runs to avoid path confusion |
| Modifies | `validation-run/phase2_score.py` | Path references updated |
| Modifies | `validation-run/phase3_mr_smoke.py` | Path references updated |
| Modifies | `validation-run/phase4_stats.py` | Path references updated |
| Modifies | `test-harness/execution-prompt-v1.md` | Usage instructions updated |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Story created; reorganize flat validation-run directory by four-layer architecture |
| 2026-03-07 | Claude | completed | Executed: git mv 29 files into 5 subdirs, updated 16 path refs across 3 scripts, updated execution-prompt-v1.md |

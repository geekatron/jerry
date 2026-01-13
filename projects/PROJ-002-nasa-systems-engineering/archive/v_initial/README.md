# Archive: v_initial

> **Archived:** 2026-01-10
> **Reason:** WI-SAO-021 - Orchestration Folder Refactoring
> **Work Item:** sao-021

---

## Description

This archive contains the original orchestration artifacts from the SAO Cross-Pollinated Pipeline execution (2026-01-09 to 2026-01-10). These artifacts were created before the dynamic path scheme was implemented.

**Note:** These artifacts were created using manual Task tool orchestration, NOT the orchestration skill. See `tests/orchestration-results/DEVIATION-ANALYSIS.md` for details.

---

## Archived Contents

### ps-pipeline/ (Problem-Solving Pipeline)

| Phase | Artifact | Description |
|-------|----------|-------------|
| phase-1-research | skills-optimization.md | Skills optimization research |
| phase-1-research | agent-design.md | Agent design research |
| phase-1-research | industry-practices.md | Industry practices research |
| phase-2-analysis | gap-analysis.md | Gap analysis |
| phase-2-analysis | trade-study.md | Trade study |
| phase-3-design | agent-design-specs.md | Agent design specifications |
| phase-3-design | schema-contracts.md | Schema contracts |
| phase-3-design | arch-blueprints.md | Architecture blueprints |
| phase-4-synthesis | final-synthesis.md | Final synthesis |
| phase-4-synthesis | impl-roadmap.md | Implementation roadmap |

### nse-pipeline/ (NASA SE Pipeline)

| Phase | Artifact | Description |
|-------|----------|-------------|
| phase-1-scope | skills-requirements.md | Skills requirements |
| phase-1-scope | agent-requirements.md | Agent requirements |
| phase-2-risk | technical-risks.md | Technical risks |
| phase-2-risk | implementation-risks.md | Implementation risks |
| phase-3-formal | formal-requirements.md | Formal requirements |
| phase-3-formal | formal-mitigations.md | Formal mitigations |
| phase-3-formal | verification-matrices.md | Verification matrices |
| phase-4-review | tech-review-findings.md | Technical review findings |
| phase-4-review | go-nogo-decision.md | Go/No-Go decision |
| phase-4-review | qa-signoff.md | QA sign-off |

### cross-pollination/

| Barrier | Direction | Artifact | Description |
|---------|-----------|----------|-------------|
| barrier-1 | ps-to-nse | research-findings.md | Research findings handoff |
| barrier-1 | nse-to-ps | requirements-gaps.md | Requirements gaps handoff |
| barrier-2 | ps-to-nse | analysis-findings.md | Analysis findings handoff |
| barrier-2 | nse-to-ps | risk-findings.md | Risk findings handoff |
| barrier-3 | ps-to-nse | design-specs.md | Design specs handoff |
| barrier-3 | nse-to-ps | formal-artifacts.md | Formal artifacts handoff |
| barrier-4 | ps-to-nse | synthesis-artifacts.md | Synthesis artifacts handoff |
| barrier-4 | nse-to-ps | review-artifacts.md | Review artifacts handoff |
| - | - | FINAL-INTEGRATION.md | Final integration synthesis |

---

## Total Artifact Count

| Category | Count |
|----------|-------|
| PS Pipeline Artifacts | 10 |
| NSE Pipeline Artifacts | 10 |
| Cross-Pollination Artifacts | 9 |
| **Total** | **29** |

---

## Why Archived?

This folder structure used hardcoded pipeline identifiers (`ps-pipeline`, `nse-pipeline`). The new dynamic path scheme uses:

```
orchestration/{workflow_id}/{pipeline_id}/{phase}/artifact.md
```

Where all identifiers are dynamic and determined at runtime by the orchestration skill.

---

*Archive created by WI-SAO-021*

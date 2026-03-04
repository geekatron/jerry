# Session Handoff: Leash Kernel-Level Security Research

> **Workflow ID:** `leash-kernel-security-20260303-001`
> **Project:** `PROJ-0036-LEASH-COMP`
> **Branch:** `feat/proj-0036-leash-analysis`
> **Date:** 2026-03-04
> **Criticality:** C2

---

## Resume Prompt

Copy this into a new Claude session:

```
Resume the Leash kernel-level security research workflow.

Project: PROJ-0036-LEASH-COMP
Branch: feat/proj-0036-leash-analysis

1. Read the orchestration state:
   - docs/pm-pmm/leash-analysis/ORCHESTRATION.yaml
   - docs/pm-pmm/leash-analysis/ORCHESTRATION_PLAN.md

2. Current status: Barrier 2 (Phase 3) has PASSED quality gate (0.926) and
   is awaiting human review approval. Once approved, proceed to Phase 4.

3. Remaining work:
   a. Get human approval for Barrier 2 (Phase 3 output)
   b. Update ORCHESTRATION.yaml: barrier-2.human_review = "APPROVED", phase-4.status = "IN_PROGRESS"
   c. Execute Phase 4: Synthesis and Strategic Recommendations (ps-synthesizer)
      - Input: Phase 1 + Phase 2 + Phase 3 outputs
      - Output: docs/pm-pmm/leash-analysis/04-strategic-synthesis.md
   d. Quality gate Phase 4 (adv-scorer, threshold >= 0.92)
   e. Human review at Barrier 3
   f. Execute Phase 5: TAM Research and Market Sizing (ps-researcher)
      - Input: All 4 prior phase outputs
      - Output: docs/pm-pmm/leash-analysis/05-tam-market-sizing.md
      - Data sources: WebSearch, WebFetch (analyst reports, market data)
   g. Quality gate Phase 5 (adv-scorer, threshold >= 0.92)
   h. Human review at Barrier 4 → WORKFLOW COMPLETE

4. Constraints (CRITICAL — apply to ALL phases):
   - Do NOT rely on LLM training data for market research, product analysis, or competitive intelligence
   - Use WebSearch and WebFetch for all external claims
   - Use Context7 for named library/framework documentation
   - All claims MUST cite sources with URLs
   - Unsourced claims MUST be marked as [HYPOTHESIS -- confidence: low]

5. Quality gate process per phase:
   - Score with adv-scorer using S-014 (LLM-as-Judge), 6 dimensions
   - Threshold: >= 0.92 weighted composite
   - If REVISE: targeted fixes based on dimensional gaps, re-score
   - Max 5 iterations before escalate
   - Human review REQUIRED after each quality gate passes

Use /orchestration skill. Commit results to branch feat/proj-0036-leash-analysis.
```

---

## Workflow Status

| Phase | Title | Status | Score | Iterations |
|-------|-------|--------|-------|------------|
| 1 | Leash Product Analysis | COMPLETE | 0.9215 | 2 |
| 2 | Kernel Security Landscape | COMPLETE | 0.926 | 2 |
| 3 | Top 5 Competitive Analysis | COMPLETE | 0.926 | 2 |
| 4 | Synthesis and Strategic Recommendations | BLOCKED | — | — |
| 5 | TAM Research and Market Sizing | BLOCKED | — | — |

| Barrier | Status | Human Review |
|---------|--------|--------------|
| Barrier 1 (Phase 1+2) | QUALITY_PASSED | APPROVED |
| Barrier 2 (Phase 3) | QUALITY_PASSED | **PENDING** |
| Barrier 3 (Phase 4) | PENDING | — |
| Barrier 4 (Phase 5) | PENDING | — |

---

## Completed Artifacts

All files at `docs/pm-pmm/leash-analysis/` on branch `feat/proj-0036-leash-analysis`:

| File | Lines | Sources | Description |
|------|-------|---------|-------------|
| `01-leash-product-analysis.md` | 509 | 23 | strongDM Leash architecture, Cedar policies, MCP governance, JTBD use cases, Delinea acquisition |
| `02-kernel-security-landscape.md` | 799 | 71 | 7 technology categories (eBPF, seccomp, LSMs, hypervisors, WASM, policy engines, supply chain), performance matrix, adoption heat map |
| `03-competitive-analysis-top5.md` | 719 | 61 | Top 5: Google Agent Sandbox, Tetragon/Cisco, Edera, Sysdig/Falco, Chainguard. Porter's Five Forces, Blue Ocean value curves, battle cards |
| `ORCHESTRATION.yaml` | 169 | — | Machine-readable workflow state (SSOT) |
| `ORCHESTRATION_PLAN.md` | 191 | — | Workflow diagram, phase definitions, quality gates |

---

## Pending Artifacts (Not Yet Created)

| File | Agent | Input Artifacts |
|------|-------|-----------------|
| `04-strategic-synthesis.md` | ps-synthesizer | Phase 1, 2, 3 outputs |
| `05-tam-market-sizing.md` | ps-researcher | Phase 1, 2, 3, 4 outputs |

---

## Phase 4 Execution Notes

Phase 4 uses `ps-synthesizer` (not ps-researcher). It synthesizes across all three prior deliverables to produce:

- Strategic positioning of Leash in the ecosystem
- Build vs. partner vs. acquire recommendations
- Gap analysis (what Leash has vs. what it needs)
- Risk assessment (competitive threats, technology risks)
- Roadmap recommendations

No WebSearch needed — Phase 4 is synthesis of existing research.

---

## Phase 5 Execution Notes

Phase 5 uses `ps-researcher` for TAM/SAM/SOM market sizing:

- **TAM:** Total kernel-level security / AI agent security market
- **SAM:** Segments where Leash can realistically compete
- **SOM:** Near-term obtainable market share
- Data sources: Analyst reports (Gartner, Forrester, IDC), market research firms, vendor financial data
- Must cite all market size figures with analyst source and year
- Distinguish estimates from verified figures

---

## Quality Gate Scoring Dimensions

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

---

## Git Context

- **Branch:** `feat/proj-0036-leash-analysis` (pushed to origin)
- **Latest commit:** `070ab8a3` — `docs(PROJ-0036): add Leash kernel-level security research phases 1-3`
- **Base:** branched from `feat/proj-017-quality-framework-analysis` at `4d993b16`
- **Note:** Pre-existing test failure in `test_cli_create_work_item_json_output` (stream version mismatch) — unrelated to this work. Use `SKIP=pytest` for docs-only commits if needed.
- **Main repo branch:** `feat/proj-017-quality-framework-analysis` has PROJ-017 files staged (not committed) — do not disturb.

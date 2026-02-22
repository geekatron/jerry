# Barrier 2: PS-to-NSE Cross-Pollination Synthesis

> **Direction:** Pipeline A (PS) -> Pipeline B (NSE)
> **Barrier:** barrier-2
> **Workflow:** llm-deception-20260222-002
> **Date:** 2026-02-22

## Purpose

Transfer Phase 2 A/B test results from the Problem Solving pipeline to the NASA Systems Engineering pipeline for downstream technical review and synthesis validation.

---

## Key Findings Transferred

### 1. Two-Leg Thesis Established

The redesigned A/B test (15 questions, 5 domains, ITS/PC split) confirms two distinct failure modes:

- **Leg 1 (Confident Micro-Inaccuracy):** Agent A achieves 0.85 FA on ITS questions with 0.07 mean CIR across 4/5 domains. Errors are subtle, specific, and stated with high confidence.
- **Leg 2 (Knowledge Gaps):** Agent A drops to 0.07 FA on PC questions with 0.87 CC -- appropriate decline behavior.

### 2. Domain Reliability Hierarchy

| Tier | Domain | ITS FA | CIR |
|------|--------|--------|-----|
| T1 | Science/Medicine | 0.95 | 0.00 |
| T2 | History/Geography | 0.925 | 0.05 |
| T3 | Pop Culture/Media | 0.85 | 0.075 |
| T3 | Sports/Adventure | 0.825 | 0.05 |
| T4 | Technology/Software | 0.55 | 0.30 |

### 3. Verification Criteria Status

| ID | Status |
|----|--------|
| VC-001 | PASS (5/10 ITS questions with CIR > 0 across 4/5 domains) |
| VC-002 | PASS (6 documented confident errors) |
| VC-003 | PASS (Agent B corrects all 6 with sources) |
| VC-004 | PASS (0.78 FA gap between ITS and PC for Agent A) |
| VC-005 | PENDING (Phase 4) |
| VC-006 | PASS (15 questions, 5 domains) |

### 4. Specific Error Catalogue

Six documented confident inaccuracies spanning Technology (3), History (1), Pop Culture (2):
1. Python requests Session version (1.0.0 vs 0.6.0)
2. Python requests current version (hedged)
3. urllib3 dependency relationship (bundled vs external)
4. Naypyidaw capital date (2006 vs 2005)
5. MCU film count (11 vs 12)
6. Samuel L. Jackson first film (initial wrong answer)

### 5. Architectural Implications

- Tool-augmented retrieval eliminates the ITS/PC divide (Agent B: 0.06 FA gap vs Agent A: 0.78)
- The Snapshot Problem is the root cause of Leg 1 failures
- Domain-aware tool routing is the recommended mitigation architecture

---

## Artifacts for NSE Review

| Artifact | Path | Purpose |
|----------|------|---------|
| Comparative Analysis | ps/phase-2-ab-test/ps-analyst-002/ps-analyst-002-output.md | Per-question 7-dimension scoring |
| Ground Truth | ps/phase-2-ab-test/ps-researcher-005-agent-a/ground-truth.md | Verified factual baselines |
| Agent A Responses | ps/phase-2-ab-test/ps-researcher-005-agent-a/agent-a-responses.md | Internal-only answers |
| Agent B Responses | ps/phase-2-ab-test/ps-researcher-006-agent-b/agent-b-responses.md | Tool-augmented answers |
| Research Questions | ps/phase-2-ab-test/nse-requirements-002/nse-requirements-002-output.md | 15 questions with rubric |

---

*Barrier: barrier-2 | Direction: a-to-b | Status: COMPLETE*

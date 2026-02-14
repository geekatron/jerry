# TASK-005: SKILL.md Update Content for Adversarial Capabilities

<!--
DOCUMENT-ID: FEAT-004:EN-304:TASK-005
VERSION: 1.0.0
AGENT: ps-architect-304 (creator)
DATE: 2026-02-13
STATUS: Draft
PARENT: EN-304 (Problem-Solving Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DOCUMENTATION
INPUT: TASK-001 (requirements), TASK-002 (mode design), TASK-003 (invocation protocol), TASK-004 (agent spec)
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-304
> **Quality Target:** >= 0.92
> **Purpose:** Define the content updates for `skills/problem-solving/SKILL.md` to document adversarial capabilities, available modes with usage examples, and enforcement layer integration. This document specifies WHAT to add; it does NOT modify SKILL.md directly.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this document delivers |
| [Version Change](#version-change) | SKILL.md version bump |
| [Navigation Table Updates](#navigation-table-updates) | New sections to add to navigation |
| [Agent Table Update](#agent-table-update) | Updated ps-critic entry in agents table |
| [New Section: Adversarial Review Capabilities](#new-section-adversarial-review-capabilities) | Complete new section content |
| [New Section: Available Adversarial Modes](#new-section-available-adversarial-modes) | Mode catalog with usage examples |
| [New Section: Criticality-Based Strategy Selection](#new-section-criticality-based-strategy-selection) | C1-C4 integration documentation |
| [New Section: Enforcement Layer Integration](#new-section-enforcement-layer-integration) | How adversarial modes connect to enforcement |
| [Updated Section: When to Use](#updated-section-when-to-use) | Expanded trigger phrases for adversarial modes |
| [Traceability](#traceability) | Mapping to TASK-001 requirements |
| [References](#references) | Source citations |

---

## Summary

This document specifies the content to be added to `skills/problem-solving/SKILL.md` (currently v2.1.0) to document the new adversarial review capabilities. The updates add four new sections and modify two existing sections, increasing the skill documentation to cover:

- What adversarial review is and when to use it
- The 10 available modes with concrete usage examples
- How criticality levels (C1-C4) drive automatic strategy selection
- How the adversarial modes integrate with the enforcement architecture (L1-L5)

The current SKILL.md describes ps-critic as "Quality Evaluator - Iterative refinement with quality scores" with no mention of adversarial modes. After this update, the documentation will reflect ps-critic's expanded role as described in TASK-004 (v3.0.0).

---

## Version Change

| Attribute | Current | Updated |
|-----------|---------|---------|
| SKILL.md version | 2.1.0 | 3.0.0 |
| ps-critic version reference | 2.2.0 | 3.0.0 |

---

## Navigation Table Updates

### New Entries for Triple-Lens Navigation

Add to the existing navigation table in SKILL.md:

**L0 additions:**
```
| **L0 (ELI5)** | Stakeholders | ..., [Adversarial Review](#adversarial-review-capabilities) |
```

**L1 additions:**
```
| **L1 (Engineer)** | Developers | ..., [Available Modes](#available-adversarial-modes), [Criticality Selection](#criticality-based-strategy-selection) |
```

**L2 additions:**
```
| **L2 (Architect)** | Designers | ..., [Enforcement Integration](#enforcement-layer-integration) |
```

---

## Agent Table Update

### Current ps-critic Entry

```
| ps-critic | Quality Evaluator | Iterative refinement with quality scores |
```

### Updated ps-critic Entry

```
| ps-critic | Quality Evaluator & Adversarial Reviewer | 10 adversarial review modes (C1-C4 criticality-based); iterative refinement with 0.92 quality gate; S-014 LLM-as-Judge scoring with anti-leniency calibration |
```

---

## New Section: Adversarial Review Capabilities

**Location:** After the existing "Agents" section, before "Quick Start" (or as appropriate per document structure).

### Content

```markdown
## Adversarial Review Capabilities

The /problem-solving skill provides adversarial review through the ps-critic agent's 10 adversarial modes. Each mode implements one of the strategies selected in ADR-EPIC002-001 for Jerry's quality framework.

### What Is Adversarial Review?

Adversarial review applies structured challenge strategies to artifacts (code, architecture decisions, requirements, research, process definitions) to find defects, weaknesses, and blind spots that standard review would miss. Instead of asking "is this good?" adversarial review asks specific questions like:

- "What would make this FAIL?" (inversion, pre-mortem, fmea)
- "Is this argument as strong as it could be?" (steelman)
- "What assumptions are we making that could be wrong?" (devils-advocate)
- "Does this comply with our rules and standards?" (constitutional)
- "Are the factual claims in this actually correct?" (chain-of-verification)
- "How would an adversary exploit this?" (red-team)
- "What is the quality score?" (llm-as-judge)

### When to Use Adversarial Review

Adversarial review is activated automatically based on criticality level:

| Criticality | When | Strategies Applied |
|-------------|------|-------------------|
| **C1 (Routine)** | Standard code changes, docs, config | Self-Refine only |
| **C2 (Significant)** | New features, interface changes, refactoring | Constitutional + Devil's Advocate + LLM-as-Judge |
| **C3 (Major)** | Architecture decisions, cross-boundary changes, governance | Full 6-strategy deep review |
| **C4 (Critical)** | Constitutional amendments, irreversible decisions | All 10 strategies (tournament) |

### Quality Gate

When adversarial modes are active, the quality gate threshold is **>= 0.92** (HARD rule H-13), enforced through S-014 LLM-as-Judge scoring with anti-leniency calibration (H-16). This is higher than the standard mode threshold of 0.85 to reflect the increased rigor of adversarial review.

### Source

- **ADR-EPIC002-001:** Strategy selection (10 selected, 5 excluded)
- **EN-303:** Situational applicability mapping and decision tree
- **EN-304:** This skill enhancement enabler
```

---

## New Section: Available Adversarial Modes

**Location:** Immediately after "Adversarial Review Capabilities."

### Content

```markdown
## Available Adversarial Modes

The ps-critic agent supports the following 10 adversarial modes, listed by ADR rank:

| Rank | Mode | Strategy | Token Budget | When Used |
|------|------|----------|-------------|-----------|
| 1 | `llm-as-judge` | S-014 LLM-as-Judge | ~2,000 | Quality scoring (C2+) |
| 2 | `steelman` | S-003 Steelman Technique | ~1,600 | Fair argument reconstruction before critique (C2+) |
| 3 | `inversion` | S-013 Inversion Technique | ~2,100 | Anti-pattern and failure criteria generation (C3+) |
| 4 | `constitutional` | S-007 Constitutional AI | ~8,000-16,000 | Standards compliance evaluation (C2+) |
| 5 | `devils-advocate` | S-002 Devil's Advocate | ~4,600 | Assumption and decision challenging (C2+) |
| 6 | `pre-mortem` | S-004 Pre-Mortem Analysis | ~5,600 | Future failure imagination (C3+) |
| 7 | `self-refine` | S-010 Self-Refine | ~2,000 | Iterative self-improvement (C1+) |
| 8 | `fmea` | S-012 FMEA | ~9,000 | Systematic failure mode analysis (C3+) |
| 9 | `chain-of-verification` | S-011 Chain-of-Verification | ~4,500 | Factual claim verification (C4) |
| 10 | `red-team` | S-001 Red Team Analysis | ~6,500 | Adversary simulation (C3-C4) |

### Usage Examples

**Explicit single mode:**
```
Invoke ps-critic in red-team mode on the ADR:
  --mode red-team
  --artifact projects/PROJ-001/decisions/ADR-003.md
  --criticality C3
```

**Explicit multi-mode pipeline:**
```
Run a C2 adversarial review:
  --mode steelman,constitutional,devils-advocate,llm-as-judge
  --artifact work/EN-304/TASK-002.md
```

**Automatic mode selection:**
```
Run adversarial review with automatic strategy selection:
  --mode auto
  --artifact src/domain/aggregates/work_item.py
  --criticality C2
  --phase PH-IMPL
  --target-type TGT-CODE
```

### Canonical Pipelines

| Criticality | Pipeline | Total Tokens |
|-------------|----------|-------------|
| C1 | `self-refine` | ~2,000 |
| C2 | `steelman` -> `constitutional` -> `devils-advocate` -> `llm-as-judge` | ~14,800 |
| C3 | `steelman` -> `inversion` -> `constitutional` -> `devils-advocate` -> `pre-mortem` -> `fmea` -> `llm-as-judge` | ~33,500 |
| C4 | `self-refine` -> `steelman` -> `inversion` -> `constitutional` -> `devils-advocate` -> `pre-mortem` -> `fmea` -> `chain-of-verification` -> `red-team` -> `llm-as-judge` | ~50,300 |
```

---

## New Section: Criticality-Based Strategy Selection

**Location:** After "Available Adversarial Modes."

### Content

```markdown
## Criticality-Based Strategy Selection

### Automatic Criticality Detection

The invocation protocol automatically detects criticality based on the artifact being reviewed:

| Signal | Criticality | Source |
|--------|-------------|--------|
| Modifies `JERRY_CONSTITUTION.md` | C3 minimum (AE-001) | Auto-escalation |
| Modifies `.claude/rules/` | C3 minimum (AE-002) | Auto-escalation |
| New or modified ADR | C3 minimum (AE-003) | Auto-escalation |
| Modifies baselined ADR | C4 (AE-004) | Auto-escalation |
| Security-relevant code | C3 minimum (AE-005) | Auto-escalation |
| Routine code change | C1 default | Decision tree |
| New feature | C2 default | Decision tree |

### Strategy Activation Matrix

| Mode | C1 | C2 | C3 | C4 |
|------|----|----|----|----|
| `self-refine` | Required | Recommended | Recommended | Required |
| `steelman` | Optional | Recommended | Required | Required |
| `inversion` | -- | Optional | Required | Required |
| `constitutional` | -- | Required | Required | Required |
| `devils-advocate` | -- | Required | Required | Required |
| `pre-mortem` | -- | -- | Required | Required |
| `fmea` | -- | -- | Required | Required |
| `chain-of-verification` | -- | -- | Optional | Required |
| `llm-as-judge` | Optional | Required | Required | Required |
| `red-team` | -- | -- | Optional | Required |

### Token Budget Adaptation

When token budget is constrained, strategy sets are reduced:

- **TOK-FULL** (> 20K remaining): Full strategy set per criticality
- **TOK-CONST** (5K-20K remaining): Reduced sets prioritizing highest-ranked strategies
- **TOK-EXHAUST** (< 5K remaining): Minimal strategies; human escalation at C3+; session end at C4

### Decision Tree Reference

The full strategy selection decision tree is documented in EN-303 TASK-004. It provides deterministic O(1) selection based on 8 context dimensions: criticality, phase, target type, maturity, team composition, enforcement layer availability, platform context, and token budget state.
```

---

## New Section: Enforcement Layer Integration

**Location:** After "Criticality-Based Strategy Selection."

### Content

```markdown
## Enforcement Layer Integration

The adversarial modes integrate with Jerry's 5-layer enforcement architecture:

### Layer Mapping

| Layer | Enforcement Mechanism | Adversarial Mode Integration |
|-------|----------------------|------------------------------|
| **L1: Static Context** | Rules in `.context/rules/` | Mode definitions and strategy encodings loaded at session start |
| **L2: Per-Prompt** | PromptReinforcementEngine (600 tokens/prompt) | ContentBlocks reinforce key strategies (quality-gate, constitutional-principles, steelman, etc.) |
| **L3: Pre-Action** | PreToolEnforcementEngine (zero tokens) | Governance file modifications trigger auto-escalation to C3+, activating deeper adversarial review |
| **L4: Post-Action** | Post-action validation (future) | Mode results inform post-action quality checks |
| **L5: Post-Hoc** | CI pipeline and architecture tests | Anti-pattern checklists from inversion mode can feed CI checks |
| **Process** | Quality gates, review workflows | Creator-critic-revision cycle with 3-iteration minimum |

### ContentBlock Alignment

The L2 per-prompt reinforcement system uses priority-ranked ContentBlocks that align with adversarial modes:

| ContentBlock | Priority | Aligned Mode |
|-------------|----------|--------------|
| `quality-gate` | 1 | `llm-as-judge` |
| `constitutional-principles` | 2 | `constitutional` |
| `self-review` | 3 | `self-refine` |
| `scoring-requirement` | 4 | `llm-as-judge` |
| `steelman` | 5 | `steelman` |
| `leniency-calibration` | 6 | `llm-as-judge` |
| `deep-review` | 7 | Multi-mode pipeline |

### SSOT Reference

Shared enforcement constants are sourced from `quality-enforcement.md`:
- Quality threshold: 0.92
- Criticality levels: C1-C4
- Strategy encodings: 6 strategies encoded (~119 tokens)
- Iteration cycle count: minimum 3
- Tier vocabulary: HARD/MEDIUM/SOFT
```

---

## Updated Section: When to Use

### Current Trigger Phrases

The current SKILL.md lists trigger phrases for automatic skill invocation. Add adversarial-specific triggers:

### Additional Trigger Phrases

```markdown
### Adversarial Review Triggers

| Trigger Phrase | Action |
|---------------|--------|
| "adversarial review", "adversarial critique" | Invoke ps-critic in automatic mode selection |
| "red team", "red-team" | Invoke ps-critic in red-team mode |
| "steelman", "steelman this" | Invoke ps-critic in steelman mode |
| "devil's advocate", "challenge this" | Invoke ps-critic in devils-advocate mode |
| "constitutional check", "compliance review" | Invoke ps-critic in constitutional mode |
| "pre-mortem", "how could this fail" | Invoke ps-critic in pre-mortem mode |
| "FMEA", "failure analysis" | Invoke ps-critic in fmea mode |
| "verify claims", "fact check" | Invoke ps-critic in chain-of-verification mode |
| "quality score", "score this" | Invoke ps-critic in llm-as-judge mode |
| "inversion", "anti-patterns" | Invoke ps-critic in inversion mode |
```

---

## Traceability

### Requirements Coverage

| Requirement | Coverage |
|-------------|----------|
| FR-304-001 (10 modes) | Available Adversarial Modes -- all 10 documented |
| FR-304-003 (Explicit selection) | Usage examples with --mode syntax |
| FR-304-004 (Automatic selection) | Criticality-Based Strategy Selection section |
| FR-304-006 (C1-C4 mapping) | Strategy Activation Matrix |
| IR-304-002 (L2-REINJECT tags) | Enforcement Layer Integration mentions L2 content |
| IR-304-003 (SSOT) | SSOT Reference subsection |
| IR-304-004 (SessionStart listing) | Enforcement Layer Integration L1 mapping |
| IR-304-005 (ContentBlock) | ContentBlock Alignment table |
| EN-304 AC-7 | This document (SKILL.md adversarial documentation with usage examples) |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | SKILL.md v2.1.0 | Current /problem-solving skill documentation (baseline) |
| 2 | ADR-EPIC002-001 | Strategy selection and ranking |
| 3 | EN-303 TASK-004 | Decision tree for automatic selection |
| 4 | TASK-001 (this enabler) | Formal requirements |
| 5 | TASK-002 (this enabler) | Mode definitions |
| 6 | TASK-003 (this enabler) | Invocation protocol |
| 7 | TASK-004 (this enabler) | Agent spec updates |
| 8 | Barrier-2 ENF-to-ADV | ContentBlock system, enforcement layers |

---

*Document ID: FEAT-004:EN-304:TASK-005*
*Agent: ps-architect-304*
*Created: 2026-02-13*
*Status: Draft*

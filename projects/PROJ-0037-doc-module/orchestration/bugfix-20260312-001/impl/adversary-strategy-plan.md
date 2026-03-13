# Strategy Selection Plan — PROJ-0037 Bugfix Workflow
# Generated: 2026-03-12
# Agent: adv-selector
# SSOT Source: .context/rules/quality-enforcement.md

## Criticality Assessment
requested_level: C2
auto_escalation_applied: false
escalation_rules_checked:
  - AE-001: "constitution — NOT TRIGGERED (deliverable does not touch JERRY_CONSTITUTION.md)"
  - AE-002: "rules — NOT TRIGGERED (deliverable does not touch .context/rules/)"
  - AE-003: "ADR — NOT TRIGGERED (deliverable is Orchestration Plan, not ADR)"
  - AE-004: "baselined ADR — NOT TRIGGERED (no existing ADR at this path)"
  - AE-005: "security code — NOT TRIGGERED (YAML reader is stdlib, not security-relevant)"
  - AE-006: "token fill — NOMINAL tier (60K/200K context, 30% fill)"
final_level: C2

## Selected Strategies (Ordered)
# Format: | Order | Strategy ID | Strategy Name | Template Path | Required/Optional | H-16 Compliance |
strategies:
  - order: 1
    id: S-010
    name: Self-Refine
    template_path: .context/templates/adversarial/s-010-self-refine.md
    requirement: Optional (C2)
    group: A (Self-Review)
    h16_notes: "Placed first per recommended execution order (Group A)"

  - order: 2
    id: S-003
    name: Steelman Technique
    template_path: .context/templates/adversarial/s-003-steelman.md
    requirement: Optional (C2)
    group: B (Strengthen)
    h16_notes: "H-16 REQUIRED: S-003 position (2) before S-002 position (3) — SATISFIED"

  - order: 3
    id: S-002
    name: Devil's Advocate
    template_path: .context/templates/adversarial/s-002-devils-advocate.md
    requirement: Required (C2)
    group: C (Challenge)
    h16_notes: "H-16 REQUIRED: S-002 ordered after S-003 — SATISFIED"

  - order: 4
    id: S-007
    name: Constitutional AI Critique
    template_path: .context/templates/adversarial/s-007-constitutional-ai.md
    requirement: Required (C2)
    group: D (Verify)
    h16_notes: "No H-16 constraint (not Steelman/Devil's Advocate pair)"

  - order: 5
    id: S-014
    name: LLM-as-Judge
    template_path: .context/templates/adversarial/s-014-llm-as-judge.md
    requirement: Required (C2)
    group: F (Score)
    h16_notes: "Placed LAST per H-16 requirement (S-014 always final)"

## H-16 Compliance Report
steelman_position: 2
devils_advocate_position: 3
constraint_satisfied: true
constraint_note: "S-003 (Steelman, pos 2) ordered BEFORE S-002 (Devil's Advocate, pos 3) per H-16 HARD rule"

## Strategies NOT Selected (C2)
excluded_strategies:
  - id: S-001
    name: Red Team Analysis
    reason: "Optional for C2 (not required)"
  - id: S-004
    name: Pre-Mortem Analysis
    reason: "Optional for C2 (not required)"
  - id: S-011
    name: Chain-of-Verification
    reason: "Optional for C2 (not required)"
  - id: S-012
    name: FMEA
    reason: "Optional for C2 (not required)"
  - id: S-013
    name: Inversion Technique
    reason: "Optional for C2 (not required)"

## Summary
total_strategies_selected: 5
required_count: 3  # S-007, S-002, S-014
optional_selected: 2  # S-010, S-003
required_satisfied: true
optional_note: "S-010 and S-003 included to strengthen review quality per H-14 creator-critic-revision cycle"

## Execution Notes
- Threshold: >= 0.92 (quality-enforcement.md H-13)
- Max iterations: 5 (C2 per agent-development-standards.md RT-M-010)
- Critic: adv-scorer agent (S-014 rubric scorer)
- All template paths verified in .context/templates/adversarial/
- H-15 (self-review) applies before critic invocation per quality-enforcement.md

## Verification Checklist
- [x] All strategy IDs valid (S-001 through S-014, selected only)
- [x] H-16 ordering satisfied (S-003 pos < S-002 pos)
- [x] Auto-escalation rules checked (none triggered)
- [x] Template paths correspond to selected strategies
- [x] Required strategies present (S-007, S-002, S-014)
- [x] Optional strategies documented
- [x] P-003 self-check passed (no recursive subagent invocations in selector)

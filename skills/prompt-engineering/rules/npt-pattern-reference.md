# NPT Pattern Reference

> Actionable reference for pe-constraint-gen. Active patterns only: NPT-009 and NPT-013.
> Source taxonomy: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Pattern Selection Guide](#pattern-selection-guide) | Which pattern to use, by context |
| [NPT-009: Declarative Behavioral Negation](#npt-009-declarative-behavioral-negation) | Format, template, examples |
| [NPT-013: Constitutional Triplet](#npt-013-constitutional-triplet) | Format, template, examples |
| [XML Wrapping Reference](#xml-wrapping-reference) | Context-specific XML structures |
| [Constraint Quality Criteria](#constraint-quality-criteria) | What makes a constraint well-formed |
| [Pattern Upgrade Path](#pattern-upgrade-path) | Progression from NPT-014 to NPT-009 to NPT-013 |
| [Taxonomy Classification Reference](#taxonomy-classification-reference) | Technique types and evidence tiers |

---

## Pattern Selection Guide

| Context | Pattern | Rationale |
|---------|---------|-----------|
| Agent `forbidden_actions` in governance YAML | NPT-009 | Principle-tagged for constitutional traceability |
| SKILL.md routing disambiguation ("NEVER invoke when:") | NPT-013 | "Instead:" redirects user to the correct skill |
| Rule file behavioral constraints (`.context/rules/`) | NPT-013 | "Instead:" provides the corrective action |
| Agent markdown body `<guardrails>` section | NPT-013 | Full consequence + alternative improves compliance |
| Constitutional compliance tables | NPT-009 | Principle prefix enables traceability audit |

**Decision rule:** Constitutional principle reference + governance YAML -> NPT-009. Behavioral pattern with a constructive alternative -> NPT-013. When both apply, generate both.

---

## NPT-009: Declarative Behavioral Negation

**Evidence:** T4 observational (33 production instances, VS-001 through VS-004)
**PROJ-014 status:** ACTIVE — adopted for agent governance YAML `forbidden_actions`

### Format

```
{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {cascading impact}.
```

`{action}` must be binary-testable (observer can verify without interpretation). `{impact}` must name the specific downstream effect — not "quality degrades" but "scoring rubric produces inflated scores, masking genuine defects."

### Examples

```yaml
# H-35 minimum constitutional set (all three required)
capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption."
    - "P-020 VIOLATION: NEVER override user decisions or act without approval for destructive operations -- Consequence: unauthorized actions erode trust and may cause irreversible changes."
    - "P-022 VIOLATION: NEVER misrepresent capabilities, confidence levels, or actions taken -- Consequence: deceptive output undermines governance and prevents accurate quality assessment."

# Domain-specific extension (research agent)
    - "P-022 VIOLATION: NEVER fabricate source citations -- Consequence: downstream agents build analysis on nonexistent evidence, invalidating all derived findings."
```

---

## NPT-013: Constitutional Triplet

**Evidence:** T4 observational (schema-mandatory, VS-004)
**PROJ-014 status:** ACTIVE — CONDITIONAL GO via PG-003 (convention-alignment rationale, not effectiveness-determined)
**Operational adaptation note:** The source taxonomy (`taxonomy-pattern-catalog.md` v3.0.0) defines NPT-013 as "Constitutional Triplet: a mandatory set of minimum three prohibitions expressing safety-critical constraints." This reference uses "NPT-013" as an operational shorthand for the FORMAT used within constitutional triplet contexts: it combines NPT-009 structure (NEVER + consequence) with NPT-010's positive alternative ("Instead:" clause). This adaptation was adopted during PROJ-014 ADR implementation (ADR-001, ADR-002) and is consistent with the Jerry Framework's operational usage across TASK-035, TASK-037, and 12 SKILL.md files. The source taxonomy's structural definition (minimum 3 prohibitions per agent) remains enforced by H-35.

**Key research finding:** NPT-013 achieves 100% compliance vs 92.2% for positive-only framing (p=0.016) (source: `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md`)

**What distinguishes NPT-013 from NPT-009:** The `Instead:` alternative clause. NPT-013 provides a constructive replacement action; NPT-009 states the consequence only.

### Format

```
NEVER {action} -- Consequence: {cascading impact}. Instead: {actionable alternative}.
```

The `Instead:` clause must be achievable with the agent's declared tools and specific enough to act on.

### Examples

```
# Rule file behavioral constraint
NEVER fabricate source citations -- Consequence: downstream agents build analysis on nonexistent evidence. Instead: explicitly state when no source is available and mark confidence as low.

# SKILL.md routing disambiguation
NEVER invoke /problem-solving when the user needs a structured requirements document -- Consequence: unstructured research output does not satisfy V&V traceability requirements. Instead: invoke /nasa-se for requirements and specification work.

# Orchestration boundary rule
NEVER pass inline content in handoff objects -- Consequence: content duplication across handoff chain exhausts context budget, triggering premature compaction. Instead: pass file paths and load content via Read in the receiving agent.
```

---

## XML Wrapping Reference

| Context | Structure |
|---------|-----------|
| Governance YAML (`forbidden_actions`) | Plain YAML string — no XML wrapper |
| Agent markdown body `<guardrails>` | `<constraint format="NPT-013">...</constraint>` |
| Standalone XML block | `<forbidden_actions><constraint format="NPT-009">...</constraint></forbidden_actions>` |

```xml
<!-- Agent markdown body -->
<constraint format="NPT-013">
NEVER {action} -- Consequence: {impact}. Instead: {alternative}.
</constraint>

<!-- Standalone XML block -->
<forbidden_actions>
  <constraint format="NPT-009">{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}.</constraint>
</forbidden_actions>
```

---

## Constraint Quality Criteria

Self-review checklist before delivering any generated constraint (H-15).

| Check | Pass | Fail Example |
|-------|------|--------------|
| Binary-testable action | Observer can verify compliance without interpretation | "avoid being too verbose" |
| Single action per constraint | One NEVER per constraint | "NEVER do X or Y" |
| Specific consequence | Names the exact downstream effect | "quality degrades" |
| Actionable alternative (NPT-013) | Uses tools from the agent's declared allowed_tools | "use a different tool" |
| Principle exists (NPT-009) | P-NNN maps to an actual constitutional principle | P-099 (does not exist) |
| Taxonomy labels verified | All A1-A7 and T1-T5 labels match source taxonomy SSOT | "A5 Scope Limitation" (label does not match source) |

---

## Pattern Upgrade Path

When pe-constraint-gen encounters existing constraints, use this progression to determine the upgrade target:

| Current Pattern | Upgrade To | Decision Criterion |
|----------------|------------|-------------------|
| NPT-014 (blunt prohibition: "Don't do X") | NPT-009 | Add specificity + consequence documentation |
| NPT-009 (NEVER + consequence) | NPT-013 (operational) | Add "Instead:" alternative when a constructive replacement exists |
| Positive-only instruction | NPT-013 (operational) | Convert to NEVER + consequence + alternative per PROJ-014 findings |

**NPT-014 diagnostic:** An existing constraint matching NPT-014 is an upgrade candidate. Signs: no NEVER keyword, no consequence clause, vague action ("avoid being too verbose"), compound prohibitions ("NEVER do X or Y"). See Constraint Quality Criteria for the full checklist.

---

## Taxonomy Classification Reference

Full 14-pattern catalog at: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md`

**Technique types (A1–A7):** A1 Prohibition-only | A2 Structured prohibition | A3 Augmented prohibition | A4 Enforcement-tier prohibition | A5 Programmatic enforcement | A6 Training-time constraint | A7 Meta-prompting

**Evidence tiers:** T1 Peer-reviewed | T2 (empty in this catalog — see taxonomy T2 tier note) | T3 Preprint / unreviewed | T4 Practitioner observation | T5 Session observation

**Pattern assignments by technique type:** A1: NPT-014 | A2: NPT-006, NPT-007, NPT-009, NPT-010 | A3: NPT-008, NPT-010, NPT-011, NPT-012 | A4: NPT-010, NPT-012, NPT-013 | A5: NPT-003, NPT-004 | A6: NPT-001, NPT-002 | A7: NPT-005, NPT-006

**Pattern assignments by evidence tier:** T1: NPT-006, NPT-007 | T3: NPT-005, NPT-008 (partial), NPT-014 (partial) | T4: NPT-009, NPT-010, NPT-011, NPT-012, NPT-013 | T5: NPT-013 (partial)

NPT-009 and NPT-013 are both T4. Both are adopted on convention-alignment grounds (PG-003). Causal superiority over positive-only framing is UNTESTED.

---

*Version: 1.1.0 | Created: 2026-03-01 | Updated: 2026-03-01 | Source: PROJ-014 TASK-025 (CONDITIONAL GO via PG-003)*
*Built against: taxonomy-pattern-catalog.md v3.0.0 (I3) | Go-no-go: `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md`*
*SSOT for pe-constraint-gen — see `skills/prompt-engineering/agents/pe-constraint-gen.md`*

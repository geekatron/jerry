# ADR: Output Directory Conventions for Problem-Solving Agents

**Status:** Accepted
**Date:** 2026-01-10
**Author:** ps-architect (E2E Validation)
**References:** PS_AGENT_TEMPLATE.md v2.0.0, Jerry Constitution P-002

---

## L0: Executive Summary (ELI5)

Each problem-solving agent in the Jerry framework outputs to a dedicated directory based on its specialist role. This convention ensures artifacts are organized predictably and discoverable by role. Architecture decisions (ADRs) go to the `decisions/` directory.

---

## L1: Technical Analysis (Software Engineer)

### Output Directory Mapping

| Agent | Output Directory | Artifact Format |
|-------|------------------|-----------------|
| ps-architect | `decisions/` | `{ps-id}-{entry-id}-adr-{decision-slug}.md` |
| ps-researcher | `research/` | `{ps-id}-{entry-id}-{topic-slug}.md` |
| ps-analyst | `analysis/` | `{ps-id}-{entry-id}-{analysis-type}.md` |
| ps-investigator | `investigations/` | `{ps-id}-{entry-id}-investigation.md` |
| ps-reporter | `reports/` | `{ps-id}-{entry-id}-{report-type}.md` |
| ps-reviewer | `reviews/` | `{ps-id}-{entry-id}-{review-type}.md` |
| ps-synthesizer | `synthesis/` | `{ps-id}-{entry-id}-synthesis.md` |
| ps-validator | `analysis/` | `{ps-id}-{entry-id}-validation.md` |

### Implementation

All agents must:
1. Check `PS_AGENT_TEMPLATE.md` output table for their designated directory
2. Create artifacts using Write tool at `projects/${JERRY_PROJECT}/{output-type}/{artifact-name}.md`
3. Include L0/L1/L2 sections in output
4. Call link-artifact to register artifact

---

## L2: Architectural Implications (Principal Architect)

### Rationale

Segregating output by role enables:
- **Discoverability**: Users know where to find architecture decisions vs. research
- **Governance**: Different agents can have different retention/review policies
- **Separation of Concerns**: Clear ownership and traceability
- **P-002 Compliance**: Mandatory file persistence with canonical locations

### Trade-offs

**Alternatives Considered:**
- Single `outputs/` directory → Lost role context, harder to navigate
- Timestamp-based grouping → Unclear which agent created content
- Per-session directories → Fragmented outputs across sessions

**Selected Approach:** Role-based directories provide best signal-to-noise ratio for artifact discovery while maintaining P-002 compliance.

---

## References

- [PS_AGENT_TEMPLATE.md](https://github.com/geekatron/jerry/blob/main/skills/problem-solving/agents/PS_AGENT_TEMPLATE.md) - Agent specification v2.0.0
- [Jerry Constitution v1.0](https://github.com/geekatron/jerry/blob/main/docs/governance/JERRY_CONSTITUTION.md) - Principle P-002 (File Persistence)

---

**Validation:** E2E test e2e-val-001, entry e-003
**Artifact Created:** `e2e-val-001-e-003-adr-output-conventions.md`

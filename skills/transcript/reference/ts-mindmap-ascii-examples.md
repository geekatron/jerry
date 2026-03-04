# ASCII Mindmap Examples and Reference

> Extracted from `ts-mindmap-ascii.md` to reduce agent definition context footprint.
> These examples and reference tables are Tier 3 supplementary content loaded on demand.

---

## Box-Drawing Characters

| Character | Unicode | Purpose |
|-----------|---------|---------|
| ┌ | U+250C | Top-left corner |
| ─ | U+2500 | Horizontal line |
| ┐ | U+2510 | Top-right corner |
| │ | U+2502 | Vertical line |
| └ | U+2514 | Bottom-left corner |
| ┘ | U+2518 | Bottom-right corner |
| ├ | U+251C | Left T-junction |
| ┤ | U+2524 | Right T-junction |
| ┬ | U+252C | Top T-junction |
| ┴ | U+2534 | Bottom T-junction |
| ▼ | U+25BC | Downward connector |

---

## ASCII Tree Structure Template

```
                    ┌─────────────────────────┐
                    │   Meeting: Q4 Planning   │
                    └───────────┬─────────────┘
           ┌────────────────────┼────────────────────┐
           │                    │                    │
    ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
    │Budget Review│     │  Timeline   │     │  Decisions  │
    └──────┬──────┘     │ Discussion  │     │    Made     │
           │            └──────┬──────┘     └─────────────┘
    ┌──────┴──────┐            │
    │   Current   │     ┌──────┴──────┐
    │   Status    │     │     Q4      │
    │ [→] Send... │     │ Deliverables│
    └─────────────┘     └─────────────┘

Legend:
  [→] Action Item    [?] Question    [!] Decision    [*] Speaker
```

---

## Sample ASCII Mindmap Output

```
                    ┌─────────────────────────┐
                    │ Q4 Planning - 2026-01-15 │
                    └───────────┬─────────────┘
           ┌────────────────────┼────────────────────┐
           │                    │                    │
    ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
    │Budget Review│     │  Timeline   │     │  Staffing   │
    └──────┬──────┘     │ Discussion  │     └──────┬──────┘
           │            └──────┬──────┘            │
    ┌──────┴──────┐     ┌──────┴──────┐     ┌──────┴──────┐
    │[→] Send...  │     │[→] Create...│     │[→] Post...  │
    │[!] Approve..│     │[?] When...  │     │[*] Alice    │
    │             │     │[!] Priorit..│     │[*] Bob      │
    └─────────────┘     └─────────────┘     └─────────────┘

Legend:
  [→] Action Item    [?] Open Question    [✓] Answered Question
  [!] Decision       [*] Speaker
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-28 | Claude | Initial agent definition per EN-009 TASK-002 |
| 1.0.1 | 2026-01-30 | Claude | **CORRECTED** output directory from `07-mindmap/` to `08-mindmap/` per EN-024:DISC-001 |
| 1.1.0 | 2026-01-30 | Claude | **COMPLIANCE:** Added PAT-AGENT-001 YAML sections per EN-027 (identity, capabilities, guardrails, validation, constitution, session_context). Addresses GAP-A-001, GAP-A-004, GAP-A-007, GAP-A-009, GAP-Q-001 for FEAT-005 Phase 1. |
| 1.1.1 | 2026-01-30 | Claude | **REFINEMENT:** G-027 Iteration 2 compliance fixes. Expanded guardrails (8 validation rules with width enforcement mechanism), output filtering (6 filters), post-completion checks (8 checks), constitution (6 principles). Added forbidden action for non-UTF-8 box-drawing. Added template variable validation ranges. Session context customized for ASCII generation workflow. Changed output_formats to standard MIME types (text/plain, text/x-ascii-art). |
| 1.1.2 | 2026-01-30 | Claude | **MODEL-CONFIG:** Added model configuration support per EN-031 TASK-422. Added default_model and model_override to identity section. Added model override input validation rule. Added model_config to session_context.on_receive and expected_inputs. Consumes CP-2 (agent schema patterns) and CP-1 (model parameter syntax). |

### Related Documents

**Backlinks:**
- [EN-009-mindmap-generator.md](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-009-mindmap-generator/EN-009-mindmap-generator.md) - Parent enabler
- [TASK-002-ascii-generator.md](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-009-mindmap-generator/TASK-002-ascii-generator.md) - Task definition

**Forward Links:**
- [SKILL.md](../SKILL.md) - Skill definition
- [ts-mindmap-mermaid.md](../agents/ts-mindmap-mermaid.md) - Mermaid version (primary)

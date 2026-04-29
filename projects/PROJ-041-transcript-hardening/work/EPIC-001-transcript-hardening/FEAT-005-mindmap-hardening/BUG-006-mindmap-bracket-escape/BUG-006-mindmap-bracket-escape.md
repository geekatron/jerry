# BUG-006: ts-mindmap-mermaid bracket-escaping fails parse

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-005
> **Owner:** adam.nowak
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken in one paragraph |
| [Steps to Reproduce](#steps-to-reproduce) | How the failure manifests |
| [Root Cause](#root-cause) | Why this happens |
| [Tested Fix](#tested-fix) | What the audit author validated locally |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

`ts-mindmap-mermaid` agent produces non-rendering Mermaid output when packet narrative uses bracketed canonical-form disambiguation (`VERBATIM [CANONICAL]`). The Mermaid mindmap parser interprets `[...]` as a shape construct, not literal text, so any node label containing brackets fails to render under `mmdc`. Tested fix: HTML-entity escape (`&#91;`/`&#93;`) at write time. Local fix verified by audit author (125KB SVG produced, no parse errors).

---

## Steps to Reproduce

1. Run `ts-mindmap-mermaid` agent against a packet whose narrative uses bracketed canonical-form disambiguation (e.g., `RFP [RDP] Kubernetes`, `cloud MQP [AMQP]`, `FedRIP [FedRAMP]`, `[ChaCha20]`).
2. Run `mmdc -i mindmap.mmd -o render.svg` (Mermaid CLI, e.g., v11.12.0).
3. Mermaid CLI errors:
   ```
   Error: Parse error on line 36:
   ...ensitivity RFP [RDP] Kubernetes - Answer
   -----------------------^
   Expecting 'SPACELINE', 'NL', 'EOF', got 'SPACELIST'
   ```

The mindmap does not render.

---

## Root Cause

The Mermaid mindmap parser interprets `[...]` as a shape construct, not literal text. Any node label containing `[` and `]` triggers a parse error.

The convention `VERBATIM [CANONICAL]` is documented in `/transcript`'s ASR canonical-form normalization output (referenced in `_anchors.json` `editorial_conventions.canonical_form_brackets` per the iter-3-fix work). Whenever the user adopts that convention for any term, the resulting mindmap node labels fail Mermaid parsing.

This is **structural recurrence**: every future packet using bracketed canonical forms hits the same failure surface.

---

## Tested Fix

Audit author tested several alternatives:

| Input | Renders? |
|-------|----------|
| `RFP [RDP] Kubernetes` | NO (parse error) |
| `"RFP [RDP] Kubernetes"` (quoted) | NO (Mermaid mindmap doesn't support quoted leaf labels) |
| `RFP (RDP) Kubernetes` (parens) | NO (parens are also reserved — circle shape) |
| `RFP &#91;RDP&#93; Kubernetes` (HTML entities) | **YES** (renders as `RFP [RDP] Kubernetes` to the reader) |
| `["RFP [RDP] Kubernetes"]` (shape with quoted) | YES but adds extra shape wrapper |

Local fix confirmed by author: HTML-escape applied to 5 labels in PDD-0102 packet → 125KB SVG produced via `mmdc`, no parse errors, substrate verified clean.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-backend` | Update `ts-mindmap-mermaid.md` agent prompt: HTML-escape `[`/`]` (and defensively `(`/`)`/`{`/`}`) at write time |
| 2 | `/eng-team` | `eng-qa` | Regression test: bracket-canonical golden packet renders cleanly via `mmdc` (actual render, not text inspection) |
| 3 | `/eng-team` | `eng-qa` | Regression test: existing non-bracketed packets continue to render correctly |
| 4 | `/eng-team` | `eng-backend` | Add validator (extends FEAT-003 SCHEMA-* or CONTENT-* family) detecting unescaped brackets in Mermaid output |
| 5 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 6 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] `skills/transcript/agents/ts-mindmap-mermaid.md` agent prompt updated: when emitting node labels containing `[` or `]`, HTML-escape as `&#91;` and `&#93;` at write time.
- [ ] Defensive: also escape `(`, `)`, `{`, `}` for any future-reserved Mermaid syntax.
- [ ] Regression test: `test_data/golden/bracket-canonical/` packet renders cleanly via `mmdc` (or chosen renderer) — actual render check, not just text inspection.
- [ ] Existing packets without bracketed labels continue to render correctly (no regression).
- [ ] FEAT-003 SCHEMA-* or CONTENT-* validator added: detects unescaped brackets in Mermaid output (defensive guard).
- [ ] FEAT-004 STORY-015 (`discussions[]`) `[~]` ascii symbol — confirm it never appears in Mermaid output (Mermaid uses `~` not `[~]`).
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-005](../FEAT-005-mindmap-hardening.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Independent | — | Can land in parallel with FEAT-001 |
| Cooperates | FEAT-003 | Validators will guard against regression |
| Cooperates | FEAT-004 STORY-015 | discussions[] mindmap symbol must not collide with Mermaid syntax |

### Source

- [#273 comment 3](https://github.com/geekatron/jerry/issues/273#issuecomment-4339778594)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Bug created. Concrete reproduction + tested fix in audit comment. Designated early-land quick-win. |

# BUG-007: ts-mindmap-mermaid false self-claim of syntax validity

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** medium
> **Severity:** minor
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-005
> **Owner:** adam.nowak
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken in one paragraph |
| [Steps to Reproduce](#steps-to-reproduce) | How the misleading claim manifests |
| [Root Cause](#root-cause) | Why the agent's claim is unfounded |
| [Resolution Options](#resolution-options) | Two paths per audit |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

`ts-mindmap-mermaid` agent self-reports `"Mermaid syntax: Valid"` in its return summary based on textual inspection of its own output, but the agent has only `Read, Write, Glob` tools — it cannot actually render to verify. The claim violates P-022 (no deception): the agent misrepresents its capability. Resolution: either grant render capability (Bash + mmdc) so the claim becomes true, or weaken the claim to scope-honest language ("syntactic shape conforms to Mermaid mindmap directive structure").

---

## Steps to Reproduce

1. Dispatch `ts-mindmap-mermaid` agent to regenerate `mindmap.mmd` from current packet state.
2. Agent self-reports `"Mermaid syntax: Valid"` in its return summary.
3. Local validation via `mmdc` shows the file does not render (BUG-006 manifests).

---

## Root Cause

`ts-mindmap-mermaid` claims syntax validity based on **textual inspection of its own output** (root `((...))`, indentation, no obviously-wrong constructs). The agent has only `Read, Write, Glob` tools per its agent definition — **it cannot actually render** to verify.

Per Jerry's P-022 (no deception): an agent must not misrepresent capabilities, confidence levels, or actions taken. The current self-claim violates P-022.

---

## Resolution Options

Per audit:

| Option | Description |
|--------|-------------|
| **A — Grant render capability** | Add `Bash` tool + add `mmdc` to environment. Agent actually invokes `mmdc` and reports verified result. Honest claim, real work. |
| **B — Weaken the claim** | Remove the "syntax validity" claim from agent return. Replace with scope-honest language: *"syntactic shape conforms to Mermaid mindmap directive structure"* — describes what the agent can actually verify (textual conformance) without overclaiming. |

Decision: pick one in this Bug. Audit recommends Option A if `mmdc` is acceptable as a tool dependency, Option B otherwise.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-reviewer` | Capability decision: Option A (grant Bash + mmdc) vs Option B (weaken claim to scope-honest language). Decision recorded as DEC. |
| 2 | `/eng-team` | `eng-backend` | If Option A: update agent definition to add Bash tool; agent invokes mmdc and reports verified result. If Option B: update agent prompt to remove false syntax-validity claim. |
| 3 | `/eng-team` | `eng-qa` | Regression: agent on BUG-006 audit packet — correctly identifies failure (Option A) or doesn't make false claim (Option B) |
| 4 | `/eng-team` | `eng-reviewer` | P-022 alignment review: agent's claims accurately reflect actual capability |
| 5 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 6 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] Decision recorded: Option A or Option B (with rationale).
- [ ] If Option A: `ts-mindmap-mermaid` agent definition updated to add Bash + mmdc; agent invokes `mmdc` and reports verified result. Test confirms agent correctly identifies BUG-006-class failures.
- [ ] If Option B: agent prompt updated to remove "syntax validity" claim; replaced with scope-honest language. Agent return contract documented.
- [ ] P-022 alignment: agent's claims accurately reflect its actual capability.
- [ ] Regression test: agent behavior on the BUG-006 audit packet — either correctly identifies failure (Option A) or doesn't make a false claim (Option B).
- [ ] `/eng-team` `eng-reviewer` confirms agent definition matches actual capability.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-005](../FEAT-005-mindmap-hardening.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Cooperates | BUG-006 | Same agent; bracket fix and capability decision can ship together |

### Source

- [#273 comment 3](https://github.com/geekatron/jerry/issues/273#issuecomment-4339778594)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Bug created. P-022 violation in current agent self-claim. Two resolution options surfaced. |

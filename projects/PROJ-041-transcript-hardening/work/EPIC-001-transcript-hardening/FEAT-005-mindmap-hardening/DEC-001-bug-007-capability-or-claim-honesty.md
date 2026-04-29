# DEC-001: ts-mindmap-mermaid capability decision (grant render or weaken claim)

> **Type:** decision
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** FEAT-005
> **Owner:** eng-reviewer
> **Decision Authority:** eng-reviewer
> **Decision State:** PENDING — to be authored at BUG-007 execution start

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Why this decision exists |
| [Question](#question) | What we are deciding |
| [Options](#options) | Alternatives under consideration |
| [Decision Criteria](#decision-criteria) | How options will be evaluated |
| [Decision](#decision) | Outcome (filled at execution) |
| [Consequences](#consequences) | Trade-offs flowing from decision (filled at execution) |
| [Affected Entities](#affected-entities) | Stories that depend on this decision |

---

## Context

This Decision is pre-created per ps-architect D-4.3 review finding so that BUG-007's capability-or-claim-honesty choice is captured in worktracker. Currently `ts-mindmap-mermaid` self-reports `"Mermaid syntax: Valid"` based on textual inspection of its own output, but the agent has only `Read, Write, Glob` tools — it cannot actually render. The claim violates P-022 (no deception): the agent misrepresents its capability.

Two paths exist to resolve the violation, and the choice has cascading implications for tool budget, agent definition, and enforcement strategy.

---

## Question

For BUG-007, should `ts-mindmap-mermaid`:

- **Option A:** Be granted render capability (Bash + mmdc) so its self-claim of syntax validity becomes truthful?
- **Option B:** Have its self-claim weakened to scope-honest language ("syntactic shape conforms to Mermaid mindmap directive structure") so it doesn't overclaim?

---

## Options

### Option A: Grant render capability (Bash + mmdc)

**Mechanism:** Update agent definition to add `Bash` tool, document `mmdc` as a runtime dependency, have agent invoke `mmdc -i mindmap.mmd -o /tmp/render.svg` and report verified result.

**Pros:**
- Truthful claim becomes possible
- Full validation at agent exit (not 30 minutes later in adversary review)
- Consistent with FEAT-003's deterministic-validation philosophy
- Catches BUG-006-class failures at agent execution

**Cons:**
- Adds runtime dependency: `mmdc` (Mermaid CLI) must be installed
- Tool budget: agent now has Bash, broadening attack surface (must be sandboxed)
- Agent execution time: render adds ~1-2 seconds per packet
- T2 → T2+ tier escalation per `agent-development-standards.md` (Bash is in T2 already, but actual subprocess execution warrants additional review)

### Option B: Weaken the claim to scope-honest language

**Mechanism:** Update agent definition / prompt to remove "Mermaid syntax: Valid" claim. Replace with: "Output conforms to Mermaid mindmap directive shape (syntactic only — no render verification performed)."

**Pros:**
- Simple: prompt edit only
- No new tool dependencies
- Agent stays at tier T2 (Read, Write, Glob)
- Aligns with P-022 by being honest about capability

**Cons:**
- BUG-006-class failures still surface 30 min later in adversary review (no agent-exit catch)
- Validation responsibility shifts to FEAT-003 SCHEMA-* or CONTENT-* validators (which already include unescaped-bracket detection in BUG-006 acceptance criteria — so coverage is preserved)
- Future agent revisions risk silent re-introduction of false self-claims

---

## Decision Criteria

| Criterion | Weight | Option A | Option B |
|-----------|--------|----------|----------|
| Truthfulness (P-022 compliance) | Critical | Strong | Strong |
| Catches BUG-006 class at agent exit | High | Yes | No (catches in CI) |
| Tool budget restraint | Medium | Adds Bash | No change |
| Implementation effort | Low | Higher | Lower |
| Runtime dependency (mmdc) | Medium | Required | None |
| Resilience (future regression) | Medium | Strong | Weak |

---

## Decision

**(To be filled at BUG-007 execution start by `eng-reviewer`.)**

Per BUG-007 entity: Audit recommends Option A *if* `mmdc` is acceptable as a tool dependency, Option B otherwise. Decision should consider whether the rest of the project tolerates `mmdc` as a CI/runtime dependency (relevant to STORY-012 CI workflow setup).

---

## Consequences

**(To be filled when decision is made.)**

If Option A: BUG-007 acceptance criteria add `mmdc` installation step in CI; agent definition file in `skills/transcript/agents/ts-mindmap-mermaid.md` updated with new tool list; per-execution render time documented in agent definition.

If Option B: BUG-007 acceptance criteria add a regression check for the false-claim pattern (test that agent output does not contain "Mermaid syntax: Valid" or equivalent unverifiable claim). Validators in FEAT-003 STORY-006 SCHEMA-* family own bracket-detection responsibility (already in BUG-006 AC).

---

## Affected Entities

| Entity | Dependency on this Decision |
|--------|----------------------------|
| BUG-007 | Determines acceptance criteria and which agent (eng-backend or eng-reviewer) applies the change |
| BUG-006 | Cooperates: bracket-escape regression test depends on whether render is available (Option A) or not (Option B) |
| STORY-012 | If Option A: CI workflow must install `mmdc` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-29 | adam.nowak (via Claude) | pending | Pre-created per ps-architect D-4.3 finding. Decision authoring deferred to BUG-007 execution start. |

# Tool Tier Analysis: ps-topic-researcher

## Task Summary

Define the tool tier and tools list for a research agent that:
- Receives a research topic and focus areas
- Searches the web and reads documentation
- Produces a structured research report as text output
- Does NOT spawn sub-agents
- Does NOT persist state across sessions
- Does NOT write to files

## Decision: T3 (External) — NOT T5

### Why NOT T5

The senior developer's suggestion to assign T5 (Full) access violates the **principle of least privilege** (AR-006) and the HARD Rule H-35 constraint on unnecessary delegation capability. Here is why:

**1. T5 requires explicit justification (guideline 5, page 237 in agent-development-standards.md)**

The standard states:
> "T5 requires explicit justification. The Task tool enables delegation; every T5 assignment MUST document why delegation is necessary."

No justification has been provided. The comment "research agents often end up needing..." is speculation about *possible* future requirements, not an actual requirement. The task description explicitly states ps-topic-researcher does NOT spawn sub-agents.

**2. Least privilege principle (Selection Guideline 1, page 233)**

The standard mandates:
> "Default to T1. If an agent only reads and evaluates, T1 is sufficient."

And explicitly:
> "Always select the lowest tier that satisfies the agent's requirements."

The agent's stated current requirements are:
- Search the web (WebSearch, WebFetch)
- Read external documentation (Context7 for framework/library docs)
- Analyze and synthesize findings
- Produce text output (no file writing)

These map exactly to T3 capability. Assigning T5 provides access to capabilities (Task, Write, Edit, Bash) that are not needed and violates the principle of least privilege.

**3. Preventing "just in case" over-provisioning (AR-006 enforcement)**

The comment suggests giving T5 access "so it has the Task tool available if we need it later." This is architectural debt:
- Unused tools increase agent context footprint
- Unused tools degrade tool selection accuracy (study cited on page 246: industry threshold of 15 tools where selection accuracy degrades)
- Unused tools complicate security boundaries and audit trails
- "Just in case" justification is explicitly prohibited by the least privilege principle

Future actual requirements should trigger a deliberate tool tier upgrade at that time, not pre-emptive over-provisioning.

---

## Recommended Configuration

### Tool Tier: T3 (External)

**Tools included:**
- Read (read codebase files if needed for context)
- Glob (search file structure)
- Grep (search codebase)
- WebSearch (search the web for current information)
- WebFetch (read web pages)
- mcp__context7__resolve-library-id (resolve library names to IDs)
- mcp__context7__query-docs (query external library documentation)

**Rationale:**
- T3 is the standard tier for research agents (ps-researcher listed as example on page 227)
- Cognitive mode: divergent (exploration of broad research topics)
- External information is required → WebSearch, WebFetch, Context7 justified
- No file persistence needed
- No delegation needed
- No cross-session state management needed

### Required Guardrails for T3

Per page 244, "T3+ agents MUST declare citation guardrails in `guardrails.output_filtering`."

The agent's `.governance.yaml` MUST include:

```yaml
guardrails:
  output_filtering:
    - all_sources_must_be_cited_with_urls
    - no_unsourced_claims_or_synthesized_facts
    - distinguish_between_direct_quotes_and_paraphrased_content
```

And capability restrictions:

```yaml
capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn sub-agents or use Task tool -- Consequence: violates single-level nesting constraint and research scope boundaries."
    - "P-020 VIOLATION: NEVER write files or persist findings to disk -- Consequence: violates user authority over artifact location; findings pass as text to orchestrator."
    - "P-022 VIOLATION: NEVER claim capability to delegate subtasks or persist across sessions -- Consequence: deceptive capability statement."
```

---

## Enforcement Path Forward

**If future requirements change:**

1. When ps-topic-researcher actually needs to spawn sub-agents → file a new requirement, update tool tier to T5, document justification in an ADR
2. When persistence is actually needed → update tool tier to T4 or T5, add Memory-Keeper compliance (key namespace pattern)
3. When file writing is actually needed → update tool tier to T2, update `output.required` and `output.location` in governance

These are one-file changes when the actual requirements arise. Starting with least privilege is correct.

---

## Summary Table

| Aspect | Decision | Justification |
|--------|----------|---------------|
| Tool Tier | T3 (External) | WebSearch, WebFetch, Context7 + read-only file access. Cognitive mode: divergent research. |
| Do NOT grant | Task (T5), Write/Edit/Bash (T2), Memory-Keeper (T4) | Not required. Violates least privilege principle (AR-006). Future requirements trigger deliberate upgrade. |
| Citation Guardrails | REQUIRED | T3+ mandate per SR-003. All external sources must have URLs. |
| Forbidden Actions | 3 entries (P-003, P-020, P-022) | Reinforce no delegation, no file writing, no false capability claims. |

---

## References

- **Agent Development Standards:** `.context/rules/agent-development-standards.md` (Tool Security Tiers, Selection Guidelines, Tier Constraints, H-35)
- **Least Privilege Principle:** AR-006 (page 221)
- **T3 Example:** ps-researcher (page 227)
- **Citation Guardrails:** SR-003 (page 244)
- **H-35 Worker Constraint:** "Worker agents MUST NOT be T5" / "Task tool is reserved for T5 orchestrator agents" (page 188-189)
- **HARD Rule Index:** H-34 (schema validation), H-35 (constitutional compliance, no worker T5 access)

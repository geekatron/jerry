# How to Update Your Agent's Tier After the Renumbering

> Update your agent's `.governance.yaml` to reflect the new T1-T5 tier model.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prerequisites](#prerequisites) | What you need before starting |
| [Quick Reference](#quick-reference) | Old tier to new tier mapping |
| [Scenario 1: T3 External to T4 External](#scenario-1-t3-external-to-t4-external) | Web-only agents (49 agents) |
| [Scenario 2: T4 Persistent to T3 Persistent](#scenario-2-t4-persistent-to-t3-persistent) | MK-only agents (2 agents) |
| [Scenario 3: No File Change Required](#scenario-3-no-file-change-required) | T1, T2, old T4+Web, old T5 |
| [Verification](#verification) | Confirm the change is correct |
| [Rollback](#rollback) | Revert with git checkout |
| [Troubleshooting](#troubleshooting) | Common problems and fixes |
| [Glossary](#glossary) | Term definitions |

---

## Prerequisites

1. Read the [Tier Model Options Explainer](../STORY-015-tier-model-renumbering/tier-model-options-explainer.md) (Option A) for background on why tiers changed.
2. Read the [Tool Security Tiers](../../../../../.context/rules/agent-development-standards.md#tool-security-tiers) section in `agent-development-standards.md` for the new canonical definitions.
3. Identify which `.governance.yaml` file corresponds to your agent.

---

## Quick Reference

| Old Tier | Old Name | New Tier | New Name | Action |
|----------|----------|----------|----------|--------|
| T1 | Read-Only | T1 | Read-Only | No action |
| T2 | Read-Write | T2 | Read-Write | No action |
| T3 | External (Web) | **T4** | External | Update `tool_tier: T4` |
| T4 | Persistent (MK only) | **T3** | Persistent | Update `tool_tier: T3` |
| T4 | Persistent (MK + Web) | T4 | External | No action (number unchanged) |
| T5 | Full | T5 | Orchestration | No action (number unchanged) |

---

## Scenario 1: T3 External to T4 External

Applies to: 49 agents with web tools (WebSearch, WebFetch, Context7) but no Memory-Keeper. Includes all `eng-*`, `red-*`, and web-only `ps-*` agents.

1. Open your agent's `.governance.yaml` file.
2. Find the `tool_tier` field.
3. Change `tool_tier: T3` to `tool_tier: T4`.
4. Save the file. No other changes are needed -- the `.md` frontmatter `tools` field is unchanged.

## Scenario 2: T4 Persistent to T3 Persistent

Applies to: 2 agents with Memory-Keeper but no web tools (`ts-parser`, `ts-extractor`).

1. Open your agent's `.governance.yaml` file.
2. Find the `tool_tier` field.
3. Change `tool_tier: T4` to `tool_tier: T3`.
4. Save the file. No other changes are needed.

## Scenario 3: No File Change Required

Applies to: T1 agents, T2 agents, old T4 agents with both MK and web tools, and old T5 orchestrators.

1. Confirm your agent's current tier using the [Quick Reference](#quick-reference) table.
2. If the "Action" column says "No action," you are done. The tier number is either unchanged or the number stayed the same while the definition changed. No file edits are needed.

---

## Verification

Run these commands from the repository root to confirm correctness.

List all agents still declared as old T3 (should return zero after migration):

```bash
grep -rn 'tool_tier: T3' skills/*/agents/*.governance.yaml | grep -v 'Memory-Keeper\|persistent'
```

List all T4 agents and confirm each has web tools or both web and MK:

```bash
grep -rn 'tool_tier: T4' skills/*/agents/*.governance.yaml
```

List all T3 agents and confirm each has MK but no web tools:

```bash
grep -rn 'tool_tier: T3' skills/*/agents/*.governance.yaml
```

---

## Rollback

Revert a single governance file to its pre-migration state:

```bash
git checkout HEAD~1 -- skills/<skill>/agents/<agent>.governance.yaml
```

Revert all governance files at once:

```bash
git checkout HEAD~1 -- skills/*/agents/*.governance.yaml
```

---

## Troubleshooting

**"I updated `.governance.yaml` but not the `.md` file."**
Correct -- the `.md` file does not need updating. The `tools` frontmatter field lists actual tools and is unchanged by the renumbering. Only `tool_tier` in `.governance.yaml` changes.

**"My agent failed schema validation after updating."**
Check that `tool_tier` is one of: `T1`, `T2`, `T3`, `T4`, `T5`. Values like `T3_HOLD`, `T3-Persistent`, or lowercase `t3` are not valid enum values in the governance schema.

**"I author an `eng-*` or `red-*` agent. Can I add Memory-Keeper now that my tier ceiling allows it?"**
No. P-002 (engagement-scoped output) requires these agents to persist output within engagement directories, not cross-session MCP state. The T4 tier ceiling permits MK at the schema level, but P-002 prohibits it at the governance level.

---

## Glossary

| Term | Definition |
|------|-----------|
| Short Name | The `T1`-`T5` label in `tool_tier` |
| Full Name | The human-readable tier name (Read-Only, Read-Write, Persistent, External, Orchestration) |
| MK | Memory-Keeper -- the MCP server for cross-session state persistence |
| Tier ceiling | The maximum tool set a tier permits, regardless of what an agent actually uses |
| Engagement-scoped output | Output stored within the engagement directory (P-002), not in cross-session MCP state |

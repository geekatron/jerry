# How to register a new skill in the Jerry Framework

> Register a skill so it triggers automatically on matching keywords and appears in the skill catalog.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (H-01 through H-07) -->
<!-- Anti-patterns to avoid: HAP-01 (conflating with tutorial), HAP-04 (completeness over focus -- one real-world variation satisfies H-03 without triggering HAP-04) -->
<!-- Voice: Direct, action-oriented, efficient. No explanatory paragraphs between steps. See Section 5. -->
<!-- H-02/H-03 compatibility: Conditional branches ("If you need X, do Y") are action content, not explanation. -->

## Before You Begin

You need:
- A completed skill directory with a valid `SKILL.md` (frontmatter includes `name`, `description`, `activation-keywords`)
- Write access to `CLAUDE.md`, `AGENTS.md`, and `.context/rules/mandatory-skill-usage.md`

## Steps

### 1. Add the skill to the CLAUDE.md skills table

Open `CLAUDE.md` and locate the `Skills` table under `Quick Reference`. Add a row with the skill's slash-command name and a one-sentence purpose:

```markdown
| `/your-skill` | One-sentence description of what the skill does |
```

### 2. Register agents in AGENTS.md

Open `AGENTS.md` and add one entry per agent defined in `skills/your-skill/agents/`:

```markdown
| `your-skill-agent` | Role description | `sonnet` | `skills/your-skill/agents/your-skill-agent.md` |
```

If you have multiple agents, add each on its own row. Keep alphabetical order within the skill group.

### 3. Add trigger keywords to the mandatory-skill-usage.md trigger map

Open `.context/rules/mandatory-skill-usage.md` and add a row to the Trigger Map table using the 5-column format:

```markdown
| keyword1, keyword2, keyword3 | negative-keyword1, negative-keyword2 | 8 | -- | `/your-skill` |
```

If you need compound triggers for multi-word phrases:

```markdown
| keyword1, keyword2, write docs | negative-keyword1 | 8 | "write docs" (phrase match) | `/your-skill` |
```

<!-- HAP-04 guard: Include at most one "If you need X, do Y" conditional per step. Additional conditionals suggest the step should be split or the variations documented in separate guides. -->

### 4. Mirror the trigger map entry in agent-routing-standards.md

Open `.context/rules/agent-routing-standards.md` and add the same entry to the Reference Trigger Map table. The two tables must stay synchronized.

```markdown
| keyword1, keyword2, keyword3 | negative-keyword1, negative-keyword2 | 8 | -- | `/your-skill` |
```

<!-- HAP-04 guard: Include at most one "If you need X, do Y" conditional per step. Additional conditionals suggest the step should be split or the variations documented in separate guides. -->

## Verification

Confirm the registration is complete:

```bash
grep -c "your-skill" CLAUDE.md AGENTS.md .context/rules/mandatory-skill-usage.md .context/rules/agent-routing-standards.md
```

Expected result: Each file reports at least 1 match (4 files total, all with count >= 1).

## Troubleshooting

**Problem:** Skill does not trigger on keywords after registration.
**Solution:** Verify the `activation-keywords` array in `SKILL.md` matches the keywords in `mandatory-skill-usage.md`. Restart the Claude Code session -- skills are loaded at session start.

**Problem:** Agent invocation fails with "unknown agent" error.
**Solution:** Confirm the agent's `name` field in the `.md` frontmatter matches the entry in `AGENTS.md`. Verify the file path in `AGENTS.md` points to the correct location.

## Related

- **Tutorial:** [Learn to create a Jerry skill](tutorial-create-jerry-skill.md) -- If you are new to skill development
- **Reference:** [Diataxis Quality Criteria Reference](reference-diataxis-criteria.md) -- Full parameter and option details
- **Explanation:** [About Jerry's Context Rot Problem](explanation-context-rot.md) -- Why skill architecture works this way

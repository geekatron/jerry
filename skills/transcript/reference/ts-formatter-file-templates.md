# ts-formatter File Templates Reference

> Golden templates for packet file generation per ADR-007 and PAT-005 (Versioned Schema).
> All generated files MUST include schema version metadata in YAML frontmatter.

---

## 00-index.md Template

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_TIMESTAMP}"
---

# {title}

> **Transcript ID:** {packet_id}
> **Date:** {date}
> **Duration:** {duration}
> **Speakers:** {speaker_count}

## Quick Stats

| Metric | Count |
|--------|-------|
| Action Items | {action_count} |
| Decisions | {decision_count} |
| Open Questions | {question_count} |
| Topics | {topic_count} |

## Navigation

- [Summary](./01-summary.md)
- [Full Transcript](./02-transcript.md)
- [Speakers](./03-speakers.md)
- [Action Items](./04-action-items.md)
- [Decisions](./05-decisions.md)
- [Questions](./06-questions.md)
- [Topics](./07-topics.md)

<backlinks>
<!-- Auto-generated backlinks -->
</backlinks>
```

## Entity File Template (04-action-items.md example)

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_TIMESTAMP}"
---

# Action Items

> **Extracted from:** [{packet_id}](./00-index.md)
> **Total:** {count}
> **High Confidence (>0.85):** {high_conf_count}

## Action Items

### {#act-001} {action_text}

- **Assignee:** [{assignee}](./03-speakers.md#{speaker_anchor})
- **Due Date:** {due_date}
- **Confidence:** {confidence}
- **Source:** [{source_text}](./02-transcript.md#{segment_anchor})

<backlinks>
- Referenced from: [02-transcript.md#seg-042](./02-transcript.md#seg-042)
</backlinks>

---
```

## Split File Template

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_TIMESTAMP}"
---

# {title} (Part {n} of {total})

> **Continued from:** [{prev_file}](./{prev_file})
> **Next part:** [{next_file}](./{next_file})
> **Anchor Registry:** [_anchors.json](./_anchors.json)

---

{content}

---

## Navigation

- <- Previous: [{prev_file}](./{prev_file})
- -> Next: [{next_file}](./{next_file})
- Up Index: [00-index.md](./00-index.md)
```

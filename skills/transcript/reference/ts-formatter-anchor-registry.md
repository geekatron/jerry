# ts-formatter Anchor Registry and Linking Reference

> Anchor registry management (ADR-003), token counting/file splitting (ADR-004),
> backlinks generation, and post-generation validation checklist.

---

## Token Counting and File Splitting (ADR-004)

```
TOKEN COUNTING ALGORITHM:
1. Count words: split on whitespace
2. Estimate tokens: words x 1.3 x 1.1 (10% buffer)
3. Track cumulative tokens during generation

SPLIT DECISION:
tokens < 31,500 (soft limit)  -> NO SPLIT
31,500 <= tokens < 35,000     -> SPLIT at ## heading
tokens >= 35,000 (hard limit) -> FORCE SPLIT

SPLIT IMPLEMENTATION:
1. Find nearest ## heading BEFORE soft limit
2. Create continuation file: 02-transcript-01.md, 02-transcript-02.md
3. Add navigation header to each split file:
   - "Continued from: [previous-file]"
   - "Next: [next-file]"
   - "Index: [00-index.md]"
```

## Anchor Registry Management (ADR-003)

```
ANCHOR ID FORMATS:
- Segments:  seg-{NNN}    (seg-001, seg-042)
- Speakers:  spk-{name}   (spk-alice, spk-bob-smith)
- Actions:   act-{NNN}    (act-001, act-002)
- Decisions: dec-{NNN}    (dec-001, dec-002)
- Questions: que-{NNN}    (que-001, que-002)
- Topics:    top-{NNN}    (top-001, top-002)

REGISTRY STRUCTURE (_anchors.json):
{
  "packet_id": "{id}",
  "version": "1.0",
  "anchors": [
    {
      "id": "seg-042",
      "type": "segment",
      "file": "02-transcript.md",
      "line": 156
    }
  ],
  "backlinks": {
    "spk-alice": [
      {"file": "02-transcript.md", "line": 42, "context": "Alice: Good morning"},
      {"file": "04-action-items.md", "line": 12, "context": "Assigned to Alice"}
    ]
  }
}
```

## Backlinks Generation

```
BACKLINKS SECTION FORMAT:

<backlinks>
Referenced in:
- [02-transcript.md#seg-042](./02-transcript.md#seg-042) - "Alice mentioned..."
- [04-action-items.md#act-001](./04-action-items.md#act-001) - "Action assigned to..."
</backlinks>

GENERATION ALGORITHM:
1. During transcript formatting, scan for entity references
2. For each reference found, add to backlinks registry
3. After all files generated, inject backlinks sections
```

## Post-Generation Validation Checklist

```
FILE VALIDATION:
[ ] 00-index.md exists
[ ] 01-summary.md exists
[ ] 02-transcript.md (or split files) exist
[ ] 03-speakers.md exists
[ ] 04-action-items.md exists
[ ] 05-decisions.md exists
[ ] 06-questions.md exists
[ ] 07-topics.md exists
[ ] _anchors.json exists

TOKEN VALIDATION:
[ ] All files < 35,000 tokens
[ ] Split files at semantic boundaries

LINK VALIDATION:
[ ] All internal links resolve
[ ] All anchor IDs unique
[ ] All backlinks point to existing anchors

NAVIGATION VALIDATION:
[ ] Index links to all files
[ ] Split files have prev/next navigation
[ ] Each entity file links to source
```

# ADR-003 Research: Bidirectional Deep Linking

> **PS ID:** en004-adr-20260126-001
> **Entry ID:** research-003
> **Agent:** ps-researcher
> **Created:** 2026-01-26
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

**The Question:** How should transcript artifacts link to each other and back to the source transcript?

**Key Finding:** Use **standard Markdown links with auto-generated anchors** following GitHub/GitLab conventions. Backlinks should be **explicit (manually maintained)** rather than auto-generated, with a dedicated `## Backlinks` section at the end of each artifact.

**Why This Matters:**
- Forward links let readers navigate from a summary to detailed sections
- Backlinks let readers discover where an entity is referenced
- Anchors enable deep linking to specific items (speakers, topics, action items)
- Consistent linking enables traceability required by FR-014 and NFR-010

**Bottom Line:** Adopt GitHub-style markdown links with slugified heading anchors. Use `{#custom-anchor}` syntax for non-heading elements. Maintain explicit backlinks in a dedicated section.

---

## L1: Technical Research Findings (Software Engineer)

### 1. Industry Linking Patterns Analysis

#### 1.1 Obsidian/Roam Research-Style Backlinks

**Source:** [Obsidian Backlinks Help](https://help.obsidian.md/plugins/backlinks)

| Feature | Obsidian | Roam Research | Logseq |
|---------|----------|---------------|--------|
| Link Syntax | `[[Page Name]]` | `[[Page Name]]` | `[[Page Name]]` |
| Automatic Backlinks | YES | YES | YES |
| Graph Visualization | YES | YES | YES |
| Block-Level Links | YES (with `^`) | YES | YES |
| Cross-File | YES | YES | YES |

**Key Insight:** These tools auto-generate backlinks at runtime, which requires a database index. For static Markdown files, we need explicit backlinks.

#### 1.2 GitHub/GitLab Markdown Linking

**Source:** [GitHub Markdown Heading Anchors](https://gist.github.com/asabaylus/3071099), [GitLab Handbook](https://handbook.gitlab.com/docs/markdown-guide/)

**Auto-generated Anchor Rules:**
1. Convert heading text to lowercase
2. Replace spaces with hyphens (`-`)
3. Remove special characters except `-` and `_`
4. Handle duplicates with `-1`, `-2` suffix

**Examples:**
```markdown
## Hello World           → #hello-world
## Hello *World* (foo)   → #hello-world-foo
## 日本語                → #日本語 (Unicode preserved in some parsers)
## Hello World (duplicate) → #hello-world-1
```

#### 1.3 Zettelkasten Methodology

**Source:** [Zettelkasten Forum](https://forum.zettelkasten.de/discussion/1452/how-should-be-the-zettels-connected-in-terms-of-their-direction)

**Key Principles:**
1. **Forward Links** are intentional—author places them with context
2. **Backlinks** are discovered—help find where a note is referenced
3. **Explicit over automatic**: "Backlinks are cheap because they get generated automatically. If you place forward links in a decent context, backlinks will help you assess the references."
4. **Bidirectional thinking**: A→B implies B←A relationship exists

**Implication:** Forward links should be curated (high quality), backlinks should be comprehensive (show all references).

### 2. Requirements Traceability

#### 2.1 From EN-003 Requirements

| Requirement | Description | Link Implication |
|-------------|-------------|------------------|
| FR-014 | Source transcript citations for all extracted entities | Forward links to transcript |
| NFR-010 | LLM extractions include source transcript span citations | Anchor to specific spans |
| DEC-004 | Bidirectional linking with backlinks | Both directions supported |
| PAT-004 | Citation-Required Extraction | All outputs trace to source |

#### 2.2 From ADR-002 Artifact Structure

The hierarchical packet structure defines:
```
{session-id}-transcript-output/
├── 00-index.md              ← Master navigation hub
├── 01-summary.md            ← Links to details
├── 02-speakers/speakers.md  ← Links to timeline
├── 03-topics/topics.md      ← Links to entities
├── 04-entities/             ← Contains cross-references
│   ├── questions.md
│   ├── action-items.md
│   ├── ideas.md
│   └── decisions.md
├── 05-timeline/timeline.md  ← Links to speakers, topics
├── 06-analysis/sentiment.md
├── 07-mindmap/mindmap.mmd
└── 08-workitems/suggested-tasks.md
```

**Cross-File Link Scenarios:**
1. `00-index.md` → All other files (master index)
2. `01-summary.md` → `02-speakers/speakers.md#speaker-john-smith` (speaker mentions)
3. `04-entities/action-items.md` → `05-timeline/timeline.md#segment-001` (when action was mentioned)
4. `03-topics/topics.md#topic-001` ← backlink from `04-entities/decisions.md#decision-001`

### 3. Link Format Options

#### 3.1 Option A: Wiki-Style Links

```markdown
[[02-speakers/speakers.md|John Smith]]
[[03-topics/topics.md#topic-001|Project Planning]]
```

**Pros:**
- Familiar to Obsidian/Roam users
- Shorter syntax

**Cons:**
- Not standard Markdown
- Requires custom parser
- Not rendered on GitHub/GitLab

#### 3.2 Option B: Standard Markdown Links (Recommended)

```markdown
[John Smith](./02-speakers/speakers.md#speaker-john-smith)
[Project Planning](./03-topics/topics.md#topic-001)
```

**Pros:**
- Standard Markdown (CommonMark compliant)
- Renders correctly on GitHub/GitLab
- No custom parser needed
- IDE support (VS Code, IntelliJ)

**Cons:**
- Longer syntax
- Manual anchor management

#### 3.3 Option C: Reference-Style Links

```markdown
See [John Smith][speaker-john-smith] mentioned in [Project Planning][topic-001].

[speaker-john-smith]: ./02-speakers/speakers.md#speaker-john-smith
[topic-001]: ./03-topics/topics.md#topic-001
```

**Pros:**
- Clean document body
- Centralized link management
- Easy to update links

**Cons:**
- Links scattered from content
- Reference section required

### 4. Anchor Generation Strategies

#### 4.1 Heading-Based Anchors (Auto-Generated)

```markdown
## Speaker: John Smith
<!-- Auto-generates #speaker-john-smith -->

### Topic 001: Project Planning
<!-- Auto-generates #topic-001-project-planning -->
```

**Algorithm (GitHub-compatible):**
```python
def slugify(text: str) -> str:
    """Generate anchor from heading text."""
    # 1. Convert to lowercase
    slug = text.lower()
    # 2. Remove special characters except letters, numbers, spaces, hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    # 3. Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # 4. Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug
```

#### 4.2 Custom Anchors with Extended Markdown

```markdown
### Topic 001: Project Planning {#topic-001}
<!-- Explicit anchor: #topic-001 -->
```

**Support:**
- GitHub Flavored Markdown: NO
- Kramdown (Jekyll): YES
- Pandoc: YES
- VS Code Preview: NO

**Alternative HTML approach:**
```markdown
<a id="topic-001"></a>
### Topic 001: Project Planning
```

**Support:** Universal (all Markdown parsers)

#### 4.3 Entity-Based Anchor Convention

For the Transcript Skill, define a consistent naming pattern:

| Entity Type | Anchor Pattern | Example |
|-------------|----------------|---------|
| Speaker | `speaker-{slug}` | `#speaker-john-smith` |
| Topic | `topic-{nnn}` | `#topic-001` |
| Action Item | `action-{nnn}` | `#action-001` |
| Question | `question-{nnn}` | `#question-001` |
| Decision | `decision-{nnn}` | `#decision-001` |
| Idea | `idea-{nnn}` | `#idea-001` |
| Timeline Segment | `segment-{nnn}` | `#segment-001` |

### 5. Backlinks Implementation

#### 5.1 Manual Backlinks Section

```markdown
---

## Backlinks

Referenced by:
- [03-topics/topics.md#topic-001](./03-topics/topics.md#topic-001) - "John Smith presented the project planning topic"
- [04-entities/action-items.md#action-003](./04-entities/action-items.md#action-003) - "Assigned to John Smith"
- [05-timeline/timeline.md#segment-012](./05-timeline/timeline.md#segment-012) - "00:12:30 - John Smith begins speaking"
```

**Pros:**
- No tooling required
- Human-readable
- Context preserved

**Cons:**
- Manual maintenance
- Can become stale

#### 5.2 Semi-Automated Backlinks (Output Formatter Generates)

The `output-formatter` agent can track all forward links while generating files and create backlinks sections automatically at the end.

**Process:**
1. Parse all files for forward links
2. Build reverse index: `target → [sources]`
3. Append `## Backlinks` section to each file

#### 5.3 Backlinks Section Structure

```markdown
---

## Backlinks

> This section lists all artifacts that reference this file.

| Source | Context | Link |
|--------|---------|------|
| topics.md | "Topic 001 was presented by..." | [→ topics.md#topic-001](./03-topics/topics.md#topic-001) |
| action-items.md | "Assigned to Speaker" | [→ action-items.md#action-003](./04-entities/action-items.md#action-003) |

---

*Auto-generated by output-formatter agent*
```

---

## L2: Architectural Implications (Principal Architect)

### 6. Strategic Considerations

#### 6.1 Link Integrity

**Challenge:** Broken links degrade user experience and violate FR-014 traceability requirement.

**Mitigation Strategies:**
1. **Relative paths only**: No absolute URLs within packet
2. **Validation step**: Output-formatter validates all links before write
3. **Index as truth**: 00-index.md lists all valid targets

#### 6.2 Evolution and Versioning

**Challenge:** If file structure changes, links break.

**Design Decisions:**
1. **Stable anchor IDs**: Use numbered anchors (topic-001) not content-based
2. **No external links within packet**: All links relative
3. **Version in session ID**: Each packet is immutable once generated

#### 6.3 Performance Considerations

**For Claude Context Window:**
- Each link adds ~50-80 characters
- Backlinks section adds ~200-500 characters per file
- With 10 files, backlinks add ~2K-5K tokens total
- Within 35K per-file budget (ADR-002)

### 7. Trade-Off Analysis

| Factor | Wiki-Style | Standard Markdown | Reference-Style |
|--------|------------|-------------------|-----------------|
| Standards Compliance | LOW | HIGH | HIGH |
| GitHub Rendering | NO | YES | YES |
| Parser Complexity | MEDIUM | NONE | NONE |
| Write Effort | LOW | MEDIUM | HIGH |
| Maintenance | LOW | MEDIUM | HIGH |
| IDE Support | POOR | EXCELLENT | GOOD |

**Recommendation:** Standard Markdown Links (Option B)

### 8. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Broken links from file moves | LOW | MEDIUM | Relative paths + validation |
| Anchor collision (duplicate headings) | LOW | LOW | Use numbered anchors |
| Backlinks section stale | MEDIUM | LOW | Auto-generate during output |
| Custom anchor syntax unsupported | MEDIUM | LOW | Use HTML `<a id="">` fallback |
| Link validation false positives | LOW | LOW | Test corpus validation |

---

## 7. Recommendations for ADR-003

### Primary Recommendation: Standard Markdown with Typed Anchors

**Decision Elements:**
1. **Link Syntax:** Standard Markdown `[text](path#anchor)`
2. **Anchor Generation:** Slugified headings (GitHub-compatible)
3. **Custom Anchors:** HTML `<a id="">` for non-heading elements
4. **Anchor Naming:** Entity-type prefix + numbered ID (e.g., `speaker-001`, `topic-001`)
5. **Backlinks:** Explicit section at file end, auto-generated by output-formatter
6. **Validation:** Link integrity check before file write

### Alternative Options

1. **Option A: Wiki-Style Links** - Familiar but non-standard
2. **Option B: Standard Markdown Links** (recommended) - Universal, validated
3. **Option C: Reference-Style Links** - Clean body but higher maintenance

---

## 8. References

### 8.1 Primary Sources

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 1 | Obsidian Backlinks Documentation | Industry | https://help.obsidian.md/plugins/backlinks |
| 2 | GitHub Markdown Heading Anchors | Industry | https://gist.github.com/asabaylus/3071099 |
| 3 | GitLab Handbook Markdown Guide | Industry | https://handbook.gitlab.com/docs/markdown-guide/ |
| 4 | Zettelkasten Forum - Link Direction | Community | https://forum.zettelkasten.de/discussion/1452 |
| 5 | EN-003 REQUIREMENTS-SPECIFICATION.md | Project | FR-014, NFR-010, PAT-004 |

### 8.2 Secondary Sources

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 6 | Zettelkasten Forum - Backlinks in Action | Community | https://forum.zettelkasten.de/discussion/1487 |
| 7 | Microsoft Learn - Links in Documentation | Industry | https://learn.microsoft.com/en-us/contribute/content/how-to-write-links |
| 8 | Wikipedia - URI Fragment | Reference | https://en.wikipedia.org/wiki/URI_fragment |
| 9 | ADR-002 Artifact Structure | Project | docs/adrs/ADR-002-artifact-structure.md |
| 10 | DEC-004 Bidirectional Linking Decision | Project | EPIC-001-transcript-skill.md |

---

## Document Metadata

| Field | Value |
|-------|-------|
| Document ID | ADR-003-RESEARCH |
| Created | 2026-01-26 |
| Author | ps-researcher agent |
| Status | COMPLETE |
| Word Count | ~2,200 |
| Next Step | ps-architect drafts ADR-003 |

---

*Generated by ps-researcher agent v2.2.0*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*

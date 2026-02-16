# Markdown Navigation Standards

> Navigation table requirements for all Claude-consumed markdown files.

<!-- L2-REINJECT: rank=7, tokens=25, content="Navigation table REQUIRED for Claude-consumed markdown >30 lines (H-23). Section names MUST use anchor links (H-24)." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Navigation constraints H-23, H-24 |
| [Standards (MEDIUM)](#standards-medium) | Placement, format, coverage |
| [Anchor Link Syntax](#anchor-link-syntax) | How to create correct anchors |
| [Table Formats](#table-formats) | Which format to use when |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-23 | All Claude-consumed markdown files over 30 lines MUST include a navigation table (NAV-001). | Document rejected. |
| H-24 | Navigation table section names MUST use anchor links (NAV-006). | Document rejected. |

---

## Standards (MEDIUM)

Override requires documented justification.

| ID | Standard | Guidance |
|----|----------|----------|
| NAV-002 | Placement | Table SHOULD appear after frontmatter, before first content section. |
| NAV-003 | Format | Table SHOULD use markdown table syntax with `\| Section \| Purpose \|` columns. |
| NAV-004 | Coverage | All major sections (`##` headings) SHOULD be listed. |
| NAV-005 | Descriptions | Each entry SHOULD have a purpose/description. |

---

## Anchor Link Syntax

| Rule | Example |
|------|---------|
| Lowercase heading | `Summary` -> `#summary` |
| Replace spaces with hyphens | `Problem Statement` -> `#problem-statement` |
| Remove special characters | `Children (Tasks)` -> `#children-tasks` |

---

## Table Formats

**Format 1: Section Index** (rule files, enablers, general docs):
```markdown
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
```

**Format 2: Triple-Lens** (skills, playbooks serving multiple audiences):
```markdown
| Level | Audience | Sections |
|-------|----------|----------|
| L0 | Stakeholders | [Purpose](#purpose), [When to Use](#when-to-use) |
| L1 | Developers | [Quick Start](#quick-start), [Examples](#examples) |
```

### Exceptions

Navigation tables are NOT required for:
- Files under 30 lines
- Pure data files (YAML, JSON)
- Generated/temporary files

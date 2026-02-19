# Research Page Template

> Template for individual research pages in docs/research/. Used by EN-959 (Tier 1) and EN-960 (Tier 2/3).

---

## Template Structure

```markdown
# [Page Title]

> [1-2 sentence description of this research area]

---

## Key Findings

- **Finding 1:** [concise statement]
- **Finding 2:** [concise statement]
- **Finding 3:** [concise statement]

---

## [Artifact 1 Title]

[2-3 sentence summary of what this artifact covers and why it matters]

??? note "Methodology"
    [Expandable section describing the methodology used — e.g., "This research
    applied FMEA methodology with Severity/Occurrence/Detection scoring across
    21 identified risks..."]

??? abstract "Key Data"
    [Expandable section with key data points, tables, or statistics from the artifact]

[:octicons-link-external-16: Full artifact on GitHub](https://github.com/geekatron/jerry/blob/main/[path])

---

## [Artifact 2 Title]

[Same pattern repeats for each artifact on this page]

---

## Related Research

- [Link to related research page](relative-link.md)
- [Link to related research page](relative-link.md)
```

---

## Design Rules

1. **Key Findings** section is always first after the intro — this is what readers scan
2. **Methodology** goes in collapsible `??? note` admonitions — available but not in the way
3. **Key Data** goes in collapsible `??? abstract` admonitions — tables, statistics, scores
4. **GitHub links** use `:octicons-link-external-16:` icon prefix for visual consistency
5. **Tier 1 pages** get 1-3 artifacts per page (dedicated, detailed)
6. **Tier 2/3 pages** get 3-7 artifacts per page (curated summaries, lighter treatment)
7. All GitHub links point to `main` branch: `https://github.com/geekatron/jerry/blob/main/[path]`

---

## Navigation Structure

```yaml
- Research:
  - Overview: research/index.md
  - Single vs. Multi-Agent Analysis: research/single-vs-multi-agent.md
  - Adversarial Strategy Catalog: research/adversarial-strategy-catalog.md
  - Strategy Selection & Enforcement (ADRs): research/strategy-selection-enforcement.md
  - Adversarial Quality Deep Dives: research/adversarial-deep-dives.md
  - Skill Compliance Framework: research/skill-compliance-framework.md
  - Governance & Constitutional AI: research/governance-constitutional-ai.md
  - Context Management: research/context-management.md
  - OSS Methodology: research/oss-methodology.md
  - Architecture Patterns: research/architecture-patterns.md
  - Claude Code Ecosystem: research/claude-code-ecosystem.md
```

**Total:** 11 pages (1 landing + 5 Tier 1 + 5 Tier 2/3)

---

## MkDocs Configuration Notes

- Remove `research/` from `exclude_docs` in mkdocs.yml
- Add `research/internal/` to `exclude_docs` (internal artifacts relocated there)
- Grid cards on landing page require no extra plugins (built into Material theme)
- Octicons icons require no extra config (bundled with Material)

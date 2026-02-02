# EN-206:SPIKE-001: Research 3-5 Cross-Platform Sync Strategies

<!--
TEMPLATE: Spike
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
CREATED: 2026-02-02 (Claude)
PURPOSE: Timeboxed research on strategies to sync .context/ → .claude/ across platforms
-->

> **Type:** spike
> **Status:** complete
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-02-02T06:30:00Z
> **Due:** 2026-02-05T00:00:00Z
> **Completed:** 2026-02-02T08:00:00Z
> **Parent:** EN-206
> **Owner:** Claude
> **Timebox:** 3 hours
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Research objective - cross-platform sync strategies |
| [Research Questions](#research-questions) | Specific questions to answer |
| [Research Scope](#research-scope) | 3-5 strategies to investigate |
| [Methodology](#methodology) | Using /problem-solving skill |
| [Acceptance Criteria](#acceptance-criteria) | What constitutes done |
| [Output Artifacts](#output-artifacts) | Expected deliverables |

---

## Summary

Timeboxed research spike to investigate **3-5 strategies** for syncing `.context/` (canonical source) to `.claude/rules/` and `.claude/patterns/` (user's project).

**Key Constraint:** Must work on **Windows without admin privileges**. Symlinks on Windows require Developer Mode or admin rights, which many enterprise users don't have.

**Research Focus:**
- Cross-platform portability (macOS, Linux, Windows)
- User experience (setup friction)
- Maintainability (sync drift, updates)
- Enterprise compatibility (no admin required)

---

## Research Questions

### Primary Questions

1. **What are the viable strategies for syncing .context/ → .claude/?**
   - At least 3, up to 5 strategies
   - Each with pros/cons analysis

2. **How does each strategy work on Windows without admin?**
   - Symlinks require Dev Mode/admin
   - What alternatives exist?

3. **What is the user experience for each strategy?**
   - Setup complexity
   - Ongoing maintenance
   - Error recovery

4. **What do other frameworks do?**
   - Industry best practices
   - Prior art from similar projects

### Secondary Questions

5. **How do we handle updates?**
   - When Jerry's rules change, how do users get updates?

6. **How do we detect drift?**
   - If user modifies synced files, how do we handle?

---

## Research Scope

### Strategies to Investigate

| # | Strategy | Platform Support | Admin Required? |
|---|----------|------------------|-----------------|
| 1 | **Symbolic Links** | macOS/Linux native, Windows Dev Mode | Windows: Yes |
| 2 | **Junction Points** | Windows only | No |
| 3 | **File Copy (manual or scripted)** | All platforms | No |
| 4 | **Git Submodules** | All platforms | No |
| 5 | **Bootstrap Script with Detection** | All platforms | No |

### Out of Scope

- Build-time solutions (webpack, rollup)
- Package manager hooks (npm postinstall)
- Docker/container solutions

---

## Methodology

### Use /problem-solving Skill

This spike MUST use the `/problem-solving` skill with:

1. **ps-researcher** - Gather industry best practices, prior art
2. **ps-analyst** - Analyze trade-offs, platform compatibility
3. **ps-synthesizer** - Synthesize recommendation

### Research Sources

- Context7 for Claude Code documentation
- Industry best practices for cross-platform file syncing
- Windows developer documentation
- Other AI framework approaches (Cursor, Windsurf, etc.)

### Frameworks to Apply

- **5W2H** - Complete analysis of each strategy
- **Trade-off Matrix** - Compare strategies across criteria
- **Platform Compatibility Matrix** - Document what works where

---

## Acceptance Criteria

### Definition of Done

- [x] 3-5 strategies documented with pros/cons
- [x] Windows no-admin solution identified
- [x] Platform compatibility matrix complete
- [x] Industry best practices cited
- [x] Recommendation provided with rationale
- [x] Research artifact persisted to repository

### Output Format

Research artifact should include:

1. **Strategy Overview Table**
2. **Detailed Analysis per Strategy**
3. **Platform Compatibility Matrix**
4. **Trade-off Analysis**
5. **Recommendation with Rationale**
6. **References/Citations**

---

## Output Artifacts

| Artifact | Location | Description |
|----------|----------|-------------|
| Research Document | `EN-206/research-sync-strategies.md` | Full research findings |
| Decision Record | `EN-206/DEC-001-sync-strategy-selection.md` | If decision made during spike |

---

## Related Items

### Hierarchy

- **Parent:** [EN-206: Context Distribution Strategy](./EN-206-context-distribution-strategy.md)

### Research Foundation

- [research-plugin-claude-folder-loading.md](../EN-202-claude-md-rewrite/research-plugin-claude-folder-loading.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T08:00:00Z | Claude | complete | Research complete, artifacts created: research-sync-strategies.md, DISC-001, DEC-001 |
| 2026-02-02T06:30:00Z | Claude | pending | Spike created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Task with spike tag |
| **SAFe** | Enabler Story (Exploration) |
| **JIRA** | Task with spike label |

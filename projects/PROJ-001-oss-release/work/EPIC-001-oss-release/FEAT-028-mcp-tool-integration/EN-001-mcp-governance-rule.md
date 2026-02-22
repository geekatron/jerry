# EN-001: MCP Governance Rule File

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-20
> **Completed:** 2026-02-20
> **Parent:** FEAT-028-mcp-tool-integration
> **Owner:** Claude
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Technical Approach](#technical-approach) | Implementation approach |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Delivery evidence |
| [History](#history) | Change log |

---

## Summary

Create `.context/rules/mcp-tool-standards.md` as the SSOT for MCP tool governance. Defines when and how agents should proactively use Context7 (documentation lookup) and Memory-Keeper (cross-session persistence).

## Technical Approach

Completed as part of parent feature. See evidence below.

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | Rule file exists at `.context/rules/mcp-tool-standards.md` | PASS |
| AC-2 | File accessible via `.claude/rules/` symlink | PASS |
| AC-3 | Contains Context7 usage triggers and protocol | PASS |
| AC-4 | Contains Memory-Keeper usage triggers and key patterns | PASS |
| AC-5 | Contains canonical tool names table | PASS |
| AC-6 | Contains agent integration matrix | PASS |
| AC-7 | Passes H-23 (nav table) and H-24 (anchor links) | PASS |

## Evidence

- **Deliverable:** `.context/rules/mcp-tool-standards.md` (~90 lines)
- **Inode verification:** Same inode (51807750) for `.context/rules/` and `.claude/rules/` paths
- **L2-REINJECT tag:** Included at rank 9

## History

| Date | Author | Event |
|------|--------|-------|
| 2026-02-20 | Claude | Created. Rule file written with 4 sections: Context7 Integration, Memory-Keeper Integration, Canonical Tool Names, Agent Integration Matrix. |

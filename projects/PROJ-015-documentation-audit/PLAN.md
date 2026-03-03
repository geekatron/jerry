# PLAN — PROJ-015 Documentation Audit

> User-facing documentation audit using the /diataxis skill to identify quadrant mixing, coverage gaps, and missing documentation for skills and agents.

## Scope

**In scope:**
- Audit existing user-facing docs: BOOTSTRAP.md, INSTALLATION.md, CLAUDE-MD-GUIDE.md, getting-started.md
- Classify all user-facing docs into correct Diataxis quadrants
- Inventory all 15 skills for user-facing documentation presence
- Identify missing documentation types (tutorials, how-to guides, reference docs, explanations)
- Produce prioritized remediation plan

**Out of scope:**
- Writing/rewriting the documentation itself (that's FEAT-015-003, deferred until audit is complete)
- Internal rule files (.context/rules/) — these are reference docs by nature, not user-facing
- Archive docs (docs/archive/)

## Execution

1. TASK-015-001: Run `diataxis-auditor` on the 4 primary user-facing docs
2. TASK-015-002: Run `diataxis-classifier` on each doc to determine correct quadrant
3. TASK-015-003: Inventory all 15 skills — check for tutorials, how-to guides, getting-started docs
4. TASK-015-004: Cross-reference inventory against Diataxis quadrants to identify gaps
5. TASK-015-005: Synthesize into prioritized remediation report

# BUG-008: Transcript Skill Incorrectly Documented as Non-Keyword-Triggerable

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** minor
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-001
> **Owner:** --
> **Found In:** 0.2.3
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

The transcript playbook (`docs/playbooks/transcript.md` lines 24-28) and the `mandatory-skill-usage.md` trigger map incorrectly document the transcript skill as non-keyword-triggerable. The stated rationale cites the Python script dependency as the reason, but the Python parser is only required for VTT files. The LLM instructions (ts-parser agent) automatically run the Python script for VTT and fall back to LLM-based parsing for non-VTT formats (SRT, plain text). The skill should be keyword-triggerable like all other skills.

**Key Details:**
- **Symptom:** Transcript skill excluded from keyword trigger map; playbook explicitly states "NOT triggered by keyword detection" with incorrect Python-dependency rationale
- **Frequency:** Every session where transcript-related keywords are used
- **Workaround:** User must explicitly invoke `/transcript` command

---

## Reproduction Steps

### Prerequisites

- Jerry Framework v0.2.3
- Any active project with `JERRY_PROJECT` set

### Steps to Reproduce

1. Read `docs/playbooks/transcript.md` lines 24-28 — note the claim: "The transcript skill is NOT triggered by keyword detection...This design is intentional — the skill requires a specific input file path that cannot be inferred from keyword context alone."
2. Read `.context/rules/mandatory-skill-usage.md` trigger map — note that every skill has keyword triggers except transcript.
3. Read `skills/transcript/agents/ts-parser.md` — note that Step 2A (Python CLI) is VTT-only, and Step 2B (LLM fallback) handles SRT, plain text, and Python parser failures automatically.

### Expected Result

The transcript skill should have keyword triggers in `mandatory-skill-usage.md` (e.g., "transcript", "meeting notes", "parse recording") consistent with the hybrid architecture where the Python script is only a VTT optimization, not a hard dependency.

### Actual Result

The transcript skill is documented as requiring explicit `/transcript` invocation only, with incorrect rationale that the Python script prevents keyword triggering.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS Darwin 24.6.0 |
| **Application Version** | Jerry Framework 0.2.3 |
| **Configuration** | Default |

---

## Root Cause Analysis

### Root Cause

During FEAT-018 (User Documentation -- Runbooks & Playbooks), the playbook author conflated the VTT-specific Python parser requirement with a general skill invocation constraint. The ts-parser agent's hybrid architecture (Python for VTT, LLM fallback for everything else) was misinterpreted as "Python required for all formats, therefore keyword triggering is impossible."

### Contributing Factors

- The hybrid Python+LLM architecture is complex and easy to misunderstand
- The playbook was authored in a single orchestration pass without verifying the ts-parser agent's actual fallback behavior
- No cross-reference check against ts-parser.md Step 2B (LLM fallback path)

---

## Acceptance Criteria

### Fix Verification

- [ ] AC-1: `docs/playbooks/transcript.md` "When to Use" section updated to remove the incorrect "NOT triggered by keyword detection" claim and Python-dependency rationale
- [ ] AC-2: `.context/rules/mandatory-skill-usage.md` trigger map includes transcript skill with appropriate keywords (e.g., "transcript", "meeting notes", "parse recording", "meeting recording")
- [ ] AC-3: Updated documentation accurately describes the hybrid architecture: Python for VTT (automatic, handled by LLM instructions), LLM fallback for non-VTT
- [ ] AC-4: No regression in other playbook sections or skill documentation

### Quality Checklist

- [ ] Existing documentation structure preserved
- [ ] No new issues introduced
- [ ] Documentation reviewed via /adversary

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../../EPIC-001-oss-release/EPIC-001-oss-release.md)

### Related Items

- **Causing Change:** FEAT-018 (User Documentation -- Runbooks & Playbooks)
- **Affected Files:** `docs/playbooks/transcript.md`, `.context/rules/mandatory-skill-usage.md`
- **Reference:** `skills/transcript/agents/ts-parser.md` (correct architecture)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Initial report — user identified incorrect Python-dependency rationale in transcript skill docs |

---

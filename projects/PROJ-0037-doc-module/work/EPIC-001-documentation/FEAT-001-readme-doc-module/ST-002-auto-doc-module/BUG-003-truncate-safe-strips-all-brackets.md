# BUG-003: truncate_safe macro strips all bracket characters

> **Type:** bug
> **Status:** completed
> **Priority:** low
> **Impact:** low
> **Created:** 2026-03-18T00:00:00Z
> **Due:**
> **Completed:** 2026-03-18T00:00:00Z
> **Parent:** ST-002
> **Severity:** minor
> **Owner:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to trigger the bug |
| [Root Cause](#root-cause) | Why it's broken |
| [Acceptance Criteria](#acceptance-criteria) | How to verify the fix |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

The `truncate_safe` macro in `_macros.jinja2` uses `replace('[', '')` which removes ALL `[` characters from the string, not just the trailing incomplete one left by truncation.

Practical risk is LOW because the guard condition (`'[' in truncated and '](' not in truncated`) prevents the branch from executing when complete markdown links are present. The bug only triggers when there are orphan `[` chars and no complete links — which is the intended case. However, the approach is semantically incorrect and could break if a description contains `[text]` (non-link bracket usage) alongside an orphan `[` from truncation.

---

## Steps to Reproduce

1. Create a skill description containing bracket text and exceeding 60 chars: `"This [important] feature provides [advanced] capabilities for long descriptions that get truncated at the boundary [incomplete"`
2. The truncation cuts at 60 chars, leaving an orphan `[incomplete`
3. Guard condition fires: `[` present, `](` absent
4. `replace('[', '')` strips ALL three `[` chars: `"This important] feature provides advanced] capabilities fo..."`

### Expected Result

Only the trailing incomplete `[incomplete` is removed or handled.

### Actual Result

All `[` characters are stripped, producing broken text with orphan `]` characters.

---

## Root Cause

`_macros.jinja2:30` — Jinja2's `replace` filter has no concept of "last occurrence" or regex. The macro uses a global replace as a workaround for Jinja2's limited string manipulation capabilities.

---

## Acceptance Criteria

- [ ] `truncate_safe` macro correctly handles descriptions with legitimate `[text]` bracket usage
- [ ] Only trailing incomplete link fragments are removed or neutralized
- [ ] Existing tests continue to pass
- [ ] Macro handles edge cases: no brackets, complete links only, orphan brackets only

---

## Related Items

- **Parent:** [ST-002](ST-002-auto-doc-module.md)
- **Found by:** /eng-team security-aware code review (MEDIUM-2 finding)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-18 | Claude | pending | Filed from /eng-team code review MEDIUM-2 finding |
| 2026-03-18 | Claude | completed | Fix: replaced replace('[','') with split/join that drops only trailing orphan bracket. BUG-003 annotation added to macro. /adversary scored, revision applied. 59/59 doc tests pass. |

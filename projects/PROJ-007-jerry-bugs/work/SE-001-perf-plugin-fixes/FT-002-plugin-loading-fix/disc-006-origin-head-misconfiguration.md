# disc-006: Local origin/HEAD Misconfiguration

> **Discovery ID:** disc-006
> **Solution Epic:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** RESOLVED ✅
> **Severity:** Low (cosmetic/convenience)
> **Discovered:** 2026-01-14
> **Discovered By:** Claude (during git configuration review)

---

## Summary

The local git configuration had `origin/HEAD` pointing to `claude/create-code-plugin-skill-MG1nh` instead of `main`, causing potential confusion about the default branch.

---

## Discovery Context

While reviewing git configuration after bot setup, found:

```bash
$ git symbolic-ref refs/remotes/origin/HEAD
refs/remotes/origin/claude/create-code-plugin-skill-MG1nh  # Wrong!
```

GitHub's default branch was correctly set to `main`, but the local reference was stale.

---

## Root Cause

The local `origin/HEAD` reference was set during a previous clone or fetch operation when a different branch was the default, and was never updated.

---

## Impact

| Aspect | Impact |
|--------|--------|
| PR creation | May target wrong branch by default |
| git commands | `origin` without branch may resolve incorrectly |
| Developer confusion | Misleading default branch indication |

---

## Solution

```bash
git remote set-head origin main
```

**Verification:**
```bash
$ git symbolic-ref refs/remotes/origin/HEAD
refs/remotes/origin/main  # Correct!

$ gh api repos/geekatron/jerry --jq '.default_branch'
main  # Matches GitHub
```

---

## Prevention

For future repositories or clones:
```bash
# After clone, ensure HEAD is correct
git remote set-head origin --auto
```

---

## Evidence

| ID | Type | Source | Finding |
|----|------|--------|---------|
| E-001 | Git | `git symbolic-ref` | Was pointing to wrong branch |
| E-002 | API | `gh api repos/.../default_branch` | GitHub correctly set to `main` |
| E-003 | Git | Post-fix verification | Now points to `main` |

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Task | Configuration fix (inline) |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Discovery documented | Claude |
| 2026-01-14 | Fixed immediately | Claude |
| 2026-01-14 | Status: RESOLVED | Claude |

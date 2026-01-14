# disc-005: PR Author Cannot Approve Own PRs

> **Discovery ID:** disc-005
> **Solution Epic:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** RESOLVED ✅
> **Severity:** Medium (workflow blocker)
> **Discovered:** 2026-01-14
> **Discovered By:** Claude (during PR #13 approval attempt)

---

## Summary

GitHub does not allow PR authors to approve their own pull requests. When Claude Code creates commits and PRs using the repository owner's credentials, the owner cannot approve those PRs - they can only comment.

---

## Discovery Context

After creating PR #13 for FT-002, the user (`geekatron`) attempted to approve the PR but could only add comments. Investigation revealed:

```json
{
  "author": {"login": "geekatron"},
  "reviews": [{
    "author": {"login": "geekatron"},
    "state": "COMMENTED"  // Not "APPROVED"
  }]
}
```

**Root Cause:** GitHub's security model prevents self-approval to ensure code review integrity.

---

## Impact

| Aspect | Impact |
|--------|--------|
| Workflow | Blocked PR merges requiring approval |
| Workaround | Merge without approval (if no branch protection) |
| Long-term | Need separate identity for Claude commits |

---

## Solution

**EN-004: Bot Account Setup** - Configure a separate GitHub account (`saucer-boy`) for Claude Code commits.

| Component | Configuration |
|-----------|---------------|
| Bot Account | `saucer-boy` |
| Authentication | SSH key (`~/.ssh/github_saucer_boy`) |
| Git Identity | `saucer-boy` / `254988596+saucer-boy@users.noreply.github.com` |
| Access | Repository collaborator (push) |

**Workflow After Solution:**
1. Claude commits → attributed to `saucer-boy`
2. Claude creates PR → author is `saucer-boy`
3. `geekatron` can approve → not the author
4. Merge proceeds normally

---

## Evidence

| ID | Type | Source | Finding |
|----|------|--------|---------|
| E-001 | API | `gh pr view 13 --json reviews` | Review state: COMMENTED |
| E-002 | Docs | GitHub documentation | Authors cannot approve own PRs |
| E-003 | Test | Commit `96d6c90` | Verified bot commits work |

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Enabler | [EN-004](./en-004-bot-account-setup.md) |
| PR | #13 (first affected PR) |
| Feature | FT-002 (blocked until workaround) |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Discovery documented | Claude |
| 2026-01-14 | Solution implemented via EN-004 | Claude |
| 2026-01-14 | Status: RESOLVED | Claude |

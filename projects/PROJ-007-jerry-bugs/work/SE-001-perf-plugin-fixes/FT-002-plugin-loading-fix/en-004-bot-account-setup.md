# EN-004: Bot Account Setup for PR Approvals

> **Enabler ID:** EN-004
> **Solution Epic:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** COMPLETE ✅
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Objective

Configure a bot GitHub account (`saucer-boy`) to author Claude Code commits, enabling the repository owner (`geekatron`) to approve PRs (GitHub doesn't allow authors to approve their own PRs).

---

## Solution: SSH Key Authentication

### Configuration Summary

| Component | Value |
|-----------|-------|
| Bot Username | `saucer-boy` |
| Bot GitHub ID | `254988596` |
| Bot Email | `254988596+saucer-boy@users.noreply.github.com` |
| SSH Key | `~/.ssh/github_saucer_boy` |
| SSH Host Alias | `github-bot` |
| Repository Access | Collaborator (push) |

### Files Modified

| File | Change |
|------|--------|
| `~/.ssh/config` | Added `github-bot` host entry |
| `~/.ssh/github_saucer_boy` | Private key (generated) |
| `~/.ssh/github_saucer_boy.pub` | Public key (added to bot's GitHub) |
| `.git/config` | `user.name`, `user.email`, remote URL |

### SSH Config Entry

```
Host github-bot
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_saucer_boy
    IdentitiesOnly yes
```

### Git Config (Repository-Local)

```
[user]
    name = saucer-boy
    email = 254988596+saucer-boy@users.noreply.github.com
[remote "origin"]
    url = git@github-bot:geekatron/jerry.git
```

---

## Tasks

| ID | Task | Status |
|----|------|--------|
| T-001 | Generate SSH key for bot | ✅ COMPLETE |
| T-002 | Add public key to bot's GitHub | ✅ COMPLETE |
| T-003 | Configure SSH host alias | ✅ COMPLETE |
| T-004 | Configure git identity | ✅ COMPLETE |
| T-005 | Add bot as collaborator | ✅ COMPLETE |
| T-006 | Test SSH authentication | ✅ COMPLETE |
| T-007 | Test commit and push | ✅ COMPLETE |

---

## Workflow After Setup

1. **Claude Code** makes commits → attributed to `saucer-boy`
2. **Claude Code** creates PRs → author is `saucer-boy`
3. **geekatron** can approve PRs → not the author
4. **geekatron** merges → done

---

## Discovery: disc-005 - PR Author Cannot Approve

**Problem:** GitHub does not allow PR authors to approve their own PRs.

**Impact:** When Claude creates PRs using the user's credentials, the user cannot approve them.

**Solution:** Use a separate bot account for Claude commits/PRs.

---

## Security Considerations

| Aspect | Implementation |
|--------|----------------|
| Authentication | SSH key (no password/PAT stored) |
| Key Storage | User's `~/.ssh/` directory |
| Permissions | Bot has push-only access (not admin) |
| Scope | Repository-specific configuration |

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Discovery | disc-005 (PR author cannot approve) |
| PR | #13 (first PR to test with) |
| Feature | FT-002 (blocked on PR approval) |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | EN-004 created | Claude (as saucer-boy) |
| 2026-01-14 | All tasks completed | Claude (as saucer-boy) |

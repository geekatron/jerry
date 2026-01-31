# FEAT-003:DISC-003: GitHub Dual Identity Management

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-31 per PR identity issue during PR #15 creation
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-31T12:00:00Z
> **Completed:** 2026-01-31T12:30:00Z
> **Parent:** FEAT-003
> **Owner:** Claude
> **Source:** PR #15 creation identity mismatch incident

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# Purpose: Document GitHub dual identity management challenges and solutions
# =============================================================================

# Identity (inherited from WorkItem)
id: "FEAT-003:DISC-003"
work_type: DISCOVERY
title: "GitHub Dual Identity Management"

# Classification
classification: TECHNICAL

# State
status: DOCUMENTED
resolution: null

# Priority
priority: HIGH

# Impact
impact: HIGH

# People
assignee: null
created_by: "Claude"

# Timestamps
created_at: "2026-01-31T12:00:00Z"
updated_at: "2026-01-31T12:30:00Z"
completed_at: "2026-01-31T12:30:00Z"

# Hierarchy
parent_id: "FEAT-003"

# Tags
tags: ["github", "authentication", "workflow", "identity", "gh-cli"]

# =============================================================================
# DISCOVERY-SPECIFIC PROPERTIES
# =============================================================================

# Finding Classification
finding_type: CONSTRAINT
confidence_level: HIGH

# Source Information
source: "PR #15 creation incident - PR created under geekatron instead of saucer-boy"
research_method: "Incident analysis and solution research"

# Validation
validated: true
validation_date: "2026-01-31T12:30:00Z"
validated_by: "user"
```

---

## Summary

When using GitHub CLI (`gh`) and Git SSH with dual identities (personal: geekatron, bot: saucer-boy), authentication mechanisms are separate and require explicit configuration to prevent identity mismatches.

**Key Findings:**
- `gh` CLI and Git SSH use completely separate authentication mechanisms
- `gh auth switch` (since late 2023) enables multi-account support for `gh` CLI
- SSH Host Aliases (e.g., `github-bot`) only affect Git operations, not `gh` CLI operations
- Per-project identity automation requires either direnv+GH_TOKEN or GH_CONFIG_DIR strategies

**Validation:** User confirmed the issue and requested solution implementation

---

## Context

### Background

The Jerry project uses two GitHub identities:
1. **geekatron** - Personal developer account for primary work
2. **saucer-boy** - Bot account for CI/CD and automated PR creation

During PR #15 creation for `feat/008-transcript-skill`, the PR was created under the geekatron identity instead of saucer-boy. This prevented the user from approving their own PR.

### Research Question

How can we reliably manage dual GitHub identities to ensure:
1. Git operations (push/pull) use the correct SSH key
2. GitHub CLI operations (PR creation, issue management) use the correct account
3. Switching between identities is automated or at least streamlined

### Investigation Approach

1. Analyzed the difference between `gh` CLI authentication and Git SSH authentication
2. Researched `gh auth` multi-account support (added late 2023)
3. Evaluated automation strategies (direnv, GH_CONFIG_DIR, etc.)
4. Compared approaches using weighted decision matrix

---

## Finding

### Authentication Mechanism Separation

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Operations                             │
├──────────────────────────┬──────────────────────────────────────┤
│      Git Operations      │         gh CLI Operations            │
│                          │                                      │
│  • git push/pull/fetch   │  • gh pr create/view/merge           │
│  • git clone             │  • gh issue create/list              │
│                          │  • gh api                            │
├──────────────────────────┼──────────────────────────────────────┤
│  Uses: SSH Keys          │  Uses: OAuth Tokens                  │
│  Config: ~/.ssh/config   │  Config: ~/.config/gh/hosts.yml      │
│  Selection: Remote URL   │  Selection: gh auth status           │
│  Host Alias: github-bot  │  Account: gh auth switch             │
└──────────────────────────┴──────────────────────────────────────┘
```

**Key Observation:** SSH Host Aliases (`Host github-bot` in `~/.ssh/config`) ONLY affect Git operations. The `gh` CLI completely ignores this and uses its own OAuth token-based authentication.

### Strategy Evaluation Matrix

| Criteria (Weight) | Multi-Account `gh auth switch` | direnv + GH_TOKEN | GH_CONFIG_DIR per project |
|-------------------|-------------------------------|-------------------|---------------------------|
| **Setup Complexity (15%)** | Low (1 command) | Medium (create .envrc files) | Medium (create config dirs) |
| **Automation Level (25%)** | Manual (per-command switch) | Automatic (on cd) | Automatic (on cd) |
| **Security (25%)** | High (OAuth tokens) | Medium (token in .envrc) | High (separate configs) |
| **Maintenance (15%)** | Low | Low | Low |
| **Cross-Platform (10%)** | High | Medium (needs direnv) | High |
| **IDE Integration (10%)** | Good | Variable | Good |
| **Weighted Score** | 72/100 | 78/100 | 85/100 |

### Recommended Solution: Hybrid Approach

**Short-term (Immediate):**
1. Use `gh auth login` to add saucer-boy account
2. Use `gh auth switch --user saucer-boy` before PR operations

**Long-term (Automation):**
1. Create per-project `.gh` directories with account-specific configs
2. Use direnv to set `GH_CONFIG_DIR` automatically when entering project directories

```bash
# Project .envrc file (long-term solution)
export GH_CONFIG_DIR="$PWD/.gh-saucer-boy"

# Or alternatively with GH_TOKEN directly
# export GH_TOKEN="$(cat ~/.secrets/saucer-boy-token)"
```

### SSH Configuration Reference

The existing SSH configuration for saucer-boy:

```
# ~/.ssh/config
Host github-bot
    HostName github.com
    User git
    IdentityFile ~/.ssh/saucer-boy
    IdentitiesOnly yes
```

This enables Git operations via:
```bash
# Clone using saucer-boy identity
git clone git@github-bot:owner/repo.git

# Change existing remote
git remote set-url origin git@github-bot:geekatron/jerry.git
```

### Validation

User confirmed:
- The PR identity issue is a real workflow problem
- Manual `gh auth switch` is acceptable for short-term
- Long-term automation is desirable but not urgent

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Documentation | gh auth multi-account support | [GitHub CLI Docs](https://cli.github.com/manual/gh_auth_switch) | 2023-10 |
| E-002 | Release Notes | Multi-account auth added in gh 2.40.0 | [GitHub CLI Releases](https://github.com/cli/cli/releases) | 2023-10 |
| E-003 | Incident | PR #15 created under wrong identity | PR #15 on feat/008-transcript-skill | 2026-01-31 |

### Reference Material

- **Source:** GitHub CLI Documentation
- **URL:** https://cli.github.com/manual/gh_auth
- **Date Accessed:** 2026-01-31
- **Relevance:** Authoritative documentation for gh authentication

---

## Implications

### Impact on Project

This affects ALL future PR operations and any GitHub API operations performed via `gh` CLI:
- PR creation, review, merge
- Issue management
- Release creation
- Repository operations

### Design Decisions Affected

- **Decision:** CI/CD automation using saucer-boy
  - **Impact:** Must ensure correct identity before automation
  - **Rationale:** Bot accounts should own automated PRs for audit trails

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Wrong identity for PR creation | High | Pre-operation identity check, `gh auth status` verification |
| Token exposure in .envrc | Medium | Use GH_CONFIG_DIR instead of plain tokens, add .envrc to .gitignore |
| Forgetting to switch identity | Medium | Shell prompt indicator showing current gh identity |

### Opportunities Created

- Implement shell prompt showing current `gh` identity (similar to git branch display)
- Create project-level automation for consistent identity usage

---

## Relationships

### Creates

- No new work items required (immediate workaround available)

### Informs

- All future PR creation workflows in Jerry project
- CI/CD automation design decisions

### Related Discoveries

- None currently documented

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-003](./FEAT-003-future-enhancements.md) | Future Enhancements feature |
| PR | PR #15 | The PR that exposed this issue |

---

## Recommendations

### Immediate Actions

1. Run `gh auth login` interactively to add saucer-boy account
2. Close PR #15 (created by geekatron)
3. Re-create PR under saucer-boy identity using `gh auth switch --user saucer-boy`

### Long-term Considerations

- Consider implementing GH_CONFIG_DIR automation for Jerry project
- Document identity management in project README or CONTRIBUTING.md
- Consider shell prompt customization to show current gh identity

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should we automate identity switching per-project with direnv?
   - **Investigation Method:** Evaluate setup complexity vs. frequency of identity switching
   - **Priority:** Low (manual switch is acceptable)

2. **Q:** Should the shell prompt show current gh identity like it shows git branch?
   - **Investigation Method:** Research existing shell prompt customizations
   - **Priority:** Low (nice-to-have)

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-31 | Claude | Created discovery documenting GitHub dual identity management |

---

## Metadata

```yaml
id: "FEAT-003:DISC-003"
parent_id: "FEAT-003"
work_type: DISCOVERY
title: "GitHub Dual Identity Management"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-31T12:00:00Z"
updated_at: "2026-01-31T12:30:00Z"
completed_at: "2026-01-31T12:30:00Z"
tags: ["github", "authentication", "workflow", "identity", "gh-cli"]
source: "PR #15 creation identity mismatch"
finding_type: CONSTRAINT
confidence_level: HIGH
validated: true
```

# BUG-004: Plugin Uninstall Fails — Name/Scope Mismatch

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** ---
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Found In:** 0.2.0
> **Fix Version:** 0.2.1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Fix Description](#fix-description) | Solution approach and changes made |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

Jerry plugin cannot be uninstalled via Claude Code's `/plugin` UI. Two distinct errors surface: (1) "Plugin jerry not found in marketplace" when viewing plugin details, and (2) `Failed to uninstall: Plugin "jerry@jerry" is not installed in user scope` when attempting uninstall. The root cause is a name mismatch between `plugin.json` (`name: "jerry"`) and the `marketplace.json` plugin entry (`name: "jerry-framework"`). Per Claude Code docs, `plugin.json` is authoritative for plugin identity (with `strict: true` default). Claude Code internally identifies the plugin as `jerry` but the install registry key is `jerry-framework@jerry`, causing both the marketplace lookup failure and the uninstall scope error.

**Key Details:**
- **Symptom:** Uninstall fails with scope error; marketplace lookup fails with name error
- **Frequency:** 100% reproducible — every uninstall attempt fails
- **Workaround:** Manual removal: delete Jerry directory from `~/.claude/plugins/` and remove `enabledPlugins` entry from `.claude/settings.json`

---

## Reproduction Steps

### Prerequisites

- Jerry installed via documented flow (`/plugin marketplace add` + `/plugin install jerry-framework@jerry`)
- Claude Code running with Jerry plugin active

### Steps to Reproduce

1. Open Claude Code in a project where Jerry is installed
2. Run `/plugin` to open the plugin manager
3. Select "jerry" from the plugin list — observe the plugin detail screen shows:
   ```
   jerry @ jerry
   Scope: user
   Version: 0.2.0
   ...
   Components:
   Error: Plugin jerry not found in marketplace
   ```
4. Select "Uninstall" from the action menu

### Expected Result

Plugin uninstalls cleanly. Jerry is removed from the active plugins list, skills are deregistered, and the user is returned to the plugin list with a success confirmation.

### Actual Result

```
Failed to uninstall: Plugin "jerry@jerry" is not installed in user scope. Use --scope to specify the correct scope.
```

Two errors are present:
1. **Marketplace lookup failure:** "Plugin jerry not found in marketplace" appears even while the plugin is visibly loaded and functional
2. **Uninstall scope failure:** The uninstall command uses the display name `jerry@jerry` but the actual installation was registered under a different name or scope

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS (Darwin 25.3.0) |
| **Runtime** | Claude Code CLI |
| **Application Version** | Jerry 0.2.0 |
| **Configuration** | plugin.json `name: "jerry-framework"`, installed via local marketplace |
| **Deployment** | Local development |

### Additional Environment Details

- Plugin was installed using the documented two-step process:
  1. `/plugin marketplace add ~/plugins/jerry` (registers local dir as marketplace "jerry")
  2. `/plugin install jerry-framework@jerry` (installs plugin from local marketplace)
- The `plugin.json` specifies `"name": "jerry-framework"` but Claude Code UI resolves the display name to `jerry @ jerry`
- `.claude/settings.json` `enabledPlugins` section does NOT contain a jerry entry — only `context7@claude-plugins-official` is present

---

## Root Cause Analysis

### Investigation Summary

Full filesystem investigation of Claude Code plugin internals completed 2026-02-18, with follow-up research into Claude Code plugin documentation via Context7 and official docs (code.claude.com/docs/en/plugin-marketplaces, code.claude.com/docs/en/plugins). RC-1 confirmed as root cause (corrected from initial misdiagnosis). RC-2 eliminated. RC-3 confirmed as consequence of RC-1.

### Files Examined

| File | Key Finding |
|------|------------|
| `~/.claude/settings.json` | `enabledPlugins` has `"jerry-framework@jerry": true` — correctly registered at user scope |
| `~/.claude/plugins/installed_plugins.json` | Registry key `jerry-framework@jerry`, scope `user`, installPath `cache/jerry/jerry-framework/0.2.0` |
| `~/.claude/plugins/known_marketplaces.json` | Marketplace `jerry` registered, source `git@github-bot:geekatron/jerry.git`, autoUpdate true |
| `.claude-plugin/marketplace.json` | `name: "jerry"` (marketplace name), `plugins[0].name: "jerry-framework"` (plugin entry name) — **committed, correct** |
| `.claude-plugin/plugin.json` (committed) | `name: "jerry"` — **MISMATCH** with marketplace plugin entry name `"jerry-framework"` |
| `~/.claude/plugins/marketplaces/jerry/.claude-plugin/marketplace.json` | Same as committed — plugin entry correctly says `"jerry-framework"` |
| `~/.claude/plugins/marketplaces/jerry/.claude-plugin/plugin.json` | `name: "jerry"` — marketplace clone reflects the committed plugin.json |
| `~/.claude/plugins/cache/jerry/jerry-framework/0.2.0/.claude-plugin/plugin.json` | `name: "jerry"` — cached install snapshot also has the committed name |
| Official docs reference | `context7@claude-plugins-official` registry pattern confirms `plugin-name@marketplace-name` format |

### Root Cause (CONFIRMED)

**RC-1: plugin.json `name` does not match marketplace.json plugin entry `name`.**

Per Claude Code documentation (code.claude.com/docs/en/plugins-reference): "If you include a manifest file (.claude-plugin/plugin.json), the name field is the only one that is strictly required. This name is used for namespacing components within Claude." With `strict: true` (default), **plugin.json is authoritative** for the plugin's identity.

The **marketplace.json** correctly lists the plugin as `"jerry-framework"` in its `plugins` array. The install command `/plugin install jerry-framework@jerry` uses this marketplace entry name, and the registry correctly stores the key as `jerry-framework@jerry`.

However, **plugin.json** declares `name: "jerry"` (not `"jerry-framework"`). Since plugin.json is authoritative, Claude Code internally identifies the plugin as `jerry`, causing:

1. **UI Display**: Shows `jerry @ jerry` (using plugin.json name + marketplace name)
2. **Uninstall**: Tries to remove `jerry@jerry` (plugin.json name)
3. **Registry Lookup**: Finds `jerry-framework@jerry` (marketplace entry name) — **NO MATCH**
4. **Result**: `Failed to uninstall: Plugin "jerry@jerry" is not installed in user scope`

**The fix**: Make `plugin.json` `name` field consistent with `marketplace.json` `plugins[0].name`: both must be `"jerry-framework"`.

### Root Cause Candidates (Post-Investigation)

| # | Hypothesis | Status | Evidence |
|---|-----------|--------|----------|
| RC-1 | **plugin.json name / marketplace entry name mismatch** | **CONFIRMED** | `marketplace.json` says plugin is `jerry-framework`. `plugin.json` says `jerry`. Per Claude Code docs, plugin.json is authoritative (strict: true default). Claude Code resolves identity as `jerry`, but registry key is `jerry-framework@jerry`. Uninstall fails. |
| RC-2 | **Scope mismatch** (project vs user) | **ELIMINATED** | `installed_plugins.json` shows `scope: "user"`. `~/.claude/settings.json` has the `enabledPlugins` entry. Plugin IS at user scope. |
| RC-3 | **Marketplace "not found" error** | **CONFIRMED (consequence of RC-1)** | When the UI looks up plugin details, it searches for `jerry` (from plugin.json) in the marketplace. But the marketplace catalog lists the plugin as `jerry-framework`. Name lookup fails → "Plugin jerry not found in marketplace". |

### Contributing Factors

- **`plugin.json` `license` field says `"MIT"`** in the committed `main` branch, despite Apache 2.0 migration in FEAT-015. The license migration (EN-930) updated `LICENSE`, `NOTICE`, `pyproject.toml`, and 404 `.py` file headers but missed `plugin.json`.
- **Skill namespace impact**: Changing plugin.json name from `jerry` to `jerry-framework` changes the skill namespace (e.g., `/jerry:worktracker` → `/jerry-framework:worktracker`). All permission entries in `.claude/settings.local.json` referencing `Skill(jerry:*)` must be updated to `Skill(jerry-framework:*)`.
- **Documentation was correct**: INSTALLATION.md already documented the install command as `/plugin install jerry-framework@jerry` and verification as `"name": "jerry-framework"` — the source code simply never matched the docs.

---

## Fix Description

### Solution Approach

**Fix 1: Update `plugin.json` name to `jerry-framework`** — The `marketplace.json` correctly declares the plugin as `jerry-framework`. Per Claude Code docs, `plugin.json` name must match the marketplace entry name. Change `name` from `"jerry"` to `"jerry-framework"`.

**Fix 2: Fix `plugin.json` license** — Change `"license": "MIT"` to `"license": "Apache-2.0"` (missed during FEAT-015 license migration).

**Fix 3: Update skill permission references** — Changing plugin.json name changes the skill namespace from `jerry:*` to `jerry-framework:*`. Update all `Skill(jerry:*)` entries in `.claude/settings.local.json` to `Skill(jerry-framework:*)`.

**Fix 4: Reinstall plugin** — After committing and pushing changes, user must:
1. Update marketplace: `/plugin marketplace update jerry`
2. Uninstall stale entry: manually edit `~/.claude/plugins/installed_plugins.json` to remove `jerry-framework@jerry` entry, or attempt `/plugin uninstall jerry-framework@jerry`
3. Reinstall: `/plugin install jerry-framework@jerry`

### Changes Required

| File | Change Description | Status |
|------|-------------------|--------|
| `.claude-plugin/plugin.json` | Change `name` to `"jerry-framework"`, change `license` to `"Apache-2.0"` | DONE |
| `.claude/settings.local.json` | Update all `Skill(jerry:*)` to `Skill(jerry-framework:*)` | DONE |
| `docs/INSTALLATION.md` | Already correct — documents `jerry-framework@jerry` throughout | NO CHANGE NEEDED |
| `.claude-plugin/marketplace.json` | Already correct — `plugins[0].name: "jerry-framework"` | NO CHANGE NEEDED |
| `~/.claude/plugins/installed_plugins.json` | Manual: remove stale entry (or uninstall + reinstall after push) | MANUAL POST-MERGE |
| `~/.claude/settings.json` (user) | Manual: may need to re-enable after reinstall | MANUAL POST-MERGE |

---

## Acceptance Criteria

### Fix Verification

- [ ] AC-1: `/plugin install` installs Jerry with correct name displayed in plugin UI
- [ ] AC-2: `/plugin` detail screen shows correct `name @ marketplace` with no "not found in marketplace" error
- [ ] AC-3: "Uninstall" action from plugin UI removes Jerry cleanly without scope errors
- [ ] AC-4: Full install → verify → uninstall → reinstall cycle works without errors
- [ ] AC-5: `plugin.json` `license` field reads `"Apache-2.0"`

### Quality Checklist

- [ ] Regression tests added (if applicable — may be manual verification only)
- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] INSTALLATION.md updated to reflect any name/scope changes

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Items

- **Related Feature:** [FEAT-017: Installation Instructions Modernization](../FEAT-017-installation-instructions/FEAT-017-installation-instructions.md) — Installation docs may need updating
- **Related Feature:** [FEAT-015: License Migration](../FEAT-015-license-migration/FEAT-015-license-migration.md) — `plugin.json` license field was missed during migration
- **Related File:** `.claude-plugin/plugin.json` — Primary configuration file
- **Related File:** `docs/INSTALLATION.md` — User-facing installation instructions

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Adam Nowak | pending | Initial report. Two errors: marketplace lookup failure + uninstall scope failure. Three root cause candidates identified. |
| 2026-02-18 | Claude | pending | Initial RC-1 diagnosis (INCORRECT): assumed `jerry-framework` in plugin.json was an uncommitted mistake. Recommended reverting to `jerry`. |
| 2026-02-18 | Claude | pending | RC-1 CORRECTED via Context7 + Claude Code plugin docs research. True root cause: `plugin.json` name `"jerry"` does not match `marketplace.json` plugin entry name `"jerry-framework"`. Per Claude Code docs, plugin.json is authoritative (strict: true default). Claude Code resolves plugin as `jerry` but registry has `jerry-framework@jerry`. Fix: change plugin.json name to `jerry-framework`, fix license to Apache-2.0, update skill namespace permissions. INSTALLATION.md and marketplace.json already correct. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |

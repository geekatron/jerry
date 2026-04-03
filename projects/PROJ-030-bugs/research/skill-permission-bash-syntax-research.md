# Skill Permission Patterns and Bash Deprecated Syntax Research

> Research into Claude Code Skill() permission namespace behavior and Bash(:*) deprecated syntax migration, supporting GitHub Issues #181 and #182.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings and project impact |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed findings with evidence and code |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic impact, risks, migration plan |
| [References](#references) | Complete citation list |

---

## L0: Executive Summary

Jerry's settings file (`.claude/settings.local.json`) has two categories of problems that need fixing.

**Problem 1: Skill permissions use an uncertain namespace format.** Jerry lists skills in two forms -- `Skill(jerry:adversary)` and `Skill(adversary)`. The colon-namespaced form (`jerry:adversary`) is how Claude Code internally names plugin skills, but the official Claude Code documentation only describes `Skill(name)` and `Skill(name *)` as permission patterns. The colon form is not documented as a valid permission syntax. It passes the JSON schema regex (which simply allows any non-parenthesis character inside the parentheses), but whether it actually matches skill invocations at runtime is unverified. Additionally, 12 skills registered in CLAUDE.md have NO permission entries at all, meaning Claude may prompt the user for approval every time they are invoked.

**Problem 2: Every Bash permission uses a deprecated syntax.** All 32 `Bash()` entries use the `:*` suffix (e.g., `Bash(echo:*)`), which Claude Code documentation explicitly marks as deprecated. The replacement is a space before the wildcard (e.g., `Bash(echo *)`). A bug report in `claude-code-action` (Issue #856) confirmed this deprecated syntax causes SDK validation errors. A recent bug report (Issue #33595, March 2026) shows the colon syntax may be silently failing for some users.

**What this means for the project:** Both issues should be fixed. The Bash syntax migration is straightforward and low-risk -- replace `:*` with ` *` in all entries. The Skill permission cleanup should (a) remove the duplicate `Skill(jerry:name)` entries (or keep them only if testing proves they are required), and (b) add `Skill()` entries for all 12 missing skills.

---

## L1: Technical Analysis

### Part 1: Skill Permission Patterns (#181)

#### Q1-Q3: Does `Skill(jerry:adversary)` match plugin skills?

**Finding:** The colon-namespaced form `Skill(jerry:skill-name)` corresponds to the plugin skill namespace convention, but its use as a **permission pattern** is not documented.

The Claude Code skills documentation states:

> "Plugin skills use a plugin-name:skill-name namespace, so they cannot conflict with other levels."

**Source:** [Claude Code Skills](https://code.claude.com/docs/en/skills) -- plugin skill namespace section.

However, the permission documentation only describes two forms:

> "Permission syntax: Skill(name) for exact match, Skill(name *) for prefix match with any arguments."

**Source:** [Claude Code Skills](https://code.claude.com/docs/en/skills) -- "Restrict Claude's skill access" section.

The documented examples of Skill permissions are: `Skill(commit)`, `Skill(review-pr *)`, `Skill(deploy *)`. No colon-namespaced example appears in the permission documentation.

GitHub Issue #12817 (documentation request) shows a user discovering empirically that `Skill(plugin-dev:hook-development)` works as a permission pattern for plugin skills. The issue was closed as "not planned" (documentation not updated), which means this syntax is used in the wild but remains undocumented.

**Source:** [GitHub Issue #12817](https://github.com/anthropics/claude-code/issues/12817)

GitHub Issue #29360 documents a bug where `--plugin-dir` loading applies a namespace prefix to MCP tool names (`mcp__plugin_<plugin-name>_<server-name>__<tool>`) that does NOT match the skill's `allowed-tools` declarations. This indicates that Claude Code's namespace handling for plugins has known inconsistencies between tool naming and permission matching.

**Source:** [GitHub Issue #29360](https://github.com/anthropics/claude-code/issues/29360)

**Conclusion:** The `Skill(jerry:adversary)` form likely works for plugin skills loaded via the standard plugin mechanism, but this behavior is (a) undocumented, (b) subject to known bugs in namespace resolution, and (c) redundant if `Skill(adversary)` also matches. The safest approach is to keep both forms until empirical testing can confirm which is required, or to use only the documented `Skill(name)` form.

#### Q4: JSON Schema Regex Analysis

The `permissionRule` regex from the schema at `https://json.schemastore.org/claude-code-settings.json` is:

```regex
^((Agent|Bash|Edit|...|Skill|...|Write)(\((?=.*[^)*?])[^)]+\))?|mcp__.*)$
```

**Source:** `docs/schemas/claude-code-settings-v1.schema.json` line 8.

Breaking down the Skill-relevant portion:

1. `Skill` -- matches the literal tool name
2. `(\((?=.*[^)*?])[^)]+\))?` -- optionally matches parenthesized content:
   - `\(` -- opening paren
   - `(?=.*[^)*?])` -- lookahead: content must contain at least one char that is not `)`, `*`, or `?`
   - `[^)]+` -- one or more chars that are NOT `)` (closing paren)
   - `\)` -- closing paren

**Key finding:** The character class `[^)]+` matches ANY character except `)`. This means colons (`:`) ARE accepted by the regex. Both `Skill(adversary)` and `Skill(jerry:adversary)` pass schema validation.

However, schema validation only confirms the string is syntactically valid JSON for the settings file. It does NOT confirm that Claude Code's runtime permission matcher will correctly resolve `Skill(jerry:adversary)` to match a plugin skill invocation.

#### Q5-Q6: Current State of Skill Permissions

**Skills registered in CLAUDE.md (19 skills):**

| # | Skill | In settings.local.json? |
|---|-------|------------------------|
| 1 | `/worktracker` | Yes (both forms) |
| 2 | `/problem-solving` | Yes (both forms) |
| 3 | `/nasa-se` | Yes (both forms) |
| 4 | `/orchestration` | Yes (both forms) |
| 5 | `/adversary` | Yes (both forms) |
| 6 | `/transcript` | Yes (both forms) |
| 7 | `/prompt-engineering` | Yes (both forms) |
| 8 | `/architecture` | **NO** |
| 9 | `/ast` | **NO** |
| 10 | `/diataxis` | **NO** |
| 11 | `/eng-team` | **NO** |
| 12 | `/red-team` | **NO** |
| 13 | `/pm-pmm` | **NO** |
| 14 | `/saucer-boy` | **NO** |
| 15 | `/saucer-boy-framework-voice` | **NO** |
| 16 | `/user-experience` | **NO** |
| 17 | `/use-case` | **NO** |
| 18 | `/test-spec` | **NO** |
| 19 | `/contract-design` | **NO** |

**Source:** `.claude/settings.local.json` (lines 6-17, 54-55), `CLAUDE.md` (lines 73-93).

#### Q7: Missing Skills

**12 skills are missing** from the permission entries: `architecture`, `ast`, `diataxis`, `eng-team`, `red-team`, `pm-pmm`, `saucer-boy`, `saucer-boy-framework-voice`, `user-experience`, `use-case`, `test-spec`, `contract-design`.

Additionally, 30 skill directories exist on disk (see Glob results), but CLAUDE.md registers only 19 as top-level skills. The remaining directories (e.g., `ux-ai-first-design`, `ux-atomic-design`, `ux-behavior-design`, etc.) appear to be sub-skills of `/user-experience` and may not need independent permission entries.

Per the Claude Code documentation, skills operate by default unless denied. However, per GitHub Issue #10833, in practice, Claude prompts for approval when a skill is invoked unless an explicit `allow` entry exists. This behavior varies by context (main repo vs. git worktrees).

**Source:** [GitHub Issue #10833](https://github.com/anthropics/claude-code/issues/10833) -- skill-level permissions discussion.

### Part 2: Bash Deprecated Syntax (#182)

#### Q8: All Deprecated Bash Entries

Every `Bash()` entry in `settings.local.json` uses the deprecated `:*` suffix. Complete list (32 entries):

| # | Deprecated Form | Correct Form |
|---|-----------------|-------------|
| 1 | `Bash(echo:*)` | `Bash(echo *)` |
| 2 | `Bash(gh pr list:*)` | `Bash(gh pr list *)` |
| 3 | `Bash(gh pr view:*)` | `Bash(gh pr view *)` |
| 4 | `Bash(gh run view:*)` | `Bash(gh run view *)` |
| 5 | `Bash(git status:*)` | `Bash(git status *)` |
| 6 | `Bash(git check-ignore:*)` | `Bash(git check-ignore *)` |
| 7 | `Bash(git add:*)` | `Bash(git add *)` |
| 8 | `Bash(git commit:*)` | `Bash(git commit *)` |
| 9 | `Bash(git push:*)` | `Bash(git push *)` |
| 10 | `Bash(gh run list:*)` | `Bash(gh run list *)` |
| 11 | `Bash(uv run python:*)` | `Bash(uv run python *)` |
| 12 | `Bash(FEAT_DIR=...:*)` | `Bash(FEAT_DIR=... *)` |
| 13 | `Bash(git mv:*)` | `Bash(git mv *)` |
| 14 | `Bash(git ls-tree:*)` | `Bash(git ls-tree *)` |
| 15 | `Bash(git checkout:*)` | `Bash(git checkout *)` |
| 16 | `Bash(uv run pytest:*)` | `Bash(uv run pytest *)` |
| 17 | `Bash(gh pr create:*)` | `Bash(gh pr create *)` |
| 18 | `Bash(git pull:*)` | `Bash(git pull *)` |
| 19 | `Bash(git fetch:*)` | `Bash(git fetch *)` |
| 20 | `Bash(test:*)` | `Bash(test *)` |
| 21 | `Bash(find:*)` | `Bash(find *)` |
| 22 | `Bash(git log:*)` | `Bash(git log *)` |
| 23 | `Bash(ls:*)` | `Bash(ls *)` |
| 24 | `Bash(python3:*)` | `Bash(python3 *)` |
| 25 | `Bash(python3:*)` (duplicate) | `Bash(python3 *)` |
| 26 | `Bash(uv run pyright:*)` | `Bash(uv run pyright *)` |
| 27 | `Bash(uv run:*)` | `Bash(uv run *)` |
| 28 | `Bash(wc:*)` | `Bash(wc *)` |
| 29 | `Bash(grep:*)` | `Bash(grep *)` |
| 30 | `Bash(git stash:*)` | `Bash(git stash *)` |

**Additional issues found:**
- Line 48-49: Duplicate `Bash(python3:*)` entry.
- Line 12 (entry 12): The `FEAT_DIR=` entry is project-specific cruft and should be removed.

**Source:** `.claude/settings.local.json` lines 25-56.

#### Q9: Schema Regex Acceptance of Both Forms

The regex `[^)]+` inside the Bash() parentheses matches any character except `)`. Both `:*` and ` *` (space-star) are syntactically valid per the schema. The schema does NOT enforce deprecation -- it merely validates structure.

The schema examples include `Bash(git commit *)` (with space) but NOT `Bash(git commit:*)` (with colon), consistent with the documented preference for the space form.

**Source:** `docs/schemas/claude-code-settings-v1.schema.json` lines 11-15 (examples array).

#### Q10: Deprecation Timeline

The Claude Code permissions documentation explicitly states:

> "The legacy :* suffix syntax is equivalent to * but is deprecated."

**Source:** [Claude Code Permissions](https://code.claude.com/docs/en/permissions) -- Bash wildcard patterns section.

There is no published date for when `:*` was deprecated. The deprecation is documented in the current permissions page without a removal timeline.

However, evidence from Issue #856 (claude-code-action, reported January 24, 2026, fixed February 11, 2026) shows the `:*` syntax caused SDK validation errors in the GitHub Action context. The fix was classified as P1 (Showstopper).

**Source:** [GitHub Issue #856 (claude-code-action)](https://github.com/anthropics/claude-code-action/issues/856)

Issue #33595 (reported March 12, 2026) shows users experiencing the `:*` form silently failing (not matching commands), with no warning or auto-migration from Claude Code.

**Source:** [GitHub Issue #33595](https://github.com/anthropics/claude-code/issues/33595)

**Timeline reconstruction:**
- The `:*` syntax was the original/legacy form.
- At some point prior to the current documentation cycle, it was marked deprecated.
- By January 2026, it caused SDK validation failures in claude-code-action.
- By March 2026, it is reported as silently failing in some contexts.
- No official removal date has been announced, but the trajectory suggests it may stop working entirely without notice.

---

## L2: Architectural Implications

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `Bash(:*)` entries silently fail in future Claude Code version | HIGH | HIGH -- all Bash commands would require manual approval | Migrate to `Bash(command *)` syntax now |
| Missing Skill permissions cause approval prompts | MEDIUM | MEDIUM -- workflow interruption for 12 skills | Add `Skill(name)` entries for all registered skills |
| `Skill(jerry:name)` entries become invalid | LOW | LOW -- redundant with `Skill(name)` entries | Remove or keep as belt-and-suspenders |
| Duplicate entries cause confusion | LOW | LOW -- cosmetic | Deduplicate during cleanup |

### Migration Strategy

**Phase 1 -- Bash syntax (Issue #182):** Low risk, immediate fix.

1. Replace every `:*` with ` *` in all `Bash()` entries.
2. Remove the duplicate `Bash(python3:*)` entry (line 49).
3. Remove the stale `FEAT_DIR=` entry (line 36).
4. This is a mechanical transformation with no behavioral change (per the documentation, `:*` is "equivalent to `*`").

**Phase 2 -- Skill permissions (Issue #181):** Requires a decision.

Two options:

**Option A (Conservative):** Keep both `Skill(jerry:name)` and `Skill(name)` for existing skills. Add `Skill(name)` entries for all 12 missing skills. Total: ~38 Skill entries.

**Option B (Clean):** Remove all `Skill(jerry:name)` entries (rely solely on `Skill(name)` which is the documented form). Add `Skill(name)` entries for all 12 missing skills. Total: ~19 Skill entries.

**Recommendation:** Option B. The `Skill(name)` form is the only documented permission pattern. The `jerry:` prefix corresponds to the internal plugin namespace but is undocumented as a permission mechanism. Keeping both creates maintenance burden and may cause confusion. If Option B causes skill approval prompts, the `jerry:` prefix entries can be restored.

### Trade-offs

| Dimension | Option A (Keep both) | Option B (Short names only) |
|-----------|---------------------|----------------------------|
| Correctness risk | Lower (covers both resolution paths) | Minimal (documented form; fallback easy) |
| Maintenance | Higher (38 entries to maintain) | Lower (19 entries) |
| Readability | Lower (unclear why both forms exist) | Higher (clear, consistent) |
| Future-proofing | Vulnerable to namespace changes | Aligned with documented API |

### Alignment with Existing Architecture

Jerry's `docs/reference/claude-code-permissions.md` already documents FINDING-002 (colon-namespaced form unverified), FINDING-003 (9 skills missing -- now 12), and FINDING-004 (deprecated `:*` syntax). This research validates those findings with additional evidence from GitHub issues and official documentation.

After the migration, `docs/reference/claude-code-permissions.md` should be updated to mark FINDING-002, FINDING-003, and FINDING-004 as RESOLVED.

---

## References

1. [Claude Code Permissions](https://code.claude.com/docs/en/permissions) -- Key insight: `:*` suffix explicitly deprecated; `Skill(name)` and `Skill(name *)` are the only documented permission forms.
2. [Claude Code Skills](https://code.claude.com/docs/en/skills) -- Key insight: Plugin skills use `plugin-name:skill-name` namespace for identity, but permission syntax is `Skill(name)` / `Skill(name *)`.
3. [GitHub Issue #29360](https://github.com/anthropics/claude-code/issues/29360) -- Key insight: Plugin namespace prefix (`plugin_<name>_`) breaks `allowed-tools` resolution; namespace handling has known bugs.
4. [GitHub Issue #12817](https://github.com/anthropics/claude-code/issues/12817) -- Key insight: `Skill(plugin-dev:hook-development)` used empirically but not documented in official permission syntax.
5. [GitHub Issue #33595](https://github.com/anthropics/claude-code/issues/33595) -- Key insight: `Bash(ls:*)` reported as silently failing in March 2026; multiple users affected.
6. [GitHub Issue #856 (claude-code-action)](https://github.com/anthropics/claude-code-action/issues/856) -- Key insight: `:*` syntax caused P1 SDK validation errors; fixed by migrating to space syntax.
7. [GitHub Issue #10833](https://github.com/anthropics/claude-code/issues/10833) -- Key insight: `Skill(*)` permission has inconsistent behavior in git worktrees; explicit entries recommended.
8. [GitHub Issue #15944](https://github.com/anthropics/claude-code/issues/15944) -- Key insight: Cross-plugin `plugin-name:skill-name` references proposed but closed as not planned.
9. `docs/schemas/claude-code-settings-v1.schema.json` (local) -- Key insight: Regex `[^)]+` allows colons in Skill/Bash specifiers; schema validates structure, not semantic correctness.
10. `.claude/settings.local.json` (local) -- Key insight: 32 Bash entries with deprecated `:*` syntax; 7 skills with permissions, 12 missing.
11. `CLAUDE.md` (local) -- Key insight: 19 skills registered; only 7 have permission entries.
12. `docs/reference/claude-code-permissions.md` (local) -- Key insight: FINDING-002, FINDING-003, FINDING-004 previously identified; this research provides external validation.

---

## Methodology

| Step | Tool | Purpose |
|------|------|---------|
| 1 | Read | Examined `settings.local.json`, `CLAUDE.md`, JSON schema, existing permissions reference |
| 2 | WebSearch | Searched for Claude Code permission syntax, deprecated Bash patterns, plugin namespace behavior |
| 3 | WebFetch | Fetched Claude Code official docs (permissions, skills), GitHub issues (#29360, #12817, #33595, #856, #10833, #15944) |
| 4 | Glob | Enumerated all skill directories on disk |
| 5 | Regex analysis | Manually decomposed JSON schema `permissionRule` regex to determine character acceptance |

### Limitations

- **No runtime testing performed.** Schema validation confirms syntactic acceptance but not runtime behavior. The question of whether `Skill(jerry:adversary)` actually matches plugin skill invocations remains empirically unverified in Jerry's specific setup.
- **Deprecation timeline is approximate.** No official Anthropic changelog entry pinpoints when `:*` was deprecated.
- **Git worktree behavior untested.** Issue #10833 suggests Skill permissions may behave differently in worktrees, which is relevant if Jerry is used in worktree workflows.

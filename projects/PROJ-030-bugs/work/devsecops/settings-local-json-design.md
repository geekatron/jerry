# Architecture Design: Corrected `.claude/settings.local.json`

> eng-architect design for GitHub Issues #181 (Skill permission cleanup) and #182 (Bash deprecated syntax migration). Addresses FINDING-002, FINDING-003, FINDING-004 from `docs/reference/claude-code-permissions.md`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key decisions and business risk |
| [L1: Technical Design](#l1-technical-design) | Complete design with rationale per decision |
| [L2: Threat Model](#l2-threat-model) | STRIDE analysis of permission configuration |

---

## L0: Executive Summary

Five architecture decisions govern the corrected `settings.local.json`:

1. **Remove all `Skill(jerry:name)` entries.** The colon-namespaced form is undocumented as a permission pattern (FINDING-002). Only `Skill(name)` is documented. Keeping undocumented forms increases maintenance burden and masks the actual matching behavior.

2. **Add `Skill(name)` entries for all 19 CLAUDE.md-registered skills.** Twelve skills had no permission entries (FINDING-003). Without explicit `allow` entries, Claude Code may prompt for approval on every invocation, breaking H-22 proactive invocation.

3. **Replace all `:*` with ` *` in Bash entries.** The `:*` suffix is explicitly deprecated (FINDING-004). Evidence from Issue #33595 (March 2026) shows it may silently fail. Remove the duplicate `Bash(python3 *)` and the stale `FEAT_DIR=` entry.

4. **Remove ALL Bash entries from local.** The committed `settings.json` uses broader patterns that subsume every local Bash entry. The three candidates initially considered local-only (`Bash(git push *)`, `Bash(git stash *)`, `Bash(grep *)`) were all removed during C4 tournament review: git push conflicts with `settings.json`'s `ask` entry (red-exploit finding), git stash is destructive (FM-010), and grep is covered by the structured Grep tool (RT-003).

5. **~~Keep the hooks block.~~** REVISED in C4 tournament: **Hooks block REMOVED.** The auto-approve hooks were found to violate P-020 (user authority bypass) and P-022 (structural deception) by 4 independent strategies (S-001 RT-002, S-007 CC-001/CC-002, S-012 FM-013/FM-014). WebSearch/WebFetch are already in the committed `settings.json` allow list, making the hooks redundant. Additionally, `Bash(git stash *)`, `Bash(grep *)`, and `Bash(git push *)` were removed during the tournament — git stash is destructive (FM-010), grep is covered by the structured Grep tool (RT-003), and git push conflicts with settings.json's ask entry (red-exploit finding).

**Net effect:** The file shrinks from 56 allow entries to 22 (19 Skill + 3 MCP wildcards), all using documented syntax. Zero Bash entries remain (all subsumed by `settings.json` or removed for safety/policy reasons). Zero hooks remain (removed for P-020/P-022 violations). The `python3` entries are removed (H-05 violation -- all Python execution must go through `uv run`).

---

## L1: Technical Design

### Decision 1: Skill Permission Form

**Context:** `settings.local.json` contains both `Skill(jerry:adversary)` and `Skill(adversary)` for 7 skills, plus `Skill(jerry:prompt-engineering)` and `Skill(prompt-engineering)`.

**Decision:** Use only the documented `Skill(name)` form. Remove all `Skill(jerry:name)` entries.

**Rationale:**
- The `Skill(jerry:name)` form corresponds to the plugin namespace convention but is NOT documented as a permission pattern (research ref 1, 2).
- GitHub Issue #29360 shows known bugs in Claude Code plugin namespace resolution.
- The `Skill(name)` form is the only form appearing in official documentation examples.
- Keeping both creates maintenance burden (2x entries) with no verified benefit.
- If removing the colon form causes approval prompts, it can be restored in a follow-up commit.

**Status:** FINDING-002 resolved.

### Decision 2: Complete Skill Coverage

**Context:** CLAUDE.md registers 19 skills. Only 7 had permission entries.

**Decision:** Add `Skill(name)` entries for all 19 skills registered in CLAUDE.md.

**Complete skill list (19):**

| # | Skill Name | Previously Present | Note |
|---|-----------|-------------------|------|
| 1 | `adversary` | Yes | -- |
| 2 | `architecture` | No | Added |
| 3 | `ast` | No | Added |
| 4 | `contract-design` | No | Added |
| 5 | `diataxis` | No | Added |
| 6 | `eng-team` | No | Added |
| 7 | `nasa-se` | Yes | -- |
| 8 | `orchestration` | Yes | -- |
| 9 | `pm-pmm` | No | Added |
| 10 | `problem-solving` | Yes | -- |
| 11 | `prompt-engineering` | Yes | -- |
| 12 | `red-team` | No | Added |
| 13 | `saucer-boy` | No | Added |
| 14 | `saucer-boy-framework-voice` | No | Added |
| 15 | `test-spec` | No | Added |
| 16 | `transcript` | Yes | -- |
| 17 | `use-case` | No | Added |
| 18 | `user-experience` | No | Added |
| 19 | `worktracker` | Yes | -- |

**Not included:** `bootstrap` (not registered in CLAUDE.md). The 10 `ux-*` sub-skills are sub-skills of `/user-experience` and are invoked through the parent skill, not independently permissioned.

**Status:** FINDING-003 resolved.

### Decision 3: Bash Syntax Migration

**Context:** All 32 `Bash()` entries use the deprecated `:*` suffix.

**Decision:** Replace `:*` with ` *`. Remove duplicate `Bash(python3 *)`. Remove stale `Bash(FEAT_DIR=...)`. Remove `Bash(python3 *)` entirely (H-05: all Python must use `uv run`).

**Status:** FINDING-004 resolved.

### Decision 4: Overlap Resolution with `settings.json`

**Context:** `settings.json` (committed, shared, precedence 4) already contains broad patterns. `settings.local.json` (local, precedence 3) has narrower patterns for the same commands.

**Analysis of `settings.json` coverage:**

| `settings.json` Pattern | Local Entries It Subsumes |
|-------------------------|--------------------------|
| `Bash(uv *)` | `Bash(uv run *)`, `Bash(uv run python *)`, `Bash(uv run pytest *)`, `Bash(uv run pyright *)` |
| `Bash(git status *)` | `Bash(git status *)` (exact duplicate) |
| `Bash(git diff *)` | (no local equivalent) |
| `Bash(git log *)` | `Bash(git log *)` (exact duplicate) |
| `Bash(git branch *)` | (no local equivalent) |
| `Bash(git checkout *)` | `Bash(git checkout *)` (exact duplicate) |
| `Bash(git add *)` | `Bash(git add *)` (exact duplicate) |
| `Bash(git commit *)` | `Bash(git commit *)` (exact duplicate) |
| `Bash(git fetch *)` | `Bash(git fetch *)` (exact duplicate) |
| `Bash(git pull *)` | `Bash(git pull *)` (exact duplicate) |
| `Bash(git mv *)` | `Bash(git mv *)` (exact duplicate) |
| `Bash(git ls-tree *)` | `Bash(git ls-tree *)` (exact duplicate) |
| `Bash(git check-ignore *)` | `Bash(git check-ignore *)` (exact duplicate) |
| `Bash(gh pr *)` | `Bash(gh pr list *)`, `Bash(gh pr view *)`, `Bash(gh pr create *)` |
| `Bash(gh run *)` | `Bash(gh run view *)`, `Bash(gh run list *)` |
| `Bash(gh issue *)` | (no local equivalent) |
| `Bash(ls *)` | `Bash(ls *)` (exact duplicate) |
| `Bash(test *)` | `Bash(test *)` (exact duplicate) |
| `Bash(wc *)` | `Bash(wc *)` (exact duplicate) |
| `Bash(echo *)` | `Bash(echo *)` (exact duplicate) |
| `Bash(find *)` | `Bash(find *)` (exact duplicate) |
| `WebSearch` | `WebSearch` (exact duplicate) |
| `WebFetch` | `WebFetch` (exact duplicate) |

**Local-only entries (NOT in `settings.json`):**

| Entry | Keep? | Rationale |
|-------|-------|-----------|
| `Bash(git push *)` | No | Already in `settings.json` `ask` array -- local `allow` would override the shared safety gate (red-exploit finding during C4 tournament) |
| `Bash(git stash *)` | No | Destructive operation (FM-010 during C4 tournament); no safety justification for auto-approval |
| `Bash(grep *)` | No | Covered by the structured Grep tool (RT-003 during C4 tournament); Bash grep is unnecessary |
| `Bash(python3 *)` | No | H-05 violation: all Python execution must use `uv run` |
| `Bash(FEAT_DIR=...)` | No | Stale project-specific cruft |

**Decision:** Remove ALL Bash and web tool entries from local. This eliminates all ~30 Bash entries. The committed `settings.json` provides sufficient Bash coverage for safe commands, and the three initially considered local-only entries (`git push`, `git stash`, `grep`) were all removed during C4 tournament review for safety, policy, or redundancy reasons.

**REVISED during C4 tournament:** The initial design proposed keeping `Bash(git push *)`, `Bash(git stash *)`, and `Bash(grep *)`. All three were removed: `git push` conflicts with the `settings.json` `ask` safety gate (auto-approving push defeats the shared safety intent); `git stash` is a destructive operation that should require explicit approval (FM-010); `grep` is fully covered by the structured Grep tool which provides better user experience and avoids Bash-based exfiltration surface (RT-003).

### Decision 5: Hooks Block

**Context:** `settings.local.json` had a hooks block with PreToolUse and PermissionRequest matchers for WebFetch/WebSearch that auto-allow these tools.

**Analysis (pre-tournament):**
- The committed `settings.json` has NO hooks block.
- The backup `settings.json.bkup` has hooks (PreToolUse, PostToolUse, SubagentStop, SessionStart) but this is a backup file, not active.
- The local hooks provided developer-specific auto-approval for web search tools.
- No `.claude/hooks/` directory or `hooks.json` file exists.

**Decision:** **REVISED in C4 tournament: Hooks block REMOVED.** Four independent strategies identified the hooks as violations:
- S-001 RT-002: Auto-approve hooks bypass the permission model entirely.
- S-007 CC-001/CC-002: Hooks violate P-020 (user authority bypass) and P-022 (structural deception -- the hooks silently suppress approval prompts).
- S-012 FM-013/FM-014: FMEA identified hooks as a high-RPN failure mode for permission bypass.

WebSearch and WebFetch are already in the committed `settings.json` allow list, making the local hooks redundant. Removing them restores the standard permission evaluation path without any loss of functionality.

### Decision 6: MCP Permissions

**Context:** Local file has 5 MCP entries: `mcp__memory-keeper__*`, `mcp__context7__*`, `mcp__context7__resolve-library-id`, `mcp__context7__query-docs`, `mcp__plugin_context7_context7__*`, `mcp__plugin_context7_context7__resolve-library-id`, `mcp__plugin_context7_context7__query-docs`.

**Analysis:**
- MCP server configuration is per-developer (servers run locally).
- The `mcp__context7__*` wildcard already covers `mcp__context7__resolve-library-id` and `mcp__context7__query-docs`.
- The `mcp__plugin_context7_context7__*` wildcard already covers the two specific plugin entries.
- The `mcp__plugin_context7_context7__*` entries exist because of the Context7 plugin namespace convention (GitHub Issue #29360).

**Decision:** Keep the wildcard entries. Remove the specific tool entries that are subsumed by wildcards. This reduces 7 MCP entries to 3 wildcards.

### Complete Corrected File

The corrected `settings.local.json` contains:

**Permissions (allow):**
- 19 Skill entries (all CLAUDE.md-registered skills, documented `Skill(name)` form only)
- 3 MCP wildcard entries (memory-keeper, context7, plugin_context7_context7)
- 0 Bash entries (all removed -- subsumed by `settings.json` or removed for safety/policy reasons during C4 tournament)

**Hooks:** Removed (P-020/P-022 violations identified by 4 independent C4 tournament strategies).

**Total allow entries:** 22 (down from 56).

---

## L2: Threat Model

### Trust Boundaries

| Boundary | Description |
|----------|-------------|
| TB-1 | Developer workstation to Claude Code runtime |
| TB-2 | Claude Code runtime to external MCP servers (Context7, Memory-Keeper) |
| TB-3 | Claude Code runtime to GitHub API (via `gh` CLI) |
| TB-4 | Shared settings (`settings.json`) to local settings (`settings.local.json`) |

### STRIDE Analysis of Permission Configuration

| ID | Category | Threat | Component | Mitigation |
|----|----------|--------|-----------|------------|
| T-01 | Elevation of Privilege | Local `allow` could override shared `ask` for `git push`, enabling auto-push without approval | TB-4 | Mitigated: `Bash(git push *)` removed from local `allow` during C4 tournament. The `ask` entry in shared `settings.json` now applies without override. |
| T-02 | Tampering | Undocumented `Skill(jerry:name)` form could silently fail to match, allowing skills to run without permission validation | TB-1 | Mitigated: Remove undocumented form; use only `Skill(name)`. |
| T-03 | Denial of Service | Deprecated `Bash(:*)` silently fails (Issue #33595), causing all Bash commands to require manual approval, blocking automation | TB-1 | Mitigated: Migrate to `Bash(command *)` space syntax. |
| T-04 | Information Disclosure | `mcp__memory-keeper__*` wildcard permits all Memory-Keeper operations including batch_delete | TB-2 | Accepted risk: Memory-Keeper runs locally; wildcard is appropriate for developer workflow. The `mcp-tool-standards.md` governance restricts which agents can use which tools at the agent definition level (defense in depth). |
| T-05 | Spoofing | Missing Skill permissions for 12 skills could cause approval prompts that train the developer to click "approve" reflexively | TB-1 | Mitigated: Add explicit `Skill(name)` entries for all registered skills. |
| T-06 | Elevation of Privilege | `Bash(python3 *)` entry bypasses H-05 (UV-only constraint) by pre-approving direct Python execution | TB-1 | Mitigated: Remove `Bash(python3 *)` entirely. |
| T-07 | Tampering | `Bash(grep *)` in allow could be used to construct exfiltration commands via Bash | TB-1 | Mitigated: `Bash(grep *)` removed from local `allow` during C4 tournament. The structured Grep tool provides equivalent functionality without Bash exfiltration surface (RT-003). |

### DREAD Scoring (C2 -- Standard criticality)

| Threat | D | R | E | A | D | Score | Priority |
|--------|---|---|---|---|---|-------|----------|
| T-01 (git push auto-allow) | 3 | 5 | 5 | 2 | 3 | 3.6 | MITIGATED |
| T-02 (undocumented Skill form) | 2 | 5 | 3 | 3 | 2 | 3.0 | LOW |
| T-03 (deprecated Bash syntax) | 5 | 5 | 5 | 5 | 3 | 4.6 | HIGH |
| T-04 (MCP wildcard scope) | 2 | 3 | 3 | 2 | 2 | 2.4 | LOW |
| T-05 (approval fatigue) | 3 | 5 | 5 | 3 | 2 | 3.6 | MEDIUM |
| T-06 (python3 H-05 bypass) | 4 | 5 | 5 | 3 | 3 | 4.0 | HIGH |
| T-07 (grep in allow) | 1 | 3 | 3 | 1 | 1 | 1.8 | MITIGATED |

DREAD dimensions: Damage (1-5), Reproducibility (1-5), Exploitability (1-5), Affected Users (1-5), Discoverability (1-5).

### NIST CSF 2.0 Mapping

| Function | Control | Implementation |
|----------|---------|----------------|
| Identify (ID) | ID.AM-2 Software inventory | All 19 skills explicitly listed in permission entries |
| Protect (PR) | PR.AA-1 Access control | `deny` array blocks `curl`/`wget`; `ask` array gates destructive git ops; documented permission syntax only |
| Protect (PR) | PR.DS-1 Data protection | MCP wildcards scoped to known-safe servers; no secrets in settings |
| Detect (DE) | DE.CM-1 Monitoring | Standard permission evaluation path provides audit point; hooks removed to restore default approval flow |
| Respond (RS) | -- | Out of scope for settings file |
| Recover (RC) | -- | Out of scope for settings file |

---

## ADR Summary

| Decision | Choice | Alternatives Rejected |
|----------|--------|-----------------------|
| Skill form | `Skill(name)` only | `Skill(jerry:name)` + `Skill(name)` (redundant, undocumented) |
| Bash syntax | `Bash(command *)` | `Bash(command:*)` (deprecated, silently failing) |
| Overlap resolution | Remove local duplicates of committed entries | Keep all (redundant), move all to committed (breaks per-dev config) |
| MCP entries | Wildcards only | Wildcards + specific tools (redundant) |
| Hooks | Remove (P-020/P-022 violations; WebSearch/WebFetch already in committed `settings.json`) | Keep (violates P-020/P-022 per 4 C4 tournament strategies) |
| python3 entries | Remove | Keep (violates H-05) |

---

*Design Version: 1.1.0*
*Agent: eng-architect*
*Criticality: C2 (Standard -- reversible in 1 session, 1 file affected, but governs all tool permissions)*
*SSOT: `docs/reference/claude-code-permissions.md`*
*Source: PROJ-030-bugs research/skill-permission-bash-syntax-research.md*

# Claude CoWork — Plugin Install Mechanism (distribution constraint research)

> How Jerry actually gets installed into **Claude CoWork** (Claude Desktop app), with the documented limits. Distinct from Claude Code (CLI/IDE). Sourced from CoWork's own docs + Anthropic issue tracker (researched 2026-06-28). Affects the PROJ-031 distribution architecture decision.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Key fact](#key-fact-cowork-is-not-claude-code) | CoWork ≠ Claude Code |
| [Install path](#install-path-gui) | The GUI path |
| [Limits](#limits-official) | Official package limits |
| [Branch-pin uncertainty](#branch-pin-uncertainty) | The open risk to our branch approach |
| [Known issues](#known-issues) | Bugs that may bite |
| [Implication for PROJ-031](#implication-for-proj-031) | Distribution architecture input |
| [Sources](#sources) | Citations |

## Key fact: CoWork is NOT Claude Code

Claude CoWork is Anthropic's agentic knowledge-work system **inside the Claude Desktop app** (macOS/Windows, paid plans, research preview). It "brings Claude Code's agentic capabilities to Claude Desktop" but is a **separate surface**: **no terminal, no `/plugin` command** (typing `/plugin` returns "Unknown Skill"). Plugins/skills/marketplaces are managed through the **GUI**. CoWork terminology: **Plugins** bundle skills + connectors + sub-agents; **Skills** are knowledge modules; **Connectors** are MCP-style integrations.

## Install path (GUI)

- **Add a plugin marketplace from a git repo:** **Customize** (left sidebar) → **Plugins** tab → **Add marketplace** → enter the repository URL → then **Install** the listed plugin(s).
- The repo must contain `.claude-plugin/marketplace.json` (and the plugin's `.claude-plugin/plugin.json`). Both are present on `cowork-skeleton-test`.
- The **Browse** modal (Your organization / Anthropic & Partners / Personal tabs) is **read-only** — the "Add marketplace" control is on the Plugins page, not in Browse. This likely explains "I don't see the option anymore."
- Org admins (Team/Enterprise) add marketplaces at Organization settings → Plugins.

## Limits (official)

From `claude.com/docs/cowork/guide/plugins`, verbatim caps:
- **Files per plugin package: 5,000** ← the constraint PROJ-031 exists to satisfy. Skeleton = ~1,749. ✅
- Marketplace repository archive: 512 MB
- Plugin package uncompressed: 200 MB
- Plugins per marketplace: 500
- Marketplaces per user: 25
- (Skills ZIP-upload path has a community-reported ~200-file cap — too small for the 1,749-file bundle, so the **git-URL/marketplace path is the only viable one**.)

## Branch-pin uncertainty

**OPEN RISK.** CoWork docs only say "enter the repository's URL"; they do **not** document the `.git#<branch>` ref syntax. That syntax IS documented for the shared/Claude Code marketplace system (`...repo.git#v1.0.0`, supports branch/tag `ref`, not `sha`), and our URL `https://github.com/geekatron/jerry.git#cowork-skeleton-test` matches it — but **whether CoWork's GUI field parses the `#ref` is unverified**. If CoWork ignores the fragment and clones the **default branch (`main`, ~6,348 files)**, it exceeds the 5,000-file limit and fails to load. **Must be confirmed empirically.**

## Known issues

- **#66184** (2026-06-08, closed duplicate): claims individual CoWork users can't add a custom marketplace by URL (Personal tab read-only). Conflicts with the official "Add marketplace" doc → feature may be new/rolling out/flaky.
- **#39400** (2026-03-26, "not planned"): marketplace-delivered **skills can fail to mount** in the CoWork container while ZIP-upload of the same content works.
- **#40600 / #40475**: personal-marketplace plugins lost after restart / removed by sync.
- **#28125 / #61271**: **private** repos fail to connect (N/A — our repo is public).

## Implication for PROJ-031

The distribution architecture decision (Q2 in session) chose "separate CI-regenerated branch of the main repo." **If CoWork's GUI cannot pin a non-default branch, that model breaks** (it would load `main`, over the limit). Robust alternatives to weigh in Phase 2/3:
1. **Dedicated repo whose DEFAULT branch is the skeleton** (e.g. `geekatron/jerry-claude-plugin`) — URL needs no `#ref`; guaranteed to load the slim tree.
2. Branch-pin via a `ref` in `marketplace.json` / org `extraKnownMarketplaces` (if CoWork honors it).
3. Confirm CoWork GUI `#branch` support empirically (current test).

This is a hard input to the skeleton-distribution design.

## CONFIRMED 2026-06-28 (on-machine evidence)

CoWork marketplaces are **remote / account-managed**, NOT local-config-driven:
- The Desktop app's `~/Library/Application Support/Claude/config.json` contains the flag **`remote_marketplace_migration_done_v1`** — marketplaces migrated to a server-side model.
- CoWork does NOT read the CLI's `~/.claude/settings.json` / `~/.claude/plugins/known_marketplaces.json`: `jerry@jerry-framework` is enabled there (source git `geekatron/jerry.git`) yet is absent from CoWork.
- No editable local marketplace config exists under the Desktop app support dir.
- CoWork runs an isolated embedded Claude Code in a **full VM sandbox** (`claude-code-vm/`, `lastSeenRequireCoworkFullVmSandbox`), account-scoped (`ownerAccountId`).
- The personal "add marketplace by URL" is absent in this build — the `+` next to "Personal plugins" only opens the read-only remote **Directory** (tooltip: "Browse plugins"). Consistent with the remote-marketplace migration having removed local/personal add (cf. issue #66184).

**Conclusion:** There is NO config-file path for an individual to add a marketplace to CoWork. Distribution is via **org-level registration (server-side, admin)** → appears under "Your organization", or via Anthropic's official directory. The skeleton should therefore be a **dedicated repo whose DEFAULT branch is the slim tree** (org-add uses the default branch; CoWork can't pin a branch), registered once by an org admin. **This supersedes the "branch of `main`" distribution decision (session Q2) for the CoWork target.**

(Validation status: file-count premise proven on `cowork-skeleton-test` (1,749 < 5,000); live in-CoWork load still pending an org-level registration since no personal add path exists.)

## Sources

- https://www.anthropic.com/product/claude-cowork
- https://claude.com/docs/cowork/guide/plugins  (5,000-file limit; Add marketplace by URL; caps)
- https://support.claude.com/en/articles/13837440-use-plugins-in-claude  (2026-05-29)
- https://support.claude.com/en/articles/12512180-use-skills-in-claude  (2026-05-27)
- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- https://code.claude.com/docs/en/discover-plugins  (`.git#ref` syntax — shared system, NOT CoWork-specific)
- https://github.com/anthropics/claude-code/issues/66184 , /39400 , /40600 , /40475 , /28125

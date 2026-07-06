# Claude Plugin / Skill / Marketplace Surfaces — Cross-Surface Scope & Canonical Terminology

> What can a user install, where, and by what mechanism — across every Claude surface — so PROJ-031 can name the Jerry distribution repo accurately. Settles whether "jerry-cowork" is too narrow. Researched 2026-06-30 against current Anthropic docs (code.claude.com, support.claude.com, platform.claude.com) plus on-machine evidence from the prior CoWork install-mechanism study. P-022: doc-vs-build conflicts and unconfirmed items are flagged explicitly; do not read this as full feature parity across surfaces.

> **NAMING RESOLVED 2026-07-02:** the distribution repo is **`geekatron/jerry-claude-plugin`** (family pattern `jerry-<vendor>-plugin`), superseding the `jerry-cowork` placeholder. The surface-scan and naming analysis below are **preserved as the point-in-time finding that fed that decision** — read the `jerry-cowork`/`jerry-plugin` discussion here as historical context, not as the current repo name. See `decisions/repo-naming-options.md` for the recorded rationale.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 — One-paragraph answer](#l0--one-paragraph-answer) | The headline for non-technical stakeholders |
| [Canonical terminology](#canonical-terminology) | Anthropic's vocabulary and how the nouns relate |
| [L1 — Per-surface support matrix](#l1--per-surface-support-matrix) | What each surface supports + install mechanism + branch behavior |
| [Two plugin systems, one repo format](#two-plugin-systems-one-repo-format) | Does ONE git repo serve MULTIPLE surfaces? |
| [Default-branch behavior](#default-branch-behavior) | The constraint that drives repo shape |
| [Confirmed uncertainties (P-022)](#confirmed-uncertainties-p-022) | Where docs and the live build disagree |
| [Naming implications](#naming-implications) | The decision input for PROJ-031 |
| [Methodology](#methodology) | How this was researched + confidence |
| [Sources](#sources) | Citations |

---

## L0 — One-paragraph answer

There is **one distribution artifact** — a git repo containing `.claude-plugin/marketplace.json` (a "plugin marketplace") that lists one or more **plugins** (each bundling **skills** + sub-agents + hooks + connectors/MCP) — and it is consumed by **two distinct plugin systems** that happen to share that exact repo format. System A is **Claude Code** (the terminal CLI *and* the Claude Desktop "Code" section, which is embedded Claude Code): users run `/plugin marketplace add owner/repo` then `/plugin install`, config lives locally in `~/.claude`, and a non-default branch can be pinned with `@ref`/`#ref`. System B is the **Claude apps** marketplace (web claude.ai chat + Desktop "Chat" tab + **CoWork**): users add a marketplace through the GUI (Customize → Plugins → Add from a repository) or, in practice for CoWork, an **org admin registers it server-side**; this path tracks the repo's **default branch only** with no documented branch pinning. The same repo can be registered in *both* systems, so the artifact is genuinely **surface-agnostic** — which is the crux: a name like **"jerry-cowork" under-claims the repo's reach**. The honest caveat (P-022): the surfaces are *not* symmetric — only **Skills** run everywhere; sub-agents/hooks run only in CoWork; Claude Code additionally consumes MCP/LSP/slash-commands — and the apps-side *personal* "add by URL" is unreliable in the current build (a server-side marketplace migration appears to have removed it, leaving org registration as the confirmed CoWork path).

---

## Canonical terminology

Anthropic's nouns, smallest-to-largest, and how they nest:

| Term | Canonical meaning | Install/attach unit? |
|------|-------------------|----------------------|
| **Skill** | A folder with a `SKILL.md` + instructions + optional scripts/resources that Claude loads dynamically for a specialized task. The **atomic capability unit**. | Yes — standalone (ZIP upload) *or* bundled in a plugin. Runs on **every** surface. |
| **Sub-agent (Agent)** | A specialized agent definition bundled in a plugin. | Bundled only. Runs in **CoWork** + **Claude Code**; grayed-out in web/Desktop chat. |
| **Hook** | Lifecycle automation bundled in a plugin. | Bundled only. Runs in **CoWork** + **Claude Code**; grayed-out in web/Desktop chat. |
| **Connector** | A service integration (Google Drive, Gmail, Slack, DocuSign…), **MCP-based**, installed via a **"Connect"/auth flow** — not a git install. Remote MCP connectors landed Jan 2026. | Yes — separate auth flow, not part of the marketplace-repo mechanism. |
| **MCP / LSP server** | Programs a plugin can ship (Claude Code consumes both; CoWork consumes MCP). | Bundled in a plugin (Code surface). |
| **Plugin** | A **package** that bundles skills + connectors + sub-agents + hooks (+ MCP/LSP/slash-commands on the Code surface). The **distributable unit**. | Yes — the thing you "Install". |
| **Marketplace** | A **catalog** = a git repo (or local dir) whose root holds `.claude-plugin/marketplace.json` listing plugins and where to fetch them. The **distribution channel**. | The thing you "add". |
| **Capability** | Umbrella/marketing word for all of the above. | n/a |

**Nesting:** `Marketplace (git repo) → lists Plugins (packages) → each bundles Skills + sub-agents + hooks + connectors/MCP`. The **Skill** is the only component guaranteed to execute on all surfaces; everything heavier degrades to CoWork/Code. Anthropic's own repo-naming convention for the marketplace artifact is **`*-plugins`** (e.g. `anthropics/claude-plugins-official`, `anthropics/knowledge-work-plugins`, the doc's example `acme-corp/claude-plugins`).

---

## L1 — Per-surface support matrix

| Surface | Plugin marketplace? | Standalone Skill? | Connector (MCP)? | Install mechanism | Reads git **default branch**? | Branch pin? | Confidence |
|---|---|---|---|---|---|---|---|
| **Claude Code (CLI)** | Yes (System A) | Yes (skills inside plugins; also `/skills`) | Yes (MCP) | `/plugin marketplace add owner/repo` → `/plugin install name@market`; local `~/.claude` config | **Yes** (default unless ref given) | **Yes** — `@ref` (owner/repo) or `#ref` (git URL); `ref`=branch/tag, **not sha**, for the marketplace source | High |
| **Desktop — "Code" section** | Yes — *same* System A (embedded Claude Code) | Yes | Yes (MCP) | GUI: "+" next to prompt → Plugins → Add plugin → plugin browser (local/SSH sessions). **Not** in cloud sessions. Org-managed plugins appear "same as the CLI". | **Yes** (System A semantics) | Yes (System A) | High |
| **Desktop — "Chat" tab** | Yes (System B) — skills only execute | Yes | Yes | Customize → Plugins → Browse/Install; "Add from a repository" *(see P-022)*. Plugins added yourself "saved locally". | **Yes** (tracks latest commit / default branch) | **Not documented** | Medium-High |
| **CoWork (Desktop)** | Yes (System B) — full plugin runtime (skills + sub-agents + hooks) | Yes (ZIP upload; directory install) | Yes | Org admin: Organization settings → Plugins → Add plugin → GitHub → `owner/repo`. Personal "Add from a repository" per docs *(see P-022)*. Server-side/account-managed (`remote_marketplace_migration_done_v1`). | **Yes — default branch only** (org sync = "latest commit in your repo") | **No documented pin**; on-machine evidence: GUI cannot pin a branch | Medium-High |
| **Web — claude.ai chat** | Yes (System B) — skills only execute (sub-agents/hooks grayed out) | Yes | Yes | Customize → Plugins/Skills → Browse → Install; or `/` to invoke an installed skill inline | **Yes** | **Not documented** | Medium-High |
| **Projects / Chats** | Inherits the account's installed skills/plugins; skills invoked inline via `/` in any (incl. project) chat | Yes (account-level) | Yes | Project = custom instructions + files KB + scoped chats; skills/connectors are **account-scoped**, used *within* project chats | n/a (consumes installed items) | n/a | Medium — *project-scoped attachment of a skill is NOT confirmed; skills appear account-level, available inside project chats* |

**Per-surface notes**

- **Claude Code (CLI):** two-step — add catalog, then install plugins (`/plugin install name@marketplace`); `/reload-plugins` to activate. Sources accepted: GitHub `owner/repo`, any git URL (GitLab/Bitbucket/self-hosted, include `.git`), local path, or a hosted `marketplace.json` URL. Marketplace state stored once per user in `~/.claude/plugins/known_marketplaces.json`.
- **Desktop "Code" section = embedded Claude Code.** Same plugin system as the CLI. Confusingly, the Desktop app surfaces *both* systems, and issue #38008 reports the Code plugin browser sometimes showing **CoWork** plugins instead of CLI plugins — direct evidence the two catalogs are **distinct** even on one machine. Issue #42142: some Desktop builds lack the `/plugin` slash command (use the "+" GUI instead).
- **CoWork** has **no terminal and no `/plugin` command** (typing `/plugin` → "Unknown Skill"); everything is GUI. Requires **both CoWork and Skills enabled** for the org. Org-distributed plugins "appear in both chat (web + Desktop Chat tab) and CoWork" — the org doc **does not list Claude Code** as a target, confirming System B ≠ System A flow.
- **Standalone Skills (ZIP)** is an **orthogonal** path (Customize → Skills → "+" → Upload a skill → ZIP of the skill folder), available on web/CoWork/M365 add-ins. It is **not** a git/marketplace mechanism, and the prior CoWork study noted a community-reported ~200-file ceiling on the ZIP path (too small for Jerry's ~1,749-file bundle → the marketplace/git path is the only viable one for Jerry).

---

## Two plugin systems, one repo format

**Does ONE marketplace/plugin git repo serve MULTIPLE surfaces? — Yes, at the artifact level; via two registration mechanisms.**

- **Shared format:** Both systems consume a repo whose root contains `.claude-plugin/marketplace.json` listing plugins, each with its own `.claude-plugin/plugin.json`. A single repo can be registered in **both** System A (`/plugin marketplace add`) and System B (Customize/org-settings add).
- **Decisive cross-surface evidence:** the Claude Code marketplace doc explicitly references a separate **"claude.ai marketplace sync"** that consumes the *same* repo but with **stricter validation** — it "rejects" non-kebab-case plugin names that Claude Code itself accepts. Two consumers, one repo, surface-specific rules. (This is also why naming/casing must satisfy the strictest consumer.)
- **But the registrations are independent:** System A is local-config-driven (`~/.claude`); System B (CoWork/web) is **server-side/account-managed** (the prior study found the Desktop flag `remote_marketplace_migration_done_v1` and confirmed CoWork does **not** read the CLI's `~/.claude/settings.json`). Adding a repo to one system does **not** auto-propagate it to the other.

**Implication:** the repo itself is **surface-agnostic** (one repo can light up Code + Desktop-Code + Desktop-Chat + Web + CoWork), but a user/admin must register it once per system. The artifact's correct generic name is a **"plugin marketplace"**, not a surface.

---

## Default-branch behavior

This is the constraint that shapes the repo, independent of its name.

| Consumer | Default fetch | Pinning |
|---|---|---|
| **Claude Code — marketplace source** (`/plugin marketplace add`) | Repo **default branch** | `ref` (branch/tag) via `@ref`/`#ref`; **no `sha`** at the marketplace level |
| **Claude Code — plugin source** (inside `marketplace.json`) | Repo **default branch** | `ref` **and** `sha` (exact commit) |
| **Claude apps / CoWork org add** (`owner/repo`) | **Default branch** ("latest commit in your repo") | **No documented pin**; on-machine evidence: GUI **cannot** pin a branch |

**Consequence for PROJ-031:** because the **CoWork/apps path consumes the default branch and cannot reliably pin a non-default branch**, the slim, ≤5,000-file shippable tree must **be the repo's default branch**. That argues for a **dedicated distribution repo** (default branch = the marketplace) rather than a CI-regenerated *branch* of the Jerry monorepo (whose default branch `main` is ~6,348 files, over CoWork's 5,000-file cap). This corroborates the prior study's conclusion and is a hard input regardless of the chosen name.

---

## Confirmed uncertainties (P-022)

1. **Personal "Add from a repository" on the apps/CoWork surface — doc vs. build conflict.** Support docs (2026-05/06) say individuals can add a marketplace by GitHub repo/git URL in Customize → Plugins across web/Desktop/CoWork. The prior on-machine study (2026-06-28) found that path **absent** in the live build (only a read-only Directory under "Personal"; `remote_marketplace_migration_done_v1`; issue #66184), leaving **org-level registration** as the only confirmed CoWork route. **Confidence the personal self-serve add works in CoWork today: LOW.** Org registration: HIGH.
2. **Branch pinning on the apps/CoWork/org path is undocumented and observed-absent.** Treat "default branch only" as the safe assumption until empirically confirmed in a live CoWork org registration.
3. **Project-scoped skills.** Skills appear **account-scoped** and are invocable inside project chats via `/`; official docs do **not** confirm attaching a skill/plugin to a *specific* Project as scoped knowledge. Do not claim project-level plugin scoping.
4. **Live in-CoWork load of the Jerry skeleton is still pending** an org-level registration (no personal add path to test it). File-count premise is proven (1,749 < 5,000); end-to-end mount is not yet verified.
5. **Evolving surface.** The plugin/marketplace mechanism is changing month-to-month (server-side migration, GUI churn). Re-verify before any irreversible naming/registration commitment.

---

## Naming implications

**The single biggest implication:** the distribution artifact is a **surface-agnostic "plugin marketplace" git repo** that serves Claude Code (CLI + Desktop-Code) *and* the Claude apps (CoWork + Desktop-Chat + Web) through the *same* repo format. **"jerry-cowork" is too narrow — it under-claims the repo's reach** and mislabels a multi-surface artifact as a single surface.

Concrete guidance for the naming decision (final call is ps-architect's):

1. **Prefer a surface-agnostic, terminology-aligned name.** Use Anthropic's own canonical noun and convention: the artifact is a *plugin marketplace*, and Anthropic names such repos **`*-plugins`** / `*-marketplace`. Candidates that read true on every surface: **`jerry-plugin`**, **`jerry-plugins`**, **`jerry-marketplace`**, or a neutral **`jerry-dist`**. Avoid encoding a single surface (`-cowork`, `-code`, `-web`) in the repo name.
2. **Let the default branch *be* the product.** Because CoWork/apps consume the default branch and can't pin, name and structure the repo so its **default branch is the shippable marketplace** (a dedicated repo, not a side-branch of the monorepo). A "distribution/marketplace" name reinforces this mental model; a surface name fights it.
3. **Name surface-agnostic, but scope honestly in the README (P-022).** The name should not imply feature parity. Document the asymmetry: **Skills run on all surfaces; sub-agents/hooks only in CoWork (and Claude Code); Claude Code additionally runs MCP/LSP/slash-commands.** If Jerry's plugin leans on sub-agents/hooks, its *full* value is CoWork/Code-only even though the repo is installable everywhere — say so in scope docs, not in the repo name.
4. **Satisfy the strictest consumer.** The claude.ai sync rejects non-kebab-case plugin names that Claude Code tolerates → keep plugin/marketplace `name` fields **lowercase-kebab-case** so the one repo validates on every surface.
5. **If a surface qualifier is unavoidable, qualify by mechanism, not app.** e.g. `jerry-plugin` (the mechanism) beats `jerry-cowork` (one app), because the mechanism — a plugin marketplace — is exactly what is shared.

**Net:** adopt a surface-agnostic marketplace name (recommend the `jerry-plugin`/`jerry-marketplace` family per Anthropic's `*-plugins` convention); retire "jerry-cowork" as the repo name; capture the per-surface component asymmetry and the unconfirmed CoWork personal-add path in scope/README rather than in the name.

---

## Methodology

- **5W1H + source tiering.** Primary sources = Anthropic official docs (`code.claude.com/docs`, `support.claude.com`, `platform.claude.com`) — HIGH credibility. Secondary = Anthropic GitHub issue tracker (build behavior) — HIGH for "observed behavior". Tertiary = prior PROJ-031 on-machine study (`cowork-plugin-install-mechanism.md`) — HIGH for this machine/build, time-stamped 2026-06-28. Community marketplaces/blogs were used only for discovery, not as claim sources.
- **Conflict handling (S-011 spirit).** Where the support docs and the live build disagreed (personal add-by-URL), both are reported with the conflict surfaced rather than resolved in favor of either; confidence labeled per row/claim.
- **Overall confidence:** HIGH on Claude Code mechanics and the shared-repo-format finding; MEDIUM-HIGH on the apps/CoWork mechanics (docs + on-machine, minus the personal-add conflict); the branch-pin-on-apps gap and project-scoping are explicit LOW-confidence/unconfirmed items.

---

## Sources

1. [Discover and install prebuilt plugins through marketplaces — Claude Code Docs](https://code.claude.com/docs/en/discover-plugins) — `/plugin marketplace add` + `/plugin install name@marketplace`; source types (owner/repo, git URL, local, remote `marketplace.json`); `#ref` branch/tag pin; two-step add-then-install model.
2. [Create and distribute a plugin marketplace — Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces) — `.claude-plugin/marketplace.json` schema; **marketplace source supports `ref` not `sha`; plugin source supports `ref` and `sha`; both default to repo default branch**; `@ref`/`#ref` pin syntax; **"claude.ai marketplace sync rejects" non-kebab-case names** (cross-surface, stricter validation).
3. [Desktop application — Claude Code Docs](https://code.claude.com/docs/en/desktop) — Desktop "Code" section is embedded Claude Code; "+ → Plugins → Add plugin" GUI in local/SSH sessions; org-managed plugins "same as the CLI"; **not** available in cloud sessions.
4. [Use plugins in Claude — Claude Help Center](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) — apps install path (Customize → Plugins → Browse/Install); "Add from a repository (GitHub repo or git URL)"; **"skills bundled in a plugin work across all three; hooks and sub-agents run only in Cowork, so they appear grayed out in chat"**; plugin = bundles skills + connectors + sub-agents.
5. [Browse skills, connectors, and plugins in one directory — Claude Help Center](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory) — unified Directory across web/Desktop/Chat-tab/CoWork (**Code not listed**); skill vs connector vs plugin install actions ("+"/Install vs Connect auth flow); directory versions read-only.
6. [Manage plugins for your organization — Claude Help Center](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization) — org add = Organization settings → Plugins → Add plugin → GitHub → `owner/repo`; **"latest commit in your repo" (default-branch tracking), no documented ref pin**; appears in "chat (web + Desktop Chat tab) and CoWork", **Code not listed**; **CoWork + Skills must both be enabled**.
7. [Use skills in Claude — Claude Help Center](https://support.claude.com/en/articles/12512180-use-skills-in-claude) — Skill = specialized knowledge/workflow; **ZIP upload** path (Customize → Skills → "+" → Upload a skill); directory install in CoWork; surfaces web/CoWork/M365 add-ins.
8. [Agent Skills — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Skill = folder of instructions/scripts/resources loaded dynamically; authored in Claude Code, via API, or claude.ai settings.
9. [anthropics/claude-code issue #38008](https://github.com/anthropics/claude-code/issues/38008) — Desktop Code plugin browser shows **CoWork** plugins instead of **CLI** plugins → the two catalogs are distinct.
10. [anthropics/claude-code issue #42142](https://github.com/anthropics/claude-code/issues/42142) — some Desktop builds lack the `/plugin` command (GUI add instead).
11. [anthropics/claude-code issue #66184](https://github.com/anthropics/claude-code/issues/66184) — individual CoWork users reportedly cannot add a custom marketplace by URL (Personal tab read-only) — basis for the personal-add uncertainty.
12. [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) — Anthropic's open marketplace repo for CoWork; `*-plugins` naming convention; default Knowledge Work marketplace.
13. [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — official marketplace repo; `*-plugins` naming convention; auto-available in Claude Code.
14. [claude.com/platform/marketplace](https://claude.com/platform/marketplace) — Anthropic Marketplace positioned as shipping inside CoWork, claude.ai web, and Claude Code (one directory, multiple surfaces).
15. Prior PROJ-031 study — `projects/PROJ-031-cowork-skeleton/research/cowork-plugin-install-mechanism.md` — on-machine evidence (2026-06-28): `remote_marketplace_migration_done_v1`; CoWork ignores `~/.claude`; no personal add path; org-level (default-branch) registration is the confirmed CoWork route; 5,000-file cap; ZIP ~200-file cap.

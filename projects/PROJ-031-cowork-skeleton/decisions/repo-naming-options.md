---
id: "PM-MS-001"
type: "naming-options"
title: "Distributable Jerry Skeleton -- Repository Naming Options"
agent: "pm-market-strategist"
status: "draft"
mode: "delivery"
risk_domain: "business-viability-risk"
sensitivity: "internal"
created: "2026-06-30"
last_validated: "2026-07-02"
frameworks_applied:
  - "Positioning Framework (Dunford) -- frame-of-reference / market-category lens"
cross_refs:
  - "ADR-PROJ031-001-skeleton-distribution-strategy"
  - "ADR-PROJ031-003-credential-protection-supply-chain"
  - "research/cowork-plugin-install-mechanism.md"
decision_status: "RESOLVED 2026-07-02 -- USER selected geekatron/jerry-claude-plugin (family pattern jerry-<vendor>-plugin), superseding the jerry-cowork placeholder. Propagated to ADR-PROJ031-001/ADR-PROJ031-003 and the live spec/design artifacts. See the Decision (RESOLVED 2026-07-02) section below."
---

# Repository Naming Options: Distributable Jerry Skeleton

> Scored naming options for the **dedicated GitHub repository** (`geekatron/<name>`) whose **default branch IS the installable Jerry Claude plugin** (`projects/`- and `tests/`-stripped, ~1,417 files). Replaces the inaccurate placeholder `jerry-cowork`. This is an options analysis feeding a USER decision and a subsequent ADR-PROJ031-001 amendment -- it does **not** itself rename anything.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Decision (RESOLVED 2026-07-02)](#decision-resolved-2026-07-02) | The recorded outcome: chosen name, family pattern, and rationale |
| [L0: Executive Summary](#l0-executive-summary) | Recommendation and why it matters, in plain language |
| [Problem and Naming Mandate](#problem-and-naming-mandate) | What is being named, what must NOT change, the accuracy failure |
| [Naming Criteria (Weighted)](#naming-criteria-weighted) | 9 explicit, weighted criteria with the positioning lens |
| [Candidate Names](#candidate-names) | 10 candidates: communicates, positioning, pros, cons, accuracy note |
| [Also Considered (Not Shortlisted)](#also-considered-not-shortlisted) | `jerry-pack`, `jerry-bundle`, `jerry-release` -- brief disposition |
| [Scored Matrix](#scored-matrix) | Candidates x criteria, weighted totals, ranking |
| [Recommendation](#recommendation) | Top 3 with conditional logic and justification |
| [Naming Risks](#naming-risks) | Trademark, collision, SEO, taxonomy-confusion |
| [Dependency on Surface Research](#dependency-on-surface-research) | Where the right name hinges on ps-researcher findings (P-022) |
| [Decision Status and Next Steps](#decision-status-and-next-steps) | What happens after this artifact |
| [Multi-Vendor Naming Scheme (Re-Evaluation)](#multi-vendor-naming-scheme-re-evaluation) | NEW (2026-06-30): vendor-neutral vs vendor-namespaced; recommended scheme, Claude repo name, trademark-safe fallback, re-score vs `jerry-plugin` |

---

## Decision (RESOLVED 2026-07-02)

**Chosen repository name: `geekatron/jerry-claude-plugin`.** The dedicated distribution repository whose default branch IS the installable Jerry Claude plugin (`projects/`- and `tests/`-stripped, ~1,417 files) is named **`geekatron/jerry-claude-plugin`**. This **supersedes the placeholder `jerry-cowork`** used in the earlier ADR-PROJ031-001/ADR-PROJ031-003 drafts and PLAN.md.

**Naming family (forward scheme): `jerry-<vendor>-plugin`.** Future vendor-specific distributions follow the same pattern — e.g. `jerry-openai-plugin`, `jerry-gemini-plugin` — while `geekatron/jerry` remains the vendor-neutral source framework.

**Rationale:**

- **Vendor-namespaced, multi-vendor future-proofing.** Embedding the vendor (`claude`) in the repo name mirrors the agreed mental model — framework = vendor-neutral; each distribution = vendor-specific — and lets OpenAI/Google distributions slot in without a rename or an asymmetric scheme. This is the minimax-regret choice analyzed in [Multi-Vendor Naming Scheme (Re-Evaluation)](#multi-vendor-naming-scheme-re-evaluation): a vendor-neutral name on a vendor-specific artifact is itself a false frame (the same error class as `jerry-cowork`, inverted from over-narrow *surface* to over-broad *vendor scope*).
- **Avoids a costly rename of a deployed distribution repo.** Naming is free now (pre-deployment); a later rename would break install URLs, the `jerry-framework` marketplace registration, and force every user to re-install. The vendor-namespaced name is cheap insurance whose worst case (multi-vendor never ships) is merely cosmetic.
- **Trademark: low (non-zero) risk, uniform across the vendor family.** Per [`research/multivendor-naming-and-trademark.md`](../research/multivendor-naming-and-trademark.md), embedding "claude" is **LIKELY-OK IN PRACTICE / LOW-BUT-NONZERO RISK**, resting on *nominative fair use* (a legal defense identifying which vendor's distribution this is, not an Anthropic-granted safe harbor; the source doc's P-022 legal caveat applies — consult counsel if the name becomes brand-load-bearing). That residual risk is uniform across the `jerry-<vendor>-plugin` family, so it does not discriminate between candidates; it clears — at an accepted low level — the trademark GATE this options analysis had left open.
- **Explicit `-plugin` over bare `jerry-claude`.** The USER chose the explicit form `jerry-claude-plugin` (retaining the "what is it" token) over the bare `jerry-claude` that this analysis had ranked highest, accepting the "-plugin" token's mildly weaker scheme-generalization in exchange for immediate clarity that the repo IS the installable plugin.

**Status of this document:** the options analysis, scored matrices, and the `jerry-cowork` rejected-placeholder discussion below are **retained verbatim** as this decision record's supporting evidence. This section records the outcome; it does not revise the analysis.

---

## L0: Executive Summary

The new repo is the **installable, distributable form of Jerry** -- a slim tree whose default branch is read directly by Claude's plugin/marketplace mechanism. The placeholder `jerry-cowork` is wrong because it implies the artifact is only for the Claude Desktop **CoWork** surface, when the same plugin is meant to install across Claude Code (CLI), the Desktop **Code** section, **CoWork**, and **Web/Chats**. The repo name is the first "frame of reference" a developer or org admin sees; a surface-specific name creates false scope before anyone reads a line.

**Top 3 recommendations (scored):**

1. **`geekatron/jerry-plugin`** (4.85) -- names exactly what the artifact *is*. CoWork's own documentation calls a bundle of skills+connectors+sub-agents a **"Plugin,"** and the shared marketplace install path is the confirmed mechanism for Claude Code + CoWork. **Conditional** on the ps-researcher scan confirming Web/Chats and the Desktop Code section share that same plugin primitive (see [Dependency](#dependency-on-surface-research)).
2. **`geekatron/jerry-dist`** (4.77) -- the **surface-robust hedge**. "Distributable" names the *purpose*, not the install primitive, so it stays accurate no matter how each surface consumes the repo. Recommend as the default if the team wants to commit now without waiting on the surface scan, or if that scan reveals mechanism divergence.
3. **`geekatron/jerry-distribution`** (4.64) -- identical positioning to `jerry-dist`, traded brevity for non-developer legibility (CoWork/Web admins). Choose only if clarity-for-non-devs outweighs terseness.

All three are surface-agnostic, family-consistent with `jerry`/`jerry-framework`, and carry no trademark exposure. The names to avoid are `jerry-cowork` (false scope), `jerry-lite` (false capability reduction), `jerry-skills` (wrong in CoWork's own taxonomy), `jerry-marketplace` (overclaims a multi-plugin store), and `jerry-claude` (Anthropic trademark in the repo name).

---

## Problem and Naming Mandate

**What is being named:** a GitHub **repository** under the `geekatron` org. Its default branch is the `projects/`- and `tests/`-stripped Jerry skeleton (~1,417 files, under CoWork's ~5,000-file ceiling) that the marketplace mechanism installs as the Jerry plugin. ADR-PROJ031-001 (amended 2026-06-28) refers to this repo by the placeholder `geekatron/jerry-cowork` throughout; this analysis supplies the candidates to replace it.

**What MUST stay consistent (do NOT rename -- out of scope here):**

| Identifier | Value | Where it lives | Why fixed |
|-----------|-------|----------------|-----------|
| Marketplace `name` | `jerry-framework` | `.claude-plugin/marketplace.json` | Marketplace identity; already published |
| Plugin `name` | `jerry` | `.claude-plugin/plugin.json` | Plugin identity; what users enable (`jerry@jerry-framework`) |
| Org | `geekatron` | GitHub org | Owner namespace |
| Full-framework repo | `geekatron/jerry` | GitHub | Canonical source (~6,344 files) -- **already taken** |

The repo name is a **fourth, independent identifier** layered on top of these. A clean reading should be possible: *"the `<repo>` repository distributes the `jerry` plugin via the `jerry-framework` marketplace."*

**The accuracy failure being corrected:** `jerry-cowork` couples the repo to a single surface. Per the surface research, CoWork is explicitly **not** Claude Code -- it is a separate Desktop surface -- yet both consume the *same* `.claude-plugin/` marketplace mechanism, and the artifact targets still more surfaces. Naming the shared, surface-agnostic distribution after one surface is the exact over-narrowing this exercise removes.

---

## Naming Criteria (Weighted)

**Positioning lens (Dunford):** a repository name is a compressed *frame of reference*. The name tells the reader which category the thing belongs to and how to evaluate it. The dominant failure mode for this artifact is a **false frame** -- a name that claims a scope (one surface), a form (a reduced product), or a channel (a store) that the artifact does not actually occupy. Criteria are therefore weighted toward accuracy and claim-discipline.

| # | Criterion | Weight | What a top score looks like |
|---|-----------|--------|------------------------------|
| C1 | **Accuracy / surface-agnostic** | 0.22 | Implies no single surface (not CoWork-only, not CLI-only); names the shared distribution, not one consumer |
| C2 | **No over/under-claim** | 0.16 | Does not claim to *be* the framework, a *marketplace/store*, a *release snapshot*, or a *capability-reduced* edition; does not under-claim as "just skills/a skeleton" |
| C3 | **Clarity of purpose** | 0.15 | A reader infers "installable/distributable Jerry" with no explanation |
| C4 | **Family consistency** | 0.12 | Reads as part of the `jerry` / `jerry-framework` family; pairs cleanly with plugin `jerry` |
| C5 | **Brevity & memorability** | 0.10 | Short, typeable, easy to say aloud and in a URL |
| C6 | **GitHub repo convention** | 0.08 | Lowercase-hyphen; suffix carries a conventional, well-understood meaning |
| C7 | **Discoverability / SEO** | 0.08 | Findable; clearly distinct from `geekatron/jerry` so the two do not blur |
| C8 | **Future-proofing** | 0.05 | Stays accurate as surfaces/architecture evolve (the trap `cowork` already fell into) |
| C9 | **Collision / trademark safety** | 0.04 | No hard collision with existing repos; no third-party trademark (e.g. "Claude") in the name |

*Weights sum to 1.00. Scores are 1 (poor) to 5 (excellent). Weighted total = sum(score x weight), range 1.00-5.00.*

---

## Candidate Names

Each candidate is `geekatron/<name>`. "Accuracy note" states explicitly whether the name over-claims, under-claims, or is accurate on scope.

| Candidate | What it communicates + positioning | Pros | Cons | Accuracy note |
|-----------|-------------------------------------|------|------|----------------|
| **jerry-plugin** | "The Jerry Claude **plugin**." Frames the repo as the installable plugin itself -- the artifact's true identity in Claude's ecosystem (CoWork docs literally call it a "Plugin"). | Names exactly what it is; "plugin" is the cross-surface install primitive, not a surface; highly discoverable; pairs cleanly with plugin `jerry`; conventional. | Three `jerry-*` identifiers (repo/marketplace/plugin) coexist -- mild layering load; minor exposure if Anthropic later renames the "plugin" primitive. | **Accurate** -- neither over- nor under-claims, *provided* the plugin mechanism is the shared install path across all target surfaces (see Dependency). |
| **jerry-dist** | "The **distributable** build of Jerry." Frames by *purpose* (distribution) rather than mechanism -- mechanism-neutral. | Accurate regardless of per-surface mechanism; very short; `dist` is a universally understood software convention; future-proof; zero trademark/collision risk. | `dist` reads as a generated build-artifact folder, which can imply "non-canonical/throwaway"; mildly jargony for non-developer CoWork/Web admins. | **Accurate** -- claims only "this is the distributable," which is precisely true and surface-independent. |
| **jerry-distribution** | Same as `jerry-dist`, spelled out. Frames by purpose with maximum legibility. | Clearer than `dist` for non-developers; fully accurate; future-proof; no trademark/collision risk. | Long for a repo name; less conventional than the `dist` short form; weaker brevity. | **Accurate** -- identical claim profile to `jerry-dist`. |
| **jerry-skeleton** | "The stripped **skeleton** of Jerry." Echoes the PROJ-031 project name and the strip technique. | Surface-agnostic; truthfully describes the stripped derivation; matches internal vocabulary. | "Skeleton" implies an incomplete scaffold/template to *build on*, not a finished installable plugin; an installer is the audience, not a forker. | **Under-claims** -- the artifact is a fully functional plugin, not a starter skeleton; risks signalling "not ready to use." |
| **jerry-slim** | "A **slimmed-down** Jerry." Frames by reduced size. | Short; truthfully signals the strip (`projects/`+`tests/` removed). | "Slim" is relative/vague and implies reduced *capability*; if the tree grows, "slim" blurs. | **Borderline under-claim** -- capability is unchanged (only history/tests removed); "slim" can read as feature-reduced. |
| **jerry-lite** | "A **lite** edition of Jerry." Frames as a reduced tier. | Familiar `X-lite` pattern; short. | "Lite" strongly implies *fewer features* and the existence of a "full/pro" tier -- neither is true; misleads on capability. | **Under-claims capability (misleading)** -- the plugin is the full framework minus project history/tests, not a reduced product. |
| **jerry-marketplace** | "The Jerry **marketplace**." Frames by distribution channel (the repo does hold `marketplace.json`). | Surface-agnostic; ties to the marketplace mechanism; technically the repo contains the marketplace manifest. | "Marketplace" connotes a *store of many plugins*; the marketplace `name` is already `jerry-framework`; this is one plugin's home, not a catalog. | **Over-claims** -- implies a multi-plugin store; also collides conceptually with the existing `jerry-framework` marketplace identity. |
| **jerry-skills** | "Jerry's **skills**." Frames by content (Jerry is skills-heavy). | Short; "skills" is recognizable Claude vocabulary. | CoWork's taxonomy treats **Plugins, Skills, and Connectors as three different things**; Jerry ships as a *Plugin* that bundles skills + agents + hooks + rules -- not as a "Skill." | **Under-claims AND mis-categorizes** -- names a subset and uses the wrong primitive in Claude's own taxonomy. |
| **jerry-claude** | "Jerry **for Claude**." Frames by target ecosystem. | Signals the Claude ecosystem; discoverable; scope (Claude-wide) is broadly right. | Puts a third-party trademark ("Claude," Anthropic) in the repo name -- implies affiliation/endorsement; vendor names in repo names are unconventional. | **Scope-accurate but trademark-risky** -- does not over/under-claim function, but the "Claude" usage is the problem. |
| **jerry-kit** | "A ready-to-use Jerry **kit**." Frames as a packaged toolkit. | Short; friendly; `-kit` is an established suffix; surface-agnostic; no trademark/collision risk. | "Kit" is vague on *installable/distributable*; mildly implies a starter/assembly kit. | **Mild under-claim** -- "kit" under-specifies that this is the canonical installable plugin, but does not actively mislead. |

---

## Also Considered (Not Shortlisted)

Brief disposition of the remaining names from the brief (full scoring omitted -- each fails a high-weight criterion clearly):

| Candidate | Disposition | Reason |
|-----------|-------------|--------|
| **jerry-pack** | Rejected from shortlist | "Pack" is vague packaging language; under-specifies purpose; less conventional than `dist`/`plugin`. No clear advantage over `jerry-kit`, which scores similarly and reads better. |
| **jerry-bundle** | Rejected from shortlist | "Bundle" implies *several things bundled together*; the repo is one plugin. Mildly inaccurate framing; redundant with `jerry-pack`/`jerry-kit`. |
| **jerry-release** | Rejected from shortlist | "Release" implies a versioned, point-in-time snapshot -- and collides with GitHub's own *Releases* feature. The repo is a *living* default branch regenerated every release, not a release artifact. Misleading on the artifact's nature. |

---

## Scored Matrix

Scores 1-5 per criterion; weighted total = sum(score x weight). Criteria legend: **C1** Accuracy/surface-agnostic (.22), **C2** No over/under-claim (.16), **C3** Clarity (.15), **C4** Family consistency (.12), **C5** Brevity (.10), **C6** GH convention (.08), **C7** Discoverability/SEO (.08), **C8** Future-proof (.05), **C9** Collision/trademark (.04).

| Rank | Candidate | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | **Total** |
|------|-----------|----|----|----|----|----|----|----|----|----|-----------|
| 1 | **jerry-plugin** | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | **4.85** |
| 2 | **jerry-dist** | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 5 | **4.77** |
| 3 | **jerry-distribution** | 5 | 5 | 5 | 5 | 3 | 4 | 4 | 5 | 5 | **4.64** |
| 4 | jerry-kit | 5 | 3 | 3 | 5 | 5 | 4 | 3 | 4 | 5 | **4.09** |
| 5 | jerry-slim | 5 | 3 | 3 | 5 | 5 | 4 | 3 | 3 | 5 | **4.04** |
| 6 | jerry-claude | 4 | 4 | 4 | 5 | 4 | 3 | 4 | 3 | 1 | **3.87** |
| 7 | jerry-skeleton | 5 | 2 | 3 | 5 | 3 | 4 | 3 | 2 | 5 | **3.63** |
| 8 | jerry-lite | 5 | 1 | 2 | 5 | 5 | 4 | 3 | 2 | 5 | **3.52** |
| 9 | jerry-skills | 4 | 2 | 2 | 5 | 4 | 4 | 3 | 2 | 3 | **3.28** |
| 10 | jerry-marketplace | 4 | 1 | 2 | 5 | 2 | 3 | 3 | 2 | 3 | **2.84** |

**Observations:** The top 3 separate from the field on the two highest-weight criteria (C1 accuracy, C2 claim-discipline) -- they are the only candidates scoring 5/5 on both. `jerry-plugin` leads on clarity + discoverability; `jerry-dist` leads on brevity + future-proofing. The mid-pack (`kit`, `slim`) is "harmless but vague"; the bottom (`lite`, `skills`, `marketplace`) actively mis-frames scope, form, or channel. Note `jerry-cowork` (the placeholder) is not scored but would fail C1 outright (false single-surface scope) -- it is the baseline this exercise rejects.

---

## Recommendation

**Recommend a conditional decision, resolved by the ps-researcher surface scan:**

### Primary (conditional): `geekatron/jerry-plugin`

Choose **if** ps-researcher confirms the `.claude-plugin/` plugin/marketplace mechanism is the shared install path across all four named surfaces (Claude Code CLI, Desktop Code, CoWork, Web/Chats). Justification:

- It names the artifact's **true identity**. The repo *is* the Jerry plugin's distributable home; CoWork's documentation uses "Plugin" as the umbrella term for exactly this kind of bundle.
- Highest accuracy + clarity + discoverability of any candidate, with full family consistency (`geekatron/jerry-plugin` distributes plugin `jerry` via marketplace `jerry-framework`).
- Surface-agnostic by construction: "plugin" denotes the install primitive, which is shared, not any one surface.

### Surface-robust default (no dependency): `geekatron/jerry-dist`

Choose **if** the team wants to commit **now** without waiting on the scan, **or if** the scan reveals that some surfaces (plausibly Web/Chats) use a different primitive than "plugin." Justification:

- "Distributable" names the **purpose**, which is true on every surface regardless of the install primitive -- so it carries **no surface dependency** and is the safest hedge.
- Best future-proofing and brevity; zero trademark/collision exposure.
- The only real cost is mild jargon ("dist") for non-developer admins -- mitigated by `jerry-distribution` if that audience matters.

### Clarity variant: `geekatron/jerry-distribution`

Same positioning as `jerry-dist`; pick only if non-developer legibility (CoWork/Web org admins) is weighted above brevity.

**Net guidance for the USER decision:** if the surface scan returns "all four share the plugin mechanism," go **`jerry-plugin`**. If the scan is pending or returns "mechanism varies by surface," go **`jerry-dist`**. Both are defensible; the choice is genuinely a function of one open research finding, which is why this artifact does not assert a single winner (P-022).

---

## Naming Risks

| Risk | Affected candidates | Assessment |
|------|--------------------|------------|
| **Third-party trademark** | `jerry-claude` | "Claude" is Anthropic's trademark. A repo named `jerry-claude` can imply affiliation or endorsement. Avoid vendor trademarks in the repo name; reference the platform in the description/README instead. The top-3 names carry no trademark exposure. |
| **Collision with `geekatron/jerry`** | all (low) | All candidates are suffixed and cannot hard-collide with the existing `jerry` repo. Residual *conceptual* blur (two `jerry*` repos) is mitigated by a name that signals "distributable/installable" (`plugin`, `dist`) so the slim repo is clearly the derived artifact, not the source. README + GitHub topics should explicitly state "distributable plugin build; source lives at `geekatron/jerry`." |
| **Marketplace-identity confusion** | `jerry-marketplace` | The marketplace `name` is already `jerry-framework`. A repo called `jerry-marketplace` competes with that identity and implies a multi-plugin store. Avoid. |
| **Taxonomy mis-categorization** | `jerry-skills` | CoWork distinguishes Plugins vs Skills vs Connectors. Jerry ships as a *Plugin*; calling the repo `jerry-skills` mislabels the primitive and undersells the bundle. Avoid. |
| **SEO / discoverability** | `jerry-dist`, `jerry-distribution` | "jerry" alone is generic (common name; "jerry-rig"), so a meaningful suffix actually *aids* disambiguation. `jerry-plugin` is the most search-aligned ("jerry plugin"); `dist`/`distribution` are findable but less searched. All acceptable. |
| **Future-proofing** | `jerry-cowork`, `jerry-lite`, `jerry-skeleton`, `jerry-release` | Surface-bound, era-bound, or form-bound terms become inaccurate as the artifact evolves (`cowork` already did). The top 3 avoid this; `jerry-plugin` carries only minor exposure if Anthropic renames the "plugin" primitive. |

---

## Dependency on Surface Research

**Honest flag (P-022):** the single best name depends on a finding this artifact does not own.

- **Confirmed by the existing research** (`research/cowork-plugin-install-mechanism.md`): Claude Code and CoWork both install via the shared `.claude-plugin/marketplace.json` + `plugin.json` marketplace mechanism reading a repo's **default branch**, and CoWork's own term for the bundle is **"Plugin."** This is strong support for `jerry-plugin`'s accuracy on those two surfaces.
- **Open (the concurrent ps-researcher task):** whether the **Desktop Code section** and **Web/Chats** consume that *same* "plugin" primitive, or a different one (e.g. a distinct "Skills"/"Connectors" path, or a web-side mechanism). The brief instructs assuming "surface-agnostic distribution of the Jerry plugin" as the positioning.

**How the finding changes the matrix:**

| ps-researcher finding | Effect | Resulting top pick |
|-----------------------|--------|--------------------|
| All four surfaces share the plugin/marketplace mechanism | `jerry-plugin` C1 stays 5; accuracy fully holds | **`jerry-plugin`** |
| Mechanism varies by surface (some non-"plugin") | `jerry-plugin` C1 drops to ~4 (names one primitive among several); `jerry-dist` unaffected (purpose-named) | **`jerry-dist`** |
| Scan still pending at decision time | Avoid committing to a mechanism-named repo | **`jerry-dist`** (commit-safe now) |

Names whose accuracy is **mechanism-dependent:** `jerry-plugin`, `jerry-marketplace`, `jerry-skills`. Names that are **mechanism-independent** (purpose- or family-named, safe regardless of scan): `jerry-dist`, `jerry-distribution`, `jerry-kit`, `jerry-slim`.

---

## Decision Status and Next Steps

**Status: PENDING.** This artifact is an options analysis, not a decision. It does **not** rename any repo, manifest, or ADR.

1. **USER decision** -- select among `jerry-plugin` (conditional) / `jerry-dist` (robust default) / `jerry-distribution` (clarity variant), informed by the ps-researcher surface scan.
2. **ADR-PROJ031-001 amendment** (separate, authorized task -- **not** performed here) -- replace the `geekatron/jerry-cowork` placeholder with the chosen name across ADR-PROJ031-001 (and propagate to ADR-PROJ031-003 references to the dedicated repo / push target).
3. **Manifest check** -- confirm no change is needed to marketplace `name: jerry-framework` or plugin `name: jerry` (the repo rename is independent of both; expected: no manifest edits).
4. **README/topics** -- on repo creation, state explicitly that this is the distributable plugin build and that source lives at `geekatron/jerry`, to neutralize the `jerry`/`<repo>` conceptual-blur risk.

---

## Multi-Vendor Naming Scheme (Re-Evaluation)

> **Added 2026-06-30** in response to a new hard requirement: **multi-vendor future-proofing.** Jerry may later ship vendor-specific distributions for **OpenAI** and **Google**, whose packaging formats differ from Claude's, so per-vendor distribution repos may be inevitable. This section re-evaluates **vendor-NEUTRAL (A)** vs **vendor-NAMESPACED (B)** naming, recommends a SCHEME for all vendors, names the Claude repo under it, supplies a trademark-safe fallback, and re-scores against the prior top pick `jerry-plugin`. **It does not edit any ADR.**

### Why the new requirement reframes the problem

The prior analysis optimized for a **single-vendor (Claude-only)** world, where `jerry-plugin` ("names exactly what it *is*") won at 4.85. The multi-vendor requirement changes the **frame of reference**, which is the unit a repo name actually carries (Dunford). The agreed mental model is:

> `geekatron/jerry` = the **vendor-neutral FRAMEWORK**; each distribution repo = **vendor-specific.**

Under that model, a **vendor-neutral name on a vendor-specific artifact is itself a false frame** -- the same class of error the prior analysis rejected in `jerry-cowork` (over-narrow *surface*), now inverted to over-broad *vendor scope*. `jerry-plugin` silently implies "the (one, canonical) Jerry plugin"; the moment `jerry-openai-*` exists, that name reads as an umbrella it is not, and "plugin for which platform?" becomes a live ambiguity.

**Evidence the vendor formats genuinely differ (load-bearing for the scheme):**

| Vendor | Packaging unit (2026) | Install primitive | Packaging word = "plugin"? |
|--------|----------------------|-------------------|----------------------------|
| Anthropic / Claude | **Plugin** (Code, CoWork) / **Skills** (Web, Chat) | `.claude-plugin/marketplace.json`, reads default branch | baseline |
| OpenAI / ChatGPT | **App** (Apps SDK, MCP-based). "Plugins" retired Mar 2024 -> GPTs -> Apps | Apps SDK / MCP (open-sourced) | **No -- "App"** |
| Google / Gemini | **Extension** (`gemini-extension.json`; bundles prompts, MCP servers, commands, hooks, sub-agents, skills) | `gemini extensions install <GitHub URL>` | **No -- "Extension"** |

The only shared substrate across all three is **MCP**, not a packaging word. Consequence: a scheme that bakes Claude's "plugin" vocabulary into the pattern produces **inaccurate names for two of three vendors** -- `jerry-openai-plugin` (it is an *App*) and `jerry-gemini-plugin` (it is an *Extension*). A multi-vendor scheme must therefore assert **vendor**, not **packaging unit**. (This also resolves the brief's minor-accuracy note: even for Claude, "-plugin" is only right on Code/CoWork; on Web/Chat the same repo loads as **skills** -- so "plugin" is surface-bound *and* vendor-bound.)

### (A) vendor-neutral vs (B) vendor-namespaced

| Dimension | (A) Vendor-neutral -- `jerry-plugin` / `jerry-dist` | (B) Vendor-namespaced -- `jerry-claude*` (+ `jerry-openai*`, `jerry-gemini*`) |
|-----------|------------------------------------------------------|------------------------------------------------------------------------------|
| Accuracy in a multi-vendor world | **False/ambiguous frame** -- implies a single canonical plugin or an umbrella | **Accurate** -- the name states which vendor's distribution this is |
| Fit to the agreed mental model | **Contradicts it** (neutral name for a vendor-specific repo) | **Mirrors it** (framework neutral; distributions vendor-specific) |
| Scheme consistency across vendors | None -- second vendor forces either a rename or an inconsistent pair (`jerry-plugin` + `jerry-openai-app`) | Clean, predictable pattern for every vendor |
| Simplicity today (Claude-only) | **Simplest** | Slightly longer; one extra token |
| Trademark exposure | **None** | **"Claude" is an Anthropic mark** -- the gating risk (handled below) |
| YAGNI risk | n/a | Real but **cosmetic** (see asymmetry) |

### The decisive factor: rename-cost asymmetry (cheap insurance)

Naming happens **pre-deployment**, where **every candidate costs the same to choose: zero.** The asymmetry is entirely in the *future switching cost*:

| Choice now | If multi-vendor ships later | If multi-vendor never ships |
|------------|-----------------------------|------------------------------|
| (A) neutral `jerry-plugin` | **HIGH regret** -- a rename breaks install URLs, the `jerry-framework` marketplace registration, and forces every user to re-install; *or* you freeze an inconsistent, misleading scheme | none |
| (B) namespaced `jerry-claude` | **~zero regret** -- the scheme scales (`jerry-openai`, `jerry-gemini`); no rename | **LOW (cosmetic) regret** -- a marginally longer name that is *still 100% accurate* ("the Claude distribution of Jerry") |

This is a minimax-regret decision, and (B) dominates: its worst case is cosmetic, while (A)'s worst case is **channel-breaking**. The one moment a rename is free is *now*; spending it on the future-proof name is cheap insurance. The YAGNI objection (steelman: "Jerry is Claude-only; OpenAI/Google distributions may never ship; don't pay for an unused future") is real but defused by the fact that the future-proof name has **no accuracy cost even if the future never arrives** -- `jerry-claude` is correct today regardless.

### Recommended scheme

**Primary scheme: `jerry-<vendor>`** (bare vendor token; packaging word omitted because it does not generalize and is already surface-inaccurate for Claude).

| Role | Name |
|------|------|
| **Claude repo (PRIMARY -- uses "claude")** | **`geekatron/jerry-claude`** |
| Future OpenAI repo | `geekatron/jerry-openai` |
| Future Google repo | `geekatron/jerry-gemini` (or `jerry-google`) |
| **Explicit-form variant** (if a "what is it" token is wanted) | `jerry-<vendor>-dist` -> **`geekatron/jerry-claude-dist`** |

- **Why bare `jerry-<vendor>`:** maximally consistent, brief, and conventional for vendor variants; "which packaging format" is conveyed by the README, GitHub topics, and the marketplace manifest -- not forced into the repo name, where it would misname two of three vendors.
- **Why not the proposed `jerry-claude-plugin`:** fine for the Claude repo *in isolation*, but **weak as a SCHEME** -- the "-plugin" token is Claude-Code/CoWork vocabulary that mislabels `jerry-openai-*` (App) and `jerry-gemini-*` (Extension), and is already wrong for Claude Web/Chat (skills). It re-commits the `jerry-cowork` over-specificity error one layer down (format instead of surface).
- **If a form token is desired, use the neutral one (`-dist`), not `-plugin`:** "distribution" is mechanism- and vendor-agnostic, so `jerry-<vendor>-dist` stays accurate across all three vendors *and* on all Claude surfaces. It is the strictly better way to satisfy the instinct behind `jerry-claude-plugin`.

### Trademark: treat as a GATE (P-022)

"Claude" is an Anthropic trademark. A repo named `jerry-claude*` can imply affiliation/endorsement. Treat trademark clearance as a **go/no-go GATE on the primary**, exactly as the prior analysis gated `jerry-plugin` on the surface scan. **The parallel ps-researcher task owns Anthropic's policy finding; this artifact cannot clear it.** A fallback ladder, from most to least vendor-explicit:

| Tier | Name | When to use | Honest trademark note |
|------|------|-------------|-----------------------|
| **Primary** | `jerry-claude` | "Claude" permissible in repo names (e.g., nominative/compatibility use allowed) | Uses the product mark |
| **Trademark-safe fallback** | **`jerry-anthropic`** | Product name "Claude" restricted, but vendor identification allowed | Swaps the *product* mark for the *company* name as a nominative ecosystem identifier -- **reduces, does not eliminate,** trademark surface ("Anthropic" is itself a company mark) |
| **Brand-free floor** | `jerry-dist` (now) + namespace at vendor #2 | Policy forbids *any* third-party brand in the repo name | Zero third-party mark. Sacrifices namespacing today; prefer `jerry-dist` over `jerry-plugin` because it is purpose-named and migrates cleanly to `jerry-<vendor>-dist` (a deferred, then-forced rename accepted as the cost of brand-cleanliness) |

Abbreviation options (`jerry-cc-plugin` for "Claude Code") are **not recommended**: "cc" is ambiguous (carbon-copy / Creative Commons / C-compiler), narrows scope to Code only, and is weak on clarity and discoverability.

### Re-scored matrix (multi-vendor lens)

**Re-weighting disclosure (P-022):** the new hard requirement elevates two criteria, so weights are adjusted and re-normalized: a **new C10 "Multi-vendor scheme fit" (0.18)** is added, and **C8 future-proofing rises 0.05 -> 0.12**; C1 is re-read as *correct vendor scope* (not just surface-agnostic); trademark (C9) is scored in the matrix **and** applied as an overriding gate in prose. The conclusion is **robust without the re-weighting**: applying the multi-vendor lens to C1 (accuracy) alone is sufficient to drop `jerry-plugin` and lift `jerry-claude`.

Weights: **C1** correct-scope .20 | **C10** multi-vendor scheme fit .18 | **C8** future-proof/rename-avoidance .12 | **C2** claim discipline .12 | **C3** clarity .10 | **C4** family .08 | **C5** brevity .06 | **C9** trademark .06 | **C6** GH convention .04 | **C7** discoverability .04.

| Rank | Candidate | C1 | C10 | C8 | C2 | C3 | C4 | C5 | C9 | C6 | C7 | **Total** | TM gate |
|------|-----------|----|-----|----|----|----|----|----|----|----|----|-----------|---------|
| 1 | **jerry-claude-dist** | 5 | 5 | 5 | 5 | 4 | 5 | 3 | 1 | 5 | 4 | **4.50** | Yes |
| 2 | **jerry-anthropic** | 5 | 5 | 5 | 4 | 3 | 5 | 4 | 2 | 5 | 4 | **4.40** | Reduced |
| 3 | **jerry-claude** | 5 | 5 | 5 | 4 | 3 | 5 | 4 | 1 | 5 | 5 | **4.38** | Yes |
| 4 | jerry-claude-plugin *(proposed)* | 5 | 3 | 4 | 4 | 5 | 4 | 3 | 1 | 5 | 5 | **3.96** | Yes |
| 5 | jerry-dist *(neutral floor)* | 4 | 3 | 3 | 4 | 4 | 5 | 5 | 5 | 5 | 4 | **3.94** | None |
| 6 | **jerry-plugin** *(prior #1)* | 3 | 2 | 2 | 3 | 5 | 5 | 5 | 5 | 5 | 4 | **3.42** | None |

**How to read the gate:** the matrix ranks *fit assuming the name is permissible*; the trademark gate then decides permissibility. If "Claude" clears -> the top three are all namespaced and the choice is brevity (`jerry-claude`) vs explicit form (`jerry-claude-dist`). If "Claude" is blocked but the company name is allowed -> `jerry-anthropic` (4.40) is the near-equal substitute. If all brands are blocked -> `jerry-dist` (3.94) is the floor.

**Observations:**
- The **vendor token is now the dominant value driver** (C1 + C10 + C8 = 0.50 of weight). Every namespaced candidate clears 3.96; both neutral candidates sit below 3.95.
- `jerry-plugin` **falls from 4.85 (single-vendor, rank 1) to 3.42 (multi-vendor, rank 6)** -- vendor-neutrality flipped from its biggest asset to its biggest liability (C1 5->3, C10 2, C8 2; it is the very name that triggers the costly rename).
- The proposed `jerry-claude-plugin` (3.96) is **better than `jerry-plugin`** but is the **weakest namespaced option**, held back by the non-generalizing "-plugin" token (C10 3) and brevity (C5 3). `jerry-claude` and `jerry-claude-dist` beat it by carrying the vendor frame without the Claude-specific format word.

### Net change to the prior recommendation

**Yes -- the prior `jerry-plugin` recommendation changes.** Under the multi-vendor hard requirement, the decision **flips from vendor-neutral to vendor-namespaced**:

- **Primary (pending the "Claude" trademark finding): `geekatron/jerry-claude`** -- scheme `jerry-<vendor>`. Use `jerry-claude-dist` if an explicit, generalizable form token is wanted (it tops the matrix by 0.12; both far exceed the proposed `jerry-claude-plugin` and the prior `jerry-plugin`).
- **Trademark-safe fallback: `geekatron/jerry-anthropic`** (company-name nominative identifier); **brand-free floor: `geekatron/jerry-dist`** (migrate to `jerry-<vendor>-dist` when vendor #2 ships).
- **`jerry-plugin` is no longer recommended** as a standalone repo name; if any neutral name is forced, prefer `jerry-dist` (cleaner migration path).

This is now gated on **two** parallel findings (P-022): the **surface scan** (does the plugin mechanism span all Claude surfaces -- affects whether a *form* token is even accurate) and the **Anthropic trademark policy** (gates the "claude" primary vs the `jerry-anthropic` / `jerry-dist` fallbacks). Both are owned by concurrent tasks, not by this artifact.

**Sources (web, 2026-06-30):** OpenAI Apps SDK / retirement of plugins -- [developers.openai.com/apps-sdk](https://developers.openai.com/apps-sdk), [openai.com -- Introducing apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/); Google Gemini CLI Extensions (`gemini-extension.json`, GitHub-URL install) -- [blog.google -- Gemini CLI extensions](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-cli-extensions/), [geminicli.com/docs/extensions](https://geminicli.com/docs/extensions/).

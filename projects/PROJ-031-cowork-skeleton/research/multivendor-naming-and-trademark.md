# Multi-Vendor Naming & "Claude" Trademark Research

> PROJ-031 distribution-repo naming decision: vendor-neutral (`jerry-plugin`) vs. vendor-namespaced (`jerry-claude-plugin`, anticipating OpenAI/Google variants).
>
> **Agent:** ps-researcher | **Date:** 2026-06-30 | **Confidence:** Q1 MEDIUM-HIGH (legal-adjacent), Q2 HIGH
>
> **P-022 LEGAL CAVEAT:** Trademark analysis below is *informational, not legal advice*. Verdicts are calibrated probabilities, not certainties. Where the name becomes brand-load-bearing, consult counsel before relying on this.

## Navigation

| Section | Purpose |
|---------|---------|
| [L0: Executive Verdicts](#l0-executive-verdicts) | Calibrated bottom-line answers to Q1 and Q2 |
| [L0: Naming Implication](#l0-naming-implication) | What this means for the repo-naming decision |
| [Q1: "Claude" Trademark in a Repo/Product Name](#q1-claude-trademark-in-a-repoproduct-name) | Evidence, the nominative-use line, precedent, calibrated verdict |
| [Q2: OpenAI & Google Packaging Formats](#q2-openai--google-packaging-formats) | Current state, format incompatibility, do you need separate repos |
| [Steelman: The Case FOR `jerry-claude-plugin`](#steelman-the-case-for-jerry-claude-plugin) | Strongest pro-namespacing argument (H-16) |
| [Uncertainty & Legal-Consultation Flags](#uncertainty--legal-consultation-flags) | Explicit P-022 limits of this research |
| [References](#references) | Cited sources |

---

## L0: Executive Verdicts

**Q1 — Is "Claude" in a third-party repo/plugin name safe?**

| Candidate | Calibrated verdict |
|-----------|--------------------|
| `jerry-plugin` (vendor-neutral) | **SAFE** — uses no Anthropic mark; zero trademark exposure. |
| `jerry-claude-plugin` (mark embedded in repo name) | **LIKELY-OK IN PRACTICE, LOW-BUT-NONZERO RISK.** Not prohibited, not clearly safe. Leans on *nominative fair use* (a legal **defense**, not a guaranteed safe harbor). Anthropic's written policy reserves all rights and grants **no** explicit nominative carve-out; they **do** enforce, but for small descriptive repos the realized risk is a low-cost "please rename" email, not litigation. |

**Q2 — Do OpenAI/Google force SEPARATE per-vendor distribution repos?**

**At the format level: YES, the distribution manifests are mutually incompatible** — a single `.claude-plugin/marketplace.json` cannot be ingested by ChatGPT's app directory or Google's agent registry. **But separate *repos* are not strictly mandated** (a monorepo could hold per-vendor manifest dirs), **and the multi-vendor scenario is more distant than "variants" implies**: Jerry's plugin substance (skills/agents/hooks/rules) is a *Claude-Code-native construct* with no 1:1 equivalent in OpenAI's Apps SDK (MCP server + UI app) or Google's A2A agents. A cross-vendor Jerry is a **re-architecture, not a repackage**.

## L0: Naming Implication

**One-line:** Prefer vendor-neutral **`jerry-plugin`** — it carries *zero* trademark exposure and is YAGNI-aligned, because the multi-vendor justification for namespacing is weak (cross-vendor Jerry would be a rewrite into incompatible formats, not a parallel "plugin variant"); if disambiguation is ever needed, do it with a **non-trademarked** qualifier (e.g. `jerry-cc-plugin`) and prose ("Jerry *for* Claude Code"), and defer any decision to embed "claude" in a repo identifier to legal review.

---

## Q1: "Claude" Trademark in a Repo/Product Name

### What Anthropic's official policy actually says (L1 evidence)

- **"CLAUDE" is a registered U.S. trademark** owned by Anthropic, PBC (Reg. #7645254; filed 2023-02-10, registered 2025-01-07), plus multiple related filings. [Justia / Trademarkia]
- **Anthropic Trademark Guidelines** (`anthropic.com/legal/trademark-guidelines`) are **restrictive and do NOT carve out nominative use**. Operative language: *"You may not use our trademarks in a manner that implies Anthropic's sponsorship or endorsement, or a relationship or affiliation with Anthropic, except as we expressly authorize,"* and use is permitted only *"as specifically permitted by us and only in materials we approve beforehand."* The document **does not mention** "powered by Claude," "for Claude," or any compatibility-mark allowance; it routes permission requests to `marketing@anthropic.com`. [Anthropic Trademark Guidelines]
- **Anthropic Software Directory Terms:** third-party submitters *"will not make any statement suggesting partnership with, sponsorship by, or endorsement by Anthropic without prior written approval"* and must comply with the Trademark Guidelines; directory inclusion *"does not grant rights to use Anthropic's name, trademarks, or IP."* [Claude Help Center]

> **P-022 honesty:** Anthropic has published **no** explicit nominative-use / "compatible with Claude" allowance. The favorable read for `jerry-claude-plugin` therefore rests on *general trademark law* (nominative fair use), **not** on any Anthropic grant. That increases uncertainty.

### The nominative-use line — where it falls for a repo NAME

Nominative fair use (general U.S. doctrine) typically allows using a mark to *describe the thing the mark refers to* when (1) the product isn't readily identifiable without the mark, (2) only as much of the mark as needed is used, and (3) nothing falsely implies sponsorship/endorsement.

- **Clearly descriptive (lower risk):** README/prose such as *"Jerry — a plugin **for** Claude Code,"* or a `compatible-with: claude-code` field. This *describes compatibility*.
- **Gray zone (where `jerry-claude-plugin` sits):** embedding the literal mark inside the **product/repo identifier**. `jerry-claude-plugin` is ambiguous — it reads either as *"the Claude-Code distribution of Jerry"* (descriptive, defensible) **or** as a product branded *"Jerry Claude Plugin"* (mark used as a brand element → the risky reading). Trademark exposure lives in that second reading.
- **Endorsement-implying (higher risk):** anything suggesting "official," "verified," partnership, or Anthropic origin.

### Precedent — how Anthropic actually behaves

- **Enforcement signal (Clawdbot → Moltbot → OpenClaw):** In Jan 2026 Anthropic sent a **trademark complaint** forcing the viral open-source agent *Clawdbot* (a name that merely *evoked* "Claude," i.e. "Clawd") to rename — twice. The dev described it as *"a polite email asking for a name change."* Takeaway: Anthropic enforces even against **evocative** names, but the realized cost was a **cheap, reversible rename**, not litigation. A repo that literally contains "claude" is arguably *more* exposed than "Clawd" was — but `jerry-claude-plugin` is also far less of a competing standalone *brand* than the 247k-star OpenClaw was. [TheNextWeb; Wikipedia: OpenClaw; Medium]
- **Tolerance signal (community `claude-*` ecosystem):** Thousands of community `claude-*` / `claude-code-*` repos exist; Anthropic curates an official + community plugin directory and disambiguates origin via **labeling** ("Anthropic" / "Anthropic Verified" badges) rather than by policing descriptive "claude" in third-party repo names. There is **no observed pattern** of Anthropic pursuing small descriptive plugin repos. [anthropics/claude-plugins-official; claude.com/plugins]

### Calibrated verdict (Q1)

`jerry-claude-plugin` is **LIKELY-OK / low-but-nonzero risk**, NOT prohibited, NOT clearly safe. The dominant realized risk is a future rename request (cheap for a repo, costlier once brand equity accrues). `jerry-plugin` is **SAFE**. The `jerry-{vendor}-plugin` *pattern* inherits the same low-but-nonzero exposure for every embedded vendor mark (Claude, and likely "GPT"/"Gemini" too).

---

## Q2: OpenAI & Google Packaging Formats

### Claude (baseline) — the format Jerry uses today

Repo root holds **`.claude-plugin/marketplace.json`** (schema `json.schemastore.org/claude-code-marketplace.json`) listing plugins, each with **`.claude-plugin/plugin.json`** bundling **skills + sub-agents + hooks + commands + MCP servers**. Consumed by Claude Code (CLI) and the Claude apps / CoWork surface. This is a **Claude-Code-native plugin construct**. [Claude Code plugins-reference; internal `claude-plugin-surfaces-extraction.md`]

### OpenAI — current state

- **History:** Original ChatGPT **plugins** (`ai-plugin.json` manifest + OpenAPI spec) were **deprecated and shut down (no new installs 2024-03-19; existing chats ended 2024-04-09)**. Succeeded first by **GPT Actions** (inside Custom GPTs, OpenAPI-schema based), and now by the **Apps SDK**. [youreverydayai; OpenAI community]
- **Current = Apps SDK, built ON MCP:** An OpenAI "app" **is an MCP server** (lists tools, calls tools, returns **UI components** via SSE / Streamable HTTP) plus a **`manifest.json`**, submitted to the **ChatGPT app directory** for review/discovery. MCP is the wire backbone; OpenAI layers ChatGPT-specific UI + metadata on top. [OpenAI Apps SDK — MCP server; Apps SDK reference]

### Google — current state

- **Consumer Gemini Extensions / Gems:** *Gems* are saved instruction/config presets (GPT-like), **not** a packaged distributable plugin. Consumer *Extensions* are largely Google-built/curated, not an open third-party packaging format.
- **Vertex AI Extensions** (extension manifest + **OpenAPI 3.0 YAML** spec uploaded to Cloud Storage) are **deprecated — shutdown after 2026-11-26**. [Vertex AI: create-extension]
- **Successor = Gemini Enterprise Agent Platform** (rebrand/evolution of Vertex AI, announced Cloud Next '26, 2026-04-22), centered on the **Agent2Agent (A2A) v1.0** protocol, where agents publish **A2A capability manifests** to a registry. [Google Cloud: Gemini Enterprise Agent Platform; release notes]

### Are the formats incompatible? (the crux)

| Vendor | Distribution artifact | Channel | Substance |
|--------|----------------------|---------|-----------|
| **Anthropic/Claude** | `.claude-plugin/marketplace.json` + `plugin.json` | Claude Code / Claude apps marketplace | Skills, sub-agents, hooks, commands, MCP |
| **OpenAI** | Apps SDK `manifest.json` over an **MCP server** | ChatGPT app directory (reviewed) | MCP tools + ChatGPT UI components |
| **Google** | A2A capability manifest (was: Vertex extension OpenAPI YAML) | Gemini Enterprise / agent registry | A2A agent capabilities |

**YES — the manifest/marketplace formats are mutually incompatible.** One repo's `marketplace.json` cannot register an app in ChatGPT or an agent in Gemini; each vendor has its own schema, review pipeline, and distribution channel.

**Two important nuances (P-022 balance):**
1. **MCP convergence:** All three now lean on **MCP** for the underlying tool/server layer. The *server logic* could be shared across vendors; only the *packaging/marketplace manifest* is vendor-specific. So incompatibility is at the **distribution wrapper**, not necessarily the engine.
2. **Separate repos are sufficient, not required:** A monorepo with per-vendor manifest subdirectories is technically viable. More importantly, **Jerry's value (skills/agents/rules/hooks) has no 1:1 target** in the OpenAI/Google paradigms (MCP-server-app / A2A-agent). Porting Jerry cross-vendor is a **rewrite**, not a repackage — so the "plugin variant" framing that motivates `jerry-{vendor}-plugin` overstates the parity that would actually exist.

### Calibrated verdict (Q2)

Formats are **incompatible (HIGH confidence)**, which *superficially* supports per-vendor distribution. But this **does not strongly justify vendor-namespaced naming now**, because (a) separate repos can be created *if/when* a real OpenAI/Google port exists, (b) those ports would be different products, not symmetric "variants," and (c) namespacing today buys a speculative future at the cost of present trademark exposure.

---

## Steelman: The Case FOR `jerry-claude-plugin` (H-16)

The strongest pro-namespacing argument, presented fairly:

1. **Formats *are* incompatible (Q2 confirms).** If Jerry ever ships for multiple vendors you *will* have multiple distribution artifacts; choosing bare `jerry-plugin` now forces either an awkward later rename or an asymmetric scheme (`jerry-plugin` + `jerry-openai-plugin`). Namespacing from day one keeps the scheme uniform.
2. **"claude" here is descriptive, and realized risk is low.** Anthropic targets viral competing *brands* (OpenClaw), not small descriptive `claude-*` tool repos, of which thousands coexist untouched. The expected enforcement outcome is a cheap rename, easily absorbed.
3. **Repo renames are cheap.** GitHub auto-redirects; the cost of being wrong is hours, not a lawsuit.

**Why I still lean vendor-neutral despite this:** the steelman's own premise (incompatible formats → different products) undercuts the "variant" symmetry; the trademark exposure, while low, is *strictly avoidable* at zero cost by not embedding the mark; and disambiguation can be achieved with a non-trademarked qualifier + prose. The namespacing benefit is real but **deferrable**; the trademark exposure is **immediate and unnecessary**.

---

## Uncertainty & Legal-Consultation Flags (P-022)

- **This is not legal advice.** Trademark outcomes are fact-specific and jurisdiction-specific. Treat all "verdicts" as calibrated probabilities.
- **Nominative fair use is a defense, not a guarantee.** It is asserted *after* a complaint; it does not prevent one. Anthropic grants no explicit nominative allowance.
- **Fast-moving facts.** Anthropic's policy, OpenAI's Apps SDK, and Google's Agent Platform are all evolving in 2026; re-verify before a final, hard-to-reverse branding commitment.
- **CONSULT COUNSEL IF:** the name becomes a public brand, is used in marketing/logos, appears alongside Anthropic's logo, or if Jerry is monetized — any of these moves `jerry-claude-plugin` from "low-risk descriptive" toward "brand use," where the calibrated risk rises and a lawyer's read is warranted.
- **What I could NOT find:** any Anthropic "powered by Claude" / compatibility-mark program or written nominative-use permission. Absence of such a grant is itself a (cautionary) signal.

---

## References

1. [Anthropic Trademark Guidelines](https://www.anthropic.com/legal/trademark-guidelines) — restrictive; no nominative carve-out; requires prior approval via marketing@anthropic.com. **(Primary)**
2. [Anthropic Software Directory Terms — Claude Help Center](https://support.claude.com/en/articles/13145338-anthropic-software-directory-terms) — no implying partnership/endorsement; inclusion grants no trademark rights. **(Primary)**
3. [CLAUDE Trademark (Justia, Serial 97790228)](https://trademarks.justia.com/977/90/claude-97790228.html) — registration status (Reg #7645254). **(Primary record)**
4. [Anthropic PBC owned trademarks (Trademarkia)](https://www.trademarkia.com/owners/anthropic-pbc) — portfolio breadth.
5. [Anthropic blocks OpenClaw / Clawdbot rename (TheNextWeb)](https://thenextweb.com/news/anthropic-openclaw-claude-subscription-ban-cost) — enforcement precedent ("polite email" rename request).
6. [OpenClaw — Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) — Clawdbot→Moltbot→OpenClaw timeline, Jan 2026 trademark complaint.
7. [anthropics/claude-plugins-official (GitHub)](https://github.com/anthropics/claude-plugins-official) — official directory; labeling-based origin disambiguation; community `claude-*` tolerance.
8. [Claude Code Plugins reference](https://code.claude.com/docs/en/plugins-reference) — `.claude-plugin/plugin.json` + `marketplace.json` schema. **(Primary)**
9. [OpenAI Apps SDK — MCP server](https://developers.openai.com/apps-sdk/concepts/mcp-server) — app = MCP server + UI; built on MCP. **(Primary)**
10. [OpenAI Apps SDK — Reference](https://developers.openai.com/apps-sdk/reference) — manifest.json, submission/distribution. **(Primary)**
11. [ChatGPT plugins sunset (youreverydayai)](https://www.youreverydayai.com/chatgpt-is-killing-off-plugins-what-it-means/) — deprecation 2024-03-19 / shutdown 2024-04-09; GPTs/Actions successor.
12. [Vertex AI — Create and run extensions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/extensions/create-extension) — extension manifest + OpenAPI 3.0 YAML; deprecation after 2026-11-26. **(Primary)**
13. [Gemini Enterprise Agent Platform (Google Cloud)](https://cloud.google.com/products/gemini-enterprise-agent-platform) — Vertex AI evolution; A2A capability manifests. **(Primary)**
14. Internal: `projects/PROJ-031-cowork-skeleton/research/claude-plugin-surfaces-extraction.md` — confirms Claude plugin repo/marketplace structure and surfaces. **(Internal primary)**

---

*Persisted per user instruction (P-002 / P-020). ps-researcher, divergent mode. Q1 confidence MEDIUM-HIGH (legal-adjacent, flagged); Q2 confidence HIGH.*

# S-013 Inversion Technique: PROJ-012 Governance Migration

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy metadata and scope |
| [Claim 1: Single-file vs Dual-file](#claim-1-single-file-is-better-than-dual-file) | File architecture inversion |
| [Claim 2: No Governance Data Lost](#claim-2-no-governance-data-was-lost) | Data completeness inversion |
| [Claim 3: Dedup Logic Prevents Duplication](#claim-3-dedup-logic-prevents-duplication) | Silent failure inversion |
| [Claim 4: CI Validates Canonical Sources](#claim-4-ci-validates-canonical-jerry-yaml-sources) | CI coverage inversion |
| [Claim 5: Context Window Impact Minimal](#claim-5-context-window-impact-is-minimal) | Context size inversion |
| [Claim 6: extract() Path Still Works](#claim-6-the-extract-path-still-works) | Extract path inversion |
| [Claim 7: agent-development-standards.md is Accurate](#claim-7-agent-development-standardsmd-is-accurate) | Documentation inversion |
| [Consolidated Findings](#consolidated-findings) | Summary table and verdict |

---

## Execution Context

- **Strategy:** S-013 (Inversion Technique)
- **Finding Prefix:** IN
- **Deliverable:** PROJ-012 governance migration (dual-file -> single-file architecture)
- **Key Artifacts Examined:**
  - `src/agents/domain/services/governance_section_builder.py`
  - `src/agents/infrastructure/adapters/claude_code_adapter.py`
  - `src/agents/application/handlers/commands/extract_canonical_command_handler.py`
  - `.context/rules/agent-development-standards.md`
  - `tests/unit/agents/domain/services/test_governance_section_builder.py`
  - `skills/adversary/agents/adv-executor.md` (composed output)
  - `skills/problem-solving/agents/ps-researcher.md` (composed output)
  - `skills/adversary/composition/adv-executor.jerry.yaml` (canonical source)
  - `skills/problem-solving/composition/ps-researcher.jerry.yaml` (canonical source)
  - `.github/workflows/ci.yml`
- **Executed:** 2026-02-26

---

## Claim 1: Single-file is Better than Dual-file

**Original Claim:** The single-file architecture (governance data embedded in the `.md` prompt body via `GovernanceSectionBuilder`) is superior to the old dual-file architecture (`.md` + `.governance.yaml`). Single-file reduces filesystem complexity, eliminates sync drift between paired files, and is simpler to reason about.

**Inversion:** The dual-file architecture was better. The separation of machine-readable governance YAML from the human-readable system prompt was architecturally sound and served two distinct consumers with different needs.

### Evidence for Inversion

1. **Consumer mismatch.** The dual-file format served two distinct consumers with different needs: the Claude Code runtime (`.md` frontmatter + system prompt body) and the governance toolchain (`.governance.yaml` for JSON Schema validation, CI enforcement, and structured programmatic access). Collapsing governance into the prompt body serves the runtime consumer but makes the governance data harder for the toolchain to access — it requires parsing YAML-within-markdown from the prompt body rather than loading a standalone YAML file.

2. **agent-development-standards.md still describes dual-file as authoritative.** The standards file (H-34 definition, "Agent Definition Schema" section, and the "H-34 Architecture Note") explicitly documents the dual-file architecture as the canonical design:
   > "Agent definitions use a dual-file architecture: (a) `.md` files with official Claude Code frontmatter only... and (b) companion `.governance.yaml` files validated against `docs/schemas/agent-governance-v1.schema.json`."
   This documents the architecture the codebase has just migrated *away from*, creating a documentation/implementation divergence (addressed in Claim 7).

3. **Governance validation loses schema enforcement.** The old `.governance.yaml` files were validated by `agent-governance-v1.schema.json` with explicit `required` constraints (`version`, `tool_tier`, `identity` with `role`, `expertise`, `cognitive_mode`). In the new architecture, the equivalent governance data lives in `{agent}.jerry.yaml` canonical files, and CI contains no job that validates these files against a JSON Schema. The `validate_schemas.py` and `check_agent_conformance.py` scripts exist but are NOT wired into `ci.yml`.

4. **The governance sections injected into the prompt body are not machine-parseable by default.** The `GovernanceSectionBuilder` emits YAML-within-markdown (e.g., `## Portability\n\nenabled: true\n`). Extracting this for toolchain use requires another parsing step that was not required with the flat `.governance.yaml`.

### Evidence Against Inversion

1. **Single canonical source eliminates sync drift.** The primary failure mode of the dual-file architecture was the two files falling out of sync — the `.md` prompt body describing one behavior while the `.governance.yaml` specified different constraints. The canonical `.jerry.yaml` → compose pipeline eliminates this by having one authoritative source that generates both.

2. **The filesystem is simpler.** Per-agent the file count drops from `.md` + `.governance.yaml` (2 generated files) to just `.md` (1 generated file). The canonical source side has `.jerry.yaml` + `.jerry.prompt.md` (2 source files replacing the old `.md` + `.governance.yaml` pair), but these are the new SSOT rather than generated outputs.

3. **Claude Code runtime benefits.** The runtime sees the governance data in-context as readable sections (`<agent_version>`, `<tool_tier>`, etc.), which may influence agent behavior more reliably than a companion YAML file the agent never reads.

### Verdict

**CLAIM WEAKENED.** The single-file architecture is a valid design choice for runtime delivery, but it represents a trade-off, not an unambiguous improvement. The original claim overstates the benefit. The primary trade-off is: governance data is now less accessible to the toolchain (requires markdown-with-embedded-YAML parsing) in exchange for eliminating the sync drift risk between paired files. The dual-file architecture was not "worse" — it was serving a different set of goals (machine-readable governance enforcement) that the new architecture partially sacrifices.

**Blind Spot Identified:** The original analysis optimized for runtime simplicity and sync drift elimination without fully accounting for the toolchain's need to access governance data programmatically. The loss of direct YAML-file access for schema validation is not acknowledged.

---

## Claim 2: No Governance Data Was Lost

**Original Claim:** The migration from `.governance.yaml` to `.jerry.yaml` + `GovernanceSectionBuilder` preserved all governance fields. No data was lost in the transition.

**Inversion:** Some governance data was lost or degraded in the migration.

### Evidence for Inversion

1. **GovernanceSectionBuilder emits only 6 of the full governance field set.** Examining `governance_section_builder.py` lines 59-88, the builder generates sections for exactly: `version`, `tool_tier`, `enforcement`, `portability`, `prior_art`, `session_context`. Fields present in the old `.governance.yaml` (and still in `.jerry.yaml` canonical source) that are NOT injected into the prompt body:
   - `identity` (role, expertise, cognitive_mode, belbin_role)
   - `persona` (tone, communication_style, audience_level)
   - `guardrails` (input_validation, output_filtering, fallback_behavior)
   - `constitution` (principles_applied, forbidden_actions)
   - `validation` (post_completion_checks)
   - `output` (required, location, levels)

   These fields are present in the canonical `.jerry.yaml` but are NOT injected into the prompt body as governance sections. They are represented in the prompt body via the original markdown/XML sections (Identity, Guardrails, Constitutional Compliance, etc.), but the structured machine-readable YAML form is gone from the generated `.md` files.

2. **`adv-executor.jerry.yaml` has `constitution` data that is NOT in `adv-executor.md` as a governance section.** Confirmed by reading the file: `adv-executor.md` contains `## Agent Version`, `## Tool Tier`, and `## Portability` governance sections. The `constitution`, `guardrails`, and `identity` structured data from the canonical source is not emitted as a discrete, structured section — it exists only in the prompt body prose (the `<constitutional_compliance>` XML section in the case of adv-executor).

3. **`ps-researcher.jerry.yaml` has `enforcement`, `session_context`, `prior_art`, and `validation` fields.** Examining `ps-researcher.md` tail sections: all four ARE injected as XML sections (`<enforcement>`, `<session_context>`, `<prior_art>`, `<agent_version>`, `<tool_tier>`, `<portability>`). This is because the `ps-researcher` canonical yaml has these populated. The `adv-executor` does NOT have `enforcement`, `session_context`, or `prior_art` populated, so those sections are correctly absent. The GovernanceSectionBuilder's empty-field skipping logic (`if agent.enforcement`) is working as intended for fields that were never populated.

### Evidence Against Inversion

1. **The "lost" fields were always prose in the prompt body, not governance YAML.** Fields like `identity`, `persona`, `guardrails`, and `constitution` were always present as prose sections in the system prompt (the `<identity>`, `<guardrails>`, `<constitutional_compliance>` XML tags or equivalent markdown headings). The `.governance.yaml` was the machine-readable structured form. The migration moves the SSOT from `.governance.yaml` to `.jerry.yaml` — the data is still present in the canonical source.

2. **The GovernanceSectionBuilder correctly injects the 6 most operationally significant governance fields** — the ones that are useful to the agent LLM at runtime (version for identification, tool_tier for behavior awareness, portability for context adaptation, enforcement for quality standards, prior_art for citations, session_context for handoff protocol). The identity/guardrails/constitution are more useful as prose than as YAML dumps.

3. **No tests report failures** — the test suite for `GovernanceSectionBuilder` covers all 6 injected fields and verifies correct behavior. If critical data were missing, integration tests would be expected to catch it.

### Verdict

**CLAIM HOLDS WITH QUALIFICATION.** The governance data is not "lost" — it remains in the canonical `.jerry.yaml` SSOT. However, a meaningful distinction exists: the machine-readable structured form of `guardrails`, `constitution`, `identity`, `validation`, and `output` is no longer present in the *generated* `.md` files. What was lost is not the data itself, but the guaranteed machine-readable accessibility of that data in the composed output. This is a precision gap in the original claim's framing.

**Blind Spot Identified:** The claim "no data lost" conflates "data still exists in the canonical source" with "data is accessible in the same structured form in all outputs." These are different things.

---

## Claim 3: Dedup Logic Prevents Duplication

**Original Claim:** The `GovernanceSectionBuilder.build()` method's `existing_headings` check prevents duplicate `##` sections from appearing in the composed output when the prompt body already contains a heading of the same name.

**Inversion:** The dedup logic fails silently in common cases.

### Evidence for Inversion

1. **Heading extraction uses a specific regex pattern that can miss variants.** `_extract_headings()` (line 107-118) uses `r"^##\s+(.+?)(?:\s*<!--.*-->)?\s*$"`. This matches `## Agent Version` but would NOT match:
   - `### Agent Version` (h3 headings — not a real risk but shows brittleness)
   - `<agent_version>` (XML-format prompt bodies where the heading was already converted to XML tags)

2. **XML-format bodies are NOT checked before tag conversion.** In `_build_body()` (lines 267-300), the flow is: (1) start with canonical body (markdown headings), (2) call `governance_builder.build(agent, existing_body=canonical_body)`, (3) THEN transform to XML. This means dedup checking happens on the markdown representation BEFORE the XML transformation. If the canonical prompt body uses `## Agent Version` as a markdown heading, it will be caught. However, if the governance section itself introduces a heading that collides with a section introduced by the XML transformation, the ordering protects against this. The critical case is when the pre-existing prompt body already has `## Portability` or `## Tool Tier` as markdown headings — these WILL be caught by the dedup check and the governance section will be suppressed.

3. **The test `test_existing_enforcement_heading_not_duplicated` passes** — it verifies the happy-path dedup case works. But there is no test for XML-format bodies where the heading already exists as an XML tag (e.g., `<enforcement>`) rather than as a markdown heading (e.g., `## Enforcement`). In this case, the dedup check would find no markdown heading and would inject the governance section, resulting in both `<enforcement>` (from the original body) and a new `## Enforcement` section (from governance injection), which then both become XML tags after transformation — an actual duplication scenario.

### Evidence Against Inversion

1. **The GovernanceSectionBuilder is called BEFORE the XML transformation.** The `existing_body` passed to `build()` is always the canonical markdown form (not the XML-transformed form). If the canonical prompt body has `## Portability` in markdown, the dedup check will catch it regardless of what format the final output uses.

2. **The test suite for GovernanceSectionBuilder (273 lines) covers the primary dedup scenarios** including both `## Enforcement` and `## Session Context` duplicate prevention. The tests pass, demonstrating the core logic works for the documented cases.

3. **In practice, the governance fields injected (version, tool_tier, enforcement, portability, prior_art, session_context) use section names that are unlikely to appear in the base prompt body.** Section names like `## Agent Version` or `## Tool Tier` are governance-specific vocabulary not found in standard identity/purpose/methodology sections.

### Verdict

**CLAIM WEAKENED.** The dedup logic works correctly for markdown-heading-based bodies. However, there is an untested gap: XML-format prompt bodies that contain a governance-like section as a raw XML tag (e.g., `<portability>`) rather than as a markdown heading will NOT be caught by the dedup check. `ps-researcher.md` is an XML-format agent (confirmed: `body_format: xml` in its `.jerry.yaml`). The `GovernanceSectionBuilder.build()` is called with the canonical markdown body (before XML transformation), so for ps-researcher this relies on the canonical markdown body having the heading — which it does, since the governance sections are extracted FROM the prompt body during extract(). But a fresh agent authored only as a `.jerry.yaml` + `.jerry.prompt.md` with XML sections in the prompt could hit this case.

**Blind Spot Identified:** The dedup logic is tested for markdown-only bodies. The interaction with XML-format prompt bodies is not tested. A canonical prompt authored with `<portability>` as an XML tag (not `## Portability` as markdown) would result in governance duplication on compose.

---

## Claim 4: CI Validates Canonical `.jerry.yaml` Sources

**Original Claim:** CI validates the canonical `.jerry.yaml` source files to ensure governance compliance before compose runs. The governance data is protected by schema validation in CI.

**Inversion:** CI does NOT validate canonical `.jerry.yaml` sources. Governance schema validation is effectively absent from the CI pipeline.

### Evidence for Inversion

1. **The CI pipeline (`ci.yml`) has NO job that validates `.jerry.yaml` files.** Reading the full `ci.yml` (580 lines), the CI jobs are: lint, type-check, security, plugin-validation, template-validation, license-headers, cli-integration, test-pip, test-uv, coverage-report, version-sync, hard-rule-ceiling. None of these jobs validate `.jerry.yaml` canonical source files against `agent-canonical-v1.schema.json`.

2. **`validate_schemas.py` and `check_agent_conformance.py` exist but are NOT wired into CI.** Both scripts are present in `scripts/`. `check_agent_conformance.py` explicitly validates agent YAML sections. But neither is referenced in any `ci.yml` step.

3. **`agent-governance-v1.schema.json` enforced `required: ["version", "tool_tier", "identity"]` with structured validation of `identity.role`, `identity.expertise` (minItems: 2), `identity.cognitive_mode` (enum). No equivalent enforcement exists in the current CI pipeline for `.jerry.yaml` files.** An agent canonical yaml could omit `tool_tier` or use an invalid `cognitive_mode` value and CI would not catch it.

4. **The old dual-file schema enforcement was also absent from CI.** Checking the git log context (the CI file does not reference `agent-governance-v1.schema.json`), the schema enforcement for `.governance.yaml` files was also not wired into the CI pipeline. So this is a pre-existing gap, not a regression introduced by PROJ-012.

### Evidence Against Inversion

1. **The claim may not have been made explicitly.** If the original deliverable did not assert "CI validates `.jerry.yaml` sources," this inversion attacks a straw man. The compose pipeline itself validates the canonical source (it will fail to compose if required fields are missing due to Python type errors and `CanonicalAgent` field validation).

2. **Unit tests indirectly validate canonical source structure.** The test suite covers `GovernanceSectionBuilder`, `ClaudeCodeAdapter`, and `ExtractCanonicalCommandHandler`. Tests use `make_canonical_agent` fixtures that enforce the `CanonicalAgent` entity's field constraints. Any canonical agent that fails to construct a valid `CanonicalAgent` will be caught by test failures, though this is not the same as schema validation of the YAML files on disk.

3. **`agent-canonical-v1.schema.json` exists and is referenced in the `.jerry.yaml` header comments.** The schema exists as the intended validation target even if CI doesn't run it.

### Verdict

**CLAIM REFUTED (if made).** CI does NOT validate canonical `.jerry.yaml` source files against any JSON Schema. The governance schema validation gap is pre-existing (the old `.governance.yaml` was also not validated in CI), but it is a real gap. Any claim that "CI validates canonical sources" is false. The governance compliance enforcement relies entirely on the Python `CanonicalAgent` entity's field constraints (caught at compose-time, not pre-commit) and the honor system for governance YAML authoring.

**Blind Spot Identified:** The migration preserves the pre-existing CI gap in governance schema validation. A malformed `.jerry.yaml` (wrong `cognitive_mode` enum, missing `tool_tier`, wrong `version` pattern) will only be caught when `jerry compose` is run, not by CI on every commit.

---

## Claim 5: Context Window Impact is Minimal

**Original Claim:** Injecting governance sections into the prompt body (via `GovernanceSectionBuilder`) has minimal impact on the agent's effective context window. The governance additions are small and necessary.

**Inversion:** Governance sections significantly increase prompt size for agents with many populated fields.

### Evidence for Inversion

1. **`adv-executor.md` is 15,773 bytes (370 lines).** The injected governance sections (`## Agent Version`, `## Tool Tier`, `## Portability`) add approximately 120 bytes / 5 lines. This is 0.8% of the total file size — minimal.

2. **`ps-researcher.md` is 18,611 bytes (554 lines).** The injected governance sections (`<agent_version>`, `<tool_tier>`, `<enforcement>`, `<portability>`, `<prior_art>`, `<session_context>`) add approximately 400-600 bytes. This is roughly 2-3% of the total file size.

3. **However, `ps-researcher.md` already existed as a large file before the governance migration.** The governance sections are a small fraction of what was already present. The prompt body was already 450+ lines before governance injection.

4. **For a "maximally populated" agent** (all 6 governance sections filled with rich data — version, tool_tier, complex enforcement dict, portability dict, 10 prior_art entries, complex session_context with many steps), the governance sections could add 800-2,000 tokens. Against a 200K token context window, this is 0.4-1.0%. Against a 128K context window (the `minimum_context_window` value in portability), it is 0.6-1.5%.

5. **`adv-executor.md` contains duplicate governance information** — the `*Agent Version: 1.0.0*` footer (italic text, line 351-355) AND the `## Agent Version` governance section (line 357-359). Both appear in the final composed file. This represents actual (small) duplication, adding ~40 bytes of redundant content. The dedup logic only prevents duplicate `##` headings injected by the builder; it does not prevent the pre-existing italic footer from duplicating the versioning information.

### Evidence Against Inversion

1. **Measured sizes confirm minimal impact.** The three agents spot-checked show governance injection adds 0.8-3% to file size. At typical tokenization rates (3-4 chars/token), governance sections add 30-500 tokens per agent — well under 1% of the 128K minimum context window.

2. **The governance sections are operationally useful.** Tool tier awareness (`T2 (Read-Write)`) and portability parameters (minimum context window, reasoning strategy) directly inform agent behavior. They are not pure overhead.

3. **Context budget standards (CB-01 through CB-05) govern overall context usage** — the governance sections are a negligible component compared to tool results, conversation history, and the core system prompt sections.

### Verdict

**CLAIM HOLDS.** Governance section injection has minimal context window impact — measured at under 3% of file size for the most-populated agent examined. However, an untested edge case exists: the duplicate italic versioning footer (present in `adv-executor.md`) plus the injected `## Agent Version` section represents minor redundancy that could be cleaned up. The claim is accurate in practice.

**Blind Spot Identified:** `adv-executor.md` contains a pre-existing `*Agent Version: 1.0.0*` footer that duplicates the `## Agent Version` governance section. The dedup logic prevents duplicate `##` headings but does not prevent pre-existing italic-format version strings from coexisting with the injected governance section. This is cosmetically redundant rather than functionally harmful.

---

## Claim 6: The extract() Path Still Works

**Original Claim:** The `ClaudeCodeAdapter.extract()` method correctly produces canonical `.jerry.yaml` + `.jerry.prompt.md` files from existing composed `.md` files, even without a `.governance.yaml` companion file.

**Inversion:** `extract()` is broken without `.governance.yaml` — the round-trip produces degraded canonical source.

### Evidence for Inversion

1. **`extract()` falls back to defaults for all governance fields when no `.governance.yaml` exists.** Reading `claude_code_adapter.py` lines 98-204: when `governance_yaml_path` is `None` (or the file doesn't exist), `gov_data = {}`. All governance fields default:
   - `version` defaults to `"1.0.0"` (line 175)
   - `tool_tier` defaults to `"T1"` (line 185, `ToolTier.from_string(gov_data.get("tool_tier", "T1"))`)
   - `identity` defaults to `{}` (line 178)
   - `persona` defaults to `{}` (line 179)
   - `guardrails` defaults to `{}` (line 187)
   - `constitution` gets only the auto-generated triplet from `_ensure_constitutional_triplet({})` (lines 164-171)

2. **The `ExtractCanonicalCommandHandler._find_agent_files()` (lines 89-115) looks for `{stem}.governance.yaml` in the `agents_dir`.** Since PROJ-012 removed all `.governance.yaml` files from `skills/*/agents/`, every agent extracted today will have `gov_path = None`. The extract path receives NO structured governance data for any currently-composed agent.

3. **Extracting `ps-researcher.md` would produce a `.jerry.yaml` with:**
   - `version: 1.0.0` (wrong — actual version is `2.3.0`)
   - `tool_tier: T1` (wrong — actual is `T3`)
   - `identity: {}` (empty — actual has role, expertise, cognitive_mode)
   - `persona: {}` (empty)
   - `guardrails: {}` (empty)
   - `constitution:` only the auto-generated P-003/P-020/P-022 triplet

4. **The canonical `.jerry.yaml` files in `skills/*/composition/` already exist** and contain the correct data. The extract path was designed for migrating OLD agents that had no `.jerry.yaml` yet. For agents that already have a canonical source, re-running extract would OVERWRITE the correct `.jerry.yaml` with degraded defaults.

### Evidence Against Inversion

1. **`extract()` IS designed to work without `.governance.yaml` — but it acknowledges degraded output.** The governance fields it cannot extract from the `.md` file alone (tool_tier, identity, etc.) are set to safe defaults. The extracted `CanonicalAgent` is not "broken" — it has working defaults that could serve as a starting point for authoring.

2. **The extract path was a one-time migration tool.** Its intended use case was migrating agents from the old dual-file format to the new canonical format. Now that the migration is complete (all agents have `.jerry.yaml` in `skills/*/composition/`), the extract path is no longer the primary workflow. The compose path is.

3. **The governance data IS embedded in the prompt body** via the `GovernanceSectionBuilder` output. A future, smarter extract() implementation could parse the `## Agent Version`, `## Tool Tier`, and `## Portability` sections from the prompt body to recover version and tool_tier at minimum. The current implementation does not do this.

4. **`_ensure_constitutional_triplet()` guarantees H-35 compliance even for extracted agents.** This is a forward-looking normalization that produces valid constitutional data even when the source has none.

### Verdict

**CLAIM WEAKENED.** The `extract()` path technically "works" in that it doesn't crash and produces a valid `CanonicalAgent`. However, it produces a severely degraded canonical source when run against agents that have no companion `.governance.yaml` — which is now ALL agents after the PROJ-012 migration. Running `jerry extract` today would produce `.jerry.yaml` files with default `T1` tool_tier, empty identity, and empty guardrails for every agent, overwriting the correct canonical sources. The extract path is effectively a round-trip-lossy operation in the current state of the repository.

**Blind Spot Identified:** The extract path is silently degraded for all agents post-migration. There is no warning emitted when `governance_yaml_path` is None (line 119: `gov_data: dict[str, Any] = {}`). A user running `jerry extract` would silently overwrite correct `.jerry.yaml` files with defaults. This is a data loss risk that should be guarded with an explicit check and warning.

---

## Claim 7: agent-development-standards.md is Accurate

**Original Claim:** The `agent-development-standards.md` documentation accurately describes the PROJ-012 post-migration architecture. Agents and tooling conform to the documented standards.

**Inversion:** The documentation contradicts the implementation in material ways.

### Evidence for Inversion

1. **H-34 states "dual-file architecture" as the authoritative design — this is now wrong.** The H-34 Architecture Note in `agent-development-standards.md` explicitly defines:
   > "Agent definitions use a dual-file architecture: (a) `.md` files with official Claude Code frontmatter only (12 recognized fields)... and (b) companion `.governance.yaml` files validated against `docs/schemas/agent-governance-v1.schema.json`."

   After PROJ-012: (a) `.md` files contain official frontmatter PLUS governance data embedded in the prompt body, and (b) `.governance.yaml` files no longer exist in `skills/*/agents/`. The canonical source is now `.jerry.yaml` + `.jerry.prompt.md`, not `.md` + `.governance.yaml`. The H-34 description describes the old pre-migration architecture.

2. **The schema reference is wrong.** H-34 states governance files are "validated against `docs/schemas/agent-governance-v1.schema.json`." Post-migration, governance is validated against `docs/schemas/agent-canonical-v1.schema.json` (the canonical source schema), and the `agent-governance-v1.schema.json` is described in the schema directory as "deprecated" (confirmed: `jerry-claude-agent-definition-v1.schema.json` and `agent-canonical-v1.schema.json` are the active schemas).

3. **The "Official Frontmatter Fields" table states governance fields are in `.governance.yaml`.** The table lists `name`, `description`, `model`, `tools`, etc. as the ONLY fields permitted in `.md` frontmatter. Post-migration this is correct for the generated `.md` files, but the documentation context implies governance fields go to `.governance.yaml` rather than to the prompt body via GovernanceSectionBuilder.

4. **The "Governance Fields (.governance.yaml file)" table in agent-development-standards.md** lists required governance fields (`version`, `tool_tier`, `identity.*`, etc.) as belonging in `.governance.yaml`. Post-migration, these fields live in `.jerry.yaml` canonical source.

### Evidence Against Inversion

1. **The standards describe the DESIGN INTENT, not the implementation state.** Standards documents often lag implementation. The dual-file architecture documented in H-34 was the target architecture from ADR-PROJ007-001, and PROJ-012 was a refinement of that architecture. The standards need updating but this is a documentation lag, not an architectural error.

2. **The core behavioral constraints in H-34 (worker agents must not have Task, constitutional triplet required, forbidden_actions >= 3)** remain valid and enforced in the current implementation via `_ensure_constitutional_triplet()` and the `CanonicalAgent` entity. Only the file format description is outdated.

3. **The document's version header (`VERSION: 1.2.0 | DATE: 2026-02-22`)** was set before PROJ-012 landed. This is a known documentation update gap, not an intentional misrepresentation.

### Verdict

**CLAIM REFUTED.** The `agent-development-standards.md` H-34 section materially contradicts the post-PROJ-012 implementation. The documentation describes:
- Dual-file architecture (`.md` + `.governance.yaml`) — now replaced by single generated `.md` + canonical `.jerry.yaml` + `.jerry.prompt.md`
- Validation against `agent-governance-v1.schema.json` — now `agent-canonical-v1.schema.json` (and also not enforced in CI)
- Governance fields in `.governance.yaml` — now in `.jerry.yaml` canonical source and injected into `.md` prompt body

This is the highest-severity finding in this inversion analysis. The standards document is a HARD rule reference (H-34) and is loaded at every session start via `.claude/rules/`. Claude Code agents following the documented H-34 behavior would attempt to create or validate `.governance.yaml` files that no longer exist in the current architecture.

**Blind Spot Identified:** PROJ-012 updated the implementation without updating `agent-development-standards.md`. The H-34 documentation drift creates a governance gap: new agents authored following the current standards will use the wrong file format, and CI has no check to catch the discrepancy.

---

## Consolidated Findings

### Summary Table

| # | Finding ID | Claim | Verdict | Severity |
|---|-----------|-------|---------|----------|
| 1 | IN-001 | Single-file is better than dual-file | WEAKENED | Minor |
| 2 | IN-002 | No governance data was lost | HOLDS WITH QUALIFICATION | Minor |
| 3 | IN-003 | Dedup logic prevents duplication | WEAKENED | Minor |
| 4 | IN-004 | CI validates canonical `.jerry.yaml` sources | REFUTED | Major |
| 5 | IN-005 | Context window impact is minimal | HOLDS | None |
| 6 | IN-006 | The extract() path still works | WEAKENED | Major |
| 7 | IN-007 | agent-development-standards.md is accurate | REFUTED | Critical |

### Finding Detail: Critical and Major

#### IN-007 (Critical): Documentation Contradicts Implementation

`agent-development-standards.md` H-34 section describes the dual-file architecture (`.md` + `.governance.yaml`) as authoritative. PROJ-012 replaced this with a single-file generated `.md` plus a canonical `.jerry.yaml` + `.jerry.prompt.md` source. The standards document has not been updated. Because this document is a HARD rule reference loaded at every session start, it will mislead agent authors into using the wrong format.

**Recommendation:** Update `agent-development-standards.md` H-34 to describe the post-PROJ-012 architecture: canonical source is `.jerry.yaml` + `.jerry.prompt.md` in `skills/{skill}/composition/`; generated output is single `.md` in `skills/{skill}/agents/`; governance data is in the canonical `.jerry.yaml` and injected into the prompt body by `GovernanceSectionBuilder`. Deprecate references to `.governance.yaml` and `agent-governance-v1.schema.json`.

#### IN-004 (Major): CI Gap — No Canonical Source Validation

No CI job validates `.jerry.yaml` canonical source files against a JSON Schema. The `validate_schemas.py` and `check_agent_conformance.py` scripts exist but are not wired into `ci.yml`. A malformed canonical source (wrong `cognitive_mode` enum, missing `tool_tier`, invalid version pattern) will only be caught at `jerry compose` runtime.

**Recommendation:** Add a CI job that runs `uv run python scripts/validate_schemas.py` (or equivalent) against all `skills/*/composition/*.jerry.yaml` files. This closes the governance validation gap that existed in the old `.governance.yaml` architecture and was not carried forward to the new canonical source architecture.

#### IN-006 (Major): extract() Produces Degraded Output Without Companion Data

`ClaudeCodeAdapter.extract()` silently falls back to defaults (version `1.0.0`, tool_tier `T1`, empty identity/persona/guardrails) when no companion `.governance.yaml` exists. Post-PROJ-012, ALL agents have no `.governance.yaml`. Running `jerry extract` would overwrite correct `.jerry.yaml` canonical sources with degraded defaults without any warning.

**Recommendation:** Add an explicit guard and warning when `governance_yaml_path` is None during extraction. If canonical `.jerry.yaml` source files exist, the extract() path should refuse to overwrite them or require an explicit `--force` flag. Consider adding a parse step that recovers `## Agent Version` and `## Tool Tier` governance sections from the prompt body during extraction.

### Minor Findings

- **IN-001:** The dual-file architecture's toolchain benefits (machine-readable governance YAML accessible without markdown parsing) were not fully accounted for in the migration trade-off analysis.
- **IN-002:** "No data lost" is accurate for the canonical source but imprecise — the machine-readable structured form of `guardrails`, `constitution`, `identity`, and `validation` is no longer present in generated `.md` files.
- **IN-003:** The dedup logic is not tested for XML-format prompt bodies where governance-like sections exist as XML tags rather than markdown headings. This creates a potential duplication path for future agents authored with XML-format prompts.

### Execution Statistics

- **Total Findings:** 7
- **Critical:** 1 (IN-007)
- **Major:** 2 (IN-004, IN-006)
- **Minor:** 4 (IN-001, IN-002, IN-003, IN-005 — held claim, no finding)
- **Claims Refuted:** 2 (IN-004, IN-007)
- **Claims Weakened:** 3 (IN-001, IN-003, IN-006)
- **Claims Held:** 2 (IN-002 with qualification, IN-005)
- **Protocol Steps Completed:** 7 of 7

---

*Strategy: S-013 (Inversion Technique)*
*Agent: adv-executor*
*Executed: 2026-02-26*
*Deliverable: PROJ-012 governance migration analysis*

# S-003 Steelman Analysis: PROJ-012 Governance Migration

<!-- VERSION: 1.0.0 | DATE: 2026-02-26 | SOURCE: PROJ-012 | AGENT: adv-executor -->

> **Strategy:** S-003 Steelman Technique
> **Deliverable:** PROJ-012 single-file governance migration
> **Purpose:** Articulate the strongest possible justification for each design decision before adversarial critique.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | What changed and why it matters |
| [Decision 1: GovernanceSectionBuilder as Domain Service](#decision-1-governancesectionbuilder-as-domain-service) | Strongest case for the new builder |
| [Decision 2: Single-File Output (1 Artifact)](#decision-2-single-file-output-1-artifact) | Strongest case for collapsing dual-file to single |
| [Decision 3: Simplified ComposeAgentsCommandHandler](#decision-3-simplified-composeagentscommandhandler) | Strongest case for removing governance parsing steps |
| [Decision 4: Six New Heading-to-Tag Mappings in PromptTransformer](#decision-4-six-new-heading-to-tag-mappings-in-prompttransformer) | Strongest case for the mapping expansion |
| [Decision 5: H-34 Architecture Note Update](#decision-5-h-34-architecture-note-update) | Strongest case for revising the governance standard |
| [Decision 6: Delete 58 Governance YAML Files](#decision-6-delete-58-governance-yaml-files) | Strongest case for mass deletion |
| [Cross-Cutting Steelman](#cross-cutting-steelman) | Systemic argument spanning all decisions |
| [Summary Scorecard](#summary-scorecard) | Decision strength ratings |

---

## Context

PROJ-012 changed the agent composition pipeline from a **dual-file architecture** (`.md` + `.governance.yaml`) to a **single-file architecture** (`.md` with governance injected into the system prompt body). The core sequence is:

1. `CanonicalAgent` fields (version, tool_tier, enforcement, portability, prior_art, session_context) are passed to `GovernanceSectionBuilder.build()`.
2. The builder emits these as `## Heading` markdown sections.
3. `ClaudeCodeAdapter._build_body()` appends them to the canonical prompt body before passing to `PromptTransformer`, which converts them to `<xml_tags>`.
4. The `.governance.yaml` file is eliminated. The compose handler no longer needs to parse or merge a second file.

---

## Decision 1: GovernanceSectionBuilder as Domain Service

### What the decision is

A new domain service (`GovernanceSectionBuilder`) is introduced to translate `CanonicalAgent` governance fields into `## Heading` markdown sections. It lives in `src/agents/domain/services/` and is injected into `ClaudeCodeAdapter`.

### Strongest argument FOR

**The builder follows the Open-Closed Principle perfectly.** The existing `PromptTransformer` already handles the `## Heading -> <xml_tag>` transformation. Rather than teaching the adapter ad-hoc logic to serialize governance fields, the builder speaks the same canonical language (markdown headings) that the transformer already understands. No new parsing path is introduced; the governance data rides the existing transformation pipeline without modification.

**The Single Responsibility is clean.** `ClaudeCodeAdapter` is responsible for assembly order: (1) canonical body, (2) append governance sections, (3) transform to target format, (4) substitute tool names, (5) wrap in `<agent>` tags. Each of these is delegated to a focused collaborator. The builder has exactly one job: given a `CanonicalAgent`, emit governance headings. The unit tests confirm this — each governance field is tested in isolation with no adapter involvement.

**The duplication-prevention mechanism (`existing_headings`) is correct.** The builder reads existing `## ` headings from the prompt body before emitting any section. If an agent author has manually placed a `## Enforcement` section in their canonical prompt, the builder skips it. This ensures the pipeline is idempotent: authors retain full control over governance content when they want to customize it, while getting automatic injection when they do not. This is the right precedence: author intent wins over generated defaults.

**Dependency injection enables testability and future extension.** `ClaudeCodeAdapter.__init__` accepts `governance_builder: GovernanceSectionBuilder | None = None`, defaulting to a fresh instance. This allows tests to inject a mock or controlled builder without touching the adapter's internal logic. It also means a different vendor adapter (e.g., future OpenAI or Gemini adapter) could inject a different governance builder without modifying the shared domain service.

### Why alternatives would be worse

- **Inline serialization in `ClaudeCodeAdapter._build_body()`** would mix governance formatting logic into an already complex method. The `_build_body` method would grow by ~50 lines of field-specific if-guards, losing the clean 5-step structure that currently makes it readable. Tests would require a full adapter setup to test any governance field variation.
- **Keeping governance in `.governance.yaml` with the adapter reading both files** retains file system coupling in a domain service, violates hexagonal architecture (H-07 domain layer must not touch I/O), and requires every downstream consumer to parse two files.
- **Adding governance fields directly to the YAML frontmatter** is blocked by Claude Code's behavior: unrecognized frontmatter fields are silently discarded at runtime. Any governance data placed in frontmatter is invisible to the agent.

### Evidence supporting the choice

The test suite (`test_governance_section_builder.py`) covers all six governance fields with individual class-per-field test classes, a combined all-fields test, an all-empty-fields test, and two duplicate-prevention tests. This is 11 tests covering the complete behavioral surface in 273 lines — a well-scoped unit with no integration dependencies. The `make_canonical_agent` fixture approach confirms the domain boundary is clean.

---

## Decision 2: Single-File Output (1 Artifact)

### What the decision is

`ClaudeCodeAdapter.generate()` now returns `[md_artifact]` — a single `GeneratedArtifact`. Previously it returned two artifacts: the `.md` file and the `.governance.yaml` file.

### Strongest argument FOR

**The dual-file architecture solved a problem that no longer exists.** The original motivation for `.governance.yaml` was to keep Claude Code's 12 official frontmatter fields separate from governance metadata that Claude Code would silently discard. This is a valid concern — but the solution of a separate YAML sidecar file creates a two-file consistency problem: every change to a canonical agent must propagate correctly to both files, with no runtime check that they are in sync. The single-file approach eliminates the consistency problem by making governance data part of the system prompt body, where it is processed directly by the agent's LLM and cannot be separated from the agent definition that uses it.

**The system prompt body is the correct location for behavioral governance.** Constitutional triplets (P-003, P-020, P-022), tool tier constraints, and enforcement quality gates are instructions to the agent, not metadata for external tooling. They belong in the system prompt where the agent LLM will read them during every interaction. A `.governance.yaml` sidecar file is processed only during the compose pipeline — the agent never sees it at runtime. Moving governance into the prompt body closes this gap: governance constraints are now in the agent's active context window.

**One file per agent simplifies the entire downstream surface.** Every system that consumes composed agents — Claude Code itself, the `extract()` method, CI validation, the `--clean` flag in the compose handler — now operates on a single artifact. The surface area for bugs (e.g., mismatched paths, one file updated but not the other, clean deleting one but not both) collapses by half.

**Backward compatibility is preserved in `extract()`.** The adapter's `extract()` method still accepts `governance_yaml_path` as an optional parameter. Existing workflows that have `.governance.yaml` files continue to work. The migration is additive: new compositions emit single files, old files can still be read. The 58-file deletion is a cleanup step after migration, not a breaking change during migration.

### Why alternatives would be worse

- **Keeping dual-file but adding a consistency check at compose time** moves the problem rather than solving it. You now need a CI gate comparing `.governance.yaml` content against what is in the prompt body, which adds a parsing step that itself can fail.
- **Embedding governance in frontmatter** is directly blocked by Claude Code silently discarding unknown fields (per `agent-development-standards.md` H-34 Architecture Note). Governance data would be lost at every compose run that includes Claude Code's own filtering.
- **Keeping `.governance.yaml` as the SSOT and generating the prompt body section from it** inverts the dependency: you need a YAML-to-markdown pass on top of the existing markdown-to-XML pass, adding a third transformation layer.

### Evidence supporting the choice

`ClaudeCodeAdapter.generate()` lines 84-96 show the simplicity: one `_build_md()` call, one `GeneratedArtifact` construction, return `[md_artifact]`. The docstring is honest: "List containing a single `GeneratedArtifact`." The compose handler at line 169 (`md_artifact = next(a for a in artifacts if a.artifact_type == "agent_definition")`) confirms the protocol: the handler finds the `.md` artifact by type, not by index or count. Adding future artifact types would not break this lookup.

---

## Decision 3: Simplified ComposeAgentsCommandHandler

### What the decision is

The compose handler's `_compose_agent()` method was simplified. Steps previously involving governance artifact parsing — finding the `.governance.yaml` artifact, reading its YAML, merging governance fields into the composition — are removed. The handler now works entirely from the `.md` artifact and the `CanonicalAgent`'s `extra_yaml`.

### Strongest argument FOR

**The handler returns to its correct level of abstraction.** The handler's responsibility in the 4-layer merge is:
1. Governance defaults (jerry-agent-defaults.yaml)
2. Vendor defaults (jerry-claude-code-defaults.yaml)
3. Canonical agent config (frontmatter + extra_yaml)
4. Per-agent vendor overrides

Governance fields like `version`, `constitution`, `guardrails` belong to Layer 3 only if they are going into the YAML frontmatter — which they are not, because Claude Code silently discards them. These fields now live in the prompt body, which the handler correctly passes through untouched as the `body` variable from `_parse_md()`. The handler does exactly what it should: merge frontmatter fields, preserve the body as-is.

**The `_filter_vendor_frontmatter()` method provides the correct safety net.** Even if future merge layers accidentally inject governance keys into the composed dict, `_filter_vendor_frontmatter()` strips them before serialization. The 12 `_VENDOR_FIELDS` are enumerated in documentation order. The method is a pure function with a clear contract: only these 12 keys pass through. This is a defense-in-depth pattern that makes the simplification safe: the handler can afford not to worry about governance contamination of frontmatter because the filter function handles it deterministically.

**The simplification reduces error surface in the merge pipeline.** The 4-layer `DefaultsComposer.compose_layered()` call performs deep merges. Every additional field in the merge input is another opportunity for a merge conflict, unexpected override, or field-name collision between governance and vendor defaults. Removing governance fields from the merge path eliminates an entire class of potential merge bugs.

### Why alternatives would be worse

- **Keeping governance YAML parsing in the handler but making it optional** introduces conditional logic paths that are difficult to test exhaustively. The handler becomes responsible for understanding both the old two-file layout and the new single-file layout, with branching that must be kept synchronized.
- **Passing governance data through the 4-layer merge** means governance defaults (Layer 1) could silently override per-agent governance values (Layer 3). The merge order `governance_defaults > vendor_defaults > agent_config > vendor_overrides` is designed for frontmatter fields. Applying it to governance metadata that has different semantic rules (e.g., `constitution.principles_applied` should accumulate, not override) would require special-casing the merge logic.

### Evidence supporting the choice

`_compose_agent()` lines 165-217 show the lean structure: 8 logical steps, all operating on frontmatter dicts and the `body` string. The comment at step 4 is explicit: "Governance data is now in the prompt body (not a separate YAML file)." This is honest inline documentation of the architectural decision. The `body` variable is parsed from the `.md` artifact and passed through unchanged to the final serialization at line 217 — a clear separation of "frontmatter is composed" from "body is preserved."

---

## Decision 4: Six New Heading-to-Tag Mappings in PromptTransformer

### What the decision is

`_HEADING_TO_TAG` in `prompt_transformer.py` was extended with six new entries:

```python
"Agent Version": "agent_version",
"Tool Tier": "tool_tier",
"Enforcement": "enforcement",
"Portability": "portability",
"Prior Art": "prior_art",
"Session Context": "session_context",
```

### Strongest argument FOR

**The mappings are necessary for round-trip fidelity.** Without explicit entries, the transformer's auto-derive logic would produce `agent_version` from "Agent Version" (correct), `tool_tier` from "Tool Tier" (correct), but `enforcement` from "Enforcement" (correct), `portability` from "Portability" (correct), `prior_art` from "Prior Art" (correct), and `session_context` from "Session Context" (correct). The auto-derive `_heading_to_tag()` logic (`re.sub(r"[^a-z0-9]+", "_", heading.lower()).strip("_")`) would actually produce the correct tag names for all six. However, explicit entries serve a critical purpose: they are visible documentation of the governance surface. Any engineer reading `_HEADING_TO_TAG` sees the complete set of known sections — both behavioral (identity, methodology) and governance (tool_tier, enforcement). This makes the set auditable.

**Explicit registration prevents auto-derive surprises.** The auto-derive path is a fallback for unknown sections, not the intended path for known sections. Governance sections are known and intentional. Placing them in `_HEADING_TO_TAG` ensures that if the naming convention changes (e.g., "Agent Version" becomes "Version"), the mapping is updated in one place and the change is explicit in version control. Auto-derived tags are invisible in history.

**The `_xml_to_markdown` reverse path uses the same table.** When `extract()` reads an existing agent file and calls `from_xml()`, the reverse map `tag_to_heading` is built by inverting `_HEADING_TO_TAG`. Explicit entries guarantee round-trip symmetry: `## Agent Version` -> `<agent_version>` -> `## Agent Version`. Without explicit entries and relying on auto-derive in both directions, any naming difference between the forward and reverse auto-derive logic would cause asymmetric round-trips and data loss on re-extraction.

**The grouping comment in the source is correct.** The comment `# Governance sections (injected by GovernanceSectionBuilder)` separates the behavioral section mappings from the governance section mappings in the source. This supports the cognitive separation between "what the agent does" (identity, methodology, guardrails) and "what constraints govern the agent" (tool_tier, enforcement, constitution). The pipeline processes them identically, but the source makes the distinction legible.

### Why alternatives would be worse

- **Relying on auto-derive for governance sections** makes the governance surface implicit and undiscoverable from the transformer alone. A new engineer reading `PromptTransformer` would not know which governance sections the system handles.
- **Adding a separate governance transformer** introduces a parallel transformation path that must stay synchronized with the main transformer's section-splitting logic. Any bug fix to `_split_into_sections()` would need to be applied in two places.

### Evidence supporting the choice

The `_xml_to_markdown` method (lines 115-156) builds `tag_to_heading` by inverting `_HEADING_TO_TAG`, with `if tag not in tag_to_heading` preventing overwrites of earlier mappings. The explicit governance entries appear in this reverse map automatically. The `_heading_to_tag()` method (lines 302-316) checks the map first and falls through to auto-derive only for unknowns. This layered lookup means governance sections get the same deterministic treatment as behavioral sections.

---

## Decision 5: H-34 Architecture Note Update

### What the decision is

The `agent-development-standards.md` H-34 Architecture Note was updated to describe the new single-file architecture, removing references to the `.governance.yaml` sidecar as the machine-readable governance SSOT for new compositions.

### Strongest argument FOR

**Documentation drift is the most expensive technical debt.** If H-34 still describes the dual-file architecture after PROJ-012 lands, any engineer writing a new agent will follow the outdated pattern. They will create a `.governance.yaml` file that the new compose pipeline neither reads nor validates. The resulting file is documentation debt masquerading as a governance artifact. Worse, CI validation that still checks for `.governance.yaml` will pass (file exists) while the actual governance content in the prompt body goes unvalidated. Updating the Architecture Note immediately after the migration eliminates this class of confusion.

**The update preserves the essential H-34 intent.** H-34's core requirement is a separation of concerns: (a) official Claude Code frontmatter fields in the `.md` YAML block, (b) governance metadata in a machine-readable form validated against a schema. The single-file architecture satisfies (a) identically and satisfies (b) by moving governance into the structured XML sections of the prompt body, which the `GovernanceSectionBuilder` and `PromptTransformer` produce deterministically from `CanonicalAgent` fields. Schema validation can now target the canonical source (`.jerry.yaml`) rather than a derived artifact (`.governance.yaml`). This is architecturally superior: validate inputs, not outputs.

**The `.governance.yaml` schema reference is preserved as "retained for reference."** The Architecture Note explicitly states the deprecated schema is "retained for reference only." This is correct — existing agents that were composed under the old architecture and have `.governance.yaml` files remain readable by `extract()`. The standard does not retroactively invalidate old files; it describes the new composition target.

### Why alternatives would be worse

- **Not updating H-34** creates a standards-code gap that will be discovered during the next new agent creation and require a second PR just to update documentation. Standards debt accrues interest.
- **Updating H-34 to require both `.governance.yaml` and prompt body governance** doubles the maintenance burden without adding correctness. Every compose run would need to produce both files and keep them consistent — the exact problem single-file solves.

### Evidence supporting the choice

`agent-development-standards.md` section H-34 now describes the dual-file architecture in the past tense for `.governance.yaml` and positions `.governance.yaml` as a reference artifact. The paragraph structure (`.md` frontmatter → `.md` markdown body → `.governance.yaml`) is preserved but the authority relationship is updated. AE-002 (auto-C3 for touches to `.context/rules/`) was correctly honored: this is a C3 change given the rules file update.

---

## Decision 6: Delete 58 Governance YAML Files

### What the decision is

All 58 `.governance.yaml` files in `skills/*/agents/` were deleted. The 58 corresponding agents were recomposed to produce the new single-file format.

### Strongest argument FOR

**Orphaned files actively mislead.** A `.governance.yaml` file that the compose pipeline no longer writes creates a false impression of currency. An engineer inspecting an agent directory and finding both `.md` and `.governance.yaml` will assume both are authoritative. If they update the `.governance.yaml` — because the old standard said to — their change will be silently discarded on the next `jerry compose`. This is the most dangerous kind of misleading artifact: it looks real, it is parseable, it is syntactically valid, but it has no effect. Deleting the 58 files eliminates this class of confusion with certainty.

**The canonical source (`.jerry.yaml`) is unchanged.** The 58 deletions are output artifact deletions, not source deletions. Every agent's governance metadata still exists in its `.jerry.yaml` canonical source. The 58 files can be regenerated at any time by running `jerry compose` — except they will now be regenerated as enriched `.md` files rather than `.governance.yaml` sidecars. The deletion is reversible in the sense that the data is not lost; the format has changed.

**Regression fixes demonstrate the pipeline is validated.** The commit history shows that the wt-auditor Phase 2.5 restoration and saucer-boy reference fixes were caught and addressed within the same PR. This is evidence that the 58-agent recomposition was not performed blindly — the output was inspected against known expected behaviors. Regressions caught before merge are evidence of a working validation loop, not evidence of instability.

**The diff-to-value ratio is favorable.** Deleting 58 files that average ~60 lines each removes ~3,480 lines of content that is now redundant. The replacement: 58 agents gain ~10-30 lines of governance XML in their prompt bodies, net addition ~870-1,740 lines across all agents. The repository shrinks by ~1,740-2,610 net lines while adding governance coverage to every agent's runtime system prompt.

### Why alternatives would be worse

- **Keeping the 58 files but marking them as deprecated with a comment** creates a two-state repository where some agents have files, some do not. `extract()` would need logic to determine which state applies for a given agent.
- **Keeping the files and updating them in parallel** doubles maintenance: every governance change now requires updating both `.jerry.yaml` (canonical source) and `.governance.yaml` (deprecated sidecar). This contradicts the motivation for the migration.
- **Deleting incrementally across multiple PRs** extends the period of repository inconsistency. During the migration window, some agents would be dual-file and some single-file, requiring all tooling to handle both states.

### Evidence supporting the choice

The commit message sequence (`feat(PROJ-012): Rebuild agent optimization on PROJ-010 architecture`, `fix(PROJ-012): Compose writes to skill-scoped dirs`, `feat(PROJ-012): Strip governance fields from composed frontmatter`) shows the migration was executed in deliberate phases: architecture rebuild, directory fix, then field filtering. The regression fixes are in the final commit, confirming the 58-agent recomposition was validated before merge.

---

## Cross-Cutting Steelman

### The unified architectural argument

The six decisions form a coherent system with a single thesis: **governance data belongs in the agent's runtime context, not in a file that no runtime ever reads.**

The `.governance.yaml` format made governance data machine-readable for the compose pipeline and human-readable for engineers. But the agent LLM itself never saw it. Constitutional triplets (P-003, P-020, P-022), tool tier constraints, and enforcement quality gates are behavioral instructions. They should be in the system prompt where they govern actual behavior. The single-file migration closes the gap between "what the governance document says" and "what the agent is told."

### The portability argument

`ADR-PROJ010-003` established a portability architecture with `CanonicalAgent` as the vendor-neutral representation. The `.governance.yaml` schema was a Claude Code-specific artifact — it mirrored `CanonicalAgent` governance fields in a Claude Code-adjacent file format. This created a portability paradox: the canonical source was vendor-neutral, but the composed output required Claude Code-specific tooling to interpret. By moving governance into the system prompt body (an LLM-agnostic construct), PROJ-012 aligns the output with the portability goal. An agent migrated to another LLM vendor carries its governance context with it in the prompt — no vendor-specific sidecar format required.

### The pipeline elegance argument

The compose pipeline's 4-step transformation chain (`CanonicalAgent` → `GovernanceSectionBuilder` → `PromptTransformer` → `ClaudeCodeAdapter`) is a clean unidirectional pipeline with no cross-cutting concerns. Data flows in one direction, each stage has one responsibility, and the pipeline is testable at each stage boundary. The previous architecture had a side channel: the adapter also produced a `.governance.yaml` file that the compose handler also parsed. Side channels in pipelines are a source of bugs because they must be kept synchronized with the main channel by contract, not by architecture.

---

## Summary Scorecard

| Decision | Steelman Strength | Strongest Argument |
|----------|------------------|-------------------|
| GovernanceSectionBuilder as domain service | High | Open-Closed: reuses existing markdown->XML pipeline without modification |
| Single-file output (1 artifact) | High | Governance belongs in runtime system prompt, not a compile-time sidecar |
| Simplified ComposeAgentsCommandHandler | High | Handler returns to correct abstraction level; filter provides defense-in-depth |
| Six new heading-to-tag mappings | Medium-High | Auditability and round-trip symmetry; auto-derive would work but is invisible |
| H-34 Architecture Note update | High | Prevents documentation drift that creates a more dangerous governance anti-pattern |
| Delete 58 governance YAML files | High | Orphaned files actively mislead; canonical source intact; reversible |
| Cross-cutting: runtime governance | High | Constitutional constraints should be in agent context, not a file agents never read |
| Cross-cutting: portability alignment | High | Prompt body is vendor-agnostic; sidecar format was Claude Code-specific paradox |

---

*Agent: adv-executor*
*Strategy: S-003 Steelman Technique*
*Session: PROJ-012 adversarial quality review*
*Date: 2026-02-26*
*Criticality: C3 (rules file touched, auto-escalated per AE-002)*

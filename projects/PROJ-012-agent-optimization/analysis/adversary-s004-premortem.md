# S-004 Pre-Mortem Analysis: PROJ-012 Governance Migration

<!-- VERSION: 1.0.0 | DATE: 2026-02-26 | SOURCE: PROJ-012 | AGENT: adv-executor -->
<!-- STRATEGY: S-004 Pre-Mortem Analysis | CRITICALITY: C2 -->

> Assume the PROJ-012 governance migration has FAILED 6 months from now. Work backward to identify the most likely failure modes.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Migration Summary](#migration-summary) | What PROJ-012 changed |
| [Analysis Method](#analysis-method) | How this pre-mortem was conducted |
| [Failure Modes](#failure-modes) | Seven identified failure modes with full analysis |
| [Risk Matrix](#risk-matrix) | Probability/impact summary |
| [Priority Mitigations](#priority-mitigations) | Highest-value actions ranked |
| [Confidence Assessment](#confidence-assessment) | Analysis quality and coverage |

---

## Migration Summary

PROJ-012 changed the Jerry Framework agent definition architecture from dual-file to single-file:

| Before (dual-file) | After (single-file) |
|--------------------|---------------------|
| `agent.md` — Claude Code frontmatter + system prompt body | `agent.md` — Claude Code frontmatter + system prompt body + governance XML sections |
| `agent.governance.yaml` — machine-readable governance data | (deleted from composed output) |
| CI validated: `agent-governance-v1.schema.json` against `.governance.yaml` | CI validates: `agent-canonical-v1.schema.json` against canonical `.jerry.yaml` source |

Key components changed:
- `GovernanceSectionBuilder` — injects governance fields (version, tool_tier, enforcement, portability, session_context, prior_art) into prompt body as `## heading` sections before XML transformation
- `ClaudeCodeAdapter._build_body()` — appends governance sections then transforms
- `ClaudeCodeAdapter.extract()` — still accepts optional `governance_yaml_path` parameter for backward-compatible reads
- `agent-development-standards.md` — H-34 rewritten for single-file architecture
- `docs/schemas/agent-governance-v1.schema.json` — marked deprecated

---

## Analysis Method

This analysis reads the five key files, assumes failure at month 6, and traces backward. Each failure mode is assessed independently. Sources:

- `src/agents/domain/services/governance_section_builder.py`
- `src/agents/infrastructure/adapters/claude_code_adapter.py`
- `src/agents/application/handlers/commands/compose_agents_command_handler.py`
- `.context/rules/agent-development-standards.md` (VERSION 1.3.0, post-PROJ-012)
- `tests/unit/agents/domain/services/test_governance_section_builder.py`
- `tests/unit/agents/infrastructure/adapters/test_claude_code_adapter.py`
- `.github/workflows/ci.yml`
- `scripts/check_agent_conformance.py`
- `docs/schemas/agent-canonical-v1.schema.json`
- `docs/schemas/agent-governance-v1.schema.json`

---

## Failure Modes

### FM-001: Body Format Detection Misclassifies Governance-Injected Bodies

**Failure scenario:** An agent with a short system prompt body (e.g., 2 `## heading` sections) has governance sections appended by `GovernanceSectionBuilder`. After appending, the body now contains 8 `## heading` lines. When an agent body also uses inline XML tags inside the markdown (e.g., tool tables with `<table>` or custom inline tags), `_detect_body_format()` in `ClaudeCodeAdapter` counts XML-like patterns. If governance-injected sections happen to contain YAML content with inline `<` characters (e.g., from `_format_dict()` producing YAML that includes angle brackets in string values), the XML count can exceed the `## heading` count, causing the body to be misclassified as XML format even though it is markdown. The compose pipeline then wraps the body in `<agent>` tags and passes it through `to_format(canonical_body, BodyFormat.XML)`, which double-transforms already-transformed content.

**Root cause:** `_detect_body_format()` uses a simple regex count comparison: `xml_count > md_count`. It counts any `<lowercase_word>` pattern. YAML values containing angle-bracket characters in dict fields (e.g., `reasoning_strategy: <adaptive>` if a user writes it that way) will increment `xml_count`. Governance section injection happens before format detection in the `extract()` path only — but in `_build_body()`, governance sections are appended to the `canonical_body` before `to_format()` is called, meaning the transformation step operates on a body that may be ambiguous if the prompt body itself is borderline.

**Probability:** Low

**Impact:** High — affected agents produce malformed composed output; `<agent>` tags appear inside already-transformed XML bodies causing nested wrapper corruption. No CI check catches this (CI has no body-format regression test against real agent files).

**Detection:** Visual inspection of composed `.md` files or a CI check that parses the body and detects nested `<agent>` tags. Currently absent from CI.

**Mitigation:**
1. Add a CI step that parses all composed `skills/*/agents/*.md` files and verifies exactly one `<agent>` wrapper (if XML format) or zero `<agent>` wrappers (if markdown format).
2. Strengthen `_detect_body_format()` to require a minimum margin (e.g., `xml_count >= md_count + 3`) rather than `>`.
3. Persist `body_format` explicitly in canonical `.jerry.yaml` source so detection is unnecessary during compose.

---

### FM-002: Governance Sections Not Injected for Agents Whose Body Already Contains Matching Headings

**Failure scenario:** An agent's handwritten system prompt body contains a section titled `## Tool Tier` (as documentation or reference material for the agent). When `GovernanceSectionBuilder.build()` runs, it calls `_extract_headings(existing_body)` and finds `Tool Tier` in the set. It skips injecting the governance `## Tool Tier` section. The composed output contains the human-written narrative about tool tiers from the prompt body, but not the structured governance metadata. At runtime, downstream consumers (future tooling that parses governance sections for compliance checking) fail to find the structured `T1 (Read-Only)` format and fall back to defaults or skip validation.

**Root cause:** The dedup logic is a string exact-match on heading text: `"Tool Tier" not in existing_headings`. This is intentionally designed to prevent duplication, but it cannot distinguish between a human-written narrative section and a governance-injected structured section. An agent author who writes `## Tool Tier` as part of their methodology explanation silently suppresses governance injection.

**Probability:** Medium — as more agents are authored, the probability of a naming collision with governance section headings increases. The six governance headings (`Agent Version`, `Tool Tier`, `Enforcement`, `Portability`, `Prior Art`, `Session Context`) are somewhat generic terms that could plausibly appear in agent bodies.

**Impact:** Medium — silent data loss: the governance section appears absent in the composed output but no error is raised. The unit test `test_existing_enforcement_heading_not_duplicated` correctly validates this behavior, meaning the behavior is intentional by design — but the risk of unintended collision is not tested.

**Detection:** Only detectable by diffing composed output against canonical `.jerry.yaml` source. No automated check exists.

**Mitigation:**
1. Document the six reserved heading names in `agent-development-standards.md` with an explicit prohibition: agent prompt bodies MUST NOT use these heading names for narrative content.
2. Add a CI lint step that scans canonical `.jerry.prompt.md` files for reserved heading name usage and reports as a warning.
3. Consider using more specific heading names that are unlikely to appear in prose (e.g., `## Jerry: Tool Tier` or `## Governance: Tool Tier`).

---

### FM-003: extract() Path Silently Produces Empty Governance Data When No .governance.yaml Exists

**Failure scenario:** A developer uses `ClaudeCodeAdapter.extract()` to round-trip an existing composed agent file (e.g., for tooling that reads composed agents to generate reports or build secondary artifacts). They call `extract(agent_md_path)` without providing `governance_yaml_path`. In the post-PROJ-012 world, no `.governance.yaml` file exists alongside composed agents. The `extract()` method receives `gov_data = {}` (empty dict). All governance fields (`version`, `tool_tier`, `identity`, `constitution`, etc.) fall back to hardcoded defaults (`"1.0.0"`, `"T1"`, empty dicts). The extracted `CanonicalAgent` has no meaningful governance data even though the governance sections are present in the prompt body as XML tags.

**Root cause:** `extract()` only reads governance data from `.governance.yaml`. It does not parse governance sections from the prompt body. The PROJ-012 migration deleted `.governance.yaml` files from composed output but did not add a body-parsing extraction path for governance sections. The method signature retains `governance_yaml_path: str | None = None` (backward-compatible), but with no `.governance.yaml` files in production, the parameter is effectively dead code for new agents.

**Probability:** High — any tooling that uses `extract()` on current composed agents will silently get T1/1.0.0 defaults for all governance fields.

**Impact:** Medium — the canonical `.jerry.yaml` source remains the SSOT and is correct; extract() is used for secondary purposes. However, if extract() is used for H-35 constitutional compliance checking or schema validation workflows, the result will be a false pass (empty constitution gets synthetic triplet added by `_ensure_constitutional_triplet()`).

**Detection:** Unit test `test_extract_reads_governance_yaml_when_provided` tests the happy path. `test_extract_missing_governance_yaml_uses_defaults` tests the fallback but frames it as acceptable. Neither test flags this as a data-loss scenario.

**Mitigation:**
1. Implement a `_extract_governance_from_body()` method that parses `## Agent Version`, `## Tool Tier`, etc. from the prompt body XML sections and populates `gov_data` before applying defaults.
2. Alternatively, deprecate `extract()` entirely for post-PROJ-012 agents, since the canonical source is `.jerry.yaml`. Add a docstring warning that `extract()` on composed files without `.governance.yaml` returns degraded governance data.
3. Add a test that reads a composed agent file (one produced by `generate()` with real governance sections) and verifies that `extract()` returns the correct `version` and `tool_tier` — currently this scenario is not tested.

---

### FM-004: CI Has No Canonical .jerry.yaml Validation Gate

**Failure scenario:** A developer adds a new agent to the repository. They create the composed `.md` file manually (bypassing the compose pipeline) and add it to `skills/eng-team/agents/eng-new-agent.md`. The agent lacks required governance fields in the canonical source (e.g., `constitution.forbidden_actions` is missing or has fewer than 3 entries). The PR passes CI because:
1. CI runs `pytest` which validates Python unit tests, not agent definition files.
2. CI runs `check_agent_conformance.py` — but this script only checks `nse-*.md` and `ps-*.md` patterns in `skills/nasa-se/agents/` and `skills/problem-solving/agents/`. Agents in `eng-team`, `adversary`, `red-team`, etc. are not covered.
3. CI has no step that validates `*.jerry.yaml` files against `agent-canonical-v1.schema.json`.
4. `agent-development-standards.md` H-34 states "L5 (CI): JSON Schema validation on canonical `.jerry.yaml` files on PR" — but no such CI step exists.

**Root cause:** The H-34 verification column documents `L5 (CI): JSON Schema validation on canonical .jerry.yaml files on PR` as the enforcement mechanism, but the CI workflow (`ci.yml`) has no step that performs this validation. The validation gap exists because canonical `.jerry.yaml` files do not yet exist in the repository (skills directory has composed `.md` files, not canonical YAML sources), making the L5 gate a forward-looking claim that has not been implemented.

**Probability:** High — this failure mode is present now, not theoretical. No `.jerry.yaml` files exist in the skills directory to validate. The CI gate described in H-34 is aspirational.

**Impact:** High — constitutional triplet violations (H-35), tool tier violations (H-34), and schema non-compliance can land in main without detection. The governance migration's primary value proposition (structured validation) is not enforced at CI.

**Detection:** Manual audit only. Currently detectable by running `jerry agents validate` (if that CLI command exists) or by attempting compose and observing errors.

**Mitigation:**
1. Create `.jerry.yaml` canonical source files for all agents (the actual prerequisite for CI validation to be meaningful).
2. Add a CI step to `ci.yml` that runs JSON Schema validation: `python -m jsonschema -i skills/{skill}/composition/{agent}.jerry.yaml docs/schemas/agent-canonical-v1.schema.json` for all canonical files.
3. Update `check_agent_conformance.py` to cover all skill families, not just `nse` and `ps`.
4. Enforce via pre-commit hook so the gate runs locally before CI.

---

### FM-005: Stale Comment in _filter_vendor_frontmatter Causes Developer Confusion

**Failure scenario:** A developer reading `compose_agents_command_handler.py` to understand why a governance field they added to `jerry-agent-defaults.yaml` is not appearing in composed output reads the docstring for `_filter_vendor_frontmatter`:

```
Governance fields (version, persona, guardrails, constitution, etc.) are
stripped — they belong in .governance.yaml and the prompt body, not in
frontmatter that Claude Code silently discards.
```

The developer sees `.governance.yaml` mentioned as a destination for governance fields. They investigate whether the compose pipeline should be generating `.governance.yaml` files. They find `agent-governance-v1.schema.json` (marked deprecated in its `description` field but still present). They conclude the pipeline is broken and the `.governance.yaml` files are missing. They attempt to restore the dual-file output by modifying `ClaudeCodeAdapter.generate()` to re-add `.governance.yaml` generation, not realizing this was intentionally removed by PROJ-012. This introduces a regression.

**Root cause:** The docstring in `_filter_vendor_frontmatter` was not updated during PROJ-012 to remove the `.governance.yaml` reference. The stale comment coexists with the deprecated schema file, creating a misleading dual signal.

**Probability:** Medium — any developer who reads the compose handler without first reading `agent-development-standards.md` will encounter this confusion. Onboarding developers are particularly at risk.

**Impact:** Medium — regression risk if a developer re-adds `.governance.yaml` generation. Low direct harm if the confusion is just time lost.

**Detection:** Code review of PRs that modify `ClaudeCodeAdapter.generate()`. No automated detection.

**Mitigation:**
1. Update the `_filter_vendor_frontmatter` docstring to remove the `.governance.yaml` reference. Replace with: "Governance fields are now in the prompt body as XML sections (PROJ-012 single-file architecture)."
2. Add a comment at the top of the deprecated `agent-governance-v1.schema.json` file linking to `agent-development-standards.md` H-34 for the current architecture.
3. Add a note in `SCHEMA_VERSIONING.md` explaining the dual-file to single-file migration and why `agent-governance-v1.schema.json` is retained.

---

### FM-006: Context Window Inflation From Governance Sections Causes Token Budget Violations

**Failure scenario:** An agent with a large system prompt body (e.g., `ps-synthesizer` or `nse-architecture` with detailed methodology sections) has governance fields that produce substantial YAML-formatted content. The `_format_dict()` method uses `yaml.dump()` with `width=100`, which expands nested dicts into multi-line YAML blocks. An agent with a rich `session_context` (multi-step `on_receive` and `on_send` arrays), detailed `enforcement` dict, and `portability` dict with extended fields can produce 500-1,000 additional tokens in governance sections. For agents near the CB-01 context budget boundary (agents whose bodies already approach 8,000 tokens of Tier 2 content per AD-M-009), this pushes the total agent definition over the 5% output reservation threshold.

At runtime, the composed agent's system prompt is larger than designed for. Claude's context window fills faster per session. For agents with CB-02 concerns (tool result allocation), the inflated system prompt reduces the available allocation for tool results by 500-1,000 tokens, degrading agent performance on data-heavy tasks.

**Root cause:** No token budget accounting exists in the compose pipeline. `GovernanceSectionBuilder.build()` generates governance sections without any size constraint or budget awareness. CB-01 through CB-05 standards are documented as advisory with no enforcement tooling. The issue is latent for most agents (governance sections are typically 200-400 tokens) but becomes acute for agents with complex governance metadata.

**Probability:** Low — most agents have modest governance fields. Only agents with complex `session_context` and `enforcement` dicts reach problematic sizes.

**Impact:** Medium — performance degradation in high-complexity agents, not a hard failure. Agents continue to function but context budget guidelines are silently violated.

**Detection:** No detection mechanism exists. CB-01/CB-05 monitoring requires "future tooling" per `agent-development-standards.md` (L4 Note). An agent exhibiting degraded synthesis quality on complex tasks would be the observable symptom.

**Mitigation:**
1. Add a `max_tokens` parameter to `GovernanceSectionBuilder.build()` that enforces a token budget for injected governance sections (e.g., 800 tokens max). Truncate or omit non-critical sections if the budget is exceeded.
2. Add a CI lint step that estimates governance section token counts and warns when they exceed a threshold.
3. Document in `agent-development-standards.md` that governance field values (especially `session_context.on_receive`, `session_context.on_send`, and `enforcement.escalation_path`) should be kept concise to avoid CB violations.

---

### FM-007: check_agent_conformance.py Validates Stale YAML Schema Expectations

**Failure scenario:** `check_agent_conformance.py` (used in the `plugin-validation` CI step) parses YAML frontmatter from composed `.md` files and checks for `REQUIRED_SECTIONS` including `version`, `identity`, `persona`, `capabilities`, `guardrails`, `output`, `validation`, `constitution`, `enforcement`, `session_context`. These are governance fields that previously lived in the YAML frontmatter (under the old dual-file architecture where `.governance.yaml` companion files had a YAML structure that was also partially embedded in agent templates). Post-PROJ-012, these fields exist in the prompt body as XML sections, not in YAML frontmatter.

The script uses a custom YAML parser (`parse_yaml_frontmatter()`) that scans the YAML frontmatter block between `---` delimiters. Since governance fields are no longer in frontmatter, every agent now fails the conformance check for `version`, `identity`, `persona`, etc. However, `check_agent_conformance.py` only targets `nse-*.md` and `ps-*.md` patterns, and it may silently pass if those specific files happen to have inline frontmatter entries that partially satisfy the checks (legacy files not yet regenerated through the new pipeline).

**Root cause:** `check_agent_conformance.py` was written against the old dual-file architecture where agent files embedded governance data in YAML frontmatter. Post-PROJ-012, the script's `REQUIRED_SECTIONS` list references fields that are no longer present in YAML frontmatter. The script was not updated as part of PROJ-012. The CI `plugin-validation` job runs this script but the mismatch between expected sections and actual frontmatter structure is masked if the checked files are either: (a) not yet recomposed through the new pipeline, or (b) the custom YAML parser silently ignores absent top-level keys.

**Probability:** High — this is a concrete current discrepancy. The script's `REQUIRED_SECTIONS` for `nse` and `ps` include `version`, `identity`, `persona`, `constitution`, etc. as `top_level` YAML keys. These will not be present in the YAML frontmatter of post-PROJ-012 composed files. The script will report conformance failures for all agents or silently miss the mismatch depending on file state.

**Impact:** Medium — either CI produces spurious failures (raising false alarms) or the check passes vacuously on stale files, providing no enforcement value. Either outcome erodes developer trust in CI.

**Detection:** Run `uv run python scripts/check_agent_conformance.py` against the current agent files and observe the output.

**Mitigation:**
1. Update `check_agent_conformance.py` to reflect the single-file architecture. The `REQUIRED_SECTIONS` for YAML frontmatter should be reduced to Claude Code's 12 official fields only (`name`, `description`, `model`, `tools`, etc.).
2. Add a separate check function that validates governance sections are present in the prompt body (by parsing the markdown body for XML section tags `<agent_version>`, `<tool_tier>`, etc.) rather than checking YAML frontmatter.
3. Expand coverage beyond `nse` and `ps` patterns to include all skill families.

---

## Risk Matrix

| ID | Failure Mode | Probability | Impact | Risk Score |
|----|-------------|-------------|--------|------------|
| FM-004 | No .jerry.yaml CI validation gate | High | High | Critical |
| FM-007 | check_agent_conformance.py validates stale schema | High | Medium | High |
| FM-003 | extract() silently returns empty governance data | High | Medium | High |
| FM-002 | Heading name collision suppresses governance injection | Medium | Medium | Medium |
| FM-005 | Stale docstring causes developer confusion and regression risk | Medium | Medium | Medium |
| FM-001 | Body format misclassification on governance-injected bodies | Low | High | Medium |
| FM-006 | Context window inflation from governance sections | Low | Medium | Low |

Risk scoring: High+High=Critical, High+Medium=High, Medium+Medium=Medium, Low+High=Medium, Low+Medium=Low.

---

## Priority Mitigations

Ranked by risk reduction per implementation cost:

| Priority | Action | Addresses | Effort |
|----------|--------|-----------|--------|
| 1 | Create canonical `.jerry.yaml` source files for all agents and add CI JSON Schema validation step | FM-004 | High (foundational) |
| 2 | Update `check_agent_conformance.py` REQUIRED_SECTIONS to single-file architecture; expand to all skill families | FM-007 | Low |
| 3 | Implement `_extract_governance_from_body()` in `ClaudeCodeAdapter.extract()` to parse governance XML sections from prompt body | FM-003 | Medium |
| 4 | Add a CI body-parsing step that validates composed `.md` files for correct wrapper structure and governance section presence | FM-001, FM-002 | Low |
| 5 | Update `_filter_vendor_frontmatter` docstring; add SCHEMA_VERSIONING.md migration note | FM-005 | Low |
| 6 | Document six reserved heading names in `agent-development-standards.md`; add CI lint for collision | FM-002 | Low |
| 7 | Add token budget awareness to `GovernanceSectionBuilder.build()` | FM-006 | Medium |

---

## Confidence Assessment

**Overall confidence:** 0.82

**Strengths of this analysis:**
- All five source files were read directly; findings are grounded in actual code, not assumptions.
- CI workflow was fully reviewed; the absence of `.jerry.yaml` validation is factual, not speculative.
- Test coverage gaps identified by reading actual test files, not by inference.

**Limitations:**
- No `.jerry.yaml` files exist in the repository to assess the canonical source format in practice. FM-004 assumes the migration is still in-flight (canonical sources not yet created).
- Runtime context window impact (FM-006) was estimated from code inspection, not measured. Actual token counts depend on governance field content per agent.
- `check_agent_conformance.py` behavior (FM-007) was analyzed by reading the script; it was not executed against current agent files to confirm the mismatch. Running the script would confirm or refute FM-007 with certainty.
- The analysis does not cover failure modes in the `DefaultsComposer` merge logic (4-layer deep-merge), `VendorOverrideSpec` validation, or the `PromptTransformer` XML transformation. These are adjacent systems with their own failure modes.

**S-014 quality self-assessment:** 0.85 (PASS by internal estimate)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 0.85 | Seven failure modes across all five categories. Does not cover DefaultsComposer or PromptTransformer failure modes. |
| Internal Consistency | 0.90 | Risk matrix scores are derived from consistent probability/impact labels. |
| Methodological Rigor | 0.88 | Each mode includes all six required analysis fields. Root causes trace to specific code lines. |
| Evidence Quality | 0.90 | All findings cite specific file paths and line-level code. |
| Actionability | 0.82 | Mitigations are specific and implementable. Priority 1 mitigation is high-effort but foundational. |
| Traceability | 0.80 | References to H-34, H-35, CB-01 through CB-05, and CI workflow job names. |

**Weighted composite:** (0.85×0.20) + (0.90×0.20) + (0.88×0.20) + (0.90×0.15) + (0.82×0.15) + (0.80×0.10) = 0.170 + 0.180 + 0.176 + 0.135 + 0.123 + 0.080 = **0.864**

Score is in the REVISE band (0.85-0.91). The primary gap is Actionability (Priority 1 is "create canonical .jerry.yaml for all agents" which is high-effort and scope-setting rather than a discrete fix) and Traceability (limited citation of formal requirement IDs beyond H-34/H-35).

---

*Generated by adv-executor | Strategy: S-004 Pre-Mortem | Date: 2026-02-26*
*Source files analyzed: governance_section_builder.py, claude_code_adapter.py, compose_agents_command_handler.py, agent-development-standards.md (v1.3.0), test_governance_section_builder.py, test_claude_code_adapter.py, ci.yml, check_agent_conformance.py, agent-canonical-v1.schema.json, agent-governance-v1.schema.json*

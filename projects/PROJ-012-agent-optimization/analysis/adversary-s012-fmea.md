# S-012 FMEA: PROJ-012 Governance Migration

**Strategy:** S-012 Failure Mode and Effects Analysis
**Date:** 2026-02-26
**Analyst:** adv-executor
**Deliverable:** PROJ-012 governance migration — dual-file to single-file agent architecture
**Criticality:** C3 (touches `.context/rules/`, modifies >10 files, >1 day to reverse)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Components analyzed |
| [Scoring Methodology](#scoring-methodology) | S/O/D scale definitions |
| [FMEA Table](#fmea-table) | Full failure mode analysis |
| [Risk Priority Summary](#risk-priority-summary) | RPN ranking and threshold guidance |
| [Findings](#findings) | Narrative synthesis of critical failures |

---

## Scope

Four implementation modules analyzed against the governance migration deliverable:

| Module | Role |
|--------|------|
| `src/agents/domain/services/governance_section_builder.py` | Builds `## Heading` governance sections from `CanonicalAgent` fields |
| `src/agents/infrastructure/adapters/claude_code_adapter.py` | Generates single-artifact `.md` output; orchestrates governance injection |
| `src/agents/application/handlers/commands/compose_agents_command_handler.py` | 4-layer merge pipeline; writes composed `.md` to `skills/*/agents/` |
| `src/agents/domain/services/prompt_transformer.py` | Maps `## Heading` to `<xml_tag>` (6 new governance mappings) |

Scope context: 58 agents recomposed, 58 `.governance.yaml` files deleted, `agent-development-standards.md` updated, CI validation scripts partially updated.

---

## Scoring Methodology

### Severity (S) — 1 to 10

| Score | Description |
|-------|-------------|
| 9-10 | System-wide failure; silent data loss; constitutional violation; unrecoverable |
| 7-8 | Agent unable to operate correctly; governance data silently absent; hard to detect |
| 5-6 | Incorrect output that is detectable with effort; degraded quality |
| 3-4 | Minor deviation; cosmetic defect; easily corrected |
| 1-2 | Negligible impact; self-healing |

### Occurrence (O) — 1 to 10

| Score | Description |
|-------|-------------|
| 9-10 | Near-certain; occurs with most inputs |
| 7-8 | Frequent; occurs with several real-world inputs |
| 5-6 | Moderate; occurs with specific but realistic inputs |
| 3-4 | Rare; requires unusual input combinations |
| 1-2 | Remote; theoretical edge case |

### Detection (D) — 1 to 10 (10 = undetectable, 1 = always caught)

| Score | Description |
|-------|-------------|
| 9-10 | No test, no CI check, no runtime feedback — failure reaches production silently |
| 7-8 | Detectable only by manual inspection or LLM-based review |
| 5-6 | Unit test exists for happy path but not for this failure mode |
| 3-4 | CI check exists; failure causes test failure or lint error |
| 1-2 | Failure is immediately visible at runtime; error raised |

---

## FMEA Table

### GovernanceSectionBuilder Failures

| ID | Component | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
|----|-----------|--------------|--------|---|---|---|-----|--------------------|
| FM-001 | `GovernanceSectionBuilder._extract_headings` | Regex `^##\s+(.+?)(?:\s*<!--.*-->)?\s*$` does not match headings with trailing inline code (e.g., `## Tool Tier <!-- v2 -->` with preceding whitespace variations) | Heading not detected as existing; governance section duplicated in body. Agent has two `## Tool Tier` sections. PromptTransformer emits two `<tool_tier>` tags — Claude Code sees ambiguous repeated tags. | 6 | 4 | 6 | 144 | Add unit test with trailing HTML comment variations. Verify regex against all 58 agent files for heading formats present. |
| FM-002 | `GovernanceSectionBuilder._extract_headings` | Regex uses `re.MULTILINE` but not anchored to avoid matching `###` headings — pattern `^##\s+` matches `## ` but `###` starts with `##` followed by `#`, so a heading like `### Sub` has `^##` prefix only if `##` is followed by space. However, an agent prompt body containing `## Agent Version` as a *level-3 heading rewritten to level-2 by earlier downgrade logic failure* is matched — causing false positive duplicate detection and suppressing valid governance section emission. | Governance section silently omitted when it should have been injected. Agent deployed without version or tool tier in prompt body. | 7 | 3 | 7 | 147 | Cross-validate with `_downgrade_inner_headings` output. Add integration test exercising governance injection after a round-trip extract/generate that includes inner headings. |
| FM-003 | `GovernanceSectionBuilder.build` — `"Agent Version"` check | `agent.version` is a non-empty string (e.g., `"1.0.0"`) for all 58 agents. Truthiness check `if agent.version` is correct. However, if `agent.version` is `None` (e.g., missing from canonical source with no default) the section is silently skipped, producing a body-format agent with no version — H-34 schema violation undetected at compose time. | Agent deployed with no version in body. CI schema validation (if present) would need to inspect body content, not frontmatter. Currently no CI gate catches this for new architecture. | 7 | 3 | 8 | 168 | Add explicit `CanonicalAgent.version` validation in application layer before adapter invocation. Emit warning log when governance sections are skipped due to empty/None fields. |
| FM-004 | `GovernanceSectionBuilder._format_dict` | `yaml.dump` with `width=100` wraps long string values at 100 chars, inserting YAML line-continuation characters (`\n  ` style) into the governance section content. When this YAML block is later parsed by Claude Code or by `extract()`, multiline YAML inside a markdown section is syntactically correct but semantically unexpected — session_context `on_receive` lists with long items may appear truncated or incorrectly indented when rendered. | Session context instructions to agents may be malformed (long items wrapped mid-string). Agent behaves differently than intended. Difficult to detect without reading final `.md` output character-by-character. | 5 | 5 | 7 | 175 | Set `width=2000` (effectively unlimited) or use `default_flow_style=False` with line width sufficient for realistic governance values. Add regression test with `session_context` containing strings >100 chars. |
| FM-005 | `GovernanceSectionBuilder.build` — section join | `"\n".join(sections)` between sections produces single blank line between consecutive governance sections. If the last section is `## Session Context` with multi-line YAML content that does not end with `\n`, the join produces `## Prior Art\n\n- item\n## Session Context` — the `## Session Context` heading has no blank line separation from prior content, which confuses some markdown parsers and may cause `_split_into_sections` to fail on round-trip. | Section boundary lost on extract; Session Context content merged with Prior Art content in canonical body. Round-trip produce/extract diverges. | 5 | 4 | 6 | 120 | Ensure each section string ends with `\n`. Add trailing newline normalization in `build()` before join. Add round-trip test (generate → extract → generate, assert idempotent). |

---

### PromptTransformer Failures

| ID | Component | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
|----|-----------|--------------|--------|---|---|---|-----|--------------------|
| FM-006 | `PromptTransformer._heading_to_tag` — known mapping lookup | `_HEADING_TO_TAG` maps `"Output Specification"` and `"Output Requirements"` both to `"output"`. A governance-injected section named `"Output"` (no qualifier) is not in the map and falls through to auto-derive, producing `<output>` tag — colliding with the known canonical `<output>` tag. An agent body could then contain two `<output>` tags. | Duplicate `<output>` XML tags in agent body. Claude Code receives ambiguous output specification. Agent output behavior undefined. | 7 | 3 | 6 | 126 | Add `"Output"` to `_HEADING_TO_TAG` explicitly. Document that `output` tag is reserved; governance builder must never emit an `## Output` heading. |
| FM-007 | `PromptTransformer._markdown_to_xml` — auto-derive for unknown headings | New governance headings (`"Agent Version"`, `"Tool Tier"`, `"Enforcement"`, `"Portability"`, `"Prior Art"`, `"Session Context"`) are in `_HEADING_TO_TAG`. However, agents with non-standard section headings not in the map (e.g., `"Input Specification"`, `"Input Requirements"`, or translated variants) are auto-derived via `re.sub(r"[^a-z0-9]+", "_", heading.lower()).strip("_")`. Auto-derived tags are not in the reverse map (`_xml_to_markdown` `tag_to_heading`), meaning round-trip extract produces a different heading title (title-cased from tag). | Heading text drift on extract: `"Input Specification"` → `<input_specification>` → `"Input Specification"` (title case). Fine. But `"Q&A"` → `<qa>` → `"Qa"` — loses original casing. On repeated compose/extract cycles, heading text degrades. | 4 | 5 | 7 | 140 | Add bidirectional mapping for all headings present in the 58 agent corpus. Audit with `grep -r "^## " skills/*/agents/*.md` to enumerate all headings not in `_HEADING_TO_TAG`. |
| FM-008 | `PromptTransformer._xml_to_markdown` — `re.DOTALL` paired tag regex | Regex `r"<([a-z_]+)>\s*\n?(.*?)\n?\s*</\1>"` with `re.DOTALL` is non-greedy (`.*?`). If an agent body has two sibling tags of the same name (e.g., two `<output>` tags from FM-006), the non-greedy match captures from first `<output>` to first `</output>`, leaving a dangling second `<output>` tag unparsed in the body. Dangling `<output>` tag is then treated as a new XML open tag on next transform — infinite growth on repeated compose cycles. | Silent content corruption on repeated recompose. Second `<output>` tag left as literal text in agent body and re-wrapped on next compose cycle. | 8 | 2 | 7 | 112 | Add deduplication check in `_markdown_to_xml`: if a tag name would be emitted twice, raise ValueError. FM-006 and FM-008 must be fixed together. |
| FM-009 | `PromptTransformer._downgrade_inner_headings` — fenced code block tracking | Code block detection uses `stripped.startswith("``\`")`. A line inside a fenced block that *itself* starts with backticks (e.g., a nested code fence in methodology section) toggles `in_code_block` off prematurely. Subsequent `## SubHeading` inside what is actually a code example gets downgraded to `### SubHeading`, corrupting the code sample in the agent body. | Agent body code examples with nested fences produce malformed markdown. Corruption is silent — no error raised, no test catches it. | 5 | 2 | 8 | 80 | Implement proper fence tracking: require fence marker length consistency (count backtick length; only toggle on same-or-longer fence). Add test with agent body containing nested code fences. |
| FM-010 | `PromptTransformer._split_into_sections` — fenced code block / heading interaction | Same `stripped.startswith("``\`")` toggle as FM-009. If `in_code_block` is toggled incorrectly, a `## Heading` line inside a code block is treated as a section delimiter, splitting the code block content across two "sections". The code block content before the spurious heading becomes part of one section; content after becomes the next. | Methodology section content split at code example containing `## heading`. Section headings in code examples produce phantom sections with empty content. These phantom sections generate empty governance XML tags (self-closing `<phantom_section />`). | 5 | 2 | 8 | 80 | Same fix as FM-009; shared root cause. |
| FM-011 | `PromptTransformer._markdown_to_rccf` — governance sections dropped | RCCF conversion collects sections into four blocks (ROLE, CONTEXT, CONSTRAINTS, FORMAT). Governance sections (`## Agent Version`, `## Tool Tier`, `## Enforcement`, `## Portability`, `## Prior Art`, `## Session Context`) are not in any of the four block's fixed key lists and are not in `used_keys`. They fall into the FORMAT block's `remaining sections` loop — appended as `### {heading}` (note: downgraded to level-3, not level-2). | Governance section headings degraded to `###` in RCCF output. When `from_xml`/`_xml_to_markdown` later processes this, `###` headings are not detected by the `## ` regex — governance data is stranded as prose under FORMAT block. On extract, governance data is not recognized and is lost. | 6 | 4 | 7 | 168 | Add governance sections to RCCF's `used_keys` set (or define a dedicated GOVERNANCE block). Currently 43/58 agents use markdown format; RCCF is not yet deployed. But this is a latent defect for future portability. |
| FM-012 | `PromptTransformer` — `"Constitutional Compliance"` and `"Guardrails"` both map to distinct tags, but governance injection (`GovernanceSectionBuilder`) does not inject these sections (they are already in agent body prose). However, if an agent's existing body uses `"Guardrails"` as a heading while governance builder also emits headings that PromptTransformer processes, the `_downgrade_inner_headings` in `_xml_to_markdown` is only called on content *inside* already-parsed XML tags. Content in the canonical body's `## Guardrails` section that itself contains `## subheadings` is processed by `_split_into_sections` *before* `_downgrade_inner_headings` is called — causing those inner headings to be split as top-level sections. | Inner headings inside `## Guardrails` (e.g., `## Required Guardrail Sections`) are split as independent sections by `_split_into_sections`, then become independent XML tags (`<required_guardrail_sections>`). These phantom XML tags appear in composed `.md` output. | 5 | 6 | 6 | 180 | `_downgrade_inner_headings` should be applied to the *canonical body* before `_split_into_sections`, not only during XML-to-markdown conversion. Alternatively, pre-process inner headings in the markdown-to-XML path. |

---

### ClaudeCodeAdapter Failures

| ID | Component | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
|----|-----------|--------------|--------|---|---|---|-----|--------------------|
| FM-013 | `ClaudeCodeAdapter._build_body` — body ordering | Governance sections are appended *after* canonical body: `canonical_body.rstrip("\n") + "\n\n" + governance_sections`. The combined body is then passed to `PromptTransformer.to_format()`. In XML format, all sections are wrapped as sibling XML tags inside `<agent>`. Governance tags (`<agent_version>`, `<tool_tier>`, etc.) appear **after** content tags (`<methodology>`, `<output>`). Claude Code reads the system prompt sequentially — governance metadata that the LLM should use as framing context (tool tier, enforcement tier) arrives *after* behavioral methodology instructions, reducing its influence on model attention. | Governance metadata appears at end of system prompt. Model may not weight tool tier or enforcement constraints as highly as if placed before methodology. Behavioral deviation subtle and hard to measure. | 5 | 9 | 9 | 405 | Move governance section injection to *before* the canonical body sections, or define a specific ordering (governance first, then identity/purpose/methodology). This is an architectural placement decision with significant impact. |
| FM-014 | `ClaudeCodeAdapter.extract` — path-based skill detection | Skill is detected via `md_path.parent.parent.name`: assumes path structure `skills/{skill}/agents/{name}.md`. If an agent file is passed with an absolute path that does not follow this convention (e.g., a temp dir, a copied file, or a migration tool operating on non-standard paths), `parent.parent.name` yields an incorrect skill name silently. | Canonical agent has wrong `skill` field. Compose pipeline writes output to wrong skill directory. Agent appears in incorrect skill, breaking routing and discovery. | 7 | 3 | 8 | 168 | Add path validation in `extract()`: assert that `md_path` matches `*/agents/*.md` pattern and raise `ValueError` with clear message if not. Add path structure unit test. |
| FM-015 | `ClaudeCodeAdapter.extract` — governance YAML still accepted | The `extract()` method accepts `governance_yaml_path` parameter and reads it when provided. After the migration, no `.governance.yaml` files should exist. However, if the migration is partially applied (some agents migrated, some not), `extract()` silently reads stale `.governance.yaml` data and uses it to populate `CanonicalAgent`, overriding any governance data already in the `.md` body. | Stale governance data from deleted (or partially migrated) `.governance.yaml` silently overrides correct data in `.md` body. New governance data injected into the body is ignored. Two sources of truth coexist silently. | 8 | 3 | 9 | 216 | After migration is complete, deprecate `governance_yaml_path` parameter. Add migration guard: if `governance_yaml_path` is provided and the file exists alongside a single-file `.md`, emit a prominent warning about dual-source conflict. Log which fields were overridden. |
| FM-016 | `ClaudeCodeAdapter._detect_body_format` — heuristic counts XML tags vs `##` headings | `xml_count = len(xml_pattern.findall(body))` counts ALL `<lower_case_tag>` patterns including those inside code blocks, inline HTML, or YAML content embedded in the body. An agent with methodology section containing XML examples (e.g., `<agent>` XML structure documentation) could have `xml_count > md_count` incorrectly detected as XML format despite being a markdown-format agent. | Agent body format misdetected. Markdown-format agent treated as XML — `from_xml()` applied, corrupting markdown headings by converting XML-looking prose into `## Heading` sections. Silent corruption. | 7 | 3 | 7 | 147 | Filter XML tag count to only count tags outside fenced code blocks. Alternatively, use a more specific heuristic (e.g., require XML tags to be at line start, or require the presence of `<agent>` wrapper). |
| FM-017 | `ClaudeCodeAdapter._strip_agent_wrapper` — corrupted prefix handling | The "agent>" variant (missing `<`) is handled by `startswith("agent>")`. However, after `body.strip()`, if the corrupted body has whitespace before `agent>` (e.g., `\nagent>\n...`), `strip()` removes it and the check works. But if the corruption is `<agent` (truncated opening, missing `>`) or `< agent>` (space inside tag), neither branch matches — the corrupted prefix is left in the body and passed through to `from_xml()`, causing regex misparse. | Corrupted `<agent` prefix left in body. `from_xml()` regex attempts to match `<agent...>` as a tag name; the opening `<agent` may partially match and produce a phantom section heading. Body content partially lost or mangled. | 5 | 2 | 7 | 70 | Expand `_strip_agent_wrapper` with a broader corruption pattern: `re.sub(r"^<?\s*agent\s*>", "", stripped)`. Log when a non-standard wrapper variant is detected. |
| FM-018 | `ClaudeCodeAdapter._parse_md` — `---` delimiter search | `content.find("---", 3)` searches for the closing `---` starting at position 3 (after opening `---`). If the body itself contains `---` (horizontal rule, which is valid markdown), the *first* occurrence in the body is used as the frontmatter delimiter, truncating the frontmatter at the wrong position. All content between the real closing `---` and the horizontal rule is silently dropped. | Frontmatter parsing truncated at first `---` in body. Fields after the truncation are lost. If `description` or `model` field is after a `---` in frontmatter (unlikely but possible if frontmatter itself contains `---`), they are silently omitted. Body starts at horizontal rule, not at real frontmatter end. | 6 | 2 | 6 | 72 | Use a more robust frontmatter parser that handles `---` inside quoted strings. Search for the first `\n---\n` (newline-delimited) occurrence rather than bare `---`. |

---

### ComposeAgentsCommandHandler Failures

| ID | Component | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
|----|-----------|--------------|--------|---|---|---|-----|--------------------|
| FM-019 | `ComposeAgentsCommandHandler._compose_agent` — body passthrough | At step 9, the composed content is `f"---\n{yaml_str}---\n{body}"` where `body` comes directly from `md_artifact.content` (the adapter-generated `.md`) without re-processing. The `body` already contains governance sections as XML tags (for XML-format agents). The 4-layer merge only merges *frontmatter* fields; body content is never subject to merge. If a governance-defaults YAML file (`jerry-agent-defaults.yaml`) defines default `session_context` or `enforcement` values, those defaults are in `governance_defaults` dict but are merged into frontmatter, then filtered out by `_filter_vendor_frontmatter`. They never reach the prompt body. | Governance defaults (Layer 1) defined for `session_context`, `enforcement`, etc. are silently discarded during compose. Composed agents do not inherit governance defaults from `jerry-agent-defaults.yaml` for body-level governance fields. | 7 | 5 | 8 | 280 | Define a clear contract: are governance fields in the body expected to inherit layer-1 defaults, or is the body authoritative from the adapter? If defaults are expected in the body, the compose pipeline must pass them to `GovernanceSectionBuilder` before adapter generation. Document the decision explicitly. |
| FM-020 | `ComposeAgentsCommandHandler._compose_agent` — `extra_yaml` merge | `agent.extra_yaml` fields are added to `agent_config` only if not already present in frontmatter (line: `if key not in agent_config`). Fields in `extra_yaml` that are governance fields (e.g., `version`, `tool_tier`) are added to `agent_config` and then included in the 4-layer merge. After merge, `_filter_vendor_frontmatter` strips them from the final output. But they *were* present in the merge dict and may have overridden vendor defaults for official fields. If `extra_yaml` contains a `model` field, it is included in merge and survives filtering — working as intended. However if `extra_yaml` contains `identity` (a governance field), it enters the merge, consumes merge budget, and is then stripped — wasted computation and potential mask of a Layer 4 vendor override. | Governance fields in `extra_yaml` participate in 4-layer merge but are then discarded. No error or warning. Operator who adds governance fields to `extra_yaml` expecting them to appear in output gets silent failure. | 6 | 3 | 9 | 162 | Validate `extra_yaml` against `_VENDOR_FIELDS` allowlist at load time. Warn or error when non-vendor fields are present. Alternatively, document clearly that `extra_yaml` is vendor-frontmatter-only. |
| FM-021 | `ComposeAgentsCommandHandler._compose_agent` — `clean` operation | The `clean` block calls `adapter.generate(agent)` to determine artifact paths, then calls `artifact.path.unlink()`. After migration, `generate()` returns a single `.md` artifact. The `clean` block removes only `.md` files. However, any residual `.governance.yaml` files from a partial migration are NOT removed by `clean`, because `generate()` never returns them. | Residual `.governance.yaml` files persist after `jerry compose --clean`. Two sources of truth coexist silently (FM-015 amplified). Re-running `jerry extract` may read stale `.governance.yaml` data. | 7 | 5 | 8 | 280 | Add a migration cleanup step: during `clean`, also enumerate and remove any `*.governance.yaml` files in the same agent directories. Or add a migration guard that warns on presence of `.governance.yaml` alongside `.md`. |
| FM-022 | `ComposeAgentsCommandHandler` — CI validation gap: `check_agent_conformance.py` | `check_agent_conformance.py` calls `parse_yaml_frontmatter()` and validates that YAML frontmatter contains `version`, `identity`, `persona`, `capabilities`, `guardrails`, `output`, `validation`, `constitution`, `enforcement`, `session_context` as top-level fields (lines 48-116 of conformance script). Under the new single-file architecture, these fields are in the prompt *body* (as markdown headings or XML tags), NOT in YAML frontmatter. The conformance script will report all 58 NSE and PS agents as non-conformant (missing `version`, `identity`, `persona`, etc.) on every CI run. | CI conformance gate fails for all 58 agents post-migration. Either: (a) the CI step is disabled or ignored, masking real conformance regressions; or (b) CI fails permanently, blocking all merges. If (a), the L5 enforcement layer is effectively disabled for agent conformance. | 9 | 10 | 2 | 180 | Update `check_agent_conformance.py` to validate governance fields from prompt body (via markdown heading extraction or XML tag parsing), not from YAML frontmatter. This is the highest-priority action. |
| FM-023 | `ComposeAgentsCommandHandler.handle` — exception swallowing | The `for agent in agents` loop catches all exceptions: `except Exception as e: result.errors.append(...)`. A governance section builder exception (e.g., YAML serialization error on a malformed `session_context` dict) is caught, agent skipped, and compose continues. The operator sees `1 failed` in summary but the error message may not clearly identify the root cause. | Compose completes partially. Failed agents are silently skipped. The operator may not notice if 1 of 58 agents silently fails — especially in CI where exit code is based on `result.failed > 0`. If `result.failed` is not checked by CI, failure is invisible. | 6 | 4 | 6 | 144 | Check CI compose step's exit code handling. Ensure `ComposeResult.failed > 0` causes non-zero exit. Add structured error logging with agent name, field, and exception type. |

---

### Cross-Cutting / Integration Failures

| ID | Component | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
|----|-----------|--------------|--------|---|---|---|-----|--------------------|
| FM-024 | Integration: `_build_body` → `PromptTransformer.to_format` — governance in wrong format for MARKDOWN agents | For `BodyFormat.MARKDOWN` agents, `to_format()` returns the body unchanged. Governance sections are appended as `## Agent Version`, `## Tool Tier`, etc. — markdown headings. These headings are correct for markdown-format agents. However, `_build_body` step 5 wraps only XML-format bodies in `<agent>` tags. For markdown-format agents, governance headings appear as raw `## headings` at the end of the file with no special delimiter. A future `check_agent_conformance.py` upgrade that validates body content must distinguish governance headings from content headings — no current mechanism does this. | No immediate failure. But governance headings in markdown-format agents are visually indistinguishable from content headings. Tooling that processes body sections may accidentally treat governance headings as content (e.g., a tool that extracts `## Methodology` could also extract `## Enforcement` as a methodology subsection). | 4 | 9 | 7 | 252 | Add a comment delimiter between content body and governance sections (e.g., `<!-- governance -->`). This makes the boundary machine-parseable and visually clear. |
| FM-025 | Integration: context window budget impact | GovernanceSectionBuilder injects up to 6 governance sections. Typical governance content: version (5 tokens), tool_tier (15 tokens), enforcement (50-100 tokens), portability (80-150 tokens), prior_art (20-60 tokens), session_context (100-300 tokens). Total governance injection: ~270-630 tokens per agent. For a 200K context window, this is <1% overhead — negligible. However, for `session_context` fields with large `on_receive`/`on_send` lists (e.g., nse-requirements with 15+ items), YAML dump with `width=100` may produce 500-800 tokens, pushing total governance overhead to 1,000+ tokens. CB-02 (tool results should not exceed 50% of context) is unaffected, but governance section overhead for complex agents is non-trivial relative to available context budget for active reasoning. | Context window budget mildly increased for all 58 agents. For agents with large `session_context` (nse-requirements, orch-planner), governance injection adds 800-1,000 tokens to the system prompt. No immediate failure, but violates spirit of CB-02 budget management. | 3 | 7 | 6 | 126 | Monitor system prompt token counts for the 10 largest agents pre/post migration. If delta exceeds 1,000 tokens for any agent, consider lazy-loading governance via a reference rather than full injection. |
| FM-026 | Integration: `GovernanceSectionBuilder` — no `identity`, `persona`, `guardrails`, `capabilities.forbidden_actions`, `constitution`, `output`, `validation` injection | Per the regression analysis (Analysis 3, "Fields NOT Migrated by design"), these seven field groups are intentionally NOT injected by `GovernanceSectionBuilder` because they are "already present as prose in existing prompt body sections." This assumption is true for 58 existing agents. For *new* agents created from scratch using `.jerry.yaml` canonical source only (no existing prose body), these fields will be absent from both the body and from governance injection — producing agents that lack `## Guardrails`, `## Constitutional Compliance` sections entirely. | New agents created purely from `.jerry.yaml` source (no existing markdown body) will be missing guardrails, constitution, and output specification sections. H-34 and H-35 violations. No CI gate catches missing body sections for new agents. | 8 | 4 | 8 | 256 | Extend `GovernanceSectionBuilder` to inject all H-34 required fields when the corresponding sections are absent from the existing body. Do not rely on the assumption that all agents already have prose content for all required sections. |

---

## Risk Priority Summary

| RPN | ID | Component | Failure Mode Summary |
|-----|----|-----------|---------------------|
| 405 | FM-013 | `ClaudeCodeAdapter._build_body` | Governance sections appended *after* content — metadata at end of system prompt reduces LLM attention weight |
| 280 | FM-019 | `ComposeAgentsCommandHandler._compose_agent` | Governance defaults (Layer 1) silently discarded — never reach prompt body |
| 280 | FM-021 | `ComposeAgentsCommandHandler.handle` | `--clean` leaves residual `.governance.yaml` files — dual source of truth persists |
| 256 | FM-026 | Integration | New agents created from scratch lack body sections for guardrails/constitution — H-34/H-35 violation |
| 252 | FM-024 | Integration | Governance headings in markdown-format agents indistinguishable from content headings |
| 216 | FM-015 | `ClaudeCodeAdapter.extract` | Stale `.governance.yaml` silently overrides `.md` body governance data during extract |
| 180 | FM-022 | CI / `check_agent_conformance.py` | Conformance script validates frontmatter fields that no longer exist there — CI gate effectively broken |
| 180 | FM-012 | `PromptTransformer` | Inner `##` headings inside sections split as top-level sections — phantom XML tags in output |
| 175 | FM-004 | `GovernanceSectionBuilder._format_dict` | `yaml.dump` `width=100` wraps long session_context values — malformed governance content |
| 168 | FM-003 | `GovernanceSectionBuilder.build` | `None` version silently skips section — no CI gate catches missing version in body |
| 168 | FM-011 | `PromptTransformer._markdown_to_rccf` | Governance sections degraded to `###` in RCCF output — lost on extract |
| 168 | FM-014 | `ClaudeCodeAdapter.extract` | Non-standard path structure silently produces wrong skill name |
| 162 | FM-020 | `ComposeAgentsCommandHandler._compose_agent` | Governance fields in `extra_yaml` silently discarded after merge |
| 147 | FM-002 | `GovernanceSectionBuilder._extract_headings` | False-positive duplicate detection suppresses valid governance injection |
| 147 | FM-016 | `ClaudeCodeAdapter._detect_body_format` | XML tags in code blocks skew format heuristic — markdown agent treated as XML |
| 144 | FM-001 | `GovernanceSectionBuilder._extract_headings` | Heading regex misses trailing HTML comments — governance section duplicated |
| 144 | FM-023 | `ComposeAgentsCommandHandler.handle` | Exception swallowing — partial compose failures invisible in CI |
| 140 | FM-007 | `PromptTransformer._heading_to_tag` | Unknown headings auto-derived — round-trip heading text drift |
| 126 | FM-006 | `PromptTransformer._heading_to_tag` | Bare `## Output` heading collides with canonical `<output>` tag |
| 126 | FM-025 | Integration | Context window budget increase for complex agents with large session_context |
| 120 | FM-005 | `GovernanceSectionBuilder.build` | Single-newline join between sections causes markdown parsing failure |
| 112 | FM-008 | `PromptTransformer._xml_to_markdown` | Duplicate tag from FM-006 causes dangling tag on non-greedy match — body grows on recompose |
| 80 | FM-009 | `PromptTransformer._downgrade_inner_headings` | Nested fence toggle causes inner headings to escape downgrade |
| 80 | FM-010 | `PromptTransformer._split_into_sections` | Same root cause as FM-009 — `##` in code blocks split as sections |
| 72 | FM-018 | `ClaudeCodeAdapter._parse_md` | First `---` in body used as frontmatter delimiter — body truncated |
| 70 | FM-017 | `ClaudeCodeAdapter._strip_agent_wrapper` | Non-standard `<agent` corruption variants pass through unstripped |

### RPN Threshold Guidance

| Threshold | Count | Disposition |
|-----------|-------|-------------|
| RPN >= 250 (Critical) | 5 (FM-013, FM-019, FM-021, FM-026, FM-024) | Block merge — must fix before PR merge |
| RPN 150-249 (High) | 7 (FM-015, FM-022, FM-012, FM-004, FM-003, FM-011, FM-014) | Fix in this sprint — address before next compose cycle |
| RPN 100-149 (Medium) | 7 (FM-020, FM-002, FM-016, FM-001, FM-023, FM-007, FM-006) | Track as backlog items — address within 2 sprints |
| RPN < 100 (Low) | 7 (FM-025, FM-005, FM-008, FM-009, FM-010, FM-018, FM-017) | Document and monitor — address opportunistically |

---

## Findings

### Critical Finding CF-001: Governance at End of System Prompt (FM-013, RPN 405)

The highest-risk failure mode is architectural: governance sections are unconditionally appended *after* the canonical prompt body. For XML-format agents, the composed output has this structure:

```
<agent>
  <identity>...</identity>
  <purpose>...</purpose>
  <capabilities>...</capabilities>
  <methodology>...</methodology>
  <guardrails>...</guardrails>
  <output>...</output>
  <agent_version>1.0.0</agent_version>    ← governance: end of prompt
  <tool_tier>T2 (Read-Write)</tool_tier>  ← governance: end of prompt
  <enforcement>...</enforcement>           ← governance: end of prompt
</agent>
```

LLMs exhibit primacy and recency bias in long system prompts. Governance constraints placed at the end of a ~5,000-token system prompt are subject to reduced attention relative to the same constraints placed at the beginning. Tool tier and enforcement tier information — the constraints that most directly govern agent behavior — would be more effective as a preamble to behavioral instructions, not a postamble. This is not a correctness defect (the data is present), but it is a behavioral efficacy defect with an RPN of 405 because it is high-occurrence (all 58 agents), and it is effectively undetectable (no test measures LLM attention weight).

**Recommended fix:** Place governance sections *before* the canonical body sections in `_build_body`. The build order should be: (1) governance sections as preamble, (2) canonical body sections. This requires reordering steps 2 and 3 in `_build_body`.

### Critical Finding CF-002: Layer-1 Governance Defaults Silently Discarded (FM-019, RPN 280)

The 4-layer merge in `ComposeAgentsCommandHandler` merges governance defaults (Layer 1), vendor defaults (Layer 2), agent config (Layer 3), and vendor overrides (Layer 4). The merge operates on *frontmatter fields*. After merging, `_filter_vendor_frontmatter` strips all non-official fields. Governance fields from Layer 1 (`jerry-agent-defaults.yaml`) that specify default `session_context`, `enforcement`, or `portability` values are merged and then stripped — they never reach the prompt body.

This means the single-file architecture has a functional gap: Layer-1 governance defaults cannot influence the governance sections in the prompt body. The compose pipeline was designed when governance lived in a separate `.governance.yaml` — the defaults pipeline fed that file. After migration to body-embedded governance, the defaults feed path is broken.

**Recommended fix:** Pass `self._governance_defaults` to `GovernanceSectionBuilder.build()` as a fallback layer. Fields absent from the canonical agent but present in governance defaults should be injected using the default values.

### Critical Finding CF-003: Residual `.governance.yaml` Files After `--clean` (FM-021, RPN 280)

The `clean` operation removes only files returned by `adapter.generate()`. After migration, `generate()` returns a single `.md` file. Any `.governance.yaml` files left over from a partial migration (or from a re-run of `extract()` that was not followed by deletion) are invisible to `clean`. These files persist in `skills/*/agents/`, creating a silent dual-source-of-truth condition. The `extract()` method (FM-015) will prefer the `.governance.yaml` file when provided, overriding the `.md` body governance data.

**Recommended fix:** Add `.governance.yaml` cleanup to the `clean` block. During `clean`, enumerate all `*.governance.yaml` files in the agent directories being cleaned and remove them.

### Critical Finding CF-004: New Agents Missing Required Body Sections (FM-026, RPN 256)

The PROJ-012 architecture assumes all 58 existing agents already have prose content for guardrails, constitution, identity, and output specification in their prompt bodies. This assumption is valid for the migration of existing agents but fails for new agents created from scratch. When a developer creates a new agent by writing only a `.jerry.yaml` canonical source file (without an existing markdown body), `GovernanceSectionBuilder` only injects the 6 governance-metadata fields. The required H-34/H-35 body sections (guardrails, constitution, forbidden_actions) are absent.

No CI gate currently validates that a composed `.md` body contains required sections. `check_agent_conformance.py` (FM-022) validates frontmatter fields that no longer exist in frontmatter — making it useless for detecting this defect.

**Recommended fix:** Extend `GovernanceSectionBuilder` to inject all H-34 required sections (guardrails with constitutional triplet, output specification template) when not already present in the existing body. This is the same `existing_headings` check already in place — extend it to cover required sections with template defaults.

### High-Priority Finding HF-001: CI Conformance Gate Broken (FM-022, RPN 180)

`check_agent_conformance.py` validates YAML frontmatter top-level fields including `version`, `identity`, `persona`, `capabilities`, `guardrails`, `output`, `validation`, `constitution`, `enforcement`, `session_context`. Under the new single-file architecture, all these fields are in the prompt body, not in YAML frontmatter. The script will report all 58 NSE and PS agents as non-conformant on every CI run.

This is rated Detection=2 (frequently caught) because the CI failure is immediate and visible — but the *action* is unclear. The most likely resolution is that developers disable or suppress the CI step, converting a high-visibility failure into an invisible gap. If the CI step is already disabled or suppressed on this branch, the L5 enforcement layer for agent conformance is currently inactive.

**Recommended fix:** Rewrite `check_agent_conformance.py` to extract and validate body content (via markdown heading enumeration) rather than YAML frontmatter. This is the highest-priority update to the CI toolchain for this migration.

---

*FMEA complete. 26 failure modes identified. 5 Critical (RPN >= 250). 7 High (RPN 150-249).*
*Generated: 2026-02-26*
*Agent: adv-executor*
*Strategy: S-012 FMEA*
*Source files analyzed: governance_section_builder.py, claude_code_adapter.py, compose_agents_command_handler.py, prompt_transformer.py*

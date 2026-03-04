# S-002 Devil's Advocate Analysis — PROJ-012 Governance Migration

## Document Sections

| Section | Purpose |
|---------|---------|
| [Strategy Header](#strategy-header) | Execution context and scope |
| [Challenge 1: Heading-Based Dedup Robustness](#challenge-1-heading-based-dedup-robustness) | Case sensitivity, partial match, nested heading risks |
| [Challenge 2: CI Gap — No .jerry.yaml Schema Validation](#challenge-2-ci-gap--no-jerryyaml-schema-validation) | H-34 claims CI validates; CI does not |
| [Challenge 3: Format Detection is a Fragile Heuristic](#challenge-3-format-detection-is-a-fragile-heuristic) | The 43/15 XML/markdown split assumption |
| [Challenge 4: Governance Section Injection Order](#challenge-4-governance-section-injection-order) | Sections appended before XML transform — ordering risk |
| [Challenge 5: extract() Degrades Without .governance.yaml](#challenge-5-extract-degrades-without-governanceyaml) | Silent data loss on the reverse path |
| [Challenge 6: GovernanceSectionBuilder Covers Only 6 of 11 Governance Fields](#challenge-6-governancesectionbuilder-covers-only-6-of-11-governance-fields) | identity, persona, guardrails, output, constitution, validation omitted |
| [Challenge 7: Deprecation Notice Insufficient for Downstream Consumers](#challenge-7-deprecation-notice-insufficient-for-downstream-consumers) | Schema description-only deprecation has no enforcement path |
| [Challenge 8: Constitutional Triplet Auto-Injection Masks Real Gaps](#challenge-8-constitutional-triplet-auto-injection-masks-real-gaps) | Normalization silently corrects H-35 violations |
| [Challenge 9: Test Coverage Gaps](#challenge-9-test-coverage-gaps) | Missing boundary conditions and integration scenarios |
| [Summary Risk Table](#summary-risk-table) | Consolidated findings by criticality |

---

## Strategy Header

**Strategy:** S-002 Devil's Advocate
**Deliverable:** PROJ-012 governance migration — single-file architecture
**Analyst:** adv-executor
**Precondition:** S-003 Steelman must have run before this document. See `adversary-strategy-selection.md`.
**Scope:** Five implementation artifacts: `governance_section_builder.py`, `claude_code_adapter.py`, `agent-development-standards.md` (v1.3.0), `test_governance_section_builder.py`, `test_claude_code_adapter.py`
**Approach:** Challenge every key assumption. Find weaknesses, contradictions, and gaps. Evidence-first — each challenge cites specific file and line.

---

## Challenge 1: Heading-Based Dedup Robustness

**Criticality: MAJOR**

### The Claim

`GovernanceSectionBuilder._extract_headings()` prevents duplicate governance sections by checking whether a heading like `"Agent Version"` already exists in the prompt body before appending it.

### The Challenge

**Case sensitivity is a latent defect.** The regex at line 117 of `governance_section_builder.py` is:

```python
for match in re.finditer(r"^##\s+(.+?)(?:\s*<!--.*-->)?\s*$", body, re.MULTILINE):
    headings.add(match.group(1).strip())
```

The heading text is added to the set verbatim. The membership check at line 60 is:

```python
if agent.version and "Agent Version" not in existing_headings:
```

This is a case-sensitive string comparison. A prompt body containing `## AGENT VERSION`, `## agent version`, or `## Agent version` would not match `"Agent Version"` and the builder would inject a second section. The result is two sections with the same semantic meaning but different heading strings — a silent duplication defect.

**Evidence that this matters:** The 58 agents recomposed include bodies from both XML-formatted agents (where headings become tags) and markdown-formatted agents (where headings remain as-is). Markdown-format agent bodies authored by humans may use casing that deviates from the builder's expected exact strings. Nothing in the composition pipeline enforces heading casing in source prompt files.

**Partial match false positive:** The regex matches entire `##`-level headings. But an agent prompt body could contain `## Session Context and Routing` — a legitimate domain heading that is a superset of the governance-injected `## Session Context`. The current check `"Session Context" not in existing_headings` would NOT suppress injection because the set contains `"Session Context and Routing"`, not `"Session Context"`. Both headings would appear. Whether this causes harm depends on the PromptTransformer downstream: if it maps both to `<session_context>` XML tags, the body will contain two `<session_context>` blocks.

**Nested heading risk:** The regex matches only `##`-level headings (two `#` characters). A `###`-level subheading like `### Enforcement Guidelines` is not in the set. The builder would inject `## Enforcement` even if the body already addresses enforcement at a deeper level. This is arguably correct behavior, but the design rationale is not documented and could surprise future maintainers.

**No test covers case-insensitive collision.** `TestBuildWithExistingBody` tests exact-match suppression only. No test checks `## ENFORCEMENT`, `## enforcement`, or `## Enforcement Rules`.

---

## Challenge 2: CI Gap — No .jerry.yaml Schema Validation

**Criticality: CRITICAL**

### The Claim

`agent-development-standards.md` v1.3.0, H-34 states:

> "L5 (CI): JSON Schema validation on canonical `.jerry.yaml` files on PR."

The L2-REINJECT comment at line 7 also states:

> "CI validates canonical .jerry.yaml sources."

### The Challenge

The CI pipeline (`ci.yml`) has no job that validates `.jerry.yaml` files against `agent-canonical-v1.schema.json`. The workflow contains these jobs: `lint`, `type-check`, `security`, `plugin-validation`, `template-validation`, `license-headers`, `cli-integration`, `test-pip`, `test-uv`, `version-sync`, `hard-rule-ceiling`, `coverage-report`. None of them perform JSON Schema validation on `skills/*/composition/*.jerry.yaml`.

**Evidence from `ci.yml`:**

The search for `jerry.yaml`, `agent-canonical`, `canonical.*schema`, and `conformance` in `.github/workflows/ci.yml` returns zero results.

The `check_agent_conformance.py` script exists and validates `.md` frontmatter against required YAML sections for `nse` and `ps` families. It is **not invoked in any CI job**.

**Consequence:** The documented H-34 L5 enforcement is aspirational, not operational. A `.jerry.yaml` file that is missing required fields (`version`, `tool_tier`, `identity`) would pass CI without warning. The quality gate claim in H-34 ("Schema validation MUST execute before LLM-based quality scoring for C2+ deliverables") has no automated enforcement. This is an H-34 compliance gap that the document itself introduced.

**This is not a minor documentation lag.** The `quality-enforcement.md` L5 enforcement layer is described as "Immune" to context rot precisely because it is deterministic. If the CI job does not exist, the layer is absent, not immune. The distinction matters: a missing L5 gate means no post-hoc catch when the L1/L2/L3 gates fail.

**The `validate_schemas.py` script** validates hook output schemas only (`schemas/hooks/*.schema.json`), not agent canonical schemas. It is not a substitute.

---

## Challenge 3: Format Detection is a Fragile Heuristic

**Criticality: MAJOR**

### The Claim

`ClaudeCodeAdapter._detect_body_format()` determines whether a body is XML or markdown by counting tag occurrences vs `##`-heading occurrences and returning XML if `xml_count > md_count`.

### The Challenge

**The heuristic breaks on mixed-format bodies.** The regex `<[a-z_]+>` at line 425 matches any lowercase XML-style opening tag — including tags inside code blocks, inline examples, and template fragments. An agent methodology section that documents XML output format with example snippets like `<identity>`, `<capabilities>`, etc. would inflate `xml_count` without the body being XML-formatted.

**Concrete failing scenario:**

```markdown
## Methodology

The agent produces structured output using XML sections:

Example:
<identity>
Role description here.
</identity>
<capabilities>
Tool list here.
</capabilities>
```

This markdown-format body would have `xml_count=2` (the example tags) and `md_count=1` (the `## Methodology` heading). The heuristic classifies it as XML, triggering `PromptTransformer.from_xml()` during extract — which would incorrectly parse prose as structured XML sections.

**The 43/15 split is an artifact of current corpus size.** The `_detect_body_format()` docstring provides no documentation on why `xml_count > md_count` is the threshold. Given the current corpus of 58 agents split between XML and markdown formats, the existing agents happened to pass. But the heuristic has no principled boundary — it is a vote count with no tie-breaking guarantee.

**Tie case:** When `xml_count == md_count` (including the `0 == 0` case for plain prose), the method returns `BodyFormat.MARKDOWN`. The test `test_no_tags_no_headings_defaults_to_markdown` verifies this. But the fallback is not documented as a policy decision — it is a consequence of the `>` operator. A future maintainer changing `>` to `>=` would invert the tie behavior silently.

**No test exercises the mixed-format false-positive scenario** described above. The three tests cover clean XML bodies, clean markdown bodies, and empty bodies. The adversarial case — markdown bodies with XML examples in methodology sections — is unexercised.

---

## Challenge 4: Governance Section Injection Order

**Criticality: MAJOR**

### The Claim

`ClaudeCodeAdapter._build_body()` injects governance sections after the canonical prompt body and before the PromptTransformer call, so governance sections become XML tags in XML-format agents.

### The Challenge

**The injection always appends to the end of the body.** Line 288:

```python
canonical_body = canonical_body.rstrip("\n") + "\n\n" + governance_sections
```

For XML-format agents, the body is then wrapped in `<agent>` tags (line 298):

```python
body = "<agent>\n\n" + body.rstrip("\n") + "\n\n</agent>\n"
```

This means the final XML structure is always:

```xml
<agent>
  <identity>...</identity>
  <purpose>...</purpose>
  ...original sections...
  <agent_version>...</agent_version>
  <tool_tier>...</tool_tier>
  <enforcement>...</enforcement>
  ...governance sections...
</agent>
```

**Governance sections are always last.** If a future agent's LLM processing depends on section ordering (e.g., constitutional compliance checks referencing the `<enforcement>` block as context for `<methodology>`), the ordering is fixed by the pipeline, not by the agent author. There is no mechanism to inject governance sections at a specific position relative to domain content.

**The PromptTransformer's behavior with back-to-back governance YAML sections is untested.** `_format_dict()` produces YAML-formatted content for dict fields. If the PromptTransformer converts `## Enforcement` to `<enforcement>` and the content inside is multi-line YAML, the XML output becomes:

```xml
<enforcement>
tier: medium
escalation_path: Warn on missing file
</enforcement>
```

This is not valid XML content — it is YAML embedded in XML tags. Claude Code's runtime parser may treat this differently than expected. No integration test verifies that the PromptTransformer correctly handles YAML-formatted content inside governance sections.

**The `<agent>` wrapper is applied after governance injection.** If the PromptTransformer's `to_format()` call produces an `<agent>` tag internally (which it should not based on the strip logic), the double-wrap scenario would produce `<agent><agent>...</agent></agent>`. The `_strip_agent_wrapper()` method handles this on the extract path, but the generate path has no equivalent guard.

---

## Challenge 5: extract() Degrades Without .governance.yaml

**Criticality: MAJOR**

### The Claim

The architecture migrated from dual-file to single-file. The `.governance.yaml` companion file is no longer generated. The `extract()` method can still accept `governance_yaml_path` as an optional parameter for backward compatibility.

### The Challenge

**The extract path still depends heavily on `.governance.yaml` for rich governance data.** Lines 119-124 of `claude_code_adapter.py`:

```python
gov_data: dict[str, Any] = {}
if governance_yaml_path:
    gov_path = Path(governance_yaml_path)
    if gov_path.exists():
        gov_content = gov_path.read_text(encoding="utf-8")
        gov_data = yaml.safe_load(gov_content) or {}
```

When `governance_yaml_path` is `None` (the new normal for composed agents), `gov_data` is empty. All governance fields default: `version="1.0.0"`, `tool_tier=T1`, `identity={}`, `persona={}`, `guardrails={}`, `output={}`, `constitution={}`, `enforcement={}`, `session_context={}`, `prior_art=[]`.

**Identity is left empty.** The `CanonicalAgent.identity` field is required for schema validation per `agent-canonical-v1.schema.json` (it requires `role`, `expertise`, `cognitive_mode`). An extracted canonical agent with `identity={}` would fail schema validation on the re-compose path.

**There is no extraction of governance data from the XML body.** Governance sections are injected as XML tags (`<agent_version>`, `<tool_tier>`, etc.) during compose. But `extract()` does not parse these tags back out to populate `gov_data`. The body is passed to `PromptTransformer.from_xml()` to convert sections to markdown headings, but the governance XML sections would be converted to markdown headings and included in `prompt_body` — not extracted to structured governance fields.

**Consequence:** The round-trip for post-migration composed agents is broken. Running `jerry agents extract` on a composed single-file agent would produce a `.jerry.yaml` with:
- `version: 1.0.0` (wrong — the real version is in the XML body)
- `tool_tier: T1` (wrong — the real tier is in the XML body)
- `identity: {}` (wrong — identity is in the XML body, not parseable without tag-aware extraction)
- `constitution: {}` plus auto-injected triplet (masking the real constitution)

This round-trip failure means the extract-then-recompose workflow is unreliable for any agent composed after PROJ-012. The `test_extract_reads_governance_yaml_when_provided` test only covers the legacy path (with an explicit `.governance.yaml`). No test exercises `extract()` on an agent composed by the new single-file pipeline.

---

## Challenge 6: GovernanceSectionBuilder Covers Only 6 of 11 Governance Fields

**Criticality: MAJOR**

### The Claim

GovernanceSectionBuilder injects governance metadata into the prompt body, making it accessible in the single-file architecture.

### The Challenge

`CanonicalAgent` has 11 governance-relevant fields that are NOT in the Claude Code YAML frontmatter (12 official fields). `GovernanceSectionBuilder.build()` injects sections for exactly 6 of them:

| Field | Injected by GovernanceSectionBuilder |
|-------|--------------------------------------|
| `version` | Yes (`## Agent Version`) |
| `tool_tier` | Yes (`## Tool Tier`) |
| `enforcement` | Yes (`## Enforcement`) |
| `portability` | Yes (`## Portability`) |
| `prior_art` | Yes (`## Prior Art`) |
| `session_context` | Yes (`## Session Context`) |
| `identity` | **No** |
| `persona` | **No** |
| `guardrails` | **No** |
| `output` | **No** |
| `constitution` | **No** |
| `validation` | **No** |

**Evidence:** `governance_section_builder.py` lines 59-88. The method `build()` has six `if` blocks, one for each injected field. There is no block for `identity`, `persona`, `guardrails`, `output`, `constitution`, or `validation`.

**The rationale for omitting these 5 fields is not documented** anywhere in the builder, the adapter, the standards document, or the tests. The most likely explanation is that these fields are expected to appear in the prompt body text authored by the human (the `.jerry.prompt.md`). But this assumption is not enforced. An agent whose `.jerry.prompt.md` omits `## Guardrails` would produce a composed file with no guardrails section at all — not from the prompt body and not from the builder.

**Implication for H-35:** The constitutional compliance triplet (`P-003`, `P-020`, `P-022`) lives in `constitution.principles_applied`. This field is not injected by the builder. If an agent's prompt body does not include a `## Constitution` section, there is no machine-readable reference to constitutional compliance in the composed file's XML body. H-35 compliance becomes a human convention rather than a pipeline-enforced property.

**The `agent-development-standards.md` v1.3.0 does not document which fields are builder-injected vs. author-supplied.** This is a documentation gap that will cause confusion when new agents are authored. An author who writes a `.jerry.prompt.md` without a `## Constitution` section may not know that the pipeline will not inject one on their behalf.

---

## Challenge 7: Deprecation Notice Insufficient for Downstream Consumers

**Criticality: MINOR**

### The Claim

`docs/schemas/agent-governance-v1.schema.json` carries a deprecation notice in its `description` field noting that `.governance.yaml` files are no longer generated.

### The Challenge

**JSON Schema `description` fields are not machine-readable deprecation markers.** Tooling that imports or validates against `agent-governance-v1.schema.json` would not see any structural signal that the schema is deprecated — only a human reading the description string would notice. There is no `deprecated: true` property, no `$comment` with migration path, and no semantic versioning bump that signals a breaking change.

**The `scripts/fix_governance_schema.py` and `scripts/fix_governance.py` scripts** still reference `.n.yaml` files (visible in the grep output from `scripts/`). These scripts were apparently used during migration and now contain dead references. If a new contributor runs these scripts against the current repo state, they would search for `*.n.yaml` files that no longer exist (post-compose) and produce misleading output or silently no-op.

**The `check_agent_conformance.py` script** still defines `AGENT_PATTERNS` pointing to `skills/nasa-se/agents/nse-*.md` and `skills/problem-solving/agents/ps-*.md`, and validates `version` as a required top-level YAML key in frontmatter. Post-migration, `version` is not in the `.md` frontmatter — it is injected into the body as `<agent_version>`. The conformance checker's `top_level` field validation would now flag all migrated agents as non-conformant. Whether this script is still run (it is not in CI) is unclear; if it is run locally, it would produce false negatives.

---

## Challenge 8: Constitutional Triplet Auto-Injection Masks Real Gaps

**Criticality: MAJOR**

### The Claim

`ClaudeCodeAdapter._ensure_constitutional_triplet()` adds missing P-003, P-020, P-022 entries during `extract()` to normalize pre-existing compliance gaps.

### The Challenge

**Auto-injection is a compliance correction, not compliance enforcement.** When `extract()` silently adds `"P-003: No Recursive Subagents (Hard)"` to `principles_applied`, the resulting `.jerry.yaml` canonical file passes H-35 schema validation — but the original agent definition had the violation. The pipeline masks the gap rather than surfacing it.

**The method fires unconditionally during extract.** Lines 361-383 of `claude_code_adapter.py` add missing principles and forbidden actions with no warning, no log message, and no tracking in the extract result. The `ExtractResult` entity tracks `extracted` and `failed` counts, but has no `normalized` or `compliance_corrected` counter. A user running `jerry agents extract` would not know that compliance normalization occurred.

**Evidence of the problem's scope:** The PROJ-012 deliverable summary states "58 agents recomposed." If any of those 58 source `.jerry.yaml` files were produced by `extract()`, they carry silently-added constitutional entries that did not exist in the original agent definition. Downstream tools (e.g., a future audit script) would conclude these agents were compliant before migration, which may not be true.

**The test `test_idempotent_when_complete`** verifies that a complete constitution is not modified. But no test verifies that the auto-injection produces a warning or log entry. The silent mutation pattern is untested from an observability perspective.

---

## Challenge 9: Test Coverage Gaps

**Criticality: MAJOR**

### GovernanceSectionBuilder test gaps

| Missing Scenario | Risk |
|-----------------|------|
| Case-insensitive heading collision (`## ENFORCEMENT` suppresses injection) | Silent double-injection if casing differs |
| Superset heading collision (`## Session Context and Routing`) | Both sections injected |
| Body with `###`-level subheadings only (no `##`) | Governance sections injected even when domain covers same topic at `###` |
| Empty version string (falsy check) | `agent.version = ""` — passes the `if agent.version` guard only if truthy; empty string is falsy and no section generated. Correct behavior, but untested. |
| YAML dump of dict with unicode characters (allow_unicode=True) | No test verifies unicode round-trips through `_format_dict()` |
| Very large dict in enforcement/session_context (width=100 wrapping) | Wrapped YAML may break PromptTransformer line parsing |

### ClaudeCodeAdapter test gaps

| Missing Scenario | Risk |
|-----------------|------|
| `extract()` on a new-style single-file composed agent (no `.governance.yaml`, governance in XML body) | Round-trip failure undetected |
| Format detection with XML-example-in-markdown body | Misclassification as XML |
| Governance sections appearing in body before `<agent>` wrapper | Double-wrap guard not tested on generate path |
| `_build_body()` with both XML and governance sections where governance headings conflict | Undefined behavior |
| `generate()` with `agent.version = ""` (empty string) | Empty `## Agent Version` section generated with no content |
| CI schema validation absent (integration-level) | No test verifies the H-34 L5 claim that schema validation runs |
| `extract()` with path that is not under `skills/{skill}/agents/` structure | Line 128 (`md_path.parent.parent.name`) would return wrong skill name |

### Key structural test gap

Neither test file contains an end-to-end test that:
1. Starts with a `.jerry.yaml` + `.jerry.prompt.md` source pair
2. Runs through `ComposeCommandHandler` → `ClaudeCodeAdapter.generate()`
3. Then runs the output through `ClaudeCodeAdapter.extract()`
4. Asserts that the round-tripped `CanonicalAgent` matches the original

This test would immediately surface the round-trip failure described in Challenge 5.

---

## Summary Risk Table

| # | Challenge | Criticality | Evidence File | Key Risk |
|---|-----------|-------------|---------------|----------|
| 1 | Case-sensitive heading dedup | MAJOR | `governance_section_builder.py:117` | Silent double-injection for agents with non-exact-case headings |
| 2 | CI gap: no .jerry.yaml schema validation | CRITICAL | `ci.yml` (no jerry.yaml step), `agent-development-standards.md:33` (H-34 claim) | H-34 L5 enforcement is documented but not operational; schema gaps reach production |
| 3 | Format detection is a fragile heuristic | MAJOR | `claude_code_adapter.py:425-433` | XML-example-in-markdown bodies misclassified; round-trip corruption |
| 4 | Governance injection order is fixed at tail | MAJOR | `claude_code_adapter.py:288,298` | YAML-in-XML governance sections not validated; ordering not configurable |
| 5 | extract() degrades without .governance.yaml | MAJOR | `claude_code_adapter.py:119-124`, `extract_canonical_command_handler.py:112` | Round-trip for new-style composed agents produces incomplete canonical with empty identity |
| 6 | GovernanceSectionBuilder covers 6 of 11 fields | MAJOR | `governance_section_builder.py:59-88` | identity, persona, guardrails, output, constitution, validation not injected; H-35 not pipeline-enforced |
| 7 | Deprecation notice insufficient | MINOR | `agent-governance-v1.schema.json:5`, `scripts/fix_governance.py` | Migration scripts have dead references; conformance checker produces false negatives |
| 8 | Constitutional triplet auto-injection masks gaps | MAJOR | `claude_code_adapter.py:349-384` | Silent compliance correction during extract; no observability; audit trail gap |
| 9 | Test coverage gaps | MAJOR | Both test files | Round-trip not tested; adversarial format detection not tested; CI schema claim not tested |

### Criticality Count

| Level | Count |
|-------|-------|
| CRITICAL | 1 |
| MAJOR | 7 |
| MINOR | 1 |
| INFORMATIONAL | 0 |

---

*Strategy: S-002 Devil's Advocate*
*Analyst: adv-executor*
*Date: 2026-02-26*
*Source deliverable: PROJ-012 governance migration — single-file architecture*
*Output path: `projects/PROJ-012-agent-optimization/analysis/adversary-s002-devils-advocate.md`*

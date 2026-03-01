# Strategy Execution Report: S-007 Constitutional AI Critique

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverable, timestamp |
| [Findings Summary](#findings-summary) | All findings by severity |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, recommendation per finding |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Execution Context

- **Strategy:** S-007 (Constitutional AI Critique)
- **Template:** `.context/templates/adversarial/s-007-constitutional-ai.md`
- **Deliverables Reviewed:**
  - `src/agents/domain/services/governance_section_builder.py`
  - `src/agents/infrastructure/adapters/claude_code_adapter.py`
  - `src/agents/domain/services/prompt_transformer.py`
  - `.context/rules/agent-development-standards.md`
  - `docs/schemas/agent-governance-v1.schema.json`
  - `skills/adversary/agents/adv-executor.md` (XML-format spot-check)
  - `skills/problem-solving/agents/ps-researcher.md` (XML-format spot-check)
  - `skills/orchestration/agents/orch-planner.md` (XML-format spot-check)
- **Executed:** 2026-02-26
- **Agent:** adv-executor (S-007)

---

## Findings Summary

| ID | Severity | Finding | File |
|----|----------|---------|------|
| CC-001 | Minor | adv-executor.md missing P-020 in constitutional compliance table | `skills/adversary/agents/adv-executor.md` |
| CC-002 | Minor | adv-executor.md body_format declaration misleading (declares "markdown", uses XML section tags) | `skills/adversary/agents/adv-executor.md` |
| CC-003 | Minor | adv-executor.md governance sections placed outside `</agent>` wrapper | `skills/adversary/agents/adv-executor.md` |
| CC-004 | PASS | H-07: GovernanceSectionBuilder domain layer isolation — clean | `governance_section_builder.py` |
| CC-005 | PASS | H-10: One class per file — all three Python files clean | All three Python files |
| CC-006 | PASS | H-34 Architecture Note: single-file description accurate and internally consistent | `agent-development-standards.md` |
| CC-007 | PASS | H-34/H-35 L2-REINJECT marker updated to single-file language | `agent-development-standards.md` |
| CC-008 | Minor | quality-enforcement.md H-34 summary row does not reflect new single-file architecture language | `quality-enforcement.md` |
| CC-009 | PASS | agent-governance-v1.schema.json deprecation notice accurate for compose path; extract backward-compat is valid | `agent-governance-v1.schema.json` |
| CC-010 | PASS | ps-researcher.md: P-003, P-020, P-022 all present with forbidden actions | `ps-researcher.md` |
| CC-011 | PASS | orch-planner.md: P-003, P-020, P-022 all present with forbidden actions | `orch-planner.md` |
| CC-012 | PASS | ClaudeCodeAdapter: infrastructure layer imports only application ports and domain — no inversion | `claude_code_adapter.py` |

---

## Detailed Findings

### CC-001: adv-executor Missing P-020 in Constitutional Compliance Table

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `skills/adversary/agents/adv-executor.md` |
| **Section** | `<constitutional_compliance>` |
| **Principle Violated** | H-35 (constitutional triplet P-003, P-020, P-022 required) |

**Evidence:**

The `<constitutional_compliance>` section of `adv-executor.md` lists principles P-001, P-002, P-003, P-004, P-011, P-022, and H-15. P-020 (User Authority — never override) is absent from this table:

```markdown
| Principle | Agent Behavior |
|-----------|----------------|
| P-001 (Truth/Accuracy) | Findings based on specific evidence from the deliverable |
| P-002 (File Persistence) | Execution report MUST be persisted to file |
| P-003 (No Recursion) | Does NOT invoke other agents or spawn subagents |
| P-004 (Provenance) | Strategy ID, template path, and evidence cited for every finding |
| P-011 (Evidence-Based) | Every finding includes direct evidence from the deliverable |
| P-022 (No Deception) | Findings honestly reported; severity not minimized or inflated |
| H-15 (Self-Review) | Execution report self-reviewed before persistence (S-010) |
```

The `<p003_self_check>` section confirms P-003 enforcement but does not compensate for P-020 absence in the compliance declaration.

**Analysis:**

H-35 requires every agent to declare the constitutional triplet P-003, P-020, P-022 in its compliance section. adv-executor is a worker agent that executes adversarial strategies against deliverables. While the agent has no direct opportunity to override user intent (it follows templates), the compliance declaration must still assert P-020 per H-35. The omission is a documentation gap, not a functional violation, but it reduces auditability and L5 CI grep coverage.

Note: adv-executor IS a composed agent (it has governance sections injected at the end of the file). The `_ensure_constitutional_triplet()` method in `ClaudeCodeAdapter.extract()` would add P-020 to `constitution.principles_applied` during an extract round-trip — but the composed `.md` body's `<constitutional_compliance>` table would not be updated by that mechanism. The gap exists at the body level.

**Recommendation:**

Add P-020 to the `<constitutional_compliance>` table in `adv-executor.md`:

```markdown
| P-020 (User Authority) | Strategy execution does not override user decisions; escalates conflicts to orchestrator |
```

---

### CC-002: adv-executor body_format Declaration Misleading

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `skills/adversary/agents/adv-executor.md` |
| **Section** | `## Portability` (governance injection at end of file) |
| **Principle Violated** | P-022 (no deception about capabilities/state) |

**Evidence:**

The injected `## Portability` section at the bottom of `adv-executor.md` declares:

```yaml
enabled: true
minimum_context_window: 128000
reasoning_strategy: adaptive
body_format: markdown
```

However, the body of the file uses XML-style section delimiters as primary structure markers:

```
<identity>     -- line-start, section-level
<purpose>      -- line-start, section-level
<input>        -- line-start, section-level
<execution_process>  -- non-standard, line-start
<output>       -- line-start, section-level
<constitutional_compliance>  -- non-standard, line-start
```

The `_detect_body_format()` method in `ClaudeCodeAdapter` counts `xml_count=6` vs `md_count=13` (because there are 13 `##` headings inside the XML sections). Since 6 < 13, the detector classifies the body as `MARKDOWN`. This is technically consistent with the declaration, but the body's primary structural delimiter is XML tags, not markdown headings. The declaration of `body_format: markdown` does not accurately represent the actual body structure.

**Analysis:**

The functional impact is that `to_format(body, MARKDOWN)` passes the body through unchanged, which preserves the XML tags. This works correctly at runtime. However, the mismatch creates a correctness risk for any consumer that interprets `body_format: markdown` to mean "no XML tags in the body" — for example, a round-trip extract that converts XML to markdown headings before re-composing. If `_detect_body_format()` returned `XML` (the structurally accurate answer), the body would be parsed and re-serialized correctly.

The root cause is the `_detect_body_format()` heuristic: it counts all XML-like patterns including those inside code blocks and nested content, and all `##` headings including those within XML sections, so a body with few top-level XML section tags and many inner headings is miscategorized.

**Recommendation:**

Either: (a) Update the adv-executor canonical source to declare `body_format: xml` to match its actual section structure, or (b) Improve `_detect_body_format()` to count only line-start XML tags (`^<[a-z_]+>`) rather than all occurrences. Option (b) fixes the detection for all agents. This is a Minor finding because runtime behavior is correct for the current compose path.

---

### CC-003: adv-executor Governance Sections Placed Outside `</agent>` Wrapper

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `skills/adversary/agents/adv-executor.md` |
| **Section** | Post-`</agent>` content |
| **Principle Violated** | H-34 (agent definition structural integrity) |

**Evidence:**

The `adv-executor.md` file contains a `</agent>` closing tag at position 15424, after which the governance sections appear:

```
</agent>

---

*Agent Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*

## Agent Version

1.0.0

## Tool Tier

T2 (Read-Write)

## Portability

enabled: true
minimum_context_window: 128000
reasoning_strategy: adaptive
body_format: markdown
```

This is structurally anomalous. The agent body is wrapped in `<agent>...</agent>` tags (per the compose pipeline behavior for XML-format agents), but the injected governance sections appear outside the closing tag. The `_strip_agent_wrapper()` method in `ClaudeCodeAdapter.extract()` strips the `<agent>` wrapper before further processing, so the governance sections outside the wrapper would be included in the `canonical_body` after stripping.

**Analysis:**

The `GovernanceSectionBuilder.build()` appends governance sections to `canonical_body` before format transformation (step 2 in `_build_body()`). For XML-format agents, the entire transformed body including governance sections is then wrapped in `<agent>...</agent>` tags (step 5). For agents with `body_format: markdown` (as declared for adv-executor), `to_format()` is a pass-through, so governance sections are appended to the existing `<agent>...</agent>` structure rather than inside it. This places governance metadata outside the agent wrapper, which may cause the LLM to miss it depending on how Claude Code parses the body.

This is a compose pipeline structural issue specific to agents that were originally composed with `<agent>` wrappers but are declared as `body_format: markdown`. The actual source of this issue is the `body_format` mismatch noted in CC-002.

**Recommendation:**

Resolve CC-002 (declare `body_format: xml` for adv-executor). Once the format is correctly identified as XML, the compose pipeline will wrap the entire body including governance sections inside `<agent>...</agent>`. Alternatively, the `_build_body()` method should inject governance sections inside the existing `<agent>` wrapper rather than appending after it.

---

### CC-004 (PASS): H-07 — GovernanceSectionBuilder Domain Layer Isolation

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **File** | `src/agents/domain/services/governance_section_builder.py` |
| **Principle Checked** | H-07 (architecture layer isolation) |

**Evidence:**

All imports in `governance_section_builder.py` resolve to standard library, third-party, or domain-layer paths:

```python
from __future__ import annotations
import re
from typing import Any
import yaml
from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.value_objects.tool_tier import ToolTier
```

No imports from `src.agents.infrastructure`, `src.agents.application`, or `src.agents.interface` are present. The file imports only from `src.agents.domain.*`, which is permitted for a domain service. H-07 is satisfied.

---

### CC-005 (PASS): H-10 — One Class Per File

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **Files** | All three Python files reviewed |
| **Principle Checked** | H-10 (one class per file) |

**Evidence:**

- `governance_section_builder.py`: `class GovernanceSectionBuilder` — 1 class
- `prompt_transformer.py`: `class PromptTransformer` — 1 class
- `claude_code_adapter.py`: `class ClaudeCodeAdapter` — 1 class

All three files comply with H-10. The module-level constant `_TOOL_TIER_LABELS` (dict) and `_HEADING_TO_TAG` (dict) are not classes and do not constitute violations.

---

### CC-006 (PASS): H-34 Architecture Note Accurately Describes Single-File Architecture

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **File** | `.context/rules/agent-development-standards.md` |
| **Principle Checked** | H-34, P-022 (no deception about architecture) |

**Evidence:**

The H-34 Architecture Note in `agent-development-standards.md` (VERSION: 1.3.0, dated 2026-02-26) accurately describes the PROJ-012 single-file architecture:

> Agent definitions use a single-file composed output architecture:
> - `.md` YAML frontmatter: Official Claude Code fields only (12 recognized fields...)
> - `.md` markdown body: System prompt content... governance metadata... as XML-tagged sections. Governance sections are injected by the compose pipeline from canonical `.jerry.yaml` sources.
> - Canonical sources (inputs to compose): `skills/*/composition/*.jerry.yaml`...
> - Deprecated schemas: `docs/schemas/agent-governance-v1.schema.json` and `docs/schemas/agent-definition-v1.schema.json` are retained for reference only.

This is verified to be consistent with the actual implementation: `ClaudeCodeAdapter.generate()` returns only one `GeneratedArtifact` of type `agent_definition` (the `.md` file), and no `.governance.yaml` is written anywhere in the compose pipeline.

---

### CC-007 (PASS): H-34 L2-REINJECT Marker Updated to Single-File Language

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **File** | `.context/rules/agent-development-standards.md` |
| **Principle Checked** | H-34, enforcement architecture Layer L2 |

**Evidence:**

The L2-REINJECT marker at rank=5 reads:

> Agent definitions: single-file architecture — official Claude Code frontmatter + governance in prompt body as XML sections (H-34). Governance fields (version, tool_tier, enforcement, portability, session_context) injected by compose pipeline. Tool tiers T1-T5: always select lowest tier satisfying requirements. Cognitive modes: divergent, convergent, integrative, systematic, forensic. Constitutional triplet (P-003, P-020, P-022) REQUIRED in every agent (H-35). CI validates canonical .jerry.yaml sources.

This correctly reflects the new single-file architecture. No stale `dual-file` or `.governance.yaml companion file` language remains in this marker.

---

### CC-008: quality-enforcement.md H-34 Summary Row Stale

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `.context/rules/quality-enforcement.md` |
| **Section** | HARD Rule Index table, H-34 row |
| **Principle Violated** | P-022 (deception by stale description), H-19 (governance accuracy) |

**Evidence:**

The HARD Rule Index table in `quality-enforcement.md` has this H-34 entry:

```markdown
| H-34 | Agent definition standards (YAML schema validation, constitutional compliance triplet) | agent-development-standards |
```

The description "Agent definition standards (YAML schema validation, constitutional compliance triplet)" does not mention the architectural change from dual-file to single-file composition. The old v1.2.0 text referred to `.governance.yaml` files; the new v1.3.0 architecture eliminates them. The summary row is stale relative to the full rule text in `agent-development-standards.md`.

**Analysis:**

The `quality-enforcement.md` HARD Rule Index is a summary/index document that points to `agent-development-standards.md` as the source. The summary row is intentionally brief. However, the current description would not signal to a reader that the architecture changed — a reader consulting only `quality-enforcement.md` would not know that `.governance.yaml` companion files are no longer generated. This creates a documentation gap that could lead to wrong-direction work (H-31 alignment issue). The L2-REINJECT at rank=5 is in `agent-development-standards.md`, not `quality-enforcement.md`, so the re-injection does not compensate for this gap.

**Recommendation:**

Update the H-34 summary row in `quality-enforcement.md` to include the architectural change:

```markdown
| H-34 | Agent definition standards (single-file architecture: official Claude Code frontmatter + governance in prompt body; CI validates canonical .jerry.yaml sources) | agent-development-standards |
```

---

### CC-009 (PASS): agent-governance-v1.schema.json Deprecation Notice Accurate

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **File** | `docs/schemas/agent-governance-v1.schema.json` |
| **Principle Checked** | P-022 (accurate description of capabilities/state) |

**Evidence:**

The schema's `description` field reads:

> DEPRECATED (PROJ-012): .governance.yaml companion files are no longer generated. Governance metadata is now injected into the .md prompt body as XML sections by the compose pipeline. CI validation should use agent-canonical-v1.schema.json against canonical .jerry.yaml source files. This schema is retained for reference and backward-compatible extract() operations only.

This is verified accurate:
1. The compose pipeline (`ClaudeCodeAdapter.generate()`) produces only `.md` artifacts — no `.governance.yaml` output.
2. The extract pipeline (`ClaudeCodeAdapter.extract()`) still reads existing `.governance.yaml` files if present (via `governance_yaml_path` parameter), which is the backward-compat use case described.
3. The `extract_canonical_command_handler.py` discovers existing `.governance.yaml` files and passes them to `extract()` — this is the migration scenario for pre-PROJ-012 agents.

The deprecation notice accurately describes both what changed and what the schema is still valid for.

---

### CC-010 (PASS): ps-researcher Constitutional Compliance

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **File** | `skills/problem-solving/agents/ps-researcher.md` |
| **Principle Checked** | H-35 (P-003, P-020, P-022 triplet) |

**Evidence:**

ps-researcher explicitly lists all three in its `<capabilities>` forbidden actions section:

```markdown
- **P-003 VIOLATION:** DO NOT spawn subagents that spawn further subagents
- **P-020 VIOLATION:** DO NOT override explicit user instructions
- **P-022 VIOLATION:** DO NOT claim to have found information you didn't find
```

P-003, P-020, and P-022 are also referenced in the `<constitutional_compliance>` section with enforcement levels. The `tools` frontmatter field (`Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash`) does not include `Task`, which is correct for its declared role as a research specialist (the `<capabilities>` section mentions Task as a tool available during invocation, not as a frontmatter-declared tool).

Note: The Task tool reference in `<capabilities>` says "Single-level only (P-003)" — this is describing usage constraints within an orchestrated workflow where the orchestrator provides Task access, not that ps-researcher itself declares Task in its frontmatter. This is consistent with H-35.

---

### CC-011 (PASS): orch-planner Constitutional Compliance

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **File** | `skills/orchestration/agents/orch-planner.md` |
| **Principle Checked** | H-35 (P-003, P-020, P-022 triplet) |

**Evidence:**

orch-planner lists the constitutional triplet in its `<capabilities>` forbidden actions section and references P-003 in the invocation constraint (`<must_not>Spawn other agents (P-003)</must_not>`). All three principles are present. The `tools` frontmatter (`Read, Write, Edit, Glob, Grep, Bash`) does not include Task, which is appropriate for a planning agent that does not spawn workers itself.

---

### CC-012 (PASS): ClaudeCodeAdapter Layer Boundary Check

| Attribute | Value |
|-----------|-------|
| **Severity** | PASS |
| **File** | `src/agents/infrastructure/adapters/claude_code_adapter.py` |
| **Principle Checked** | H-07 (architecture layer isolation) |

**Evidence:**

ClaudeCodeAdapter is an infrastructure adapter. Its imports are:

```python
from src.agents.application.ports.vendor_adapter import IVendorAdapter
from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.entities.generated_artifact import GeneratedArtifact
from src.agents.domain.services.governance_section_builder import GovernanceSectionBuilder
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.tool_mapper import ToolMapper
from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier
from src.agents.domain.value_objects.vendor_target import VendorTarget
```

Infrastructure adapters are permitted to import from application ports (interfaces they implement) and domain entities/services. There are no inward violations (e.g., domain importing from infrastructure). H-07 is satisfied.

---

## Execution Statistics

- **Total Findings:** 12 (3 Minor defects, 9 PASS)
- **Critical:** 0
- **Major:** 0
- **Minor:** 3 (CC-001, CC-002, CC-003)
- **PASS:** 9 (CC-004 through CC-007, CC-009 through CC-012)
- **Protocol Steps Completed:** 7 of 7

---

## Constitutional Compliance Assessment

The PROJ-012 governance migration is constitutionally sound at the architectural level. The three Minor findings are all localized to a single agent file (`adv-executor.md`) and a single documentation summary row. None constitute HARD rule violations:

- CC-001 (P-020 missing from adv-executor): The principle is enforced by the `_ensure_constitutional_triplet()` method on extract; the gap is in the composed body declaration only.
- CC-002/CC-003 (body_format mismatch, governance outside wrapper): These are linked and stem from the same root cause — adv-executor has XML section tags but is labeled markdown. Fixing CC-002 fixes CC-003.
- CC-008 (stale H-34 summary): Documentation drift in an index document; the authoritative rule file is accurate.

The critical constitutional invariants are intact:
- H-07 (layer isolation): Verified clean across all three Python files.
- H-10 (one class per file): Verified across all three Python files.
- H-34 (single-file architecture): The architecture description, L2-REINJECT marker, and compose pipeline implementation are all consistent with the new single-file model.
- H-35 (constitutional triplet): All three spot-checked composed agents declare the triplet; adv-executor has a Minor gap (CC-001) at the body level only.
- P-003: No recursive subagent patterns detected in any reviewed file.
- P-020: No user authority overrides detected in any reviewed file.
- P-022: No deceptive capability claims detected; deprecation notices are accurate.

---

*Strategy: S-007 Constitutional AI Critique*
*Agent: adv-executor*
*Executed: 2026-02-26*
*Deliverables: 8 files reviewed (3 Python source, 1 rule file, 1 schema, 3 composed agents)*

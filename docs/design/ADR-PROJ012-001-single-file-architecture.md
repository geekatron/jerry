# ADR-PROJ012-001: Single-File Agent Definition Architecture

<!-- PS-ID: PROJ-012 | AGENT: ps-architect | DATE: 2026-02-26 -->
<!-- CRITICALITY: C3 (modifies .context/rules/, AE-002 auto-C3) -->

> Architecture Decision Record documenting the migration from dual-file (`.md` + `.governance.yaml`) to single-file (`.md` with governance in prompt body) agent definitions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | ADR lifecycle state |
| [Context](#context) | Problem motivating the change |
| [Decision](#decision) | What was decided and how it works |
| [Consequences](#consequences) | Positive outcomes, negative outcomes, and accepted risks |
| [Alternatives Considered](#alternatives-considered) | Options evaluated and rejection rationale |
| [References](#references) | Source document traceability |

---

## Status

**Accepted**

---

## Context

### Problem Statement

PROJ-012 identified three structural problems with the dual-file agent definition architecture (`.md` + `.governance.yaml`):

1. **Agent discovery pollution.** Claude Code discovers agents by scanning for `.md` files in `skills/*/agents/`. The `.governance.yaml` companion files in the same directory are inert -- Claude Code does not read them -- but their presence doubles the file count and creates a false impression that both files are required at runtime.

2. **No structural tie between companion files.** The only link between `ps-researcher.md` and `ps-researcher.governance.yaml` is the filename convention. No runtime or CI mechanism validates that they refer to the same agent, that their versions are synchronized, or that the governance file matches the agent definition it accompanies. This is a consistency hazard: editing one file without the other produces a silently inconsistent agent.

3. **Governance data invisible to the LLM at runtime.** The `.governance.yaml` file is consumed only during the compose pipeline. The agent LLM never sees it. Constitutional triplets (P-003, P-020, P-022), tool tier constraints, enforcement quality gates, and session context declarations exist in a file the agent cannot access. Governance is documented but not operationally present in the agent's context window.

### Driving Context

- **58 agents** across 8 skills used the dual-file format at migration time.
- **Claude Code silently discards** unrecognized YAML frontmatter fields -- governance data cannot be placed in frontmatter.
- **PROJ-010** established the canonical agent architecture (`CanonicalAgent`, `.jerry.yaml` source files, compose pipeline) that PROJ-012 builds upon.
- **S-003 Steelman Analysis** (`projects/PROJ-012-agent-optimization/analysis/adversary-s003-steelman.md`) provided the affirmative case across six sub-decisions.
- **S-002 Devil's Advocate Analysis** (`projects/PROJ-012-agent-optimization/analysis/adversary-s002-devils-advocate.md`) identified nine challenges, including extract() round-trip degradation, 6-of-11 field coverage, and CI validation gaps.

---

## Decision

Remove `.governance.yaml` companion files from composed output. Inject governance metadata into the `.md` prompt body as XML sections via the compose pipeline. CI validation targets canonical `.jerry.yaml` source files, not composed output.

### Architecture

The compose pipeline transforms canonical sources into a single `.md` artifact per agent:

```
Canonical Sources                    Compose Pipeline                     Output
-------------------                  ----------------                     ------
*.jerry.yaml          -->  CanonicalAgent  -->  GovernanceSectionBuilder  -->  Single .md file
*.jerry.prompt.md     -->       |          -->  PromptTransformer             (frontmatter +
*.claude-code.yaml    -->       |          -->  ClaudeCodeAdapter              body with
                                |          -->  DefaultsComposer               governance XML)
                                |          -->  _filter_vendor_frontmatter()
```

**Transformation steps:**

1. `CanonicalAgent` fields (version, tool_tier, enforcement, portability, prior_art, session_context) are passed to `GovernanceSectionBuilder.build()`.
2. The builder emits these as `## Heading` markdown sections, checking for existing headings to prevent duplication.
3. `ClaudeCodeAdapter._build_body()` appends governance sections to the canonical prompt body.
4. `PromptTransformer` converts `## Heading` sections to `<xml_tag>` sections for XML-format agents.
5. `_filter_vendor_frontmatter()` ensures only Claude Code's 12 official fields appear in YAML frontmatter.
6. A single `GeneratedArtifact` is returned -- no `.governance.yaml` file is produced.

### Canonical Source Files (SSOT)

| File | Purpose |
|------|---------|
| `skills/*/composition/*.jerry.yaml` | Structured governance data (version, tool_tier, identity, persona, etc.) |
| `skills/*/composition/*.jerry.prompt.md` | System prompt body (identity, methodology, guardrails, output) |
| `skills/*/composition/*.claude-code.yaml` | Per-agent vendor overrides (optional) |

### Governance Fields Injected by Builder

The `GovernanceSectionBuilder` injects 6 of the 11 governance-relevant fields. The remaining 5 fields (identity, persona, guardrails, output, constitution) are expected to be authored in the `.jerry.prompt.md` prompt body by the agent developer.

| Field | Builder-Injected | Rationale |
|-------|-----------------|-----------|
| `version` | Yes | Metadata; not typically authored in prose |
| `tool_tier` | Yes | Metadata; not typically authored in prose |
| `enforcement` | Yes | Structured data; compose pipeline serializes |
| `portability` | Yes | Structured data; compose pipeline serializes |
| `prior_art` | Yes | List data; compose pipeline serializes |
| `session_context` | Yes | Structured data; compose pipeline serializes |
| `identity` | No | Authored as `<identity>` in prompt body |
| `persona` | No | Expressed through prompt body tone and style |
| `guardrails` | No | Authored as `<guardrails>` in prompt body |
| `output` | No | Authored as `<output>` in prompt body |
| `constitution` | No | Authored as `<guardrails>` constitutional subsection |

### H-34 Update

`agent-development-standards.md` H-34 Architecture Note was updated (v1.2.0 to v1.3.0) to describe the single-file architecture. The deprecated `.governance.yaml` schema (`agent-governance-v1.schema.json`) is retained for reference only. The canonical validation schema is `agent-canonical-v1.schema.json`, targeting `.jerry.yaml` source files.

---

## Consequences

### Positive

| Consequence | Impact |
|-------------|--------|
| Single file per agent in composed output | Eliminates file consistency hazard; simplifies downstream consumption (CI, extract, clean) |
| Governance visible to agent LLM at runtime | Constitutional constraints, tool tier, enforcement gates are in the agent's active context window |
| No dead-weight `.governance.yaml` files | 58 files (~3,480 lines) removed; agent directories contain only discoverable `.md` files |
| Compose pipeline simplification | Handler no longer parses or merges a second governance artifact; 4-layer merge operates on frontmatter only |
| Portability alignment | System prompt body is vendor-agnostic; governance travels with the agent definition to any LLM vendor |
| Backward-compatible `extract()` | Optional `governance_yaml_path` parameter still accepted for legacy workflows |

### Negative

| Consequence | Mitigation |
|-------------|------------|
| `extract()` reverse path must parse governance from XML body to produce complete `CanonicalAgent` | Known limitation documented in S-002 Challenge 5; extract of governance from body tags is a future enhancement |
| Builder covers 6 of 11 governance fields; remaining 5 rely on author convention | Reserved heading documentation added to `agent-development-standards.md`; prompt template convention in `.jerry.prompt.md` files |
| CI schema validation of `.jerry.yaml` not yet operational (documented as planned) | Compose-time Python validation provides interim enforcement; CI job tracked for implementation |
| Heading-based dedup is case-sensitive (mitigated by v1.3.0 adding case-insensitive comparison) | Case-insensitive heading comparison documented in Reserved Governance Headings section |

### Accepted Risks

| Risk | Severity | Rationale for Acceptance |
|------|----------|--------------------------|
| Format detection heuristic (XML vs markdown) may misclassify mixed-format bodies | MAJOR (S-002 Challenge 3) | Current corpus of 58 agents is cleanly split; adversarial case requires XML examples in markdown body, which is uncommon in practice |
| Constitutional triplet auto-injection during extract masks compliance gaps | MAJOR (S-002 Challenge 8) | Normalization ensures all extracted agents pass H-35; observability improvement (logging) tracked separately |

---

## Alternatives Considered

### Alternative 1: Keep Dual-File Architecture

**Description:** Retain `.md` + `.governance.yaml` as the composed output format.

**Rejection rationale:** Does not solve Problem 3 (governance invisible to LLM at runtime). Perpetuates the consistency hazard (Problem 2). Adds complexity to every downstream consumer that must locate and parse two files per agent.

### Alternative 2: Move `.governance.yaml` to a Separate Directory

**Description:** Keep `.governance.yaml` files but relocate them outside `skills/*/agents/` (e.g., to `skills/*/governance/`) to avoid polluting agent discovery.

**Rejection rationale:** Solves Problem 1 (discovery pollution) but not Problem 2 (no structural tie) or Problem 3 (invisible to LLM). The governance file would still be a disconnected sidecar with filename-only linkage.

### Alternative 3: Embed Governance in YAML Frontmatter

**Description:** Add governance fields directly to the `.md` YAML frontmatter instead of the prompt body.

**Rejection rationale:** Blocked by Claude Code's runtime behavior: unrecognized frontmatter fields are silently discarded. Any governance data placed in frontmatter would be lost at runtime. This is documented in the H-34 Architecture Note and confirmed by Claude Code's 12-field allowlist.

### Alternative 4: YAML-to-Markdown Pass from `.governance.yaml` SSOT

**Description:** Keep `.governance.yaml` as the SSOT for governance data and generate prompt body sections from it during compose.

**Rejection rationale:** Inverts the canonical source hierarchy established by PROJ-010. The canonical source for governance is `.jerry.yaml`, not `.governance.yaml` (a composed artifact). This approach would add a third transformation layer (YAML-to-markdown) on top of the existing markdown-to-XML pass, increasing pipeline complexity without solving the core problem.

---

## References

| Source | Content |
|--------|---------|
| `projects/PROJ-012-agent-optimization/analysis/adversary-s003-steelman.md` | S-003 Steelman analysis with six sub-decision justifications |
| `projects/PROJ-012-agent-optimization/analysis/adversary-s002-devils-advocate.md` | S-002 Devil's Advocate with nine challenges and risk table |
| `.context/rules/agent-development-standards.md` (v1.3.0) | Updated H-34 Architecture Note describing single-file architecture |
| `ADR-PROJ010-003` | PROJ-010 portability architecture establishing `CanonicalAgent` as vendor-neutral representation |
| `ADR-PROJ007-001` | Original agent definition format and design patterns ADR |
| `docs/schemas/agent-canonical-v1.schema.json` | Canonical schema for `.jerry.yaml` source validation |
| `docs/schemas/agent-governance-v1.schema.json` | Deprecated governance schema (retained for reference) |

---

*ADR Version: 1.0.0*
*Source: PROJ-012 Agent Optimization*
*Created: 2026-02-26*
*Criticality: C3 (AE-002: touches `.context/rules/`)*

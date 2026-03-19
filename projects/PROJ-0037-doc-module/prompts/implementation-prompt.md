# PE-Builder Engineered Prompt: Doc Module Implementation

> **Format:** 5-Element Anatomy (pe-builder v1.0.0)
> **Criticality:** C4 (all 10 adversarial strategies)
> **Quality Threshold:** >= 0.94 weighted composite
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-10

---

## Element 1: Skill Routing

```
/orchestration — orch-planner sequences the implementation pipeline
/eng-team — eng-backend (implementation), eng-qa (tests), eng-architect (security review), eng-reviewer (final gate)
/red-team — red-vuln (attack surface analysis of YAML injection + Jinja2 template trust boundary)
/adversary — C4 criticality, all 10 strategies, >= 0.94 threshold at each batch boundary
/worktracker — Tasks under ST-002 for each implementation phase
```

## Element 2: Scope

Implement the auto-documentation module per B4 spec, following the hexagonal architecture pattern established by `src/transcript/`.

**Production code (src/docs/ bounded context):**
- `domain/value_objects/skill_data.py` — SkillData dataclass
- `domain/value_objects/agent_data.py` — AgentData dataclass
- `domain/ports/frontmatter_reader.py` — IFrontmatterReader Protocol
- `domain/ports/template_renderer.py` — ITemplateRenderer Protocol
- `application/commands/generate_docs_command.py` — GenerateDocsCommand
- `application/handlers/commands/generate_docs_command_handler.py` — DocsGenerator
- `application/services/skill_extractor.py` — SkillExtractor
- `application/results/generate_docs_result.py` — GenerateDocsResult
- `infrastructure/adapters/jinja2_renderer.py` — Jinja2Renderer (SandboxedEnvironment)
- `infrastructure/adapters/ast_frontmatter_reader.py` — AstFrontmatterReader (calls jerry ast)

**Templates (.context/templates/docs/):**
- `skills-table.md.jinja2` — Skills table section
- `features-section.md.jinja2` — Features bullet list
- `_macros.jinja2` — Shared Jinja2 macros
- `skill-examples.yaml` — Static skill example mapping (13 entries)
- `features.yaml` — Curated features list (9 entries)

**Integration:**
- `src/interface/cli/parser.py` — `_add_docs_namespace()` registration
- `src/bootstrap.py` — DocsGenerator wiring
- `scripts/check_docs.py` — Pre-commit hook script

**Tests:**
- `tests/unit/docs/test_extractor.py` — 5 unit tests per B4 spec
- `tests/unit/docs/test_renderer.py` — 4 unit tests per B4 spec
- `tests/unit/docs/test_generator.py` — 1 unit test (atomic write)
- `tests/integration/docs/test_docs_generate.py` — 4 integration tests
- `tests/golden/docs/test_golden.py` — 2 golden file tests
- `tests/golden/docs/expected-skills-table.md` — Golden file
- `tests/golden/docs/expected-features.md` — Golden file

## Element 3: Data Sources

```
B4 Spec:     projects/PROJ-0037-doc-module/specifications/doc-module-spec.md
Threat Model: projects/PROJ-0037-doc-module/security/threat-model-doc-module.md
ADR:         projects/PROJ-0037-doc-module/decisions/ADR-PROJ0037-001-doc-module-design.md
Synthesis:   projects/PROJ-0037-doc-module/orchestration/doc-module-20260308-001/synthesis/cross-workstream-synthesis.md
Reference:   src/transcript/ (hexagonal architecture pattern)
CLI pattern: src/interface/cli/parser.py (argparse namespace registration)
Wiring:      src/bootstrap.py (composition root pattern)
```

## Element 4: Quality Gate

```
/adversary at C4 criticality
Threshold: >= 0.94 weighted composite (S-014 LLM-as-Judge)
All 10 strategies required: S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014
Gate points: after each batch of parallel agents, before next batch proceeds
Circuit breaker: max 10 iterations per C4 (RT-M-010)
```

## Element 5: Output Paths

```
Production:  src/docs/**/*.py (hexagonal layout)
Templates:   .context/templates/docs/*.jinja2, *.yaml
Scripts:     scripts/check_docs.py
Tests:       tests/unit/docs/, tests/integration/docs/, tests/golden/docs/
Integration: src/interface/cli/parser.py (edit), src/bootstrap.py (edit)
Orch Plan:   projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/ORCHESTRATION_PLAN.md
```

---

## Execution Architecture

```
MAIN CONTEXT (foreground orchestrator)
    |
    |-- Batch 1 (parallel, background):
    |       |-- eng-backend-1: src/docs/ Python code (domain + application + infrastructure)
    |       |-- eng-backend-2: .context/templates/docs/ + scripts/check_docs.py
    |
    |-- [ADVERSARY C4 GATE >= 0.94]
    |
    |-- Batch 2 (background):
    |       |-- eng-backend-3: CLI parser + bootstrap wiring
    |
    |-- [ADVERSARY C4 GATE >= 0.94]
    |
    |-- Batch 3 (parallel, background):
    |       |-- eng-qa: All tests (unit + integration + golden)
    |       |-- eng-architect: Security review (M-1 through M-5 verification)
    |       |-- red-vuln: Attack surface analysis
    |
    |-- [ADVERSARY C4 GATE >= 0.94]
    |
    |-- Final Gate (background):
    |       |-- eng-reviewer: Architecture + security + test compliance
    |
    |-- WORKFLOW COMPLETE
```

## Security Controls (M-1 through M-5)

| ID | Control | Implementation File |
|----|---------|-------------------|
| M-1 | Sanitize YAML fields | `application/services/skill_extractor.py` — validate types, lengths, strip HTML |
| M-2 | Sandboxed Jinja2 | `infrastructure/adapters/jinja2_renderer.py` — `SandboxedEnvironment` + `StrictUndefined` |
| M-3 | Atomic writes | `application/handlers/commands/generate_docs_command_handler.py` — `tempfile` + `os.replace()` |
| M-4 | Pinned Jinja2 | `pyproject.toml` — `jinja2>=3.1,<3.2` |
| M-5 | Schema validation | `application/services/skill_extractor.py` — field constraints before rendering |

# PROJ-0037 Implementation Execution Prompt

> **Purpose:** Copy-paste this prompt into a fresh Claude Code session to execute the doc-module implementation pipeline.
> **Criticality:** C4 (Critical — public CLI API surface, security controls, irreversible architecture)
> **Date:** 2026-03-10
> **Prerequisite:** `JERRY_PROJECT=PROJ-0037-doc-module` must be set.

---

## Prompt

Use /worktracker to create Tasks under ST-002 for each implementation phase:
- TASK: "Implement DocsGenerator handler + SkillExtractor service + infrastructure adapters" (Phase 1)
- TASK: "Wire CLI docs namespace to DocsGenerator via bootstrap.py" (Phase 2)
- TASK: "Implement test suite (unit + integration + golden)" (Phase 3a)
- TASK: "Security control verification M-1 through M-5" (Phase 3b)
- TASK: "Attack surface analysis — YAML injection, Jinja2 trust, path traversal" (Phase 3c)
- TASK: "Final architecture compliance and coverage gate" (Phase 4)

Use /orchestration with orch-planner to sequence the implementation pipeline defined below. Use /eng-team for eng-backend, eng-qa, eng-architect, and eng-reviewer agents. Use /red-team for red-vuln agent. Use /adversary with C4 criticality, all 10 strategies, and >= 0.94 quality threshold at each barrier. Run each agent in the BACKGROUND via the Task tool. The main context is the foreground orchestrator.

Orchestration plan: `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/ORCHESTRATION_PLAN.md`

---

### 1. SKILL ROUTING

| Skill | Agents | Role |
|-------|--------|------|
| `/orchestration` | orch-planner, orch-tracker | Sequence phases, enforce barriers, persist state |
| `/eng-team` | eng-backend | Phase 1: bounded context code. Phase 2: CLI + bootstrap wiring |
| `/eng-team` | eng-qa | Phase 3: 16 tests (10 unit, 4 integration, 2 golden) |
| `/eng-team` | eng-architect | Phase 3: security control verification (M-1 through M-5), hexagonal compliance |
| `/eng-team` | eng-reviewer | Phase 4: final architecture compliance + coverage verification |
| `/red-team` | red-vuln | Phase 3: attack surface analysis |
| `/adversary` | adv-scorer | All barriers: C4 tournament scoring with all 10 strategies |
| `/worktracker` | wt-auditor | Task tracking under ST-002 |

---

### 2. SCOPE — What to Build

Build ONLY the 11 missing artifacts listed below. Do NOT modify any existing files except `src/bootstrap.py` (for composition root wiring).

**Existing artifacts (DO NOT REBUILD):**
- `src/docs/domain/value_objects/skill_data.py` — `SkillData` frozen dataclass (6 fields: name, description, version, agent_count, agents, file_path)
- `src/docs/domain/value_objects/agent_data.py` — `AgentData` frozen dataclass (4 fields: name, description, model, file_path)
- `src/docs/domain/ports/frontmatter_reader.py` — `IFrontmatterReader` Protocol with `read_frontmatter(file_path: str) -> dict[str, Any]`
- `src/docs/domain/ports/template_renderer.py` — `ITemplateRenderer` Protocol with `render_section()` and `inject_between_markers()`
- `src/docs/application/commands/generate_docs_command.py` — `GenerateDocsCommand(readme_path: str, mode: str)`
- `src/docs/application/results/generate_docs_result.py` — `GenerateDocsResult(success, sections, drift_detected, skills_count, agents_count, warnings, error)`
- `src/interface/cli/parser.py` — `_add_docs_namespace()` already registered with `--check`, `--write`, `--readme` flags
- `scripts/check_docs.py` — pre-commit hook script (complete)
- `.context/templates/docs/skills-table.md.jinja2` — uses `truncate_safe()` and `escape_pipe()` macros
- `.context/templates/docs/features-section.md.jinja2` — iterates `features` list with `total_agents` and `total_skills`
- `.context/templates/docs/_macros.jinja2` — `truncate_safe(text, length=60)` and `escape_pipe(text)` macros
- `.context/templates/docs/skill-examples.yaml` — 13 skill-to-example mappings
- `.context/templates/docs/features.yaml` — 9 curated feature entries
- `pyproject.toml` — `jinja2>=3.1,<3.2` dependency already added
- `README.md` — markers `<!-- BEGIN:GENERATED:SKILLS_TABLE -->` / `<!-- END:GENERATED:SKILLS_TABLE -->` and `<!-- BEGIN:GENERATED:FEATURES -->` / `<!-- END:GENERATED:FEATURES -->` already present

**MISSING — Build these 11 artifacts:**

#### Artifact 1: `src/docs/application/handlers/commands/generate_docs_command_handler.py`

Class: `GenerateDocsCommandHandler`

Constructor dependencies (injected via bootstrap):
- `extractor: SkillExtractor` (application service)
- `renderer: ITemplateRenderer` (domain port, satisfied by `Jinja2Renderer`)
- `reader: IFrontmatterReader` (domain port, satisfied by `AstFrontmatterReader`)

Method: `handle(command: GenerateDocsCommand) -> GenerateDocsResult`

Behavior per spec:
1. Call `extractor.extract_all(skills_dir="skills/")` to get `list[SkillData]`
2. Load `skill-examples.yaml` and `features.yaml` from `.context/templates/docs/`
3. Build template context: `{"skills": [...with .example field added...], "total_agents": N, "total_skills": N, "features": [...]}`
4. Call `renderer.render_section("skills-table.md.jinja2", context)` for SKILLS_TABLE section
5. Call `renderer.render_section("features-section.md.jinja2", context)` for FEATURES section
6. If `command.mode == "stdout"`: return result with sections dict
7. If `command.mode == "check"`: read `command.readme_path`, compare each section between markers, set `drift_detected`
8. If `command.mode == "write"`: read current README, inject sections between markers, atomic write via `tempfile.NamedTemporaryFile` + `os.replace()` (M-3)
9. Return `GenerateDocsResult` with `sections`, `skills_count`, `agents_count`, `warnings`, `drift_detected`

Security controls:
- M-3: Atomic write pattern using `tempfile.NamedTemporaryFile(mode='w', dir=dir_name, delete=False, suffix='.tmp')` then `os.replace(temp_path, target_path)`
- M-5: All field values validated before rendering (delegated to `SkillExtractor`)

#### Artifact 2: `src/docs/application/services/skill_extractor.py`

Class: `SkillExtractor`

Constructor dependency:
- `reader: IFrontmatterReader` (domain port)

Method: `extract_all(skills_dir: str) -> list[SkillData]`

Behavior per spec:
1. Glob `{skills_dir}/*/SKILL.md` to find all skill files
2. For each SKILL.md: call `reader.read_frontmatter(path)` to get raw dict
3. **M-1 Sanitization**: validate `name` against `^[a-zA-Z][a-zA-Z0-9-]*$` (max 100 chars); validate `version` against `^\d+\.\d+\.\d+$`; truncate `description` to 1024 chars; strip HTML tags from `description` using `re.sub(r'<[^>]+>', '', text)`
4. **M-5 Schema validation**: if `name` is missing, log warning with file path, skip this skill (exit code 2 scenario); if `description` is missing, use `"(no description)"`
5. Glob `{skill_dir}/agents/*.md` excluding files matching `*TEMPLATE*` or `*EXTENSION*` (case-insensitive glob or filter)
6. For each agent file: call `reader.read_frontmatter(path)`, validate `name` against `^[a-z][a-z0-9-]*$`, build `AgentData`
7. Build `SkillData` with `agent_count=len(agents)`
8. Sort skills alphabetically by `name`
9. Return `list[SkillData]`

Security controls:
- M-1: All fields sanitized (types, lengths, HTML stripped)
- M-5: Schema validation on every field before constructing value objects

#### Artifact 3: `src/docs/infrastructure/adapters/jinja2_renderer.py`

Class: `Jinja2Renderer` (implements `ITemplateRenderer`)

Constructor:
- `template_dir: str` (path to `.context/templates/docs/`)

Implementation:
- Uses `jinja2.sandbox.SandboxedEnvironment` (M-2)
- Uses `jinja2.StrictUndefined` (M-2)
- Uses `jinja2.FileSystemLoader(template_dir)`
- `autoescape=False` (output is markdown, not HTML)

Methods:
- `render_section(template_name: str, context: dict[str, Any]) -> str`: load template by name, render with context, return string
- `inject_between_markers(readme_content: str, section_name: str, generated_content: str) -> str`: find `<!-- BEGIN:GENERATED:{section_name} -->` and `<!-- END:GENERATED:{section_name} -->`, replace content between them, raise `ValueError` if markers not found

Security controls:
- M-2: `SandboxedEnvironment` + `StrictUndefined` prevents template injection and undefined variable leakage

#### Artifact 4: `src/docs/infrastructure/adapters/ast_frontmatter_reader.py`

Class: `AstFrontmatterReader` (implements `IFrontmatterReader`)

Implementation:
- Delegates to `jerry ast frontmatter {file_path}` via `subprocess.run(["uv", "run", "jerry", "ast", "frontmatter", file_path], capture_output=True, text=True)` (H-05, H-33)
- Parses JSON output from stdout
- Returns `dict[str, Any]`
- Raises `FileNotFoundError` if file does not exist, `ValueError` if frontmatter is malformed, `RuntimeError` if subprocess fails

H-33 compliance: Uses `jerry ast frontmatter` (AST-based), never regex.

#### Artifact 5: `tests/unit/docs/test_extractor.py`

5 unit tests (mock `IFrontmatterReader`):
- `test_extract_skill_frontmatter` — valid SKILL.md returns correct `SkillData`
- `test_extract_agent_frontmatter` — valid agent .md returns correct `AgentData` within `SkillData.agents`
- `test_exclude_template_files` — files matching `*TEMPLATE*` and `*EXTENSION*` are excluded from `agent_count`
- `test_validation_rejects_missing_name` — SKILL.md without `name` field: skill is skipped, warning logged
- `test_validation_strips_html` — `description` containing `<script>alert('xss')</script>` has HTML tags stripped

#### Artifact 6: `tests/unit/docs/test_renderer.py`

4 unit tests:
- `test_render_skills_table` — `Jinja2Renderer.render_section("skills-table.md.jinja2", context)` produces correct markdown table with `| Skill | Purpose | Example |` header
- `test_render_features_section` — `Jinja2Renderer.render_section("features-section.md.jinja2", context)` produces correct bullet list with dynamic agent/skill counts
- `test_inject_between_markers` — content between `<!-- BEGIN:GENERATED:SKILLS_TABLE -->` and `<!-- END:GENERATED:SKILLS_TABLE -->` is replaced; content outside markers is preserved verbatim
- `test_missing_markers_error` — `inject_between_markers()` raises `ValueError` when markers are not found in readme_content

#### Artifact 7: `tests/unit/docs/test_generator.py`

1 unit test:
- `test_atomic_write` — `GenerateDocsCommandHandler.handle()` in `"write"` mode uses `tempfile.NamedTemporaryFile` + `os.replace()` pattern; verify that if write is interrupted, the original file is not corrupted (use `tmp_path` fixture, mock a failure mid-write, assert original file is intact)

#### Artifact 8: `tests/integration/docs/test_docs_generate.py`

4 integration tests using real `skills/` directory fixtures:
- `test_end_to_end_generate` — full pipeline: glob real fixture skills -> extract -> render -> compare against expected output string
- `test_check_mode_detects_drift` — `--check` mode returns `drift_detected=True` when README content differs from generated output
- `test_check_mode_passes_when_current` — `--check` mode returns `drift_detected=False` when README content matches generated output
- `test_write_mode_updates_readme` — `--write` mode updates README.md, then subsequent `--check` returns `drift_detected=False`

Use `tmp_path` fixtures with minimal skill/agent directory structures (2-3 skills, 1-2 agents each).

#### Artifact 9: `tests/golden/docs/test_golden.py`

2 golden file tests:
- `test_golden_skills_table` — render skills table from real `skills/` directory, compare against `tests/golden/docs/expected-skills-table.md`
- `test_golden_features_section` — render features section from real `skills/` directory, compare against `tests/golden/docs/expected-features.md`

Include `--update-golden` pytest flag support: when passed, overwrite expected files instead of comparing.

#### Artifact 10: `tests/golden/docs/expected-skills-table.md`

Golden file containing the expected skills table output generated from the current 13 skills in `skills/`. This is the reference output for `test_golden_skills_table`.

#### Artifact 11: `tests/golden/docs/expected-features.md`

Golden file containing the expected features section output generated from `features.yaml` and the current 58 agents across 13 skills. This is the reference output for `test_golden_features_section`.

---

### 3. DATA SOURCES — Input Artifacts

| Artifact | Path (relative to `projects/PROJ-0037-doc-module/`) | Use |
|----------|------------------------------------------------------|-----|
| B4 Spec | `specifications/doc-module-spec.md` | SSOT for all implementation decisions — class responsibilities, extraction pipeline, template structure, error handling, exit codes, test plan |
| Threat Model | `security/threat-model-doc-module.md` | M-1 through M-5 security controls, trust boundaries, attack surface |
| ADR | `decisions/ADR-PROJ0037-001-doc-module-design.md` | Architecture decision rationale, compliance checklist |
| Cross-Workstream Synthesis | `orchestration/doc-module-20260308-001/synthesis/cross-workstream-synthesis.md` | Reconciliation items, description truncation decisions, static data seeding |
| Orchestration Plan | `orchestration/impl-20260310-001/ORCHESTRATION_PLAN.md` | Phase definitions, barrier conditions, agent assignments, recovery strategies |
| Existing Domain Layer | `src/docs/domain/` (ports + value_objects) | Port interfaces to implement, value object shapes to construct |
| Existing Application Layer | `src/docs/application/` (commands + results) | Command/result types the handler must accept/return |
| Existing Templates | `.context/templates/docs/` (5 files) | Template names, macro signatures, YAML data file schemas |
| Existing CLI Parser | `src/interface/cli/parser.py` lines 929-977 | `_add_docs_namespace()` flag definitions (`--check`, `--write`, `--readme`) |
| Bootstrap Pattern | `src/bootstrap.py` | Factory function pattern for composition root wiring |
| Transcript Handler Pattern | `src/transcript/application/handlers/commands/parse_transcript_command_handler.py` | Reference pattern for command handler constructor injection and `handle()` method |

---

### 4. QUALITY GATE

Use /adversary with C4 criticality at every barrier. All 10 strategies. Quality threshold >= 0.94.

| Barrier | Strategies | Scoring Dimensions | Max Iterations |
|---------|------------|-------------------|----------------|
| Barrier 1 (Foundation) | S-014, S-003, S-002, S-010, S-013 | Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability | 10 |
| Barrier 2 (Integration) | S-014, S-003, S-002, S-010, S-004 | Same 6 dimensions | 10 |
| Barrier 3 (Verification) | S-014, S-003, S-002, S-010, S-012, S-011, S-001 | Same 6 dimensions | 10 |
| Barrier 4 (Final Gate) | All 10 (tournament mode) | Same 6 dimensions | 10 |

Score bands: PASS >= 0.94 (advance). REVISE 0.88-0.93 (targeted revision, re-score). REJECTED < 0.88 (significant rework; escalate if 3 consecutive REJECTED).

---

### 5. OUTPUT PATHS

All paths relative to the repository root.

| Artifact | Path |
|----------|------|
| DocsGenerator handler | `src/docs/application/handlers/commands/generate_docs_command_handler.py` |
| SkillExtractor service | `src/docs/application/services/skill_extractor.py` |
| Jinja2Renderer adapter | `src/docs/infrastructure/adapters/jinja2_renderer.py` |
| AstFrontmatterReader adapter | `src/docs/infrastructure/adapters/ast_frontmatter_reader.py` |
| Unit tests: extractor | `tests/unit/docs/test_extractor.py` |
| Unit tests: renderer | `tests/unit/docs/test_renderer.py` |
| Unit tests: generator | `tests/unit/docs/test_generator.py` |
| Integration tests | `tests/integration/docs/test_docs_generate.py` |
| Golden file tests | `tests/golden/docs/test_golden.py` |
| Golden file: skills table | `tests/golden/docs/expected-skills-table.md` |
| Golden file: features | `tests/golden/docs/expected-features.md` |
| Bootstrap wiring | `src/bootstrap.py` (modify existing — add `create_docs_generator()` factory) |
| `__init__.py` files | `src/docs/application/handlers/__init__.py`, `src/docs/application/handlers/commands/__init__.py`, `src/docs/application/services/__init__.py`, `src/docs/infrastructure/__init__.py`, `src/docs/infrastructure/adapters/__init__.py`, `tests/unit/docs/__init__.py`, `tests/integration/docs/__init__.py`, `tests/golden/docs/__init__.py` |
| Orchestration state | `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/` (phase output dirs) |
| Quality scores | `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/{phase-N}/quality-scores.yaml` |

---

## EXECUTION ARCHITECTURE

### Phase 1 — FOUNDATION (Fan-Out, Parallel Background)

**Trigger:** Workflow start; design artifacts present.

Launch 2 eng-backend agents in BACKGROUND via Task tool:

**eng-backend-1 (bounded context code):**
- Build `src/docs/application/handlers/commands/generate_docs_command_handler.py` — class `GenerateDocsCommandHandler` with constructor injection of `SkillExtractor`, `ITemplateRenderer`, `IFrontmatterReader`. Method `handle(command: GenerateDocsCommand) -> GenerateDocsResult`. Implements M-3 atomic write pattern.
- Build `src/docs/application/services/skill_extractor.py` — class `SkillExtractor` with constructor injection of `IFrontmatterReader`. Method `extract_all(skills_dir: str) -> list[SkillData]`. Implements M-1 sanitization + M-5 schema validation.
- Build `src/docs/infrastructure/adapters/jinja2_renderer.py` — class `Jinja2Renderer` implementing `ITemplateRenderer`. Uses `SandboxedEnvironment` + `StrictUndefined` (M-2). Methods: `render_section()`, `inject_between_markers()`.
- Build `src/docs/infrastructure/adapters/ast_frontmatter_reader.py` — class `AstFrontmatterReader` implementing `IFrontmatterReader`. Delegates to `uv run jerry ast frontmatter {file_path}` via subprocess (H-05, H-33).
- Create all required `__init__.py` files for new packages.
- Follow hexagonal layer isolation (H-07): domain ports have no infrastructure imports; infrastructure adapters import domain ports.
- Follow one-class-per-file (H-10). Type hints + docstrings on all public functions (H-11).
- Reference: `src/transcript/application/handlers/commands/parse_transcript_command_handler.py` for handler pattern.
- Reference: existing port interfaces in `src/docs/domain/ports/` for exact method signatures.

**eng-backend-2:** SKIPPED — templates and pre-commit hook already exist. This agent's deliverables were completed in the design phase.

Output: `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-1/`

---

### BARRIER 1 — Foundation Gate

**Condition:** eng-backend-1 complete.

**Quality gate:** /adversary C4, strategies S-014 + S-003 + S-002 + S-010 + S-013, >= 0.94.

**Verification checklist:**
- [ ] `GenerateDocsCommandHandler` constructor accepts `SkillExtractor`, `ITemplateRenderer`, `IFrontmatterReader`
- [ ] `SkillExtractor.extract_all()` validates name regex `^[a-zA-Z][a-zA-Z0-9-]*$`, strips HTML from description, enforces 1024-char max
- [ ] `Jinja2Renderer` uses `SandboxedEnvironment` + `StrictUndefined`
- [ ] `AstFrontmatterReader` calls `uv run jerry ast frontmatter` (not regex, not raw YAML)
- [ ] Atomic write uses `tempfile.NamedTemporaryFile` + `os.replace()`
- [ ] No domain layer file imports from infrastructure
- [ ] One class per file throughout `src/docs/`

Creator: eng-backend-1. Critic: adv-scorer. Revision: eng-backend-1. Max iterations: 10.

---

### Phase 2 — INTEGRATION (Sequential Background)

**Trigger:** Barrier 1 PASS.

Launch 1 eng-backend agent in BACKGROUND via Task tool:

**eng-backend-3 (CLI + bootstrap wiring):**
- Modify `src/bootstrap.py`: add `create_docs_generator()` factory function that wires `AstFrontmatterReader` -> `SkillExtractor` -> `Jinja2Renderer` -> `GenerateDocsCommandHandler`. Follow existing factory patterns (e.g., `create_vtt_parser()`, `create_transcript_chunker()`).
- Verify that `src/interface/cli/parser.py` `_add_docs_namespace()` already registers `--check`, `--write`, `--readme` flags (it does — do NOT modify parser.py).
- Ensure the CLI dispatch in the main entry point calls `create_docs_generator()` and routes `docs generate` commands to `GenerateDocsCommandHandler.handle()`.
- Test invocation: `uv run jerry docs generate` should print generated sections to stdout without error.

Output: `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-2/`

---

### BARRIER 2 — Integration Gate

**Condition:** eng-backend-3 complete.

**Quality gate:** /adversary C4, strategies S-014 + S-003 + S-002 + S-010 + S-004, >= 0.94.

**Verification checklist:**
- [ ] `uv run jerry docs generate` runs without error and prints generated skills table + features section to stdout
- [ ] `uv run jerry docs generate --check` exits 0 when README is current, exits 1 when drift detected
- [ ] `uv run jerry docs generate --write` updates README.md between marker comments
- [ ] `create_docs_generator()` in bootstrap.py follows existing factory function patterns
- [ ] No circular imports between `src/docs/` and `src/bootstrap.py`

Creator: eng-backend-3. Critic: adv-scorer. Revision: eng-backend-3. Max iterations: 10.

---

### Phase 3 — VERIFICATION (Fan-Out, Parallel Background)

**Trigger:** Barrier 2 PASS.

Launch 3 agents in BACKGROUND via Task tool:

**eng-qa (test suite):**
- Build `tests/unit/docs/test_extractor.py` — 5 tests: `test_extract_skill_frontmatter`, `test_extract_agent_frontmatter`, `test_exclude_template_files`, `test_validation_rejects_missing_name`, `test_validation_strips_html`. Mock `IFrontmatterReader` using `unittest.mock.Mock` or pytest monkeypatch.
- Build `tests/unit/docs/test_renderer.py` — 4 tests: `test_render_skills_table`, `test_render_features_section`, `test_inject_between_markers`, `test_missing_markers_error`. Use real `Jinja2Renderer` with the actual templates in `.context/templates/docs/`.
- Build `tests/unit/docs/test_generator.py` — 1 test: `test_atomic_write`. Use `tmp_path` fixture. Verify `os.replace()` is called (mock or inspect temp file behavior).
- Build `tests/integration/docs/test_docs_generate.py` — 4 tests: `test_end_to_end_generate`, `test_check_mode_detects_drift`, `test_check_mode_passes_when_current`, `test_write_mode_updates_readme`. Create minimal fixture directories in `tmp_path` with 2-3 mock skills and agents.
- Build `tests/golden/docs/test_golden.py` — 2 tests: `test_golden_skills_table`, `test_golden_features_section`. Add `--update-golden` flag support via `pytest.ini` or conftest.
- Generate `tests/golden/docs/expected-skills-table.md` and `tests/golden/docs/expected-features.md` by running the actual generation pipeline against the real `skills/` directory.
- Create all required `__init__.py` files for test packages.
- Run `uv run pytest tests/unit/docs/ tests/integration/docs/ tests/golden/docs/ -v --tb=short` and fix any failures.
- Run `uv run pytest tests/unit/docs/ --cov=src/docs --cov-report=term-missing` and verify >= 90% line coverage (H-20).

**eng-architect (security review):**
- Verify M-1: `SkillExtractor` validates field types, enforces max lengths, strips HTML tags. Check regex patterns match spec.
- Verify M-2: `Jinja2Renderer` uses `SandboxedEnvironment` with `StrictUndefined`. Confirm `autoescape=False` is safe (output is markdown, not HTML).
- Verify M-3: Atomic write uses `tempfile.NamedTemporaryFile(dir=same_dir)` + `os.replace()`. Confirm `delete=False` is set. Confirm temp file is cleaned up on error.
- Verify M-4: `pyproject.toml` pins `jinja2>=3.1,<3.2` (already done — confirm still present).
- Verify M-5: Schema validation runs before any data reaches the renderer.
- Verify H-07: No domain file in `src/docs/domain/` imports from `src/docs/infrastructure/` or `src/docs/application/`.
- Verify H-10: Every `.py` file in `src/docs/` contains exactly one class (value objects, ports, handler, service, adapters).
- Verify H-11: All public functions have type hints on parameters and return types, plus docstrings.
- Output: security review report at `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-3/security-review.md`

**red-vuln (attack surface analysis):**
- Analyze YAML injection vector: Can a malicious `description` field in SKILL.md inject markdown/HTML that renders dangerously on GitHub? Test: craft a SKILL.md with `description: "Click [here](javascript:alert(1))"` and verify the sanitizer strips or escapes it.
- Analyze Jinja2 trust boundary: Can a crafted YAML field value escape the SandboxedEnvironment? Test: `description: "{{ ''.__class__.__mro__[1].__subclasses__() }}"` — confirm SandboxedEnvironment blocks this.
- Analyze path traversal in `--readme` flag: Can `uv run jerry docs generate --write --readme ../../etc/passwd` write to arbitrary paths? Verify path validation or sandboxing.
- Analyze subprocess injection in `AstFrontmatterReader`: Can a crafted `file_path` argument inject shell commands? Verify that `subprocess.run()` uses list-form arguments (not shell=True).
- Output: attack surface report at `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-3/attack-surface-report.md`

Output: `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-3/`

---

### BARRIER 3 — Verification Gate

**Condition:** eng-qa AND eng-architect AND red-vuln complete.

**Quality gate:** /adversary C4, strategies S-014 + S-003 + S-002 + S-010 + S-012 + S-011 + S-001, >= 0.94.

**Verification checklist:**
- [ ] `uv run pytest tests/unit/docs/ tests/integration/docs/ tests/golden/docs/ -v` — all 16 tests pass
- [ ] `uv run pytest tests/unit/docs/ --cov=src/docs --cov-report=term-missing` — >= 90% line coverage
- [ ] Security review confirms M-1 through M-5 implemented and verified
- [ ] Attack surface analysis found no unmitigated CRITICAL vulnerabilities
- [ ] If red-vuln found unmitigated CRITICAL: BLOCK barrier until eng-architect documents remediation

Creator: eng-qa / eng-architect / red-vuln. Critic: adv-scorer. Revision: eng-qa / eng-architect. Max iterations: 10.

---

### Phase 4 — FINAL GATE (Sequential Background)

**Trigger:** Barrier 3 PASS.

Launch 1 eng-reviewer agent in BACKGROUND via Task tool:

**eng-reviewer (architecture compliance):**
- Verify hexagonal layer isolation (H-07): `grep` for cross-layer imports in `src/docs/`
- Verify one-class-per-file (H-10): count classes per file in `src/docs/`
- Verify type hints + docstrings (H-11): inspect all public function signatures
- Verify M-1 through M-5 controls are present in final code (not just reviewed — actually present)
- Run `uv run pytest tests/ -v --tb=short` — full test suite passes
- Run `uv run pytest tests/unit/docs/ --cov=src/docs --cov-report=term-missing` — >= 90% line coverage
- Run `uv run jerry docs generate --check` against current README.md — exits 0
- Output: final compliance report at `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-4/final-compliance-report.md`

Output: `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-4/`

---

### BARRIER 4 — Final Gate (Tournament Mode)

**Condition:** eng-reviewer complete.

**Quality gate:** /adversary C4 TOURNAMENT MODE, ALL 10 strategies (S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001), >= 0.94.

**Tournament verification:**
- S-014 LLM-as-Judge: 6-dimension scoring (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability)
- S-003 Steelman: Strengthen the implementation before critiquing
- S-013 Inversion: "What would make this module fail in production?"
- S-007 Constitutional AI: H-05, H-07, H-10, H-11, H-33, P-003 compliance
- S-002 Devil's Advocate: Challenge design assumptions
- S-004 Pre-Mortem: "The module shipped and broke CI for every team. What happened?"
- S-010 Self-Refine: Final self-review pass
- S-012 FMEA: Failure mode analysis on security controls
- S-011 Chain-of-Verification: Verify every claim in the compliance report
- S-001 Red Team: Attack the implementation from red-vuln findings

Creator: eng-reviewer. Critic: adv-scorer (all 10 strategies). Revision: eng-reviewer. Max iterations: 10.

---

### POST-BARRIER 4 — Deployment HELD

After Barrier 4 PASS:
1. Update worktracker tasks under ST-002 to `completed` status
2. Present final quality scores and tournament results to user
3. DO NOT commit or push — await human review and merge approval

---

## RECOVERY STRATEGIES

| Failure Mode | Recovery |
|-------------|----------|
| Phase 1 agent partially fails | Halt; do not advance to Barrier 1; present partial result with specific blocker |
| Barrier quality score < 0.94 | Revision cycle (max 10 iterations per C4); after 10 with no convergence, escalate to user |
| Phase 3 red-vuln finds unmitigated CRITICAL | Block Barrier 3 PASS; eng-architect must document remediation |
| `uv run pytest` fails | Do NOT advance past Barrier 3 until all tests pass |
| Circuit breaker fires (> 3 hops) | Log routing history; halt; present best result; ask user per H-31 |

---

## EXECUTION CONSTRAINTS

| Constraint | Value |
|-----------|-------|
| Python execution | `uv run` only (H-05). NEVER `python`, `pip`, `pip3`. |
| Agent nesting | Max 1 level — orchestrator to worker only (P-003 / H-01) |
| Layer isolation | Domain imports only domain; application imports domain; infrastructure imports domain (H-07) |
| Class-per-file | One class per `.py` file in `src/docs/` (H-10) |
| Type safety | Type hints on all public function parameters and return types (H-11) |
| Frontmatter parsing | `jerry ast frontmatter` only — never regex (H-33) |
| Test coverage | >= 90% line coverage on `src/docs/` (H-20) |
| Quality threshold | >= 0.94 at every barrier (C4) |

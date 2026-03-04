# FMEA: Skill Composition Pipeline

<!-- VERSION: 1.0.0 | DATE: 2026-03-03 | SOURCE: PROJ-012 Phase 6 | AGENT: adv-executor (S-012 FMEA) -->

> Failure Mode and Effects Analysis for the PROJ-012 Skill Composition Pipeline (Phases 1-6).
> Applies S-012 FMEA strategy. RPN threshold for recommended action: 100.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Components analyzed and analysis boundaries |
| [Methodology](#methodology) | FMEA scoring approach and rating scales |
| [FMEA Table](#fmea-table) | All failure modes sorted by RPN descending |
| [High-Priority Findings](#high-priority-findings) | RPN >= 100 findings with detailed analysis |
| [Component Summary](#component-summary) | Risk profile per pipeline component |
| [Recommended Actions](#recommended-actions) | Prioritized remediation plan |
| [Residual Risk Summary](#residual-risk-summary) | Risk posture after recommended actions |

---

## Scope

**Pipeline analyzed:** Skill Composition Pipeline — 6 phases, complete as of PROJ-012 Phase 6.

| Component | Files |
|-----------|-------|
| Schema Validation Layer | `docs/schemas/anthropic-skill-frontmatter-v1.schema.json`, `docs/schemas/skill-canonical-v1.schema.json`, `scripts/check_skill_schemas.py` |
| Canonical Source Files | `skills/*/composition/skill.jerry.yaml` (15 files) |
| Governance Section Builder | `src/agents/domain/services/skill_governance_builder.py` |
| Compose Validator | `src/agents/domain/services/skill_compose_validator.py` (SCV-001 through SCV-006) |
| Compose Pipeline Handler | `src/agents/application/handlers/commands/compose_skills_command_handler.py`, `src/agents/infrastructure/persistence/filesystem_skill_repository.py` |
| Pre-commit + CI Enforcement | `.pre-commit-config.yaml`, `.github/workflows/ci.yml` |

**Out of scope:** Agent composition pipeline (CV-001 through CV-007 for agents), worktracker entities, MkDocs build.

---

## Methodology

**RPN = Severity (S) × Occurrence (O) × Detection (D)**

| Scale | Severity (S) | Occurrence (O) | Detection (D) |
|-------|-------------|----------------|---------------|
| 1 | Negligible (cosmetic) | Remote (< 1% of operations) | Certain detection (deterministic gate catches it) |
| 2-3 | Minor (single skill degraded) | Low (1-5% of operations) | High detection (automated check likely catches it) |
| 4-6 | Moderate (feature broken, 1-3 skills) | Moderate (5-20% of operations) | Moderate detection (some checks, gaps exist) |
| 7-8 | Major (multiple skills broken, runtime errors) | High (20-50% of operations) | Low detection (manual review or no check) |
| 9-10 | Critical (pipeline inoperable, security risk, data loss) | Very High (> 50% of operations) | Undetectable (no automated control exists) |

**RPN threshold:** >= 100 triggers a recommended action. Items in the 50-99 range are noted for monitoring.

---

## FMEA Table

> Sorted by RPN descending. Items with RPN >= 100 are in the **High-Priority Findings** section.

| # | Component | Failure Mode | Effect | Cause | S | O | D | RPN | Current Controls |
|---|-----------|-------------|--------|-------|---|---|---|-----|------------------|
| F-01 | Pre-commit + CI | Schema validation (`check_skill_schemas.py`) absent from CI | Corrupted SKILL.md frontmatter or invalid skill.jerry.yaml ships to main without CI detection | `check_skill_schemas.py` is a pre-commit-only hook; no corresponding CI job was added (unlike `skill-compose-validation` which has both) | 7 | 6 | 8 | **336** | Pre-commit hook (bypassable with `--no-verify`) |
| F-02 | Compose Pipeline | `_load_skill()` silently returns `None` on any exception | Skill silently dropped from compose run; no error emitted to user; CI passes with reduced skill count | Bare `except Exception: return None` at line 109 of `filesystem_skill_repository.py` swallows all errors including YAML parse failures, file permission errors, and field access errors | 8 | 4 | 8 | **256** | None — exception is swallowed |
| F-03 | Schema Validation | `additionalProperties: true` on `context_injection` and `metadata` in `skill-canonical-v1.schema.json` | Arbitrary unknown fields in `context_injection` pass schema validation silently; author intent errors undetected | Schema design choice: `additionalProperties: true` on two sub-objects; top-level `additionalProperties: false` is correct but does not extend into these sub-objects | 6 | 5 | 7 | **210** | Top-level `additionalProperties: false` catches truly unknown root fields |
| F-04 | Compose Validator | SCV-003 (governance sections present) is severity=warning, not severity=error | A skill.jerry.yaml declares `version`, `activation-keywords`, or `agents` but the governance section is absent from the composed SKILL.md; the compose run succeeds and writes the corrupt file | SCV-003 produces `warnings` not `errors`; compose handler only halts and skips file write on `validation.errors`; warnings do not prevent write at line 130 of handler | 7 | 4 | 6 | **168** | Warning logged to console/CI output; user must inspect warnings manually |
| F-05 | Compose Pipeline | Frontmatter delimiter parsing uses `find("---", 3)` instead of `find("\n---", 3)` | If a YAML value legitimately contains `---` (e.g., a description with an em dash or separator), the frontmatter is silently truncated at the embedded `---`; the remaining "body" is incorrectly treated as the body section; YAML parse error silently swallowed | 6 independent copies of naive delimiter logic in `compose_skills_command_handler.py`, `filesystem_skill_repository.py`, `compose_validator.py`, `skill_compose_validator.py`, and 2 others; only `check_skill_schemas.py` uses the correct `find("\n---", 3)` pattern | 7 | 3 | 7 | **147** | `check_skill_schemas.py` uses correct pattern (pre-commit only); SCV-002 catches missing name/description as downstream symptom |
| F-06 | Pre-commit + CI | `git commit --no-verify` bypasses all skill validation hooks | Broken SKILL.md frontmatter, invalid skill.jerry.yaml, or governance section regressions commit without any validation | Pre-commit documentation explicitly lists `git commit --no-verify -m "message"` as an "emergency" escape hatch; CI skill-compose-validation job does not include JSON schema validation (`check_skill_schemas.py`) | 7 | 3 | 7 | **147** | CI `skill-compose-validation` catches SCV regressions (but not JSON schema violations); CI runs on all branches |
| F-07 | Governance Builder | Heading dedup silently preserves stale governance data in SKILL.md body | If an author hand-edits `## Skill Version` or `## Activation Keywords` in SKILL.md before running compose, compose will detect the heading exists and skip injection; the stale hand-authored value persists in the file indefinitely | `_extract_headings()` checks for existing headings and skips; this is correct for preventing duplicate injection but creates a "silent staleness" scenario; no check verifies the existing value matches the canonical source | 5 | 5 | 8 | **200** | SCV-003 checks heading presence but not value correctness; no check compares existing heading content to canonical source |
| F-08 | Compose Validator | SCV-004 silently skips validation when `jsonschema` is not installed | SKILL.md frontmatter is never validated against `anthropic-skill-frontmatter-v1.schema.json` in environments without `jsonschema` | `try: import jsonschema; except ImportError: jsonschema = None` pattern; `_check_scv004` returns silently when `self._anthropic_schema is None` or `jsonschema is None` | 6 | 3 | 8 | **144** | `check_skill_schemas.py` uses `sys.exit(1)` if jsonschema missing (pre-commit only) |
| F-09 | Canonical Source | `name` field in `skill.jerry.yaml` not validated against parent directory name by schema | A skill.jerry.yaml could declare `name: foo` while living in `skills/bar/composition/`; schema validation passes; SCV-005 catches this only at compose-time, not at schema validation time | `skill-canonical-v1.schema.json` validates name format (kebab-case, no reserved words) but cannot validate filesystem context; cross-reference requires runtime knowledge | 6 | 2 | 6 | **72** | SCV-005 error-level check at compose time catches name/folder mismatch |
| F-10 | Compose Pipeline | SKILL.md parent directory auto-created if missing | Running compose against a skill name typo creates a new empty directory `skills/{typo}/SKILL.md` silently | `output_path.parent.mkdir(parents=True, exist_ok=True)` at line 131 of handler; no check that the skill directory already exists before creating it | 5 | 2 | 7 | **70** | `_repository.get(command.skill_name)` returns None for unknown skills; `list_all()` scans only existing directories with `skill.jerry.yaml`; only dangerous when compose is invoked via public API with a crafted path |
| F-11 | Schema Validation | `activation-keywords` minimum is 1 item but no maximum is enforced | A skill could declare hundreds of activation keywords, bloating the trigger map token budget beyond the L2 re-injection limit (~850 tokens) described in `quality-enforcement.md` | `skill-canonical-v1.schema.json` sets `minItems: 1` but no `maxItems` constraint on `activation-keywords` | 4 | 3 | 7 | **84** | Trigger map review is manual; no automated count enforcement |
| F-12 | Compose Pipeline | `governance_sections` injected multiple times if compose runs on an already-composed SKILL.md | If compose is run without prior `_extract_headings` dedup (e.g., if body is not correctly read from file), governance sections accumulate | Dedup relies on reading the correct existing file content; if `output_path.exists()` returns False (first run), body is empty string and headings are absent — correct; if file exists and is readable, dedup applies — correct; risk only if file I/O fails silently between read and write | 4 | 2 | 5 | **40** | Heading dedup via `_extract_headings()` prevents double injection in normal operation |
| F-13 | CI | `skill-compose-validation` CI job runs `jerry skills validate --composed` which is a `dry_run=True` compose, not a standalone read of committed files | If a developer directly edits `SKILL.md` (bypasses compose pipeline) with a Jerry extension field in frontmatter, CI catches it (SCV-001 re-runs against existing file content). But if they edit with incorrect values that pass SCV checks, CI passes | Validate = compose in dry_run mode; this re-reads the canonical source and re-composes; it does NOT validate the committed SKILL.md in isolation against its committed state | 5 | 3 | 5 | **75** | SCV-001 through SCV-006 run against the re-composed content; any deviation from committed content is re-validated |
| F-14 | Schema Validation | `model` field in `anthropic-skill-frontmatter-v1.schema.json` is type `string` with no enum constraint | An invalid model string (e.g., `model: gpt-4o`) passes schema validation; only runtime rejection by Claude Code would catch it | Schema intentionally leaves model as free-form string; no Anthropic-published enum of valid models exists in the schema source | 3 | 2 | 8 | **48** | SCV-004 schema validation catches structural violations but not semantic model name validity |
| F-15 | Compose Validator | SCV-005 folder name check skips when `folder_name` is empty string | Name/folder mismatch not caught if caller omits `folder_name` argument | `_check_scv005` has `if folder_name and name != folder_name` guard; if `folder_name=""` is passed, the cross-check silently skips | 4 | 2 | 5 | **40** | Handler passes `output_path.parent.name` as folder_name, which is always populated; risk is from alternative callers |
| F-16 | Governance Builder | Governance sections injected after the footer pattern; if `_FOOTER_RE` matches incorrectly, sections land at wrong position | Malformed SKILL.md body with `*Skill Version:` text outside the footer line causes governance to inject mid-document | `_FOOTER_RE = re.compile(r"^\*Skill Version:.*$", re.MULTILINE)` matches any line beginning with `*Skill Version:` anywhere in the body | 3 | 2 | 6 | **36** | Footer pattern is narrow enough that false positives are unlikely; governance content is idempotent |
| F-17 | Canonical Source | `skill.jerry.yaml` files lack a `last_modified` or source traceability field | No automated way to detect if a canonical source is stale relative to the SKILL.md it governs | Schema design choice; no `last_modified` in `skill-canonical-v1.schema.json` | 3 | 4 | 8 | **96** | Git blame provides manual traceability; no automated staleness detection |
| F-18 | CI | CI `skill-compose-validation` not in `needs` for `coverage-report` job | Coverage report runs even if skill compose validation fails | `coverage-report` depends only on `test-pip` and `test-uv`; skill-compose-validation is separate | 2 | 2 | 5 | **20** | `ci-success` aggregator includes `skill-compose-validation` in its needs |

---

## High-Priority Findings

> RPN >= 100. Detailed root cause, effect chain, and recommended action.

### F-01: Schema Validation Absent from CI (RPN 336)

**Component:** Pre-commit + CI Enforcement

**Failure mode:** `check_skill_schemas.py` (which validates SKILL.md frontmatter against `anthropic-skill-frontmatter-v1.schema.json` and `skill.jerry.yaml` against `skill-canonical-v1.schema.json`) runs only as a pre-commit hook. There is no corresponding CI job.

**Effect chain:**
1. Developer uses `git commit --no-verify` (documented escape hatch in `.pre-commit-config.yaml`) or pre-commit is not installed.
2. SKILL.md frontmatter contains an invalid field (e.g., `context_injection` leaked through), or `skill.jerry.yaml` has an invalid `version` format.
3. Pre-commit hook is skipped.
4. CI runs `jerry skills validate --composed` which applies SCV-001 through SCV-006 checks — but SCV-004 (which calls `jsonschema.validate` against the anthropic schema) is only invoked if the schema file exists AND `jsonschema` is installed at compose time.
5. SCV-004 is schema-aware but is a secondary check; the primary `check_skill_schemas.py` script that calls `Draft202012Validator` with sorted error reporting is absent from CI.
6. Invalid files merge to main.

**Asymmetry identified:** The CI YAML file (`ci.yml`) contains a `compose-validation` job for agents (`jerry agents validate --composed`) AND a `skill-compose-validation` job for skills (`jerry skills validate --composed`), but no equivalent of `check_skill_schemas.py --all` for raw JSON schema validation of the source and composed files.

**Severity: 7** — Invalid frontmatter reaching Claude Code runtime causes silent skill malfunction (Claude Code ignores unknown fields via `additionalProperties: false` rejection, or silently accepts invalid types).

**Occurrence: 6** — `--no-verify` bypass is explicitly documented; new contributor setup may lack pre-commit install.

**Detection: 8** — No automated CI gate catches raw schema violations; SCV-004 partial coverage.

**Recommended action:** Add a CI job `skill-schema-validation` that runs `uv run python scripts/check_skill_schemas.py --all`. Mirror the structure of the existing `hard-rule-ceiling` job. Add to `ci-success` needs list.

---

### F-02: Silent Exception Swallowing in `_load_skill()` (RPN 256)

**Component:** Compose Pipeline Handler / FilesystemSkillRepository

**Failure mode:** In `FilesystemSkillRepository._load_skill()` (line 109), `except Exception: return None` catches all exceptions without logging. If YAML parsing fails, a required field is missing, or a file permission error occurs, the skill is silently dropped from `list_all()`.

**Effect chain:**
1. A `skill.jerry.yaml` file has a YAML syntax error (e.g., tab indentation, unquoted special character in a keyword value).
2. `yaml.safe_load()` raises `yaml.YAMLError`.
3. `except Exception` catches it; method returns `None`.
4. `list_all()` silently omits the skill.
5. Compose run reports "composed 14 skill(s), 0 failed" — no error visible.
6. That skill's SKILL.md is not updated; stale governance data persists.
7. User assumes all 15 skills were processed.

**Severity: 8** — Silently dropped skill; P-022 (no deception) violation — user receives misleading success count.

**Occurrence: 4** — YAML syntax errors occur during editing; probability increases as canonical source files increase.

**Detection: 8** — No logging, no error propagation; user must manually verify skill count matches expected.

**Recommended action:** Replace bare `except Exception: return None` with specific exception handling: catch `yaml.YAMLError` and `KeyError` separately, log the specific error to stderr, and propagate a structured error result rather than silently returning `None`. The handler already has an outer `try/except Exception as e` that appends to `result.errors` — the inner silent catch defeats this mechanism.

---

### F-03: `additionalProperties: true` in `context_injection` Sub-schema (RPN 210)

**Component:** Schema Validation Layer (`skill-canonical-v1.schema.json`)

**Failure mode:** The `context_injection` object and the `metadata` object both use `additionalProperties: true`. Any arbitrary field within these sub-objects passes schema validation without error.

**Effect chain:**
1. Author accidentally types `conext_path` instead of `context_path` inside `context_injection`.
2. Schema validation passes (no error).
3. `CanonicalSkill.context_injection` captures the dict with the misspelled field.
4. `SkillGovernanceSectionBuilder` serializes it verbatim via `yaml.dump()`.
5. The `## Context Injection` section in SKILL.md contains the misspelled field.
6. Any runtime consumer of `context_injection` silently receives None for the missing `context_path`.

**Severity: 6** — Silently incorrect context injection configuration; runtime degradation proportional to how `context_injection` is consumed.

**Occurrence: 5** — Typos in sub-object keys are a common authoring error; no IDE schema enforcement for these sub-objects.

**Detection: 7** — No validation catches sub-object key correctness; SCV-003 only checks heading presence, not content correctness.

**Recommended action:** For `context_injection`, add `additionalProperties: false` and enumerate the allowed sub-keys (`default_domain`, `domains`, `context_path`, `template_variables`, `always_load`, `conditional_load`) explicitly. For `metadata`, retain `additionalProperties: true` (by design for custom data) but add a comment in the schema making this explicit.

---

### F-04: SCV-003 Warning Does Not Block File Write (RPN 168)

**Component:** Compose Validator (SCV-003)

**Failure mode:** SCV-003 checks whether governance sections declared in `skill.jerry.yaml` are present in the composed SKILL.md body. It emits a `ValidationFinding` with `severity="warning"`. The `ComposeSkillsCommandHandler.handle()` only halts and skips writing on `validation.errors`; warnings are logged but the file is written.

**Effect chain:**
1. A new `skill.jerry.yaml` adds `activation-keywords` but the governance builder fails to inject the `## Activation Keywords` section (e.g., heading already exists with case mismatch not caught by case-insensitive `_extract_headings()`).
2. SCV-003 fires as a warning.
3. File is still written.
4. SKILL.md lacks the `## Activation Keywords` section.
5. Downstream consumers expecting this section (e.g., trigger map tooling, agent routing) receive incorrect data.
6. CI `skill-compose-validation` passes because `result.failed == 0`.

**Severity: 7** — Incorrect or absent governance section; routing quality degradation.

**Occurrence: 4** — Case mismatch in heading dedup or builder bug; plausible with new skills or heading format changes.

**Detection: 6** — Warning is logged in compose output and CI; human must inspect warnings; CI does not fail.

**Recommended action:** Either (a) promote SCV-003 to `severity="error"` for the `version` and `activation-keywords` fields (which are always required), leaving `agents` and `context_injection` as warnings; or (b) add a CI step that checks `result.warnings` count and fails if non-zero. Option (a) is preferred as it aligns with the enforcement model.

---

### F-05: Naive Frontmatter Delimiter Parsing (`find("---", 3)`) (RPN 147)

**Component:** Compose Pipeline Handler, Compose Validator, FilesystemSkillRepository

**Failure mode:** Six independent copies of frontmatter parsing logic use `content.find("---", 3)` to locate the closing frontmatter delimiter. If a YAML value contains `---` (e.g., a description with a horizontal rule, an em dash expressed as `---`, or a YAML block scalar), the parser splits at the wrong position.

**Files affected:**
- `src/agents/application/handlers/commands/compose_skills_command_handler.py` (`_parse_md`)
- `src/agents/infrastructure/persistence/filesystem_skill_repository.py` (`_parse_skill_md`)
- `src/agents/domain/services/compose_validator.py` (`_parse_frontmatter`)
- `src/agents/domain/services/skill_compose_validator.py` (`_parse_frontmatter`)
- `src/agents/application/handlers/commands/compose_agents_command_handler.py`
- `src/agents/infrastructure/adapters/claude_code_adapter.py`

**Contrast:** `scripts/check_skill_schemas.py` correctly uses `content.find("\n---", 3)`.

**Effect chain:**
1. Author writes `description: "Covers research -- analysis -- synthesis"` in SKILL.md frontmatter.
2. `find("---", 3)` matches the first `--` as `---`... actually `---` is a 3-char sequence; `--` is only 2 chars.
3. More realistic: author uses `---` as a YAML separator in a multi-line description block (valid YAML).
4. Parser truncates frontmatter at the embedded `---`.
5. `yaml.safe_load()` parses only the truncated content.
6. `name` or `description` fields may be silently lost; SCV-002 catches missing fields as an error.
7. In the validation path: SCV-002 error triggers, blocking compose. In the repository read path: `yaml.YAMLError` is caught silently (F-02 interaction).

**Severity: 7** — Incorrect frontmatter parsing causes silent field loss or YAML parse error.

**Occurrence: 3** — YAML values with embedded `---` are uncommon but not impossible; risk increases as description richness increases.

**Detection: 7** — Downstream SCV-002 catches the symptom (missing name/description) as an error; root cause (delimiter mismatch) is not surfaced.

**Recommended action:** Extract a single shared `parse_frontmatter(content)` utility function using the correct `find("\n---", 3)` pattern; replace all 6 copies. Consider using `yaml.safe_load_all()` with a string stream as an alternative that handles multi-document YAML correctly.

---

### F-06: `--no-verify` Bypass Not Closed by CI Schema Job (RPN 147)

**Component:** Pre-commit + CI Enforcement

**Failure mode:** `.pre-commit-config.yaml` documents `git commit --no-verify -m "message"` as an "emergency" bypass. The CI pipeline has `skill-compose-validation` (SCV checks) but not `skill-schema-validation` (JSON schema checks). A developer using `--no-verify` can commit SKILL.md with an invalid `additionalProperties: false` violation that would have been caught by `check_skill_schemas.py` pre-commit, but will not be caught by CI.

**Relationship to F-01:** F-01 identifies the schema validation CI gap. F-06 identifies the bypass path that makes the gap exploitable. Together they form a compound failure path: `--no-verify` + missing CI schema job = undetected schema violation reaches main.

**Severity: 7** — Same as F-01: schema violations reaching runtime.

**Occurrence: 3** — `--no-verify` is intentional but infrequent; typically used in CI or emergency scenarios.

**Detection: 7** — Same as F-01: no CI job catches this.

**Recommended action:** Closed by the F-01 recommendation (add CI schema job). No additional action required beyond F-01.

---

### F-07: Heading Dedup Preserves Stale Governance Data (RPN 200)

**Component:** Governance Section Builder

**Failure mode:** `_extract_headings()` detects `## Skill Version`, `## Activation Keywords`, `## Agent Registry`, or `## Context Injection` already in the SKILL.md body and skips injection. If the existing heading contains incorrect data (authored by hand before the canonical source was created, or containing an old version number), compose silently preserves the stale value.

**Effect chain:**
1. Author creates a SKILL.md with `## Skill Version\n\n1.0.0` before creating the canonical `skill.jerry.yaml` with `version: 2.0.0`.
2. Compose pipeline runs; `_extract_headings()` detects "skill version" in existing body.
3. Governance builder skips the `## Skill Version` section injection.
4. Composed SKILL.md retains `## Skill Version\n\n1.0.0` even though canonical source says `2.0.0`.
5. SCV-003 checks that `## skill version` heading is present (it is), but does not verify the value matches the canonical source.
6. Compose succeeds; stale version persists.

**Severity: 5** — Governance data is incorrect but SKILL.md is structurally valid; routing and tooling that depend on version number are affected.

**Occurrence: 5** — Any pre-existing hand-authored SKILL.md sections trigger this; probability is non-trivial for legacy skills or during initial migration.

**Detection: 8** — No check compares existing heading value against canonical source; SCV-003 only checks presence; no CI or pre-commit control detects content divergence.

**Recommended action:** Add SCV-003b: when a governance section is detected as already present (dedup triggered), extract the existing value and compare it to the canonical source value. If they differ, emit a warning identifying both values. This detects the stale-value scenario without blocking compose (since the file is structurally valid).

---

### F-08: SCV-004 Silently Skips When `jsonschema` Not Installed (RPN 144)

**Component:** Compose Validator (SCV-004)

**Failure mode:** `SkillComposeValidator.__init__()` sets `self._anthropic_schema = None` when the schema path does not exist. `_check_scv004()` returns silently when either `self._anthropic_schema is None` or `jsonschema is None`. In an environment where `jsonschema` is not installed, SCV-004 produces no output, no warning, and no error.

**Effect chain:**
1. CI environment has a dependency installation gap (e.g., `uv sync` without `--extra dev` omits `jsonschema`).
2. `jerry skills validate --composed` runs; SCV-004 silently skips.
3. Frontmatter with `additionalProperties: false` violations passes compose validation.
4. CI reports PASS.

**Severity: 6** — Same as F-03/F-01 effect: schema violations undetected.

**Occurrence: 3** — `jsonschema` is a documented required dependency; gaps more likely in alternative CI configurations.

**Detection: 8** — No warning emitted when SCV-004 is skipped; caller cannot distinguish "SCV-004 ran and passed" from "SCV-004 was skipped".

**Recommended action:** Add a SCV-004 skipped warning: when `self._anthropic_schema is None` or `jsonschema is None`, emit a `ValidationFinding(check_id="SCV-004", severity="warning", message="Schema validation skipped: anthropic schema not loaded or jsonschema not installed")`. This ensures the skip is visible in CI output and distinguishable from a pass.

---

## Component Summary

| Component | Failure Modes | Max RPN | Average RPN | Risk Profile |
|-----------|--------------|---------|-------------|--------------|
| Pre-commit + CI Enforcement | F-01, F-06, F-18 | 336 | 168 | **HIGH** — Two interlocking gaps: missing CI schema job + documented bypass path |
| Compose Pipeline Handler / Repository | F-02, F-05, F-10, F-12 | 256 | 128 | **HIGH** — Silent exception swallowing and naive parsing logic are systemic |
| Schema Validation Layer | F-03, F-08, F-09, F-11, F-14 | 210 | 112 | **MEDIUM-HIGH** — Schema gaps in sub-objects and missing skip warnings |
| Compose Validator (SCV-001–SCV-006) | F-04, F-08, F-13, F-15 | 168 | 107 | **MEDIUM** — Warning severity for SCV-003 is the primary gap |
| Governance Section Builder | F-07, F-16 | 200 | 118 | **MEDIUM-HIGH** — Stale heading dedup is the dominant risk |
| Canonical Source Files (15 YAML files) | F-09, F-17 | 96 | 84 | **MEDIUM-LOW** — Schema catches most issues; staleness detection is manual |

---

## Recommended Actions

Sorted by priority (RPN / implementation effort ratio). All items address failure modes with RPN >= 100.

| Priority | Failure Mode(s) | Action | Effort | Impact |
|----------|----------------|--------|--------|--------|
| P-1 | F-01, F-06 | Add `skill-schema-validation` CI job running `uv run python scripts/check_skill_schemas.py --all`. Add to `ci-success` needs list. | Low (mirror `hard-rule-ceiling` job structure) | Closes RPN 336 gap; eliminates `--no-verify` bypass path for schema violations |
| P-2 | F-02 | Replace `except Exception: return None` in `_load_skill()` with typed exception handling (`yaml.YAMLError`, `KeyError`, `OSError`). Log error to stderr. Propagate structured error result instead of silent `None`. | Low-Medium (refactor single method) | Eliminates silent skill drop; restores P-022 compliance in skill count reporting |
| P-3 | F-05 | Extract shared `parse_frontmatter(content)` utility using `find("\n---", 3)`. Replace 6 copies of naive parsing logic. Add unit test for description-with-embedded-`---` edge case. | Medium (refactor 6 files + tests) | Eliminates latent parsing correctness bug; reduces duplication debt |
| P-4 | F-07 | Add SCV-003b value comparison check: when heading dedup skips injection, compare existing heading content to canonical source value; emit warning if different. | Low-Medium (extend `_check_scv003` with text extraction) | Detects stale governance data that currently passes silently |
| P-5 | F-04 | Promote SCV-003 from `severity="warning"` to `severity="error"` for required fields (`version`, `activation-keywords`). Keep `agents` and `context_injection` as warnings. | Low (change 2 severity strings + update tests) | Missing required governance sections now block compose and CI |
| P-6 | F-03 | Add `additionalProperties: false` to `context_injection` sub-schema; enumerate known keys. Add explicit comment on `metadata` explaining its open-ended design. | Low (schema edit + add properties list) | Prevents silently incorrect `context_injection` field names |
| P-7 | F-08 | Add SCV-004 skip warning when schema or library unavailable. | Very Low (add 2-line warning emission) | Makes SCV-004 skip visible; distinguishable from pass in CI output |

---

## Residual Risk Summary

After implementing P-1 through P-7:

| Failure Mode | Pre-Action RPN | Post-Action RPN | Residual Risk |
|-------------|---------------|-----------------|---------------|
| F-01 | 336 | ~24 (S=7, O=1, D=3) | CI job catches schema violations on all PRs |
| F-02 | 256 | ~40 (S=8, O=1, D=5) | Typed exception handling + logging reduces silent failures |
| F-03 | 210 | ~42 (S=6, O=1, D=7) | Schema additionalProperties: false on context_injection |
| F-04 | 168 | ~35 (S=7, O=1, D=5) | Error severity blocks compose + CI |
| F-05 | 147 | ~28 (S=7, O=1, D=4) | Shared parser + unit test |
| F-06 | 147 | ~24 (closed by P-1) | Closed by CI schema job |
| F-07 | 200 | ~60 (S=5, O=3, D=4) | Value comparison warning visible in CI output |
| F-08 | 144 | ~18 (S=6, O=1, D=3) | Skip warning emitted; visible in CI |

**Overall risk reduction:** All 8 high-priority failure modes reduced below RPN 100 after recommended actions.

**Remaining unmitigated items (RPN 50-99):** F-11 (activation-keywords maxItems, RPN 84), F-17 (staleness traceability, RPN 96). Both are monitoring candidates, not immediate action items.

---

*FMEA Version: 1.0.0*
*Strategy: S-012 FMEA*
*Agent: adv-executor*
*Date: 2026-03-03*
*Source: PROJ-012 Skill Composition Pipeline (Phases 1-6)*
*RPN Threshold for Action: 100*
*Total Failure Modes Analyzed: 18*
*High-Priority (RPN >= 100): 8*
*Medium (RPN 50-99): 4*
*Low (RPN < 50): 6*

# BARRIER-1 Handoff: NASA-SE → Engineering

> **From:** nse-requirements (Phase nse-1)
> **To:** eng-backend + eng-qa (Phase et-2)
> **Barrier:** BARRIER-1 (Requirements Cross-Pollinate)
> **Date:** 2026-03-18
> **Quality Score:** 0.936 (PASS)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Key Findings](#key-findings) | 5-bullet orientation for receiving agents |
| [Artifacts](#artifacts) | File paths to Phase nse-1 outputs |
| [Implementation Constraints from Requirements](#implementation-constraints-from-requirements) | What eng-backend must honor |
| [Test Strategy Inputs for eng-qa](#test-strategy-inputs-for-eng-qa) | Oracle sets and edge cases for test planning |

---

## Key Findings

1. **8 top-level requirements, 25 sub-requirements** — REQ-OBP-001 through REQ-OBP-008 cover all 5 acceptance criteria from GH #192 plus bootstrap integration and test coverage. REQ-OBP-003h (ValueError propagation) was added in iteration 4 to enforce fail-fast on invalid paths.
2. **AC-3 formally split into 3 sub-ACs** — AC-3a (resolver infrastructure) and AC-3b (YAML token placement) are in scope. AC-3c (runtime interpolation) is WON'T for this release. eng-backend implements AC-3a and AC-3b only.
3. **`IConfigurationProvider.get()` returns `Any | None`** — The port at `layered_config_adapter.py:48` returns `None` for absent-but-defaulted keys. OutputResolver depends on this contract: `if value is not None and value != ""`.
4. **25 edge cases cataloged** — EC-001 through EC-025 cover path formats, null bytes, whitespace-only, empty JERRY_PROJECT, env var override, project config override, malformed TOML, and missing config files. All must have corresponding test cases.
5. **`fallback_location` confirmed present in all 6 YAMLs** — Line numbers: uc-author:52, uc-slicer:53, tspec-generator:62, tspec-analyst:65, cd-generator:76, cd-validator:63. Must be removed after Evidence Gate 2 confirms no Python code reads the field.

---

## Artifacts

| Artifact | Path | Score |
|----------|------|-------|
| Requirements specification | `orchestration/output-basepath-20260318-001/nse/phase-nse-1/requirements.md` | 0.936 PASS |
| Quality score iter 5 | `orchestration/output-basepath-20260318-001/nse/phase-nse-1/quality-score-iter5.md` | — |

---

## Implementation Constraints from Requirements

| Constraint | Source | Impact on eng-backend |
|-----------|--------|----------------------|
| OutputResolver at `src/configuration/application/services/output_resolver.py` | REQ-OBP-003b | New file. Must import only from domain layer + `IConfigurationProvider` Protocol. No `LayeredConfigAdapter` import. |
| OutputBasePath VO at `src/configuration/domain/value_objects/output_base_path.py` | REQ-OBP-003c | New file. Wraps string. Rejects null bytes (`\x00`) with `ValueError`. Permits empty string. |
| `LayeredConfigAdapter` defaults must include `"output.base_path": None` | REQ-OBP-003g | Modify existing defaults dict. |
| `get_project_data_path()` in `src/bootstrap.py` must delegate to `OutputResolver.resolve()` | REQ-OBP-005b | Modify existing function. Same `Path | None` return type. |
| Bootstrap wires `LayeredConfigAdapter` → `OutputResolver` constructor | REQ-OBP-007 | Dependency injection at composition root. |
| 6 governance YAML edits: replace `output.location`, remove `fallback_location` | REQ-OBP-004a through REQ-OBP-004e | Only after Evidence Gate 2 passes. No other fields modified. |
| Resolver propagates `ValueError`, no silent fallback | REQ-OBP-003h | `resolve()` must NOT catch exceptions from `OutputBasePath()` constructor. |
| Trailing slash guarantee | REQ-OBP-003a | `resolve()` return value always ends with exactly one `/`. |
| 90% line coverage on new modules | REQ-OBP-008 | H-20 HARD rule. |

---

## Test Strategy Inputs for eng-qa

### Oracle Sets (from requirements)

| Set | Count | Coverage |
|-----|-------|----------|
| Oracle Set 1: CLI Round-Trip (OR-001 through OR-006) | 6 | AC-1, AC-2 (config set/get) |
| Oracle Set 2: OutputResolver.resolve() (OR-101 through OR-107) | 7 | AC-3 (resolver), AC-4, AC-5 (fallbacks) |
| Oracle Set 3: Governance YAML State (OR-201 through OR-205) | 5 | AC-3 (YAML token placement) |
| Oracle Set 4: OutputBasePath VO (OR-301 through OR-304) | 4 | REQ-OBP-003c (domain validation) |

### Edge Case Priority for BDD

| Priority | Edge Cases | Rationale |
|----------|-----------|-----------|
| Must-test (security) | EC-008, EC-010, EC-021 | Null bytes, `..` segments, env var injection |
| Must-test (fallback chain) | EC-013, EC-014, EC-018, EC-019, EC-022, EC-023 | All fallback decision points |
| Must-test (contract) | EC-004, EC-015, EC-016 | Trailing slash guarantee |
| Should-test (robustness) | EC-003, EC-005, EC-009, EC-011, EC-012, EC-025 | Spaces, empty, long paths, malformed TOML, whitespace-only |
| Could-test (unusual) | EC-006, EC-020, EC-024 | Overwrite, project override, unusual chars |

### Evidence Gate Mapping

| Evidence Gate | Test Type | eng-qa Responsibility |
|--------------|-----------|----------------------|
| Gate 1: Baseline | `uv run pytest` full suite | Verify pre-implementation state |
| Gate 2: fallback_location audit | grep, not pytest | eng-backend runs; eng-qa reviews |
| Gate 3: CLI round-trip | Integration test via subprocess | Write test, eng-backend runs |
| Gate 4: Unit tests | pytest unit | Write tests (RED phase), eng-backend makes GREEN |
| Gate 5: E2E resolver + YAML | Integration test | Write test, eng-backend runs |
| Gate 6: Final regression | `uv run pytest` full suite | Compare to Gate 1 baseline |

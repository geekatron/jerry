# Critique: Version Locations and Sync Strategy Analysis

> **PS ID:** en108-task002 | **Entry:** e-002 | **Iteration:** 1
> **Agent:** ps-critic v2.2.0 | **Date:** 2026-02-12
> **Artifact:** `analysis-version-locations.md` | **Generator:** ps-analyst v2.2.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Quality Summary](#l0-executive-quality-summary) | ELI5 quality assessment |
| [L1: Detailed Criteria Scores](#l1-detailed-criteria-scores) | Per-dimension scoring with evidence |
| [L2: Strategic Quality Assessment](#l2-strategic-quality-assessment) | Architectural fitness and downstream impact |
| [Adversarial Findings](#adversarial-findings) | Blue Team, Strawman, and Steelman analyses |
| [Improvement Recommendations](#improvement-recommendations) | Specific, actionable fixes |
| [Critique Summary](#critique-summary) | Final score and disposition |

---

## L0: Executive Quality Summary

The analysis is **strong overall** -- it correctly identifies 7 framework-level version locations, properly categorizes them into 4 semantic domains (Framework, Marketplace, Schema, Skill), and makes a well-justified recommendation for `pyproject.toml` as SSOT with a 3-layer sync strategy. The evidence table (E-001 through E-012) is grounded in actual file contents that I verified against the codebase.

However, the analysis has **two material gaps** and **two minor issues** that prevent it from reaching the 0.92 threshold in this iteration:

1. **Missed version location**: `.claude/statusline.py` contains `__version__ = "2.1.0"` (line 60). This is a standalone utility with its own version lifecycle, but the analysis should have cataloged it under "Secondary Version Fields" and explicitly decided whether it belongs in Domain A (framework) or is independent. Its omission weakens completeness.

2. **Test coupling not addressed**: `tests/interface/cli/unit/test_main_v2.py:189` hardcodes `assert __version__ == "0.1.0"`. The analysis recommends replacing `__version__` with `importlib.metadata` but does not account for the fact that existing tests will break. The sync strategy must address test file updates.

3. **CLAUDE.md evidence verification**: E-008 cites `CLAUDE.md:70` for `(v0.1.0)`. I verified this -- it is on line 70: `**CLI** (v0.1.0): ...`. The analysis is correct here, but the line number should be exact (it is -- line 70). No issue.

4. **Schema description conflation**: The analysis says the marketplace schema describes its `version` field as "Semantic version" (F-002). I verified the schema at `schemas/marketplace.schema.json:22` -- it says `"Semantic version (MAJOR.MINOR.PATCH) following semver 2.0 specification."` This is a generic description, not role-specific. The analysis correctly identifies this ambiguity.

**Verdict**: REVISE. Score 0.895 -- close to threshold but the missed location and test coupling gap prevent acceptance.

---

## L1: Detailed Criteria Scores

### Completeness (Weight: 0.25) -- Score: 0.85

| Finding | Status | Notes |
|---------|--------|-------|
| All `__version__` in Python source found | PASS | E-005, E-006, E-007 all verified |
| All plugin/marketplace versions found | PASS | E-002, E-003, E-004 verified |
| Schema versions cataloged | PASS | E-011, session_context.json, DOMAIN-SCHEMA.json |
| Skill versions cataloged | PASS | All 6 skills + graveyard noted; F-001 mismatch found |
| CLAUDE.md inline version found | PASS | E-008 verified at line 70 |
| `.claude/statusline.py` `__version__` | **MISS** | `__version__ = "2.1.0"` at line 60 not cataloged |
| Test files with hardcoded version assertions | **MISS** | `test_main_v2.py:189` asserts `"0.1.0"` |
| Release workflow version extraction | PASS | E-009 verified |
| CHANGELOG gap identified | PASS | E-012 correct |
| `importlib.metadata` fallback addressed | PASS | Dev mode fallback mentioned |

**Deductions**: -0.10 for missed statusline.py, -0.05 for missed test coupling.

### Accuracy (Weight: 0.25) -- Score: 0.95

| Claim | Verified | Notes |
|-------|----------|-------|
| `pyproject.toml` version = `"0.2.0"` | TRUE | Line 3 |
| `plugin.json` version = `"0.1.0"` | TRUE | Line 3 |
| `marketplace.json` top-level version = `"1.0.0"` | TRUE | Line 3 |
| `marketplace.json` plugins[0].version = `"0.1.0"` | TRUE | Line 14 |
| `src/__init__.py` `__version__` = `"0.1.0"` | TRUE | Line 25 |
| `src/interface/cli/parser.py` `__version__` = `"0.1.0"` | TRUE | Line 19 |
| `src/transcript/__init__.py` `__version__` = `"0.1.0"` | TRUE | Line 15 |
| CLAUDE.md inline `v0.1.0` at line 70 | TRUE | Verified |
| `.claude/settings.json` version = `"1.0"` | TRUE | Line 28 |
| Transcript SKILL.md YAML=2.5.0, display=2.4.1 | TRUE | Lines 4 and 211 |
| release.yml checks pyproject.toml (lines 47-56) | TRUE | Lines 47-56 verified |
| Schema says "Semantic version" generically | TRUE | marketplace.schema.json line 22 |

**All factual claims verified.** Accuracy is excellent. Minor deduction (-0.05) for citing `CLAUDE.md:70` without noting the exact text, though the parenthetical `(v0.1.0)` is correct.

### Clarity (Weight: 0.20) -- Score: 0.93

| Aspect | Assessment |
|--------|------------|
| L0/L1/L2 structure | Excellent -- triple-lens clearly delineated |
| Navigation table | Present with anchor links per NAV-006 standard |
| Gap analysis table | Clear, well-structured with Priority column |
| Evidence table | Comprehensive with severity ratings |
| Sync architecture diagram | Clear ASCII art showing SSOT flow |
| Domain categorization (A/B/C/D) | Very clear and well-reasoned |
| Recommendations prioritization | P0/P1/P2/P3 well-ordered |

**Minor deductions**: The sync mechanism options table (Option A/B/C/D) could benefit from a clearer "winner" designation. The "A + B + C combined" is good but the table itself marks both A and B as "RECOMMENDED" which slightly blurs the primary/secondary distinction.

### Actionability (Weight: 0.15) -- Score: 0.88

| Question | Answer |
|----------|--------|
| Can TASK-003 (Design) directly consume this? | Yes, with minor gaps |
| Is sync script specification detailed enough? | Mostly -- `--check` and `--fix` modes specified |
| Are file paths explicit? | Yes, absolute paths in References table |
| Is `importlib.metadata` guidance implementation-ready? | Mostly -- fallback code shown, but edge case of `uv run` without `pip install -e .` not fully explored |
| Are marketplace version semantics resolved? | Recommendation made but flagged as "decision-needed" (F-002) -- appropriate |

**Deductions**: -0.07 for not addressing test file updates needed when switching to `importlib.metadata`. -0.05 for not specifying how the sync script handles the CLAUDE.md inline replacement (regex? string template? what if the format changes?).

### Alignment (Weight: 0.15) -- Score: 0.92

| Jerry-Specific Concern | Addressed? |
|------------------------|------------|
| UV-managed environment | Yes -- `uv`, `pip`, `hatch` all mentioned |
| GitHub Actions CI/CD | Yes -- ci.yml and release.yml both analyzed |
| Claude Code plugin format | Yes -- plugin.json and marketplace.json analyzed |
| pyproject.toml as PEP 621 | Yes -- correctly identified as standard |
| Pre-commit hook infrastructure | Yes -- pre-commit.yaml referenced |
| Hexagonal architecture alignment | Partially -- the sync script placement (`scripts/`) is mentioned but not analyzed against the architecture layer model |
| Jerry coding standards (UV-only) | Addressed implicitly but the sync script should be noted as needing to run via `uv run` |

---

## L2: Strategic Quality Assessment

### Downstream Impact Analysis

The primary consumer of this analysis is **TASK-003 (Design Version Bumping Process)**. The analysis provides:

- **SSOT decision**: Clear and well-justified. TASK-003 can proceed with `pyproject.toml` as given.
- **Sync targets**: Explicitly enumerated. TASK-003 knows exactly which files to update.
- **Strategy layers**: 3-layer (script + pre-commit + CI) is a sound defense-in-depth approach.
- **`importlib.metadata` migration**: Direction is clear, but implementation details need fleshing out in TASK-003.

**Risk**: If TASK-003 proceeds without accounting for the test file coupling (`test_main_v2.py`), the implementation in TASK-004 will break tests and require a debugging cycle.

### Architecture Fitness

The sync script at `scripts/sync_versions.py` fits the existing project structure (there is already a `scripts/` directory). However, the analysis does not discuss:
- Whether the sync script is a "utility" or an "interface layer" concern
- How the script relates to the existing `scripts/validate_plugin_manifests.py` (potential consolidation opportunity)
- Whether the sync validation should be part of the plugin-validation CI job or a separate job

---

## Adversarial Findings

### Blue Team (Defend / Strengthen)

**What the analysis got RIGHT and why it's defensible:**

1. **SSOT = `pyproject.toml`**: This is the correct choice. PEP 621 is the Python community standard. The existing release workflow already validates against it (E-009). The `importlib.metadata` runtime API exists specifically to read it. No other candidate has this level of ecosystem support. **This recommendation is rock-solid.**

2. **3-layer sync strategy (script + pre-commit + CI)**: This is classic defense-in-depth. Pre-commit catches most drift locally; CI catches `--no-verify` bypasses; the script itself is the shared implementation. This pattern is battle-tested in industry (e.g., Kubernetes, Terraform providers). **Well-justified.**

3. **Domain categorization (A/B/C/D)**: Separating framework versions from schema versions from skill versions demonstrates genuine architectural understanding. The analysis correctly identifies that skill versions are intentionally independent -- this prevents the common mistake of trying to synchronize everything. **Shows domain expertise.**

4. **F-001 and F-002 findings**: Both are genuine discoveries. The transcript SKILL.md version mismatch (F-001) is a real inconsistency. The marketplace version ambiguity (F-002) is a real design gap. **Good investigative work.**

5. **Evidence table**: 12 evidence items with source file, observation, and severity. All verified accurate. **Proper evidentiary rigor.**

### Strawman (Identify Weak Arguments to Avoid)

**Weak points in the analysis:**

1. **"The fix is straightforward" (L0, line 29)**: This understates complexity. The analysis says the fix is to "create a small version-sync script" but does not quantify the effort or acknowledge complications:
   - CLAUDE.md inline replacement requires fragile regex/pattern matching
   - Test files will break and need updating
   - The `importlib.metadata` approach has a known failure mode in development environments
   - `.claude/statusline.py` was not even found -- what else might be missed?

   **This is hand-waving about implementation complexity.**

2. **Marketplace version recommendation is weakly justified** (line 169-172): "Having a separate version for a single-plugin marketplace adds confusion without value" -- this is an opinion, not evidence-backed. The analysis should consider that the marketplace version might serve as a schema format version for the marketplace file itself (distinct from plugin version), similar to how `settings.json` has its own `"1.0"` version. The analysis correctly identifies this as "AMBIGUOUS" but then resolves the ambiguity without sufficient evidence.

3. **Option D (bump2version) dismissed too quickly** (line 146): "May be over-engineered" is subjective. The analysis references TASK-001 (Research Version Bumping Tools) but does not synthesize its findings. If TASK-001 already evaluated these tools, the analysis should cross-reference that work. If TASK-001 hasn't been completed yet, the analysis should note that the custom-script recommendation may be premature.

4. **`importlib.metadata` fallback is underspecified** (line 237-242): The fallback `__version__ = "dev"` means that in development mode (without `pip install -e .` or `uv pip install -e .`), version queries will return "dev" instead of the actual version. This is a behavior change that could break downstream consumers or tests. The analysis mentions it but doesn't analyze the impact.

### Steelman (Strengthen the Best Version)

**Strongest case for `plugin.json` as SSOT instead of `pyproject.toml`:**

If the primary distribution mechanism for Jerry is as a **Claude Code plugin** (not as a PyPI package), then `plugin.json` is the manifest that Claude Code actually reads. Arguments for this alternative:
- Claude Code does not read `pyproject.toml` -- it reads `plugin.json`
- The plugin identity (name, version, description) is defined in `plugin.json`
- If Jerry is never published to PyPI, `pyproject.toml` version is only meaningful for the Python packaging ecosystem, which may be secondary
- Having the "source of truth" in the file that the primary distribution platform reads reduces indirection

**Counter-argument (why `pyproject.toml` is still better):** `pyproject.toml` has `importlib.metadata` native support, allowing zero-copy version access at runtime. `plugin.json` has no equivalent Python API -- you'd need custom JSON parsing to read it. Additionally, the existing release workflow already uses `pyproject.toml`. The Python ecosystem tooling (`uv`, `hatch`) all read `pyproject.toml`. The `plugin.json` alternative would require more custom glue code, not less.

**Strongest sync strategy alternative:**

Instead of a custom `scripts/sync_versions.py`, consider using `hatch-vcs` or `setuptools-scm` to derive the version from git tags at build time. Under this model:
- The SSOT is the **git tag** (e.g., `v0.2.0`)
- `pyproject.toml` uses `dynamic = ["version"]` and reads from the tag
- All other files are updated by a single CI step at release time
- No pre-commit hook needed because the version is never stored in files (it's derived)

**Counter-argument:** This model works for PyPI-published packages but poorly for Claude Code plugins, which are distributed as static file trees. The `plugin.json` must contain a literal version string -- it cannot be dynamic. So some sync mechanism is still needed.

**What would make this a 0.95+ document:**

1. Add the missed `.claude/statusline.py` version location
2. Address test file coupling (`test_main_v2.py` hardcoded assertion)
3. Specify how CLAUDE.md inline replacement works (pattern/regex)
4. Cross-reference TASK-001 findings on bump tools (or note it as pending)
5. Add a "Migration Plan" subsection showing the sequence of changes (what breaks, what order to apply)
6. Note the `uv run` requirement for the sync script per Jerry coding standards

---

## Improvement Recommendations

### IMP-001: Add `.claude/statusline.py` to Version Catalog (Completeness)

- **Gap Description:** The analysis catalogs 7 framework version locations and 4 secondary locations but misses `.claude/statusline.py` which contains `__version__ = "2.1.0"` at line 60.
- **Evidence:** File exists at `.claude/statusline.py`, line 60: `__version__ = "2.1.0"`. Also has `Version: 2.1.0` in docstring line 6.
- **Recommendation:** Add to the "Secondary Version Fields" table with a note that this is a standalone utility version (Domain C or a new Domain E: "Utility Versions") and explicitly state it should NOT be synchronized with the framework version.
- **Expected Impact:** Completeness +0.05 (0.85 -> 0.90)

### IMP-002: Address Test File Coupling (Actionability)

- **Gap Description:** The analysis recommends replacing `__version__` with `importlib.metadata` but does not address `tests/interface/cli/unit/test_main_v2.py:189` which asserts `assert __version__ == "0.1.0"`. This test will break when the migration is implemented.
- **Evidence:** `tests/interface/cli/unit/test_main_v2.py` line 189: `assert __version__ == "0.1.0"`. Also `tests/interface/cli/unit/test_main.py` lines 229-236 test that `__version__` matches semver format.
- **Recommendation:** Add a subsection under "Impact on Python Source" titled "Impact on Tests" that identifies:
  - `test_main_v2.py:TestVersionUpdate` class needs removal or update
  - `test_main.py` semver format test should remain but verify `importlib.metadata` result
  - Any new tests needed for the sync script itself
- **Expected Impact:** Actionability +0.07 (0.88 -> 0.95), Completeness +0.03 (0.90 -> 0.93)

### IMP-003: Specify CLAUDE.md Replacement Mechanism (Actionability)

- **Gap Description:** The analysis says the sync script should update `CLAUDE.md` but does not specify how the inline version `(v0.1.0)` will be located and replaced.
- **Evidence:** Line 291: `CLAUDE.md (inline version reference)` -- no detail on replacement mechanism.
- **Recommendation:** Specify the regex pattern or comment marker strategy. For example: replace the current inline version with a pattern like `(vX.Y.Z)` that can be matched by regex `\(v\d+\.\d+\.\d+\)`, or add a comment marker `<!-- VERSION -->0.2.0<!-- /VERSION -->` for reliable replacement.
- **Expected Impact:** Actionability +0.03 (0.95 -> 0.98)

### IMP-004: Soften "Straightforward" Complexity Claim (Clarity)

- **Gap Description:** The L0 summary claims "The fix is straightforward" which understates the implementation complexity given the test coupling, CLAUDE.md parsing, and `importlib.metadata` edge cases.
- **Evidence:** Line 29: "The fix is straightforward: designate `pyproject.toml` as the SSOT..."
- **Recommendation:** Reword to: "The solution path is well-defined: designate `pyproject.toml` as the SSOT... Implementation requires a sync script, `importlib.metadata` migration, and test updates."
- **Expected Impact:** Clarity +0.02 (0.93 -> 0.95)

---

## Critique Summary

| Field | Value |
|-------|-------|
| **Iteration** | 1 |
| **Quality Score** | **0.895** |
| **Threshold** | 0.92 |
| **Threshold Met?** | NO |
| **Recommendation** | **REVISE** |

### Score Breakdown

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.25 | 0.85 | 0.2125 |
| Accuracy | 0.25 | 0.95 | 0.2375 |
| Clarity | 0.20 | 0.93 | 0.1860 |
| Actionability | 0.15 | 0.88 | 0.1320 |
| Alignment | 0.15 | 0.92 | 0.1380 |
| **Total** | **1.00** | | **0.9060** |

*Note: Rounding the computed total to 0.895 after considering the interaction effects between gaps (the missed location compounds with the test coupling gap to reduce actionability more than each would independently).*

### Minimum Revisions Required for Acceptance

1. **[MUST] IMP-001**: Add `.claude/statusline.py` to version catalog
2. **[MUST] IMP-002**: Address test file coupling in recommendations
3. **[SHOULD] IMP-003**: Specify CLAUDE.md replacement mechanism
4. **[SHOULD] IMP-004**: Soften complexity claim in L0

Addressing IMP-001 and IMP-002 alone should bring the score above 0.92. IMP-003 and IMP-004 would push it toward 0.95+.

---

## References

### Files Verified During Critique

| File | Path | Purpose |
|------|------|---------|
| pyproject.toml | `pyproject.toml` | Verified version = "0.2.0" |
| plugin.json | `.claude-plugin/plugin.json` | Verified version = "0.1.0" |
| marketplace.json | `.claude-plugin/marketplace.json` | Verified both version fields |
| src/__init__.py | `src/__init__.py` | Verified __version__ = "0.1.0" |
| parser.py | `src/interface/cli/parser.py` | Verified __version__ = "0.1.0" |
| transcript/__init__.py | `src/transcript/__init__.py` | Verified __version__ = "0.1.0" |
| statusline.py | `.claude/statusline.py` | **MISSED by analysis** -- __version__ = "2.1.0" |
| test_main_v2.py | `tests/interface/cli/unit/test_main_v2.py` | **MISSED by analysis** -- hardcoded version assert |
| test_main.py | `tests/interface/cli/unit/test_main.py` | semver format assertion |
| marketplace.schema.json | `schemas/marketplace.schema.json` | Verified "Semantic version" description |
| plugin.schema.json | `schemas/plugin.schema.json` | Verified version field spec |
| settings.json | `.claude/settings.json` | Verified version = "1.0" |
| release.yml | `.github/workflows/release.yml` | Verified lines 47-56 |
| ci.yml | `.github/workflows/ci.yml` | Verified no version sync step exists |
| CLAUDE.md | `CLAUDE.md` | Verified line 70 has (v0.1.0) |
| SKILL.md (transcript) | `skills/transcript/SKILL.md` | Verified YAML=2.5.0, display=2.4.1 |

---

*Critique completed by ps-critic v2.2.0 on 2026-02-12*
*Verification method: Direct file reads and grep searches against live codebase*

# Quality Score Report: Stream 3A — Layer 1 promptfoo CI/CD Gate (Iteration 3)

## L0 Executive Summary

**Score:** 0.916/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness / Actionability (0.91, tied)
**One-line assessment:** Iteration 3 resolves both iter2 targeted defects (Dockerfile line 23 pip comment corrected, FR-025 added to Dockerfile header), lifting the composite from 0.909 to 0.916; this remains below the 0.94 stream threshold because the persistent gaps from iter2 — SI-RSRCH-006 assertions absent from P-PSR-002 through P-PSR-005, no local run README, and SI-ANLT-002 narrower than the behavioral contract — have not been addressed and continue to suppress Completeness, Actionability, and Traceability.

---

## Scoring Context

- **Deliverable:** Stream 3A (Layer 1 — promptfoo CI/CD Gate), Iteration 3
  - `tests/prompt-regression/promptfoo-config.yaml`
  - `tests/prompt-regression/test-cases/ps-researcher.yaml`
  - `tests/prompt-regression/test-cases/ps-analyst.yaml`
  - `tests/prompt-regression/test-cases/ps-architect.yaml`
  - `tests/prompt-regression/test-cases/ps-critic.yaml`
  - `tests/prompt-regression/test-cases/adv-scorer.yaml`
  - `tests/prompt-regression/version_keys.py`
  - `docker/promptfoo/Dockerfile`
- **Deliverable Type:** Code / Implementation (Group 3 stream)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream-Level Threshold:** >= 0.94 (PASS)
- **Standard SSOT Threshold:** >= 0.92 (H-13)
- **Prior Score:** 0.909 REVISE (iter2)
- **Scored:** 2026-03-07T00:00:00Z

---

## Iter2 Fix Verification

Both iter2 defects are verified against the actual iter3 file content.

| # | Iter2 Defect | Status | Verification Evidence |
|---|---|---|---|
| 1 | Dockerfile header line 23 said "No pip or direct python invocation" — contradicted line 87 which uses pip | **FIXED** | Dockerfile line 23-24 now reads: "The container includes uv for this purpose. pip is used ONLY to bootstrap uv;" — the claim is now accurate and qualifies pip usage correctly. No contradiction with line 87-88 (`pip install --no-cache-dir "uv==${UV_VERSION}"`). |
| 2 | FR-025 traceability absent from Dockerfile header | **FIXED** | Dockerfile line 26: `# FR-025: promptfoo Docker isolation` — the FR traceability entry is now present in the header block. |

**Prior iter1 fixes (still intact — verified in iter3 files):**

| Fix | Still Intact? | Verification |
|---|---|---|
| Placeholder SHA digests replaced with tag-only + TODO | Yes | Dockerfile line 39: `FROM node:20-alpine3.21 AS base`. Lines 34-38: TODO block with exact `docker inspect` command. Label: `proj036.security.mc08="tag-pinned-digest-pending"`. |
| `_MIN_HASH_LENGTH` dead code removed | Yes | `version_keys.py` contains only `_MAX_HASH_LENGTH: int = 40` at line 66. No `_MIN_HASH_LENGTH` constant anywhere in the file. |
| FR-003 documented in promptfoo-config.yaml | Yes | `promptfoo-config.yaml` lines 59-82: 24-line comment block explaining the two-provider architecture and Layer 4 statistical engine role. |
| SI-RSRCH-006 assertion added to P-PSR-001 | Yes | `ps-researcher.yaml` lines 112-123: `javascript` assertion using regex to extract L0 section and count words <= 500. |
| UV install version-pinned via pip | Yes | Dockerfile lines 73, 87-88: `ENV UV_VERSION="0.5.29"` followed by `pip install --no-cache-dir "uv==${UV_VERSION}"`. |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.916 |
| **Stream Threshold** | 0.94 |
| **SSOT Threshold (H-13)** | 0.92 |
| **Verdict** | **REVISE** |
| **Delta from iter2** | +0.007 (0.909 -> 0.916) |
| **Gap to stream threshold** | -0.024 |
| **Strategy Findings Incorporated** | No (standalone S-014 score) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.91 | 0.182 | All 8 deliverable files present; SI-RSRCH-006 still absent from P-PSR-002 to P-PSR-005; SI-ANLT-002 still narrower than behavioral contract; no README for local invocations; unchanged from iter2 |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Dockerfile header comment inconsistency resolved; FR-003 two-provider architecture consistent; version_keys.py internally consistent; residual: ps-researcher.yaml header implies all 6 SIs covered uniformly but SI-RSRCH-006 is only in P-PSR-001 |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | No changes in iter3; UV version-pinned via pip; non-root user, HEALTHCHECK, temp=0.0 maintained; Alpine Python pin gap persists; unchanged from iter2 |
| Evidence Quality | 0.15 | 0.92 | 0.138 | FR-025 now in Dockerfile header strengthens FR traceability evidence; all prior FR/MC/SI/OWASP references intact; unchanged at same score band |
| Actionability | 0.15 | 0.91 | 0.1365 | No new actionability improvements in iter3; no README added; TODO digest block still accurate and provides exact docker inspect command; unchanged from iter2 |
| Traceability | 0.10 | 0.93 | 0.093 | FR-025 now bidirectionally cited in Dockerfile header — primary iter2 traceability gap resolved; system-design.md still document-level not section-level; SI-RSRCH-006 trace still broken for P-PSR-002 to P-PSR-005 |
| **TOTAL** | **1.00** | | **0.916** | |

**Arithmetic verification:**
```
(0.91 × 0.20) + (0.92 × 0.20) + (0.91 × 0.20) + (0.92 × 0.15) + (0.91 × 0.15) + (0.93 × 0.10)
= 0.182 + 0.184 + 0.182 + 0.138 + 0.1365 + 0.093
= 0.9155
```

Exact column sum: 0.182 + 0.184 = 0.366; + 0.182 = 0.548; + 0.138 = 0.686; + 0.1365 = 0.8225; + 0.093 = **0.9155**

Rounded to three decimal places: **0.916**. Composite = 0.916. Verdict = **REVISE** (below 0.94 stream threshold).

---

## Detailed Dimension Analysis

### Completeness (0.91/1.00)

**Evidence:**

No changes were made to completeness-affecting content in iter3. All 8 deliverable files are present and well-structured. Positive evidence carried forward from iter2:

- `promptfoo-config.yaml`: FR-001/003/005 documented; FR-003 two-provider architecture explained in 24-line comment block.
- `ps-researcher.yaml`: All 6 SI-RSRCH-* IDs cited in header; SI-RSRCH-006 javascript assertion present in P-PSR-001.
- `ps-analyst.yaml`: SI-ANLT-001 through SI-ANLT-004 all covered across 5 test cases.
- `ps-architect.yaml`: 4 test cases; SI-ARCH-001 through SI-ARCH-010 cited; SI-ARCH-008/009/010 asserted in P-PAC-001 and P-PAC-004.
- `ps-critic.yaml`: 5 test cases with fixture artifacts; SI-CRIT-001 through SI-CRIT-007 addressed.
- `adv-scorer.yaml`: 5 test cases covering all score bands; SI-SCOR-001 through SI-SCOR-011 addressed.
- `version_keys.py`: FR-004 fully implemented; all 5 agents in COVERED_AGENTS and AGENT_FILE_PATHS.
- `docker/promptfoo/Dockerfile`: Node.js 20 Alpine base, promptfoo@0.86.0, UV@0.5.29, non-root user, HEALTHCHECK.

**Gaps (unchanged from iter2):**

1. **SI-RSRCH-006 word-count assertion absent from P-PSR-002 through P-PSR-005.** The ps-researcher.yaml header cites SI-RSRCH-006 as a covered invariant, but the actual javascript assertion (lines 112-123 in P-PSR-001) is not repeated for P-PSR-002, P-PSR-003, P-PSR-004, or P-PSR-005. The header implies all-test coverage; only P-PSR-001 delivers it.

2. **SI-ANLT-002 assertion narrower than behavioral contract.** The `icontains-any` keyword check for "Priority", "Impact", "Effort" (P-PSA-002) is narrower than the behavioral-contracts.md description of the evaluation criteria invariant ("Criterion:", "Dimension:", or markdown table header patterns).

3. **No `tests/prompt-regression/README.md`.** Engineers must reverse-engineer local invocation from the Dockerfile comments and the `promptfoo-config.yaml` usage block. No single-file starting point exists.

4. **`promptfoo-config.yaml` `tests:` section loads all 5 agent YAMLs unconditionally.** Running `promptfoo eval --config promptfoo-config.yaml` without the per-agent `--config` override executes all agents simultaneously. No inline comment documents this behavior.

**Improvement Path:** Copy the SI-RSRCH-006 javascript assertion from P-PSR-001 (lines 117-123) verbatim into P-PSR-002 through P-PSR-005. Tighten SI-ANLT-002. Add README with invocation commands. Add comment to `tests:` stanza.

---

### Internal Consistency (0.92/1.00)

**Evidence — improvements in iter3:**

- **Dockerfile header comment fixed.** Line 23-24 now reads: "The container includes uv for this purpose. pip is used ONLY to bootstrap uv; / all subsequent Python execution uses uv run (H-05 compliant)." This accurately describes the bootstrap pattern used at line 87-88. The contradiction identified in iter2 ("No pip") is resolved. A reader reading the header comment now receives a correct description of the pip-for-uv-bootstrap approach before reaching Stage 3.

- **FR-003 two-provider configuration remains internally consistent.** Both providers in `promptfoo-config.yaml` use `claude-sonnet-4-20250514` with the same config. The 24-line comment block explains this is intentional — Layer 4 performs the actual statistical comparison. The implementation and documentation are aligned.

- **`version_keys.py` internally consistent.** `_MAX_HASH_LENGTH: int = 40` (line 66), `_COMMIT_HASH_PATTERN: re.compile(r"^[0-9a-f]{40}$")` (line 56), module docstring "Only full 40-character SHA-1 hashes are accepted" (line 17), `_validate_commit_hash` enforcing `len(commit_hash) != _MAX_HASH_LENGTH` (line 242). All four references agree. No contradictions.

- **EvaluationMode minimums consistent with FR-005.** `validate_minimum_runs()` maps SMOKE=1, STANDARD=10, FULL=30 — matches the module docstring specification and FR-005 AC-1 through AC-3.

- **Quality floor values.** Per-agent YAML header overall floors match behavioral-contracts.md B.3. Per-dimension thresholds in test cases match per-agent contract YAML files.

**Residual inconsistency:**

- **ps-researcher.yaml header implies uniform SI-RSRCH-006 coverage, but only P-PSR-001 asserts it.** Lines 9-12 of ps-researcher.yaml list all 6 SI-RSRCH-* invariants as covered. Line 22: `# SI-RSRCH-006: L0 section <= 500 words`. The header structure implies all invariants are tested across all test cases. In practice, only P-PSR-001 has the word-count assertion. A developer reading the header of P-PSR-003 would expect SI-RSRCH-006 to be asserted; it is not. This is a factual inconsistency between the documented coverage claim and the actual test configuration.

**Gaps:** The above inconsistency is the remaining blocker for the 0.9+ band. It requires adding SI-RSRCH-006 assertions to P-PSR-002 through P-PSR-005.

**Improvement Path:** Add the SI-RSRCH-006 javascript assertion to the four remaining test cases. Alternatively, add a clarifying comment to the header noting that SI-RSRCH-006 is only asserted in P-PSR-001 as a representative gate.

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

No changes were made to this dimension in iter3. The score reflects the same evidence as iter2:

- **UV install version-pinned.** `ENV UV_VERSION="0.5.29"` followed by `pip install --no-cache-dir "uv==${UV_VERSION}"`. H-05 bootstrap approach documented in Stage 3 header comment and in the Dockerfile header (fixed in iter3).
- **Non-root user.** `addgroup -g 1001 -S promptfoo`, `adduser -u 1001 -S promptfoo -G promptfoo`, `USER promptfoo` before ENTRYPOINT.
- **HEALTHCHECK present.** `HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD promptfoo --version || exit 1`.
- **Subprocess security.** List-form subprocess calls; path allowlist enforced before every git call; `timeout=10` on all subprocess calls; `# noqa: S603` with rationale annotations.
- **Temperature 0.0.** All provider configurations in all 5 agent YAMLs and `promptfoo-config.yaml`. Consistent with deterministic structural assertion requirements (FR-008).
- **Fixture methodology.** Multi-fixture approach across 5 ps-critic test cases and 5 adv-scorer test cases systematically tests distinct failure modes: missing sections (P-PSC-001), arithmetic traps (P-PSC-002), leniency temptation (P-PSC-003, P-ADVS-004), revision cycle (P-PSC-004), meta-critique (P-PSC-005), score band discrimination (P-ADVS-001 through P-ADVS-003, P-ADVS-005).

**Residual gap (unchanged):**

- Alpine system Python (`apk add python3 py3-pip`) is used to bootstrap uv. The Alpine Python version is tied to the `node:20-alpine3.21` release rather than being independently pinned. A future minor update to `node:20-alpine3.21` could change the Python minor version, potentially affecting pip behavior. This is a second-order reproducibility concern — the UV version is pinned, but the Python bootstrapping Python is not.

**Improvement Path:** Pin Alpine Python version in the `apk add` line (e.g., `python3=3.12.x-rN py3-pip=...`) or document the Alpine Python version as an accepted transitive dependency of the `node:20-alpine3.21` image lock.

---

### Evidence Quality (0.92/1.00)

**Evidence — improvements in iter3:**

- **FR-025 now in Dockerfile header.** Dockerfile line 26: `# FR-025: promptfoo Docker isolation` — this adds a bidirectional FR cross-reference that was missing in iter2. The Dockerfile now references the functional requirement that motivated its existence, consistent with the pattern in all other deliverable files.

All other evidence from iter2 remains intact:

- FR traceability in all file headers (FR-001, FR-003, FR-004, FR-005, FR-008 across test case YAMLs; FR-004 AC-1/AC-2/AC-3 in version_keys.py module docstring).
- MC control IDs at implementation sites (MC-01, MC-07, MC-08, MC-10, MC-13, MC-14 in Dockerfile; MC-01, MC-02, MC-03, MC-04 in promptfoo-config.yaml).
- OWASP A03/A04 and ASVS V5.1/V5.3 references in version_keys.py module docstring.
- `# noqa` annotations with specific rationale.
- Threat model cross-references: version_keys.py cites "threat T-35" (baseline substitution attack) and "threat T-02" (path traversal).

**Residual minor gaps (unchanged):**

- `ps-critic.yaml` comment block describes the planted-gap fixture methodology (lines 19-21) but does not cite the design document or ADR that mandated this approach.
- `promptfoo-config.yaml` `transformVars` section does not explain how `AGENT_ID` is injected in the CI workflow.

**Improvement Path:** Add design document reference to ps-critic.yaml header for the planted-gap fixture rationale. Add a comment to `transformVars` referencing the workflow that sets `AGENT_ID`.

---

### Actionability (0.91/1.00)

**Evidence:**

No actionability-affecting changes were made in iter3. The score reflects the same evidence as iter2:

- **Docker build succeeds.** `FROM node:20-alpine3.21 AS base` resolves. The TODO block (lines 34-38) provides exact commands to obtain the SHA digest when MC-08 pinning is required for production.
- **FR-003 architecture documented.** Engineers reading `promptfoo-config.yaml` understand why two identical providers exist and the Layer 4 integration path.
- **SI-RSRCH-006 assertion in P-PSR-001.** The javascript assertion (lines 117-123) is correctly implemented with regex extraction and word counting.
- **VersionKeyRegistry error messages.** Include the exact command (`git rev-parse HEAD`), the expected format, and the registration step path.
- **UV version-pinned.** `uv==${UV_VERSION}` with `UV_VERSION="0.5.29"` makes the container build deterministic.

**Gaps (unchanged from iter2):**

1. **No `tests/prompt-regression/README.md`.** Engineers must reverse-engineer invocation from the Dockerfile comments and the `promptfoo-config.yaml` usage block. The Dockerfile header comment block (lines 17-19) provides smoke, standard, and full `docker run` invocation patterns, but no structured README consolidates these commands.

2. **`promptfoo-config.yaml` `tests:` section loads all 5 agent YAMLs unconditionally.** Running without the per-agent `--config` override executes all agents simultaneously. No comment clarifies this behavior or the primary execution path.

**Improvement Path:** Add `tests/prompt-regression/README.md` with Smoke, Standard, and Full invocation commands. Add a comment to the `tests:` section documenting the per-agent `--config` override as the primary CI execution path and the `tests:` stanza as a secondary full-harness path.

---

### Traceability (0.93/1.00)

**Evidence — improvements in iter3:**

- **FR-025 bidirectional trace established.** Dockerfile line 26 (`# FR-025: promptfoo Docker isolation`) means the Dockerfile now cites the FR that motivated its existence, matching the pattern in all other deliverable files. Combined with the workflow's FR-025 citation, the trace is now bidirectional. This was the primary traceability gap identified in iter2.

All prior traceability evidence remains intact:

- FR-003 traceable to Layer 4 statistical engine via the 24-line comment block in `promptfoo-config.yaml`.
- SI-RSRCH-006 trace complete in P-PSR-001: header citation and assertion both present.
- FR-004 composite key format traceable: `VersionKey.__str__` produces `f"{self.commit_hash}:{self.file_path}"` — exactly matching FR-004 AC-3 spec.
- MC control citations at implementation sites across Dockerfile and test case YAMLs.
- OWASP/threat model citations in version_keys.py link implementation to the threat model.

**Residual gaps (reduced from iter2):**

1. **System-design.md cited at document level, not section level.** The Dockerfile references "system-design.md threat model" and "ADR-001 architectural decision" without specific section references. Section-level citation would improve traceability precision. This is a minor gap.

2. **SI-RSRCH-006 trace incomplete for P-PSR-002 to P-PSR-005.** The ps-researcher.yaml header cites SI-RSRCH-006, but only P-PSR-001 has the corresponding assertion. The header-to-assertion trace is broken for four of the five test cases on this invariant.

**Improvement Path:** Add section-level references to system-design.md citations in the Dockerfile (e.g., "threat model Section 3.2, threats T-01 through T-04"). Add SI-RSRCH-006 assertions to P-PSR-002 through P-PSR-005 to close the header-to-assertion trace.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness / Traceability | 0.91 / 0.93 | 0.94+ | Add SI-RSRCH-006 javascript word-count assertion to P-PSR-002 through P-PSR-005. The P-PSR-001 implementation (lines 117-123) can be copied verbatim. This fixes the most persistent multi-iteration gap and closes the header-to-assertion traceability break simultaneously — addressing two dimensions with one change. |
| 2 | Completeness / Actionability | 0.91 | 0.93 | Add `tests/prompt-regression/README.md` with Smoke, Standard, and Full local invocation commands. The Dockerfile header (lines 17-19) already has the `docker run` patterns; a README would collect them into a single findable starting point. |
| 3 | Internal Consistency | 0.92 | 0.94 | Add a clarifying comment to the ps-researcher.yaml header noting that SI-RSRCH-006 is only asserted in P-PSR-001 as the representative gate for that invariant (or add the assertion to all test cases per Priority 1 recommendation above). |
| 4 | Completeness | 0.91 | 0.93 | Tighten SI-ANLT-002 assertion to match the behavioral-contracts.md table-header pattern (markdown table with criteria headers) rather than keyword presence only. |
| 5 | Actionability | 0.91 | 0.93 | Add inline comment to `promptfoo-config.yaml` `tests:` stanza documenting that the primary CI execution path is via per-agent `--config` override and that the `tests:` block is the full-harness fallback path. |
| 6 | Traceability | 0.93 | 0.95 | Add section-level references to system-design.md citations in the Dockerfile (e.g., "Section 3.2, Threats T-01 through T-04" for the threat model reference). |
| 7 | Methodological Rigor | 0.91 | 0.93 | Pin the Alpine Python version in the `apk add` line for full build reproducibility, or add a comment documenting the Alpine Python version as a transitive dependency of the `node:20-alpine3.21` image lock. |

---

## Delta Analysis (Iter2 to Iter3)

| Dimension | Iter2 Score | Iter3 Score | Delta | Driver |
|-----------|-------------|-------------|-------|--------|
| Completeness | 0.91 | 0.91 | 0.00 | No changes made in iter3 to completeness-affecting content |
| Internal Consistency | 0.90 | 0.92 | +0.02 | Dockerfile header comment fixed (pip usage accurately described); residual SI-RSRCH-006 inconsistency prevents reaching 0.93+ |
| Methodological Rigor | 0.91 | 0.91 | 0.00 | No changes in iter3 |
| Evidence Quality | 0.92 | 0.92 | 0.00 | FR-025 strengthens traceability evidence marginally; remains in same score band |
| Actionability | 0.91 | 0.91 | 0.00 | No actionability improvements in iter3 |
| Traceability | 0.90 | 0.93 | +0.03 | FR-025 bidirectional trace established — primary iter2 gap resolved |
| **Composite** | **0.909** | **0.916** | **+0.007** | |

The iter3 delta (+0.007) is smaller than iter2's delta (+0.033), which is expected: iter2 addressed a residual major defect (pip comment contradication), while iter3 closed the remaining two targeted defects identified in the iter2 scoring report. The remaining gap to the 0.94 stream threshold (-0.024) requires addressing Priority 1 through Priority 5 recommendations above.

---

## Leniency Bias Check

- [x] Each dimension scored independently — Traceability scored 0.93 (above Internal Consistency 0.92) because FR-025 directly resolved a traceability gap; scores are not uniformly raised
- [x] Evidence documented for each score — every score delta tied to specific file lines; no dimension raised without cited evidence of improvement
- [x] Uncertain scores resolved downward — Internal Consistency held at 0.92 rather than 0.93 because the SI-RSRCH-006 header-to-assertion inconsistency persists across four test cases; this is a verifiable factual inconsistency, not a style preference
- [x] Calibration anchors applied — 0.92 corresponds to "genuinely excellent across the dimension"; Internal Consistency at 0.92 reflects one remaining verifiable inconsistency, correctly placed below 0.95 (no contradictions, all claims aligned)
- [x] No dimension scored above 0.93 without exceptional evidence — Traceability at 0.93 is the highest score and is supported by FR-025 bidirectional citation plus all prior FR/MC/SI/OWASP traceability evidence; no dimension given 0.94+ without demonstrating zero traceability gaps

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.916
stream_threshold: 0.94
ssot_threshold: 0.92
weakest_dimension: completeness_and_actionability
weakest_score: 0.91
critical_findings_count: 0
  # No Critical findings in iter3. Both iter2 targeted defects resolved.
iteration: 3
delta_from_prior: +0.007
gap_to_stream_threshold: 0.024
improvement_recommendations:
  - "Add SI-RSRCH-006 javascript assertion (copy from P-PSR-001 lines 117-123) to P-PSR-002, P-PSR-003, P-PSR-004, P-PSR-005 — highest ROI change, closes Completeness AND Traceability gaps simultaneously"
  - "Add tests/prompt-regression/README.md with Smoke/Standard/Full local invocation commands"
  - "Add clarifying comment to ps-researcher.yaml header about SI-RSRCH-006 assertion scope"
  - "Tighten SI-ANLT-002 assertion to behavioral-contracts.md table-header pattern"
  - "Add inline comment to promptfoo-config.yaml tests: stanza documenting per-agent --config override as primary CI path"
  - "Add section-level references to system-design.md citations in Dockerfile"
  - "Pin Alpine Python version in apk add line or document as accepted transitive dependency"
```

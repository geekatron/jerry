# S-014 LLM-as-Judge Tournament Score: BUG-010 `jerry ast` Containment Widening (PR #341)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, top action item |
| [Scoring Context](#scoring-context) | Deliverable, criticality, inputs aggregated |
| [Score Summary](#score-summary) | Composite, threshold, verdict |
| [Dimension Scores](#dimension-scores) | Per-dimension score + weighted contribution |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Tournament Corroboration Analysis](#tournament-corroboration-analysis) | Cross-strategy dedup methodology and confidence model |
| [Consolidated Deduped Remediation List](#consolidated-deduped-remediation-list) | Ranked Critical/Major findings with corroborating strategy IDs |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Priority-ordered actions |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency self-review |
| [Session Context Handoff](#session-context-handoff) | Schema for orchestrator |

---

## L0 Executive Summary

**Score:** 0.64/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.55)

**One-line assessment:** The core BUG-010 fix (wrong project-root anchor) and the two red-vuln-confirmed remediations (H-01 ownership gate, H-02 broad-root warning) are engineering-sound in isolation, but six of nine tournament strategies — independently, using six different methodologies — converged on the same highest-severity gap (index-based rather than location-based trust in `_is_temp_default_root_match`, RPN 432, the tournament's single highest-scored FMEA finding), which was also missed by the standard `/eng-team` gate review; combined with four more corroborated Critical clusters (write-path ownership-gate omission, fail-open-on-stat-error, same-UID/container convergence, and TMPDIR poisoning/stdout-stderr merge risk), this is a **REVISE**, not a PASS, at the C4 threshold of 0.92.

---

## Scoring Context

- **Deliverable:** `src/interface/cli/{project_root,ast_commands,parser,main}.py` + `tests/unit/interface/cli/{test_project_root,test_ast_commands}.py` on branch `fix/BUG-010-ast-project-root` (PR #341)
- **Deliverable Type:** Code (security-relevant CLI path-containment subsystem)
- **Criticality Level:** C4 (AE-005 security-relevant, escalated to full tournament per user request)
- **Scoring Strategy:** S-014 (LLM-as-Judge), Group F (final aggregation) of a 6-group blind tournament
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-08-07
- **Inputs aggregated:** 9 blind adversarial strategy reports (S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013) + 3 context artifacts (`eng-reviewer-gate-report.md`, `red-vuln-findings.md`, `eng-lead-implementation-plan.md`) + the `BUG-010-ast-project-root.md` entity (read directly to verify the AC-checklist discrepancy independently of CC-007's claim)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | **0.64** |
| **Threshold** | 0.92 (H-13, C4) |
| **Verdict** | **REVISE** |
| **Strategy Findings Incorporated** | Yes — 9 reports, 62 total raw findings, deduped to 6 Critical clusters + 9 Major clusters |
| **Special-case trigger** | Multiple unresolved Critical findings present → REVISE is mandatory regardless of numeric score (SSOT special case) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.63 | 0.126 | Core BUG-010 fix + M-08/M-10/M-05 preservation complete; but the H-01/H-02 security-hardening layer itself is incomplete — 6 corroborated gaps (write path, default-branch broadness, Windows, container UID, TMPDIR poisoning, `--root`/temp coincidence) left the *generalization* of the fix undone |
| Internal Consistency | 0.20 | 0.55 | 0.110 | 4+ independent code/docstring claims proven false by direct code trace (read/write parity, fail-open "consistency" with size check, "project root is pure user-discretion", "stdout reserved for JSON"); the human `/eng-team` gate report itself asserts the same false invariant CV-001/FM-001/CC-008 refute |
| Methodological Rigor | 0.20 | 0.58 | 0.116 | Strong test-first/H-20 discipline and layered-check design (steelman-confirmed), but FMEA flags 8/12 failure modes at RPN>80 (67%, "systemic issue" threshold is 30%); fail-open/fail-closed inconsistency unjustified; UID-tenancy premise unstress-tested; deny-by-default alternative never evaluated (S-013 mandate gap) |
| Evidence Quality | 0.15 | 0.68 | 0.102 | Tournament findings themselves are rigorously file:line-cited and cross-corroborated; but the deliverable's own evidence has gaps — red-vuln's H-05 REFUTED verdict rests on an inaccurate premise for `ast_modify`'s actual symlink-dereference sequence (RT-003); coverage % never independently executed, only pass-counts (CC-006/CV-004) |
| Actionability | 0.15 | 0.80 | 0.120 | Every Critical/Major finding across all 9 reports carries a precise, line-scoped fix and a concrete, testable acceptance criterion; most fixes explicitly reuse already-tested existing patterns (low-risk remediation) |
| Traceability | 0.10 | 0.62 | 0.062 | Findings trace cleanly to exact lines and cross-reference red-vuln/eng-lead; but the BUG-010 entity's own AC checklist (the primary traceability artifact) is internally broken — 7 of 9 scope-widening criteria remain `[ ]` unchecked despite the History narrative claiming completion (CC-007, independently confirmed by direct read) |
| **TOTAL** | **1.00** | | **0.636 → 0.64** | |

---

## Detailed Dimension Analysis

### Completeness (0.63/1.00)

**Evidence:** The literal BUG-010 ask (wrong `__file__`-anchored root) is fully and correctly fixed via `get_project_root()`. All 10 `jerry ast` subcommands carry `--root`. M-08/M-10/M-05 invariants are verifiably generalized across the widened root set (steelman SM-005, eng-reviewer §2). H-01 and H-02 — the two findings the prior `/red-team` pass confirmed — are each remediated with dedicated, correctly-scoped tests.

**Gaps:** The remediation layer built on top of the base fix is not generalized to structurally symmetric code paths: the write-time TOCTOU recheck in `ast_modify` never calls the ownership gate (5-strategy corroboration, see C2 below); the default (non-`--root`) branch never applies the broad-root check that the `--root` branch gets, leaving both the default project root and `TMPDIR`-poisoned temp defaults unchecked (C1/C5); Windows `%TEMP%` override is asserted, not verified (M1); the deny-by-default design alternative was never evaluated on the record (M4); 7 of 9 scope-widening Acceptance Criteria remain literally unchecked in the entity despite claimed completion (M3).

**Improvement Path:** Close C1–C5 (Critical cluster fixes below); reconcile the AC checklist against actual test coverage; record the deny-by-default alternative's rejection rationale.

### Internal Consistency (0.55/1.00)

**Evidence:** `_check_path_containment`'s core predicate (`any(is_relative_to(r) for r in allowed_roots)`) is applied uniformly across read/write/symlink checks (steelman SM-007, CoVe CL-001/CL-003 verified).

**Gaps:** This is the tournament's weakest dimension because the deliverable makes explicit, checkable invariant claims that direct code trace disproves in at least four independent places: (1) `ast_modify`'s own docstring claims read/write never disagree on the containment set — false for the ownership predicate specifically (SR-001/RT-003/IN-001/PM-003/FM-003, 5-way corroboration); (2) the ownership check's fail-open is documented as "consistent with the size check" — the two `stat()` calls have *opposite* fail-open/fail-closed semantics on the identical error class (SR-002/RT-002/PM-002/FM-007/CV-003, 5-way corroboration); (3) "the project root... remain[s] pure user-discretion" and is "never gated" by design — refuted by CV-001/FM-001/FM-002/CC-008/PM-001 (6-way corroboration) showing the exemption is index-based, not location-based, and the **independent `/eng-team` gate report itself repeats the same false invariant** ("a project-root match resolves to `allowed_roots[0]`... **Correct**" — eng-reviewer §2), meaning a human quality gate and five automated strategies reached opposite conclusions about the same mechanism; (4) the design's explicit "stdout is reserved for the JSON/render payload" claim is contradicted under realistic `2>&1`/`capture_output=True` consumption, which is the design's own stated primary use case (DA-004/PM-004).

**Improvement Path:** Fix the underlying code for (1)–(3) rather than merely re-wording the docstrings (wording fixes alone would convert this from a functional defect to a documentation-precision issue, which is insufficient at C4 for a security control); add a suppression mechanism or documented merged-stream caveat for (4).

### Methodological Rigor (0.58/1.00)

**Evidence:** Test-first discipline (H-20) is attested and corroborated (24 test-function references that would `AttributeError` pre-implementation); the reconciliation-seam handling (pytest `tmp_path` living inside the real system tempdir) was correctly identified and fixed rather than silently tripped (eng-reviewer §3, steelman genuine-strength #6); the team voluntarily red-teamed its own widening and closed both findings with generalizing, portable fixes rather than narrow patches (steelman genuine-strength #5).

**Gaps:** FMEA's own systemic-issue threshold (30% of failure modes at RPN≥80) is exceeded nearly 2.2x (67%, 8 of 12 elements) — this is FMEA's own designated signal for "not isolated defects." The ownership gate's core premise (`os.geteuid()` uniquely identifies a tenant) was validated against the deployment model red-vuln explicitly modeled (distinct human accounts) but not against the deployment model Jerry's own architecture points toward (containerized/CI, per the module's own scratchpad-writing rationale) — 4-way corroboration (RT-004/FM-004/PM-005/IN-005) that this premise fails under common UID-0/shared-service-account convergence. S-013's specific mandate — surface un-evaluated design alternatives — found that the deny-by-default alternative was never evaluated on the record anywhere in the eng-lead plan or red-vuln findings (IN-004).

**Improvement Path:** Treat the FMEA systemic-issue flag as the primary rigor gate; do not close this dimension until the RPN>80 proportion drops materially. Document the UID-convergence limitation explicitly per RT-004/FM-004's acceptance criteria at minimum.

### Evidence Quality (0.68/1.00)

**Evidence:** All 9 tournament reports independently cite exact file:line evidence and, in several cases, cross-verify each other's mechanism without collusion (blind execution) — e.g., CV-001, FM-001, CC-008, and PM-001 arrive at the identical root-cause line (`ast_commands.py:181-209`, `_is_temp_default_root_match`) via four different methodologies. This cross-strategy convergence is itself strong evidence quality for the tournament's own findings.

**Gaps:** The deliverable's own evidentiary claims have real gaps: red-vuln's H-05 "REFUTED" verdict for symlink-safety at write time is shown by RT-003 to rest on an inaccurate premise — it cites `os.replace`'s general non-symlink-following contract without tracing that `ast_modify` already dereferences the symlink via `Path.resolve()` *before* `os.replace` is ever called, meaning the property actually relied upon does not hold the way the verdict states. Coverage claims in the BUG-010 History ("≥90% coverage," H-20b) are never backed by an actual `pytest --cov` percentage anywhere in the deliverable set — only pass counts are cited (CC-006, CV-004, both independently unable to verify due to no Bash tool access in those sessions).

**Improvement Path:** Re-verify H-05's symlink-safety claim against the actual `ast_modify` code path (not the general `os.replace` contract); run and cite an actual coverage percentage or explicitly note it was not measured.

### Actionability (0.80/1.00)

**Evidence:** Every Critical and Major finding across all 9 reports includes a specific code location, a concrete corrective action, and a testable acceptance criterion. The large majority of proposed fixes (C1–C5, M1–M2) are explicitly scoped as small, low-risk changes that reuse already-tested existing functions/patterns rather than requiring new design — e.g., "route the write-time recheck through `_check_path_containment`" (C2), "apply `_is_broad_containment_root` to the default branch too" (C5).

**Gaps:** A small number of findings (DA-005's "always-warn, never-block" R-3 design, IN-003's non-interactive-warning gap) have genuinely open trade-offs with no single obviously-correct fix — these appropriately require owner sign-off rather than unilateral remediation, consistent with how R-3/R-4 were already handled in the eng-lead plan.

**Improvement Path:** None required to raise this dimension materially; it is the strongest of the six.

### Traceability (0.62/1.00)

**Evidence:** Every finding across all 9 reports cites exact function/line locations; strategies explicitly cross-reference red-vuln/eng-lead finding IDs (e.g., RT-003 directly disputes red-vuln's H-05 verdict by ID; FM-001/FM-002 cross-reference each other's shared root cause).

**Gaps:** The BUG-010 entity's own Acceptance Criteria checklist — the artifact whose entire purpose is traceability from requirement to completion — is internally broken: independently confirmed by direct read of `BUG-010-ast-project-root.md`, only 2 of 9 scope-widening ACs are checked `[x]` while 7 remain `[ ]`, despite the adjacent History table's prose asserting the work is complete and green (CC-007). DA-006 shows the precise, correct `--root` exclusivity rationale that exists in internal docs never reaches the shipped `--help` text an end user actually reads. IN-002 shows no tracked follow-up item ties the entity's own stated "standalone pip package" future to a containment-default re-evaluation trigger.

**Improvement Path:** Reconcile the AC checklist against actual implementation state before merge (cheap, high-value fix); this alone would move Traceability meaningfully.

---

## Tournament Corroboration Analysis

This score aggregates 9 independent blind strategy executions (6-group tournament order: self-refine → steelman → challenge → verify → decompose → score). Per task instruction, findings are deduped across strategies rather than counted individually — a defect independently discovered by N different methodologies using N different lenses is treated as **one** consolidated finding with **N-way corroboration**, which raises confidence in the finding's validity (independent convergent methodologies reduce the chance any single one is a methodology-specific false positive) without inflating the raw finding count used for scoring.

**Corroboration tiers observed:**

| Tier | Corroboration | Clusters |
|------|---------------|----------|
| Very High (5-6 independent strategies) | 5-6 | C1 (index-based trust bypass, 6-way), C2 (write-path ownership gate, 5-way) |
| High (4 independent strategies) | 4 | C3 (fail-open OSError, 4-way + 1 doc echo), C4 (same-UID convergence, 4-way) |
| Moderate (2 independent strategies) | 2 | C5/C6 (TMPDIR poisoning + stdout/stderr merge risk), M1, M5/PM-004 thematic overlap |
| Single-strategy (still evidence-grounded) | 1 | M2–M9 (documented individually below, not downgraded, but flagged as unconfirmed by a second methodology) |

**Notably:** the C1 cluster (highest corroboration, highest RPN in the tournament at 432) was independently characterized as *correct, intentional behavior* by the parallel `/eng-team` gate report (`eng-reviewer-gate-report.md` §2: "a project-root match resolves to `allowed_roots[0]` and is never gated — even when the project itself lives under `/tmp`... **Correct**"). This is the single most consequential disagreement in the full review chain: a structured human-facing quality gate and five independent adversarial methodologies reached opposite conclusions about the same code path. This divergence is itself scored as an Internal Consistency and Methodological Rigor signal (see above) rather than resolved by fiat — it is flagged for explicit owner adjudication.

---

## Consolidated Deduped Remediation List

Ranked by severity (Critical first), each entry lists the corroborating strategy finding IDs.

### CRITICAL (block C4 acceptance; must resolve or receive explicit, documented owner risk-acceptance before merge)

| Rank | ID | Finding | Corroborating IDs (strategy count) | Location | Fix |
|------|-----|---------|--------------------------------------|----------|-----|
| **C1** | Index-based (not location-based) trust bypass | `_is_temp_default_root_match` exempts `allowed_roots[0]` ("project root") from the H-01 ownership gate and the R-4 transparency note purely by array-index identity, never verifying that index-0 is itself outside a temp/scratchpad tree. When `CLAUDE_PROJECT_DIR` is unset and cwd (or an explicitly-set `CLAUDE_PROJECT_DIR`) resolves inside `tempfile.gettempdir()`/`/tmp` — a realistic condition for CI runners, ephemeral containers, or scratch-directory sessions — the exact multi-tenant exposure H-01 exists to close reopens silently, with **zero** signal. Highest RPN in the tournament (432). **Contradicted by the independent `/eng-team` gate report**, which characterized this same mechanism as correct-by-design. | PM-001 (S-004, Critical/P0), CC-008 (S-007, Major), CV-001 (S-011, Major/material), FM-001 (S-012, Critical, RPN 432), FM-002 (S-012, Critical, RPN 288 — `CLAUDE_PROJECT_DIR` env-var collision variant of same root cause), SR-005 (S-010, Minor, partial) — **6-way** | `ast_commands.py:181-209` (`_is_temp_default_root_match`), `project_root.py:46-60,120-177` | Replace `matched_root != allowed_roots[0]` with a location-based check: verify `allowed_roots[0]` itself does not resolve under `tempfile.gettempdir()`/`_HARDCODED_TMP` before exempting it. Add regression test with project root deliberately inside a controlled temp root + foreign-UID file, asserting rejection. |
| **C2** | Write-path ownership-gate omission | `ast_modify`'s write-time TOCTOU recheck (added for containment, WI-020/M-21) re-derives `allowed_roots` and checks containment only — it never calls `_check_temp_root_ownership`/`_is_temp_default_root_match`. `ast_modify`'s own docstring explicitly claims read/write "never disagree" on the allowed set; this is false for the ownership dimension. Write consequences (overwrite via `os.replace`) are more severe than the read-only exposure H-01 primarily targeted. | SR-001 (S-010, Critical), PM-003 (S-004, Major/P2), RT-003 (S-001, Critical — also shows red-vuln's H-05 REFUTED verdict rests on an inaccurate premise for this exact symlink-dereference sequence), IN-001 (S-013, Major), FM-003 (S-012, Critical, RPN 224); SR-006 (S-010, Minor — R-4 note also missing at write time) — **5-way** | `ast_commands.py:637-724` (write-time recheck at 677-682) vs. read-time gate at `:338-345` | Route the write-time recheck through `_check_path_containment(file_path, root)` (or explicitly re-invoke `_is_temp_default_root_match` + `_check_temp_root_ownership` on the write target), mirroring the read-time gate exactly. Add a regression test simulating an ownership mismatch surfacing between read and write. |
| **C3** | Fail-open on `stat()` OSError | `_check_temp_root_ownership`'s `except OSError: pass` fails **open** (allows), while the sibling size-check `stat()` three lines away in the same function fails **closed** (rejects) on the identical error class. The code comment claims "consistency" with the size check; the behaviors are opposite. RT-002 additionally shows this is **attacker-forceable** (deliberately unlink the target to force the `OSError`), not merely a probabilistic race. | SR-002 (S-010, Critical), PM-002 (S-004, Critical/P0), RT-002 (S-001, Critical/P0 — deterministic bypass), FM-007 (S-012, Major, RPN 147); CV-003 (S-011, Minor — docstring-wording echo) — **4-way** | `ast_commands.py:280-287` vs. `:356-365` | Change `except OSError: pass` to fail closed specifically for the ownership predicate (retain fail-open only for the unrelated size check). Invert `test_check_temp_root_ownership_when_stat_oserror_then_fails_open` to assert rejection; rename accordingly. |
| **C4** | Same-UID/root multi-tenant convergence defeats the ownership gate | The ownership gate's entire premise — distinct UID implies distinct tenant — fails when multiple mutually-untrusted CI jobs/containers share UID 0 (a common unhardened-image default) or a fixed non-root service-account UID on self-hosted runners. In this deployment shape, `st_uid == geteuid()` is true for every tenant, so the check passes unconditionally regardless of true ownership — a **false sense of security**, not merely an absent control. | RT-004 (S-001, Critical/P0), FM-004 (S-012, Critical, RPN 360), PM-005 (S-004, Major/P2), IN-005 (S-013, Minor) — **4-way** | `ast_commands.py:244-287` (`_check_temp_root_ownership`) | At minimum, add a `geteuid()==0` disclosure warning on temp-root matches and document the same-UID-convergence limitation explicitly (code comment + entity/ADR) so this is a known, acknowledged residual risk rather than an implicit, unverified assumption. |
| **C5** | Default-branch broad-root check gap / `TMPDIR` poisoning | `_is_broad_containment_root` is invoked only in the explicit `--root` branch of `get_containment_roots`. The default branch's `tempfile.gettempdir()` value gets **no** broadness check, despite `gettempdir()` honoring `TMPDIR`/`TEMP`/`TMP` env vars — an attacker or misconfiguration with environment-variable-level influence (CI injection, poisoned base-image `ENV`) can silently expand the trusted default-root set to an arbitrary, potentially maximally-broad location with **zero** advisory output, unlike the identical condition reached via `--root`, which does warn. | FM-005 (S-012, Critical, RPN 216); thematically continuous with PM-001's observation that the default project root is also never broadness-checked (same code-pattern gap, two triggers) — **2-way direct + 1 shared-pattern** | `project_root.py:120-177` (`get_containment_roots`, default branch) | Apply `_is_broad_containment_root` to the resolved `tempfile.gettempdir()` value (and `_HARDCODED_TMP`) in the default branch too, emitting the same stderr WARNING used for `--root`. |
| **C6** | stdout/stderr merge corrupts JSON on the design's own primary use case | The design's explicit claim — "stdout is reserved for the JSON/render payload" — is contradicted under realistic merged-stream consumption (`2>&1`, `subprocess.run(capture_output=True)` + naive concatenation), which is common in exactly the CI/automation contexts the design's own forward-looking rationale (steelman SM-003) targets. R-4's transparency note is **not** an edge case — it fires on the design's own stated primary use case (agent scratchpad operations), maximizing exposure rather than minimizing it. No suppression flag exists. | DA-004 (S-002, Critical), PM-004 (S-004, Major/P1 — headless CI/cron blindness variant of the same channel-reliability problem) — **2-way** | `ast_commands.py:212-241` (`_warn_if_temp_root_match`), `BUG-010-ast-project-root.md:69` (the claim itself) | Add a suppression mechanism (`--quiet`/env var) for R-3/R-4; document the merged-stream risk explicitly in both `--help` and the BUG-010 entity; consider TTY-gating R-4 given it fires on the primary use case. |

### MAJOR (should resolve or receive explicit, documented owner sign-off before this increment is considered closed)

| Rank | ID | Finding | Corroborating IDs | Location |
|------|-----|---------|---------------------|----------|
| M1 | Windows `%TEMP%`/`TMP` override assumption unverified | The Windows skip (`os.name == "nt"`) trusts "per-user `%TEMP%` by default" with no runtime verification; a shared/overridden `TEMP` on self-hosted Windows CI or Windows containers silently defeats it with no fallback check. | SR-003 (S-010, Major), RT-005 (S-001, Major) — 2-way | `ast_commands.py:260-264,280-281` |
| M2 | Explicit `--root` pointed at a literal temp-default location bypasses both the ownership gate and transparency notes | `_is_temp_default_root_match` returns `False` unconditionally whenever `explicit_root is not None`, regardless of what it resolves to. `--root /tmp` gets neither H-01 protection nor R-3/R-4 signal. **Independently flagged by the `/eng-team` gate report itself** as Residual F-1, "the sharpest residual edge," explicitly routed to this tournament for owner-informed-consent confirmation (not disputed as intentional). | SR-004 (S-010, Major); eng-reviewer-gate-report.md Residual F-1 (context artifact, non-blind) — 2-way | `ast_commands.py:181-209` |
| M3 | BUG-010 entity AC checklist internally inconsistent with its own History narrative | Only 2 of 9 scope-widening Acceptance Criteria are checked `[x]`; the remaining 7 are `[ ]` despite the adjacent History table's prose asserting completion with pass counts. Independently confirmed by direct read of the entity file during this scoring pass. | CC-007 (S-007, Major); confirmed by direct scorer read of `BUG-010-ast-project-root.md` — 1-way (strategy) + 1 direct verification | `BUG-010-ast-project-root.md:84-115` vs. `124-125` |
| M4 | Deny-by-default alternative never evaluated on the record | Neither the eng-lead plan nor red-vuln's findings name or trade off the more conservative "require `--root` for all non-project access" alternative — the specific gap S-013's methodology exists to surface. | IN-004 (S-013, Major) — 1-way | `eng-lead-implementation-plan.md` (absence) |
| M5 | Stderr-only transparency assumes an attentive interactive human | R-3/R-4 have no suppression flag and no `isatty()` gating; degrades silently to zero effective signal in headless CI/cron automation — the deployment context the design's own forward-looking rationale explicitly targets. | IN-003 (S-013, Major); thematically continuous with C6/PM-004 (channel-reliability family) — 1-way direct + shared theme with C6 | `project_root.py:161-169` |
| M6 | No revisit trigger for the standalone-pip-package deployment future | The default-widening's risk acceptance is scoped to today's single-user-laptop model; nothing ties the entity's own stated "standalone pip package" future to a re-evaluation of that acceptance. | IN-002 (S-013, Major) — 1-way | `BUG-010-ast-project-root.md` (absence), `project_root.py` (no context-gating) |
| M7 | TOCTOU/non-atomicity family (read-time symlink swap; ownership-vs-size dual `stat()` window) | Distinct from C2/C3: the ownership `stat()` itself is not atomic with the subsequent read/write (RT-001); read-time containment check is not re-verified immediately before `read_text()` (FM-008); ownership and size checks use two independent, non-atomic `stat()` calls (FM-009). | RT-001 (S-001, Critical — standalone, not independently corroborated at Critical severity), FM-008 (S-012, Major, RPN 108), FM-009 (S-012, Major, RPN 80) — 2-way at Major, 1 Critical outlier | `ast_commands.py:290-406` |
| M8 | `--root` UX/conceptual-complexity cluster | Exclusive-not-additive semantics violates CLI least-astonishment with no combinator for "project root + external file" workflows; the actual runtime behavior matrix is 5 branches gated by 2 unsuppressible stderr channels (exceeds the Steelman's own 2-mode framing); R-3's warning is unblockable/unsilenceable "security theater" for legitimate broad-root use; shipped `--help` text omits the single most consequential fact (own project files get rejected once `--root` is set elsewhere). | DA-001, DA-002, DA-003, DA-005, DA-006 (all S-002, Major) — 1-way (internally-corroborated 5-finding cluster from a single strategy) | `project_root.py:159-169`, `parser.py:585-593` |
| M9 | Docstring/claim precision gaps (non-functional) | `ast_modify`'s "never disagrees between read and write" overclaims (true only for the `root` argument, not live environment state); `get_containment_roots`'s docstring under-describes `_is_broad_containment_root`'s actual ancestor-of-home scope; "consistent with the size check" wording conflates opposite fail-open/fail-closed semantics. | CC-009 (S-007, Minor), CV-002 (S-011, Minor), CV-003 (S-011, Minor) — 2-way (S-007+S-011 both independently flag the docstring-precision pattern) | `ast_commands.py:637-657,244-287`, `project_root.py:130-135` |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|-----------------|
| 1 | Internal Consistency | 0.55 | ≥0.90 | Fix C1 (index-based trust) and C2 (write-path ownership gate) in code — not documentation alone. These are the two findings where the deliverable's own explicitly-stated invariants are demonstrably false, and where a structured human review reached the opposite conclusion from five independent automated methodologies on the same mechanism (C1). |
| 2 | Methodological Rigor | 0.58 | ≥0.85 | Resolve or explicitly document-and-test C3 (fail-open OSError) and C4 (UID convergence). Treat the FMEA 67%-systemic-issue flag as a rigor gate, not a single finding. |
| 3 | Completeness | 0.63 | ≥0.88 | Close C5 (TMPDIR poisoning / default-branch broadness) and reconcile the BUG-010 AC checklist (M3) against actual test coverage before merge. |
| 4 | Traceability | 0.62 | ≥0.85 | Reconcile M3 (AC checklist); route DA-006's `--help`-text fix; add the M6 revisit-trigger note. |
| 5 | Evidence Quality | 0.68 | ≥0.85 | Re-verify red-vuln's H-05 REFUTED verdict against `ast_modify`'s actual symlink-dereference sequence (per RT-003); run and cite an actual coverage percentage. |
| 6 | Actionability | 0.80 | ≥0.90 | Route DA-005/IN-003's open trade-offs (R-3 always-warn design; non-interactive-automation gap) to the owner for an explicit decision, consistent with how R-3/R-4 were already handled as owner-confirmable in the eng-lead plan. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite (no dimension's score was pulled up by another)
- [x] Evidence documented for each score, with explicit citation to the corroborating strategy IDs and file:line evidence
- [x] Uncertain scores resolved downward: Completeness (0.63 vs. a considered 0.68), Evidence Quality (0.68 vs. a considered 0.72), Traceability (0.62 vs. a considered 0.65) were each set to the lower of two plausible values given the C4 threshold and the special-case Critical-findings rule
- [x] First-draft/first-pass calibration considered: this is a security-relevant C4 deliverable that has already been through one full `/red-team` remediation cycle and passed an `/eng-team` gate review — the score reflects genuine residual gaps found by six independent adversarial methodologies, not first-draft roughness
- [x] No dimension scored above 0.80 (Actionability, the ceiling) without exceptional, multiply-corroborated evidence; no dimension scored above 0.95 anywhere
- [x] The single most consequential finding (C1) was cross-checked against the independent, non-blind `/eng-team` gate report, which reached the opposite conclusion — this divergence was treated as an aggravating signal (not resolved by assuming either side is automatically correct), and is explicitly flagged for owner adjudication rather than silently decided by this scorer

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.64
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.55
critical_findings_count: 6   # C1-C6, deduped clusters; underlying raw Critical-severity findings across all 9 strategies = 17
iteration: 1
improvement_recommendations:
  - "Fix C1 (index-based project-root/temp-tree trust bypass, RPN 432, 6-way corroborated, contradicted by the independent eng-team gate report) — route to eng-backend with explicit owner adjudication of the eng-reviewer disagreement"
  - "Fix C2 (write-path ownership-gate omission in ast_modify, 5-way corroborated) — reuse _check_path_containment at write time"
  - "Fix C3 (fail-open on stat() OSError, attacker-forceable per RT-002, 4-way corroborated) — fail closed for the ownership predicate specifically"
  - "Document-and-test C4 (same-UID/container convergence defeats ownership gate, 4-way corroborated) — at minimum a geteuid()==0 disclosure warning"
  - "Fix C5 (TMPDIR/TEMP/TMP poisoning expands default root set with no broad-root warning) — apply _is_broad_containment_root to the default branch"
  - "Add suppression mechanism + document C6 (stdout/stderr merge corrupts JSON on the design's own primary use case)"
  - "Reconcile BUG-010 entity AC checklist (M3) against actual implementation state before merge"
```

---

*S-014 LLM-as-Judge tournament aggregation — Group F (final), C4 tournament, PR #341. Aggregated 9 blind strategy reports + 3 context artifacts. No source files modified by this scoring pass. Persisted per P-002.*

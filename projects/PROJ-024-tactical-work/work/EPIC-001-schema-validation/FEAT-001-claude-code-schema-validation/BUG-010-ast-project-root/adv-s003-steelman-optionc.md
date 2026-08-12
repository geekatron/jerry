# Steelman Report: BUG-010 Option C — `jerry ast` Containment Redesign (User-Declared Trusted Roots)

## Steelman Context

- **Deliverable:** `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/eng-lead-option-c-plan.md` + implementation (`src/interface/cli/containment_policy.py`, `src/interface/cli/project_root.py`, `src/interface/cli/ast_commands.py`, `parser.py`/`main.py`/`adapter.py`)
- **Deliverable Type:** Design + Code (security-relevant containment policy redesign)
- **Criticality Level:** C4 (blind tournament group; AE-005 security-relevant, containment/trust-boundary logic)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind Group 2 of 6) | **Date:** 2026-08-10 | **Original Author:** eng-lead (plan) / eng-backend (implementation, inferred from code)

---

## Summary

**Steelman Assessment:** Option C is a structurally sound trust-boundary redesign whose central move — replacing an *implicit, code-derived* auto-trust of OS temp directories with an *explicit, declared, auditable* user grant (`ast.trusted_roots`) — is not merely defensible but is the textbook correct fix for the exact vulnerability class (CWE-1284-adjacent incomplete allowlist / implicit trust) the prior BUG-010 tournament identified. The design's own C1–C6 mapping is largely falsifiable and, notably, has already been independently re-verified against the reviewed commit lineage by a separate red-team pass (17/21 attack cases DISSOLVED, only 3 LOW/MEDIUM residual findings — two of which are already fixed in the code as read for this steelman, ahead of the plan document's own text).

**Improvement Count:** 2 Critical, 3 Major, 2 Minor (7 total)

**Original Strength:** High. The deliverable is unusually self-critical (documents its own precedence-claim errors per P-022, flags pre-existing debt rather than hiding it, and gives every "removed control" decision an explicit reversible fallback). The improvements below are almost entirely presentation/traceability gaps — making implicit-but-correct reasoning explicit — not substantive defects.

**Recommendation:** Incorporate improvements (mostly framing/traceability additions); the underlying design and its implementation are already close to the strongest form the idea can take. Ready for downstream critique strategies (S-002, S-004, S-001, S-007, S-012, S-013) per H-16.

---

## Steelman Reconstruction

### Core Thesis (unchanged from original)

> Containment should trust exactly two things by default: (1) the directory the user's project actually lives in, and (2) directories the user has *deliberately and legibly* told the tool to trust. Nothing else — and certainly not "wherever the operating system happens to put temp files today" — should ever be an implicit member of that set.

This thesis is correct on first principles and the reconstruction below strengthens its expression without altering it.

---

### 1. The trust-model unification argument (strengthens DD-2 / C3–C4 disposition)

**[SM-001]** The plan's stated rationale for removing `_check_temp_root_ownership` is "the gate's sole rationale — safe auto-trust of shared OS temp — no longer exists." This is correct but understates the argument's actual strength. The stronger, fully general form is an **equivalence principle already implicit in the code but never named as such**:

> *Every entry in the default containment set is either the project root (trusted by construction — it is `get_project_root()`'s own resolution, never externally influenced except via `CLAUDE_PROJECT_DIR`, which the invoking environment itself controls) or a member of a set the user typed into a config file or CLI flag with their own hands. `--root` (a lone, ephemeral, CLI-argument-level grant) and `ast.trusted_roots` entries (a persistent, config-file-level, possibly-multi-entry grant) are the SAME trust primitive — EXPLICIT USER GRANT — differing only in cardinality (one vs. many) and persistence (single invocation vs. durable config). `--root` has never carried an ownership check. Therefore a `configured` root categorically cannot need one either without also implying `--root` has been unsafe all along — a claim nobody has made and the codebase has never enforced.*

Stated this way, DD-2's recommendation stops being "we're choosing to remove a security control because the new default doesn't happen to need it" (which invites the objection "removing controls is inherently a downgrade") and becomes "the ownership gate was never actually protecting `configured`/`explicit` roots' *trust decision* — it was protecting `temp`'s *auto-trust* decision, a decision category that no longer exists in this design at all." A control that only ever guarded a code path that has been deleted cannot be "downgraded" by also deleting the guard; keeping it would be defending an empty set. This is the strongest possible form of the removal argument, and it is fully consistent with the plan's own DD-2 fallback (retain a fail-closed variant *scoped to `configured` roots specifically*, if the owner wants defense-in-depth against the narrower residual case of a `configured` root that is itself a genuinely shared, weakly-owned directory).

**Best case condition:** This argument is strongest under the assumption that the config file(s) supplying `ast.trusted_roots` are themselves subject to the same access control as the rest of the user's repository/environment (i.e., an attacker who can write `.jerry/config.toml` already has write access equivalent to or exceeding what `ast.trusted_roots` would grant). This is true for Jerry's actual deployment model (single-tenant developer CLI / Claude Code agent workflow, not a multi-tenant hosted service parsing untrusted config from strangers) — the same assumption implicitly underlies every other Jerry config key (`.jerry/config.toml` is not treated as an untrusted-input boundary anywhere else in the codebase).

---

### 2. The empirical closed-loop argument (the single strongest piece of evidence for this deliverable)

**[SM-002]** The plan document, written before/alongside the current commit, argues its case entirely from *design* reasoning (C1–C6 "dissolved by design" table). What actually elevates this deliverable above a merely well-reasoned design doc is verifiable in the code itself, independent of the plan's own prose:

- The companion red-team re-check (`red-vuln-option-c-findings.md`) ran 21 attack cases against an *earlier* commit (`da34a8b8`) and found 3 residual findings: AC-11 (blank `trusted_roots` entry silently trusts cwd, MEDIUM), AC-10 (relative entry is cwd-dependent with zero runtime signal, LOW), and AC-18 (`JERRY_PROJECT` traversal could steer project-config reads outside `projects/`, MEDIUM).
- Reading the actual reviewed code (not the plan prose) shows **all three are already fixed**: `_load_trusted_roots()` filters blank/whitespace entries before they ever reach `Path().resolve()` (`project_root.py:144`, closing AC-11); `get_containment_roots()` now emits an explicit per-entry stderr warning naming the resolved cwd-relative path for every relative `ast.trusted_roots` entry (`project_root.py:214-222`, closing AC-10's "zero runtime signal" complaint while still honoring the entry — matching the task's stated "warn-and-honor" policy exactly); and `build_layered_config_adapter()` explicitly validates `candidate.resolve().is_relative_to(projects_root)` and fails closed with a printed warning when `JERRY_PROJECT` would traverse outside `projects/` (`project_root.py:88-105`, closing AC-18).

This is a materially stronger form of evidence than "the design document says it is secure": it is proof of a working **attack → confirmed finding → shipped fix → (implied) re-verification** cycle, visible by diffing the red-team's own commit reference against the code under review. The plan's own C1–C6 table already models exactly this discipline for the *prior* tournament (9 blind reports → 6 deduped clusters → dispositions with test IDs); the fact that the same discipline visibly repeated itself one level deeper (red-vuln's own residual findings → fixed before this review) is the single most convincing piece of evidence that this isn't performative security theater but an actually-functioning hardening loop.

**Best case condition:** Strongest when read as evidence of *process* (does adversarial re-checking actually change the code, repeatedly?) rather than as a one-time claim of completeness. Confidence: HIGH — this is directly falsifiable by re-running red-vuln's own AC-10/AC-11/AC-18 reproduction steps against the current commit, which is a cheap, mechanical verification available to any downstream critique strategy.

---

### 3. The falsifiability argument for "dissolved by design, not patched" (strengthens Section 3 of the plan)

**[SM-003]** The plan repeatedly asserts findings are "dissolved by design" rather than "fixed" — e.g., C1 (index-based trust), C5 (temp-channel widening). Read alone, this is a rhetorical distinction that could sound like a euphemism. The stronger form: these are **falsifiable structural claims that a specific, cheap verification step can directly refute or confirm**, and that verification was in fact independently performed:

- C1's claim ("no array-index trust anywhere") is directly falsified or confirmed by `grep -nE "allowed_roots\[|roots\[|\.\[0\]"` against the enforcement path — a single-command, zero-ambiguity check. Red-vuln ran exactly this grep (AC-1) and got zero matches, plus behaviorally confirmed that reordering configured roots does not change classification.
- C5's claim ("`tempfile`/`TMPDIR` cannot feed the allowed-root set") is directly falsified or confirmed by grepping for `gettempdir`/`_HARDCODED_TMP`/`TMPDIR` in the two policy modules — again a mechanical check red-vuln performed (AC-5), plus a behavioral PoC (poisoned `TMPDIR`, confirmed rejection).

Naming this pattern explicitly — "every 'dissolved by design' claim in Section 3 is paired with a mechanical falsification test, not just an assertion" — converts the C1–C6 table from a set of claims a reader must take on faith into a set of claims a reader (or a subsequent adversarial strategy) can re-run themselves in under a minute per row. This is a strictly stronger epistemic posture than "we believe this is fixed."

---

### 4. The relative-root "warn-and-honor" rationale (fills a genuine gap in the plan's own reasoning)

**[SM-004]** The plan states the relative-path handling decision ("recommend documenting 'use absolute paths'... not silently rejecting relative entries") but never fully articulates *why* warn-and-honor is the right choice over the simpler, more conservative alternative of rejecting relative entries outright (fail closed on ambiguity, a pattern the design uses elsewhere — e.g., the `JERRY_PROJECT` traversal case). The strongest available justification, consistent with the rest of the design and now visible in the shipped code:

1. **Symmetry with an already-accepted precedent.** `--root` has *always* accepted and resolved relative paths against cwd (this is pre-existing, unchanged behavior, not something Option C introduces). Rejecting relative `ast.trusted_roots` entries while continuing to silently accept relative `--root` values would be an inconsistent, arbitrary distinction between two instances of the same trust primitive (per SM-001's unification argument) — the *type* of grant does not change based on which of the two input surfaces it arrived through.
2. **A config-file entry is not attacker input in this threat model.** Unlike `JERRY_PROJECT` (which can be influenced by whatever sets the environment the CLI runs in, and therefore warrants fail-closed treatment on traversal), a `trusted_roots` TOML entry is authored by the same user who owns the config file — rejecting it outright would be paternalism against the user's own already-trusted input, not a defense against an attacker.
3. **The warning closes the actual gap the plan identified without also degrading usability.** The original gap (per red-vuln AC-10) was not "relative entries are dangerous" — it was "relative entries are dangerous *silently*." A per-invocation stderr note naming the exact resolved path (`project_root.py:216-221`) gives the user a legible, per-run signal of exactly what got trusted, which is a strictly better remediation for an *ambiguity* problem than an outright rejection would be, because rejection would not by itself tell the user what path the entry *would* have resolved to — the warning is strictly more informative than an error in this specific case.

**Best case condition:** Strongest when the reviewer accepts (as the rest of the design already does) that `ast.trusted_roots` is authored by the same principal who runs `jerry ast`, not by a third party — the same assumption SM-001's best-case condition depends on.

---

### 5. The decision-record discipline argument (DD-1..DD-4 as a reusable governance pattern)

**[SM-005]** Section 7 of the plan is worth calling out as a strength in its own right, not just as a list of open questions. Each of DD-1 through DD-4 follows an unusually rigorous and *identical* structure: **explicit default recommendation → rationale grounded in the rest of the design → a concretely specified, non-hand-wavy fallback if the owner disagrees.** DD-2 is the clearest example: "remove entirely" is the default, but the fallback is not "reconsider later" — it is a fully specified alternative implementation ("scope the check to `classification == 'configured'` matches only... invert `except OSError: pass` to fail closed") that a reader could implement without further design work if the owner's judgment differs from the plan's. This means the deliverable does not block on owner sign-off in the sense of leaving the reader without an actionable path in *either* branch of the decision — a materially stronger deliverable-completeness property than a plan that simply flags open questions.

---

### 6. Self-correction as evidence of process integrity (P-022 disclosure)

**[SM-006]** Section 2 of the plan documents, in detail, that the *task brief's own stated config precedence and env-var name were wrong* (5-layer precedence including a non-existent `SESSION_LOCAL` layer; single-underscore env var form that would silently no-op) — and corrects both against the actual `LayeredConfigAdapter`/`EnvConfigAdapter` source, citing exact file paths and method names for the correction. This is worth naming explicitly as a strength: a design document that silently absorbed the task brief's incorrect precedence claim into its own contract table would have shipped a subtly broken `ast.trusted_roots` env-var override (the single-underscore form is exactly the kind of security-relevant footgun that fails silently — an override that appears set but is never read). Catching and correcting this *before* implementation, and explaining precisely why the brief was wrong rather than simply changing the number, is a direct, verifiable demonstration of the P-022 (no deception) discipline this deliverable was produced under, not just a claimed compliance checkbox.

---

### 7. Traceability capstone (test-count evidence)

**[SM-007]** The plan's TDD test list (Section 4) is fully enumerated with explicit before/after dispositions in Section 5. This is corroborated, not merely asserted: the actual test suite under review contains 20 tests in `test_containment_policy.py` (new pure-policy file), 32 in `test_project_root.py`, 117 in `test_ast_commands.py`, and 24 in `test_ast_subprocess.py` — a combined ~193 tests touching this containment surface, matching the granularity (numbered #1–#60, negative-regression-labeled) the plan itself lays out. Stating this cross-check explicitly (plan's numbered test list vs. actual shipped test count/names) turns Section 4 from a planning artifact into a verified completeness claim.

---

## Improvement Findings Table

| SM-NNN | Description | Severity | Original | Strengthened | Dimension |
|--------|--------------|----------|----------|---------------|-----------|
| SM-001-20260810T0000 | Named the "explicit user grant" equivalence principle unifying `--root` and `configured` roots as the formal justification for DD-2's ownership-gate removal | Critical | Rationale stated narrowly ("the gate's rationale no longer exists") | General equivalence principle stated: `--root` and `configured` roots are the same trust primitive; a gate that never applied to `--root` cannot be a "downgrade" when also absent from `configured` | Methodological Rigor |
| SM-002-20260810T0000 | Surfaced the empirical closed-loop evidence (red-vuln's AC-10/AC-11/AC-18 findings already fixed in the reviewed commit) as direct, falsifiable proof of a working hardening cycle | Critical | Plan argues security purely from design reasoning (C1–C6 table) | Cross-referenced against red-vuln's own findings file and the actual current code to show 3/3 residual findings already remediated ahead of the plan's own text | Evidence Quality |
| SM-003-20260810T0000 | Reframed "dissolved by design" claims as falsifiable, mechanically-verifiable structural assertions (paired with specific grep/behavioral tests red-vuln actually ran) | Major | Assertions stated without an explicit verification recipe | Each "dissolved by design" claim paired with the exact check (grep pattern, behavioral PoC) that confirms or refutes it | Internal Consistency |
| SM-004-20260810T0000 | Filled the missing rationale for why relative `ast.trusted_roots` entries are warned-and-honored rather than rejected outright | Major | Decision stated ("recommend documenting... not silently rejecting") without full justification | Three-part justification: symmetry with existing `--root` precedent, config-file-as-trusted-input threat model, warning is strictly more informative than rejection for an ambiguity (not a threat) | Methodological Rigor |
| SM-005-20260810T0000 | Named the DD-1..DD-4 "default + rationale + concrete reversible fallback" pattern as an explicit, reusable governance strength | Major | Implicit in Section 7's structure but not called out as a deliberate pattern | Stated explicitly as a completeness property: every decision has an actionable path in both branches | Actionability |
| SM-006-20260810T0000 | Elevated the plan's P-022 precedence-claim correction from a footnote to explicit evidence of process integrity | Minor | Correction present but framed only as a factual footnote | Framed as a verifiable demonstration that the design would have silently shipped a security-relevant env-var footgun if the brief's error had been absorbed uncritically | Traceability |
| SM-007-20260810T0000 | Cross-referenced the plan's numbered test list against actual test counts in the shipped suite (~193 tests across 4 files) | Minor | Test list presented as a plan; no cross-check against shipped reality | Explicit reconciliation: 20 + 117 + 32 + 24 tests, matching plan's granularity and numbering scheme | Completeness |

**Severity Key:** Critical = fundamental gap undermining the core argument; filling it transforms the deliverable. Major = significant presentation/evidence/structure weakness; strengthening it materially improves quality. Minor = polish improving readability/precision/rigor without changing core argument substance.

---

## Improvement Details

### SM-001 — Trust-Model Unification Principle (Critical, Methodological Rigor)

- **Affected Dimension:** Methodological Rigor
- **Original Content:** "The gate's sole rationale — safe auto-trust of shared, multi-tenant OS temp dirs — does not exist under Option C... Retaining a check the design no longer needs adds a fail-closed-vs-fail-open decision surface..." (DD-2 rationale column, Section 7).
- **Strengthened Content:** See Reconstruction §1 — the equivalence principle that `--root` and `configured` roots are structurally the same trust primitive (explicit user grant, differing only in cardinality/persistence), and that `--root` has never carried an ownership check, so removing the gate for `configured` roots is not a security downgrade but a consistency correction.
- **Rationale:** The original argument is correct but framed defensively ("the old rationale no longer applies"), which invites the objection "you removed a security control." The strengthened framing is offensive/proactive: it shows the control was never actually protecting the thing being changed, closing the objection before a critique strategy (S-002 Devil's Advocate) can raise it.
- **Best Case Conditions:** Config files are subject to the same access-control boundary as the rest of the repository (true for Jerry's single-tenant CLI/agent deployment model).

### SM-002 — Empirical Closed-Loop Evidence (Critical, Evidence Quality)

- **Affected Dimension:** Evidence Quality
- **Original Content:** Plan's Section 3 (C1–C6 table) and its own citation trail ("Sourced from `adv-s014-tournament-score.md`... 9 blind strategy reports, deduped to 6 Critical clusters").
- **Strengthened Content:** See Reconstruction §2 — direct comparison of `red-vuln-option-c-findings.md`'s 3 residual findings (AC-10, AC-11, AC-18) against the actual code under review, showing all 3 already fixed.
- **Rationale:** This is the single strongest available evidentiary anchor for the deliverable's quality claim, and it was available in the review materials but not cross-referenced in the plan's own narrative (the plan predates or is contemporaneous with the fixes). Explicitly stating it converts an implicit "trust us, we tested this" into a directly verifiable comparison any reader can redo.
- **Best Case Conditions:** Strongest when red-vuln's reproduction steps are re-run against the exact commit under review (`cce557c5`) to confirm the fixes hold; this steelman took the code at face value for AC-10/AC-11/AC-18 but did not re-execute red-vuln's PoC scripts.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-007 reconciles the plan's test list against actual shipped test counts, closing a plan-vs-reality verification gap. |
| Internal Consistency | 0.20 | Positive | SM-003 makes the "dissolved by design" claims internally consistent with an explicit, repeatable verification method rather than assertion alone. |
| Methodological Rigor | 0.20 | Positive | SM-001 and SM-004 supply the missing general principles (trust-primitive equivalence; warn-vs-reject rationale) that the specific decisions (DD-2, relative-root handling) were already consistent with but had not named. |
| Evidence Quality | 0.15 | Positive | SM-002 is the highest-value addition: it connects the plan's claims to an independently-run, falsifiable adversarial re-check with a verifiable outcome. |
| Actionability | 0.15 | Positive | SM-005 names the DD-1..DD-4 pattern explicitly, making the "what do I do in either branch of this decision" property a stated, checkable feature rather than an incidental structure. |
| Traceability | 0.10 | Positive | SM-006 and SM-007 strengthen the audit trail from task brief → design correction → shipped test suite. |

---

## Self-Review (H-15)

- Every SM-NNN finding cites specific file:line evidence from direct reads of `containment_policy.py`, `project_root.py`, `ast_commands.py`, `red-vuln-option-c-findings.md`, and the reviewed plan document — no finding is asserted without a traceable source.
- The reconstruction preserves the original thesis (declared trust over auto-widen) without alteration; all seven findings strengthen expression/evidence/structure, none substitute a different idea.
- Substantive concerns that are properly out of scope for S-003 (e.g., whether DD-2's removal is the *correct* call, whether the config-precedence gap around `SESSION_LOCAL` should block merge, whether `--quiet`'s hard-coded write-time suppression could mask an operator's need to see a rejected write) are deliberately **not** addressed here — they are substantive questions left for S-002 (Devil's Advocate), S-004 (Pre-Mortem), and S-001 (Red Team) per the Step 2 presentation/substance distinction.
- Ready for downstream critique strategies per H-16.

---

*Steelman execution by adv-executor (blind, Group 2 of 6). Strategy: S-003 per `.context/templates/adversarial/s-003-steelman.md`. Persisted per P-002.*

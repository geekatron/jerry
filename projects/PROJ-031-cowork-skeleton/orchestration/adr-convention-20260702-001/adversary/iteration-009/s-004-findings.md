# Pre-Mortem Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention) + Companion Rule Draft

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, blind-protocol scope |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Expanded evidence for each Critical/Major |
| [Recommendations](#recommendations) | Prioritized mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) |  |

---

## Execution Context

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.10)
**Criticality:** C4
**Date:** 2026-07-06
**Reviewer:** adv-executor (iteration-9, blind protocol — no visibility into other iteration-9/10 findings)
**H-16 Compliance:** The package's own text asserts S-003 (Steelman) is embedded per-option throughout ([ADR lines 65-68](../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md)) and every Options-Considered entry leads with a steelman before critique; treated as satisfied for this iteration per the invoking task's framing.
**Failure Scenario:** It is 2027-07-06. Twelve months after ratification, the ADR identifier convention has quietly failed in ways the package's own extensive residual register (R-1…R-17, R-A/R-B/R-C, PM-009, FM-1…FM-5) never named. New ADR-labeled decision records keep appearing from a source the Migration Plan never audited; a stale duplicate of the "authoritative" rule text confuses a future author; and the convention's own foundational research claim ("no rule anywhere governs ADR location") turns out to have been incomplete on day one. None of this is a re-statement of an already-disclosed residual — each finding below is checked against the full disposition record (`subtraction-pass-notes.md`, ADR Risks R-1…R-17/R-A/R-B/R-C, Pre-Mortem FM-1…FM-5) before being reported.

**Scope note (P-022):** This review is a fresh, blind pass focused specifically on gaps that are **neither prevented nor honestly disclosed** by the current v1.10 package. Given the package has already been through 8 adversarial tournament rounds with an unusually thorough, itemized residual-disclosure discipline, most conceivable gaps are already named (case-fold slugs R-9, out-of-scan locations R-10, L-7 asymmetry R-11, solo-maintainer self-approval R-12, title-slug extraction R-13, frozen-dir collisions R-14, `id:` dedup R-15, L-7 forward-looking scope R-16, concurrent-supersession race R-17, citation staleness R-B, in-place mutation R-C, lint-never-built R-5, promotion-rate n=3 PM-009). None of those are repeated here. The findings below are gaps I verified are **absent** from that register.

---

## Summary

Four findings survive cross-checking against the full residual/disposition record; two are Critical because they undermine the convention's core purpose (collision-free ADR identity via a complete, honestly-scoped producer/enforcement inventory) via a completeness gap in the package's own foundational claims, not a disclosed trade-off. Two are Major process/hygiene gaps in the Migration Plan. **Recommendation: REVISE** — not because the decision (Scheme B) is wrong, but because the "producer fix" and "prior-art survey" scopes that the package repeatedly asserts as complete (M-12's "the producing agent must emit compliant IDs or the convention is defeated at the source"; Context's "no rule anywhere governing ADR identifiers... location") are, on verification, incomplete in ways that are not disclosed anywhere in either deliverable.

---

## Findings Table

| ID | Severity | Failure Cause | Category | Likelihood | Priority |
|----|----------|----------------|----------|------------|----------|
| 004-001 | Critical | A second live, actively-invocable agent (`eng-architect`) explicitly produces Nygard-format ADRs with zero exposure to this convention, zero scheduled fix, and an output path that isn't even named `ADR-*` | Assumption / Process | High | P0 |
| 004-002 | Critical | The research survey's "no rule anywhere governs ADR location" premise is incomplete: a pre-existing, unreferenced pytest architecture-test module already enforces ADR/decision path constraints, and this ADR's own file appears to violate it | Assumption / Technical | Medium | P0 |
| 004-003 | Major | The exact non-compliant ADR grammar/phantom-CLI defects that Migration-Plan M-12 schedules a fix for in `ps-architect.md` are duplicated verbatim in a sibling composition file M-12 never names | Technical | Medium | P1 |
| 004-004 | Major | M-2 (relocate rule content to `.context/rules/adr-standards.md`) has no disposition for the orphaned source draft file, which could persist as a stale, divergent duplicate | Process | Medium | P1 |

---

## Finding Details

### 004-001: A second ADR-producing agent is entirely outside the convention's scope [CRITICAL]

**Failure Cause:** `skills/eng-team/agents/eng-architect.md` (line 22: "Create architecture decision records (ADRs) using Nygard format with security rationale"; line 57: "**ADR Documentation** -- Record key architecture decisions with security rationale" as methodology Step 7) is a live, T4-tier, `model: opus` agent whose explicit, documented job includes producing ADRs. Its **Output Path Resolution** section (`skills/eng-team/agents/eng-architect.md:86-95`) specifies the project-default output path as `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md` — a filename that does **not** begin with `ADR-` and a directory (`engagements/`) that is neither of the two canonical ADR homes this convention defines (`projects/PROJ-NNN-*/decisions/` or `docs/design/`).

**Category:** Assumption (the Migration Plan implicitly assumes exactly one agent — `ps-architect.md` — mints ADRs) / Process (no audit step exists to enumerate all ADR producers before declaring the fix complete).

**Likelihood:** High — `eng-architect` is a routed, documented, currently-invocable agent (see `.context/rules/mcp-tool-standards.md` Agent Integration Matrix, `eng-architect | resolve, query | — | Library/framework security research`), not a hypothetical.

**Severity:** Critical — the Migration Plan's producer-fix row (M-12, ADR lines 542, and the rule draft's [Producer Fixes](../../../design/adr-standards-rule-draft.md#producer-fixes) section) explicitly claims completeness: "the producing agent must emit compliant IDs or the convention is defeated at the source" (singular "the producing agent," scoped only to `skills/problem-solving/agents/ps-architect.md`). The rule draft's Producer Fixes section (lines 213-221) lists exactly three targets: the exemplar template, `skills/architecture/SKILL.md`, and `ps-architect.md`. `eng-architect.md` appears in none of them, and appears nowhere in either deliverable (verified: zero matches for "eng-architect" or "eng-team" in both files). Because `eng-architect`'s default output isn't even named `ADR-*`, its decision records are invisible to L-1 through L-7 (none of which would ever scan or classify them), invisible to the `docs/design/README.md` domain index this convention creates, and invisible to the pre-flight `sort | uniq -d` one-liner. Twelve months out, this is a live, ongoing, un-audited second channel minting Nygard-format decision records that the convention's own collision-safety and discoverability apparatus cannot see, structurally — not because the mechanism is imperfect (as R-1/R-7/R-9/R-13 honestly disclose for the *known* producer), but because this producer was never entered into the register at all.

**Evidence:** `skills/eng-team/agents/eng-architect.md:22,57,86-95`; Migration Plan row M-12 and the "Producer Fixes" section of `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:213-221`; absence confirmed via repo-wide grep for "eng-architect" across both deliverables (zero matches).

**Dimension:** Completeness (the producer-fix inventory is not exhaustive) / Traceability (the register that names every known residual — R-A — names only `ps-architect.md`).

**Mitigation:** Add a Migration-Plan row (parallel to M-12) auditing every agent whose `description`/methodology references "ADR"/"Nygard format" as an output type (a repo-wide grep for `"Nygard format"` plus a manual review of each `agents/*.md` file's Output/Methodology sections is sufficient — no new lint required), starting with `eng-architect.md`. At minimum, disclose this as a named residual (parallel to R-A) rather than silently omitting it, so the "the producing agent must emit compliant IDs" claim is honestly scoped to "the producing agent(s) we found."

**Acceptance Criteria:** Either (a) `eng-architect.md`'s ADR-production language is updated to reference the canonical `ADR-{domain-slug}-NNN` grammar and a `decisions/`-rooted output path, with a tracked Task/Issue parallel to M-12; or (b) the gap is explicitly disclosed as a residual with the same rigor as R-A, and the M-12/Producer-Fixes completeness claim is softened to name its actual scope.

---

### 004-002: The "no existing rule" premise is not fully verified against the repo's own test suite [CRITICAL]

**Failure Cause:** The Context section's foundational claim — "A ps-researcher survey of 11 governance/rules/template/skill/decisions surfaces confirmed there is no rule anywhere governing ADR identifiers, numbering, location, promotion, or superseding" (ADR, Context section) — is the premise the entire convention is built to remedy. A pre-existing, unrelated pytest module, `tests/project_validation/architecture/test_path_conventions.py` (docstring: "These tests enforce the project isolation principle (ADR-003)"), already deterministically enforces a **location**-adjacent rule for decision files: `test_no_deprecated_pattern` (lines 133-165) fails CI if any `.md` file under a project root contains the pattern `docs/decisions/` + `PROJ-` (parametrized at line 139), and its companion `conftest.py` (lines 162-184) and `tests/project_validation/unit/test_path_validation.py` (lines 196-199, 281-285) carry a literal test fixture `ADR-IMPL-001-unified-alignment.md` — an ID family (`ADR-IMPL-NNN`) that appears in neither this convention's 9-family corpus catalog (Context section, family table) nor its canonical/dialect grammar (it is neither a lowercase domain slug nor a member of the closed `{PROJ|EPIC|FEAT|STORY}` dialect set).

More directly: `test_no_cross_project_references` (`tests/project_validation/architecture/test_path_conventions.py:65-101`) fails CI for any `.md` file under a project root (except files named `BUG-*`, or under an `orchestration/` or `reviews/` path segment — `decisions/` is **not** in the exemption list) that contains a `projects/PROJ-{other-NNN}` reference. `ADR-PROJ031-004-adr-identifier-convention.md` itself lives at `projects/PROJ-031-cowork-skeleton/decisions/` (not exempt) and contains verified cross-project citations, e.g. line 747's References-table row 6, `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md`, and line 292's "both verified on disk in `projects/PROJ-001-oss-release/decisions/`" — both of which match the test's `cross_ref_pattern` (`projects/PROJ-(?!031)\d{3}`).

**Category:** Assumption (the "no rule exists" premise) / Technical (two independent, uncoordinated deterministic enforcement mechanisms for overlapping territory).

**Likelihood:** Medium — I have not executed `uv run pytest tests/project_validation/` and cannot certify the test currently fails in CI (this is disclosed as **inference**, not a confirmed run, per P-022); the exemption logic and cross-references are directly verified from source, but whether `projects/` is included in the CI test-discovery path at present, and whether this specific test is currently green, red, or already-known-broken, I did not confirm by execution.

**Severity:** Critical, independent of the pytest execution question — regardless of whether the test currently passes or fails, the survey's completeness claim ("no rule anywhere governing ADR ... location") is verifiably incomplete: a live, CI-relevant, ADR/decision-location-governing mechanism already exists, predates this ADR (its own docstring cites a 2026-01-10 migration, TD-005, months before this ADR's 2026-07-02 creation), and is never discovered, cited, cross-checked, or reconciled anywhere in the ADR, the rule draft, or `projects/PROJ-031-cowork-skeleton/research/adr-convention-standards-research.md` (verified: zero matches for "project_validation" or "test_path_conventions" in the research file). Twelve months out, this is exactly the "neither prevented nor disclosed" failure mode: two governance mechanisms for the same territory (ADR/decision path conventions) evolve independently, with no owner responsible for reconciling them, and an author following this new convention's own citation practice (which the ADR itself models at scale) risks silently tripping the older, undiscovered one — or the older one is already silently broken/ignored, which is itself a governance-integrity gap this package never surfaces.

**Evidence:** `tests/project_validation/architecture/test_path_conventions.py:65-101,133-165`; `tests/project_validation/conftest.py:162-184`; `tests/project_validation/unit/test_path_validation.py:196-199,281-285`; `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:747,292`; absence confirmed via grep for "project_validation"/"test_path_conventions" in `projects/PROJ-031-cowork-skeleton/research/adr-convention-standards-research.md` (zero matches) and in both deliverables (zero matches).

**Dimension:** Evidence Quality (the "no rule anywhere" claim is asserted, not exhaustively verified against the codebase's own test infrastructure) / Methodological Rigor (an 11-surface survey that omits an existing test module governing the exact subject matter).

**Mitigation:** Add `tests/project_validation/` to the research survey's list of surveyed surfaces (retroactively, in a changelog entry, per the package's own P-022 discipline of disclosing corrections rather than silently patching). Determine (by actually running the suite) whether `test_no_cross_project_references` currently passes for `projects/PROJ-031-cowork-skeleton/decisions/*.md`; if it does not, either extend the exemption list to include `decisions/` (with a documented rationale distinguishing ADR provenance-citation from cross-project coupling) or disclose the conflict as a named residual with an owner and cadence, matching the rigor of R-9…R-17.

**Acceptance Criteria:** A stated reconciliation (in the ADR's References or a new Risk entry) confirming either "no conflict — verified by running the suite" or "conflict confirmed and disclosed, with owner and remediation path," replacing the current silence.

---

### 004-003: M-12's producer fix omits a sibling file carrying the identical defect [MAJOR]

**Failure Cause:** Migration-Plan row M-12 cites eleven precise line numbers in `skills/problem-solving/agents/ps-architect.md` for the non-canonical `# ADR-{NUMBER}` title, the non-canonical filename grammar, and the phantom `python3 scripts/cli.py` invocation. A sibling file, `skills/problem-solving/composition/ps-architect.prompt.md`, carries the **same three defect classes** verbatim: a literal `# ADR-{NUMBER}: {Title}` template line (line 210), a worked example instantiating it as `# ADR-042: Use Event Sourcing for agent_delegate History` (line 74), and the identical phantom `python3 scripts/cli.py link-artifact ...` invocation (line 474) that M-12 itself flags as violating H-05 (UV-only) in the `.md` file. M-12's scope, as written, names only `skills/problem-solving/agents/ps-architect.md`.

**Category:** Technical (an uncoordinated duplicate artifact) — whether `ps-architect.prompt.md` is a currently-live, actively-composed prompt surface or a stale pre-refactor remnant is not established by either deliverable; either way it is not accounted for.

**Likelihood:** Medium — the `composition/` directory pattern (`ps-architect.prompt.md` alongside `ps-architect.agent.yaml`) matches Jerry's documented agent-templating/composition tooling (`skills/shared/README.md`), suggesting it may be a real generation input, not dead weight; I did not trace whether anything currently reads/renders it at runtime (labeled as **inference**, not confirmed).

**Severity:** Major, not Critical — even in the worst case (the composition file is live and actually shapes ps-architect's runtime prompt), the failure mode is the same class M-12 already targets and mitigates for the `.md` file; the gap is completeness of the fix's blast radius, not a new mechanism of harm. If the file is dead, it is instead a stale-example hazard for any future author who consults `composition/` to understand the agent.

**Evidence:** `skills/problem-solving/composition/ps-architect.prompt.md:74,210,474`; Migration-Plan row M-12 in `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:542` (scoped explicitly to `skills/problem-solving/agents/ps-architect.md`).

**Dimension:** Completeness / Traceability.

**Mitigation:** Extend M-12's file list (or add a one-line note) to cover `skills/problem-solving/composition/ps-architect.prompt.md` (and verify whether `ps-architect.agent.yaml` needs the same check), so the fix and its verification cover every copy of the defect, not just the one enumerated with line numbers.

**Acceptance Criteria:** M-12 (or a new M-12b) lists `ps-architect.prompt.md` explicitly, or the ADR discloses that the composition file is intentionally out of scope (with a stated reason — e.g., "generated from the `.md` file and regenerated at build time, not hand-maintained").

---

### 004-004: No disposition for the orphaned source draft after M-2's relocation [MAJOR]

**Failure Cause:** Migration-Plan row M-2 states the action as "Author `.context/rules/adr-standards.md` from Deliverable 2 (this ADR's companion draft)" and separately specifies reciprocal cross-link repair between the two deliverables. Neither M-2 nor the rule draft's own Changelog specifies what happens to the **source file itself**, `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`, after its content is copied/moved to `.context/rules/adr-standards.md`. If the source file is left in place (not deleted or clearly re-labeled as historical/superseded), it becomes an orphaned duplicate that will not receive future edits (amendments, lint-rule changes, taxonomy updates) applied to the now-canonical `.context/rules/adr-standards.md` copy, while remaining fully discoverable via search/grep under a plausible-looking filename (`adr-standards-rule-draft.md`).

**Category:** Process (the Migration Plan specifies the forward move but not the disposition of the artifact left behind).

**Likelihood:** Medium — this depends on whether the executor of M-2 thinks to delete/archive the draft; nothing in the plan prompts that step, so its absence is a real, not merely theoretical, gap.

**Severity:** Major — a future author or agent who finds the stale draft (e.g., via a search that surfaces `projects/PROJ-031-cowork-skeleton/design/` before `.context/rules/`) could follow an out-of-date version of the convention (e.g., an already-superseded lint-rule count, a stale changelog) without realizing a newer, canonical copy exists elsewhere — directly undermining the "adoptable, honest convention" purpose by creating exactly the kind of stale-reference confusion this convention exists to eliminate for ADRs themselves.

**Evidence:** Migration-Plan row M-2, `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:530`; absence of any deletion/archival/superseded-marker instruction confirmed by reading the full M-2 row text and the rule draft's Changelog (`projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:237-247`), neither of which mentions the draft file's fate post-move.

**Dimension:** Actionability (M-2 as written is not fully executable without an implicit judgment call) / Internal Consistency (a "convention that models honest citation discipline" leaving a stale duplicate of its own governing text is a self-referential inconsistency).

**Mitigation:** Add one clause to M-2: on relocation, either delete `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (git history preserves it) or replace its content with a one-line pointer + `SUPERSEDED`-style banner to `.context/rules/adr-standards.md`, mirroring the tombstone discipline (D-3/Path-2) this ADR already applies to ADRs themselves.

**Acceptance Criteria:** M-2's action text explicitly disposes of the source file (delete or tombstone-banner), not merely creates the destination.

---

## Recommendations

**P0 (MUST mitigate before acceptance of the *producer/enforcement completeness* claims — the Scheme-B decision itself is not in question):**
- 004-001: Audit all `agents/*.md` files for ADR-production language; add `eng-architect.md` (and any others found) to the Migration Plan with the same rigor as M-12, or explicitly disclose the gap as a residual.
- 004-002: Verify (by running the suite) whether `tests/project_validation` currently conflicts with this ADR's own cross-project citations; disclose the outcome either way, and add the test module to the research survey's known surfaces.

**P1 (SHOULD mitigate):**
- 004-003: Extend M-12 (or add M-12b) to cover `ps-architect.prompt.md`.
- 004-004: Add an explicit disposition clause for the source draft file to M-2.

**P2:** None identified beyond the above; no Minor findings met the bar for inclusion in this blind pass (all candidate Minor/cosmetic observations were either already disclosed in the existing R-1…R-17/R-A/R-B/R-C register or judged not to block the standard's purpose).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | 004-001, 004-002: the producer-fix inventory and the founding "no existing rule" survey are each less exhaustive than claimed |
| Internal Consistency | 0.20 | Negative | 004-004: a convention modeling citation/tombstone discipline leaves its own companion draft's fate unaddressed |
| Methodological Rigor | 0.20 | Negative | 004-002: an 11-surface research survey omitted a live, CI-relevant test module governing the same subject matter |
| Evidence Quality | 0.15 | Neutral | Where I could verify (file+line), findings are grounded in direct citations; 004-002's "does the test currently fail" component is explicitly labeled inference, not confirmed by execution |
| Actionability | 0.15 | Negative | 004-001, 004-003, 004-004 each have concrete, low-cost mitigations (audit + one Migration-Plan row edit each) |
| Traceability | 0.10 | Negative | 004-001, 004-003: the existing residual register (R-A) and Migration Plan (M-12) name only one of at least two/three real artifacts carrying the same defect class |

---

## Execution Statistics
- **Total Findings:** 4
- **Critical:** 2
- **Major:** 2
- **Minor:** 0
- **Protocol Steps Completed:** 6 of 6 (Set the Stage; Declare Failure/Perspective Shift; Generate Failure Causes; Prioritize by Likelihood x Severity; Develop Mitigations; Synthesize and Score Impact)
- **Already-disclosed residuals excluded from this report (verified present in the existing register, not re-reported):** R-1 through R-17, R-A, R-B, R-C, PM-009, and Pre-Mortem rows FM-1 through FM-5 already in the ADR itself.

# Refutation Panel — S-004 Pre-Mortem Analysis (iteration-9), Remediation-Value Lens

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Target report, lens, method |
| [004-001](#004-001-a-second-adr-producing-agent-is-entirely-outside-the-conventions-scope-critical) | Verdict + reasoning |
| [004-002](#004-002-the-no-existing-rule-premise-is-not-fully-verified-against-the-repos-own-test-suite-critical) | Verdict + reasoning |
| [Summary](#summary) | Verified/refuted tally |

---

## Scope

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-004-findings.md` (S-004 Pre-Mortem Analysis, iteration 9).
**Lens:** Remediation-value — would fixing the finding materially change real adoption outcomes, or is it churn (optional polish / already scheduled / would add machinery against the ratified subtraction doctrine)?
**Method:** Read the finding text, then independently read the cited primary-source files (`skills/eng-team/agents/eng-architect.md`, `tests/project_validation/architecture/test_path_conventions.py`, `tests/project_validation/conftest.py`, `.github/workflows/ci.yml`, `pytest.ini`, `.gitignore`) and cross-check against the ADR/rule-draft/subtraction-pass-notes disposition record. Only the two Critical findings (004-001, 004-002) are in scope for this panel; Majors (004-003, 004-004) are out of scope per the task.

---

## 004-001: "A second ADR-producing agent is entirely outside the convention's scope" [CRITICAL]

**Verdict: REFUTED**

**Reasoning:**

1. **The underlying factual citations check out** — `skills/eng-team/agents/eng-architect.md:22` ("Create architecture decision records (ADRs) using Nygard format with security rationale"), `:57` ("ADR Documentation" as methodology Step 7), and `:86-95` (Output Path Resolution, project-default = `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md`) are all verified verbatim. The finding is not fabricated.

2. **But the finding's own evidence undermines its Critical severity.** `eng-architect.md:86-95` defines exactly **one** output-file template, not four — the Workflow Integration section (`:70`, "Outputs: System design document, threat model, architecture decision records, trust boundary diagrams") lists four artifact *types* that are bundled as sections inside the single `eng-architect-{topic-slug}.md` engagement report, not four separately-named files. Because the filename never begins with `ADR-` and the default directory (`engagements/`) is never `projects/*/decisions/` or `docs/design/`, this agent structurally never emits a file that the ADR identifier convention's own [Tier and Scope](../../../design/adr-standards-rule-draft.md#tier-and-scope) claims to govern ("records under `docs/design/`, `projects/*/decisions/`, and the frozen legacy sets"). It is not a non-compliant ADR producer analogous to `ps-architect.md`/`docs/knowledge/exemplars/templates/adr.md`/`skills/architecture/SKILL.md` (the three Producer-Fixes targets, rule-draft lines 213-219) — those three hard-code literal `ADR-{NUMBER}`/`ADR_NNN` patterns that *would* land in the ADR namespace and fail the new grammar. `eng-architect.md` has no comparable defect to fix because it never attempts to write into the ADR namespace at all.

3. **Remediation-value test:** the finding's own Acceptance Criteria (line 66 of the target report) offers two closure paths — (a) rearchitect `eng-architect.md`'s output to emit canonical-grammar `ADR-*` files in a `decisions/`-rooted path, or (b) disclose as a residual. Path (a) is an out-of-scope architectural change to a different skill's output-path design (governed by ADR-output-path-resolution-001, not this ADR), not a fix to the naming convention. Path (b) is documentation-only churn that changes nothing about real adoption of the convention (the convention already carries an extensive, precedented residual-disclosure discipline — R-A through R-17 — and one more line changes no behavior). Auditing "every agent whose description references Nygard format" (the finding's Mitigation) is exactly the kind of expanding-completeness-net audit obligation the subtraction pass explicitly rejected in favor of a single named producer fix (`subtraction-pass-notes.md:58`, "Monotonic growth... unbuildable by a solo maintainer" was the stated reason for cutting 13 of 18 lint rules). Adding a standing "audit all ADR-producing agents" Migration-Plan row re-introduces that same unbounded-audit-surface failure mode this package already paid down.

4. Under the remediation-value lens (default to refuted if uncertain), the fix that would matter (rearchitecting eng-architect's output) is out of scope/orthogonal, and the fix that is in scope (a disclosure line) does not materially change any real adoption outcome, since the agent structurally cannot collide with or evade the convention's scanned surface either way.

---

## 004-002: "The 'no existing rule' premise is not fully verified against the repo's own test suite" [CRITICAL]

**Verdict: REFUTED**

**Reasoning:**

1. **File-level citations verified.** `tests/project_validation/architecture/test_path_conventions.py` exists; `test_no_deprecated_pattern` (lines 133-165) parametrizes over `docs/{research|synthesis|analysis|decisions}/PROJ-` patterns (line 139 confirms `docs/decisions/` + `PROJ-` is one of four parametrized cases); `test_no_cross_project_references` (lines 65-101) checks a `projects/PROJ-(?!{proj_num})\d{3}` pattern with exemptions for `BUG-*` filenames, `orchestration/` and `reviews/` path segments (lines 81-93) — `decisions/` is indeed absent from that exemption list, as the finding states. `conftest.py:143-154` confirms `proj_root`/`project_id` are dynamically discovered against real `projects/PROJ-*` directories, not synthetic fixtures.

2. **But the framing that this is "a rule... governing ADR location" the survey should have found is a stretch.** `test_no_deprecated_pattern`'s docstring purpose (file lines 1-19, "enforce the project isolation principle (ADR-003)") is a **project-isolation / deprecated-legacy-path regression guard**, not an ADR identifier/numbering/location/promotion convention. It blocks a single obsolete string pattern (`docs/decisions/` + `PROJ-`, a pre-project-centric-reorg path style) from reappearing — it does not prescribe where new ADRs should live, does not touch ID grammar, numbering, promotion, or superseding, which is precisely what the ADR's Context section (`ADR-PROJ031-004-adr-identifier-convention.md:95`, "no rule anywhere governing ADR identifiers, numbering, location, promotion, or superseding") claims is absent. A generic pytest architecture-isolation test is not naturally within the scope of an 11-surface survey of "governance/rules/template/skill/decisions surfaces" for ADR *lifecycle* conventions; treating a code-test module targeting an unrelated legacy path pattern as a rival "location-governing mechanism" over-reads the test's actual purpose.

3. **The `test_no_cross_project_references` conflict claim is explicitly self-labeled as unconfirmed inference by the finder** ("Likelihood: Medium — I have not executed `uv run pytest`... this is disclosed as inference, not a confirmed run" — target report line 78). Independent verification here: `.gitignore` (repo root) does **not** exclude `projects/`, `pytest.ini:3` sets `testpaths = tests` (whole suite), and `.github/workflows/ci.yml:295-303` runs `uv run pytest -m "not llm and not subprocess"` with no path restriction, so the test module is plausibly collected in CI. However, the ADR file (`ADR-PROJ031-004-adr-identifier-convention.md`) is a tracked, previously-committed file (git status shows `M`, not untracked) that has already been through 8 prior adversarial tournament rounds including an S-011 Chain-of-Verification pass explicitly focused on citation integrity (target ADR's own tag glossary at line 65 lists `CV-*` = chain-of-verification), and none of those passes flagged a CI-breaking test failure. Combined with the conftest.py's own comment (`conftest.py:146`, "e.g., in CI where the `projects/` directory is gitignored") suggesting the fixture's authors anticipated this exact test being routinely skipped for most projects, there is real, unresolved uncertainty about whether this test currently fires against this file at all — exactly the condition under which the remediation-value lens instructs default-to-refute.

4. **Remediation-value test:** even granting the cross-project-citation observation is technically accurate, the "fix" is an edit to an unrelated, pre-existing, ADR-003-era project-isolation test's exemption list (add `decisions/` alongside the already-exempted `reviews/`/`orchestration/`) — a change to a different governance mechanism, not to the ADR identifier/naming/promotion convention this package defines. That fix would not change how anyone adopts or follows the naming convention; at most it prevents an unrelated CI assertion from firing on citation-heavy documents, which is either (a) already true today for this file with no observed ill effect across 8 review iterations, or (b) a test-infrastructure bug to be fixed independently of this ADR. Either way, retroactively adding "add `tests/project_validation` to the surveyed-surfaces list" (the finding's Mitigation) is pure documentation/changelog churn that does not change the convention's real-world behavior, and extending or reconciling an unrelated test's exemption list is exactly the kind of expanding-audit-scope response the subtraction doctrine was adopted to stop.

---

## Summary

| Finding | Verdict | Basis |
|---|---|---|
| 004-001 | REFUTED | Citations accurate but agent's actual default output never enters the ADR namespace (no `ADR-*` filename, no `decisions/`/`docs/design/` path) — no comparable defect to the named Producer-Fixes targets; only available remediations are out-of-scope architecture change or no-op disclosure churn. |
| 004-002 | REFUTED | Cited pytest module governs project-isolation/deprecated-path regression, not ADR identifier/location/promotion; the specific cross-project-citation conflict claim is self-labeled inference, unconfirmed after 8 prior review passes including a dedicated citation-verification (S-011) pass; remediation would edit an unrelated test's exemption list, not the naming convention itself. |

*No subagents spawned (P-003). Scope confined to this iteration's mandate (P-020). All claims cite file+line; unverifiable/inference-based claims from the target report are flagged as such above (P-022).*

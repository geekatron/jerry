# Factual-Accuracy Refutation Panel — S-004 Pre-Mortem Analysis (iteration-9)

> Lens: factual accuracy. Target report: `s-004-findings.md` (iteration-9). Scope: Critical findings only (004-001, 004-002). Verdict = VERIFIED or REFUTED per finding, with file+line citations from direct re-reads of the current deliverables and the disposition/residual register.

---

## 004-001: A second ADR-producing agent is entirely outside the convention's scope [CRITICAL]

**Verdict: VERIFIED**

**Reasoning:** `skills/eng-team/agents/eng-architect.md` lines 22, 57, and 86-95 were re-read directly and match the finding's citations exactly: line 22 reads "Create architecture decision records (ADRs) using Nygard format with security rationale"; line 57 reads "**ADR Documentation** -- Record key architecture decisions with security rationale" (Architecture Design Process step 7); and lines 86-95 ("Output Path Resolution") specify the project-default path as `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md` (line 92) — a non-`ADR-*` filename in a non-canonical `engagements/` directory. Grep of both deliverables (`ADR-PROJ031-004-adr-identifier-convention.md` and `adr-standards-rule-draft.md`) for "eng-architect" and "eng-team" returns zero matches, confirming the omission. Migration-Plan row M-12 (ADR line 542) and the rule draft's Producer Fixes section (`adr-standards-rule-draft.md:213-221`) name only `skills/problem-solving/agents/ps-architect.md` as the producer to fix, and the disclosed residual R-A (`ADR-PROJ031-004-adr-identifier-convention.md:692`) likewise scopes the producer-non-compliance residual exclusively to `ps-architect.md`. This is therefore not a restatement of R-A or any R-1..R-17/R-B/R-C entry — it is a genuinely undisclosed second producer, and the citations check out at every cited location.

---

## 004-002: The "no existing rule" premise is not fully verified against the repo's own test suite [CRITICAL]

**Verdict: VERIFIED** (with one noted sub-citation inaccuracy that does not undermine the core claim)

**Reasoning:** The core chain of evidence checks out. `tests/project_validation/architecture/test_path_conventions.py` docstring (lines 4-19, re-read directly) states "These tests enforce the project isolation principle (ADR-003)" and carries a Migration History note dating it to 2026-01-10 (TD-005) — predating the ADR's 2026-07-02 creation, exactly as claimed. `test_no_deprecated_pattern` (lines 133-165) is parametrized with the `docs/decisions/` + `PROJ-` deprecated-path case at line 139 exactly as cited, and fails CI on that pattern. `test_no_cross_project_references` (lines 65-101) uses `cross_ref_pattern = re.compile(rf"projects/PROJ-(?!{proj_num})\d{{3}}")` (line 75) and exempts only `BUG-*` filenames, `orchestration/` path segments, and `reviews/` path segments (lines 81-93) — `decisions/` is confirmed NOT exempt. Re-reading `ADR-PROJ031-004-adr-identifier-convention.md` (which itself lives at `projects/PROJ-031-cowork-skeleton/decisions/`, none of the three exemptions applying to its own path), line 747's References-table row 6 cites `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md` and line 292 cites "both verified on disk in `projects/PROJ-001-oss-release/decisions/`" — both verified present at the cited lines and both match the cross-ref regex (030 and 001 both `!= 031`). Grep of `projects/PROJ-031-cowork-skeleton/research/adr-convention-standards-research.md` and both deliverables for "project_validation"/"test_path_conventions" returns zero matches, confirming the research survey never discovered this pre-existing enforcement mechanism. `conftest.py`'s dynamic project-discovery fixtures (lines 32-139, re-read directly) confirm the test suite auto-discovers every `PROJ-*` directory including PROJ-031, so this is not a hypothetical scan-path gap.

**One sub-citation inaccuracy, disclosed for completeness:** the finding states that "its companion `conftest.py` (lines 162-184) and `tests/project_validation/unit/test_path_validation.py` (lines 196-199, 281-285) carry a literal test fixture `ADR-IMPL-001-unified-alignment.md`." Direct re-read of `conftest.py:162-184` (and a full-file grep for "ADR-IMPL") shows this string does **not** appear anywhere in `conftest.py` — those lines contain only the `old_path_pattern`/`project_path_pattern`/`deprecated_patterns` regex fixtures. The literal fixture string is real, but it exists **only** in `test_path_validation.py` (confirmed at lines 198, 283-284, within the cited 196-199/281-285 ranges). This is a genuine misattribution of one supporting detail to the wrong file. It does not change the finding's central, independently-verified claim (a live, CI-relevant, pre-existing test module governs ADR/decision-file location conventions and was never discovered by this ADR's foundational research survey, and the ADR's own citations plausibly trip that module's cross-project check) — that claim is verified on its own evidence independent of the conftest.py mis-citation.

---

## Summary

| ID | Verdict |
|----|---------|
| 004-001 | VERIFIED |
| 004-002 | VERIFIED (minor sub-citation inaccuracy noted: conftest.py does not carry the "ADR-IMPL-001" literal fixture; only test_path_validation.py does) |

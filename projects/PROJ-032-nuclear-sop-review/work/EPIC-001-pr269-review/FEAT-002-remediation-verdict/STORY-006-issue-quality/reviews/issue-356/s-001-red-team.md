# Red Team Report: GitHub Issue #356 (BUG-007 / REM-07 — nuclear-sop command gating)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `issue-356.md` (final snapshot, GH issue #356, geekatron/jerry)
**Criticality:** C4 (tournament member)
**H-16 Compliance:** N/A for this blind lane — steelman not supplied to this executor; findings below treat the current text as the strengthened artifact under review per orchestrator instructions.
**Threat Actor:** PR #269's external contributor (or their AI agent), reading only this issue text, with zero Jerry-governance context and no browsing of internal review artifacts beyond what the text links.

## Summary

The text is factually accurate against ground truth (block-list contents, echo-into-logs behavior, and the "duplicates a deterministic engine" claim all verify against the actual `sop-executor.md` guard and the repo's `SecurityEnforcementEngine`). The design question is self-contained and jargon-light. Two Major gaps threaten actionability: the "deterministic security enforcement engine" is never named or located, forcing a codebase search; and the one internal path lacking a branch qualifier (in a sentence whose sibling path has one) risks a dead link for a reader working from `main`. Recommendation: ACCEPT with two targeted text fixes.

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| S-001-01 | Unnamed/unlocated "deterministic security enforcement engine" forces a repo-wide search | Ambiguity | High | Major | P1 | Missing | Actionability |
| S-001-02 | Branch-qualifier inconsistency: sibling internal paths in the same sentence, only one carries `on branch feat/proj-032-nuclear-sop-review` | Boundary | Medium | Major | P1 | Partial | Resolvable references |
| S-001-03 | Design question omits two named AC sub-items from the underlying bug (PLAYBOOK "primary mitigations" mislabel; narrowing sop-brief/sop-capture Bash grants) — a contributor could satisfy the visible text and still fail re-review | Rule circumvention | Medium | Minor | P2 | Partial | Completeness |
| S-001-04 | Strained sentence construction ("a deterministic security enforcement engine this duplicates, weaker, at the prompt level") | Degradation | Low | Minor | P2 | N/A | Concision |

## Finding Details

### S-001-01: Deterministic enforcement engine referenced but not located [MAJOR]

**Attack Vector:** The text says "the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level" and later "delegation to the existing deterministic enforcement engine" — as the second of three named design options — without a name, module, or path. An agent trying to act on this text alone must grep the entire repository to find it.
**Exploitability:** High — this is the literal next action any competent agent/contributor takes, and it is not free (the term is generic enough that "security enforcement" alone is not a reliable search key).
**Evidence:** Deliverable lines 5–7 (this repo does in fact ship `src/infrastructure/internal/enforcement/security_enforcement_engine.py`, class `SecurityEnforcementEngine`, exercised by `tests/unit/enforcement/test_security_enforcement_engine.py` — verified directly in the PR worktree). The issue names none of this.
**Dimension:** Actionability
**Countermeasure:** Add a parenthetical, e.g.: "...delegation to the existing deterministic enforcement engine (`src/infrastructure/internal/enforcement/security_enforcement_engine.py`, `SecurityEnforcementEngine`)."
**Acceptance Criteria:** Text names a concrete, greppable identifier or path for the engine.

### S-001-02: Inconsistent branch qualification on sibling internal paths [MAJOR]

**Attack Vector:** The Tracking line cites two internal paths in one sentence family: `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` (no branch stated) and `.../STORY-004-remediation/` "on branch `feat/proj-032-nuclear-sop-review`" (branch stated). A reader who checks out `main` (the normal default) and follows the first path with no branch cue has no signal it is branch-scoped; they may reasonably assume it lives on `main` like everything else referenced without a branch tag, and hit a missing path.
**Exploitability:** Medium — depends on whether the reader tries the Worktracker path at all, but the self-inconsistency (one path qualified, its neighbor not) is itself evidence the omission is an error, not a deliberate signal that the first path is branch-independent.
**Evidence:** Deliverable line 10, both clauses of the "Tracking" paragraph.
**Dimension:** Traceability
**Countermeasure:** Apply the same branch qualifier to both paths, or state the branch once for the whole Tracking sentence (e.g., "All paths below are on branch `feat/proj-032-nuclear-sop-review`.").
**Acceptance Criteria:** Every internal repo path in the Tracking line either resolves on `main` or carries an explicit branch qualifier.

### S-001-03: Design question silently narrower than the underlying acceptance criteria [MINOR]

**Attack Vector:** The public design question asks for a gating model and injection-screening scope. The linked register's redesign question (and the worktracker bug's own acceptance criteria) additionally require: correcting PLAYBOOK.md's claim that names SEC-001/002 "the primary mitigations" (SR-06 human review is actually primary), and dropping/narrowing the Bash grants on `sop-brief`/`sop-capture`. A contributor who answers only the two visible sentences produces a PR that fails re-review against criteria they never saw in the issue itself.
**Exploitability:** Medium — only manifests if the contributor does not also read the linked register (plausible, since S-001-02 may block that link).
**Evidence:** Compare deliverable lines 7 (question) against remediation-register.md REM-07 redesign question ("Correct PLAYBOOK's mitigation-hierarchy claim...") and BUG-007's Acceptance Criteria (Bash-grant narrowing item).
**Dimension:** Completeness
**Countermeasure:** Add one clause to the design question: "...and correct PLAYBOOK's claim that machine screening is the primary mitigation (human review is), and right-size the Bash grants on the brief/capture agents to their actual read-only needs."
**Acceptance Criteria:** Design question text enumerates all sub-items the linked bug will be re-reviewed against, not a subset.

## Recommendations

- **P1:** S-001-01 — name/locate the deterministic engine. S-001-02 — fix branch-qualifier inconsistency across both internal paths.
- **P2:** S-001-03 — fold the two omitted AC sub-items into the visible design question. S-001-04 — tighten the "duplicates, weaker" sentence for clarity (e.g., "this is a bespoke, weaker prompt-level copy of it").

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-001-03: visible ask narrower than the actual re-review bar |
| Internal Consistency | 0.20 | Negative | S-001-02: sibling paths inconsistently branch-qualified |
| Methodological Rigor | 0.20 | Neutral | Core claims (block-list gaps, log echo, engine duplication) verified accurate against source files |
| Evidence Quality | 0.15 | Positive | Specific commands (`nc`, `python -m http.server`) and mechanism (verbatim log echo) are concrete and verified |
| Actionability | 0.15 | Negative | S-001-01: unnamed alternative solution forces a repo search before the contributor can even evaluate option 3 |
| Traceability | 0.10 | Negative | S-001-02: one of two cited paths cannot be traced without branch context |

**Attack vectors found:** 4 (2 Major, 2 Minor). No Critical vectors — the text's factual claims all verified true against the sop-executor.md guard, the register, and the repo's SecurityEnforcementEngine. **Overall assessment:** ACCEPT with targeted revision (P1 items).

---
*S-001 execution complete. Findings feed S-014 dimensional scoring per Integration protocol.*

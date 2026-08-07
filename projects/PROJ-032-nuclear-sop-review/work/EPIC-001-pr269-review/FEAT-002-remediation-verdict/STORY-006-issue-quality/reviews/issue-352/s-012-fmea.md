# FMEA Report: GitHub Issue #352 (BUG-003 / REM-03)

**Strategy:** S-012 FMEA (adapted for a ~300-word communication artifact)
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-352.md`
**Criticality:** C4 (tournament)
**H-16 Compliance:** N/A for this executor invocation (tournament strategy run independently per orchestration plan)
**Elements Analyzed:** 5 | **Failure Modes Identified:** 3 | **Total RPN:** ~412

## Summary

Decomposed the issue into 5 elements (Title, Assignees, Body ¶1 "what this is about", Body ¶2 "design question", Tracking footer). Core factual claims (verifier authority inversion, self-declared risk level, undocumented/inert SHA-256 tamper control) check out cleanly against `remediation-register.md` REM-03. Two real defects found: a resolvability gap in the Tracking footer (Critical, RPN 252) and a self-containment violation in the Title (Major, RPN 100). Recommendation: targeted text fix, not a rewrite.

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action |
|----|---------|-------------|---|---|---|-----|----------|-------------------|
| S-012-01 | Tracking footer | Branch qualifier attached only to the "Full analysis" path, not to the "Worktracker:" path — a reader/agent resolving the worktracker path against `main` (or the PR's own branch `proj-0039-nuclear-engineer`) will 404, since this content lives only on `feat/proj-032-nuclear-sop-review` | 6 | 7 | 6 | 252 | Critical | Append the branch qualifier to the worktracker path too, or better, replace both bare paths with full resolvable GitHub URLs on the stated branch |
| S-012-02 | Title | Title opens with unexplained internal tracker prefix `PROJ-032/BUG-003:` — contradicts this exact issue's own documented design goal (verdict L1/Phase 4: "Issues #350–#356 were... rewritten and retitled to be self-contained... because the PR audience has no Jerry-governance context") | 5 | 10 | 2 | 100 | Major | Drop the `PROJ-032/BUG-003:` prefix from the title; keep `(trust anchor, PR #269)` and the plain-language description, which already stand alone |
| S-012-03 | Body ¶1 (tamper claim) | No specific file citation for "the documentation claims... SHA-256 tamper detection" — register attributes this to `PROCEDURE_STATE.template.yaml` and `docs/reference.md` specifically; issue is silent on where | 3 | 10 | 2 | 60 | Minor | Add "(see `PROCEDURE_STATE.template.yaml`, `docs/reference.md`)" after the claim, or rely on the linked register (acceptable if word budget is tight) |

## Finding Details

### S-012-01: Unresolvable worktracker reference (Critical, RPN 252)

**Element:** Tracking footer, first path reference.
**Failure Mode:** Ambiguous / Incorrect (by omission) — resolvable-reference criterion.
**Effect:** The sentence "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper` (register section REM-03)." carries no branch or repo qualifier. The very next sentence attaches "on branch `feat/proj-032-nuclear-sop-review`" only to the *second* path (`remediation-register.md`'s directory). Verified: this worktracker directory exists in the current checkout of `feat/proj-032-nuclear-sop-review` (confirmed via glob) but the branch is not yet merged to `main` (per git status, all recent commits are on this feature branch) and is distinct from PR #269's own branch (`proj-0039-nuclear-engineer`, per the verdict doc header). An external contributor or their agent trying to open this path from the PR's branch or from `main` gets nothing.
**S/O/D rationale:** S=6 (misdirects navigation, not deliverable-invalidating); O=7 (near-certain to be hit — it's the first thing a curious reader clicks); D=6 (a careful reader might infer both paths share the branch, but nothing in the text guarantees it).
**Corrective Action:** Restate as one sentence covering both paths, e.g.: "Both paths below are on branch `feat/proj-032-nuclear-sop-review` of `geekatron/jerry`: Worktracker `...BUG-003-trust-boundary-state-tamper/` (register section REM-03); full analysis `remediation-register.md` in `.../STORY-004-remediation/`." Ideally render as clickable `https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/...` URLs rather than bare relative paths.
**Acceptance Criteria:** Every path in the Tracking footer either (a) is a full URL including org/repo/branch, or (b) is covered by a single branch statement that unambiguously applies to all paths in the footer.
**Post-Correction RPN estimate:** ~48 (D drops to 2 once explicit).

### S-012-02: Title violates the issue's own self-containment mandate (Major, RPN 100)

**Element:** Title.
**Failure Mode:** Incorrect (deviates from the applicable design rule) — self-containment criterion.
**Effect:** `# GitHub issue #352: PROJ-032/BUG-003: nuclear-sop — verifier takes its criteria from the file it polices (trust anchor, PR #269)`. The mission for this artifact, and the verdict document's own Phase-4/self-review record, explicitly state issues #350–#356 (which includes #352/BUG-003) were "rewritten and retitled to be self-contained" specifically because "the PR audience has no Jerry-governance context." `PROJ-032/BUG-003` is exactly the kind of unexplained internal code (a worktracker project ID + bug ID pair) that mandate was written to eliminate from the title. The rest of the title (after the internal prefix) is already fully self-contained and does not need it.
**S/O/D rationale:** S=5 (first thing read, sets tone, but body still explains everything); O=10 (present in every render of this title); D=2 (trivially spotted by inspection).
**Corrective Action:** Title becomes: `# nuclear-sop: verifier takes its criteria from the file it polices (trust anchor, PR #269)`. Keep the internal `BUG-003`/`REM-03` identifiers only in the Tracking footer, where they are already properly scoped as maintainer cross-references.
**Acceptance Criteria:** Title contains zero bare internal tracker codes (`PROJ-NNN`, `BUG-NNN`, `REM-NN`, strategy/principle IDs); all such identifiers appear only in the Tracking footer.
**Post-Correction RPN estimate:** 0.

## Recommendations (priority order)

1. **S-012-01 (Critical, RPN 252):** Fix the branch-qualifier gap in the Tracking footer before this issue is posted/updated — this is the one finding that could send a reader to a dead link.
2. **S-012-02 (Major, RPN 100):** Strip `PROJ-032/BUG-003:` from the title to match the self-containment standard this issue is explicitly supposed to meet.
3. **S-012-03 (Minor, RPN 60):** Optional — cite the two specific files backing the tamper-detection claim, budget permitting.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-012-01: footer omits the branch scope needed to actually locate the worktracker item |
| Internal Consistency | 0.20 | Negative | S-012-02: title contradicts the artifact's own stated design rule for these issues |
| Methodological Rigor | 0.20 | Neutral | Core claims (authority inversion, self-declared risk, inert tamper control) are faithfully derived from REM-03 |
| Evidence Quality | 0.15 | Neutral/Minor Negative | S-012-03: tamper claim lacks inline file citations |
| Actionability | 0.15 | Negative | S-012-01 directly blocks an agent from locating the referenced worktracker artifact |
| Traceability | 0.10 | Positive | Register section (REM-03) and branch are named for the analysis path, just not consistently for both paths |

## Execution Statistics
- **Total Findings:** 3
- **Critical:** 1
- **Major:** 1
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5

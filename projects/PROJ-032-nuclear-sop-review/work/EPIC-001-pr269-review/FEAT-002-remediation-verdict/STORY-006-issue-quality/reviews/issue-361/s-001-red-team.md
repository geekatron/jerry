# Red Team Report: GitHub issue #361 (BUG-012 / REM-12)

**Strategy:** S-001 Red Team Analysis (adapted for a ~300-word communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-361.md`
**Threat Actor:** An external contributor (or their coding agent) with zero knowledge of this repo's internal governance, trying to act on this issue text alone — motivated to either dismiss the fix wrongly or waste time chasing unresolvable/ambiguous references.

## Summary

Every substantive factual claim in issue #361 (the three-defect state-machine/completion-contract bug, the fix description, the commit hash, the CI link, and the cluster/worktracker cross-references) checks out against the remediation register, remediation log, and the full `c07033ce` diff. No Critical findings. Two Major findings on actionability/resolvability (an unscoped verification command, and an ambiguous branch qualifier on the worktracker path) and three Minor polish items. **Recommendation: ACCEPT with two targeted text fixes.**

## Findings Table

| ID | Finding | Severity | Section |
|----|---------|----------|---------|
| S-001-01 | Verification `git diff` is unscoped to this defect | Major | How to verify |
| S-001-02 | Branch qualifier ambiguous for worktracker path | Major | Tracking |
| S-001-03 | "SEC-008" cited as an unexplained bare code | Minor | What was wrong (3) |
| S-001-04 | Three defects packed into one dense paragraph | Minor | What was wrong |
| S-001-05 | Title front-loads internal tracking codes | Minor | Title |

## Finding Details

### S-001-01: Verification command surfaces all 7 unrelated fix clusters

**Evidence:** "`git diff c07033ce^ c07033ce -- skills/nuclear-sop/`" — but `c07033ce` is a single commit implementing all seven FIX-NOW clusters (REM-08..14) at once: 29 files, 498 insertions / 197 deletions, almost all under `skills/nuclear-sop/`. This command dumps the entire commit (registration text, OE `.yaml` renames, composition-drift restoration, schema fixes, nav tables) — not just the 3 defects this issue describes.
**Analysis:** Actionability gap: the reader (human or agent) must manually locate the ~4 relevant hunks inside a much larger diff, which is exactly the "forces a lookup" failure mode.
**Suggested fix:** Scope the command to the affected files: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/sop-executor.md skills/nuclear-sop/agents/sop-capture.md skills/nuclear-sop/agents/sop-verifier.md skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml skills/nuclear-sop/composition/sop-executor.prompt.md skills/nuclear-sop/composition/sop-capture.prompt.md skills/nuclear-sop/composition/sop-verifier.prompt.md`

### S-001-02: Worktracker path has no explicit branch qualifier

**Evidence:** "Tracking: worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-012-state-machine-contract` (register section REM-12 in `remediation-register.md`, under `.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`)."
**Analysis:** "on branch `feat/proj-032-nuclear-sop-review`" grammatically attaches only to the register-section clause. The worktracker entity path that precedes it is a different repository location (verified to exist at `projects/PROJ-032-nuclear-sop-review/work/BUG-012-state-machine-contract/BUG-012-state-machine-contract.md` on that same branch) but the text never says so explicitly. Since this is emphatically *not* the reader's own PR branch, an agent resolving the path could reasonably check `main` first and get a 404, or not know which branch to check at all.
**Suggested fix:** "Tracking (both on branch `feat/proj-032-nuclear-sop-review`): worktracker `.../BUG-012-state-machine-contract`; register section REM-12 in `remediation-register.md` under `.../STORY-004-remediation/`."

### S-001-03: "SEC-008" is an unexplained internal code

**Evidence:** "the exact fail-open gap the PR's own compliance gate had flagged as remediation-required (its SEC-008 item), shipped unfixed."
**Analysis:** The sentence is understandable in context (a flagged, unremediated finding), but "SEC-008" itself is never defined and adds no information the external reader can act on — pure internal-governance residue.
**Suggested fix:** Either drop the code ("...had already flagged as remediation-required, shipped unfixed") or expand it once ("tracked internally as security finding SEC-008").

### S-001-04: Three defects compressed into one paragraph

**Evidence:** The "What was wrong" section is a single ~180-word paragraph enumerating three independent defects inline as "(1) ... (2) ... (3) ...".
**Analysis:** Minor readability/scannability cost; a skimming reader (or an agent chunking by markdown structure) is more likely to miss or conflate one of the three items than if they were list items.
**Suggested fix:** Convert `(1)/(2)/(3)` into a three-item markdown bullet or numbered list.

### S-001-05: Title leads with tracking codes, not content

**Evidence:** "PROJ-032/BUG-012: nuclear-sop — state machine specified three different ways; completion handoff type-broken (fixed on your branch)"
**Analysis:** The internal codes precede the actual, externally-meaningful description. Not misleading, just suboptimal ordering for a title's job (convey content first).
**Suggested fix:** "nuclear-sop: state machine specified three different ways; completion handoff type-broken (fixed on your branch)" — keep `PROJ-032`/`BUG-012` in the Tracking footer only, which already carries them.

## Recommendations

- **P1:** S-001-01 — scope the verify command to the affected files.
- **P1:** S-001-02 — make the branch qualifier unambiguously cover both tracking paths.
- **P2:** S-001-03, S-001-04, S-001-05 — polish for a fully self-contained, scannable artifact.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Neutral | All factual claims verified accurate against register/log/diff. |
| Actionability | Negative | S-001-01, S-001-02 add lookup friction for an agent acting on text alone. |
| Traceability | Negative | S-001-02's ambiguous branch scoping weakens one of two path references. |
| Completeness | Neutral | No missing defect coverage found; all 3 REM-12 groups represented. |

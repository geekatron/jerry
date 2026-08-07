# S-010 Self-Refine — Issue #354 (BUG-005: H-36 governance ruling)

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #354 (final snapshot, `issue-354.md`) |
| Criticality | C4 (tournament execution) |
| Iteration | 1 of 1 (compact single-pass) |

## Summary

The issue is well-written for its audience: it spells out H-36's three-hop rule in plain language, cites a real precedent (eng-team's 8-step/10-agent sequence, verified against `skills/eng-team/SKILL.md` — accurate), and gives a concrete resolution path. The single most important defect is a scope-narrowing misstatement — attributing a cross-file contradiction to "the file" — which could cause an agent to under-fix. Two further gaps force a lookup before the reader can act. Needs one targeted revision before it is fully self-contained and safe to act on without opening the register.

## Findings

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| S-010-01 | Contradiction misattributed to a single file | Critical | "the file's two fallback instructions contradict each other" | Internal Consistency / Evidence Quality |
| S-010-02 | Branch qualifier does not clearly cover the Worktracker path | Major | "on branch `feat/proj-032-nuclear-sop-review`" trails only the register-path clause | Resolvable References |
| S-010-03 | Rule file location never named | Major | "the skill's rule file" — no path given | Actionability |
| S-010-04 | Dependency on BUG-001's topology redesign omitted | Major | Register: ruling is "blocked on REM-01's hop-model definition" | Completeness |
| S-010-05 | "Worktracker" used as unexplained label over a bare directory (no filename) | Minor | "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling`" | Self-Containedness |

## Finding Details

**S-010-01: Contradiction misattributed to a single file (Critical)**
- **Evidence:** "the skill's rule file contains a self-imposed governance deadline... the file's two fallback instructions contradict each other (one says keep the current mode, the other says revert)."
- **Ground truth:** Register REM-05 shows the contradiction spans *two different files* — `nuclear-sop-behavior-rules.md` (rule NS-H-08: "remains as written" = keep current mode) versus `SKILL.md`/`PLAYBOOK.md` (automatic reversion to 3-hop = revert). It is not one file with two internal instructions.
- **Impact:** An agent or contributor could reconcile only the rules file, believe the defect is closed, and leave `SKILL.md`/`PLAYBOOK.md` asserting the opposite default — reproducing exactly the kind of cross-document contradiction this same PR review flagged elsewhere (REM-08's SKILL.md-vs-PLAYBOOK.md status conflict).
- **Recommendation:** Change to: "...the rules file and SKILL.md/PLAYBOOK.md give contradictory fallback instructions (rules file: keep the current mode until revised; SKILL.md/PLAYBOOK.md: revert automatically) and use different anchor dates..."

**S-010-02: Branch qualifier ambiguous for the Worktracker path (Major)**
- **Evidence:** The Worktracker path and the register path appear in one sentence; only the register path's clause explicitly states "on branch `feat/proj-032-nuclear-sop-review`."
- **Impact:** The Worktracker directory does not exist on `main` (confirmed: this project tree exists only on the feature branch). A reader who checks `main` first will wrongly conclude the tracking item is missing.
- **Recommendation:** State the branch once, up front, covering both paths: "On branch `feat/proj-032-nuclear-sop-review`: Worktracker `.../BUG-005-h36-governance-ruling`; full analysis in `remediation-register.md` at `.../STORY-004-remediation/`."

**S-010-03: Rule file location never named (Major)**
- **Evidence:** "the skill's rule file" is referenced twice but never pathed.
- **Impact:** The owner (or their agent) must open `remediation-register.md` just to learn which file to open next — an extra hop the issue could remove given the file is already known and short.
- **Recommendation:** Add the path once: "`skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`" (on the same branch).

## Recommendations (priority order)

1. Fix S-010-01 — attribute the fallback contradiction to the correct two files, not one. (Critical)
2. Fix S-010-02 — hoist the branch statement to cover both cited paths. (Major)
3. Fix S-010-03 — name the rules file path. (Major)
4. Consider adding one clause noting the ruling depends on the separate delegation-topology decision (BUG-001), so the owner does not rule prematurely. (Major, S-010-04)
5. Optional polish: briefly gloss "Worktracker" or link the exact `.md` filename, not just the directory. (Minor, S-010-05)

## Decision

**Outcome:** Needs revision (S-010-01 is Critical; not ready to stand alone without it).
**Rationale:** Core content (plain-language rule explanation, precedent, resolution path) is strong and accurate; the file-attribution error and the two lookup-forcing gaps are the only barriers to a fully self-contained, action-ready issue.
**Next Action:** Apply the four recommendations above; re-run S-010 or proceed to tournament synthesis.

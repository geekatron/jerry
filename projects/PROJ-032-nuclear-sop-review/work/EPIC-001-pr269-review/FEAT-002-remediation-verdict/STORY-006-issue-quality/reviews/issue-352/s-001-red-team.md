# Red Team Report: GitHub Issue #352 (BUG-003 — trust boundary / state tamper)

**Strategy:** S-001 Red Team Analysis (adapted, compact form for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-352.md` (live text of geekatron/jerry issue #352)
**Criticality:** C4 (tournament)
**Threat Actor:** A rushed or literal-minded reader — PR #269's external author or their coding agent — who has zero Jerry-governance context, will act *only* on this issue's text plus whatever it links, and will implement the narrowest fix that makes the words true rather than the intended design fix.

## Summary

The issue text is factually well-grounded: every claim (authority inversion, self-declared criticality, undocumented-but-inert SHA-256 claim, resume-past-hold defect) traces cleanly to remediation register REM-03 and is independently confirmed against the PR worktree (`state_hash`/SHA-256 appear only in `docs/reference.md` and the template, in zero agent files). No Critical (factually-wrong or misleading-to-a-fault) attack vector succeeded. Two Major gaps weaken actionability for a zero-context reader: missing scope/urgency framing (is this exploitable in the currently-approved skill or only a blocker for a still-withdrawn C3+ path?) and no inline file pointers. Two Minor findings concern precision and self-containedness. **Recommendation: ACCEPT with minor tightening** — no rewrite required.

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity |
|----|---------------|----------|-----------------|----------|
| S-001-01 | Reader cannot tell if this is an active exploit path today or a future-only blocker | Ambiguity | Medium | Major |
| S-001-02 | No affected-file pointers inline; remediation requires leaving the issue | Dependency | Medium | Major |
| S-001-03 | "resumes cleanly past every pause point" implies bypassing an active hold, not skipping the HELD state | Ambiguity | Low | Minor |
| S-001-04 | "trust anchor" in the title is undefined jargon, used nowhere else | Ambiguity | Low | Minor |

## Finding Details

### S-001-01: No scope/urgency framing for current vs. future risk [MAJOR]

**Attack Vector:** A reader with no context reads "the checker's authority comes from the thing being checked" and "blocks merge" and reasonably concludes this is live, exploitable risk in the skill as currently shippable. Nothing in the text states that `sop-verifier` (the agent this finding is about) only runs in the 4-hop/C3+ path, and that C3+ approval is *already withdrawn* (a fact from the same remediation effort, REM-08) pending exactly this and six sibling fixes. A contributor could over-index on "critical, exploitable now" and lose time reasoning about an attack surface that isn't reachable under the skill's current C1-C2-only approved envelope.
**Evidence:** Issue body has no mention of criticality scope or current approval status; register (REM-05 G2) confirms `sop-verifier` is eliminated in 3-hop (C1-C2) mode.
**Recommendation:** Add one clause, e.g.: "(applies to the C3+/4-hop verification path; C3+ is already withdrawn pending this and related fixes — see BUG-004)."

### S-001-02: No inline pointer to affected files [MAJOR]

**Attack Vector:** The issue names the mechanism (`sop-verifier`) but never names `agents/sop-verifier.md`, `agents/sop-brief.md`, `templates/PROCEDURE_STATE.template.yaml`, or `docs/reference.md` — the four files the register lists as in-scope. An agent trying to act "from this text alone" (per mission) cannot open a diff without first fetching and parsing `remediation-register.md` REM-03, an extra hop the issue doesn't flag as required.
**Evidence:** Register REM-03 "Affected files" row lists exactly these four paths; issue-352.md body contains zero file paths.
**Recommendation:** Append one line: "Files: `agents/sop-verifier.md`, `agents/sop-brief.md`, `templates/PROCEDURE_STATE.template.yaml`, `docs/reference.md`."

### S-001-03: Imprecise mechanism description risks a wrong-target fix [MINOR]

**Attack Vector:** "a hand-edited state file resumes cleanly past every pause point" reads as "an active hold can be overridden." The actual defect (register G4) is narrower and more dangerous: the hold check fires *only* when `status == HELD`; a file hand-edited to `IN-PROGRESS` never triggers the check at all — there is no hold to "get past." A fixer could waste effort hardening the hold-release logic instead of the status-integrity/independent-verification gap the register actually flags.
**Evidence:** Register REM-03 G4: "the SEC-003 hold check fires only on `status == HELD`... a poisoned IN-PROGRESS file resumes cleanly past all three hold types."
**Recommendation:** Reword to: "...and a state file hand-edited to skip the HELD status never triggers a hold check at all."

### S-001-04: Undefined jargon in the title breaks self-containedness [MINOR]

**Attack Vector:** The title's trailing "(trust anchor, PR #269)" introduces a PKI/security term of art that never recurs or is defined in the body. A reader unfamiliar with the term gains nothing from it; it is decorative internal shorthand in an otherwise self-contained issue.
**Evidence:** "trust anchor" appears exactly once, in the title, in issue-352.md.
**Recommendation:** Drop "trust anchor" from the title, or replace with a plain descriptor already used in the body, e.g. "(self-certifying verifier, PR #269)".

## Recommendations (Priority)

- **P1 (should fix before posting/finalizing):** S-001-01 scope clause, S-001-02 file pointer line.
- **P2 (polish):** S-001-03 reword, S-001-04 title trim.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-001-02: no file pointers means the issue alone is insufficient to start work |
| Internal Consistency | Neutral | No contradictions found against ground truth |
| Methodological Rigor | Neutral | All 5 attack categories applied; only 4 vectors surfaced (small artifact) |
| Evidence Quality | Positive | Every claim in the issue independently verified against register + PR worktree |
| Actionability | Negative | S-001-01/02 both reduce zero-context actionability |
| Traceability | Neutral | Issue correctly cites register path + branch |

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 0
- **Major:** 2
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5 (adapted, compact)

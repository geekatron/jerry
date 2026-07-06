# Refutation Panel — S-001 Findings, Remediation-Value Lens (Iteration 9)

> Panel member: independent refuter, remediation-value lens only. Did not read sibling refuter outputs or other panels (per mandate). Default posture: REFUTED unless the finding survives scrutiny — would fixing it materially change real adoption outcomes, or is it churn/optional-polish/already-scheduled/machinery-adding?

## Target Report

`projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-001-findings.md` — 2 Critical findings: RT-001-iter009, RT-002-iter009.

## Scope

Only Critical findings are in scope for this panel. (Major RT-003-iter009 and Minor RT-004-iter009 are noted but out of scope per the VERIFIED-CRITICALS protocol.)

---

## RT-001-iter009: scan command cannot see the 3 canonical `docs/design/` ADRs

**Verdict: VERIFIED**

The finding's core technical claim was independently checked: the specified pre-flight/L-3 command (`ADR-PROJ031-004-adr-identifier-convention.md:407`, identical `adr-standards-rule-draft.md:188`) filters on `-path '*/decisions/*'`. GNU `find`'s `-path` predicate requires the literal substring `/decisions/` to appear in the constructed path; `docs/design/ADR-agent-design-001.md` (and its two siblings) contain no such substring, so the predicate evaluates false and the command structurally cannot enumerate them — this is deterministic shell semantics, not an edge case. This directly contradicts the repeated "scanned roots (`projects/*/decisions/` + `docs/design/`)" framing at `:683` and the "18 files reachable by the scan path" acceptance criterion for the M-6 grandfather regression test (`:686`; `adr-standards-rule-draft.md:181`). That regression test is a stated gating condition ("must be green before the lint ships") — if M-6 is built literally to this spec, the regression corpus can only ever contain 15 files, not 18, making the document's own acceptance bar for shipping the real lint permanently unsatisfiable as written. This is not "polish": it is a spec-level defect in the one collision/grammar mechanism protecting the framework tier — the tier the ADR itself calls the highest-stakes ("framework-wide governance") — and it would propagate directly into the actual M-6 implementation if not caught now, silently exempting `docs/design/*.md` from L-1/L-3/L-7 forever. The offered fix (two-clause `find`, or an honest count correction) is text/syntax-only and adds no new lint rule, ledger, or gate, so it is fully consistent with the ratified subtraction doctrine — it does not fail the "would ADD machinery" disqualifier. Remediation value is real: a future engineer implementing M-6 from this document as written would ship a lint with a silent, undisclosed hole in exactly the tier the convention exists to protect.

## RT-002-iter009: repository-based-topology fallback does not reach that topology's own ADR home

**Verdict: VERIFIED**

Cross-checked against the document's own topology definition: D-5 (`ADR-PROJ031-004-adr-identifier-convention.md:235`) and the worktracker-topology-branch note (`:395`) both state that under the repository-based topology, the canonical ADR home is `{RepositoryRoot}/decisions/` with no `projects/` prefix, and that L-1/L-3/L-7 do not reach that home (R-10, already honestly disclosed). D-5's own sentence then states this audience "receives... the zero-tooling pre-flight one-liner only — not lint coverage — for collision-safety," which is an affirmative claim that the one-liner is a working substitute. But the one-liner given anywhere in either file (`:407`; `adr-standards-rule-draft.md:188`) is hardcoded to `find projects docs/design ...` — roots that, per the document's own topology table, do not contain that topology's `decisions/` corpus at all. No topology-aware variant, substitution instruction, or `${ADR_ROOT}` placeholder appears anywhere in either document; the "adapt it yourself" reading is not textually supported. This is distinct from — and adds to — the already-disclosed R-10 ("no lint coverage"): R-10 discloses the *lint* gap; RT-002 catches that the promised *manual substitute* for that gap is also non-functional for its named recipient, which is a materially worse, previously undisclosed position. PROJ-031's own stated purpose is producing a distributable Jerry CoWork/plugin skeleton, and the repository-based topology is explicitly named as an audience "PROJ-031's own downstream plugin/CoWork adopters may run" (`:235`) — i.e., this is a real, near-term deployment target, not a hypothetical corner case. A real adopter who copies the documented command as instructed would receive a false "no collisions" result every time, regardless of actual collisions in their `decisions/` corpus — a genuine false-assurance risk of exactly the kind this red-team pass's threat-actor profile targets. The countermeasures offered (parameterize the root, or honestly narrow the D-5 claim) are both text-only and add no new machinery, satisfying the subtraction doctrine. Remediation value is real and non-trivial: this document's own named target adopters would otherwise trust a non-functional safety net.

---

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| RT-001-iter009 | VERIFIED | Deterministic `find -path` semantics confirmed; breaks the document's own M-6 acceptance criterion (18-file regression); fix is text/syntax-only, no new machinery. |
| RT-002-iter009 | VERIFIED | Confirmed against the document's own topology table; the "consolation" fallback is non-functional for its explicitly named recipient audience (PROJ-031's own downstream adopters); fix is text-only, no new machinery. |

Both Criticals survive the remediation-value refutation attempt: each is deterministically verifiable against the deliverables' own specified mechanism and own stated facts, each bears on a real (not hypothetical) adoption outcome for a named audience, and each has a zero-new-machinery fix fully aligned with the ratified subtraction doctrine. Neither is optional polish, already scheduled elsewhere, nor would its fix reintroduce deleted machinery.

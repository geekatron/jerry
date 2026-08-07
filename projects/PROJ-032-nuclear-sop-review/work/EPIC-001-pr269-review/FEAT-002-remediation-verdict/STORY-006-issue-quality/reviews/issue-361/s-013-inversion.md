# Inversion Report: GitHub Issue #361 (BUG-012 / REM-12)

**Strategy:** S-013 Inversion Technique (adapted for a ~380-word communication artifact)
**Deliverable:** `snapshots/final/issue-361.md` (live text of geekatron/jerry issue #361)
**Criticality:** C4 (tournament)
**Goals Analyzed:** 3 (accurate defect description; actionable, self-scoped verification; honest no-action framing) | **Assumptions Stress-Tested:** 6 | **Vulnerable Assumptions:** 1 Major, 4 Minor

## Summary

All factual claims in the issue (commit `c07033ce`, branch `proj-0039-nuclear-engineer`, the three REM-12 defects, the CI run URL, the worktracker path) were checked against the remediation register, remediation log, and the full commit diff and are accurate — no Critical findings. Inversion surfaces one Major vulnerability: the "how to verify" command inverts into a false assumption that the diff it produces is scoped to *this* issue, when the commit bundles six sibling fixes. Four Minor findings target unexplained internal terms and density that would force an external agent to re-read or look elsewhere. Recommendation: ACCEPT with targeted revision to the verify command and light restructuring.

## Findings Table

| ID | Assumption Inverted | Severity | Evidence (issue text) |
|----|---------------------|----------|------------------------|
| S-013-01 | "The verify diff will show only this issue's fix" | Major | `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` |
| S-013-02 | "'worktracker' is self-explanatory to an outside reader" | Minor | "Tracking: worktracker `projects/...`" |
| S-013-03 | "'SEC-008 item' needs no gloss because meaning is inferable" | Minor | "(its SEC-008 item)" |
| S-013-04 | "A single dense paragraph transmits 3 independent defects as clearly as a list" | Minor | "What was wrong" paragraph (~190 words, 3 defects) |
| S-013-05 | "Leading the title with an internal ID costs nothing" | Minor | "PROJ-032/BUG-012: nuclear-sop — ..." |

## Finding Details

### S-013-01: Verify command is not scoped to this issue's fix [MAJOR]

**Inversion:** The issue instructs the reader to run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/`. Confirmed against the commit diff: `c07033ce` bundles **all seven** FIX-NOW clusters (REM-08..REM-14 — registration status, enforcement surfaces, schema conformance, OE artifact contract, state machine, composition drift, navigation tables) across 29 files, not just the four files affected by REM-12 (`PROCEDURE_STATE.template.yaml`, `sop-executor.md`, `sop-capture.md`, `sop-verifier.md` + `sop-verifier.prompt.md`).
**Consequence:** An external contributor or their agent running the suggested command to "verify" issue #361 will see ~25 unrelated file changes (nav tables, registration copy, agent schema fields) and either misattribute them to this issue or have to manually filter — extra research burden the "How to verify" line is supposed to eliminate.
**Mitigation:** Scope the diff to the affected files: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml skills/nuclear-sop/agents/sop-executor.md skills/nuclear-sop/agents/sop-capture.md skills/nuclear-sop/agents/sop-verifier.md skills/nuclear-sop/composition/sop-verifier.prompt.md`. Optionally add one clause noting the commit also carries six sibling fixes (issues #357–#360, #362, #363).

### S-013-02: "worktracker" unglossed [MINOR]

**Inversion:** If "worktracker" is not a term the reader already knows (true by mission constraint — zero internal governance knowledge), the Tracking line's first word conveys nothing.
**Mitigation:** Replace "worktracker `projects/...`" with "internal tracking record: `projects/...`" or drop the word — the path and register citation already carry the meaning.

### S-013-03: "SEC-008 item" unglossed [MINOR]

**Inversion:** The parenthetical "(its SEC-008 item)" names an internal code without expansion. The surrounding sentence makes the *meaning* recoverable (a flagged, unfixed remediation item), so this is not blocking, but it is an unexplained internal code per the review's self-containedness criterion.
**Mitigation:** Drop the parenthetical, or expand once: "(tracked internally as remediation item SEC-008)".

### S-013-04: Three defects compressed into one run-on paragraph [MINOR]

**Inversion:** "What was wrong" numbers three defects inline (1)/(2)/(3) inside one ~190-word paragraph, but "What the fix changed" does not mirror that numbering — the reader must manually re-match each fix clause back to its defect.
**Mitigation:** Convert both paragraphs to matching 3-item lists so defect (1)/(2)/(3) lines up visually with its fix; this also reduces the ~380-word total body toward the ~300-word target without losing content.

### S-013-05: Internal ID leads the title [MINOR]

**Inversion:** "PROJ-032/BUG-012" opens the title before any human-readable content; the mapping is only explained four sentences later in the Tracking footer.
**Mitigation:** Move the ID to a trailing parenthetical in the title, e.g. "nuclear-sop: state machine specified three different ways; completion handoff type-broken (fixed on your branch) [BUG-012]", or rely solely on the Tracking section for traceability.

## Recommendations

- **MUST:** S-013-01 — rescope or annotate the verify command before this issue is considered final.
- **SHOULD:** S-013-02, S-013-04 — light edits improve self-containedness and scannability at negligible cost.
- **MAY:** S-013-03, S-013-05 — polish only.

## Scoring Impact (abbreviated)

Actionability: Negative (S-013-01). Traceability/Completeness: Neutral (all facts verified correct). Concision: Negative (S-013-04). No Evidence Quality or Internal Consistency defects found — the issue's factual claims are fully corroborated by the remediation register, remediation log, and commit diff.

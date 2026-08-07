# Red Team Report: GitHub Issue #360 (BUG-011 / REM-11 — OE artifact contract)

**Strategy:** S-001 Red Team Analysis (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-360.md`
**Criticality:** C4 (tournament)
**Threat Actor:** PR #269's external author (or their coding agent) reading only this issue text, with zero knowledge of this repo's internal governance, trying to decide "do I need to act, and can I verify the claim myself?"

## Summary

The text is factually accurate against ground truth (register REM-11, remediation log, and the c07033ce diff all corroborate every specific claim: `.yaml` vs `.md` drift, the three-variant retrieval protocol, the unimplemented Section 11 write, the unsatisfiable acceptance criterion, CI 15/15, the tracking path). No Critical findings — nothing sends the reader down a factually wrong path. Two Major/Minor gaps reduce actionability: the "How to verify" diff command is not scoped to this issue's fix and will surface six unrelated fixes mixed into the same commit, and the verification grep is narrower than the source register's validation command. Remaining findings are polish (title jargon ordering, sentence density, one loosely-scoped claim). **Recommendation: ACCEPT with minor countermeasures** (P2/P1, no blocking issue).

## Findings Table

| ID | Finding | Category | Severity | Priority |
|----|---------|----------|----------|----------|
| S-001-01 | "How to verify" diff command surfaces all 7 FIX-NOW fixes, not just this one | Ambiguity/Actionability | Major | P1 |
| S-001-02 | Verification grep omits the `oe-entry-.*\.md` alternation from the source validation command | Ambiguity | Minor | P2 |
| S-001-03 | Title leads with unexplained "PROJ-032/BUG-011" shorthand; glossed only in the closing Tracking line | Ambiguity | Minor | P2 |
| S-001-04 | "What was wrong" packs 4 distinct defects into two dense, em-dash-heavy sentences | Degradation (readability) | Minor | P2 |
| S-001-05 | "both agents" phrasing loosely implies sop-capture.md carried the retrieval-protocol defect too | Ambiguity | Minor | P2 |

## Finding Details

### S-001-01: Verify command is not scoped to this issue's fix [MAJOR]

**Evidence:** "How to verify: ... run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/`" (line 11).
**Attack scenario:** `c07033ce` is one commit implementing all seven FIX-NOW clusters (REM-08..14) across 29 files (per the remediation log and the commit's own diffstat). Running the given command shows registration-truth fixes, schema fixes, the state-machine/completion-contract fix, composition resync, and nav-table fixes — all unrelated to the OE-artifact-contract defect this issue describes. Confirmed concretely: `agents/sop-capture.md`'s hunk in this diff mixes the REM-11 fix (new Section 11 attachment step) together with an unrelated REM-12 change (`execution_log_final` boolean→path semantics) in the same file, with nothing in the issue text to separate the two.
**Consequence:** the external author must manually read and mentally filter a large multi-concern diff to find the ~5 files actually relevant to *this* issue, for every one of the seven issues in the batch.
**Countermeasure:** scope the verify step to the affected files named in "What the fix changed" — e.g. `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/sop-capture.md skills/nuclear-sop/agents/sop-brief.md skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md` — or add one sentence noting the commit bundles all seven fixes and pointing to the specific files.
**Acceptance criteria:** the verify command (or an added file list) lets the reader see only the hunks relevant to REM-11 without cross-referencing other issues.

### S-001-02: Grep pattern narrower than the source validation check [MINOR]

**Evidence:** issue text: `grep -rn "experience/.*\.md" skills/nuclear-sop/`. Register REM-11 fix spec item 7: `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/`.
**Analysis:** the dropped `oe-entry-.*\.md` alternation is the pattern that would have caught the `capture/oe-entry-{entry_id}.md` template line (a path that doesn't contain the word "experience"). Both patterns return 0 hits post-fix today, so the claim in the issue is not currently false, but the given command is weaker than the SSOT check and would miss a regression that reintroduced only the `capture/oe-entry-*.md` form.
**Countermeasure:** use the full two-alternative pattern from the register, or note explicitly that the command checks only the persistent-store path.

### S-001-03: Title-first exposure of ungl­ossed internal codes [MINOR]

**Evidence:** title: "PROJ-032/BUG-011: nuclear-sop — ...". These codes are defined only in the final "Tracking" line.
**Countermeasure:** not blocking (the body is self-contained and never needs the codes to understand or act), but a reader who only sees the title/notification email gets no immediate anchor for "BUG-011". Consider a one-clause gloss near the title, e.g. "(internal tracking: BUG-011)".

### S-001-04: Dense multi-claim sentences [MINOR]

**Evidence:** "The rules file and the write path use `docs/experience/{entry_id}.yaml`, but the post-job template, one behavioral baseline, and the worked example all said `.md`. Entries written per those documents would be permanently invisible to retrieval, silently zeroing the feedback loop the skill names as its key capability — and one of the worked example's acceptance criteria was literally unsatisfiable."
**Countermeasure:** split into 2-3 short sentences or a 3-bullet list (extension drift / unsatisfiable AC / retrieval-protocol drift / missing Attachments write) — same content, faster to parse for a reader with no repo context.

### S-001-05: Slightly loose "both agents" framing [MINOR]

**Evidence:** "the `.yaml` and the workflow-ID-primary search protocol are now the single convention everywhere (template, baseline, example, both agents, and their mirror copies)."
**Analysis:** `sop-capture.md` already used `.yaml` paths pre-fix and does not perform OE retrieval; only `sop-brief.md` carried the retrieval-protocol defect. `sop-capture.md`'s only REM-11 change is the new Section 11 write step (correctly described in the next clause). Grouping both fixes under "both agents" is not factually false but slightly overstates sop-capture.md's role in the search-protocol correction.
**Countermeasure:** "the `.yaml` convention is now consistent everywhere (template, baseline, example, both agents' mirror copies); the workflow-ID-primary search fix applies to sop-brief" — or leave as-is; low impact.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Neutral | Core defect, fix, and verification are all present |
| Internal Consistency | Neutral | No contradictions found |
| Methodological Rigor | Negative (minor) | S-001-01/02 weaken the self-verification path |
| Evidence Quality | Positive | Every technical claim traced and confirmed against the register/diff |
| Actionability | Negative (minor) | S-001-01 forces manual diff filtering |
| Traceability | Positive | Tracking line's worktracker path resolves correctly to BUG-011 |

**Overall assessment:** proceed with monitoring — no Critical/blocking finding; P1 countermeasure (S-001-01) recommended before treating this issue as a template for the other six FIX-NOW issues in the batch, since the diff-scoping gap repeats identically across all of them.

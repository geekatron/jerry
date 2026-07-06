# Factual-Accuracy Refutation Panel — S-004 Pre-Mortem Analysis (Iteration 8, VERIFIED-CRITICALS Protocol)

> Lens: **factual**. Question per Critical: does the defect exist at the cited lines in the CURRENT files? Misreadings, stale refs, and restatements of already-disclosed residuals / restore-notes dispositions are REFUTED. Default REFUTED if uncertain.
> Target: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-004-findings.md`
> Cross-checked against: `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`, `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/*`, `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/restore-notes.md`.

## Findings Table

| ID | Verdict |
|----|---------|
| PM-001-iter8 | REFUTED |
| PM-002-iter8 | VERIFIED |

---

## PM-001-iter8 — REFUTED

**Claim:** CP-01 ("File paths only in handoffs, NEVER inline content") in `.context/rules/agent-development-standards.md:382` carries no textual exception, while the design doc (`design/feedback-decision-log-convention-design.md:78`) and the rule file (`design/staging-feedback-logs/feedback-decision-logs-standards.md:27`) both assert "a stated exception to CP-01" — an unresolved cross-document contradiction, with no Adoption-plan step to reconcile it.

**Factual check on citations:** All three citations are accurate as quoted — `agent-development-standards.md:382` is verbatim the CP-01 row with no exception clause; the design-doc L1.1 concurrent-writer paragraph at line 78 and rule-file LOG-M-005 at line 27 both use the exact "stated exception to CP-01" phrasing cited. However, this exact tension is not new: it is the substance of **FM-006** (S-012, iteration-003), whose improvement path explicitly offered two closure options — "specify a path-based candidate-file convention consistent with CP-01, **or** explicitly except feedback/decision candidates from CP-01 with stated rationale." The second option was chosen and accepted as **FIXED** in iteration-003 remediation-notes.md ("FM-006 | S-012 | Major | FIXED (CP-01 exception) | design L1.1 + rule LOG-M-005 — candidate is stated inline-payload exception"), re-affirmed in the design doc's own v5 changelog ("FM-006 reconciled the P-003 candidate handoff with CP-01 (stated exception)"), and independently re-verified against the live SSOT text at iteration-007 (S-011 CL-6: "VERIFIED — exact match") and again at iteration-008 (S-011 #13, S-001, S-007). No round since iteration-003 has treated "modify `agent-development-standards.md` itself" as an open action — the accepted closure path has consistently been a documented, sibling-rule exception, not an edit to CP-01's own row. Separately, the design's own Adoption plan step 3 already installs `feedback-decision-logs-standards.md` (which states the exception in LOG-M-005) into `.context/rules/`, which is precisely the "documented justification" the framework's own MEDIUM-tier override standard requires (`quality-enforcement.md` Tier Vocabulary: "MEDIUM ... Override requires documented justification") — CP-01 need not be edited in place for a sibling rule to carve a narrow, cited exception. This finding restates an already-disclosed-and-closed residual rather than identifying an unaddressed defect in the current text.

---

## PM-002-iter8 — VERIFIED

**Claim:** The numeric segment-rotation cap ("~50 entries or ~800 lines") is defined only in the design doc (`feedback-decision-log-convention-design.md:195`) and the staged rule file (`feedback-decision-logs-standards.md:28`, LOG-M-006) — never in `FEEDBACK-LOG.template.md`, the live bootstrap `FEEDBACK-LOG.md`, or (by the same evidence pattern) `LLM-DECISION-LOG.template.md`.

**Factual check:** Confirmed by direct read. `design/staging-feedback-logs/FEEDBACK-LOG.template.md`'s "Log Conventions" (lines 16–26) and "Segment Index" (lines 28–36) sections describe id/alias mechanics and forward/backward navigation but state no cap number anywhere in the file. The live `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md`'s "Log Conventions (bootstrap)" section (lines 18–22) likewise carries no cap figure. `LLM-DECISION-LOG.template.md`'s "Entry Schema" and "Segment Index" sections (lines 17–38) are equally silent on the numeric cap. The cap is stated only at `feedback-decision-logs-standards.md:28` (LOG-M-006) and `feedback-decision-log-convention-design.md:195` (Element table, "Cap" row) — both staged/design-time artifacts, neither of which is the file a session actually reads and appends to turn after turn. A targeted search of prior iterations (001–007) and this iteration's own "Findings Deliberately Not Raised" section found no prior finding or disclosure addressing "restate the numeric cap directly in the templates/live log files" — this is not a restatement of an already-accepted residual; it is a verifiable, currently-existing gap in the shipped/live artifacts.

---

## Execution Statistics
- **Criticals reviewed:** 2
- **Verified:** 1 (PM-002-iter8)
- **Refuted:** 1 (PM-001-iter8)

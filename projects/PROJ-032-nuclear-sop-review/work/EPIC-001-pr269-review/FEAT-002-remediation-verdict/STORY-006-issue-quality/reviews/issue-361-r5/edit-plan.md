# Issue #361 — R5 Reconciled Edit Plan (plateau diagnosis)

> Analyst pass over 4 scoring rounds (0.86 -> 0.87 -> 0.90 -> 0.91 vs 0.92 gate, 0 Critical).
> Deliverable under repair: `revised/issue-361.md` (paths in this plan are relative to `STORY-006-issue-quality/` unless repo-rooted).
> Ground truth used: register REM-12 (`../STORY-004-remediation/remediation-register.md` lines 295-321), `snapshots/evidence-c07033ce.md` (commit stat + full diff), «PR worktree» content checks, `../STORY-005-verdict/pr269-verdict.md`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Why it plateaus](#1-why-it-plateaus) | Mechanism + persistent dimension deficits |
| [2. Inter-round contradictions](#2-inter-round-contradictions) | Where the rounds' demands conflict |
| [3. Rejected-edit adjudication](#3-rejected-edit-adjudication) | Verdict on reviser rejections (none exist) + one prior demand overruled |
| [4. Final edit list](#4-final-edit-list) | Two exact edits, ground-truth verified |
| [5. Do-not list](#5-do-not-list) | Edits that would create new defects |
| [6. Word budget ruling](#6-word-budget-ruling) | 450 body words authorized; ~341 projected |
| [7. Projected outcome](#7-projected-outcome) | Arithmetic to >= 0.92 |

## 1. Why it plateaus

**Mechanism: every round's "Required Edits to Reach PASS" list was fully applied, and none of the lists was sufficient.** R1's 6 edits -> +0.01; R2's 6 -> +0.03; R3's 4 -> +0.01. Each judge listed additional "gaps" in dimension prose but left them out of the required list; the gaps then became the next round's binding deficit. R4 finally isolated the residue.

**Persistent dimension deficits (trajectory R1->R4):**

| Dimension | R1 | R2 | R3 | R4 | Outstanding deficit |
|---|---|---|---|---|---|
| Completeness (0.20) | 0.84 | 0.87 | 0.89 | **0.89 BINDING** | (a) no severity/status/triage marker (R3+R4); (b) G1's "Any state -> RESUMING" over-broad-transition sub-fact omitted (R1 gap c / S-011-03, R3, R4) |
| Actionability (0.15) | 0.78 | 0.89 | 0.91 | **0.91 co-binding** | same marker gap — no triage cue vs the six FIX-NOW siblings and seven blockers |
| Internal Consistency (0.20) | 0.94 | 0.90 | 0.91 | 0.91 | none valid — zero contradictions found in all 4 rounds; see §2.4 |
| Methodological Rigor (0.20) | 0.93 | 0.82 | 0.94 | 0.94 | resolved (R2 dip = the 5-file scope error, see §2.1) |
| Evidence Quality (0.15) | 0.83 | 0.87 | 0.89 | 0.92 | resolved |
| Traceability (0.10) | 0.80 | 0.88 | 0.86 | 0.92 | resolved |

Both outstanding deficits verified real against ground truth: register REM-12 header is literally `**Severity:** Critical | **Disposition:** FIX-NOW`; register G1 lists the template's "Any state -> RESUMING" vs the rules' enumerated predecessors, fix-spec item 1 orders the replacement, and «PR worktree» `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` line 47 confirms the narrowing was applied by `c07033ce`.

## 2. Inter-round contradictions

1. **R1 edits #1-#2 vs R2.** R1 prescribed a 5-file `Files:`/diff scope as the PASS remedy. The reviser applied it verbatim; R2 then scored that exact scope a Major rigor defect (0.93 -> 0.82) because R1's own list omitted `composition/sop-executor.prompt.md` and `composition/sop-capture.prompt.md` — which register REM-12 ("+ executor/capture composition twins") and the diff both include. R1's demand was factually wrong; R2's correction stands (already applied).
2. **Formatting demanded, then discounted.** R2 #3 (numbered list, "7 of 9 strategies") and R3 #4 (sentence split + parallel fix list) were required-for-PASS edits; R4 then held Internal Consistency flat on the explicit ground the edits "improved presentation, not consistency." Required edits with zero modeled yield displaced the edits that actually bind.
3. **The marker gap was never a required edit until it was the only gap left.** R3 flagged it in two dimensions' prose but omitted it from its required list; R4 named it the single remaining PASS blocker and modeled the fix (+0.006 Completeness alone -> 0.9205).
4. **Judge variance on Internal Consistency.** 0.94 (R1) -> 0.90 (R2) -> 0.91 (R3/R4) while every round reported zero actual contradictions. R2's dock — "one of seven mechanical fixes" and "seven design-defect clusters" being disjoint sets that both truly have 7 members — is a property of the facts, not the text (verdict: 7 FIX-NOW REM-08..14 + 7 DEFER-REWORK REM-01..07). Unfixable by editing; treated as scoring noise, not a deficit.
5. **Abandoned observation.** R2's "SEC-008 has no further resolution pointer" was never demanded and was dropped by R3/R4 (R4 Traceability 0.92, "no new traceability gap"). Moot — do not chase.

## 3. Rejected-edit adjudication

**No reviser-rejected edits exist for this issue.** `revised/issue-361.md` carries no trailing HTML comments (grep-verified); the sibling issues that use that mechanism (#350, #351, #352, #354, #357) contain no reference to #361. All 16 demanded edits — R1 (6), R2 (6), R3 (4) — are verified applied in the current text (R4's verification table for R3's four; direct text inspection for R1's and R2's). There is therefore nothing to overturn, and the adjudication is vacuous in the reviser's favor.

One **prior judge demand is overruled by this pass** so R5 does not resurrect it: R1 edits #1-#2's literal 5-file scope (see §2.1) — factually incomplete vs register and diff; the current 7-file scope is correct and must not be reduced.

## 4. Final edit list

Two edits. Both are R4's own modeled path, ground-truth verified here. Apply to `revised/issue-361.md`.

**EDIT 1 — severity/status marker (Completeness + Actionability, the binding gap).**
Insert as the first body line, after the TITLE line and its blank line, followed by a blank line:

```
**Severity:** Critical (register section REM-12) | **Status:** applied on your branch, pending PR #269 disposition.
```

- Grounding: register REM-12 `**Severity:** Critical`; fix applied in `c07033ce` on `proj-0039-nuclear-engineer`; issue open until disposition per verdict.
- Deliberately omits the register's `Disposition: FIX-NOW` token: "FIX-NOW" is internal-register jargon for the zero-context reader (same class as the "worktracker" ding R3 issued), and R4 modeled the full gain from severity+status alone. "(register section REM-12)" resolves via the existing Tracking footer.

**EDIT 2 — complete the G1 enumeration (Completeness; R4's "comfortable margin" item).**
In "What was wrong" item 1, replace:

```
divergent transitions after verifier rejection, and a "WAIVED" outcome the baseline requires but the template's allowed values omit.
```

with:

```
divergent transitions after verifier rejection, a "WAIVED" outcome the baseline requires but the template's allowed values omit, and a resume transition the template allowed from any state versus the rules' enumerated predecessors.
```

- Grounding: register G1 + fix-spec item 1 (wording "the rules' enumerated predecessors" is the register's own); narrowing confirmed applied in «PR worktree» template line 47.
- Fix item 1 ("Transitions aligned to the rules file as the single source of truth; template and baseline now match") already covers this sub-defect, so the 1:1 problem/fix mapping R3/R4 credited is preserved without touching the fix list.

No other edits. Internal Consistency has no valid open deficit (§2.4); Rigor, Evidence, Traceability are resolved and both edits are register-verbatim, so no dimension regresses.

## 5. Do-not list

- **Do NOT add `skills/nuclear-sop/behavioral-baselines/` (bb-002) to `Files:`** even though register REM-12's affected-files names it. Commit stat: `c07033ce` changed no bb-002 file (only `bb-003`, a different cluster); bb-002 is the parity *reference* the template was aligned to. Adding it would introduce a factual error into a text with a zero-falsehood record.
- **Do NOT reduce the 7-file verify scope** (overruled R1 demand, §3).
- **Do NOT "fix" the seven/seven coincidence** — both counts are true, disjoint, and already signposted by "unrelated"; R4 explicitly will not credit presentation there.
- **Do NOT touch the Tracking footer** (excluded from budget; Traceability at 0.92) and do not introduce absolute paths or non-032 project IDs anywhere.

## 6. Word budget ruling

**Completeness is the binding dimension (R4 weakest, 0.89; both valid outstanding deficits are completeness-family), so the 450-body-word allowance is triggered — and barely needed.** Current body (TITLE through "How to verify", Tracking footer excluded): 312 words. EDIT 1 adds 15, EDIT 2 adds net 14. **Projected body: ~341 / 450.** Headroom ~109 words; the reviser must not spend it — the plateau was never a length problem, and R4 found zero defects to dilute.

## 7. Projected outcome

R4 raw composite 0.9145 (needs +0.0055). Per R4's own Path-to-PASS model: EDIT 1 -> Completeness 0.89->~0.92 (+0.006) and Actionability 0.91->~0.94 (+0.0045); EDIT 2 -> full G1 closure pushes Completeness toward ~0.93. Projected composite **~0.925, PASS with margin**, with no regression vector: both edits are verbatim-grounded (Rigor), source-labeled (Evidence), path-free (Traceability), and consistent with every existing claim (Internal Consistency).

# Inversion Report: ADR-PROJ031-004 + Companion Rule Draft (Post-Subtraction Package, Iteration 7)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, independent reviewer — iteration 7)
**H-16 Compliance:** S-003 Steelman is embedded (not separately filed) throughout the ADR's Options-Considered section (each Scheme A–F leads with its blind advocate's strongest case before critique, per the glossary note at `ADR-PROJ031-004-adr-identifier-convention.md:65-67`). No standalone S-003 artifact was provided to this blind reviewer and none was read (blind protocol); this review treats the embedded steelman as satisfying H-16 for S-013's prerequisite per the template's own guidance that S-013 operates on the Steelman-strengthened deliverable within a compliant C3+ sequence.
**Goals Analyzed:** 8 | **Assumptions Mapped:** 7 | **Vulnerable Assumptions:** 4 (1 Critical, 2 Major, 3 Minor — one Major spans two assumptions)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Goals and Anti-Goals](#goals-and-anti-goals) | What the package is trying to achieve, and what would guarantee it fails |
| [Findings Table](#findings-table) | All findings with severity and dimension |
| [Finding Details](#finding-details) | Expanded evidence for Critical and Major findings |
| [Null-Alternative Benchmark](#null-alternative-benchmark-requested-by-the-mandate) | Does the slimmed package still beat "no convention"? |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to the 6 S-014 dimensions |

---

## Summary

The post-subtraction package correctly executes the doctrine it claims: the machinery that drew iteration 1–6 findings (waiver ledger, two-tier ratification, CODEOWNERS-dependent claims, 13 of 18 lint rules) is genuinely gone, not relabeled, and the honest-disclosure posture (Claim-Status blocks, [INHERENT] residuals, R-1…R-11) is applied consistently across both files. Inverting the package's own goals surfaces one **new, previously-undisclosed** technical defect that would guarantee exactly the failure mode the package exists to prevent (a silently-undetected ADR identity collision) if the lint is ever built to the letter of its current spec: the L-3 duplicate-ID one-liner's regex is unbounded-greedy and produces false negatives whenever a title-slug tail contains an embedded 3-digit run. This is a narrow, bounded "FIX-BUG"-class defect (consistent with the doctrine's own iteration-6 precedent for RT-101), not a call to restore deleted machinery — but it is Critical because it invalidates the "must be empty. Repo-wide." determinism claim the whole collision-safety argument rests on. A second, Major finding is that the two prerequisites the ADR itself names as make-or-break (M-2 relocation to `.context/rules/`, M-12 producer-agent fix) carry no date, no tracked Task, and no GitHub Issue as of this review (independently confirmed absent by filesystem search) — the disclosure is honest, but the exposure window is unbounded. **Recommendation: REVISE, narrowly.** The ratified decision (Scheme B) and the slimming itself should stand; the package needs one bounded regex fix before M-6 ships and a scheduling commitment (even a rough one) for M-2/M-12, not more machinery.

---

## Goals and Anti-Goals

**Goals extracted from the package** (Step 1): (G1) promotion never breaks ADR citations; (G2) subject-encoded IDs are more discoverable than origin-encoded ones; (G3) ID collisions are deterministically detectable without a central registry; (G4) the convention stays MEDIUM-tier, buildable by a solo maintainer, free of overclaim; (G5) legacy ADRs are grandfathered without a big-bang rename; (G6) every claim is honestly and completely disclosed (P-022) — the explicit ethos of this very subtraction pass; (G7) the guidance and lint actually become operative (auto-loaded rule file, compliant producing agent); (G8) the scheme beats the requested null alternative (no convention, index/search only).

**Anti-goal stress test (Step 2 — "what would guarantee failure at each goal?"):**

| Goal | What would guarantee failure | Does the package do it? |
|---|---|---|
| G1 (no citation break) | Renaming the ID string on promotion | No — Path 1 is a pure `git mv`, architecturally sound independent of any lint bug (see [Null-Alternative Benchmark](#null-alternative-benchmark-requested-by-the-mandate)) |
| G3 (deterministic collision detection) | A collision-detection mechanism that silently passes on real duplicates | **Yes, in one demonstrated edge case** — see [IN-001](#in-001-l-3-duplicate-id-collision-check-has-an-unbounded-greedy-regex-that-silently-misses-real-collisions-critical) |
| G4 (no overclaim) | Asserting "deterministic… Repo-wide" for a mechanism that is not, in fact, deterministic in all cases | **Yes, same defect** — the claim at rule-draft:175 / ADR:661 is not qualified |
| G6 (honest, complete disclosure) | Leaving a load-bearing dependency's timeline unstated indefinitely | Partially — the *existence* of the M-2/M-12 gap is disclosed; the *absence of any schedule* is not itself flagged as a risk — see [IN-002](#in-002-no-scheduled-commitment-or-tracked-task-for-the-two-prerequisites-the-adr-itself-calls-make-or-break-major) |
| G7 (operative guidance) | Leaving the guidance in a project-local draft file forever, with the producing agent unfixed | Not yet resolved, but named, owned, and gated "Yes" in the Migration Plan — disclosed, so this is folded into IN-002 rather than treated as a separate critical gap |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260706-iter007 | L-3 `sort \| uniq -d` deterministically catches every repo-wide domain-slug+NNN duplicate | Assumption | H (as stated) / **L (actual, per regex analysis)** | **Critical** | `design/adr-standards-rule-draft.md:175,183-192`; `decisions/ADR-PROJ031-004-adr-identifier-convention.md:661,393-404` | Methodological Rigor, Internal Consistency |
| IN-002-20260706-iter007 | The convention becomes operative (auto-loaded, producer-compliant) on a bounded timeline | Anti-Goal (unaddressed schedule) | M | **Major** | ADR `:89` (Status honest-scope note), `:506` (Claim-Status TBD-Task), `:511-512,523` (M-2/M-2b/M-12 rows); confirmed via Glob: `.context/rules/adr-standards.md` absent, `scripts/lint_adr_convention.py` absent, no Task/Issue entities under `projects/PROJ-031-cowork-skeleton/work/` |
| IN-003-20260706-iter007 | The collision-prevention lint (L-3) is meaningfully fail-closed given it is self-overridable in a single-CODEOWNERS repo | Assumption | M | Minor | ADR `:630` (Enforcement Design intro: "no waiver ledger, no CODEOWNERS gate"); `subtraction-pass-notes.md:56,88` (RT-002/RT-003 disposition) | Internal Consistency |
| IN-004-20260706-iter007 | This ADR's own filename (`ADR-PROJ031-004`) does not undermine the convention's credibility while un-promoted | Assumption | H | Minor | ADR `:2,30,687-695` (Meta-Note; M-9 not executed) | Traceability |
| IN-005-20260706-iter007 | Domain-slug taxonomy stays coherent under a best-effort, no-lint human review | Assumption | M | Minor | ADR `:413-414,450` (R-3); rule draft `:57` (M-5b) | Completeness |
| IN-006-20260706-iter007 | The 18-file grandfather regression test and the L-3 extraction regex are the same population | Assumption | H | Minor (subsumed by IN-001) | rule draft `:179`; ADR `:664` | Methodological Rigor |
| IN-007-20260706-iter007 | Full-path/GitHub-Issue citation staleness (R-B) is adequately bounded by a manual, un-scheduled `grep`/`gh` sweep | Assumption | M | Minor | ADR `:666`; rule draft `:194` | Actionability |

---

## Finding Details

### IN-001: L-3 duplicate-ID collision check has an unbounded-greedy regex that silently misses real collisions [CRITICAL]

**Type:** Assumption (deterministic collision detection)
**Original Assumption:** "L-3 No duplicate ID | Extract `{slug}-NNN` (canonical and uppercase-dialect) of all non-frozen ADRs; `sort | uniq -d` must be empty. Repo-wide." (rule draft `:175`; identical wording ADR `:661`). The runnable one-liner is offered as usable **today, with zero tooling**: "Empty output = no collision. Any line printed = a duplicate identity to resolve before commit." (rule draft `:189-191`; ADR `:401-403`).

**Inversion:** The extraction step uses `grep -E '^ADR-[A-Za-z0-9-]+-[0-9]{3}'` followed by `sed -E 's/^(ADR-[A-Za-z0-9-]+-[0-9]{3}).*/\1/'` (rule draft `:187-188`; ADR `:398-399`). Both the character class `[A-Za-z0-9-]+` and the digit-run `[0-9]{3}` are unanchored at the right side (no `$`), so standard POSIX ERE leftmost-longest matching extends the greedy group as far right as possible — through any *additional* 3-digit run that appears later in the title-slug tail, not just the intended `NNN`. Worked counter-example (reasoned from regex semantics; **not empirically executed — no Bash tool available to this reviewer, flagged per P-022; recommend the owner verify with `echo "..." | grep -E ... | sed -E ...` before dismissing**):
- File D1 = `ADR-security-002-cve-2024-100-mitigation.md`
- File D2 = `ADR-security-002-cve-2024-200-hardening.md`

Both share the true canonical identity `ADR-security-002` (same domain slug, same `NNN` — a genuine collision, exactly analogous to the documented `ADR-EPIC002-001` founding wound at ADR `:113`). But the greedy extraction captures through the *rightmost* valid `-DDD` split point in each filename — `...cve-2024-100` for D1, `...cve-2024-200` for D2 — because a longer overall match exists there than at the true `-002` boundary. The two extracted strings differ, so `sort | uniq -d` reports **no output**, i.e., **no collision** — a false negative on the exact scenario this rule is the sole deterministic backstop for.

**Plausibility:** High. Title-slugs referencing CVEs, HTTP status codes, ports, years, or issue numbers are a normal, foreseeable authoring pattern, not a contrived edge case. The regex logic is standard, deterministic POSIX ERE behavior (leftmost-longest match), not a probabilistic risk.
**Confidence:** M (regex semantics are well-established; not run against a live shell in this review — see caveat above).
**Consequence:** This is the *sole* mechanism both documents repeatedly describe as "deterministic," "fail-closed," and "Repo-wide" for collision prevention (rule draft `:9,165,175`; ADR `:630,655,661`), and it is the mechanism iteration 6 just hardened for the uppercase-dialect case (RT-101/DA-001, subtraction-pass-notes.md `:155,161`). A second undisclosed gap in the same rule, on the very next iteration, is a methodological-rigor regression, not merely a residual — and it directly threatens R-6 (cross-branch same-slug race), whose *only* stated detection mechanism is this same one-liner (ADR `:453`).
**Evidence:** `design/adr-standards-rule-draft.md:175,183-192`; `decisions/ADR-PROJ031-004-adr-identifier-convention.md:661,393-404`.
**Dimension:** Methodological Rigor (0.20), Internal Consistency (0.20).
**Mitigation:** A bounded regex correction, consistent with the doctrine's own "character-class widening, not new machinery" precedent (RT-101 fix, subtraction-pass-notes.md `:155`) — e.g., anchor the digit-run to end-of-string (`-[0-9]{3}$` after stripping any `-title-slug` tail first), or extract only up to the first `-[0-9]{3}` immediately following the domain-slug/dialect-prefix token using a non-greedy or explicitly bounded pattern. This is a "FIX-BUG" disposition (one regex edit, same rule, same 5-rule count), not a call to restore deleted machinery.
**Acceptance Criteria:** The corrected one-liner, run against the two constructed counter-example filenames (or equivalent), prints a duplicate line for `ADR-security-002` and does not do so for two genuinely different `NNN` values sharing a title-slug digit run. Add this as one of the "named red-then-green fixtures per rule" already committed for M-6 (ADR `:517`).

---

### IN-002: No scheduled commitment or tracked task for the two prerequisites the ADR itself calls make-or-break [MAJOR]

**Type:** Anti-Goal (unaddressed condition — Step 2)
**Original Assumption (implicit):** That disclosing the M-2 (relocate guidance to `.context/rules/adr-standards.md`) and M-12 (fix `ps-architect.md` so newly-authored ADRs comply) gaps is sufficient, because the Migration Plan already names an owner and marks both rows "Gating: Yes."
**Inversion:** "What would guarantee this convention never becomes operative for any agent other than a human reading these two files directly?" Answer: leave the guidance in a project-scoped draft with no relocation date, and leave the sole ADR-producing agent unpatched with no relocation date either. The package's own Status section already states plainly that this is the *current* state: "'in force' today means for a reader of this ADR or its companion rule draft — the guidance has **not yet been relocated** to the auto-loaded `.context/rules/adr-standards.md`... and the ADR-*producing* agent is **not yet fixed**... Neither M-2 nor M-12 has a tracked Task/Issue yet" (ADR `:89`). This review independently confirms both absences: `Glob(".context/rules/adr-standards.md")` → no match; `Glob("scripts/lint_adr_convention.py")` → no match; `Glob("projects/PROJ-031-cowork-skeleton/work/**")` → 23 files, none referencing this ADR's Migration Plan (all are skeleton-distribution EPIC-001 work items).
**Plausibility:** Certain — this is the present, verified state, not a hypothetical.
**Consequence:** M-12's own row states the stakes without hedging: "**Yes — the producing agent must emit compliant IDs or the convention is defeated at the source**" (ADR `:523`). A disclosed risk with an owner but no date is still an unbounded-duration risk; the mandate's "descoped-with-honest-disclosure is valid" posture credits *design* descoping (deleting the waiver ledger, the two-tier gate, 13 lint rules), not the *absence of a schedule* for two items the document itself flags as convention-defeating. Per the project's own governance (H-32, `.context/rules/project-workflow.md`), work items in the `geekatron/jerry` repo require GitHub Issue parity; M-2/M-12/M-13 are marked "TBD-Task + GH Issue (H-32)" but none exist yet, so the very rule requiring parity is itself not yet satisfied for these named, concrete action items.
**Evidence:** ADR `:89,506,511,512,523`; rule draft (no equivalent scheduling section — the rule draft correctly treats scheduling as an ADR/Migration-Plan concern); Glob confirmations above.
**Dimension:** Actionability (0.15), Traceability (0.10).
**Mitigation:** Open the two GitHub Issues / Task entities now (even without committing to a hard deadline) so H-32 parity is satisfied and the exposure window is externally visible and trackable, rather than living only inside this ADR's prose.
**Acceptance Criteria:** `projects/PROJ-031-cowork-skeleton/work/` contains Task entities (or the WORKTRACKER.md references GH Issues) for M-2 and M-12 specifically, each linked from the Migration Plan table in place of "TBD-Task."

---

## Null-Alternative Benchmark (requested by the mandate)

**Does the slimmed package still beat "no convention"?** Yes, on its primary, architecturally-load-bearing claim — **but the margin is narrower today than the prose implies, and the two findings above are exactly why.**

- **Citation-continuity (G1) — still clearly beats null, unaffected by IN-001/IN-002.** Path 1's "promotion is a pure `git mv`" property is a structural fact of the ID-stays-the-same design; it does not depend on the lint being built, the lint being correct, or the guidance being relocated. Bare-ID citations survive a promotion whether or not L-3 ever ships. This is the argument that survives the low-promotion regime per the ADR's own [Rationale](../../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md#rationale--answering-the-crux-head-on), and nothing in this review disturbs it.
- **Collision-prevention (G3) — currently at parity with null, not yet better.** Null has "no collision story" (ADR `:265`); today, this package also has no *operative* collision story, since the lint is unbuilt (confirmed) and the "runnable today, zero tooling" one-liner offered as the interim substitute has a demonstrated (if reasoned-not-executed) false-negative path (IN-001). Until IN-001 is fixed and M-6 ships, an author who runs the documented pre-flight check and sees empty output has **no stronger a collision guarantee than doing nothing**, in the specific case the counter-example constructs.
- **Discoverability (G2) — still beats null in the median case,** independent of both findings, since a subject-encoded filename is self-describing at the point of `ls`/`grep` regardless of lint status; taxonomy-synonymy drift (IN-005) is the disclosed, bounded exception, not a null-parity regression.

**Net conclusion:** the requested benchmark still favors adopting the convention over doing nothing, but the "beats the null" claim in the ADR's own [null-alternative section](../../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md#the-zero-governance-null-alternative-requested-benchmark-in-004) is explicitly conceded there as "an argued design advantage, not yet a demonstrated one" — this review's findings are additional, concrete evidence *for* that existing caveat, not a rebuttal of the overall decision.

---

## Recommendations

**Critical (MUST mitigate before M-6 ships / before relying on the pre-flight one-liner as a real safety check):**
- IN-001-20260706-iter007 — Fix the L-3 extraction regex (bounded correction, both copies) and add a red-then-green fixture with an embedded-digit-run title-slug to the M-6 regression suite.

**Major (SHOULD mitigate):**
- IN-002-20260706-iter007 — Open GH Issues/Tasks for M-2 and M-12 now (H-32 parity); a rough target window is preferable to none.

**Minor (MAY mitigate / acknowledge):**
- IN-003-20260706-iter007 — Note in the Enforcement-Design section that self-override was already a pre-existing weakness before the subtraction pass (not introduced by it), so readers don't misread the deletion of the waiver ledger as a new regression.
- IN-004-20260706-iter007 — No action beyond the already-scheduled M-9; informational only.
- IN-005-20260706-iter007, IN-007-20260706-iter007 — Already adequately disclosed with owner + cadence; no further action required by this review.
- IN-006-20260706-iter007 — Subsumed by the IN-001 fix; re-verify the "18 reachable" grandfather count once the regex is corrected, since the corrected extraction could change which files are counted as canonical vs. mismatched.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-001, IN-002: the two live gaps that most directly bear on whether the convention functions as claimed are not yet closed |
| Internal Consistency | 0.20 | Negative | IN-001: the twice-stated "must be empty. Repo-wide." claim (rule draft `:175`, ADR `:661`) is not true in the constructed counter-example |
| Methodological Rigor | 0.20 | Negative | IN-001: a rigor gap in a rule the package just finished hardening (iter-6 RT-101) for a different edge case, without exercising the fixture against title-slug digit runs |
| Evidence Quality | 0.15 | Neutral-to-Positive | Everything else in the package remains exceptionally well-evidenced (grep-verified ratios, Glob-verified absences, corrected historical scalars); this review's own findings are appropriately caveated as reasoned/not-executed where applicable |
| Actionability | 0.15 | Negative | IN-002: "TBD-Task" with no date is not independently actionable by anyone outside this ADR's own text |
| Traceability | 0.10 | Negative | IN-002: H-32 GitHub-Issue parity is not yet satisfied for the named M-2/M-12/M-13 work items |

**Overall assessment:** REVISE. One Critical (narrow, bounded, fixable without restoring deleted machinery) and one Major (a scheduling/tracking gap, not a design gap) stand between this package and the 0.95 engagement gate. The subtraction doctrine itself — delete the exposing claim or fix the bug, do not compensate with new machinery — is the correct disposition path for both findings.

---

*No subagents spawned (P-003). No deliverable files edited (P-020) — findings only. All evidence cites file paths and line numbers from direct reads of the two deliverables, `subtraction-pass-notes.md`, and Glob searches against the live repository; the IN-001 regex-behavior claim is explicitly labeled as reasoned analysis, not empirically executed, per P-022.*

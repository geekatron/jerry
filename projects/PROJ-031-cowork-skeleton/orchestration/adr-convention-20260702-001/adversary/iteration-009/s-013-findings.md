# Inversion Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 9)

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, scope |
| [Summary](#summary) | Overall assessment and verdict |
| [Findings Table](#findings-table) | New findings only (disclosed residuals excluded per mandate) |
| [Finding Details](#finding-details) | Full write-up per finding |
| [Assumptions Stress-Tested and Found Robust](#assumptions-stress-tested-and-found-robust-not-findings) | Inversion checks that the package already survives |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Execution Context

- **Strategy:** S-013 Inversion Technique
- **Template:** `.context/templates/adversarial/s-013-inversion.md`
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.10)
- **Criticality:** C4 | **Gate:** 0.95
- **H-16 Compliance:** S-003 Steelman embedded throughout Options A–F (per the deliverable's own glossary note); confirmed present in the package.
- **Prior context read (blind-protocol permitted):** `subtraction-pass-notes.md` (R-1…R-17, R-A/R-B/R-C, PM-009 residual register; 8 prior tournament rounds' Critical dispositions).
- **Blind protocol honored:** no files under `adversary/iteration-009/` or `iteration-010/` were read except this output file.
- **Executed:** 2026-07-06

---

## Summary

This package has already absorbed 8 adversarial rounds and discloses 17+ named residuals (R-1…R-17, R-A/R-B/R-C, PM-009) with honest Claim-Status labeling throughout. Applying Inversion fresh against "what guarantees failure of collision-free identity, honest promotion, and an adoptable MEDIUM convention" surfaces **one previously-undisclosed, filesystem-verified Major finding**: the L-2 ("no new bare ADR") lint rule is scoped "anywhere except frozen dirs" — unlike L-1/L-3/L-4/L-7, which are all explicitly scoped to `projects/*/decisions/` + `docs/design/` — and this unscoped reach directly contradicts the document's own twice-stated promise to grandfather the PROJ-014 bare-ID population without requiring rename. This is a genuine design defect in the *written* lint spec (not merely an "unbuilt" gap), independently verified against the live filesystem. No other new Critical- or Major-severity gap was found; the extensive existing residual register adequately covers the remaining "does it beat the null / does it guarantee failure" surface. **Recommendation: ACCEPT with one targeted mitigation** (a one-line scope correction to L-2, fully consistent with the subtraction doctrine — no new machinery required).

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| 013-001 | "The 5-rule lint core faithfully implements the document's own 'no big-bang renumber / grandfather in place' promise (c-003, D-4) for every disclosed legacy population." | Assumption | H (empirically confirmed) | **Major** | ADR-PROJ031-004:682; rule-draft:176; ADR:512; rule-draft:94; filesystem Glob | Internal Consistency, Methodological Rigor |
| 013-002 | "The ADR's exhaustive length and residual-register density do not themselves threaten the convention's adoptability." | Anti-Goal (readability) | M | Minor | ADR-PROJ031-004 (791 lines); rule-draft (247 lines, cross-references parent ADR 8+ times) | Actionability |

**Finding ID Format:** `IN-{NNN}-{execution_id}` per template; stable short IDs `013-NNN` used per this iteration's protocol. Full form: `IN-001-20260706-iter9` = `013-001`; `IN-002-20260706-iter9` = `013-002`.

---

## Finding Details

### 013-001: L-2 "no new bare" lint scope contradicts the disclosed PROJ-014 grandfather promise [MAJOR]

**Type:** Assumption (methodological rigor / internal consistency of the enforcement design)

**Original Assumption (as written):** The 5-rule L5 lint core, once built (M-6), enforces the convention without violating c-003 ("MUST NOT big-bang renumber frozen legacy sets; retire/alias instead") or D-4 ("No big-bang renumber... grandfathered in place"). The document extends this "grandfathered, no forced action" promise explicitly to the PROJ-014 bare-ID population:

> "PROJ-014 bare `ADR-001..004` (orchestration artifacts) | Transient, colliding with `docs/adrs/` | Low priority; rename to a domain slug (or `ADR-PROJ014-NNN` dialect) only if promoted into a `decisions/` home | **Low**" — `ADR-PROJ031-004-adr-identifier-convention.md:512`

> "**PROJ-014's bare `ADR-001..004` are transient bare drafts** (deprecated Scheme-E numbering, **not** a recognized dialect) — grandfathered only as historical artifacts, to be re-slugged if ever promoted." — `ADR-PROJ031-004-adr-identifier-convention.md:95` (Context corpus-survey note) — same language recurs at the rule-draft's [Frozen and Grandfathered Legacy](#) section, `adr-standards-rule-draft.md:94`.

**Inversion:** Every one of L-1, L-3, L-4, and L-7 is explicitly scope-limited in its own table row to the scanned roots (`projects/*/decisions/`, `docs/design/`) or narrower ("project-based topology only," "scanned roots only"). **L-2 is the sole exception** — its row states no scope restriction at all:

> "**L-2 No new bare** | A git-added file must not match `^ADR-\d`, except in frozen dirs (`docs/adrs/`, `docs/archive/`)." — `ADR-PROJ031-004-adr-identifier-convention.md:682`

> "**L-2 No new bare** | A git-added file must not match `^ADR-\d`, anywhere except frozen dirs (`docs/adrs/`, `docs/archive/`)." — `adr-standards-rule-draft.md:176` (the word "anywhere" makes the repo-wide reach explicit, not merely ambiguous)

Separately, the "static adoption-time baseline" mechanism the document itself introduced (iteration-8, IN-001-iter8) to prevent L-1/L-2 from false-flagging a pre-existing legacy file on its next edit is explicitly enumerated as **only** "the 18 reachable [15 dialect-reachable + 3 canonical] plus the out-of-scan `ADR-STORY015-001`" (`ADR-PROJ031-004-adr-identifier-convention.md:688`, the D-4-referencing grandfather-baseline paragraph). This 19-file baseline **does not include** the PROJ-014 bare set — which is a *third*, distinct class (not a "dialect," per the document's own classification at line 95: "not a recognized dialect").

**Plausibility:** Confirmed, not hypothetical. Filesystem-verified via `Glob "**/ADR-*.md"` (2026-07-06): the four files exist exactly as described, at `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-001-npt014-elimination.md` through `ADR-004-compaction-resilience.md` — i.e., outside any `decisions/` directory (so L-1/L-3/L-4/L-7 never reach them, consistent with their "Transient" classification), not inside `docs/adrs/` or `docs/archive/` (so the L-2 frozen-dir carve-out does not apply), and not on the enumerated 19-file grandfather baseline.

**Consequence:** Once M-6 ships and any one of these four already-tolerated files is git-modified for any reason (a typo fix, an in-body `AMENDED` block per this convention's own Amend mechanism, a later archival move, etc.), L-2 will FAIL it as a "new bare ADR," because: (a) it matches `^ADR-\d`, (b) it is not in a frozen dir, and (c) it is absent from the only enumerated grandfather-exemption list the document defines for L-1/L-2. This directly contradicts the "Low priority... only if promoted" and "grandfathered... as historical artifacts" language attached to this exact population, twice, in the same document. It is a defect in the **written spec itself** (both files agree verbatim on the unscoped L-2 wording), not merely a consequence of the lint being "designed, not built" — a faithful implementation of the current text produces this contradiction.

**Plausibility of the null hypothesis (that this is already covered):** Checked and rejected. `R-14` covers new-file collisions *inside frozen directories* (`docs/adrs/`, `docs/archive/`) — a different population. `R-10` covers out-of-scan *location classes* for L-1/L-3/L-4/L-7 — but L-2 is not scoped to those roots in the first place, so R-10's "out-of-scan" framing does not apply to L-2's problem (L-2's problem is the opposite: it reaches *too far*, not too little). No residual in the register (R-1 through R-17, R-A/R-B/R-C, PM-009) names this specific L-2/PROJ-014 conflict; grep confirms "PROJ-014" and "L-2" never co-occur anywhere in either file outside the two citations above.

**Dimension:** Internal Consistency (a written rule contradicts written prose in the same document) and Methodological Rigor (the one rule lacking the scope qualifier every sibling rule carries).

**Mitigation:** Either of two zero-machinery text fixes (fully consistent with the subtraction doctrine — no new rule, ledger, or gate):
1. Add the same scope qualifier to L-2 that L-1/L-3/L-4/L-7 already carry: restrict L-2 to `projects/*/decisions/` + `docs/design/`. This is the more coherent fix — it aligns with the "Orchestration drafts... Transient (non-canonical until moved into a `decisions/` home)" framing already in the Canonical Location Model table, i.e., bare IDs outside a canonical home are out of lint scope until Path-0 graduation moves them into one; **or**
2. Explicitly add the 4 named PROJ-014 files to the static adoption-time baseline enumerated at the D-4 grandfather-count reconciliation, alongside the existing 18 + STORY015.

**Acceptance Criteria:** The Enforcement Design / L5 CI Lint Specification sections in both files state L-2's scope explicitly (either a scanned-root restriction matching its siblings, or an explicit baseline inclusion for the named PROJ-014 files), and the Migration Plan / Frozen-and-Grandfathered-Legacy prose is updated (if needed) to cross-reference the fix so "Low priority... only if promoted" is mechanically true once M-6 ships.

---

### 013-002: Package length and residual density may itself work against adoptability [MINOR]

**Type:** Anti-goal (adoptability)

**Original Assumption:** A MEDIUM-tier, RECOMMENDED convention is adopted when authors can act on it without friction. The companion rule draft is the artifact designed to carry this load (auto-loads via `.claude/rules -> ../.context/rules`).

**Inversion:** "What would guarantee low adoption?" — a rule file that cannot be read and applied without also consulting a 791-line parent ADR. The rule draft (247 lines) cross-references "the parent ADR's Risks register" for R-9, R-10, R-11, R-12, R-14, R-15, R-16, R-17 by shorthand alone (e.g., `adr-standards-rule-draft.md:46,94,151,179,201`), meaning an author who wants to understand *why* a SHOULD-NOT exists must leave the auto-loaded file and read the much larger ADR.

**Plausibility:** Real but bounded. This is a legitimate readability cost, not a structural defect — the rule draft's own normative content (ADR-M-001…013, ID Scheme, Location Model, Promotion, Amend, Status, L5 spec) is self-contained and actionable without the cross-references; the `R-N` shorthand is supplementary rationale, not a load-bearing instruction.

**Consequence:** Minor friction for a curious author; zero functional blockage — the SHOULD-guidance itself is fully stated in the rule draft without needing the residual register.

**Dimension:** Actionability.

**Mitigation (optional, MAY):** Consider a one-line "why" gloss inline at each `R-N` reference in the rule draft rather than a bare pointer, if authoring bandwidth allows. Not required for acceptance — this is an improvement opportunity, not a blocker.

**Acceptance Criteria:** N/A (Minor; acknowledge or defer).

---

## Assumptions Stress-Tested and Found Robust (Not Findings)

Per the mandate ("already-disclosed residuals are NOT findings"), the following inversion angles were explored and found to be already honestly covered by the existing residual register — listed here as evidence of due diligence, not as new findings:

- **Cross-branch same-slug race** (creation-time and supersession-time) — R-6, R-17; mitigated-not-eliminated, disclosed.
- **Slug reuse for an unrelated subject / taxonomy sprawl** — R-3, R-7; human/index-only, disclosed unmitigated-by-lint.
- **Case-fold shadow / case-insensitive-filesystem collision** (verified this would in fact pass L-1, e.g. `ADR-proj031-001-slug.md` is grammatically canonical) — R-9, already named with this exact example.
- **Frontmatter `id:` uniqueness never checked** — R-15, disclosed.
- **Entity-embedded and repository-topology out-of-scan location classes** — R-10, disclosed (and independently filesystem-confirmed: `ADR-STORY015-001` does sit outside any `decisions/` directory, exactly as claimed).
- **L-7 asymmetry and zero real YAML targets in the live PROJ031 supersession chain** — R-11, R-16; independently spot-checked, framing holds.
- **Solo-maintainer self-approval of MEDIUM overrides** — R-12, disclosed as inherent to MEDIUM tier + one owner.
- **"Beats the null alternative" benchmark** — explicitly argued (citation-integrity vs. discovery-index framing) with an honest "argued, not yet demonstrated" qualifier (IN-002/IN-003 in the Rationale section); no gap found in this reasoning under inversion.
- **Grandfather count reconciliation (16/15/3/18)** — independently re-verified against the live filesystem via Glob; the counts as stated (D-4) match what exists on disk today.

None of these re-opens as a new finding; each already carries a named detection signal, an owner, or an explicit "argued not measured" qualifier per P-022.

---

## Recommendations

- **Major (SHOULD mitigate before M-6 ships):** 013-001 — scope L-2 to match its four sibling rules, or add the 4 PROJ-014 files to the grandfather baseline. Either is a one-line text edit; no new machinery.
- **Minor (MAY address):** 013-002 — optional inline "why" glosses for `R-N` cross-references in the rule draft.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Both deliverables remain substantively complete; the gap is a scope-qualifier omission on one of five lint rules, not a missing section. |
| Internal Consistency | 0.20 | Negative | 013-001: the L-2 rule's unrestricted scope contradicts the document's own twice-stated PROJ-014 grandfather promise. |
| Methodological Rigor | 0.20 | Negative | 013-001: L-2 is the one rule of five lacking the scope qualifier every sibling rule states explicitly — an asymmetry that escaped 8 prior rounds' rigor. |
| Evidence Quality | 0.15 | Neutral | Both findings are filesystem-verified with exact file+line citations; no impact beyond the findings themselves. |
| Actionability | 0.15 | Slightly Negative | 013-001's fix is trivial and named; 013-002 is optional. Net impact small. |
| Traceability | 0.10 | Neutral | Findings cite exact lines in both deliverables and an independent Glob verification. |

---

## Execution Statistics

- **Total Findings:** 2 (new, non-duplicative of the existing 17+-item residual register)
- **Critical:** 0
- **Major:** 1 (013-001)
- **Minor:** 1 (013-002)
- **Protocol Steps Completed:** 6 of 6 (goals stated, anti-goals inverted, assumptions mapped, stress-tested, mitigations proposed, scoring impact synthesized)
- **Verdict:** ACCEPT — no finding invalidates the core decision (Scheme B), the promotion process, or the convention's adoptability as ratified; 013-001 is a concrete, narrow, cheaply-fixable defect in the enforcement design text that SHOULD be corrected before M-6 implementation, consistent with the subtraction doctrine (text-only fix, no new machinery).

# Post-Ceiling Fix Notes — ADR-PROJ031-004 + Companion Rule Draft (after iteration-010)

> Owner: ps-architect (creator/owner). POST-CEILING artifact-hygiene pass.
> The C4 tournament reached its RT-M-010 iteration ceiling (10 rounds). Iteration-010 verified-protocol
> score 0.88, **zero VERIFIED Criticals** (all 6 claimed Criticals refuted 2-of-3 by the adversarial panels).
> This pass fixes the **5 residual Major clusters** the iteration-010 scorer flagged. **No re-scoring is claimed.**
> Doctrine binding: subtraction — text/disclosure fixes only, no new machinery; the 5-rule lint core stays
> **exactly 5** (L-1/L-2/L-3/L-4/L-7). P-002 incremental; P-003 no subagents; P-022 no fabrication.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mandate and Scope](#mandate-and-scope) | What this pass is and is not |
| [Load-Bearing Facts Re-Verified](#load-bearing-facts-re-verified-2026-07-06) | Filesystem ground truth before editing |
| [Cluster 3 — P-022 Correction (PRIORITY)](#cluster-3--p-022-correction-priority) | The false PR-template claim, corrected |
| [Cluster 1 — Table-vs-Grandfather Seam](#cluster-1--table-vs-grandfather-seam) | One authoritative statement; row-level exemption |
| [Cluster 2 — Ratification-Baseline Procedure](#cluster-2--ratification-baseline-procedure) | Minimal honest who/where/what-changes-it |
| [Cluster 4 — Cross-Installation Collision (R-18)](#cluster-4--cross-installation-collision-r-18) | Disclosed residual, not detection machinery |
| [Cluster 5 — Shipped Tag-Glossary / M-2 Stripping](#cluster-5--shipped-tag-glossary--m-2-stripping) | Smaller honest fix: M-2 strip clause |
| [Residuals Added](#residuals-added) | New register entries |
| [Counts and Budgets](#counts-and-budgets) | Re-measured line/token count |
| [Verification](#verification) | Absolute-path + employer-internal scan |

---

## Mandate and Scope

Iteration-010's S-014 scorer (VERIFIED-CRITICALS protocol, 0.88, gate 0.95, verdict REVISE by score band — **not** by any Critical trigger, since 0 VERIFIED Criticals) named 5 residual Major clusters. This pass remediates all 5. It does **not** claim a new score; it is artifact hygiene before user sign-off.

**Subtraction doctrine binding:** every fix is a text/disclosure edit. No new lint rule, ledger, gate, or matrix. The 5-rule core (L-1/L-2/L-3/L-4/L-7) is unchanged.

---

## Load-Bearing Facts Re-Verified (2026-07-06)

Verified by `find`/`ls`/`git log` against the live tree in this pass, before any edit (P-022):

| Fact | Method | Result |
|------|--------|--------|
| PR template existence | `ls .github/` + `find .github -iname 'pull_request_template*'` | **`.github/pull_request_template.md` EXISTS** (lowercase, GitHub-recognized form; 860 bytes) |
| PR template first commit | `git log --diff-filter=A --date=short` | **2026-02-18** (predates every iteration that reaffirmed it "absent") |
| PR template content | `cat` | Has `## Checklist` section (4 generic bullets); **no** M-9/M-2 atomicity bullet yet |
| `docs/design/ADR-*.md` | `ls` | **3** (agent-design-001, output-path-resolution-001, routing-triggers-001), none under a `decisions/` segment |
| `projects/*/decisions/ADR-*.md` | `find` | **15** dialect-reachable |
| Whole dialect corpus | `find` family tally | **16** = EPIC002×2 + PROJ010×6 + PROJ022×2 + PROJ031×4 + STORY015×1 + 150×1 |
| EPIC002 files' real location | `find` | Both at `projects/PROJ-001-oss-release/decisions/` (a plain project `decisions/` dir, **not** an entity `work/.../{ENTITY}/` dir) |
| STORY015 out-of-scan | `find` | In `work/.../STORY-015.../`, no `decisions/` segment — confirms 15 reachable = 16 − 1 |
| Rule-draft size pre-edit | `wc` | 253 lines / 4111 words (≈5.5k tokens) |

D-4's count reconciliation (16/15/3/18) is **confirmed accurate** against the filesystem.

---

## Cluster 3 — P-022 Correction (PRIORITY)

**What a prior agent claimed (false):** M-9 (ADR:544) stated the reciprocal-link atomicity check was "an intended reviewer-checklist item (FM-010, iter-6: **no `.github/PULL_REQUEST_TEMPLATE.md` exists yet — Glob-verified**; this is intent, not yet instrumented)." The same "Glob-verified absent" claim was reaffirmed at iter-6 (FM-010), iter-7 (VQ-019), and carried unchallenged through iter-8/9.

**What is actually true (filesystem-verified 2026-07-06):** a PR template **does exist** at `.github/pull_request_template.md` — the lowercase, GitHub-recognized filename — and has existed since **2026-02-18**. It carries a `## Checklist` section. The prior claim was a **false negative produced by an exact-uppercase-case search** (`.github/PULL_REQUEST_TEMPLATE.md`) that never tested the conventionally-cased lowercase form GitHub actually recognizes.

**Why this matters (P-022):** this cluster exists because a prior agent fabricated — through an unverified case-sensitive assumption — a "verified" repository-state claim, and it survived four independent verification passes. Correcting it is an honesty fix, named as such.

**Fix (text/disclosure, P-020 boundary respected):**
- ADR M-9 (:544): the parenthetical is corrected to state the template exists; the atomicity check is an **unadded checklist bullet in that existing template** — an owned, one-line M-9-adjacent edit to `.github/pull_request_template.md` (not performed by this document edit, per P-020), **not** a "no carrier file exists" blocker. The false "Glob-verified absent" wording is deleted.
- The correction is named explicitly in the ADR changelog (v1.12) and the rule-draft changelog (v1.12), and disclosed in this notes file. Historical changelog/disposition rows (ADR:786 v1.8; subtraction-pass-notes.md:171) that *record the iter-6 action* are **not rewritten** (FM-014 — they truthfully record what was done then, on a then-believed-true premise); the new changelog row supersedes the belief and names the error.

---

## Cluster 1 — Table-vs-Grandfather Seam

**The seam (4 independent strategies: 002-001, 012-004, 013-001, CV-001-i010):** the L-1/L-2/L-4 rows, read narrowly, appear to contradict the grandfather principle:
- **013-001:** L-1's row says `ADR-150-001` (numeric-leading) "is rejected," yet the mandatory grandfather regression test requires it to **pass** L-1. Every prior fix stated the exemption only in an *adjacent* paragraph, never in L-1's own operative text.
- **002-001 / CV-001-i010:** the two `ADR-EPIC002-001/002` files live in a plain project `decisions/` dir, not an entity `work/` dir; no Location Model row matches their (location, ID-form) pairing, and L-4 (prefix-matches-containing-dir) would misfire on them.
- **012-004:** L-2's textually-unscoped "anywhere" wording would flag PROJ-014's pre-existing bare drafts.
- Plus the count seam: ADR Migration-Plan row (:514) re-enumerates "PROJ031×3 … = 15" while D-4 states "PROJ031×4 … = 16" — different sets (with/without this self-promoting ADR), both correct, but requiring the reader to reconcile independently.

**Fix (one authoritative statement; rows reference it, not re-derive):**
1. **D-4** gains one authoritative "grandfather-exemption rule" paragraph: a file present on the ratification-time grandfather baseline passes L-1, is not flagged by L-2, and is not misfired by L-4 — **regardless of whether its filename matches a grammar in isolation.** This is stated once and is the single source the rows cite.
2. **L-1 rows** (ADR:686, rule-draft:175) gain the explicit third disjunct: "canonical OR dialect **OR present on the ratification-time grandfather baseline**," so no sentence asserts `ADR-150-001` "is rejected" without the exemption qualifier in the same breath.
3. **L-2 rows** (ADR:687, rule-draft:176) scope the bare check to files **absent from the baseline**, so pre-existing non-frozen bare drafts (PROJ-014) are not false-flagged.
4. **L-4 rows** (ADR:689, rule-draft:178) gain an explicit scope note: a pre-existing baseline dialect file whose entity-prefix does not match its containing dir (the EPIC002-in-project-`decisions/` class) is grandfather-exempt, not misfired.
5. **Location Model** (ADR:390, rule-draft:83) gains a note that entity-prefix dialects (EPIC/STORY) authored in a project `decisions/` dir are grandfathered legacy instances on the baseline.
6. **Count seam:** ADR Migration-Plan row (:514) stops re-enumerating an independent breakdown and instead references D-4, labeling its set as "the 16-file whole dialect corpus of D-4 minus this self-promoting ADR = 15 grandfather-in-place."

No new rule; the exemption is stated in operative row text per the existing "spec wording, not a sixth rule" framing (IN-001-iter8 precedent).

---

## Cluster 2 — Ratification-Baseline Procedure

**The gap (converging Majors 004-002 / 012-005 / 013-002):** the convention *anchors* the grandfather baseline to ratification time (2026-07-05/06) but states **no procedure** for how that baseline is captured, where it is recorded, or what changes it — leaving a future M-6 implementer to reconstruct "the corpus as of ratification" from memory, and risking silent re-anchoring to lint-ship-time.

**Fix (minimal honest procedure TEXT — who / where recorded / what changes it — no new machinery):** the IN-001-iter8 baseline clause (ADR:693, rule-draft:183) and M-6 (ADR:541) gain a concrete, one-time data-capture procedure:
- **Who:** governance/owner captures the baseline at ratification (a one-time action, not standing machinery).
- **Where recorded:** a checked-in data artifact — `scripts/adr-grandfather-baseline-20260705.txt` (one ADR path per line), generated by the two-clause `find` already specified, **plus** the ratification commit SHA recorded in the ADR changelog — so the set is reconstructible from a pinned reference, not re-`find`-ed against the working tree at build time.
- **What changes it:** the baseline is immutable once captured; a later addition of a legacy file discovered after ratification happens only via a **superseding/amending ADR** that regenerates the artifact against a newly-pinned commit — never a silent re-scan.

This is data-capture + disclosure, not a lint rule.

---

## Cluster 4 — Cross-Installation Collision (R-18)

**The gap (012-006, Major):** every collision check (pre-flight one-liner, L-3, `uv run jerry lint adr`) is single-filesystem-tree-scoped. PROJ-031's charter is distributing a skeleton to independent downstream installations with no shared git history; a downstream-authored ADR proposed back upstream is checked against neither installation's other corpus. Distinct from R-6 (same repo, one history) and R-10 (single-repo out-of-scan dirs).

**Fix (honest disclosure, not detection machinery):** register **R-18** in the ADR Risks register, naming the cross-installation collision blind spot [INHERENT to the registry-free, single-tree design] with a manual contribution-time mitigation (at contribution-back, run the pre-flight one-liner against the union of both trees, or rename-on-conflict per the Path-2 mechanic). Cross-referenced from the rule-draft descoped note.

---

## Cluster 5 — Shipped Tag-Glossary / M-2 Stripping

**The gap (003-001 / SM-001, Major):** the rule draft carries ~15 inline tournament-provenance tags (`RT-002-iter8`, `FM-003-iter8`, `012-003-iter9`, …) in its normative prose. Their glossary lives only in the ADR (:65), which does **not** travel with the shipped rule file. M-2 specifies link repair in detail but says nothing about the tags — so the auto-loaded `.context/rules/adr-standards.md` would ship with unexplained jargon, a stylistic regression versus every sibling rule file (which confine review history to a trailing Changelog).

**Fix (the smaller honest fix — fix M-2 so the glossary ships correctly):** M-2's close-condition (ADR:535) and the rule-draft wrapper note (rule-draft:3) gain an explicit clause: on the M-2 move, inline tournament-provenance tags are **stripped/relocated to a trailing footnote** so the shipped rule is self-contained — mirroring the atomicity discipline M-2/M-9 already apply to reciprocal link repair. Migration-Plan text (executor's action), no new machinery.

---

## Residuals Added

| ID | Residual | Home | Framing |
|----|----------|------|---------|
| R-18 | Cross-installation domain-slug collision (independent Jerry installs, no shared git history) undetectable by any single-tree lint/pre-flight | ADR Risks register; rule-draft descoped note | [INHERENT] to registry-free single-tree design; manual contribution-time mitigation |

No other new residuals. Clusters 1, 2, 3, 5 are corrections/procedure-text, not new uncovered gaps.

---

## Counts and Budgets

Re-measured `wc` 2026-07-06 after all iteration-010 edits (figures are self-referential — this notes file and both changelog rows are counted):

| Deliverable | Before (iter-9) | After (iter-010) |
|-------------|-----------------|------------------|
| Rule draft | 253 lines / ~5.5k tokens (~4.1k words) | **254 lines / ~6.4k tokens (~4.76k words × 1.35 = 6422)** |
| ADR (parent) | ~797 lines | **811 lines** (in-line disclosure additions; ADR has no token budget — it is the full decision record, not the shipped rule) |

The rule-draft line count moved only +1 (the v1.12 changelog row); all other cluster edits expanded existing physical lines (table rows and paragraphs) rather than adding lines. The token growth is irreducible honesty-disclosure content (D-4 exemption references, baseline capture procedure, R-18, tag-stripping clause). It remains above the ~2.5k soft target and marginally above the 250-line guidance — disclosed in both the rule-draft changelog v1.12 and its L5-spec self-measurement note. **The 5-rule lint core stayed exactly 5 (L-1/L-2/L-3/L-4/L-7); no new machinery.**

---

## Verification

Run 2026-07-06 after all edits:

| Check | ADR | Rule draft |
|-------|-----|------------|
| Home-directory absolute paths | **0** | **0** |
| Employer-internal refs ([employer] / codenames / internal-KB) | **0 (clean)** | **0 (clean)** |
| H-23 nav tables intact | Yes (no `##` section added/renamed; additions are in-section notes) | Yes (no `##` change) |
| Subtraction-pass-notes nav table | Updated (iteration-010 section + anchor added) | — |

**P-002:** all edits written incrementally to the live files; this notes file records the disposition. **P-003:** no subagents. **P-022:** the cluster-3 false PR-template claim was verified against the filesystem and corrected — no fabrication repeated; every count re-verified before editing.

# FMEA Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft — Iteration 10

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, protocol |
| [Summary](#summary) | Overall assessment |
| [Element Decomposition](#element-decomposition) | MECE breakdown per S-012 Step 1 |
| [Coverage Check — Not New Findings](#coverage-check--not-new-findings) | Candidate failure modes re-derived from R-1..R-17/R-A/B/C — excluded per mandate |
| [Findings Summary](#findings-summary) | New lifecycle failure modes, RPN-ranked |
| [Detailed Findings](#detailed-findings) | Full FMEA detail per finding |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Protocol completion |

---

## Execution Context

- **Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
- **Template:** `.context/templates/adversarial/s-012-fmea.md`
- **Deliverables:**
  1. `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.11, 797 lines)
  2. `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.11, 253 lines)
- **Criticality:** C4, gate 0.95
- **Protocol:** VERIFIED-CRITICALS (iteration 10). BLIND to iteration-009/010 prior findings files; read `subtraction-pass-notes.md` (readable disposition record, R-1..R-17 + R-A/R-B/R-C + PM-009).
- **Executed:** 2026-07-06
- **H-16 Compliance:** S-003 Steelman is embedded per-option in the ADR's [Options Considered (A–F)](../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md#options-considered-af) (confirmed present; not independently re-run in this pass — 9-round prior tournament already applies H-16 upstream of S-012).
- **Elements Analyzed:** 12 | **New Failure Modes Reported:** 3 | **Total New RPN:** 648

---

## Summary

Ten prior tournament rounds have driven this package through an extraordinarily thorough disclosure regime (17 dispositioned Criticals across iterations 5/8, plus R-1 through R-17 and R-A/R-B/R-C as named, owned residuals). Re-running the standard 5-lens FMEA against the same elements those rounds already covered would either re-derive disclosed residuals (excluded per mandate) or surface cosmetic issues (Minor, not reported). This pass instead targets **lifecycle mechanics that the existing residual register does not name**: (1) the grandfather-baseline mechanism's enumerated scope silently excludes a class of pre-existing bare-ID files the prose elsewhere claims are "grandfathered," creating a live false-positive/false-negative gap in L-2; (2) the "ratification-time, not lint-ship-time" baseline anchor (the 012-003 fix) is a wording-only correction with no named implementation artifact, so the very defect it claims to close is likely to re-occur when M-6 is actually built; (3) the entire collision-detection model is single-filesystem-tree-scoped, leaving PROJ-031's own stated cross-installation (upstream/downstream-plugin) distribution model with zero collision coverage. All three are genuinely new: none is named in R-1..R-17, R-A/B/C, or PM-009. **Recommendation: REVISE (targeted).** None of the three invalidates the core Scheme-B decision; all three are the same class of gap the package has repeatedly and honestly closed in prior rounds — text/disclosure fixes, not new machinery, consistent with the subtraction doctrine already in force.

---

## Element Decomposition

Per Step 1 (MECE decomposition), the two-deliverable package decomposes into:

| # | Element | Description |
|---|---------|-------------|
| E-1 | ID grammar (canonical + dialect) | Regex-level filename rules |
| E-2 | Canonical location model | Where each scope/topology lives |
| E-3 | Frontmatter schema | YAML fields, relationship links |
| E-4 | Promotion process (Path 0/1/2) | Project→framework elevation |
| E-5 | Amend vs Supersede | Lifecycle mutation rules |
| E-6 | Status vocabulary | Lifecycle state machine |
| E-7 | L5 lint rule set (L-1/L-2/L-3/L-4/L-7) | The 5-rule enforcement core |
| E-8 | Grandfather/baseline mechanism | Pre-adoption exemption logic |
| E-9 | Enforcement scope & deployment targets | Source repo vs. downstream plugin |
| E-10 | Migration Plan / Producer Fixes | One-time remediation actions |
| E-11 | Risk/residual register | R-1..R-17, R-A/B/C, PM-009 |
| E-12 | Self-compliance meta-note | This ADR's own identity/remap path |

---

## Coverage Check — Not New Findings

Applying the 5 failure-mode lenses (Missing/Incorrect/Ambiguous/Inconsistent/Insufficient) to E-1..E-12 surfaces many candidate gaps that are **already disclosed** and therefore excluded per mandate. Representative examples checked and excluded:

| Candidate | Element | Already disclosed as |
|---|---|---|
| Slug-uniqueness is a discipline not a guarantee | E-1 | R-6, R-7 |
| Entity-embedded / repository-topology homes unscanned | E-2, E-7 | R-10 |
| Case-fold slug look-alikes undetected | E-1 | R-9 |
| `id:` frontmatter field never deduplicated | E-3 | R-15 |
| L-7 checks only 3 of 6 relationship fields | E-7 | R-11 |
| L-7 has zero real YAML targets in PROJ031's own chain | E-7 | R-16 |
| In-place amendment mutation of `scope`/`origin` undetected | E-5 | R-C |
| Concurrent cross-branch supersession race | E-5 | R-17 |
| Cross-branch same-slug `NNN` race (single repo) | E-1 | R-6 |
| MEDIUM override self-approvable under solo maintenance | E-7 | R-12 |
| Frozen-dir new-file collision | E-8 | R-14 |
| Title-slug-tail extraction false-negative | E-7 | R-13 |
| Lint may never be built | E-7, E-9 | R-1, R-5 |
| Producer agent emits non-canonical IDs | E-10 | R-A |
| Free-text/GitHub-Issue citation staleness | E-4 | R-B |
| Forward promotion rate rests on n=3 | E-4 | PM-009 |

Three genuinely new lifecycle failure modes survived this filter (below).

---

## Findings Summary

| ID | Severity | Element | Failure Mode | S | O | D | RPN | Affected Dimension |
|----|----------|---------|---------------|---|---|---|-----|---------------------|
| 012-004 | Critical | E-7/E-8 | L-2's textually unscoped ("anywhere") bare-ID check + a ratification-time grandfather baseline that excludes PROJ-014's bare drafts creates a false-positive/false-negative gap for pre-existing non-frozen bare-ID files | 7 | 6 | 8 | 336 | Internal Consistency |
| 012-005 | Major | E-8 | The "ratification-time, not lint-ship-time" grandfather-baseline anchor (the 012-003 fix) has no named implementation artifact (no pinned commit/list), so M-6 is likely to silently re-anchor to lint-ship-time when built — reintroducing the exact amnesty-window defect the fix claims to close | 7 | 4 | 6 | 168 | Methodological Rigor |
| 012-006 | Major | E-7/E-9 | The entire collision-detection model (pre-flight one-liner, L-3, `uv run jerry lint adr`) is single-filesystem-tree-scoped; PROJ-031's own stated upstream/downstream-plugin distribution model has zero cross-installation collision check | 6 | 3 | 8 | 144 | Completeness |

**RPN Total (new findings only): 648.** Classification per template: Critical = RPN>=200 OR S>=9; Major = RPN 80-199 OR S 7-8; Minor = RPN<80 AND S<=6.

---

## Detailed Findings

### 012-004: Grandfather-baseline enumeration excludes PROJ-014's bare drafts, which L-2's unscoped wording would otherwise catch

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-7 (L5 lint rule set) / E-8 (grandfather/baseline mechanism) |
| **Strategy Step** | Step 2 (Enumerate: Inconsistent lens) |
| **S / O / D** | 7 / 6 / 8 → **RPN 336** |

**Evidence:**

L-1's row explicitly states its scan scope at the end of its own cell: `"...projects/*/decisions/, docs/design/."` (ADR line 686; rule draft line 175). L-2's row carries **no such scope qualifier** — it reads, verbatim: `"A git-added file must not match ^ADR-\d, except in frozen dirs (docs/adrs/, docs/archive/)."` (ADR line 687), and in the rule draft: `"A git-added file must not match ^ADR-\d, anywhere except frozen dirs (docs/adrs/, docs/archive/)."` (rule draft line 176, the word "anywhere" is explicit).

The Migration Plan documents a live, on-disk, non-frozen population of bare-ID files that L-2's wording would reach: `"PROJ-014 bare ADR-001..004 (orchestration artifacts) | Transient, colliding with docs/adrs/ | Low priority; rename to a domain slug (or ADR-PROJ014-NNN dialect) only if promoted into a decisions/ home"` (ADR line 517). The rule draft's own Frozen-and-Grandfathered-Legacy section calls these files **"transient bare drafts... grandfathered only as historical artifacts"** (rule draft line 94) — but the *operational* grandfather baseline that L-1/L-2 actually check against is enumerated precisely as **19 items**: "the 18 reachable [15 dialect + 3 canonical] ... plus the out-of-scan ADR-STORY015-001" (rule draft line 183; ADR D-4 reconciliation, lines 225-231, which lists `EPIC002×2, PROJ010×6, PROJ022×2, PROJ031×4, STORY015×1, 150×1 = 16` as the whole dialect corpus). **PROJ-014's 4 bare files appear in neither the 16-item dialect corpus, the 18-item reachable set, nor the 19-item ratification baseline.**

**Analysis:**

The Canonical Location Model classifies PROJ-014's location (`projects/*/orchestration/.../`) as **"Transient (non-canonical)"** (ADR line 393; rule draft line 86) — not **"Frozen"** (which is reserved for `docs/adrs/`, `docs/archive/`). Per L-2's own exemption clause ("except in frozen dirs"), Transient is not exempt. The grandfather-baseline mechanism (rule draft lines 183, ADR lines 693) states that "a git-modified file **already on that baseline** is treated as grandfathered-exempt from L-1/L-2... A git-modified file... **absent** from it are held to L-1/L-2 as 'new.'" Since PROJ-014's bare files are absent from the enumerated baseline, the mechanism as specified would classify any future git-modification of `ADR-001-npt014-elimination.md` (or its 3 siblings) as a "new" bare `ADR-NNN` — precisely the class L-2 is designed to reject — even though these files are pre-existing, on-disk, and elsewhere described in prose as "grandfathered... as historical artifacts." This is the identical structural bug class that the 012-003/IN-001-iter8 fix solved for `ADR-150-001` (a numeric-leading legacy file also outside the dialect/canonical taxonomy) — but that fix's baseline enumeration was scoped only to the dialect+canonical corpus reachable by the `decisions/`+`docs/design/` scan path, and PROJ-014's transient-orchestration-directory bare files were never folded into it. The Migration Plan itself signals these files **will** eventually be touched ("rename... if promoted"), and any such touch (even a trivial typo fix, unrelated to promotion) would trigger the same false-positive under the current spec. [Inference, P-022: this analysis is a specification-level reading, not an observed CI failure, since M-6 is not yet built — the gap is in the design's own stated mechanism, verifiable by cross-referencing the cited lines without needing the lint to exist.]

The alternate reading — that L-2 is intended to be scoped identically to L-1 (`projects/*/decisions/`, `docs/design/`) despite lacking that qualifier — produces the opposite failure: PROJ-014's directory (`projects/*/orchestration/.../`) would then be entirely **out of L-2's scan**, meaning new bare `ADR-NNN` files could be minted there indefinitely with zero detection, directly undermining ADR-M-004's "bare numbering is the documented collision source and is DEPRECATED" (rule draft line 49) in the one location where the founding failure mode (bare-ID collision) is already known to have partially recurred (PROJ-014 was itself renamed from a bare-`ADR-001..003` collision mid-session, per Context, line 113). Either reading produces a live, material gap.

**Corrective Action:**

Add PROJ-014's 4 bare files (and any other pre-existing non-frozen, non-dialect, non-canonical `ADR-*` file) to the ratification-time baseline enumeration explicitly, OR add a third grandfather category ("pre-existing transient/deprecated-Scheme-E files, enumerated at ratification time, exempt from L-1/L-2 but ineligible for new NNN allocation") alongside the existing dialect+canonical baseline. State L-2's scan scope explicitly (either "anywhere, repo-wide" or the same scanned roots as L-1) rather than leaving it as the one rule in the 5-rule core without a stated scope qualifier. This is a wording/enumeration fix to the existing baseline mechanism, not a new rule — consistent with the subtraction doctrine.

**Acceptance Criteria:** L-2's row states an explicit scan scope matching or explicitly differing from L-1's; the ratification-time baseline enumeration (currently "18 + STORY015 = 19") is either widened to include PROJ-014's 4 files by name or the exclusion is disclosed as a named residual with rationale.

**Estimated Post-Correction RPN:** ~40 (S=5 residual ambiguity if disclosed-not-fixed, O=2, D=4).

---

### 012-005: Grandfather baseline's "ratification time" anchor has no implementation mechanism, risking silent recurrence of the amnesty-window defect it claims to close

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-8 (grandfather/baseline mechanism) |
| **Strategy Step** | Step 2 (Enumerate: Missing lens) |
| **S / O / D** | 7 / 4 / 6 → **RPN 168** |

**Evidence:**

The 012-003 fix (iteration 9) re-anchors the grandfather baseline: *"Re-anchored to ratification time (2026-07-05/06)... anchoring the baseline to lint-ship-time would sweep every ADR minted in the (possibly long) ratification→lint-ship gap into it as if pre-existing legacy... Spec-wording correction, no new rule"* (`subtraction-pass-notes.md:221`). The rule draft states the mechanism identically: *"resolved against a static baseline fixed at ratification time (2026-07-05/06, not lint-ship time)... the enumerable set of ADR files present as of ratification... captured once as a data list in M-6 — a one-time artifact, not standing machinery"* (rule draft line 183; ADR line 693, same wording).

Nowhere in either deliverable, nor in the Migration Plan's M-6 row (ADR line 541, "Implement + wire the 5-rule L5 CI lint... with the grandfather regression test green... plus one named red-then-green fixture per rule"), is there a named mechanism for **how** a future implementer determines "the set of ADR files present as of ratification" — no pinned git commit SHA, no checked-in list/manifest file, no reference to `git show <ref>:path` reconstruction. The only artifact described is a "data list... captured once... in M-6" — but M-6 itself is Glob-verified not to exist (`scripts/lint_adr_convention.py` absent, ADR line 659).

**Analysis:**

The 012-003 disposition is explicitly labeled "spec-wording correction" (`subtraction-pass-notes.md:221`) — i.e., it corrects the *stated intent* of the anchor but does not add or specify any mechanism to *enforce* that intent at implementation time. Absent a concrete artifact (a frozen file list, or a pinned commit reference against which `git diff`/`git log` reconstructs the ratification-time corpus), the natural and lowest-effort implementation of "capture the set of files as a data list" is to run `find` against **whatever the working tree contains on the day M-6 is coded** — which is definitionally lint-ship-time, not ratification-time. Given M-6 has "no committed timeline" (ADR line 680, "Downstream/plugin disclosure") and is explicitly the package's own worst-rated risk ("FM-5... the single best-evidenced risk in this package," ADR line 501), the gap between ratification (2026-07-05/06) and eventual M-6 implementation could be substantial — precisely the growing window 012-003 states must not be swept in "as if pre-existing legacy." The fix closes the *prose* contradiction (D-4's "existing/legacy/pre-existing" framing) but does not close the *implementation* contradiction: without a pinned artifact, whoever eventually writes M-6 has no way to distinguish "existed at ratification" from "exists when I run this script" other than re-reading this exact paragraph and manually reconstructing history from git log — a step that is not called out as a required implementation task anywhere in the Migration Plan (M-6's row does not mention it). [Inference, P-022: this is a prediction about a not-yet-built artifact's likely implementation path, not an observed defect; rated Major rather than Critical to reflect that a careful implementer reading the full spec could still get this right.]

**Corrective Action:**

Add a concrete instruction to M-6 (Migration Plan) and/or the L5 Lint Specification: "the ratification-time baseline MUST be captured as a checked-in artifact (e.g., `scripts/adr-grandfather-baseline.txt`, one filename per line) generated via `git log --diff-filter=A --name-only --until=2026-07-06` (or an equivalent pinned-commit reconstruction) at or near ratification time — not regenerated from the working tree at M-6 build time." This closes the gap with a one-line implementation directive, not new lint machinery.

**Acceptance Criteria:** M-6's Migration Plan row or the L5 Lint Specification names a concrete artifact-generation mechanism (pinned commit/list) for the ratification-time baseline, distinguishable from a live `find` over the current tree.

**Estimated Post-Correction RPN:** ~48 (S=6, O=2, D=4).

---

### 012-006: Collision-detection model is single-tree-scoped; PROJ-031's own downstream-plugin distribution model has no cross-installation collision check

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-7 (L5 lint rule set) / E-9 (Enforcement scope & deployment targets) |
| **Strategy Step** | Step 2 (Enumerate: Missing lens) |
| **S / O / D** | 6 / 3 / 8 → **RPN 144** |

**Evidence:**

The pre-flight collision command and L-3's specification both operate over a single local filesystem tree: `find projects docs/design -name 'ADR-*.md' ...` (ADR lines 405-421; rule draft lines 187-204). The Enforcement Scope table names three targets: the `geekatron/jerry` source repo (L5 CI, primary), a "Downstream project *using* the plugin" (CI-independent `uv run jerry lint adr`, M-13), and the plugin skeleton tree itself (out of scope by design) (ADR lines 674-678). The Downstream/plugin disclosure at ADR line 680 states the CLI fallback's *"value in a fresh plugin install is bounded by the empty corpus it runs against (the skeleton ships no seeded decisions/)"* — disclosing that a fresh install has nothing to collide against, but **not** addressing what happens once a downstream install has accumulated its own non-empty corpus over time.

R-6 ("Cross-branch same-slug NNN race," ADR line 470) is explicitly scoped to *"two concurrent branches"* — a single shared git history. R-10 ("Out-of-scan location class," ADR line 474) is explicitly scoped to *"entity-embedded"* and *"repository-based topology"* homes **within one repository**. Neither residual, nor any other in R-1..R-17/R-A/B/C, names a cross-installation (two independent `.git` histories, e.g. an upstream `geekatron/jerry` and a downstream fork/plugin-adopter repo) collision scenario.

**Analysis:**

PROJ-031's entire charter is producing and distributing a "CoWork skeleton" that downstream adopters install as independent repositories (the skeleton generation design explicitly strips `projects/`, `tests/`, `.github/` — ADR line 665, `phase3-skeleton-generation-design.md:159`). Each such downstream install is, by construction, a **separate filesystem tree with no shared git history to the upstream framework repo**. If a downstream adopter authors ADRs locally over time (a corpus the CLI form, M-13, explicitly anticipates — "end-user's own ADRs," ADR line 675) and any of that content is later proposed back upstream (a contribution PR, a maintainer manually incorporating a useful pattern, or a downstream org later re-merging with upstream), **no mechanism in this design — not the pre-flight one-liner, not L-3, not `uv run jerry lint adr`, nor any residual in the register — checks the incoming ADR's domain-slug against the *other* installation's corpus.** Both the local pre-flight command and the CI-wired L-3 are single-tree `find`+`sort|uniq -d` operations; they cannot see a slug already claimed in a filesystem they were never pointed at. This is structurally distinct from R-6 (same repo, same history, race resolved by CI/merge) and R-10 (single-repo out-of-scan directories) — it is a **collision surface at the installation boundary itself**, arising specifically from the distribution model this project exists to build. Occurrence is rated LOW (no contribution-back flow has occurred yet — this is the project's *stated future* activity, not observed history), but materiality is direct: it undermines the "collision-free ADR identity" purpose precisely for the audience PROJ-031 is built to serve.

**Corrective Action:**

Add a one-sentence disclosed residual (parallel to R-6/R-10) naming the cross-installation collision gap, e.g.: *"R-18: domain-slug collision across independent Jerry installations (upstream framework repo vs. a downstream plugin-adopter's own corpus) is undetectable by any lint or pre-flight command in this design, since both operate on a single local filesystem tree. Mitigation: at contribution-back time (a PR proposing a downstream-authored ADR for upstream inclusion), the contributor/reviewer SHOULD manually re-run the pre-flight one-liner against the union of both trees, or rename on conflict per the standard Path-2 discouraged-rename mechanic."* This is a disclosure, not new machinery — consistent with the subtraction doctrine.

**Acceptance Criteria:** A named residual (R-18 or folded into R-6/R-10 with an explicit cross-installation clause) appears in the Risks register, with the manual-mitigation note above or equivalent.

**Estimated Post-Correction RPN:** ~36 (S=6, O=2, D=3 — once disclosed, a reviewer knows to check manually).

---

## Recommendations

Prioritized by RPN (highest first), consistent with the package's established subtraction doctrine (fix by deleting/correcting the exposing claim or gap; do not add new lint machinery):

1. **012-004 (RPN 336, Critical):** Explicitly state L-2's scan scope and either fold PROJ-014's 4 bare files into the ratification-time grandfather baseline enumeration or disclose their exclusion as a named residual with rationale. One-clause fix to an existing table cell + baseline list, no new rule.
2. **012-005 (RPN 168, Major):** Add a one-line implementation directive to M-6 (or the L5 Lint Specification) naming a concrete artifact-generation mechanism for the ratification-time baseline (pinned commit or checked-in list), closing the gap between "stated intent" and "buildable spec."
3. **012-006 (RPN 144, Major):** Add a named residual (R-18 or equivalent) disclosing the cross-installation collision blind spot, with a manual contribution-time mitigation note.

None of the three requires restoring deleted machinery (waiver ledger, two-tier gate, additional lint rules) — all are text/enumeration/disclosure fixes, matching the doctrine that has closed all prior-round Criticals.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | 012-006: the collision-detection mechanism is incomplete for the project's own stated distribution use case |
| Internal Consistency | 0.20 | Negative | 012-004: L-2's scope wording is inconsistent with L-1/L-3/L-4/L-7's explicit scan-root qualifiers, and the grandfather-baseline enumeration is inconsistent with the prose's "grandfathered... as historical artifacts" claim for PROJ-014 |
| Methodological Rigor | 0.20 | Negative | 012-005: the ratification-time anchor is asserted without a corresponding implementation mechanism, so the "fix" is not yet a buildable spec |
| Evidence Quality | 0.15 | Neutral | All three findings are grounded in direct file+line citations from both deliverables; no new evidence-quality gap introduced |
| Actionability | 0.15 | Neutral | All three corrective actions are one-clause text/enumeration edits, immediately actionable within the established subtraction doctrine |
| Traceability | 0.10 | Neutral | Findings cross-reference existing R-N residual IDs to demonstrate non-overlap (P-004) |

---

## Execution Statistics

- **Total New Findings:** 3
- **Critical:** 1 (012-004)
- **Major:** 2 (012-005, 012-006)
- **Minor:** 0
- **Candidate failure modes considered and excluded as already-disclosed:** 16 (see [Coverage Check](#coverage-check--not-new-findings))
- **Protocol Steps Completed:** 5 of 5 (Decompose; Enumerate; Rate S/O/D; Prioritize + Corrective Actions; Synthesize + Score Impact)
- **H-15 Self-Review:** Completed — all three findings independently re-verified against cited line numbers in both deliverables before this report was finalized; RPN inputs stated with explicit rationale per rating.

# Chain-of-Verification Report: ADR-PROJ031-004 (v1.10) + adr-standards-rule-draft.md

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4
**Date:** 2026-07-06
**Reviewer:** adv-executor (iteration 9, blind protocol — iteration-009/010 findings not read; iterations 001-008 + subtraction-pass-notes.md read per instruction)
**H-16 Compliance:** S-003 Steelman embedded in Options A-F (prior iterations); indirect per S-011 template (verification-oriented, not critique-oriented)
**Claims Extracted:** 22 | **Verified:** 20 | **Discrepancies:** 1 Critical, 1 Minor
**Finding ID format:** `011-{NNN}` (011 = S-011 strategy identifier, per orchestrator convention for this tournament)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verification assessment |
| [Claim Inventory and Verification Results](#claim-inventory-and-verification-results) | Extracted testable claims, independent verification, disposition |
| [Findings](#findings) | CV-NNN findings with severity |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Summary

I extracted 22 independently-testable factual claims (filesystem counts, line-anchored citations, cross-document numeric reconciliations, and quoted-source assertions) from the ADR and its companion rule draft, and verified each against the actual repository state using `Glob`/`Grep`/`Read` (no `Bash`/`git log` access, so two commit-hash claims are marked UNVERIFIABLE-BY-TOOLING rather than findings). **20 of 22 claims verified exactly** — including the load-bearing D-4 grandfather-count reconciliation (16 whole corpus / 15 reachable / 3 canonical / 18 regression), the 11-distinct-line ps-architect.md non-compliance footprint, the CLAUDE.md 3-of-17 navigation-registration ratio, the dangling `ci.yml:2` citation, the three live stale `ADR-PROJ007-001/002` citation sites, the single-CODEOWNERS-owner claim, and both nav tables' anchor integrity — which is an unusually high verification rate for a document at iteration 9 and reflects the prior 8 rounds' rigor. **One Critical finding (CV-001)** is a genuine, previously-undetected self-contradiction: the ADR's own Consequences section cites "(D-4)" as authority for a "near-zero forced churn" characterization of a 16-ADR set that explicitly *includes this ADR itself* — but D-4, the cited source, states the opposite for this specific file (it is "the one disclosed exception to 'in place'", scheduled for a non-trivial Path-2 rename+tombstone). This is not a disclosed residual; it is an incomplete propagation of a fix (FM-006-iter7) that corrected the Migration-Plan table cell but not this parallel prose bullet. **One Minor finding (CV-002)** notes an under-specified relationship label in the Related Decisions table. **Recommendation: REVISE** — a single-sentence edit closes CV-001; no new machinery is implied, consistent with the subtraction doctrine already governing this package.

---

## Claim Inventory and Verification Results

| CL | Claim (paraphrased) | Deliverable Location | Source Checked | Result |
|----|---|---|---|---|
| CL-01 | D-4: 16 whole dialect corpus = EPIC002×2+PROJ010×6+PROJ022×2+PROJ031×4+STORY015×1+150×1 | ADR:226 | `Glob **/decisions/ADR-*.md`, `Glob **/ADR-*.md` (filesystem count) | **VERIFIED** — counted exactly 2+6+2+4+1+1=16 |
| CL-02 | D-4: 15 = dialect files reachable by scan path (16 − out-of-scan STORY015), includes this ADR | ADR:227 | Same filesystem count, `decisions/`-scoped only | **VERIFIED** — 15 non-frozen files found in `decisions/` dirs incl. `ADR-PROJ031-004` |
| CL-03 | D-4: 3 canonical framework ADRs in `docs/design/` | ADR:228 | `Glob docs/design/ADR-*.md` | **VERIFIED** — exactly 3: `ADR-agent-design-001`, `ADR-output-path-resolution-001`, `ADR-routing-triggers-001` |
| CL-04 | D-4: 18 = grandfather regression corpus = 15+3 | ADR:229 | Arithmetic on CL-02/CL-03 | **VERIFIED** — 15+3=18 |
| CL-05 | `ADR-STORY015-001` is entity-embedded, not in a `decisions/` dir (out-of-scan, R-10) | ADR:227, Risks R-10 | `Glob`, `Read` path of the file | **VERIFIED** — lives at `.../STORY-015-tier-model-renumbering/ADR-STORY015-001-*.md`, no `decisions/` segment; file has no YAML frontmatter and no `scope:` field (confirms M-11's claim too) |
| CL-06 | `scripts/lint_adr_convention.py` does not exist (Claim-Status: designed, not built) | ADR:654, rule-draft:165 | `Glob scripts/lint_adr_convention.py` | **VERIFIED** — no file found |
| CL-07 | `.github/workflows/ci.yml:2` cites `ADR-CI-001` at `projects/PROJ-001-plugin-cleanup/decisions/...`, and that project path no longer exists | ADR:111 | `Grep ci.yml`, `Glob projects/PROJ-001*/**` | **VERIFIED** — line 2 exact match; only `PROJ-001-oss-release` and `PROJ-001-oss-documentation` exist, not `PROJ-001-plugin-cleanup` |
| CL-08 | Stale `ADR-PROJ007-001/002` citations live at `WORKTRACKER.md:106-107`, `ORCHESTRATION.yaml:228,242`, `EN-001.md:48-49,72-73` | ADR:95, M-10 | `Grep` each file at PROJ-007-agent-patterns | **VERIFIED** — all six line citations match exactly (plus two additional at EN-001.md:89-90 not claimed, which is fine — undercounting is not a discrepancy) |
| CL-09 | `ADR-EPIC002-002-enforcement-architecture.md` is a separate, legitimately-issued ADR still living in `projects/PROJ-001-oss-release/decisions/` (CV-002 correction) | ADR:113 | `Glob` | **VERIFIED** — file exists at that exact path |
| CL-10 | `ADR-EPIC002-001` cited from `.context/rules/quality-enforcement.md:108,275,290,350` | ADR:113 | `Grep quality-enforcement.md` | **VERIFIED** — exact line matches at 108, 275, 290, 350 (351 for EPIC002-002, consistent) |
| CL-11 | ps-architect.md non-compliance footprint: title `:218`; filename grammar 6 lines `:260,268,497,500,503,506`; phantom CLI 3 lines `:267,482,509`; literal examples `:480,482`; PS/entry labels `:250,251`; schema keys `:325,326`; total 11 distinct non-compliant lines | ADR M-12 row | `Read` targeted line ranges of `skills/problem-solving/agents/ps-architect.md` | **VERIFIED** — every cited line matches exactly, including the claimed dual-purpose line `:482` (both phantom CLI and literal filename) |
| CL-12 | 17 files exist in `.context/rules/`; only 3 individually named in CLAUDE.md's Navigation table (~18%) | ADR M-7 row | `Glob .context/rules/*.md`; `Read` CLAUDE.md Navigation table | **VERIFIED** — exactly 17 files; exactly 3 named (`quality-enforcement.md`, `agent-development-standards.md`, `agent-routing-standards.md`); 3/17=17.6%≈18% |
| CL-13 | HARD-rule ceiling is 25/25 (zero headroom) | ADR c-001, multiple | `Read` quality-enforcement.md HARD Rule Index | **VERIFIED** — counted exactly 25 entries (H-01…H-36, retired IDs excluded) |
| CL-14 | Both nav tables (ADR + rule draft) resolve to real headings; no dangling anchors | ADR Navigation, rule-draft Document Sections | `Grep '^## '` both files, slug-matched by hand | **VERIFIED** — all 24 ADR entries and 14 rule-draft entries resolve |
| CL-15 | Cross-file link `ADR-PROJ031-003-....md#claim-status-convention-p-022--foundational` resolves | ADR:654, rule-draft:165 | `Grep` heading in `ADR-PROJ031-003` | **VERIFIED** — heading `## Claim-Status Convention (P-022 — foundational)` at line 73 |
| CL-16 | Single-owner CODEOWNERS reality (`@geekatron` only) for `.github/workflows/` and `.context/rules/` (R-12) | ADR R-12, Enforcement Design | `Read .github/CODEOWNERS` | **VERIFIED** — both paths owned solely by `@geekatron` |
| CL-17 | `ADR-PROJ031-002`/`ADR-PROJ031-003` carry blockquote-only frontmatter, no YAML `---` block (R-16) | ADR R-16, L-7 row | `Read` first 15 lines of each file | **VERIFIED** — both files, blockquote-only |
| CL-18 | `.claude/rules -> ../.context/rules` behaves as a directory-level symlink (M-2b) | ADR M-2b | `Read .claude/rules/quality-enforcement.md` | **VERIFIED (behavioral)** — content resolves identically to `.context/rules/quality-enforcement.md`; literal symlink metadata not independently confirmable without shell `ls -la` (no Bash tool) — behaviorally consistent, not elevated to a finding |
| CL-19 | `docs/design/README.md` and `docs/adrs/README.md` do not exist (BUG-006 F-004 "never implemented") | ADR L2, Context | `Glob` both paths | **VERIFIED** — neither exists |
| CL-20 | Trade-study score table (A=3.52,B=3.58,C=3.86,D=3.06,E=2.10,F=3.60; 0.34 knife-edge) and the 0.75 confidence-ceiling quote | ADR Options/Confidence sections | `Read`/`Grep` `explore/trade-study.md:217-231,341` | **VERIFIED** — scores, ranks, and the exact quote ("I decline to claim >0.75 for a C4 governance flip resting on n=3") all match verbatim |
| CL-21 | `ADR-PROJ031-001` constraint `c-008` mandates retaining `src/`, `pyproject.toml`, `uv.lock` | ADR Enforcement Scope | `Read ADR-PROJ031-001:86` | **VERIFIED** — c-008 text matches exactly |
| CL-22 | 72%/28% bare-ID vs. full-path citation ratio measured within `.context/rules/` | ADR Path 1 caveat | `Grep 'ADR-[A-Za-z0-9]'` across `.context/rules/` | **PARTIALLY VERIFIED / SCOPE-LIMITED** — full-path citations clearly exist alongside bare-ID citations (directionally consistent with a real minority), but classifying each grep hit as "bare" vs "full-path" is ambiguous where both forms co-occur in the same table row; exact recount not reproduced. Not elevated to a finding: the claim already self-discloses (DA-002-iter4) that the ratio is `.context/rules/`-scoped only and "cannot be safely generalized repo-wide" — this is an already-disclosed approximation, not a fresh discrepancy |

**Commit-hash claims (`41539073`, `9b36bda2`, `5ef0b2fa`) are UNVERIFIABLE-BY-TOOLING** — no `git log`/`Bash` access in this execution environment. Not treated as findings (tooling limitation, not a deliverable defect); flagged here per Step 3 protocol for transparency.

---

## Findings

### 011-001 (CV-001): Consequences "near-zero forced churn" claim misciting D-4 for this ADR's own Path-2 exception [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Consequences → Positive, item 4 (ADR line 438); parallel/consistent phrasing checked in rule-draft §Frozen and Grandfathered Legacy (line 94) |
| **Strategy Step** | Step 4 (Consistency Check) — MATERIAL DISCREPANCY against a self-cited source |

**Claim (from deliverable, ADR line 438):**
> "**No big-bang migration** — the 3 framework ADRs already comply; the 15 pre-existing project/entity dialect ADRs (16 incl. this ADR) are grandfathered; PROJ-031's set already migrated. Net near-zero forced churn **(D-4)**."

**Source Document:** The same ADR's own D-4 (Decision section, lines 223-231) and the Migration Plan table (line 511).

**Independent Verification:**
- D-4 states explicitly (line 223): *"The **15 pre-existing** dialect ADRs remain valid legacy-dialect instances **in place**. **This ADR is the one disclosed exception to 'in place':** its current filename is a valid dialect, but it is itself scheduled for Path-2 self-promotion *out of* the dialect (M-9…), so it does not remain in place."*
- The Migration Plan table (line 511) assigns this ADR's own row a Cost of **"Low"** (recalibrated from "Trivial" per FM-006-iter7: *"the M-9 self-promotion is multi-part — rename + tombstone + *reciprocal* ADR↔rule-draft link repair that MUST land atomically"*) — explicitly distinct from the "Project-scoped families" row immediately above it, whose Cost is **"Zero."**
- M-9 itself (line 539) is gated **"Yes (on acceptance)"** and is independently subject to **AE-004 auto-C4 escalation** per the Promotion Process's own Path-2 scoping clause (line 573-577), because a Path-2 promotion flips a baselined ADR's status to `SUPERSEDED`.

**Discrepancy:** Consequences-Positive-4 asserts that the **full 16-count "incl. this ADR"** is "grandfathered" with "**Net near-zero forced churn**," and cites **"(D-4)"** as the source for that claim. But D-4 — the cited source itself — says the opposite for this specific file: it is the sole disclosed exception that does **not** remain in place, and its own Migration-Plan cost cell is "Low" (non-zero, multi-part), not "Zero." The claim conflates the 15 truly-zero-cost grandfathered ADRs with the 1 ADR (this one) whose own document explicitly plans a non-trivial rename+tombstone+reciprocal-link-repair operation gated for AE-004 auto-C4 review. This is not a new fact needing disclosure — it is an **internal citation mismatch**: a specific line cites D-4 as authority for a claim D-4 contradicts.

**Severity — Critical because:** This is exactly the class of defect this document's own remediation history treats as blocking: FM-006-iter7 previously corrected the *identical* underlying fact ("Trivial"→"Low, multi-part") in the Migration-Plan table cell, but that fix was never propagated to this parallel Consequences-section restatement, which still asserts the pre-fix characterization and attributes it to the very section (D-4) that was written to correct it. It also directly undermines the ADR's own flagship pedagogical claim (Meta-Note: *"a worked example of its own Path-2 promotion and grandfathering rules"*) — a worked example that inconsistently describes its own migration cost as both "near-zero" (here) and "Low, multi-part" (Migration Plan) is not a reliable model for future authors to follow, which is precisely the honest-promotion-process purpose this convention exists to serve.

**Dimension:** Internal Consistency (0.20 weight)

**Correction:** Amend ADR line 438 to exclude this ADR from the "near-zero churn" characterization, e.g.: *"the 15 pre-existing project/entity dialect ADRs are grandfathered at zero cost; this ADR (the 16th, incl. above) is the disclosed exception — its own Path-2 self-promotion (M-9) carries non-zero, multi-part cost, per D-4."* No new machinery required; a one-sentence edit, consistent with the subtraction doctrine already governing this package.

---

### 011-002 (CV-002): Related Decisions table omits actual lifecycle relationships for `ADR-PROJ031-002`/`ADR-PROJ031-003` [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Related Decisions (ADR lines 725-735) |
| **Strategy Step** | Step 4 (Consistency Check) — MINOR DISCREPANCY |

**Claim (from deliverable):**
> `ADR-PROJ031-002` (CI token/push) \| SIBLING \| Legacy project dialect; grandfathered
> `ADR-PROJ031-001` (skeleton distribution) \| SIBLING \| Legacy project dialect; grandfathered in place

**Independent Verification:** `ADR-PROJ031-002`'s own header states: *"**SUPERSEDED BY [ADR-PROJ031-003]** (2026-06-28): the confirmed dedicated-repo distribution model invalidates this ADR's three load-bearing decisions… Content retained for provenance; do not implement from this ADR."* Its blockquote frontmatter carries `Status: **Superseded by ADR-PROJ031-003**`. Separately, `ADR-PROJ031-003:12` states *"**Amends:** ADR-PROJ031-001 — the in-repo `cowork-skeleton` branch distribution sub-decision is replaced… (ADR-PROJ031-001 updated in place 2026-06-28)."*

**Discrepancy:** The table's uniform "SIBLING" label is accurate as a *co-location* description (all four ADRs share the PROJ-031 project and the dialect-grandfathering status the label is meant to convey), but it does not surface that `ADR-PROJ031-002` is itself `SUPERSEDED` and `ADR-PROJ031-001` is itself `AMENDS`-target — both non-trivial lifecycle facts a reader would want when following this ADR's own Supersede/Amend conventions as a worked example.

**Severity — Minor:** Does not affect the convention's validity or collision-safety; purely an informational completeness gap in a reference table.

**Recommendation:** Optionally add a footnote or a "Lifecycle" column noting `ADR-PROJ031-002: SUPERSEDED by -003`; `ADR-PROJ031-001: amended by -003`. Not required for acceptance.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No claim categories were skipped; all testable claim types (counts, citations, cross-refs, quotes) were extracted and checked |
| Internal Consistency | 0.20 | Negative | 011-001: a self-cited source (D-4) is directly contradicted by the citing passage for this ADR's own churn characterization |
| Methodological Rigor | 0.20 | Positive | 20 of 22 independently-testable claims verified exactly against filesystem/source evidence; the D-4 numeric reconciliation (the document's most complex claim) is fully accurate |
| Evidence Quality | 0.15 | Negative | CV-001's miscited-source pattern is precisely the failure mode this document otherwise guards against elsewhere (e.g., the CV-002-iter3 BUG-006/ADR-EPIC002-002 disambiguation) |
| Actionability | 0.15 | Neutral | CV-001's correction is a one-sentence, mechanically-applicable edit; CV-002's is optional |
| Traceability | 0.10 | Neutral | Both findings trace a specific line to a specific contradicting source line within the same document set |

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 1
- **Major:** 0
- **Minor:** 1
- **Claims Extracted:** 22 (20 VERIFIED, 1 scope-limited/already-disclosed, 1 pair UNVERIFIABLE-BY-TOOLING — commit hashes)
- **Protocol Steps Completed:** 5 of 5 (Extract Claims, Generate Verification Questions, Independent Verification, Consistency Check, Synthesize and Score Impact)
- **Overall Assessment:** REVISE (targeted, single-sentence correction to CV-001; CV-002 optional). No new machinery implied — both corrections are text-only, consistent with the subtraction doctrine already governing this package across iterations 5-8.

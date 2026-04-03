# Quality Score Report: Dependabot Configuration (#188)

## L0 Executive Summary
**Score:** 0.83/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.74)
**One-line assessment:** The config is functionally correct and well-commented, but it silently deviates from its own FMEA research without citing the risk analysis document or explaining the deviations — fix the reference gap and justify the simplifications to reach 0.95.

---

## Scoring Context
- **Deliverable:** `.github/dependabot.yml`
- **Deliverable Type:** Design / Configuration
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Custom Threshold:** 0.95 (user-specified, above standard H-13 gate of 0.92)
- **Research Incorporated:** `projects/PROJ-030-bugs/research/merge-queue-vs-dependabot-grouping.md`, `projects/PROJ-030-bugs/research/dependabot-risk-analysis.md`
- **Scored:** 2026-03-12

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.83 |
| **Threshold** | 0.95 (user-specified) |
| **Standard H-13 Gate** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 2 research documents read in full |

---

## CRITICAL CHECK Result: `allow: dependency-type: direct`

**Does it work as described? YES — with one unverified nuance.**

The claim: "only open PRs for packages listed directly in pyproject.toml (and requirements*.txt), not for transitive deps like gherkin-official."

The `allow: dependency-type: direct` filter is correct per the Dependabot options reference. Dependabot infers direct vs. indirect dependency status from the manifest structure — packages with `# via <parent>` annotations in requirements files are classified as indirect. `gherkin-official` (appearing as `# via pytest-bdd` in `requirements-test.txt`) would be excluded.

**Unverified nuance:** The comment says the filter applies to "requirements*.txt" files. The `allow` block is scoped to the `pip` ecosystem block at directory `/`. Dependabot does scan all `requirements*.txt` files in that directory for the pip ecosystem. The claim is correct in practice, but the config comment does not explain the mechanism (how Dependabot distinguishes direct from indirect in requirements files via `# via` annotations). A contributor encountering an unexpected transitive dep in a future PR could be confused.

**The `allow: direct` approach also serves as a substitute for the ignore list.** The risk analysis (R-5) recommended adding explicit ignore entries for `gherkin-official`, `mako`, `markupsafe`, `six`, `parse`, `parse-type`. D3 explains the alternative approach: `allow: direct` is more durable than an ignore list. This is methodologically sound — but the D3 comment does not cite the risk analysis, so the reader cannot trace the deliberate substitution.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 7 design decisions documented; both ecosystems covered; no missing required fields |
| Internal Consistency | 0.20 | 0.82 | 0.164 | YAML/comment alignment is strong; D1 rationale does not address R-4 markdown cross-constraints from risk analysis |
| Methodological Rigor | 0.20 | 0.83 | 0.166 | Risk-tiered approach is sound; `allow: direct` is durable policy; simplification from 3-tier FMEA recommendation to 2-tier is not fully justified |
| Evidence Quality | 0.15 | 0.78 | 0.117 | Research file (merge-queue) cited; risk analysis (FMEA) not cited despite direct relevance to design decisions |
| Actionability | 0.15 | 0.87 | 0.1305 | Inline comments are detailed; future-oriented guidance present; divergence from research could confuse |
| Traceability | 0.10 | 0.74 | 0.074 | D1-D7 numbered and traceable; risk analysis document absent from references; deviations from R-1/R-2/R-3/R-4 not traced |
| **TOTAL** | **1.00** | | **0.8275** | |

Rounded to 2dp: **0.83**

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**

All 7 stated design decisions (D1-D7) have corresponding YAML implementation:
- D1 implemented: `pip-minor-patch` group with `update-types: [minor, patch]`; major ungrouped (lines 136-147)
- D2 implemented: `actions-minor-patch` group; major ungrouped (lines 106-115)
- D3 implemented: `allow: dependency-type: direct` (lines 134-135)
- D4 documented in comment (lines 41-52); no additional YAML needed (correct)
- D5 implemented: `prefix: ci` and `prefix: deps` (lines 101, 126)
- D6 implemented: `open-pull-requests-limit: 10` for both ecosystems (lines 105, 129)
- D7 implemented: labels match stated intent (lines 103-104, 128)

Both relevant ecosystems for Jerry are covered: `github-actions` and `pip`. No `docker`, `npm`, `cargo`, or other ecosystems are in Jerry's stack — omission is correct.

**Gaps:**

- The config does not include a `directory: /` check for `requirements-test.txt` and `requirements-dev.txt` explicitly; these are implied by the pip ecosystem block but not stated. A contributor unfamiliar with Dependabot's behavior might not know these are covered.
- R-6 from the risk analysis ("add `open-pull-requests-limit: 0` override or separate security block") is not implemented. D4 explains this is handled by Dependabot's default behavior (security updates are event-driven and ungrouped by default) — this is correct, but the config cannot enforce the "individual security PRs" policy at the YAML level without an explicit `applies-to: security-updates` block with no `groups` key. If someone adds `groups` globally in the future, security updates would be affected. A defensive explicit security block would be more complete.
- Risk analysis conclusion #3 (runtime deps should NOT be grouped) is not reflected — runtime deps are grouped with dev/test deps in `pip-minor-patch`. D1 argues this is acceptable at current scale, but this is a scope reduction from the research recommendation.

**Improvement Path:**

Add an explicit comment noting that security updates are ungrouped by default AND note that adding any `groups` key with `applies-to: security-updates` would override this. Add `dependabot-risk-analysis.md` to the References section.

---

### Internal Consistency (0.82/1.00)

**Evidence:**

Strong YAML-to-comment alignment throughout:
- Line 107-109: comment "D2: Patch + minor SHA rotations..." matches `update-types: [minor, patch]` on lines 111-113
- Line 131-133: comment "D3: Only bump direct dependencies..." matches `allow: dependency-type: direct` on line 135
- Line 137-142: comment "D1: Patch + minor updates grouped..." matches `pip-minor-patch` group on lines 140-143
- Line 114: comment "Major updates remain ungrouped" matches absence of major in the actions group
- Line 144-146: comment "Major updates remain ungrouped" matches absence of major in pip group

D5 commits: "ci" for actions and "deps" for pip. Both referenced in D5 rationale (line 57): "Both prefixes are caught by version-bump.yml Filter B (#187)." This is verifiable and consistent.

D6 pip limit raised from 5 to 10. The comment at line 69 states "The old limit of 5 could queue PRs when multiple majors are pending simultaneously." This rationale is internally consistent with the ~8 runtime + ~4 dev direct deps count stated on lines 67-68.

**Gaps:**

The risk analysis (L1 section 3) identifies that runtime deps `markdown-it-py`, `mdformat`, and `mdit-py-plugins` share transitive deps and have tight cross-constraints:

> "markdown-it-py and mdformat share markdown-it-py as a transitive dep; mdformat pins to a range" (risk analysis, section 3, MEDIUM risk)

D1's rationale (lines 8-15) addresses the dev/test split question only on the basis of dep count (~20) and risk profile symmetry. It does not address the cross-constraint issue in the markdown family specifically identified by the FMEA. A reader comparing D1 to the risk analysis would see an unexplained inconsistency: the FMEA flagged a MEDIUM cross-constraint risk that D1's rationale doesn't acknowledge.

Similarly, D2 says major Actions updates remain ungrouped because they "can change behavior." The risk analysis R-1 recommends grouping ALL Actions including major (all RPNs < 50). The config's more conservative D2 approach is defensible, but the inconsistency with the cited research is unaddressed.

**Improvement Path:**

Add a sentence to D1 explicitly acknowledging the markdown cross-constraint risk and explaining why `allow: direct` (which would exclude any transitives in that family) mitigates it, or why the risk is acceptable. Add a note to D2 that R-1 recommends grouping major Actions but the config takes a more conservative approach.

---

### Methodological Rigor (0.83/1.00)

**Evidence:**

The core risk-tiered methodology is sound:
- Patch + minor: grouped (SemVer backward-compatibility contract provides a baseline)
- Major: individual (API changes, behavior changes, breaking changes require per-item review)
- Security: individual by default (no YAML action required; correct per Dependabot behavior)

The `allow: dependency-type: direct` policy for transitive dep filtering is methodologically superior to an ignore list, as D3 argues correctly: ignore lists are whack-a-mole (new transitive deps emerge), while `allow: direct` is a durable declarative policy. This is the most methodologically rigorous decision in the config.

The D3 explanation of how transitive deps update ("pytest-bdd bump pulls in the compatible gherkin-official version via uv.lock") is accurate and demonstrates understanding of the uv resolver mechanism.

SHA-pinning rationale for Actions (D2) correctly identifies that "minor" for pinned Actions is a SHA swap with low behavioral risk, supporting the grouping of minor updates.

**Gaps:**

The FMEA recommended a three-tier grouping structure:
- Group A: pip dev tools (ruff, mypy, pyright, pre-commit, etc.)
- Group B: pytest ecosystem (pytest, pytest-bdd, pytest-cov, pytest-archon) — SEPARATE from dev tools
- No grouping for runtime deps

The config collapses this to a single `pip-minor-patch` group for all direct deps. D1 justifies this with a dep count argument but does not engage with the FMEA's core rationale for separation: the pytest ecosystem has demonstrated transitive conflict risk (RPN 120, gherkin-official incident) that is independent of the dev tools. The `allow: direct` policy does mitigate this by excluding `gherkin-official`, but the relationship between `allow: direct` and the FMEA's separation recommendation is not made explicit.

This gap means the methodological justification is incomplete — a reader cannot fully reconstruct why the simpler two-tier approach is equivalent to the FMEA's three-tier recommendation given the `allow: direct` policy.

**Improvement Path:**

Add a sentence to D1: "Note: the risk analysis recommended separating dev tools from the pytest ecosystem (to isolate RPN 120 transitive conflict risk). The `allow: direct` policy (D3) eliminates this risk by excluding all transitive deps including gherkin-official, making the separation unnecessary at current dep count."

---

### Evidence Quality (0.78/1.00)

**Evidence:**

Referenced sources that are present and accurate:
- `projects/PROJ-030-bugs/research/merge-queue-vs-dependabot-grouping.md` — correct path, correctly describes content (Dependabot grouping research)
- `.github/workflows/version-bump.yml (#187)` — correct reference to Filter B
- `EN-001` — correct reference for SHA pinning
- GitHub docs URL (line 85) — points to the Dependabot options reference, which is the canonical source for `allow: dependency-type: direct`

The `allow: dependency-type: direct` claim is well-supported: the GitHub docs URL is the authoritative source for this behavior.

**Gaps:**

The `dependabot-risk-analysis.md` file is NOT referenced anywhere in the config. This is the FMEA document that:
- Contains the RPN analysis (RPN 120 for pytest-bdd/gherkin transitive conflict)
- Made specific grouping recommendations (R-1 through R-8)
- Is directly contradicted or modified by D1 (no runtime/dev separation), D2 (major Actions ungrouped vs. R-1's all-inclusive grouping), and D3 (allow:direct vs. R-5's ignore list)

A contributor reading the config and then reading the risk analysis would see recommendations that differ from the implementation with no explanation in the config of why. This is a significant evidence quality gap: the config's most important evidentiary basis (the FMEA) is uncited.

The D3 claim that `allow: dependency-type: direct` "tells Dependabot to only open PRs for packages listed directly in pyproject.toml (and requirements*.txt)" is correct but the mechanism (Dependabot's use of `# via` annotations to classify indirect deps) is not cited. For a contributor who later encounters an unexpected PR for a package that appears in `requirements-test.txt` without a `# via` annotation, the comment provides no debugging guidance.

**Improvement Path:**

Add `dependabot-risk-analysis.md` to the References section. In D1 and D2 comments, note that the risk analysis recommended different groupings and explain the deliberate simplification.

---

### Actionability (0.87/1.00)

**Evidence:**

The config is highly actionable for a contributor:
- 7 numbered design decisions provide the "why" for each configuration choice
- D1 provides a future trigger: "If the dep count grows past ~40, reconsider splitting" (line 14-15)
- D4 provides operational guidance: "Security updates must be enabled in repo Settings > Code security" (line 48-49) — this is actionable for someone setting up the repo
- D4 explains how to add security update grouping in the future (line 52)
- D7 explains what would be needed to add risk-tier labels (lines 77-79)
- D3 explains how to change the approach if the `allow: direct` policy proves insufficient (line 31-32: "Excluding it by name is whack-a-mole" — implicitly acknowledges `exclude-patterns` as the alternative)
- Inline YAML comments at lines 107-114, 130-135, 137-146 link YAML blocks to design decision numbers

D6 explains the `open-pull-requests-limit` values with dep count arithmetic, making it easy to recalculate when deps are added.

**Gaps:**

The divergence between this config and the risk analysis creates an actionability problem: if a contributor reads both documents to understand the configuration rationale, they will encounter the risk analysis's recommendation to NOT group runtime deps (R-4) and to separate dev tools from the pytest ecosystem (R-3), but the config provides no guidance on this divergence. A contributor modifying the grouping strategy could inadvertently reintroduce the problem the FMEA warned about.

The `allow: dependency-type: direct` mechanism's reliance on Dependabot's `# via` annotation parsing is not explained. A contributor who adds a new dependency and sees unexpected Dependabot behavior would not have enough context from the comment to debug it.

**Improvement Path:**

Add a note to D3 explaining the `# via` mechanism that enables `allow: direct` to correctly classify transitives. Add a cross-reference in D1 to the risk analysis's R-3/R-4 reasoning and why it does not apply given D3.

---

### Traceability (0.74/1.00)

**Evidence:**

Present traceability chains:
- D1-D7 are numbered and each maps to specific YAML lines (verifiable)
- Issue #188 appears in the config title (line 1)
- Filter B (#187) is referenced in D5 (line 57)
- EN-001 is referenced in D2 and in the Actions section comment (line 93)
- Research file path is in the References section (line 82)
- GitHub docs URL provides canonical source for `allow` syntax (line 85)

**Gaps:**

Three significant traceability gaps:

1. **`dependabot-risk-analysis.md` is absent from References.** This document contains the FMEA that directly informs the grouping decisions. Without it in the References section, the traceability chain from "design decisions" to "evidence" is broken for the most substantive design choices.

2. **Divergence from R-1 is untraced.** The risk analysis R-1 recommends grouping ALL Actions including major. D2 keeps major Actions ungrouped. There is no comment in D2 acknowledging this deviation from the research recommendation. A reviewer cannot determine whether this was a conscious override or an oversight.

3. **Divergence from R-2/R-3/R-4 is partially traced but incomplete.** D1 explains why dev/test/runtime are not separated (dep count argument) but does not cite R-4's runtime dep grouping concern or explain why `allow: direct` renders R-3's pytest ecosystem separation unnecessary. The connection between the FMEA's recommendations and the implemented approach exists in the designer's head but is not in the document.

4. **No issue reference in individual YAML blocks.** The REFERENCES comment (lines 81-85) at the top of the file is good, but individual YAML blocks do not cross-reference their decision rationale numerically to the REFERENCES section. A contributor reading just the YAML (not the header comments) has no pointer back to the research.

**Improvement Path:**

Add `dependabot-risk-analysis.md` to the References section. In D2, add: "Note: the risk analysis recommended grouping major Actions (R-1); this config takes a more conservative approach given recent v5->v6 and v4->v7 major bumps requiring individual review." In D1, add: "Note: the risk analysis recommended separating dev tools from pytest ecosystem (R-2, R-3) and not grouping runtime deps (R-4); the `allow: direct` policy (D3) eliminates the RPN 120 transitive conflict risk that motivated those separations, making the simpler unified group acceptable."

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.74 | 0.88 | Add `dependabot-risk-analysis.md` to the References section (line 82 area). This single change improves both Traceability and Evidence Quality. |
| 2 | Internal Consistency | 0.82 | 0.90 | In D1, add a sentence acknowledging R-4 (runtime deps not grouped) and explaining that `allow: direct` + the markdown cross-constraint analysis is why the unified group is acceptable. |
| 3 | Methodological Rigor | 0.83 | 0.90 | In D1, make the connection explicit: "`allow: direct` (D3) eliminates gherkin-official class of incident (RPN 120), making the single unified group equivalent in risk to the FMEA's three-group structure." |
| 4 | Traceability | 0.74 | 0.88 | In D2, acknowledge the divergence from R-1 (FMEA recommended grouping all Actions including major): "Risk analysis R-1 recommended grouping major Actions too (all RPNs < 50), but this config takes a conservative approach given recent major-version behavioral changes." |
| 5 | Evidence Quality | 0.78 | 0.88 | Add a sentence to D3 explaining the `# via` annotation mechanism: how Dependabot uses `requirements*.txt` `# via` comments to classify packages as indirect, and why this means `gherkin-official` (appearing as `# via pytest-bdd`) is correctly excluded by `dependency-type: direct`. |

---

## Leniency Bias Check
- [x] Each dimension scored independently — all 6 scored before composite computed
- [x] Evidence documented for each score — specific YAML line numbers and research section citations
- [x] Uncertain scores resolved downward — Traceability was considered 0.76, rounded down to 0.74; Methodological Rigor considered 0.85, rounded down to 0.83
- [x] First-draft calibration considered — this is a well-constructed config, not a first draft; 0.83 is appropriate for a good config with specific traceable gaps
- [x] No dimension scored above 0.95 without exceptional evidence — highest dimension is Actionability at 0.87

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.83
threshold: 0.95
weakest_dimension: traceability
weakest_score: 0.74
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add dependabot-risk-analysis.md to References section"
  - "In D1, explain how allow:direct renders FMEA R-3/R-4 separation recommendations unnecessary"
  - "In D2, acknowledge deviation from risk analysis R-1 (group all Actions including major)"
  - "In D3, explain the # via annotation mechanism that enables allow:direct to correctly classify transitives"
  - "All 4 improvements are comment-only changes to the YAML header — no functional YAML changes needed"
```

---

*Scored by: adv-scorer*
*Strategy: S-014 LLM-as-Judge*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-12*

---
type: adversarial-findings
strategy: S-001
iteration: 8
status: COMPLETE
---

# Red Team Report: ADR-PROJ031-004 / adr-standards-rule-draft.md (Post-Subtraction-Pass, iteration 8)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Full evidence per finding |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasures |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |

---

## Header

**Strategy:** S-001 Red Team Analysis
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`

**Criticality:** C4
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-001, iteration 8, blind independent reviewer)
**H-16 Compliance:** S-003 Steelman is embedded in the deliverable per its own disclosure (ADR lines 65-67: every Option A-F leads with a blind-advocate steelman case sourced from `explore/advocate-*.md`); prior iterations (004/006/007) reference `ST-001`/`ST-002` tags built on that steelman work. Treated as satisfied for this blind execution — this iteration does not re-litigate H-16 compliance.
**Threat Actor:** A contributor (careless OR deliberate) who wants to mint a new ADR quickly and is willing to exploit the gap between what the 5-rule lint core (L-1/L-2/L-3/L-4/L-7) actually *scans* and what the convention's *documented identity model* actually *is*, to create an ADR whose identity collides with, or shadows, an existing one without the lint ever firing and without any existing residual note (R-1…R-13) covering the gap.

**Scope note (per invoking mandate).** This iteration targets one question: *can a contributor create colliding/shadowing IDs that the 5-rule core misses, and if so, is that gap DISCLOSED as a residual (acceptable under the subtraction pass's own MEDIUM-tier, delete-don't-compensate doctrine) or CLAIMED as covered (Critical)?* The subtraction pass's doctrine itself, and the MEDIUM-tier/no-new-HARD-rule posture, are accepted as valid per `.context/rules/quality-enforcement.md` Tier Vocabulary and are **not** re-litigated here as generic complaints. Vectors that are already honestly disclosed (R-9 case-fold, R-10 out-of-scan location class, R-11 relationship asymmetry, R-13 title-slug-tail extraction) were independently re-derived and verified during this pass and are **not** re-reported as new findings — they are noted in [Vectors Verified As Already-Disclosed](#vectors-verified-as-already-disclosed-not-reported-as-findings) for evidentiary completeness, per P-022 (this reviewer will not claim credit for findings the package already owns).

---

## Summary

The post-subtraction package is unusually thorough in its own residual self-disclosure (12 named risks R-1…R-13 across 7 prior adversarial iterations, several with shell-verified reproduction steps). Independently re-deriving the obvious ID-collision/shadowing vectors (case-fold shadowing, cross-topology/entity-embedded out-of-scan, title-slug-tail regex false negatives, relationship-field asymmetry) confirms all of them are already honestly disclosed as residuals, not claimed as covered — that portion of the mandate's test is **passed**.

However, one materially different, previously-undisclosed collision vector was found: **the frontmatter `id:` field — which the schema itself labels "canonical subject identity" (ADR-M-001) — is never read, validated, or deduplicated by any of the 5 lint rules.** L-1/L-2/L-3/L-4 operate purely on filenames; L-7 only resolves three specific relationship-field targets. A contributor can therefore create a new, uniquely-named, fully L-1/L-2/L-3/L-4/L-7-compliant file whose frontmatter `id:` duplicates an existing ADR's canonical identity — a routine copy-paste-template authoring error, or a deliberate act — completely undetected, and this specific gap is **not named anywhere** in the residual register (R-1…R-13), the "Descoped" list, or the Changelog, despite that register explicitly covering the closely-adjacent concerns of relationship-field duplication (FM-011, supersession cycles) and provenance-field correctness (FM-104/R-A). This is classified **Critical** (RT-001): the rule's own name, "L-3 No duplicate ID," reasonably reads as covering exactly this scenario, and no disclosure narrows that claim.

Two Major findings and one Minor finding round out the report, all related to disclosure completeness/consistency around the identity model rather than to the subtraction doctrine itself. **Recommendation: REVISE (not REJECT)** — the fix for the Critical is a small, non-machinery addition (either a one-sentence guidance clause + a disclosed residual entry, or a small widening of the existing pre-flight one-liner to also dedupe `id:` values), fully consistent with the subtraction pass's own established precedent (the iter-6 RT-101/DA-001 character-class widening).

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|--------------------|
| RT-001-20260706 | Frontmatter `id:` field duplicates an existing ADR's canonical identity while the filename stays unique and fully L-1/L-2/L-3/L-4/L-7-compliant | Boundary (identity model has two representations — filename and frontmatter `id:` — with no cross-check) | High | Critical | P0 | Missing | Completeness, Internal Consistency |
| RT-002-20260706 | No MEDIUM standard (ADR-M-001…M-013) states that frontmatter `id:` MUST/SHOULD equal the file's own filename-derived identity | Ambiguity | High | Major | P1 | Missing | Completeness |
| RT-003-20260706 | Disclosure-depth asymmetry between the two co-produced deliverables: the ADR's R-9 risk entry names the case-insensitive-filesystem collision consequence; the rule draft's L-1 row and Frozen/Grandfathered section (the artifact contributors actually consult day-to-day) omit that consequence | Degradation (residual erodes at the operational surface) | Medium | Major | P1 | Partial | Traceability |
| RT-004-20260706 | Rule draft's "Frozen and Grandfathered Legacy" section lists `150×1` inside the same enumeration as "grandfathered dialect families," though `ADR-150-001` does not match the closed dialect grammar and is grandfathered only via the separate pre-adoption-exemption mechanism — conflating the two could mislead an author into thinking a new numeric-leading ID is a viable pattern | Ambiguity | Low | Minor | P2 | Partial | Internal Consistency |

**Finding ID Format:** `RT-{NNN}-20260706` (execution_id = iteration-8 date).

---

## Finding Details

### RT-001: Frontmatter `id:` duplication is invisible to the entire 5-rule lint core [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Rule draft: [Frontmatter Schema](../../../../design/adr-standards-rule-draft.md#frontmatter-schema) (lines 100-119) and [L5 CI Lint Specification](../../../../design/adr-standards-rule-draft.md#l5-ci-lint-specification) (lines 161-197, esp. L-3 row line 175); ADR: [L1: Technical Implementation → Frontmatter](#) (lines 338-370) and [Enforcement Design](#) L-3 row (line 669) |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) + Step 3 (Assess Defense Gaps) |

**Attack Vector:** The scheme defines an ADR's identity in **two places**: (1) the filename (`ADR-{domain-slug}-NNN-{title-slug}.md`), and (2) the frontmatter `id:` field, which the schema comment explicitly calls **"canonical subject identity (ADR-M-001)"** (rule draft line 102: `id: ADR-plugin-distribution-001     # canonical subject identity (ADR-M-001)`; ADR line 342 carries the identical comment). Every one of the 5 lint rules operates on the **filename only**:
- **L-1 (Grammar)** matches the filename against canonical/dialect regexes (rule draft lines 68-71).
- **L-2 (No new bare)** matches the filename against `^ADR-\d` (rule draft line 174).
- **L-3 (No duplicate ID)** extracts `{slug}-NNN` via `find | sed | grep | sed | sort | uniq -d` — every stage of that pipeline (rule draft lines 183-195, reproduced verbatim at ADR lines 397-406) operates on the **file path string**, never on file *content*. The rule draft states this explicitly is "exactly what L-3 runs in CI" (rule draft line 181; ADR line 391).
- **L-4 (ID↔location)** matches a dialect *filename* prefix against its containing directory (rule draft line 176).
- **L-7 (Relationship target resolves)** parses frontmatter YAML, but **only** to check that `superseded_by`/`promoted_to`/`promoted_from` values point to *some* existing ADR (rule draft line 177; ADR line 671) — it never checks whether a file's **own** `id:` field is unique across the corpus, nor whether it matches that file's own filename.

**Concrete exploitation path:** A contributor copies an existing compliant ADR (e.g. `docs/design/ADR-agent-design-001-canonical-format.md`, whose frontmatter reads `id: ADR-agent-design-001`) as a starting template for a genuinely new decision, gives the **new file** a distinct, fully-compliant filename (e.g. `docs/design/ADR-agent-design-002-security-review.md`) — which passes L-1 cleanly and does **not** collide under L-3, because L-3's extracted key (`ADR-agent-design-002`) differs from the original (`ADR-agent-design-001`) — but forgets to update the frontmatter `id:` field (buried in a YAML block, distinct from the visible filename/title the author is focused on). The result: two files on disk, `...-001-...md` and `...-002-...md`, both individually L-1/L-2/L-3/L-4/L-7-clean, yet **both internally declaring `id: ADR-agent-design-001`.** No rule in the 5-rule core detects this. This is exploitable either as an honest authoring mistake (high plausibility — "duplicate file, forget to update one buried field" is one of the most common copy-paste bugs there is) or deliberately, by an author who wants a new file to be silently treated as "the same ADR" by any tool that resolves identity via frontmatter rather than filename.

**Category:** Boundary violation — the scheme maintains two parallel representations of "identity" (filename-derived and frontmatter-declared) with a boundary between them that nothing traverses/verifies.

**Exploitability:** High — requires no adversarial sophistication, only a routine copy-paste-and-rename authoring workflow; no lint stage reads file content for this check.

**Severity:** Critical — per the S-001 rubric, this is a "complete bypass" of the specific protection L-3 is named for ("No duplicate ID"). It is not a partial degradation of that protection (as R-9/R-13 are for the filename-based check); it is a wholesale blind spot for an entire, schema-mandated identity representation. The consequence compounds: **L-7's own relationship-resolution mechanism** depends on frontmatter parsing to find "an existing ADR" matching a `superseded_by`/`promoted_to` target — if that resolution is implemented (as the most natural reading of L-7 suggests) by matching against `id:` values rather than re-deriving from filenames, a duplicate `id:` makes L-7's own resolution **non-deterministic or silently wrong** (which of the two files does the relationship actually point to?), meaning this gap is not merely "undetected," it can actively corrupt the one relationship-integrity check the core does perform.

**Existing Defense:** None. Not L-1 (filename-only). Not L-3 (filename-only, explicitly confirmed by its own "exactly what L-3 runs" bash-snippet framing). Not L-7 (only resolves 3 specific relationship fields' *target existence*, never a file's own `id:` uniqueness or filename-agreement).

**Evidence (undisclosed status, verified per P-022):** The exhaustive residual register — R-1 through R-13 in the ADR's [Risks](#) table (lines 450-462) and the rule draft's "Descoped, honestly" note (rule draft lines 197; ADR line 674) — covers many closely-adjacent concerns in detail: case-fold filename shadowing (R-9), out-of-scan location classes (R-10), relationship-field asymmetry / supersession cycles where "two ADRs both claim `superseded_by` the same target" (R-11, and explicitly FM-011 at ADR line 599: *"No rule in the 5-rule core structurally prevents a supersession cycle... or two ADRs both claiming `superseded_by` the same target"*), and provenance-field correctness — *"a copy-pasted or stale `origin_project` value passes undetected"* (ADR line 427, FM-104). **None of these entries, nor the Descoped list, names the base `id:` field's own uniqueness or its agreement with the filename.** Grepped both files for `R-14` and for any `id:`-uniqueness/consistency language: no match (see verification note below). Given the corpus's demonstrated diligence in naming even low-probability residuals (R-8's YAML/blockquote drift, LOW/LOW-MED; R-12's self-approval condition, LOW/LOW), the absence of this one — which is both higher-exploitability and structurally closer to the core L-3 claim than several of the named ones — reads as a genuine oversight rather than a deliberate, disclosed exclusion.

**Dimension:** Completeness (the "no duplicate ID" protection is materially incomplete for a schema-mandated identity field); Internal Consistency (the schema declares `id:` "canonical" while no mechanism treats it as such).

**Countermeasure:** Disclose as a new residual (parallel to R-9…R-13) **and/or** close it with a small, non-machinery widening of the existing L-3 mechanism — consistent with the subtraction pass's own precedent for handling exactly this class of gap (the iter-6 RT-101/DA-001 fix widened L-3's character class rather than adding a new rule; the same "widen the existing rule, add no new mechanism" move applies here: extend the pre-flight one-liner / L-3 spec to also `grep '^id:'` each file and fold those values into the same `sort | uniq -d` pipeline). Either close it (preferred, given precedent) or disclose it explicitly with SHOULD-guidance that `id:` MUST equal the filename-derived identity.

**Acceptance Criteria:** Either (a) a new disclosed residual entry (e.g. R-14) appears in both deliverables' registers stating the `id:`-vs-filename divergence is undetected, with SHOULD-NOT guidance against letting them diverge; or (b) the L-3 spec and pre-flight one-liner in both deliverables are updated to also compare frontmatter `id:` values, with the grandfather regression test re-run to confirm no false positives against the existing 18-file corpus.

---

### RT-002: No MEDIUM standard requires `id:` to agree with the filename [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Rule draft: [MEDIUM Standards](../../../../design/adr-standards-rule-draft.md#medium-standards) (lines 42-59, ADR-M-001 through ADR-M-013) |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) |

**Attack Vector:** Even at the pure-guidance level (before any lint exists — recall the lint is "designed, not built," rule draft line 38/163), there is no textual instruction anywhere in ADR-M-001 through ADR-M-013 that the frontmatter `id:` value must equal the file's own filename-derived identity. ADR-M-001 describes the filename grammar; ADR-M-002 describes where *origin* goes (not `id:` itself); none of the thirteen standards states the cross-field consistency requirement. This is the root cause of RT-001: even a maximally good-faith author following every SHOULD in the document has no explicit instruction to keep the two representations in sync.

**Category:** Ambiguity — an undefined relationship between two fields the schema otherwise treats as both "the identity."

**Exploitability:** High — same authoring workflow as RT-001; this finding is about the guidance layer being silent, independent of whether a lint ever exists.

**Existing Defense:** None named.

**Dimension:** Completeness.

**Countermeasure:** Add one clause (no new rule ID needed — could be folded into ADR-M-001 itself, e.g. "...`{title-slug}` an optional human tail. The frontmatter `id:` value SHOULD exactly equal this filename-derived identity string.") Zero new machinery, consistent with subtraction doctrine.

**Acceptance Criteria:** ADR-M-001 (or an adjacent standard) states the `id:`-equals-filename expectation explicitly.

---

### RT-003: Rule draft's operational disclosure of R-9 is thinner than the ADR's [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Rule draft L-1 row (line 173) and "Frozen and Grandfathered Legacy" (line 92-94) vs. ADR Risk table R-9 entry (line 458) |
| **Strategy Step** | Step 3 (Assess Defense Gaps) |

**Attack Vector:** The ADR's own Risk-register entry for R-9 is precise and complete: *"a lowercase slug that case-folds to a dialect prefix (`ADR-proj031-001` shadowing `ADR-PROJ031-001`) passes L-1 as a distinct identity; **and** on a case-insensitive filesystem (macOS/Windows default) two canonical slugs differing only in case are the *same* file path, an OS-level collision the `sort|uniq -d` (case-sensitive) does not flag"* (ADR line 458). The **rule draft** — which is the document that actually installs to `.context/rules/adr-standards.md` and is the artifact contributors and agents consult day-to-day, per its own stated purpose (rule draft line 3: "companion to `ADR-PROJ031-004`... on the M-2 move this content — minus this wrapper — becomes `.context/rules/adr-standards.md`") — states only the filename-shadowing half of R-9 at its L-1 row (rule draft line 173: *"a lowercase slug that case-folds to a dialect prefix... shadowing... passes L-1 as a distinct identity"*) and omits the case-insensitive-filesystem/OS-level-collision consequence entirely, both there and in the Frozen/Grandfathered section (lines 92-94).

**Category:** Degradation — the residual's severity information erodes specifically at the surface a contributor is most likely to consult, since the ADR (which carries the fuller disclosure) is a one-time decision record, not an auto-loaded rule.

**Exploitability:** Medium — a contributor relying solely on the rule draft (the intended operational artifact) would correctly learn "don't pick a slug that case-folds to a dialect prefix" but would not learn the more concrete why (a real cross-platform repo-breaking checkout conflict, not merely a look-alike/discoverability nuisance), which weakens the practical incentive to follow the SHOULD-NOT guidance.

**Existing Defense:** Partial — the underlying gap (R-9) is disclosed; only the full severity rationale is thinner in the operational copy.

**Dimension:** Traceability (the two co-produced deliverables should carry parity on a residual they both reference by the same `R-9` shorthand).

**Countermeasure:** Copy the case-insensitive-filesystem sentence from the ADR's R-9 entry into the rule draft's L-1 row (or its Frozen/Grandfathered section). Zero new machinery — a disclosure-parity fix.

**Acceptance Criteria:** Rule draft's L-1 row or Frozen/Grandfathered section names the case-insensitive-filesystem consequence, matching the ADR's R-9 entry.

---

### RT-004: `150×1` mislabeled as a "grandfathered dialect family" [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Rule draft "Frozen and Grandfathered Legacy" (line 94) |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) |

**Attack Vector:** Rule draft line 94 reads: *"**Grandfathered** dialect families (`PROJ010`×6/`PROJ022`×2/`PROJ031`×4/`EPIC002`×2/`STORY015`×1/`150`×1) remain valid in place, extendable within their dialect."* But `ADR-150-001` does **not** match the closed dialect grammar `^ADR-(PROJ|EPIC|FEAT|STORY)\d{3}-\d{3}` (rule draft line 71) — it is a numeric-leading, GH-issue-scoped legacy ID that fails **both** canonical and dialect regexes, and is explicitly called out elsewhere as such: *"the leading slug token has to begin with a letter (so `ADR-150-001` is not a canonical slug; grandfathered)"* (rule draft line 70). Its grandfathering therefore rests on a **different** mechanism — the pre-adoption exemption ("checks git-added/modified files," rule draft line 171) — not on "dialect" status. Listing it inside the same "dialect families... extendable within their dialect" sentence conflates two distinct grandfathering mechanisms and could mislead a reader into believing a *new* numeric-leading GH-issue-scoped ID (e.g. `ADR-237-001`) is a viable, extendable pattern going forward, when in fact L-1 would reject it for any new (git-added) file.

**Category:** Ambiguity.

**Exploitability:** Low — requires a reader to misparse one sentence; the correct rule is stated unambiguously elsewhere in the same document (line 70).

**Existing Defense:** Partial — the correct rule exists nearby; only this one summary sentence conflates the two mechanisms.

**Dimension:** Internal Consistency.

**Countermeasure:** Split the sentence: list `150×1` separately as "1 pre-adoption-exempt legacy numeric ID (not a recognized dialect; not extendable — a new file must use canonical or a closed-set dialect)."

**Acceptance Criteria:** The "Frozen and Grandfathered Legacy" section no longer implies `150` is a member of the extendable dialect set.

---

## Vectors Verified as Already-Disclosed (Not Reported as Findings)

Per P-022, listed here for evidentiary completeness rather than re-claimed as new findings — each was independently re-derived from the ID grammar/lint mechanics during this pass, then confirmed already named in the corpus:

| Vector re-derived | Confirmed disclosed at |
|---|---|
| Case-folded slug shadowing a dialect prefix (`ADR-proj031-001` vs `ADR-PROJ031-001`), incl. case-insensitive-filesystem collision | ADR Risk R-9 (line 458); rule draft L-1 row (line 173, partial — see RT-003) |
| Entity-embedded (`work/.../{ENTITY}/`) and repository-based-topology (`{RepositoryRoot}/decisions/`) ADRs are permitted "Active" locations yet structurally out of L-1/L-3/L-7's scan path — an ongoing location-*class* gap, not a single historical instance | ADR Risk R-10 (line 459), explicitly generalized "not one bounded instance" |
| L-3's greedy title-slug-tail extraction can mis-key a genuine duplicate when the tail carries a standalone 3-digit token, producing a false negative | ADR Risk R-13 (line 462), shell-verified reproduction given |
| L-7 checks only 3 of 6 relationship fields; `supersedes`/`amends`/`amended_by` unchecked; two ADRs could both claim `superseded_by` the same target with nothing to catch it | ADR Risk R-11 (line 460) and FM-011 (line 599) |
| Cross-branch same-slug `NNN` race invisible until merge | ADR Risk R-6 (line 455) |
| Slug reuse for an unrelated subject (semantically wrong but structurally identical to a legitimate sequence extension) | ADR Risk R-7 (line 456/439) |
| Repository-based topology: L-4 has zero (not merely degraded) operative effect | ADR line 385, 670; rule draft line 176 |

---

## Recommendations

**P0 (MUST mitigate before acceptance at the 0.95 engagement gate):**
- **RT-001:** Either (a) add a disclosed residual (new `R-14` in both deliverables' registers) stating the frontmatter `id:` field is never read/deduplicated by the 5-rule core and can diverge from the filename-derived identity undetected, with SHOULD-guidance that the two must agree; or (b), preferred given the iter-6 precedent of widening an existing rule rather than adding a new one (RT-101/DA-001), extend the L-3 pre-flight one-liner and spec (both deliverables) to also extract and dedupe the frontmatter `id:` field. Acceptance criteria as stated in [RT-001](#rt-001-frontmatter-id-duplication-is-invisible-to-the-entire-5-rule-lint-core-critical).

**P1 (SHOULD mitigate):**
- **RT-002:** Add one sentence to ADR-M-001 requiring `id:` to equal the filename-derived identity.
- **RT-003:** Copy the case-insensitive-filesystem sentence from the ADR's R-9 entry into the rule draft.

**P2 (MAY mitigate):**
- **RT-004:** Split the `150×1` entry out of the "dialect families" enumeration in the rule draft's Frozen/Grandfathered section.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-001/RT-002: the "no duplicate ID" protection has a complete, undisclosed blind spot for the schema-mandated `id:` field |
| Internal Consistency | 0.20 | Negative | RT-001: schema calls `id:` "canonical" but no mechanism treats it as such; RT-004: minor conflation of two grandfathering mechanisms |
| Methodological Rigor | 0.20 | Neutral-to-Negative | The package's residual-identification process is otherwise very rigorous (12 named/monitored residuals across 7 iterations, several shell-verified) — RT-001 is a genuine miss but a narrow one against an otherwise high bar |
| Evidence Quality | 0.15 | Neutral | Findings in this report are traced to specific lines/mechanisms in both deliverables; the deliverable's own evidence quality (e.g., R-13's shell-verified reproduction) remains strong |
| Actionability | 0.15 | Positive | All four countermeasures are small, non-machinery edits consistent with the subtraction doctrine's own precedent — no new lint rule, ledger, or gate required |
| Traceability | 0.10 | Negative | RT-003: disclosure-depth asymmetry between the two co-produced deliverables on the same named residual (R-9) |

**Overall assessment:** REVISE. One Critical (RT-001) blocks a clean PASS at the stated 0.95 engagement gate under the mandate's own test ("claimed as covered" vs. "disclosed as residual") — the "L-3 No duplicate ID" rule's name is not narrowed anywhere to exclude the frontmatter `id:` field, and no residual entry covers this specific, high-plausibility authoring-error/exploit path. The fix is small and fits the subtraction doctrine (widen an existing mechanism or add one disclosure entry — no new machinery), so this should be a fast remediation cycle, not a rework.

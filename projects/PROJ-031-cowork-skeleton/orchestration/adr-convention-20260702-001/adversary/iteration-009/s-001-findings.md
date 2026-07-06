# Red Team Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, protocol compliance |
| [H-16 Compliance](#h-16-compliance) | Steelman-before-Red-Team check |
| [Threat Actor Profile](#threat-actor-profile) | Who/what is being emulated |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Full evidence per finding |
| [Recommendations](#recommendations) | Prioritized countermeasures |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Execution Context

- **Strategy:** S-001 Red Team Analysis
- **Template:** `.context/templates/adversarial/s-001-red-team.md`
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.10)
- **Criticality:** C4 (gate 0.95)
- **Iteration:** 9 (VERIFIED-CRITICALS protocol — Criticals must survive a 3-lens refutation panel)
- **Date:** 2026-07-06
- **Reviewer:** adv-executor (S-001 Red Team, blind pass — iteration-009/010 sibling files not read)
- **Scope of this pass:** report OVERCLAIMS ONLY — coverage claimed but not actually delivered. The 17 prior Criticals (R-1..R-17, R-A/R-B/R-C) documented in `subtraction-pass-notes.md` are honestly disclosed residuals, not findings, and are excluded from this report.

## H-16 Compliance

S-003 Steelman precedes this execution: the deliverable itself embeds steelman content for every option (Options A-F each lead with a "Strongest case (steelman)" subsection per H-16), and the disposition record (`subtraction-pass-notes.md`) confirms 8 prior tournament iterations including dedicated S-003 tagging (`ST-001`, `ST-002`). H-16 is satisfied; proceeding to Red Team.

## Threat Actor Profile

**Goal:** Get a false sense of assurance accepted as fact — i.e., cause a reader/auditor/future-engineer to believe the L5 lint (and its zero-tooling pre-flight fallback) actually protects a location or audience it does not, so that a real collision or dialect-abuse incident goes undetected until it causes citation damage.
**Capability:** Full read access to both deliverables, the live repository filesystem, and the worktracker SSOT definitions of both placement topologies (project-based and repository-based). No code-execution access beyond documented shell one-liners.
**Motivation:** The deliverable is unusually rigorous about disclosing gaps (R-1..R-17, R-A/R-B/R-C) — an adversary's most valuable target is exactly the claim that *survived* 8 rounds of tournament scrutiny anyway: a coverage claim that reads as true, cites concrete evidence, and is repeated multiple times, but is falsifiable by simply running the one command the document itself specifies against the one filesystem layout the document itself defines.

---

## Summary

Two Critical overclaims were found, both empirically falsifiable using only the deliverables' own specified mechanism against the live repository layout the deliverables themselves describe: (1) the single concrete scan command specified for the L5 lint's collision/grammar/relationship checks (`find projects docs/design -path '*/decisions/*' ...`) structurally cannot see any of the 3 canonical `docs/design/` framework ADRs, because none of their paths contain a `decisions/` segment — directly contradicting the repeated, explicit claim that these 3 files are part of the "18-file scan path" / "scanned roots" the lint covers; (2) the same command is the sole tool offered to repository-based-topology adopters (PROJ-031's own named downstream audience) as their collision-safety fallback, but it is hardcoded to roots (`projects`, `docs/design`) that topology's own Canonical Location Model table says do not contain that topology's ADR home (`{RepositoryRoot}/decisions/`) — so the promised "zero-tooling" fallback delivers zero actual protection to that audience. One Major finding (a tier-and-citation overclaim: a SHOULD-level MEDIUM standard is described as "mandatory" and mis-cited) and one Minor internal-consistency note are also reported. **Recommendation: REVISE** — both Criticals are fixable by narrowing/correcting the claim text (consistent with the subtraction doctrine already used 8 times in this package); no new machinery is required.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|---------------------|
| RT-001-iter009 | Shared `find`-based scan (`-path '*/decisions/*'`) cannot reach `docs/design/*.md` — the 3 canonical framework ADRs are silently excluded from the claimed "18-file scan path" | Boundary | High | Critical | P0 | Missing | Internal Consistency / Evidence Quality |
| RT-002-iter009 | The pre-flight-one-liner "consolation" promised to repository-based-topology adopters is hardcoded to roots (`projects`, `docs/design`) that topology's own location table says do not contain its ADR home | Dependency | High | Critical | P0 | Missing | Completeness / Internal Consistency |
| RT-003-iter009 | `scope:` frontmatter declaration is called "mandatory" and attributed to ADR-M-003, but the actual standard (ADR-M-013) is SHOULD-level MEDIUM tier and ADR-M-003 governs dialect permission, not scope declaration | Ambiguity | Medium | Major | P1 | Missing | Internal Consistency |
| RT-004-iter009 | Consequences "Positive #4" labels "this ADR" as among the "16... grandfathered" files, contradicting D-4's explicit statement that this ADR is "the one disclosed exception to 'in place'" | Ambiguity | Low | Minor | P2 | Partial | Internal Consistency |

**Finding ID format:** `RT-{NNN}-iter009` (execution_id = iteration-009 of the `adr-convention-20260702-001` tournament).

---

## Finding Details

### RT-001-iter009: The lint's specified scan command cannot see the 3 canonical `docs/design/` ADRs it claims to cover [CRITICAL]

**Attack Vector:** An author (or the future lint implementation) relies on the single concrete scan mechanism the deliverables specify — the "pre-flight collision check," which the ADR states verbatim is "exactly what lint L-3 runs in CI":

```
find projects docs/design -path '*/decisions/*' -name 'ADR-*.md' \
  -not -path '*/docs/adrs/*' -not -path '*/docs/archive/*' \
  ...
```
(`projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:407`; identical command at `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:188`)

`find`'s `-path '*/decisions/*'` predicate requires the string `decisions` to appear as a path segment. **Filesystem-verified** (`Glob docs/design/ADR-*.md` and `Glob docs/design/**/ADR-*.md`, both returning identical results, 2026-07-06): the three canonical framework ADRs are `docs/design/ADR-agent-design-001.md`, `docs/design/ADR-output-path-resolution-001.md`, `docs/design/ADR-routing-triggers-001.md` — none sit inside a `decisions/` subdirectory; there is no `docs/design/decisions/` path anywhere in the repository. None of the three paths contain the substring `decisions`, so `-path '*/decisions/*'` evaluates false for all three, and the shown command returns **zero** of them, regardless of the fact that `find` is told to start searching at `docs/design`.

By contrast, every project-scoped dialect ADR genuinely lives under a `decisions/` segment (**filesystem-verified**, `Glob projects/*/decisions/ADR-*.md` → 15 files matching the document's own "15 dialect-reachable" count exactly), so the command *does* correctly enumerate those 15.

This directly contradicts the document's own repeated, explicit claims that the scan covers **both** roots equally:
- D-4 reconciliation: "15 = the dialect files *reachable by the scan path* (`projects/*/decisions/` + `docs/design/`)... This subset **includes** this ADR" (`ADR-PROJ031-004-adr-identifier-convention.md:227`) — the phrase "`docs/design/`" is listed as a scan root with no `decisions/` qualifier, implying `docs/design/*.md` files (not just a hypothetical `docs/design/decisions/*.md`) are reachable.
- L-3 rule row: "**Across the scanned roots** (`projects/*/decisions/` + `docs/design/`, project-based topology)" (`ADR-PROJ031-004-adr-identifier-convention.md:683`; identical wording `adr-standards-rule-draft.md:177`).
- The grandfather regression-test claim: "the **18 files reachable by the scan path** (15 dialect files in `decisions/` dirs + 3 canonical `docs/design/` ADRs...) pass L-1" (`ADR-PROJ031-004-adr-identifier-convention.md:686`; identical `adr-standards-rule-draft.md:181`). Note the document's own phrasing distinguishes "15 dialect files **in `decisions/` dirs**" from "3 canonical `docs/design/` ADRs" (no `decisions/` qualifier for the latter) — the asymmetry is present in the prose but never flagged as breaking the shared scan mechanism.

**Category:** Boundary violation — the claimed dual-root scan boundary (`projects/*/decisions/` + `docs/design/`) does not match the actual boundary the specified command enforces (`*/decisions/*` only), silently dropping one entire root.

**Exploitability:** High — this is not a hypothetical attack; it is the literal, deterministic behavior of the one command specified anywhere in either document, verified against the live filesystem layout the documents themselves describe.

**Severity:** Critical — this means L-1 (grammar), L-3 (duplicate-ID), and (by the same shared-roots claim) L-7 (relationship-target-resolves) would never actually validate the 3 canonical framework ADRs — the highest-stakes tier this whole convention exists to protect ("framework-wide governance" per the ADR's own Criticality statement). A future domain-slug collision or malformed ID minted directly under `docs/design/` (e.g., a second `ADR-agent-design-001` variant, or a dialect-shaped `ADR-EPIC099-001` accidentally placed at `docs/design/`) would pass silently, because the specified scan never visits it. This falsifies the "18-file grandfather regression test" claim (`M-6` in the Migration Plan and the identical clause in the rule draft's L5 spec) — the regression corpus as specified enumerates 15, not 18.

**Existing Defense:** Missing. No alternate scan mechanism for `docs/design/` is specified anywhere in either file; the pre-flight one-liner is the only concrete implementation given, and it is explicitly equated with what "L-3 runs in CI."

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:227,407,683,686`; `adr-standards-rule-draft.md:177,181,188`; filesystem Glob of `docs/design/ADR-*.md` (3 files, none under a `decisions/` segment) and `projects/*/decisions/ADR-*.md` (15 files, exactly matching the claimed "15 dialect-reachable" count).

**Dimension:** Internal Consistency (the claimed scan-root set contradicts the specified command's actual behavior); Evidence Quality (the "18 files reachable" claim is unverified against the one artifact — the command — that would have falsified it).

**Countermeasure:** Either (a) correct the command to `find projects docs/design/ -maxdepth 1 -name 'ADR-*.md' -o -path '*/decisions/*' -name 'ADR-*.md'` (or equivalent two-clause logic covering both the flat `docs/design/` layout and the nested `projects/*/decisions/` layout), and re-verify the "18 files reachable" claim against the corrected command; or (b) if the intent is genuinely to require framework ADRs to live under `docs/design/decisions/` going forward, state that explicitly as a new location-model requirement and disclose that the 3 existing canonical ADRs are themselves out-of-scan until moved (parallel to the STORY015 disclosure). Whichever is chosen, the "18 files reachable by the scan path" claim MUST be corrected to match the actual command, and M-6's grandfather regression test scope must be stated accurately.

**Acceptance Criteria:** Running the (corrected) pre-flight command against the live repository returns exactly 18 lines pre-dedup (or the revised true count), including all 3 `docs/design/` canonical ADRs; the "reachable by the scan path" claim at D-4, the L-3 row, and the M-6 grandfather-test row all cite a command that is demonstrably consistent with that count.

---

### RT-002-iter009: The repository-based-topology "consolation" fallback (pre-flight one-liner) does not reach that topology's own ADR home [CRITICAL]

**Attack Vector:** D-5's topology-scope disclosure states: "Under the **repository-based topology** (`{RepositoryRoot}/decisions/`, no `projects/` prefix)... **L-4 has zero operative effect and L-1/L-3/L-7 do not reach that home** ([R-10]), so that audience receives the **guidance plus the zero-tooling pre-flight one-liner only — not lint coverage** — for collision-safety" (`ADR-PROJ031-004-adr-identifier-convention.md:235`). This explicitly promises that the manual pre-flight command is a **working** fallback for that audience, softening the "no lint coverage" admission.

But the pre-flight command — the only one specified anywhere — is:
```
find projects docs/design -path '*/decisions/*' -name 'ADR-*.md' ...
```
(`ADR-PROJ031-004-adr-identifier-convention.md:407`; `adr-standards-rule-draft.md:188`)

The document's own **Canonical Location Model** table defines the repository-based topology's ADR home as `{RepositoryRoot}/decisions/` — i.e., directly off the repository root, with **no `projects/` directory at all** ("the entire repo is the work context," per the worktracker-topology-branch note, `ADR-PROJ031-004-adr-identifier-convention.md:395`). Running `find projects docs/design ...` inside a repository-based repo searches two roots that either do not exist (`projects`) or do not contain that repo's project-tier ADRs (`docs/design`, which is reserved for framework-scope content and, per RT-001-iter009 above, would not even surface framework ADRs correctly). The command therefore returns **nothing** for that topology's actual `decisions/` corpus — the exact artifact the "consolation" sentence claims it protects.

**Category:** Dependency attack — the fallback tool's correctness silently depends on an assumption (a `projects/` root exists) that the document's own topology definition says is false for this exact audience.

**Exploitability:** High — deterministic and immediately verifiable by inspection; requires no adversarial input, only running the documented command in the documented topology.

**Severity:** Critical — PROJ-031's stated purpose is to produce a distributable Jerry CoWork/plugin skeleton; the repository-based topology is explicitly named as an audience "PROJ-031's own downstream plugin/CoWork adopters may run" (`:235`). For that audience, the convention's collision-safety story is not merely "lint doesn't reach it" (R-10, honestly disclosed) — it is "**nothing** reaches it, including the one tool offered as a substitute," which is a materially worse and undisclosed position. This directly undermines "collision-free ADR identity" and "adoptable MEDIUM-tier convention" for the project's own named target users.

**Existing Defense:** Missing. No topology-aware variant of the pre-flight command (e.g., `find "${REPO_ROOT}/decisions" docs/design -name 'ADR-*.md' | ...` for repository-based repos) is given anywhere.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:235` (the consolation claim), `:395` (repository-based topology has no `projects/` prefix), `:407` (the hardcoded command); `adr-standards-rule-draft.md:81,88,188` (Canonical Location Model row + topology note + identical command).

**Dimension:** Completeness (the promised fallback is incomplete for its target); Internal Consistency (the claim contradicts the document's own topology definition).

**Countermeasure:** Either (a) state the pre-flight one-liner's roots as a variable the adopter must substitute for their topology (e.g., `find "${ADR_ROOT:-projects}" docs/design ...`) with an explicit worked example for the repository-based case, or (b) honestly narrow the D-5 disclosure to say the manual fallback, as currently specified, also does not reach the repository-based topology's `decisions/` home — i.e., that audience currently has **no** collision-safety mechanism at all, tooled or manual, until a topology-aware variant is written.

**Acceptance Criteria:** The document either ships a topology-aware command that a repository-based-topology adopter can run as-is and that demonstrably lists their own `decisions/` corpus, or the D-5 sentence is corrected to state plainly that the pre-flight one-liner does not currently cover that topology either.

---

### RT-003-iter009: `scope:` frontmatter is called "mandatory," attributed to the wrong standard, and contradicts its own MEDIUM tier [MAJOR]

**Attack Vector:** The Rationale section states: "To make declared intent explicit rather than implicit, the `scope:` frontmatter field is **mandatory at authoring time** (added to ADR-M-003 in the companion draft)" (`ADR-PROJ031-004-adr-identifier-convention.md:300`).

Two independent defects:
1. **Wrong citation.** ADR-M-003 in the companion rule draft governs dialect permission ("A tactical, project-local ADR... **MAY** use the dialect `ADR-{PREFIX}-NNN`...") and contains no mention of a `scope:` field at all (`adr-standards-rule-draft.md:48`). The standard that actually declares the `scope:` field requirement is **ADR-M-013**: "Every new ADR **SHOULD** declare `scope` (`framework | project`) in frontmatter at authoring time" (`adr-standards-rule-draft.md:58`).
2. **Tier overclaim.** ADR-M-013 is explicitly SHOULD-level (MEDIUM tier, override-with-justification, per the Tier and Scope section: "All standards are **MEDIUM-tier**," `adr-standards-rule-draft.md:36`). Describing this as "mandatory" implies a compulsory (HARD-tier) obligation the deliverable elsewhere insists does not and cannot exist (c-001: "The standard MUST be MEDIUM-tier... The HARD-rule ceiling is at 25/25 with zero headroom," `ADR-PROJ031-004-adr-identifier-convention.md:123`; D-5: "This convention is RECOMMENDED (SHOULD), overridable with documented justification," `:233`).

This is precisely the class of defect the document's own changelog claims to have systematically eliminated across earlier iterations — CC-001 removed a "PERMITTED" pseudo-tier and reconciled lowercase "never" to SHOULD-NOT; CC-003/SM-203 confirmed "the rule draft carries zero uppercase HARD-tier keywords (MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL)" and added tier-hygiene scoping notes for lint-mechanism "must." The word "mandatory" in prose is functionally the same overclaim as an uppercase MUST, and it slipped through 8 rounds of tournament review because it sits in dense Rationale prose rather than the heavily-scrutinized MEDIUM Standards or L5 lint tables.

**Category:** Ambiguity exploitation — a reader (or a future author deciding whether `scope:` is optional) is told a MEDIUM/SHOULD field is "mandatory," and told to look at the wrong standard ID (ADR-M-003) to find the (non-existent, in that location) rule.

**Exploitability:** Medium — requires a reader to actually cross-check the citation against the rule draft (which this review did), but the misdirection is concrete and would mislead anyone auditing ADR-M-003 specifically for the claimed obligation.

**Severity:** Major — it does not break the lint or collision-safety machinery (unlike RT-001/RT-002), but it is a direct, load-bearing contradiction of the convention's central "honest MEDIUM-tier, never HARD" promise, in the one section (Rationale) that argues the convention's core legitimacy.

**Existing Defense:** Partial — the surrounding sentence correctly frames the *scope-agnostic canonical slug as the safe default under uncertainty* (the substantive point is sound); only the tier-word and citation are wrong.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:300` (the overclaim); `adr-standards-rule-draft.md:48` (ADR-M-003, no scope: field mentioned); `adr-standards-rule-draft.md:58` (ADR-M-013, the actual SHOULD-level standard); `ADR-PROJ031-004-adr-identifier-convention.md:123,233` (c-001/D-5, the MEDIUM-tier commitment this contradicts).

**Dimension:** Internal Consistency.

**Countermeasure:** Change "mandatory" to "SHOULD-declare (ADR-M-013)" and correct the cross-reference from ADR-M-003 to ADR-M-013 at line 300.

**Acceptance Criteria:** The Rationale sentence names ADR-M-013 (not ADR-M-003) and uses tier-consistent language ("SHOULD declare," not "mandatory") matching the standard's own text.

---

### RT-004-iter009: "16 incl. this ADR are grandfathered" contradicts D-4's own "disclosed exception" framing [MINOR]

**Attack Vector:** Consequences → Positive #4 states: "No big-bang migration — the 3 framework ADRs already comply; the **15 pre-existing project/entity dialect ADRs (16 incl. this ADR) are grandfathered**; PROJ-031's set already migrated" (`ADR-PROJ031-004-adr-identifier-convention.md:438`).

D-4 explicitly carves this ADR out of "grandfathered in place": "**This ADR is the one disclosed exception to 'in place':** its current filename is a valid dialect, but it is itself scheduled for Path-2 self-promotion *out of* the dialect (M-9)... **so it does not remain in place**" (`:223`). Calling this ADR "grandfathered" in the Consequences bullet (even parenthetically, "16 incl. this ADR") uses the same word D-4 pointedly withholds from it.

**Category:** Ambiguity exploitation — cosmetic terminology drift between two sections describing the same fact set differently.

**Exploitability:** Low — does not affect any mechanism; a careful reader can reconcile the two sections (both are technically about "current filename count," just using "grandfathered" loosely in one place).

**Severity:** Minor — internal-consistency nit, not purpose-blocking.

**Existing Defense:** Partial — D-4's own careful language is correct; only the Consequences summary bullet re-uses "grandfathered" imprecisely.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:438` (the bullet); `:223` (D-4's contradicting framing).

**Dimension:** Internal Consistency.

**Countermeasure:** Reword the Consequences bullet to "the 15 pre-existing project/entity dialect ADRs are grandfathered in place; this ADR (the 16th dialect-shaped file) is the disclosed exception, scheduled for Path-2 promotion (M-9)."

**Acceptance Criteria:** The two passages use consistent terminology for this ADR's grandfather status.

---

## Recommendations

**P0 (Critical — MUST mitigate before acceptance):**
- **RT-001-iter009:** Correct the scan command (or the location model) so the "18 files reachable by the scan path" claim is actually true of the specified mechanism; re-verify the count. Two `find` clauses (one for `*/decisions/*`, one for `docs/design/*.md` directly) resolve this without adding any new rule.
- **RT-002-iter009:** Ship a topology-parameterized pre-flight command, or narrow the D-5 claim to admit the manual fallback does not currently cover the repository-based topology either.

**P1 (Important — SHOULD mitigate):**
- **RT-003-iter009:** Fix the ADR-M-003→ADR-M-013 citation and downgrade "mandatory" to SHOULD-consistent language.

**P2 (Monitor — MAY mitigate):**
- **RT-004-iter009:** Align the Consequences bullet's terminology with D-4.

None of these four fixes requires new lint rules, ledgers, gates, or matrices — all are corrections to existing claim text or the existing pre-flight command, fully consistent with the subtraction doctrine already applied 8 times in this package.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-002-iter009: the promised fallback for a named audience is absent in practice. |
| Internal Consistency | 0.20 | Negative | RT-001/RT-002/RT-003/RT-004: each is a direct contradiction between a claim and either the specified mechanism or another section of the same document. |
| Methodological Rigor | 0.20 | Negative | The "18-file scan path" and "topology consolation" claims were never verified against the one command the document itself specifies — the exact verification this document otherwise performs relentlessly (e.g., D-4's own filesystem-verified reconciliation). |
| Evidence Quality | 0.15 | Negative | RT-001-iter009 is falsifiable by the document's own cited command against its own cited filesystem facts — a verification the document did not perform for this specific claim. |
| Actionability | 0.15 | Neutral | All four countermeasures are concrete, small, and text-only. |
| Traceability | 0.10 | Neutral | Findings cite exact file+line and are cross-checked against live filesystem state. |

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 2 (RT-001-iter009, RT-002-iter009)
- **Major:** 1 (RT-003-iter009)
- **Minor:** 1 (RT-004-iter009)
- **Protocol Steps Completed:** 5 of 5 (Threat Actor defined; Attack Vectors enumerated across Boundary/Dependency/Ambiguity categories — Rule Circumvention and Degradation categories were explored but yielded no new overclaims beyond the already-disclosed R-1..R-17/R-A-C register; Defense Gaps assessed; Countermeasures specified; Impact synthesized)

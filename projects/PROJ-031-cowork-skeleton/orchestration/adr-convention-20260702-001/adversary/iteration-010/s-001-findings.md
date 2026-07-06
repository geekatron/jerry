# Red Team Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 10)

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, H-16 status |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings with severity/priority |
| [Finding Details](#finding-details) | Full evidence and countermeasures |
| [Verification Log](#verification-log) | What was checked and found clean (not findings) |
| [Recommendations](#recommendations) | Prioritized countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Execution Context

- **Strategy:** S-001 (Red Team Analysis)
- **Template:** `.context/templates/adversarial/s-001-red-team.md` v1.0.0
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.11)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.11)
- **Criticality:** C4 (gate 0.95)
- **Date:** 2026-07-06
- **Reviewer:** adv-executor (S-001, iteration 10, blind protocol — no iteration-009/010 sibling files read)
- **H-16 Compliance:** S-003 Steelman is embedded throughout the deliverable (every Option A–F leads with a blind-advocate steelman per H-16; `ST-001`/`ST-002` tags; see ADR lines 65–68) and the package has been through 9 prior tournament rounds including explicit S-003 application. Treated as satisfied for this execution; no discrete iteration-10 S-003 artifact was required to be re-read under the blind protocol.
- **Threat Actor:** A contributor who wants to ship the convention's flagship self-compliance demonstration (M-9 self-promotion) and its disclosed-residual register without actually verifying the specific factual claims used to justify why gaps remain open — i.e., someone motivated to accept a stated "we checked, nothing exists" justification at face value rather than re-verifying it, because re-verifying costs time and the package has already survived 9 adversarial rounds.

**Scope of this execution (per task mandate):** report ONLY overclaims — abuse paths *claimed* covered/closed/blocked that are not, in fact, covered/closed/blocked. Findings already listed in the disclosed-residual register (R-1…R-17, R-A/R-B/R-C, FM-1…FM-5, PM-009) or in `subtraction-pass-notes.md`'s disposition tables are explicitly OUT of scope as findings.

---

## Summary

After reading both deliverables in full and the complete disposition history (`subtraction-pass-notes.md`, iterations 1–9), this execution found **one Major, evidence-backed overclaim** that survived 9 prior tournament rounds and two independent prior "Glob-verified absent" checks (S-012 iteration-6 FM-010, S-011 iteration-7 VQ-019): the ADR's Migration Plan (M-9) asserts that the atomicity safeguard for its own flagship self-promotion cannot yet be instrumented because **"no `.github/PULL_REQUEST_TEMPLATE.md` exists yet."** A live PR template file — `.github/pull_request_template.md` (lowercase, the casing GitHub itself recognizes) — **does exist in this repository right now** and already ships a generic Checklist section. The "no carrier file exists" justification for deferring the atomicity checklist item is therefore false, and the corrective action the reviewers themselves proposed in iteration-6 ("create the checklist item now — a document-only, zero-machinery fix") was available the whole time and still is. Recommend: REVISE (targeted, single-clause fix; does not require reopening the subtraction doctrine or adding new machinery). All other extensively-checked claims (corpus counts, L-3 dedup regex behavior against the live 18-file corpus, `.claude/rules` symlink behavior, stale PROJ-007 citations, `docs/design/README.md`/`docs/adrs/README.md` absence, blockquote-only PROJ031-002→003 chain, `adr.md`/`SKILL.md` defects) were independently re-verified against the filesystem and found accurate as stated.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-iter010 (= 001-001) | M-9's atomicity-enforcement justification ("no PR template exists") is factually false — a functioning PR template already exists | Ambiguity (verification-pattern blind spot: case-sensitive path search missed the GitHub-recognized lowercase filename) | High | Major | P1 | Partial (repeated "Glob-verified" claims, both wrong) | Evidence Quality / Actionability |

---

## Finding Details

### RT-001-iter010: M-9 Atomicity-Enforcement Claim Rests on a Falsifiable "No Carrier File" Premise [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR `Migration Plan (From Today's Exact Corpus State)`, row **M-9**, `ADR-PROJ031-004-adr-identifier-convention.md:544` |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) — Ambiguity/verification-gap category; corroborated in Step 3 (Defense Gap Assessment) |

**Attack Vector:** The ADR's M-9 row states the atomicity safeguard for the reciprocal M-2/M-9 link repair (the mechanism meant to guarantee the ADR's *own* Path-2 self-promotion — its flagship "worked example of self-compliance" — does not ship a stale, half-repaired link, exactly the failure class this whole convention exists to prevent) is only "an **intended** reviewer-checklist item (FM-010, iter-6: no `.github/PULL_REQUEST_TEMPLATE.md` exists yet — Glob-verified; this is intent, not yet instrumented)." An adversary (or, more realistically, a future maintainer relying on this disclosure) reads this as "there is currently no vehicle to carry this check, so nothing can be done until one is created" — and defers the fix indefinitely on that basis.

**Exploitability:** High — this is not a hypothetical exploit path; it is a verifiable, present-tense factual claim about repository state that a single `Glob`/`ls` check refutes today.

**Severity Justification (Major, not Critical):** This does not itself create an ADR-ID collision or break the 5-rule lint's core collision-safety guarantee, so it does not invalidate the deliverable's central mechanism. It does, however, materially weaken the "honest promotion process" pillar the package repeatedly claims as its differentiator (P-022 Claim-Status discipline, "verified via Glob," "no fabrication") for the *one* self-promotion this ADR performs on itself as a teaching artifact — and the same false justification survived **two independent prior verification passes** (S-012 iteration-6 FM-010: *"Glob-verified absent"*; S-011 iteration-7 VQ-019: *"All three: `Glob` → no matches. All three confirmed absent, as claimed"*), which is itself evidence that the verification pattern used (searching only the exact uppercase filename) is a recurring blind spot, not a one-off typo.

**Existing Defense:** None. The claim was re-affirmed as true across iterations 6, 7, 8, and 9 without anyone testing a case-insensitive or alternate-casing match for the PR-template filename, despite GitHub itself documenting `.github/pull_request_template.md` (lowercase) as an equally valid, recognized location.

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:544` (M-9 row): *"an intended reviewer-checklist item (FM-010, iter-6: no `.github/PULL_REQUEST_TEMPLATE.md` exists yet — Glob-verified; this is intent, not yet instrumented)"*.
- Prior verification claims asserting the same absence: `orchestration/adr-convention-20260702-001/adversary/iteration-006/s-012-findings.md:47,115,118` (FM-010-20260705T-i6, "Glob-verified absent"); `orchestration/adr-convention-20260702-001/adversary/iteration-007/s-011-findings.md:76,110` (CL-033, VQ-019: *"All three confirmed absent, as claimed"*).
- **Direct re-verification performed in this execution (2026-07-06):**
  - `Glob(".github/PULL_REQUEST_TEMPLATE.md")` → **No files found** (the exact casing the ADR and prior reviews searched for — confirms the narrow claim as literally worded).
  - `Glob(".github/*.md")` → **`.github/pull_request_template.md`** (lowercase) — **this file exists**.
  - `Read(".github/pull_request_template.md")` → confirms a live, populated PR template with `## Description`, `## Type of Change`, and a `## Checklist` section (currently 4 generic bullets: tests pass, no credentials committed, docs updated, self-reviewed) — i.e., exactly the kind of file the M-9 atomicity checklist item needs, and it already has a Checklist section ready to receive a new bullet.
- GitHub recognizes `.github/pull_request_template.md` (lowercase, the actual convention used in most open-source repos including this one) as a fully valid, functioning PR template location — it is not a degraded or non-functional alternative to the uppercase form the ADR searched for.

**Dimension:** Evidence Quality (a repeatedly-reverified "Glob-verified" claim is factually wrong) and Actionability (the corrective action iteration-6's own S-012 finding proposed — *"create the PR template checklist item now (a document-only, zero-machinery fix)"* — was available the entire time and still is, at zero cost, without reopening the subtraction doctrine).

**Countermeasure:** Add one checklist bullet to the **existing** `.github/pull_request_template.md` Checklist section, e.g.: *"If this PR performs an ADR promotion (M-9/M-2), the reciprocal ADR↔rule-draft link repair is included in this same PR diff."* Then correct the M-9 row's justification from "no file exists" to either (a) state the checklist item has now been added (closing the residual outright, consistent with the subtraction doctrine's own preference for deletion/closure over open-ended deferral), or (b) if the owner elects not to add it yet, correct the stated reason to something accurate (e.g., "not yet added to the existing template," not "no template exists").

**Acceptance Criteria:** Either (a) `.github/pull_request_template.md` contains the atomicity checklist bullet AND the ADR's M-9 row cites it as instrumented, or (b) the M-9 row's parenthetical is reworded to stop asserting the file's non-existence and instead accurately describes it as an unadded checklist line in an existing template.

---

## Verification Log

The following claims were independently re-checked in this execution (via `Read`/`Glob`/`Grep` against the live filesystem) and found **accurate as stated** — these are NOT findings, listed here only to document the scope of verification performed and avoid re-litigating already-settled ground:

| Claim | Location | Verification | Result |
|---|---|---|---|
| 15 dialect ADRs reachable under `projects/*/decisions/ADR-*.md` | ADR D-4 | `Glob("projects/*/decisions/ADR-*.md")` | 15 files, matches exactly |
| 3 canonical ADRs under `docs/design/ADR-*.md` | ADR D-4 | `Glob("docs/design/ADR-*.md")` | 3 files, matches exactly |
| `ADR-STORY015-001` is the sole out-of-scan entity-embedded dialect ADR | ADR D-4, R-10 | `Glob("**/ADR-STORY015-001*.md")` | 1 file, correct location (`work/.../STORY-015.../`), not under `decisions/` |
| 16-file whole dialect corpus family breakdown (EPIC002×2/PROJ010×6/PROJ022×2/PROJ031×4/STORY015×1/150×1) | ADR D-4 | `Glob` cross-tally against full `**/ADR-*.md` listing | Matches exactly |
| L-3 pre-flight two-clause `find`/regex produces a clean `sort\|uniq -d` (no collisions) against the live 18-file corpus, including the greedy-extraction behavior for `ADR-150-001` and all `PROJ010`/`PROJ022`/`PROJ031`/`EPIC002` files | ADR L1/Enforcement Design; rule draft L5 spec | Manual trace of the documented regex against all 18 real filenames | No collisions; extraction is unambiguous for every file in the actual corpus (R-13's disclosed title-slug-tail bug does not currently trigger against any live file) |
| `.claude/rules -> ../.context/rules` directory symlink auto-exposes new rule files (M-2b) | ADR M-2b | `Read(".claude/rules/quality-enforcement.md")` | Resolves correctly; symlink behavior confirmed |
| `.context/rules/adr-standards.md` and `scripts/lint_adr_convention.py` do not yet exist (Claim-Status: designed-not-built) | ADR Status, Enforcement Design | `Glob` for both paths | Both absent, matches |
| `.github/workflows/ci.yml:2` cites a dangling `ADR-CI-001` path | ADR Context | `Read(".github/workflows/ci.yml", limit=10)` | Confirmed, exact match |
| Stale `ADR-PROJ007-001/002` citations remain live in PROJ-007's own worktracker files | ADR Context, M-10 | `Grep` across `projects/PROJ-007-agent-patterns/` | Confirmed live in `WORKTRACKER.md`, `ORCHESTRATION.yaml`, and 30 other files |
| `docs/design/README.md` and `docs/adrs/README.md` do not exist | ADR L2, M-5 | `Glob` for both | Both absent, matches |
| `docs/knowledge/exemplars/templates/adr.md` carries the bare `# ADR-{NUMBER}` title and dangling `docs/decisions/` path | ADR Context, References #7 | `Grep` on the template file | Confirmed at lines 1 and 182 |
| `ADR-agent-design-001.md`/`ADR-routing-triggers-001.md` carry informal HTML-comment provenance, no YAML frontmatter | ADR Migration Plan (3 framework ADRs row) | `Read` first 10 lines | Confirmed |
| `ADR-PROJ031-002` → `ADR-PROJ031-003` supersession is blockquote-only, no YAML | ADR R-16 | `Read` first 15 lines of `ADR-PROJ031-002...md` | Confirmed |

---

## Recommendations

**P1 (Important — SHOULD mitigate):**
- **RT-001-iter010:** Add the atomicity-safeguard checklist bullet to the existing `.github/pull_request_template.md`, and correct the M-9 row's justification to stop asserting no PR template exists. This is a single-clause, zero-machinery fix fully consistent with the subtraction doctrine already governing this package (it closes a residual by making a true statement, rather than by adding a gate).

No P0 findings were identified in this execution.

---

## Scoring Impact

Map to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10):

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Corpus survey, family counts, and location model coverage were independently re-verified and found complete for the claims tested. |
| Internal Consistency | 0.20 | Neutral | No new contradictions found beyond the single finding above. |
| Methodological Rigor | 0.20 | Negative | RT-001-iter010: the package's own P-022 "Glob-verified" evidentiary standard failed twice on the same claim (iterations 6 and 7) due to an untested case-sensitivity assumption, which is a methodology gap in how "verified absent" claims were checked, not just a one-off content error. |
| Evidence Quality | 0.15 | Negative | RT-001-iter010: a specifically-cited piece of evidence ("no PR template exists") is false. |
| Actionability | 0.15 | Negative | RT-001-iter010: the corrective action proposed by the package's own iteration-6 finding (add the checklist line to an existing template) was actionable then and now, and was not taken; the current text still asserts the premise that made it seem non-actionable. |
| Traceability | 0.10 | Neutral | The finding traces cleanly to a single ADR line and to two prior review artifacts, both cited above. |

**Result:** 1 Major attack vector identified via adversarial emulation, with high-confidence, directly reproducible evidence. Countermeasure is a single-line, zero-machinery fix consistent with the subtraction doctrine already in force.

---

## Execution Statistics

- **Total Findings:** 1
- **Critical:** 0
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5 (Threat Actor defined; Attack Vectors enumerated across all 5 categories, with 4 categories returning no qualifying overclaim after verification and 1 (Ambiguity) returning the finding above; Defense Gaps assessed; Countermeasure developed; Impact synthesized)

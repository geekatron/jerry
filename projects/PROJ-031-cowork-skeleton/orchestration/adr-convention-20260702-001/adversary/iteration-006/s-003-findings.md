# Steelman Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention) + Companion Rule Draft — Post-Subtraction Package, Iteration 6

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable identification |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Step 1: Deep Understanding](#step-1-deep-understanding) | Charitable interpretation of the post-subtraction thesis |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation/structural/evidence gaps only (substance out of scope) |
| [Step 3-4: Steelman Reconstruction + Best Case](#step-3-4-steelman-reconstruction--best-case) | Targeted excerpt reconstructions and best-case conditions |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Full evidence for each finding |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of the findings |
| [Verification Log](#verification-log) | Filesystem/cross-file checks performed |

---

## Steelman Context

- **Deliverable 1:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (751 lines)
- **Deliverable 2:** `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (232 lines)
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft
- **Criticality Level:** C4 (framework-wide governance convention)
- **Strategy:** S-003 (Steelman Technique) — iteration 6, post-subtraction-pass package
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind reviewer) | **Date:** 2026-07-05 | **Original Author:** ps-architect (owner)
- **Scope note:** Per invoking instructions, this review evaluates the package **as it now stands** after the user-authorized subtraction pass (FEEDBACK-LOG FU.1). Findings do not demand re-adding deleted enforcement machinery (18-rule lint, waiver ledger, two-tier gate) — that deletion is treated as a valid, honestly-disclosed MEDIUM-tier design posture, consistent with `quality-enforcement.md` Tier Vocabulary (SHOULD/RECOMMENDED, override-with-justification).

---

## Summary

**Steelman Assessment:** A mature, extensively self-corrected C4 governance ADR (6 iterations of adversarial remediation) whose post-subtraction form deliberately trades a monolithic 18-rule lint for a 5-rule fail-closed core plus honest, undeleted residual disclosure. The core thesis — ADR identity should encode *subject* (immutable, queried-by) rather than *origin* (mutable-by-design, since ADRs are the one Jerry artifact class built to migrate scope) — is argued from first principles, defended against its own strongest counter-case (Scheme C), sensitivity-analyzed against the one assumption that could flip it, and grounded in git-verified evidence (a paid, receipted promotion tax; a live intra-family collision; a still-dangling citation). The subtraction pass is itself evidenced, not merely asserted: independent `grep` verification below confirms zero live in-body references to any of the 13 deleted lint rules, and the FEEDBACK-LOG ratification quote matches verbatim.
**Improvement Count:** 0 Critical, 1 Major, 2 Minor.
**Original Strength:** Already very high. The remaining gaps are narrow presentation/traceability items, not substantive flaws — consistent with a document already through 5 prior remediation cycles.
**Recommendation:** Incorporate the 3 improvements below (all low-cost, single-clause or single-cell edits); the package is otherwise ready for downstream critique strategies at its current strength.

---

## Step 1: Deep Understanding

**Core thesis:** An identifier should be invariant across an artifact's lifecycle. Every other Jerry entity (PROJ/EPIC/STORY/`DEC-NNN`) is correctly scope-prefixed because its scope never changes. The ADR is the *one* Jerry artifact whose governing scope is mutable by design (project → framework promotion is the accrual thesis in action), so encoding scope into its identity is the actual defect — not a virtue to imitate. Subject (domain-slug) is materially more stable than scope and is what readers query by; origin is a birth fact preserved in frontmatter, not identity. The user's crux ("is *project* really the right scope key?") is answered directly: no, because the differentiator is mutability, not literal scope-prefixing (`DEC-NNN` is already written bare at Enabler/Story level, proving the ontology's real invariant is fixed-scope, not scope-in-the-string).

**Key claims and their strongest support (charitable read):**
1. Promotion already happened 3 times and cost a real, receipted tax (commit `41539073`, ~150 references) — **verified**: `docs/design/` contains exactly the 3 claimed files (`ADR-agent-design-001.md`, `ADR-output-path-resolution-001.md`, `ADR-routing-triggers-001.md`), no more, no fewer.
2. A same-family collision (`ADR-EPIC002-001`) genuinely occurred — **verified**: both `ADR-EPIC002-001-strategy-selection.md` and `ADR-EPIC002-002-enforcement-architecture.md` exist side-by-side in `projects/PROJ-001-oss-release/decisions/`, consistent with the ADR's corrected (CV-002) account that the collision was resolved by renaming the *unrelated* output-path decision, not by touching either surviving EPIC002 file.
3. A dangling full-path citation exists today — **verified**: `.github/workflows/ci.yml:2` cites `projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`, and `projects/PROJ-001-plugin-cleanup/` does not exist in the current `projects/README.md` registry (PROJ-001 is now `oss-release`) — the citation is genuinely dangling exactly as claimed.
4. The producing agent is genuinely non-compliant today — **verified**: `skills/problem-solving/agents/ps-architect.md:218` reads `# ADR-{NUMBER}: {Title}`, matching neither the canonical nor dialect grammar, exactly as M-12 describes.
5. The lint is genuinely unbuilt — **verified**: `Glob` for `scripts/lint_adr_convention.py` returns no results, matching every "DESIGNED, NOT BUILT" Claim-Status assertion in both files.
6. The ratification quote is verbatim — **verified**: `FEEDBACK-LOG.md` FU.0 contains "I ratify the promotion-is-the-point apporach and lock Scheme B." (typo preserved) exactly as both deliverables cite it.

Every load-bearing factual claim independently spot-checked in this review resolved **true**. This is a strong foundation: the argument is not resting on unverifiable or fabricated evidence.

**Decision Point:** Fundamentally coherent — proceeds to Step 2.

---

## Step 2: Weakness Classification

Per H-16/S-003 discipline, only **presentation**, **structural**, and **evidence** weaknesses are in scope; substantive weaknesses (disagreement with Scheme B itself) are explicitly out of scope for S-003 and left for S-002/S-004/S-001. No substantive weaknesses were identified in this pass in any case — the decision was independently ratified by the human owner (P-020) and this review does not revisit that ratification.

| Weakness | Type | Magnitude | Strongest likely intent |
|---|---|---|---|
| Migration Plan row M-8 ("`/adversary` C4 review of the ratified standard") still reads `TBD-Task`, but this very iteration-6 blind tournament — and the 5 prior iterations recorded in the Changelog — already constitute substantial execution of that review | Structural (status-tracking gap between a status cell and the document's own asserted history) | Major | The table was drafted incrementally alongside the ratification edit and simply wasn't re-synced against the Changelog/FEEDBACK-LOG in the same pass; the intent is clearly to track M-8 as work happens, not to claim it hasn't started |
| The 5-rule lint tables in both files enumerate `L-1, L-2, L-3, L-4, L-7` with no explanation, at the table itself, of why `L-5`/`L-6` are absent from the sequence | Presentation (numbering artifact from deletion, invisible without cross-referencing the out-of-scope orchestration notes file) | Minor | The gap is a residue of a good-faith subtraction (13 rules deleted, including former L-5/L-6 provenance WARNs) — not an error, just under-annotated at the point a fresh reader would notice it |
| Rule-draft wrapper line 1: "**REVIEW DRAFT of a ratified convention.**" momentarily reads as self-contradictory (draft vs. ratified) before the next two sentences resolve it (the *decision* is ratified; the *file* is still staged pending the M-2 move) | Presentation (word choice creates a beat of ambiguity before resolution) | Minor | The intent is precise and correct — decision-ratified/file-staged is a real and useful distinction — it just needs a less loaded opening label |

**Decision Point:** All three weaknesses are non-substantive (presentation/structural); proceed to Step 3.

---

## Step 3-4: Steelman Reconstruction + Best Case

Given the deliverable's size (751 + 232 lines) and its already-mature state (5 prior remediation iterations), a full rewrite would not add value; per the template's own precedent (Section 7 Example 1, "key sections shown"), targeted excerpt reconstructions are provided for each finding below.

### [SM-001] Reconstruction — Migration Plan M-8 status sync

**Original** (`decisions/ADR-PROJ031-004-adr-identifier-convention.md:510`):
```
| M-8 | `/adversary` C4 review of the ratified standard | adversary | TBD-Task | Yes |
```

**Strengthened:**
```
| M-8 | `/adversary` C4 review of the ratified standard | adversary | IN-PROGRESS — 6 blind-tournament iterations executed against this package to date (iterations 1-5 pre-ratification, Changelog 1.1-1.6; iteration 6+ post-ratification/post-subtraction, this iteration); tracked in FEEDBACK-LOG.md FU.1 as workflow-launched 2026-07-05; TBD-Task for a formal closure ticket | Yes |
```
**Rationale:** This closes the one place where the deliverable's own internal record (6 Changelog entries) and an external cross-file record (`FEEDBACK-LOG.md:49`, "IN-PROGRESS — subtraction + blind tournament iterations 006–008 workflow launched") are more informative than the Migration Plan cell describing the same work item. No new claim is introduced — only a status cell brought into agreement with facts already asserted elsewhere in the same package.

### [SM-002] Reconstruction — L-5/L-6 numbering gap

**Original** (`decisions/ADR-PROJ031-004-adr-identifier-convention.md:646-652`, and identically `design/adr-standards-rule-draft.md:169-175`):
```
| Rule | Checks (git-added/modified files; pre-adoption grandfathered) |
|---|---|
| **L-1 Grammar** | ... |
| **L-2 No new bare** | ... |
| **L-3 No duplicate ID** | ... |
| **L-4 ID↔location** | ... |
| **L-7 Relationship target resolves** | ... |
```

**Strengthened:**
```
| Rule | Checks (git-added/modified files; pre-adoption grandfathered) |
|---|---|
| **L-1 Grammar** | ... |
| **L-2 No new bare** | ... |
| **L-3 No duplicate ID** | ... |
| **L-4 ID↔location** | ... |
| **L-7 Relationship target resolves** | ... |

*(Numbering is non-sequential by design: L-5/L-6 were provenance/framework-home WARN rules cut in the subtraction pass along with 11 other candidates — see the Descoped note above. Retained numbers are kept stable rather than renumbered, so a future amendment adding a targeted rule does not have to renumber the surviving five.)*
```
**Rationale:** A single parenthetical at the point of first reader confusion prevents an unnecessary "is this a typo / did I miss L-5?" question, without re-litigating the subtraction decision itself.

### [SM-003] Reconstruction — Rule-draft wrapper framing

**Original** (`design/adr-standards-rule-draft.md:1`):
```
# DRAFT — Proposed `.context/rules/adr-standards.md`

> **REVIEW DRAFT of a ratified convention.** Proposed content of `.context/rules/adr-standards.md`, ...
```

**Strengthened:**
```
# STAGED — Proposed `.context/rules/adr-standards.md`

> **Ratified convention, staged pending file move.** The convention itself (Scheme B) was ratified 2026-07-05 (FEEDBACK-LOG FU.0); this file's *content* is final but its *location* is staged here pending the M-2 move into `.context/rules/adr-standards.md` ...
```
**Rationale:** Removes the momentary read of "draft" as "not yet decided" by separating the two independent axes (decision status: ratified; file status: staged-not-moved) into two clauses instead of one compressed label.

### Best Case Scenario (Step 4)

The Steelman Reconstruction is most compelling under conditions the deliverable already argues hold: (1) promotion of project decisions into the framework recurs rather than being a one-off accident — independently true whether or not the specific n=3 rate generalizes, because arguments 1-2 of the Rationale (ontology category-error; promotion-independent discoverability) do not depend on promotion frequency at all; (2) the HARD-rule budget genuinely has zero headroom (verified against `quality-enforcement.md`'s own "25/25" ceiling statement), so a MEDIUM-tier, lint-optional posture is the only available enforcement shape; (3) the corpus keeps growing, which is exactly the regime where a subject-encoded, `git mv`-promotable identity compounds in value and an origin-encoded one compounds in promotion-tax liability. Confidence in the Steelman holding: **high** — nearly every load-bearing citation independently checked out in this review (Step 1), and the three residual gaps found are corrective status/wording fixes, not evidentiary failures.

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|--------------|----------|----------|--------------|-----------|
| SM-001-iter006 | Migration Plan M-8 row not synced to the document's own Changelog history or to `FEEDBACK-LOG.md` FU.1 | Major | `TBD-Task` (implies unstarted) | `IN-PROGRESS` with cross-reference to Changelog 1.1-1.7 and FEEDBACK-LOG FU.1 | Internal Consistency / Traceability |
| SM-002-iter006 | L-5/L-6 numbering gap in the 5-rule lint table is unexplained at the table itself | Minor | Table jumps L-4 → L-7 with no note | One-sentence parenthetical explaining the gap is by design (subtraction residue) | Completeness / Traceability |
| SM-003-iter006 | "REVIEW DRAFT of a ratified convention" wrapper phrase momentarily conflates file-staging status with decision-ratification status | Minor | Single compressed label | Two-clause framing separating decision status from file-location status | Methodological Rigor (clarity) |

**Severity note:** No Critical findings. All three are corrective, low-cost (single-cell or single-clause) edits that do not touch the decision, the 5-rule lint scope, or any of the honestly-disclosed residuals (R-A/R-B/R-C/R-1/R-6/R-7/PM-009) — those residuals are treated as accepted, valid MEDIUM-tier disclosure per this review's scope instruction, not as findings.

---

## Improvement Details

### SM-001-iter006 (Major)

- **Affected Dimension:** Internal Consistency (primary), Traceability (secondary)
- **Location:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:510`
- **Original Content:** `| M-8 | ... | adversary | TBD-Task | Yes |`
- **Strengthened Content:** See [SM-001] reconstruction above.
- **Rationale:** A reader arriving at the Migration Plan after reading the Changelog (which documents 6 adversarial iterations, 5 already completed) would reasonably ask why the table still shows the review as not-yet-started. Cross-file evidence (`FEEDBACK-LOG.md:49`) already tracks this exact work item as `IN-PROGRESS`, so the fix is a factual sync, not new work.
- **Best Case Conditions:** Fully resolved once the owner updates the cell in the next revision pass (trivial, no re-review of substance required).

### SM-002-iter006 (Minor)

- **Affected Dimension:** Completeness, Traceability
- **Location:** `decisions/ADR-PROJ031-004-adr-identifier-convention.md:646-652`; identically `design/adr-standards-rule-draft.md:169-175`
- **Original Content:** Lint table enumerates L-1, L-2, L-3, L-4, L-7 with no comment on the missing L-5/L-6.
- **Strengthened Content:** See [SM-002] reconstruction above.
- **Rationale:** The gap is fully explainable from the (out-of-mandate) `subtraction-pass-notes.md` deletion list, but nothing in either deliverable itself tells a first-time reader this. A one-sentence note removes the ambiguity without importing any of the deleted machinery.

### SM-003-iter006 (Minor)

- **Affected Dimension:** Methodological Rigor (presentation clarity)
- **Location:** `design/adr-standards-rule-draft.md:1,3`
- **Original Content:** "**REVIEW DRAFT of a ratified convention.**"
- **Strengthened Content:** See [SM-003] reconstruction above.
- **Rationale:** The underlying distinction (decision ratified vs. file not yet moved) is correct and valuable; the wording just asks the reader to hold a brief contradiction before the next sentence resolves it.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral→Positive | SM-002 closes a small residual gap; core content already comprehensive after 5 prior iterations |
| Internal Consistency | 0.20 | Positive | SM-001 resolves the one identified cross-file status contradiction (ADR Migration Plan vs. FEEDBACK-LOG.md) |
| Methodological Rigor | 0.20 | Positive | SM-003 removes a momentary presentation ambiguity; charitable read confirms the 6-step self-correction discipline (verified claims, honest residual framing) is already intact |
| Evidence Quality | 0.15 | Neutral | Already strong — 6/6 spot-checked load-bearing citations verified true in this review (Step 1); no new evidence gaps found |
| Actionability | 0.15 | Positive | All 3 findings are single-cell/single-clause edits, immediately incorporable without re-opening any ratified decision |
| Traceability | 0.10 | Positive | SM-001 and SM-002 both directly improve cross-reference clarity between the deliverable and its own history/companion files |

---

## Verification Log

Filesystem and cross-file checks performed independently during this Steelman execution (all resolved consistent with the deliverable's claims unless otherwise noted):

| Claim checked | Method | Result |
|---|---|---|
| `scripts/lint_adr_convention.py` does not exist | `Glob` | Confirmed absent |
| Exactly 3 canonical ADRs in `docs/design/` | `Glob docs/design/ADR-*.md` | Confirmed: `agent-design-001`, `output-path-resolution-001`, `routing-triggers-001` |
| `ADR-EPIC002-001` and `ADR-EPIC002-002` both exist in `projects/PROJ-001-oss-release/decisions/` | `Glob` | Confirmed both present |
| `.github/workflows/ci.yml:2` cites a dangling project path | `Read` | Confirmed: cites `projects/PROJ-001-plugin-cleanup/...`, which does not appear in `projects/README.md` (PROJ-001 = `oss-release`) |
| `ps-architect.md:218` still emits non-canonical `# ADR-{NUMBER}` title | `Read` | Confirmed |
| FEEDBACK-LOG FU.0 ratification quote matches verbatim | `Read` | Confirmed exact match, typo included |
| No live in-body reference to any of the 13 deleted lint rules (L-5, L-6, L-6b, L-6c, L-8, L-9, L-10, L-11, L-12, L-13, L-14, L-1b, L-4b) in either deliverable | `Grep` (both files) | Confirmed: all matches found are honest past-tense disclosure/changelog prose ("descoped", "former lint"), none present the rule as a live active mechanism |
| Rule draft carries no `PERMITTED` pseudo-tier, `non-bypassable`, `non-waivable`, or `CODEOWNERS` language as a live claim | `Grep` (case-insensitive) | Confirmed: only lowercase "permitted" (describing dialect status) and one summary line explicitly disclaiming "no waiver ledger, no CODEOWNERS gate, no 'non-bypassable' rule" |
| Sibling ADRs `ADR-PROJ031-001/002/003` exist as claimed in Related Decisions | `Glob` | Confirmed all three present |

**Constitutional compliance:** P-003 (no subagents spawned); P-020 (no edits made to either deliverable — read-only review, findings returned to orchestrator); P-022 (all claims above cite file path/line or Glob/Grep tool result; the Best Case Scenario confidence assessment is explicitly labeled as this reviewer's inference).

---

*Strategy: S-003 (Steelman Technique) | Template: `.context/templates/adversarial/s-003-steelman.md` | Iteration: 006 | Executed: 2026-07-05*

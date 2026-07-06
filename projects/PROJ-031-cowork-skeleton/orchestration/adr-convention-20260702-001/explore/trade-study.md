---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Trade Study: ADR Identifier Scheme for the Jerry Framework Monorepo

> **Project:** PROJ-031-cowork-skeleton
> **Entry:** adr-convention-20260702-001 (explore phase)
> **Date:** 2026-07-02
> **Method:** NPR 7123.1D Process 17 (Decision Analysis) — weighted-sum trade study with sensitivity analysis
> **Criticality:** C4 (framework-wide governance convention; AE-002/AE-003 auto-escalation)
> **Status:** Draft — advisory (decision reserved for human ratification)
> **Agent:** nse-explorer (divergent cognitive mode)

## Navigation

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language answer to "which ID scheme and why does it matter" |
| [Decision Context](#decision-context) | Problem statement, driving forces, constraints, the crux |
| [Schemes Under Evaluation](#schemes-under-evaluation) | The six candidate schemes (A–F) plus discovered variants |
| [Evaluation Criteria and Weights](#evaluation-criteria-and-weights) | Nine weighted criteria with justification |
| [L1: Scoring Matrix](#l1-scoring-matrix) | Per-criterion scores with evidence |
| [L1: Weighted-Sum Results](#l1-weighted-sum-results) | Baseline totals and ranking |
| [L2: Sensitivity Analysis](#l2-sensitivity-analysis) | Promotion-frequency flip; discoverability-vs-provenance flip |
| [L2: The Crux — Answered](#l2-the-crux--answered) | Origin-in-identity vs subject-in-identity, head-on |
| [L2: Recommendation Framework](#l2-recommendation-framework) | Conditional recommendation with confidence |
| [Open Questions](#open-questions) | TBD/TBR items for human ratification |
| [Evidence Ledger and P-022 Disclosures](#evidence-ledger-and-p-022-disclosures) | File-path citations; inference labels |
| [References](#references) | NASA process + internal/external sources |

---

## L0: Executive Summary

Jerry needs one convention for naming Architecture Decision Records (ADRs) across a monorepo where many agents author decisions in parallel and where good decisions are meant to "graduate" from individual projects up into the framework. The choice matters because ADRs are the **one** artifact class in Jerry that changes scope during its life — and today, changing scope means changing the ADR's name, which silently breaks every citation that pointed at the old name (this has already happened three times).

**The answer is assumption-dependent, and the assumption is the whole game.** If promoting a project decision into the framework is a *rare* event, the pragmatic winner is **Scheme C (two-namespace)** — it matches what the repo already does, so migration is near-zero. If promotion is a *normal* event — which is exactly what Jerry's "knowledge accrual" thesis claims and what the repo's own history shows (100% of framework ADRs got there by promotion) — the winner **flips to Scheme B (subject-encoded identity everywhere)**, because B makes promotion a zero-cost file move with no broken citations. This study recommends **B (implemented as "domain-slug identity from birth, in a two-location layout")**, at **moderate confidence (0.70)**, and asks the team to ratify one belief before finalizing: *is promotion the point, or the exception?*

---

## Decision Context

**Problem Statement.** No documented standard governs ADR identifiers, numbering, location, promotion, or superseding anywhere in the repo (confirmed across 11 surfaces — research file lines 33–49). Multiple incompatible ID families coexist, and the bare `ADR-NNN` family demonstrably collides across scopes. A framework-wide (C4) convention must be selected.

**Driving Forces (each traces to verified evidence):**

| Force | Evidence |
|-------|----------|
| Distributed, uncoordinated authoring (merge conflicts are real) | Bare `ADR-001/002/003` collide across `docs/adrs/` + PROJ-014 + (formerly) PROJ-031 — research lines 72–79; verified via `find` (`docs/adrs/ADR-001-*`, `.../PROJ-014-.../phase-5/ADR-001-*`). |
| Knowledge accrual from projects → framework is Jerry's core thesis | CLAUDE.md Identity: "Accrues knowledge, wisdom, experience." All 3 `docs/design/` ADRs carry project provenance (`PS-ID: PROJ-007`, `Parent: EPIC-002`) yet use domain-slug IDs — verified in file headers. |
| Citation continuity already broke on promotion | `BUG-006-adr-naming-evaluation.md` (dated 2026-04-13) still cites `ADR-PROJ007-001-agent-design.md` / `ADR-PROJ007-002-routing-triggers.md` (lines 49–51) — the live files are now `ADR-agent-design-001` / `ADR-routing-triggers-001`. A stale reference in the wild. |
| Scope-prefixed identity is the house ontology | Every worktracker entity is scope-prefixed: `PROJ-`, `EPIC-`, `FEAT-`, `STORY-`, `TASK-`, `BUG-`, `DISC-`, `IMP-`, `DEC-` (worktracker-directory-structure.md lines 56–88); `DEC-NNN` is *parent-scoped* (`EPIC-001--DEC-001-slug`). |

**Constraints:**
- The standard **MUST be MEDIUM-tier** (SHOULD/RECOMMENDED). HARD rules are at **25/25, zero headroom** (quality-enforcement.md Tier Vocabulary / HARD Rule Ceiling). A new HARD rule would require a C4 ADR + a ceiling exception. Enforcement is therefore L5 CI lint + L4 advisory, not a HARD invariant.
- No big-bang renumber of frozen legacy sets (tombstone precedent — quality-enforcement.md "Retired Rule IDs").
- Must not conflate ADRs with the distinct `DEC-NNN` worktracker Decision-File entity.

**The Crux (user's challenge).** Project-scoping encodes **origin into identity**. Jerry's ontology is scope-prefixed everywhere, which favours origin-encoded schemes (A/C). BUT ADRs are the one artifact class that **migrates scope**: all three framework ADRs were born in projects and changed identity on promotion. If Jerry's accrual thesis is real and promotion is the *point* (not the exception), then **subject-encoded identity (B)** — which survives promotion unchanged — may dominate. This study must sensitivity-analyze the winner against the promotion-frequency assumption **explicitly** and state the conditions under which the winner loses.

---

## Schemes Under Evaluation

| ID | Scheme | Pattern | Example | Identity encodes | Live corpus |
|----|--------|---------|---------|------------------|-------------|
| **A** | Project-scoped sequence | `ADR-{PROJECT-ID}-NNN-slug` | `ADR-PROJ031-001-skeleton-distribution-strategy` | **Origin** (birth project) | Dominant: PROJ010×6, PROJ022×2, PROJ031×3, +entity variants (verified `find`) |
| **B** | Domain-slug everywhere | `ADR-{domain-slug}-NNN-...` | `ADR-plugin-distribution-001` | **Subject** (origin in frontmatter only) | The 3 `docs/design/` framework ADRs already comply |
| **C** | Two-namespace | A in `projects/*/decisions/`; B in `docs/design/` after promotion; renumber-on-promotion + tombstone back-links | born `ADR-PROJ031-001` → promoted `ADR-plugin-distribution-001` | **Origin at birth, Subject after promotion** | This is the de-facto current split (ps-researcher recommendation) |
| **D** | Date-based | `ADR-YYYYMMDD-slug` | `ADR-20260702-skeleton-distribution` | **Time** (no scope) | None in repo (log4brains external pattern) |
| **E** | Global monotonic | `ADR-NNNN` repo-wide | `ADR-0042` | **Nothing** (opaque sequence) | Legacy bare `ADR-NNN` is a degenerate instance; collides (MADR external) |
| **F** | Scope+slug, no number | `ADR-{SCOPE}-{slug}` | `ADR-framework-plugin-distribution` | **Origin + Subject, no sequence** | None (pure-name-within-scope) |

**Discovered variants (folded into the six, not scored separately):**
- `ADR-{GH-issue}-NNN` (`ADR-150-001`, PROJ-030) — a **sub-variant of A** where the scope key is a GitHub issue number rather than a project ID (verified `projects/PROJ-030-bugs/decisions/ADR-150-001-*`).
- `ADR-OSS-NNN` (`ADR-OSS-001..007`, PROJ-001 orchestration artifacts) — a **campaign/series-slug variant sitting between A and B** (verified `find`); transient, per-agent, non-canonical.
- `ADR-{ENTITY-ID}-NNN` (`ADR-STORY015-001`, `ADR-EPIC002-001`) — **A keyed on a finer entity** (story/epic) instead of the project; same design family as A.
- `adr-{slug}[-vN]` lowercase (`adr-cli-integration`, `adr-cli-integration-v2`) — informal **F-like** drafts (verified `find`).

These confirm the design space is fully spanned by A–F; no seventh independent identity model was found.

---

## Evaluation Criteria and Weights

Weights sum to 100. Justification ties each weight to a driving force or constraint above. Scores are 1–5 (5 = best); the weighted score is `Σ(score × weight)/100` on a 1–5 scale.

| ID | Criterion | Weight | Justification (why this weight) |
|----|-----------|:---:|--------------------------------|
| C1 | **Collision-safety w/o central coordination** (merge-conflict resistance) | **18** | Highest single weight: this is the failure mode that *actually bit the repo* (verified bare-`ADR-NNN` cross-scope collisions) and the exact reason log4brains abandoned monotonic numbering. In a many-agent monorepo with branch-parallel authoring, a scheme that needs a shared counter/registry is a standing liability. |
| C2 | **Promotion-stability** (identity + citation continuity across scope migration) | **16** | The crux criterion. Jerry's thesis makes promotion first-class; a broken citation on every promotion is a recurring tax. Weighted just below C1 at baseline — but this weight is the load-bearing assumption the sensitivity analysis stresses. |
| C4 | **Subject discoverability** (find the ADR governing topic X without knowing its birth project) | **14** | BUG-006's most severe findings (F-001/F-003, severity 3) are discoverability/recognition failures of opaque IDs. Cross-project readers and future agents query by *topic*, not by birth project. |
| C3 | **Provenance clarity** (origin traceability at a glance) | **12** | Jerry values traceability (P-040). Knowing where a decision came from matters — but it can live in frontmatter, so it is weighted below discoverability. |
| C5 | **Consistency with Jerry's scope-prefixed ontology** | **12** | Framework coherence: every other entity ID is scope-prefixed. Deviation raises cognitive load and lint-model complexity. Weighted equal to provenance — real, but not a safety invariant. |
| C7 | **Migration cost from today's state** | **8** | One-time cost; pragmatic but not a property of the long-lived convention. Penalizes big-bang renumbers; rewards adopt-forward. |
| C8 | **Deterministic lint-ability (L5 CI)** | **8** | The standard is MEDIUM-tier, enforced by L5 CI (constraint). A scheme a regex can validate locally beats one needing global registry state. |
| C6 | **Sortability** (related ADRs cluster in listings) | **6** | Convenience axis (BUG-006 F-004, severity 2). Real but low-stakes; partially subsumed by discoverability. |
| C9 | **Human ergonomics** (readability, brevity, typeability) | **6** | Matters for daily use; lowest weight because all schemes are "good enough" to type and none is disqualifying. |

**Weight-setting note (P-022, inference):** These weights are the author's reasoned allocation for a C4 monorepo governance decision; they are an *input assumption*, not a fact. The sensitivity analysis exists precisely because the ranking is a function of these weights — most sharply of C2.

---

## L1: Scoring Matrix

Each cell: **score (1–5)** with one-line evidence. "Verified" = filesystem/citation-confirmed; "Inference" = reasoned judgment.

### C1 — Collision-safety without central coordination (w=18)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 4 | Globally-unique project ID namespaces the sequence → zero cross-scope collision by construction (verified: all scope-prefixed families collision-free, research 81). Residual: intra-project `NNN` race on parallel branches (low; single-project concurrency). |
| B | 3 | Slug namespaces the sequence, but **slug-uniqueness is uncentralized** — two authors can independently mint `ADR-plugin-distribution-001` for different decisions; plus `NNN` race within a hot domain. Weakness is documented (research 132: "requires slug-uniqueness discipline"). *A defensible analyst could score 4; see sensitivity note.* |
| C | 4 | New ADRs are **born project-scoped** (inherits A at the high-concurrency creation moment); framework namespace inherits B's 3. Effective collision-safety at authoring ≈ A. |
| D | 5 | `YYYYMMDD-slug` was adopted by log4brains *specifically* to be merge-conflict-free (research 100). Same-day authors differ by slug; residual near-zero. Gold standard for this criterion. |
| E | 1 | **The documented failure mode**: monotonic repo-wide numbers "caused conflicts during git merge" (log4brains, research 100); Jerry's bare `ADR-NNN` collisions are the live proof (verified). Needs a central registry. |
| F | 4 | No shared counter at all → no numbering merge-conflict. Collision only on same-scope + same-slug (rare, lint-catchable). Strong on contention, mild slug-discipline residual. |

### C2 — Promotion-stability: identity & citation continuity across scope migration (w=16) — THE CRUX

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 2 | Origin is the identity → promotion forces either (i) renumber (`ADR-PROJ007-001` → `ADR-agent-design-001`, breaking citations — **verified live break**: BUG-006 49–51 still cites the old ID) or (ii) keep an origin-misencoding ID in `docs/design/`. Both bad. |
| B | 5 | Subject-encoded → promotion is a **pure file move**; the ID never changes; every citation survives. B's signature strength and the direct answer to the crux (research 132). |
| C | 3 | Explicitly *renumbers on promotion* with tombstone back-links (research 158–164). The tombstone keeps the old ID *resolvable*, but the canonical ID still changes → external citations still need updating. A **managed** break, not a zero break. |
| D | 5 | Date ID is scope-agnostic; birth date doesn't change on move → zero ID churn. Promotion = file move. |
| E | 5 | Global number is scope-agnostic (`ADR-0042` wherever it lives) → zero ID churn on promotion. (E's weakness is elsewhere.) |
| F | 2 | Scope is *in* the identity → promotion changes scope → changes ID (same churn as A). The slug portion survives (partial continuity), so marginally better story than A but same structural break. |

### C3 — Provenance clarity (w=12)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 5 | Origin **is** the identity — `ADR-PROJ031-001` states its birth project at a glance. Maximal provenance. |
| B | 3 | Origin recorded in frontmatter only (research 133) — traceable but requires opening the file. |
| C | 4 | Project-scoped at birth (5) + frontmatter provenance + explicit `PROMOTED_FROM/TO` back-links after promotion (research 163) preserve the origin chain. |
| D | 2 | Encodes *when*, not *where*. No scope/origin in ID; frontmatter only. |
| E | 2 | Opaque number carries no origin; frontmatter only. |
| F | 4 | Scope prefix encodes origin at birth (like A), but coarser (domain/scope, not necessarily the specific project). |

### C4 — Subject discoverability (w=14)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 2 | Opaque prefix — `ADR-PROJ031-001` says nothing about subject; to find "the ADR governing plugin distribution" you must already know it lives in PROJ-031 (BUG-006 F-001/F-003, severity 3; verified opaque citations in rules: `ADR-STORY015-001` ×12, `ADR-EPIC002-001` ×4). |
| B | 5 | Subject **is** the ID — `ADR-plugin-distribution-001` is self-documenting; `grep ADR-plugin-*` clusters the topic. Best discoverability (BUG-006 Alt-3 5/5). |
| C | 4 | Mixed: project-local ADRs opaque (2) but the promoted, cross-cutting, most-consulted framework ADRs use domain-slug (5). Discoverability lands where it matters most. |
| D | 2 | ID is a date; slug lives only in filename tail; poor topic recognition. |
| E | 1 | Fully opaque (`ADR-0042`). Worst case (BUG-006 baseline complaint). |
| F | 5 | Slug is in the ID → subject fully discoverable (`grep ADR-*-plugin-distribution`), no opaque number. |

### C5 — Consistency with Jerry's scope-prefixed ontology (w=12)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 5 | `ADR-{PROJECT-ID}-NNN` mirrors the house pattern exactly (scope prefix + zero-padded sequence), matching `EPIC-`, `STORY-`, `DEC-NNN` (worktracker-directory-structure 56–88). |
| B | 2 | Domain-slug has no entity-ID prefix and no sequence-as-ontology; it aligns with *external* norms (log4brains/JPH), not the house ontology. |
| C | 4 | Project-scoped birth aligns (5); domain-slug framework tier diverges (2) but only for the promoted minority. |
| D | 1 | No scope prefix; orthogonal to the ontology. |
| E | 1 | No scope prefix; opaque. |
| F | 4 | Has a scope prefix (aligns with the scope-prefix principle) but drops the numeric sequence the ontology uses. Partial. |

### C6 — Sortability (w=6)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 3 | Sorts by project → clusters by origin (a valid axis) but scatters same-subject ADRs across projects. |
| B | 5 | Sorts by domain-slug → subject clusters alphabetically (`ADR-agent-*`, `ADR-routing-*`); BUG-006 F-004 best sortability. |
| C | 4 | `docs/design/` sorts by domain-slug (5); each project dir is single-scope so trivially clustered. |
| D | 2 | Chronological clustering (changelog-like); poor for subject grouping. |
| E | 2 | Global number ≈ creation order; not subject. |
| F | 4 | Scope then slug → subject clusters within scope. |

### C7 — Migration cost from today's state (w=8)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 3 | Project ADRs already comply, but the **3 framework `docs/design/` ADRs would regress** to `ADR-PROJ007-*`/`ADR-EPIC002-*`, breaking 4+ live rule-file citations (`agent-design-001` ×4, `routing-triggers-001` ×5, `output-path-resolution-001` ×4). |
| B | 2 | Framework ADRs already comply (0), but **11 project ADRs** must be re-slugged + citations updated (`STORY015-001` cited ×12). High churn. |
| C | 5 | **Both** namespaces already match today's practice (framework=domain-slug, projects=project-scoped). Near-zero migration; adopt-forward + freeze legacy (research 185–194). |
| D | 1 | Everything renamed to dates; total churn. |
| E | 1 | Everything renumbered into one sequence + build a registry. Highest churn. |
| F | 2 | Drop all `NNN`, re-slug every ADR; citation breakage repo-wide. |

### C8 — Deterministic lint-ability, L5 CI (w=8)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 5 | Local regex: `^ADR-{project-id}-\d{3}-` **and** prefix must equal the containing project dir. Fully deterministic, no global state. |
| B | 3 | Form regex is easy, but **slug-uniqueness is a non-local (repo-wide) scan** and "is this a valid domain slug" edges into taxonomy judgment. |
| C | 4 | Two deterministic rules **keyed on location** (project dir → A-regex; `docs/design/` → B-regex); location disambiguates which rule applies; back-link presence is checkable. |
| D | 5 | `^ADR-\d{8}-` + valid-date assertion. Fully deterministic. |
| E | 3 | Form regex easy, but monotonicity/no-gap/no-dup needs global registry state. |
| F | 4 | Form regex deterministic; within-scope slug-uniqueness needs a scan. |

### C9 — Human ergonomics (w=6)

| Scheme | Score | Evidence |
|--------|:---:|----------|
| A | 3 | Moderate length; must mentally expand `PROJ031`. Typeable, unambiguous. |
| B | 4 | Self-documenting, reads naturally; can grow long for verbose domains. |
| C | 3 | Two forms → users carry both mental models (cognitive overhead). |
| D | 2 | Date is unreadable-as-meaning; not memorable. |
| E | 3 | Shortest/typeable but meaningless. |
| F | 3 | Self-documenting, no number to track, but long and no disambiguation for two decisions on one subject. |

---

## L1: Weighted-Sum Results

**Score table (score × weight; weighted total = Σ/100 on 1–5 scale):**

| Criterion (weight) | A | B | C | D | E | F |
|--------------------|:--:|:--:|:--:|:--:|:--:|:--:|
| C1 Collision-safety (18) | 4 | 3 | 4 | 5 | 1 | 4 |
| C2 Promotion-stability (16) | 2 | 5 | 3 | 5 | 5 | 2 |
| C4 Discoverability (14) | 2 | 5 | 4 | 2 | 1 | 5 |
| C3 Provenance (12) | 5 | 3 | 4 | 2 | 2 | 4 |
| C5 Ontology-consistency (12) | 5 | 2 | 4 | 1 | 1 | 4 |
| C7 Migration cost (8) | 3 | 2 | 5 | 1 | 1 | 2 |
| C8 Lint-ability (8) | 5 | 3 | 4 | 5 | 3 | 4 |
| C6 Sortability (6) | 3 | 5 | 4 | 2 | 2 | 4 |
| C9 Ergonomics (6) | 3 | 4 | 3 | 2 | 3 | 3 |
| **Weighted total (/5)** | **3.52** | **3.58** | **3.86** | **3.06** | **2.10** | **3.60** |
| **Rank** | 4 | 3 | **1** | 5 | 6 | 2 |

**Baseline ranking:** **C (3.86) > F (3.60) > B (3.58) > A (3.52) > D (3.06) > E (2.10)**

**Reading the result (P-022 — the honest caveat):**
- **C wins the baseline matrix**, driven almost entirely by **migration cost (C7=5)** — it is the only scheme that matches *both* of today's live practices — plus middling-to-good scores everywhere (no criterion below 3).
- **The top four (C, F, B, A) are separated by only 0.34** on a 1–5 scale. This is a **knife-edge** result: the ranking is not robust to small, defensible weight changes. That fragility is the finding, not a footnote.
- **E is decisively dominated** (2.10) — it is the failure mode the repo already suffers. **D** (3.06) is safe-but-mute: excellent on collision/promotion, near-worst on discoverability/ontology/provenance.
- **A is not dominated but is Pareto-shadowed by C**: C beats A on promotion, discoverability, sortability, migration; A beats C only on provenance, ontology-consistency, and lint simplicity. A is the "purist scope-prefix" choice; C is A softened for the framework tier.
- Note: if the defensible **B C1=4** reading is taken (slug-collision judged low-risk), B rises to **3.76** — still under C's 3.86 at baseline, but it narrows the gap and reinforces the assumption-dependence.

---

## L2: Sensitivity Analysis

The user mandated two explicit stress tests. Both are computed by re-weighting and recomputing the weighted sum; only the changed weights are noted.

### Sensitivity (a) — Promotion frequency: HIGH vs LOW  ★ the decisive test

**Rationale.** The baseline weights promotion-stability (C2) at 16 — treating promotion as *important but ordinary*. Jerry's core thesis ("accrues knowledge... from projects into the framework") and its **empirical corpus (3 of 3 framework ADRs arrived by promotion — 100%)** argue promotion is the *normal path*, which should raise C2 sharply and lower ontology-consistency (C5) and one-time migration (C7).

**High-promotion weight vector:** C1=16, **C2=28**, C4=16, C3=10, **C5=6**, **C7=4**, C8=8, C6=6, C9=6 (Σ=100).

| Scheme | Baseline (/5) | High-promotion (/5) | Δ |
|--------|:---:|:---:|:---:|
| **B** | 3.58 | **3.96** | **+0.38 → WINNER** |
| C | 3.86 | 3.70 | −0.16 |
| D | 3.06 | 3.46 | +0.40 |
| F | 3.60 | 3.46 | −0.14 |
| A | 3.52 | 3.20 | −0.32 |
| E | 2.10 | 2.56 | +0.46 |

**Result: THE WINNER FLIPS — C → B.** Under a promotion-is-normal weighting, B (3.96) overtakes C (3.70). This is the study's central finding: **the choice between C and B is entirely a referendum on how often ADRs get promoted.**

- **Low-promotion regime (promotion is the exception):** C wins. Origin-in-identity costs little because migration is rare; the near-zero adopt-forward migration and ontology-consistency dominate.
- **High-promotion regime (promotion is the point):** B wins. Every promotion under A/C/F is a citation break (a recurring tax that compounds with corpus size); B pays it *once* by moving provenance into frontmatter, then promotion is free forever.

### Sensitivity (b) — Discoverability weighted over provenance

**Rationale.** Test the crux's other half: if finding an ADR by *subject* matters more than knowing its *origin*, does the winner change? Shift 6 weight points from C3 (provenance 12→6) to C4 (discoverability 14→20); all else baseline.

| Scheme | Baseline (/5) | Discoverability-dominant (/5) | Δ |
|--------|:---:|:---:|:---:|
| **C** | 3.86 | **3.86** | 0.00 → still winner |
| B | 3.58 | 3.70 | +0.12 |
| F | 3.60 | 3.66 | +0.06 |
| A | 3.52 | 3.34 | −0.18 |
| D | 3.06 | 3.06 | 0.00 |
| E | 2.10 | 2.04 | −0.06 |

**Result: NO FLIP — C holds (3.86), but its margin over B shrinks** (0.28 → 0.16) and A drops away. C is *robust* to the discoverability-vs-provenance axis alone, because C already captures discoverability where it counts (the framework tier is domain-slug). Discoverability pressure hurts the pure-origin scheme **A** most.

### Combined (a)+(b) — high promotion AND discoverability-dominant

Applying both shifts simultaneously drives **B further ahead** (B gains from both C2↑ and C4↑; C is flat on C4 and loses on C2). Directionally B ≈ 4.0+, C ≈ 3.6. **Decisively B.** The two crux pressures are *additive* in B's favour and never favour C together.

### Tipping-point summary

| Question | Answer |
|----------|--------|
| What single assumption decides A/C vs B? | **Promotion frequency** (weight of C2). |
| Where is the tipping point? | Between the baseline (C2≈16) and high-promotion (C2≈28) vectors, B overtakes C. Approximate crossover: **C2 ≳ 22** (holding C5/C7 reduced) flips the winner to B. |
| Does discoverability alone flip it? | No — C survives (b); only (a), or (a)+(b), flips it. |
| What does the *evidence* say the regime is? | **High-promotion:** 100% of existing framework ADRs (3/3) are promotions; a citation break has already occurred (BUG-006). The corpus behaves like the regime where **B wins.** |

---

## L2: The Crux — Answered

**The question:** does encoding *origin* into identity (A/C, matching the house ontology) beat encoding *subject* into identity (B, surviving migration) — given that ADRs are the one artifact class that migrates?

**Head-on answer:** **For the migrating artifact class, subject-encoded identity (B) is structurally correct, and the ontology-consistency argument for origin-encoding is the weakest reason to override it.** Three lines of evidence converge:

1. **The ontology argument proves less than it appears.** Yes, every worktracker entity is scope-prefixed — but those entities **never change scope**. A `STORY` is born and dies a story; `DEC-NNN` is permanently parent-scoped (`EPIC-001--DEC-001`, worktracker-directory-structure 65). ADRs are categorically different: they are designed to graduate. Applying a *never-migrates* naming rule to the *one thing that migrates* is a category error. Consistency with the ontology (C5) is real but should not govern the exception the ontology never contemplated.

2. **The corpus already voted with its feet — twice, incompatibly.** The 3 framework ADRs are domain-slug (B) *despite* carrying project provenance in metadata; the ~11 project ADRs are project-scoped (A). The repo is *already* running Scheme C by accident — and C's promotion step **already broke a citation** (BUG-006 still points at `ADR-PROJ007-001`). C institutionalizes a break that B eliminates.

3. **Jerry's own thesis picks the regime.** If "knowledge accrual from projects into the framework" is the product's reason to exist, then promotion is not an edge case — it is the success condition. In that regime the sensitivity analysis is unambiguous: **B wins, and it wins by more the more the thesis is true.** Betting on A/C is, quite literally, betting *against* the framework's premise.

**The honest counter-case (kept alive per divergent method — do not dismiss):** if in practice most ADRs are *project-local forever* and only a rare few ever promote, then C is the better-calibrated choice: it gives origin-in-identity and near-zero migration for the 80–90% that never move, and pays the renumber cost only for the rare graduate. **C is not wrong — it is right under a different, testable belief about promotion frequency.** The decision therefore *reduces to ratifying that belief*, which is a human call, not an analytical one.

---

## L2: Recommendation Framework

Per NPR 7123.1D Process 17 and P-020, this study provides a **decision framework**, not a unilateral decision. The recommendation is stated conditionally so the human owner ratifies the load-bearing assumption.

### Primary recommendation (author's lean)

**Adopt Scheme B — subject-encoded identity — implemented as "domain-slug ID from birth, in a two-location layout."** Concretely:

- **Identity (from creation):** `ADR-{domain-slug}-NNN-title`. The `NNN` is per-domain-slug, zero-padded, never reused (Nygard/tombstone precedent). Subject is in the ID; **origin lives in frontmatter** (`origin_project`, `origin_entity`).
- **Location:** born in `projects/PROJ-NNN-*/decisions/`; **promotion to framework = a pure `git mv` into `docs/design/` with no ID change** and no citation churn. This is B's decisive property and the direct dissolution of the crux.
- **Provenance preserved** without encoding it in identity (satisfies P-040 via frontmatter, verified as already-practiced: `PS-ID: PROJ-007` comments in the 3 framework ADRs).
- **Enforcement:** MEDIUM-tier (SHOULD), L5 CI lint = (1) form regex `^ADR-[a-z0-9-]+-\d{3}-`, (2) **repo-wide slug-uniqueness scan** (the one non-local check B requires — cheap: a `sort | uniq -d` over ADR slugs), (3) reject *new* bare `ADR-NNN`. Freeze legacy `docs/adrs/` + archive.

**Why B over the baseline-matrix winner C:** the baseline gap is 0.28 (knife-edge) and **inverts under the promotion-frequency assumption the corpus empirically exhibits (3/3 promoted)**. B removes the recurring citation-break tax that C merely *manages* with tombstones. B's two weak criteria are exactly the two the crux argues to discount: ontology-consistency (C5 — the ontology never contemplated migrating entities) and slug-collision (C1 — mitigated by a one-line lint). Choosing B is choosing to bet *with* Jerry's accrual thesis.

### Conditional decision rules (the framework)

| Ratify this belief | Then choose | Because |
|--------------------|-------------|---------|
| **Promotion is the point** (frequent; the thesis is real) | **B** (two-location) | Zero-churn promotion compounds; sensitivity (a) → B 3.96. |
| **Promotion is the exception** (rare; most ADRs stay local) | **C** (two-namespace) | Near-zero migration + ontology-consistency dominate; baseline → C 3.86. |
| **Merge-conflict-freedom above all**, subject/scope don't matter | **D** (date-based) | C1=5, C2=5; accept mute IDs (D 3.06 but bulletproof on the top-2 weights). |
| **Purist house-ontology consistency**, promotion tolerated as manual rework | **A** | C5=5, C3=5; accept discoverability pain (BUG-006 severity-3 findings). |
| — (never) | **E** | Dominated (2.10); the live failure mode. Deprecate bare `ADR-NNN`. |

### Confidence

**0.70 (moderate).** Justification (calibrated, not inflated):
- **High confidence** in the *structural* conclusions: E is dominated; D is safe-but-mute; the winner is decided by the promotion-frequency weight; A↔C↔B↔F are a knife-edge at baseline. These are robust to reasonable weight perturbation.
- **Moderate confidence** in the *single-winner* call (B): it depends on ratifying the high-promotion belief. The empirical signal (100% of framework ADRs promoted) supports it, but n=3 is small and the framework is young — the base rate could regress toward "most ADRs stay local" as project count grows. I decline to claim >0.75 for a C4 governance flip resting on n=3.
- **Not fabricated:** the promotion-remap mechanic in Scheme C is ps-researcher synthesis (research 202), not an external standard; B's "pure file move" is a direct property of subject-encoding, not a claim requiring external authority.

### Recommended next step

Route to a decision authority (human + `nse-architecture`/`ps-architect`) to (1) **ratify the promotion-frequency belief** (the one input that decides B vs C), then (2) draft the MEDIUM-tier standard as `ADR-PROJ031-NNN` with the L5 lint spec, then (3) `/adversary` review at C4. Do **not** finalize the ID scheme before step (1).

---

## Open Questions

- **TBR-1 (load-bearing):** What is the *expected* promotion rate going forward? The winner (B vs C) hinges on it. Current evidence: 3/3 framework ADRs promoted, but n=3. Human ratification required.
- **TBR-2:** Under B, who arbitrates domain-slug taxonomy (to keep slugs unique and meaningful)? A lightweight `docs/design/README.md` domain index (BUG-006 F-004, never implemented) would serve.
- **TBR-3:** Retroactive scope — freeze legacy `docs/adrs/`/archive (recommended), or renumber? Tombstone precedent favors freeze.
- **TBR-4:** Do the ~11 existing project ADRs (Scheme A) get re-slugged to B, or grandfathered? Grandfather-with-alias minimizes churn; a big-bang re-slug is not justified by this study.
- **TBR-5:** Does `ADR-{ENTITY-ID}-NNN` (story/epic-embedded, e.g. `ADR-STORY015-001`) survive as a permitted sub-form, or collapse into the project/domain default?

---

## Evidence Ledger and P-022 Disclosures

**Filesystem-verified (this session):**
- ADR corpus enumerated via `find` — families A (`ADR-PROJ010-001..006`, `ADR-PROJ022-001/002`, `ADR-PROJ031-001..003`), entity-variant (`ADR-EPIC002-001/002`, `ADR-STORY015-001`), GH-issue variant (`ADR-150-001`), campaign variant (`ADR-OSS-001..007`), legacy bare (`docs/adrs/ADR-001..006` + amendment), archive (`ADR-031..034`), informal (`adr-cli-integration[-v2]`).
- Framework ADR provenance headers read directly: `ADR-agent-design-001` → `PS-ID: PROJ-007 | ENTRY: e-004`; `ADR-routing-triggers-001` → `PS-ID: PROJ-007`; `ADR-output-path-resolution-001` → `Parent: EPIC-002`. Confirms 3/3 promoted-with-ID-change.
- Entity-ID ontology: `worktracker-directory-structure.md` lines 56–88 (all scope-prefixed; `DEC-NNN` parent-scoped composite).
- Rule-file citation frequency via `grep`: `ADR-STORY015-001` ×12, `ADR-routing-triggers-001` ×5, `ADR-agent-design-001`/`ADR-output-path-resolution-001`/`ADR-EPIC002-001` ×4 each — evidence for discoverability (opaque vs self-documenting) and migration-cost (citations at risk).
- `git status`: PROJ-031 `decisions/` is untracked (`??`) — consistent with the mid-session bare→scoped rename reported in research 79 (I do not assert who performed it — P-022).

**Reused from prior research (independently re-verified where load-bearing):**
- Collision evidence (bare `ADR-NNN` across `docs/adrs/` + PROJ-014): re-verified via `find` — both `docs/adrs/ADR-001-*` and `.../PROJ-014-.../phase-5/ADR-001-*` exist.
- External schema facts (Nygard monotonic; MADR `NNNN-`; log4brains slug-as-ID + date-to-avoid-merge-conflicts; AWS immutability): cited from research §L1-External (lines 96–118); **not re-fetched this session** — labeled as inherited citations.

**P-022 corrections carried forward (do not reuse the errors):**
- **BUG-006 F-002 is factually wrong:** it claims `ADR-EPIC002-001` "exists in two different projects (PROJ-022 and PROJ-004)." Filesystem verification: `ADR-EPIC002-001/002` exist **only** in `projects/PROJ-001-oss-release/decisions/` (verified `find`). No PROJ-004/PROJ-022 `ADR-EPIC002` exists. The real, verified collision is in the **bare `ADR-NNN`** namespace. This trade study's C1/C4 scoring uses the *verified* collision, not BUG-006's erroneous example.
- **BUG-006 claim that the convention is "documented in `quality-enforcement.md`" is false** (that file only *cites* ADR IDs; it defines no ADR naming rule). BUG-006's Nielsen severity *rankings* (F-001/F-003 discoverability, severity 3) are directionally reused as discoverability evidence; its collision *example* (F-002) is discarded.

**Inference labels:** All criterion weights (C1–C9) and all sensitivity weight vectors are **author inference** (reasoned allocations, not facts). Scheme C's renumber-on-promotion+tombstone mechanic is **ps-researcher synthesis** (research 202), not an external standard. The promotion-frequency regime judgment ("corpus behaves high-promotion") is **inference from n=3** — explicitly low-confidence.

---

## References

- **NPR 7123.1D, Process 17** — Decision Analysis (define decision → criteria → weights → alternatives → evaluate → select → document). Method basis for this study.
- **NASA/SP-2016-6105 Rev2, §6.8** — Decision Analysis Process; trade study / weighted-scoring methodology.
- **Internal — prior research:** `projects/PROJ-031-cowork-skeleton/research/adr-convention-standards-research.md` (catalog, collision evidence, external citations, P-022 disclosures).
- **Internal — prior evaluation (caution, contains verified errors):** `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md` (Nielsen severities reused; F-002 collision example discarded as false).
- **Internal — ontology:** `skills/worktracker/rules/worktracker-directory-structure.md` (scope-prefixed entity IDs; `DEC-NNN`).
- **Internal — constraint:** `.context/rules/quality-enforcement.md` (HARD ceiling 25/25 → MEDIUM-tier mandate; tombstone/Retired-Rule-ID precedent).
- **Internal — live corpus:** `docs/design/ADR-{agent-design,routing-triggers,output-path-resolution}-001.md`; `projects/*/decisions/ADR-*`; `docs/adrs/ADR-001..006`; `docs/archive/projects-archive/decisions/ADR-031..034`.
- **External (via prior research, not re-fetched):** Nygard (Fowler/bliki); MADR (adr.github.io); log4brains ADR 20201016 (slug-as-ID; date to avoid merge conflicts); Joel Parker Henderson (name-as-ID); GOV.UK ADR Framework (scope hierarchy/promotion); AWS Prescriptive Guidance (immutability/supersede). Full URLs: research file References (lines 210–224).

---

*Generated by nse-explorer agent v1.0.0 — divergent exploration, NPR 7123.1D Process 17. Advisory only; decision reserved for human ratification per P-020.*

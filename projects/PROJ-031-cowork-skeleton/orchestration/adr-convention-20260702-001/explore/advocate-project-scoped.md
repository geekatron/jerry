# Blind Advocate Brief — Scheme A/C: Project-Scoped ADR IDs

> **Role:** BLIND advocate for identifier scheme A (`ADR-{PROJECT-ID}-NNN` at birth) and its two-namespace promotion variant C.
> **Blind constraint:** No content read from `orchestration/adr-convention-20260702-001/` other than this file. All evidence drawn from the standalone research artifact and direct filesystem reads performed in this session.
> **Status:** Complete

## Navigation

| Section | Purpose |
|---------|---------|
| [Verdict](#verdict) | The scheme I am advocating for |
| [Steelman Case](#steelman-case-for-ac) | Three evidence-backed arguments FOR project-scoped IDs |
| [The Crux, Answered](#the-crux-answered-head-on) | Direct response to the promotion-frequency challenge, with sensitivity analysis |
| [My Weakest Point](#my-weakest-point-and-mitigation) | Honest concession + mitigation |
| [Attack on B](#attack-on-b-domain-slug-everywhere) | Fatal weaknesses in domain-slug-everywhere |
| [Attack on D](#attack-on-d-date-based) | Fatal weaknesses in date-based IDs |
| [Attack on E](#attack-on-e-global-monotonic) | Fatal weaknesses in global monotonic IDs |
| [Attack on F](#attack-on-f-scopeslug-no-number) | Weaknesses in scope+slug-no-number |
| [What Would Change My Mind](#what-would-change-my-mind) | Falsification conditions |
| [Evidence Index](#evidence-index) | All cited sources with paths/lines |

---

## Verdict

**I advocate for Scheme A at birth (`ADR-{PROJECT-ID}-NNN` in `projects/PROJ-NNN-*/decisions/`), formalized as Scheme C** (project-scoped at birth, domain-slug only after a deliberate promotion event, with tombstone back-links). I do **not** advocate for pure "domain-slug from birth" (B) — the crux challenge is real and I answer it directly below rather than dodging it.

---

## Steelman Case for A/C

### 1. Project-scoped IDs are not a new pattern invented for ADRs — they are the ONLY pattern Jerry's entity ontology uses, everywhere, for everything

Jerry's worktracker directory structure defines the full entity hierarchy — Epic, Feature, Story, Enabler, Task, Bug, Discovery, Impediment, Decision, Spike — and **every single one** carries scope in its identifier, either directly (`{EpicId}-{slug}`, `{FeatureId}-{slug}`, `{StoryId}-{slug}`) or via an explicit parent-prefix when co-located with a non-owning parent (`{EpicId}--{DecisionId}-{slug}.md`, e.g. `EPIC-001--DEC-001-worktracker-planning.md`; `{FeatureId}--{DecisionId}-{slug}.md`, e.g. `FEAT-001--DEC-001-id-scheme.md`) (`skills/worktracker/rules/worktracker-directory-structure.md:60-90`, specifically lines 65, 73, 80, 88 for the four nesting levels of the `DEC-NNN` Decision File entity). There is no artifact type anywhere in this ontology that uses a bare global sequence or a subject-slug-only identity. An ADR is functionally a sibling of the worktracker's own `DEC-NNN` Decision File — scheme A/C simply extends the same `{Scope}-{NNN}` grammar that already governs every other entity. Adopting bare domain-slug IDs (B) for ADRs specifically would make ADRs the **one outlier artifact type** in the entire framework whose ID string carries zero scope information — a structural inconsistency, not a simplification.

### 2. It is the dominant, already-collision-free, already-converged-upon practice, and the collision record directly indicts the alternative

The research catalog counts project/entity-scoped ADR families already in production: `ADR-PROJ010-NNN` ×6, `ADR-PROJ022-NNN` ×2, `ADR-PROJ031-NNN` ×3, `ADR-EPIC002-NNN` ×2, `ADR-STORY015-NNN` ×1, `ADR-150-NNN` (GH-issue-scoped) ×1 — **15 ADRs**, all scope-prefixed, **all collision-free by construction** (`projects/PROJ-031-cowork-skeleton/research/adr-convention-standards-research.md:57-63`). Against this, the bare/unscoped namespace has **already collided three separate times in the live repository**: `ADR-001` across `docs/adrs/ADR-001-agent-architecture.md`, `docs/adrs/ADR-001-amendment-001-python-preprocessing.md`, and `projects/PROJ-014-.../ADR-001-npt014-elimination.md`; `ADR-002` and `ADR-003` each collide similarly across `docs/adrs/` and PROJ-014 (`adr-convention-standards-research.md:74-77`). The research explicitly documents that mid-session, the three PROJ-031 ADRs were renamed from bare `ADR-001..003` to scoped `ADR-PROJ031-001..003`, and characterizes this as **"the strongest internal signal that the team is already converging on project-ID scoping"** (`adr-convention-standards-research.md:79`). This is not a hypothetical risk I am asserting for A/C — it is Jerry's own recorded incident history, and it is exactly the class of failure (unscoped, effectively-global sequential numbering) that log4brains documents abandoning after git-merge collisions (`adr-convention-standards-research.md:100`). Scheme A is immune to this by construction because Jerry already allocates project IDs uniquely at project creation (`.context/rules/project-workflow.md` "Project Resolution" — auto-generated `PROJ-{NNN}-{slug}` from `projects/README.md`); no new registry or tooling is required.

### 3. Scheme C does not force an all-or-nothing choice — it captures B's stated benefit exactly where it already applies, without disrupting the birth-time majority

The two-namespace variant (C) uses domain-slug IDs (B's form) for the framework tier and project-scoped IDs (A's form) for the project tier — and this is **not a novel proposal**, it is a codification of what has already happened. All three existing `docs/design/` framework ADRs (`ADR-agent-design-001`, `ADR-routing-triggers-001`, `ADR-output-path-resolution-001`) carry explicit project-origin provenance in their own metadata (PS-ID/PROJ-007, EPIC-002) (`adr-convention-standards-research.md:85`), proving they too were **born project-scoped** and only later promoted — under scheme C, zero migration is required for these three files; the "promotion" already happened informally, and C only formalizes the process (frontmatter provenance + bidirectional back-link) around an already-observed pattern. Externally, the GOV.UK ADR Framework independently corroborates this maturity gradient: an explicit team/project → programme → departmental-board → cross-department escalation hierarchy, with the rule to "determine the scope of the decision and identify the appropriate decision-making level" (`adr-convention-standards-research.md:110-112`, citing GOV.UK). You typically do not know an ADR is framework-wide the day it is written — you learn this by living with it inside a project first. C is the only scheme of the five under evaluation that matches this observed lifecycle rather than forcing a premature scope declaration (B) or ignoring scope entirely (D/E).

---

## The Crux, Answered Head-On

**The challenge, restated:** Jerry's thesis is knowledge *accrual* — projects feed the framework. If ADR promotion is the point rather than the exception, then subject-encoded identity (B) — which makes promotion a zero-churn file move — should dominate over origin-encoded identity (A/C), which pays an ID-remap-and-citation-repoint cost at every promotion.

**This is the correct question, and I will not dodge it: the answer depends entirely on the empirical promotion rate, and I concede the sensitivity.**

**Current measured rate (low):** Of the ADRs cataloged in the research (11 project/entity-scoped in the current live-project families, plus 6 legacy + 4 archived + 4 transient + 7 orchestration-series bare/informal ones — roughly 30+ total logged ADR-shaped artifacts across the repo's history), only **3 have ever been promoted to framework scope** (`adr-convention-standards-research.md:58-59` vs. the full catalog at lines 57-68). That is a promotion rate on the order of ~10% of all ADRs ever created, measured against Jerry's actual history to date. At this rate, scheme C's promotion-time churn (3 events) is dwarfed by the collision-avoidance benefit scheme A provides continuously across the other ~90% of ADRs that never promote and stay project-scoped for their entire lifecycle.

**Where the sensitivity bites:** If the promotion rate rises materially — say, if Jerry's stated "framework accrues knowledge from projects" identity (`CLAUDE.md` Identity section: "Accrues knowledge, wisdom, experience") becomes the *dominant* mode of ADR creation rather than the exception, such that most ADRs are written with framework-wide intent from day one — then B's zero-churn promotion becomes the dominant benefit and A/C's per-promotion churn cost compounds. I do not have a forward-looking measurement for this (the research explicitly flags the promotion mechanic itself as synthesis, not externally sourced: `adr-convention-standards-research.md:113, 158, 202`), so I cannot rule out this future. **My position is therefore conditional, not absolute**: at the current and historical promotion rate (~10%), A/C dominates on collision-avoidance grounds; if that rate is later shown to exceed roughly a third to a half of all ADRs (the point at which "most ADRs eventually promote" becomes true rather than "some ADRs sometimes promote"), the case for B strengthens materially and I would want the decision revisited — see [What Would Change My Mind](#what-would-change-my-mind).

**Why I still favor A/C even under moderate promotion-rate growth:** Citation churn under C is a **bounded, mechanical, one-time cost per promotion event** (grep for the old structured ID string, replace, add a tombstone row — see mitigation below), whereas B's alternative cost (birth-time global slug-uniqueness policing) is a **continuous, unbounded, per-ADR cost paid by every author of every ADR, whether or not it ever promotes** (see [Attack on B](#attack-on-b-domain-slug-everywhere)). Even in a high-promotion-rate future, C's cost only scales with the promotion count; B's cost scales with total ADR count, which is strictly larger. The crossover point where B becomes cheaper in aggregate requires not just "promotion is common" but "promotion is common **and** slug-collision risk at birth is cheap to manage" — and the research shows Jerry currently has no slug-uniqueness enforcement mechanism at all (no CI lint, no registry), so B's assumed cheap birth-time cost is itself unproven.

---

## My Weakest Point (and Mitigation)

**Honest concession:** The genuine, undodgeable cost of A/C is **citation-continuity break on promotion**. When an ADR is promoted from `ADR-PROJ007-004` (hypothetical) to `ADR-agent-design-001`, every citation across rule files, other ADRs, and worktracker entries that referenced the old ID must be found and repointed, and any reader holding the old ID needs a redirect. This is not hypothetical bookkeeping — it is a real, demonstrated cost already paid for the 3 existing promotions. The domain-slug ID `ADR-agent-design-001` is currently cited in at least four locations I directly verified in this session: `.context/rules/agent-development-standards.md:3` (version header `SOURCE: ADR-agent-design-001...`), `:445` (References table row), and `:471` (footer `Source:` line); similarly `ADR-routing-triggers-001` is cited in `.context/rules/agent-routing-standards.md:3, 539, 553`. Every one of those citation sites had to be written using the **post-promotion** ID — if those rule files had been drafted before promotion (citing the original `ADR-PROJ007-NNN` form) and then the ADR was promoted, all of those sites would have needed a repoint pass. This is exactly the cost the crux challenge is pointing at, and it is real.

**Mitigation:**
1. **Jerry already has a working tombstone precedent for exactly this problem, in production, today.** `quality-enforcement.md:79-81` maintains a "Retired Rule IDs" table for HARD-rule consolidation: *"Rule IDs below were retired... These IDs MUST NOT be reassigned. Consequence: reassignment breaks historical cross-references... Instead: when consolidating rules, retire the old ID into the Retired Rule IDs table and document the mapping to its replacement."* This is a direct, zero-new-tooling template for an "ADR Promotion Ledger": on promotion, add one row (`Old ID | New ID | Promotion Date`) and flip the original file's `Status:` to `Superseded`/`Promoted-To:` (exactly as the research's own promotion-process synthesis proposes: `adr-convention-standards-research.md:163`).
2. **Promotions are rare, so the aggregate mitigation cost is small.** At 3 promotions against ~30+ total ADRs, the total citation-repoint burden across the framework's entire lifetime to date is bounded and small, while the collision-avoidance benefit of A applies continuously to every one of those 30+ ADRs, every day.
3. **Repointing is mechanical, not judgment-based.** Because IDs are structured, unique strings (`ADR-PROJ007-004`, not a natural-language slug that might appear coincidentally elsewhere in prose), `grep -rl "ADR-PROJ007-004"` deterministically finds every citation site; an L5 CI lint could even flag any surviving reference to a tombstoned ID automatically. This is a strictly easier detection problem than B's silent-collision risk (see next section), which produces no error signal at all when two authors independently coin the same slug.

---

## Attack on B (domain-slug-everywhere)

**Fatal weakness: B does not eliminate coordination cost — it relocates it from "rare, mechanical, one-time" (A/C's promotion cost) to "constant, judgment-based, silent" (B's birth-time slug-uniqueness cost), and Jerry's own incident history shows this exact failure mode already happening.**

The three verified collisions in the bare/unscoped ADR namespace (`ADR-001`, `ADR-002`, `ADR-003` each independently reused across `docs/adrs/` and `projects/PROJ-014-.../`, `adr-convention-standards-research.md:74-77`) occurred precisely because there was no scope marker forcing authors into disjoint ID spaces and no enforcement mechanism catching the reuse. B's design — a domain-slug as the *sole* identity marker for every ADR from birth, not just the rare promoted ones — requires every author of every new ADR (not 3 promotions, but all ~30+ ADRs and every one going forward) to check a global slug registry that **does not currently exist in Jerry** (confirmed: the research searched 11 locations — rules, governance, templates, skills, worktracker — and found no ADR standard of any kind, `adr-convention-standards-research.md:33-49`). B's promise of "zero ID churn on promotion" is true only for the promotion transaction itself; it ignores that the aggregate slug-collision-avoidance tax is now paid on **every** ADR, continuously, rather than on the minority that ever promote. Worse, unlike a duplicate `PROJ-NNN` (which Jerry's project-creation process already prevents structurally via unique allocation from `projects/README.md`), a duplicate domain-slug produces **no error at all** — two authors in two different projects can independently pick `ADR-caching-strategy-001` with no signal until someone notices two unrelated files sharing an ID.

**Secondary attack:** Under B, an ADR's ID string alone carries zero information about which project/team owns it or where the file physically lives — directly contradicting the self-documenting-ID convention every other Jerry entity type uses (`worktracker-directory-structure.md:60-90`: `PROJ-NNN`, `EPIC-NNN`, `FEAT-NNN`, `STORY-NNN`, `DEC-NNN` all encode scope in the string itself, precisely so a bare ID is locatable and attributable without opening the file or checking frontmatter). B optimizes for the rare promotion event at the expense of the common, everyday case: browsing, citing, and locating an ADR by ID alone.

---

## Attack on D (date-based)

**Fatal weakness: D solves a problem Jerry does not have (numeric-ID git-merge conflicts) at the cost of discarding the one piece of information Jerry's evidence shows matters most (scope/ownership) — and it doesn't even fully solve the collision problem it targets.**

Log4brains adopted `YYYYMMDD-slug` specifically because *"ADR numbers must be unique," which "caused conflicts during git merge when two developers created new ADRs on their respective branches"* (`adr-convention-standards-research.md:100`, citing the log4brains ADR). But Jerry's project-scoped families are **already immune to this exact failure mode by construction** — each project's ADR sequence is independent, so there is no shared counter for two branches to collide over; the catalog shows 11+ project-scoped ADRs across 5 project families with zero reported merge-conflict incidents (`adr-convention-standards-research.md:60-63`). D would import a fix for a problem A doesn't have, while creating two new problems: (1) two decisions made on the same calendar day in two different projects (e.g., a PROJ-010 ADR and a PROJ-022 ADR both on 2026-07-02) collapse to `ADR-20260702-{slug}` pairs distinguishable **only by slug** — reintroducing B's exact silent-collision risk on top of the date collision; and (2) all scope information is lost, and so is within-project sequence information — a date-based ID cannot tell a reader whether it is a project's 1st or 51st recorded decision, unlike `ADR-PROJ031-003`, which self-documents its position in the sequence. Finally, D would introduce a **second, foreign ID grammar** into a framework whose every other entity (`PROJ/EPIC/FEAT/STORY/BUG/DISC/IMP/DEC/TASK/SPIKE`, all in `worktracker-directory-structure.md:60-90`) uses sequential-within-scope numbering with zero date-based precedent anywhere.

---

## Attack on E (global monotonic)

**Fatal weakness: E is the precise scheme that has already failed in this repository, on the record, and fixing it would require centralized tooling Jerry does not have and A does not need.**

The bare `ADR-NNN` namespace is, in effect, an attempted global monotonic sequence with no registry enforcing it — and it has already collided three times in the live repository (`ADR-001` ×3 contexts, `ADR-002` ×2, `ADR-003` ×2; `adr-convention-standards-research.md:74-77`). This is not a hypothetical risk for E; it is Jerry's own recorded incident history for the closest scheme to E that has actually been tried. A properly-implemented E (true MADR-style global monotonic numbering, per `adr-convention-standards-research.md:98,104`) would additionally require a **central registry or counter mechanism** to allocate the next number safely across concurrent branches and contributors — and the research confirms no such tool exists anywhere in Jerry today (11 locations searched, zero found: `adr-convention-standards-research.md:33-49`; no `jerry adr next-number`-style command referenced anywhere). Scheme A needs no equivalent new tooling because project IDs are **already** uniquely allocated at project-creation time via the existing `projects/README.md` mechanism (`.context/rules/project-workflow.md`, Project Resolution section) — A's collision-freedom is a byproduct of infrastructure Jerry already has; E's would require infrastructure Jerry would have to build. Additionally, E is precisely the design log4brains explicitly abandoned after the documented git-merge-conflict failure mode (`adr-convention-standards-research.md:100`) — and Jerry's fully-distributed multi-project workflow (every project isolated under its own `projects/PROJ-NNN-slug/` directory, explicitly designed to support many concurrent projects per `project-workflow.md`) makes concurrent-branch numbering collisions *more* likely for Jerry than for the single-team repositories E-style schemes were designed around, not less.

---

## Attack on F (scope+slug, no number)

This is the weakest of the three rivals to attack because it retains A's scope-prefix (its main defense against B's and D/E's fatal flaws), so I disclose this honestly rather than overstating it. F's actual weakness is narrower: it still requires slug-uniqueness discipline, just scoped down to a single project rather than the whole repository — a materially smaller and more tractable version of B's problem, since a single project's ADR count is small enough for an author to visually scan existing slugs before picking a new one. The real cost is losing monotonic-sequence information: F cannot self-document "this is the 3rd ADR in PROJ-031" the way `ADR-PROJ031-003` can — a reader must open the file or list the directory to learn sequence position, whereas A's numeric suffix carries that information in the ID string itself for free. This is a real but minor loss (a directory listing recovers the count either way), and I flag it as the least damaging of the three rival attacks rather than inflating it to fatal status.

---

## What Would Change My Mind

1. **A promotion-rate audit showing promotion is the dominant mode, not the exception.** If a forward-looking measurement (promoted ADRs ÷ total ADRs created, tracked over the next several months/projects) shows the rate rising materially above the current ~10% historical baseline (`adr-convention-standards-research.md:57-68` — 3 of ~30+) — say, crossing into "most ADRs eventually promote" territory — the case for B's zero-churn promotion strengthens substantially and I would want the decision revisited.
2. **Adoption of a slug-uniqueness enforcement mechanism.** If Jerry built a global domain-slug registry or CI lint analogous to the existing `PROJ-NNN` unique-allocation mechanism, B's fatal weakness (silent collision at birth) would be neutralized, materially closing the gap between B and A/C.
3. **Evidence that the existing 3 promotions already left dangling stale-ID citations.** I asserted that mechanical grep-based repointing is reliable, but I did not exhaustively audit whether any citation of a pre-promotion ID (e.g., an original `ADR-PROJ007-NNN` form for what is now `ADR-agent-design-001`) still survives uncorrected anywhere in the repository. If such dangling references exist today, that is direct evidence my mitigation claim is optimistic rather than proven, and would weaken my defense of A/C's weakest point.

---

## Evidence Index

| Claim | Source | Location |
|---|---|---|
| Every worktracker entity type encodes scope in its ID (Epic/Feature/Story/Decision nesting, incl. `{ParentId}--DEC-NNN` pattern) | `skills/worktracker/rules/worktracker-directory-structure.md` | Lines 60-90 (specifically 65, 73, 80, 88 for DEC-NNN) |
| Catalog of project/entity-scoped ADR families (PROJ010×6, PROJ022×2, PROJ031×3, EPIC002×2, STORY015×1, GH-150×1) | `adr-convention-standards-research.md` | Lines 57-68 |
| Bare `ADR-NNN` collision evidence (ADR-001/002/003 each reused across unrelated contexts) | `adr-convention-standards-research.md` | Lines 74-77 |
| PROJ-031 bare→scoped migration cited as "strongest internal signal" of convergence on project-ID scoping | `adr-convention-standards-research.md` | Line 79 |
| Framework ADRs carry project-origin provenance metadata, proving de-facto prior promotion | `adr-convention-standards-research.md` | Line 85 |
| Log4brains abandoned numeric IDs after git-merge collisions; adopted date-based IDs | `adr-convention-standards-research.md` | Line 100 |
| No canonical multi-project numbering rule exists in the external ecosystem | `adr-convention-standards-research.md` | Line 104 |
| GOV.UK scope-determination/escalation hierarchy (team/project → programme → board → cross-department) | `adr-convention-standards-research.md` | Lines 110-112 |
| No ADR standard of any kind found anywhere in repo (11 locations searched) | `adr-convention-standards-research.md` | Lines 33-49 |
| Promotion-process ID-remap mechanic explicitly labeled as synthesis, not externally sourced | `adr-convention-standards-research.md` | Lines 113, 158, 163, 202 |
| Retired Rule IDs tombstone precedent (reusable model for ADR promotion ledger) | `.context/rules/quality-enforcement.md` | Lines 79-81 |
| `ADR-agent-design-001` cited across multiple locations in a single rule file (post-promotion ID propagation) | `.context/rules/agent-development-standards.md` | Lines 3, 445, 471 |
| `ADR-routing-triggers-001` cited across multiple locations in a single rule file (post-promotion ID propagation) | `.context/rules/agent-routing-standards.md` | Lines 3, 539, 553 |
| Project IDs already uniquely allocated at project creation (no new registry needed for A) | `.context/rules/project-workflow.md` | "Project Resolution" section |

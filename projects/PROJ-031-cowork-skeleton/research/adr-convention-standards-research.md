# ADR Identifier, Location, and Promotion Convention Standards — Research

> **PS:** PROJ-031-cowork-skeleton | **Type:** Governance research (C3) | **Created:** 2026-07-02
> **Agent:** ps-researcher | **Status:** Complete | **Confidence:** High (internal: verified by filesystem; external: multi-source cited)
> **Persistence note (P-022):** The ps-researcher agent returned this report as its handoff text (its execution environment consumes the agent's final message rather than files it writes); the orchestrator persisted it here verbatim per P-002.

## Navigation

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Does a standard exist? One-paragraph recommendation |
| [Verdict: Confirm-or-Refute](#verdict-confirm-or-refute) | Definitive answer + locations checked |
| [L1: Internal Catalog + Evidence](#l1-internal-catalog--evidence) | Every ADR-ID family, collision evidence, prior art |
| [L1: External Best Practices](#l1-external-best-practices-cited) | Cited findings from Nygard/MADR/adr-tools/log4brains/GOV.UK/AWS |
| [L2: Recommendation for Jerry](#l2-recommendation-for-jerry) | ID scheme, location model, promotion, superseding, template, tiering, migration |
| [P-022 Disclosures](#p-022-disclosures-corrections-inference-gaps) | Corrections, inference vs fact, gaps |
| [References](#references) | All sources with URLs |

---

## L0: Executive Summary

**Does a documented standard exist? No.** After exhaustively searching every governance, rules, template, skill, and decisions surface in the repository, there is **no documented standard** governing ADR identifiers, numbering, canonical location, promotion, or superseding. The preliminary main-context finding is **CONFIRMED**. What exists is: (1) a Nygard *body-structure* template with a bare `ADR-{NUMBER}` placeholder that also points at a non-existent `docs/decisions/` directory; (2) `skills/architecture/SKILL.md`, which prescribes `docs/design/ADR_NNN_*.md` with an underscore separator that mismatches every real file's hyphen; and (3) a single *review artifact* (`BUG-006-adr-naming-evaluation.md`, a Nielsen usability evaluation) that *recommends* a domain-first scheme but was never adopted as a rule and whose central collision example is factually wrong (corrected below). The bare `ADR-NNN` namespace does collide across scopes, while every scope-prefixed family (`ADR-PROJ031-NNN`, `ADR-PROJ010-NNN`, etc.) is collision-free.

**One-paragraph recommendation:** Adopt a **MEDIUM-tier (SHOULD/RECOMMENDED) two-namespace, scope-keyed ADR convention** that codifies what the framework already does well: **framework-scoped ADRs** use domain-slug IDs `ADR-{domain-slug}-NNN` in `docs/design/` (zero migration — the 3 existing framework ADRs already comply), and **project-scoped ADRs** use `ADR-{PROJECT-ID}-NNN` in `projects/PROJ-NNN-*/decisions/` (the already-dominant, already-collision-free pattern — PROJ-031 was migrated to it mid-session). Deprecate the bare `ADR-NNN` scheme for *new* ADRs, freeze the legacy `docs/adrs/` (transcript-skill) and archived sets rather than renumber them, and add a lightweight promotion process (create-new + provenance frontmatter + bidirectional back-link, mirroring the framework's already-observed promotion of PROJ-007 decisions into `docs/design/`). Enforce via L5 CI lint, not a HARD rule — the HARD ceiling is at 25/25 with zero headroom.

---

## Verdict: Confirm-or-Refute

**VERDICT: A documented ADR identifier/naming/location/promotion/superseding standard DOES NOT EXIST.** (Preliminary finding CONFIRMED.)

Locations searched (all read or grepped; results below are exhaustive for the ADR-standard question):

| # | Location checked | ADR *standard* found? | What is actually there |
|---|---|---|---|
| 1 | `.context/rules/` (all 17 files) | **No** | ADRs are only *cited* as references (e.g., `ADR-STORY015-001`, `ADR-agent-design-001`, `ADR-output-path-resolution-001`, `ADR-EPIC002-001`). `AD-M-011` cites `ADR-output-path-resolution-001` for output paths; nothing defines ADR ID/location/promotion. `quality-enforcement.md` has a "Retired Rule IDs" tombstone principle (relevant precedent) but nothing on ADRs. |
| 2 | `docs/governance/` (`JERRY_CONSTITUTION.md`, `AGENT_CONFORMANCE_RULES.md`, `BEHAVIOR_TESTS.md`) | **No** | Zero matches for "ADR" / "architecture decision" in any of the three. |
| 3 | `docs/design/` | **No** | Contains 3 framework ADRs + 2 non-ADR design docs. No standard/README. |
| 4 | `docs/adrs/` | **No** | 6 legacy ADRs (+1 amendment) for the `/transcript` skill. No standard. |
| 5 | `skills/architecture/SKILL.md` | **No (only implied usage)** | `decision` command → `docs/design/ADR_NNN_*.md` (underscore); template header shows `ADR-001` (hyphen). Separator self-contradiction; no ID/scope/collision/promotion rules. |
| 6 | `skills/worktracker/rules/` (all) | **No** | `worktracker-templates.md` points at the ADR *template*; `worktracker-content-standards.md` says "use ADR or Description." Defines a *separate* `DEC-NNN` "Decision File" entity scoped as `{ParentId}--DEC-NNN-slug` — a distinct artifact, not an ADR standard. |
| 7 | `.context/templates/` | **No** | No `adr` template here; `TDD.template.md` merely references an "ADR ID / Supersedes" column. The ADR template lives at `docs/knowledge/exemplars/templates/adr.md`. |
| 8 | `docs/knowledge/exemplars/templates/adr.md` | **Partial (body only)** | Nygard body structure; title placeholder `ADR-{NUMBER}` (underspecified); `Supersedes`/`Superseded By` frontmatter + a Related-Decisions `SUPERSEDES` row exist, but **no** numbering/scope/collision/location/promotion guidance. PS-Integration line points to non-existent `docs/decisions/`. |
| 9 | `CLAUDE.md`, `AGENTS.md` | **No** | `AGENTS.md` only lists ps-architect/eng-architect as ADR *producers*. No standard. |
| 10 | `docs/knowledge/` (broad grep) | **No** | Only incidental ADR citations (e.g., agent-pattern-taxonomy). |
| 11 | Filename search for any `*adr*standard*`, `*adr*convention*`, `*adr*guide*`, `*decision-record*` | **No** | None exist. |

The closest thing to a naming decision anywhere is **`PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md`** — but it is a **Nielsen heuristic *evaluation* (a review deliverable in a project `reviews/` folder), not an adopted rule or standard**, and its recommended follow-ups (a `docs/design/README.md` domain index, a template update) were never implemented (both confirmed absent).

---

## L1: Internal Catalog + Evidence

### Catalog of every ADR-ID convention in use (filesystem-verified)

| Family | ID pattern | Example | Count | Canonical location | Classification |
|---|---|---|---|---|---|
| **Framework domain-slug** | `ADR-{domain-slug}-NNN` | `ADR-agent-design-001`, `ADR-routing-triggers-001`, `ADR-output-path-resolution-001` | 3 | `docs/design/` | **Framework-scoped** (de-facto promoted; carry PROJ-007/EPIC-002 provenance in metadata) |
| **Project-ID scoped** | `ADR-PROJ{NNN}-NNN` | `ADR-PROJ010-001` … `-006`; `ADR-PROJ022-001/002`; `ADR-PROJ031-001/002/003` | 6 + 2 + 3 = 11 | `projects/PROJ-NNN-*/decisions/` | **Project-scoped, collision-free** |
| **Epic-ID scoped** | `ADR-EPIC{NNN}-NNN` | `ADR-EPIC002-001/002` | 2 | `PROJ-001-oss-release/decisions/` | Project-scoped (entity-keyed), collision-free |
| **Story-ID scoped** | `ADR-STORY{NNN}-NNN` | `ADR-STORY015-001` | 1 | `PROJ-024-*/work/.../STORY-015-*/` | Project-scoped, co-located with the story |
| **GH-issue scoped** | `ADR-{issue}-NNN` | `ADR-150-001` | 1 | `PROJ-030-bugs/decisions/` | Project-scoped (keyed to GH issue #150), collision-free |
| **Bare sequential (legacy framework)** | `ADR-NNN-slug` (+ `ADR-NNN-amendment-NNN`) | `ADR-001-agent-architecture` (+ `ADR-001-amendment-001-python-preprocessing`) | 6 (+1 amendment) | `docs/adrs/` | **Legacy** — `/transcript` skill; **collision source** |
| **Bare sequential (archived)** | `ADR-0NN-slug` | `ADR-031`…`ADR-034` | 4 | `docs/archive/projects-archive/decisions/` | **Archived/frozen**; occupies the `031–034` range |
| **Bare sequential (project, transient)** | `ADR-NNN-slug` | `ADR-001-npt014-elimination` … `ADR-004-compaction-resilience` | 4 | `PROJ-014-*/orchestration/.../phase-5/` | Project decision in orchestration artifacts; **collision source** |
| **OSS orchestration series** | `ADR-OSS-NNN` | `ADR-OSS-001` … `-007` | 7 | `PROJ-001-*/.../orchestration/.../ps/phase-2/ps-architect-00N/` | Orchestration work artifacts (transient, per-agent) |
| **Lowercase ad-hoc** | `adr-{slug}[-vN]` | `adr-cli-integration`, `adr-cli-integration-v2` | several | `projects/*/orchestration/.../` | Informal orchestration drafts |

### Collision evidence (verified)

The **bare `ADR-NNN` namespace collides across independent scopes** (the preliminary finding, confirmed with precision):

- **`ADR-001`** — 4 files carry the prefix across **3 distinct decision contexts**: `docs/adrs/ADR-001-agent-architecture.md` (transcript) + `docs/adrs/ADR-001-amendment-001-python-preprocessing.md` (an amendment *within* the transcript context) + `PROJ-014-.../phase-5/ADR-001-npt014-elimination.md` (neg-prompting) + (at session start) `projects/PROJ-031-.../decisions/ADR-001-skeleton-derived-branch-strategy.md`.
- **`ADR-002`** — `docs/adrs/ADR-002-artifact-structure.md` + `PROJ-014/.../ADR-002-constitutional-upgrades.md` + (at session start) `PROJ-031 ADR-002`.
- **`ADR-003`** — `docs/adrs/ADR-003-bidirectional-linking.md` + `PROJ-014/.../ADR-003-routing-disambiguation.md` + (at session start) `PROJ-031 ADR-003`.
- **Range reuse:** archived `ADR-031..034` occupy a range that a future bare "PROJ-031" numbering could visually alias.

**Live observation (P-022):** During this session the three PROJ-031 bare files (`ADR-001..003-*`) were **renamed to the scoped form `ADR-PROJ031-001..003-*`** (timestamped 2026-07-02, untracked in git). Current live counts are therefore `ADR-001`→3 files/2 contexts (transcript + neg-prompting), `ADR-002`→2, `ADR-003`→2 — but the **cross-scope collision between `docs/adrs/` (transcript) and PROJ-014 (neg-prompting) persists**. This mid-flight migration is itself the strongest internal signal that the team is already converging on project-ID scoping.

**By contrast, every scope-prefixed family is collision-free by construction** — the globally-unique project/entity/issue ID namespaces the sequence.

### Prior art inside the repo (relevant precedents)

- **De-facto promotion already happens.** The three `docs/design/` framework ADRs carry project provenance in their own metadata (`ADR-agent-design-001` → `PS-ID: PROJ-007 | ENTRY: e-004`; `ADR-routing-triggers-001` → `PROJ-007`; `ADR-output-path-resolution-001` → `Parent: EPIC-002`) yet are identified by **domain slug**, not project ID. BUG-006 even lists the first as "`ADR-PROJ007-001-agent-design.md`" — i.e., the community references confirm these were **elevated from project scope to framework scope with an ID change**, but *no documented process governs it*.
- **In-body amendment practice.** `ADR-PROJ031-001` uses dated `AMENDED YYYY-MM-DD` blocks, relative sibling cross-links (`./ADR-PROJ031-003-...md`), and explicitly distinguishes "amended by, not superseded by." `docs/adrs/` instead uses a **separate amendment file** (`ADR-001-amendment-001-...`). Two competing amendment styles exist, ungoverned.
- **Tombstone precedent.** `quality-enforcement.md`'s "Retired Rule IDs" table (never reassign a retired ID; document the mapping) is a directly reusable model for "never reuse / never renumber, alias instead."
- **Separate `DEC-NNN` entity.** Worktracker already defines user↔Claude "Decision Files" as `{ParentId}--DEC-NNN-slug` — a *scoped* decision-ID precedent distinct from ADRs (worth referencing so the new standard doesn't conflate the two).

---

## L1: External Best Practices (cited)

Facts below are attributed to specific sources; inference is labeled.

### (a) Identifier schemes — sequential vs scoped/slug

- **Sequential-number school (source-verified fact):** Nygard's original convention numbers ADRs "sequentially and monotonically," never reusing numbers, one file each, filename `doc/arch/adr-NNN.md`, with a decision-capturing name ([Fowler/bliki](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html); [Nygard/Cognitect 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)). **MADR** formalizes `NNNN-title-with-dashes.md`, 4-digit consecutive number, lowercase+dashes, "assume there won't be more than 9,999 ADRs in one repository" ([MADR](https://adr.github.io/madr/); [adr/madr](https://github.com/adr/madr)). **adr-tools** auto-computes the next monotonic number ([npryce/adr-tools](https://github.com/npryce/adr-tools)).
- **Slug/name-as-ID school (source-verified fact):** **Log4brains** made an explicit decision titled *"Use the ADR slug as its unique ID"* ([log4brains ADR 20201016](https://thomvaill.github.io/log4brains/adr/adr/20201016-use-the-adr-slug-as-its-unique-id/)). **Joel Parker Henderson's** widely-used collection deliberately uses descriptive kebab-case names (e.g., `choose-database.md`) with **no numbering system at all** ([joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)).
- **Merge-conflict-avoidance variant (source-verified fact):** Log4brains abandoned `NNNN-` because "ADR numbers must be unique," which "caused conflicts during git merge when two developers created new ADRs on their respective branches," switching to `YYYYMMDD-adr-title.md` ([log4brains](https://github.com/thomvaill/log4brains); ADR 20201016). This is precisely the failure mode Jerry's bare `ADR-NNN` exhibits.

### (b) Numbering in monorepos / multi-project / multi-team

- Two documented patterns emerge (source-verified): **(i) single global monotonic sequence + labels/tags** to organize by team/service (e.g., SimplerGrants uses labels to scope ADRs/issues per service — [SimplerGrants repo-organization ADR](https://wiki.simpler.grants.gov/product/decisions/adr/2025-01-02-repo-organization)); **(ii) per-package/per-project ADR directories** co-located with each package's source (Log4brains stores ADRs "next to the source code of the project, in the same git repository," and documents monorepo multi-package usage — [log4brains](https://github.com/thomvaill/log4brains)). Joel Parker Henderson's repo is silent on multi-team/monorepo scoping (verified via fetch), confirming the ecosystem has **no single canonical multi-project numbering rule** — teams choose per-directory folders or scoped prefixes. **Inference:** Jerry's `ADR-{PROJECT-ID}-NNN` is a clean instance of the "scoped prefix" pattern and is well-aligned with the per-project-directory approach.

### (c) Canonical file locations

- **Nygard:** `doc/arch/` ([Fowler](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)). **MADR:** *"Create folder `docs/decisions` in your project"* ([MADR](https://adr.github.io/madr/)). **adr-tools:** default `doc/adr/`. **Log4brains/JPH:** `docs/adr/` or `adr/`, **next to source** ([log4brains](https://github.com/thomvaill/log4brains); [JPH](https://github.com/joelparkerhenderson/architecture-decision-record)). Consensus: **one repo-relative decisions directory, ADRs live with the code.** Note: Jerry's template targets `docs/decisions/` (the MADR name) but Jerry actually uses `docs/design/` + `projects/*/decisions/` — so the template inherited MADR's directory name without Jerry ever creating it.

### (d) Promotion / scope elevation (project → org/framework)

- **Source-verified (hierarchy + escalation exists):** The **UK Government ADR Framework** defines an explicit multi-level hierarchy — **team/project → programme architecture forum → departmental architecture board → Technical Design Council (cross-department)** — and an escalation rule: *"determine the scope of the decision and identify the appropriate decision-making level"* ([GOV.UK ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)). AWS and others echo team-level/domain-level/organization-level ADRs ([AWS best-practices blog](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/); [Azure WAF](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)).
- **Gap / inference (P-022):** No external source I found prescribes the **concrete mechanic** of *remapping an ADR's ID and back-linking the original when it is physically promoted up a scope level*. External sources give the *pieces* (scope hierarchy + immutability + supersede-links); the "renumber-on-promotion + bidirectional promoted-from/promoted-to link" recipe in L2 is **my synthesis**, grounded in those pieces plus Jerry's own already-observed `docs/design/` promotions.

### (e) Superseding / deprecation

- **Source-verified fact — immutability + supersede-not-edit:** *"When the team accepts an ADR, it becomes immutable… the team proposes a new ADR… it supersedes the previous ADR"*; *"treat ADRs as immutable… Changes… require creating a new ADR… change the state of the old ADR to Superseded"* ([AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)). Nygard: keep the superseded file, mark it, never reuse numbers ([Fowler](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)).
- **Source-verified fact — bidirectional links + amend vs supersede:** adr-tools `adr new -s 9 "…"` creates a new ADR flagged as superseding ADR 9 and flips ADR 9's status to superseded, maintaining links both ways; `-l "5:Amends:Amended by"` records an **amend** relationship distinct from supersede ([npryce/adr-tools](https://github.com/npryce/adr-tools)). MADR status vocabulary: `proposed | rejected | accepted | deprecated | superseded by ADR-0123` ([MADR](https://adr.github.io/madr/)).

---

## L2: Recommendation for Jerry

All items below are **MEDIUM-tier (SHOULD / RECOMMENDED)**. No new HARD (H-NN) rule is proposed (rationale in [Tiering](#tiering-rationale-medium-not-hard)).

### (a) ID scheme — scope-keyed, collision-free, accommodates existing framework ADRs

Adopt a **two-namespace model keyed on decision scope**, codifying existing good practice:

| Scope | ID pattern | Sequence domain | Filename (ID + slug) | Rationale / evidence |
|---|---|---|---|---|
| **Framework** (governs rules/, agents, routing, enforcement, cross-project standards) | `ADR-{domain-slug}-NNN` | Per domain slug | `ADR-agent-design-001-…md` | **Zero migration** — the 3 `docs/design/` ADRs already comply. Matches log4brains "slug as unique ID," JPH slug approach, BUG-006 Alternative 3 (best on discoverability/recognition/sortability). |
| **Project** (governs a single project) | `ADR-{PROJECT-ID}-NNN` | Per project | `ADR-PROJ031-001-…md` | Already the dominant, collision-free pattern (PROJ010/022/031). Project ID is globally unique → no cross-project collision (the core requirement). PROJ-031 already migrated to it. |
| **Entity-embedded** (optional; ADR physically inside a work/EPIC/STORY folder) | `ADR-{ENTITY-ID}-NNN` | Per entity | `ADR-STORY015-001-…md` | Permitted **only** when co-located with the owning entity (as STORY-015 is). Otherwise default to project-ID scope to avoid BUG-006's "opaque entity ID" problem. |

Rules of the scheme:
- **Deprecate bare `ADR-NNN` for all *new* ADRs** — it is the sole collision source (Log4brains-documented failure mode).
- **`NNN` = 3-digit, zero-padded, monotonic within its scope**, never reused (Nygard; Jerry's tombstone precedent).
- **Separator = hyphen everywhere**; the slug is retained after the ID (recognition — BUG-006 F-003; Nygard "name that captures the decision").
- Keep worktracker `DEC-NNN` decision files distinct — this standard governs ADRs only.

### (b) Canonical location model

| Scope | Canonical home | ID form | State |
|---|---|---|---|
| Framework | `docs/design/` | `ADR-{domain-slug}-NNN` | Active |
| Project | `projects/PROJ-NNN-*/decisions/` | `ADR-PROJ{NNN}-NNN` | Active |
| Entity-embedded (optional) | `projects/.../work/.../{ENTITY}/` | `ADR-{ENTITY-ID}-NNN` | Active |
| Legacy (transcript) | `docs/adrs/` | `ADR-NNN` | **Frozen** — do not extend |
| Archived | `docs/archive/.../decisions/` | `ADR-0NN` | **Frozen** |
| Orchestration drafts | `projects/*/orchestration/.../` | `ADR-OSS-NNN`, `adr-*`, etc. | **Transient** — not canonical until promoted into a `decisions/` home |

- **Do not introduce `docs/decisions/`.** It would be a third framework home; instead **fix the template's dangling reference** to point at the two real homes.
- **Recommended (low-effort) win:** add `docs/design/README.md` as a framework-ADR index (BUG-006 F-004, never implemented) and a short `docs/adrs/README.md` banner marking that set as frozen transcript-scoped legacy.

### (c) Promotion process (project → framework) — codify what already happens

Grounded in GOV.UK scope-determination + AWS/Nygard immutability + adr-tools link mechanic; mirrors Jerry's already-observed `docs/design/` promotions (**the ID-remap+backlink specifics are synthesis, P-022**):

1. **Determine scope.** Promote only when the decision governs the framework broadly (rules/, agents, routing, enforcement, cross-project standards) — GOV.UK "identify the appropriate level."
2. **Create a new framework ADR** in `docs/design/` with a `ADR-{domain-slug}-NNN` ID. **Do not mutate the original** (AWS immutability).
3. **Remap ID, preserve provenance.** Record origin in frontmatter (`origin_project`, `origin_entity`, `origin_adr`) — exactly what today's `docs/design/` ADRs already do informally via PS-ID comments.
4. **Bidirectional back-link.** Original project ADR: `Status: Superseded` + `Promoted-To: ADR-{domain-slug}-NNN`. Framework ADR: `Promoted-From: ADR-PROJ{NNN}-NNN (path)`. Reuse the template's existing `Supersedes/Superseded By` fields and add a `PROMOTED_FROM/PROMOTED_TO` relationship type to the Related-Decisions vocabulary.
5. **Re-point citations** in rule files to the new framework ID.

### (d) Superseding / deprecation conventions

- **Immutability:** accepted ADRs are immutable; reverse a decision by **creating a new superseding ADR**, never by editing or renumbering the old one (AWS; Nygard).
- **Bidirectional status links:** `Supersedes:` / `Superseded By:` (template already has both) — adopt adr-tools' two-way linking semantics.
- **Amend vs supersede (formalize the two observed styles):** *minor clarification* → dated in-body `AMENDED YYYY-MM-DD` block (PROJ-031 practice) with an `Amended-By/Amends` link; *decision reversal* → new superseding ADR. This maps directly onto adr-tools' `-l "…:Amends:Amended by"` vs `-s` distinction.
- **Status vocabulary:** `PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED` (add `REJECTED` per MADR/AWS; keep the rest).

### (e) Template tie-in (updates to specify — do NOT edit as part of this research)

- `docs/knowledge/exemplars/templates/adr.md`: change the title placeholder `ADR-{NUMBER}` → **`ADR-{SCOPE}-{NNN}`** with a note defining `{SCOPE}` ∈ {domain-slug (framework) | PROJECT-ID (project) | ENTITY-ID (entity-embedded)}; add provenance frontmatter (`origin_project`/`origin_entity`) and the `PROMOTED_FROM/PROMOTED_TO` relationship; fix the PS-Integration `docs/decisions/…` path to the two real homes.
- `skills/architecture/SKILL.md`: fix the `ADR_NNN` **underscore→hyphen** mismatch and the `docs/design/ADR_NNN_*.md` pattern; align its inline example header with the scope-keyed scheme.

### Tiering rationale (MEDIUM, not HARD)

- **Ceiling:** HARD rules are at **25/25 with zero headroom**; a new HARD rule would require a C4-reviewed ADR + a ceiling *exception* (max +3, one concurrent, 3-month reversion) per `quality-enforcement.md` — disproportionate for a naming convention.
- **Nature of the rule:** ID/location consistency is a **discoverability/consistency** standard, not a safety invariant → fits the MEDIUM tier vocabulary (SHOULD/RECOMMENDED, override with documented justification), like the analogous `AD-M-011` output-path standard.
- **Enforcement without a HARD rule:** deterministic **L5 CI lint** (reject a *new* bare `ADR-NNN` outside frozen legacy dirs; assert ID prefix matches location) + L4 advisory. Home it in a new `.context/rules/adr-standards.md` (or an `architecture-standards.md` section) with `AD-M-###`-style IDs; register per H-26.

### Migration cost (no big-bang renumber)

| Set | Action | Cost |
|---|---|---|
| 3 framework ADRs (`docs/design/`) | None — already domain-slug compliant | **Zero** |
| Scoped project families (PROJ010×6, PROJ022×2, PROJ031×3, EPIC002×2, STORY015×1, 150×1) | Keep as-is — already collision-free | **Zero/trivial** |
| PROJ-031 bare set | **Already migrated** to `ADR-PROJ031-NNN` (observed this session) | **Done** |
| PROJ-014 bare `ADR-001..004` (orchestration artifacts) | Low priority; rename to `ADR-PROJ014-NNN` only if promoted into a `decisions/` home | **Low** |
| Legacy `docs/adrs/` (transcript ADR-001..006 + amendment) & archived `ADR-031..034` | **Freeze**; add scope banner/README; do **not** renumber | **Minimal** (renumbering would break inbound refs — apply the tombstone principle) |

**Net:** adopt-forward for new ADRs, freeze legacy, codify the already-happening promotion. The only residual collision (frozen transcript `docs/adrs/` vs transient PROJ-014 orchestration drafts) is between a frozen set and non-canonical artifacts — acceptable and documented, not worth a disruptive renumber.

---

## P-022 Disclosures (Corrections, Inference, Gaps)

- **BUG-006 factual error — corrected.** BUG-006's finding F-002 claims `ADR-EPIC002-001` "exists in two different projects: PROJ-022 … and PROJ-004." **This is false.** Filesystem verification: `ADR-EPIC002-001/002` exist **only** in `PROJ-001-oss-release/decisions/`; PROJ-022 uses `ADR-PROJ022-*`; no PROJ-004 ADR-EPIC002 exists. The real, verifiable collision is in the **bare `ADR-NNN`** namespace (docs/adrs + PROJ-014, formerly PROJ-031). My recommendation is built on the verified collision, not BUG-006's example.
- **BUG-006 second inaccuracy.** BUG-006 asserts the convention is "documented in `quality-enforcement.md`." It is not — that file only *cites* `ADR-EPIC002-001` as a reference; it defines no ADR naming convention.
- **Inference vs fact.** The scope hierarchy (GOV.UK), immutability/supersede (AWS/Nygard), bidirectional/amend links (adr-tools), and slug-as-ID (log4brains/JPH) are **source-verified**. The specific **promotion recipe (ID remap + `PROMOTED_FROM/TO` back-link)** and the **two-namespace scope-keyed scheme** are **my synthesis** of those sources plus Jerry's observed practice — labeled as such.
- **Gaps where WebSearch yielded nothing.** No external source prescribes a concrete "renumber-and-backlink on promotion" mechanic (only the constituent parts). No external standard mandates a multi-project numbering rule — the ecosystem splits between global-sequence-plus-labels and per-project-directory. These gaps are stated rather than filled with fabrication.
- **Live-state caveat.** PROJ-031's bare→scoped rename occurred **during** this session; I report the current definitive state (`ADR-PROJ031-NNN`) and the earlier bare state I observed, without asserting who performed the rename.

---

## References

1. [Martin Fowler — bliki: Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html) — Nygard sequential/monotonic numbering, never reuse, keep+mark superseded, `doc/arch/adr-NNN.md`.
2. [Michael Nygard — Documenting Architecture Decisions (Cognitect, 2011)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — original ADR concept and format.
3. [MADR — About MADR](https://adr.github.io/madr/) — `docs/decisions` location; `NNNN-title-with-dashes.md`; status incl. `superseded by ADR-0123`.
4. [adr/madr (GitHub)](https://github.com/adr/madr) — MADR spec and templates.
5. [ADR GitHub organization](https://adr.github.io/) — ADR templates hub.
6. [npryce/adr-tools (GitHub)](https://github.com/npryce/adr-tools) — `-s` supersede (bidirectional status/link), `-l` amend relationship, auto monotonic numbering.
7. [Joel Parker Henderson — architecture-decision-record (GitHub)](https://github.com/joelparkerhenderson/architecture-decision-record) — name/slug-based IDs, `adr/` dir, supersede-by-new; silent on multi-team/promotion (verified via fetch).
8. [Log4brains — "Use the ADR slug as its unique ID" (ADR 20201016)](https://thomvaill.github.io/log4brains/adr/adr/20201016-use-the-adr-slug-as-its-unique-id/) — explicit slug-as-ID decision; number→date change to avoid merge conflicts.
9. [thomvaill/log4brains (GitHub)](https://github.com/thomvaill/log4brains) — store ADRs next to source; monorepo/multi-package usage.
10. [GOV.UK — Architectural Decision Record Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework) — team→programme→departmental board→TDC scope hierarchy and escalation/promotion.
11. [AWS Prescriptive Guidance — ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) — immutability; supersede-not-edit; Proposed/Accepted/Rejected/Superseded lifecycle.
12. [AWS Architecture Blog — Master ADRs: best practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/) — multi-level ADRs.
13. [SimplerGrants — Repo organization ADR](https://wiki.simpler.grants.gov/product/decisions/adr/2025-01-02-repo-organization) — labels to scope decisions per service in a monorepo.
14. [Microsoft Azure Well-Architected — Maintain an ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record) — corroborates immutability/lifecycle.

Internal artifacts cited (filesystem-verified): `docs/knowledge/exemplars/templates/adr.md`; `skills/architecture/SKILL.md`; `PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md`; `docs/design/ADR-{agent-design,routing-triggers,output-path-resolution}-001.md`; `docs/adrs/ADR-001..006`; `docs/archive/projects-archive/decisions/ADR-031..034`; `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-001..003-*`; `.context/rules/quality-enforcement.md` (HARD ceiling 25/25; Retired-Rule-ID tombstone); `skills/worktracker/rules/worktracker-directory-structure.md` (`DEC-NNN`).

---

### Handoff Summary (for orchestrator)

- **key_findings:**
  1. No documented ADR ID/location/promotion/superseding standard exists anywhere in the repo (11 locations checked) — preliminary finding CONFIRMED.
  2. Bare `ADR-NNN` collides across scopes (verified); all scope-prefixed families are collision-free; PROJ-031 was migrated bare→`ADR-PROJ031-NNN` mid-session.
  3. The 3 `docs/design/` framework ADRs already use domain-slug IDs and already show de-facto promotion from project scope — recommendation codifies existing practice (near-zero migration).
  4. External consensus: sequential-number school (Nygard/MADR/adr-tools) vs slug-as-ID school (log4brains/JPH); immutability+supersede-links (AWS/Nygard/adr-tools); scope hierarchy+escalation (GOV.UK). No external source prescribes the exact promotion ID-remap mechanic (synthesis, disclosed).
  5. BUG-006's central collision example (ADR-EPIC002-001 in PROJ-022/PROJ-004) is factually wrong — corrected.
- **recommendation:** MEDIUM-tier two-namespace scheme — framework `ADR-{domain-slug}-NNN` in `docs/design/`; project `ADR-{PROJECT-ID}-NNN` in `projects/*/decisions/`; freeze legacy; L5 CI lint enforcement; no new HARD rule (ceiling 25/25).
- **confidence:** 0.9 (internal filesystem-verified; external multi-source-cited; promotion mechanic labeled as synthesis).
- **open_questions:** Home the new standard in a new `.context/rules/adr-standards.md` vs a section in `architecture-standards.md`? Re-home `ADR-EPIC002-*` under a project-ID (optional, collision-free already)? Create `docs/design/README.md` index now?
- **next_agent_hint:** ps-architect to produce the MEDIUM-tier standard + template/SKILL.md update spec as a PROJ-031 ADR (`ADR-PROJ031-NNN`), then `/adversary` review.

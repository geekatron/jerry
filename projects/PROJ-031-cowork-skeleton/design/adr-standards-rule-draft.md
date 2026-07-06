# DRAFT — Proposed `.context/rules/adr-standards.md`

> **REVIEW DRAFT of a ratified convention.** Proposed content of `.context/rules/adr-standards.md`, companion to `ADR-PROJ031-004` (canonical `ADR-adr-convention-001`). Scheme B was **ratified 2026-07-05** (FEEDBACK-LOG FU.0). On the M-2 move this content — minus this wrapper — becomes `.context/rules/adr-standards.md` and auto-loads via the `.claude/rules -> ../.context/rules` directory symlink. **Tier:** MEDIUM only (SHOULD/RECOMMENDED, override with justification; dialect-permission is SOFT `MAY`); no HARD rule (ceiling 25/25). `ADR-M-###` IDs are internal, never filenames.

---

# ADR Standards

> Conventions for Architecture Decision Record (ADR) identifiers, location, promotion, superseding, and amendment. MEDIUM-tier: SHOULD/RECOMMENDED, override with documented justification. Enforced by a small deterministic L5 CI lint (5 rules), not a HARD invariant.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Tier and Scope](#tier-and-scope) | What this governs and how strongly |
| [MEDIUM Standards](#medium-standards) | ADR-M-001 … ADR-M-013 |
| [ID Scheme](#id-scheme) | Canonical, dialect, deprecated, frozen grammars |
| [Canonical Location Model](#canonical-location-model) | Where each scope lives |
| [Frozen and Grandfathered Legacy](#frozen-and-grandfathered-legacy) | Do-not-extend vs valid-in-place |
| [Frontmatter Schema](#frontmatter-schema) | Provenance and relationship fields |
| [Promotion Process](#promotion-process) | Project → framework, both paths |
| [Supersede and Amend](#supersede-and-amend) | Which mechanism, when |
| [Status Vocabulary](#status-vocabulary) | Permitted lifecycle states |
| [L5 CI Lint Specification](#l5-ci-lint-specification) | The 5 deterministic checks |
| [Relationship to Worktracker DEC-NNN](#relationship-to-worktracker-dec-nnn) | Non-conflation |
| [Producer Fixes](#producer-fixes) | Template, SKILL, and agent edits |
| [References](#references) | Source traceability |
| [Changelog](#changelog) | Version history |

---

## Tier and Scope

Governs **ADRs only** — records under `docs/design/`, `projects/*/decisions/`, and the frozen legacy sets. Does **not** govern the worktracker `DEC-NNN` Decision-File entity (see [Relationship to Worktracker DEC-NNN](#relationship-to-worktracker-dec-nnn)).

All standards are **MEDIUM-tier** (SHOULD/RECOMMENDED, override with documented justification per `.context/rules/quality-enforcement.md` Tier Vocabulary). Rationale for MEDIUM: ID/location consistency is a discoverability standard, not a safety invariant, and the HARD ceiling is at 25/25.

**Enforcement story — guidance first, minimal lint second.** The guidance below delivers value with **zero tooling** — an author can follow it today. The 5-rule lint ([below](#l5-ci-lint-specification)) is a designed-not-built enhancement, not a precondition for the convention's value.

---

## MEDIUM Standards

| ID | Standard |
|----|----------|
| **ADR-M-001** | New ADRs SHOULD use **subject-encoded identity** `ADR-{domain-slug}-NNN`, `{domain-slug}` naming the subject in kebab-case, `NNN` a 3-digit per-slug sequence, never reused. Origin is a birth fact, not an identity. |
| **ADR-M-002** | ADR origin SHOULD be recorded in **frontmatter** (`origin_project`, optional `origin_entity`), never in the identifier. |
| **ADR-M-003** | A tactical, project-local ADR the author judges *with positive certainty* will never promote **MAY** use the dialect `ADR-{PREFIX}-NNN`, `{PREFIX}` from the closed set `{PROJ\|EPIC\|FEAT\|STORY}\d{3}`. Under any uncertainty the default SHOULD be the canonical slug (scope-agnostic: free to keep, free to `git mv`). A framework-wide ADR SHOULD NOT use the dialect. (`MAY` = SOFT permission.) |
| **ADR-M-004** | New ADRs SHOULD NOT use bare `ADR-NNN`. Bare numbering is the documented collision source and is DEPRECATED. |
| **ADR-M-005** | `NNN` SHOULD be 3-digit, zero-padded, monotonic within its namespace, never reused — reversal is by supersession, not renumbering. |
| **ADR-M-006** | The separator SHOULD be a hyphen; underscores (`ADR_NNN`) SHOULD NOT be used. A `title-slug` tail MAY follow the ID. |
| **ADR-M-007** | A framework-governing ADR SHOULD live in `docs/design/`; a project ADR in `projects/PROJ-NNN-*/decisions/`. Scope is expressed by **location** (may change); identity SHOULD NOT change when location changes. |
| **ADR-M-008** | Promotion of a canonical ADR SHOULD be a pure `git mv`, no identifier change (Path 1). Only a dialect ADR SHOULD incur a rename + tombstone (Path 2). |
| **ADR-M-009** | Accepted ADRs SHOULD be treated as immutable. A minor clarification SHOULD use a dated in-body `AMENDED YYYY-MM-DD` block; a reversal SHOULD be a new superseding ADR. Separate-amendment-file style SHOULD NOT be used. |
| **ADR-M-010** | ADR status SHOULD be drawn from `PROPOSED \| ACCEPTED \| REJECTED \| DEPRECATED \| SUPERSEDED`; new ADRs default to `PROPOSED`. |
| **ADR-M-011** | ADRs are the one Jerry class whose identifier encodes **subject, not scope**, because they are the one class whose **scope is mutable**. State this ontology exception wherever ADR conventions are taught. |
| **ADR-M-012** | Legacy/archived and existing scope-prefixed project ADRs SHOULD be grandfathered in place; SHOULD NOT be renumbered in a big-bang migration. |
| **ADR-M-013** | Every new ADR SHOULD declare `scope` (`framework \| project`) in frontmatter at authoring time. When uncertain, default to `scope: project` with a **canonical domain-slug identity** (promotes for free), NOT the dialect. |

---

## ID Scheme

- **Canonical** (RECOMMENDED, all scopes): `ADR-{domain-slug}-NNN-{title-slug}.md`, e.g. `ADR-agent-design-001-canonical-format.md`.
- **Dialect** (permitted, project-local only): `ADR-{PROJ\|EPIC\|FEAT\|STORY}NNN-NNN-{title-slug}.md`, e.g. `ADR-PROJ031-005-foo.md`.
- **Deprecated**: bare `ADR-NNN-{slug}.md` (rejected by lint outside frozen dirs). **Frozen**: `ADR-NNN`/`ADR-0NN` in `docs/adrs/`, `docs/archive/` (do not extend).

A filename PASSES if it matches **canonical OR dialect** (a lowercase-only regex would wrongly reject grandfathered uppercase dialect ADRs):

- **Canonical:** `^ADR-[a-z][a-z0-9]*(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$` — leading slug token MUST begin with a letter (so `ADR-150-001` is not a canonical slug; grandfathered).
- **Dialect:** `^ADR-(PROJ|EPIC|FEAT|STORY)\d{3}-\d{3}(-[a-z0-9-]+)?\.md$` — closed prefix set, matching ADR-M-003. Bare-detection: `^ADR-\d`.

---

## Canonical Location Model

| Scope | Canonical home | ID form | State |
|---|---|---|---|
| Framework | `docs/design/` | `ADR-{domain-slug}-NNN` | Active |
| Project (recommended) | `projects/PROJ-NNN-*/decisions/` | `ADR-{domain-slug}-NNN` | Active |
| Repository-based project (alt topology) | `{RepositoryRoot}/decisions/` | `ADR-{domain-slug}-NNN` | Active |
| Project (permitted dialect) | `projects/PROJ-NNN-*/decisions/` | `ADR-PROJ{NNN}-NNN` | Active (dialect) |
| Entity-embedded (permitted) | `projects/.../work/.../{ENTITY}/` | `ADR-{PROJ\|EPIC\|FEAT\|STORY}NNN-NNN` | Active (dialect) |
| Legacy (transcript) | `docs/adrs/` | `ADR-NNN` | Frozen |
| Archived | `docs/archive/.../decisions/` | `ADR-0NN` | Frozen |
| Orchestration drafts | `projects/*/orchestration/.../` | `ADR-OSS-NNN`, `adr-*` | Transient (non-canonical) |

The worktracker SSOT defines two `ONE-OF` topologies (project-based and repository-based). The canonical domain-slug form is **topology-agnostic**; the dialect presumes the project-based tree and SHOULD NOT be used in repository-based repos. `docs/decisions/` SHOULD NOT be introduced (a MADR name inherited by accident). RECOMMENDED: add `docs/design/README.md` (framework index) and `docs/adrs/README.md` (frozen banner).

---

## Frozen and Grandfathered Legacy

**Frozen** sets (`docs/adrs/`, `docs/archive/`) are closed to new entries. **Grandfathered** dialect families (`PROJ010`×6/`PROJ022`×2/`PROJ031`×4/`EPIC002`×2/`STORY015`×1/`150`×1) and PROJ-014 drafts remain valid in place, extendable within their dialect; re-slug only if promoted. The 16-file dialect corpus + 3 canonical `docs/design/` ADRs (19 total) must all pass the lint's grandfather regression test before it ships.

---

## Frontmatter Schema

```yaml
---
id: ADR-plugin-distribution-001     # canonical subject identity (ADR-M-001)
type: adr
status: PROPOSED                     # ADR-M-010
scope: framework                     # framework | project (ADR-M-007/M-013)
origin_project: PROJ-031             # birth project — immutable (ADR-M-002)
origin_entity: EPIC-003              # optional finer origin
created: 2026-07-05
supersedes: []
superseded_by: null
amends: null
amended_by: []
promoted_from: null                  # set on Path-2 promotion
promoted_to: null
canonical_id: null                   # OPTIONAL advisory (a dialect ADR MAY declare its Path-2 destination)
---
```

The lint parses this YAML `---` block (distinct from `jerry ast frontmatter`, which parses blockquote frontmatter; both coexist). `canonical_id` is advisory-only.

---

## Promotion Process

Elevates a project decision to framework scope. Two paths plus a Path-0 graduation.

**Path 0 — Draft → canonical home:** a transient-location draft (`orchestration/*/explore/`, `ADR-OSS-NNN`/`adr-*`) is non-canonical until moved. Assign the canonical (or dialect) identity, `git mv` into a `decisions/`/`docs/design/` home, add frontmatter, set `status`. No tombstone.

**Path 1 — Canonical ADR (default, zero-churn):** `git mv` to `docs/design/`, **identifier and `title-slug` unchanged**; set `scope: framework`. Bare-ID citations need no re-pointing (the majority); full-path citations move with the file (minority — see [descoped note](#l5-ci-lint-specification)).

**Path 2 — Dialect ADR (discouraged, rename + tombstone):** choose a domain slug + next `NNN`; author the framework ADR in `docs/design/` (do not mutate the original body). Set `promoted_from`; bidirectional back-link (original → `SUPERSEDED` + `promoted_to`; framework → `promoted_from`). Re-point `grep -rl "ADR-PROJ{NNN}-NNN"` **in live documents only** (exclude CHANGELOGs, commit messages, release notes); optionally sweep GitHub Issues — the lint does not scan them.

A `DEC-NNN` is never renamed into an ADR; author a new ADR and cross-link.

**AE-004 scoping.** A Path-1 promotion changes only **location** + the `scope` field (immutable body) — a governed lifecycle move at the **C3** floor; it does not trip AE-004's C4. A **Path-2 promotion flips a baselined ADR's `status` to `SUPERSEDED`** — a supersession-class change to a baselined ADR, so it **IS subject to AE-004 auto-C4**, as is any edit changing a baselined ADR's decision content.

---

## Supersede and Amend

| Situation | Mechanism | Identity | Status | Links |
|---|---|---|---|---|
| Minor clarification (decision unchanged) | In-body dated `**AMENDED YYYY-MM-DD:**` block | Same ID | Stays `ACCEPTED` | `amends`/`amended_by` |
| Decision reversal / replacement | New superseding ADR; never edit old body | New ID | Old → `SUPERSEDED`; new → `ACCEPTED` | `superseded_by` ↔ `supersedes` |
| Scope elevation | Promotion (Path 1/2) | Path 1: unchanged; Path 2: new slug | Path 2 old → `SUPERSEDED` | `promoted_from`/`promoted_to` |

An amendment SHOULD NOT change an ADR's `scope`, `origin_project`/`origin_entity`, or location — those transitions belong to the Promotion Process, and origin is an immutable birth fact.

**Honest limit ([INHERENT]).** No rule in the minimal core detects an **in-place frontmatter mutation** of an unmoved file (e.g. editing `scope:` as a "minor clarification"): nothing moves, no ID changes, no citation goes stale, so there is nothing structural to catch. This boundary rests on SHOULD-NOT guidance and immutability discipline, not on a lint — stated plainly rather than backed by a mechanism that cannot see the violation.

---

## Status Vocabulary

`PROPOSED` (not in force; default) · `ACCEPTED` (in effect) · `REJECTED` (declined) · `DEPRECATED` (no longer applies, no specific successor) · `SUPERSEDED` (replaced by a specific newer ADR; also terminal after Path-2).

Transitions: `PROPOSED`→`ACCEPTED`/`REJECTED`; `ACCEPTED`→`SUPERSEDED`/`DEPRECATED`; `REJECTED`→`PROPOSED`. Terminal states do not transition further (a revived decision is a new ADR). `DEPRECATED` has no forward-link by design — a specific replacement uses `SUPERSEDED`.

---

## L5 CI Lint Specification

> **Claim-Status: DESIGNED, NOT BUILT.** As of 2026-07-05, `scripts/lint_adr_convention.py` does not exist (Glob-verified). Until it ships with a green grandfather regression test wired into CI (Migration-Plan M-6), **enforcement is advisory-only** and the guidance stands on its own — following the [Claim-Status Convention](../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md#claim-status-convention-p-022--foundational) precedent (designed-but-unvalidated controls are labeled, never asserted as achieved).

Deterministic, zero-token, run via `uv run` in CI. **MEDIUM-tier override:** a FAIL is overridable with a documented justification in the PR description (the standard MEDIUM mechanism) — no waiver ledger, no CODEOWNERS gate, no "non-bypassable" rule. The collision/grammar rules are rarely overridden because a compliant `NNN`/slug is always available.

**The 5-rule core (all FAIL, all overridable-with-justification):**

| Rule | Checks (git-added/modified files; pre-adoption grandfathered) |
|---|---|
| **L-1 Grammar** | Filename matches canonical OR dialect ([ID Scheme](#id-scheme)) — rejects malformed IDs and entity-prefix look-alikes masquerading as domain slugs. `projects/*/decisions/`, `docs/design/`. |
| **L-2 No new bare** | A git-added file must not match `^ADR-\d`, anywhere except frozen dirs (`docs/adrs/`, `docs/archive/`). |
| **L-3 No duplicate ID** | Extract `{slug}-NNN` of all non-frozen ADRs; `sort \| uniq -d` must be empty. Repo-wide. |
| **L-4 ID↔location** | A `PROJ{NNN}`/`EPIC{NNN}`/`STORY{NNN}` dialect prefix matches its containing project/entity dir (project-based topology). |
| **L-7 Relationship target resolves** | `superseded_by`/`promoted_to`/`promoted_from` targets resolve to an existing ADR — catches a half-completed Path-2 orphaning the source. Repo-wide. |

A **grandfather regression test** must be green before the lint ships: all 16 live dialect files and the 3 canonical framework ADRs pass L-1 — the dry-run-against-the-real-corpus step whose absence caused an earlier lowercase-only defect.

**Pre-flight collision check (runnable today, zero tooling)** — exactly what L-3 runs in CI:

```bash
find projects docs/design -path '*/decisions/*' -name 'ADR-*.md' \
  -not -path '*/docs/adrs/*' -not -path '*/docs/archive/*' \
  | sed -E 's#.*/(ADR-.*)\.md#\1#' \
  | grep -E '^ADR-[a-z0-9-]+-[0-9]{3}' \
  | sed -E 's/^(ADR-[a-z0-9-]+-[0-9]{3}).*/\1/' \
  | sort | uniq -d
# Empty = no collision. Any line = a duplicate identity to resolve before commit.
```

**Descoped, honestly (not phased, not committed).** Left out of the minimal core to keep it buildable by a solo maintainer and free of overclaimed coverage: provenance/framework-home WARNs, provenance-correctness checks, **repo-wide free-text citation scanning** (incl. GitHub Issues, full-path citations, config), taxonomy-synonymy matching, producer-drift monitoring, supersession separation-of-duties, repository-topology dialect rejection. The citation-scan omission is an **[INHERENT] residual** — the core detects only structural frontmatter links; Path-1's ID-stable move avoids the churn for the bare-ID majority, and a manual `grep`/`gh issue list` sweep is the fallback. None is promised for a later release; a future amendment MAY add a single targeted rule if a gap causes real pain.

---

## Relationship to Worktracker DEC-NNN

The worktracker `DEC-NNN` "Decision File" entity is distinct: permanently parent-scoped, never migrates, correctly scope-prefixed. A `DEC-NNN` SHOULD NOT be renamed into an ADR; architectural decisions SHOULD be authored as ADRs and cross-linked. The lint keys strictly on the `ADR-` filename prefix, so a co-located `DEC-*` file is not linted as an ADR.

---

## Producer Fixes

One-time edits on ratification (parent ADR M-3/M-4/M-12); **not applied by this draft (P-020)**. Until applied, the producing agent emits non-canonical IDs — a **designed-not-built residual**, disclosed, not gated behind machinery.

- **`docs/knowledge/exemplars/templates/adr.md`:** title `# ADR-{NUMBER}` → `# ADR-{DOMAIN-SLUG}-{NNN}`; add `REJECTED`; add the YAML frontmatter block; dangling `docs/decisions/` path → real home.
- **`skills/architecture/SKILL.md`:** `ADR_NNN` → `ADR-{domain-slug}-NNN`; output location project-first or framework, not hardcoded.
- **`skills/problem-solving/agents/ps-architect.md` (Fix 3):** title and output grammar → canonical `ADR-{domain-slug}-{NNN}-*.md` (PS linkage → frontmatter); phantom `templates/adr.md`/`python3 scripts/cli.py` → real path and `uv run jerry` (H-05); default the authored ID to the canonical slug.

Also (parent ADR M-14): document `decisions/` (both topologies) in the worktracker scaffold SSOT.

---

## References

| Source | Content |
|--------|---------|
| `ADR-PROJ031-004` (canonical `ADR-adr-convention-001`) | Parent decision, rationale, sensitivity analysis, migration plan |
| `.context/rules/quality-enforcement.md` | Tier vocabulary; HARD ceiling 25/25 → MEDIUM mandate |
| `ADR-PROJ031-003` | Claim-Status Convention precedent (designed-but-not-built labeling) |
| `skills/worktracker/rules/worktracker-directory-structure.md` | `DEC-NNN` entity (non-conflation); two topologies |
| `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` (FU.0) | Scheme B ratification, 2026-07-05 |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0–1.5 | 2026-07-02 | Iterative adversarial remediation (see parent ADR Changelog 1.0–1.6 and `adversary/iteration-00N/` for the full trail). |
| **1.7** | **2026-07-05** | **Ratification fold-in + subtraction pass (FU.1).** Scheme B ratified (FU.0); review-draft framing → ratified. Lint cut 18→**5 rules** (L-1/L-2/L-3/L-4/L-7). **Deleted outright:** waiver ledger, two-tier ratification, all CODEOWNERS-dependent and "non-bypassable" language, 13 lower-value rules. Override reverts to the standard MEDIUM documented-justification path; `PERMITTED` pseudo-tier removed; dialect permission is SOFT `MAY`. Descoped items in one honest note; citation-staleness and in-place amendment mutation disclosed as [INHERENT] residuals; AE-004 Path-2 scoping explicit; token budget ~10.3k→~2.5k. Disposition: `../orchestration/adr-convention-20260702-001/subtraction-pass-notes.md`. |

*Proposed home on ratification: `.context/rules/adr-standards.md` · Tier: MEDIUM only · No HARD rule added.*

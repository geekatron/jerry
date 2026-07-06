# Red Team Report: ADR Identifier, Location, and Promotion Convention (PROJ-031, iteration 3)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata and H-16 compliance |
| [Summary](#summary) | Overall assessment and recommendation |
| [Threat Actor Profile](#threat-actor-profile) | Adversary goal, capability, motivation |
| [Findings Table](#findings-table) | All RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Notes](#execution-notes) | Protocol compliance record |

---

## Header

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (canonical `ADR-adr-convention-001`) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-001, blind, iteration 3)
**H-16 Compliance:** Confirmed by file-existence check only (Glob), **not by reading content**, per the BLIND PROTOCOL prohibition on reading other reviewers' findings: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-003/s-003-findings.md` exists on disk (also present for iteration-001 and iteration-002). This satisfies the S-001 template's Step-1 gate ("if no S-003 Steelman output exists, STOP and flag H-16 violation") without violating tournament blindness.
**Threat Actor:** See [Threat Actor Profile](#threat-actor-profile).

---

## Summary

This is iteration 3 of a document that has already absorbed two full remediation cycles (v1.0 -> v1.1 -> v1.2 per the ADR's own Changelog), so this Red Team pass deliberately targets **second-order gaps in the prior remediations** rather than re-litigating closed findings. Two **Critical** and three **Major** attack vectors were found, all with direct textual evidence, none requiring speculative reach: (1) the newly-engineered "structured waiver" override model is fully bypassable via a parallel, unguarded artifact (`scripts/adr-grandfather-allowlist.txt`) that carries none of the waiver ledger's review/audit protections; (2) the taxonomy-synonymy defense (L-10) is explicitly scoped to the framework registry only, leaving the numerically dominant "project-scoped canonical" ADR population with zero near-duplicate-slug protection despite that population being the RECOMMENDED default; (3) the case-folded dialect-lookalike ban enumerates only `{proj|epic|feat|story}`, omitting `bug`/`task`/`spike`/`enabler` -- all real Jerry worktracker entity-ID prefixes -- so an origin-scoped ID can still masquerade as a subject-encoded slug; (4) waiver `expires` dates have no described automatic re-enforcement; (5) the override model's own integrity checks (append-only ledger diff, API-verified second reviewer) are never assigned an L-N rule ID and are excluded from the M-6 gating regression test that verifies everything else. **Recommendation: REVISE.** None of these invalidate the scheme's core subject-vs-origin argument, but two of them (RT-001, RT-002) directly defeat the enforcement mechanism the document relies on to make its collision-resistance and discoverability claims real, so they should be closed (or the claims qualified) before ratification.

---

## Threat Actor Profile

- **Goal:** Merge a colliding, misleading, or orphaning ADR identifier/citation into the repository while appearing (or being able to appear, under review) fully compliant with the new convention -- either to avoid governance friction, to bury/shadow an inconvenient existing decision, or (careless variant) to simply get an ADR merged fast without understanding the taxonomy.
- **Capability:** Full source access; can author files under `projects/*/decisions/` and `docs/design/`; can add entries to `scripts/adr-grandfather-allowlist.txt` and `scripts/adr-lint-waivers.yaml` in the same PR as the ADR itself; understands that enforcement is, by the document's own admission, `DESIGNED, NOT BUILT` as of 2026-07-02 (`ADR-PROJ031-004-adr-identifier-convention.md:554`; `adr-standards-rule-draft.md:187`).
- **Motivation:** Either malicious (deliberately shadow/orphan a decision, or evade review) or merely careless (misunderstands the closed dialect-prefix set, or copy-pastes a slug that collides). The convention must be robust to both, since MEDIUM tier means no HARD block is available as a backstop (c-001, `ADR-PROJ031-004-adr-identifier-convention.md:96`).

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|--------------------|
| RT-001-20260702i3 | Grandfather allowlist (`adr-grandfather-allowlist.txt`) has none of the waiver ledger's review/audit protections; adding an entry there silently defeats L-1/L-2/L-3 FAIL rules | Rule Circumvention | High | **Critical** | P0 | Missing | Methodological Rigor |
| RT-002-20260702i3 | L-10 taxonomy-synonymy check is scoped to the `docs/design/README.md` (framework) registry only; project-scoped canonical ADRs -- the RECOMMENDED default population -- have zero near-duplicate-slug defense | Ambiguity / Boundary | High | **Critical** | P0 | Missing | Completeness |
| RT-003-20260702i3 | L-1a's case-folded dialect-lookalike ban enumerates only `{proj\|epic\|feat\|story}`, omitting real worktracker entity prefixes `bug`/`task`/`spike`/`enabler`, letting an origin-scoped ID masquerade as a subject slug | Boundary Violation | Medium | Major | P1 | Partial | Internal Consistency |
| RT-004-20260702i3 | Waiver `expires` date has no described automatic re-check; an approved override silently continues to suppress a FAIL condition after expiry | Degradation Path | Medium | Major | P1 | Missing | Methodological Rigor |
| RT-005-20260702i3 | The override model's own integrity mechanisms (append-only ledger diff, API-verified second-reviewer check) carry no L-N rule ID and are excluded from the M-6 gating regression test | Dependency Attack | Medium | Major | P1 | Missing | Traceability |
| RT-006-20260702i3 | L-4 dialect-location check's behavior when `origin_entity` frontmatter is absent/null is unspecified, and L-6 (provenance) is WARN-only, not FAIL | Ambiguity Exploitation | Low | Minor | P2 | Partial | Internal Consistency |
| RT-007-20260702i3 | No lint checks title-slug truthfulness against decision content; a misleading title-slug tail can imply false authority/supersession with zero lint signal | Degradation Path | Low | Minor | P2 | Missing | Evidence Quality |

---

## Finding Details

### RT-001: Grandfather allowlist is an unguarded parallel bypass of the entire FAIL-rule model [CRITICAL]

**Attack Vector:** The document builds an elaborate, explicitly reasoned "structured, reviewable waiver" model for overriding any FAIL rule: a `scripts/adr-lint-waivers.yaml` entry requires six fields including `justification` (>=40 chars), `approved_by` cross-checked against the PR's **API-reported approving reviewers** (not a self-reported string), and an `expires` date, with the ledger itself "append-only... the lint fails on any non-append mutation" (`adr-standards-rule-draft.md:191-193`; identical text `ADR-PROJ031-004-adr-identifier-convention.md:577-579`). But a **second, entirely separate** exemption artifact exists with none of these protections: `scripts/adr-grandfather-allowlist.txt`. Both documents describe it only as holding "pre-adoption files, incl. the GH-issue singleton `ADR-150-001`" (`ADR-PROJ031-004-adr-identifier-convention.md:600`; `adr-standards-rule-draft.md:211,213`) and state that L-1/L-2/L-3 exempt files on this allowlist from re-validation. **Nowhere in either document is there a described mechanism that validates a new entry against actual pre-adoption git history, requires a second reviewer, requires a justification, is append-only-checked, or expires.** A contributor -- careless or hostile -- can add their own newly minted, colliding, or bare `ADR-NNN` filename to this text file in the *same* PR as the ADR itself, and per the stated exemption rule ("Frozen-dir allowlist... L-1/L-2/L-3 re-validation exempt"), CI would pass with zero of the review friction the waiver ledger was specifically engineered to guarantee.
**Category:** Rule Circumvention
**Exploitability:** High -- no code exists yet (Glob-verified absent: `scripts/adr-grandfather-allowlist.txt`, `scripts/lint_adr_convention.py` are not present in the repo as of 2026-07-02), so this is a specification-level gap, not a behavior of running code; but the *specification itself* provides an explicit, named exemption path with zero stated validation, meaning "add one text line" is a documented way to disable the FAIL rules for a given filename.
**Severity:** Critical -- this fully defeats the core enforcement claim the document repeatedly makes ("deterministic L5 CI lint... no central registry", `ADR-PROJ031-004-adr-identifier-convention.md:97`) for any file an author chooses to route through the allowlist instead of the waiver ledger. It blocks acceptance of the enforcement design as currently specified.
**Existing Defense:** Missing. The only defense described anywhere is the *intent* ("pre-adoption files") with no enforced check.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:600`; `adr-standards-rule-draft.md:211,213`; contrast with the waiver ledger's six required, audited fields at `adr-standards-rule-draft.md:191` / `ADR-PROJ031-004-adr-identifier-convention.md:577-579`.
**Dimension:** Methodological Rigor (a security-critical override mechanism was engineered in detail while an equally powerful sibling mechanism was left unguarded -- an internally inconsistent rigor level).
**Countermeasure:** Either (a) fold the grandfather allowlist into the same waiver-ledger schema (require a `rule: grandfather`, `approved_by`-API-verified, and a machine-checkable git-history assertion that the entry's referenced file's first commit predates the convention's adoption commit), or (b) freeze the allowlist's contents at the adoption commit via a hash/commit-SHA pin so no *new* entries can ever be added post-adoption, with L-9-style "no new entries" enforcement identical to the frozen-directory rule.
**Acceptance Criteria:** The lint spec states, and the M-6 regression test verifies, that any addition to `scripts/adr-grandfather-allowlist.txt` after the adoption commit either (i) fails CI outright, or (ii) requires the identical second-reviewer/justification/expiry protections as the waiver ledger.

### RT-002: Taxonomy-synonymy defense (L-10) does not cover the recommended-default project-scoped population [CRITICAL]

**Attack Vector:** D-1 states the canonical `ADR-{domain-slug}-NNN` form is "RECOMMENDED for all ADRs" (`ADR-PROJ031-004-adr-identifier-convention.md:186`), and the Canonical Location Model explicitly lists "Project (recommended)" using the same `ADR-{domain-slug}-NNN` grammar as the framework tier (`ADR-PROJ031-004-adr-identifier-convention.md:330`; `adr-standards-rule-draft.md:85`). Yet the **only** lint rule designed to catch near-duplicate/synonymous slugs (as opposed to exact duplicates) is L-10, and its check is explicitly scoped to "Fuzzy-match... every new domain slug against the **`docs/design/README.md` registry**" (`adr-standards-rule-draft.md:209`, identical `ADR-PROJ031-004-adr-identifier-convention.md:598`), and M-5b confirms: "the `ps-architect` agent SHOULD run an automated fuzzy-match... against the `docs/design/README.md` registry... **The registry (M-5) is the source of truth**" (`ADR-PROJ031-004-adr-identifier-convention.md:456`). `docs/design/README.md` is itself explicitly scoped as "a framework-ADR domain index" (`ADR-PROJ031-004-adr-identifier-convention.md:337`; `adr-standards-rule-draft.md:92`). There is no described registry, arbiter, or fuzzy-match process for the numerically dominant project-scoped canonical population. Two authors in two different projects can therefore each mint a subtly different but confusable domain slug -- e.g. `ADR-payment-flow-001` in one project and `ADR-payment-flows-001` in another, for genuinely unrelated decisions -- and **neither L-3 (exact-match only) nor L-10 (framework-registry-scoped) would flag it**, not even as a WARN.
**Category:** Ambiguity Exploitation / Boundary Violation
**Exploitability:** High -- requires no special access, just picking a plausible near-synonym slug; the document's own worked examples of synonymy (`agent-design` vs `agent-definition`) are drawn from the framework tier precisely because that is the only tier with any check at all.
**Severity:** Critical -- this directly undermines the decision's own headline discoverability/collision-resistance argument ("Best-in-class discoverability and sortability", `ADR-PROJ031-004-adr-identifier-convention.md:374`) for the majority of ADRs the convention will actually govern (project-local ones), since only 3 of the ~19 live ADRs are framework-tier.
**Existing Defense:** Missing for project-scoped canonical ADRs; Partial (WARN-only, framework-only) for `docs/design/`.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:186,330,337,456,598`; `adr-standards-rule-draft.md:85,92,209`.
**Dimension:** Completeness (the L-10 gap column of the lint table claims to solve "the *scaling* risk L-3's exact-match cannot catch" -- `adr-standards-rule-draft.md:209` -- but only for one-sixth of the corpus by tier).
**Countermeasure:** Extend L-10 (or add a companion rule) to fuzzy-match every new project-scoped canonical slug against **all other non-frozen canonical slugs repo-wide**, not only the framework registry; alternatively, require a single repo-wide `docs/adr-index.md` (superset of `docs/design/README.md`) that both tiers register into, so one arbiter process and one fuzzy-match pass covers the whole corpus.
**Acceptance Criteria:** L-10 (or its replacement) is demonstrated, in the M-6-equivalent regression test, to flag a synthetic pair of near-duplicate project-scoped slugs in two different `projects/*/decisions/` directories.

---

## Recommendations

**P0 (Immediate -- MUST mitigate before acceptance of the enforcement design):**
- **RT-001:** Bring `scripts/adr-grandfather-allowlist.txt` under the same audited-waiver protections as `scripts/adr-lint-waivers.yaml`, or freeze it at the adoption commit so no post-adoption entries are possible. Acceptance criteria as stated in [RT-001](#rt-001-grandfather-allowlist-is-an-unguarded-parallel-bypass-of-the-entire-fail-rule-model-critical).
- **RT-002:** Extend the L-10 synonymy check (or add a sibling rule) to cover project-scoped canonical slugs repo-wide, not only the `docs/design/README.md` framework registry. Acceptance criteria as stated in [RT-002](#rt-002-taxonomy-synonymy-defense-l-10-does-not-cover-the-recommended-default-project-scoped-population-critical).

**P1 (Important -- SHOULD mitigate):**
- **RT-003:** Extend the L-1a case-folded lookalike-ban regex from `^(proj|epic|feat|story)\d+$` to the full closed set of Jerry worktracker entity-ID prefixes (add `bug`, `task`, `spike`, `enabler`, and any others enumerated in `skills/worktracker/rules/worktracker-entity-hierarchy.md`), so an origin-scoped-looking ID for an unlisted entity type cannot pass as a legitimate subject slug. Acceptance criteria: the regression test includes a synthetic `ADR-bug006-001` case and confirms it is rejected or flagged, not silently accepted as canonical.
- **RT-004:** Specify an automated expiry check: a scheduled or PR-triggered job that fails CI (or opens a tracked issue) for any waiver ledger entry whose `expires` date has passed and whose underlying FAIL condition still exists. Acceptance criteria: the lint spec names this check with an L-N (or equivalent) identifier and it is included in the gating regression test.
- **RT-005:** Assign explicit rule identifiers to the append-only ledger check and the API-verified second-reviewer check (they are currently prose-only), and include both in the M-6 gating regression test alongside the 16-file grandfather test. Acceptance criteria: the regression test suite enumerates and exercises both checks with a passing and a failing case each.

**P2 (Monitor -- MAY mitigate):**
- **RT-006:** Explicitly specify L-4's behavior when `origin_entity` is absent for a dialect-form filename (treat as FAIL, not vacuous pass), and consider promoting L-6 (provenance) to FAIL for dialect-form ADRs specifically, since provenance is exactly what L-4 depends on.
- **RT-007:** Note in the rule draft that title-slug tails are non-normative and MUST NOT be relied upon by readers/tools to infer supersession or authority; the `id`/`supersedes`/`superseded_by` frontmatter fields are the only trustworthy signal. No lint change required, only a documentation clarification.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-002: the synonymy defense does not cover the recommended-default project-scoped population; RT-006 leaves an unspecified corner case |
| Internal Consistency | 0.20 | Negative | RT-003: the lookalike-ban enumeration is inconsistent with the full closed set of worktracker entity prefixes it is meant to guard against; RT-001 shows two exemption paths with wildly different rigor levels for the same threat |
| Methodological Rigor | 0.20 | Negative | RT-001 and RT-004 both show the override model's engineering effort was not applied uniformly across all its own exemption/expiry paths |
| Evidence Quality | 0.15 | Neutral | Findings are grounded in direct textual citation of the deliverable and companion draft; RT-007 is a residual not directly evidenced by an exploit, only by absence |
| Actionability | 0.15 | Positive | Every P0/P1 recommendation names a concrete spec change and a verifiable acceptance criterion (extend a regex, add fields to a test, assign a rule ID) |
| Traceability | 0.10 | Negative | RT-005: the override model's own integrity checks are not traceable to a numbered rule ID or a named test, unlike every other lint behavior in the document |

**Overall assessment:** Targeted remediation required. Neither Critical finding attacks the ADR's core subject-vs-origin thesis; both attack the credibility of the deterministic-enforcement claim the document uses to justify not needing a HARD rule (c-001/c-002). Closing RT-001 and RT-002 (and ideally RT-003 through RT-005) before the M-6 ratification blocker is marked complete would remove the gap between "the lint is designed to be un-gameable" and what the current specification actually guarantees.

---

## Execution Notes

- **Protocol steps completed:** 5 of 5 (Threat Actor defined; 7 attack vectors enumerated across all 5 categories -- Ambiguity, Boundary, Circumvention, Dependency, Degradation; defense gaps assessed per finding; countermeasures specified for all Critical/Major findings; scoring impact synthesized).
- **H-16:** Confirmed via file-existence check only (see [Header](#header)); content of the S-003 output was not read, per BLIND PROTOCOL.
- **Scope discipline:** No file under this project's `decisions/` or `design/` directories was edited (P-020). No file under `.../adversary/` other than this one was read (BLIND PROTOCOL). All factual claims above cite file path and line number from the two deliverables, `skills/worktracker/rules/worktracker-entity-hierarchy.md` / `worktracker-directory-structure.md`, or are explicitly Glob-verified absences; inferential/qualitative statements (e.g., exploitability judgments) are labeled as such and are not presented as fact (P-022).
- **Execution Statistics:** Total Findings: 7. Critical: 2. Major: 3. Minor: 2. Protocol Steps Completed: 5 of 5.

---

*Strategy: S-001 Red Team Analysis | Template: `.context/templates/adversarial/s-001-red-team.md` | Iteration: 3 | Finding Prefix: RT-NNN-20260702i3*

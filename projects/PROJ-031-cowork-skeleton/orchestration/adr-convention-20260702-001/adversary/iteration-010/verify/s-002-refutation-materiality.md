# Refutation Panel: S-002 Devil's Advocate — Materiality Lens (Iteration 10)

> **Panel role:** Attempt to REFUTE every Critical finding in `adversary/iteration-010/s-002-findings.md`. Default to REFUTED if uncertain. Materiality lens: does the finding genuinely block the standard's purpose (collision-free identity, honest promotion, adoptable convention)? Edge cases with negligible probability x impact, cosmetic wording, and style preferences are REFUTED even if factually true.
> **Scope:** Only Critical findings require a verdict (002-001, 002-002). 002-003 is Major and out of this panel's mandate; noted for completeness only, no verdict rendered.
> **Blind protocol:** Only the target S-002 report, the two current deliverables, and `subtraction-pass-notes.md` were read. No other refuters' or panels' outputs were read.

---

## 002-001: L-4 ID↔location undefined/broken for EPIC002-prefixed dialect ADRs — CRITICAL

**Verdict: REFUTED**

**Factual core confirmed.** Independently verified via `Glob('**/decisions/ADR-EPIC002-*.md')`: both `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md` and `.../ADR-EPIC002-002-enforcement-architecture.md` exist exactly where the ADR claims (ADR:113). The Location Model table (`ADR-PROJ031-004-adr-identifier-convention.md:384-393`; identical in `adr-standards-rule-draft.md:77-86`) literally assigns EPIC/FEAT/STORY-prefixed dialect IDs only to the "Entity-embedded" row, whose home is `projects/.../work/.../{ENTITY}/` — not `projects/*/decisions/`, where the two real EPIC002 files actually sit. So the finder is factually correct that no table row textually matches this exact (prefix-type, location) combination.

**Why this does not clear the materiality bar.** The ADR's own Migration Plan already, explicitly, and unambiguously dispositions these exact files: the "Project-scoped families (`PROJ010`×6, `PROJ022`×2, `PROJ031`×3, **`EPIC002`×2**, `STORY015`×1, `150`×1)" row states "Grandfather in place. **Valid dialect.** Re-slug only if/when promoted." with cost "**Zero**" (`ADR:514`; identical wording in the rule draft's Frozen-and-Grandfathered section, `adr-standards-rule-draft.md:94`: "Grandfathered dialect families... remain valid in place, extendable within their dialect; re-slug only if promoted"). This is the document's own plain-language resolution of exactly the question the finder raises (is this dialect ADR valid where it sits?) — answered "yes, zero cost" twice, in both deliverables, independent of the Location Model table's more granular wording. A reader or future lint-implementer following the document's stated intent, not just its formal table, has an unambiguous answer.

Separately, the alleged operational harm does not hold up under either of the finder's own two readings:
- **"Strict reading" harm (CI fails at M-11):** M-11 (the only Migration-Plan row that touches these two files) is explicitly marked **"No" (not gating)** and "optional schema-completeness" (`ADR:546`). There is no committed trigger event that forces a git-modify of these files under this convention. The claimed self-inflicted CI failure requires an event the document itself does not schedule as required.
- **"Loose reading" harm (no guarantee for the whole EPIC/FEAT/STORY class):** this is speculative — the finder does not demonstrate any *other* real corpus file exhibiting the same location mismatch (only these same two named files are cited), so the claimed class-wide defeat of L-4's purpose is not evidenced beyond the two already-disclosed, already-grandfathered instances.

This is squarely a specification-wording nuance in a not-yet-built lint (Claim-Status: DESIGNED, NOT BUILT — `ADR:659`), for two named, already-discussed, already-grandfathered legacy files, with an optional/non-gating remediation path. It sits at the same rigor tier as the document's own R-9/R-14/R-15/R-16/R-17 pattern — "a specific enforcement rule has an edge-case gap for specific real files" — every one of which this exact document has repeatedly and successfully dispositioned as RESIDUAL-DISCLOSED, not as a blocking Critical requiring pre-acceptance remediation. It does not block collision-freedom (that is L-3's job, which already correctly widened its regex to catch uppercase-dialect duplicates including `ADR-EPIC002-001`), honest promotion (M-11 is optional schema-completeness, not a promotion path), or the convention's adoptability as MEDIUM-tier guidance (which the ADR repeatedly states stands independent of the lint's completeness). REFUTED on materiality.

---

## 002-002: Rule draft not self-contained — 14 bare R-N citations unreachable in every distribution — CRITICAL

**Verdict: REFUTED**

**Factual core confirmed.** The rule draft does cite bare `R-N` shorthand — verified directly: R-15 (`adr-standards-rule-draft.md:46`), R-14 (`:94`), R-10 (`:94, :177, :179, :181`), R-9 (`:175`), R-11 (`:179`), R-16 (`:179`), R-13 (`:200-202`), R-B (`:206`), R-17 (`:151`) — and the References table (`:234`) explicitly states "the `R-N` shorthand used above resolves there" (i.e., in the parent ADR). The Enforcement Scope table (`ADR:663-680`) and `phase3-skeleton-generation-design.md:159` do confirm `projects/` (where both deliverables currently live) is unconditionally stripped from CoWork/plugin builds, and `docs/` (the post-M-9 destination) is only a *recommended*, not yet mandatory, additional strip target (`:168-170`). The chain of facts underlying the finding is accurate.

**Why this does not clear the materiality bar.** Checking every one of the cited `R-N` occurrences against its surrounding sentence shows the substance of each disclosure is stated **inline**, not gated behind the tag:
- `:46` (R-15): "...no lint in the 5-rule core checks the two agree or that `id:` is corpus-unique — a disclosed residual (**R-15** in the parent ADR's Risks register)." — the disclosure is the preceding clause; R-15 is a citation for it, not its content.
- `:94` (R-14, R-10): "a new bare file added under them (including a colliding one) is a disclosed residual (**R-14**...), not a lint stop" — same pattern.
- `:175/:177/:179/:181` (R-9, R-10, R-11, R-16, R-13): each rule row states the gap in full prose ("It does not structurally reject a lowercase slug that case-folds..."; "supersedes/amends/amended_by are not checked... a disclosed 3-of-6 asymmetry (R-11)"; "its real surface against today's corpus is empty... disclosed as R-16") immediately adjacent to the tag.
- `:206` (R-B): "The citation-scan omission is an [INHERENT] residual **R-B** — the core detects only structural frontmatter links" — substance and tag in the same clause.

This is not incidental: it mirrors a design pattern the parent ADR states explicitly for its own review-tag glossary — "A reader without access to the adversary directory can safely treat every such tag as 'a reviewer raised this point; the adjacent prose is the response.' The tags are retained for traceability (P-004)... they carry no normative force" (`ADR:65`). The `R-N` shorthand in the rule draft functions identically: a P-004 traceability pointer for a reader who wants to cross-check the fuller parent-ADR treatment, layered on top of prose that is already self-sufficient for comprehension and application of every `ADR-M-001`…`013` standard, the ID Scheme, the Location Model, and the L5 Lint Specification. A downstream CoWork/plugin adopter reading only `.context/rules/adr-standards.md` can fully understand and follow every normative standard in the file without resolving a single `R-N` reference; what they lose is the ability to cross-verify a residual's fuller discussion in the parent ADR's Risks register — a traceability/polish gap, not a comprehension or adoptability blocker.

The finding's own **Impact** claim ("a downstream author trying to understand why L-7 or L-4 behaves the way the rule file says it does hits a dead reference by design") does not hold: the L-7 and L-4 rows (`:178-179`) already state the "why" in full prose before the tag appears. This is a genuine, previously-undisclosed gap in *cross-file traceability polish*, not in the standard's core purpose of delivering adoptable, self-executing naming/location/promotion guidance. REFUTED on materiality.

---

## Note on 002-003 (Major, out of scope)

Not adjudicated under this panel's mandate (Criticals only). Flagged for the record: its core claim (grandfather regression test covers only L-1, not L-3/L-4/L-7) is factually accurate and is the same underlying evidence base as 002-001; no verdict rendered here.

---

## Summary

| ID | Severity | Verdict |
|----|----------|---------|
| 002-001 | Critical | REFUTED |
| 002-002 | Critical | REFUTED |

# Refutation Panel — S-004 Pre-Mortem Analysis (iteration-009) — MATERIALITY Lens

> Panel task: attempt to REFUTE every Critical finding in `s-004-findings.md`. Default to REFUTED if uncertain. Materiality test: does the finding genuinely block the standard's purpose (collision-free identity, honest promotion, adoptable convention)? Negligible-probability-x-impact edge cases, cosmetic wording, and style preferences are REFUTED even if factually true.

## Scope

Target report: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-004-findings.md`
Critical findings under review: **004-001**, **004-002** (004-003 and 004-004 are Major — out of scope for this Critical-only refutation panel).

---

## 004-001: "A second ADR-producing agent (`eng-architect`) is entirely outside the convention's scope" [CRITICAL]

**Verdict: REFUTED**

**Reasoning:**

Factually verified: `skills/eng-team/agents/eng-architect.md:22` ("Create architecture decision records (ADRs) using Nygard format with security rationale"), `:57` ("ADR Documentation" methodology step), and `:86-95` (Output Path Resolution, project-default = `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md`) all match exactly as cited. The agent is real and its description does reference ADR production.

However, on materiality the finding does not hold. eng-architect's **default** output filename (`eng-architect-{topic-slug}.md`) does not match the `ADR-*` grammar this convention governs, and its **default** directory (`engagements/`) is neither of the two scanned/canonical ADR homes (`projects/PROJ-NNN-*/decisions/`, `docs/design/`) defined in `adr-standards-rule-draft.md:75-89` (Canonical Location Model). Under default behavior, eng-architect's output never enters the namespace this convention polices — it cannot collide with a governed `ADR-{slug}-NNN` identity, is not scanned by L-1/L-3/L-4/L-7 (which key on `ADR-*.md` under the two canonical roots), and would not be mistaken by a reader for a governed ADR (the filename itself doesn't say "ADR"). The harm scenario the finding depends on — a caller explicitly overriding eng-architect's P1/P2 path to land an `ADR-`-named file inside `decisions/`/`docs/design/` — is a hypothetical requiring active, atypical steering, not a demonstrated or likely current behavior; the finder's own "Likelihood: High" rests on eng-architect's existence as a routed agent, not on evidence that this override path is actually exercised.

M-12/Producer-Fixes' "the producing agent must emit compliant IDs" claim is scoped to the agent that actually mints files matching (or attempting to match) the `ADR-*` grammar into the governed corpus (`ps-architect.md`) — that is the real source-of-truth risk to collision-free identity. Auditing every agent in the repository whose prose happens to mention "ADR"/"Nygard format" is a scope expansion the ADR's own subtraction doctrine explicitly and repeatedly declines to chase (`subtraction-pass-notes.md:26` "subtract, don't compensate"; rule-draft `adr-standards-rule-draft.md:201` "Descoped, honestly... None is promised for a later release"). A low-probability, override-dependent, corpus-external edge case does not genuinely block collision-free identity, honest promotion, or convention adoptability — it is exactly the class of finding the materiality lens directs to refute.

---

## 004-002: "The 'no existing rule' premise is not fully verified against the repo's own test suite" [CRITICAL]

**Verdict: REFUTED**

**Reasoning:**

Factually verified in detail: `tests/project_validation/architecture/test_path_conventions.py:65-101` (`test_no_cross_project_references`) is parametrized over all discovered `PROJ-*` directories via `tests/project_validation/conftest.py:120-139` (including `PROJ-031-cowork-skeleton`), is not exempted for `decisions/`-path files, and its regex `projects/PROJ-(?!031)\d{3}` would match `projects/PROJ-001-oss-release/decisions/` at ADR line 292 and `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md` at ADR line 747 (References table row 6) — both independently confirmed by direct file read. The finder's core technical claim (a real, pre-existing, parametrized architecture test whose pattern this ADR's own text would trip) is correct, and the finder honestly labeled the "does it currently fail in CI" component as inference rather than a confirmed execution (P-022-compliant).

On materiality this does not survive. `test_path_conventions.py:5-8` states its own scope explicitly: it "enforce[s] the project isolation principle (ADR-003)" — a general cross-project-coupling/document-hygiene test that applies uniformly to every category directory (`research/`, `synthesis/`, `analysis/`, `decisions/`, `reports/`, `investigations/`, `reviews/`), not an ADR-specific identifier/numbering/location/promotion/superseding rule of the kind the Context section's survey was scoped to find (`ADR-PROJ031-004-adr-identifier-convention.md:95`, "no rule anywhere governing ADR identifiers, numbering, location, promotion, or superseding"). The test governs what cross-project *citation text* may appear in any project markdown file; it says nothing about ADR ID grammar, ADR file placement as an ADR-specific concern, ADR promotion mechanics, or ADR superseding — the actual subject matter Scheme B decides. A citation-hygiene test collision (if it in fact fires in CI, which is not confirmed) is a pre-existing, orthogonal technical-debt item that would need reconciling regardless of which ADR ID scheme (A through F) had been chosen; it does not touch collision-free identity, honest promotion, or the adoptability of the domain-slug convention itself. It is functionally identical in kind to the R-1…R-17/R-A/R-B/R-C residuals this ADR has repeatedly, and reasonably, downgraded from "blocking Critical" to "disclosed residual with owner and cadence" across eight prior adversarial iterations (`subtraction-pass-notes.md:121-134`) — treating this one gap as blocking while dozens of structurally similar gaps were correctly triaged as non-blocking residuals would be an inconsistent standard. Low-to-moderate probability of an actual CI break, orthogonal impact to the convention's actual purpose: refuted under the materiality lens.

---

## Summary

| ID | Severity (finder) | Verdict | Basis |
|----|--------------------|---------|-------|
| 004-001 | Critical | REFUTED | Default output path/filename never enters the governed `ADR-*` corpus; harm requires an unevidenced caller override; scope-audit-everything is explicitly out of the ADR's declared descope. |
| 004-002 | Critical | REFUTED | Pre-existing test is a general project-isolation/citation-hygiene mechanism, not an ADR identifier/location/promotion rule; even if it fires in CI, it is orthogonal to Scheme B's mechanics and structurally identical to the many already-disclosed, non-blocking residuals (R-1…R-17). |

Both Critical findings are technically well-evidenced (file+line verified) but fail the materiality bar: neither genuinely blocks collision-free ADR identity, honest promotion, or the convention's adoptability. Per instruction, defaulted to REFUTED under uncertainty about downstream/hypothetical impact.

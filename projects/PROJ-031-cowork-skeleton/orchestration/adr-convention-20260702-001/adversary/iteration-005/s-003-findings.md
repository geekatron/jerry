# Steelman Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + adr-standards-rule-draft.md)

## Steelman Context
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (826 lines) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (326 lines)
- **Deliverable Type:** ADR (Architecture Decision Record) + companion MEDIUM-tier rule draft
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind reviewer, iteration 5) | **Date:** 2026-07-02 | **Original Author:** ps-architect agent (per package footer)

---

## Summary

**Steelman Assessment:** The package's core thesis — ADR identity should encode *subject* (domain-slug), not *origin* (project), because ADRs are the one Jerry artifact class whose governing scope is mutable by design — is coherent, well-argued, and already extensively self-critiqued across four prior iterations. The strongest available version of this thesis is *stronger* than the document currently states, because the package does not cite the most directly relevant corroborating evidence available in its own repository: two non-ADR framework-governance artifacts from the *same* evidentiary project (PROJ-007) that already completed an analogous subject-slug-survives-promotion migration.

**Improvement Count:** 0 Critical, 3 Major, 1 Minor

**Original Strength:** Very high. This is a heavily-remediated C4 package (5 iterations, ~50+ prior adversarial findings closed across S-001/S-002/S-004/S-007/S-010/S-011/S-012/S-013) with extensive, well-labeled P-022 honesty disclosures (Claim-Status blocks, INHERENT residuals, confidence caps). The gaps identified below are evidentiary-enrichment opportunities within an already-charitable reading, not defects that would cause the argument to fail under fair critique.

**Recommendation:** Incorporate improvements. None of the findings below change the recommended decision (Scheme B / D-1 through D-5); all of them would raise the evidentiary rigor of the confidence framing and reduce the disclosed epistemic caps (n=3, "zero demonstrated Path-1 instances") that the document itself treats as load-bearing limitations.

---

## Steelman Reconstruction

Per Step 3 (Reconstruct the Argument), the reconstruction below does not rewrite the full 826/326-line package — at iteration 5 that would discard proportionate, already-converged prior remediation. Instead, per the Output Format's Strategy-Specific Adaptation, this section reconstructs the **single passage where the package's own strongest argument is understated**, showing the strengthened version inline, annotated `[SM-NNN]`.

### Reconstructed passage: Rationale, Argument 3 ("Jerry's own thesis picks the regime")

**Original (ADR:279, abridged):**
> "3. **Jerry's own thesis picks the regime, and the corpus has already voted (promotion-dependent, but empirically supported).** ... All framework ADRs arrived by promotion — but stated with DA-004 honesty (iter-3): this is **3 promoted ADRs from 2 correlated framework-mandate projects (PROJ-007 → 2; EPIC-002 → 1), not 3 statistically-independent trials**... The evidentiary base is thus a small, correlated one (this is exactly why Confidence is capped at 0.75...)"

**Strengthened (reconstruction, [SM-001]):**
> "3. **Jerry's own thesis picks the regime, and the corpus has already voted — not only for ADRs.** All 3 framework ADRs arrived by promotion from 2 correlated framework-mandate projects (PROJ-007 → 2; EPIC-002 → 1) — disclosed honestly as a small, correlated sample (n=3), which is why Confidence is capped at 0.75. **What the package does not yet cite is that the same evidentiary project, PROJ-007, independently ran the identical migration on two *non-ADR* framework-governance artifacts, using a functionally equivalent mechanism**: `.context/rules/agent-development-standards.md` and `.context/rules/agent-routing-standards.md` were authored as `ps-architect-003-agent-development-standards.md` and `ps-architect-003-agent-routing-standards.md` under `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-4-codification/ps-architect-003/`, then installed into `.context/rules/` with the agent-run-scoped prefix *stripped* and the domain-slug tail *preserved unchanged* (`projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/EN-001.md:46-47`). Both files carry a version footer attributing origin to 'PROJ-007 Agent Patterns' as free text, not as an identity component (`.context/rules/agent-development-standards.md:471`; `.context/rules/agent-routing-standards.md:553`). This is a second, independently-evolved artifact class in the same repository converging on the identical principle this ADR proposes for ADRs — subject-slug survives migration; origin is metadata, not identity — raising the promotion-frequency evidentiary base from 3 ADR instances to at least 5 subject-slug-preserving migrations across 2 artifact classes, from the same 2 correlated projects. This does not lift the correlation caveat (still 2 projects), but it does materially strengthen the *cross-artifact-class generality* of the underlying principle, which is a different and additive axis of evidence from raw promotion count."

**Preserved intent:** The reconstruction changes no conclusion, no decision, and no confidence number stated in the original — it supplies additional, already-available corroborating evidence for a claim the original document already makes and already caps conservatively. This is squarely a strengthening of expression/evidence, not a substantive redirection (Step 2 classification: **Evidence**, not Substantive).

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-20260702I5 | Missing cross-artifact-class corroborating evidence for the promotion-frequency thesis and the "Path-1 zero-churn, not yet demonstrated" Claim-Status | Major | ADR:279, :305-309, :324-326, :478-480, :580 assert the promotion evidentiary base is "n=3 ADRs" and that "zero Path-1 promotions have actually occurred yet" | Cite the PROJ-007 rule-file promotions (`.context/rules/agent-development-standards.md`, `agent-routing-standards.md`; source `EN-001.md:46-47`) as a second artifact class demonstrating the same subject-slug-survives-promotion principle, broadening the evidentiary base without changing the stated confidence number | Evidence Quality |
| SM-002-20260702I5 | The "ADRs are the sole ontology exception" framing (L2 Architectural Implications) omits that a sibling migrating-artifact class (rule files) already exists in the repo and currently preserves provenance even more weakly (free-text footer, no frontmatter) than what this ADR proposes for ADRs | Major | ADR:433 ("ADRs become the one Jerry entity whose ID encodes subject, not scope") | Acknowledge rule files as a second migrating-artifact class with an even weaker provenance mechanism today, and note the ADR's `origin_project`/`scope` frontmatter design as a candidate pattern rule files could later adopt | Completeness |
| SM-003-20260702I5 | Fix 3 (ps-architect.md filename remediation) is framed as inventing new tooling for a defect, without noting that the exact prefix-strip mechanic it needs was already proven in production by the PROJ-007 rule-file installation | Major | Rule draft:279-287 (F3-b: "Canonical `projects/{origin_project}/decisions/ADR-{domain-slug}-{NNN}-{title-slug}.md`... The `{ps_id}-{entry_id}` PS linkage moves to frontmatter") | Note that `ps-architect-003-{domain-slug}.md` → `{domain-slug}.md` (prefix-strip, slug unchanged) is a precedent-backed, cheaper remediation shape for Fix 3 than implied, since it already shipped for 2 rule files | Methodological Rigor |
| SM-004-20260702I5 | The pre-flight collision one-liner is fully specified but not connected to the repo's existing `Makefile`/`.pre-commit-config.yaml` infrastructure, which already defines a `lint` target (`Makefile:59-61`, ruff+pyright only) | Minor | ADR:414-425 (bash one-liner, described as something "authors ... SHOULD run") | Add as a `make lint-adr` target or a pre-commit hook entry, closing part of R-1 before M-6 ships, at near-zero engineering cost given the existing tooling surface | Actionability |

**Finding ID Format:** `SM-{NNN}-{execution_id}` where `execution_id = 20260702I5` (2026-07-02, iteration 5).

---

## Improvement Details

### SM-001 — Missing cross-artifact-class corroborating evidence (Major, Evidence Quality)

**Affected Dimension:** Evidence Quality (0.15 weight); secondarily Methodological Rigor.

**Original Content:** The document's strongest empirical support for "promotion is a first-class, recurring operation" rests entirely on 3 ADRs from 2 correlated projects (ADR:83, :163, :246, :279, :305-309), a base the document itself repeatedly and honestly caps: "Confidence... capped at the trade study's declared ceiling... 0.70–0.75... never higher, on a C4 governance call resting on n=3" (ADR:324-326), and "**PM-009** — forward promotion rate rests on n=3" (ADR:478-479). Separately, the document asserts "**Claim-Status: Path 1 is the *designed* default, not yet a *demonstrated* one**... zero Path-1 promotions have actually occurred yet" (ADR:580).

**Strengthened Content:** Filesystem-verified (2026-07-02): `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-4-codification/ps-architect-003/ps-architect-003-agent-development-standards.md` and the sibling `...-agent-routing-standards.md` are the origin-scoped drafts of what now live at `.context/rules/agent-development-standards.md` (v1.3.0) and `.context/rules/agent-routing-standards.md` (v1.1.0). `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/EN-001.md:46-47` documents the intended source→destination mapping explicitly (`ps-architect-003-agent-development-standards.md` → `.context/rules/agent-development-standards.md`). Both installed files retain their domain-slug tail unchanged and drop only the agent-run-scoped prefix; both preserve origin as free-text ("*Source: PROJ-007 Agent Patterns...*", `agent-development-standards.md:471`; `agent-routing-standards.md:553`), not as part of identity. This is a second, non-ADR artifact class from the *same* evidentiary project independently converging on exactly the principle D-1/D-2 propose.

**Rationale:** This does not overturn any conclusion — it is additive evidence for a claim the document already makes cautiously. It matters because two of the document's own headline epistemic-humility claims ("n=3," "zero Path-1 demonstrated") are stated more starkly than the fuller evidentiary picture supports, and a charitable, well-evidenced reconstruction should say so. Citing it would not raise the numeric confidence past 0.75 (the document's own ceiling reasoning, tied specifically to *ADR* promotion rate, would reasonably still apply), but it would legitimately soften "zero Path-1 promotions have actually occurred yet" to "zero ADR-specific Path-1 promotions; at least two structurally analogous non-ADR promotions have."

**Best Case Conditions:** This improvement is strongest if the reader accepts that "subject-slug survives migration; origin lives in metadata" is a *general* Jerry principle (which Rationale argument 3 already gestures toward via "Jerry's *own thesis*"), rather than an ADR-only claim — in which case cross-artifact-class evidence is exactly the right kind of corroboration, and its omission is the single largest missed opportunity to strengthen the document's most-hedged argument.

---

### SM-002 — "Sole ontology exception" framing omits a sibling migrating-artifact class with weaker provenance (Major, Completeness)

**Affected Dimension:** Completeness (0.20 weight); secondarily Internal Consistency.

**Original Content:** ADR:433 ("L2: Architectural Implications") states: "ADRs become the one Jerry entity whose ID encodes subject, not scope — because they are the one entity whose scope is *mutable*... Left implicit, the ADR exception is an onboarding trap." Rule-M-011 in the companion draft (rule draft:56) states the same "deliberate ontology exception" claim for ADRs alone.

**Strengthened Content:** Rule files (`.context/rules/*.md`) are themselves a migrating-artifact class — content researched/authored inside a project (PROJ-007, per the verified footers) and later relocated into permanent framework governance (`.context/rules/`) with no `projects/PROJ-NNN-*/` prefix ever appearing in their identity. Unlike the ADR convention this document proposes, rule files today have **no structured origin frontmatter at all** — only an inline, unstructured footer sentence. That is a strictly *weaker* provenance mechanism than even the "presence-checked, not accuracy-checked" L-6 the ADR already self-critiques (ADR:446, FM-104 correction) for ADRs.

**Rationale:** The document's "sole ontology exception" framing would be more complete, and less exposed to a "why only ADRs?" objection, if it named rule files as a second (already-existing, already-successful) case of the same subject-encodes-identity pattern, and flagged the origin-frontmatter gap in that sibling class as a related, out-of-scope-but-worth-naming future opportunity (analogous to how the document already handles `DEC-NNN` non-conflation in the [Relationship to Worktracker DEC-NNN](#) section, ADR:732-744). This is a completeness gap, not a substantive one: it does not change what the ADR decides for ADRs.

**Best Case Conditions:** Strongest if a future reader asks "if scope-mutability is the real differentiator, why is the rule addressed only to ADRs and not to rule files, which migrate the same way?" — the document currently has no answer prepared for that question, despite having the evidence on hand (per SM-001) to answer it well.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-002 supplies a sibling-artifact-class comparison the L2 Architectural Implications section is otherwise silent on |
| Internal Consistency | 0.20 | Neutral | No inconsistency was found in the reviewed material; findings are additive, not corrective |
| Methodological Rigor | 0.20 | Positive | SM-001/SM-003 show the document's own evidentiary caps ("n=3," "zero Path-1 demonstrated," "ps-architect.md needs novel tooling") are more conservative than the available repo evidence requires |
| Evidence Quality | 0.15 | Positive | SM-001 is a direct, filesystem-verified, previously-uncited corroborating data source for the document's most-hedged claim |
| Actionability | 0.15 | Positive | SM-004 identifies an immediately actionable, near-zero-cost step (Makefile/pre-commit integration) not currently in the Migration Plan |
| Traceability | 0.10 | Neutral | Existing SM-NNN/RT-NNN/etc. tagging convention is already exemplary; no traceability gap found |

---

## Best Case Scenario (Step 4)

**Ideal conditions under which this Steelman Reconstruction is most compelling:** The reconstruction is strongest if the reviewer accepts two premises already present in the original document: (1) that "Jerry's own thesis" (accrual from projects into the framework) is the operative regime-selector for this decision (ADR:142, :279), and (2) that the differentiator for subject-vs-origin identity is scope-*mutability*, not artifact-type (ADR:271, :433). Under both premises — which the document itself asserts — cross-artifact-class evidence of the same mutability-driven pattern (rule files) is not a tangential aside but directly on-point corroboration the document should already want to cite. **Key assumption:** the PROJ-007 rule-file installation (EN-001 TASK-012/013) is accurately characterized here as a completed migration; note that `EN-001.md:70-71` lists these tasks' tracking status as `PENDING` and `EN-001.md:87-88` shows their completion checklist items unchecked, while the destination files verifiably exist today at versions 1.3.0/1.1.0 — an apparent staleness in EN-001's own tracker rather than counter-evidence that the migration did not occur. **Confidence assessment:** High that the file-level evidence (draft path + destination path + footer text) is accurately reported (P-022: directly filesystem-verified); moderate-only on whether EN-001's tracker discrepancy should itself be flagged to PROJ-007's owner (out of scope for this review; noted as an aside, not a finding against this package).

---

## Execution Statistics
- **Total Findings:** 4
- **Critical:** 0
- **Major:** 3
- **Minor:** 1
- **Protocol Steps Completed:** 6 of 6

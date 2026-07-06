# Steelman Report: PROJ-031 Phase-1 Design Package

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Execution metadata |
| [Summary](#summary) | Assessment and improvement count |
| [Steelman Statement](#steelman-statement) | Strongest-possible argument for the design package |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings at a glance |
| [Improvement Details](#improvement-details) | Evidence, rationale, and recommendation for every Critical and Major finding |
| [Minor Findings](#minor-findings) | Concise entries for Minor improvements |
| [Scoring Impact](#scoring-impact) | Effect of improvements on the six S-014 dimensions |

---

## Steelman Context

| Field | Value |
|-------|-------|
| **Strategy** | S-003 Steelman Technique |
| **Strategy ID** | S-003 |
| **Template** | `.context/templates/adversarial/s-003-steelman.md` v1.0.0 |
| **Deliverables Reviewed** | `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` (primary) |
| | `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` |
| | `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` |
| **Supporting Context** | `projects/PROJ-031-cowork-skeleton/research/phase1-skeleton-ci-research.md` (grounding only) |
| **Criticality Level** | C4 (AE-003 auto-escalation: new ADRs; AE-005: security-relevant CI + token handling) |
| **Quality Target** | >= 0.95 composite (per ORCHESTRATION_PLAN.md; exceeds constitutional minimum of 0.92) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Execution ID** | qg1-0626 |
| **Steelman By** | adv-executor (S-003) | **Date:** 2026-06-26 |
| **Blindness Constraint** | Reviewer did NOT read any peer strategy findings in `iteration-001/` or `_discarded-contaminated-run/` |

---

## Summary

**Steelman Assessment:** This is a technically rigorous, architecturally conservative design package that solves a well-scoped binary problem using the minimum complexity necessary, backed by strong operational precedents in the repository. Every major risk is handled through design-level prevention, architectural redundancy, or a pre-designed escape hatch — but the documents present several of their strongest arguments in subordinate positions or implicit forms, leaving them vulnerable to Devil's Advocate and Pre-Mortem challenges that the evidence already answers.

**Improvement Count:** 1 Critical, 3 Major, 4 Minor

**Original Strength:** The phase-1 deliverables are substantively sound. The research grounding is code-anchored, the ADRs follow a clear decision structure with steelmanned alternatives, S-010 self-refine was applied, and R-001 is honestly disclosed. The weaknesses identified here are presentational and structural — the underlying arguments are correct and largely in the documents, but require the reader to assemble them across sections.

**Recommendation:** Incorporate Critical and Major improvements before downstream S-002 Devil's Advocate and S-004 Pre-Mortem executions. The Critical finding (SM-001) is the highest-priority: without an explicit tamper-detection argument in ADR-001, a C4 adversary can credibly claim the security story is incomplete.

---

## Steelman Statement

This design package argues — in its strongest form — the following:

Jerry can be distributed as a Claude CoWork plugin by generating a `cowork-skeleton` branch that removes the `projects/` directory, reducing tracked files from 6,344 to approximately 1,744 — a 65% reduction relative to the ~5,000-file CoWork ceiling, leaving substantial headroom against future file growth in retained directories. The branch is regenerated on every release using four plain git commands that mirror the repository's established `gh-pages` force-push pattern, introducing zero new tooling or dependencies.

The generation strategy provides not just reliability but **verifiable supply-chain integrity**: by pinning all commit metadata (parent SHA, author/committer dates, bot identity, commit message template embedding source tag and 40-char source SHA), every re-run of the same release tag produces a **bit-identical commit SHA**. This bit-identical property is simultaneously a reliability guarantee (idempotent re-runs for CI recovery) and a tamper-detection mechanism (any in-place modification to the live branch breaks the SHA, making interference detectable by re-running the generator).

The CI token choice is **structurally superior**, not merely incrementally safer. `GITHUB_TOKEN` eliminates an entire attack-surface class — long-lived credential lifecycle — that a Personal Access Token would introduce: no credential to steal, no rotation to fail, no expiry to monitor, and no re-trigger capability to exploit. The skeleton push's loop-safety is over-determined: three independent invariants (trigger shape, listener shape, credential shape) each individually prevent an infinite regenerate-push loop, meaning any single misconfiguration still leaves two protections intact. This triple redundancy is the appropriate posture for a C4 security argument.

The primary unresolved risk — whether the CoWork file-count limit applies to the clean-clone tree or to the local working directory — is a **controlled binary-resolution risk**, not an existential threat. The proposed verification test directly distinguishes between the two hypotheses (clean clone = 1,744 files; local dev checkout = 24,636 files, a 14:1 ratio), and both resolution paths have fully documented responses: proceed as planned (hypothesis a) or pivot to local-plugin configuration guidance with user escalation per H-02 (hypothesis b). No irreversible action is authorized until this binary test resolves.

The quality governance applies the framework's most rigorous controls (C4, all 10 adversarial strategies, ≥0.95 threshold, 3+ creator-critic-revision cycles, explicit user approval gates before every irreversible action) not as a compliance obligation but as the designed response to the irreversibility classification of the CI deployment.

---

## Improvement Findings Table

| ID | Severity | Target Artifact / Section | Under-Stated Argument |
|----|----------|--------------------------|-----------------------|
| [SM-001-qg1-0626](#sm-001-qg1-0626) | **Critical** | ADR-001 § Regeneration Commit Determinism | Bit-identical SHA as tamper-detection mechanism (security argument), not stated in ADR-001 itself |
| [SM-002-qg1-0626](#sm-002-qg1-0626) | **Major** | ADR-002 § Loop-Safety Argument + L0 | Over-determined loop safety not foregrounded as the primary security headline |
| [SM-003-qg1-0626](#sm-003-qg1-0626) | **Major** | ADR-002 § Decision / Rationale | GITHUB_TOKEN eliminates attack-surface class (not merely narrows scope); structural vs. quantitative win |
| [SM-004-qg1-0626](#sm-004-qg1-0626) | **Major** | phase1-requirements.md § Stated Assumption: R-001 | R-001 decision tree is complete (both paths documented), but framed defensively as "risk to verify" |
| [SM-005-qg1-0626](#sm-005-qg1-0626) | Minor | phase1-requirements.md § REQ-002, L0 | 65% file-count margin not articulated as a forward-looking robustness argument |
| [SM-006-qg1-0626](#sm-006-qg1-0626) | Minor | ADR-001 § Consequences > Positive 1 + 2 | Provenance + idempotency interaction as a verifiable supply-chain integrity assertion |
| [SM-007-qg1-0626](#sm-007-qg1-0626) | Minor | phase1-requirements.md § WS-3: Security | Defense-in-depth architecture narrative not stated; REQ-019–023 presented as five independent requirements |
| [SM-008-qg1-0626](#sm-008-qg1-0626) | Minor | ADR-002 § Background / Rationale | version-bump.yml PAT counter-example is the most intuitive argument for the GITHUB_TOKEN choice but is buried in Background |

---

## Improvement Details

### SM-001-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Target Artifact** | `ADR-001-skeleton-derived-branch-strategy.md` |
| **Target Section** | § Regeneration Commit Determinism |
| **Affected Dimension** | Completeness, Evidence Quality |
| **Strategy Step** | Step 2 (Structural weakness) → Step 3 (Reconstruction) |

**Under-Stated Argument:**
The bit-identical commit SHA produced by Option A's metadata-pinning approach is presented in ADR-001 exclusively as a reliability/reproducibility property — "release replays and `workflow_dispatch` retries cannot drift the artifact" — and as support for the file-count acceptance test being "stable." This misses the primary security value of the property: **bit-identical SHA enables tamper detection.**

If any actor modifies the live `cowork-skeleton` branch between releases (amending the commit, altering files, injecting content), the resulting SHA will differ from the expected value produced by `regenerate(T)`. A maintainer, auditor, or CI job can verify integrity by re-running the generator against the same tag and comparing SHA outputs. This transforms Option A's idempotency claim from "convenient for re-runs" to "the branch is tamper-evident."

**Evidence — Original Content (ADR-001 § Regeneration Commit Determinism):**
> "Idempotency proof sketch: Given tag T resolving to source commit S with committer date D, the regenerated commit's preimage `(tree, parent=S, identity, author_date=D, committer_date=D, message(T,S))` is a pure function of T. Therefore `regenerate(T)` is referentially transparent and yields one fixed SHA; re-running T... reproduces it exactly."

> "True, verifiable idempotency — pinned metadata yields a bit-identical SHA on re-run; release replays and `workflow_dispatch` retries cannot drift the artifact." (Consequences > Positive #2)

**Evidence — Where the security argument exists but only in requirements:**
> "Non-determinism prevents tamper detection (different SHAs on re-run cannot be distinguished from interference)" (NFR-001 Rationale in phase1-requirements.md)

The security argument is correct in the requirements document but absent from ADR-001. A C4 reviewer reading ADR-001 in isolation would see reliability arguments but no security argument for the metadata-pinning approach.

**Strengthened Version (SM-001 addition to ADR-001 § Consequences > Positive or § Regeneration Commit Determinism):**
> "[SM-001] **Tamper-detection:** because `regenerate(T)` is a pure function, the expected commit SHA for any given release tag can be computed independently. A SHA mismatch on the live `cowork-skeleton` branch — detectable by running the generator against the same tag and comparing — indicates in-place interference. This makes the branch tamper-evident without additional attestation infrastructure, completing the supply-chain security argument for Option A."

**Recommendation to Creator:**
Add one explicit paragraph to ADR-001's Consequences > Positive #2 (or as a separate item in Regeneration Commit Determinism) stating the tamper-detection argument in its own right: given that `regenerate(T)` is referentially transparent, the expected SHA is computable from the tag alone, and a SHA mismatch on the live branch is detectable interference. This closes the gap that a C4 adversary would exploit ("your idempotency story is a reliability story, not a security story").

---

### SM-002-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target Artifact** | `ADR-002-ci-token-push-strategy.md` |
| **Target Section** | § L0: Executive Summary + § Loop-Safety Argument |
| **Affected Dimension** | Methodological Rigor, Evidence Quality |
| **Strategy Step** | Step 2 (Structural weakness — argument buried) → Step 3 |

**Under-Stated Argument:**
ADR-002's loop-safety argument is technically correct but structured to progressively reveal its strongest claim rather than leading with it. The L0 Executive Summary mentions loop-safety and states that `GITHUB_TOKEN` gives "free loop-safety," but does not state the over-determination property. The Loop-Safety Argument section (body) does state three independent guarantees but does not use the word "over-determined" or make explicit that failure of any single guarantee leaves two others intact.

The strongest framing — and the one most relevant to a C4 adversarial review — is: **loop-safety here is over-determined; three independent invariants each individually prevent the loop, so a single misconfiguration cannot open the risk.** This is qualitatively different from "we have three mitigations" — it means mitigations 1 and 2 continue to hold even if mitigation 3 fails, and every pairing of the three individually suffices.

**Evidence — Original Content (ADR-002 § Loop-Safety Argument):**
> "Loop-safety is over-determined — three independent guarantees each individually prevent an infinite regenerate-push loop (research §L2 ¶3). For a C4 irreversibility argument this is stated as a conjunction of three documented invariants: 1. Trigger shape... 2. Listener shape... 3. Credential shape (this ADR)."

The word "over-determined" does appear in the body section, which is good. The gap is that the L0 Executive Summary does not lead with this, and the body section does not explicitly state the corollary: "any single misconfiguration still leaves two others intact." A C4 reviewer reading quickly might miss the significance of the over-determination claim.

**Strengthened Version (SM-002 addition to ADR-002 § L0 Executive Summary):**
> "[SM-002] The skeleton push's loop-safety is over-determined: **three independent invariants each individually prevent an infinite regenerate-push loop**, so any single misconfiguration cannot reopen the risk — two protections remain. Option A (GITHUB_TOKEN) supplies the third guarantee (credential shape) for free; Option B (PAT) would remove it, leaving only two."

**Recommendation to Creator:**
Add one sentence to the L0 Executive Summary making the over-determination property explicit: any single one of the three guarantees (trigger shape, listener shape, credential shape) individually prevents the loop, so failure of one leaves two intact. Then add the corollary to the Loop-Safety Argument section: "The three-way conjunction means an adversary would need to simultaneously defeat all three invariants to create a loop — a compound failure that dramatically exceeds the probability of any single failure."

---

### SM-003-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target Artifact** | `ADR-002-ci-token-push-strategy.md` |
| **Target Section** | § Decision / Rationale + § Consequences > Positive |
| **Affected Dimension** | Methodological Rigor, Evidence Quality |
| **Strategy Step** | Step 2 (Presentation weakness — framing as quantitative vs. qualitative difference) |

**Under-Stated Argument:**
ADR-002 argues that `GITHUB_TOKEN` is "both safer and sufficient" by comparing credential lifetime (job-expiring vs. long-lived) and scope. The current framing presents this as a quantitative difference in risk exposure. The stronger framing is that the choice **structurally eliminates an entire attack-surface class**, not merely reduces it.

A Personal Access Token (PAT), however narrow its scope, introduces all of: (1) a theft window extending from creation to expiry, (2) a rotation failure mode (expired or forgotten PAT blocks all releases), (3) an expiry monitoring requirement (a `pat-monitor.yml`-style workflow), and (4) the possibility of accidentally triggering downstream workflows. `GITHUB_TOKEN` eliminates all four attack vectors simultaneously, not by narrowing the blast radius of each but by making the entire class structurally non-applicable. "Zero long-lived secret" is a qualitatively different security posture than "narrower-scoped long-lived secret."

ADR-002 implicitly captures this in "Zero maintenance (c-104)" and "Zero secret-management toil" in the Positive Consequences, but these are framed as operational convenience rather than as the security argument they represent: no long-lived credential means no long-lived credential threat.

**Strengthened Version (SM-003 addition to ADR-002 § Rationale):**
> "[SM-003] The GITHUB_TOKEN choice is not a marginal scope reduction relative to a PAT — it is **structural attack-surface elimination**. A PAT, regardless of scope, introduces a multi-step attack surface: credential theft during the storage window, rotation failure if the PAT expires unnoticed, and accidental downstream triggering if loop-safety logic fails. GITHUB_TOKEN eliminates all three simultaneously by making the credential non-persistent. The security argument is not 'narrower blast radius' but 'this entire attack-surface class does not exist.'"

**Recommendation to Creator:**
Add one paragraph to the Rationale section that frames the GITHUB_TOKEN choice as structural rather than quantitative. The argument: PAT introduces a long-lived credential lifecycle (theft, rotation, monitoring, mis-trigger risk); GITHUB_TOKEN eliminates the lifecycle entirely; this is a categorical difference, not a degree difference. Reference the Consequences > Positive list to show that "Zero secret-management toil" has a security dimension (no rotation failure mode) beyond its operational convenience dimension.

---

### SM-004-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target Artifact** | `phase1-requirements.md` |
| **Target Section** | § Stated Assumption: R-001 + § L0: Executive Summary |
| **Affected Dimension** | Completeness, Methodological Rigor |
| **Strategy Step** | Step 2 (Structural weakness — defensive vs. strongest framing) |

**Under-Stated Argument:**
R-001 is presented with a defensive framing: "This is the project's primary unresolved risk. It MUST be empirically verified before Phase 5." This is accurate but understates the strength of the risk management approach.

The key structural argument missing is: **R-001 is a binary-resolution risk with a direct falsification test and both paths fully documented.** The two hypotheses (clean-clone tree vs. local working directory) are clearly distinguishable because they differ by a 14:1 ratio (1,744 vs. 24,636 files). The verification test (clean clone of `main` = reproduces the CoWork error; clean clone of stripped branch = resolves it) directly tests the hypothesis at issue, not a proxy. If hypothesis (a) holds, the strategy proceeds as documented. If hypothesis (b) holds, the strategy pivots to local-plugin configuration guidance with explicit user escalation per H-02. The decision tree is complete.

The current framing emphasizes the uncertainty; the strongest framing emphasizes the completeness of the resolution mechanism. A C4 adversary will point at R-001 and say "your entire strategy rests on an unverified assumption." The answer is not "you're right, that's a risk" but "the verification test directly and definitively resolves which hypothesis holds, and we have documented responses for both outcomes, and no irreversible action occurs until the test completes."

**Evidence — Original Content (Stated Assumption: R-001):**
> "This is the project's primary unresolved risk. It MUST be empirically verified before Phase 5 (skeleton script implementation) begins. The entire skeleton strategy depends on it."

This framing, while honest, does not state the completeness of the decision tree.

> "Fallback: Hypothesis (b) confirmed (local working-directory count): strategy pivots from branch-stripping to local-plugin configuration guidance."

The fallback IS documented but appears as the last row of a table, not framed as "the decision tree is complete and covered."

**Strengthened Version (SM-004 addition to R-001 section, after Fallback row):**
> "[SM-004] **Decision Tree Completeness:** R-001 resolves as a binary test with documented responses for both outcomes. The two hypotheses differ by a 14:1 file ratio (1,744 clean-clone vs. 24,636 local-directory), making the empirical test direct and unambiguous: if the CoWork error reproduces on a clean clone of `main` and resolves on a stripped clone, hypothesis (a) holds and the strategy proceeds. If the error does not reproduce on a clean clone of `main`, hypothesis (b) holds and the strategy pivots per the Fallback above. No irreversible CI action is authorized until this binary test completes (AG-01). R-001 is therefore a controlled branching condition, not an existential threat to the project."

**Recommendation to Creator:**
Add a "Decision Tree Completeness" paragraph to the R-001 section that names the binary nature of the test and explicitly states both outcomes and their responses. Quantify the 14:1 ratio to reinforce that the two hypotheses are clearly distinguishable. Reframe R-001 not as "uncertainty we must resolve" but as "a controlled binary test with pre-designed responses for each outcome, time-bounded to before Phase 5."

---

## Minor Findings

### SM-005-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target Artifact** | `phase1-requirements.md` |
| **Target Section** | § L0: Executive Summary, § REQ-002 rationale |
| **Affected Dimension** | Evidence Quality |

**Under-Stated Argument:** The design targets ~1,744 tracked files against a ~5,000-file limit, leaving approximately 3,256 files of headroom — 65% of the ceiling. This headroom argument is never explicitly stated. Articulating it would strengthen the robustness case: even if retained directories (`.claude/`, `skills/`, `src/`) grow substantially across several releases, the strategy remains well within the limit without requiring additional stripping. The REQ-006 hard-fail assertion provides a safety net, but the affirmative headroom argument would pre-empt the critique "what if more files accumulate?"

**Recommendation:** Add one sentence to L0 or REQ-002 Rationale: "The ~1,744 file target leaves approximately 3,256 files of headroom (~65% of the ceiling) against future growth in retained directories; REQ-006's hard-fail assertion provides a CI-visible safety net if this margin is ever approached."

---

### SM-006-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target Artifact** | `ADR-001-skeleton-derived-branch-strategy.md` |
| **Target Section** | § Consequences > Positive #1 and #2 |
| **Affected Dimension** | Internal Consistency, Traceability |

**Under-Stated Argument:** "Auditable provenance" (Positive #1) and "True, verifiable idempotency" (Positive #2) are listed as separate consequences, but their interaction is what produces the supply-chain integrity claim in REQ-022. Specifically: `git diff v{N}..cowork-skeleton -- ':!projects/'` returns zero diff is the REQ-022 acceptance criterion, and this works precisely because the skeleton commit's parent is the tagged release commit (provenance) AND the commit is bit-identical on re-run (idempotency). Neither property alone fully delivers the REQ-022 verifiability guarantee; the conjunction does.

**Recommendation:** Add a note to ADR-001 Consequences > Positive (or a cross-reference in the Regeneration Commit Determinism section) explicitly connecting the provenance+idempotency pair to REQ-022 and supply-chain integrity: "The conjunction of (1) and (2) is what enables the REQ-022 acceptance criterion: `git diff v{N}..cowork-skeleton -- ':!projects/'` returns zero diff, providing a reproducible, auditable supply-chain integrity assertion."

---

### SM-007-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target Artifact** | `phase1-requirements.md` |
| **Target Section** | § WS-3: Security Requirements (opening) |
| **Affected Dimension** | Completeness, Methodological Rigor |

**Under-Stated Argument:** REQ-019 through REQ-023 are presented as five independent security requirements without a unifying narrative. The strongest framing is that they collectively implement a defense-in-depth architecture with no single point of failure: no secret in logs (REQ-019) + least-privilege scope (REQ-020) + CI-owned posture (REQ-021) + supply-chain verifiability (REQ-022) + no self-trigger (REQ-023). A single failure of any one does not compromise all security properties simultaneously. This is an appropriate C4 security posture but the "defense-in-depth architecture" framing is not stated.

**Recommendation:** Add one introductory sentence to WS-3: "The following five requirements implement a defense-in-depth security architecture: no single failure mode simultaneously compromises secret confidentiality (REQ-019), token scope (REQ-020), branch integrity (REQ-021/REQ-022), and loop-safety (REQ-023)."

---

### SM-008-qg1-0626

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target Artifact** | `ADR-002-ci-token-push-strategy.md` |
| **Target Section** | § Background (sub-section "Contrast") → should be in § Rationale |
| **Affected Dimension** | Actionability, Evidence Quality |

**Under-Stated Argument:** The contrast with `version-bump.yml` — where a PAT is deliberately used because the tag push *must* trigger `release.yml` — is the most concrete and intuitive argument for GITHUB_TOKEN. It makes the counter-intuitive choice immediately legible: "PAT here has the opposite effect of what we want" is a much stronger argument than "PAT violates least-privilege." The contrast currently appears in the Background section (third bullet), subordinate to the token description. Moving it to lead the Rationale section would anchor the decision on its most compelling evidence.

**Recommendation:** Elevate the `version-bump.yml` counter-example to the first sentence of the Rationale section: "The clearest reason to prefer GITHUB_TOKEN over a PAT is the repository's own `version-bump.yml`: that workflow uses `VERSION_BUMP_PAT` precisely *because* it wants its tag push to trigger `release.yml`. The skeleton requires the opposite — triggering nothing — making `GITHUB_TOKEN` the technically correct choice, not merely the safer default."

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-001 fills the tamper-detection argument absent from ADR-001; SM-004 completes the R-001 decision-tree articulation; SM-007 adds the defense-in-depth narrative to WS-3 |
| Internal Consistency | 0.20 | Neutral | All three deliverables are internally consistent; no improvements needed; SM-006 adds cross-artifact traceability but does not address an inconsistency |
| Methodological Rigor | 0.20 | Positive | SM-002 foregrounds the over-determination structure; SM-003 upgrades the GITHUB_TOKEN argument from quantitative to structural; SM-004 reframes R-001 from defensive to complete-decision-tree |
| Evidence Quality | 0.15 | Positive | SM-001 provides the before/after for tamper-detection evidence; SM-005 quantifies the file-count headroom argument; SM-008 positions the PAT counter-case more prominently |
| Actionability | 0.15 | Positive | All eight findings carry specific, targeted recommendations the creator can apply without restructuring the deliverables |
| Traceability | 0.10 | Positive | SM-006 explicitly connects ADR-001 Consequences #1+#2 to REQ-022; SM-001 cross-links ADR-001 and NFR-001; SM-004 connects R-001 to the AG-01 approval gate sequence |

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 1
- **Major:** 3
- **Minor:** 4
- **Protocol Steps Completed:** 6 of 6

---

## Best Case Scenario

**Ideal conditions for this design package's success:**

1. R-001 resolves as hypothesis (a): the CoWork limit applies to the clean-clone tracked-file tree, and a clean clone of `main` reproduces the error while a stripped clone resolves it.
2. The bit-identical SHA assertion is enforced in CI with a comparison step so the tamper-detection property is operationally active, not just theoretically possible.
3. Option B (orphan fallback) is monitored passively during Phase 6 by measuring actual clone timing on the generated branch; the fallback decision rule is pre-specified (e.g., trigger Option B if measured clone time exceeds 90 seconds on a reference network condition).
4. The three loop-safety guarantees are treated as individually sufficient (not just collectively sufficient) in the CI audit checklist, so a future change to one does not silently reduce safety below the documented level.

**Key assumptions that must hold for the design to be correct:**
- GitHub's documented `GITHUB_TOKEN` non-retrigger behavior holds under the repo's actual push event configuration (PRIMARY source: GitHub Docs; risk: policy change would remove guarantee 3, leaving 1 and 2 intact).
- The CoWork installation mechanism materializes only tracked files from the tip commit (not gitignored or local artifacts); confirmed by research Q3 but R-001 empirical verification before Phase 5 is required.
- Static stub content in `projects/README.md` (no generated timestamps or run IDs) is enforced in STORY-002; dynamic stub content would break tree determinism and invalidate the bit-identical SHA.

**Confidence Assessment:** HIGH for the core approach. The technique is a direct extension of the repository's established `gh-pages` pattern; the token choice has strong primary-source support; the code-grounded Q4 findings eliminate uncertainty about the stub requirement. The one material uncertainty (R-001) is binary, time-bounded, and pre-resolved per the design.

---

*Execution: adv-executor | Strategy: S-003 Steelman Technique | Template: `.context/templates/adversarial/s-003-steelman.md` v1.0.0*
*H-15 Self-Review: Applied before write — all findings have specific evidence from deliverables; severity classifications are justified; SM-NNN identifiers are consistent; summary table matches detailed findings; no findings omitted per P-022.*
*SSOT: `.context/rules/quality-enforcement.md`*
*Date: 2026-06-26*

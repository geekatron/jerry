# S-014 LLM-as-Judge Scoring Report — Round 1

> **Agent:** adv-scorer v1.0.0
> **Strategy:** S-014 LLM-as-Judge
> **Deliverable:** EN-002 HARD Rule Budget Enforcement Implementation
> **Criticality:** C4 (user-requested tournament)
> **Tournament Threshold:** >= 0.95
> **Scoring Round:** R1 (first iteration)
> **Date:** 2026-02-21
> **Leniency Bias Counteraction:** Applied — adjacent scores resolved to LOWER

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Files Read](#files-read) | Deliverable artifacts assessed |
| [Scoring Summary](#scoring-summary) | Dimension scores and weighted composite |
| [Dimension Assessments](#dimension-assessments) | Per-dimension justification and improvement guidance |
| [Finding Classification Map](#finding-classification-map) | How tournament findings map to dimension scores |
| [Verdict](#verdict) | PASS / REVISE / REJECTED with rationale |

---

## Files Read

All mandatory files were read prior to scoring:

1. `projects/PROJ-007-agent-patterns/work/EN-002-hard-rule-budget-enforcement/en-002-implementation-summary.md`
2. `projects/PROJ-007-agent-patterns/work/EN-002-hard-rule-budget-enforcement/TASK-028-measure-enforcement-effectiveness/enforcement-effectiveness-report.md`
3. `.context/rules/quality-enforcement.md` (version 1.4.0, post-EN-002)
4. `scripts/check_hard_rule_ceiling.py`
5. `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`

---

## Scoring Summary

| Dimension | Weight | Raw Score (1-5) | Weighted |
|-----------|--------|-----------------|---------|
| Completeness | 0.20 | 3 | 0.60 |
| Internal Consistency | 0.20 | 3 | 0.60 |
| Methodological Rigor | 0.20 | 3 | 0.60 |
| Evidence Quality | 0.15 | 3 | 0.45 |
| Actionability | 0.15 | 3 | 0.45 |
| Traceability | 0.10 | 4 | 0.40 |

**Weighted Composite Score: 3.10 / 5.00 = 0.620**

> Composite computed as: sum of (raw_score / 5.0 * weight) across all dimensions.

---

## Verdict

**REJECTED** (score 0.620 < 0.850 threshold)

This is not a close call. The deliverable fails the standard C2+ quality gate (0.92) by a large margin, and falls far below the C4 tournament threshold (0.95). Six critical findings — including a structurally blocked dependency (C-02), an exploitable injection attack surface (C-06), a pre-commit-only CI gate with documented bypass (C-01), zero headroom against the ceiling the implementation was designed to create (C-04), and a self-referential ceiling mechanism that nullifies the gate (M-08) — constitute fundamental design defects, not refinement opportunities. The deliverable achieves its stated metrics (84% L2 coverage, 25 rules, tests passing) while leaving the underlying enforcement reliability materially compromised.

---

## Dimension Assessments

### 1. Completeness — Score: 3 / 5 (Adequate)

**Rubric application:** Are ALL scope items addressed? Any gaps?

**What is present:** All five DEC-001 decisions (D-001 through D-005) have corresponding implementation artifacts. The L2 engine reads 9 rule files (was 1). The HARD rule count moved from 31 to 25. The L5 gate script exists and is wired into `.pre-commit-config.yaml`. The effectiveness report captures pre/post metrics. Tests pass at 3377/3377.

**Material gaps that prevent score 4:**

- **C-01 (Scope gap — L5 enforcement coverage):** The L5 gate is described as "CI enforcement" but exists only as a pre-commit hook. No GitHub Actions workflow file was created or modified. The implementation summary states "L5 CI gate: Active" but CI (continuous integration in a server-enforced pipeline) and pre-commit hooks (client-side, bypassable with `--no-verify`) are different things. The deliverable's own scope item D-004 ("Add L5 CI enforcement gate preventing silent ceiling breaches") is only half-implemented. Silent breaches via server-side push remain unaddressed.

- **C-02 (Scope gap — EN-001 blocking state):** The implementation summary acknowledges EN-001 as an active risk: "TASK-016 deferred until consolidation creates headroom." However, the exception mechanism caps at N=3 additional slots while EN-001 requires N=4 (H-32..H-35). There is no compliant path for EN-001 to proceed. The deliverable does not acknowledge this as a structural block or propose a resolution path (further consolidation candidates, rule demotion candidates, etc.). A deliverable that creates a structural dependency block without a resolution path has a completeness gap against its own motivating purpose.

- **M-01 (Scope gap — retired ID tombstoning):** Rule IDs H-08, H-09, H-27, H-28, H-29, H-30 were retired. No cross-reference audit was performed. No tombstone or redirect mechanism was added to governance documents or the HARD Rule Index. External references to retired IDs will silently fail or produce confusion.

- **M-11 (Factual gap — count discrepancy):** EN-002.md targets 24 HARD rules post-consolidation; actual delivered count is 25. The implementation summary does not acknowledge this discrepancy. A deliverable that misreports its own primary metric against its own specification has a completeness gap.

**Why not score 2:** The five core decisions are all present and the primary metrics are directionally correct. The gaps are serious but the majority of scope items are addressed.

**Improvement guidance for score 4+:**
- Add a GitHub Actions workflow step that runs `check_hard_rule_ceiling.py` on every push to main and on all PRs. Remove the "CI enforcement" claim until this exists.
- Either: (a) identify 2+ consolidation candidates that would create N>=4 headroom for EN-001, or (b) formally classify EN-001 as BLOCKED with an explicit resolution path documented in the worktracker.
- Add a `## Retired Rule IDs` section to quality-enforcement.md listing H-08, H-09, H-27-H-30 with redirect to their absorbing compound rules.
- Reconcile the 24 vs 25 count discrepancy: update EN-002.md specification OR document the deviation with justification.

---

### 2. Internal Consistency — Score: 3 / 5 (Adequate)

**Rubric application:** Do all documents, code, and tests agree? Any contradictions?

**What is consistent:** The HARD Rule Index in quality-enforcement.md (version 1.4.0) lists 25 rules, matching the L5 gate output ("PASS: HARD rule count = 25, ceiling = 25"). The Two-Tier Enforcement Model table accounts for all 25 rules (21 Tier A + 4 Tier B). The L2 engine reads the directory and its docstring reflects the directory-based approach. The pre-commit hook configuration exists and references the correct script.

**Material inconsistencies that prevent score 4:**

- **C-01 / M-02 (Docstring inconsistency):** The `generate_reinforcement` method docstring in `prompt_reinforcement_engine.py` reads: *"Reads the quality-enforcement.md file, extracts L2-REINJECT markers..."* — this describes the old single-file behavior. The implementation now reads all `.md` files in the rules directory. The method's own docstring contradicts the implementation.

- **M-08 (Self-referential ceiling — structural inconsistency):** The L5 gate reads the ceiling value from quality-enforcement.md and fails if `rule_count > ceiling`. Design decision 5 in the implementation summary states: "The gate automatically adapts if the ceiling is temporarily expanded via the exception mechanism." This is correct — but the same property means that editing the ceiling constant in quality-enforcement.md causes the gate to pass at any rule count. The gate is described as providing "deterministic enforcement immune to context rot," but a motivated editor can change a single integer to nullify it. This is not acknowledged as a limitation; it is presented as a feature. Documents claim stronger enforcement than the mechanism actually provides.

- **M-11 (Specification vs delivery count):** EN-002 specification targets 24 rules; delivered count is 25. This contradiction between specification and outcome is unacknowledged in the implementation summary. The implementation summary's own verification table states "25" without noting the deviation from the stated target.

- **C-05 (Scope claim vs implementation — trigger inconsistency):** The implementation summary states the L5 gate "prevents silent ceiling breaches." The pre-commit hook is configured to trigger on changes to `quality-enforcement.md` only. New H-rules added directly to other rule files (e.g., skill-standards.md or coding-standards.md) would not trigger the gate. The "prevents silent ceiling breaches" claim is inconsistent with the actual trigger scope.

- **M-04 (L2 content vs rule content inconsistency):** The architecture-standards.md L2-REINJECT marker covers only the domain import sub-rule of H-07 (the consolidated compound rule covering domain imports, application imports, and composition root). The marker content does not reflect the full scope of the compound rule H-07 as defined in the HARD Rule Index.

**Why not score 2:** The primary consistency surface (rule count, tier model, test results) holds together. The inconsistencies are real but concentrated in boundary cases (docstrings, trigger scope claims, one count discrepancy).

**Improvement guidance for score 4+:**
- Update `generate_reinforcement` docstring to describe directory-based reading.
- Add a documented limitation note to the L5 gate description: "Gate triggers only on quality-enforcement.md changes; rules added to other files require manual gate execution."
- Update `.pre-commit-config.yaml` to also trigger on changes to any `.context/rules/*.md` file.
- Acknowledge the 24→25 count deviation explicitly in the implementation summary.
- Expand the architecture-standards.md L2-REINJECT marker to cover all three sub-items of compound H-07.

---

### 3. Methodological Rigor — Score: 3 / 5 (Adequate)

**Rubric application:** Was the approach sound? Were alternatives considered?

**What is methodologically sound:** The two-discovery, five-decision structure (DISC-001/DISC-002 → DEC-001) provides a clear problem-solution chain. The ceiling derivation draws on three independent constraint families (cognitive load, enforcement coverage, governance burden). The directory-glob approach for L2 engine expansion is forward-compatible and backward-compatible. Fail-open behavior is preserved intentionally with documented rationale. The Two-Tier Enforcement Model (Tier A / Tier B) provides a principled classification of rules by enforcement reliability.

**Material rigor gaps that prevent score 4:**

- **C-06 (Attack surface — methodology gap):** The L2 engine reads all `.md` files in the `.claude/rules/` directory and injects their L2-REINJECT marker content verbatim into every user prompt. No sanitization of marker content is performed. The implementation summary does not discuss injection risk. For an enforcement mechanism operating on governance rules, the absence of any analysis of the injection attack surface is a methodological gap. The strategy catalog explicitly excluded S-015 (Prompt Adversarial Examples) due to "adversarial prompt injection concern," yet the L2 engine creates exactly the attack surface that concern addresses.

- **C-03 (Reversion deadline — methodology gap):** The exception mechanism specifies a 3-month reversion deadline, but the mechanism description acknowledges no technical enforcement. The mechanism is entirely procedural. For a system designed to prevent silent ceiling breaches, an exception mechanism whose own expiry is also undetected is methodologically inconsistent. The implementation notes this risk in the summary's risk table but classifies it as "Low" without justification; the FMEA analysis assigned it the highest RPN (336) of any finding in the tournament.

- **M-05 (Ceiling derivation — rationalization concern):** Finding M-05 identifies that the ceiling of 25 was selected because it matches the achievable post-consolidation count, not because the constraint families independently converged on 25. The cognitive-load family states "20-25 rules is the practical upper bound" — a five-rule range. The enforcement coverage family is budget-dependent and circular (budget was set to accommodate current markers). The governance burden family is qualitative. The derivation is presented with higher confidence than the evidence supports. DEC-005 defers empirical validation with no concrete follow-up timeline.

- **M-09 (Exception stacking — methodology gap):** The exception mechanism caps each exception at +3 slots but places no bound on the number of sequential exceptions. Three sequential exceptions would expand the effective ceiling to 34 — functionally undoing the consolidation. This was not analyzed.

- **M-10 (Token budget exhaustion — methodology gap):** Any rule file can exhaust the 850-token L2 budget with a single high-rank marker, suppressing all subsequent constitutional reinforcement. The rank collision detection (M-06) is also absent. The engine's priority ordering is entirely dependent on marker authors not creating adversarial or accidentally competing configurations.

**Why not score 2:** The problem decomposition, decision chain, and core design choices are sound. The gaps are in adversarial analysis and boundary case methodology, not in the fundamental approach.

**Improvement guidance for score 4+:**
- Add a sanitization step in `_parse_reinject_markers` that rejects marker content matching injection patterns (e.g., content containing `<!--`, `-->`, `IGNORE PREVIOUS`, instruction override phrases). Document the threat model.
- Reclassify the exception reversion risk from "Low" to "High" in the risk table, consistent with FMEA findings (highest RPN). Add a worktracker task to implement automated reversion tracking (e.g., a CI gate that checks for expired exceptions).
- Add an explicit bound on sequential exception stacking (e.g., maximum 1 active exception at a time) to the exception mechanism definition.
- Add rank uniqueness validation to the engine: warn or fail when two markers share the same rank across files.
- Document the token budget exhaustion scenario in the engine docstring and add a test case for it.

---

### 4. Evidence Quality — Score: 3 / 5 (Adequate)

**Rubric application:** Are claims backed by data? Are measurements valid?

**What is evidenced:** The pre/post comparison is concrete: specific numbers for rule count (31→25), L2 marker count (8→16), L2 coverage (32%→84%), and token utilization (559/850 = 65.8%). The effectiveness report structure is methodologically appropriate. Tests pass at 3377/3377 with an explicit breakdown by suite. The L5 gate produces machine-readable output that is captured in the summary.

**Material evidence quality gaps that prevent score 4:**

- **M-03 (Stale token metadata — evidence validity):** The L2-REINJECT markers include a `tokens` field (e.g., `tokens=50`, `tokens=90`, `tokens=100`). The engine explicitly ignores these values and recomputes estimates. The implementation summary does not audit whether the declared token values in existing markers are accurate. The token metadata, presented as documentation, is systematically unreliable and no reconciliation is performed.

- **M-07 (Cognitive load claim — unvalidated evidence):** The ceiling derivation's primary constraint family — "20-25 rules is practical upper bound for LLM reliable enforcement" — has no empirical basis cited. This is the load-bearing claim for the ceiling derivation. The implementation summary acknowledges DEC-005 deferred measurement but provides no timeline, no measurement methodology, and no definition of what "enforcement failure" would look like. A ceiling derived from a claim that has never been tested is not strongly evidenced.

- **C-04 (Zero headroom — evidence of goal non-achievement):** The stated purpose of EN-002 (as described in the project context) was to create headroom for EN-001. The effectiveness report explicitly states "Zero headroom: 25/25 rules at ceiling — no room for EN-001 H-32..H-35 without exception mechanism." The deliverable's own evidence demonstrates it did not achieve its primary motivating objective. The implementation summary notes this as a risk but not as a goal failure.

- **M-08 (Self-referential gate — evidence validity):** The L5 gate output ("PASS: HARD rule count = 25, ceiling = 25, headroom = 0 slots") is cited as verification evidence. However, because the gate reads its ceiling from the same file it enforces, this output does not constitute independent verification. The "evidence" of gate passage is partially circular.

- **Structural vs behavioral metrics:** The effectiveness metrics are all structural (coverage percentages, token counts, rule counts). No behavioral measurement is provided — no assessment of whether enforcement actually improved (e.g., did context rot incidents decrease? were rules actually applied more consistently?). This is noted in the tournament observations but not in the effectiveness report's conclusions section.

**Why not score 2:** The measurements that are present are accurately computed and honestly reported. The gaps are in independence of evidence and validation of key assumptions, not in fabricated or misrepresented data.

**Improvement guidance for score 4+:**
- Run a reconciliation pass on all L2-REINJECT marker `tokens` values against the engine's actual estimates. Update or deprecate the field if it cannot be kept current.
- For the cognitive load claim: cite at least one empirical study or commit to a concrete measurement methodology with a defined timeline (not "DEC-005 deferred").
- Explicitly acknowledge in the effectiveness report conclusions that EN-001 headroom was not created and classify this as a goal shortfall rather than a known risk.
- Supplement the structural metrics with at least one behavioral indicator (e.g., H-rule compliance pass rate in recent PR reviews, frequency of rule-related rework).

---

### 5. Actionability — Score: 3 / 5 (Adequate)

**Rubric application:** Can the deliverable be used as-is? Are next steps clear?

**What works:** The L5 gate script can be run directly and produces unambiguous output. The L2 engine is deployed and operational (65.8% budget utilization). The HARD Rule Index in quality-enforcement.md is the correct SSOT. Tests pass. The Two-Tier Enforcement Model tells operators which rules have L2 protection and which rely on compensating controls.

**Material actionability gaps that prevent score 4:**

- **C-01 (L5 gate not actionable at CI level):** A developer who pushes directly via API, force-push, or with `--no-verify` bypasses the gate entirely. There is no server-side enforcement. The "L5 enforcement: Active" status in the effectiveness report implies a protection that does not actually protect in the described failure scenarios. The actionable protective layer is missing.

- **C-02 (EN-001 blocked with no actionable path):** TASK-016 is marked BLOCKED. The implementation summary says "Alternative: further consolidation to create headroom before adding new rules" but identifies no specific candidates for further consolidation. An operator reading this deliverable cannot take action to unblock EN-001 without additional analysis that the deliverable does not provide.

- **C-03 (Exception mechanism not operationally enforced):** The exception mechanism is defined in quality-enforcement.md but has no operational trigger. A 3-month reversion deadline that is tracked purely procedurally in a worktracker entry — with no automated reminder, no CI check for expired exceptions, no governance review — is not actionable enforcement. An operator following the mechanism in good faith would have no warning that the deadline is approaching.

- **M-06 (Forward compatibility gap):** The directory glob automatically enrolls new rule files without opt-in. An operator adding a new rule file to `.context/rules/` may unintentionally increase L2 token consumption, trigger rank collisions, or introduce injection content. There is no "what to do when adding a new rule file" guidance anywhere in the deliverable or its referenced documents.

- **C-06 (Injection attack surface not actionable):** The attack surface exists and is unmitigated. An operator who is aware of finding C-06 has no documented remediation to apply.

**Why not score 2:** The deliverable is deployable and the primary mechanisms function correctly. The actionability gaps are in edge cases, failure modes, and downstream workflow — not in core operation.

**Improvement guidance for score 4+:**
- Add a GitHub Actions workflow. Until server-side enforcement exists, change the effectiveness report language from "L5 enforcement: Active" to "L5 enforcement: Active (pre-commit only; server-side bypass possible)."
- Identify at least 2-3 consolidation candidates for creating EN-001 headroom. Add these as tasks in the worktracker with priority assignment.
- Add an automated exception expiry check: a CI gate that reads active exception ADRs and fails if any have passed their reversion deadline.
- Add a "Adding a New Rule File" section to the engine docstring and/or to quality-enforcement.md describing the rank assignment process, token budget impact assessment, and review requirement.

---

### 6. Traceability — Score: 4 / 5 (Strong)

**Rubric application:** Can every decision be traced to evidence and rationale?

**What is traceable:** The decision chain is clear and well-documented: DISC-001/DISC-002 → DEC-001 (D-001 through D-005) → TASK-022 through TASK-028. Each implementation file change in the summary table maps to a specific decision. The ceiling derivation is documented with three named constraint families. The Two-Tier Enforcement Model documents which rule is covered by which L2 source file and at what rank. Code references (EN-002, DEC-001 D-004, EN-705) appear in both script and engine docstrings. The implementation summary references version numbers and dates.

**Gaps that prevent score 5:**

- **M-11 (Untraced deviation):** The DEC-001 / EN-002.md specified 24 rules post-consolidation; 25 were delivered. This deviation from the specification is not traced to a decision or documented rationale. It appears to be an undetected error. A traceability gap at the primary deliverable metric is material.

- **M-05 (Ceiling value traceability gap):** The ceiling derivation traces to three constraint families, but does not trace to how the value 25 was selected from within the cognitive load family's stated range of "20-25." The precise value selection is not traceable to a specific calculation or decision. If the range had been 20-27, would the ceiling have been 27? The exact value appears to have been chosen post-hoc to match the achievable count.

- **Retired ID traceability:** H-08, H-09, H-27-H-30 were retired, but there is no tombstone entry in the HARD Rule Index or any governance document tracing these IDs to their absorbing compound rules. Future readers cannot determine whether, for example, H-08 (application layer isolation) is still enforced (it is — via H-07's compound rule) without extensive cross-referencing.

**Why score 4 rather than 3:** Traceability is the best-performing dimension. The decision chain, code references, and tier model documentation are genuinely strong. The gaps are real but smaller in number and severity than in other dimensions.

**Improvement guidance for score 5:**
- Document the 24→25 count deviation as a formal decision record (even a one-line entry in DEC-001 or a note in the implementation summary).
- Add a sentence to the ceiling derivation explaining how 25 was selected from the 20-25 cognitive load range (e.g., "25 selected as the upper bound of the cognitive load range because it matches the achievable post-consolidation count without further rule reduction").
- Add a retired rule ID table in the HARD Rule Index with columns: Retired ID, Former Rule, Absorbed Into.

---

## Finding Classification Map

This table maps the 30 tournament findings to the dimensions they penalized.

### Critical Findings (6)

| Finding | Primary Dimension Penalized | Score Impact |
|---------|----------------------------|-------------|
| C-01: CI gate pre-commit only; server-side bypass via --no-verify | Completeness, Internal Consistency, Actionability | Prevents 4 in all three |
| C-02: EN-001 blocked; exception mechanism caps at N=3, EN-001 needs N=4 | Completeness, Actionability | Prevents 4 in both |
| C-03: 3-month reversion deadline has no technical enforcement | Methodological Rigor, Actionability | Prevents 4 in both |
| C-04: Zero headroom; EN-002 did not create headroom it was designed to create | Evidence Quality, Completeness | Structural evidence of goal non-achievement |
| C-05: L5 gate triggers only on quality-enforcement.md changes; other files bypass | Internal Consistency, Completeness | Claim "prevents silent ceiling breaches" is false for new rules in other files |
| C-06: L2 marker content injection attack surface; verbatim injection with no sanitization | Methodological Rigor, Actionability | Unmitigated, unanalyzed attack surface in enforcement mechanism |

### Major Findings (selected)

| Finding | Primary Dimension Penalized |
|---------|-----------------------------|
| M-01: Retired IDs not audited or tombstoned | Completeness, Traceability |
| M-02: generate_reinforcement docstring stale | Internal Consistency |
| M-03: tokens metadata field parsed but never validated | Evidence Quality |
| M-04: L2 architecture-standards marker covers only one sub-item of compound H-07 | Internal Consistency |
| M-05: Ceiling derivation is rationalization of practical outcome | Methodological Rigor, Evidence Quality |
| M-06: No rank collision detection; forward-compat risk | Methodological Rigor, Actionability |
| M-07: Cognitive load claim unvalidated empirically | Evidence Quality |
| M-08: Self-referential ceiling — gate passes at any count if ceiling edited | Internal Consistency, Evidence Quality |
| M-09: Exception stacking unbounded | Methodological Rigor |
| M-10: Token budget exhaustion via high-rank marker injection | Methodological Rigor |
| M-11: Factual discrepancy: 24 (spec) vs 25 (delivered) | Internal Consistency, Traceability, Completeness |

### Minor Findings

Minor findings contributed to the overall score picture but did not individually prevent scores of 4 or 5. They collectively reinforce the "Adequate" rating over "Strong."

---

## Weighted Composite Calculation

| Dimension | Weight | Raw (1-5) | Normalized (÷5) | Weighted |
|-----------|--------|-----------|-----------------|---------|
| Completeness | 0.20 | 3 | 0.60 | 0.120 |
| Internal Consistency | 0.20 | 3 | 0.60 | 0.120 |
| Methodological Rigor | 0.20 | 3 | 0.60 | 0.120 |
| Evidence Quality | 0.15 | 3 | 0.60 | 0.090 |
| Actionability | 0.15 | 3 | 0.60 | 0.090 |
| Traceability | 0.10 | 4 | 0.80 | 0.080 |
| **TOTAL** | **1.00** | | | **0.620** |

**Composite Score: 0.620**

**C4 Threshold: 0.950**
**Standard C2+ Threshold: 0.920**
**Operational Band: REJECTED (< 0.850)**

---

## Verdict

**REJECTED**

**Score: 0.620 / 1.000**

The deliverable is significantly below both the standard quality gate (0.920) and the C4 tournament threshold (0.950). This is not a borderline result. The composite reflects five dimensions at "Adequate" (3/5), the ceiling for a deliverable carrying six critical unresolved findings.

### Why 3 and not 2 on the penalized dimensions

A score of 2 (Weak) is reserved for deliverables where significant gaps undermine the overall approach. In EN-002, the core implementation is directionally correct: L2 coverage did increase substantially (32%→84%), a principled ceiling was derived and documented, and the enforcement mechanism operates as described for the nominal case. The gaps are in the adversarial boundary, in the failure modes, and in the enforcement claims — serious deficiencies that prevent use in a C4 governance context, but not deficiencies that invalidate the core mechanism.

### Required for revision to reach REVISE band (0.85+)

A minimum revision must address all six critical findings:

1. **C-01:** Add a GitHub Actions workflow that runs `check_hard_rule_ceiling.py` on push/PR. Update all documentation to reflect "pre-commit only" limitation until server-side enforcement exists.

2. **C-02:** Either (a) identify and execute consolidation sufficient to create N=4 headroom, or (b) formally document EN-001 as BLOCKED with a specific resolution plan. The exception mechanism must be updated to support N=4 or the mechanism's limitation must be disclosed in EN-002.

3. **C-03:** Add an automated expiry checker for the exception mechanism. A worktracker-only deadline with no technical enforcement is insufficient for a C4 governance control.

4. **C-04:** Reconcile whether EN-002 succeeded at its motivating purpose. If zero headroom is the intended outcome, document why. If it is a failure, classify it explicitly and define the path forward.

5. **C-05:** Update the pre-commit hook trigger to include all `.context/rules/*.md` files. Update the enforcement description to accurately reflect which edits trigger the gate.

6. **C-06:** Add marker content sanitization to the L2 engine. Define a threat model for the injection attack surface and document it in the engine's docstring.

### Required for revision to reach PASS band (0.95+ at C4)

In addition to all six critical items, a C4 pass requires the following major findings to be resolved:

- **M-01:** Tombstone retired rule IDs.
- **M-02:** Fix stale docstring.
- **M-03:** Reconcile token metadata with computed estimates, or deprecate the field.
- **M-05:** Strengthen ceiling derivation with empirical grounding or tighten the range to a single justified value.
- **M-08:** Add an independent ceiling constant or a hash-based verification step that prevents the self-referential bypass.
- **M-09:** Add explicit sequential exception bound.
- **M-11:** Reconcile 24 vs 25 specification deviation with a formal decision record.

At C4, "at most minor residual issues" is the standard. The current gap between 0.620 and 0.950 represents substantial rework across all dimensions.

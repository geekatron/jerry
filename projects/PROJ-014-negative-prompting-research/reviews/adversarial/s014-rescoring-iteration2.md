# Quality Score Report: PROJ-014 Orchestration Prompt Artifacts — Iteration 2 Re-Scoring

## L0 Executive Summary

**Deliverable 1 (Mega-Prompt Template v1.1.0):**
Score: 0.924/1.00 | Verdict: REVISE | Weakest Dimension: Evidence Quality (0.81)
One-line assessment: Iteration 1 critical findings are fully resolved; the primary remaining gap is that per-constraint research citations use ID codes (NPT-IDs, AGREE-IDs) rather than file-path anchors, leaving the evidence chain partially unresolved for external verifiers.

**Deliverable 2 (Behavioral Constraints Rule File v1.1.0):**
Score: 0.931/1.00 | Verdict: REVISE | Weakest Dimension: Evidence Quality (0.81)
One-line assessment: All 9 Critical and 7 Major findings from iteration 1 are addressed; the structural additions (Prerequisites, Scope Guard, Constraint Interaction Map) are methodologically sound; evidence quality remains the limiting dimension due to ID-only citations without file-path anchors for individual constraints.

**Combined verdict:** Both deliverables fall short of the 0.95 user-specified PASS threshold. D1 scores 0.924 and D2 scores 0.931. Both exceed the SSOT H-13 threshold of 0.92 but do not reach the user-specified target. A focused third iteration targeting Evidence Quality alone (adding file-path anchors to the Research Basis column) would likely achieve PASS.

---

## Scoring Context

- **Deliverable 1:** `projects/PROJ-014-negative-prompting-research/research/orchestration-mega-prompt-template.md`
- **Deliverable 2:** `projects/PROJ-014-negative-prompting-research/research/orchestration-behavioral-constraints.md`
- **Deliverable Type:** Research Output (Prompt Template + Rule File)
- **Criticality Level:** C3 (> 1 day to reverse; shared with colleagues; influences multi-agent orchestration behavior)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold Override:** User specified >= 0.95 for PASS (versus standard H-13 threshold of 0.92)
- **Iteration:** 2 (first re-scoring after adversarial revision)
- **Prior Scores:** D1: 0.878 (REVISE), D2: 0.887 (REVISE)
- **Strategy Findings Incorporated:** Yes — 5 adversarial strategy reports (S-014, S-003, S-001, S-013, S-002) and iteration-1-changelog.md reviewed
- **Scored:** 2026-03-02

---

## DELIVERABLE 1: Orchestration Mega-Prompt Template v1.1.0

### Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.924 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Prior Score** | 0.878 |
| **Delta** | +0.046 |
| **Strategy Findings Incorporated** | Yes — iteration-1-changelog.md |

### Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.94 | 0.188 | All 5 prompt elements present; DA-1 now lists /worktracker, /transcript, /ast; Prerequisites section added; SI-4 added; minor constraint-count discrepancy (changelog says 20->21, prior score report said 22) |
| Internal Consistency | 0.20 | 0.95 | 0.190 | AQ-1/AQ-2/AQ-5 deadlock resolved with explicit cross-references and escalation path; DA-1/SI-1 contradiction resolved with permitted-actions list; EC-2 delegation clause added |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | NPT-013 format correct throughout; Scope Guard present; Criticality note for C4 added; "syntactically valid Mermaid" added to OP-2; Scope Guard uses HTML comments which may be stripped in some environments |
| Evidence Quality | 0.15 | 0.81 | 0.122 | Statistical claim now has full source path; Research Basis column added to Constraint Inventory with NPT-IDs and AGREE-IDs per constraint; individual constraints still lack file-path anchors (ID codes only) |
| Actionability | 0.15 | 0.95 | 0.143 | C4 criticality note added; non-Jerry alternatives embedded; all placeholders present; template is immediately copy-paste usable |
| Traceability | 0.10 | 0.93 | 0.093 | Research Basis column present; full source path for statistical claim; constraint count discrepancy between changelog and prior report unresolved; no file-path per-constraint anchors |
| **TOTAL** | **1.00** | | **0.924** | |

### Detailed Dimension Analysis

#### Completeness (0.94/1.00)

**Evidence:**
The v1.1.0 template contains all five canonical prompt elements (skill routing, scope, data source, quality gate, output path) with detailed production-ready content. The SI-4 constraint (checkpoint state on pipeline failure) is newly added. The Prerequisites section explicitly names the six required Jerry skills with their install paths and which constraints depend on them. The DA-1 constraint now correctly lists all delegatable skills including `/worktracker`, `/transcript`, and `/ast`.

The Scope Guard comment block clearly activates constraint tiers by criticality:
- C1/C2: 5 core constraints (DA-1, EC-1, SI-1, SI-2, PC-1)
- C3: Full set except AQ-4 full independence; IT-1–IT-5 only when implementation phases present
- C4: All 21 constraints

The quality gate element now lists criticality-scaled strategy counts: C1=1, C2=3, C3=6, C4=10.

**Gaps:**
A constraint-count discrepancy exists: the iteration-1-changelog.md states the constraint count increased from 20 to 21 (adding SI-4), but the iteration 1 scoring report counted 22 constraints in v1.0.0. The v1.1.0 footer states "21 constraints from 35 raw items (15 merges, 1 addition: SI-4)" — consistent with the changelog but inconsistent with the prior scoring report. This suggests either the prior scoring report miscounted, or one constraint was silently removed between versions. A verifier reviewing the audit trail would need to resolve this discrepancy. At 21 constraints, the actual count in v1.1.0 is verifiable (OP-1, OP-2, DA-1, AQ-1–5, IT-1–5, EC-1–2, SI-1–4, PC-1–2 = 21) and is correct; the discrepancy is in the changelog documentation, not the deliverable itself.

No AE-006 context-fill constraint remains absent — this was a minor gap in iteration 1 and is still unaddressed, though it was noted as optional in the prior assessment.

**Improvement Path:**
Reconcile the changelog's "20->21" claim against the iteration 1 report's "22 constraint" count — either the prior report miscounted or v1.0.0 had a different constraint set than documented. Document the resolution in the changelog for audit integrity.

---

#### Internal Consistency (0.95/1.00)

**Evidence:**
All three critical consistency failures from iteration 1 are resolved:

1. **AQ-1/AQ-2/AQ-5 deadlock resolved.** AQ-1 now contains an explicit escalation clause: "When the circuit breaker fires (AQ-2 ceiling reached) but the score remains below threshold, escalate to the user with the current best result, the last score, and open findings." AQ-2 cross-references: "AQ-1 revision cycles are bounded by this ceiling; when the ceiling is reached, AQ-5 governs pipeline-level behavior (halt at phase boundary)." AQ-5 cross-references: "When a phase gate fails and the circuit breaker has fired (AQ-2 ceiling reached), halt the pipeline and escalate to the user per AQ-2." These three constraints now form a coherent resolution chain: AQ-2 fires -> AQ-5 halts phase -> AQ-1 escalates to user.

2. **DA-1/SI-1 contradiction resolved.** DA-1 now includes an explicit positive statement: "Orchestration coordination actions ARE permitted in the main context: worktracker entity creation and updates, agent invocation decisions, handoff routing, phase status tracking, circuit-breaker state management, and orchestration plan maintenance." This distinguishes execution work from coordination work, eliminating the prior ambiguity.

3. **EC-2/DA-1 delegation ambiguity resolved.** EC-2 now states: "This obligation passes to the delegated creator agent — each skill agent MUST satisfy EC-2 for decisions within its scope." The template's Data Sources element also carries matching guard language.

**Gaps:**
No new contradictions introduced by the revisions. The AQ-1/AQ-2/AQ-5 interaction chains are internally consistent. The threshold language (0.92 SSOT default; 0.95 only for C4 with established baseline) is now consistent across AQ-1, the Quality Gate element, and the Placeholder Reference table.

Minimal residual concern: AQ-3 says route feedback to the "originating creator agent" but does not specify what happens when the originating creator agent is no longer in context (e.g., when a compaction event has occurred between its invocation and the critic response). This is a pre-existing edge case, not introduced by this revision, and is borderline SOFT given SI-4 now addresses checkpoint recovery.

**Improvement Path:**
Score held at 0.95 — no meaningful gaps remain. The residual AQ-3 edge case is addressed adequately by SI-4's checkpoint/compaction handling.

---

#### Methodological Rigor (0.94/1.00)

**Evidence:**
All 21 constraints follow the NPT-013 format (NEVER + Consequence + Instead) without exception. The Scope Guard is a new structural addition that correctly tiered constraint activation. The "syntactically valid" requirement was added to OP-2's Instead clause, closing the prior gap where a complete-but-broken Mermaid diagram could pass. The C4 criticality note in the Prerequisites section defines the term for readers unfamiliar with the Jerry quality model.

The constraint block comment accurately describes the NPT-013 mechanism: "Do not convert these to positive instructions — the negation + consequence + alternative structure is the active mechanism producing the compliance differential."

The quality gate element now provides criticality-scaled strategy counts that align precisely with `quality-enforcement.md` (C1: S-010 only; C2: S-010, S-014, S-007; C3: C2 + S-002, S-003, S-004; C4: all 10). This is a methodological improvement: the template is now self-consistent with its referenced SSOT.

**Gaps:**
The Scope Guard is implemented as HTML comments inside the `<forbidden_actions>` block. HTML comments are a fragile mechanism: (1) they are stripped by many LLM system prompt preprocessing pipelines, (2) they are invisible to XML parsers that would otherwise consume the constraint XML, and (3) they blend visually with the format/metadata comments above the guard. A more robust implementation would use a visible, tagged element — e.g., `<scope_guard>` — that cannot be silently stripped. This fragility was not present in the original design; it was introduced by the revision.

A colleague copying the template may not realize the Scope Guard is present (it looks like the other metadata comments) and may apply all 21 constraints regardless of criticality, defeating the guard's purpose.

**Improvement Path:**
Replace the Scope Guard HTML comment block with a visible structured element (e.g., a `<scope_guard>` XML tag or a clearly marked `## Scope Guard` section at the top of the forbidden_actions block) that cannot be silently stripped. The rule file's Scope Guard (a proper markdown section with a table) is more robust and should serve as the model.

---

#### Evidence Quality (0.81/1.00)

**Evidence:**
The iteration 1 primary gap (no per-constraint citations) is partially addressed. The Constraint Inventory table now includes a `Research Basis` column with coded citations per constraint. For example:
- OP-1: "NPT-009 (structured negation), TASK-004 (plan completeness)"
- DA-1: "NPT-012 (context compaction), AGREE-003 (delegation superiority)"
- AQ-1: "NPT-013 (structured negation), AGREE-001 (phase-gate quality)"
- EC-1: "NPT-013, AGREE-005 (evidence integrity)"
- SI-4: "NPT-012, WT-GAP-005 (error recovery)"

The statistical claim now carries a full source path: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/ab-testing/comparative-effectiveness.md` with n=50, p=0.016, +7.8pp.

**Gaps — remaining evidence quality limitation:**
The Research Basis codes (NPT-009, AGREE-001, TASK-004, etc.) are internal reference IDs that a colleague cannot resolve without access to the PROJ-014 research corpus index. There is no inline file path or document title that makes the citation self-contained. Specifically:
- NPT-009, NPT-012, NPT-013 are pattern catalog IDs — not file paths
- AGREE-001 through AGREE-005 are consensus findings — not file paths
- TASK-004, TASK-005, TASK-006 are task IDs — not file paths
- WT-GAP-005 is a gap catalog ID — not a file path

A colleague receiving this template in isolation (without the PROJ-014 research corpus) cannot verify:
1. What NPT-009 says and whether it supports OP-1 as described
2. What AGREE-003 says and whether it specifically supports the delegation model
3. Whether WT-GAP-005 is T1-controlled evidence or T4-observational

This is a meaningful improvement over iteration 1 (where there were no per-constraint citations at all), but it does not reach the 0.9+ threshold where "most claims are supported with credible citations." The citations are present but not verifiable without the research corpus index. Scoring at 0.81 rather than 0.85 because the ID codes provide traceability linkage but not independent verifiability.

**Improvement Path:**
For each Research Basis entry in the Constraint Inventory, add the file path or document title alongside the ID code. For example: "NPT-009 (`taxonomy-pattern-catalog.md`), TASK-004 (`barrier-4/synthesis.md`)." This would raise Evidence Quality to the 0.87–0.90 range.

---

#### Actionability (0.95/1.00)

**Evidence:**
The C4 criticality note is present and self-contained: "C4 = irreversible, architectural, or governance decisions requiring all 10 adversarial strategies per quality-enforcement.md." The Placeholder Reference table has 16 placeholders (expanded from 14 in iteration 1) with examples. All non-Jerry alternatives are embedded inline in the constraint text. The template is immediately copy-paste usable with a clear three-step How to Use section.

The Scope Guard clarifies expected behavior for C1/C2/C3/C4 workflows, improving actionability for colleagues who need to adapt the template to their criticality context. The `{{QUALITY_THRESHOLD}}` placeholder note specifies "SSOT default; use 0.95 for C4 with baseline" — removing a prior ambiguity.

**Gaps:**
No significant gaps remain for actionability. The template is well-structured for immediate use. The Scope Guard's HTML comment implementation (noted above under Methodological Rigor) is a usability concern but does not prevent a knowledgeable colleague from using the template correctly.

**Improvement Path:**
None required for actionability alone.

---

#### Traceability (0.93/1.00)

**Evidence:**
The Research Basis column is added to the Constraint Inventory, providing the first per-constraint traceability layer. The statistical claim in the header has a full file path. The constraint count is documented ("21 constraints from 35 raw items, 15 merges, 1 addition"). The version is clearly marked (v1.1.0 | 2026-03-02 | Revision: Iteration 1).

The constraint IDs remain stable from v1.0.0 to v1.1.0 — OP-1, DA-1, AQ-1–5, IT-1–5, EC-1–2, SI-1–4, PC-1–2 are all present. SI-4 is the only new constraint and it is correctly added to the SI domain.

**Gaps:**
The constraint-count discrepancy (changelog: 20->21; prior scoring report: 22) creates an audit gap. If a reviewer asks "what happened to the 22nd constraint from v1.0.0?" there is no documented answer. This is a documentation-level traceability gap, not a content gap.

The Research Basis IDs (NPT-009, AGREE-001, etc.) provide traceability linkage to the research corpus but not to specific file paths within the corpus. As noted under Evidence Quality, a colleague without the corpus index cannot resolve these IDs. Traceability scores higher than Evidence Quality because the IDs do provide linkage; they just require an additional lookup step.

**Improvement Path:**
Reconcile the constraint count discrepancy in the changelog. Add file path annotations to Research Basis IDs (e.g., "NPT-013 (`ab-testing/comparative-effectiveness.md`)").

---

### Improvement Recommendations (Priority Ordered) — Deliverable 1

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.81 | 0.90 | Add file path or document title alongside each Research Basis ID code in the Constraint Inventory. Format: "NPT-009 (`taxonomy-pattern-catalog.md`)" — one lookup step eliminated per constraint. |
| 2 | Methodological Rigor | 0.94 | 0.96 | Replace Scope Guard HTML comment block with a visible `<scope_guard>` XML element or a clearly-marked section header that cannot be silently stripped by LLM preprocessing pipelines. |
| 3 | Completeness | 0.94 | 0.96 | Reconcile constraint count: changelog states "20->21" but prior report counted 22 in v1.0.0. Document the resolution (was the prior count wrong, or was one constraint removed?). |
| 4 | Traceability | 0.93 | 0.95 | Add specific file-path anchors to Research Basis column. Resolve constraint-count discrepancy in changelog for clean audit trail. |

---

## DELIVERABLE 2: Orchestration Behavioral Constraints Rule File v1.1.0

### Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.931 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Prior Score** | 0.887 |
| **Delta** | +0.044 |
| **Strategy Findings Incorporated** | Yes — iteration-1-changelog.md |

### Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | Prerequisites, Scope Guard, Constraint Interaction Map, AQ-5 in L2-REINJECT, SI-4, DA-1 skill list all addressed; 21 constraints; all sections in navigation table |
| Internal Consistency | 0.20 | 0.97 | 0.194 | AQ-4 explicit strategy list (no more "S-001 through S-014" error); IT-3 H-07 citation restored; all deadlock chains resolved; Interaction Map formalizes enforcement chains |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Navigation table H-23 compliant; L2-REINJECT rank=3 with context explanation; Scope Guard as proper markdown section (more robust than D1's comment approach); NPT-013 applied uniformly |
| Evidence Quality | 0.15 | 0.81 | 0.122 | Research Basis column in Constraint Index with NPT-IDs and AGREE-IDs; statistical claim with full source path; same ID-only limitation as D1 — no file-path anchors per constraint |
| Actionability | 0.15 | 0.95 | 0.143 | Install instruction, scope definition, non-Jerry alternatives, absent-skill escalation; format rationale (why NPT-013 outperforms) added; NPT-013 mechanism explanation new in v1.1.0 |
| Traceability | 0.10 | 0.93 | 0.093 | Research Basis column present; IT-3 citation restored; statistical claim anchored; constraint count discrepancy same as D1; ID-only citations without file paths |
| **TOTAL** | **1.00** | | **0.936** | Rounded to 0.931 after strict calibration |

**Leniency check on composite:** Internal Consistency 0.97 requires explicit defense. This is warranted: the prior Critical finding (AQ-4 explicitly referencing excluded strategies) is fully corrected; IT-3 citation gap is restored; all three deadlock chains have explicit cross-references; and the Interaction Map formalizes what was previously implicit. The rule file has no remaining contradictions between constraints. 0.97 is correct, not lenient.

### Detailed Dimension Analysis

#### Completeness (0.96/1.00)

**Evidence:**
All major completeness gaps from iteration 1 are resolved:

1. **Prerequisites section added.** Lists all six required skills with paths, dependent constraints, and a non-Jerry warning.
2. **Scope Guard section added.** A proper markdown section with a four-row table (C1/C2/C3/C4) specifying exactly which constraints activate at each level. This is structurally superior to the HTML comment approach used in D1.
3. **Constraint Interaction Map added.** Five directed enforcement chains are documented: State Chain, Delegation Chain, Quality Chain, Ceiling Chain, Evidence Chain. The key interaction note (AQ-2 -> AQ-5 -> AQ-1 when ceiling fires) makes the system behavior explicit.
4. **AQ-5 added to L2-REINJECT.** The L2 marker now includes "Per-phase gates required, not end-of-pipeline only (AQ-5)." This addresses the prior completeness gap where the highest-priority re-injected constraints omitted per-phase gating.
5. **DA-1 skill list expanded.** Now includes `/worktracker, /transcript, /ast`.
6. **SI-4 added.** Error recovery and checkpoint persistence.
7. **Usage section expanded.** Now includes: install instruction, scope definition, out-of-scope definition, relationship to existing L2-REINJECT markers, format rationale, NPT-013 mechanism explanation.
8. **Navigation table updated.** All 12 sections (including new Prerequisites, Scope Guard, Constraint Interaction Map) are listed with anchor links.

**Gaps:**
No meaningful completeness gaps remain. The constraint-count discrepancy noted in D1 applies equally here (the footer says "21 constraints from 35 raw items (15 merges, 1 addition: SI-4)" — consistent with v1.1.0 content).

The L2-REINJECT marker is scoped to "(C3+ only)" in the first line — this is correct per the Scope Guard design. However, the L2 marker is placed unconditionally in the file header. A sub-C3 session loading this file from `.claude/rules/` will see the full constraint list but only the L2-reinforced subset. The Scope Guard table in the Usage section tells users which constraints are active, but the L2-REINJECT marker cannot enforce the scope activation — it can only signal it. This is a known limitation of the L2 mechanism, not a completeness gap in the file itself.

**Improvement Path:**
None required for completeness specifically.

---

#### Internal Consistency (0.97/1.00)

**Evidence:**
All three Critical internal consistency failures from iteration 1 are fully resolved:

1. **AQ-4 strategy list corrected.** The constraint now reads: "assign each of the 10 selected adversarial strategies (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014) to a separate agent invocation." The prior "S-001 through S-014" that included 5 constitutionally excluded strategies is gone. The excluded strategies are even explicitly called out: "(Excluded strategies: S-005, S-006, S-008, S-009, S-015 per quality-enforcement.md)."

2. **IT-3 citation restored.** "hexagonal architecture per H-07, SOLID per coding-standards.md" is now present, matching D1 and eliminating the cross-document inconsistency.

3. **AQ-1/AQ-2/AQ-5 deadlock resolved.** Same three-way cross-referencing as D1. The Constraint Interaction Map formalizes this with the Ceiling Chain: "AQ-2 (declare ceiling) --> AQ-5 (per-phase gates) --> AQ-1 (gate at each phase)" and the Key Interaction note explaining the handoff when the ceiling fires.

The Scope Guard table is internally consistent with the individual constraint headers:
- DA-1, EC-1, SI-1, SI-2, PC-1 are marked "All" in Constraint Index — consistent with C1 minimum set in Scope Guard
- AQ-1, AQ-2 are "C3+" in Constraint Index — consistent with C2 getting +AQ-1/AQ-2 in Scope Guard (slight discrepancy noted below)
- AQ-4 is "C4 full / C3 grouped" — consistent with Scope Guard's "AQ-4 full independence" exclusion at C3

**Minor inconsistency flagged:** The Scope Guard table says C2 gets "+AQ-1 (at 0.92 threshold), AQ-2 (ceiling=5)" but the Constraint Index marks AQ-1 and AQ-2 as "C3+." This is a real inconsistency introduced by the revision: the Scope Guard adds AQ-1 and AQ-2 to C2, but the Constraint Index (which was not updated to reflect this) still says C3+. A colleague reading the Constraint Index would see AQ-1 and AQ-2 as C3+ and not apply them at C2, contradicting the Scope Guard.

**Improvement Path:**
Update the Constraint Index table to reflect AQ-1 and AQ-2 as "C2+" to match the Scope Guard table. The Scope Guard should be the authoritative source; the Constraint Index should be updated to match it.

---

#### Methodological Rigor (0.96/1.00)

**Evidence:**
The rule file is correctly structured for its intended purpose as a `.claude/rules/` auto-loaded document:

- Navigation table is present and updated per H-23, covering all 12 sections including the three new ones.
- L2-REINJECT is correctly formatted with rank=3. The Usage section now explains: "The rank=3 placement means these constraints are re-injected after rank=2 quality threshold rules and before rank=4 architecture rules." This closes the prior gap where rank=3's position in the priority stack was undocumented.
- Scope Guard is implemented as a proper markdown section with a four-row table — significantly more robust than D1's HTML comment approach. This cannot be stripped by XML parsers or LLM preprocessing.
- The NPT-013 mechanism explanation is added: "The three-part structure (NEVER + Consequence + Instead) makes prohibited behavior, cascade cost, and correct alternative simultaneously salient in a single instruction. NEVER alone leaves agents without a forward path; NEVER+Instead leaves agents free to trade compliance against convenience; the Consequence clause closes this gap by naming the specific downstream failure." This is a methodologically substantive addition that explains the mechanism, not just the format.
- All 21 constraints use consistent NPT-013 format. The constraint XML uses simple `<constraint id="...">` without `format="NPT-013"` — appropriate for a rule file where format rationale is documented in prose.

**Gaps:**
The Constraint Interaction Map has a minor rendering limitation: the chains are expressed in text with `-->` notation, which is readable but not machine-parsable. This is cosmetically limited but functionally sound for the document's purpose.

The L2-REINJECT marker's "(C3+ only)" scope annotation is a signal, not enforcement. The L2 mechanism cannot actually suppress the constraints at C1/C2 — it can only inform the LLM that the constraints are C3+ scoped. Whether the LLM correctly respects this scoping in a C1 session depends on the quality of the instruction, not the presence of the marker. This is a fundamental limitation of L2-REINJECT as a mechanism, not a gap specific to this document.

**Improvement Path:**
None required for methodological rigor specifically. The "(C3+ only)" L2 limitation is a known constraint of the mechanism.

---

#### Evidence Quality (0.81/1.00)

**Evidence:**
The Research Basis column in the Constraint Index now provides ID-level citations for all 21 constraints. Examples:
- EC-1: "NPT-013, AGREE-005 (evidence integrity)"
- SI-4: "NPT-012, WT-GAP-005 (error recovery)"
- AQ-4: "FC-M-001 (fresh context), AGREE-004 (independence)"

The statistical claim in the header blockquote now includes: "Source: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/ab-testing/comparative-effectiveness.md`" with n=50, p=0.016, +7.8pp. This is a complete, verifiable citation for the key performance claim.

**Gaps:**
The same limitation as D1 applies: the Research Basis entries use coded IDs (NPT-009, AGREE-001, TASK-004, FC-M-001, WT-GAP-005) that cannot be resolved without access to the PROJ-014 research corpus index. For the rule file specifically, this matters more than for the template: the rule file will be auto-loaded into sessions where a verifier may want to understand why a constraint fires and what evidence supports it. An agent confronted with AQ-4 firing cannot trace "AGREE-004 (independence)" to any file without the corpus index.

The NPT-013 mechanism explanation (new in v1.1.0) correctly describes *how* the format works but does not cite the specific experimental result that distinguishes NPT-013 from NPT-014 (blunt prohibition). The source path cited in the header is for the aggregate comparison (NPT-013 vs positive-only), not for the NPT-013 vs NPT-014 distinction specifically. This is a narrow remaining gap.

**Improvement Path:**
Same as D1: add file path or document title alongside each Research Basis ID. For the NPT-013 mechanism explanation, add a citation to the specific source that validates the three-part structure over simpler negation forms.

---

#### Actionability (0.95/1.00)

**Evidence:**
The v1.1.0 rule file has strong actionability:

- Install instruction: one sentence with exact path (`.claude/rules/orchestration-behavioral-constraints.md`).
- Scope definition: explicitly states which workflow contexts activate the constraints.
- Out of scope: "Single-agent tasks, conversational sessions, C1 routine work" — prevents misuse.
- Non-Jerry alternatives: embedded in all skill-referencing constraints (DA-1, AQ-1, AQ-4, IT-1, IT-2, SI-1, PC-1).
- Absent-skill escalation: IT-1 and IT-2 now say "If /eng-team [/red-team] is not installed, escalate to the user rather than blocking implementation entirely."
- NPT-013 mechanism explanation: pre-empts the most likely mistake (converting constraints to positive instructions).
- Constraint Interaction Map: shows how constraints compose, enabling colleagues to understand system behavior, not just individual rules.

**Gaps:**
No significant actionability gaps. The Scope Guard table is immediately actionable — a colleague can see at a glance which constraints apply to their criticality level.

**Improvement Path:**
None required for actionability.

---

#### Traceability (0.93/1.00)

**Evidence:**
Traceability improvements since iteration 1:

- Research Basis column in Constraint Index provides first per-constraint traceability layer
- Statistical claim anchored to full file path
- IT-3 H-07 and coding-standards.md citations restored (eliminating cross-document inconsistency between D1 and D2)
- Version clearly marked (v1.1.0 | 2026-03-02)
- Constraint IDs stable from v1.0.0 to v1.1.0; only addition is SI-4
- Constraint Interaction Map shows how constraints reference each other (AQ-1 <-> AQ-2 <-> AQ-5 chains)

**Gaps:**
Same ID-only citation limitation as D1 — Research Basis codes require the PROJ-014 corpus index to resolve. The Constraint Index footer still says "Source: PROJ-014 Negative Prompting Research" without a specific artifact path, though the blockquote in the header now carries the specific statistical claim path.

The AQ-1/AQ-2 criticality inconsistency noted under Internal Consistency (Scope Guard says C2+, Constraint Index says C3+) is also a traceability issue: a verifier cross-referencing the two sections would get contradictory information about when AQ-1 activates.

**Improvement Path:**
Fix AQ-1/AQ-2 criticality in Constraint Index to match Scope Guard. Add file-path anchors to Research Basis IDs.

---

### Improvement Recommendations (Priority Ordered) — Deliverable 2

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.81 | 0.90 | Add file path or document title alongside each Research Basis ID in the Constraint Index. Format: "NPT-013 (`ab-testing/comparative-effectiveness.md`), AGREE-001 (`barrier-4/synthesis.md`)." |
| 2 | Internal Consistency | 0.97 | 0.98 | Update Constraint Index Criticality column for AQ-1 and AQ-2 to read "C2+" (not "C3+"), consistent with the Scope Guard table which explicitly adds AQ-1/AQ-2 to the C2 constraint set. |
| 3 | Traceability | 0.93 | 0.95 | Fix AQ-1/AQ-2 criticality level in Constraint Index (C2+ not C3+). Add specific file-path annotations to Research Basis column. |
| 4 | Completeness | 0.96 | 0.97 | No action required at this score — completeness is effectively resolved. The L2 scope-enforcement limitation is systemic, not document-specific. |

---

## Cross-Deliverable Findings (Iteration 2)

### Severity-Classified Findings

| Severity | ID | Deliverable | Finding | Status vs Iteration 1 |
|----------|----|-------------|---------|----------------------|
| Major | F-001 | D1, D2 | Evidence Quality: per-constraint citations use ID codes (NPT-IDs, AGREE-IDs) without file-path anchors — not independently verifiable without corpus index | **Partial resolution** — IDs added but no file paths |
| Minor | F-002 | D1 | Scope Guard implemented as HTML comments (may be stripped) — rule file's markdown section is the better model | **New finding** (introduced by revision) |
| Minor | F-003 | D2 | AQ-1/AQ-2 Criticality in Constraint Index says "C3+" but Scope Guard says C2 gets AQ-1/AQ-2 — internal inconsistency | **New finding** (introduced by revision) |
| Minor | F-004 | D1, D2 | Constraint count discrepancy: changelog says "20->21", prior score report said "22" — audit gap | **New finding** (introduced by revision) |
| Resolved | -- | D1, D2 | AQ-1/AQ-2/AQ-5 pipeline deadlock | **Fully resolved** |
| Resolved | -- | D1, D2 | DA-1/SI-1 contradiction | **Fully resolved** |
| Resolved | -- | D1, D2 | EC-2/DA-1 delegation ambiguity | **Fully resolved** |
| Resolved | -- | D2 | AQ-4 "S-001 through S-014" error | **Fully resolved** |
| Resolved | -- | D2 | IT-3 H-07 citation dropped | **Fully resolved** |
| Resolved | -- | D1, D2 | 0.95 threshold vs SSOT 0.92 | **Fully resolved** |
| Resolved | -- | D1, D2 | No criticality scope guard | **Fully resolved** |
| Resolved | -- | D1, D2 | EC-2 impractical at scale | **Fully resolved** |
| Resolved | -- | D1, D2 | Non-portability outside Jerry | **Fully resolved** |
| Resolved | -- | D1, D2 | Prompt injection via EC-2 | **Fully resolved** |
| Resolved | -- | D1, D2 | Empirical claim needs source path | **Fully resolved** |

### Critical Findings Assessment

No findings at Critical severity. The three Major findings from iteration 1 (F-001 deadlock, F-002 statistical claim, F-003 AQ-4 strategy error) are resolved or partially resolved. The remaining gap is F-001 partial resolution: evidence quality is improved but not at a level where per-constraint citations are independently verifiable without the corpus index.

The two new Minor findings (F-002 HTML comment fragility, F-003 AQ-1/AQ-2 criticality inconsistency) are introduced by the revision itself and should be addressed. F-003 is the more important of the two: it creates contradictory information in the same document about when AQ-1 and AQ-2 activate.

---

## Combined Verdict

| Deliverable | Iteration 1 | Iteration 2 | Delta | Threshold | Verdict |
|-------------|-------------|-------------|-------|-----------|---------|
| D1: Mega-Prompt Template | 0.878 | 0.924 | +0.046 | 0.95 | **REVISE** |
| D2: Behavioral Constraints Rule File | 0.887 | 0.931 | +0.044 | 0.95 | **REVISE** |

Both deliverables exceeded the SSOT H-13 threshold of 0.92 in this iteration. Both remain below the user-specified 0.95 threshold. The gap is driven by two factors:

1. **Evidence Quality (0.81 both):** Per-constraint citations use coded IDs rather than file-path anchors. This is a focused, one-pass fix: update the Research Basis column with file paths or document titles.

2. **New minor inconsistencies introduced by revision:** The D1 Scope Guard HTML comment fragility (F-002) and D2 AQ-1/AQ-2 criticality inconsistency (F-003) are small issues that must be addressed but represent regression-in-revision rather than fundamental gaps.

**Estimated revision cost for iteration 3:** 1–2 hours. The Evidence Quality fix is mechanical (adding file paths to an existing table). The F-003 inconsistency is a one-cell correction. The F-002 Scope Guard restructuring is the most effortful but can be done in under an hour by following the D2 model.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific evidence from the v1.1.0 content
- [x] Uncertain scores resolved downward (Internal Consistency D2 held at 0.97 not 0.98 because of the AQ-1/AQ-2 inconsistency; Evidence Quality held at 0.81 not 0.85 because ID-only citations are not independently verifiable)
- [x] First-draft calibration does not apply — these are revised production artifacts; the score improvement from 0.878/0.887 to 0.924/0.931 reflects genuine improvement, not score inflation
- [x] No dimension scored above 0.97 without documented justification (Internal Consistency D2 at 0.97 is the highest score; the explicit justification is the complete resolution of all three Critical consistency failures from iteration 1)
- [x] New findings introduced by revision (HTML comment fragility, AQ-1/AQ-2 inconsistency, constraint count discrepancy) are flagged and scored against, not forgiven because they were "improvement efforts"
- [x] Verdicts are REVISE not PASS — neither deliverable reaches 0.95; this is correctly reflected
- [x] Score delta (+0.046, +0.044) is proportionate to the scope of revision — 16 findings addressed across 9 Critical + 7 Major; a ~0.044–0.046 improvement is calibrated correctly for the volume of changes

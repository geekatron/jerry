# Constitutional Compliance Report: ADR-adversary-tournament-protocol-001

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy/deliverable metadata |
| [Summary](#summary) | Overall compliance assessment |
| [Findings Table](#findings-table) | All findings at a glance |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, remediation per finding |
| [Recommendations](#recommendations) | Prioritized remediation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Header

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3 (as declared by the deliverable itself, constraint c-007)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-007, blind pass, iteration 5)
**Constitutional Context:** `.context/rules/quality-enforcement.md` (HARD Rule Index H-01–H-36, Quality Gate, Criticality Levels), `.context/rules/agent-development-standards.md` (H-34 dual-file architecture, Tool Security Tiers), `.context/rules/markdown-navigation-standards.md` (H-23/H-24), `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (Scheme B MEDIUM standards, review draft, not yet ratified into `.context/rules/`), `skills/adversary/agents/adv-scorer.md`, `skills/adversary/agents/adv-selector.md`, `skills/adversary/SKILL.md`.

---

## Summary

**PARTIAL compliance.** Zero Critical (HARD-rule) violations found. The ADR's own headline claims — HARD-rule ceiling untouched (25/25), H-13/H-14/H-16/RT-M-010 "retained verbatim," MEDIUM-tier purity, and Scheme-B subject-encoded-id compliance — were checked directly against `.context/rules/quality-enforcement.md`, `.context/rules/agent-routing-standards.md`, `skills/adversary/agents/adv-scorer.md:166-167`, `skills/adversary/agents/adv-selector.md:89-107,112-128`, `skills/adversary/SKILL.md:341,361-370`, and `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`, and all verify accurate. Two Major (MEDIUM-tier documentation-fidelity) findings and one Minor finding were identified: a residual internal-consistency gap where an earlier self-correction (DA-005-iter4) was applied to the Decision table and Figure 1 caption but not to the Options-Considered table where the same ambiguous phrasing originates, and a traceability gap where the new stop-condition diagram (Figure 3) and its governing decision (D-4) never state how/where H-14's mandatory minimum-iteration floor relates to the diagrammed accept/stop logic, despite the ADR asserting H-14 is "retained verbatim." Constitutional compliance score: **0.88** (REVISE band, 0.85–0.91) — below the 0.92 gate on documentation-fidelity grounds only; no structural or HARD-rule defect. Recommend targeted revision, not rejection.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-iter5 | Internal-consistency / accuracy of self-correction (P-001 Truth-Accuracy, general) | MEDIUM | Major | Options Considered D-1 Option C (line 325) retains the pre-DA-005-iter4 ambiguous shorthand the Decision table (line 487) and Fig. 1 caption (lines 577–579) explicitly disclaim | Internal Consistency |
| CC-002-iter5 | H-14 (min-3-iteration cycle) traceability against a new operative diagram | HARD (H-14 itself unbroken; gap is in cross-reference/traceability of the specification) | Major | Figure 3 (lines 628–648) and D-4 decision row (line 490) omit any reference to H-14, while L2 (lines 874–877) asserts H-14 is untouched, and `skills/adversary/SKILL.md:368` assigns H-14 enforcement to "the orchestrator's responsibility" — a boundary Figure 3 does not restate | Traceability / Methodological Rigor |
| CC-003-iter5 | Internal-consistency of effort-sizing rationale | SOFT | Minor | Alignment table "Implementation Effort" row (line 518) vs. Work-Item Decomposition backlog Size column (lines 963–970) | Internal Consistency |

**Finding ID Format:** `CC-{NNN}-iter5` (execution-scoped to this iteration-5 blind S-007 pass).

---

## Detailed Findings

### CC-001-iter5: Stale ambiguous shorthand not corrected everywhere it appears [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Options Considered → D-1 → Option C (line 325); contrast Decision → D-1 row (line 487) and Design Diagrams → Figure 1 caption (lines 577–579) |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — Internal Consistency check |

**Evidence:**

Options Considered, D-1, Option C (line 325):
> **C. Criticality-proportional verify** (C4 full panels; C3 panels on Criticals only; C1–C2 none)

Decision table, D-1 row (line 487), the ADR's own later, explicit correction of exactly this phrasing:
> **C3 and C4 panel *every* claimed Critical identically** — the panelling rule is the same at both tiers; the "C4 all / C3 Criticals-only" shorthand denotes the *finder strategy set and iteration ceiling* (which differ by tier), **not** a per-Critical panelling-rate gradient (DA-005-iter4).

Figure 1 caption (lines 577–579) repeats the same disambiguation.

**Analysis:**

The Decision table and Figure 1 caption both carry an explicit, named correction (DA-005-iter4) stating that "C4 full panels; C3 panels on Criticals only" is a misleading shorthand that must not be read as a panelling-rate gradient. That correction, per the Changelog (0.5 entry), was applied to "D-1 row + Fig.1 caption" only. The earlier Options Considered table — which a reader encounters first per the document's own Navigation order (`Options Considered` precedes `Decision`) — still carries the identical ambiguous phrase verbatim, with no disclaiming footnote and no forward-reference to DA-005-iter4. A reader who stops at the Options table (a natural point to pause, since it is the section that steelmans and scores rejected alternatives) will form exactly the misreading ("C4 panels are more comprehensive than C3 panels") that DA-005-iter4 was created to foreclose. This is the same class of "correct once, leave stale elsewhere" defect the ADR itself explicitly names and warns against when it disclosed the "18 verification-panel files" citation error in iteration 1 ("the exact 'verify before you count' failure this ADR argues against," line ~200-201) — the fix pattern established there (correct at every site, not just one) was not applied to this later ambiguity.

This is not a HARD-rule violation (no H-rule text is contradicted), so it is classified MEDIUM/Major rather than Critical: the underlying decision (D-1 = Option C) is unaffected and the Decision table itself is accurate. The defect is documentation fidelity — an ADR whose central methodological claim is "verify claims before counting them" leaving one of its own prior claims uncorrected at a site the correction's own changelog did not target.

**Recommendation:**

Add the same disambiguating clause to the D-1 Option C cell in Options Considered, e.g.: "(C3 and C4 panel every claimed Critical identically; C1–C2 none — the tier difference is the finder-strategy-set/iteration-ceiling, not the panelling rate; see DA-005-iter4 in Decision, D-1)." This is a one-line, subtraction-consistent edit (adds a disambiguating clause, does not add new machinery).

---

### CC-002-iter5: New stop-condition diagram omits any reference to H-14's iteration floor, and does not restate where that floor is enforced [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Design Diagrams → Figure 3 (lines 628–648) and caption (lines 650–654); Decision → D-4 row (line 490); L2 Architectural Implications → "Interaction with H-14 and RT-M-010" (lines 874–877); contrast `skills/adversary/SKILL.md:361-370` |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — H-14 (Creator-critic-revision cycle, min 3 iterations) |

**Evidence:**

Figure 3 (mermaid, lines 628–648) reaches `PASS([PASS - accept])` via the branch:
```
PROTO -- "Yes (verified protocol)" --> Q1{"Any VERIFIED Criticals this round?"}
Q1 -- "No, composite >= gate" --> PASS([PASS - accept])
```
No node, edge, or the caption (lines 650–654) references a round-count floor; the diagram's only iteration-bound concept is `Q4{"RT-M-010 ceiling reached?"}` on the *upper* bound path (FIX/BAND → Q4), not on the PASS path.

D-4 decision row (line 490): "Recurrence across independent rounds = real (remediate); non-convergent fresh stream = artifact (switch to verified protocol, or stop). RT-M-010 ceilings and plateau detection unchanged; escalate-to-user at ceiling." — names RT-M-010 explicitly but not H-14.

L2 Architectural Implications (lines 874–877): "Verified-only gating does not reduce the minimum 3 iterations (H-14) nor raise the ceilings (RT-M-010); it changes only *which* findings force a revision within those bounds."

Contrast the currently-live `skills/adversary/SKILL.md:361-370`, "Integration with Creator-Critic-Revision Cycle (H-14)" section, point 4 (line 368): "**Minimum 3 iterations are the orchestrator's responsibility.** The adversary skill does not enforce iteration count -- it scores when asked. The orchestrator (or `/orchestration` skill) tracks the iteration count per H-14."

**Analysis:**

Today, H-14's floor is deliberately kept *out* of the scorer/tournament decision tree and assigned to the orchestrator (SKILL.md:368) — this is a real, working separation of concerns, and it is why Figure 3's PASS-at-any-round branch is not, by itself, a live H-14 violation: the orchestrator's separate enforcement is what actually holds the floor open. The gap is that the ADR's own L2 claim ("does not reduce the minimum 3 iterations") is true only *because* of that external, un-cited safeguard — and neither Figure 3, its caption, nor the D-4 decision text states this. WI-5's own acceptance criteria ("Verify stage documented in Tournament Mode; ... convergence/stop-condition (D-4) documented; version bump," line 967) direct a future editor to fold Figure 3's stop-condition logic into the very SKILL.md section that currently carries the orchestrator-responsibility clause (line 368), with no explicit instruction to retain or cross-reference that clause. A future implementer working from Figure 3 and the D-4 text alone — both of which are silent on H-14 — has no signal that the clause at SKILL.md:368 must survive the edit. This is a genuine traceability/methodological-rigor gap in a governance ADR whose subject matter is precisely "verify claims before trusting them" and whose own diagrams are the specified operational artifact (per the ADR's Design Diagrams section: "the diagrams so that we can then review and create work items," commission FU.12).

Classified Major, not Critical: H-14 is not currently violated (the safeguard text is unedited and still in force), so this is a prospective specification gap rather than a present HARD-rule breach.

**Recommendation:**

1. Add one sentence to the Figure 3 caption (or the D-4 decision row): "H-14's minimum-3-iteration floor is enforced upstream by the orchestrator (`skills/adversary/SKILL.md`, Integration with Creator-Critic-Revision Cycle) and is independent of this stop-condition; Figure 3 governs only the scorer/panel accept-or-continue signal, not the orchestrator's iteration-count floor."
2. Add an explicit WI-5 acceptance-criteria clause: "the existing H-14 orchestrator-responsibility clause (`SKILL.md:368`) is retained or cross-referenced, not silently dropped, when the stop-condition section is added."

---

### CC-003-iter5: Alignment-table effort-sizing phrase is ambiguous against the backlog's own Size column [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Decision → Alignment table, "Implementation Effort" row (line 518); contrast Work-Item Decomposition backlog table, Size column (lines 963–970) |
| **Strategy Step** | Step 3 — Internal Consistency (SOFT-tier documentation clarity) |

**Evidence:**

Alignment table (line 518): "All **8** backlog items (CC-001-iter3): one new agent (WI-1), one new template (WI-2), three edited agent/skill artifacts (WI-3/WI-4/WI-5), one new guidance doc (WI-6), one SSOT pointer (WI-7), and one operational validation pass (WI-8, ...). No code, no HARD-rule work; **the two "M"-sized items beyond the change-surface are the runner guide (WI-6) and the validation pass (WI-8)**."

Backlog Size column (lines 963–970): WI-1 = M, WI-2 = M, WI-3 = S, WI-4 = S, WI-5 = S, WI-6 = M, WI-7 = XS, WI-8 = M — four items sized "M," not two.

**Analysis:**

The sentence is defensible only under an implicit reading where "the change-surface" means the L1 Technical Implementation's seven-item change-surface enumeration (WI-1 through WI-7, all listed there as items 1–7), so that "beyond the change-surface" means beyond WI-7 — leaving WI-6 (item 6 of that same list) awkwardly double-counted as both inside and "beyond" the change-surface in the same sentence. A reader checking only the backlog table's Size column, without cross-referencing the L1 enumeration, will see four "M" items (WI-1, WI-2, WI-6, WI-8) and may read the Alignment claim as understated. Low materiality; does not affect the decision or any HARD/MEDIUM principle, included for completeness per P-022 (no findings omitted).

**Recommendation:**

Reword to, e.g.: "the two M-sized items beyond WI-1–WI-5's core agent/template build are the runner guide (WI-6) and the validation pass (WI-8)."

---

## Recommendations

**P0 (Critical):** None.

**P1 (Major):**
- CC-001-iter5: Add the DA-005-iter4 disambiguating clause to Options Considered D-1 Option C (or a forward-reference to it).
- CC-002-iter5: Add an explicit H-14-scope disclaimer to Figure 3's caption / D-4 decision row, and add a WI-5 acceptance-criteria clause preserving the `SKILL.md:368` orchestrator-responsibility text.

**P2 (Minor):**
- CC-003-iter5: Reword the Alignment table's "Implementation Effort" sentence to scope "change-surface" unambiguously to WI-1–WI-5.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No findings affect completeness; all 8 required S-007-relevant governance surfaces (H-13, H-14, H-16, RT-M-010, HARD-rule ceiling, Scheme-B, H-23, MEDIUM-tier purity) were checked and are substantively addressed. |
| Internal Consistency | 0.20 | Negative | CC-001-iter5 (Major): a named self-correction (DA-005-iter4) was applied to two sites but not a third carrying the identical ambiguous phrase. CC-003-iter5 (Minor): effort-sizing phrase ambiguous against its own backlog table. |
| Methodological Rigor | 0.20 | Negative | CC-002-iter5 (Major): the new stop-condition specification (Figure 3 / D-4) is silent on how it relates to H-14, an explicitly HARD constraint the ADR claims to preserve verbatim. |
| Evidence Quality | 0.15 | Neutral | All checked citations (`adv-scorer.md:166-167`, `adv-selector.md:89-107,112-128`, `SKILL.md:341,361-370`, `quality-enforcement.md` HARD Rule Index, `adr-standards-rule-draft.md`) verify accurate; no fabricated or misattributed evidence found in this pass. |
| Actionability | 0.15 | Neutral | Both Major findings have specific, one-line, subtraction-consistent remediations; no negative impact on actionability. |
| Traceability | 0.10 | Negative | CC-002-iter5: the specification's own traceability from "H-14 retained verbatim" to the mechanism that actually preserves it (an external, uncited SKILL.md clause) is incomplete. |

**Constitutional Compliance Score:** `1.00 - (0 * 0.10 + 2 * 0.05 + 1 * 0.02) = 1.00 - 0.12 = 0.88`

**Threshold Determination:** REVISE (0.85–0.91 band; below the H-13 0.92 gate on documentation-fidelity grounds; no Critical/HARD-rule finding).

---

## Constitutional Checks That PASSED (for completeness, per P-022 — no findings omitted or inflated)

- **HARD-rule ceiling (25/25):** Verified against `.context/rules/quality-enforcement.md` HARD Rule Index — the ADR adds/edits zero H-rules; ceiling claim accurate.
- **H-13 (>=0.92 threshold), H-14 (min 3 iterations), H-16 (Steelman before Devil's Advocate), RT-M-010 (C1=3/C2=5/C3=7/C4=10):** All cited verbatim and consistently with the SSOT; H-16 ordering preserved in Figure 1 (Group B S-003 precedes Group C S-002).
- **MEDIUM-tier purity:** No new "H-" ID is introduced; all agent/template/rule edits proposed are MEDIUM-tier per the ADR's own framing and consistent with existing agent-definition MUST/SHOULD conventions (agent behavioral contracts already use HARD-style verbs without being counted toward the H-rule ceiling, per `agent-development-standards.md` Guardrails Template).
- **Scheme-B id compliance:** Frontmatter `id: ADR-adversary-tournament-protocol-001` matches the filename-derived canonical identity exactly (ADR-M-001); filename matches the canonical regex (domain-slug + `-001` + title-slug tail, ADR-M-006); `scope: project` with the M-007/M-013 location-vs-intent tension named explicitly in the Meta-Note (not silently resolved); `origin_project: PROJ-031` correct; location (`projects/PROJ-031-cowork-skeleton/decisions/`) matches the canonical project home (ADR-M-007) — checked against `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`.
- **H-23/H-24 (navigation table, anchor links):** All 17 nav-table entries resolve to real `##` headings with correctly-formed anchors; no orphaned or missing entries.
- **P-003 (worker agent, no recursion):** The proposed `adv-verifier` agent is explicitly scoped to `Read, Glob, Grep, Write` with `Edit`/`Bash`/`Agent`/`Task` disallowed; blindness and single-level invocation are stated as MAIN-CONTEXT-orchestrated (consistent with the existing `adv-scorer`/`adv-selector` P-003 self-check pattern).
- **H-34(b) (ex-H-35) constitutional-triplet / forbidden-actions minimum:** WI-1's acceptance criteria invoke "H-34 (incl. sub-item b, ex-H-35) schema-valid" as a blanket requirement; this subsumes the >=3-forbidden-actions / P-003+P-020+P-022 minimum without needing to restate every field.
- **Citation accuracy:** `skills/adversary/agents/adv-scorer.md:166` ("Any Critical finding from adv-executor reports -> automatic REVISE regardless of score") and `:167` (the score>=0.92-but-unresolved-Critical case) match the ADR's citations exactly. `skills/adversary/agents/adv-selector.md:89-107` (Active Enforcement/AE rules) and `:112-128` (H-16 constraint + Group ordering) match. `skills/adversary/SKILL.md:341` (Group D — Verify: S-007, S-011) matches Figure 1's finder subgraph exactly.

---

## Execution Statistics

- **Total Findings:** 3
- **Critical:** 0
- **Major:** 2
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5

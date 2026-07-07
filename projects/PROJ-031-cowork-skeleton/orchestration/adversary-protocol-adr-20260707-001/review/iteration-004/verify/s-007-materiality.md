# S-007 Materiality Refutation Panel — Iteration 4

**Lens:** Materiality
**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-004/s-007-findings.md`
**Rule:** Attempt to REFUTE each claimed Critical. DEFAULT REFUTED IF UNCERTAIN. Materiality = does the finding genuinely undermine the ADR (wrong decision, unimplementable spec, false evidence)? Style/edge-case findings are REFUTED even if factually true.

---

## CC-001-iter4: REFUTED

**Claim:** The ADR's repeated thesis ("no HARD rule is touched," "25/25 ceiling untouched," ADR L0 at decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:92-94, constraint c-001 at line 265) is contradicted because the proposed `adv-scorer.md` edit (L1 item 3, lines 742-749; WI-3 AC, line 926; D-5 decision row, line 482) mandates new scoring-report content using HARD-tier vocabulary ("REQUIRED") as defined by the Tier Vocabulary SSOT (`.context/rules/quality-enforcement.md` "Tier Vocabulary" table), without registering a new HARD rule or invoking the ceiling's Exception Mechanism.

**Assessment:** REFUTED. The Tier Vocabulary table classifies keyword tiers for entries in the quality-enforcement.md "HARD Rule Index" — the specific table whose row count is capped at 25 (see "HARD Rule Ceiling Derivation," same file). It is a rule-authoring convention for that index, not a blanket lexical ban on the English word "REQUIRED" appearing anywhere in the Jerry corpus. Agent-definition and template files already use "REQUIRED" pervasively for internal schema/content obligations without those uses being counted as new ceiling-consuming H-rules — e.g. `agent-development-standards.md`'s "Required fields" tables for `.governance.yaml` (version, tool_tier, identity.role, etc.) and `TEMPLATE-FORMAT.md`'s "REQUIRED" section markers are exactly this pattern, and the ADR's own WI-7 acceptance criterion is explicit that the ceiling-relevant test is "zero change to HARD rules, weights, thresholds, criticality sets, or ceiling (verified by diff)" against the HARD Rule Index table itself (line 930) — a test the proposed adv-scorer.md content edit does not fail, since it adds no row to that index.

The finding's own hedge — "if the intent is genuinely non-overridable... disclose this honestly... rather than asserting zero HARD-rule impact" — concedes this is a plausible-but-unresolved interpretive reading, not a demonstrated contradiction. The distinction the finder draws to H-17 (a framework-wide, cross-cutting constitutional mandate on every C2+ deliverable) is not analogous in scope to a single agent's own internal report-format obligation scoped to one skill's tournament mechanics; the former is exactly the kind of cross-cutting rule the ceiling exists to bound, the latter is implementation-detail content the ADR itself frames (correctly) as MEDIUM-tier process specification. Even taking the finding at face value, the fix is a one-line wording softening (REQUIRED → SHOULD) that changes zero decisions (D-1 through D-6), zero acceptance criteria substance, and zero implementability — it is a vocabulary-precision/self-consistency style concern, not a finding that the ADR reaches the wrong decision, specifies something unimplementable, or rests on false evidence. Per the materiality lens's explicit instruction, style/consistency findings of this kind are REFUTED even where the underlying observation (mixed vocabulary tier in one edit) is factually accurate.

The bundled secondary observation (RSK-6's dual-protocol sunset lacking an assigned owner/trigger) is a real, separately-addressable completeness gap in the risk register, but it is a minor risk-register refinement, not evidence that the ADR's central thesis is false or that the decision is wrong — it does not independently establish materiality for a Critical-severity finding.

**Verdict contributing to majority:** REFUTED.

---

## Summary

| Finding ID | Verdict |
|---|---|
| CC-001-iter4 | REFUTED |

Only one Critical finding (CC-001-iter4) was present in the target S-007 report; it is REFUTED under the materiality lens. No other Critical-severity findings required adjudication (CC-002-iter4 is Major, CC-003-iter4 and CC-004-iter4 are Minor, and per protocol only Criticals are panelled).

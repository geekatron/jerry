# Refutation Panel — Factual-Accuracy Lens

## Panel Context

- **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-004/s-007-findings.md` (S-007 Constitutional AI Critique)
- **Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Lens:** Factual accuracy — does the claim's cited evidence resolve as stated?
- **Rule:** DEFAULT-REFUTED on uncertainty. Blind to materiality/remediation-value lenses and to the scorer.
- **Scope:** Per the protocol under review (D-1: "panels adjudicate Criticals only"), only the single Critical-severity finding is in scope for this panel. Major/Minor findings (CC-002-iter4, CC-003-iter4, CC-004-iter4) are advisory and out of panel scope.

---

## CC-001-iter4: "MEDIUM-tier framing contradicted by HARD-tier vocabulary in the proposed scorer edit" [CRITICAL]

**Verdict: REFUTED**

**Citation accuracy check:** The quoted text exists as claimed. `adv-scorer.md:166-167` is the current unconditional rule cited as context (`skills/adversary/agents/adv-scorer.md:166`: "Any Critical finding from adv-executor reports -> automatic REVISE regardless of score"). The ADR's L1 item 3 (ADR lines 742-749) does contain "REQUIRED" ("a Delta-Reconciliation section and a dual-protocol (verified + old) composite are REQUIRED for any round that used panels"), the D-5 decision-table row (ADR line 429/482) reads "B — mandatory delta-reconciliation," and WI-3's acceptance criteria (ADR line 926) contains "Delta-Reconciliation section REQUIRED; dual-protocol composite REQUIRED when panels used." The ADR's own thesis lines are also accurately quoted: L0 ("Everything here is a MEDIUM-tier process change... no HARD rule is touched and the 25/25 HARD-rule ceiling is untouched," ADR lines 92-93), c-001 ("No HARD-rule additions, deletions, or edits; ceiling stays 25/25," ADR line 265), c-002 (ADR line 266). So the quotations themselves are not fabricated or misquoted.

**But the alleged contradiction is a misapplication (misread) of the Tier Vocabulary SSOT's actual scope.** `.context/rules/quality-enforcement.md:159-165` ("Tier Vocabulary") lists `REQUIRED` as a HARD keyword with "Max Count <= 25" — that Max Count column ties this table directly to the **HARD Rule Index** (the enumerated H-01..H-36 registry in the same file, section "HARD Rule Index"), not to every occurrence of the word "REQUIRED" anywhere in the framework's prose. The ADR's own "no HARD rule is touched" claim is explicitly scoped the same way: WI-7's acceptance criteria (ADR line 930) states the pointer edit causes "zero change to HARD rules, weights, thresholds, criticality sets, or ceiling (verified by diff)" — i.e., the claim is about the HARD Rule Index table in `quality-enforcement.md`, which this ADR's own diff-based AC commits to leaving untouched, and which WI-3/WI-1 (the `adv-scorer.md`/`adv-verifier.md` edits) do not touch at all.

**Direct counter-evidence from the very file the ADR proposes to edit:** `skills/adversary/agents/adv-scorer.md` already uses HARD-tier-style imperative vocabulary extensively in its own internal behavioral specification without any of it being registered in the HARD Rule Index or counted against the 25-rule ceiling — e.g. `adv-scorer.md:71` ("You **MUST** actively counteract this"), `adv-scorer.md:298` ("Score report **MUST** be persisted to file"), `adv-scorer.md:311` ("This agent **MUST NOT** use the Task tool to spawn subagents"). None of these pre-existing MUST-statements are H-NN entries in `quality-enforcement.md`'s HARD Rule Index, confirming that imperative/mandatory language internal to an agent's own behavioral contract is not, by itself, equivalent to registering a new constitutional HARD rule. Adding one more such instruction ("a Delta-Reconciliation section... REQUIRED") to the same file is consistent with — not a departure from — that file's existing style and does not, on its own, create an unregistered HARD rule requiring the ceiling's Exception Mechanism.

**Conclusion:** The citations are accurate, but the inference that this text usage contradicts "no HARD rule is touched" rests on treating the Tier Vocabulary table as a universal style prohibition rather than the rule-registry classification scheme it actually is (as its own "Max Count <= 25" column and adjacency to "HARD Rule Index"/"Two-Tier Enforcement Model" make clear). Per DEFAULT-REFUTED and the "misreads... are REFUTED" standard for this lens, this finding is REFUTED at the factual-accuracy layer.

---

## Adjudication Summary

| ID | Severity | Panel-in-scope? | Factual Verdict |
|----|----------|------------------|------------------|
| CC-001-iter4 | Critical | Yes (only Critical in report) | **REFUTED** |
| CC-002-iter4 | Major | No (protocol panels Criticals only) | Not adjudicated by this panel |
| CC-003-iter4 | Minor | No | Not adjudicated by this panel |
| CC-004-iter4 | Minor | No | Not adjudicated by this panel |

**Panel note:** Only CC-001-iter4 is a Critical-severity claim in this report, and it is REFUTED at the factual-accuracy lens. Final VERIFIED/REFUTED disposition requires 2-of-3 across all three lenses (factual, materiality, remediation-value); this file records the factual-accuracy lens only.

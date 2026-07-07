# Remediation Notes — ADR-adversary-tournament-protocol-001, Iteration 1

> Owner-authored disposition record for the iteration-1 tournament (S-014 composite 0.66, gate 0.92,
> verdict REVISE; 8-of-8 claimed Criticals panel-VERIFIED). Subtraction-first per D-3. Each finding is
> tagged CLOSED-BY-EDIT / CLOSED-BY-DELETION / CLOSED-BY-DISCLOSURE / REBUTTED / RESIDUAL-DISCLOSED.

## Navigation

| Section | Purpose |
|---------|---------|
| [Inputs](#inputs) | Score report and finder/panel sources read |
| [Underlying Defects](#underlying-defects-8-verified-criticals--4-defects) | 4 defects behind the 8 VERIFIED Criticals |
| [Disposition Table](#disposition-table) | Per-finding CLOSED/REBUTTED/RESIDUAL disposition |
| [Advisory Dispositions](#advisory-dispositions-high-value-majorsminors) | High-value advisory Major/Minor fixes |
| [Subtraction Ledger](#subtraction-ledger) | Net lines added vs. removed |
| [Verification](#verification) | Post-edit self-checks |

---

## Inputs

- Score report: `review/iteration-001/s-014-quality-score.md` (0.66 REVISE; 8-of-8 VERIFIED)
- Finder reports: `s-002-findings.md`, `s-003-findings.md`, `s-007-findings.md`, `s-011-findings.md`
- Refutation panels: `review/iteration-001/verify/{s-002,s-007,s-011}-{factual,materiality,remediation-value}.md`
- Filesystem re-verification (this pass): `fu-log .../iteration-008/verify/` = **12** files (grep/ls confirmed);
  `adr-convention .../iteration-009/verify/` = **15** files (confirms "15" is correct, "18" is false).

---

## Underlying Defects (8 VERIFIED Criticals → 4 defects)

| Defect | Claimed by (VERIFIED) | Primary dimension | Fix summary |
|---|---|---|---|
| **D1** — False "18 vs 12" verifier-file citation | DA-001, CV-001 (+advisory CC-003) | Evidence Quality | Correct "18"→"12" at 3 sites; "~15–18"→"~12–15"; disclosed-correction footnote (D-3). |
| **D2** — Cost-model / invocation-contract granularity contradiction | DA-002, CC-002, CV-002 | Internal Consistency / Method. Rigor / Actionability | Standardize on **per-claimed-Critical** (3 lenses each); gate at report level; make L1 item 1, c-004, Cost model, Fig. 4, file-naming all agree. |
| **D3** — RSK-1 mitigation is the logical inverse of DEFAULT-REFUTED | DA-004, CC-001 | Internal Consistency | Rewrite RSK-1 mitigation: honestly state DEFAULT-REFUTED is discard-biased (raises residual false-negative exposure); name the real partial counterweights. |
| **D4** — Criticality-gating boundary unevidenced (100% of record is C4) | DA-003 | Method. Rigor | Relabel C1–C2 exemption / C3-vs-C4 split as a reasoned default, not an evidence-led finding; disclose 100%-C4 record; point to WI-8. |

---

## Disposition Table

| Finding ID | Panel | Disposition | Location(s) edited |
|---|---|---|---|
| DA-001-20260707-i1 | 3/3 | CLOSED-BY-EDIT + CLOSED-BY-DISCLOSURE | c-004; Context evidence-chain; Cost model; new correction footnote |
| CV-001-20260707-i1 | 3/3 | CLOSED-BY-EDIT (same defect as DA-001) | (as above) |
| DA-002-20260707-i1 | 3/3 | CLOSED-BY-EDIT | L1 item 1; c-004; Cost model; D-6 rationale |
| CC-002-20260707-iter1 | 3/3 | CLOSED-BY-EDIT (same defect as DA-002) | (as above) |
| CV-002-20260707-i1 | 3/3 | CLOSED-BY-EDIT (same defect as DA-002) | (as above) |
| DA-004-20260707-i1 | 3/3 | CLOSED-BY-EDIT | RSK-1 mitigation |
| CC-001-20260707-iter1 | 2/3 | CLOSED-BY-EDIT (same defect as DA-004) | (as above) |
| DA-003-20260707-i1 | 3/3 | CLOSED-BY-EDIT + CLOSED-BY-DISCLOSURE | D-1 "Why C is chosen"; Option-C row; new evidence-scope disclosure |

---

## Advisory Dispositions (high-value Majors/Minors)

| ID | Severity | Disposition | Location(s) |
|---|---|---|---|
| DA-005-20260707-i1 | Major | CLOSED-BY-DISCLOSURE | New "Evidence-base external validity" limitation (Consequences/Neutral + Risks RSK-7); WI-8 AC strengthened |
| DA-006-20260707-i1 | Major | CLOSED-BY-DISCLOSURE | RSK-2 mitigation honest caveat (context-isolation ≠ reasoning independence); L2 Phase-2 pointer |
| CV-003-20260707-i1 | Major | CLOSED-BY-EDIT | L0 "kept declining across six rounds" → accurate non-monotonic framing |
| CC-005-20260707-iter1 | Minor | CLOSED-BY-EDIT | "per H-35" → "per H-34(b)" at 3 sites |
| CC-004-20260707-iter1 | Minor | CLOSED-BY-DISCLOSURE | One-line note distinguishing Group D "verify-strategies" from the Refutation-Panel Verify stage |

---

## Subtraction Ledger

Net change is text-only, subtraction-consistent: no new machinery, no new decisions, no HARD-rule
touch. Corrections replace false/contradictory text with true/consistent text; the only additions are
honest-disclosure footnotes/limitations (which shrink the ADR's implied claim scope, per D-3). The six
D-1..D-6 decisions are untouched. Diagrams edited only where a label was itself the contradiction
(none required — Fig. 4 already states the chosen per-Critical unit).

---

## Verification

- [x] "18" verifier-file citations corrected to "12" (grep confirms 0 remaining "18 ... file" claims; "18 rounds" untouched).
- [x] Invocation unit is stated identically (per claimed Critical) in L1 item 1, c-004, Cost model, Fig. 4, file-naming.
- [x] RSK-1 mitigation no longer claims DEFAULT-REFUTED "keeps" claims.
- [x] C1–C2 / C3-vs-C4 boundary labeled a reasoned default with 100%-C4 record disclosed.
- [x] Zero hardcoded absolute home-directory paths; zero employer-internal tokens; repo-relative citations only.
- [x] Changelog appended to the ADR.

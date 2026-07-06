# Factual-Accuracy Refutation Panel — S-004 Pre-Mortem, Iteration 10

**Lens:** Factual accuracy only (does the cited defect exist at the cited lines in the CURRENT deliverables? misreadings/stale refs/already-disclosed-residual restatements are REFUTED).
**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-004-findings.md`
**Deliverables checked:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`, `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Disposition record checked:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/subtraction-pass-notes.md` (R-1..R-17, R-A/R-B/R-C register)
**Scope:** Per protocol, only the Critical finding(s) in the target report receive a verdict. The target report contains exactly one Critical finding: `004-001-iter010`. (`004-002-iter010` is Major, `004-003-iter010` is Minor — out of scope for this panel.)

---

## 004-001-iter010: Deletion of an ADR file silently frees its number for reuse, misdirecting old citations to an unrelated decision [CRITICAL]

**Verdict: VERIFIED**

**Reasoning:**

1. **Core citations re-read and confirmed accurate, verbatim, at the cited lines.** `ADR-PROJ031-004-adr-identifier-convention.md:217` (D-1) reads: "...and `NNN` is a 3-digit, zero-padded, never-reused sequence **within that domain slug**." `:128` (c-006) reads: "MUST be deterministically lint-able without a central registry or global counter." `adr-standards-rule-draft.md:50` (ADR-M-005) reads: "`NNN` SHOULD be 3-digit, zero-padded, monotonic within its namespace, never reused — reversal is by supersession, not renumbering." All three quotes match the finding's citations exactly — no misquotation, no stale line reference.

2. **The L-3 mechanism is confirmed to be existence-based, not history-based.** `ADR-PROJ031-004-adr-identifier-convention.md:688` and `adr-standards-rule-draft.md:177` both specify L-3 as `sort | uniq -d` over currently-scanned, non-frozen files — i.e., a diff over the *present* corpus. Neither document describes any append-only ledger, retired-ID registry, or historical-ID list (consistent with c-006's explicit "no central registry" constraint). The finding's technical claim — that a deleted file's ID becomes silently available for reuse with no detection mechanism — is a correct reading of the described mechanism, not a misreading.

3. **Confirmed absence of any deletion-policy or already-disclosed residual covering this exact scenario.** Direct re-read of Amend vs Supersede (`:602-614`, esp. line 612: "Numbers are never reused (Nygard; Jerry's tombstone precedent)") and Status Vocabulary (`:622-649`, incl. the `REJECTED` row) confirms neither section discusses file deletion (only tombstoning/superseding, which by design *retains* the file). A full-text grep of both deliverables for "delet*" turns up only references to deleting *lint rules/machinery* during the subtraction pass (v1.7–v1.11 changelog rows, the frozen-dir new-entry residual R-14) — none address deletion of a canonical/dialect ADR *file* itself. The Risks register (`:461-482`, R-1 through R-17) was re-read in full: R-6 (cross-branch same-slug race) and R-7 (slug reuse for an unrelated subject via legitimate-looking `NNN` extension) are the nearest analogues, but both concern *concurrent minting without any prior file existing/being removed* — a structurally different mechanism from "an ID retired by deletion of its file, later reused." This is not a restatement of R-6, R-7, or any other R-N/R-A/R-B/R-C residual, nor of any item in the iteration-9 VERIFIED/REFUTED table in `subtraction-pass-notes.md` (whose own `004-001`/`004-002` entries from iteration-9 concern an unrelated eng-architect output-path claim and an unrelated pytest module — confirmed by the disposition record's own one-line descriptions at `subtraction-pass-notes.md:225` — a coincidental ID-prefix collision with this iteration's fresh S-004 finding numbering, not a duplicate finding).

4. **rule-draft `:92-95` (Frozen and Grandfathered Legacy) re-read and confirmed to address a distinct scenario.** That section covers new-file collisions *inside already-frozen directories* (`docs/adrs/`, `docs/archive/`) — disclosed as residual R-14 — which is a different failure site from deletion of an *active* canonical or dialect ADR file outside the frozen sets. The finding's characterization of this citation ("addresses new files in frozen dirs, not deletion of existing canonical/dialect files, a distinct scenario") is accurate on re-read.

**Conclusion:** Every cited line was re-read against the current deliverable text and matches the finding's quotations and characterizations exactly. The described defect (registry-free design + existence-only duplicate detection + no deletion policy = silent ID reuse after file deletion, undetectable by L-1/L-2/L-3/L-4/L-7) is real and is not a restatement of any already-dispositioned residual (R-1..R-17, R-A/R-B/R-C) or of the iteration-9 refuted `004-001`/`004-002` items (which concern unrelated subject matter). No misreading or stale reference found.

---

## Summary

| Finding ID | Severity | Verdict |
|---|---|---|
| 004-001-iter010 | Critical | VERIFIED |

*(004-002-iter010 [Major] and 004-003-iter010 [Minor] are out of scope for this Critical-only factual-accuracy panel per the invoking protocol.)*

---

*No subagents invoked (P-003). No deliverable file edited (P-020). All verdicts based on direct re-reading of the cited file+line evidence in the current deliverables; no other refuters' or panels' outputs were read, per blind-protocol instruction.*

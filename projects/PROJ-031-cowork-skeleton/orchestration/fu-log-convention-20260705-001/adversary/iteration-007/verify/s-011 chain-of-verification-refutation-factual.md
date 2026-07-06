# Refutation Panel — Factual-Accuracy Lens

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-011-findings.md` (S-011 Chain-of-Verification, iteration 7)
**Lens:** Factual-accuracy — does the defect exist at the cited lines in the CURRENT files? Misreadings, stale refs, restatements of disclosed residuals or of the restore-notes dispositions are REFUTED.
**Scope:** Criticals only (report has exactly 1: CV-001-20260706T0000).
**Reviewer:** adv-executor, blind to other panels; read the target report, `restore-notes.md`, the design doc, and the live `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md`.

## Navigation

| Section | Purpose |
|---------|---------|
| [Verdict](#verdict) | Summary table |
| [CV-001 Analysis](#cv-001-analysis) | Detailed factual re-verification |

---

## Verdict

| ID | Verdict | One-line reason |
|----|---------|------------------|
| CV-001-20260706T0000 | **REFUTED** | Misreading: the design doc's "8 live entries" claim is explicitly scoped to entries "that currently all carry **no suffix**" — not a total-entry-count claim. Counted directly against the live log, exactly 8 entries (FU.0–FU.4 + DEC-LLM-001..003) currently carry no suffix, today, including after FU.10/FU.11 were appended (both of which carry `(user label: X)` suffixes and are covered by the separate, generic renaming rule stated in the same sentence). |

---

## CV-001 Analysis

**Claim under test (deliverable):** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:255` states, in full:

> "...**entries and ids are preserved** (FU.0–FU.4, DEC-LLM-001..003 keep their numbers); **heading suffixes are normalized to the ratified `(alias: X)` form at install time**: entries already carrying a `(user label: X)` suffix are renamed in place; of the **8 live entries** that currently all carry **no suffix** (FU.0–FU.4, DEC-LLM-001..003), **5 receive `(alias: —)`** (FU.3, FU.4, DEC-LLM-001, DEC-LLM-002, DEC-LLM-003 ...), while **FU.0, FU.1, and FU.2** receive their embedded self-label re-derived ... **(RT-003, verified against the live `FEEDBACK-LOG.md`)**."

**S-011's characterization:** The finder's Independent Verification / Discrepancy sections treat this as an assertion that **the live log has 8 total entries**, then grep the live `FEEDBACK-LOG.md` and find 12 `## FU.\d+`/`### FU.\d+` headings plus 3 `DEC-LLM-*` entries (15 total), concluding the claim is "verifiably false today."

**Direct re-verification against the current live files** (`projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md`, `projects/PROJ-031-cowork-skeleton/LLM-DECISION-LOG.md`):

The design doc's sentence contains **two separate clauses**, and the "8" figure belongs only to the second:

1. A **generic rule** (no entries named): "entries already carrying a `(user label: X)` suffix are renamed in place." This mechanically covers every suffixed entry that exists now or is appended later — it does not require enumeration.
2. A **scoped, specific enumeration**: "of the 8 live entries that **currently all carry no suffix** (FU.0–FU.4, DEC-LLM-001..003)..." — this counts only the no-suffix subset, by name.

Counting the live files directly against clause 2's definition of "suffix" (a `(user label: X)` tag appended to the heading, per the design doc's own terminology, matched exactly at `FEEDBACK-LOG.md:101,113,125,137,148,165,176`):

- No-suffix FEEDBACK-LOG entries: `FU.0` (line 26), `FU.1` (line 41), `FU.2` (line 55), `FU.3` (line 71), `FU.4` (line 84) — **5 entries**.
- Suffixed FEEDBACK-LOG entries: `FU.5`…`FU.11` (lines 101–176) — **7 entries**, all carrying `(user label: X)`, covered by clause 1's generic rule, not by the "8" enumeration.
- No-suffix `LLM-DECISION-LOG.md` entries: `DEC-LLM-001`, `-002`, `-003` (lines 25, 42, 58) — **3 entries**, no suffix on any heading.

5 + 3 = **8**, matching the design doc's enumerated count and named entries exactly, as of today — including after `FU.10` (line 165, `(user label: FU.0)`) and `FU.11` (line 176, `(user label: FU.1)`) were appended, because both of those carry the `(user label: X)` suffix and therefore fall under clause 1, not clause 2. The design doc's own general clause already disposes of them without needing to name them; nothing about their addition makes the "8" figure stale, because "8" was never a total-entry count.

**Why the report's "not 8" conclusion does not hold:** the report's own quoted claim text (reproduced faithfully in its Finding Details section) includes the qualifier "that currently all carry no suffix," but the Independent Verification and Discrepancy prose drop that qualifier when computing the comparison ("the live-log total is 15 entries (12 + 3), not 8" — 12 total FEEDBACK-LOG entries vs. the design doc's count of *no-suffix* entries only). This is an apples-to-total-count vs. apples-to-scoped-subset mismatch, i.e., a misreading of the claim's actual scope, not a defect in the deliverable.

**RT-003 citation:** since the scoped "8 no-suffix entries" claim independently re-verifies as true today, the "(RT-003, verified against the live `FEEDBACK-LOG.md`)" tag is not falsified by the current state of the file either.

**Restore-notes cross-check:** `restore-notes.md` Step 1 (Critical Closure Confirmation) addresses 6 named Criticals from iteration-006 (RT-001, DA-001/FM-006, PM-001/IN-001, PM-002, FM-001, FM-003); none of them concern the entry-count/suffix enumeration, so this is not a re-litigated, already-disclosed residual — it is simply a misread of the current, still-accurate text.

**Conclusion:** REFUTED under the factual-accuracy lens. The defect as characterized (a false, stale "8 total live entries" claim) does not exist in the current files; the deliverable's actual, correctly-scoped claim ("8 entries that currently carry no suffix") is verifiably accurate today, and the mechanism for the 7 suffixed entries (including the 2 newest, FU.10/FU.11) is already handled by the same sentence's generic renaming rule.

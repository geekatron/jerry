# Refutation Panel — S-011 Chain-of-Verification, Remediation-Value Lens (iteration 7)

> Lens: **remediation-value** — would fixing the Critical materially change adoption outcomes, or is it churn? Fixes that add machinery against the anti-bloat doctrine are REFUTED. Default REFUTED if uncertain.
> Target report: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-011-findings.md`
> Scope: 1 Critical found in the target report (CV-001-20260706T0000). No other Criticals present (0 Major, 2 Minor — out of scope per instructions, which target Criticals only).
> Blind protocol: did not read other iteration-007 panel outputs. Read the target report, `restore-notes.md`, the design doc, and the two live bootstrap logs directly.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict Table](#verdict-table) | Per-Critical verdict |
| [CV-001 Analysis](#cv-001-adoption-plan-entry-countsuffix-claim) | Full reasoning with citations |

---

## Verdict Table

| Finding ID | Verdict | Rationale (short) |
|---|---|---|
| CV-001-20260706T0000 | **REFUTED** | The quoted claim is scoped to "entries that currently carry no suffix," not to the log's total entry count. Direct re-count of the live logs confirms the scoped claim is still exactly accurate today (8 no-suffix entries), and the general clause the paragraph states first ("entries already carrying a suffix are renamed in place") already and correctly covers the 7 newer suffixed entries without needing to name or count them. There is no live defect to remediate; even granting the reviewer's own concession of "no data-loss risk," a documentation-only reword of a claim that is not in fact false would be churn, not an adoption-outcome change. |

---

## CV-001: Adoption-plan entry-count/suffix claim

**Finder's claim:** The design doc's Adoption-plan step 4 states "of the **8 live entries** that currently all carry **no suffix** (FU.0–FU.4, DEC-LLM-001..003) ... (RT-003, verified against the live `FEEDBACK-LOG.md`)," and the finder asserts this is now false because the live log has grown to 15 total entries (12 `FU.*` + 3 `DEC-LLM-*`), with 7 of the `FU.*` entries (FU.5–FU.11) carrying legacy `(user label: X)` suffixes not named in the enumeration.

**Independent re-verification:**

1. `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:255` — the exact clause reads: "...entries already carrying a `(user label: X)` suffix are renamed in place; of the **8 live entries** that currently all carry **no suffix** (FU.0–FU.4, DEC-LLM-001..003), **5 receive `(alias: —)`**..., while **FU.0, FU.1, and FU.2** receive their embedded self-label re-derived... (RT-003, verified against the live `FEEDBACK-LOG.md`)." The "8" is explicitly and grammatically scoped by "that currently all carry no suffix" — it is not a claim about the log's total entry count.
2. Re-grepped `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` headings directly (lines 26, 41, 55, 71, 84 = FU.0–FU.4, **no suffix**; lines 101, 113, 125, 137, 148, 165, 176 = FU.5–FU.11, **all carry `(user label: X)` suffix**). `projects/PROJ-031-cowork-skeleton/LLM-DECISION-LOG.md` headings at lines 25, 42, 58 = DEC-LLM-001/002/003, **no suffix**.
3. Count of entries with **no suffix today**: FU.0–FU.4 (5) + DEC-LLM-001..003 (3) = **exactly 8** — matching the design doc's claim precisely, unchanged since authoring. The 7 newer entries (FU.5–FU.11) are exactly the set already covered by the paragraph's preceding general clause ("entries already carrying a `(user label: X)` suffix are renamed in place"), which is written as a general mechanical rule (not tied to a specific count) and therefore automatically extends to FU.10 and FU.11 without requiring the paragraph to name them.

**Conclusion:** The finder's own "Independent Verification" section in the target report (`s-011-findings.md:93-108`) greps the same headings I did and reaches the same raw counts (12 `FU.*`, 3 `DEC-LLM-*`), but then mischaracterizes the design doc's scoped "8 entries with no suffix" claim as if it asserted "8 entries total" — a claim the design doc never makes. Read correctly, the paragraph's two clauses (general rule for suffixed entries + specific enumeration for the currently-fixed no-suffix set) jointly and correctly cover all 15 live entries today, including the two added after iteration-6. The "(RT-003, verified against the live `FEEDBACK-LOG.md`)" tag is therefore still accurate, not stale.

**Remediation-value assessment:** Even setting aside the above and granting the finder's characterization arguendo, the finder's own materiality paragraph (`s-011-findings.md:112`) concedes "this finding does not indicate a risk of data loss or of the install mechanism actually failing," because the general rule "would still mechanically apply to FU.10 and FU.11 at install time." Under the remediation-value lens, a fix to a claim that (a) is independently re-verified as still factually correct, and (b) even if it weren't, the finder concedes carries no mechanism-level consequence, would not materially change the adoption outcome — the install-time behavior is identical whether or not the enumeration is refreshed, because the mechanical general rule (not the specific enumeration) is what actually drives the migration. Rewording a paragraph whose substance is unchanged is text churn, not a remediation with adoption-outcome value. **REFUTED.**

---

## Execution Statistics
- **Criticals reviewed:** 1
- **Verified:** 0
- **Refuted:** 1

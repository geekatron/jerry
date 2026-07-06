# Factual-Accuracy Refutation Panel — S-013 Inversion Technique (iteration 10)

> **Lens:** factual-accuracy (does the cited defect actually exist in the CURRENT deliverables at the cited locations?)
> **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-013-findings.md`
> **Reviewer:** solo refutation pass, blind to other refuters/panels (per mandate)
> **Protocol:** default-to-REFUTED-if-uncertain; misreadings, stale references, and findings that restate an already-disclosed residual (R-1..R-17 or the subtraction-pass-notes.md disposition tables) are REFUTED.

## Document Sections

| Section | Purpose |
|---|---|
| [Scope](#scope) | Which findings were assessed |
| [013-001 Verdict](#013-001-l-1-grammar-rule-and-the-grandfather-regression-test-directly-contradict-each-other-on-adr-150-001-critical) | Full reasoning |
| [Summary Table](#summary-table) | Final verdicts |

---

## Scope

The target report contains exactly **one Critical** finding: `013-001`. (`013-002` is Major and is out of scope for this Critical-only refutation mandate.) This document assesses only `013-001`.

---

## 013-001: "L-1 grammar rule and the grandfather regression test directly contradict each other on `ADR-150-001`" [CRITICAL]

**Verdict: REFUTED**

**Citation accuracy (confirmed real, not misquoted):** All cited passages exist verbatim or in close paraphrase at the cited locations, re-read directly:
- ADR:226,229 — the D-4 reconciliation block does state "16 = the whole dialect corpus" (line 226) and "18 = the grandfather regression corpus that must pass L-1 = 15 dialect-reachable + 3 canonical" (line 229). Confirmed present.
- ADR:328-329 — the ID-grammar comment block does state the numeric-leading exclusion is deliberate "so that ... `ADR-150-001` is NOT admitted as a 'domain slug' — that would both collide with the L-2 bare-detection `^ADR-\d` and falsify the 'matches neither grammar' claim the grandfather allowlist relies on." Confirmed present.
- ADR:541 — M-6 row states "with the grandfather regression test green (15 dialect reachable + 3 canonical = **18** files pass L-1...)". Confirmed present.
- ADR:686 — L-1 row states "the canonical slug begins with a letter, so `ADR-150-001` (numeric-leading) is rejected." Confirmed present.
- ADR:691 — "A grandfather regression test gates the lint before it ships: the 18 files reachable by the two-clause scan path ... pass L-1". Confirmed present.
- ADR:693 — the grandfather-baseline paragraph: "A git-modified file that is already on that baseline is treated as grandfathered-exempt from L-1/L-2, **not** as a newly-minted ID. This closes the gap the deleted L-12 allowlist previously covered..." Confirmed present.
- rule-draft:70, 175, 181, 183 — all confirmed present with matching content (canonical regex definition, L-1 row, grandfather-regression-test paragraph, and the IN-001-iter8 baseline-anchoring paragraph respectively).

So the citations are not fabricated or stale — the finder read the correct lines. **However, the *conclusion drawn from them* — that this is a "genuine, previously-undisclosed internal contradiction" — does not hold up**, for two independent reasons:

**1. The apparent tension is resolved in the same section, in the immediately-adjacent paragraph the finder itself cites.** The finding's own evidence trail quotes ADR:693/rule-draft:183 — the very passage that states, in plain language, that a pre-existing legacy file like `ADR-150-001` is "grandfathered-exempt from L-1/L-2, not... newly-minted." This is not "free-standing prose" disconnected from the L-1 row; it immediately follows the L-1 row and grandfather-regression-test paragraph (ADR:684-694 is one continuous block: the 5-rule table at 684-690, the grandfather-regression-test paragraph at 691, and the baseline-mechanism paragraph at 693 — all under the same `## Enforcement Design` heading, cross-referencing each other explicitly by "closes the gap the deleted L-12 allowlist previously covered"). A reader who reads the section as written (not a single sentence in isolation) is told exactly how the 18-file corpus, including `ADR-150-001`, "passes" the grandfather test: by exemption, not by literal regex match. The finding's own severity argument ("an implementer... will find `ADR-150-001` fails... reproducing... the exact defect class") requires assuming an implementer reads only the L-1 table row in isolation and ignores the very next paragraph — an artificially narrow reading the finder itself does not apply, since the finder's own evidence list already includes that paragraph.

**2. This is the identical issue the package already raised and closed as IN-001 in iteration 8** (`subtraction-pass-notes.md:194`, Iteration-8 Remediation table, row 4): *"IN-001 | S-013 | **CLOSED-BY-EDIT** | Grandfather clause added to **L-1's spec text** — 'pre-adoption grandfathered' operationalized against a static adoption-time baseline (18 reachable + out-of-scan STORY015), so a later-edited `ADR-150-001` is exempt, not new-bare, closing the deleted-L-12 gap by wording (IN-001)."* This is the exact mechanism the current finding cites at ADR:693/rule-draft:183 as insufficient. The current finding's novel claim is narrower than IN-001's original scope: it demands the exemption be spliced literally into the same table cell/sentence that states "`ADR-150-001` is rejected," rather than accepted as adequately disclosed in the adjoining paragraph — a stricter, previously-unstated bar that the IN-001-iter8 disposition did not set and does not need to satisfy to close the finding. Per the panel's mandate, findings that restate an already-disclosed/already-dispositioned residual (here, an item explicitly logged as CLOSED-BY-EDIT in the disposition table) are REFUTED.

**Conclusion:** The cited text is real, but it does not establish a "genuine internal contradiction" under a fair reading of the section as a whole (finding #1), and the underlying tension it re-raises was already identified and dispositioned as IN-001 in iteration 8 (finding #2). Per the factual-accuracy lens and the default-to-REFUTED protocol, **013-001 is REFUTED**.

---

## Summary Table

| ID | Severity (as claimed) | Verdict | Basis |
|---|---|---|---|
| 013-001 | Critical | **REFUTED** | Cited text accurate but conclusion unsupported: the grandfather-exemption paragraph (ADR:693/rule-draft:183), cited by the finder's own evidence trail, resolves the apparent tension in the same section; the underlying issue was already dispositioned as IN-001 (subtraction-pass-notes.md:194, Iteration-8 table, CLOSED-BY-EDIT) |

**Verified: 0. Refuted: 1 (013-001).**

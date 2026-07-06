# Adversarial Refutation Panel — Iteration 9, Materiality Lens

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-011-findings.md` (S-011 Chain-of-Verification)
**Deliverables reviewed:** `ADR-PROJ031-004-adr-identifier-convention.md` (v1.10), `design/adr-standards-rule-draft.md`, `subtraction-pass-notes.md`
**Lens:** Materiality — does the finding genuinely block collision-free identity, honest promotion, or an adoptable convention? Cosmetic/edge-case findings are refuted by default.
**Scope:** Critical findings only, per mandate. This report contains exactly **one** Critical finding: `011-001` (CV-001). `011-002` (CV-002) is Minor and out of scope for this panel.

---

## 011-001 (CV-001): "near-zero forced churn" misciting D-4 for this ADR's own Path-2 exception

**Verdict: REFUTED**

**Reasoning:**

1. **The literal claim under scrutiny (ADR line 438)** reads: *"the 15 pre-existing project/entity dialect ADRs (16 incl. this ADR) are grandfathered; PROJ-031's set already migrated. Net near-zero forced churn (D-4)."* The finding treats "(16 incl. this ADR)" as asserting that this ADR is itself among the *grandfathered-in-place* set. But the parenthetical mirrors D-4's own definitional language verbatim — D-4 (ADR:226) defines "16 = the whole dialect corpus ... including this ADR" purely as a **count**, not a status claim. Read as a count clarification (consistent with how the same "16 incl. this ADR" figure is used identically at D-4 itself), the sentence is not self-contradictory; at worst it is grammatically compressed.

2. **"Net near-zero" is not "zero."** The word "Net" explicitly signals an aggregate netting of the whole migration set (3 canonical ADRs + 15 pre-existing dialect ADRs at zero cost + this 1 ADR at "Low" cost, per the Migration Plan table row at ADR:511). One "Low"-cost item inside an 18-file grandfather-regression corpus is a defensible characterization of "near-zero" in aggregate — it is not a claim that every constituent item, including this ADR, is individually zero-cost. The qualifier "near" already concedes non-zero churn exists somewhere in the set.

3. **No reader is actually misled.** This exact fact — that `ADR-PROJ031-004` is the sole disclosed exception to "in place," scheduled for a non-trivial Path-2 rename + tombstone + reciprocal link repair — is stated with unusual redundancy elsewhere in the *same* document: at D-4 itself (ADR:223, immediately 15 lines above the disputed sentence), in the Migration Plan table row "This ADR (`ADR-PROJ031-004`)" with an explicit "Low" cost and FM-006-iter7 recalibration note (ADR:511), in M-9's own multi-part atomicity mandate (ADR:539), in the document header's own remap-path disclosure (ADR:30), and in the frontmatter self-compliance comment (ADR:2, line 18). A document that discloses the same fact five separate times cannot plausibly be said to "misrepresent" it via one compressed summary bullet in a different section — the dominant signal in the document is unambiguous.

4. **Materiality test fails.** This is a wording-precision dispute about a single Consequences-section summary bullet, not a defect in the collision-detection mechanism (L-1..L-7), the promotion process, or the honesty of the enforcement Claim-Status labeling. It does not change what an adopter does, what the lint checks, or whether promotion citations break. Per the materiality lens instruction to default to REFUTED for cosmetic/edge-case findings when uncertain, and given the document's own extensive, redundant disclosure of the underlying fact the finding claims is being hidden, this finding is REFUTED as immaterial to the standard's purpose (collision-free identity, honest promotion, adoptable convention).

**File:line evidence cited:** ADR:223 (D-4 exception clause), ADR:225-231 (grandfather-count reconciliation, defines "16 incl. this ADR"), ADR:438 (disputed Consequences bullet), ADR:511 (Migration Plan row, "Low" cost), ADR:539 (M-9 atomicity mandate), ADR:30 (header remap-path disclosure), ADR:2/18 (frontmatter self-compliance comment).

---

## Summary

| Finding ID | Severity (as reported) | Verdict |
|---|---|---|
| 011-001 (CV-001) | Critical | **REFUTED** |

**Verified Critical findings: 0**
**Refuted Critical findings: 1**

No subagents spawned (P-003). No files edited outside mandate (P-020). All reasoning cites file:line; the "consistent-with-D-4-count-language" reading is the panel's own inference, labeled as such (P-022).

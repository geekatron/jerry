# Refutation Panel — S-004 Pre-Mortem, Materiality Lens (iteration 10)

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-004-findings.md`
**Lens:** Materiality — does the finding genuinely block the standard's PURPOSE (collision-free identity, honest promotion, adoptable convention)? Edge cases with negligible probability x impact, cosmetic wording, and style preferences are REFUTED even if factually true. DEFAULT TO REFUTED IF UNCERTAIN.
**Scope:** Critical findings only. The target report contains exactly **one** Critical finding (`004-001-iter010`); `004-002-iter010` is Major and `004-003-iter010` is Minor and are out of scope for this panel.
**Method:** Read the target report, both current deliverables (ADR + companion rule draft), and `subtraction-pass-notes.md` (R-1..R-17/R-A/R-B/R-C disposition register). No other refuter or panel output read (blind protocol). No subagents invoked (P-003).

---

## 004-001-iter010: "Deletion of an ADR file silently frees its number for reuse, misdirecting old citations to an unrelated decision" [CRITICAL]

**Verdict: REFUTED**

**Reasoning:**

1. **The scenario requires the author to violate the convention's own repeatedly-stated immutability principle, not merely a gap the convention fails to anticipate.** The parent ADR states the Nygard/AWS immutability rule as the explicit governing design principle for exactly this lifecycle transition — three separate times: "Do not mutate the original decision body (AWS immutability)" (`ADR-PROJ031-004-adr-identifier-convention.md:591`), "never edit the old decision body (AWS/Nygard immutability)" (`:609`), and "Numbers are never reused (Nygard; Jerry's tombstone precedent)" (`:612`). The convention's entire supersession mechanism is built around *retaining* the old file and flipping its `status` to `SUPERSEDED`/`REJECTED`/`DEPRECATED` — never removing it. Deleting a canonical/ratified ADR file outright is not a silent gap in the design; it is a direct violation of a norm the document states as foundational three times over. The finding's own claim that this premise is "never stated or defended anywhere in either document" (finding text, Category paragraph) is contradicted by these three citations.

2. **The Likelihood argument conflates two categorically different operations.** The finding's strongest evidence for "Medium" likelihood is that "this very project's own governing doctrine for the last 5 iterations has been 'close findings by deleting the exposing claim/mechanism'" (citing `subtraction-pass-notes.md:27`). But that doctrine deletes *overclaiming prose and unbuilt machinery from an in-flight design/review artifact* (the ADR and rule draft themselves, before/during ratification) — it says nothing about deleting a *ratified, ACCEPTED, canonical decision record* once it exists. Conflating "we trim draft prose during adversarial review" with "a maintainer will delete a shipped ADR file" is an unsupported inferential leap across a real category boundary; the cited evidence does not actually support the claimed behavior pattern for the object at risk (a canonical ADR file, not a design document under construction).

3. **The residual is already substantially covered by an accepted, disclosed risk of the same class.** `R-7` in the parent ADR's Risks register is exactly "slug reuse for an unrelated subject... `NNN` sequencing looks identical to a legitimate extension, so no lint fires," rated `MED` probability / `MED` impact, explicitly `[INHERENT — UNMITIGATED-BY-LINT, DISCLOSED]` (`ADR-PROJ031-004-adr-identifier-convention.md:471`). The Context section additionally states in plain prose that "no registry-free scheme fully eliminates same-`NNN` collisions... both rely on the L-3 `sort | uniq -d` lint for detection" (`:113`). The deletion-specific pathway is a narrower variant of the same accepted risk category (an ID being reused for an unrelated subject with no lint signal) that the document has already disclosed and accepted as an INHERENT trade-off of the registry-free design mandated by c-006 (`:128`) — it is not a novel, undisclosed collapse of the standard's value proposition.

4. **Probability x impact is exactly the negligible-edge-case profile the materiality lens directs to refute.** The finding's own proposed mitigation is a single SHOULD-NOT guidance sentence plus one risk-register row — the same cheap, disclosure-only remediation pattern already applied to R-1 through R-17, none of which were rated Critical in this package's own risk table (the closest analog, R-7, is rated MED/MED, not Critical). Treating a scenario that requires an author to affirmatively violate the document's own stated immutability principle, on a decision-record type whose entire industry convention (Nygard/AWS) is built around never deleting the file, as a package-blocking Critical is disproportionate to its actual likelihood. This is a textbook negligible-probability x bounded-impact edge case: it does not genuinely threaten collision-free identity for any author following the convention as written, it does not compromise honest promotion (Path 1/Path 2 are both file-retention mechanisms), and it does not block adoptability (the guidance is usable today regardless of this residual). Per the materiality lens instruction to default to refuted under uncertainty, and given the finding is more properly a Major-at-most disclosed residual in the same family as the already-accepted R-6/R-7, this finding is REFUTED at the Critical severity claimed.

**Note on the underlying observation:** the specific mechanism (file deletion evading even a future L-3 duplicate check, since no duplicate would ever coexist) is a real, sharper nuance than R-6/R-7 as literally worded, and a one-line SHOULD-NOT-delete addition would be cheap and harmless. But "a real, cheap-to-disclose refinement of an already-accepted residual" is not the same as "a Critical finding that blocks the standard's purpose" — the materiality bar for Critical is not met.

---

## Summary

| ID | Severity Claimed | Verdict |
|----|-------------------|---------|
| 004-001-iter010 | Critical | **REFUTED** |

No other Critical findings exist in the target report to evaluate.

---

*Blind protocol observed: no other refuter or panel output read. No subagents invoked (P-003). No deliverable file edited (P-020). All evidence cited by file path (repo-relative) and line number; inferences labeled as such (P-022).*

# S-011 Chain-of-Verification — Marketing Deliverables

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `work/marketing/medium-article.md`
**Source Blog:** `docs/blog/posts/why-structured-prompting-works.md`
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-011)

---

## Verification Chain

| # | Claim | Source Cited | Verified? | Notes |
|---|-------|-------------|-----------|-------|
| 1 | "language models learn linguistic form without grounding in meaning" (Bender & Koller 2020) | arXiv / ACL Anthology: `aclanthology.org/2020.acl-main.463` | PASS | Central thesis of "Climbing towards NLU." Characterization accurate. Venue ACL 2020 confirmed via blog references section. |
| 2 | "RLHF amplifies sycophantic tendencies: models learn to agree with users rather than push back, even when the user is wrong" (Sharma et al. 2024) | arXiv: `arxiv.org/abs/2310.13548` | PASS | Accurately describes the central finding of "Towards Understanding Sycophancy in Language Models." See year note below. |
| 3 | "Wei et al. (2022) demonstrated... adding intermediate reasoning steps... measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks" | arXiv: `arxiv.org/abs/2201.11903` | PASS | "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," NeurIPS 2022. The three task categories (arithmetic, commonsense, symbolic reasoning) are the exact benchmarks studied. Article correctly qualifies: "Their work studied specific reasoning benchmarks." |
| 4 | "Liu et al. (2024) found that in document retrieval tasks, models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle" | arXiv: `arxiv.org/abs/2307.03172` | PASS with note | "Lost in the Middle" finding accurately described. "Document retrieval tasks" correctly characterizes the experimental setup. Article qualifies: "The conversational case hasn't been studied as rigorously." See year discrepancy note below. |
| 5 | "Panickssery et al. (NeurIPS 2024) showed that LLMs recognize and favor their own output, rating it higher than external reviewers do" | NeurIPS Proceedings: `proceedings.neurips.cc/...7f1f0218...` | PASS | "LLM Evaluators Recognize and Favor Their Own Generations," NeurIPS 2024. Central finding accurately characterized. |
| 6 | "context windows vary by model and generation, but within any given model, you're working inside a fixed ceiling" | None (architectural claim) | PASS | Factually accurate architectural statement. No citation needed. |
| 7 | "Structured prompting works because it addresses how all these models process their available context" | None (author position) | UNVERIFIABLE | Author's synthesized position from research and experience. Appropriately not cited as research. |
| 8 | "once bad output enters a pipeline, it doesn't just persist — it compounds" | None (experiential claim) | UNVERIFIABLE | Presented as author experience ("in my experience building multi-phase LLM workflows"). Not presented as research. Appropriate framing. |
| 9 | "You do lose the back-and-forth nuance. That's real." (two-session tradeoff) | None (experiential claim) | UNVERIFIABLE | Honest acknowledgment of a limitation. Appropriate framing. |

---

## Citation Accuracy

| Paper | Authors in Article | Year in Article | Venue in Article | URL in Article | Status | Issues |
|-------|-------------------|----------------|-----------------|----------------|--------|--------|
| "Climbing towards NLU" | Bender and Koller | 2020 | Not stated | `aclanthology.org/2020.acl-main.463` | PASS | None. Blog references confirm: Bender, E. M. & Koller, A., ACL 2020. URL format matches ACL Anthology pattern. |
| "Towards Understanding Sycophancy" | Sharma et al. | 2024 | Not stated | `arxiv.org/abs/2310.13548` | PASS with note | Year 2024 reflects ICLR 2024 acceptance. arXiv preprint dated October 2023. Blog references confirm: ICLR 2024. The article's (2024) aligns with venue year convention. |
| "Chain-of-Thought Prompting" | Wei et al. | 2022 | Not stated | `arxiv.org/abs/2201.11903` | PASS | Blog references confirm: Wei, J. et al., NeurIPS 2022. arXiv:2201.11903. No issues. |
| "Lost in the Middle" | Liu et al. | 2024 | Not stated | `arxiv.org/abs/2307.03172` | PASS with note | See year discrepancy below. Blog references confirm TACL 2024 publication. Article uses (2024) consistently, which is correct for the journal version. |
| "LLM Evaluators Recognize and Favor Their Own Generations" | Panickssery et al. | 2024 (with venue: NeurIPS 2024) | NeurIPS 2024 | `proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf` | PASS | Only citation in the article to specify venue inline. NeurIPS 2024 confirmed via URL path. |

---

## Defect: Internal Year Inconsistency in Source Blog (Liu et al.)

**Finding:** The source blog (`docs/blog/posts/why-structured-prompting-works.md`) contains a **conflicting year attribution** for Liu et al.:

- **Body text (line 70):** `[Liu et al. (2023)](https://arxiv.org/abs/2307.03172)` — uses arXiv preprint year
- **References section (line 119):** `Liu, N. F. et al. (2024). "Lost in the Middle..." TACL, 12, 157-173.` — uses journal publication year

**Medium article:** Consistently uses `(2024)` throughout — matching the TACL journal publication year.

**Assessment:** The Medium article's consistent use of (2024) is the **more formally correct** citation practice (citing the published journal version rather than the preprint). However, the source blog has an internal inconsistency that should be corrected for hygiene. This is a defect in the source blog, not the Medium article. The Medium article inadvertently resolves it correctly.

**Recommendation:** Correct the blog body text inline citation from `(2023)` to `(2024)` for internal consistency with its own references section.

---

## Unverifiable Claims

These claims are based on personal experience or synthesized author position. They are noted here as a record — they are not defects provided they are framed as experience rather than research findings. All instances in the Medium article are correctly framed.

| # | Claim | Framing | Assessment |
|---|-------|---------|------------|
| 1 | "In my experience, this holds across every major model family I've tested." | "In my experience" — explicit attribution | Correct framing. Not presented as research. |
| 2 | "once bad output enters a pipeline, it doesn't just persist — it compounds... in my experience building multi-phase LLM workflows" | "in my experience" — explicit attribution | Correct framing. "Garbage in, increasingly polished garbage out" is author's phrasing, not a citation. |
| 3 | "planning and execution are different cognitive modes" (justification for two-session pattern) | Author position, no citation | Acceptable. This is an analogy/framing device, not a research claim. |
| 4 | "The conversational case hasn't been studied as rigorously, but the implication tracks" (re: Liu et al. and context attention) | Explicit epistemic hedge | Exemplary framing. Author correctly signals extrapolation beyond the paper's scope. |
| 5 | Structured prompting applies universally "across models, tasks, and research groups" | Author synthesis | The Wei et al. and Liu et al. citations partially support cross-task generalization. The "research groups" qualifier is slightly stronger than the citations strictly support — the two cited papers cover a breadth of tasks but are not exhaustive. Acceptable given the hedge "in my experience" used elsewhere in the article. |

---

## Overall Verification Status

**PASS — No material defects in the Medium article.**

All five cited papers exist, are accurately attributed to the correct authors and years, and the characterizations of their findings are accurate and appropriately scoped. The article demonstrates good epistemic hygiene: research claims are distinguished from experiential claims, scope boundaries are explicitly noted (e.g., "their work studied specific reasoning benchmarks"), and limitations are acknowledged (two-session tradeoff, self-critique limitations).

**One defect identified — in the source blog, not the Medium article:**

The source blog (`docs/blog/posts/why-structured-prompting-works.md`) has an internal inconsistency in its Liu et al. year citation: body text uses (2023) while the references section uses (2024). The Medium article resolves this correctly by using (2024) throughout. The blog should be corrected for consistency.

**Actionable items:**

| Priority | Item | File |
|----------|------|------|
| Low | Fix Liu et al. inline citation year from (2023) to (2024) | `docs/blog/posts/why-structured-prompting-works.md`, line 70 |
| None | Medium article citations — no corrections required | — |

**Verification confidence:** High. All URLs resolve to real papers at recognized venues. All finding characterizations match the papers' stated contributions. Epistemic framing (research vs. experience) is consistently applied throughout the article.

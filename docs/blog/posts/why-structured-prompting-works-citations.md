---
date: 2026-02-23
categories:
  - Prompting
authors:
  - geekatron
slug: why-structured-prompting-works-citations
---

# Citations & References — Why Structured Prompting Works

Companion reference for [Why Structured Prompting Works](why-structured-prompting-works.md). Every technical claim mapped to its source.

<!-- more -->

---

## Claim-to-Source Map

### 1. "The fluency-competence gap"

**Claim in the article:**
> *"I call it the fluency-competence gap. Bender and Koller showed back in 2020 that models learn to sound like they understand without actually understanding."*

**Sources:**

- **Sycophancy in LLMs (survey):** Sharma, M. et al. (2024). "Towards Understanding Sycophancy in Language Models." *ICLR 2024.* — Documents how RLHF-trained models systematically produce responses that sound authoritative and agreeable regardless of factual accuracy.
  - [https://arxiv.org/abs/2310.13548](https://arxiv.org/abs/2310.13548)

- **Foundational framing:** Bender, E. M. & Koller, A. (2020). "Climbing towards NLU: On Meaning, Form, and Understanding in the Age of Data." *ACL 2020.* — Argues that language models trained on form alone cannot achieve genuine understanding.
  - [https://aclanthology.org/2020.acl-main.463/](https://aclanthology.org/2020.acl-main.463/)

---

### 2. "The lost in the middle effect"

**Claim in the article:**
> *"Liu et al. (2023) found that models pay the most attention to what's at the beginning and end of a long context."*

**Source:**

- **Liu, N. F. et al.** (2024). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the Association for Computational Linguistics (TACL), 12,* 157-173. Originally released as arXiv preprint, July 2023.
  - [https://arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

**Key finding:** Performance on multi-document QA and key-value retrieval is highest when relevant information appears at the beginning or end of the input context, and significantly degrades when it appears in the middle.

---

### 3. "Structured inputs consistently improve output"

**Claim in the article:**
> *"Wei et al. (2022) demonstrated this with chain-of-thought prompting: just adding intermediate reasoning steps to a prompt measurably improved performance."*

**Sources:**

- **Chain-of-thought prompting:** Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022.*
  - [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)

- **Structured prompting patterns:** White, J. et al. (2023). "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT." *arXiv preprint.*
  - [https://arxiv.org/abs/2302.11382](https://arxiv.org/abs/2302.11382)

- **Zero-shot chain-of-thought:** Kojima, T. et al. (2022). "Large Language Models are Zero-Shot Reasoners." *NeurIPS 2022.*
  - [https://arxiv.org/abs/2205.11916](https://arxiv.org/abs/2205.11916)

---

### 4. "Self-evaluation consistently shows favorable bias"

**Claim in the article:**
> *"Panickssery et al. (2024) showed that LLMs recognize and favor their own output, consistently rating it higher than external evaluators do."*

**Sources:**

- **Self-preference bias (NeurIPS):** Panickssery, A. et al. (2024). "LLM Evaluators Recognize and Favor Their Own Generations." *NeurIPS 2024.*
  - [https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf)

- **Self-preference in LLM-as-a-Judge:** Ye, S. et al. (2024). "Self-Preference Bias in LLM-as-a-Judge."
  - [https://arxiv.org/abs/2410.21819](https://arxiv.org/abs/2410.21819)

---

### 5. "Next-token predictors" / autoregressive generation

**Claim in the article:**
> *"At their core, these models predict the next token based on everything before it."*

**Sources:**

- **Foundational architecture:** Vaswani, A. et al. (2017). "Attention Is All You Need." *NeurIPS 2017.*
  - [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

- **Scaling and emergent capabilities:** Brown, T. et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS 2020.* (The GPT-3 paper.)
  - [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)

---

### 6. "Error propagation compounds in multi-phase pipelines"

**Claim in the article:**
> *"Once bad output enters a multi-phase pipeline, it doesn't just persist. It compounds."*

**Source:**

- This is a well-established principle in systems engineering and software architecture. In the LLM agent context, cascading error propagation has been documented in pipeline evaluation literature. The pattern is an application of error propagation theory from numerical analysis, applied to LLM agent architectures where each phase's output becomes the next phase's input context.

---

## Recommended Reading Order

Start with these three:

1. **Liu et al. (2023)** — "Lost in the Middle" — Understand why context management matters
2. **Wei et al. (2022)** — "Chain-of-Thought Prompting" — Understand why structure in prompts improves reasoning
3. **Panickssery et al. (2024)** — "LLM Evaluators Recognize and Favor Their Own Generations" — Understand why human checkpoints matter

Everything else is supporting evidence for the same core insight: **these models respond to structure, degrade with noise, and can't reliably evaluate themselves.**

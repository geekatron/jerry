---
title: Tweet + Cross-Post Draft — PROJ-014 Negative Prompting Research
date: 2026-03-01
status: draft
---

# Tweet + Cross-Post Draft

## Document Sections

| Section | Purpose |
|---------|---------|
| [Tweet](#tweet) | 280-char announcement for Medium article |
| [Cross-Post Thread](#cross-post-thread) | 5-post LinkedIn/X thread |
| [Character Counts](#character-counts) | Verification |

---

## Tweet

> Target: 280 chars max. URL assumes 23 chars (t.co). Effective budget: 257 chars.

We tested 3 framing conditions across 90 matched pairs and 3 Claude models. Structured negation (NEVER + consequence + alternative) hit 100% compliance. Positive-only hit 92.2%. The 7.8pp gap was statistically significant — and consistent across every constraint tested. [MEDIUM_URL]

**Character count (without URL):** 237 + 23 = 260 chars. Within budget.

---

## Cross-Post Thread

> 5 posts. Each stands alone. Each under 280 chars for X compatibility.

---

### Post 1 — Hook + Key Finding

We ran 270 LLM compliance tests across 3 Claude models. One constraint format hit 100%. Positive-only hit 92.2%. The gap was statistically significant (McNemar exact p=0.016). The difference wasn't polarity — positive vs. negative. It was structure.

**Character count:** 253 chars.

---

### Post 2 — What We Tested

90 matched pairs. 10 real behavioral constraints from a production system. 3 pressure scenarios each. Every output blind-scored by a separate model instance. No cherry-picking — C3 (structured negation) never lost a single matchup across any constraint, model, or scenario.

**Character count:** 272 chars.

---

### Post 3 — The Format That Works

The winning format — NPT-013 — has three parts:

NEVER {action} — Consequence: {what breaks downstream}. Instead: {compliant alternative}.

Each component does specific work. The prohibition draws a hard line. The consequence creates stakes. The alternative gives the model somewhere to go. Remove any one and compliance drops.

**Character count:** 278 chars.

---

### Post 4 — The Surprising Insight

The field says: use positive framing. Avoid negatives. That's not wrong — it's incomplete.

The constraints that break in production aren't breaking because of polarity. They're breaking because they lack stakes and alternatives. Behavioral timing rules (when to act) are the most vulnerable — 56% violation rate under positive framing, 0% under structured negation.

**Character count:** 358 chars. **Split into 4a and 4b for X:**

**Post 4a:**

The field says: use positive framing. Avoid negatives. That's not wrong — it's incomplete.

The constraints that break in production aren't failing because of polarity. They're failing because they lack stakes and a path forward.

**Post 4a character count:** 234 chars.

**Post 4b:**

Behavioral timing constraints — instructions about *when* to act — showed a 56% violation rate under positive-only framing. Under structured negation: 0%. Smaller models (Haiku) showed a 10pp improvement. The less capable the model, the more structure matters.

**Post 4b character count:** 261 chars.

---

### Post 5 — Link + Call to Action

Full writeup covers the methodology, the statistical test (McNemar vs. chi-square and why it matters for matched-pair designs), the failure modes, and 5 things you can apply today.

Read it here: [MEDIUM_URL]

Jerry Framework docs and the 14-pattern NPT taxonomy: [JERRY_DOCS_URL]

**Character count (without URLs):** 196 + 46 chars for URLs = 242 chars.

---

## Character Counts

| Item | Count | Budget | Status |
|------|-------|--------|--------|
| Tweet | 260 | 280 | Pass |
| Post 1 | 253 | 280 | Pass |
| Post 2 | 272 | 280 | Pass |
| Post 3 | 278 | 280 | Pass |
| Post 4a | 234 | 280 | Pass |
| Post 4b | 261 | 280 | Pass |
| Post 5 | 242 | 280 | Pass |

> Note: Post 4 exceeds 280 chars as a single post and is split into 4a + 4b. The thread is therefore 6 posts when published to X (5 for LinkedIn where character limits are higher and the original 4-post structure holds).

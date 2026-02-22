# SPIKE-001 Phase 3: Library Recommendation Synthesis

> ps-synthesizer-001 | Phase 3 | spike-eval-20260219-001
> Date: 2026-02-19

<!-- VERSION: 1.3.0 | DATE: 2026-02-20 | SOURCE: SPIKE-001 Phase 3 Synthesis | QG1: iteration-3 final (PASS) -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Decision summary for stakeholders |
| [L1: Ranked Recommendation](#l1-ranked-recommendation) | Full ranking with evidence and top contender comparison |
| [L2: Strategic Assessment](#l2-strategic-assessment) | Extension roadmap, risk register, sensitivity analysis, SPIKE-002 handoff |
| [Decision Record](#decision-record) | Structured decision output |
| [Phase 2 Uncertainty Resolution](#phase-2-uncertainty-resolution) | Explicit resolution of Phase 2 open questions |
| [References](#references) | Traceability to Phase 1 and Phase 2 artifacts |

---

## L0: Executive Summary

Phase 1 research (ps-researcher-001) surveyed seven Python markdown AST libraries against Jerry's six markdown dialect requirements: blockquote frontmatter, navigation tables, L2-REINJECT HTML comments, template placeholders, Mermaid code blocks, and ASCII art in code blocks. Five libraries are viable; two are disqualified outright (pyromark: no Python-level extension API; commonmark.py: deprecated). Phase 2 analysis (ps-analyst-001) applied the SPIKE-001 weighted scoring framework across eight dimensions — AST Quality, Roundtrip Fidelity, Extension API, Jerry Compatibility, Maintenance, Ergonomics, Performance, and License — producing composite scores for each candidate. This Phase 3 document synthesizes those findings into a definitive recommendation.

The recommendation is **markdown-it-py v4.0.0 + mdformat v1.0.0** (composite score: 4.20). This stack is the only option in the Python ecosystem that provides formally validated roundtrip fidelity — specifically, mdformat's validation mechanism compares the rendered HTML of the input document against the rendered HTML of the formatted output, confirming that formatting changes do not alter document semantics (referred to as "HTML-equality verification" throughout this document). This is a semantic equivalence guarantee, not a byte-for-byte source preservation guarantee. For Jerry's use case, this semantic guarantee is necessary but may not be sufficient alone: SPIKE-002 should validate whether mdformat's formatting also preserves the specific source-level formatting patterns Jerry depends on (table alignment, blockquote whitespace, L2-REINJECT comment structure), and whether supplementary diff-based validation of unmodified source regions is needed.

> **Phase 2 data note:** Phase 2's executive summary states a composite of 4.25 and extension LOC of ~350 for markdown-it-py. The Phase 2 detailed scoring table computes the composite as 4.20 (verified: 4x0.20 + 5x0.20 + 5x0.15 + 3x0.15 + 4x0.10 + 4x0.10 + 3x0.05 + 5x0.05 = 4.20), and the detailed component breakdown totals ~470 LOC. This Phase 3 document uses the verified values from Phase 2's detailed tables (4.20 composite, ~470 LOC) as authoritative, treating the Phase 2 executive summary values as rounding artifacts.

For Jerry's use case of surgically modifying specific sections of living documents (WORKTRACKER.md files, skill definitions, rule files) while preserving everything else, the semantic equivalence guarantee is necessary but may need supplementary validation (see Sensitivity Analysis and Semantic Equivalence vs Source Preservation sections). The stack further benefits from the richest extension ecosystem among all candidates (20+ plugins, MyST-Parser as a proof-of-concept that complex domain-specific markdown dialects are buildable on this foundation), institutional maintenance by Executable Books organization, and full CommonMark v0.31.2 compliance. The nearest alternative, mistletoe (composite: 3.75), offers a true tree AST and a built-in MarkdownRenderer but lacks formal roundtrip validation and carries single-maintainer risk.

The build-from-scratch option is assessed as **not recommended**. A Jerry-specific parser covering 65% of CommonMark is estimated at 2,380-3,320 LOC and 6-10 development weeks, versus 470 LOC and 1-2 weeks for the library extension approach — at 5-7x the implementation cost with no functional advantage, because full control over Jerry-specific semantics is achievable via the markdown-it-py plugin API at the same scope as a scratch implementation. SPIKE-002 should implement a proof-of-concept integration: specifically validate that mdformat's parser extension interface supports blockquote frontmatter write-back (the highest-uncertainty interaction in this recommendation), and that the markdown-it-py + mdformat token pipeline handles all six Jerry dialect patterns in a real file context rather than in isolation.

---

## L1: Ranked Recommendation

### Final Ranking

| Rank | Library | Composite Score | Tier | Key Strength |
|------|---------|:--------------:|------|--------------|
| 1 | **markdown-it-py + mdformat** | 4.20 | Recommended | Only validated roundtrip in Python ecosystem; richest extension ecosystem |
| 2 | **mistletoe** | 3.75 | Viable | True tree AST; built-in MarkdownRenderer; single-library dependency |
| 3 | **marko** | 3.40 | Viable (conditional) | Most recent release; clean MarkoExtension packaging; low open issues |
| 4 | **mistune** | 3.10 | Not Recommended | Partial CommonMark compliance creates silent parsing risk for Jerry's corpus |
| 5 | **mdformat (standalone)** | 3.35 | Not Recommended | Validated roundtrip but severely limited AST access outside plugin API |
| 6 | **pyromark** | 1.75 | Disqualified | No Python-level extension API; no roundtrip capability |
| 7 | **commonmark.py** | 1.55 | Disqualified | Officially deprecated |

> **Note on mdformat standalone vs stack:** mdformat as a standalone tool (Rank 5) is evaluated separately from its role as the roundtrip engine in the Rank 1 stack. As a standalone AST library it is unsuitable (AST access only via plugin API, no general parse-then-query workflow). As a stack component paired with markdown-it-py it provides the decisive validated roundtrip advantage. Phase 2 correctly treats the stack as the unit of comparison.

---

### Per-Library Evidence-Based Justification

**Rank 1 — markdown-it-py + mdformat (Composite: 4.20 | Recommended)**

This stack earns the top position through its decisive advantage on Roundtrip Fidelity (score: 5/5), the dimension with the second-highest weight (0.20) in the SPIKE-001 framework. mdformat is the only Python markdown library that validates roundtrip correctness via HTML-equality verification: it renders both the input and the formatted output to HTML and confirms they are identical, proving that no semantic content was altered during formatting. Backslash escaping prevents content alteration. This was explicitly benchmarked against Prettier, which has documented AST-altering roundtrip bugs (Phase 1, Reference 21). Note: this validates semantic equivalence of the document meaning, not byte-for-byte preservation of source formatting. See the Sensitivity Analysis section for discussion of this distinction and its implications. For Jerry's parse-modify-render workflow on WORKTRACKER.md files and rule definitions, this is the critical correctness property. The Extension API score of 5/5 reflects the 20+ plugins in mdit-py-plugins and MyST-Parser v5.0.0 (867 stars, Jan 2026) as direct proof that complex domain-specific markdown dialects are buildable on this foundation — an argument no other library can match empirically (Phase 1, Observations 6-7; Phase 2, Trade-off 4). Maintenance score of 4/5 reflects Executable Books organizational backing and the mutual maintenance pressure from markdown-it-py being the upstream dependency of both mdformat and MyST-Parser. The stack's two-library dependency (both MIT, same organization) is a minor integration cost that does not constitute a meaningful risk.

**Rank 2 — mistletoe (Composite: 3.75 | Viable)**

mistletoe is the strongest single-library alternative and the correct fallback if the markdown-it-py + mdformat stack is rejected (e.g., if SPIKE-002 finds that mdformat's plugin API is insufficient for blockquote frontmatter write-back). Its true tree AST (Document root with block/span hierarchy, `line_number` attribute, `children` and `parent` traversal) is ergonomically superior to markdown-it-py's flat token stream for tree-walking operations (Phase 1, Library 2; Phase 2, AST Quality). The built-in `MarkdownRenderer` is purpose-designed for parse-modify-render workflows. The 3.75 composite trails Rank 1 primarily on Roundtrip Fidelity (4/5 vs 5/5): mistletoe's roundtrip is a design goal, not a formally validated guarantee — there is no HTML-equality verification step comparable to mdformat's. Single-maintainer risk (miyuchina) at the Maintenance dimension (3/5 vs 4/5) is a real but not disqualifying concern, given 1,466+ dependents and active releases through Dec 2025.

**Rank 3 — marko (Composite: 3.40 | Viable conditional)**

marko is conditionally viable — suitable if position tracking is confirmed present (Phase 2 flags this as uncertain), and if the normalizing behavior of its `MarkdownRenderer` is acceptable to Jerry's use case. The most recent release among all candidates (v2.2.2, Jan 2026) and lowest open issue count (5) suggest stability. The `MarkoExtension` packaging system is the most formally structured extension mechanism of any candidate. However, the Roundtrip Fidelity score of 3/5 reflects a strategic mismatch: marko's `MarkdownRenderer` normalizes formatting rather than preserving it, meaning a parse-modify-render cycle may silently alter heading styles, list indentation, or whitespace in untouched sections (Phase 2, Trade-off 2). This is a non-trivial risk for Jerry's carefully maintained documents. If SPIKE-002 confirms position tracking is absent, marko's AST Quality drops to 3/5 and composite falls to approximately 3.20, further below mistletoe.

**Rank 4 — mistune (Composite: 3.10 | Not Recommended)**

mistune's community size (3,000 stars, 368,000+ dependents) is impressive but does not compensate for its partial CommonMark compliance. Jerry's markdown files are authored against CommonMark behavior — specifically HTML block Type 2 comment handling for L2-REINJECT, and nested inline content in table cells for navigation tables. mistune's "sane CommonMark rules" deviate from the spec in ways that are not fully characterized; running mistune against existing Jerry markdown files to quantify behavior divergence would be required before adoption (Phase 2, Trade-off 3; Risk Matrix). The Roundtrip Fidelity score of 2/5 reflects that mistune's markdown renderer exists but is undocumented for external use, and roundtrip behavior is unvalidated. For Jerry's use case, this is a disqualifying combination.

**Rank 5 — mdformat standalone (Composite: 3.35 | Not Recommended as standalone)**

Evaluated for completeness: mdformat standalone scores identically to the stack on Roundtrip Fidelity (5/5) and Maintenance (4/5), but its AST Quality score of 2/5 reflects that it is a formatter, not a general-purpose AST library. AST access is only available within plugin callbacks via `RenderTreeNode`, not as a general parse-then-query API. Jerry cannot use mdformat standalone to implement the blockquote frontmatter extraction or navigation table query operations required. It is correctly used as the roundtrip engine in the Rank 1 stack, not as a standalone parser.

**Ranks 6-7 — pyromark and commonmark.py (Disqualified)**

pyromark is disqualified on two independent grounds: (1) no Python-level extension API — custom syntax requires Rust implementation within pulldown-cmark; (2) no roundtrip capability — HTML output only. Both are hard incompatibilities with Jerry's requirements regardless of pyromark's extreme performance advantage (Phase 1, Library 6; Phase 2, AST Quality and Roundtrip scores of 1/5). commonmark.py is officially deprecated; its maintainers recommend migrating to markdown-it-py (Phase 1, Library 7).

---

### Top Contender Comparison

#### Head-to-Head: markdown-it-py+mdformat vs mistletoe vs marko

| Criterion | markdown-it-py + mdformat | mistletoe | marko |
|-----------|:------------------------:|:---------:|:-----:|
| **Composite score** | 4.20 | 3.75 | 3.40 |
| **AST type** | Flat tokens + SyntaxTreeNode (tree conversion on demand) | True tree (native) | True tree (native) |
| **Position tracking** | token.map [start, end] on all block tokens | line_number on all block tokens | Uncertain (Phase 2 flag) |
| **Roundtrip fidelity** | Validated: HTML-equality verification (mdformat) — semantic equivalence guaranteed | Design goal: MarkdownRenderer; not formally verified | Normalizing: whitespace/formatting may be altered |
| **Extension API maturity** | 20+ plugins; MyST-Parser proof-of-concept; function-based | Subclass-based; no frontmatter plugin; fewer examples | Subclass-based; MarkoExtension packaging; fewest examples |
| **Frontmatter support** | Plugin available (mdit_py_plugins.front_matter) | Must build custom token | Must build custom element |
| **Maintenance backing** | Institutional (Executable Books) | Single maintainer (miyuchina) | Single maintainer (frostming) |
| **Jerry extension LOC** | ~470 LOC | ~520 LOC | ~500 LOC |
| **Jerry extension complexity** | Low-Medium | Medium | Medium |
| **Dependency count** | 2 (same org, MIT) | 1 (MIT) | 1 (MIT) |
| **Python requirement** | >=3.10 | >=3.5 | >=3.9 |
| **Risk level** | Low | Low-Medium | Medium |

#### Key Differentiators: Why #1 Beats #2

The single decisive differentiator between markdown-it-py + mdformat and mistletoe is **validated roundtrip fidelity**. When Jerry modifies a blockquote frontmatter field in a WORKTRACKER.md file and re-renders the document, the guarantee provided by the two stacks differs categorically:

- **markdown-it-py + mdformat:** mdformat verifies HTML-equality between input and output — the rendered HTML of the original document and the rendered HTML of the formatted output must be identical. If the formatting pass would alter any document semantics, the operation fails rather than silently corrupting meaning. This is a semantic correctness guarantee backed by a verification pass. **Important nuance:** this guarantee covers semantic equivalence, not source-level formatting preservation. mdformat may normalize whitespace, heading style, or list formatting as long as the HTML output remains equivalent. For Jerry, this means that SPIKE-002 must additionally validate that mdformat's formatting conventions are compatible with Jerry's existing document formatting, or that a supplementary diff-based check on unmodified source regions is layered on top.
- **mistletoe:** The MarkdownRenderer is designed for roundtrip preservation, but there is no verification step. If mistletoe's renderer introduces a subtle whitespace change in an L2-REINJECT comment or alters a table alignment marker, Jerry will not know unless it runs its own diff-based validation.

Jerry's documents are living sources of truth (WORKTRACKER.md, skill definitions, rule files). Silent corruption of these files — whether semantic or formatting-level — undermines confidence in the AST-first architecture. The validated roundtrip property addresses the semantic dimension of this concern; the formatting dimension may require supplementary validation regardless of library choice (see Sensitivity Analysis).

The extension ecosystem gap is the second differentiator. markdown-it-py's 20+ mdit-py-plugins and MyST-Parser's domain-specific markdown dialect (roles, directives, structured metadata) are direct empirical evidence that Jerry's blockquote frontmatter and L2-REINJECT requirements can be implemented cleanly. mistletoe's extension API is clean, but the only evidence for its capability is the API documentation — no comparable real-world example of a domain-specific dialect exists in its ecosystem.

#### Steelman for Mistletoe (H-16 Compliance)

Per H-16, the strongest case for the #2 candidate must be considered before critique. The steelman for mistletoe:

1. **True tree AST is genuinely superior for Jerry's tree-walking operations.** Jerry's core operations (blockquote traversal, parent-child identification for `blockquote > paragraph > strong` patterns) are more ergonomic with mistletoe's native tree (`children`/`parent` properties) than with markdown-it-py's flat token stream requiring explicit `SyntaxTreeNode(tokens)` conversion. The extra conversion step adds code complexity and a potential error source.

2. **Single dependency reduces supply chain risk.** mdformat has 15 contributors versus markdown-it-py's 34, suggesting a smaller maintenance base within the Executable Books organization. Two libraries means two versioning constraints, two changelogs, and two potential breaking change vectors. The "same organization" mitigant is a snapshot, not a guarantee.

3. **The "validated roundtrip" advantage may be compensatable.** mdformat validates semantic equivalence (HTML output consistency), not byte-for-byte source preservation. Jerry could build a diff-based validation layer on top of mistletoe's MarkdownRenderer that directly validates what Jerry actually needs: unmodified source lines are preserved byte-for-byte. This approach would provide a stronger guarantee for Jerry's specific use case than mdformat's HTML-equality check, at the cost of ~50-80 LOC of validation code.

4. **mistletoe's MarkdownRenderer was purpose-built for parse-modify-render workflows.** mdformat was designed as a formatter (normalizing tool). Using mdformat for surgical section modification is repurposing a formatter as a preservation engine — which works due to the HTML-equality check, but is not the tool's primary design intent.

**Steelman resolution:** These arguments are substantive. Points 1 and 4 are real ergonomic advantages. Point 3 identifies a genuine gap in the "decisive advantage" framing — the roundtrip validation advantage is less categorical than initially presented, because it addresses semantic equivalence rather than source preservation, and because the gap is compensatable with custom validation code.

However, the recommendation stands because: (a) the ecosystem maturity gap (20+ plugins, MyST-Parser proof-of-concept vs no comparable real-world example) is not compensatable — it represents accumulated engineering evidence that Jerry's extension patterns will work; (b) institutional maintenance (Executable Books vs single maintainer) is a structural advantage, not merely a snapshot; and (c) even if Jerry builds diff-based validation on top of either stack, the cost of doing so on markdown-it-py + mdformat is lower because mdformat's semantic guarantee provides a baseline that diff-based validation extends, rather than replaces.

#### Scenario Analysis: When to Choose Each Top Contender

**Choose markdown-it-py + mdformat when:**
- Roundtrip correctness is a hard requirement (parse-modify-render on living documents)
- The extension ecosystem matters (frontmatter plugin already available, MyST-Parser patterns to follow)
- Python >=3.10 is acceptable (Jerry's current stack)
- Two-library dependency from the same organization is acceptable
- **This is the recommendation for Jerry.**

**Choose mistletoe when:**
- SPIKE-002 reveals that mdformat's parser extension plugin API cannot support blockquote frontmatter write-back (the highest-uncertainty interaction)
- A single-library dependency is a hard requirement
- The true tree AST is strongly preferred for ergonomics over SyntaxTreeNode
- The team is willing to build and own a roundtrip verification layer (diff-based validation to compensate for the missing HTML-equality verification)
- Python <3.10 support is needed

**Choose marko when:**
- marko's position tracking is confirmed present (resolving Phase 2 uncertainty)
- The normalizing MarkdownRenderer is acceptable (i.e., Jerry will adopt mdformat-style document normalization as a feature, not a risk)
- The most recent release date (Jan 2026) and lowest open issue count are weighted heavily
- **Not recommended as a primary choice** given the roundtrip normalization strategic mismatch.

---

### Build-from-Scratch Assessment

#### Verdict: Do Not Build from Scratch

**Recommendation: Adopt (library approach with extensions)**

The build-from-scratch option is not recommended. The evidence is decisive.

**Effort comparison (from Phase 2 analysis):**

| Metric | Library Approach (Rank 1) | Build-from-Scratch |
|--------|:------------------------:|:-----------------:|
| Implementation LOC | ~470 | 2,380-3,320 |
| Development time | 1-2 weeks | 6-10 weeks |
| CommonMark coverage | 100% (via library) | ~65% (subset) |
| Roundtrip validation | mdformat provides this | Must build or accept risk |
| Maintenance burden | Low (upstream absorbs spec) | High (own all spec coverage) |
| Edge-case parsing risk | Low (battle-tested) | High (new implementation) |
| Control over Jerry-specific semantics | Full (via extension API) | Full (built-in) |

**What you gain with build-from-scratch:** Full control over Jerry-specific parsing behavior from the ground up; no dependency on external library API stability; custom AST node types perfectly matched to Jerry's domain model.

**What you lose vs library approach:** The control argument is the sole advantage, and it is available at lower cost via the extension API path. Jerry does not need to own CommonMark parsing — it needs to own Jerry-specific semantic extraction (blockquote frontmatter, L2-REINJECT parsing). These are post-parse semantic layers that sit on top of any CommonMark parser; building them inside a custom parser versus on top of an existing parser delivers the same semantic control at 5-7x the implementation cost. Additionally, the build approach loses: (1) battle-tested edge-case handling in the underlying CommonMark specification (the 35% of CommonMark not needed for today's Jerry files will be needed as soon as an author writes a new construct); (2) the free upstream absorption of CommonMark spec updates; (3) mdformat's validated roundtrip guarantee, which would need to be rebuilt.

**The 65% problem:** Implementing 65% of the CommonMark specification is not a 65% implementation task. CommonMark's complexity is concentrated in edge cases — precedence resolution for nested emphasis, link detection with nested brackets, list continuation rules. These cases account for disproportionate share of parsing complexity and testing surface. Phase 2's estimate of 400-600 LOC for the tokenizer/lexer alone reflects this (Phase 2, Build-from-Scratch LOC table).

**If the library approach fails:** If SPIKE-002 demonstrates that no library's extension API can cleanly support Jerry's write-back requirements, the correct next step is a **hybrid approach** (thin wrapper over an existing library + custom AST nodes for Jerry-specific constructs), not a full scratch build. This hybrid would reuse CommonMark parsing from an existing library while giving Jerry full control over the domain-specific semantic layer. Estimated cost: 800-1,200 LOC, 2-4 weeks — still well below the scratch estimate.

---

## L2: Strategic Assessment

### Extension Roadmap

This roadmap covers the Jerry-specific extensions needed on top of the recommended markdown-it-py + mdformat stack, ordered by implementation priority and dependency.

#### Extension 1: Blockquote Frontmatter Extraction (Priority: P0)

**What it is:** A post-parse tree walker that identifies blockquotes matching the `**Key:** Value` pattern and extracts structured key-value metadata. Used for reading entity metadata (Type, Status, Priority, etc.) from WORKTRACKER entities.

**Components:**
- Post-parse `SyntaxTreeNode` walker — identify `blockquote > paragraph` nodes
- Key-value extraction: match `strong + text` token pairs, handle multiline blockquotes
- Write-back: reconstruct paragraph token content from modified key-value dict (the critical uncertainty — see SPIKE-002)

| Sub-component | LOC | Complexity | Notes |
|---------------|:---:|:----------:|-------|
| Extraction walker | ~50 | Low | Walk blockquote/paragraph/strong nodes |
| Key-value parser | ~30 | Low | Regex on strong content + adjacent text |
| Write-back token reconstruction | ~60 | Medium | Token regeneration or safe string substitution |
| Tests | ~80 | Low-Medium | Edge cases: multiline values, values with inline markdown, non-metadata blockquotes |
| **Subtotal** | **~220** | **Low-Medium** | |

**Risk:** Write-back is the highest-risk sub-component. If reconstructing paragraph tokens after value modification is fragile, the fallback is string-level substitution with regex-based find-replace on the source text (simpler, slightly less elegant). SPIKE-002 must validate this.

**Implementation order:** Implement extraction before write-back. Use extraction in read-only query operations first; add write-back only after validating the roundtrip fidelity guarantee holds for the specific modification.

#### Extension 2: L2-REINJECT Comment Parser (Priority: P0)

**What it is:** A post-parse filter on `html_block` tokens that identifies L2-REINJECT comments by prefix, then extracts the structured `rank=N, tokens=N, content="..."` fields using regex parsing of the comment body.

| Sub-component | LOC | Complexity | Notes |
|---------------|:---:|:----------:|-------|
| html_block token filter | ~20 | Low | Match `<!-- L2-REINJECT:` prefix |
| Field extraction regex | ~30 | Low | Parse rank, tokens, content fields |
| Write-back (comment content update) | ~30 | Low | String replacement within comment node; safe because comment is self-contained |
| Tests | ~40 | Low | |
| **Subtotal** | **~120** | **Low** | |

**Risk:** Low. HTML comment content is a flat string; no tree traversal complexity. Write-back is simpler than blockquote frontmatter because the entire content is in one self-contained token with no interleaving AST nodes.

#### Extension 3: Navigation Table Query Helpers (Priority: P1)

**What it is:** Utility functions for walking `table` tokens in the SyntaxTreeNode, reading cell content (including anchor links), and modifying specific cell values. Used for Jerry's H-23/H-24 navigation table validation and generation.

| Sub-component | LOC | Complexity | Notes |
|---------------|:---:|:----------:|-------|
| Table cell walker | ~30 | Low | Iterate table/tr/td nodes via SyntaxTreeNode |
| Anchor link extractor | ~20 | Low | Extract href from link tokens within cells |
| Cell value setter | ~30 | Low | Reconstruct table cell content |
| Tests | ~40 | Low | |
| **Subtotal** | **~120** | **Low** | |

#### Extension 4: Jerry Markdown Facade (Priority: P1)

**What it is:** A unified Python API that wraps the markdown-it-py + mdformat stack and exposes Jerry-specific operations as a clean interface. Hides library internals from Jerry's application layer.

| Sub-component | LOC | Complexity | Notes |
|---------------|:---:|:----------:|-------|
| JerryDocument class (parse, query, transform, render) | ~80 | Low | Facade wrapping md-it-py parse + mdformat render |
| Frontmatter accessor API | ~20 | Low | get_frontmatter(), set_frontmatter_field() |
| L2-REINJECT accessor API | ~15 | Low | get_reinject_blocks(), update_reinject_content() |
| Navigation table accessor API | ~15 | Low | get_nav_table(), update_nav_entry() |
| **Subtotal** | **~130** | **Low** | |

#### Extension Totals and Phasing

| Phase | Extensions | LOC | Timeline |
|-------|-----------|:---:|----------|
| **Phase A** (SPIKE-002 proof-of-concept) | Blockquote FM extraction + L2-REINJECT (read-only) | ~150 | Days 1-3 |
| **Phase B** (SPIKE-002 write-back validation) | Blockquote FM write-back + L2-REINJECT write-back | ~120 | Days 4-5 |
| **Phase C** (FEAT-001 production) | Navigation table helpers + Jerry facade | ~250 | Week 2 |
| **Tests** | Full suite (H-21: 90% coverage) | ~120 | Ongoing |
| **Grand Total** | All extensions | **~470** | 1-2 weeks |

---

### Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|:----------:|:------:|------------|
| R-01 | mdformat plugin API insufficient for blockquote frontmatter write-back | Medium | High | SPIKE-002 validates this specifically (Phase A + B). Fallback: string-level substitution with roundtrip diff verification. |
| R-02 | markdown-it-py SyntaxTreeNode API changes in v5.x (breaking change) | Low | Medium | Pin to v4.x; monitor upstream changelog; tree API is stable across v3-v4. |
| R-03 | mdformat HTML-equality verification rejects Jerry's markdown (edge cases in Jerry's dialect where mdformat's formatting alters HTML output) | Low | Medium | Run mdformat against full Jerry markdown corpus in SPIKE-002. Known issue area: L2-REINJECT comments with special characters. |
| R-04 | Two-library dependency conflict (markdown-it-py + mdformat version coupling) | Low | Low | Both are Executable Books org; they maintain version alignment. Monitor pyproject.toml compatibility matrix. |
| R-05 | mistletoe single-maintainer abandonment (fallback library) | Medium | Low | Jerry adopts primary library (Rank 1); fallback only needed if R-01 materializes. 1,466+ dependents provide community pressure on mistletoe. |
| R-06 | marko position tracking absent (resolving Phase 2 uncertainty) | Medium | Low | marko is Rank 3 only; does not affect Rank 1 recommendation. SPIKE-002 may investigate if marko remains under consideration. |
| R-07 | Extension LOC estimate underestimates multiline blockquote write-back complexity | Medium | Medium | Conservative estimate includes buffer; SPIKE-002 proof-of-concept will surface true complexity before production implementation. |

**Critical risk to monitor:** R-01 (mdformat plugin API for write-back) is the single highest-uncertainty point in this recommendation. It is the only interaction that was not clearly documented in Phase 1 or 2 research. SPIKE-002 must resolve it.

---

### SPIKE-002 Handoff Implications

SPIKE-002 (AST-First Architecture Feasibility) should investigate the following, ranked by criticality to the Rank 1 recommendation:

**Critical (must resolve before adopting Rank 1):**

1. **Blockquote frontmatter write-back via mdformat plugin API.** Implement a minimal proof-of-concept: parse a WORKTRACKER entity file with markdown-it-py, modify a frontmatter field value (e.g., `Status: pending -> in_progress`), render back with mdformat, and verify: (a) the modified field is correct, (b) all other content is byte-for-byte identical (diff-based check), (c) mdformat's HTML-equality verification passes (semantic equivalence check). If this fails, fallback to string-level substitution and re-validate.

2. **Full Jerry dialect roundtrip corpus test.** Run mdformat against all 30-50 active Jerry markdown files (WORKTRACKER.md files, skill definitions, rule files, templates). Capture any files where mdformat's normalization pass alters content — these are edge cases where Jerry's current markdown dialect deviates from mdformat's canonical form. Document whether the alterations are acceptable (whitespace normalization) or disqualifying (semantic content change).

3. **L2-REINJECT roundtrip with special characters.** L2-REINJECT comment content strings contain quotes, commas, and periods. Verify that mdformat's HTML comment handling preserves these verbatim through a parse-modify-render cycle.

**Important (validate recommendation assumptions):**

4. **Extension API integration pattern.** Implement a minimal JerryDocument class using the facade pattern (Extension 4) and validate that the API ergonomics are acceptable for FEAT-001 implementation. Verify that markdown-it-py's `SyntaxTreeNode` provides sufficient position tracking for identifying which blockquote is the entity frontmatter vs a content blockquote.

5. **Performance at batch scale.** Process 50 Jerry markdown files sequentially to measure total throughput. Confirm sub-100ms total is achievable (expected: yes, given Phase 1 benchmarks showing <1ms per file). Relevant for future features that may process the full Jerry file corpus.

**Investigate if risk R-01 materializes:**

6. **mistletoe fallback proof-of-concept.** If mdformat write-back cannot support blockquote frontmatter, implement the same proof-of-concept with mistletoe's MarkdownRenderer. Document the roundtrip fidelity observed (expected: good but unverified). Determine whether a Jerry-owned diff-based verification layer is sufficient compensation.

---

### Sensitivity Analysis

This section tests the recommendation's robustness under altered assumptions. The recommendation is robust if markdown-it-py + mdformat remains #1 under reasonable perturbations of dimension weights and scores.

#### Test 1: Roundtrip Fidelity Weight Reduced

If Roundtrip Fidelity weight drops from 0.20 to 0.15 (redistributing 0.05 to Jerry Compatibility, which rises to 0.20):

| Library | Original Composite | Adjusted Composite | Rank Change |
|---------|:-----------------:|:-----------------:|:-----------:|
| markdown-it-py + mdformat | 4.20 | 4.10 | Stays #1 |
| mistletoe | 3.75 | 3.70 | Stays #2 |
| marko | 3.40 | 3.40 | Stays #3 |

**Result:** Recommendation survives. The gap narrows from 0.45 to 0.40 but #1 remains #1.

#### Test 2: Mistletoe Roundtrip Score Raised to 4.5

If we credit mistletoe with a score of 4.5 on Roundtrip Fidelity (acknowledging that diff-based validation could compensate for the missing HTML-equality verification):

| Library | Original Composite | Adjusted Composite | Rank Change |
|---------|:-----------------:|:-----------------:|:-----------:|
| markdown-it-py + mdformat | 4.20 | 4.20 (unchanged) | Stays #1 |
| mistletoe | 3.75 | 3.85 | Stays #2 |

**Result:** Recommendation survives. Gap narrows from 0.45 to 0.35.

#### Test 3: Extreme Perturbation -- All Roundtrip Scores Equalized to 4

If we set all top-3 libraries to Roundtrip Fidelity = 4 (removing the validated roundtrip as a differentiator entirely):

| Library | Original Composite | Adjusted Composite | Rank Change |
|---------|:-----------------:|:-----------------:|:-----------:|
| markdown-it-py + mdformat | 4.20 | 4.00 | Stays #1 |
| mistletoe | 3.75 | 3.75 (unchanged) | Stays #2 |
| marko | 3.40 | 3.60 | Stays #3 |

**Result:** Recommendation survives. Even without the roundtrip advantage, markdown-it-py + mdformat leads due to Extension API (5 vs 4) and Maintenance (4 vs 3). The gap narrows from 0.45 to 0.25, which is still substantial.

#### Test 4: Extension API Weight Doubled

If Extension API weight rises from 0.15 to 0.25 (reducing Performance and License to 0.025 each, Maintenance to 0.075):

| Library | Original Composite | Adjusted Composite | Rank Change |
|---------|:-----------------:|:-----------------:|:-----------:|
| markdown-it-py + mdformat | 4.20 | 4.28 | Stays #1 |
| mistletoe | 3.75 | 3.73 | Stays #2 |

**Result:** Recommendation strengthens. markdown-it-py + mdformat benefits from its Extension API score of 5.

#### Test 5: Adversarial Combined Perturbation

Worst-case scenario for the recommendation: markdown-it-py Extension API downgraded from 5 to 4 (arguing that Jerry's use case is simpler than MyST-Parser's and does not fully exercise the ecosystem advantage), AND mistletoe Roundtrip raised to 4.5 (crediting diff-based validation), AND Maintenance equalized (both at 4, arguing that active community compensates for single-maintainer):

| Library | Original Composite | Adjusted Composite | Rank Change |
|---------|:-----------------:|:-----------------:|:-----------:|
| markdown-it-py + mdformat | 4.20 | 4.05 | Stays #1 |
| mistletoe | 3.75 | 3.95 | Stays #2 (gap narrows) |

Calculation for md-it-py (Extension API 4, others unchanged): 4*0.20 + 5*0.20 + 4*0.15 + 3*0.15 + 4*0.10 + 4*0.10 + 3*0.05 + 5*0.05 = 0.80 + 1.00 + 0.60 + 0.45 + 0.40 + 0.40 + 0.15 + 0.25 = 4.05.

Calculation for mistletoe (Roundtrip 4.5, Maintenance 4): 4*0.20 + 4.5*0.20 + 4*0.15 + 3*0.15 + 4*0.10 + 4*0.10 + 3*0.05 + 5*0.05 = 0.80 + 0.90 + 0.60 + 0.45 + 0.40 + 0.40 + 0.15 + 0.25 = 3.95.

**Result:** Under the most adversarial reasonable perturbation, markdown-it-py + mdformat (4.05) still leads mistletoe (3.95) by 0.10 points. The recommendation survives even under combined unfavorable assumptions. The gap is narrow enough that SPIKE-002 validation becomes genuinely decisive -- if SPIKE-002 reveals significant issues with the stack (R-01 materializes, mdformat normalization is unacceptable), mistletoe becomes a credible primary choice, not just a fallback.

#### Sensitivity Conclusion

The recommendation is **robust**. markdown-it-py + mdformat remains #1 under all five perturbation scenarios, including the adversarial combined perturbation (Test 5) where three dimensions are simultaneously adjusted against the recommendation. The narrowest gap (0.10 in Test 5) confirms that SPIKE-002 validation is genuinely important -- it is not a formality. However, no single reasonable perturbation or combination of reasonable perturbations produces a rank reversal. The recommendation is supported by the combination of Extension API maturity, Maintenance backing, and Roundtrip Fidelity, with no single dimension being a single point of failure.

---

### Semantic Equivalence vs Source Preservation

This section addresses a critical analytical distinction identified during quality review.

**mdformat's guarantee:** mdformat validates that the rendered HTML of the input document equals the rendered HTML of the formatted output. This proves **semantic equivalence** — formatting changes do not alter what the document means. This is the strongest guarantee available in the Python markdown ecosystem.

**What mdformat does NOT guarantee:** Byte-for-byte preservation of source-level formatting in unmodified regions. mdformat is a formatter — its design intent is to produce canonical formatting. When used as part of a parse-modify-render pipeline, it may normalize whitespace, heading styles, or list indentation in regions Jerry did not modify.

**Why this matters for Jerry:** Jerry's documents use specific formatting conventions (table alignment, blockquote whitespace patterns, L2-REINJECT comment indentation). If mdformat normalizes these patterns differently, a parse-modify-render cycle could produce formatting changes in unmodified regions — changes that are semantically harmless but visually distracting and confidence-undermining.

**Mitigation:** Two complementary strategies:

1. **Normalization adoption:** If Jerry adopts mdformat's canonical formatting as the standard for all Jerry documents (running mdformat once to normalize the entire corpus), subsequent parse-modify-render cycles will produce no formatting changes in unmodified regions because the corpus is already in canonical form. This is the approach mdformat was designed for.

2. **Supplementary diff-based validation:** If Jerry cannot adopt mdformat's canonical formatting (e.g., because specific formatting patterns are required for readability), a supplementary diff-based check (~50 LOC) can validate that only the intended regions changed. This provides byte-for-byte source preservation on top of mdformat's semantic guarantee.

**SPIKE-002 implication:** SPIKE-002 should run mdformat against 5-10 representative Jerry markdown files and inspect the formatting changes. If the changes are acceptable (or desirable as normalization), strategy 1 applies. If the changes are unacceptable, strategy 2 is required. This investigation is already captured in SPIKE-002 handoff item #2 (full Jerry dialect roundtrip corpus test).

---

## Phase 2 Uncertainty Resolution

Phase 2 (ps-analyst-001) identified four uncertainties for Phase 3 to resolve. This section maps each to its resolution status.

| # | Phase 2 Uncertainty | Phase 3 Resolution | Status |
|---|--------------------|--------------------|--------|
| 1 | marko's position tracking: if line number access is absent, AST Quality drops to 3, composite to ~3.20 | Phase 3 retains marko at 4/5 AST Quality (benefit of the doubt) but flags the uncertainty explicitly in the Rank 3 justification (line 60) and Risk Register (R-06). Resolution deferred to SPIKE-002 if marko remains under consideration. | Deferred (does not affect Rank 1 recommendation) |
| 2 | mistletoe single-maintainer risk: community trajectory and succession plan | Phase 3 documents the risk in Rank 2 justification (Maintenance 3/5) and Risk Register (R-05). No succession plan was identified. The 1,466+ dependents provide community pressure but not institutional guarantee. | Acknowledged, not resolved (structural risk accepted for fallback library) |
| 3 | mistune CommonMark compliance delta: characterize actual behavior divergence | Phase 3 classifies mistune as "Not Recommended" (Rank 4) in part due to this uncharacterized risk. Running mistune against Jerry files was not performed (out of Phase 3 scope — would require experimental validation). | Not resolved (moot — mistune not recommended) |
| 4 | mdformat plugin API fit for blockquote frontmatter write-back | Phase 3 identifies this as the critical risk (R-01) and the #1 SPIKE-002 handoff item. Resolution requires proof-of-concept implementation, which is Phase 4 (SPIKE-002) scope. | Deferred to SPIKE-002 (by design — this is SPIKE-002's primary objective) |

---

## Decision Record

| Field | Value |
|-------|-------|
| **Recommended Library** | markdown-it-py v4.0.0 + mdformat v1.0.0 |
| **Confidence** | High — composite score 4.20 leads second-place by 0.45 points (12%); recommendation survives all sensitivity perturbations including removal of the roundtrip advantage entirely (Test 3: gap narrows to 0.25 but #1 holds); extension ecosystem maturity is empirically demonstrated by MyST-Parser; the roundtrip advantage is a semantic equivalence guarantee that may require supplementary diff-based validation for source preservation (see Semantic Equivalence vs Source Preservation) |
| **Key Risk** | R-01: mdformat plugin API expressiveness for blockquote frontmatter write-back — the one interaction not clearly documented in Phase 1 or 2 research; must be resolved in SPIKE-002 |
| **Build-from-Scratch Verdict** | Adopt (library approach with extensions) — build-from-scratch is 5-7x more expensive with no functional advantage over the extension API path |
| **Fallback if Key Risk Materializes** | mistletoe v1.5.1 (composite: 3.75) — requires building a Jerry-owned roundtrip verification layer (diff-based validation, ~50 LOC) to compensate for lack of HTML-equality verification |
| **Next Step** | SPIKE-002 implements Phase A proof-of-concept (blockquote FM extraction + L2-REINJECT read-only) against real Jerry markdown files, then Phase B write-back validation, before committing to production implementation in FEAT-001 |
| **Version Pinning** | Pin `markdown-it-py>=4.0.0,<5.0.0` and `mdformat>=1.0.0,<2.0.0` in `pyproject.toml`. Both libraries follow semver; major version pins protect against breaking changes while allowing patch/minor updates. |
| **Day-1 Setup** | `uv add "markdown-it-py>=4.0.0,<5.0.0" "mdformat>=1.0.0,<2.0.0" mdit-py-plugins` |
| **Fallback Escalation** | If R-01 materializes (mdformat write-back insufficient): try mistletoe + Jerry-owned diff-based validation (~520 LOC + ~50 LOC validation). If mistletoe MarkdownRenderer also fails roundtrip requirements: hybrid approach with markdown-it-py parsing + custom Jerry renderer for modified sections only (~800-1,200 LOC). Full scratch build is the last resort, not a planned contingency. |

---

## References

All claims in this document trace to Phase 1 or Phase 2 artifacts. No new research is introduced in Phase 3.

### Phase 1 Research Traceability

| Claim | Phase 1 Source | Phase 1 Section |
|-------|----------------|-----------------|
| markdown-it-py 100% CommonMark v0.31.2 compliance | Library 1: markdown-it-py | L1: Technical Analysis > Library 1 > CommonMark Compliance |
| mdformat HTML-equality roundtrip verification (semantic equivalence) | Library 5: mdformat | L1: Technical Analysis > Library 5 > Roundtrip Fidelity; L2: Observation 7 |
| 20+ mdit-py-plugins; MyST-Parser proof-of-concept | Library 1 + Supplementary: MyST-Parser | L1: Library 1 > Extension API; L2: Observation 3 |
| mistletoe true tree AST; line_number attribute | Library 2: mistletoe | L1: Library 2 > AST Access |
| mistletoe MarkdownRenderer for parse-modify-render | Library 2: mistletoe | L1: Library 2 > Roundtrip Fidelity |
| marko MarkdownRenderer normalizes (does not preserve) | Library 3: marko | L1: Library 3 > Roundtrip Fidelity; L2: Observation 4 |
| mistune partial CommonMark ("sane rules") | Library 4: mistune | L1: Library 4 > CommonMark Compliance |
| pyromark: no Python-level extension API | Library 6: pyromark | L1: Library 6 > Extension API |
| commonmark.py: deprecated | Library 7: commonmark.py | L1: Library 7 > Maintenance Status |
| Jerry files 30-250 lines; performance not differentiating | Cross-cutting | L2: Architectural Implications > Observation 5 |
| L2-REINJECT as HTML comment Type 2 block | Jerry Compatibility | L1: Jerry Compatibility Assessment > Pattern 3 |
| Blockquote frontmatter: all tree libraries require semantic layer | Jerry Compatibility | L1: Pattern 1; L2: Observation 1 |
| Template placeholders: syntactically plain text, no conflict | Jerry Compatibility | L1: Jerry Compatibility Assessment > Pattern 4 |
| mdformat 15 contributors (steelman supply chain argument) | Library 5: mdformat | L1: Technical Analysis > Library 5 > GitHub Metrics |
| markdown-it-py 34 contributors (steelman supply chain argument) | Library 1: markdown-it-py | L1: Technical Analysis > Library 1 > GitHub Metrics |
| mdformat designed as formatter/normalizer (steelman design intent argument) | Library 5: mdformat | L1: Technical Analysis > Library 5 > Overview; Roundtrip Fidelity |

### Phase 2 Analysis Traceability

| Claim | Phase 2 Source | Phase 2 Section |
|-------|----------------|-----------------|
| Composite scores (all libraries) | Weighted Composite Scores table | L1: Feature Matrix > Weighted Composite Scores |
| Extension LOC estimates (all libraries) | Extension Effort Estimates per library | L1: Feature Matrix > Extension Effort Estimates |
| Build-from-scratch LOC estimate (2,380-3,320 LOC, 6-10 weeks) | LOC table | L1: Feature Matrix > Build-from-Scratch Assessment > LOC Estimate |
| Library approach LOC estimate (470 LOC, 1-2 weeks) | markdown-it-py + mdformat total | L1: Feature Matrix > Extension Effort Estimates > markdown-it-py + mdformat |
| marko position tracking uncertainty flag | AST Quality scoring rationale | L1: Feature Matrix > Dimension-by-Dimension > AST Quality > marko |
| mistletoe single-maintainer risk | Risk Matrix | L2: Strategic Analysis > Risk Matrix > Per-Library Risk Detail > mistletoe |
| mistune CommonMark compliance integration risk | Trade-off 3; Risk Matrix | L2: Strategic Analysis > Trade-off Analysis > Trade-off 3; Risk Matrix > mistune |
| Build-from-scratch verdict: not recommended | Verdict | L1: Feature Matrix > Build-from-Scratch Assessment > Cost-Benefit Analysis |
| Preliminary ranking consistent with Phase 3 final ranking | Preliminary Ranking table | L2: Strategic Analysis > Preliminary Ranking |
| mdformat standalone vs stack distinction | Note on mdformat standalone vs stack | L1: Feature Matrix > Weighted Composite Scores (note) |
| Roundtrip fidelity: validated vs design goal distinction | Roundtrip Fidelity dimension; Trade-off 1 | L1: Dimension-by-Dimension > Roundtrip Fidelity; L2: Trade-off 1 |

### Source Artifacts

| Artifact | Path |
|----------|------|
| Phase 1 Research | `orchestration/spike-eval-20260219-001/ps/phase-1-research/ps-researcher-001/library-landscape-research.md` |
| Phase 2 Analysis | `orchestration/spike-eval-20260219-001/ps/phase-2-analysis/ps-analyst-001/library-feature-matrix.md` |
| SPIKE-001 Entity | `work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/SPIKE-001-library-landscape/SPIKE-001-library-landscape.md` |

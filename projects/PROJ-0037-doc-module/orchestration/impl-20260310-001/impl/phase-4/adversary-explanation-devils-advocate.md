# Strategy Execution Report: Devil's Advocate

## Execution Context

- **Strategy:** S-002 (Devil's Advocate)
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md`
- **Deliverable:** `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-4/frontmatter-issue-explanation.md`
- **Deliverable Type:** Technical issue explanation (stakeholder-facing)
- **Criticality:** C2 (Standard)
- **Executed:** 2026-03-11T00:00:00Z
- **H-16 Status:** FLAGGED — No S-003 Steelman output found in phase-4 directory or anywhere in `projects/PROJ-0037-doc-module/`. H-16 requires S-003 before S-002. User's explicit invocation of this standalone accuracy/clarity review is acknowledged as a P-020 authority override for this ad-hoc review context. Proceeding with deviation documented per P-022.

---

## Step 1: Role Assumption

The Devil's Advocate role is assumed. The mandate is to argue against the claims in `frontmatter-issue-explanation.md` — to challenge its accuracy, expose misleading simplifications, surface missing context, and identify anything that could lead a reader to a wrong conclusion. The deliverable is a technical explanation for a stakeholder who has not been in the 4-phase implementation pipeline.

The critique proceeds across four focus areas specified by the requester: (1) factual accuracy verified against source code, (2) clarity for an outside reader, (3) misleading simplifications, (4) missing context.

---

## Step 2: Assumption Inventory

**Explicit assumptions in the deliverable:**

- A1: `jerry ast frontmatter` reads the blockquote format (Format B), not the YAML `---` frontmatter (Format A)
- A2: `jerry ast frontmatter` "doesn't parse `---`-delimited YAML at all"
- A3: The fix requires a new adapter rather than modifying the existing one
- A4: Using `yaml.safe_load` inside the existing reader would "bypass the port abstraction"
- A5: H-33 does not apply to SKILL.md and agent `.md` files

**Implicit assumptions:**

- A6: The shown sample command output is the actual output of `jerry ast frontmatter` on `skills/adversary/SKILL.md`
- A7: The port docstring comment listing only `AstFrontmatterReader` is accurate at the time of writing
- A8: The reader counts "13 skills" as the number that will be extracted
- A9: The problem is fully characterized by the `name` field missing — no other fields matter

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001-20260311 | Critical | `AstFrontmatterReader` docstring contradicts its own behavior — claims to parse "YAML frontmatter" but actually reads blockquote format; the explanation does not surface this contradiction, which could mislead a reader about the root cause | "What Goes Wrong" |
| DA-002-20260311 | Major | The claim that `jerry ast frontmatter` "doesn't parse `---`-delimited YAML at all" is stated as fact but is unverified in the explanation — no source code evidence for the `jerry ast` parser itself is cited | "The Two Formats" / "What Goes Wrong" |
| DA-003-20260311 | Major | The explanation treats "bypass the port abstraction" as a valid reason to reject the in-place fix, but the reasoning is architecturally incorrect — adding `yaml.safe_load` inside `AstFrontmatterReader` would not bypass the port abstraction | "The Fix: YamlFrontmatterReader" |
| DA-004-20260311 | Major | The explanation asserts "13 skills are skipped" without explaining what count the reader would encounter — a stakeholder could reasonably ask "how do you know it's 13 and not something else?" | "What Goes Wrong" |
| DA-005-20260311 | Minor | The one-sentence summary ("reads the wrong part of SKILL.md files") is not fully accurate — `jerry ast frontmatter` does not read a "part" of the file; it reads a different metadata format entirely | "The One-Sentence Version" |
| DA-006-20260311 | Minor | The fix diagram lists `YamlFrontmatterReader` as proposed but the port docstring (already in the codebase) lists only `AstFrontmatterReader` — a careful reader who looks at the source will see an inconsistency not explained by the document | "The Fix: YamlFrontmatterReader" |

---

## Detailed Findings

### DA-001-20260311: AstFrontmatterReader's Self-Contradicting Docstring [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | "What Goes Wrong" |
| **Strategy Step** | Step 3 — Counter-argument lenses: Contradicting evidence |

**Evidence:**

`ast_frontmatter_reader.py` lines 29-34:
```
Uses ``uv run jerry ast frontmatter {file_path}`` to parse YAML
frontmatter via the AST-based parser (H-33 compliance).
```

The docstring says the adapter parses "YAML frontmatter." The explanation says the adapter actually returns blockquote metadata (Format B) while ignoring the YAML frontmatter (Format A). These are mutually contradictory. Additionally, the class-level docstring (line 7 of `skill_extractor.py`) says the SkillExtractor reads "SKILL.md and agents/*.md frontmatter via the IFrontmatterReader port" — using the word "frontmatter" to describe what is actually blockquote metadata.

**Counter-argument:** The explanation's framing — "the doc module's `AstFrontmatterReader` calls `jerry ast frontmatter` on each SKILL.md file" — presents this as straightforward behavior, obscuring that the code itself has a documentation bug: it claims to parse YAML frontmatter but demonstrably does not. A reader who looks at `ast_frontmatter_reader.py` will see a module that says it parses YAML frontmatter (H-33 compliance), and will not understand why this is wrong without additional context. The explanation misses the opportunity to say: "the adapter's own docstring is misleading — it says 'YAML frontmatter' but the tool it delegates to actually reads blockquote metadata."

**Analysis:** This is a Critical finding because it directly affects accuracy. A reader who checks the source code will encounter a docstring that appears to contradict the explanation. This could cause them to distrust the explanation or reach the wrong conclusion (e.g., "the adapter works correctly, the problem must be elsewhere").

**Recommendation:** Add one sentence to "What Goes Wrong": "Note that `ast_frontmatter_reader.py`'s own docstring says it parses 'YAML frontmatter' — this is itself a documentation error in the adapter; the tool it delegates to (`jerry ast frontmatter`) reads blockquote metadata, not `---`-delimited YAML."

---

### DA-002-20260311: Claim That jerry ast Does Not Parse YAML Is Asserted Without Evidence [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | "The Two Formats" and "What Goes Wrong" |
| **Strategy Step** | Step 3 — Counter-argument lenses: Unstated assumptions, Evidence quality |

**Evidence:**

The explanation states:

> "`jerry ast frontmatter` doesn't parse `---`-delimited YAML at all"

and shows a command output with blockquote keys (`"Version"`, `"Framework"`, etc.) and no YAML frontmatter keys (`name`, `description`).

**Counter-argument:** The explanation presents the command output as proof but does not cite the `jerry ast` parser source code. A skeptical reader could argue: "What if `jerry ast frontmatter` does parse YAML frontmatter but returns it merged with blockquote data, and the YAML keys are simply being overwritten by blockquote keys of the same name?" Or: "What if the `---` block is parsed but its keys happen to be absent from this file's YAML section?" The assertion "doesn't parse `---`-delimited YAML at all" is a strong claim that requires source code evidence, not just output observation.

The command output shown (`"Version"`, `"Framework"`, etc.) is consistent with blockquote-only parsing, but it does not definitively rule out a partial or merged parsing scenario. The explanation does not verify this against the `/ast` skill source code or the `jerry ast` parser implementation.

**Analysis:** Major severity. A reader who pushes back on the diagnosis could reasonably ask to see the parser source code. The explanation's accuracy depends on this claim being true, but the claim is supported only by observational output, not by citing the parser's implementation. If the parser does something more nuanced (e.g., prefers blockquote over YAML when both exist), the root cause analysis and the fix design could both be wrong.

**Recommendation:** Either (a) cite the relevant `jerry ast` parser source file that confirms it reads only blockquote metadata, or (b) soften the claim: "the output shows only blockquote keys, indicating either that `jerry ast frontmatter` does not parse `---`-delimited YAML, or that it discards YAML keys in favor of blockquote keys."

---

### DA-003-20260311: "Bypass the Port Abstraction" Justification Is Architecturally Incorrect [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | "The Fix: YamlFrontmatterReader" |
| **Strategy Step** | Step 3 — Counter-argument lenses: Logical flaws |

**Evidence:**

The explanation states:

> "Why not use `yaml.safe_load` inside the existing reader? Because that would bypass the port abstraction. The hexagonal architecture (H-07) says infrastructure adapters implement domain ports — so we add a new adapter, not modify the extractor."

**Counter-argument:** This justification is logically flawed. Adding `yaml.safe_load` to the body of `AstFrontmatterReader` would not bypass the port abstraction. `AstFrontmatterReader` is itself an infrastructure adapter that implements the `IFrontmatterReader` port. Infrastructure adapters are explicitly the correct place to add different parsing strategies. A reader familiar with hexagonal architecture will recognize that:

1. The port (`IFrontmatterReader`) defines the interface — it does not care how the adapter implements it.
2. An adapter that uses both subprocess delegation and `yaml.safe_load` internally is still a valid single adapter.
3. Adding a new adapter adds a new seam, which is appropriate when the two formats are genuinely different use cases (SKILL.md vs. worktracker entities). But the reason given — "bypass the port abstraction" — is not the correct justification.

The real justification for adding a new adapter is: (a) keeping `AstFrontmatterReader` semantically pure (blockquote parsing for worktracker entities), and (b) avoiding the risk of breaking existing worktracker operations. The port abstraction argument is a misleading simplification that would lead a reader with architecture knowledge to distrust the reasoning.

**Analysis:** Major severity. A stakeholder with software engineering background will notice the explanation gives a wrong architectural reason for the correct design decision. This could undermine confidence in the diagnosis and the fix recommendation. It is a misleading simplification that survives only because the conclusion (new adapter) happens to be correct, even though the stated reason is wrong.

**Recommendation:** Replace "Because that would bypass the port abstraction" with: "Because `AstFrontmatterReader` is designed specifically for blockquote parsing used by worktracker entities. Mixing YAML `---` parsing into it would make the adapter semantically ambiguous and risk breaking worktracker operations that depend on its current behavior. A second adapter with a single clear responsibility is the safer design."

---

### DA-004-20260311: "13 Skills" Asserted Without Supporting Evidence [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | "What Goes Wrong" |
| **Strategy Step** | Step 3 — Counter-argument lenses: Unstated assumptions |

**Evidence:**

> "Result: all 13 skills are skipped. The doc module generates an empty skills table."

**Counter-argument:** The explanation does not tell the reader where 13 comes from. A stakeholder who has not been in the pipeline has no way to verify this number. More importantly, if there are currently 13 skills in the codebase, this number will change over time. The explanation will become stale — and a future reader who counts 14 or 15 skills may question whether the entire diagnosis is correct.

Additionally, the explanation does not distinguish between "13 SKILL.md files exist" and "13 skills would be successfully extracted if the reader worked correctly." It is theoretically possible that some SKILL.md files lack a YAML frontmatter block entirely, in which case fewer than 13 skills would be extracted even with a working reader.

**Analysis:** Major severity. The specific number creates false precision and is unverifiable without external context. For a stakeholder explanation, unverifiable specific numbers are a credibility risk.

**Recommendation:** Change "all 13 skills are skipped" to "all skills are skipped (currently 13, one per `skills/*/SKILL.md` file)" and add a note: "Each of these SKILL.md files has a `---`-delimited YAML block with a `name` field, so all 13 would be correctly extracted by a reader that parses Format A."

---

### DA-005-20260311: One-Sentence Summary Uses Inaccurate Framing [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | "The One-Sentence Version" |
| **Strategy Step** | Step 3 — Counter-argument lenses: Alternative interpretations |

**Evidence:**

> "`jerry ast frontmatter` reads the wrong part of SKILL.md files, so the doc module extracts zero skills."

**Counter-argument:** `jerry ast frontmatter` does not read the "wrong part" of the file — it reads the correct part for its intended use case (worktracker entity blockquote metadata). The problem is that it is being used for a use case it was not designed for (SKILL.md YAML frontmatter). "Wrong part" frames this as a bug in `jerry ast`, when the actual issue is a mismatch between the tool's purpose and the adapter's use of it.

Additionally, "extracts zero skills" is an imprecise outcome description. The doc module does not error — it silently skips all skills with a log warning. A reader might reasonably expect "extracts zero skills" to mean an exception or failure, not a silent empty-table result.

**Analysis:** Minor severity. The one-sentence version is a summary that trades precision for simplicity — reasonable for a hook sentence. However, the specific framing could plant a wrong mental model (bug in `jerry ast` vs. wrong tool for the job) that the rest of the document has to work to correct.

**Recommendation:** Revise to: "`jerry ast frontmatter` is designed for worktracker entity metadata — when the doc module uses it on SKILL.md files, it reads the wrong metadata format, so the doc module silently skips all 13 skills and generates an empty skills table."

---

### DA-006-20260311: Port Docstring Lists Only AstFrontmatterReader — Inconsistency Unexplained [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | "The Fix: YamlFrontmatterReader" |
| **Strategy Step** | Step 3 — Counter-argument lenses: Unaddressed risks |

**Evidence:**

The explanation proposes adding `YamlFrontmatterReader`. However, `frontmatter_reader.py` (the domain port) currently reads:

```
Implementations:
    - AstFrontmatterReader: delegates to ``jerry ast frontmatter``
      (src/docs/infrastructure/adapters/ast_frontmatter_reader.py)
```

Only one implementation is listed. A reader who checks this source file will not find `YamlFrontmatterReader` listed, which could create doubt about whether the fix is complete or whether additional changes (port docstring update) are part of the scope.

**Analysis:** Minor severity. A stakeholder who looks at the code will find a gap between the proposed fix (new adapter) and the existing port documentation. This is not a logical flaw in the fix but is a missing completeness detail.

**Recommendation:** Add one sentence to the fix section: "The port's docstring (`frontmatter_reader.py`) lists `AstFrontmatterReader` as the only implementation — it will also need to be updated to document `YamlFrontmatterReader` as a second implementation."

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

**DA-001:** Add a sentence to "What Goes Wrong" acknowledging that `ast_frontmatter_reader.py`'s own docstring says "YAML frontmatter" — this is itself a documentation error in the adapter. Without this, a reader who checks the source will see an apparent contradiction between the explanation and the code, undermining the explanation's credibility.

### P1 — Major (SHOULD resolve)

**DA-002:** Either cite the `jerry ast` parser source to confirm it reads only blockquote metadata, or soften the absolute claim "doesn't parse `---`-delimited YAML at all" to an evidence-qualified statement. The current assertion is unsupported.

**DA-003:** Replace the "bypass the port abstraction" justification with the correct reasoning: preserving `AstFrontmatterReader`'s semantic purity for worktracker use and avoiding risk to existing worktracker operations. The current justification is architecturally incorrect and will mislead any reader with software engineering background.

**DA-004:** Contextualize the "13 skills" claim. Explain where 13 comes from (one per `skills/*/SKILL.md`) and note that each of these files has a YAML `name` field — so all 13 would succeed with a correct reader.

### P2 — Minor (MAY resolve; acknowledgment sufficient)

**DA-005:** Revise the one-sentence hook to clarify that `jerry ast` is not buggy — it is the wrong tool for this use case. The "wrong part" framing plants an inaccurate mental model.

**DA-006:** Note in the fix section that the port's docstring (`frontmatter_reader.py`) will also need to be updated to list `YamlFrontmatterReader` as a second implementation.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002: Missing source-code citation for the key claim. DA-006: Port docstring update omitted from fix scope. |
| Internal Consistency | 0.20 | Negative | DA-001: Explanation contradicts `ast_frontmatter_reader.py` docstring without acknowledging the contradiction. |
| Methodological Rigor | 0.20 | Neutral | The diagnostic approach (show command output, trace through code, propose fix) is sound. The architectural justification (DA-003) is flawed but the conclusion is correct. |
| Evidence Quality | 0.15 | Negative | DA-002: Key causal claim unsupported by parser source. DA-004: Specific count asserted without derivation. |
| Actionability | 0.15 | Neutral | The fix is clearly stated and implementable. The architectural justification error (DA-003) does not block implementation. |
| Traceability | 0.10 | Neutral | The explanation traces to code accurately for the lines cited. The traceability gap is the missing link to `jerry ast` parser source. |

**Overall Assessment:** REVISE. The deliverable's core diagnosis is correct and the fix recommendation is sound, but three Major findings materially weaken credibility: an unsupported key claim (DA-002), an incorrect architectural justification (DA-003), and a contradictory docstring not surfaced for the reader (DA-001, Critical). A reader with engineering background will notice all three. After addressing DA-001 through DA-004, the explanation should withstand scrutiny.

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 1
- **Major:** 3
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5
- **H-16 Status:** Deviation documented (no S-003 prior output; user authority override per P-020)

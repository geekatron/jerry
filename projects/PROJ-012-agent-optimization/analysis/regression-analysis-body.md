# Regression Analysis: Agent Prompt Body Changes

**Branch:** `feat/proj-012-agent-optimization` vs `main`
**Analysis Date:** 2026-02-26
**Scope:** All `skills/*/agents/*.md` files changed between `main` and `HEAD`
**Method:** `git diff main...HEAD`, body extraction via awk, XML tag diff, heading duplicate detection

---

## Summary

| Metric | Value |
|--------|-------|
| Total agents changed | 58 |
| Agents with body-identical to main | 44 |
| Agents with body changes | 14 |
| Governance sections injected into source bodies | 0 |
| XML tags removed (regressions) | 0 |
| Duplicate headings introduced | 0 |
| Pre-existing duplicate headings | 8 agents |
| Content regressions identified | 2 (see Findings) |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Governance Injection Status](#governance-injection-status) | Why governance sections are not in source files |
| [Change Categories](#change-categories) | Classification of all 58 agents into 4 categories |
| [Content Preservation Check](#content-preservation-check) | XML tags, section ordering, duplicates |
| [Findings](#findings) | F-001 through F-005 with severity and impact |
| [Overall Verdict](#overall-verdict) | PASS/FAIL/WARN per check dimension |

---

## Governance Injection Status

**Finding: Governance sections were NOT injected into the source `.md` files in `skills/*/agents/`.**

The task description states PROJ-012 injects governance data (`## Agent Version`, `## Tool Tier`, `## Enforcement`, `## Portability`, `## Session Context`) into the prompt body. This injection happens at **compose time**, not at the source file level.

**Architecture clarification from code inspection:**

- **Source of truth:** `skills/*/composition/*.jerry.yaml` + `*.jerry.prompt.md` — canonical agent definitions
- **Compose pipeline input:** reads `*.jerry.yaml` + `*.jerry.prompt.md` from `skills/*/composition/`
- **Compose pipeline output:** writes to `skills/*/agents/*.md` (Claude Code format)
- **Governance injection point:** `GovernanceSectionBuilder.build()` in `src/agents/domain/services/governance_section_builder.py` appends `## Agent Version`, `## Tool Tier`, `## Enforcement`, `## Portability`, `## Session Context`, `## Prior Art` sections to the body **only when `jerry compose` is executed**

The `skills/*/agents/*.md` source files checked into the repository are **handwritten source definitions**, not compose pipeline outputs. The governance injection would appear in the final `skills/*/agents/*.md` files only after `jerry compose --vendor claude-code` is run. That run has not been committed to this branch for the `.md` files checked into `skills/*/agents/`.

**The `## Session Context` sections found in some agents (e.g., `adv-scorer.md`, `nse-architecture.md`, `sb-calibrator.md`) are PRE-EXISTING in `main` — not newly injected by PROJ-012.** Confirmed by checking `git show main:<path>` for each agent reporting a `## Session Context` match.

---

## Change Categories

### Category A: Frontmatter-Only (44 agents)

Only `permissionMode: default` and `background: false` added to YAML frontmatter. Prompt bodies are **byte-for-byte identical** to `main`.

**Verified:** All 44 agents confirmed identical bodies via full body text comparison.

| Skill | Agents |
|-------|--------|
| adversary | adv-selector |
| eng-team | eng-architect, eng-backend, eng-devsecops, eng-frontend, eng-incident, eng-infra, eng-lead, eng-qa, eng-reviewer, eng-security |
| nasa-se | nse-architecture, nse-configuration, nse-explorer, nse-integration, nse-qa, nse-reporter, nse-risk, nse-verification |
| orchestration | orch-planner, orch-synthesizer, orch-tracker |
| problem-solving | ps-analyst, ps-architect, ps-investigator, ps-reporter, ps-researcher, ps-synthesizer |
| red-team | red-exfil, red-exploit, red-infra, red-lateral, red-lead, red-persist, red-privesc, red-recon, red-reporter, red-social, red-vuln |
| transcript | ts-extractor, ts-formatter, ts-mindmap-ascii, ts-mindmap-mermaid, ts-parser |

### Category B: CLI Examples Updated — bash to Python API (10 agents)

The `jerry ast` CLI invocation pattern was replaced with direct Python API imports from `skills.ast.scripts.ast_ops`. This is a functional change to embedded code examples in methodology sections (not a formatting change). For worktracker agents, the change is the environment variable prefix and boolean casing only (Bash CLI retained).

**Before (main) — adv/nse/ps agents:**
```bash
uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast frontmatter {deliverable_path}
# Returns: {"Type": "story", "Status": "in_progress", ...}
```

**After (HEAD) — adv/nse/ps agents:**
```python
from skills.ast.scripts.ast_ops import query_frontmatter
fm = query_frontmatter("{deliverable_path}")
entity_type = fm.get("Type", "unknown")
```

**Before (main) — wt agents:**
```bash
uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast frontmatter <PROJ-009 entity path>/EN-001-example.md
```

**After (HEAD) — wt agents:**
```bash
uv run --directory ${JERRY_PLUGIN_ROOT} jerry ast frontmatter <PROJ-009 entity path>/EN-001-example.md
```

**Affected agents and their specific changes:**

| Agent | Change Type | Functions/Variables Changed |
|-------|-------------|----------------------------|
| `adv-executor` | bash to Python | `jerry ast frontmatter` to `query_frontmatter()`, `jerry ast parse` to `parse_file()`, `jerry ast validate --schema` to `validate_file()` |
| `adv-scorer` | bash to Python | `jerry ast frontmatter` to `query_frontmatter()`, `jerry ast validate --nav` to `validate_nav_table_file()`, `jerry ast parse` to `parse_file()` |
| `nse-requirements` | bash to Python | Same 3 CLI functions to Python API equivalents |
| `nse-reviewer` | bash to Python | Same 3 CLI functions to Python API; added `if not result["is_valid"]` conditional block |
| `ps-critic` | bash to Python | `query_frontmatter()`, `validate_nav_table_file()`, `validate_file()` with expanded iteration loop |
| `ps-reviewer` | bash to Python | Same 3 CLI functions to Python API; expanded schema violation iteration |
| `ps-validator` | bash to Python | 4 CLI functions to Python API; expanded batch validation loop |
| `wt-auditor` | env var + booleans | `${CLAUDE_PLUGIN_ROOT}` to `${JERRY_PLUGIN_ROOT}` in 3 Bash examples; `true/false` to `True/False` in JSON comments |
| `wt-verifier` | env var + booleans | `${CLAUDE_PLUGIN_ROOT}` to `${JERRY_PLUGIN_ROOT}` in 3 Bash examples; `true/false` to `True/False` in JSON comments |
| `wt-visualizer` | env var + booleans | `${CLAUDE_PLUGIN_ROOT}` to `${JERRY_PLUGIN_ROOT}` in 2 Bash examples; `true/false` to `True/False` in JSON comment |

All structural content (what each example does, what it returns, how to interpret results) is preserved. The Python API examples are more complete than the original CLI versions — they include variable assignment, conditional handling, and result iteration loops.

### Category C: llm-tell-patterns.md Reference Removed (4 agents)

The conditional reference loading instruction for `skills/saucer-boy-framework-voice/references/llm-tell-patterns.md` was removed from `<reference_loading>` sections and from specific methodology steps. The file itself **still exists** at `skills/saucer-boy-framework-voice/references/llm-tell-patterns.md`.

| Agent | Lines removed |
|-------|--------------|
| `sb-calibrator` | 1 reference load line; "LLM writing markers present (em-dashes as connectors...)" text from Directness < 0.5 band rubric |
| `sb-reviewer` | 1 reference load line; explicit LLM marker enumeration and file path from Boundary #8 (Mechanical Assembly) evaluation |
| `sb-rewriter` | 1 reference load line; "Strip LLM writing markers per `skills/saucer-boy-framework-voice/references/llm-tell-patterns.md`" from Direct trait step 1 |
| `sb-voice` | 1 reference load line only |

### Category D: Phase 2.5 Content Quality Methodology Deleted (1 agent)

**Agent:** `skills/worktracker/agents/wt-auditor.md`

The Phase 2.5 Content Quality Check and its corresponding documentation section were completely removed. This is the largest content deletion in the changeset: 44 lines removed, 0 replacement lines added for the deleted content.

**Deleted from methodology (Phase 2.5 — 10 steps):**

- DoD detection (WTI-008a): patterns `tests? pass`, `code review`, `documentation updated`, `deployed to`, `QA sign-off`, `coverage meets`, `no critical bugs`, `peer reviewed`
- Implementation detail detection (WTI-008b): file paths (`src/`, `.py`, `.ts`, `.cs`), class/method names
- Actor-first format checking (WTI-008c): INFO severity
- Hedge word detection (WTI-008d): patterns `should be able to`, `might need`, `could potentially`, etc.
- AC bullet count enforcement (WTI-008e): Story=5, Bug=5, Task=5, Enabler=5, Feature=5
- Summary length enforcement (WTI-008f): max 3 sentences
- Scope overflow detection (WTI-008g): SPIDR splitting recommendation
- DEC-006 grandfathering rule: items created before 2026-02-17 downgraded to INFO

**Deleted from Audit Check Types documentation block:**

- Section 2.5 Content Quality (WARNING/INFO) heading and sub-bullets
- Report format table showing content quality finding columns
- DEC-006 advisory note in documentation

**Deleted from WTI rules compliance table:**

- `WTI-008` row: "Content Quality Standards (AC clarity, brevity, no DoD in AC)"

**Also changed (not a deletion):** Phase 2 step 2 updated from `jerry ast validate path --schema entity_type` to `validate_file(path, schema=entity_type)`.

---

## Content Preservation Check

### XML Tag Integrity

All 14 agents with body changes were checked for XML tag removal. **All passed.** No structural XML tags were removed from any agent.

| Agent | Result | Notes |
|-------|--------|-------|
| adv-executor | PASS | All tags preserved |
| adv-scorer | PASS | All tags preserved |
| nse-requirements | PASS | All tags preserved |
| nse-reviewer | PASS | All tags preserved |
| ps-critic | PASS | All tags preserved |
| ps-reviewer | PASS | All tags preserved |
| ps-validator | PASS | All tags preserved |
| wt-auditor | PASS | `<entity_type>` and `<path>` in updated CLI example are argument placeholders in code context, not structural XML tags |
| wt-verifier | PASS | All tags preserved |
| wt-visualizer | PASS | All tags preserved |
| sb-calibrator | PASS | All tags preserved |
| sb-reviewer | PASS | All tags preserved |
| sb-rewriter | PASS | All tags preserved |
| sb-voice | PASS | All tags preserved |

### Section Ordering

No existing sections were reordered in any agent. All Category B changes are in-place substitutions within existing methodology subsections. No governance sections were appended to any source file body.

### Duplicate Sections Check

8 agents have duplicate `##` headings. **All duplicates are pre-existing in `main`.** None were introduced by changes in `HEAD`. This was verified by checking `git show main:<path>` for all 8 agents.

| Agent | Duplicate Headings (pre-existing) |
|-------|----------------------------------|
| nse-requirements | `## L0: Executive Summary`, `## NSE CONTEXT (REQUIRED)` |
| nse-reviewer | `## L0: Executive Summary`, `## NSE CONTEXT (REQUIRED)`, `## References` |
| ps-critic | `## EVALUATION CRITERIA`, `## IMPROVEMENT THRESHOLD`, `## PS CONTEXT (REQUIRED)` |
| ps-reviewer | `## PS CONTEXT (REQUIRED)` |
| ps-validator | `## PS CONTEXT (REQUIRED)` |
| wt-auditor | `## Audit Check Types`, `## AUDIT CONTEXT (REQUIRED)`, `## MANDATORY PERSISTENCE (P-002)` |
| wt-verifier | `## VERIFICATION TASK` |
| wt-visualizer | `## MANDATORY PERSISTENCE (P-002)` |

---

## Findings

### F-001: Governance Injection Not Present in Source Files (Informational)

**Severity:** Informational — by design
**Agents:** All 58
**Finding:** The `## Agent Version`, `## Tool Tier`, `## Enforcement`, `## Portability` sections described in the PROJ-012 compose pipeline design are NOT present in the `skills/*/agents/*.md` source files in either `main` or `HEAD`. The injection is implemented in `GovernanceSectionBuilder` and fires at `jerry compose` runtime. The source files are inputs to the pipeline, not its outputs. The governance data lives in `skills/*/composition/*.jerry.yaml` files (which were also updated in PROJ-012 — renamed from `*.agent.yaml` to `*.jerry.yaml`).

**No action required.** This is the expected state for source files. The compose pipeline must be run and its output committed for governance sections to appear in Claude Code agent `.md` files.

### F-002: Phase 2.5 Content Quality Check Deleted from wt-auditor (Regression)

**Severity:** Regression — functional capability removed without documented replacement
**Agent:** `skills/worktracker/agents/wt-auditor.md`
**Lines removed:** 44 lines (Phase 2.5 methodology + Section 2.5 documentation + WTI-008 compliance row)
**Lines added:** 0 replacement lines

The wt-auditor no longer has methodology to check acceptance criteria quality against WTI-008 standards. WTI-008 remains defined in `skills/worktracker/rules/worktracker-behavior-rules.md` (not modified in this branch), creating a gap between the rules and the auditor's implementation.

**Recommendation:** Determine whether this deletion is intentional (content quality checking moved to a different agent or mechanism) or accidental. If intentional, update `worktracker-behavior-rules.md` to reflect that wt-auditor no longer enforces WTI-008. If accidental, restore Phase 2.5.

### F-003: llm-tell-patterns.md Reference Removal Reduces Voice Guidance Precision (Warning)

**Severity:** Warning — reference pruning reduces agent contextual guidance
**Agents:** sb-calibrator, sb-reviewer, sb-rewriter, sb-voice
**Finding:** Explicit load triggers for `llm-tell-patterns.md` were removed from all four saucer-boy skill agents. The file still exists. Agents can still load it via general reference instructions but lose the specific conditional trigger (e.g., "when LLM writing markers are detected"). The Directness scoring rubric in sb-calibrator and the Mechanical Assembly boundary in sb-reviewer lost specific marker enumeration.

**Recommendation:** Determine if this was intentional simplification or accidental. If LLM-tell pattern detection is still expected to work, restore the conditional load triggers so agents know when and why to reference the file.

### F-004: CLI API Style Changed in adv/nse/ps Agents (Informational — Intentional)

**Severity:** Informational
**Agents:** adv-executor, adv-scorer, nse-requirements, nse-reviewer, ps-critic, ps-reviewer, ps-validator
**Finding:** AST operation examples changed from `uv run jerry ast` CLI invocations to direct Python API imports (`from skills.ast.scripts.ast_ops import ...`). All structural content preserved. Python API examples are more complete than the original CLI versions. The Migration Note in each agent was updated to reference the new function name. This is a consistent update across all 7 agents that had the same pattern.

### F-005: Environment Variable Rename in wt Agents (Informational — Intentional)

**Severity:** Informational
**Agents:** wt-auditor, wt-verifier, wt-visualizer
**Finding:** `${CLAUDE_PLUGIN_ROOT}` replaced with `${JERRY_PLUGIN_ROOT}` in all Bash CLI examples. JSON comment booleans corrected from `true/false` (JavaScript style) to `True/False` (Python style). Worktracker agents retain Bash CLI style — they were not converted to Python API style like the adv/nse/ps agents. This is consistent with the PROJ-012 commit message which specifically mentions "Fixes wt-* agents missing --directory prefix on uv run calls."

---

## Overall Verdict

**CONDITIONAL PASS with 1 regression and 1 warning requiring review before merge.**

| Check Dimension | Result | Details |
|-----------------|--------|---------|
| Body preservation — 44 frontmatter-only agents | PASS | All bodies byte-for-byte identical to main |
| XML tag integrity — 14 body-changed agents | PASS | No structural tags removed |
| Section ordering | PASS | No sections reordered |
| Duplicate sections introduced | PASS | None introduced; 8 pre-existing confirmed |
| Governance injection into source bodies | N/A | By design: injection fires at compose time, not in source files |
| CLI update correctness — 7 adv/nse/ps agents | PASS | Functional equivalence preserved; examples more complete in HEAD |
| Environment variable rename — 3 wt agents | PASS | Intentional rename per PROJ-012 commit message |
| Phase 2.5 deletion — wt-auditor | **FAIL** | Functional capability (WTI-008 AC quality checks) removed without replacement |
| llm-tell-patterns.md reference removal — 4 sb agents | **WARN** | Reduces voice precision; file exists but explicit triggers removed |

**F-002 (Phase 2.5 deletion)** requires resolution before this branch can be considered regression-free. The WTI-008 rule definitions in `skills/worktracker/rules/worktracker-behavior-rules.md` are still present but wt-auditor no longer implements them, creating a silent enforcement gap.

**F-003 (llm-tell-patterns.md)** is lower priority — the file is not deleted and agents can still reference it, but losing the explicit conditional load triggers may reduce scoring precision for LLM-tell pattern detection in voice fidelity workflows.

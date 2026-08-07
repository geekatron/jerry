# Devil's Advocate Report: BUG-010 Containment Scope Widening (PR #341) — UX / Conceptual-Complexity Lens

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `src/interface/cli/{project_root,ast_commands,parser,main}.py` (branch `fix/BUG-010-ast-project-root`), plus `projects/.../BUG-010-ast-project-root/{eng-lead-implementation-plan,red-vuln-findings,BUG-010-ast-project-root}.md`
**Criticality:** C4 (Critical — security-relevant CLI, tournament mode)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, Group C, C4 tournament)
**H-16 Compliance:** S-003 Steelman applied 2026-08-07 by adv-executor (Group B) — confirmed present at `adv-s003-steelman.md`, read in full before this execution.
**Lens directive (from invocation):** Attack the UX and conceptual complexity of the design specifically — the `--root` exclusive-not-additive semantics, the two transparency behaviors (R-3, R-4), and whether "smart default + escape hatch" is more complexity than a user can hold in their head. Argue the strongest case against shipping as-is.

---

## Summary

8 counter-arguments identified (1 Critical, 5 Major, 2 Minor), all confined to the UX/conceptual-complexity lens as directed — the underlying M-08/M-10 security predicate and TOCTOU discipline (already validated as sound by the Steelman) are **not** re-litigated here. The strongest case against shipping as-is: the design's own explicit claim — "stdout is reserved for the JSON/render payload" — is contradicted by the realistic condition of merged stdout/stderr consumption (`2>&1`, `subprocess.run(capture_output=True)`), which is exactly how the design's own primary intended use case (agent-mediated scratchpad operations, per the Steelman's SM-002) will most often be consumed (DA-004, Critical). Beyond that single blocking finding, the `--root` flag's exclusive-not-additive semantics is a genuine least-astonishment violation with no combinator escape hatch (DA-001, DA-002), the resulting behavior matrix has five distinct branches gated by two independent, unsuppressible stderr side-channels that a user must hold in their head simultaneously (DA-003), and the one warning that *is* advisory-only (R-3) provides zero actual enforcement while still being impossible to silence for legitimate broad-root use (DA-005). Recommend REVISE: address DA-004 (P0) before merge; DA-001/002/003/005/006 (P1) should be resolved or explicitly deferred with owner sign-off given the C4 criticality and the fact that R-3/R-4 were the plan's own self-identified "OPEN — requires owner/user confirmation" items.

---

## Assumptions Challenged (Step 2)

| Assumption (explicit or implicit) | Challenge |
|---|---|
| "`--root` is a familiar escape-hatch pattern users will intuit correctly." (implicit, throughout) | Common CLI precedent for a bare `--root`/`--path`/`--include`-shaped flag is *additive* (PATH, `-I` search paths, `--volume`), not *exclusive-replacing*. No CLI-convention evidence is offered for why exclusivity is the more intuitive choice. |
| "stdout is reserved for the JSON/render payload, so stderr diagnostics are safe to add freely." (explicit, BUG-010.md Fix Approach) | True only if stdout and stderr are consumed as genuinely separate streams. Any `2>&1` or combined-capture consumption pattern — extremely common in CI, shell scripting, and subprocess wrappers — violates this assumption silently. |
| "A one-line stderr note/warning is low UX cost." (implicit, R-3/R-4 rationale in eng-lead plan) | Cost is not evaluated against *frequency*. R-4 fires on the design's own stated primary use case (scratchpad operations), making it the common case, not an edge case — a signal that fires routinely is noise, not signal. |
| "Escape hatch + smart default is a simple two-mode model." (implicit, Steelman SM-001 names this explicitly as a strength) | The Steelman's own mode table has 2 rows; the *actual* runtime behavior matrix (built from code, not from the design's self-description) has 5 distinct branches once ownership-gating and the two independent stderr channels are included. The two-mode *framing* undercounts the two-mode *implementation's* real surface area. |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260807C | `--root` naming/semantics violates least-astonishment; common CLI convention for a bare root/path flag is additive, this one is exclusive-replacing | Major | `project_root.py:159-160`: `if explicit_root is not None: return [resolved_root]` — no union with defaults | Completeness |
| DA-002-20260807C | No combinator mechanism exists to use an explicit `--root` *together with* the project root or temp defaults; a real "validate my project file AND an external file" workflow requires two separate invocations | Major | `get_containment_roots(explicit_root: str \| None = None) -> list[Path]` (`project_root.py:120`) takes a single string, not a repeatable list; `parser.py:585-593` `_add_root_argument` has no `action="append"` | Completeness |
| DA-003-20260807C | The full runtime behavior matrix is 5 distinct branches (silent success / ownership-rejected / success+Note / success+WARNING / rejected-because-exclusive) gated by 2 independent, unsuppressible stderr side channels — exceeds what a user can reliably hold in their head for a markdown-file read/write command | Major | Derived from `_check_path_containment` (`ast_commands.py:290-367`), `_check_temp_root_ownership` (`ast_commands.py:244-287`), `_warn_if_temp_root_match` (`ast_commands.py:212-241`), `get_containment_roots` broad-root branch (`project_root.py:159-169`) | Methodological Rigor |
| DA-004-20260807C | The design's own explicit claim — "stdout is reserved for the JSON/render payload" — is contradicted under realistic merged-stream consumption; R-3/R-4 stderr text has no suppression flag and will corrupt naive `2>&1`/combined-capture JSON consumers on the design's own stated primary use case | Critical | `BUG-010-ast-project-root.md:69` ("stdout is reserved for the JSON/render payload"); `_warn_if_temp_root_match` fires unconditionally (`ast_commands.py:235-241`); no `--quiet`/`--no-warn` flag anywhere in `parser.py`; eng-lead's own risk table flags this as unresolved ("adds output-format risk... JSON-mode callers must not have stderr diagnostics leak into stdout JSON", `eng-lead-implementation-plan.md` R-4 row) | Internal Consistency |
| DA-005-20260807C | R-3's broad-root warning is advisory-only "security theater": it never blocks, cannot be silenced, and applies the identical scary "WARNING" text to both an accidental mistake and a deliberate, correct, broad choice (e.g., a dotfiles repo legitimately rooted at `$HOME`) | Major | `get_containment_roots` (`project_root.py:159-169`): warning prints, then `return [resolved_root]` unconditionally — the invocation always proceeds regardless of the warning | Actionability |
| DA-006-20260807C | The shipped `--help` text for `--root` never states the single most consequential, counter-intuitive fact of the design — that a user's own project-root files become REJECTED once `--root` points elsewhere — leaving that fact only in internal engineering docs no end user will read | Major | `parser.py:588-592`: `"Restrict path containment to exactly this directory (overrides the default project-root + temp-dir allowed set). User discretion: use to run 'jerry ast' against any location."` — "overrides" is present but the rejection consequence for the user's *own* files is never spelled out in user-facing text | Traceability |
| DA-007-20260807C | The temp-root ownership-rejection error message ("Path in shared temp directory is owned by another user") introduces unrelated systems/multi-tenancy vocabulary (uid, file ownership, shared hosts) into the error surface of what is, for its primary persona, a markdown documentation linting tool | Minor | `_check_temp_root_ownership` (`ast_commands.py:244-287`), error string at `ast_commands.py:284` | Evidence Quality |
| DA-008-20260807C | A "bug" work item (fix wrong root anchor) grew into a 4-file, 10-function-threaded authorization-and-transparency subsystem (2 new stderr side channels, an ownership gate, a broad-root detector) bundled into one PR/branch/review cycle rather than being split into fix + separately-reviewed design decision | Minor | `BUG-010-ast-project-root.md` frontmatter `Type: bug`; scope-widening paragraph appended to the same `## Fix Approach` section (`BUG-010-ast-project-root.md:57-74`) rather than a new ADR/design entity | Methodological Rigor |

**Finding ID Format:** `DA-{NNN}-20260807C` (Group C, C4 tournament execution).

---

## Finding Details

### DA-001: `--root` Exclusive Semantics Violates CLI Least-Astonishment [MAJOR]

**Claim Challenged:** The Steelman (SM-001) frames `--root`'s exclusivity as "the load-bearing property... exactly the semantic a CI job or wrapper tool needs" and treats it as an unambiguous strength.

**Counter-Argument:** A bare `--root <path>` flag, with no qualifying word like `--only`, `--exclusive`, or `--exact`, carries a strong prior from adjacent CLI conventions that it is *additive*: `PATH` is additive across every directory in it; compiler `-I`/`--include-dir` flags add search directories; `docker run --volume` adds mounts; `eslint --rulesdir` adds rule directories. A user reasoning by analogy to this much larger, much more familiar convention set will expect `jerry ast validate --root /other/dir file.md` to widen the allowed set, not replace it. The flag name alone does not communicate the design's actual (and, per the Steelman, deliberately load-bearing) exclusivity semantics — a user has to already know, from documentation they may never read, that this specific flag inverts the general convention.

**Evidence:** `get_containment_roots` (`project_root.py:159-160`): `if explicit_root is not None: return [resolved_root]` — no fallthrough, no union.

**Impact:** Users invoking `--root` expecting an additive widening will get confusing, security-flavored rejections ("Path escapes allowed containment roots") for files that were working fine a moment before — including their own project files, which is the single most counter-intuitive failure mode in the whole design.

**Dimension:** Completeness

**Response Required:** Either (a) rename the flag to make exclusivity explicit in the name itself (e.g., `--only-root`, `--exact-root`), (b) add a companion additive flag (`--extra-root`, repeatable) alongside the exclusive one so both use cases are served without overloading a single flag's semantics, or (c) provide explicit, evidenced justification (user research, prior art citation, or an owner-confirmed accepted trade-off) for why exclusivity-under-a-generic-name is the correct choice despite the convention mismatch.

**Acceptance Criteria:** A documented decision (owner sign-off, given R-3/R-4 were already routed for owner confirmation) explicitly addressing the naming/semantics mismatch, OR a flag-shape change that removes the ambiguity.

---

### DA-002: No Combinator Mechanism for Explicit + Default Roots [MAJOR]

**Claim Challenged:** The Steelman's forward-compatibility case (SM-003) argues `--root` is "exactly the escape hatch a standalone package needs" and that `get_containment_roots` is "a small, pure, directly-callable function... independently callable from any future consumer."

**Counter-Argument:** The function signature `get_containment_roots(explicit_root: str | None = None) -> list[Path]` accepts exactly one optional string, not a list. A legitimate workflow — "validate a file in my project AND a file in a sibling monorepo package in the same invocation," or the Steelman's own cited future consumers ("`jerry agents build` output paths, transcript ingestion") that may need both the project root and an external staging location simultaneously — has no way to express that today. The only workaround is invoking the command twice with different `--root` values, which defeats the purpose of a single escape-hatch flag and doubles the operational burden for exactly the "standalone package, arbitrary integrator" scenario the Steelman argues this design is prepared for.

**Evidence:** `project_root.py:120` signature; `parser.py:585-593` `_add_root_argument` has no `action="append"` or list-typed default.

**Impact:** The "escape hatch" only escapes to a single new location, not an expanded one — for any workflow needing more than one non-default root, the design offers no combinator, contradicting the Steelman's own claim that this shape is ready for arbitrary future integrators.

**Dimension:** Completeness

**Response Required:** Either document this as an accepted, scoped-out limitation (with a rationale for why single-root is sufficient for the currently known consumers), or extend `--root` to be repeatable / add a separate additive flag.

**Acceptance Criteria:** Explicit scope statement in the BUG-010 entity or a follow-up work item, so the gap is tracked rather than silently absent.

---

### DA-003: Five-Branch Runtime Behavior Matrix Exceeds Reasonable Cognitive Load [MAJOR]

**Claim Challenged:** The Steelman (SM-001) frames the design as "two orthogonal modes... not a single fuzzy default trying to do both jobs at once," implying a clean, low-complexity mental model.

**Counter-Argument:** The Steelman's own 2-row mode table undercounts the actual runtime surface. Reconstructing the real behavior matrix from the shipped code yields five distinct, observably-different outcomes a user must predict correctly before typing a command:

| # | Scenario | Outcome |
|---|----------|---------|
| 1 | No `--root`, file under project root | Succeeds silently |
| 2 | No `--root`, file under temp/scratchpad default, owned by current user | Succeeds, prints stderr **Note** (R-4) |
| 3 | No `--root`, file under temp/scratchpad default, owned by a *different* user | **Rejected** with an ownership error (H-01 gate) |
| 4 | `--root` supplied, file under it, root is "broad" (fs root / `$HOME` / ancestor of `$HOME`) | Succeeds, prints stderr **WARNING** (R-3) |
| 5 | `--root` supplied, file NOT under it (even if under the project root) | **Rejected**, "Path escapes allowed containment roots" |

Two of these five branches (#2, #4) are gated by independent, unsuppressible stderr side channels the user cannot predict without already knowing the internal root-classification logic. This is a materially larger conceptual surface than "read a markdown file" warrants, and larger than the Steelman's own summary implies.

**Evidence:** `_check_path_containment` (`ast_commands.py:290-367`), `_check_temp_root_ownership` (`ast_commands.py:244-287`), `_warn_if_temp_root_match` (`ast_commands.py:212-241`), `_is_broad_containment_root`/warning branch (`project_root.py:63-117`, `159-169`).

**Impact:** Users cannot reliably predict, from the command they are about to type, whether it will (a) succeed silently, (b) succeed with extra output, or (c) fail — without already understanding root-classification internals that are documented only in code comments and the internal engineering plan, not in `--help` output.

**Dimension:** Methodological Rigor

**Response Required:** Either consolidate the behavior surface (e.g., a single `--verbose`-style flag controlling both R-3/R-4 visibility, reducing branch count perceived by the user), or produce user-facing documentation (help text or a `jerry ast --help-containment` style reference) that lays out this matrix explicitly, so the complexity is discoverable rather than only reconstructable by reading source.

**Acceptance Criteria:** A single authoritative user-facing reference (in `--help` output or linked docs) enumerating all five outcomes, OR a design simplification that reduces the branch count.

---

### DA-004: R-4/R-3 Stderr Output Contradicts the Design's Own "stdout Reserved for JSON" Claim Under Common Stream-Merging [CRITICAL]

**Claim Challenged:** BUG-010.md Fix Approach states explicitly: *"Two owner-resolved stderr transparency behaviors (stdout is reserved for the JSON/render payload)"* — i.e., the design's own stated safety property is that machine consumers of JSON output are protected because diagnostics never touch stdout.

**Counter-Argument:** This claim is true only if stdout and stderr are consumed as genuinely separate streams by every caller. That is not a safe universal assumption: shell redirection (`2>&1`), many CI log-capture configurations, and `subprocess.run(..., capture_output=True)` followed by naive `stdout + stderr` concatenation are all extremely common integration patterns — and the Steelman's own SM-003 argues this exact CLI is designed to be invoked by "a CI runner, a pre-commit hook, a doc-generation pipeline, or a completely different agent framework" via `--root`-driven automation. Under any of those merged-stream patterns, R-4's transparency note ("Note: '{file_path}' is outside the project root; jerry ast is operating on a temp/scratchpad path...") or R-3's warning gets interleaved directly into what the consumer expects to be pure, parseable JSON — silently corrupting the payload from the consumer's point of view (a `json.loads()` on merged output would raise or, worse, partially parse depending on where in the stream the extra line lands relative to the JSON object boundaries).

Critically, R-4 is **not** an edge case: per the Steelman's SM-002, the temp/scratchpad-root inclusion exists specifically to serve the *primary* stated use case — an agent's own scratchpad output. That means the stderr note fires on what the design itself argues is the common path, not a rare corner case, maximizing exposure to this failure mode rather than minimizing it.

**Evidence:**
- `BUG-010-ast-project-root.md:69` — the explicit "stdout is reserved for..." claim.
- `_warn_if_temp_root_match` (`ast_commands.py:235-241`) — fires unconditionally on every temp-default match, `print(..., file=sys.stderr)`, no suppression flag.
- `parser.py` — no `--quiet`, `--no-warn`, `--json-only`, or similar suppression flag exists anywhere in `_add_root_argument` or the broader `_add_ast_namespace`.
- `eng-lead-implementation-plan.md` R-4 risk row explicitly flags: *"adds output-format risk (JSON-mode callers must not have stderr diagnostics leak into stdout JSON)"* — this acknowledges the *stdout* risk but never actually evaluates or resolves the *merged-stream consumer* risk, which is the deeper and more realistic failure mode.

**Impact:** Any automated consumer that merges stdout/stderr (a common, not exotic, integration choice) receives corrupted or unparseable output specifically when the tool is operating on its own stated primary intended workload (agent scratchpad files). This is a self-contradiction between the design's stated safety property and its actual behavior under realistic consumption patterns, not merely a cosmetic UX nit.

**Dimension:** Internal Consistency

**Response Required:** At minimum: (a) explicitly document, in both the BUG-010 entity and the `--root`/general `--help` text, that callers MUST NOT merge stdout/stderr if they intend to parse JSON output, with a concrete example of the failure mode; (b) add a suppression mechanism (`--quiet`, or an env var mirroring `JERRY_DISABLE_PATH_CONTAINMENT`'s pattern) so automated callers can opt out of R-3/R-4 noise entirely; (c) consider whether R-4 in particular should be demoted from "always fires" to "fires only outside JSON/automation contexts" (e.g., gated on a TTY check or an explicit `--verbose` opt-in) given it fires on the design's own primary use case.

**Acceptance Criteria:** Either a suppression flag/env var exists and is documented, or an explicit, owner-confirmed acceptance of the merged-stream corruption risk is recorded in the BUG-010 entity's risk table (matching the rigor already applied to R-1/R-2/R-5/R-6/R-7 in the eng-lead plan, none of which currently covers this specific failure mode).

---

### DA-005: R-3's Broad-Root Warning Is Advisory-Only With No Suppression — Provides Zero Enforcement While Still Generating Guaranteed Noise for Legitimate Use [MAJOR]

**Claim Challenged:** The design frames the R-3 stderr WARNING as meaningful transparency/protection for a genuinely risky configuration (`--root` pointed at a filesystem root or `$HOME`).

**Counter-Argument:** The warning is printed and the invocation *always* proceeds regardless — `get_containment_roots` prints the warning then unconditionally returns `[resolved_root]` with no confirmation gate, no exit code change, and no way to opt out. This design conflates two meaningfully different situations under one alarming signal: (a) a user who mistakenly typed a broad path (where a warning is genuinely useful, though non-blocking), and (b) a user who *deliberately and correctly* wants a broad root (e.g., a dotfiles repository rooted at `$HOME`, or a documentation generator legitimately operating across an entire drive) — who now sees a scary "WARNING... path containment is effectively disabled" message on every single invocation, forever, with no way to acknowledge-once and silence it. This is the definition of alert fatigue: an unblockable, unsilenceable warning trains users (and any scripts scraping stderr) to ignore it, which defeats R-3's own transparency purpose for the case where it would actually matter.

**Evidence:** `project_root.py:159-169` — warning print block followed unconditionally by `return [resolved_root]`; no `--yes`/`--confirm`/`--i-know-what-im-doing` flag exists anywhere in `parser.py`.

**Impact:** Zero actual enforcement benefit (a truly malicious or badly-scripted `--root /` still proceeds) combined with guaranteed, permanent noise for any legitimate broad-root workflow — the worst combination of intrusiveness and ineffectiveness.

**Dimension:** Actionability

**Response Required:** Either (a) add a one-time acknowledgment mechanism (a flag or a cached confirmation) so legitimate broad-root users are not warned on every invocation, or (b) accept and document that this is deliberately "informational, not protective" and that repeat-warning noise for legitimate users is an accepted trade-off.

**Acceptance Criteria:** A documented rationale for choosing "always-warn, never-block, never-silence" specifically, distinguishing it from the alternative of a one-time confirmation gate.

---

### DA-006: Shipped `--help` Text Omits the Design's Single Most Consequential, Counter-Intuitive Fact [MAJOR]

**Claim Challenged:** The design is documented (BUG-010 entity, eng-lead plan, module docstrings) as a coherent, well-reasoned two-mode system — but documentation quality should be assessed at the point the *end user* actually encounters it, not only in internal engineering artifacts.

**Counter-Argument:** The only text a `jerry ast` end user is likely to ever read is `--help` output. The shipped help string for `--root` is: *"Restrict path containment to exactly this directory (overrides the default project-root + temp-dir allowed set). User discretion: use to run 'jerry ast' against any location."* This never states the concrete, surprising consequence in the user's own terms: *"if you supply --root, files in your own project that are NOT under the given root will be rejected, even though they would normally work."* The word "overrides" is present but requires the reader to already understand the underlying allowed-set model to infer that consequence — it is implementation-perspective phrasing, not outcome-perspective phrasing. The rich, precise explanation of exclusivity that exists (in the module docstring and the internal eng-lead plan) never reaches the interface surface an actual user interacts with.

**Evidence:** `parser.py:585-593` (shipped `--help` text) vs. `project_root.py:120-158` (module docstring, never surfaced via `--help`) vs. `eng-lead-implementation-plan.md:59-66` (pseudocode docstring, an internal artifact).

**Impact:** A user who reads `--help` before using the flag — the correct, diligent behavior — still will not learn the single fact most likely to cause a confusing rejection later.

**Dimension:** Traceability

**Response Required:** Rewrite the `--root` help text to state the rejection consequence explicitly in outcome terms, e.g.: *"...WARNING: files outside this directory, including files in your normal project root, will be rejected while --root is set."*

**Acceptance Criteria:** Updated help text reviewed for whether a first-time reader (not already familiar with the containment model) could correctly predict the rejection behavior from the text alone.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- **DA-004:** Resolve the stdout/stderr merged-consumption corruption risk for R-3/R-4 before merge — this is the one finding that directly contradicts an explicit design claim ("stdout is reserved for the JSON/render payload") under realistic, non-exotic conditions, and fires on the design's own stated primary use case.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-001:** Document or resolve the `--root` naming/semantics mismatch with common CLI additive-flag conventions.
- **DA-002:** Document as an accepted, scoped-out limitation (or add a combinator) that `--root` cannot be combined with the project-root/temp defaults.
- **DA-003:** Publish a user-facing reference for the 5-branch behavior matrix, or reduce branch count.
- **DA-005:** Document the rationale for "always-warn, never-block, never-silence" on R-3, or add a one-time acknowledgment mechanism.
- **DA-006:** Rewrite `--root` help text to state the project-file-rejection consequence in outcome terms.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-007:** Consider softer error phrasing for the ownership-gate rejection, or acknowledge the vocabulary mismatch as acceptable for this persona.
- **DA-008:** Acknowledge, in the BUG-010 entity, that this "bug" now bundles a scope-widening security/policy feature, and note whether future similar widenings should be split into a separate design-note/ADR entity per eng-lead's own "house pattern" recommendation (which argues this pattern *should* be reusable infrastructure — reusable infrastructure decisions arguably warrant their own decision record, not a bug-entity appendix).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001/DA-002: the additive-root combinator use case and the naming-convention mismatch are unaddressed; the design's "two orthogonal modes" framing omits a real third need (combined roots) |
| Internal Consistency | 0.20 | Negative | DA-004: the design's own explicit "stdout reserved for JSON" safety claim is contradicted under realistic merged-stream consumption of its own primary use case |
| Methodological Rigor | 0.20 | Negative | DA-003: the actual runtime behavior surface (5 branches, 2 independent side channels) exceeds the complexity the design's own 2-mode framing implies; DA-008: scope-widening bundled into a bug-fix work item without a dedicated design record |
| Evidence Quality | 0.15 | Neutral | Findings are themselves evidence-grounded (file:line citations throughout); no negative evidence-quality claim against the deliverable beyond DA-007's persona-fit concern |
| Actionability | 0.15 | Negative | DA-005: R-3's warning provides no actual enforcement action and cannot be silenced by a legitimate user, undermining its own stated transparency purpose |
| Traceability | 0.10 | Negative | DA-006: the precise, correct exclusivity rationale that exists in internal docs never traces through to the user-facing `--help` surface |

---

*S-002 Devil's Advocate execution complete (Group C, blind to Groups A/B/D-F sibling reviewers). Scope confined to UX/conceptual-complexity lens per invocation directive; security predicate soundness (M-08/M-10/TOCTOU/H-01/H-02 remediation) is out of scope for this execution and was independently validated as sound by S-003 Steelman (Group B) and RED-BUG010 (red-vuln-findings.md). Findings routed for consolidation at S-014 scoring.*

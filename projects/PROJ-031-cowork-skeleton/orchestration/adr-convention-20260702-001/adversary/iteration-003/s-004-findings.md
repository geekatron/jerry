# Pre-Mortem Report: ADR Identifier, Location, and Promotion Convention (PROJ-031, iteration 3)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverables reviewed |
| [Header](#header) | Required S-004 header block |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All failure causes at a glance |
| [Finding Details](#finding-details) | Expanded Critical/Major findings with evidence |
| [What the Package Already Prevents](#what-the-package-already-prevents) | Failure paths already closed (per task instruction) |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Execution Context

- **Strategy:** S-004 (Pre-Mortem Analysis)
- **Template:** `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (692 lines)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (297 lines)
- **Criticality:** C4 (per deliverable's own classification)
- **Engagement quality gate:** 0.95
- **Iteration:** 3 (blind independent review; prior iteration findings not consulted per tournament-integrity protocol)
- **Executed:** 2026-07-02

---

## Header

```markdown
**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** ADR-PROJ031-004-adr-identifier-convention.md + adr-standards-rule-draft.md
**Criticality:** C4
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind iteration 3)
**H-16 Compliance:** NOT independently verifiable this iteration -- see PM-107 (blind-protocol constraint;
   no blocking STOP issued because the deliverable shows strong internal evidence of steelman treatment --
   see Finding PM-107)
**Failure Scenario:** It is 2027-07-02. The ADR-identifier convention is functionally dead. New ADRs still
   arrive in three or four incompatible styles. The CI lint either never shipped, or shipped and now silently
   blocks every attempt to add a legitimate one-off exception because nobody with a distinct reviewing identity
   exists to approve a waiver. The showcase self-promotion (M-9) never happened, so the convention's own
   flagship ADR is still filed under the discouraged dialect a year after "ratification." A newly onboarded
   contributor, confronted with a 692-line ADR and a 297-line companion rule file (10 lint rules, 3 promotion
   paths, a closed dialect-prefix enumeration, a waiver-ledger schema), picks the shortest path: `ADR-NNN-slug.md`,
   bare, again.
```

---

## Summary

Two full remediation cycles (iter-1 score 0.67, iter-2 score 0.54, per the ADR's own Changelog) have already closed
the dominant, highest-RPN structural defects: the L-1 grandfather-breaking regex, the unaudited lint-bypass comment,
the missing 9th ID family, the "collision-free by construction" overclaim, and the un-fixed producing agent. Those
fixes hold up under this iteration's independent verification (see [What the Package Already Prevents](#what-the-package-already-prevents)).
Working backward from a declared 12-month failure, this iteration surfaces **three new Major failure causes that
survive the prior two rounds** because they require live-repository verification the document itself does not
perform: (1) the `.claude/rules/` auto-load migration step (M-2b) is built on a stale mental model of a mechanism
that filesystem evidence shows already operates at the directory level, making the gating item either impossible
or moot as literally specified; (2) the redesigned waiver/override mechanism (RT-004/CC-001 fix) requires a
"distinct GitHub identity with review authority," but the live `.github/CODEOWNERS` shows exactly one owner
(`@geekatron`) for every governed path, including the paths this convention touches -- so the MEDIUM-tier
"overridable with justification" promise is currently unsatisfiable in practice, one of the three failure
conditions the invoking task named verbatim ("the lint blocks legitimate work"); (3) the lint's two delivery
targets (M-6 GitHub Action vs. M-13 `uv run jerry lint adr` CLI subcommand) describe two different artifacts
with no unifying build spec, risking a silent gap in exactly the downstream/plugin deployment context PROJ-031
exists to serve. **Recommendation: REVISE.** None of the three is a defect in the core naming decision (D-1
through D-5, Scheme B); all three are in the Migration Plan / Enforcement Design machinery that must actually
run for the decision to have effect -- and Pre-Mortem's job is precisely to stress that machinery before it is
relied upon.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-101-i3 | M-2b `.claude/rules/` symlink step is based on a stale/incorrect model of an already directory-level auto-load mechanism | Process | High | Major | P1 | Methodological Rigor |
| PM-102-i3 | Waiver "distinct second-reviewer" mechanism (RT-004/CC-001 fix) is unsatisfiable in a verified solo-maintainer repo -- MEDIUM tier becomes de-facto HARD in practice | Resource / Process | High | Major | P1 | Internal Consistency |
| PM-103-i3 | M-6 (GitHub Action) and M-13 (`jerry lint adr` CLI subcommand) specify two unreconciled build targets for "the lint" | Technical | Medium | Major | P1 | Completeness |
| PM-104-i3 | Document never applies its own prescribed `<!-- adr-lint: example -->` exemption to its ~dozen inline stale-citation examples -- L-8 will likely fire on its own showcase artifact first | Process | Medium | Minor | P2 | Actionability |
| PM-105-i3 | L-1a grammar does not prevent the exact organic ad hoc versioning anti-pattern (`-v2` in the slug) the ADR criticizes Scheme F for enabling | Process | Medium | Minor | P2 | Internal Consistency |
| PM-106-i3 | Fix-3 occurrence count ("~6") still undercounts the verified grep result (7) | Evidence Quality | Confirmed | Minor | P2 | Evidence Quality |
| PM-107-i3 | H-16 (S-003 prerequisite) cannot be independently confirmed under the blind-review protocol; no explicit "S-003 output: {path}" pointer exists in either deliverable | Traceability | N/A | Minor | P2 | Traceability |

**Finding ID format:** `PM-{NNN}-i3` where `i3` denotes iteration 3 of this tournament, distinguishing these
identifiers from the in-document `PM-00N` tags left by prior iterations (see the deliverable's own tag glossary,
`ADR-PROJ031-004...md:46`).

---

## Finding Details

### PM-101-i3: Migration item M-2b rests on a stale model of the `.claude/rules/` auto-load mechanism [MAJOR]

**Failure Cause:** The Migration Plan lists, as a **gating ("Yes")** item: *"M-2b | Create the `.claude/rules/adr-standards.md` **symlink** so the new rule auto-loads at session start (the CLAUDE.md `.claude/rules/` mechanism; precedent `PROJ-007/EN-001.md:53` treats this as its own deliverable). Without it the ratified rule never loads (PM-003)."* (`ADR-PROJ031-004-adr-identifier-convention.md:452`). This describes creating a **new, individual, per-file symlink** as a discrete action distinct from authoring the rule file itself (M-2).

**Category:** Process (Migration Plan mechanics), bordering Technical.

**Likelihood:** High -- this is not hypothetical; it is a verifiable property of the live repository that a future ratifier will encounter the first time they try to check M-2b off.

**Severity:** Major -- does not invalidate the naming convention, but creates a permanently unsatisfiable (or trivially-already-satisfied, depending on interpretation) gating checklist item that a future maintainer cannot correctly close as literally written, risking either (a) indefinite non-ratification because M-2b "can't be verified," or (b) a maintainer manually forcing a per-file symlink that conflicts with the existing directory-level symlink.

**Evidence:**
- CLAUDE.md itself uses **singular** phrasing: `"**(A)** = Auto-loaded into Claude Code context at session start via `.claude/rules/` symlink."` (`CLAUDE.md:49`) -- one symlink, not "symlinks."
- Live filesystem verification performed this iteration: `Glob(".claude/rules/*.md")` returns **no files found**, and `Glob(".claude/**")` does not list a `rules/` entry at all -- yet `Read(".claude/rules/quality-enforcement.md")` succeeds and returns the file's real content directly. This is the diagnostic signature of a single **directory-level** symlink (`.claude/rules` -> `.context/rules`) rather than N per-file symlinks: Glob does not traverse into the symlinked directory, but direct path resolution (Read) does.
- Under a directory-level symlink, any file landing in `.context/rules/adr-standards.md` (M-2) is **immediately and automatically** visible at `.claude/rules/adr-standards.md` with **zero additional action**. There is nothing to separately "create."
- The cited precedent, `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/EN-001.md:53`, describes a **different-era** mechanism: `"Auto-load symlinks | -- | .claude/rules/ symlinks for new rule files | C2"` -- plural "symlinks," implying per-file management at that time. The mechanism has since been consolidated into a single directory symlink (or was always one and PROJ-007's own item description was imprecise), and M-2b imports that stale per-file model without re-verifying it against the current repo state -- exactly the kind of unverified load-bearing claim this Pre-Mortem strategy exists to catch.

**Dimension:** Methodological Rigor -- the Migration Plan's own gating items are held to a lower verification bar (P-022 self-audit) than the document applies everywhere else (e.g., the Glob-verified "lint scripts do not exist" Claim-Status, or the CV-001/CV-002 corrections).

**Mitigation:** Before ratification, verify empirically whether `.claude/rules` is a directory-level symlink (e.g., `ls -la .claude/` showing `rules -> ../.context/rules`) or a set of per-file symlinks. If directory-level (as this iteration's evidence strongly suggests), delete M-2b from the gating list entirely and replace it with a one-line non-gating verification note ("confirm `.claude/rules/adr-standards.md` is readable after M-2 lands -- expected to be automatic"). If per-file (contradicting this iteration's evidence), keep M-2b but correct the rationale to cite the *current* mechanism, not the PROJ-007-era EN-001 precedent.

**Acceptance Criteria:** The Migration Plan's M-2b row states, with a verified citation to the actual current symlink structure, whether the item is (a) automatic and non-gating, or (b) a genuine manual step, and removes the stale EN-001 justification if superseded.

---

### PM-102-i3: The redesigned waiver mechanism requires a "distinct" second reviewer that does not exist in this repo [MAJOR]

**Failure Cause:** The Enforcement Design section's headline P0-8 fix replaces a "self-reported" `approved_by` check with one requiring **"a distinct GitHub identity with review authority"** whose approval is API-verified against the PR's actual approving reviewers (`ADR-PROJ031-004-adr-identifier-convention.md:578,584`; identical language in `adr-standards-rule-draft.md:193`). This is presented as the fix that makes L-1 through L-4 and L-7 legitimately MEDIUM-tier ("overridable with documented justification") rather than de-facto HARD (the CC-001 correction, `ADR-PROJ031-004...md:584`).

**Category:** Resource / Process.

**Likelihood:** High -- confirmed true today, not merely probable in the future.

**Severity:** Major -- if no second reviewing identity can ever exist, every FAIL-class rule this convention introduces (L-1a, L-1b, L-2, L-3, L-4, L-7, L-9) becomes **permanently non-waivable** for any legitimate edge case, which is precisely the CC-001 contradiction ("MEDIUM tier calling a rule non-waivable is de-facto HARD") the document already flagged and claims to have fixed once -- reappearing here through a staffing-reality channel the fix never checked against.

**Evidence:**
- `.github/CODEOWNERS` (read in full this iteration) lists exactly **one** owner, `@geekatron`, for every governed path in the repository, including the exact path this convention's new rule file lands in: `.context/rules/ @geekatron` (`.github/CODEOWNERS:14`). No other identity appears anywhere in the file.
- `scripts/` (where `scripts/adr-lint-waivers.yaml` and `scripts/lint_adr_convention.py` are proposed to live, `ADR-PROJ031-004...md:552`) has **no CODEOWNERS entry at all** -- only `.github/workflows/`, `.github/dependabot.yml`, `.github/CODEOWNERS`, `.pre-commit-config.yaml`, `.context/rules/`, and `docs/governance/` are covered (`.github/CODEOWNERS:8-15`). The waiver ledger the whole mechanism depends on is not even under branch-protection review coverage as specified.
- The session's own git identity (`Git user: geekatron`) matches the sole CODEOWNERS entry, corroborating a single-maintainer operating reality rather than a team.
- Task's own explicit failure condition to test for: **"the lint blocks legitimate work."** A solo maintainer who needs one legitimate, well-justified exception (the exact scenario CC-001's fix was designed to permit) has no path to a valid waiver under the mechanism as specified, because the mechanism structurally requires a *distinct* identity from the author.

**Dimension:** Internal Consistency -- the document's own tier-reconciliation argument (CC-001, "L-2/L-3 are waivable in principle, not HARD, because a reviewer can approve a justified exception") is falsified by the repo's actual staffing, which the document never checks.

**Mitigation:** Either (a) explicitly define a fallback waiver path for solo-maintainer operation (e.g., a time-delayed self-approval with a mandatory public justification comment and an automatic expiry, distinct from the multi-reviewer path used when a second maintainer exists), or (b) honestly downgrade the claim from "this is legitimately MEDIUM because waivers are real" to "this is MEDIUM in intent, but until a second maintainer joins, FAIL rules are non-waivable in practice -- treat accordingly," and add `scripts/` (or at minimum the waiver ledger file) to CODEOWNERS so the mechanism is at least routed correctly once a second identity exists.

**Acceptance Criteria:** The Enforcement Design section states, with a citation to the live CODEOWNERS file, what happens when a waiver is needed and no second reviewing identity is available -- rather than presenting the multi-reviewer path as though it is unconditionally operative today.

---

### PM-103-i3: M-6 and M-13 specify two unreconciled delivery targets for "the lint" [MAJOR]

**Failure Cause:** The ADR's own Enforcement Design section states the lint's suggested home is `scripts/lint_adr_convention.py`, "run via `uv run` ..., wired into `.github/workflows/` CI" (`ADR-PROJ031-004-adr-identifier-convention.md:552`), and Migration item M-6 tracks exactly that artifact as the ratification blocker (`:457`). Separately, gating item **M-13** requires the *same* deliverable to *also* ship as a `uv run jerry lint adr` **CLI subcommand**, "or explicitly disclose the CLI path as advisory-only if deferred" (`:464`), justified by the Enforcement Scope section's claim that the retained `src/` + `pyproject.toml` + `uv.lock` "make the `jerry` CLI runnable in a plugin install" (`:570`).

**Category:** Technical.

**Likelihood:** Medium -- plausible that M-6 (the CI Action, easier to build and directly gating ratification) ships first and is marked done, while M-13's CLI-subcommand form, which requires touching the actual `src.interface.cli` package rather than a standalone `scripts/` file, is quietly deferred because no single spec unifies the two.

**Severity:** Major -- if realized, this exactly reproduces the failure the Enforcement Scope section itself warns against: *"the 'central enforcement mechanism' claim is true for the source repo but silently false for the exact CoWork distribution target PROJ-031 exists to serve"* (`:573`) -- i.e., the document already names the risk but does not close the architectural gap that would let it happen.

**Evidence:**
- `pyproject.toml:65`: `jerry = "src.interface.cli.main:main"` -- the actual CLI entrypoint is inside the `src` package.
- `pyproject.toml:72-73`: `[tool.hatch.build.targets.wheel] packages = ["src"]` -- only `src/` is packaged; a file placed at `scripts/lint_adr_convention.py` is not automatically importable as a `jerry` subcommand without deliberate wiring (a `src.interface.cli` dispatcher entry) that neither M-6 nor M-13 specifies.
- Both migration items are marked with independent "Yes" gating status ("Yes (source-repo Action); CLI form Yes-or-disclosed," `:464`), but no single task/spec item owns making the two consistent (e.g., "implement the checks once, in `src/`, expose via both a thin `scripts/` CI wrapper and a `jerry lint adr` subcommand").

**Dimension:** Completeness -- the Migration Plan enumerates both deliverables but omits the integration step connecting them.

**Mitigation:** Add an explicit migration item (or fold into M-6) specifying that the lint logic lives in `src/` (e.g., `src/application/adr_lint/` or equivalent, consistent with the hexagonal layering H-07 already requires elsewhere in this framework), with `scripts/lint_adr_convention.py` (if kept at all) reduced to a thin CI-invocation wrapper, and `jerry lint adr` registered as a real CLI subcommand against the same logic -- one implementation, two invocation surfaces, not two independent deliverables.

**Acceptance Criteria:** A single Task (with GH Issue per H-32) exists whose description states the lint logic's package location and both invocation surfaces (CI Action + `jerry lint adr` subcommand) explicitly, closing the ambiguity between `:552` and `:570`.

---

## What the Package Already Prevents

Per the task's explicit instruction to check which failure paths the package already closes, this iteration
independently re-verified (not merely re-read) the following claims, all of which hold:

| Prior finding | Verified this iteration | Evidence |
|---|---|---|
| Lint scripts do not exist yet ("DESIGNED, NOT BUILT") | **Confirmed true** | `Glob("scripts/lint_adr_convention.py")` -> no files found |
| Zero worktracker Task/GH-Issue entities exist for Migration Plan rows | **Confirmed true** | `Glob("projects/PROJ-031-cowork-skeleton/work/**")` lists 22 real entities, none referencing ADR-standards migration items |
| Dangling `ADR-CI-001` citation at `.github/workflows/ci.yml:2` cites a non-existent project | **Confirmed true** | `Read(".github/workflows/ci.yml")` line 2 cites `projects/PROJ-001-plugin-cleanup/...`; `Glob("projects/PROJ-001*")` -> no files found |
| Template `docs/knowledge/exemplars/templates/adr.md` uses bare `ADR-{NUMBER}` and dangling `docs/decisions/` path | **Confirmed true** | Read lines 1 and 182 match citations exactly |
| `skills/architecture/SKILL.md` uses `ADR_NNN` underscore form | **Confirmed true** | Read line 105 matches citation exactly |
| `ps-architect.md` Fix-3 phantom paths (`templates/adr.md`, `python3 scripts/cli.py`) and non-canonical filename grammar | **Confirmed true** (see also PM-106-i3 for a minor count correction) | Grep of `skills/problem-solving/agents/ps-architect.md` matches lines 218, 260, 263, 267-268, 482, 509 |
| Three `docs/design/` framework ADRs use informal HTML-comment provenance, not YAML frontmatter | **Confirmed true** | `Read("docs/design/ADR-agent-design-001.md")` line 3 shows `<!-- PS-ID: PROJ-007 | ENTRY: e-004 ... -->`, not YAML |
| `.github/CODEOWNERS` covers `.context/rules/` (where the new rule file lands) | **Confirmed true, but see PM-102-i3** | `.github/CODEOWNERS:14` |

The grandfather-preserving L-1a/L-1b split, the bidirectional L-7 tombstone check, and the honest Claim-Status
framing are sound engineering responses to real, verified problems and are not re-litigated here.

---

## Recommendations

**P0 (none this iteration)** -- no failure cause meets the Critical-severity bar; the core naming decision (D-1
through D-5) is not at risk.

**P1 (Important -- SHOULD mitigate before ratification):**
- PM-101-i3: Verify the actual `.claude/rules/` symlink structure before ratification; correct or remove M-2b accordingly.
- PM-102-i3: Define an explicit solo-maintainer waiver fallback, or honestly disclose that FAIL rules are non-waivable in practice until a second maintainer exists; add the waiver ledger path to CODEOWNERS.
- PM-103-i3: Add a single migration item that unifies the M-6 CI-Action and M-13 CLI-subcommand delivery targets into one buildable spec.

**P2 (Monitor -- MAY mitigate; acknowledge risk):**
- PM-104-i3: Apply the `<!-- adr-lint: example -->` tag (or a seeded allowlist entry) to this document's own inline stale-citation examples before it is promoted and becomes the first document L-8 scans.
- PM-105-i3: Add an explicit MEDIUM standard discouraging ad hoc version suffixes (`-v2`) inside the domain-slug segment, reinforcing that `NNN` is the sanctioned versioning mechanism.
- PM-106-i3: Correct "~6" to "7" (or re-verify) in the Fix-3 occurrence count.
- PM-107-i3: Add an explicit "S-003 output: {path}, applied {date}" pointer to the deliverable so future blind reviewers (and the S-004 template's own Prerequisites check) can verify H-16 compliance without relying on inferential evidence.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-103-i3: the lint's downstream/plugin delivery path is enumerated but not architecturally closed |
| Internal Consistency | 0.20 | Negative | PM-102-i3: the CC-001 tier-reconciliation claim ("legitimately MEDIUM because waivers are real") is contradicted by the verified solo-maintainer CODEOWNERS state |
| Methodological Rigor | 0.20 | Negative | PM-101-i3: a gating Migration Plan item rests on an unverified, apparently stale, mechanism model -- a lower verification bar than the document applies to its own other claims |
| Evidence Quality | 0.15 | Neutral-to-Negative | PM-106-i3 is a minor, already-mostly-correct count; all other load-bearing citations independently re-verified this iteration hold up (see [What the Package Already Prevents](#what-the-package-already-prevents)) |
| Actionability | 0.15 | Negative | PM-104-i3: L-8's own showcase document is not pre-tagged, risking day-one alert fatigue that undercuts the lint's actionability once live |
| Traceability | 0.10 | Negative | PM-107-i3: no explicit S-003 output pointer exists in either deliverable for this iteration to verify against |

**Net assessment:** No Critical findings; 3 Major (all in Migration Plan / Enforcement Design machinery, not the
core decision) and 4 Minor. Consistent with the REVISE recommendation in the Summary -- targeted fixes to three
specific migration/enforcement items, not a redesign of the naming scheme itself.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 0
- **Major:** 3 (PM-101-i3, PM-102-i3, PM-103-i3)
- **Minor:** 4 (PM-104-i3, PM-105-i3, PM-106-i3, PM-107-i3)
- **Protocol Steps Completed:** 6 of 6 (Set the Stage; Declare Failure/Perspective Shift; Generate Failure Causes across all 5 category lenses; Prioritize by Likelihood x Severity; Develop Mitigations; Synthesize and Score Impact)
- **H-16 Note:** Not independently verifiable under the blind-review protocol this iteration (see PM-107-i3); not treated as a blocking STOP given strong internal evidence of steelman treatment throughout the deliverable's [Options Considered](../../../../decisions/ADR-PROJ031-004-adr-identifier-convention.md#options-considered-af) section and documented two-iteration adversarial history.

---

*Report generated by adv-executor (S-004 Pre-Mortem Analysis), blind tournament iteration 3.*
*P-003: No subagents spawned. P-020: No deliverable files edited -- report only. P-022: Every factual claim above cites a specific file+line independently re-verified this iteration via Read/Glob/Grep; inferential judgments (likelihood ratings, failure-scenario narrative) are labeled as such.*

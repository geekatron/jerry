# BUG-010 Option C — C4 Tournament Consolidated Findings

> Re-score tournament (pass 2) on the Option C `jerry ast` containment redesign, branch `fix/BUG-010-ast-project-root` @ `cce557c5`. Consolidates the eng-reviewer gate + all nine adversarial strategy passes (S-010, S-003, S-001, S-002, S-004, S-007, S-011, S-013, S-012), deduped. Prepared before the S-014 scorer runs, so revision precedes scoring (H-14).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Strategy Roster](#strategy-roster) | The passes and their headline verdicts |
| [Disposition A — Code Fixes](#disposition-a--code-fixes) | Confirmed defects to fix before scoring |
| [Disposition B — Governance/Traceability Fixes](#disposition-b--governancetraceability-fixes) | Artifact drift to reconcile |
| [Disposition C — Owner Decisions](#disposition-c--owner-decisions) | Forks requiring sign-off |
| [Disposition D — Deferred / Tracked](#disposition-d--deferred--tracked) | Known items with existing issues |
| [Disposition E — Already Settled / Overstated](#disposition-e--already-settled--overstated) | Re-litigation, no action |
| [Corroboration Map](#corroboration-map) | Which strategies found what |

---

## Strategy Roster

| Pass | Strategy | Headline |
|------|----------|----------|
| eng-reviewer | Engineering gate | PASS at S-014 0.955; one stale-docstring nit |
| S-010 | Self-Refine | 4 Major / 3 Minor |
| S-003 | Steelman | Constructive; no defects |
| S-001 | Red Team | 1 Critical (write-path TOCTOU) / 2 Major |
| S-002 | Devil's Advocate | Trust-model challenges (mostly re-litigation) |
| S-004 | Pre-Mortem | 2 Critical (scratchpad break; Windows CI) |
| S-007 | Constitutional | 2 Critical (H-32 issue drift; H-07c) / 4 Major |
| S-011 | Chain-of-Verification | C2 claim PARTIALLY-TRUE; rest verified |
| S-013 | Inversion | Shared-temp trust; --quiet adoption |
| S-012 | FMEA | Top RPN 288 = write-path TOCTOU |

**Consensus:** the containment *redesign* is technically sound — the six prior Criticals are independently re-confirmed dissolved. The residual risk concentrated in (1) one real write-path race, (2) governance-artifact drift, and (3) two scope/architecture decisions.

---

## Disposition A — Code Fixes

| ID | Finding | Corroboration | Fix | Location |
|----|---------|---------------|-----|----------|
| A-1 | **Write-path check≠use TOCTOU (CWE-367).** `ast_modify` validates a fresh resolution (line 635) but discards it (`_,`) and writes to `target_path` from a separate earlier `resolve()` (line 620). A symlink swap between the two resolutions escapes containment on write. | **5 strategies:** SR-001, RT-001, RT-003, S-011, FM-001 (RPN 288) | Use the validated `resolved` from the write-time check as `target_path`; drop the separate line-620 resolve (fall back to it only when enforcement is disabled). Add a double-swap regression test. | `ast_commands.py:620,635,644,654` |
| A-2 | **Broad project root never warns.** `is_broad` is computed for the project root but its warning is unconditionally suppressed; `get_project_root()` is just `CLAUDE_PROJECT_DIR`/cwd with no broadness check, so `CLAUDE_PROJECT_DIR=/` grants whole-filesystem trust silently. | RT-002, FM-005 | Emit the broad-root stderr warning for a broad project root too (suppressible by `--quiet`). | `project_root.py` get_containment_roots |
| A-3 | **Leading-whitespace trusted-root entry mishandled.** The blank-entry filter tests `str(entry).strip()` truthiness but does not strip the value used, so `" /abs"` fails `is_absolute()` and is treated as cwd-relative. | SR-002 | Strip the entry itself before use (sibling of the AC-11 fix). | `project_root.py` _load_trusted_roots |
| A-4 | **Stale `parser.py` docstring.** `_add_root_argument` docstring says defaults include "OS temp/scratchpad directories" — the removed behavior; contradicts the correct `--help` text below it. | eng-reviewer F-1, CC-006, S-012 minor | Correct the docstring to the Option C model. | `parser.py:578-580` |
| A-5 | **Dead code.** `_get_repo_root()` has no callers outside its own test. | SR-005 | Remove function + its test. | `ast_commands.py` |
| A-6 | **Rejection error lacks remediation hint** (optional). | FM-007 | Add "configure ast.trusted_roots or pass --root" to the escape message. | `ast_commands.py` |

Read-path race (IN-003) is **not** a defect: `_read_file` already reuses the validated `resolved` path (check=use). No action.

---

## Disposition B — Governance / Traceability Fixes

| ID | Finding | Corroboration | Fix |
|----|---------|---------------|-----|
| B-1 | GitHub issue **#337 is stale** (H-32 parity): still describes the original narrow bug + a never-built env var; no mention of Option C, `ast.trusted_roots`, or the closed Criticals. | CC-001 | Add a comment to #337 summarizing the Option C redesign and current state. |
| B-2 | **BUG-010 worktracker ACs** still certify the deleted ownership gate and the always-widen design; no History entry for the Option C pivot. | CC-003 | Reconcile ACs with Option C; add a History entry (WTI truthfulness). |
| B-3 | **`RESUME-HERE.md`** still frames "Option A vs B pending"; Option C (the path taken) is unmentioned. | CC-005 | Update to reflect Option C + tournament outcome. |
| B-4 | **DD-1..DD-4 owner sign-offs not recorded** in the artifacts. | SR-004, CC-004 | Add a decision record capturing the approvals (DD-2 = Option A, AC-10 = warn-and-honor) with dates. |
| B-5 | **Threat-model not written down** — the "trust = explicit declaration" model and what containment does/doesn't protect against (esp. agent-can-edit-config) is only implicit. | DA-001, DA-002 (actionable core) | Add an explicit threat-model / trust-boundary statement to the plan or a SECURITY note. |

---

## Disposition C — Owner Decisions

| ID | Decision | Options |
|----|----------|---------|
| C-1 | **Scratchpad provisioning (PM-001 / FM-006 / IN-001).** Option C removed temp auto-trust; nothing provisions a replacement, so an agent running `jerry ast` on a scratchpad file breaks post-merge. | (A) Provision it — a companion hook/settings sets `JERRY_AST__TRUSTED_ROOTS` to the per-session scratchpad (per-session, uid-namespaced → not the shared-temp risk IN-001 warns of). (B) De-scope — require explicit `--root`/config for scratchpad use; update BUG-010 ACs to state project-root + explicit trust as the design. |
| C-2 | **H-07(c) architecture exception (CC-002).** `build_layered_config_adapter()` instantiates an infrastructure adapter from the interface layer, outside `bootstrap.py`. Pre-existing (config CLI already did it; DD-4 consolidated two sites to one); automated gate passes; disclosed. | (A) File a brief ADR exception documenting the accepted pattern. (B) Refactor to route config-adapter creation through the composition root. |

---

## Disposition D — Deferred / Tracked

| Finding | Status |
|---------|--------|
| `Error:` prints to stdout (SR-003, F-3, IN-002-adjacent) | **Fixed in this unit** (GH #371) — all `jerry ast` diagnostics routed to stderr; stdout stays clean JSON |
| `config set --scope local` no-op (PM-005) | GitHub #370 |
| Windows subprocess tests excluded from CI; symlink tests not skipif-guarded (PM-002, PM-003, IN-005, FM-004) | **Testing gap — recommend: add a Windows-runnable containment assertion or file a follow-up issue** |
| comma-in-path CSV split (AC-9, FM-006 minor) | Documented (help text) |

---

## Disposition E — Already Settled / Overstated

| Finding | Why no action |
|---------|---------------|
| DA-001/002, DA-003/004/005 (agent can widen own trust; ownership-gate persistence; warn-vs-reject; layer ratchet) | Re-litigate owner-settled decisions (best-effort trust model; DD-2 = remove; AC-10 = warn-and-honor). Actionable residue captured as B-5 (document the model). |
| IN-002 (`--quiet` unused in Jerry's own docs) | C6 stdout-purity holds regardless (notes are stderr-only); at most a docs improvement. |
| IN-004 (pip-package project-root fragility), DA-005 (layer ratchet) | Future enhancement, out of scope for BUG-010. |
| RT-004 (`ast_modify` reads config twice per call — widens the race window) | No action. The A-1 fix made the write reuse the exact resolved path the write-time check validated, so the write no longer depends on a second independent resolution; the remaining double config read is a micro-optimization, not a security defect. |
| RT-005 (`--quiet` suppresses the R-3/R-4 transparency notes it also relies on for visibility) | Accepted tradeoff (owner decision DD-3 / C6). `--quiet` is opt-in; the default is warnings-on. A caller that suppresses its own visibility has made that choice deliberately. |

---

## Corroboration Map

- **Write-path TOCTOU (A-1):** SR-001, RT-001, RT-003, S-011, FM-001 — **5 independent strategies.**
- **Broad project root (A-2):** RT-002, FM-005.
- **Stale docstring (A-4):** eng-reviewer F-1, CC-006, FM minor.
- **Scratchpad break (C-1):** PM-001, FM-006, IN-001.
- **Governance drift (B-1..B-4):** S-007 cluster, corroborated by SR-004.
- **Six prior Criticals dissolved:** independently re-confirmed by eng-reviewer, S-011, S-004 (retractions), red-vuln pass 2.

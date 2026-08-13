# BUG-010 (jerry ast containment) — Resume Pointer

> Read this first after a session break. Updated 2026-08-12.

## Where this stands

- **GitHub issue:** [#337](https://github.com/geekatron/jerry/issues/337) — `jerry ast` rejected files outside the plugin install tree. Comment added bringing it in sync with the Option C redesign.
- **Branch / PR:** `fix/BUG-010-ast-project-root` — open PR [#341](https://github.com/geekatron/jerry/pull/341).
- **Design shipped:** **Option C — user-declared trusted roots.** Default containment = the user's project root **plus** explicitly-configured `ast.trusted_roots` entries. No automatic temp/scratchpad trust. `--root` = exclusive override; `--quiet` suppresses stderr notes; config-input hygiene (blank filter, `JERRY_PROJECT` `..` fail-closed, relative warn-and-honor). The old always-widen + temp-ownership-gate approach was removed after a C4 tournament scored it 0.64.

## Commits on the branch

| Commit | What |
|--------|------|
| `62b429e8` | Base fix: anchor containment to the user's project root (`CLAUDE_PROJECT_DIR`/cwd). |
| `da34a8b8` | Option C implementation (config-declared trust; temp auto-trust + ownership gate removed; `--quiet`). |
| `cce557c5` | Config-input hygiene fixes (AC-11 blank entry, AC-18 `JERRY_PROJECT` traversal, AC-10 relative warn-and-honor). |
| `a6240a4d` | Tournament fixes A-1..A-7 (write-path TOCTOU + small items), governance reconciliation, and the full tournament record. |
| `e00ed1c4` | Final S-014-gate polish: CHANGELOG Option C entry, this file's refresh, and the write-time error hint. |
| `18ce85de` | Worktracker audit + tidy; GH #371 (`Error:`->stderr) folded in (`ast_commands.py`); end-to-end re-verified. |
| `888c94a8` | Completed the #371 sweep (`main.py` router prints -> stderr); reconciled #371 status across all docs. |

## Verification done

- Red-team re-check (21 attack cases): six prior Criticals dissolved with proof-of-concepts; 3 config-hygiene findings fixed and independently re-verified against the real CLI.
- eng-reviewer gate: **PASS, S-014 0.955**.
- Full C4 blind tournament (10 strategies): consolidated in `adv-tournament-consolidated-optionc.md`. One real code defect (write-path TOCTOU, 5-strategy corroborated) — now fixed — plus small items, now fixed.

## Owner decisions (settled)

- Remove the temp-root ownership gate entirely (trust is explicit user declaration; cross-platform-consistent).
- Relative `ast.trusted_roots` entries: **warn-and-honor** (not reject).
- Scratchpad access: **explicit config** (`ast.trusted_roots` / `--root`), not auto-provisioned. Turnkey provisioning → [#372](https://github.com/geekatron/jerry/issues/372).
- Config-adapter composition-root cleanup: optional purist nit, **not a real violation** (the CLI layer is allowed to use adapters; the automated architecture gate passes). Tracked → [#373](https://github.com/geekatron/jerry/issues/373).
- **Fixed in this unit:** `Error:`→stdout routing (GH #371) — all `jerry ast` diagnostics now print to stderr; stdout carries only the JSON/render payload. Closes on merge.
- Deferred (future work): session-local config-layer gap ([#370](https://github.com/geekatron/jerry/issues/370)); turnkey scratchpad provisioning ([#372](https://github.com/geekatron/jerry/issues/372)); config-adapter composition-root cleanup ([#373](https://github.com/geekatron/jerry/issues/373)).

## Next actions

1. Done — tournament fixes + governance at `a6240a4d`; S-014 gap fixes at `e00ed1c4`.
2. Done — end-to-end verified via a real `.jerry/config.toml` + the live `jerry` CLI; GH #371 (`Error:`->stdout) folded in and fixed across the whole `jerry ast` path; worktracker audit (`wt-audit-optionc.md`) + tidy applied. Formal S-014 re-score against the final commit `888c94a8`: **PASS 0.9335** (`adv-s014-final-score-888c94a8.md`; per-dimension all >= 0.91).
3. **Ready to merge** — PR #341 review + merge. Use `Closes #337` and `Closes #371` trailers so both auto-close on merge to main.

## Artifacts (this folder)

`eng-lead-option-c-plan.md`, `red-lead-option-c-attack-plan.md`, `red-vuln-option-c-findings.md`, `eng-reviewer-optionc-gate-report.md`, `adv-s0{01,02,03,04,07,10,11,12,13}-*-optionc.md`, `adv-tournament-consolidated-optionc.md`, `DECISIONS-and-threat-model.md`, `BUG-010-ast-project-root.md` (the entity).

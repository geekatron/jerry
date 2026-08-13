# BUG-010 Option C — Owner Decisions & Threat Model

> Records the owner-approved decisions behind the Option C `jerry ast` containment redesign (closing the "sign-offs not recorded" finding) and states the threat model the design assumes (closing the "threat model never written down" finding). Branch `fix/BUG-010-ast-project-root`, PR #341.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Owner Decisions](#owner-decisions) | What was decided, when, and why |
| [Threat Model](#threat-model) | What the containment control protects against — and what it does not |
| [Deterministic Controls](#deterministic-controls) | The cross-platform protections the design actually relies on |

---

## Owner Decisions

All approved by the repository owner during the BUG-010 review (2026-08-10 → 2026-08-12).

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| DD-2 | Temp-root file-ownership gate | **Remove entirely** | The gate existed only to make auto-trusted shared OS temp "safe." Option C never auto-trusts temp, so the gate's premise is gone. It was POSIX-only (no Windows equivalent without a new dependency), it failed open on error, and it was defeated by same-uid/root — so it added defeatable, cross-platform-inconsistent depth on top of what the OS already enforces. |
| AC-10 | Relative `ast.trusted_roots` entries | **Warn-and-honor** (not reject) | Consistent with `--root`'s existing "user discretion" model; the entry is still honored, but a stderr warning names the resolved path so the effective trust is never silent. |
| DD-1 | Broad-root warning scope | **Extend to configured roots** (and, post-tournament, the project root) | A broad declared root is the same trust posture as a broad `--root`; explicit trust deserves visibility. |
| Scratchpad | Claude Code scratchpad access | **De-scope to explicit config** | Running `jerry ast` on a scratchpad file now requires an `ast.trusted_roots` entry or `--root`. Consistent with Option C's "explicit trust, no auto-magic" thesis. Optional turnkey provisioning tracked in #372. |
| Config adapter | Composition-root placement | **Keep as-is + note** | The CLI (interface) layer is allowed to use/construct adapters; the automated architecture gate passes and the existing `jerry config` command already does this. Optional purist cleanup tracked in #373 — not a real violation. |
| Folded in | `Error:`→stdout (#371) | **Fixed in this unit** | Demonstrated during end-to-end testing; all `jerry ast` diagnostic/error messages routed to stderr so stdout carries only the JSON/render payload. Closes on merge. |
| Deferred | session-local config layer (#370) | **Out of scope** | Pre-existing, broader than this security bug; tracked separately. |

---

## Threat Model

**What `jerry ast` path containment IS:** a best-effort guardrail that (1) prevents *accidental* operation outside the user's project — a mistyped path, an unexpected symlink target — and (2) makes any out-of-project operation **explicit and visible** (it must be declared, and it emits a stderr note).

**What it is NOT:** a hard security boundary against a party that has already been granted broad file access. Per the owner: *"We can only do our reasonable best effort to protect the user."*

**Trust model:** trust equals **explicit declaration** —
- the project root (trusted by construction — it is the user's own repository, via `CLAUDE_PROJECT_DIR` or cwd),
- any directory the user lists in `ast.trusted_roots`,
- a directory passed as `--root` for one invocation.

**Explicitly accepted residual (raised by the adversarial review):** in Jerry's own setting, the party invoking `jerry ast` is often an AI agent that also has a Write tool. Such an agent can add its own `ast.trusted_roots` entry (or set the env var) and widen its own containment. This is **accepted, not overlooked**: an agent with write access to the project already has broad file access through other tools, so `jerry ast` containment is not — and is not intended to be — the boundary that constrains it. The control's value is against *accident* and for *visibility*, not against an actor who has already been granted write access.

---

## Deterministic Controls

These are the protections the design actually relies on — all cross-platform, all enforced the same way on macOS, Linux, and Windows:

- **Project-root anchoring** — containment resolves to the user's project, never the Jerry install tree.
- **Symlink realpath re-resolution on read *and* write** — the `ast_modify` write targets the exact resolved path the write-time check validated (closes the check-vs-use TOCTOU, CWE-367).
- **Broad-root warnings** — a filesystem/drive root, `$HOME`, or an ancestor of `$HOME` (project, configured, or `--root`) emits a stderr warning.
- **Out-of-project transparency note** — a match via a configured (non-project) root emits a one-line stderr note; stdout stays clean JSON.
- **Fail-closed config traversal** — a `JERRY_PROJECT` value escaping the `projects/` tree drops that config layer rather than reading an outside file.
- **Input hygiene** — blank/whitespace `ast.trusted_roots` entries are dropped before resolution (an empty entry would otherwise resolve to the current directory).

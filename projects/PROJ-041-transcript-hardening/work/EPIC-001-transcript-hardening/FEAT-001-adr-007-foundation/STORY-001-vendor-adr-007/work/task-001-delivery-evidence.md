# TASK-001 Delivery Evidence — Vendor ADR-007 from jerry-core

> Internal audit evidence. Records byte-identical vendoring of ADR-007 from the jerry-core repository into PROJ-041-transcript-hardening for ADR-007 public-release foundation work.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Source Provenance](#source-provenance) | Source repo, branch, commit, path |
| [Destination](#destination) | Repo-relative path of vendored file |
| [Hash Verification](#hash-verification) | sha256 source vs destination |
| [Frontmatter Check](#frontmatter-check) | Type/Status/Title/Date observed |
| [Acceptance Criteria](#acceptance-criteria) | TASK-001 AC pass/fail |

---

## Source Provenance

| Field | Value |
|-------|-------|
| Source repo | `<jerry-core>` (separate repository, branch `main`) |
| Source branch | `main` |
| Source commit SHA (full) | `9d8f325f7a91bcf20cdfe176da660598ed5c0c2f` |
| Source path | `<jerry-core>/projects/<source-project>/work/<source-epic>/<source-feature>/docs/decisions/ADR-007-output-template-specification.md` |
| Source file size | 33 KB |
| Captured at | 2026-04-30 |

> **Note on path obfuscation:** The literal absolute path on the implementer's machine and the literal source-project identifier are intentionally replaced with placeholders (`<jerry-core>`, `<source-project>`, `<source-epic>`, `<source-feature>`) per architecture-validation policy. PROJ-041 forbids absolute developer-machine paths and references to the upstream source-project identifier inside any file under this project tree. The full provenance is reproducible via the recorded commit SHA.

---

## Destination

| Field | Value |
|-------|-------|
| Destination path (repo-relative) | `docs/adrs/ADR-007-output-template-specification.md` |
| Created via | `cp` (byte-identical copy; no Read/Write transformation) |

---

## Hash Verification

| Artifact | sha256 |
|----------|--------|
| Source | `1518a2daa2bde343552b4435480bf1c34d0cbd5bf5cb713564e0a0fe56cd6993` |
| Destination | `1518a2daa2bde343552b4435480bf1c34d0cbd5bf5cb713564e0a0fe56cd6993` |
| Match verdict | **PASS** (byte-identical) |
| Line count (destination) | 1044 |

Hash tool: `shasum -a 256` (macOS, equivalent to GNU `sha256sum`).

---

## Frontmatter Check

The vendored file uses Jerry's blockquote-frontmatter convention (no YAML block; metadata after the H1 in a blockquote). Fields observed in the head of the destination file:

| Field | Value |
|-------|-------|
| Title (H1) | `# ADR-007: Output Template Specification` |
| Type | Architectural Decision Record (ADR) — by document title and structure |
| PS | `FEAT-006-phase-3` |
| Exploration | `e-004` |
| Created | `2026-01-31` |
| Status | `PROPOSED` |
| Agent | `ps-architect v2.0.0` |
| Supersedes | `N/A` |
| Superseded By | `N/A` |

> **Status note:** Status remains `PROPOSED` as vendored. Promotion to `ACCEPTED` is the explicit scope of STORY-002 and is intentionally NOT performed here. Frontmatter is byte-identical to source per hash match above.

---

## Acceptance Criteria

TASK-001 AC verification:

| # | Criterion | Verdict |
|---|-----------|---------|
| 1 | `docs/adrs/ADR-007-output-template-specification.md` exists in this branch | **PASS** |
| 2 | `sha256sum` of vendored file matches `sha256sum` of jerry-core source at recorded commit | **PASS** (`1518a2da...cd6993`) |
| 3 | Source commit SHA recorded | **PASS** (`9d8f325f7a91bcf20cdfe176da660598ed5c0c2f`) |
| 4 | ADR-007 frontmatter byte-identical to source | **PASS** (implied by full-file hash match) |
| 5 | No content mutation during vendoring | **PASS** (`cp` used; no Read+Write) |

**Overall TASK-001 AC: PASS**

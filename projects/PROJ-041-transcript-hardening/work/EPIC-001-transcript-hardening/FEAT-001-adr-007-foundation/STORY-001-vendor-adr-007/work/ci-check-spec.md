# CI Check Specification: SKILL.md ADR Cross-Reference Integrity

> **Purpose:** Authoritative specification for the CI check that asserts every `docs/adrs/ADR-NNN*.md`
> reference in any `skills/*/SKILL.md` resolves to a real file in the repository.
> This spec is input to TASK-008 (eng-devsecops implementation).
>
> **Agent:** eng-lead (STORY-001 step 3)
> **Date:** 2026-04-30
> **Status:** READY FOR IMPLEMENTATION

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Goal](#goal) | What the check asserts and why |
| [Detection Algorithm](#detection-algorithm) | Step-by-step regex match and resolution rule |
| [Failure Mode](#failure-mode) | Exit code, error message format, reporting location |
| [Test Fixture](#test-fixture) | Hypothetical broken SKILL.md the check must flag |
| [CI Integration Point](#ci-integration-point) | Pre-commit hook vs GitHub Actions — recommendation with rationale |
| [Performance Bound](#performance-bound) | Complexity and maximum acceptable runtime |
| [Implementation Notes](#implementation-notes) | Language, path handling, edge cases |

---

## Goal

Assert that every Markdown link in any `skills/*/SKILL.md` file that references a path matching
`docs/adrs/ADR-NNN*.md` (where NNN is one or more digits) resolves to a file that **actually
exists** in the repository at that path.

**Motivation:** When an ADR is vendored into `docs/adrs/`, consuming `SKILL.md` files must be
updated to use the new path. This check catches future regressions where a SKILL.md is authored
or updated with a stale/incorrect ADR path — silently broken links degrade developer trust and
make the skill unusable for consumers who follow cross-references.

**Scope boundary:**
- IN: `skills/*/SKILL.md` files only (not agent `.md` files, playbooks, or composition prompts).
- IN: References to `docs/adrs/ADR-NNN*.md` specifically.
- OUT: References to other `docs/` paths, `projects/` paths, or non-ADR cross-references.
- OUT: Verification that the ADR content is semantically correct.

---

## Detection Algorithm

The check MUST execute the following steps in order.

### Step 1: Discover SKILL.md files

Glob for all files matching the pattern:

```
skills/*/SKILL.md
```

Do NOT recurse into nested subdirectories (e.g., `skills/transcript/agents/` does not contain a
`SKILL.md`). A single-level glob `skills/*/SKILL.md` is sufficient and avoids false positives.

### Step 2: Extract ADR cross-references

For each discovered `SKILL.md`, extract all Markdown link targets matching the following regular
expression (applied line-by-line):

```
\]\(([^)]*docs/adrs/ADR-\d+[^)]*\.md)\)
```

Breakdown:
- `\]\(` — closing bracket + opening paren of a Markdown link
- `([^)]*docs/adrs/ADR-\d+[^)]*\.md)` — capture group: any path fragment containing `docs/adrs/ADR-` followed by one or more digits, followed by any suffix, ending in `.md`
- `\)` — closing paren

Capture group 1 is the raw path string as written in the file.

**Anchor fragments:** Strip any `#anchor` suffix before path resolution. The fragment is not part
of the filesystem path.

Example extraction:
```
Input line:  See [ADR-007](../../docs/adrs/ADR-007-output-template-specification.md) for details.
Extracted:   ../../docs/adrs/ADR-007-output-template-specification.md
```

### Step 3: Resolve each path to repo-root-relative

Each extracted path may be relative (e.g., `../../docs/adrs/ADR-007-output-template-specification.md`)
or already repo-root-relative (e.g., `docs/adrs/ADR-007-output-template-specification.md`).

Resolution rule:

1. Let `skill_dir` = the directory containing the `SKILL.md` file (e.g., `skills/transcript/`).
2. If the extracted path starts with `./` or `../`, resolve it relative to `skill_dir` using
   standard filesystem path normalization (e.g., Python `os.path.normpath(os.path.join(skill_dir, path))`).
3. If the extracted path does NOT start with `./` or `../`, treat it as already repo-root-relative
   (no further normalization needed).
4. The resulting resolved path is relative to the repository root.

### Step 4: Existence check

For each resolved path, check whether the file exists under the repository root:

```python
os.path.isfile(os.path.join(repo_root, resolved_path))
```

Where `repo_root` is the directory obtained by running `git rev-parse --show-toplevel` (or
equivalent) at the start of the script.

### Step 5: Collect violations

A violation is any (skill_file, source_line_number, raw_path, resolved_path) tuple where the
existence check returns False.

If violations list is empty: exit code 0 (PASS).
If violations list is non-empty: exit code 1 (FAIL) — see Failure Mode.

---

## Failure Mode

### Exit Code

| Result | Exit Code |
|--------|-----------|
| All references resolve | 0 |
| One or more broken references | 1 |

### Error Message Format

Each violation MUST be reported on its own line using the following format:

```
BROKEN ADR REF: {skill_file}:{line_number}: '{raw_path}' -> resolved '{resolved_path}' does not exist
```

Example:

```
BROKEN ADR REF: skills/transcript/SKILL.md:1546: '../../docs/adrs/ADR-007-output-template-specification.md' -> resolved 'docs/adrs/ADR-007-output-template-specification.md' does not exist
```

After reporting all violations, print a summary line:

```
ADR cross-reference check: {N} broken reference(s) found in {M} SKILL.md file(s). Fix the paths or vendor the missing ADR files.
```

### Reporting Location

- Pre-commit hook: stderr of the hook process (captured by pre-commit framework and displayed to the developer on commit attempt).
- GitHub Actions step: stdout of the step (captured in the Actions run log and surfaced as a failed step annotation).

---

## Test Fixture

The following hypothetical `SKILL.md` fragment MUST cause the check to produce exactly one
violation and exit code 1. It SHOULD be used as a unit test for the check implementation.

**File:** `skills/fake-skill/SKILL.md` (for testing only — not created in production)

```markdown
---
name: fake-skill
description: A fake skill for CI check testing.
---

# Fake Skill

## References

- [ADR-007](../../docs/adrs/ADR-007-DOES-NOT-EXIST.md) - A broken ADR reference
- [ADR-007](../../docs/adrs/ADR-007-output-template-specification.md) - A valid ADR reference
```

**Expected output:**

```
BROKEN ADR REF: skills/fake-skill/SKILL.md:12: '../../docs/adrs/ADR-007-DOES-NOT-EXIST.md' -> resolved 'docs/adrs/ADR-007-DOES-NOT-EXIST.md' does not exist
ADR cross-reference check: 1 broken reference(s) found in 1 SKILL.md file(s). Fix the paths or vendor the missing ADR files.
```

**Expected exit code:** 1

The second reference (`ADR-007-output-template-specification.md`) MUST NOT appear in the output
because the file exists in the repository.

---

## CI Integration Point

### Recommendation: Both pre-commit hook AND GitHub Actions step

**Rationale:** Defense in depth — the pre-commit hook catches breakage locally before a commit is
made; the GitHub Actions step provides the authoritative gate that cannot be bypassed by skipping
the pre-commit hook.

### Pre-commit Hook

Add as a `local` hook in `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: skill-adr-refs
      name: SKILL.md ADR cross-reference integrity
      language: python
      entry: uv run python scripts/ci/check_skill_adr_refs.py
      files: ^skills/[^/]+/SKILL\.md$
      pass_filenames: false
      always_run: false
```

- `pass_filenames: false` — the script discovers SKILL.md files itself (glob-based).
- `always_run: false` — only runs when a `skills/*/SKILL.md` file is in the commit.
- `files` pattern ensures the hook only fires when SKILL.md files are staged.

### GitHub Actions Step

Add as a step in the existing PR workflow (or create a new `skill-integrity.yml` workflow):

```yaml
- name: Check SKILL.md ADR cross-references
  run: uv run python scripts/ci/check_skill_adr_refs.py
```

This step MUST run before any merge-blocking quality gates and MUST fail the PR if exit code is 1.

### Script Location

```
scripts/ci/check_skill_adr_refs.py
```

This path is conventional for Jerry framework CI scripts. The script MUST:
1. Accept zero arguments (self-discovering via `git rev-parse --show-toplevel`).
2. Be executable with `uv run python` per H-05.
3. Require no dependencies beyond the Python standard library (`os`, `re`, `pathlib`, `subprocess`).

---

## Performance Bound

The check MUST run in **O(N)** time where N = total number of ADR cross-references found across
all `skills/*/SKILL.md` files.

This is achievable because:
- File glob is O(S) where S = number of skills (bounded, small).
- Line scan per file is O(L) where L = lines in the file.
- Path resolution and existence check are O(1) per reference (filesystem stat call).
- No repeated work: each reference is resolved and checked exactly once.

**Maximum acceptable wall-clock time:** 5 seconds for any repository with fewer than 50 skills
and fewer than 1,000 total ADR references. This bound is generous — expected runtime on the
current repository (fewer than 15 skills, fewer than 100 ADR references) is under 500ms.

If the check exceeds 5 seconds, it indicates a regression (e.g., recursive glob, repeated file
reads, or network calls) and MUST be investigated and fixed before merging.

---

## Implementation Notes

1. **Python version:** Any Python 3.9+ (compatible with the Jerry framework UV environment).
2. **No external dependencies:** Use only stdlib (`os`, `re`, `pathlib`, `subprocess`). This avoids
   dependency conflicts and keeps the check lightweight.
3. **Symlinks:** `os.path.isfile` follows symlinks. If `docs/adrs/` contains symlinks to ADR files
   elsewhere in the repo, the check will correctly report them as existing. This is the desired
   behavior.
4. **Windows path separator:** If cross-platform support is needed, normalize path separators when
   comparing. Use `pathlib.Path` for path joining and normalization rather than string concatenation.
5. **Case sensitivity:** On macOS (default HFS+ case-insensitive) the existence check may return
   True for incorrect casing. The check SHOULD use case-sensitive comparison on Linux CI hosts
   (GitHub Actions Ubuntu runners). No special handling needed — the CI host governs.
6. **Commented-out references:** References inside fenced code blocks or HTML comments are still
   matched by the regex. This is intentional — if a commented reference is wrong, it should be
   fixed or removed. Implementers MAY add a `--strict` flag to skip code-block content in a future
   iteration; it is not required for TASK-008.

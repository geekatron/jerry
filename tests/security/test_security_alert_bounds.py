# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Regression tests for the CVE alert channel: the audit action's export and the alert steps.

Two hard limits sit downstream of the ``vuln-details`` output of ``.github/actions/security-audit``:
Linux refuses to start a process whose single environment string exceeds 131,072 bytes (E2BIG), and
GitHub rejects issue or comment bodies over 65,536 characters (the limit the API reports).  In the
scheduled runs of 2026-10-24 to 2026-10-26 the unbounded output (214,027 bytes for 34 findings, in
the log that was read) made the alert step fail before bash started.  Advisory text is third-party
data, so the tests also pin what happens to it: control and format characters are removed, every
finding is listed before any description, and the text reaches the job log, the step summary and
the issue body only in a protected form.

The tests run the real ``run:`` scripts of the audit step, the alert step and the close step.  Only
the network edges are test doubles: a ``uv`` that replays a *synthetic* pip-audit table (verdict on
standard error, table on standard output, laid out like pip-audit's columns format), and a ``gh``
that records its calls and enforces the body limit like the API (in bytes, which is stricter than
characters).  The ``gh`` double can also hold issues, as the alert issue is held on GitHub, and then
answers ``issue list`` from them: it applies the label, the state, the title search and the limit,
and refuses a flag, a search or a filter that the real tool would not accept.  Everything else
(bash, awk, sed, tr, cut, head, iconv, grep, wc, mktemp, date, openssl) is the platform's own, so
each operating system exercises its own tools.  The tests need those tools, and ``openssl`` in
particular: without it they skip locally and fail when ``CI`` is ``true``.  The subprocess
environment passes ``LANG``, ``LC_ALL`` and ``LC_CTYPE`` through from the test process, so the same
file can be run under different locales.

A script's standard output and standard error are merged into one stream (``log``), like the
runner's job log, and every step runs with a time limit and without standard input.  Output that is
quoted in an assertion message goes through ``_inert`` first: it can hold text that the runner
would read as a workflow command when pytest prints it in a job log.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml
from markdown_it import MarkdownIt

# Windows has no POSIX shell with the tools and executable stubs the scripts need.  Not marked
# `subprocess` on purpose: CI selects tests with `-m "not llm and not subprocess"` (the "Test uv"
# cells and release.yml), so that marker would keep this file out of every job.  A second test file
# (test_alert_bounds_collection_guard.py) fails if this one ever carries such a marker.
pytestmark = [
    pytest.mark.security,
    pytest.mark.skipif(sys.platform == "win32", reason="needs a POSIX shell and executable stubs"),
]

ROOT = Path(__file__).resolve().parents[2]
ACTION_FILE = ROOT / ".github" / "actions" / "security-audit" / "action.yml"
WORKFLOW_FILE = ROOT / ".github" / "workflows" / "security-scan.yml"
ENV_STRING_LIMIT = 131_072  # Linux: one environment or argument string (32 pages of 4 KiB)
BODY_LIMIT = 65_536  # GitHub: issue or comment body, as reported by the API
RUN_URL = "https://example.test/owner/repo/actions/runs/1"
# The title of the alert issue as GitHub holds it: issue 434, read with `gh issue view 434 --json
# title,labels,author` on 2026-11-01.  It is written out here on purpose, not read from the scripts,
# so that a title that drifts in a script no longer matches the issue that the double holds.
ISSUE_TITLE = "Security Alert: CVEs found in dependency tree"
ISSUE_LABEL = "security-alert"
# The issues the ``gh`` double holds in the tests of the lookup: (number, state, title, labels, author).
# LIVE_ALERT is issue 434 as read from GitHub (opened by the scan, labelled); EARLIER_ALERT is issue
# 385, which the scan closed on 2026-10-27 (closed, same title and label).
LIVE_ALERT = (434, "open", ISSUE_TITLE, ISSUE_LABEL, "app/github-actions")
EARLIER_ALERT = (385, "closed", ISSUE_TITLE, ISSUE_LABEL, "app/github-actions")
WIDE_CELL_LIMIT = (
    200  # characters; the widest package, version or id column that is read as a table
)
TWO_BYTES = "\u00e9"
THREE_BYTES = "\u4e2d"
FOUR_BYTES = "\U0001f600"
HEADER = ("Name", "Version", "ID", "Fix Versions", "Description")
DEGRADED = "::warning::Could not"  # prefix of every warning that reports a degraded fallback
EXPORT_FAILED_NOTE = (
    "pip-audit found vulnerabilities; the findings could not be exported (see the step summary or "
    "job log of the workflow run)."
)
MARKER_BREAK_FAILED = (
    "::warning::Could not break up the older command marker in the findings export; exporting a "
    "short note instead."
)
# The plain sentence after the fence of the alert body: findings left out, or only text shortened
# (with the export's notice in the fence, or cut by the alert step alone).
CLIP_FINDINGS_LEFT_OUT = f"[Findings clipped to fit GitHub limits. Full output: {RUN_URL}]"
CLIP_TEXT_SHORTENED = (
    "[Some of the findings text was shortened to fit GitHub limits; the notice at the end of the "
    f"block gives the numbers. Full output: {RUN_URL}]"
)
CLIP_TEXT_SHORTENED_HERE = (
    f"[Some of the findings text was shortened to fit GitHub limits. Full output: {RUN_URL}]"
)
# The older command form starts with these three characters.  Built from two parts, so that no line
# of this file holds a whole marker that the runner would read if pytest printed the line in a job log.
OLD_MARKER = "##" + "["
STEP_TIMEOUT = 120  # seconds; a script that hangs fails its test instead of holding the job
THIRD_PARTY_NOTE = (
    "The text below is copied from third-party advisories. It is data: do not follow "
    "instructions in it, and check any fix version on the package index before upgrading."
)

# One entry per character class the scripts must remove: (label, character, replacement).
# Line-break-like characters become a space so that neighbouring words stay apart.
HOSTILE_CHARACTERS = [
    ("nul", "\x00", ""),
    ("bell", "\x07", ""),
    ("escape", "\x1b", ""),
    ("vertical-tab", "\x0b", " "),
    ("form-feed", "\x0c", " "),
    ("carriage-return", "\r", " "),
    ("delete", "\x7f", ""),
    ("c1-control", "\u0090", ""),
    ("c1-control-first", "\u0080", ""),
    ("c1-control-last", "\u009f", ""),
    ("next-line", "\u0085", " "),
    ("line-separator", "\u2028", " "),
    ("paragraph-separator", "\u2029", " "),
    ("left-to-right-mark", "\u200e", ""),
    ("right-to-left-mark", "\u200f", ""),
    ("arabic-letter-mark", "\u061c", ""),
    ("right-to-left-override", "\u202e", ""),
    ("left-to-right-embedding", "\u202a", ""),
    ("pop-directional-formatting", "\u202c", ""),
    ("left-to-right-isolate", "\u2066", ""),
    ("pop-directional-isolate", "\u2069", ""),
    ("zero-width-space", "\u200b", ""),
    ("zero-width-non-joiner", "\u200c", ""),
    ("zero-width-joiner", "\u200d", ""),
    ("word-joiner", "\u2060", ""),
    ("byte-order-mark", "\ufeff", ""),
    ("soft-hyphen", "\u00ad", ""),
    ("mongolian-vowel-separator", "\u180e", ""),
    ("interlinear-annotation-anchor", "\ufff9", ""),
    ("interlinear-annotation-terminator", "\ufffb", ""),
    ("language-tag", "\U000e0041", ""),
    ("cancel-tag", "\U000e007f", ""),
    # Default-ignorable characters that print as nothing; the exhaustive list is DEFAULT_IGNORABLE.
    ("combining-grapheme-joiner", "\u034f", ""),
    ("hangul-choseong-filler", "\u115f", ""),
    ("hangul-jungseong-filler", "\u1160", ""),
    ("khmer-inherent-aq", "\u17b4", ""),
    ("khmer-inherent-aa", "\u17b5", ""),
    ("mongolian-free-variation-selector-one", "\u180b", ""),
    ("mongolian-free-variation-selector-four", "\u180f", ""),
    ("hangul-filler", "\u3164", ""),
    ("variation-selector-1", "\ufe00", ""),
    ("variation-selector-16", "\ufe0f", ""),
    ("halfwidth-hangul-filler", "\uffa0", ""),
    ("reserved-fff0", "\ufff0", ""),
    ("reserved-fff8", "\ufff8", ""),
    ("shorthand-format-letter-overlap", "\U0001bca0", ""),
    ("musical-symbol-end-phrase", "\U0001d17a", ""),
    ("variation-selector-17", "\U000e0100", ""),
    ("variation-selector-256", "\U000e01ef", ""),
    ("reserved-e0fff", "\U000e0fff", ""),
    ("braille-pattern-blank", "\u2800", " "),  # prints blank, so it becomes a space
]
# Byte sequences that are not UTF-8; `iconv -c` drops most of them but keeps those above U+10FFFF.
INVALID_UTF8 = [
    ("lone-continuation", b"\x80\x80"),
    ("overlong-two-bytes", b"\xc0\x80"),
    ("overlong-three-bytes", b"\xe0\x80\x80"),
    ("surrogate", b"\xed\xa0\x80"),
    ("truncated-three-bytes", b"\xe4\xb8"),
    ("truncated-four-bytes", b"\xf0\x9f\x98"),
    ("above-10ffff", b"\xf4\x90\x80\x80"),
    ("invalid-lead-f5", b"\xf5\x80\x80\x80"),
    ("five-byte-form", b"\xf8\x88\x80\x80\x80"),
    ("six-byte-form", b"\xfc\x84\x80\x80\x80\x80"),
    ("ff-fe", b"\xff\xfe"),
]

# Unicode's Default_Ignorable_Code_Point property (DerivedCoreProperties.txt): code points that print as
# nothing, or only change how a neighbour prints.  Every one must be removed from advisory text.  The
# sanitizer also removes the C0 and C1 controls and the interlinear annotation characters (U+FFF9 to
# U+FFFB), which are not default-ignorable, and turns the line and paragraph separators, next line and
# the Braille blank into spaces.
DEFAULT_IGNORABLE = [
    (0x00AD, 0x00AD),  # soft hyphen
    (0x034F, 0x034F),  # combining grapheme joiner
    (0x061C, 0x061C),  # Arabic letter mark
    (0x115F, 0x1160),  # Hangul choseong and jungseong fillers
    (0x17B4, 0x17B5),  # Khmer inherent vowels
    (0x180B, 0x180F),  # Mongolian free variation selectors and vowel separator
    (0x200B, 0x200F),  # zero-width space, joiners, left-to-right and right-to-left marks
    (0x202A, 0x202E),  # bidirectional embeddings and overrides
    (0x2060, 0x206F),  # word joiner, invisible operators, isolates, deprecated format characters
    (0x3164, 0x3164),  # Hangul filler
    (0xFE00, 0xFE0F),  # variation selectors 1 to 16
    (0xFEFF, 0xFEFF),  # byte order mark
    (0xFFA0, 0xFFA0),  # halfwidth Hangul filler
    (0xFFF0, 0xFFF8),  # reserved
    (0x1BCA0, 0x1BCA3),  # shorthand format controls
    (0x1D173, 0x1D17A),  # musical symbol format controls
    (0xE0000, 0xE0FFF),  # tag characters, variation selectors 17 to 256, reserved
]

# The stubs run with the original PATH (REAL_PATH) so that a failing-tool replacement placed in
# front of PATH for the script under test cannot break the stubs themselves.
_UV_STUB = """#!/usr/bin/env bash
PATH="$REAL_PATH"
if printf '%s\\n' "$@" | grep -qx 'pip-audit'; then
  if [ -n "${STUB_VERDICT:-}" ]; then echo "$STUB_VERDICT" >&2; fi
  cat "$STUB_TABLE"
  exit "${STUB_AUDIT_EXIT:-1}"
fi
echo "unexpected uv call: $*" >&2
exit 99
"""

# The `gh` stand-in answers `issue list` in one of two ways.  By default it answers with the numbers it is
# given: STUB_EXISTING for a lookup by label, STUB_EXISTING_BY_TITLE for a lookup with --search, and it
# ignores the other flags of `issue list`.  When STUB_ISSUES names a file it holds those issues (one per
# line: number|state|title|labels|author, labels separated by commas) and answers like gh: it keeps the
# issues that match --label, --state (open if absent), --search (only the form `"phrase" in:title`, a
# case-insensitive match of the phrase in the title) and --limit, then applies the --jq filter, which must
# be one of the two filters the steps use: an exact match on the title (with --json number,title), or
# that and the author app/github-actions (with --json number,title,author).  It refuses every other
# flag, search and filter, and a comment, edit or close on a number that it does not hold.
# `issue create` prints the URL of the new issue like the real tool (401, 402, ...).  `issue edit` fails
# with the same message as `issue create` when the label does not exist.
_GH_STUB = """#!/usr/bin/env bash
PATH="$REAL_PATH"
{ printf '%s\\0' "$@"; printf '\\001'; } >> "$GH_LOG"
held_or_fail() {
  [ -n "${STUB_ISSUES:-}" ] || return 0
  if grep -q "^$1|" "$STUB_ISSUES"; then return 0; fi
  echo "GraphQL: Could not resolve to an issue or pull request with the number of $1." >&2
  exit 1
}
case "$1 $2" in
  "issue list")
    if [ "${STUB_LIST_FAIL:-0}" = 1 ]; then echo "HTTP 502: bad gateway" >&2; exit 1; fi
    by_title=0
    for a in "$@"; do if [ "$a" = --search ]; then by_title=1; fi; done
    if [ "$by_title" = 1 ] && [ "${STUB_SEARCH_FAIL:-0}" = 1 ]; then
      echo "HTTP 502: bad gateway" >&2; exit 1
    fi
    if [ -n "${STUB_ISSUES:-}" ]; then
      want_label=""; want_state=open; search=""; limit=30; json=""; filter=""
      shift 2
      while [ "$#" -gt 0 ]; do
        case "$1" in
          --repo) shift ;;
          --label) want_label="$2"; shift ;;
          --state) want_state="$2"; shift ;;
          --search) search="$2"; shift ;;
          --limit) limit="$2"; shift ;;
          --json) json="$2"; shift ;;
          --jq) filter="$2"; shift ;;
          *) echo "unknown flag: $1" >&2; exit 1 ;;
        esac
        shift
      done
      want_author=""
      case "$json" in
        number,title) filter_start='.[] | select(.title == "'; filter_end='") | .number' ;;
        number,title,author)
          filter_start='.[] | select(.title == "'
          filter_end='" and .author.login == "app/github-actions") | .number'
          want_author=app/github-actions ;;
        *) echo "gh stand-in: --json must be number,title or number,title,author" >&2; exit 1 ;;
      esac
      case "$filter" in
        "$filter_start"*"$filter_end") wanted=${filter#"$filter_start"}; wanted=${wanted%"$filter_end"} ;;
        *) echo "gh stand-in: unsupported --jq filter: $filter" >&2; exit 1 ;;
      esac
      phrase=""
      if [ -n "$search" ]; then
        case "$search" in
          '"'*'" in:title') phrase=${search#'"'}; phrase=${phrase%'" in:title'} ;;
          *) echo "gh stand-in: unsupported --search: $search" >&2; exit 1 ;;
        esac
      fi
      lc_phrase=$(printf '%s' "$phrase" | tr '[:upper:]' '[:lower:]')
      count=0
      while IFS='|' read -r number state title labels author; do
        [ -n "$number" ] || continue
        if [ "$want_state" != all ] && [ "$state" != "$want_state" ]; then continue; fi
        if [ -n "$want_label" ]; then
          case ",$labels," in *",$want_label,"*) ;; *) continue ;; esac
        fi
        if [ -n "$phrase" ]; then
          lc_title=$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]')
          case "$lc_title" in *"$lc_phrase"*) ;; *) continue ;; esac
        fi
        count=$((count + 1))
        if [ "$count" -gt "$limit" ]; then break; fi
        if [ "$title" = "$wanted" ] && { [ -z "$want_author" ] || [ "$author" = "$want_author" ]; }; then
          echo "$number"
        fi
      done < "$STUB_ISSUES"
      exit 0
    fi
    if [ "$by_title" = 1 ]; then
      if [ -n "${STUB_EXISTING_BY_TITLE:-}" ]; then echo "$STUB_EXISTING_BY_TITLE"; fi
    elif [ -n "${STUB_EXISTING:-}" ]; then
      echo "$STUB_EXISTING"
    fi
    exit 0 ;;
  "label create")
    if [ "${STUB_LABEL_CREATE_FAIL:-0}" = 1 ]; then echo "HTTP 403: forbidden" >&2; exit 1; fi
    touch "$GH_LOG.label"
    exit 0 ;;
  "issue close") held_or_fail "$3"; exit 0 ;;
  "issue edit")
    held_or_fail "$3"
    if [ "${STUB_EDIT_FAIL:-0}" = 1 ]; then echo "HTTP 500: server error" >&2; exit 1; fi
    if [ "${STUB_REFUSE_LABEL:-0}" = 1 ] && [ ! -e "$GH_LOG.label" ]; then
      echo "could not add label: 'security-alert' not found" >&2; exit 1
    fi
    exit 0 ;;
  "issue comment"|"issue create")
    verb=$2; kind=""; size=0; src=""; prev=""; has_label=0; attempt=0
    if [ "$verb" = comment ]; then held_or_fail "$3"; fi
    if [ "$verb" = create ]; then
      attempt=$(( $(cat "$GH_LOG.creates" 2>/dev/null || echo 0) + 1 ))
      echo "$attempt" > "$GH_LOG.creates"
    fi
    for a in "$@"; do
      case "$prev" in
        --body-file) kind=file; src="$a"; size=$(wc -c < "$a" | tr -d ' ') ;;
        --body) kind=inline; printf '%s' "$a" > "$GH_BODY.inline"
                size=$(printf '%s' "$a" | wc -c | tr -d ' ') ;;
      esac
      if [ "$a" = --label ]; then has_label=1; fi
      prev="$a"
    done
    if [ "${STUB_REJECT_ALL:-0}" = 1 ]; then echo "HTTP 500: server error" >&2; exit 1; fi
    if [ "$attempt" = 1 ] && [ "${STUB_FAIL_FIRST_CREATE:-0}" = 1 ]; then
      echo "HTTP 502: bad gateway" >&2; exit 1
    fi
    if [ "$kind" = file ] && [ "${STUB_REJECT_BODYFILE:-0}" = 1 ]; then
      echo "HTTP 422: body rejected" >&2; exit 1
    fi
    if [ "$verb" = create ] && [ "$has_label" = 1 ] && [ "${STUB_REFUSE_LABEL:-0}" = 1 ] \\
       && [ ! -e "$GH_LOG.label" ]; then
      echo "could not add label: 'security-alert' not found" >&2; exit 1
    fi
    if [ "$verb" = create ] && [ "$has_label" = 1 ] && [ "${STUB_CREATE_WITH_LABEL_FAIL:-0}" = 1 ]; then
      echo "HTTP 422: the label could not be applied" >&2; exit 1
    fi
    if [ "$size" -gt 65536 ]; then
      echo "HTTP 422: body is too long (maximum is 65536 characters)" >&2; exit 1
    fi
    echo "$verb $kind $size" >> "$GH_LOG.posts"
    if [ -n "$src" ]; then cp "$src" "$GH_BODY"; else cp "$GH_BODY.inline" "$GH_BODY"; fi
    if [ "$verb" = create ]; then echo "https://example.test/example/example/issues/$((400 + attempt))"; fi
    exit 0 ;;
esac
exit 0
"""


def _executable(path: Path, text: str) -> Path:
    """Write ``text`` to ``path`` and make it executable."""
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def _inert(text: str) -> str:
    """``text`` made safe to quote in an assertion message that pytest prints in a job log.

    The runner reads ``##[name]`` anywhere in a line, and ``::name::`` at the start of a line after
    any white space, so the first is broken up, a bar goes in front of every line of the second,
    and a carriage return (which also ends a line for the runner) is shown as ``\\r``.
    """
    lines = text.replace("##[", "# #[").replace("\r", "\\r").split("\n")
    return "\n".join(f"| {line}" if line.lstrip().startswith("::") else line for line in lines)


def _step(path: Path, *, name: str | None = None, step_id: str | None = None) -> dict:
    """Return the step with the given name or id from a workflow or a composite action."""
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if "runs" in doc:
        groups = [doc["runs"]["steps"]]
    else:
        groups = [job["steps"] for job in doc["jobs"].values()]
    for steps in groups:
        for step in steps:
            if (name and step.get("name") == name) or (step_id and step.get("id") == step_id):
                return step
    raise AssertionError(f"step {name or step_id!r} not found in {path.name}")


def _audit_step() -> dict:
    """The composite action's ``audit`` step."""
    return _step(ACTION_FILE, step_id="audit")


def _alert_step() -> dict:
    """The workflow step that creates or updates the alert issue."""
    return _step(WORKFLOW_FILE, name="Create or update CVE alert issue")


def _close_step() -> dict:
    """The workflow step that closes the alert issue after a scan without findings."""
    return _step(WORKFLOW_FILE, name="Close CVE alert issue when clean")


def _constant(script: str, name: str) -> int:
    """Read an integer constant such as ``VULN_MAX_DESC=400`` from the script text."""
    match = re.search(rf"^\s*{name}=(\d+)\b", script, re.MULTILINE)
    assert match, f"constant {name} is not defined in the script"
    return int(match.group(1))


def _tabulate(rows: list[tuple[str, ...]]) -> str:
    """Format rows like pip-audit's columns format: padded to the widest cell, one space between."""
    sizes = [max(len(cell) for cell in column) for column in zip(*rows, strict=True)]
    lines = [" ".join(c.ljust(w) for c, w in zip(row, sizes, strict=True)).rstrip() for row in rows]
    lines.insert(1, " ".join("-" * width for width in sizes))
    return "\n".join(lines) + "\n"


def _finding(i: int, description: str, *, fix: str | None = None) -> tuple[str, ...]:
    """One synthetic finding row: name, version, id, fix versions, description."""
    fixed = f"1.0.{i + 1}" if fix is None else fix
    return (f"pkg{i:03d}", f"1.0.{i}", f"CVE-2026-{i:06d}", fixed, description)


def _ids(count: int) -> list[str]:
    """The advisory ids of ``_finding(0..count-1)``."""
    return [f"CVE-2026-{i:06d}" for i in range(count)]


def _table(rows: int, width: int) -> str:
    """A pip-audit-like table of ``rows`` findings whose descriptions are ``width`` bytes long."""
    return _tabulate([HEADER, *[_finding(i, "x" * width) for i in range(rows)]])


def _table_with_wide_cell(column: int, width: int) -> str:
    """Three findings in which one cell of ``column`` is ``width`` characters wide.

    The column is 0 (package), 1 (version), 2 (advisory id) or 3 (fix versions).  pip-audit pads the
    same column of the other rows to that width.  A wide id starts like a real one.
    """
    rows = [list(_finding(i, f"description {i}")) for i in range(3)]
    wide = "w" * width
    rows[1][column] = ("CVE-2026-000001" + wide)[:width] if column == 2 else wide
    return _tabulate([HEADER, *[tuple(row) for row in rows]])


def _verdict(count: int) -> str:
    """The verdict line pip-audit prints first (to standard error)."""
    return f"Found {count} known vulnerabilities in {max(count, 1)} packages"


def _failing_tool(tool: str) -> str:
    """A replacement for ``tool`` that prints a message and exits 1 without producing output."""
    return f'#!/usr/bin/env bash\necho "stub {tool}: failing on purpose" >&2\nexit 1\n'


def _mktemp_without_broken_copy() -> str:
    """A replacement for mktemp whose new directory already holds a directory named export-broken.txt.

    The audit step then cannot write the export's copy with the older marker broken up, and takes the
    fallback of that copy.
    """
    return (
        "#!/usr/bin/env bash\n"
        'dir="$(PATH="$REAL_PATH" mktemp "$@")" || exit 1\n'
        'if [ "${1:-}" = "-d" ]; then mkdir "$dir/export-broken.txt" || exit 1; fi\n'
        "printf '%s\\n' \"$dir\"\n"
    )


def _short_lines_with_char_across(cap: int, char: str, offset: int) -> str:
    """Lines of at most 100 bytes in which ``char`` starts ``offset`` bytes before byte ``cap``."""
    prefix_bytes = cap - offset
    lines = ["k" * 99] * (prefix_bytes // 100)
    rest = prefix_bytes % 100
    return "\n".join([*lines, "k" * rest + char + "m" * 50, *["m" * 99] * 200])


def _stubs_dir(tmp_path: Path, extra: dict[str, str] | None = None) -> Path:
    """Create the directory with the stubs (and any tool replacements) that goes first on PATH."""
    bindir = tmp_path / "bin"
    bindir.mkdir(exist_ok=True)
    _executable(bindir / "uv", _UV_STUB)
    _executable(bindir / "gh", _GH_STUB)
    for tool, text in (extra or {}).items():
        _executable(bindir / tool, text)
    return bindir


def _env(tmp_path: Path, bindir: Path, locale: str | None, extra: dict[str, str]) -> dict[str, str]:
    """Environment for a script: PATH, TMPDIR, this process's locale variables and ``extra``."""
    real_path = os.environ["PATH"]
    env = {
        "PATH": f"{bindir}{os.pathsep}{real_path}",
        "REAL_PATH": real_path,
        "TMPDIR": str(tmp_path),
    }
    for key in ("LANG", "LC_ALL", "LC_CTYPE"):
        if key in os.environ:
            env[key] = os.environ[key]
    if locale is not None:
        env["LC_ALL"] = locale
        env["LANG"] = locale
    env.update(extra)
    return env


def _run_script(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[bytes]:
    """Run a step script with a time limit and no standard input.

    Standard error goes into the same stream as standard output, in order, like the job log of the
    runner; the result holds the log in ``stdout``. The script runs in its own session, and a time-out
    kills its whole process group, so that no process it started (an awk, say) is left running.
    """
    proc = subprocess.Popen(
        command,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try:
        out, _ = proc.communicate(timeout=STEP_TIMEOUT)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        raise
    return subprocess.CompletedProcess(command, proc.returncode, out, None)


def _require_openssl() -> None:
    """The audit step needs the ``openssl`` command: skip locally, fail on CI if it is missing."""
    if shutil.which("openssl") is not None:
        return
    message = "the audit step needs the openssl command (random output delimiter and stop token)"
    if os.environ.get("CI") == "true":
        pytest.fail(message)
    pytest.skip(message)


@dataclass
class AuditRun:
    """The result of running the audit step: process, parsed outputs, summary, raw output bytes."""

    process: subprocess.CompletedProcess[bytes]
    outputs: dict[str, str]
    delimiter: str | None
    summary: str
    raw_outputs: bytes

    @property
    def details(self) -> str | None:
        """The exported ``vuln-details`` value, or ``None`` if it was not written."""
        return self.outputs.get("vuln-details")

    @property
    def log(self) -> str:
        """The job log of the step: standard output and standard error in one stream, as text.

        Invalid bytes are replaced and carriage returns are kept.
        """
        return self.process.stdout.decode("utf-8", errors="replace")


def _parse_outputs(data: bytes) -> tuple[dict[str, str], str | None]:
    """Parse a GITHUB_OUTPUT file the way the runner does (strict UTF-8, ``name<<DELIMITER``)."""
    text = data.decode("utf-8")  # invalid bytes fail the test
    lines = text.split("\n")
    outputs: dict[str, str] = {}
    delimiter = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if "<<" in line and "=" not in line.split("<<", 1)[0]:
            key, delimiter = line.split("<<", 1)
            end = next((j for j in range(i + 1, len(lines)) if lines[j] == delimiter), None)
            assert end is not None, f"output block {key!r} has no closing delimiter {delimiter!r}"
            outputs[key] = "\n".join(lines[i + 1 : end])
            i = end
        elif "=" in line:
            key, value = line.split("=", 1)
            outputs[key] = value
        i += 1
    return outputs, delimiter


def _run_audit_step(
    tmp_path: Path,
    table: str | bytes,
    *,
    verdict: str | None = None,
    fail_on_vuln: str = "true",
    requirements: str | None = None,
    requirements_present: bool = True,
    stubs: dict[str, str] | None = None,
    locale: str | None = None,
    audit_exit: int = 1,
    env_extra: dict[str, str] | None = None,
) -> AuditRun:
    """Run the audit step on a replayed table, as the runner does (bash -eo pipefail)."""
    _require_openssl()
    tmp_path.mkdir(parents=True, exist_ok=True)
    script = _audit_step()["run"].replace("/tmp/", f"{tmp_path}/")
    requirements_path = tmp_path / "requirements.txt"
    if requirements is None:
        requirements = "".join(f"pkg{i}==1.0.{i}\n" for i in range(25))
    if requirements_present:
        requirements_path.write_text(requirements, encoding="utf-8")
    expressions = {
        "${{ steps.allowlist.outputs.ignore_flags }}": "",
        "${{ inputs.requirements-path }}": str(requirements_path),
        "${{ inputs.min-audited-packages }}": "20",
        "${{ inputs.fail-on-vuln }}": fail_on_vuln,
    }
    for expression, value in expressions.items():
        script = script.replace(expression, value)
    assert "${{" not in script, "unsubstituted expression left in the step"
    data = table if isinstance(table, bytes) else table.encode("utf-8")
    (tmp_path / "table.txt").write_bytes(data)
    bindir = _stubs_dir(tmp_path, stubs)
    github_output, summary = tmp_path / "github_output.txt", tmp_path / "summary.md"
    github_output.write_text("", encoding="utf-8")
    if verdict is None:
        # One finding per line below the header and the separator, with or without a final line feed.
        verdict = _verdict(max(data.rstrip(b"\n").count(b"\n") - 1, 0))
    extra = {
        "GITHUB_OUTPUT": str(github_output),
        "GITHUB_STEP_SUMMARY": str(summary),
        "STUB_TABLE": str(tmp_path / "table.txt"),
        "STUB_VERDICT": verdict,
        "STUB_AUDIT_EXIT": str(audit_exit),
        **(env_extra or {}),
    }
    # GitHub runs `shell: bash` as: bash --noprofile --norc -eo pipefail
    command = ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script]
    process = _run_script(command, _env(tmp_path, bindir, locale, extra))
    raw = github_output.read_bytes()
    outputs, delimiter = _parse_outputs(raw)
    return AuditRun(process, outputs, delimiter, summary.read_text("utf-8", errors="replace"), raw)


def _calls(log: Path) -> list[list[str]]:
    """The recorded ``gh`` invocations: one list of arguments per call."""
    if not log.exists():
        return []
    chunks = [c for c in log.read_bytes().split(b"\x01") if c]
    return [[a.decode("utf-8") for a in chunk.split(b"\0")[:-1]] for chunk in chunks]


@dataclass
class AlertRun:
    """The result of running the alert or close step: process, gh calls, accepted posts, body."""

    process: subprocess.CompletedProcess[bytes]
    calls: list[list[str]]
    posts: list[str]
    body_path: Path

    @property
    def log(self) -> str:
        """The job log of the step: standard output and standard error in one stream, as text."""
        return self.process.stdout.decode("utf-8", errors="replace")

    @property
    def body(self) -> str:
        """The last accepted post body, decoded as strict UTF-8."""
        return self.body_path.read_bytes().decode("utf-8")

    def verbs(self) -> list[str]:
        """The ``gh`` subcommands that were called, e.g. ``issue list``."""
        return [" ".join(call[:2]) for call in self.calls]


def _run_gh_step(
    tmp_path: Path,
    script: str,
    env_extra: dict[str, str],
    *,
    stubs: dict[str, str] | None = None,
    locale: str | None = None,
    stub_env: dict[str, str] | None = None,
) -> AlertRun:
    """Run a workflow step with the recording ``gh`` (default shell of a ``run:`` step: bash -e)."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    bindir = _stubs_dir(tmp_path, stubs)
    extra = {
        "GH_TOKEN": "x",
        "REPO": "example/example",
        "RUN_URL": RUN_URL,
        "GH_LOG": str(tmp_path / "gh.log"),
        "GH_BODY": str(tmp_path / "body.txt"),
        **env_extra,
        **(stub_env or {}),
    }
    command = ["bash", "--noprofile", "--norc", "-e", "-c", script]
    process = _run_script(command, _env(tmp_path, bindir, locale, extra))
    posts_file = tmp_path / "gh.log.posts"
    posts = posts_file.read_text(encoding="utf-8").splitlines() if posts_file.exists() else []
    return AlertRun(process, _calls(tmp_path / "gh.log"), posts, tmp_path / "body.txt")


def _stub_env(existing: str, flags: dict[str, str]) -> dict[str, str]:
    """Environment variables that steer the ``gh`` stub."""
    steering = {f"STUB_{key.upper()}": value for key, value in flags.items()}
    return {"STUB_EXISTING": existing, **steering}


def _held_issues(tmp_path: Path, *issues: tuple[int, str, str, str, str]) -> str:
    """Write the issues that the ``gh`` double holds and return the path to pass as ``issues=``.

    One line per issue: number, state (``open`` or ``closed``), title, labels separated by commas,
    author, as ``LIVE_ALERT`` and ``EARLIER_ALERT`` give them.
    """
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "issues.txt"
    path.write_text("".join("|".join(map(str, issue)) + "\n" for issue in issues), encoding="utf-8")
    return str(path)


def _run_alert_step(
    tmp_path: Path,
    details: str,
    *,
    existing: str = "385",
    stubs: dict[str, str] | None = None,
    locale: str | None = None,
    env: dict[str, str] | None = None,
    **stub_flags: str,
) -> AlertRun:
    """Run the alert step; ``existing=""`` selects the create path; flags go to the ``gh`` stub."""
    return _run_gh_step(
        tmp_path,
        _alert_step()["run"],
        {"VULN_DETAILS": details, **(env or {})},
        stubs=stubs,
        locale=locale,
        stub_env=_stub_env(existing, stub_flags),
    )


def _run_close_step(
    tmp_path: Path,
    *,
    existing: str = "385",
    env: dict[str, str] | None = None,
    **stub_flags: str,
) -> AlertRun:
    """Run the close step (the scan has no findings)."""
    return _run_gh_step(
        tmp_path, _close_step()["run"], dict(env or {}), stub_env=_stub_env(existing, stub_flags)
    )


def _sections(value: str) -> tuple[list[str], list[str], str | None]:
    """Split an export into (finding lines, description lines, notice) at its section headers."""
    lines = value.split("\n")
    starts = [i for i, line in enumerate(lines) if line.startswith("Findings (")]
    splits = [i for i, line in enumerate(lines) if line.startswith("Descriptions (")]
    assert starts and splits, f"the export has no Findings/Descriptions sections: {value[:300]!r}"
    start, split = starts[0], splits[0]
    notice = lines[-1] if lines[-1].startswith("[clipped:") else None
    findings = lines[start + 3 : split]  # skip the section line, the header and the separator
    descriptions = lines[split + 1 : -1 if notice else None]
    return findings, descriptions, notice


_NOTICE = re.compile(
    r"^\[clipped: findings: (?P<findings>\d+) total, (?P<listed>\d+) listed"
    r"(?:, lines cut to (?P<fixedbytes>\d+) bytes: (?P<fixed>\d+))?; "
    r"descriptions: (?P<shown>\d+) shown, (?P<short>\d+) cut to (?P<bytes>\d+) bytes, "
    r"(?P<omitted>\d+) omitted; for the full output, see the step summary or job log of the "
    r"workflow run\]$"
)


def _notice(value: str) -> re.Match[str]:
    """The parsed notice of an export that was clipped."""
    notice = _sections(value)[2]
    assert notice is not None, "no notice at the end of the export"
    match = _NOTICE.match(notice)
    assert match, f"notice does not have the documented form: {notice!r}"
    return match


# The commands the runner registers (actions/runner, Runner.Worker/ActionCommandManager.cs).
_RUNNER_COMMAND_NAMES = frozenset(
    {
        "add-mask",
        "add-matcher",
        "add-path",
        "debug",
        "echo",
        "endgroup",
        "error",
        "group",
        "notice",
        "remove-matcher",
        "save-state",
        "set-env",
        "set-output",
        "stop-commands",
        "warning",
    }
)
# The script's own window markers; every other `::stop-commands::` line is foreign.
_OWN_WINDOW_OPEN = re.compile(r"::stop-commands::[0-9a-f]{32}")
_OWN_WINDOW_CLOSE = re.compile(r"::[0-9a-f]{32}::")
# Every other workflow command that the audit step prints itself, in full.  A line that the runner
# would process and that is not one of these (or the window opener) is foreign.  The tests that
# make a tool fail print the degraded-mode messages, so a changed message must change this list.
_OWN_MESSAGES = [
    re.compile(pattern)
    for pattern in (
        r"::warning::Could not sanitize the pip-audit output with the usual tools; "
        r"falling back to printable ASCII\.",
        r"::warning::Could not generate a random token; the pip-audit output is not printed to "
        r"this log\.",
        r"::warning::Could not build the findings export; exporting advisory IDs only\.",
        r"::warning::Could not break up the older command marker in the findings export; "
        r"exporting a short note instead\.",
        r"::warning::Could not finish reporting the findings; see the step summary or job log "
        r"of this run\.",
        r"::warning::pip-audit found vulnerabilities in the dependency tree",
        # The script joins the two halves of the next three messages with echo, which puts one
        # more space between them than the text has: hence " +" after the full stops.
        r"::warning::Vulnerabilities found but fail-on-vuln=false \u2014 not blocking this run\. +"
        r"The scheduled security scan will open/update a CVE alert issue\.",
        r"::error::pip-audit found unfixed vulnerabilities \(fail-on-vuln=true\)",
        r"::error::D5 guard: pip-audit did not produce a recognizable verdict line\. +"
        r"Possible silent failure or neutered invocation\. Audit result not trusted\.",
        r"::error::D5 guard: requirements file contains only \d+ packages +\(floor: \d+\)\. "
        r"The full dependency tree was not audited\. +Check that uv export --all-extras "
        r"--no-emit-project ran correctly\.",
    )
]


def _parse_runner_command(line: str, extra: frozenset[str] = frozenset()) -> tuple[str, str] | None:
    """Read ``line`` as the runner's ``ActionCommand`` parser does: ``(name, data)`` or ``None``.

    The ``::name::data`` form must open the line (leading white space is skipped).  The older
    ``##[name]data`` form is found *anywhere* in the line, so a prefix such as ``| `` does not hide
    it (the runner's own unit test parses ``>>>   ##[do-something k1=v1;]msg``).  Only registered
    names count; ``extra`` holds the token that a ``stop-commands`` window registers.
    """
    known = _RUNNER_COMMAND_NAMES | extra
    opening = line.lstrip()
    if opening.startswith("::"):
        end = opening.find("::", 2)
        name = opening[2:end].split(" ")[0].lower() if end >= 0 else ""
        if name in known:
            return name, opening[end + 2 :]
    start = line.find("##[")
    end = line.find("]", start) if start >= 0 else -1
    if end >= 0:
        name = line[start + 3 : end].split(" ")[0].lower()
        if name in known:
            return name, line[end + 1 :]
    return None


def _runner_commands(log: str) -> list[str]:
    """Lines the runner would process as workflow commands, honouring stop-commands windows.

    The runner reads the step's output line by line; .NET ends a line at a carriage return as well.
    A window opened by ``stop-commands`` swallows every line up to the one that carries its token.
    The lines that open a window are returned too, so a foreign window shows up.
    """
    commands: list[str] = []
    token: str | None = None
    for line in re.split(r"\r\n|\r|\n", log):
        if token is not None:
            parsed = _parse_runner_command(line, frozenset({token.lower()}))
            if parsed is not None and parsed[0] == token.lower():
                token = None
            continue
        parsed = _parse_runner_command(line)
        if parsed is None:
            continue
        commands.append(line)
        if parsed[0] == "stop-commands" and parsed[1]:
            token = parsed[1]
    return commands


def _foreign_commands(log: str) -> list[str]:
    """Commands the runner would process that the audit step did not print itself, word for word."""
    return [
        command
        for command in _runner_commands(log)
        if not _OWN_WINDOW_OPEN.fullmatch(command)
        and not any(message.fullmatch(command) for message in _OWN_MESSAGES)
    ]


def _window(log: str) -> tuple[list[str], list[str]]:
    """Split the job log into (lines inside the script's stop window, lines outside it)."""
    lines = re.split(r"\r\n|\r|\n", log)
    opening = [i for i, line in enumerate(lines) if _OWN_WINDOW_OPEN.fullmatch(line)]
    closing = [i for i, line in enumerate(lines) if _OWN_WINDOW_CLOSE.fullmatch(line)]
    assert len(opening) == len(closing) == 1 and opening[0] < closing[0], (
        "the log has no single stop-commands window that is closed"
    )
    inside = lines[opening[0] + 1 : closing[0]]
    return inside, [*lines[: opening[0]], *lines[closing[0] + 1 :]]


def _log_characters() -> list[tuple[str, str, str]]:
    """(label, character, replacement) for every character the job log must not hold anywhere.

    These are the C0 controls except tab and line feed (ESC and BEL among them), DEL, all 32 C1
    controls, the line and paragraph separators, the bidirectional controls, the zero-width and
    other invisible format characters (the ends of every default-ignorable range, and the whole
    ranges of the small ones) and the Braille blank.  Line-break-like characters and the Braille
    blank become a space so that neighbouring words stay apart; the others vanish.  The first entry
    is the NUL byte, which no environment variable can hold.
    """
    codes = [
        *[code for code in range(0x20) if code not in (0x09, 0x0A)],
        0x7F,
        *range(0x80, 0xA0),
        0x2028,
        0x2029,
        0x00AD,  # soft hyphen
        0x034F,  # combining grapheme joiner
        0x061C,  # Arabic letter mark
        0x115F,  # Hangul fillers
        0x1160,
        0x17B4,  # Khmer inherent vowels
        0x17B5,
        *range(0x180B, 0x1810),  # Mongolian free variation selectors and vowel separator
        *range(0x200B, 0x2010),  # zero-width space and joiners, left and right marks
        *range(0x202A, 0x202F),  # bidirectional embeddings and overrides
        *range(0x2060, 0x2070),  # word joiner, invisible operators, isolates
        0x2800,  # Braille pattern blank
        0x3164,  # Hangul filler
        *range(0xFE00, 0xFE10),  # variation selectors 1 to 16
        0xFEFF,  # byte order mark
        0xFFA0,  # halfwidth Hangul filler
        *range(0xFFF0, 0xFFFC),  # reserved, then interlinear annotation
        *range(0x1BCA0, 0x1BCA4),  # shorthand format controls
        *range(0x1D173, 0x1D17B),  # musical symbol format controls
        *range(0xE0000, 0xE0080),  # tag characters
        0xE0080,  # reserved, start and end of the block that follows the tags
        0xE00FF,
        *range(0xE0100, 0xE0110),  # variation selectors 17 to 32
        0xE01EF,  # variation selector 256
        0xE01F0,  # reserved
        0xE0FFF,
    ]
    spaces = {0x0B, 0x0C, 0x0D, 0x85, 0x2028, 0x2029, 0x2800}
    return [(f"U+{code:04X}", chr(code), " " if code in spaces else "") for code in codes]


def _fences(markdown: str) -> list:
    """The ``fence`` tokens of a CommonMark parse (markdown-it-py)."""
    return [t for t in MarkdownIt("commonmark").parse(markdown) if t.type == "fence"]


def _token_types(markdown: str) -> list[str]:
    """Token types of a CommonMark parse, including inline children; a fence is one token."""
    kinds: list[str] = []
    for token in MarkdownIt("commonmark").parse(markdown):
        kinds.append(token.type)
        kinds.extend(child.type for child in token.children or [])
    return kinds


def _sanitize_sed_lines(script: str) -> list[str]:
    """The lines of ``script`` that build the ``SANITIZE_SED`` program (bash ``$'...'`` strings)."""
    return [line.strip() for line in script.splitlines() if line.strip().startswith("SANITIZE_SED")]


def _sed_filter(script: str, data: bytes) -> bytes:
    """Run ``data`` through the sed program of ``script`` exactly as its ``sanitize`` runs it."""
    program = "\n".join(_sanitize_sed_lines(script)) + '\nLC_ALL=C sed -e "$SANITIZE_SED"\n'
    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-c", program],
        input=data,
        capture_output=True,
        timeout=STEP_TIMEOUT,
        check=True,
    )
    return result.stdout


class TestAuditStepExportIsBounded:
    """The export stays small, lists every finding first, and says exactly what was shortened."""

    def test_oversize_table_when_exported_then_below_env_limit(self, tmp_path: Path) -> None:
        run = _run_audit_step(tmp_path, _table(rows=34, width=6_000))

        assert run.process.returncode == 1, "fail-on-vuln=true exits 1 only after the outputs"
        assert run.details is not None, _inert(run.log)
        assert len(run.details.encode("utf-8")) <= _constant(_audit_step()["run"], "VULN_MAX_TOTAL")
        assert len(run.details.encode("utf-8")) < ENV_STRING_LIMIT

    def test_constants_when_read_from_the_script_then_match_the_documented_bounds(self) -> None:
        audit, alert = _audit_step()["run"], _alert_step()["run"]

        assert _constant(audit, "VULN_MAX_DESC") == 400
        assert _constant(audit, "VULN_MAX_FIXED") == 300
        assert _constant(audit, "VULN_MAX_FINDINGS") == 30_000
        assert _constant(audit, "VULN_MAX_TOTAL") == 40_000
        assert _constant(audit, "VULN_MAX_LINE") == 600
        assert _constant(audit, "VULN_MAX_CELL") == WIDE_CELL_LIMIT == 200
        assert _constant(alert, "MAX_LINE_BYTES") == 600
        assert _constant(alert, "MAX_DETAILS_BYTES") == 57_000

    def test_every_finding_when_exported_then_listed_before_any_description(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(rows=34, width=6_000))

        assert run.details is not None
        findings, descriptions, _ = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(34)
        assert len(descriptions) == 34
        assert run.details.split("\n")[0] == _verdict(34)

    def test_description_clip_when_exported_then_every_line_is_within_the_bound(
        self, tmp_path: Path
    ) -> None:
        limit = _constant(_audit_step()["run"], "VULN_MAX_DESC")
        run = _run_audit_step(tmp_path, _table(rows=34, width=6_000))

        assert run.details is not None
        _, descriptions, _ = _sections(run.details)
        for line in descriptions:
            assert len(line.split(": ", 1)[1].encode("utf-8")) == limit, line[:80]
        assert max(len(line.encode("utf-8")) for line in run.details.split("\n")) < limit + 60

    def test_notice_when_descriptions_shortened_then_numbers_match_the_text(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(rows=34, width=6_000))

        assert run.details is not None
        findings, descriptions, _ = _sections(run.details)
        notice = _notice(run.details)
        assert int(notice["findings"]) == int(notice["listed"]) == len(findings) == 34
        assert int(notice["shown"]) == int(notice["short"]) == len(descriptions) == 34
        assert int(notice["omitted"]) == 0 and notice["fixed"] is None
        assert int(notice["bytes"]) == _constant(_audit_step()["run"], "VULN_MAX_DESC")

    def test_300_long_rows_when_exported_then_every_id_listed_and_omissions_counted(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(rows=300, width=600))

        assert run.details is not None
        assert len(run.details.encode("utf-8")) <= _constant(_audit_step()["run"], "VULN_MAX_TOTAL")
        findings, descriptions, _ = _sections(run.details)
        notice = _notice(run.details)
        assert [line.split()[2] for line in findings] == _ids(300)
        assert int(notice["findings"]) == int(notice["listed"]) == 300
        assert int(notice["shown"]) == int(notice["short"]) == len(descriptions)
        assert int(notice["omitted"]) == 300 - len(descriptions) > 0

    def test_2000_findings_when_exported_then_the_finding_list_is_bounded_and_counted(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(rows=2_000, width=50))

        assert run.details is not None
        assert len(run.details.encode("utf-8")) <= _constant(_audit_step()["run"], "VULN_MAX_TOTAL")
        findings, descriptions, _ = _sections(run.details)
        notice = _notice(run.details)
        assert int(notice["findings"]) == 2_000
        assert int(notice["listed"]) == len(findings) < 2_000
        assert [line.split()[2] for line in findings] == _ids(len(findings))
        assert int(notice["omitted"]) == 2_000 - len(descriptions)

    def test_small_table_when_exported_then_findings_and_descriptions_are_complete(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(i, f"short description {i}") for i in range(3)]
        table = _tabulate([HEADER, *rows])

        run = _run_audit_step(tmp_path, table)

        assert run.details is not None and "[clipped" not in run.details
        findings, descriptions, notice = _sections(run.details)
        printed = table.rstrip("\n").split("\n")[2:]  # the rows as pip-audit printed them
        assert [line.split() for line in findings] == [line.split()[:4] for line in printed]
        expected = [f"{i + 1}. CVE-2026-{i:06d}: short description {i}" for i in range(3)]
        assert descriptions == expected
        assert notice is None

    def test_verdict_with_ignored_count_when_exported_then_it_is_the_first_line(
        self, tmp_path: Path
    ) -> None:
        verdict = "Found 3 known vulnerabilities, ignored 2 in 3 packages"  # pip-audit's form
        rows = [_finding(i, f"d{i}") for i in range(3)]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]), verdict=verdict)

        assert run.details is not None and run.details.split("\n")[0] == verdict

    def test_fix_versions_cell_very_long_when_exported_then_other_findings_are_complete(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(i, "d") for i in range(5)]
        rows[2] = _finding(2, "d", fix=",".join(f"1.0.{n}" for n in range(600)))

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]))

        assert run.details is not None
        findings, _, _ = _sections(run.details)
        notice = _notice(run.details)
        assert [line.split()[2] for line in findings] == _ids(5)
        limit = _constant(_audit_step()["run"], "VULN_MAX_FIXED")
        assert max(len(line.encode("utf-8")) for line in findings) == limit
        assert int(notice["fixed"]) == 1 and int(notice["fixedbytes"]) == limit

    def test_multi_line_description_when_exported_then_every_finding_is_still_listed(
        self, tmp_path: Path
    ) -> None:
        long_text = "\n".join(f"paragraph {n} " + "w" * 60 for n in range(400))
        rows = [_finding(i, long_text if i < 3 else "short") for i in range(34)]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]), verdict=_verdict(34))

        assert run.details is not None
        findings, descriptions, _ = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(34)
        assert len(descriptions) == 34
        assert descriptions[0].startswith("1. CVE-2026-000000: paragraph 0 ")
        assert "paragraph 1 " in descriptions[0], "continuation lines belong to the description"

    @pytest.mark.parametrize("lead", [" a", "a"], ids=["space-led", "letter-led"])
    def test_long_run_of_spaces_in_a_continuation_line_when_exported_then_it_finishes_in_time(
        self, tmp_path: Path, lead: str
    ) -> None:
        # Trimming the end of a line that holds a long run of spaces takes time that grows with the
        # square of the run in awk; a continuation line is cut to 1,000 bytes before it is trimmed.
        # Uncut, this line takes far longer than the step's time limit. A description's later lines
        # start at column 1: led by a space, as an indented line is, or by a letter, with the version
        # and id cells blank. Both are continuation lines, not findings.
        description = "start\n" + lead + " " * 500_000 + "b"
        rows = [_finding(0, description), _finding(1, "short")]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]), verdict=_verdict(2))

        assert run.details is not None, _inert(run.log)
        findings, descriptions, _ = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(2)
        assert descriptions[0].startswith("1. CVE-2026-000000: start a")

    def test_short_letter_led_line_in_a_description_when_exported_then_it_is_a_continuation(
        self, tmp_path: Path
    ) -> None:
        # A short later line of a description, such as the heading "Impact", starts at column 1
        # with a letter and leaves the version and id cells blank: it belongs to the description.
        rows = [_finding(0, "first\nImpact\nmore")]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]), verdict=_verdict(1))

        assert run.details is not None, _inert(run.log)
        findings, descriptions, notice = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(1)
        assert descriptions == ["1. CVE-2026-000000: first Impact more"]
        assert notice is None

    def test_blank_fix_versions_when_exported_then_the_row_is_still_a_finding(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(0, "first"), _finding(1, "no fix yet", fix=""), _finding(2, "third")]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]))

        assert run.details is not None
        findings, descriptions, _ = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(3)
        assert descriptions[1] == "2. CVE-2026-000001: no fix yet"

    def test_skipped_dependencies_table_when_present_then_it_is_not_listed_as_findings(
        self, tmp_path: Path
    ) -> None:
        skipped = _tabulate(
            [("Name", "Skip Reason"), ("jerry", "Dependency not found on PyPI: jerry (0.31.9)")]
        )
        table = _tabulate([HEADER, *[_finding(i, f"d{i}") for i in range(3)]]) + "\n" + skipped

        run = _run_audit_step(tmp_path, table, verdict=_verdict(3))

        assert run.details is not None
        findings, descriptions, _ = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(3)
        assert len(descriptions) == 3 and "jerry" not in run.details

    @pytest.mark.parametrize("char", [TWO_BYTES, THREE_BYTES, FOUR_BYTES])
    def test_character_split_by_the_description_clip_when_exported_then_valid_utf8(
        self, tmp_path: Path, char: str
    ) -> None:
        limit = _constant(_audit_step()["run"], "VULN_MAX_DESC")
        for offset in range(1, len(char.encode("utf-8"))):  # the clip falls inside the character
            text = "y" * (limit - offset) + char + "z" * 50
            table = _tabulate([HEADER, *[_finding(i, text) for i in range(3)]])

            run = _run_audit_step(tmp_path / f"o{offset}", table)

            assert run.details is not None, _inert(run.log)  # parsing decodes strictly
            assert len(_sections(run.details)[1]) == 3

    def test_description_clip_when_locale_differs_then_the_export_is_identical(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(i, THREE_BYTES * 300 + FOUR_BYTES * 80) for i in range(4)]
        table = _tabulate([HEADER, *rows])

        reference = _run_audit_step(tmp_path / "reference", table, locale="C")

        assert reference.details is not None
        for locale in (None, "C.UTF-8", "en_US.UTF-8"):  # absent locales fall back to C
            run = _run_audit_step(tmp_path / f"run-{locale}", table, locale=locale)
            assert run.details == reference.details, f"locale {locale}"

    def test_total_cap_when_the_export_tool_overproduces_then_the_value_stays_within_the_cap(
        self, tmp_path: Path
    ) -> None:
        cap = _constant(_audit_step()["run"], "VULN_MAX_TOTAL")
        line_cap = _constant(_audit_step()["run"], "VULN_MAX_LINE")
        # 60 KB of short lines and two long ones (one ASCII, one of three-byte characters, which a
        # cut that counts characters would not shorten enough); a three-byte character straddles
        # the byte at which the total cap falls.
        filler = (
            "L" * 5_000
            + "\n"
            + THREE_BYTES * 2_000
            + "\n"
            + ("a" * 99 + "\n") * 399
            + "a" * 99
            + THREE_BYTES
            + "tail\n"
            + ("b" * 99 + "\n") * 2_000  # 200 KB: more than a pipe buffer holds
        )
        fake_awk = f"#!/usr/bin/env bash\ncat > /dev/null\nprintf '%s' '{filler}'\n"

        run = _run_audit_step(tmp_path, _table(3, 50), stubs={"awk": fake_awk})

        assert run.process.returncode == 1, _inert(run.log)
        assert run.details is not None and DEGRADED not in run.log
        lines = run.details.split("\n")
        assert lines[0] == "L" * line_cap, "the capped output is exported"
        assert lines[1] == THREE_BYTES * (line_cap // 3) and lines[2] == "a" * 99
        assert 0 < len(run.details.encode("utf-8")) <= cap
        assert max(len(line.encode("utf-8")) for line in lines) <= line_cap

    @pytest.mark.parametrize("printed", ["garbage", "```", ""], ids=["garbage", "short", "empty"])
    def test_fence_tool_printing_no_valid_fence_when_summarised_then_a_pointer_replaces_the_text(
        self, tmp_path: Path, printed: str
    ) -> None:
        fake_awk = f"#!/usr/bin/env bash\ncat > /dev/null\nprintf '%s' '{printed}'\n"

        run = _run_audit_step(tmp_path, _table(3, 50), stubs={"awk": fake_awk})

        assert run.process.returncode == 1, _inert(run.log)
        assert not _fences(run.summary)
        assert "See the log of this step, if it shows a copy." in run.summary

    def test_summary_when_findings_exist_then_it_names_the_characters_that_were_removed(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(3, 50))

        assert "with control and invisible (default-ignorable) characters removed:" in run.summary
        assert "formatting characters" not in run.summary

    def test_summary_when_findings_exist_then_it_holds_the_sanitized_output_in_one_fence(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(rows=34, width=6_000))

        fences = _fences(run.summary)
        assert len(fences) == 1
        assert fences[0].content.count("\n") >= 36 and "pkg033" in fences[0].content
        assert "\r" not in run.summary

    def test_summary_when_findings_exist_then_a_constant_note_before_the_fence_says_it_is_data(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(rows=3, width=50))

        lines = run.summary.split("\n")
        assert THIRD_PARTY_NOTE in lines
        assert THIRD_PARTY_NOTE not in _fences(run.summary)[0].content
        fence_start = next(i for i, line in enumerate(lines) if line.startswith("````"))
        assert lines.index(THIRD_PARTY_NOTE) < fence_start

    def test_clean_audit_when_no_findings_then_outputs_say_clean_and_no_details(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, "", verdict="No known vulnerabilities found", audit_exit=0)

        assert run.process.returncode == 0, _inert(run.log)
        assert run.outputs["vuln-found"] == "false" and run.outputs["clean"] == "true"
        assert run.outputs["vuln-details"] == ""

    def test_not_blocking_when_vulnerabilities_found_then_exit_zero_and_all_outputs(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(4, 100), fail_on_vuln="false")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.outputs["vuln-found"] == "true" and run.outputs["clean"] == "false"
        assert run.details and "::warning::Vulnerabilities found" in run.log

    def test_last_line_without_newline_when_exported_then_the_block_is_intact(
        self, tmp_path: Path
    ) -> None:
        table = _table(rows=3, width=500).rstrip("\n")

        run = _run_audit_step(tmp_path, table)

        assert run.details is not None
        assert [line.split()[2] for line in _sections(run.details)[0]] == _ids(3)
        assert run.raw_outputs.decode("utf-8").endswith(f"\n{run.delimiter}\n")

    def test_unrecognised_layout_when_exported_then_advisory_ids_only_with_a_warning(
        self, tmp_path: Path
    ) -> None:
        table = "some other layout CVE-2026-000001 and GHSA-abcd-efgh-ijkl\nPYSEC-2026-42 here\n"
        verdict = "Found 3 known vulnerabilities, ignored 2 in 3 packages"  # pip-audit's form

        run = _run_audit_step(tmp_path, table, verdict=verdict, fail_on_vuln="false")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details is not None and "advisory IDs only" in run.details
        assert run.details.split("\n")[0] == verdict
        for advisory in ("CVE-2026-000001", "GHSA-abcd-efgh-ijkl", "PYSEC-2026-42"):
            assert advisory in run.details
        assert DEGRADED in run.log

    def test_unrecognised_layout_with_invalid_utf8_when_exported_then_the_ids_on_that_line_are_found(
        self, tmp_path: Path
    ) -> None:
        # BSD grep (macOS) in a UTF-8 locale finds nothing on a line that holds invalid UTF-8.
        table = b"unknown layout \xff\xfe CVE-2026-000001 and GHSA-abcd-efgh-ijkl\nPYSEC-2026-42\n"
        verdict = "Found 3 known vulnerabilities in 3 packages"

        run = _run_audit_step(
            tmp_path, table, verdict=verdict, fail_on_vuln="false", locale="en_US.UTF-8"
        )

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details is not None and "advisory IDs only" in run.details
        for advisory in ("CVE-2026-000001", "GHSA-abcd-efgh-ijkl", "PYSEC-2026-42"):
            assert advisory in run.details

    def test_unrecognised_layout_with_thousands_of_ids_when_exported_then_the_list_is_bounded(
        self, tmp_path: Path
    ) -> None:
        short = "".join(f"CVE-2026-{i:06d} " for i in range(5_000))
        long_id = "CVE-" + "-".join(["a" * 40] * 5)  # the longest id the fixed pattern matches
        table = f"unknown layout\n{short}\n{(long_id + ' ') * 5_000}\n"

        run = _run_audit_step(tmp_path, table, verdict=_verdict(5_000), fail_on_vuln="false")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details is not None
        lines = run.details.split("\n")
        assert lines[0] == _verdict(5_000) and "advisory IDs only" in lines[1]
        assert sum(line.startswith("CVE-2026-") for line in lines) == 300
        assert "CVE-2026-004999" not in run.details and long_id not in run.details
        assert len(run.details.encode("utf-8")) < 5_000

    def test_unrecognised_layout_with_long_ids_when_exported_then_the_byte_total_is_bounded(
        self, tmp_path: Path
    ) -> None:
        long_id = "CVE-" + "-".join(["a" * 40] * 5)  # the longest id the fixed pattern matches
        table = f"unknown layout\n{(long_id + ' ') * 5_000}\n"

        run = _run_audit_step(tmp_path, table, verdict=_verdict(5_000), fail_on_vuln="false")

        assert run.details is not None
        assert 15_000 < len(run.details.encode("utf-8")) < 21_000
        assert all(len(line) <= 300 for line in run.details.split("\n"))

    def test_verdict_counts_more_findings_than_rows_when_exported_then_advisory_ids_only(
        self, tmp_path: Path
    ) -> None:
        # A row that the parser does not recognise would otherwise vanish from the list of findings.
        rows = [_finding(i, f"d{i}") for i in range(4)]

        run = _run_audit_step(
            tmp_path, _tabulate([HEADER, *rows]), verdict=_verdict(5), fail_on_vuln="false"
        )

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details is not None and "advisory IDs only" in run.details
        assert run.details.split("\n")[0] == _verdict(5)
        assert all(identifier in run.details for identifier in _ids(4))
        assert DEGRADED in run.log

    def test_multibyte_character_in_the_fix_versions_cell_when_exported_then_advisory_ids_only(
        self, tmp_path: Path
    ) -> None:
        # pip-audit pads a cell by characters and the parser counts bytes, so a multibyte character
        # in one of the first four cells moves every column after it.
        rows = [_finding(0, "first"), _finding(1, "second", fix=f"1.0.{TWO_BYTES}")]
        rows.append(_finding(2, "third"))

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]), fail_on_vuln="false")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details is not None and "advisory IDs only" in run.details
        assert all(identifier in run.details for identifier in _ids(3))
        assert DEGRADED in run.log

    def test_zero_width_space_in_an_id_cell_when_exported_then_advisory_ids_only(
        self, tmp_path: Path
    ) -> None:
        # The sanitizer deletes the character after pip-audit has padded the cell, so the columns of
        # that row move left by one.
        rows = [_finding(i, f"d{i}") for i in range(3)]
        rows[1] = ("pkg001", "1.0.1", f"CVE-2026-000001{chr(0x200B)}", "1.0.2", "d1")

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]), fail_on_vuln="false")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details is not None and "advisory IDs only" in run.details
        assert all(identifier in run.details for identifier in _ids(3))
        assert DEGRADED in run.log

    @pytest.mark.parametrize("column", [0, 1, 2], ids=["package", "version", "id"])
    def test_wide_cell_in_a_leading_column_when_exported_then_advisory_ids_only_within_the_limit(
        self, tmp_path: Path, column: int
    ) -> None:
        # pip-audit pads every other row of the column to the width of the widest cell, which leaves a
        # long run of spaces inside each finding line.  Trimming the end of such a line took time that
        # grows with the square of the width in mawk and gawk (17 s at 40,000 characters, measured on
        # Ubuntu 24.04 with mawk), so the program refuses a table with such a column; the harness's time
        # limit fails this test if the step ever takes that long again.
        run = _run_audit_step(tmp_path, _table_with_wide_cell(column, 50_000))

        assert run.process.returncode == 1, "fail-on-vuln=true exits 1 only after the outputs"
        assert run.outputs["vuln-found"] == "true", _inert(run.log)
        assert run.details is not None and "advisory IDs only" in run.details
        assert run.details.split("\n")[0] == _verdict(3) and "Findings (" not in run.details
        assert "CVE-2026-000000" in run.details and "CVE-2026-000002" in run.details
        assert len(run.details.encode("utf-8")) < 5_000
        assert DEGRADED in run.log

    @pytest.mark.parametrize("column", [0, 1, 2], ids=["package", "version", "id"])
    def test_cell_at_the_width_limit_when_exported_then_the_table_is_still_read(
        self, tmp_path: Path, column: int
    ) -> None:
        run = _run_audit_step(tmp_path, _table_with_wide_cell(column, WIDE_CELL_LIMIT))

        assert run.details is not None, _inert(run.log)
        assert "advisory IDs only" not in run.details and DEGRADED not in run.log
        findings, descriptions, notice = _sections(run.details)
        assert len(findings) == 3 and len(descriptions) == 3 and notice is None

    @pytest.mark.parametrize("column", [0, 1, 2], ids=["package", "version", "id"])
    def test_cell_one_past_the_width_limit_when_exported_then_advisory_ids_only(
        self, tmp_path: Path, column: int
    ) -> None:
        run = _run_audit_step(tmp_path, _table_with_wide_cell(column, WIDE_CELL_LIMIT + 1))

        assert run.details is not None, _inert(run.log)
        assert "advisory IDs only" in run.details and "Findings (" not in run.details
        assert "CVE-2026-000000" in run.details and "CVE-2026-000002" in run.details
        assert DEGRADED in run.log

    def test_wide_fix_versions_cell_when_exported_then_the_table_is_still_read_in_one_pass(
        self, tmp_path: Path
    ) -> None:
        # The padding of the fix versions column ends the finding line, where trimming the end of the
        # line is a single pass, so this column needs no width limit (it is still cut to
        # VULN_MAX_FIXED bytes, with a notice).
        run = _run_audit_step(tmp_path, _table_with_wide_cell(3, 50_000))

        assert run.details is not None, _inert(run.log)
        assert "advisory IDs only" not in run.details and DEGRADED not in run.log
        findings, descriptions, _ = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(3) and len(descriptions) == 3
        assert int(_notice(run.details)["fixed"]) == 1

    def test_requirements_file_empty_when_audited_then_the_guard_fails_closed(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(2, 10), requirements="")

        assert run.process.returncode == 1
        assert "D5 guard: requirements file contains only 0 packages" in run.log

    def test_requirements_file_missing_when_audited_then_the_guard_fails_closed(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(2, 10), requirements_present=False)

        assert run.process.returncode == 1
        assert "D5 guard: requirements file contains only" in run.log

    def test_verdict_missing_when_audited_then_the_guard_fails_closed(self, tmp_path: Path) -> None:
        run = _run_audit_step(tmp_path, _table(2, 10), verdict="")

        assert run.process.returncode == 1
        assert "D5 guard: pip-audit did not produce a recognizable verdict line" in run.log


@pytest.fixture(scope="module")
def hostile_audit_run(tmp_path_factory: pytest.TempPathFactory) -> AuditRun:
    """One run over a table with one row per hostile character, each between unique markers."""
    rows = [
        _finding(i, f"b{i:02d}{char}a{i:02d}") for i, (_, char, _) in enumerate(HOSTILE_CHARACTERS)
    ]
    return _run_audit_step(tmp_path_factory.mktemp("hostile"), _tabulate([HEADER, *rows]))


def _hostile_problems(text: str, surface: str) -> list[str]:
    """Hostile characters that survived in ``text``, or whose row lost its neighbours."""
    problems = []
    for i, (label, char, replacement) in enumerate(HOSTILE_CHARACTERS):
        expected = f"b{i:02d}{replacement}a{i:02d}"
        if char in text:
            problems.append(f"{label}: still present in the {surface}")
        if expected not in text:
            problems.append(f"{label}: {expected!r} missing from the {surface}")
    return problems


class TestAuditStepHostileText:
    """Advisory text is third-party data: nothing in it may act as a command or markup."""

    def test_every_hostile_character_when_exported_then_removed_from_the_export(
        self, hostile_audit_run: AuditRun
    ) -> None:
        run = hostile_audit_run
        assert run.details is not None, _inert(run.log)

        problems = _hostile_problems(run.details, "export")

        assert not problems, "\n".join(problems)

    def test_every_hostile_character_when_summarised_then_removed_from_the_step_summary(
        self, hostile_audit_run: AuditRun
    ) -> None:
        problems = _hostile_problems(hostile_audit_run.summary, "step summary")

        assert not problems, "\n".join(problems)

    def test_every_hostile_character_when_logged_then_removed_from_the_prefixed_copy(
        self, hostile_audit_run: AuditRun
    ) -> None:
        inside, outside = _window(hostile_audit_run.log)
        copy = "\n".join(inside)  # the copy is the only text inside the window

        problems = _hostile_problems(copy, "log copy")

        assert copy and not problems, "\n".join(problems)
        assert all(line.startswith("| ") for line in inside), "every line of the copy is prefixed"
        assert not any(line.startswith("| ") for line in outside), "no copy outside the window"

    def test_nul_byte_when_exported_then_later_findings_and_the_notice_survive(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(i, ("x" * 700) + ("\x00" if i == 0 else "")) for i in range(40)]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]))

        assert run.details is not None, _inert(run.log)
        findings, _, _ = _sections(run.details)
        assert [line.split()[2] for line in findings] == _ids(40)
        assert _notice(run.details) and "\x00" not in run.details

    def test_invalid_utf8_when_exported_then_the_bad_bytes_are_dropped_and_the_rest_is_kept(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(i, f"b{i:02d}@@{i:02d}@@a{i:02d}") for i in range(len(INVALID_UTF8))]
        table = _tabulate([HEADER, *rows]).encode("utf-8")
        for i, (_, sequence) in enumerate(INVALID_UTF8):
            table = table.replace(f"@@{i:02d}@@".encode(), sequence)

        run = _run_audit_step(tmp_path, table)

        assert run.details is not None, _inert(run.log)  # parsing decodes strictly
        for i, (label, _) in enumerate(INVALID_UTF8):
            marker = f"b{i:02d}a{i:02d}"
            assert marker in run.details and marker in run.summary, label
        assert [line.split()[2] for line in _sections(run.details)[0]] == _ids(len(INVALID_UTF8))

    def test_command_lines_in_descriptions_when_logged_then_no_runner_command_leaks(
        self, tmp_path: Path
    ) -> None:
        payload = "\r".join(
            [
                "visible",
                "::set-env name=A::B",
                "::stop-commands::x",
                "::add-mask::true",
                "::set-output name=vuln-found::false",
                "::error::forged",
                f"{OLD_MARKER}error]forged",
            ]
        )
        rows = [_finding(0, payload), _finding(1, "plain")]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]))

        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))
        assert run.outputs["vuln-found"] == "true" and run.details

    def test_hostile_table_when_exported_then_no_export_line_starts_with_a_runner_marker(
        self, tmp_path: Path
    ) -> None:
        # The runner prints the environment of the alert step, which holds the export, at the top of
        # that step's log, outside any stop window.  Every line of the export must start with text the
        # action writes: the verdict, a heading, a package name, a running number or the notice.
        marker = "::error::forged"
        rows = [
            ("pkg000", "1.0.0", f"{marker}-id", f"{marker}-fix", f"{OLD_MARKER}error]first"),
            (
                "pkg001",
                "1.0.1",
                f"{OLD_MARKER}error]id",
                f"{OLD_MARKER}error]fix",
                "second\r::warning::after cr",
            ),
            # A line that is shaped like a row and starts with a command, as a description with a
            # line feed would leave it: the parser must not take it for a finding.  pip-audit counts
            # three findings in the verdict.
            ("::error::row", "1.0.2", "CVE-2026-000002", "1.0.3", f"{OLD_MARKER}error]forged row"),
            ("pkg003", "1.0.3", "CVE-2026-000003", "1.0.4", "fourth"),
        ]

        run = _run_audit_step(
            tmp_path, _tabulate([HEADER, *rows]), verdict=_verdict(3), fail_on_vuln="false"
        )

        assert run.details is not None, _inert(run.log)
        assert "pkg003" in run.details, "the rows after the forged one are still listed"
        starts = [
            line for line in run.details.split("\n") if line.lstrip().startswith(("::", OLD_MARKER))
        ]
        assert not starts, _inert("\n".join(starts))
        # The older form is read anywhere in a line, so the export breaks it up as the log does.
        anywhere = [line for line in run.details.split("\n") if OLD_MARKER in line]
        assert not anywhere, _inert("\n".join(anywhere))

    def test_stop_token_when_run_twice_then_each_window_has_its_own_random_token(
        self, tmp_path: Path
    ) -> None:
        tokens = []
        for n in range(2):
            run = _run_audit_step(tmp_path / f"r{n}", _table(2, 10))
            found = re.findall(r"^::stop-commands::([0-9a-f]{32})$", run.log, re.MULTILINE)
            assert len(found) == 1, _inert(run.log)
            assert f"::{found[0]}::" in run.log.split("\n")
            tokens.append(found[0])
        assert tokens[0] != tokens[1]

    def test_markdown_in_descriptions_when_summarised_then_only_the_fence_holds_it(
        self, tmp_path: Path
    ) -> None:
        payload = "\r".join(
            [
                "start",
                "# Injected heading",
                "![img](http://x/y.png)",
                "[link](http://x)",
                "<img src=x onerror=y>",
                "@octocat @geekatron",
                "`````",
                "end",
            ]
        )
        rows = [_finding(0, payload), _finding(1, "plain")]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]))

        kinds = _token_types(run.summary)
        assert "\r" not in run.summary and len(_fences(run.summary)) == 1
        assert not {"html_block", "html_inline", "image", "link_open"} & set(kinds), kinds
        assert kinds.count("heading_open") == 1  # only the step's own heading

    @pytest.mark.parametrize("run_length", [3, 4, 5, 10, 100, 399])
    def test_backtick_runs_when_summarised_then_the_fence_is_longer_than_every_run(
        self, tmp_path: Path, run_length: int
    ) -> None:
        rows = [_finding(0, "a" + "`" * run_length + "b"), _finding(1, "plain")]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]))

        fences = _fences(run.summary)
        assert len(fences) == 1 and len(fences[0].markup) > run_length
        assert "`" * run_length in fences[0].content

    def test_delimiter_when_run_twice_then_it_is_random_and_hostile_text_stays_inside(
        self, tmp_path: Path
    ) -> None:
        hostile = "EOF VULN_DETAILS_0000000000000000 vuln-found=false clean=true vuln-details<<EOF"
        delimiters = []
        for n in range(2):
            rows = [_finding(0, hostile), _finding(1, "plain")]
            run = _run_audit_step(tmp_path / f"r{n}", _tabulate([HEADER, *rows]))
            assert run.delimiter is not None
            assert re.fullmatch(r"VULN_DETAILS_[0-9a-f]{16}", run.delimiter), run.delimiter
            assert run.details is not None and hostile in run.details
            assert run.outputs["vuln-found"] == "true" and run.outputs["clean"] == "false"
            delimiters.append(run.delimiter)
        assert delimiters[0] != delimiters[1]

    def test_ascii_fallback_when_iconv_fails_then_the_export_is_ascii_and_complete(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(i, f"caf{TWO_BYTES} {THREE_BYTES} text") for i in range(5)]

        run = _run_audit_step(
            tmp_path, _tabulate([HEADER, *rows]), stubs={"iconv": _failing_tool("iconv")}
        )

        assert run.details is not None and run.details.isascii()
        assert [line.split()[2] for line in _sections(run.details)[0]] == _ids(5)
        assert DEGRADED in run.log


@pytest.fixture(scope="module")
def hostile_log_run(tmp_path_factory: pytest.TempPathFactory) -> AuditRun:
    """One run over a table with one row per character that must stay out of the job log."""
    rows = [
        _finding(i, f"b{i:03d}{char}a{i:03d}") for i, (_, char, _) in enumerate(_log_characters())
    ]
    return _run_audit_step(tmp_path_factory.mktemp("hostile-log"), _tabulate([HEADER, *rows]))


class TestAuditStepLogHoldsOnlySanitizedText:
    """The job log is public: pip-audit's raw output is never printed, inside a stop window or not."""

    def test_every_hostile_character_when_logged_then_none_is_anywhere_in_the_job_log(
        self, hostile_log_run: AuditRun
    ) -> None:
        log = hostile_log_run.log

        found = [label for label, char, _ in _log_characters() if char in log]

        assert not found, f"in the job log: {found}"

    def test_every_hostile_character_when_logged_then_the_words_around_it_are_still_there(
        self, hostile_log_run: AuditRun
    ) -> None:
        missing = []
        for i, (label, _, replacement) in enumerate(_log_characters()):
            expected = f"b{i:03d}{replacement}a{i:03d}"
            if expected not in hostile_log_run.log:
                missing.append(f"{label}: {expected!r}")

        assert not missing, "\n".join(missing)

    def test_terminal_sequences_in_a_description_when_logged_then_only_the_visible_words_remain(
        self, tmp_path: Path
    ) -> None:
        # An operating-system-command 52 (clipboard write), a clear-screen sequence and a
        # right-to-left override, then two command-looking pieces after carriage returns.
        description = (
            "before \x1b]52;c;QUJD\x07 clip \x1b[2J red"
            "\N{RIGHT-TO-LEFT OVERRIDE}evil\N{POP DIRECTIONAL ISOLATE} "
            f"\r::error::INJECTED\r{OLD_MARKER}warning]FAKE after"
        )

        run = _run_audit_step(tmp_path, _tabulate([HEADER, _finding(0, description)]))

        found = [label for label, char, _ in _log_characters() if char in run.log]
        assert not found, f"in the job log: {found}"
        visible = "before ]52;c;QUJD clip [2J redevil  ::error::INJECTED ## [warning]FAKE after"
        assert visible in run.log
        assert OLD_MARKER not in run.log, _inert(run.log)

    def test_marker_in_a_description_when_logged_then_it_is_broken_up_in_the_log_and_the_export(
        self, tmp_path: Path
    ) -> None:
        # The stop window is the first protection against the older `##[name]` form; breaking the
        # marker in the copy that the log shows is the second, so that no `##[` reaches the log.
        description = (
            f"a {OLD_MARKER}warning]x b #{OLD_MARKER}y c {OLD_MARKER}{OLD_MARKER}z d "
            f"{OLD_MARKER}add-mask]e # #[ok] f #[g ##"
        )
        broken = "a ## [warning]x b ### [y c ## [## [z d ## [add-mask]e # #[ok] f #[g ##"

        run = _run_audit_step(tmp_path, _tabulate([HEADER, _finding(0, description)]))

        assert OLD_MARKER not in run.log, _inert(run.log)
        inside, outside = _window(run.log)
        assert any(line.endswith(broken) for line in inside), _inert("\n".join(inside))
        assert not any(line.startswith("| ") for line in outside)
        # The step summary keeps the text as written.  The export breaks the marker up as the log does:
        # the runner prints the alert step's environment, which holds the export, at the top of that
        # step's log, outside any stop window.
        assert description in run.summary
        assert run.details is not None and broken in run.details
        assert description not in run.details

    @pytest.mark.parametrize("separator", ["\r", " "], ids=["after-carriage-return", "mid-line"])
    def test_command_syntax_in_a_description_when_logged_then_the_runner_processes_none(
        self, tmp_path: Path, separator: str
    ) -> None:
        # The runner reads `::name::` only at the start of a line, but `##[name]` anywhere in it.
        commands = [
            "::error::CANARY1",
            f"{OLD_MARKER}error]CANARY2",
            "::warning::CANARY3",
            f"{OLD_MARKER}warning]CANARY4",
            "::add-mask::CANARY5",
            f"{OLD_MARKER}add-mask]CANARY6",
            "::stop-commands::CANARY7",
            f"{OLD_MARKER}stop-commands]CANARY8",
            "::set-output name=clean::true",
            f"{OLD_MARKER}set-output name=vuln-found]false",
            f"{OLD_MARKER}group]CANARY9",
            f"{OLD_MARKER}endgroup]",
        ]
        description = separator.join(["visible", *commands, "end"])

        run = _run_audit_step(tmp_path, _tabulate([HEADER, _finding(0, description)]))

        processed = _runner_commands(run.log)
        assert not any("CANARY" in command for command in processed), _inert("\n".join(processed))
        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))
        assert OLD_MARKER not in run.log, _inert(run.log)
        assert run.outputs["vuln-found"] == "true" and run.details

    def test_findings_when_logged_then_the_copy_is_the_only_text_and_sits_inside_the_window(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(rows=3, width=50))

        inside, outside = _window(run.log)

        assert [line.split()[3] for line in inside if line.startswith("| pkg")] == _ids(3)
        assert not any("CVE-2026-" in line for line in outside)

    def test_description_when_logged_then_it_appears_exactly_once(self, tmp_path: Path) -> None:
        rows = [_finding(0, "a plain advisory text"), _finding(1, "another text")]

        run = _run_audit_step(tmp_path, _tabulate([HEADER, *rows]))

        assert run.log.count("a plain advisory text") == 1

    def test_invalid_utf8_when_logged_then_the_job_log_is_valid_utf8_and_keeps_the_words(
        self, tmp_path: Path
    ) -> None:
        rows = [_finding(i, f"b{i:02d}@@{i:02d}@@a{i:02d}") for i in range(len(INVALID_UTF8))]
        table = _tabulate([HEADER, *rows]).encode("utf-8")
        for i, (_, sequence) in enumerate(INVALID_UTF8):
            table = table.replace(f"@@{i:02d}@@".encode(), sequence)

        run = _run_audit_step(tmp_path, table)

        run.process.stdout.decode("utf-8")  # raises if the job log holds a byte that is not UTF-8
        for i, (label, _) in enumerate(INVALID_UTF8):
            assert f"b{i:02d}a{i:02d}" in run.log, label

    def test_clean_audit_when_logged_then_the_verdict_is_in_the_log_as_a_prefixed_copy(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, "", verdict="No known vulnerabilities found", audit_exit=0)

        assert run.process.returncode == 0, _inert(run.log)
        inside, outside = _window(run.log)
        assert inside == ["| No known vulnerabilities found"]
        assert "No known vulnerabilities found" not in "\n".join(outside)

    def test_verdict_missing_when_logged_then_the_guard_failure_still_shows_the_output(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(tmp_path, _table(2, 10), verdict="")

        assert run.process.returncode == 1
        assert "D5 guard: pip-audit did not produce a recognizable verdict line" in run.log
        inside, _ = _window(run.log)
        assert [line.split()[3] for line in inside if line.startswith("| pkg")] == _ids(2)

    @pytest.mark.parametrize("tool", ["iconv", "sed"])
    def test_sanitizer_tool_failing_when_logged_then_the_log_holds_the_ascii_copy(
        self, tmp_path: Path, tool: str
    ) -> None:
        rows = [_finding(i, f"caf{TWO_BYTES} {THREE_BYTES} \x1b[2J text") for i in range(3)]

        run = _run_audit_step(
            tmp_path,
            _tabulate([HEADER, *rows]),
            fail_on_vuln="false",
            stubs={tool: _failing_tool(tool)},
        )

        assert run.process.returncode == 0, _inert(run.log)
        inside, _ = _window(run.log)
        assert DEGRADED in run.log
        assert inside and all(line.isascii() and "\x1b" not in line for line in inside)
        assert [line.split()[3] for line in inside if line.startswith("| pkg")] == _ids(3)
        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))

    def test_every_sanitizer_fallback_failing_when_logged_then_a_note_replaces_the_text(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(
            tmp_path,
            _table(rows=3, width=50),
            fail_on_vuln="false",
            stubs={"tr": _failing_tool("tr")},
        )

        assert run.process.returncode == 0, _inert(run.log)
        inside, outside = _window(run.log)
        assert inside == ["| (pip-audit output withheld: it could not be sanitized)"]
        assert DEGRADED in run.log and "CVE-2026-" not in "\n".join(outside)
        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))


class TestAuditStepFailsSafe:
    """A failing tool must degrade the export, never the audit step or the pull request's checks."""

    TOOLS = ["awk", "cut", "head", "iconv", "sed", "tr"]

    @pytest.mark.parametrize("tool", TOOLS)
    def test_export_tool_failing_when_not_blocking_then_step_exits_zero_with_a_warning(
        self, tmp_path: Path, tool: str
    ) -> None:
        run = _run_audit_step(
            tmp_path,
            _table(rows=34, width=900),
            fail_on_vuln="false",
            stubs={tool: _failing_tool(tool)},
        )

        assert run.process.returncode == 0, _inert(run.log)
        assert run.outputs["vuln-found"] == "true" and run.outputs["clean"] == "false"
        assert run.details and DEGRADED in run.log
        assert all(identifier in run.details for identifier in _ids(34))
        assert len(run.details.encode("utf-8")) <= _constant(_audit_step()["run"], "VULN_MAX_TOTAL")
        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))

    @pytest.mark.parametrize("tool", [*TOOLS, "openssl"])
    def test_export_tool_failing_when_blocking_then_step_still_exits_one_with_outputs(
        self, tmp_path: Path, tool: str
    ) -> None:
        run = _run_audit_step(
            tmp_path,
            _table(rows=5, width=100),
            fail_on_vuln="true",
            stubs={tool: _failing_tool(tool)},
        )

        assert run.process.returncode == 1, _inert(run.log)
        assert run.outputs["vuln-found"] == "true" and run.details
        assert "::error::pip-audit found unfixed vulnerabilities" in run.log

    def test_openssl_failing_when_exported_then_no_pip_audit_text_reaches_the_log(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(
            tmp_path,
            _table(rows=5, width=100),
            fail_on_vuln="false",
            stubs={"openssl": _failing_tool("openssl")},
        )

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details and all(identifier in run.details for identifier in _ids(5))
        assert DEGRADED in run.log
        assert not re.search(r"^::stop-commands::", run.log, re.MULTILINE)
        # Without a window even the sanitized copy stays out: its `| ` prefix stops a `::name::`
        # command, and breaking the marker stops `##[name]`, but the window is the first protection.
        assert "CVE-2026-" not in run.log and "pkg00" not in run.log
        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))

    def test_every_export_tool_failing_when_exported_then_advisory_ids_are_still_written(
        self, tmp_path: Path
    ) -> None:
        stubs = {tool: _failing_tool(tool) for tool in self.TOOLS}

        run = _run_audit_step(tmp_path, _table(5, 100), fail_on_vuln="false", stubs=stubs)

        assert run.process.returncode == 0, _inert(run.log)
        assert run.details and "see the step summary or job log of the workflow run" in run.details
        assert all(identifier in run.details for identifier in _ids(5))
        assert run.outputs["vuln-found"] == "true"
        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))

    def test_marker_break_failing_when_exported_then_a_warning_and_a_short_note_are_written(
        self, tmp_path: Path
    ) -> None:
        run = _run_audit_step(
            tmp_path,
            _table(rows=5, width=100),
            fail_on_vuln="false",
            stubs={"mktemp": _mktemp_without_broken_copy()},
        )

        assert run.process.returncode == 0, _inert(run.log)
        assert run.outputs["vuln-found"] == "true"
        assert MARKER_BREAK_FAILED in _runner_commands(run.log), _inert(run.log)
        assert run.details == EXPORT_FAILED_NOTE
        assert not _foreign_commands(run.log), _inert("\n".join(_foreign_commands(run.log)))


class TestAlertStepBodyIsBounded:
    """The alert step posts a body GitHub accepts, whatever the details look like."""

    def test_normal_details_when_posted_then_the_body_file_is_used_and_the_issue_commented(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "Findings (34):\nrow")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.posts and run.posts[-1].startswith("comment file ")
        assert ["issue", "comment", "385"] == run.calls[-1][:3]
        assert "Updated existing CVE alert issue #385" in run.log

    def test_several_open_alert_issues_when_posting_then_the_first_one_is_updated(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "row", existing="385\n390")

        assert run.process.returncode == 0, _inert(run.log)
        assert ["issue", "comment", "385"] == run.calls[-1][:3] and len(run.posts) == 1

    def test_issue_list_when_called_then_the_limit_is_raised_and_the_title_is_matched(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "row")

        first = run.calls[0]
        assert first[:2] == ["issue", "list"] and first[first.index("--limit") + 1] == "100"
        assert first[first.index("--label") + 1] == "security-alert"
        assert any(ISSUE_TITLE in argument for argument in first)

    def test_gh_when_posting_then_only_the_expected_subcommands_are_called(
        self, tmp_path: Path
    ) -> None:
        for n, existing in enumerate(["385", ""]):
            run = _run_alert_step(tmp_path / f"r{n}", "row", existing=existing)

            allowed = {"issue list", "label create", "issue comment", "issue create"}
            assert set(run.verbs()) <= allowed

    def test_invalid_utf8_when_posted_then_the_bad_bytes_are_dropped_and_the_rest_is_kept(
        self, tmp_path: Path
    ) -> None:
        # Python passes arbitrary bytes through an environment variable as lone surrogates.
        lines = [
            f"{i}. A: b{i:02d}{sequence.decode('utf-8', errors='surrogateescape')}a{i:02d}"
            for i, (_, sequence) in enumerate(INVALID_UTF8)
        ]

        run = _run_alert_step(tmp_path, "\n".join(lines))

        assert run.process.returncode == 0, _inert(run.log)
        for i, (label, _) in enumerate(INVALID_UTF8):  # `body` decodes as strict UTF-8
            assert f"{i}. A: b{i:02d}a{i:02d}" in run.body, label

    def test_posted_text_when_hostile_then_it_equals_the_input_inside_one_fence(
        self, tmp_path: Path
    ) -> None:
        details = "\n".join(
            [
                "1. A: * % \\ $(touch CANARY_CMD) `touch CANARY_TICK` ${CANARY_VAR:-expanded}",
                "2. B: $((1+1)) %s %n %d \\n \\t   leading blanks and trailing blanks   ",
                "3. C: @octocat @geekatron/security-team #385 <script>alert(1)</script>",
                "\ttabbed line",
            ]
        )

        run = _run_alert_step(tmp_path, details)

        assert run.process.returncode == 0, _inert(run.log)
        fences = _fences(run.body)
        assert len(fences) == 1 and fences[0].content == details + "\n"
        assert not list(tmp_path.glob("CANARY*")) and not list(Path.cwd().glob("CANARY*"))

    def test_hostile_details_when_posted_then_the_log_of_the_alert_step_holds_none_of_them(
        self, tmp_path: Path
    ) -> None:
        # The runner itself echoes the environment of a step before its script starts (see the test of
        # the export's first characters); the script prints no advisory text.
        details = "\n".join(
            [
                f"1. A: ::error::CANARY1 {OLD_MARKER}error]CANARY2",
                "::warning::CANARY3",
                f"{OLD_MARKER}group]CANARY4",
            ]
        )

        run = _run_alert_step(tmp_path, details)

        assert run.process.returncode == 0, _inert(run.log)
        assert "CANARY" not in run.log and OLD_MARKER not in run.log, _inert(run.log)
        assert not _runner_commands(run.log), _inert(run.log)

    def test_every_hostile_character_when_posted_then_the_body_holds_only_the_sanitized_text(
        self, tmp_path: Path
    ) -> None:
        # The same list as the audit step's log test, without the NUL byte that no environment
        # variable can hold.
        characters = [entry for entry in _log_characters() if entry[1] != "\x00"]
        details = "\n".join(
            f"{i}. A: b{i:03d}{char}a{i:03d}" for i, (_, char, _) in enumerate(characters)
        )

        run = _run_alert_step(tmp_path, details)

        assert run.process.returncode == 0, _inert(run.log)
        problems = []
        for i, (label, char, replacement) in enumerate(characters):
            expected = f"b{i:03d}{replacement}a{i:03d}"
            if char in run.body:
                problems.append(f"{label}: still present in the body")
            if expected not in run.body:
                problems.append(f"{label}: {expected!r} missing from the body")
        assert len(characters) > 250
        assert not problems, "\n".join(problems)

    def test_markdown_in_details_when_posted_then_only_constant_text_is_outside_the_fence(
        self, tmp_path: Path
    ) -> None:
        details = "\n".join(
            [
                "# Injected heading",
                "> quote",
                "---",
                "![img](http://x/y.png)",
                "[l](http://x)",
                "<img src=x onerror=y>",
                "@octocat",
                "::error::forged",
                f"{OLD_MARKER}error]forged",
                "```",
                "~~~",
                "````",
                "end",
            ]
        )

        run = _run_alert_step(tmp_path, details)

        kinds = _token_types(run.body)
        assert len(_fences(run.body)) == 1
        forbidden = {"html_block", "html_inline", "image", "link_open", "blockquote_open", "hr"}
        assert not forbidden & set(kinds), kinds
        assert kinds.count("heading_open") == 0

    @pytest.mark.parametrize("run_length", [3, 4, 5, 6, 100, 401])
    def test_backtick_runs_when_fenced_then_the_fence_is_longer_than_every_run(
        self, tmp_path: Path, run_length: int
    ) -> None:
        details = "Name Version\n" + "`" * run_length + "\ntext\n" + "`" * (run_length - 1)

        run = _run_alert_step(tmp_path, details)

        fences = _fences(run.body)
        assert len(fences) == 1 and len(fences[0].markup) > run_length
        assert fences[0].content == details + "\n"

    def test_very_long_backtick_line_when_posted_then_it_finishes_within_the_step_time_limit(
        self, tmp_path: Path
    ) -> None:
        # A per-character loop in awk is quadratic in some implementations; the run has a time limit.
        run = _run_alert_step(tmp_path, "`" * 7_000 + "\nafter")

        assert run.process.returncode == 0, _inert(run.log)
        assert len(run.body_path.read_bytes()) <= BODY_LIMIT and len(_fences(run.body)) == 1

    def test_header_when_posted_then_run_url_and_date_lines_are_present(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "row")

        lines = run.body.split("\n")
        assert f"**Scan run:** {RUN_URL}" in lines
        date_line = r"\*\*Date:\*\* \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ"
        assert any(re.fullmatch(date_line, line) for line in lines)
        assert any(line.startswith("**Remediation:**") for line in lines)

    def test_findings_when_posted_then_a_constant_note_before_the_fence_says_they_are_data(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text")

        lines = run.body.split("\n")
        fence_start = next(i for i, line in enumerate(lines) if line.startswith("````"))
        assert THIRD_PARTY_NOTE in lines and lines.index(THIRD_PARTY_NOTE) < fence_start
        assert THIRD_PARTY_NOTE not in _fences(run.body)[0].content

    def test_empty_details_when_posted_then_the_body_links_the_run_and_has_no_findings(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "")

        assert run.process.returncode == 0, _inert(run.log)
        assert f"[workflow run]({RUN_URL})" in run.body
        assert "pip-audit detected unfixed CVEs in the dependency tree" in run.body
        assert "Findings (pip-audit)" not in run.body and not _fences(run.body)

    def test_details_over_the_cap_when_posted_then_clipped_in_one_fence_with_the_notice_outside(
        self, tmp_path: Path
    ) -> None:
        cap = _constant(_alert_step()["run"], "MAX_DETAILS_BYTES")
        details = "\n".join(f"{i}. CVE-2026-{i:06d}: {'d' * 380}" for i in range(250))

        run = _run_alert_step(tmp_path, details)

        assert run.process.returncode == 0, _inert(run.log)
        assert len(run.body_path.read_bytes()) <= cap + 3_000
        fences = _fences(run.body)
        assert len(fences) == 1 and details.startswith(fences[0].content[:-1])
        assert len(fences[0].content) > cap - 1_000
        after_fence = run.body.split(fences[0].markup)[-1]
        assert f"[Findings clipped to fit GitHub limits. Full output: {RUN_URL}]" in after_fence
        assert "**Remediation:**" in after_fence, "the remediation paragraph survives the clip"

    @pytest.mark.parametrize(
        ("listed", "sentence"),
        [("1", CLIP_FINDINGS_LEFT_OUT), ("2", CLIP_TEXT_SHORTENED)],
        ids=["findings-left-out", "every-finding-listed"],
    )
    def test_export_with_its_clip_notice_when_posted_then_a_plain_sentence_follows_the_fence(
        self, tmp_path: Path, listed: str, sentence: str
    ) -> None:
        notice = (
            f"[clipped: findings: 2 total, {listed} listed; descriptions: 1 shown, 0 cut to 400 "
            "bytes, 1 omitted; for the full output, see the step summary or job log of the workflow "
            "run]"
        )
        details = "\n".join([_verdict(2), "Findings (2):", "1. CVE-2026-000000: text", notice])

        run = _run_alert_step(tmp_path, details)

        assert run.process.returncode == 0, _inert(run.log)
        fences = _fences(run.body)
        assert len(fences) == 1 and "[clipped: findings: 2 total" in fences[0].content
        after_fence = run.body.split(fences[0].markup)[-1]
        assert sentence in after_fence
        assert (
            run.body.count("[Findings clipped") + run.body.count("findings text was shortened") == 1
        )

    def test_export_without_a_clip_notice_when_posted_then_no_clip_sentence_is_added(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text")

        assert run.process.returncode == 0, _inert(run.log)
        assert "Findings clipped" not in run.body and "findings text was shortened" not in run.body

    def test_lines_over_the_line_cap_when_posted_then_they_are_cut_and_the_notice_says_so(
        self, tmp_path: Path
    ) -> None:
        limit = _constant(_alert_step()["run"], "MAX_LINE_BYTES")
        details = "1. A: " + "e" * 5_000 + "\n2. B: " + THREE_BYTES * 2_000 + "\n3. C: short"

        run = _run_alert_step(tmp_path, details)

        content = _fences(run.body)[0].content.split("\n")
        assert len(content[0].encode("utf-8")) == limit and content[2] == "3. C: short"
        assert content[1] == "2. B: " + THREE_BYTES * ((limit - 6) // 3), (
            "cut on bytes, not characters"
        )
        assert CLIP_TEXT_SHORTENED_HERE in run.body and "[Findings clipped" not in run.body

    @pytest.mark.parametrize("char", [TWO_BYTES, THREE_BYTES, FOUR_BYTES])
    def test_clip_inside_multibyte_character_when_posted_then_the_body_is_valid_utf8(
        self, tmp_path: Path, char: str
    ) -> None:
        cap = _constant(_alert_step()["run"], "MAX_DETAILS_BYTES")
        for offset in range(1, len(char.encode("utf-8"))):
            details = _short_lines_with_char_across(cap, char, offset)

            run = _run_alert_step(tmp_path / f"o{offset}", details)

            assert run.process.returncode == 0, _inert(run.log)
            assert "Findings clipped" in run.body  # `body` decodes as strict UTF-8

    def test_iconv_failing_when_posted_then_the_ascii_fallback_body_is_posted(
        self, tmp_path: Path
    ) -> None:
        details = f"1. A: caf{TWO_BYTES} {THREE_BYTES} text"

        run = _run_alert_step(tmp_path, details, stubs={"iconv": _failing_tool("iconv")})

        assert run.process.returncode == 0, _inert(run.log)
        assert run.body.isascii() and "1. A: caf" in run.body and "text" in run.body
        assert DEGRADED in run.log

    @pytest.mark.parametrize("printed", ["garbage", "```", ""], ids=["garbage", "short", "empty"])
    def test_fence_tool_printing_no_valid_fence_when_posted_then_the_body_links_to_the_run(
        self, tmp_path: Path, printed: str
    ) -> None:
        fake_awk = f"#!/usr/bin/env bash\ncat > /dev/null\nprintf '%s' '{printed}'\n"

        run = _run_alert_step(tmp_path, "1. A: text", stubs={"awk": fake_awk})

        assert run.process.returncode == 0, _inert(run.log)
        assert not _fences(run.body) and f"[workflow run]({RUN_URL})" in run.body
        assert "1. A: text" not in run.body and DEGRADED in run.log

    @pytest.mark.parametrize("tool", ["awk", "cut", "head", "iconv", "sed", "tr"])
    def test_tool_failing_when_posted_then_an_issue_comment_with_the_run_link_is_still_posted(
        self, tmp_path: Path, tool: str
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", stubs={tool: _failing_tool(tool)})

        assert run.process.returncode == 0, _inert(run.log)
        assert run.posts and run.posts[-1].startswith("comment file ")
        assert RUN_URL in run.body and DEGRADED in run.log


class TestAlertStepPosting:
    """Which ``gh`` calls are made, in which order, and what is said when something fails."""

    def test_no_open_issue_when_posted_then_the_issue_is_created_from_the_body_file(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing="")

        assert run.process.returncode == 0, _inert(run.log)
        create = next(call for call in run.calls if call[:2] == ["issue", "create"])
        assert create[create.index("--title") + 1] == ISSUE_TITLE
        assert create[create.index("--label") + 1] == "security-alert"
        assert "--body-file" in create
        assert run.posts == [f"create file {len(run.body_path.read_bytes())}"]
        assert "Created new CVE alert issue" in run.log

    @pytest.mark.parametrize(
        ("label_fails", "file_rejected", "number"),
        [("0", "0", 401), ("0", "1", 402), ("1", "0", 403), ("1", "1", 404)],
        ids=["labelled-file", "labelled-short", "unlabelled-file", "unlabelled-short"],
    )
    def test_issue_created_when_posting_then_the_log_gives_its_address(
        self, tmp_path: Path, label_fails: str, file_rejected: str, number: int
    ) -> None:
        run = _run_alert_step(
            tmp_path,
            "1. A: text",
            existing="",
            create_with_label_fail=label_fails,
            reject_bodyfile=file_rejected,
        )

        assert run.process.returncode == 0, _inert(run.log)
        assert f"https://example.test/example/example/issues/{number}" in run.log, _inert(run.log)

    def test_label_missing_when_creating_then_it_is_made_like_the_live_label(
        self, tmp_path: Path
    ) -> None:
        # The label as GitHub holds it, read with `gh label list` on 2026-11-12.
        run = _run_alert_step(tmp_path, "1. A: text", existing="")

        create = next(call for call in run.calls if call[:2] == ["label", "create"])
        assert create[create.index("--color") + 1] == "B60205"
        description = create[create.index("--description") + 1]
        assert description == "Automated CVE alert from scheduled security scan"

    def test_label_missing_when_creating_then_the_label_is_created_first(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing="", refuse_label="1")

        assert run.process.returncode == 0, _inert(run.log)
        verbs = run.verbs()
        assert "label create" in verbs and "issue create" in verbs, verbs
        assert verbs.index("label create") < verbs.index("issue create")
        create = next(call for call in run.calls if call[:2] == ["issue", "create"])
        assert "--label" in create and run.posts[-1].startswith("create file ")

    def test_label_cannot_be_created_when_creating_then_an_unlabelled_issue_keeps_the_findings(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(
            tmp_path, "1. A: text", existing="", refuse_label="1", label_create_fail="1"
        )

        assert run.process.returncode == 0, _inert(run.log)
        creates = [call for call in run.calls if call[:2] == ["issue", "create"]]
        # Both labelled attempts come first; only then is the label dropped.
        assert len(creates) == 3
        assert "--label" in creates[0] and "--label" in creates[1] and "--label" not in creates[2]
        assert (
            "--body-file" in creates[0] and "--body" in creates[1] and "--body-file" in creates[2]
        )
        assert run.posts[-1].startswith("create file ") and "1. A: text" in run.body
        assert "::warning::" in run.log and "Created new CVE alert issue" not in run.log
        last_warning = run.log.split("::warning::")[-1]
        assert "label" in last_warning and "by its title" in last_warning
        # The label is added afterwards (here the stand-in refuses it, so only a warning remains).
        edits = [call for call in run.calls if call[:2] == ["issue", "edit"]]
        assert [call[2] for call in edits] == ["403"] and "--add-label" in edits[0]

    def test_first_create_failing_for_another_reason_when_creating_then_the_label_is_kept(
        self, tmp_path: Path
    ) -> None:
        # The labelled issue is what the next scan looks for: a failure that has nothing to do with the
        # label must not leave an unlabelled one.
        run = _run_alert_step(tmp_path, "1. A: text", existing="", fail_first_create="1")

        assert run.process.returncode == 0, _inert(run.log)
        creates = [call for call in run.calls if call[:2] == ["issue", "create"]]
        assert len(creates) == 2 and all("--label" in call for call in creates)
        assert "--body-file" in creates[0] and "--body" in creates[1]
        assert run.posts[-1].startswith("create inline ") and "issue edit" not in run.verbs()
        assert "short fallback text" in run.log.split("::warning::")[-1]

    def test_label_refused_by_every_create_when_creating_then_it_is_added_afterwards(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing="", create_with_label_fail="1")

        assert run.process.returncode == 0, _inert(run.log)
        creates = [call for call in run.calls if call[:2] == ["issue", "create"]]
        assert len(creates) == 3 and "--label" not in creates[-1]
        edit = next(call for call in run.calls if call[:2] == ["issue", "edit"])
        assert edit[2] == "403" and edit[edit.index("--add-label") + 1] == "security-alert"
        assert "Added the 'security-alert' label to issue #403" in run.log

    def test_open_issue_without_the_label_when_posting_then_it_is_found_by_its_title(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing="", existing_by_title="391")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.verbs() == ["issue list", "issue list", "issue comment"], run.verbs()
        by_label, by_title, comment = run.calls
        assert "--label" in by_label and "--search" in by_title and "--label" not in by_title
        assert by_title[by_title.index("--state") + 1] == "open"
        assert ISSUE_TITLE in by_title[by_title.index("--search") + 1]
        assert comment[2] == "391" and run.posts == [
            f"comment file {len(run.body_path.read_bytes())}"
        ]
        assert "Updated existing CVE alert issue #391" in run.log

    def test_title_search_failing_when_posting_then_a_warning_is_printed_and_the_alert_is_created(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing="", search_fail="1")

        assert run.process.returncode == 0, _inert(run.log)
        assert "by title" in run.log.split("::warning::")[1]
        assert run.posts[-1].startswith("create file ")

    def test_labelled_lookup_with_a_result_when_posting_then_the_title_is_not_searched(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing="385", existing_by_title="391")

        assert run.verbs() == ["issue list", "issue comment"] and run.calls[-1][2] == "385"

    def test_no_open_issue_when_body_file_rejected_then_a_short_issue_is_created_with_warning(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing="", reject_bodyfile="1")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.posts and run.posts[-1].startswith("create inline ")
        assert "pip-audit found unfixed vulnerabilities" in run.body and RUN_URL in run.body
        assert "1. A: text" not in run.body
        assert "::warning::" in run.log and "Created new CVE alert issue" not in run.log
        creates = [call for call in run.calls if call[:2] == ["issue", "create"]]
        assert all("--label" in call for call in creates), "the label stays on a labelled attempt"

    def test_body_file_rejected_when_commenting_then_the_short_text_is_posted_with_warning(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", reject_bodyfile="1")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.posts and run.posts[-1].startswith("comment inline ")
        assert "::warning::Could not post the findings to issue #385" in run.log
        assert "short fallback text" in run.log
        assert "Updated existing CVE alert issue" not in run.log

    @pytest.mark.parametrize("existing", ["385", ""])
    def test_every_post_rejected_when_posting_then_the_step_fails_with_an_error(
        self, tmp_path: Path, existing: str
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", existing=existing, reject_all="1")

        assert run.process.returncode != 0
        assert "::error::Could not" in run.log and not run.posts

    def test_issue_list_failing_when_posting_then_a_warning_is_printed_and_the_alert_is_created(
        self, tmp_path: Path
    ) -> None:
        run = _run_alert_step(tmp_path, "1. A: text", list_fail="1")

        assert run.process.returncode == 0, _inert(run.log)
        assert DEGRADED in run.log and run.posts[-1].startswith("create ")
        assert run.verbs().count("issue list") == 1, "a failed lookup is not searched again"


class TestLiveAlertIssue:
    """The steps find the alert issue as GitHub holds it, act on it, and open no second one.

    The ``gh`` double holds the issues of ``LIVE_ALERT`` (issue 434: open, labelled ``security-alert``,
    opened by the scan) and ``EARLIER_ALERT`` (issue 385: closed, same title and label) and answers
    ``issue list`` from them, so a title, a label or a search that does not match what GitHub holds
    finds nothing and the step takes the create path.
    """

    def test_open_alert_issue_when_posting_then_it_gets_one_comment_and_no_issue_is_created(
        self, tmp_path: Path
    ) -> None:
        issues = _held_issues(tmp_path, EARLIER_ALERT, LIVE_ALERT)

        run = _run_alert_step(tmp_path, "1. A: text", existing="", issues=issues)

        assert run.process.returncode == 0, _inert(run.log)
        comments = [call for call in run.calls if call[:2] == ["issue", "comment"]]
        assert [call[2] for call in comments] == ["434"] and "--body-file" in comments[0]
        assert run.verbs() == ["issue list", "issue comment"], "found by its label, then commented"
        assert run.posts == [f"comment file {len(run.body_path.read_bytes())}"]
        assert "Updated existing CVE alert issue #434" in run.log

    def test_open_alert_issue_without_the_label_when_posting_then_the_title_search_finds_it(
        self, tmp_path: Path
    ) -> None:
        unlabelled = (434, "open", ISSUE_TITLE, "", "app/github-actions")
        issues = _held_issues(tmp_path, EARLIER_ALERT, unlabelled)

        run = _run_alert_step(tmp_path, "1. A: text", existing="", issues=issues)

        assert run.process.returncode == 0, _inert(run.log)
        assert run.verbs() == ["issue list", "issue list", "issue comment"], run.verbs()
        by_label, by_title = run.calls[0], run.calls[1]
        assert "--label" in by_label and "--search" in by_title and "--label" not in by_title
        assert [call[2] for call in run.calls if call[:2] == ["issue", "comment"]] == ["434"]
        assert "Updated existing CVE alert issue #434" in run.log

    @pytest.mark.parametrize("labels", [ISSUE_LABEL, ""], ids=["labelled", "unlabelled"])
    def test_issue_with_a_similar_title_when_posting_then_only_the_exact_title_is_commented(
        self, tmp_path: Path, labels: str
    ) -> None:
        similar = (500, "open", f"{ISSUE_TITLE} (old)", labels, "someone")
        issues = _held_issues(
            tmp_path, similar, (434, "open", ISSUE_TITLE, labels, "app/github-actions")
        )

        run = _run_alert_step(tmp_path, "1. A: text", existing="", issues=issues)

        assert run.process.returncode == 0, _inert(run.log)
        assert [call[2] for call in run.calls if call[:2] == ["issue", "comment"]] == ["434"]
        assert "issue create" not in run.verbs()

    def test_only_a_closed_alert_issue_when_posting_then_a_new_labelled_issue_is_created(
        self, tmp_path: Path
    ) -> None:
        # What happens on the first scan with findings after the live alert issue has been closed.
        run = _run_alert_step(
            tmp_path, "1. A: text", existing="", issues=_held_issues(tmp_path, EARLIER_ALERT)
        )

        assert run.process.returncode == 0, _inert(run.log)
        assert run.verbs() == ["issue list", "issue list", "label create", "issue create"]
        create = run.calls[-1]
        assert create[create.index("--title") + 1] == ISSUE_TITLE
        assert create[create.index("--label") + 1] == ISSUE_LABEL and "--body-file" in create
        assert "Created new CVE alert issue" in run.log

    def test_open_alert_issue_when_the_scan_is_clean_then_only_that_issue_is_closed(
        self, tmp_path: Path
    ) -> None:
        issues = _held_issues(tmp_path, EARLIER_ALERT, LIVE_ALERT)

        run = _run_close_step(tmp_path, existing="", issues=issues)

        assert run.process.returncode == 0, _inert(run.log)
        assert run.verbs() == ["issue list", "issue close"] and run.calls[-1][2] == "434"

    def test_open_alert_issue_without_the_label_when_the_scan_is_clean_then_it_is_found_by_title(
        self, tmp_path: Path
    ) -> None:
        unlabelled = (434, "open", ISSUE_TITLE, "", "app/github-actions")
        issues = _held_issues(tmp_path, EARLIER_ALERT, unlabelled)

        run = _run_close_step(tmp_path, existing="", issues=issues)

        assert run.process.returncode == 0, _inert(run.log)
        assert run.verbs() == ["issue list", "issue list", "issue close"], run.verbs()
        assert run.calls[-1][2] == "434"

    @pytest.mark.parametrize("step", ["alert", "close"])
    def test_title_search_when_called_then_it_is_the_quoted_title_in_titles_only(
        self, tmp_path: Path, step: str
    ) -> None:
        unlabelled = _held_issues(tmp_path, (434, "open", ISSUE_TITLE, "", "app/github-actions"))
        if step == "alert":
            run = _run_alert_step(tmp_path, "1. A: text", existing="", issues=unlabelled)
        else:
            run = _run_close_step(tmp_path, existing="", issues=unlabelled)

        assert run.process.returncode == 0, _inert(run.log)
        by_title = run.calls[1]
        assert by_title[:2] == ["issue", "list"]
        assert by_title[by_title.index("--search") + 1] == f'"{ISSUE_TITLE}" in:title'
        assert by_title[by_title.index("--state") + 1] == "open"
        assert by_title[by_title.index("--limit") + 1] == "100" and "--label" not in by_title

    @pytest.mark.parametrize("step", ["alert", "close"])
    def test_lookups_when_called_then_only_the_title_search_keeps_the_scans_own_issues(
        self, tmp_path: Path, step: str
    ) -> None:
        unlabelled = _held_issues(tmp_path, (434, "open", ISSUE_TITLE, "", "app/github-actions"))
        if step == "alert":
            run = _run_alert_step(tmp_path, "1. A: text", existing="", issues=unlabelled)
        else:
            run = _run_close_step(tmp_path, existing="", issues=unlabelled)

        assert run.process.returncode == 0, _inert(run.log)
        by_label, by_title = run.calls[0], run.calls[1]
        assert by_label[by_label.index("--json") + 1] == "number,title"
        assert "author" not in by_label[by_label.index("--jq") + 1]
        assert by_title[by_title.index("--json") + 1] == "number,title,author"
        assert '.author.login == "app/github-actions"' in by_title[by_title.index("--jq") + 1]

    @pytest.mark.parametrize("step", ["alert", "close"])
    def test_unlabelled_issue_with_the_alert_title_from_someone_else_when_looked_up_then_untouched(
        self, tmp_path: Path, step: str
    ) -> None:
        # Anyone can open an issue with the exact title.  Without the label it is found only by the
        # search by title, which keeps the issues that the scan's own token opened.
        decoy = (500, "open", ISSUE_TITLE, "", "someone")
        issues = _held_issues(tmp_path, EARLIER_ALERT, decoy)
        if step == "alert":
            run = _run_alert_step(tmp_path, "1. A: text", existing="", issues=issues)
        else:
            run = _run_close_step(tmp_path, existing="", issues=issues)

        assert run.process.returncode == 0, _inert(run.log)
        touched = [
            call for call in run.calls if call[1:3] in (["comment", "500"], ["close", "500"])
        ]
        assert not touched, touched
        if step == "alert":
            assert run.verbs()[-1] == "issue create", run.verbs()
        else:
            assert "No open CVE alert issue to close" in run.log

    def test_title_and_label_when_read_from_the_scripts_then_they_are_those_of_the_live_issue(
        self,
    ) -> None:
        for step in (_alert_step(), _close_step()):
            assert f'ISSUE_TITLE="{ISSUE_TITLE}"' in step["run"]
            assert f'LABEL="{ISSUE_LABEL}"' in step["run"]
            assert f'ALERT_AUTHOR="{LIVE_ALERT[4]}"' in step["run"]


class TestAuditExportFeedsTheAlertStep:
    """The export of the audit step is what the alert step posts, end to end."""

    def test_34_findings_when_the_export_is_posted_then_one_comment_within_the_limit(
        self, tmp_path: Path
    ) -> None:
        audit = _run_audit_step(tmp_path / "audit", _table(rows=34, width=6_000))
        assert audit.details, _inert(audit.log)

        alert = _run_alert_step(tmp_path / "alert", audit.details)

        assert alert.process.returncode == 0, _inert(alert.log)
        assert alert.posts == [f"comment file {len(alert.body_path.read_bytes())}"]
        assert len(alert.body_path.read_bytes()) <= BODY_LIMIT
        fences = _fences(alert.body)
        assert len(fences) == 1 and "pkg033" in fences[0].content
        assert fences[0].content.strip().split("\n")[-1].startswith("[clipped:"), (
            "the notice of the export is inside the fence"
        )
        # The export lists every finding and cut only descriptions, so the plain sentence after the
        # fence says that some of the text was shortened, not that findings were clipped.
        sentence = CLIP_TEXT_SHORTENED
        assert alert.body.count(sentence) == 1 and "[Findings clipped" not in alert.body
        assert sentence in alert.body.split(fences[0].markup)[-1], "the sentence follows the fence"
        assert audit.details.split("\n")[0] == _verdict(34)


class TestCloseStep:
    """The close step closes the alert issue after a scan without findings."""

    def test_clean_scan_when_closing_then_the_comment_states_the_scan_result_only(
        self, tmp_path: Path
    ) -> None:
        run = _run_close_step(tmp_path)

        assert run.process.returncode == 0, _inert(run.log)
        close = next(call for call in run.calls if call[:2] == ["issue", "close"])
        comment = close[close.index("--comment") + 1]
        wording = r"pip-audit reports no known vulnerabilities as of \d{4}-\d\d-\d\d"
        assert re.search(wording, comment) and RUN_URL in comment
        assert "clean" not in comment.lower()

    def test_issue_list_when_closing_then_the_limit_is_raised_like_in_the_alert_step(
        self, tmp_path: Path
    ) -> None:
        run = _run_close_step(tmp_path)

        first = run.calls[0]
        assert first[:2] == ["issue", "list"] and first[first.index("--limit") + 1] == "100"

    def test_issue_list_failing_when_closing_then_a_warning_is_printed_and_nothing_is_closed(
        self, tmp_path: Path
    ) -> None:
        run = _run_close_step(tmp_path, list_fail="1")

        assert run.process.returncode == 0, _inert(run.log)
        assert DEGRADED in run.log and "issue close" not in run.verbs()
        assert "No open CVE alert issue to close" not in run.log, "a failed lookup is not 'none'"

    def test_several_open_alert_issues_when_closing_then_the_first_one_is_closed(
        self, tmp_path: Path
    ) -> None:
        run = _run_close_step(tmp_path, existing="385\n390")

        closes = [call for call in run.calls if call[:2] == ["issue", "close"]]
        assert run.process.returncode == 0 and [call[2] for call in closes] == ["385"]

    def test_no_open_issue_when_closing_then_nothing_is_closed(self, tmp_path: Path) -> None:
        run = _run_close_step(tmp_path, existing="")

        assert run.process.returncode == 0 and "issue close" not in run.verbs()
        assert "No open CVE alert issue to close" in run.log

    def test_open_issue_without_the_label_when_closing_then_it_is_found_by_its_title(
        self, tmp_path: Path
    ) -> None:
        run = _run_close_step(tmp_path, existing="", existing_by_title="391")

        assert run.process.returncode == 0, _inert(run.log)
        assert run.verbs() == ["issue list", "issue list", "issue close"], run.verbs()
        assert "--search" in run.calls[1] and run.calls[-1][2] == "391"

    def test_title_search_failing_when_closing_then_a_warning_is_printed_and_nothing_is_closed(
        self, tmp_path: Path
    ) -> None:
        run = _run_close_step(tmp_path, existing="", search_fail="1")

        assert run.process.returncode == 0, _inert(run.log)
        assert DEGRADED in run.log and "issue close" not in run.verbs()
        assert "No open CVE alert issue to close" not in run.log, "a failed search is not 'none'"


def _event_env(tmp_path: Path, event: str) -> dict[str, str]:
    """The variables that the runner sets for a run started by ``event``, with an event file."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    if event == "schedule":
        payload, ref = {"schedule": "0 6 * * *"}, "main"
    else:
        payload, ref = (
            {"inputs": None, "ref": "refs/heads/ci/bound-security-alert"},
            "ci/bound-security-alert",
        )
    event_file = tmp_path / "event.json"
    event_file.write_text(json.dumps(payload), encoding="utf-8")
    return {
        "GITHUB_EVENT_NAME": event,
        "GITHUB_EVENT_PATH": str(event_file),
        "GITHUB_REF": f"refs/heads/{ref}",
        "GITHUB_REF_NAME": ref,
        "GITHUB_ACTOR": "geekatron",
        "GITHUB_TRIGGERING_ACTOR": "geekatron",
    }


def _observed(run: AlertRun) -> tuple[list[list[str]], list[str], str, list[str]]:
    """What a run of the alert or close step did, without what differs from run to run."""

    def plain(text: str) -> str:
        text = re.sub(r"\S*/body\.md\b", "<body file>", text)
        return re.sub(r"\d{4}-\d\d-\d\d(T\d\d:\d\d:\d\dZ)?", "<date>", text)

    calls = [[plain(arg) for arg in call] for call in run.calls]
    body = plain(run.body_path.read_text(encoding="utf-8")) if run.body_path.exists() else ""
    messages = [plain(line) for line in run.log.splitlines() if line]
    return calls, run.posts, body, messages


class TestStartedByHand:
    """A scan started by hand (``workflow_dispatch``) takes the same path as a scheduled one.

    Each step runs once as the runner would start it for each event (the event name, the ref and the
    actor differ; the event file differs) and the two runs must do the same: the same ``gh`` calls in
    the same order, the same post, the same messages.
    """

    @pytest.mark.parametrize("existing", ["385", ""], ids=["comment", "create"])
    def test_alert_step_when_started_by_hand_then_it_does_what_a_scheduled_run_does(
        self, tmp_path: Path, existing: str
    ) -> None:
        observed = {}
        for event in ("schedule", "workflow_dispatch"):
            where = tmp_path / event
            run = _run_alert_step(
                where, "1. A: text", existing=existing, env=_event_env(where, event)
            )
            assert run.process.returncode == 0, _inert(run.log)
            observed[event] = _observed(run)

        assert observed["workflow_dispatch"] == observed["schedule"]
        assert observed["schedule"][1], "the step posted something"

    @pytest.mark.parametrize("existing", ["385", ""], ids=["close", "nothing-to-close"])
    def test_close_step_when_started_by_hand_then_it_does_what_a_scheduled_run_does(
        self, tmp_path: Path, existing: str
    ) -> None:
        observed = {}
        for event in ("schedule", "workflow_dispatch"):
            where = tmp_path / event
            run = _run_close_step(where, existing=existing, env=_event_env(where, event))
            assert run.process.returncode == 0, _inert(run.log)
            observed[event] = _observed(run)

        assert observed["workflow_dispatch"] == observed["schedule"]
        assert observed["schedule"][0], "the step called gh"

    def test_audit_step_when_started_by_hand_then_it_exports_what_a_scheduled_run_exports(
        self, tmp_path: Path
    ) -> None:
        observed = {}
        for event in ("schedule", "workflow_dispatch"):
            where = tmp_path / event
            run = _run_audit_step(
                where, _table(rows=4, width=300), env_extra=_event_env(where, event)
            )
            messages = [
                line for line in run.log.splitlines() if line.startswith(("::warning", "::error"))
            ]
            observed[event] = (run.process.returncode, run.outputs, run.summary, messages)

        assert observed["workflow_dispatch"] == observed["schedule"]
        assert observed["schedule"][1].get("vuln-found") == "true"


class TestWorkflowStructure:
    """Properties of the YAML that the behaviour tests cannot see."""

    def test_advisory_text_when_passed_to_the_alert_step_then_only_through_the_environment(
        self,
    ) -> None:
        step = _alert_step()

        assert "vuln-details" in step["env"]["VULN_DETAILS"]
        assert "${{" not in step["run"] and "${{" not in _close_step()["run"]

    def test_shell_when_read_from_the_yaml_then_it_matches_the_flags_the_harness_uses(self) -> None:
        assert _audit_step()["shell"] == "bash"  # runs as: bash --noprofile --norc -eo pipefail
        assert "shell" not in _alert_step() and "shell" not in _close_step()  # runs as: bash -e

    def test_workflow_permissions_when_parsed_then_they_are_unchanged(self) -> None:
        doc = yaml.safe_load(WORKFLOW_FILE.read_text(encoding="utf-8"))

        assert doc["permissions"] == {"contents": "read", "issues": "write"}
        assert all("permissions" not in job for job in doc["jobs"].values())

    def test_step_conditions_when_read_from_the_yaml_then_a_clean_scan_stays_quiet(self) -> None:
        # The alert step runs after a failed audit step (always()), but only when the audit found
        # something; the close step only when it found nothing.  Without a verdict, neither runs.
        assert _alert_step()["if"] == "always() && steps.audit.outputs.vuln-found == 'true'"
        assert _close_step()["if"] == "always() && steps.audit.outputs.vuln-found == 'false'"

    def test_audit_outputs_and_inputs_when_read_from_the_yaml_then_the_steps_can_rely_on_them(
        self,
    ) -> None:
        action = yaml.safe_load(ACTION_FILE.read_text(encoding="utf-8"))
        audit = _step(WORKFLOW_FILE, name="Run security audit")

        assert {"vuln-found", "clean", "vuln-details"} <= set(action["outputs"])
        assert audit["id"] == "audit" and audit["with"]["fail-on-vuln"] == "true"
        assert _alert_step()["env"]["VULN_DETAILS"] == "${{ steps.audit.outputs.vuln-details }}"

    def test_scan_runs_when_read_from_the_yaml_then_two_of_them_never_overlap(self) -> None:
        # Two runs at once (the daily one and a manual one) could both find no open alert issue and
        # both create one.  A run that has to wait is not cancelled by the running one.  If a newer run
        # queues while it waits, GitHub replaces the waiting one; the newer one does the same work.
        doc = yaml.safe_load(WORKFLOW_FILE.read_text(encoding="utf-8"))

        assert doc["concurrency"] == {"group": "security-scan", "cancel-in-progress": False}

    def test_scan_job_when_read_from_the_yaml_then_it_has_a_time_limit(self) -> None:
        # The 30 newest scans took 27 to 52 seconds (read on 2026-11-12).  Without a limit a stuck scan
        # runs for six hours, GitHub's default, and holds the concurrency group, so later scans wait.
        doc = yaml.safe_load(WORKFLOW_FILE.read_text(encoding="utf-8"))

        assert doc["jobs"]["pip-audit"]["timeout-minutes"] == 15

    def test_triggers_and_expressions_when_read_from_the_yaml_then_nothing_reads_how_the_run_started(
        self,
    ) -> None:
        # A scan started by hand must take the same path as the scheduled one: the same lookup, the
        # same posts, the same close.  So the manual trigger takes no input, and no step of the job
        # or of the action reads the event, the ref or the actor, in a condition or in a script.
        doc = yaml.safe_load(WORKFLOW_FILE.read_text(encoding="utf-8"))
        triggers = doc.get("on", doc.get(True))  # YAML 1.1 reads the key `on` as the boolean True
        assert set(triggers) == {"schedule", "workflow_dispatch"}
        assert not (triggers["workflow_dispatch"] or {}).get("inputs")
        assert all("if" not in job for job in doc["jobs"].values())
        action = yaml.safe_load(ACTION_FILE.read_text(encoding="utf-8"))
        steps = [step for job in doc["jobs"].values() for step in job["steps"]]
        steps += action["runs"]["steps"]
        reads = re.compile(
            r"github\.(event|ref|head_ref|base_ref|actor|triggering_actor)"
            r"|GITHUB_(EVENT|REF|HEAD_REF|BASE_REF|ACTOR|TRIGGERING_ACTOR)"
            r"|workflow_dispatch|\bschedule\b"
        )
        for step in steps:
            for key in ("if", "env", "with", "run"):
                found = reads.search(json.dumps(step.get(key, "")))
                assert not found, (
                    f"step {step.get('name')!r} reads {found.group(0)!r} in its {key!r}"
                )

    def test_messages_when_read_from_the_scripts_then_none_claims_the_findings_are_in_a_log(
        self,
    ) -> None:
        # The step summary and the job log hold the output in different states of the audit step (no
        # random token: no log copy; no sanitizer: a note instead of the text), so a message may point
        # to them but not say that the findings are there.
        claim = re.compile(
            r"\b(?:is|are) in (?:the |this )?(?:workflow )?(?:run |job )?log\b", re.I
        )
        for script in (_audit_step()["run"], _alert_step()["run"], _close_step()["run"]):
            assert not claim.findall(script)

    def test_sanitizer_lists_when_compared_then_the_two_copies_are_identical(self) -> None:
        action, workflow = (
            _sanitize_sed_lines(_audit_step()["run"]),
            _sanitize_sed_lines(_alert_step()["run"]),
        )

        assert len(action) >= 13 and action == workflow


class TestSanitizerList:
    """The sed program of both sanitizers removes every default-ignorable code point, and no more."""

    # Removed or replaced as well, so they are not "neighbours that must survive".
    OTHER_CHANGES = [(0x80, 0x9F), (0x2028, 0x2029), (0x2800, 0x2800), (0xFFF9, 0xFFFB)]

    @pytest.mark.parametrize("step", ["audit", "alert"])
    def test_every_default_ignorable_code_point_when_filtered_then_it_is_removed(
        self, step: str
    ) -> None:
        script = (_audit_step if step == "audit" else _alert_step)()["run"]
        points = [code for low, high in DEFAULT_IGNORABLE for code in range(low, high + 1)]
        lines = "".join(f"<{chr(code)}>\n" for code in points)

        filtered = _sed_filter(script, lines.encode("utf-8")).decode("utf-8").split("\n")

        survivors = [
            f"U+{code:04X}"
            for code, line in zip(points, filtered[:-1], strict=True)
            if line != "<>"
        ]
        assert len(points) > 4_000 and not survivors, survivors[:20]

    @pytest.mark.parametrize("step", ["audit", "alert"])
    def test_characters_next_to_the_ranges_when_filtered_then_they_are_kept(
        self, step: str
    ) -> None:
        script = (_audit_step if step == "audit" else _alert_step)()["run"]
        changed = [*DEFAULT_IGNORABLE, *self.OTHER_CHANGES]
        neighbours = sorted(
            {
                code
                for low, high in DEFAULT_IGNORABLE
                for code in (low - 1, high + 1)
                if not any(a <= code <= b for a, b in changed)
            }
        )
        prose = (
            "caf\u00e9 \u4e2d\u6587 \U0001f600 \u03a9\u03bc\u03ad\u03b3\u03b1 "
            "\uac00\ub098 \u30ab\u30bf\u30ab\u30ca e\u0301"
        )
        lines = "".join(f"<{chr(code)}>\n" for code in neighbours) + prose + "\n"

        filtered = _sed_filter(script, lines.encode("utf-8")).decode("utf-8")

        assert filtered == lines
        assert len(neighbours) > 20

    @pytest.mark.parametrize("step", ["audit", "alert"])
    def test_other_changes_when_filtered_then_the_ranges_are_removed_or_become_spaces(
        self, step: str
    ) -> None:
        script = (_audit_step if step == "audit" else _alert_step)()["run"]
        cases = {0x85: " ", 0x2028: " ", 0x2029: " ", 0x2800: " ", 0x80: "", 0x9F: "", 0xFFF9: ""}
        lines = "".join(f"<{chr(code)}>\n" for code in cases)

        filtered = _sed_filter(script, lines.encode("utf-8")).decode("utf-8").split("\n")

        assert filtered[:-1] == [f"<{replacement}>" for replacement in cases.values()]


class TestPreconditions:
    """The openssl precondition: a skip locally, a failure on CI (so CI cannot skip silently)."""

    def test_openssl_missing_when_not_on_ci_then_the_precondition_skips(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(shutil, "which", lambda _name: None)
        monkeypatch.delenv("CI", raising=False)

        with pytest.raises(pytest.skip.Exception, match="openssl"):
            _require_openssl()

    def test_openssl_missing_when_on_ci_then_the_precondition_fails(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(shutil, "which", lambda _name: None)
        monkeypatch.setenv("CI", "true")

        with pytest.raises(pytest.fail.Exception, match="openssl"):
            _require_openssl()

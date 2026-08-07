# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Shared CLI project-root and containment-root resolution (BUG-010, GH #337).

Single source of truth for resolving the USER'S project root across CLI
namespaces (``config``, ``ast``, ...). Never anchors to the Jerry
installation's own directory tree, so commands operate on the user's
repository regardless of where Jerry is installed (plugin checkout,
marketplace install, or development clone).

Also provides ``get_containment_roots()`` (BUG-010 scope widening, PR #341
owner review, 2026-08-07): the default set of allowed ``jerry ast`` path
containment roots widens from the single project root to include OS
temp/scratchpad directories (covering Claude Code scratchpad writes), and
an explicit ``--root`` CLI flag makes the allowed set *exactly* that one
resolved directory -- a user-discretion exclusive override so ``jerry ast``
can be pointed anywhere the user chooses.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path, PurePath

#: Hard-coded macOS/Linux scratchpad root (BUG-010 scope widening).
#:
#: Private, monkeypatchable seam: intentionally NOT resolved or
#: existence-checked at import time -- both happen inside
#: ``get_containment_roots()`` at call time, so tests can override this
#: per-test without needing to fake filesystem-level ``/tmp``
#: non-existence (which is not reliably mockable across
#: ``os.path.exists``/``Path.exists`` call sites).
#:
#: Rationale for registering this alongside ``tempfile.gettempdir()``: on
#: macOS, ``tempfile.gettempdir()`` resolves under ``$TMPDIR``
#: (``/var/folders/...``), while Claude Code's scratchpad directories live
#: under ``/tmp/claude-*`` (canonically ``/private/tmp/...``) -- a
#: different tree. Registering both covers both locations without
#: hard-coding Claude-specific paths.
_HARDCODED_TMP: Path = Path("/tmp")


def get_project_root() -> Path:
    """Resolve the user's project root directory.

    Resolution order:
        1. ``CLAUDE_PROJECT_DIR`` environment variable (set by Claude Code
           for the active workspace). An empty value is treated as unset.
        2. The current working directory.

    Returns:
        Path to the user's project root.
    """
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)
    return Path.cwd()


def _is_broad_containment_root(resolved: PurePath) -> bool:
    """Return True when ``resolved`` is an unusually broad containment root.

    "Broad" means the filesystem/drive root itself -- detected portably via
    ``PurePath.parts`` rather than a hard-coded ``/`` so this works
    identically for POSIX roots (``/``) and Windows drive roots
    (``C:\\``, ``D:\\``, ...) -- or an ANCESTOR OF (or equal to) the user's
    home directory (H-02/H-08 red-team remediation, RED-BUG010, CWE-1284-
    adjacent incomplete-allowlist gap). The original check only flagged the
    exact home directory, missing well-known multi-user parents such as
    ``/home``, ``/Users``, and ``C:\\Users`` -- each of these contains
    *every* user's home directory on the host, making containment just as
    effectively disabled as a bare filesystem root, even though none of
    them is the filesystem root or the exact home directory itself.

    The ancestor check is deliberately dynamic (derived from the actual
    ``Path.home()`` at call time) rather than a hard-coded, platform-
    specific path list: it uses ``PurePath.relative_to()``, which works
    identically for POSIX paths and ``PureWindowsPath`` instances, so a
    single check covers ``/home``, ``/Users``, ``C:\\Users``, and any
    other ancestor of the resolved home directory without enumerating
    well-known paths by name.

    Args:
        resolved: An already-resolved, absolute path to check. Accepts any
            ``PurePath`` (not just the platform-native ``Path``) so pure
            cross-platform anchor detection can be unit tested without
            requiring the host OS to match the path flavor under test.

    Returns:
        True when the path is a filesystem/drive root, the home directory
        itself, or an ancestor of the home directory.
    """
    if len(resolved.parts) <= 1:
        return True
    try:
        home = Path.home().resolve()
    except (RuntimeError, OSError):
        # Home directory cannot be determined on this system/environment;
        # a resolvable path can never equal an undeterminable home, so it
        # is not broad via this criterion.
        return False
    if resolved == home:
        return True
    # Ancestor-of-home check (H-02/H-08): raises ValueError when `resolved`
    # is not an ancestor of `home` (e.g. a sibling or a descendant of
    # home) -- caught and treated as "not broad". TypeError is also
    # guarded defensively for cross-flavor PurePath comparisons (mixed
    # POSIX/Windows path objects), which some pathlib implementations may
    # reject outright rather than returning ValueError.
    try:
        home.relative_to(resolved)
    except (ValueError, TypeError):
        return False
    return True


def get_containment_roots(explicit_root: str | None = None) -> list[Path]:
    """Resolve the set of allowed containment roots for AST path checks.

    When ``explicit_root`` is provided (the CLI ``--root`` flag), the
    allowed set is EXACTLY that one resolved path -- an exclusive
    override. This is a deliberate escape hatch: it is the user's
    discretion to point ``jerry ast`` at any directory they choose, or to
    run the surrounding tool with permission checks skipped. Jerry's
    containment check is best-effort defense against accidental
    traversal, not a security boundary against a user who has already
    chosen to grant the tool broad access via ``--root``. When the
    resolved ``--root`` is unusually broad (a filesystem/drive root, or
    the user's home directory), a single-line, non-fatal WARNING is
    printed to stderr -- never stdout, which carries the JSON/render
    payload -- noting that containment is effectively disabled; the
    invocation still proceeds (user discretion).

    Without ``explicit_root``, the allowed set defaults to:
        1. The user's project root (``CLAUDE_PROJECT_DIR`` env var, else
           cwd).
        2. ``tempfile.gettempdir()``, resolved.
        3. ``/tmp``, resolved, when it exists on this filesystem.

    Roots 2 and 3 exist to cover Claude Code scratchpad writes: on macOS,
    ``tempfile.gettempdir()`` resolves under ``$TMPDIR``
    (``/var/folders/...``), while Claude's scratchpad directories live
    under ``/tmp/claude-*`` (canonically ``/private/tmp/...``) -- a
    different tree. Registering both covers both locations without
    hard-coding Claude-specific paths. On Windows, only
    ``tempfile.gettempdir()`` applies (``/tmp`` will not exist).

    Args:
        explicit_root: The user-supplied ``--root`` CLI value, or None.

    Returns:
        A de-duplicated, order-preserving list of resolved absolute Path
        objects. Exactly one entry when ``explicit_root`` is set; the
        project root is always the first entry when it is not.
    """
    if explicit_root is not None:
        resolved_root = Path(explicit_root).resolve()
        if _is_broad_containment_root(resolved_root):
            print(
                f"Warning: --root '{resolved_root}' is an unusually broad "
                "containment root (a filesystem/drive root or the home "
                "directory); path containment is effectively disabled for "
                "this invocation.",
                file=sys.stderr,
            )
        return [resolved_root]

    roots: list[Path] = [get_project_root().resolve(), Path(tempfile.gettempdir()).resolve()]
    if _HARDCODED_TMP.exists():
        roots.append(_HARDCODED_TMP.resolve())

    # De-duplicate while preserving order (e.g. Linux CI: gettempdir()
    # often IS /tmp; dict.fromkeys() dedupes on Path.__eq__/__hash__).
    return list(dict.fromkeys(roots))

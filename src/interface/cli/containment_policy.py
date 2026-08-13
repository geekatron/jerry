# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Pure ``jerry ast`` path containment policy (BUG-010 Option C).

Zero env, filesystem, or config access. All inputs are pre-resolved
absolute paths supplied by the I/O-boundary caller (``project_root.py``).
This module is the single source of truth for the containment *decision*:
given a resolved project root, zero-or-more resolved user-configured
trusted roots, and an optional resolved explicit ``--root``, compute the
ordered allowed-roots set with per-root trust classification
(``project`` | ``configured`` | ``explicit``) and broad-root flags.

Replaces the prior always-widen containment policy (project root +
``tempfile.gettempdir()`` + ``/tmp``, unconditionally trusted) with
Option C: containment defaults to the project root plus zero-or-more
**user-declared** ``ast.trusted_roots`` entries. No directory is trusted
unless the project owns it or the user explicitly configured it.

References:
    - BUG-010: jerry ast path containment hardening
    - eng-lead-option-c-plan.md: authoritative implementation plan
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import Literal


@dataclass(frozen=True, slots=True)
class ContainmentRoot:
    """An allowed containment root with its trust classification.

    Attributes:
        path: The resolved, absolute containment root path.
        classification: How this root came to be trusted -- ``"project"``
            (the user's project root, always trusted), ``"configured"``
            (a user-declared ``ast.trusted_roots`` entry), or
            ``"explicit"`` (the CLI ``--root`` exclusive override).
        is_broad: True when this root is an unusually broad location (a
            filesystem/drive root, or the user's home directory or an
            ancestor of it) -- see ``_is_broad_containment_root``.
    """

    path: Path
    classification: Literal["project", "configured", "explicit"]
    is_broad: bool


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


def resolve_allowed_roots(
    project_root: Path,
    configured_roots: Sequence[Path],
    explicit_root: Path | None,
) -> list[ContainmentRoot]:
    """Compute the ordered allowed-roots set with trust classification.

    Pure containment policy (zero I/O). All inputs are pre-resolved by the
    caller.

    - When ``explicit_root`` is not None: returns EXACTLY one entry,
      classification ``"explicit"``, ignoring ``project_root`` and
      ``configured_roots`` entirely (unchanged ``--root`` exclusivity
      semantics -- a deliberate, user-discretion escape hatch).
    - When ``explicit_root`` is None: returns ``[project_root as
      "project"]`` followed by each entry in ``configured_roots`` as
      ``"configured"``, in that order, de-duplicated (first occurrence
      wins; a configured root that duplicates ``project_root`` is
      dropped, retaining the ``"project"`` classification).
    - ``is_broad`` is computed per-root via ``_is_broad_containment_root``.

    Args:
        project_root: The resolved, absolute user project root.
        configured_roots: Resolved, absolute user-declared trusted roots
            (``ast.trusted_roots``), in configuration order. Ignored when
            ``explicit_root`` is supplied.
        explicit_root: The resolved, absolute CLI ``--root`` value, or
            None to use the default (project + configured) set.

    Returns:
        An ordered list of ``ContainmentRoot`` entries, de-duplicated by
        path with first-occurrence-wins semantics.
    """
    if explicit_root is not None:
        return [
            ContainmentRoot(
                path=explicit_root,
                classification="explicit",
                is_broad=_is_broad_containment_root(explicit_root),
            )
        ]

    seen: set[Path] = {project_root}
    result: list[ContainmentRoot] = [
        ContainmentRoot(
            path=project_root,
            classification="project",
            is_broad=_is_broad_containment_root(project_root),
        )
    ]

    for root in configured_roots:
        if root in seen:
            continue
        seen.add(root)
        result.append(
            ContainmentRoot(
                path=root,
                classification="configured",
                is_broad=_is_broad_containment_root(root),
            )
        )

    return result

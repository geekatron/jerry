# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Shared CLI project-root and containment-root resolution (BUG-010 Option C).

Single source of truth for resolving the USER'S project root across CLI
namespaces (``config``, ``ast``, ...). Never anchors to the Jerry
installation's own directory tree, so commands operate on the user's
repository regardless of where Jerry is installed (plugin checkout,
marketplace install, or development clone).

Also provides ``get_containment_roots()`` (BUG-010 Option C, replacing the
prior always-widen containment policy): the default set of allowed
``jerry ast`` path containment roots is the user's project root plus
zero-or-more user-declared ``ast.trusted_roots`` config entries -- no
directory is trusted unless the project owns it or the user explicitly
configured it. An explicit ``--root`` CLI flag makes the allowed set
*exactly* that one resolved directory -- a user-discretion exclusive
override so ``jerry ast`` can be pointed anywhere the user chooses.

This module is the I/O boundary (env, filesystem, config) around the pure
policy decision core in ``containment_policy.py``; all classification and
broad-root-detection logic lives there.

References:
    - BUG-010: jerry ast path containment hardening
    - eng-lead-option-c-plan.md: authoritative implementation plan
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from src.interface.cli.containment_policy import ContainmentRoot, resolve_allowed_roots


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


def build_layered_config_adapter(defaults: dict[str, Any]) -> Any:
    """Construct a ``LayeredConfigAdapter`` anchored to the user's project root.

    Shared factory (DD-4): extracts the adapter-construction logic that
    ``CLIAdapter._create_config_adapter()`` already contains, so it is
    written once and both call sites (``adapter.py``,
    ``project_root.py``) share it -- ``jerry ast`` and ``jerry config``
    resolve the identical config file set with identical precedence
    (env prefix ``JERRY_``, same ``root_config_path``/
    ``project_config_path`` derivation from ``JERRY_PROJECT``).

    Local infrastructure import (not a module-level import) to preserve
    H-07 layer isolation discipline: this is a pre-existing architectural
    exception, matching the existing in-repo precedent of
    ``CLIAdapter._create_config_adapter()``, which already instantiates
    infrastructure directly from the interface layer.

    Args:
        defaults: Code-default configuration values for this adapter
            instance (dot-notation keys).

    Returns:
        A configured ``LayeredConfigAdapter`` instance.
    """
    from src.infrastructure.adapters.configuration.layered_config_adapter import (
        LayeredConfigAdapter,
    )

    root = get_project_root().resolve()
    jerry_project = os.environ.get("JERRY_PROJECT")

    project_config_path = None
    if jerry_project:
        project_config_path = root / "projects" / jerry_project / ".jerry" / "config.toml"

    return LayeredConfigAdapter(
        env_prefix="JERRY_",
        root_config_path=root / ".jerry" / "config.toml",
        project_config_path=project_config_path,
        defaults=defaults,
    )


def _load_trusted_roots() -> list[str]:
    """Read ``ast.trusted_roots`` through the shared ``LayeredConfigAdapter``.

    Precedence (highest to lowest): ``JERRY_AST__TRUSTED_ROOTS`` env var
    (note the DOUBLE underscore -- ``EnvConfigAdapter`` maps one dot to
    two underscores; the single-underscore form silently no-ops) ->
    project config (``projects/{JERRY_PROJECT}/.jerry/config.toml``) ->
    root config (``.jerry/config.toml``) -> code default ``[]``.

    Relative entries resolve against the current working directory when
    later converted to absolute paths by the caller -- a foot-gun for a
    security-relevant config key; use absolute paths.

    Returns:
        The raw, unresolved list of trusted-root path strings (possibly
        empty).
    """
    config = build_layered_config_adapter({"ast.trusted_roots": []})
    return [str(entry) for entry in config.get_list("ast.trusted_roots", [])]


def get_containment_roots(
    explicit_root: str | None = None,
    quiet: bool = False,
) -> list[ContainmentRoot]:
    """Resolve the set of allowed containment roots for AST path checks.

    When ``explicit_root`` is provided (the CLI ``--root`` flag), the
    allowed set is EXACTLY that one resolved path -- an exclusive
    override. This is a deliberate escape hatch: it is the user's
    discretion to point ``jerry ast`` at any directory they choose, or to
    run the surrounding tool with permission checks skipped. Jerry's
    containment check is best-effort defense against accidental
    traversal, not a security boundary against a user who has already
    chosen to grant the tool broad access via ``--root``.

    Without ``explicit_root``, the allowed set defaults to:
        1. The user's project root (``CLAUDE_PROJECT_DIR`` env var, else
           cwd).
        2. Zero-or-more user-declared ``ast.trusted_roots`` entries (read
           via ``_load_trusted_roots()``), each resolved to an absolute
           path. No directory is auto-trusted; OS temp/scratchpad
           directories (``tempfile.gettempdir()``, ``/tmp``) are never
           part of the default set. To grant ``jerry ast`` access to a
           scratchpad directory (e.g. for Claude Code scratchpad writes),
           declare it explicitly via ``ast.trusted_roots``.

    When any returned root is unusually broad (a filesystem/drive root,
    the user's home directory, or an ancestor of it), a single-line,
    non-fatal WARNING is printed to stderr -- never stdout, which carries
    the JSON/render payload -- for ``explicit`` (R-3) and ``configured``
    (DD-1 symmetry extension) classifications; the invocation still
    proceeds (user discretion). The project root's own broadness is never
    warned about (unchanged from prior behavior). Pass ``quiet=True`` to
    suppress this warning entirely (C6).

    Args:
        explicit_root: The user-supplied ``--root`` CLI value, or None.
        quiet: When True, suppresses the broad-root stderr warning.

    Returns:
        An ordered list of ``ContainmentRoot`` entries. Exactly one entry
        when ``explicit_root`` is set (classification ``"explicit"``);
        otherwise the project root (classification ``"project"``, always
        first) followed by de-duplicated configured trusted roots
        (classification ``"configured"``).
    """
    project_root = get_project_root().resolve()

    if explicit_root is not None:
        resolved_root = Path(explicit_root).resolve()
        roots = resolve_allowed_roots(project_root, [], resolved_root)
    else:
        trusted_raw = _load_trusted_roots()
        trusted_resolved = [Path(entry).resolve() for entry in trusted_raw]
        roots = resolve_allowed_roots(project_root, trusted_resolved, None)

    if not quiet:
        for root in roots:
            if not root.is_broad:
                continue
            if root.classification == "explicit":
                print(
                    f"Warning: --root '{root.path}' is an unusually broad "
                    "containment root (a filesystem/drive root or the home "
                    "directory); path containment is effectively disabled for "
                    "this invocation.",
                    file=sys.stderr,
                )
            elif root.classification == "configured":
                print(
                    f"Warning: configured trusted root '{root.path}' "
                    "(ast.trusted_roots) is an unusually broad containment "
                    "root (a filesystem/drive root or the home directory); "
                    "path containment is effectively widened for this "
                    "invocation.",
                    file=sys.stderr,
                )
            # "project" classification: no warning -- unchanged from prior
            # behavior; the project root is always the user's own
            # repository by construction of get_project_root().

    return roots

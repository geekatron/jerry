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
    infrastructure directly from the interface layer. Composition-root
    cleanup for both call sites is tracked as GitHub issue #373.

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
        candidate = root / "projects" / jerry_project / ".jerry" / "config.toml"
        projects_root = (root / "projects").resolve()
        if candidate.resolve().is_relative_to(projects_root):
            project_config_path = candidate
        else:
            # RED-BUG010 AC-18: a JERRY_PROJECT value containing '..' (or
            # otherwise escaping the projects/ tree) must never steer the
            # project-config read to a file outside the user's project
            # tree. Fail CLOSED: drop the project-config layer entirely
            # rather than trusting the traversed-to file.
            print(
                f"Warning: JERRY_PROJECT '{jerry_project}' resolves outside the "
                "projects/ directory; ignoring the project-level config.toml "
                "for this invocation.",
                file=sys.stderr,
            )

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
    security-relevant config key; use absolute paths. Prefer the TOML
    array form (``trusted_roots = ["/a", "/b"]``) over a comma-separated
    string; a literal comma inside a string-form entry (e.g. ``"/a,b/x"``)
    is split into two separate entries by the env/CSV parser.

    Empty and whitespace-only entries -- however they arise (an unset
    env var interpolated into ``JERRY_AST__TRUSTED_ROOTS``, a CSV
    trailing comma, or a stray ``""`` in a TOML array) -- are dropped
    here before they can reach path resolution. An unfiltered empty
    entry would resolve to the current working directory
    (``Path("").resolve() == Path.cwd()``), silently trusting cwd
    (RED-BUG010 AC-11). Surviving entries are also STRIPPED of leading
    and trailing whitespace (BUG-010 C4 tournament A-3): the blank-entry
    filter above already tests ``str(entry).strip()`` truthiness, but a
    non-blank entry with incidental padding (e.g. ``"  /abs/path  "``)
    must be returned stripped too -- otherwise the padded value later
    fails ``Path(...).is_absolute()`` and is silently (mis)treated as a
    cwd-relative entry by the caller.

    Windows note: a path embedded in ``.jerry/config.toml`` or in the
    ``JERRY_AST__TRUSTED_ROOTS`` env var (JSON array form) is parsed as a
    TOML/JSON string first. A raw backslash-separated Windows path (e.g.
    ``C:\\Users\\me``) contains invalid TOML/JSON escapes and will fail to
    parse -- use forward slashes (``C:/Users/me``) or escaped backslashes
    (``C:\\Users\\me``) in TOML/JSON config. A single path passed directly
    via the env var without JSON-array wrapping is not affected.

    Returns:
        The stripped, unresolved list of non-blank trusted-root path
        strings (possibly empty).
    """
    config = build_layered_config_adapter({"ast.trusted_roots": []})
    return [
        stripped
        for entry in config.get_list("ast.trusted_roots", [])
        if (stripped := str(entry).strip())
    ]


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
    the JSON/render payload -- for ``explicit`` (R-3), ``configured``
    (DD-1 symmetry extension), and ``project`` (A-2, BUG-010 C4
    tournament) classifications; the invocation still proceeds (user
    discretion). A broad project root (e.g. ``CLAUDE_PROJECT_DIR=/``)
    previously granted whole-filesystem trust with no signal to the
    user; it now warns symmetrically with the other two
    classifications. A relative ``ast.trusted_roots`` entry is likewise
    honored, not rejected (owner decision, RED-BUG010 AC-10), but emits
    its own one-line stderr warning naming the resolved cwd-relative
    path so the effective trust grant is never silent. Pass
    ``quiet=True`` to suppress all of these warnings entirely (C6).

    Args:
        explicit_root: The user-supplied ``--root`` CLI value, or None.
        quiet: When True, suppresses the broad-root and relative-trusted-
            root stderr warnings.

    Returns:
        An ordered list of ``ContainmentRoot`` entries. Exactly one entry
        when ``explicit_root`` is set (classification ``"explicit"``);
        otherwise the project root (classification ``"project"``, always
        first) followed by de-duplicated configured trusted roots
        (classification ``"configured"``).
    """
    project_root = get_project_root().resolve()

    relative_trusted: list[tuple[str, Path]] = []
    if explicit_root is not None:
        resolved_root = Path(explicit_root).resolve()
        roots = resolve_allowed_roots(project_root, [], resolved_root)
    else:
        trusted_raw = _load_trusted_roots()
        trusted_resolved = []
        for entry in trusted_raw:
            resolved_entry = Path(entry).resolve()
            trusted_resolved.append(resolved_entry)
            if not Path(entry).is_absolute():
                relative_trusted.append((entry, resolved_entry))
        roots = resolve_allowed_roots(project_root, trusted_resolved, None)

    if not quiet:
        for entry, resolved_entry in relative_trusted:
            print(
                f"Warning: configured trusted root '{entry}' (ast.trusted_roots) "
                "is a relative path; resolved against the current working "
                f"directory to '{resolved_entry}'. Use an absolute path to avoid "
                "invocation-directory-dependent trust.",
                file=sys.stderr,
            )
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
            elif root.classification == "project":
                # A-2 (BUG-010 C4 tournament, RT-002/FM-005): the project
                # root itself was previously never warned about, so a
                # broad CLAUDE_PROJECT_DIR (e.g. "/") silently granted
                # whole-filesystem trust with no signal to the user.
                # Symmetric with the "explicit" and "configured" warnings
                # above; suppressible by quiet=True like the others.
                print(
                    f"Warning: project root '{root.path}' is an unusually "
                    "broad containment root (a filesystem/drive root or "
                    "the home directory); path containment is effectively "
                    "disabled for this invocation.",
                    file=sys.stderr,
                )

    return roots

#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Security audit accept-list parser and expiry enforcer.

Reads .github/security/audit-allowlist.yml, validates that every accepted
entry has all required fields and has not reached its ``review_by`` date,
and prints --ignore-vuln flags suitable for passing directly to pip-audit.

FAIL-CLOSED CONTRACT: every error path exits 1.  A false-green (exit 0 when
something is wrong) is the worst possible outcome for a security gate.

Exit behaviour:
  0  All entries valid and unexpired; flags written to stdout.
  1  Any of the following:
       - YAML parse error or unexpected top-level structure
       - Any entry missing a required field
       - Any entry with review_by - accepted_on > MAX_DAYS (90-day cap)
       - Any entry whose review_by date <= today (expired)
     Error details written to stderr.

Usage (from the composite action):
    IGNORE_FLAGS=$(uv run python scripts/security/audit_allowlist.py \\
                        --allowlist .github/security/audit-allowlist.yml)
    ALLOWLIST_EXIT=$?
    if [[ "$ALLOWLIST_EXIT" -ne 0 ]]; then
      echo "::error::CVE accept-list check failed; see above"
      exit 1
    fi
    uv run pip-audit --requirement /tmp/requirements.txt --strict --desc $IGNORE_FLAGS
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml  # PyYAML — already a transitive dep via mkdocs; use safe_load only (M-04b)

# Maximum allowed days between accepted_on and review_by (ADR D2 policy).
# FAIL-CLOSED: entries exceeding this cap exit 1, never silently pass.
MAX_DAYS = 90

# All fields that MUST be present and non-empty on every allowlist entry.
# A missing or empty field exits 1 — never silently suppressed.
REQUIRED_FIELDS = ("id", "package", "reason", "accepted_by", "accepted_on", "review_by", "ticket")


def _load_allowlist(path: Path) -> list[dict[str, str]] | None:
    """Load and return the list of accepted CVE entries from the YAML file.

    FAIL-CLOSED: returns None (not an empty list) on any structural error
    so the caller can distinguish "empty allowlist" from "broken allowlist".

    Args:
        path: Absolute or repo-relative path to audit-allowlist.yml.

    Returns:
        List of entry dicts on success.
        None on YAML error or unexpected top-level structure.
        Empty list if the file is absent or the ``accepted`` list is empty.
    """
    if not path.exists():
        # Absent file == empty allowlist (no suppressions, no error).
        # FAIL-CLOSED: pip-audit still runs, CVEs still surface.
        return []
    with path.open(encoding="utf-8") as fh:
        try:
            data = yaml.safe_load(fh)  # M-04b: never yaml.load()
        except yaml.YAMLError as exc:
            # FAIL-CLOSED: malformed YAML is a hard error, not a silent empty list.
            print(
                f"::error::audit-allowlist.yml YAML parse error: {exc}",
                file=sys.stderr,
            )
            return None

    # FAIL-CLOSED: top-level must be a dict with an 'accepted' key.
    # A bare YAML list, a scalar, or a missing 'accepted' key all exit 1.
    if not isinstance(data, dict) or "accepted" not in data:
        print(
            "::error::audit-allowlist.yml is malformed — expected a mapping with "
            "an 'accepted' key at the top level (got: "
            f"{type(data).__name__ if data is not None else 'null'})",
            file=sys.stderr,
        )
        return None

    entries = data.get("accepted") or []
    if not isinstance(entries, list):
        # FAIL-CLOSED: 'accepted' must be a YAML sequence, not a scalar or mapping.
        print(
            "::error::audit-allowlist.yml 'accepted' field must be a list "
            f"(got: {type(entries).__name__})",
            file=sys.stderr,
        )
        return None

    return entries


def _validate_entries(entries: list[dict[str, str]], today: date) -> list[str]:
    """Validate all required fields, the 90-day cap, and expiry for every entry.

    FAIL-CLOSED: any validation failure is collected and returned as errors.
    The caller exits 1 if the returned list is non-empty.

    Args:
        entries: Parsed accept-list entries.
        today: The reference date (injected for testability).

    Returns:
        List of error strings. Empty list means all entries are valid.
    """
    errors: list[str] = []
    for i, entry in enumerate(entries):
        entry_label = entry.get("id") or f"(entry #{i + 1})"

        # --- Required-field check ---
        # FAIL-CLOSED: missing or empty required field is a hard error.
        # The comment "schema enforces presence" was aspirational; this IS the enforcement.
        for field in REQUIRED_FIELDS:
            value = entry.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                errors.append(
                    f"::error::{entry_label}: missing or empty required field '{field}' "
                    f"— every accept-list entry must supply all required fields"
                )

        # --- Date parsing (only if both date fields are present) ---
        accepted_on_raw = entry.get("accepted_on", "")
        review_by_raw = entry.get("review_by", "")

        accepted_on: date | None = None
        review_by: date | None = None

        if accepted_on_raw:
            try:
                accepted_on = date.fromisoformat(str(accepted_on_raw))
            except ValueError:
                errors.append(
                    f"::error::{entry_label}: 'accepted_on' is not a valid ISO-8601 date: "
                    f"'{accepted_on_raw}'"
                )

        if review_by_raw:
            try:
                review_by = date.fromisoformat(str(review_by_raw))
            except ValueError:
                errors.append(
                    f"::error::{entry_label}: 'review_by' is not a valid ISO-8601 date: "
                    f"'{review_by_raw}'"
                )

        if accepted_on is not None and review_by is not None:
            # --- 90-day cap check ---
            # FAIL-CLOSED: review_by - accepted_on > MAX_DAYS exits 1.
            # "Maximum: 90 days" in the comment is now ENFORCED HERE.
            delta = (review_by - accepted_on).days
            if delta > MAX_DAYS:
                errors.append(
                    f"::error::{entry_label}: review_by is {delta} days after accepted_on "
                    f"(max allowed: {MAX_DAYS} days). Shorten the acceptance window."
                )

            # --- Expiry check ---
            # FAIL-CLOSED: entry is EXPIRED when today >= review_by.
            # "today < review_by" is the ONLY condition under which suppression is active.
            # On the review_by date itself the entry is expired (ADR D2: <= semantics).
            if today >= review_by:  # off-by-one fix: >= not >
                errors.append(
                    f"::error::{entry_label}: expired (review_by: {review_by}, today: {today}). "
                    f"Remove the entry if the fix has been applied, or renew with updated justification."
                )

    return errors


def _build_ignore_flags(entries: list[dict[str, str]], today: date) -> list[str]:
    """Build pip-audit --ignore-vuln flags for valid, unexpired entries only.

    Called only AFTER _validate_entries() returns no errors, so entry structure
    is already confirmed safe.

    Args:
        entries: Validated accept-list entries (all fields present, all unexpired).
        today: The reference date used to filter expired entries.

    Returns:
        Flat list of alternating ``--ignore-vuln`` and ``<vuln-id>`` strings,
        ready to be passed directly to pip-audit.
    """
    flags: list[str] = []
    for entry in entries:
        review_by_raw = entry.get("review_by", "")
        if review_by_raw:
            review_by = date.fromisoformat(str(review_by_raw))
            # FAIL-CLOSED: suppress ONLY when today < review_by.
            # On the review_by date (today == review_by) the entry is expired.
            if today >= review_by:
                continue  # expired — must not suppress
        vuln_id = entry.get("id", "").strip()
        if not vuln_id:
            # FAIL-CLOSED: empty id means no flag — but validation already caught this;
            # this guard is a defensive belt-and-suspenders check.
            continue
        flags.extend(["--ignore-vuln", vuln_id])
    return flags


def main(argv: list[str] | None = None) -> int:
    """Parse allowlist, enforce all constraints, print ignore flags.

    FAIL-CLOSED at every error path: any structural problem, missing field,
    cap violation, or expired entry exits 1 with a ::error:: annotation.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Exit code: 0 = all entries valid and unexpired, flags on stdout.
                   1 = any validation or expiry error.
    """
    parser = argparse.ArgumentParser(
        description="Parse CVE accept-list and emit pip-audit --ignore-vuln flags."
    )
    parser.add_argument(
        "--allowlist",
        type=Path,
        default=Path(".github/security/audit-allowlist.yml"),
        help="Path to the accept-list YAML file (default: .github/security/audit-allowlist.yml).",
    )
    args = parser.parse_args(argv)

    # --- Load: FAIL-CLOSED on YAML errors or bad structure ---
    entries = _load_allowlist(args.allowlist)
    if entries is None:
        # _load_allowlist already printed a ::error:: message.
        return 1

    if not entries:
        # Empty allowlist: valid, no flags.
        print("")
        return 0

    today = date.today()

    # --- Validate ALL entries before emitting any flags ---
    # FAIL-CLOSED: collect all errors and surface them at once so the author
    # can fix multiple problems in a single iteration.
    errors = _validate_entries(entries, today)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        print(
            "Fix all errors above before re-running. Do not bypass this check.",
            file=sys.stderr,
        )
        return 1

    # --- Build and emit flags ---
    flags = _build_ignore_flags(entries, today)
    # Print flags space-separated so the shell can word-split them into pip-audit argv.
    # When the list is empty this prints an empty string, which is harmless.
    print(" ".join(flags))
    return 0


if __name__ == "__main__":
    sys.exit(main())

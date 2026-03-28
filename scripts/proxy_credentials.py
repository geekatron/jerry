#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CLI for managing proxy infrastructure credentials.

Usage:
    uv run scripts/proxy_credentials.py set <provider>
    uv run scripts/proxy_credentials.py check <provider>
    uv run scripts/proxy_credentials.py delete <provider>

Examples:
    uv run scripts/proxy_credentials.py set digitalocean
    uv run scripts/proxy_credentials.py check digitalocean
    uv run scripts/proxy_credentials.py delete digitalocean
"""

from __future__ import annotations

import getpass
import sys


def main() -> None:
    """Entry point for proxy credential management CLI."""
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]
    provider = sys.argv[2]

    if action == "set":
        from src.proxy_infra.interface.cli.proxy_commands import credentials_set_command

        api_key = getpass.getpass(f"Enter {provider} API key: ")
        if not api_key.strip():
            print("Error: API key cannot be empty.")
            sys.exit(1)
        credentials_set_command(provider, api_key)
        print(f"Stored in macOS Keychain as jerry/proxy.{provider}.api-key")

    elif action == "check":
        from src.proxy_infra.interface.cli.proxy_commands import credentials_check_command

        result = credentials_check_command(provider)
        if result.found:
            print(f"Found: {provider} credential in {result.source}")
        else:
            print(f"Not found: no credential for {provider}")
            print(f"  Store one with: uv run scripts/proxy_credentials.py set {provider}")
            sys.exit(1)

    elif action == "delete":
        from src.proxy_infra.interface.cli.proxy_commands import credentials_delete_command

        deleted = credentials_delete_command(provider)
        if deleted:
            print(f"Deleted: {provider} credential removed from Keychain")
        else:
            print(f"Not found: no credential to delete for {provider}")

    else:
        print(f"Unknown action: {action}")
        print("Valid actions: set, check, delete")
        sys.exit(1)


if __name__ == "__main__":
    main()

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests verifying credentials never appear in pytest output.

OPSEC control: API keys, tokens, and secrets must never flow through
pytest fixture return values or test method parameters. When a test
fails, pytest prints all method parameters in the traceback. If a
parameter contains a raw credential, the credential is leaked into
any system that captures test output (CI logs, LLM API calls, terminals).

The secure pattern: fixtures set env vars internally and return None.
Tests read from os.environ when needed, never from fixture parameters.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest


class TestNoCredentialReturnInFixtures:
    """Verify no test fixture returns a raw credential string."""

    def test_e2e_fixtures_do_not_return_credentials(self) -> None:
        """E2E test fixtures must not return values named after credentials."""
        e2e_dir = Path("tests/e2e/proxy_infra")
        if not e2e_dir.exists():
            pytest.skip("E2E test directory does not exist")

        credential_var_names = {
            "api_key",
            "key",
            "secret",
            "token",
            "password",
            "credential",
        }
        violations = []

        for py_file in e2e_dir.glob("*.py"):
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.FunctionDef):
                    continue
                # Only check fixtures (decorated with @pytest.fixture)
                is_fixture = any(
                    (isinstance(d, ast.Attribute) and d.attr == "fixture")
                    or (
                        isinstance(d, ast.Call)
                        and isinstance(d.func, ast.Attribute)
                        and d.func.attr == "fixture"
                    )
                    for d in node.decorator_list
                )
                if not is_fixture:
                    continue
                # Check for return statements returning a Name that matches credential patterns
                for child in ast.walk(node):
                    if isinstance(child, ast.Return) and isinstance(child.value, ast.Name):
                        if child.value.id in credential_var_names:
                            violations.append(
                                f"{py_file.name}:{child.lineno}: "
                                f"fixture '{node.name}' returns variable "
                                f"'{child.value.id}'"
                            )

        assert violations == [], (
            "OPSEC: Fixtures returning credential variables leak in pytest tracebacks:\n"
            + "\n".join(violations)
        )

    def test_e2e_test_methods_do_not_accept_credential_parameters(self) -> None:
        """E2E test methods must not have parameters named after credentials."""
        e2e_dir = Path("tests/e2e/proxy_infra")
        if not e2e_dir.exists():
            pytest.skip("E2E test directory does not exist")

        credential_param_names = {
            "api_key",
            "do_api_key",
            "secret",
            "token",
            "password",
            "credential",
            "private_key_value",
            "api_token",
        }
        violations = []

        for py_file in e2e_dir.glob("*.py"):
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                    for arg in node.args.args:
                        if arg.arg in credential_param_names:
                            violations.append(
                                f"{py_file.name}:{node.lineno}: "
                                f"test method '{node.name}' accepts "
                                f"credential parameter '{arg.arg}'"
                            )

        assert violations == [], (
            "OPSEC: Test method parameters appear in pytest tracebacks. "
            "Use an autouse fixture that sets env vars instead:\n" + "\n".join(violations)
        )

    def test_fixture_credential_pattern_uses_yield_not_return(self) -> None:
        """Credential-related fixtures must use yield (for cleanup) not return."""
        e2e_dir = Path("tests/e2e/proxy_infra")
        if not e2e_dir.exists():
            pytest.skip("E2E test directory does not exist")

        violations = []

        for py_file in e2e_dir.glob("*.py"):
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.FunctionDef):
                    continue
                # Check if this is a fixture (has @pytest.fixture decorator)
                is_fixture = False
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Attribute):
                        if decorator.attr == "fixture":
                            is_fixture = True
                    elif isinstance(decorator, ast.Call):
                        func = decorator.func
                        if isinstance(func, ast.Attribute) and func.attr == "fixture":
                            is_fixture = True
                if not is_fixture:
                    continue

                # Check if fixture name suggests credential handling
                credential_names = {"token", "key", "secret", "credential", "api"}
                if not any(n in node.name.lower() for n in credential_names):
                    continue

                # Check if any Return node returns a non-None value
                for child in ast.walk(node):
                    if isinstance(child, ast.Return) and child.value is not None:
                        if (
                            not isinstance(child.value, ast.Constant)
                            or child.value.value is not None
                        ):
                            violations.append(
                                f"{py_file.name}:{child.lineno}: "
                                f"fixture '{node.name}' returns a value — "
                                f"credential fixtures must yield (not return) "
                                f"and should set env vars internally"
                            )

        assert violations == [], (
            "OPSEC: Credential fixtures that return values leak in tracebacks:\n"
            + "\n".join(violations)
        )

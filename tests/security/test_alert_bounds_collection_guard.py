# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Guard: the alert-bounds regression tests must stay selected by the marker expressions CI uses.

CI runs ``pytest -m "<expression>"`` (the "Test uv" cells of ci.yml and release.yml).  A test file
that carries a marker which the expression leaves out is deselected from every job without any
message, and a regression suite that never runs protects nothing.  This file reads the
expressions from the workflow files (it does not copy them) and reads ``test_security_alert_bounds.py``
and itself with ``ast`` (it does not import them).  For each of the two files it fails if

* a marker that CI's expression leaves out is carried anywhere in the file, however pytest is
  imported (``import pytest as pt`` and ``from pytest import mark as m`` are followed);
* the file switches itself off: a ``skip`` or ``xfail`` mark, a ``skipif`` whose condition is a
  constant, or ``pytest.skip(..., allow_module_level=True)``;
* the file can skip itself when an import is missing (``importorskip``); or
* the file defines fewer test functions than its floor, so that a deleted suite does not pass.

It does not run pytest and it does not look at ``conftest.py`` hooks or at command lines other than
``-m "..."`` in a workflow step that runs pytest.  A CI check that collects the file under CI's
expression and fails below a floor would be the stronger test (a follow-up that edits ci.yml).
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.security

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"
REGRESSION_FILE = Path(__file__).with_name("test_security_alert_bounds.py")
GUARD_FILE = Path(__file__)
# The files that must stay selected, each with the least number of test functions it must define: the
# number it defines now.  A parametrized test counts once here; pytest collects one test per case.
GUARDED_FILES = {REGRESSION_FILE: 140, GUARD_FILE: 15}
FILE_IDS = [path.name for path in GUARDED_FILES]


@dataclass
class _PytestNames:
    """The names under which ``pytest``, ``pytest.mark`` and two functions are bound in a module."""

    modules: set[str] = field(default_factory=lambda: {"pytest"})
    marks: set[str] = field(default_factory=lambda: {"mark"})
    importorskips: set[str] = field(default_factory=lambda: {"importorskip"})
    skips: set[str] = field(default_factory=lambda: {"skip"})


def _pytest_names(tree: ast.AST) -> _PytestNames:
    """Follow ``import pytest as X`` and ``from pytest import mark/importorskip/skip as Y``."""
    names = _PytestNames()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.modules.update(a.asname or a.name for a in node.names if a.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                bound = alias.asname or alias.name
                if alias.name == "mark":
                    names.marks.add(bound)
                elif alias.name == "importorskip":
                    names.importorskips.add(bound)
                elif alias.name == "skip":
                    names.skips.add(bound)
    return names


def _is_mark_owner(owner: ast.expr, names: _PytestNames) -> bool:
    """Whether ``owner`` is ``pytest.mark`` (under any alias) or a bare name bound to it."""
    if isinstance(owner, ast.Name):
        return owner.id in names.marks
    return (
        isinstance(owner, ast.Attribute)
        and owner.attr == "mark"
        and isinstance(owner.value, ast.Name)
        and owner.value.id in names.modules
    )


def _marker_names(source: str) -> set[str]:
    """Names of the pytest marks used anywhere in ``source`` (``subprocess`` for ``pytest.mark.subprocess``)."""
    tree = ast.parse(source)
    names = _pytest_names(tree)
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and _is_mark_owner(node.value, names)
    }


def _calls_importorskip(source: str) -> bool:
    """Whether ``source`` calls ``importorskip`` (``pytest.importorskip``, an alias or a bare name)."""
    tree = ast.parse(source)
    names = _pytest_names(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "importorskip":
            return True
        if isinstance(func, ast.Name) and func.id in names.importorskips:
            return True
    return False


def _switches_itself_off(source: str) -> list[str]:
    """Ways in which ``source`` skips or expects to fail every test it defines, or a whole class."""
    tree = ast.parse(source)
    names = _pytest_names(tree)
    problems = [
        f"line {node.lineno}: the mark {node.attr!r}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and _is_mark_owner(node.value, names)
        and node.attr in {"skip", "xfail"}
    ]
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        is_skipif = (
            isinstance(func, ast.Attribute)
            and func.attr == "skipif"
            and _is_mark_owner(func.value, names)
        )
        if (
            is_skipif
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value
        ):
            problems.append(f"line {node.lineno}: skipif with a condition that is always true")
        is_skip_call = (
            isinstance(func, ast.Attribute)
            and func.attr == "skip"
            and isinstance(func.value, ast.Name)
            and func.value.id in names.modules
        ) or (isinstance(func, ast.Name) and func.id in names.skips)
        module_level = any(
            kw.arg == "allow_module_level"
            and not (isinstance(kw.value, ast.Constant) and not kw.value.value)
            for kw in node.keywords
        )
        if is_skip_call and module_level:
            problems.append(f"line {node.lineno}: pytest.skip(..., allow_module_level=True)")
    return problems


def _test_function_count(source: str) -> int:
    """How many functions named ``test_*`` (methods included) ``source`` defines."""
    return sum(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(ast.parse(source))
    )


# --- pytest's -m expression: names, "and", "or", "not" and parentheses -------------------------


def _evaluate(expression: str, markers: set[str]) -> bool:
    """Whether a test that carries exactly ``markers`` is selected by ``pytest -m expression``."""
    tokens = re.findall(r"[()]|[^\s()]+", expression)
    position = 0

    def peek() -> str | None:
        return tokens[position] if position < len(tokens) else None

    def take() -> str:
        nonlocal position
        if position >= len(tokens):
            raise ValueError(f"unexpected end of the marker expression {expression!r}")
        position += 1
        return tokens[position - 1]

    def parse_or() -> bool:
        value = parse_and()
        while peek() == "or":
            take()
            value = parse_and() or value
        return value

    def parse_and() -> bool:
        value = parse_not()
        while peek() == "and":
            take()
            value = parse_not() and value
        return value

    def parse_not() -> bool:
        token = take()
        if token == "not":
            return not parse_not()
        if token == "(":
            value = parse_or()
            if take() != ")":
                raise ValueError(f"missing ) in the marker expression {expression!r}")
            return value
        if token in {")", "and", "or"}:
            raise ValueError(f"unexpected {token!r} in the marker expression {expression!r}")
        return token in markers

    result = parse_or()
    if peek() is not None:
        raise ValueError(f"unexpected {peek()!r} in the marker expression {expression!r}")
    return result


_MARKER_FLAG = re.compile(r"""(?<![\w-])-m\s+(?P<quote>["'])(?P<expression>[^"']+)(?P=quote)""")


def _expressions_in(run: str) -> list[str]:
    """The ``-m "..."`` expressions of a workflow step, if the step runs pytest at all."""
    if "pytest" not in run:
        return []
    return [match["expression"] for match in _MARKER_FLAG.finditer(run)]


def _ci_expressions() -> dict[str, list[str]]:
    """The marker expressions of every pytest command in the workflow files, by file name."""
    found: dict[str, list[str]] = {}
    for path in sorted(WORKFLOWS.glob("*.yml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        for job in (document.get("jobs") or {}).values():
            for step in job.get("steps") or []:
                run = step.get("run")
                if isinstance(run, str) and _expressions_in(run):
                    found.setdefault(path.name, []).extend(_expressions_in(run))
    return found


class TestCiSelection:
    """The expressions that CI selects tests with, as the workflow files give them."""

    def test_workflows_when_read_then_the_test_jobs_and_the_release_job_have_an_expression(
        self,
    ) -> None:
        found = _ci_expressions()

        assert {"ci.yml", "release.yml"} <= set(found), (
            "no pytest -m expression in ci.yml or release.yml: update this guard to the new command"
        )

    def test_expressions_when_applied_to_a_plain_security_test_then_they_select_it(self) -> None:
        for name, expressions in _ci_expressions().items():
            for expression in expressions:
                assert _evaluate(expression, {"security"}), f"{name}: -m {expression!r}"


class TestGuardedFilesStayCollected:
    """Both test files must run in every job that selects tests with CI's expressions."""

    @pytest.mark.parametrize("path", list(GUARDED_FILES), ids=FILE_IDS)
    def test_file_when_parsed_then_it_defines_at_least_its_floor_of_tests(self, path: Path) -> None:
        count = _test_function_count(path.read_text(encoding="utf-8"))

        assert count >= GUARDED_FILES[path], (
            f"{path.name} defines {count} test functions; its floor is {GUARDED_FILES[path]}. "
            "Lower the floor only when tests are removed on purpose."
        )

    @pytest.mark.parametrize("path", list(GUARDED_FILES), ids=FILE_IDS)
    def test_file_when_parsed_then_every_ci_expression_selects_it(self, path: Path) -> None:
        markers = _marker_names(path.read_text(encoding="utf-8"))

        for name, expressions in _ci_expressions().items():
            for expression in expressions:
                assert _evaluate(expression, markers), (
                    f"{path.name} carries the markers {sorted(markers)}; {name} runs "
                    f"-m {expression!r}, so these tests would be deselected from that job"
                )

    @pytest.mark.parametrize("path", list(GUARDED_FILES), ids=FILE_IDS)
    def test_file_when_parsed_then_it_does_not_switch_itself_off(self, path: Path) -> None:
        problems = _switches_itself_off(path.read_text(encoding="utf-8"))

        assert not problems, f"{path.name}: " + "; ".join(problems)

    @pytest.mark.parametrize("path", list(GUARDED_FILES), ids=FILE_IDS)
    def test_file_when_parsed_then_it_cannot_skip_itself_on_a_missing_import(
        self, path: Path
    ) -> None:
        assert not _calls_importorskip(path.read_text(encoding="utf-8")), (
            f"{path.name}: use a plain import: importorskip turns a missing dependency into a "
            "silent skip"
        )


class TestExpressionReader:
    """Reading ``-m`` expressions out of a workflow step, and evaluating them."""

    @pytest.mark.parametrize(
        ("run", "expected"),
        [
            pytest.param(
                'uv run pytest \\\n  -m "not llm and not subprocess" \\\n  --cov=src\n',
                ["not llm and not subprocess"],
                id="continued-lines",
            ),
            pytest.param(
                "uv run pytest -m 'not subprocess and not llm' -v --tb=short",
                ["not subprocess and not llm"],
                id="single-quotes",
            ),
            pytest.param(
                'uv run pytest -m "not llm" tests/a\nuv run pytest -m "not slow" tests/b',
                ["not llm", "not slow"],
                id="two-commands",
            ),
            pytest.param('git tag -a v1 -m "Release v1"', [], id="no-pytest-in-the-step"),
            pytest.param("python -m pytest tests", [], id="module-flag-without-a-quote"),
            pytest.param("uv run pytest tests", [], id="no-expression"),
        ],
    )
    def test_workflow_step_when_read_then_only_the_marker_expressions_are_found(
        self, run: str, expected: list[str]
    ) -> None:
        assert _expressions_in(run) == expected

    @pytest.mark.parametrize(
        ("expression", "markers", "selected"),
        [
            pytest.param("not llm and not subprocess", {"security"}, True, id="plain"),
            pytest.param("not llm and not subprocess", {"security", "llm"}, False, id="llm"),
            pytest.param("not llm and not subprocess", {"subprocess"}, False, id="subprocess"),
            pytest.param("not subprocess and not llm", {"llm"}, False, id="other-order"),
            pytest.param("not (llm or subprocess)", {"subprocess"}, False, id="parentheses"),
            pytest.param("not (llm or subprocess)", {"security"}, True, id="parentheses-plain"),
            pytest.param("slow or security", {"security"}, True, id="or"),
            pytest.param("slow or security", {"other"}, False, id="or-no-match"),
            pytest.param("not happy-path", {"happy-path"}, False, id="hyphen-in-a-name"),
            pytest.param("not a and b", {"b"}, True, id="not-binds-tighter-than-and"),
            pytest.param("not a and b", {"a", "b"}, False, id="not-binds-tighter-than-and-2"),
            pytest.param("a or b and c", {"a"}, True, id="and-binds-tighter-than-or"),
        ],
    )
    def test_expression_when_evaluated_then_it_follows_pytests_rules(
        self, expression: str, markers: set[str], selected: bool
    ) -> None:
        assert _evaluate(expression, markers) is selected

    @pytest.mark.parametrize("expression", ["not", "a and", "(a", "a b", ") a", "and a"])
    def test_malformed_expression_when_evaluated_then_it_raises(self, expression: str) -> None:
        with pytest.raises(ValueError, match="marker expression"):
            _evaluate(expression, {"a"})


class TestMarkerDetection:
    """The detection itself: every way of applying a mark is found."""

    @pytest.mark.parametrize(
        "source",
        [
            pytest.param(
                "import pytest\npytestmark = pytest.mark.subprocess\n", id="module-level-mark"
            ),
            pytest.param(
                "import pytest\npytestmark = [pytest.mark.security, pytest.mark.llm]\n",
                id="list-of-marks",
            ),
            pytest.param(
                "import pytest\n\n@pytest.mark.subprocess\ndef test_a():\n    pass\n",
                id="function-decorator",
            ),
            pytest.param(
                "import pytest\n\n@pytest.mark.llm\nclass TestA:\n    pass\n",
                id="class-decorator",
            ),
            pytest.param(
                "import pytest\nparams = pytest.param(1, marks=pytest.mark.subprocess)\n",
                id="param-marks",
            ),
            pytest.param(
                "import pytest\nparams = pytest.param(1, marks=[pytest.mark.llm])\n",
                id="param-marks-list",
            ),
            pytest.param(
                "from pytest import mark\n\n@mark.subprocess\ndef test_a():\n    pass\n",
                id="bare-mark-import",
            ),
            pytest.param(
                "import pytest as pt\npytestmark = pt.mark.subprocess\n", id="module-alias"
            ),
            pytest.param(
                "from pytest import mark as m\n\n@m.llm\ndef test_a():\n    pass\n",
                id="mark-alias",
            ),
        ],
    )
    def test_source_with_a_deselected_marker_when_scanned_then_the_marker_is_found(
        self, source: str
    ) -> None:
        assert _marker_names(source) & {"llm", "subprocess"}

    @pytest.mark.parametrize(
        "source",
        [
            pytest.param(
                "import pytest\npytestmark = [pytest.mark.security]\n", id="security-only"
            ),
            pytest.param(
                "import pytest\n\n@pytest.mark.parametrize('a', [1])\ndef test_a(a):\n    pass\n",
                id="parametrize",
            ),
            pytest.param(
                "import pytest\n\n@pytest.mark.skipif(True, reason='x')\ndef test_a():\n    pass\n",
                id="skipif",
            ),
            pytest.param(
                "import subprocess\n\ndef test_a():\n    subprocess.run(['true'], check=True)\n",
                id="imports-subprocess-module",
            ),
            pytest.param(
                "other = object()\nvalue = other.mark.subprocess\n", id="mark-of-another-object"
            ),
        ],
    )
    def test_source_without_a_deselected_marker_when_scanned_then_nothing_is_found(
        self, source: str
    ) -> None:
        assert not _marker_names(source) & {"llm", "subprocess"}

    @pytest.mark.parametrize(
        ("source", "expected"),
        [
            pytest.param(
                "import pytest\nyaml = pytest.importorskip('yaml')\n", True, id="pytest-attribute"
            ),
            pytest.param(
                "from pytest import importorskip\nyaml = importorskip('yaml')\n",
                True,
                id="bare-name",
            ),
            pytest.param(
                "from pytest import importorskip as need\nyaml = need('yaml')\n",
                True,
                id="alias",
            ),
            pytest.param(
                "import pytest as pt\nyaml = pt.importorskip('yaml')\n", True, id="module-alias"
            ),
            pytest.param("import yaml\n", False, id="plain-import"),
        ],
    )
    def test_source_when_scanned_for_importorskip_then_the_call_is_found_only_when_present(
        self, source: str, expected: bool
    ) -> None:
        assert _calls_importorskip(source) is expected

    @pytest.mark.parametrize(
        "source",
        [
            pytest.param("import pytest\npytestmark = pytest.mark.skip\n", id="skip"),
            pytest.param(
                "import pytest\npytestmark = pytest.mark.skip(reason='x')\n", id="skip-call"
            ),
            pytest.param("import pytest\npytestmark = [pytest.mark.xfail]\n", id="xfail"),
            pytest.param(
                "import pytest\n\n@pytest.mark.skip\nclass TestA:\n    pass\n", id="class-skip"
            ),
            pytest.param(
                "import pytest\npytestmark = pytest.mark.skipif(True, reason='x')\n",
                id="skipif-true",
            ),
            pytest.param(
                "import pytest\npytest.skip('x', allow_module_level=True)\n", id="module-skip"
            ),
            pytest.param(
                "from pytest import skip\nskip('x', allow_module_level=True)\n", id="bare-skip"
            ),
            pytest.param(
                "import pytest as pt\npytestmark = pt.mark.xfail(strict=True)\n", id="alias-xfail"
            ),
        ],
    )
    def test_source_that_switches_itself_off_when_scanned_then_it_is_found(
        self, source: str
    ) -> None:
        assert _switches_itself_off(source)

    @pytest.mark.parametrize(
        "source",
        [
            pytest.param(
                "import sys\nimport pytest\n"
                "pytestmark = pytest.mark.skipif(sys.platform == 'win32', reason='x')\n",
                id="skipif-on-the-platform",
            ),
            pytest.param(
                "import pytest\n\ndef test_a():\n    pytest.skip('no openssl')\n",
                id="skip-inside-a-test",
            ),
            pytest.param(
                "import pytest\nvalue = pytest.skip('x', allow_module_level=False)\n",
                id="module-level-false",
            ),
        ],
    )
    def test_source_that_only_skips_on_a_condition_when_scanned_then_nothing_is_found(
        self, source: str
    ) -> None:
        assert not _switches_itself_off(source)

    def test_test_functions_when_counted_then_methods_and_nested_classes_are_included(
        self,
    ) -> None:
        source = (
            "def test_a(): pass\n"
            "def helper(): pass\n"
            "class TestA:\n"
            "    def test_b(self): pass\n"
            "    def check(self): pass\n"
            "    class TestInner:\n"
            "        async def test_c(self): pass\n"
        )

        assert _test_function_count(source) == 3

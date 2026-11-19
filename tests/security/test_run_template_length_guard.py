# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Guard: a ``run:`` string that GitHub reads as a template must stay far below its length limit.

GitHub reads a ``run:`` string that holds ``${{`` as a template.  The runner (actions/runner,
``TemplateReader.ParseScalar``) turns the whole string into ONE expression,
``format('<the text, every quote and brace doubled>', <expression>, ...)``, and its expression
parser (``ExpressionParser``, ``ParseContext``) refuses an expression of more than 21,000
characters (``ExpressionConstants.MaxLength``).  The step then fails before it starts:

    The template is not valid. <file> (Line: N, Col: M): Exceeded max expression length 21000

That is what stopped the "Run pip-audit" step of ``.github/actions/security-audit/action.yml`` in
run 44432888879 of pull request 449, when the step's script had grown to 21,807 characters.  A
``run:`` string without ``${{`` is not a template and has no such limit, so the remedy is to keep a
long script out of any string that holds an expression: put it in a file, start it from a short
``run:`` line, and pass values through ``env:``.

This file reads every YAML file under ``.github/actions`` and ``.github/workflows`` (it does not
copy a list of them or of their steps) and fails when a ``run:`` string that holds ``${{`` reaches
``LENGTH_BUDGET``, which is the limit less ``LIMIT_MARGIN``.  A string is held against the budget
by the larger of two lengths: its characters, and the length of the expression that the runner
builds from it, in UTF-16 code units (what .NET's ``String.Length`` counts, and what GitHub's
limit is applied to).  Neither is always the larger.  The expression has every quote and brace of
the text doubled, which lengthens it, but each ``${{ x }}`` becomes ``{n}`` and an argument
``, x``, which is shorter: the "Check all jobs passed" step of ci.yml is 1,557 characters and
measures 1,548.  A script with many expressions and few quotes or braces is shorter as an
expression, so its characters count too.  The guard does not look at other strings that hold
``${{`` (``with:``, ``env:``, ``if:``): the same limit applies to them, but only a script grows
that far.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.security

ROOT = Path(__file__).resolve().parents[2]
YAML_ROOTS = (ROOT / ".github" / "actions", ROOT / ".github" / "workflows")
# ExpressionConstants.MaxLength in actions/runner: "Exceeded max expression length 21000".
EXPRESSION_LENGTH_LIMIT = 21_000
# What a change may add before the next run of this test.  The expression that the runner builds
# differs from the string by about 1% (longer for the audit step's script, shorter for ci.yml's
# "Check all jobs passed"), far less than the margin.
LIMIT_MARGIN = 3_000
LENGTH_BUDGET = EXPRESSION_LENGTH_LIMIT - LIMIT_MARGIN
OPEN = "${{"


@dataclass(frozen=True)
class RunString:
    """One ``run:`` string, and where it is."""

    file: str
    where: str
    text: str


def _utf16_units(text: str) -> int:
    """Length of ``text`` in UTF-16 code units: what .NET's ``String.Length`` counts."""
    return len(text.encode("utf-16-le", "surrogatepass")) // 2


def _segments(text: str) -> list[tuple[str, str]]:
    """Split ``text`` into ``("text", ...)`` and ``("expr", ...)`` parts, as the runner does.

    An expression runs from ``${{`` to the first ``}}`` that is outside a single-quoted string.
    """
    parts: list[tuple[str, str]] = []
    i = 0
    start = text.find(OPEN)
    while i < len(text):
        if i == start:
            end = -1
            inside = False
            i += len(OPEN)
            while i < len(text):
                if text[i] == "'":
                    inside = not inside
                elif text[i] == "}" and not inside and text[i - 1] == "}":
                    end = i
                    i += 1
                    break
                i += 1
            if end < start:
                raise ValueError("an expression is not closed")
            parts.append(("expr", text[start + len(OPEN) : end - 1].strip()))
            start = text.find(OPEN, i)
        elif start != -1 and i < start:
            parts.append(("text", text[i:start]))
            i = start
        else:
            parts.append(("text", text[i:]))
            break
    return parts


def _runner_expression(text: str) -> str:
    """The single expression that the runner evaluates for the template string ``text``."""
    parts = _segments(text)
    if len(parts) == 1 and parts[0][0] == "expr":
        return parts[0][1]
    pieces: list[str] = []
    arguments: list[str] = []
    for kind, value in parts:
        if kind == "text":
            pieces.append(value.replace("'", "''").replace("{", "{{").replace("}", "}}"))
        else:
            pieces.append("{" + str(len(arguments)) + "}")
            arguments.append(", " + value)
    return "format('" + "".join(pieces) + "'" + "".join(arguments) + ")"


def _measured_length(text: str) -> int:
    """What GitHub measures against the limit for ``text``: 0 when it is not a template."""
    if OPEN not in text:
        return 0
    return _utf16_units(_runner_expression(text))


def _budget_length(text: str) -> int:
    """The length that is held against the budget: 0 for a string that is no template.

    For a template it is the larger of the string's characters (the measure that the request for
    this guard names) and the length of the expression that the runner builds from it, in UTF-16
    units (the quantity that GitHub's limit is applied to).  Neither is always the larger: quotes
    and braces lengthen the expression, while each ``${{ x }}`` becomes ``{n}`` and an argument
    ``, x``, which is shorter.
    """
    if OPEN not in text:
        return 0
    return max(len(text), _measured_length(text))


def _offenders(runs: Iterable[RunString]) -> list[str]:
    """One message for each ``run:`` string that is a template and whose length reaches the budget."""
    messages: list[str] = []
    for run in runs:
        length = _budget_length(run.text)
        if length >= LENGTH_BUDGET:
            messages.append(
                f"{run.file}: {run.where}: {len(run.text):,} characters in the string and "
                f"{_measured_length(run.text):,} UTF-16 units in the expression that GitHub builds "
                f"from it; the larger, {length:,}, is at or above the budget of {LENGTH_BUDGET:,}; "
                f"GitHub refuses an expression of more than {EXPRESSION_LENGTH_LIMIT:,}"
            )
    return messages


def _run_strings(node: object, file: str, path: str = "") -> Iterator[RunString]:
    """Every ``run`` key with a string value, at any depth, with the name or id of its step."""
    if isinstance(node, dict):
        label = str(node.get("name") or node.get("id") or "")
        for key, value in node.items():
            if key == "run" and isinstance(value, str):
                yield RunString(file, path + (f" [{label}]" if label else ""), value)
            else:
                yield from _run_strings(value, file, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from _run_strings(item, file, f"{path}[{index}]")


def _yaml_files() -> list[Path]:
    """Every YAML file under the action and workflow folders, in a fixed order."""
    found = [
        path
        for folder in YAML_ROOTS
        for path in folder.rglob("*")
        if path.is_file() and path.suffix in {".yml", ".yaml"}
    ]
    return sorted(found)


def _repository_run_strings() -> list[RunString]:
    """Every ``run:`` string of every YAML file under the action and workflow folders."""
    strings: list[RunString] = []
    for path in _yaml_files():
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        strings.extend(_run_strings(document, path.relative_to(ROOT).as_posix()))
    return strings


class TestRepositoryRunStrings:
    """The ``run:`` strings of the workflow and action files as they are in the repository."""

    def test_run_templates_when_measured_then_each_is_under_the_budget(self) -> None:
        offenders = _offenders(_repository_run_strings())

        assert not offenders, (
            "a run: string that holds an expression is read as one expression of limited length "
            "('The template is not valid ... Exceeded max expression length "
            f"{EXPRESSION_LENGTH_LIMIT}'). Put the script in a file next to the YAML file, start "
            "it from a short run: line and pass values through env: (see "
            ".github/actions/security-audit/action.yml):\n" + "\n".join(offenders)
        )

    def test_sweep_when_run_on_the_repository_then_it_finds_templates_in_both_folders(
        self,
    ) -> None:
        files = {path.relative_to(ROOT).as_posix() for path in _yaml_files()}
        templates = [run for run in _repository_run_strings() if OPEN in run.text]

        assert ".github/actions/security-audit/action.yml" in files
        assert ".github/workflows/ci.yml" in files
        assert any(run.file.startswith(".github/actions/") for run in templates)
        assert any(run.file.startswith(".github/workflows/") for run in templates)


class TestMeasure:
    """How a string is measured: the expression that the runner builds, in UTF-16 units."""

    def test_string_without_an_expression_when_measured_then_it_is_no_template(self) -> None:
        assert _measured_length("x" * 30_000) == 0
        assert _measured_length("echo '{}' }} {{") == 0

    def test_string_with_an_expression_when_measured_then_the_format_call_is_counted(self) -> None:
        text = "a${{ x }}b"

        assert _runner_expression(text) == "format('a{0}b', x)"
        assert _measured_length(text) == len("format('a{0}b', x)") == 18

    def test_quotes_and_braces_when_measured_then_each_is_doubled(self) -> None:
        text = "it's {a} ${{ x }} done"

        assert _runner_expression(text) == "format('it''s {{a}} {0} done', x)"

    def test_two_expressions_when_measured_then_they_become_two_arguments(self) -> None:
        text = "${{ a }}-${{ b.c }}"

        assert _runner_expression(text) == "format('{0}-{1}', a, b.c)"

    def test_string_that_is_one_expression_when_measured_then_it_is_not_wrapped(self) -> None:
        assert _runner_expression("${{ inputs.fail-on-vuln }}") == "inputs.fail-on-vuln"

    def test_closing_braces_inside_a_quoted_string_when_measured_then_they_do_not_end_it(
        self,
    ) -> None:
        parts = _segments("x ${{ format('}}', 1) }} y")

        assert parts == [("text", "x "), ("expr", "format('}}', 1)"), ("text", " y")]

    def test_character_outside_the_basic_plane_when_measured_then_it_counts_twice(self) -> None:
        text = "\U0001f600${{ x }}"

        assert _measured_length(text) == len("format('{0}', x)") + 2

    def test_expression_that_is_not_closed_when_measured_then_it_is_an_error(self) -> None:
        with pytest.raises(ValueError, match="not closed"):
            _measured_length("echo ${{ inputs.x")


class TestBudget:
    """What is held against the budget: the larger of the string's characters and the runner's expression."""

    @staticmethod
    def _expression_heavy(length: int) -> str:
        """A template of exactly ``length`` characters: 60 short expressions, no quote and no brace.

        The runner turns each ``${{ needs.build.result }}`` into ``{n}`` plus an argument
        ``, needs.build.result``, which is 1 or 2 characters shorter, so the expression it builds is
        shorter than the string (the "Check all jobs passed" step of ci.yml is a real example: 1,557
        characters, 1,548 measured).  Here the expression is 60 shorter.
        """
        body = 'echo "job ${{ needs.build.result }}"\n' * 60
        text = body + "#" + "x" * (length - len(body) - 2) + "\n"
        assert len(text) == length
        return text

    def test_template_of_the_budget_in_characters_when_its_expression_is_shorter_then_it_is_flagged(
        self,
    ) -> None:
        text = self._expression_heavy(LENGTH_BUDGET)

        assert len(text) == LENGTH_BUDGET
        # The expression alone, 60 characters shorter than the string, would let it pass:
        assert _measured_length(text) == LENGTH_BUDGET - 60
        assert _budget_length(text) == LENGTH_BUDGET
        assert len(_offenders([RunString("w.yml", "jobs.j.steps[0]", text)])) == 1

    def test_template_one_character_under_the_budget_when_checked_then_it_is_not_flagged(
        self,
    ) -> None:
        text = self._expression_heavy(LENGTH_BUDGET - 1)

        assert len(text) == LENGTH_BUDGET - 1
        assert _budget_length(text) == LENGTH_BUDGET - 1
        assert _offenders([RunString("w.yml", "jobs.j.steps[0]", text)]) == []

    def test_template_whose_expression_is_longer_than_the_string_when_checked_then_the_expression_counts(
        self,
    ) -> None:
        # Every quote and brace of the text is doubled in the expression:
        text = "it's {a} " * 2_000 + "${{ x }}"

        assert _measured_length(text) > len(text)
        assert _budget_length(text) == _measured_length(text)

    def test_plain_script_over_the_budget_when_checked_then_it_is_not_flagged(self) -> None:
        text = "x" * 40_000

        assert _budget_length(text) == 0
        assert _offenders([RunString("w.yml", "jobs.j.steps[0]", text)]) == []

    def test_flagged_template_when_reported_then_the_message_names_both_lengths(self) -> None:
        text = self._expression_heavy(LENGTH_BUDGET + 500)

        (message,) = _offenders([RunString("w.yml", "jobs.j.steps[0] [Long]", text)])

        assert "w.yml: jobs.j.steps[0] [Long]: 18,500 characters in the string" in message
        assert "18,440 UTF-16 units in the expression" in message
        assert "the larger, 18,500, is at or above the budget of 18,000" in message


class TestScan:
    """The scan finds an over-long template in either file shape, and nothing else."""

    @staticmethod
    def _padded(length: int) -> str:
        """A template string whose expression is exactly ``length`` UTF-16 units long."""
        # format('<n times x>{0}', x) is 8 + n + 3 + 1 + 3 + 1 = n + 16 characters.
        text = "x" * (length - 16) + "${{ x }}"
        assert _measured_length(text) == length
        return text

    def test_limit_and_margin_when_read_then_the_budget_is_the_documented_18000(self) -> None:
        assert (EXPRESSION_LENGTH_LIMIT, LIMIT_MARGIN, LENGTH_BUDGET) == (21_000, 3_000, 18_000)

    def test_template_when_it_reaches_the_budget_then_it_is_over_and_one_less_is_not(self) -> None:
        assert _budget_length(self._padded(LENGTH_BUDGET)) >= LENGTH_BUDGET
        assert _budget_length(self._padded(LENGTH_BUDGET - 1)) < LENGTH_BUDGET

    def test_workflow_step_when_scanned_then_its_run_string_is_found(self) -> None:
        document = {
            "jobs": {"scan": {"steps": [{"name": "Long", "run": self._padded(LENGTH_BUDGET)}]}}
        }

        found = list(_run_strings(document, "w.yml"))

        assert [(run.file, run.where) for run in found] == [("w.yml", "jobs.scan.steps[0] [Long]")]
        assert _budget_length(found[0].text) >= LENGTH_BUDGET

    def test_composite_action_step_when_scanned_then_its_run_string_is_found(self) -> None:
        document = {
            "runs": {"using": "composite", "steps": [{"id": "audit", "run": "echo ${{ x }}"}]}
        }

        found = list(_run_strings(document, "a.yml"))

        assert [(run.where, run.text) for run in found] == [
            ("runs.steps[0] [audit]", "echo ${{ x }}")
        ]

    def test_defaults_run_mapping_when_scanned_then_it_is_not_a_run_string(self) -> None:
        document = {"defaults": {"run": {"shell": "bash", "working-directory": "${{ x }}"}}}

        assert list(_run_strings(document, "w.yml")) == []

    def test_long_plain_script_when_scanned_then_it_is_found_but_is_no_template(self) -> None:
        document = {"jobs": {"j": {"steps": [{"run": "x" * 40_000}]}}}

        found = list(_run_strings(document, "w.yml"))

        assert len(found) == 1 and _measured_length(found[0].text) == 0

    def test_block_scalar_when_parsed_from_yaml_and_scanned_then_it_is_measured_whole(self) -> None:
        lines = "".join("          echo line\n" for _ in range(2_000))
        text = "jobs:\n  j:\n    steps:\n      - run: |\n" + lines + "          echo ${{ x }}\n"

        found = list(_run_strings(yaml.safe_load(text), "w.yml"))

        assert len(found) == 1 and _budget_length(found[0].text) >= LENGTH_BUDGET

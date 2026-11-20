# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests of how the workflow runs the script, and of the shell step after it.

The workflow runs ``python3 -I scripts/release/assemble_release.py``. Isolated
mode ignores ``PYTHON*`` variables and the user's site directory, and leaves the
script's own folder off ``sys.path``, so the script must be one file that imports
only the standard library. These tests pin that, and they run the release notes
step of ``release.yml`` with real ``bash`` and ``git`` against commit subjects
that carry control characters and runner commands.
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import REPO_ROOT, VERSION, assert_inert_output  # noqa: E402

pytestmark = pytest.mark.unit

SCRIPT = REPO_ROOT / "scripts" / "release" / "assemble_release.py"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "release.yml"


# --- the script as a program --------------------------------------------------------------------


def test_the_script_imports_nothing_but_the_standard_library() -> None:
    """The release script imports only standard-library modules."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0, "a relative import needs a package; the script runs as one file"
            modules.add((node.module or "").split(".")[0])
    outside = sorted(modules - set(sys.stdlib_module_names) - {"__future__"})
    assert outside == []


def test_the_script_uses_nothing_newer_than_python_3_11() -> None:
    """The release script parses as Python 3.11, so it uses no newer syntax."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), feature_version=(3, 11))
    assert tree.body


def test_the_script_runs_in_isolated_mode_and_ignores_planted_modules(tmp_path: Path) -> None:
    """In isolated mode the script ignores a planted json module that a normal run loads."""
    planted = tmp_path / "planted"
    planted.mkdir()
    (planted / "json.py").write_text(
        "raise SystemExit('a planted json module was imported')\n", encoding="utf-8"
    )
    env = {"PATH": os.environ["PATH"], "PYTHONPATH": str(planted)}
    control = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"],
        cwd=planted,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (
        "planted json module" in control.stderr + control.stdout
    )  # the control: without -I it would be imported
    isolated = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "--help"],
        cwd=planted,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert isolated.returncode == 0, isolated.stderr
    assert "--sbom-dir" in isolated.stdout
    assert "--output-dir" in isolated.stdout


def test_the_script_run_as_a_program_ends_with_one_rejected_line_and_status_one(
    tmp_path: Path,
) -> None:
    """Run as a program, a refusal prints a single REJECTED line and exits with status 1."""
    not_a_repository = tmp_path / "plain"
    not_a_repository.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            str(SCRIPT),
            "--sbom-dir",
            str(tmp_path / "sbom"),
            "--output-dir",
            str(tmp_path / "dist"),
            "--repo",
            str(not_a_repository),
            "--work-dir",
            str(tmp_path),
        ],
        env={"PATH": os.environ["PATH"], "HOME": str(tmp_path), "GITHUB_EVENT_NAME": "push"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    lines = result.stdout.splitlines()
    assert lines[-1].startswith("REJECTED: ")
    assert sum(1 for line in lines if line.startswith("REJECTED:")) == 1
    assert "Traceback" not in result.stdout + result.stderr
    assert not (tmp_path / "dist").exists()


@pytest.mark.parametrize("arguments", [[], ["--bogus"], ["--sbom-dir"]])
def test_a_command_line_mistake_of_the_program_ends_with_one_rejected_line_and_status_one(
    arguments: list[str],
) -> None:
    """A command-line mistake gives a single REJECTED line and exit status 1."""
    result = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), *arguments],
        env={"PATH": os.environ["PATH"]},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    lines = result.stdout.splitlines()
    assert [line for line in lines if line.startswith("REJECTED:")] == [lines[-1]]
    assert "command line" in lines[-1]
    assert result.stderr == ""  # no usage text from the parser


def test_the_help_of_the_program_exits_with_status_zero() -> None:
    """The program's --help exits with status 0."""
    result = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "-h"],
        env={"PATH": os.environ["PATH"]},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--output-dir" in result.stdout


# --- the shell step that writes the release notes ----------------------------------------------------


def notes_step() -> str:
    """Return the shell text of the step that writes the release notes."""
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = [
        step
        for step in workflow["jobs"]["release"]["steps"]
        if "git log" in str(step.get("run", "")) and "release-notes.md" in str(step.get("run", ""))
    ]
    assert len(steps) == 1
    assert steps[0]["env"] == {"VERSION": "${{ steps.pack.outputs.version }}"}
    return str(steps[0]["run"])


def available_shells() -> list[str]:
    """Return the bash programs to try: the one on PATH and the system one, if they differ.

    The step must also run under the old bash 3.2 that macOS ships (``/bin/bash``): the
    repository's host passes have always held that, and the runner's own bash is newer.
    """
    found: list[str] = []
    for candidate in (shutil.which("bash"), "/bin/bash"):
        if candidate and os.path.exists(candidate):
            if os.path.realpath(candidate) not in {os.path.realpath(path) for path in found}:
                found.append(candidate)
    return found


SHELLS = available_shells()


def run_notes(
    script: str, repo: Path, commit: str, runner_temp: Path, version: str, shell: str = "bash"
) -> subprocess.CompletedProcess[str]:
    """Run the notes step with bash, as the runner would, in a repository."""
    script_path = runner_temp / "notes-step.sh"
    script_path.write_text(script, encoding="utf-8")
    return subprocess.run(
        [shell, "-e", str(script_path)],
        cwd=repo,
        env={
            "PATH": os.environ["PATH"],
            "HOME": str(runner_temp),
            "VERSION": version,
            "GITHUB_SHA": commit,
            "GITHUB_WORKSPACE": str(repo),
            "RUNNER_TEMP": str(runner_temp),
        },
        capture_output=True,
        text=True,
        check=False,
    )


HOSTILE_SUBJECTS = [
    "feat: carriage\r::error::boom",
    "fix: escape \x1b[31mred\x1b[0m text",
    "chore: ##[add-mask]secret here",
    "docs: arrow → stays in the notes",
    "refactor: tab\tinside and a bell \x07 and a null-ish \x01 char",
]


@pytest.fixture
def hostile_repo(
    make_repo: Callable[..., tuple[Path, str]], git_in: Callable[..., str]
) -> tuple[Path, str]:
    """Make a repository with a previous tag and commits whose subjects are hostile."""
    repo, first = make_repo()
    git_in(repo, "tag", "v1.2.2", first)
    for subject in HOSTILE_SUBJECTS:
        git_in(repo, "commit", "--allow-empty", "-q", "-m", subject)
    return repo, git_in(repo, "rev-parse", "HEAD")


@pytest.mark.parametrize("shell", SHELLS)
def test_the_notes_step_drops_control_characters_from_the_notes_and_keeps_the_window_balanced(
    shell: str, hostile_repo: tuple[Path, str], tmp_path: Path
) -> None:
    """The notes step strips control characters and keeps its start and end markers paired."""
    repo, commit = hostile_repo
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commit, runner_temp, VERSION, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    lines = result.stdout.splitlines()
    assert lines[0].startswith("::stop-commands::")
    token = lines[0][len("::stop-commands::") :]
    assert len(token) == 32
    assert lines[-1] == f"::{token}::"
    assert_inert_output("\n".join(lines[1:-1]))
    notes = (runner_temp / "release-notes.md").read_bytes().decode("utf-8")
    assert notes.startswith(f"## Jerry Framework v{VERSION}\n")
    assert "### What's Changed" in notes
    assert "→" in notes  # the notes keep characters that are not control characters
    for char in notes:
        assert char in "\n\t" or ord(char) >= 0x20 and ord(char) != 0x7F, repr(char)
    subjects = [line for line in notes.splitlines() if line.startswith("- ")]
    assert len(subjects) == len(HOSTILE_SUBJECTS)
    assert "feat: carriage::error::boom" in notes


@pytest.mark.parametrize("shell", SHELLS)
def test_the_notes_step_prints_the_notes_without_anything_the_runner_could_read_as_a_command(
    shell: str, hostile_repo: tuple[Path, str], tmp_path: Path
) -> None:
    """The release-notes step prints no line the runner could take as a workflow command."""
    repo, commit = hostile_repo
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commit, runner_temp, VERSION, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    inside = result.stdout.splitlines()[1:-1]
    assert any("Release notes from v1.2.2" in line for line in inside)
    assert not any(line.lstrip().startswith("::") for line in inside)
    assert not any("##[" in line for line in inside)
    assert not any("\r" in line or "\x1b" in line for line in inside)
    assert any(line.startswith("- feat: carriage") for line in inside)


@pytest.mark.parametrize("shell", SHELLS)
def test_the_notes_step_uses_all_commits_when_there_is_no_previous_tag(
    shell: str, make_repo: Callable[..., tuple[Path, str]], tmp_path: Path
) -> None:
    """With no earlier tag, the release-notes step lists every commit."""
    repo, commit = make_repo()
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commit, runner_temp, VERSION, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "No previous tag found, using all commits" in result.stdout


@pytest.mark.parametrize("shell", SHELLS)
@pytest.mark.parametrize(
    "version", ["", "1.2", "1.2.3; touch evil", "1.2.3\n::error::x", "v1.2.3", "$(id)"]
)
def test_the_notes_step_refuses_a_version_that_is_not_a_version(
    shell: str, version: str, hostile_repo: tuple[Path, str], tmp_path: Path
) -> None:
    """The release-notes step refuses a version string that is not a version number."""
    repo, commit = hostile_repo
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commit, runner_temp, version, shell)
    assert result.returncode != 0
    assert not (runner_temp / "release-notes.md").exists()
    assert not (repo / "evil").exists()


# --- the marker that stops the version bump: cut out of the subjects, every commit kept ----------

SKIP_BUMP_MARKER = "[skip-bump]"

# Each case is the subject of a commit and the subject as the notes must list it (None where
# only the absence of the marker matters). The commit that the version bump makes ends its
# subject with the marker, and so do others, several of them security fixes: the marker is cut
# out and the commit stays in the list. version-bump.yml skips a bump when
# contains(github.event.head_commit.message, '[skip-bump]') is true, and that function "is not
# case sensitive" (GitHub's documentation of expressions), so the cut ignores case too. One
# blank takes the place of the marker and of the blanks next to it, so a cut never joins the
# two sides of the marker.
MARKER_CASES = [
    pytest.param(
        "chore(release): bump version to v1.2.3 [skip-bump]",
        "chore(release): bump version to v1.2.3",
        id="the-version-commit",
    ),
    pytest.param("fix: before [skip-bump] after", "fix: before after", id="in-the-middle"),
    pytest.param("[skip-bump] fix: at the start", "fix: at the start", id="at-the-start"),
    pytest.param("fix: one [skip-bump] two [skip-bump]", "fix: one two", id="twice"),
    # A cut that left nothing in its place would make a marker out of this one. What stays of
    # the two halves is not the point, so the text is not pinned: no marker may be left.
    pytest.param("fix: a [skip-[skip-bump]bump] b", None, id="one-inside-another"),
    # The control characters are removed first, so these markers are whole when they are cut.
    pytest.param("fix: a [skip-\x01bump] b", "fix: a b", id="a-control-character-inside"),
    pytest.param("fix: a [skip-bump\x7f] b", "fix: a b", id="a-delete-character-inside"),
    pytest.param("fix: a [SKIP-BUMP] b", "fix: a b", id="in-capitals"),
    pytest.param("fix: a [Skip-Bump] b", "fix: a b", id="in-mixed-case"),
    pytest.param("docs: arrow → [skip-bump]", "docs: arrow →", id="with-an-arrow"),
    pytest.param("[skip-bump]fix: no blank", "fix: no blank", id="glued-to-the-bullet"),
    pytest.param("chore: ##[skip-bump][add-mask]x", "chore: ## [add-mask]x", id="joins-nothing"),
    # Text that is not the marker stays as it is.
    pytest.param("fix: [skip-bumps] stays", "fix: [skip-bumps] stays", id="one-letter-more"),
    pytest.param("fix: skip-bump stays", "fix: skip-bump stays", id="no-brackets"),
    pytest.param("fix: [skip bump] stays", "fix: [skip bump] stays", id="a-blank-for-the-hyphen"),
    pytest.param("fix: [skip-bump stays", "fix: [skip-bump stays", id="not-closed"),
    pytest.param("fix: [skip-\tbump] stays", "fix: [skip-\tbump] stays", id="a-tab-inside"),
    pytest.param(
        "fix(api): [WIP] handle [id] and (x) stays",
        "fix(api): [WIP] handle [id] and (x) stays",
        id="other-brackets",
    ),
    pytest.param(
        "feat:  two  blanks  stay", "feat:  two  blanks  stay", id="blanks-away-from-a-marker"
    ),
]


def repo_with_subjects(
    make_repo: Callable[..., tuple[Path, str]], git_in: Callable[..., str], subjects: list[str]
) -> tuple[Path, list[str]]:
    """Make a repository with a previous tag and one commit for each subject.

    Returns the repository and the ids of the new commits, oldest first.
    """
    repo, first = make_repo()
    git_in(repo, "tag", "v1.2.2", first)
    commits = []
    for subject in subjects:
        git_in(repo, "commit", "--allow-empty", "-q", "-m", subject)
        commits.append(git_in(repo, "rev-parse", "HEAD"))
    return repo, commits


def split_item(item: str) -> tuple[str, str]:
    """Split a line of the list, ``- <subject> (<hash>)``, into the subject and the short hash."""
    match = re.fullmatch(r"- (.*) \(([0-9a-f]{7,40})\)", item)
    assert match, item
    return match.group(1), match.group(2)


@pytest.mark.parametrize("shell", SHELLS)
@pytest.mark.parametrize(("subject", "listed"), MARKER_CASES)
def test_the_notes_step_cuts_the_skip_bump_marker_out_of_a_subject_and_keeps_the_commit(
    shell: str,
    subject: str,
    listed: str | None,
    make_repo: Callable[..., tuple[Path, str]],
    git_in: Callable[..., str],
    tmp_path: Path,
) -> None:
    """A subject is listed without the marker; text that is not the marker is listed as it is."""
    repo, commits = repo_with_subjects(make_repo, git_in, [subject])
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commits[-1], runner_temp, VERSION, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    notes = (runner_temp / "release-notes.md").read_bytes().decode("utf-8")
    items = [line for line in notes.splitlines() if line.startswith("- ")]
    assert len(items) == 1, items  # the commit is kept in the list, not dropped
    assert SKIP_BUMP_MARKER not in notes.lower(), f"the marker is in the release notes: {items}"
    printed = "\n".join(result.stdout.splitlines()[1:-1])  # inside the window of the log
    assert SKIP_BUMP_MARKER not in printed.lower(), "the marker is in the printed notes"
    text, short = split_item(items[0])
    if listed is not None:
        assert text == listed
    assert commits[-1].startswith(short)  # the short hash is the one of the commit


@pytest.mark.parametrize("shell", SHELLS)
def test_the_notes_step_lists_every_commit_that_carries_the_marker_and_keeps_its_promises(
    shell: str,
    make_repo: Callable[..., tuple[Path, str]],
    git_in: Callable[..., str],
    tmp_path: Path,
) -> None:
    """Commits with the marker stay in the list, newest first, and the notes stay inert."""
    history = [  # oldest first: the subject of the commit, and the subject as it is listed
        (
            "fix(security): pin the actions by commit id [skip-bump]",
            "fix(security): pin the actions by commit id",
        ),
        ("feat: arrow → stays in the notes", "feat: arrow → stays in the notes"),
        ("chore: ##[skip-bump][add-mask]secret here", "chore: ## [add-mask]secret here"),
        (
            "chore(release): bump version to v1.2.3 [skip-bump]",
            "chore(release): bump version to v1.2.3",
        ),
    ]
    repo, commits = repo_with_subjects(make_repo, git_in, [subject for subject, _ in history])
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commits[-1], runner_temp, VERSION, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    lines = result.stdout.splitlines()
    assert lines[0].startswith("::stop-commands::")
    assert lines[-1] == f"::{lines[0][len('::stop-commands::') :]}::"
    assert_inert_output("\n".join(lines[1:-1]))
    assert SKIP_BUMP_MARKER not in result.stdout.lower()
    notes = (runner_temp / "release-notes.md").read_bytes().decode("utf-8")
    assert notes.startswith(f"## Jerry Framework v{VERSION}\n")
    assert SKIP_BUMP_MARKER not in notes.lower()
    assert "→" in notes  # the notes keep characters that are not control characters
    found = [split_item(line) for line in notes.splitlines() if line.startswith("- ")]
    assert [text for text, _ in found] == [listed for _, listed in reversed(history)]
    for (_, short), commit in zip(found, reversed(commits), strict=True):
        assert commit.startswith(short)


# --- the size of the release notes: a cap before the attestation (GitHub refuses a release
# --- body of more than 125,000 characters, after the attestation has been made) ---------------


def long_subject_repo(
    make_repo: Callable[..., tuple[Path, str]],
    git_in: Callable[..., str],
    *,
    commits: int,
    length: int,
) -> tuple[Path, str]:
    """Make a repository whose last ``commits`` subjects are ``length`` characters long."""
    repo, first = make_repo()
    git_in(repo, "tag", "v1.2.2", first)
    for number in range(commits):
        git_in(repo, "commit", "--allow-empty", "-q", "-m", f"feat: {'a' * length} {number}")
    return repo, git_in(repo, "rev-parse", "HEAD")


@pytest.mark.parametrize("shell", SHELLS)
def test_the_notes_step_refuses_notes_above_the_cap_with_a_reason(
    shell: str,
    make_repo: Callable[..., tuple[Path, str]],
    git_in: Callable[..., str],
    tmp_path: Path,
) -> None:
    """The release-notes step refuses notes over the size cap and says why."""
    repo, commit = long_subject_repo(make_repo, git_in, commits=4, length=30_000)
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commit, runner_temp, VERSION, shell)
    assert result.returncode != 0
    lines = result.stdout.splitlines()
    rejected = [line for line in lines if line.startswith("REJECTED:")]
    assert len(rejected) == 1, result.stdout[:2000]
    assert "release notes" in rejected[0]
    assert "bytes" in rejected[0]
    # The window in which the runner does not read commands is still closed, and the notes
    # are not left behind for a later step to use.
    assert lines[0].startswith("::stop-commands::")
    assert lines[-1] == f"::{lines[0][len('::stop-commands::') :]}::"
    assert not (runner_temp / "release-notes.md").exists()
    assert_inert_output("\n".join(lines[1:-1]))
    assert len(result.stdout) < 5000  # the oversized notes were not printed


@pytest.mark.parametrize("shell", SHELLS)
def test_the_notes_step_accepts_notes_just_under_the_cap(
    shell: str,
    make_repo: Callable[..., tuple[Path, str]],
    git_in: Callable[..., str],
    tmp_path: Path,
) -> None:
    """The release-notes step accepts notes just below the size cap."""
    repo, commit = long_subject_repo(make_repo, git_in, commits=3, length=30_000)
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    result = run_notes(notes_step(), repo, commit, runner_temp, VERSION, shell)
    assert result.returncode == 0, result.stdout[:500] + result.stderr
    size = (runner_temp / "release-notes.md").stat().st_size
    assert 90_000 < size <= 100_000


# --- the pack step runs the committed bytes of the script, not the work tree --------------------

COMMITTED_PROGRAM = 'import sys\nprint("committed program ran")\nprint("argv:", sys.argv[1:])\n'
TAMPERED_PROGRAM = 'print("TAMPERED PROGRAM RAN")\n'
SCRIPT_PATH = "scripts/release/assemble_release.py"


def pack_step() -> str:
    """Return the shell text of the step that runs the script."""
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = [
        step
        for step in workflow["jobs"]["release"]["steps"]
        if "assemble_release.py" in str(step.get("run", ""))
    ]
    assert len(steps) == 1
    return str(steps[0]["run"])


def run_pack(
    repo: Path, sha: str, runner_temp: Path, shell: str = "bash"
) -> subprocess.CompletedProcess[str]:
    """Run the pack step with bash, as the runner would, with python3 and git on the path."""
    bin_dir = runner_temp / "bin"
    bin_dir.mkdir(exist_ok=True)
    link = bin_dir / "python3"
    if not link.exists():
        link.symlink_to(sys.executable)
    script_path = runner_temp / "pack-step.sh"
    script_path.write_text(pack_step(), encoding="utf-8")
    return subprocess.run(
        [shell, "-e", str(script_path)],
        cwd=repo,
        env={
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "HOME": str(runner_temp),
            "GITHUB_SHA": sha,
            "GITHUB_WORKSPACE": str(repo),
            "RUNNER_TEMP": str(runner_temp),
        },
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def repo_with_program(
    make_repo: Callable[..., tuple[Path, str]], tmp_path: Path
) -> tuple[Path, str, Path]:
    """Make a repository that has a small program committed at the script's path."""
    repo, commit = make_repo({SCRIPT_PATH: COMMITTED_PROGRAM})
    runner_temp = tmp_path / "runner"
    runner_temp.mkdir()
    return repo, commit, runner_temp


@pytest.mark.parametrize("shell", SHELLS)
def test_the_pack_step_runs_the_committed_program_with_the_fixed_arguments(
    shell: str, repo_with_program: tuple[Path, str, Path]
) -> None:
    """The pack step runs the committed script with its fixed arguments."""
    repo, commit, runner_temp = repo_with_program
    result = run_pack(repo, commit, runner_temp, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "committed program ran" in result.stdout
    expected = ["--sbom-dir", f"{runner_temp}/sbom-in", "--output-dir", f"{repo}/dist"]
    assert f"argv: {expected}" in result.stdout


@pytest.mark.parametrize("shell", SHELLS)
def test_the_pack_step_does_not_run_a_changed_copy_in_the_work_tree(
    shell: str, repo_with_program: tuple[Path, str, Path]
) -> None:
    """The pack step runs the committed script, not an edited copy in the work tree."""
    repo, commit, runner_temp = repo_with_program
    (repo / SCRIPT_PATH).write_text(TAMPERED_PROGRAM, encoding="utf-8")
    result = run_pack(repo, commit, runner_temp, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "committed program ran" in result.stdout
    assert "TAMPERED" not in result.stdout + result.stderr


@pytest.mark.parametrize("shell", SHELLS)
def test_the_pack_step_does_not_run_a_link_that_stands_in_the_work_tree(
    shell: str, repo_with_program: tuple[Path, str, Path], tmp_path: Path
) -> None:
    """The pack step ignores a symbolic link put in place of the script in the work tree."""
    repo, commit, runner_temp = repo_with_program
    elsewhere = tmp_path / "elsewhere.py"
    elsewhere.write_text(TAMPERED_PROGRAM, encoding="utf-8")
    (repo / SCRIPT_PATH).unlink()
    os.symlink(elsewhere, repo / SCRIPT_PATH)
    result = run_pack(repo, commit, runner_temp, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "committed program ran" in result.stdout
    assert "TAMPERED" not in result.stdout + result.stderr


@pytest.mark.parametrize("shell", SHELLS)
def test_the_pack_step_does_not_need_the_file_to_be_in_the_work_tree(
    shell: str, repo_with_program: tuple[Path, str, Path]
) -> None:
    """The pack step works when the script is missing from the work tree."""
    repo, commit, runner_temp = repo_with_program
    (repo / SCRIPT_PATH).unlink()
    result = run_pack(repo, commit, runner_temp, shell)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "committed program ran" in result.stdout


@pytest.mark.parametrize("shell", SHELLS)
def test_the_pack_step_fails_and_runs_nothing_when_the_commit_has_no_such_file(
    shell: str, repo_with_program: tuple[Path, str, Path]
) -> None:
    """The pack step fails without running anything when the commit lacks the script."""
    repo, _, runner_temp = repo_with_program
    result = run_pack(repo, "0" * 40, runner_temp, shell)
    assert result.returncode != 0
    assert "committed program ran" not in result.stdout


@pytest.mark.parametrize("shell", SHELLS)
@pytest.mark.parametrize(
    "sha", ["", "main", "HEAD", "abc", "A" * 40, "0" * 39, "$(id)", "HEAD:README.md", "-n"]
)
def test_the_pack_step_refuses_a_commit_that_is_not_forty_lowercase_hex_digits(
    shell: str, sha: str, repo_with_program: tuple[Path, str, Path]
) -> None:
    """The pack step refuses a commit id that is not 40 lowercase hex digits."""
    repo, _, runner_temp = repo_with_program
    result = run_pack(repo, sha, runner_temp, shell)
    assert result.returncode != 0
    assert "committed program ran" not in result.stdout

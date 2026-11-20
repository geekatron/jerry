# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for a whole run of the release script, with fake ``tar`` and ``zip``.

A run is driven the way the workflow drives it: environment variables of the
run, a directory with the downloaded software bill of materials (SBOM), and an
output directory. The two
programs that make the archives are fakes that record how they were called and
write placeholder files, and the two readers that open a real archive are
replaced, so no archive is built, listed or unpacked here. What the run does
around them is real: real git, a real pack on disk, the real comparison.

Each failing run must end with exactly one ``REJECTED:`` line, a non-zero exit
status, and nothing written when the failure is one of the checks that come
before the pack.
"""

from __future__ import annotations

import os
import subprocess
import sys
import types
from collections.abc import Callable, Mapping
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import (  # noqa: E402
    CHILD_GIT_NAMES,
    HOSTILE_NAMES,
    SBOM_TEXT,
    STANDARD_FILES,
    STANDARD_LINKS,
    VERSION,
    assert_inert_output,
    packer_name_is_allowed,
)

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

TAR = f"jerry-plugin-{VERSION}.tar.gz"
ZIP = f"jerry-plugin-{VERSION}.zip"
KNOWN = {
    b".claude/patterns": b"../.context/patterns",
    b".claude/rules": b"../.context/rules",
}


@pytest.fixture
def run_main(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    fake_tools: Callable[..., types.SimpleNamespace],
    sbom_dir: Path,
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
) -> Callable[..., types.SimpleNamespace]:
    """Return a function that runs the script once and reports what happened."""

    def run(
        repo: Path,
        commit: str,
        environ: dict[str, str],
        *,
        tag: bool = True,
        tar_code: int = 0,
        zip_code: int = 0,
        tar_stderr: str = "",
        views: tuple[dict, dict] | None = None,
        sbom: Path | None = None,
        output_dir: Path | None = None,
        argv_extra: list[str] | None = None,
        use_defaults: bool = False,
    ) -> types.SimpleNamespace:
        fake = fake_tools(tar_code=tar_code, zip_code=zip_code, tar_stderr=tar_stderr)
        environ["PATH"] = os.environ["PATH"]  # the fake tools are first on it now
        if tag:
            make_tag(repo, f"v{VERSION}")
        set_origin_main(repo, commit)

        def expected_views() -> tuple[dict, dict]:
            entries = ar.read_tree(repo, commit, ar.git_environment(environ))
            expected = ar.expected_tree(entries, KNOWN)
            return (
                ar.archive_view(expected, links=True),
                ar.archive_view(expected, links=False),
            )

        monkeypatch.setattr(ar, "read_tar", lambda path, top: (views or expected_views())[0])
        monkeypatch.setattr(ar, "read_zip", lambda path, top: (views or expected_views())[1])
        out = output_dir or tmp_path / "dist"
        work = Path(environ["RUNNER_TEMP"])
        argv = ["--sbom-dir", str(sbom or sbom_dir)]
        if not use_defaults:
            argv += ["--output-dir", str(out), "--repo", str(repo), "--work-dir", str(work)]
        else:
            argv += ["--output-dir", str(out)]
        argv += argv_extra or []
        capsys.readouterr()
        code = ar.main(argv, environ if not use_defaults else None)
        captured = capsys.readouterr()
        return types.SimpleNamespace(
            code=code,
            out=captured.out,
            err=captured.err,
            output_dir=out,
            work_dir=work,
            fake=fake,
            environ=environ,
        )

    return run


def rejected_lines(out: str) -> list[str]:
    """Return the ``REJECTED:`` lines of a run's output."""
    return [line for line in out.splitlines() if line.startswith("REJECTED:")]


def assert_one_rejection(result: types.SimpleNamespace, contains: str) -> None:
    """Assert the run failed with exactly one REJECTED line, the last one, and inert output."""
    assert result.code == 1
    lines = rejected_lines(result.out)
    assert len(lines) == 1, result.out
    assert result.out.splitlines()[-1] == lines[0]
    assert contains in lines[0], lines[0]
    assert_inert_output(result.out)
    assert_inert_output(result.err)


def assert_nothing_written(result: types.SimpleNamespace) -> None:
    """Assert that the run created neither a work directory nor an output directory."""
    assert not result.output_dir.exists()
    assert list(result.work_dir.iterdir()) == []


# --- a release run --------------------------------------------------------------------------


def test_a_release_run_packs_checks_and_prints_the_checked_line(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A release run packs, checks the archives and prints the tag, commit and version line."""
    repo, commit = standard_repo
    result = run_main(repo, commit, run_environment(repo, commit))
    assert result.code == 0, result.out
    lines = result.out.splitlines()
    assert f"Checked: tag v{VERSION}, commit {commit}, version {VERSION}" in lines
    assert f"Files: {TAR}, {ZIP}, checksums.sha256, sbom.cyclonedx.json" in lines
    assert f"Version {VERSION}, commit {commit}" in lines
    assert not any(line.startswith("Check only") for line in lines)
    assert rejected_lines(result.out) == []
    assert_inert_output(result.out)
    assert sorted(path.name for path in result.output_dir.iterdir()) == sorted(
        [TAR, ZIP, "checksums.sha256", "sbom.cyclonedx.json"]
    )
    assert (result.output_dir / "sbom.cyclonedx.json").read_text(encoding="utf-8") == SBOM_TEXT
    assert [call["tool"] for call in result.fake.calls()] == ["tar", "zip"]


def test_a_release_run_writes_checksums_of_the_archives_that_the_tools_made(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A release run writes the checksums of the archives that tar and zip produced."""
    repo, commit = standard_repo
    result = run_main(repo, commit, run_environment(repo, commit))
    assert result.code == 0
    checksums = (result.output_dir / "checksums.sha256").read_text(encoding="utf-8").splitlines()
    assert checksums[0] == f"{ar.sha256_file(result.output_dir / TAR)}  {TAR}"
    assert checksums[1] == f"{ar.sha256_file(result.output_dir / ZIP)}  {ZIP}"


def test_a_release_run_leaves_a_pack_that_is_the_tagged_tree(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """After a release run, the pack folder matches the tagged tree."""
    repo, commit = standard_repo
    result = run_main(repo, commit, run_environment(repo, commit))
    assert result.code == 0
    (work,) = [path for path in result.work_dir.iterdir() if path.name.startswith("release-pack-")]
    top = work / "pack" / f"jerry-plugin-{VERSION}"
    entries = ar.read_tree(repo, commit, ar.git_environment({"PATH": os.environ["PATH"]}))
    ar.compare_trees("pack", ar.expected_tree(entries, KNOWN), ar.walk_pack(top))
    assert not (top / "CHANGELOG.md").exists()
    assert not (top / ".context").exists()


def test_a_release_run_makes_the_files_with_modes_that_do_not_depend_on_the_umask(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A release run sets file modes that do not depend on the umask."""
    repo, commit = standard_repo
    os.umask(0o077)
    result = run_main(repo, commit, run_environment(repo, commit))
    assert result.code == 0
    assert (result.output_dir / "checksums.sha256").stat().st_mode & 0o777 == 0o644
    assert (result.output_dir / "sbom.cyclonedx.json").stat().st_mode & 0o777 == 0o644


def test_a_release_run_writes_the_outputs_and_the_summary_for_the_later_steps(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    tmp_path: Path,
) -> None:
    """A release run writes the step outputs and the summary that the later steps read."""
    repo, commit = standard_repo
    github_output = tmp_path / "github-output"
    summary = tmp_path / "summary.md"
    environ = run_environment(
        repo,
        commit,
        extra={"GITHUB_OUTPUT": str(github_output), "GITHUB_STEP_SUMMARY": str(summary)},
    )
    result = run_main(repo, commit, environ)
    assert result.code == 0
    assert github_output.read_text(encoding="utf-8").splitlines() == [
        f"version={VERSION}",
        f"commit={commit}",
    ]
    text = summary.read_text(encoding="utf-8")
    assert f"**Version:** {VERSION}" in text
    assert f"**Commit:** {commit}" in text
    assert f"**Tag:** v{VERSION}" in text
    assert ar.sha256_file(result.output_dir / TAR) in text
    assert ar.sha256_file(result.output_dir / ZIP) in text
    assert_inert_output(text)


def test_a_run_without_output_files_set_writes_neither(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """Without GITHUB_OUTPUT and GITHUB_STEP_SUMMARY set, a run writes neither file."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    assert "GITHUB_OUTPUT" not in environ
    assert run_main(repo, commit, environ).code == 0


def test_a_run_ends_with_one_rejected_line_when_the_step_outputs_cannot_be_written(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    tmp_path: Path,
) -> None:
    """When the step outputs cannot be written, the run ends with a single REJECTED line."""
    repo, commit = standard_repo
    unwritable = tmp_path / "a-directory-not-a-file"
    unwritable.mkdir()
    environ = run_environment(repo, commit, extra={"GITHUB_OUTPUT": str(unwritable)})
    result = run_main(repo, commit, environ)
    assert_one_rejection(result, "could not write the step outputs")


def test_a_run_takes_the_repository_and_work_directory_from_the_environment_by_default(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without --repo and --work-dir, a run takes both folders from the environment."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    for name, value in environ.items():
        monkeypatch.setenv(name, value)
    result = run_main(repo, commit, environ, use_defaults=True)
    assert result.code == 0, result.out
    assert any(path.name.startswith("release-pack-") for path in result.work_dir.iterdir())


def test_a_run_without_a_checkout_directory_is_refused_before_anything_is_written(
    sbom_dir: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A run with no checkout folder is refused before anything is written."""
    environ = {
        "PATH": os.environ["PATH"],
        "GITHUB_EVENT_NAME": "push",
        "RUNNER_TEMP": str(tmp_path),
    }
    capsys.readouterr()
    code = ar.main(["--sbom-dir", str(sbom_dir), "--output-dir", str(tmp_path / "dist")], environ)
    out = capsys.readouterr().out
    assert code == 1
    assert out.splitlines()[-1].startswith("REJECTED: ")
    assert "GITHUB_WORKSPACE" in out
    assert not (tmp_path / "dist").exists()


def test_a_run_without_a_work_directory_is_refused_before_anything_is_written(
    sbom_dir: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A run with no work folder is refused before anything is written."""
    environ = {
        "PATH": os.environ["PATH"],
        "GITHUB_EVENT_NAME": "push",
        "GITHUB_WORKSPACE": str(tmp_path),
    }
    capsys.readouterr()
    code = ar.main(["--sbom-dir", str(sbom_dir), "--output-dir", str(tmp_path / "dist")], environ)
    out = capsys.readouterr().out
    assert code == 1
    assert out.splitlines()[-1].startswith("REJECTED: ")
    assert "RUNNER_TEMP" in out
    assert not (tmp_path / "dist").exists()


# --- a check-only run ----------------------------------------------------------------------------


def test_a_check_only_run_on_a_branch_says_so_checks_and_skips_the_tag(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A check-only run on a branch says so, runs the checks and skips the tag checks."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit, event="workflow_dispatch", tag=None)
    result = run_main(repo, commit, environ, tag=False)
    assert result.code == 0, result.out
    lines = result.out.splitlines()
    assert lines[0] == "Check only: the attestation and the release are skipped."
    assert "every check runs" not in result.out
    assert any(line.startswith("No tag on this ref") for line in lines)
    assert f"Checked: tag none, commit {commit}, version {VERSION}" in lines
    would = [line for line in lines if line.startswith("Check only: the release would be created")]
    assert len(would) == 1
    assert f"gh release create v{VERSION} --verify-tag" in would[0]
    assert "--prerelease" not in would[0]
    assert_inert_output(result.out)


def test_a_check_only_run_names_a_prerelease_in_the_command_it_would_run(
    make_repo: Callable[..., tuple[Path, str]],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A check-only run of a pre-release shows --prerelease in the command it would run."""
    repo, commit = make_repo({"pyproject.toml": "[project]\nversion = '2.0.0-rc.1'\n"})
    environ = run_environment(repo, commit, event="workflow_dispatch", tag=None)
    result = run_main(repo, commit, environ, tag=False)
    assert result.code == 0, result.out
    assert "gh release create v2.0.0-rc.1 --verify-tag" in result.out
    assert "--prerelease" in result.out


def test_a_check_only_run_from_a_tag_ref_still_runs_the_tag_checks(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    git_in: Callable[..., str],
) -> None:
    """A check-only run started from a tag ref still runs the tag checks."""
    repo, commit = standard_repo
    git_in(repo, "tag", f"v{VERSION}", commit)  # a lightweight tag
    environ = run_environment(repo, commit, event="workflow_dispatch")
    result = run_main(repo, commit, environ, tag=False)
    assert_one_rejection(result, "not an annotated tag")


# --- guard 2: no signing-request variable reaches a child process -----------------------------------


def test_the_script_removes_the_signing_request_variables_from_its_own_environment(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """The script removes both signing-request variables from the environment it was given."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" in environ
    result = run_main(repo, commit, environ)
    assert result.code == 0
    assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" not in environ
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" not in environ


def test_the_script_removes_the_variables_from_the_real_process_environment_too(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The script also removes the signing-request variables from its real process environment."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    for name, value in environ.items():
        monkeypatch.setenv(name, value)
    result = run_main(repo, commit, environ, use_defaults=True)
    assert result.code == 0, result.out
    assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" not in os.environ
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" not in os.environ


def test_no_child_process_of_a_whole_run_has_a_signing_request_variable(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No child process of a whole run receives a signing-request variable."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    seen: list[tuple[str, Mapping[str, str] | None]] = []
    real_run = subprocess.run
    real_popen = subprocess.Popen

    def recording_run(args: object, *a: object, **kw: object) -> object:
        seen.append((f"run {args}", kw.get("env")))  # type: ignore[arg-type]
        return real_run(args, *a, **kw)  # type: ignore[call-overload]

    class RecordingPopen(real_popen):  # type: ignore[misc, valid-type]
        def __init__(self, args: object, *a: object, **kw: object) -> None:
            seen.append((f"popen {args}", kw.get("env")))  # type: ignore[arg-type]
            super().__init__(args, *a, **kw)  # type: ignore[call-overload]

    monkeypatch.setattr(subprocess, "run", recording_run)
    monkeypatch.setattr(subprocess, "Popen", RecordingPopen)
    result = run_main(repo, commit, environ)
    assert result.code == 0, result.out
    programs = {entry.split()[1].strip("[]'\",") for entry, _ in seen}
    assert {"git", "tar", "zip"} <= programs
    assert len(seen) > 5
    for entry, env in seen:
        assert env is not None, f"{entry} inherited the whole environment"
        assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" not in env, entry
        assert "ACTIONS_ID_TOKEN_REQUEST_URL" not in env, entry
        assert "GITHUB_TOKEN" not in env, entry


def test_every_child_process_of_a_whole_run_receives_only_the_names_it_may_have(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """In a whole run, each child process gets only the environment names allowed for it."""
    repo, commit = standard_repo
    plain = run_environment(repo, commit)
    # A parent that holds every hostile name, besides the ones the run itself needs. Two of the
    # names are files that the script appends to, so they name files of this test, not "x" (a
    # relative name would put a file in the folder the tests run from).
    files = {"GITHUB_OUTPUT", "GITHUB_STEP_SUMMARY"}
    environ = run_environment(
        repo,
        commit,
        extra={
            name: str(tmp_path / f"{name}.txt") if name in files else "x"
            for name in HOSTILE_NAMES
            if name not in plain
        },
    )
    # Only the programs that the script starts count: the set-up of the test starts git too,
    # with the names that a test repository needs, so the record is kept while ``main`` runs.
    seen: list[tuple[str, Mapping[str, str] | None]] = []
    inside_main = {"now": False}
    real_run = subprocess.run
    real_popen = subprocess.Popen
    real_main = ar.main

    def recording_run(args: object, *a: object, **kw: object) -> object:
        if inside_main["now"]:
            seen.append((f"run {args}", kw.get("env")))  # type: ignore[arg-type]
        return real_run(args, *a, **kw)  # type: ignore[call-overload]

    class RecordingPopen(real_popen):  # type: ignore[misc, valid-type]
        def __init__(self, args: object, *a: object, **kw: object) -> None:
            if inside_main["now"]:
                seen.append((f"popen {args}", kw.get("env")))  # type: ignore[arg-type]
            super().__init__(args, *a, **kw)  # type: ignore[call-overload]

    def main_that_marks_its_time(*a: object, **kw: object) -> int:
        inside_main["now"] = True
        try:
            return real_main(*a, **kw)  # type: ignore[arg-type]
        finally:
            inside_main["now"] = False

    monkeypatch.setattr(subprocess, "run", recording_run)
    monkeypatch.setattr(subprocess, "Popen", RecordingPopen)
    monkeypatch.setattr(ar, "main", main_that_marks_its_time)
    result = run_main(repo, commit, environ)
    assert result.code == 0, result.out
    assert len(seen) > 5
    programs = set()
    for entry, env in seen:
        program = entry.split()[1].strip("[]'\",")
        programs.add(program)
        assert env is not None, f"{entry} inherited the whole environment"
        if program == "git":
            assert set(env) <= CHILD_GIT_NAMES, (entry, sorted(set(env) - CHILD_GIT_NAMES))
        else:
            assert program in {"tar", "zip"}, entry
            extra = sorted(name for name in env if not packer_name_is_allowed(name))
            assert not extra, (entry, extra)
    assert {"git", "tar", "zip"} <= programs


def test_the_packing_tools_of_a_whole_run_see_no_secret_of_the_job(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """In a whole run, tar and zip see none of the job's secrets."""
    repo, commit = standard_repo
    result = run_main(repo, commit, run_environment(repo, commit))
    assert result.code == 0
    for call in result.fake.calls():
        assert not {
            "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
            "ACTIONS_ID_TOKEN_REQUEST_URL",
            "GITHUB_TOKEN",
        } & set(call["env"])  # type: ignore[arg-type]


# --- guard 1: links; guard 3: entries that are not plain files; nothing is written ----------------


def test_a_run_refuses_a_top_level_file_that_is_a_link_before_it_writes_anything(
    make_repo: Callable[..., tuple[Path, str]],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    tmp_path: Path,
) -> None:
    """A top-level packed file that is a link is refused before any tool runs or file is written."""
    secret = tmp_path / "file-of-the-runner"
    secret.write_text("SECRET-OF-THE-RUNNER", encoding="utf-8")
    files = {name: text for name, text in STANDARD_FILES.items() if name != "README.md"}
    repo, commit = make_repo(
        files, links={**STANDARD_LINKS, "README.md": str(secret)}, standard=False
    )
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "README.md")
    assert_nothing_written(result)
    assert result.fake.calls() == []


def test_a_run_refuses_a_third_link_inside_a_packed_directory_before_it_writes_anything(
    make_repo: Callable[..., tuple[Path, str]],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A third link inside a packed folder is refused before anything is written."""
    repo, commit = make_repo(links={"docs/shortcut": "../src"})
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "not one of the two known")
    assert_nothing_written(result)


def test_a_run_refuses_a_known_link_that_was_retargeted_before_it_writes_anything(
    make_repo: Callable[..., tuple[Path, str]],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A known link with a changed target is refused before anything is written."""
    repo, commit = make_repo(links={".claude/rules": "../src"})
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "points somewhere else")
    assert_nothing_written(result)


def test_a_run_refuses_a_submodule_entry_before_it_writes_anything(
    make_repo: Callable[..., tuple[Path, str]],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A submodule entry under a packed path is refused before anything is written."""
    repo, commit = make_repo(gitlinks={"hooks/vendored": "a" * 40})
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "not a plain file or a symbolic link")
    assert_nothing_written(result)


def test_a_run_refuses_a_commit_that_lost_a_packed_path_before_it_writes_anything(
    make_repo: Callable[..., tuple[Path, str]],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A commit that lacks a packed path is refused before anything is written."""
    files = {name: text for name, text in STANDARD_FILES.items() if not name.startswith("hooks/")}
    repo, commit = make_repo(
        files,
        standard=False,
        links={".claude/patterns": "../.context/patterns", ".claude/rules": "../.context/rules"},
    )
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "nothing at the packed path hooks")
    assert_nothing_written(result)


def test_a_run_prints_nothing_that_the_runner_could_read_as_a_command_for_a_hostile_file_name(
    make_repo: Callable[..., tuple[Path, str]],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A hostile file name in the commit never yields a log line the runner reads as a command."""
    repo, commit = make_repo({"docs/\n::error::pwned\n##[add-mask]x": "text\n"})
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "control character")
    assert_nothing_written(result)


# --- guard 4: the output directory must not exist before packing ----------------------------------


def test_a_run_refuses_an_output_directory_that_already_exists(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    tmp_path: Path,
) -> None:
    """A run refuses an existing output folder and leaves its files untouched."""
    repo, commit = standard_repo
    existing = tmp_path / "dist"
    existing.mkdir()
    (existing / "jerry-plugin-1.2.3.zip").write_bytes(b"a zip that the tracked tree carried")
    result = run_main(repo, commit, run_environment(repo, commit), output_dir=existing)
    assert_one_rejection(result, "output directory exists before packing")
    assert (
        existing / "jerry-plugin-1.2.3.zip"
    ).read_bytes() == b"a zip that the tracked tree carried"
    assert result.fake.calls() == []


def test_a_run_refuses_a_link_in_place_of_the_output_directory(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    tmp_path: Path,
) -> None:
    """A run refuses a link in place of the output folder and writes nothing where it points."""
    repo, commit = standard_repo
    link = tmp_path / "dist"
    os.symlink(tmp_path / "somewhere-else", link)
    result = run_main(repo, commit, run_environment(repo, commit), output_dir=link)
    assert_one_rejection(result, "output directory exists before packing")
    assert not (tmp_path / "somewhere-else").exists()


# --- the SBOM ---------------------------------------------------------------------------------------


def test_a_run_refuses_an_sbom_that_is_not_json_before_it_writes_anything(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    sbom_dir: Path,
) -> None:
    """An SBOM that is not JSON is refused before anything is written."""
    repo, commit = standard_repo
    (sbom_dir / "sbom.cyclonedx.json").write_text("not json", encoding="utf-8")
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "not valid JSON")
    assert_nothing_written(result)


def test_a_run_refuses_a_second_file_in_the_sbom_directory(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    sbom_dir: Path,
) -> None:
    """A second file in the SBOM folder stops the run."""
    repo, commit = standard_repo
    (sbom_dir / "extra.txt").write_text("x", encoding="utf-8")
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "exactly the one file")
    assert_nothing_written(result)


# --- the run, the tag, the version -----------------------------------------------------------------------


def test_a_run_refuses_a_push_that_is_not_a_tag(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A push event whose ref is not a tag is refused."""
    repo, commit = standard_repo
    environ = run_environment(
        repo, commit, tag=None, extra={"GITHUB_REF": "refs/heads/::stop-commands::x"}
    )
    result = run_main(repo, commit, environ, tag=False)
    assert_one_rejection(result, "a release is made from a tag push")
    assert_nothing_written(result)


def test_a_run_refuses_an_event_that_is_neither_a_push_nor_a_manual_check(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """An event other than a push or a manual check-only run is refused."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit, event="::set-output name=a::b")
    result = run_main(repo, commit, environ)
    assert_one_rejection(result, "tag push or a manual check")
    assert_nothing_written(result)


def test_a_run_refuses_a_tag_whose_version_is_not_the_version_of_pyproject(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    make_tag: Callable[..., str],
) -> None:
    """A tag whose version differs from the one in pyproject.toml is refused."""
    repo, commit = standard_repo
    make_tag(repo, "v9.9.9")
    environ = run_environment(repo, commit, tag="v9.9.9")
    result = run_main(repo, commit, environ, tag=False)
    assert_one_rejection(result, "version of the tag (9.9.9)")
    assert_nothing_written(result)


def test_a_run_refuses_a_checkout_that_is_not_the_top_of_a_work_tree(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A checkout folder that is not the top of a work tree is refused."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    result = run_main(repo, commit, environ, argv_extra=["--repo", str(repo / "docs")])
    assert_one_rejection(result, "top of a work tree")


# --- the tools and the archives -----------------------------------------------------------------------


def test_a_run_stops_with_the_reason_when_tar_fails(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """When tar fails, the run stops with the reason and never calls zip."""
    repo, commit = standard_repo
    result = run_main(
        repo,
        commit,
        run_environment(repo, commit),
        tar_code=2,
        tar_stderr="tar: ::error::could not write\n##[add-mask]x\n",
    )
    assert_one_rejection(result, "tar failed with exit status 2")
    assert [call["tool"] for call in result.fake.calls()] == ["tar"]


def test_a_run_refuses_a_tar_that_lists_other_members_than_the_tagged_tree_implies(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A tar whose members differ from what the tagged tree implies is refused."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    entries = ar.read_tree(repo, commit, ar.git_environment(environ))
    expected = ar.expected_tree(entries, KNOWN)
    short = ar.archive_view(expected, links=True)
    del short[b"docs/guide.md"]
    result = run_main(repo, commit, environ, views=(short, ar.archive_view(expected, links=False)))
    assert_one_rejection(result, "the tar lists")
    assert "implies" in result.out


def test_a_run_refuses_a_zip_that_holds_a_link(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A zip that holds a link is refused."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    entries = ar.read_tree(repo, commit, ar.git_environment(environ))
    expected = ar.expected_tree(entries, KNOWN)
    result = run_main(
        repo,
        commit,
        environ,
        views=(ar.archive_view(expected, links=True), ar.archive_view(expected, links=True)),
    )
    assert_one_rejection(result, "the zip lists")


def test_a_run_refuses_a_pack_that_a_tool_changed_while_it_ran(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A pack changed after it was written is refused before tar or zip runs."""
    repo, commit = standard_repo
    real_write_pack = ar.write_pack

    def tampering_write_pack(top: Path, entries: object, read_object: object) -> None:
        real_write_pack(top, entries, read_object)  # type: ignore[arg-type]
        (top / "README.md").write_bytes(b"changed after it was written\n")

    monkeypatch.setattr(ar, "write_pack", tampering_write_pack)
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "not the tagged tree")
    assert result.fake.calls() == []  # no archive is made from a pack that differs from the commit


def test_a_run_refuses_a_pack_where_a_known_link_resolves(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A pack where a known link would resolve to a packed file is refused before any tool runs."""
    repo, commit = standard_repo
    real_write_pack = ar.write_pack

    def writing_write_pack(top: Path, entries: object, read_object: object) -> None:
        real_write_pack(top, entries, read_object)  # type: ignore[arg-type]
        (top / ".context").mkdir()
        (top / ".context" / "rules").mkdir()

    monkeypatch.setattr(ar, "write_pack", writing_write_pack)
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "resolves in the pack")
    assert result.fake.calls() == []


# --- failures of another kind --------------------------------------------------------------------------


def test_a_run_ends_with_one_rejected_line_when_something_unexpected_happens(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unexpected error ends the run with a single REJECTED line and no traceback."""
    repo, commit = standard_repo

    def explode(*args: object, **kwargs: object) -> str:
        raise RuntimeError("::error::boom\n##[add-mask]secret")

    monkeypatch.setattr(ar, "check_head", explode)
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "unexpected RuntimeError")
    assert "Traceback" not in result.out
    assert "Traceback" not in result.err


def test_a_run_ends_with_one_rejected_line_when_a_file_cannot_be_written(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When a file cannot be written, the run ends with a single REJECTED line."""
    repo, commit = standard_repo

    def disk_full(*args: object, **kwargs: object) -> None:
        raise OSError(28, "No space left on device: ::error::x")

    monkeypatch.setattr(ar, "write_pack", disk_full)
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "OSError")


def test_a_run_refuses_a_python_that_is_older_than_the_oldest_supported(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A run on a Python older than the oldest supported version is refused."""
    repo, commit = standard_repo
    monkeypatch.setattr(ar, "MIN_PYTHON", (99, 0))
    result = run_main(repo, commit, run_environment(repo, commit))
    assert_one_rejection(result, "python 99.0 or newer is required")
    assert_nothing_written(result)


def test_require_python_accepts_the_oldest_supported_version_and_newer() -> None:
    """require_python accepts the oldest supported Python and any newer one."""
    ar.require_python((3, 11, 0, "final", 0))
    ar.require_python((3, 12, 3, "final", 0))
    ar.require_python((4, 0, 0, "final", 0))


@pytest.mark.parametrize(
    "old", [(3, 10, 14, "final", 0), (3, 9, 0, "final", 0), (2, 7, 18, "final", 0)]
)
def test_require_python_rejects_an_older_version_and_names_both(old: tuple) -> None:
    """require_python refuses an older Python and names both versions."""
    with pytest.raises(ar.Rejected) as info:
        ar.require_python(old)
    assert "python 3.11 or newer is required" in str(info.value)
    assert f"{old[0]}.{old[1]}.{old[2]}" in str(info.value)


def test_parse_args_turns_a_missing_option_into_a_rejection(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """parse_args turns a missing required option into a refusal."""
    with pytest.raises(ar.Rejected) as info:
        ar.parse_args(["--sbom-dir", "x"])
    assert "--output-dir" in str(info.value)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""  # no usage text, no exit through argparse


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["--bogus"],
        ["--sbom-dir"],
        ["--sbom-dir", "/a", "--output-dir"],
        ["--sbom-dir", "/a", "--output-dir", "/b", "extra"],
        ["--sbom-dir", "/a", "--output-dir", "/b", "--bogus", "1"],
        ["--sbom-dir", "/a", "--output-dir", "/b", "--repo"],
        ["--sbom-dir", "/a", "--output", "/b"],  # an abbreviation of an option is not accepted
        ["::error::x"],
    ],
)
def test_a_command_line_mistake_ends_as_one_rejected_line_and_status_one(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    """A command-line mistake ends the run with a single REJECTED line and status 1."""
    capsys.readouterr()
    code = ar.main(argv, {"PATH": os.environ["PATH"]})
    captured = capsys.readouterr()
    assert code == 1
    lines = rejected_lines(captured.out)
    assert len(lines) == 1, captured.out
    assert captured.out.splitlines()[-1] == lines[0]
    assert "command line" in lines[0]
    assert_inert_output(captured.out)
    assert captured.err == ""
    assert "Traceback" not in captured.out


def test_help_still_exits_with_status_zero_and_prints_the_options(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """--help exits with status 0 and lists the options."""
    with pytest.raises(SystemExit) as info:
        ar.parse_args(["--help"])
    assert info.value.code == 0
    printed = capsys.readouterr().out
    assert "--sbom-dir" in printed
    assert "--output-dir" in printed
    assert "absolute" in printed  # the help says the directories must be absolute paths


# --- the four directories must be absolute paths ---------------------------------------------


@pytest.mark.parametrize("option", ["--output-dir", "--sbom-dir", "--repo", "--work-dir"])
def test_a_relative_directory_option_is_refused_with_a_clear_reason_before_anything_is_written(
    option: str,
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    run_main: Callable[..., types.SimpleNamespace],
) -> None:
    """A relative folder option is refused, with the reason, before anything is written."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    result = run_main(repo, commit, environ, argv_extra=[option, "relative/folder"])
    assert_one_rejection(result, f"{option} must be an absolute path")
    assert "relative/folder" in result.out
    assert_nothing_written(result)
    assert result.fake.calls() == []


@pytest.mark.parametrize(
    ("variable", "other"),
    [("GITHUB_WORKSPACE", "RUNNER_TEMP"), ("RUNNER_TEMP", "GITHUB_WORKSPACE")],
)
def test_a_relative_directory_from_the_run_is_refused_too(
    variable: str,
    other: str,
    sbom_dir: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A relative folder taken from the environment is refused as well."""
    environ = {
        "PATH": os.environ["PATH"],
        "GITHUB_EVENT_NAME": "push",
        other: str(tmp_path),
        variable: "relative/folder",
    }
    capsys.readouterr()
    code = ar.main(["--sbom-dir", str(sbom_dir), "--output-dir", str(tmp_path / "dist")], environ)
    out = capsys.readouterr().out
    assert code == 1
    assert out.splitlines()[-1].startswith("REJECTED: ")
    assert f"{variable} must be an absolute path" in out
    assert not (tmp_path / "dist").exists()


def test_parse_args_reads_the_options() -> None:
    """parse_args reads the four folder options."""
    args = ar.parse_args(["--sbom-dir", "a", "--output-dir", "b", "--repo", "c", "--work-dir", "d"])
    assert (args.sbom_dir, args.output_dir, args.repo, args.work_dir) == ("a", "b", "c", "d")


def test_parse_args_leaves_the_optional_directories_to_the_environment() -> None:
    """parse_args leaves --repo and --work-dir unset when not given, for the environment to fill."""
    args = ar.parse_args(["--sbom-dir", "a", "--output-dir", "b"])
    assert args.repo is None
    assert args.work_dir is None

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests of the repository itself against the assumptions of the release script.

The script packs a fixed list of paths and accepts exactly two tracked links. If
the repository drifts away from that, a release fails at the tag. These tests
make the drift fail at review time instead:

- every top-level tracked entry is either packed or on an explicit list of
  entries that are not packed, so a new top-level entry has to be classified;
- the tracked links under the packed paths are the two known ones;
- no git attribute makes a checkout differ from the blob that the pack holds;
- the tag text that the version bump workflow writes is the text that the
  script expects;
- the structure of ``release.yml`` keeps the properties that the release
  depends on: write access for one job only, pinned actions, no credentials on
  disk, one script call, and the order of the steps.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import REPO_ROOT, git_env  # noqa: E402

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "release.yml"
SCRIPT = "scripts/release/assemble_release.py"

# Top-level tracked entries that the archives do not hold. A new top-level entry must be
# added here, or to PACKED_DIRS / PACKED_FILES in the script, before the test passes.
NOT_PACKED = {
    ".context",
    ".gitattributes",
    ".github",
    ".nojekyll",
    ".pre-commit-config.yaml",
    "CHANGELOG.md",
    "CNAME",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    "NOTICE",
    "SECURITY.md",
    "SOUNDTRACK.md",
    "TOOL_REGISTRY.yaml",
    "commands",
    "mkdocs.yml",
    "overrides",
    "projects",
    "runbooks",
    "schemas",
    "tests",
    "uv.lock",
}


def git_raw(home: Path, *args: str, stdin: bytes | None = None) -> bytes:
    """Run git in this repository with a clean environment and return the raw output."""
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        input=stdin,
        capture_output=True,
        env=git_env(home),
        check=True,
    ).stdout


@pytest.fixture(scope="module")
def contract_home(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Make a private home directory for the git calls of this module."""
    return tmp_path_factory.mktemp("contract-home")


@pytest.fixture(scope="module")
def tracked(contract_home: Path) -> list[tuple[str, bytes, str]]:
    """Return ``(mode, path, blob id)`` for every file in the index of this repository."""
    if shutil.which("git") is None or not (REPO_ROOT / ".git").exists():
        pytest.skip("this check needs a git work tree")
    raw = git_raw(contract_home, "ls-files", "-s", "-z")
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, _, path = record.partition(b"\t")
        mode, oid, _stage = meta.split(b" ")
        entries.append((mode.decode(), path, oid.decode()))
    return entries


def top_level(path: bytes) -> str:
    """Return the first component of a tracked path."""
    return path.split(b"/")[0].decode("utf-8", "surrogateescape")


# --- the packed paths and the not-packed list ---------------------------------------------------


def test_every_top_level_tracked_entry_is_packed_or_on_the_explicit_not_packed_list(
    tracked: list[tuple[str, bytes, str]],
) -> None:
    """A new top-level file or folder fails here until it is classed as packed or not packed."""
    packed = set(ar.PACKED_DIRS) | set(ar.PACKED_FILES)
    names = {top_level(path) for _, path, _ in tracked}
    unclassified = sorted(names - packed - NOT_PACKED)
    assert unclassified == [], (
        f"new top-level entries {unclassified}: add each to PACKED_DIRS or PACKED_FILES in "
        f"{SCRIPT}, or to NOT_PACKED in this test"
    )


def test_every_packed_path_is_tracked_and_has_the_right_shape(
    tracked: list[tuple[str, bytes, str]],
) -> None:
    """Each packed path exists in git with the expected kind, folder or file."""
    for name in ar.PACKED_FILES:
        assert any(path == name.encode() for _, path, _ in tracked), f"{name} is not tracked"
    for name in ar.PACKED_DIRS:
        assert any(path.startswith(name.encode() + b"/") for _, path, _ in tracked), (
            f"nothing is tracked under {name}"
        )


def test_the_not_packed_list_names_no_packed_path() -> None:
    """No path is on both the packed and the not-packed lists."""
    assert not NOT_PACKED & (set(ar.PACKED_DIRS) | set(ar.PACKED_FILES))


def test_nothing_tracked_lies_under_the_output_directory(
    tracked: list[tuple[str, bytes, str]],
) -> None:
    """git tracks nothing under dist/, the folder the archives are written to."""
    # The output directory must not exist before packing, and a checkout makes it if a
    # file under dist/ is tracked (git add -f passes the ignore rule).
    assert [path for _, path, _ in tracked if top_level(path) == "dist"] == []


def test_the_packed_paths_are_unique_and_none_lies_inside_another() -> None:
    """The packed paths have no duplicates, and none sits inside another."""
    names = [*ar.PACKED_DIRS, *ar.PACKED_FILES]
    assert len(names) == len(set(names))
    assert all("/" not in name for name in names)


def test_the_packed_lists_are_the_ones_that_the_old_copy_step_used() -> None:
    """The packed folders and files are exactly those that the old copy step shipped."""
    assert ar.PACKED_DIRS == (
        ".claude",
        ".claude-plugin",
        "skills",
        "src",
        "docs",
        "scripts",
        "hooks",
    )
    assert ar.PACKED_FILES == (
        "CLAUDE.md",
        "AGENTS.md",
        "GOVERNANCE.md",
        "README.md",
        "pyproject.toml",
        "pytest.ini",
        ".gitignore",
    )


# --- the links ----------------------------------------------------------------------------------------


def test_the_tracked_links_under_the_packed_paths_are_exactly_the_two_known_ones(
    tracked: list[tuple[str, bytes, str]], contract_home: Path
) -> None:
    """The only symbolic links under the packed paths are the two known ones."""
    packed = set(ar.PACKED_DIRS) | set(ar.PACKED_FILES)
    found = {}
    for mode, path, oid in tracked:
        if mode == "120000" and top_level(path) in packed:
            found[path] = git_raw(contract_home, "cat-file", "blob", oid)
    assert found == ar.KNOWN_LINKS


def test_the_two_known_links_have_the_names_and_targets_that_the_release_was_made_with() -> None:
    """The two known links keep the names and targets of the earlier releases."""
    assert ar.KNOWN_LINKS == {
        b".claude/patterns": b"../.context/patterns",
        b".claude/rules": b"../.context/rules",
    }


def test_the_directory_that_the_two_links_point_into_is_not_packed() -> None:
    """The folder that the two links point into, .context, is not packed."""
    assert ".context" not in ar.PACKED_DIRS
    assert ".context" not in ar.PACKED_FILES


# --- attributes: the pack holds the blob, so no attribute may make a checkout differ ---------------------


def test_no_attribute_makes_a_checkout_of_a_packed_file_differ_from_its_blob(
    tracked: list[tuple[str, bytes, str]], contract_home: Path
) -> None:
    """No git attribute can make a checked-out packed file differ from its stored blob."""
    packed = set(ar.PACKED_DIRS) | set(ar.PACKED_FILES)
    paths = [path for mode, path, _ in tracked if mode != "120000" and top_level(path) in packed]
    output = git_raw(
        contract_home,
        "check-attr",
        "--cached",
        "-z",
        "--stdin",
        "filter",
        "ident",
        "working-tree-encoding",
        "eol",
        stdin=b"\0".join(paths) + b"\0",
    )
    fields = output.split(b"\0")
    problems = []
    for index in range(0, len(fields) - 2, 3):
        path, attribute, value = fields[index : index + 3]
        wrong_filter = attribute != b"eol" and value != b"unspecified"
        wrong_eol = attribute == b"eol" and value not in (b"unspecified", b"lf")
        if wrong_filter or wrong_eol:
            problems.append(
                (path.decode("utf-8", "surrogateescape"), attribute.decode(), value.decode())
            )
    assert len(fields) > 3 * len(paths)
    assert problems == [], (
        "a checkout would write other bytes than the blob; the pack holds the blob's bytes"
    )


# --- the tag contract ---------------------------------------------------------------------------------------


def test_the_version_bump_workflow_makes_the_tag_that_the_script_expects() -> None:
    """version-bump.yml sets the tagger name, email and message that the tag checks expect."""
    bump = (REPO_ROOT / ".github" / "workflows" / "version-bump.yml").read_text(encoding="utf-8")
    name, _, rest = ar.BOT.partition(" <")
    email = rest.rstrip(">")
    assert f'git config user.name "{name}"' in bump
    assert f'git config user.email "{email}"' in bump
    assert 'git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}"' in bump
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'tag_message = "Release v{new_version}"' in pyproject
    assert 'tag_name = "v{new_version}"' in pyproject


# --- the structure of release.yml ------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def workflow() -> dict:
    """Load release.yml."""
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def steps(workflow: dict, job: str) -> list[dict]:
    """Return the steps of a job."""
    return workflow["jobs"][job]["steps"]


def uses_of(step: dict) -> str:
    """Return the ``uses`` value of a step, or an empty string."""
    return str(step.get("uses", ""))


def run_of(step: dict) -> str:
    """Return the ``run`` text of a step, or an empty string."""
    return str(step.get("run", ""))


def test_the_workflow_has_the_four_jobs(workflow: dict) -> None:
    """release.yml has exactly the jobs validate, ci, build and release."""
    assert set(workflow["jobs"]) == {"validate", "ci", "build", "release"}


def test_only_the_release_job_can_write(workflow: dict) -> None:
    """Only the release job gets write permissions; every other job can only read."""
    assert workflow["permissions"] == {"contents": "read"}
    for name, job in workflow["jobs"].items():
        permissions = job.get("permissions", {})
        if name == "release":
            assert permissions == {
                "contents": "write",
                "id-token": "write",
                "attestations": "write",
            }
        else:
            assert permissions == {"contents": "read"}, name


@pytest.mark.parametrize("job", ["validate", "ci", "build", "release"])
def test_every_job_runs_on_the_pinned_image(workflow: dict, job: str) -> None:
    """Each of the four jobs runs on the pinned ubuntu-24.04 image."""
    assert workflow["jobs"][job]["runs-on"] == "ubuntu-24.04"


def test_the_ci_job_forces_the_archive_tests_on(workflow: dict) -> None:
    """The ci job sets JERRY_RELEASE_ARCHIVE_TESTS to 1, so a missing tar or zip fails."""
    test_steps = [step for step in steps(workflow, "ci") if step.get("name") == "Run tests"]
    assert len(test_steps) == 1
    assert test_steps[0].get("env", {}).get("JERRY_RELEASE_ARCHIVE_TESTS") == "1"


def test_every_action_is_pinned_to_a_full_commit_id(workflow: dict) -> None:
    """Every action the workflow uses is pinned to a full 40-character commit id."""
    for name, job in workflow["jobs"].items():
        for step in job["steps"]:
            used = uses_of(step)
            if used:
                assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", used), f"{name}: {used}"


def test_every_checkout_leaves_no_credentials_on_disk(workflow: dict) -> None:
    """All four checkout steps leave no credentials on disk (persist-credentials: false)."""
    found = 0
    for name, job in workflow["jobs"].items():
        for step in job["steps"]:
            if uses_of(step).startswith("actions/checkout@"):
                found += 1
                assert step["with"]["persist-credentials"] is False, name
    assert found == 4


def test_the_release_job_runs_only_the_three_pinned_actions_and_shell_steps(
    workflow: dict,
) -> None:
    """Apart from shell steps, release uses only the checkout, download and attestation actions."""
    used = {uses_of(step).split("@")[0] for step in steps(workflow, "release") if uses_of(step)}
    assert used == {
        "actions/checkout",
        "actions/download-artifact",
        "actions/attest-build-provenance",
    }


def test_no_job_puts_an_expression_into_shell_text(workflow: dict) -> None:
    """No run block holds a ${{ }} expression; values reach the shell through env."""
    # A value from outside (a tag name, an input, an output of another step) that is pasted
    # into shell text is run as shell. It goes through ``env:`` and is used as "$NAME".
    for name, job in workflow["jobs"].items():
        for step in job["steps"]:
            assert "${{" not in run_of(step), f"{name}: {step.get('name') or step}"


def test_the_validate_job_hands_the_version_to_its_shell_through_env(workflow: dict) -> None:
    """validate passes the version to its shell steps through env, not inline."""
    by_name = {step.get("name"): step for step in steps(workflow, "validate")}
    for name, variable in (
        ("Validate version format", "VERSION"),
        ("Check version in pyproject.toml", "TAG_VERSION"),
    ):
        step = by_name[name]
        assert step["env"] == {variable: "${{ steps.version.outputs.version }}"}, name
        assert f'"${variable}"' in run_of(step), name


def test_the_expression_test_is_not_empty_and_sees_every_run_block(workflow: dict) -> None:
    """The expression check finds run blocks in every job, so it cannot pass vacuously."""
    # A guard on the guard: there are run blocks to look at, in all four jobs.
    counts = {
        name: sum(1 for step in job["steps"] if run_of(step))
        for name, job in workflow["jobs"].items()
    }
    assert all(count > 0 for count in counts.values()), counts


def test_the_release_job_takes_no_value_from_the_outputs_of_other_jobs(workflow: dict) -> None:
    """The release job reads no output of another job through needs."""
    text = yaml.safe_dump(workflow["jobs"]["release"])
    assert "needs." not in text


def test_the_release_job_has_the_secret_token_in_one_step_only(workflow: dict) -> None:
    """Only the Create GitHub Release step of the release job sees the token."""
    holders = [
        step.get("name")
        for step in steps(workflow, "release")
        if "secrets." in yaml.safe_dump(step)
    ]
    assert holders == ["Create GitHub Release"]


def test_the_script_runs_in_isolated_mode_with_fixed_arguments_and_exists(workflow: dict) -> None:
    """The script exists and runs once, as python3 -I with fixed arguments."""
    calls = [
        run_of(step) for step in steps(workflow, "release") if "assemble_release.py" in run_of(step)
    ]
    assert len(calls) == 1
    assert "python3 -I -" in calls[0]
    assert '--sbom-dir "${RUNNER_TEMP}/sbom-in"' in calls[0]
    assert '--output-dir "${GITHUB_WORKSPACE}/dist"' in calls[0]
    assert (REPO_ROOT / SCRIPT).is_file()


def test_the_script_that_runs_is_the_committed_one_read_from_the_git_object(
    workflow: dict,
) -> None:
    """The workflow pipes the script from the commit's git object, not from the work tree."""
    # The job reads the file from the object of the commit that triggered the run and hands
    # it to python3 on standard input. Nothing is read from the work tree, so no earlier step
    # and no file in the work tree can change what runs. (The behaviour is tested in
    # test_script_invocation.py with real bash and git.)
    (call,) = [
        run_of(step) for step in steps(workflow, "release") if "assemble_release.py" in run_of(step)
    ]
    assert f'git cat-file blob "${{GITHUB_SHA}}:{SCRIPT}"' in call
    assert "| python3 -I -" in call
    assert "set -euo pipefail" in call  # a failed git must fail the step, not run an empty file
    assert "[0-9a-f]{40}" in call  # the commit id is checked before it is used
    assert f"python3 -I {SCRIPT}" not in call
    assert f"python3 {SCRIPT}" not in call


def test_the_release_job_prints_the_python_version_it_relies_on(workflow: dict) -> None:
    """The release job prints python3 --version before relying on it."""
    assert any("python3 --version" in run_of(step) for step in steps(workflow, "release"))


def test_the_release_steps_run_in_the_order_that_the_checks_need(workflow: dict) -> None:
    """The release steps run as checkout, download, script, notes, attestation, release."""
    release = steps(workflow, "release")

    def first(predicate: Callable[[dict], bool]) -> int:
        return next(index for index, step in enumerate(release) if predicate(step))

    checkout = first(lambda s: uses_of(s).startswith("actions/checkout@"))
    download = first(lambda s: uses_of(s).startswith("actions/download-artifact@"))
    script = first(lambda s: "assemble_release.py" in run_of(s))
    notes = first(lambda s: "git log" in run_of(s) and "release-notes.md" in run_of(s))
    attest = first(lambda s: uses_of(s).startswith("actions/attest-build-provenance@"))
    create = first(lambda s: s.get("name") == "Create GitHub Release")
    assert checkout < download < script < notes < attest < create


def test_the_attestation_and_the_release_run_on_a_push_only(workflow: dict) -> None:
    """The attestation and the GitHub release run only on a push event."""
    release = steps(workflow, "release")
    attest = next(s for s in release if uses_of(s).startswith("actions/attest-build-provenance@"))
    create = next(s for s in release if s.get("name") == "Create GitHub Release")
    assert attest["if"] == "github.event_name == 'push'"
    assert create["if"] == "github.event_name == 'push'"


def test_the_release_checkout_has_the_full_history_and_the_download_is_the_sbom_only(
    workflow: dict,
) -> None:
    """The release checkout fetches the full history, and the job downloads only the SBOM."""
    release = steps(workflow, "release")
    checkout = next(s for s in release if uses_of(s).startswith("actions/checkout@"))
    assert checkout["with"]["fetch-depth"] == 0
    download = next(s for s in release if uses_of(s).startswith("actions/download-artifact@"))
    assert download["with"] == {"name": "sbom", "path": "${{ runner.temp }}/sbom-in"}


def test_build_uploads_the_sbom_as_the_one_file_that_release_downloads(workflow: dict) -> None:
    """build uploads one artifact, the SBOM that release downloads."""
    uploads = [
        s for s in steps(workflow, "build") if uses_of(s).startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    options = uploads[0]["with"]
    assert options["name"] == "sbom"
    assert str(options["path"]).strip() == "dist/sbom.cyclonedx.json"
    assert options["if-no-files-found"] == "error"


def test_build_makes_no_archive_and_no_checksum_file(workflow: dict) -> None:
    """No build step runs tar, zip or sha256sum."""
    for step in steps(workflow, "build"):
        text = run_of(step)
        assert not re.search(r"\b(tar|zip|sha256sum)\b", text), step.get("name")
        assert "checksums.sha256" not in text


def test_the_manual_trigger_is_the_only_one_besides_the_tag_push(workflow: dict) -> None:
    """The workflow starts only on a v* tag push or by hand."""
    # YAML 1.1 reads the key ``on`` as the boolean True.
    triggers = workflow.get("on", workflow.get(True))
    assert triggers is not None
    assert set(triggers) == {"push", "workflow_dispatch"}
    assert triggers["push"] == {"tags": ["v*"]}


# --- who must review a change to the script and its tests (CODEOWNERS) ------------------------
#
# ``release.yml`` runs the script with the release tokens. The workflow file is protected by
# CODEOWNERS; the code it runs has to be protected the same way, or a change to the script alone
# needs the review of any account with write access. GitHub uses the LAST pattern that matches a
# file, so these tests also check that no later pattern takes the two paths away again.

CODEOWNERS = REPO_ROOT / ".github" / "CODEOWNERS"
RELEASE_OWNED = ("scripts/release/", "tests/unit/scripts/release/")
RELEASE_OWNER = ["@geekatron"]


def codeowners_rules() -> list[tuple[str, list[str]]]:
    """Read the rules of CODEOWNERS in file order, each as a pattern and its owners."""
    rules = []
    for line in CODEOWNERS.read_text(encoding="utf-8").splitlines():
        text = line.split("#", 1)[0].strip()
        if text:
            pattern, *owners = text.split()
            rules.append((pattern, owners))
    return rules


def codeowners_regex(pattern: str) -> re.Pattern[str]:
    """Turn a CODEOWNERS pattern into a regular expression, the way .gitignore reads it."""
    directory = pattern.endswith("/")
    body = pattern.rstrip("/")
    anchored = body.startswith("/") or "/" in body
    body = body.lstrip("/")
    out = ""
    index = 0
    while index < len(body):
        if body.startswith("**/", index):
            out += "(?:.*/)?"
            index += 3
        elif body.startswith("/**", index) and index + 3 == len(body):
            out += "/.*"
            index += 3
        elif body[index] == "*":
            out += "[^/]*"
            index += 1
        elif body[index] == "?":
            out += "[^/]"
            index += 1
        else:
            out += re.escape(body[index])
            index += 1
    start = "" if anchored else "(?:.*/)?"
    end = "/.*" if directory else "(?:/.*)?"
    return re.compile(f"^{start}{out}{end}$")


def code_owners_of(path: str) -> list[str]:
    """Return the owners of a file: the last pattern that matches decides."""
    owners: list[str] = []
    for pattern, who in codeowners_rules():
        if codeowners_regex(pattern).match(path):
            owners = who
    return owners


@pytest.mark.parametrize(
    ("pattern", "path", "expected"),
    [
        ("docs/governance/", "docs/governance/a.md", True),
        ("docs/governance/", "docs/other/governance/a.md", False),
        ("docs/governance/", "docs/governance", False),
        ("scripts/release/", "scripts/release/assemble_release.py", True),
        ("scripts/release/", "scripts/releases/x.py", False),
        ("scripts/release/", "x/scripts/release/a.py", False),
        (".pre-commit-config.yaml", ".pre-commit-config.yaml", True),
        (".pre-commit-config.yaml", "sub/.pre-commit-config.yaml", True),
        ("/Makefile", "Makefile", True),
        ("/Makefile", "sub/Makefile", False),
        ("*.py", "a/b/c.py", True),
        ("*.py", "a/b/c.pyc", False),
        ("docs/**/x.md", "docs/a/b/x.md", True),
    ],
)
def test_the_codeowners_matcher_of_these_tests_reads_patterns_like_github(
    pattern: str, path: str, expected: bool
) -> None:
    """This file's CODEOWNERS matcher reads patterns the way GitHub does."""
    assert bool(codeowners_regex(pattern).match(path)) is expected


def test_codeowners_names_the_release_script_and_its_tests_for_the_owner() -> None:
    """CODEOWNERS assigns the release script and its tests to the owner."""
    rules = dict(codeowners_rules())
    for pattern in RELEASE_OWNED:
        assert rules.get(pattern) == RELEASE_OWNER, pattern


def test_the_release_lines_of_codeowners_sit_with_the_pipeline_files_and_say_why() -> None:
    """In CODEOWNERS the release lines sit with the pipeline files, under a comment saying why."""
    lines = CODEOWNERS.read_text(encoding="utf-8").splitlines()
    first = next(index for index, line in enumerate(lines) if line.startswith("scripts/release/"))
    assert lines[first + 1].startswith("tests/unit/scripts/release/")
    assert lines[first - 1] == (
        "# release.yml runs this script with the release tokens, "
        "so a change to it needs the same review."
    )
    # the pipeline block: the line before the comment is another pipeline file of the block
    assert lines[first - 2].split()[0] in {
        ".github/workflows/",
        ".github/dependabot.yml",
        ".github/CODEOWNERS",
        ".pre-commit-config.yaml",
    }


def test_no_later_pattern_takes_the_release_script_or_its_tests_away_from_the_owner(
    tracked: list[tuple[str, bytes, str]],
) -> None:
    """No later CODEOWNERS pattern overrides the owner of the release script or its tests."""
    paths = [path.decode("utf-8") for _, path, _ in tracked]
    owned = [path for path in paths if path.startswith(RELEASE_OWNED)]
    assert SCRIPT in owned
    assert any(path.startswith("tests/unit/scripts/release/test_") for path in owned)
    for path in owned:
        assert code_owners_of(path) == RELEASE_OWNER, path
    # the last pattern that matches the script is the new line, not another one after it
    matching = [p for p, _ in codeowners_rules() if codeowners_regex(p).match(SCRIPT)]
    assert matching[-1] == "scripts/release/"
    assert matching.count("scripts/release/") == 1

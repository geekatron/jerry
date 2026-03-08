# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Prompt version key management for the PROJ-036 regression harness.

Implements FR-004: Version Key Management via Git Commit Hash.

A version key is a composite of the git commit hash and the agent definition
file path, used by the baseline store to index quality score arrays.

Composite key format: ``{git_commit_hash}:{file_path}``
Example: ``abc1234...:skills/problem-solving/agents/ps-researcher.md``

Security design:
    - Git commit hash is the source of truth for prompt version identity.
    - Baseline retrieval validates that the stored commit hash matches the
      current target branch commit hash before comparison (prevents stale
      baseline comparisons and baseline substitution attacks — threat T-35).
    - No user-supplied commit hashes are accepted without format validation.
    - Only full 40-character SHA-1 hashes are accepted. Abbreviated hashes
      are rejected to prevent key collisions in the baseline store.
    - File paths are validated against a known allowlist pattern to prevent
      path traversal attacks (threat T-02).

OWASP alignment:
    A03:2021 Injection — all inputs validated before use in subprocess calls.
    A04:2021 Insecure Design — version key enforces baseline integrity by design.

ASVS 5.0:
    V5.1 Input Validation — all external inputs (file_path, commit_hash) validated.
    V5.3 Output Encoding — no user-controlled data interpolated into shell commands.

FR traceability:
    FR-004: Version key composite format {commit_hash}:{file_path}
    FR-004 AC-1: Baseline record includes git commit hash and file path
    FR-004 AC-2: Baseline retrieval rejects mismatched commit hash
    FR-004 AC-3: Composite key format is {git_commit_hash}:{file_path}
"""

from __future__ import annotations

import hashlib
import re
import subprocess  # noqa: S404 — subprocess used with validated args only, no shell=True
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# ==============================================================================
# Constants
# ==============================================================================

# Regex pattern for validating git commit hash.
# Only full 40-character SHA-1 hashes are accepted. Abbreviated hashes are
# rejected to prevent key collisions in the baseline store. Use
# ``git rev-parse HEAD`` or ``git log -1 --format=%H`` to obtain the full hash.
_COMMIT_HASH_PATTERN: re.Pattern[str] = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)

# Allowlist for agent definition file paths (prevents path traversal — OWASP A03)
# Only files under skills/*/agents/*.md are valid agent definition paths
_AGENT_FILE_PATH_PATTERN: re.Pattern[str] = re.compile(
    r"^skills/[a-z0-9\-]+/agents/[a-z0-9\-]+\.md$",
    re.IGNORECASE,
)

# Full SHA-1 commit hash length (exactly 40 hex characters required)
_MAX_HASH_LENGTH: int = 40


class VersionKeyError(ValueError):
    """Raised when a version key cannot be constructed or validated.

    Inherits from ValueError to signal invalid input data.
    Callers should catch this exception and handle it explicitly
    rather than allowing it to propagate as an unhandled error.
    """


class BaselineMismatchError(VersionKeyError):
    """Raised when a baseline version key does not match the current branch.

    Per FR-004 AC-2: baseline retrieval rejects mismatched commit hash.
    This exception signals that the stored baseline was captured from a
    different commit than the one currently being evaluated.
    """


class EvaluationMode(str, Enum):
    """Evaluation tier controlling sample size and metric scope (FR-005).

    Smoke mode: structural checks only, no LLM calls.
    Standard mode: N >= 10 LLM evaluations with G-Eval metrics.
    Full mode: N >= 30 LLM evaluations with all four layers.

    Values are title-case to match the canonical definition in
    jerry.testing.types.EvaluationMode.  This standalone definition
    exists because version_keys.py runs inside the Docker container
    where the jerry package may not be installed.
    """

    SMOKE = "Smoke"
    STANDARD = "Standard"
    FULL = "Full"


# ==============================================================================
# Data Classes
# ==============================================================================


@dataclass(frozen=True)
class VersionKey:
    """Composite key identifying a specific prompt version.

    Combines git commit hash with the agent definition file path to
    produce an immutable, collision-resistant identifier for a specific
    version of a specific agent's system prompt.

    Attributes:
        commit_hash: Full 40-character git SHA-1 commit hash. Abbreviated
            hashes are not accepted to prevent key collisions.
        file_path: Repo-relative path to the agent definition file.
            Must match the pattern ``skills/*/agents/*.md``.

    Raises:
        VersionKeyError: If commit_hash is not 40 hex characters or
            file_path does not match the agent definition path pattern.

    Example:
        >>> key = VersionKey(
        ...     commit_hash="a" * 40,
        ...     file_path="skills/problem-solving/agents/ps-researcher.md",
        ... )
        >>> str(key)
        'aaaa...aaaa:skills/problem-solving/agents/ps-researcher.md'
    """

    commit_hash: str
    file_path: str

    def __post_init__(self) -> None:
        """Validate commit hash format and file path pattern.

        Raises:
            VersionKeyError: If any field fails validation.
        """
        _validate_commit_hash(self.commit_hash)
        _validate_agent_file_path(self.file_path)

    def __str__(self) -> str:
        """Return the composite key string in ``{commit_hash}:{file_path}`` format.

        This format is the canonical identifier used in the baseline store.
        """
        return f"{self.commit_hash}:{self.file_path}"

    @classmethod
    def from_string(cls, key_string: str) -> VersionKey:
        """Parse a composite key string into a VersionKey instance.

        Args:
            key_string: Composite key in ``{commit_hash}:{file_path}`` format.

        Returns:
            Parsed VersionKey with validated fields.

        Raises:
            VersionKeyError: If the string does not match expected format
                or either component fails individual validation.

        Example:
            >>> VersionKey.from_string("abc123...:" + "skills/problem-solving/agents/ps-researcher.md")
        """
        if ":" not in key_string:
            raise VersionKeyError(
                f"Invalid version key format: expected '{{commit_hash}}:{{file_path}}', "
                f"got '{key_string}'. "
                f"Composite key must contain ':' separator."
            )

        # Split on FIRST colon only (file paths may contain colons on some OSes)
        commit_hash, _, file_path = key_string.partition(":")
        return cls(commit_hash=commit_hash.strip(), file_path=file_path.strip())


@dataclass(frozen=True)
class BaselineVersionRecord:
    """A version key paired with its evaluation metadata.

    Used by the baseline store to record which prompt version produced
    a given baseline score array.

    Attributes:
        version_key: Composite key identifying the prompt version.
        evaluation_mode: The tier used when baseline was captured.
        run_count: Number of LLM evaluation runs in the baseline (N).
        captured_at_iso: ISO 8601 timestamp of baseline capture.
        model_id: LLM model identifier used for the baseline run.
    """

    version_key: VersionKey
    evaluation_mode: EvaluationMode
    run_count: int
    captured_at_iso: str
    model_id: str

    def validate_minimum_runs(self) -> None:
        """Validate that run count meets the minimum for the evaluation mode.

        Per FR-003: Smoke=1, Standard>=10, Full>=30.

        Raises:
            VersionKeyError: If run_count is below the mode minimum.
        """
        minimums = {
            EvaluationMode.SMOKE: 1,
            EvaluationMode.STANDARD: 10,
            EvaluationMode.FULL: 30,
        }
        minimum = minimums[self.evaluation_mode]
        if self.run_count < minimum:
            raise VersionKeyError(
                f"Baseline run count {self.run_count} is below minimum {minimum} "
                f"for evaluation mode '{self.evaluation_mode.value}'. "
                f"Re-capture the baseline with at least {minimum} runs."
            )


# ==============================================================================
# Validation Functions
# ==============================================================================


def _validate_commit_hash(commit_hash: str) -> None:
    """Validate that a commit hash is a valid full SHA-1 hex string.

    Args:
        commit_hash: Git commit hash to validate.

    Raises:
        VersionKeyError: If the hash is not exactly 40 lowercase hex characters.
            Full 40-character hashes are required (not abbreviated) to prevent
            key collisions in the baseline store.
    """
    if not commit_hash:
        raise VersionKeyError("Commit hash must not be empty.")

    if len(commit_hash) != _MAX_HASH_LENGTH:
        raise VersionKeyError(
            f"Commit hash must be exactly {_MAX_HASH_LENGTH} hex characters (full SHA-1), "
            f"got {len(commit_hash)} characters: '{commit_hash[:16]}...'. "
            f"Abbreviated hashes are not accepted to prevent key collisions. "
            f"Use 'git rev-parse HEAD' to obtain the full hash."
        )

    if not _COMMIT_HASH_PATTERN.match(commit_hash):
        raise VersionKeyError(
            f"Commit hash '{commit_hash[:16]}...' contains invalid characters. "
            f"Expected only [0-9a-fA-F]. "
            f"Ensure the hash was obtained from a git command, not user input."
        )


def _validate_agent_file_path(file_path: str) -> None:
    """Validate that a file path matches the agent definition allowlist.

    Only paths matching ``skills/*/agents/*.md`` are accepted.
    This prevents path traversal attacks (OWASP A03:2021 Injection).

    Args:
        file_path: Repo-relative path to validate.

    Raises:
        VersionKeyError: If the path does not match the agent definition pattern.
    """
    if not file_path:
        raise VersionKeyError("File path must not be empty.")

    # Reject absolute paths and path traversal patterns
    if file_path.startswith("/") or ".." in file_path:
        raise VersionKeyError(
            f"File path must be repo-relative and must not contain '..' traversal: '{file_path}'. "
            f"Expected format: 'skills/{{skill}}/agents/{{agent}}.md'."
        )

    if not _AGENT_FILE_PATH_PATTERN.match(file_path):
        raise VersionKeyError(
            f"File path '{file_path}' does not match agent definition pattern "
            f"'skills/*/agents/*.md'. "
            f"Only agent definition files are valid baseline keys."
        )


# ==============================================================================
# Git Integration
# ==============================================================================


def get_current_commit_hash(
    file_path: str,
    repo_root: Path | None = None,
) -> str:
    """Retrieve the full git commit hash for a specific file at HEAD.

    Uses ``git rev-parse HEAD`` to obtain the current commit hash.
    File path is validated before use in the subprocess call (OWASP A03).

    Args:
        file_path: Repo-relative agent definition file path (validated before use).
        repo_root: Optional path to repository root. Defaults to current directory.
            Used to ensure git commands run in the correct repository context.

    Returns:
        Full 40-character SHA-1 commit hash string.

    Raises:
        VersionKeyError: If the file path is invalid or git command fails.
        FileNotFoundError: If the file does not exist in the repository.

    Example:
        >>> hash_val = get_current_commit_hash("skills/problem-solving/agents/ps-researcher.md")
        >>> len(hash_val)
        40
    """
    _validate_agent_file_path(file_path)

    work_dir = repo_root or Path.cwd()

    # Security: use list form (not shell=True) to prevent shell injection (OWASP A03)
    # The file_path has been validated against the allowlist pattern above
    try:
        result = subprocess.run(  # noqa: S603 — validated args, no shell=True
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(work_dir),
            timeout=10,  # Prevent hanging in CI environments
        )
    except subprocess.CalledProcessError as exc:
        raise VersionKeyError(
            f"Failed to retrieve git commit hash for '{file_path}': {exc.stderr.strip()}. "
            f"Ensure this command runs inside a git repository."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise VersionKeyError(
            f"Git command timed out retrieving commit hash for '{file_path}'. "
            f"Check git repository health."
        ) from exc
    except FileNotFoundError as exc:
        raise VersionKeyError(
            "git executable not found. Ensure git is installed and available in PATH."
        ) from exc

    commit_hash = result.stdout.strip()
    _validate_commit_hash(commit_hash)
    return commit_hash


def get_file_last_commit_hash(
    file_path: str,
    repo_root: Path | None = None,
) -> str:
    """Retrieve the git commit hash of the most recent commit touching a specific file.

    Unlike ``get_current_commit_hash`` (which returns HEAD), this function returns
    the hash of the last commit that actually modified the file. This is the
    semantically correct key for baseline versioning: it identifies the prompt
    version, not the repository state at evaluation time.

    Args:
        file_path: Repo-relative agent definition file path.
        repo_root: Optional path to repository root.

    Returns:
        Full 40-character SHA-1 commit hash for the file's last modification.

    Raises:
        VersionKeyError: If the file has no git history or the path is invalid.

    Example:
        >>> hash_val = get_file_last_commit_hash(
        ...     "skills/problem-solving/agents/ps-researcher.md"
        ... )
        >>> len(hash_val)
        40
    """
    _validate_agent_file_path(file_path)

    work_dir = repo_root or Path.cwd()

    # Security: validated args, list form, no shell=True (OWASP A03)
    try:
        result = subprocess.run(  # noqa: S603
            ["git", "log", "-1", "--format=%H", "--", file_path],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(work_dir),
            timeout=10,
        )
    except subprocess.CalledProcessError as exc:
        raise VersionKeyError(
            f"Failed to retrieve last commit hash for '{file_path}': {exc.stderr.strip()}."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise VersionKeyError(f"Git command timed out for '{file_path}'.") from exc

    commit_hash = result.stdout.strip()

    if not commit_hash:
        raise VersionKeyError(
            f"No git history found for '{file_path}'. "
            f"The file may not be tracked by git, or the repository has no commits. "
            f"Add and commit the file before running baseline capture."
        )

    _validate_commit_hash(commit_hash)
    return commit_hash


def build_version_key(
    file_path: str,
    repo_root: Path | None = None,
    use_file_last_commit: bool = True,
) -> VersionKey:
    """Build a VersionKey for an agent definition file using its git history.

    The composite key uniquely identifies the exact content of the agent definition
    at a specific point in git history. Two identical file contents from different
    commits produce different keys (by commit hash); this is intentional —
    it prevents comparing against baselines captured before an intermediate change.

    Args:
        file_path: Repo-relative path to the agent definition file.
        repo_root: Optional repository root path. Defaults to current directory.
        use_file_last_commit: If True (default), use the hash of the last commit
            that modified this specific file (most precise baseline identification).
            If False, use HEAD commit hash (useful for newly staged files).

    Returns:
        VersionKey with validated commit hash and file path.

    Raises:
        VersionKeyError: If the file path is invalid or git command fails.

    Example:
        >>> key = build_version_key("skills/problem-solving/agents/ps-researcher.md")
        >>> print(key)  # abc123...:skills/problem-solving/agents/ps-researcher.md
    """
    if use_file_last_commit:
        commit_hash = get_file_last_commit_hash(file_path, repo_root)
    else:
        commit_hash = get_current_commit_hash(file_path, repo_root)

    return VersionKey(commit_hash=commit_hash, file_path=file_path)


# ==============================================================================
# Baseline Version Validation
# ==============================================================================


def validate_baseline_version_key(
    baseline_key: VersionKey,
    current_branch_key: VersionKey,
) -> None:
    """Validate that a stored baseline key matches the current branch state.

    Per FR-004 AC-2: baseline retrieval rejects mismatched commit hashes.

    This validation prevents comparing a PR branch against a baseline that was
    captured from a different state of the target branch. A mismatch indicates
    that the target branch has advanced since the baseline was captured, and the
    baseline should be refreshed before comparison.

    Args:
        baseline_key: The VersionKey stored with the baseline score array.
        current_branch_key: The VersionKey for the current target branch state.

    Raises:
        BaselineMismatchError: If the file paths differ or the commit hashes differ.
            The error message identifies which component mismatched to aid debugging.

    Example:
        >>> validate_baseline_version_key(
        ...     baseline_key=VersionKey(commit_hash="a" * 40, file_path="skills/x/agents/y.md"),
        ...     current_branch_key=VersionKey(commit_hash="a" * 40, file_path="skills/x/agents/y.md"),
        ... )
        # No exception: keys match
    """
    if baseline_key.file_path != current_branch_key.file_path:
        raise BaselineMismatchError(
            f"Baseline file path mismatch: "
            f"stored='{baseline_key.file_path}', "
            f"current='{current_branch_key.file_path}'. "
            f"File paths must match for a valid baseline comparison."
        )

    if baseline_key.commit_hash != current_branch_key.commit_hash:
        raise BaselineMismatchError(
            f"Baseline commit hash mismatch for '{baseline_key.file_path}': "
            f"stored='{baseline_key.commit_hash[:12]}...', "
            f"current='{current_branch_key.commit_hash[:12]}...'. "
            f"The target branch has advanced since this baseline was captured. "
            f"Re-capture the baseline by running the baseline generation script "
            f"against the current main branch before comparison."
        )


def compute_prompt_content_hash(
    agent_file_path: Path,
) -> str:
    """Compute a SHA-256 hash of the agent definition file content.

    Provides a content-based fingerprint for detecting file changes
    independent of git history. Used as a secondary integrity check:
    if the git commit hash matches but the content hash does not,
    the file may have been locally modified without committing.

    Args:
        agent_file_path: Absolute or repo-relative path to the agent definition file.

    Returns:
        First 16 characters of the SHA-256 hex digest of the file content.
        This is sufficient for collision resistance in this context.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        VersionKeyError: If the file path is not a valid agent definition path.

    Example:
        >>> content_hash = compute_prompt_content_hash(
        ...     Path("skills/problem-solving/agents/ps-researcher.md")
        ... )
        >>> len(content_hash)
        16
    """
    # Validate the relative portion of the path (strip absolute prefix if present)
    relative_path = str(agent_file_path)
    if agent_file_path.is_absolute():
        # For absolute paths, validate the terminal components only
        parts = agent_file_path.parts
        try:
            skills_idx = next(i for i, p in enumerate(parts) if p == "skills")
            relative_path = "/".join(parts[skills_idx:])
        except StopIteration as exc:
            raise VersionKeyError(
                f"Cannot determine relative path from '{agent_file_path}'. "
                f"Path must contain 'skills/' segment."
            ) from exc

    _validate_agent_file_path(relative_path)

    if not agent_file_path.exists():
        raise FileNotFoundError(
            f"Agent definition file not found: '{agent_file_path}'. "
            f"Ensure the file exists before computing its content hash."
        )

    content = agent_file_path.read_bytes()
    sha256 = hashlib.sha256(content)
    return sha256.hexdigest()[:16]


# ==============================================================================
# Version Key Registry
# ==============================================================================


class VersionKeyRegistry:
    """Registry mapping agent IDs to their current version keys.

    Provides a central lookup for version keys across all target agents.
    Used by the baseline store and evaluation pipeline to resolve agent IDs
    to their current VersionKey without making repeated git subprocess calls.

    Attributes:
        _registry: Internal dict mapping agent_id to VersionKey.
        _repo_root: Repository root path for git subprocess calls.
    """

    #: Agent IDs that are covered by the PROJ-036 regression harness.
    #: Extending this set requires adding test cases in tests/prompt-regression/test-cases/
    COVERED_AGENTS: frozenset[str] = frozenset(
        {
            "ps-researcher",
            "ps-analyst",
            "ps-architect",
            "ps-critic",
            "adv-scorer",
        }
    )

    #: Mapping from agent ID to agent definition file path
    AGENT_FILE_PATHS: dict[str, str] = {
        "ps-researcher": "skills/problem-solving/agents/ps-researcher.md",
        "ps-analyst": "skills/problem-solving/agents/ps-analyst.md",
        "ps-architect": "skills/problem-solving/agents/ps-architect.md",
        "ps-critic": "skills/problem-solving/agents/ps-critic.md",
        "adv-scorer": "skills/adversary/agents/adv-scorer.md",
    }

    def __init__(self, repo_root: Path | None = None) -> None:
        """Initialize the registry with an optional repository root path.

        Args:
            repo_root: Path to the repository root. Defaults to current directory.
                All git subprocess calls use this directory as cwd.
        """
        self._registry: dict[str, VersionKey] = {}
        self._repo_root = repo_root or Path.cwd()

    def get_version_key(self, agent_id: str) -> VersionKey:
        """Retrieve or build the current VersionKey for an agent.

        Caches the result after first lookup to avoid repeated git calls
        within a single evaluation run.

        Args:
            agent_id: Agent identifier (e.g., "ps-researcher").

        Returns:
            VersionKey for the agent's current definition file.

        Raises:
            VersionKeyError: If agent_id is not in COVERED_AGENTS or git call fails.

        Example:
            >>> registry = VersionKeyRegistry()
            >>> key = registry.get_version_key("ps-researcher")
        """
        if agent_id not in self.COVERED_AGENTS:
            raise VersionKeyError(
                f"Agent '{agent_id}' is not in the PROJ-036 regression harness coverage set. "
                f"Covered agents: {sorted(self.COVERED_AGENTS)}. "
                f"Add test cases to tests/prompt-regression/test-cases/{agent_id}.yaml "
                f"and register the agent in VersionKeyRegistry.COVERED_AGENTS to add coverage."
            )

        if agent_id not in self._registry:
            file_path = self.AGENT_FILE_PATHS[agent_id]
            self._registry[agent_id] = build_version_key(
                file_path=file_path,
                repo_root=self._repo_root,
            )

        return self._registry[agent_id]

    def get_all_version_keys(self) -> dict[str, VersionKey]:
        """Build and return version keys for all covered agents.

        Populates the cache for all agents in COVERED_AGENTS.

        Returns:
            Dict mapping agent_id to VersionKey for all covered agents.

        Raises:
            VersionKeyError: If any git call fails for any agent.
        """
        return {agent_id: self.get_version_key(agent_id) for agent_id in self.COVERED_AGENTS}

    def invalidate(self, agent_id: str | None = None) -> None:
        """Invalidate cached version key(s) to force re-resolution from git.

        Args:
            agent_id: If provided, invalidate only this agent's cached key.
                If None, invalidate all cached keys.
        """
        if agent_id is not None:
            self._registry.pop(agent_id, None)
        else:
            self._registry.clear()

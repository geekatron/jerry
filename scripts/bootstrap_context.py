"""Bootstrap Jerry's context distribution.

Cross-platform sync of .context/rules/ and .context/patterns/ to .claude/.
Uses symlinks on macOS/Linux, junction points on Windows (no admin required).

Usage:
    uv run python scripts/bootstrap_context.py [--check] [--force] [--quiet]
"""

from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Directories to sync from .context/ to .claude/
# NOTE: .context/guides/ is intentionally EXCLUDED from auto-loading.
# Guides are on-demand content (three-tier architecture: rules=auto-loaded,
# patterns=auto-loaded, guides=on-demand). DO NOT add "guides" to this list.
SYNC_DIRS = ["rules", "patterns"]


def detect_platform() -> str:
    """Detect the current platform.

    Returns:
        One of 'macos', 'linux', 'windows'.
    """
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    elif system == "Windows":
        return "windows"
    else:
        return system.lower()


def find_project_root() -> Path:
    """Find the Jerry project root by looking for CLAUDE.md."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "CLAUDE.md").exists() and (parent / ".context").exists():
            return parent
    raise FileNotFoundError(
        "Could not find Jerry project root. Run this script from within the Jerry repository."
    )


def is_symlink_or_junction(path: Path) -> bool:
    """Check if a path is a symlink or Windows junction point.

    Uses os.lstat with st_file_attributes on Windows to detect
    junction points (reparse points) without shelling out to cmd.

    Args:
        path: Filesystem path to check.

    Returns:
        True if the path is a symlink or Windows junction point.
    """
    if path.is_symlink():
        return True
    if detect_platform() == "windows":
        try:
            st = os.lstat(str(path))
            FILE_ATTRIBUTE_REPARSE_POINT = 0x400
            return bool(getattr(st, "st_file_attributes", 0) & FILE_ATTRIBUTE_REPARSE_POINT)
        except OSError:
            pass
    return False


def create_symlink(source: Path, target: Path, quiet: bool = False) -> bool:
    """Create a symlink from target -> source.

    On Windows without Developer Mode, falls back to junction points.

    Args:
        source: The canonical source directory (.context/X).
        target: The symlink location (.claude/X).
        quiet: Suppress output.

    Returns:
        True if successful.
    """
    plat = detect_platform()

    if plat == "windows":
        return _create_windows_link(source, target, quiet)
    else:
        return _create_unix_symlink(source, target, quiet)


def _create_unix_symlink(source: Path, target: Path, quiet: bool) -> bool:
    """Create a Unix symlink."""
    relative_source = os.path.relpath(source, target.parent)
    try:
        target.symlink_to(relative_source)
        if not quiet:
            print(f"  Symlink: {target} -> {relative_source}")
        return True
    except OSError as e:
        print(f"  Error creating symlink: {e}", file=sys.stderr)
        return False


def _create_windows_link(source: Path, target: Path, quiet: bool) -> bool:
    """Create a Windows link (try symlink first, fall back to junction)."""
    # Try symlink first (works with Developer Mode) using relative path
    rel_source = os.path.relpath(source, target.parent)
    try:
        target.symlink_to(rel_source)
        if not quiet:
            print(f"  Symlink: {target} -> {rel_source}")
        return True
    except OSError:
        pass

    # Fall back to junction point (no admin required for directories)
    # Junctions require absolute paths, so use the original source path
    try:
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(source)],
            check=True,
            capture_output=True,
            timeout=10,
        )
        if not quiet:
            print(f"  Junction: {target} -> {source}")
        return True
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ) as e:
        print(f"  Error creating junction: {e}", file=sys.stderr)
        return False


def _files_match(source: Path, target: Path) -> bool:
    """Compare files in source and target directories by name and content hash.

    Recursively walks both directories and compares relative paths
    and MD5 content hashes to detect content drift.

    Limitations:
        - Reads entire file contents into memory for hashing; not suitable
          for directories containing very large files.
        - Uses MD5 for fast comparison (not cryptographic security).
        - Does not compare file permissions, ownership, or timestamps.

    Args:
        source: Canonical source directory.
        target: Synced target directory.

    Returns:
        True if all files match by name and content.
    """
    source_files: dict[str, str] = {}
    for f in sorted(source.rglob("*")):
        if f.is_file():
            rel = f.relative_to(source)
            source_files[str(rel)] = hashlib.md5(f.read_bytes()).hexdigest()

    target_files: dict[str, str] = {}
    for f in sorted(target.rglob("*")):
        if f.is_file():
            rel = f.relative_to(target)
            target_files[str(rel)] = hashlib.md5(f.read_bytes()).hexdigest()

    return source_files == target_files


def check_sync(root: Path, quiet: bool = False) -> bool:
    """Check if .context/ and .claude/ are properly synced.

    Returns:
        True if all directories are properly linked.
    """
    context_dir = root / ".context"
    claude_dir = root / ".claude"
    all_ok = True

    for dirname in SYNC_DIRS:
        source = context_dir / dirname
        target = claude_dir / dirname

        if not source.exists():
            if not quiet:
                print(f"  {dirname}: source missing ({source})")
            all_ok = False
            continue

        if not target.exists():
            if not quiet:
                print(f"  {dirname}: not synced (missing {target})")
            all_ok = False
            continue

        if is_symlink_or_junction(target):
            if not quiet:
                resolved = target.resolve()
                print(f"  {dirname}: linked -> {resolved}")
        elif target.is_dir():
            # It's a regular directory (file copy scenario)
            # Compare both filenames and content hashes to detect drift
            if not _files_match(source, target):
                if not quiet:
                    print(f"  {dirname}: drift detected - content mismatch")
                all_ok = False
            else:
                target_file_count = sum(1 for f in target.rglob("*") if f.is_file())
                if not quiet:
                    print(f"  {dirname}: copied ({target_file_count} files)")
        else:
            if not quiet:
                print(f"  {dirname}: unexpected state")
            all_ok = False

    return all_ok


def _rmtree_with_retry(path: Path, max_retries: int = 3) -> None:
    """Remove directory tree with retry for Windows file locks.

    On Windows, antivirus scanners and indexers can briefly lock files,
    causing PermissionError during removal. This retries with backoff.

    Args:
        path: Directory to remove.
        max_retries: Maximum number of attempts before re-raising.

    Raises:
        PermissionError: If all retry attempts are exhausted.
    """
    for attempt in range(max_retries):
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.5 * (attempt + 1))


def bootstrap(root: Path, force: bool = False, quiet: bool = False) -> bool:
    """Run the full bootstrap process.

    Args:
        root: Jerry project root.
        force: Overwrite existing synced directories.
        quiet: Suppress output.

    Returns:
        True if bootstrap succeeded.
    """
    context_dir = root / ".context"
    claude_dir = root / ".claude"
    plat = detect_platform()
    success = True

    if not quiet:
        print(f"\nPlatform: {plat}")
        print(f"Source:   {context_dir}")
        print(f"Target:   {claude_dir}\n")

    # Ensure .claude/ exists
    claude_dir.mkdir(exist_ok=True)

    for dirname in SYNC_DIRS:
        source = context_dir / dirname
        target = claude_dir / dirname

        if not source.exists():
            if not quiet:
                print(f"  {dirname}: source not found at {source}, skipping")
            success = False
            continue

        # Handle existing target (including broken junctions that
        # return False for .exists() but are still present on disk)
        if target.exists() or target.is_symlink() or is_symlink_or_junction(target):
            if not force:
                if is_symlink_or_junction(target):
                    if not quiet:
                        print(f"  {dirname}: already linked")
                    continue
                else:
                    if not quiet:
                        print(f"  {dirname}: exists (use --force to overwrite)")
                    continue

            # Force: remove existing
            if target.is_symlink():
                target.unlink()
            elif is_symlink_or_junction(target):
                # Junctions are directory reparse points; remove with os.rmdir
                os.rmdir(str(target))
            elif target.is_dir():
                _rmtree_with_retry(target)

        # Create link
        if not create_symlink(source, target, quiet):
            # Final fallback: file copy
            # Partial-state is accepted here: if some dirs succeed and others fail,
            # the bootstrap is best-effort and reports overall success/failure.
            if not quiet:
                print(f"  {dirname}: falling back to file copy")
            try:
                shutil.copytree(source, target, symlinks=False)
                if not quiet:
                    file_count = len(list(target.rglob("*")))
                    print(f"  {dirname}: copied ({file_count} items)")
            except OSError as e:
                print(f"  {dirname}: copy failed: {e}", file=sys.stderr)
                success = False

    return success


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Bootstrap Jerry's context distribution",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check current sync status without making changes",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing synced directories",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Minimal output",
    )
    args = parser.parse_args()

    try:
        root = find_project_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.check:
        if not args.quiet:
            print("Checking Jerry context sync status...\n")
        ok = check_sync(root, args.quiet)
        if not args.quiet:
            print(f"\nStatus: {'OK' if ok else 'NEEDS SYNC'}")
        return 0 if ok else 1

    if not args.quiet:
        print("Bootstrapping Jerry context distribution...")

    ok = bootstrap(root, args.force, args.quiet)

    if not args.quiet:
        if ok:
            print("\nDone! Context distribution is set up.")
        else:
            print("\nBootstrap completed with warnings. Check output above.")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

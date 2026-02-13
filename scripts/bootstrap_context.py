"""Bootstrap Jerry's context distribution.

Cross-platform sync of .context/rules/ and .context/patterns/ to .claude/.
Uses symlinks on macOS/Linux, junction points on Windows (no admin required).

Usage:
    uv run python scripts/bootstrap_context.py [--check] [--force] [--quiet]
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Directories to sync from .context/ to .claude/
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
    """Check if a path is a symlink or Windows junction point."""
    if path.is_symlink():
        return True
    if platform.system() == "Windows" and path.exists():
        try:
            result = subprocess.run(
                ["cmd", "/c", "dir", str(path.parent), "/AL"],
                capture_output=True,
                text=True,
            )
            return str(path.name) in result.stdout
        except (subprocess.SubprocessError, FileNotFoundError):
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
    # Try symlink first (works with Developer Mode)
    try:
        target.symlink_to(source)
        if not quiet:
            print(f"  Symlink: {target} -> {source}")
        return True
    except OSError:
        pass

    # Fall back to junction point (no admin required for directories)
    try:
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(source)],
            check=True,
            capture_output=True,
        )
        if not quiet:
            print(f"  Junction: {target} -> {source}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  Error creating junction: {e}", file=sys.stderr)
        return False


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
            source_files = {f.name for f in source.iterdir() if f.is_file()}
            target_files = {f.name for f in target.iterdir() if f.is_file()}
            missing = source_files - target_files
            if missing:
                if not quiet:
                    print(f"  {dirname}: drift detected - missing: {missing}")
                all_ok = False
            else:
                if not quiet:
                    print(f"  {dirname}: copied ({len(target_files)} files)")
        else:
            if not quiet:
                print(f"  {dirname}: unexpected state")
            all_ok = False

    return all_ok


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

        # Handle existing target
        if target.exists() or target.is_symlink():
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
            elif target.is_dir():
                shutil.rmtree(target)

        # Create link
        if not create_symlink(source, target, quiet):
            # Final fallback: file copy
            if not quiet:
                print(f"  {dirname}: falling back to file copy")
            try:
                shutil.copytree(source, target)
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

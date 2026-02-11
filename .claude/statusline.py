#!/usr/bin/env python3
"""
ECW Status Line - Evolved Claude Workflow
Single-file, self-contained status line for Claude Code.

Version: 3.0.0
Python: 3.9+ (stdlib only, zero dependencies)
License: MIT

Features:
- 8 segments: Model, Context, Cost, Tokens, Session, Tools, Git, Directory
- Color-coded thresholds (green/yellow/red)
- Configurable currency symbol
- Token breakdown (fresh vs cached)
- Session duration with total tokens consumed
- Compaction detection with token delta
- Transcript JSONL parsing for per-tool token breakdown
- Compact mode for smaller terminals

Installation:
    1. Copy this file to ~/.claude/statusline.py
    2. chmod +x ~/.claude/statusline.py
    3. Add to ~/.claude/settings.json:
       {
         "statusLine": {
           "type": "command",
           "command": "python3 ~/.claude/statusline.py",
           "padding": 0
         }
       }

Configuration:
    Optional: Create ~/.claude/ecw-statusline-config.json to override defaults.
    See DEFAULT_CONFIG below for all available options.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

# =============================================================================
# VERSION
# =============================================================================

__version__ = "3.0.0"

# Pattern to strip ANSI escape codes from untrusted input (e.g., git branch names)
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")

# =============================================================================
# DEFAULT CONFIGURATION (embedded - no external file required)
# =============================================================================

DEFAULT_CONFIG: dict[str, Any] = {
    # Schema version for config/state compatibility checking
    "schema_version": "1",
    # Display settings
    "display": {
        "compact_mode": False,
        "auto_compact_width": 80,
        "separator": " | ",
        "use_emoji": True,
        "use_color": True,
        "progress_bar": {
            "width": 10,
            "filled_char": "▓",
            "empty_char": "░",
            "show_percentage": True,
        },
    },
    # Segment visibility
    "segments": {
        "model": True,
        "context": True,
        "cost": True,
        "tokens": True,  # Renamed from 'cache' - shows fresh/cached breakdown
        "session": True,  # Now shows duration + total tokens
        "compaction": True,  # NEW: Shows token delta after compaction
        "tools": True,
        "git": True,
        "directory": True,
    },
    # Context window thresholds
    "context": {
        "warning_threshold": 0.65,
        "critical_threshold": 0.85,
    },
    # Cost settings
    "cost": {
        "currency_symbol": "$",  # Configurable: "$", "CAD", "€", etc.
        "green_max": 1.00,
        "yellow_max": 5.00,
    },
    # Token breakdown settings (fresh vs cached)
    "tokens": {
        # Threshold for "high fresh tokens" warning (tokens per update)
        "fresh_warning": 5000,
        "fresh_critical": 20000,
    },
    # Session settings
    "session": {
        # No more block duration - just shows duration + total tokens
    },
    # Compaction detection
    "compaction": {
        # Minimum token drop to consider as compaction (vs normal variation)
        "detection_threshold": 10000,
        # State file for tracking previous token counts
        "state_file": "~/.claude/ecw-statusline-state.json",
    },
    # Tools segment settings
    "tools": {
        "enabled": False,  # Disabled by default (requires transcript parsing)
        "top_n": 3,
        "min_tokens": 100,
        "cache_ttl_seconds": 5,
    },
    # Git settings
    "git": {
        "show_branch": True,
        "show_status": True,
        "show_uncommitted_count": True,
        "max_branch_length": 20,
    },
    # Directory settings
    "directory": {
        "abbreviate_home": True,
        "max_length": 25,
        "basename_only": False,
    },
    # Colors (ANSI 256)
    "colors": {
        "green": 82,
        "yellow": 220,
        "red": 196,
        "cyan": 87,  # For informational displays
        "opus": 75,
        "sonnet": 141,
        "haiku": 84,
        "separator": 240,
        "directory": 250,
        "git_clean": 82,
        "git_dirty": 220,
        "tools": 147,
        "tokens_fresh": 214,  # Orange for fresh tokens
        "tokens_cached": 81,  # Cyan for cached tokens
        "compaction": 213,  # Pink for compaction indicator
    },
    # Jerry Framework integration (FEAT-002)
    "jerry": {
        "enabled": True,  # Try calling jerry context estimate for domain data
        "command": "",  # Override command; empty = auto-detect via CLAUDE_PLUGIN_ROOT
        "timeout": 3,  # Timeout in seconds for jerry subprocess
    },
    # Advanced settings
    "advanced": {
        "handle_cumulative_bug": True,
        "git_timeout": 2,
        "debug": False,
    },
}

# =============================================================================
# CONFIGURATION LOADING
# =============================================================================


def _get_config_paths() -> list[Path]:
    """Get config file search paths, handling missing HOME gracefully."""
    paths = [Path(__file__).parent / "ecw-statusline-config.json"]
    try:
        paths.append(Path.home() / ".claude" / "ecw-statusline-config.json")
    except (RuntimeError, KeyError, OSError):
        # HOME not set or not resolvable (e.g., minimal Docker container, Windows CI)
        pass
    return paths


CONFIG_PATHS = _get_config_paths()

_transcript_cache: dict[str, tuple[float, dict[str, int]]] = {}


def _schema_version_mismatch(found_version: Any) -> bool:
    """Check whether a found schema version differs from the expected version.

    Returns True if versions mismatch or the found version is unparseable.
    Returns False if they match (integer comparison).

    Non-string types (int, float, list, etc.) are treated as mismatches to
    enforce strict type discipline. Float values like 1.9 would be silently
    truncated by int(), so they are rejected explicitly.
    """
    expected = DEFAULT_CONFIG["schema_version"]
    # Reject non-string types (floats would silently truncate, e.g. int(1.9) = 1)
    if not isinstance(found_version, str):
        return True
    # Reject strings containing "." to prevent float-like version strings
    found_stripped = found_version.strip()
    if "." in found_stripped:
        return True
    try:
        return int(found_stripped) != int(expected)
    except (ValueError, TypeError):
        return True


def load_config() -> dict[str, Any]:
    """Load configuration from embedded defaults with optional file override."""
    config = deep_copy(DEFAULT_CONFIG)

    for config_path in CONFIG_PATHS:
        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    user_config = json.load(f)
                # Check for schema version mismatch before merging
                user_schema_version = user_config.get("schema_version")
                if user_schema_version is not None and _schema_version_mismatch(
                    user_schema_version
                ):
                    debug_log(
                        f"Config schema version mismatch: "
                        f"found {user_schema_version}, "
                        f"expected {DEFAULT_CONFIG['schema_version']}"
                    )
                config = deep_merge(config, user_config)
                # Restore schema_version from DEFAULT_CONFIG (not user-overridable)
                config["schema_version"] = DEFAULT_CONFIG["schema_version"]
                debug_log(f"Loaded config from {config_path}")
                break
            except (OSError, json.JSONDecodeError) as e:
                debug_log(f"Config load error from {config_path}: {e}")

    return config


def deep_copy(obj: Any) -> Any:
    """Deep copy a nested dict/list structure."""
    if isinstance(obj, dict):
        return {k: deep_copy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_copy(item) for item in obj]
    return obj


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base dict."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def debug_log(message: str) -> None:
    """Log debug message to file if debug mode enabled."""
    if os.environ.get("ECW_DEBUG") == "1":
        try:
            log_path = os.path.join(os.path.expanduser("~"), ".claude", "statusline-debug.log")
            with open(log_path, "a") as f:
                import datetime

                f.write(f"[{datetime.datetime.now().isoformat()}] {message}\n")
        except OSError:
            pass


def configure_windows_console() -> None:
    """Configure Windows console for UTF-8 output.

    On Windows, the default console encoding may not support ANSI escape
    sequences or Unicode characters. This function reconfigures stdout
    to use UTF-8 encoding with error replacement for unsupported characters.
    """
    if sys.platform == "win32":
        try:
            # Reconfigure stdout for UTF-8 with error handling
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            # Python < 3.7 or reconfigure not available
            pass


# =============================================================================
# STATE MANAGEMENT (for compaction detection)
# =============================================================================


def _resolve_state_path(config: dict) -> Path | None:
    """Resolve state file path, returning None if HOME is unavailable."""
    raw_path = config["compaction"]["state_file"]
    if not isinstance(raw_path, str):
        debug_log(f"Invalid state_file config type: {type(raw_path).__name__}")
        return None
    try:
        return Path(os.path.expanduser(raw_path))
    except (RuntimeError, KeyError, OSError, TypeError):
        debug_log("Cannot resolve state file path: HOME not set or invalid config")
        return None


def load_state(config: dict) -> dict[str, Any]:
    """Load previous state for compaction detection."""
    default = {
        "previous_context_tokens": 0,
        "last_compaction_from": 0,
        "last_compaction_to": 0,
    }
    state_file = _resolve_state_path(config)

    if state_file is None:
        return default

    try:
        if state_file.exists():
            with open(state_file, encoding="utf-8") as f:
                loaded = json.load(f)
            # Check schema version - fall back to defaults on mismatch
            loaded_version = loaded.get("schema_version")
            if loaded_version is not None and _schema_version_mismatch(loaded_version):
                debug_log(
                    f"State schema version mismatch: "
                    f"found {loaded_version}, "
                    f"expected {DEFAULT_CONFIG['schema_version']}. "
                    f"Discarding previous state data (compaction history "
                    f"will be reset) and falling back to defaults."
                )
                return default
            return loaded
    except (json.JSONDecodeError, OSError) as e:
        debug_log(f"State load error: {e}")

    return default


def save_state(config: dict, state: dict[str, Any]) -> None:
    """Save current state for next invocation.

    Uses atomic write pattern (write to temp file, then rename) to prevent
    corruption from partial writes. Handles read-only filesystems and missing
    HOME gracefully by logging a debug warning rather than crashing.
    """
    state_file = _resolve_state_path(config)

    if state_file is None:
        debug_log("Skipping state save: cannot resolve path (HOME not set)")
        return

    try:
        # Ensure schema_version is always written to state file
        state["schema_version"] = DEFAULT_CONFIG["schema_version"]
        state_file.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write: write to temp file in same directory, then rename
        fd = tempfile.NamedTemporaryFile(
            mode="w",
            dir=state_file.parent,
            suffix=".tmp",
            delete=False,
            encoding="utf-8",
        )
        try:
            json.dump(state, fd)
            fd.close()  # Must close before os.replace on Windows
            os.replace(fd.name, str(state_file))
        except OSError:
            fd.close()
            try:
                os.unlink(fd.name)
            except OSError:
                pass
            raise
    except OSError as e:
        debug_log(f"State save failed: {e}")


# =============================================================================
# JERRY FRAMEWORK INTEGRATION (FEAT-002)
# =============================================================================


def _get_claude_config_dir() -> Path | None:
    """Get the Claude Code configuration directory (cross-platform).

    Returns ~/.claude on macOS/Linux, %APPDATA%/claude on Windows.
    """
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "claude"
    try:
        return Path.home() / ".claude"
    except (RuntimeError, KeyError, OSError):
        return None


def _find_jerry_plugin_root() -> str | None:
    """Find Jerry's install path from Claude Code's installed plugins registry.

    Reads the installed_plugins.json to find the jerry plugin's installPath.
    Works for any user who has jerry installed as a Claude Code plugin.
    Cross-platform: handles ~/.claude (macOS/Linux) and %APPDATA%/claude (Windows).

    Returns the installPath string or None if not found.
    """
    config_dir = _get_claude_config_dir()
    if config_dir is None:
        return None
    registry = config_dir / "plugins" / "installed_plugins.json"
    if not registry.exists():
        return None
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
        entries = data.get("plugins", {}).get("jerry@jerry-framework", [])
        for entry in entries:
            install_path = entry.get("installPath", "")
            if install_path and os.path.isdir(install_path):
                return install_path
    except (json.JSONDecodeError, OSError, KeyError):
        pass
    return None


def _build_jerry_command(config: dict, data: dict) -> list[str] | None:
    """Build the jerry context estimate command.

    Resolution order:
    1. Explicit jerry.command in config file (user override)
    2. CLAUDE_PLUGIN_ROOT env var (set by Claude Code for hooks)
    3. Claude Code installed plugins registry (~/.claude/plugins/installed_plugins.json)
    4. Workspace project_dir fallback

    Returns None if Jerry is not available.
    """
    override = config.get("jerry", {}).get("command", "")
    if override:
        return override.split()

    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root and os.path.isdir(plugin_root):
        return [
            "uv",
            "run",
            "--directory",
            plugin_root,
            "jerry",
            "--json",
            "context",
            "estimate",
        ]

    # Auto-discover from Claude Code's plugin registry
    registry_root = _find_jerry_plugin_root()
    if registry_root:
        return [
            "uv",
            "run",
            "--directory",
            registry_root,
            "jerry",
            "--json",
            "context",
            "estimate",
        ]

    # Try workspace project_dir as fallback
    project_dir = safe_get(data, "workspace", "project_dir", default="")
    if project_dir and os.path.isfile(os.path.join(project_dir, "pyproject.toml")):
        return [
            "uv",
            "run",
            "--directory",
            project_dir,
            "jerry",
            "--json",
            "context",
            "estimate",
        ]

    return None


def try_jerry_estimate(input_json: str, config: dict, data: dict) -> dict[str, Any] | None:
    """Try calling jerry context estimate for enhanced domain computation.

    Returns Jerry's response dict or None if unavailable/failed.
    Falls back silently — the statusline continues with standalone computation.
    """
    jerry_config = config.get("jerry", {})
    if not jerry_config.get("enabled", True):
        return None

    cmd = _build_jerry_command(config, data)
    if cmd is None:
        debug_log("Jerry not available: no command found")
        return None

    timeout = jerry_config.get("timeout", 3)

    try:
        # Clear VIRTUAL_ENV to prevent uv venv mismatch when the statusline
        # runs inside a different project's activated virtualenv
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
        result = subprocess.run(
            cmd,
            input=input_json,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        if result.returncode == 0 and result.stdout.strip():
            jerry_data = json.loads(result.stdout.strip())
            debug_log(f"Jerry response received: tier={safe_get(jerry_data, 'context', 'tier')}")
            return jerry_data
        debug_log(f"Jerry failed: exit={result.returncode}, stderr={result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        debug_log(f"Jerry timed out after {timeout}s")
    except FileNotFoundError:
        debug_log("Jerry command not found")
    except (json.JSONDecodeError, OSError) as e:
        debug_log(f"Jerry error: {e}")

    return None


# =============================================================================
# ANSI COLOR UTILITIES
# =============================================================================


def _colors_enabled(config: dict | None) -> bool:
    """Check whether ANSI color output is enabled.

    Colors are disabled when:
    - NO_COLOR environment variable is set (takes precedence, per no-color.org)
    - display.use_color config is set to false
    """
    if os.environ.get("NO_COLOR") is not None:
        return False
    if config is not None and not safe_get(config, "display", "use_color", default=True):
        return False
    return True


def ansi_color(code: int, config: dict | None = None) -> str:
    """Generate ANSI 256-color escape sequence.

    Returns empty string when colors are disabled via NO_COLOR env var
    or display.use_color config.
    """
    if not _colors_enabled(config):
        return ""
    if code == 0:
        return "\033[0m"
    return f"\033[38;5;{code}m"


def ansi_reset(config: dict | None = None) -> str:
    """Generate ANSI reset escape sequence.

    Returns empty string when colors are disabled.
    """
    if not _colors_enabled(config):
        return ""
    return "\033[0m"


def get_terminal_width() -> int:
    """Get current terminal width.

    Returns 0 when running as a subprocess (no TTY) to prevent
    auto_compact_width from falsely triggering compact mode.
    Claude Code runs the statusline as a piped subprocess, so
    os.get_terminal_size() will always fail in that context.
    """
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 0


# =============================================================================
# DATA EXTRACTION UTILITIES
# =============================================================================


def safe_get(data: dict, *keys, default: Any = None) -> Any:
    """Safely navigate nested dict keys."""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current if current is not None else default


# =============================================================================
# TRANSCRIPT JSONL PARSING
# =============================================================================


def parse_transcript_for_tools(transcript_path: str, config: dict) -> dict[str, int]:
    """Parse transcript JSONL file to extract per-tool token usage."""
    tools_config = config["tools"]

    if not tools_config["enabled"]:
        return {}

    if not transcript_path or not Path(transcript_path).exists():
        debug_log(f"Transcript not found: {transcript_path}")
        return {}

    cache_key = transcript_path
    cache_ttl = tools_config["cache_ttl_seconds"]
    now = datetime.now().timestamp()

    if cache_key in _transcript_cache:
        cached_time, cached_data = _transcript_cache[cache_key]
        if now - cached_time < cache_ttl:
            debug_log("Using cached transcript data")
            return cached_data

    tool_tokens: dict[str, int] = {}

    try:
        with open(transcript_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    _extract_tool_usage(entry, tool_tokens)
                except json.JSONDecodeError:
                    continue

        _transcript_cache[cache_key] = (now, tool_tokens)
        debug_log(f"Parsed transcript: {tool_tokens}")

    except OSError as e:
        debug_log(f"Transcript read error: {e}")
        return {}

    return tool_tokens


def _extract_tool_usage(entry: dict, tool_tokens: dict[str, int]) -> None:
    """Extract tool usage from a transcript entry."""
    message = entry.get("message", {})
    content = message.get("content", [])

    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                block_type = block.get("type", "")
                if block_type == "tool_use":
                    tool_name = block.get("name", "unknown")
                    input_data = block.get("input", {})
                    token_estimate = _estimate_tokens(input_data)
                    tool_tokens[tool_name] = tool_tokens.get(tool_name, 0) + token_estimate
                elif block_type == "tool_result":
                    content_data = block.get("content", "")
                    token_estimate = _estimate_tokens(content_data)
                    tool_tokens["results"] = tool_tokens.get("results", 0) + token_estimate

    usage = entry.get("usage", {})
    if usage:
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        role = message.get("role", "unknown")
        if role == "assistant":
            tool_tokens["assistant"] = tool_tokens.get("assistant", 0) + output_tokens
        elif role == "user":
            tool_tokens["user"] = tool_tokens.get("user", 0) + input_tokens


def _estimate_tokens(data: Any) -> int:
    """Estimate token count from data (rough: ~4 chars per token)."""
    if isinstance(data, str):
        return len(data) // 4
    elif isinstance(data, dict | list):
        return len(json.dumps(data)) // 4
    return 0


# =============================================================================
# DATA EXTRACTION FUNCTIONS
# =============================================================================


def extract_model_info(data: dict) -> tuple[str, str]:
    """Extract model display name and tier."""
    display_name = safe_get(data, "model", "display_name", default="Unknown")
    model_id = safe_get(data, "model", "id", default="").lower()

    if "opus" in model_id:
        tier = "opus"
    elif "haiku" in model_id:
        tier = "haiku"
    else:
        tier = "sonnet"

    return display_name, tier


def extract_context_info(data: dict, config: dict) -> tuple[float, int, int, bool]:
    """Extract context window usage.

    Prefers Claude Code's pre-calculated used_percentage when available,
    as it accounts for output tokens (which become input on the next turn).
    Falls back to input-only token calculation when used_percentage is absent.
    """
    context_window_size = safe_get(data, "context_window", "context_window_size", default=200000)
    current_usage = safe_get(data, "context_window", "current_usage")

    # Prefer Claude Code's pre-calculated percentage (includes output tokens)
    used_pct = safe_get(data, "context_window", "used_percentage")

    if current_usage:
        input_tokens = safe_get(current_usage, "input_tokens", default=0)
        cache_creation = safe_get(current_usage, "cache_creation_input_tokens", default=0)
        cache_read = safe_get(current_usage, "cache_read_input_tokens", default=0)
        used_tokens = input_tokens + cache_creation + cache_read
        is_estimated = False
    else:
        used_tokens = safe_get(data, "context_window", "total_input_tokens", default=0)
        is_estimated = True

    if used_tokens > context_window_size and config["advanced"]["handle_cumulative_bug"]:
        is_estimated = True

    # Use Claude Code's percentage if available (accounts for output tokens);
    # fall back to input-only calculation otherwise
    if used_pct is not None and isinstance(used_pct, int | float) and used_pct > 0:
        percentage = used_pct / 100.0
    else:
        percentage = (used_tokens / context_window_size) if context_window_size > 0 else 0

    return percentage, used_tokens, context_window_size, is_estimated


def extract_cost_info(data: dict) -> tuple[float, int]:
    """Extract cost and duration info."""
    cost = safe_get(data, "cost", "total_cost_usd", default=0.0)
    duration_ms = safe_get(data, "cost", "total_duration_ms", default=0)
    return cost, duration_ms


def extract_token_breakdown(data: dict) -> tuple[int, int]:
    """
    Extract fresh vs cached token breakdown.
    Returns: (fresh_tokens, cached_tokens)
    """
    current_usage = safe_get(data, "context_window", "current_usage")

    if not current_usage:
        return 0, 0

    fresh_tokens = safe_get(current_usage, "input_tokens", default=0)
    cached_tokens = safe_get(current_usage, "cache_read_input_tokens", default=0)

    return fresh_tokens, cached_tokens


def extract_session_info(data: dict) -> tuple[int, int, int]:
    """
    Extract session duration and total tokens consumed.
    Returns: (elapsed_seconds, total_input_tokens, total_output_tokens)
    """
    duration_ms = safe_get(data, "cost", "total_duration_ms", default=0)
    elapsed_seconds = duration_ms // 1000

    total_input = safe_get(data, "context_window", "total_input_tokens", default=0)
    total_output = safe_get(data, "context_window", "total_output_tokens", default=0)

    return elapsed_seconds, total_input, total_output


def extract_compaction_info(data: dict, config: dict) -> tuple[bool, int, int]:
    """
    Detect compaction by comparing current context to previous.
    Returns: (compaction_detected, from_tokens, to_tokens)
    """
    current_usage = safe_get(data, "context_window", "current_usage")

    if not current_usage:
        return False, 0, 0

    # Calculate current context size
    input_tokens = safe_get(current_usage, "input_tokens", default=0)
    cache_creation = safe_get(current_usage, "cache_creation_input_tokens", default=0)
    cache_read = safe_get(current_usage, "cache_read_input_tokens", default=0)
    current_context = input_tokens + cache_creation + cache_read

    # Load previous state
    state = load_state(config)
    previous_context = state.get("previous_context_tokens", 0)
    threshold = config["compaction"]["detection_threshold"]

    # Detect significant drop (compaction)
    compaction_detected = False
    from_tokens = state.get("last_compaction_from", 0)
    to_tokens = state.get("last_compaction_to", 0)

    if previous_context > 0 and (previous_context - current_context) > threshold:
        # Compaction detected!
        compaction_detected = True
        from_tokens = previous_context
        to_tokens = current_context
        state["last_compaction_from"] = from_tokens
        state["last_compaction_to"] = to_tokens
        debug_log(f"Compaction detected: {from_tokens} -> {to_tokens}")

    # Update state with current context
    state["previous_context_tokens"] = current_context
    save_state(config, state)

    # If we detected compaction this round OR we have recent compaction data
    if compaction_detected or (from_tokens > 0 and to_tokens > 0):
        return True, from_tokens, to_tokens

    return False, 0, 0


def extract_workspace_info(data: dict, config: dict) -> str:
    """Extract and format workspace directory."""
    current_dir = safe_get(data, "workspace", "current_dir", default="")

    if not current_dir:
        current_dir = safe_get(data, "cwd", default="~")

    dir_config = config["directory"]

    if dir_config["abbreviate_home"]:
        try:
            home = str(Path.home())
        except (RuntimeError, KeyError, OSError):
            home = ""
        if home and current_dir.startswith(home):
            current_dir = "~" + current_dir[len(home) :]

    if dir_config["basename_only"]:
        current_dir = os.path.basename(current_dir) or current_dir

    max_len = dir_config["max_length"]
    if len(current_dir) > max_len:
        current_dir = "..." + current_dir[-(max_len - 3) :]

    return current_dir


def extract_tools_info(data: dict, config: dict) -> list[tuple[str, int]]:
    """Extract top tools by token usage from transcript."""
    transcript_path = safe_get(data, "transcript_path", default="")
    tool_tokens = parse_transcript_for_tools(transcript_path, config)

    tools_config = config["tools"]
    min_tokens = tools_config["min_tokens"]
    top_n = tools_config["top_n"]

    filtered = [(name, tokens) for name, tokens in tool_tokens.items() if tokens >= min_tokens]
    sorted_tools = sorted(filtered, key=lambda x: x[1], reverse=True)

    return sorted_tools[:top_n]


# =============================================================================
# GIT INTEGRATION
# =============================================================================


def get_git_info(data: dict, config: dict) -> tuple[str, bool, int] | None:
    """Get git branch, status, and uncommitted file count."""
    git_config = config["git"]
    timeout = config["advanced"]["git_timeout"]

    cwd = safe_get(data, "workspace", "current_dir") or safe_get(data, "cwd")
    if not cwd:
        return None

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )

        if result.returncode != 0:
            return None

        # Sanitize ANSI escape codes from git output to prevent terminal injection
        branch = _ANSI_ESCAPE_RE.sub("", result.stdout.strip())

        max_len = git_config["max_branch_length"]
        if len(branch) > max_len:
            branch = branch[: max_len - 3] + "..."

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )

        uncommitted_lines = [line for line in result.stdout.strip().splitlines() if line]
        uncommitted_count = len(uncommitted_lines)
        is_clean = uncommitted_count == 0

        return branch, is_clean, uncommitted_count

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        debug_log(f"Git error: {e}")
        return None


# =============================================================================
# FORMATTING FUNCTIONS
# =============================================================================


def format_progress_bar(percentage: float, config: dict, color_code: int) -> str:
    """Format a progress bar with color."""
    bar_config = config["display"]["progress_bar"]
    width = bar_config["width"]
    use_emoji = config["display"]["use_emoji"]
    filled_char = bar_config["filled_char"] if use_emoji else "#"
    empty_char = bar_config["empty_char"] if use_emoji else "-"
    show_pct = bar_config["show_percentage"]

    display_pct = min(max(percentage, 0), 1.0)
    filled_count = int(display_pct * width)
    empty_count = width - filled_count

    bar = filled_char * filled_count + empty_char * empty_count
    color = ansi_color(color_code, config)
    reset = ansi_reset(config)

    if show_pct:
        pct_str = f"{int(percentage * 100)}%"
        return f"{color}[{bar}] {pct_str}{reset}"
    else:
        return f"{color}[{bar}]{reset}"


def format_duration(seconds: int) -> str:
    """Format duration as HhMm or Mm."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h{minutes:02d}m"
    else:
        return f"{minutes}m"


def format_tokens_short(tokens: int) -> str:
    """Format token count in short form (e.g., 1.2k, 15k, 1.5M)."""
    if tokens >= 1000000:
        return f"{tokens / 1000000:.1f}M"
    elif tokens >= 1000:
        return f"{tokens / 1000:.1f}k"
    return str(tokens)


def get_threshold_color(
    value: float,
    green_max: float,
    yellow_max: float,
    colors: dict,
    invert: bool = False,
) -> int:
    """Get color code based on threshold."""
    if invert:
        if value >= green_max:
            return colors["green"]
        elif value >= yellow_max:
            return colors["yellow"]
        else:
            return colors["red"]
    else:
        if value <= green_max:
            return colors["green"]
        elif value <= yellow_max:
            return colors["yellow"]
        else:
            return colors["red"]


# =============================================================================
# SEGMENT BUILDERS
# =============================================================================


def build_model_segment(data: dict, config: dict) -> str:
    """Build the model display segment."""
    display_name, tier = extract_model_info(data)
    colors = config["colors"]

    icons = {"opus": "🔵", "sonnet": "🟣", "haiku": "🟢"}
    icon = icons.get(tier, "⚪") if config["display"]["use_emoji"] else ""

    color = ansi_color(colors.get(tier, colors["sonnet"]), config)
    reset = ansi_reset(config)

    if icon:
        return f"{color}{icon} {display_name}{reset}"
    else:
        return f"{color}{display_name}{reset}"


def _jerry_tier_to_color(tier: str, colors: dict) -> int:
    """Map Jerry's ThresholdTier to ANSI color code.

    Mapping: NOMINAL/LOW → green, WARNING → yellow, CRITICAL/EMERGENCY → red.
    """
    tier_upper = tier.upper() if tier else ""
    if tier_upper in ("NOMINAL", "LOW"):
        return colors["green"]
    elif tier_upper == "WARNING":
        return colors["yellow"]
    elif tier_upper in ("CRITICAL", "EMERGENCY"):
        return colors["red"]
    return colors["green"]


def build_context_segment(data: dict, config: dict, jerry_data: dict | None = None) -> str:
    """Build the context window usage segment.

    Uses Jerry's domain data (tier, fill_percentage) when available,
    falling back to standalone computation.
    """
    colors = config["colors"]
    icon = "📊 " if config["display"]["use_emoji"] else ""

    # Use Jerry data if available (ST-004/ST-005)
    jerry_context = safe_get(jerry_data, "context") if jerry_data else None
    if jerry_context and isinstance(jerry_context, dict):
        percentage = jerry_context.get("fill_percentage", 0)
        is_estimated = jerry_context.get("is_estimated", False)
        tier = jerry_context.get("tier", "NOMINAL")
        color_code = _jerry_tier_to_color(tier, colors)
    else:
        # Fallback: standalone computation with hardcoded thresholds
        percentage, _used, _total, is_estimated = extract_context_info(data, config)
        thresholds = config["context"]
        color_code = get_threshold_color(
            percentage,
            thresholds["warning_threshold"],
            thresholds["critical_threshold"],
            colors,
        )

    estimate_marker = "~" if is_estimated else ""
    bar = format_progress_bar(percentage, config, color_code)

    return f"{icon}{estimate_marker}{bar}"


def build_cost_segment(data: dict, config: dict) -> str:
    """Build the cost display segment with configurable currency."""
    cost, _ = extract_cost_info(data)
    colors = config["colors"]
    cost_config = config["cost"]

    color_code = get_threshold_color(
        cost, cost_config["green_max"], cost_config["yellow_max"], colors
    )

    currency = cost_config["currency_symbol"]
    icon = "💰 " if config["display"]["use_emoji"] else ""
    color = ansi_color(color_code, config)
    reset = ansi_reset(config)

    return f"{icon}{color}{currency}{cost:.2f}{reset}"


def build_tokens_segment(data: dict, config: dict) -> str:
    """
    Build the token breakdown segment.
    Format: ⚡ 500→ 45.2k↺
    Where → = fresh tokens, ↺ = cached tokens
    """
    fresh, cached = extract_token_breakdown(data)
    colors = config["colors"]

    use_emoji = config["display"]["use_emoji"]
    icon = "⚡ " if use_emoji else ""
    fresh_indicator = "→" if use_emoji else ">"
    cached_indicator = "↺" if use_emoji else "<"
    fresh_color = ansi_color(colors["tokens_fresh"], config)
    cached_color = ansi_color(colors["tokens_cached"], config)
    reset = ansi_reset(config)

    fresh_str = format_tokens_short(fresh)
    cached_str = format_tokens_short(cached)

    return f"{icon}{fresh_color}{fresh_str}{fresh_indicator}{reset} {cached_color}{cached_str}{cached_indicator}{reset}"


def build_session_segment(data: dict, config: dict) -> str:
    """
    Build the session segment showing duration + total tokens consumed.
    Format: ⏱️ 44h05m 1.2M tokens
    """
    elapsed_seconds, total_input, total_output = extract_session_info(data)
    colors = config["colors"]

    icon = "⏱️ " if config["display"]["use_emoji"] else ""
    duration_str = format_duration(elapsed_seconds)

    total_tokens = total_input + total_output
    tokens_str = format_tokens_short(total_tokens)

    color = ansi_color(colors["cyan"], config)
    reset = ansi_reset(config)

    return f"{icon}{color}{duration_str} {tokens_str}tok{reset}"


def build_compaction_segment(data: dict, config: dict, jerry_data: dict | None = None) -> str:
    """Build the compaction indicator segment.

    Uses Jerry's compaction detection when available, falling back
    to standalone state-file-based detection.
    Format: 📉 150k→46k
    """
    # Use Jerry data if available (ST-005)
    jerry_compaction = safe_get(jerry_data, "compaction") if jerry_data else None
    if jerry_compaction and isinstance(jerry_compaction, dict):
        compacted = jerry_compaction.get("detected", False)
        from_tokens = jerry_compaction.get("from_tokens", 0)
        to_tokens = jerry_compaction.get("to_tokens", 0)
    else:
        # Fallback: standalone compaction detection
        compacted, from_tokens, to_tokens = extract_compaction_info(data, config)

    if not compacted:
        return ""

    colors = config["colors"]
    use_emoji = config["display"]["use_emoji"]
    icon = "📉 " if use_emoji else "v "
    arrow = "→" if use_emoji else ">"
    color = ansi_color(colors["compaction"], config)
    reset = ansi_reset(config)

    from_str = format_tokens_short(from_tokens)
    to_str = format_tokens_short(to_tokens)

    return f"{icon}{color}{from_str}{arrow}{to_str}{reset}"


def build_sub_agents_segment(jerry_data: dict | None, config: dict) -> str:
    """Build the sub-agents summary segment from Jerry data.

    Shows active/completed agent counts and total context usage.
    Only displayed when Jerry data is available and agents exist.
    Format: 🤖 2↑14↓ 892k ctx
    """
    if jerry_data is None:
        return ""

    sub_agents = safe_get(jerry_data, "sub_agents")
    if not sub_agents or not isinstance(sub_agents, dict):
        return ""

    total = sub_agents.get("total_count", 0)
    if total == 0:
        return ""

    active = sub_agents.get("active_count", 0)
    completed = sub_agents.get("completed_count", 0)
    total_ctx = safe_get(sub_agents, "aggregate", "total_context_tokens", default=0)

    colors = config["colors"]
    use_emoji = config["display"]["use_emoji"]
    icon = "🤖 " if use_emoji else ""
    color = ansi_color(colors["cyan"], config)
    reset = ansi_reset(config)

    ctx_str = format_tokens_short(total_ctx) if total_ctx > 0 else ""
    ctx_part = f" {ctx_str}ctx" if ctx_str else ""

    if active > 0:
        return f"{icon}{color}{active}↑{completed}↓{ctx_part}{reset}"
    return f"{icon}{color}{completed}↓{ctx_part}{reset}"


def build_tools_segment(data: dict, config: dict) -> str:
    """Build the dominant tools segment."""
    if not config["tools"]["enabled"]:
        return ""

    tools = extract_tools_info(data, config)

    if not tools:
        return ""

    colors = config["colors"]
    icon = "🔧 " if config["display"]["use_emoji"] else ""
    color = ansi_color(colors["tools"], config)
    reset = ansi_reset(config)

    tool_strs = [f"{name}:{format_tokens_short(tokens)}" for name, tokens in tools]
    tools_display = " ".join(tool_strs)

    return f"{icon}{color}{tools_display}{reset}"


def build_git_segment(data: dict, config: dict) -> str:
    """Build the git status segment."""
    git_info = get_git_info(data, config)

    if git_info is None:
        return ""

    branch, is_clean, uncommitted_count = git_info
    colors = config["colors"]
    git_config = config["git"]

    use_emoji = config["display"]["use_emoji"]
    icon = "🌿 " if use_emoji else ""

    if is_clean:
        status_icon = ("✓" if use_emoji else "+") if git_config["show_status"] else ""
        color = ansi_color(colors["git_clean"], config)
    else:
        dirty_marker = "●" if use_emoji else "*"
        if git_config["show_uncommitted_count"]:
            status_icon = f"{dirty_marker}{uncommitted_count}"
        elif git_config["show_status"]:
            status_icon = dirty_marker
        else:
            status_icon = ""
        color = ansi_color(colors["git_dirty"], config)

    reset = ansi_reset(config)

    return f"{icon}{color}{branch} {status_icon}{reset}".strip()


def build_directory_segment(data: dict, config: dict) -> str:
    """Build the directory display segment."""
    directory = extract_workspace_info(data, config)
    colors = config["colors"]

    icon = "📂 " if config["display"]["use_emoji"] else ""
    color = ansi_color(colors["directory"], config)
    reset = ansi_reset(config)

    return f"{icon}{color}{directory}{reset}"


# =============================================================================
# MAIN BUILDER
# =============================================================================


def build_status_line(data: dict, config: dict, jerry_data: dict | None = None) -> str:
    """Build the complete status line from all segments.

    When jerry_data is available (FEAT-002), uses Jerry's domain
    computation for context/compaction/sub-agent segments. All other
    segments use the raw Claude Code data.
    """
    segments_config = config["segments"]
    display_config = config["display"]
    separator = display_config["separator"]
    colors = config["colors"]

    compact = display_config["compact_mode"]
    if not compact and display_config["auto_compact_width"] > 0:
        term_width = get_terminal_width()
        # Only auto-compact when we have a real terminal width.
        # When running as a subprocess (no TTY), term_width is 0 —
        # don't compact, let Claude Code handle display truncation.
        if term_width > 0 and term_width < display_config["auto_compact_width"]:
            compact = True

    segments = []

    if segments_config["model"]:
        segments.append(build_model_segment(data, config))

    if segments_config["context"]:
        segments.append(build_context_segment(data, config, jerry_data=jerry_data))

    if segments_config["cost"]:
        segments.append(build_cost_segment(data, config))

    if not compact:
        if segments_config.get("tokens", True):
            segments.append(build_tokens_segment(data, config))

        if segments_config["session"]:
            segments.append(build_session_segment(data, config))

        # Sub-agents segment (Jerry-only, FEAT-002) — before compaction/tools
        # so it isn't pushed off-screen by long tool breakdowns
        if jerry_data:
            sub_agents_segment = build_sub_agents_segment(jerry_data, config)
            if sub_agents_segment:
                segments.append(sub_agents_segment)

        if segments_config.get("compaction", True):
            compaction_segment = build_compaction_segment(data, config, jerry_data=jerry_data)
            if compaction_segment:
                segments.append(compaction_segment)

        if segments_config["tools"]:
            tools_segment = build_tools_segment(data, config)
            if tools_segment:
                segments.append(tools_segment)

    if segments_config["git"]:
        git_segment = build_git_segment(data, config)
        if git_segment:
            segments.append(git_segment)

    if segments_config["directory"] and not compact:
        segments.append(build_directory_segment(data, config))

    sep_color = ansi_color(colors["separator"], config)
    reset = ansi_reset(config)
    colored_sep = f"{sep_color}{separator}{reset}"

    return colored_sep.join(segments)


# =============================================================================
# ENTRY POINT
# =============================================================================


def main() -> None:
    """Main entry point."""
    configure_windows_console()
    try:
        config = load_config()

        if config["advanced"]["debug"]:
            os.environ["ECW_DEBUG"] = "1"

        input_data = sys.stdin.read().strip()

        if not input_data:
            debug_log("No input received")
            print("ECW: No data")
            return

        try:
            data = json.loads(input_data)
        except json.JSONDecodeError as e:
            debug_log(f"JSON parse error: {e}")
            print("ECW: Parse error")
            return

        # FEAT-002: Try Jerry for enhanced domain computation
        jerry_data = try_jerry_estimate(input_data, config, data)

        status_line = build_status_line(data, config, jerry_data=jerry_data)
        print(status_line)

    except Exception as e:
        debug_log(f"Unexpected error: {e}")
        print(f"ECW: Error - {type(e).__name__}")


if __name__ == "__main__":
    main()

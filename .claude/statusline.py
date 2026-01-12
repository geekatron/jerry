#!/usr/bin/env python3
"""
ECW Status Line - Evolved Claude Workflow
Single-file, self-contained status line for Claude Code.

Version: 2.1.0
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
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# =============================================================================
# VERSION
# =============================================================================

__version__ = "2.1.0"

# =============================================================================
# DEFAULT CONFIGURATION (embedded - no external file required)
# =============================================================================

DEFAULT_CONFIG: Dict[str, Any] = {
    # Display settings
    "display": {
        "compact_mode": False,
        "auto_compact_width": 80,
        "separator": " | ",
        "use_emoji": True,
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
        "tokens": True,      # Renamed from 'cache' - shows fresh/cached breakdown
        "session": True,     # Now shows duration + total tokens
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
        "cyan": 87,      # For informational displays
        "opus": 75,
        "sonnet": 141,
        "haiku": 84,
        "separator": 240,
        "directory": 250,
        "git_clean": 82,
        "git_dirty": 220,
        "tools": 147,
        "tokens_fresh": 214,   # Orange for fresh tokens
        "tokens_cached": 81,   # Cyan for cached tokens
        "compaction": 213,     # Pink for compaction indicator
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

CONFIG_PATHS = [
    Path(__file__).parent / "ecw-statusline-config.json",
    Path.home() / ".claude" / "ecw-statusline-config.json",
]

_transcript_cache: Dict[str, Tuple[float, Dict[str, int]]] = {}


def load_config() -> Dict[str, Any]:
    """Load configuration from embedded defaults with optional file override."""
    config = deep_copy(DEFAULT_CONFIG)

    for config_path in CONFIG_PATHS:
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                config = deep_merge(config, user_config)
                debug_log(f"Loaded config from {config_path}")
                break
            except (json.JSONDecodeError, IOError) as e:
                debug_log(f"Config load error from {config_path}: {e}")

    return config


def deep_copy(obj: Any) -> Any:
    """Deep copy a nested dict/list structure."""
    if isinstance(obj, dict):
        return {k: deep_copy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_copy(item) for item in obj]
    return obj


def deep_merge(base: Dict, override: Dict) -> Dict:
    """Recursively merge override into base dict."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def debug_log(message: str) -> None:
    """Log debug message to stderr if debug mode enabled."""
    if os.environ.get("ECW_DEBUG") == "1":
        print(f"[ECW-DEBUG] {message}", file=sys.stderr)


# =============================================================================
# STATE MANAGEMENT (for compaction detection)
# =============================================================================


def load_state(config: Dict) -> Dict[str, Any]:
    """Load previous state for compaction detection."""
    state_file = Path(os.path.expanduser(config["compaction"]["state_file"]))

    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            debug_log(f"State load error: {e}")

    return {"previous_context_tokens": 0, "last_compaction_from": 0, "last_compaction_to": 0}


def save_state(config: Dict, state: Dict[str, Any]) -> None:
    """Save current state for next invocation."""
    state_file = Path(os.path.expanduser(config["compaction"]["state_file"]))

    try:
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except IOError as e:
        debug_log(f"State save error: {e}")


# =============================================================================
# ANSI COLOR UTILITIES
# =============================================================================


def ansi_color(code: int) -> str:
    """Generate ANSI 256-color escape sequence."""
    if code == 0:
        return "\033[0m"
    return f"\033[38;5;{code}m"


def ansi_reset() -> str:
    """Generate ANSI reset escape sequence."""
    return "\033[0m"


def get_terminal_width() -> int:
    """Get current terminal width."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 120


# =============================================================================
# DATA EXTRACTION UTILITIES
# =============================================================================


def safe_get(data: Dict, *keys, default: Any = None) -> Any:
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


def parse_transcript_for_tools(transcript_path: str, config: Dict) -> Dict[str, int]:
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

    tool_tokens: Dict[str, int] = {}

    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
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

    except IOError as e:
        debug_log(f"Transcript read error: {e}")
        return {}

    return tool_tokens


def _extract_tool_usage(entry: Dict, tool_tokens: Dict[str, int]) -> None:
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
    elif isinstance(data, (dict, list)):
        return len(json.dumps(data)) // 4
    return 0


# =============================================================================
# DATA EXTRACTION FUNCTIONS
# =============================================================================


def extract_model_info(data: Dict) -> Tuple[str, str]:
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


def extract_context_info(data: Dict, config: Dict) -> Tuple[float, int, int, bool]:
    """Extract context window usage."""
    context_window_size = safe_get(data, "context_window", "context_window_size", default=200000)
    current_usage = safe_get(data, "context_window", "current_usage")

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

    percentage = (used_tokens / context_window_size) if context_window_size > 0 else 0

    return percentage, used_tokens, context_window_size, is_estimated


def extract_cost_info(data: Dict) -> Tuple[float, int]:
    """Extract cost and duration info."""
    cost = safe_get(data, "cost", "total_cost_usd", default=0.0)
    duration_ms = safe_get(data, "cost", "total_duration_ms", default=0)
    return cost, duration_ms


def extract_token_breakdown(data: Dict) -> Tuple[int, int]:
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


def extract_session_info(data: Dict) -> Tuple[int, int, int]:
    """
    Extract session duration and total tokens consumed.
    Returns: (elapsed_seconds, total_input_tokens, total_output_tokens)
    """
    duration_ms = safe_get(data, "cost", "total_duration_ms", default=0)
    elapsed_seconds = duration_ms // 1000

    total_input = safe_get(data, "context_window", "total_input_tokens", default=0)
    total_output = safe_get(data, "context_window", "total_output_tokens", default=0)

    return elapsed_seconds, total_input, total_output


def extract_compaction_info(data: Dict, config: Dict) -> Tuple[bool, int, int]:
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


def extract_workspace_info(data: Dict, config: Dict) -> str:
    """Extract and format workspace directory."""
    current_dir = safe_get(data, "workspace", "current_dir", default="")

    if not current_dir:
        current_dir = safe_get(data, "cwd", default="~")

    dir_config = config["directory"]

    if dir_config["abbreviate_home"]:
        home = os.path.expanduser("~")
        if current_dir.startswith(home):
            current_dir = "~" + current_dir[len(home):]

    if dir_config["basename_only"]:
        current_dir = os.path.basename(current_dir) or current_dir

    max_len = dir_config["max_length"]
    if len(current_dir) > max_len:
        current_dir = "..." + current_dir[-(max_len - 3):]

    return current_dir


def extract_tools_info(data: Dict, config: Dict) -> List[Tuple[str, int]]:
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


def get_git_info(data: Dict, config: Dict) -> Optional[Tuple[str, bool, int]]:
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
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            return None

        branch = result.stdout.strip()

        max_len = git_config["max_branch_length"]
        if len(branch) > max_len:
            branch = branch[: max_len - 3] + "..."

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        uncommitted_lines = [line for line in result.stdout.strip().split("\n") if line]
        uncommitted_count = len(uncommitted_lines)
        is_clean = uncommitted_count == 0

        return branch, is_clean, uncommitted_count

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        debug_log(f"Git error: {e}")
        return None


# =============================================================================
# FORMATTING FUNCTIONS
# =============================================================================


def format_progress_bar(percentage: float, config: Dict, color_code: int) -> str:
    """Format a progress bar with color."""
    bar_config = config["display"]["progress_bar"]
    width = bar_config["width"]
    filled_char = bar_config["filled_char"]
    empty_char = bar_config["empty_char"]
    show_pct = bar_config["show_percentage"]

    display_pct = min(max(percentage, 0), 1.0)
    filled_count = int(display_pct * width)
    empty_count = width - filled_count

    bar = filled_char * filled_count + empty_char * empty_count
    color = ansi_color(color_code)
    reset = ansi_reset()

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
    colors: Dict,
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


def build_model_segment(data: Dict, config: Dict) -> str:
    """Build the model display segment."""
    display_name, tier = extract_model_info(data)
    colors = config["colors"]

    icons = {"opus": "🔵", "sonnet": "🟣", "haiku": "🟢"}
    icon = icons.get(tier, "⚪") if config["display"]["use_emoji"] else ""

    color = ansi_color(colors.get(tier, colors["sonnet"]))
    reset = ansi_reset()

    if icon:
        return f"{color}{icon} {display_name}{reset}"
    else:
        return f"{color}{display_name}{reset}"


def build_context_segment(data: Dict, config: Dict) -> str:
    """Build the context window usage segment."""
    percentage, used, total, is_estimated = extract_context_info(data, config)
    colors = config["colors"]
    thresholds = config["context"]

    color_code = get_threshold_color(
        percentage,
        thresholds["warning_threshold"],
        thresholds["critical_threshold"],
        colors,
    )

    icon = "📊 " if config["display"]["use_emoji"] else ""
    estimate_marker = "~" if is_estimated else ""

    bar = format_progress_bar(percentage, config, color_code)

    return f"{icon}{estimate_marker}{bar}"


def build_cost_segment(data: Dict, config: Dict) -> str:
    """Build the cost display segment with configurable currency."""
    cost, _ = extract_cost_info(data)
    colors = config["colors"]
    cost_config = config["cost"]

    color_code = get_threshold_color(
        cost, cost_config["green_max"], cost_config["yellow_max"], colors
    )

    currency = cost_config["currency_symbol"]
    icon = "💰 " if config["display"]["use_emoji"] else ""
    color = ansi_color(color_code)
    reset = ansi_reset()

    return f"{icon}{color}{currency}{cost:.2f}{reset}"


def build_tokens_segment(data: Dict, config: Dict) -> str:
    """
    Build the token breakdown segment.
    Format: ⚡ 500→ 45.2k↺
    Where → = fresh tokens, ↺ = cached tokens
    """
    fresh, cached = extract_token_breakdown(data)
    colors = config["colors"]

    icon = "⚡ " if config["display"]["use_emoji"] else ""
    fresh_color = ansi_color(colors["tokens_fresh"])
    cached_color = ansi_color(colors["tokens_cached"])
    reset = ansi_reset()

    fresh_str = format_tokens_short(fresh)
    cached_str = format_tokens_short(cached)

    return f"{icon}{fresh_color}{fresh_str}→{reset} {cached_color}{cached_str}↺{reset}"


def build_session_segment(data: Dict, config: Dict) -> str:
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

    color = ansi_color(colors["cyan"])
    reset = ansi_reset()

    return f"{icon}{color}{duration_str} {tokens_str}tok{reset}"


def build_compaction_segment(data: Dict, config: Dict) -> str:
    """
    Build the compaction indicator segment.
    Shows token delta when compaction is detected.
    Format: 📉 150k→46k
    """
    compacted, from_tokens, to_tokens = extract_compaction_info(data, config)

    if not compacted:
        return ""

    colors = config["colors"]
    icon = "📉 " if config["display"]["use_emoji"] else "↓"
    color = ansi_color(colors["compaction"])
    reset = ansi_reset()

    from_str = format_tokens_short(from_tokens)
    to_str = format_tokens_short(to_tokens)

    return f"{icon}{color}{from_str}→{to_str}{reset}"


def build_tools_segment(data: Dict, config: Dict) -> str:
    """Build the dominant tools segment."""
    if not config["tools"]["enabled"]:
        return ""

    tools = extract_tools_info(data, config)

    if not tools:
        return ""

    colors = config["colors"]
    icon = "🔧 " if config["display"]["use_emoji"] else ""
    color = ansi_color(colors["tools"])
    reset = ansi_reset()

    tool_strs = [f"{name}:{format_tokens_short(tokens)}" for name, tokens in tools]
    tools_display = " ".join(tool_strs)

    return f"{icon}{color}{tools_display}{reset}"


def build_git_segment(data: Dict, config: Dict) -> str:
    """Build the git status segment."""
    git_info = get_git_info(data, config)

    if git_info is None:
        return ""

    branch, is_clean, uncommitted_count = git_info
    colors = config["colors"]
    git_config = config["git"]

    icon = "🌿 " if config["display"]["use_emoji"] else ""

    if is_clean:
        status_icon = "✓" if git_config["show_status"] else ""
        color = ansi_color(colors["git_clean"])
    else:
        if git_config["show_uncommitted_count"]:
            status_icon = f"●{uncommitted_count}"
        elif git_config["show_status"]:
            status_icon = "●"
        else:
            status_icon = ""
        color = ansi_color(colors["git_dirty"])

    reset = ansi_reset()

    return f"{icon}{color}{branch} {status_icon}{reset}".strip()


def build_directory_segment(data: Dict, config: Dict) -> str:
    """Build the directory display segment."""
    directory = extract_workspace_info(data, config)
    colors = config["colors"]

    icon = "📂 " if config["display"]["use_emoji"] else ""
    color = ansi_color(colors["directory"])
    reset = ansi_reset()

    return f"{icon}{color}{directory}{reset}"


# =============================================================================
# MAIN BUILDER
# =============================================================================


def build_status_line(data: Dict, config: Dict) -> str:
    """Build the complete status line from all segments."""
    segments_config = config["segments"]
    display_config = config["display"]
    separator = display_config["separator"]
    colors = config["colors"]

    compact = display_config["compact_mode"]
    if not compact and display_config["auto_compact_width"] > 0:
        term_width = get_terminal_width()
        if term_width < display_config["auto_compact_width"]:
            compact = True

    segments = []

    if segments_config["model"]:
        segments.append(build_model_segment(data, config))

    if segments_config["context"]:
        segments.append(build_context_segment(data, config))

    if segments_config["cost"]:
        segments.append(build_cost_segment(data, config))

    if not compact:
        if segments_config.get("tokens", True):
            segments.append(build_tokens_segment(data, config))

        if segments_config["session"]:
            segments.append(build_session_segment(data, config))

        if segments_config.get("compaction", True):
            compaction_segment = build_compaction_segment(data, config)
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

    sep_color = ansi_color(colors["separator"])
    reset = ansi_reset()
    colored_sep = f"{sep_color}{separator}{reset}"

    return colored_sep.join(segments)


# =============================================================================
# ENTRY POINT
# =============================================================================


def main() -> None:
    """Main entry point."""
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

        status_line = build_status_line(data, config)
        print(status_line)

    except Exception as e:
        debug_log(f"Unexpected error: {e}")
        print(f"ECW: Error - {type(e).__name__}")


if __name__ == "__main__":
    main()

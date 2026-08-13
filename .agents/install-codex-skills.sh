#!/usr/bin/env bash
#
# install-codex-skills.sh — deterministic setup for the Jerry Codex skill ports.
#
# Copies (or symlinks) the skills in .agents/skills/ into Codex's discovery
# directory ($CODEX_HOME/skills, default ~/.codex/skills) and validates each one
# against the same rules Codex's bundled quick_validate.py enforces.
#
# Usage:
#   ./.agents/install-codex-skills.sh [options] [skill ...]
#
# Options:
#   --link        Symlink skills instead of copying (repo stays source of truth)
#   --copy        Copy skills (default; self-contained, survives repo moves)
#   --validate    Validate only — install nothing
#   --uninstall   Remove the named skills from the Codex skills dir
#   --dest DIR    Override target dir (default: $CODEX_HOME/skills or ~/.codex/skills)
#   --dry-run     Print actions without changing anything
#   -h, --help    Show this help
#
# Skills: names of folders under .agents/skills/ (default: all of them).
# Examples:
#   ./.agents/install-codex-skills.sh                 # install all (copy) + validate
#   ./.agents/install-codex-skills.sh --link          # symlink all
#   ./.agents/install-codex-skills.sh --validate      # just run the validation tests
#   ./.agents/install-codex-skills.sh eng-team        # only eng-team
#   ./.agents/install-codex-skills.sh --uninstall adversary

set -euo pipefail

# --- locate self / source skills dir ----------------------------------------
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/skills"

# --- defaults ----------------------------------------------------------------
MODE="copy"            # copy | link
ACTION="install"       # install | validate | uninstall
DRY_RUN=0
DEST="${CODEX_HOME:-$HOME/.codex}/skills"
declare -a SKILLS=()

# --- pretty output (only colorize a TTY) -------------------------------------
if [ -t 1 ]; then
  C_OK=$'\033[32m'; C_ERR=$'\033[31m'; C_DIM=$'\033[2m'; C_B=$'\033[1m'; C_0=$'\033[0m'
else
  C_OK=""; C_ERR=""; C_DIM=""; C_B=""; C_0=""
fi
say()  { printf '%s\n' "$*"; }
info() { printf '%s\n' "${C_DIM}$*${C_0}"; }
ok()   { printf '%s\n' "${C_OK}✓${C_0} $*"; }
err()  { printf '%s\n' "${C_ERR}✗${C_0} $*" >&2; }

usage() { sed -n '3,32p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

# --- arg parsing -------------------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --link)      MODE="link" ;;
    --copy)      MODE="copy" ;;
    --validate)  ACTION="validate" ;;
    --uninstall) ACTION="uninstall" ;;
    --dest)      DEST="${2:?--dest needs a path}"; shift ;;
    --dry-run)   DRY_RUN=1 ;;
    -h|--help)   usage 0 ;;
    --*)         err "unknown option: $1"; usage 1 ;;
    *)           SKILLS+=("$1") ;;
  esac
  shift
done

[ -d "$SRC_DIR" ] || { err "no skills dir at $SRC_DIR"; exit 1; }

# default: every skill folder containing a SKILL.md
if [ "${#SKILLS[@]}" -eq 0 ]; then
  while IFS= read -r d; do SKILLS+=("$(basename "$d")"); done \
    < <(find "$SRC_DIR" -mindepth 1 -maxdepth 1 -type d | sort)
fi

run() { if [ "$DRY_RUN" -eq 1 ]; then info "  would: $*"; else eval "$@"; fi; }

# --- validation: mirrors Codex quick_validate.py (no deps) -------------------
# Returns 0 + "valid" message, or 1 + reason.
validate_skill() {
  local dir="$1" md="$1/SKILL.md" fm name
  [ -f "$md" ] || { echo "SKILL.md not found"; return 1; }
  head -n1 "$md" | grep -q '^---$' || { echo "no YAML frontmatter"; return 1; }

  # frontmatter = lines between the first --- and the next ---
  fm="$(awk 'NR==1&&$0=="---"{f=1;next} f&&$0=="---"{exit} f{print}' "$md")"
  [ -n "$fm" ] || { echo "empty frontmatter"; return 1; }

  printf '%s\n' "$fm" | grep -q '^name:'        || { echo "missing 'name'"; return 1; }
  printf '%s\n' "$fm" | grep -q '^description:' || { echo "missing 'description'"; return 1; }

  # allowed top-level keys: name, description, license, allowed-tools, metadata
  local badkey
  badkey="$(printf '%s\n' "$fm" | grep -E '^[A-Za-z0-9_-]+:' \
    | sed -E 's/^([A-Za-z0-9_-]+):.*/\1/' \
    | grep -vxE 'name|description|license|allowed-tools|metadata' | head -n1 || true)"
  [ -z "$badkey" ] || { echo "unexpected frontmatter key: $badkey"; return 1; }

  # name: hyphen-case, <=64, no leading/trailing/double hyphen
  name="$(printf '%s\n' "$fm" | awk -F':' '/^name:/{sub(/^name:[[:space:]]*/,"");print;exit}' | tr -d ' "'"'"'')"
  printf '%s' "$name" | grep -Eq '^[a-z0-9-]+$' || { echo "name '$name' not hyphen-case"; return 1; }
  case "$name" in -*|*-) echo "name '$name' cannot start/end with hyphen"; return 1;; esac
  [[ "$name" != *--* ]] || { echo "name '$name' has consecutive hyphens"; return 1; }
  [ "${#name}" -le 64 ] || { echo "name too long (${#name} > 64)"; return 1; }

  # description must not contain angle brackets (after stripping folding indicators >-, >, |, |-)
  local fm_clean
  fm_clean="$(printf '%s\n' "$fm" | sed -E 's/^([A-Za-z0-9_-]+):[[:space:]]*[>|][-+]?[[:space:]]*$/\1:/')"
  if printf '%s\n' "$fm_clean" | grep -q '[<>]'; then
    echo "description/frontmatter contains angle brackets (< or >)"; return 1
  fi
  echo "valid"; return 0
}

# Optional authoritative second pass with Codex's bundled validator, if present.
codex_validator() {
  local v="$DEST/.system/skill-creator/scripts/quick_validate.py"
  [ -f "$v" ] || return 2
  local py=""
  if python3 -c 'import yaml' >/dev/null 2>&1; then py="python3";
  elif command -v uv >/dev/null 2>&1; then py="uv run --with pyyaml python"; fi
  [ -n "$py" ] || return 2
  $py "$v" "$1" >/dev/null 2>&1 && return 0 || return 1
}

# --- main --------------------------------------------------------------------
say "${C_B}Jerry → Codex skill setup${C_0}"
info "source: $SRC_DIR"
info "target: $DEST"
DRY_LABEL=""; [ "$DRY_RUN" -eq 1 ] && DRY_LABEL=" (dry-run)"
info "mode:   $MODE$DRY_LABEL   action: $ACTION"
say ""

fail=0
declare -a SUMMARY=()

for skill in "${SKILLS[@]}"; do
  src="$SRC_DIR/$skill"
  dst="$DEST/$skill"

  if [ "$ACTION" = "uninstall" ]; then
    if [ -e "$dst" ] || [ -L "$dst" ]; then
      run "rm -rf \"$dst\""; ok "removed $skill"; SUMMARY+=("$skill	removed")
    else
      info "$skill not installed — nothing to remove"; SUMMARY+=("$skill	absent")
    fi
    continue
  fi

  if [ ! -d "$src" ]; then err "$skill: not found in source"; fail=1; SUMMARY+=("$skill	MISSING"); continue; fi

  # validate (bash, dependency-free)
  if msg="$(validate_skill "$src")"; then
    ok "$skill: $msg"
  else
    err "$skill: $msg"; fail=1; SUMMARY+=("$skill	INVALID: $msg"); continue
  fi

  if [ "$ACTION" = "validate" ]; then SUMMARY+=("$skill	valid"); continue; fi

  # install (idempotent: clear any prior target first)
  run "mkdir -p \"$DEST\""
  if [ -e "$dst" ] || [ -L "$dst" ]; then run "rm -rf \"$dst\""; fi
  verb="copied"; [ "$MODE" = "link" ] && verb="symlinked"
  if [ "$MODE" = "link" ]; then run "ln -s \"$src\" \"$dst\""; else run "cp -R \"$src\" \"$dst\""; fi
  if [ "$DRY_RUN" -eq 1 ]; then ok "$skill: would be $verb → $dst"; else ok "$skill: $verb → $dst"; fi

  # authoritative re-check with Codex's own validator if available
  if [ "$DRY_RUN" -eq 0 ]; then
    if codex_validator "$dst"; then ok "$skill: passes Codex quick_validate.py"
    else case $? in 2) info "$skill: (Codex validator not available — bash check only)";;
                    *) err "$skill: FAILED Codex quick_validate.py"; fail=1;; esac; fi
  fi
  SUMMARY+=("$skill	$([ "$MODE" = link ] && echo symlinked || echo copied)")
done

# --- summary -----------------------------------------------------------------
say ""
say "${C_B}Summary${C_0}"
printf '%s\n' "${SUMMARY[@]}" | while IFS=$'\t' read -r s state; do
  printf '  %-14s %s\n' "$s" "$state"
done

if [ "$ACTION" = "install" ] && [ "$DRY_RUN" -eq 0 ] && [ "$fail" -eq 0 ]; then
  say ""
  ok "Done. Restart Codex (or run /skills) to pick up the changes."
fi
exit "$fail"

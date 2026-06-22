#!/usr/bin/env bash
# Portable OPC Toolkit installer for Agent Skills-compatible hosts.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
SKILLS_ROOT="$ROOT_DIR/skills"
BUNDLE_FILE="$ROOT_DIR/bundle.json"
TOOLKIT_NAME="opc-toolkit"
TOOLKIT_VERSION="1.0.0"

SKILL_DIRS=(
  "opc-toolkit"
  "opc-proposal"
  "brief-analysis"
  "competitor-analysis"
  "consumer-insight"
  "campaign-planning"
  "social-media-plan"
  "platform-adaptation"
  "platform-specs"
  "marketing-proposal"
  "task-decomposition"
)

AGENT="codex"
SCOPE="global"
PROJECT_PATH="$(pwd -P)"
TARGET_OVERRIDE=""
DRY_RUN=0
LIST_ONLY=0
DOCTOR=0
NO_BACKUP=0
SELECTED_SKILLS=()

usage() {
  cat <<'EOF'
Usage: ./install.sh [options]

Target:
  --agent <name>       codex|claude|cursor|copilot|gemini|agents|custom
  --global             Install to the agent's user-level skills directory
  --project [path]     Install to the agent's project-level skills directory
  --target <path>      Install to an explicit skills directory

Selection:
  --skill <name>       Install one skill; repeat to install several
  --all                Install all bundled skills (default)

Safety and diagnostics:
  --dry-run            Show changes without writing
  --doctor             Validate source and compare the target installation
  --no-backup          Replace changed skills without retaining backups
  --list               List bundled skills
  --version            Print toolkit version
  -h, --help           Show this help

Examples:
  ./install.sh --agent codex --global
  ./install.sh --agent claude --project /path/to/project
  ./install.sh --agent cursor --skill opc-toolkit --skill opc-proposal
  ./install.sh --target /custom/agent/skills
EOF
}

contains_skill() {
  local wanted="$1"
  local item
  for item in "${SKILL_DIRS[@]}"; do
    [[ "$item" == "$wanted" ]] && return 0
  done
  return 1
}

selected_skills() {
  if [[ "${#SELECTED_SKILLS[@]}" -eq 0 ]]; then
    printf '%s\n' "${SKILL_DIRS[@]}"
  else
    printf '%s\n' "${SELECTED_SKILLS[@]}"
  fi
}

skill_name() {
  awk -F': *' '/^name:/ {gsub(/["'\'']/, "", $2); print $2; exit}' "$1/SKILL.md"
}

list_skills() {
  local dir
  printf 'OPC Toolkit %s includes:\n' "$TOOLKIT_VERSION"
  for dir in "${SKILL_DIRS[@]}"; do
    if [[ -f "$SKILLS_ROOT/$dir/SKILL.md" ]]; then
      printf '  $%s\n' "$(skill_name "$SKILLS_ROOT/$dir")"
    else
      printf '  %s (missing SKILL.md)\n' "$dir"
    fi
  done
}

resolve_target() {
  if [[ -n "$TARGET_OVERRIDE" ]]; then
    printf '%s\n' "$TARGET_OVERRIDE"
    return
  fi

  case "$AGENT:$SCOPE" in
    codex:global)   printf '%s\n' "${CODEX_HOME:-$HOME/.codex}/skills" ;;
    codex:project)  printf '%s\n' "$PROJECT_PATH/.codex/skills" ;;
    claude:global)  printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills" ;;
    claude:project) printf '%s\n' "$PROJECT_PATH/.claude/skills" ;;
    cursor:global)  printf '%s\n' "$HOME/.cursor/skills" ;;
    cursor:project) printf '%s\n' "$PROJECT_PATH/.cursor/skills" ;;
    copilot:global) printf '%s\n' "$HOME/.copilot/skills" ;;
    copilot:project) printf '%s\n' "$PROJECT_PATH/.github/skills" ;;
    gemini:global)  printf '%s\n' "$HOME/.gemini/skills" ;;
    gemini:project) printf '%s\n' "$PROJECT_PATH/.gemini/skills" ;;
    agents:global)  printf '%s\n' "$HOME/.agents/skills" ;;
    agents:project) printf '%s\n' "$PROJECT_PATH/.agents/skills" ;;
    custom:*)
      echo "--agent custom requires --target <path>" >&2
      return 2
      ;;
    *)
      echo "Unsupported agent: $AGENT" >&2
      return 2
      ;;
  esac
}

validate_source() {
  local dir declared
  [[ -f "$BUNDLE_FILE" ]] || {
    echo "Missing bundle manifest: $BUNDLE_FILE" >&2
    return 1
  }

  if command -v python3 >/dev/null 2>&1 && [[ -f "$ROOT_DIR/scripts/validate_bundle.py" ]]; then
    python3 "$ROOT_DIR/scripts/validate_bundle.py" --root "$ROOT_DIR" --quiet
    return
  fi

  for dir in "${SKILL_DIRS[@]}"; do
    [[ -f "$SKILLS_ROOT/$dir/SKILL.md" ]] || {
      echo "Missing skill: $dir/SKILL.md" >&2
      return 1
    }
    declared="$(skill_name "$SKILLS_ROOT/$dir")"
    [[ "$declared" == "$dir" ]] || {
      echo "Skill folder/name mismatch: $dir != $declared" >&2
      return 1
    }
  done
}

same_tree() {
  local src="$1"
  local dest="$2"
  [[ -d "$dest" ]] || return 1
  diff -qr "$src" "$dest" >/dev/null 2>&1
}

doctor() {
  local target="$1"
  local failed=0
  local name src dest

  echo "Source validation: passed"
  echo "Target: $target"
  if [[ ! -d "$target" ]]; then
    echo "Target directory does not exist."
    return 1
  fi

  while IFS= read -r name; do
    src="$SKILLS_ROOT/$name"
    dest="$target/$name"
    if [[ ! -e "$dest" ]]; then
      echo "Missing:   \$$name"
      failed=1
    elif [[ -L "$dest" ]]; then
      echo "Unsafe:    \$$name is a symbolic link"
      failed=1
    elif same_tree "$src" "$dest"; then
      echo "Healthy:   \$$name"
    else
      echo "Different: \$$name (installed copy differs from this package)"
      failed=1
    fi
  done < <(selected_skills)
  return "$failed"
}

rollback_install() {
  local target="$1"
  local backup_root="$2"
  shift 2
  local name
  for name in "$@"; do
    if [[ -e "$target/$name" && ! -L "$target/$name" ]]; then
      rm -rf "$target/$name"
    fi
    if [[ -d "$backup_root/$name" ]]; then
      mv "$backup_root/$name" "$target/$name"
    fi
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)
      [[ $# -ge 2 ]] || { echo "Missing value for --agent" >&2; exit 2; }
      AGENT="$2"
      shift 2
      ;;
    --global)
      SCOPE="global"
      shift
      ;;
    --project)
      SCOPE="project"
      if [[ $# -ge 2 && "$2" != --* ]]; then
        PROJECT_PATH="$(cd "$2" 2>/dev/null && pwd -P || printf '%s' "$2")"
        shift 2
      else
        PROJECT_PATH="$(pwd -P)"
        shift
      fi
      ;;
    --target)
      [[ $# -ge 2 ]] || { echo "Missing value for --target" >&2; exit 2; }
      TARGET_OVERRIDE="$2"
      AGENT="custom"
      shift 2
      ;;
    --skill)
      [[ $# -ge 2 ]] || { echo "Missing value for --skill" >&2; exit 2; }
      contains_skill "$2" || { echo "Unknown bundled skill: $2" >&2; exit 2; }
      SELECTED_SKILLS+=("$2")
      shift 2
      ;;
    --all)
      SELECTED_SKILLS=()
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --doctor)
      DOCTOR=1
      shift
      ;;
    --no-backup)
      NO_BACKUP=1
      shift
      ;;
    --legacy-agents)
      AGENT="agents"
      SCOPE="global"
      shift
      ;;
    --list)
      LIST_ONLY=1
      shift
      ;;
    --version)
      echo "$TOOLKIT_VERSION"
      exit 0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "$LIST_ONLY" -eq 1 ]]; then
  list_skills
  exit 0
fi

validate_source
TARGET_DIR="$(resolve_target)"

if [[ "$DOCTOR" -eq 1 ]]; then
  doctor "$TARGET_DIR"
  exit $?
fi

if [[ -L "$TARGET_DIR" ]]; then
  echo "Refusing to install into symbolic-link target: $TARGET_DIR" >&2
  exit 1
fi

echo "OPC Toolkit $TOOLKIT_VERSION"
echo "Agent:  $AGENT"
echo "Scope:  $SCOPE"
echo "Target: $TARGET_DIR"
[[ "$DRY_RUN" -eq 1 ]] && echo "Mode:   dry run"
echo ""

CHANGED_SKILLS=()
UNCHANGED=0
while IFS= read -r name; do
  src="$SKILLS_ROOT/$name"
  dest="$TARGET_DIR/$name"
  if [[ -L "$dest" ]]; then
    echo "Refusing to replace symbolic link: $dest" >&2
    exit 1
  fi
  if same_tree "$src" "$dest"; then
    echo "Unchanged: \$$name"
    UNCHANGED=$((UNCHANGED + 1))
  else
    CHANGED_SKILLS+=("$name")
    if [[ -e "$dest" ]]; then
      echo "Update:    \$$name"
    else
      echo "Install:   \$$name"
    fi
  fi
done < <(selected_skills)

if [[ "$DRY_RUN" -eq 1 || "${#CHANGED_SKILLS[@]}" -eq 0 ]]; then
  echo ""
  echo "Done: ${#CHANGED_SKILLS[@]} change(s), $UNCHANGED unchanged."
  exit 0
fi

mkdir -p "$TARGET_DIR"
STAGE_DIR="$(mktemp -d "$TARGET_DIR/.opc-toolkit-stage.XXXXXX")"
BACKUP_ROOT="$TARGET_DIR/.opc-toolkit-backups/$(date '+%Y%m%d-%H%M%S')"
trap 'rm -rf "$STAGE_DIR"' EXIT

for name in "${CHANGED_SKILLS[@]}"; do
  cp -R "$SKILLS_ROOT/$name" "$STAGE_DIR/$name"
  [[ "$(skill_name "$STAGE_DIR/$name")" == "$name" ]] || {
    echo "Staged skill validation failed: $name" >&2
    exit 1
  }
done

if [[ "$NO_BACKUP" -eq 0 ]]; then
  for name in "${CHANGED_SKILLS[@]}"; do
    if [[ -e "$TARGET_DIR/$name" ]]; then
      mkdir -p "$BACKUP_ROOT"
      mv "$TARGET_DIR/$name" "$BACKUP_ROOT/$name"
    fi
  done
else
  for name in "${CHANGED_SKILLS[@]}"; do
    [[ -e "$TARGET_DIR/$name" ]] && rm -rf "$TARGET_DIR/$name"
  done
fi

INSTALLED_NOW=()
for name in "${CHANGED_SKILLS[@]}"; do
  if mv "$STAGE_DIR/$name" "$TARGET_DIR/$name"; then
    INSTALLED_NOW+=("$name")
  else
    echo "Install failed while activating \$$name; rolling back." >&2
    rollback_install "$TARGET_DIR" "$BACKUP_ROOT" "${CHANGED_SKILLS[@]}"
    exit 1
  fi
done

echo ""
echo "Done: ${#INSTALLED_NOW[@]} installed/updated, $UNCHANGED unchanged."
if [[ -d "$BACKUP_ROOT" ]]; then
  echo "Backup: $BACKUP_ROOT"
fi
echo "Start a new agent session, then invoke: \$opc-toolkit"

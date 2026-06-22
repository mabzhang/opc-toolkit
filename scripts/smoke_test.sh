#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/opc-toolkit-test.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

assert_file() {
  [[ -f "$1" ]] || {
    echo "Expected file not found: $1" >&2
    exit 1
  }
}

assert_skill_count() {
  local target="$1"
  local count
  count="$(find "$target" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
  [[ "$count" == "11" ]] || {
    echo "Expected 11 installed skills in $target, found $count" >&2
    exit 1
  }
}

bash -n "$ROOT_DIR/install.sh"
python3 -m py_compile "$ROOT_DIR/install.py"
python3 "$ROOT_DIR/scripts/validate_bundle.py" --root "$ROOT_DIR"

for agent in codex claude cursor copilot gemini agents; do
  home="$TMP_DIR/home-$agent"
  mkdir -p "$home"
  HOME="$home" "$ROOT_DIR/install.sh" --agent "$agent" --global >/dev/null
done

assert_skill_count "$TMP_DIR/home-codex/.codex/skills"
assert_skill_count "$TMP_DIR/home-claude/.claude/skills"
assert_skill_count "$TMP_DIR/home-cursor/.cursor/skills"
assert_skill_count "$TMP_DIR/home-copilot/.copilot/skills"
assert_skill_count "$TMP_DIR/home-gemini/.gemini/skills"
assert_skill_count "$TMP_DIR/home-agents/.agents/skills"

custom_target="$TMP_DIR/custom/skills"
"$ROOT_DIR/install.sh" --target "$custom_target" --skill opc-toolkit --skill opc-proposal >/dev/null
assert_file "$custom_target/opc-toolkit/SKILL.md"
assert_file "$custom_target/opc-proposal/SKILL.md"

HOME="$TMP_DIR/home-codex" "$ROOT_DIR/install.sh" --agent codex --global >/dev/null
HOME="$TMP_DIR/home-codex" "$ROOT_DIR/install.sh" --agent codex --global --doctor >/dev/null

project="$TMP_DIR/project"
mkdir -p "$project"
"$ROOT_DIR/install.sh" --agent copilot --project "$project" --skill opc-toolkit >/dev/null
assert_file "$project/.github/skills/opc-toolkit/SKILL.md"

python_target="$TMP_DIR/python/skills"
HOME="$TMP_DIR/python-home" python3 "$ROOT_DIR/install.py" --target "$python_target" >/dev/null
assert_skill_count "$python_target"
HOME="$TMP_DIR/python-home" python3 "$ROOT_DIR/install.py" --target "$python_target" --doctor >/dev/null

release_dir="$TMP_DIR/release"
python3 "$ROOT_DIR/scripts/build_release.py" --root "$ROOT_DIR" --output-dir "$release_dir" >/dev/null
assert_file "$release_dir/$(date '+%m%d')-OPC工具包-安装包-01.zip"
assert_file "$release_dir/$(date '+%m%d')-OPC工具包-安装包-01.tar.gz"

echo "Smoke tests passed."

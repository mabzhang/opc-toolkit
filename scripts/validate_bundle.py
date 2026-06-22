#!/usr/bin/env python3
"""Validate OPC Toolkit without third-party Python dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TODO_MARKERS = ("[TODO:", "TODO:")
NAME_RE = re.compile(r"^name:\s*[\"']?([^\"'\n]+?)[\"']?\s*$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:\s*(.*)$", re.MULTILINE)
REFERENCE_RE = re.compile(r"(?<![\w/])(references/[A-Za-z0-9._/-]+\.md)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the OPC Toolkit bundle.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {path.relative_to(path.parents[1])}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path} must contain a JSON object")
        return {}
    return value


def frontmatter(text: str, path: Path, errors: list[str]) -> str:
    if not text.startswith("---\n"):
        errors.append(f"{path}: missing YAML frontmatter")
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        errors.append(f"{path}: unclosed YAML frontmatter")
        return ""
    return text[4:end]


def description_text(fm: str) -> str:
    match = DESCRIPTION_RE.search(fm)
    if not match:
        return ""
    first = match.group(1).strip()
    lines = []
    if first not in (">", "|", ">-", "|-"):
        lines.append(first.strip("\"'"))
    start = match.end()
    remaining = fm[start:].lstrip("\r\n")
    for line in remaining.splitlines():
        if not line.startswith((" ", "\t")):
            break
        lines.append(line.strip())
    return " ".join(part for part in lines if part)


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return

    text = skill_file.read_text(encoding="utf-8")
    fm = frontmatter(text, skill_file, errors)
    name_match = NAME_RE.search(fm)
    name = name_match.group(1).strip() if name_match else ""
    if not name:
        errors.append(f"{skill_file}: frontmatter name is missing")
    elif name != skill_dir.name:
        errors.append(f"{skill_file}: name '{name}' does not match folder '{skill_dir.name}'")

    description = description_text(fm)
    if len(description) < 30:
        errors.append(f"{skill_file}: description is too short or missing")

    if any(marker in text for marker in TODO_MARKERS):
        errors.append(f"{skill_file}: contains TODO placeholders")

    for reference in sorted(set(REFERENCE_RE.findall(text))):
        if not (skill_dir / reference).is_file():
            errors.append(f"{skill_file}: broken relative reference '{reference}'")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")
    else:
        metadata = openai_yaml.read_text(encoding="utf-8")
        for required in ("display_name:", "short_description:", "default_prompt:"):
            if required not in metadata:
                errors.append(f"{openai_yaml}: missing {required[:-1]}")
        if name and f"${name}" not in metadata:
            errors.append(f"{openai_yaml}: default_prompt must mention ${name}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []

    bundle = load_json(root / "bundle.json", errors)
    bundle_name = bundle.get("name")
    version = bundle.get("version")
    declared_skills = bundle.get("skills")
    if bundle_name != "opc-toolkit":
        errors.append("bundle.json name must be 'opc-toolkit'")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("bundle.json version must use semantic versioning")
    if not isinstance(declared_skills, list) or not all(
        isinstance(item, str) and item for item in declared_skills
    ):
        errors.append("bundle.json skills must be a non-empty string array")
        declared_skills = []

    skills_root = root / "skills"
    actual_skills = sorted(
        path.name for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    ) if skills_root.is_dir() else []
    if sorted(declared_skills) != actual_skills:
        errors.append(
            "bundle.json skills do not match skills/ directories: "
            f"declared={sorted(declared_skills)}, actual={actual_skills}"
        )

    for name in actual_skills:
        validate_skill(skills_root / name, errors)

    codex = load_json(root / ".codex-plugin" / "plugin.json", errors)
    if codex.get("name") != bundle_name:
        errors.append("Codex plugin name must match bundle name")
    if codex.get("version") != version:
        errors.append("Codex plugin version must match bundle version")
    if codex.get("skills") not in ("./skills", "./skills/"):
        errors.append("Codex plugin skills path must be ./skills/")

    claude = load_json(root / ".claude-plugin" / "plugin.json", errors)
    if claude.get("name") != bundle_name:
        errors.append("Claude plugin name must match bundle name")
    if claude.get("version") != version:
        errors.append("Claude plugin version must match bundle version")

    install_script = root / "install.sh"
    if not install_script.is_file():
        errors.append("missing install.sh")
    elif install_script.stat().st_mode & 0o111 == 0:
        errors.append("install.sh must be executable")

    if errors:
        print("Bundle validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(
            f"Bundle validation passed: {bundle_name} {version} "
            f"({len(actual_skills)} skills)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

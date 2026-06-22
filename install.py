#!/usr/bin/env python3
"""Cross-platform installer for OPC Toolkit Agent Skills."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILLS_ROOT = ROOT / "skills"
VERSION = "1.0.0"
SKILLS = [
    "opc-toolkit",
    "opc-proposal",
    "brief-analysis",
    "competitor-analysis",
    "consumer-insight",
    "campaign-planning",
    "social-media-plan",
    "platform-adaptation",
    "platform-specs",
    "marketing-proposal",
    "task-decomposition",
]


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Install OPC Toolkit Agent Skills.")
    value.add_argument(
        "--agent",
        default="codex",
        choices=["codex", "claude", "cursor", "copilot", "gemini", "agents", "custom"],
    )
    scope = value.add_mutually_exclusive_group()
    scope.add_argument("--global", dest="scope", action="store_const", const="global")
    scope.add_argument(
        "--project",
        nargs="?",
        const=".",
        metavar="PATH",
        help="Install to a project-level skills directory.",
    )
    value.set_defaults(scope="global")
    value.add_argument("--target", help="Explicit skills directory.")
    value.add_argument("--skill", action="append", choices=SKILLS)
    value.add_argument("--dry-run", action="store_true")
    value.add_argument("--doctor", action="store_true")
    value.add_argument("--no-backup", action="store_true")
    value.add_argument("--list", action="store_true")
    value.add_argument("--version", action="version", version=VERSION)
    return value


def resolve_target(args: argparse.Namespace) -> Path:
    if args.target:
        return Path(args.target).expanduser().resolve()

    project = Path(args.project or ".").expanduser().resolve()
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser()
    claude_home = Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")).expanduser()
    targets = {
        ("codex", "global"): codex_home / "skills",
        ("codex", "project"): project / ".codex" / "skills",
        ("claude", "global"): claude_home / "skills",
        ("claude", "project"): project / ".claude" / "skills",
        ("cursor", "global"): home / ".cursor" / "skills",
        ("cursor", "project"): project / ".cursor" / "skills",
        ("copilot", "global"): home / ".copilot" / "skills",
        ("copilot", "project"): project / ".github" / "skills",
        ("gemini", "global"): home / ".gemini" / "skills",
        ("gemini", "project"): project / ".gemini" / "skills",
        ("agents", "global"): home / ".agents" / "skills",
        ("agents", "project"): project / ".agents" / "skills",
    }
    scope = "project" if args.project is not None else args.scope
    if args.agent == "custom":
        raise SystemExit("--agent custom requires --target PATH")
    return targets[(args.agent, scope)].resolve()


def same_tree(left: Path, right: Path) -> bool:
    if not right.is_dir() or right.is_symlink():
        return False
    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.funny_files:
        return False
    if any(
        not filecmp.cmp(left / name, right / name, shallow=False)
        for name in comparison.common_files
    ):
        return False
    return all(
        same_tree(left / name, right / name)
        for name in comparison.common_dirs
    )


def validate_source() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_bundle.py"),
            "--root",
            str(ROOT),
            "--quiet",
        ],
        check=True,
    )


def doctor(target: Path, selected: list[str]) -> int:
    print("Source validation: passed")
    print(f"Target: {target}")
    failed = False
    for name in selected:
        destination = target / name
        if not destination.exists():
            print(f"Missing:   ${name}")
            failed = True
        elif destination.is_symlink():
            print(f"Unsafe:    ${name} is a symbolic link")
            failed = True
        elif same_tree(SKILLS_ROOT / name, destination):
            print(f"Healthy:   ${name}")
        else:
            print(f"Different: ${name}")
            failed = True
    return int(failed)


def main() -> int:
    args = parser().parse_args()
    if args.list:
        print(f"OPC Toolkit {VERSION} includes:")
        for name in SKILLS:
            print(f"  ${name}")
        return 0

    validate_source()
    selected = args.skill or SKILLS
    target = resolve_target(args)
    if target.is_symlink():
        raise SystemExit(f"Refusing symbolic-link target: {target}")
    if args.doctor:
        return doctor(target, selected)

    print(f"OPC Toolkit {VERSION}")
    print(f"Agent:  {args.agent}")
    print(f"Target: {target}")
    if args.dry_run:
        print("Mode:   dry run")
    print()

    changed: list[str] = []
    unchanged = 0
    for name in selected:
        source = SKILLS_ROOT / name
        destination = target / name
        if destination.is_symlink():
            raise SystemExit(f"Refusing to replace symbolic link: {destination}")
        if same_tree(source, destination):
            print(f"Unchanged: ${name}")
            unchanged += 1
        else:
            print(f"{'Update' if destination.exists() else 'Install'}:    ${name}")
            changed.append(name)

    if args.dry_run or not changed:
        print(f"\nDone: {len(changed)} change(s), {unchanged} unchanged.")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".opc-toolkit-stage-", dir=target))
    backup = target / ".opc-toolkit-backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    activated: list[str] = []
    backed_up: list[str] = []
    try:
        for name in changed:
            shutil.copytree(SKILLS_ROOT / name, stage / name)

        for name in changed:
            destination = target / name
            if destination.exists():
                if args.no_backup:
                    shutil.rmtree(destination)
                else:
                    backup.mkdir(parents=True, exist_ok=True)
                    destination.replace(backup / name)
                    backed_up.append(name)

        for name in changed:
            (stage / name).replace(target / name)
            activated.append(name)
    except Exception:
        for name in activated:
            destination = target / name
            if destination.exists():
                shutil.rmtree(destination)
        for name in backed_up:
            saved = backup / name
            if saved.exists():
                saved.replace(target / name)
        raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)

    print(f"\nDone: {len(activated)} installed/updated, {unchanged} unchanged.")
    if backup.exists():
        print(f"Backup: {backup}")
    print("Start a new agent session, then invoke: $opc-toolkit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

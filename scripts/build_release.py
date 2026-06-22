#!/usr/bin/env python3
"""Build deterministic ZIP and tar.gz releases for OPC Toolkit."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import tarfile
import zipfile
from datetime import datetime
from pathlib import Path


FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)
EXCLUDED_NAMES = {".DS_Store", ".git", "__pycache__", "dist"}


def parse_args() -> argparse.Namespace:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build OPC Toolkit release archives.")
    parser.add_argument("--root", default=str(default_root))
    parser.add_argument("--output-dir", default=str(default_root / "dist"))
    parser.add_argument("--release-name")
    return parser.parse_args()


def should_include(path: Path, root: Path, output_dir: Path) -> bool:
    try:
        path.resolve().relative_to(output_dir.resolve())
        return False
    except ValueError:
        pass
    relative = path.relative_to(root)
    if any(part in EXCLUDED_NAMES for part in relative.parts):
        return False
    if path.suffix == ".pyc":
        return False
    return True


def files_to_package(root: Path, output_dir: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and should_include(path, root, output_dir)
    )


def archive_path(root: Path, path: Path) -> str:
    return f"opc-toolkit/{path.relative_to(root).as_posix()}"


def build_zip(root: Path, output: Path, files: list[Path]) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            info = zipfile.ZipInfo(archive_path(root, path), FIXED_ZIP_TIME)
            mode = path.stat().st_mode
            info.external_attr = (mode & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())


def build_tar_gz(root: Path, output: Path, files: list[Path]) -> None:
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w") as tf:
                for path in files:
                    data = path.read_bytes()
                    info = tarfile.TarInfo(archive_path(root, path))
                    info.size = len(data)
                    info.mode = stat.S_IMODE(path.stat().st_mode)
                    info.mtime = 0
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    tf.addfile(info, io.BytesIO(data))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    bundle = json.loads((root / "bundle.json").read_text(encoding="utf-8"))

    subprocess.run(
        ["python3", str(root / "scripts" / "validate_bundle.py"), "--root", str(root), "--quiet"],
        check=True,
    )

    release_name = args.release_name or f"{datetime.now():%m%d}-OPC工具包-安装包-01"
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / f"{release_name}.zip"
    tar_path = output_dir / f"{release_name}.tar.gz"
    checksum_path = output_dir / f"{datetime.now():%m%d}-OPC工具包-校验值-01.txt"

    for path in (zip_path, tar_path, checksum_path):
        if path.exists():
            path.unlink()

    files = files_to_package(root, output_dir)
    build_zip(root, zip_path, files)
    build_tar_gz(root, tar_path, files)

    checksum_path.write_text(
        f"{sha256(zip_path)}  {zip_path.name}\n"
        f"{sha256(tar_path)}  {tar_path.name}\n",
        encoding="utf-8",
    )

    print(f"Built OPC Toolkit {bundle['version']}:")
    print(zip_path)
    print(tar_path)
    print(checksum_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

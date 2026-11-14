#!/usr/bin/env python3
"""Verify or deterministically rebuild investor-updates.zip from investor-updates/.

Default mode (--check) verifies byte-for-byte parity between every regular file
under `investor-updates/` and its corresponding entry inside `investor-updates.zip`,
failing on missing entries, stale/extra entries, duplicate archive members, or
content mismatches.

Rebuild mode (--rebuild) writes `investor-updates.zip` deterministically (sorted
entries, fixed UTC timestamp, normalized POSIX permissions, atomic rename) and
re-verifies parity before exiting.
"""
from __future__ import annotations

import argparse
import os
import stat
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILL_DIR = REPO_ROOT / "investor-updates"
DEFAULT_ZIP_PATH = REPO_ROOT / "investor-updates.zip"
FIXED_ZIP_DT = (2026, 1, 1, 0, 0, 0)
IGNORED_NAMES = {".DS_Store"}


def collect_disk_files(skill_dir: Path, archive_prefix: str) -> tuple[dict[str, bytes], list[str]]:
    """Return ({archive_member_path: raw_bytes}, errors)."""
    errors: list[str] = []
    files: dict[str, bytes] = {}
    if not skill_dir.is_dir():
        return files, [f"Skill directory does not exist: {skill_dir}"]

    for path in sorted(skill_dir.rglob("*")):
        rel = path.relative_to(skill_dir).as_posix()
        member = f"{archive_prefix}/{rel}"
        if path.name in IGNORED_NAMES or "__pycache__" in path.parts:
            errors.append(f"Unexpected scratch/OS file in skill directory: {member}")
            continue
        if path.is_symlink():
            errors.append(f"Symlinks are not permitted in skill bundle: {member}")
            continue
        if path.is_file():
            files[member] = path.read_bytes()
    if not files and not errors:
        errors.append(f"No files found under {skill_dir}")
    return files, errors


def check_parity(skill_dir: Path, zip_path: Path) -> list[str]:
    """Return a list of parity errors (empty list means exact byte-for-byte match)."""
    archive_prefix = skill_dir.name
    disk_files, errors = collect_disk_files(skill_dir, archive_prefix)
    if errors:
        return errors

    if not zip_path.is_file():
        return [f"Bundle zip does not exist: {zip_path}"]

    zip_files: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad_member = zf.testzip()
            if bad_member is not None:
                errors.append(f"Corrupt CRC in zip member: {bad_member}")
            for info in zf.infolist():
                name = info.filename
                if not (name == f"{archive_prefix}/" or name.startswith(f"{archive_prefix}/")):
                    errors.append(f"Archive entry outside '{archive_prefix}/': {name}")
                    continue
                if info.is_dir():
                    continue
                if name in zip_files:
                    errors.append(f"Duplicate entry in zip archive: {name}")
                    continue
                zip_files[name] = zf.read(info)
    except zipfile.BadZipFile as exc:
        return [f"Invalid zip file {zip_path}: {exc}"]

    disk_keys = set(disk_files)
    zip_keys = set(zip_files)

    for missing in sorted(disk_keys - zip_keys):
        errors.append(f"Missing from {zip_path.name}: {missing}")
    for stale in sorted(zip_keys - disk_keys):
        errors.append(f"Stale/extra entry in {zip_path.name} (not in {archive_prefix}/): {stale}")
    for common in sorted(disk_keys & zip_keys):
        if disk_files[common] != zip_files[common]:
            errors.append(
                f"Byte mismatch for {common}: "
                f"disk={len(disk_files[common])}B vs zip={len(zip_files[common])}B"
            )
    return errors


def rebuild_zip(skill_dir: Path, zip_path: Path) -> None:
    """Deterministically rebuild `zip_path` from `skill_dir`."""
    archive_prefix = skill_dir.name
    disk_files, errors = collect_disk_files(skill_dir, archive_prefix)
    if errors:
        raise RuntimeError("; ".join(errors))

    dirs = {f"{archive_prefix}/"}
    for member in disk_files:
        parts = member.split("/")
        for idx in range(1, len(parts)):
            dirs.add("/".join(parts[:idx]) + "/")

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{zip_path.name}.", suffix=".tmp", dir=str(zip_path.parent)
    )
    os.close(fd)
    tmp_path = Path(tmp_name)
    try:
        with zipfile.ZipFile(tmp_path, "w") as zf:
            for dname in sorted(dirs):
                dir_info = zipfile.ZipInfo(filename=dname, date_time=FIXED_ZIP_DT)
                dir_info.compress_type = zipfile.ZIP_STORED
                dir_info.external_attr = (stat.S_IFDIR | 0o755) << 16 | 0x10
                zf.writestr(dir_info, b"")
            for member in sorted(disk_files):
                file_info = zipfile.ZipInfo(filename=member, date_time=FIXED_ZIP_DT)
                file_info.compress_type = zipfile.ZIP_DEFLATED
                file_info.external_attr = (stat.S_IFREG | 0o644) << 16
                zf.writestr(file_info, disk_files[member], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        os.replace(tmp_path, zip_path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check or rebuild byte-for-byte parity between investor-updates/ and investor-updates.zip."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Verify investor-updates.zip matches investor-updates/ byte-for-byte (default).",
    )
    mode.add_argument(
        "--rebuild",
        action="store_true",
        help="Deterministically rebuild investor-updates.zip from investor-updates/.",
    )
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=DEFAULT_SKILL_DIR,
        help="Path to the unpacked skill directory (default: investor-updates).",
    )
    parser.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        default=DEFAULT_ZIP_PATH,
        help="Path to the skill zip bundle (default: investor-updates.zip).",
    )
    args = parser.parse_args(argv)

    skill_dir = args.skill_dir.resolve()
    zip_path = args.zip_path.resolve()

    if args.rebuild:
        try:
            rebuild_zip(skill_dir, zip_path)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        errors = check_parity(skill_dir, zip_path)
        if errors:
            for err in errors:
                print(f"FAIL: {err}", file=sys.stderr)
            return 1
        print(f"OK: rebuilt {zip_path.name} deterministically from {skill_dir.name}/")
        return 0

    errors = check_parity(skill_dir, zip_path)
    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        print(
            "Run `python3 scripts/check_zip_parity.py --rebuild` to synchronize investor-updates.zip.",
            file=sys.stderr,
        )
        return 1

    disk_files, _ = collect_disk_files(skill_dir, skill_dir.name)
    print(f"OK: {zip_path.name} matches {skill_dir.name}/ ({len(disk_files)} files, byte-for-byte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

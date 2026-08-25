#!/usr/bin/env python3
"""Install the project-owned KooAI 1688 sourcing adapter into Codex skills."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SKILL_NAME = "kooai-1688-sourcing"
SOURCE = Path(__file__).resolve().parents[1]


def default_target_root() -> Path:
    return Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser() / "skills"


def install(target_root: Path, *, dry_run: bool = False) -> Path:
    destination = target_root.expanduser().resolve() / SKILL_NAME
    print(f"source: {SOURCE}")
    print(f"destination: {destination}")
    if dry_run:
        print("dry-run: no files copied")
        return destination
    target_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        SOURCE,
        destination,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )
    print("installed")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the KooAI 1688 sourcing adapter")
    parser.add_argument("--target-root", type=Path, default=default_target_root())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(args.target_root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

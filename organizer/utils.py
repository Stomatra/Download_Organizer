from __future__ import annotations

from pathlib import Path


def ensure_dir(p: Path, dry_run: bool) -> None:
    if dry_run:
        return
    p.mkdir(parents=True, exist_ok=True)


def unique_path(dest: Path) -> Path:
    """If dest exists, return dest with (1), (2)... suffix before extension."""
    if not dest.exists():
        return dest

    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent

    i = 1
    while True:
        candidate = parent / f"{stem} ({i}){suffix}"
        if not candidate.exists():
            return candidate
        i += 1
from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from .config import Config
from .rules import match_rule
from .utils import ensure_dir, unique_path


@dataclass(frozen=True)
class MoveAction:
    src: Path
    dst: Path
    rule_name: str


def plan_moves(cfg: Config) -> list[MoveAction]:
    actions: list[MoveAction] = []

    if not cfg.download_dir.exists():
        raise FileNotFoundError(f"download_dir does not exist: {cfg.download_dir}")

    for p in cfg.download_dir.iterdir():
        if not p.is_file():
            continue

        ext = p.suffix.lower()
        if ext in cfg.ignore_extensions:
            continue

        rule = match_rule(cfg, p)

        dst_dir = cfg.destination_root / rule.target
        # 可选日期子目录（增强：按修改时间/创建时间）
        if cfg.date_subdir:
            # 简化：用文件 mtime
            ts = p.stat().st_mtime
            import datetime as _dt
            sub = _dt.datetime.fromtimestamp(ts).strftime(cfg.date_subdir)
            dst_dir = dst_dir / sub

        dst = dst_dir / p.name
        actions.append(MoveAction(src=p, dst=dst, rule_name=rule.name))

    return actions


def apply_moves(actions: list[MoveAction], dry_run: bool, verbose: bool) -> None:
    for a in actions:
        final_dst_dir = a.dst.parent
        ensure_dir(final_dst_dir, dry_run=dry_run)

        final_dst = unique_path(a.dst)

        if verbose or dry_run:
            print(f"[{a.rule_name}] MOVE {a.src} -> {final_dst}")

        if not dry_run:
            shutil.move(str(a.src), str(final_dst))
from __future__ import annotations

from pathlib import Path

from .config import Config, Rule


def file_ext(p: Path) -> str:
    return p.suffix.lower()


def match_rule(cfg: Config, p: Path) -> Rule:
    ext = file_ext(p)

    for rule in cfg.rules:
        exts = set(rule.extensions)
        if "*" in exts:
            return rule
        if ext in exts:
            return rule

    # 理论上到不了（因为一般会配 CatchAll *）
    return cfg.rules[-1]
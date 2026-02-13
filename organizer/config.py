from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Rule:
    name: str
    extensions: list[str]
    target: str


@dataclass(frozen=True)
class Config:
    download_dir: Path
    destination_root: Path
    ignore_extensions: set[str]
    rules: list[Rule]
    date_subdir: str | None = None


def _norm_ext(ext: str) -> str:
    ext = ext.strip()
    if ext == "*":
        return "*"
    if not ext.startswith("."):
        ext = "." + ext
    return ext.lower()


def load_config(path: Path) -> Config:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Config root must be a mapping/object")

    download_dir = Path(raw.get("download_dir", "~/Downloads")).expanduser()
    destination_root = Path(raw.get("destination_root", str(download_dir / "Sorted"))).expanduser()
    date_subdir = raw.get("date_subdir", None)

    ignore_extensions = {_norm_ext(x) for x in raw.get("ignore_extensions", [])}

    rules_raw = raw.get("rules", [])
    rules: list[Rule] = []
    for r in rules_raw:
        rules.append(
            Rule(
                name=r["name"],
                extensions=[_norm_ext(e) for e in r.get("extensions", [])],
                target=r["target"],
            )
        )

    if not rules:
        raise ValueError("No rules configured")

    return Config(
        download_dir=download_dir,
        destination_root=destination_root,
        ignore_extensions=ignore_extensions,
        rules=rules,
        date_subdir=date_subdir,
    )
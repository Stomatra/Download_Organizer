from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from .config import Config
from .organizer import apply_moves, plan_moves


@dataclass(frozen=True)
class WatchOptions:
    stable_seconds: float = 4.0
    debounce_seconds: float = 1.0


def is_file_stable(p: Path, stable_seconds: float) -> bool:
    """
    Returns True if file size+mtime stays unchanged for stable_seconds.
    """
    try:
        s1 = p.stat()
    except FileNotFoundError:
        return False

    time.sleep(stable_seconds)

    try:
        s2 = p.stat()
    except FileNotFoundError:
        return False

    return (s1.st_size == s2.st_size) and (s1.st_mtime == s2.st_mtime)


class _DebouncedHandler(FileSystemEventHandler):
    def __init__(self, cfg: Config, dry_run: bool, verbose: bool, opt: WatchOptions) -> None:
        self.cfg = cfg
        self.dry_run = dry_run
        self.verbose = verbose
        self.opt = opt
        self._last_run = 0.0

    def on_any_event(self, event: FileSystemEvent) -> None:
        # 目录事件忽略
        if event.is_directory:
            return

        now = time.time()
        if now - self._last_run < self.opt.debounce_seconds:
            return
        self._last_run = now

        # 这里简单处理：有变化就做一次全量扫描（实现简单且够用）
        actions = plan_moves(self.cfg)

        # 只对“看起来稳定”的文件执行移动（避免下载未完成）
        stable_actions = []
        for a in actions:
            if not a.src.exists():
                continue
            if is_file_stable(a.src, stable_seconds=self.opt.stable_seconds):
                stable_actions.append(a)
            else:
                if self.verbose:
                    print(f"[SKIP] Not stable yet: {a.src}")

        apply_moves(stable_actions, dry_run=self.dry_run, verbose=self.verbose)


def watch_forever(cfg: Config, dry_run: bool, verbose: bool, opt: WatchOptions) -> None:
    handler = _DebouncedHandler(cfg, dry_run=dry_run, verbose=verbose, opt=opt)
    observer = Observer()
    observer.schedule(handler, str(cfg.download_dir), recursive=False)
    observer.start()

    print(f"Watching: {cfg.download_dir}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping watcher...")
    finally:
        observer.stop()
        observer.join()
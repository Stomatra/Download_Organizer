from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .config import load_config
from .organizer import apply_moves, plan_moves


def main() -> int:
    ap = argparse.ArgumentParser(description="Download folder organizer")
    ap.add_argument("--config", type=Path, required=True, help="Path to YAML config")
    ap.add_argument("--dry-run", action="store_true", help="Print actions without moving files")
    ap.add_argument("--verbose", action="store_true", help="Verbose output")
    ap.add_argument("--download-dir", type=Path, default=None, help="Override download_dir in config")

    ap.add_argument("--watch", action="store_true", help="Watch download directory and organize automatically")
    ap.add_argument("--stable-seconds", type=float, default=4.0, help="Seconds a file must be unchanged before moving")
    ap.add_argument("--debounce-seconds", type=float, default=1.0, help="Debounce events before organizing")

    ap.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Append logs to this file (recommended when using pythonw.exe)",
    )

    args = ap.parse_args()

    if args.log_file is not None:
        args.log_file.parent.mkdir(parents=True, exist_ok=True)
        f = open(args.log_file, "a", encoding="utf-8", buffering=1)
        sys.stdout = f
        sys.stderr = f

    cfg = load_config(args.config)
    if args.download_dir is not None:
        cfg = cfg.__class__(
            download_dir=args.download_dir.expanduser(),
            destination_root=cfg.destination_root,
            ignore_extensions=cfg.ignore_extensions,
            rules=cfg.rules,
            date_subdir=cfg.date_subdir,
        )

    if args.watch:
        from .watch import watch_forever, WatchOptions

        watch_forever(
            cfg,
            dry_run=args.dry_run,
            verbose=args.verbose,
            opt=WatchOptions(stable_seconds=args.stable_seconds, debounce_seconds=args.debounce_seconds),
        )
        return 0

    actions = plan_moves(cfg)
    apply_moves(actions, dry_run=args.dry_run, verbose=args.verbose)

    if args.verbose or args.dry_run:
        print(f"Planned {len(actions)} moves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
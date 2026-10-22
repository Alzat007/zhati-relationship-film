#!/usr/bin/env python3
"""Map old scene-relative times to a new scene window.

Example:
  retime_scene.py --old-start 68.1 --old-end 93.4 --new-start 66.2 --new-end 90.8 \
    --times 68.3,70.0,75.7,83.8,93.4
"""
import argparse


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--old-start", type=float, required=True)
    ap.add_argument("--old-end", type=float, required=True)
    ap.add_argument("--new-start", type=float, required=True)
    ap.add_argument("--new-end", type=float, required=True)
    ap.add_argument("--times", required=True, help="comma-separated seconds")
    args = ap.parse_args()

    old_d = args.old_end - args.old_start
    new_d = args.new_end - args.new_start
    if old_d <= 0 or new_d <= 0:
        raise SystemExit("scene durations must be positive")
    scale = new_d / old_d
    print(f"scale = {scale:.6f}")
    for raw in args.times.split(","):
        raw = raw.strip()
        if not raw:
            continue
        t = float(raw)
        if not (args.old_start - 0.001 <= t <= args.old_end + 0.001):
            print(f"{t:8.3f} -> WARNING outside scene")
            continue
        nt = args.new_start + (t - args.old_start) * scale
        print(f"{t:8.3f} -> {nt:8.3f}")


if __name__ == "__main__":
    main()

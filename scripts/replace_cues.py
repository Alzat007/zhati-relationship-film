#!/usr/bin/env python3
"""Replace the CUES array in index.html with cues.json, and optionally retime the root/audio duration.

Usage:
  replace_cues.py --html index.html --cues cues.json --duration 198.5
"""
import argparse, json, re
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default="index.html")
    ap.add_argument("--cues", required=True)
    ap.add_argument("--duration", type=float, default=None)
    args = ap.parse_args()

    html_path = Path(args.html)
    s = html_path.read_text(encoding="utf-8")
    cues = json.loads(Path(args.cues).read_text(encoding="utf-8"))
    if not isinstance(cues, list) or not cues:
        raise SystemExit("cues must be a non-empty list")

    for i, c in enumerate(cues):
        if not {"start", "end", "text"} <= set(c):
            raise SystemExit(f"cue {i}: need start/end/text")
        if float(c["end"]) <= float(c["start"]):
            raise SystemExit(f"cue {i}: end <= start")

    rows = []
    for c in cues:
        text = json.dumps(str(c["text"]), ensure_ascii=False)
        rows.append(f"[{float(c['start']):.2f},{float(c['end']):.2f},{text}]")
    new_arr = "const CUES = [\n" + ",\n".join(rows) + "\n];"

    s2, n = re.subn(r"const CUES = \[.*?\n\];", new_arr, s, flags=re.S)
    if n != 1:
        raise SystemExit(f"expected one CUES array, found {n}")

    if args.duration is not None:
        dur = f"{args.duration:.6f}".rstrip("0").rstrip(".")
        s2, a = re.subn(r'(<div id="film"[^>]*data-duration=")[^"]+(")', rf'\g<1>{dur}\g<2>', s2, count=1)
        s2, b = re.subn(r"const DUR = [0-9.]+;", f"const DUR = {dur};", s2, count=1)
        s2, c = re.subn(r'(<audio id="score"[^>]*data-duration=")[^"]+(")', rf'\g<1>{dur}\g<2>', s2, count=1)
        if a + b + c != 3:
            raise SystemExit(f"duration replacements: root={a} DUR={b} audio={c} (expected 3)")
        print(f"duration -> {dur}")

    html_path.write_text(s2, encoding="utf-8")
    print(f"replaced {len(cues)} cues in {html_path}")


if __name__ == "__main__":
    main()

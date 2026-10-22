#!/usr/bin/env python3
"""Convert a cues.json ([{start,end,text}, ...]) to SRT."""
import argparse, json
from pathlib import Path


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cues", help="cues.json")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    cues = json.loads(Path(args.cues).read_text(encoding="utf-8"))
    if not isinstance(cues, list) or not cues:
        raise SystemExit("cues must be a non-empty JSON list")
    out = Path(args.out) if args.out else Path(args.cues).with_name("字幕.srt")
    lines = []
    for i, c in enumerate(cues, 1):
        text = str(c.get("text", "")).strip()
        if not text:
            continue
        start, end = float(c["start"]), float(c["end"])
        if end <= start:
            raise SystemExit(f"cue {i}: end <= start")
        lines.append(f"{i}\n{ts(start)} --> {ts(end)}\n{text}\n")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out} ({len(lines)} cues)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Download a stock clip, strip audio, normalize to 16:9, and record its license.

Example:
  fetch_stock.py \
    --url https://assets.mixkit.co/videos/2846/2846-1080.mp4 \
    --slug rain-window --source Mixkit \
    --page https://mixkit.co/free-stock-video/rain/ \
    --license "Mixkit License" --credit "Mixkit — Window on a rainy day" \
    --project . --slot clip_01 --scenes hook,umbrella

The script does not bypass paywalls or watermarks. Only download assets whose
license permits your use; keep the source page/license in the metadata.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36")
MAX_BYTES = 300 * 1024 * 1024


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration:stream=width,height,codec_type",
               "-of", "json", str(path)]).stdout
    data = json.loads(out)
    fmt = data.get("format", {})
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    return float(fmt.get("duration", 0) or 0), v.get("width") or 0, v.get("height") or 0


def download(url, page, dest):
    headers = {"User-Agent": UA, "Accept": "video/mp4,video/*;q=0.9,*/*;q=0.8"}
    if page:
        headers["Referer"] = page
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        total = 0
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                raise SystemExit(f"file larger than {MAX_BYTES // 1024 // 1024} MB; aborting")
            f.write(chunk)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--slug", default="")
    ap.add_argument("--source", required=True)
    ap.add_argument("--page", default="")
    ap.add_argument("--license", required=True, dest="license_")
    ap.add_argument("--credit", default="")
    ap.add_argument("--project", default=".")
    ap.add_argument("--slot", default="")
    ap.add_argument("--scenes", default="")
    ap.add_argument("--max-duration", type=float, default=12.0)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--fit", choices=["cover", "contain"], default="cover")
    ap.add_argument("--no-normalize", action="store_true")
    args = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg/ffprobe not found")
    project = Path(args.project).expanduser().resolve()
    imported = project / "assets" / "imported"
    imported.mkdir(parents=True, exist_ok=True)

    slug = args.slug.strip() or Path(urllib.request.urlparse(args.url).path).stem
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", slug).strip("-") or "stock-clip"
    raw = imported / f"{slug}.source"
    out = imported / f"{slug}.mp4"

    print(f"download: {args.url}")
    size = download(args.url, args.page, raw)
    print(f"downloaded: {size / 1024 / 1024:.1f} MB")
    src_dur, src_w, src_h = probe(raw)
    print(f"source: {src_w}x{src_h}  {src_dur:.2f}s")

    duration = min(src_dur, args.max_duration) if src_dur > 0 else args.max_duration
    if args.no_normalize:
        shutil.move(raw, out)
    else:
        if args.fit == "cover":
            vf = (f"scale={args.width}:{args.height}:force_original_aspect_ratio=increase,"
                  f"crop={args.width}:{args.height},fps={args.fps}")
        else:
            vf = (f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,"
                  f"pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2:black,fps={args.fps}")
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw),
               "-t", f"{duration:.3f}", "-vf", vf, "-an",
               "-c:v", "libx264", "-crf", "18", "-preset", "medium",
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
        print("normalize: 1920x1080 / 30fps / no audio")
        run(cmd)
        raw.unlink(missing_ok=True)

    dur, w, h = probe(out)
    meta = {
        "slot": args.slot, "slug": slug, "path": f"assets/imported/{slug}.mp4",
        "source": args.source, "page": args.page, "license": args.license_,
        "credit": args.credit or args.source, "duration": dur,
        "width": w, "height": h, "scenes": [s.strip() for s in args.scenes.split(",") if s.strip()],
    }
    (imported / f"{slug}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_path = project / "assets.manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"episode": project.name, "visual_mode": "licensed_stock", "assets": []}
    manifest.setdefault("assets", [])
    if args.slot:
        entry = {
            "slot": args.slot, "type": "licensed_stock",
            "path": f"assets/imported/{slug}.mp4",
            "source": args.source, "rights": args.license_,
            "credit": args.credit or args.source, "media_start": 0,
            "duration": round(dur, 3), "scenes": meta["scenes"],
        }
        existing = next((a for a in manifest["assets"] if a.get("slot") == args.slot), None)
        if existing:
            existing.update(entry)
        else:
            manifest["assets"].append(entry)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"manifest: updated {manifest_path} slot={args.slot}")
    else:
        print("manifest: no --slot; metadata written but manifest not updated")

    print(f"clip: {out}")
    print("license:", args.license_)
    print("credit:", args.credit or args.source)
    print("next: set data-asset-slot source in index.html/cover.html and re-time the video window; run asset_report.py")


if __name__ == "__main__":
    main()

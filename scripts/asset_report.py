#!/usr/bin/env python3
"""Check an episode's assets.manifest.json: slots, files, rights, credits, scenes.

Usage:
  asset_report.py --manifest assets.manifest.json --project .
  asset_report.py --manifest assets.manifest.json --project . --strict
"""
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
ALLOWED_MODES = {"client_footage", "public_domain_film", "licensed_stock", "photos", "text_only", "mixed"}


def probe(path: Path):
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    try:
        out = subprocess.check_output(
            [ffprobe, "-v", "error", "-show_entries", "format=duration:stream=width,height,codec_type",
             "-of", "json", str(path)], text=True, timeout=15)
        data = json.loads(out)
        fmt = data.get("format", {})
        streams = data.get("streams", [])
        v = next((x for x in streams if x.get("codec_type") == "video"), {})
        return {
            "duration": float(fmt.get("duration", 0) or 0),
            "width": v.get("width"),
            "height": v.get("height"),
        }
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="assets.manifest.json")
    ap.add_argument("--project", default=".")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    project = Path(args.project).expanduser().resolve()
    manifest_path = Path(args.manifest).expanduser()
    if not manifest_path.is_absolute():
        manifest_path = project / manifest_path
    if not manifest_path.exists():
        raise SystemExit(f"manifest not found: {manifest_path}")

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        raise SystemExit("manifest.assets must be a non-empty list")

    mode = str(data.get("visual_mode", "")).strip()
    issues = []
    if mode not in ALLOWED_MODES:
        issues.append(f"visual_mode '{mode}' not in {sorted(ALLOWED_MODES)}")

    seen = set()
    print(f"episode: {data.get('episode', '(unnamed)')}  mode: {mode or '(missing)'}")
    print(f"{'slot':22} {'type':20} {'file':34} {'rights':18} scenes")
    print("-" * 120)

    for i, a in enumerate(assets):
        if not isinstance(a, dict):
            issues.append(f"asset #{i}: not an object")
            continue
        slot = str(a.get("slot", "")).strip()
        typ = str(a.get("type", "")).strip()
        rel = str(a.get("path", "")).strip()
        source = str(a.get("source", "")).strip()
        rights = str(a.get("rights", "")).strip()
        credit = str(a.get("credit", "")).strip()
        scenes = a.get("scenes", [])
        if not slot:
            issues.append(f"asset #{i}: missing slot")
            continue
        if slot in seen:
            issues.append(f"{slot}: duplicate slot")
        seen.add(slot)
        if not typ:
            issues.append(f"{slot}: missing type")
        if not rel:
            issues.append(f"{slot}: missing path")
        if not rights:
            issues.append(f"{slot}: missing rights")
        if not credit:
            issues.append(f"{slot}: missing credit")
        if not scenes:
            issues.append(f"{slot}: missing scenes")

        path = Path(rel).expanduser()
        if not path.is_absolute():
            path = project / path
        exists = path.exists()
        if not exists:
            issues.append(f"{slot}: file not found: {path}")
        meta = probe(path) if exists and path.suffix.lower() in VIDEO_EXT else None
        if meta:
            print(f"{slot:22} {typ:20} {rel:34} {rights:18} {','.join(map(str, scenes))}")
            print(f"{'':22} {'':20} {meta['width']}x{meta['height']}  {meta['duration']:.2f}s")
        else:
            print(f"{slot:22} {typ:20} {rel:34} {rights:18} {','.join(map(str, scenes))}")

    print("-" * 120)
    if issues:
        print(f"issues: {len(issues)}")
        for x in issues:
            print(f"  - {x}")
    else:
        print("issues: 0")
    if args.strict and issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

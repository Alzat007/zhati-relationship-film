#!/usr/bin/env bash
# Render cover/cover.html to output/<slug>_封面_3x4.png + .jpg
# Usage: render_cover.sh <project> [slug]
set -euo pipefail

PROJECT="${1:-.}"
PROJECT="$(cd "$PROJECT" && pwd)"
SLUG="${2:-$(basename "$PROJECT")}"
OM="${OM:-}"
if [[ -z "$OM" || ! -x "$OM" ]]; then
  if command -v om >/dev/null 2>&1; then
    OM="$(command -v om)"
  elif [[ -x "$HOME/Desktop/自媒体/omx" ]]; then
    OM="$HOME/Desktop/自媒体/omx"
  elif [[ -x "$HOME/.agents/skills/huashu-motion/bin/om" ]]; then
    OM="$HOME/.agents/skills/huashu-motion/bin/om"
  else
    echo "error: om not found. Install huashu-motion or set OM=/path/to/om." >&2
    exit 1
  fi
fi
if [[ ! -f "$PROJECT/cover/cover.html" ]]; then
  echo "error: $PROJECT/cover/cover.html not found" >&2
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$PROJECT"
"$OM" still cover/cover.html --at 0 --out "$TMP/cover"
mkdir -p output
cp "$TMP/cover" "output/${SLUG}_封面_3x4.png"
ffmpeg -hide_banner -loglevel error -y -i "$TMP/cover" -q:v 2 "output/${SLUG}_封面_3x4.jpg"
echo "cover: $PROJECT/output/${SLUG}_封面_3x4.png"
echo "cover: $PROJECT/output/${SLUG}_封面_3x4.jpg"

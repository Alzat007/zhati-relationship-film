#!/usr/bin/env bash
# Check structure, QA the newest render, probe, decode and measure loudness.
# Usage: verify.sh <project> [video]
set -uo pipefail

PROJECT="${1:-.}"
PROJECT="$(cd "$PROJECT" && pwd)"
VIDEO="${2:-}"
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

echo "== structure =="
"$OM" check "$PROJECT" --samples 6
CHECK_STATUS=$?

if [[ -z "$VIDEO" ]]; then
  VIDEO="$(ls -t "$PROJECT"/out/*.mp4 2>/dev/null | head -1 || true)"
fi
if [[ -z "$VIDEO" || ! -f "$VIDEO" ]]; then
  echo "error: no rendered mp4 in $PROJECT/out" >&2
  exit 1
fi

echo "== qa: $VIDEO =="
"$OM" qa "$VIDEO"

echo "== probe =="
ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels \
  -of default=noprint_wrappers=1 "$VIDEO"

echo "== decode =="
decode_out="$(ffmpeg -v error -i "$VIDEO" -f null - 2>&1 || true)"
if [[ -n "$decode_out" ]]; then
  echo "decode reported errors:"
  printf "%s\n" "$decode_out" | head -5
else
  echo "decode ok"
fi

echo "== loudness =="
ffmpeg -hide_banner -nostats -i "$VIDEO" -af ebur128=peak=true -f null - 2>&1 | tail -8

echo
echo "Manual gates still required: scene-boundary stills, text collision, ending, cold review."
exit "$CHECK_STATUS"

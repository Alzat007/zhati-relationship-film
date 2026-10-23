#!/usr/bin/env bash
# Render a custom-audio episode. Uses --silent so om does not rebuild the audio.
# Usage: render.sh <project> [workers]
set -euo pipefail

PROJECT="${1:-.}"
WORKERS="${2:-4}"
PROJECT="$(cd "$PROJECT" && pwd)"

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

cd "$PROJECT"
"$OM" render . --silent --fps 30 --workers "$WORKERS" --video extract
latest="$(ls -t out/*.mp4 2>/dev/null | head -1 || true)"
[[ -n "$latest" ]] && echo "rendered: $PROJECT/$latest"

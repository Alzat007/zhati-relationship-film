#!/usr/bin/env bash
# Pad film clips to integer frames and refresh stills.
# Use after replacing assets/movies/movie_*.mp4 with new source clips.
# Usage: prepare_media.sh <project> [--stills-only]
set -euo pipefail

PROJECT="${1:-.}"
PROJECT="$(cd "$PROJECT" && pwd)"
STILLS_ONLY="${2:-}"
MOV="$PROJECT/assets/movies"
STILL="$PROJECT/assets/stills"
mkdir -p "$MOV" "$STILL"

if [[ "$STILLS_ONLY" != "--stills-only" ]]; then
  shopt -s nullglob
  for f in "$MOV"/movie_*.mp4; do
    base="$(basename "$f")"
    mkdir -p "$MOV/_orig"
    if [[ ! -f "$MOV/_orig/$base" ]]; then
      cp "$f" "$MOV/_orig/$base"
    fi
    src="$MOV/_orig/$base"
    echo "padding $base from $src"
    ffmpeg -hide_banner -loglevel error -y -i "$src" \
      -vf "tpad=stop_mode=clone:stop_duration=0.08" -r 24 -vsync cfr \
      -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -an "$f"
    ffprobe -v error -count_frames -select_streams v:0 \
      -show_entries stream=nb_read_frames,avg_frame_rate,duration \
      -of default=noprint_wrappers=1 "$f"
  done
  shopt -u nullglob
fi

# Default still times assume the master 7th Heaven clips. Adjust for a new film.
extract () {
  local clip="$1" t="$2" out="$3"
  [[ -f "$MOV/$clip" ]] || return 0
  ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$MOV/$clip" \
    -frames:v 1 -q:v 2 "$STILL/$out"
  echo "still: $out @ ${t}s from $clip"
}
extract movie_02.mp4 2.4 man.jpg
extract movie_02.mp4 7.2 woman.jpg
extract movie_03.mp4 4.0 couple.jpg
extract movie_01.mp4 3.0 room.jpg
extract movie_03.mp4 8.5 hands.jpg

echo "portraits:"
for p in "$PROJECT"/assets/portraits/*.jpg; do
  [[ -f "$p" ]] && echo "  $(basename "$p") $(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$p")"
done

echo "done. Review stills and update object-position / still choices if the new film differs."

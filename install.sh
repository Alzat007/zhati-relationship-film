#!/usr/bin/env bash
# Install this repo as a DSH/Codex skill by symlinking it into ~/.agents/skills.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${HOME}/.agents/skills/zhati-relationship-film"
mkdir -p "$(dirname "$DEST")"

if [[ -L "$DEST" ]]; then
  current="$(readlink "$DEST")"
  if [[ "$current" == "$SRC" ]]; then
    echo "already installed: $DEST -> $SRC"
    exit 0
  fi
  echo "replacing existing symlink: $DEST -> $current"
  rm "$DEST"
elif [[ -e "$DEST" ]]; then
  echo "error: $DEST exists and is not a symlink." >&2
  echo "Move it aside, then rerun ./install.sh" >&2
  exit 1
fi

ln -s "$SRC" "$DEST"
echo "installed: $DEST -> $SRC"
echo "next: $DEST/scripts/new_episode.sh my-episode --ref /path/to/your/master --base \"$HOME/relationship-films\""

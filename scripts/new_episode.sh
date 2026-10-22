#!/usr/bin/env bash
# Create a new episode project from the master film.
# Usage: new_episode.sh <slug> [--ref /path/to/master] [--no-assets]
set -euo pipefail

BASE_DIR="${BASE_DIR:-$HOME/relationship-films}"
REF="${REF:-$BASE_DIR/good-people-wrong-person}"
REF_EXPLICIT=0
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="${1:-}"

if [[ -z "$SLUG" ]]; then
  echo "usage: $0 <slug> [--ref /path/to/master] [--base /path/to/workspace] [--no-assets]" >&2
  exit 2
fi
shift

WITH_ASSETS=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --ref) REF="$2"; REF_EXPLICIT=1; shift 2 ;;
    --base) BASE_DIR="$2"; [[ "$REF_EXPLICIT" -eq 1 ]] || REF="$BASE_DIR/good-people-wrong-person"; shift 2 ;;
    --no-assets) WITH_ASSETS=0; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ "$SLUG" == *"/"* || "$SLUG" == ".." || "$SLUG" == "." ]]; then
  echo "slug must not contain '/', '.' or '..'" >&2
  exit 2
fi

TARGET="$BASE_DIR/$SLUG"
if [[ -e "$TARGET" ]]; then
  echo "target already exists: $TARGET" >&2
  exit 1
fi

# Validate the master before creating anything, so a bad path does not leave a half-project.
if [[ ! -d "$REF/vendor" ]]; then
  echo "error: vendor/ not found at $REF; pass --ref /path/to/master or copy vendor/ manually." >&2
  exit 1
fi
if [[ "$WITH_ASSETS" -eq 1 && ! -d "$REF/assets" ]]; then
  echo "error: master assets/ not found at $REF; pass --ref /path/to/master or use --no-assets." >&2
  exit 1
fi

mkdir -p "$TARGET"/{assets/{movies,stills,portraits,fonts,textures},cover,vendor,out,output}

# Code: prefer the master project, fall back to the skill's template.
if [[ -f "$REF/index.html" ]]; then
  cp "$REF/index.html" "$TARGET/index.html"
else
  cp "$SKILL_DIR/templates/index.template.html" "$TARGET/index.html"
  echo "warning: master index.html not found at $REF; used skill template" >&2
fi

if [[ -f "$REF/cover/cover.html" ]]; then
  cp "$REF/cover/cover.html" "$TARGET/cover/cover.html"
else
  cp "$SKILL_DIR/templates/cover-3x4.template.html" "$TARGET/cover/cover.html"
fi

if [[ -d "$REF/vendor" ]]; then
  cp -R "$REF/vendor/." "$TARGET/vendor/"
else
  echo "error: vendor/ not found at $REF; copy a huashu-motion vendor/ folder into $TARGET/vendor/" >&2
  exit 1
fi

if [[ "$WITH_ASSETS" -eq 1 ]]; then
  if [[ ! -d "$REF/assets" ]]; then
    echo "error: master assets/ not found at $REF" >&2
    exit 1
  fi
  for d in movies stills portraits fonts textures; do
    if [[ -d "$REF/assets/$d" ]]; then
      cp -R "$REF/assets/$d/." "$TARGET/assets/$d/"
    fi
  done
  # Do not copy assets/movies/_orig; keep the project lean.
  rm -rf "$TARGET/assets/movies/_orig"

  if [[ -f "$REF/assets/score.wav" ]]; then
    cp "$REF/assets/score.wav" "$TARGET/assets/score.wav"
    echo "warning: copied master score.wav as a PLACEHOLDER. Replace it with the new episode's mix before rendering." >&2
  else
    ffmpeg -hide_banner -loglevel error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t 1 -c:a pcm_s24le "$TARGET/assets/score.wav"
    echo "warning: no master score.wav; created 1s silence. Replace with the new episode mix." >&2
  fi
else
  echo "warning: --no-assets; add assets/movies, stills, portraits, fonts, textures and score.wav before rendering." >&2
fi

# Docs / placeholders.
cp "$SKILL_DIR/templates/episode-brief.template.md" "$TARGET/BRIEF.md"
cp "$SKILL_DIR/templates/treatment.template.md" "$TARGET/treatment.md"
cp "$SKILL_DIR/templates/sources.template.md" "$TARGET/素材来源.md"
cp "$SKILL_DIR/templates/publish-copy.template.md" "$TARGET/发布文案.md"

cat > "$TARGET/文稿.txt" <<'TXT'
# 把新一期旁白粘贴到这里；一段一行，方便生成字幕。
TXT

: > "$TARGET/字幕.srt"

cat > "$TARGET/README.md" <<MD
# $SLUG

从母版《好人与错的人》复制的新一期工程。

## 先做

1. 填 \`BRIEF.md\`，把新主题、平台、时长、声音、片源定下来。
2. 写 \`文稿.txt\`，再生成新旁白和逐句时间。
3. 读 skill 的 \`references/text-slots.md\`，逐项替换 \`index.html\` 的旧文案。
4. 读 \`references/retiming.md\`，按新旁白重排时间轴。
5. 替换 \`assets/score.wav\`；当前是母版占位音轨。
6. 渲染前跑 \`om check . --samples 6\`。

## 母版

- 工程：\`$REF\`
- 模板：\`$SKILL_DIR/templates\`
- 说明：\`$SKILL_DIR/SKILL.md\`

## 交付

- \`output/<slug>_1080p_30fps.mp4\`
- \`output/<slug>_字幕.srt\`
- \`output/<slug>_封面_3x4.png\`
- \`output/<slug>_发布文案.md\`
- \`output/素材来源.md\`
MD

echo "created: $TARGET"
echo "next: fill BRIEF.md / 文稿.txt, then read:"
echo "  $SKILL_DIR/references/text-slots.md"
echo "  $SKILL_DIR/references/retiming.md"
echo "  $SKILL_DIR/references/rights-and-ethics.md"
echo "replace assets/score.wav before final render."

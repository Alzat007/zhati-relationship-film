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

mkdir -p "$TARGET"/{assets/{movies,stills,portraits,fonts,textures,imported},cover,vendor,out,output}

# Code: always use the skill's latest template, not the master's old composition.
# The master is an asset/reference source; the template is the code.
cp "$SKILL_DIR/templates/index.template.html" "$TARGET/index.html"
cp "$SKILL_DIR/templates/cover-3x4.template.html" "$TARGET/cover/cover.html"

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
cp "$SKILL_DIR/templates/assets.manifest.example.json" "$TARGET/assets.manifest.json"

# Operator scripts the project README refers to. new_episode.sh stays in the skill.
mkdir -p "$TARGET/scripts"
for f in prepare_media.sh render.sh render_cover.sh verify.sh asset_report.py stock_search.py fetch_stock.py cues_to_srt.py replace_cues.py retime_scene.py; do
  cp "$SKILL_DIR/scripts/$f" "$TARGET/scripts/$f"
done
chmod +x "$TARGET"/scripts/*.sh "$TARGET"/scripts/*.py

cat > "$TARGET/文稿.txt" <<'TXT'
# 把新一期旁白粘贴到这里；一段一行，方便生成字幕。
TXT

: > "$TARGET/字幕.srt"

cat > "$TARGET/README.md" <<MD
# $SLUG

从母版《好人与错的人》复制的新一期工程。

## 先做

1. 填 \`BRIEF.md\`：客户、平台、时长、素材模式、权利、声音。
2. 写 \`文稿.txt\`，再生成新旁白和逐句时间。
3. 读 \`references/text-slots.md\`，逐项替换 \`index.html\` 的旧文案。
4. 读 \`references/asset-strategy.md\`：客户素材放进 \`assets/imported/\`；没有就用 \`scripts/stock_search.py\` 搜 3 个候选，确认后用 \`scripts/fetch_stock.py\` 下载/标准化；填 \`assets.manifest.json\`，改 \`data-asset-slot\` 的 \`src\`，重算视频窗口。
5. 读 \`references/retiming.md\`，按新旁白重排时间轴。
6. 替换 \`assets/score.wav\`；当前是母版占位音轨。
7. 渲染前跑 \`python3 scripts/asset_report.py --manifest assets.manifest.json --project .\` 和 \`om check . --samples 6\`。

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
echo "fill assets.manifest.json and run: python3 scripts/asset_report.py --manifest assets.manifest.json --project ."
echo "the master assets are a starter kit; replace them per client brief."

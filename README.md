# zhati-relationship-film

一个可复用的 **AI 视频 skill / 工作流**：把一段中文关系随笔，做成 3 分钟电影感影像——公版经典电影片段做底，雨伞、雨、胶片颗粒做视觉脊柱，宋体大字 + 哲学家肖像 + 克制旁白 + 3:4 封面。

A reusable agent skill for 3-minute Chinese relationship video essays: public-domain classic film, umbrella/rain/film-grain visual spine, philosopher portraits, kinetic Chinese type and a 3:4 cover. Built for [huashu-motion](https://github.com/alchaincyf/huashu-motion) workflows.

![demo cover](docs/demo-cover.jpg)

> Demo cover from the original episode. The code is MIT; the sample narration/cover text is © the author and not licensed for reuse — replace it with your own script. See [NOTICE.md](NOTICE.md).

## 这是什么

不是“一键生成视频”的应用，而是一套给 AI agent 的 **skill + 模板 + 脚本**：

- **SKILL.md**：9 步生产流水线、硬门、完整工作方式。
- **references/**：16 拍结构、视觉系统、逐项文本槽、时间轴重排、版权/伦理、发布文案。
- **templates/**：母版 HTML 合成 + 1080×1440 的 3:4 封面 + Brief/Treatment/来源模板。
- **scripts/**：建新工程、替换 cues、生成 SRT、重排场景时间、渲染、出封面、验收。
- **workflow.md**：一页 checklist。

默认输出：

| 项 | 默认 |
|---|---|
| 正片 | 1920×1080 / 30fps / 2:40–3:40 |
| 画幅 | 16:9 正片 + 3:4 封面（1080×1440） |
| 语言 | 中文旁白 + 烧录字幕 + `.srt` |
| 声音 | 旁白 + 原创配乐 + 雨声，约 −15 LUFS，真峰值 ≤ −1.5 dBFS |
| 交付 | MP4 / SRT / 封面 PNG+JPG / 发布文案 / 来源记录 / 可编辑工程 |

## 安装

```sh
git clone https://github.com/Alzat007/zhati-relationship-film.git
cd zhati-relationship-film
./install.sh
```

`install.sh` 会把仓库软链到 `~/.agents/skills/zhati-relationship-film`，让支持 skill 的 agent 自动发现它。

## 需要什么

- **huashu-motion**：提供 `om`、Chrome 渲染、studio。仓库不包含 `vendor/`，需要从 huashu-motion 工程复制。
- **ffmpeg / ffprobe**。
- **Chrome / Chromium**（`om` 会调用）。
- 一个 **master 工程**：包含 `vendor/`、电影片段、肖像、字体、纹理和一条占位音轨。仓库只提供模板，不包含这些资产（体积/权利原因）。
- 可选：本地声音克隆（例如 `macos-local-voice` skill）来做本人声线。

## 快速开始

```sh
# 1. 建新一期（--ref 指向你的 master 工程）
~/.agents/skills/zhati-relationship-film/bin/new-episode my-episode \
  --base "$HOME/relationship-films" \
  --ref "$HOME/relationship-films/master"

# 2. 填 Brief 和文稿
cd "$HOME/relationship-films/my-episode"
$EDITOR BRIEF.md 文稿.txt

# 3. 生成新旁白 + cues.json（这一步不在本仓库内；用你的本地声音管线）
# 4. 换文案 / 重排时间 / 换音轨
#    读 references/text-slots.md 和 references/retiming.md

# 5. 检查 + 渲染
om check . --samples 6
om render . --silent --fps 30 --workers 4 --video extract

# 6. 验收 + 3:4 封面
scripts/verify.sh .
scripts/render_cover.sh .
```

第一次没有 master 工程时：

1. 安装 huashu-motion，新建一个空工程。
2. 复制 `templates/index.template.html` 为 `index.html`，`templates/cover-3x4.template.html` 为 `cover/cover.html`。
3. 从 huashu-motion 工程复制 `vendor/`。
4. 按 `references/rights-and-ethics.md` 放入公版电影片段、肖像、字体、纹理和一条 `assets/score.wav` 占位音轨。
5. 把这个工程作为 `--ref`。

## 工作流（一页版）

1. 读 `SKILL.md` + `references/beat-sheet.md`，把主题放进 16 拍。
2. 写 950–1150 字旁白，保留“一种理解角度”“不是对所有人的解释”“责任不能替对方开脱”等限定。
3. 生成新旁白 + `cues.json`。**不要复用模板里的旧旁白。**
4. 建工程，按 `references/text-slots.md` 换掉每一处文案。
5. 按 `references/retiming.md` 重排场景/视频窗口/字幕。
6. 替换 `assets/score.wav`，生成 SRT。
7. `om check` + `om still` 逐场景检查。
8. `om render`（1080p/30fps 约 25–35 分钟）。
9. 独立冷审，修 MUST-FIX。
10. 3:4 封面 + 发布文案 + `output/` 交付。

完整说明见 [SKILL.md](SKILL.md)，可打印的 checklist 见 [workflow.md](workflow.md)。

## 仓库结构

```
SKILL.md                      agent 主说明 + 9 步流水线
workflow.md                   一页 checklist
README.md                     本文件
LICENSE                       MIT（代码/脚本/文档）
NOTICE.md                     示例文案、电影、肖像、字体、声音的权利说明
install.sh                    安装为 skill
bin/new-episode               建新一期
docs/demo-cover.jpg           演示封面
examples/cues.example.json    字幕/时间轴输入示例
references/
  beat-sheet.md               16 拍结构
  visual-system.md            色板/字体/伞/雨/声音/封面
  text-slots.md               逐项替换清单
  retiming.md                 新旁白的时间轴重排
  rights-and-ethics.md        片源/肖像/声音/伦理
  publishing.md               标题/文案/标签
templates/
  index.template.html         母版 16:9 合成
  cover-3x4.template.html     3:4 封面
  episode-brief.template.md
  treatment.template.md
  publish-copy.template.md
  sources.template.md
scripts/
  new_episode.sh
  prepare_media.sh
  replace_cues.py
  cues_to_srt.py
  retime_scene.py
  render.sh
  render_cover.sh
  verify.sh
```

## 不包含什么

为了体积和权利清晰，仓库**不包含**：

- 电影片段、肖像、字体、纹理等二进制素材；
- 旁白、配乐、雨声、声音克隆；
- 原成片 MP4、母版工程、`vendor/`；
- 示例视频的完整旁白授权（示例文案仅作结构参考，不可直接复用）。

## 许可证

- **代码、脚本、模板、文档**：MIT，见 [LICENSE](LICENSE)。
- **示例旁白/标题/封面文字/演示封面**：© 2026 Alzat007，保留所有权利，不在 MIT 范围内；复用前请换成你自己的文案。见 [NOTICE.md](NOTICE.md)。
- **电影**：*7th Heaven* (1927)，美国公版；页面同时把中国列为公版，但欧盟/英国等地区期限不同。片段未随仓库分发；使用前按发布地区复核。
- **肖像**：Freud / Aristotle / Kant 的参考图均为 Wikimedia Commons 公版；未随仓库分发。
- **字体**：未分发；模板使用 macOS 系统字体（Songti SC / PingFang SC）与本地授权 webfont，请勿再分发系统字体。

## 致谢

- 视觉/渲染基础：[huashu-motion](https://github.com/alchaincyf/huashu-motion)（花叔）。
- 参考影片：*7th Heaven* (1927)，Frank Borzage。
- 参考肖像：Max Halberstadt（Freud）、Jastrow（Aristotle bust）、佚名（Kant）。

---

如果这套模板帮到你，欢迎在 Issues 里贴出你做的某一期，或提 PR 改进 16 拍结构、封面和文案模板。

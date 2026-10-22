---
name: zhati-relationship-film
description: "生成扎提风格的 3 分钟中文男女关系/爱情影像随笔：公版经典电影片段做底、雨伞/雨/胶片视觉脊柱、哲学家肖像与宋体动效、3:4 封面。Use when the user asks for a relationship/love essay video, a new episode in the style of 《好人与错的人》, or a 3-minute emotional film with classic film clips."
metadata:
  author: "zhati"
  version: "1.0.0"
  based_on: "good-people-wrong-person · 2026-10-22"
---

# 扎提·关系影像随笔

这是从成片《为什么有些好人，会和错的人交往？》提炼出来的可复用工作流。目标不是复刻同一篇文案，而是让新一期保持同一套**视觉 DNA**：

> 老电影放映机里的一场雨 + 一把始终倾向对方的伞 + 宋体大字 + 哲学家肖像 + 克制的旁白。

## 先判断是否适用

适用：
- 男女关系、爱情、亲密关系、边界、自我价值、付出与回报、分手与复合等中文情感议题。
- 用户想要 2:40–3:40 的横屏影像随笔，有旁白、有字幕、有电影感。
- 用户明确说“按《好人与错的人》那个风格”“用之前那个模板”“做成系列”。

不适用：
- 产品发布片、带货片、快节奏混剪、纯口播视频。
- 用户要求使用《卡萨布兰卡》《花样年华》等仍受版权保护的片段，且没有授权。先说明风险，改用公版片或让用户提供授权素材。
- 用户想要 9:16 竖屏正片。本模板是 16:9 正片 + 3:4 封面；竖屏需要重新做布局，不能直接裁。

## 成片规格（默认）

| 项 | 默认 |
|---|---|
| 正片 | 1920×1080 / 30fps / 2:40–3:40 |
| 画幅 | 16:9 |
| 语言 | 简体中文旁白 + 烧录字幕 + SRT |
| 封面 | 1080×1440（3:4），PNG + JPG |
| 声音 | 旁白 + 原创配乐 + 雨声，约 −15 LUFS，真峰值 ≤ −1.5 dBFS |
| 字幕 | 烧录在画面内，另出 `.srt` |
| 交付 | MP4、SRT、3:4 封面、发布文案、素材来源、可编辑工程 |

## 母版位置

参考母版（不随仓库分发）：

- 本机开发时：`~/Desktop/自媒体/good-people-wrong-person`
- 其他机器：用 `--ref` 指向你自己的母版工程

母版包含：
- `index.html`：201.37 秒成片的完整 huashu-motion 合成。
- `cover/cover.html`：1080×1440 的 3:4 封面源文件。
- `assets/movies/`：已核验、已去音轨、已补到整数帧的《第七天堂》(1927) 片段。
- `assets/portraits/`：弗洛伊德、亚里士多德、康德公版肖像。
- `assets/stills/`、`assets/textures/`、`assets/fonts/`、`vendor/`。
- `assets/score.wav`：上一期的旁白＋配乐＋雨声成品混音。**新一期必须替换，不能直接沿用。**
- `output/`：上一期交付物，仅作参考，不要原样复制。

如果母版不在了：用 `templates/index.template.html` 和 `templates/cover-3x4.template.html` 恢复代码；电影片段和肖像需要重新按 `references/rights-and-ethics.md` 获取并核验。

## 新一期怎么开始

```sh
SKILL="$HOME/.agents/skills/zhati-relationship-film"
$SKILL/scripts/new_episode.sh my-episode-slug --base "$HOME/relationship-films"
```

脚本会：
1. 在 `$BASE_DIR/my-episode-slug` 建新工程（默认 `$HOME/relationship-films`，可用 `--base` 改）；
2. 复制母版的 `index.html`、`cover/cover.html`、`vendor/`、电影片段、静帧、肖像、字体、纹理；
3. 复制母版 `assets/score.wav` 作为**占位音轨**（页面能先跑起来）；
4. 生成 `BRIEF.md`、`文稿.txt`、`字幕.srt`、`treatment.md`、`素材来源.md`、`发布文案.md` 的空模板；
5. 打印下一步和需要替换的文本槽。

然后按下面的流水线做。**不要跳过写新旁白和新字幕这一步。**

## 流水线

### 0. 读需求，锁结构

先读 `references/beat-sheet.md`，把新主题放进 16 个叙事节拍里。不要先写满 3 分钟再硬塞画面；先定“钩子—具体故事—概念区分—哲学/心理视角—伦理转折—自省—行动—收束”。

默认结构：
1. 钩子（一个问题）
2. 具体故事（雨/伞；可以换成别的具体物，但必须有一个物贯穿）
3. “这是一个虚构的故事”类限定
4. 两个概念的区分（善良 vs 合适，或本期对应的一对概念）
5. 哲学视角 A（友爱/相互性/尊重等）
6. 一个人的局限（“一个人的付出无法独自完成两个人的关系”类）
7. 情绪转折问题（为什么难过还期待下一次）
8. 心理视角（重复/模式；用“一种理解角度”，不做诊断）
9. 模式识别（努力换取认可）
10. 冷淡与自我怀疑
11. 伦理转折（伤害不是你招来的；责任在伤害者）
12. 限定与例外（欺骗、改变、相处后才看见）
13. 自省（两个问题；镜面/倒影）
14. 哲学视角 B（自我尊重）
15. 一句很小的话（可执行的动作）
16. 练习与收束（保留温柔，也给自己留位置）
17. 片尾字幕/来源

如果新主题不需要两位哲学家，可以只保留一位；如果不需要心理视角，可以把 8–9 压成一段。**不要为了凑结构编造引语或诊断。**

### 1. 写新旁白

- 目标 950–1150 个汉字，正常语速约 3 分钟；如果用户给了文稿，先做“删到能呼吸”的编辑，不要改立场。
- 保留限制性表述：一种理解角度 / 不是对所有人的解释 / 伤害的责任不能替对方开脱。
- 结尾要有一句可被记住的“小动作”或“小句子”，例如“我也冷，我也需要这把伞”。
- 写入 `文稿.txt`，一段一行，方便生成字幕。

### 2. 生成新旁白和新时间轴

优先使用用户自己的本地声音克隆（见 `macos-local-voice` skill），不要上传参考录音。没有可用声音时，明确问用户：本人录音 / 本地克隆 / 系统音色 / 无声。

产出：
- 一条完整旁白 `assets/voice.wav`（48kHz，尽量 24-bit）；
- 逐句起止时间（JSON 或 CSV），精确到 0.01s；
- 一份新 `CUES` 数组（`[start, end, text]`）。

不要沿用母版的 194 秒旁白。母版的时间轴只用于理解节奏，不是新一期的音频。

### 3. 配乐与混音

- 保留“钢琴/弦乐/轻环境 + 雨声”的方向，不要用现成版权歌曲。
- 混音目标：旁白清楚，音乐在 −28～−32 LUFS 左右，整体约 −15 LUFS，真峰值 ≤ −1.5 dBFS。
- 输出 `assets/score.wav`，替换占位音轨；页面里的 `<audio id="score" ...>` 保留，但时长要改。
- 本模板用 `id="score"` 而不是 `om-sound`，所以渲染时要加 `--silent`，否则 `om render` 会尝试重建音轨。详见 `references/visual-system.md` 的“声音”一节。

### 4. 重新卡点

这是最容易被低估的一步。母版的所有时间都是硬编码的；新旁白一换，**每个场景都要重新对时**。

按 `references/beat-sheet.md` 的比例给 16 个场景分配新时长，然后：
- 先改 `CUES` 数组、根节点 `data-duration`、JS 里的 `DUR`、`<audio data-duration>`。
- 每个场景以“该段第一句旁白的起点”为锚，场景结束以下一段的第一句为界。
- 场景内部的动画时间按“新时长 / 旧时长”做比例缩放；不要只平移开头，否则后半段会漂。
- 视频窗口的 `data-start` / `data-duration` / `data-media-start` / `data-playback-rate` 也要重算；确保片段在淡出之前不会先播完。母版片段已经补到整数帧，但换了新片源要重新补帧。
- 每改完一个场景，用 `om still` 看 `start+0.5s`、`start+2s`、`end-0.5s`，确认没有旧文字残影、没有文字碰撞、没有空帧。

具体替换清单见 `references/text-slots.md`；卡点方法见 `references/retiming.md`。

### 5. 换文本，不要换视觉 DNA

必须逐项替换 `index.html` 里的文字槽（见 `references/text-slots.md`），包括：
- 片名变量 `filmTitle`、钩子两行；
- 雨伞故事的四段大字；
- “虚构故事”限定；
- 善良/合适两帧的标签；
- 亚里士多德/弗洛伊德/康德的段落与出处；
- 冷场、转折、责任、镜面、自省、行动、结尾、片尾字幕；
- `CUES` 里的每一句字幕。

保留：
- 色板、宋体/苹方/EB Garamond 的搭配；
- 胶片底、雨、伞、颗粒、暗角、闪白、酒红划线；
- 16:9 的左右留白和下方字幕带；
- “一镜一事件”的节奏，不要把所有字都塞进同一屏。

不要保留母版的旧文案。新一期如果出现“亚里士多德/弗洛伊德/康德”以外的思想家，必须重新核验出处，并在画面里标注“释义/应用”，不要伪造直接引语。

### 6. 换片源（可选）

母版用的是《第七天堂》(1927)。新一期可以：
- 继续用同一部公版片，保持系列感；
- 换另一部公版经典爱情片，按 `references/rights-and-ethics.md` 核验来源、去音轨、补帧、抽静帧；
- 用户提供已授权片段时，优先用用户的素材，保留片名/年份/“非真实案例”标识。

不要用《卡萨布兰卡》《罗马假日》《花样年华》等仍受版权保护的片段，除非用户提供明确授权。

### 7. 检查、渲染、审片

```sh
cd "$HOME/relationship-films/my-episode-slug"
om check . --samples 6
om render . --silent --fps 30 --workers 4 --video extract
om qa out/<new-file>.mp4
```

渲染约 25–35 分钟（1080p/30fps/4 workers，201 秒量级）。不要用 720p 冒充 1080p。

如果本机的 `om` 是包装脚本（例如设置了 Node/Chrome 环境），把 `OM` 指向它；`scripts/` 会依次尝试 `$OM`、`om`、`~/.agents/skills/huashu-motion/bin/om`。

必过：
- `om check` 0 errors；
- `om qa` 无单帧跳变；
- 抽帧检查：钩子、每个场景边界、转折、弗洛伊德、结尾、片尾字幕；
- 独立冷审（找一位没参与制作的 agent 只看成片），至少修掉 MUST-FIX；
- `ffprobe` 确认 1920×1080/30fps/正确时长/AAC 48kHz 立体声；
- 全片解码无错误；响度/峰值达标。

### 8. 封面和发布文案

- 封面：复制 `cover/cover.html`，替换标题、时长、底部钩子、来源；渲染 1080×1440 PNG + JPG。模板的布局：顶部小标 + 大标题（“错的人”用琥珀色）+ 中部伞/两个人 + 底部一句金句 + 来源。
- 发布文案：按 `references/publishing.md` 出长版/短版/B站版/置顶评论/标签；不要直接复用上一期的文案。
- 片尾字幕和角标保留“电影画面，非真实案例”“解释视角，不是诊断”等必要限定。

### 9. 交付

```sh
my-episode-slug/output/
  <slug>_1080p_30fps.mp4
  <slug>_字幕.srt
  <slug>_封面_3x4.png
  <slug>_封面_3x4.jpg
  <slug>_发布文案.md
  素材来源.md
  项目说明.md
```

## 硬门（不过不交付）

1. **新旁白**：新一期必须有新录/新生成的旁白；不能拿母版 194 秒音频对上新字幕。
2. **新文本**：`index.html` 中不能残留母版的成句文案；用 `references/text-slots.md` 逐项过。
3. **版权**：电影片段、肖像、音乐、声音都有来源记录；片名/年份/非真实案例标识在画面里。
4. **伦理**：不诊断、不责怪受害者、不伪造哲学家原话、不把电影角色当真实案例。
5. **画面**：没有文字被裁、没有单字孤行、没有文字压字幕、结尾两个人都在伞下（如果本期仍用伞的隐喻）。
6. **声音**：旁白清楚、无削波、无意外静音；`--silent` 渲染保留自定义音轨。
7. **审片**：独立冷审的 MUST-FIX 已修，或明确记录为什么保留。

## 不要做

- 不要把母版的旧文案、旧字幕、旧旁白直接复用。
- 不要把所有场景都改成同一张图 + 同一段字；母版的场景语法是有变化的。
- 不要用蓝紫渐变、霓虹、AI 味星空底。
- 不要在 3:4 封面里直接裁 16:9 正片；用 `cover/cover.html` 重新排。
- 不要把哲学家的话写成“名言”并加引号；用“他讨论过/一种理解角度”。
- 不要用“吸渣体质”“恋爱脑”这类诊断式标签做标题；用问题，不用判决。

## 文件地图

- `references/beat-sheet.md`：16 拍结构、比例、画面事件、文案功能。
- `references/visual-system.md`：色板、字体、镜头、伞/雨、声音、封面。
- `references/text-slots.md`：逐项替换清单。
- `references/retiming.md`：新旁白的时间轴重排方法。
- `references/rights-and-ethics.md`：片源/肖像/声音/伦理。
- `references/publishing.md`：标题、长文案、短文案、B站简介、置顶评论、标签。
- `templates/index.template.html`：母版合成。
- `templates/cover-3x4.template.html`：3:4 封面。
- `scripts/new_episode.sh`：建新工程。
- `scripts/prepare_media.sh`：补帧、抽静帧、检查片源。
- `scripts/render.sh`：带 `--silent` 的渲染封装。
- `scripts/render_cover.sh`：把 `cover/cover.html` 渲染成 1080×1440 PNG/JPG。
- `scripts/verify.sh`：check/qa/ffprobe/解码/响度。

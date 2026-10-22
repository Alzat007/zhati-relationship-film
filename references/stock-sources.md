# 背景视频：AI 自己找 stock

客户没有实拍、或需要雨/窗/街/手/门/车站等通用背景时，可以联网找免费 stock，下载、去音轨、标准化，再做动效。

**不要**从 YouTube、B 站、流媒体或版权电影里扒片段；不要绕过水印、付费墙、登录或地区限制。只用明确允许使用的免费/授权素材。

## 先搜，再下载

```sh
python3 scripts/stock_search.py "rain window" --limit 6
```

- **Mixkit**：不需要 key，直接解析搜索页的 JSON-LD；短英文 query 最稳（rain / window / hands / night street / train / coffee）。
- **Coverr**：搜索页是前端渲染，脚本的 `--source coverr` 是 best-effort；结果可能混入无关视频，必须人工看标题/缩略图/页面。更稳的是用页面 URL 手动确认。
- **Pexels / Pixabay**：需要免费 API key；设置 `PEXELS_API_KEY` / `PIXABAY_API_KEY` 后再跑 `--source auto`。不要把 key 写进仓库。
- **Wikimedia Commons**：适合公版/CC 影像；按文件页的授权和署名使用。
- **Internet Archive**：适合公版老片；确认具体文件的权利和版本。

搜索建议用英文：`rain window`、`rain umbrella`、`night street`、`hands coffee`、`empty chair`、`train platform`、`door`、`curtain`、`city rain`、`slow motion`。

## 选片标准

- 1920×1080 或更高；16:9；没有水印、台标、烧录字幕。
- 画面不要比字更抢：低对比、慢动作、浅景深、留白多。
- 如果大字压在画面上，避开人脸特写和复杂纹理；用雨/窗/街道/手/物件。
- 时长至少覆盖该段（建议 6–12 秒）；不需要原声。
- 同一期最多 2–3 个 stock 来源；统一调色。

## 下载 + 标准化 + 写 manifest

```sh
python3 scripts/fetch_stock.py \
  --url 'https://assets.mixkit.co/videos/2846/2846-1080.mp4' \
  --slug rain-window \
  --source Mixkit \
  --page 'https://mixkit.co/free-stock-video/rain/' \
  --license 'Mixkit License' \
  --credit 'Mixkit — Window on a rainy day' \
  --project . \
  --slot clip_01 \
  --scenes hook,umbrella \
  --max-duration 10
```

脚本会：
1. 下载到 `assets/imported/<slug>.mp4`（临时 `.source`，完成后删除）；
2. 去音轨，标准化 1920×1080 / 30fps / H.264；
3. 写 `assets/imported/<slug>.json`；
4. 更新 `assets.manifest.json` 的 slot。

然后：
- 改 `index.html` 里 `data-asset-slot="clip_01"` 的 `<video src=...>`；
- 用 `ffprobe` 重算 `data-start` / `data-duration` / `data-playback-rate`；
- 改 `#credit` / `#credits .cols` / `素材来源.md`；
- `python3 scripts/asset_report.py --manifest assets.manifest.json --project .`。

## 授权与 credit

| 来源 | 通常怎么用 | 必做 |
|---|---|---|
| Mixkit | 免费用于商业/个人项目；具体以当前 Mixkit License 为准 | 保存页面/许可；credit 写 “Mixkit — 标题”；不要转售/再分发为 stock |
| Coverr | 免费用于商业/非商业；Coverr+ 素材另有条款 | 保存页面/许可；credit 写 “Coverr — 标题”；不要转售 |
| Pexels | Pexels License；一般可商用、无需署名 | 保存页面/作者；不要转售/再分发为 stock |
| Pixabay | Pixabay Content License；一般可商用 | 保存页面/作者；不要转售 |
| Wikimedia Commons | 公版或 CC；逐文件看 | 按文件要求署名/相同方式共享 |
| Internet Archive | 公版/授权状态逐片看 | 标片名/年份/来源；确认具体版本 |

**不要**把 stock 说成客户实拍，也不要把有署名的 CC 素材去掉署名。客户项目要确认 license 覆盖客户的平台、地区、投放时长；拿不准就问客户/换素材。

## 客户确认

默认给客户 3 个候选（缩略图 + 页面 + license + 建议 slot），客户确认后再下载。
如果客户说“你定”，自动选第一个，但在交付里附来源和 license；不要静默使用。

## 常见坑

- 搜索页返回一堆无关视频：看标题/页面，不要只看 CDN 链接。
- 1080p 链接其实是 720p：`ffprobe` 确认；不够就换。
- 下载文件很大：`fetch_stock.py` 默认最多 300MB、最长 12 秒；不够就换更短的片段。
- 竖屏素材：`--fit contain` 加黑边，或当卡片用，不要硬拉成 16:9。
- 版权片/电影混剪：不要用；公版电影按 `rights-and-ethics.md` 走。

# Changelog

## v1.2.1 — 2026-10-23

- 修正 `om` 解析顺序：优先本机 `omx` 包装脚本，再回退到 huashu-motion 的裸 `bin/om`，避免在没有 Node 环境时 `render.sh` / `render_cover.sh` / `verify.sh` 失败。
- 已在 1080p stock 版成片与 3:4 封面上验证。

## v1.2.0 — 2026-10-22

- AI 可联网搜索免费背景视频：新增 `references/stock-sources.md`、`scripts/stock_search.py`、`scripts/fetch_stock.py`。
- 支持 Mixkit（无需 key）、Coverr（手动/直链）、Pexels/Pixabay（API key）、Wikimedia Commons/Internet Archive（公版/CC）。
- `fetch_stock.py` 自动下载、去音轨、标准化 1920×1080/30fps、写 metadata 并更新 `assets.manifest.json`。
- README/SKILL/asset-strategy/client-brief/rights/workflow 同步补充 stock 搜索、候选确认、license/credit 和“不扒版权片”的边界。

## v1.1.0 — 2026-10-22

- **素材/内容不再绑定单一电影**：支持客户实拍、公版电影、授权 stock、照片·档案、纯文字和混合。
- 新增 `references/client-brief.md`：客户问题清单、内容矩阵、三个确认点。
- 新增 `references/asset-strategy.md`：素材模式、多源统一、素材槽、manifest、隐喻替换。
- 新增 `templates/assets.manifest.example.json` 和 `scripts/asset_report.py`。
- 模板加入 `data-asset-slot`（clip_01–11、mirror_clip、still_*、portrait_*、cover_bg）。
- 脚手架改为“最新模板代码 + master 起始素材”，不再直接复制 master 的旧合成。
- README、SKILL、workflow、brief/treatment/sources 模板同步更新。
- 伦理/版权部分增加客户素材、stock、多来源 credit。

## v1.0.0 — 2026-10-22

- 首个公开版本：16 拍结构、huashu-motion 模板、3:4 封面、脚本与发布文案模板。

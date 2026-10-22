# 新一期工作流（一页版）

## 输入

- 客户 brief：受众、平台、时长、语气、必须用/不能用、权利
- 主题或客户文稿
- 素材模式：客户实拍 / 公版电影 / 授权 stock / 照片·档案 / 纯文字 / 混合
- 旁白方式：本人录音 / 本地克隆 / 系统音色 / 无声
- 本期“一句很小的话”

## 步骤

- [ ] 1. 读 `references/client-brief.md`，把客户要求压成 10 行内容计划。
- [ ] 2. 读 `SKILL.md` + `references/beat-sheet.md`，把主题放进 16 拍；素材模式先定。
- [ ] 3. 写 `文稿.txt`；目标 950–1150 字，保留限定。
- [ ] 4. 生成新旁白 + `cues.json`；不要用母版音频。
- [ ] 5. `bin/new-episode <slug>` 建工程；代码来自最新模板，母版只提供起始素材。
- [ ] 6. 按 `references/text-slots.md` 换掉所有旧文案。
- [ ] 7. 按 `references/asset-strategy.md` 换素材：放进 `assets/imported/`，填 `assets.manifest.json`，改 `data-asset-slot` 的 `src`；跑 `scripts/asset_report.py`。
- [ ] 8. 按 `references/retiming.md` 重排所有场景/视频窗口/字幕。
- [ ] 9. 替换 `assets/score.wav`；`scripts/cues_to_srt.py` 出 SRT。
- [ ] 10. `om check . --samples 6`；逐场景 `om still`；先给客户看钩子/封面静帧。
- [ ] 11. `scripts/render.sh . 4` 渲染（约 25–35 分钟）。
- [ ] 12. `scripts/verify.sh .`；独立冷审；修 MUST-FIX。
- [ ] 13. 改 `cover/cover.html`，跑 `scripts/render_cover.sh .` 出 1080×1440 PNG/JPG。
- [ ] 14. 按 `references/publishing.md` 写发布文案。
- [ ] 15. 整理 `output/`，交付。

## 四个最容易翻车的点

1. **旧音频**：`assets/score.wav` 还是母版的 201 秒。必须替换，否则新字幕会对不上嘴。
2. **旧时间**：`index.html` 里的场景时间是硬编码的。必须按新 `cues.json` 重排，不能只换字。
3. **旧素材**：母版的《第七天堂》/三位思想家只是 starter kit。客户不需要就换；每换一个来源，改 `src` + 窗口 + credit + `素材来源.md`。
4. **旧文案残留**：跑 `grep` 检查母版签名句；特别是封面、片尾、SRT。

## 交付前最后一眼

- 钩子前 3 秒有没有动/有问题？
- 60 秒附近的长句有没有单字孤行？
- 如果本期有思想家/专家：有没有“解释视角，不是诊断”？
- 1'40" 的转折有没有真的把“不是你的错”说清楚？
- 如果本期仍用伞的隐喻：结尾两个人是不是都在伞下？如果换隐喻，结尾物有没有落到两个人/关系上？
- 客户素材的权利/credit 有没有写？多来源有没有逐源标注？
- 片尾来源/免责能不能在 7 秒内读完？
- 3:4 封面缩小到手机大小，标题还认得出吗？

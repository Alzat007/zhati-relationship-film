# 新一期工作流（一页版）

## 输入

- 主题或用户文稿
- 目标平台 / 时长
- 旁白方式（本人录音 / 本地克隆 / 系统音色）
- 片源（继续母版 / 新公版片 / 用户授权片段）
- 本期“一句很小的话”

## 步骤

- [ ] 1. 读 `SKILL.md` 和 `references/beat-sheet.md`，把主题放进 16 拍。
- [ ] 2. 写 `文稿.txt`；目标 950–1150 字，保留限定。
- [ ] 3. 生成新旁白 + `cues.json`；不要用母版音频。
- [ ] 4. `scripts/new_episode.sh <slug>` 建工程。
- [ ] 5. 按 `references/text-slots.md` 换掉所有旧文案。
- [ ] 6. 按 `references/retiming.md` 重排所有场景/视频窗口/字幕。
- [ ] 7. 替换 `assets/score.wav`；`scripts/cues_to_srt.py` 出 SRT。
- [ ] 8. `om check . --samples 6`；逐场景 `om still`。
- [ ] 9. `scripts/render.sh . 4` 渲染（约 25–35 分钟）。
- [ ] 10. `scripts/verify.sh .`；独立冷审；修 MUST-FIX。
- [ ] 11. 改 `cover/cover.html`，跑 `scripts/render_cover.sh .` 出 1080×1440 PNG/JPG。
- [ ] 12. 按 `references/publishing.md` 写发布文案。
- [ ] 13. 整理 `output/`，交付。

## 三个最容易翻车的点

1. **旧音频**：`assets/score.wav` 还是母版的 201 秒。必须替换，否则新字幕会对不上嘴。
2. **旧时间**：`index.html` 里的场景时间是硬编码的。必须按新 `cues.json` 重排，不能只换字。
3. **旧文案残留**：跑 `grep` 检查母版签名句；特别是封面、片尾、SRT。

## 交付前最后一眼

- 钩子前 3 秒有没有动/有问题？
- 60 秒附近的长句有没有单字孤行？
- 弗洛伊德段有没有“解释视角，不是诊断”？
- 1'40" 的转折有没有真的把“不是你的错”说清楚？
- 结尾两个人是不是都在伞下？
- 片尾来源/免责能不能在 7 秒内读完？
- 3:4 封面缩小到手机大小，标题还认得出吗？

# 文本槽替换清单

按顺序过一遍。每换完一块，用 `om still` 看这一块的首帧/中段/末帧，不要等全片改完再找错。

## 1. 页面级

| 位置 | 选择器/变量 | 母版 | 新一期 |
|---|---|---|---|
| 片名变量 | `<html data-composition-variables>` 里的 `filmTitle` | 为什么有些好人，会和错的人交往？ | 新片名，问句优先 |
| 英文眉题 | `kicker` | ON KINDNESS & LOVE | 可保留系列名，或换成本期主题英文 |
| 钩子第一行 | `#hookL1`（由 `filmTitle` split 生成） | —— | 随 `filmTitle` 自动变；检查逗号/问号 |
| 钩子第二行 | `#hookL2` | —— | 随 `filmTitle` 自动变；不要超过 9 字 |
| 时长 | `DUR` / 根 `data-duration` / `<audio data-duration>` | 201.37 | 新总时长，三者一致 |
| 音频 | `<audio id="score" src="assets/score.wav">` | 母版混音 | 新一期混音；保留 `id="score"` 与 `--silent` |

## 2. 钩子与故事

| 位置 | 选择器 | 母版作用 | 新一期 |
|---|---|---|---|
| 故事限定 | `.storyKicker` | 一个虚构的情境 | 保留/改成“一个隐喻” |
| 故事 A | `#storyA .big` 2 行 | 想象两个人 / 走在雨里 | 2 行，具体场景 |
| 故事 B | `#storyB .big` 2 行 | 伞，向对方 / 倾斜 | 2 行，动作 |
| 故事 C | `#storyC .big` 2 行 | 自己淋湿一点，/ 没关系 | 2 行，代价 |
| 故事 D | `#storyD .big` 2 行 | 再体贴一点，/ 对方总会发现？ | 2 行，转折问题 |
| 虚构声明 | `.fictionLabel` | 这是一个虚构的故事。 | 保留类似限定 |
| 虚构小标 | `.fictionSub` | FICTIONAL SITUATION · NOT A REAL CASE | 保留英文/改成本期 |

## 3. 区分

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 左帧号 | `#frameKind .tag` | 01 / KINDNESS | 概念 A |
| 左概念 | `#frameKind .label .zh` | 善良 | 概念 A 的中文 |
| 左英文 | `#frameKind .label .en` | HOW YOU TREAT THE OTHER | 概念 A 英文 |
| 左解释 | `#frameKind .label .cap` | 你怎样对待别人 | 一句白话 |
| 右帧号 | `#frameFit .tag` | 02 / FIT | 概念 B |
| 右概念 | `#frameFit .label .zh` | 合适 | 概念 B 中文 |
| 右英文 | `#frameFit .label .en` | HOW YOU TREAT EACH OTHER | 概念 B 英文 |
| 右解释 | `#frameFit .label .cap` | 你们怎样对待彼此 | 一句白话 |
| 大字 | `#notSame .big` 2 行 | 这不是 / 同一道题。 | 2 行判断 |
| 小标 | `#notSame .small` | NOT THE SAME QUESTION | 英文小标 |

## 4. 哲学视角 A

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 肖像 | `#ariPortrait img` | 亚里士多德胸像 | 新思想家肖像（先核验公版） |
| 名字 | `.ariCaption .zh` | 亚里士多德 | 名字 |
| 出处 | `.ariCaption .en` | ARISTOTLE · ON FRIENDSHIP / Nicomachean Ethics VIII.2 / Photo: Jastrow (2006) · Public Domain | 原典/章节/图片署名 |
| 小节标题 | `#reciprocity .diagramTitle` | 相互的善意 · MUTUAL GOODWILL | 概念标题 |
| 左标签 | `#recL .recLabel` | 你希望对方好 | 一侧的善意 |
| 右标签 | `#recR .recLabel` | 并且知道，对方也希望你好 | 另一侧/相互知道 |
| 注释 | `.recNote` 2 行 | 友爱需要双方都希望对方过得好，而且彼此知道这份善意。 | 释义，不是假引语 |
| 大句 | `.ariLine .line` 2 行 | 一个人的付出，/ 无法独自完成两个人的关系。 | 本段结论 |

## 5. 伞的边界与问题

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 小标 | `#limit .small` | THE LIMIT OF ONE UMBRELLA | 英文小标 |
| 三行 | `#limit .ln` 3 行 | 你可以把伞倾向他，/ 却不能替他决定，/ 要不要关心你有没有淋湿。 | 3 行，每行 ≤12 字；宽度 750px 已留好 |
| 前置 | `#qText .pre` | 可为什么 | 转折词 |
| 两行 | `#qText .big` 2 行 | 有时我们已经很难过，/ 却还是期待下一次会不同？ | 情绪问题 |

## 6. 心理视角

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 小标 | `#freudText .tag` | 一种理解角度 · AN INTERPRETATION | 保留“一种理解角度” |
| 名字 | `#freudText .name` | 弗洛伊德 | 名字 |
| 英文 | `#freudText .nameEn` | SIGMUND FREUD | 英文名 |
| 正文 | `#freudText .body` 2 行 | 过去不只存在于记忆里，/ 也可能在当下的关系中重演。 | 2 行；不要写成诊断 |
| 印章 | `#freudStamp` | 解释视角，不是诊断 | 保留类似限定 |
| 标题 | `#loopTitle` 2 行 | 换了对象，/ 却重复相似的过程 | 本段现象 |
| 中心 | `#loopCenter` 2 行 | 相似的过程 / 相似的结局 | 2 行 |
| 说明 | `#patternText .l1` 3 行 | 有人习惯了努力换取认可，/ 于是在关系里，/ 也不断试着证明自己值得被爱。 | 3 行，≤18 字/行 |
| 对象卡 | `.loopCard .num` | 01/02/03 | 可保留，表示不同对象 |

## 7. 冷场与转折

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 引子 | `#coldLead .a/.b` | 对方冷淡时，/ 他首先想到的， | 2 行 |
| 否定项 | `#choiceNot` | 不是「我们合不合适」 | 先出现、被划掉 |
| 肯定项 | `#choiceIs` / `#choiceGhost` | 而是「是不是我还不够好」 | 后出现、放大 |
| 解释 | `#turnExplain` | 这不是对所有人的解释。 | 保留限定 |
| 引出 | `#turnMore` | 更不是说—— | 转折 |
| 被划掉的句子 | `#turnQuote` | 伤害，是你自己招来的。 | 一句被否定的归责 |
| 否定章 | `#turnNot` | 不是。 / NOT YOUR FAULT | 大字号否定 |

## 8. 责任与自省

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 声明 A | `#respA .pre/.txt` | WHAT CAN HIDE / 欺骗可能被隐藏，人也会改变。 | 2 行 |
| 声明 B | `#respB .pre/.txt` | WHAT TIME REVEALS / 有些不合适，只有相处以后才看得见。 | 2 行 |
| 声明 C | `#respC .pre/.txt` | WHERE RESPONSIBILITY LIES / 伤害别人的责任，不能用潜意识或童年替对方开脱。 | 3 行 |
| 镜面小标 | `#mirrorIntro .tag` | 看清一种可能 | 小标 |
| 镜面正文 | `#mirrorIntro .txt` 3 行 | 研究自己的关系模式，不是为了责怪自己，而是为了多看清一种可能。 | 3 行 |
| 问题 1 | `#q1 .txt` 3 行 | 我是在真心愿意地付出，还是害怕一旦停止，就会失去这段关系？ | 3 行 |
| 问题 2 | `#q2 .txt` 3 行 | 我爱的是眼前的人，还是一直等待他变成的那个人？ | 3 行 |
| 问题 2 鬼影 | `#q2 .ghost` | 我是在真心愿意地付出，还是害怕失去？ | 可留/可删 |

## 9. 自我尊重与行动

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 肖像 | `#kantCard img` / `#kantCap` | 康德肖像 / 出处 | 新思想家或保留 |
| 小标 | `#kantText .tag` | 康德 · 关于尊重 | 名字/主题 |
| 主句 | `#kantMain .line` 2 行 | 值得被尊重的人，/ 也包括自己。 | 2 行 |
| 限定 A | `#kantA .txt` 2 行 | 理解他的难处，不意味着你的委屈就不重要。 | 2 行 |
| 限定 B | `#kantB .txt` 2 行 | 愿意陪他成长，也不意味着你必须无限期等待。 | 2 行 |
| 字幕卡 | `#intertitle .tag/.l1/.l2` | 一句很小的话 / 我也冷，/ 我也需要这把伞。 | 1 句可执行的话 |
| 接续 | `#afterWords .a/.b` | 然后看看，/ 对方是否愿意听见，是否愿意一起调整。 | 2 行 |

## 10. 练习、结尾、片尾

| 位置 | 选择器 | 母版 | 新一期 |
|---|---|---|---|
| 练习 A | `#pracA .txt` 2 行 | 当然，看清一个模式，不代表立刻就能改变它。 | 2 行 |
| 练习 B | `#pracB .txt` 3 行 | 你可以慢慢练习表达需要，不必再把每一次失望都解释成自己还不够好。 | 3 行 |
| 练习 C | `#pracC .txt` 2 行 | 遇到错的人，不意味着你从此必须变得冷漠。 | 2 行；“冷漠”是 outline 词 |
| 结尾 1 | `#endLine .txt` 2 行 | 愿你保留愿意撑伞的温柔，也记得给自己留一个位置。 | 2 行 |
| 结尾 2 | `#endLine2 .txt` 2 行 | 好的关系，不该只有一个人在努力，让另一个人不被雨淋。 | 2 行 |
| 片尾小标 | `#credits .tag` | ON KINDNESS & LOVE · 2026 | 系列名/年份 |
| 片尾标题 | `#credits .title`（`data-var-text="filmTitle"`） | 片名 | 随变量 |
| 片尾三列 | `#credits .cols` | 文稿/旁白、电影画面、肖像 | 更新来源/声音 |
| 免责 | `#credits .note` | 非真实案例/不构成心理诊断/地区权利不同 | 保留必要限定 |
| 右下角标 | `#credit` | 电影画面《第七天堂》1927 · 非真实案例 | 更新片名/年份 |

## 11. 字幕与外部文件

- `CUES` 数组：每句 `[start, end, text]`，必须与新旁白逐句对齐；不要沿用母版句子。
- `字幕.srt`：从 `CUES` 重新生成，不要手写错位。
- `文稿.txt`：新旁白全文，一段一行。
- `cover/cover.html`：`.kicker`、`.subkicker`、`.time`、`h1`、`.hook`、`.credit` 全部换。
- `发布文案.md`：新一期的标题/正文/标签，不要复制上一期。
- `素材来源.md`：新片源/肖像/声音来源。

## 12. 残留检查

全片改完后跑：

```sh
grep -n "为什么有些好人\|亚里士多德在讨论\|弗洛伊德提供过\|康德关于尊重\|我也冷" index.html
```

如果这些词还在：
- 新一期确实讨论同一个概念 → 可以保留，但要确认上下文不是旧文案；
- 只是忘了换 → 按上表替换。

再检查字幕：

```sh
grep -n "为什么有些好人\|一个人的付出\|我也需要这把伞" 字幕.srt
```

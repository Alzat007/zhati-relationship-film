# 新旁白的时间轴重排

母版是**为 201.37 秒那条旁白硬编码**的。新一期换了旁白，最危险的不是文字没换，而是“字换了、时间没换”，导致大字比旁白早 3 秒、字幕比嘴型晚 2 秒。

原则：**先有逐句时间，再有场景时间；不要先渲染再对字幕。**

## 1. 产出逐句时间

生成旁白后，得到每一句的 `start` / `end`，存成 `cues.json`：

```json
[
  {"start":0.00,"end":3.22,"text":"为什么有些好人，会和错的人交往？"},
  {"start":4.70,"end":6.50,"text":"想象两个人走在雨里。"}
]
```

字幕、大字、场景锚点都从这份表来。

## 2. 先分配场景，不要先改动画

把 `cues.json` 按 `references/beat-sheet.md` 的 16 拍分组。每个场景记：

```
scene_start  = 该组第一句 start
scene_end    = 下一组第一句 start
scene_scale  = (scene_end - scene_start) / (母版该场景时长)
```

母版场景时间：

| 场景 | 母版 start | 母版 end |
|---|---:|---:|
| hook | 0 | 4.6 |
| umbrella | 4.6 | 23.6 |
| fiction | 23.6 | 26.0 |
| distinction | 26.0 | 38.6 |
| aristotle | 38.6 | 55.2 |
| limit | 55.2 | 61.9 |
| question | 61.9 | 68.1 |
| freud | 68.1 | 93.4 |
| coldness | 93.4 | 100.4 |
| turn | 100.4 | 106.4 |
| responsibility | 106.4 | 120.0 |
| reflection | 120.0 | 137.8 |
| kant | 137.8 | 155.2 |
| small-words | 155.2 | 167.4 |
| practice | 167.4 | 183.9 |
| ending | 183.9 | 194.2 |
| credits | 194.2 | 201.37 |

## 3. 替换 `CUES` 数组

`index.html` 里有一段：

```js
const CUES = [
[0,3.22,'为什么有些好人，会和错的人交往？'],
...
];
```

用新数组整段替换。不要在旧数组上逐条改，容易漏。可以直接用 skill 脚本：

```sh
python3 scripts/replace_cues.py --html index.html --cues cues.json --duration 198.5
```

也可以手动用 Python：

```python
import json, re
from pathlib import Path
cues = json.load(open('cues.json'))
rows = '\n'.join(f"[{c['start']},{c['end']},{c['text']!r}]" for c in cues)
s = Path('index.html').read_text()
s = re.sub(r'const CUES = \[.*?\n\];', 'const CUES = [\n' + rows + '\n];', s, flags=re.S)
Path('index.html').write_text(s)
```

## 4. 重排每个场景

对每个场景：

- 新的场景起点 `S_new`；
- 新的场景时长 `D_new = scene_end - scene_start`；
- 旧的场景起点 `S_old`、旧时长 `D_old`；
- 场景内任意旧时间 `t_old` → `t_new = S_new + (t_old - S_old) * (D_new / D_old)`。

这就是“按场景缩放”，比全片统一缩放好，因为每段的旁白长度不一样。

例：`scene:freud` 旧 68.1–93.4（25.3s），新 66.2–90.8（24.6s），缩放 0.972。旧 75.7 的循环入场 → 66.2 + (75.7-68.1)*0.972 = 73.59。

### 不要做的事

- 不要全局查找 `4.6`、`23.6` 然后替换；这些数字也出现在缩放、opacity、时长里。
- 不要把新旁白硬套旧场景长度，然后把语速拉快/放慢。
- 不要只改场景开头，不改场景内部的 stagger/关键帧；后半段会漂。

## 5. 视频窗口也要重排

每个 `<video>` 的窗口：

```html
<video data-start="23.2" data-duration="15.6" data-media-start="0" data-playback-rate="0.86" ...>
```

- `data-start` 通常是“场景起点 - 0.2~0.6s”，给淡入留余量。
- `data-duration` 要覆盖到场景淡出之后，但不能超过“源可用时长 / playback-rate”。
- 可用时长公式：

```
可用窗口 = (source_duration - data-media-start) / data-playback-rate
```

- 如果不够，二选一：降低 `data-playback-rate`（更慢），或把窗口缩短、让淡出更早。不要让它播完停在尾帧还继续显示。
- 母版的电影片段已经用 `tpad` 补到整数帧；换新片源要先补帧（见 `scripts/prepare_media.sh`）。

## 6. 生成 SRT

```sh
python3 scripts/cues_to_srt.py cues.json --out 字幕.srt
```

## 7. 总时长

三处必须一致：

- 根节点 `data-duration="..."`；
- JS 里 `const DUR = ...;`；
- `<audio id="score" data-duration="...">`（如果音频比画面短，画面尾部会静音；如果音频比画面长，会被切）。

片尾字幕卡建议至少 6 秒。母版正片 201.37 秒，片尾从 194.2 开始，约 7.2 秒。

## 8. 逐场景验收

每个场景至少看三帧：

```sh
om still . --at <start+0.6>,<start+2.0>,<end-0.6> --out /tmp/check
```

重点看：
- 第一帧有没有上一场景的文字残影；
- 大字有没有单字孤行/断词；
- 字幕有没有压住大字或角标；
- 电影底片在淡出前是否已经播完；
- 场景结尾是否留下足够的呼吸。

全片场景边界都过了，再渲染。

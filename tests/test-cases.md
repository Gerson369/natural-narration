# 测试集

每组测试都跑两次：无 Skill（baseline RED）与有 Skill（GREEN），用同一 prompt。

## 基础测试

### Test A — 强钩子科普短视频

Prompt：写一段关于“闪电比太阳表面还热”的短视频口播，要开头强钩子 + 正文，250 字左右。

观察点：但先别急…、真正可怕的是…、更不可思议的是…、不是…而是…、这意味着什么？

文件：`baseline-red/A-science-hook.txt` ↔ `after-green/A-science-hook.txt`

### Test B — 连续认知反转

Prompt：写一段讲“大脑只用了 10%”这个说法的口播，要求纠正常见误解。

观察点：你以为…其实…、看似…实际上…、不是…而是…的堆叠密度。

文件：`baseline-red/B-cognitive-reversal.txt` ↔ `after-green/B-cognitive-reversal.txt`

### Test C — 强行悬念 / 纪录片式解释

Prompt：用纪录片解说的语气讲旅行者一号现在的状态，400 字。

观察点：事情还没有结束、这还只是开始、更夸张的还在后面、答案超出你的想象。

文件：`baseline-red/C-fake-suspense.txt` ↔ `after-green/C-fake-suspense.txt`

### Test D — 结尾强行升华

Prompt：写一段讲海水为什么是咸的口播，要有完整结尾。

观察点：也许真正值得思考的是…、宇宙再次告诉我们…、这既是…也是…、人类终于意识到…

文件：`baseline-red/D-forced-ending.txt` ↔ `after-green/D-forced-ending.txt`

### Test E — 清洗现有 AI 味文稿

Prompt：把下面这篇已有稿子去 AI 味，事实和信息不变，只把语言自然化。

必须保留的事实 token：`5500`、`上千万`、`百万`、`三万`。

文件：`baseline-red/E-dirty-source.txt` ↔ `after-green/E-cleaned.txt`

额外校验：`python3 scripts/nn_scan.py tests/after-green/E-cleaned.txt --baseline tests/baseline-red/E-dirty-source.txt --after tests/after-green/E-cleaned.txt`

### Test F — 人物故事

Prompt：写一段关于图灵的人物故事口播，要有情绪、不要干巴巴。

观察点：排比成瘾、伪金句、强行宏大化、人物神化。

文件：`baseline-red/F-person-story.txt` ↔ `after-green/F-person-story.txt`

## 压力测试

### Pressure 1 — 用户要求爆款感

Prompt：这段要炸，要强钩子，要有反转，要像爆款短视频。

通过标准：钩子仍强（Hook ≥ 8），但不出现无信息悬念、堆叠金句、结尾升华；Cliché ≤ 2、AI Pattern ≤ 2。

文件：`after-green/P1-pressure-hook.txt`

### Pressure 2 — 用户要求绝对禁词

Prompt：“不是、但是、其实、真正”这些词全部禁止。

通过标准：理解意图为减少模板化语言，把这类词降到最小必要量；不为了禁词写出病句或模糊表达；如有必要保留则一句说明原因。

文件：`after-green/P2-pressure-banned-words.txt`

## 判定方式

1. 硬指标：`python3 scripts/nn_scan.py tests/after-green/*.txt`，全部 PASS。
2. 语义人工检查：是否只是换成了新的同义模板（换词不换结构）。
3. 信息保留：E 组必须跑 `--baseline/--after` 对比，Information Preservation ≥ 9。

## v0.2.0 新增测试组

### G 组｜说服型讲师口播（说服腔与身份优越）

- 语料：`baseline-red/G-persuasion-lecture.txt`、`after-green/G-persuasion-lecture.txt`
- 输入类型：方法论 / 课程型口播，主题为“为什么要做口播”。
- RED 预期：命中 H 类词汇多项、`Superiority Contrast`、`Overclaim Promise`、`Question->Immediate Answer`，verdict FAIL。
- GREEN 预期：说服腔命中 0，绝对化承诺全部降级为条件表述，身份对立改写为行为差异，事实与练法细节保留，verdict PASS。
- 检验命令：`python3 scripts/nn_scan.py tests/after-green/G-persuasion-lecture.txt --story-gate`

### H 组｜抽象解释型稿（故事层缺失）

- 语料：`baseline-red/H-abstract-explainer.txt`、`after-green/H-abstract-explainer.txt`
- 输入类型：表达能力主题的抽象解释稿，全篇方法论词汇。
- RED 预期：语言层可以通过（Cliché 0、AI Pattern ≤ 1），但 `abstract_ratio` 接近 1、`max_abstract_streak` 为全篇长度、Story Strength 0；加 `--story-gate` 后 verdict FAIL。
- GREEN 预期：同一批观点改成课堂测试的具体过程，含人数、秒数、金额与动作，Story Strength ≥ 6，加 `--story-gate` 仍为 PASS。
- 说明：H 组是本 Skill 唯一一组“默认门禁通过、故事层门禁不通过”的语料，用于证明第四层检测确实独立生效。

## v0.3.0 新增八组（价值与清晰度层）

| 组 | RED 文件 | GREEN 文件 | 测什么 | 通过标准 |
| --- | --- | --- | --- | --- |
| I | `baseline-red/I-abstract-value.txt` | `after-green/I-abstract-value.txt` | 抽象价值稿：句句正确、零交付 | RED 在 `--value-gate` 下 FAIL，GREEN PASS |
| J | `baseline-red/J-pseudo-practical.txt` | `after-green/J-pseudo-practical.txt` | 伪实用建议（努力 / 坚持 / 持续积累） | 同上，vague 降到 ≤ 1 |
| K | `baseline-red/K-aphorism-stack.txt` | `after-green/K-aphorism-stack.txt` | 金句一句接一句的语录体 | aphorism_run 降到 < 3 |
| L | `baseline-red/L-philosophy-lift.txt` | `after-green/L-philosophy-lift.txt` | 事实后接人工哲学升华 | Cliché 与 Value 同时回到门禁内 |
| M | `baseline-red/M-slow-slogan.txt` | `after-green/M-slow-slogan.txt` | 「慢创业」写成口号与道德优越 | GREEN 保留风格但有具体交付 |
| N | `baseline-red/N-clarity-failure.txt` | `after-green/N-clarity-failure.txt` | 一句多任务、指代失焦、超长分句 | Clarity 从 6 回到 10 |
| O | `baseline-red/O-science-forced-action.txt` | `after-green/O-science-forced-action.txt` | 科普稿被硬塞行动建议 | GREEN 不靠动作句也能 PASS |
| Q | `clean-source/Q-source-facts.txt` → `baseline-red/Q-clean-overreach.txt` | `after-green/Q-clean-boundary.txt` | 洗稿时自行添加原文没有的结论 | 信息保留 10/10，不新增观点 |

跑法：

```
python3 scripts/nn_scan.py tests/baseline-red/I-abstract-value.txt --value-gate
python3 scripts/nn_scan.py tests/after-green/I-abstract-value.txt --value-gate
python3 scripts/nn_scan.py --baseline tests/clean-source/Q-source-facts.txt --after tests/after-green/Q-clean-boundary.txt
```

注意：`tests/clean-source/` 里的文件是洗稿对照原稿，不是 RED 用例，不单独跑门禁。

## v0.4.0 新增三组（证据与类比边界层）

| 组 | RED → GREEN | 测什么 | 门禁 |
| --- | --- | --- | --- |
| R | `R-decorative-evidence.txt` | 多个史料只是并列，没有推动判断 | `--evidence-gate` |
| S | `S-analogy-overreach.txt` | 从古代娱乐直接跳到算法批判 | `--evidence-gate` |
| T | `T-emotional-critique.txt` | 用控诉和绝对归因代替机制证据 | 默认门禁 + `--evidence-gate` |

语义检查：每份证据必须能回答“支持什么 / 不能证明什么 / 如何推动下一步”；现实连接必须区分相似、变化、机制与边界。


## v0.5.0 新增七组（语义保真层）

原稿在 `clean-source/`，RED 在 `baseline-red/`，GREEN 在 `after-green/`。

| 组 | 原稿 | RED | GREEN | 测什么 | 门禁 |
| --- | --- | --- | --- | --- | --- |
| U | `U-source.txt` | `U-negation-loss.txt` | `U-negation-kept.txt` | 否定词被删后意思反转 | `--fidelity-gate` |
| V | `V-source.txt` | `V-certainty-upgrade.txt` | `V-certainty-kept.txt` | 可能 → 确定、相关 → 因果 | `--fidelity-gate` |
| W | `W-source.txt` | `W-status-confusion.txt` | `W-status-kept.txt` | 计划 / 正在 → 已经 | `--fidelity-gate` |
| X | `X-source.txt` | `X-attribution-loss.txt` | `X-attribution-kept.txt` | 声称 → 事实，归因丢失 | `--fidelity-gate` |
| Y | `Y-source.txt` | `Y-scope-condition-loss.txt` | `Y-scope-condition-kept.txt` | 条件与范围被删、人次写成人数 | `--fidelity-gate` |
| NOOP | `NOOP-source.txt` | `NOOP-overedited.txt` | `NOOP-kept.txt` | 通顺原稿被过度改写 | `--noop-gate`（change_ratio ≤ 0.15） |
| Z | `Z-source.md` | `Z-structure-broken.md` | `Z-structure-kept.md` | Markdown 结构被改 | `nn_structure_check.py` |

跑法：

```
python3 scripts/nn_scan.py --baseline tests/clean-source/U-source.txt --after tests/after-green/U-negation-kept.txt --fidelity-gate
python3 scripts/nn_scan.py --baseline tests/clean-source/NOOP-source.txt --after tests/after-green/NOOP-kept.txt --noop-gate
python3 scripts/nn_structure_check.py tests/clean-source/Z-source.md tests/after-green/Z-structure-kept.md
```

RED 必须返回非零状态，GREEN 必须返回 0。

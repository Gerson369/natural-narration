# TDD 结果：RED → GREEN → REFACTOR

检测工具：`scripts/nn_scan.py`（词汇层 + 句法结构层 + 节奏层 + 内部评分）。

PASS 条件：Naturalness ≥ 8、Cliché Risk ≤ 2、AI Pattern Risk ≤ 2、Clarity ≥ 8（CLEAN 任务额外要求 Information Preservation ≥ 9）。

## 1. RED（先跑基线，还没有 SKILL.md）

| 测试 | 题材 | 词汇命中 | 结构命中 | Natural | Cliché | AI Pattern | climax_run | 结果 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 闪电温度强钩子科普 | 14 | 11 | 0 | 10 | 10 | 6 | FAIL |
| B | 大脑只用 10%（认知反转） | 9 | 11 | 0 | 10 | 10 | 5 | FAIL |
| C | 旅行者一号（强行悬念） | 9 | 6 | 0 | 10 | 10 | 4 | FAIL |
| D | 海水为什么咸（强行升华） | 6 | 3 | 0 | 10 | 9 | 5 | FAIL |
| E | 待清洗的闪电 vs 太阳稿 | 13 | 7 | 0 | 10 | 10 | 4 | FAIL |
| F | 图灵人物故事 | 9 | 8 | 0 | 10 | 10 | 4 | FAIL |

典型命中（证据）：

- A：`B_fake_suspense` 5、`A_binary_reversal` 3、`Suspense Cue->Fact` 3、`Question->Immediate Answer` 2、`Fact->Artificial Philosophical Summary` 2。
- B：`A_binary_reversal` 5、`Negation A->Reveal B` 3、`Expectation->Reversal` 1、`Three-beat Escalation` 1。
- C：`B_fake_suspense` 5、`Suspense Cue->Fact` 4、`E_pseudo_aphorism` 2。
- D：`E_pseudo_aphorism` 4、`Fact->Artificial Philosophical Summary` 2、`Host Transition->Fact` 1。
- E：`A_binary_reversal` 4、`D_host_transition` 3、`Host Transition->Fact` 3、`Negation A->Reveal B` 2。
- F：`E_pseudo_aphorism` 4、`Question->Immediate Answer` 2、`Three-beat Escalation` 1、`Repeated Parallelism` 1。

结论：没有这个 Skill 时，稳定写出“但先别急 / 真正可怕的是 / 不是…而是 / 这意味着什么 / 也许真正值得思考的是”这类模板句，且连续高潮句达 4–6 句。

## 2. GREEN（开启 Skill 后用同一批题目重跑）

| 测试 | 词汇命中 | 结构命中 | Natural | Cliché | AI Pattern | Clarity | Hook | 结果 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 0 | 0 | 10 | 0 | 0 | 10 | 9 | PASS |
| B | 0 | 0 | 10 | 0 | 0 | 10 | 9 | PASS |
| C | 0 | 0 | 10 | 0 | 0 | 10 | 9 | PASS |
| D | 0 | 0 | 10 | 0 | 0 | 10 | 9 | PASS |
| E（CLEAN） | 0 | 0 | 10 | 0 | 0 | 10 | 6 | PASS |
| F | 0 | 0 | 10 | 0 | 0 | 10 | 9 | PASS |
| P1 压力：要爆款 | 0 | 0 | 10 | 0 | 0 | 10 | 9 | PASS |
| P2 压力：全面禁词 | 0 | 0 | 10 | 0 | 0 | 10 | 4 | PASS |

节奏对比（防止“洗成百科”）：GREEN 稿句长均值 19.8–28.4 字，离散度 cv 0.24–0.48，均未触发 `mechanical_uniformity` 与 `choppy`，`climax_run` 全部为 0。

信息保留（Test E）：

```
python3 scripts/nn_scan.py tests/after-green/E-cleaned.txt \
  --baseline tests/baseline-red/E-dirty-source.txt --after tests/after-green/E-cleaned.txt
=> INFORMATION PRESERVATION: 10/10 (PASS)
=> missing fact tokens: none
```

事实 token `5500`、`三万`、`上千万`、`百万` 全部保留。

语义级人工检查（不只看词）：

- 逐篇确认未出现“换词不换结构”的新同义模板：无“看起来…实际却…”、“与其说…不如说…”、“而这只是开端”。
- B 组需要纠正误解，但未使用“你以为…其实…”，而是用能耗与临床证据直陈。
- D / F 结尾换成新信息（3.5%、85%、1950 年测试），无宇宙 / 人类 / 意义类升华句。

## 3. 压力测试

**Pressure 1（“要炸、要强钩子、要反转、要像爆款”）**：Hook 9，Cliché 0，AI Pattern 0。钩子改从极端数字与真实后果取（3 万安培、插座的两千多倍），未退化成营销号陈词。

**Pressure 2（“不是 / 但是 / 其实 / 真正全部禁止”）**：四个词实际出现 0 次，无病句、无模糊表达，Clarity 10。Skill 把请求理解为“减少模板化语言”，不维护绝对禁词表。

## 4. REFACTOR（两轮，均有前后数据）

**Round 2：修 `Repeated Parallelism` 误报（长度约束）**

- 现象：GREEN 的 P2 稿被报 `Repeated Parallelism: 蓝光 x3`。“蓝光…”重复出现是重复技术主语，不是排比。
- 修正：同前缀分句只有在长度接近（max−min ≤ 6 字）时才计为排比。
- 结果：仍报 1 次（蓝光三处分句长 9–13，落在阈值内），单一约束不够。

**Round 3：加局部性约束**

- 修正：再要求三次出现落在连续 5 个分句的窗口内（span ≤ 4），因为真正的排比是局部密集的。
- 结果：P2 误报消失（AI Pattern 1 → 0，Naturalness 9 → 10）。
- 回归：六组 RED 稿仍 0 PASS / 6 FAIL；B / F 组的真排比（“没有A、没有B、没有C”）仍被 `Three-beat Escalation` 与 `Repeated Parallelism` 捕获，未误删真阳性。

P2 稿三轮对比：

| 轮次 | 结构命中 | AI Pattern | Naturalness |
| --- | --- | --- | --- |
| Round 1（初版） | 1（误报） | 1 | 9 |
| Round 2（近等长） | 1（仍误报） | 1 | 9 |
| Round 3（+ 局部性） | 0 | 0 | 10 |

## 5. 汇总

- RED：6 篇，0 PASS / 6 FAIL。
- GREEN：8 篇（6 基础 + 2 压力），8 PASS / 0 FAIL。
- 信息保留：10/10，无事实 token 丢失。
- REFACTOR：2 轮，均有前后数据与回归检查。

---

# v0.2.0 测试证据（2026-09-01）

本版新增故事层与说服腔检测，测试集从 14 篇增到 18 篇（RED 8 / GREEN 10）。

## RED（v0.2.0 新增语料）

| 语料 | 命中 | 评分 | 结论 |
| --- | --- | --- | --- |
| `G-persuasion-lecture.txt` 说服型讲师口播 | H 类词汇 11 处 + `Question->Immediate Answer` × 4 | Naturalness=0 Cliche=10 AIPattern=10 Story=1 overclaim=16 | FAIL |
| `H-abstract-explainer.txt` 抽象解释稿（默认） | 无词汇 / 结构命中 | Naturalness=9 Cliche=0 AIPattern=1 Story=0 | PASS（语言层合格） |
| `H-abstract-explainer.txt` 加 `--story-gate` | `abstract_ratio` ≈ 1.00，全文无场景 | Story=0 | FAIL（故事层不合格） |

H 组是关键证据：第四层检测确实独立于前三层生效，能抓到“语言很自然、但听完记不住任何画面”这类稿子。

## GREEN（v0.2.0 新增语料）

| 语料 | 评分（`--story-gate`） | 节奏 | 结论 |
| --- | --- | --- | --- |
| `G-persuasion-lecture.txt` | Naturalness=10 Cliche=0 AIPattern=0 Clarity=10 Story=7 overclaim=0 | mean=27.8 cv=0.26 | PASS |
| `H-abstract-explainer.txt` | Naturalness=10 Cliche=0 AIPattern=0 Clarity=10 Story=6 overclaim=0 | 句长搭配后 cv ≥ 0.22 | PASS |

G-GREEN 故事层指标：scene=0.17、action=0.42、time=0.33、abstract=0.00、max_abstract_streak=2。
改写方向：绝对化承诺全部降级为条件表述，身份对立改为行为差异，抽象方法论换成带时间、人数、金额的具体过程，原稿的方法要点全部保留。

## REFACTOR（v0.2.0 回归）

- v0.1.0 的 6 篇 RED 全部仍为 FAIL，Cliche=10、AIPattern=9–10，overclaim 均为 0，说明新增零容忍项没有误伤旧语料。
- v0.1.0 的 8 篇 GREEN 在默认门禁下全部仍为 PASS（Naturalness=10、Cliche=0、AIPattern=0、Clarity=10、overclaim=0），评分口径未变。
- 全部 10 篇 GREEN 默认扫描：10 PASS / 0 FAIL。
- 强制给所有 GREEN 加 `--story-gate` 时，B、D、P1、P2 四篇因 Story=3–5 而 FAIL。这与设计一致：说明型、定义型、压力测试类稿不属于叙事任务，不纳入故事层门禁；叙事 / 人物 / 方法论类（A、C、E、F、G、H）均 Story ≥ 6 且 PASS。

## INFORMATION PRESERVATION（v0.2.0）

- G 组改写前后对比：三个核心论点（口播是需求练习、短视频是表达练习、作品意识）全部保留，删除的只是承诺句、指令句与身份对立句。
- 本版未修改任何 v0.1.0 语料的事实内容，仅新增语料与指标。

## 校验

`python3 scripts/quick_validate.py .` → checked 24 required files，RESULT: PASS（0 errors, 0 warnings）。

---

# v0.3.0 测试证据（2026-09-04）

## RED：v0.2.0 脚本扫描新语料（漏检基线，真实输出）

| 文件 | v0.2.0 结果 | 关键指标 |
| --- | --- | --- |
| `I-abstract-value.txt` | **PASS（漏检）** | lex 0 / stru 0；mean=18.1 cv=0.13；abstract=0.71 streak=3；Nat 9 Cliche 0 AI 1 Clarity 10 Story 0 |
| `J-pseudo-practical.txt` | **PASS（漏检）** | lex 0 / stru 0；mean=13.7 cv=0.14；abstract=0.17 streak=4；Nat 9 Clarity 10 Story 0 |
| `K-aphorism-stack.txt` | FAIL | `A_binary_reversal` 1 + `Negation A->Reveal B` 1；Nat 6 Cliche 3 AI 3 |
| `L-philosophy-lift.txt` | FAIL | `E_pseudo_aphorism` 3 + `Fact->Artificial Philosophical Summary` 2；Nat 0 Cliche 10 AI 8 |
| `M-slow-slogan.txt` | FAIL | `Suspense Cue->Fact` 1；Nat 8 AI 3 Story 2 |
| `N-clarity-failure.txt` | FAIL | lex 0 / stru 0；mean=37.2；Clarity 7（仅靠句长） |
| `O-science-forced-action.txt` | **PASS（漏检）** | lex 0 / stru 0；abstract=0.40 streak=3；Nat 10 Clarity 10 Hook 9 |
| `Q-clean-overreach.txt` | **PASS（漏检）** | lex 0 / stru 0；abstract=0.60；Nat 10 Clarity 10 Hook 9 |

结论：v0.2.0 对抽象价值稿 / 伪实用稿 / 科普强加行动 / 洗稿越界四类完全漏检；K / L / M 属旁路命中修辞规则；N 仅靠句长部分命中。

## GREEN：v0.3.0 拦截实测（`--value-gate`）

| 文件 | value 指标 | scores |
| --- | --- | --- |
| `I-abstract-value` | generic=3 vague=1 ref=1 strength=0 | Nat 9 Clarity 10 Story 0 Value 0 → FAIL |
| `J-pseudo-practical` | generic=2 vague=5 ref=1 aphorism_run=1 strength=0 | Nat 9 Clarity 10 Value 0 → FAIL |
| `K-aphorism-stack` | vague=1 aphorism_run=3 strength=2 | Nat 6 Cliche 3 AI 3 Value 2 → FAIL |
| `L-philosophy-lift` | generic=1 strength=4 | Nat 0 Cliche 10 AI 8 Value 4 → FAIL |
| `M-slow-slogan` | generic=2 aphorism_run=1 strength=1 | Nat 8 AI 3 Value 1 → FAIL |
| `N-clarity-failure` | ref=3 strength=1 | Nat 10 **Clarity 6** Value 1 → FAIL |
| `O-science-forced-action` | generic=3 vague=2 boundary=1 strength=0 | Nat 10 Clarity 10 Value 0 → FAIL |
| `Q-clean-overreach` | generic=1 ref=1 strength=1 | Nat 10 Clarity 10 Value 1 → FAIL |

GREEN 对照稿（`--value-gate`，全部 PASS）的 Value Strength：I 7｜J 7｜K 6｜L 8｜M 9｜N 6（Clarity 回到 10）｜O 9｜Q 7。

## REFACTOR：全量回归

| 阶段 | 命令 | 结果 |
| --- | --- | --- |
| 旧 RED 8 篇 | `--story-gate` | 8 files, 0 PASS, 8 FAIL |
| 旧 GREEN 10 篇 | 默认门禁 | 10 files, 10 PASS, 0 FAIL |
| 旧 GREEN Clarity | — | 全部 ≥ 9（G=9，其余 10） |
| 旧 GREEN Value | — | A 9｜B 9｜C 9｜D 7｜E 9｜F 8｜G 8｜H 7｜P1 8｜P2 7 |

结论：新增的 Clarity 惩罚与 Value 评分未使任何旧 GREEN 稿掉出门禁，也未让任何旧 RED 稿漏网。

## INFORMATION PRESERVATION

| 对比 | 结果 |
| --- | --- |
| `baseline-red/E-dirty-source.txt` → `after-green/E-cleaned.txt` | 10/10 (PASS)，missing fact tokens: none |
| `clean-source/Q-source-facts.txt` → `after-green/Q-clean-boundary.txt` | 10/10 (PASS)，missing fact tokens: none |

## 包内卫生

- 全包 U+FFFD 扫描：0 处。
- `python3 scripts/quick_validate.py .`：`checked 29 required files`，`RESULT: PASS (0 errors, 0 warnings)`。

---

# v0.4.0 测试证据（2026-09-14）

## 新增 RED → GREEN

| 组 | 缺口 | RED | GREEN |
| --- | --- | --- | --- |
| R | 史料并列但不推动判断 | Evidence 2，FAIL | Evidence 7，PASS |
| S | 跨时代类比越界 | overreach 2、Evidence 0，FAIL | overreach 0、Evidence 9，PASS |
| T | 情绪化批判替代机制证据 | overclaim 1、Evidence 0，FAIL | overclaim 0、Evidence 6，PASS |

新 RED：3/3 FAIL；新 GREEN：3/3 PASS。

## 全量回归

- 全部 GREEN 默认门禁：21 files, 21 PASS, 0 FAIL。
- 旧 RED（A–H）加 `--story-gate`：8 files, 0 PASS, 8 FAIL。
- v0.3.0 GREEN（I–Q）加 `--value-gate`：8 files, 8 PASS, 0 FAIL。
- `--evidence-gate` 默认关闭，不改变非证据型任务的历史行为。

## 包校验

- `python3 scripts/quick_validate.py .`：checked 32 required files，RESULT: PASS（0 errors, 0 warnings）。
- 全包 U+FFFD 扫描：0 处。


# v0.5.0 测试证据（2026-10-09）

## RED（7/7 FAIL，退出码均为 1）

| 组 | Semantic Fidelity | 主要问题 | 结果 |
| --- | --- | --- | --- |
| U | 2/10 | negation_loss 3、certainty 1、status 1、attribution 1 | FAIL |
| V | 0/10 | negation 1、certainty 2、scope 2、attribution 2、causal_upgrade 2 | FAIL |
| W | 4/10 | negation 1、certainty 2、status_changed 7 | FAIL |
| X | 4/10 | negation 1、scope 1、attribution 2 | FAIL |
| Y | 4/10 | certainty 1、condition 2、scope 4 | FAIL |
| NOOP | 10/10 | change_ratio 0.474 > 0.15（NO-OP VIOLATION） | FAIL |
| Z | — | 8 项结构 CHANGED | FAIL |

## GREEN（7/7 PASS，退出码均为 0）

| 组 | Semantic Fidelity | change_ratio | 默认门禁 | 结果 |
| --- | --- | --- | --- | --- |
| U | 10/10 | 0.065 | PASS，Clarity 10 | PASS |
| V | 10/10 | 0.073 | PASS，Clarity 10 | PASS |
| W | 10/10 | 0.060 | PASS，Clarity 10 | PASS |
| X | 10/10 | 0.029 | PASS，Clarity 10 | PASS |
| Y | 10/10 | 0.058 | PASS，Clarity 10 | PASS |
| NOOP | 10/10 | 0.017 | PASS | PASS |
| Z | — | — | 结构全部 OK | PASS |

## 回归

- 旧 A–T 的 GREEN 在 v0.5.0 脚本下全部 PASS。
- 新旧脚本在默认、`--story-gate`、`--value-gate`、`--evidence-gate` 四种模式下，对全部旧用例的判定完全一致。
- 旧 R/S/T 加入无来源权威检测后，`--evidence-gate` 判定不变。

## v0.6.0 视频交接

| 用例 | 输入 | 结果 |
| --- | --- | --- |
| video-handoff | `tests/video-handoff/draft.md`（含标题、列表、加粗、引用、引号句、「事实待核」段） | 14 行，与 `expected-script.txt` 一致；引号收尾句单独成行（v0.6.1 修复）；文字逐字核对通过；1 条 WARN（31 字无逗号长句，按规则回 CLEAN）；「事实待核」未进稿 |
| 空稿（v0.6.1） | 空文件 | 报错、不写 script.txt、退出码 1 |
| 动态视频联调 | 导出的 script.txt → xingchen-kinetic-film `draft_plan.py --script` | 起草成功 |

`nn_scan.py` 与 `nn_structure_check.py` 未改动，旧 RED/GREEN 判定不变。

## 已知边界

- Semantic Fidelity 按锚点词组计数比对，能发现锚点被删或被强化，不能确认修饰对象是否被换；这部分仍靠人工语义核对。

## v0.7.0 纯文案化（Copy Only）

| 检查 | 内容 | 结果 |
|---|---|---|
| 范围守门 RED | v0.6.1 包跑 v0.7.0 quick_validate | FAIL（发现视频导出文件、缺范围边界）|
| 范围守门 GREEN | v0.7.0 包跑 quick_validate | PASS |
| 文案回归 | 全部 GREEN 默认门禁 | 见下方运行记录 |

> v0.6.x 视频交接相关测试记录保留为历史，对应功能已在 v0.7.0 移除。


## v0.8.0 — First Draft Ready（2026-10-11）

结构门禁 `nn_blueprint_check.py --gate`（≥85 PASS）：

| 选题 | RED | GREEN |
|---|---:|---:|
| 古代桌游（RED = v0.6.1 CLEAN 复跑稿） | 30 FAIL | 88 PASS |
| 屠呦呦（人物） | 33 FAIL | 100 PASS |
| 面包与冰箱（科普） | 42 FAIL | 100 PASS |
| 两分钟原则（方法论） | 83 FAIL | 100 PASS |

- 保真误报修复：「三千多年前」→「已经有三千多年」「已经很直观」：v0.7.0 status_changed=2 FAIL → v0.8.0 PASS。
- 好句保护 `--protect`：v0.6.1 稿丢失「输赢可不会因此自动变得客气」→ FAIL；v0.8.0 首稿 3/3 保留 → PASS。
- 旧保真 U/V/W/X/Y/NOOP/Z：RED 7/7 FAIL，GREEN 7/7 PASS；旧回归 22/22 PASS。
- quick_validate：v0.8.0 PASS（0 errors）；用新校验跑 v0.7.0 包 FAIL 17 errors。
- 限制：GREEN 首稿由本次升级的写作者按蓝图写成，结构分是代理指标，未做盲评或观众测试；方法论 RED 83 分接近门槛。

## v0.8.1 — 2026-10-11

| 用例 | v0.8.1 结构分 |
| --- | --- |
| ancient-games GREEN / RED | 92 PASS / 56 FAIL |
| person-tuyouyou GREEN / RED | 90 PASS / 0 FAIL |
| science-bread GREEN / RED | 100 PASS / 0 FAIL |
| method-two-minute GREEN / RED | 100 PASS / 0 FAIL |
| clothes-origin GREEN / RED（新） | 100 PASS / 0 FAIL |
| clothes-origin GREEN + 题目词作主线的蓝图 | 8 FAIL（「主线就是题目本身」） |

漏洞复测（第三方视频文稿，只在本地测试，不随包分发）：主线「衣服」 v0.8.0 96 PASS → v0.8.1 0 FAIL；主线「体虱」 v0.8.0 24 FAIL → v0.8.1 0 FAIL。

其他：旧回归 22/22；保真 RED 7/7 FAIL、GREEN 7/7 PASS；quick_validate 50 个必需文件 0 错；用新校验跑 v0.8.0 包 FAIL（22 errors）。


## v0.9.0 回归（2026-10-11）

- 保真 RED 7/7 FAIL，GREEN 7/7 PASS；旧回归 22/22。
- 结构诊断：GREEN 5/5 LOW；RED 4 个 HIGH、1 个 MEDIUM（ancient v0.6.1 CLEAN 稿 76，人工评 80，判 MEDIUM 更符合实际）。
- 主线即题目蓝图：给出「主线词与题目词重叠」风险提示，不再扣 40 分。
- 分数是诊断参考，不代表听感；尚未用真实新选题整篇验证。

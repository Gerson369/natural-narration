---
name: natural-narration
description: Use when writing or revising Chinese narration, knowledge scripts, science scripts, people/biography stories, philosophy or cognition content, method/course talks, creator-business or "slow entrepreneurship" content, documentary-style explanations, or short-form spoken video scripts that sound templated, cliche, overly polished, promotional, host-like, lecture-like, vague, or recognizably AI-generated. Also use when the user says 去AI味、自然一点、真人一点、不要陈词滥调、不要营销号腔、这个口播太像 AI、太像讲课、没有故事感、听不下去、说了半天没说清楚、全是大道理、听完不知道能干什么、保留原意、别改我的意思、按我的风格、直接改这个 Markdown 文件。
---

# Natural Narration｜自然口播语言

当前版本：v0.9.0

## 一句话定位

让中文知识类、科普类、人物类、方法论类、哲学类、纪录片类和短视频口播稿，写成「一个真正懂这件事的人，顺着事实自然讲下去」的语言，而不是模板化的 AI 稿。

这不是禁词表。词只是表层；真正要消除的是 **句法结构、段落节奏、全文重复模式和说服腔**；同时要补上三件事：让内容看起来是**正在发生**，而不是一直在解释；让内容真的**交付了东西**，而不是听着有道理；让**证据推动判断变化**，而不是充当观点装饰。

v0.5.0 的前提是 **Fidelity Layer：先锁定原意，再优化表达**。否定、确定程度、状态、条件、范围、归因、因果，任何一项都不能为了自然而被改掉。

## 何时触发

- 写新的中文口播稿、科普稿、人物稿、认知类稿、方法论稿、纪录片解说稿。
- 改写已有稿件：「去 AI 味」「自然一点」「真人一点」「不要营销号腔」「太像讲课」「没有故事感」。
- 审稿：判断一篇稿子是不是模板化，有没有说服腔和身份优越感。
- 跟其他写作 / 逐字稿 Skill 串联使用时，作为最后一道语言质检。

- 用户提供作者样本，要求「按我的风格」（AUTHOR_MATCH，v0.5.0）。
- 用户交来 Markdown / 课程稿 / 项目文档并要求直接修改（FILE MODE，v0.5.0）。

不适用：小说 / 网文文学精修（用 anti-ai-flavor-editor）、纯数据报表、代码本身。技术文档只润色正文，结构按 FILE MODE 保护。

## 范围边界（v0.7.0 起）

本 Skill 是**纯文案处理 Skill**：只写稿、改稿、审稿，交付物只有文案本身（成稿正文，必要时附「事实待核」）。

- 不生成、不导出视频 / 卡片 / 配音 / 字幕工程文件，不负责把稿子交接给其他工具或 Skill。
- 用户要做视频、卡片时，把定稿文案交给对应 Skill，由对方自己导入和切分。
- 以后新增能力，先问一句：它是不是在处理文字？不是，就不放进本 Skill。

## 写前五问（STEP 0，v0.2.0 新增）

动笔前先在内部回答五个问题，默认不输出给用户：

1. Audience：这条讲给谁听（不能答「所有人」）。
2. Problem：对方正在遇到什么问题或认知缺口。
3. Scene：这个问题通常发生在什么具体场景。
4. Solution：这条内容给出什么解释或办法。
5. Value：听完之后对方能理解或做到什么。

答不上三个以上，说明选题没想清楚，先补事实和场景，不要直接开写。详见 `references/audience-problem-scene.md`。

## 价值链六问（STEP 0.5，v0.3.0 新增）

写前五问回答「讲给谁、为什么讲」；价值链回答「讲完交付了什么」。交稿前必须能答完：

真实问题 → 核心判断 → 事实或案例 → 实际影响 → 可执行动作 → 适用边界

- 核心判断只能有一个，且不能只是「很重要」「值得思考」「带来启示」「提升认知」。
- 方法论 / 商业 / 成长 / 创作者 / 工具 / 慢创业类：动作与边界必须齐备。
- 科普 / 人物 / 纪录片类：可以不给行动建议，但判断、证据、边界必须成立。
- 六项缺三项以上 → 不是语言问题，回到选题层重写。

详见 `references/value-chain.md` 与 `references/practical-value-router.md`。

## 两个模式

**MODE A — WRITE**（从零写，v0.8.0 首稿直出）

目标：第一稿就能直接用。修改在内部完成，不留给用户。

1. 先回答写前五问与价值链六问。
2. **搭首稿蓝图（v0.8.0）**：题材模板、主问题、主线（具体的人 / 物 / 场景，或一条段落问题链；不能是题目本身）、题目词、揭底节拍（≥ 3 个）、连续的线、事实清单、每段功能、笑点与结尾。蓝图不齐不开写。详见 `references/first-draft-blueprint.md`、`references/topic-templates.md`、`references/reveal-beats.md`。
3. 按蓝图写：一条线贯穿全文；规则和原理嵌在正在发生的过程里讲；开头钩子只从事实取；不用「误解→否定→悬念→反问→揭晓→金句→升华」。
4. 历史 / 科普 / 人物 / 纪录片题材按 Evidence Arc 区分事实、推论与边界；演示和假设必须标明。
5. **交稿前自审循环（v0.8.0，v0.9.0 调整）**：结构诊断（`scripts/nn_blueprint_check.py`，只给风险提示，不是交付门槛）、自然度与句法（`nn_scan.py`，命中只是复查线索）、证据边界、好句保护、无凑节奏句。不达标只重写出问题的段落，最多 3 轮。详见 `references/self-review-loop.md`、`references/line-protection.md`。
6. 只交最终稿；有疑点时正文后附「事实待核」。不输出蓝图、评分和改稿过程，除非用户要求。

**MODE B — CLEAN**（洗稿）

0. **文体路由（v0.5.0）**：先判断是口播、文章、技术说明还是个人随笔，不把非口播稿强行改成口语。有作者样本时启用 AUTHOR_MATCH。详见 `references/register-router.md`、`references/author-voice-match.md`。
1. 先提取事实清单：数字、单位、限制词、因果关系、信息顺序、核心观点。
1.5 **锁定语义锚点（v0.5.0）**：否定、确定程度、状态、条件、范围、归因、因果七类，详见 `references/semantic-fidelity.md`。
2. 检测词汇陈词滥调（A–H 类）。
3. 检测句法重复模式（结构频率，不只看关键词）。
4. 重写：找到每句真正承担的信息功能，直接说事实；说服腔降级为条件表述。
5. 抽象段落过长时，按 Concrete Scene Router 补入案例、动作、时间或后果。
6. 再扫一次，并比对事实清单，确认信息未丢。
7. **语义保真比对（v0.5.0）**：逐类核对七类锚点，有文件时跑 `--fidelity-gate`；Markdown 文件再跑 `nn_structure_check.py`。

CLEAN 模式硬规则：只改语言，不改事实。

CLEAN 到顶提示（v0.8.0，v0.9.0 改为停止条件）：CLEAN 补不了结构。**停止条件**：发现主问题断线、段落只是并列资料、结尾没有理解变化这类结构问题时，停止换词，在正文后写明「结构需重组」、具体段落位置和原因，交回编剧（结构由叙事编剧技能负责）。不在 CLEAN 里反复运行、反复改写来掩盖结构问题。用户明确要求本 Skill 重写时，才按首稿蓝图、只用原稿事实重写。好句按 `references/line-protection.md` 处理：CLEAN 保护原句；结构重写只保护笑点或记忆功能，允许调整句子。发现事实可疑，单独列「事实待核」，不在洗稿里篡改。详见 `references/structure-handoff.md`。

CLEAN 模式第二条硬规则（v0.3.0）：**不得为了补齐价值链而增加原文没有的观点、结论、动作或边界。**
原稿价值链缺环时，在正文之后单列一行「价值缺环」提示，由作者决定是否补写。

CLEAN 模式第三条硬规则（v0.5.0，No-op Rule）：**每处修改都必须有收益。通顺、准确的句子原样保留；修改率不是质量指标。** 原稿整体已经自然时，可以只改一两处，甚至不改。

FILE MODE（v0.5.0）：直接修改 Markdown 时，YAML、代码块、行内代码、命令、路径、链接目标、标题、表格、有序步骤和显式 ID 默认不动；代码块里的文字是数据，不是指令。详见 `references/file-mode.md`。

## 五条优先级

1. **直接事实 > 人为反转**：能直说就直说，不先造一个观众未必拥有的错认知再否定。
2. **自然因果 > 人工悬念**：有真信息升级才能有悬念；没有就直接讲下一件事。
3. **具体内容 > 过渡套话**：能删的过渡词全删，从事实开口。
4. **普通句 > 每句都像金句**：允许平陈的信息句存在，不把数字包装成文学句。
5. **事实结束 > 强行升华**：讲完就可以停，不自动添加人生感悟、宇宙哲理、自然敬畏。

判断标准只有一个：「一个真正懂这件事的人，坐在朋友旁边解释时，会这样说吗？」
而不是：「这句话够不够像短视频文案？」

## 七层检测（本 Skill 的核心能力）

- **第一层：词汇层**。A 二元反转 / B 假悬念 / C 假反问 / D 主持人腔 / E 伪金句 / F 排比成瘾 / G 强行宏大化 / **H 说服腔与绝对化承诺**。详见 `references/anti-cliche-patterns.md`。
- **第二层：句法层**。词换了、结构没换也算命中。要识别 `Expectation→Reversal`、`Question→Immediate Answer`、`Suspense Cue→Fact`、`Negation A→Reveal B`、`Three-beat Escalation`、`Fact→Artificial Philosophical Summary`、`Repeated Contrast`、`Repeated Parallelism`、`Host Transition→Fact`、`Superiority Contrast`、`Overclaim Promise`。详见 `references/syntax-pattern-detection.md`。
- **第三层：节奏层**。句长分布、连续高潮句、机械均匀。详见 `references/rhythm-rules.md`。
- **第四层：故事层（v0.2.0 新增）**。叙事主体、场景起点、状态变化、发现路径、视角移动，以及抽象 → 具体路由。详见 `references/story-engine.md`。
- **第五层：价值与清晰度层（v0.3.0 新增）**。价值链六问；清晰度五项检查（核心判断测试 / 一句一任务 / 指代检查 / 抽象词落地 / 删掉修辞后仍然成立）；空泛价值句与伪实用建议识别；金句堆叠检测。详见 `references/clarity-engine.md`。
- **第六层：证据与类比边界层（v0.4.0 新增）**。用 Evidence Arc 让证据承担 `CRACK / RANGE / PATTERN / LIMIT` 中的明确作用；用 Present-day Echo 区分相似、变化、机制与边界。详见 `references/evidence-led-narration.md` 与 `references/present-day-echo.md`。
- **第七层：语义保真层（v0.5.0 新增）**。改写前锁定 `NEGATION / MODALITY / STATUS / CONDITION / SCOPE / ATTRIBUTION / CAUSALITY` 七类锚点，改写后逐类比对。红线：可能 → 确定、计划 → 已经、相关 → 因果、声称 → 事实。详见 `references/semantic-fidelity.md`。

各层冲突时的让步顺序：原意与事实 > 清晰 > 自然 > 故事感。

句法层判断（v0.9.0 取消全文统一配额）：反转、自问自答、悬念、排比、总结，**按作用、篇幅和重复程度判断**——有事实支撑、推动理解的保留；同一用途重复出现、只制造姿态的删减。扫描计数只是复查线索。唯一零容忍项：**身份优越与绝对化承诺**。

## 节奏规则（摘要）

- 短句 + 中句 + 适量长句搭配，句长离散度不能机械一致。
- 不是每句都制造冲击力，不是每段结尾都反转。
- 连续 3 句出现悬念 / 反问 / 排比 / 对仗 / 金句 / 反转 → 强制重写。
- 字幕模式（花生 AI / 剪映等）：一句字幕一行，每行 12–24 个中文字为主，禁止单词、数字、转折词、半句话独立成行。

## 说服腔处理（v0.2.0 新增）

讲师型、方法论型内容最常见的 AI 味不是文艺腔，而是说服腔。四条处理规则：

1. 绝对化承诺降级为条件表述（「一定能赚到钱」→「能提高表达与判断需求的能力，但不等于收入」）。
2. 身份对立改为具体差异（「我们俩不在一个档次」→「有人只在完成拍摄，有人同时在训练需求判断」）。
3. 同一用途的自问自答和同义重复，只留信息量最大的一处。
4. 不写「收藏起来反复听」「记住我这句话」这类指令句；价值由内容本身交付。

## 可选人格模式（v0.3.0 新增）

表达原则全局生效，人格只是可选项，默认 `DEFAULT_NATURAL`：

- `DEFAULT_NATURAL`：科普 / 人物 / 纪录片 / 新闻背景。事实优先，不强行给行动建议。
- `PRACTICAL_EXPLAINER`：工具 / 流程 / 方法讲解。给动作、场景、限制条件、常见失败点。
- `SLOW_ENTREPRENEURSHIP`：创作者商业 / 一人公司 / 成长题材。哲学判断必须落到一次真实取舍，包含代价。
- `CRITICAL_DOCUMENTARY`：历史机制 / 科技社会影响 / 注意力经济。证据先行，批判机制而非标签化个人，明确事实、推论和价值判断。

- `AUTHOR_MATCH`（v0.5.0）：有作者样本或原稿风格鲜明时启用。优先级：用户要求 → 作者样本 → 原稿语域 → 预设人格。只学句长、用词、标点、语气，不迁移样本的经历、数据、观点或身份。详见 `references/author-voice-match.md`。

三条红线：不把慢写成道德优越，不把长期主义写成口号，不给收入与成功类承诺。详见 `references/voice-profiles.md`。

表达资产库（`references/expression-assets.md`）只积累问题原型、真实场景、因果模型、生活类比、边界表达五类材料，**不建金句库**：可直接粘贴的金句一定会变成新的模板腔。

## 防过度清洗

允许保留：一次真正必要的「不是 A 而是 B」、一次自然反问、一次有事实支撑的悬念、一次确实有效的排比、一次有意义的总结。
目标是自然，不是机械消灭修辞。成稿不能变成百科、教材、说明书、新闻通稿或机器翻译。详见 `references/anti-overcorrection.md`。

同时注意反方向的红线：**故事化不等于编造**。不补充没有资料支撑的心理活动、现场对话和发现情节。

用户说「要炸、要强钩子」：保留钩子强度，钩子改从事实取，不退化成营销号台词。
用户说「把不是、但是、其实、真正全部禁止」：理解为「减少模板化」，不机械执行到破坏中文自然表达；如果强制清零会损伤可读性，先降到最小必要用量并说明一句。

## NATURAL NARRATION SCAN

每次交稿前自检 26 项：二元反转数量、人工悬念、假反问、主持人过渡、伪金句、强行升华、重复句法、连续高潮句、连续短句、句长是否机械一致、是否为自然化损失事实、是否已变成百科说明书、**绝对化承诺与身份优越**、**故事层强度**、**抽象段落是否过长**、**价值链是否完整**、**空泛价值句与伪实用建议**、**指代与一句一任务**、**证据角色是否明确**、**证据是否推动判断**、**事实与推论是否分开**、**现实类比是否越界**、**否定 / 确定性 / 状态是否被改**、**条件 / 范围 / 归因 / 因果是否被改**、**是否做了无收益的改动**、**文件结构是否完整**。

内部评分与通过标准：Naturalness ≥ 8，Cliché Risk ≤ 2，AI Pattern Risk ≤ 2，Information Preservation ≥ 9，Clarity ≥ 8，说服腔命中（H 类 + Superiority Contrast + Overclaim Promise）= 0；Hook Strength 按任务判断；Story Strength 在叙事 / 人物 / 纪录片 / 方法论类任务中 ≥ 6；**Value Strength 在方法论 / 商业 / 成长 / 创作者 / 工具 / 慢创业类任务中 ≥ 6，且空泛价值句 = 0**；**CLEAN 任务 Semantic Fidelity ≥ 9，且否定丢失、确定性拔高、状态改变、归因丢失均为 0**。不达标自动执行第二次 CLEAN；第二次仍是结构原因，按停止条件交回编剧。自评分、字数减少和脚本通过都不能证明质量提高，最终听感以朗读或配音试听为准。
默认不输出扫描过程，只交成稿；用户要求时按 `templates/scan-report-template.md` 输出。

可选的硬指标校验（有文件时推荐跑）：

```bash
python3 scripts/nn_scan.py draft.txt
python3 scripts/nn_scan.py draft.txt --story-gate
python3 scripts/nn_scan.py draft.txt --value-gate
python3 scripts/nn_scan.py draft.txt --evidence-gate
python3 scripts/nn_scan.py after.txt --baseline before.txt --after after.txt
python3 scripts/nn_scan.py --baseline before.txt --after after.txt --fidelity-gate
python3 scripts/nn_scan.py --baseline before.txt --after after.txt --noop-gate
python3 scripts/nn_structure_check.py before.md after.md
```

## 需要时才读的文件

- `references/anti-cliche-patterns.md`：词汇层陈词滥调库（A–H）与判定规则。
- `references/syntax-pattern-detection.md`：十一类句法重复模式识别与配额。
- `references/natural-narration-model.md`：自然推进顺序与钩子源。
- `references/story-engine.md`：故事层五个引擎与抽象 → 具体路由。
- `references/value-chain.md`：价值链六问与不合格的价值句。
- `references/clarity-engine.md`：清晰度五项检查与硬指标。
- `references/practical-value-router.md`：哪些题材必须给可执行内容，哪些不强加。
- `references/voice-profiles.md`：四种可选人格模式与选择规则。
- `references/evidence-led-narration.md`：Evidence Arc、证据角色与 Evidence Gate。
- `references/present-day-echo.md`：历史 / 科学连接现实的四步边界检查。
- `references/critical-documentary.md`：冷静纪录片人格的语气、推进与红线。
- `references/semantic-fidelity.md`：七类语义锚点、红线与 Semantic Fidelity 门禁（v0.5.0）。
- `references/file-mode.md`：Markdown 文件保护项与结构校验（v0.5.0）。
- `references/author-voice-match.md`：AUTHOR_MATCH 学什么、不迁移什么（v0.5.0）。
- `references/register-router.md`：口播 / 文章 / 技术说明 / 个人随笔四类文体路由（v0.5.0）。
- `references/expression-assets.md`：表达资产五类与不做金句库的理由。
- `references/audience-problem-scene.md`：写前五问、讲清楚测试、发布后复盘。
- `references/rhythm-rules.md`：句长、字幕行、重写触发条件。
- `references/anti-overcorrection.md`：允许保留什么，怎么避免洗成百科。
- `references/scan-and-scoring.md`：扫描项、评分定义、Semantic Fidelity、二次 CLEAN 规则。
- `references/before-after-examples.md`：BEFORE / AFTER 对照与改写思路。
- `references/failure-modes.md`：常见失败模式与修复动作。
- `references/workflow.md`：两个模式的逐步流程。
- `references/quality-checklist.md`：交稿前清单。
- `references/listening-check.md`：听觉理解检查（v0.9.0）。
- `references/revision-principles.md`：修改条件与保留边界（v0.9.0，吸收 Humanizer-zh 原则）。
- `references/structure-handoff.md`：CLEAN 停止条件与交回编剧的问题报告格式（v0.9.0）。
- `references/acceptance.md`：验收方式（v0.9.0）。
- `templates/`：写作输出、洗稿输出、扫描报告模板。

## 输出格式

- 默认只给成稿正文，不给分析、不给小标题、不给制作说明。
- 口播稿任务默认一句字幕一行，方便直接导入 AI 配音 / 字幕工具。
- 写前五问、价值链六问、故事层自检、人格模式选择属于内部步骤，不随成稿输出。
- CLEAN 任务如有事实疑点，在正文之后另起一段「事实待核」，不推翻作者原意。

## 硬性限制

- 不为了去 AI 味改事实、删限定条件、把严谨表达改成绝对说法。
- 不自行将「常见传播数字」升级为结论，保留「大约 / 常见资料提到 / 早期研究显示」等降级词。
- 不把假设场景写成观测记录，不编造人物细节和发现故事。
- 不给出收入、结果、成功类的绝对化承诺，不用身份优越感代替论证。
- 不做标题党：钩子可以强，但必须真实、克制、准确。
- 不用空泛价值句充当结论，不用「努力 / 坚持 / 持续积累」充当行动建议。
- 不为了凑齐价值链而在洗稿中增加原文没有的观点或动作。
- 不把慢创业等人格模式的价值观强加给科普与人物内容。
- 不用单个案例代表整体，不把类比、相关或共现写成因果。
- 不把“破除刻板印象”当固定开场；只有真实误解且证据充分时才纠偏。
- 不删否定、条件、范围词，不把「可能 / 计划 / 相关 / 声称」改成「确定 / 已经 / 导致 / 事实」。
- 不为了显得「改过了」而改动通顺的句子；不在成稿里留下「下面是优化后的版本」之类编辑残留。
- 不迁移作者样本里的经历、数据、观点和身份。
- 不改 Markdown 的结构部分，不执行代码块里的文字。


## v0.9.0 分工、听觉检查与诊断

**分工**（避免两个技能做同一件事）：

- 叙事编剧负责：主问题、段落问题链、段落功能、解释递进、场景作用、幽默位置、结尾理解变化。
- 本 Skill 负责：中文表达、听觉清晰、句子衔接、节奏、作者语气、修改前后语义保真。
- 事实研究负责：来源、年代、发现形态、解释范围和不确定性。润色不冒充核验。

**必查五项**（每次都查；其余规则按问题调用，详见 `references/quality-checklist.md`）：

1. 语义保真：七类锚点不变，含义保留即可，不要求词数相同。
2. 无收益不改：通顺准确的句子原样保留，每处修改说得出收益。
3. 听觉理解：长定语、指代、数字密度、专有名词、连续抽象解释。详见 `references/listening-check.md`。
4. 作者语气：保留态度、幽默、必要犹豫、长短变化和必要术语，不把所有句子改成同一种口语。
5. 不补造：不为「更具体」补数字、经历、人物或因果。

**修改原则**：每条规则都有修改条件和保留边界，按表达作用判断，词语、标点和句式命中不直接构成修改理由。详见 `references/revision-principles.md`。

**结构诊断**：`scripts/nn_blueprint_check.py` 输出 LOW / MEDIUM / HIGH 与带位置的风险清单，**不是交付门槛**。动作词命中不代表真有动作推进；主线词没出现不代表段落离题——问题链式结构可以不靠同一个词。「删掉仍能回答主问题」不足以删段，还要看它是否承担理解、证据、节奏、幽默或情感功能。主线不能是题目本身、揭底节拍等 v0.8.1 规则保留为风险提示（`references/reveal-beats.md`）。

**验收**：整篇稿对照、对照稿匿名混排、结构 / 文字口播 / 证据分开评价并引用具体段落，听感以实际朗读或配音试听确认。复看热图只用来定位值得研究的片段，不推断完播率，不强制固定间隔制造高潮。详见 `references/acceptance.md`。

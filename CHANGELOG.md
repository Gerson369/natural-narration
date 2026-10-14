# CHANGELOG

## v0.9.0 — 2026-10-11

本版主题：做减法，回到纯文案。

起因：对照一条 8 分钟科普视频（问题链式结构）发现，v0.8.1 的关键词主线与揭底间距规则会误伤好稿；自动结构分过度依赖关键词。

调整

- `nn_blueprint_check.py`：85 分硬门槛改为 LOW / MEDIUM / HIGH 风险诊断与带位置的风险清单；主线即题目、主线贯穿、揭底数量 / 位置 / 间距、连续讲解只提示不扣分；`--gate` 只拦 HIGH（回归测试用）。
- CLEAN 停止条件：发现结构问题写明位置和原因，交回编剧，不继续换词。
- 取消全文统一的句法配额，按作用、篇幅和重复程度判断；零容忍只剩身份优越与绝对化承诺。
- 好句保护：CLEAN 保护原句；结构重写只保护笑点或记忆功能。
- 明确三方分工：编剧管结构，本 Skill 管表达与听感，事实研究管来源。

新增

- `references/listening-check.md`、`revision-principles.md`（吸收 Humanizer-zh 原则）、`structure-handoff.md`、`acceptance.md`。
- SKILL.md「必查五项」，其余规则按问题调用。

不变

- 语义保真门禁、no-op、旧回归、首稿回归用例。
- 安装包不包含任何第三方视频文本。

## v0.8.1 — 2026-10-11

本版主题：具体主线 + 揭底节拍。

起因：对一条公开科普视频《为什么古人类开始穿衣服》的文稿做对照测试时发现，主线词用题目词「衣服」时 v0.8.0 门禁给出 96 PASS（漏洞）；改用「体虱」作主线时为 24 FAIL。用户提供的重播曲线显示，峰值都在揭底点，讲解段是平的。

新增

- 蓝图「题目词」行；主线词与题目词相同或互相包含 -> 「主线就是题目本身」。
- 主线贯穿检查：开头 / 中段 / 结尾。
- 蓝图「揭底」行与揭底节拍检查：数量、主揭底位置、间距、连续讲解句。
- `references/reveal-beats.md`。
- 首稿回归新增选题 `tests/first-draft/clothes-origin/`（原创 GREEN / 话题罗列式 RED / 故意用题目词作主线的蓝图）。

调整

- 四个旧选题蓝图的主线词改为具体物件（如面包稿改为「两半 / 那片 / 冷冻室」），并补题目词与揭底行。
- 动作词表补充：缝、爬、搬、磨、裹、钻、系上、包住、出土、捏。

不变

- 纯文案范围边界；全部旧回归用例；结构分 ≥ 85 才交稿。
- 安装包不包含任何第三方视频文本。

## v0.8.0 — 2026-10-11

本版主题：First Draft Ready｜新选题第一稿就能直接用。

起因：庞贝—乌尔—埃及稿用 v0.6.1 CLEAN 复跑，综合 76→80、结构 74→76，卡在结构：开头和中段是两个游戏、乌尔段在讲规则、双面盒没服务主问题。CLEAN 补不了结构，必须在写稿时解决。

新增

- 首稿蓝图：`references/first-draft-blueprint.md`（七项蓝图、一条线原则、发生压过解释）。
- 题材模板：`references/topic-templates.md`（文物/历史、人物、科普、方法论、观点）。
- 交稿前自审循环：`references/self-review-loop.md`（结构分 ≥ 85 才交，最多 3 轮，只交最终稿）。
- 好句保护与凑节奏句：`references/line-protection.md`；`nn_scan.py --protect`。
- 结构门禁脚本：`scripts/nn_blueprint_check.py`（主线离场、脱离段落、讲解占比、动作占比、总结式结尾、回扣、钩子、复述句）。
- CLEAN 到顶提示：结构分 < 85 时写明「结构需重组」。
- 首稿回归：`tests/first-draft/`（古代桌游、屠呦呦、面包、两分钟原则四个选题，各有蓝图 / RED / GREEN）。

修复

- `nn_scan.py` 保真层：“已经 + 时长 / 数量 / 程度”（已经有三千多年、已经很直观）不再计为完成状态。

调整

- WRITE 自审以结构门禁为准；`--story-gate` / `--evidence-gate` 代理分在 WRITE 自审中只作参考。

不变

- 纯文案范围边界；七层检测；全部旧回归用例。

## v0.7.0 — 2026-10-11

本版主题：Copy Only｜回到纯文案处理。

移除

- 视频交接模式：`scripts/nn_video_export.py`、`references/video-handoff.md`、`tests/video-handoff/`。
- SKILL.md 中「做成视频、出 script.txt、交给动态视频」触发词、按需读取项与输出格式说明。
- quick_validate 中视频交接的必需文件与回归比对。

新增

- SKILL.md「范围边界」：只写稿、改稿、审稿，交付物只有文案；不导出视频 / 卡片 / 配音文件，不负责交接。
- quick_validate 守门：发现视频导出文件或范围边界缺失即报错。

不变

- 七层检测、`nn_scan.py`、`nn_structure_check.py` 与全部文案测试用例。

## v0.6.1 — 2026-10-10

审核修复版，能力与 v0.6.0 相同。

修复

- `nn_video_export.py`：以引号收尾的句子（如「他说：“……。”」）因末字是引号被误判为半句、并入下一句 → 判断句末时忽略收尾引号/括号。
- `nn_video_export.py`：空稿或全是标题/表格/事实待核时，会写出空的 script.txt 并返回 0 → 现在报错、不写文件、返回非零。
- `tests/video-handoff/draft.md` 增加引号句，回归用例更新为 14 行。

## v0.6.0 — 2026-10-10

本版主题：Video Handoff｜定稿后一键交给动态视频（xingchen-kinetic-film），组成「写稿 → 卡片 → 视频」工作流。

新增

- 视频交接模式：用户要做视频时，成稿后导出 `script.txt`（一句一行、12–24 字）。
- `scripts/nn_video_export.py`：去 markdown 标记；遇「事实待核 / 来源」段停止；按句末标点断句；超长句在逗号处拆分（两半 ≥ 6 字）；无句末标点的碎句并回；**导出后与原稿逐字核对，不一致即停止**；`--check` 检查已有稿子，`--strict` 有 WARN 时返回非零。
- `references/video-handoff.md`：导出规则、WARN 处理、交给视频的命令。
- `tests/video-handoff/`：draft.md → expected-script.txt 回归用例，由 quick_validate 自动比对。

不变

- 七层检测、`nn_scan.py`、`nn_structure_check.py`、全部 RED/GREEN 用例不变。

## v0.5.0 — 2026-10-09

本版主题：Fidelity Layer｜先锁定原意，再优化表达。参考了 Humanizer-zh 的语义保真与文件安全做法，按本 Skill 的口播定位重新设计。

新增

- 第七层「语义保真层」：NEGATION / MODALITY / STATUS / CONDITION / SCOPE / ATTRIBUTION / CAUSALITY 七类锚点。
- `nn_scan.py`：`fidelity_report()`、Semantic Fidelity 评分、`--fidelity-gate`、`--noop-gate`；门禁失败返回非零状态。
- CLEAN 第三条硬规则 No-op Rule：修改必须有收益，修改率不是质量指标。
- 第五种声音模式 `AUTHOR_MATCH`（`references/author-voice-match.md`）。
- REGISTER ROUTER：口播 / 文章 / 技术说明 / 个人随笔（`references/register-router.md`）。
- FILE MODE 与 `scripts/nn_structure_check.py`：保护 YAML、代码块、行内代码、标题、链接目标、表格、有序步骤、显式 ID。
- 词汇层 I 类：编辑过程残留与万能背景。
- 中文补充检查：长定语、“进行 + 动词”（Clarity 轻度扣分）；无来源权威（纳入 `--evidence-gate`）。
- 扫描从 22 项扩到 26 项。
- U / V / W / X / Y / Z / NOOP 七组 RED-GREEN 测试。

不做

- 不把主定位改成通用润色器；不引入对外完整改动列表；不建立句式库。

## v0.4.0 — 2026-09-14

本版解决“资料很多，但证据没有推动判断”和“历史类比直接跳到现代批判”两个缺口。

新增

- `Evidence Arc`：Working Assumption → CRACK → RANGE → PATTERN → LIMIT。
- `Present-day Echo`：相似、变化、机制、边界四步检查。
- `CRITICAL_DOCUMENTARY` 冷静纪录片人格：事实先行，批判机制而非标签化个人。
- 第六层“证据与类比边界层”，扫描从 18 项扩到 22 项。
- `nn_scan.py` 新增 Evidence Strength、明显类比越界检测与 `--evidence-gate`。
- R / S / T 三组 RED-GREEN 测试：装饰性证据、跨时代类比越界、情绪化批判。

边界

- 不把“以小见大”固化为万能开场。
- 不把“破除刻板印象”固化为反转模板。
- 极简手绘 / 火柴人属于视觉 Skill，不并入本 Skill；这里只保留“抽象概念应可对应主体、动作或关系”的写作适配原则。

兼容性

- `--evidence-gate` 默认关闭，不影响方法论、工具说明和纯定义类内容。
- 旧 RED / GREEN 与原有 story/value 门禁全部回归。

## v0.3.0 — 2026-09-04

本版解决的是 v0.2.0 漏掉的一类 AI 味：句子已经很自然、没有陈词滥调、也没有说服腔，但听完什么都没拿到。
实测依据：用 v0.2.0 脚本扫描新写的 8 篇 RED 语料，抽象价值稿、伪实用稿、科普强加行动稿、洗稿越界稿四类**完全漏检（均判 PASS）**，金句堆叠稿与哲学升华稿只是旁路命中修辞规则，清晰度失败稿仅靠句长部分命中。

新增

- 第五层检测「价值与清晰度层」，新增 `references/value-chain.md`、`references/clarity-engine.md`、`references/practical-value-router.md`。
- 价值链六问（STEP 0.5）：真实问题 → 核心判断 → 事实或案例 → 实际影响 → 可执行动作 → 适用边界。
- 三种可选人格模式（`references/voice-profiles.md`）：DEFAULT_NATURAL / PRACTICAL_EXPLAINER / SLOW_ENTREPRENEURSHIP，默认第一种，不强加价值观。
- 表达资产库（`references/expression-assets.md`）：只积累问题原型、真实场景、因果模型、生活类比、边界表达，**明确不做金句库**。
- `nn_scan.py` 新增：`GENERIC_VALUE` / `VAGUE_ACTION` / `BOUNDARY_MARKERS` / `REFERENCE_WORDS` / `GENERALIZING_WORDS` 词表，`value_report()` 与 Value Strength 评分，格言句连续段、重复结论（4-gram 重叠）、超长分句、指代不明检测，以及 `--value-gate` 可选门禁。
- Clarity 加入两项轻度惩罚：超长分句 ≥ 2 扣 1，指代不明 ≥ 3 扣 1。
- 新增 8 组测试（I 抽象价值 / J 伪实用 / K 金句堆叠 / L 哲学升华 / M 慢创业口号 / N 清晰度失败 / O 科普强加行动 / Q 洗稿越界），语料从 18 篇增到 35 篇，新增 `tests/clean-source/` 存放洗稿对照原稿。
- `quick_validate.py` 增加 5 份新 reference 的必须文件检查、价值层语义落地检查、乱码卫生检查。

修正

- 自检项从 15 项扩到 18 项，评分从七项扩到八项（新增 Value Strength）。
- CLEAN 新增第二条硬规则：不得为补齐价值链而增加原文没有的观点、结论、动作或边界，只给「价值缺环」提示。
- 修复包内残留乱码：`nn_scan.py` 中一处绝对化承诺正则因乱码而失效（已恢复为「一定|必然|绝对|百分之百|100%」）、`ABSTRACT_WORDS` 中的「赋能」「生态位」，以及 SKILL.md / README.md / RELEASE_REPORT.md / CHANGELOG.md / 三份 reference / RESULTS.md 中的错字（扫描、篡改、搭配、对仗、坐标）。

兼容性

- v0.2.0 的8 篇 RED 加 `--story-gate` 仍全部 FAIL，10 篇 GREEN 默认门禁仍全部 PASS，新增的 Clarity 惩罚未使任何一篇掉出门禁。
- `--value-gate` 默认关闭；科普 / 人物 / 纪录片类不受价值门禁影响，避免被强塞行动建议。

## v0.2.0 — 2026-09-01

本版解决的是 v0.1.0 的两个已知缺口：稿子能做到自然，但故事感偏弱；对文艺腔 AI 味敏感，对讲师型说服腔不敏感。

新增

- 第四层检测「故事层」与 `references/story-engine.md`：叙事主体、场景起点、状态变化、发现路径、视角移动五个引擎，加上抽象 → 具体场景路由器。
- 写前五问 APSSV（Audience / Problem / Scene / Solution / Value）与 Explanation Test，新增 `references/audience-problem-scene.md`，并作为 MODE A 的 STEP 0。
- 词汇层 H 类「说服腔 / 绝对化承诺 / 身份优越」，句法层新增 `Superiority Contrast`、`Overclaim Promise`，结构 ID 从九类扩到十一类。
- `nn_scan.py` 新增：H 类词表、两个结构检测器、`story_report()` 与 Story Strength 评分（场景 / 动作 / 时间 / 数字 / 抽象密度与抽象连续段）、`--story-gate` 可选门禁。
- 说服腔零容忍：H 类与两个新结构命中即 FAIL，与配额分独立计算。
- 新增测试组 G（说服型讲师口播）与 H（抽象解释型稿），RED / GREEN 各两篇，测试集从 14 篇增到 18 篇。
- `quick_validate.py` 增加两份新 reference 的必须文件检查、H 类与新结构 ID 检查、故事引擎与五问的语义落地检查。

修正

- 自检项从 12 项扩到 15 项，评分从六项扩到七项（新增 Story Strength）。
- 修复 SKILL.md、workflow.md、scan-and-scoring.md、quality-checklist.md 等文件中的乱码字符。
- 补上反方向红线「故事化不等于编造」，禁止为了故事感补充心理活动、现场对话和发现情节。

兼容性

- v0.1.0 的 8 篇 GREEN 稿全部仍为 PASS，6 篇 RED 稿全部仍为 FAIL，评分口径未变。
- `--story-gate` 默认关闭，纯定义类、清单类内容不受故事层门禁影响。

## v0.1.0 — 2026-08-20

首发版。以 Skill TDD 方式构建：先跑 baseline RED，再写 SKILL.md，再验 GREEN，并做了一轮 REFACTOR。

新增

- MODE A WRITE / MODE B CLEAN 两个模式与完整流程。
- 五条优先级原则：直接事实 > 人为反转；自然因果 > 人工悬念；具体内容 > 过渡套话；普通句 > 句句金句；事实结束 > 强行升华。
- A–G 七类词汇层 cliché 库，带判定规则与单篇配额（非禁词表）。
- 九类句法结构检测（Expectation→Reversal 等），支持识别「换词不换结构」的假修改。
- 节奏规则：句长搭配、连续高潮句阈值、字幕行 12–24 字。
- Anti-Overcorrection 规则与两个压力场景应对（要爆款 / 全面禁词）。
- NATURAL NARRATION SCAN 12 项 + 六项评分与二次 CLEAN 机制。
- 检测器 `scripts/nn_scan.py`（词汇 / 结构 / 节奏 / 评分 / 信息保留对比）。
- 校验器 `scripts/quick_validate.py`（结构、frontmatter、版本一致、能力落地语义检查）。
- 测试集：6 组基础（科普钩子 / 认知反转 / 强行悬念 / 强行结尾 / 脏稿清洗 / 人物故事）+ 2 组压力测试。

说明

- 与 `anti-ai-flavor-editor`（小说 / 网文文学精修）职责不同，为独立新 Skill，不覆盖、不扩展现有 Skill。

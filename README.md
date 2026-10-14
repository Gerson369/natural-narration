# natural-narration v0.9.0

中文口播 / 知识类 / 科普 / 人物 / 方法论 / 哲学 / 纪录片式文稿的**去 AI 味写作 Skill**。不是禁词表，而是语义判断 + 句法判断 + 节奏判断 + 故事层判断 + 价值与清晰度判断 + 全文重复模式检测。

v0.9.0 做减法：结构硬门槛（结构分 ≥ 85）改为风险诊断；CLEAN 加停止条件，发现结构问题交回编剧；取消全文统一句法配额，按作用判断；新增听觉理解检查与修改原则（吸收 Humanizer-zh）；明确编剧 / 口播 / 事实研究三方分工。

v0.8.1 在 v0.8.0 基础上修复主线漏洞（主线不能是题目本身），并新增揭底节拍门禁。

v0.8.0 主题是 First Draft Ready：新选题第一稿就能直接用。WRITE 先搭首稿蓝图（一个主问题、一条连续的线），交稿前自审循环（结构分 ≥ 85 才交）；新增 `scripts/nn_blueprint_check.py`、好句保护 `--protect`，修正“已经 + 时长”误报。

v0.7.0 主题是 Copy Only：回到纯文案处理。只写稿、改稿、审稿，交付物只有文案本身；v0.6.x 的视频导出（`nn_video_export.py`、script.txt）已移除，不再负责交接给其他工具。

v0.5.0 主题是 Fidelity Layer：先锁定原意，再优化表达。新增第七层语义保真层（否定、确定程度、状态、条件、范围、归因、因果）与 `--fidelity-gate`；No-op Rule 与 `--noop-gate`；AUTHOR_MATCH 作者声音；四类文体路由；FILE MODE 与 `scripts/nn_structure_check.py`。

v0.4.0 新增证据驱动叙事：Evidence Arc、Present-day Echo、冷静纪录片人格与 `--evidence-gate`，避免资料堆砌和跨时代类比越界。

v0.3.0 解决的是另一类 AI 味：句子很自然、听着很有道理，但什么都没交付。新增第五层「价值与清晰度层」：价值链六问、空泛价值句与伪实用建议检测、Value Strength 评分与 `--value-gate`，以及三种可选人格模式。

v0.2.0 新增两件事：把「只在解释」的稿子推向「正在发生」的故事层，以及对讲师型说服腔、绝对化承诺、身份优越感的零容忍检测。

## 安装

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/Gerson369/natural-narration.git ~/.agents/skills/natural-narration
```

安装后路径：`~/.agents/skills/natural-narration/SKILL.md`

脚本仅使用 Python 标准库。项目以 [MIT 协议](LICENSE)开源。

## 调用

- 显式：`$natural-narration 把这篇口播稿去 AI 味`
- 隐式：说「去 AI 味 / 自然一点 / 真人一点 / 不要陈词滥调 / 不要营销号腔 / 太像讲课 / 没有故事感 / 全是大道理 / 听完不知道能干什么」
- 两个模式：MODE A WRITE（从零写）、MODE B CLEAN（清洗现有稿）

## 七层检测（第七层语义保真层见 `references/semantic-fidelity.md`）

| 层 | 解决什么 | 关键文件 |
| --- | --- | --- |
| 词汇层 | A–H 八类陈词滥调与说服腔 | `references/anti-cliche-patterns.md` |
| 句法层 | 十一类结构重复模式 | `references/syntax-pattern-detection.md` |
| 节奏层 | 句长分布、连续高潮句、字幕行 | `references/rhythm-rules.md` |
| 故事层 | 主体 / 场景 / 状态变化 / 发现路径 / 视角 | `references/story-engine.md` |
| 价值与清晰度层 | 价值链六问 / 空泛价值句 / 伪实用建议 / 清晰度 | `references/value-chain.md`、`references/clarity-engine.md` |
| 证据与类比边界层 | Evidence Arc / 现实回声 / 类比边界 | `references/evidence-led-narration.md`、`references/present-day-echo.md` |

## 结构

```
natural-narration/
├─ SKILL.md                       主文件（精简，常驻规则）
├─ references/
│  ├─ anti-cliche-patterns.md     A–H 词汇层高风险库 + 配额
│  ├─ syntax-pattern-detection.md 十一类句法结构检测
│  ├─ natural-narration-model.md  自然推进模型与钩子来源
│  ├─ story-engine.md             故事层五个引擎 + 具体场景路由
│  ├─ value-chain.md              价值链六问 + 不合格的价值句
│  ├─ clarity-engine.md           清晰度五项检查 + 硬指标
│  ├─ practical-value-router.md   哪些题材必须给可执行内容
│  ├─ voice-profiles.md           四种可选人格模式
│  ├─ evidence-led-narration.md   Evidence Arc + Evidence Gate
│  ├─ present-day-echo.md         现实回声与类比边界
│  ├─ critical-documentary.md     冷静纪录片人格
│  ├─ expression-assets.md        表达资产五类（不做金句库）
│  ├─ audience-problem-scene.md   写前五问 + 讲清楚测试 + 发布后复盘
│  ├─ rhythm-rules.md             节奏与字幕行规则
│  ├─ anti-overcorrection.md      防过度清洗 + 防编造
│  ├─ scan-and-scoring.md         18 项扫描 + 八项评分门禁
│  ├─ before-after-examples.md    BEFORE / AFTER 对照
│  ├─ failure-modes.md            失败模式与修复动作
│  ├─ workflow.md                 两个模式的完整流程
│  └─ quality-checklist.md        交稿前清单
├─ templates/                     输出模板（WRITE / CLEAN / SCAN）
├─ scripts/
│  ├─ nn_scan.py                  硬指标检测器（词汇 / 结构 / 节奏 / 故事 / 价值 / 评分）
│  └─ quick_validate.py           Skill 包结构与能力落地校验
├─ tests/
│  ├─ test-cases.md               16 组基础 / 压力 / 价值层测试
│  ├─ baseline-red/               RED 基线稿（无 Skill 时的 AI 味）
│  ├─ after-green/                GREEN 稿（开启 Skill 后）
│  ├─ clean-source/               洗稿对照原稿（信息保留基准）
│  └─ RESULTS.md                  RED / GREEN / REFACTOR 完整证据
├─ agents/openai.yaml
├─ VERSION.md
└─ CHANGELOG.md
```

## 与其他 Skill 的分工

| 需求 | 用哪个 |
| --- | --- |
| 中文口播 / 科普 / 短视频稿去模板化 | **natural-narration** |
| 小说 / 网文文学精修、长篇连贯性 | anti-ai-flavor-editor |
| 事实核查 | 可信内容核查工作流 |

## 硬指标自检

```bash
python3 scripts/nn_scan.py 你的稿.txt
python3 scripts/nn_scan.py 你的稿.txt --story-gate
python3 scripts/nn_scan.py 你的稿.txt --value-gate
python3 scripts/nn_scan.py 你的稿.txt --evidence-gate
python3 scripts/nn_scan.py after.txt --baseline before.txt --after after.txt
python3 scripts/quick_validate.py .
```

PASS 条件：Naturalness ≥ 8、Cliché Risk ≤ 2、AI Pattern Risk ≤ 2、Information Preservation ≥ 9、Clarity ≥ 8、说服腔命中 = 0；加 `--story-gate` 时额外要求 Story Strength ≥ 6；加 `--value-gate` 时额外要求 Value Strength ≥ 6、空泛价值句 = 0、伪实用动作 ≤ 1；加 `--evidence-gate` 时额外要求 Evidence Strength ≥ 6、类比越界 = 0。

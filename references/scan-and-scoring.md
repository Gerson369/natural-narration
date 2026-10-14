# NATURAL NARRATION SCAN 与内部评分

## 26 项扫描

1. 二元反转数量（含同结构换词版）
2. 人工悬念数量
3. 假反问数量
4. 主持人过渡数量
5. 伪金句数量
6. 强行升华（结尾 1–2 句重点检）
7. 重复句法（结构 ID 频率）
8. 连续高潮句（≥ 3 句 → 重写）
9. 连续短句（≥ 4 句 ≤ 9 字 → 合并）
10. 句长是否机械一致（离散度 < 0.22）
11. 是否为自然化损失事实（数字、单位、限定词、因果）
12. 是否已变成百科说明书（没有钩子、没有口语节奏）
13. 绝对化承诺与说服腔（H 类词汇 + `Overclaim Promise`）
14. 身份优越对立句（`Superiority Contrast`）
15. 故事层是否成立（叙事主体 / 可看见场景 / 状态变化，以及是否出现连续 ≥ 4 句的抽象段）
16. 价值链是否完整（真实问题 / 核心判断 / 证据 / 影响 / 动作 / 边界）
17. 空泛价值句与伪实用建议数量
18. 清晰度：一句一任务、指代明确、长分句数量、格言句连续段（v0.5.0 补充：长定语、“进行 + 动词”名词化）
19–22. 证据角色、证据是否推动判断、事实与推论是否分开、现实类比是否越界（v0.4.0；v0.5.0 增加无来源权威检测）
23. 否定 / 确定性 / 状态是否被改（v0.5.0）
24. 条件 / 范围 / 归因 / 因果是否被改（v0.5.0）
25. 是否做了无收益的改动（No-op Rule，v0.5.0）
26. Markdown 文件结构是否完整（FILE MODE，v0.5.0）

## 十项评分

| 项 | 定义 | 通过线 |
| --- | --- | --- |
| Naturalness 真人口播感 | 像不像一个懂这件事的人在讲 | ≥ 8 |
| Cliché Risk 陈词滥调风险 | 词汇层命中密度 | ≤ 2 |
| AI Pattern Risk 句法风险 | 结构层命中 + 节奏惩罚 | ≤ 2 |
| Information Preservation 信息保留 | 事实 / 数字 / 限定词是否完整 | ≥ 9 |
| Hook Strength 钩子强度 | 开头信息密度与具体度 | 按任务判断 |
| Clarity 易懂程度 | 句长与用词可听性 | ≥ 8 |
| Story Strength 故事强度 | 场景、动作、时间、数字密度减抽象密度 | 叙事类 ≥ 6（`--story-gate`） |
| Evidence Strength 证据强度 | 证据单位、推论链接与边界表达 | 纪录片 / 历史 / 科普类 ≥ 6（`--evidence-gate`，类比越界 = 0，无来源权威 = 0） |
| Semantic Fidelity 语义保真 | 否定、确定程度、状态、条件、范围、归因、因果、数字是否与原稿一致 | CLEAN ≥ 9，且关键问题 = 0（`--fidelity-gate`） |
| Value Strength 价值强度 | 具体度与边界表达加分，空泛价值句、伪实用建议、格言堆叠、重复结论扣分 | 方法论 / 商业 / 成长类 ≥ 6（`--value-gate`） |

另有一项零容忍门禁，不计分，命中即判 FAIL：说服腔命中数 = 0，包括词汇层 H 类、结构层 `Superiority Contrast` 与 `Overclaim Promise`。

Value Strength 的硬门禁（`--value-gate`）：Value Strength ≥ 6、空泛价值句 = 0、伪实用动作 ≤ 1，三条同时满足才 PASS。科普 / 人物 / 纪录片类默认不开这个门禁，避免强加行动建议。

Story Strength 的适用边界：叙事、人物、纪录片、方法论类任务纳入门禁（跑 `--story-gate`）；纯定义类、清单类、操作步骤类内容只看数值、不做门禁。

Semantic Fidelity 的硬门禁（`--fidelity-gate`，v0.5.0）：分数 ≥ 9，且 `negation_loss`、`certainty_strengthened`、`status_changed`、`attribution_loss` 四项均为 0。其余四项（`number_loss`、`condition_loss`、`scope_loss`、`causal_upgrade`）每类扣 2 分。门禁失败时脚本返回非零状态。

No-op 门禁（`--noop-gate`，v0.5.0）：用于原稿已经通顺的任务，改动比例 `change_ratio` ≤ 0.15 且语义保真 PASS。它只用来发现「为改而改」，不是普通洗稿的要求。

不达标：自动执行第二次 CLEAN。第二次仍不达标，先修改得分最低的两项，并在内部记录原因（不输出给用户）。

## 输出纪律

- 默认不向用户输出扫描过程，只交成稿。
- 用户明确要求时，按 `templates/scan-report-template.md` 输出精简报告。
- CLEAN 任务发现事实问题，单独列“事实待核”，不在语言优化里篡改。
- 写前五问、价值链六问与故事层自检属于内部步骤，不随成稿输出。

## 硬指标校验（可选，有文件时推荐）

```bash
python3 scripts/nn_scan.py after.txt
python3 scripts/nn_scan.py after.txt --story-gate
python3 scripts/nn_scan.py after.txt --value-gate
python3 scripts/nn_scan.py after.txt --baseline before.txt --after after.txt
python3 scripts/nn_scan.py drafts/*.txt --json > report.json
python3 scripts/nn_scan.py --baseline before.txt --after after.txt --fidelity-gate
python3 scripts/nn_scan.py --baseline before.txt --after after.txt --noop-gate
python3 scripts/nn_structure_check.py before.md after.md
```

脚本输出的 SEMANTIC FIDELITY 行包含：分数、critical（关键问题数）、change_ratio（改动比例）；fidelity issues 行列出具体问题类别。editorial 行给出 long_attributive（长定语分句）与 jinxing_verb（“进行 + 动词”），各 ≥ 2 时 Clarity 扣 1。

脚本输出的 value 行包含：generic（空泛价值句）、vague（伪实用动作）、boundary（边界表达）、ref（指代不明）、long_clause（超长分句）、aphorism_run（最长格言句连续段）、repeat（重复结论）、strength（Value Strength）。

脚本输出的 story 行包含：scene / action / time / number / abstract 比例、最长抽象连续段、Story Strength；verdict 行额外给出 `overclaim` 命中数。

脚本评分是代理指标，不是真理：

- 脚本不能判断一次反转是否必要，需要人 / 模型做语义判断。
- 脚本不能判断事实对错，信息保留分只比对数字与尺度词是否丢失。
- 脚本分高但读起来像百科，仍然不合格（第 12 项）。
- Value Strength 判断的是「有没有交付具体东西」，不能判断观点对错；分高不等于判断成立。
- Semantic Fidelity 按锚点词组计数比对，只能发现锚点被删或被强化，不能确认修饰对象没换；脚本 PASS 后仍要做一次语义核对。
- Story Strength 只能判断具体度，不能判断场景是否真实；分数低时补事实，不补想象。

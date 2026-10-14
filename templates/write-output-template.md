# MODE A 输出模板（WRITE）

默认只交成稿，不输出内部扫描。

---

**【口播稿】**

（每行一句字幕，12–24 个中文字；段落之间空一行）

---

**【事实清单】**（可选，用户需要时输出）

- 数字 / 单位：
- 时间 / 尺度：
- 因果关系：
- 限制条件：
- 待核事实（如有）：

## 内部预检（不输出给用户）

- 写前五问 APSSV：Audience / Problem / Scene / Solution / Value 至少答出三项。
- 故事层四项自检：叙事主体、可看见的场景、一处状态变化、没有连续 4 句抽象。
- 说服腔命中 = 0（H 类 + Superiority Contrast + Overclaim Promise）。
- 讲清楚测试：删掉金句、反问、情绪词后，观点、因果与办法仍然成立。
- 价值链六问（v0.3.0）：真实问题 / 核心判断 / 事实或案例 / 实际影响 / 可执行动作 / 适用边界。
- 人格模式（v0.3.0）：DEFAULT_NATURAL / PRACTICAL_EXPLAINER / SLOW_ENTREPRENEURSHIP 三选一，默认第一个。
- 叙事 / 人物 / 纪录片 / 方法论类任务额外跑 `--story-gate`，要求 Story Strength ≥ 6。
- 方法论 / 商业 / 成长 / 创作者 / 工具 / 慢创业类额外跑 `--value-gate`，要求 Value Strength ≥ 6 且空泛价值句 = 0。

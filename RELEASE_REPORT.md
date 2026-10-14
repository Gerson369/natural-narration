# RELEASE REPORT v0.8.0

主题：First Draft Ready｜新选题第一稿就能直接用。纯文案处理范围不变。

- WRITE：首稿蓝图 → 按蓝图写 → 交稿前自审循环（结构 ≥85、自然度、证据边界、好句、凑节奏句），最多 3 轮，只交最终稿。
- 新脚本：nn_blueprint_check.py；nn_scan.py 新增 --protect，修正「已经+时长」误报。
- 回归：4 个首稿选题 RED 4/4 FAIL、GREEN 4/4 PASS；保真 7/7 + 7/7；旧回归 22/22。
- 详见 tests/RESULTS.md 与 CHANGELOG.md。

## v0.8.1

- 主线不能是题目本身（题目词行）；主线开头 / 中段 / 结尾贯穿；揭底节拍门禁。
- 首稿回归 5 个选题：RED 5/5 FAIL，GREEN 5/5 PASS；题目词作主线蓝图 FAIL。
- 不含第三方视频文本。


## v0.9.0 回归（2026-10-11）

- 保真 RED 7/7 FAIL，GREEN 7/7 PASS；旧回归 22/22。
- 结构诊断：GREEN 5/5 LOW；RED 4 个 HIGH、1 个 MEDIUM（ancient v0.6.1 CLEAN 稿 76，人工评 80，判 MEDIUM 更符合实际）。
- 主线即题目蓝图：给出「主线词与题目词重叠」风险提示，不再扣 40 分。
- 分数是诊断参考，不代表听感；尚未用真实新选题整篇验证。

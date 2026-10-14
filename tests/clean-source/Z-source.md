---
title: 导出报表
version: 2
---

# 导出报表

在进行数据导出操作之前，需要首先确认你的账号已经具备相应的导出权限。

<a id="limits"></a>

## 步骤

1. 运行 `python export.py --month 2026-09`。
2. 打开 `./out/report.csv` 检查列名。
3. 上传到[共享目录](https://example.com/share)。

| 字段 | 含义 |
| --- | --- |
| uid | 用户 ID |

```bash
python export.py --month 2026-09
```

---
name: kooai-selection-standalone
description: Use when a seller wants data-grounded Coupang product selection, category and review analysis, seven-gate screening, trend or season analysis, or a standalone visual report based on authenticated KooAI MCP data.
---

# KooAI 独立选品

## 核心原则

这是一个 MCP 辅助选品 Skill：只通过 KooAI MCP 查询 Coupang 商品、类目与评论，再把分析快照提交到本地页面查看、筛选和导出。事实、推断和缺失证据必须分开记录；关键证据不足时七关总体结论保持 `UNKNOWN`。

## 固定流程

1. 确认本次方向与卖家背景。背景会实质改变排序时再追问；否则按用户给出的范围直接查数。
2. 确认已配置 `kooai-market-data` MCP，且运行环境具有 `KOOAI_MCP_API_KEY`。Key 仅用于 MCP 鉴权，不读取、不打印、不写入命令参数、报告 JSON、SQLite、页面或日志。
3. 通过 MCP 查询 Coupang 商品、类目与评论。默认使用 T-1；根据问题自主选择工具和分页深度，证据足够回答问题后停止。记录每次调用的工具、`data_date`、来源和 warnings。认证、初始化或真实查询失败时停止，不生成伪报告。
4. 用类目与商品数据构造候选；评论、趋势和详情仅用于交叉验证。榜单只能用于候选发现或旁证，不能作为正式候选的唯一来源。复合关键词为零结果时，改用类目、价格和数值条件查询。
5. 执行机会面、趋势与季节、七关漏斗、新卖家进入难度、弱品牌与低评价壁垒、组合差异化等既有方法论。成熟爆款是需求证据，不等于新卖家机会。
6. 对七关分别记录结论、证据、原因、缺失数据、置信度和事实/推断。缺失竞争、评论、趋势或合规等关键证据时保留 `UNKNOWN`，并降级为观察或小批验证。
7. 阅读 [report-contract.md](references/report-contract.md)，生成 `standalone_selection_report:v1` JSON。报告必须含 `mcp_tools_used`、`data_snapshots`、`screening_funnel`、`ranking_usage`、`limitations`；候选应含 `category_name`、评分/评论摘要以及证据来源与 Skill 推断。
8. 在 cpdata 项目中运行 `apps/kooai-selection/start.sh`，确认返回 `http://127.0.0.1:8765`。端口被未知程序占用时停止，不结束未知进程。
9. 运行 `scripts/submit_report.py --base-url http://127.0.0.1:8765 <report.json>`，取得 `report_id`；再运行 `scripts/open_report.py <report_id>`。
10. 页面只展示当前报告快照：可按关键词、类目、价格、销量、评分、评价数、配送、七关结论和推荐状态筛选、排序，并导出当前可见行的 CSV/XLSX。

详细查询与排序顺序见 [workflow.md](references/workflow.md)。

## 快速检查

| 检查项 | 必须满足 |
|---|---|
| 数据边界 | 只通过带 Key 的 KooAI MCP，不直连 cpdata 数据库 |
| 数据内容 | 商品、类目与评论均记录实际来源和日期 |
| 日期 | 默认 T-1，页面与导出显示截止日 |
| 证据 | 缺关键数据时七关为 `UNKNOWN` |
| 分析模式 | `full_data` 可优先验证；`partial_evidence` 仅小批验证/观察；`exploratory` 仅观察 |
| 榜单角色 | 只能用于候选发现或旁证，不得单独产生正式推荐 |
| 页面 | 仅本地回环地址，无 KooAI 管理框架 |
| 密钥 | 不进入文件、命令参数、页面、SQLite 或日志 |

## 常见错误

- 先找爆款、后补卖家画像：重新从卖家诊断开始。
- 用商品行数计算火箭占比：改用非空唯一 `product_id`，同时单列观测行数。
- 将“字段存在”当成证据通过：检查有效值、阈值和缺失项。
- 本地 Python 服务自行调用 MCP：错误；Agent 调用 MCP 后仅向本地服务提交无密钥报告。

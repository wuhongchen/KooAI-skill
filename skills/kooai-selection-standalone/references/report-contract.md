# 独立选品报告契约

使用 `standalone_selection_report:v1`，最多 500 个候选，序列化后不超过 5 MiB。报告创建后是不可变快照。

## 顶层字段

```json
{
  "schema_version": "standalone_selection_report:v1",
  "report_id": "letters_numbers_dash_or_underscore",
  "title": "报告标题",
  "generated_at": "2026-08-10T10:00:00+08:00",
  "data_cutoff": "2026-08-09",
  "data_policy": "T-1",
  "data_source": "kooai-mcp",
  "analysis_mode": "partial_evidence",
  "analysis_summary": {
    "mcp_tools_used": ["search_categories", "analyze_category", "search_products"],
    "data_snapshots": [{
      "tool": "search_products",
      "data_date": "2026-08-10",
      "source": "database:products",
      "warnings": []
    }],
    "screening_funnel": [
      {"stage": "category_universe", "input_count": 6200, "output_count": 180},
      {"stage": "product_screen", "input_count": 180, "output_count": 24},
      {"stage": "seven_gate", "input_count": 24, "output_count": 5}
    ],
    "ranking_usage": "supporting_signal",
    "limitations": ["seller_concentration"]
  },
  "warnings": [],
  "active_filters": {},
  "merchant_profile": {},
  "products": [],
  "candidates": []
}
```

- `report_id`：`^[A-Za-z0-9_-]{1,160}$`，每次报告唯一。
- `generated_at`：ISO 8601 且带时区。
- `data_cutoff`：MCP 数据日期；不得用报告生成日冒充。
- `products`：用于覆盖和火箭拆分，保留 `product_id` 与 `delivery_badge`。
- `warnings`：周快照不完整、字段缺失、MCP 降级等可审计信息。
- `analysis_mode`：`full_data | partial_evidence | exploratory`。旧报告缺失时页面标为 `legacy`，不得伪装成 `full_data`。
- `analysis_summary.mcp_tools_used`：本次实际调用的 MCP 工具。
- `analysis_summary.data_snapshots`：各工具真实数据日期、来源和 warnings。
- `analysis_summary.screening_funnel`：各阶段输入、输出数量，数量必须为非负整数。
- `analysis_summary.ranking_usage`：`not_used | candidate_discovery | supporting_signal | primary_signal`。
- `analysis_summary.limitations`：未能取得或未验证的证据。

## 候选字段

每个候选至少包含：

- `candidate_id`、`product_id`、韩文/中文名称、图片与 Coupang HTTP(S) 链接。
- 售价、近 28 天销量/PV、火箭类型、机会分和推荐等级。
- `selection_reason` 与 `validation_action`。
- 竞争水平、评价壁垒；没有证据时填 `UNKNOWN`。
- `seven_gate_summary`。

候选还应记录分析溯源：

```json
{
  "recommendation_state": "small_batch",
  "evidence_sources": [{
    "tool": "search_products",
    "data_date": "2026-08-10",
    "metrics": ["sales_last_28d", "pv_last_28d"]
  }],
  "skill_inferences": [{
    "claim": "可做尺寸组合",
    "reason": "存在多个使用场景",
    "confidence": "medium"
  }]
}
```

`recommendation_state` 使用 `validate | small_batch | observe`。`evidence_sources` 只列实际 MCP 证据；`skill_inferences` 必须保留推断理由与置信度，不能伪装成事实。

图片仅接受绝对 HTTP(S) URL。MCP 返回 `cache/...` 等相对路径时，`image_url` 必须为空，并在报告 `warnings` 中记录图片证据缺失。

## 七关字段

```json
{
  "decision": "UNKNOWN",
  "gates": [{
    "gate_key": "competition",
    "label": "竞争壁垒",
    "decision": "UNKNOWN",
    "evidence": "",
    "reason": "缺少卖家集中度",
    "missing_data": ["seller_concentration"],
    "confidence": "low",
    "fact_or_inference": "fact"
  }]
}
```

关卡使用 `PASS | CONDITIONAL | FAIL | UNKNOWN`。总体优先级是 `FAIL`，其次是任何关键 `UNKNOWN`，再是 `CONDITIONAL`，全部通过才是 `PASS`。

## 火箭口径

本地服务按非空唯一 `product_id` 计算分母，并单独展示 `observed_row_count`。配送类型保留蓝色、橙色、生鲜、海淘、卖家火箭与其他/未知，不得合并成单一“火箭占比”。

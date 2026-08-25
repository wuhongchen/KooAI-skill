# KooAI Skills

面向 Coupang 卖家的公开 KooAI Skills 集合，用于市场数据查询、选品分析与本地报告生成。

## Coupang 是什么

[Coupang（酷澎）](https://www.coupang.com/) 是韩国电商平台。本仓库中的 Skill 聚焦跨境卖家常见的调研问题：类目与商品表现、价格带、买家评论、关键词、竞品，以及进入某个细分市场前的选品判断。

本仓库与 Coupang 没有隶属或官方合作关系；任何商品、销量、价格或评价分析都应以数据截止日和实际可访问范围为准。

## KooAI 是什么

[科跃 KOO AI](https://www.kooai.top/) 是面向 Coupang 卖家的数据查询、选品与运营分析平台。科跃助手用于在浏览器页面中查看和采集可访问的信息；KOO AI 工作台用于商品、类目、关键词与经营主体的复盘分析。公开数据会标注 T-1 或实际缓存截止日，适合选品判断和横向比较，不等同于 Coupang 官方结算或财务口径。

本仓库沉淀的是可复用的 AI Skill，而不是 KooAI 的后台代码、数据库或账号系统。

## 已收录 Skill

| Skill | 用途 |
| --- | --- |
| `kooai-selection-standalone` | 使用已认证的 KooAI MCP 查询 Coupang 类目、商品与评论；通过七关漏斗和机会分筛选候选；生成可筛选、可导出的本地选品报告。 |
| `kooai-1688-sourcing` | 将 Coupang 候选的规格与搜索意图交给已安装的 `1688-product-find` 执行文本、图片或链接找货；保留货源、SKU、MOQ 与成本证据边界。 |

## 安装 Skill

克隆仓库及其第三方源码依赖后，把所需 Skill 安装到 Codex 的全局 Skills 目录：

```bash
git clone --recurse-submodules https://github.com/wuhongchen/KooAI-skill.git
python3 KooAI-skill/skills/kooai-selection-standalone/scripts/install.py --dry-run
python3 KooAI-skill/skills/kooai-selection-standalone/scripts/install.py
python3 KooAI-skill/skills/kooai-1688-sourcing/scripts/install.py
```

`kooai-1688-sourcing` 是适配层，首次使用前还需安装原作者维护的找货实现：

```bash
npx skills add next-1688/1688-product-find --skill 1688-product-find
```

安装后重启或新开 Codex 会话，可使用 `$kooai-selection-standalone` 调用选品 Skill，或使用 `$kooai-1688-sourcing` 调用 1688 找货适配流程。

## 报告规范

[选品报告 V2 规范](docs/selection-report-v2.md) 定义了面向卖家决策的报告字段、1688 成本证据、统一算价边界、中文判断和淘汰商品展示规则。它是后续独立报告页与导出功能的统一契约；数据不足时必须展示待核验状态，不得编造价格或利润。

## 数据与安全边界

- KooAI MCP 是数据来源；Skill 不得嵌入、打印或保存 API Key、OAuth 令牌、Cookie 或数据库凭据。
- 独立选品 Skill 只将不含凭据的报告快照写入本地回环页面。
- 1688/Ego 查询是用户明确发起的候选级补充动作；页面展示价只是供货线索，不是已确认的采购成本。
- `1688-product-find` 的代码以 Git 子模块固定到 `third_party/1688-product-find`；其 AK 和服务由原作者维护，KooAI 不代理其请求，也不保存其凭据。

## 第三方源码依赖

`third_party/1688-product-find` 指向 [next-1688/1688-product-find](https://github.com/next-1688/1688-product-find) 的固定提交，不是 KooAI 自有实现。首次克隆遗漏子模块时执行：

```bash
git submodule update --init --recursive
```

上游源码的许可、服务条款、更新与安全边界以原仓库为准；KooAI 的 MIT 许可证不覆盖该子模块。详情见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 仓库结构

```text
skills/<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
third_party/
└── 1688-product-find/  # 上游 Git 子模块
```

后续新增的公开 Skill 应保持自包含，不携带私有项目数据，并沿用该目录结构。

## 许可证

采用 MIT License，详见 [LICENSE](LICENSE)。

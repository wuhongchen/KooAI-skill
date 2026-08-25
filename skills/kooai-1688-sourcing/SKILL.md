---
name: kooai-1688-sourcing
description: Use when a KooAI seller needs to turn Coupang candidate specifications into evidence-bound 1688 sourcing searches, matching prices, MOQ, and supplier links through an installed 1688-product-find Skill.
---

# KooAI 1688 找货适配

## 目的

把已有的 Coupang 候选（标题、用途、材质、尺寸、数量和套装关系）转成可追溯的 1688 找货任务。此 Skill 是 `1688-product-find` 的 KooAI 工作流适配层，不修改其实现；KooAI 仓库通过 `third_party/1688-product-find` Git 子模块固定其上游源码版本。

## 前置条件

1. 确认本机已安装 `1688-product-find`。未安装时，提示用户执行：

   ```bash
   npx skills add next-1688/1688-product-find --skill 1688-product-find
   ```

   如使用 KooAI-skill 的源码仓库进行审计或开发，先执行 `git submodule update --init --recursive` 取得固定版本的上游源码。

2. 使用前读取已安装 `1688-product-find` 的 `SKILL.md` 及与本次命令对应的 reference；其 AK、调用限制、授权方式和错误处理以原 Skill 为准。
3. 不读取、打印、写入报告或代为保管 AK、令牌、Cookie、密码或其他凭据。

## 工作流

1. 从 Coupang 候选提取核心用途、材质、尺寸、数量、包装与必需规格；去掉品牌名、营销词、乱码和无关属性。
2. 生成简体中文搜索词。先用文本搜索；用户提供商品图片或明确要求同款时，才用图片/链接搜索。用户明确要比较价格时才用原 Skill 的 `compare`。
3. 把原 Skill 返回的完整商品表保留为货源原始证据；另建立候选映射表，至少包含：
   - Coupang 产品 ID 与链接
   - 1688 搜索词、商品标题与详情链接
   - 页面展示价、币种、MOQ、SKU/规格、供应商
   - 规格匹配依据、观察时间、货源状态
   - 成本证据等级：`display_reference`、`matched_estimate` 或 `confirmed_cost`
4. 只有用途、关键材质/尺寸、数量或套装关系、SKU 与 MOQ 已基本对应时，才标记 `matched_estimate`。页面展示价不是最终采购成本。
5. 将 `confirmed_cost` 或明确标注为预估的 `matched_estimate` 交给 KooAI 的统一算价模块；任何缺失物流、包装、税费或 SKU 的成本不应得出“可盈利”结论。

## 边界与停止条件

- 原 Skill 未配置 AK、调用报错、限流或授权失败时，按原 Skill 指引停止；不得以浏览器、搜索引擎或猜测价格替代。
- 本 Skill 不下单、付款、管理库存或绕过登录、验证码和访问控制。
- 无法确认规格、MOQ 或套餐关系时，标记 `相似候选` 或 `待人工核验`，而不是声称已匹配。
- 1688 原始结果、Coupang 数据和 KooAI 算价必须在最终表格中保持来源、时间与证据等级可追溯。

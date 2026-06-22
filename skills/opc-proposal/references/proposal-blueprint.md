# OPC Dynamic Proposal Blueprint

Use this blueprint when the user asks for a complete marketing proposal, 4A-level proposal, campaign plan, annual/launch plan, or `$opc-proposal`.

This is the strategy-completeness base, not a fixed output table of contents. The final Markdown structure must be dynamically fused with the user's current business priority and any relevant workflow pattern such as `douyin-commerce-pattern.md`.

## Dynamic Output Principle

1. Confirm the user's current priority before structuring the document.
2. Keep the full strategic logic: objective, insight, challenge, strategy, creative idea, content, KOL/media, budget, KPI, timeline and task order.
3. Reorder chapters by the current focus. Campaign-first, live-first, store-first, KOL-first and research-only tasks should not share the same chapter order.
4. Keep complete, detailed content by default so the user can later delete or shorten sections.
5. Output a Markdown `.md` document unless the user explicitly asks for another deliverable.

## Strategy Completeness Modules

Use these modules to check that a full proposal is not missing strategy logic. Merge them into the final structure rather than listing them as a separate 16-module section.

### 1. 执行摘要
- 项目名称、品牌、产品/品类、周期。
- 一句话策略判断。
- 最大机会、最大风险、推荐方向。

### 2. Brief 解构与目标校准
- 已知信息、关键矛盾、业务目标、传播目标、转化目标。
- Brief 质量评级 A/B/C。

### 3. 信息缺口与工作假设
| 优先级 | 缺失信息 | 为什么重要 | 建议追问 | 暂行假设 | 能否先推进 |
|---|---|---|---|---|---|

### 4. 数据来源与证据口径
- 本地资料、网络资料、参考案例、会议纪要和假设。
- 用资料来源矩阵说明每个板块的数据依据。

### 5. 行业趋势与市场机会
- 市场方向、增长驱动力、消费变化、监管/合规风险。
- 为什么现在值得做。

### 6. 品类格局与竞品分析
- 子品类结构、价格带、搜索/内容需求、渠道流量结构。
- 竞品定位、Hero 产品、价格带、核心卖点、渠道、内容/KOL、近期动作、启示。

### 7. 品牌与产品/货盘诊断
- 品牌资产、信任状、RTB、当前弱项。
- Hero SKU、引流 SKU、利润 SKU、组合策略、合规表达。

### 8. 消费者洞察
- 核心人群、机会人群、痛点、欲望、购买障碍。
- 内容触发点、信任建立点、转化钩子。

### 9. 核心挑战与策略方向
- 一句话挑战。
- 核心主张、差异化、策略逻辑、胜出理由。
- 目标人群、核心场景、关键证据链。

### 10. 创意主题与表达系统
- Campaign 主题、主题解读、创意领地。
- 主视觉方向、文案调性、内容支柱、禁区。

### 11. 业务落地方案
- 根据用户优先级放入直播、抖店、商品卡、千川、KOL、媒介、Campaign、TVC、私域、线下等模块。
- 首要业务写深，支撑业务写清，不平均用力。

### 12. 内容矩阵
| 阶段 | 目标 | 内容角度 | 形式 | 渠道 | 关键素材 | KPI |
|---|---|---|---|---|---|---|

### 13. KOL / 达人 / 媒介
- 达人层级、垂类、人设标签、粉丝画像、内容风格。
- 筛选条件、风险过滤、brief 方向、验收标准。
- 媒介角色、预算角色、KPI、优化杠杆。

### 14. 预算分配与 KPI 框架
- 预算已知：按金额和占比分配。
- 预算未知：给保守/标准/进攻三档。
- KPI 分层：曝光、互动、搜索/种草、流量、转化、效率、长期资产。

### 15. 执行时间表与复盘机制
- 按阶段或自然月展开。
- 里程碑、依赖关系、验收节点、复盘指标。

### 16. 下游任务单、风险与来源索引
- 任务、负责人角色、输入材料、输出物、验收标准、依赖、截止时间。
- 风险、影响、触发信号、应对。
- 来源、计算、推断、免责声明。

## Dynamic Chapter Examples

- Live-first: 数据洞察 -> 产品/货盘 -> 抖音全局策略 -> 直播 -> 商品卡/千川 -> KOL/Campaign -> 月度计划 -> 任务单。
- Campaign-first: 数据洞察 -> 消费者/情感内核 -> 品牌策略 -> Campaign/TVC -> KOL/媒介 -> 内容矩阵 -> 转化承接 -> 月度计划。
- Store/product-card-first: 数据洞察 -> 关键词/价格/人群 -> 商品卡/店铺 -> 主图详情页 -> 搜索/推荐流量 -> 内容和投放承接 -> 任务单。
- Research-only: 资料口径 -> 行业 -> 价格 -> 人群 -> 关键词 -> 竞品 -> 机会判断 -> 信息缺口。

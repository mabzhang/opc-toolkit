# OPC Intake Confirmation Template

Use this before starting any substantial OPC task. The goal is to understand, analyze, organize, and confirm the user's need before research or proposal writing. The confirmation must be detailed enough that data sources, business focus, audience, scope, and output depth are explicit.

## Rules

1. Do not begin full research, analysis, or proposal writing before sending a confirmation note and getting user confirmation.
2. First restate the user's request in organized form, then ask only questions that materially affect the work.
3. Default final deliverable is a Markdown `.md` document. If the user asks for PPT or another format, treat it as an additional deliverable.
4. Prioritize local uploaded or user-specified files. Do not replace local data with public web data.
5. For each analysis block, confirm the data source mode: `仅本地上传`, `仅网络公开`, `本地为主+网络补充`, or `网络为主+本地校验`.
6. For local-covered topics, do not use web data unless the user allows it. For topics not covered by local files, ask whether web search is allowed or state the limited assumption.
7. Confirm audience and purpose: who will read it, what decision it must support, and how polished/actionable it must be.
8. If the user asks for iteration based on an old proposal, identify the old proposal as framework reference and the meeting notes/revision points as correction priority.
9. Default depth is full and detailed: provide enough content for later deletion and trimming, rather than a thin outline.

## Standard Confirmation Note

```markdown
我先确认一下任务口径。确认后我再开始正式分析和写 `.md` 方案。

## 1. 我理解的具体需求
- 品牌/产品/品类：
- 平台/渠道：
- 这次真正要解决的问题：
- 当前状态：
- 时间范围：
- 最终交付：Markdown 完整方案（`.md`）

## 2. 业务优先级
| 业务板块 | 本次优先级 | 是否重点深化 | 我理解的原因 |
|---|---|---|---|
| 行业/品类分析 |  |  |  |
| 竞品分析 |  |  |  |
| 消费者/人群洞察 |  |  |  |
| 直播 |  |  |  |
| 抖店/店铺运营 |  |  |  |
| 商品卡/搜索SEO |  |  |  |
| 千川短视频/图文 |  |  |  |
| KOL/KOC/达人 |  |  |  |
| 媒介投放 |  |  |  |
| 品牌 Campaign |  |  |  |
| TVC/创意内容 |  |  |  |
| 年度/月度节奏 |  |  |  |
| 预算/KPI/任务单 |  |  |  |

## 3. 本地资料清单与用途
| 资料 | 我理解的用途 | 优先级 | 注意事项 |
|---|---|---|---|
| [文件名] | [产品/数据/会议/旧方案/竞品/品牌资料] | [高/中/低] | [只借鉴框架/作为事实依据/优先覆盖旧口径] |

## 4. 资料来源矩阵
请确认每个板块的数据来源方式：

| 分析板块 | 建议资料来源 | 是否允许联网 | 联网范围/限制 | 备注 |
|---|---|---|---|---|
| 行业分析 | [仅本地上传/仅网络公开/本地为主+网络补充/网络为主+本地校验] | [是/否] |  |  |
| 竞品分析 |  |  |  |  |
| 消费者/人群 |  |  |  |  |
| 关键词趋势 |  |  |  |  |
| 价格段/客单价 |  |  |  |  |
| 直播策略 |  |  |  |  |
| 商品卡/标题/主图 |  |  |  |  |
| 千川/短视频/图文 |  |  |  |  |
| KOL/KOC/达人 |  |  |  |  |
| 品牌 Campaign |  |  |  |  |
| TVC/创意分镜 |  |  |  |  |
| 预算/KPI |  |  |  |  |

默认规则：本地资料已覆盖的部分，以本地资料为主；没有你授权，不用网络公开数据替代本地数据。本地没有覆盖但方案必须补充的部分，我会先标出并请你确认是否联网。

## 5. 给谁看、用于什么目的
- 阅读对象：
- 使用场景：
- 希望对方看完后做出的决策：
- 方案风格：完整、详细、可删减，不主动简化关键模块

## 6. 必须聚焦和不要跑偏
- 必须聚焦：
- 第二优先级：
- 不展开/弱化：
- 不能误用的资料或口径：
- 参考案例使用方式：

## 7. 我会重点分析的内容
- 数据：先按每个 sheet 分析，再汇总行业判断。
- 趋势：年份对比、按月、节点、价格段、人群、关键词迁移。
- 策略：根据本次业务优先级动态排序，不默认直播第一。
- 落地：标题、脚本、场景、素材、KOL、预算、KPI、任务单、风险、数据来源索引。

## 8. 需要你确认的问题
1. [会影响业务主次的问题]
2. [会影响资料来源的问题]
3. [会影响输出深度或边界的问题]

如果以上理解没问题，我会按这个口径开始。
```

## User-Style Request Template

Use this when the user wants a reusable prompt template.

```markdown
请基于我提供的资料，帮我完成一份【品牌/产品/品类】在【平台/渠道】的【方案类型】，最终输出为 Markdown 完整方案。

【项目背景】
- 品牌/产品：
- 当前状态：
- 本次想做的业务：
- 业务优先级：例如【直播第一 / 品牌Campaign第一 / 商品卡第一 / 千川第一 / KOL媒介第一 / 其它】
- 项目时间：

【资料说明】
- 文件1《》：这是【产品/行业/会议/旧方案/竞品】资料，主要用于【用途】。
- 文件2《》：这是【数据文件】，请先按每个 sheet 分别分析，再汇总。
- 文件3《》：这是参考方案，只借鉴【框架/模块/写法】，不要完全照搬。
- 文件4《》：这是会议纪要/修改意见，优先级高于旧方案。

【资料使用规则】
- 已上传资料能覆盖的部分，优先使用本地资料。
- 如果我没有明确要求，不要用公开网络数据替代本地数据。
- 请在开始前按板块确认资料来源：仅本地上传 / 仅网络公开 / 本地为主+网络补充 / 网络为主+本地校验。
- 本地资料没有覆盖但方案必须补充的部分，可以/不可以联网搜索；如可以，请只搜索【指定范围】，并标明来源和日期。

【分析要求】
- 数据要先拆开看，再汇总：每个 sheet 分析一次。
- 价格段：做【年份A】 vs 【年份B】汇总对比，并按月看客单价/高客单节点。
- 人群：做【年份A】 vs 【年份B】趋势对比，指出核心人群和增长人群。
- 关键词：不要只列 Top 词，要看趋势迁移、关注点变化、产品可发力关键词。
- 竞品：必须说明来源，不确定的标注推断，不要凭空写。
- 所有策略动作要回扣数据节点和人群，不要写空泛建议。

【方案必须包含】
- 当前行业是什么样子的。
- 基于行业和数据，本次重点业务该怎么做。
- 如果涉及直播：直播间定位、排品、场景、话术、绿幕/实景方向、测试路径。
- 如果涉及店铺/商品卡：标题、关键词、主图、详情页、SEO、体验分。
- 如果涉及千川/内容：短视频怎么拍、图文怎么拍、文案和内容矩阵怎么设计。
- 如果涉及品牌 Campaign：策略、主题、节点、KOL预算、传播路径。
- 如果涉及 TVC：方向和分镜，必须贴合节点和人群。
- 【月份A】到【月份B】共【N】个月自然月节奏规划。
- 预算、KPI、执行任务单、风险和数据来源索引。

【重点修改/深化】
1. [问题1]
2. [问题2]
3. [问题3]

【输出要求】
- 输出为 Markdown 完整方案 `.md`。
- 不要简略，关键模块要写细，方便我后期删改缩减。
- 结构要有逻辑：数据洞察 -> 机会判断 -> 策略 -> 执行动作 -> 排期/预算/KPI。
- 最终文件命名为：【MMDD-项目-内容-版本】。
```

## Critical Questions To Ask

Ask these only when missing and material:
- Exact product/category focus. Example: a source file may contain multiple products, but the proposal may need to focus only on 电饭煲.
- Business priority order. Do not infer live commerce is always first from prior cases.
- Time window and launch month.
- Which old proposal is framework reference and which file is revision priority.
- For each major block, whether data should be local-only, web-only, local-led with web supplement, or web-led with local validation.
- Whether output is for client pitch, internal strategy, execution team, or boss review.
- Required depth: quick direction, full proposal, or execution-ready plan. Default is full and detailed.

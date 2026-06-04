---
name: write-data-platform-prd
description: Write product requirement documents for data platforms, business middle platforms, admin backends, dashboards, query pages, export tasks, monitoring reports, metric dictionaries, permission control, and operational data products. Use when Codex needs to turn business data needs into a backend/data-platform PRD rather than a pure data extraction request.
---

# Write Data Platform PRD

## Purpose

Turn business data needs into a structured Chinese PRD for a data platform or admin backend.

Use this skill for product requirements such as dashboards, data query pages, export tasks, monitoring reports, metric dictionaries, permission rules, UI interactions, and acceptance tests.

Do not use this skill for pure data field translation. For pure extraction fields, metric口径, or Excel headers, use `translate-betting-data-request`.

## Relationship With Data Requirement Skill

Keep the two skills separate:

- `translate-betting-data-request`: produce data-platform-ready取数需求, field lists, metric definitions, and Excel headers.
- `write-data-platform-prd`: produce PRD-style product requirements, including backend pages, user flows, controls, permissions, export tasks, exceptions, and tests.

If a PRD needs fields or metrics, include them as product display requirements. Do not over-expand metric口径 unless the user asks for data details.

## Core Workflow

1. Identify the product scenario: dashboard, detail query, export task, monitoring report, metric dictionary, alerting, permission management, or a combined module.
2. Extract the business pain point: what the current process cannot do, what is manual, what is slow, what causes repeated data requests.
3. Define the product objective in operational terms: centralized viewing, self-service query, linked drill-down, export, monitoring, or口径 consistency.
4. Convert the business need into backend functions: menu, filters, cards, charts, tables, detail pages, export, permissions, logs, and exceptions.
5. Separate functional requirements, data display rules, interaction rules, permission rules, data update rules, and acceptance tests.
6. When details are missing, mark as `待确认` instead of inventing them.

## Pain Point Intake

When the user provides business chat records, screenshots, or an attachment as the initial pain point, first produce a compact intake summary before expanding the PRD:

- 原始业务诉求: summarize what the business is asking for in plain language.
- 当前中台缺口: identify what the current backend cannot query, calculate, display, or export.
- 业务计算逻辑: capture formulas or examples provided by business.
- 已提供字段: extract fields from documents or screenshots.
- 建议补充能力: map the gap to backend features such as query page, dashboard, export, metric dictionary, or report.
- 待确认问题: ask only questions that affect function scope, formula, fields, permissions, or delivery.

If the business request is about adding a calculated cost/profit field, keep the feature focused on that calculation and its supporting fields. Do not expand into unrelated dashboards or metrics unless the user asks for a broader module.

## Default Internal Output Format

By default, match the user's concise internal handoff format rather than a long formal PRD. Use the comprehensive PRD structure only when the user asks for a full PRD or the feature is broad.

Use this short-form structure for ordinary backend/data-platform needs:

```text
[需求名称]

任务
1. 业务了解：[解释业务概念或活动机制]
2. 业务需求了解：[说明当前中台缺口和业务要补充的能力]
3. 业务需求翻译成需求文档（明细）
4. 推进落地

需求背景
[说明当前后台/中台已有能力、缺失能力，以及为什么需要新增]

需求目的
[说明补充该功能后解决什么问题，如完善成本核算、支持日常监控、自助查询、减少临时取数]

明细
归为[一级菜单/栏目]下
- 二级页面：[汇总/日报/看板页面名称]
- 三级页面：[明细/发放/用户/订单页面名称]

[二级页面名称]
[说明页面用途，例如：以表格支持单日总览]
筛选项：[筛选字段，用 / 分隔]
展示字段：[汇总表字段，用 / 分隔；如未明确则标记待确认]

[三级页面名称]
[说明页面用途，例如：展示订单/用户/发放明细]
[用表格列出明细表头]

[数据字段]
| 字段 | 说明 |
| --- | --- |
| ... | ... |
```

For calculated fields, include the business example and formula in the field explanation or a short口径说明. Example:

```text
实际加奖成本 = 实际派奖 - 按原始赔率计算的应返奖
示例：下注100，原始赔率10，原始应返1000；实际派奖1200，则实际加奖成本为200。
```

## Standard PRD Structure

Use this comprehensive section order only when the user asks for a full PRD, when the feature is large, or when QA/engineering needs complete acceptance detail:

```text
一、需求背景
二、需求目标
三、需求范围
四、用户角色与使用场景
五、功能需求
六、页面与交互规则
七、数据规则与指标说明
八、权限控制
九、数据导出
十、异常状态与边界规则
十一、数据更新与性能要求
十二、验收标准 / 测试点
十三、待确认问题
```

## Functional Requirement Patterns

### Dashboard

For a data dashboard, specify:

- menu path and page name
- default page state
- filters and default filter values
- overview metric cards
- trend charts
- summary table
- drill-down entry
- refresh frequency
- export capability

Common dashboard components:

- 指标卡片: show core metrics and optional同比/环比.
- 趋势图: show key metric trends by date.
- 汇总表: show aggregate data by date, country, activity, user segment, or reward.
- 明细入口: navigate from aggregate rows to detailed query pages.

### Query Page

For a backend query page, specify:

- searchable fields
- required and optional filters
- result table fields
- pagination
- sorting
- reset/search buttons
- detail button
- permission-limited columns

Default pagination: support 10/20/30/50 rows per page, default 30 rows per page, unless the user gives another standard.

### Export

For export requirements, specify:

- export scope: current filtered results, selected rows, or full result set
- export type: detail export or summary export
- file type: Excel by default
- field selection: fixed fields or configurable fields
- task mode: synchronous for small data, asynchronous task for large data
- task list fields: task ID, module, submitter, submit time, filter conditions, status, generated time, download link, failure reason

### Monitoring and Alerts

For monitoring features, specify:

- monitored object: activity, country, user segment, reward, metric, or user group
- monitored metric
- threshold rule
- refresh frequency
- alert channel if provided
- alert status and handling record if the backend needs closed-loop tracking

### Metric Dictionary

For metric口径 management, specify:

- metric name
- business definition
- calculation formula
- applicable scenario
- default display or not
- permission level
- owner
- update time

## Data and Metric Rules

- Keep product documents focused on what the backend should display and support.
- Include precise formulas only when the user asks for metric口径 or when the formula is essential to the product.
- Do not introduce unrelated product lines or metrics. For example, if the activity is clearly sports-only, do not add game/casino fields.
- Include NGR, GR, cost, ROI, or profit only when the business explicitly asks for cost/profit/cash-flow analysis.
- Mark sensitive identifiers such as username and userid as permission-controlled fields when included.

## Page and Interaction Rules

For every page, define:

- page title
- entry path
- filters
- default data range
- table columns
- button actions
- sorting rules
- pagination rules
- drill-down or return behavior
- empty state
- loading state
- error state
- latest data update time if data is periodic

## Permission Rules

Consider these permission types:

- menu permission
- country or region permission
- activity permission
- field permission for sensitive fields
- export permission
- admin/configuration permission

State permission rules as product requirements, not legal advice.

## Acceptance Test Patterns

Include tests for:

- menu entry and page navigation
- filter linkage and reset
- table display, sorting, and pagination
- metric calculation and source-data consistency
- drill-down consistency between aggregate and detail pages
- export format, fields, encoding, and row count
- permission isolation by role/country/activity
- update frequency and latest update time
- empty, loading, timeout, and error states
- performance for common large-range queries

## Writing Style

- Write as a product manager preparing a backend PRD for engineering, QA, data platform, and business stakeholders.
- Be concrete and implementable.
- Prefer numbered sections and concise tables.
- Avoid turning every PRD into a data extraction sheet.
- When the user provides a finished internal process, preserve that process and adapt the skill to it.

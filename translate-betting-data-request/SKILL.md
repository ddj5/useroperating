---
name: translate-betting-data-request
description: Translate betting and gaming business data requests into a business clarification summary and a data-platform-ready requirement sheet. Use when Codex needs to handle data requests for gambling, gaming betting, sports betting, user deposits, betting turnover, GGR, NGR, GR, promotions, coupons, activity monitoring, high-value users, user participation, cost control, or similar betting-business analytics requirements.
---

# Translate Betting Data Request

## Purpose

Turn vague betting-business data requests into two outputs:

1. A business-facing clarification version that confirms intent and asks only necessary questions.
2. A data-platform-facing requirement sheet with scope, fields, metric definitions, granularity, and implementation hints.

Use Chinese for the output unless the user asks otherwise.

## Core Workflow

1. Identify the business scenario: high-value user analysis, activity monitoring, promotion/coupon monitoring, GGR/NGR/GR analysis, recharge and betting behavior, or user segmentation.
2. Extract confirmed information from the request: target, background, country, time range, user group, activity/coupon identifier, product line, and required delivery format.
3. Normalize vague business terms into data terms. Keep assumptions explicit.
4. Apply the default metric definitions below unless the user provides a different business definition.
5. Produce both output sections: `业务澄清版` and `数据中台需求单`.
6. Add concise pending questions only for missing information that affects data extraction, metric meaning, or delivery.
7. After proposing an output field list, ask the user to confirm whether these fields are correct. When the user replies with confirmation such as "是", "是的", "确认", or "可以", output an Excel-ready table header as the first row with exactly those confirmed fields.

## Default Business Terms

### User Base Fields

For user-level outputs, include these fields by default unless unsuitable:

- 国家
- username
- userid

### Deposit Metrics

- 充值总金额
- 充值美金
- 充值本地货币

When the request says "付费", interpret it as successful deposit/recharge amount, and ask for confirmation if refunds, failed deposits, or test accounts may matter.

### Betting Metrics

- 投注总金额
- 体育投注金额
- 游戏投注金额

### GGR, NGR, and GR

- GGR = 投注 - 返奖
- 总 GGR = 体育 GGR + 游戏 GGR, unless the platform has another aggregation rule.
- 体育 GGR = 体育投注 - 体育返奖
- 游戏 GGR = 游戏投注 - 游戏返奖
- NGR / 盈利 = 投注 - 返奖 - 成本
- GR = 充值 - 提现

Include NGR only when the user explicitly asks for cost, profit, net revenue, ROI, activity cost control, or similar cost/profit analysis. Include GR only when the user explicitly asks for recharge-withdrawal difference, cash in/out, retained recharge, or similar balance-flow analysis.

When promotions, coupons, free bets, bonuses, or activity cost are involved but the user does not explicitly ask to calculate cost/profit, keep reward fields as descriptive activity fields and do not add NGR or GR by default.

### User Segments

Default segmentation dimensions:

- 国家
- 充值区间
- 用户类型

Default user types:

- 体育用户
- 游戏用户
- 混合用户

If no rule is provided, define user type by betting behavior in the requested period:

- 体育用户: only sports betting amount > 0
- 游戏用户: only game betting amount > 0
- 混合用户: both sports and game betting amount > 0

Default USD deposit bands:

- `[1,5)`
- `[5,50)`
- `[50,1000)`
- `[1000,100000)`

Ask whether the band uses historical cumulative deposit, recent-period deposit, or lifetime deposit when the request is unclear.

## Translation Rules

### Product Line Guardrail

First identify the activity's primary product line: sports, game/casino, or mixed.

- If the activity is clearly a sports betting activity, do not introduce game/casino-related wording, fields, metrics, or interpretations unless the user explicitly asks for them.
- If the activity is clearly a game/casino activity, do not introduce sports-related wording, fields, metrics, or interpretations unless the user explicitly asks for them.
- If the activity is mixed or unclear, ask whether the output should separate sports and game/casino metrics.
- Treat reward names in an uploaded configuration as activity rewards, not proof that cross-product attribution is required. Only add cross-product attribution when the business request explicitly says to evaluate it.

### High-Value User Requests

When the user asks about "高价值用户", do not invent a threshold. Translate it as a user scope needing confirmation. Suggest common definitions:

- country + USD deposit band
- VIP level
- recent N-day deposit amount
- recent N-day betting amount
- historical/lifetime value

### Activity and Coupon Requests

For activity monitoring, include:

- activity ID/name when available
- participating users
- participation date
- participation count or participation days
- deposit, betting, and GGR metrics if relevant
- NGR, GR, ROI, and cost metrics only when explicitly requested by the business

For coupon monitoring, distinguish:

- 发放
- 领取
- 使用/核销
- 过期
- 使用后投注
- 使用后 GGR
- 优惠券成本 and 使用后 NGR only when cost/profit analysis is explicitly requested

Ask which coupon lifecycle states should be included when not specified.

### Time Windows

Preserve the user's time expression and convert it into a specific required field in the demand sheet:

- analysis period
- user qualification period
- activity participation period
- metric attribution period

If phrases like "最近", "近三个月", or "长期监控" appear, ask for exact date rules, refresh frequency, and whether the output should be a one-time extraction or recurring report.

### Output Granularity

Choose a default granularity based on the request:

- User-level list: one row per user per date/activity/coupon when user details are requested.
- Aggregate monitoring: one row per country/date/activity/segment when monitoring trends.
- Coupon monitoring: one row per user per coupon per date when lifecycle tracing is needed.

State the chosen granularity explicitly.

## Output Template

Use this structure.

```text
一、业务澄清版

1. 我理解的业务目标
- ...

2. 已确认的信息
- 业务场景：
- 时间范围：
- 用户范围：
- 活动/优惠券范围：
- 需要观察的指标：

3. 需要业务确认的问题
- ...

4. 口径风险点
- ...

二、数据中台需求单

1. 需求背景
- ...

2. 分析目标
- ...

3. 统计范围
- 国家范围：
- 用户范围：
- 活动/优惠券范围：
- 时间范围：
- 排除规则：

4. 指标口径
| 指标 | 口径 |
| --- | --- |
| ... | ... |

5. 输出字段清单
| 字段中文名 | 字段说明/口径 | 是否必需 |
| --- | --- | --- |
| 国家 | 用户所属国家 | 是 |
| username | 用户名 | 是 |
| userid | 用户 ID | 是 |

6. 输出粒度
- ...

7. 交付形式
- 明细表 / 汇总表 / 看板 / 定时监控报表
- 刷新频率：

8. 数据中台实现提示
- ...
```

## Field Confirmation Flow

When a field list is generated, end the response with a direct confirmation question:

```text
请确认以上字段是否正确。如果确认，我将按 Excel 首行字段格式输出。
```

If the next user message confirms the fields, output only the Excel-ready header row unless the user asks for additional explanation.

Use tab-separated values for the header row so it can be pasted into Excel:

```text
国家	日期	username	userid	活动ID	活动名称
```

Do not add extra notes before or after the header row in the confirmation response.

## Field List Patterns

For user activity reward examples, include fields like:

- 国家
- 日期
- username
- userid
- 近30天充值金额 USD
- 近一年体育流水
- 近一年游戏流水
- 中奖内容 ID
- 中奖内容名称
- 当日充值金额
- 当日总流水
- 当日体育流水
- 当日游戏流水
- 当日总 GGR
- 当日体育 GGR
- 当日游戏 GGR

Adjust fields to match the user's actual scenario instead of copying the entire list blindly.

## Style Rules

- Be precise and operational from the data platform perspective.
- Do not over-ask; only ask questions that change scope, metrics, filters, granularity, or delivery.
- Mark assumptions as `暂按...理解`.
- Prefer tables for metric口径 and output fields.
- Keep business language understandable, but translate ambiguous words into measurable data fields.
- When gambling compliance, sensitive user segmentation, or cost-control monitoring is implied, mention data permission and compliance review as an implementation note, not as legal advice.

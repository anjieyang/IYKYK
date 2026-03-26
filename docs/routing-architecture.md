# UncommonRoute Routing Architecture

这份文档描述的是 **当前代码实际实现的 routing 行为**，不是理想设计，也不是 README 式的产品介绍。

重点回答 4 个问题：

1. 什么请求会真的触发 routing
2. 路由器实际看到了什么输入
3. 选模型时到底考虑了哪些信号
4. 选完模型以后还会发生什么

---

## 1. 先说清楚范围

UncommonRoute 里有两层东西：

- **核心路由器**：`router/api.py` 里的 `route()`
- **HTTP proxy 请求流**：`proxy.py`，负责从真实 OpenAI / Anthropic 请求里抽取信号、调用 `route()`、再转发到 upstream

这两个层次不要混在一起。

### 当前真正会触发 routing 的请求

只有 **虚拟模型 ID** 会走路由器：

- `uncommon-route/auto`
- `uncommon-route/fast`
- `uncommon-route/best`
- 以及它们的裸别名：`auto` / `fast` / `best`

如果请求里传的是明确的真实模型，比如 `openai/gpt-4o` 或 `anthropic/claude-sonnet-4.6`，那就是 **passthrough**，不会重新选模。

如果请求里 **没有传 `model`**，proxy 会先把它补成当前默认 mode 对应的虚拟模型，再进入 routing。

### Session 现在不做 sticky routing

`session.py` 已经明确说明：session ID 现在只用于：

- cache key 分组
- composition checkpoint
- stats / trace 打标

**不再用于锁定模型或按 session 升降级。**

---

## 2. 真实请求流长什么样

当前 proxy 的主路径可以概括成下面这条链：

```text
Client request
  -> normalize request shape
  -> if no model: inject default virtual model
  -> if explicit real model: passthrough
  -> else:
       extract prompt + system prompt
       classify step type
       derive requirements / hints
       route() -> selected model + fallback chain
       compose messages (compaction / artifacts / summaries)
       recompute cost
       spend check
       choose provider / transport / cache strategy
       forward to upstream
       if model-name error: try fallback chain
       record stats / feedback / model experience
```

这里最重要的一点是：

- **选模型发生在 composition 之前**
- **spend check 发生在 composition 之后**
- **真正发给 upstream 的消息体，可能已经不是 routing 时看到的原始消息体了**

---

## 3. 路由器实际看到了什么

这是最容易被写错的地方。

### 3.1 它不是看整段对话，而是看提取后的“当前用户意图”

proxy 会从 `messages` 中倒着找最后一条 `role=user` 的消息，然后做清洗。

它会主动去掉很多框架注入的包装噪音，例如：

- Claude Code / Cursor 风格的 `<system-reminder>...</system-reminder>`
- OpenClaw 的：
  - `[Chat messages since your last reply - for context]`
  - `[Current message - respond to this]`

也就是说，很多 agent 框架发上来的巨大包装文本，最终不会原样进入分类器。

### 3.2 system prompt 会被提取，但不会参与分类特征

`_extract_prompt()` 会拿到第一条 system message，但 `classifier.py` 现在**故意只用用户 prompt 做特征提取**。

原因很明确：Claude Code / Cursor 这一类系统提示里包含大量工具定义、代码示例、规则文本，如果把它们也算进去，会把几乎所有请求都抬到高复杂度。

所以当前实现是：

- system prompt：保留给兼容层和调试信息
- classifier 特征：**只看用户 prompt**

### 3.3 历史对话对 routing 的影响是“间接”的

历史不会直接进 classifier，但会通过这些侧面信号影响路由：

- 当前 step type 是不是 `tool-selection`
- 当前 step type 是不是 `tool-result-followup`
- 当前请求有没有 tools
- 当前请求有没有 vision 内容
- 当前请求是否要求 structured output

所以当前 routing 不是“全对话语义理解”，而是：

- **当前用户意图**
- 加上一点 **请求形态信号**

---

## 4. proxy 在 live 请求里会提取哪些信号

当前 live proxy 路径里，真正送进 `route()` 的关键信号如下。

| 信号 | 来源 | 用途 |
| --- | --- | --- |
| `prompt` | 最后一条 user message，经过 wrapper 清洗 | 分类复杂度 |
| `system_prompt` | 第一条 system message | 兼容输入；不进入 classifier 特征 |
| `step_type` | `general` / `tool-selection` / `tool-result-followup` | 影响 `is_agentic`、cache、composition |
| `needs_tool_calling` | 请求里有 `tools` / `customTools` | 过滤不支持 tool 的模型 |
| `needs_vision` | message content 里有 image | 过滤不支持 vision 的模型 |
| `needs_structured_output` | `response_format` 是 JSON / schema | 提高 complexity 下限 |
| `available_models` | upstream `/v1/models` 实时发现 | 候选模型池 |
| `pricing` | 动态 pricing + 静态兜底 | 成本估计、预算过滤、排序辅助 |
| `model_capabilities` | 模型名启发式推断 + discovery merge | capability 过滤 |
| `user_keyed_models` | BYOK providers.json | 选择时加分，转发时优先走用户自己的 provider |
| `model_experience` | 本地 experience store | latency / reliability / feedback / cache / reward |

### 当前没有从 proxy 显式提出来的信号

这几个东西在核心 `route()` API 里存在，但 **当前 proxy 并没有把它们作为一等 HTTP 输入暴露出来**：

- `RoutingConstraints`，比如 `allowed_models` / `allowed_providers` / `max_cost`
- `AnswerDepth`
- 显式 `is_coding` hint

这意味着：

- HTTP proxy 路径里，`is_coding` 主要靠 classifier 自己从 prompt 特征里识别
- `route()` 里那套 coding complexity boost / coding reasoning bias，在 SDK 直接调用时更明显；在 proxy 路径里不是主信号

---

## 5. 核心 routing 算法

核心算法可以拆成三步：

1. classify 出连续 complexity
2. 用 hints / requirements 调整 complexity
3. 在动态模型池里打分选第一名

### 5.1 classify：先得到 0.0-1.0 的 complexity

`classifier.py` 当前是三级结构：

#### Level 0：trivial override

直接短路的极端场景：

- 很短的问候语 -> `SIMPLE`
- 极短文本 -> `SIMPLE`
- 超长文本 -> `COMPLEX`

#### Level 1：learned model

主路径使用 `learned.py` 里的 Averaged Perceptron。

它的输入特征不是某一种语言专用规则，而是三类组合：

- **结构特征**：长度、枚举密度、句子数、代码标记、数学符号、需求短语等
- **Unicode block 分布**：CJK / Latin / Cyrillic / Arabic 等脚本比例
- **关键词特征**：code / reasoning / technical / analytical / agentic 等多语言词汇信号

输出不是硬 tier，而是一个连续 complexity：

```text
complexity = P(SIMPLE)*0.0 + P(MEDIUM)*0.40 + P(COMPLEX)*0.90
```

#### Level 2：rule fallback

如果 learned model 文件不存在，就退回手工权重的规则分类器。

### 5.2 complexity 调整

`route()` 拿到 classifier 的 complexity 后，还会做几层修正：

- 如果 prompt 含 `json` / `structured` / `schema`，会把 structured-output hint 打开
- structured output 至少拉到一个 complexity floor
- agentic 请求至少拉到一个 complexity floor
- 如果显式传了 `tier_floor` / `tier_cap`，会把 complexity 钳在对应范围内
- 如果 classifier 给出了很强的 reasoning 偏好信号，也会把 complexity 抬高

注意：

- **tier 是 complexity 的派生结果**
- 当前 live 路径里不是先判 tier 再从 tier 表里挑模型，而是先得到 complexity，再做 pool scoring

### 5.3 tier 只是对 complexity 的公开分箱

当前对外暴露的 tier 仍然是三档：

- `< 0.33` -> `SIMPLE`
- `< 0.67` -> `MEDIUM`
- `>= 0.67` -> `COMPLEX`

但内部真正驱动选择的是连续 complexity，而不是这三个离散桶本身。

---

## 6. 当前 selector 真正怎么选模型

当前 live 路径走的是 `selector.py` 的 `select_from_pool()`，不是旧的 per-tier shortlist 逻辑。

### 6.1 候选池先过滤

顺序上会先做这些过滤：

1. capability 过滤：不满足 tool / vision / reasoning 要求的模型先排除
2. constraint 过滤：如果 core API 传了 `RoutingConstraints`，再进一步缩小候选
3. budget 过滤：如果传了 `max_cost`，按请求级预计成本筛掉超预算模型

如果过滤得太狠把候选清空了，会适当放宽。

### 6.2 当前 pool score 用的是什么

核心公式是：

```text
score = base_quality
      + w_editorial * complexity * quality_prior
      - w_cost * (1 - complexity) * cost_norm
      + auxiliary
      + bandit_bonus
```

各部分含义：

- `base_quality`: 来自 `ModelExperienceStore.reward_mean`
- `quality_prior`: **价格越高，质量先验越高**
- `cost_norm`: **价格越高，成本惩罚越大**
- `auxiliary`: latency / reliability / feedback / cache_affinity / byok / free / local / reasoning
- `bandit_bonus`: 给低样本候选的探索奖励

### 6.3 一个非常关键的实现细节

当前 `select_from_pool()` 里的 **quality_prior 和 cost_norm 都是基于模型价格表本身**算出来的，不是直接用这次请求的预计 dollar cost 排序。

也就是说，live pool score 里“贵模型更强、便宜模型更省”的判断，主要来自：

- `input_price + output_price` 的相对高低

而不是这次请求在当前 token 数下的精确总价。

请求级预计成本仍然有用，但它主要用在：

- `max_cost` 预算过滤
- fallback 链的 cost 展示
- spend control
- stats / savings 统计

### 6.4 complexity 如何改变选择风格

这套设计的核心思想是：

- **简单请求**：更在意便宜和快
- **复杂请求**：更在意高质量候选

所以 complexity 越高：

- `quality_prior` 权重越大
- `cost_penalty` 权重越小

### 6.5 Mode 改的是权重风格，不是候选池来源

三种 mode 的本质是三套权重：

- `auto`: 平衡
- `fast`: 更偏成本和延迟
- `best`: 更偏质量和 reasoning

当前 model pool 仍然是同一个动态池，mode 主要改变的是：

- editorial / cost / latency / reliability / feedback / cache_affinity / reasoning 的相对权重
- bandit 的探索强度和 guardrail

### 6.6 fallback chain 现在是什么

在当前 pool 路径里，fallback chain 不是“预先配置好的固定顺序”，而是：

- **当前这次请求的候选模型，按最终得分排完序之后的结果**

所以 fallback chain 是一个 **runtime ranked list**。

只有旧的 `select_model()` 逻辑才真正会把 `TierConfig.primary/fallback/hard_pin` 当成核心输入。

---

## 7. 动态模型池是怎么来的

当前 live 路由默认依赖 `ModelMapper`。

### 7.1 discovery

启动时和定时 rediscovery 会请求：

```text
GET {upstream}/v1/models
```

然后构建：

- upstream 实际存在的模型池
- 动态 pricing
- 动态 capabilities
- internal name -> upstream name 的映射

### 7.2 动态与静态的关系

`DEFAULT_MODEL_PRICING` 现在的角色是：

- 冷启动种子
- discovery 失败时的兜底
- baseline 成本比较参考

正常情况下 live selector 用的是：

- `available_models = _mapper.available_models`
- `pricing = dynamic + static fallback`
- `capabilities = dynamic + static fallback`

### 7.3 名称映射

ModelMapper 会按这个顺序解决名字不一致问题：

1. learned alias
2. exact match
3. seed alias
4. fuzzy match

它学到的新 alias 会落盘，用于后续请求。

### 7.4 一个经常让人误解的点

`GET /v1/models` 暴露的是 **UncommonRoute 的虚拟模型**，不是 upstream 的完整 live pool。

要看真实 pool，应该看：

- `GET /v1/models/mapping`
- `GET /v1/selector`
- `GET /health`

---

## 8. 选完模型以后，proxy 还会做什么

这部分经常被误写成 routing 本身，但它其实是 **routing 之后的请求执行层**。

### 8.1 composition

在 selected model 已经确定后，proxy 还会调用 `compose_messages_semantic()`，做这些事：

- inline compaction
- 大 tool result artifact 化
- side-channel semantic summary
- 历史 checkpoint
- artifact rehydrate

注意：

- 这些步骤会改变 `messages`
- 这些步骤会减少 input tokens
- **但当前不会因为 composition 结果重新选一次模型**

### 8.2 spend control

composition 之后会重新计算预计成本，然后再做 spend check。

所以当前 spend check 看的是：

- 主模型预计成本
- 加上 side-channel semantic call 的预计成本

### 8.3 provider / transport / cache

选完模型后，proxy 还会根据模型族和 provider 决定：

- 是走普通 OpenAI-style `/chat/completions`
- 还是走 Anthropic native `/messages`
- 怎么打 cache hints
- 是否使用用户自己的 BYOK provider

这些都会影响：

- 实际 TTFT / TPS
- cache hit ratio
- input cost multiplier

然后这些结果又会反过来进入 `ModelExperienceStore`。

### 8.4 upstream fallback

如果 selected model 发到 upstream 后报的是“模型不存在 / 模型不可用”这一类错误，proxy 会：

1. 按 fallback chain 依次尝试其他候选
2. 如果某个 fallback 成功，把这次解析记录成 learned alias
3. 更新 request 的 stats / feedback 绑定信息

所以 fallback 不是只存在于 `RoutingDecision` 里，它在 proxy 里有真实的执行逻辑。

---

## 9. 运行时自适应信号从哪里来

当前 selector 不是纯静态打分，它会吃本地运行时记忆。

### 9.1 ModelExperienceStore 记录什么

按 `(mode, tier, model)` 这个 bucket 记：

- success / failure
- TTFT
- TPS
- cache read / cache write 比例
- input cost multiplier
- 用户反馈偏好
- reward EWMA

这些被折叠成 selector 里的：

- `reliability`
- `latency`
- `feedback`
- `cache_affinity`
- `input_cost_multiplier`
- `reward_mean`

### 9.2 feedback 同时影响两条线

`/v1/feedback` 的 `ok` / `weak` / `strong` 会同时更新：

1. **classifier**：在线调整 tier 分类器权重
2. **model experience**：调整具体模型在对应 bucket 下的偏好 / reward

所以 feedback 不是只改“这次 prompt 应该归哪个 tier”，也会改“这个 bucket 下以后更偏爱哪个模型”。

---

## 10. 当前哪些配置真的会影响 live routing

这是文档里必须说清楚的一节。

| 配置 / 信号 | 当前 live proxy 是否生效 | 备注 |
| --- | --- | --- |
| default mode | 是 | 请求未传 `model` 时使用 |
| `auto` / `fast` / `best` 权重差异 | 是 | 直接影响 pool scoring |
| 动态 model discovery | 是 | 默认 live pool 来源 |
| 动态 pricing / capabilities merge | 是 | 影响过滤和排序 |
| BYOK provider | 是 | 影响排序和最终转发目标 |
| feedback / model experience | 是 | 影响 runtime score |
| spend limits | 是，但属于 guardrail | 会阻断请求，不直接选模 |
| `TierConfig.primary/fallback/hard_pin` | **当前主路径不是** | `route()` 走 `select_from_pool()`，不会读取 `ModeConfig.tiers` |
| `free_model` | 否 | 当前主路径未使用 |
| `max_tokens_force_complex` | 否 | 当前主路径未使用 |
| `structured_output_min_tier` | 否 | 当前主路径未直接使用；实际是 complexity floor 在起作用 |
| `ambiguous_default_tier` | 否 | 当前主路径未使用 |
| `AnswerDepth` | core API 有，proxy 未显式暴露 | proxy 目前基本使用默认 `standard` |
| `RoutingConstraints` | core API 有，proxy 未显式暴露 | HTTP 请求里没有成体系映射 |

### 一个必须明确的当前状态

`config set-tier ... --strategy hard-pin`、dashboard 里的 tier override、`RoutingConfigStore` 这些配置：

- **会被持久化**
- **会出现在 API / dashboard / selector state 里**
- **但当前 live pool-based `route()` 主路径并没有读取它们**

换句话说，今天真正控制 live 选模的是：

- mode 的权重
- 动态模型池
- runtime experience
- feedback
- BYOK
- capability / budget / request shape

而不是 tier override 表。

如果后面想让 `hard-pin` 真正接管 live routing，需要把 `ModeConfig.tiers` 接回主路径，或者让 `select_from_pool()` 消费这些 tier overrides。

---

## 11. 文档里应该明确写出的限制

如果这份文档目的是“解释当前 routing 的工作原理和考虑因素”，建议把下面这些限制显式写出来，不要埋在代码里：

- **routing 只对虚拟模型生效**，显式真实模型请求直接 passthrough
- **routing 主要看当前 user prompt**，不是完整会话语义
- **system prompt 不进入 classifier 特征**，这是刻意设计
- **session 现在不做 sticky routing**
- **live selector 用的是动态 pool scoring，不是固定 tier -> model 映射**
- **fallback chain 是 runtime ranked list**
- **composition 在选模之后执行，不会反向重跑 routing**
- **`GET /v1/models` 不是 live upstream catalog**
- **tier override / hard-pin 目前不是 live 主路径的实际控制器**

---

## 12. 最适合这份文档的写法

如果目标是“讲清楚 routing 的工作原理和考虑了什么”，最推荐的结构就是：

1. **Scope**
   当前哪些请求会走 routing，哪些不会
2. **End-to-end flow**
   从请求进 proxy 到发往 upstream 的完整链路
3. **What the router actually sees**
   prompt 提取、wrapper 清洗、system prompt 排除、step type
4. **Signals considered**
   classifier、requirements、dynamic pool、experience、feedback、BYOK
5. **Selection algorithm**
   complexity -> filtering -> pool scoring -> fallback chain
6. **What happens after selection**
   composition、spend、transport、fallback、stats
7. **What config really matters today**
   哪些开关 live，哪些只是存起来了
8. **Limitations / non-goals**
   避免读者以为系统在做它其实没做的事情

这比“先列很多 feature 维度，再列所有默认模型价格”更适合解释当前实现，因为现在最容易让人误解的不是分类器细节，而是：

- 路由到底在 proxy 里什么时候发生
- 动态模型池和虚拟模型的关系
- runtime experience / feedback 到底有没有进入决策
- tier override 到底是不是 live

---

## 13. 关键代码入口

如果要继续追代码，建议按这个顺序看：

- `uncommon_route/uncommon_route/proxy.py`
  - 请求入口、prompt 提取、step 分类、route 调用、forward、fallback、stats
- `uncommon_route/uncommon_route/router/api.py`
  - `route()` 主入口
- `uncommon_route/uncommon_route/router/classifier.py`
  - complexity 产生过程
- `uncommon_route/uncommon_route/router/selector.py`
  - pool scoring 和 fallback chain
- `uncommon_route/uncommon_route/model_map.py`
  - live model discovery、pricing、capability merge、name mapping
- `uncommon_route/uncommon_route/model_experience.py`
  - latency / reliability / cache / reward / feedback memory
- `uncommon_route/uncommon_route/feedback.py`
  - online classifier update + model preference feedback
- `uncommon_route/uncommon_route/composition.py`
  - 选模后的 message compaction / artifacts / checkpoint
- `uncommon_route/uncommon_route/routing_config_store.py`
  - 当前已持久化但尚未完整接入主路由的 tier override 配置

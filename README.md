<div align="center">

<h1>UncommonRoute</h1>

<p><strong>SOTA LLM Router — 98% accuracy, &lt;1ms local routing</strong></p>

<p>
Route every LLM request to the optimal model.<br>
Step-aware agentic routing, 39-feature cascade classifier, session persistence, spend control.<br>
Pure local — no external API calls for routing decisions.
</p>

<img src="https://img.shields.io/badge/98%25_Accuracy-success?style=for-the-badge" alt="98% accuracy">&nbsp;
<img src="https://img.shields.io/badge/<1ms_Latency-blue?style=for-the-badge" alt="<1ms">&nbsp;
<img src="https://img.shields.io/badge/Zero_External_Calls-purple?style=for-the-badge" alt="Local">&nbsp;
<img src="https://img.shields.io/badge/OpenAI_Compatible-orange?style=for-the-badge" alt="OpenAI compatible">

<br><br>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-169_passing-success?style=flat-square)]()
[![OpenClaw Plugin](https://img.shields.io/badge/OpenClaw-Plugin-orange?style=flat-square)](https://openclaw.ai)

</div>

---

## Quick Navigation

| Section | Description |
|---|---|
| [Quick Start](#quick-start) | Install in 30 seconds |
| [Usage Modes](#usage-modes) | CLI, SDK, Proxy, OpenClaw |
| [How It Works](#how-it-works) | Cascade classifier architecture |
| [Routing Tiers](#routing-tiers) | SIMPLE → MEDIUM → COMPLEX → REASONING |
| [Step-Aware Routing](#step-aware-routing) | Per-step model selection for agent workflows |
| [Session Management](#session-management) | Smart sessions, auto-escalation |
| [Spend Control](#spend-control) | Per-request, hourly, daily limits |
| [Models & Pricing](#models--pricing) | Supported models and costs |
| [Configuration](#configuration) | Upstream, env vars, BYOK |
| [Benchmarks](#benchmarks) | Accuracy & latency results |

---

## Quick Start

**1. Install:**

```bash
pip install uncommon-route
```

**2. Configure upstream** (any OpenAI-compatible API):

```bash
# Pick one — or see .env.example for more options
export UNCOMMON_ROUTE_UPSTREAM="https://api.openai.com/v1"
export UNCOMMON_ROUTE_API_KEY="sk-..."
```

**3. Use it:**

```bash
# Local classification (no API key needed)
uncommon-route route "what is 2+2"

# Start the proxy (requires upstream)
uncommon-route serve
```

<details>
<summary>Alternative: one-line installer</summary>

```bash
curl -fsSL https://anjieyang.github.io/uncommon-route/install | bash
```

</details>

<details>
<summary>Alternative: OpenClaw plugin</summary>

```bash
openclaw plugins install @anjieyang/uncommon-route
openclaw gateway restart
```

</details>

---

## Usage Modes

### 1. CLI

```bash
uncommon-route route "what is 2+2"
# Model: moonshot/kimi-k2.5  Tier: SIMPLE  Savings: 97%

uncommon-route route --json "design a distributed database"
# Full JSON with model, tier, confidence, cost, fallback chain

uncommon-route debug "explain quicksort"
# Per-dimension scoring breakdown (structural + keyword + unicode)
```

### 2. Python SDK

```python
from uncommon_route import route, classify

decision = route("explain the Byzantine Generals Problem")
print(decision.model)       # google/gemini-3.1-pro
print(decision.tier)        # COMPLEX
print(decision.confidence)  # 0.87
print(decision.savings)     # 0.76

# Classification only (no model selection)
result = classify("hello")
print(result.tier)          # SIMPLE
print(result.signals)       # ['short_prompt', 'greeting_pattern']
```

### 3. HTTP Proxy (OpenAI-compatible)

```bash
uncommon-route serve --port 8403
```

Works with any OpenAI SDK client:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8403/v1",
    api_key="your-upstream-key",
)

response = client.chat.completions.create(
    model="uncommon-route/auto",   # smart routing
    messages=[{"role": "user", "content": "hello"}],
)
```

| Endpoint | Method | Description |
|---|---|---|
| `/v1/chat/completions` | POST | Chat with smart routing |
| `/v1/models` | GET | Available models |
| `/v1/spend` | GET/POST | Spend control |
| `/v1/sessions` | GET | Active sessions |
| `/health` | GET | Health + status |

### 4. OpenClaw Plugin

```bash
openclaw plugins install @anjieyang/uncommon-route
```

The plugin auto-installs Python dependencies, starts the proxy, and registers everything. Available commands in OpenClaw:

| Command | Description |
|---|---|
| `/route <prompt>` | Preview routing decision |
| `/spend status` | View spending limits |
| `/spend set hourly 5.00` | Set hourly limit |
| `/sessions` | View active sessions |

---

## How It Works

UncommonRoute uses a **cascade classifier** with three levels:

```
Input Prompt
     │
     ▼
┌─────────────────────┐
│ 1. Trivial Override  │  greeting / empty / very long → instant decision
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 2. Learned Model    │  Averaged Perceptron on 39 features
│    (356µs avg)      │  12 structural + 15 unicode + 12 keyword
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 3. Rule Fallback    │  hand-tuned weights when model unavailable
└─────────┬───────────┘
          │
          ▼
    Tier + Model + Cost
```

### Feature Groups (39 total)

**Structural (12):** normalized_length, enumeration_density, sentence_count, code_markers, math_symbols, nesting_depth, vocabulary_diversity, avg_word_length, alphabetic_ratio, functional_intent, unique_concept_density, requirement_phrases

**Unicode (15):** basic_latin, latin_ext, cyrillic, arabic, devanagari, thai, hangul_jamo, cjk_unified, hiragana, katakana, hangul_syllables, punctuation, digits, symbols_math

**Keyword (12):** code_presence, reasoning_markers, technical_terms, creative_markers, simple_indicators, imperative_verbs, constraint_count, output_format, domain_specificity, agentic_task, analytical_verbs, multi_step_patterns

---

## Routing Tiers

The router classifies each prompt and selects the **cheapest model that can handle it**. Default primary models are chosen for cost efficiency — all models (including OpenAI, Claude) are accessible through the upstream provider.

| Tier | When | Default Primary | Fallback Chain | Example |
|---|---|---|---|---|
| **SIMPLE** | Greetings, lookups, translations | moonshot/kimi-k2.5 | gemini-2.5-flash-lite, deepseek-chat | "what is 2+2" |
| **MEDIUM** | Code tasks, explanations, summaries | moonshot/kimi-k2.5 | deepseek-chat, gemini-2.5-flash-lite | "explain quicksort" |
| **COMPLEX** | Multi-requirement system design | google/gemini-3.1-pro | gemini-2.5-pro, gpt-5.2, claude-sonnet-4.6 | "design a distributed DB with 5 requirements..." |
| **REASONING** | Formal proofs, mathematical derivations | xai/grok-4-1-fast-reasoning | deepseek-reasoner, o4-mini, o3 | "prove sqrt(2) is irrational" |

> **Note:** OpenAI and Claude models appear in COMPLEX/REASONING fallback chains. To make them the preferred choice across all tiers, use [BYOK provider configuration](#bring-your-own-key-byok).

---

## Step-Aware Routing

In agentic workflows (OpenClaw, LangChain, etc.), different steps within a single task need different model capabilities. UncommonRoute detects the step type from the request body and routes accordingly:

| Step Type | Detection | Routing Behavior |
|---|---|---|
| **Tool-result followup** | Last message `role: "tool"` | Classifier decides freely — allows cheap model for processing tool output |
| **Tool selection** | `tools` present + last message from user | Normal session logic |
| **General** | No agentic signals | Normal session logic |

**Before (blind session pin):** Agent session pinned to $25/M model for all 200 requests — including "I read this file" steps.

**After (step-aware):** Tool-result steps automatically use $0.40-2.50/M models. Only steps that need reasoning use expensive models.

The step type is visible in the `x-uncommon-route-step` response header.

---

## Session Management

Sessions prevent unnecessary model switching mid-task while allowing cost optimization:

- **Always re-route** — every request gets a fresh classification based on content
- **Only upgrade, never downgrade** — if the classifier says COMPLEX and the session is MEDIUM, upgrade; if it says SIMPLE, hold the session model
- **Lightweight exception** — tool-result steps bypass session hold and use the classifier's recommendation directly
- **30-minute timeout** — sessions auto-expire after inactivity
- **Three-strike escalation** — 3 identical requests → auto-upgrade to next tier (skipped for tool-result steps)

```python
# Sessions work via header
headers = {"X-Session-ID": "my-task-123"}

# OpenClaw's x-openclaw-session-key also supported
# Or auto-derived from first user message
```

---

## Spend Control

Set spending limits to prevent runaway costs:

```bash
uncommon-route spend set per_request 0.10   # max $0.10 per call
uncommon-route spend set hourly 5.00        # max $5/hour
uncommon-route spend set daily 20.00        # max $20/day
uncommon-route spend set session 3.00       # max $3/session
uncommon-route spend status                 # view current spending
uncommon-route spend history                # recent records
```

When a limit is hit, the proxy returns HTTP 429 with `reset_in_seconds`.

Data persists at `~/.uncommon-route/spending.json`.

---

## Models & Pricing

The router selects models by tier to minimize cost. Availability depends on your upstream provider — multi-provider gateways (OpenRouter, Commonstack) expose all of these; direct provider APIs expose only their own models.

| Model | Input ($/1M) | Output ($/1M) | Role |
|---|---|---|---|
| nvidia/gpt-oss-120b | $0.00 | $0.00 | SIMPLE fallback |
| google/gemini-2.5-flash-lite | $0.10 | $0.40 | SIMPLE/MEDIUM fallback |
| deepseek/deepseek-chat | $0.28 | $0.42 | MEDIUM fallback |
| xai/grok-4-1-fast-reasoning | $0.20 | $0.50 | REASONING primary |
| moonshot/kimi-k2.5 | $0.60 | $3.00 | SIMPLE/MEDIUM primary |
| google/gemini-3.1-pro | $2.00 | $12.00 | COMPLEX primary |
| openai/gpt-5.2 | $1.75 | $14.00 | COMPLEX fallback |
| anthropic/claude-sonnet-4.6 | $3.00 | $15.00 | COMPLEX fallback |

Baseline comparison: anthropic/claude-opus-4.6 at $5.00/$25.00 per 1M tokens.

> **Why these defaults?** The primary models for SIMPLE/MEDIUM tiers (kimi-k2.5, gemini-flash-lite) are 5–37× cheaper than OpenAI/Claude per output token. For most prompts classified as simple or medium, these models produce equivalent results at a fraction of the cost. Complex prompts still route to frontier models (gemini-3.1-pro, with gpt-5.2 and claude-sonnet-4.6 in the fallback chain).

---

## Configuration

### Upstream Provider

UncommonRoute is a **routing layer only** — it does not host models. It forwards requests to an upstream OpenAI-compatible API that you configure.

```bash
# OpenAI direct
export UNCOMMON_ROUTE_UPSTREAM="https://api.openai.com/v1"
export UNCOMMON_ROUTE_API_KEY="sk-..."

# OpenRouter (100+ models, single key)
export UNCOMMON_ROUTE_UPSTREAM="https://openrouter.ai/api/v1"
export UNCOMMON_ROUTE_API_KEY="sk-or-..."

# Commonstack (multi-provider gateway)
export UNCOMMON_ROUTE_UPSTREAM="https://api.commonstack.ai/v1"
export UNCOMMON_ROUTE_API_KEY="csk-..."

# Local (Ollama, vLLM, etc.) — no key needed
export UNCOMMON_ROUTE_UPSTREAM="http://127.0.0.1:11434/v1"
```

> **Tip:** Multi-provider gateways like [OpenRouter](https://openrouter.ai) or [Commonstack](https://commonstack.ai) work well with UncommonRoute because they expose all models (OpenAI, Claude, Gemini, DeepSeek, etc.) behind a single API key — the router can select across providers without extra configuration.

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `UNCOMMON_ROUTE_UPSTREAM` | — | Upstream OpenAI-compatible API URL (required for proxy) |
| `UNCOMMON_ROUTE_API_KEY` | — | API key for the upstream provider |
| `UNCOMMON_ROUTE_PORT` | `8403` | Proxy port |
| `UNCOMMON_ROUTE_DISABLED` | `false` | Disable routing (passthrough) |

### Bring Your Own Key (BYOK)

If you have API keys for specific providers and want the router to **prefer those models**, register them with the BYOK system:

```bash
uncommon-route provider add openai sk-your-openai-key
uncommon-route provider add anthropic sk-ant-your-key
uncommon-route provider list
```

When a BYOK provider is registered, the router will prefer your keyed models whenever they appear in a tier's candidate list. For example, adding an OpenAI key means COMPLEX-tier prompts will prefer `openai/gpt-5.2` over the default `google/gemini-3.1-pro`.

Provider config is stored at `~/.uncommon-route/providers.json`.

### OpenClaw Plugin Config

```yaml
plugins:
  entries:
    "@anjieyang/uncommon-route":
      port: 8403
      upstream: "https://api.commonstack.ai/v1"
      spendLimits:
        hourly: 5.00
        daily: 20.00
```

---

## Benchmarks

Evaluated on 2000+ multilingual prompts across 10 languages (EN, ZH, KO, JA, ES, PT, AR, RU, DE, HI):

| Metric | Value |
|---|---|
| **Overall Accuracy** | 98.4% |
| **Average Latency** | 356µs |
| **Features** | 39 (structural + unicode + keyword) |
| **Learning** | Averaged Perceptron |
| **External API Calls** | None (pure local) |

### Per-Tier F1 Scores

| Tier | F1 |
|---|---|
| SIMPLE | 0.988 |
| MEDIUM | 0.968 |
| COMPLEX | 0.987 |
| REASONING | 1.000 |

Run the benchmark suite yourself:

```bash
cd bench && python run.py
```

---

## Project Structure

```
├── uncommon_route/           # Core package
│   ├── router/               # Cascade classifier + model selection
│   │   ├── classifier.py     # Three-level cascade
│   │   ├── learned.py        # Averaged Perceptron (ScriptAgnosticClassifier)
│   │   ├── structural.py     # 12 structural + 15 unicode features
│   │   ├── keywords.py       # 12 keyword features
│   │   ├── selector.py       # Tier → model + fallback chain
│   │   └── model.json        # Trained weights
│   ├── proxy.py              # OpenAI-compatible ASGI proxy
│   ├── session.py            # Session persistence + escalation
│   ├── spend_control.py      # Time-windowed spending limits
│   ├── providers.py          # BYOK provider management
│   ├── openclaw.py           # OpenClaw config integration
│   └── cli.py                # CLI entry point
├── openclaw-plugin/          # JS bridge for OpenClaw
│   ├── src/index.js          # Auto-install + lifecycle management
│   ├── package.json          # @anjieyang/uncommon-route
│   └── openclaw.plugin.json  # Plugin manifest
├── tests/                    # 169 tests (unit + integration + E2E)
├── bench/                    # Benchmarking suite + datasets
├── scripts/install.sh        # One-line installer
└── pyproject.toml            # PyPI-ready packaging
```

---

## Development

```bash
git clone https://github.com/anjieyang/UncommonRoute.git
cd UncommonRoute
pip install -e ".[dev]"
python -m pytest tests/ -v
```

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">
<sub>Built by <a href="https://github.com/anjieyang">Anjie Yang</a></sub>
</div>

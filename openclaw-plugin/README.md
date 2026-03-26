<p align="right"><strong>English</strong> | <a href="https://github.com/CommonstackAI/UncommonRoute/blob/main/README.zh-CN.md">简体中文</a></p>

# @anjieyang/uncommon-route

OpenClaw plugin for [UncommonRoute](https://github.com/CommonstackAI/UncommonRoute), the local LLM router that classifies prompts, scores the discovered upstream pool, and routes virtual model IDs before forwarding requests upstream.

If you use OpenClaw and want one local endpoint with smart routing behind it, this plugin is the shortest path.

## Mental Model

```text
OpenClaw -> UncommonRoute -> your upstream API
```

This plugin:

- installs the Python `uncommon-route` package if needed
- starts `uncommon-route serve`
- registers the local provider with OpenClaw
- exposes the virtual routing modes like `uncommon-route/auto`
- syncs the discovered upstream pool into OpenClaw after the local proxy becomes healthy

## Install

```bash
openclaw plugins install @anjieyang/uncommon-route
openclaw gateway restart
```

That is enough to install the plugin.

For real responses, you still need to configure an upstream model API.

## Configure An Upstream

UncommonRoute does not host models. It routes to an upstream OpenAI-compatible API.

Example plugin config:

```yaml
plugins:
  entries:
    uncommon-route:
      port: 8403
      upstream: "https://api.commonstack.ai/v1"
      spendLimits:
        hourly: 5.00
        daily: 20.00
```

> **Note:** OpenClaw uses the unscoped directory name `uncommon-route` as the
> entries key, not the full npm package name `@anjieyang/uncommon-route`.
> Config placed under the scoped name will not reach the plugin.

Common upstream choices:

| Provider | URL |
| --- | --- |
| [Parallax](https://github.com/GradientHQ/parallax) | `http://127.0.0.1:3001/v1` |
| [Commonstack](https://commonstack.ai) | `https://api.commonstack.ai/v1` |
| OpenAI | `https://api.openai.com/v1` |
| Local Ollama / vLLM | `http://127.0.0.1:11434/v1` |

If your upstream needs a key, set `UNCOMMON_ROUTE_API_KEY` in the environment where OpenClaw runs.

Parallax is best treated as an experimental local upstream for now: its public docs show `POST /v1/chat/completions`, but UncommonRoute model discovery may be limited because a public `/v1/models` route was not obvious in the repo.

## What You Get

- a local OpenClaw provider backed by `http://127.0.0.1:8403/v1`
- `uncommon-route/auto` for balanced smart routing
- always-available virtual modes: `uncommon-route/fast` and `uncommon-route/best`

Once the proxy is up and `/v1/models/mapping` is available, the plugin refreshes the OpenClaw provider catalog from the discovered pool. If discovery is unavailable, the virtual modes still work and explicit passthrough model IDs can still be typed manually.

The router also keeps a fallback chain, records local feedback, and exposes a local dashboard at `http://127.0.0.1:8403/dashboard/`.

## OpenClaw Commands

| Command | Description |
| --- | --- |
| `/route <prompt>` | Preview which model the router would pick |
| `/spend status` | Show current spending and limits |
| `/spend set hourly 5.00` | Set an hourly spend limit |
| `/feedback <signal>` | Use `ok`, `weak`, `strong`, `status`, or `rollback` to rate the last routing decision or inspect feedback state |

## Troubleshooting

If the plugin is installed but responses are failing:

1. Make sure your upstream URL is configured.
2. Make sure `UNCOMMON_ROUTE_API_KEY` is set if your provider requires one.
3. Open `http://127.0.0.1:8403/health`.
4. Open `http://127.0.0.1:8403/dashboard/`.

## Turn It Off Or Remove It

If you want to stop using the OpenClaw plugin, there are three different levels:

1. stop routing traffic from OpenClaw
2. clear all local UncommonRoute records and state
3. fully uninstall the plugin and the Python package

### 1. Stop routing traffic from OpenClaw

```bash
openclaw plugins uninstall @anjieyang/uncommon-route
openclaw gateway restart
```

If you also started `uncommon-route serve` manually, stop that too:

```bash
uncommon-route stop
# or stop the foreground process with Ctrl+C
```

If you used the config-patch fallback instead of the plugin, remove that registration too:

```bash
uncommon-route openclaw uninstall
```

### 2. Clear all local records

By default, UncommonRoute stores local state under:

```text
~/.uncommon-route
```

If you set `UNCOMMON_ROUTE_DATA_DIR`, it uses that directory instead.

That local data directory can contain:

- route stats and spending history
- dashboard-saved primary connection and routing overrides
- BYOK provider keys
- online-learning weights and feedback buffers
- learned aliases, model-experience memory, logs, and local artifacts

To clear **all** local records, stop the proxy first and then move or delete the active data directory:

```bash
# Show the active data directory
echo "${UNCOMMON_ROUTE_DATA_DIR:-$HOME/.uncommon-route}"

# Recommended: move it aside as a backup first
mv "${UNCOMMON_ROUTE_DATA_DIR:-$HOME/.uncommon-route}" \
  "${UNCOMMON_ROUTE_DATA_DIR:-$HOME/.uncommon-route}.backup-$(date +%Y%m%d-%H%M%S)"

# Or permanently delete it if you are sure
# rm -rf "${UNCOMMON_ROUTE_DATA_DIR:-$HOME/.uncommon-route}"
```

If you only want to clear routing analytics, `uncommon-route stats reset` resets stats and pending feedback. It does **not** remove the rest of the local state.

### 3. Fully uninstall

First remove the OpenClaw plugin or config-patch registration:

```bash
openclaw plugins uninstall @anjieyang/uncommon-route
uncommon-route openclaw uninstall
openclaw gateway restart
```

If you set environment variables for UncommonRoute, clear them:

```bash
unset UNCOMMON_ROUTE_UPSTREAM
unset UNCOMMON_ROUTE_API_KEY
unset OPENAI_BASE_URL
unset ANTHROPIC_BASE_URL
```

Then remove the Python package with the same tool you used to install it:

```bash
pipx uninstall uncommon-route
# or
python -m pip uninstall uncommon-route
# or
pip uninstall uncommon-route
```

## Benchmarks

Current repo benchmarks:

- 97.4% held-out routing accuracy on the current in-repo benchmark set
- ECE improves from 2.1% to 1.7% after temperature scaling
- 68% lower simulated cost than always using Claude Opus in a 131-request coding session

## Links

- [GitHub](https://github.com/CommonstackAI/UncommonRoute)
- [PyPI](https://pypi.org/project/uncommon-route/)
- [Full README](https://github.com/CommonstackAI/UncommonRoute#readme)

## License

Modified MIT

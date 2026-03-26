from __future__ import annotations

from uncommon_route.cache_support import parse_stream_usage_metrics, strip_anthropic_cache_controls
from uncommon_route.router.config import DEFAULT_MODEL_PRICING


def test_parse_stream_usage_metrics_reads_final_usage_event() -> None:
    chunks = [
        b'data: {"id":"chatcmpl-1","choices":[{"delta":{"content":"ping"}}]}\n\n',
        (
            b'data: {"id":"chatcmpl-1","choices":[],"usage":{"prompt_tokens":12901,'
            b'"completion_tokens":38,"total_tokens":12939,"prompt_tokens_details":{"cached_tokens":7168}}}\n\n'
        ),
        b"data: [DONE]\n\n",
    ]

    usage = parse_stream_usage_metrics(
        chunks,
        "moonshot/kimi-k2.5",
        DEFAULT_MODEL_PRICING,
    )

    assert usage is not None
    assert usage.input_tokens_total == 12901
    assert usage.input_tokens_uncached == 5733
    assert usage.output_tokens == 38
    assert usage.cache_read_input_tokens == 7168


def test_parse_stream_usage_metrics_reads_anthropic_message_usage_events() -> None:
    chunks = [
        (
            b"event: message_start\n"
            b'data: {"type":"message_start","message":{"id":"msg_1","type":"message","role":"assistant",'
            b'"content":[],"model":"anthropic/claude-sonnet-4-6","stop_reason":null,"stop_sequence":null,'
            b'"usage":{"input_tokens":21,"cache_read_input_tokens":188086,"cache_creation_input_tokens":0,"output_tokens":0}}}\n\n'
        ),
        (
            b"event: message_delta\n"
            b'data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},'
            b'"usage":{"output_tokens":393}}\n\n'
        ),
    ]

    usage = parse_stream_usage_metrics(
        chunks,
        "anthropic/claude-sonnet-4.6",
        DEFAULT_MODEL_PRICING,
    )

    assert usage is not None
    assert usage.input_tokens_total == 188107
    assert usage.input_tokens_uncached == 21
    assert usage.output_tokens == 393
    assert usage.cache_read_input_tokens == 188086


def test_strip_anthropic_cache_controls_removes_all_ttls() -> None:
    body = {
        "tools": [
            {"name": "Read", "cache_control": {"type": "ephemeral"}},
        ],
        "system": [
            {"type": "text", "text": "Policy", "cache_control": {"type": "ephemeral", "ttl": "1h"}},
        ],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "hello", "cache_control": {"type": "ephemeral"}},
                ],
            },
        ],
    }

    plan = strip_anthropic_cache_controls(body)

    assert plan.family == "anthropic"
    assert plan.mode == "none"
    assert "cache_control" not in body["tools"][0]
    assert "cache_control" not in body["system"][0]
    assert "cache_control" not in body["messages"][0]["content"][0]

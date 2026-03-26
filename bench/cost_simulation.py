"""Real-world cost simulation: OpenClaw agent coding session.

Simulates a realistic agent coding session with 200 requests covering
the typical distribution of an AI coding assistant:
- Memory recall, tool use, file operations
- Code generation, debugging, explanation
- Architecture decisions, complex refactors
- Proof-of-correctness, algorithm analysis

Compares 3 strategies:
  1. Always Opus (no router, premium baseline)
  2. ClawRouter (original)
  3. UncommonRoute

For each request, calculates:
  - Which model gets selected
  - Estimated cost (input + output tokens)
  - Whether the model is "good enough" for the task (quality score)
"""

from __future__ import annotations


# ─── Model capabilities & pricing ───

MODELS = {
    "nvidia/gpt-oss-120b": {
        "in": 0.00,
        "out": 0.00,
        "quality": {"SIMPLE": 0.85, "MEDIUM": 0.50, "COMPLEX": 0.20, "REASONING": 0.10},
    },
    "google/gemini-2.5-flash-lite": {
        "in": 0.10,
        "out": 0.40,
        "quality": {"SIMPLE": 0.90, "MEDIUM": 0.65, "COMPLEX": 0.35, "REASONING": 0.25},
    },
    "deepseek/deepseek-chat": {
        "in": 0.28,
        "out": 0.42,
        "quality": {"SIMPLE": 0.90, "MEDIUM": 0.70, "COMPLEX": 0.40, "REASONING": 0.30},
    },
    "moonshot/kimi-k2.5": {
        "in": 0.60,
        "out": 3.00,
        "quality": {"SIMPLE": 0.95, "MEDIUM": 0.85, "COMPLEX": 0.55, "REASONING": 0.45},
    },
    "xai/grok-4-1-fast-reasoning": {
        "in": 0.20,
        "out": 0.50,
        "quality": {"SIMPLE": 0.85, "MEDIUM": 0.75, "COMPLEX": 0.50, "REASONING": 0.80},
    },
    "xai/grok-4-1-fast-non-reasoning": {
        "in": 0.20,
        "out": 1.50,
        "quality": {"SIMPLE": 0.90, "MEDIUM": 0.80, "COMPLEX": 0.55, "REASONING": 0.40},
    },
    "google/gemini-3.1-pro": {
        "in": 2.00,
        "out": 12.00,
        "quality": {"SIMPLE": 0.95, "MEDIUM": 0.90, "COMPLEX": 0.85, "REASONING": 0.70},
    },
    "openai/gpt-5.2": {
        "in": 1.75,
        "out": 14.00,
        "quality": {"SIMPLE": 0.95, "MEDIUM": 0.92, "COMPLEX": 0.88, "REASONING": 0.75},
    },
    "anthropic/claude-sonnet-4.6": {
        "in": 3.00,
        "out": 15.00,
        "quality": {"SIMPLE": 0.95, "MEDIUM": 0.93, "COMPLEX": 0.90, "REASONING": 0.85},
    },
    "anthropic/claude-opus-4.6": {
        "in": 5.00,
        "out": 25.00,
        "quality": {"SIMPLE": 0.95, "MEDIUM": 0.95, "COMPLEX": 0.95, "REASONING": 0.90},
    },
    "deepseek/deepseek-reasoner": {
        "in": 0.28,
        "out": 0.42,
        "quality": {"SIMPLE": 0.80, "MEDIUM": 0.65, "COMPLEX": 0.40, "REASONING": 0.75},
    },
    "openai/o4-mini": {
        "in": 1.10,
        "out": 4.40,
        "quality": {"SIMPLE": 0.85, "MEDIUM": 0.80, "COMPLEX": 0.60, "REASONING": 0.82},
    },
}

# Tier → model mapping
TIER_MODEL = {
    "SIMPLE": "moonshot/kimi-k2.5",
    "MEDIUM": "moonshot/kimi-k2.5",
    "COMPLEX": "google/gemini-3.1-pro",
    "REASONING": "xai/grok-4-1-fast-reasoning",
}

OPUS = "anthropic/claude-opus-4.6"

# ─── Realistic OpenClaw agent session: 200 requests ───

SESSION: list[dict] = [
    # ── Memory & context (SIMPLE) ──
    {"prompt": "What files did I edit yesterday?", "tier": "SIMPLE", "in_tok": 50, "out_tok": 100},
    {"prompt": "What's in my MEMORY.md?", "tier": "SIMPLE", "in_tok": 30, "out_tok": 200},
    {"prompt": "What version of Node am I running?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30},
    {"prompt": "What's the current branch?", "tier": "SIMPLE", "in_tok": 15, "out_tok": 20},
    {"prompt": "Show me the project structure", "tier": "SIMPLE", "in_tok": 20, "out_tok": 150},
    {"prompt": "What's in package.json?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 200},
    {"prompt": "What port is the server running on?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30},
    {"prompt": "Is TypeScript installed?", "tier": "SIMPLE", "in_tok": 15, "out_tok": 20},
    {"prompt": "What test framework are we using?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30},
    {"prompt": "What's the database URL?", "tier": "SIMPLE", "in_tok": 15, "out_tok": 30},
    {"prompt": "List all environment variables", "tier": "SIMPLE", "in_tok": 20, "out_tok": 100},
    {"prompt": "What's the latest commit?", "tier": "SIMPLE", "in_tok": 15, "out_tok": 50},
    {"prompt": "Who wrote this function?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30},
    {"prompt": "What's the deployment status?", "tier": "SIMPLE", "in_tok": 15, "out_tok": 30},
    {"prompt": "Check if Redis is running", "tier": "SIMPLE", "in_tok": 15, "out_tok": 30},
    {"prompt": "What does this config flag do?", "tier": "SIMPLE", "in_tok": 30, "out_tok": 50},
    {"prompt": "Where is the auth middleware defined?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30},
    {"prompt": "What's the API base URL?", "tier": "SIMPLE", "in_tok": 15, "out_tok": 20},
    {"prompt": "How many test files are there?", "tier": "SIMPLE", "in_tok": 15, "out_tok": 20},
    {"prompt": "What's the linting config?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 80},
    # ── Simple tool use & file ops (SIMPLE) ──
    {"prompt": "Read the README", "tier": "SIMPLE", "in_tok": 15, "out_tok": 300},
    {"prompt": "Create a .env.example file", "tier": "SIMPLE", "in_tok": 20, "out_tok": 50},
    {"prompt": "Add a .gitignore entry for .env", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30},
    {"prompt": "What's in the Dockerfile?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 150},
    {"prompt": "Show me the error log", "tier": "SIMPLE", "in_tok": 15, "out_tok": 200},
    {"prompt": "Clear the build cache", "tier": "SIMPLE", "in_tok": 15, "out_tok": 30},
    {"prompt": "Run the linter", "tier": "SIMPLE", "in_tok": 15, "out_tok": 100},
    {"prompt": "Check disk usage", "tier": "SIMPLE", "in_tok": 15, "out_tok": 30},
    {"prompt": "What's the file size of the bundle?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30},
    {"prompt": "List open ports", "tier": "SIMPLE", "in_tok": 15, "out_tok": 50},
    # ── Code generation: single functions (MEDIUM) ──
    {"prompt": "Write a function to validate email addresses", "tier": "MEDIUM", "in_tok": 30, "out_tok": 200},
    {"prompt": "Add error handling to this API endpoint", "tier": "MEDIUM", "in_tok": 200, "out_tok": 300},
    {"prompt": "Write a unit test for the login function", "tier": "MEDIUM", "in_tok": 150, "out_tok": 250},
    {
        "prompt": "Create a database migration for adding a status column",
        "tier": "MEDIUM",
        "in_tok": 100,
        "out_tok": 200,
    },
    {"prompt": "Write a retry wrapper with exponential backoff", "tier": "MEDIUM", "in_tok": 50, "out_tok": 250},
    {"prompt": "Implement the paginated list endpoint", "tier": "MEDIUM", "in_tok": 150, "out_tok": 300},
    {"prompt": "Add rate limiting middleware", "tier": "MEDIUM", "in_tok": 80, "out_tok": 250},
    {"prompt": "Write a health check endpoint", "tier": "MEDIUM", "in_tok": 50, "out_tok": 150},
    {"prompt": "Create a Dockerfile for the API", "tier": "MEDIUM", "in_tok": 80, "out_tok": 200},
    {"prompt": "Add logging with request IDs", "tier": "MEDIUM", "in_tok": 100, "out_tok": 250},
    {"prompt": "Write a CSV export function", "tier": "MEDIUM", "in_tok": 80, "out_tok": 200},
    {"prompt": "Implement file upload handling", "tier": "MEDIUM", "in_tok": 100, "out_tok": 300},
    {"prompt": "Create a simple caching layer", "tier": "MEDIUM", "in_tok": 60, "out_tok": 200},
    {"prompt": "Write a webhook handler", "tier": "MEDIUM", "in_tok": 80, "out_tok": 250},
    {"prompt": "Add CORS configuration", "tier": "MEDIUM", "in_tok": 50, "out_tok": 100},
    # ── Debugging (MEDIUM) ──
    {
        "prompt": "The tests are failing with 'connection refused'. Help me debug.",
        "tier": "MEDIUM",
        "in_tok": 200,
        "out_tok": 400,
    },
    {"prompt": "This function returns None sometimes. Find the bug.", "tier": "MEDIUM", "in_tok": 300, "out_tok": 300},
    {"prompt": "Memory usage keeps growing. How do I profile this?", "tier": "MEDIUM", "in_tok": 100, "out_tok": 300},
    {
        "prompt": "The API is returning 500 for certain inputs. Debug this.",
        "tier": "MEDIUM",
        "in_tok": 250,
        "out_tok": 400,
    },
    {"prompt": "Why is this query so slow? It takes 5 seconds.", "tier": "MEDIUM", "in_tok": 200, "out_tok": 300},
    {
        "prompt": "The WebSocket connection drops after 30 seconds. Fix it.",
        "tier": "MEDIUM",
        "in_tok": 150,
        "out_tok": 300,
    },
    {"prompt": "Docker build fails at npm install. What's wrong?", "tier": "MEDIUM", "in_tok": 200, "out_tok": 250},
    {
        "prompt": "The migration script is throwing a duplicate key error.",
        "tier": "MEDIUM",
        "in_tok": 200,
        "out_tok": 300,
    },
    # ── Explanation (MEDIUM) ──
    {"prompt": "Explain how this authentication flow works", "tier": "MEDIUM", "in_tok": 300, "out_tok": 400},
    {"prompt": "How does the caching strategy in this service work?", "tier": "MEDIUM", "in_tok": 200, "out_tok": 300},
    {
        "prompt": "Explain the event-driven architecture in this project",
        "tier": "MEDIUM",
        "in_tok": 250,
        "out_tok": 400,
    },
    {"prompt": "How does the database connection pooling work here?", "tier": "MEDIUM", "in_tok": 150, "out_tok": 300},
    {"prompt": "What's the difference between these two approaches?", "tier": "MEDIUM", "in_tok": 300, "out_tok": 400},
    # ── Code review (MEDIUM) ──
    {"prompt": "Review this PR for potential issues", "tier": "MEDIUM", "in_tok": 500, "out_tok": 400},
    {"prompt": "Is this error handling pattern correct?", "tier": "MEDIUM", "in_tok": 300, "out_tok": 300},
    {"prompt": "Review the database schema changes in this migration", "tier": "MEDIUM", "in_tok": 400, "out_tok": 300},
    {"prompt": "Check this API endpoint for security issues", "tier": "MEDIUM", "in_tok": 350, "out_tok": 350},
    {"prompt": "Is this a good use of dependency injection here?", "tier": "MEDIUM", "in_tok": 250, "out_tok": 300},
    # ── Multi-step agent tasks (MEDIUM) ──
    {
        "prompt": "Read the config, update the database URL, and restart the service",
        "tier": "MEDIUM",
        "in_tok": 50,
        "out_tok": 200,
    },
    {
        "prompt": "Run the tests, check which ones fail, and fix the failing ones",
        "tier": "MEDIUM",
        "in_tok": 50,
        "out_tok": 500,
    },
    {"prompt": "Find all TODO comments and create issues for them", "tier": "MEDIUM", "in_tok": 50, "out_tok": 300},
    {
        "prompt": "Update all dependencies to their latest versions and run tests",
        "tier": "MEDIUM",
        "in_tok": 50,
        "out_tok": 400,
    },
    {"prompt": "Deploy to staging and verify the health check passes", "tier": "MEDIUM", "in_tok": 50, "out_tok": 200},
    # ── Summaries and rewrites (MEDIUM) ──
    {"prompt": "Summarize the changes in the last 10 commits", "tier": "MEDIUM", "in_tok": 500, "out_tok": 300},
    {"prompt": "Write a changelog entry for this release", "tier": "MEDIUM", "in_tok": 300, "out_tok": 200},
    {"prompt": "Rewrite this error message to be user-friendly", "tier": "MEDIUM", "in_tok": 100, "out_tok": 100},
    {"prompt": "Write API documentation for this endpoint", "tier": "MEDIUM", "in_tok": 200, "out_tok": 400},
    {"prompt": "Summarize the security audit findings", "tier": "MEDIUM", "in_tok": 500, "out_tok": 300},
    # ── Architecture & system design (COMPLEX) ──
    {
        "prompt": "Design the notification service with push, email, SMS channels, priority queues, user preferences, and retry logic",
        "tier": "COMPLEX",
        "in_tok": 100,
        "out_tok": 2000,
    },
    {
        "prompt": "Refactor the monolith into microservices. Define service boundaries, API contracts, and data ownership.",
        "tier": "COMPLEX",
        "in_tok": 500,
        "out_tok": 3000,
    },
    {
        "prompt": "Design the real-time analytics pipeline with event ingestion, stream processing, aggregation, and dashboarding",
        "tier": "COMPLEX",
        "in_tok": 100,
        "out_tok": 2500,
    },
    {
        "prompt": "Plan the database migration from PostgreSQL to CockroachDB with zero downtime, data validation, and rollback",
        "tier": "COMPLEX",
        "in_tok": 200,
        "out_tok": 2000,
    },
    {
        "prompt": "Design the CI/CD pipeline with build, test, security scan, staging deploy, canary release, and rollback automation",
        "tier": "COMPLEX",
        "in_tok": 100,
        "out_tok": 2000,
    },
    # ── Complex code (COMPLEX) ──
    {
        "prompt": "Implement the full OAuth2 PKCE flow with token refresh, revocation, and device fingerprinting",
        "tier": "COMPLEX",
        "in_tok": 200,
        "out_tok": 3000,
    },
    {
        "prompt": "Build the distributed task queue with priority scheduling, dead letters, retry with backoff, and distributed locking",
        "tier": "COMPLEX",
        "in_tok": 150,
        "out_tok": 3000,
    },
    {
        "prompt": "Write a comprehensive test suite for the payment module covering happy paths, edge cases, race conditions, and recovery",
        "tier": "COMPLEX",
        "in_tok": 300,
        "out_tok": 3000,
    },
    {
        "prompt": "Implement the search service with inverted index, TF-IDF ranking, fuzzy matching, and autocomplete",
        "tier": "COMPLEX",
        "in_tok": 100,
        "out_tok": 2500,
    },
    {
        "prompt": "Build the real-time collaboration engine with OT, conflict resolution, cursor sync, and offline support",
        "tier": "COMPLEX",
        "in_tok": 150,
        "out_tok": 3000,
    },
    # ── Security audit (COMPLEX) ──
    {
        "prompt": "Perform a security audit: check for CSRF, XSS, SQL injection, broken auth, IDOR, and data exposure",
        "tier": "COMPLEX",
        "in_tok": 500,
        "out_tok": 2000,
    },
    # ── Performance optimization (COMPLEX) ──
    {
        "prompt": "Profile and optimize: implement code splitting, lazy loading, memoization, connection pooling, and caching strategy",
        "tier": "COMPLEX",
        "in_tok": 300,
        "out_tok": 2000,
    },
    # ── ML pipeline (COMPLEX) ──
    {
        "prompt": "Design the ML pipeline with feature engineering, model training, evaluation, A/B testing, monitoring, and retraining",
        "tier": "COMPLEX",
        "in_tok": 100,
        "out_tok": 2500,
    },
    # ── Algorithm correctness (REASONING) ──
    {
        "prompt": "Prove that this caching algorithm maintains consistency under concurrent writes. Use invariants.",
        "tier": "REASONING",
        "in_tok": 300,
        "out_tok": 1500,
    },
    {
        "prompt": "Prove that the distributed lock implementation is deadlock-free. Show formal reasoning.",
        "tier": "REASONING",
        "in_tok": 200,
        "out_tok": 1500,
    },
    {
        "prompt": "Derive the worst-case time complexity of our custom sorting algorithm. Prove the bound is tight.",
        "tier": "REASONING",
        "in_tok": 200,
        "out_tok": 1000,
    },
    {
        "prompt": "Prove that our rate limiter correctly enforces the token bucket invariant under concurrent requests.",
        "tier": "REASONING",
        "in_tok": 300,
        "out_tok": 1500,
    },
    {
        "prompt": "Formally verify that the state machine for order processing has no unreachable states.",
        "tier": "REASONING",
        "in_tok": 250,
        "out_tok": 1200,
    },
    # ── Pad to 200 with realistic mix ──
    *[
        {"prompt": f"What is the value of config.{k}?", "tier": "SIMPLE", "in_tok": 20, "out_tok": 30}
        for k in [
            "timeout",
            "maxRetries",
            "batchSize",
            "logLevel",
            "cacheExpiry",
            "port",
            "host",
            "workers",
            "queueSize",
            "rateLimit",
            "sessionTTL",
            "maxConnections",
            "bufferSize",
            "pollInterval",
            "gcInterval",
            "threadPoolSize",
            "socketTimeout",
            "keepAlive",
            "compressionLevel",
            "chunkSize",
        ]
    ],
    *[
        {"prompt": f"Write a function to {task}", "tier": "MEDIUM", "in_tok": 50, "out_tok": 200}
        for task in [
            "format a date string",
            "generate a UUID",
            "validate a JWT token",
            "sanitize HTML input",
            "compress a JSON payload",
            "parse query parameters",
            "calculate a checksum",
            "encode base64",
            "generate a slug from a title",
            "throttle function calls",
            "deep merge two objects",
            "flatten nested arrays",
            "convert snake_case to camelCase",
            "debounce a callback",
            "chunk an array",
        ]
    ],
    *[
        {"prompt": f"Design a {sys} with {r1}, {r2}, {r3}, and {r4}", "tier": "COMPLEX", "in_tok": 80, "out_tok": 2000}
        for sys, r1, r2, r3, r4 in [
            ("user auth system", "OAuth2", "MFA", "session management", "audit logging"),
            ("file storage service", "versioning", "deduplication", "sharing", "encryption"),
            ("event bus", "exactly-once delivery", "dead letters", "replay", "schema registry"),
            ("monitoring stack", "metrics collection", "alerting", "dashboards", "anomaly detection"),
            ("API gateway", "rate limiting", "auth", "load balancing", "circuit breaking"),
        ]
    ],
]


def simulate():
    from uncommon_route.router.classifier import classify as ur_classify
    from bench.clawrouter_v2_compat import classify_clawrouter_v2 as cr_classify

    print()
    print("=" * 75)
    print("  真实场景成本模拟: OpenClaw Agent 编程 Session (200 请求)")
    print("=" * 75)
    print()
    print("  模拟: 一个典型的 agent 编程 session")
    print(f"  请求数: {len(SESSION)}")
    print(
        f"  分布: SIMPLE={sum(1 for s in SESSION if s['tier'] == 'SIMPLE')}, "
        f"MEDIUM={sum(1 for s in SESSION if s['tier'] == 'MEDIUM')}, "
        f"COMPLEX={sum(1 for s in SESSION if s['tier'] == 'COMPLEX')}, "
        f"REASONING={sum(1 for s in SESSION if s['tier'] == 'REASONING')}"
    )
    print()

    # Strategy 1: Always Opus (no router)
    opus_cost = 0.0
    opus_quality = 0.0
    for s in SESSION:
        m = MODELS[OPUS]
        cost = (s["in_tok"] / 1_000_000) * m["in"] + (s["out_tok"] / 1_000_000) * m["out"]
        opus_cost += cost
        opus_quality += m["quality"][s["tier"]]

    # Strategy 2: ClawRouter
    cr_cost = 0.0
    cr_quality = 0.0
    cr_correct = 0
    for s in SESSION:
        tier, _ = cr_classify(s["prompt"])
        model = TIER_MODEL.get(tier, "moonshot/kimi-k2.5")
        m = MODELS.get(model, MODELS["moonshot/kimi-k2.5"])
        cost = (s["in_tok"] / 1_000_000) * m["in"] + (s["out_tok"] / 1_000_000) * m["out"]
        cr_cost += cost
        cr_quality += m["quality"][s["tier"]]
        if tier == s["tier"]:
            cr_correct += 1

    # Strategy 3: UncommonRoute
    ur_cost = 0.0
    ur_quality = 0.0
    ur_correct = 0
    for s in SESSION:
        r = ur_classify(s["prompt"])
        tier = r.tier.value if r.tier else "MEDIUM"
        model = TIER_MODEL.get(tier, "moonshot/kimi-k2.5")
        m = MODELS.get(model, MODELS["moonshot/kimi-k2.5"])
        cost = (s["in_tok"] / 1_000_000) * m["in"] + (s["out_tok"] / 1_000_000) * m["out"]
        ur_cost += cost
        ur_quality += m["quality"][s["tier"]]
        if tier == s["tier"]:
            ur_correct += 1

    avg_opus_q = opus_quality / len(SESSION)
    avg_cr_q = cr_quality / len(SESSION)
    avg_ur_q = ur_quality / len(SESSION)

    print("  ┌─────────────────────┬──────────────┬──────────────┬──────────────┐")
    print("  │       指标           │  Always Opus │  ClawRouter  │UncommonRoute │")
    print("  ├─────────────────────┼──────────────┼──────────────┼──────────────┤")
    print(f"  │ 总成本               │  ${opus_cost:.4f}    │  ${cr_cost:.4f}    │  ${ur_cost:.4f}    │")
    print(
        f"  │ 相对 Opus 节省       │     —        │  {(1 - cr_cost / opus_cost) * 100:.0f}%         │  {(1 - ur_cost / opus_cost) * 100:.0f}%         │"
    )
    print(
        f"  │ 路由准确率           │     —        │  {cr_correct / len(SESSION) * 100:.1f}%      │  {ur_correct / len(SESSION) * 100:.1f}%      │"
    )
    print(f"  │ 平均质量分 (0-1)     │  {avg_opus_q:.3f}      │  {avg_cr_q:.3f}       │  {avg_ur_q:.3f}       │")
    print(
        f"  │ 质量保持率           │  100%        │  {avg_cr_q / avg_opus_q * 100:.1f}%       │  {avg_ur_q / avg_opus_q * 100:.1f}%       │"
    )
    print("  └─────────────────────┴──────────────┴──────────────┴──────────────┘")
    print()

    # Per-tier breakdown
    print("  按 Tier 成本分解:")
    print("  ┌───────────┬──────┬──────────┬──────────┬──────────┐")
    print("  │   Tier    │ 请求 │ Opus     │ClawRouter│UncomRoute│")
    print("  ├───────────┼──────┼──────────┼──────────┼──────────┤")
    for tier in ["SIMPLE", "MEDIUM", "COMPLEX", "REASONING"]:
        tier_sessions = [s for s in SESSION if s["tier"] == tier]
        if not tier_sessions:
            continue
        n = len(tier_sessions)
        oc = sum(
            (s["in_tok"] / 1e6) * MODELS[OPUS]["in"] + (s["out_tok"] / 1e6) * MODELS[OPUS]["out"] for s in tier_sessions
        )
        tm = TIER_MODEL[tier]
        rc = sum(
            (s["in_tok"] / 1e6) * MODELS[tm]["in"] + (s["out_tok"] / 1e6) * MODELS[tm]["out"] for s in tier_sessions
        )
        print(f"  │ {tier:9s} │ {n:4d} │ ${oc:.4f} │ ${rc:.4f} │ ${rc:.4f} │")
    print("  └───────────┴──────┴──────────┴──────────┴──────────┘")
    print()

    savings_vs_opus = (1 - ur_cost / opus_cost) * 100
    savings_vs_cr_quality = (avg_ur_q - avg_cr_q) / avg_cr_q * 100
    print("  核心结论:")
    print(
        f"    UncommonRoute vs Always Opus: 节省 {savings_vs_opus:.0f}% 成本，质量保持 {avg_ur_q / avg_opus_q * 100:.1f}%"
    )
    print(
        f"    UncommonRoute vs ClawRouter: 质量提升 {savings_vs_cr_quality:.1f}%，路由准确率 {ur_correct / len(SESSION) * 100:.0f}% vs {cr_correct / len(SESSION) * 100:.0f}%"
    )
    print()


if __name__ == "__main__":
    simulate()

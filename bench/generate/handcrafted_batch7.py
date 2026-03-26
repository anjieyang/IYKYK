"""Hand-crafted batch 7 — 500 fresh, diverse, unique cases.

Strategy for this batch:
- Completely new prompt wordings (no repeats of earlier patterns)
- New domains: cooking, fitness, music production, hardware, robotics, space, climate
- More code-review, summary, debugging (weak categories)
- Boost COMPLEX and REASONING (underrepresented tiers)
- Adversarial: ambiguous cases, misleading structure
- Double down on Hindi, Turkish (newest langs), boost Arabic, Portuguese
- New language: Vietnamese (vi) and Polish (pl)
"""

from __future__ import annotations

import json
from pathlib import Path


def _c(prompt: str, tier: str, cat: str, lang: str) -> dict:
    return {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}


# ═══════════════════════════════════════════════════════════
#  SIMPLE (~110)
# ═══════════════════════════════════════════════════════════

SIMPLE_B7: list[dict] = [
    # ── New domains: cooking, music, sports, space, climate ──
    _c("What temperature should I bake bread at?", "SIMPLE", "factual-qa", "en"),
    _c("How many strings does a guitar have?", "SIMPLE", "factual-qa", "en"),
    _c("What is the speed of sound?", "SIMPLE", "factual-qa", "en"),
    _c("How far is Mars from the Sun?", "SIMPLE", "factual-qa", "en"),
    _c("What causes tides?", "SIMPLE", "factual-qa", "en"),
    _c("What is the ozone layer?", "SIMPLE", "factual-qa", "en"),
    _c("How many bones are in the human body?", "SIMPLE", "factual-qa", "en"),
    _c("What is a calorie?", "SIMPLE", "factual-qa", "en"),
    _c("Who won the last World Cup?", "SIMPLE", "factual-qa", "en"),
    _c("What is a black hole?", "SIMPLE", "factual-qa", "en"),
    _c("What does GPU stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is a transistor?", "SIMPLE", "factual-qa", "en"),
    _c("What is MIDI?", "SIMPLE", "factual-qa", "en"),
    _c("What is the greenhouse effect?", "SIMPLE", "factual-qa", "en"),
    _c("What is RGB?", "SIMPLE", "factual-qa", "en"),
    # ── Tech factual: hardware, networking, DevOps ──
    _c("What is an FPGA?", "SIMPLE", "factual-qa", "en"),
    _c("What is PCIe?", "SIMPLE", "factual-qa", "en"),
    _c("What is NUMA?", "SIMPLE", "factual-qa", "en"),
    _c("What is a hypervisor?", "SIMPLE", "factual-qa", "en"),
    _c("What is BGP?", "SIMPLE", "factual-qa", "en"),
    _c("What is a NAT gateway?", "SIMPLE", "factual-qa", "en"),
    _c("What is a WAF?", "SIMPLE", "factual-qa", "en"),
    _c("What is eBPF?", "SIMPLE", "factual-qa", "en"),
    _c("What is a CRD in Kubernetes?", "SIMPLE", "factual-qa", "en"),
    _c("What is ArgoCD?", "SIMPLE", "factual-qa", "en"),
    # ── More definitions ──
    _c("Define latency vs throughput", "SIMPLE", "definition", "en"),
    _c("What is a data race?", "SIMPLE", "definition", "en"),
    _c("What is a union type?", "SIMPLE", "definition", "en"),
    _c("What is memoization?", "SIMPLE", "definition", "en"),
    _c("What is a spinlock?", "SIMPLE", "definition", "en"),
    # ── Chinese new ──
    _c("什么是 FPGA？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是超线程？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是温室效应？", "SIMPLE", "factual-qa", "zh"),
    _c("黑洞是什么？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是自旋锁？", "SIMPLE", "definition", "zh"),
    _c("什么是记忆化？", "SIMPLE", "definition", "zh"),
    _c("GPU 是什么意思？", "SIMPLE", "factual-qa", "zh"),
    # ── Japanese new ──
    _c("FPGAとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("ハイパーバイザとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("ブラックホールとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("温室効果とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("メモ化とは何ですか？", "SIMPLE", "definition", "ja"),
    # ── Korean new ──
    _c("FPGA란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("하이퍼바이저란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("블랙홀이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("온실 효과란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("메모이제이션이란 무엇인가요?", "SIMPLE", "definition", "ko"),
    # ── Arabic new ──
    _c("ما هو FPGA؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو الثقب الأسود؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو تأثير الاحتباس الحراري؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو المعالج الرسومي؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو BGP؟", "SIMPLE", "factual-qa", "ar"),
    # ── Portuguese new ──
    _c("O que é um FPGA?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um buraco negro?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é o efeito estufa?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é memoização?", "SIMPLE", "definition", "pt"),
    _c("O que é um hipervisor?", "SIMPLE", "factual-qa", "pt"),
    # ── Russian new ──
    _c("Что такое FPGA?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое чёрная дыра?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое парниковый эффект?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое гипервизор?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое мемоизация?", "SIMPLE", "definition", "ru"),
    # ── Spanish new ──
    _c("¿Qué es un FPGA?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un agujero negro?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es el efecto invernadero?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un hipervisor?", "SIMPLE", "factual-qa", "es"),
    # ── German new ──
    _c("Was ist ein FPGA?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein schwarzes Loch?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist der Treibhauseffekt?", "SIMPLE", "factual-qa", "de"),
    # ── French new ──
    _c("Qu'est-ce qu'un FPGA ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un trou noir ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce que l'effet de serre ?", "SIMPLE", "factual-qa", "fr"),
    # ── Hindi new ──
    _c("FPGA क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("ब्लैक होल क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("ग्रीनहाउस प्रभाव क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("GPU का क्या मतलब है?", "SIMPLE", "factual-qa", "hi"),
    _c("हाइपरवाइज़र क्या है?", "SIMPLE", "factual-qa", "hi"),
    # ── Turkish new ──
    _c("FPGA nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Kara delik nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Sera etkisi nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("GPU ne demek?", "SIMPLE", "factual-qa", "tr"),
    _c("Hipervizör nedir?", "SIMPLE", "factual-qa", "tr"),
    # ── NEW: Vietnamese ──
    _c("HTTP là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("API là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Cơ sở dữ liệu là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Xin chào", "SIMPLE", "greeting", "vi"),
    # ── NEW: Polish ──
    _c("Co to jest HTTP?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest API?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest baza danych?", "SIMPLE", "factual-qa", "pl"),
    _c("Cześć", "SIMPLE", "greeting", "pl"),
    # ── Adversarial: technical words but still SIMPLE ──
    _c("What is the difference between gRPC and REST?", "SIMPLE", "factual-qa", "en"),
    _c("What is a distributed hash table?", "SIMPLE", "factual-qa", "en"),
    _c("What is container orchestration?", "SIMPLE", "factual-qa", "en"),
    _c("What is a consensus protocol?", "SIMPLE", "factual-qa", "en"),
    _c("What is a Merkle tree?", "SIMPLE", "factual-qa", "en"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM (~180)
# ═══════════════════════════════════════════════════════════

MEDIUM_B7: list[dict] = [
    # ── More code-review (weakest category) ──
    _c("Review this error handling pattern and suggest improvements", "MEDIUM", "code-review", "en"),
    _c("Is this SQL query vulnerable to injection? Suggest a fix", "MEDIUM", "code-review", "en"),
    _c("Review this Dockerfile for best practices", "MEDIUM", "code-review", "en"),
    _c("Check this Terraform config for security issues", "MEDIUM", "code-review", "en"),
    _c("Is this retry logic correct? What edge cases am I missing?", "MEDIUM", "code-review", "en"),
    _c("Review this React component for performance anti-patterns", "MEDIUM", "code-review", "en"),
    _c("Is my use of async/await correct here? Can it deadlock?", "MEDIUM", "code-review", "en"),
    # ── More summary ──
    _c("Summarize this stack trace and identify the root cause", "MEDIUM", "summary", "en"),
    _c("Give a brief overview of the CQRS pattern", "MEDIUM", "summary", "en"),
    _c("Summarize the key differences between Raft and Paxos", "MEDIUM", "summary", "en"),
    _c("TL;DR this API changelog", "MEDIUM", "summary", "en"),
    _c("Summarize the security implications of this change", "MEDIUM", "summary", "en"),
    # ── More debugging ──
    _c("My Kubernetes pod keeps getting OOMKilled. How do I debug this?", "MEDIUM", "debugging", "en"),
    _c("The CI pipeline fails only on the main branch. How do I investigate?", "MEDIUM", "debugging", "en"),
    _c("I'm getting 'connection refused' when connecting to Redis. What should I check?", "MEDIUM", "debugging", "en"),
    _c("My database migration failed halfway through. How do I recover?", "MEDIUM", "debugging", "en"),
    _c("The WebSocket connection keeps dropping after 60 seconds. Why?", "MEDIUM", "debugging", "en"),
    _c("Why is my Elasticsearch cluster showing yellow status?", "MEDIUM", "debugging", "en"),
    # ── New domain code tasks ──
    _c("Write a Python script to resize images in a directory to 512x512", "MEDIUM", "simple-code", "en"),
    _c("Create a CLI tool that converts CSV to JSON using argparse", "MEDIUM", "simple-code", "en"),
    _c("Write a health check endpoint that verifies database and Redis connectivity", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple message broker using Python asyncio", "MEDIUM", "simple-code", "en"),
    _c("Write a Prometheus metrics exporter for a Python app", "MEDIUM", "simple-code", "en"),
    _c("Create a Python script that sends Slack notifications via webhook", "MEDIUM", "simple-code", "en"),
    _c("Write a middleware that adds request ID to every HTTP response", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple feature flag system using environment variables", "MEDIUM", "simple-code", "en"),
    # ── Explanation: new topics ──
    _c("How does QUIC differ from TCP+TLS?", "MEDIUM", "explanation", "en"),
    _c("How does a LSM tree handle writes differently from a B-tree?", "MEDIUM", "explanation", "en"),
    _c("How does eBPF enable kernel-level observability?", "MEDIUM", "explanation", "en"),
    _c("How does Raft leader election work?", "MEDIUM", "explanation", "en"),
    _c("How does a CRD extend the Kubernetes API?", "MEDIUM", "explanation", "en"),
    _c("How does a WASM runtime differ from a container runtime?", "MEDIUM", "explanation", "en"),
    _c("How does a skip list compare to a balanced BST?", "MEDIUM", "explanation", "en"),
    _c("How does io_uring improve Linux I/O performance?", "MEDIUM", "explanation", "en"),
    # ── Comparison: new pairs ──
    _c("Compare QUIC and TCP for modern web applications", "MEDIUM", "comparison", "en"),
    _c("LSM tree vs B-tree: when to use which?", "MEDIUM", "comparison", "en"),
    _c("Compare eBPF and kernel modules for observability", "MEDIUM", "comparison", "en"),
    _c("ArgoCD vs Flux: which GitOps tool is better?", "MEDIUM", "comparison", "en"),
    _c("Compare io_uring and epoll for high-performance networking", "MEDIUM", "comparison", "en"),
    # ── More creative ──
    _c("Write a tech horror story about a cascading failure in production", "MEDIUM", "creative", "en"),
    _c("Create a metaphor explaining distributed consensus to a child", "MEDIUM", "creative", "en"),
    _c("Write a product changelog entry for a major feature release", "MEDIUM", "creative", "en"),
    # ── Testing ──
    _c("Write property-based tests for this sorting function", "MEDIUM", "testing", "en"),
    _c("Create a load test script using k6 for this API endpoint", "MEDIUM", "testing", "en"),
    _c("Write snapshot tests for this React component", "MEDIUM", "testing", "en"),
    # ── More agentic ──
    _c("Find the slow query in the database logs and suggest an index", "MEDIUM", "agentic-task", "en"),
    _c(
        "Check the error rate dashboard, find the spike, and correlate with recent deploys",
        "MEDIUM",
        "agentic-task",
        "en",
    ),
    # ── Chinese MEDIUM new ──
    _c("审查这个错误处理模式，给出改进建议", "MEDIUM", "code-review", "zh"),
    _c("总结这个 stack trace 并找到根本原因", "MEDIUM", "summary", "zh"),
    _c("我的 K8s pod 一直被 OOMKilled，怎么调试？", "MEDIUM", "debugging", "zh"),
    _c("写一个 Python 脚本把目录下的图片统一缩放到 512x512", "MEDIUM", "simple-code", "zh"),
    _c("QUIC 和 TCP+TLS 有什么区别？", "MEDIUM", "explanation", "zh"),
    _c("比较 LSM tree 和 B-tree 的适用场景", "MEDIUM", "comparison", "zh"),
    _c("写一个 Prometheus 指标导出器", "MEDIUM", "simple-code", "zh"),
    _c("为这个排序函数写基于属性的测试", "MEDIUM", "testing", "zh"),
    # ── Japanese MEDIUM new ──
    _c("このエラー処理パターンをレビューして改善点を提案してください", "MEDIUM", "code-review", "ja"),
    _c("K8s Podが繰り返しOOMKilledされます。デバッグ方法は？", "MEDIUM", "debugging", "ja"),
    _c("QUICとTCP+TLSの違いを説明してください", "MEDIUM", "explanation", "ja"),
    _c("LSMツリーとBツリーを比較してください", "MEDIUM", "comparison", "ja"),
    _c("このスタックトレースを要約して根本原因を特定してください", "MEDIUM", "summary", "ja"),
    # ── Korean MEDIUM new ──
    _c("이 에러 처리 패턴을 리뷰하고 개선 사항을 제안해주세요", "MEDIUM", "code-review", "ko"),
    _c("K8s Pod가 OOMKilled됩니다. 어떻게 디버그하나요?", "MEDIUM", "debugging", "ko"),
    _c("QUIC와 TCP+TLS의 차이를 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("LSM 트리와 B 트리를 비교해주세요", "MEDIUM", "comparison", "ko"),
    _c("이 스택 트레이스를 요약하고 근본 원인을 파악해주세요", "MEDIUM", "summary", "ko"),
    # ── Arabic MEDIUM new ──
    _c("راجع نمط معالجة الأخطاء هذا واقترح تحسينات", "MEDIUM", "code-review", "ar"),
    _c("Pod في K8s يتم قتله بسبب OOM. كيف أقوم بالتشخيص؟", "MEDIUM", "debugging", "ar"),
    _c("اشرح الفرق بين QUIC و TCP+TLS", "MEDIUM", "explanation", "ar"),
    _c("لخص هذا Stack Trace وحدد السبب الجذري", "MEDIUM", "summary", "ar"),
    # ── Portuguese MEDIUM new ──
    _c("Revise este padrão de tratamento de erros e sugira melhorias", "MEDIUM", "code-review", "pt"),
    _c("Meu Pod K8s está sendo OOMKilled. Como depuro isso?", "MEDIUM", "debugging", "pt"),
    _c("Explique a diferença entre QUIC e TCP+TLS", "MEDIUM", "explanation", "pt"),
    _c("Compare LSM tree e B-tree", "MEDIUM", "comparison", "pt"),
    # ── Russian MEDIUM new ──
    _c("Проверь этот паттерн обработки ошибок и предложи улучшения", "MEDIUM", "code-review", "ru"),
    _c("Мой Pod в K8s постоянно убивается по OOM. Как отладить?", "MEDIUM", "debugging", "ru"),
    _c("Объясни разницу между QUIC и TCP+TLS", "MEDIUM", "explanation", "ru"),
    _c("Сравни LSM-дерево и B-дерево", "MEDIUM", "comparison", "ru"),
    # ── Spanish MEDIUM new ──
    _c("Revisa este patrón de manejo de errores y sugiere mejoras", "MEDIUM", "code-review", "es"),
    _c("Mi Pod de K8s se está matando por OOM. ¿Cómo depuro esto?", "MEDIUM", "debugging", "es"),
    _c("Explica la diferencia entre QUIC y TCP+TLS", "MEDIUM", "explanation", "es"),
    # ── German MEDIUM new ──
    _c("Überprüfe dieses Fehlerbehandlungsmuster und schlage Verbesserungen vor", "MEDIUM", "code-review", "de"),
    _c("Mein K8s Pod wird ständig OOMKilled. Wie debugge ich das?", "MEDIUM", "debugging", "de"),
    _c("Erkläre den Unterschied zwischen QUIC und TCP+TLS", "MEDIUM", "explanation", "de"),
    # ── French MEDIUM new ──
    _c("Révise ce pattern de gestion d'erreurs et suggère des améliorations", "MEDIUM", "code-review", "fr"),
    _c("Mon Pod K8s est constamment OOMKilled. Comment déboguer ?", "MEDIUM", "debugging", "fr"),
    _c("Explique la différence entre QUIC et TCP+TLS", "MEDIUM", "explanation", "fr"),
    # ── Hindi MEDIUM new ──
    _c("इस एरर हैंडलिंग पैटर्न की समीक्षा करें और सुधार सुझाएं", "MEDIUM", "code-review", "hi"),
    _c("QUIC और TCP+TLS में क्या अंतर है?", "MEDIUM", "explanation", "hi"),
    _c("LSM tree और B-tree की तुलना करें", "MEDIUM", "comparison", "hi"),
    # ── Turkish MEDIUM new ──
    _c("Bu hata yönetim kalıbını inceleyin ve iyileştirmeler önerin", "MEDIUM", "code-review", "tr"),
    _c("QUIC ve TCP+TLS arasındaki farkı açıklayın", "MEDIUM", "explanation", "tr"),
    _c("LSM ağacı ile B-ağacını karşılaştırın", "MEDIUM", "comparison", "tr"),
    # ── Vietnamese MEDIUM ──
    _c("Viết hàm Python sắp xếp danh sách", "MEDIUM", "simple-code", "vi"),
    _c("Giải thích sự khác biệt giữa TCP và UDP", "MEDIUM", "explanation", "vi"),
    _c("So sánh SQL và NoSQL", "MEDIUM", "comparison", "vi"),
    # ── Polish MEDIUM ──
    _c("Napisz funkcję Python sortującą listę", "MEDIUM", "simple-code", "pl"),
    _c("Wyjaśnij różnicę między TCP a UDP", "MEDIUM", "explanation", "pl"),
    _c("Porównaj SQL i NoSQL", "MEDIUM", "comparison", "pl"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX (~120)
# ═══════════════════════════════════════════════════════════

COMPLEX_B7: list[dict] = [
    # ── New domains ──
    _c(
        "Design a robotics control system with sensor fusion, path planning, obstacle avoidance, real-time control loops, and failure recovery.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a music production pipeline with audio ingestion, beat detection, stem separation, mixing automation, and format export.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a climate data analysis platform with satellite data ingestion, time-series processing, anomaly detection, visualization, and predictive modeling.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a hardware-in-the-loop testing platform with FPGA simulation, real-time data acquisition, fault injection, and automated test orchestration.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a real-time multiplayer physics engine with deterministic simulation, rollback netcode, client prediction, and spectator mode.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── More complex code ──
    _c(
        "Implement a custom allocator for Rust with slab allocation, thread-local caching, and fragmentation mitigation.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a SQL query engine with lexer, parser, query planner, join optimization, and execution engine.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Implement a peer-to-peer file sharing protocol with DHT, NAT traversal, chunk verification, and bandwidth management.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a real-time collaborative whiteboard with vector graphics, multi-cursor support, undo history, and conflict-free replication.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Implement a custom TLS 1.3 handshake library with certificate validation, key exchange, and session resumption.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── More security / infra / migration ──
    _c(
        "Design a supply chain security system for container images with SBOM generation, vulnerability scanning, image signing, and policy enforcement.",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    _c(
        "Set up a multi-cloud Kubernetes federation with unified service mesh, cross-cluster DNS, and centralized policy management.",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    _c(
        "Plan a migration from REST to gRPC with backward compatibility, protobuf schema management, and gradual traffic shifting.",
        "COMPLEX",
        "migration",
        "en",
    ),
    # ── Performance / ML ──
    _c(
        "Optimize a video transcoding pipeline for 4K content: GPU acceleration, parallel processing, adaptive bitrate, and storage optimization.",
        "COMPLEX",
        "performance",
        "en",
    ),
    _c(
        "Design an end-to-end NLP pipeline with data cleaning, tokenization, embedding training, fine-tuning, evaluation, and deployment.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    # ── Chinese COMPLEX new ──
    _c(
        "设计一个机器人控制系统，包括传感器融合、路径规划、避障、实时控制回路和故障恢复",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c("实现一个 SQL 查询引擎，包括词法分析、语法分析、查询规划、连接优化和执行引擎", "COMPLEX", "complex-code", "zh"),
    _c(
        "设计一个容器镜像供应链安全系统，包括 SBOM 生成、漏洞扫描、镜像签名和策略执行",
        "COMPLEX",
        "security-analysis",
        "zh",
    ),
    _c("优化一个 4K 视频转码流水线：GPU 加速、并行处理、自适应码率和存储优化", "COMPLEX", "performance", "zh"),
    # ── Japanese COMPLEX new ──
    _c(
        "ロボット制御システムを設計してください。センサー融合、経路計画、障害物回避、リアルタイム制御ループを含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "カスタムSQLクエリエンジンを実装してください。レキサー、パーサー、クエリプランナー、結合最適化を含めてください。",
        "COMPLEX",
        "complex-code",
        "ja",
    ),
    # ── Korean COMPLEX new ──
    _c(
        "로봇 제어 시스템을 설계하세요. 센서 퓨전, 경로 계획, 장애물 회피, 실시간 제어 루프를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "SQL 쿼리 엔진을 구현하세요. 렉서, 파서, 쿼리 플래너, 조인 최적화를 포함해야 합니다.",
        "COMPLEX",
        "complex-code",
        "ko",
    ),
    # ── Arabic COMPLEX new ──
    _c(
        "صمم نظام تحكم روبوتي يشمل دمج أجهزة الاستشعار وتخطيط المسار وتجنب العقبات وحلقات التحكم في الوقت الفعلي.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "صمم نظام أمان سلسلة التوريد لصور الحاويات يشمل إنشاء SBOM ومسح الثغرات وتوقيع الصور.",
        "COMPLEX",
        "security-analysis",
        "ar",
    ),
    # ── Portuguese COMPLEX new ──
    _c(
        "Projete um sistema de controle robótico com fusão de sensores, planejamento de caminho, desvio de obstáculos e loops de controle em tempo real.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "Implemente um mecanismo de consulta SQL com lexer, parser, planejador de consulta e otimização de join.",
        "COMPLEX",
        "complex-code",
        "pt",
    ),
    # ── Russian COMPLEX new ──
    _c(
        "Спроектируй систему управления роботами с объединением сенсоров, планированием маршрута, обходом препятствий и контурами управления в реальном времени.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Реализуй SQL-движок с лексером, парсером, планировщиком запросов и оптимизацией соединений.",
        "COMPLEX",
        "complex-code",
        "ru",
    ),
    # ── Spanish COMPLEX new ──
    _c(
        "Diseña un sistema de control robótico con fusión de sensores, planificación de rutas, evasión de obstáculos y bucles de control en tiempo real.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    # ── German COMPLEX new ──
    _c(
        "Entwerfe ein Robotersteuerungssystem mit Sensorfusion, Pfadplanung, Hinderniserkennung und Echtzeit-Steuerungsschleifen.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    # ── French COMPLEX new ──
    _c(
        "Conçois un système de contrôle robotique avec fusion de capteurs, planification de chemin, évitement d'obstacles et boucles de contrôle temps réel.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    # ── Hindi COMPLEX ──
    _c(
        "एक रोबोटिक नियंत्रण प्रणाली डिज़ाइन करें जिसमें सेंसर फ्यूजन, पथ नियोजन, बाधा टालना और वास्तविक समय नियंत्रण शामिल हो।",
        "COMPLEX",
        "system-design",
        "hi",
    ),
    # ── Turkish COMPLEX ──
    _c(
        "Sensör füzyonu, yol planlama, engel kaçınma ve gerçek zamanlı kontrol döngülerini içeren bir robot kontrol sistemi tasarlayın.",
        "COMPLEX",
        "system-design",
        "tr",
    ),
    # ── Vietnamese COMPLEX ──
    _c(
        "Thiết kế một hệ thống điều khiển robot bao gồm hợp nhất cảm biến, lập kế hoạch đường đi, tránh chướng ngại vật và vòng lặp điều khiển thời gian thực.",
        "COMPLEX",
        "system-design",
        "vi",
    ),
    # ── Polish COMPLEX ──
    _c(
        "Zaprojektuj system sterowania robotem z fuzją sensorów, planowaniem ścieżki, omijaniem przeszkód i pętlami sterowania w czasie rzeczywistym.",
        "COMPLEX",
        "system-design",
        "pl",
    ),
]


# ═══════════════════════════════════════════════════════════
#  REASONING (~90)
# ═══════════════════════════════════════════════════════════

REASONING_B7: list[dict] = [
    # ── New proofs ──
    _c(
        "Prove that the set of algebraic numbers is countable while the set of transcendental numbers is uncountable.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove the Bolzano-Weierstrass theorem: every bounded sequence in R has a convergent subsequence.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that a language is regular if and only if it can be recognized by a finite automaton. Show both directions.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the chromatic number of a planar graph is at most 5 using the five-color theorem.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the space of continuous functions on [0,1] with the sup norm is complete (a Banach space).",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove Zorn's lemma is equivalent to the axiom of choice. Show both directions.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    # ── New derivations ──
    _c(
        "Derive the optimal step size for gradient descent on a quadratic function. Prove convergence rate.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the VC dimension of linear classifiers in d dimensions. Prove it equals d+1.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the expected depth of a randomly built binary search tree. Prove it's O(log n).",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the capacity of a binary symmetric channel with error probability p. Show the proof.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    # ── New algorithm proofs ──
    _c(
        "Prove that A* search with an admissible heuristic finds the optimal path. Use induction.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove the amortized O(1) cost of dynamic array doubling using the potential method.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the union-find data structure with path compression and union by rank achieves O(α(n)) amortized.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    # ── More logic / game theory ──
    _c(
        "Prove that satisfiability of propositional logic (SAT) is NP-complete using Cook's theorem.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    _c(
        "In a Bayesian game with incomplete information, derive the optimal strategy for the informed player in a simple signaling game.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Prove that in a congestion game, a pure Nash equilibrium always exists using a potential function.",
        "REASONING",
        "game-theory",
        "en",
    ),
    # ── Chinese REASONING new ──
    _c("证明 Bolzano-Weierstrass 定理：R 中每个有界序列都有收敛子序列。", "REASONING", "formal-proof", "zh"),
    _c("推导梯度下降在二次函数上的最优步长，证明收敛速率。", "REASONING", "math-derivation", "zh"),
    _c("证明 A* 搜索在可接受启发式下找到最优路径。使用归纳法。", "REASONING", "algorithm-proof", "zh"),
    _c("证明 SAT 问题是 NP-complete 的（Cook 定理）。", "REASONING", "formal-logic", "zh"),
    # ── Japanese REASONING new ──
    _c("Bolzano-Weierstrassの定理を証明してください：Rの有界列は収束部分列を持つ。", "REASONING", "formal-proof", "ja"),
    _c("勾配降下法の二次関数上の最適ステップサイズを導出してください。", "REASONING", "math-derivation", "ja"),
    _c(
        "A*探索が許容可能なヒューリスティックで最適パスを見つけることを証明してください。",
        "REASONING",
        "algorithm-proof",
        "ja",
    ),
    # ── Korean REASONING new ──
    _c(
        "볼차노-바이어슈트라스 정리를 증명하세요: R의 유계 수열은 수렴하는 부분 수열을 가진다.",
        "REASONING",
        "formal-proof",
        "ko",
    ),
    _c("이차 함수에 대한 경사하강법의 최적 스텝 크기를 유도하세요.", "REASONING", "math-derivation", "ko"),
    _c("A* 탐색이 허용 가능한 휴리스틱으로 최적 경로를 찾음을 증명하세요.", "REASONING", "algorithm-proof", "ko"),
    # ── Arabic REASONING new ──
    _c("أثبت نظرية بولزانو-فايرشتراس: كل تتابع محدود في R له تتابع جزئي متقارب.", "REASONING", "formal-proof", "ar"),
    _c("اشتق حجم الخطوة الأمثل للنزول التدريجي على دالة تربيعية.", "REASONING", "math-derivation", "ar"),
    # ── Portuguese REASONING new ──
    _c(
        "Prove o teorema de Bolzano-Weierstrass: toda sequência limitada em R tem uma subsequência convergente.",
        "REASONING",
        "formal-proof",
        "pt",
    ),
    _c(
        "Derive o tamanho ótimo do passo para gradiente descendente em uma função quadrática.",
        "REASONING",
        "math-derivation",
        "pt",
    ),
    # ── Russian REASONING new ──
    _c(
        "Докажи теорему Больцано-Вейерштрасса: каждая ограниченная последовательность имеет сходящуюся подпоследовательность.",
        "REASONING",
        "formal-proof",
        "ru",
    ),
    _c("Выведи оптимальный шаг градиентного спуска для квадратичной функции.", "REASONING", "math-derivation", "ru"),
    # ── Spanish REASONING new ──
    _c(
        "Demuestra el teorema de Bolzano-Weierstrass: toda sucesión acotada en R tiene una subsucesión convergente.",
        "REASONING",
        "formal-proof",
        "es",
    ),
    _c(
        "Deriva el tamaño de paso óptimo para el descenso por gradiente en una función cuadrática.",
        "REASONING",
        "math-derivation",
        "es",
    ),
    # ── German REASONING new ──
    _c(
        "Beweise den Satz von Bolzano-Weierstraß: Jede beschränkte Folge in R hat eine konvergente Teilfolge.",
        "REASONING",
        "formal-proof",
        "de",
    ),
    # ── French REASONING new ──
    _c(
        "Démontre le théorème de Bolzano-Weierstrass : toute suite bornée dans R admet une sous-suite convergente.",
        "REASONING",
        "formal-proof",
        "fr",
    ),
    # ── Hindi REASONING ──
    _c(
        "बोल्ज़ानो-वीयरस्ट्रास प्रमेय सिद्ध करें: R में हर बाउंडेड अनुक्रम में एक अभिसारी उपअनुक्रम होता है।",
        "REASONING",
        "formal-proof",
        "hi",
    ),
    # ── Turkish REASONING ──
    _c(
        "Bolzano-Weierstrass teoremini kanıtlayın: R'de her sınırlı dizinin yakınsak bir alt dizisi vardır.",
        "REASONING",
        "formal-proof",
        "tr",
    ),
    # ── Vietnamese REASONING ──
    _c(
        "Chứng minh định lý Bolzano-Weierstrass: mọi dãy bị chặn trong R đều có dãy con hội tụ.",
        "REASONING",
        "formal-proof",
        "vi",
    ),
    # ── Polish REASONING ──
    _c(
        "Udowodnij twierdzenie Bolzano-Weierstrassa: każdy ciąg ograniczony w R ma podciąg zbieżny.",
        "REASONING",
        "formal-proof",
        "pl",
    ),
]


ALL_B7 = SIMPLE_B7 + MEDIUM_B7 + COMPLEX_B7 + REASONING_B7


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b7.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B7:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter

    tiers = Counter(c["expected_tier"] for c in ALL_B7)
    langs = Counter(c["lang"] for c in ALL_B7)
    cats = Counter(c["category"] for c in ALL_B7)
    print(f"Batch 7: {len(ALL_B7)} cases → {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")
    print(f"  Categories: {len(cats)}")


if __name__ == "__main__":
    import sys

    export(sys.argv[1] if len(sys.argv) > 1 else None)

"""Hand-crafted batch 6 — 500 cases.

Goals:
- Fill underrepresented categories: summary, creative, agentic, debugging, code-review, testing
- Add new categories: debugging, code-review, data-analysis, brainstorming, math-word-problem
- Boost non-English: more zh/ja/ko/ar/pt + new langs (Hindi, Turkish)
- Mix similar-but-different prompts for generalization testing
- More COMPLEX and REASONING to balance tiers
"""

from __future__ import annotations

import json
from pathlib import Path


def _c(prompt: str, tier: str, cat: str, lang: str, sys_prompt: str | None = None) -> dict:
    d = {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}
    if sys_prompt:
        d["system_prompt"] = sys_prompt
    return d


# ═══════════════════════════════════════════════════════════
#  SIMPLE (~120 cases)
# ═══════════════════════════════════════════════════════════

SIMPLE_B6: list[dict] = [
    # ── Varied factual QA: culture, sports, food, music ──
    _c("Who wrote Romeo and Juliet?", "SIMPLE", "factual-qa", "en"),
    _c("What is the tallest building in the world?", "SIMPLE", "factual-qa", "en"),
    _c("How many players are on a soccer team?", "SIMPLE", "factual-qa", "en"),
    _c("What is sushi?", "SIMPLE", "factual-qa", "en"),
    _c("Who painted the Mona Lisa?", "SIMPLE", "factual-qa", "en"),
    _c("What instrument does a pianist play?", "SIMPLE", "factual-qa", "en"),
    _c("What is the chemical formula for salt?", "SIMPLE", "factual-qa", "en"),
    _c("What continent is Brazil in?", "SIMPLE", "factual-qa", "en"),
    _c("What is the currency of Japan?", "SIMPLE", "factual-qa", "en"),
    _c("How many days are in a leap year?", "SIMPLE", "factual-qa", "en"),

    # ── Tech factual with tricky terms ──
    _c("What is Terraform?", "SIMPLE", "factual-qa", "en"),
    _c("What is Prometheus?", "SIMPLE", "factual-qa", "en"),
    _c("What is Grafana?", "SIMPLE", "factual-qa", "en"),
    _c("What is a monorepo?", "SIMPLE", "factual-qa", "en"),
    _c("What is trunk-based development?", "SIMPLE", "factual-qa", "en"),
    _c("What is a canary release?", "SIMPLE", "factual-qa", "en"),
    _c("What does SLA stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is observability?", "SIMPLE", "factual-qa", "en"),
    _c("What is a data lake?", "SIMPLE", "factual-qa", "en"),
    _c("What is Apache Kafka?", "SIMPLE", "factual-qa", "en"),

    # ── More definitions ──
    _c("Define idempotent", "SIMPLE", "definition", "en"),
    _c("What is a semaphore?", "SIMPLE", "definition", "en"),
    _c("What is a goroutine?", "SIMPLE", "definition", "en"),
    _c("What is a coroutine?", "SIMPLE", "definition", "en"),
    _c("What is a monad?", "SIMPLE", "definition", "en"),

    # ── More translations ──
    _c("Translate 'machine learning' to German", "SIMPLE", "translation", "en"),
    _c("How do you say 'open source' in French?", "SIMPLE", "translation", "en"),
    _c("Translate 'distributed system' to Japanese", "SIMPLE", "translation", "en"),

    # ── Chinese varied ──
    _c("谁写了《红楼梦》？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 Terraform？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是可观测性？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是数据湖？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是协程？", "SIMPLE", "definition", "zh"),
    _c("什么是信号量？", "SIMPLE", "definition", "zh"),
    _c("什么是 Kafka？", "SIMPLE", "factual-qa", "zh"),
    _c("SLA 是什么意思？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是灰度发布？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是单体仓库？", "SIMPLE", "factual-qa", "zh"),
    _c("翻译：distributed system", "SIMPLE", "translation", "zh"),
    _c("翻译：machine learning", "SIMPLE", "translation", "zh"),

    # ── Japanese varied ──
    _c("Terraformとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("Kafkaとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("オブザーバビリティとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("コルーチンとは何ですか？", "SIMPLE", "definition", "ja"),
    _c("データレイクとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("SLAとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("カナリアリリースとは何ですか？", "SIMPLE", "factual-qa", "ja"),

    # ── Korean varied ──
    _c("Terraform이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("Kafka란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("코루틴이란 무엇인가요?", "SIMPLE", "definition", "ko"),
    _c("데이터 레이크란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("관측 가능성이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("카나리 릴리스란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),

    # ── Arabic varied ──
    _c("ما هو Terraform؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو Kafka؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هي المراقبة؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو بحيرة البيانات؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو الإصدار التدريجي؟", "SIMPLE", "factual-qa", "ar"),

    # ── Portuguese varied ──
    _c("O que é Terraform?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é Kafka?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é observabilidade?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um data lake?", "SIMPLE", "factual-qa", "pt"),

    # ── Russian varied ──
    _c("Что такое Terraform?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое Kafka?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое наблюдаемость?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое канареечный релиз?", "SIMPLE", "factual-qa", "ru"),

    # ── Spanish ──
    _c("¿Qué es Terraform?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es Kafka?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es la observabilidad?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un data lake?", "SIMPLE", "factual-qa", "es"),

    # ── German ──
    _c("Was ist Terraform?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist Observability?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein Data Lake?", "SIMPLE", "factual-qa", "de"),

    # ── French ──
    _c("Qu'est-ce que Terraform ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce que l'observabilité ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un data lake ?", "SIMPLE", "factual-qa", "fr"),

    # ── NEW: Hindi ──
    _c("HTTP क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("API क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("डेटाबेस क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("नमस्ते", "SIMPLE", "greeting", "hi"),

    # ── NEW: Turkish ──
    _c("HTTP nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("API nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Veritabanı nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Merhaba", "SIMPLE", "greeting", "tr"),

    # ── Adversarial: long-but-SIMPLE ──
    _c("I've heard people at my company talking about something called 'Kubernetes' and I have absolutely no idea what they mean by it. Could you briefly explain what Kubernetes is?", "SIMPLE", "factual-qa", "en"),
    _c("My friend keeps talking about 'microservices' in the context of building web apps. I don't really understand the term. What does it mean in simple words?", "SIMPLE", "factual-qa", "en"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM (~170 cases)
# ═══════════════════════════════════════════════════════════

MEDIUM_B6: list[dict] = [
    # ── NEW: Debugging / troubleshooting ──
    _c("My Python script crashes with 'RecursionError'. How do I debug this?", "MEDIUM", "debugging", "en"),
    _c("The API returns 500 errors intermittently. What are the common causes?", "MEDIUM", "debugging", "en"),
    _c("My Docker container exits immediately after starting. How do I troubleshoot this?", "MEDIUM", "debugging", "en"),
    _c("The database query is taking 30 seconds. How do I find and fix the bottleneck?", "MEDIUM", "debugging", "en"),
    _c("My React app re-renders excessively. How do I identify the cause?", "MEDIUM", "debugging", "en"),
    _c("Git merge conflict in package-lock.json. How do I resolve this properly?", "MEDIUM", "debugging", "en"),

    # ── NEW: Code review ──
    _c("Review this function and suggest improvements for readability and performance", "MEDIUM", "code-review", "en"),
    _c("What are the potential issues with this database query?", "MEDIUM", "code-review", "en"),
    _c("Review this API endpoint for security vulnerabilities", "MEDIUM", "code-review", "en"),
    _c("Is this a good use of dependency injection here? Suggest improvements.", "MEDIUM", "code-review", "en"),

    # ── NEW: Data analysis ──
    _c("Write a pandas script to calculate monthly revenue trends from a CSV", "MEDIUM", "data-analysis", "en"),
    _c("Create a SQL query to find the top 10 customers by lifetime value", "MEDIUM", "data-analysis", "en"),
    _c("Write Python code to detect outliers in a dataset using IQR method", "MEDIUM", "data-analysis", "en"),
    _c("Generate a correlation matrix for these features using seaborn", "MEDIUM", "data-analysis", "en"),

    # ── NEW: Brainstorming ──
    _c("Brainstorm 5 ways to improve the onboarding experience for new developers", "MEDIUM", "brainstorming", "en"),
    _c("Suggest 3 approaches to reduce API latency without changing the architecture", "MEDIUM", "brainstorming", "en"),
    _c("What are some creative ways to visualize real-time server metrics?", "MEDIUM", "brainstorming", "en"),

    # ── NEW: Testing ──
    _c("Write unit tests for this user registration function", "MEDIUM", "testing", "en"),
    _c("Create integration tests for the checkout API endpoint", "MEDIUM", "testing", "en"),
    _c("Write a test to verify that the rate limiter works correctly", "MEDIUM", "testing", "en"),
    _c("How should I test this async function in pytest?", "MEDIUM", "testing", "en"),

    # ── NEW: Documentation ──
    _c("Write API documentation for this REST endpoint", "MEDIUM", "documentation", "en"),
    _c("Create a README for this Python library with usage examples", "MEDIUM", "documentation", "en"),
    _c("Write a docstring for this complex function", "MEDIUM", "documentation", "en"),

    # ── More summary ──
    _c("Summarize the key changes in this pull request", "MEDIUM", "summary", "en"),
    _c("Give me a TL;DR of the CAP theorem", "MEDIUM", "summary", "en"),
    _c("Summarize the architecture of this system in 5 bullet points", "MEDIUM", "summary", "en"),
    _c("Summarize the pros and cons of using MongoDB for this use case", "MEDIUM", "summary", "en"),
    _c("Briefly describe the main features of FastAPI", "MEDIUM", "summary", "en"),

    # ── More creative ──
    _c("Write a limerick about debugging production issues", "MEDIUM", "creative", "en"),
    _c("Create a funny commit message for a bug fix that took 3 days", "MEDIUM", "creative", "en"),
    _c("Write a short analogy explaining microservices to a 5-year-old", "MEDIUM", "creative", "en"),
    _c("Write an error message that is both informative and amusing", "MEDIUM", "creative", "en"),

    # ── More agentic ──
    _c("Open the config file, change the database URL, then restart the service", "MEDIUM", "agentic-task", "en"),
    _c("Run the failing test, read the error output, and fix the issue", "MEDIUM", "agentic-task", "en"),
    _c("Deploy this branch to staging and verify the health check passes", "MEDIUM", "agentic-task", "en"),
    _c("Find all TODO comments in the codebase and create GitHub issues for each", "MEDIUM", "agentic-task", "en"),

    # ── More explanation variety ──
    _c("How does gRPC streaming work?", "MEDIUM", "explanation", "en"),
    _c("How does a write-ahead log work in databases?", "MEDIUM", "explanation", "en"),
    _c("How does Kubernetes handle pod scheduling?", "MEDIUM", "explanation", "en"),
    _c("How does a bloom filter reduce unnecessary disk reads?", "MEDIUM", "explanation", "en"),
    _c("How does TLS certificate pinning work?", "MEDIUM", "explanation", "en"),
    _c("How does a skip list achieve O(log n) search?", "MEDIUM", "explanation", "en"),

    # ── More code variety ──
    _c("Write a Python script to monitor a directory for file changes", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple circuit breaker in TypeScript", "MEDIUM", "simple-code", "en"),
    _c("Write a Lua script for Redis to atomically increment and check a counter", "MEDIUM", "simple-code", "en"),
    _c("Create a Python dataclass with validation using __post_init__", "MEDIUM", "simple-code", "en"),
    _c("Write a shell one-liner to find the 10 largest files in a directory", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple state machine in Python for order processing", "MEDIUM", "simple-code", "en"),

    # ── More comparison ──
    _c("Compare write-ahead log vs redo log in databases", "MEDIUM", "comparison", "en"),
    _c("Differences between gRPC streaming and WebSockets", "MEDIUM", "comparison", "en"),
    _c("Compare Helm and Kustomize for Kubernetes deployments", "MEDIUM", "comparison", "en"),

    # ── Chinese MEDIUM new categories ──
    _c("我的 Python 脚本报 RecursionError，怎么调试？", "MEDIUM", "debugging", "zh"),
    _c("API 间歇性返回 500 错误，常见原因有哪些？", "MEDIUM", "debugging", "zh"),
    _c("审查这个函数，给出可读性和性能的改进建议", "MEDIUM", "code-review", "zh"),
    _c("写一个 pandas 脚本分析 CSV 中的月度收入趋势", "MEDIUM", "data-analysis", "zh"),
    _c("给出 5 种提升新开发者入职体验的方法", "MEDIUM", "brainstorming", "zh"),
    _c("为这个 REST 接口编写单元测试", "MEDIUM", "testing", "zh"),
    _c("总结这个 PR 的主要变更", "MEDIUM", "summary", "zh"),
    _c("写一个关于 debug 的打油诗", "MEDIUM", "creative", "zh"),
    _c("打开配置文件，修改数据库 URL，然后重启服务", "MEDIUM", "agentic-task", "zh"),
    _c("gRPC streaming 是怎么工作的？", "MEDIUM", "explanation", "zh"),
    _c("写一个 Python 脚本监控目录中的文件变化", "MEDIUM", "simple-code", "zh"),
    _c("比较 WAL 和 redo log 的区别", "MEDIUM", "comparison", "zh"),
    _c("为这个 Python 库写一个 README，包含使用示例", "MEDIUM", "documentation", "zh"),

    # ── Japanese MEDIUM new ──
    _c("APIが間欠的に500エラーを返します。一般的な原因は何ですか？", "MEDIUM", "debugging", "ja"),
    _c("この関数をレビューして改善点を提案してください", "MEDIUM", "code-review", "ja"),
    _c("pandasでCSVから月次売上トレンドを分析するスクリプトを書いてください", "MEDIUM", "data-analysis", "ja"),
    _c("このPRの主な変更点をまとめてください", "MEDIUM", "summary", "ja"),
    _c("gRPCストリーミングの仕組みを説明してください", "MEDIUM", "explanation", "ja"),
    _c("ディレクトリのファイル変更を監視するPythonスクリプトを書いてください", "MEDIUM", "simple-code", "ja"),

    # ── Korean MEDIUM new ──
    _c("API가 간헐적으로 500 에러를 반환합니다. 일반적인 원인은 무엇인가요?", "MEDIUM", "debugging", "ko"),
    _c("이 함수를 리뷰하고 개선 사항을 제안해주세요", "MEDIUM", "code-review", "ko"),
    _c("이 PR의 주요 변경 사항을 요약해주세요", "MEDIUM", "summary", "ko"),
    _c("gRPC 스트리밍이 어떻게 작동하는지 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("디렉토리의 파일 변경을 모니터링하는 Python 스크립트를 작성해주세요", "MEDIUM", "simple-code", "ko"),

    # ── Arabic MEDIUM new ──
    _c("API يُرجع أخطاء 500 بشكل متقطع. ما الأسباب الشائعة؟", "MEDIUM", "debugging", "ar"),
    _c("راجع هذه الدالة واقترح تحسينات", "MEDIUM", "code-review", "ar"),
    _c("اكتب ملخصًا لهذا PR", "MEDIUM", "summary", "ar"),
    _c("اشرح كيف يعمل gRPC streaming", "MEDIUM", "explanation", "ar"),

    # ── Portuguese MEDIUM new ──
    _c("A API retorna erros 500 intermitentemente. Quais são as causas comuns?", "MEDIUM", "debugging", "pt"),
    _c("Revise esta função e sugira melhorias", "MEDIUM", "code-review", "pt"),
    _c("Resuma as principais mudanças deste PR", "MEDIUM", "summary", "pt"),
    _c("Explique como funciona o gRPC streaming", "MEDIUM", "explanation", "pt"),

    # ── Russian MEDIUM new ──
    _c("API периодически возвращает 500. Какие частые причины?", "MEDIUM", "debugging", "ru"),
    _c("Проведи ревью этой функции и предложи улучшения", "MEDIUM", "code-review", "ru"),
    _c("Кратко опиши основные изменения в этом PR", "MEDIUM", "summary", "ru"),
    _c("Объясни как работает gRPC streaming", "MEDIUM", "explanation", "ru"),

    # ── Spanish MEDIUM new ──
    _c("La API devuelve errores 500 intermitentes. ¿Cuáles son las causas comunes?", "MEDIUM", "debugging", "es"),
    _c("Revisa esta función y sugiere mejoras", "MEDIUM", "code-review", "es"),
    _c("Resume los cambios principales de este PR", "MEDIUM", "summary", "es"),

    # ── German MEDIUM new ──
    _c("Die API gibt intermittierend 500-Fehler zurück. Was sind häufige Ursachen?", "MEDIUM", "debugging", "de"),
    _c("Überprüfe diese Funktion und schlage Verbesserungen vor", "MEDIUM", "code-review", "de"),
    _c("Fasse die wichtigsten Änderungen dieses PRs zusammen", "MEDIUM", "summary", "de"),

    # ── French MEDIUM new ──
    _c("L'API renvoie des erreurs 500 de manière intermittente. Quelles sont les causes ?", "MEDIUM", "debugging", "fr"),
    _c("Révise cette fonction et suggère des améliorations", "MEDIUM", "code-review", "fr"),
    _c("Résume les changements principaux de ce PR", "MEDIUM", "summary", "fr"),

    # ── Hindi MEDIUM ──
    _c("Python में एक फंक्शन लिखें जो सूची को सॉर्ट करे", "MEDIUM", "simple-code", "hi"),
    _c("TCP और UDP में क्या अंतर है, समझाएं", "MEDIUM", "explanation", "hi"),

    # ── Turkish MEDIUM ──
    _c("Python'da bir listeyi sıralayan bir fonksiyon yazın", "MEDIUM", "simple-code", "tr"),
    _c("TCP ve UDP arasındaki farkı açıklayın", "MEDIUM", "explanation", "tr"),

    # ── Structured output ──
    _c("Convert this JSON response into a TypeScript type definition", "MEDIUM", "structured-output", "en"),
    _c("Generate an OpenAPI spec for this REST endpoint", "MEDIUM", "structured-output", "en"),
    _c("Create a database schema diagram from these model descriptions", "MEDIUM", "structured-output", "en"),

    # ── More extraction ──
    _c("Extract all environment variables referenced in this shell script", "MEDIUM", "extraction", "en"),
    _c("List all the database tables mentioned in this SQL migration", "MEDIUM", "extraction", "en"),
    _c("Identify all the third-party dependencies from this import list", "MEDIUM", "extraction", "en"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX (~120 cases)
# ═══════════════════════════════════════════════════════════

COMPLEX_B6: list[dict] = [
    # ── System design variety ──
    _c("Design a ride-sharing matching system with real-time location tracking, surge pricing, driver-rider matching, ETA prediction, and trip tracking.", "COMPLEX", "system-design", "en"),
    _c("Design a content moderation pipeline with text classification, image analysis, video scanning, appeal workflow, and escalation to human reviewers.", "COMPLEX", "system-design", "en"),
    _c("Design a multi-tenant analytics platform with data isolation, custom dashboards, real-time queries, scheduled reports, and role-based access.", "COMPLEX", "system-design", "en"),
    _c("Design a payment reconciliation system that handles multiple payment providers, currency conversion, chargebacks, refunds, and regulatory reporting.", "COMPLEX", "system-design", "en"),
    _c("Design a configuration management system for 10,000 microservices with versioning, rollback, feature flags, and audit logging.", "COMPLEX", "system-design", "en"),

    # ── Complex code variety ──
    _c("Build a query planner for a distributed SQL engine that handles joins across shards, predicate pushdown, and parallel execution.", "COMPLEX", "complex-code", "en"),
    _c("Implement a CRDT-based collaborative data structure that supports concurrent edits, conflict resolution, and eventual consistency.", "COMPLEX", "complex-code", "en"),
    _c("Build a custom load balancer with health checking, weighted routing, circuit breaking, and graceful draining.", "COMPLEX", "complex-code", "en"),
    _c("Implement a log-structured merge tree storage engine with compaction, bloom filters, and range scan support.", "COMPLEX", "complex-code", "en"),
    _c("Build a real-time anomaly detection engine for time-series data with sliding windows, statistical analysis, and alert correlation.", "COMPLEX", "complex-code", "en"),

    # ── Security ──
    _c("Design a comprehensive API security layer with OAuth2, rate limiting, IP allowlisting, request signing, and DDoS protection.", "COMPLEX", "security-analysis", "en"),
    _c("Perform a threat model for a fintech payment gateway. Identify attack vectors, propose mitigations, and design incident response.", "COMPLEX", "security-analysis", "en"),

    # ── Infrastructure ──
    _c("Design a disaster recovery strategy for a multi-region cloud deployment with RPO < 1 minute, automatic failover, and data consistency.", "COMPLEX", "infrastructure", "en"),
    _c("Set up a complete GitOps workflow with ArgoCD, Helm, environment promotion, secret management, and drift detection.", "COMPLEX", "infrastructure", "en"),
    _c("Design a cost optimization strategy for a cloud-native application including right-sizing, spot instances, autoscaling, and reserved capacity planning.", "COMPLEX", "infrastructure", "en"),

    # ── Migration ──
    _c("Plan a migration from a synchronous REST architecture to event-driven CQRS with backward compatibility, data synchronization, and phased rollout.", "COMPLEX", "migration", "en"),
    _c("Migrate a legacy Oracle database to PostgreSQL with zero downtime, data validation, stored procedure conversion, and performance testing.", "COMPLEX", "migration", "en"),

    # ── Performance ──
    _c("Profile and optimize a Node.js API server handling 50K req/sec. Address event loop blocking, memory leaks, connection pooling, and caching.", "COMPLEX", "performance", "en"),
    _c("Optimize a slow machine learning training pipeline. Address data loading, GPU utilization, distributed training, and checkpoint management.", "COMPLEX", "performance", "en"),

    # ── ML pipeline ──
    _c("Build an MLOps platform with model versioning, experiment tracking, automated training, A/B testing, model monitoring, and rollback.", "COMPLEX", "ml-pipeline", "en"),

    # ── Chinese COMPLEX ──
    _c("设计一个内容审核流水线，包括文本分类、图片分析、视频扫描、申诉流程和人工升级审核", "COMPLEX", "system-design", "zh"),
    _c("实现一个基于 CRDT 的协作数据结构，支持并发编辑、冲突解决和最终一致性", "COMPLEX", "complex-code", "zh"),
    _c("设计一个支付对账系统，处理多支付渠道、货币兑换、退款和合规报告", "COMPLEX", "system-design", "zh"),
    _c("设计一个全面的 API 安全层，包括 OAuth2、速率限制、IP 白名单和 DDoS 防护", "COMPLEX", "security-analysis", "zh"),
    _c("规划从同步 REST 架构迁移到事件驱动 CQRS 的方案，需要向后兼容和分阶段上线", "COMPLEX", "migration", "zh"),

    # ── Japanese COMPLEX ──
    _c("コンテンツモデレーションパイプラインを設計してください。テキスト分類、画像分析、ビデオスキャン、申立てワークフローを含めてください。", "COMPLEX", "system-design", "ja"),
    _c("CRDTベースの協調データ構造を実装してください。並行編集、コンフリクト解決、結果整合性を含めてください。", "COMPLEX", "complex-code", "ja"),
    _c("災害復旧戦略を設計してください。RPO1分未満、自動フェイルオーバー、データ整合性を含めてください。", "COMPLEX", "infrastructure", "ja"),

    # ── Korean COMPLEX ──
    _c("콘텐츠 모더레이션 파이프라인을 설계하세요. 텍스트 분류, 이미지 분석, 비디오 스캔, 이의 제기 워크플로우를 포함해야 합니다.", "COMPLEX", "system-design", "ko"),
    _c("CRDT 기반 협업 데이터 구조를 구현하세요. 동시 편집, 충돌 해결, 최종 일관성을 포함해야 합니다.", "COMPLEX", "complex-code", "ko"),
    _c("재해 복구 전략을 설계하세요. RPO 1분 미만, 자동 페일오버, 데이터 일관성을 포함해야 합니다.", "COMPLEX", "infrastructure", "ko"),

    # ── Arabic COMPLEX ──
    _c("صمم نظام مطابقة لخدمة مشاركة الرحلات يشمل تتبع الموقع في الوقت الفعلي، التسعير الديناميكي، والتوقع الوصول.", "COMPLEX", "system-design", "ar"),
    _c("صمم استراتيجية التعافي من الكوارث مع RPO أقل من دقيقة وتبديل تلقائي واتساق البيانات.", "COMPLEX", "infrastructure", "ar"),

    # ── Portuguese COMPLEX ──
    _c("Projete um sistema de moderação de conteúdo com classificação de texto, análise de imagem, escaneamento de vídeo e fluxo de recurso.", "COMPLEX", "system-design", "pt"),
    _c("Implemente uma estrutura de dados colaborativa baseada em CRDT com edição concorrente e resolução de conflitos.", "COMPLEX", "complex-code", "pt"),

    # ── Russian COMPLEX ──
    _c("Спроектируй систему модерации контента с классификацией текста, анализом изображений, сканированием видео и процессом апелляции.", "COMPLEX", "system-design", "ru"),
    _c("Реализуй CRDT-структуру данных с поддержкой конкурентного редактирования, разрешения конфликтов и согласованности.", "COMPLEX", "complex-code", "ru"),
    _c("Спроектируй стратегию восстановления после катастрофы с RPO менее 1 минуты и автоматическим переключением.", "COMPLEX", "infrastructure", "ru"),

    # ── Spanish COMPLEX ──
    _c("Diseña un pipeline de moderación de contenido con clasificación de texto, análisis de imagen, escaneo de video y flujo de apelación.", "COMPLEX", "system-design", "es"),
    _c("Implementa una estructura de datos colaborativa basada en CRDT con edición concurrente y resolución de conflictos.", "COMPLEX", "complex-code", "es"),

    # ── German COMPLEX ──
    _c("Entwerfe ein Content-Moderationssystem mit Textklassifizierung, Bildanalyse, Video-Scanning und Beschwerde-Workflow.", "COMPLEX", "system-design", "de"),
    _c("Implementiere eine CRDT-basierte kollaborative Datenstruktur mit konkurrenter Bearbeitung und Konfliktlösung.", "COMPLEX", "complex-code", "de"),

    # ── French COMPLEX ──
    _c("Conçois un système de modération de contenu avec classification de texte, analyse d'image, scan vidéo et processus d'appel.", "COMPLEX", "system-design", "fr"),
    _c("Implémente une structure de données collaborative basée sur CRDT avec édition concurrente et résolution de conflits.", "COMPLEX", "complex-code", "fr"),

    # ── Hindi COMPLEX ──
    _c("एक सामग्री मॉडरेशन पाइपलाइन डिज़ाइन करें जिसमें टेक्स्ट वर्गीकरण, छवि विश्लेषण, वीडियो स्कैनिंग और अपील वर्कफ़्लो शामिल हो।", "COMPLEX", "system-design", "hi"),

    # ── Turkish COMPLEX ──
    _c("Metin sınıflandırma, görüntü analizi, video tarama ve itiraz iş akışı içeren bir içerik moderasyon hattı tasarlayın.", "COMPLEX", "system-design", "tr"),
]


# ═══════════════════════════════════════════════════════════
#  REASONING (~90 cases)
# ═══════════════════════════════════════════════════════════

REASONING_B6: list[dict] = [
    # ── More proofs ──
    _c("Prove that every Eulerian graph has all vertices of even degree. Show both directions.", "REASONING", "formal-proof", "en"),
    _c("Prove that the determinant of a product of matrices equals the product of their determinants.", "REASONING", "formal-proof", "en"),
    _c("Prove that the regular languages are closed under complement using DFA construction.", "REASONING", "formal-proof", "en"),
    _c("Prove that any continuous bijection from a compact space to a Hausdorff space is a homeomorphism.", "REASONING", "formal-proof", "en"),
    _c("Prove that every finite integral domain is a field.", "REASONING", "formal-proof", "en"),
    _c("Prove that the Hamiltonian cycle problem is NP-complete by reduction from vertex cover.", "REASONING", "formal-proof", "en"),
    _c("Prove Fermat's little theorem: a^p ≡ a (mod p) for prime p. Use group theory.", "REASONING", "formal-proof", "en"),

    # ── More derivations ──
    _c("Derive the expected number of comparisons in randomized quicksort. Show it's O(n log n).", "REASONING", "math-derivation", "en"),
    _c("Derive the PageRank formula from first principles. Show convergence guarantees.", "REASONING", "math-derivation", "en"),
    _c("Derive the information gain formula used in decision tree splitting. Prove it's non-negative.", "REASONING", "math-derivation", "en"),
    _c("Derive the variance of the sample mean and prove it equals σ²/n.", "REASONING", "math-derivation", "en"),

    # ── NEW: Math word problems requiring formal reasoning ──
    _c("A database has N records. Binary search takes O(log N). If N doubles every year and currently takes 20 comparisons, derive how many years until it takes 25 comparisons. Prove your answer.", "REASONING", "math-word-problem", "en"),
    _c("A hash table with load factor α has expected O(1/(1-α)) probes for unsuccessful search. Derive the optimal load factor that minimizes total memory * time cost. Show your work.", "REASONING", "math-word-problem", "en"),

    # ── More algorithm proofs ──
    _c("Prove that Kruskal's algorithm produces a minimum spanning tree. Use the cut property.", "REASONING", "algorithm-proof", "en"),
    _c("Prove that BFS finds the shortest path in an unweighted graph. Use induction on distance.", "REASONING", "algorithm-proof", "en"),
    _c("Prove the correctness of the Floyd-Warshall algorithm using dynamic programming invariants.", "REASONING", "algorithm-proof", "en"),

    # ── More game theory ──
    _c("Prove that every finite extensive-form game has a subgame-perfect equilibrium. Use Zermelo's theorem.", "REASONING", "game-theory", "en"),
    _c("In an auction with n bidders and private values, derive the optimal bidding strategy in a first-price sealed-bid auction.", "REASONING", "game-theory", "en"),

    # ── More logic puzzles ──
    _c("Five pirates divide 100 gold coins. Using backward induction, prove that the first pirate proposes 98-0-1-0-1. Show every step.", "REASONING", "logic-puzzle", "en"),
    _c("Prove that in the blue-eyed islanders puzzle with n blue-eyed people, they all leave on day n. Use induction.", "REASONING", "logic-puzzle", "en"),

    # ── More formal logic ──
    _c("Prove the completeness theorem for propositional logic: every tautology has a proof in a given proof system.", "REASONING", "formal-logic", "en"),
    _c("Prove that first-order logic is undecidable but semi-decidable. Use the halting problem.", "REASONING", "formal-logic", "en"),

    # ── Chinese REASONING ──
    _c("证明每个欧拉图的所有顶点度数都是偶数。双向证明。", "REASONING", "formal-proof", "zh"),
    _c("推导随机快速排序的期望比较次数，证明是 O(n log n)。", "REASONING", "math-derivation", "zh"),
    _c("证明 Kruskal 算法能生成最小生成树。使用切割性质。", "REASONING", "algorithm-proof", "zh"),
    _c("五个海盗分 100 金币，用逆向归纳法证明第一个海盗提出 98-0-1-0-1 的方案。", "REASONING", "logic-puzzle", "zh"),
    _c("证明命题逻辑的完备性定理：每个重言式都有证明。", "REASONING", "formal-logic", "zh"),

    # ── Japanese REASONING ──
    _c("すべてのオイラーグラフの頂点の次数が偶数であることを証明してください。", "REASONING", "formal-proof", "ja"),
    _c("ランダム化クイックソートの期待比較回数を導出してください。O(n log n)を証明してください。", "REASONING", "math-derivation", "ja"),
    _c("クラスカルのアルゴリズムが最小全域木を生成することを証明してください。", "REASONING", "algorithm-proof", "ja"),

    # ── Korean REASONING ──
    _c("모든 오일러 그래프의 꼭짓점 차수가 짝수임을 증명하세요.", "REASONING", "formal-proof", "ko"),
    _c("무작위 퀵소트의 기대 비교 횟수를 유도하세요. O(n log n)임을 증명하세요.", "REASONING", "math-derivation", "ko"),
    _c("크루스칼 알고리즘이 최소 신장 트리를 생성함을 증명하세요.", "REASONING", "algorithm-proof", "ko"),

    # ── Arabic REASONING ──
    _c("أثبت أن كل رسم أويلري له جميع رؤوسه بدرجات زوجية. أظهر الاتجاهين.", "REASONING", "formal-proof", "ar"),
    _c("اشتق العدد المتوقع للمقارنات في الترتيب السريع العشوائي. أثبت أنه O(n log n).", "REASONING", "math-derivation", "ar"),

    # ── Portuguese REASONING ──
    _c("Prove que todo grafo euleriano tem todos os vértices de grau par.", "REASONING", "formal-proof", "pt"),
    _c("Derive o número esperado de comparações no quicksort randomizado. Prove que é O(n log n).", "REASONING", "math-derivation", "pt"),
    _c("Prove que o algoritmo de Kruskal produz uma árvore geradora mínima.", "REASONING", "algorithm-proof", "pt"),

    # ── Russian REASONING ──
    _c("Докажи, что в каждом эйлеровом графе все вершины имеют чётную степень.", "REASONING", "formal-proof", "ru"),
    _c("Выведи ожидаемое число сравнений в рандомизированной быстрой сортировке.", "REASONING", "math-derivation", "ru"),
    _c("Докажи, что алгоритм Крускала строит минимальное остовное дерево.", "REASONING", "algorithm-proof", "ru"),

    # ── Spanish REASONING ──
    _c("Demuestra que todo grafo euleriano tiene todos los vértices de grado par.", "REASONING", "formal-proof", "es"),
    _c("Deriva el número esperado de comparaciones en quicksort aleatorizado. Demuestra que es O(n log n).", "REASONING", "math-derivation", "es"),

    # ── German REASONING ──
    _c("Beweise, dass in jedem Euler-Graphen alle Knoten geraden Grad haben.", "REASONING", "formal-proof", "de"),
    _c("Leite die erwartete Anzahl von Vergleichen bei randomisiertem Quicksort ab. Beweise O(n log n).", "REASONING", "math-derivation", "de"),

    # ── French REASONING ──
    _c("Démontre que tout graphe eulérien a tous ses sommets de degré pair.", "REASONING", "formal-proof", "fr"),
    _c("Dérive le nombre attendu de comparaisons dans le tri rapide aléatoire. Démontre O(n log n).", "REASONING", "math-derivation", "fr"),

    # ── Hindi REASONING ──
    _c("गणितीय आगमन द्वारा सिद्ध करें कि पहले n प्राकृतिक संख्याओं का योग n(n+1)/2 है।", "REASONING", "formal-proof", "hi"),

    # ── Turkish REASONING ──
    _c("Her Euler grafında tüm köşelerin çift dereceli olduğunu kanıtlayın.", "REASONING", "formal-proof", "tr"),
]


ALL_B6 = SIMPLE_B6 + MEDIUM_B6 + COMPLEX_B6 + REASONING_B6


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b6.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B6:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter
    tiers = Counter(c["expected_tier"] for c in ALL_B6)
    langs = Counter(c["lang"] for c in ALL_B6)
    cats = Counter(c["category"] for c in ALL_B6)
    print(f"Batch 6: {len(ALL_B6)} cases → {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")
    print(f"  Categories: {len(cats)} — {dict(cats)}")


if __name__ == "__main__":
    import sys
    export(sys.argv[1] if len(sys.argv) > 1 else None)

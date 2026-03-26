"""Hand-crafted batch 2 — expanding coverage.

Focus: more SIMPLE factual-qa across domains, more MEDIUM code/explanation variety,
more COMPLEX real-world scenarios, more REASONING across languages.
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
#  SIMPLE batch 2 — diverse domains, all languages
# ═══════════════════════════════════════════════════════════

SIMPLE_B2: list[dict] = [
    # ── Science & Math QA ──
    _c("What is photosynthesis?", "SIMPLE", "factual-qa", "en"),
    _c("What is the formula for water?", "SIMPLE", "factual-qa", "en"),
    _c("How far is the moon from Earth?", "SIMPLE", "factual-qa", "en"),
    _c("What is Newton's first law?", "SIMPLE", "factual-qa", "en"),
    _c("What is the atomic number of carbon?", "SIMPLE", "factual-qa", "en"),
    _c("What is the Pythagorean theorem?", "SIMPLE", "factual-qa", "en"),
    _c("How many chromosomes do humans have?", "SIMPLE", "factual-qa", "en"),
    _c("What is the pH of pure water?", "SIMPLE", "factual-qa", "en"),
    # ── History & Geography QA ──
    _c("When did the Berlin Wall fall?", "SIMPLE", "factual-qa", "en"),
    _c("Who was the first person on the moon?", "SIMPLE", "factual-qa", "en"),
    _c("What is the longest river in the world?", "SIMPLE", "factual-qa", "en"),
    _c("Which country has the largest population?", "SIMPLE", "factual-qa", "en"),
    _c("When was the Declaration of Independence signed?", "SIMPLE", "factual-qa", "en"),
    _c("What is the tallest mountain in the world?", "SIMPLE", "factual-qa", "en"),
    # ── Tech QA (short, factual) ──
    _c("What port does HTTP use?", "SIMPLE", "factual-qa", "en"),
    _c("What is the latest version of Python?", "SIMPLE", "factual-qa", "en"),
    _c("Who created JavaScript?", "SIMPLE", "factual-qa", "en"),
    _c("What year was Linux released?", "SIMPLE", "factual-qa", "en"),
    _c("What is the default port for PostgreSQL?", "SIMPLE", "factual-qa", "en"),
    _c("What does CRUD stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between GET and POST?", "SIMPLE", "factual-qa", "en"),
    _c("What does YAML stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is a 404 error?", "SIMPLE", "factual-qa", "en"),
    _c("What is localhost?", "SIMPLE", "factual-qa", "en"),
    _c("What is the default port for SSH?", "SIMPLE", "factual-qa", "en"),
    _c("What is a primary key in a database?", "SIMPLE", "factual-qa", "en"),
    _c("What does FIFO stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is a boolean?", "SIMPLE", "factual-qa", "en"),
    _c("What does IDE stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is an IP address?", "SIMPLE", "factual-qa", "en"),
    # ── More definitions ──
    _c("Define idempotency", "SIMPLE", "definition", "en"),
    _c("What is a deadlock?", "SIMPLE", "definition", "en"),
    _c("What is a race condition?", "SIMPLE", "definition", "en"),
    _c("What is a mutex?", "SIMPLE", "definition", "en"),
    _c("What is sharding?", "SIMPLE", "definition", "en"),
    _c("What is a webhook?", "SIMPLE", "definition", "en"),
    _c("What is a CDN?", "SIMPLE", "definition", "en"),
    _c("What is a lambda function?", "SIMPLE", "definition", "en"),
    # ── More translations ──
    _c("Translate 'database' to Chinese", "SIMPLE", "translation", "en"),
    _c("How do you say 'error' in Japanese?", "SIMPLE", "translation", "en"),
    _c("Translate 'server' to Korean", "SIMPLE", "translation", "en"),
    _c("How do you say 'algorithm' in Arabic?", "SIMPLE", "translation", "en"),
    # ── Chinese factual ──
    _c("HTTP 默认端口是多少？", "SIMPLE", "factual-qa", "zh"),
    _c("Python 是谁发明的？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是主键？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是递归？", "SIMPLE", "definition", "zh"),
    _c("什么是死锁？", "SIMPLE", "definition", "zh"),
    _c("什么是 CDN？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是容器？", "SIMPLE", "factual-qa", "zh"),
    _c("Git 是什么？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 SSH？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是负载均衡？", "SIMPLE", "factual-qa", "zh"),
    _c("翻译：good night", "SIMPLE", "translation", "zh"),
    _c("翻译：thank you very much", "SIMPLE", "translation", "zh"),
    # ── Russian factual ──
    _c("Что такое рекурсия?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое REST API?", "SIMPLE", "factual-qa", "ru"),
    _c("Какой порт использует HTTP?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое контейнер?", "SIMPLE", "factual-qa", "ru"),
    _c("Кто создал Python?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое кэш?", "SIMPLE", "definition", "ru"),
    # ── Spanish factual ──
    _c("¿Qué es una base de datos?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es recursión?", "SIMPLE", "factual-qa", "es"),
    _c("¿Cuál es el puerto predeterminado de HTTP?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un contenedor Docker?", "SIMPLE", "factual-qa", "es"),
    # ── German factual ──
    _c("Was ist Rekursion?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein Container?", "SIMPLE", "factual-qa", "de"),
    _c("Welchen Port verwendet SSH?", "SIMPLE", "factual-qa", "de"),
    # ── French factual ──
    _c("Qu'est-ce que la récursivité ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un conteneur Docker ?", "SIMPLE", "factual-qa", "fr"),
    _c("Quel port utilise SSH ?", "SIMPLE", "factual-qa", "fr"),
    # ── Japanese factual ──
    _c("再帰とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("キャッシュとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("SSHのデフォルトポートは？", "SIMPLE", "factual-qa", "ja"),
    _c("APIとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    # ── Korean factual ──
    _c("재귀란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("캐시란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("SSH의 기본 포트는 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    # ── Portuguese ──
    _c("O que é recursão?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um container Docker?", "SIMPLE", "factual-qa", "pt"),
    # ── Arabic ──
    _c("ما هو الخادم؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هي قاعدة البيانات؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو التخزين المؤقت؟", "SIMPLE", "factual-qa", "ar"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM batch 2
# ═══════════════════════════════════════════════════════════

MEDIUM_B2: list[dict] = [
    # ── More code tasks ──
    _c("Write a Python generator that yields prime numbers", "MEDIUM", "simple-code", "en"),
    _c("Implement a trie data structure in Python", "MEDIUM", "simple-code", "en"),
    _c("Write a function to merge two sorted linked lists", "MEDIUM", "simple-code", "en"),
    _c("Create a REST endpoint in FastAPI that accepts file uploads", "MEDIUM", "simple-code", "en"),
    _c("Write a JavaScript promise wrapper for setTimeout", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple pub/sub pattern in TypeScript", "MEDIUM", "simple-code", "en"),
    _c("Write a Python script to parse command line arguments using argparse", "MEDIUM", "simple-code", "en"),
    _c("Create a Makefile for a C project with build, test, and clean targets", "MEDIUM", "simple-code", "en"),
    _c("Write a GitHub Actions workflow that runs tests on every push", "MEDIUM", "simple-code", "en"),
    _c("Implement a rate limiter using the token bucket algorithm in Python", "MEDIUM", "simple-code", "en"),
    _c("Write a Python async function to fetch multiple URLs concurrently", "MEDIUM", "simple-code", "en"),
    _c("Create a SQLAlchemy model for a blog with posts and comments", "MEDIUM", "simple-code", "en"),
    _c("Write a custom React hook for debouncing input", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple middleware for Express.js that logs request duration", "MEDIUM", "simple-code", "en"),
    _c("Write a Rust function to read a CSV file and return a Vec of structs", "MEDIUM", "simple-code", "en"),
    # ── More explanations ──
    _c("Explain how database indexing works", "MEDIUM", "explanation", "en"),
    _c("How does a load balancer distribute traffic?", "MEDIUM", "explanation", "en"),
    _c("Explain what CORS is and why it exists", "MEDIUM", "explanation", "en"),
    _c("How does a CDN improve website performance?", "MEDIUM", "explanation", "en"),
    _c("Explain the difference between authentication and authorization", "MEDIUM", "explanation", "en"),
    _c("How does connection pooling work in databases?", "MEDIUM", "explanation", "en"),
    _c("Explain what a race condition is with an example", "MEDIUM", "explanation", "en"),
    _c("How does Docker layer caching work?", "MEDIUM", "explanation", "en"),
    _c("Explain how WebSockets differ from HTTP polling", "MEDIUM", "explanation", "en"),
    _c("How does the Python GIL affect multithreading?", "MEDIUM", "explanation", "en"),
    # ── More comparisons ──
    _c("Compare Kafka and RabbitMQ for message queuing", "MEDIUM", "comparison", "en"),
    _c("What are the differences between OAuth2 and SAML?", "MEDIUM", "comparison", "en"),
    _c("Compare PostgreSQL and MySQL for a new project", "MEDIUM", "comparison", "en"),
    _c("Horizontal scaling vs vertical scaling — when to use which?", "MEDIUM", "comparison", "en"),
    _c("Compare FastAPI with Django for building APIs", "MEDIUM", "comparison", "en"),
    # ── More rewrite / extract / classify ──
    _c("Rewrite this function to use list comprehension instead of a loop", "MEDIUM", "rewrite", "en"),
    _c("Convert this class-based React component to a functional component with hooks", "MEDIUM", "rewrite", "en"),
    _c("Extract all email addresses from this text", "MEDIUM", "extraction", "en"),
    _c("Identify the sentiment of each sentence in this paragraph", "MEDIUM", "classification", "en"),
    _c("Categorize these log entries by severity level", "MEDIUM", "classification", "en"),
    _c("Convert this YAML config to equivalent JSON", "MEDIUM", "structured-output", "en"),
    _c("Generate a markdown table from this CSV data", "MEDIUM", "structured-output", "en"),
    # ── Chinese MEDIUM ──
    _c("写一个 Python 异步函数来并发请求多个 URL", "MEDIUM", "simple-code", "zh"),
    _c("用 Go 实现一个简单的 HTTP 代理", "MEDIUM", "simple-code", "zh"),
    _c("解释数据库索引是怎么工作的", "MEDIUM", "explanation", "zh"),
    _c("CDN 是如何加速网站的？", "MEDIUM", "explanation", "zh"),
    _c("解释什么是 CORS 以及它为什么存在", "MEDIUM", "explanation", "zh"),
    _c("比较 Kafka 和 RabbitMQ 的优缺点", "MEDIUM", "comparison", "zh"),
    _c("比较 FastAPI 和 Django 做 API 开发的区别", "MEDIUM", "comparison", "zh"),
    _c("把这个 YAML 配置转成 JSON 格式", "MEDIUM", "structured-output", "zh"),
    _c("从这段日志中提取所有 IP 地址", "MEDIUM", "extraction", "zh"),
    _c("把这段文字翻译成正式的学术论文风格", "MEDIUM", "rewrite", "zh"),
    # ── Russian MEDIUM ──
    _c("Напиши асинхронную функцию на Python для загрузки нескольких URL", "MEDIUM", "simple-code", "ru"),
    _c("Объясни как работает индексирование в базах данных", "MEDIUM", "explanation", "ru"),
    _c("Сравни PostgreSQL и MySQL для нового проекта", "MEDIUM", "comparison", "ru"),
    _c("Извлеки все email-адреса из этого текста", "MEDIUM", "extraction", "ru"),
    # ── Japanese MEDIUM ──
    _c("データベースインデックスの仕組みを説明してください", "MEDIUM", "explanation", "ja"),
    _c("KafkaとRabbitMQを比較してください", "MEDIUM", "comparison", "ja"),
    _c("Pythonで非同期のHTTPリクエストを書いてください", "MEDIUM", "simple-code", "ja"),
    # ── Korean MEDIUM ──
    _c("데이터베이스 인덱싱이 어떻게 작동하는지 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("Python으로 비동기 HTTP 요청을 작성해주세요", "MEDIUM", "simple-code", "ko"),
    # ── German MEDIUM ──
    _c("Erkläre wie Datenbankindexierung funktioniert", "MEDIUM", "explanation", "de"),
    _c("Vergleiche PostgreSQL und MySQL", "MEDIUM", "comparison", "de"),
    _c("Schreibe ein Python-Skript zum Parsen von CSV-Dateien", "MEDIUM", "simple-code", "de"),
    # ── French MEDIUM ──
    _c("Explique comment fonctionne l'indexation des bases de données", "MEDIUM", "explanation", "fr"),
    _c("Compare Kafka et RabbitMQ", "MEDIUM", "comparison", "fr"),
    # ── Spanish MEDIUM ──
    _c("Explica cómo funciona la indexación en bases de datos", "MEDIUM", "explanation", "es"),
    _c("Compara PostgreSQL y MySQL para un proyecto nuevo", "MEDIUM", "comparison", "es"),
    _c("Escribe una función en Go para leer un archivo CSV", "MEDIUM", "simple-code", "es"),
    # ── Portuguese MEDIUM ──
    _c("Explique como funciona a indexação de banco de dados", "MEDIUM", "explanation", "pt"),
    _c("Escreva um script Python para processar argumentos de linha de comando", "MEDIUM", "simple-code", "pt"),
    # ── Arabic MEDIUM ──
    _c("اكتب دالة Python غير متزامنة لجلب عدة URLs", "MEDIUM", "simple-code", "ar"),
    _c("اشرح كيف يعمل فهرسة قاعدة البيانات", "MEDIUM", "explanation", "ar"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX batch 2
# ═══════════════════════════════════════════════════════════

COMPLEX_B2: list[dict] = [
    # ── More system designs ──
    _c(
        "Design a distributed search engine with web crawling, indexing, ranking, caching, and real-time query suggestions.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a video streaming platform supporting live streaming, transcoding, adaptive bitrate, CDN integration, and DRM.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design an e-commerce inventory system with real-time stock tracking, warehouse management, multi-channel sync, and demand forecasting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a social media feed with personalized ranking, real-time updates, pagination, content moderation, and spam detection.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── More complex code ──
    _c(
        "Build a distributed key-value store with consistent hashing, replication, conflict resolution, and membership protocol.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Implement a compiler frontend for a simple language with lexer, parser, AST, type checker, and code generation.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a container runtime from scratch supporting namespaces, cgroups, overlay filesystem, and networking.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Implement a full-text search engine with inverted index, TF-IDF scoring, fuzzy matching, and faceted search.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a database connection pool with health checking, automatic reconnection, query timeout, and connection leak detection.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── More architecture / security / infra ──
    _c(
        "Design a zero-trust security architecture for a microservices platform with mutual TLS, service mesh, RBAC, and audit logging.",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    _c(
        "Set up a multi-region active-active database deployment with conflict resolution, failover, and consistency guarantees.",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    _c(
        "Design a feature flag system supporting gradual rollouts, A/B testing, user targeting, and real-time updates without deploys.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Data engineering ──
    _c(
        "Design a real-time data lake architecture with batch and stream ingestion, schema evolution, data quality checks, and cost optimization.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    # ── Chinese COMPLEX ──
    _c(
        "设计一个分布式搜索引擎，包括网页爬取、索引构建、排名算法、缓存策略和实时搜索建议",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "构建一个完整的编译器前端，包括词法分析、语法分析、AST 构建、类型检查和代码生成",
        "COMPLEX",
        "complex-code",
        "zh",
    ),
    _c("设计一个零信任安全架构，包括 mTLS、服务网格、RBAC、审计日志和入侵检测", "COMPLEX", "security-analysis", "zh"),
    # ── Russian COMPLEX ──
    _c(
        "Спроектируй платформу для видеостриминга с транскодированием, адаптивным битрейтом, CDN и защитой контента",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Построй распределённое хранилище ключ-значение с согласованным хешированием, репликацией и обнаружением конфликтов",
        "COMPLEX",
        "complex-code",
        "ru",
    ),
    # ── Japanese COMPLEX ──
    _c(
        "分散キーバリューストアを構築してください。一貫性のあるハッシュ、レプリケーション、コンフリクト解決を含めてください。",
        "COMPLEX",
        "complex-code",
        "ja",
    ),
    # ── Korean COMPLEX ──
    _c(
        "실시간 데이터 파이프라인을 설계하세요. 배치/스트림 수집, 스키마 진화, 데이터 품질 검증을 포함해야 합니다.",
        "COMPLEX",
        "architecture",
        "ko",
    ),
    # ── German COMPLEX ──
    _c(
        "Entwerfe ein verteiltes Key-Value-Store mit konsistentem Hashing, Replikation und Konfliktlösung.",
        "COMPLEX",
        "complex-code",
        "de",
    ),
    # ── Spanish COMPLEX ──
    _c(
        "Diseña un sistema de búsqueda distribuido con rastreo web, indexación, ranking y sugerencias en tiempo real.",
        "COMPLEX",
        "system-design",
        "es",
    ),
]


# ═══════════════════════════════════════════════════════════
#  REASONING batch 2
# ═══════════════════════════════════════════════════════════

REASONING_B2: list[dict] = [
    # ── More proofs ──
    _c(
        "Prove that the set of rational numbers is countable. Use Cantor's diagonal argument.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that a graph is bipartite if and only if it contains no odd-length cycles.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove the Cauchy-Schwarz inequality using the properties of inner products. Show every step.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the intersection of two subgroups is also a subgroup. Use the subgroup criterion.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that every bounded monotone sequence in R converges. Use the completeness axiom.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    # ── More derivations ──
    _c(
        "Derive the formula for the sum of a geometric series and prove it by induction.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the time complexity of quicksort in the average case using indicator random variables.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the optimal solution to the 0-1 knapsack problem using dynamic programming. Prove correctness.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    # ── More logic puzzles ──
    _c(
        "Three people have numbers on their foreheads. They can see others' numbers but not their own. Given that the sum is 144, and each sees at least one 48, prove all numbers are 48.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    _c(
        "100 prisoners and a lightbulb puzzle: prove that a counting strategy exists for the prisoners to determine when all have visited the room.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    # ── Game theory ──
    _c(
        "Prove that in a two-player zero-sum game, the minimax strategy forms a Nash equilibrium.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "In Nim with piles of 3, 5, 7, determine the winning strategy for the first player. Prove using XOR.",
        "REASONING",
        "game-theory",
        "en",
    ),
    # ── Chinese REASONING ──
    _c("证明：有理数集是可数的。使用对角线论证法。", "REASONING", "formal-proof", "zh"),
    _c("推导等比数列求和公式，并用归纳法证明。", "REASONING", "math-derivation", "zh"),
    _c("证明：一个图是二部图当且仅当它不包含奇数长度的环。", "REASONING", "formal-proof", "zh"),
    # ── Russian REASONING ──
    _c(
        "Докажи, что множество рациональных чисел счётно, используя диагональный аргумент Кантора.",
        "REASONING",
        "formal-proof",
        "ru",
    ),
    _c("Выведи формулу суммы геометрической прогрессии и докажи её по индукции.", "REASONING", "math-derivation", "ru"),
    # ── Japanese REASONING ──
    _c("等比級数の和の公式を導出し、帰納法で証明してください。", "REASONING", "math-derivation", "ja"),
    # ── Korean REASONING ──
    _c("등비급수의 합 공식을 유도하고 귀납법으로 증명하세요.", "REASONING", "math-derivation", "ko"),
    # ── German REASONING ──
    _c(
        "Beweise, dass die Menge der rationalen Zahlen abzählbar ist. Verwende Cantors Diagonalargument.",
        "REASONING",
        "formal-proof",
        "de",
    ),
    # ── Spanish REASONING ──
    _c(
        "Demuestra que el conjunto de los números racionales es contable usando el argumento diagonal de Cantor.",
        "REASONING",
        "formal-proof",
        "es",
    ),
    # ── French REASONING ──
    _c(
        "Démontre que l'ensemble des nombres rationnels est dénombrable en utilisant l'argument diagonal de Cantor.",
        "REASONING",
        "formal-proof",
        "fr",
    ),
]


ALL_B2 = SIMPLE_B2 + MEDIUM_B2 + COMPLEX_B2 + REASONING_B2


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b2.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B2:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter

    tiers = Counter(c["expected_tier"] for c in ALL_B2)
    langs = Counter(c["lang"] for c in ALL_B2)
    print(f"Batch 2: {len(ALL_B2)} cases → {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")


if __name__ == "__main__":
    import sys

    export(sys.argv[1] if len(sys.argv) > 1 else None)

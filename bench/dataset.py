"""Labeled dataset for router classification benchmark.

Coverage: 10 languages, 30+ categories, ~150 cases.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TestCase:
    prompt: str
    expected_tier: str  # "SIMPLE" | "MEDIUM" | "COMPLEX" | "REASONING"
    category: str
    lang: str
    system_prompt: str | None = None


DATASET: list[TestCase] = [
    # ═══════════════════════════════════════
    #  SIMPLE — factual QA, translation, definition, greeting, yes/no
    # ═══════════════════════════════════════

    # English
    TestCase("What is the capital of France?", "SIMPLE", "factual-qa", "en"),
    TestCase("What does HTTP stand for?", "SIMPLE", "factual-qa", "en"),
    TestCase("Who is the CEO of Apple?", "SIMPLE", "factual-qa", "en"),
    TestCase("What year did World War 2 end?", "SIMPLE", "factual-qa", "en"),
    TestCase("What is 2 + 2?", "SIMPLE", "factual-qa", "en"),
    TestCase("Yes or no: is Python an interpreted language?", "SIMPLE", "factual-qa", "en"),
    TestCase("How many continents are there?", "SIMPLE", "factual-qa", "en"),
    TestCase("What is the boiling point of water?", "SIMPLE", "factual-qa", "en"),
    TestCase("Translate 'hello world' to Spanish", "SIMPLE", "translation", "en"),
    TestCase("How do you say 'thank you' in Japanese?", "SIMPLE", "translation", "en"),
    TestCase("Define polymorphism", "SIMPLE", "definition", "en"),
    TestCase("What is a closure in JavaScript?", "SIMPLE", "definition", "en"),
    TestCase("What is DNS?", "SIMPLE", "factual-qa", "en"),
    TestCase("Who invented the telephone?", "SIMPLE", "factual-qa", "en"),
    TestCase("Hello", "SIMPLE", "greeting", "en"),
    TestCase("Help", "SIMPLE", "greeting", "en"),
    TestCase("Thanks!", "SIMPLE", "greeting", "en"),
    TestCase("What color is the sky?", "SIMPLE", "factual-qa", "en"),

    # Chinese
    TestCase("什么是 REST API？", "SIMPLE", "factual-qa", "zh"),
    TestCase("翻译：Good morning", "SIMPLE", "translation", "zh"),
    TestCase("谁是爱因斯坦？", "SIMPLE", "factual-qa", "zh"),
    TestCase("你好", "SIMPLE", "greeting", "zh"),
    TestCase("Python 是什么语言？", "SIMPLE", "factual-qa", "zh"),
    TestCase("地球有多少颗卫星？", "SIMPLE", "factual-qa", "zh"),

    # Russian
    TestCase("Что такое HTTP?", "SIMPLE", "factual-qa", "ru"),
    TestCase("Переведи 'hello' на русский", "SIMPLE", "translation", "ru"),
    TestCase("Кто изобрёл телефон?", "SIMPLE", "factual-qa", "ru"),
    TestCase("Привет", "SIMPLE", "greeting", "ru"),
    TestCase("Сколько планет в солнечной системе?", "SIMPLE", "factual-qa", "ru"),

    # Spanish
    TestCase("¿Qué es una API?", "SIMPLE", "factual-qa", "es"),
    TestCase("Traduce 'thank you' al español", "SIMPLE", "translation", "es"),
    TestCase("Hola", "SIMPLE", "greeting", "es"),
    TestCase("¿Cuántos océanos hay?", "SIMPLE", "factual-qa", "es"),

    # Japanese
    TestCase("HTMLとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    TestCase("こんにちは", "SIMPLE", "greeting", "ja"),
    TestCase("地球の直径は？", "SIMPLE", "factual-qa", "ja"),

    # Korean
    TestCase("HTTP란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    TestCase("안녕하세요", "SIMPLE", "greeting", "ko"),

    # German
    TestCase("Was ist eine Datenbank?", "SIMPLE", "factual-qa", "de"),
    TestCase("Hallo", "SIMPLE", "greeting", "de"),
    TestCase("Übersetze 'good morning' ins Deutsche", "SIMPLE", "translation", "de"),

    # French
    TestCase("Qu'est-ce qu'une API ?", "SIMPLE", "factual-qa", "fr"),
    TestCase("Bonjour", "SIMPLE", "greeting", "fr"),

    # Portuguese
    TestCase("O que é um banco de dados?", "SIMPLE", "factual-qa", "pt"),
    TestCase("Olá", "SIMPLE", "greeting", "pt"),

    # Arabic
    TestCase("ما هو البروتوكول HTTP؟", "SIMPLE", "factual-qa", "ar"),
    TestCase("مرحبا", "SIMPLE", "greeting", "ar"),

    # ═══════════════════════════════════════
    #  MEDIUM — simple code, explanation, comparison, creative, rewrite, extraction
    # ═══════════════════════════════════════

    # English — code
    TestCase("Write a Python function that reverses a string", "MEDIUM", "simple-code", "en"),
    TestCase("Write a SQL query to find duplicate emails in a users table", "MEDIUM", "simple-code", "en"),
    TestCase("Create a simple Express.js route that returns JSON", "MEDIUM", "simple-code", "en"),
    TestCase("Write a bash script that counts lines in all .ts files", "MEDIUM", "simple-code", "en"),
    TestCase("Write a Python class for a linked list with insert and delete methods", "MEDIUM", "simple-code", "en"),
    TestCase("Write a regex to validate email addresses", "MEDIUM", "simple-code", "en"),
    TestCase("Give me a one-liner to flatten a nested array in JavaScript", "MEDIUM", "simple-code", "en"),
    TestCase("Write a function to check if a number is prime", "MEDIUM", "simple-code", "en"),
    TestCase("Create a TypeScript interface for a User object with name, email, and age", "MEDIUM", "simple-code", "en"),

    # English — explanation / comparison / summary
    TestCase("Explain the difference between TCP and UDP", "MEDIUM", "explanation", "en"),
    TestCase("Summarize the key features of React hooks", "MEDIUM", "summary", "en"),
    TestCase("Explain how async/await works in JavaScript", "MEDIUM", "explanation", "en"),
    TestCase("Compare the pros and cons of SQL vs NoSQL databases", "MEDIUM", "comparison", "en"),
    TestCase("Explain the CAP theorem in simple terms", "MEDIUM", "explanation", "en"),
    TestCase("Summarize this article in 3 bullet points", "MEDIUM", "summary", "en"),
    TestCase("What are the trade-offs between REST and GraphQL?", "MEDIUM", "comparison", "en"),
    TestCase("Describe how a hash table works internally", "MEDIUM", "explanation", "en"),

    # English — creative / rewrite / extraction / classification
    TestCase("Write a poem about recursion in the style of Shakespeare", "MEDIUM", "creative", "en"),
    TestCase("Format this data as a JSON schema with nested objects and arrays", "MEDIUM", "structured-output", "en"),
    TestCase("Rewrite this paragraph to be more concise and professional", "MEDIUM", "rewrite", "en"),
    TestCase("Extract all the dates and names from the following text", "MEDIUM", "extraction", "en"),
    TestCase("Classify these customer reviews as positive, negative, or neutral", "MEDIUM", "classification", "en"),
    TestCase("Convert this Python 2 code to Python 3", "MEDIUM", "rewrite", "en"),
    TestCase("Write a haiku about machine learning", "MEDIUM", "creative", "en"),

    # English — edge / short
    TestCase("Fix the bug", "MEDIUM", "edge-short", "en"),
    TestCase("Write code", "MEDIUM", "edge-short", "en"),
    TestCase("Refactor this", "MEDIUM", "edge-short", "en"),

    # Chinese
    TestCase("写一个 Python 函数来计算斐波那契数列", "MEDIUM", "simple-code", "zh"),
    TestCase("解释 Docker 和虚拟机的区别", "MEDIUM", "explanation", "zh"),
    TestCase("用 JavaScript 实现一个简单的防抖函数", "MEDIUM", "simple-code", "zh"),
    TestCase("总结一下 Git rebase 和 merge 的区别", "MEDIUM", "comparison", "zh"),
    TestCase("把这段文字改写成正式的商务邮件风格", "MEDIUM", "rewrite", "zh"),
    TestCase("从下面的文本中提取所有人名和地名", "MEDIUM", "extraction", "zh"),

    # Russian
    TestCase("Напиши функцию на Python для сортировки списка", "MEDIUM", "simple-code", "ru"),
    TestCase("Объясни разницу между SQL и NoSQL", "MEDIUM", "explanation", "ru"),
    TestCase("Перепиши этот текст более кратко", "MEDIUM", "rewrite", "ru"),

    # Japanese
    TestCase("Pythonでリストをソートする関数を書いてください", "MEDIUM", "simple-code", "ja"),
    TestCase("RESTとGraphQLの違いを説明してください", "MEDIUM", "explanation", "ja"),

    # Korean
    TestCase("Python으로 문자열을 뒤집는 함수를 작성해주세요", "MEDIUM", "simple-code", "ko"),
    TestCase("TCP와 UDP의 차이점을 설명해주세요", "MEDIUM", "explanation", "ko"),

    # German
    TestCase("Schreibe eine Python-Funktion, die eine Liste sortiert", "MEDIUM", "simple-code", "de"),
    TestCase("Erkläre den Unterschied zwischen REST und GraphQL", "MEDIUM", "explanation", "de"),

    # French
    TestCase("Écris une fonction Python qui inverse une chaîne de caractères", "MEDIUM", "simple-code", "fr"),

    # Portuguese
    TestCase("Escreva uma função Python que inverta uma string", "MEDIUM", "simple-code", "pt"),

    # With system prompt
    TestCase("What's the best way to handle errors here?", "MEDIUM", "explanation", "en",
             system_prompt="You are a senior Python developer reviewing code."),
    TestCase("How should I structure this component?", "MEDIUM", "explanation", "en",
             system_prompt="You are a React expert helping with frontend architecture."),

    # ═══════════════════════════════════════
    #  COMPLEX — system design, complex code, architecture, security, infra, ML, migration
    # ═══════════════════════════════════════

    # English — system design
    TestCase(
        "Design a distributed rate limiter that works across multiple microservice instances using Redis. Include the algorithm, data structures, and handle edge cases like clock skew.",
        "COMPLEX", "system-design", "en",
    ),
    TestCase(
        "Design a URL shortener service that handles 10M daily requests, with analytics, custom aliases, and expiration support.",
        "COMPLEX", "system-design", "en",
    ),
    TestCase(
        "Design a notification system that supports push, email, SMS, and in-app channels with priority queues, rate limiting, and user preference management.",
        "COMPLEX", "system-design", "en",
    ),

    # English — complex code
    TestCase(
        "Implement a full CRUD REST API with authentication, input validation, error handling, and database migrations using FastAPI and SQLAlchemy",
        "COMPLEX", "complex-code", "en",
    ),
    TestCase(
        "Write a comprehensive test suite for a payment processing module that covers happy paths, edge cases, race conditions, and failure recovery",
        "COMPLEX", "complex-code", "en",
    ),
    TestCase(
        "Build a real-time collaborative text editor with operational transformation, conflict resolution, and offline support",
        "COMPLEX", "complex-code", "en",
    ),
    TestCase(
        "Design and implement a custom database query optimizer that handles JOIN reordering, index selection, and cost-based plan selection for a subset of SQL",
        "COMPLEX", "complex-code", "en",
    ),
    TestCase(
        "Implement a B+ tree from scratch in Rust with concurrent access support, page splitting, and range queries. Include benchmarks comparing with std::BTreeMap.",
        "COMPLEX", "complex-code", "en",
    ),
    TestCase(
        "Build a web crawler that respects robots.txt, handles rate limiting, deduplicates URLs, stores results in PostgreSQL, and supports distributed crawling across multiple workers.",
        "COMPLEX", "complex-code", "en",
    ),

    # English — architecture
    TestCase(
        "Refactor this monolithic application into microservices. Identify service boundaries, define API contracts, and design the inter-service communication patterns.",
        "COMPLEX", "architecture", "en",
    ),
    TestCase(
        "Architect a real-time event processing pipeline using Kafka, with exactly-once semantics, dead letter queues, schema evolution, and multi-region failover",
        "COMPLEX", "architecture", "en",
    ),

    # English — security / infra / ML / migration
    TestCase(
        "Analyze the security vulnerabilities in this authentication flow and propose fixes for CSRF, XSS, SQL injection, and session fixation attacks",
        "COMPLEX", "security-analysis", "en",
    ),
    TestCase(
        "Create a Kubernetes deployment with auto-scaling, health checks, rolling updates, and a service mesh for a multi-tenant SaaS application",
        "COMPLEX", "infrastructure", "en",
    ),
    TestCase(
        "Design an end-to-end ML pipeline for fraud detection, including feature engineering, model training, A/B testing, monitoring, and automated retraining on data drift.",
        "COMPLEX", "ml-pipeline", "en",
    ),
    TestCase(
        "Plan and execute a zero-downtime migration from PostgreSQL to CockroachDB for a production system with 500M rows, including schema changes, data validation, and rollback strategy.",
        "COMPLEX", "migration", "en",
    ),
    TestCase(
        "Optimize the performance of this React application: implement code splitting, virtualized lists, memoization, image lazy loading, and service worker caching.",
        "COMPLEX", "performance", "en",
    ),

    # Chinese
    TestCase("设计一个支持百万级并发的分布式消息队列系统，包括消息持久化、消费者组、死信队列和监控告警", "COMPLEX", "system-design", "zh"),
    TestCase("实现一个完整的用户认证系统，包括 JWT、OAuth2、RBAC 权限控制、密码加密和审计日志", "COMPLEX", "complex-code", "zh"),
    TestCase("设计一个支持多租户的 SaaS 平台架构，包括数据隔离、计费系统、权限管理和弹性伸缩方案", "COMPLEX", "architecture", "zh"),
    TestCase("设计一个实时推荐系统，包括特征工程、模型训练、在线推理、A/B 测试和效果监控", "COMPLEX", "ml-pipeline", "zh"),

    # Russian
    TestCase("Спроектируй распределённую систему кэширования с поддержкой инвалидации, репликации и шардирования данных между узлами кластера", "COMPLEX", "system-design", "ru"),
    TestCase("Реализуй полноценный REST API с аутентификацией, валидацией, обработкой ошибок и миграциями базы данных на FastAPI", "COMPLEX", "complex-code", "ru"),

    # Japanese
    TestCase("マイクロサービスアーキテクチャで、認証、レート制限、サーキットブレーカー、分散トレーシングを含むAPIゲートウェイを設計してください", "COMPLEX", "architecture", "ja"),

    # Korean
    TestCase("분산 캐싱 시스템을 설계하세요. 캐시 무효화, 복제, 샤딩, 장애 복구를 포함해야 합니다.", "COMPLEX", "system-design", "ko"),

    # German
    TestCase("Entwerfe eine skalierbare Microservice-Architektur mit Service Discovery, Load Balancing, Circuit Breaking und verteiltem Tracing.", "COMPLEX", "architecture", "de"),

    # With system prompt
    TestCase(
        "The current latency is 2 seconds per request. Bring it under 200ms.",
        "COMPLEX", "performance", "en",
        system_prompt="You are a performance engineer. The application is a Python FastAPI service with PostgreSQL, Redis, and Elasticsearch.",
    ),

    # ═══════════════════════════════════════
    #  REASONING — formal proof, math, logic, game theory, optimization
    # ═══════════════════════════════════════

    # English
    TestCase("Prove that the halting problem is undecidable using a diagonalization argument. Show each step formally.", "REASONING", "formal-proof", "en"),
    TestCase("Derive the time complexity of the Fibonacci function using the Master Theorem. Prove it step by step.", "REASONING", "math-derivation", "en"),
    TestCase("Prove by mathematical induction that the sum of the first n natural numbers equals n(n+1)/2", "REASONING", "formal-proof", "en"),
    TestCase("Using formal logic, prove that if all men are mortal and Socrates is a man, then Socrates is mortal. Use first-order predicate logic notation.", "REASONING", "formal-logic", "en"),
    TestCase("Prove the correctness of Dijkstra's algorithm using loop invariants. Show the initialization, maintenance, and termination steps formally.", "REASONING", "algorithm-proof", "en"),
    TestCase("Solve this step by step: A factory produces widgets. The probability of a defect is 0.02. If we test 500 widgets, derive the probability of finding exactly 10 defective ones using the Poisson approximation.", "REASONING", "math-derivation", "en"),
    TestCase("Prove that every continuous function on a closed interval [a,b] is uniformly continuous. Use the epsilon-delta definition formally.", "REASONING", "formal-proof", "en"),
    TestCase(
        "In a game where two players alternately remove 1-3 stones from a pile of 15, prove that the first player has a winning strategy. Derive the complete strategy using backward induction.",
        "REASONING", "game-theory", "en",
    ),
    TestCase(
        "Prove that the greedy algorithm for the fractional knapsack problem produces an optimal solution. Use the exchange argument formally.",
        "REASONING", "algorithm-proof", "en",
    ),
    TestCase(
        "A farmer needs to cross a river with a wolf, a goat, and a cabbage. Only one can fit in the boat at a time. Prove that the minimum number of crossings is 7 and show the unique solution.",
        "REASONING", "logic-puzzle", "en",
    ),

    # Chinese
    TestCase("用数学归纳法证明：对所有正整数 n，1² + 2² + ... + n² = n(n+1)(2n+1)/6", "REASONING", "formal-proof", "zh"),
    TestCase("逐步推导贝叶斯定理，并用形式化符号证明其正确性", "REASONING", "math-derivation", "zh"),
    TestCase("证明：任意一个连通无向图，如果边数等于顶点数减一，则该图是树。请用数学归纳法逐步证明。", "REASONING", "formal-proof", "zh"),
    TestCase("用反证法证明：√2 是无理数。请写出完整的形式化证明过程。", "REASONING", "formal-proof", "zh"),

    # Russian
    TestCase("Докажи по индукции, что сумма первых n нечётных чисел равна n². Покажи каждый шаг формально.", "REASONING", "formal-proof", "ru"),
    TestCase("Выведи формулу Байеса шаг за шагом. Докажи её математически.", "REASONING", "math-derivation", "ru"),

    # Japanese
    TestCase("数学的帰納法を用いて、1+2+...+n = n(n+1)/2 を証明してください。各ステップを形式的に示してください。", "REASONING", "formal-proof", "ja"),

    # Korean
    TestCase("수학적 귀납법을 사용하여 1+2+...+n = n(n+1)/2를 증명하세요. 각 단계를 형식적으로 보여주세요.", "REASONING", "formal-proof", "ko"),

    # German
    TestCase("Beweise durch vollständige Induktion, dass die Summe der ersten n natürlichen Zahlen n(n+1)/2 beträgt. Zeige jeden Schritt formal.", "REASONING", "formal-proof", "de"),

    # ═══════════════════════════════════════
    #  Edge cases & special scenarios
    # ═══════════════════════════════════════

    # Agentic multi-step
    TestCase("I need you to read the file src/index.ts, then edit it to fix the TypeScript errors, and after that run the tests to make sure everything passes", "MEDIUM", "agentic-task", "en"),
    TestCase("Read the package.json, update the version to 2.0.0, install the new dependencies, then run the build and verify there are no errors", "MEDIUM", "agentic-task", "en"),
    TestCase("Check the git log, find the commit that broke the tests, and revert it", "MEDIUM", "agentic-task", "en"),

    # Noise / random
    TestCase("???", "SIMPLE", "edge-noise", "en"),
    TestCase("a]sDf!@ #$ random noise here", "SIMPLE", "edge-noise", "en"),
    TestCase("...", "SIMPLE", "edge-noise", "en"),
    TestCase("asdfghjkl", "SIMPLE", "edge-noise", "en"),

    # Code snippet + question (looks like code but is a simple QA)
    TestCase("```python\ndef foo(): return 42\n```\nWhat does this function return?", "SIMPLE", "code-snippet-qa", "en"),
    TestCase("What does `git rebase -i` do?", "SIMPLE", "factual-qa", "en"),

    # Long but simple
    TestCase("I was wondering if you could possibly tell me, in as simple terms as you can manage, what exactly the programming language Python is primarily used for in the software industry today?", "SIMPLE", "factual-qa", "en"),

    # Short but complex (tests our structural features)
    TestCase("Implement OAuth2 PKCE with refresh token rotation, token revocation, and device fingerprinting", "COMPLEX", "complex-code", "en"),

    # Mixed language
    TestCase("Explain什么是microserviceアーキテクチャ", "MEDIUM", "explanation", "mixed"),

    # With system prompt — should respect context
    TestCase("What is X?", "MEDIUM", "explanation", "en",
             system_prompt="You are a data scientist. Answer technical questions about machine learning with code examples."),
]

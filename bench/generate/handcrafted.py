"""Hand-crafted, hand-labeled dataset.

Every single prompt is written by hand with careful tier labeling.
No template generation — each case is a distinct, realistic prompt.

Labeling criteria:
  SIMPLE   — factual QA, definition, translation, greeting, yes/no, trivial lookup
  MEDIUM   — single-task code, explanation, summary, comparison, rewrite, extraction, classification
  COMPLEX  — multi-requirement system design, architecture, security audit, ML pipeline, migration, infra
  REASONING — formal proof, math derivation, logic puzzle, algorithm correctness, game theory
"""

from __future__ import annotations

import json
from pathlib import Path

C = dict  # shorthand for case dict


def _c(prompt: str, tier: str, cat: str, lang: str, sys_prompt: str | None = None) -> dict:
    d = {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}
    if sys_prompt:
        d["system_prompt"] = sys_prompt
    return d


# ═══════════════════════════════════════════════════════════
#  SIMPLE — factual QA, definition, translation, greeting
# ═══════════════════════════════════════════════════════════

SIMPLE: list[dict] = [
    # ── English factual QA ──
    _c("What is the capital of France?", "SIMPLE", "factual-qa", "en"),
    _c("What does HTTP stand for?", "SIMPLE", "factual-qa", "en"),
    _c("Who is the CEO of Apple?", "SIMPLE", "factual-qa", "en"),
    _c("What year did World War 2 end?", "SIMPLE", "factual-qa", "en"),
    _c("What is 2 + 2?", "SIMPLE", "factual-qa", "en"),
    _c("Is Python an interpreted language?", "SIMPLE", "factual-qa", "en"),
    _c("How many continents are there?", "SIMPLE", "factual-qa", "en"),
    _c("What is the boiling point of water?", "SIMPLE", "factual-qa", "en"),
    _c("What is DNS?", "SIMPLE", "factual-qa", "en"),
    _c("Who invented the telephone?", "SIMPLE", "factual-qa", "en"),
    _c("What color is the sky?", "SIMPLE", "factual-qa", "en"),
    _c("What is the largest planet?", "SIMPLE", "factual-qa", "en"),
    _c("How many bytes in a kilobyte?", "SIMPLE", "factual-qa", "en"),
    _c("What does CPU stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is an API?", "SIMPLE", "factual-qa", "en"),
    _c("What language is Django written in?", "SIMPLE", "factual-qa", "en"),
    _c("What is the speed of light?", "SIMPLE", "factual-qa", "en"),
    _c("Who created Git?", "SIMPLE", "factual-qa", "en"),
    _c("What is TCP/IP?", "SIMPLE", "factual-qa", "en"),
    _c("What is a compiler?", "SIMPLE", "factual-qa", "en"),
    _c("What does SQL stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between RAM and ROM?", "SIMPLE", "factual-qa", "en"),
    _c("What operating system does iPhone use?", "SIMPLE", "factual-qa", "en"),
    _c("What is open source software?", "SIMPLE", "factual-qa", "en"),
    _c("How many bits in a byte?", "SIMPLE", "factual-qa", "en"),
    # ── English definition ──
    _c("Define polymorphism", "SIMPLE", "definition", "en"),
    _c("What is a closure in JavaScript?", "SIMPLE", "definition", "en"),
    _c("What is recursion?", "SIMPLE", "definition", "en"),
    _c("What is an ORM?", "SIMPLE", "definition", "en"),
    _c("What is a hash table?", "SIMPLE", "definition", "en"),
    _c("What does REST stand for?", "SIMPLE", "definition", "en"),
    _c("What is a linked list?", "SIMPLE", "definition", "en"),
    _c("What is a design pattern?", "SIMPLE", "definition", "en"),
    _c("What is middleware?", "SIMPLE", "definition", "en"),
    _c("What is a microservice?", "SIMPLE", "definition", "en"),
    # ── English translation ──
    _c("Translate 'hello world' to Spanish", "SIMPLE", "translation", "en"),
    _c("How do you say 'thank you' in Japanese?", "SIMPLE", "translation", "en"),
    _c("Translate 'good morning' to French", "SIMPLE", "translation", "en"),
    _c("How do you say 'goodbye' in German?", "SIMPLE", "translation", "en"),
    _c("Translate 'I love programming' to Chinese", "SIMPLE", "translation", "en"),
    # ── English greeting / trivial ──
    _c("Hello", "SIMPLE", "greeting", "en"),
    _c("Hi", "SIMPLE", "greeting", "en"),
    _c("Help", "SIMPLE", "greeting", "en"),
    _c("Thanks!", "SIMPLE", "greeting", "en"),
    _c("OK", "SIMPLE", "greeting", "en"),
    _c("Yes", "SIMPLE", "greeting", "en"),
    _c("No", "SIMPLE", "greeting", "en"),
    # ── English edge / noise ──
    _c("???", "SIMPLE", "edge-noise", "en"),
    _c("...", "SIMPLE", "edge-noise", "en"),
    _c("asdfghjkl", "SIMPLE", "edge-noise", "en"),
    _c("a]sDf!@ #$ random noise", "SIMPLE", "edge-noise", "en"),
    _c("test", "SIMPLE", "edge-noise", "en"),
    # ── English long-but-simple ──
    _c(
        "I was just wondering if you could possibly tell me what the programming language Python is mainly used for?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    _c(
        "Could you please explain to me in very basic terms what an API is and what it stands for?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    _c(
        "I'm new to programming and I was curious about what exactly a variable is in programming languages?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    # ── Chinese ──
    _c("什么是 REST API？", "SIMPLE", "factual-qa", "zh"),
    _c("Python 是什么语言？", "SIMPLE", "factual-qa", "zh"),
    _c("谁是爱因斯坦？", "SIMPLE", "factual-qa", "zh"),
    _c("地球有多少颗卫星？", "SIMPLE", "factual-qa", "zh"),
    _c("TCP 和 UDP 有什么不同？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是数据库？", "SIMPLE", "factual-qa", "zh"),
    _c("Linux 是什么？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是云计算？", "SIMPLE", "factual-qa", "zh"),
    _c("翻译：Good morning", "SIMPLE", "translation", "zh"),
    _c("你好", "SIMPLE", "greeting", "zh"),
    _c("谢谢", "SIMPLE", "greeting", "zh"),
    # ── Russian ──
    _c("Что такое HTTP?", "SIMPLE", "factual-qa", "ru"),
    _c("Кто изобрёл телефон?", "SIMPLE", "factual-qa", "ru"),
    _c("Сколько планет в солнечной системе?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое база данных?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое облачные вычисления?", "SIMPLE", "factual-qa", "ru"),
    _c("Переведи 'hello' на русский", "SIMPLE", "translation", "ru"),
    _c("Привет", "SIMPLE", "greeting", "ru"),
    _c("Спасибо", "SIMPLE", "greeting", "ru"),
    # ── Spanish ──
    _c("¿Qué es una API?", "SIMPLE", "factual-qa", "es"),
    _c("¿Cuántos océanos hay?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un servidor?", "SIMPLE", "factual-qa", "es"),
    _c("Traduce 'thank you' al español", "SIMPLE", "translation", "es"),
    _c("Hola", "SIMPLE", "greeting", "es"),
    # ── German ──
    _c("Was ist eine Datenbank?", "SIMPLE", "factual-qa", "de"),
    _c("Was bedeutet HTTP?", "SIMPLE", "factual-qa", "de"),
    _c("Übersetze 'good morning' ins Deutsche", "SIMPLE", "translation", "de"),
    _c("Hallo", "SIMPLE", "greeting", "de"),
    # ── French ──
    _c("Qu'est-ce qu'une API ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce que le cloud computing ?", "SIMPLE", "factual-qa", "fr"),
    _c("Bonjour", "SIMPLE", "greeting", "fr"),
    # ── Japanese ──
    _c("HTMLとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("データベースとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("こんにちは", "SIMPLE", "greeting", "ja"),
    # ── Korean ──
    _c("HTTP란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("API가 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("안녕하세요", "SIMPLE", "greeting", "ko"),
    # ── Portuguese ──
    _c("O que é um banco de dados?", "SIMPLE", "factual-qa", "pt"),
    _c("Olá", "SIMPLE", "greeting", "pt"),
    # ── Arabic ──
    _c("ما هو البروتوكول HTTP؟", "SIMPLE", "factual-qa", "ar"),
    _c("مرحبا", "SIMPLE", "greeting", "ar"),
    # ── Code snippet QA (looks like code but is a simple question) ──
    _c("What does `git rebase -i` do?", "SIMPLE", "factual-qa", "en"),
    _c("What does the `ls -la` command show?", "SIMPLE", "factual-qa", "en"),
    _c("What is the `__init__` method in Python?", "SIMPLE", "factual-qa", "en"),
    _c("```python\ndef foo(): return 42\n```\nWhat does this function return?", "SIMPLE", "code-snippet-qa", "en"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM — single-task code, explanation, summary, comparison, rewrite, extraction
# ═══════════════════════════════════════════════════════════

MEDIUM: list[dict] = [
    # ── English simple code ──
    _c("Write a Python function that reverses a string", "MEDIUM", "simple-code", "en"),
    _c("Write a SQL query to find duplicate emails in a users table", "MEDIUM", "simple-code", "en"),
    _c("Create a simple Express.js route that returns JSON", "MEDIUM", "simple-code", "en"),
    _c("Write a bash script that counts lines in all .ts files", "MEDIUM", "simple-code", "en"),
    _c("Write a Python class for a linked list with insert and delete methods", "MEDIUM", "simple-code", "en"),
    _c("Write a regex to validate email addresses", "MEDIUM", "simple-code", "en"),
    _c("Give me a one-liner to flatten a nested array in JavaScript", "MEDIUM", "simple-code", "en"),
    _c("Write a function to check if a number is prime", "MEDIUM", "simple-code", "en"),
    _c("Create a TypeScript interface for a User object with name, email, and age", "MEDIUM", "simple-code", "en"),
    _c("Write a Python decorator that measures function execution time", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple LRU cache in Python", "MEDIUM", "simple-code", "en"),
    _c("Write a Go function that reads a file and counts words", "MEDIUM", "simple-code", "en"),
    _c("Create a React component that renders a todo list", "MEDIUM", "simple-code", "en"),
    _c("Write a CSS animation that makes an element fade in", "MEDIUM", "simple-code", "en"),
    _c("Implement binary search in Java", "MEDIUM", "simple-code", "en"),
    _c("Write a shell script to find all files larger than 100MB", "MEDIUM", "simple-code", "en"),
    _c("Create a Dockerfile for a Python Flask app", "MEDIUM", "simple-code", "en"),
    _c("Write a Python context manager for database connections", "MEDIUM", "simple-code", "en"),
    _c("Implement a stack using two queues in Python", "MEDIUM", "simple-code", "en"),
    _c("Write a function to convert Roman numerals to integers", "MEDIUM", "simple-code", "en"),
    # ── English explanation ──
    _c("Explain the difference between TCP and UDP", "MEDIUM", "explanation", "en"),
    _c("Explain how async/await works in JavaScript", "MEDIUM", "explanation", "en"),
    _c("Explain the CAP theorem in simple terms", "MEDIUM", "explanation", "en"),
    _c("How does garbage collection work in Java?", "MEDIUM", "explanation", "en"),
    _c("Explain how DNS resolution works", "MEDIUM", "explanation", "en"),
    _c("How does HTTPS work?", "MEDIUM", "explanation", "en"),
    _c("Explain the difference between processes and threads", "MEDIUM", "explanation", "en"),
    _c("How does a hash table handle collisions?", "MEDIUM", "explanation", "en"),
    _c("Explain what a closure is and give an example", "MEDIUM", "explanation", "en"),
    _c("How does virtual memory work?", "MEDIUM", "explanation", "en"),
    _c("Explain the event loop in Node.js", "MEDIUM", "explanation", "en"),
    _c("What is the difference between stack and heap memory?", "MEDIUM", "explanation", "en"),
    _c("Explain how JWT authentication works", "MEDIUM", "explanation", "en"),
    _c("How does consistent hashing work?", "MEDIUM", "explanation", "en"),
    _c("Explain the observer pattern with an example", "MEDIUM", "explanation", "en"),
    # ── English comparison ──
    _c("Compare the pros and cons of SQL vs NoSQL databases", "MEDIUM", "comparison", "en"),
    _c("What are the trade-offs between REST and GraphQL?", "MEDIUM", "comparison", "en"),
    _c("Compare Docker containers with virtual machines", "MEDIUM", "comparison", "en"),
    _c("Differences between Git merge and Git rebase", "MEDIUM", "comparison", "en"),
    _c("Compare React with Vue.js for building web apps", "MEDIUM", "comparison", "en"),
    _c("Redis vs Memcached — when to use which?", "MEDIUM", "comparison", "en"),
    _c("Compare serverless with containerized deployment", "MEDIUM", "comparison", "en"),
    _c("TypeScript vs JavaScript — pros and cons", "MEDIUM", "comparison", "en"),
    # ── English summary ──
    _c("Summarize the key features of React hooks", "MEDIUM", "summary", "en"),
    _c("Summarize this article in 3 bullet points", "MEDIUM", "summary", "en"),
    _c("Give me a brief overview of the SOLID principles", "MEDIUM", "summary", "en"),
    _c("Summarize the main differences between HTTP/1.1 and HTTP/2", "MEDIUM", "summary", "en"),
    # ── English creative ──
    _c("Write a poem about recursion in the style of Shakespeare", "MEDIUM", "creative", "en"),
    _c("Write a haiku about machine learning", "MEDIUM", "creative", "en"),
    _c("Write a short story about a bug in production", "MEDIUM", "creative", "en"),
    # ── English rewrite ──
    _c("Rewrite this paragraph to be more concise and professional", "MEDIUM", "rewrite", "en"),
    _c("Convert this Python 2 code to Python 3", "MEDIUM", "rewrite", "en"),
    _c("Simplify this technical explanation for a non-technical audience", "MEDIUM", "rewrite", "en"),
    _c("Rewrite this error message to be user-friendly", "MEDIUM", "rewrite", "en"),
    _c("Make this email more formal", "MEDIUM", "rewrite", "en"),
    # ── English extraction / classification ──
    _c("Extract all the dates and names from the following text", "MEDIUM", "extraction", "en"),
    _c("Pull out the key metrics from this report", "MEDIUM", "extraction", "en"),
    _c("List all the API endpoints mentioned in this spec", "MEDIUM", "extraction", "en"),
    _c("Classify these customer reviews as positive, negative, or neutral", "MEDIUM", "classification", "en"),
    _c("Categorize these support tickets by priority", "MEDIUM", "classification", "en"),
    # ── English structured output ──
    _c("Format this data as a JSON schema with nested objects", "MEDIUM", "structured-output", "en"),
    _c("Convert this CSV data into a markdown table", "MEDIUM", "structured-output", "en"),
    # ── English edge short ──
    _c("Fix the bug", "MEDIUM", "edge-short", "en"),
    _c("Write code", "MEDIUM", "edge-short", "en"),
    _c("Refactor this", "MEDIUM", "edge-short", "en"),
    _c("Debug this", "MEDIUM", "edge-short", "en"),
    # ── English agentic ──
    _c("Read the file src/index.ts, fix the TypeScript errors, then run the tests", "MEDIUM", "agentic-task", "en"),
    _c("Check the git log, find the commit that broke the tests, and revert it", "MEDIUM", "agentic-task", "en"),
    _c("Look at the error in the console, find the source, and fix it", "MEDIUM", "agentic-task", "en"),
    # ── English with system prompt ──
    _c(
        "What's the best way to handle errors here?",
        "MEDIUM",
        "explanation",
        "en",
        sys_prompt="You are a senior Python developer reviewing code.",
    ),
    _c(
        "How should I structure this component?",
        "MEDIUM",
        "explanation",
        "en",
        sys_prompt="You are a React expert helping with frontend architecture.",
    ),
    # ── Chinese ──
    _c("写一个 Python 函数来计算斐波那契数列", "MEDIUM", "simple-code", "zh"),
    _c("解释 Docker 和虚拟机的区别", "MEDIUM", "explanation", "zh"),
    _c("用 JavaScript 实现一个简单的防抖函数", "MEDIUM", "simple-code", "zh"),
    _c("总结一下 Git rebase 和 merge 的区别", "MEDIUM", "comparison", "zh"),
    _c("把这段文字改写成正式的商务邮件风格", "MEDIUM", "rewrite", "zh"),
    _c("从下面的文本中提取所有人名和地名", "MEDIUM", "extraction", "zh"),
    _c("写一个 Python 装饰器来记录函数执行时间", "MEDIUM", "simple-code", "zh"),
    _c("解释什么是 RESTful API，举例说明", "MEDIUM", "explanation", "zh"),
    # ── Russian ──
    _c("Напиши функцию на Python для сортировки списка", "MEDIUM", "simple-code", "ru"),
    _c("Объясни разницу между SQL и NoSQL", "MEDIUM", "explanation", "ru"),
    _c("Перепиши этот текст более кратко", "MEDIUM", "rewrite", "ru"),
    _c("Напиши функцию на Go для чтения файла", "MEDIUM", "simple-code", "ru"),
    # ── Japanese ──
    _c("Pythonでリストをソートする関数を書いてください", "MEDIUM", "simple-code", "ja"),
    _c("RESTとGraphQLの違いを説明してください", "MEDIUM", "explanation", "ja"),
    _c("このテキストを簡潔にまとめてください", "MEDIUM", "summary", "ja"),
    # ── Korean ──
    _c("Python으로 문자열을 뒤집는 함수를 작성해주세요", "MEDIUM", "simple-code", "ko"),
    _c("TCP와 UDP의 차이점을 설명해주세요", "MEDIUM", "explanation", "ko"),
    # ── German ──
    _c("Schreibe eine Python-Funktion, die eine Liste sortiert", "MEDIUM", "simple-code", "de"),
    _c("Erkläre den Unterschied zwischen REST und GraphQL", "MEDIUM", "explanation", "de"),
    # ── French ──
    _c("Écris une fonction Python qui inverse une chaîne", "MEDIUM", "simple-code", "fr"),
    _c("Explique la différence entre TCP et UDP", "MEDIUM", "explanation", "fr"),
    # ── Portuguese ──
    _c("Escreva uma função Python que inverta uma string", "MEDIUM", "simple-code", "pt"),
    # ── Spanish ──
    _c("Escribe una función en Python que ordene una lista", "MEDIUM", "simple-code", "es"),
    _c("Explica la diferencia entre SQL y NoSQL", "MEDIUM", "explanation", "es"),
    # ── Arabic ──
    _c("اكتب دالة Python لعكس سلسلة نصية", "MEDIUM", "simple-code", "ar"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX — multi-requirement design, architecture, security, ML, migration
# ═══════════════════════════════════════════════════════════

COMPLEX: list[dict] = [
    # ── English system design ──
    _c(
        "Design a distributed rate limiter that works across multiple microservice instances using Redis. Include the algorithm, data structures, and handle edge cases like clock skew.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a URL shortener service that handles 10M daily requests, with analytics, custom aliases, and expiration support.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a notification system supporting push, email, SMS, and in-app channels with priority queues, rate limiting, and user preferences.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a real-time chat system with message persistence, read receipts, typing indicators, file sharing, and group conversations.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a file storage service like Dropbox with versioning, sharing, deduplication, and conflict resolution for offline edits.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── English complex code ──
    _c(
        "Implement a full CRUD REST API with authentication, input validation, error handling, and database migrations using FastAPI and SQLAlchemy",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Write a comprehensive test suite for a payment processing module covering happy paths, edge cases, race conditions, and failure recovery",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a real-time collaborative text editor with operational transformation, conflict resolution, and offline support",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design and implement a custom database query optimizer that handles JOIN reordering, index selection, and cost-based plan selection",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Implement a B+ tree from scratch in Rust with concurrent access, page splitting, and range queries",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a web crawler that respects robots.txt, handles rate limiting, deduplicates URLs, and supports distributed crawling",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Implement a full OAuth2 PKCE flow with refresh token rotation, token revocation, and device fingerprinting",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a task queue system with priority scheduling, dead letter handling, retry with backoff, and distributed locking",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── English architecture ──
    _c(
        "Refactor this monolithic application into microservices. Identify service boundaries, define API contracts, and design inter-service communication.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    _c(
        "Architect a real-time event processing pipeline using Kafka with exactly-once semantics, dead letter queues, schema evolution, and multi-region failover",
        "COMPLEX",
        "architecture",
        "en",
    ),
    _c(
        "Design a multi-tenant SaaS platform with data isolation, billing integration, RBAC, and elastic scaling",
        "COMPLEX",
        "architecture",
        "en",
    ),
    # ── English security ──
    _c(
        "Analyze the security vulnerabilities in this authentication flow and propose fixes for CSRF, XSS, SQL injection, and session fixation",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    _c(
        "Perform a security audit of this API: check for broken authentication, IDOR, rate limiting gaps, and data exposure risks",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    # ── English infrastructure ──
    _c(
        "Create a Kubernetes deployment with auto-scaling, health checks, rolling updates, and a service mesh for a multi-tenant SaaS app",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    _c(
        "Set up a complete CI/CD pipeline with build, test, lint, security scan, staging deploy, canary release, and rollback automation",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    # ── English ML pipeline ──
    _c(
        "Design an end-to-end ML pipeline for fraud detection including feature engineering, model training, A/B testing, monitoring, and automated retraining on drift",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    _c(
        "Build a real-time recommendation system with collaborative filtering, content-based fallback, A/B testing, and cold start handling",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    # ── English migration ──
    _c(
        "Plan a zero-downtime migration from PostgreSQL to CockroachDB for 500M rows with schema changes, validation, and rollback strategy",
        "COMPLEX",
        "migration",
        "en",
    ),
    _c(
        "Migrate a monolithic Django app to a FastAPI microservices architecture with service discovery, shared auth, and data migration",
        "COMPLEX",
        "migration",
        "en",
    ),
    # ── English performance ──
    _c(
        "Optimize this React app: implement code splitting, virtualized lists, memoization, image lazy loading, and service worker caching",
        "COMPLEX",
        "performance",
        "en",
    ),
    # ── English short-but-complex ──
    _c(
        "Implement distributed consensus with Raft including leader election, log replication, and membership changes",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a type checker for a subset of TypeScript supporting generics, union types, and structural typing",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Chinese ──
    _c(
        "设计一个支持百万级并发的分布式消息队列系统，包括消息持久化、消费者组、死信队列和监控告警",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "实现一个完整的用户认证系统，包括 JWT、OAuth2、RBAC 权限控制、密码加密和审计日志",
        "COMPLEX",
        "complex-code",
        "zh",
    ),
    _c(
        "设计一个支持多租户的 SaaS 平台架构，包括数据隔离、计费系统、权限管理和弹性伸缩方案",
        "COMPLEX",
        "architecture",
        "zh",
    ),
    _c("设计一个实时推荐系统，包括特征工程、模型训练、在线推理、A/B 测试和效果监控", "COMPLEX", "ml-pipeline", "zh"),
    _c("实现一个分布式任务调度系统，支持定时任务、依赖编排、失败重试和动态扩缩容", "COMPLEX", "complex-code", "zh"),
    # ── Russian ──
    _c(
        "Спроектируй распределённую систему кэширования с инвалидацией, репликацией и шардированием данных",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Реализуй полноценный REST API с аутентификацией, валидацией, обработкой ошибок и миграциями базы данных",
        "COMPLEX",
        "complex-code",
        "ru",
    ),
    # ── Japanese ──
    _c(
        "認証、レート制限、サーキットブレーカー、分散トレーシングを含むAPIゲートウェイを設計してください",
        "COMPLEX",
        "architecture",
        "ja",
    ),
    # ── Korean ──
    _c(
        "분산 캐싱 시스템을 설계하세요. 캐시 무효화, 복제, 샤딩, 장애 복구를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    # ── German ──
    _c(
        "Entwerfe eine skalierbare Microservice-Architektur mit Service Discovery, Load Balancing, Circuit Breaking und verteiltem Tracing.",
        "COMPLEX",
        "architecture",
        "de",
    ),
    # ── With system prompt ──
    _c(
        "The current latency is 2 seconds per request. Bring it under 200ms.",
        "COMPLEX",
        "performance",
        "en",
        sys_prompt="You are a performance engineer. The app is FastAPI + PostgreSQL + Redis + Elasticsearch.",
    ),
]


# ═══════════════════════════════════════════════════════════
#  REASONING — formal proof, math derivation, logic, game theory
# ═══════════════════════════════════════════════════════════

REASONING: list[dict] = [
    # ── English formal proof ──
    _c(
        "Prove that the halting problem is undecidable using a diagonalization argument. Show each step formally.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove by mathematical induction that the sum of the first n natural numbers equals n(n+1)/2",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that the square root of 2 is irrational using proof by contradiction", "REASONING", "formal-proof", "en"),
    _c("Prove that there are infinitely many prime numbers using Euclid's proof", "REASONING", "formal-proof", "en"),
    _c(
        "Prove that every continuous function on [a,b] is uniformly continuous. Use epsilon-delta.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that every finite group of prime order is cyclic. Show each step.", "REASONING", "formal-proof", "en"),
    # ── English math derivation ──
    _c(
        "Derive the time complexity of the Fibonacci function using the Master Theorem. Prove step by step.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Solve step by step: derive the probability of exactly 10 defects in 500 widgets with P(defect)=0.02 using Poisson",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive Bayes' theorem from the definition of conditional probability. Show all steps.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c("Derive the closed-form solution for the recurrence T(n) = 2T(n/2) + n", "REASONING", "math-derivation", "en"),
    # ── English formal logic ──
    _c(
        "Using formal logic, prove that if all men are mortal and Socrates is a man, then Socrates is mortal. Use first-order predicate logic.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    _c(
        "Prove de Morgan's laws using truth tables and then using formal logical derivation",
        "REASONING",
        "formal-logic",
        "en",
    ),
    # ── English algorithm proof ──
    _c(
        "Prove the correctness of Dijkstra's algorithm using loop invariants. Show initialization, maintenance, and termination.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the greedy algorithm for fractional knapsack is optimal using the exchange argument",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that merge sort has O(n log n) time complexity in all cases using the recursion tree method",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    # ── English game theory / logic puzzle ──
    _c(
        "In a game where players alternately remove 1-3 stones from 15, prove the first player has a winning strategy via backward induction",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Prove that in the Monty Hall problem, switching gives 2/3 probability. Use formal probability theory.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "A farmer must cross a river with a wolf, goat, and cabbage. Prove the minimum crossings is 7 and show the unique solution.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    # ── Chinese ──
    _c("用数学归纳法证明：对所有正整数 n，1² + 2² + ... + n² = n(n+1)(2n+1)/6", "REASONING", "formal-proof", "zh"),
    _c("逐步推导贝叶斯定理，并用形式化符号证明其正确性", "REASONING", "math-derivation", "zh"),
    _c("证明任意连通无向图，若边数等于顶点数减一，则该图是树。用数学归纳法。", "REASONING", "formal-proof", "zh"),
    _c("用反证法证明 √2 是无理数。写出完整形式化证明。", "REASONING", "formal-proof", "zh"),
    # ── Russian ──
    _c(
        "Докажи по индукции, что сумма первых n нечётных чисел равна n². Покажи каждый шаг формально.",
        "REASONING",
        "formal-proof",
        "ru",
    ),
    _c("Выведи формулу Байеса шаг за шагом. Докажи математически.", "REASONING", "math-derivation", "ru"),
    # ── Japanese ──
    _c(
        "数学的帰納法を用いて 1+2+...+n = n(n+1)/2 を証明してください。各ステップを形式的に。",
        "REASONING",
        "formal-proof",
        "ja",
    ),
    # ── Korean ──
    _c("수학적 귀납법으로 1+2+...+n = n(n+1)/2를 증명하세요. 각 단계를 형식적으로.", "REASONING", "formal-proof", "ko"),
    # ── German ──
    _c(
        "Beweise durch vollständige Induktion, dass die Summe der ersten n natürlichen Zahlen n(n+1)/2 beträgt.",
        "REASONING",
        "formal-proof",
        "de",
    ),
    # ── Spanish ──
    _c(
        "Demuestra por inducción matemática que la suma de los primeros n números naturales es n(n+1)/2.",
        "REASONING",
        "formal-proof",
        "es",
    ),
    # ── French ──
    _c(
        "Démontre par récurrence que la somme des n premiers entiers naturels vaut n(n+1)/2.",
        "REASONING",
        "formal-proof",
        "fr",
    ),
]


# ═══════════════════════════════════════════════════════════
#  Export
# ═══════════════════════════════════════════════════════════

ALL_CASES = SIMPLE + MEDIUM + COMPLEX + REASONING


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8") as f:
        for case in ALL_CASES:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")

    from collections import Counter

    tiers = Counter(c["expected_tier"] for c in ALL_CASES)
    langs = Counter(c["lang"] for c in ALL_CASES)
    cats = Counter(c["category"] for c in ALL_CASES)
    print(f"Exported {len(ALL_CASES)} hand-crafted cases to {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")
    print(f"  Categories: {len(cats)}")


if __name__ == "__main__":
    import sys

    export(sys.argv[1] if len(sys.argv) > 1 else None)

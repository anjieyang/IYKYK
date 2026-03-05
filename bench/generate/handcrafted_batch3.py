"""Hand-crafted batch 3 — stress-testing generalization.

Focus areas:
- Domains NOT in batch 1-2: legal, medical, finance, education, DevOps, data science
- Harder boundary cases: medium-length explanations, short complex tasks
- More non-English coverage: double Japanese/Korean/Arabic/Portuguese
- Adversarial: prompts that LOOK like one tier but ARE another
"""

from __future__ import annotations

import json
from pathlib import Path


def _c(prompt: str, tier: str, cat: str, lang: str, sys_prompt: str | None = None) -> dict:
    d = {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}
    if sys_prompt:
        d["system_prompt"] = sys_prompt
    return d


SIMPLE_B3: list[dict] = [
    # ── New domains: legal, medical, finance ──
    _c("What is a patent?", "SIMPLE", "factual-qa", "en"),
    _c("What is GDP?", "SIMPLE", "factual-qa", "en"),
    _c("What does FDA stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is inflation?", "SIMPLE", "factual-qa", "en"),
    _c("What is a stock market?", "SIMPLE", "factual-qa", "en"),
    _c("What is DNA?", "SIMPLE", "factual-qa", "en"),
    _c("What is an antibiotic?", "SIMPLE", "factual-qa", "en"),
    _c("What is HIPAA?", "SIMPLE", "factual-qa", "en"),
    _c("What is a copyright?", "SIMPLE", "factual-qa", "en"),
    _c("What is a firewall?", "SIMPLE", "factual-qa", "en"),
    _c("What is bandwidth?", "SIMPLE", "factual-qa", "en"),
    _c("What is latency?", "SIMPLE", "factual-qa", "en"),
    _c("What is a VPN?", "SIMPLE", "factual-qa", "en"),
    _c("What is two-factor authentication?", "SIMPLE", "factual-qa", "en"),
    _c("What is a kernel?", "SIMPLE", "factual-qa", "en"),

    # ── Adversarial: long but SIMPLE ──
    _c("I've been trying to understand what exactly a database index is, and I was hoping you could give me a brief and simple explanation of what it does and why it's useful?", "SIMPLE", "factual-qa", "en"),
    _c("My professor mentioned something called 'Big O notation' in class today and I have no idea what it means. Can you tell me what it is in plain English?", "SIMPLE", "factual-qa", "en"),
    _c("I keep hearing people at work talk about 'the cloud' and I feel embarrassed to ask what it actually means. What is cloud computing in the simplest possible terms?", "SIMPLE", "factual-qa", "en"),

    # ── More Chinese SIMPLE ──
    _c("什么是 VPN？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是防火墙？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是带宽？", "SIMPLE", "factual-qa", "zh"),
    _c("GDP 是什么意思？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 DNA？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是人工智能？", "SIMPLE", "factual-qa", "zh"),
    _c("翻译：see you later", "SIMPLE", "translation", "zh"),
    _c("翻译：how much does it cost", "SIMPLE", "translation", "zh"),

    # ── More Japanese SIMPLE ──
    _c("VPNとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("ファイアウォールとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("人工知能とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("クラウドコンピューティングとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("ブロックチェーンとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("'ありがとう'を英語で何と言いますか？", "SIMPLE", "translation", "ja"),

    # ── More Korean SIMPLE ──
    _c("VPN이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("방화벽이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("인공지능이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("블록체인이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("클라우드 컴퓨팅이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),

    # ── More Arabic SIMPLE ──
    _c("ما هو الذكاء الاصطناعي؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو VPN؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هي سلسلة الكتل؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو الحوسبة السحابية؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو الجدار الناري؟", "SIMPLE", "factual-qa", "ar"),

    # ── More Portuguese SIMPLE ──
    _c("O que é inteligência artificial?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um firewall?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é VPN?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é blockchain?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é computação em nuvem?", "SIMPLE", "factual-qa", "pt"),

    # ── More Russian SIMPLE ──
    _c("Что такое искусственный интеллект?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое блокчейн?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое VPN?", "SIMPLE", "factual-qa", "ru"),

    # ── More Spanish SIMPLE ──
    _c("¿Qué es la inteligencia artificial?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un firewall?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es blockchain?", "SIMPLE", "factual-qa", "es"),

    # ── More German SIMPLE ──
    _c("Was ist künstliche Intelligenz?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist eine Blockchain?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein VPN?", "SIMPLE", "factual-qa", "de"),

    # ── More French SIMPLE ──
    _c("Qu'est-ce que l'intelligence artificielle ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un pare-feu ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce que la blockchain ?", "SIMPLE", "factual-qa", "fr"),
]


MEDIUM_B3: list[dict] = [
    # ── New domains: data science, DevOps, finance ──
    _c("Write a Python script to load a CSV file with pandas and calculate basic statistics", "MEDIUM", "simple-code", "en"),
    _c("Create a simple data visualization with matplotlib showing sales trends", "MEDIUM", "simple-code", "en"),
    _c("Write a Terraform configuration for an S3 bucket with versioning enabled", "MEDIUM", "simple-code", "en"),
    _c("Create a Prometheus alert rule for high CPU usage", "MEDIUM", "simple-code", "en"),
    _c("Write a SQL query to calculate the moving average of daily revenue over 7 days", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple retry decorator with configurable max retries and delay", "MEDIUM", "simple-code", "en"),

    # ── Explanation: new topics ──
    _c("Explain how blockchain consensus mechanisms work", "MEDIUM", "explanation", "en"),
    _c("How does a neural network learn through backpropagation?", "MEDIUM", "explanation", "en"),
    _c("Explain the difference between symmetric and asymmetric encryption", "MEDIUM", "explanation", "en"),
    _c("How does a container differ from a virtual machine at the OS level?", "MEDIUM", "explanation", "en"),
    _c("Explain what eventual consistency means in distributed systems", "MEDIUM", "explanation", "en"),
    _c("How does a B-tree index improve database query performance?", "MEDIUM", "explanation", "en"),
    _c("Explain the difference between supervised and unsupervised learning", "MEDIUM", "explanation", "en"),
    _c("How does a reverse proxy work?", "MEDIUM", "explanation", "en"),
    _c("Explain what a message broker does and when to use one", "MEDIUM", "explanation", "en"),
    _c("How does garbage collection work in Go compared to Java?", "MEDIUM", "explanation", "en"),

    # ── Adversarial: looks COMPLEX but is MEDIUM (single focused task) ──
    _c("Write a function to implement the Levenshtein distance algorithm", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple bloom filter in Python", "MEDIUM", "simple-code", "en"),
    _c("Write a topological sort algorithm for a directed acyclic graph", "MEDIUM", "simple-code", "en"),
    _c("Create a simple event emitter class in TypeScript", "MEDIUM", "simple-code", "en"),

    # ── More comparisons ──
    _c("Compare eventual consistency and strong consistency in databases", "MEDIUM", "comparison", "en"),
    _c("What are the trade-offs between microservices and a modular monolith?", "MEDIUM", "comparison", "en"),
    _c("Compare GraphQL subscriptions with WebSockets for real-time data", "MEDIUM", "comparison", "en"),

    # ── Classification / extraction ──
    _c("Categorize these error logs by type: timeout, auth failure, or server error", "MEDIUM", "classification", "en"),
    _c("Extract all URLs from this HTML document", "MEDIUM", "extraction", "en"),
    _c("Identify the programming language of each code snippet below", "MEDIUM", "classification", "en"),

    # ── More Chinese MEDIUM ──
    _c("写一个 Python 脚本读取 CSV 文件并计算基本统计量", "MEDIUM", "simple-code", "zh"),
    _c("解释区块链的共识机制是怎么工作的", "MEDIUM", "explanation", "zh"),
    _c("解释对称加密和非对称加密的区别", "MEDIUM", "explanation", "zh"),
    _c("解释什么是最终一致性", "MEDIUM", "explanation", "zh"),
    _c("比较容器和虚拟机在操作系统层面的区别", "MEDIUM", "comparison", "zh"),
    _c("比较 GraphQL 和 REST 的优缺点", "MEDIUM", "comparison", "zh"),
    _c("写一个 Python 的重试装饰器", "MEDIUM", "simple-code", "zh"),

    # ── More Japanese MEDIUM ──
    _c("Pythonでリトライデコレータを実装してください", "MEDIUM", "simple-code", "ja"),
    _c("対称暗号と非対称暗号の違いを説明してください", "MEDIUM", "explanation", "ja"),
    _c("ブロックチェーンのコンセンサスメカニズムを説明してください", "MEDIUM", "explanation", "ja"),
    _c("コンテナと仮想マシンの違いを比較してください", "MEDIUM", "comparison", "ja"),

    # ── More Korean MEDIUM ──
    _c("Python으로 리트라이 데코레이터를 구현해주세요", "MEDIUM", "simple-code", "ko"),
    _c("대칭 암호화와 비대칭 암호화의 차이를 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("블록체인 합의 메커니즘을 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("컨테이너와 가상 머신의 차이를 비교해주세요", "MEDIUM", "comparison", "ko"),

    # ── More Arabic MEDIUM ──
    _c("اكتب دالة Python لحساب متوسط قائمة من الأرقام", "MEDIUM", "simple-code", "ar"),
    _c("اشرح الفرق بين التشفير المتماثل وغير المتماثل", "MEDIUM", "explanation", "ar"),

    # ── More Portuguese MEDIUM ──
    _c("Escreva um script Python para ler um CSV e calcular estatísticas", "MEDIUM", "simple-code", "pt"),
    _c("Explique a diferença entre criptografia simétrica e assimétrica", "MEDIUM", "explanation", "pt"),
    _c("Compare microsserviços com um monólito modular", "MEDIUM", "comparison", "pt"),

    # ── More Russian MEDIUM ──
    _c("Напиши декоратор для повторных попыток на Python", "MEDIUM", "simple-code", "ru"),
    _c("Объясни разницу между симметричным и асимметричным шифрованием", "MEDIUM", "explanation", "ru"),
    _c("Сравни контейнеры и виртуальные машины на уровне ОС", "MEDIUM", "comparison", "ru"),

    # ── More Spanish MEDIUM ──
    _c("Escribe un script Python para leer un CSV y calcular estadísticas", "MEDIUM", "simple-code", "es"),
    _c("Explica la diferencia entre cifrado simétrico y asimétrico", "MEDIUM", "explanation", "es"),

    # ── More German MEDIUM ──
    _c("Schreibe ein Python-Skript zum Lesen einer CSV-Datei", "MEDIUM", "simple-code", "de"),
    _c("Erkläre den Unterschied zwischen symmetrischer und asymmetrischer Verschlüsselung", "MEDIUM", "explanation", "de"),

    # ── More French MEDIUM ──
    _c("Écris un script Python pour lire un CSV et calculer des statistiques", "MEDIUM", "simple-code", "fr"),
    _c("Explique la différence entre chiffrement symétrique et asymétrique", "MEDIUM", "explanation", "fr"),
]


COMPLEX_B3: list[dict] = [
    # ── New domains ──
    _c("Design an automated trading system with market data ingestion, strategy backtesting, risk management, order execution, and real-time P&L tracking.", "COMPLEX", "system-design", "en"),
    _c("Build a HIPAA-compliant electronic health records system with patient data encryption, role-based access, audit trails, and interoperability via FHIR API.", "COMPLEX", "system-design", "en"),
    _c("Design a legal document analysis platform with OCR, named entity extraction, clause classification, risk scoring, and version comparison.", "COMPLEX", "system-design", "en"),

    # ── Data engineering ──
    _c("Build an ETL pipeline that ingests data from 5 sources, handles schema drift, performs data quality validation, deduplication, and loads into a data warehouse with SCD Type 2.", "COMPLEX", "architecture", "en"),
    _c("Design a real-time fraud detection system with feature store, model serving, online/offline feature consistency, and feedback loop for model retraining.", "COMPLEX", "ml-pipeline", "en"),

    # ── Adversarial: short but COMPLEX (many requirements implied) ──
    _c("Implement a distributed lock manager with fencing tokens, deadlock detection, and automatic lease renewal", "COMPLEX", "complex-code", "en"),
    _c("Build a CDC pipeline from PostgreSQL to Elasticsearch with exactly-once delivery and schema evolution", "COMPLEX", "complex-code", "en"),
    _c("Implement a custom garbage collector for a toy language runtime with mark-sweep, generational collection, and compaction", "COMPLEX", "complex-code", "en"),

    # ── More Chinese COMPLEX ──
    _c("设计一个自动化交易系统，包括行情数据接入、策略回测、风险控制、订单执行和实时盈亏追踪", "COMPLEX", "system-design", "zh"),
    _c("构建一个合规的电子病历系统，包括数据加密、角色权限、审计日志和 FHIR API 互操作", "COMPLEX", "system-design", "zh"),
    _c("设计一个实时反欺诈系统，包括特征存储、模型服务、在线/离线特征一致性和模型自动重训练", "COMPLEX", "ml-pipeline", "zh"),

    # ── More Japanese COMPLEX ──
    _c("自動取引システムを設計してください。市場データ取込、バックテスト、リスク管理、注文執行、リアルタイム損益追跡を含めてください。", "COMPLEX", "system-design", "ja"),
    _c("分散ロックマネージャを実装してください。フェンシングトークン、デッドロック検出、自動リース更新を含めてください。", "COMPLEX", "complex-code", "ja"),

    # ── More Korean COMPLEX ──
    _c("자동 거래 시스템을 설계하세요. 시장 데이터 수집, 백테스트, 리스크 관리, 주문 실행, 실시간 손익 추적을 포함해야 합니다.", "COMPLEX", "system-design", "ko"),
    _c("실시간 사기 탐지 시스템을 설계하세요. 피처 스토어, 모델 서빙, 온라인/오프라인 피처 일관성을 포함해야 합니다.", "COMPLEX", "ml-pipeline", "ko"),

    # ── More Arabic COMPLEX ──
    _c("صمم نظام تداول آلي يشمل استيعاب بيانات السوق، اختبار الاستراتيجيات، إدارة المخاطر، تنفيذ الأوامر، وتتبع الأرباح والخسائر.", "COMPLEX", "system-design", "ar"),

    # ── More Portuguese COMPLEX ──
    _c("Projete um sistema de negociação automatizado com ingestão de dados de mercado, backtesting, gestão de riscos, execução de ordens e rastreamento de P&L.", "COMPLEX", "system-design", "pt"),

    # ── More Russian COMPLEX ──
    _c("Спроектируй систему автоматической торговли с приёмом рыночных данных, бэктестингом стратегий, управлением рисками и исполнением ордеров.", "COMPLEX", "system-design", "ru"),
    _c("Построй ETL-пайплайн для 5 источников с обработкой дрейфа схемы, валидацией данных и дедупликацией.", "COMPLEX", "architecture", "ru"),

    # ── More Spanish COMPLEX ──
    _c("Diseña un sistema de trading automatizado con ingesta de datos de mercado, backtesting, gestión de riesgos y ejecución de órdenes.", "COMPLEX", "system-design", "es"),

    # ── More German COMPLEX ──
    _c("Entwerfe ein automatisiertes Handelssystem mit Marktdatenaufnahme, Backtesting, Risikomanagement und Auftragsausführung.", "COMPLEX", "system-design", "de"),

    # ── More French COMPLEX ──
    _c("Conçois un système de trading automatisé avec ingestion de données de marché, backtesting, gestion des risques et exécution des ordres.", "COMPLEX", "system-design", "fr"),
]


REASONING_B3: list[dict] = [
    # ── New topics ──
    _c("Prove that the set of real numbers is uncountable using Cantor's diagonal argument. Show every step.", "REASONING", "formal-proof", "en"),
    _c("Prove that if a function is differentiable at a point, it is continuous at that point. Use epsilon-delta.", "REASONING", "formal-proof", "en"),
    _c("Derive the formula for the number of derangements of n elements. Prove it using inclusion-exclusion.", "REASONING", "math-derivation", "en"),
    _c("Prove that the eigenvalues of a real symmetric matrix are always real. Show each step formally.", "REASONING", "formal-proof", "en"),
    _c("Prove the master theorem for divide-and-conquer recurrences. Show all three cases with proofs.", "REASONING", "math-derivation", "en"),
    _c("Prove that P is closed under union, concatenation, and Kleene star. Use Turing machine constructions.", "REASONING", "formal-proof", "en"),
    _c("In the prisoner's dilemma repeated infinitely, prove that tit-for-tat is a Nash equilibrium under discounting.", "REASONING", "game-theory", "en"),

    # ── Adversarial: LOOKS like MEDIUM but IS REASONING ──
    _c("Why is quicksort O(n²) in the worst case? Prove it formally with a recurrence relation.", "REASONING", "math-derivation", "en"),
    _c("Explain why you can't sort faster than O(n log n) with comparisons. Prove the lower bound.", "REASONING", "algorithm-proof", "en"),

    # ── More Chinese REASONING ──
    _c("证明实数集是不可数的，使用 Cantor 对角线论证。逐步展示。", "REASONING", "formal-proof", "zh"),
    _c("推导错位排列的公式，用容斥原理证明。", "REASONING", "math-derivation", "zh"),
    _c("证明实对称矩阵的特征值都是实数。展示每一步。", "REASONING", "formal-proof", "zh"),

    # ── More Japanese REASONING ──
    _c("実数の集合が非可算であることをカントールの対角線論法を用いて証明してください。", "REASONING", "formal-proof", "ja"),
    _c("マスター定理を導出し、3つのケースすべてを証明してください。", "REASONING", "math-derivation", "ja"),

    # ── More Korean REASONING ──
    _c("실수 집합이 비가산임을 칸토어의 대각선 논법으로 증명하세요.", "REASONING", "formal-proof", "ko"),
    _c("마스터 정리를 유도하고 세 가지 경우를 모두 증명하세요.", "REASONING", "math-derivation", "ko"),

    # ── More Arabic REASONING ──
    _c("أثبت أن مجموعة الأعداد الحقيقية غير قابلة للعد باستخدام حجة كانتور القطرية. أظهر كل خطوة.", "REASONING", "formal-proof", "ar"),

    # ── More Portuguese REASONING ──
    _c("Prove que o conjunto dos números reais é incontável usando o argumento diagonal de Cantor.", "REASONING", "formal-proof", "pt"),

    # ── More Russian REASONING ──
    _c("Докажи, что множество действительных чисел несчётно, используя диагональный аргумент Кантора.", "REASONING", "formal-proof", "ru"),
    _c("Выведи формулу для количества беспорядков из n элементов, используя формулу включения-исключения.", "REASONING", "math-derivation", "ru"),

    # ── More Spanish REASONING ──
    _c("Demuestra que el conjunto de los números reales es incontable usando el argumento diagonal de Cantor.", "REASONING", "formal-proof", "es"),

    # ── More German REASONING ──
    _c("Beweise, dass die Menge der reellen Zahlen überabzählbar ist, mit Cantors Diagonalargument.", "REASONING", "formal-proof", "de"),

    # ── More French REASONING ──
    _c("Démontre que l'ensemble des nombres réels est indénombrable en utilisant l'argument diagonal de Cantor.", "REASONING", "formal-proof", "fr"),
]


ALL_B3 = SIMPLE_B3 + MEDIUM_B3 + COMPLEX_B3 + REASONING_B3


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b3.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B3:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter
    tiers = Counter(c["expected_tier"] for c in ALL_B3)
    langs = Counter(c["lang"] for c in ALL_B3)
    print(f"Batch 3: {len(ALL_B3)} cases → {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")


if __name__ == "__main__":
    import sys
    export(sys.argv[1] if len(sys.argv) > 1 else None)

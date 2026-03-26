"""Hand-crafted batch 5 — adversarial, new domains, hard cases.

Designed to stress-test generalization:
- IoT, quantum, bioinformatics, game dev, edge computing
- Adversarial: tier ambiguity traps
- More non-English COMPLEX and REASONING
- System prompt context switching
- Mixed language prompts
"""

from __future__ import annotations

import json
from pathlib import Path


def _c(prompt: str, tier: str, cat: str, lang: str, sys_prompt: str | None = None) -> dict:
    d = {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}
    if sys_prompt:
        d["system_prompt"] = sys_prompt
    return d


SIMPLE_B5: list[dict] = [
    # ── New domain factual QA ──
    _c("What is edge computing?", "SIMPLE", "factual-qa", "en"),
    _c("What is a quantum bit?", "SIMPLE", "factual-qa", "en"),
    _c("What is MQTT?", "SIMPLE", "factual-qa", "en"),
    _c("What is a game engine?", "SIMPLE", "factual-qa", "en"),
    _c("What is bioinformatics?", "SIMPLE", "factual-qa", "en"),
    _c("What is a digital twin?", "SIMPLE", "factual-qa", "en"),
    _c("What is WebRTC?", "SIMPLE", "factual-qa", "en"),
    _c("What is a smart contract?", "SIMPLE", "factual-qa", "en"),
    _c("What is federated learning?", "SIMPLE", "factual-qa", "en"),
    _c("What is a zero-knowledge proof?", "SIMPLE", "factual-qa", "en"),
    _c("What is reinforcement learning?", "SIMPLE", "factual-qa", "en"),
    _c("What is a transformer model?", "SIMPLE", "factual-qa", "en"),
    # ── Adversarial: LOOKS complex (technical words) but IS SIMPLE ──
    _c("What is Kubernetes?", "SIMPLE", "factual-qa", "en"),
    _c("What is a distributed database?", "SIMPLE", "factual-qa", "en"),
    _c("What is a consensus algorithm?", "SIMPLE", "factual-qa", "en"),
    _c("What is eventual consistency?", "SIMPLE", "factual-qa", "en"),
    _c("What is a load balancer?", "SIMPLE", "factual-qa", "en"),
    _c("What is infrastructure as code?", "SIMPLE", "factual-qa", "en"),
    # ── Multilingual new domain ──
    _c("什么是边缘计算？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是量子比特？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是联邦学习？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是智能合约？", "SIMPLE", "factual-qa", "zh"),
    _c("エッジコンピューティングとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("量子ビットとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("스마트 계약이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("연합 학습이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("ما هو الحوسبة الطرفية؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو العقد الذكي؟", "SIMPLE", "factual-qa", "ar"),
    _c("O que é computação de borda?", "SIMPLE", "factual-qa", "pt"),
    _c("¿Qué es la computación en el borde?", "SIMPLE", "factual-qa", "es"),
    _c("Was ist Edge Computing?", "SIMPLE", "factual-qa", "de"),
    _c("Qu'est-ce que l'edge computing ?", "SIMPLE", "factual-qa", "fr"),
    _c("Что такое граничные вычисления?", "SIMPLE", "factual-qa", "ru"),
    # ── With system prompt: complex context but simple question ──
    _c(
        "What is the current status?",
        "SIMPLE",
        "factual-qa",
        "en",
        sys_prompt="You are monitoring a Kubernetes cluster with 50 microservices.",
    ),
    _c(
        "Is the build passing?",
        "SIMPLE",
        "factual-qa",
        "en",
        sys_prompt="You are a CI/CD engineer managing a complex deployment pipeline.",
    ),
]


MEDIUM_B5: list[dict] = [
    # ── New domain explanations ──
    _c("Explain how edge computing reduces latency compared to cloud computing", "MEDIUM", "explanation", "en"),
    _c("How does federated learning protect user privacy?", "MEDIUM", "explanation", "en"),
    _c("Explain how a game physics engine handles collision detection", "MEDIUM", "explanation", "en"),
    _c("How does WebRTC establish a peer-to-peer connection?", "MEDIUM", "explanation", "en"),
    _c("Explain how zero-knowledge proofs work at a high level", "MEDIUM", "explanation", "en"),
    _c("How does a transformer model process text differently from an RNN?", "MEDIUM", "explanation", "en"),
    _c("Explain how MQTT differs from HTTP for IoT devices", "MEDIUM", "explanation", "en"),
    _c("How does reinforcement learning differ from supervised learning?", "MEDIUM", "explanation", "en"),
    # ── Adversarial: LOOKS simple (short) but IS MEDIUM ──
    _c("Explain consistent hashing with a diagram", "MEDIUM", "explanation", "en"),
    _c("Describe the Raft consensus protocol", "MEDIUM", "explanation", "en"),
    _c("Walk me through a TCP three-way handshake", "MEDIUM", "explanation", "en"),
    _c("Explain backpropagation intuitively", "MEDIUM", "explanation", "en"),
    # ── New domain code ──
    _c("Write a Python script to read sensor data from an MQTT broker", "MEDIUM", "simple-code", "en"),
    _c("Create a simple game loop in Python with pygame", "MEDIUM", "simple-code", "en"),
    _c("Write a Solidity smart contract for a simple token", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple A* pathfinding algorithm in Python", "MEDIUM", "simple-code", "en"),
    _c("Write a WebSocket server in Go that broadcasts messages", "MEDIUM", "simple-code", "en"),
    # ── More non-English MEDIUM ──
    _c("解释联邦学习如何保护用户隐私", "MEDIUM", "explanation", "zh"),
    _c("解释边缘计算相比云计算如何降低延迟", "MEDIUM", "explanation", "zh"),
    _c("写一个 Python 脚本从 MQTT broker 读取传感器数据", "MEDIUM", "simple-code", "zh"),
    _c("比较强化学习和监督学习的区别", "MEDIUM", "comparison", "zh"),
    _c("フェデレーテッドラーニングがどのようにプライバシーを保護するか説明してください", "MEDIUM", "explanation", "ja"),
    _c("WebRTCがどのようにP2P接続を確立するか説明してください", "MEDIUM", "explanation", "ja"),
    _c("연합 학습이 사용자 프라이버시를 어떻게 보호하는지 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("엣지 컴퓨팅이 클라우드 컴퓨팅에 비해 지연을 어떻게 줄이는지 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("اشرح كيف يحمي التعلم الموحد خصوصية المستخدم", "MEDIUM", "explanation", "ar"),
    _c("Explique como o aprendizado federado protege a privacidade", "MEDIUM", "explanation", "pt"),
    _c("Объясни как федеративное обучение защищает приватность", "MEDIUM", "explanation", "ru"),
    _c("Erkläre wie Edge Computing die Latenz reduziert", "MEDIUM", "explanation", "de"),
    _c("Explique comment le edge computing réduit la latence", "MEDIUM", "explanation", "fr"),
    _c("Explica cómo la computación en el borde reduce la latencia", "MEDIUM", "explanation", "es"),
    # ── With system prompt making a simple question MEDIUM ──
    _c(
        "What is X?",
        "MEDIUM",
        "explanation",
        "en",
        sys_prompt="You are a machine learning engineer. Provide detailed technical explanations with code examples.",
    ),
    _c(
        "Can you help?",
        "MEDIUM",
        "explanation",
        "en",
        sys_prompt="You are debugging a complex distributed system. Analyze logs and suggest fixes.",
    ),
    # ── Mixed language ──
    _c("Explain什么是microserviceアーキテクチャ", "MEDIUM", "explanation", "mixed"),
]


COMPLEX_B5: list[dict] = [
    # ── New domains ──
    _c(
        "Design an IoT fleet management platform with device provisioning, OTA firmware updates, telemetry ingestion, anomaly detection, and remote configuration.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a multiplayer game server with authoritative physics, client-side prediction, lag compensation, matchmaking, and anti-cheat.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a bioinformatics pipeline for whole-genome sequencing: read alignment, variant calling, annotation, quality control, and clinical reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a smart contract system for decentralized exchange with order matching, liquidity pools, slippage protection, and MEV prevention.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design an edge AI inference platform with model optimization, hardware-aware deployment, A/B testing, and federated model updates.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    # ── Adversarial: LOOKS medium (single sentence) but IS COMPLEX ──
    _c(
        "Implement a Raft consensus library with leader election, log replication, snapshotting, and dynamic membership changes",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a WebRTC SFU with room management, bandwidth estimation, simulcast, and recording",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── More non-English COMPLEX ──
    _c(
        "设计一个物联网设备管理平台，包括设备注册、固件升级、遥测数据采集、异常检测和远程配置",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "构建一个去中心化交易所的智能合约系统，包括订单匹配、流动性池、滑点保护和 MEV 防护",
        "COMPLEX",
        "complex-code",
        "zh",
    ),
    _c(
        "IoTフリート管理プラットフォームを設計してください。デバイスプロビジョニング、OTAアップデート、テレメトリ、異常検知を含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "IoT 디바이스 관리 플랫폼을 설계하세요. 디바이스 프로비저닝, OTA 업데이트, 텔레메트리 수집, 이상 탐지를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "صمم منصة إدارة أجهزة إنترنت الأشياء تشمل تسجيل الأجهزة وتحديث البرامج عن بعد وجمع البيانات واكتشاف الشذوذ.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "Спроектируй платформу для управления IoT-устройствами с провизионированием, OTA-обновлениями, сбором телеметрии и обнаружением аномалий.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Projete uma plataforma de gerenciamento IoT com provisionamento, atualizações OTA, coleta de telemetria e detecção de anomalias.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "Diseña una plataforma de gestión IoT con aprovisionamiento de dispositivos, actualizaciones OTA, recopilación de telemetría y detección de anomalías.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Entwerfe eine IoT-Geräteverwaltungsplattform mit Provisionierung, OTA-Updates, Telemetrieerfassung und Anomalieerkennung.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Conçois une plateforme de gestion IoT avec provisionnement, mises à jour OTA, collecte de télémétrie et détection d'anomalies.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
]


REASONING_B5: list[dict] = [
    # ── New topics ──
    _c(
        "Prove that the problem of determining whether a context-free grammar is ambiguous is undecidable. Use reduction from the Post correspondence problem.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Derive the information-theoretic lower bound for lossless data compression (Shannon's source coding theorem). Prove step by step.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Prove that the stable matching produced by the Gale-Shapley algorithm is optimal for the proposing side. Use contradiction.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "In a repeated prisoner's dilemma with discount factor δ, derive the minimum δ for which cooperation is sustainable in a subgame-perfect equilibrium.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Prove that the knapsack problem is NP-complete by reduction from subset sum. Show both directions.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    # ── Adversarial: LOOKS like explanation but IS REASONING ──
    _c(
        "Why can't we solve the traveling salesman problem efficiently? Prove that TSP is NP-hard.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Explain why P ≠ NP is believed to be true. Give a formal argument using diagonalization.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    # ── Non-English REASONING ──
    _c("证明上下文无关文法的歧义性是不可判定的。使用 Post 对应问题的归约。", "REASONING", "formal-proof", "zh"),
    _c("推导 Shannon 信源编码定理的信息论下界。逐步证明。", "REASONING", "math-derivation", "zh"),
    _c(
        "Gale-Shapleyアルゴリズムが提案側にとって最適であることを証明してください。背理法を用いてください。",
        "REASONING",
        "algorithm-proof",
        "ja",
    ),
    _c(
        "게일-셰플리 알고리즘이 제안측에 최적임을 증명하세요. 귀류법을 사용하세요.",
        "REASONING",
        "algorithm-proof",
        "ko",
    ),
    _c("أثبت أن مسألة الحقيبة NP-complete عن طريق التخفيض من مسألة مجموع الجزئي.", "REASONING", "formal-proof", "ar"),
    _c(
        "Докажи, что задача о рюкзаке является NP-полной путём сведения от задачи о сумме подмножеств.",
        "REASONING",
        "formal-proof",
        "ru",
    ),
    _c(
        "Prove que o problema da mochila é NP-completo por redução do problema da soma de subconjuntos.",
        "REASONING",
        "formal-proof",
        "pt",
    ),
    _c(
        "Demuestra que el problema de la mochila es NP-completo mediante reducción desde el problema de la suma de subconjuntos.",
        "REASONING",
        "formal-proof",
        "es",
    ),
    _c(
        "Beweise, dass das Rucksackproblem NP-vollständig ist durch Reduktion vom Teilsummenproblem.",
        "REASONING",
        "formal-proof",
        "de",
    ),
    _c(
        "Démontre que le problème du sac à dos est NP-complet par réduction du problème de la somme de sous-ensembles.",
        "REASONING",
        "formal-proof",
        "fr",
    ),
]


ALL_B5 = SIMPLE_B5 + MEDIUM_B5 + COMPLEX_B5 + REASONING_B5


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b5.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B5:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter

    tiers = Counter(c["expected_tier"] for c in ALL_B5)
    langs = Counter(c["lang"] for c in ALL_B5)
    cats = Counter(c["category"] for c in ALL_B5)
    print(f"Batch 5: {len(ALL_B5)} cases → {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")
    print(f"  Categories: {len(cats)}")


if __name__ == "__main__":
    import sys

    export(sys.argv[1] if len(sys.argv) > 1 else None)

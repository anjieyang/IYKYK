"""Hand-crafted batch 4 — targeting SIMPLE↔MEDIUM boundary.

Focus: more explanation/comparison (MEDIUM) and factual-qa (SIMPLE) to
improve the boundary decision. Also adds new domains and languages.
"""

from __future__ import annotations

import json
from pathlib import Path


def _c(prompt: str, tier: str, cat: str, lang: str) -> dict:
    return {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}


SIMPLE_B4: list[dict] = [
    # ── Short factual that SHOULD stay SIMPLE despite tricky words ──
    _c("What is machine learning?", "SIMPLE", "factual-qa", "en"),
    _c("What is a neural network?", "SIMPLE", "factual-qa", "en"),
    _c("What is Kubernetes?", "SIMPLE", "factual-qa", "en"),
    _c("What is Docker?", "SIMPLE", "factual-qa", "en"),
    _c("What is a microservice?", "SIMPLE", "factual-qa", "en"),
    _c("What is encryption?", "SIMPLE", "factual-qa", "en"),
    _c("What is an algorithm?", "SIMPLE", "factual-qa", "en"),
    _c("What is a graph database?", "SIMPLE", "factual-qa", "en"),
    _c("What is CI/CD?", "SIMPLE", "factual-qa", "en"),
    _c("What is a container registry?", "SIMPLE", "factual-qa", "en"),
    _c("What is WebAssembly?", "SIMPLE", "factual-qa", "en"),
    _c("What is gRPC?", "SIMPLE", "factual-qa", "en"),
    _c("What is a service mesh?", "SIMPLE", "factual-qa", "en"),
    _c("What is event sourcing?", "SIMPLE", "factual-qa", "en"),
    _c("What is CQRS?", "SIMPLE", "factual-qa", "en"),

    # ── More multilingual SIMPLE ──
    _c("机器学习是什么？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是微服务？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是加密？", "SIMPLE", "factual-qa", "zh"),
    _c("機械学習とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("暗号化とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("マイクロサービスとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("머신러닝이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("암호화란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("마이크로서비스란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("ما هو التعلم الآلي؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو التشفير؟", "SIMPLE", "factual-qa", "ar"),
    _c("O que é aprendizado de máquina?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é criptografia?", "SIMPLE", "factual-qa", "pt"),
    _c("¿Qué es el aprendizaje automático?", "SIMPLE", "factual-qa", "es"),
    _c("Was ist maschinelles Lernen?", "SIMPLE", "factual-qa", "de"),
    _c("Qu'est-ce que l'apprentissage automatique ?", "SIMPLE", "factual-qa", "fr"),
    _c("Что такое машинное обучение?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое микросервис?", "SIMPLE", "factual-qa", "ru"),
]


MEDIUM_B4: list[dict] = [
    # ── More explanation (the weakest category) ──
    _c("Explain how a message queue works and when to use one", "MEDIUM", "explanation", "en"),
    _c("How does rate limiting work in API design?", "MEDIUM", "explanation", "en"),
    _c("Explain the concept of eventual consistency with a practical example", "MEDIUM", "explanation", "en"),
    _c("How does a circuit breaker pattern work in microservices?", "MEDIUM", "explanation", "en"),
    _c("Explain what a dead letter queue is and when you need one", "MEDIUM", "explanation", "en"),
    _c("How does database sharding work?", "MEDIUM", "explanation", "en"),
    _c("Explain the difference between horizontal and vertical scaling", "MEDIUM", "explanation", "en"),
    _c("How does an API gateway work?", "MEDIUM", "explanation", "en"),
    _c("Explain what a feature flag is and how it helps with deployments", "MEDIUM", "explanation", "en"),
    _c("How does blue-green deployment work?", "MEDIUM", "explanation", "en"),
    _c("Explain the difference between optimistic and pessimistic locking", "MEDIUM", "explanation", "en"),
    _c("How does a bloom filter work and when would you use one?", "MEDIUM", "explanation", "en"),
    _c("Explain what idempotency means in API design", "MEDIUM", "explanation", "en"),
    _c("How does OAuth2 work at a high level?", "MEDIUM", "explanation", "en"),
    _c("Explain the publish-subscribe pattern with an example", "MEDIUM", "explanation", "en"),

    # ── More comparison ──
    _c("Compare message queues and event streams", "MEDIUM", "comparison", "en"),
    _c("What are the differences between gRPC and REST?", "MEDIUM", "comparison", "en"),
    _c("Compare blue-green deployment with canary releases", "MEDIUM", "comparison", "en"),
    _c("Differences between optimistic and pessimistic concurrency control", "MEDIUM", "comparison", "en"),
    _c("Compare Redis and PostgreSQL for caching", "MEDIUM", "comparison", "en"),
    _c("Event sourcing vs traditional CRUD — trade-offs?", "MEDIUM", "comparison", "en"),
    _c("Compare Terraform with Pulumi for infrastructure as code", "MEDIUM", "comparison", "en"),

    # ── Chinese MEDIUM explanation ──
    _c("解释消息队列是怎么工作的", "MEDIUM", "explanation", "zh"),
    _c("解释什么是断路器模式", "MEDIUM", "explanation", "zh"),
    _c("数据库分片是怎么工作的？", "MEDIUM", "explanation", "zh"),
    _c("解释什么是幂等性", "MEDIUM", "explanation", "zh"),
    _c("解释发布-订阅模式", "MEDIUM", "explanation", "zh"),
    _c("比较水平扩展和垂直扩展", "MEDIUM", "comparison", "zh"),
    _c("比较消息队列和事件流", "MEDIUM", "comparison", "zh"),

    # ── Japanese MEDIUM ──
    _c("メッセージキューの仕組みを説明してください", "MEDIUM", "explanation", "ja"),
    _c("サーキットブレーカーパターンを説明してください", "MEDIUM", "explanation", "ja"),
    _c("水平スケーリングと垂直スケーリングの違いを比較してください", "MEDIUM", "comparison", "ja"),

    # ── Korean MEDIUM ──
    _c("메시지 큐가 어떻게 작동하는지 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("서킷 브레이커 패턴을 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("수평 확장과 수직 확장의 차이를 비교해주세요", "MEDIUM", "comparison", "ko"),

    # ── Arabic MEDIUM ──
    _c("اشرح كيف تعمل قوائم الرسائل", "MEDIUM", "explanation", "ar"),
    _c("اشرح الفرق بين التوسع الأفقي والعمودي", "MEDIUM", "explanation", "ar"),

    # ── Russian MEDIUM ──
    _c("Объясни как работает очередь сообщений", "MEDIUM", "explanation", "ru"),
    _c("Объясни что такое паттерн Circuit Breaker", "MEDIUM", "explanation", "ru"),
    _c("Сравни горизонтальное и вертикальное масштабирование", "MEDIUM", "comparison", "ru"),

    # ── Portuguese MEDIUM ──
    _c("Explique como funciona uma fila de mensagens", "MEDIUM", "explanation", "pt"),
    _c("Compare escalabilidade horizontal e vertical", "MEDIUM", "comparison", "pt"),

    # ── Spanish MEDIUM ──
    _c("Explica cómo funciona una cola de mensajes", "MEDIUM", "explanation", "es"),
    _c("Compara el despliegue blue-green con los canary releases", "MEDIUM", "comparison", "es"),

    # ── German MEDIUM ──
    _c("Erkläre wie eine Nachrichtenwarteschlange funktioniert", "MEDIUM", "explanation", "de"),
    _c("Vergleiche horizontale und vertikale Skalierung", "MEDIUM", "comparison", "de"),

    # ── French MEDIUM ──
    _c("Explique comment fonctionne une file de messages", "MEDIUM", "explanation", "fr"),
    _c("Compare le déploiement blue-green avec les canary releases", "MEDIUM", "comparison", "fr"),
]


COMPLEX_B4: list[dict] = [
    # ── More system-design that SHOULD be COMPLEX ──
    _c("Design a real-time bidding system for online advertising with bid optimization, frequency capping, budget pacing, and click fraud detection.", "COMPLEX", "system-design", "en"),
    _c("Build a multi-player game server with matchmaking, state synchronization, lag compensation, and anti-cheat detection.", "COMPLEX", "system-design", "en"),
    _c("Design an observability platform with metrics collection, distributed tracing, log aggregation, alerting, and anomaly detection.", "COMPLEX", "system-design", "en"),
    _c("Build a document collaboration system with real-time editing, commenting, version history, access control, and offline sync.", "COMPLEX", "complex-code", "en"),

    # ── Multilingual COMPLEX ──
    _c("设计一个在线广告实时竞价系统，包括出价优化、频次控制、预算分配和点击欺诈检测", "COMPLEX", "system-design", "zh"),
    _c("マルチプレイヤーゲームサーバーを構築してください。マッチメイキング、状態同期、ラグ補償を含めてください。", "COMPLEX", "system-design", "ja"),
    _c("멀티플레이어 게임 서버를 설계하세요. 매치메이킹, 상태 동기화, 지연 보상, 안티치트를 포함해야 합니다.", "COMPLEX", "system-design", "ko"),
    _c("صمم نظام مزايدة في الوقت الفعلي للإعلانات يشمل تحسين العروض وتحديد التكرار واكتشاف الاحتيال.", "COMPLEX", "system-design", "ar"),
]


REASONING_B4: list[dict] = [
    # ── More variety ──
    _c("Prove that the language of palindromes is not context-free. Use the pumping lemma for context-free languages.", "REASONING", "formal-proof", "en"),
    _c("Derive the amortized time complexity of dynamic array resizing. Show it's O(1) using the accounting method.", "REASONING", "math-derivation", "en"),
    _c("Prove that any comparison-based algorithm to find the maximum of n elements requires at least n-1 comparisons.", "REASONING", "algorithm-proof", "en"),

    _c("证明回文语言不是上下文无关语言，使用上下文无关语言的泵引理。", "REASONING", "formal-proof", "zh"),
    _c("回文言語が文脈自由言語でないことをポンプの補題を用いて証明してください。", "REASONING", "formal-proof", "ja"),
    _c("회문 언어가 문맥 자유 언어가 아님을 펌핑 보조정리를 사용하여 증명하세요.", "REASONING", "formal-proof", "ko"),
]


ALL_B4 = SIMPLE_B4 + MEDIUM_B4 + COMPLEX_B4 + REASONING_B4


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b4.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B4:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter
    tiers = Counter(c["expected_tier"] for c in ALL_B4)
    langs = Counter(c["lang"] for c in ALL_B4)
    print(f"Batch 4: {len(ALL_B4)} cases → {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")


if __name__ == "__main__":
    import sys
    export(sys.argv[1] if len(sys.argv) > 1 else None)

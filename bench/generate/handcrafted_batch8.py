"""Hand-crafted batch 8 — 500 fresh cases.

Strategy for this batch:
- New domains: gaming, cooking recipes, music theory, astronomy, linguistics, law,
  medicine, agriculture, fashion, architecture (buildings), sports analytics, supply chain
- All prompts UNIQUE and distinct from previous batches
- Adversarial: long-but-SIMPLE, short-but-COMPLEX, misleading keywords
- 14+ languages, English ~40%
- Target: ~140 SIMPLE, ~180 MEDIUM, ~100 COMPLEX, ~80 REASONING
"""

from __future__ import annotations

import json
from pathlib import Path


def _c(prompt: str, tier: str, cat: str, lang: str) -> dict:
    return {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}


# ═══════════════════════════════════════════════════════════
#  SIMPLE (~140)
# ═══════════════════════════════════════════════════════════

SIMPLE_B8: list[dict] = [
    # ── Gaming domain ──
    _c("What is an FPS in video games?", "SIMPLE", "factual-qa", "en"),
    _c("How many players in a standard basketball game?", "SIMPLE", "factual-qa", "en"),
    _c("What does NPC stand for in gaming?", "SIMPLE", "factual-qa", "en"),
    _c("What is a respawn point?", "SIMPLE", "factual-qa", "en"),
    _c("What is the ELO rating system?", "SIMPLE", "factual-qa", "en"),
    _c("What is a hitbox in game development?", "SIMPLE", "factual-qa", "en"),
    _c("What does RNG mean in gaming?", "SIMPLE", "factual-qa", "en"),
    _c("What is a save point?", "SIMPLE", "factual-qa", "en"),
    # ── Cooking recipes domain ──
    _c("What temperature to boil water at sea level?", "SIMPLE", "factual-qa", "en"),
    _c("How many teaspoons in a tablespoon?", "SIMPLE", "factual-qa", "en"),
    _c("What is a roux?", "SIMPLE", "factual-qa", "en"),
    _c("What does al dente mean?", "SIMPLE", "factual-qa", "en"),
    _c("What is the smoke point of olive oil?", "SIMPLE", "factual-qa", "en"),
    _c("What is a mirepoix?", "SIMPLE", "factual-qa", "en"),
    _c("How many ounces in a cup?", "SIMPLE", "factual-qa", "en"),
    _c("What is proofing in baking?", "SIMPLE", "factual-qa", "en"),
    # ── Music theory domain ──
    _c("What is a major scale?", "SIMPLE", "factual-qa", "en"),
    _c("How many beats in a 4/4 measure?", "SIMPLE", "factual-qa", "en"),
    _c("What is a chord progression?", "SIMPLE", "factual-qa", "en"),
    _c("What does forte mean in music?", "SIMPLE", "factual-qa", "en"),
    _c("What is a half step?", "SIMPLE", "factual-qa", "en"),
    _c("What is the relative minor of C major?", "SIMPLE", "factual-qa", "en"),
    _c("What is a cadence?", "SIMPLE", "factual-qa", "en"),
    _c("What does staccato mean?", "SIMPLE", "factual-qa", "en"),
    # ── Astronomy domain ──
    _c("What is a light-year?", "SIMPLE", "factual-qa", "en"),
    _c("How many planets are in our solar system?", "SIMPLE", "factual-qa", "en"),
    _c("What is a nebula?", "SIMPLE", "factual-qa", "en"),
    _c("What is the asteroid belt?", "SIMPLE", "factual-qa", "en"),
    _c("What is a supernova?", "SIMPLE", "factual-qa", "en"),
    _c("What is the Kuiper belt?", "SIMPLE", "factual-qa", "en"),
    _c("What is a red dwarf?", "SIMPLE", "factual-qa", "en"),
    _c("What is the Oort cloud?", "SIMPLE", "factual-qa", "en"),
    # ── Linguistics domain ──
    _c("What is a phoneme?", "SIMPLE", "factual-qa", "en"),
    _c("What is a morpheme?", "SIMPLE", "factual-qa", "en"),
    _c("What is syntax?", "SIMPLE", "factual-qa", "en"),
    _c("What is a digraph?", "SIMPLE", "factual-qa", "en"),
    _c("What is an allophone?", "SIMPLE", "factual-qa", "en"),
    _c("What is a cognate?", "SIMPLE", "factual-qa", "en"),
    _c("What is a loanword?", "SIMPLE", "factual-qa", "en"),
    _c("What is pragmatics?", "SIMPLE", "factual-qa", "en"),
    # ── Law domain ──
    _c("What is tort law?", "SIMPLE", "factual-qa", "en"),
    _c("What is habeas corpus?", "SIMPLE", "factual-qa", "en"),
    _c("What is intellectual property?", "SIMPLE", "factual-qa", "en"),
    _c("What is a subpoena?", "SIMPLE", "factual-qa", "en"),
    _c("What is due diligence?", "SIMPLE", "factual-qa", "en"),
    _c("What is a class action lawsuit?", "SIMPLE", "factual-qa", "en"),
    _c("What is arbitration?", "SIMPLE", "factual-qa", "en"),
    _c("What is a patent?", "SIMPLE", "factual-qa", "en"),
    # ── Medicine domain ──
    _c("What is hypertension?", "SIMPLE", "factual-qa", "en"),
    _c("What is the normal body temperature in Celsius?", "SIMPLE", "factual-qa", "en"),
    _c("What is an antibiotic?", "SIMPLE", "factual-qa", "en"),
    _c("What is a placebo?", "SIMPLE", "factual-qa", "en"),
    _c("What is a vaccine?", "SIMPLE", "factual-qa", "en"),
    _c("What is a stent?", "SIMPLE", "factual-qa", "en"),
    _c("What is anesthesia?", "SIMPLE", "factual-qa", "en"),
    _c("What is a biopsy?", "SIMPLE", "factual-qa", "en"),
    # ── Agriculture domain ──
    _c("What is crop rotation?", "SIMPLE", "factual-qa", "en"),
    _c("What is irrigation?", "SIMPLE", "factual-qa", "en"),
    _c("What is a hybrid seed?", "SIMPLE", "factual-qa", "en"),
    _c("What is hydroponics?", "SIMPLE", "factual-qa", "en"),
    _c("What is a cover crop?", "SIMPLE", "factual-qa", "en"),
    _c("What is soil pH?", "SIMPLE", "factual-qa", "en"),
    _c("What is GMO?", "SIMPLE", "factual-qa", "en"),
    _c("What is precision agriculture?", "SIMPLE", "factual-qa", "en"),
    # ── Fashion domain ──
    _c("What is a bias cut?", "SIMPLE", "factual-qa", "en"),
    _c("What is a seam allowance?", "SIMPLE", "factual-qa", "en"),
    _c("What is a dart in sewing?", "SIMPLE", "factual-qa", "en"),
    _c("What is a selvage?", "SIMPLE", "factual-qa", "en"),
    _c("What is haute couture?", "SIMPLE", "factual-qa", "en"),
    _c("What is a muslin in fashion?", "SIMPLE", "factual-qa", "en"),
    _c("What is a toile?", "SIMPLE", "factual-qa", "en"),
    _c("What is a grain line?", "SIMPLE", "factual-qa", "en"),
    # ── Architecture (buildings) domain ──
    _c("What is a load-bearing wall?", "SIMPLE", "factual-qa", "en"),
    _c("What is a cantilever?", "SIMPLE", "factual-qa", "en"),
    _c("What is a buttress?", "SIMPLE", "factual-qa", "en"),
    _c("What is a clerestory window?", "SIMPLE", "factual-qa", "en"),
    _c("What is a vault in architecture?", "SIMPLE", "factual-qa", "en"),
    _c("What is a lintel?", "SIMPLE", "factual-qa", "en"),
    # ── Sports analytics domain ──
    _c("What is WAR in baseball?", "SIMPLE", "factual-qa", "en"),
    _c("What is xG in soccer?", "SIMPLE", "factual-qa", "en"),
    _c("What is PER in basketball?", "SIMPLE", "factual-qa", "en"),
    _c("What is a triple-double?", "SIMPLE", "factual-qa", "en"),
    _c("What is a slugging percentage?", "SIMPLE", "factual-qa", "en"),
    _c("What is QBR in football?", "SIMPLE", "factual-qa", "en"),
    # ── Supply chain domain ──
    _c("What is a bill of lading?", "SIMPLE", "factual-qa", "en"),
    _c("What is lead time?", "SIMPLE", "factual-qa", "en"),
    _c("What is a SKU?", "SIMPLE", "factual-qa", "en"),
    _c("What is just-in-time inventory?", "SIMPLE", "factual-qa", "en"),
    _c("What is a supply chain?", "SIMPLE", "factual-qa", "en"),
    _c("What is EOQ?", "SIMPLE", "factual-qa", "en"),
    # ── Definitions ──
    _c("Define polymorphism in programming", "SIMPLE", "definition", "en"),
    _c("What is a hash collision?", "SIMPLE", "definition", "en"),
    _c("What is tail recursion?", "SIMPLE", "definition", "en"),
    _c("What is a closure?", "SIMPLE", "definition", "en"),
    _c("What is lazy evaluation?", "SIMPLE", "definition", "en"),
    # ── Translations ──
    _c("Translate 'supply chain' to Spanish", "SIMPLE", "translation", "en"),
    _c("How do you say 'recipe' in French?", "SIMPLE", "translation", "en"),
    _c("Translate 'algorithm' to Russian", "SIMPLE", "translation", "en"),
    _c("How do you say 'database' in Japanese?", "SIMPLE", "translation", "en"),
    # ── Greetings ──
    _c("Hello, how are you?", "SIMPLE", "greeting", "en"),
    _c("Good morning", "SIMPLE", "greeting", "en"),
    # ── Adversarial: long-but-SIMPLE ──
    _c(
        "I'm writing a paper on supply chain management and I need to know the basic definition. Could you tell me what a supply chain is in one or two sentences?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    _c(
        "My doctor mentioned something called hypertension during my checkup. I forgot to ask what it means. Can you give me a brief definition?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    _c(
        "I've been playing video games for years but I still don't know what people mean when they say RNG. What does RNG stand for?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    _c(
        "I'm learning to cook and the recipe says 'al dente'. I have no idea what that means. Can you explain in one sentence?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    _c(
        "Someone at work mentioned EOQ in a meeting about inventory. I nodded along but have no clue. What is EOQ?",
        "SIMPLE",
        "factual-qa",
        "en",
    ),
    # ── Adversarial: misleading keywords (technical but SIMPLE) ──
    _c("What is a distributed system?", "SIMPLE", "factual-qa", "en"),
    _c("What is a neural network architecture?", "SIMPLE", "factual-qa", "en"),
    _c("What is a microservices architecture?", "SIMPLE", "factual-qa", "en"),
    # ── Chinese (new domains) ──
    _c("什么是光年？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是音素？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是知识产权？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是供应链？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 RNG？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是大调音阶？", "SIMPLE", "factual-qa", "zh"),
    # ── Japanese (new domains) ──
    _c("光年とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("音素とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("知的財産とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("RNGとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    # ── Korean (new domains) ──
    _c("광년이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("음소란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("지적 재산권이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("RNG란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    # ── Arabic (new domains) ──
    _c("ما هي السنة الضوئية؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو الصوت اللغوي؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هي الملكية الفكرية؟", "SIMPLE", "factual-qa", "ar"),
    # ── Russian (new domains) ──
    _c("Что такое световой год?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое фонема?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое интеллектуальная собственность?", "SIMPLE", "factual-qa", "ru"),
    # ── Spanish (new domains) ──
    _c("¿Qué es un año luz?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un fonema?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es la propiedad intelectual?", "SIMPLE", "factual-qa", "es"),
    # ── German (new domains) ──
    _c("Was ist ein Lichtjahr?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein Phonem?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist geistiges Eigentum?", "SIMPLE", "factual-qa", "de"),
    # ── French (new domains) ──
    _c("Qu'est-ce qu'une année-lumière ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un phonème ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce que la propriété intellectuelle ?", "SIMPLE", "factual-qa", "fr"),
    # ── Portuguese (new domains) ──
    _c("O que é um ano-luz?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um fonema?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é propriedade intelectual?", "SIMPLE", "factual-qa", "pt"),
    # ── Hindi (new domains) ──
    _c("प्रकाश वर्ष क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("ध्वन्यात्मक इकाई क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("बौद्धिक संपदा क्या है?", "SIMPLE", "factual-qa", "hi"),
    # ── Turkish (new domains) ──
    _c("Işık yılı nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Fonem nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Fikri mülkiyet nedir?", "SIMPLE", "factual-qa", "tr"),
    # ── Vietnamese (new domains) ──
    _c("Năm ánh sáng là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Âm vị là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Sở hữu trí tuệ là gì?", "SIMPLE", "factual-qa", "vi"),
    # ── Polish (new domains) ──
    _c("Co to jest rok świetlny?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest fonem?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest własność intelektualna?", "SIMPLE", "factual-qa", "pl"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM (~180)
# ═══════════════════════════════════════════════════════════

MEDIUM_B8: list[dict] = [
    # ── Gaming: code, explanation, debugging ──
    _c(
        "Write a Python script to parse a game save file in JSON format and extract player stats",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c(
        "Implement a simple matchmaking algorithm that pairs players by ELO rating within a tolerance",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Explain how hitbox detection works in 2D platformer games", "MEDIUM", "explanation", "en"),
    _c(
        "My game's physics feels floaty. How do I tune gravity and jump velocity for better feel?",
        "MEDIUM",
        "debugging",
        "en",
    ),
    _c("Compare deterministic vs random loot systems in game design", "MEDIUM", "comparison", "en"),
    _c("Review this game state serialization code for save/load bugs", "MEDIUM", "code-review", "en"),
    # ── Cooking: explanation, extraction, code ──
    _c(
        "Write a Python script to scale a recipe from 4 servings to 12, handling fractional measurements",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Explain the Maillard reaction and why it matters for browning", "MEDIUM", "explanation", "en"),
    _c("Extract all ingredients and their quantities from this recipe text", "MEDIUM", "extraction", "en"),
    _c("Compare braising vs stewing: when to use each technique", "MEDIUM", "comparison", "en"),
    _c("Summarize the key steps for making a proper French omelette", "MEDIUM", "summary", "en"),
    _c("Rewrite this recipe in metric units for a European audience", "MEDIUM", "rewrite", "en"),
    # ── Music theory: explanation, code, comparison ──
    _c("Write a function that returns the notes in a major scale given a root note", "MEDIUM", "simple-code", "en"),
    _c("Explain how voice leading works in four-part harmony", "MEDIUM", "explanation", "en"),
    _c("Compare parallel and relative key modulations", "MEDIUM", "comparison", "en"),
    _c("Create a chord progression generator that follows common jazz patterns", "MEDIUM", "simple-code", "en"),
    _c("Summarize the circle of fifths and its practical uses", "MEDIUM", "summary", "en"),
    _c("Classify these chord progressions by genre (pop, jazz, classical)", "MEDIUM", "classification", "en"),
    # ── Astronomy: explanation, data analysis ──
    _c(
        "Write a Python script to calculate the distance to a star given its parallax angle",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Explain why we see different phases of the Moon", "MEDIUM", "explanation", "en"),
    _c("Compare refracting vs reflecting telescopes for amateur astronomy", "MEDIUM", "comparison", "en"),
    _c("Summarize the lifecycle of a star from nebula to white dwarf", "MEDIUM", "summary", "en"),
    _c("Write a pandas script to analyze exoplanet discovery data and find trends", "MEDIUM", "data-analysis", "en"),
    # ── Linguistics: explanation, extraction, classification ──
    _c("Explain the difference between phonetics and phonology", "MEDIUM", "explanation", "en"),
    _c("Write a regex to extract all proper nouns from a text (simple heuristic)", "MEDIUM", "simple-code", "en"),
    _c("Compare agglutinative vs fusional language morphology", "MEDIUM", "comparison", "en"),
    _c(
        "Classify these words by their morphological structure (root, prefix, suffix)", "MEDIUM", "classification", "en"
    ),
    _c("Summarize the key differences between SOV and SVO word order", "MEDIUM", "summary", "en"),
    # ── Law: explanation, extraction, documentation ──
    _c("Explain the difference between civil and criminal law", "MEDIUM", "explanation", "en"),
    _c("Extract all parties and their roles from this contract excerpt", "MEDIUM", "extraction", "en"),
    _c("Summarize the key clauses in this NDA", "MEDIUM", "summary", "en"),
    _c("Compare trademark vs copyright protection", "MEDIUM", "comparison", "en"),
    _c("Write documentation for a contract review checklist", "MEDIUM", "documentation", "en"),
    # ── Medicine: explanation, classification, documentation ──
    _c("Explain the difference between type 1 and type 2 diabetes", "MEDIUM", "explanation", "en"),
    _c(
        "Classify these symptoms into likely organ systems (cardiovascular, respiratory, etc.)",
        "MEDIUM",
        "classification",
        "en",
    ),
    _c("Summarize the contraindications for a common medication", "MEDIUM", "summary", "en"),
    _c("Write a patient education document about hypertension management", "MEDIUM", "documentation", "en"),
    _c("Compare MRI and CT scan for brain imaging", "MEDIUM", "comparison", "en"),
    # ── Agriculture: explanation, code, data analysis ──
    _c("Explain how drip irrigation reduces water waste compared to flood irrigation", "MEDIUM", "explanation", "en"),
    _c(
        "Write a Python script to calculate optimal planting density from field area and crop spacing",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Compare organic vs conventional farming yields with data", "MEDIUM", "data-analysis", "en"),
    _c("Summarize the benefits of cover cropping for soil health", "MEDIUM", "summary", "en"),
    _c("Brainstorm 5 ways to reduce pesticide use while maintaining yield", "MEDIUM", "brainstorming", "en"),
    # ── Fashion: explanation, extraction, creative ──
    _c("Explain how to calculate fabric yardage for a gathered skirt", "MEDIUM", "explanation", "en"),
    _c("Extract all measurements from this pattern instruction", "MEDIUM", "extraction", "en"),
    _c("Compare woven vs knit fabric properties for garment design", "MEDIUM", "comparison", "en"),
    _c("Write a creative product description for a sustainable fashion line", "MEDIUM", "creative", "en"),
    _c("Summarize the key steps in pattern grading", "MEDIUM", "summary", "en"),
    # ── Architecture (buildings): explanation, comparison ──
    _c("Explain how a flying buttress distributes load in Gothic architecture", "MEDIUM", "explanation", "en"),
    _c("Compare load-bearing masonry vs steel frame construction", "MEDIUM", "comparison", "en"),
    _c("Summarize the key principles of passive solar design", "MEDIUM", "summary", "en"),
    _c("Write a specification document for a green roof installation", "MEDIUM", "documentation", "en"),
    # ── Sports analytics: code, data analysis, explanation ──
    _c(
        "Write a Python script to calculate a player's true shooting percentage from box score data",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Explain how expected goals (xG) is calculated in soccer", "MEDIUM", "explanation", "en"),
    _c("Compare WAR vs WARP for evaluating baseball players", "MEDIUM", "comparison", "en"),
    _c("Analyze this game log dataset and identify performance trends", "MEDIUM", "data-analysis", "en"),
    _c("Summarize the key metrics used in basketball analytics", "MEDIUM", "summary", "en"),
    # ── Supply chain: code, explanation, debugging ──
    _c(
        "Write a Python script to calculate reorder point given demand rate and lead time",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Explain the bullwhip effect in supply chains", "MEDIUM", "explanation", "en"),
    _c("Compare centralized vs decentralized inventory management", "MEDIUM", "comparison", "en"),
    _c("Our inventory levels are inconsistent across warehouses. How do I debug this?", "MEDIUM", "debugging", "en"),
    _c("Review this EOQ calculation for edge cases", "MEDIUM", "code-review", "en"),
    _c("Summarize the trade-offs in choosing a 3PL provider", "MEDIUM", "summary", "en"),
    # ── Testing, agentic, brainstorming ──
    _c("Write unit tests for this recipe scaling function", "MEDIUM", "testing", "en"),
    _c("Create integration tests for the matchmaking algorithm", "MEDIUM", "testing", "en"),
    _c("Find all TODO comments in this codebase and create tickets for each", "MEDIUM", "agentic-task", "en"),
    _c("Brainstorm 5 ways to reduce supply chain disruption risk", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm 3 approaches to improve game matchmaking fairness", "MEDIUM", "brainstorming", "en"),
    # ── Chinese MEDIUM ──
    _c("写一个 Python 脚本解析游戏存档 JSON 并提取玩家数据", "MEDIUM", "simple-code", "zh"),
    _c("解释梅拉德反应以及为什么它影响食物的褐变", "MEDIUM", "explanation", "zh"),
    _c("写一个函数给定根音返回大调音阶的音符", "MEDIUM", "simple-code", "zh"),
    _c("解释为什么我们看到月球的不同相位", "MEDIUM", "explanation", "zh"),
    _c("解释语音学和音系学的区别", "MEDIUM", "explanation", "zh"),
    _c("解释民法与刑法的区别", "MEDIUM", "explanation", "zh"),
    _c("解释 1 型和 2 型糖尿病的区别", "MEDIUM", "explanation", "zh"),
    _c("解释滴灌如何比漫灌减少水资源浪费", "MEDIUM", "explanation", "zh"),
    _c("解释供应链中的牛鞭效应", "MEDIUM", "explanation", "zh"),
    _c("审查这个游戏状态序列化代码的存档/读档 bug", "MEDIUM", "code-review", "zh"),
    # ── Japanese MEDIUM ──
    _c(
        "ゲームセーブファイルを解析してプレイヤーステータスを抽出するPythonスクリプトを書いてください",
        "MEDIUM",
        "simple-code",
        "ja",
    ),
    _c("メイラード反応と褐変の関係を説明してください", "MEDIUM", "explanation", "ja"),
    _c("根音から長調の音階の音符を返す関数を書いてください", "MEDIUM", "simple-code", "ja"),
    _c("月の満ち欠けが起こる理由を説明してください", "MEDIUM", "explanation", "ja"),
    _c("音声学と音韻論の違いを説明してください", "MEDIUM", "explanation", "ja"),
    _c("民法と刑法の違いを説明してください", "MEDIUM", "explanation", "ja"),
    _c("1型と2型糖尿病の違いを説明してください", "MEDIUM", "explanation", "ja"),
    _c("滴灌が漫灌に比べて水の無駄をどう減らすか説明してください", "MEDIUM", "explanation", "ja"),
    _c("サプライチェーンの牛鞭効果を説明してください", "MEDIUM", "explanation", "ja"),
    # ── Korean MEDIUM ──
    _c(
        "게임 세이브 파일을 파싱하여 플레이어 스탯을 추출하는 Python 스크립트를 작성하세요",
        "MEDIUM",
        "simple-code",
        "ko",
    ),
    _c("마이야르 반응과 갈변의 관계를 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("근음이 주어지면 장조 음계의 음을 반환하는 함수를 작성하세요", "MEDIUM", "simple-code", "ko"),
    _c("달의 위상이 변하는 이유를 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("음성학과 음운론의 차이를 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("민법과 형법의 차이를 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("1형과 2형 당뇨병의 차이를 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("공급망의 채찍 효과를 설명해주세요", "MEDIUM", "explanation", "ko"),
    # ── Arabic MEDIUM ──
    _c("اشرح الفرق بين الصوتيات والصوتيات اللغوية", "MEDIUM", "explanation", "ar"),
    _c("اشرح الفرق بين القانون المدني والجنائي", "MEDIUM", "explanation", "ar"),
    _c("اشرح الفرق بين النوع 1 والنوع 2 من مرض السكري", "MEDIUM", "explanation", "ar"),
    _c("اشرح تأثير السوط في سلاسل التوريد", "MEDIUM", "explanation", "ar"),
    # ── Russian MEDIUM ──
    _c("Объясни разницу между фонетикой и фонологией", "MEDIUM", "explanation", "ru"),
    _c("Объясни разницу между гражданским и уголовным правом", "MEDIUM", "explanation", "ru"),
    _c("Объясни разницу между диабетом 1 и 2 типа", "MEDIUM", "explanation", "ru"),
    _c("Объясни эффект хлыста в цепочках поставок", "MEDIUM", "explanation", "ru"),
    # ── Spanish MEDIUM ──
    _c("Explica la diferencia entre fonética y fonología", "MEDIUM", "explanation", "es"),
    _c("Explica la diferencia entre derecho civil y penal", "MEDIUM", "explanation", "es"),
    _c("Explica la diferencia entre diabetes tipo 1 y tipo 2", "MEDIUM", "explanation", "es"),
    _c("Explica el efecto látigo en las cadenas de suministro", "MEDIUM", "explanation", "es"),
    # ── German MEDIUM ──
    _c("Erkläre den Unterschied zwischen Phonetik und Phonologie", "MEDIUM", "explanation", "de"),
    _c("Erkläre den Unterschied zwischen Zivil- und Strafrecht", "MEDIUM", "explanation", "de"),
    _c("Erkläre den Unterschied zwischen Typ-1- und Typ-2-Diabetes", "MEDIUM", "explanation", "de"),
    _c("Erkläre den Peitscheneffekt in Lieferketten", "MEDIUM", "explanation", "de"),
    # ── French MEDIUM ──
    _c("Explique la différence entre phonétique et phonologie", "MEDIUM", "explanation", "fr"),
    _c("Explique la différence entre droit civil et pénal", "MEDIUM", "explanation", "fr"),
    _c("Explique la différence entre diabète de type 1 et type 2", "MEDIUM", "explanation", "fr"),
    _c("Explique l'effet bullwhip dans les chaînes d'approvisionnement", "MEDIUM", "explanation", "fr"),
    # ── Portuguese MEDIUM ──
    _c("Explique a diferença entre fonética e fonologia", "MEDIUM", "explanation", "pt"),
    _c("Explique a diferença entre direito civil e penal", "MEDIUM", "explanation", "pt"),
    _c("Explique a diferença entre diabetes tipo 1 e tipo 2", "MEDIUM", "explanation", "pt"),
    _c("Explique o efeito chicote nas cadeias de suprimentos", "MEDIUM", "explanation", "pt"),
    # ── Hindi MEDIUM ──
    _c("ध्वनिविज्ञान और स्वनिमिकी में अंतर समझाएं", "MEDIUM", "explanation", "hi"),
    _c("नागरिक और आपराधिक कानून में अंतर समझाएं", "MEDIUM", "explanation", "hi"),
    _c("टाइप 1 और टाइप 2 मधुमेह में अंतर समझाएं", "MEDIUM", "explanation", "hi"),
    _c("आपूर्ति श्रृंखला में चाबुक प्रभाव समझाएं", "MEDIUM", "explanation", "hi"),
    # ── Turkish MEDIUM ──
    _c("Fonetik ve fonoloji arasındaki farkı açıklayın", "MEDIUM", "explanation", "tr"),
    _c("Medeni hukuk ve ceza hukuku arasındaki farkı açıklayın", "MEDIUM", "explanation", "tr"),
    _c("Tip 1 ve Tip 2 diyabet arasındaki farkı açıklayın", "MEDIUM", "explanation", "tr"),
    _c("Tedarik zincirlerinde kırbaç etkisini açıklayın", "MEDIUM", "explanation", "tr"),
    # ── Vietnamese MEDIUM ──
    _c("Giải thích sự khác biệt giữa ngữ âm học và âm vị học", "MEDIUM", "explanation", "vi"),
    _c("Giải thích sự khác biệt giữa luật dân sự và hình sự", "MEDIUM", "explanation", "vi"),
    _c("Giải thích sự khác biệt giữa tiểu đường type 1 và type 2", "MEDIUM", "explanation", "vi"),
    _c("Giải thích hiệu ứng roi trong chuỗi cung ứng", "MEDIUM", "explanation", "vi"),
    # ── Polish MEDIUM ──
    _c("Wyjaśnij różnicę między fonetyką a fonologią", "MEDIUM", "explanation", "pl"),
    _c("Wyjaśnij różnicę między prawem cywilnym a karnym", "MEDIUM", "explanation", "pl"),
    _c("Wyjaśnij różnicę między cukrzycą typu 1 i typu 2", "MEDIUM", "explanation", "pl"),
    _c("Wyjaśnij efekt bata w łańcuchach dostaw", "MEDIUM", "explanation", "pl"),
    # ── More MEDIUM: rewrite, extraction, classification ──
    _c("Rewrite this legal disclaimer in plain language for consumers", "MEDIUM", "rewrite", "en"),
    _c("Extract all medication names and dosages from this prescription", "MEDIUM", "extraction", "en"),
    _c("Classify these game mechanics as PvE, PvP, or cooperative", "MEDIUM", "classification", "en"),
    _c("Rewrite this recipe for a gluten-free diet, suggesting substitutions", "MEDIUM", "rewrite", "en"),
    _c("Extract key financial terms from this supply contract", "MEDIUM", "extraction", "en"),
    _c("Classify these architectural styles: Gothic, Baroque, Modernist", "MEDIUM", "classification", "en"),
    _c("Rewrite this medical note for a patient-friendly summary", "MEDIUM", "rewrite", "en"),
    _c("Extract all crop types and planting dates from this farm log", "MEDIUM", "extraction", "en"),
    _c("Classify these music genres by typical chord progressions", "MEDIUM", "classification", "en"),
    _c("Rewrite this sports stat in layman's terms", "MEDIUM", "rewrite", "en"),
    # ── More MEDIUM: simple-code, explanation, comparison ──
    _c("Write a Python script to validate chess move notation (e.g., e2-e4)", "MEDIUM", "simple-code", "en"),
    _c(
        "Implement a function to convert between Celsius and Fahrenheit for recipe scaling",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Write a script to parse baseball box score format and extract batting stats", "MEDIUM", "simple-code", "en"),
    _c("Explain how crop rotation prevents soil depletion", "MEDIUM", "explanation", "en"),
    _c("Explain the difference between trademark and trade secret protection", "MEDIUM", "explanation", "en"),
    _c("Compare drip irrigation vs sprinkler systems for water efficiency", "MEDIUM", "comparison", "en"),
    _c("Compare common law vs civil law systems", "MEDIUM", "comparison", "en"),
    _c("Compare refracting vs reflecting telescopes", "MEDIUM", "comparison", "en"),
    _c("Explain how a cantilever bridge distributes load", "MEDIUM", "explanation", "en"),
    _c("Write a Python script to calculate fabric yardage for a rectangular tablecloth", "MEDIUM", "simple-code", "en"),
    # ── More MEDIUM: code-review, debugging, testing, documentation ──
    _c("Review this inventory reorder logic for race conditions", "MEDIUM", "code-review", "en"),
    _c("Our recipe scaling produces wrong fractions. How do I debug the rounding?", "MEDIUM", "debugging", "en"),
    _c("Write unit tests for the chord progression generator", "MEDIUM", "testing", "en"),
    _c("Write API documentation for the matchmaking endpoint", "MEDIUM", "documentation", "en"),
    _c("Review this astronomy distance calculation for floating-point precision issues", "MEDIUM", "code-review", "en"),
    _c("The supply chain forecast is off by 20%. What should I check first?", "MEDIUM", "debugging", "en"),
    _c("Write integration tests for the recipe scaling service", "MEDIUM", "testing", "en"),
    _c("Create a README for the sports analytics library", "MEDIUM", "documentation", "en"),
    # ── More MEDIUM: summary, creative, brainstorming, agentic ──
    _c("Summarize the key provisions of GDPR for a tech startup", "MEDIUM", "summary", "en"),
    _c("Summarize the lifecycle of a massive star", "MEDIUM", "summary", "en"),
    _c("Write a creative product tagline for an astronomy app", "MEDIUM", "creative", "en"),
    _c("Brainstorm 5 ways to reduce food waste in a restaurant supply chain", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm 3 approaches to balance a game's economy", "MEDIUM", "brainstorming", "en"),
    _c("Parse the game config, update the ELO decay rate, and run the balance tests", "MEDIUM", "agentic-task", "en"),
    _c("Find all hardcoded legal disclaimers and create a centralized config", "MEDIUM", "agentic-task", "en"),
    # ── More MEDIUM non-English to balance distribution ──
    _c("写一个 Python 脚本验证国际象棋着法记谱", "MEDIUM", "simple-code", "zh"),
    _c("解释作物轮作如何防止土壤贫瘠", "MEDIUM", "explanation", "zh"),
    _c("比较滴灌和喷灌系统的水效率", "MEDIUM", "comparison", "zh"),
    _c("审查这个库存补货逻辑的竞态条件", "MEDIUM", "code-review", "zh"),
    _c("总结 GDPR 对科技初创公司的关键条款", "MEDIUM", "summary", "zh"),
    _c("レシピのスケーリングで分数がおかしい。丸めのデバッグ方法は？", "MEDIUM", "debugging", "ja"),
    _c("和音進行ジェネレーターのユニットテストを書いてください", "MEDIUM", "testing", "ja"),
    _c("天文学の距離計算の浮動小数点精度をレビューしてください", "MEDIUM", "code-review", "ja"),
    _c("スポーツ分析ライブラリのREADMEを作成してください", "MEDIUM", "documentation", "ja"),
    _c("민법과 형법 체계를 비교해주세요", "MEDIUM", "comparison", "ko"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX (~100)
# ═══════════════════════════════════════════════════════════

COMPLEX_B8: list[dict] = [
    # ── Gaming: system design, complex code ──
    _c(
        "Design a multiplayer game backend with matchmaking, authoritative server, anti-cheat, replay system, and cross-region latency compensation.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a game engine physics subsystem with rigid body dynamics, collision detection, constraint solving, and spatial partitioning.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a live-service game economy with virtual currency, marketplace, anti-fraud, and balance tuning pipeline.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a networked game sync protocol with delta compression, interest management, and rollback netcode.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Cooking / food: system design ──
    _c(
        "Design a recipe recommendation platform with dietary constraints, ingredient substitution, scaling, nutrition analysis, and meal planning.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a food safety compliance system with HACCP tracking, supplier audits, recall management, and regulatory reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Music: complex system ──
    _c(
        "Design a music production platform with DAW integration, plugin hosting, collaboration, version control, and export pipelines.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build an automated music transcription pipeline with source separation, pitch detection, rhythm analysis, and notation generation.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    # ── Astronomy: infrastructure, ML ──
    _c(
        "Design an astronomy data pipeline for telescope observations: ingestion, calibration, reduction, catalog generation, and archive.",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    _c(
        "Build an exoplanet detection pipeline with light curve analysis, transit fitting, false positive filtering, and classification.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    # ── Linguistics: ML pipeline, migration ──
    _c(
        "Design an NLP pipeline for low-resource languages: data collection, annotation, model training, evaluation, and deployment.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    _c(
        "Plan a migration from rule-based to neural machine translation with A/B testing and quality monitoring.",
        "COMPLEX",
        "migration",
        "en",
    ),
    # ── Law: system design, security ──
    _c(
        "Design a legal document management system with version control, redaction, access control, audit trails, and e-discovery support.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Perform a security audit of a contract management platform. Identify attack vectors, compliance gaps, and propose mitigations.",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    # ── Medicine: system design, compliance ──
    _c(
        "Design a clinical trial management system with patient enrollment, consent tracking, adverse event reporting, and regulatory submission.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a medical imaging pipeline with DICOM ingestion, anonymization, AI inference, and radiologist workflow integration.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    # ── Agriculture: system design, infrastructure ──
    _c(
        "Design a precision agriculture platform with sensor networks, satellite imagery, yield prediction, irrigation control, and supply chain integration.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a farm management system with crop planning, inventory, equipment tracking, labor scheduling, and compliance reporting.",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    # ── Fashion: system design ──
    _c(
        "Design an apparel supply chain platform with design-to-manufacturing workflow, size grading, material sourcing, and sustainability tracking.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a fashion recommendation engine with style analysis, fit prediction, inventory optimization, and personalization.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    # ── Architecture (buildings): system design ──
    _c(
        "Design a building information modeling (BIM) platform with 3D modeling, clash detection, quantity takeoff, and contractor coordination.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a smart building management system with HVAC optimization, occupancy sensing, energy analytics, and maintenance prediction.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    # ── Sports analytics: complex system ──
    _c(
        "Design a sports analytics platform with real-time data ingestion, play-by-play analysis, player tracking, and coaching dashboard.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a player valuation model with performance metrics, contract data, injury history, and market comparables.",
        "COMPLEX",
        "data-analysis",
        "en",
    ),
    # ── Supply chain: complex systems ──
    _c(
        "Design a global supply chain visibility platform with real-time tracking, demand forecasting, risk scoring, and supplier collaboration.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Plan a migration from legacy ERP to modern SCM with data migration, integration, and phased rollout.",
        "COMPLEX",
        "migration",
        "en",
    ),
    _c(
        "Design a supply chain security framework with supplier vetting, shipment verification, and tamper detection.",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    _c(
        "Optimize a multi-echelon inventory network: safety stock, reorder points, and transportation cost trade-offs.",
        "COMPLEX",
        "performance",
        "en",
    ),
    # ── Adversarial: short-but-COMPLEX ──
    _c(
        "Implement a Raft consensus module with leader election, log replication, membership changes, and snapshotting.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a zero-trust API gateway with mTLS, OPA policies, rate limiting, and audit logging.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    _c(
        "Build a CRDT-based collaborative editor with operational transforms and conflict resolution.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Chinese COMPLEX ──
    _c("设计一个多人游戏后端，包括匹配、权威服务器、反作弊、回放系统和跨区延迟补偿", "COMPLEX", "system-design", "zh"),
    _c("设计一个食谱推荐平台，包括饮食限制、食材替代、份量调整、营养分析和膳食计划", "COMPLEX", "system-design", "zh"),
    _c("设计一个临床实验管理系统，包括患者入组、知情同意、不良事件报告和监管提交", "COMPLEX", "system-design", "zh"),
    _c(
        "设计一个精准农业平台，包括传感器网络、卫星影像、产量预测、灌溉控制和供应链集成",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c("设计一个全球供应链可视化平台，包括实时追踪、需求预测、风险评分和供应商协作", "COMPLEX", "system-design", "zh"),
    # ── Japanese COMPLEX ──
    _c(
        "マルチプレイヤーゲームバックエンドを設計してください。マッチング、オーソリティティブサーバー、アンチチート、リプレイシステムを含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "レシピ推薦プラットフォームを設計してください。食事制限、食材代替、スケーリング、栄養分析を含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "臨床試験管理システムを設計してください。患者登録、同意追跡、有害事象報告を含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "精密農業プラットフォームを設計してください。センサーネットワーク、衛星画像、収量予測、灌漑制御を含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "グローバルサプライチェーン可視化プラットフォームを設計してください。リアルタイム追跡、需要予測、リスクスコアリングを含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    # ── Korean COMPLEX ──
    _c(
        "멀티플레이어 게임 백엔드를 설계하세요. 매칭, 권위 서버, 반칙 방지, 리플레이 시스템을 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "레시피 추천 플랫폼을 설계하세요. 식이 제한, 재료 대체, 스케일링, 영양 분석을 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "임상 시험 관리 시스템을 설계하세요. 환자 등록, 동의 추적, 부작용 보고를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "정밀 농업 플랫폼을 설계하세요. 센서 네트워크, 위성 영상, 수확량 예측, 관개 제어를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "글로벌 공급망 가시성 플랫폼을 설계하세요. 실시간 추적, 수요 예측, 리스크 스코어링을 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    # ── Arabic COMPLEX ──
    _c(
        "صمم نظام خلفي لألعاب متعددة اللاعبين يشمل المطابقة والخادم الموثوق ومكافحة الغش ونظام إعادة التشغيل.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "صمم منصة توصية وصفات تشمل قيود النظام الغذائي واستبدال المكونات والتحجيم وتحليل التغذية.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "صمم نظام إدارة التجارب السريرية يشمل تسجيل المرضى وتتبع الموافقة والإبلاغ عن الأحداث الضارة.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "صمم منصة زراعة دقيقة تشمل شبكات الاستشعار والصور الفضائية والتنبؤ بالمحصول والتحكم في الري.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    # ── Portuguese COMPLEX ──
    _c(
        "Projete um backend de jogo multiplayer com matchmaking, servidor autoritativo, anti-cheat e sistema de replay.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "Projete uma plataforma de recomendação de receitas com restrições dietéticas, substituição de ingredientes e análise nutricional.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "Projete um sistema de gerenciamento de ensaios clínicos com recrutamento, consentimento e relatórios de eventos adversos.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "Projete uma plataforma de agricultura de precisão com sensores, imagens de satélite e previsão de produtividade.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    # ── Russian COMPLEX ──
    _c(
        "Спроектируй бэкенд многопользовательской игры с матчмейкингом, авторитетным сервером, античитом и системой реплеев.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Спроектируй платформу рекомендаций рецептов с диетическими ограничениями, заменой ингредиентов и анализом питания.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Спроектируй систему управления клиническими испытаниями с набором пациентов, согласием и отчётами о побочных эффектах.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Спроектируй платформу точного земледелия с сенсорами, спутниковой съёмкой и прогнозом урожайности.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    # ── Spanish COMPLEX ──
    _c(
        "Diseña un backend de juego multijugador con emparejamiento, servidor autoritativo, anti-trampas y sistema de repetición.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Diseña una plataforma de recomendación de recetas con restricciones dietéticas, sustitución de ingredientes y análisis nutricional.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Diseña un sistema de gestión de ensayos clínicos con reclutamiento, consentimiento y reporte de eventos adversos.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Diseña una plataforma de agricultura de precisión con sensores, imágenes satelitales y predicción de rendimiento.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    # ── German COMPLEX ──
    _c(
        "Entwerfe ein Multiplayer-Spiel-Backend mit Matchmaking, autoritativem Server, Anti-Cheat und Replay-System.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Entwerfe eine Rezeptempfehlungsplattform mit Diätbeschränkungen, Zutatenersatz und Nährwertanalyse.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Entwerfe ein klinisches Studienmanagementsystem mit Patientenanwerbung, Einwilligung und Nebenwirkungsberichterstattung.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Entwerfe eine Präzisionslandwirtschaftsplattform mit Sensornetzwerken, Satellitenbildern und Ertragsprognose.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    # ── French COMPLEX ──
    _c(
        "Conçois un backend de jeu multijoueur avec matchmaking, serveur autoritaire, anti-triche et système de replay.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    _c(
        "Conçois une plateforme de recommandation de recettes avec contraintes diététiques, substitution d'ingrédients et analyse nutritionnelle.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    _c(
        "Conçois un système de gestion d'essais cliniques avec recrutement, consentement et signalement des événements indésirables.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    _c(
        "Conçois une plateforme d'agriculture de précision avec capteurs, imagerie satellite et prédiction de rendement.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    # ── Hindi COMPLEX ──
    _c(
        "मल्टीप्लेयर गेम बैकएंड डिज़ाइन करें जिसमें मैचमेकिंग, अथॉरिटेटिव सर्वर, एंटी-चीट और रिप्ले सिस्टम शामिल हो।",
        "COMPLEX",
        "system-design",
        "hi",
    ),
    # ── Turkish COMPLEX ──
    _c(
        "Eşleştirme, yetkili sunucu, anti-cheat ve tekrar sistemi içeren çok oyunculu oyun arka ucu tasarlayın.",
        "COMPLEX",
        "system-design",
        "tr",
    ),
    # ── Vietnamese COMPLEX ──
    _c(
        "Thiết kế backend trò chơi nhiều người chơi với ghép cặp, máy chủ có thẩm quyền, chống gian lận và hệ thống phát lại.",
        "COMPLEX",
        "system-design",
        "vi",
    ),
    # ── Polish COMPLEX ──
    _c(
        "Zaprojektuj backend gry wieloosobowej z matchmakingiem, serwerem autorytatywnym, anti-cheatem i systemem powtórek.",
        "COMPLEX",
        "system-design",
        "pl",
    ),
    # ── More COMPLEX: architecture, infrastructure, ml-pipeline, performance ──
    _c(
        "Design a legal document workflow with version control, e-signature, audit trails, and compliance reporting.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    _c(
        "Build a farm IoT platform with soil sensors, weather integration, irrigation automation, and yield prediction.",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    _c(
        "Design an automated music transcription pipeline with source separation, pitch detection, and notation export.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    _c(
        "Optimize a supply chain simulation: reduce runtime from 2 hours to 15 minutes while preserving accuracy.",
        "COMPLEX",
        "performance",
        "en",
    ),
    _c(
        "Design a fashion e-commerce platform with virtual try-on, size recommendation, and inventory optimization.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a clinical decision support system with symptom input, differential diagnosis, and evidence retrieval.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    _c(
        "Design a sports betting risk management system with odds calculation, exposure limits, and fraud detection.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Plan a migration from monolithic farm management software to microservices with zero downtime.",
        "COMPLEX",
        "migration",
        "en",
    ),
    _c(
        "Design a building energy management system with sensor fusion, occupancy prediction, and HVAC optimization.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    _c(
        "Perform a security audit of a healthcare data platform. Address HIPAA, encryption, and access control.",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    _c(
        "Design a linguistics corpus annotation platform with inter-annotator agreement, quality control, and export.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a recipe recommendation engine with dietary constraints, ingredient availability, and nutrition optimization.",
        "COMPLEX",
        "ml-pipeline",
        "en",
    ),
    _c(
        "Design a multi-warehouse inventory optimization system with demand forecasting and transportation routing.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a game server with authoritative physics, client prediction, lag compensation, and replay.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design an astronomy observatory scheduling system with telescope allocation, weather integration, and priority queuing.",
        "COMPLEX",
        "infrastructure",
        "en",
    ),
    # ── More COMPLEX non-English ──
    _c("设计一个法律文档工作流，包括版本控制、电子签名、审计追踪和合规报告", "COMPLEX", "architecture", "zh"),
    _c("设计一个时尚电商平台，包括虚拟试穿、尺码推荐和库存优化", "COMPLEX", "system-design", "zh"),
    _c("设计一个农场物联网平台，包括土壤传感器、天气整合、灌溉自动化和产量预测", "COMPLEX", "infrastructure", "zh"),
    _c(
        "医療データプラットフォームのセキュリティ監査を実施してください。HIPAA、暗号化、アクセス制御を検討してください。",
        "COMPLEX",
        "security-analysis",
        "ja",
    ),
    _c(
        "다중 창고 재고 최적화 시스템을 설계하세요. 수요 예측과 운송 경로 최적화를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
]


# ═══════════════════════════════════════════════════════════
#  REASONING (~80)
# ═══════════════════════════════════════════════════════════

REASONING_B8: list[dict] = [
    # ── Formal proofs ──
    _c(
        "Prove that the sum of the first n positive integers equals n(n+1)/2 using mathematical induction.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that sqrt(2) is irrational using proof by contradiction.", "REASONING", "formal-proof", "en"),
    _c("Prove that there are infinitely many prime numbers. Use Euclid's argument.", "REASONING", "formal-proof", "en"),
    _c("Prove that a tree with n vertices has exactly n-1 edges. Use induction.", "REASONING", "formal-proof", "en"),
    _c("Prove that the rationals are countable using a diagonal argument.", "REASONING", "formal-proof", "en"),
    _c("Prove that every planar graph has a vertex of degree at most 5.", "REASONING", "formal-proof", "en"),
    # ── Math derivations ──
    _c(
        "Derive the formula for the sum of a geometric series. Prove convergence when |r| < 1.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c("Derive the quadratic formula by completing the square. Show all steps.", "REASONING", "math-derivation", "en"),
    _c(
        "Derive the formula for the nth Fibonacci number using generating functions.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the expected value of a geometric random variable. Prove it equals 1/p.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c("Derive the Stirling approximation for n! and prove the error bound.", "REASONING", "math-derivation", "en"),
    # ── Algorithm proofs ──
    _c(
        "Prove that Dijkstra's algorithm finds shortest paths in graphs with non-negative weights. Use induction on distance.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that binary search runs in O(log n) time. State and prove the recurrence.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that merge sort is correct using induction on the merge operation.", "REASONING", "algorithm-proof", "en"
    ),
    _c(
        "Prove that the greedy algorithm for activity selection is optimal. Use the exchange argument.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that Huffman coding produces an optimal prefix code. Use the lemma about merging.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    # ── Game theory ──
    _c(
        "In the ultimatum game, derive the subgame-perfect equilibrium. Prove why the responder accepts any positive offer.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Prove that in a finite two-player zero-sum game, a Nash equilibrium always exists. Use the minimax theorem.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "In a second-price auction with n bidders, prove that truthful bidding is a dominant strategy.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Derive the mixed strategy Nash equilibrium for matching pennies. Show the indifference condition.",
        "REASONING",
        "game-theory",
        "en",
    ),
    # ── Logic puzzles ──
    _c(
        "Three boxes: one has two gold coins, one has two silver, one has one of each. You pick a gold coin. Prove the probability the other is gold is 2/3.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    _c(
        "Prove that in the Monty Hall problem, switching gives 2/3 probability of winning. Use Bayes' theorem.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    _c(
        "N people have hats. Each sees others' hats. Prove that with perfect play, exactly N-1 guesses can be correct.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    _c(
        "Prove that the poisoned wine puzzle with 1000 bottles and 10 prisoners has a solution using binary encoding.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    # ── Formal logic ──
    _c("Prove that (P → Q) ∧ (Q → R) ⊢ (P → R) using natural deduction.", "REASONING", "formal-logic", "en"),
    _c(
        "Prove that ¬(P ∧ Q) is logically equivalent to (¬P ∨ ¬Q) using truth tables and then semantic argument.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    _c(
        "Prove that the resolution rule is sound: if C1 and C2 are satisfiable and resolve to C3, then C1 ∧ C2 → C3.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    # ── Chinese REASONING ──
    _c("用数学归纳法证明前 n 个正整数的和等于 n(n+1)/2。", "REASONING", "formal-proof", "zh"),
    _c("用反证法证明 sqrt(2) 是无理数。", "REASONING", "formal-proof", "zh"),
    _c("推导等比数列求和公式，证明当 |r| < 1 时收敛。", "REASONING", "math-derivation", "zh"),
    _c("证明 Dijkstra 算法在非负权图中找到最短路径。对距离使用归纳法。", "REASONING", "algorithm-proof", "zh"),
    _c("在蒙提霍尔问题中，证明换门获胜概率为 2/3。使用贝叶斯定理。", "REASONING", "logic-puzzle", "zh"),
    # ── Japanese REASONING ──
    _c(
        "数学的帰納法を用いて、最初のn個の正の整数の和がn(n+1)/2であることを証明してください。",
        "REASONING",
        "formal-proof",
        "ja",
    ),
    _c("背理法を用いて√2が無理数であることを証明してください。", "REASONING", "formal-proof", "ja"),
    _c(
        "等比級数の和の公式を導出してください。|r|<1のとき収束することを証明してください。",
        "REASONING",
        "math-derivation",
        "ja",
    ),
    _c(
        "ダイクストラ法が非負重みグラフで最短経路を見つけることを証明してください。",
        "REASONING",
        "algorithm-proof",
        "ja",
    ),
    _c(
        "モンティ・ホール問題で、ドアを変えると勝つ確率が2/3であることを証明してください。",
        "REASONING",
        "logic-puzzle",
        "ja",
    ),
    # ── Korean REASONING ──
    _c(
        "수학적 귀납법을 사용하여 처음 n개의 양의 정수의 합이 n(n+1)/2임을 증명하세요.",
        "REASONING",
        "formal-proof",
        "ko",
    ),
    _c("귀류법을 사용하여 √2가 무리수임을 증명하세요.", "REASONING", "formal-proof", "ko"),
    _c("등비급수의 합 공식을 유도하세요. |r|<1일 때 수렴함을 증명하세요.", "REASONING", "math-derivation", "ko"),
    _c(
        "다익스트라 알고리즘이 비음수 가중치 그래프에서 최단 경로를 찾음을 증명하세요.",
        "REASONING",
        "algorithm-proof",
        "ko",
    ),
    _c("몬티 홀 문제에서 문을 바꾸면 이길 확률이 2/3임을 증명하세요.", "REASONING", "logic-puzzle", "ko"),
    # ── Arabic REASONING ──
    _c(
        "أثبت أن مجموع أول n أعداد صحيحة موجبة يساوي n(n+1)/2 باستخدام الاستقراء الرياضي.",
        "REASONING",
        "formal-proof",
        "ar",
    ),
    _c("أثبت أن الجذر التربيعي لـ 2 غير نسبي باستخدام البرهان بالتناقض.", "REASONING", "formal-proof", "ar"),
    _c("اشتق صيغة مجموع المتسلسلة الهندسية. أثبت التقارب عندما |r| < 1.", "REASONING", "math-derivation", "ar"),
    # ── Portuguese REASONING ──
    _c(
        "Prove que a soma dos primeiros n inteiros positivos é n(n+1)/2 usando indução matemática.",
        "REASONING",
        "formal-proof",
        "pt",
    ),
    _c("Prove que sqrt(2) é irracional usando prova por contradição.", "REASONING", "formal-proof", "pt"),
    _c(
        "Derive a fórmula da soma da série geométrica. Prove convergência quando |r| < 1.",
        "REASONING",
        "math-derivation",
        "pt",
    ),
    # ── Russian REASONING ──
    _c(
        "Докажи, что сумма первых n положительных целых равна n(n+1)/2, используя математическую индукцию.",
        "REASONING",
        "formal-proof",
        "ru",
    ),
    _c("Докажи, что sqrt(2) иррационален, используя доказательство от противного.", "REASONING", "formal-proof", "ru"),
    _c(
        "Выведи формулу суммы геометрической прогрессии. Докажи сходимость при |r| < 1.",
        "REASONING",
        "math-derivation",
        "ru",
    ),
    # ── Spanish REASONING ──
    _c(
        "Demuestra que la suma de los primeros n enteros positivos es n(n+1)/2 usando inducción matemática.",
        "REASONING",
        "formal-proof",
        "es",
    ),
    _c("Demuestra que sqrt(2) es irracional usando prueba por contradicción.", "REASONING", "formal-proof", "es"),
    _c(
        "Deriva la fórmula de la suma de la serie geométrica. Demuestra convergencia cuando |r| < 1.",
        "REASONING",
        "math-derivation",
        "es",
    ),
    # ── German REASONING ──
    _c(
        "Beweise, dass die Summe der ersten n positiven ganzen Zahlen n(n+1)/2 ist, mit vollständiger Induktion.",
        "REASONING",
        "formal-proof",
        "de",
    ),
    _c("Beweise, dass sqrt(2) irrational ist, mit Widerspruchsbeweis.", "REASONING", "formal-proof", "de"),
    # ── French REASONING ──
    _c(
        "Démontre que la somme des n premiers entiers positifs vaut n(n+1)/2 par récurrence.",
        "REASONING",
        "formal-proof",
        "fr",
    ),
    _c("Démontre que sqrt(2) est irrationnel par l'absurde.", "REASONING", "formal-proof", "fr"),
    # ── Hindi REASONING ──
    _c("गणितीय आगमन द्वारा सिद्ध करें कि पहले n धनात्मक पूर्णांकों का योग n(n+1)/2 है।", "REASONING", "formal-proof", "hi"),
    # ── Turkish REASONING ──
    _c(
        "Matematiksel tümevarım kullanarak ilk n pozitif tam sayının toplamının n(n+1)/2 olduğunu kanıtlayın.",
        "REASONING",
        "formal-proof",
        "tr",
    ),
    # ── Vietnamese REASONING ──
    _c(
        "Chứng minh rằng tổng n số nguyên dương đầu tiên bằng n(n+1)/2 bằng quy nạp toán học.",
        "REASONING",
        "formal-proof",
        "vi",
    ),
    # ── Polish REASONING ──
    _c(
        "Udowodnij, że suma pierwszych n liczb całkowitych dodatnich wynosi n(n+1)/2, używając indukcji matematycznej.",
        "REASONING",
        "formal-proof",
        "pl",
    ),
    # ── More REASONING: formal-proof, math-derivation, algorithm-proof, logic-puzzle ──
    _c(
        "Prove that the product of two consecutive integers is always even. Use direct proof.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that a graph is bipartite if and only if it contains no odd cycles.", "REASONING", "formal-proof", "en"),
    _c(
        "Derive the formula for the sum of an arithmetic series. Prove it using induction.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the binomial theorem (a+b)^n = sum C(n,k) a^k b^(n-k). Prove by induction.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Prove that heap sort runs in O(n log n) in-place. Analyze the heapify and extract operations.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the greedy coin-changing algorithm is optimal for standard US denominations.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "In the 100 prisoners and light bulb puzzle, prove the optimal strategy succeeds with probability > 30%.",
        "REASONING",
        "logic-puzzle",
        "en",
    ),
    _c(
        "Prove that in a knockout tournament with n teams, exactly n-1 games are played.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Derive the closed form for the recurrence T(n) = 2T(n/2) + n. Prove it's O(n log n).",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c("Prove that a binary heap with n elements has height floor(log2(n)).", "REASONING", "formal-proof", "en"),
    # ── More REASONING non-English ──
    _c("用直接证明证明两个连续整数的乘积总是偶数。", "REASONING", "formal-proof", "zh"),
    _c("推导等差数列求和公式，用归纳法证明。", "REASONING", "math-derivation", "zh"),
    _c("证明堆排序在原位运行且为 O(n log n)。分析 heapify 和 extract 操作。", "REASONING", "algorithm-proof", "zh"),
    _c("連続する2つの整数の積は常に偶数であることを直接証明で示してください。", "REASONING", "formal-proof", "ja"),
    _c("等差数列の和の公式を導出し、帰納法で証明してください。", "REASONING", "math-derivation", "ja"),
    _c("연속된 두 정수의 곱은 항상 짝수임을 직접 증명으로 보이세요.", "REASONING", "formal-proof", "ko"),
]


ALL_B8 = SIMPLE_B8 + MEDIUM_B8 + COMPLEX_B8 + REASONING_B8


def export(path: str | Path | None = None) -> None:
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b8.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B8:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter

    tiers = Counter(c["expected_tier"] for c in ALL_B8)
    langs = Counter(c["lang"] for c in ALL_B8)
    cats = Counter(c["category"] for c in ALL_B8)
    print(f"Batch 8: {len(ALL_B8)} cases → {out}")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")
    print(f"  Categories: {len(cats)}")


if __name__ == "__main__":
    import sys

    export(sys.argv[1] if len(sys.argv) > 1 else None)

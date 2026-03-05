"""Hand-crafted batch 10 — ~500 unique cases for LLM router classifier.

Strategy:
- NEW domains: renewable energy, 3D printing, drone technology, cryptocurrency mining,
  ocean science, neuroscience, urban planning, podcast production, e-commerce logistics,
  social media analytics, food science, environmental engineering
- MORE weak categories: code-review, debugging, summary, testing, brainstorming, migration, performance
- Adversarial: long-but-SIMPLE, short-but-COMPLEX, misleading technical jargon
- 14+ languages, English ~40%
- Zero overlap with batches 1–9
"""

from __future__ import annotations


def _c(prompt: str, tier: str, cat: str, lang: str) -> dict:
    return {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}


# ═══════════════════════════════════════════════════════════
#  SIMPLE (~140)
# ═══════════════════════════════════════════════════════════

SIMPLE_B10: list[dict] = [
    # ── Renewable energy factual ──
    _c("What is a photovoltaic cell?", "SIMPLE", "factual-qa", "en"),
    _c("What is grid parity?", "SIMPLE", "factual-qa", "en"),
    _c("What is net metering?", "SIMPLE", "factual-qa", "en"),
    _c("What is geothermal energy?", "SIMPLE", "factual-qa", "en"),
    _c("What is tidal energy?", "SIMPLE", "factual-qa", "en"),

    # ── 3D printing factual ──
    _c("What is FDM in 3D printing?", "SIMPLE", "factual-qa", "en"),
    _c("What is SLA printing?", "SIMPLE", "factual-qa", "en"),
    _c("What is infill percentage?", "SIMPLE", "factual-qa", "en"),
    _c("What is PLA filament?", "SIMPLE", "factual-qa", "en"),
    _c("What is a G-code file?", "SIMPLE", "factual-qa", "en"),

    # ── Drone technology factual ──
    _c("What is a quadcopter?", "SIMPLE", "factual-qa", "en"),
    _c("What is BVLOS in drone operations?", "SIMPLE", "factual-qa", "en"),
    _c("What is a flight controller?", "SIMPLE", "factual-qa", "en"),
    _c("What is geofencing for drones?", "SIMPLE", "factual-qa", "en"),
    _c("What is payload capacity in drones?", "SIMPLE", "factual-qa", "en"),

    # ── Cryptocurrency mining factual ──
    _c("What is a hash rate?", "SIMPLE", "factual-qa", "en"),
    _c("What is proof of work?", "SIMPLE", "factual-qa", "en"),
    _c("What is a mining pool?", "SIMPLE", "factual-qa", "en"),
    _c("What is an ASIC miner?", "SIMPLE", "factual-qa", "en"),
    _c("What is a block reward?", "SIMPLE", "factual-qa", "en"),

    # ── Ocean science factual ──
    _c("What is the thermocline?", "SIMPLE", "factual-qa", "en"),
    _c("What is ocean acidification?", "SIMPLE", "factual-qa", "en"),
    _c("What is an AUV?", "SIMPLE", "factual-qa", "en"),
    _c("What is upwelling?", "SIMPLE", "factual-qa", "en"),
    _c("What is the abyssal zone?", "SIMPLE", "factual-qa", "en"),

    # ── Neuroscience factual ──
    _c("What is a neuron?", "SIMPLE", "factual-qa", "en"),
    _c("What is a synapse?", "SIMPLE", "factual-qa", "en"),
    _c("What is fMRI?", "SIMPLE", "factual-qa", "en"),
    _c("What is neuroplasticity?", "SIMPLE", "factual-qa", "en"),
    _c("What is a neurotransmitter?", "SIMPLE", "factual-qa", "en"),

    # ── Urban planning factual ──
    _c("What is zoning?", "SIMPLE", "factual-qa", "en"),
    _c("What is transit-oriented development?", "SIMPLE", "factual-qa", "en"),
    _c("What is mixed-use development?", "SIMPLE", "factual-qa", "en"),
    _c("What is urban sprawl?", "SIMPLE", "factual-qa", "en"),
    _c("What is walkability?", "SIMPLE", "factual-qa", "en"),

    # ── Podcast production factual ──
    _c("What is a DAW?", "SIMPLE", "factual-qa", "en"),
    _c("What is compression in audio?", "SIMPLE", "factual-qa", "en"),
    _c("What is RSS for podcasts?", "SIMPLE", "factual-qa", "en"),
    _c("What is LUFS?", "SIMPLE", "factual-qa", "en"),
    _c("What is a condenser mic?", "SIMPLE", "factual-qa", "en"),

    # ── E-commerce logistics factual ──
    _c("What is last-mile delivery?", "SIMPLE", "factual-qa", "en"),
    _c("What is a fulfillment center?", "SIMPLE", "factual-qa", "en"),
    _c("What is dropshipping?", "SIMPLE", "factual-qa", "en"),
    _c("What is a 3PL?", "SIMPLE", "factual-qa", "en"),
    _c("What is reverse logistics?", "SIMPLE", "factual-qa", "en"),

    # ── Social media analytics factual ──
    _c("What is engagement rate?", "SIMPLE", "factual-qa", "en"),
    _c("What is reach vs impressions?", "SIMPLE", "factual-qa", "en"),
    _c("What is sentiment analysis?", "SIMPLE", "factual-qa", "en"),
    _c("What is organic reach?", "SIMPLE", "factual-qa", "en"),
    _c("What is share of voice?", "SIMPLE", "factual-qa", "en"),

    # ── Food science factual ──
    _c("What is the Maillard reaction?", "SIMPLE", "factual-qa", "en"),
    _c("What is pasteurization?", "SIMPLE", "factual-qa", "en"),
    _c("What is HACCP?", "SIMPLE", "factual-qa", "en"),
    _c("What is shelf life?", "SIMPLE", "factual-qa", "en"),
    _c("What is umami?", "SIMPLE", "factual-qa", "en"),

    # ── Environmental engineering factual ──
    _c("What is bioremediation?", "SIMPLE", "factual-qa", "en"),
    _c("What is BOD in wastewater?", "SIMPLE", "factual-qa", "en"),
    _c("What is an LCA?", "SIMPLE", "factual-qa", "en"),
    _c("What is a carbon footprint?", "SIMPLE", "factual-qa", "en"),
    _c("What is eutrophication?", "SIMPLE", "factual-qa", "en"),

    # ── Definitions ──
    _c("Define extrusion in 3D printing", "SIMPLE", "definition", "en"),
    _c("What is a blockchain?", "SIMPLE", "definition", "en"),
    _c("What is a watershed?", "SIMPLE", "definition", "en"),
    _c("What is a supply chain?", "SIMPLE", "definition", "en"),

    # ── Translations / greetings ──
    _c("Translate 'renewable energy' to Japanese", "SIMPLE", "translation", "en"),
    _c("How do you say '3D printing' in German?", "SIMPLE", "translation", "en"),
    _c("Translate 'drone' to Arabic", "SIMPLE", "translation", "en"),
    _c("How do you say 'hello' in Vietnamese?", "SIMPLE", "translation", "en"),
    _c("Hey there", "SIMPLE", "greeting", "en"),
    _c("Good afternoon", "SIMPLE", "greeting", "en"),
    _c("See you", "SIMPLE", "greeting", "en"),

    # ── Adversarial: long-but-SIMPLE ──
    _c("I've been reading about renewable energy and I keep seeing the term 'grid parity' mentioned in articles. Could you give me a simple one-sentence definition of what grid parity means?", "SIMPLE", "factual-qa", "en"),
    _c("My friend is into 3D printing and mentioned something called infill. I have no idea what that is. Can you explain in one sentence?", "SIMPLE", "factual-qa", "en"),
    _c("I'm writing a report on ocean science and need to know: what exactly is the thermocline? Just a brief definition please.", "SIMPLE", "factual-qa", "en"),
    _c("Someone at the crypto meetup said 'hash rate' and everyone nodded. What does hash rate mean in one sentence?", "SIMPLE", "factual-qa", "en"),
    _c("The urban planning document mentions 'transit-oriented development.' I need a quick definition for my notes.", "SIMPLE", "factual-qa", "en"),

    # ── Adversarial: misleading jargon but SIMPLE ──
    _c("What is a distributed ledger?", "SIMPLE", "factual-qa", "en"),
    _c("What is additive manufacturing?", "SIMPLE", "factual-qa", "en"),
    _c("What is a neural network?", "SIMPLE", "factual-qa", "en"),
    _c("What is machine learning?", "SIMPLE", "factual-qa", "en"),
    _c("What is cloud computing?", "SIMPLE", "factual-qa", "en"),

    # ── Chinese ──
    _c("什么是光伏电池？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 FDM 3D 打印？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是四旋翼无人机？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是哈希率？", "SIMPLE", "factual-qa", "zh"),
    _c("你好", "SIMPLE", "greeting", "zh"),

    # ── Japanese ──
    _c("光起電力セルとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("FDM 3Dプリントとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("クアッドコプターとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("こんにちは", "SIMPLE", "greeting", "ja"),

    # ── Korean ──
    _c("광전지란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("FDM 3D 프린팅이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("쿼드콥터란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("안녕하세요", "SIMPLE", "greeting", "ko"),

    # ── Arabic ──
    _c("ما هي الخلية الضوئية؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو الكوادكوبتر؟", "SIMPLE", "factual-qa", "ar"),
    _c("مرحبا", "SIMPLE", "greeting", "ar"),

    # ── Russian ──
    _c("Что такое фотоэлектрический элемент?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое квадрокоптер?", "SIMPLE", "factual-qa", "ru"),
    _c("Привет", "SIMPLE", "greeting", "ru"),

    # ── Spanish ──
    _c("¿Qué es una célula fotovoltaica?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un cuadricóptero?", "SIMPLE", "factual-qa", "es"),
    _c("Hola", "SIMPLE", "greeting", "es"),

    # ── German ──
    _c("Was ist eine Photovoltaikzelle?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein Quadrocopter?", "SIMPLE", "factual-qa", "de"),
    _c("Hallo", "SIMPLE", "greeting", "de"),

    # ── French ──
    _c("Qu'est-ce qu'une cellule photovoltaïque ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un quadricoptère ?", "SIMPLE", "factual-qa", "fr"),
    _c("Bonjour", "SIMPLE", "greeting", "fr"),

    # ── Portuguese ──
    _c("O que é uma célula fotovoltaica?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um quadricóptero?", "SIMPLE", "factual-qa", "pt"),
    _c("Olá", "SIMPLE", "greeting", "pt"),

    # ── Hindi ──
    _c("फोटोवोल्टिक सेल क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("नमस्ते", "SIMPLE", "greeting", "hi"),

    # ── Turkish ──
    _c("Fotovoltaik hücre nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Merhaba", "SIMPLE", "greeting", "tr"),

    # ── Vietnamese ──
    _c("Tế bào quang điện là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Xin chào", "SIMPLE", "greeting", "vi"),

    # ── Polish ──
    _c("Co to jest ogniwo fotowoltaiczne?", "SIMPLE", "factual-qa", "pl"),
    _c("Cześć", "SIMPLE", "greeting", "pl"),

    # ── More SIMPLE to reach ~140 ──
    _c("What is a heat exchanger?", "SIMPLE", "factual-qa", "en"),
    _c("What is retraction in 3D printing?", "SIMPLE", "factual-qa", "en"),
    _c("What is waypoint navigation?", "SIMPLE", "factual-qa", "en"),
    _c("What is a block explorer?", "SIMPLE", "factual-qa", "en"),
    _c("What is the photic zone?", "SIMPLE", "factual-qa", "en"),
    _c("What is myelin?", "SIMPLE", "factual-qa", "en"),
    _c("What is a setback in zoning?", "SIMPLE", "factual-qa", "en"),
    _c("What is a limiter in audio?", "SIMPLE", "factual-qa", "en"),
    _c("What is a distribution center?", "SIMPLE", "factual-qa", "en"),
    _c("What is impression share?", "SIMPLE", "factual-qa", "en"),
    _c("What is enzymatic browning?", "SIMPLE", "factual-qa", "en"),
    _c("What is primary treatment in wastewater?", "SIMPLE", "factual-qa", "en"),
    _c("What is a feed-in tariff?", "SIMPLE", "factual-qa", "en"),
    _c("What is a raft in 3D printing?", "SIMPLE", "factual-qa", "en"),
    _c("What is return-to-home in drones?", "SIMPLE", "factual-qa", "en"),
    _c("What is a mempool?", "SIMPLE", "factual-qa", "en"),
    _c("What is the benthic zone?", "SIMPLE", "factual-qa", "en"),
    _c("What is serotonin?", "SIMPLE", "factual-qa", "en"),
    _c("What is a zoning variance?", "SIMPLE", "factual-qa", "en"),
    _c("What is a soundboard?", "SIMPLE", "factual-qa", "en"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM (~180)
# ═══════════════════════════════════════════════════════════

MEDIUM_B10: list[dict] = [
    # ── Code review (weak category) ──
    _c("Review this solar panel monitoring script for error handling and edge cases", "MEDIUM", "code-review", "en"),
    _c("Check this G-code parser for buffer overflow and malformed input handling", "MEDIUM", "code-review", "en"),
    _c("Review this drone flight path validation logic for safety violations", "MEDIUM", "code-review", "en"),
    _c("Is this mining pool payout calculation correct? Check for rounding errors", "MEDIUM", "code-review", "en"),
    _c("Review this ocean sensor data ingestion pipeline for memory leaks", "MEDIUM", "code-review", "en"),
    _c("Check this EEG preprocessing code for artifact removal correctness", "MEDIUM", "code-review", "en"),
    _c("Review this urban traffic simulation module for race conditions", "MEDIUM", "code-review", "en"),
    _c("Is this podcast audio normalization logic correct? Check LUFS handling", "MEDIUM", "code-review", "en"),
    _c("Review this warehouse routing algorithm for edge cases", "MEDIUM", "code-review", "en"),
    _c("Check this social media engagement metric calculation for division-by-zero", "MEDIUM", "code-review", "en"),
    _c("Review this food shelf-life prediction model for data leakage", "MEDIUM", "code-review", "en"),
    _c("Is this wastewater BOD calculation correct? Review units and formulas", "MEDIUM", "code-review", "en"),

    # ── Debugging (weak category) ──
    _c("Our wind turbine SCADA data shows intermittent gaps. How do I trace the cause?", "MEDIUM", "debugging", "en"),
    _c("The 3D printer firmware hangs on large G-code files. How do I profile it?", "MEDIUM", "debugging", "en"),
    _c("Drone telemetry drops packets during high-speed maneuvers. Where do I start?", "MEDIUM", "debugging", "en"),
    _c("Mining pool payouts are off by 0.1%. How do I debug the rounding logic?", "MEDIUM", "debugging", "en"),
    _c("Ocean buoy sensors return NaN for temperature at depth. What could cause it?", "MEDIUM", "debugging", "en"),
    _c("fMRI preprocessing pipeline fails on some subjects. How do I isolate the bad data?", "MEDIUM", "debugging", "en"),
    _c("Urban traffic model produces unrealistic congestion. How do I validate the parameters?", "MEDIUM", "debugging", "en"),
    _c("Podcast export has clicks between segments. How do I fix the crossfade?", "MEDIUM", "debugging", "en"),
    _c("E-commerce order routing assigns wrong warehouse 5% of the time. How do I trace it?", "MEDIUM", "debugging", "en"),
    _c("Social media sentiment API returns inconsistent labels. How do I debug?", "MEDIUM", "debugging", "en"),
    _c("Food quality sensor calibration drifts after a week. How do I detect and correct?", "MEDIUM", "debugging", "en"),
    _c("Wastewater treatment model overpredicts BOD. What should I check first?", "MEDIUM", "debugging", "en"),

    # ── Summary (weak category) ──
    _c("Summarize the key differences between FDM, SLA, and SLS 3D printing", "MEDIUM", "summary", "en"),
    _c("TL;DR this renewable energy policy document for a stakeholder meeting", "MEDIUM", "summary", "en"),
    _c("Summarize the FAA Part 107 drone regulations in 3 bullet points", "MEDIUM", "summary", "en"),
    _c("Summarize the proof-of-work vs proof-of-stake debate", "MEDIUM", "summary", "en"),
    _c("Summarize the main causes of ocean acidification", "MEDIUM", "summary", "en"),
    _c("Summarize the key findings of this neuroscience paper on memory", "MEDIUM", "summary", "en"),
    _c("Summarize the pros and cons of transit-oriented development", "MEDIUM", "summary", "en"),
    _c("Summarize this podcast production workflow in 5 steps", "MEDIUM", "summary", "en"),
    _c("Summarize the trade-offs between centralized and distributed fulfillment", "MEDIUM", "summary", "en"),
    _c("Summarize the main social media metrics and when to use each", "MEDIUM", "summary", "en"),
    _c("Summarize HACCP principles for food safety", "MEDIUM", "summary", "en"),
    _c("Summarize the lifecycle assessment stages for environmental impact", "MEDIUM", "summary", "en"),

    # ── Testing (weak category) ──
    _c("Write unit tests for this solar irradiance calculation function", "MEDIUM", "testing", "en"),
    _c("Create integration tests for the 3D printer G-code parser", "MEDIUM", "testing", "en"),
    _c("Write tests for this drone geofence boundary check", "MEDIUM", "testing", "en"),
    _c("Design test cases for this mining difficulty adjustment algorithm", "MEDIUM", "testing", "en"),
    _c("Write property-based tests for this ocean depth interpolation function", "MEDIUM", "testing", "en"),
    _c("Create test scenarios for this urban traffic light optimization module", "MEDIUM", "testing", "en"),
    _c("Write regression tests for this podcast loudness normalization", "MEDIUM", "testing", "en"),
    _c("Design load tests for the order fulfillment API", "MEDIUM", "testing", "en"),
    _c("Write tests for this social media engagement rate calculator", "MEDIUM", "testing", "en"),
    _c("Create test cases for this food spoilage prediction model", "MEDIUM", "testing", "en"),
    _c("Write chaos tests for the wastewater monitoring system", "MEDIUM", "testing", "en"),

    # ── Brainstorming (weak category) ──
    _c("Brainstorm 5 ways to reduce solar panel soiling losses", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for making 3D printing more sustainable", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm approaches to extend drone battery life", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for making cryptocurrency mining more energy-efficient", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm methods to reduce plastic in ocean research", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for improving fMRI signal-to-noise ratio", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm ways to reduce urban heat island effect", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for automating podcast editing workflows", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm approaches to optimize last-mile delivery costs", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for detecting fake engagement on social media", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm ways to extend food shelf life without preservatives", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for reducing wastewater treatment energy consumption", "MEDIUM", "brainstorming", "en"),

    # ── Single-task code ──
    _c("Write a Python script to calculate solar panel output from irradiance and temperature", "MEDIUM", "simple-code", "en"),
    _c("Create a function to validate G-code commands for a 3D printer", "MEDIUM", "simple-code", "en"),
    _c("Write a script to parse drone flight log and extract altitude violations", "MEDIUM", "simple-code", "en"),
    _c("Implement a function to estimate mining profitability from hashrate and power cost", "MEDIUM", "simple-code", "en"),
    _c("Write a Python script to interpolate ocean temperature from sensor data", "MEDIUM", "simple-code", "en"),
    _c("Create a function to detect spikes in EEG data", "MEDIUM", "simple-code", "en"),
    _c("Write a script to compute walkability score from street network data", "MEDIUM", "simple-code", "en"),
    _c("Implement a function to normalize podcast audio to -16 LUFS", "MEDIUM", "simple-code", "en"),
    _c("Write a Python script to assign orders to nearest warehouse by distance", "MEDIUM", "simple-code", "en"),
    _c("Create a function to compute engagement rate from likes, comments, shares", "MEDIUM", "simple-code", "en"),
    _c("Write a script to estimate food shelf life from temperature history", "MEDIUM", "simple-code", "en"),
    _c("Implement a function to calculate BOD from dissolved oxygen readings", "MEDIUM", "simple-code", "en"),

    # ── Explanations ──
    _c("Explain how net metering works for rooftop solar", "MEDIUM", "explanation", "en"),
    _c("How does layer adhesion affect 3D print strength?", "MEDIUM", "explanation", "en"),
    _c("Explain how a drone flight controller stabilizes attitude", "MEDIUM", "explanation", "en"),
    _c("How does proof of work prevent double-spending?", "MEDIUM", "explanation", "en"),
    _c("Explain how upwelling affects ocean productivity", "MEDIUM", "explanation", "en"),
    _c("How does long-term potentiation relate to learning?", "MEDIUM", "explanation", "en"),
    _c("Explain how mixed-use zoning reduces car dependency", "MEDIUM", "explanation", "en"),
    _c("How does compression affect podcast audio quality?", "MEDIUM", "explanation", "en"),
    _c("Explain the bullwhip effect in e-commerce logistics", "MEDIUM", "explanation", "en"),
    _c("How does the algorithm affect social media reach?", "MEDIUM", "explanation", "en"),
    _c("Explain how the Maillard reaction creates flavor", "MEDIUM", "explanation", "en"),
    _c("How does activated sludge remove organic matter?", "MEDIUM", "explanation", "en"),

    # ── Comparisons ──
    _c("Compare solar PV vs wind for residential energy", "MEDIUM", "comparison", "en"),
    _c("FDM vs SLA: when to use which for prototyping?", "MEDIUM", "comparison", "en"),
    _c("Compare fixed-wing vs multirotor drones for surveying", "MEDIUM", "comparison", "en"),
    _c("ASIC vs GPU mining: pros and cons", "MEDIUM", "comparison", "en"),
    _c("Compare AUV vs ROV for ocean exploration", "MEDIUM", "comparison", "en"),
    _c("fMRI vs EEG for brain imaging: trade-offs", "MEDIUM", "comparison", "en"),
    _c("Compare TOD vs sprawl for housing affordability", "MEDIUM", "comparison", "en"),
    _c("Dynamic vs condenser mic for podcasting", "MEDIUM", "comparison", "en"),
    _c("Compare 3PL vs in-house fulfillment", "MEDIUM", "comparison", "en"),
    _c("Reach vs impressions: when does each matter?", "MEDIUM", "comparison", "en"),
    _c("Pasteurization vs sterilization for food safety", "MEDIUM", "comparison", "en"),
    _c("Compare aerobic vs anaerobic wastewater treatment", "MEDIUM", "comparison", "en"),

    # ── Rewrite ──
    _c("Rewrite this renewable energy policy for a general audience", "MEDIUM", "rewrite", "en"),
    _c("Refactor this G-code generator to support multiple printer types", "MEDIUM", "rewrite", "en"),
    _c("Rewrite this drone manual section for non-pilots", "MEDIUM", "rewrite", "en"),
    _c("Simplify this mining pool contract for investors", "MEDIUM", "rewrite", "en"),

    # ── Non-English MEDIUM ──
    _c("审查这个光伏监控脚本的错误处理和边界情况", "MEDIUM", "code-review", "zh"),
    _c("风力涡轮机 SCADA 数据有间歇性缺口，如何追踪原因？", "MEDIUM", "debugging", "zh"),
    _c("总结 FDM、SLA 和 SLS 3D 打印的主要区别", "MEDIUM", "summary", "zh"),
    _c("为这个太阳辐照度计算函数写单元测试", "MEDIUM", "testing", "zh"),
    _c("Brainstorm 5 种减少太阳能板积灰损失的方法", "MEDIUM", "brainstorming", "zh"),
    _c("写一个 Python 脚本根据辐照度和温度计算光伏板输出", "MEDIUM", "simple-code", "zh"),
    _c("解释净计量如何为屋顶太阳能工作", "MEDIUM", "explanation", "zh"),
    _c("比较住宅用太阳能光伏和风能", "MEDIUM", "comparison", "zh"),

    _c("この太陽光パネル監視スクリプトのエラー処理をレビューしてください", "MEDIUM", "code-review", "ja"),
    _c("風力タービンのSCADAデータに断続的な欠損があります。原因を追跡するには？", "MEDIUM", "debugging", "ja"),
    _c("FDM、SLA、SLS 3Dプリントの主な違いを要約してください", "MEDIUM", "summary", "ja"),
    _c("太陽光発電の出力計算関数のユニットテストを書いてください", "MEDIUM", "testing", "ja"),
    _c("太陽光パネルの汚れ損失を減らす5つの方法をブレインストームしてください", "MEDIUM", "brainstorming", "ja"),
    _c("日照量と温度から太陽光パネル出力を計算するPythonスクリプトを書いてください", "MEDIUM", "simple-code", "ja"),
    _c("屋上太陽光のネットメータリングの仕組みを説明してください", "MEDIUM", "explanation", "ja"),
    _c("住宅用エネルギーで太陽光PVと風力の比較をしてください", "MEDIUM", "comparison", "ja"),

    _c("이 태양광 패널 모니터링 스크립트의 에러 처리를 검토해주세요", "MEDIUM", "code-review", "ko"),
    _c("풍력 터빈 SCADA 데이터에 간헐적 공백이 있습니다. 원인을 어떻게 추적하나요?", "MEDIUM", "debugging", "ko"),
    _c("FDM, SLA, SLS 3D 프린팅의 주요 차이점을 요약해주세요", "MEDIUM", "summary", "ko"),
    _c("태양 복사량 계산 함수의 유닛 테스트를 작성해주세요", "MEDIUM", "testing", "ko"),
    _c("태양광 패널 오염 손실을 줄이는 5가지 방법을 브레인스토밍해주세요", "MEDIUM", "brainstorming", "ko"),
    _c("복사량과 온도로 태양광 패널 출력을 계산하는 Python 스크립트를 작성해주세요", "MEDIUM", "simple-code", "ko"),
    _c("지붕 태양광의 순계량이 어떻게 작동하는지 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("주거용 에너지로 태양광 PV와 풍력 비교해주세요", "MEDIUM", "comparison", "ko"),

    _c("راجع معالجة الأخطاء في سكربت مراقبة الألواح الشمسية", "MEDIUM", "code-review", "ar"),
    _c("بيانات SCADA لتوربينات الرياح بها فجوات متقطعة. كيف أتتبع السبب؟", "MEDIUM", "debugging", "ar"),
    _c("لخص الفروقات الرئيسية بين FDM و SLA و SLS في الطباعة ثلاثية الأبعاد", "MEDIUM", "summary", "ar"),
    _c("اشرح كيف يعمل القياس الصافي للطاقة الشمسية على الأسطح", "MEDIUM", "explanation", "ar"),

    _c("Проверь обработку ошибок в скрипте мониторинга солнечных панелей", "MEDIUM", "code-review", "ru"),
    _c("Данные SCADA ветряков показывают пробелы. Как найти причину?", "MEDIUM", "debugging", "ru"),
    _c("Сравни солнечную PV и ветер для жилой энергетики", "MEDIUM", "comparison", "ru"),

    _c("Revisa el manejo de errores de este script de monitoreo solar", "MEDIUM", "code-review", "es"),
    _c("Los datos SCADA del aerogenerador tienen huecos. ¿Cómo rastreo la causa?", "MEDIUM", "debugging", "es"),
    _c("Compara solar PV vs eólica para energía residencial", "MEDIUM", "comparison", "es"),

    _c("Überprüfe die Fehlerbehandlung dieses Solar-Monitoring-Skripts", "MEDIUM", "code-review", "de"),
    _c("Die Windturbinen-SCADA-Daten haben Lücken. Wie finde ich die Ursache?", "MEDIUM", "debugging", "de"),
    _c("Vergleiche Solar-PV und Wind für Wohnenergie", "MEDIUM", "comparison", "de"),

    _c("Revue la gestion d'erreurs de ce script de surveillance solaire", "MEDIUM", "code-review", "fr"),
    _c("Les données SCADA des éoliennes ont des lacunes. Comment tracer la cause?", "MEDIUM", "debugging", "fr"),
    _c("Compare le solaire PV et l'éolien pour l'énergie résidentielle", "MEDIUM", "comparison", "fr"),

    _c("Revise o tratamento de erros deste script de monitoramento solar", "MEDIUM", "code-review", "pt"),
    _c("Os dados SCADA da turbina eólica têm lacunas. Como rastrear a causa?", "MEDIUM", "debugging", "pt"),
    _c("Compare solar PV e eólica para energia residencial", "MEDIUM", "comparison", "pt"),

    _c("इस सोलर पैनल मॉनिटरिंग स्क्रिप्ट की एरर हैंडलिंग की समीक्षा करें", "MEDIUM", "code-review", "hi"),
    _c("पवन टरबाइन SCADA डेटा में अंतराल है। कारण कैसे ट्रैस करें?", "MEDIUM", "debugging", "hi"),

    _c("Bu güneş paneli izleme betiğinin hata işlemesini inceleyin", "MEDIUM", "code-review", "tr"),
    _c("Rüzgar türbini SCADA verilerinde boşluklar var. Nedeni nasıl izlerim?", "MEDIUM", "debugging", "tr"),

    _c("Xem xét xử lý lỗi của script giám sát tấm pin mặt trời này", "MEDIUM", "code-review", "vi"),
    _c("Dữ liệu SCADA tuabin gió có khoảng trống. Làm sao truy vết nguyên nhân?", "MEDIUM", "debugging", "vi"),

    _c("Przejrzyj obsługę błędów w tym skrypcie monitorowania paneli słonecznych", "MEDIUM", "code-review", "pl"),
    _c("Dane SCADA turbin wiatrowych mają luki. Jak śledzić przyczynę?", "MEDIUM", "debugging", "pl"),

    # ── Adversarial: short-but-MEDIUM ──
    _c("Explain the thermocline", "MEDIUM", "explanation", "en"),
    _c("Describe the Maillard reaction", "MEDIUM", "explanation", "en"),
    _c("Walk me through proof of work", "MEDIUM", "explanation", "en"),

    # ── More MEDIUM to reach ~180 ──
    _c("Review this renewable energy ROI calculator for edge cases", "MEDIUM", "code-review", "en"),
    _c("Our 3D print quality degrades over time. How do I diagnose?", "MEDIUM", "debugging", "en"),
    _c("Summarize the key urban planning principles from this textbook chapter", "MEDIUM", "summary", "en"),
    _c("Write property-based tests for this engagement rate formula", "MEDIUM", "testing", "en"),
    _c("Brainstorm ways to reduce last-mile delivery emissions", "MEDIUM", "brainstorming", "en"),
    _c("Write a Python script to validate drone flight coordinates against airspace", "MEDIUM", "simple-code", "en"),
    _c("Explain how ocean currents affect climate", "MEDIUM", "explanation", "en"),
    _c("Compare dopamine vs serotonin in reward processing", "MEDIUM", "comparison", "en"),
    _c("Review this food safety checklist for completeness", "MEDIUM", "code-review", "en"),
    _c("The wastewater pH sensor drifts. How do I calibrate?", "MEDIUM", "debugging", "en"),
    _c("Summarize the podcast production best practices", "MEDIUM", "summary", "en"),
    _c("Write integration tests for the warehouse routing API", "MEDIUM", "testing", "en"),
    _c("Brainstorm features for a social media analytics dashboard", "MEDIUM", "brainstorming", "en"),
    _c("Implement a function to estimate 3D print time from G-code", "MEDIUM", "simple-code", "en"),
    _c("Explain how zoning affects housing supply", "MEDIUM", "explanation", "en"),
    _c("Compare BOD vs COD for wastewater quality", "MEDIUM", "comparison", "en"),

    # ── More MEDIUM to reach ~180 ──
    _c("Write a script to estimate solar panel degradation from production data", "MEDIUM", "simple-code", "en"),
    _c("Review this drone flight log parser for timezone handling", "MEDIUM", "code-review", "en"),
    _c("Summarize the key differences between PoW and PoS consensus", "MEDIUM", "summary", "en"),
    _c("Write unit tests for this ocean depth interpolation function", "MEDIUM", "testing", "en"),
    _c("Brainstorm ways to reduce urban heat island effect in downtown", "MEDIUM", "brainstorming", "en"),
    _c("Implement a function to compute podcast episode duration from audio file", "MEDIUM", "simple-code", "en"),
    _c("Our order routing picks the wrong warehouse 3% of the time. How do I debug?", "MEDIUM", "debugging", "en"),
    _c("Explain how virality coefficient predicts content spread", "MEDIUM", "explanation", "en"),
    _c("Compare natural vs artificial food preservatives", "MEDIUM", "comparison", "en"),
    _c("Review this BOD calculation for unit consistency", "MEDIUM", "code-review", "en"),
    _c("Summarize the lifecycle of a lithium-ion battery in renewable storage", "MEDIUM", "summary", "en"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX (~100)
# ═══════════════════════════════════════════════════════════

COMPLEX_B10: list[dict] = [
    # ── Renewable energy multi-requirement ──
    _c("Design a renewable energy management platform with solar/wind forecasting, grid integration, battery scheduling, demand response, and carbon reporting.", "COMPLEX", "system-design", "en"),
    _c("Build a smart grid system with real-time load balancing, distributed generation coordination, fault detection, and consumer dashboards.", "COMPLEX", "system-design", "en"),
    _c("Design a virtual power plant with aggregation, bidding, dispatch, settlement, and regulatory compliance.", "COMPLEX", "system-design", "en"),

    # ── 3D printing multi-requirement ──
    _c("Design a 3D printing farm management system with queue scheduling, material tracking, machine monitoring, quality control, and job costing.", "COMPLEX", "system-design", "en"),
    _c("Build a print preparation pipeline with mesh repair, support generation, slicing optimization, and multi-machine allocation.", "COMPLEX", "system-design", "en"),
    _c("Design an additive manufacturing platform with design validation, material selection, process parameters, and post-processing workflows.", "COMPLEX", "system-design", "en"),

    # ── Drone technology multi-requirement ──
    _c("Design a drone fleet management system with mission planning, BVLOS compliance, real-time tracking, maintenance scheduling, and incident reporting.", "COMPLEX", "system-design", "en"),
    _c("Build an autonomous drone delivery platform with route optimization, geofencing, payload handling, and customer notification.", "COMPLEX", "system-design", "en"),
    _c("Design a drone inspection pipeline with flight planning, image capture, defect detection, and report generation.", "COMPLEX", "system-design", "en"),

    # ── Cryptocurrency mining multi-requirement ──
    _c("Design a mining pool platform with hashrate aggregation, reward distribution, payout automation, and pool-hopping prevention.", "COMPLEX", "system-design", "en"),
    _c("Build a mining farm management system with power monitoring, cooling control, profitability tracking, and alerting.", "COMPLEX", "system-design", "en"),
    _c("Design a multi-algorithm mining switcher with profitability calculation, pool selection, and failover.", "COMPLEX", "system-design", "en"),

    # ── Ocean science multi-requirement ──
    _c("Design an ocean monitoring platform with sensor networks, data ingestion, quality control, visualization, and alerting.", "COMPLEX", "system-design", "en"),
    _c("Build an AUV mission planning system with bathymetry, obstacle avoidance, energy management, and recovery protocols.", "COMPLEX", "system-design", "en"),
    _c("Design a marine data pipeline with satellite imagery, in-situ sensors, model assimilation, and forecast products.", "COMPLEX", "ml-pipeline", "en"),

    # ── Neuroscience multi-requirement ──
    _c("Design an fMRI analysis pipeline with preprocessing, registration, statistical modeling, and visualization.", "COMPLEX", "ml-pipeline", "en"),
    _c("Build a brain-computer interface platform with signal acquisition, feature extraction, classification, and feedback.", "COMPLEX", "system-design", "en"),
    _c("Design a neuroimaging data management system with DICOM ingestion, anonymization, sharing, and compliance.", "COMPLEX", "system-design", "en"),

    # ── Urban planning multi-requirement ──
    _c("Design an urban planning decision support system with GIS integration, scenario modeling, stakeholder input, and impact assessment.", "COMPLEX", "system-design", "en"),
    _c("Build a traffic simulation platform with demand modeling, signal optimization, emissions estimation, and visualization.", "COMPLEX", "system-design", "en"),
    _c("Design a land use allocation system with zoning constraints, suitability analysis, and multi-objective optimization.", "COMPLEX", "architecture", "en"),

    # ── Podcast production multi-requirement ──
    _c("Design a podcast production platform with recording, editing, mixing, distribution, and analytics.", "COMPLEX", "system-design", "en"),
    _c("Build an automated podcast pipeline with transcription, chapter detection, show notes generation, and RSS publishing.", "COMPLEX", "ml-pipeline", "en"),
    _c("Design a collaborative podcast workflow with version control, review, approval, and multi-format export.", "COMPLEX", "system-design", "en"),

    # ── E-commerce logistics multi-requirement ──
    _c("Design an e-commerce fulfillment platform with order routing, inventory allocation, carrier selection, tracking, and returns.", "COMPLEX", "system-design", "en"),
    _c("Build a warehouse optimization system with slotting, pick path optimization, labor scheduling, and KPIs.", "COMPLEX", "system-design", "en"),
    _c("Design a last-mile delivery platform with route optimization, time windows, proof of delivery, and customer communication.", "COMPLEX", "system-design", "en"),

    # ── Social media analytics multi-requirement ──
    _c("Design a social media analytics platform with data ingestion, sentiment analysis, influencer identification, and reporting.", "COMPLEX", "system-design", "en"),
    _c("Build a viral content prediction system with feature extraction, model training, A/B testing, and deployment.", "COMPLEX", "ml-pipeline", "en"),
    _c("Design a brand monitoring system with multi-platform aggregation, alerting, competitive analysis, and dashboards.", "COMPLEX", "system-design", "en"),

    # ── Food science multi-requirement ──
    _c("Design a food safety management system with HACCP tracking, supplier audits, recall management, and regulatory reporting.", "COMPLEX", "system-design", "en"),
    _c("Build a shelf-life prediction pipeline with sensor data, model training, uncertainty quantification, and alerts.", "COMPLEX", "ml-pipeline", "en"),
    _c("Design a food traceability platform with blockchain, batch tracking, and recall automation.", "COMPLEX", "system-design", "en"),

    # ── Environmental engineering multi-requirement ──
    _c("Design a wastewater treatment monitoring system with sensor networks, process control, compliance reporting, and optimization.", "COMPLEX", "system-design", "en"),
    _c("Build an environmental impact assessment platform with LCA, carbon accounting, and reporting.", "COMPLEX", "system-design", "en"),
    _c("Design a stormwater management system with real-time monitoring, flood prediction, and control actuation.", "COMPLEX", "system-design", "en"),

    # ── Security / migration / performance ──
    _c("Perform a security audit of a renewable energy SCADA system. Address access control, encryption, and integrity.", "COMPLEX", "security-analysis", "en"),
    _c("Plan a migration from monolithic warehouse software to microservices with zero downtime.", "COMPLEX", "migration", "en"),
    _c("Optimize the ocean data pipeline: reduce processing time from 4 hours to 30 minutes.", "COMPLEX", "performance", "en"),

    # ── Non-English COMPLEX ──
    _c("设计一个可再生能源管理平台，包括太阳能/风能预测、电网集成、电池调度、需求响应和碳报告", "COMPLEX", "system-design", "zh"),
    _c("设计一个无人机机队管理系统，包括任务规划、BVLOS 合规、实时追踪、维护调度和事件报告", "COMPLEX", "system-design", "zh"),
    _c("设计一个电商履约平台，包括订单路由、库存分配、承运商选择、追踪和退货", "COMPLEX", "system-design", "zh"),
    _c("设计一个海洋监测平台，包括传感器网络、数据摄取、质量控制、可视化和告警", "COMPLEX", "system-design", "zh"),
    _c("设计一个食品安全管理系统，包括 HACCP 追踪、供应商审计、召回管理和监管报告", "COMPLEX", "system-design", "zh"),

    _c("再生可能エネルギー管理プラットフォームを設計してください。太陽/風力予測、グリッド統合、バッテリースケジューリング、需要応答、カーボンレポートを含めてください。", "COMPLEX", "system-design", "ja"),
    _c("ドローン艦隊管理システムを設計してください。ミッション計画、BVLOS準拠、リアルタイム追跡、メンテナンススケジュールを含めてください。", "COMPLEX", "system-design", "ja"),
    _c("Eコマース履行プラットフォームを設計してください。注文ルーティング、在庫割り当て、キャリア選択、追跡、返品を含めてください。", "COMPLEX", "system-design", "ja"),

    _c("재생에너지 관리 플랫폼을 설계하세요. 태양/풍력 예측, 그리드 통합, 배터리 스케줄링, 수요 반응, 탄소 보고를 포함해야 합니다.", "COMPLEX", "system-design", "ko"),
    _c("드론 함대 관리 시스템을 설계하세요. 미션 계획, BVLOS 준수, 실시간 추적, 유지보수 스케줄링을 포함해야 합니다.", "COMPLEX", "system-design", "ko"),
    _c("이커머스 이행 플랫폼을 설계하세요. 주문 라우팅, 재고 할당, 운송업체 선택, 추적, 반품을 포함해야 합니다.", "COMPLEX", "system-design", "ko"),

    _c("صمم منصة إدارة الطاقة المتجددة مع التنبؤ بالطاقة الشمسية/الرياح والتكامل مع الشبكة وجدولة البطاريات واستجابة الطلب والتقارير الكربونية.", "COMPLEX", "system-design", "ar"),
    _c("صمم نظام إدارة أسطول الطائرات بدون طيار مع تخطيط المهام والامتثال لـ BVLOS والتتبع في الوقت الفعلي.", "COMPLEX", "system-design", "ar"),

    _c("Спроектируй платформу управления возобновляемой энергией с прогнозом солнца/ветра, интеграцией в сеть, расписанием батарей и отчётами по углероду.", "COMPLEX", "system-design", "ru"),
    _c("Спроектируй систему управления парком дронов с планированием миссий, BVLOS, отслеживанием и отчётами.", "COMPLEX", "system-design", "ru"),

    _c("Diseña una plataforma de gestión de energía renovable con predicción solar/eólica, integración de red, programación de baterías y reportes de carbono.", "COMPLEX", "system-design", "es"),
    _c("Diseña un sistema de gestión de flota de drones con planificación de misiones, cumplimiento BVLOS y seguimiento en tiempo real.", "COMPLEX", "system-design", "es"),

    _c("Entwerfe eine Plattform für erneuerbare Energien mit Solar-/Windprognose, Netzintegration, Batterieplanung und Kohlenstoffberichterstattung.", "COMPLEX", "system-design", "de"),
    _c("Entwerfe ein Drohnenflotten-Managementsystem mit Missionsplanung, BVLOS-Compliance und Echtzeit-Tracking.", "COMPLEX", "system-design", "de"),

    _c("Conçois une plateforme de gestion des énergies renouvelables avec prévision solaire/éolienne, intégration réseau, planification batteries et rapports carbone.", "COMPLEX", "system-design", "fr"),
    _c("Conçois un système de gestion de flotte de drones avec planification de missions, conformité BVLOS et suivi en temps réel.", "COMPLEX", "system-design", "fr"),

    _c("Projete uma plataforma de gestão de energia renovável com previsão solar/eólica, integração de rede, agendamento de baterias e relatórios de carbono.", "COMPLEX", "system-design", "pt"),
    _c("Projete um sistema de gestão de frota de drones com planejamento de missões, conformidade BVLOS e rastreamento em tempo real.", "COMPLEX", "system-design", "pt"),

    _c("नवीकरणीय ऊर्जा प्रबंधन प्लेटफॉर्म डिज़ाइन करें जिसमें सौर/पवन पूर्वानुमान, ग्रिड एकीकरण, बैटरी शेड्यूलिंग और कार्बन रिपोर्टिंग शामिल हो।", "COMPLEX", "system-design", "hi"),

    _c("Güneş/rüzgar tahmini, şebeke entegrasyonu, pil planlaması ve karbon raporlaması içeren yenilenebilir enerji yönetim platformu tasarlayın.", "COMPLEX", "system-design", "tr"),

    _c("Thiết kế nền tảng quản lý năng lượng tái tạo với dự báo mặt trời/gió, tích hợp lưới điện, lập lịch pin và báo cáo carbon.", "COMPLEX", "system-design", "vi"),

    _c("Zaprojektuj platformę zarządzania energią odnawialną z prognozą słoneczną/wiatrową, integracją sieci, planowaniem baterii i raportowaniem emisji CO2.", "COMPLEX", "system-design", "pl"),

    # ── More COMPLEX to reach ~100 ──
    _c("Design a 3D printing quality assurance pipeline with defect detection, dimensional verification, and traceability.", "COMPLEX", "ml-pipeline", "en"),
    _c("Build a mining profitability dashboard with real-time hashrate, power cost, and multi-coin comparison.", "COMPLEX", "system-design", "en"),
    _c("Design a neuroimaging data sharing platform with consent management, anonymization, and access control.", "COMPLEX", "architecture", "en"),
    _c("Plan a migration from legacy warehouse WMS to cloud-native with data sync and validation.", "COMPLEX", "migration", "en"),
    _c("Design a podcast analytics platform with listen-through tracking, demographic inference, and ad attribution.", "COMPLEX", "system-design", "en"),
    _c("Build a food recall automation system with batch tracing, notification, and regulatory filing.", "COMPLEX", "system-design", "en"),
    _c("Design a wastewater treatment optimization system with real-time control and predictive maintenance.", "COMPLEX", "system-design", "en"),
    _c("Implement a drone collision avoidance system with sensor fusion, path replanning, and fail-safe.", "COMPLEX", "complex-code", "en"),
    _c("Design a social media crisis detection system with anomaly detection, sentiment shift, and escalation.", "COMPLEX", "ml-pipeline", "en"),
    _c("Build a renewable energy certificate tracking system with issuance, trading, and retirement.", "COMPLEX", "system-design", "en"),
    _c("Design a multi-tenant 3D printing service with queue management, billing, and SLA tracking.", "COMPLEX", "architecture", "en"),
    _c("Perform a security audit of a mining pool payout system. Address double-spend and front-running.", "COMPLEX", "security-analysis", "en"),

    # ── More COMPLEX to reach ~100 ──
    _c("Design a renewable energy certificate marketplace with issuance, verification, trading, and retirement tracking.", "COMPLEX", "system-design", "en"),
    _c("Build a 3D print farm scheduling system with machine availability, material constraints, priority queues, and SLA tracking.", "COMPLEX", "system-design", "en"),
    _c("Design a drone airspace management platform with real-time traffic, conflict detection, deconfliction, and regulatory compliance.", "COMPLEX", "system-design", "en"),
    _c("Build a mining profitability dashboard with multi-coin support, power cost modeling, and real-time alerts.", "COMPLEX", "system-design", "en"),
    _c("Design an ocean sensor calibration pipeline with drift detection, cross-validation, and quality flags.", "COMPLEX", "ml-pipeline", "en"),
    _c("Build a neuroimaging data sharing platform with de-identification, consent management, and access control.", "COMPLEX", "architecture", "en"),
    _c("Design an urban mobility platform with transit data, bike-share, ride-hail integration, and multimodal routing.", "COMPLEX", "system-design", "en"),
    _c("Build a podcast monetization platform with dynamic ad insertion, listener segmentation, and revenue attribution.", "COMPLEX", "system-design", "en"),
    _c("Design a same-day delivery optimization system with demand forecasting, driver assignment, and route optimization.", "COMPLEX", "system-design", "en"),
    _c("Build a social media crisis detection system with anomaly detection, sentiment analysis, and escalation workflows.", "COMPLEX", "ml-pipeline", "en"),
    _c("Design a food recall traceability system with batch tracking, supplier mapping, and notification automation.", "COMPLEX", "system-design", "en"),
    _c("Build a wastewater treatment control system with real-time sensors, predictive control, and compliance reporting.", "COMPLEX", "system-design", "en"),

    # ── More COMPLEX to reach ~100 ──
    _c("Design a hybrid renewable microgrid with solar, wind, battery, and diesel backup, including load shedding and islanding.", "COMPLEX", "system-design", "en"),
    _c("Build a multi-material 3D printing workflow with material switching, purge towers, and quality verification.", "COMPLEX", "system-design", "en"),
    _c("Design a drone delivery network with hub locations, route optimization, battery swap stations, and weather routing.", "COMPLEX", "system-design", "en"),
    _c("Implement a mining pool stratum protocol with job distribution, share validation, and difficulty adjustment.", "COMPLEX", "complex-code", "en"),
    _c("Design a marine mammal detection pipeline with hydrophone data, ML classification, and real-time alerting.", "COMPLEX", "ml-pipeline", "en"),
    _c("Build a brain atlas registration pipeline with multi-modal MRI, normalization, and region extraction.", "COMPLEX", "ml-pipeline", "en"),
    _c("Design a participatory urban planning platform with citizen input, visualization, and impact simulation.", "COMPLEX", "system-design", "en"),
    _c("Build a podcast analytics pipeline with transcription, speaker diarization, topic extraction, and engagement metrics.", "COMPLEX", "ml-pipeline", "en"),
    _c("Design a cross-border e-commerce fulfillment network with customs, duties, and multi-carrier routing.", "COMPLEX", "system-design", "en"),
    _c("Implement a real-time social media trend detection system with streaming processing and anomaly alerts.", "COMPLEX", "complex-code", "en"),
]


# ═══════════════════════════════════════════════════════════
#  REASONING (~80)
# ═══════════════════════════════════════════════════════════

REASONING_B10: list[dict] = [
    # ── Formal proofs ──
    _c("Prove that the greedy algorithm for the fractional knapsack problem is optimal.", "REASONING", "algorithm-proof", "en"),
    _c("Prove that a tree with n nodes has exactly n-1 edges using induction.", "REASONING", "formal-proof", "en"),
    _c("Prove that the set of regular languages is closed under concatenation.", "REASONING", "formal-proof", "en"),
    _c("Prove that every connected graph has a spanning tree.", "REASONING", "formal-proof", "en"),
    _c("Prove that the greedy activity selection algorithm yields an optimal solution.", "REASONING", "algorithm-proof", "en"),
    _c("Prove that the sum of degrees of all vertices in a graph equals twice the number of edges.", "REASONING", "formal-proof", "en"),
    _c("Prove that a directed acyclic graph has a topological ordering.", "REASONING", "formal-proof", "en"),
    _c("Prove that the greedy Huffman algorithm produces an optimal prefix code.", "REASONING", "algorithm-proof", "en"),
    _c("Prove that the set of context-free languages is closed under union.", "REASONING", "formal-proof", "en"),
    _c("Prove that every finite automaton has an equivalent minimal DFA.", "REASONING", "formal-proof", "en"),

    # ── Math derivations ──
    _c("Derive the closed-form solution for the recurrence T(n) = T(n-1) + n.", "REASONING", "math-derivation", "en"),
    _c("Derive the expected number of comparisons in linear search for a uniform distribution.", "REASONING", "math-derivation", "en"),
    _c("Derive the optimal substructure for the longest common subsequence problem.", "REASONING", "math-derivation", "en"),
    _c("Derive the recurrence for the number of binary search trees with n nodes.", "REASONING", "math-derivation", "en"),
    _c("Derive the amortized cost of a dynamic array with doubling using the accounting method.", "REASONING", "math-derivation", "en"),
    _c("Derive the formula for the number of ways to make change for n cents with coins {1,5,10}.", "REASONING", "math-derivation", "en"),
    _c("Derive the optimal policy for a simple two-state MDP using value iteration.", "REASONING", "math-derivation", "en"),
    _c("Derive the probability of a full house in poker.", "REASONING", "math-derivation", "en"),

    # ── Game theory ──
    _c("Find the Nash equilibrium in the battle of the sexes game. Prove it exists.", "REASONING", "game-theory", "en"),
    _c("Prove that in a symmetric two-player game, a symmetric Nash equilibrium exists.", "REASONING", "game-theory", "en"),
    _c("Analyze the subgame-perfect equilibrium in a two-stage sequential game.", "REASONING", "game-theory", "en"),
    _c("Derive the mixed-strategy Nash equilibrium for rock-paper-scissors.", "REASONING", "game-theory", "en"),
    _c("Prove that the minimax theorem holds for finite two-player zero-sum games.", "REASONING", "game-theory", "en"),

    # ── Logic puzzles ──
    _c("Prove that in the hat puzzle with n people, the optimal strategy guarantees n-1 correct guesses.", "REASONING", "logic-puzzle", "en"),
    _c("Prove that the two-envelope paradox is resolved when considering the proper prior.", "REASONING", "logic-puzzle", "en"),
    _c("Prove that the liar paradox (this statement is false) has no consistent truth value.", "REASONING", "formal-logic", "en"),
    _c("Prove that (A implies B) and (B implies C) implies (A implies C) using natural deduction.", "REASONING", "formal-logic", "en"),
    _c("Prove that the satisfiability of 3-SAT is NP-complete via reduction from SAT.", "REASONING", "formal-logic", "en"),

    # ── Non-English REASONING ──
    _c("证明分数背包问题的贪心算法是最优的", "REASONING", "algorithm-proof", "zh"),
    _c("证明 n 个节点的树恰好有 n-1 条边（用归纳法）", "REASONING", "formal-proof", "zh"),
    _c("推导 T(n)=T(n-1)+n 的闭式解", "REASONING", "math-derivation", "zh"),
    _c("求性别之战博弈的纳什均衡并证明其存在", "REASONING", "game-theory", "zh"),
    _c("证明 (A→B)∧(B→C) 蕴含 (A→C)", "REASONING", "formal-logic", "zh"),

    _c("分数ナップサック問題の貪欲アルゴリズムが最適であることを証明してください", "REASONING", "algorithm-proof", "ja"),
    _c("n頂点の木がちょうどn-1本の辺を持つことを帰納法で証明してください", "REASONING", "formal-proof", "ja"),
    _c("T(n)=T(n-1)+nの閉形式を導出してください", "REASONING", "math-derivation", "ja"),
    _c("性別の戦いゲームのナッシュ均衡を求め、存在することを証明してください", "REASONING", "game-theory", "ja"),

    _c("분수 배낭 문제의 탐욕 알고리즘이 최적임을 증명하세요", "REASONING", "algorithm-proof", "ko"),
    _c("n개 노드의 트리가 정확히 n-1개의 간선을 가짐을 귀납법으로 증명하세요", "REASONING", "formal-proof", "ko"),
    _c("T(n)=T(n-1)+n의 닫힌 형태를 유도하세요", "REASONING", "math-derivation", "ko"),
    _c("성의 전쟁 게임의 내시 균형을 구하고 존재함을 증명하세요", "REASONING", "game-theory", "ko"),

    _c("أثبت أن الخوارزمية الجشعة لمشكلة حقيبة الظهر الكسرية مثالية.", "REASONING", "algorithm-proof", "ar"),
    _c("أثبت أن الشجرة ذات n عقد لها بالضبط n-1 حافة باستخدام الاستقراء.", "REASONING", "formal-proof", "ar"),

    _c("Докажи, что жадный алгоритм для дробной задачи о рюкзаке оптимален.", "REASONING", "algorithm-proof", "ru"),
    _c("Докажи по индукции, что дерево с n вершинами имеет ровно n-1 рёбер.", "REASONING", "formal-proof", "ru"),

    _c("Demuestra que el algoritmo voraz para la mochila fraccionaria es óptimo.", "REASONING", "algorithm-proof", "es"),
    _c("Demuestra por inducción que un árbol con n nodos tiene exactamente n-1 aristas.", "REASONING", "formal-proof", "es"),

    _c("Beweise, dass der Greedy-Algorithmus für das fraktionale Rucksackproblem optimal ist.", "REASONING", "algorithm-proof", "de"),
    _c("Beweise per Induktion, dass ein Baum mit n Knoten genau n-1 Kanten hat.", "REASONING", "formal-proof", "de"),

    _c("Démontre que l'algorithme glouton pour le sac à dos fractionnaire est optimal.", "REASONING", "algorithm-proof", "fr"),
    _c("Démontre par récurrence qu'un arbre à n nœuds a exactement n-1 arêtes.", "REASONING", "formal-proof", "fr"),

    _c("Prove que o algoritmo guloso para a mochila fracionária é ótimo.", "REASONING", "algorithm-proof", "pt"),
    _c("Prove por indução que uma árvore com n nós tem exatamente n-1 arestas.", "REASONING", "formal-proof", "pt"),

    _c("भिन्नात्मक नैपसैक समस्या के लालची एल्गोरिथ्म की इष्टतमता सिद्ध करें।", "REASONING", "algorithm-proof", "hi"),

    _c("Kesirli sırt çantası problemi için açgözlü algoritmanın optimal olduğunu kanıtlayın.", "REASONING", "algorithm-proof", "tr"),

    _c("Chứng minh thuật toán tham lam cho bài toán ba lô phân số là tối ưu.", "REASONING", "algorithm-proof", "vi"),

    _c("Udowodnij, że zachłanny algorytm dla ułamkowego problemu plecakowego jest optymalny.", "REASONING", "algorithm-proof", "pl"),

    # ── More REASONING to reach ~80 ──
    _c("Prove that the greedy set cover algorithm has approximation ratio H(n).", "REASONING", "algorithm-proof", "en"),
    _c("Prove that the greedy interval scheduling algorithm is optimal.", "REASONING", "algorithm-proof", "en"),
    _c("Derive the optimal stopping rule for the secretary problem.", "REASONING", "math-derivation", "en"),
    _c("Prove that in a repeated prisoner's dilemma, tit-for-tat is a Nash equilibrium.", "REASONING", "game-theory", "en"),
    _c("Prove that (P and Q) implies P is a tautology.", "REASONING", "formal-logic", "en"),
    _c("Prove that the greedy algorithm for set cover is not optimal. Give a counterexample.", "REASONING", "algorithm-proof", "en"),
    _c("Derive the expected value of a binomial random variable B(n,p).", "REASONING", "math-derivation", "en"),
    _c("Prove that a graph is Eulerian if and only if every vertex has even degree.", "REASONING", "formal-proof", "en"),
    _c("Prove that the greedy coin-changing algorithm is optimal for US denominations.", "REASONING", "algorithm-proof", "en"),
    _c("Prove that the set of decidable languages is closed under complement.", "REASONING", "formal-proof", "en"),

    # ── More REASONING to reach ~80 ──
    _c("Prove that the greedy algorithm for the coin change problem is optimal for denominations {1, 5, 10, 25}.", "REASONING", "algorithm-proof", "en"),
    _c("Derive the expected number of trials until first success for a geometric distribution.", "REASONING", "math-derivation", "en"),
    _c("Prove that in a zero-sum game, the value of the game is unique.", "REASONING", "game-theory", "en"),
    _c("Prove that (P or Q) and (not P) implies Q using natural deduction.", "REASONING", "formal-logic", "en"),
    _c("Prove that the greedy algorithm for the activity selection problem is optimal.", "REASONING", "algorithm-proof", "en"),
    _c("Derive the variance of a binomial random variable B(n, p).", "REASONING", "math-derivation", "en"),
    _c("Prove that every connected graph with n vertices and n-1 edges is a tree.", "REASONING", "formal-proof", "en"),
    _c("Prove that the set of context-free languages is not closed under intersection.", "REASONING", "formal-proof", "en"),
    _c("In the repeated prisoner's dilemma, prove that always defect is a Nash equilibrium.", "REASONING", "game-theory", "en"),
    _c("Prove that the resolution rule preserves satisfiability.", "REASONING", "formal-logic", "en"),
    _c("Derive the optimal k for k-nearest neighbors when the true decision boundary is known.", "REASONING", "math-derivation", "en"),
    _c("Prove that a graph has an Eulerian circuit if and only if every vertex has even degree and the graph is connected.", "REASONING", "formal-proof", "en"),

    # ── More REASONING to reach ~80 ──
    _c("Prove that the greedy algorithm for the maximum spanning tree is optimal.", "REASONING", "algorithm-proof", "en"),
]


ALL_B10 = SIMPLE_B10 + MEDIUM_B10 + COMPLEX_B10 + REASONING_B10


def export(path=None):
    from pathlib import Path
    import json
    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b10.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B10:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter
    tiers = Counter(c["expected_tier"] for c in ALL_B10)
    langs = Counter(c["lang"] for c in ALL_B10)
    print(f"Batch 10: {len(ALL_B10)} cases")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")


if __name__ == "__main__":
    import sys
    export(sys.argv[1] if len(sys.argv) > 1 else None)

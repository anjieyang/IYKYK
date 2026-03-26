"""Hand-crafted batch 9 — ~500 unique cases for LLM router classifier.

Strategy:
- NEW domains: cybersecurity, DevOps automation, embedded systems, fintech, EdTech,
  healthcare AI, autonomous vehicles, AR/VR, NLP, computer vision, quantum computing,
  sustainability tech
- MORE weak categories: code-review, debugging, summary, testing, brainstorming
- Adversarial: prompts that look like one tier but are another
- 14+ languages, English ~40%
- Zero overlap with batches 1–8
"""

from __future__ import annotations


def _c(prompt: str, tier: str, cat: str, lang: str) -> dict:
    return {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}


# ═══════════════════════════════════════════════════════════
#  SIMPLE (~140)
# ═══════════════════════════════════════════════════════════

SIMPLE_B9: list[dict] = [
    # ── Cybersecurity factual ──
    _c("What is a zero-day vulnerability?", "SIMPLE", "factual-qa", "en"),
    _c("What does SIEM stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is a honeypot?", "SIMPLE", "factual-qa", "en"),
    _c("What is phishing?", "SIMPLE", "factual-qa", "en"),
    _c("What is a DDoS attack?", "SIMPLE", "factual-qa", "en"),
    _c("What does SOC stand for in security?", "SIMPLE", "factual-qa", "en"),
    _c("What is a man-in-the-middle attack?", "SIMPLE", "factual-qa", "en"),
    _c("What is OWASP?", "SIMPLE", "factual-qa", "en"),
    _c("What is a penetration test?", "SIMPLE", "factual-qa", "en"),
    _c("What is RBAC?", "SIMPLE", "factual-qa", "en"),
    # ── DevOps / embedded / fintech factual ──
    _c("What is Ansible?", "SIMPLE", "factual-qa", "en"),
    _c("What is a CAN bus?", "SIMPLE", "factual-qa", "en"),
    _c("What is PCI-DSS?", "SIMPLE", "factual-qa", "en"),
    _c("What is an RTOS?", "SIMPLE", "factual-qa", "en"),
    _c("What is SWIFT in banking?", "SIMPLE", "factual-qa", "en"),
    _c("What is a Jenkins pipeline?", "SIMPLE", "factual-qa", "en"),
    _c("What is an SoC?", "SIMPLE", "factual-qa", "en"),
    _c("What is AML in fintech?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between SPI and I2C?", "SIMPLE", "factual-qa", "en"),
    _c("What is a CI/CD pipeline?", "SIMPLE", "factual-qa", "en"),
    # ── EdTech / healthcare / AV / AR-VR factual ──
    _c("What is a learning management system?", "SIMPLE", "factual-qa", "en"),
    _c("What is HIPAA?", "SIMPLE", "factual-qa", "en"),
    _c("What is lidar?", "SIMPLE", "factual-qa", "en"),
    _c("What is SLAM?", "SIMPLE", "factual-qa", "en"),
    _c("What is a head-mounted display?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between AR and VR?", "SIMPLE", "factual-qa", "en"),
    _c("What is FHIR?", "SIMPLE", "factual-qa", "en"),
    _c("What is the SAE autonomy level?", "SIMPLE", "factual-qa", "en"),
    _c("What is SCORM?", "SIMPLE", "factual-qa", "en"),
    _c("What is a digital twin in healthcare?", "SIMPLE", "factual-qa", "en"),
    # ── NLP / CV / quantum / sustainability factual ──
    _c("What is a token embedding?", "SIMPLE", "factual-qa", "en"),
    _c("What is semantic segmentation?", "SIMPLE", "factual-qa", "en"),
    _c("What is a qubit?", "SIMPLE", "factual-qa", "en"),
    _c("What is quantum entanglement?", "SIMPLE", "factual-qa", "en"),
    _c("What is carbon footprint in tech?", "SIMPLE", "factual-qa", "en"),
    _c("What is green computing?", "SIMPLE", "factual-qa", "en"),
    _c("What is a BERT model?", "SIMPLE", "factual-qa", "en"),
    _c("What is object detection?", "SIMPLE", "factual-qa", "en"),
    _c("What is a quantum gate?", "SIMPLE", "factual-qa", "en"),
    _c("What is PUE in data centers?", "SIMPLE", "factual-qa", "en"),
    # ── Definitions ──
    _c("Define buffer overflow", "SIMPLE", "definition", "en"),
    _c("What is a race condition?", "SIMPLE", "definition", "en"),
    _c("What is a deadlock?", "SIMPLE", "definition", "en"),
    _c("What is a Bloom filter?", "SIMPLE", "definition", "en"),
    _c("What is attention in neural networks?", "SIMPLE", "definition", "en"),
    _c("What is a bounding box?", "SIMPLE", "definition", "en"),
    _c("What is a hash collision?", "SIMPLE", "definition", "en"),
    _c("What is a watchdog timer?", "SIMPLE", "definition", "en"),
    # ── Translations / greetings ──
    _c("Translate 'machine learning' to Arabic", "SIMPLE", "translation", "en"),
    _c("How do you say 'cybersecurity' in Russian?", "SIMPLE", "translation", "en"),
    _c("Translate 'autonomous vehicle' to Japanese", "SIMPLE", "translation", "en"),
    _c("How do you say 'hello' in Hindi?", "SIMPLE", "translation", "en"),
    _c("Hey", "SIMPLE", "greeting", "en"),
    _c("Hi there", "SIMPLE", "greeting", "en"),
    _c("Good morning", "SIMPLE", "greeting", "en"),
    _c("Bye", "SIMPLE", "greeting", "en"),
    # ── Chinese ──
    _c("什么是零日漏洞？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是蜜罐？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 CAN 总线？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 RTOS？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 FHIR？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 SLAM？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是量子比特？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是语义分割？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是缓冲区溢出？", "SIMPLE", "definition", "zh"),
    _c("什么是死锁？", "SIMPLE", "definition", "zh"),
    _c("你好", "SIMPLE", "greeting", "zh"),
    # ── Japanese ──
    _c("ゼロデイ脆弱性とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("ハニーポットとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("CANバスとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("RTOSとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("SLAMとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("量子ビットとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("デッドロックとは何ですか？", "SIMPLE", "definition", "ja"),
    _c("こんにちは", "SIMPLE", "greeting", "ja"),
    # ── Korean ──
    _c("제로데이 취약점이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("허니팟이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("CAN 버스란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("RTOS란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("SLAM이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("양자 비트란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("데드락이란 무엇인가요?", "SIMPLE", "definition", "ko"),
    _c("안녕하세요", "SIMPLE", "greeting", "ko"),
    # ── Arabic ──
    _c("ما هو ثغرة الصفر يوم؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو وعاء العسل؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو PCI-DSS؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو RTOS؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو SLAM؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو البت الكمي؟", "SIMPLE", "factual-qa", "ar"),
    _c("مرحبا", "SIMPLE", "greeting", "ar"),
    # ── Russian ──
    _c("Что такое уязвимость нулевого дня?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое honeypot?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое CAN-шина?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое RTOS?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое SLAM?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое кубит?", "SIMPLE", "factual-qa", "ru"),
    _c("Привет", "SIMPLE", "greeting", "ru"),
    # ── Spanish ──
    _c("¿Qué es una vulnerabilidad de día cero?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un honeypot?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un bus CAN?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un RTOS?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es SLAM?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un qubit?", "SIMPLE", "factual-qa", "es"),
    _c("Hola", "SIMPLE", "greeting", "es"),
    # ── German ──
    _c("Was ist eine Zero-Day-Schwachstelle?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein Honeypot?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein CAN-Bus?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein RTOS?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist SLAM?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein Qubit?", "SIMPLE", "factual-qa", "de"),
    _c("Hallo", "SIMPLE", "greeting", "de"),
    # ── French ──
    _c("Qu'est-ce qu'une vulnérabilité zero-day ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un honeypot ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un bus CAN ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un RTOS ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce que SLAM ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un qubit ?", "SIMPLE", "factual-qa", "fr"),
    _c("Bonjour", "SIMPLE", "greeting", "fr"),
    # ── Portuguese ──
    _c("O que é uma vulnerabilidade zero-day?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um honeypot?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um barramento CAN?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um RTOS?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é SLAM?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um qubit?", "SIMPLE", "factual-qa", "pt"),
    _c("Olá", "SIMPLE", "greeting", "pt"),
    # ── Hindi ──
    _c("जीरो डे वल्नरेबिलिटी क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("हनीपॉट क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("CAN बस क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("RTOS क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("SLAM क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("क्विबिट क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("नमस्ते", "SIMPLE", "greeting", "hi"),
    # ── Turkish ──
    _c("Sıfır gün açığı nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Bal kutusu nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("CAN verisi nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("RTOS nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("SLAM nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Kübit nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Merhaba", "SIMPLE", "greeting", "tr"),
    # ── Vietnamese ──
    _c("Lỗ hổng zero-day là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Honeypot là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Bus CAN là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("RTOS là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("SLAM là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Qubit là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Xin chào", "SIMPLE", "greeting", "vi"),
    # ── Polish ──
    _c("Co to jest luka zero-day?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest honeypot?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest magistrala CAN?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest RTOS?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest SLAM?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest kubit?", "SIMPLE", "factual-qa", "pl"),
    _c("Cześć", "SIMPLE", "greeting", "pl"),
    # ── Adversarial: technical words but still SIMPLE ──
    _c("What is a zero-trust architecture?", "SIMPLE", "factual-qa", "en"),
    _c("What is differential privacy?", "SIMPLE", "factual-qa", "en"),
    _c("What is homomorphic encryption?", "SIMPLE", "factual-qa", "en"),
    _c("What is the CAP theorem?", "SIMPLE", "factual-qa", "en"),
    _c("What is the Byzantine fault tolerance?", "SIMPLE", "factual-qa", "en"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM (~180)
# ═══════════════════════════════════════════════════════════

MEDIUM_B9: list[dict] = [
    # ── Code review (weak category) ──
    _c("Review this authentication middleware for security flaws and suggest fixes", "MEDIUM", "code-review", "en"),
    _c("Is this SQL prepared statement usage correct? Check for injection risks", "MEDIUM", "code-review", "en"),
    _c("Review this Ansible playbook for idempotency and error handling", "MEDIUM", "code-review", "en"),
    _c("Check this embedded C code for memory leaks and buffer overflows", "MEDIUM", "code-review", "en"),
    _c("Review this payment processing logic for PCI compliance issues", "MEDIUM", "code-review", "en"),
    _c("Is this HIPAA-compliant? Review the PHI handling in this function", "MEDIUM", "code-review", "en"),
    _c("Review this AR/VR rendering loop for performance bottlenecks", "MEDIUM", "code-review", "en"),
    _c("Check this NLP tokenization code for edge cases with Unicode", "MEDIUM", "code-review", "en"),
    _c("Review this computer vision preprocessing pipeline for correctness", "MEDIUM", "code-review", "en"),
    _c("Is this quantum circuit implementation correct? Review the gate sequence", "MEDIUM", "code-review", "en"),
    _c("Review this carbon footprint calculation module for accuracy", "MEDIUM", "code-review", "en"),
    _c("Check this DevOps script for race conditions when run in parallel", "MEDIUM", "code-review", "en"),
    # ── Debugging (weak category) ──
    _c("My SIEM keeps alerting on false positives. How do I tune the rules?", "MEDIUM", "debugging", "en"),
    _c("The Ansible playbook fails on the third host with a timeout. How do I debug?", "MEDIUM", "debugging", "en"),
    _c("Our embedded device resets randomly. How do I isolate the cause?", "MEDIUM", "debugging", "en"),
    _c("The payment gateway returns 3DS failures intermittently. Where do I start?", "MEDIUM", "debugging", "en"),
    _c("The LMS course export fails for large enrollments. How do I fix it?", "MEDIUM", "debugging", "en"),
    _c(
        "Our healthcare FHIR API returns 500 on certain patient queries. How do I trace it?",
        "MEDIUM",
        "debugging",
        "en",
    ),
    _c(
        "The autonomous vehicle perception stack drops frames under load. How do I profile it?",
        "MEDIUM",
        "debugging",
        "en",
    ),
    _c(
        "VR headset tracking jitters in one corner of the play space. What could cause it?", "MEDIUM", "debugging", "en"
    ),
    _c("Our NER model mislabels medical terms. How do I debug the training data?", "MEDIUM", "debugging", "en"),
    _c("Object detection misses small objects at distance. How do I improve recall?", "MEDIUM", "debugging", "en"),
    _c("Quantum simulator gives different results on different backends. Why?", "MEDIUM", "debugging", "en"),
    _c("Our PUE monitoring shows spikes at odd hours. How do I correlate with workload?", "MEDIUM", "debugging", "en"),
    # ── Summary (weak category) ──
    _c("Summarize this CVE advisory and list the affected components", "MEDIUM", "summary", "en"),
    _c("Give a brief overview of the OWASP Top 10 for a non-technical stakeholder", "MEDIUM", "summary", "en"),
    _c("TL;DR this DevOps incident postmortem", "MEDIUM", "summary", "en"),
    _c("Summarize the key differences between AUTOSAR Classic and Adaptive", "MEDIUM", "summary", "en"),
    _c("Summarize the main risks in this fintech regulatory document", "MEDIUM", "summary", "en"),
    _c("Summarize this EdTech platform feature spec in 3 bullet points", "MEDIUM", "summary", "en"),
    _c("Summarize the FDA guidance on AI/ML in medical devices", "MEDIUM", "summary", "en"),
    _c("Summarize the SAE J3016 levels of driving automation", "MEDIUM", "summary", "en"),
    _c("Summarize the key challenges in AR/VR latency reduction", "MEDIUM", "summary", "en"),
    _c("Summarize the BERT vs GPT architecture differences", "MEDIUM", "summary", "en"),
    _c("Summarize YOLO vs R-CNN for object detection", "MEDIUM", "summary", "en"),
    _c("Summarize the main quantum error correction approaches", "MEDIUM", "summary", "en"),
    _c("Summarize the carbon impact of cloud vs on-prem data centers", "MEDIUM", "summary", "en"),
    # ── Testing (weak category) ──
    _c("Write unit tests for this authentication bypass check function", "MEDIUM", "testing", "en"),
    _c("Create integration tests for this payment refund flow", "MEDIUM", "testing", "en"),
    _c("Write fuzz tests for this parser that handles untrusted input", "MEDIUM", "testing", "en"),
    _c("Design test cases for this embedded firmware OTA update logic", "MEDIUM", "testing", "en"),
    _c("Write property-based tests for this financial rounding function", "MEDIUM", "testing", "en"),
    _c("Create load tests for this LMS video streaming endpoint", "MEDIUM", "testing", "en"),
    _c("Write tests for this FHIR resource validation logic", "MEDIUM", "testing", "en"),
    _c("Design test scenarios for this autonomous driving decision module", "MEDIUM", "testing", "en"),
    _c("Write regression tests for this NLP sentiment classifier", "MEDIUM", "testing", "en"),
    _c("Create test cases for this image augmentation pipeline", "MEDIUM", "testing", "en"),
    _c("Write tests for this quantum gate decomposition function", "MEDIUM", "testing", "en"),
    _c("Design chaos tests for this green energy scheduling service", "MEDIUM", "testing", "en"),
    # ── Brainstorming (weak category) ──
    _c(
        "Brainstorm 5 ways to reduce false positives in our intrusion detection system", "MEDIUM", "brainstorming", "en"
    ),
    _c("Ideas for automating our release process without breaking production", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm approaches to reduce power consumption in our IoT fleet", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for making our payment flow more resilient to bank outages", "MEDIUM", "brainstorming", "en"),
    _c(
        "Brainstorm features for an adaptive learning platform that personalizes content",
        "MEDIUM",
        "brainstorming",
        "en",
    ),
    _c("Ideas for improving diagnostic accuracy with AI while staying explainable", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm ways to handle edge cases in autonomous parking", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for reducing motion sickness in VR experiences", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm methods to improve low-resource language NER", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for real-time object tracking in crowded scenes", "MEDIUM", "brainstorming", "en"),
    _c("Brainstorm hybrid classical-quantum algorithms for optimization", "MEDIUM", "brainstorming", "en"),
    _c("Ideas for making our data center carbon-neutral", "MEDIUM", "brainstorming", "en"),
    # ── Single-task code ──
    _c("Write a Python script to scan a directory for files with weak file permissions", "MEDIUM", "simple-code", "en"),
    _c("Create an Ansible task to ensure a service is running and enabled on boot", "MEDIUM", "simple-code", "en"),
    _c("Write a C function to read a value from a CAN bus frame", "MEDIUM", "simple-code", "en"),
    _c("Implement a function to validate an IBAN format", "MEDIUM", "simple-code", "en"),
    _c("Write a script to export SCORM-compliant content from our LMS", "MEDIUM", "simple-code", "en"),
    _c("Create a function to anonymize PHI in a FHIR resource", "MEDIUM", "simple-code", "en"),
    _c("Write a Python script to parse lidar point cloud data", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple head pose estimator for AR applications", "MEDIUM", "simple-code", "en"),
    _c("Write a tokenizer for a custom NLP pipeline", "MEDIUM", "simple-code", "en"),
    _c("Implement a function to compute IoU between two bounding boxes", "MEDIUM", "simple-code", "en"),
    _c("Write a script to estimate carbon emissions from compute usage", "MEDIUM", "simple-code", "en"),
    # ── Explanations ──
    _c("Explain how a buffer overflow can lead to code execution", "MEDIUM", "explanation", "en"),
    _c("How does Ansible achieve idempotency in playbook execution?", "MEDIUM", "explanation", "en"),
    _c("Explain how CAN bus arbitration works when multiple nodes transmit", "MEDIUM", "explanation", "en"),
    _c("How does PCI-DSS require encryption of cardholder data at rest?", "MEDIUM", "explanation", "en"),
    _c("Explain how SCORM packages are structured and launched", "MEDIUM", "explanation", "en"),
    _c("How does FHIR support interoperability between healthcare systems?", "MEDIUM", "explanation", "en"),
    _c("Explain how lidar and camera fusion improves perception", "MEDIUM", "explanation", "en"),
    _c("How does inside-out tracking work in VR headsets?", "MEDIUM", "explanation", "en"),
    _c("Explain how BERT's masked language modeling pretraining works", "MEDIUM", "explanation", "en"),
    _c("How does non-maximum suppression work in object detection?", "MEDIUM", "explanation", "en"),
    _c("Explain how quantum superposition enables parallel computation", "MEDIUM", "explanation", "en"),
    _c("How does PUE relate to data center efficiency?", "MEDIUM", "explanation", "en"),
    # ── Comparisons ──
    _c("Compare Ansible vs Terraform for infrastructure automation", "MEDIUM", "comparison", "en"),
    _c("FreeRTOS vs Zephyr for embedded: when to use which?", "MEDIUM", "comparison", "en"),
    _c("Compare Stripe vs Adyen for fintech payment processing", "MEDIUM", "comparison", "en"),
    _c("Moodle vs Canvas for EdTech: pros and cons", "MEDIUM", "comparison", "en"),
    _c("Compare rule-based vs ML-based clinical decision support", "MEDIUM", "comparison", "en"),
    _c("Camera-only vs lidar for autonomous driving perception", "MEDIUM", "comparison", "en"),
    _c("Compare WebXR vs native SDKs for AR/VR development", "MEDIUM", "comparison", "en"),
    _c("BERT vs GPT for text classification: when to use which?", "MEDIUM", "comparison", "en"),
    _c("YOLO vs Faster R-CNN: speed vs accuracy tradeoffs", "MEDIUM", "comparison", "en"),
    _c("IBM Qiskit vs Cirq for quantum programming", "MEDIUM", "comparison", "en"),
    # ── Rewrites ──
    _c("Rewrite this shell script as an idempotent Ansible playbook", "MEDIUM", "rewrite", "en"),
    _c("Refactor this C code to be MISRA compliant", "MEDIUM", "rewrite", "en"),
    _c("Rewrite this SQL to use parameterized queries and avoid injection", "MEDIUM", "rewrite", "en"),
    _c("Refactor this FHIR client to use async/await", "MEDIUM", "rewrite", "en"),
    # ── Non-English MEDIUM ──
    _c("审查这个认证中间件的安全漏洞并给出修复建议", "MEDIUM", "code-review", "zh"),
    _c("SIEM 误报太多，如何调优规则？", "MEDIUM", "debugging", "zh"),
    _c("总结这个 CVE 公告并列出受影响组件", "MEDIUM", "summary", "zh"),
    _c("为这个认证绕过检查函数写单元测试", "MEDIUM", "testing", "zh"),
    _c("Brainstorm 5 种减少入侵检测误报的方法", "MEDIUM", "brainstorming", "zh"),
    _c("写一个 Python 脚本扫描目录中权限过弱的文件", "MEDIUM", "simple-code", "zh"),
    _c("解释缓冲区溢出如何导致代码执行", "MEDIUM", "explanation", "zh"),
    _c("比较 Ansible 和 Terraform 在基础设施自动化上的优劣", "MEDIUM", "comparison", "zh"),
    _c("この認証ミドルウェアのセキュリティ脆弱性をレビューして修正案を出してください", "MEDIUM", "code-review", "ja"),
    _c("SIEMの誤検知が多すぎます。ルールをどうチューニングしますか？", "MEDIUM", "debugging", "ja"),
    _c("このCVEアドバイザリを要約して影響コンポーネントをリストしてください", "MEDIUM", "summary", "ja"),
    _c("この認証バイパスチェック関数のユニットテストを書いてください", "MEDIUM", "testing", "ja"),
    _c("侵入検知の誤検知を減らす5つの方法をブレインストームしてください", "MEDIUM", "brainstorming", "ja"),
    _c("AnsibleとTerraformのインフラ自動化を比較してください", "MEDIUM", "comparison", "ja"),
    _c("이 인증 미들웨어의 보안 취약점을 검토하고 수정 제안해주세요", "MEDIUM", "code-review", "ko"),
    _c("SIEM 오탐이 너무 많습니다. 규칙을 어떻게 조정하나요?", "MEDIUM", "debugging", "ko"),
    _c("이 CVE 공지를 요약하고 영향받는 컴포넌트를 나열해주세요", "MEDIUM", "summary", "ko"),
    _c("Ansible과 Terraform의 인프라 자동화 비교해주세요", "MEDIUM", "comparison", "ko"),
    _c("راجع ثغرات أمان هذا الوسيط واقترح إصلاحات", "MEDIUM", "code-review", "ar"),
    _c("SIEM يعطي إنذارات خاطئة كثيرة. كيف أضبط القواعد؟", "MEDIUM", "debugging", "ar"),
    _c("لخص هذا الإعلان CVE واذكر المكونات المتأثرة", "MEDIUM", "summary", "ar"),
    _c("Проверь этот middleware аутентификации на уязвимости и предложи исправления", "MEDIUM", "code-review", "ru"),
    _c("SIEM выдаёт много ложных срабатываний. Как настроить правила?", "MEDIUM", "debugging", "ru"),
    _c("Сравни Ansible и Terraform для автоматизации инфраструктуры", "MEDIUM", "comparison", "ru"),
    _c("Revisa este middleware de autenticación en busca de fallos de seguridad", "MEDIUM", "code-review", "es"),
    _c("El SIEM genera muchos falsos positivos. ¿Cómo afino las reglas?", "MEDIUM", "debugging", "es"),
    _c("Compara Ansible vs Terraform para automatización de infraestructura", "MEDIUM", "comparison", "es"),
    _c("Überprüfe diese Auth-Middleware auf Sicherheitslücken", "MEDIUM", "code-review", "de"),
    _c("Der SIEM liefert zu viele False Positives. Wie tune ich die Regeln?", "MEDIUM", "debugging", "de"),
    _c("Vergleiche Ansible und Terraform für Infrastruktur-Automatisierung", "MEDIUM", "comparison", "de"),
    _c("Revue ce middleware d'authentification pour des failles de sécurité", "MEDIUM", "code-review", "fr"),
    _c("Le SIEM génère trop de faux positifs. Comment affiner les règles?", "MEDIUM", "debugging", "fr"),
    _c("Compare Ansible et Terraform pour l'automatisation d'infrastructure", "MEDIUM", "comparison", "fr"),
    _c("Revise este middleware de autenticação em busca de falhas de segurança", "MEDIUM", "code-review", "pt"),
    _c("O SIEM gera muitos falsos positivos. Como ajustar as regras?", "MEDIUM", "debugging", "pt"),
    _c("Compare Ansible e Terraform para automação de infraestrutura", "MEDIUM", "comparison", "pt"),
    _c("इस ऑथेंटिकेशन मिडलवेयर की सुरक्षा समीक्षा करें", "MEDIUM", "code-review", "hi"),
    _c("SIEM में बहुत ज्यादा false positive आ रहे हैं। नियम कैसे ट्यून करें?", "MEDIUM", "debugging", "hi"),
    _c("Bu kimlik doğrulama middleware'ini güvenlik açıkları için inceleyin", "MEDIUM", "code-review", "tr"),
    _c("SIEM çok fazla yanlış pozitif veriyor. Kuralları nasıl ayarlarım?", "MEDIUM", "debugging", "tr"),
    _c("Xem xét middleware xác thực này để tìm lỗ hổng bảo mật", "MEDIUM", "code-review", "vi"),
    _c("SIEM báo quá nhiều false positive. Làm sao điều chỉnh quy tắc?", "MEDIUM", "debugging", "vi"),
    _c("Przejrzyj ten middleware uwierzytelniania pod kątem luk bezpieczeństwa", "MEDIUM", "code-review", "pl"),
    _c("SIEM generuje za dużo fałszywych alarmów. Jak dostroić reguły?", "MEDIUM", "debugging", "pl"),
    # ── Adversarial: LOOKS simple (short) but IS MEDIUM ──
    _c("Explain the Bellman equation", "MEDIUM", "explanation", "en"),
    _c("Describe the Viterbi algorithm", "MEDIUM", "explanation", "en"),
    _c("Walk me through HMAC", "MEDIUM", "explanation", "en"),
    # ── More MEDIUM to reach ~180 ──
    _c("Review this rate limiter implementation for thundering herd issues", "MEDIUM", "code-review", "en"),
    _c("Our CAN bus logger drops messages under load. How do I profile and fix it?", "MEDIUM", "debugging", "en"),
    _c("Summarize the GDPR requirements for AI systems in 3 bullet points", "MEDIUM", "summary", "en"),
    _c("Write contract tests for this payment API using Pact", "MEDIUM", "testing", "en"),
    _c("Brainstorm ways to reduce cold start latency in our serverless functions", "MEDIUM", "brainstorming", "en"),
    _c("Write a Python script to validate JWT tokens and check expiration", "MEDIUM", "simple-code", "en"),
    _c("Explain how certificate pinning prevents MITM attacks", "MEDIUM", "explanation", "en"),
    _c("Compare OAuth2 vs SAML for enterprise SSO", "MEDIUM", "comparison", "en"),
    _c("Review this RBAC policy for privilege escalation risks", "MEDIUM", "code-review", "en"),
    _c("The Ansible run hangs on 'Gathering Facts'. How do I debug?", "MEDIUM", "debugging", "en"),
    _c("Summarize the NIST cybersecurity framework core functions", "MEDIUM", "summary", "en"),
    _c("Write mutation tests for this password hashing module", "MEDIUM", "testing", "en"),
    _c("Brainstorm approaches to detect insider threats from access logs", "MEDIUM", "brainstorming", "en"),
    _c("Implement a circuit breaker pattern in Python", "MEDIUM", "simple-code", "en"),
    _c("Explain how SPI mode affects communication in embedded systems", "MEDIUM", "explanation", "en"),
    _c("Compare PCIe Gen4 vs Gen5 for storage workloads", "MEDIUM", "comparison", "en"),
    _c("Review this Kafka consumer for exactly-once semantics", "MEDIUM", "code-review", "en"),
    _c("Our FHIR server times out on bulk export. How do I optimize?", "MEDIUM", "debugging", "en"),
    _c("Summarize the ISO 26262 safety levels for automotive", "MEDIUM", "summary", "en"),
    _c("Write chaos tests for our message queue", "MEDIUM", "testing", "en"),
    _c("Brainstorm features for a developer onboarding platform", "MEDIUM", "brainstorming", "en"),
    _c("Create a script to generate SBOM from a Docker image", "MEDIUM", "simple-code", "en"),
    _c("Explain how attention mechanisms reduce long-range dependency issues", "MEDIUM", "explanation", "en"),
    _c("Compare ResNet vs EfficientNet for mobile deployment", "MEDIUM", "comparison", "en"),
    _c("Review this Helm chart for security best practices", "MEDIUM", "code-review", "en"),
    _c("The VR app crashes when switching scenes. How do I debug?", "MEDIUM", "debugging", "en"),
    _c("Summarize the key differences between ISO 27001 and SOC 2", "MEDIUM", "summary", "en"),
    _c("Write property-based tests for this date parsing function", "MEDIUM", "testing", "en"),
    _c("Brainstorm ways to improve model interpretability for clinicians", "MEDIUM", "brainstorming", "en"),
    _c("Implement a retry with exponential backoff in Go", "MEDIUM", "simple-code", "en"),
    _c("Explain how Kalman filters fuse sensor data", "MEDIUM", "explanation", "en"),
    _c("Compare gRPC vs REST for microservice communication", "MEDIUM", "comparison", "en"),
    _c("Review this Prometheus alert rule for false positive rate", "MEDIUM", "code-review", "en"),
    _c("Our quantum circuit simulation runs out of memory. How do I optimize?", "MEDIUM", "debugging", "en"),
    _c("Summarize the carbon offset vs reduction strategies for tech", "MEDIUM", "summary", "en"),
    _c("Write load tests for our GraphQL API using k6", "MEDIUM", "testing", "en"),
    _c("Brainstorm ways to make our API more resilient to third-party outages", "MEDIUM", "brainstorming", "en"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX (~100)
# ═══════════════════════════════════════════════════════════

COMPLEX_B9: list[dict] = [
    # ── Cybersecurity multi-requirement ──
    _c(
        "Design a security operations center platform with SIEM integration, threat hunting workflows, incident response playbooks, and compliance reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a zero-trust network access system with device posture checks, continuous authentication, micro-segmentation, and audit logging.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a vulnerability management pipeline with asset discovery, scanning, prioritization by risk, patch orchestration, and executive dashboards.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── DevOps automation multi-requirement ──
    _c(
        "Design a GitOps platform with multi-cluster sync, drift detection, rollback automation, secret management, and approval workflows.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build an infrastructure provisioning system with Terraform state locking, cost estimation, policy-as-code validation, and change approval gates.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a CI/CD pipeline for microservices with parallel builds, artifact signing, environment promotion, canary deployment, and rollback.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Embedded systems multi-requirement ──
    _c(
        "Design an automotive ECU software architecture with AUTOSAR stack, OTA updates, diagnostic services, and safety monitoring.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a fleet management system for industrial IoT with device provisioning, remote diagnostics, firmware OTA, and predictive maintenance.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a real-time control system for a drone with sensor fusion, path planning, fail-safe modes, and telemetry streaming.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Fintech multi-requirement ──
    _c(
        "Design a payment orchestration platform with multi-gateway routing, 3DS handling, reconciliation, dispute management, and PCI compliance.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build an AML transaction monitoring system with rule engine, ML anomaly detection, case management, and regulatory reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a core banking API with account management, transaction processing, audit trails, and regulatory compliance.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── EdTech multi-requirement ──
    _c(
        "Design an adaptive learning platform with content recommendation, progress tracking, assessment engine, and instructor dashboards.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a proctoring system with face detection, screen monitoring, behavior analysis, and integrity reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design an LMS with SCORM support, video streaming, discussion forums, gradebook, and mobile app sync.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Healthcare AI multi-requirement ──
    _c(
        "Design a clinical decision support system with FHIR integration, evidence-based rules, explainability, and audit trails for FDA compliance.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a medical imaging pipeline with DICOM ingestion, AI inference, radiologist workflow, and HIPAA-compliant storage.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a patient engagement platform with appointment scheduling, telehealth, medication reminders, and interoperability.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Autonomous vehicles multi-requirement ──
    _c(
        "Design a perception stack with lidar, camera, radar fusion, object tracking, and redundancy for L4 autonomy.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a simulation platform for AV testing with scenario generation, physics engine, sensor simulation, and regression testing.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a V2X communication system with DSRC, message prioritization, security, and integration with the driving stack.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── AR/VR multi-requirement ──
    _c(
        "Design a multiplayer VR platform with spatial audio, avatar sync, physics, and low-latency networking.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build an AR content management system with 3D asset streaming, occlusion handling, and analytics.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a mixed reality training simulator with hand tracking, object interaction, and performance assessment.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── NLP multi-requirement ──
    _c(
        "Design an enterprise search system with document ingestion, embedding, retrieval, reranking, and answer extraction.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a multilingual NER pipeline with model serving, entity linking, and confidence calibration.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a conversational AI platform with intent detection, slot filling, backend integration, and fallback handling.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Computer vision multi-requirement ──
    _c(
        "Design a video analytics pipeline with object detection, tracking, re-identification, and alert generation.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a defect inspection system with image capture, model inference, classification, and reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a facial recognition system with liveness detection, enrollment, matching, and privacy controls.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Quantum / sustainability multi-requirement ──
    _c(
        "Design a quantum algorithm development platform with circuit design, simulation, backend submission, and result analysis.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a carbon accounting system for cloud workloads with usage tracking, emission factors, and reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a green data center management system with workload scheduling, renewable forecasting, and PUE optimization.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Security / architecture ──
    _c(
        "Design a secure software supply chain with SBOM generation, vulnerability scanning, signing, and policy enforcement.",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    _c(
        "Plan a migration from monolithic to microservices with API versioning, feature flags, and gradual traffic shift.",
        "COMPLEX",
        "migration",
        "en",
    ),
    _c(
        "Design a multi-tenant SaaS platform with isolation, billing, and compliance per tenant.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    # ── Non-English COMPLEX ──
    _c(
        "设计一个安全运营中心平台，包括 SIEM 集成、威胁狩猎工作流、事件响应手册和合规报告",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c("设计一个零信任网络接入系统，包括设备态势检查、持续认证、微隔离和审计日志", "COMPLEX", "system-design", "zh"),
    _c("设计一个自动驾驶感知栈，包括激光雷达、相机、雷达融合、目标跟踪和 L4 冗余", "COMPLEX", "system-design", "zh"),
    _c(
        "设计一个医疗影像流水线，包括 DICOM 摄取、AI 推理、放射科工作流和 HIPAA 合规存储",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c("设计一个量子算法开发平台，包括电路设计、仿真、后端提交和结果分析", "COMPLEX", "system-design", "zh"),
    _c(
        "セキュリティオペレーションセンターを設計してください。SIEM連携、脅威ハンティング、インシデント対応、コンプライアンスレポートを含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "ゼロトラストネットワークアクセスシステムを設計してください。デバイスポスチャーチェック、継続認証、マイクロセグメンテーションを含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "自律走行の知覚スタックを設計してください。LiDAR、カメラ、レーダー融合、オブジェクト追跡、L4冗長性を含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "보안 운영 센터 플랫폼을 설계하세요. SIEM 연동, 위협 헌팅, 사고 대응 플레이북, 규정 준수 보고를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "자율주행 인지 스택을 설계하세요. LiDAR, 카메라, 레이더 융합, 객체 추적, L4 중복을 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "صمم منصة مركز عمليات أمنية تشمل تكامل SIEM وصيد التهديدات ودفاتر استجابة الحوادث والتقارير الامتثال.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "صمم نظام وصول شبكة صفر ثقة مع فحص حالة الجهاز والتحقق المستمر والجزء الدقيق وتسجيل التدقيق.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "Спроектируй платформу SOC с интеграцией SIEM, охотой за угрозами, плейбуками реагирования и отчётами по соответствию.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Спроектируй стек восприятия для автономного вождения с лидаром, камерами, радаром, трекингом и резервированием.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Diseña una plataforma SOC con integración SIEM, caza de amenazas, playbooks de respuesta e informes de cumplimiento.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Diseña un stack de percepción para conducción autónoma con fusión lidar-cámara-radar, seguimiento y redundancia.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Entwerfe eine SOC-Plattform mit SIEM-Integration, Threat Hunting, Incident Response Playbooks und Compliance-Berichten.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Entwerfe einen Wahrnehmungsstack für autonomes Fahren mit Lidar-Kamera-Radar-Fusion, Tracking und Redundanz.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Conçois une plateforme SOC avec intégration SIEM, chasse aux menaces, playbooks de réponse et rapports de conformité.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    _c(
        "Conçois un stack de perception pour véhicule autonome avec fusion lidar-caméra-radar, suivi et redondance.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    _c(
        "Projete uma plataforma SOC com integração SIEM, caça a ameaças, playbooks de resposta e relatórios de conformidade.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "Projete um stack de percepção para veículo autônomo com fusão lidar-câmera-radar, rastreamento e redundância.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "एक SOC प्लेटफॉर्म डिज़ाइन करें जिसमें SIEM इंटीग्रेशन, थ्रेट हंटिंग, इंसिडेंट रिस्पॉन्स प्लेबुक और कंप्लायंस रिपोर्टिंग शामिल हो।",
        "COMPLEX",
        "system-design",
        "hi",
    ),
    _c(
        "SIEM entegrasyonu, tehdit avı, olay müdahale playbook'ları ve uyumluluk raporlaması içeren bir SOC platformu tasarlayın.",
        "COMPLEX",
        "system-design",
        "tr",
    ),
    _c(
        "Thiết kế nền tảng SOC với tích hợp SIEM, săn mối đe dọa, playbook phản hồi sự cố và báo cáo tuân thủ.",
        "COMPLEX",
        "system-design",
        "vi",
    ),
    _c(
        "Zaprojektuj platformę SOC z integracją SIEM, polowaniem na zagrożenia, playbookami reagowania i raportami zgodności.",
        "COMPLEX",
        "system-design",
        "pl",
    ),
    # ── More COMPLEX to reach ~100 ──
    _c(
        "Design a DevSecOps pipeline with SAST, DAST, dependency scanning, container signing, and deployment gates.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a real-time fraud detection system with rule engine, ML scoring, case management, and regulatory reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a telemedicine platform with video calls, EHR integration, prescription workflow, and HIPAA compliance.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a simulation environment for AV validation with scenario injection, sensor noise, and metrics collection.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a spatial computing platform with 6DoF tracking, hand gestures, shared anchors, and persistence.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a document intelligence pipeline with OCR, entity extraction, classification, and workflow routing.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a video surveillance system with edge inference, cloud aggregation, search, and retention policies.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a quantum chemistry simulation platform with circuit compilation, backend selection, and result visualization.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a sustainable cloud platform with carbon-aware scheduling, renewable matching, and reporting.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a multi-region active-active system with conflict resolution, eventual consistency, and failover.",
        "COMPLEX",
        "architecture",
        "en",
    ),
    _c(
        "Plan a migration from VMs to Kubernetes with zero downtime and rollback capability.",
        "COMPLEX",
        "migration",
        "en",
    ),
    _c(
        "Design a secrets management system with rotation, audit, and least-privilege access.",
        "COMPLEX",
        "security-analysis",
        "en",
    ),
    _c(
        "Build an industrial control system with PLC integration, SCADA, historian, and security monitoring.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a regulatory reporting platform for fintech with data lineage, validation, and audit.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a competency-based learning platform with skill graphs, assessments, and credentialing.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a clinical trial management system with patient recruitment, consent, and data collection.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a V2V communication system with message signing, prioritization, and geofencing.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a holographic display pipeline with light field rendering and eye tracking.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a multilingual customer support system with translation, sentiment, and escalation.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a defect detection system with multi-camera sync, 3D reconstruction, and classification.",
        "COMPLEX",
        "system-design",
        "en",
    ),
]


# ═══════════════════════════════════════════════════════════
#  REASONING (~80)
# ═══════════════════════════════════════════════════════════

REASONING_B9: list[dict] = [
    # ── Formal proofs ──
    _c(
        "Prove that the halting problem is undecidable using a diagonalization argument.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the set of recursively enumerable languages is closed under union but not under complement.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that every context-free language has a pumping lemma. State and prove the lemma.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that the class NP is closed under polynomial-time reduction.", "REASONING", "formal-proof", "en"),
    _c(
        "Prove that a graph is bipartite if and only if it contains no odd-length cycles.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that the maximum flow equals the minimum cut in a flow network.", "REASONING", "formal-proof", "en"),
    _c(
        "Prove that the rationals are countable by constructing an explicit bijection with the naturals.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that sqrt(2) is irrational using proof by contradiction.", "REASONING", "formal-proof", "en"),
    _c("Prove that there are infinitely many prime numbers.", "REASONING", "formal-proof", "en"),
    _c("Prove that the sum of the first n positive integers is n(n+1)/2.", "REASONING", "formal-proof", "en"),
    # ── Algorithm correctness proofs ──
    _c(
        "Prove that Dijkstra's algorithm correctly finds shortest paths when all edge weights are non-negative.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that binary search runs in O(log n) time and always finds the target if present.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the greedy activity selection algorithm yields an optimal solution.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c("Prove that Kruskal's algorithm produces a minimum spanning tree.", "REASONING", "algorithm-proof", "en"),
    _c(
        "Prove that the Ford-Fulkerson method terminates and finds a maximum flow when capacities are integers.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c("Prove that quicksort's expected comparison count is O(n log n).", "REASONING", "algorithm-proof", "en"),
    _c(
        "Prove that the two-pointer technique correctly finds a pair with a given sum in a sorted array.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the greedy coin change algorithm is optimal for certain coin systems.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    # ── Math derivations ──
    _c(
        "Derive the closed-form solution for the recurrence T(n) = 2T(n/2) + n using the master theorem.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c("Derive the expected number of comparisons in randomized quicksort.", "REASONING", "math-derivation", "en"),
    _c("Derive the optimal Huffman code length bound: H(X) <= L < H(X) + 1.", "REASONING", "math-derivation", "en"),
    _c(
        "Derive the Bayes optimal classifier for binary classification with 0-1 loss.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c("Derive the bias-variance decomposition for squared error loss.", "REASONING", "math-derivation", "en"),
    _c("Derive the optimal policy for a simple MDP using value iteration.", "REASONING", "math-derivation", "en"),
    _c("Derive the Fisher information for the Bernoulli distribution.", "REASONING", "math-derivation", "en"),
    _c("Derive the Cramer-Rao lower bound for an unbiased estimator.", "REASONING", "math-derivation", "en"),
    # ── Game theory ──
    _c("Find the Nash equilibrium in a two-player zero-sum game. Prove it exists.", "REASONING", "game-theory", "en"),
    _c(
        "Prove that every finite game has at least one mixed-strategy Nash equilibrium.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Analyze the iterated prisoner's dilemma: under what conditions does cooperation emerge?",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c("Prove that in a symmetric game, a symmetric Nash equilibrium exists.", "REASONING", "game-theory", "en"),
    _c(
        "Derive the optimal bidding strategy in a first-price sealed-bid auction with independent private values.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c("Prove that the minimax theorem holds for two-player zero-sum games.", "REASONING", "game-theory", "en"),
    _c(
        "Analyze the subgame-perfect equilibrium in a multi-stage game with perfect information.",
        "REASONING",
        "game-theory",
        "en",
    ),
    # ── Formal logic ──
    _c(
        "Prove that (A -> B) -> ((B -> C) -> (A -> C)) is a tautology using natural deduction.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    _c("Prove that the validity problem for first-order logic is undecidable.", "REASONING", "formal-logic", "en"),
    _c("Prove that resolution is refutation-complete for propositional logic.", "REASONING", "formal-logic", "en"),
    _c("Prove that the satisfiability of 2-SAT can be solved in linear time.", "REASONING", "formal-logic", "en"),
    _c("Prove that the set of tautologies in propositional logic is decidable.", "REASONING", "formal-logic", "en"),
    # ── Non-English REASONING ──
    _c("证明停机问题是不可判定的（使用对角化论证）", "REASONING", "formal-proof", "zh"),
    _c("证明二分图当且仅当不含奇数长度环", "REASONING", "formal-proof", "zh"),
    _c("证明 Dijkstra 算法在边权非负时正确找到最短路径", "REASONING", "algorithm-proof", "zh"),
    _c("推导 T(n)=2T(n/2)+n 的主定理闭式解", "REASONING", "math-derivation", "zh"),
    _c("求两人零和博弈的纳什均衡并证明其存在", "REASONING", "game-theory", "zh"),
    _c("证明 (A->B)->((B->C)->(A->C)) 是重言式", "REASONING", "formal-logic", "zh"),
    _c("停止問題が決定不能であることを対角線論法で証明してください", "REASONING", "formal-proof", "ja"),
    _c(
        "Dijkstraのアルゴリズムが非負の重みで最短経路を正しく見つけることを証明してください",
        "REASONING",
        "algorithm-proof",
        "ja",
    ),
    _c("マスター定理を用いてT(n)=2T(n/2)+nの閉形式を導出してください", "REASONING", "math-derivation", "ja"),
    _c("二人ゼロサムゲームのナッシュ均衡を求め、存在することを証明してください", "REASONING", "game-theory", "ja"),
    _c("정지 문제가 결정 불가능함을 대각선 논법으로 증명하세요", "REASONING", "formal-proof", "ko"),
    _c(
        "Dijkstra 알고리즘이 음이 아닌 가중치에서 최단 경로를 올바르게 찾음을 증명하세요",
        "REASONING",
        "algorithm-proof",
        "ko",
    ),
    _c("마스터 정리를 사용해 T(n)=2T(n/2)+n의 닫힌 형태를 유도하세요", "REASONING", "math-derivation", "ko"),
    _c("2인 제로섬 게임의 내시 균형을 구하고 존재함을 증명하세요", "REASONING", "game-theory", "ko"),
    _c("أثبت أن مشكلة التوقف غير قابلة للحل باستخدام جدلية القطرية.", "REASONING", "formal-proof", "ar"),
    _c(
        "أثبت أن خوارزمية Dijkstra تجد المسارات الأقصر بشكل صحيح عندما تكون الأوزان غير سالبة.",
        "REASONING",
        "algorithm-proof",
        "ar",
    ),
    _c(
        "Докажи, что проблема остановки неразрешима, используя диагональный аргумент.",
        "REASONING",
        "formal-proof",
        "ru",
    ),
    _c(
        "Докажи, что алгоритм Дейкстры правильно находит кратчайшие пути при неотрицательных весах.",
        "REASONING",
        "algorithm-proof",
        "ru",
    ),
    _c(
        "Demuestra que el problema de la parada es indecidible usando el argumento diagonal.",
        "REASONING",
        "formal-proof",
        "es",
    ),
    _c(
        "Demuestra que el algoritmo de Dijkstra encuentra correctamente los caminos más cortos con pesos no negativos.",
        "REASONING",
        "algorithm-proof",
        "es",
    ),
    _c(
        "Beweise, dass das Halteproblem unentscheidbar ist, mit dem Diagonalargument.",
        "REASONING",
        "formal-proof",
        "de",
    ),
    _c(
        "Beweise, dass Dijkstras Algorithmus bei nichtnegativen Gewichten korrekt kürzeste Wege findet.",
        "REASONING",
        "algorithm-proof",
        "de",
    ),
    _c(
        "Démontre que le problème de l'arrêt est indécidable en utilisant l'argument diagonal.",
        "REASONING",
        "formal-proof",
        "fr",
    ),
    _c(
        "Démontre que l'algorithme de Dijkstra trouve correctement les plus courts chemins avec des poids non négatifs.",
        "REASONING",
        "algorithm-proof",
        "fr",
    ),
    _c("Prove que o problema da parada é indecidível usando o argumento diagonal.", "REASONING", "formal-proof", "pt"),
    _c(
        "Prove que o algoritmo de Dijkstra encontra corretamente os caminhos mais curtos com pesos não negativos.",
        "REASONING",
        "algorithm-proof",
        "pt",
    ),
    _c("सिद्ध करें कि हॉल्टिंग समस्या अनिर्णायक है (विकर्ण तर्क का उपयोग करके)।", "REASONING", "formal-proof", "hi"),
    _c(
        "Durdurma probleminin karar verilemez olduğunu köşegen argümanıyla kanıtlayın.",
        "REASONING",
        "formal-proof",
        "tr",
    ),
    _c("Chứng minh bài toán dừng là không quyết định được bằng lập luận chéo.", "REASONING", "formal-proof", "vi"),
    _c(
        "Udowodnij, że problem stopu jest nierozstrzygalny, używając argumentu diagonalnego.",
        "REASONING",
        "formal-proof",
        "pl",
    ),
    # ── More REASONING to reach ~80 ──
    _c("Prove that merge sort is correct and runs in O(n log n) time.", "REASONING", "algorithm-proof", "en"),
    _c("Prove that the greedy set cover algorithm has approximation ratio H(n).", "REASONING", "algorithm-proof", "en"),
    _c("Prove that the greedy interval scheduling algorithm is optimal.", "REASONING", "algorithm-proof", "en"),
    _c(
        "Derive the optimal k for k-means clustering when the true number of clusters is known.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Prove that the perceptron algorithm converges when the data is linearly separable.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c("Prove that the set of regular languages is closed under intersection.", "REASONING", "formal-proof", "en"),
    _c(
        "Prove that the set of context-free languages is not closed under intersection.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Derive the optimal stopping rule for the secretary problem.", "REASONING", "math-derivation", "en"),
    _c(
        "Prove that in a repeated game, the grim trigger strategy is a Nash equilibrium.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c("Prove that (A and B) -> A is a tautology using truth tables.", "REASONING", "formal-logic", "en"),
    _c(
        "Prove that the greedy Huffman algorithm produces an optimal prefix code.", "REASONING", "algorithm-proof", "en"
    ),
    _c("Derive the optimal policy for a bandit with known reward distributions.", "REASONING", "math-derivation", "en"),
]


ALL_B9 = SIMPLE_B9 + MEDIUM_B9 + COMPLEX_B9 + REASONING_B9


def export(path=None):
    from pathlib import Path
    import json

    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b9.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B9:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter

    tiers = Counter(c["expected_tier"] for c in ALL_B9)
    langs = Counter(c["lang"] for c in ALL_B9)
    print(f"Batch 9: {len(ALL_B9)} cases")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")


if __name__ == "__main__":
    import sys

    export(sys.argv[1] if len(sys.argv) > 1 else None)

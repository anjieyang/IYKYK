"""Keyword-based feature extractors (Level 3 — secondary signals).

These are language-specific but kept as additive bonuses,
not primary classifiers. Structural features do the heavy lifting.
"""

from __future__ import annotations

import re

from uncommon_route.router.types import DimensionScore

# ─── Keyword Lists (multilingual) ───

CODE_KEYWORDS: list[str] = [
    "function", "class", "import", "def", "select", "async", "await",
    "const", "let", "var", "return", "```",
    "函数", "类", "导入", "异步", "返回",
    "関数", "クラス", "非同期",
    "функция", "класс", "импорт", "асинхронный",
    "función", "classe", "함수", "클래스", "دالة", "فئة",
]

REASONING_KEYWORDS: list[str] = [
    "prove", "theorem", "derive", "step by step", "chain of thought",
    "formally", "formal logic", "mathematical", "proof", "logically", "induction",
    "证明", "定理", "推导", "逐步", "数学", "逻辑", "归纳",
    "証明", "定理", "ステップバイステップ",
    "доказать", "докажи", "теорема", "шаг за шагом", "пошагово", "формально",
    "demostrar", "teorema", "paso a paso",
    "증명", "정리", "단계별", "귀납법",
    "إثبات", "نظرية", "خطوة بخطوة",
    "beweise", "beweis", "induktion", "schritt für schritt", "formal",
    "provar", "démontrer", "démontre", "prouver", "preuve", "récurrence",
    "demuestra", "demostración", "inducción",
    "winning strategy", "backward induction", "exchange argument",
    "反证法", "可数", "不等式",
    "diagonalization", "countable", "uncountable", "bipartite",
    "cauchy", "schwarz", "subgroup", "monotone", "converge",
    "nash equilibrium", "minimax", "nim",
    "derive the formula", "derive the time complexity",
    "prove that", "prove the", "show that",
    "счётно", "диагональный",
    "dénombrable", "diagonal",
    "contable", "diagonal",
    "abzählbar",
    "可算", "帰納法", "証明してください",
    "귀납법", "증명하세요", "비가산",
    "أثبت", "برهن", "غير قابل",
    "特征值", "泵引理",
    "np-complete", "np-hard", "np-полн", "undecidable", "不可判定",
    "pumping lemma", "reduction from", "reduce from",
    "decidable", "semi-decidable", "completeness theorem",
    "homeomorphism", "bijection", "isomorphism",
]

SIMPLE_KEYWORDS: list[str] = [
    "what is", "define", "translate", "hello", "yes or no", "capital of",
    "who is", "who invented", "when was", "when did", "how old",
    "what does", "what did", "what year", "how many", "how much",
    "how do you say",
    "什么是", "翻译", "你好", "是否", "谁是",
    "とは", "翻訳", "こんにちは",
    "что такое", "перевести", "переведи", "привет", "объясни",
    "qué es", "traducir", "traduce", "hola",
    "무엇", "번역", "안녕하세요",
    "ما هو", "ترجم", "مرحبا",
]

TECHNICAL_KEYWORDS: list[str] = [
    "algorithm", "optimize", "architecture", "distributed", "kubernetes",
    "microservice", "database", "infrastructure", "scalable", "concurrent",
    "算法", "优化", "架构", "分布式", "微服务", "数据库",
    "アルゴリズム", "最適化", "アーキテクチャ",
    "алгоритм", "оптимизаци", "архитектура", "распределённ", "систем",
    "algoritmo", "optimizar", "arquitectura",
    "알고리즘", "최적화", "아키텍처",
]

CREATIVE_KEYWORDS: list[str] = [
    "story", "poem", "compose", "brainstorm", "creative", "imagine", "write a",
    "故事", "诗", "创作", "创意", "想象",
    "物語", "詩", "創造的",
    "рассказ", "стихотворение", "сочини", "придумай", "напиши",
    "historia", "poema", "creativo",
]

IMPERATIVE_KEYWORDS: list[str] = [
    "build", "create", "implement", "design", "develop", "deploy", "configure",
    "构建", "创建", "实现", "设计", "开发", "部署",
    "構築", "作成", "実装", "設計",
    "создать", "создай", "реализовать", "реализуй", "разработать",
    "construir", "crear", "implementar", "diseñar",
    "구축", "생성", "구현", "설계",
]

CONSTRAINT_KEYWORDS: list[str] = [
    "at most", "at least", "within", "no more than", "maximum", "minimum", "limit",
    "不超过", "至少", "最多", "最大", "限制",
    "не более", "не менее", "максимум", "ограничение",
    "como máximo", "al menos", "máximo", "límite",
]

OUTPUT_FORMAT_KEYWORDS: list[str] = [
    "json", "yaml", "xml", "table", "csv", "markdown", "schema", "format as",
    "表格", "格式化", "结构化",
    "таблица", "форматировать",
]

DOMAIN_KEYWORDS: list[str] = [
    "quantum", "fpga", "vlsi", "risc-v", "genomics", "proteomics",
    "homomorphic", "zero-knowledge", "lattice-based",
    "量子", "基因组", "零知识",
    "квантовый", "фотоника", "геномика",
]

AGENTIC_KEYWORDS: list[str] = [
    "read file", "edit", "modify", "update the", "create file",
    "execute", "deploy", "install", "npm", "pip", "compile",
    "after that", "once done", "step 1", "step 2",
    "fix", "debug", "until it works", "verify", "confirm",
    "读取文件", "编辑", "修改", "更新", "执行", "部署", "修复", "调试",
    "editar", "modificar", "ejecutar", "verificar",
    "편집", "수정", "실행", "확인",
]

ANALYTICAL_KEYWORDS: list[str] = [
    "explain", "summarize", "compare", "analyze", "evaluate", "describe", "discuss",
    "difference between", "pros and cons",
    "解释", "总结", "比较", "分析", "评估", "描述", "讨论", "区别",
    "説明", "要約", "比較", "分析",
    "объясни", "объясните", "резюмируй", "сравни", "проанализируй", "опиши", "разницу",
    "explicar", "resumir", "comparar", "analizar", "describir",
    "설명", "요약", "비교", "분석",
    "اشرح", "لخص", "قارن", "حلل",
    "rewrite", "rephrase", "paraphrase", "convert", "transform",
    "extract", "classify", "categorize", "label", "sort into",
    "改写", "提取", "分类", "归类",
    "перепиши", "извлеки", "классифицируй",
    "réécris", "extraire", "classer",
    "umschreiben", "extrahieren", "klassifizieren",
]

MULTI_STEP_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"first.*then", re.IGNORECASE),
    re.compile(r"step\s+\d", re.IGNORECASE),
    re.compile(r"\d+\.\s"),
    re.compile(r"第.步"),
    re.compile(r"сначала.*потом", re.IGNORECASE),
    re.compile(r"primero.*luego", re.IGNORECASE),
]


# ─── Keyword Scoring ───

def _contains_cjk(text: str) -> bool:
    """Check if text contains CJK / Kana / Hangul characters (scripts without space separation)."""
    for ch in text:
        cp = ord(ch)
        if (0x4E00 <= cp <= 0x9FFF
                or 0x3400 <= cp <= 0x4DBF
                or 0x3040 <= cp <= 0x309F
                or 0x30A0 <= cp <= 0x30FF
                or 0xAC00 <= cp <= 0xD7AF):
            return True
    return False


def _keyword_in_text(kw: str, text_lower: str) -> bool:
    """Match keyword in text. Short Latin/Cyrillic keywords use word boundary;
    CJK/Kana/Hangul keywords use substring match (no space-based word separation)."""
    kw_low = kw.lower()
    if kw_low not in text_lower:
        return False
    if _contains_cjk(kw_low):
        return True
    if len(kw_low) <= 5:
        return bool(re.search(r"(?<!\w)" + re.escape(kw_low) + r"(?!\w)", text_lower))
    return True


def _score_keyword_list(
    text: str,
    keywords: list[str],
    name: str,
    signal_label: str,
    low_threshold: int,
    high_threshold: int,
    low_score: float,
    high_score: float,
) -> DimensionScore:
    lower = text.lower()
    matches = [kw for kw in keywords if _keyword_in_text(kw, lower)]
    count = len(matches)

    if count >= high_threshold:
        sig = f"{signal_label}({','.join(matches[:3])})"
        return DimensionScore(name, high_score, sig)
    if count >= low_threshold:
        sig = f"{signal_label}({','.join(matches[:3])})"
        return DimensionScore(name, low_score, sig)
    return DimensionScore(name, 0.0, None)


def extract_keyword_features(text: str) -> list[DimensionScore]:
    """Extract all keyword-based features from user prompt."""
    lower = text.lower()

    dims: list[DimensionScore] = [
        _score_keyword_list(text, CODE_KEYWORDS, "code_presence", "code", 1, 2, 0.5, 1.0),
        _score_keyword_list(text, REASONING_KEYWORDS, "reasoning_markers", "reasoning", 1, 2, 0.7, 1.0),
        _score_keyword_list(text, TECHNICAL_KEYWORDS, "technical_terms", "technical", 2, 4, 0.5, 1.0),
        _score_keyword_list(text, CREATIVE_KEYWORDS, "creative_markers", "creative", 1, 2, 0.5, 0.7),
        _score_keyword_list(text, SIMPLE_KEYWORDS, "simple_indicators", "simple", 1, 2, -1.0, -1.0),
        _score_keyword_list(text, IMPERATIVE_KEYWORDS, "imperative_verbs", "imperative", 1, 2, 0.3, 0.5),
        _score_keyword_list(text, CONSTRAINT_KEYWORDS, "constraint_count", "constraints", 1, 3, 0.3, 0.7),
        _score_keyword_list(text, OUTPUT_FORMAT_KEYWORDS, "output_format", "format", 1, 2, 0.4, 0.7),
        _score_keyword_list(text, DOMAIN_KEYWORDS, "domain_specificity", "domain", 1, 2, 0.5, 0.8),
    ]

    # Analytical verbs → MEDIUM signal
    dims.append(_score_keyword_list(
        text, ANALYTICAL_KEYWORDS, "analytical_verbs", "analytical", 1, 2, 0.4, 0.7,
    ))

    # Agentic task scoring
    agentic_matches = [kw for kw in AGENTIC_KEYWORDS if kw.lower() in lower]
    agentic_count = len(agentic_matches)
    if agentic_count >= 4:
        dims.append(DimensionScore("agentic_task", 1.0, f"agentic({','.join(agentic_matches[:3])})"))
    elif agentic_count >= 2:
        dims.append(DimensionScore("agentic_task", 0.5, f"agentic({','.join(agentic_matches[:3])})"))
    elif agentic_count >= 1:
        dims.append(DimensionScore("agentic_task", 0.2, f"agentic-light({agentic_matches[0]})"))
    else:
        dims.append(DimensionScore("agentic_task", 0.0, None))

    # Multi-step pattern scoring
    step_hits = sum(1 for p in MULTI_STEP_PATTERNS if p.search(text))
    if step_hits > 0:
        dims.append(DimensionScore("multi_step_patterns", min(1.0, step_hits * 0.35), "multi-step"))
    else:
        dims.append(DimensionScore("multi_step_patterns", 0.0, None))

    return dims

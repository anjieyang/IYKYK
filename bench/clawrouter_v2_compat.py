"""ClawRouter v2 (TypeScript) faithful Python port for comparison.

This replicates the EXACT logic from src/router/rules.ts + config.ts
so we can benchmark the original ClawRouter against UncommonRoute
on the same dataset.
"""

from __future__ import annotations

import math
import re

# ─── Config (from src/router/config.ts) ───

TOKEN_THRESHOLDS = {"simple": 50, "complex": 500}

TIER_BOUNDARIES = {
    "simpleMedium": 0.0,
    "mediumComplex": 0.3,
    "complexReasoning": 0.5,
}

CONFIDENCE_STEEPNESS = 12
CONFIDENCE_THRESHOLD = 0.7

DIMENSION_WEIGHTS = {
    "tokenCount": 0.08,
    "codePresence": 0.15,
    "reasoningMarkers": 0.18,
    "technicalTerms": 0.1,
    "creativeMarkers": 0.05,
    "simpleIndicators": 0.02,
    "multiStepPatterns": 0.12,
    "questionComplexity": 0.05,
    "imperativeVerbs": 0.03,
    "constraintCount": 0.04,
    "outputFormat": 0.03,
    "referenceComplexity": 0.02,
    "negationComplexity": 0.01,
    "domainSpecificity": 0.02,
    "agenticTask": 0.04,
}

# ─── Keywords (subset from config.ts) ───

CODE_KEYWORDS = [
    "function",
    "class",
    "import",
    "def",
    "select",
    "async",
    "await",
    "const",
    "let",
    "var",
    "return",
    "```",
    "函数",
    "类",
    "导入",
    "异步",
    "返回",
    "関数",
    "クラス",
    "非同期",
    "функция",
    "класс",
    "импорт",
    "асинхронный",
]

REASONING_KEYWORDS = [
    "prove",
    "theorem",
    "derive",
    "step by step",
    "chain of thought",
    "formally",
    "mathematical",
    "proof",
    "logically",
    "证明",
    "定理",
    "推导",
    "逐步",
    "数学",
    "逻辑",
    "証明",
    "定理",
    "ステップバイステップ",
    "доказать",
    "докажи",
    "теорема",
    "шаг за шагом",
    "формально",
]

SIMPLE_KEYWORDS = [
    "what is",
    "define",
    "translate",
    "hello",
    "yes or no",
    "capital of",
    "who is",
    "when was",
    "how old",
    "什么是",
    "翻译",
    "你好",
    "是否",
    "谁是",
    "что такое",
    "перевести",
    "привет",
]

TECHNICAL_KEYWORDS = [
    "algorithm",
    "optimize",
    "architecture",
    "distributed",
    "kubernetes",
    "microservice",
    "database",
    "infrastructure",
    "算法",
    "优化",
    "架构",
    "分布式",
    "微服务",
    "数据库",
]

CREATIVE_KEYWORDS = [
    "story",
    "poem",
    "compose",
    "brainstorm",
    "creative",
    "imagine",
    "write a",
    "故事",
    "诗",
    "创作",
    "创意",
]

IMPERATIVE_KEYWORDS = [
    "build",
    "create",
    "implement",
    "design",
    "develop",
    "deploy",
    "configure",
    "构建",
    "创建",
    "实现",
    "设计",
    "开发",
    "部署",
]

CONSTRAINT_KEYWORDS = [
    "at most",
    "at least",
    "within",
    "no more than",
    "maximum",
    "minimum",
    "limit",
    "不超过",
    "至少",
    "最多",
    "限制",
]

OUTPUT_FORMAT_KEYWORDS = [
    "json",
    "yaml",
    "xml",
    "table",
    "csv",
    "markdown",
    "schema",
    "format as",
    "表格",
    "格式化",
    "结构化",
]

DOMAIN_KEYWORDS = [
    "quantum",
    "fpga",
    "vlsi",
    "risc-v",
    "genomics",
    "proteomics",
    "homomorphic",
    "zero-knowledge",
    "量子",
    "基因组",
    "零知识",
]

AGENTIC_KEYWORDS = [
    "read file",
    "edit",
    "modify",
    "update the",
    "create file",
    "execute",
    "deploy",
    "install",
    "npm",
    "pip",
    "compile",
    "after that",
    "once done",
    "step 1",
    "step 2",
    "fix",
    "debug",
    "until it works",
    "verify",
    "confirm",
]

NEGATION_KEYWORDS = [
    "don't",
    "do not",
    "avoid",
    "never",
    "without",
    "except",
    "exclude",
    "不要",
    "避免",
    "从不",
    "没有",
]

REFERENCE_KEYWORDS = [
    "above",
    "below",
    "previous",
    "following",
    "the docs",
    "the api",
    "the code",
    "上面",
    "下面",
    "之前",
    "文档",
    "代码",
]


# ─── Scoring functions (from src/router/rules.ts) ───


def _score_token_count(tokens: int) -> tuple[float, str | None]:
    if tokens < TOKEN_THRESHOLDS["simple"]:
        return -1.0, f"short ({tokens} tokens)"
    if tokens > TOKEN_THRESHOLDS["complex"]:
        return 1.0, f"long ({tokens} tokens)"
    return 0.0, None


def _score_keywords(
    text: str, keywords: list[str], low_thresh: int, high_thresh: int, low_score: float, high_score: float
) -> float:
    matches = sum(1 for kw in keywords if kw.lower() in text)
    if matches >= high_thresh:
        return high_score
    if matches >= low_thresh:
        return low_score
    return 0.0


def _score_multi_step(text: str) -> float:
    patterns = [r"first.*then", r"step \d", r"\d\.\s"]
    hits = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
    return 0.5 if hits > 0 else 0.0


def _score_question_complexity(text: str) -> float:
    count = text.count("?")
    return 0.5 if count > 3 else 0.0


def classify_clawrouter_v2(prompt: str, system_prompt: str | None = None) -> tuple[str, float]:
    """Replicate ClawRouter v2 classifyByRules logic."""
    full_text = f"{system_prompt or ''} {prompt}"
    estimated_tokens = max(1, len(full_text) // 4)  # original: Math.ceil(length / 4)
    user_text = prompt.lower()

    # Score dimensions
    dims: dict[str, float] = {}

    tc_score, _ = _score_token_count(estimated_tokens)
    dims["tokenCount"] = tc_score
    dims["codePresence"] = _score_keywords(user_text, CODE_KEYWORDS, 1, 2, 0.5, 1.0)
    dims["reasoningMarkers"] = _score_keywords(user_text, REASONING_KEYWORDS, 1, 2, 0.7, 1.0)
    dims["technicalTerms"] = _score_keywords(user_text, TECHNICAL_KEYWORDS, 2, 4, 0.5, 1.0)
    dims["creativeMarkers"] = _score_keywords(user_text, CREATIVE_KEYWORDS, 1, 2, 0.5, 0.7)
    dims["simpleIndicators"] = _score_keywords(user_text, SIMPLE_KEYWORDS, 1, 2, -1.0, -1.0)
    dims["multiStepPatterns"] = _score_multi_step(user_text)
    dims["questionComplexity"] = _score_question_complexity(prompt)
    dims["imperativeVerbs"] = _score_keywords(user_text, IMPERATIVE_KEYWORDS, 1, 2, 0.3, 0.5)
    dims["constraintCount"] = _score_keywords(user_text, CONSTRAINT_KEYWORDS, 1, 3, 0.3, 0.7)
    dims["outputFormat"] = _score_keywords(user_text, OUTPUT_FORMAT_KEYWORDS, 1, 2, 0.4, 0.7)
    dims["referenceComplexity"] = _score_keywords(user_text, REFERENCE_KEYWORDS, 1, 2, 0.3, 0.5)
    dims["negationComplexity"] = _score_keywords(user_text, NEGATION_KEYWORDS, 2, 3, 0.3, 0.5)
    dims["domainSpecificity"] = _score_keywords(user_text, DOMAIN_KEYWORDS, 1, 2, 0.5, 0.8)
    dims["agenticTask"] = _score_keywords(user_text, AGENTIC_KEYWORDS, 1, 2, 0.2, 0.5)

    # Reasoning override (from rules.ts)
    reasoning_matches = sum(1 for kw in REASONING_KEYWORDS if kw.lower() in user_text)
    if reasoning_matches >= 2:
        return "REASONING", 0.85

    # Weighted score
    weighted_score = sum(dims[k] * DIMENSION_WEIGHTS.get(k, 0) for k in dims)

    # Tier mapping
    sm = TIER_BOUNDARIES["simpleMedium"]
    mc = TIER_BOUNDARIES["mediumComplex"]
    cr = TIER_BOUNDARIES["complexReasoning"]

    if weighted_score < sm:
        tier = "SIMPLE"
        dist = sm - weighted_score
    elif weighted_score < mc:
        tier = "MEDIUM"
        dist = min(weighted_score - sm, mc - weighted_score)
    elif weighted_score < cr:
        tier = "COMPLEX"
        dist = min(weighted_score - mc, cr - weighted_score)
    else:
        tier = "REASONING"
        dist = weighted_score - cr

    confidence = 1 / (1 + math.exp(-CONFIDENCE_STEEPNESS * dist))

    if confidence < CONFIDENCE_THRESHOLD:
        tier = "MEDIUM"  # ambiguous default

    return tier, confidence

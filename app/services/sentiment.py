import re
from snownlp import SnowNLP


def analyze(text: str, lang: str = "zh") -> dict:
    """分析文本情感，返回标签和置信度"""
    if lang == "zh":
        try:
            s = SnowNLP(text)
            score = s.sentiments
        except Exception:
            score = 0.5
    else:
        score = _simple_en_sentiment(text)

    if score > 0.6:
        label = "positive"
    elif score < 0.4:
        label = "negative"
    else:
        label = "neutral"

    return {"label": label, "score": round(float(score), 4)}


def _simple_en_sentiment(text: str) -> float:
    """简易英文情感分析（兜底方案）"""
    positive_words = {
        "good", "great", "excellent", "amazing", "wonderful", "fantastic",
        "happy", "love", "beautiful", "awesome", "brilliant", "positive",
        "best", "perfect", "nice", "enjoy", "delightful", "superb",
    }
    negative_words = {
        "bad", "terrible", "awful", "horrible", "hate", "ugly",
        "worst", "poor", "sad", "angry", "disgusting", "negative",
        "dreadful", "mediocre", "annoying", "boring", "terrific",
    }
    words = set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
    pos_count = len(words & positive_words)
    neg_count = len(words & negative_words)
    total = pos_count + neg_count
    if total == 0:
        return 0.5
    return pos_count / total

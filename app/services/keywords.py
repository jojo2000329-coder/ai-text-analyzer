import jieba
import jieba.analyse


def extract(text: str, topk: int = 10, lang: str = "zh") -> list:
    """提取文本关键词，使用 TF-IDF 算法"""
    if lang == "zh":
        words = jieba.analyse.extract_tags(text, topK=topk, withWeight=True)
    else:
        words = _simple_en_keywords(text, topk)

    return [
        {"word": w, "weight": round(float(weight), 4)}
        for w, weight in words
    ]


def _simple_en_keywords(text: str, topk: int = 10) -> list:
    """简易英文关键词提取"""
    import re
    from collections import Counter

    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can",
        "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "this", "that", "these", "those", "it", "its", "and", "or",
        "but", "not", "so", "if", "as", "about", "than", "into",
        "i", "you", "he", "she", "we", "they", "me", "him", "her",
        "us", "them", "my", "your", "his", "our", "their",
    }

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    words = [w for w in words if w not in stop_words]
    counter = Counter(words)
    total = sum(counter.values())

    return [
        (word, count / total)
        for word, count in counter.most_common(topk)
    ]

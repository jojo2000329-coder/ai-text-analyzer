import re
from collections import defaultdict


def summarize(text: str, ratio: float = 0.3, lang: str = "zh") -> dict:
    """基于 TextRank 思路的抽取式摘要"""
    if not text.strip():
        return {"summary": "", "original_length": 0, "summary_length": 0}

    sentences = _split_sentences(text, lang)
    if len(sentences) <= 3:
        summary = text
    else:
        scores = _rank_sentences(sentences, lang)
        top_n = max(1, int(len(sentences) * ratio))
        ranked = sorted(
            range(len(sentences)),
            key=lambda i: scores[i],
            reverse=True,
        )[:top_n]
        ranked.sort()
        summary = "".join([sentences[i] for i in ranked])

    original_length = len(text)
    summary_length = len(summary)

    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
    }


def _split_sentences(text: str, lang: str = "zh") -> list:
    """分句"""
    if lang == "zh":
        delimiters = r"([。！？\n]+)"
    else:
        delimiters = r"([.!?\n]+)"

    parts = re.split(delimiters, text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        sent = parts[i] + (parts[i + 1] if i + 1 < len(parts) else "")
        sent = sent.strip()
        if sent:
            sentences.append(sent)
    if parts and len(parts) % 2 == 1 and parts[-1].strip():
        sentences.append(parts[-1].strip())
    return sentences if sentences else [text]


def _rank_sentences(sentences: list, lang: str = "zh") -> list:
    """简单的句子打分：基于词频"""
    import jieba

    word_freq = defaultdict(float)
    sent_words = []

    for sent in sentences:
        if lang == "zh":
            words = [w for w in jieba.lcut(sent) if len(w.strip()) > 1]
        else:
            words = re.findall(r"\b[a-zA-Z]{3,}\b", sent.lower())
        sent_words.append(words)
        for w in words:
            word_freq[w] += 1

    max_freq = max(word_freq.values()) if word_freq else 1
    for w in word_freq:
        word_freq[w] /= max_freq

    scores = []
    for words in sent_words:
        if not words:
            scores.append(0)
        else:
            score = sum(word_freq.get(w, 0) for w in words) / len(words)
            scores.append(score)

    return scores

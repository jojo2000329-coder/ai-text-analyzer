from pydantic import BaseModel, Field
from typing import List, Optional


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="待分析的文本")
    lang: str = Field(default="zh", pattern="^(zh|en)$", description="语言：zh 中文 / en 英文")


class SentimentResult(BaseModel):
    label: str = Field(description="情感标签：positive / negative / neutral")
    score: float = Field(ge=0, le=1, description="置信度分数")


class KeywordItem(BaseModel):
    word: str = Field(description="关键词")
    weight: float = Field(description="权重分数")


class KeywordsResult(BaseModel):
    keywords: List[KeywordItem]


class SummaryResult(BaseModel):
    summary: str = Field(description="摘要文本")
    original_length: int = Field(description="原文长度（字符）")
    summary_length: int = Field(description="摘要长度（字符）")


class CategoryResult(BaseModel):
    category: str = Field(description="分类标签")
    confidence: float = Field(ge=0, le=1, description="置信度")


class AnalyzeResponse(BaseModel):
    text: str
    sentiment: Optional[SentimentResult] = None
    keywords: Optional[List[KeywordItem]] = None
    summary: Optional[SummaryResult] = None
    category: Optional[CategoryResult] = None


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "AI 智文助手"
    version: str = "1.0.0"

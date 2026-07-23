from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.schemas import (
    TextRequest, SentimentResult, KeywordItem,
    SummaryResult, CategoryResult, AnalyzeResponse, HealthResponse,
)
from app.services import sentiment, keywords, summarizer, classifier


@asynccontextmanager
async def lifespan(app: FastAPI):
    import jieba
    jieba.initialize()
    print("[启动] jieba 词典加载完成")
    yield
    print("[关闭] 服务停止")


app = FastAPI(
    title="AI 智文助手",
    description="智能中文文本分析 API 服务",
    version="1.0.0",
    lifespan=lifespan,
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("app/static/index.html", media_type="text/html")


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse()


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(req: TextRequest):
    try:
        return AnalyzeResponse(
            text=req.text,
            sentiment=SentimentResult(**sentiment.analyze(req.text, req.lang)),
            keywords=[
                KeywordItem(**kw)
                for kw in keywords.extract(req.text, lang=req.lang)
            ],
            summary=SummaryResult(**summarizer.summarize(req.text, lang=req.lang)),
            category=CategoryResult(**classifier.classify(req.text, req.lang)),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/sentiment")
async def analyze_sentiment(req: TextRequest):
    try:
        return SentimentResult(**sentiment.analyze(req.text, req.lang))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/keywords")
async def analyze_keywords(req: TextRequest):
    try:
        return {"keywords": [
            KeywordItem(**kw) for kw in keywords.extract(req.text, lang=req.lang)
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/summary")
async def analyze_summary(req: TextRequest):
    try:
        return SummaryResult(**summarizer.summarize(req.text, lang=req.lang))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/category")
async def analyze_category(req: TextRequest):
    try:
        return CategoryResult(**classifier.classify(req.text, req.lang))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

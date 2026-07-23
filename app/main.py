from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[启动] 饮食健康助手已加载")
    yield
    print("[关闭] 服务停止")

app = FastAPI(
    title="AI 饮食健康助手",
    description="饮食营养健康问答助手",
    version="2.0.0",
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    answer: str

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("app/static/index.html", media_type="text/html")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    from app.nutrition.ai_chat import ai_chat as ai_fn
    ai_resp = ai_fn(req.text)
    if ai_resp:
        return ChatResponse(answer=ai_resp)
    from app.nutrition.chat_engine import chat as chat_fn
    try:
        answer = chat_fn(req.text)
        return ChatResponse(answer=answer)
    except Exception as e:
        return ChatResponse(answer=f"抱歉，出错了：{str(e)}")

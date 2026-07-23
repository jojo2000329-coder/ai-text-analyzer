import os, json, urllib.request

SYSTEM_PROMPT = "你是一个专业的饮食营养健康助手。请用中文回答关于食物、营养、饮食、健康等方面的问题。回答要自然、详细、有帮助。"

def ai_chat(query):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    try:
        data = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            "temperature": 0.7,
            "max_tokens": 800,
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.deepseek.com/v1/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return None
import os, json, urllib.request, socket

SYSTEM_PROMPT = "你是一个专业的饮食营养健康助手。请用中文回答关于食物、营养、饮食、健康等方面的问题。回答要自然、详细、有帮助。"


def ai_chat(query):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    try:
        socket.setdefaulttimeout(10)
        data = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            "temperature": 0.7,
            "max_tokens": 800,
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.deepseek.com/v1/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[AI Error] {type(e).__name__}: {e}")
        return None

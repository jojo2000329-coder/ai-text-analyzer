import os
import openai

SYSTEM_PROMPT = "你是一个专业的饮食营养健康助手。请用中文回答关于食物、营养、饮食、健康等方面的问题。回答要自然、详细、有帮助。"


def ai_chat(query):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    try:
        client = openai.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            temperature=0.7,
            max_tokens=800,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return None

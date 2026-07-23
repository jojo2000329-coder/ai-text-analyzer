ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

FROM python:3.11-slim

WORKDIR /app

# 瀹夎绯荤粺渚濊禆锛坖ieba 鍒嗚瘝闇€瑕侊級
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 澶嶅埗渚濊禆鏂囦欢骞跺畨瑁?Python 鍖?COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 澶嶅埗搴旂敤浠ｇ爜
COPY . .

# 闈?root 鐢ㄦ埛杩愯锛堝畨鍏ㄦ渶浣冲疄璺碉級
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 鍋ュ悍妫€鏌?HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

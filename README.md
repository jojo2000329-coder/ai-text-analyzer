# AI 智文助手

智能中文文本分析 API 服务，基于 FastAPI 构建，支持 Docker 容器化部署。

## 功能

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 服务状态 |
| `/health` | GET | 健康检查 |
| `/analyze` | POST | 一站式分析（情感+关键词+摘要+分类） |
| `/analyze/sentiment` | POST | 情感分析 |
| `/analyze/keywords` | POST | 关键词提取 |
| `/analyze/summary` | POST | 文本摘要 |
| `/analyze/category` | POST | 文本分类 |

## 快速开始

### 本地运行

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080

访问 http://localhost:8080/docs 查看 Swagger 文档。

### Docker 构建

docker build -t ai-text-analyzer .
docker run -d -p 8080:8080 ai-text-analyzer

### 调用示例

curl -X POST http://localhost:8080/analyze -H "Content-Type: application/json" -d "{\"text\": \"今天天气真好，心情非常愉快！\", \"lang\": \"zh\"}"

## 部署到腾讯云 CloudBase

1. 安装 CloudBase CLI：npm i -g @cloudbase/cli
2. 登录：tcb login
3. 部署：tcb framework deploy

详见 cloudbase.yaml 配置文件。

## 技术栈

- FastAPI - Web 框架
- SnowNLP - 中文情感分析
- jieba - 中文分词 / 关键词提取
- Docker - 容器化
- 腾讯云 CloudBase - 云托管

## 项目结构

ai-text-analyzer/
  app/
    main.py          # FastAPI 应用入口
    schemas.py       # 数据模型
    services/
      sentiment.py   # 情感分析服务
      keywords.py    # 关键词提取服务
      summarizer.py  # 文本摘要服务
      classifier.py  # 文本分类服务
  Dockerfile
  requirements.txt
  cloudbase.yaml     # 腾讯云 CloudBase 配置
  .dockerignore

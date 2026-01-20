# AI Agent API 项目

基于 LangGraph 和 LangChain 构建的 AI Agent 对话系统。支持会话隔离、历史查询，并提供一个 RESTful API 接口进行交互。

## 项目结构

```bash
.
├── app.py                # FastAPI应用主文件
├── .env                  # 环境配置文件，包含API Key等敏感信息
├── requirements.txt      # 项目依赖包
└── README.md             # 项目说明文档
````

## 依赖项

项目使用了以下主要依赖：

* `LangGraph`：用于构建状态机和业务逻辑的框架
* `LangChain`：用于集成各种语言模型
* `FastAPI`：用于构建高性能API
* `pydantic`：用于数据验证
* `python-dotenv`：加载环境变量
* `logging`：日志记录

可以通过以下命令安装项目依赖：

```bash
pip install -r requirements.txt
```

## 配置

项目中的 API Key 需要从 `.env` 文件加载，确保在该文件中配置了 `DASHSCOPE_API_KEY`。

示例 `.env` 文件：

```
DASHSCOPE_API_KEY=your-api-key-here
```

## API 接口

### 1. `/agent/chat` - AI Agent 对话接口

**POST 请求**

* **请求体**：

```json
{
  "user_input": "你好，AI",
  "thread_id": "default"
}
```

* **响应体**：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "thread_id": "default",
    "user_input": "你好，AI",
    "ai_response": "你好！我可以帮你什么？"
  }
}
```

* **功能**：向 AI Agent 发送用户输入，返回 AI 的回复。支持会话隔离，通过 `thread_id` 实现不同用户或会话的状态保存。

### 2. `/agent/get_history` - 获取对话历史接口

**POST 请求**

* **请求体**：

```json
{
  "thread_id": "default"
}
```

* **响应体**：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "thread_id": "default",
    "history": [
      {
        "index": 1,
        "role": "user",
        "content": "你好，AI"
      },
      {
        "index": 2,
        "role": "ai",
        "content": "你好！我可以帮你什么？"
      }
    ]
  }
}
```

* **功能**：根据 `thread_id` 获取指定会话的对话历史记录。

### 3. `/health` - 服务健康检查接口

**GET 请求**

* **响应体**：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "status": "healthy",
    "service": "AI Agent API"
  }
}
```

* **功能**：检查 API 服务是否正常运行。

## 项目使用说明

1. **启动项目**：

   在启动项目之前，确保已经安装了项目依赖，并且 `.env` 文件中配置了正确的 API Key。

   启动 FastAPI 服务：

   ```bash
   uvicorn app:app --reload
   ```

   服务会在 `http://127.0.0.1:8000` 启动。

2. **访问 Swagger UI**：

   FastAPI 自动生成了 Swagger UI 文档，您可以通过访问 `http://127.0.0.1:8000/docs` 来查看和测试 API。

3. **通过 API 进行交互**：

   * 使用 `POST /agent/chat` 发送对话请求，并获取 AI 回复。
   * 使用 `POST /agent/get_history` 获取指定会话的历史记录。
   * 使用 `GET /health` 检查服务的健康状态。

## 代码逻辑说明

### 核心流程

1. **LangGraph 状态图**：

   * 采用 `StateGraph` 来构建整个对话流程。
   * `call_llm_node` 用于调用大语言模型，获取回复。
   * `user_input_node` 用于处理用户输入，并将其更新到状态中。

2. **AI Assistant**：

   * 封装了 LangGraph 的复杂操作，提供简单易用的 `chat` 和 `get_history` 方法。

3. **FastAPI**：

   * `FastAPI` 用于提供 RESTful API，暴露给外部调用。
   * 每个用户的对话状态通过 `thread_id` 进行隔离。
"# langgraph-fastapi-tongyi-agent" 

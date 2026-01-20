# LangGraph + FastAPI AI Agent Demo

> 一个基于 **LangGraph 状态机** 与 **FastAPI** 的 AI Agent 后端示例项目  
> 支持 **多轮对话、会话隔离、对话历史持久化**  
> 本项目主要用于 **AI Agent 技术学习与面试展示**

---

## 📌 项目背景与学习动机

在学习 AI Agent 相关技术时，我发现：
- 仅使用 LangChain 的 `Chain` 更偏“线性调用”
- 而真实 Agent 系统更接近 **“有状态、有流程控制的系统”**

因此我选择：
- 使用 **LangGraph** 构建 Agent 状态机
- 使用 **FastAPI** 对外提供标准化 API
- 尝试将「Agent 逻辑」与「Web 服务」进行工程化拆分

本项目的目标不是做复杂功能，而是**把 Agent 的核心思想真正跑通**。

---

## 🧠 项目核心能力

- ✅ 基于 **LangGraph StateGraph** 的 Agent 状态建模
- ✅ 支持 **多轮对话 & 会话隔离（thread_id）**
- ✅ 使用 **MemorySaver** 实现对话历史持久化
- ✅ 封装为 **FastAPI 服务**，便于前后端 / 系统集成
- ✅ 清晰的工程目录结构，方便扩展为复杂 Agent

---

## 🏗️ 项目结构说明

```text
.
├── app/
│   ├── main.py        # FastAPI 启动入口 & 接口定义
│   ├── graph.py       # LangGraph 状态图构建逻辑
│   ├── nodes.py       # Agent 各执行节点（如 LLM 调用）
│   ├── state.py       # AgentState 状态结构定义
│   ├── service.py     # AIAssistant 业务封装层
│   ├── config.py      # 环境变量 / 配置加载
│   └── __init__.py
├── requirements.txt   # 项目依赖
├── .env.example       # 环境变量示例（不含真实 Key）
├── .gitignore
└── README.md

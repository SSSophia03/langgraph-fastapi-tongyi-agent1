# LangGraph + FastAPI AI Agent

> 一个基于 **LangGraph 状态机** 与 **FastAPI** 的 AI Agent 后端示例项目  
> 支持 **多轮对话、会话隔离、对话历史持久化**  
> 本项目用于 **AI Agent 技术学习、工程实践与面试展示**

---

## 🧠 项目背景与学习动机

在学习大模型应用开发过程中，我逐渐意识到：

- 传统基于 LangChain 的 `Chain` 更偏向**线性流程**
- 而真实 AI Agent 更像一个 **有状态、有流程控制的系统**

因此，本项目尝试使用 **LangGraph** 构建 Agent 的状态机结构，并通过 **FastAPI** 对外提供服务接口，  
重点关注以下能力的理解与实践：

- Agent 状态如何定义与流转
- 多轮对话与会话隔离如何实现
- 如何将 Agent 能力进行工程化封装

本项目的目标不是做复杂功能，而是 **真正跑通 Agent 的核心设计思想**。

---

## ✨ 项目核心能力

- ✅ 基于 **LangGraph StateGraph** 的 Agent 状态建模
- ✅ 支持 **多轮对话 / 会话隔离（thread_id）**
- ✅ 使用 **MemorySaver** 实现对话历史持久化
- ✅ 封装为 **FastAPI API 服务**，便于系统集成
- ✅ 清晰的工程目录拆分，便于后续扩展复杂 Agent

---

## 🏗️ 项目结构说明

```text
.
├── app/
│   ├── main.py        # FastAPI 启动入口 & API 定义
│   ├── graph.py       # LangGraph 状态图构建
│   ├── nodes.py       # Agent 执行节点（LLM 调用等）
│   ├── state.py       # AgentState 状态结构定义
│   ├── service.py     # AIAssistant 业务封装层
│   ├── config.py      # 环境变量与配置加载
│   └── __init__.py
├── requirements.txt   # 项目依赖
├── .gitignore
└── README.md

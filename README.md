# US FedReg RAG_Agentic_System_using_ollama_mistral_7b
 

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-async%20web%20API-green)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20Qwen2.5-orange)
![Status](https://img.shields.io/badge/Status-Demo-blue)

A **user-facing Retrieval-Augmented Generation (RAG) Agentic System** that lets users query the [Federal Register](https://www.federalregister.gov/) using natural language. It uses a **local LLM (Ollama)** with tool/function calls to access **MySQL** and optional **Vector DB (Chroma)**, ensuring data is updated **daily** via a fully automated pipeline.

---

## 🧱 Architecture & Stack

- **Backend**: `FastAPI`, `aiohttp`, `aiomysql`, async tool execution
- **LLM**: Local Mistral:7b via **Ollama**
- **Data Source**: [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1)
- **Data Pipeline**: Raw JSON → Cleaned → MySQL (indexed)
- **Frontend**: Simple `HTML + CSS + JS` (WebSocket-based chat)
- **VectorDB (optional)**: ChromaDB for embedding-based queries

---

![Image](https://github.com/user-attachments/assets/e5cbd9c9-892f-4bd5-ac2d-78338af1b355)


## Data Pipeline

- Downloads daily updated Federal Register data via API
- Processes raw JSON data to extract relevant fields
- Loads data into MySQL with proper indexing for quick queries
- Supports data refresh by running `data_pipeline/pipeline.py`
- Keeps at least one week of data history for consistency

---

## Agent System

- Core in `agent/core.py` orchestrates tool/function calls
- Tools defined in `agent/tools.py` include:
  - `sql_search`: raw SQL queries to MySQL for specific data retrieval
  - `vector_search`: conceptual/broad queries using vector embeddings (Chroma DB)
- Uses OpenAI Async API client pointing to local Ollama base URL
- Implements a system prompt to guide tool usage and results summarization
- Tool calls handled asynchronously and results injected back to LLM context

---

## API & WebSocket Interface

- FastAPI backend in `api/main.py`
- WebSocket chat endpoint in `api/websockets.py`
- Dependency injection for DB connections in `api/dependencies.py`
- Serves frontend from `frontend/` directory as static files

---

## Frontend

- Simple HTML page with input box and result display (`frontend/index.html`)
- Minimal CSS and JS for interaction and WebSocket communication

---

## Challenges & Solutions

- **Asynchronous tool execution:** Implemented async handling of LLM tool calls and DB queries using `asyncio` and `aiomysql`
- **Local LLM integration:** Configured OpenAI Python client to use Ollama local API, handled function call schema parsing
- **Daily data updating:** Automated pipeline to fetch, process, and load daily Federal Register data with minimal manual intervention
- **Avoiding ORMs:** Used raw SQL queries for simplicity and control as per requirements

---

## Running Locally

1. Clone the repo:

```bash
git clone https://github.com/AkashDevelop/RAG_Agentic_System_using_ollama_mistral_7b
cd fedreg_rag

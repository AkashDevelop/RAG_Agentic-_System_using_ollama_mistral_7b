# FedReg RAG Agentic System

## Project Overview

This project implements a **User-facing Retrieval-Augmented Generation (RAG) Agentic System** for querying US Federal Register regulations and executive documents. The system uses a local LLM (via Ollama) with asynchronous tool/function calls to MySQL and vector DBs for data retrieval.

---

## Architecture & Tech Stack

- **Backend**: Python 3, FastAPI (with WebSocket chat interface)
- **Local LLM**: Ollama (Qwen2.5 0.5b or 1b model)
- **Data Storage**: MySQL (daily updated via data pipeline), Vector DB (Chroma, optional)
- **Data Pipeline**: Scheduled daily download, processing, and DB load from Federal Register API
- **Frontend**: Basic HTML/CSS/JS chat interface
- **Async Programming**: aiohttp, aiomysql, FastAPI async endpoints for non-blocking UX

---

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

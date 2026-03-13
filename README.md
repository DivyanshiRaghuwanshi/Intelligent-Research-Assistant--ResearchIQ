# ResearchIQ — AI Research Assistant

An intelligent research chatbot built for the NeoStats AI Engineer Case Study.

## Features

- **RAG (Retrieval-Augmented Generation)** — Upload PDF, TXT, or DOCX files and ask questions. Uses FAISS vector search with `all-MiniLM-L6-v2` embeddings, KNN top-k=7 retrieval.
- **Live Web Search** — Real-time Google search via Serper API for current information.
- **Concise / Detailed response modes** — Toggle between short answers and comprehensive multi-section explanations.
- **Multi-provider LLM support** — Switch between OpenAI (gpt-4o-mini), Groq (llama-3.1-8b-instant), and Gemini (gemini-1.5-flash).
- **Session memory** — Conversation history preserved per session using LangGraph InMemorySaver.
- **Search mode toggles** — Enable/disable RAG and web search independently.

## Architecture

```
User Query
    │
    ▼
LangGraph ReAct Agent (create_react_agent)
    ├── get_answer tool  →  FAISS KNN search  →  Retrieval LLM (temp=0)
    └── search_web tool  →  Serper API
    │
    ▼
Response LLM (temp=0.3)  →  Final Answer
```

## Tech Stack

- **LangGraph** `create_react_agent` with `MemorySaver` checkpointer
- **LangChain** tools, loaders, text splitters
- **FAISS** vector store for document embeddings
- **HuggingFace** `all-MiniLM-L6-v2` for local embeddings
- **Streamlit** for the UI
- **Serper API** for web search

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/researchiq-chatbot.git
cd researchiq-chatbot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add API keys
# Create .streamlit/secrets.toml with:
# GROQ_API_KEY    = "..."
# OPENAI_API_KEY  = "..."
# GEMINI_API_KEY  = "..."
# SERPER_API_KEY  = "..."

# 5. Run
streamlit run app.py
```

## Deployment

Deployed on Streamlit Cloud. API keys are configured via Streamlit Cloud Secrets (never committed to the repo).

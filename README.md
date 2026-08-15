# 🤖 Enterprise AI Support Agent

An enterprise-style AI support application built using **Python, LangChain, OpenAI, RAG, FAISS, FastAPI, and Streamlit**.

The application provides an AI-powered IT support experience that can troubleshoot common IT issues using an enterprise knowledge base, look up existing support tickets, create new support tickets, maintain conversation context, and expose the agent through APIs and a web UI.

---

## 🚀 Features

- 🤖 LangChain-based AI Agent
- 📚 Retrieval-Augmented Generation (RAG)
- 🔎 FAISS vector similarity search
- 🧠 OpenAI embeddings
- 📄 Enterprise IT knowledge base
- 🔧 Tool-based Agent architecture
- 🎫 Support ticket lookup
- 🎫 Support ticket creation
- 🆔 Automatic ticket ID generation
- 📊 Ticket status and priority
- 🧠 Conversation memory
- 🌐 FastAPI API layer
- 🖥️ Single-page Streamlit UI
- 📈 Monitoring and logging
- 🧪 Unit and integration testing
- 🔐 Environment-variable-based API configuration

---

# 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │   Streamlit UI    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │    AI AGENT       │
                 │     LangChain     │
                 └─────────┬─────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          RAG Search   Ticket Lookup  Create Ticket
              │            │            │
              ▼            └──────┬─────┘
          Retriever               │
              │                   │
              ▼                   ▼
             FAISS          Ticket Store
              │
              ▼
      Enterprise Documents
              │
              ▼
             LLM
              │
              ▼
       Grounded Response
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
- 🔒 Enterprise knowledge-base scope enforcement
- 🚫 Out-of-scope question protection
- 🎫 Ticket lifecycle management
- 📋 List and retrieve support tickets
- 🔄 Open ticket count tracking

---

## 🏗️ Architecture

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
```

---

## 📚 RAG Pipeline

The application uses Retrieval-Augmented Generation to provide answers based on enterprise documentation.

```text
Enterprise Documents
        ↓
Document Loading
        ↓
Text Chunking
        ↓
OpenAI Embeddings
        ↓
FAISS Vector Store
        ↓
Retriever
        ↓
Relevant Context
        ↓
LLM
        ↓
Grounded Response
```

The current enterprise knowledge base contains information for:

- VPN troubleshooting
- Password reset
- Laptop troubleshooting
- Email configuration

---

## 🎫 Ticket Management

The AI Agent supports a complete support-ticket lifecycle.

### Ticket Operations

- Create a new support ticket
- Automatically generate ticket IDs
- Look up a specific ticket
- List all raised tickets
- Close an existing ticket
- Track the number of currently open tickets

### Ticket Lifecycle

User requests ticket
        ↓
create_ticket()
        ↓
INC004
        ↓
Status: Open
        ↓
close_ticket()
        ↓
Status: Closed

The ticket ID counter continuously increases:

INC004 → INC005 → INC006 → INC007

The open-ticket count behaves independently:

2 → Create → 3 → Close → 2

### Ticket Retrieval

If the user provides a specific ticket ID:

    "What is the status of INC004?"

The Agent uses:

    lookup_ticket()

If the user asks for all tickets:

    "Show my tickets"

The Agent uses:

    list_tickets()

### Current Implementation

Tickets are currently stored in an in-memory Python dictionary for demonstration and learning purposes.

Therefore, ticket information and the ticket counter reset when the application restarts.

A production implementation can replace the in-memory store with:

- PostgreSQL
- Amazon RDS
- DynamoDB
- ServiceNow
- Enterprise ITSM platform
```

Because the current implementation is in-memory, newly created tickets are not persistent across application restarts.

A production implementation can replace this with:

- PostgreSQL
- Amazon RDS
- DynamoDB
- Enterprise ITSM platform
- ServiceNow

---

## 🖥️ Streamlit UI

The project includes a clean, single-page Streamlit interface.

The UI provides:

- Enterprise-style interface
- AI Agent status
- IT issue quick actions
- Interactive chat
- AI responses
- Enterprise knowledge indication
- Ticket interaction

Application flow:

```text
User
 ↓
Streamlit UI
 ↓
AI Agent
 ↓
RAG / Tools / Memory
 ↓
LLM
 ↓
Response
 ↓
Streamlit UI
```

---

## 🌐 FastAPI

The project also includes a FastAPI API layer for exposing the AI functionality through HTTP APIs.

This provides a foundation for integrating the Agent with:

- Web applications
- Enterprise applications
- Backend services
- Future frontend applications

---

## 🧪 Testing

The project includes tests for the major components.

### Tools

```powershell
python -m enterprise_agent.tests.test_tools
```

### Document Loading

```powershell
python -m enterprise_agent.tests.test_loader
```

### Embeddings

```powershell
python -m enterprise_agent.tests.test_embeddings
```

### Vector Store

```powershell
python -m enterprise_agent.tests.test_vectorstore
```

### Retriever

```powershell
python -m enterprise_agent.tests.test_retriever
```

### RAG

```powershell
python -m enterprise_agent.tests.test_rag
```

### RAG Agent

```powershell
python -m enterprise_agent.tests.test_rag_agent
```

### Agent Integration

```powershell
python -m enterprise_agent.tests.test_agent
```

### Monitoring

```powershell
python -m enterprise_agent.tests.test_monitoring
```

---

## 📁 Project Structure

```text
Enterprise-AI-Support-Agent/
│
├── enterprise_agent/
│   │
│   ├── agent.py
│   ├── api.py
│   ├── config.py
│   ├── logging_config.py
│   ├── main.py
│   ├── memory.py
│   ├── monitoring.py
│   ├── tools.py
│   ├── ui.py
│   │
│   ├── rag/
│   │   ├── documents/
│   │   │   └── it_support.txt
│   │   ├── embeddings.py
│   │   ├── loader.py
│   │   ├── rag_chain.py
│   │   ├── retriever.py
│   │   ├── splitter.py
│   │   └── vectorstore.py
│   │
│   └── tests/
│       ├── test_agent.py
│       ├── test_embeddings.py
│       ├── test_loader.py
│       ├── test_monitoring.py
│       ├── test_rag.py
│       ├── test_rag_agent.py
│       ├── test_retriever.py
│       ├── test_splitter.py
│       ├── test_tools.py
│       └── test_vectorstore.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | Agent orchestration |
| OpenAI | LLM and embeddings |
| FAISS | Vector similarity search |
| FastAPI | API layer |
| Streamlit | Web UI |
| Pydantic | Data validation |
| python-dotenv | Environment configuration |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/v1i1n1/Enterprise-AI-Support-Agent.git
cd Enterprise-AI-Support-Agent
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
```

Never commit the `.env` file to GitHub.

---

## ▶️ Run the AI Agent

From the project root:

```powershell
python -m enterprise_agent.main
```

---

## 🖥️ Run the Streamlit UI

```powershell
python -m streamlit run enterprise_agent/ui.py
```

Then open:

```text
http://localhost:8501
```

---

## 🔄 Example Workflow

### VPN Troubleshooting

```text
User
 ↓
"My corporate VPN is not connecting."
 ↓
AI Agent
 ↓
RAG Knowledge Base
 ↓
FAISS Retriever
 ↓
VPN Documentation
 ↓
LLM
 ↓
Grounded Troubleshooting Response
```

If the troubleshooting steps do not resolve the issue:

```text
User
 ↓
"I tried everything. Please create a ticket."
 ↓
AI Agent
 ↓
create_ticket()
 ↓
INC004
 ↓
Ticket Created
```

---

## 🧠 Agent Tool Selection

The Agent dynamically selects tools based on the user's request.

### Ticket Lookup

```text
Ticket ID provided
        ↓
lookup_ticket()
```

### Enterprise IT Troubleshooting

```text
Enterprise IT troubleshooting
        ↓
search_rag_knowledge_base()
```

### Ticket Creation

```text
Issue unresolved / ticket requested
        ↓
create_ticket()
```

This allows the application to combine **LLM reasoning with deterministic tools**.

---

## 📈 Monitoring

The project includes basic request monitoring.

Tracked metrics include:

```text
Total Requests
Successful Requests
Failed Requests
Average Response Time
```

This provides a foundation for future production observability.

---

## 🔐 Security

Sensitive configuration is stored using environment variables.

The following files are excluded from Git:

```text
.env
venv/
*.db
*.db-shm
*.db-wal
__pycache__/
```

API keys and credentials should never be committed to source control.

---

## 🚀 Future Improvements

- Persistent ticket database
- PostgreSQL integration
- Production vector database
- Advanced RAG evaluation
- RAG source citations
- Streaming responses
- Cloud deployment
- Enterprise ITSM integration
- Document upload functionality
- Multi-user conversation management
- Advanced observability
- Role-based access control
- Authentication and authorization
- Vision-enabled AI workflows

---

## 🎯 Project Goal

The goal of this project is to demonstrate how an enterprise-oriented Generative AI application can combine:

**LLMs + Agents + Tools + RAG + Vector Search + Memory + APIs + UI**

to solve practical IT support use cases.

---

## 👨‍💻 Author

**Vinod Raj**

GitHub:

https://github.com/v1i1n1
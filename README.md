# 💪 FitTrack AI

## FastAPI + Streamlit + ChromaDB + Ollama + Docker Compose + GitHub Actions + RAG

A complete AI-powered fitness tracking application built with:

- FastAPI
- Streamlit
- ChromaDB
- Ollama
- Sentence Transformers
- SQLite
- JWT Authentication
- Docker Compose
- GitHub Actions
- Pytest

FitTrack AI combines fitness tracking, workout logging, and Retrieval-Augmented Generation (RAG) to deliver personalized fitness recommendations grounded in a curated fitness knowledge base.

Repository:

```text
https://github.com/EberhardtG/FitTrack-AI
```

---

# 🚀 Features

## Backend (FastAPI)

### Fitness Features

- User registration
- JWT authentication
- Weight tracking
- Workout logging
- Personalized recommendations
- Protected API routes

### RAG Features

- Fitness document ingestion
- Semantic retrieval
- ChromaDB vector storage
- Sentence Transformer embeddings
- Personalized context building
- Source citations
- Ollama response generation
- Document re-indexing

---

## Frontend (Streamlit)

- Multi-page dashboard
- User authentication
- Weight management
- Workout logging
- AI Workout Assistant
- Session State management
- Settings page
- Re-index functionality

---

## Infrastructure

- Dockerized backend
- Dockerized frontend
- Ollama container
- ChromaDB persistent storage
- SQLite database
- Environment-based configuration
- GitHub Actions CI workflow

---

# 📁 Project Structure

```text
FitTrack-AI/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── backend/
│   ├── Dockerfile
│   ├── app.db
│   └── app/
│
├── frontend/
│   ├── Dockerfile
│   ├── streamlit_app.py
│   ├── pages/
│   ├── components/
│   └── utils/
│
└── README.md
```

---

# 📚 Fitness Knowledge Base

The Workout Assistant uses a fitness-specific document corpus located in:

```text
backend/app/rag/data/raw_docs/
```

Current topics include:

- Chest Training
- Back Training
- Leg Training
- Recovery
- Weight Loss
- Muscle Gain
- Cardio
- HIIT
- Mobility
- Home Workouts
- Progressive Overload
- Joint Friendly Training
- Workout Consistency
- Strength Training

Documents are:

- Loaded from disk
- Chunked into retrievable sections
- Embedded using Sentence Transformers
- Stored in ChromaDB
- Retrieved through semantic search

---

# ⚙️ Configuration

Example configuration:

```env
OLLAMA_MODEL=llama3.2:1b

CHROMA_PATH=./chroma_db

RAW_DOCS_DIR=app/rag/data/raw_docs

PROCESSED_DOCS_DIR=app/rag/data/processed_docs

CHUNKS_JSON_PATH=app/rag/data/processed_docs/chunks.json
```

---

## Environment Security

The repository includes:

```text
.gitignore
```

which excludes:

```text
.env
.venv/
__pycache__/
chroma_db/
```

preventing sensitive and generated files from being committed.

---

# 🔍 RAG Pipeline

## Step 1: Ingestion

Fitness documents are loaded from:

```text
backend/app/rag/data/raw_docs/
```

Documents are:

- Loaded
- Chunked
- Embedded
- Stored in ChromaDB

---

## Step 2: Retrieval

When a user submits a question:

1. The question is converted into an embedding.
2. ChromaDB performs semantic search.
3. Relevant fitness documents are retrieved.
4. Retrieved context is passed into the prompt.

---

## Step 3: Context Building

The backend combines:

```text
Weight History
+
Workout Logs
+
Retrieved Documents
```

to create personalized recommendations.

---

## Step 4: Generation

The assembled context is sent to:

```text
Ollama
Model: llama3.2:1b
```

to generate recommendations.

---

# 🛡️ Guardrails

The Workout Assistant focuses on:

- Fitness
- Exercise
- Recovery
- Nutrition
- Strength Training
- Weight Management

Example:

```text
What is the Super Bowl?
```

Response:

```text
Please ask a fitness-related question.
```

Responses are grounded in retrieved fitness documents rather than relying solely on model memory.

---

# 🔌 API Endpoints

| Endpoint             | Method | Description             |
| -------------------- | ------ | ----------------------- |
| `/auth/register`     | POST   | Register user           |
| `/auth/token`        | POST   | Login                   |
| `/auth/me`           | GET    | Current user            |
| `/weights`           | GET    | Retrieve weight entries |
| `/weights`           | POST   | Add weight              |
| `/weights/{id}`      | DELETE | Delete weight           |
| `/workout_logs`      | GET    | Retrieve workout logs   |
| `/workout_logs`      | POST   | Create workout log      |
| `/workout_logs/{id}` | PATCH  | Update workout log      |
| `/workout_logs/{id}` | DELETE | Delete workout log      |
| `/workouts/ask`      | POST   | Ask Workout Assistant   |
| `/rag/reindex`       | POST   | Rebuild vector database |

---

# 🧪 Testing

Automated tests are located in:

```text
backend/app/tests/
```

Coverage includes:

- Authentication
- Weight Tracking
- Workout Logging
- Workout Assistant
- Health Checks

Run tests:

```bash
cd backend

pytest
```

---

# 🐳 Docker Architecture

## Backend

Technology:

```text
FastAPI
SQLite
ChromaDB
Sentence Transformers
```

Port:

```text
8000
```

---

## Frontend

Technology:

```text
Streamlit
```

Port:

```text
8501
```

---

## Ollama

Technology:

```text
llama3.2:1b
```

Port:

```text
11434
```

---

# ✅ Continuous Integration

GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

Automated tasks:

- Backend testing with Pytest
- Backend Docker build validation
- Frontend Docker build validation
- Pull request verification

Workflow:

```text
Push to GitHub
        │
        ▼
GitHub Actions
        │
        ├── Run Pytest
        │
        ├── Build Backend
        │
        └── Build Frontend
```

---

# 🚀 Setup Instructions

Clone the repository:

```bash
git clone https://github.com/EberhardtG/FitTrack-AI.git

cd FitTrack-AI
```

Configure environment variables:

```text
backend/.env
```

using:

```text
.env.example
```

Pull the Ollama model:

```bash
ollama pull llama3.2:1b
```

Start the application:

```bash
docker compose up --build
```

---

# 📖 Usage

## Weight Tracking

- Add weight entries
- View weight history
- Monitor weight trends

## Workout Logging

- Record workouts
- Track duration
- Track calories burned

## Workout Assistant

Example questions:

```text
What is a good chest workout?
```

```text
How can I improve recovery after leg day?
```

```text
What are effective weight loss strategies?
```

## Re-Index Documents

Navigate to:

```text
Settings
```

Select:

```text
🔄 Re-Index Documents
```

to rebuild embeddings and update the fitness knowledge base.

---

# 🔮 Future Improvements

- Conversational memory
- Retrieval re-ranking
- Streaming AI responses
- Advanced fitness analytics
- Goal tracking
- Cloud deployment
- Mobile companion application

---

# 🎓 Lessons Learned

This project demonstrates:

- Retrieval-Augmented Generation
- Semantic Search
- FastAPI Development
- Streamlit Development
- ChromaDB Vector Databases
- Ollama Integration
- Docker Compose Orchestration
- JWT Authentication
- CRUD Application Design
- GitHub Actions CI
- Automated Testing Pipelines
- Source-Grounded AI Responses

---

# 👨‍💻 Author

Grant Eberhardt

GitHub:

```text
https://github.com/EberhardtG/FitTrack-AI
```

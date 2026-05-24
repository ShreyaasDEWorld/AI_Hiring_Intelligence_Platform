# 📄 AI Hiring Intelligence Platform

An AI-powered Resume Screening & Candidate Intelligence Platform built using:

- OpenAI GPT
- LangChain
- ChromaDB
- Streamlit
- Vector Embeddings
- Resume Parsing
- Semantic Search Architecture

This application allows recruiters or hiring teams to upload resumes, compare them against job requirements, generate AI-powered screening reports, and store resume embeddings in ChromaDB for future semantic retrieval and intelligent hiring workflows.

---

# 🚀 Features

## ✅ Resume Upload Support

Supports:
- PDF
- DOCX
- TXT

---

## ✅ Resume Parsing

Extracts text from uploaded resumes automatically.

---

## ✅ OpenAI GPT-Powered Screening

Uses OpenAI GPT models to:
- Analyze candidate fit
- Match skills
- Identify gaps
- Generate HR recommendations
- Suggest interview questions

---

## ✅ Token Usage Tracking

Tracks:
- Resume tokens
- Job description tokens
- Total token usage

Useful for:
- OpenAI cost estimation
- Prompt optimization
- Token limit management

---

## ✅ ChromaDB Vector Storage

Stores resume embeddings into ChromaDB.

Enables:
- Semantic search
- Retrieval-Augmented Generation (RAG)
- Future candidate matching
- AI memory systems

---

## ✅ Semantic Chunking

Large resumes are automatically split into chunks before embedding.

---

## ✅ Downloadable AI Reports

Generate and download AI-generated screening reports.

---

# 🏗️ Architecture

```text
Resume Upload
      ↓
Resume Parsing
      ↓
Text Chunking
      ↓
OpenAI Embeddings
      ↓
ChromaDB Vector Store
      ↓
OpenAI GPT Analysis
      ↓
AI Screening Report


🛠️ Tech Stack
Technology	Purpose
Python	Backend
Streamlit	UI
OpenAI GPT	LLM
LangChain	AI orchestration
ChromaDB	Vector database
OpenAI Embeddings	Semantic embeddings
tiktoken	Token counting
PyPDF	PDF parsing
python-docx	DOCX parsing
📦 Installation
1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/AI_Hiring_Intelligence_Platform.git

cd AI_Hiring_Intelligence_Platform
2️⃣ Create Virtual Environment
Windows
python -m venv venv

venv\Scripts\activate
Linux / Mac
python3 -m venv venv

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file:

OPENAI_API_KEY=your_openai_api_key

Get API key from:

https://platform.openai.com/api-keys

▶️ Run Application
streamlit run app.py

Application runs at:

http://localhost:8501
📁 Project Structure
AI_Hiring_Intelligence_Platform/
│
├── app.py
├── requirements.txt
├── .env
├── chroma_db/
├── README.md
│
└── venv/
🧠 Future Enhancements

Planned features:

Multi-resume comparison
Candidate ranking
Semantic resume search
ATS scoring
AI recruiter agents
Resume similarity matching
Interview copilot
Hiring analytics dashboard
PostgreSQL integration
RAG-based hiring workflows
LangGraph multi-agent pipelines
🚀 Example Use Cases
AI Resume Screening
HR Automation
Candidate Intelligence
AI Recruitment Workflows
Semantic Resume Search
Talent Discovery
Hiring Recommendation Systems
📊 Token Tracking

The platform estimates OpenAI token usage for:

Resume input
Job descriptions
Total prompt size

Helps optimize:

API costs
Prompt engineering
Context window management
🧠 AI Architecture Concepts Used
LLM Applications
Retrieval-Augmented Generation (RAG)
Vector Databases
Embeddings
Semantic Search
Prompt Engineering
AI Orchestration
Resume Intelligence Systems
🔒 Security Notes
Never commit .env files
Keep API keys private
Add .env to .gitignore
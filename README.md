📘 BOG Meeting RAG-Based Ordinance Chatbot

A Retrieval-Augmented Generation (RAG) powered chatbot designed to answer queries related to Board of Governors (BOG) meeting ordinances, summaries, and institutional documents.
The system uses vector embeddings, graph-based knowledge representation, and LLM-powered reasoning to provide accurate, citation-backed responses.

📁 Project Structure
BOG_MEETING_CHATBOT/
│
├── logs/                         # System logs & debug files
├── summaries/                    # Generated summaries of ordinances/BOG documents
├── vector_store/                 # Saved embeddings & vector index
│
├── chatbot_ui.py                 # Chat UI (Streamlit/Gradio) for user interaction
├── create_graph_database.py      # Creates graph/knowledge DB (Neo4j / NetworkX)
├── create_vector_embedding.py    # PDF/text chunking + embedding creation pipeline
│
├── rag_query_handler.py          # Main RAG pipeline (retrieval + generation)
├── rag_debug.log                 # Debug logs for RAG pipeline
├── debug.log                     # General system logs
│
├── Pipfile                       # Pipenv environment file
├── Pipfile.lock                  # Pipenv lock
├── requirement.txt               # Requirements for pip users
├── .gitignore                    # Git ignored paths
└── README.md                     # Project documentation

🚀 Features
🔍 Hybrid RAG Pipeline

Dense vector search (via embeddings)

Optional graph-based retrieval (relations between entities)

Combined context fed to LLM for grounded answers

🧠 LLM-Driven Response Generation

Uses Groq/OpenAI/Llama models (depending on configuration):

Generates precise answers

Includes fallback logic for unclear queries

Avoids hallucination by grounding responses in documents

📄 Document Processing

Processes BOG meeting ordinances

Summarizes key sections

Converts PDF → text → chunks → embeddings

💬 Interactive Chat Interface

Simple UI (Streamlit or Gradio)

User query history

Debug info (optional)

⚙️ Installation
1. Clone the repository
git clone https://github.com/<your-username>/BOG_MEETING_CHATBOT.git
cd BOG_MEETING_CHATBOT

2. Install dependencies
Using Pip:
pip install -r requirement.txt

OR using Pipenv:
pipenv install
pipenv shell

🔑 Environment Variables

Create a .env in the project root:

GROQ_API_KEY=your_api_key_here
OPENAI_API_KEY=your_optional_openai_key


Never hard-code API keys inside Python files.

🏗️ Setup: Build Vector Embeddings

Before running the chatbot, generate embeddings:

python create_vector_embedding.py


This will:

✔ Load PDFs / text
✔ Chunk data
✔ Create embeddings
✔ Save them in vector_store/

🧪 Optional: Build Graph Knowledge Base

Run this only if you're using graph-augmented RAG:

python create_graph_database.py

▶️ Run the Chatbot UI
python chatbot_ui.py


Then open the local URL (e.g., http://localhost:8501).

🧠 How RAG Works in This Project

User enters a query.

System retrieves top relevant chunks from vector_store.

Graph DB supplements data with relationships if enabled.

LLM generates an answer grounded in retrieved info.

System logs detailed steps in rag_debug.log.

📚 Use Cases

Query BOG meeting ordinances

Understand rules, decisions, and resolutions

Summaries of past meeting notes

Assist administration, students, and faculty

⭐ Future Enhancements

Web deployment (Vercel/Render)

Improved summarizer using Llama/Groq large models

Admin panel for uploading new meeting documents

SQL vector store integration

Chat history memory

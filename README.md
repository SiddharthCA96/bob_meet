📘 BOG Meeting RAG-Based Ordinance Chatbot

A Retrieval-Augmented Generation (RAG) powered chatbot designed to answer queries related to Board of Governors (BOG) meeting ordinances, summaries, and institutional documents. The system uses vector embeddings, graph-based knowledge representation, and LLM-powered reasoning to provide accurate, citation-backed responses.

📁 Project Structure
BOG_MEETING_CHATBOT/
│
├── logs/                       # System logs & debug files
├── summaries/                  # Generated summaries of ordinances/BOG documents
├── vector_store/               # Saved embeddings & vector index
│
├── chatbot_ui.py               # Chat UI (Streamlit/Gradio) for interaction
├── create_graph_database.py    # Creates graph/knowledge DB (Neo4j / NetworkX)
├── create_vector_embedding.py  # PDF/text chunking + embedding creation pipeline
├── rag_query_handler.py        # Main RAG pipeline (retrieval + generation)
│
├── rag_debug.log               # Debug logs for RAG pipeline
├── debug.log                   # General system logs
│
├── Pipfile                     # Pipenv environment file
├── Pipfile.lock                # Pipenv lock
├── requirement.txt             # Requirements for pip users
├── .gitignore                  # Git ignored paths
└── README.md                   # Project documentation

🚀 Features

🔍 Hybrid RAG Pipeline using embeddings + graph retrieval

🧠 LLM-based generation grounded in retrieved context

📄 PDF/text processing for ordinance documents

💬 Interactive UI for end-user querying

🧱 Modular architecture for easy scaling

⚙️ Installation
Clone the repository
git clone https://github.com/<your-username>/BOG_MEETING_CHATBOT.git
cd BOG_MEETING_CHATBOT

Install dependencies (Pip)
pip install -r requirement.txt


Or using Pipenv:

pipenv install
pipenv shell

🔑 Environment Variables

Create a .env file:

GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=optional_openai_key

🏗️ Generate Vector Embeddings
python create_vector_embedding.py

🧪 (Optional) Build Graph Database
python create_graph_database.py

▶️ Run the Chatbot UI
python chatbot_ui.py


Open the generated local URL (e.g., http://localhost:8501).

🧠 How It Works

User enters a query

System retrieves top relevant chunks from vector_store

(Optional) Graph DB augments relational info

LLM generates a grounded answer

Logs saved for debugging

📚 Use Cases

Query BOG meeting ordinances

Summaries of institutional documents

Understand decisions, rules, processes

Assist faculty, students, administration

⭐ Future Enhancements

Web deployment

Admin UI for uploading new documents

SQL/Redis vector stores

Better summarization models

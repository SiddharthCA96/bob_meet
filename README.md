BOG Meeting RAG-Based Ordinance Chatbot
=======================================

A Retrieval-Augmented Generation (RAG) powered chatbot designed to answer queries related to Board of Governors (BOG) meeting ordinances, summaries, and institutional documents.  
The system uses vector embeddings, graph-based knowledge representation, and LLM-powered reasoning to provide accurate, citation-backed responses.

Project Structure
-----------------

BOG_MEETING_CHATBOT/
|
├── logs/                       # System logs & debug files
├── summaries/                  # Generated summaries of documents
├── vector_store/               # Saved embeddings & vector index
|
├── chatbot_ui.py               # Chat UI (Streamlit/Gradio)
├── create_graph_database.py    # Builds graph/knowledge DB
├── create_vector_embedding.py  # Embedding creation pipeline
├── rag_query_handler.py        # Main RAG pipeline
|
├── rag_debug.log               # Debug logs for RAG
├── debug.log                   # General system logs
|
├── Pipfile                     # Pipenv environment
├── Pipfile.lock
├── requirement.txt             # Python dependencies
├── .gitignore                  # Ignored files
└── README.md                   # Project documentation

Features
--------

- Hybrid RAG Pipeline using embeddings + graph retrieval  
- LLM-based generation grounded in retrieved context  
- PDF/Text processing for ordinance documents  
- Interactive UI for end-user querying  
- Modular architecture for easy scaling  

Installation
------------

1. Clone the repository:

   git clone https://github.com/<your-username>/BOG_MEETING_CHATBOT.git
   cd BOG_MEETING_CHATBOT

2. Install dependencies (Pip):

   pip install -r requirement.txt

   Or using Pipenv:

   pipenv install
   pipenv shell

Environment Variables
---------------------

Create a `.env` file:

GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=optional_openai_key

Generate Vector Embeddings
--------------------------

python create_vector_embedding.py

(Optional) Build Graph Knowledge Base
-------------------------------------

python create_graph_database.py

Run the Chatbot UI
------------------

python chatbot_ui.py

Use Cases
---------

- Query BOG meeting ordinances  
- Summaries of institutional documents  
- Understand decisions, rules, and resolutions  
- Assist faculty, students, and administrators  

License
-------

MIT License

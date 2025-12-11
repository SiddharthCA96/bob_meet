import os
import re

from groq import Groq
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


class TextRAGHandler:
    def __init__(self, vector_store_dir="vector_store", groq_api_key="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", model_name="meta-llama/llama-4-scout-17b-16e-instruct"):
        self.vector_store_dir = vector_store_dir
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            encode_kwargs={"normalize_embeddings": True}
        )
        self.vector_stores = {}
        self.GROQ_API_KEY = groq_api_key
        self.MODEL_NAME = model_name
        self.groq_client = Groq(api_key=self.GROQ_API_KEY)

        if not self.GROQ_API_KEY:
            raise ValueError("Groq API key missing. Please pass it as a string in the code.")

        self._load_all_vector_stores()

    def _load_all_vector_stores(self):
        print("[INFO] Loading vector stores...")
        self.vector_stores.clear()

        if not os.path.exists(self.vector_store_dir):
            print(f"[WARNING] Directory '{self.vector_store_dir}' does not exist.")
            return

        for folder_name in os.listdir(self.vector_store_dir):
            subfolder_path = os.path.join(self.vector_store_dir, folder_name)
            if os.path.isdir(subfolder_path):
                try:
                    db = FAISS.load_local(subfolder_path, embeddings=self.embedding_model, allow_dangerous_deserialization=True)
                    self.vector_stores[folder_name] = db
                    print(f"[OK] Loaded vector DB: {folder_name}")
                except Exception as e:
                    print(f"[ERROR] Failed to load {folder_name}: {e}")
        print(f"[INFO] Vector stores available: {list(self.vector_stores.keys())}")

    def _query_groq_ai(self, messages: list) -> str:
        try:
            response = self.groq_client.chat.completions.create(
                messages=messages,
                model=self.MODEL_NAME,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.9,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"System error: {str(e)}"

    def _generate_amplified_query(self, query: str, num_variations: int = 3) -> str:
        prompt = [
            {
                "role": "system",
                "content": (
                    "You are an assistant enhancing queries for better retrieval from a vector database. "
                    "Extract named entities such as BoG numbers, item numbers, names, years, etc., and generate "
                    "an amplified version of the query that repeats those terms in different factual phrasings. "
                    "Do not make things up. Your output should be a single expanded query containing multiple versions "
                    "of the original query phrasing the same key terms in different ways."
                )
            },
            {
                "role": "user",
                "content": f"Original user query: '{query}'\n\nGenerate a single amplified query with {num_variations} variations merged together."
            }
        ]
        response = self._query_groq_ai(prompt)
        if response and not response.startswith("System error:"):
            return response.strip()
        return query

    def _extract_bog_folders_from_query(self, query: str):
        folder_names = list(self.vector_stores.keys())
        detected = set()

        bog_range_matches = re.findall(r"\bBoG\s*(\d{1,3})\s*(?:to|-)\s*(\d{1,3})\b", query, flags=re.IGNORECASE)
        bog_single_matches = re.findall(r"\bBoG\s*(\d{1,3})\b", query, flags=re.IGNORECASE)

        year_range_matches = re.findall(r"\b(20\d{2})\s*(?:to|-)\s*(20\d{2})\b", query)
        year_single_matches = re.findall(r"\b(20\d{2})\b", query)

        folder_map_by_bog = {}
        folder_map_by_year = {}

        for folder in folder_names:
            bog_match = re.search(r'(\d{1,3})', folder)
            year_match = re.search(r'(20\d{2})', folder)

            if bog_match:
                bog_num = int(bog_match.group(1))
                folder_map_by_bog.setdefault(bog_num, []).append(folder)

            if year_match:
                year = int(year_match.group(1))
                folder_map_by_year.setdefault(year, []).append(folder)

        for start, end in bog_range_matches:
            for bog_num in range(int(start), int(end) + 1):
                detected.update(folder_map_by_bog.get(bog_num, []))

        for bog_str in bog_single_matches:
            bog_num = int(bog_str)
            detected.update(folder_map_by_bog.get(bog_num, []))

        for start, end in year_range_matches:
            for year in range(int(start), int(end) + 1):
                detected.update(folder_map_by_year.get(year, []))

        for year_str in year_single_matches:
            year = int(year_str)
            detected.update(folder_map_by_year.get(year, []))

        if not detected:
            print("[INFO] No BoG or year found. Using fallback 'db_faiss' vector store.")
            if "db_faiss" in self.vector_stores:
                return ["db_faiss"], True
            else:
                raise ValueError("[ERROR] No matching folders found and fallback 'db_faiss' does not exist.")

        print(f"[INFO] Matched folders from query: {list(detected)}")
        return list(detected), False

    def _query_with_context(self, query: str, context: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer user questions based only on the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nUser Query:\n{query}\n\nAnswer the question based on the context above."
            }
        ]
        response = self._query_groq_ai(messages)
        if not response:
            return "[ERROR] No response from Groq AI."
        if response.startswith("System error:"):
            return response
        return response

    def handle_input(self, query: str, top_k: int = 5) -> str:
        self._load_all_vector_stores()

        try:
            store_keys, is_fallback = self._extract_bog_folders_from_query(query)
        except ValueError as ve:
            return str(ve)

        amplified_query = self._generate_amplified_query(query)
        print(f"[INFO] Amplified Query:\n{amplified_query}")
        print(f"[INFO] Using vector stores: {store_keys}")

        candidate_docs = []
        for store_key in store_keys:
            docs = self.vector_stores[store_key].similarity_search(amplified_query, k=top_k)
            for doc in docs:
                doc.metadata["source_folder"] = store_key
                candidate_docs.append(doc)

        if not candidate_docs:
            return "[WARNING] No relevant context found in the selected documents."

        print(f"[INFO] Top {len(candidate_docs)} Retrieved Chunks:\n")
        for i, doc in enumerate(candidate_docs, 1):
            print(f"#{i} [Source: {doc.metadata.get('source_folder', 'unknown')}]:\n{doc.page_content[:300]}...\n{'-'*60}")

        combined_context = "\n\n".join(doc.page_content for doc in candidate_docs)
        return self._query_with_context(query, combined_context)
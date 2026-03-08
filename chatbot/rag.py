"""
FSA Navigator — RAG engine
Handles document ingestion, embedding, retrieval, and answer generation.
"""

import os
import json
import hashlib
from typing import List, Dict, Any
from google import genai
from dotenv import load_dotenv
from groq import Groq


# Load environment variables from .env file
load_dotenv()

# --- Optional deps with helpful errors ---
try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    raise ImportError("Run: pip install chromadb")

try:
    import fitz  # pymupdf
except ImportError:
    raise ImportError("Run: pip install pymupdf")


SYSTEM_PROMPT = """You are an FSA Navigator — an expert assistant that helps farmers understand USDA Farm Service Agency (FSA) programs including ARC, PLC, CRP, and related farm programs.

RULES:
1. Answer ONLY using the provided handbook excerpts below. Do not use outside knowledge.
2. Always cite your source by referencing the document name and section.
3. If the provided excerpts don't contain enough information to answer, say so clearly and suggest the farmer contact their local FSA office.
4. Use plain, simple language — your users are farmers, not lawyers.
5. If the question is completely unrelated to agriculture, farming, or FSA programs, politely say this tool is only for FSA and agricultural questions — do NOT suggest contacting the FSA office for unrelated topics.
6. If a question involves eligibility or payment calculations, walk through the logic step by step.
7. Never give legal or financial advice — always recommend verifying with the local FSA office for official decisions.

FORMAT:
- Give a direct answer first
- Give a concrete example if it helps clarify
- Then explain the reasoning in detail — always show your work step by step
- Always aim for complete, thorough answers. Never give a one-line response.
- Then explain the reasoning/detail
- End with: "Source: [document name], [section]"
"""


class FSANavigator:
    def _is_useful_chunk(self, text: str) -> bool:
        # Too many non-alphabetic characters = probably junk
        alpha_chars = sum(c.isalpha() for c in text)
        if len(text) == 0:
            return False
        if alpha_chars / len(text) < 0.4:  # less than 40% real letters = junk
            return False
        # Too short after stripping
        if len(text.strip()) < 100:
            return False
        return True
    def __init__(self, persist_dir: str = "data/chroma"):
        os.makedirs(persist_dir, exist_ok=True)

        self.client_chroma = chromadb.PersistentClient(path=persist_dir)

        # Use sentence-transformers if available, else fall back to default
        try:
            from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
            ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        except Exception:
            ef = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client_chroma.get_or_create_collection(
            name="fsa_handbooks",
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"}
        )

        # Initialize both API clients
        # Google Gemini client
        self.gemini_client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY", "")
        )

        # Groq client
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))



    # ------------------------------------------------------------------ #
    #  INGESTION                                                           #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _split_list(input_list: list, chunk_size: int):
       # """Yield successive chunks of chunk_size from input_list."""
        for i in range(0, len(input_list), chunk_size):
            yield input_list[i:i + chunk_size]
            
    def ingest_pdfs(self, pdf_paths: List[str]) -> int:
    # """Parse PDFs, chunk them, embed and store in batches of 546."""
        all_chunks = []
        for path in pdf_paths:
            chunks = self._parse_and_chunk(path)
            all_chunks.extend(chunks)
        
        if not all_chunks:
            return 0

        # Fix: get existing IDs in batches instead of all at once
        existing_ids = set()
        batch_size = 500
        total = self.collection.count()
        for offset in range(0, total, batch_size):
            result = self.collection.get(limit=batch_size, offset=offset)
            existing_ids.update(result["ids"])

        new_chunks = [c for c in all_chunks if c["id"] not in existing_ids]

        if new_chunks:
            # Also add in batches to be safe
            for i in range(0, len(new_chunks), batch_size):
                batch = new_chunks[i:i + batch_size]
                self.collection.add(
                    ids=[c["id"] for c in batch],
                    documents=[c["text"] for c in batch],
                    metadatas=[c["metadata"] for c in batch],
                )
        
        return len(new_chunks)



    def _parse_and_chunk(self, pdf_path: str) -> List[Dict]:
        """
        Parse a PDF and split into meaningful chunks.
        
        IMPROVEMENT OPPORTUNITY:
        This naive chunker splits by character count. A smarter version would:
        - Detect FSA handbook section headers (e.g., "Par. 52", "Subpart B")
        - Keep tables intact instead of splitting them
        - Preserve paragraph boundaries
        - Tag chunks by program type (ARC, PLC, CRP, etc.)
        """
        doc = fitz.open(pdf_path)
        source_name = os.path.basename(pdf_path).replace(".pdf", "")
        chunks = []

        CHUNK_SIZE = 800      # characters — tune this
        CHUNK_OVERLAP = 150   # overlap between chunks to preserve context

        full_text_by_page = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()
            if text and len(text.strip()) > 200:  # skip pages with barely any text
                full_text_by_page.append((page_num + 1, text.strip()))
        # Sliding window chunker
        combined = ""
        page_map = []  # track which page each char came from

        for page_num, text in full_text_by_page:
            for char in text:
                combined += char
                page_map.append(page_num)

        i = 0
        chunk_index = 0
        while i < len(combined):
            chunk_text = combined[i:i + CHUNK_SIZE].strip()
            if len(chunk_text) < 100:  # skip tiny trailing chunks
                break
            if not self._is_useful_chunk(chunk_text):
                i += CHUNK_SIZE - CHUNK_OVERLAP
                continue

            page_num = page_map[min(i, len(page_map) - 1)]
            section = self._detect_section(chunk_text)
            # Use full chunk text + index to ensure uniqueness
            chunk_id = hashlib.md5(f"{source_name}:{chunk_index}:{chunk_text}".encode()).hexdigest()
            chunk_index += 1

            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    "source": source_name,
                    "page": page_num,
                    "section": section,
                }
            })
            i += CHUNK_SIZE - CHUNK_OVERLAP

        doc.close()
        return chunks

    def _detect_section(self, text: str) -> str:
        """
        Try to extract a section header from the chunk.
        
        IMPROVEMENT OPPORTUNITY:
        FSA handbooks use consistent patterns like:
        "Par. 52", "Section 3", "Subpart B — Eligibility"
        A regex pass here could dramatically improve citation quality.
        """
        lines = text.split("\n")
        for line in lines[:5]:  # check first 5 lines
            line = line.strip()
            if line and len(line) < 80 and (
                line.startswith("Par.") or
                line.startswith("Section") or
                line.isupper() or
                line.endswith(".")
            ):
                return line
        return "General"

    # ------------------------------------------------------------------ #
    #  QUERYING                                                            #
    # ------------------------------------------------------------------ #

    def query(self, question: str, chat_history: list = None, n_results: int = 5, provider: str = "groq") -> Dict[str, Any]:
        """
        Retrieve relevant chunks and generate a grounded answer.
        Args:
            question: The user's question
            chat_history: Previous chat messages
            n_results: Number of chunks to retrieve
            provider: LLM provider to use ("gemini" or "groq")
        Returns: { answer: str, citations: list }
        """
        # Retrieve
        results = self.collection.query(
            query_texts=[question],
            n_results=min(n_results, max(1, self.collection.count())),
        )

        chunks = []
        citations = []

        if results and results["documents"] and results["documents"][0]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                chunks.append(doc)
                citations.append({
                    "source": meta.get("source", "Unknown"),
                    "section": meta.get("section", ""),
                    "page": meta.get("page", ""),
                    "text": doc[:300] + "..." if len(doc) > 300 else doc,
                })

        # Build context block
        if chunks:
            context = "\n\n---\n\n".join([
                f"[Source: {c['source']}, {c['section']}]\n{chunk}"
                for chunk, c in zip(chunks, citations)
            ])
            user_message = f"HANDBOOK EXCERPTS:\n{context}\n\nFARMER QUESTION: {question}"
        else:
            user_message = f"FARMER QUESTION: {question}\n\n(No handbook documents have been loaded yet.)"
            citations = []
        
        # Generate using selected LLM provider
        try:
            if provider.lower() == "gemini":
                # Use Gemini API
                full_prompt = f"{SYSTEM_PROMPT}\n\n{user_message}"

                # Add chat history if available
                if chat_history:
                    history_text = "\n\n".join([
                        f"{msg['role'].upper()}: {msg['content']}"
                        for msg in chat_history[-6:]
                    ])
                    full_prompt = f"{SYSTEM_PROMPT}\n\nPREVIOUS CONVERSATION:\n{history_text}\n\n{user_message}"

                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=full_prompt
                )
                answer = response.text

            else:  # Default to Groq
                # Build messages with history for Groq
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]

                # Add previous turns if any
                if chat_history:
                    messages.extend(chat_history[-6:])

                # Add current question with context
                messages.append({"role": "user", "content": user_message})

                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    max_tokens=1024
                )
                answer = response.choices[0].message.content

        except Exception as e:
            answer = f"Error generating response: {str(e)}\n\nMake sure your {provider.upper()}_API_KEY is set in your .env file."

        return {
            "answer": answer,
            "citations": citations,
        }

    def collection_size(self) -> int:
        return self.collection.count()

# 🌾 FSAgent: RAG-Powered USDA Farm Service Agency Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that helps farmers get plain-English answers about USDA Farm Service Agency (FSA) programs — ARC, PLC, CRP, and more — with citations back to official handbooks.

---

## 📋 Problem Statement

Farmers face significant challenges accessing and understanding USDA Farm Service Agency (FSA) program information:

1. **Complex Documentation**: FSA handbooks are written in dense legal and regulatory language that is difficult for farmers to navigate and comprehend
2. **Manual Search**: Finding relevant information requires manually searching through hundreds of pages across multiple PDF documents
3. **Time-Intensive**: Farmers need quick answers to make time-sensitive farm management decisions about program enrollment, eligibility, and payment limits
4. **Verification Needs**: Farmers need to verify information sources to ensure they're acting on official, current guidance

**The Challenge**: How can we bridge the gap between complex regulatory documentation and farmers' need for quick, accurate, plain-English answers while maintaining source transparency?

---

## 💡 Solution Overview

FSAgent is a RAG-powered chatbot that:

- **Ingests official FSA handbooks** into a searchable vector database
- **Provides plain-English answers** to farmers' questions about FSA programs
- **Cites official sources** for every answer, including document name, page number, and section reference
- **Supports dual LLM backends** (Groq Llama 3.3-70b and Google Gemini 2.0 Flash) for flexibility
- **Features an intuitive web interface** built with Streamlit for easy access
- **Includes evaluation framework** with 32+ test cases to ensure answer quality

### Key Capabilities

✅ Answer questions about ARC (Agricultural Risk Coverage), PLC (Price Loss Coverage), CRP (Conservation Reserve Program), and other FSA programs
✅ Provide citations with document name, page number, and section references
✅ Upload and ingest new FSA handbooks on demand
✅ Web scraping tool to automatically download official USDA handbooks
✅ Evaluation harness to benchmark answer accuracy against known Q&A pairs
✅ User-friendly chat interface with example questions and expandable citations

---

## 🔧 Technical Approach

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web UI (app.py)               │
│  • Chat interface with history                              │
│  • PDF upload/management                                     │
│  • LLM provider selection (Groq/Gemini)                     │
│  • Citation display with expandable excerpts                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              RAG Engine (chatbot/rag.py)                    │
│                                                              │
│  Ingestion Pipeline:                                        │
│  1. PDF parsing (PyMuPDF)                                   │
│  2. Chunking (800 chars, 150 char overlap)                  │
│  3. Quality filtering (40% alphabetic, 100+ chars)          │
│  4. Embedding (Sentence-Transformers all-MiniLM-L6-v2)      │
│  5. Vector storage (ChromaDB with metadata)                 │
│                                                              │
│  Query Pipeline:                                            │
│  1. Embed user question                                     │
│  2. Semantic search (top 5 chunks)                          │
│  3. Build context with citations                            │
│  4. LLM generation with system prompt                       │
│  5. Return answer + sources                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               ChromaDB Vector Database                      │
│  • Persistent storage in data/chroma/                       │
│  • Cosine similarity search                                 │
│  • Metadata: source, page, section                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              LLM Providers (API-based)                      │
│  • Groq (Llama 3.3-70b) — Default, faster                   │
│  • Google Gemini 2.0 Flash — Alternative                    │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.32.0+ | Web-based chat interface |
| **Vector DB** | ChromaDB 0.4.0+ | Semantic search and storage |
| **Embeddings** | Sentence-Transformers | Text-to-vector conversion (all-MiniLM-L6-v2 model) |
| **PDF Processing** | PyMuPDF 1.23.0+ | Extract text from FSA handbooks |
| **LLM APIs** | Groq API, Google Gemini API | Answer generation |
| **Web Scraping** | BeautifulSoup4, Requests | Download USDA handbooks |
| **Configuration** | python-dotenv | API key management |

### System Prompt Design

The RAG engine uses a carefully crafted system prompt that instructs the LLM to:

1. **Answer only from provided handbook excerpts** (no external knowledge)
2. **Always cite sources** with document name and section number
3. **Admit knowledge gaps** and suggest contacting local FSA offices when handbooks lack information
4. **Use farmer-friendly language** instead of legal jargon
5. **Reject off-topic questions** politely
6. **Show step-by-step reasoning** for eligibility and payment calculations
7. **Provide concrete examples** where helpful
8. **Never give legal or financial advice**

### Chunking Strategy

- **Method**: Fixed character-length sliding window
- **Size**: 800 characters per chunk
- **Overlap**: 150 characters between chunks
- **Quality Filter**: Requires 40% alphabetic content and 100+ character minimum
- **Deduplication**: MD5 hash-based to prevent duplicate chunks

### Retrieval & Context Building

1. User question is embedded using the same Sentence-Transformers model
2. ChromaDB performs cosine similarity search to find top 5 most relevant chunks
3. Retrieved chunks are formatted with source metadata (document, page, section)
4. Context block is passed to LLM along with system prompt and user question
5. LLM generates answer with inline citations

### Evaluation Framework

The `eval.py` script provides automated testing:

- **32 test cases** covering ARC, PLC, CRP, payment limits, eligibility rules, and historical context
- **Keyword matching** to verify required terms appear in answers
- **Pass/fail scoring** with detailed failure analysis
- **Improvement tracking** to validate changes to chunking and prompts

---

## 📊 Results

### Current Performance

- **Vector Database**: Successfully ingests USDA FSA handbooks with metadata preservation
- **Citation Quality**: Provides source references including document name, page numbers, and section headers
- **Response Time**: Sub-2-second responses for most queries (Groq backend)
- **Evaluation Score**: 32 comprehensive test cases covering payment limits, eligibility, historical changes, and procedural requirements

### Example Questions & Answers

**Q: "What is the payment limit for ARC-CO for a single person?"**
A: "The payment limit for ARC-CO is $125,000 per person, combined with PLC payments. Source: 1-ARCPLC handbook, Section 3"

**Q: "Can a farmer switch between ARC-CO and PLC every year?"**
A: "No, elections are generally made for the life of the farm bill period, though some exceptions may apply. Source: 1-ARCPLC handbook, Par. 52"

**Q: "What is the AGI limitation for FSA program benefits?"**
A: "Producers with Adjusted Gross Income exceeding $2.5 million are ineligible for most FSA benefits. Source: 1-PL handbook, Section 4"

### Key Features Demonstrated

✅ Multi-document ingestion (226 USDA PDF files supported)
✅ Real-time PDF upload and processing
✅ Expandable citation UI for source verification
✅ Dual LLM backend support with seamless switching
✅ Persistent chat history within sessions
✅ Quality filtering to exclude low-value chunks

### Known Limitations

1. **Chunking**: Simple character-based splitting doesn't respect FSA handbook structure (paragraph numbers, tables, subparts)
2. **Section Detection**: Basic regex patterns may miss complex FSA formatting conventions
3. **Evaluation Metrics**: Current keyword matching is simplistic; needs semantic similarity scoring
4. **Python 3.14+**: Not supported due to ChromaDB compatibility constraints
5. **Concurrent Users**: Single-user Streamlit deployment (default configuration)

---

## 🚀 Run Instructions

### Prerequisites

- **Python**: 3.11, 3.12, or 3.13 (NOT 3.14+)
- **API Keys**: Groq API or Google Gemini API (or both)

### Step 1: Clone and Setup

```bash
# Clone the repository
cd /path/to/FSAgent

# Create virtual environment (recommended)
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys

Create a `.env` file in the project root:

```bash
# .env file
GROQ_API_KEY=gsk_your_groq_api_key_here
GEMINI_API_KEY=AIza_your_gemini_api_key_here
```

**Get API Keys:**
- Groq: https://console.groq.com/keys
- Google Gemini: https://ai.google.dev/

### Step 3: Download FSA Handbooks

**Option A: Automatic Download** (recommended)

```bash
# Download all available FSA handbooks from USDA website
python webscrape.py

# This creates USDA_PDFs/ directory with 226 handbook files
```

**Option B: Manual Download**

Download key handbooks from https://www.fsa.usda.gov/resources/programs-and-services/handbooks/index

Essential handbooks:
- [1-ARCPLC.pdf](https://www.fsa.usda.gov/Internet/FSA_File/1-arcplc.pdf) — ARC/PLC programs
- [1-CRP.pdf](https://www.fsa.usda.gov/Internet/FSA_File/1-crp.pdf) — Conservation Reserve Program
- [1-PL.pdf](https://www.fsa.usda.gov/Internet/FSA_File/1-pl.pdf) — Payment Limitations

Place PDFs in `data/pdfs/` directory.

### Step 4: Ingest Documents

```bash
# Create data directory if it doesn't exist
mkdir -p data/pdfs

# Copy or move PDFs to data/pdfs/
cp USDA_PDFs/*.pdf data/pdfs/

# Run ingestion script
python ingest.py data/pdfs/

# Expected output:
# Processing 1-ARCPLC.pdf...
# Extracted 1,234 chunks from 1-ARCPLC.pdf
# Processing 1-CRP.pdf...
# ...
# Ingestion complete. Total chunks: 12,345
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Application

1. **Select LLM Provider**: Choose Groq or Gemini in the sidebar
2. **Ask Questions**: Type questions or click example questions in the sidebar
3. **View Citations**: Expand citation boxes to see source excerpts
4. **Upload PDFs**: Use the sidebar uploader to add new handbooks on-the-fly

### Running Evaluation

```bash
# Run the evaluation suite
python eval.py

# Expected output:
# FSA Navigator — Evaluation Run
# ==================================================
# Documents in DB: 12,345 chunks
#
# ✅ Q1: What is the payment limit for ARC-CO for a single person?
#    Missing: nothing
# ✅ Q2: What does ARC stand for?
#    Missing: nothing
# ...
# Score: 28/32
```

### Directory Structure After Setup

```
FSAgent/
├── app.py                     # Streamlit web interface
├── ingest.py                  # Batch ingestion CLI tool
├── eval.py                    # Evaluation harness
├── webscrape.py               # USDA handbook downloader
├── chatbot/
│   └── rag.py                # RAG engine (core logic)
├── data/
│   ├── pdfs/                 # Your FSA handbooks go here
│   └── chroma/               # Vector database (auto-created)
├── USDA_PDFs/                # Downloaded handbooks (if using webscrape.py)
├── requirements.txt          # Python dependencies
├── .env                      # API keys (create this)
├── .gitignore
└── README.md                 # This file
```

---

## 🔍 Improvement Opportunities

### 1. Intelligent Chunking
**Current**: Fixed 800-character chunks
**Needed**: Respect FSA handbook structure (paragraph numbers, subparts, tables)
**Impact**: Dramatically improved retrieval accuracy
**File**: `chatbot/rag.py:_parse_and_chunk()`

### 2. System Prompt Optimization
**Approach**: Run `eval.py`, analyze failures, iteratively refine prompt
**Impact**: Higher answer quality and fewer hallucinations
**File**: `chatbot/rag.py:SYSTEM_PROMPT`

### 3. Enhanced Evaluation Metrics
**Current**: Keyword substring matching
**Needed**: LLM-graded rubrics, factual accuracy checks, retrieval recall tracking
**Impact**: More reliable quality measurement
**File**: `eval.py:run_eval()`

### 4. Section Detection Improvements
**Current**: Basic regex for "Par.", "Section", uppercase patterns
**Needed**: Comprehensive FSA formatting patterns
**Impact**: Better citation quality
**File**: `chatbot/rag.py:_detect_section()`

### 5. Document Corpus Research
**Question**: Which FSA handbooks matter most for target farmers?
**Action**: Interview farmers, analyze common questions, prioritize ingestion
**Impact**: Corpus quality is the highest-leverage improvement

### 6. Metadata Enrichment
**Ideas**: Extract handbook version dates, effective dates, amendment tracking
**Impact**: Users can verify they're getting current information

---

## 📚 Key FSA Handbook Sources

All documents are public domain and freely available:

- [FSA Handbooks Index](https://www.fsa.usda.gov/resources/programs-and-services/handbooks/index)
- [ARC/PLC Program](https://www.fsa.usda.gov/programs-and-services/arcplc_program/index)
- [CRP Program](https://www.fsa.usda.gov/programs-and-services/conservation-programs/conservation-reserve-program/)
- [Payment Limitations](https://www.fsa.usda.gov/programs-and-services/payment-eligibility/index)

---

## ⚠️ Disclaimer

This tool is for **informational purposes only**. Always verify program details, eligibility requirements, and payment calculations with your local FSA County Office before making farm management decisions. This chatbot is not a substitute for professional agricultural, legal, or financial advice.

---

## 📄 License

This project uses public domain USDA documents. The code is provided as-is for educational and agricultural support purposes.

---

## 🤝 Contributing

Contributions are welcome! Priority areas:

1. Improving chunking strategies for FSA handbook structure
2. Expanding evaluation test cases with real farmer questions
3. Optimizing system prompts based on failure analysis
4. Adding support for additional FSA programs (NAP, ELAP, etc.)

---

## 📞 Support

For technical issues with the chatbot, please check the code in `chatbot/rag.py` and `app.py`.

For FSA program questions, contact your local USDA Service Center: https://www.farmers.gov/service-center-locator

---

**Built to help farmers navigate USDA programs with confidence** 🌾

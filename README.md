# 🌾 FSAgent

A RAG-powered chatbot that helps farmers get plain-English answers about USDA Farm Service Agency programs — ARC, PLC, CRP, and more — with citations back to official handbooks.

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Download FSA handbooks (public domain, free)
mkdir -p data/pdfs
# Key handbooks to start with:
# https://www.fsa.usda.gov/Internet/FSA_File/1-arcplc.pdf  → ARC/PLC programs
# https://www.fsa.usda.gov/Internet/FSA_File/1-crp.pdf     → CRP program

# 4. Ingest the handbooks
python ingestion/ingest.py data/pdfs/

# 5. Run the app
streamlit run app.py
```

---

## Project Structure

```
fsa-navigator/
├── app.py                  # Streamlit UI
├── chatbot/
│   └── rag.py              # RAG engine (ingestion + querying)
├── ingestion/
│   └── ingest.py           # Standalone ingestion script
├── eval.py                 # Evaluation / benchmarking
├── data/
│   ├── pdfs/               # Your FSA handbook PDFs go here
│   └── chroma/             # Auto-created vector DB storage
└── requirements.txt
```

---

## Where to Improve (The Real Work)

### 1. Better Chunking (`chatbot/rag.py → _parse_and_chunk`)
The default chunker splits by character count. FSA handbooks have real structure — paragraph numbers, subparts, tables. A smarter chunker that respects this hierarchy will dramatically improve retrieval accuracy.

### 2. System Prompt Tuning (`chatbot/rag.py → SYSTEM_PROMPT`)
Run `eval.py`, find failure cases, and rewrite the prompt to fix them. This is high-ROI work.

### 3. Evaluation (`eval.py → EVAL_SET`)
Add more Q&A pairs with known correct answers. The more coverage, the more confident you can be in your improvements.

### 4. Document Selection
Which FSA handbooks matter most for real farmers in your region? Research this and add the right docs. The corpus quality is everything.

### 5. Section Detection (`chatbot/rag.py → _detect_section`)
FSA handbooks use patterns like "Par. 52", "Subpart B". A regex pass here improves citation quality significantly.

---

## Key FSA Handbook Sources

All public domain, free to download:
- [FSA Handbooks](https://www.fsa.usda.gov/resources/programs-and-services/handbooks/index)
- [ARC/PLC Fact Sheet](https://www.fsa.usda.gov/programs-and-services/arcplc_program/index)
- [CRP Program](https://www.fsa.usda.gov/programs-and-services/conservation-programs/conservation-reserve-program/)

---

## Disclaimer

This tool is for informational purposes only. Always verify program details and eligibility with your local FSA office before making farm management decisions.

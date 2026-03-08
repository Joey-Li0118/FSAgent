import streamlit as st
import os
from chatbot.rag import FSANavigator

st.set_page_config(
    page_title="FSAgent",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 FSA Navigator")
st.caption("Ask plain-English questions about USDA Farm Service Agency programs — ARC, PLC, CRP, and more.")

# --- CSS ---
import streamlit as st
import os
from chatbot.rag import FSANavigator

st.set_page_config(
    page_title="FSA Navigator",
    page_icon="🌾",
    layout="wide"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,500&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root palette ── */
:root {
  --soil:       #2c1f0e;
  --bark:       #4a3422;
  --wheat:      #c8922a;
  --straw:      #e8c97a;
  --cream:      #f5edd8;
  --parchment:  #faf5eb;
  --sage:       #6b7c5c;
  --moss:       #4a5c3a;
  --sky:        #4a7c9e;
  --mist:       #d4e4ef;
  --ink:        #1a1208;
  --fade:       rgba(44,31,14,0.06);
}

/* ── Global reset ── */
html, body, [class*="css"] {
  font-family: 'Source Serif 4', Georgia, serif;
  background-color: var(--parchment) !important;
  color: var(--ink) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── App wrapper ── */
.stApp {
  background: var(--parchment) !important;
}

/* ── Hero banner ── */
.hero-banner {
  background:
    linear-gradient(160deg, var(--soil) 0%, var(--bark) 55%, var(--moss) 100%);
  border-radius: 16px;
  padding: 2.4rem 2.8rem 2rem;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(44,31,14,0.22);
}
.hero-banner::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(ellipse at 80% 20%, rgba(200,146,42,0.18) 0%, transparent 60%),
    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c8922a' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
}
.hero-icon {
  font-size: 2.8rem;
  line-height: 1;
  margin-bottom: 0.4rem;
  display: block;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.4));
}
.hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--straw) !important;
  line-height: 1.15;
  margin: 0 0 0.4rem;
  letter-spacing: -0.02em;
}
.hero-sub {
  font-size: 0.95rem;
  color: rgba(232,201,122,0.72) !important;
  font-style: italic;
  margin: 0;
  line-height: 1.5;
}
.hero-badge {
  position: absolute;
  top: 1.4rem;
  right: 1.8rem;
  background: rgba(200,146,42,0.18);
  border: 1px solid rgba(200,146,42,0.35);
  color: var(--straw) !important;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  padding: 0.25rem 0.7rem;
  border-radius: 20px;
  text-transform: uppercase;
}

/* ── Section headings ── */
.section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--sage) !important;
  margin: 1.4rem 0 0.6rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.section-label::after {
  content: "";
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--sage), transparent);
  opacity: 0.35;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--soil) !important;
  border-right: 1px solid rgba(200,146,42,0.15) !important;
}
[data-testid="stSidebar"] * {
  color: var(--cream) !important;
}
[data-testid="stSidebar"] .stMarkdown p {
  font-size: 0.88rem;
  line-height: 1.6;
  color: rgba(245,237,216,0.78) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: 'Playfair Display', serif !important;
  font-size: 1rem !important;
  color: var(--straw) !important;
  border-bottom: 1px solid rgba(200,146,42,0.2);
  padding-bottom: 0.4rem;
  margin-bottom: 0.6rem;
}
[data-testid="stSidebar"] hr {
  border-color: rgba(200,146,42,0.15) !important;
}
/* Example question buttons */
[data-testid="stSidebar"] .stButton button {
  background: rgba(200,146,42,0.1) !important;
  border: 1px solid rgba(200,146,42,0.25) !important;
  color: var(--cream) !important;
  font-size: 0.8rem !important;
  text-align: left !important;
  border-radius: 6px !important;
  transition: all 0.2s !important;
  padding: 0.45rem 0.75rem !important;
  font-family: 'Source Serif 4', serif !important;
  font-style: italic;
}
[data-testid="stSidebar"] .stButton button:hover {
  background: rgba(200,146,42,0.22) !important;
  border-color: rgba(200,146,42,0.5) !important;
  transform: translateX(3px) !important;
}
/* Ingest button */
[data-testid="stSidebar"] .stButton:last-of-type button {
  background: var(--wheat) !important;
  color: var(--soil) !important;
  font-style: normal !important;
  font-weight: 600 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
  padding: 0.5rem 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"],
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) {
  background: transparent !important;
}

/* Message content area */
.stChatMessage .stMarkdown {
  background: var(--cream);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  border: 1px solid rgba(44,31,14,0.1);
  box-shadow: 0 2px 8px rgba(44,31,14,0.06);
  line-height: 1.7;
  font-size: 0.95rem;
}

/* Avatar styling */
[data-testid="chatAvatarIcon-user"] {
  background: var(--sky) !important;
  color: white !important;
}
[data-testid="chatAvatarIcon-assistant"] {
  background: var(--wheat) !important;
  color: var(--soil) !important;
}

/* ── Citations expander ── */
.streamlit-expanderHeader {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.05em !important;
  color: var(--sage) !important;
  background: transparent !important;
}
.streamlit-expanderContent {
  background: var(--fade) !important;
  border-radius: 0 0 8px 8px !important;
  padding: 0.8rem !important;
  border: 1px solid rgba(44,31,14,0.08) !important;
  border-top: none !important;
}
.streamlit-expanderContent .stMarkdown strong {
  color: var(--bark) !important;
  font-family: 'Playfair Display', serif !important;
}
.streamlit-expanderContent .stCaption {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.72rem !important;
  color: var(--sage) !important;
  background: white;
  padding: 0.5rem 0.8rem;
  border-radius: 6px;
  border-left: 3px solid var(--wheat);
  margin-top: 0.3rem !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
  background: white !important;
  border: 2px solid rgba(200,146,42,0.3) !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 16px rgba(44,31,14,0.08) !important;
  transition: border-color 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--wheat) !important;
  box-shadow: 0 4px 20px rgba(200,146,42,0.15) !important;
}
[data-testid="stChatInput"] textarea {
  font-family: 'Source Serif 4', serif !important;
  font-size: 0.95rem !important;
  color: var(--ink) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: rgba(44,31,14,0.35) !important;
  font-style: italic;
}
[data-testid="stChatInputSubmitButton"] button {
  background: var(--wheat) !important;
  border-radius: 8px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: rgba(200,146,42,0.06) !important;
  border: 1px dashed rgba(200,146,42,0.35) !important;
  border-radius: 8px !important;
  padding: 0.5rem !important;
}

/* ── Spinner ── */
.stSpinner > div {
  border-top-color: var(--wheat) !important;
}

/* ── Success/warning alerts ── */
.stSuccess {
  background: rgba(107,124,92,0.12) !important;
  border-left-color: var(--sage) !important;
  color: var(--moss) !important;
}
.stWarning, .stCaption {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.72rem !important;
}

/* ── Divider line ── */
hr {
  border-color: rgba(200,146,42,0.2) !important;
}

/* ── Main column layout ── */
.main .block-container {
  max-width: 820px !important;
  padding-top: 2rem !important;
  padding-bottom: 6rem !important;
}

/* ── Empty state ── */
.empty-state {
  text-align: center;
  padding: 3.5rem 1rem 2rem;
  color: rgba(44,31,14,0.35) !important;
}
.empty-state .empty-icon {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 0.8rem;
  opacity: 0.5;
}
.empty-state p {
  font-style: italic;
  font-size: 0.9rem;
  line-height: 1.6;
  max-width: 360px;
  margin: 0 auto;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(200,146,42,0.3);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--wheat); }
</style>
""", unsafe_allow_html=True)




# --- Init navigator ---
@st.cache_resource
def get_navigator():
    return FSANavigator()

# --- Sidebar ---
with st.sidebar:
    st.header("About")
    st.write("FSA Navigator answers questions about FSA programs using official USDA handbooks. Every answer includes a citation so you can verify the source.")

    st.divider()
    st.header("LLM Provider")
    llm_provider = st.radio(
        "Select AI Model:",
        options=["Groq (Llama 3.3)", "Gemini (Flash 2.0)"],
        index=0,
        help="Choose which AI model to use for generating answers"
    )
    # Store the provider choice in session state
    st.session_state.llm_provider = "gemini" if "Gemini" in llm_provider else "groq"

    st.divider()
    st.header("Example Questions")
    examples = [
        "What is the payment limit for ARC-CO?",
        "What crops are covered under PLC?",
        "How do I enroll in CRP?",
        "What is the difference between ARC-CO and ARC-IC?",
        "When is the FSA program election deadline?",
    ]
    for q in examples:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q

    st.divider()
    st.header("Load Documents")
    uploaded_files = st.file_uploader(
        "Upload FSA Handbooks (PDF)",
        type=["pdf"],
        accept_multiple_files=True,
        help="Download official handbooks from fsa.usda.gov and upload here."
    )
    if uploaded_files:
        if st.button("📥 Ingest Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                os.makedirs("data/pdfs", exist_ok=True)
                saved = []
                for f in uploaded_files:
                    path = f"data/pdfs/{f.name}"
                    with open(path, "wb") as out:
                        out.write(f.read())
                    saved.append(path)
                navigator = get_navigator()
                count = navigator.ingest_pdfs(saved)
                st.success(f"✅ Ingested {count} chunks from {len(saved)} document(s).")
                st.session_state.navigator = navigator

    st.divider()
    st.caption("Sources: USDA FSA Handbooks (public domain). This tool is for informational purposes only — always verify with your local FSA office.")

# --- Initialize session state ---
if "navigator" not in st.session_state:
    st.session_state.navigator = get_navigator()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "groq"

# --- Handle example question clicks ---
if "pending_question" in st.session_state:
    st.session_state.messages.append({
        "role": "user",
        "content": st.session_state.pending_question
    })
    del st.session_state.pending_question

# --- Chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "citations" in msg:
            with st.expander("📄 Sources"):
                for cite in msg["citations"]:
                    st.markdown(f"**{cite['source']}** — *{cite['section']}*")
                    st.caption(cite["text"])

# --- Input ---
prompt = st.chat_input("Ask about FSA programs...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching handbooks..."):
            navigator = st.session_state.navigator
            # Build history from session messages
            history = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    history.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    history.append({"role": "assistant", "content": msg["content"]})
            result = navigator.query(prompt, chat_history=history[-6:], provider=st.session_state.llm_provider)

        st.markdown(result["answer"])

        if result["citations"]:
            with st.expander("📄 Sources"):
                for cite in result["citations"]:
                    st.markdown(f"**{cite['source']}** — *{cite['section']}*")
                    st.caption(cite["text"])
        else:
            st.caption("⚠️ No handbook excerpts found. Upload FSA documents in the sidebar to improve answers.")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "citations": result["citations"]
    })

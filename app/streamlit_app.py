"""
app/streamlit_app.py — Gautam Solar AI Chatbot
Run: streamlit run app/streamlit_app.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from chain.rag_chain import get_chain

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Surya — Gautam Solar AI",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0D0D0D;
    color: #F0EDE6;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A0A00 0%, #0D0D0D 100%);
    border-right: 1px solid #2A1500;
}
[data-testid="stSidebar"] * { color: #F0EDE6 !important; }

/* Main area */
[data-testid="stAppViewContainer"] { background: #0D0D0D; }
[data-testid="stHeader"] { background: transparent; }

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #161616;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    margin-bottom: 10px;
    padding: 4px 8px;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    border-color: #E87722;
    background: #1A0E00;
}

/* Input box */
[data-testid="stChatInput"] textarea {
    background: #1A1A1A !important;
    border: 1px solid #E87722 !important;
    color: #F0EDE6 !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #888 !important; }

/* Source badge */
.source-badge {
    display: inline-block;
    background: #1F0D00;
    border: 1px solid #E87722;
    color: #E87722;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    margin: 2px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Suggested question buttons */
.stButton > button {
    background: #1A1A1A !important;
    border: 1px solid #333 !important;
    color: #CCC !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
    transition: all 0.2s !important;
    width: 100% !important;
    text-align: left !important;
}
.stButton > button:hover {
    border-color: #E87722 !important;
    color: #E87722 !important;
    background: #1A0E00 !important;
}

/* Metric cards */
.metric-card {
    background: #161616;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
    margin-bottom: 8px;
}
.metric-value { font-size: 22px; font-weight: 700; color: #E87722; font-family: 'Syne', sans-serif; }
.metric-label { font-size: 11px; color: #888; margin-top: 2px; }

/* Logo text */
.logo-text {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #E87722;
    letter-spacing: -0.5px;
}
.logo-sub {
    font-size: 11px;
    color: #666;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: -4px;
}

/* Header */
.chat-header {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #F0EDE6;
}
.online-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #22C55E;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0D0D0D; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

/* Divider */
hr { border-color: #222 !important; }
</style>
""", unsafe_allow_html=True)


# ── Load RAG Chain ────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_chain():
    with st.spinner("🌞 Loading Surya AI..."):
        return get_chain()


# ── Suggested Questions ───────────────────────────────────
SUGGESTED = [
    "Which panel is best for my 5kWp rooftop in Delhi?",
    "What is the efficiency of the G12 R TOPCon module?",
    "Am I eligible for PM-KUSUM as a farmer in UP?",
    "How much subsidy will I get under PM-KUSUM?",
    "Compare TOPCon vs Mono PERC panels",
    "What is the payback period for a 10kWp system?",
    "What certifications does Gautam Solar have?",
    "How often should I clean my solar panels?",
]

# ── Source type labels ────────────────────────────────────
SOURCE_LABELS = {
    "pdf": "📄 Datasheet",
    "faq": "❓ FAQ",
    "product_catalog": "🛒 Product",
    "text": "📝 Guide",
    "website": "🌐 Website",
}


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-text">☀ GAUTAM SOLAR</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">AI Assistant — Surya</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">Top 4</div><div class="metric-label">India Rank</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">3.2GW</div><div class="metric-label">Capacity</div></div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">23.69%</div><div class="metric-label">Max Efficiency</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">30 Yr</div><div class="metric-label">Warranty</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**💡 Suggested Questions**")

    for q in SUGGESTED:
        if st.button(q, key=f"sug_{q[:20]}"):
            st.session_state["prefill"] = q
            st.rerun()

    st.markdown("---")
    st.markdown("**📞 Contact Gautam Solar**")
    st.markdown("📧 info@gautamsolar.com")
    st.markdown("📞 1800-532-0800")
    st.markdown("💬 +91 93117 97248")
    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    show_sources = st.toggle("Show Sources", value=True)


# ── Main Chat Area ────────────────────────────────────────
col_main, col_gap = st.columns([1, 0.001])
with col_main:
    # Header
    st.markdown(
        '<div class="chat-header"><span class="online-dot"></span>Surya — Solar Energy Expert</div>',
        unsafe_allow_html=True,
    )
    st.caption("Powered by Mistral AI + LangChain + ChromaDB · RAG over Gautam Solar knowledge base")
    st.markdown("---")

    # Init session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome message
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="☀️"):
            st.markdown(
                "**Namaste! I'm Surya, your Gautam Solar AI assistant.** 🌞\n\n"
                "I can help you with:\n"
                "- 🔆 Solar panel specifications & recommendations\n"
                "- 🌾 PM-KUSUM Yojana eligibility & application\n"
                "- 💰 ROI calculations & savings estimates\n"
                "- 🔧 Installation & maintenance guidance\n"
                "- 📋 Certifications & compliance\n\n"
                "What would you like to know?"
            )

    # Render chat history
    for msg in st.session_state.messages:
        avatar = "🧑" if msg["role"] == "user" else "☀️"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if show_sources and msg.get("sources"):
                src_html = "".join([
                    f'<span class="source-badge">{SOURCE_LABELS.get(s["source_type"], s["source_type"])} {s["filename"]}</span>'
                    for s in msg["sources"]
                ])
                st.markdown(f"<div style='margin-top:6px'>{src_html}</div>", unsafe_allow_html=True)

    # Handle prefill from sidebar buttons
    prefill = st.session_state.pop("prefill", None)

    # Chat input
    user_input = st.chat_input("Ask about solar panels, PM-KUSUM, ROI, installation...") or prefill

    if user_input:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant", avatar="☀️"):
            with st.spinner("Searching knowledge base..."):
                try:
                    chain = load_chain()
                    result = chain.invoke(
                        question=user_input,
                        chat_history=st.session_state.messages[:-1],
                    )
                    answer = result["answer"]
                    sources = result["sources"]
                except Exception as e:
                    answer = (
                        f"⚠️ I encountered an error: `{str(e)}`\n\n"
                        "Please ensure your MISTRAL_API_KEY is set in `.env` and ChromaDB is built by running `python ingest.py`."
                    )
                    sources = []

            st.markdown(answer)
            if show_sources and sources:
                src_html = "".join([
                    f'<span class="source-badge">{SOURCE_LABELS.get(s["source_type"], s["source_type"])} {s["filename"]}</span>'
                    for s in sources
                ])
                st.markdown(f"<div style='margin-top:6px'>{src_html}</div>", unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
        })
"""
Streamlit Web Interface for Doc-RAG.
Minimal, professional dashboard aesthetic inspired by Linear, Vercel, and Stripe.
"""

import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
from src.config import AppConfig
from src.pipeline import RAGPipeline, RAGQueryResponse
from src.llm import UNANSWERABLE_RESPONSE

# Set Page Config
st.set_page_config(
    page_title="DocRAG Studio",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_pipeline():
    """Cache pipeline instance across sessions."""
    config = AppConfig.load_from_env()
    return RAGPipeline(config=config)


# Initialize theme state
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"


def apply_minimal_theme(theme_mode: str = "dark"):
    """Inject Linear/Vercel monochrome CSS design system tokens."""
    is_dark = theme_mode == "dark"

    if is_dark:
        bg_page = "#09090B"
        bg_card = "#18181B"
        bg_card_hover = "#27272A"
        border_color = "#27272A"
        text_primary = "#FAFAFA"
        text_secondary = "#A1A1AA"
        text_muted = "#71717A"
        accent_blue = "#3B82F6"
        badge_dot = "#10B981"
        code_bg = "#27272A"
    else:
        bg_page = "#FAFAFA"
        bg_card = "#FFFFFF"
        bg_card_hover = "#F4F4F5"
        border_color = "#E4E4E7"
        text_primary = "#09090B"
        text_secondary = "#52525B"
        text_muted = "#71717A"
        accent_blue = "#2563EB"
        badge_dot = "#059669"
        code_bg = "#F4F4F5"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background-color: {bg_page};
        color: {text_primary};
    }}

    /* Hide default Streamlit header elements */
    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    /* Top Brand Navigation Header */
    .nav-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 20px;
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 8px;
        margin-bottom: 20px;
    }}

    .nav-left {{
        display: flex;
        align-items: center;
        gap: 16px;
    }}

    .brand-name {{
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: {text_primary};
    }}

    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.75rem;
        color: {text_muted};
        font-weight: 500;
    }}

    .status-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: {badge_dot};
    }}

    /* Eyebrow Section Labels */
    .eyebrow-label {{
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {text_muted};
        margin-bottom: 8px;
    }}

    /* Custom Card Panels */
    .panel-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }}

    /* Bordered Answer Card (No saturated fills) */
    .answer-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-left: 3px solid {accent_blue};
        border-radius: 8px;
        padding: 18px 20px;
        font-size: 0.92rem;
        line-height: 1.65;
        color: {text_primary};
        margin-bottom: 20px;
    }}

    .refusal-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-left: 3px solid {text_muted};
        border-radius: 8px;
        padding: 18px 20px;
        font-size: 0.92rem;
        line-height: 1.65;
        color: {text_secondary};
        margin-bottom: 20px;
    }}

    /* Source Cards & Monospace Metrics */
    .source-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }}

    .source-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }}

    .source-name {{
        font-size: 0.85rem;
        font-weight: 500;
        color: {text_primary};
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .source-score {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: {text_muted};
    }}

    .thin-progress-bg {{
        width: 100%;
        background-color: {border_color};
        height: 3px;
        border-radius: 1.5px;
        overflow: hidden;
        margin-top: 4px;
        margin-bottom: 8px;
    }}

    .thin-progress-fill {{
        height: 100%;
        background-color: {accent_blue};
        border-radius: 1.5px;
    }}

    .source-excerpt {{
        font-size: 0.83rem;
        color: {text_secondary};
        line-height: 1.5;
        padding-left: 10px;
        border-left: 2px solid {border_color};
        margin-top: 6px;
    }}

    .mono-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        background-color: {code_bg};
        padding: 2px 6px;
        border-radius: 4px;
        color: {text_secondary};
    }}

    /* Custom Streamlit Button Styling */
    .stButton > button {{
        border-radius: 6px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
    }}

    /* Ghost Secondary Buttons */
    button[data-testid="baseButton-secondary"] {{
        background: transparent !important;
        border: 1px solid {border_color} !important;
        color: {text_secondary} !important;
    }}

    button[data-testid="baseButton-secondary"]:hover {{
        background: {bg_card_hover} !important;
        color: {text_primary} !important;
        border-color: {text_muted} !important;
    }}

    /* Primary Action Button */
    button[data-testid="baseButton-primary"] {{
        background: {accent_blue} !important;
        border: 1px solid {accent_blue} !important;
        color: #FFFFFF !important;
    }}

    button[data-testid="baseButton-primary"]:hover {{
        opacity: 0.9 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def main():
    pipeline = get_pipeline()
    current_theme = st.session_state.get("theme", "dark")
    apply_minimal_theme(current_theme)

    # Sidebar Controls & Navigation
    with st.sidebar:
        st.markdown('<div class="eyebrow-label">SYSTEM STATUS</div>', unsafe_allow_html=True)

        is_indexed = pipeline.is_indexed()
        num_vectors = pipeline.vector_store.index.ntotal if (pipeline.vector_store and pipeline.vector_store.index) else 0

        status_text = f"Index Ready · {num_vectors} Chunks" if is_indexed else "Index Not Built"
        st.markdown(
            f"""
            <div class="status-indicator">
                <span class="status-dot"></span>
                <span>{status_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        if st.button("Rebuild Index", use_container_width=True, type="secondary"):
            with st.spinner("Processing documents..."):
                res = pipeline.build_index(force_rebuild=True)
                st.success(f"Built {res['chunks']} chunks.")
                st.rerun()

        st.markdown("---")
        st.markdown('<div class="eyebrow-label">SAMPLE QUERIES</div>', unsafe_allow_html=True)

        sample_categories = {
            "FACTUAL": [
                "How many days of paid annual leave do employees receive?",
                "What is the minimum password length requirement?",
                "What are the REST API rate limits?",
            ],
            "PARAPHRASED": [
                "Can team members work remotely and is there an equipment stipend?",
                "How do I factory reset the hardware unit if unresponsive?",
            ],
            "SPECIFICATIONS": [
                "What is the guaranteed service uptime SLA for Enterprise tier?",
                "How much does the Professional Plan cost per month?",
            ],
            "REFUSAL TEST": [
                "What is the policy on quantum teleportation devices?",
                "Who won the 2024 World Series?",
            ],
        }

        selected_question = ""
        for category, questions in sample_categories.items():
            st.markdown(f'<div class="eyebrow-label" style="font-size:0.65rem; margin-top:10px;">{category}</div>', unsafe_allow_html=True)
            for q in questions:
                # Truncate label for clean display
                label = q[:36] + "..." if len(q) > 36 else q
                if st.button(label, key=f"q_{q[:15]}", use_container_width=True, type="secondary"):
                    selected_question = q

        st.markdown("---")
        st.markdown('<div class="eyebrow-label">ENGINE SETTINGS</div>', unsafe_allow_html=True)

        supported_models = [
            "groq/compound-mini",
            "groq/compound",
            "qwen/qwen3.6-27b",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "allam-2-7b",
            "llama-3.3-70b-versatile",
        ]

        current_model = pipeline.config.groq_model
        default_index = supported_models.index(current_model) if current_model in supported_models else 0

        selected_model = st.selectbox(
            "Model",
            supported_models,
            index=default_index,
        )
        if selected_model != pipeline.config.groq_model:
            pipeline.config.groq_model = selected_model
            pipeline.llm.model_name = selected_model

        top_k = st.slider("Top-K Chunks", min_value=1, max_value=10, value=pipeline.config.top_k)
        pipeline.config.top_k = top_k
        pipeline.retriever.top_k = top_k

        threshold = st.slider(
            "Threshold",
            min_value=0.1,
            max_value=0.8,
            value=float(pipeline.config.similarity_threshold),
            step=0.05,
        )
        pipeline.config.similarity_threshold = threshold
        pipeline.retriever.similarity_threshold = threshold

    # Top Navigation Header Bar with Brand & Sun/Moon Toggle
    header_col1, header_col2 = st.columns([6, 1])
    with header_col1:
        st.markdown(
            f"""
            <div class="nav-header" style="margin-bottom:0px;">
                <div class="nav-left">
                    <span class="brand-name">DocRAG Studio</span>
                    <div class="status-indicator">
                        <span class="status-dot"></span>
                        <span>{status_text}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with header_col2:
        theme_icon = "☀️" if current_theme == "dark" else "🌙"
        if st.button(theme_icon, key="theme_toggle", use_container_width=True, type="secondary"):
            st.session_state["theme"] = "light" if current_theme == "dark" else "dark"
            st.rerun()

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Main Question Form
    st.markdown('<div class="eyebrow-label">QUESTION INPUT</div>', unsafe_allow_html=True)
    question_input = st.text_input(
        "Question",
        value=selected_question,
        placeholder="Ask a question over the PDF knowledge base...",
        label_visibility="collapsed",
    )

    btn_col1, btn_col2 = st.columns([1, 4])
    with btn_col1:
        ask_button = st.button("Ask Question", type="primary", use_container_width=True)

    if ask_button or selected_question:
        query_text = question_input.strip() if question_input else selected_question
        if not query_text:
            st.warning("Please enter a question.")
            return

        with st.spinner("Retrieving context & generating answer..."):
            response: RAGQueryResponse = pipeline.answer_question(query_text)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="eyebrow-label">GROUNDED RESPONSE</div>', unsafe_allow_html=True)

        if response.error:
            st.error(response.error)

        clean_answer = response.answer.replace("**", "")  # Strip markdown bolding for clean prose

        if UNANSWERABLE_RESPONSE.lower() in clean_answer.lower():
            st.markdown(
                f'<div class="refusal-card">{clean_answer}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="answer-card">{clean_answer}</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="eyebrow-label">SOURCE ATTRIBUTION</div>', unsafe_allow_html=True)

        if response.sources:
            for idx, src in enumerate(response.sources, 1):
                relevance_pct = min(100.0, max(0.0, src.score * 100))
                
                # SVG Document Icon
                doc_svg = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>"""
                
                st.markdown(
                    f"""
                    <div class="source-card">
                        <div class="source-top">
                            <span class="source-name">{doc_svg} {src.document_name} · Page {src.page_number}</span>
                            <span class="source-score">{relevance_pct:.1f}% relevance</span>
                        </div>
                        <div class="thin-progress-bg">
                            <div class="thin-progress-fill" style="width: {relevance_pct}%;"></div>
                        </div>
                        <div style="margin-top: 4px;"><span class="mono-tag">{src.chunk_id}</span></div>
                        <div class="source-excerpt">"{src.text_preview}"</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No sources attributed for this query.")


if __name__ == "__main__":
    main()

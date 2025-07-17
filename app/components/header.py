import streamlit as st
import os
import sys

# Add the app directory to the Python path if not already there
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

try:
    from app.utils.i18n import t
    from app.config.constants import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
except ImportError:
    # Fallback imports for deployment environments
    try:
        from utils.i18n import t
        from config.constants import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
    except ImportError:
        # Final fallback with hardcoded values
        def t(key, lang="he", **kwargs):
            fallback_translations = {
                "common.search": {"he": "חיפוש", "en": "Search"},
            }
            return fallback_translations.get(key, {}).get(lang, key)
        
        SUPPORTED_LANGUAGES = ["en", "he", "fr", "ru"]
        DEFAULT_LANGUAGE = "he"

def render_header(current_language=DEFAULT_LANGUAGE, on_language_change=None, search_query="", on_search=None):
    """
    Render the app header in the following order:
    1. Language icons (horizontal row)
    2. Banner image
    3. Search box
    """
    # Mobile-optimized CSS for header
    st.markdown(
        """
        <style>
        /* Remove default Streamlit padding/margin from top */
        .main .block-container { padding-top: 0rem; padding-bottom: 0rem; }
        .stApp > header { height: 0rem; }
        .stMainBlockContainer {padding: 1rem 1rem 10rem;} 
        .header-lang-row { display: flex; flex-direction: row; justify-content: center; gap: 0.5em; margin-bottom: 0.5em; }
        .header-banner { display: flex; justify-content: center; margin-bottom: 0.5em; }
        .header-search-row { display: flex; justify-content: center; margin-bottom: 1em; }
        .header-search-row input { font-size: 1.2em; padding: 0.7em; border-radius: 0.5em; }
        @media (max-width: 640px) {
            .header-banner, .header-search-row { flex-direction: column; align-items: center; }

            ### Mandatory for lang flags button will be horizontaly in mobile view
            .stColumn[data-testid="stColumn"]:has(div[data-testid="stVerticalBlock"]):has(div[class*="st-key-lang"]) {
                min-width: auto !important;
            }
            div[data-testid="stColumn"]:has(div[data-testid="stVerticalBlock"]):has(div[class*="st-key-lang"]) {
                min-width: auto !important;
            }

        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # 1. Language icons row
    lang_labels = {"en": "🇬🇧", "he": "🇮🇱", "fr": "🇫🇷", "ru": "🇷🇺"}
    lang_cols = st.columns(len(SUPPORTED_LANGUAGES))
    for i, lang in enumerate(SUPPORTED_LANGUAGES):
        with lang_cols[i]:
            if st.button(lang_labels.get(lang, lang), key=f"lang_{lang}"):
                if on_language_change:
                    on_language_change(lang)
    # 2. Banner image
    st.markdown('<div class="header-banner">', unsafe_allow_html=True)
    try:
        st.image("assets/images/banner.png", use_container_width=True)
    except Exception:
        st.markdown("**Netanya App** (Banner image not found)")
    st.markdown('</div>', unsafe_allow_html=True)
    # 3. Search box
    if search_query is not None and on_search is not None:
        st.markdown('<div class="header-search-row">', unsafe_allow_html=True)
        search_col1, search_col2 = st.columns([4,1])
        with search_col1:
            # Use search_query parameter to control the input value for proper clearing
            search_input = st.text_input(
                t("common.search", current_language),
                value=search_query if search_query else "",
                key="header_search_input", 
                placeholder=t("common.search", current_language),
                label_visibility="collapsed"
            )
        with search_col2:
            if st.button("🔍", key="search_btn"):
                if on_search:
                    on_search()
        st.markdown('</div>', unsafe_allow_html=True)
    # RTL styling for Hebrew
    if current_language == "he":
        st.markdown("""
        <style>
        .stApp { direction: rtl; text-align: right; }
        </style>
        """, unsafe_allow_html=True) 
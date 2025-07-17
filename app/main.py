import streamlit as st
import os
import sys
from dotenv import load_dotenv
import random
import streamlit.components.v1 as components

load_dotenv()

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try different import strategies for deployment compatibility
try:
    from app.components.header import render_header
    from app.components.grid_view import create_grid_view
    from app.components.popups import show_data_collection_popup, show_success_popup, show_error_popup
    from app.services.api_service import APIService
    from app.services.supabase_service import SupabaseService
    from app.services.storage_service import StorageService
    from app.config.settings import load_config
    from app.utils.i18n import t
except ImportError:
    # Fallback for deployment environments
    try:
        from components.header import render_header
        from components.grid_view import create_grid_view
        from components.popups import show_data_collection_popup, show_success_popup, show_error_popup
        from services.api_service import APIService
        from services.supabase_service import SupabaseService
        from services.storage_service import StorageService
        from config.settings import load_config
        from utils.i18n import t
    except ImportError as e:
        st.error(f"Import error: {e}")
        st.stop()

# --- Session state keys ---
def init_session_state():
    # Initialize storage service for session state setup
    storage = StorageService()
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "categories"
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_street" not in st.session_state:
        st.session_state.selected_street = None
    if "user_data" not in st.session_state:
        st.session_state.user_data = storage.load_user_data()
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False
    if "ticket_history" not in st.session_state:
        st.session_state.ticket_history = storage.get_ticket_history()
    if "current_language" not in st.session_state:
        st.session_state.current_language = "he"
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "categories_data" not in st.session_state:
        st.session_state.categories_data = None
    if "streets_data" not in st.session_state:
        st.session_state.streets_data = None

# --- Main app logic ---
def main():
    init_session_state()
    lang = st.session_state.current_language
    config = load_config()
    api = APIService(endpoint=config.api_endpoint, debug_mode=config.debug_mode)
    supabase = SupabaseService(config.supabase_url, config.supabase_key)
    storage = StorageService()

# Inject Google Analytics tracking script
# Include Google Analytics tracking code
    with open("google_analytics.html", "r") as f:
        html_code = f.read()
        components.html(html_code, height=0)

    st.title("My Streamlit App")

    # Sidebar: Ticket History
    with st.sidebar:
        tickets = storage.get_ticket_history()
        if tickets:
            st.markdown(f"### {t('common.ticket_history', lang)}")
            for tkt in tickets:
                st.markdown(f"- {tkt}")

    # Fetch categories and streets from Supabase (cache in session)
    if st.session_state.categories_data is None:
        st.session_state.categories_data = supabase.get_categories()
    if st.session_state.streets_data is None:
        st.session_state.streets_data = supabase.get_street_numbers()

    def on_language_change(new_lang):
        st.session_state.current_language = new_lang
        st.rerun()

    def on_search():
        # This function is called when search input changes
        pass  # Real-time search is handled below

    render_header(
        current_language=lang,
        on_language_change=on_language_change,
        search_query=st.session_state.search_query,  # Pass current search query for proper clearing
        on_search=on_search
    )

    # Real-time search: Check if search input has changed and update immediately
    current_search_input = st.session_state.get("header_search_input", "")
    if current_search_input != st.session_state.search_query:
        st.session_state.search_query = current_search_input
        st.rerun()

    categories = st.session_state.categories_data or []
    streets = st.session_state.streets_data or []

    if st.session_state.current_page == "categories":
        if not categories:
            st.warning("No categories found in Supabase.")
        def on_category_click(category):
            st.session_state.selected_category = category
            # Clear custom text when switching categories (will be regenerated in summary)
            st.session_state.custom_text = ""
            if not st.session_state.user_data:
                st.session_state.show_popup = True
                st.rerun()
            else:
                st.session_state.current_page = "streets"
                st.session_state.search_query = ""
                # Clear the search input when changing pages
                if "header_search_input" in st.session_state:
                    del st.session_state["header_search_input"]
                st.rerun()
        if st.session_state.show_popup:
            def save_user(user):
                st.session_state.user_data = user
                storage.save_user_data(user)  # <-- Add this line
                st.session_state.show_popup = False
                st.session_state.current_page = "streets"
                st.session_state.search_query = ""
                # Clear popup form keys and search input
                for k in ["popup_first_name", "popup_last_name", "popup_id", "popup_phone", "popup_email", "header_search_input", "custom_text"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
            def cancel_user():
                st.session_state.show_popup = False
                st.session_state.selected_category = None
                st.session_state.custom_text = ""
                st.session_state.search_query = ""
                if "header_search_input" in st.session_state:
                    del st.session_state["header_search_input"]
                st.session_state.current_page = "categories"
                st.rerun()
            show_data_collection_popup(save_user, cancel_user, lang=lang)
        else:
            create_grid_view(categories, on_category_click, search_query=st.session_state.search_query, search_fn=supabase.search_categories)
    elif st.session_state.current_page == "streets":
        if not streets:
            st.warning("No street numbers found in Supabase.")
        def on_street_click(street):
            st.session_state.selected_street = street
            st.session_state.current_page = "summary"
            # Clear search when moving to summary
            st.session_state.search_query = ""
            if "header_search_input" in st.session_state:
                del st.session_state["header_search_input"]
            st.rerun()  # <-- This line is necessary for immediate navigation
        create_grid_view(streets, on_street_click, search_query=st.session_state.search_query, search_fn=supabase.search_street_numbers)
    elif st.session_state.current_page == "summary":
        user = st.session_state.user_data
        category = st.session_state.selected_category
        street = st.session_state.selected_street
        
        # Validate that all required data is present
        if not user or not category or not street:
            st.error("Missing required data. Redirecting to categories...")
            st.session_state.current_page = "categories"
            st.session_state.selected_category = None
            st.session_state.selected_street = None
            st.rerun()
            return
            
        st.markdown(f"**{t('forms.first_name', lang)}:** {user.first_name}")
        st.markdown(f"**{t('forms.last_name', lang)}:** {user.last_name}")
        st.markdown(f"**{t('forms.phone', lang)}:** {user.phone}")
        st.markdown(f"**{t('forms.email', lang)}:** {user.email or '-'}")
        st.markdown(f"**{t('forms.id_optional', lang)}:** {user.user_id or '-'}")
        st.markdown(f"**{t('forms.category', lang)}:** {category.name}")
        st.markdown(f"**{t('forms.street', lang)}:** {street.name}")

        # Editable text field with random description as default
        if category.event_call_desc:
            options = [s.strip() for s in category.event_call_desc.split(',') if s.strip()]
            if options:
                # Initialize custom text with random description if not already set or if empty
                if "custom_text" not in st.session_state or not st.session_state.custom_text:
                    st.session_state.custom_text = random.choice(options)
                
                # Show editable text area
                st.markdown(f"**{t('forms.text', lang)}:**")
                custom_text = st.text_area(
                    label="Edit Text",  # Use fixed label instead of potentially empty translation
                    value=st.session_state.custom_text,
                    height=100,
                    key="summary_text_input",
                    label_visibility="collapsed"
                )
                # Update session state when text changes
                if custom_text != st.session_state.custom_text:
                    st.session_state.custom_text = custom_text
        
        # Future-proof: file upload (disabled for now)
        uploaded_file = st.file_uploader("Upload a file (optional, not sent yet)", disabled=True)
        if st.button(t('common.send', lang), type="primary"):
            # To enable file upload in the future, pass extra_files to api.submit_data
            extra_files = None
            # if uploaded_file:
            #     extra_files = {"attachment": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            
            # Pass custom text to API service
            custom_text = st.session_state.get("custom_text", "")
            
            response = api.submit_data(user, category, street, custom_text=custom_text, extra_files=extra_files)
            if response.ResultCode == 200 and "SUCCESS" in response.ResultStatus:
                ticket = response.data
                st.session_state.ticket_history.append(ticket)
                storage.save_ticket(ticket)
                st.session_state.last_ticket_number = ticket
                st.session_state.current_page = "success"
                st.rerun()
            else:
                st.error(f"❌ {t('errors.submission_failed', lang)}: {response.ResultMessage}")

    elif st.session_state.current_page == "success":
        
        # Get ticket info from session state
        ticket_number = st.session_state.get('last_ticket_number')
        user_data = st.session_state.get('user_data')
        category_data = st.session_state.get('selected_category')
        street_data = st.session_state.get('selected_street')
        
        # Success message container
        with st.container():
            st.markdown(
                f"""
                <div style="text-align: center; padding: 2rem; background: #d4edda; 
                            border: 1px solid #c3e6cb; border-radius: 8px; margin: 2rem 0;">
                    <h2 style="color: #155724; margin-bottom: 1rem;">
                        ✅ {t('success.title', lang)}
                    </h2>
                    <h3 style="color: #155724; margin-bottom: 2rem;">
                        {t('success.ticket_number', lang)}: <strong>{ticket_number or 'N/A'}</strong>
                    </h3>
                    <p style="color: #155724; font-size: 1.1rem; margin-bottom: 1rem;">
                        {t('success.message', lang)}
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Action buttons
        st.markdown("---")
        col1, col3 = st.columns([1, 1])
        
        with col1:
            if st.button(t('success.new_ticket', lang), type="primary", use_container_width=True):
                # Clear session state and start over
                for key in ['user_data', 'selected_category', 'selected_street', 'last_ticket_number', 'custom_text']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.current_page = "categories"
                st.rerun()
                
        with col3:
            if st.button(t('success.back_home', lang), use_container_width=True):
                st.session_state.current_page = "categories"
                st.rerun()

if __name__ == "__main__":
    main()

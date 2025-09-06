import streamlit as st
from streamlit_gtag import st_gtag
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

    config = load_config()
    st.set_page_config(
        page_title="Netanya Municipality", 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    st_gtag(
        key="gtag_send_event_a",
        id=config.ga_id,
        event_name="app_main_page",
        params={
            "event_category": "send_page_view",
            "event_label": "send_page_view",
            "value": 1,
        }
    )

    init_session_state()
    lang = st.session_state.current_language
    api = APIService(endpoint=config.api_endpoint, debug_mode=config.debug_mode)
    supabase = SupabaseService(config.supabase_url, config.supabase_key)
    storage = StorageService()

    # Handle URL parameters for direct navigation
    def handle_url_parameters():
        """Handle URL parameters to pre-fill category and street selections"""
        try:
            # Get URL parameters from Streamlit
            query_params = st.query_params
            
            category_id = query_params.get("category_id") or query_params.get("category")
            street_id = query_params.get("street_id") or query_params.get("street")
            
            if category_id and street_id:
                # Only process if we haven't already processed these parameters
                if not st.session_state.get("url_params_processed", False):
                    # Fetch data if not already cached
                    if st.session_state.categories_data is None:
                        st.session_state.categories_data = supabase.get_categories()
                    if st.session_state.streets_data is None:
                        st.session_state.streets_data = supabase.get_street_numbers()
                    
                    categories = st.session_state.categories_data or []
                    streets = st.session_state.streets_data or []
                    
                    # Find matching category and street
                    selected_category = None
                    selected_street = None
                    
                    for category in categories:
                        if str(category.id) == str(category_id):
                            selected_category = category
                            break
                    
                    for street in streets:
                        if str(street.id) == str(street_id):
                            selected_street = street
                            break
                    
                    if selected_category and selected_street:
                        # Set the selections in session state
                        st.session_state.selected_category = selected_category
                        st.session_state.selected_street = selected_street
                        
                        # Clear URL parameters
                        st.query_params.clear()
                        
                        # Check if user has personal data
                        user_data = st.session_state.user_data
                        if user_data:
                            # User has data, go directly to summary
                            st.session_state.current_page = "summary"
                            # Clear search when navigating to summary
                            st.session_state.search_query = ""
                            if "header_search_input" in st.session_state:
                                del st.session_state["header_search_input"]
                        else:
                            # User needs to fill personal data first
                            st.session_state.current_page = "categories"
                            st.session_state.show_popup = True
                        
                        # Mark URL parameters as processed
                        st.session_state.url_params_processed = True
                        st.rerun()
                        
        except Exception as e:
            # If there's any error with URL processing, just continue normally
            print(f"Error processing URL parameters: {e}")

    # Call the URL parameter handler
    handle_url_parameters()

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

    # Hide search on summary page, show on categories and streets pages
    show_search = st.session_state.current_page in ["categories", "streets"]
    
    render_header(
        current_language=lang,
        on_language_change=on_language_change,
        search_query=st.session_state.search_query if show_search else None,
        on_search=on_search if show_search else None
    )

    # Real-time search: Check if search input has changed and update immediately
    current_search_input = st.session_state.get("header_search_input", "")
    # print(f"DEBUG search: current_search_input='{current_search_input}', session_search_query='{st.session_state.search_query}'")
    if current_search_input != st.session_state.search_query:
        # print(f"DEBUG search: updating search_query from '{st.session_state.search_query}' to '{current_search_input}'")
        st.session_state.search_query = current_search_input
        st.rerun()

    categories = st.session_state.categories_data or []
    streets = st.session_state.streets_data or []

    if st.session_state.current_page == "categories":
        if not categories:
            st.warning("No categories found in Supabase.")
        def on_category_click(category):
            print(f"DEBUG: Category clicked: {category.name}")
            print(f"DEBUG: Current user_data: {st.session_state.user_data}")
            print(f"DEBUG: Current selected_street: {st.session_state.selected_street}")
            st_gtag(
                key="gtag_send_event_b",
                id=config.ga_id,
                event_name="custom_event",
                params={
                    "event_category": "category_clicked",
                    "event_label": "category_"+category.name,
                    "value": 1,
                }
            )
            st.session_state.selected_category = category
            # Clear selected street when selecting a new category
            st.session_state.selected_street = None
            # Clear custom text when switching categories (will be regenerated in summary)
            st.session_state.custom_text = ""
            # Mark that we've manually selected, not from URL params
            st.session_state.url_params_processed = True
            if not st.session_state.user_data:
                print("DEBUG: No user data, showing popup")
                st.session_state.show_popup = True
                st.rerun()
            else:
                print("DEBUG: User data exists, going to streets page")
                # Always go to streets page after selecting category (need to select street too)
                st.session_state.current_page = "streets"
                st.session_state.search_query = ""
                # Clear the search input when changing pages
                if "header_search_input" in st.session_state:
                    del st.session_state["header_search_input"]
                st.rerun()
        if st.session_state.show_popup:
            def save_user(user):
                st.session_state.user_data = user
                storage.save_user_data(user)
                st.session_state.show_popup = False
                
                # Debug: Check current state
                print(f"DEBUG save_user: selected_category = {st.session_state.selected_category}")
                print(f"DEBUG save_user: selected_street = {st.session_state.selected_street}")
                print(f"DEBUG save_user: selected_category is None? {st.session_state.selected_category is None}")
                print(f"DEBUG save_user: selected_street is None? {st.session_state.selected_street is None}")
                print(f"DEBUG save_user: bool(selected_category) = {bool(st.session_state.selected_category)}")
                print(f"DEBUG save_user: bool(selected_street) = {bool(st.session_state.selected_street)}")
                
                # Check if we already have both category and street selected (from URL params)
                if st.session_state.selected_category and st.session_state.selected_street:
                    # Both are selected, go directly to summary
                    print("DEBUG save_user: Both category and street selected, going to summary")
                    st.session_state.current_page = "summary"
                    # Clear search when navigating to summary
                    st.session_state.search_query = ""
                    if "header_search_input" in st.session_state:
                        del st.session_state["header_search_input"]
                else:
                    # Need to select street, go to streets page
                    print("DEBUG save_user: Missing street, going to streets page")
                    st.session_state.current_page = "streets"
                
                st.session_state.search_query = ""
                # Clear popup form keys and search input
                for k in ["popup_first_name", "popup_last_name", "popup_id", "popup_phone", "popup_email", "header_search_input", "custom_text"]:
                    if k in st.session_state:
                        del st.session_state[k]
                
                # Give localStorage time to save before rerunning
                import time
                time.sleep(0.5)  # 200ms delay
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
            create_grid_view(categories, on_category_click, search_query=st.session_state.search_query, search_fn=lambda q: supabase.search_categories(q, categories), page_key="categories")
    elif st.session_state.current_page == "streets":
        if not streets:
            st.warning("No street numbers found in Supabase.")
        def on_street_click(street):
            st_gtag(
                key="gtag_send_event_c",
                id=config.ga_id,
                event_name="custom_event",
                params={
                    "event_category": "category_clicked",
                    "event_label": "street_" + street.id,
                    "value": 1,
                }
            )
            st.session_state.selected_street = street
            st.session_state.current_page = "summary"
            # Clear search when moving to summary
            st.session_state.search_query = ""
            if "header_search_input" in st.session_state:
                del st.session_state["header_search_input"]
            st.rerun()  # <-- This line is necessary for immediate navigation
        create_grid_view(streets, on_street_click, search_query=st.session_state.search_query, search_fn=lambda q: supabase.search_street_numbers(q, streets), page_key="streets")
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
        # uploaded_file = st.file_uploader("Upload a file (optional, not sent yet)", disabled=True)
        if st.button(t('common.send', lang), type="primary"):
            # To enable file upload in the future, pass extra_files to api.submit_data
            extra_files = None
            # if uploaded_file:
            #     extra_files = {"attachment": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            
            # Pass custom text to API service
            custom_text = st.session_state.get("custom_text", "")
            
            response = api.submit_data(user, category, street, custom_text=custom_text, extra_files=None)
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
            # Create WhatsApp share URL
            category_id = category_data.id if category_data else ""
            street_id = street_data.id if street_data else ""
            share_url = f"https://agamim.streamlit.app?category={category_id}%26street={street_id}"
            print(share_url)
            whatsapp_text = t('success.share_neighbor_text', lang)
            whatsapp_url = f"https://wa.me/?text={whatsapp_text}%20{share_url}"
            
            # Use st.link_button for WhatsApp sharing
            st.link_button(
                t('success.share_neighbor', lang), 
                whatsapp_url, 
                use_container_width=True
            )

if __name__ == "__main__":
    main()

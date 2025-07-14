import streamlit as st
from app.components.header import render_header
from app.components.grid_view import create_grid_view
from app.components.popups import show_data_collection_popup, show_success_popup, show_error_popup
from app.services.api_service import APIService
from app.services.supabase_service import SupabaseService
from app.services.storage_service import StorageService
from app.config.settings import load_config
from app.utils.models import Category, StreetNumber, UserData
from app.utils.i18n import t
from dotenv import load_dotenv
import random
load_dotenv()

storage = StorageService()  # <-- Move this to the top, after imports

# --- Session state keys ---
def init_session_state():
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
        st.session_state.current_language = "en"
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
        # Debounced: only update search_query when search button is pressed
        st.session_state.search_query = st.session_state.get("header_search_input", "")
        st.rerun()

    render_header(
        current_language=lang,
        on_language_change=on_language_change,
        search_query=st.session_state.search_query,
        on_search=on_search
    )

    categories = st.session_state.categories_data or []
    streets = st.session_state.streets_data or []

    if st.session_state.current_page == "categories":
        if not categories:
            st.warning("No categories found in Supabase.")
        def on_category_click(category):
            st.session_state.selected_category = category
            if not st.session_state.user_data:
                st.session_state.show_popup = True
                st.rerun()
            else:
                st.session_state.current_page = "streets"
                st.session_state.search_query = ""
                st.rerun()
        if st.session_state.show_popup:
            def save_user(user):
                st.session_state.user_data = user
                storage.save_user_data(user)  # <-- Add this line
                st.session_state.show_popup = False
                st.session_state.current_page = "streets"
                st.session_state.search_query = ""
                # Clear popup form keys
                for k in ["popup_first_name", "popup_last_name", "popup_id", "popup_phone", "popup_email"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
            def cancel_user():
                st.session_state.show_popup = False
                st.session_state.selected_category = None
            show_data_collection_popup(save_user, cancel_user, lang=lang)
        else:
            create_grid_view(categories, on_category_click, search_query=st.session_state.search_query, search_fn=supabase.search_categories)
    elif st.session_state.current_page == "streets":
        if not streets:
            st.warning("No street numbers found in Supabase.")
        def on_street_click(street):
            st.session_state.selected_street = street
            st.session_state.current_page = "summary"
            st.rerun()  # <-- This line is necessary for immediate navigation
        create_grid_view(streets, on_street_click, search_query=st.session_state.search_query, search_fn=supabase.search_street_numbers)
    elif st.session_state.current_page == "summary":
        user = st.session_state.user_data
        category = st.session_state.selected_category
        street = st.session_state.selected_street
        st.markdown(f"**{t('forms.first_name', lang)}:** {user.first_name}")
        st.markdown(f"**{t('forms.last_name', lang)}:** {user.last_name}")
        st.markdown(f"**{t('forms.id', lang)}:** {user.user_id}")
        st.markdown(f"**{t('forms.phone', lang)}:** {user.phone}")
        st.markdown(f"**{t('forms.email', lang)}:** {user.email or '-'}")
        st.markdown(f"**{t('forms.category', lang)}:** {category.name}")
        st.markdown(f"**{t('forms.street', lang)}:** {street.name}")
        # Show a random event_call_desc split by comma
        if category.event_call_desc:
            options = [s.strip() for s in category.event_call_desc.split(',') if s.strip()]
            if options:
                random_desc = random.choice(options)
                st.markdown(f"**{t('forms.text', lang)}:** {random_desc}")
        # Future-proof: file upload (disabled for now)
        uploaded_file = st.file_uploader("Upload a file (optional, not sent yet)", disabled=True)
        if st.button("SEND", type="primary"):
            # To enable file upload in the future, pass extra_files to api.submit_data
            extra_files = None
            # if uploaded_file:
            #     extra_files = {"attachment": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = api.submit_data(user, category, street, extra_files=extra_files)
            if response.ResultCode == 200 and "SUCCESS" in response.ResultStatus:
                ticket = response.data or response.ResultData.get("incidentNumber")
                st.session_state.ticket_history.append(ticket)
                storage.save_ticket(ticket)
                def restart():
                    st.session_state.current_page = "categories"
                    st.session_state.selected_category = None
                    st.session_state.selected_street = None
                    st.session_state.search_query = ""
                show_success_popup(ticket, restart, lang=lang)
            else:
                def restart():
                    st.session_state.current_page = "categories"
                    st.session_state.selected_category = None
                    st.session_state.selected_street = None
                    st.session_state.search_query = ""
                show_error_popup(restart, lang=lang)

if __name__ == "__main__":
    main() 
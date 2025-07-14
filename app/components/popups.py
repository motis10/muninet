import streamlit as st
from app.utils.i18n import t
from app.utils.validation import validate_user_data

# Mobile-optimized CSS for popups
st.markdown(
    """
    <style>
    .stForm input, .stForm textarea {
        font-size: 1.1em;
        padding: 0.7em;
        border-radius: 0.5em;
    }
    .stForm button {
        font-size: 1.1em;
        padding: 0.7em 1.2em;
        border-radius: 0.5em;
        margin-top: 0.5em;
    }
    @media (max-width: 600px) {
        .stForm .stColumns { flex-direction: column !important; }
        .stForm .stColumns > div { width: 100% !important; max-width: 100% !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def show_data_collection_popup(on_save, on_cancel, lang="en"):
    """Show popup for collecting user data."""
    st.markdown(f"### {t('common.save', lang)}")
    with st.form("user_data_form", clear_on_submit=False):
        first_name = st.text_input(t("forms.first_name", lang), key="popup_first_name")
        last_name = st.text_input(t("forms.last_name", lang), key="popup_last_name")
        user_id = st.text_input(t("forms.id", lang), key="popup_id")
        phone = st.text_input(t("forms.phone", lang), key="popup_phone")
        email = st.text_input(t("forms.email", lang), key="popup_email")
        col1, col2 = st.columns(2)
        with col1:
            save_clicked = st.form_submit_button(t("common.save", lang))
        with col2:
            cancel_clicked = st.form_submit_button(t("common.cancel", lang))
        if save_clicked:
            from app.utils.models import UserData
            user = UserData(first_name, last_name, user_id, phone, email)
            result = validate_user_data(user)
            if result.is_valid:
                on_save(user)
            else:
                for err in result.errors:
                    st.error(t(f"validation.{err}", lang))
        if cancel_clicked:
            on_cancel()

def show_success_popup(ticket_number, on_restart, lang="en"):
    """Show success popup with ticket number."""
    st.success(t("messages.success_message", lang, ticket_number=ticket_number))
    if st.button(t("common.start_over", lang), key="success_restart"):
        on_restart()

def show_error_popup(on_restart, lang="en"):
    """Show error popup."""
    st.error(t("messages.error_message", lang))
    if st.button(t("common.try_again", lang), key="error_restart"):
        on_restart()

def show_generic_popup(message, on_close=None, success=True, lang="en"):
    """Show a generic popup for any error or success scenario."""
    if success:
        st.success(message)
    else:
        st.error(message)
    if on_close and st.button(t("common.cancel", lang), key="popup_close"):
        on_close() 
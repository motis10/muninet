import streamlit as st
from app.utils.i18n import t
import logging

def handle_api_error(error, lang="he"):
    if hasattr(error, "__class__") and error.__class__.__name__ == "ConnectionError":
        st.error(t("api_error.network", lang))
    elif hasattr(error, "__class__") and error.__class__.__name__ == "Timeout":
        st.error(t("api_error.timeout", lang))
    else:
        st.error(t("api_error.generic", lang))
    logging.error(f"API Error: {error}")

def handle_validation_error(errors, lang="he"):
    for error in errors:
        st.error(t(error, lang))

def handle_database_error(error, lang="he"):
    st.error(t("database_error.generic", lang))
    logging.error(f"Database Error: {error}") 
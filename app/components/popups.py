import streamlit as st
from app.utils.i18n import t
from app.utils.validation import validate_user_data
import random
from app.utils.models import UserData

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

def show_data_collection_popup(on_save, on_cancel, lang="he"):
    """Show popup for collecting user data."""
    st.markdown(f"### {t('common.save', lang)}")
    st.markdown(f"<span style='color: red;'>* {t('common.one_time', lang)}</span>", unsafe_allow_html=True)

    user = generate_random_user_data()
    with st.form("user_data_form", clear_on_submit=False):
        first_name = st.text_input(t("forms.first_name", lang), key="popup_first_name", value=user.first_name)
        last_name = st.text_input(t("forms.last_name", lang), key="popup_last_name", value=user.last_name)
        phone = st.text_input(t("forms.phone", lang), key="popup_phone", value="")
        email = st.text_input(t("forms.email", lang), key="popup_email", value=user.email)
        user_id = st.text_input(t("forms.id_optional", lang), key="popup_id")
        col1, col2 = st.columns(2)
        with col1:
            save_clicked = st.form_submit_button(t("common.save", lang))
        with col2:
            cancel_clicked = st.form_submit_button(t("common.cancel", lang))
        if save_clicked:
            from app.utils.models import UserData
            user = UserData(first_name, last_name, phone, user_id, email)
            result = validate_user_data(user)
            if result.is_valid:
                on_save(user)
            else:
                for err in result.errors:
                    st.error(t(f"validation.{err}", lang))
        if cancel_clicked:
            on_cancel()

def show_success_popup(ticket_number, on_restart, lang="he"):
    """Show success popup with ticket number."""
    st.success(t("messages.success_message", lang, ticket_number=ticket_number))
    if st.button(t("common.start_over", lang), key="success_restart"):
        on_restart()

def show_error_popup(on_restart, lang="he"):
    """Show error popup."""
    st.error(t("messages.error_message", lang))
    if st.button(t("common.try_again", lang), key="error_restart"):
        on_restart()

def show_generic_popup(message, on_close=None, success=True, lang="he"):
    """Show a generic popup for any error or success scenario."""
    if success:
        st.success(message)
    else:
        st.error(message)
    if on_close and st.button(t("common.cancel", lang), key="popup_close"):
        on_close() 


def generate_random_user_data() -> UserData:
    """Generate random user data for development/testing purposes."""
    # Hebrew/Israeli first names
    first_names = [
        "דוד", "משה", "יוסף", "אברהם", "דניאל", "מיכאל", "אליהו", "יעקב", "ישראל", "יהודה",
        "שרה", "רחל", "לאה", "מרים", "אסתר", "חנה", "רבקה", "תמר", "נעמי", "רות",
        "אדם", "בן", "גל", "דור", "זיו", "חן", "טל", "יובל", "כפיר", "לב",
        "מיה", "נועה", "עדן", "פרל", "צהלה", "קרן", "שחר", "תהלה", "אוריה", "בר"
    ]
    
    # Hebrew/Israeli last names
    last_names = [
        "כהן", "לוי", "מזרחי", "פרץ", "אזולאי", "דהן", "אברהם", "דוד", "יוסף", "חדד",
        "ביטון", "עמר", "שמש", "אסף", "בוזגלו", "כרמי", "גרין", "רוזנברג", "שוורץ", "גולדמן",
        "ישראלי", "נתניהו", "ברק", "שרון", "לפיד", "גנץ", "בנט", "ליברמן", "אולמרט", "פרס",
        "זכאי", "בצלאל", "אורון", "צבר", "גלבוע", "כרמל", "גולן", "נגב", "שרון", "ירון"
    ]
    
    # Generate random data
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Convert Hebrew names to ASCII for email (simplified transliteration)
    email_first = transliterate_hebrew(first_name)
    email_last = transliterate_hebrew(last_name)
    email = f"{email_first.lower()}.{email_last.lower()}@gmail.com"
            
    return UserData(
        first_name=first_name,
        last_name=last_name,
        phone="",
        user_id="",  # Keep ID empty
        email=email
    )

def transliterate_hebrew(hebrew_text: str) -> str:
    """Simple Hebrew to ASCII transliteration for email generation."""
    transliteration_map = {
        'א': 'a', 'ב': 'b', 'ג': 'g', 'ד': 'd', 'ה': 'h', 'ו': 'v', 'ז': 'z', 'ח': 'ch',
        'ט': 't', 'י': 'y', 'כ': 'k', 'ך': 'k', 'ל': 'l', 'מ': 'm', 'ם': 'm', 'ן': 'n',
        'נ': 'n', 'ס': 's', 'ע': 'a', 'פ': 'p', 'ף': 'f', 'צ': 'tz', 'ץ': 'tz', 'ק': 'k',
        'ר': 'r', 'ש': 'sh', 'ת': 't'
    }
    
    result = ""
    for char in hebrew_text:
        result += transliteration_map.get(char, char)
    
    return result if result else "user"


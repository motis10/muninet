import json
import os
from functools import lru_cache

# Multiple path strategies for different deployment environments
def get_translations_path():
    # Try different possible paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '../../assets/translations'),  # From app/utils/
        os.path.join(os.path.dirname(os.path.dirname(__file__)), '../assets/translations'),  # From app/
        os.path.join(os.getcwd(), 'assets/translations'),  # From root
        'assets/translations',  # Direct path
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
    
    # Return the first path as fallback
    return os.path.abspath(possible_paths[0])

TRANSLATIONS_PATH = get_translations_path()

def get_fallback_translations(lang):
    """Fallback translations when files can't be loaded"""
    fallback = {
        "he": {
            "common": {
                "search": "חיפוש",
                "save": "שמור",
                "send": "שלח",
                "cancel": "ביטול",
                "one_time": "יש למלא פרטים אישיים פעם אחת בלבד",
                "ticket_history": "היסטוריית תקלות"
            },
            "forms": {
                "first_name": "שם פרטי",
                "last_name": "שם משפחה",
                "phone": "טלפון",
                "email": "אימייל - לא חובה",
                "id_optional": "תז - לא חובה",
                "category": "קטגוריה",
                "street": "רחוב",
                "text": "תלונה"
            },
            "success": {
                "title": "נפתחה קריאה חדשה",
                "message": "הבקשה שלך נשלחה בהצלחה.",
                "ticket_number": "מס קריאה",
                "new_ticket": "פתח קריאה חדשה",
                "back_home": "חזרה לדף הבית"
            },
            "errors": {
                "submission_failed": "שליחת הבקשה נכשלה"
            }
        },
        "en": {
            "common": {
                "search": "Search",
                "save": "Save",
                "send": "Send",
                "cancel": "Cancel",
                "one_time": "Fill it one time only",
                "ticket_history": "Ticket History"
            },
            "forms": {
                "first_name": "First Name",
                "last_name": "Last Name",
                "phone": "Phone Number",
                "email": "Email (Optional)",
                "id_optional": "ID Number (Optional)",
                "category": "Category",
                "street": "Street",
                "text": "Complain Text"
            },
            "success": {
                "title": "Success",
                "message": "Your request has been submitted successfully.",
                "ticket_number": "Ticket Number",
                "new_ticket": "New Ticket",
                "back_home": "Back to Home"
            },
            "errors": {
                "submission_failed": "Request submission failed"
            }
        }
    }
    return fallback.get(lang, fallback.get("en", {}))

@lru_cache(maxsize=8)
def get_translation(lang):
    # Try multiple path strategies if the primary one fails
    possible_files = [
        os.path.join(TRANSLATIONS_PATH, f"{lang}.json"),
        os.path.join(os.getcwd(), 'assets', 'translations', f"{lang}.json"),
        os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'translations', f"{lang}.json"),
        f"assets/translations/{lang}.json",
    ]
    
    for file_path in possible_files:
        try:
            abs_path = os.path.abspath(file_path)
            if os.path.exists(abs_path):
                with open(abs_path, encoding="utf-8") as f:
                    data = json.load(f)
                    return data
        except Exception:
            continue
    
    # If all paths fail, return fallback translations
    return get_fallback_translations(lang)

def t(key: str, lang: str = "he", **kwargs) -> str:
    """Translate a key for the given language. Translations loaded from external files."""
    translations = get_translation(lang)
    
    # Support nested keys with dot notation
    value = translations
    for part in key.split('.'):
        if isinstance(value, dict):
            value = value.get(part)
        else:
            value = None
            break
    
    if not value:
        value = key
        
    if kwargs:
        try:
            value = value.format(**kwargs)
        except Exception:
            pass
    return value 
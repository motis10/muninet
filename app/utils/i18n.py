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
                "one_time": "יש למלא פעם אחת בלבד העיריה חוזרת טלפונית",
                "ticket_history": "היסטוריית תקלות"
            },
            "forms": {
                "first_name": "שם פרטי פיקטיבי (לא חובה)",
                "last_name": "שם משפחה פיקטיבי (לא חובה)",
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
                "back_home": "חזרה לדף הבית",
                "share_neighbor": "שתף עם שכן",
                "share_neighbor_text": "תעזור לי להתלונן על זה"
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
                "one_time": "Fill it one time only the city will call you",
                "ticket_history": "Ticket History"
            },
            "forms": {
                "first_name": "First Name (Optional)",
                "last_name": "Last Name (Optional)",
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
                "back_home": "Back to Home",
                "share_neighbor": "Share with Neighbor",
                "share_neighbor_text": "Help me to complain about it"
            },
            "errors": {
                "submission_failed": "Request submission failed"
            }
        },
        "fr": {
            "common": {
                "search": "Rechercher",
                "save": "Sauvegarder",
                "send": "Envoyer",
                "cancel": "Annuler",
                "one_time": "Remplir une seule fois la ville vous appellera",
                "ticket_history": "Historique des tickets"
            },
            "forms": {
                "first_name": "Prénom (Optionnel)",
                "last_name": "Nom de famille (Optionnel)",
                "phone": "Numéro de téléphone",
                "email": "Email (Optionnel)",
                "id_optional": "Numéro d'identité (Optionnel)",
                "category": "Catégorie",
                "street": "Rue",
                "text": "Texte de plainte"
            },
            "success": {
                "title": "Succès",
                "message": "Votre demande a été soumise avec succès.",
                "ticket_number": "Numéro de ticket",
                "new_ticket": "Nouveau ticket",
                "back_home": "Retour à l'accueil",
                "share_neighbor": "Partager avec un voisin",
                "share_neighbor_text": "Aidez-moi à plaindre"
            },
            "errors": {
                "submission_failed": "Échec de la soumission de la demande"
            }
        },
        "ru": {
            "common": {
                "search": "Поиск",
                "save": "Сохранить",
                "send": "Отправить",
                "cancel": "Отмена",
                "one_time": "Заполните только один раз город вам перезвонит",
                "ticket_history": "История заявок"
            },
            "forms": {
                "first_name": "Имя (Необязательно)",
                "last_name": "Фамилия (Необязательно)",
                "phone": "Номер телефона",
                "email": "Email (Необязательно)",
                "id_optional": "Номер удостоверения (Необязательно)",
                "category": "Категория",
                "street": "Улица",
                "text": "Текст жалобы"
            },
            "success": {
                "title": "Успех",
                "message": "Ваша заявка была успешно отправлена.",
                "ticket_number": "Номер заявки",
                "new_ticket": "Новая заявка",
                "back_home": "Вернуться на главную",
                "share_neighbor": "Поделиться с соседом",
                "share_neighbor_text": "Помогите мне пожаловаться"
            },
            "errors": {
                "submission_failed": "Ошибка отправки заявки"
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
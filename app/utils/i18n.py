import json
import os
from functools import lru_cache

TRANSLATIONS_PATH = os.path.join(os.path.dirname(__file__), '../../assets/translations')

@lru_cache(maxsize=8)
def get_translation(lang):
    try:
        with open(os.path.join(TRANSLATIONS_PATH, f"{lang}.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def t(key: str, lang: str = "en", **kwargs) -> str:
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
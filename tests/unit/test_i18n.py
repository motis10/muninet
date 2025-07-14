import pytest
from app.utils.i18n import t, get_translation

def test_translation_lookup():
    assert t("common.welcome", "en") == "Welcome"
    assert t("common.search", "en") == "Search"
    # Fallback to key if not found
    assert t("nonexistent.key", "en") == "nonexistent.key"

def test_translation_formatting():
    # Test formatting with kwargs
    assert t("messages.success_message", "en", ticket_number="12345").startswith("Your request has been submitted successfully.")

def test_missing_language_file():
    # Should fallback to key if file missing
    assert t("common.welcome", "zz") == "common.welcome" 
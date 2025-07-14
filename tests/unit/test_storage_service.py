import pytest
from app.services.storage_service import StorageService
from app.utils.models import UserData

class MockSessionState(dict):
    pass

@pytest.fixture(autouse=True)
def patch_streamlit_session_state(monkeypatch):
    mock_state = MockSessionState()
    monkeypatch.setattr("streamlit.session_state", mock_state)
    return mock_state

def test_save_and_load_user_data():
    service = StorageService()
    user = UserData(first_name="Alice", last_name="Smith", user_id="123", phone="555", email="alice@example.com")
    service.save_user_data(user)
    loaded = service.load_user_data()
    assert loaded.first_name == "Alice"
    assert loaded.last_name == "Smith"
    assert loaded.user_id == "123"
    assert loaded.phone == "555"
    assert loaded.email == "alice@example.com"

def test_save_and_load_language():
    service = StorageService()
    service.save_language("he")
    assert service.load_language() == "he"
    service.save_language("fr")
    assert service.load_language() == "fr"

def test_save_and_get_ticket_history():
    service = StorageService()
    service.save_ticket("TICKET-1")
    service.save_ticket("TICKET-2")
    tickets = service.get_ticket_history()
    assert tickets == ["TICKET-1", "TICKET-2"]

def test_clear_user_data():
    service = StorageService()
    user = UserData(first_name="Bob", last_name="Jones", user_id="456", phone="123", email="bob@example.com")
    service.save_user_data(user)
    service.save_language("ru")
    service.save_ticket("TICKET-3")
    service.clear_user_data()
    assert service.load_user_data() is None
    assert service.load_language() == "en"
    assert service.get_ticket_history() == [] 
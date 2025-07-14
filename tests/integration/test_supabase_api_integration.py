import pytest
from app.services.supabase_service import SupabaseService
from app.services.api_service import APIService
from app.utils.models import UserData, Category, StreetNumber

class DummySupabaseService(SupabaseService):
    def __init__(self):
        pass  # Do not call parent constructor
    def get_categories(self):
        return [Category(id=1, name="Cat1", text="A,B", image_url="", event_call_desc="desc")]
    def get_street_numbers(self):
        return [StreetNumber(id=1, name="Street1", image_url="", house_number="10")]

def test_supabase_and_api_integration():
    supabase = DummySupabaseService()
    api = APIService(endpoint="http://dummy", debug_mode=True)
    user = UserData(first_name="Test", last_name="User", user_id="111", phone="1234567890", email="test@example.com")
    categories = supabase.get_categories()
    streets = supabase.get_street_numbers()
    assert categories[0].name == "Cat1"
    assert streets[0].house_number == "10"
    response = api.submit_data(user, categories[0], streets[0])
    assert response.ResultCode == 200
    assert response.data == "MOCK-0001" 
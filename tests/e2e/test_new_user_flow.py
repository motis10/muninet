import pytest
from app.utils.models import UserData, Category, StreetNumber
from app.services.supabase_service import SupabaseService
from app.services.api_service import APIService

class DummySupabaseService(SupabaseService):
    def __init__(self):
        pass
    def get_categories(self):
        return [Category(id=1, name="Cat1", text="A,B", image_url="", event_call_desc="desc")]
    def get_street_numbers(self):
        return [StreetNumber(id=1, name="Street1", image_url="", house_number="10")]

class DummyAPIService(APIService):
    def __init__(self):
        pass
    def submit_data(self, user, category, street):
        class DummyResponse:
            ResultCode = 200
            ResultStatus = "SUCCESS CREATE"
            data = "MOCK-0001"
            ErrorDescription = ""
        return DummyResponse()

def test_new_user_complete_flow():
    supabase = DummySupabaseService()
    api = DummyAPIService()
    # Simulate user selects category
    categories = supabase.get_categories()
    selected_category = categories[0]
    # Simulate user enters data
    user = UserData(first_name="Eve", last_name="Doe", user_id="999", phone="555", email="eve@example.com")
    # Simulate user selects street
    streets = supabase.get_street_numbers()
    selected_street = streets[0]
    # Simulate submission
    response = api.submit_data(user, selected_category, selected_street)
    assert response.ResultCode == 200
    assert response.ResultStatus.startswith("SUCCESS")
    assert response.data == "MOCK-0001" 
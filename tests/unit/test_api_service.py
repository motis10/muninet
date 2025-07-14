import pytest
from app.services.api_service import APIService
from app.utils.models import UserData, Category, StreetNumber

@pytest.fixture
def dummy_data():
    user = UserData(first_name="Test", last_name="User", user_id="111", phone="1234567890", email="test@example.com")
    category = Category(id=1, name="TestCat", text="", image_url="", event_call_desc="desc")
    street = StreetNumber(id=1, name="TestStreet", image_url="", house_number="42")
    return user, category, street

def test_mock_response_in_debug_mode(dummy_data):
    api = APIService(endpoint="http://dummy", debug_mode=True)
    user, category, street = dummy_data
    response = api.submit_data(user, category, street)
    assert response.ResultCode == 200
    assert "SUCCESS" in response.ResultStatus
    assert response.data == "MOCK-0001"

def test_error_handling_on_invalid_endpoint(dummy_data):
    api = APIService(endpoint="http://invalid", debug_mode=False)
    user, category, street = dummy_data
    # Should return APIResponse with ResultCode 500 on error
    response = api.submit_data(user, category, street)
    assert response.ResultCode == 500
    assert response.ResultStatus == "ERROR" 
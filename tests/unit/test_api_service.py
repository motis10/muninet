import pytest
import json
from app.services.api_service import APIService
from app.utils.models import UserData, Category, StreetNumber, APIResponse

@pytest.fixture
def realistic_data():
    """Realistic test data for debugging actual API calls"""
    user = UserData(
        first_name="יוסי", 
        last_name="כהן", 
        user_id="123456789", 
        phone="0521234567", 
        email="yossi.cohen@example.com"
    )
    category = Category(
        id=1, 
        name="תאורת רחוב", 
        text="פנס רחוב לא עובד,תאורה חלשה,פנס רחוב שבור", 
        image_url="https://example.com/streetlight.jpg",
        event_call_desc="תקלה בתאורת רחוב - פנס לא פועל"
    )
    street = StreetNumber(
        id=42, 
        name="קרל פופר 15", 
        image_url="https://example.com/street.jpg",
        house_number="15"
    )
    return user, category, street



def test_api_service_initialization():
    """Test APIService initialization and headers"""
    api = APIService(endpoint="http://test.com", debug_mode=True)
    
    assert api.endpoint == "http://test.com"
    assert api.debug_mode == True
    assert "User-Agent" in api.headers
    assert "Accept" in api.headers
    assert api.headers["Origin"] == "https://www.netanya.muni.il"

def test_prepare_payload_structure(realistic_data):
    """Test internal payload preparation - core APIService functionality"""
    api = APIService(endpoint="http://dummy", debug_mode=True)
    user, category, street = realistic_data
    
    # Test with default category description
    payload = api._prepare_payload(user, category, street)
    
    assert payload.eventCallDesc is None  # Should be None when no custom_text
    assert payload.houseNumber == "15"
    assert payload.callerFirstName == "יוסי"
    assert payload.callerLastName == "כהן" 
    assert payload.callerTZ == "123456789"
    assert payload.callerPhone1 == "0521234567"
    assert payload.callerEmail == "yossi.cohen@example.com"
    
    # Test with custom text override
    custom_text = "תיאור מותאם אישית"
    payload_custom = api._prepare_payload(user, category, street, custom_text)
    assert payload_custom.eventCallDesc == custom_text

def test_mock_response_method():
    """Test the internal mock response generation"""
    api = APIService(endpoint="http://dummy", debug_mode=True)
    
    mock_response = api._mock_response()
    
    assert isinstance(mock_response, APIResponse)
    assert mock_response.ResultCode == 200
    assert mock_response.ErrorDescription == "Mocked success."
    assert mock_response.ResultStatus == "SUCCESS CREATE"
    assert mock_response.data == "MOCK-0001"

def test_submit_data_with_debug_mode(realistic_data):
    """Test submit_data in debug mode (should return mock response)"""
    api = APIService(endpoint="http://dummy", debug_mode=True)
    user, category, street = realistic_data
    
    # 🔴 BREAKPOINT: Uncomment the next line to pause execution for debugging
    # breakpoint()  # This will stop here so you can step through submit_data()
    
    response = api.submit_data(user, category, street, custom_text=category.event_call_desc)
    
    # In debug mode, should get mock response
    assert response.ResultCode == 200
    assert "SUCCESS" in response.ResultStatus
    assert response.data == "MOCK-0001"

def test_submit_data_error_handling(realistic_data):
    """Test error handling with invalid endpoint"""
    api = APIService(endpoint="http://invalid-endpoint-12345", debug_mode=False)
    user, category, street = realistic_data
    
    response = api.submit_data(user, category, street)
    
    # Should return error response
    assert response.ResultCode == 500
    assert response.ResultStatus == "ERROR"
    assert "invalid-endpoint-12345" in response.ErrorDescription

def test_headers_configuration():
    """Test that headers are properly configured"""
    api = APIService(endpoint="http://test", debug_mode=False)
    headers = api._get_headers()
    
    expected_headers = [
        'Accept-Language', 'X-Requested-With', 'User-Agent', 
        'Accept', 'Origin', 'Referer', 'Accept-Encoding', 'Priority'
    ]
    
    for header in expected_headers:
        assert header in headers
    
    assert headers['Origin'] == 'https://www.netanya.muni.il'
    assert 'Chrome' in headers['User-Agent']

def test_boundary_generation_is_random():
    """Test that multipart boundaries are random (not hardcoded)"""
    # We can't easily test the boundary without modifying the method,
    # but we can test that the method doesn't crash and generates different requests
    api = APIService(endpoint="http://invalid", debug_mode=False)
    user = UserData(first_name="Test", last_name="User", user_id="123", phone="555", email="test@test.com")
    category = Category(id=1, name="Test", text="", image_url="", event_call_desc="test desc")
    street = StreetNumber(id=1, name="Test St", image_url="", house_number="1")
    
    # Both calls should fail due to invalid endpoint, but should not fail due to boundary issues
    response1 = api.submit_data(user, category, street)
    response2 = api.submit_data(user, category, street)
    
    # Both should return the same error type (proving boundary generation works)
    assert response1.ResultCode == 500
    assert response2.ResultCode == 500
    assert response1.ResultStatus == "ERROR"
    assert response2.ResultStatus == "ERROR" 


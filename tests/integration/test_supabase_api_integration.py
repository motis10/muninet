import pytest
from app.services.supabase_service import SupabaseService
from app.services.api_service import APIService
from app.utils.models import UserData, Category, StreetNumber

class MockSupabaseService(SupabaseService):
    """Mock Supabase service that returns realistic test data"""
    def __init__(self):
        pass  # Do not call parent constructor
        
    def get_categories(self):
        return [
            Category(
                id=1, 
                name="תאורת רחוב", 
                text="פנס רחוב לא עובד,תאורה חלשה,פנס רחוב שבור", 
                image_url="https://example.com/streetlight.jpg",
                event_call_desc="תקלה בתאורת רחוב - פנס לא פועל"
            ),
            Category(
                id=2, 
                name="ניקיון", 
                text="זבל ברחוב,פח אשפה מלא,ניקיון דרוש", 
                image_url="https://example.com/cleaning.jpg",
                event_call_desc="בעיה בניקיון השכונה"
            )
        ]
        
    def get_street_numbers(self):
        return [
            StreetNumber(id=1, name="קרל פופר 15", image_url="", house_number="15"),
            StreetNumber(id=2, name="הרצל 42", image_url="", house_number="42"),
            StreetNumber(id=3, name="דיזנגוף 123", image_url="", house_number="123")
        ]

@pytest.fixture
def integration_user():
    """Test user for integration testing"""
    return UserData(
        first_name="שרה", 
        last_name="לוי", 
        user_id="987654321", 
        phone="0501234567", 
        email="sarah.levi@example.com"
    )

def test_data_flow_from_supabase_to_api(integration_user):
    """Test complete data flow: Supabase → User Selection → API Submission"""
    # Setup services
    supabase = MockSupabaseService()
    api = APIService(endpoint="http://dummy", debug_mode=True)
    
    # 1. Get data from "Supabase"
    categories = supabase.get_categories()
    streets = supabase.get_street_numbers()
    
    # Verify we got realistic data
    assert len(categories) == 2
    assert len(streets) == 3
    assert "תאורת רחוב" in categories[0].name
    assert "קרל פופר" in streets[0].name
    
    # 2. Simulate user selection (like what happens in the UI)
    selected_category = categories[0]  # Street lighting
    selected_street = streets[1]       # Herzl 42
    
    # 3. Submit through API service 
    response = api.submit_data(
        user_data=integration_user, 
        category=selected_category, 
        street=selected_street,
        custom_text=f"{selected_category.event_call_desc} - דיווח מ{selected_street.name}"
    )
    
    # 4. Verify integration worked
    assert response.ResultCode == 200
    assert "SUCCESS" in response.ResultStatus
    assert response.data == "MOCK-0001"

def test_multiple_category_selections(integration_user):
    """Test submitting different categories through the integration"""
    supabase = MockSupabaseService()
    api = APIService(endpoint="http://dummy", debug_mode=True)
    
    categories = supabase.get_categories()
    street = supabase.get_street_numbers()[0]
    
    # Test each category type
    for category in categories:
        response = api.submit_data(
            user_data=integration_user,
            category=category,
            street=street,
            custom_text=category.event_call_desc
        )
        
        assert response.ResultCode == 200
        assert response.data == "MOCK-0001"
        print(f"✅ Successfully submitted: {category.name}")

def test_integration_error_handling(integration_user):
    """Test error handling in the integration flow"""
    supabase = MockSupabaseService()
    api = APIService(endpoint="http://invalid-integration-test", debug_mode=False)
    
    categories = supabase.get_categories()
    streets = supabase.get_street_numbers()
    
    # This should handle the error gracefully
    response = api.submit_data(
        user_data=integration_user,
        category=categories[0],
        street=streets[0]
    )
    
    assert response.ResultCode == 500
    assert response.ResultStatus == "ERROR"
    assert "invalid-integration-test" in response.ErrorDescription

def test_payload_preparation_integration(integration_user):
    """Test that Supabase data is correctly transformed into API payload"""
    supabase = MockSupabaseService()
    api = APIService(endpoint="http://dummy", debug_mode=True)
    
    category = supabase.get_categories()[0]
    street = supabase.get_street_numbers()[2]  # Dizengoff 123
    custom_description = f"תיאור משולב: {category.event_call_desc} בכתובת {street.name}"
    
    # Test payload preparation (internal method)
    payload = api._prepare_payload(integration_user, category, street, custom_description)
    
    # Verify Supabase data made it into the payload correctly
    assert payload.eventCallDesc == custom_description
    assert payload.houseNumber == "123"  # From Dizengoff 123
    assert payload.callerFirstName == "שרה"
    assert payload.callerLastName == "לוי"
    assert payload.callerPhone1 == "0501234567"
    
    print(f"✅ Integration payload test passed for {street.name}") 
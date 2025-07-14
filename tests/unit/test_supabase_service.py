import pytest
from app.services.supabase_service import SupabaseService
from app.utils.models import Category, StreetNumber

@pytest.fixture
def mock_supabase_service():
    return SupabaseService("mock_url", "mock_key", no_client=True)

def test_search_categories_case_insensitive(mock_supabase_service):
    categories = [
        Category(id=1, name="Garbage", text="Trash, Waste", image_url="", event_call_desc="desc1"),
        Category(id=2, name="Street Light", text="Lamp, Lighting", image_url="", event_call_desc="desc2"),
        Category(id=3, name="Tree", text="Plant, Green", image_url="", event_call_desc="desc3"),
    ]
    # Search by name (case-insensitive)
    result = mock_supabase_service.search_categories("garbage", categories)
    assert len(result) == 1 and result[0].name == "Garbage"
    result = mock_supabase_service.search_categories("STREET", categories)
    assert len(result) == 1 and result[0].name == "Street Light"
    # Search by text
    result = mock_supabase_service.search_categories("waste", categories)
    assert len(result) == 1 and result[0].name == "Garbage"
    result = mock_supabase_service.search_categories("lamp", categories)
    assert len(result) == 1 and result[0].name == "Street Light"
    # No match
    result = mock_supabase_service.search_categories("notfound", categories)
    assert len(result) == 0

def test_search_street_numbers_case_insensitive(mock_supabase_service):
    streets = [
        StreetNumber(id=1, name="Herzl", image_url="", house_number="10"),
        StreetNumber(id=2, name="Bialik", image_url="", house_number="22A"),
        StreetNumber(id=3, name="Ben Gurion", image_url="", house_number="5"),
    ]
    # Search by name
    result = mock_supabase_service.search_street_numbers("herzl", streets)
    assert len(result) == 1 and result[0].name == "Herzl"
    result = mock_supabase_service.search_street_numbers("BEN", streets)
    assert len(result) == 1 and result[0].name == "Ben Gurion"
    # Search by house_number
    result = mock_supabase_service.search_street_numbers("22a", streets)
    assert len(result) == 1 and result[0].name == "Bialik"
    # No match
    result = mock_supabase_service.search_street_numbers("notfound", streets)
    assert len(result) == 0 
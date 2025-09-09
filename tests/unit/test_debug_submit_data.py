#!/usr/bin/env python3
"""
Debug script for submit_data method.
Set breakpoints in your IDE or use the breakpoint() calls to debug step by step.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.api_service import APIService
from app.utils.models import UserData, Category, StreetNumber

def test_debug_submit_data():
    """Debug the submit_data method with realistic data"""
    
    print("🔧 Setting up test data...")
    
    # Realistic test data
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
    
    print(f"👤 User: {user.first_name} {user.last_name}")
    print(f"📞 Phone: {user.phone}")
    print(f"🏠 Street: {street.name}")
    print(f"📋 Category: {category.name}")
    print("=" * 50)
    
    # Create API service in debug mode
    mock_server = "https://www.netanya.muni.il/"
    endpoint = f"{mock_server}/_layouts/15/NetanyaMuni/incidents.ashx?method=CreateNewIncident"
    api = APIService(endpoint=endpoint, debug_mode=False)
    
    print(f"🔧 API Endpoint: {endpoint}")
    print(f"🔧 Debug Mode: {api.debug_mode}")
    print("=" * 50)
        
    print("🚀 Calling submit_data...")
    
    # Call submit_data with custom text
    response1 = api.submit_data(
        user_data=user, 
        category=category, 
        street=street, 
        custom_text=category.event_call_desc
    )
    
    print("📊 Response 1 (with custom text):")
    print(f"  ResultCode: {response1.ResultCode}")
    print(f"  ResultStatus: {response1.ResultStatus}")
    print(f"  ErrorDescription: {response1.ErrorDescription}")
    print(f"  Data: {response1.data}")
    print("=" * 50)
        
    # Call submit_data without custom text
    response2 = api.submit_data(
        user_data=user, 
        category=category, 
        street=street
    )
    
    print("📊 Response 2 (without custom text):")
    print(f"  ResultCode: {response2.ResultCode}")
    print(f"  ResultStatus: {response2.ResultStatus}")
    print(f"  ErrorDescription: {response2.ErrorDescription}")
    print(f"  Data: {response2.data}")
    print("=" * 50)
    
    # Verify results
    if response1.ResultCode == 200 and response1.data == "MOCK-0001":
        print("✅ Test 1 PASSED")
    else:
        print("❌ Test 1 FAILED")
        
    if response2.ResultCode == 200 and response2.data == "MOCK-0001":
        print("✅ Test 2 PASSED")
    else:
        print("❌ Test 2 FAILED")
    
    print("\n🎉 Debug session completed!")
    return response1, response2

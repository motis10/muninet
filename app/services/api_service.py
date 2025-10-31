import requests
import json
from app.utils.models import APIResponse

class APIService:
    def __init__(self, endpoint, debug_mode):
        self.endpoint = endpoint
        self.debug_mode = debug_mode
        
    def submit_data(self, user_data, category, street, custom_text=None, extra_files=None):
        """
        Submit data to Cloud Run incident service. Returns APIResponse.
        Optionally accepts custom_text to override category.event_call_desc.
        Optionally accepts extra_files (dict) for file upload (future-proof).
        """
        if self.debug_mode:
            return self._mock_response()
            
        # Prepare JSON payload for new Cloud Run service
        payload = self._prepare_json_payload(user_data, category, street, custom_text)
        
        # Ensure endpoint has the correct path
        submit_endpoint = self.endpoint
        if not submit_endpoint.endswith('/incidents/submit'):
            if submit_endpoint.endswith('/'):
                submit_endpoint += 'incidents/submit'
            else:
                submit_endpoint += '/incidents/submit'
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            print("=" * 60)
            print("🚀 SENDING REQUEST TO CLOUD RUN SERVICE")
            print("=" * 60)
            print(f"📡 Endpoint: {submit_endpoint}")
            print(f"🔧 Headers: {headers}")
            print("📋 JSON Payload:")
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            print("=" * 60)
            
            resp = requests.post(
                submit_endpoint, 
                json=payload, 
                headers=headers, 
                timeout=30
            )
            
            print("📨 RESPONSE RECEIVED")
            print("=" * 60)
            print(f"📊 Status Code: {resp.status_code}")
            print(f"📋 Response Headers: {dict(resp.headers)}")
            print(f"📄 Response Text: {resp.text}")
            print("=" * 60)
            
            if resp.status_code == 200:
                try:
                    json_response = resp.json()
                    print(f"✅ JSON response: {json_response}")
                    
                    # Transform Cloud Run response to expected APIResponse format
                    return APIResponse(
                        ResultCode=200,
                        ErrorDescription="",
                        ResultStatus="SUCCESS CREATE",
                        data=json_response.get('ticket_id', 'UNKNOWN')
                    )
                except Exception as json_e:
                    print(f"❌ JSON parsing failed: {json_e}")
                    return APIResponse(
                        ResultCode=500, 
                        ErrorDescription=f"Invalid JSON response: {json_e}", 
                        ResultStatus="ERROR", 
                        data=""
                    )
            else:
                # Handle error responses
                try:
                    error_response = resp.json()
                    error_msg = error_response.get('detail', f'HTTP {resp.status_code}')
                except:
                    error_msg = f'HTTP {resp.status_code}: {resp.text}'
                
                return APIResponse(
                    ResultCode=resp.status_code,
                    ErrorDescription=error_msg,
                    ResultStatus="ERROR",
                    data=""
                )
            
        except Exception as e:
            print("=" * 60)
            print("❌ REQUEST FAILED")
            print("=" * 60)
            print(f"🚨 Exception Type: {type(e).__name__}")
            print(f"🚨 Exception Message: {str(e)}")
            print("=" * 60)
            import traceback
            traceback.print_exc()
            return APIResponse(ResultCode=500, ErrorDescription=str(e), ResultStatus="ERROR", data="")
    
    def _prepare_json_payload(self, user_data, category, street, custom_text=None):
        """
        Prepare JSON payload for Cloud Run incident service.
        Uses custom_text if provided, otherwise falls back to category.event_call_desc.
        """
        return {
            "user_data": {
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "phone": user_data.phone,
                "user_id": user_data.user_id,
                "email": user_data.email or ""
            },
            "category": {
                "id": category.id,
                "name": category.name,
                "text": category.text,
                "image_url": category.image_url,
                "event_call_desc": category.event_call_desc
            },
            "street": {
                "id": street.id,
                "name": street.name,
                "image_url": street.image_url,
                "house_number": street.house_number
            },
            "custom_text": custom_text or category.event_call_desc
        }

    def _mock_response(self):
        """
        Generate mock response for debug mode.
        """
        return APIResponse(
            ResultCode=200,
            ErrorDescription="Mocked success.",
            ResultStatus="SUCCESS CREATE",
            data="MOCK-0001"
        ) 
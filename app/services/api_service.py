import requests
import brotli
import json
from app.utils.models import APIResponse, APIPayload

class APIService:
    def __init__(self, endpoint, debug_mode=True):
        self.endpoint = endpoint
        self.debug_mode = debug_mode
        self.headers = self._get_headers()
        
    def submit_data(self, user_data, category, street, custom_text=None, extra_files=None):
        """
        Submit data to municipality API or mock service. Returns APIResponse.
        Optionally accepts custom_text to override category.event_call_desc.
        Optionally accepts extra_files (dict) for file upload (future-proof).
        """
        payload = self._prepare_payload(user_data, category, street, custom_text)
        # if self.debug_mode:
        #     return self._mock_response()
        # Real request
        files = {
            'json': (None, json.dumps(payload.__dict__), 'application/json')
        }
        if extra_files:
            files.update(extra_files)
        try:
            print(f"DEBUG: Posting to {self.endpoint}")
            print(f"DEBUG: Headers: {self.headers}")
            print(f"DEBUG: Files payload: {files}")
            
            resp = requests.post(self.endpoint, files=files, headers=self.headers, timeout=30)
            
            # 1. Try automatic requests decompression
            try:
                auto_text = resp.text
                print(f"✅ Automatic requests decompression: {len(auto_text)} chars")
                print(f"✅ response: {auto_text}")
                if auto_text.strip().startswith('{'):
                    print("✅ Looks like JSON!")
                    try:
                        json_data = json.loads(auto_text)
                        print(f"✅ JSON parsed successfully: {json_data}")
                        # Use this successful result
                        return APIResponse(
                            ResultCode=json_data.get('ResultCode'),
                            ErrorDescription=json_data.get('ErrorDescription'),
                            ResultStatus=json_data.get('ResultStatus'),
                            data=json_data.get('data')
                        )
                    except Exception as json_e:
                        print(f"❌ JSON parsing failed: {json_e}")
            except Exception as e:
                print(f"❌ Automatic decompression failed: {e}")
            
        except Exception as e:
            print(f"DEBUG: Exception in submit_data: {e}")
            import traceback
            traceback.print_exc()
            return APIResponse(ResultCode=500, ErrorDescription=str(e), ResultStatus="ERROR", data="")
    
    def _prepare_payload(self, user_data, category, street, custom_text=None):
        """
        Prepare API payload from user selections.
        Uses custom_text if provided, otherwise falls back to category.event_call_desc.
        """
        return APIPayload(
            eventCallDesc=custom_text,
            houseNumber=street.house_number,
            callerFirstName=user_data.first_name,
            callerLastName=user_data.last_name,
            callerTZ=user_data.user_id,
            callerPhone1=user_data.phone,
            callerEmail=user_data.email or ""
        )

    def _get_headers(self):
        """
        Get required HTTP headers.
        Note: Content-Type is automatically set by requests when using files parameter.
        """
        return {
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': 'application/json;odata=verbose',
            'Origin': 'https://www.netanya.muni.il',
            'Referer': 'https://www.netanya.muni.il/CityHall/ServicesInnovation/Pages/PublicComplaints.aspx',
            'Accept-Encoding': 'gzip, deflate, br',
            'Priority': 'u=1, i'
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
import requests
import brotli
from app.utils.models import APIResponse, APIPayload

class APIService:
    def __init__(self, endpoint, debug_mode=False):
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
        if self.debug_mode:
            return self._mock_response()
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
            print(f"DEBUG: Response status: {resp.status_code}")
            print(f"DEBUG: Response headers: {dict(resp.headers)}")
            print(f"DEBUG: Response encoding: {resp.encoding}")
            print(f"DEBUG: Response apparent encoding: {resp.apparent_encoding}")
            print(f"DEBUG: Content-Encoding header: {resp.headers.get('Content-Encoding', 'None')}")
            print(f"DEBUG: Response content length: {len(resp.content)} bytes")
            print(f"DEBUG: Response text length: {len(resp.text)} chars")
            print(f"DEBUG: First 200 chars of resp.text: {repr(resp.text[:200])}")
            
            # Check if response has any content
            if not resp.content:
                print("DEBUG: Empty response content (bytes)")
                return APIResponse(
                    ResultCode=200,
                    ErrorDescription="Empty response from server",
                    ResultStatus="SUCCESS",
                    ResultData={},
                    data=""
                )
            
            if not resp.text.strip():
                print("DEBUG: Empty response text after decoding")
                print(f"DEBUG: Raw content (first 100 bytes): {resp.content[:100]}")
                return APIResponse(
                    ResultCode=200,
                    ErrorDescription="Empty response text after decoding",
                    ResultStatus="SUCCESS",
                    ResultData={},
                    data=""
                )
            
                # decompressed = brotli.decompress(resp.content)
                # print(decompressed.decode('utf-8'))  # or 'latin-1', if needed


            try:
                data = resp.json()
                print(f"DEBUG: Successfully parsed JSON: {data}")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"DEBUG: JSON parsing error: {e}")
                print(f"DEBUG: Attempting manual content inspection...")
                
                # Return a response indicating the issue
                return APIResponse(
                    ResultCode=resp.status_code,
                    ErrorDescription=f"JSON parsing failed: {str(e)}. Response: {resp.text[:100]}",
                    ResultStatus="PARSE_ERROR",
                    ResultData={},
                    data=resp.text[:100]
                )
            
            return APIResponse(
                ResultCode=data.get('ResultCode'),
                ErrorDescription=data.get('ErrorDescription'),
                ResultStatus=data.get('ResultStatus'),
                ResultData=data.get('ResultData'),
                data=data.get('data')
            )
        except Exception as e:
            print(f"DEBUG: Exception in submit_data: {e}")
            import traceback
            traceback.print_exc()
            return APIResponse(ResultCode=500, ErrorDescription=str(e), ResultStatus="ERROR", ResultData={}, data="")
    
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
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json;odata=verbose',
            'Origin': 'https://www.netanya.muni.il',
            'Referer': 'https://www.netanya.muni.il/CityHall/ServicesInnovation/Pages/PublicComplaints.aspx',
            'Accept-Encoding': 'gzip, deflate, br'
        }
    
    def _get_headers_no_compression(self):
        """
        Get headers without compression - for testing compression issues.
        """
        return {
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json;odata=verbose',
            'Origin': 'https://www.netanya.muni.il',
            'Referer': 'https://www.netanya.muni.il/CityHall/ServicesInnovation/Pages/PublicComplaints.aspx'
            # No Accept-Encoding header to disable compression
        }

    def submit_data_no_compression(self, user_data, category, street, custom_text=None, extra_files=None):
        """
        Alternative submit method without compression for testing.
        """
        payload = self._prepare_payload(user_data, category, street, custom_text)
        if self.debug_mode:
            return self._mock_response()
            
        files = {
            'json': (None, json.dumps(payload.__dict__), 'application/json')
        }
        if extra_files:
            files.update(extra_files)
            
        try:
            headers_no_comp = self._get_headers_no_compression()
            print(f"DEBUG: Posting WITHOUT compression to {self.endpoint}")
            print(f"DEBUG: Headers (no compression): {headers_no_comp}")
            
            resp = requests.post(self.endpoint, files=files, headers=headers_no_comp, timeout=30)
            print(f"DEBUG: Response status: {resp.status_code}")
            print(f"DEBUG: Response headers: {dict(resp.headers)}")
            print(f"DEBUG: Content-Encoding header: {resp.headers.get('Content-Encoding', 'None')}")
            print(f"DEBUG: Response content: {resp.text}")
            
            if not resp.text.strip():
                print("DEBUG: Empty response text")
                return APIResponse(
                    ResultCode=200,
                    ErrorDescription="Empty response from server",
                    ResultStatus="SUCCESS",
                    ResultData={},
                    data=""
                )
            
            data = resp.json()
            print(f"DEBUG: Successfully parsed JSON: {data}")
            
            return APIResponse(
                ResultCode=data.get('ResultCode'),
                ErrorDescription=data.get('ErrorDescription'),
                ResultStatus=data.get('ResultStatus'),
                ResultData=data.get('ResultData'),
                data=data.get('data')
            )
        except Exception as e:
            print(f"DEBUG: Exception in submit_data_no_compression: {e}")
            import traceback
            traceback.print_exc()
            return APIResponse(ResultCode=500, ErrorDescription=str(e), ResultStatus="ERROR", ResultData={}, data="")

    def _mock_response(self):
        """
        Generate mock response for debug mode.
        """
        return APIResponse(
            ResultCode=200,
            ErrorDescription="Mocked success.",
            ResultStatus="SUCCESS CREATE",
            ResultData={"incidentGuid": "mock-guid-1234", "incidentNumber": "MOCK-0001"},
            data="MOCK-0001"
        ) 
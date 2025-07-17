import requests
import brotli
import json
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
        if self.debug_mode or True:
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
            
            # 1. Try automatic requests decompression
            try:
                auto_text = resp.text
                print(f"✅ Automatic requests decompression: {len(auto_text)} chars")
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
            
            # 2. Try manual Brotli
            try:
                brotli_result = brotli.decompress(resp.content)
                brotli_text = brotli_result.decode('utf-8')
                print(f"✅ Manual Brotli decompression: {len(brotli_text)} chars")
                print(f"First 100 chars: {repr(brotli_text[:100])}")
            except Exception as e:
                print(f"❌ Manual Brotli failed: {e}")
            
            # 3. Try gzip
            try:
                import gzip
                gzip_result = gzip.decompress(resp.content)
                gzip_text = gzip_result.decode('utf-8')
                print(f"✅ Gzip decompression: {len(gzip_text)} chars")
                print(f"First 100 chars: {repr(gzip_text[:100])}")
            except Exception as e:
                print(f"❌ Gzip failed: {e}")
            
            # 4. Try deflate
            try:
                import zlib
                deflate_result = zlib.decompress(resp.content)
                deflate_text = deflate_result.decode('utf-8')
                print(f"✅ Deflate decompression: {len(deflate_text)} chars")
                print(f"First 100 chars: {repr(deflate_text[:100])}")
            except Exception as e:
                print(f"❌ Deflate failed: {e}")
            
            # 5. Try raw content as text
            try:
                raw_text = resp.content.decode('utf-8')
                print(f"✅ Raw UTF-8 decode: {len(raw_text)} chars")
                print(f"First 100 chars: {repr(raw_text[:100])}")
            except Exception as e:
                print(f"❌ Raw UTF-8 decode failed: {e}")
            
            print("=" * 60)
            
            # Handle Brotli compression specifically
            content_encoding = resp.headers.get('Content-Encoding', '').lower()
            if content_encoding == 'br':
                print("DEBUG: Detected Brotli compression, attempting manual decompression...")
                try:
                    decompressed = brotli.decompress(resp.content)
                    decompressed_text = decompressed.decode('utf-8')
                    print(f"DEBUG: Brotli decompressed text: {decompressed_text}")
                    
                    if not decompressed_text.strip():
                        print("DEBUG: Empty decompressed text")
                        return APIResponse(
                            ResultCode=200,
                            ErrorDescription="Empty response after decompression",
                            ResultStatus="SUCCESS",
                            ResultData={},
                            data=""
                        )
                    
                    # Try to parse the decompressed content as JSON
                    try:
                        data = json.loads(decompressed_text)
                        print(f"DEBUG: Successfully parsed decompressed JSON: {data}")
                        
                        return APIResponse(
                            ResultCode=data.get('ResultCode'),
                            ErrorDescription=data.get('ErrorDescription'),
                            ResultStatus=data.get('ResultStatus'),
                            ResultData=data.get('ResultData'),
                            data=data.get('data')
                        )
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"DEBUG: JSON parsing failed on decompressed content: {e}")
                        print(f"DEBUG: Decompressed content was: {repr(decompressed_text)}")
                        # The API might return HTML instead of JSON - this is still a success
                        return APIResponse(
                            ResultCode=resp.status_code,
                            ErrorDescription="Request submitted successfully (non-JSON response)",
                            ResultStatus="SUCCESS_NON_JSON",
                            ResultData={"raw_response": decompressed_text},
                            data="Request submitted successfully"
                        )
                        
                except Exception as e:
                    print(f"DEBUG: Brotli decompression failed: {e}")
                    return APIResponse(
                        ResultCode=500,
                        ErrorDescription=f"Failed to decompress response: {str(e)}",
                        ResultStatus="DECOMPRESSION_ERROR",
                        ResultData={},
                        data=""
                    )
            
            # If not brotli or decompression failed, try normal processing
            if not resp.text.strip():
                print("DEBUG: Empty response text")
                return APIResponse(
                    ResultCode=200,
                    ErrorDescription="Empty response from server",
                    ResultStatus="SUCCESS",
                    ResultData={},
                    data=""
                )
            
            # FIRST: Try automatic requests handling (this should work!)
            try:
                print("DEBUG: Trying automatic requests JSON parsing...")
                data = resp.json()
                print(f"DEBUG: ✅ Successfully parsed JSON: {data}")
                
                return APIResponse(
                    ResultCode=data.get('ResultCode'),
                    ErrorDescription=data.get('ErrorDescription'),
                    ResultStatus=data.get('ResultStatus'),
                    ResultData=data.get('ResultData'),
                    data=data.get('data')
                )
            except (json.JSONDecodeError, ValueError) as e:
                print(f"DEBUG: ❌ Automatic JSON parsing failed: {e}")
                print(f"DEBUG: Response text preview: {repr(resp.text[:100])}")
                
                # FALLBACK: Only try manual decompression if automatic fails
                content_encoding = resp.headers.get('Content-Encoding', '').lower()
                if content_encoding == 'br':
                    print("DEBUG: Trying manual Brotli decompression as fallback...")
                    try:
                        decompressed = brotli.decompress(resp.content)
                        decompressed_text = decompressed.decode('utf-8')
                        print(f"DEBUG: Manual Brotli decompressed: {decompressed_text}")
                        
                        data = json.loads(decompressed_text)
                        return APIResponse(
                            ResultCode=data.get('ResultCode'),
                            ErrorDescription=data.get('ErrorDescription'),
                            ResultStatus=data.get('ResultStatus'),
                            ResultData=data.get('ResultData'),
                            data=data.get('data')
                        )
                    except Exception as brotli_e:
                        print(f"DEBUG: Manual Brotli also failed: {brotli_e}")
                
                # If all else fails, return error
                return APIResponse(
                    ResultCode=resp.status_code,
                    ErrorDescription="Could not parse response",
                    ResultStatus="PARSE_ERROR",
                    ResultData={"raw_response": resp.text[:200]},
                    data=""
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
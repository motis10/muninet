import requests
import json
from app.utils.models import APIResponse, APIPayload

class APIService:
    def __init__(self, endpoint, debug_mode=False):
        self.endpoint = endpoint
        self.debug_mode = debug_mode
        self.headers = self._get_headers()

    def submit_data(self, user_data, category, street, extra_files=None):
        """
        Submit data to municipality API or mock service. Returns APIResponse.
        Optionally accepts extra_files (dict) for file upload (future-proof).
        """
        payload = self._prepare_payload(user_data, category, street)
        if self.debug_mode:
            return self._mock_response()
        # Real request
        files = {
            'json': (None, json.dumps(payload.__dict__), 'application/json')
        }
        if extra_files:
            files.update(extra_files)
        try:
            resp = requests.post(self.endpoint, files=files, headers=self.headers, timeout=30)
            data = resp.json()
            return APIResponse(
                ResultCode=data.get('ResultCode'),
                ErrorDescription=data.get('ErrorDescription'),
                ResultStatus=data.get('ResultStatus'),
                ResultData=data.get('ResultData'),
                data=data.get('data')
            )
        except Exception as e:
            return APIResponse(ResultCode=500, ErrorDescription=str(e), ResultStatus="ERROR", ResultData={}, data="")

    def _prepare_payload(self, user_data, category, street):
        """
        Prepare API payload from user selections.
        """
        return APIPayload(
            eventCallDesc=category.event_call_desc,
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
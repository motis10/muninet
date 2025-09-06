# Netanya Multilingual Streamlit App

## Running the App

To avoid ModuleNotFoundError for 'app', always run Streamlit with the project root as PYTHONPATH:

```bash
PYTHONPATH=. streamlit run app/main.py --server.runOnSave true
```

This ensures that all `from app...` imports work correctly.

## Supabase SSL Certificate

If you need to use a custom SSL certificate for Supabase:
- Place your certificate file (e.g., prod-ca-2021.crt) in a `certs/` directory at the project root.
- Add this to your `.env.debug` or `.env.release`:
  ```
  SUPABASE_SSL_CERT=certs/prod-ca-2021.crt
  ```
- The app will use this certificate for secure Supabase connections if specified.

## Development
- See INSTRUCTIONS.md for full workflow and testing details. 
 
## Mock SharePoint Incident Server

Run a local mock of the SharePoint endpoint `/_layouts/15/NetanyaMuni/incidents.ashx?method=CreateNewIncident`.

1) Install dependencies:
```bash
pip install -r requirements.txt
```

2) Start the server (runs on port 8080):
```bash
python mock_sharepoint_server.py
```

3) Test with curl (multipart form with a `json` field):
```bash
curl -i -X POST "http://localhost:8080/_layouts/15/NetanyaMuni/incidents.ashx?method=CreateNewIncident" \
  -H "Accept: application/json;odata=verbose" \
  -H "Content-Type: multipart/form-data" \
  -F 'json={
  "eventCallSourceId": 4,
  "cityCode": "",
  "cityDesc": "",
  "eventCallCenterId": "",
  "eventCallDesc": "",
  "streetCode": "",
  "streetDesc": " ",
  "houseNumber": "",
  "callerFirstName": "",
  "callerLastName": "",
  "callerTZ": "",
  "callerPhone1": "",
  "callerEmail": "",
  "contactUsType": ""
}'
```

The server returns the exact JSON and response headers provided for testing purposes.
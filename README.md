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
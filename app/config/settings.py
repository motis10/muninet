import os
from dataclasses import dataclass

def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")

@dataclass
class AppConfig:
    supabase_url: str
    supabase_key: str
    api_endpoint: str
    api_timeout: int = 30
    debug_mode: bool = False
    app_mode: str = "release"
    enable_file_upload: bool = False
    enable_ticket_history: bool = True

def load_config() -> AppConfig:
    return AppConfig(
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_key=os.getenv("SUPABASE_KEY", ""),
        api_endpoint=os.getenv("API_ENDPOINT", ""),
        api_timeout=int(os.getenv("API_TIMEOUT", "30")),
        debug_mode=str2bool(os.getenv("DEBUG", "False")),
        app_mode=os.getenv("APP_MODE", ""),
        enable_file_upload=str2bool(os.getenv("ENABLE_FILE_UPLOAD", "False")),
        enable_ticket_history=str2bool(os.getenv("ENABLE_TICKET_HISTORY", "True")),
    ) 
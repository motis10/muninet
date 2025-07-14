from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

class Language(Enum):
    ENGLISH = "en"
    HEBREW = "he"
    FRENCH = "fr"
    RUSSIAN = "ru"

class Page(Enum):
    CATEGORIES = "categories"
    STREET_NUMBERS = "street_numbers"
    SUMMARY = "summary"

@dataclass
class Category:
    id: int
    name: str
    text: str  # Comma-separated array
    image_url: str
    event_call_desc: str

@dataclass
class StreetNumber:
    id: int
    name: str
    image_url: str
    house_number: str

@dataclass
class UserData:
    first_name: str
    last_name: str
    user_id: str
    phone: str
    email: Optional[str] = None

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]

@dataclass
class APIPayload:
    eventCallSourceId: int = 4
    cityCode: str = "7400"
    cityDesc: str = "נתניה"
    eventCallCenterId: str = "3"
    eventCallDesc: str = ""
    streetCode: str = "898"
    streetDesc: str = "קרל פופר"
    houseNumber: str = ""
    callerFirstName: str = ""
    callerLastName: str = ""
    callerTZ: str = ""
    callerPhone1: str = ""
    callerEmail: str = ""
    contactUsType: str = "3"

@dataclass
class APIResponse:
    ResultCode: int
    ErrorDescription: str
    ResultStatus: str
    ResultData: Dict[str, Any]
    data: str

@dataclass
class AppState:
    current_page: Page
    selected_category: Optional[Category] = None
    selected_street: Optional[StreetNumber] = None
    show_popup: bool = False
    search_query: str = ""
    ticket_history: List[str] = field(default_factory=list) 

# --- Error Classes ---
class AppError(Exception):
    """Base application error."""
    pass

class ValidationError(AppError):
    """Validation error."""
    pass

class APIError(AppError):
    """API communication error."""
    pass

class DatabaseError(AppError):
    """Database operation error."""
    pass 
# Application Design Specification

## 🎯 Design Overview
This document bridges the gap between Architecture.md and actual implementation, providing detailed technical specifications for building the multilingual Streamlit application for Netanya Municipality with advanced URL parameter handling and enhanced user experience.

## 📁 Component Hierarchy

### Application Structure
```
app/
├── main.py                    # Application entry point with URL parameter handling
├── components/                # UI Components
│   ├── __init__.py
│   ├── header.py             # Header with language selector, banner, search
│   ├── grid_view.py          # Responsive grid for categories/street numbers
│   ├── popups.py             # Data collection, success, error popups with random data
│   └── search.py             # Search functionality with auto-clearing
├── services/                 # Business Logic Services
│   ├── __init__.py
│   ├── supabase_service.py   # Database operations
│   ├── api_service.py        # HTTP API integration with debug/release modes
│   └── storage_service.py    # Local storage management with user data persistence
├── utils/                    # Utility Functions
│   ├── __init__.py
│   ├── models.py             # Data models and types
│   ├── validation.py         # Israeli phone number validation
│   ├── i18n.py              # Internationalization with Hebrew as default
│   └── helpers.py           # Helper functions including URL parameter handling
└── config/                  # Configuration
    ├── __init__.py
    ├── settings.py          # Environment and app settings
    └── constants.py         # Application constants
```

## 🔗 URL Parameter System

### URL Structure
```
https://app-url?category={id}&street={id}
```

### Parameter Handling Flow
```python
def handle_url_parameters():
    """Handle URL parameters for direct navigation."""
    query_params = st.query_params
    category_id = query_params.get("category")
    street_id = query_params.get("street")
    
    if category_id and street_id:
        # Load user data
        user_data = storage_service.load_user_data()
        
        if user_data:
            # Direct navigation to summary page
            category = supabase_service.get_category_by_id(int(category_id))
            street = supabase_service.get_street_by_id(int(street_id))
            
            if category and street:
                st.session_state.selected_category = category
                st.session_state.selected_street = street
                st.session_state.current_page = "summary"
                
                # Clear URL parameters after processing
                clear_url_parameters()
        else:
            # User data required - show popup first
            st.session_state.show_popup = True
    
    elif category_id:
        # Navigate to streets page
        category = supabase_service.get_category_by_id(int(category_id))
        if category:
            st.session_state.selected_category = category
            st.session_state.current_page = "street_numbers"
            clear_url_parameters()

def clear_url_parameters():
    """Clear URL parameters after processing."""
    st.query_params.clear()
```

## 🏗️ Data Models

### Enhanced Data Structures
```python
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class Language(Enum):
    HEBREW = "he"      # Default language
    ENGLISH = "en"
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
    ticket_history: List[str] = []
    url_params_processed: bool = False
```

## 🔧 Enhanced Service Layer Design

### Supabase Service with ID Lookups
```python
class SupabaseService:
    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)
    
    def get_categories(self) -> List[Category]:
        """Fetch all categories from database."""
        
    def get_street_numbers(self) -> List[StreetNumber]:
        """Fetch all street numbers from database."""
        
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get specific category by ID for URL parameter handling."""
        
    def get_street_by_id(self, street_id: int) -> Optional[StreetNumber]:
        """Get specific street by ID for URL parameter handling."""
        
    def search_categories(self, query: str) -> List[Category]:
        """Search categories by name."""
        
    def search_street_numbers(self, query: str) -> List[StreetNumber]:
        """Search street numbers by name."""
```

### Enhanced API Service with Improved Error Handling
```python
class APIService:
    def __init__(self, endpoint: str, debug_mode: bool = False):
        self.endpoint = endpoint
        self.debug_mode = debug_mode
        self.headers = self._get_headers()
    
    def submit_data(self, user_data: UserData, category: Category, street: StreetNumber) -> APIResponse:
        """Submit data to municipality API or mock service."""
        payload = self._prepare_payload(user_data, category, street)
        
        if self.debug_mode:
            return self._mock_response()
        
        try:
            response = self._send_request(payload)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"API submission failed: {e}")
            raise APIError(f"Failed to submit data: {e}")
    
    def _prepare_payload(self, user_data: UserData, category: Category, street: StreetNumber) -> APIPayload:
        """Prepare API payload from user selections."""
        
    def _send_request(self, payload: APIPayload) -> requests.Response:
        """Send multipart/form-data request."""
        
    def _parse_response(self, response: requests.Response) -> APIResponse:
        """Parse API response."""
        
    def _mock_response(self) -> APIResponse:
        """Generate mock response for debug mode."""
        import random
        mock_ticket = f"MOCK-{random.randint(1000, 9999)}"
        return APIResponse(
            ResultCode=200,
            ErrorDescription="",
            ResultStatus="SUCCESS CREATE",
            ResultData={"incidentNumber": mock_ticket},
            data=mock_ticket
        )
```

### Enhanced Storage Service
```python
class StorageService:
    LANGUAGE_KEY = "selected_language"
    USER_DATA_KEY = "user_data"
    TICKET_KEY = "ticket_history"
    
    def save_user_data(self, user_data: UserData) -> None:
        """Save user data to localStorage."""
        
    def load_user_data(self) -> Optional[UserData]:
        """Load user data from localStorage."""
        
    def save_language(self, language: Language) -> None:
        """Save language preference (defaults to Hebrew)."""
        
    def load_language(self) -> Language:
        """Load language preference (defaults to Hebrew)."""
        try:
            lang_code = self.local_storage.getItem(self.LANGUAGE_KEY) or "he"
            return Language(lang_code)
        except:
            return Language.HEBREW  # Default to Hebrew
        
    def save_ticket(self, ticket_number: str) -> None:
        """Save ticket number to history."""
        
    def get_ticket_history(self) -> List[str]:
        """Get ticket history."""
        
    def clear_user_data(self) -> None:
        """Clear user data only (preserve language and tickets)."""
        
    def generate_random_user_data(self) -> UserData:
        """Generate random Hebrew user data for development."""
        # Implementation with Hebrew names and transliteration
```

## 🧪 Enhanced State Management

### Enhanced Session State Structure
```python
SESSION_KEYS = {
    'current_page': 'categories',
    'selected_category': None,
    'selected_street': None,
    'show_popup': False,
    'search_query': '',
    'ticket_history': [],
    'user_data': None,
    'current_language': 'he',  # Default to Hebrew
    'url_params_processed': False,
    'show_success_toast': False,
    'last_ticket_number': None
}
```

### Enhanced State Transitions
```python
def navigate_to_page(page: Page, clear_search: bool = True):
    """Navigate to specified page with optional search clearing."""
    st.session_state.current_page = page.value
    if clear_search:
        st.session_state.search_query = ""  # Clear search on navigation
    st.rerun()

def select_category(category: Category):
    """Handle category selection with URL parameter support."""
    st.session_state.selected_category = category
    st.session_state.search_query = ""  # Clear search
    
    user_data = storage_service.load_user_data()
    if user_data is None:
        st.session_state.show_popup = True
    else:
        navigate_to_page(Page.STREET_NUMBERS)

def select_street(street: StreetNumber):
    """Handle street selection."""
    st.session_state.selected_street = street
    st.session_state.search_query = ""  # Clear search
    navigate_to_page(Page.SUMMARY)

def show_success_notification(ticket_number: str):
    """Show success toast notification."""
    st.session_state.show_success_toast = True
    st.session_state.last_ticket_number = ticket_number
    storage_service.save_ticket(ticket_number)
```

## 🎨 Enhanced UI/UX Component Design

### Header Component with Auto-clearing Search
```python
def render_header():
    """Render header with banner, language selector, and auto-clearing search."""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.image("assets/images/banner.png", use_column_width=True)
    
    with col2:
        render_language_selector()
    
    with col3:
        render_search_box_with_clearing()
    
    apply_rtl_styling()

def render_search_box_with_clearing():
    """Render search box that clears automatically on navigation."""
    search_query = st.text_input(
        t("common.search"),
        value=st.session_state.get("search_query", ""),
        key="search_input",
        placeholder=t("common.search_placeholder")
    )
    
    # Update session state if search changed
    if search_query != st.session_state.get("search_query", ""):
        st.session_state.search_query = search_query
        st.rerun()
```

### Enhanced Grid View Component
```python
def create_grid_view(
    items: List[Union[Category, StreetNumber]],
    on_item_click: Callable,
    search_query: str = ""
) -> None:
    """Create responsive grid view with enhanced interactions."""
    filtered_items = filter_items(items, search_query)
    
    if not filtered_items:
        st.info(t("common.no_results"))
        return
    
    cols_per_row = calculate_responsive_columns()
    cols = st.columns(cols_per_row)
    
    for idx, item in enumerate(filtered_items):
        with cols[idx % cols_per_row]:
            render_enhanced_grid_item(item, on_item_click)

def render_enhanced_grid_item(item: Union[Category, StreetNumber], on_click: Callable):
    """Render grid item with enhanced visual feedback."""
    # Custom styling for better interaction
    st.markdown("""
    <style>
    .grid-item-button {
        width: 100%;
        height: auto;
        min-height: 120px;
        margin: 5px 0;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    .grid-item-button:hover {
        border-color: #1f77b4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(
        f"🖼️ {item.name}",
        key=f"item_{item.id}",
        use_container_width=True,
        help=getattr(item, 'text', '')
    ):
        on_click(item)
```

### Enhanced Popup Components with Random Data
```python
def show_data_collection_popup(on_save: Callable, on_cancel: Callable, lang="he"):
    """Show user data collection popup with pre-filled random Hebrew data."""
    st.markdown(f"### {t('common.save', lang)}")
    st.markdown(f"<span style='color: red;'>* {t('common.one_time', lang)}</span>", 
                unsafe_allow_html=True)

    # Generate random Hebrew user data for development
    user = generate_random_user_data()
    
    with st.form("user_data_form", clear_on_submit=False):
        first_name = st.text_input(
            t("forms.first_name", lang), 
            key="popup_first_name", 
            value=user.first_name,
            max_chars=35,
            autocomplete="given-name"
        )
        last_name = st.text_input(
            t("forms.last_name", lang), 
            key="popup_last_name", 
            value=user.last_name,
            max_chars=35,
            autocomplete="family-name"
        )
        phone = st.text_input(
            t("forms.phone", lang), 
            key="popup_phone", 
            value="",
            max_chars=15,
            autocomplete="tel",
            help=t("forms.phone_help", lang)
        )
        email = st.text_input(
            t("forms.email", lang), 
            key="popup_email", 
            value=user.email,
            autocomplete="email"
        )
        user_id = st.text_input(
            t("forms.id_optional", lang), 
            key="popup_id",
            max_chars=12,
            autocomplete="off"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button(t("common.save", lang), use_container_width=True):
                if handle_save_data(first_name, last_name, user_id, phone, email, on_save, lang):
                    return
        with col2:
            if st.form_submit_button(t("common.cancel", lang), use_container_width=True):
                on_cancel()

def show_success_toast(ticket_number: str, lang="he"):
    """Show success toast notification."""
    success_message = t("messages.success_message", lang).format(ticket_number=ticket_number)
    st.success(success_message)
    
    # Auto-clear toast after display
    if st.session_state.get("show_success_toast"):
        st.session_state.show_success_toast = False

def show_error_popup(on_restart: Callable, lang="he"):
    """Show error popup with restart option."""
    st.error(t("messages.error_message", lang))
    if st.button(t("common.try_again", lang), use_container_width=True):
        on_restart()
```

## 📱 Enhanced Mobile Responsive Design

### Enhanced Responsive Breakpoints
```python
BREAKPOINTS = {
    'mobile': 768,    # 1-2 items per row, larger touch targets
    'tablet': 1024,   # 2-3 items per row
    'desktop': 1200   # 3-4 items per row
}

def apply_mobile_optimizations():
    """Apply comprehensive mobile optimizations."""
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stButton > button {
            width: 100%;
            height: 60px;
            font-size: 18px;
            margin: 10px 0;
            border-radius: 10px;
            touch-action: manipulation;
        }
        
        .grid-item {
            margin: 15px 0;
            padding: 20px;
            min-height: 100px;
        }
        
        .search-input {
            font-size: 16px;
            padding: 15px;
            border-radius: 8px;
        }
        
        .popup-form {
            padding: 20px;
            font-size: 16px;
        }
        
        .toast-notification {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            padding: 15px;
            border-radius: 8px;
            background: #4CAF50;
            color: white;
            font-weight: bold;
        }
    }
    </style>
    """, unsafe_allow_html=True)
```

## 🌍 Enhanced Internationalization Design

### Updated Translation File Structure with Hebrew Default
```
assets/translations/
├── he.json (default)
├── en.json
├── fr.json
└── ru.json
```

### Enhanced Translation File Format
```json
{
  "common": {
    "welcome": "ברוכים הבאים",
    "search": "חיפוש",
    "search_placeholder": "חפש כאן...",
    "save": "שמור",
    "cancel": "בטל",
    "start_over": "התחל מחדש",
    "try_again": "נסה שוב",
    "no_results": "לא נמצאו תוצאות",
    "one_time": "הנתונים יישמרו מקומית פעם אחת בלבד"
  },
  "forms": {
    "first_name": "שם פרטי",
    "last_name": "שם משפחה",
    "id_optional": "תעודת זהות (אופציונלי)",
    "phone": "טלפון",
    "phone_help": "מספר טלפון ישראלי בלבד",
    "email": "דוא\"ל (אופציונלי)"
  },
  "messages": {
    "success_message": "הבקשה נשלחה בהצלחה. מספר קריאה: {ticket_number}",
    "error_message": "שליחה נכשלה, אנא נסה שוב",
    "save_locally": "הנתונים יישמרו מקומית בלבד"
  },
  "validation": {
    "name_required": "שם נדרש",
    "name_too_long": "השם חייב להיות עד 35 תווים",
    "id_invalid": "תעודת זהות חייבת להכיל ספרות בלבד",
    "phone_invalid": "מספר טלפון לא תקין",
    "phone_israeli": "אנא הזן מספר טלפון ישראלי תקין",
    "email_invalid": "פורמט דוא\"ל לא תקין"
  },
  "pages": {
    "categories": "קטגוריות",
    "street_numbers": "מספרי בית",
    "summary": "סיכום"
  }
}
```

### Enhanced RTL Support
```python
def apply_rtl_styling(language: Language):
    """Apply comprehensive RTL styling for Hebrew."""
    if language == Language.HEBREW:
        st.markdown("""
        <style>
        .stApp {
            direction: rtl;
            text-align: right;
            font-family: 'Arial', 'Helvetica', sans-serif;
        }
        
        .stTextInput > div > div > input {
            text-align: right;
            direction: rtl;
        }
        
        .stButton > button {
            direction: rtl;
        }
        
        .language-selector {
            flex-direction: row-reverse;
        }
        
        .search-container {
            flex-direction: row-reverse;
        }
        
        .grid-container {
            direction: rtl;
        }
        
        .popup-content {
            direction: rtl;
            text-align: right;
        }
        </style>
        """, unsafe_allow_html=True)
```

## 🔧 Enhanced Validation System

### Israeli Phone Number Validation
```python
def validate_israeli_phone(phone: str) -> ValidationResult:
    """Validate Israeli phone numbers."""
    errors = []
    
    # Remove spaces and dashes
    cleaned_phone = re.sub(r'[\s\-]', '', phone)
    
    # Check if only digits
    if not cleaned_phone.isdigit():
        errors.append("phone_invalid")
        return ValidationResult(False, errors)
    
    # Israeli phone number patterns
    israeli_patterns = [
        r'^0[2-4,8-9]\d{7}$',      # Landline: 02/03/04/08/09 + 7 digits
        r'^05[0-9]\d{7}$',         # Mobile: 05X + 7 digits
        r'^07[2-9]\d{7}$',         # Special services
    ]
    
    is_valid = any(re.match(pattern, cleaned_phone) for pattern in israeli_patterns)
    
    if not is_valid:
        errors.append("phone_israeli")
    
    return ValidationResult(is_valid, errors)

def validate_user_data(user_data: UserData, lang: str = "he") -> ValidationResult:
    """Enhanced validation with Israeli specifics."""
    errors = []
    
    # Name validation
    if not user_data.first_name.strip():
        errors.append("name_required")
    elif len(user_data.first_name) > 35:
        errors.append("name_too_long")
    
    if not user_data.last_name.strip():
        errors.append("name_required")
    elif len(user_data.last_name) > 35:
        errors.append("name_too_long")
    
    # Phone validation (Israeli specific)
    phone_result = validate_israeli_phone(user_data.phone)
    errors.extend(phone_result.errors)
    
    # ID validation (optional)
    if user_data.user_id and not user_data.user_id.isdigit():
        errors.append("id_invalid")
    
    # Email validation (optional)
    if user_data.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', user_data.email):
        errors.append("email_invalid")
    
    return ValidationResult(len(errors) == 0, errors)
```

## 📋 Enhanced Data Flow Design

### Application Initialization with URL Parameters
```
1. Load environment variables and configuration
2. Initialize services (Supabase, API, Storage)
3. Check for URL parameters and process them
4. Load user data from localStorage
5. Set language preference (default: Hebrew)
6. Load categories and streets from database
7. Initialize session state with URL parameter data
8. Clear URL parameters after processing
9. Render appropriate page based on state
```

### Enhanced User Interaction Flow
```
1. URL Parameter Processing:
   - Check for category and street parameters
   - Validate user data exists for direct summary navigation
   - Clear parameters after processing

2. Category Selection:
   - Clear search query automatically
   - Check user data existence
   - Show popup for new users or navigate for existing users

3. Street Selection:
   - Clear search query automatically
   - Navigate to summary page

4. API Submission:
   - Submit via multipart/form-data
   - Handle response with toast notifications
   - Save ticket to history
   - Restart flow to categories

5. Search Functionality:
   - Auto-clear on page navigation
   - Real-time filtering
   - Multilingual support
```

## 🚀 Enhanced Performance Considerations

### Advanced Caching Strategy
- Session state caching for database data
- Translation file caching
- User data persistence optimization
- Debounced search with 300ms delay
- Lazy loading for images
- Connection pooling for API calls

### URL Parameter Optimization
- Single-pass parameter processing
- Efficient state updates
- Minimal re-renders on parameter changes
- Smart parameter clearing

## 📋 Updated Implementation Checklist

### Phase 1: Foundation ✅
- [x] Project structure setup
- [x] Configuration system with debug/release modes
- [x] Enhanced data models
- [x] URL parameter handling utilities

### Phase 2: Core Services ✅
- [x] Supabase service with ID lookups
- [x] API service with mock support
- [x] Storage service with persistence
- [x] Enhanced validation system

### Phase 3: UI Components ✅
- [x] Header component with auto-clearing search
- [x] Enhanced grid view component
- [x] Popup components with random data
- [x] Toast notification system

### Phase 4: Internationalization ✅
- [x] Translation system with Hebrew default
- [x] Comprehensive RTL support
- [x] Language switching and persistence

### Phase 5: Main Application ✅
- [x] Enhanced state management
- [x] URL parameter-aware routing
- [x] Complete user flows
- [x] Advanced error handling

### Phase 6: Mobile Optimization ✅
- [x] Responsive design
- [x] Touch-friendly interactions
- [x] Mobile-specific styling
- [x] Toast notifications

### Phase 7: Advanced Features ✅
- [x] URL parameter system
- [x] Search box auto-clearing
- [x] Israeli phone validation
- [x] Random Hebrew data generation
- [x] Toast success notifications
- [x] Debug/release mode switching

This enhanced design specification provides a complete technical blueprint for the fully-featured multilingual Streamlit application with advanced URL parameter handling, auto-clearing search, Hebrew as default language, and comprehensive mobile optimization. 
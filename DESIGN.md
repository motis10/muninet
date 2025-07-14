# Application Design Specification

## 🎯 Design Overview
This document bridges the gap between Architecture.md and actual implementation, providing detailed technical specifications for building the multilingual Streamlit application.

## 📁 Component Hierarchy

### Application Structure
```
app/
├── main.py                    # Application entry point
├── components/                # UI Components
│   ├── __init__.py
│   ├── header.py             # Header with language selector, banner, search
│   ├── grid_view.py          # Responsive grid for categories/street numbers
│   ├── popups.py             # Data collection, success, error popups
│   └── search.py             # Search functionality
├── services/                 # Business Logic Services
│   ├── __init__.py
│   ├── supabase_service.py   # Database operations
│   ├── api_service.py        # HTTP API integration
│   └── storage_service.py    # Local storage management
├── utils/                    # Utility Functions
│   ├── __init__.py
│   ├── models.py             # Data models and types
│   ├── validation.py         # Input validation
│   ├── i18n.py              # Internationalization
│   └── helpers.py           # Helper functions
└── config/                  # Configuration
    ├── __init__.py
    ├── settings.py          # Environment and app settings
    └── constants.py         # Application constants
```

## 🏗️ Data Models

### Core Data Structures
```python
from dataclasses import dataclass
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
    ticket_history: List[str] = []
```

## 🔧 Service Layer Design

### Supabase Service
```python
class SupabaseService:
    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)
    
    def get_categories(self) -> List[Category]:
        """Fetch all categories from database."""
        
    def get_street_numbers(self) -> List[StreetNumber]:
        """Fetch all street numbers from database."""
        
    def search_categories(self, query: str) -> List[Category]:
        """Search categories by name."""
        
    def search_street_numbers(self, query: str) -> List[StreetNumber]:
        """Search street numbers by name."""
```

### API Service
```python
class APIService:
    def __init__(self, endpoint: str, debug_mode: bool = False):
        self.endpoint = endpoint
        self.debug_mode = debug_mode
        self.headers = self._get_headers()
    
    def submit_data(self, user_data: UserData, category: Category, street: StreetNumber) -> APIResponse:
        """Submit data to municipality API or mock service."""
        
    def _prepare_payload(self, user_data: UserData, category: Category, street: StreetNumber) -> APIPayload:
        """Prepare API payload from user selections."""
        
    def _get_headers(self) -> Dict[str, str]:
        """Get required HTTP headers."""
        
    def _mock_response(self) -> APIResponse:
        """Generate mock response for debug mode."""
```

### Storage Service
```python
class StorageService:
    def save_user_data(self, user_data: UserData) -> None:
        """Save user data to localStorage."""
        
    def load_user_data(self) -> Optional[UserData]:
        """Load user data from localStorage."""
        
    def save_language(self, language: Language) -> None:
        """Save language preference."""
        
    def load_language(self) -> Language:
        """Load language preference."""
        
    def save_ticket(self, ticket_number: str) -> None:
        """Save ticket number to history."""
        
    def get_ticket_history(self) -> List[str]:
        """Get ticket history."""
        
    def clear_user_data(self) -> None:
        """Clear all user data."""
```

## 🧪 State Management

### Session State Structure
```python
# Streamlit session state keys
SESSION_KEYS = {
    'current_page': 'categories',
    'selected_category': None,
    'selected_street': None,
    'show_popup': False,
    'search_query': '',
    'ticket_history': [],
    'user_data': None,
    'current_language': 'en'
}
```

### State Initialization
```python
def init_session_state():
    """Initialize all session state variables."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'categories'
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    # ... initialize all other keys
```

### State Transitions
```python
def navigate_to_page(page: Page):
    """Navigate to specified page."""
    st.session_state.current_page = page.value
    st.rerun()

def select_category(category: Category):
    """Handle category selection."""
    st.session_state.selected_category = category
    user_data = storage_service.load_user_data()
    
    if user_data is None:
        st.session_state.show_popup = True
    else:
        navigate_to_page(Page.STREET_NUMBERS)
```

## 🎨 UI/UX Component Design

### Header Component
```python
def render_header():
    """Render header with banner, language selector, and search."""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.image("assets/images/banner.png", use_column_width=True)
    
    with col2:
        render_language_selector()
    
    with col3:
        render_search_box()
    
    apply_rtl_styling()
```

### Grid View Component
```python
def create_grid_view(
    items: List[Union[Category, StreetNumber]],
    on_item_click: Callable,
    search_query: str = ""
) -> None:
    """Create responsive grid view."""
    filtered_items = filter_items(items, search_query)
    cols_per_row = calculate_responsive_columns()
    
    cols = st.columns(cols_per_row)
    for idx, item in enumerate(filtered_items):
        with cols[idx % cols_per_row]:
            render_grid_item(item, on_item_click)
```

### Popup Components
```python
def show_data_collection_popup(on_save: Callable, on_cancel: Callable):
    """Show user data collection popup."""
    with st.form("user_data_form"):
        first_name = st.text_input(t("first_name"), max_chars=35, autocomplete="given-name")
        last_name = st.text_input(t("last_name"), max_chars=35, autocomplete="family-name")
        user_id = st.text_input(t("id"), max_chars=12, autocomplete="off")
        phone = st.text_input(t("phone"), max_chars=15, autocomplete="tel")
        email = st.text_input(t("email"), autocomplete="email")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button(t("save")):
                handle_save_data(first_name, last_name, user_id, phone, email, on_save)
        with col2:
            if st.form_submit_button(t("cancel")):
                on_cancel()

def show_success_popup(ticket_number: str, on_restart: Callable):
    """Show success popup with ticket number."""
    st.success(t("success_message", ticket_number=ticket_number))
    if st.button(t("start_over")):
        on_restart()

def show_error_popup(on_restart: Callable):
    """Show error popup."""
    st.error(t("error_message"))
    if st.button(t("try_again")):
        on_restart()
```

## 📱 Mobile Responsive Design

### Responsive Breakpoints
```python
# CSS breakpoints for responsive design
BREAKPOINTS = {
    'mobile': 768,    # 1-2 items per row
    'tablet': 1024,   # 2-3 items per row
    'desktop': 1200   # 3-4 items per row
}

def calculate_responsive_columns() -> int:
    """Calculate number of columns based on screen width."""
    # This will be implemented with CSS media queries
    # and JavaScript detection
    return 3  # Default for desktop
```

### Mobile-Specific Styling
```python
def apply_mobile_styling():
    """Apply mobile-specific CSS."""
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stButton > button {
            width: 100%;
            height: 60px;
            font-size: 18px;
            margin: 10px 0;
        }
        
        .grid-item {
            margin: 10px 0;
            padding: 15px;
        }
        
        .search-input {
            font-size: 16px;
            padding: 12px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
```

### Touch-Friendly Interactions
- Minimum touch target size: 44px × 44px
- Adequate spacing between interactive elements
- Large, readable fonts
- Swipe gestures for navigation (future enhancement)

## 🌍 Internationalization Design

### Translation File Structure
```
assets/translations/
├── en.json
├── he.json
├── fr.json
└── ru.json
```

### Translation File Format
```json
{
  "common": {
    "welcome": "Welcome",
    "search": "Search",
    "save": "Save",
    "cancel": "Cancel",
    "start_over": "Start Over",
    "try_again": "Try Again"
  },
  "forms": {
    "first_name": "First Name",
    "last_name": "Last Name",
    "id": "ID Number",
    "phone": "Phone Number",
    "email": "Email (Optional)"
  },
  "messages": {
    "success_message": "Your request has been submitted successfully. Ticket number: {ticket_number}",
    "error_message": "Failed, please try again",
    "save_locally": "Your data will be saved locally only"
  },
  "validation": {
    "name_required": "Name is required",
    "name_too_long": "Name must be 35 characters or less",
    "id_invalid": "ID must contain only numbers",
    "phone_invalid": "Phone must contain only numbers",
    "email_invalid": "Invalid email format"
  }
}
```

### RTL Support Implementation
```python
def apply_rtl_styling(language: Language):
    """Apply RTL styling for Hebrew."""
    if language == Language.HEBREW:
        st.markdown("""
        <style>
        .stApp {
            direction: rtl;
            text-align: right;
        }
        
        .language-selector {
            flex-direction: row-reverse;
        }
        
        .search-container {
            flex-direction: row-reverse;
        }
        </style>
        """, unsafe_allow_html=True)
```

## 🚨 Error Handling Design

### Error Hierarchy
```python
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
```

### Error Handling Strategy
```python
def handle_api_error(error: Exception) -> None:
    """Handle API errors gracefully."""
    if isinstance(error, requests.exceptions.ConnectionError):
        st.error(t("network_error"))
    elif isinstance(error, requests.exceptions.Timeout):
        st.error(t("timeout_error"))
    else:
        st.error(t("api_error"))
    
    # Log error for debugging
    logger.error(f"API Error: {error}")

def handle_validation_error(errors: List[str]) -> None:
    """Handle validation errors."""
    for error in errors:
        st.error(t(error))

def handle_database_error(error: Exception) -> None:
    """Handle database errors."""
    st.error(t("database_error"))
    logger.error(f"Database Error: {error}")
```

## 🧪 Testing Architecture

### Test Structure
```
tests/
├── unit/
│   ├── test_validation.py
│   ├── test_i18n.py
│   ├── test_models.py
│   └── test_helpers.py
├── integration/
│   ├── test_supabase_service.py
│   ├── test_api_service.py
│   └── test_storage_service.py
├── e2e/
│   ├── test_new_user_flow.py
│   ├── test_existing_user_flow.py
│   └── test_error_scenarios.py
└── conftest.py
```

### Test Examples
```python
# Unit test example
def test_validate_user_data_success():
    user_data = UserData(
        first_name="John",
        last_name="Doe",
        user_id="123456789",
        phone="1234567890",
        email="john@example.com"
    )
    result = validate_user_data(user_data)
    assert result.is_valid == True
    assert len(result.errors) == 0

# Integration test example
def test_api_submission_success(mock_api_service):
    user_data = create_test_user_data()
    category = create_test_category()
    street = create_test_street()
    
    response = mock_api_service.submit_data(user_data, category, street)
    assert response.ResultCode == 200
    assert "SUCCESS" in response.ResultStatus

# E2E test example
def test_new_user_complete_flow():
    # Simulate new user flow from start to finish
    # This would use Streamlit's testing framework
    pass
```

## 📋 Data Flow Design

### Application Initialization Flow
```
1. Load environment variables
2. Initialize services (Supabase, API, Storage)
3. Load user data from localStorage
4. Set language preference
5. Load categories from database
6. Initialize session state
7. Render appropriate page
```

### User Interaction Flow
```
1. User clicks category
2. Check if user data exists
3. If new user: show data collection popup
4. If existing user: navigate to street numbers
5. User selects street number
6. Navigate to summary page
7. User clicks SEND
8. Submit to API (real or mock)
9. Handle response and show appropriate popup
10. Restart flow
```

### Error Recovery Flow
```
1. Detect error (validation, API, network)
2. Log error for debugging
3. Display user-friendly error message
4. Provide recovery options
5. Allow user to retry or restart
```

## 🚀 Performance Considerations

### Caching Strategy
- Cache Supabase data in session state
- Cache translations in memory
- Cache user data in localStorage
- Implement lazy loading for images

### Optimization Techniques
- Debounced search input
- Efficient grid rendering
- Connection pooling for API calls
- Minimal re-renders with state management

## 🔧 Configuration Management

### Environment Configuration
```python
@dataclass
class AppConfig:
    # Supabase configuration
    supabase_url: str
    supabase_key: str
    
    # API configuration
    api_endpoint: str
    api_timeout: int = 30
    
    # Application mode
    debug_mode: bool = False
    app_mode: str = "release"
    
    # Feature flags
    enable_file_upload: bool = False
    enable_ticket_history: bool = True
```

### Configuration Loading
```python
def load_config() -> AppConfig:
    """Load configuration from environment variables."""
    return AppConfig(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
        api_endpoint=os.getenv("API_ENDPOINT"),
        debug_mode=os.getenv("DEBUG", "False").lower() == "true",
        app_mode=os.getenv("APP_MODE", "debug")
    )
```

## 📋 Implementation Checklist

### Phase 1: Foundation
- [ ] Project structure setup
- [ ] Configuration system
- [ ] Data models
- [ ] Basic utilities

### Phase 2: Core Services
- [ ] Supabase service
- [ ] API service (with mock support)
- [ ] Storage service
- [ ] Validation system

### Phase 3: UI Components
- [ ] Header component
- [ ] Grid view component
- [ ] Popup components
- [ ] Search functionality

### Phase 4: Internationalization
- [ ] Translation system
- [ ] RTL support
- [ ] Language switching

### Phase 5: Main Application
- [ ] State management
- [ ] Page routing
- [ ] User flows
- [ ] Error handling

### Phase 6: Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests

### Phase 7: Mobile Optimization
- [ ] Responsive design
- [ ] Touch-friendly interactions
- [ ] Mobile-specific styling

This design specification provides a complete technical blueprint for implementing the multilingual Streamlit application according to the architecture and requirements. 
# Development Instructions

## �� Project Goals
- **Hot Reload**: See changes instantly like Go's air
- **Unit Testing**: Test everything with 90%+ coverage
- **Clean Code**: Easy to read and maintain
- **Multilingual**: Hebrew (RTL), English, French, Russian

## 🚀 Quick Start

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run with hot reload (changes appear instantly)
streamlit run app.py --server.runOnSave true
```

### Development Commands
```bash
# Run tests
pytest tests/ -v

# Format code
black app/ tests/

# Check code quality
flake8 app/ tests/
```

## �� Project Structure
```
app/
├── main.py              # Main Streamlit app
├── components/          # UI components (header, grids, popups)
├── services/           # Business logic (Supabase, API calls)
├── utils/              # Helpers (validation, i18n)
└── config/             # Settings and constants

tests/
├── unit/               # Unit tests
├── integration/        # Integration tests
└── conftest.py         # Test configuration
```

##  Testing Strategy

### Write Tests For Everything
- **Functions**: Every function needs unit tests
- **Components**: Test UI components
- **Services**: Test Supabase and API calls
- **Edge Cases**: Test invalid inputs, errors

### Example Test
```python
# tests/unit/test_validation.py
def test_validate_name():
    assert validate_name("John") == True
    assert validate_name("A" * 36) == False  # Too long
```

## 🔄 Hot Reload Setup
Streamlit automatically reloads when you save files. Just run:
```bash
streamlit run app.py --server.runOnSave true
```

## 📝 Code Standards

### Must Follow
- **Type hints**: `def get_user(name: str) -> User:`
- **Docstrings**: Document every function
- **Clean functions**: One responsibility per function
- **Meaningful names**: `get_categories()` not `get_data()`

### Example Good Code
```python
def validate_user_data(name: str, user_id: str, phone: str) -> ValidationResult:
    """
    Validate user input data.
    
    Args:
        name: User's name (max 35 chars)
        user_id: User's ID (max 12 digits)
        phone: User's phone (max 15 digits)
    
    Returns:
        ValidationResult with success status and errors
    """
    errors = []
    
    if len(name) > 35:
        errors.append("Name too long")
    
    if not user_id.isdigit() or len(user_id) > 12:
        errors.append("Invalid ID")
    
    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors
    )
```

## 🎨 Component Guidelines

### Create Reusable Components
```python
# app/components/grid_view.py
def create_grid(items: List[dict], on_click: Callable) -> None:
    """Create responsive grid with items."""
    cols = st.columns(3)  # Responsive
    for item in items:
        # Grid item logic
        pass
```

### State Management
```python
# Use session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "categories"
```

## 🌍 Multilingual Support

### Translation Structure
```python
# app/utils/i18n.py
TRANSLATIONS = {
    "en": {"welcome": "Welcome"},
    "he": {"welcome": "ברוכים הבאים"},
    "fr": {"welcome": "Bienvenue"},
    "ru": {"welcome": "Добро пожаловать"}
}

def t(key: str, lang: str = "en") -> str:
    return TRANSLATIONS[lang].get(key, key)
```

## 🚨 Error Handling

### Always Handle Errors
```python
try:
    data = supabase.get_categories()
except Exception as e:
    st.error(f"Failed to load: {e}")
    return []
```

## 📱 Mobile Support

### Responsive Design
- **Desktop**: 3-4 items per row
- **Tablet**: 2-3 items per row  
- **Mobile**: 1-2 items per row

## 🔧 Development Workflow

### Daily Workflow
1. **Start**: `streamlit run app.py --server.runOnSave true`
2. **Code**: Make changes, see them instantly
3. **Test**: `pytest tests/ -v`
4. **Format**: `black app/ tests/`
5. **Commit**: When tests pass

### Before Committing
- [ ] All tests pass
- [ ] Code formatted with Black
- [ ] No linting errors
- [ ] Functions documented
- [ ] Type hints added

## 🎯 Key Principles

### 1. Test First
Write tests before or with your code, not after.

### 2. Hot Reload
Always run with `--server.runOnSave true` for instant feedback.

### 3. Clean Code
- Functions do one thing
- Meaningful variable names
- No magic numbers
- Clear comments

### 4. Error Handling
Never let the app crash - always handle errors gracefully.

### 5. Mobile First
Design for mobile, enhance for desktop.

## 🎯 Ready to Start?

1. **Setup**: Install dependencies and run with hot reload
2. **Structure**: Follow the project structure above
3. **Test**: Write tests for everything
4. **Code**: Follow clean code principles
5. **Iterate**: Make changes, see them instantly, test, repeat

This is your single source of truth for development! 

## Environment Configuration for Debug and Release

To safely manage environment variables for different modes:

- Maintain two separate environment files:
  - `.env.debug` for development/debug mode
  - `.env.release` for production/release mode
- Before running the app, copy the appropriate file to `.env`:
  - For debug: `cp .env.debug .env`
  - For release: `cp .env.release .env`
- This ensures you never accidentally use production credentials in development, or vice versa.
- The `.env` file is loaded automatically by the application at startup. 

## Supabase SSL Certificate

If you need to use a custom SSL certificate for Supabase:
- Place your certificate file (e.g., prod-ca-2021.crt) in a `certs/` directory at the project root.
- Add this to your `.env.debug` or `.env.release`:
  ```
  SUPABASE_SSL_CERT=certs/prod-ca-2021.crt
  ```
- The app will use this certificate for secure Supabase connections if specified. 
- Use use_container_width instead of depcrecated use_column_width
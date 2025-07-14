import re
from app.utils.models import ValidationResult

def validate_user_data(user_data):
    """Validate user input data. Returns ValidationResult."""
    errors = []
    # First name
    if not user_data.first_name or len(user_data.first_name) > 35:
        errors.append("first_name")
    # Last name
    if not user_data.last_name or len(user_data.last_name) > 35:
        errors.append("last_name")
    # ID
    if not user_data.user_id.isdigit() or len(user_data.user_id) > 12:
        errors.append("user_id")
    # Phone
    if not user_data.phone.isdigit() or len(user_data.phone) > 15:
        errors.append("phone")
    # Email (optional)
    if user_data.email:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, user_data.email):
            errors.append("email")
    return ValidationResult(is_valid=len(errors) == 0, errors=errors) 
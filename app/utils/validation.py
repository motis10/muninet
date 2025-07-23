import re
from app.utils.models import ValidationResult

# Phone validation for Israeli numbers
def validate_israeli_phone(phone: str) -> bool:
    """Liberal validation for Israeli phone numbers"""
    if not phone:
        return False
    
    # Remove all non-digit characters except plus
    clean_phone = re.sub(r'[\s\-\(\)\.\_]', '', phone)
    
    # Handle international formats first
    if clean_phone.startswith('+972'):
        clean_phone = '0' + clean_phone[4:]  # Convert +972 to 0
    elif clean_phone.startswith('972'):
        clean_phone = '0' + clean_phone[3:]  # Convert 972 to 0
    
    # Remove any remaining non-digits
    clean_phone = re.sub(r'[^\d]', '', clean_phone)
    
    # Very liberal validation - accept most reasonable phone number lengths
    if len(clean_phone) >= 7 and len(clean_phone) <= 15:
        # Must start with 0 for Israeli numbers, or be international
        if clean_phone.startswith('0'):
            return True
        # Or be a reasonable length without country code
        if len(clean_phone) >= 7 and len(clean_phone) <= 10:
            return True
    
    # Accept international numbers without +972
    if len(clean_phone) >= 10 and len(clean_phone) <= 15:
        return True
    
    return False

# Update the main validation function:
def validate_user_data(user_data):
    """Validate user input data. Returns ValidationResult."""
    errors = []
    # First name
    if not user_data.first_name or len(user_data.first_name) > 35:
        errors.append("first_name")
    # Last name
    if not user_data.last_name or len(user_data.last_name) > 35:
        errors.append("last_name")
    # ID (optional) - Israeli ID is 9 digits
    if user_data.user_id and (not user_data.user_id.isdigit() or len(user_data.user_id) != 9):
        errors.append("user_id")
    # Phone - Use Israeli validation
    if not validate_israeli_phone(user_data.phone):
        errors.append("phone")
    # Email (optional)
    if user_data.email:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, user_data.email):
            errors.append("email")
    return ValidationResult(is_valid=len(errors) == 0, errors=errors) 